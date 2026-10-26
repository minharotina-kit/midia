import sys
sys.path.insert(0, '/tmp/claude-0/-home-claude/5d8bda1a-7926-5607-9e1a-eeb000255e05/scratchpad/tools')
import build_reel_noite as bn
S = bn.S
seg = {'hook': 0.0, 'i1': 5.25, 'i2': 8.95, 'i3': 11.3, 'fonte': 15.8, 'cta': 20.0, 'fim': 23.4}
cues = {'hook': [2.4], 'i1': [1.6], 'i2': [1.2], 'i3': [1.4], 'fonte': [0.2], 'cta': [1.0]}
print(bn.render(seg, cues, 'reel-noite-2610', S + 'audio/2026-10-26-faz-hoje/take1.mp3', S + 'musica/2026-10-26-ninar.wav'))
