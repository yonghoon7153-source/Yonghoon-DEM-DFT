# -*- coding: utf-8 -*-
"""Codex 회차 ④ 재개 탐침 무변경 재실행 로그 — run_codex_probe.sh 화면 원문 → 회차 ④ 로그 꼴 (머리 · 탐침 sha256 · 명령 · 대상 sha256 · rc · 결과 원문 · 경로 = <탐침 풂 자리>).
쓰임: python3 codex_probe_log.py <화면 원문> <탐침 풂 폴더> <출력 로그>"""
import re
import sys
from pathlib import Path

raw, probe_dir, out = sys.argv[1], sys.argv[2], sys.argv[3]
t = Path(raw).read_text(encoding='utf-8')
lines = t.splitlines()
psha = lines[0].split()[0]
tsha = lines[1].split()[0]
rc = re.findall(r'^rc=(\d+)$', t, re.M)[-1]
body = '\n'.join(lines[2:]).replace(str(Path(probe_dir).resolve()), '<탐침 풂 자리>').replace(probe_dir, '<탐침 풂 자리>')
body = re.sub(r'\nrc=\d+\s*$', '', body)
head = [
    '# Codex 회차 ④ 재개 탐침 무변경 재실행 — 고침 C (사전 공격 15 처분) 고친 판 (11-09 · 탐침 파일은 리포에 넣지 않음 = 회차 ④ 반입 규칙 그대로 · 이름 · sha256 · 결과만)',
    '탐침 = resume_attack/probe_resume_independent.py (받은 ZIP 안 이름 · 회차 ④ 고침 증거 logs/probe_rerun.log 와 같은 파일)',
    f'탐침 sha256 = {psha} (바꾸지 않음)',
    '명령 = python3 -I -X utf8 -B resume_attack/probe_resume_independent.py (Python 3.11 · 리포 밖 빈 폴더에 푼 자리에서 · RINT_REVIEW_REPO = 이 작업 트리 · TMPDIR = 세션 scratch)',
    f'대상 scripts/rint_r_chain.py sha256 = {tsha} (고친 판)',
    f'rc = {rc}',
    '결과 (화면 원문 · 경로만 <탐침 풂 자리> 로 바꿈):',
]
tail = ['읽기 = 탐침 181 줄 = PC14_03_attempt_null 단언 (폴더 증거만 자격 True ∧ 다음 순서 None ∧ 풀기 전 사슬 None ∧ 판정 쪽 found_attempts_problem 사유) — '
        '고친 판 (회차 ④ 고침 · 고침 C 둘 다) = 다음 순서 · 풀기 전 사슬이 RESUME_NOT_ALLOWED [ⓐ] 라 단언 실패 = 기대한 뒤집힘 그대로 (회차 ④ 고침 로그와 같은 줄 · 같은 단언)']
Path(out).write_text('\n'.join(head) + '\n' + body.rstrip('\n') + '\n' + '\n'.join(tail) + '\n', encoding='utf-8')
print(Path(out).read_text(encoding='utf-8'))
