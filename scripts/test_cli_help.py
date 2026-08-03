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
    # ── ★ 내용 검사 (2026-07-30 리뷰 HIGH-7) ─────────────────────────────────────────────
    #   위 루프는 `--help` 가 **크래시 없이 도는지**만 본다.  그래서 `--i0-temp-scale` 의 help 가
    #   HIGH-1 이 거짓이라 선언한 `R_ct∝1/i0` 와 정정 **전** 배수(5.60)를 계속 가르치는데도
    #   GREEN 이었다.  **help 가 플래그의 1차 사양서**이므로 핵심 문구를 직접 대조한다.
    print('  [내용] 온도 플래그 help 가 정정된 물리를 가르치는가 (HIGH-7)')
    _s4 = os.path.join(ROOT, 'scripts', 'step4_dyn.py')
    try:
        _h = subprocess.run([sys.executable, _s4, '--help'], capture_output=True,
                            text=True, timeout=90).stdout
    except Exception as e:                                   # noqa: BLE001
        _h = ''
        bad.append(('step4_dyn.py', f'--help 실행 실패: {e}'))
    if _h:
        # argparse 가 줄바꿈으로 접으므로 공백을 정규화해서 대조한다 (문구는 있는데 개행으로
        # 쪼개져 FAIL 하는 위양성 방지)
        _h = ' '.join(_h.split())
        _forbid = [
            ('R_ct∝1/i0', 'HIGH-1 이 거짓이라 선언한 비례관계 (정답: i0 ∝ T/R_ct)'),
            ('i0 ×5.60', 'RT 전인자 정정 **전** 배수 (코드는 6.25 를 적용)'),
            ('60 °C 에서 i0 ×5.60', '동상'),
        ]
        for _txt, _why in _forbid:
            if _txt in _h:
                bad.append(('step4_dyn.py --help', f'정정 전 문구 잔존 "{_txt}" — {_why}'))
        _need = [
            ('i0 ∝ **T/R_ct**', 'RT 전인자 포함 비례관계'),
            ('×6.25', '정정 후 60 °C 배수'),
            ('한 쌍', '--temp-k ↔ --i0-temp-scale 짝-불변식'),
            ('uncoated', '앵커 조성 한계 (코팅계는 Eₐ 다름)'),
            ('yun2023', 'R_ct(N) 앵커 (kim2025 아님 — HIGH-6)'),
        ]
        for _txt, _why in _need:
            if _txt not in _h:
                bad.append(('step4_dyn.py --help', f'필수 문구 부재 "{_txt}" — {_why}'))
        # --temp-k help 는 "i0 는 T 를 안 따른다" 를 **무조건** 말하면 안 된다 (조건부여야 함)
        if '--i0-temp-scale 을 켜면' not in _h:
            bad.append(('step4_dyn.py --help',
                        '--temp-k help 가 i0 스케일 시의 예외를 말하지 않는다 (조건부 아님)'))
        if not any(b[0] == 'step4_dyn.py --help' for b in bad):
            print('    OK  금지 3 / 필수 5 / --temp-k 조건부 — 전부 통과')
    for b in bad:
        print(f'  FAIL {b[0]}: {b[1]}')
    print(f'CLI-HELP TEST {"PASS" if not bad else "FAIL"} ({scanned} CLI 스크립트 검사)')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
