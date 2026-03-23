#!/bin/bash
#
# Add background music to a Manim video.
#
# Usage:
#   ./scripts/add_music.sh <video.mp4> [music.mp3] [volume]
#
# Examples:
#   ./scripts/add_music.sh reel.mp4                     # random track, default volume
#   ./scripts/add_music.sh reel.mp4 music/lofi-chill.mp3
#   ./scripts/add_music.sh reel.mp4 music/lofi-chill.mp3 0.2
#
# - Trims music to video length
# - Adds 2s fade-in and 3s fade-out
# - Output: <video>_with_music.mp4

set -euo pipefail

VIDEO="${1:?Usage: add_music.sh <video.mp4> [music.mp3] [volume]}"
MUSIC_DIR="$(cd "$(dirname "$0")/.." && pwd)/music"

# Pick music: use argument, or pick a random .mp3 from music/
if [[ -n "${2:-}" ]]; then
    MUSIC="$2"
else
    MUSIC=$(find "$MUSIC_DIR" -name "*.mp3" | shuf -n 1)
    echo "🎵 Random track: $(basename "$MUSIC")"
fi

VOLUME="${3:-0.25}"

# Get video duration
DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO")
DURATION_INT=${DURATION%.*}
FADE_OUT_START=$((DURATION_INT - 3))

# Output filename
OUTPUT="${VIDEO%.*}_with_music.mp4"

echo "📹 Video:    $VIDEO (${DURATION_INT}s)"
echo "🎵 Music:    $(basename "$MUSIC")"
echo "🔊 Volume:   $VOLUME"
echo "📁 Output:   $OUTPUT"
echo ""

ffmpeg -y -i "$VIDEO" -i "$MUSIC" -filter_complex \
    "[1:a]atrim=0:${DURATION},afade=t=in:d=2,afade=t=out:st=${FADE_OUT_START}:d=3,volume=${VOLUME}[a]" \
    -map 0:v -map "[a]" -c:v copy -shortest "$OUTPUT" 2>/dev/null

echo "✅ Done: $OUTPUT"
