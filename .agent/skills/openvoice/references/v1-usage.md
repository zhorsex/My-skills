# OpenVoice V1 使用指南

OpenVoice V1 提供了强大的语音克隆、风格控制和跨语言合成功能。

## 核心功能演示

### 1. 灵活的语音风格控制

OpenVoice 允许对克隆语音的风格进行精细控制。

**参考示例**: [`demo_part1.ipynb`](https://github.com/myshell-ai/OpenVoice/blob/main/demo_part1.ipynb)

在这个演示中，你可以看到如何：
- 克隆参考音色
- 控制情感（喜怒哀乐等）
- 控制口音
- 调整节奏、停顿和语调

### 2. 跨语言语音克隆

OpenVoice 支持零样本跨语言语音克隆，即生成的语音语言和参考语音的语言不需要在训练集中出现。

**参考示例**: [`demo_part2.ipynb`](https://github.com/myshell-ai/OpenVoice/blob/main/demo_part2.ipynb)

在这个演示中，你可以看到如何：
- 使用英语参考音频生成中文语音
- 使用中文参考音频生成英语语音
- 处理训练集中未见过的语言

### 3. Gradio 本地演示

OpenVoice 提供了一个极简的本地 Gradio Web 界面，方便快速试用。

**启动命令**:
```bash
python -m openvoice_app --share
```

**注意**: 如果在使用 Gradio 演示时遇到问题，建议先查阅 `demo_part1.ipynb` 和 `demo_part2.ipynb` 以及常见问题解答。

## 模型检查点

请确保你已经下载了 V1 版本的检查点用于 inference：
- 下载地址: [checkpoints_1226.zip](https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_1226.zip)
- 解压位置: `OpenVoice/checkpoints/`
