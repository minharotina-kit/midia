"""Remistura voz + música e junta com o vídeo mudo. Uso: remix.py video_mudo narr musica dur saida.mp4 [musica_db]"""
import subprocess, sys
video, narr, music, dur, out = sys.argv[1:6]
mdb = sys.argv[6] if len(sys.argv) > 6 else '-13'
dur = float(dur); fo = dur - 1.4
fc = (f'[0:a]aresample=48000,aformat=channel_layouts=stereo,volume=10dB,apad=pad_dur=4,atrim=0:{dur},asplit=2[voc][sc];'
      f'[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{dur},asetpts=PTS-STARTPTS,volume={mdb}dB,afade=t=in:d=0.4,afade=t=out:st={fo}:d=1.4[mus];'
      '[mus][sc]sidechaincompress=threshold=0.015:ratio=6:attack=30:release=450:makeup=1[duck];'
      '[voc][duck]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[out]')
wav = out[:-4] + '.wav'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', narr, '-i', music, '-filter_complex', fc, '-map', '[out]',
                '-ar', '48000', '-t', str(dur), wav], check=True)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', video, '-i', wav, '-c:v', 'libx264', '-crf', '21',
                '-maxrate', '5M', '-bufsize', '10M', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                '-b:a', '192k', '-shortest', '-movflags', '+faststart', out], check=True)
print(out)
