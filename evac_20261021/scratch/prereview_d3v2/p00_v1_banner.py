#!/usr/bin/env python3
"""PRE-D3V2 탐침 00 — v1 설계 배너 커밋이 본문을 바꾸지 않았는가 (바이트 대조).

입력: 같은 폴더의 v1_old.md (= git show 055ddd04e:<v1>) · v1_new.md (= git show 2f1d29d09:<v1>)
재실행:
    git show 055ddd04e:docs/reviews/mixer_d3_se_flowability_anchor_design_20261015.md > v1_old.md
    git show 2f1d29d09:docs/reviews/mixer_d3_se_flowability_anchor_design_20261015.md > v1_new.md
    python3 -I p00_v1_banner.py
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
old = open(os.path.join(HERE, 'v1_old.md'), 'rb').read()
new = open(os.path.join(HERE, 'v1_new.md'), 'rb').read()
lines = new.split(b'\n')
banner, blank = lines[0], lines[1]
body = b'\n'.join(lines[2:])
print('old bytes', len(old), 'new bytes', len(new), 'diff', len(new) - len(old))
print('banner bytes', len(banner), 'blank line empty?', blank == b'')
print('body == old ?', body == old)
print('sha256 old ', hashlib.sha256(old).hexdigest())
print('sha256 body', hashlib.sha256(body).hexdigest())
print('banner starts with "> "?', banner.startswith(b'> '))
print('old ends with newline?', old.endswith(b'\n'), 'new ends with newline?', new.endswith(b'\n'))
sys.exit(0 if body == old else 1)
