#!/usr/bin/env bash
# Mistura do vídeo das 12h com ganho fixo (sem loudnorm dinâmico, sem ducking).
# Uso: mix12h.sh voz.wav musica.mp3 DURACAO video_mudo.mp4 saida.mp4 [inicio_reforco fim_reforco]
#   O reforço opcional sobe +8 dB um trecho da voz (final de frase que a voz fala baixinho).
# Voz em -16 LUFS, música em -27, soma, total em -14 com limitador.
set -euo pipefail
VOZ=$1; MUS=$2; D=$3; VID=$4; OUT=$5; A=${6:-}; B=${7:-}
T=$(mktemp -d)
li(){ ffmpeg -nostats -hide_banner -i "$1" -af ebur128 -f null - 2>&1 | grep -A3 Summary | grep "I:" | awk '{print $2}'; }
BOOST=""; [ -n "$A" ] && BOOST="volume=enable='between(t,$A,$B)':volume=2.5,"
ffmpeg -v error -y -i "$VOZ" -af "${BOOST}acompressor=threshold=-26dB:ratio=2.5:attack=8:release=150:makeup=2" "$T/v.wav"
ffmpeg -v error -y -ss 0 -t "$D" -i "$MUS" -af "aresample=48000,aformat=channel_layouts=stereo" "$T/m.wav"
GV=$(echo "-16 - ($(li "$T/v.wav"))" | bc -l); GM=$(echo "-27 - ($(li "$T/m.wav"))" | bc -l)
FO=$(echo "$D - 2.2" | bc -l)
ffmpeg -v error -y -i "$T/v.wav" -i "$T/m.wav" -filter_complex \
 "[0:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur=$D,volume=${GV}dB[v];[1:a]volume=${GM}dB,afade=t=in:d=1.0,afade=t=out:st=$FO:d=2.2[m];[v][m]amix=inputs=2:normalize=0[o]" \
 -map "[o]" -t "$D" "$T/pre.wav"
GF=$(echo "-14 - ($(li "$T/pre.wav"))" | bc -l)
ffmpeg -v error -y -i "$T/pre.wav" -af "volume=${GF}dB,alimiter=limit=0.84:attack=5:release=60:level=disabled" -ar 48000 "$T/mix.wav"
ffmpeg -v error -y -i "$VID" -i "$T/mix.wav" -c:v libx264 -crf 21 -maxrate 5M -bufsize 10M -preset medium -pix_fmt yuv420p \
 -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
echo "final $(li "$OUT") LUFS, $(du -h "$OUT" | cut -f1)"
rm -rf "$T"
