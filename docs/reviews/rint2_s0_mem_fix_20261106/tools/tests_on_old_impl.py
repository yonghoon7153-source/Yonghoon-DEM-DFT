#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""시험 먼저 기록 (2026-11-06 · `SELF-155` 고침) — 최종 시험 파일을 **고치기 전 구현** 위에서 돌린다.

scripts/carbon_junction.py · scripts/ca_s0_census.py 를 잠시 고치기 전 blob (커밋 3b12fbe2d · 39104710a) 으로 바꾸고 → 주어진 시험 명령을
돌려 로그를 남긴다 → 새 판 바이트를 되돌리고 sha256 을 확인한다 (finally · 되돌림 실패 = 이 도구 실패 · rc 2).

  python3 docs/reviews/rint2_s0_mem_fix_20261106/tools/tests_on_old_impl.py <로그 접두> -- <시험 명령 …>
"""
import hashlib
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
TARGETS = (('scripts/carbon_junction.py', '3b12fbe2d'), ('scripts/ca_s0_census.py', '39104710a'))


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    out = os.path.abspath(sys.argv[1])
    cmd = sys.argv[sys.argv.index('--') + 1:]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    new = {rel: open(os.path.join(ROOT, rel), 'rb').read() for rel, _ in TARGETS}
    old = {rel: subprocess.run(['git', '-C', ROOT, 'show', f'{c}:{rel}'], capture_output=True, check=True).stdout for rel, c in TARGETS}
    rc, meta = None, []
    try:
        for rel, _ in TARGETS:
            with open(os.path.join(ROOT, rel), 'wb') as fh:
                fh.write(old[rel])
            meta.append(f'in_place {rel} sha256={sha(open(os.path.join(ROOT, rel), "rb").read())}')
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        rc = p.returncode
        with open(out + '.log', 'w', encoding='utf-8') as fh:
            fh.write(p.stdout + p.stderr)
    finally:
        ok = True
        for rel, _ in TARGETS:
            with open(os.path.join(ROOT, rel), 'wb') as fh:
                fh.write(new[rel])
            back = sha(open(os.path.join(ROOT, rel), 'rb').read())
            ok &= back == sha(new[rel])
            meta.append(f'restored {rel} sha256={back} ok={back == sha(new[rel])}')
    with open(out + '.meta', 'w', encoding='utf-8') as fh:
        fh.write(f'cmd={" ".join(cmd)}\n' + '\n'.join(meta) + f'\nrc={rc}\n')
    if os.path.exists(out + '.log'):
        print('\n'.join(open(out + '.log', encoding='utf-8').read().splitlines()[-2:]))
    print(f'rc={rc} 되돌림={ok}')
    return 2 if not ok else 0


if __name__ == '__main__':
    sys.exit(main())
