#!/usr/bin/env bash
#
# YouTube Audio Downloader Script
# Extracts audio from YouTube videos as MP3 using yt-dlp
#
# Usage:
#   download_audio.sh <URL> [OUTPUT_DIR]
#
# Examples:
#   download_audio.sh "https://www.youtube.com/watch?v=VIDEO_ID"
#   download_audio.sh "https://www.youtube.com/watch?v=VIDEO_ID" ~/Music

set -euo pipefail

URL="${1:-}"
OUTPUT_DIR="${2:-./}"

if [ -z "$URL" ]; then
    echo "Error: YouTube URL is required"
    echo "Usage: $0 <URL> [OUTPUT_DIR]"
    exit 1
fi

# Check if yt-dlp is installed
if ! command -v yt-dlp &> /dev/null; then
    echo "Error: yt-dlp is not installed"
    echo "Install it with: brew install yt-dlp"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

echo "Extracting audio from: $URL"
echo "Output directory: $OUTPUT_DIR"
echo ""

# Extract audio as MP3 with best quality
yt-dlp \
    -x \
    --audio-format mp3 \
    --audio-quality 0 \
    -o "${OUTPUT_DIR}/%(title)s.%(ext)s" \
    "$URL"

echo ""
echo "✅ Audio extraction complete!"
