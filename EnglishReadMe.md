# Bilibili Chatbot

A locally trained chatbot refined from user comments on [Bilibili](https://bilibili.com). It supports text-based chatting and can also generate voice conversations based on the provided questions in `questions.txt`.

The core text generation model used in this project is [Qwen1.5-32B-Chat](https://huggingface.co/Qwen/Qwen1.5-32B-Chat), fine-tuned using Apple's [mlx-lm LORA example project](https://github.com/ml-explore/mlx-examples/blob/main/llms/mlx_lm/LORA.md). The voice generation component is based on the open-source project [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS), and the voice questions are trained by Bilibili user [Employee No. 1145 from the Cabbage Factory](https://space.bilibili.com/518098961).

### File Structure

The main scripts of the project are stored in the `main/` directory, and the models are stored in the `models/` directory. Prompt templates and the list of questions are stored in the `text/` directory. `tools/compress_model.py` can be used to quantize and compress the complete model, significantly speeding up the content generation process.

## Running Guide

This project is based on the Python programming language, and the program is run using Python version 3.10. It is recommended to use [Anaconda](https://www.anaconda.com) to set up the Python environment. The configuration process below has been tested on macOS.

### Environment Setup

```bash
conda create -n bilibot python=3.10
conda activate bilibot
cd bilibot
pip install -r requirements.txt
```
### Model Fine-tuning and Inference Testing

Using command-line instructions, fine-tune Qwen1.5-32B-Chat with mlx-lm:

```bash
python -m mlx_lm.lora --model models/Qwen1.5-32B-Chat --data data/ --train --iters 1000 --batch-size 16 --lora-layers 12
```

Merge the fine-tuned adapters file with the base model:

```bash
python -m mlx_lm.fuse --model models/Qwen1.5-32B-Chat --save-path models/Qwen1.5-32B-Chat-FT --adapter-path models/Qwen1.5-32B-Chat-Adapters
```
Quantize the merged model for acceleration:

```bash
python tools/compress_model.py
```

Test the dialogue with the fine-tuned model:

```bash
python chat.py
```

## Voice Generation

This project utilizes the open-source project GPT-SoVITS for voice generation.

First, refer to the official guide of GPT-SoVITS to set up the environment and run the voice generation program:

```bash
conda create -n GPTSOVITS python=3.9
conda activate GPTSOVITS
cd GPT-SoVITS
pip install -r requirements.txt
python webui.py
```
Run the API program to provide voice generation services for Paimon and Lin Yi using ports 9880 and 9881 respectively. Complete this step using the GPT-SoVITS codebase:

```bash
python api.py -s SoVITS_weights/paimeng2_e110_s159940.pth -g GPT_weights/paimeng2-e10.ckpt -dr samples/Paimon/疑问—哇，这个，还有这个…只是和史莱姆打了一场，就有这么多结论吗？.wav -dt "哇，这个，还有这个…只是和史莱姆打了一场，就有这么多结论吗？" -dl "zh" -a 127.0.0.1 -p 9880
python api.py -s SoVITS_weights/linyi_e25_s1150.pth -g GPT_weights/linyi-e50.ckpt -dr "samples/linyi/【愤怒】你这问题太弱智了，我都不知道该从哪开始骂你。.WAV" -dt "你这问题太弱智了，我都不知道该从哪开始骂你。" -dl "zh" -a 127.0.0.1 -p 9881

```

Run the question-answer generation program:

```bash
python start_qa_dialogue.py
```

## References

1. MLX machine learning framework from Apple Machine Learning Research Group: [https://github.com/ml-explore/mlx](https://github.com/ml-explore/mlx)
2. Alibaba's Qwen1.5 Question-Answering Model: [https://qwenlm.github.io/zh/blog/qwen1.5/](https://qwenlm.github.io/zh/blog/qwen1.5/)
3. Open-source Text-to-Speech project GPT-SoVITS, by Huaer Bucry: [https://github.com/RVC-Boss/GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS)
4. Paimon's voice model, by Employee No. 1145 from the Cabbage Factory: [【GPT-SoVITS】30-hour large dataset test, is more time spent really useful?](https://www.bilibili.com/video/BV1Yu4m1N79m)

