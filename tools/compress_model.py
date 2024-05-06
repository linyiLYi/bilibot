from mlx_lm import convert

# Compress Qwen1.5-32B-Chat.
convert(
    "models/Qwen1.5-32B-Chat",
    mlx_path="mlx_model/Qwen1.5-32B-Chat",
    quantize=True
)

# Compress fine-tuned Qwen1.5-32B-Chat.
# convert(
#     "models/Qwen1.5-32B-Chat-FT", 
#     mlx_path="models/Qwen1.5-32B-Chat-FT-4Bit",
#     quantize=True
# )