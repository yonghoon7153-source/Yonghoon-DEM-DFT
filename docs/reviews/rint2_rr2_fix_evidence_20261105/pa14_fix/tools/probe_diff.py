"""탐침 고치기 전 → 뒤 바뀐 줄 (정규화: utc 시각 · 12 자리 이상 hex = 런마다 다른 표지 · 폴더 요약 sha) — 탐침마다 바뀐 줄 수 + 줄 (앞 260 자).
쓰임: python3 probe_diff.py <출력 폴더> <탐침 이름 …>"""
import difflib
import re
import sys
from pathlib import Path

d = Path(sys.argv[1])
UTC = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z')
HEX = re.compile(r'\b[0-9a-f]{12,64}\b')


def norm(t):
    return [HEX.sub('<hex>', UTC.sub('<utc>', ln)) for ln in t.splitlines()]


for p in sys.argv[2:]:
    b = norm((d / f'{p}_before.out').read_text(encoding='utf-8'))
    a = norm((d / f'{p}_after.out').read_text(encoding='utf-8'))
    diff = [ln for ln in difflib.unified_diff(b, a, lineterm='', n=0) if ln[:1] in '+-' and not ln.startswith(('+++', '---'))]
    print(f'== {p}: 바뀐 줄 {sum(1 for ln in diff if ln.startswith("+"))} (고치기 전 {sum(1 for ln in diff if ln.startswith("-"))})')
    for ln in diff:
        print('  ' + ln[:260])
