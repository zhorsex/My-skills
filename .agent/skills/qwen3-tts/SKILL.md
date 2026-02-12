---
name: qwen3-tts
description: Qwen3-TTS 语音合成模型使用指南。支持 10 种语言的文本转语音、声音克隆、声音设计和自然语言语音控制。当用户需要进行以下任务时使用此技能：(1) 文本转语音合成，(2) 使用预设音色生成语音，(3) 3 秒快速声音克隆，(4) 自然语言描述自定义声音，(5) 多语言语音生成，(6) 流式实时语音生成
license: Apache 2.0. See LICENSE.txt for details
---

# Qwen3-TTS 语音合成

Qwen3-TTS 是阿里巴巴通义千问团队开发的强大语音合成模型系列，支持语音克隆、声音设计和高质量人声生成。

## 概述

### 支持的语言

- 中文、英语、日语、韩语
- 德语、法语、俄语、葡萄牙语、西班牙语、意大利语

### 核心特性

- **端到端语音建模**：基于离散多码本 LM 架构
- **极低延迟流式生成**：单字符输入后 97ms 延迟
- **自然语言语音控制**：支持多维度声学属性控制（音色、情感、韵律）
- **智能文本理解**：自适应语调、语速和情感表达

## 模型类型

| 模型 | 功能 | 支持语言 | 流式 | 指令控制 |
|------|------|---------|------|----------|
| Qwen3-TTS-12Hz-1.7B-VoiceDesign | 声音设计 | 10 种语言 | ✅ | ✅ |
| Qwen3-TTS-12Hz-1.7B-CustomVoice | 9 种预设音色 | 10 种语言 | ✅ | ✅ |
| Qwen3-TTS-12Hz-1.7B-Base | 语音克隆基座 | 10 种语言 | ✅ | - |
| Qwen3-TTS-12Hz-0.6B-CustomVoice | 9 种预设音色 | 10 种语言 | ✅ | - |
| Qwen3-TTS-12Hz-0.6B-Base | 语音克隆基座 | 10 种语言 | ✅ | - |

## 安装

### 基础安装

```bash
pip install -U qwen-tts
```

### 推荐安装（包含 FlashAttention 2）

```bash
pip install -U qwen-tts flash-attn --no-build-isolation
```

### 从源码安装

```bash
git clone https://github.com/QwenLM/Qwen3-TTS.git
cd Qwen3-TTS
pip install -e .
```

## Python 库

### 基础用法

#### 1. 使用预设音色生成语音

适用于 CustomVoice 模型，支持 9 种预设音色：

```python
import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel

model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
    device_map="cuda:0",
    dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",
)

# 单文本生成
wavs, sr = model.generate_custom_voice(
    text="其实我真的有发现，我是一个特别善于观察别人情绪的人。",
    language="Chinese",
    speaker="Vivian",
    instruct="用特别愤怒的语气说"
)
sf.write("output.wav", wavs[0], sr)
```

**预设音色列表：**

| 音色 | 描述 | 母语 |
|------|------|------|
| Vivian | 明亮、略带棱角的年轻女声 | 中文 |
| Serena | 温柔、温和的年轻女声 | 中文 |
| Uncle_Fu | 经验丰富、低沉浑厚的男声 | 中文 |
| Dylan | 年轻北京男声，清晰自然 | 中文（京腔） |
| Eric | 活跃成都男声，略带沙哑明亮 | 中文（四川话） |
| Ryan | 动感男声，节奏感强 | 英语 |
| Aiden | 阳光美国男声，中音清晰 | 英语 |
| Ono_Anna | 活泼日本女声，轻盈灵巧 | 日语 |
| Sohee | 温暖韩语女声，情感丰富 | 韩语 |

#### 2. 声音设计

使用自然语言描述自定义声音：

```python
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
    device_map="cuda:0",
    dtype=torch.bfloat16,
)

wavs, sr = model.generate_voice_design(
    text="哥哥，你回来啦，人家等了你好久好久了，要抱抱！",
    language="Chinese",
    instruct="体现撒娇稚嫩的萝莉女声，音调偏高且起伏明显，营造出黏人、做作又刻意卖萌的听觉效果。"
)
sf.write("output.wav", wavs[0], sr)
```

#### 3. 语音克隆

使用 3 秒参考音频快速克隆声音：

```python
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    device_map="cuda:0",
    dtype=torch.bfloat16,
)

ref_audio = "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-TTS-Repo/clone.wav"
ref_text = "Okay. Yeah. I resent you. I love you. I respect you."

wavs, sr = model.generate_voice_clone(
    text="I am solving the equation.",
    language="English",
    ref_audio=ref_audio,
    ref_text=ref_text,
)
sf.write("output.wav", wavs[0], sr)
```

**音频输入格式支持：**
- 本地文件路径：`"path/to/audio.wav"`
- URL：`"https://example.com/audio.wav"`
- NumPy 数组：`(waveform, sample_rate)` 元组
- Base64 字符串

#### 4. 可复用的克隆提示词

```python
# 一次性构建提示词，避免重复计算
prompt_items = model.create_voice_clone_prompt(
    ref_audio=ref_audio,
    ref_text=ref_text,
)

# 多次复用
wavs, sr = model.generate_voice_clone(
    text=["句子 A", "句子 B"],
    language=["English", "English"],
    voice_clone_prompt=prompt_items,
)
```

#### 5. 声音设计后克隆

工作流程：
1. 使用 VoiceDesign 模型创建参考音频
2. 构建 reusable prompt
3. 使用 Base 模型批量生成

```python
# 步骤 1: 创建声音设计参考
design_model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
    device_map="cuda:0",
    dtype=torch.bfloat16,
)

ref_text = "H-hey! You dropped your... uh... calculus notebook?"
ref_instruct = "Male, 17 years old, tenor range, gaining confidence"
ref_wavs, sr = design_model.generate_voice_design(
    text=ref_text,
    language="English",
    instruct=ref_instruct
)

# 步骤 2: 构建提示词
clone_model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    device_map="cuda:0",
    dtype=torch.bfloat16,
)

voice_clone_prompt = clone_model.create_voice_clone_prompt(
    ref_audio=(ref_wavs[0], sr),
    ref_text=ref_text,
)

# 步骤 3: 批量生成
sentences = ["No problem!", "What? No!"]
wavs, sr = clone_model.generate_voice_clone(
    text=sentences,
    language=["English", "English"],
    voice_clone_prompt=voice_clone_prompt,
)
```

#### 6. 音频编解码

```python
from qwen_tts import Qwen3TTSTokenizer

tokenizer = Qwen3TTSTokenizer.from_pretrained(
    "Qwen/Qwen3-TTS-Tokenizer-12Hz",
    device_map="cuda:0",
)

# 编码
enc = tokenizer.encode("https://example.com/audio.wav")

# 解码
wavs, sr = tokenizer.decode(enc)
sf.write("output.wav", wavs[0], sr)
```

### 批量推理

```python
wavs, sr = model.generate_custom_voice(
    text=["你好世界", "Hello World", "こんにちは"],
    language=["Chinese", "English", "Japanese"],
    speaker=["Vivian", "Ryan", "Ono_Anna"],
    instruct=["开心", "", ""]
)
```

## Web UI 演示

### 启动本地演示

```bash
qwen-tts-demo Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice --ip 0.0.0.0 --port 8000
```

### HTTPS 模式（Base 模型推荐）

```bash
# 生成自签名证书
openssl req -x509 -newkey rsa:2048 \
  -keyout key.pem -out cert.pem \
  -days 365 -nodes \
  -subj "/CN=localhost"

# 启动 HTTPS 服务
qwen-tts-demo Qwen/Qwen3-TTS-12Hz-1.7B-Base \
  --ip 0.0.0.0 --port 8000 \
  --ssl-certfile cert.pem \
  --ssl-keyfile key.pem \
  --no-ssl-verify
```

访问 `https://localhost:8000`

## vLLM 支持

Qwen3-TTS 已支持 vLLM-Omni。详见 [vLLM-Omni 文档](https://docs.vllm.ai/projects/vllm-omni/en/latest/getting_started/quickstart/)。

### 离线推理

```bash
git clone https://github.com/vllm-project/vllm-omni.git
cd vllm-omni/examples/offline_inference/qwen3_tts
python end2end.py --query-type CustomVoice
```

## API 用法

阿里云 DashScope 提供 Qwen3-TTS 实时 API：

- [自定义语音 API（中文）](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime)
- [语音克隆 API（中文）](https://help.aliyun.com/zh/model-studio/qwen-voice-cloning)
- [声音设计 API（中文）](https://help.aliyun.com/zh/model-studio/qwen-voice-design)

## 参考

更多信息参见参考文件：
- [API 参考文档](references/api-reference.md)
- [使用示例](references/examples.md)
- [模型详细信息](references/model-info.md)
- [微调指南](references/finetuning.md)
