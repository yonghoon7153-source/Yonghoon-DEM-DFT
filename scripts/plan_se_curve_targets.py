#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""임의 베드의 SE 응답곡선 측정점 설계 — φ-전이 가정의 **직접 검증**용.

═══ 왜 필요한가 ═══════════════════════════════════════════════════════════════════════
`am_load_balance_jam.REAL14_SE_CURVE` 는 real_14(2mAh, 30 µm) 베드에서 잰 11점이고,
색인 변수를 두께가 아니라 **φ_SE_local = V_SE/(A·h − V_AM)** 로 바꿔 "베드를 옮겨갈 수
있다"고 전제한다.  그런데 selftest 가 고정한 것은 **수학적 불변성**(베드를 통째로 k배
하면 φ 가 정확히 불변)뿐이다 — 조성·AM 배치가 **다른** 베드에서도 같은 σ(φ) 가 나오는지는
미검증인데, 6mAh 10케이스 판정과 다압력 판정이 이미 이 곡선을 쓰고 있다.

전이가 성립할 물리적 이유: SE 응력은 SE 가 자기 몫의 공간에서 얼마나 조밀한가(=φ)에
달린 물성이다.  깨질 이유: AM 배치가 다르면 SE 가 갇힌 공간의 **모양**(협착 채널 분포)도
달라 같은 φ 에서도 응력 전달이 다를 수 있다.  → 실측으로 가른다.

이 스크립트는 대상 킷의 (V_AM, V_SE, A) 를 읽어 **real_14 곡선의 φ 격자에 대응하는 ε_target**
을 역산하고, 그대로 붙여 실행할 --compact-to 명령을 찍는다.  φ 축에서 겹쳐야 비교가 된다.

  python3 scripts/plan_se_curve_targets.py --kit /home/ubuntu/Yonghoon-DEM-DFT/kit_ps_7_3
  python3 scripts/plan_se_curve_targets.py --kit <킷> --phi 0.60,0.70,0.80 --gpu-mem 8
  python3 scripts/plan_se_curve_targets.py --selftest
"""
from __future__ import annotations

import argparse
import csv
import glob
import os
import sys

import numpy as np

UM_PER_LU = 1000.0
# real_14 곡선의 상승·포화 구간을 대표하는 φ 격자 (전이 검증은 겹치는 구간에서만 뜻이 있다).
# 무응력 구간(φ≲0.58)은 σ=0 이라 정보량이 없어 뺀다.
PHI_DEFAULT = (0.60, 0.67, 0.72, 0.81, 0.86)


def read_scaffold(path):
    rows = [r for r in csv.reader(open(path)) if r and not r[0].lstrip().startswith('#')]
    if not rows:
        sys.exit(f'{path}: 데이터 행 없음')
    r = np.array([float(x[4]) for x in rows]) * UM_PER_LU
    c = np.array([[float(v) for v in x[1:4]] for x in rows]) * UM_PER_LU
    return c, r


def bed_overlap(kit_dir, area, v_sph_sum):
    """union 관례 고체높이 보정용 겹침 [µm³] — **킷 metrics 에서 역산**.

    ε_union 목표를 sphere 관례로 잡으면 φ 도달점이 곡선 위로 밀린다 (real_14: 겹침
    946.7 µm³ = 1.25 %p → φ +0.03).  전이 검증은 **겹치는 φ 구간**을 노리는 것이 목적이라
    그 밀림을 없애야 한다.
    ★ 기하 KDTree 로 직접 세면 3~8만 점에서 파이썬 루프가 분 단위로 느리다.  킷의 MPM
    metrics 에 이미 (thickness_um, porosity_settled_pct[union]) 가 있으므로
        solid_union = h·(1−ε/100)  ⇒  겹침 = V_sphere − solid_union·A
    로 **한 줄에** 얻는다 (같은 정의, 측정 기반).  metrics 가 없으면 0 + 라벨.
    """
    import json
    # 킷 바로 아래 + run_*/ 하위 (run_mpm.sh 는 실행마다 run_<태그>/ 에 metrics 를 남긴다)
    cands = []
    for nm in ('mpm_metrics.json', 'mpm_payload.json'):
        cands.append(os.path.join(kit_dir, nm))
        cands += sorted(glob.glob(os.path.join(kit_dir, '*', nm)), reverse=True)
    for p in cands:
        if not os.path.exists(p):
            continue
        try:
            j = json.load(open(p))
        except Exception:
            continue
        m = j if 'thickness_um' in j else (j.get('mpm_metrics') or j.get('metrics') or {})
        h = m.get('thickness_um') or m.get('thickness_mpm_um')
        e = m.get('porosity_settled_pct') or m.get('porosity_mpm_pct')
        if h and e is not None:
            ov = v_sph_sum - float(h) * (1.0 - float(e) / 100.0) * area
            tag = f'{os.path.relpath(p, kit_dir)} (h {float(h):.3f}µm · ε_union {float(e):.3f}%)'
            # ★ 음수 = union 고체가 AM+SE 구 부피 합보다 크다 = 기하적으로 불가능.
            #   실제 원인은 metrics 가 **첨가제 포함**(run_VGCF1_PTFE1_… 등) solid 를 재는데
            #   여기 v_sph_sum 은 AM+SE 스캐폴드만이라는 것이다.  조용히 0 으로 클램프하면
            #   "보정했다" 는 거짓 인상을 준다 (§F1) → 사유를 그대로 노출하고 미보정 처리.
            if ov < 0:
                return (0.0, f'⚠ 역산 음수 ({ov:,.0f} µm³) — {tag} 가 AM+SE 외 상(첨가제 등)을 '
                             f'포함 → 미보정 (실행은 scaffold 만 쓰므로 순수 AM+SE 로 돈다; '
                             f'φ 는 사후 실측 환산)')
            # ⚠ 겹침은 압밀 상태의 함수 — 다른 두께 목표에 쓰면 근사다.  무해한 이유:
            #   목표는 도달점 유도용이고 곡선은 **실측 정착값**(json)으로 만든다.
            return (float(ov), tag)
    return 0.0, None


def bed_volumes(kit_dir):
    """킷 → (V_AM, V_SE, A, box_um).  A 는 스캐폴드 측면 외피(킷에 box 기록이 없을 때)."""
    am_p = os.path.join(kit_dir, 'am_scaffold.csv')
    se_p = os.path.join(kit_dir, 'se_scaffold.csv')
    for p in (am_p, se_p):
        if not os.path.exists(p):
            sys.exit(f'{p} 없음 — mpm_input_from_case.py 로 만든 킷이어야 한다')
    ac, ar = read_scaffold(am_p)
    sc, sr = read_scaffold(se_p)
    v_am = float((4.0 / 3.0 * np.pi * ar ** 3).sum())
    v_se = float((4.0 / 3.0 * np.pi * sr ** 3).sum())
    lat = 50.0
    import json
    mi = os.path.join(kit_dir, 'mpm_input.json')
    if os.path.exists(mi):
        j = json.load(open(mi))
        if j.get('lateral_box'):
            lat = float(j['lateral_box']) * UM_PER_LU
    return v_am, v_se, lat * lat, lat


def eps_for_phi(phi, v_am, v_se, area, overlap_um3=0.0):
    """φ_SE_local 목표 → (두께 h, ε_union 목표 %).

    φ = V_SE/(A·h − V_AM)  ⇒  h = (V_SE/φ + V_AM)/A
    ε_union = 1 − (V_AM + V_SE − 겹침)/(A·h).  겹침을 모르면 0 (= sphere 관례 상한)로 두고
    라벨을 남긴다 — --compact-to 는 MPM 자신의 union porosity 를 기준으로 멈추므로 근사가
    ε_target 을 몇 %p 밀 수 있다.  ★ 그래도 무해하다: 곡선은 **실측 정착값**(json 의
    porosity_settled_pct·thickness_um)으로 만들고 목표는 도달점 유도용일 뿐이다.
    """
    if phi <= 0:
        return None, None
    h = (v_se / float(phi) + v_am) / area
    solid = (v_am + v_se - overlap_um3) / area
    return h, (1.0 - solid / h) * 100.0


def _selftest():
    ok, fail = 0, []

    def chk(n, c):
        nonlocal ok
        ok += 1 if c else 0
        if not c:
            fail.append(n)

    # real_14 실측으로 왕복: φ 0.5956 ↔ 두께 30.218 µm (곡선 4번째 점)
    V_AM, V_SE, A = 46679.9, 17190.8, 2500.0
    h, eps = eps_for_phi(0.5956, V_AM, V_SE, A, 946.7)
    chk('real_14 φ→h 왕복 (곡선 실측 30.218 µm)', abs(h - 30.218) < 0.02)
    chk('그 높이의 ε_union 이 실측 16.67 % 와 일치', abs(eps - 16.67) < 0.05)
    # 단조: φ 가 크면(조밀) 두께가 작다
    h1, _ = eps_for_phi(0.60, V_AM, V_SE, A)
    h2, _ = eps_for_phi(0.85, V_AM, V_SE, A)
    chk('φ↑ → h↓ (조밀할수록 얇다)', h2 < h1)
    # 스케일 불변: 베드를 k배 하면 같은 φ 가 k배 두께
    k = 3.7
    hk, _ = eps_for_phi(0.5956, V_AM * k, V_SE * k, A)
    chk('★ 베드 k배 → 같은 φ 의 두께도 k배 (전이 가정의 수학적 근거)',
        abs(hk - h * k) < 1e-6 * h * k)
    chk('φ≤0 은 None', eps_for_phi(0.0, V_AM, V_SE, A)[0] is None)
    # ★ metrics 역산이 real_14 의 알려진 겹침 946.7 µm³ 를 되돌려주는가
    import json as _json, tempfile as _tmp
    _d = _tmp.mkdtemp()
    _json.dump({'thickness_um': 30.218, 'porosity_settled_pct': 16.670},
               open(os.path.join(_d, 'mpm_metrics.json'), 'w'))
    _ov, _src = bed_overlap(_d, A, V_AM + V_SE)
    # ★ 항등식 왕복이 옳은 검증이다.  절대값을 기하 렌즈(946.7, 주기 KDTree)와 맞추려 하면
    #   안 된다 — metrics 역산은 **MPM 복셀 union** 관례(양자화 vox 0.13µm + SE-in-AM 축출)라
    #   기하값과 ~3 % 다른 게 정상이고, --compact-to 가 그 관례로 멈추므로 이쪽이 정확하다.
    _h_rt, _e_rt = eps_for_phi(0.5956, V_AM, V_SE, A, _ov)
    chk('★ metrics 역산 왕복: φ→(h, ε) 가 측정 그 점(30.218 µm, 16.670 %)을 재현',
        abs(_h_rt - 30.218) < 0.02 and abs(_e_rt - 16.670) < 0.02)
    chk('역산 겹침이 기하 렌즈(946.7)와 같은 자릿수 (관례차 ~3 %)',
        0.9 * 946.7 < _ov < 1.1 * 946.7)
    chk('metrics 없으면 0 + 라벨 없음 (조용한 보정 금지)',
        bed_overlap(_tmp.mkdtemp(), A, V_AM + V_SE) == (0.0, None))
    # ★ 첨가제 포함 metrics → 역산 음수: 클램프만 하고 침묵하면 "보정됨" 오해 (§F1)
    _d2 = _tmp.mkdtemp()
    _json.dump({'thickness_um': 113.199, 'porosity_settled_pct': 12.203},
               open(os.path.join(_d2, 'mpm_metrics.json'), 'w'))
    _ov2, _src2 = bed_overlap(_d2, A, 243067.0)
    chk('★ 역산 음수(첨가제 포함 metrics) → 0 + 사유 노출',
        _ov2 == 0.0 and _src2 is not None and '음수' in _src2)
    print(f'selftest: {ok}/{ok + len(fail)} PASS' + (f'  FAILED {fail}' if fail else ''))
    return 0 if not fail else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--kit', help='mpm_input_from_case.py 산출 킷 (am/se_scaffold.csv)')
    ap.add_argument('--phi', default='', help=f'쉼표 φ 목록 (기본 {",".join(map(str, PHI_DEFAULT))})')
    ap.add_argument('--n-grid', type=int, default=384)
    ap.add_argument('--sub', type=int, default=160)
    ap.add_argument('--gpu-mem', type=float, default=8.0)
    ap.add_argument('--repo', default='/home/ubuntu/Yonghoon-DEM-DFT', help='V100 리포 경로')
    ap.add_argument('--no-overlap', action='store_true',
                    help='겹침 계산 생략 (빠르지만 ε 목표가 ~1%%p 밀려 φ 도달점이 위로 이동)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    if not a.kit:
        ap.error('--kit 이 필요합니다 (또는 --selftest)')

    v_am, v_se, area, lat = bed_volumes(a.kit)
    ov, ov_src = (0.0, None)
    if not a.no_overlap:
        ov, ov_src = bed_overlap(a.kit, area, v_am + v_se)
    phis = [float(x) for x in a.phi.split(',')] if a.phi else list(PHI_DEFAULT)
    name = os.path.basename(os.path.normpath(a.kit))
    print(f'베드 {name}:  V_AM {v_am:,.0f} · V_SE {v_se:,.0f} µm³ · 측면 {lat:g} µm '
          f'(SE/solid {v_se / (v_am + v_se):.1%})')
    print(f'  겹침 {ov:,.1f} µm³ = 고체높이 {ov / area:.3f} µm  '
          + (f'← {ov_src}' if ov_src else
             '(⚠ 미보정 — metrics 부재 or --no-overlap: ε 목표가 ~1%p 밀린다)'))
    print(f'{"φ_SE":>7}{"두께(µm)":>10}{"ε_union 목표(%)":>16}')
    rows = []
    for p in phis:
        h, e = eps_for_phi(p, v_am, v_se, area, ov)
        if h is None:
            continue
        print(f'{p:7.4f}{h:10.2f}{e:16.2f}')
        rows.append((p, h, e))

    print('\n실행 (V100, setsid nohup — ssh 끊겨도 생존):')
    print(f'''cd {a.repo}/se_curve
setsid nohup bash -c '
  source {a.repo}/scripts/activate_dem.sh >/dev/null 2>&1
  cd {a.repo}/se_curve
  R={a.repo}
  for E in {" ".join(f"{e:.2f}" for _, _, e in rows)}; do
    T=$(echo $E | tr -d .)
    echo "=== {name} eps ${{E}}%  $(date "+%H:%M:%S")"
    t0=$SECONDS
    python3 -u $R/scripts/mpm3d_compaction.py \\
        --arch cuda --gpu-mem {a.gpu_mem:g} \\
        --am-scaffold {a.kit}/am_scaffold.csv \\
        --se-dump     {a.kit}/se_scaffold.csv \\
        --n-grid {a.n_grid} --sub {a.sub} --print-every 5 \\
        --protocol hold --periodic \\
        --compact-to $E --save-metrics xfer_{name}_e${{T}}.json \\
        > xfer_{name}_e${{T}}.log 2>&1
    echo "  EXIT=$?  wall=$((SECONDS-t0))s"
  done
  echo "XFER DONE $(date "+%H:%M:%S")"
' > xfer_{name}.log 2>&1 < /dev/null &
echo "PID=$!"''')
    print(f'\n판정: 나온 json 의 (thickness_um, final_stress_GPa) 를 φ 로 환산해')
    print(f'      REAL14_SE_CURVE 와 같은 φ 에서 σ 가 몇 % 다른지 본다.')
    print(f'      ⇒ ≲10 % = 전이 성립(곡선 하나로 전 코퍼스) / ≳25 % = 베드별 곡선 필요')
    print(f'      환산: φ = {v_se:,.1f}/({area:,.0f}·h − {v_am:,.1f})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
