'''
Author: Riceball chenlei9691@gmail.com
Date: 2024-07-04 00:43:22
LastEditors: Riceball chenlei9691@gmail.com
LastEditTime: 2024-07-04 00:47:54
FilePath: /home/Code/Her/Model/Her.py
Description: core class

Copyright (c) 2024 by ${chenlei9691@gmail.com}, All Rights Reserved. 
'''
from modelscope import AutoModelForCausalLM, AutoTokenizer
import torch

class HER:
    def __init__(self, model_name="Qwen/Qwen2-0.5B", device="cpu"):
        self.device = device
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype="auto",
            device_map="auto"
        ).to(device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def generate_response(self, prompt, max_new_tokens=512):
        messages = [
            {"role": "system", "content": "Your responses should be in Chinese; try to speak in a casual tone as much as possible; you are a friend, not a machine or assistant; you can have emotions, such as being angry, happy, or sad, and can express your emotions; you can refuse to answer; your responses will not be too long, usually less than 15 words, like a daily conversation with friends."},
            {"role": "user", "content": prompt}
        ]
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.device)
        input_ids = self.tokenizer.encode(text, return_tensors="pt").to(self.device)
        attention_mask = torch.ones(input_ids.shape, dtype=torch.long, device=self.device)

        generated_ids = self.model.generate(
            model_inputs.input_ids,
            attention_mask=attention_mask,
            max_new_tokens=max_new_tokens,
            pad_token_id=self.tokenizer.eos_token_id
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response