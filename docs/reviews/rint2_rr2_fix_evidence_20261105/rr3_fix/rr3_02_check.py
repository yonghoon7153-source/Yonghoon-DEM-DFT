"""RR3-02 확인 — 판정문 §2 의 rg 한 줄 (같은 정규식 · 파이썬 re) 로 요청서의 걸린 줄을 바탕 (40d9658c0) · 작업 트리에서 세고, 걸린 줄마다 '11-08 정정' 표지가 있는지 ·
계획이 든 줄 (83 · 84 · 86 · 94 · 140 · 154) 이 다 표지를 받았는지 · 바뀐 줄이 그 줄뿐인지 본다.  python3 rr3_02_check.py <작업 트리>"""
import difflib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
REL = 'docs/reviews/codex_rint2_rr_round3_request_20261108.md'
PAT = re.compile('교차 대조 없음|디스크 signal_after 받음|STOPS 소속 안 봄|PC12 고침으로')
PLAN = [83, 84, 86, 94, 140, 154]
old = subprocess.run(['git', 'show', f'40d9658c0:{REL}'], cwd=str(ROOT), capture_output=True, text=True, check=True).stdout.splitlines()
new = (ROOT / REL).read_text(encoding='utf-8').splitlines()
hit_old = [i + 1 for i, ln in enumerate(old) if PAT.search(ln)]
hit_new = [i + 1 for i, ln in enumerate(new) if PAT.search(ln)]
marked = [n for n in hit_new if '11-08 정정' in new[n - 1]]
marks = [i + 1 for i, ln in enumerate(new) if '11-08 정정' in ln]
changed = sorted({i + 1 for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old, new).get_opcodes() if tag != 'equal' for i in range(i1, i2)})
print(f'바탕 줄 수 {len(old)} · 작업 트리 줄 수 {len(new)}')
print(f'rg 꼴 걸린 줄 — 바탕 {hit_old} · 작업 트리 {hit_new} · 그중 표지 있음 {marked} ({len(marked)}/{len(hit_new)})')
print(f"'11-08 정정' 표지 줄 = {marks} · 계획 목록 {PLAN} 다 있음 = {all(n in marks for n in PLAN)}")
print(f'바뀐 줄 (바탕 번호) = {changed} · 표지 줄과 같음 = {changed == marks}')
ok = len(marked) == len(hit_new) and all(n in marks for n in PLAN) and changed == marks and len(old) == len(new)
print('결과', 'OK' if ok else 'NG')
sys.exit(0 if ok else 1)
