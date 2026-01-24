---
name: qwen3-tts
description: Text-to-Speech generation, voice design, and voice cloning using Qwen3-TTS. Use when Claude needs to generate speech, design unique voices, or clone existing voices from audio samples.
---

# Qwen3-TTS

Qwen3-TTS is a powerful speech generation library supporting voice cloning, voice design, and high-quality human-like speech generation in 10 languages (Chinese, English, Japanese, Korean, German, French, Russian, Portuguese, Spanish, Italian).

## Environment Setup

To use Qwen3-TTS, you need a Python 3.9+ environment.

```bash
# Basic installation
pip install -U qwen-tts

# Optional: Install FlashAttention 2 for GPU optimization (requires compatible hardware)
pip install -U flash-attn --no-build-isolation
```

**Note**: On macOS, `flash-attn` might not be available or difficult to install. It is optional.

## Usage Patterns

Import the model and use one of the generation methods.

### 1. Custom Voice Generation

Use pre-defined premium voices.

```python
import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel

# Load model (can be 1.7B or 0.6B)
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
    device_map="auto",  # Use "cuda" for GPU, "cpu" or "mps" for Mac
    dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
)

# Generate
wavs, sr = model.generate_custom_voice(
    text="Hello, this is a test.",
    language="English",
    speaker="Ryan", # See references/models.md for list
    instruct="Happy tone", # Optional instruction
)
sf.write("output_custom.wav", wavs[0], sr)
```

**See [references/models.md](references/models.md) for a full list of supported speakers.**

### 2. Voice Design

Create a unique voice from a text description.

```python
model = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign", device_map="auto")

wavs, sr = model.generate_voice_design(
    text="Hello world!",
    language="English",
    instruct="A deep, resonant male voice, sounding wise and ancient.",
)
sf.write("output_design.wav", wavs[0], sr)
```

### 3. Voice Cloning

Clone a voice from a reference audio file (3-10 seconds recommended).

```python
model = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-Base", device_map="auto")

# Single inference with cloning
wavs, sr = model.generate_voice_clone(
    text="This is the new voice.",
    language="English",
    ref_audio="path/to/reference_audio.wav",
    ref_text="Transcript of the reference audio.", # Optional if x_vector_only_mode=True
)
sf.write("output_clone.wav", wavs[0], sr)
```

### 4. Running the Web UI Demo

To launch the local web UI:

```bash
# Launch generic demo (specify model)
qwen-tts-demo Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice --ip 0.0.0.0 --port 8000
```

Then visit `http://localhost:8000`.

## Reference Materials

- **[Models and Speakers](references/models.md)**: Detailed list of available models and supported speakers.
