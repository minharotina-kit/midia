#!/bin/bash
set -e
M=$(ls /mnt/user-data/attachments/5d8bda1a-7926-5607-9e1a-eeb000255e05/*funny-bouncy-cartoon-mischief*.mp3)
read T0 DUR < out/meme_t.txt || true
L=$(python3 -c "print(round($DUR-$T0,3))"); FO=$(python3 -c "print(round($DUR-$T0-1.3,3))"); D=$(python3 -c "print(int($T0*1000))")
ffmpeg -y -loglevel error -i voz/t1.wav -i out/bed.wav -i out/fx.wav -i "$M" -filter_complex "\
[0:a]aresample=48000,adelay=150,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[v];\
[1:a]loudnorm=I=-30:TP=-6,aresample=48000[b];\
[2:a]volume=0.4[f];\
[3:a]aresample=48000,atrim=0:$L,asetpts=PTS-STARTPTS,afade=t=in:d=0.25,afade=t=out:st=$FO:d=1.3,loudnorm=I=-25:TP=-4,aresample=48000,adelay=$D[m];\
[v][b][f][m]amix=inputs=4:normalize=0:duration=longest,alimiter=limit=0.9,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,atrim=0:$DUR[o]" -map "[o]" -ac 2 -c:a pcm_s16le out/mix.wav
ffmpeg -i out/mix.wav -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I:|Peak:)" | tail -2
