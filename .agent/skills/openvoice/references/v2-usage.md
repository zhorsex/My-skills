# OpenVoice V2 使用指南

OpenVoice V2 在 V1 的基础上提升了音频质量，增加了原生多语言支持，并完全免费商用。

## 新增特性

1. **更好的音频质量**: 采用了新的训练策略。
2. **原生多语言支持**: 原生支持英语、西班牙语、法语、中文、日语和韩语。
3. **免费商业使用**: 采用 MIT 许可证。

## 安装与配置

### 1. 下载检查点

- **下载地址**: [checkpoints_v2_0417.zip](https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_v2_0417.zip)
- **解压位置**: `OpenVoice/checkpoints_v2/`

### 2. 安装 MeloTTS

OpenVoice V2 依赖 MeloTTS 作为基础 TTS 模型。

```bash
pip install git+https://github.com/myshell-ai/MeloTTS.git
python -m unidic download
```

## 使用演示

**参考示例**: [`demo_part3.ipynb`](https://github.com/myshell-ai/OpenVoice/blob/main/demo_part3.ipynb)

在这个演示中，你可以体验 V2 的所有新特性，特别是原生多语言支持。

## 支持的语言

OpenVoice V2 原生支持以下语言：

- 英语 (English)
- 西班牙语 (Spanish)
- 法语 (French)
- 中文 (Chinese)
- 日语 (Japanese)
- 韩语 (Korean)

对于其他语言，只要有对应的基础说话人模型，OpenVoice V2 同样支持跨语言克隆。
