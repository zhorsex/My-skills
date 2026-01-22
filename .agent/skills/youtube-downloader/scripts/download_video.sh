#!/usr/bin/env bash
#
# YouTube Video Downloader Script
# Downloads YouTube videos with best quality using yt-dlp
#
# Usage:
#   download_video.sh <URL> [OUTPUT_DIR]
#
# Examples:
#   download_video.sh "https://www.youtube.com/watch?v=VIDEO_ID"
#   download_video.sh "https://www.youtube.com/watch?v=VIDEO_ID" ~/Downloads

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

echo "Downloading video from: $URL"
echo "Output directory: $OUTPUT_DIR"
echo ""

# Download with best quality
yt-dlp \
    -f "bestvideo+bestaudio" \
    -o "${OUTPUT_DIR}/%(title)s.%(ext)s" \
    --merge-output-format mp4 \
    "$URL"

echo ""
echo "✅ Download complete!"
