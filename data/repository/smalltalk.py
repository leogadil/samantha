from .components import ComponentBase

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class SmallTalk(ComponentBase):
    
    tokenizer = AutoTokenizer.from_pretrained("r3dhummingbird/DialoGPT-medium-joshua")
    model = AutoModelForCausalLM.from_pretrained("r3dhummingbird/DialoGPT-medium-joshua")

    intro = ""

    __chat_history_ids = None
    turn = 0 
        
    # pre_input = tokenizer.encode(intro + tokenizer.eos_token, return_tensors='pt')
    # __chat_history_ids = model.generate(pre_input, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    @classmethod
    def ask(cls, question):
        if cls.turn > 4:
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