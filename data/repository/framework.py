import data.repository.imports

from .components import ComponentBase

class Framework():

    def __init__(self):
        
        self.speechrecognition = ComponentBase.get_component("SpeechRecognition")().start_listening()

        # smalltalk = ComponentBase.get_component("SmallTalk")

        # while(True):
        #     question = input("Question: ")
        #     print("response: {}".format(smalltalk.ask(question)))


        