#!/usr/bin/env python3
"""실행기 print_followups (등록 §6 의 후속 명령 원천) 를 받은 manifest 로 다시 찍는다 — 경로 = manifest 의 WSL ROOT 그대로
(읽기 전용 · 아무것도 돌리지 않는다 · 찍힌 `cd` 줄은 이 체크아웃 경로라 WSL 에서는 `cd ~/dem-audit` 로 · `python3` 는 배치 venv `$PY` 로 바꿔 쓴다).
사용: python3 -I s5_followups.py --repo <리포> --root194 <풀어 둔 194 뿌리> --rootsupp <풀어 둔 보충 뿌리>
"""
import argparse
import json
import os
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('--repo', required=True)
ap.add_argument('--root194', required=True)
ap.add_argument('--rootsupp', required=True)
a = ap.parse_args()
sys.path.insert(0, os.path.join(a.repo, 'scripts'))
import run_network_194_parallel as NP  # noqa: E402

for sub in (a.root194, a.rootsupp):
    with open(os.path.join(sub, 'manifest.json'), encoding='utf-8') as f:
        man = json.load(f)
    root = Path(man['argv'][man['argv'].index('--root') + 1])
    print(f'##### {root} · root_from={man.get("root_from")!r} root_to={man.get("root_to")!r} · python={man.get("python")!r}')
    NP.print_followups(root, man, out=print)
