import io
import re
import json
import time
import wave
import requests
import simpleaudio as sa
from flask import Flask, render_template, request, jsonify
from mlx_lm import load, generate

app = Flask(__name__)

def generate_speech(text, port):
    time_ckpt = time.time()
    data = {
        "text": text,
        "text_language": "zh"
    }
    response = requests.post(f"http://127.0.0.1:{port}", json=data)
    if response.status_code == 400:
        raise Exception(f"GPT-SoVITS ERROR: {response.message}")
    audio_data = io.BytesIO(response.content)
    with wave.open(audio_data, 'rb') as wave_read:
        audio_frames = wave_read.readframes(wave_read.getnframes())
        audio_wave_obj = sa.WaveObject(audio_frames, wave_read.getnchannels(), wave_read.getsampwidth(), wave_read.getframerate())
    play_obj = audio_wave_obj.play()
    play_obj.wait_done()
    print("Audio Generation Time: %d ms\n" % ((time.time() - time_ckpt) * 1000))

def split_text(text):
    sentence_endings = ['！', '。', '？']
    for punctuation in sentence_endings:
        text = text.replace(punctuation, punctuation + '\n')
    pattern = r'\[.*?\]'
    text = re.sub(pattern, '', text)
    return text

# Load model and tokenizer
with open('../models/Qwen1.5-32B-Chat-FT-4Bit/tokenizer_config.json', 'r') as file:
    tokenizer_config = json.load(file)

model, tokenizer = load(
    "../models/Qwen1.5-32B-Chat-FT-4Bit/",
    tokenizer_config=tokenizer_config
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_response():
    question = request.form['question']
    question = split_text(question)
    
    # Generate speech for the question
    generate_speech(question, 9880)

    sys_msg = 'You are a helpful assistant'
    template = '你是一个友好的助手。请回答以下问题：{usr_msg}'
    prompt = template.replace("{usr_msg}", question)

    # Generate the response
    time_ckpt = time.time()
    response = generate(
        model,
        tokenizer,
        prompt=prompt,
        temp=0.3,
        max_tokens=500,
        verbose=False
    )

    print("%s: %s (Time %d ms)\n" % ("哔友", response, (time.time() - time_ckpt) * 1000))
    
    response = split_text(response)
    # Generate speech for the response
    generate_speech(response, 9881)

    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=10000)
