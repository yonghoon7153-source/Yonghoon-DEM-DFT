#!/usr/bin/env python3
"""모든 CLI 스크립트의 --help 스모크 — argparse help 의 '%' 이스케이프 누락(ValueError/KeyError)을
런타임 전에 잡는다.  2026-07-27: '−7.8% → …' 가 --help 를 죽인 회귀에서 도입.

  python3 scripts/test_cli_help.py     # 종료코드 0=PASS
"""
import glob
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    bad = []
    me = os.path.abspath(__file__)
    files = sorted(glob.glob(os.path.join(ROOT, 'scripts', '*.py')))
    scanned = 0
    for fp in files:
        # ★자기 자신·다른 테스트 러너 제외 — 이 파일 소스에 'add_argument' 문자열이 있어 자기매칭하면
        #   재귀 실행으로 멈추지 않는다 (2026-07-27 도입 즉시 밟은 함정).
        if os.path.abspath(fp) == me or os.path.basename(fp).startswith('test_'):
            continue
        src = open(fp, encoding='utf-8', errors='replace').read()
        if 'ArgumentParser(' not in src or 'add_argument(' not in src:
            continue                                    # CLI 아님 (호출 형태로 판정)
        scanned += 1
        try:
            r = subprocess.run([sys.executable, fp, '--help'], capture_output=True,
                               text=True, timeout=90)
        except subprocess.TimeoutExpired:
            bad.append((os.path.basename(fp), 'TIMEOUT — --help 가 90s 안에 안 끝남(무거운 import/재귀?)'))
            continue
        # import 실패(선택 의존성 부재)는 이 테스트의 관심사가 아님 — argparse 포맷 오류만 잡는다
        err = r.stderr or ''
        if r.returncode != 0 and ('_expand_help' in err or 'unsupported format character' in err
                                  or ('KeyError' in err and 'argparse' in err)):
            bad.append((os.path.basename(fp), err.strip().splitlines()[-1][:90]))
    for b in bad:
        print(f'  FAIL {b[0]}: {b[1]}')
    print(f'CLI-HELP TEST {"PASS" if not bad else "FAIL"} ({scanned} CLI 스크립트 검사)')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
