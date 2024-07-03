'''
Author: Riceball chenlei9691@gmail.com
Date: 2024-07-03 23:01:09
LastEditors: Riceball chenlei9691@gmail.com
LastEditTime: 2024-07-03 23:45:01
FilePath: /home/Code/Her/app.py
Description: 

Copyright (c) 2024 by ${chenlei9691@gmail.com}, All Rights Reserved. 
'''
# Load model directly
from modelscope import AutoModelForCausalLM, AutoTokenizer
import torch
device = "cpu" # the device to load the model onto

# Now you do not need to add "trust_remote_code=True"
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2-0.5B",
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-0.5B")

# Instead of using model.chat(), we directly use model.generate()
# But you need to use tokenizer.apply_chat_template() to format your inputs as shown below
prompt = "Give me a short introduction to large language model."
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
model_inputs = tokenizer([text], return_tensors="pt").to(device)
input_ids = tokenizer.encode(text, return_tensors="pt")
attention_mask = torch.ones(input_ids.shape, dtype=torch.long, device=device)

# Directly use generate() and tokenizer.decode() to get the output.
# Use `max_new_tokens` to control the maximum output length.
generated_ids = model.generate(
    model_inputs.input_ids,
    attention_mask=attention_mask,
    max_new_tokens=512,
    pad_token_id=tokenizer.eos_token_id
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

print(response)