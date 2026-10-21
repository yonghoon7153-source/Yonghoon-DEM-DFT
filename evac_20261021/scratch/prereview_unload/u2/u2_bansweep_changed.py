#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""U2 — 바뀐 파일 전체에 금지 인용 스윕 (scripts/check_review_findings.ban_sweep 를 files= 로 · 리포에 쓰지 않는다).
사용: python3 -I -B u2_bansweep_changed.py <작업 트리> <바뀐 파일 목록 txt> <출력 JSON>"""
import json
import os
import sys

WT = os.path.abspath(sys.argv[1])
LST = sys.argv[2]
OUT = sys.argv[3]
sys.path.insert(0, os.path.join(WT, 'scripts'))
import check_review_findings as C  # noqa: E402

rel = [ln.strip() for ln in open(LST, encoding='utf-8') if ln.strip()]
files = [os.path.join(WT, r) for r in rel if os.path.isfile(os.path.join(WT, r))]
probs, nfile, nban = C.ban_sweep(WT, None, files=files)
# 기본 스윕 글롭 (_ban_files) 이 이 파일들 중 어느 것을 원래 읽는지도 적는다 (스윕 밖 파일 = 기본 CI 가 보지 않음)
default = set(os.path.relpath(p, WT).replace(os.sep, '/') for p in C._ban_files(WT))
out = {'n_changed': len(rel), 'n_swept': nfile, 'n_bans': nban, 'problems': probs,
       'outside_default_globs': [r for r in rel if r not in default]}
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'changed {len(rel)} · swept {nfile} · bans {nban} · problems {len(probs)} · outside default globs {len(out["outside_default_globs"])}')
for p in probs[:20]:
    print(p)
