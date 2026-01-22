---
name: youtube-downloader
description: Download YouTube videos, playlists, and audio using yt-dlp. Use when the user asks to download YouTube content, extract audio from videos, get video metadata, or download video subtitles/transcripts. Supports quality selection, format conversion, and batch downloads.
---

# YouTube Downloader

## Overview

This skill enables downloading YouTube videos, playlists, audio tracks, and subtitles using `yt-dlp`, a powerful command-line video downloader.

## Quick Start

### Download a Video (Best Quality)

```bash
yt-dlp "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Download Audio Only (MP3)

```bash
yt-dlp -x --audio-format mp3 "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Download with Subtitles

```bash
yt-dlp --write-auto-sub --sub-lang en "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Common Tasks

### 1. Video Download

**Best quality video + audio:**
```bash
yt-dlp -f "bestvideo+bestaudio" "URL"
```

**Specific quality (e.g., 1080p):**
```bash
yt-dlp -f "bestvideo[height<=1080]+bestaudio" "URL"
```

**Download to specific directory:**
```bash
yt-dlp -o "/path/to/output/%(title)s.%(ext)s" "URL"
```

### 2. Audio Extraction

**Extract as MP3:**
```bash
yt-dlp -x --audio-format mp3 --audio-quality 0 "URL"
```

**Extract as M4A (better quality):**
```bash
yt-dlp -x --audio-format m4a "URL"
```

### 3. Playlist Download

**Download entire playlist:**
```bash
yt-dlp -o "%(playlist_index)s-%(title)s.%(ext)s" "PLAYLIST_URL"
```

**Download specific items from playlist:**
```bash
yt-dlp --playlist-items 1-5 "PLAYLIST_URL"
```

### 4. Subtitle Download

**Auto-generated subtitles:**
```bash
yt-dlp --write-auto-sub --sub-lang en --skip-download "URL"
```

**Manual subtitles only:**
```bash
yt-dlp --write-sub --sub-lang en --skip-download "URL"
```

**All available subtitles:**
```bash
yt-dlp --write-sub --all-subs --skip-download "URL"
```

### 5. Get Video Information (No Download)

**Get metadata in JSON:**
```bash
yt-dlp --dump-json --skip-download "URL"
```

**List available formats:**
```bash
yt-dlp -F "URL"
```

## Advanced Options

### Quality Selection

- `-f "best"` - Best single file
- `-f "bestvideo+bestaudio"` - Best video + best audio (merged)
- `-f "worst"` - Lowest quality (for testing)
- `--list-formats` or `-F` - List all available formats

### Output Templates

- `%(title)s` - Video title
- `%(id)s` - Video ID
- `%(ext)s` - File extension
- `%(upload_date)s` - Upload date (YYYYMMDD)
- `%(uploader)s` - Channel name
- `%(playlist_index)s` - Position in playlist

**Example:**
```bash
yt-dlp -o "%(uploader)s - %(upload_date)s - %(title)s.%(ext)s" "URL"
```

### Rate Limiting

**Limit download speed:**
```bash
yt-dlp -r 1M "URL"  # Limit to 1 MB/s
```

### Batch Downloads

**From a text file (one URL per line):**
```bash
yt-dlp -a urls.txt
```

## Error Handling

### Common Issues

1. **Age-restricted videos**: Use `--cookies-from-browser chrome` (requires logged-in browser)
2. **Geo-blocked content**: May need VPN or proxy
3. **Format not available**: Use `-F` to list available formats first
4. **Slow downloads**: Use `-r` to set rate limit or try different time

### Update yt-dlp

Keep yt-dlp updated for best compatibility:
```bash
brew upgrade yt-dlp  # macOS
# or
pip install --upgrade yt-dlp  # Python
```

## Usage Examples

**Download video as MP4 with best quality:**
```bash
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" "URL"
```

**Download only audio from playlist:**
```bash
yt-dlp -x --audio-format mp3 "PLAYLIST_URL"
```

**Download with thumbnail and metadata:**
```bash
yt-dlp --write-thumbnail --add-metadata "URL"
```

**Download with English subtitles embedded:**
```bash
yt-dlp --write-sub --sub-lang en --embed-subs "URL"
```
