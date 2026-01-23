---
name: openvoice
description: Instant voice cloning with OpenVoice. Use when the user needs to clone voices, perform text-to-speech with specific voice characteristics, control voice styles (emotion, accent, rhythm), or perform cross-lingual voice synthesis. Supports both OpenVoice V1 and V2 for multi-language voice cloning tasks.
---

# OpenVoice

## Overview

OpenVoice 是由 MIT 和 MyShell 开发的即时语音克隆技术,支持精确的音色克隆、灵活的语音风格控制和零样本跨语言语音克隆。

## 核心功能

### OpenVoice V1
- **精确的音色克隆**: 准确克隆参考音色并生成多种语言和口音的语音
- **灵活的语音风格控制**: 对情感、口音、节奏、停顿和语调等风格参数进行精细控制
- **零样本跨语言语音克隆**: 生成语音和参考语音的语言都不需要出现在训练数据集中

### OpenVoice V2
- **更好的音频质量**: 采用不同的训练策略提供更好的音频质量
- **原生多语言支持**: 原生支持英语、西班牙语、法语、中文、日语和韩语
- **免费商业使用**: MIT 许可证,可免费用于商业用途

## 快速开始

### 在线使用

最快的方式是使用已部署的服务:
- [British English](https://app.myshell.ai/widget/vYjqae)
- [American English](https://app.myshell.ai/widget/nEFFJf)
- [Spanish](https://app.myshell.ai/widget/NNFFVz)
- [French](https://app.myshell.ai/widget/z2uyUz)
- [Chinese](https://app.myshell.ai/widget/fU7nUz)
- [Japanese](https://app.myshell.ai/widget/IfIB3u)
- [Korean](https://app.myshell.ai/widget/q6ZjIn)

### 本地安装

```bash
# 创建环境
conda create -n openvoice python=3.9
conda activate openvoice

# 克隆仓库
git clone git@github.com:myshell-ai/OpenVoice.git
cd OpenVoice
pip install -e .
```

## 使用指南

### V1 版本

详细使用说明请参考 [references/v1-usage.md](references/v1-usage.md)

**主要功能:**
1. 灵活的语音风格控制 - 参见 `demo_part1.ipynb`
2. 跨语言语音克隆 - 参见 `demo_part2.ipynb`
3. Gradio 演示 - 运行 `python -m openvoice_app --share`

### V2 版本

详细使用说明请参考 [references/v2-usage.md](references/v2-usage.md)

**安装步骤:**
```bash
# 下载检查点
# 从 https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_v2_0417.zip
# 解压到 checkpoints_v2 文件夹

# 安装 MeloTTS
pip install git+https://github.com/myshell-ai/MeloTTS.git
python -m unidic download
```

**使用示例:**
参见 `demo_part3.ipynb` 了解 V2 的使用方法。

## 常见问题

详细的故障排除指南请参考 [references/troubleshooting.md](references/troubleshooting.md)

### 重要提示

**OpenVoice 是技术,不是产品**

OpenVoice 的目标用户是开发者和研究人员,不是最终用户。虽然它在大多数情况下表现良好,但不要期望它在每个案例上都完美工作。

### 音质问题

- **口音和情感不匹配**: OpenVoice 只克隆音色,不克隆口音或情感。口音和情感由基础 TTS 模型控制。
- **音频质量差**: 检查参考音频是否清晰、无背景噪音、长度适中、只包含一个人的声音。

### 语言支持

OpenVoice 支持任何语言,只要你有该语言的基础说话人模型。可以使用 OpenAI TTS 模型作为基础说话人。

## 辅助脚本

本 skill 提供了以下辅助脚本:

- `scripts/setup_v1.sh` - V1 环境自动设置
- `scripts/setup_v2.sh` - V2 环境自动设置

## 参考资源

- [官方论文](https://arxiv.org/abs/2312.01479)
- [官方网站](https://research.myshell.ai/open-voice)
- [GitHub 仓库](https://github.com/myshell-ai/OpenVoice)
- [安装指南](references/installation.md)
- [V1 使用指南](references/v1-usage.md)
- [V2 使用指南](references/v2-usage.md)
- [故障排除](references/troubleshooting.md)
