# -*- coding: utf-8 -*-
"""로그 경로 가림 — 세션 scratch 뿌리 → <scratch> · 작업 트리 → <작업 트리> · 리포 → <리포> (값 · 판정 글은 그대로).  쓰임: python3 sanitize_log.py <입력> <출력> <scratch 뿌리> <작업 트리> <리포>."""
import sys
from pathlib import Path

src, dst, scratch, wt, repo = sys.argv[1:6]
t = Path(src).read_text(encoding='utf-8', errors='replace')
for old, new in ((scratch, '<scratch>'), (wt, '<작업 트리>'), (repo, '<리포>')):
    t = t.replace(old, new)
t = t.replace('/tmp/claude-0/', '<세션 임시>/')          # 잘린 scratch 경로 조각 (표 칸 길이 제한으로 뿌리 전체가 안 보이는 자리)
Path(dst).write_text(t, encoding='utf-8')
print(dst, len(t))
