#!/usr/bin/env python3
"""⛔ 폐기 — 이 계획 생성기는 **실행 불가능한 명령을 만든다**.  킷 경로가 대체한다.

⚠⚠ 2026-09-07 (Codex R9, P0-1) — 이 파일은 selftest 15/15 를 통과하면서 캠페인을 **시작조차
못 하는** 명령을 냈다.  검사가 센 것은 *"있어야 할 축이 다 있나"* 였고, *"이 명령이 도는가"* 는
한 번도 묻지 않았다.  실제로 빠진 것:

  · `--add-recipe VGCF=1,PTFE=1`  → 파서는 `VGCF:PTFE=1:1` 만 받는다
  · STEP2 에 `--save-se --save-phase --save-fibre --save-fibre-dia --save-metrics` 없음
  · STEP3 에 `--se --scaffold --phase --fibre --metrics-json` **전부** 없음
    → 빈 scaffold 의 `max()` 에서 즉시 죽는다
  · 출력명에 `.json` 이 없는데 판정기는 `arms/*.json` 만 읽는다
  · 읽어도 payload 는 σ_e 를 `mpm_metrics` **아래**에 두는데 판정기는 최상위를 요구한다
  · 사전등록 STEP2 봉인축 21 개 중 **17 개 미명시** · `n_grid` 288 vs 실물 킷 256

★ 교훈 — **필수 토큰을 세는 것은 필수 입력이 빠졌는지 확인하는 것이 아니다.**
  자료구조로 만들어 검사 가능하게 한 것은 옳았고, **무엇을 검사할지 고른 것이 틀렸다.**

⇒ 정본 경로: `mpm_input_from_case.py` 가 `run_mpm.sh` 를 만들고 그것이 STEP2+STEP3 를 한다.
  킷 5 개는 `docs/data/phase_a_6mah/kits/` 에 있다.  쓰는 법은 그 폴더의 README.

이 파일은 **기록으로만** 남긴다 — 실행하면 거부한다.

━━ 아래는 폐기 전 원문 (기록) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  | Phase A 실행 계획 생성기 — 사전등록 §1·§4·§5 를 **실제 명령으로** 펼친다.
  |
  |     python3 scripts/phase_a_plan.py                       # 요약
  |     python3 scripts/phase_a_plan.py --emit sh > run.sh    # 실행 스크립트
  |     python3 scripts/phase_a_plan.py --selftest
  |
  | ━━ 왜 셸이 아니라 파이썬인가 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  | 실행은 GPU 기계에서 하지만 **계획은 여기서 전수 검증된다**.  리포가 이미 아홉 번 잡은 결함이
  | *"규약 축이 봉인 문서엔 있는데 **실제 명령엔 없다**"* 이고 (CLAUDE.md 규율 ⑤), 그건 셸
  | 스크립트로는 시험이 안 된다.  ⇒ 계획을 **자료구조로** 만들고 selftest 가 그 자료구조를 센다.
  |
  | ★ 이 스크립트는 **아무것도 실행하지 않는다.**  명령 문자열만 만든다.
  |
  | ━━ 무엇을 펼치나 (prereg §1) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  |     STEP2   4 조성 (VGCF 1/2/3/4 + PTFE 1)  +  Lee 1              =   5 런
  |     STEP3   primary  4 조성 × 3 격자 × 8 origin                   =  96
  |             secondary 생산·Lee × 0.15 × 8                         =  16
  |             QC       exact replay × 8                             =   8
  |                                                                     ───
  |                                                                     120 팔
  | 격자 순서는 **0.15 먼저** — 원 질문의 완전한 답이 거기 하나에 다 있다.
"""

from __future__ import annotations

import argparse
import itertools
import json
import os
import shlex
import sys

_RETIRED = True          # 실행 거부 (모듈 docstring 참조)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

#  ── 사전등록 축 (prereg §1·§4·§5) ─────────────────────────────────────────────
VGCF_WTS = (1.0, 2.0, 3.0, 4.0)
PTFE_WT = 1.0
VOXES = (0.15, 0.20, 0.25)          # ★ 0.15 먼저 (prereg §1)
N_ORIGIN = 8
SEED = 3
N_GRID = 288                         # d_h/dx = 5.65 (CL-78, 문턱 3.5)
LEE_RECIPE = 'VGCF=3,PTFE=0.5'       # Lee 2025 첨가제 wt% (AM:SE 는 스캐폴드가 정한다 — §6)
BED = 'docs/data/phase_a_6mah'

#  STEP3 봉인 규약 (prereg §5) — **모든** STEP3 명령에 들어가야 한다
#  ⛔⛔ **낡았다 (2026-09-18 확인)** — `--step3-bridge-um 0` 은 **개정 전** 값이다.
#    사전등록 §5 는 2026-09-08 (CL-87) 에 `bridge = 0.24 µm 물리 고정` 으로 개정됐고
#    이 파일은 그 **하루 전** 09-07 이 마지막 수정이다.  `0` 은 CLI 에서 '반경 0' 이
#    아니라 **'기본 1.2·vox'** 라 격자에 묶인다 (0.18 / 0.24 / 0.30 µm @ vox 0.15/0.20/0.25).
#  ★ 그러나 **런에 닿지 못한다** — 이 파일은 폐기돼 `--emit` 이 거부하므로 죽은 상수다.
#    고치지 않고 표시만 남긴다 (기록 보존).  ⚠ **여기서 축을 베끼지 말 것 — §5 가 정본이다.**
#  ⚠ selftest ④ 는 이 상수를 **자기 자신과** 대조하므로 이 어긋남을 영원히 못 잡는다
#    (규율 ⑤ — 후보를 고르는 코드가 곧 사각지대).  검사를 정본에 묶으려면 §5 를 읽어야 한다.
STEP3_SEALED = ('--step3-fibre-stamp', 'segment',
                '--ptfe-stamp', 'centerline',
                '--sigma-ptfe', '0',
                '--step3-bridge-um', '0',
                '--no-ion', '--no-pore')
LEAN_ENV = 'LEAN=2'                  # σ_e 전용 (prereg §5)


def origins(vox, n=N_ORIGIN):
    """8 origin = {0, vox/2}³ 전수 (prereg §2 — 완전 nuisance 집합)."""
    return [tuple(t) for t in itertools.product((0.0, vox / 2.0), repeat=3)][:n]


def step2_plan():
    """STEP2 — 조성마다 한 런.  ★ `--add-rng-per-phase` 가 **필수**다 (CL-71/77)."""
    out = []
    for w in VGCF_WTS:
        out.append({'kind': 'step2', 'role': 'primary', 'vgcf_wt': w,
                    'tag': f'v{w:g}p{PTFE_WT:g}',
                    'argv': ['python3', 'scripts/mpm3d_compaction.py',
                             '--am-scaffold', f'{BED}/am_scaffold.csv.gz',
                             '--se-dump', f'{BED}/se_scaffold.csv.gz',
                             '--add-recipe', f'VGCF={w:g},PTFE={PTFE_WT:g}',
                             '--add-rng-per-phase',            # ★ 조성 축 ↔ morphology 분리
                             '--seed', str(SEED), '--n-grid', str(N_GRID),
                             '--protocol', 'hold',
                             '--platen-mach', '0.03', '--allow-fast-platen']})
    out.append({'kind': 'step2', 'role': 'secondary', 'vgcf_wt': None, 'tag': 'lee',
                'argv': ['python3', 'scripts/mpm3d_compaction.py',
                         '--am-scaffold', f'{BED}/am_scaffold.csv.gz',
                         '--se-dump', f'{BED}/se_scaffold.csv.gz',
                         '--add-recipe', LEE_RECIPE,
                         '--add-rng-per-phase',
                         '--seed', str(SEED), '--n-grid', str(N_GRID),
                         '--protocol', 'hold',
                         '--platen-mach', '0.01']})    # ⚠ 절대 대조 = 준정적 경로, 승인 플래그 없음
    return out


def _step3(role, tag, vox, sh, outdir, vgcf_wt):
    return {'kind': 'step3', 'role': role, 'vgcf_wt': vgcf_wt, 'vox': vox,
            'origin': sh, 'outdir': outdir, 'env': {'LEAN': '2'},
            'argv': ['python3', 'scripts/mpm_webapp_payload.py',
                     '--step3-vox', f'{vox:g}',
                     '--step3-origin-shift', f'{sh[0]:.6g}', f'{sh[1]:.6g}', f'{sh[2]:.6g}',
                     *STEP3_SEALED, '--out', outdir]}


def step3_plan():
    """STEP3 — primary 96 + secondary 16 + QC 8."""
    out = []
    for vox in VOXES:                                   # 0.15 먼저
        for w in VGCF_WTS:
            for i, sh in enumerate(origins(vox)):
                out.append(_step3('primary', f'v{w:g}', vox, sh,
                                  f'{BED}/arms/p_v{w:g}_x{vox:g}_o{i}', w))
    for i, sh in enumerate(origins(0.15)):              # Lee 대조 (0.15 만)
        out.append(_step3('secondary', 'lee', 0.15, sh, f'{BED}/arms/s_lee_o{i}', None))
        out.append(_step3('secondary', 'prod', 0.15, sh, f'{BED}/arms/s_prod_o{i}', 3.0))
    for i, sh in enumerate(origins(0.15)):              # ★ QC = exact replay
        #   음성대조의 정의: **다른 출력 경로**에서 같은 계산을 반복한다 (prereg §3).
        #   seed 를 바꾸는 것이 아니다 — 그건 morphology replicate 다 (CL-71).
        out.append(_step3('qc_replay', 'replay', 0.15, sh, f'{BED}/arms/q_v1_o{i}', 1.0))
    return out


def plan():
    return step2_plan() + step3_plan()


def to_sh(p):
    L = ['#!/usr/bin/env bash',
         '# Phase A — 자동 생성 (scripts/phase_a_plan.py).  ⚠ 손으로 고치지 말 것:',
         '#   축을 여기서 바꾸면 사전등록과 어긋나고 selftest 가 그것을 못 잡는다.',
         '#   바꿔야 하면 phase_a_plan.py 를 고치고 --selftest 를 통과시킨 뒤 다시 생성한다.',
         'set -euo pipefail', '']
    for i, c in enumerate(p, 1):
        env = ' '.join(f'{k}={v}' for k, v in (c.get('env') or {}).items())
        L.append(f'echo "[{i}/{len(p)}] {c["kind"]} {c["role"]} '
                 f'{c.get("tag", "")} {c.get("vox", "")}"')
        L.append((env + ' ' if env else '') + ' '.join(shlex.quote(a) for a in c['argv']))
        L.append('')
    return '\n'.join(L)


# ═══════════════════════════════════════════════════════════════════════════
def _selftest():
    ok, fail = 0, []

    def chk(n, c):
        nonlocal ok
        (ok := ok + 1) if c else fail.append(n)
        print(('  PASS  ' if c else '  FAIL  ') + n)

    p = plan()
    s2 = [c for c in p if c['kind'] == 'step2']
    s3 = [c for c in p if c['kind'] == 'step3']
    prim = [c for c in s3 if c['role'] == 'primary']
    sec = [c for c in s3 if c['role'] == 'secondary']
    qc = [c for c in s3 if c['role'] == 'qc_replay']

    chk(f'① STEP2 5 런 (4 조성 + Lee) — 측정 {len(s2)}', len(s2) == 5)
    chk(f'① STEP3 120 팔 = 96 + 16 + 8 — 측정 {len(prim)} + {len(sec)} + {len(qc)}',
        (len(prim), len(sec), len(qc)) == (96, 16, 8))
    # ② 조성 축과 morphology 를 가르는 플래그가 **모든** STEP2 에 있나 (CL-71/77)
    chk('② `--add-rng-per-phase` 가 STEP2 전부에 있다 (조성 교락 차단)',
        all('--add-rng-per-phase' in c['argv'] for c in s2))
    # ③ platen — primary 는 승인 플래그 동반, Lee 는 준정적 경로
    pr2 = [c for c in s2 if c['role'] == 'primary']
    lee = [c for c in s2 if c['role'] == 'secondary'][0]
    chk('③ primary = mach 0.03 + --allow-fast-platen (위반이 기록된다)',
        all('0.03' in c['argv'] and '--allow-fast-platen' in c['argv'] for c in pr2))
    chk('③ Lee = mach 0.01 이고 승인 플래그 **없음** (절대 대조는 준정적)',
        '0.01' in lee['argv'] and '--allow-fast-platen' not in lee['argv'])
    # ④ STEP3 봉인 규약이 **전부**에 있나
    miss = [c['outdir'] for c in s3
            if not all(t in c['argv'] for t in STEP3_SEALED)]
    chk(f'④ STEP3 봉인 규약이 120 팔 전부에 (누락 {len(miss)})', not miss)
    chk('④ LEAN=2 가 STEP3 전부에 (σ_e 전용)',
        all((c.get('env') or {}).get('LEAN') == '2' for c in s3))
    # ⑤ origin = {0, vox/2}³ 전수, vox 마다 8개 서로 다름
    bad = []
    for vox in VOXES:
        o = {c['origin'] for c in prim if c['vox'] == vox}
        if len(o) != 8 or o != set(origins(vox)):
            bad.append(vox)
    chk(f'⑤ origin 이 vox 마다 {{0, vox/2}}³ 전수 8개 (어긋난 격자 {bad})', not bad)
    # ⑥ 설계 격자점 전수 — 판정기가 요구하는 것과 같은 집합인가
    cells = {(c['vgcf_wt'], c['vox'], c['origin']) for c in prim}
    chk(f'⑥ primary 격자점 96개가 서로 다르다 — 측정 {len(cells)}', len(cells) == 96)
    # ⑦ ★ QC = exact replay 의 정의 — primary 쌍둥이와 **출력 경로만** 달라야 한다
    twin = {(c['vox'], c['origin']): c for c in prim if c['vgcf_wt'] == 1.0 and c['vox'] == 0.15}
    diffs = []
    for q in qc:
        t = twin.get((q['vox'], q['origin']))
        if t is None:
            diffs.append(('짝 없음', q['outdir'])); continue
        a = [x for x in q['argv'] if x != q['outdir']]
        b = [x for x in t['argv'] if x != t['outdir']]
        if a != b:
            diffs.append((q['outdir'], t['outdir']))
        if q['outdir'] == t['outdir']:
            diffs.append(('경로가 같다', q['outdir']))
    chk(f'⑦ QC 는 쌍둥이와 **출력 경로만** 다르다 = exact replay (어긋남 {len(diffs)})', not diffs)
    # ⑧ 출력 경로 충돌 없음 (덮어쓰면 팔이 조용히 사라진다)
    outs = [c['outdir'] for c in s3]
    chk(f'⑧ 출력 경로 120개가 전부 다르다 — 고유 {len(set(outs))}', len(set(outs)) == 120)
    # ⑨ 격자 순서 — 0.15 가 먼저 나온다 (prereg §1)
    first = next(c['vox'] for c in prim)
    chk(f'⑨ 0.15 를 먼저 돈다 (첫 팔 vox = {first})', first == 0.15)
    # ⑩ 셸 출력이 실제로 그 축들을 담고 있나 (자료구조 ↔ 산출물 일치)
    sh = to_sh(p)
    chk('⑩ 생성된 셸에 --add-rng-per-phase 가 5회 (STEP2 수만큼)',
        sh.count('--add-rng-per-phase') == 5)
    chk('⑩ 생성된 셸에 --no-ion 이 120회 (STEP3 수만큼)', sh.count('--no-ion') == 120)
    chk('⑩ 생성된 셸에 LEAN=2 가 120회', sh.count('LEAN=2') == 120)

    print(f'\nphase_a_plan selftest: {ok}/{ok + len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Phase A 실행 계획 (아무것도 실행하지 않는다)')
    ap.add_argument('--emit', choices=['sh', 'json'], default='')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    #  ⛔ 폐기 — 실행 불가능한 명령을 만든다 (모듈 docstring 참조).  selftest 만 남긴다.
    raise SystemExit(
        '⛔ phase_a_plan.py 는 폐기됐다 — 이 생성기의 명령은 **실행되지 않는다** '
        '(STEP3 에 침대 입력이 없어 즉시 죽는다).\n'
        '   정본 = docs/data/phase_a_6mah/kits/<recipe>/run_mpm.sh  '
        '(mpm_input_from_case.py 가 생성).\n'
        '   자세한 것은 이 파일의 docstring 과 그 폴더의 README.md.')

    p = plan()
    if a.emit == 'sh':
        print(to_sh(p)); raise SystemExit(0)
    if a.emit == 'json':
        print(json.dumps(p, ensure_ascii=False, indent=1)); raise SystemExit(0)

    s2 = [c for c in p if c['kind'] == 'step2']
    s3 = [c for c in p if c['kind'] == 'step3']
    print(f'Phase A 계획 — STEP2 {len(s2)} 런 · STEP3 {len(s3)} 팔')
    for r in ('primary', 'secondary', 'qc_replay'):
        n = sum(1 for c in s3 if c['role'] == r)
        print(f'   STEP3 {r:<10} {n:>4}')
    print(f'\n격자 순서 {VOXES}  ·  n_grid {N_GRID} (d_h/dx 5.65)  ·  seed {SEED}')
    print(f'봉인 규약: {" ".join(STEP3_SEALED)}   [{LEAN_ENV}]')
    print(f'\n실행 스크립트:  python3 scripts/phase_a_plan.py --emit sh > run_phase_a.sh')
    print(f'판정:           python3 scripts/phase_a_order_verdict.py --dir {BED}/arms')
    print('\n⚠ 이 스크립트는 아무것도 실행하지 않는다.  명령만 만든다.')
