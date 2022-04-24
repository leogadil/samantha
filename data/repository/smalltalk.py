from .components import ComponentBase

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class SmallTalk(ComponentBase):

    __chat_history_ids = None
    turn = 0

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("r3dhummingbird/DialoGPT-medium-joshua")
        self.model = AutoModelForCausalLM.from_pretrained("r3dhummingbird/DialoGPT-medium-joshua")

    @classmethod
    def ask(cls, question):
        if cls.turn > 3:
            cls.__chat_history_ids = None
            cls.turn = 0

        question = question.lower()
        new_user_input_ids = cls.tokenizer.encode(question + cls.tokenizer.eos_token, return_tensors='pt')
        bot_input_ids = torch.cat([cls.__chat_history_ids, new_user_input_ids], dim=-1) if cls.__chat_history_ids is not None else new_user_input_ids
        cls.__chat_history_ids = cls.model.generate(
            bot_input_ids, max_length=200,
            pad_token_id=cls.tokenizer.eos_token_id,  
            no_repeat_ngram_size=3,       
            do_sample=True, 
            top_k=100, 
            top_p=0.7,
            temperature=0.8
        )

        

        cls.turn += 1
        return cls.tokenizer.decode(cls.__chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)