import datetime
import os
import random
import sys
from string import punctuation

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './data/repository')))

import nltk
import numpy as np
from tensorflow.keras import models
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam

from .components import ComponentBase
from .helper import load_json, save_json
from .nlp import nlp

nltk.download('omw-1.4')

class Trainer_Model:

    words = []
    classes = []
    doc_x = []
    doc_y = []

    def __init__(self, intents) -> None:
        # Load the model
        for intent in load_json(intents)['intents']:
            if 'skip' in intent and intent['skip']:
                continue

            for pattern in intent['patterns']:
                tokens = nlp.tokenize(pattern)
                self.words.extend(tokens)
                self.doc_x.append(pattern)
                self.doc_y.append(intent['tag'])

            if intent['tag'] not in self.classes:
                self.classes.append(intent['tag'])

        self.words = [nlp.lemmatize(word.lower()) for word in self.words if word not in punctuation]

        self.words = sorted(set(self.words))
        self.classes = sorted(set(self.classes))

class Recognizer_Model:

    def __init__(self, model) -> None:
        self.model_path = model
        self.metadata = load_json(self.model_path + 'intent_metadata.json')
        self.vocab = self.metadata['vocab']
        self.labels = self.metadata['classes']
        self.model = models.load_model(self.model_path + 'intent_model.h5')

    def __call__(self, *args: any, **kwds: any) -> any:
        return self.model.predict(args[0])

class Recognizer(ComponentBase):

    def __init__(self, model_path):
        # Load the model
        print("loading model")
        self.model = Recognizer_Model(model_path)

    def recognize(self, str):
        bow = nlp.bag_of_words(str.lower(), self.model.vocab)
        result = self.model(np.array([bow]))[0]

        y_pred = [[i, res] for i, res in enumerate(result) if res > 0.5]
        y_pred.sort(key=lambda x: x[1], reverse=True)

        return self.model.labels[y_pred[0][0]]

class Trainer(ComponentBase):

    epochs = 500
    batch_size = 64
    verbose = 1

    def __init__(self, intents_path, test_after=False, model_path='./data/repository/models/') -> None:
        # Load the intent data
        print("loading intents")
        metadata = Trainer_Model(intents_path)
        train_x, train_y = self.prepare_data(metadata)
        training_model = self.create_model(train_x, train_y)
        trained_model = self.train(training_model, train_x, train_y)
        self.test_after = test_after
        if self.test_after:
            self.result = self.test_model(trained_model, train_x, train_y)

        self.save_model(metadata, trained_model, model_path)

    def get_report(self) -> str:
        if not self.test_after:
            return 'add test_after=True to the Trainer constructor to test the model'

        return self.result
    
    
    def prepare_data(self, model: Trainer_Model):
        training = []
        out_empty = [0] * len(model.classes)

        for i, doc in enumerate(model.doc_x):
            bow = []
            text = nlp.lemmatize(doc.lower())

            for word in model.words:
                bow.append(1) if word in text else bow.append(0)

            output_row = list(out_empty)
            output_row[model.classes.index(model.doc_y[i])] = 1

            training.append([bow, output_row])

        random.shuffle(training)
        training = np.array(training, dtype=object)

        return np.array(list(training[:, 0])), np.array(list(training[:, 1]))

    def create_model(self, train_x, train_y):
        model = models.Sequential()
        model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(train_y[0]), activation='softmax'))
        adam = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
        model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
        print(model.summary())

        return model

    def train(self, model, train_x, train_y):
        model.fit(train_x, train_y, epochs=self.epochs, batch_size=self.batch_size, verbose=self.verbose)

        return model

    def test_model(self, model, test_x, test_y) -> str:
        ypred = model.predict(test_x, verbose=self.verbose)
        ypred = np.argmax(ypred, axis=1)

        model_score = model.evaluate(test_x, test_y, verbose=self.verbose)
        
        result = '\nModel Classification Report:'
        result += '\nAccuracy: ' + str(model_score[1])
        result += '\nLoss: ' + str(model_score[0])
        result += '\n'

        return result
    
    def save_model(self, model_data, model, model_path) -> any:
        model.save(model_path + f'intent_model.h5')
        save_json({
            'vocab': model_data.words,
            'classes': model_data.classes,
            'date': str(datetime.datetime.now())
        }, model_path + f'intent_metadata.json')

        print('Trainer_Model saved to', model_path + f'intent_model.h5')
        print('Trainer_Model metadata saved to', model_path + f'intent_metadata.json')
