---
name: qwen3-tts
description: Qwen3-TTS 模型微调指南 - 自定义训练数据准备和训练流程
license: Apache 2.0. See LICENSE.txt for details
---

# Qwen3-TTS 模型微调指南

## 概述

Qwen3-TTS 支持在自定义数据集上进行微调，以适应特定领域、特定声音风格或特定应用场景。本指南将介绍数据准备、训练配置和推理优化。

## 数据准备

### 训练数据格式

微调 Qwen3-TTS 需要准备 JSONL 格式的训练数据，每行包含一个样本。

**基础格式**:
```json
{
  "text": "这段文字将被转换为语音。",
  "audio_path": "path/to/audio.wav"
}
```

**完整示例** (train.jsonl):
```json
{"text": "欢迎使用 Qwen3-TTS 语音合成系统。", "audio_path": "data/train/audio_001.wav"}
{"text": "我们提供多语言语音合成服务。", "audio_path": "data/train/audio_002.wav"}
{"text": "支持高质量语音设计和克隆功能。", "audio_path": "data/train/audio_003.wav"}
{"text": "本示例展示中文语音合成效果。", "audio_path": "data/train/audio_004.wav"}
```

### 音频要求

**格式要求**:
- 文件格式: WAV
- 采样率:
  - Base 模型: 16kHz / 22.05kHz / 24kHz
  - VoiceDesign 模型: 24kHz
  - CustomVoice 模型: 24kHz
- 位深度: 16-bit 或 24-bit
- 通道数: 单声道 (mono)

**质量要求**:
- 背景噪音: 尽可能低
- 音量一致: 各文件音量水平尽量一致
- 音频时长: 建议 2-10 秒，避免过短或过长
- 声音清晰度: 发音清晰，无口吃或明显错误

**数据量参考**:
- 最小数据集: 100 小时
- 推荐数据集: 500+ 小时
- 最佳效果: 1000+ 小时

### 数据集结构

```
fine_tuning_data/
├── train/
│   ├── train.jsonl
│   ├── audio_001.wav
│   ├── audio_002.wav
│   └── audio_003.wav
├── valid/
│   ├── valid.jsonl
│   ├── audio_001.wav
│   ├── audio_002.wav
│   └── audio_003.wav
└── test/
    ├── test.jsonl
    ├── audio_001.wav
    ├── audio_002.wav
    └── audio_003.wav
```

### 数据预处理

1. **音频格式转换**:
```bash
# 使用 ffmpeg 统一音频格式
for file in data/*.wav; do
  output=$(echo $file | sed 's/data/processed/')
  ffmpeg -i "$file" -ar 24000 -ac 1 -acodec pcm_s16le "$output"
done
```

2. **音频音量归一化**:
```bash
# 使用 sox 进行音量归一化
for file in processed/*.wav; do
  output=$(echo $file | sed 's/processed/normalized/')
  sox "$file" --norm "$output"
done
```

3. **音频质量检查**:
```python
import librosa
import numpy as np
from pathlib import Path

def check_audio_quality(audio_path, min_duration=0.5, max_duration=30.0):
    """检查音频质量"""
    y, sr = librosa.load(audio_path)

    # 检查时长
    duration = len(y) / sr
    if duration < min_duration or duration > max_duration:
        return False, f"时长异常: {duration:.2f}秒"

    # 检查静音
    silence = np.sum(np.abs(y) < 0.001) / len(y)
    if silence > 0.5:
        return False, f"静音过多: {silence*100:.1f}%"

    # 检查音频幅度
    amplitude = np.max(np.abs(y))
    if amplitude < 0.1:
        return False, f"音量过低: {amplitude:.3f}"

    return True, "正常"

# 批量检查
audio_dir = Path("normalized")
for audio_file in audio_dir.glob("*.wav"):
    valid, msg = check_audio_quality(audio_file)
    print(f"{audio_file.name}: {msg}")
```

## 训练配置

### 训练脚本

创建微调脚本 `finetune.py`:

```python
from transformers import (
    Trainer,
    TrainingArguments,
    Qwen3TTSConfig,
    Qwen3TTSModel,
    Qwen3TTSTokenizer,
)
from datasets import Dataset
import torch
from pathlib import Path

# 加载预训练模型和分词器
model_name = "Qwen/Qwen3-1.5B-Base-TTS"
config = Qwen3TTSConfig.from_pretrained(model_name)
model = Qwen3TTSModel.from_pretrained(model_name, config=config)
tokenizer = Qwen3TTSTokenizer.from_pretrained(model_name)

# 加载训练数据
train_data = []
valid_data = []

with open("fine_tuning_data/train/train.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        train_data.append(json.loads(line.strip()))

with open("fine_tuning_data/valid/valid.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        valid_data.append(json.loads(line.strip()))

# 自定义数据集类
class TTSDataset(Dataset):
    def __init__(self, data, tokenizer):
        self.data = data
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]

        # 加载文本
        text_encodings = self.tokenizer(
            item["text"],
            truncation=True,
            max_length=512,
            return_tensors="pt",
        )

        # 加载音频
        audio, sr = librosa.load(item["audio_path"], sr=24000)
        audio_tensor = torch.FloatTensor(audio)

        return {
            "input_ids": text_encodings["input_ids"].squeeze(0),
            "attention_mask": text_encodings["attention_mask"].squeeze(0),
            "audio_labels": audio_tensor,
        }

# 创建数据集
train_dataset = TTSDataset(train_data, tokenizer)
valid_dataset = TTSDataset(valid_data, tokenizer)

# 训练参数
training_args = TrainingArguments(
    output_dir="./checkpoint",
    num_train_epochs=10,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    learning_rate=1e-5,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=100,
    evaluation_strategy="steps",
    eval_steps=500,
    save_strategy="steps",
    save_steps=500,
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    fp16=True,  # 使用混合精度训练
    dataloader_num_workers=4,
    gradient_checkpointing=True,
)

# 创建 Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=valid_dataset,
)

# 开始训练
trainer.train()

# 保存模型
trainer.save_model("./finetuned_model")
tokenizer.save_pretrained("./finetuned_model")
```

### 训练参数详解

| 参数 | 默认值 | 说明 | 建议值 |
|------|--------|------|--------|
| `num_train_epochs` | 3 | 训练轮数 | 5-10 |
| `per_device_train_batch_size` | 4 | 每个 GPU 的批大小 | 2-8 (取决于显存) |
| `learning_rate` | 5e-5 | 学习率 | 1e-5 - 5e-5 |
| `warmup_steps` | 0 | 热身步数 | 500-1000 |
| `weight_decay` | 0.0 | 权重衰减 | 0.01 |
| `fp16` | False | 混合精度训练 | True (推荐) |
| `gradient_accumulation_steps` | 1 | 梯度累积步数 | 1-4 |

### 启动训练

```bash
# 单 GPU 训练
python finetune.py

# 多 GPU 训练 (使用 torchrun)
torchrun --nproc_per_node=4 finetune.py

# 使用 DeepSpeed 进行分布式训练
deepspeed finetune.py --deepspeed_config ds_config.json
```

### DeepSpeed 配置示例

```json
{
  "train_batch_size": 32,
  "train_micro_batch_size_per_gpu": 4,
  "gradient_accumulation_steps": 2,
  "fp16": {
    "enabled": true
  },
  "optimizer": {
    "type": "AdamW",
    "params": {
      "lr": 1e-5,
      "betas": [0.9, 0.999],
      "eps": 1e-8
    }
  },
  "scheduler": {
    "type": "WarmupLR",
    "params": {
      "warmup_min_lr": 0,
      "warmup_max_lr": 1e-5,
      "warmup_num_steps": 500
    }
  },
  "zero_optimization": {
    "stage": 2,
    "offload_optimizer": {
      "device": "cpu"
    },
    "overlap_comm": true
  }
}
```

## 训练监控

### 使用 TensorBoard

```bash
# 启动 TensorBoard
tensorboard --logdir=./logs --port=6006

# 在浏览器中访问
# http://localhost:6006
```

### 训练曲线分析

关注以下指标：
- **训练损失**: 逐步下降
- **验证损失**: 应接近训练损失，避免过拟合
- **学习率**: 按预热策略逐步上升并保持稳定

## 模型评估

### 评估指标

1. **客观指标**:
   - MOS评分 (Mean Opinion Score)
   - 频谱距离 (Spectral Distance)
   - 音质指标 (PESQ, STOI)

2. **主观评估**:
   - 自然度
   - 清晰度
   - 情感准确度

### 评估脚本示例

```python
import torch
import scipy.io.wavfile as wavfile
from qwen3_tts import Qwen3TTSModel, Qwen3TTSTokenizer

# 加载微调后的模型
tokenizer = Qwen3TTSTokenizer.from_pretrained("./finetuned_model")
model = Qwen3TTSModel.from_pretrained("./finetuned_model")

# 测试文本
test_texts = [
    "这是一个测试文本，用于评估微调效果。",
    "语音质量应该接近原始数据风格。",
]

for i, text in enumerate(test_texts):
    audio_input = tokenizer(text, return_tensors="pt").input_ids

    with torch.no_grad():
        audio_output = model.generate(audio_input)

    # 保存音频
    audio_numpy = audio_output.cpu().numpy().squeeze(-1)
    wavfile.write(f"test_{i}.wav", 24000, audio_numpy)

    print(f"已生成: test_{i}.wav")
```

## 推理优化

### 模型量化

```python
from optimum.bettertransformer import BetterTransformer

# 加载量化模型
model = BetterTransformer.transform(
    model,
    quantization="int8",
)

# 保存量化模型
model.save_pretrained("./finetuned_model_int8")
```

### ONNX 导出

```python
import torch.onnx

# 切换为评估模式
model.eval()

# 创建示例输入
dummy_input = tokenizer("测试文本", return_tensors="pt").input_ids

# 导出 ONNX 模型
torch.onnx.export(
    model,
    dummy_input,
    "qwen3_tts.onnx",
    input_names=["input_ids"],
    output_names=["audio"],
    opset_version=17,
    dynamic_axes={
        "input_ids": {0: "batch_size", 1: "sequence_length"},
        "audio": {0: "batch_size"},
    },
)
```

### 批量推理优化

```python
def batch_inference(texts, batch_size=16):
    """批量推理"""
    model.eval()

    all_audio = []
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]

        # 批量分词
        audio_inputs = tokenizer(
            batch_texts,
            return_tensors="pt",
            padding=True,
            truncation=True,
        )

        # 批量生成
        with torch.no_grad():
            audio_outputs = model.generate(audio_inputs.input_ids)

        # 分离结果
        for audio in audio_outputs:
            all_audio.append(audio.squeeze())

    return all_audio
```

## 常见问题

### Q1: 微调出现内存不足怎么办？

**A**:
- 减少 `per_device_train_batch_size`
- 增加 `gradient_accumulation_steps`
- 启用 `gradient_checkpointing=True`
- 使用 DeepSpeed 的 ZeRO 优化

### Q2: 微调后模型效果不好？

**A**:
- 检查训练数据质量
- 增加训练数据量
- 调整学习率（尝试 1e-5 - 5e-5）
- 检查是否过拟合（验证集损失上升）
- 尝试从检查点恢复训练

### Q3: 如何加速训练？

**A**:
- 启用混合精度训练 (`fp16=True`)
- 使用多个 GPU
- 使用 DeepSpeed 分布式训练
- 使用梯度累积减少通信次数

### Q4: 微调模型可以跨语言使用吗？

**A**:
- 可以，但建议在同一语言上微调以获得最佳效果
- 跨语言微调可能降低特定语言的质量

## 最佳实践

1. **数据质量优先**: 高质量数据比大量数据更重要
2. **小规模测试**: 先在小数据集上验证流程
3. **定期保存**: 使用 `save_steps` 定期保存检查点
4. **监控过拟合**: 密切关注训练集和验证集损失差异
5. **逐步迭代**: 从基础配置开始，逐步优化参数
6. **充分验证**: 使用多样化的测试样本验证模型泛化能力
