#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""이미 배포된 킷의 `run_mpm.sh` / `run_a1_anchors.sh` 에 준정적 게이트 승인을 **소급** 배선한다.

배경 (2026-08-11 회귀).  같은 날 `mpm3d_compaction.py` 에 준정적 게이트가 들어갔다 —
`V/c_P > 0.01` 이면 `--allow-fast-platen` 없이는 **sys.exit** 한다.  의도는 "위반을 모르고
지나치지 않게" 였는데, 기존 킷 러너는 **전부** 기하 규칙(`vmax = 0.008·(WALL0−FLOOR)`)을
쓰고 그 값이 두꺼운 침대에서 0.1 근처다 (114 µm P:S 킷 실측 V/c_P ≈ 0.105).
⇒ 게이트가 **배포된 모든 킷을 시작조차 못 하게** 만들었다.  생성기
(`mpm_input_from_case.py`) 는 고쳤지만, 이미 zip 으로 나가 GPU 박스에 풀린 킷 폴더는
git pull 로 갱신되지 않는다 (`run_mpm.sh` 는 킷 안에 있고, pull 은 `scripts/` 만 당긴다).
이 스크립트가 그 한 칸을 잇는다.

무엇을 넣나 — 생성기와 **같은 규약**:
  기본   `--allow-fast-platen`  → 기하 규칙 유지.  게이트의 목적은 그대로 달성된다:
         위반이 `mpm_metrics.json` 의 `quasistatic_violation` / `platen_mach_VcP` 에
         박혀 결과가 그것을 달고 다닌다 (등급 B — 같은 마하로 통일한 **상대 비교**는
         공통모드 상쇄로 유효, **절대값**은 아래 처방으로 재측정).
  MPM_QUASISTATIC=1 → `--platen-mach 0.01 --frames ${MPM_QS_FRAMES:-1500}`.
         ⚠ 프레임당 하강폭이 마하비만큼 줄어 프레임도 같은 배수로 늘어야 하고
         런타임이 ~10× 된다.  ⚠⚠ 그 베드는 기존 코퍼스와 **재하율이 다른 별도 트랙**이다.

성질:
  • **멱등** — 이미 배선돼 있으면(`--allow-fast-platen` / `--platen-mach` 둘 중 하나가
    이미 있으면) 건드리지 않고 `skipped` 로 보고한다.
  • 원본을 `.bak` 로 남긴다 (`--no-backup` 로 끔).
  • `--dry-run` 이 기본이 **아니다** — 파일을 고치는 도구이므로 무엇을 고쳤는지 인쇄한다.

사용:
    # 리포 보존본 (docs/data/kit_ps_scaffolds/kit_ps_*__run_mpm.sh)
    python3 scripts/patch_kit_quasistatic.py --archive
    # GPU 박스에 풀린 킷 폴더 (재귀 탐색)
    python3 scripts/patch_kit_quasistatic.py ~/Yonghoon-DEM-DFT/se_curve
    python3 scripts/patch_kit_quasistatic.py --selftest
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys

ARCHIVE_DEFAULT = os.path.join('docs', 'data', 'kit_ps_scaffolds')

#: 이 문자열 중 하나라도 이미 있으면 = 배선됨 (멱등 판정).
_ALREADY = ('--allow-fast-platen', '--platen-mach')

#: run_mpm.sh 의 삽입 기준점 — 이 줄 **다음**에 QS 블록이 들어간다.
_ANCHOR_RUN = 'PSIG=(); ['

#: 압밀 호출의 기본 --frames 가 있는 줄 — 그 **뒤**에 "${QS[@]}" 를 얹어야 --frames 를 덮는다.
_ANCHOR_CALL = '--protocol hold --frames 150 \\'

_QS_BLOCK = '''# ── 준정적 재하율 규약 (2026-08-11 소급 배선; scripts/patch_kit_quasistatic.py) ──────────
#   mpm3d 는 V/c_P > 0.01 이면 **거부**한다 (docs/mpm_platen_kinematic_stop_defect.md §7-2).
#   기존 코퍼스는 전부 기하 규칙 vmax=0.008·(WALL0−FLOOR) — 두꺼운 침대에서 V/c_P≈0.105 라
#   그대로 두면 이 킷은 시작조차 못 한다.  기본값 = 그 규약 유지 + **명시 승인**.
#   게이트의 목적은 그대로: 위반이 mpm_metrics.json 의 quasistatic_violation /
#   platen_mach_VcP 에 박혀 나온다 (등급 B — 같은 마하 상대비교는 유효, 절대값은 아래 처방).
#   MPM_QUASISTATIC=1 → --platen-mach 0.01 (⚠ 프레임 ~10×, 런타임 ~10×,
#   ⚠⚠ 기존 코퍼스와 재하율이 다른 **별도 트랙** — 섞어 쓰지 말 것).
QS=(--allow-fast-platen)
if [ "${MPM_QUASISTATIC:-0}" = "1" ]; then
  QS=(--platen-mach 0.01 --frames "${MPM_QS_FRAMES:-1500}")
  echo "[run_mpm] ★ MPM_QUASISTATIC=1 → --platen-mach 0.01 --frames ${MPM_QS_FRAMES:-1500} (준정적 처방)"
  echo "[run_mpm]   런타임 ~10×.  ⚠ 기존 코퍼스(기하 규칙)와 재하율이 달라 직접 비교 금지 — 별도 트랙."
else
  echo "[run_mpm] 준정적: 기하 규칙 유지 + --allow-fast-platen (등급 B — 위반이 mpm_metrics.json 의"
  echo "[run_mpm]   quasistatic_violation/platen_mach_VcP 에 기록됨).  절대값용 처방은 MPM_QUASISTATIC=1."
fi
'''

#: a1 앵커 러너는 COMMON=( … ) 배열이라 블록이 아니라 **한 줄**만 넣는다.
#   앵커를 `--arch cuda` 같은 옵션 문자열이 아니라 **배열 시작줄**로 잡는다 — 옵션 문자열은
#   주석·echo 에도 나올 수 있어 엉뚱한 곳에 꽂힌다 (그러면 bash -n 은 통과하고 런에서 터진다).
_A1_ANCHOR = 'COMMON=('
_A1_INSERT = '        --allow-fast-platen\n'


def patch_run_mpm(text):
    """run_mpm.sh 본문 → (새 본문, 상태).  상태 ∈ {patched, skipped, no_anchor}."""
    if any(tok in text for tok in _ALREADY):
        return text, 'skipped'
    lines = text.splitlines(keepends=True)
    i_blk = i_call = None
    for i, ln in enumerate(lines):
        if i_blk is None and ln.startswith(_ANCHOR_RUN):
            i_blk = i
        if i_call is None and ln.rstrip('\n').endswith(_ANCHOR_CALL):
            i_call = i
    if i_blk is None or i_call is None or i_call <= i_blk:
        return text, 'no_anchor'
    # 뒤에서부터 넣어야 앞 삽입이 뒤 인덱스를 밀지 않는다.
    lines.insert(i_call + 1, '  "${QS[@]}" \\\n')
    lines.insert(i_blk + 1, _QS_BLOCK)
    return ''.join(lines), 'patched'


def patch_a1(text):
    """run_a1_anchors.sh 본문 → (새 본문, 상태).  COMMON=( … ) 안에 한 줄 추가."""
    if any(tok in text for tok in _ALREADY):
        return text, 'skipped'
    lines = text.splitlines(keepends=True)
    hits = [i for i, ln in enumerate(lines) if ln.lstrip().startswith(_A1_ANCHOR)]
    if not hits:
        return text, 'no_anchor'
    for i in sorted(hits, reverse=True):
        lines.insert(i + 1, _A1_INSERT)
    return ''.join(lines), 'patched'


_HANDLERS = {'run_mpm.sh': patch_run_mpm, 'run_a1_anchors.sh': patch_a1}


def _kind(path):
    """파일명 → 어느 패처인가.  보존본의 `kit_ps_7_3__run_mpm.sh` 규약도 받는다."""
    base = os.path.basename(path)
    for name, fn in _HANDLERS.items():
        if base == name or base.endswith('__' + name):
            return fn
    return None


def find_targets(root):
    out = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for fn in sorted(filenames):
            p = os.path.join(dirpath, fn)
            if _kind(p) is not None:
                out.append(p)
    return sorted(out)


def apply(paths, backup=True, dry=False):
    """→ {상태: [경로]}."""
    res = {'patched': [], 'skipped': [], 'no_anchor': [], 'error': []}
    for p in paths:
        fn = _kind(p)
        try:
            with open(p, encoding='utf-8') as fh:
                old = fh.read()
            new, st = fn(old)
        except Exception as exc:                        # noqa: BLE001 — 한 파일 실패가 배치를 멈추면 안 된다
            print(f'  ERROR {p}: {exc}')
            res['error'].append(p)
            continue
        if st == 'patched' and not dry:
            if backup:
                shutil.copy2(p, p + '.bak')
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(new)
        res[st].append(p)
    return res


# ───────────────────────────── selftest ─────────────────────────────

_FAKE_RUN = '''#!/usr/bin/env bash
set -uo pipefail
FRAC=()
PSIG=(); [ "${MPM_PERIODIC_SIGMA:-0}" = "1" ] && { PSIG=(--periodic); echo "x"; }
# 1) compaction
python3 "$SCR/mpm3d_compaction.py" \\
  --am-scaffold "$KIT/am_scaffold.csv" --se-dump "$KIT/se_scaffold.csv" --periodic \\
  --lateral-box 0.05 --n-grid 256 --arch cuda --gpu-mem 28 --protocol hold --frames 150 \\
  --e-se 1.53 --nu-se 0.49 --target-gpa 0.3 \\
  --save-metrics mpm_metrics.json "${FRAC[@]}" \\
  || { echo fail; exit 1; }
'''

#: ★ 디코이 2줄이 일부러 들어있다 — 주석과 echo 에도 `--arch cuda --gpu-mem 28` 이 나온다.
#   옵션 문자열을 앵커로 잡으면 거기 꽂히고, bash -n 은 그래도 통과한다 (런에서만 터진다).
_FAKE_A1 = '''#!/usr/bin/env bash
# 참고: 공통 인자는 --arch cuda --gpu-mem 28 로 고정한다
echo "COMMON 은 --arch cuda --gpu-mem 28 을 씁니다"
COMMON=(--am-scaffold "$KIT/am_scaffold.csv" --se-dump "$KIT/se_scaffold.csv" --periodic
        --lateral-box 0.05 --n-grid 256 --arch cuda --gpu-mem 28 --frames 150
        --e-se 1.53 --nu-se 0.49)
'''


def _selftest():
    import subprocess
    import tempfile
    ok = fail = 0

    def chk(cond, msg):
        nonlocal ok, fail
        if cond:
            ok += 1
            print(f'  PASS  {msg}')
        else:
            fail += 1
            print(f'  FAIL  {msg}')

    new, st = patch_run_mpm(_FAKE_RUN)
    chk(st == 'patched', '1) run_mpm 패치됨')
    chk('QS=(--allow-fast-platen)' in new, '2) 기본 팔 = --allow-fast-platen')
    chk('MPM_QUASISTATIC' in new and '--platen-mach 0.01' in new, '3) 처방 팔이 env 로 열림')
    # ★ 순서가 핵심: "${QS[@]}" 가 기본 --frames 150 **뒤**여야 argparse 가 덮어쓴다.
    chk(new.index('--frames 150') < new.index('"${QS[@]}"'), '4) ★ QS 가 기본 --frames 뒤')
    # 블록이 호출부보다 앞이어야 변수가 정의된 뒤 쓰인다.
    chk(new.index('QS=(--allow-fast-platen)') < new.index('"${QS[@]}"'), '5) 정의가 사용보다 앞')
    chk(new.index('mpm3d_compaction.py') < new.index('"${QS[@]}"')
        < new.index('|| { echo fail'), '6) QS 가 압밀 호출 **안**에 들어감')
    again, st2 = patch_run_mpm(new)
    chk(st2 == 'skipped' and again == new, '7) ★ 멱등 (두 번 돌려도 안 늘어남)')

    a1n, a1st = patch_a1(_FAKE_A1)
    chk(a1st == 'patched' and '--allow-fast-platen' in a1n, '8) a1 COMMON 배선')
    chk(a1n.count('--allow-fast-platen') == 1, '9) a1 중복 삽입 없음')
    chk(patch_a1(a1n)[1] == 'skipped', '10) a1 멱등')
    # ★ 디코이(주석·echo)가 아니라 배열 안에 들어갔는가 — 옵션 문자열 앵커였다면 여기서 깨진다
    _al = a1n.splitlines()
    _i = next(i for i, ln in enumerate(_al) if '--allow-fast-platen' in ln)
    chk(_al[_i - 1].lstrip().startswith('COMMON=('), '10b) ★ COMMON 배열 첫 줄 바로 뒤 (디코이 회피)')

    # 문법 — 실제 bash 로 판정 (인쇄만 보고 넘어가면 따옴표 실수를 못 잡는다)
    with tempfile.TemporaryDirectory() as td:
        for nm, body in (('run_mpm.sh', new), ('run_a1_anchors.sh', a1n)):
            p = os.path.join(td, nm)
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(body)
            r = subprocess.run(['bash', '-n', p], capture_output=True, text=True)
            chk(r.returncode == 0, f'11/12) bash -n {nm} 통과' + (f' — {r.stderr.strip()}' if r.returncode else ''))
        # 파일 단위 apply 도 (백업·상태) 확인
        res = apply([os.path.join(td, 'run_mpm.sh')], backup=True)
        chk(res['skipped'] and not res['patched'], '13) 이미 패치된 파일은 skipped')

    # ★ QS 배열이 실제로 --frames 를 덮는지 = argparse 의 "마지막이 이긴다" 를 실측
    import argparse as _ap
    _p = _ap.ArgumentParser()
    _p.add_argument('--frames', type=int, default=150)
    chk(_p.parse_args(['--frames', '150', '--frames', '1500']).frames == 1500,
        '14) ★ argparse 는 뒤에 온 --frames 를 채택 (QS 덮어쓰기 성립)')

    # 앵커가 없는 파일은 조용히 통과시키지 말고 no_anchor 로 보고
    chk(patch_run_mpm('#!/bin/bash\necho hi\n')[1] == 'no_anchor', '15) 앵커 없으면 no_anchor')

    print(f'\npatch_kit_quasistatic selftest: {ok}/{ok + fail} PASS')
    return 0 if fail == 0 else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('root', nargs='?', default=None,
                    help='킷 폴더(들)를 담은 디렉토리 — 재귀 탐색.  생략하면 --archive 필요.')
    ap.add_argument('--archive', action='store_true',
                    help=f'리포 보존본({ARCHIVE_DEFAULT})을 대상으로 한다.')
    ap.add_argument('--no-backup', action='store_true', help='.bak 을 남기지 않는다.')
    ap.add_argument('--dry-run', action='store_true', help='무엇이 바뀔지만 인쇄.')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    root = ARCHIVE_DEFAULT if a.archive else a.root
    if not root:
        ap.error('root 또는 --archive 중 하나가 필요합니다.')
    if not os.path.isdir(root):
        print(f'ABORT — 디렉토리가 아닙니다: {root}')
        return 1
    targets = find_targets(root)
    if not targets:
        print(f'대상 없음 — {root} 아래에 run_mpm.sh / run_a1_anchors.sh 가 없습니다.')
        return 1
    res = apply(targets, backup=not a.no_backup, dry=a.dry_run)
    for st in ('patched', 'skipped', 'no_anchor', 'error'):
        for p in res[st]:
            print(f'  {st:9s} {p}')
    print(f"\n{'(dry-run) ' if a.dry_run else ''}patched {len(res['patched'])} · "
          f"skipped {len(res['skipped'])} · no_anchor {len(res['no_anchor'])} · error {len(res['error'])}")
    return 1 if res['error'] or res['no_anchor'] else 0


if __name__ == '__main__':
    sys.exit(main())
