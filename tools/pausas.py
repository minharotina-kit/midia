"""Deixa a narração das 12h calma: corta nas frases, põe pausas fixas e desacelera 10%.

Uso: python3 pausas.py voz_bruta.wav palavras.json pausas.json saida.wav cues.json
  palavras.json: [["Palavra", inicio, fim], ...] (tempos da transcrição, em segundos)
  pausas.json:   {"palavra_que_fecha_frase": pausa_em_segundos, ...}
                 (a chave é a palavra exatamente como veio na transcrição; se a mesma palavra
                  fecha mais de uma frase, use "palavra#2" pra segunda vez)
Saída: wav a 48 kHz e cues.json [{"w": palavra, "s": inicio_no_video}] pro molde de motion.
"""
import json
import subprocess
import sys

PRE, POST, LEAD, TAIL, TEMPO = 0.05, 0.09, 0.25, 0.6, 0.9


def main(src, words_path, pauses_path, out_wav, out_cues):
    W = [tuple(w) for w in json.load(open(words_path))]
    pauses = json.load(open(pauses_path))
    seen = {}
    keyed = []
    for w, s, e in W:
        seen[w] = seen.get(w, 0) + 1
        k = w if seen[w] == 1 else f"{w}#{seen[w]}"
        keyed.append((k, w, s, e))
    segs, cur = [], []
    for k, w, s, e in keyed:
        cur.append((k, w, s, e))
        if k in pauses:
            segs.append(cur)
            cur = []
    if cur:
        segs.append(cur)
    tcur, cues, parts = LEAD, [], []
    for i, sg in enumerate(segs):
        a = max(0, sg[0][2] - PRE)
        b = sg[-1][3] + POST
        if i + 1 < len(segs):
            b = min(b, (sg[-1][3] + segs[i + 1][0][2]) / 2)
        gap = max(0.0, pauses.get(sg[-1][0], 0.0) - PRE - POST)
        for k, w, s, e in sg:
            cues.append({"w": w, "s": round((tcur + (s - a)) / TEMPO, 3)})
        parts.append((a, b, gap))
        tcur += (b - a) + gap
    ins = ['-f', 'lavfi', '-t', str(LEAD), '-i', 'anullsrc=r=44100:cl=mono']
    labels, fc, idx = ['[0:a]'], '', 1
    for a, b, gap in parts:
        ins += ['-ss', f'{a:.3f}', '-to', f'{b:.3f}', '-i', src]
        fc += f'[{idx}:a]aformat=sample_rates=44100:channel_layouts=mono,afade=t=in:d=0.012,afade=t=out:st={b - a - 0.012:.3f}:d=0.012[p{idx}];'
        labels.append(f'[p{idx}]')
        idx += 1
        if gap > 0:
            ins += ['-f', 'lavfi', '-t', f'{gap:.3f}', '-i', 'anullsrc=r=44100:cl=mono']
            labels.append(f'[{idx}:a]')
            idx += 1
    ins += ['-f', 'lavfi', '-t', str(TAIL), '-i', 'anullsrc=r=44100:cl=mono']
    labels.append(f'[{idx}:a]')
    fc += ''.join(labels) + f'concat=n={len(labels)}:v=0:a=1,atempo={TEMPO}[o]'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', fc, '-map', '[o]', '-ar', '48000', out_wav], check=True)
    json.dump(cues, open(out_cues, 'w'), ensure_ascii=False)
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out_wav],
                             capture_output=True, text=True).stdout)
    print('voz', round(d, 2), 'última palavra', cues[-1], 'frases', len(parts))


if __name__ == '__main__':
    main(*sys.argv[1:6])
