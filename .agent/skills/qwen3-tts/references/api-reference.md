# API 参考文档

本文档提供 Qwen3-TTS Python API 的详细参考信息。

## Qwen3TTSModel

### from_pretrained

加载预训练模型。

```python
Qwen3TTSModel.from_pretrained(
    model_name_or_path: str,
    device_map: str | dict | None = None,
    dtype: torch.dtype | None = None,
    attn_implementation: str | None = None,
    trust_remote_code: bool = False
) -> Qwen3TTSModel
```

**参数：**
- `model_name_or_path`：Hugging Face 模型 ID 或本地路径
- `device_map`：设备映射（如 `"cuda:0"`、`"cuda:1"` 或 `"auto"`）
- `dtype`：数据类型（`torch.float16` 或 `torch.bfloat16`）
- `attn_implementation`：注意力实现（推荐 `"flash_attention_2"`）
- `trust_remote_code`：是否信任远程代码

**返回：** 模型实例

### generate_custom_voice

使用预设音色生成语音（CustomVoice 模型）。

```python
model.generate_custom_voice(
    text: str | list[str],
    language: str | list[str],
    speaker: str | list[str],
    instruct: str | list[str] | None = None,
    **kwargs
) -> tuple[list[np.ndarray], int]
```

**参数：**
- `text`：输入文本（字符串或字符串列表）
- `language`：语言代码（`"Chinese"`、`"English"` 等，或 `"Auto"` 自动检测）
- `speaker`：预设音色名称（见 SKILL.md 中的列表）
- `instruct`：可选的情感/语气指令
- `**kwargs`：其他生成参数（`max_new_tokens`、`top_p` 等）

**返回：**
- `(wavs, sr)`：音频波形数组和采样率

**示例：**

```python
wavs, sr = model.generate_custom_voice(
    text="Hello world!",
    language="English",
    speaker="Ryan",
    instruct="Very happy style"
)
```

### get_supported_speakers

获取当前模型支持的预设音色列表。

```python
model.get_supported_speakers() -> dict[str, str]
```

**返回：** 音色名称到描述的字典

### get_supported_languages

获取当前模型支持的语言列表。

```python
model.get_supported_languages() -> list[str]
```

**返回：** 支持的语言代码列表

### generate_voice_design

使用自然语言描述设计声音（VoiceDesign 模型）。

```python
model.generate_voice_design(
    text: str | list[str],
    language: str | list[str],
    instruct: str | list[str],
    **kwargs
) -> tuple[list[np.ndarray], int]
```

**参数：**
- `text`：输入文本
- `language`：语言代码
- `instruct`：自然语言声音描述
- `**kwargs`：其他生成参数

**返回：**
- `(wavs, sr)`：音频波形数组和采样率

**instruct 描述示例：**

```python
# 性别、年龄、音域
"Male, 17 years old, tenor range"

# 情感和语气
"Speak in an incredulous tone, but with a hint of panic"

# 详细描述
"Bright, lively young woman with a crisp clear pronunciation, slightly higher pitch with noticeable variations"
```

### generate_voice_clone

使用参考音频克隆声音（Base 模型）。

```python
model.generate_voice_clone(
    text: str | list[str],
    language: str | list[str],
    ref_audio: str | urllib.parse.ParseResult | tuple[np.ndarray, int],
    ref_text: str,
    voice_clone_prompt: list | None = None,
    x_vector_only_mode: bool = False,
    **kwargs
) -> tuple[list[np.ndarray], int]
```

**参数：**
- `text`：要合成的文本
- `language`：语言代码
- `ref_audio`：参考音频（路径/URL/(波形, 采样率)）
- `ref_text`：参考音频的转写文本
- `voice_clone_prompt`：可复用的提示词（来自 `create_voice_clone_prompt`）
- `x_vector_only_mode`：仅使用说话人嵌入模式（简化克隆但质量降低）
- `**kwargs`：其他生成参数

**返回：**
- `(wavs, sr)`：音频波形数组和采样率

**ref_audio 格式：**

| 格式 | 示例 |
|------|------|
| 路径 | `"/path/to/audio.wav"` |
| URL | `"https://example.com/audio.wav"` |
| NumPy | `(waveform_array, sample_rate)` |

**x_vector_only_mode：**
- `True`：仅使用说话人嵌入，不需要 `ref_text`，速度更快但质量较低
- `False`（默认）：使用完整克隆流程，需要 `ref_text`，质量更高

### create_voice_clone_prompt

构建可复用的语音克隆提示词。

```python
model.create_voice_clone_prompt(
    ref_audio,
    ref_text: str,
    x_vector_only_mode: bool = False
) -> list
```

**参数：**
- `ref_audio`：参考音频
- `ref_text`：转写文本
- `x_vector_only_mode`：是否仅使用嵌入模式

**返回：** 提示词对象（用于 `generate_voice_clone` 的 `voice_clone_prompt` 参数）

**用途：**
- 一次构建，多次使用
- 避免重复计算特征
- 适合批量生成或长文本分段生成

## Qwen3TTSTokenizer

### from_pretrained

加载音频分词器。

```python
Qwen3TTSTokenizer.from_pretrained(
    model_name_or_path: str,
    device_map: str | dict | None = None
) -> Qwen3TTSTokenizer
```

**参数：**
- `model_name_or_path`：`"Qwen/Qwen3-TTS-Tokenizer-12Hz"`
- `device_map`：设备映射

### encode

编码音频为分词器码。

```python
tokenizer.encode(
    audio: str | urllib.parse.ParseResult | tuple[np.ndarray, int],
    sample_rate: int | None = None
) -> dict
```

**参数：**
- `audio`：音频（路径/URL/(波形, 采样率)）
- `sample_rate`：如果 `audio` 是波形数组时的采样率

**返回：** 编码结果字典

### decode

解码分词器码为音频。

```python
tokenizer.decode(
    codes: dict | list,
    sample_rate: int = 24000
) -> list[np.ndarray]
```

**参数：**
- `codes`：编码结果（`encode` 的输出）
- `sample_rate`：输出采样率

**返回：** 音频波形数组列表

## 生成参数

所有 `generate_*` 方法都支持以下 Hugging Face Transformers 生成参数：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `max_new_tokens` | 最大生成 token 数 | 来自配置 |
| `top_p` | 核采样概率阈值 | 0.9 |
| `temperature` | 采样温度 | 1.0 |
| `top_k` | Top-K 采样 K 值 | 50 |
| `do_sample` | 是否采样 | True |

## 错误处理

### 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `CUDA out of memory` | GPU 内存不足 | 使用较小的模型（0.6B）或 `device_map="auto"` |
| `ValueError: Unknown speaker` | 音色名称错误 | 检查 `get_supported_speakers()` |
| `ValueError: Unsupported language` | 语言不支持 | 检查 `get_supported_languages()` |
| `RuntimeError: Audio format error` | 音频格式不支持 | 使用 WAV/MP3 格式 |
