#!/usr/bin/env bash
# Przygotowuje klip do scroll-scrub: bez dźwięku, 1080p, gęste klatki kluczowe
# (płynne przewijanie w obie strony) i faststart.
# Użycie: tools/prepare-clip.sh wejscie.mp4 [wyjscie.mp4]
set -euo pipefail

IN="${1:?podaj plik wejściowy}"
OUT="${2:-$(dirname "$0")/../media/hero.mp4}"
mkdir -p "$(dirname "$OUT")"

ffmpeg -y -i "$IN" -an \
  -vf "scale=-2:1080,fps=30" \
  -c:v libx264 -preset slow -crf 20 -g 2 -keyint_min 2 -sc_threshold 0 \
  -pix_fmt yuv420p -movflags +faststart \
  "$OUT"

echo "Gotowe: $OUT"
