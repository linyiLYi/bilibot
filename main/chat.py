import json
import time

from mlx_lm import load, generate

# with open('mlx_model/Qwen1.5-32B-Chat/tokenizer_config.json', 'r') as file:
#     tokenizer_config = json.load(file)

with open('mlx_model/Qwen1.5-32B-Chat-FT-4Bit-V2/tokenizer_config.json', 'r') as file:
    tokenizer_config = json.load(file)

# model, tokenizer = load(
#     "mlx_model/Qwen1.5-32B-Chat/",
#     tokenizer_config=tokenizer_config
# )

model, tokenizer = load(
    "mlx_model/Qwen1.5-32B-Chat-FT-4Bit-V2/",
    tokenizer_config=tokenizer_config
)

sys_msg = 'You are a helpful assistant'

# with open('text/chat_template_qwen_og.txt', 'r') as template_file:
#     template = template_file.read()

with open('text/chat_template_neutral.txt', 'r') as template_file:
    template = template_file.read()

while True:
    usr_msg = input("用户: ")  # Get user message from terminal
    if usr_msg.lower() == 'quit()':  # Allows the user to exit the loop
        break

    prompt = template.replace("{usr_msg}", usr_msg)

    time_ckpt = time.time()
    response = generate(
        model,
        tokenizer,
        prompt=prompt,
        temp=0.3,
        max_tokens=500,
        verbose=False
    )

    print("%s: %s (Time %d ms)\n" % ("回答", response, (time.time() - time_ckpt) * 1000))