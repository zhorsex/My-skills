---
name: qwen3-tts
description: Qwen3-TTS 使用示例 - 基础、语音设计、语音克隆等实际用例
license: Apache 2.0. See LICENSE.txt for details
---

# Qwen3-TTS 使用示例

## 基础示例

### 单语言文本转语音

```python
from qwen3_tts import Qwen3TTSModel, Qwen3TTSTokenizer
from io import BytesIO
import scipy.io.wavfile as wavfile
import torch

# 选择 GPU 设备
device = "cuda" if torch.cuda.is_available() else "cpu"

# 初始化模型和分词器
tokenizer = Qwen3TTSTokenizer.from_pretrained("Qwen/Qwen3-1.5B-Base-TTS")
model = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-1.5B-Base-TTS", device=device)

# 输入文本
text = "你好，我是 Qwen3-TTS 语音合成模型。支持多语言合成，包括中文、英文、日文、韩文等。"

# 生成语音
audio_input = tokenizer(text, return_tensors="pt", device=device).input_ids
with torch.no_grad():
    audio_output = model.generate(audio_input)

# 保存为 WAV 文件
audio_numpy = audio_output.cpu().numpy().squeeze(-1)
wavfile.write("qwen3_tts_demo.wav", 22050, audio_numpy)

print("语音已保存为 qwen3_tts_demo.wav")
```

### 多语言文本转语音

```python
# 多语言示例
texts = {
    "中文": "今天天气真不错！",
    "英文": "The weather today is wonderful!",
    "日文": "今日は本当にいい天気ですね！",
    "韩文": "오늘 날씨가 정말 좋아요!",
    "德文": "Das Wetter heute ist wunderbar!",
    "法文": "Le temps est magnifique aujourd'hui!",
    "西班牙文": "¡El clima hoy está maravilloso!",
    "俄文": "Сегодня прекрасная погода!",
    "阿拉伯文": "الطقس اليوم رائع!",
    "意大利文": "Il tempo oggi è meraviglioso!"
}

for lang, text in texts.items():
    audio_input = tokenizer(text, return_tensors="pt", device=device).input_ids
    with torch.no_grad():
        audio_output = model.generate(audio_input)

    audio_numpy = audio_output.cpu().numpy().squeeze(-1)
    wavfile.write(f"tts_{lang}.wav", 22050, audio_numpy)
    print(f"已生成语音: tts_{lang}.wav")
```

## 语音设计示例

### 创建角色语音

```python
# 角色音频文件
character_audio_path = "voice_samples/chef_voice.wav"

# 情感提示词
emotion_prompt = "一位经验丰富的厨师，声音温暖、热情，像在教人做菜"

# 设计角色语音
with open(character_audio_path, "rb") as f:
    character_audio = f.read()

design_request = [
    {
        "role": "user",
        "content": [
            {"type": "audio", "audio": character_audio},
            {"type": "text", "text": emotion_prompt}
        ]
    }
]

# 生成设计语音
designed_audio = model.chat(design_request, generate_audio=True)

# 保存结果
wavfile.write("designed_chef_voice.wav", 24000, designed_audio.cpu().numpy().squeeze(-1))
print("角色语音已设计完成: designed_chef_voice.wav")
```

### 多角色场景

```python
# 为故事创建多个角色
characters = [
    {
        "name": "爷爷",
        "audio": "voice_samples/grandpa.wav",
        "prompt": "和蔼可亲的爷爷，说话缓慢、稳重，带有岁月的沧桑感"
    },
    {
        "name": "孙女",
        "audio": "voice_samples/granddaughter.wav",
        "prompt": "活泼可爱的女孩，声音清脆、充满活力"
    }
]

for char in characters:
    with open(char["audio"], "rb") as f:
        audio_data = f.read()

    design_request = [
        {
            "role": "user",
            "content": [
                {"type": "audio", "audio": audio_data},
                {"type": "text", "text": char["prompt"]}
            ]
        }
    ]

    designed_audio = model.chat(design_request, generate_audio=True)
    wavfile.write(f"voice_{char['name']}.wav", 24000, designed_audio.cpu().numpy().squeeze(-1))
    print(f"已创建角色语音: {char['name']}")
```

## 语音克隆示例

### 基础语音克隆

```python
# 使用 CustomVoice 模型
tokenizer = Qwen3TTSTokenizer.from_pretrained("Qwen/Qwen3-1.5B-CustomVoice-TTS")
model = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-1.5B-CustomVoice-TTS", device=device)

# 参考音频文件
audio_path = "voice_samples/target_voice.wav"

# 目标文本
target_text = "这是语音克隆的效果，你可以尝试任何你想要的文本。"

# 执行语音克隆
with open(audio_path, "rb") as f:
    reference_audio = f.read()

clone_request = [
    {
        "role": "user",
        "content": [
            {"type": "audio", "audio": reference_audio},
            {"type": "text", "text": target_text}
        ]
    }
]

with torch.no_grad():
    cloned_audio = model.chat(clone_request, generate_audio=True)

wavfile.write("cloned_voice.wav", 24000, cloned_audio.cpu().numpy().squeeze(-1))
print("语音克隆完成: cloned_voice.wav")
```

### 使用 URL 音频进行克隆

```python
# 从远程 URL 获取音频
import requests

# 示例音频 URL（需替换为实际可访问的 URL）
audio_url = "https://example.com/sample_audio.wav"

# 下载音频
response = requests.get(audio_url)
remote_audio = response.content

# 使用远程音频进行克隆
clone_request = [
    {
        "role": "user",
        "content": [
            {"type": "audio", "audio": remote_audio},
            {"type": "text", "text": "这段语音使用网络音频进行克隆。"}
        ]
    }
]

cloned_audio = model.chat(clone_request, generate_audio=True)
wavfile.write("url_cloned_voice.wav", 24000, cloned_audio.cpu().numpy().squeeze(-1))
print("使用 URL 音频克隆完成")
```

### 批量语音克隆

```python
# 批量处理多个音频
audio_files = [
    {"path": "voice_samples/voice1.wav", "text": "这是第一段文本。"},
    {"path": "voice_samples/voice2.wav", "text": "这是第二段文本。"},
    {"path": "voice_samples/voice3.wav", "text": "这是第三段文本。"}
]

for item in audio_files:
    with open(item["path"], "rb") as f:
        audio_data = f.read()

    clone_request = [
        {
            "role": "user",
            "content": [
                {"type": "audio", "audio": audio_data},
                {"type": "text", "text": item["text"]}
            ]
        }
    ]

    cloned_audio = model.chat(clone_request, generate_audio=True)
    output_name = item["path"].split("/")[-1].replace(".wav", "_cloned.wav")
    wavfile.write(output_name, 24000, cloned_audio.cpu().numpy().squeeze(-1))
    print(f"已处理: {output_name}")
```
