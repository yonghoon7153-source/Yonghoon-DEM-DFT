"""고치기 전 탐침 출력 (바탕 뿌리) ↔ 사전 공격 14 원 출력 (`../../preattack14/out/`) — 바이트 같음 · 아니면 정규화 (utc 시각 · 12 자리 이상 hex = 런마다 다른 표지 ·
폴더 요약 sha) 뒤 같음.  쓰임: python3 before_vs_preattack.py <고치기 전 출력 폴더> <원 출력 폴더> <탐침 이름 …>"""
import re
import sys
from pathlib import Path

bdir, odir = Path(sys.argv[1]), Path(sys.argv[2])
UTC = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z')
HEX = re.compile(r'\b[0-9a-f]{12,64}\b')


def norm(t):
    return HEX.sub('<hex>', UTC.sub('<utc>', t))


n_same = n_norm = n_diff = 0
for p in sys.argv[3:]:
    b = (bdir / f'{p}_before.out').read_text(encoding='utf-8')
    o = (odir / f'{p}.out').read_text(encoding='utf-8')
    if b == o:
        v, n_same = '바이트 같음', n_same + 1
    elif norm(b) == norm(o):
        v, n_norm = '정규화 뒤 같음 (utc 시각 · 런 표지 · 폴더 요약 sha 만 다름)', n_norm + 1
    else:
        v, n_diff = '다름', n_diff + 1
    print(f'{p}: {v}')
print(f'탐침 {len(sys.argv) - 3} = 바이트 같음 {n_same} · 정규화 뒤 같음 {n_norm} · 다름 {n_diff}')
sys.exit(1 if n_diff else 0)
