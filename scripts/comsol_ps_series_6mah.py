#!/usr/bin/env python3
"""6 mAh **P:S 시리즈** → COMSOL 패키지 (2026-08-18 지시: "면용량 6짜리 0:10, 3:7, 5:5,
7:3, 10:0 활물질만 넘겨주면 될 거 같아, 도전재 적용은 이미 comsol 없어도 우리 모델로 가능").

이 스크립트가 하는 일은 **케이스를 고르는 것과 그 선택이 통제됐음을 증명하는 것**이다.
좌표 추출·패키징은 이미 있는 두 도구가 한다 (작업규율 ① — 새로 짜지 않는다):
    case results → `mpm_input_from_case.py` → 킷(am_scaffold.csv 등) → `comsol_export.py`

★★ **왜 케이스 선택에 스크립트가 필요한가 — 이름이 함정이다** ★★
6 mAh 세트에는 **완전한 5점 시리즈가 두 개** 있고, 그 둘은 **r_SE 로 갈린다**:

    r_SE = 0.5 µm 시리즈  real_1(0:10) real_2(3:7) real_3(5:5) real_4(7:3) real_5(10:0)
    r_SE = 1.5 µm 시리즈  real_6(0:10) real_7(3:7) real_8(5:5) real_9(7:3) real_10(10:0)

⚠ 그런데 파일명이 `real_5 … real_9` 로 **연속**이라 그 다섯을 집으면 자연스러워 보인다.
   실제로는 **real_5 만 r_SE = 0.5** 이고 나머지 넷은 1.5 다 → 10:0 팔에만 SE 크기가
   3배 다른 시리즈가 된다 = P:S 효과와 SE 크기 효과가 **교락**된다.
   (실측: real_5 r_SE 0.5 · real_6~9 r_SE 1.5.  `docs/data/dem_design_points.csv`)

기본은 **r_SE = 0.5 시리즈** — CLAUDE.md 가 기록한 생산 기본값이고 (Fan 2026 §3.5 대조에서
이온 무손실 최대 크기 ∧ 기계 협동변형 영역에 동시 착지), 1.5 시리즈는 `--r-se 1.5` 로 크기
민감도 동반 세트로 쓸 수 있다.

사용:
  python3 scripts/comsol_ps_series_6mah.py --check                 # 통제 검증만 (어디서나)
  python3 scripts/comsol_ps_series_6mah.py --emit-commands \
      --results-root ~/Yonghoon-DEM-DFT/webapp/results --out-root comsol_6mah
  python3 scripts/comsol_ps_series_6mah.py --selftest
"""
from __future__ import annotations

import argparse
import csv
import os
import sys

#  (P:S 라벨, r_SE 0.5 케이스명, r_SE 1.5 케이스명) — 실측 설계점에서 뽑았다
SERIES = [
    ('0:10', 'input_6mAh_real_1',  'input_6mAh_real_6'),
    ('3:7',  'input_6mAh_real_2',  'input_6mAh_real_7'),
    ('5:5',  'input_6mAh_real_3',  'input_6mAh_real_8'),
    ('7:3',  'input_6mAh_real_4',  'input_6mAh_real_9'),
    ('10:0', 'input_6mAh_real_5',  'input_6mAh_real_10'),
]
#  통제되어야 하는 인자 (P:S 는 당연히 변한다).  r_AM_* 는 그 상이 **없는** 팔에서 0 이
#  기록되므로 0 은 비교에서 제외한다 (0:10 에 AM_P 없음 · 10:0 에 AM_S 없음).
CONTROLLED = ('r_SE', 'r_AM_P', 'r_AM_S')
AM_WT_TOL = 1.0          # wt%p — 같은 목표 조성의 실현 산포 허용
_HERE = os.path.dirname(os.path.abspath(__file__))
_DP = os.path.join(_HERE, '..', 'docs', 'data', 'dem_design_points.csv')
_CM = os.path.join(_HERE, '..', 'docs', 'data', 'case_master.csv')


def load_tables(dp=_DP, cm=_CM):
    d = {r['name']: r for r in csv.DictReader(open(dp, encoding='utf-8'))}
    m = {r['name']: r for r in csv.DictReader(open(cm, encoding='utf-8'))}
    return d, m


def resolve(r_se='0.5', dp=_DP, cm=_CM):
    """→ [{ps, name, case, design row}] · 실패하면 무엇이 없는지 말한다."""
    col = 1 if str(r_se) == '0.5' else 2
    d, m = load_tables(dp, cm)
    out, miss = [], []
    for ps, *names in SERIES:
        nm = names[col - 1]
        if nm not in m:
            miss.append(f'{nm} (case_master 에 없음)')
            continue
        cid = m[nm]['case']
        if cid not in d:
            miss.append(f'{nm} → {cid} (dem_design_points 에 없음)')
            continue
        out.append({'ps': ps, 'name': nm, 'case': cid, 'design': d[cid]})
    return out, miss


def check_controlled(rows):
    """→ (ok, 메시지들).  ★ fail-closed: 통제 안 된 시리즈를 COMSOL 로 넘기면
    P:S 효과와 다른 인자가 섞인 채 상대가 그것을 모른다."""
    msg, ok = [], True
    if len(rows) != 5:
        return False, [f'시리즈가 5점이 아니다 ({len(rows)}점) — 빠진 케이스가 있다']
    for fld in CONTROLLED:
        vals = {}
        for r in rows:
            v = float(r['design'].get(fld) or 0.0)
            if v == 0.0:                       # 그 상이 없는 팔 (0:10 의 AM_P 등)
                continue
            vals.setdefault(round(v, 4), []).append(r['ps'])
        if len(vals) > 1:
            ok = False
            msg.append(f'⛔ `{fld}` 가 팔마다 다르다 — ' +
                       ' · '.join(f'{k} → {"/".join(v)}' for k, v in sorted(vals.items())) +
                       '  ⇒ P:S 효과와 교락된다')
        elif vals:
            msg.append(f'✓ `{fld}` = {list(vals)[0]} (모든 팔 동일; 상 부재 팔 제외)')
    wt = [float(r['design'].get('AM_wt') or 0.0) for r in rows]
    spread = max(wt) - min(wt)
    if spread > AM_WT_TOL:
        ok = False
        msg.append(f'⛔ AM_wt 산포 {spread:.2f} %p > {AM_WT_TOL} — 조성이 통제되지 않았다')
    else:
        msg.append(f'✓ AM_wt {min(wt):.1f}–{max(wt):.1f} wt% (산포 {spread:.2f} %p ≤ {AM_WT_TOL})')
    return ok, msg


def emit_commands(rows, results_root, out_root, extra=''):
    """좌표 추출·패키징 명령 — **기존 두 도구**를 부른다 (새 추출기를 짜지 않는다)."""
    lines = ['set -euo pipefail', f'mkdir -p "{out_root}"', '']
    for r in rows:
        tag = f"ps{r['ps'].replace(':', '_')}"
        kit = f'{out_root}/kit_{tag}'
        pkg = f'{out_root}/comsol_pkg_{tag}'
        lines += [
            f"# ── P:S = {r['ps']}   {r['name']}   case {r['case']}",
            f'python3 "{_HERE}/mpm_input_from_case.py" \\',
            f'    --results "{results_root}/{r["case"]}" --case "{r["case"]}" \\',
            f'    --out "{kit}"{(" " + extra) if extra else ""}',
            f'python3 "{_HERE}/comsol_export.py" --kit "{kit}" --out "{pkg}"',
            '',
        ]
    lines += [f'echo "→ {out_root}/comsol_pkg_ps* (5개)"']
    return '\n'.join(lines)


UM_PER_LU = 1000.0          # am_scaffold.csv 의 x,y,z,r 은 LIGGGHTS box unit — ×1000 = µm
#   ★ 이 상수는 `mpm_input_from_case.py:386,413` 의 `_UM_PER_LU` 와 **같아야 한다**.
#     실측 확인: real14 스캐폴드의 r 고유값 {0.002, 0.006} × 1000 = {2, 6} µm =
#     설계점의 r_AM_S 2.0 · r_AM_P 6.0 과 정확히 일치.


def emit_raw(rows, results_root, out_root, extra=''):
    """**raw 핸드오프** — am_scaffold.csv 만 뽑는다 (comsol_export 는 안 부른다).

    지시(2026-08-18): "comsol 그거는 그냥 raw data 후배한테 줄거니까 알아서 하라고 할거야."
    ⇒ 패키징은 빼고, 대신 **파일이 자기를 설명하게** 만든다 (README + 검증).
    """
    lines = ['set -euo pipefail', f'mkdir -p "{out_root}"', '']
    for r in rows:
        tag = f"ps{r['ps'].replace(':', '_')}"
        lines += [
            f"# ── P:S = {r['ps']}   {r['name']}   case {r['case']}",
            f'python3 "{_HERE}/mpm_input_from_case.py" \\',
            f'    --results "{results_root}/{r["case"]}" --case "{r["case"]}" \\',
            f'    --out "{out_root}/{tag}"{(" " + extra) if extra else ""}',
            f'cp "{out_root}/{tag}/am_scaffold.csv" "{out_root}/am_spheres_{tag}.csv"',
            '',
        ]
    lines += [
        '# ── 자기설명 README + fail-closed 단위 검증 ─────────────────────────',
        f'python3 "{os.path.abspath(__file__)}" --write-readme --out-root "{out_root}" '
        f'--r-se {rows[0]["design"]["r_SE"]}',
        f'echo "→ {out_root}/am_spheres_ps*.csv + README.md"',
    ]
    return '\n'.join(lines)


def readme(rows, out_root):
    L = [f'# 6 mAh P:S 시리즈 — AM 구 좌표 raw (r_SE = {rows[0]["design"]["r_SE"]} µm)', '',
         '건식 후막 양극 DEM(LIGGGHTS) 압밀 **완료 후**의 활물질 구 좌표다.',
         'P:S(대립:소립) 비만 다르고 나머지는 전부 같다 — 아래 §3 이 그것을 실측으로 보인다.', '',
         '## 1. 파일', '',
         '| 파일 | P:S | case |', '|---|---|---|']
    for r in rows:
        L.append(f'| `am_spheres_ps{r["ps"].replace(":", "_")}.csv` | {r["ps"]} | `{r["case"]}` |')
    L += ['',
          '## 2. ★★ 열과 **단위** — 여기가 사고 나는 자리다', '',
          '```', '# type,x,y,z,r', '1,0.025033,0.040912,0.007308,0.006000', '```', '',
          '| 열 | 뜻 | 단위 |', '|---|---|---|',
          '| `type` | **1 = AM_P(대립) · 2 = AM_S(소립)** | — |',
          '| `x,y,z` | 구 중심 | **LIGGGHTS box unit** |',
          '| `r` | 구 반경 (**반경이다, 직경 아님**) | **LIGGGHTS box unit** |', '',
          f'⚠ **µm 로 바꾸려면 × {UM_PER_LU:.0f}**.  파일 안에는 이 배율이 안 적혀 있다.',
          f'   검산: `r` 고유값 × {UM_PER_LU:.0f} 가 §3 표의 `r_AM_P` / `r_AM_S` 와 같아야 한다.',
          '   (이 README 를 만든 스크립트가 그것을 **실제로 대조하고** 아래 §4 에 결과를 적는다.)',
          '',
          '## 3. 설계점 — P:S 만 다르다', '',
          '| P:S | r_AM_P (µm) | r_AM_S (µm) | r_SE (µm) | AM wt% | DEM porosity % |',
          '|---|---|---|---|---|---|']
    for r in rows:
        g = r['design']
        L.append(f'| {r["ps"]} | {g["r_AM_P"]} | {g["r_AM_S"]} | {g["r_SE"]} | '
                 f'{g["AM_wt"]} | {g["dem_porosity"]} |')
    L += ['',
          '`r_AM_P = 0` 은 그 팔에 **대립이 없다**는 뜻이고 (`0:10`), `r_AM_S = 0` 은 소립이 없다는',
          '뜻이다 (`10:0`) — 크기가 0 인 입자가 아니다.',
          '',
          '⚠ **함정 하나 알려둔다**: 6 mAh 세트에는 완전한 5점 시리즈가 **둘** 있고 `r_SE` 로 갈린다',
          '(0.5 계열 `real_1..real_5` · 1.5 계열 `real_6..real_10`).  파일명이 `real_5..real_9` 로',
          '연속이라 그 다섯을 집기 쉬운데, 그러면 **10:0 팔만 r_SE 가 3배 다른** 시리즈가 되어',
          'P:S 효과와 SE 크기 효과가 섞인다.  이 폴더는 한 계열로 통제된 것만 담았다.',
          '',
          '## 4. 자동 검증', '']
    return L


def verify_raw(out_root, rows):
    """★ fail-closed — README 가 적은 단위 배율이 **실제 파일과 맞는지** 대조한다.
    핸드오프에서 가장 잘 나는 사고가 단위이고, 그건 데이터로 검산할 수 있다."""
    msg, ok = [], True
    for r in rows:
        f = os.path.join(out_root, f'am_spheres_ps{r["ps"].replace(":", "_")}.csv')
        if not os.path.exists(f):
            ok = False
            msg.append(f'⛔ {os.path.basename(f)} 없음')
            continue
        radii, types = set(), {}
        for row in csv.reader(open(f, encoding='utf-8')):
            if not row or row[0].lstrip().startswith('#'):
                continue
            radii.add(round(float(row[4]) * UM_PER_LU, 3))
            types[row[0]] = types.get(row[0], 0) + 1
        want = {float(r['design'][k]) for k in ('r_AM_P', 'r_AM_S')} - {0.0}
        if not want <= radii:
            ok = False
            msg.append(f'⛔ {r["ps"]}: 파일 반경×{UM_PER_LU:.0f} = {sorted(radii)} µm 인데 '
                       f'설계점은 {sorted(want)} µm — **단위 배율이 틀렸거나 케이스가 다르다**')
        else:
            msg.append(f'✓ {r["ps"]}: 반경×{UM_PER_LU:.0f} = {sorted(radii)} µm = 설계점 일치 · '
                       f'입자 {sum(types.values()):,}개 ' +
                       '(' + ' · '.join(f'type {k} {v:,}' for k, v in sorted(types.items())) + ')')
    return ok, msg


def _selftest():
    ok, fail = 0, []

    def chk(n, c):
        nonlocal ok
        (ok := ok + 1) if c else fail.append(n)
        print(('  PASS  ' if c else '  FAIL  ') + n)

    rows05, miss05 = resolve('0.5')
    rows15, miss15 = resolve('1.5')
    chk(f'① r_SE 0.5 시리즈 5점 해석 ({len(rows05)}점, 누락 {miss05})', len(rows05) == 5 and not miss05)
    chk(f'② r_SE 1.5 시리즈 5점 해석 ({len(rows15)}점, 누락 {miss15})', len(rows15) == 5 and not miss15)
    o5, m5 = check_controlled(rows05)
    o15, m15 = check_controlled(rows15)
    chk('③ 0.5 시리즈가 통제됐다', o5)
    chk('④ 1.5 시리즈가 통제됐다', o15)
    #  ⑤ ★ 핵심 회귀 — 이름 순서대로 real_5..real_9 를 집으면 **교락이 잡혀야** 한다
    d, m = load_tables()
    naive = []
    for nm in ('input_6mAh_real_6', 'input_6mAh_real_7', 'input_6mAh_real_8',
               'input_6mAh_real_9', 'input_6mAh_real_5'):
        naive.append({'ps': m[nm]['name'][-1], 'name': nm, 'case': m[nm]['case'],
                      'design': d[m[nm]['case']]})
    on, mn = check_controlled(naive)
    chk('⑤ ★ 이름 연속(real_5..real_9) 선택은 r_SE 교락으로 **거부**된다',
        (not on) and any('r_SE' in x for x in mn))
    #  ⑥ 두 시리즈의 r_SE 가 실제로 다르다 (그래서 갈라 놓는 것이 의미가 있다)
    r5 = {float(r['design']['r_SE']) for r in rows05}
    r15 = {float(r['design']['r_SE']) for r in rows15}
    chk(f'⑥ 두 시리즈의 r_SE 가 다르다 ({r5} vs {r15})', r5 == {0.5} and r15 == {1.5})
    #  ⑦ 명령 생성이 **기존 두 도구**를 부른다 (새 추출기 금지)
    cmd = emit_commands(rows05, '/R', '/O')
    chk('⑦ 명령이 mpm_input_from_case + comsol_export 를 부른다',
        cmd.count('mpm_input_from_case.py') == 5 and cmd.count('comsol_export.py') == 5)
    #  ⑧⑨ ★ raw 핸드오프 — **단위 검증이 실제로 작동**하는지 (합성 파일 왕복)
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        def mk(scale):
            for r in rows05:
                g = r['design']
                rr = [float(g['r_AM_P']), float(g['r_AM_S'])]
                lines = ['# type,x,y,z,r  # synth']
                for t, rad in ((1, rr[0]), (2, rr[1])):
                    if rad == 0.0:
                        continue
                    for i in range(3):
                        lines.append(f'{t},0.01,0.02,{0.001*i:.6f},{rad/scale:.6f}')
                open(os.path.join(td, f"am_spheres_ps{r['ps'].replace(':', '_')}.csv"),
                     'w', encoding='utf-8').write('\n'.join(lines) + '\n')
        mk(UM_PER_LU)                       # 올바른 배율
        v_ok, v_msg = verify_raw(td, rows05)
        chk(f'⑧ 올바른 배율(×{UM_PER_LU:.0f})은 통과한다', v_ok)
        mk(1.0)                             # 틀린 배율 = µm 를 그대로 적은 파일
        b_ok, b_msg = verify_raw(td, rows05)
        chk('⑨ ★ 배율이 틀린 파일은 **거부**된다 (핸드오프 최대 사고 지점)',
            (not b_ok) and any('단위 배율' in x for x in b_msg))
    #  ⑩ raw 명령은 comsol_export 를 부르지 않는다 (지시: raw 만 넘긴다)
    raw = emit_raw(rows05, '/R', '/O')
    chk('⑩ raw 모드는 comsol_export 를 안 부르고 README 생성을 붙인다',
        'comsol_export.py' not in raw and '--write-readme' in raw
        and raw.count('mpm_input_from_case.py') == 5)
    print(f'\ncomsol_ps_series_6mah selftest: {ok}/{ok + len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--r-se', default='0.5', choices=('0.5', '1.5'),
                    help='어느 시리즈인가 (기본 0.5 = 생산 기본값)')
    ap.add_argument('--check', action='store_true', help='통제 검증만')
    ap.add_argument('--emit-commands', action='store_true')
    ap.add_argument('--raw', action='store_true',
                    help='COMSOL 패키징 없이 **AM 좌표 raw + 자기설명 README** 만 (후배 핸드오프)')
    ap.add_argument('--write-readme', action='store_true',
                    help='이미 뽑힌 out-root 에 README 를 쓰고 단위를 검증한다')
    ap.add_argument('--results-root', default='~/Yonghoon-DEM-DFT/webapp/results')
    ap.add_argument('--out-root', default='comsol_6mah')
    ap.add_argument('--extra', default='', help='mpm_input_from_case 에 붙일 추가 인자')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())

    rows, miss = resolve(a.r_se)
    if miss:
        print('⛔ 해석 실패:', '; '.join(miss))
        raise SystemExit(2)
    print(f'6 mAh P:S 시리즈 (r_SE = {a.r_se} µm)\n')
    print(f"{'P:S':>6} {'name':22s} {'case':22s} {'r_AM_P':>7} {'r_AM_S':>7} {'r_SE':>6} "
          f"{'AM_wt':>7} {'porosity':>9}")
    for r in rows:
        g = r['design']
        print(f"{r['ps']:>6} {r['name']:22s} {r['case']:22s} {g['r_AM_P']:>7} {g['r_AM_S']:>7} "
              f"{g['r_SE']:>6} {g['AM_wt']:>7} {g['dem_porosity']:>9}")
    ok, msg = check_controlled(rows)
    print()
    for x in msg:
        print('  ' + x)
    if not ok:
        print('\n⛔ 통제되지 않은 시리즈 — COMSOL 로 넘기지 말 것')
        raise SystemExit(1)
    print('\n✓ 통제 확인 — P:S 만 변한다')

    if a.write_readme:
        #  이미 뽑힌 폴더에 README 를 쓰고 **단위를 실제 파일과 대조**한다 (fail-closed).
        vok, vmsg = verify_raw(a.out_root, rows)
        L = readme(rows, a.out_root) + ['```'] + vmsg + ['```', '']
        L += (['✓ 단위·케이스 검증 통과.'] if vok else
              ['⛔ **검증 실패 — 이 폴더를 넘기지 말 것.**  위 줄이 무엇이 어긋났는지 말한다.'])
        L += ['', f'생성: `scripts/{os.path.basename(__file__)}` (2026-08-18)']
        os.makedirs(a.out_root, exist_ok=True)
        with open(os.path.join(a.out_root, 'README.md'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(L) + '\n')
        print(f"\n→ {a.out_root}/README.md")
        for x in vmsg:
            print('  ' + x)
        raise SystemExit(0 if vok else 1)

    if a.raw or a.emit_commands:
        gen = emit_raw if a.raw else emit_commands
        sh = gen(rows, os.path.expanduser(a.results_root), a.out_root, a.extra)
        print('\n' + '─' * 70)
        print(sh)
    elif not a.check:
        print('\n(명령을 보려면 --raw 또는 --emit-commands)')
    sys.stdout.flush()
