#!/bin/bash
# ─────────────────────────────────────────────────────────
#  Mësonjëtorja Manim — Render with background music
# ─────────────────────────────────────────────────────────
#
#  Usage:
#    ./render.sh <script_path> <ClassName> [quality]
#
#  Examples:
#    ./render.sh scripts/matematike/matematika-10-11-pjesa-2/7.2A/ushtrimi4.py Ushtrimi4
#    ./render.sh scripts/matematike/matematika-10-11-pjesa-2/7.2A/ushtrimi4.py Ushtrimi4 k
#
#  Quality flags: l (480p), m (720p), h (1080p, default), k (4K)
#
#  Output goes to: output/<ClassName>.mp4
# ─────────────────────────────────────────────────────────

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MUSIC_DIR="$SCRIPT_DIR/music"
OUTPUT_DIR="$SCRIPT_DIR/output"

# Default music track and volume
MUSIC_FILE="$MUSIC_DIR/lofi-chill.mp3"
MUSIC_VOLUME=0.12  # 12% volume — subtle background

# Parse arguments
SCRIPT_PATH="$1"
CLASS_NAME="$2"
QUALITY="${3:-h}"  # default: high (1080p60)

if [ -z "$SCRIPT_PATH" ] || [ -z "$CLASS_NAME" ]; then
    echo "Usage: ./render.sh <script_path> <ClassName> [quality: l/m/h/k]"
    echo ""
    echo "Examples:"
    echo "  ./render.sh scripts/matematike/.../ushtrimi4.py Ushtrimi4"
    echo "  ./render.sh scripts/matematike/.../ushtrimi4.py Ushtrimi4 k"
    exit 1
fi

# Map quality flag
case "$QUALITY" in
    l) QF="-ql" ;;
    m) QF="-qm" ;;
    h) QF="-qh" ;;
    k) QF="-qk" ;;
    *) echo "Invalid quality: $QUALITY (use l/m/h/k)"; exit 1 ;;
esac

echo "▸ Rendering $CLASS_NAME at quality -q$QUALITY ..."
python3 -m manim render "$SCRIPT_PATH" "$CLASS_NAME" $QF --format mp4

# Find the rendered video — pick the most recently modified match
# (manim puts it in media/videos/<filename>/<resolution>/)
BASENAME=$(basename "$SCRIPT_PATH" .py)
VIDEO_FILE=$(find "$SCRIPT_DIR/media/videos/$BASENAME" -name "$CLASS_NAME.mp4" -type f -print0 \
    | xargs -0 ls -t 2>/dev/null | head -1)

if [ -z "$VIDEO_FILE" ]; then
    echo "✗ Could not find rendered video for $CLASS_NAME"
    exit 1
fi

echo "▸ Found video: $VIDEO_FILE"

# Check music file exists
if [ ! -f "$MUSIC_FILE" ]; then
    echo "✗ Music file not found: $MUSIC_FILE"
    echo "  Place an .mp3 file in the music/ directory."
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

FINAL="$OUTPUT_DIR/${CLASS_NAME}.mp4"

echo "▸ Adding background music (volume: ${MUSIC_VOLUME}) ..."

# Merge video + looped music at low volume with fade-out at the end
# -stream_loop -1  → loop the music track indefinitely
# volume=...       → keep music subtle
# afade=t=out      → fade out music in the last 3 seconds
VIDEO_DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO_FILE")
FADE_START=$(echo "$VIDEO_DURATION - 3" | bc)

ffmpeg -y \
    -i "$VIDEO_FILE" \
    -stream_loop -1 -i "$MUSIC_FILE" \
    -filter_complex "[1:a]volume=${MUSIC_VOLUME},afade=t=out:st=${FADE_START}:d=3[bg]" \
    -map 0:v -map "[bg]" \
    -c:v copy -c:a aac -b:a 128k \
    -shortest \
    "$FINAL" \
    2>/dev/null

echo "✓ Done: $FINAL"
echo "  Duration: ${VIDEO_DURATION}s"

# Open the video
open "$FINAL"
