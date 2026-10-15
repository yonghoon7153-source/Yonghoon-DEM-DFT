"""L214 수정 — 봉인 CODE_FILES (scripts/run_network_194_parallel.CODE_FILES · 32) 의 code_fp · 인계 도구 (HANDOVER_FILES) 지문 보고 (재봉인 아님 · 읽기 전용).

  BASE (기본 0c557e72a — 원격 본 가지 · 수정 직전) 의 파일 바이트 (git show) ↔ 지금 작업 트리 → 파일마다 sha256 · code_fp (같은 함수 `code_fp`) · 바뀐 파일.
실행:  python3 docs/reviews/lhs214_fix_evidence_20261015/code_fp_report.py [--base REF]
"""
import argparse
import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import run_network_194_parallel as NP          # noqa: E402


def base_hash(base, rel):
    try:
        b = subprocess.run(['git', '-C', ROOT, 'show', f'{base}:{rel}'], capture_output=True, check=True, timeout=60).stdout
    except subprocess.SubprocessError:
        return None
    return hashlib.sha256(b).hexdigest()


def main():
    ap = argparse.ArgumentParser(description='봉인 CODE_FILES code_fp 보고 (재봉인 아님)')
    ap.add_argument('--base', default='0c557e72a')
    a = ap.parse_args()
    now = NP.code_hashes()
    old = {rel: base_hash(a.base, rel) for rel in NP.CODE_FILES}
    print(f'CODE_FILES {len(NP.CODE_FILES)} 파일')
    print(f'  code_fp BASE ({a.base}) = {NP.code_fp(old)}')
    print(f'  code_fp 지금 작업 트리     = {NP.code_fp(now)}')
    ch = [rel for rel in NP.CODE_FILES if old.get(rel) != now.get(rel)]
    print(f'  바뀐 봉인 파일 {len(ch)}:')
    for rel in ch:
        print(f'    {rel}: {str(old.get(rel))[:16]}… → {str(now.get(rel))[:16]}…   (지금 {now.get(rel)})')
    print(f'HANDOVER_FILES {len(NP.HANDOVER_FILES)} (인계 단계 · 봉인 판정 밖 · 발사 때 기록):')
    for rel in NP.HANDOVER_FILES:
        o, n = base_hash(a.base, rel), NP.sha256_file(os.path.join(ROOT, rel)) if hasattr(NP, 'sha256_file') else None
        print(f'    {rel}: {str(o)[:16]}… → {n}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
