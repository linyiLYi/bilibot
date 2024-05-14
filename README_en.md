# Bilibot

This repository is a local chatbot finetuned using a dataset consisted from comments in [Bilibili](https://bilibili.com). It supports pure text input, you can also use tts for its output using `questions.txt`.

This repository uses [Qwen1.5-32B-Chat](https://huggingface.co/Qwen/Qwen1.5-32B-Chat) as the base model for text generation. It fine-tunes the base model with the help of Apple's [mlx-lm LORA example repository](https://github.com/ml-explore/mlx-examples/blob/main/llms/mlx_lm/LORA.md). Voice generation part is based on [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS). Paimon voice model (generates the audio for questions) is trained by [白菜工厂1145号员工](https://space.bilibili.com/518098961).

### File structure

The main files of this repository are located in the `main/` folder, and the models are stored in the `models/` folder. Prompt templates and question lists are stored in the `text/` folder. `tools/compress_model.py` can quantize and compress the full model, hence greatly improving the inference speed.

## Usage

This repository is based on Python 3.10. It is recommended to use [Anaconda](https://www.anaconda.com) to configure the Python environment. The following process has been tested on macOS.


### Environment setup

```
conda create -n bilibot python=3.10
conda activate bilibot
cd bilibot
pip install -r requirements.txt
```

### Fine-Tuning, Training and Inference 

Use console to fine-tune Qwen1.5-32B-Chat using [mlx-lm](https://github.com/ml-explore/mlx-examples/blob/main/llms/mlx_lm/LORA.md):

```
python -m mlx_lm.lora --model models/Qwen1.5-32B-Chat --data data/ --train --iters 1000 --batch-size 16 --lora-layers 12
```

Merge the fine-tuned `adapters` files with the base model:

```
python -m mlx_lm.fuse --model models/Qwen1.5-32B-Chat --save-path models/Qwen1.5-32B-Chat-FT --adapter-path models/Qwen1.5-32B-Chat-Adapters
```

Quantize the merged model for acceleration:
```
python tools/compress_model.py
```

Inference
```
python chat.py
```
### TTS
This repository uses [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) for voice generation.

First, refer to the official guide of [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) to set up the environment and run the webui.

```
conda create -n GPTSOVITS python=3.9
conda activate GPTSOVITS
cd GPT-SoVITS
pip install -r requirements.txt
python webui.py
```

Run the API to provide TTS for Paimon and Lin Yi using ports 9880 and 9881 respectively. Please use the GPT-SoVITS codebase to complete the following:
```
python api.py -s SoVITS_weights/paimeng2_e110_s159940.pth -g GPT_weights/paimeng2-e10.ckpt -dr samples/Paimon/疑问—哇，这个，还有这个…只是和史莱姆打了一场，就有这么多结论吗？.wav -dt "哇，这个，还有这个…只是和史莱姆打了一场，就有这么多结论吗？" -dl "zh" -a 127.0.0.1 -p 9880
python api.py -s SoVITS_weights/linyi_e25_s1150.pth -g GPT_weights/linyi-e50.ckpt -dr "samples/linyi/【愤怒】你这问题太弱智了，我都不知道该从哪开始骂你。.WAV" -dt "你这问题太弱智了，我都不知道该从哪开始骂你。" -dl "zh" -a 127.0.0.1 -p 9881
```

Start Q&A Dialogue
```
python start_qa_dialogue.py
```

## Credits

[MLX](https://github.com/ml-explore/mlx)

[Qwen 1.5](https://qwenlm.github.io/zh/blog/qwen1.5/)

[GPT-SovITS](https://github.com/RVC-Boss/GPT-SoVITS) from [花儿不哭](https://space.bilibili.com/5760446)

Paimon GPT-SoVITS model by [白菜工厂1145号员工](https://space.bilibili.com/518098961) （[Video:【GPT-SoVITS】30小时超大数据集测试，堆时长真的有用吗？](https://www.bilibili.com/video/BV1Yu4m1N79m))
