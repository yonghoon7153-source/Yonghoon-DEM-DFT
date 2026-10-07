#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEM 3D 뷰어 — 입자 하중 보기 (1저자 10-07 결정 · 웹앱 묶음 #11 · WEB-06).

  #11 AM 만 칠하기 — SE 숨김 · 색 범위 = AM 만 · 두 양: (a) Love–Weber 입자 응력 (σ_VM · full_metrics stress_ratio_<상>_lw 와 같은
      정의 = `dem_analysis_core.calc_love_weber_stress` 를 그대로 부른다 · 비 = σ_VM,i / ⟨σ_VM⟩_전 입자) · (b) AM 입자마다 최대 AM–AM
      접촉 법선력 (µN · `calc_contact_force_distribution` 과 같은 환산 1e6/scale · 압축 접촉만) · 벽 (바닥 · 판) 에 닿은 입자 표지
      (그 입자의 LW 응력에는 벽 힘이 없다 — `calc_love_weber_stress` 의 벽 규칙 그대로).
  WEB-06 'Stress Concentration' — 양 = 입자별 최대 접촉 압력 |Fn| / A (hooke/hysteresis 에서 쌍 유형마다 거의 일정 ≈ k/(2πR*) — 하중이
      아니다) · 이름 정정 ("Max contact pressure") · 당김 (접착) 접촉은 범위에서 뺀다 (δ ≈ 0 면적의 10⁴–10⁶ MPa 튐) · 한정어 = 툴팁.

  ⚠ 자료 길: 3D 데이터 (`/3d-data` aux) 는 `webapp/app.py` (194 봉인 파일) 가 키를 **하나씩** 옮겨 담고 캐시 스키마 (12) 도 거기에 있다 →
    새 자료 (`aux.load_view`) 는 그 파일을 바꿔야 화면에 온다.  봉인 중에는 바꾸지 않는다 — 계산 (`scripts/viewer3d_data.py`) ·
    뷰어 (`webapp/static/js/viewer3d.js`) 는 지금 넣고, app.py 변경은 **발사 뒤 패치** `docs/reviews/webapp_load_view_deferred_20261007.patch`
    로 둔다.  이 시험의 [P] 절이 그 패치를 임시 사본에 적용해 실제로 자료가 오는지 (live · archive · 캐시 HIT · 옛 스키마) 본다 —
    패치가 이미 적용된 트리에서는 진짜 app.py 를 본다.

  [S] 접촉 법선력 부호 (압축 · 당김 · 판정 불가) — 최소영상 · 접촉점 대체 · 0 힘.
  [W] 최대 접촉 압력 (압축만) — 손 계산 · 옛 stress_max (aggregate_particle_metrics) 는 바이트 그대로 · 당김 때문에 옛 값이 더 큰 입자 수.
  [F] 최대 AM–AM 접촉 힘 — 손 계산 · 당김 · 판정 불가 제외 · µN 환산 = calc_contact_force_distribution.
  [L] Love–Weber — 정본 함수 배열과 비트 같음 (AM 만 싣는다) · 상 평균 비 = 정본 type_stress 비 · 벽 표지 수 = 정본 벽 수 · 예산 초과 = NOT_COMPUTED.
  [R] real14 커밋 원자료 — 부호 = WEB-06 점검 (contact_pressure_check: 주기 너머 뺀 압축 95,277 · 당김 6,757) · 압축만 최대 ≥ 1e4 MPa 0 개 ·
      LW 상 비 = 2.737 (AM_P) · 2.341 (AM_S) · 0.981 (SE) · 벽 표지 = 정본 (AM_P 바닥 7 · 판 8 · AM_S 46 · 38).
  [J] 뷰어 (node) — 드롭다운 이름 · AM 만 보기 함수 (양 · 범위 = AM 만 · 벽 회색 · 컬러바) · 최대 접촉 압력 범례 (압축만 / 옛 계산 경고 · 툴팁) ·
      자료 없음 안내 (발사 뒤 패치).
  [Z] Z-profile 이름 정정 (탭 · PNG 제목 — 값은 옛 계산 그대로 · "당김 포함" 표기 · 압축만으로 바꾸는 것은 다음 묶음).
  [P] 발사 뒤 패치 — 적용 확인 · 패치한 app 의 /3d-data (live · archive · 캐시 HIT · 옛 스키마 12 → 다시 계산).
  [X] check_all 배선.

  python3 webapp/test_viewer_load_view.py        # 종료코드 0 = PASS
"""
import copy
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = os.path.join(ROOT, 'scripts')
VIEWER_JS = os.path.join(HERE, 'static', 'js', 'viewer3d.js')
CHECK_ALL = os.path.join(SCRIPTS, 'check_all.sh')
PATCH = os.path.join(ROOT, 'docs', 'reviews', 'webapp_load_view_deferred_20261007.patch')
sys.path.insert(0, HERE)
sys.path.insert(0, SCRIPTS)
from test_closed_param_labels import js_fn, run_node   # noqa: E402  (렌더된 JS 를 잘라 node 로 — 같은 도구)

_ok, _fail = 0, []
TM = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
SCALE = 1000.0


def chk(name, cond, extra=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f' — {extra}' if extra else ''))
    return bool(cond)


def rel(a, b):
    try:
        a, b = float(a), float(b)
    except (TypeError, ValueError):
        return math.inf
    return abs(a - b) / max(abs(a), abs(b), 1e-300)


def ikeys(d):
    return {int(k): v for k, v in (d or {}).items()}


# ══════════════════════════════════════════════════════════════════════════════
#  합성 침대 (sim 단위 · scale 1000 → µm) — 상자 0.05 · 판 0.03 · 접촉은 모두 기하가 맞다 (접촉점이 두 입자 안 — LW 검사 통과)
#    1 AM_P (r 0.006) · 2 · 3 AM_S (r 0.002) · 4 · 5 AM_S (x 주기 경계를 넘는 접촉) · 10–14 SE (r 0.0005) · 15 · 16 AM_S (접촉 없음 ·
#    바닥 · 판) · 12 · 13 SE 바닥 · 14 SE 판
#    접촉 (id1, id2, |F|, 부호, 면적, δ): 1–2 압축 · 2–3 당김 (힘이 더 크다) · 4–5 압축 (주기 너머) · 4–5 δ = 0 행 (힘이 더 크다) ·
#    1–10 당김 (δ ≈ 0 · 면적 거의 0 → 압력 튐) · 1–11 압축 · 1–11 힘 0 행 · 12–13 압축 (둘 다 바닥)
# ══════════════════════════════════════════════════════════════════════════════
BOX, PLATE = 0.05, 0.03
RAD = {1: 0.006, 2: 0.002, 3: 0.002, 4: 0.002, 5: 0.002, 10: 0.0005, 11: 0.0005, 12: 0.0005, 13: 0.0005,
       14: 0.0005, 15: 0.002, 16: 0.002}
TYPE = {1: 1, 2: 2, 3: 2, 4: 2, 5: 2, 10: 3, 11: 3, 12: 3, 13: 3, 14: 3, 15: 2, 16: 2}


def _mi(d):
    d = list(d)
    for ax in (0, 1):
        d[ax] -= BOX * round(d[ax] / BOX)
    return d


def _unit(v):
    n = math.sqrt(sum(x * x for x in v))
    return [x / n for x in v]


def synth_bed():
    P = {}
    dl = 1e-5
    P[1] = [0.020, 0.020, 0.012]
    P[2] = [P[1][0] + RAD[1] + RAD[2] - dl, 0.020, 0.012]                     # 1–2 x 방향
    P[3] = [P[2][0], 0.020 + RAD[2] + RAD[3] - dl, 0.012]                     # 2–3 y 방향
    P[4] = [0.0485, 0.035, 0.012]
    P[5] = [0.0485 + RAD[4] + RAD[5] - dl - BOX, 0.035, 0.012]                # 4–5 x 주기 경계 너머 (원 좌표 차 0.046)
    P[10] = [0.020, 0.020, P[1][2] + RAD[1] + RAD[10] - 1e-9]                 # 1–10 z 방향 · δ ≈ 0
    P[11] = [0.020, 0.020 - (RAD[1] + RAD[11] - dl), 0.012]                   # 1–11 −y 방향
    P[12] = [0.030, 0.005, 0.0004]                                            # 바닥 (z − r < 0)
    P[13] = [0.030, 0.005 + RAD[12] + RAD[13] - dl, 0.0004]                   # 12–13 y 방향 · 13 도 바닥
    P[14] = [0.040, 0.010, PLATE - 0.0003]                                    # 판 (z + r > 판)
    P[15] = [0.010, 0.040, 0.0015]                                            # AM_S 바닥 (접촉 없음)
    P[16] = [0.010, 0.040, PLATE - 0.0015]                                    # AM_S 판 (접촉 없음)
    rows = []

    def con(i, j, mag, sign, area, delta, d_geom=dl):
        u = _unit(_mi([P[i][k] - P[j][k] for k in range(3)]))
        fn = [sign * mag * x for x in u]                                    # id1 이 받는 법선력 (+ = 밀어냄)
        cp = [P[i][k] - (RAD[i] - d_geom / 2.0) * u[k] for k in range(3)]   # 접촉점 = 두 입자 안 (기하 겹침의 가운데)
        rows.append(dict(id1=i, id2=j, fn=fn, area=area, delta=delta, cp=cp))
    con(1, 2, 0.02, +1, 2e-7, dl)
    con(2, 3, 0.5, -1, 1e-7, dl)
    con(4, 5, 0.01, +1, 1e-7, dl)
    con(4, 5, 0.05, +1, 1e-7, 0.0)                                          # δ = 0 행 (힘 · 면적은 있다) — 압력 · 힘에서 뺀다
    con(1, 10, 0.003, -1, 1e-12, 1e-9, d_geom=1e-9)
    con(1, 11, 0.004, +1, 5e-8, dl)
    con(1, 11, 0.0, +1, 1e-8, dl)                                           # 힘 0 행
    con(12, 13, 0.001, +1, 2e-8, dl)
    return P, rows


def write_bed(d, P, rows, mesh=True, box=True):
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'atoms.csv'), 'w') as f:
        f.write('id,type,x,y,z,radius\n')
        for i in sorted(P):
            f.write(f'{i},{TYPE[i]},{P[i][0]!r},{P[i][1]!r},{P[i][2]!r},{RAD[i]!r}\n')
    with open(os.path.join(d, 'contacts.csv'), 'w') as f:
        f.write('p1_x,p1_y,p1_z,p2_x,p2_y,p2_z,id1,id2,periodic_flag,fx,fy,fz,fn_x,fn_y,fn_z,ft_x,ft_y,ft_z,'
                'torque_x,torque_y,torque_z,contact_area,delta,cp_x,cp_y,cp_z\n')
        for r in rows:
            p1, p2 = P[r['id1']], P[r['id2']]
            fn, cp = r['fn'], r['cp']
            f.write(','.join(repr(float(x)) for x in (*p1, *p2)) + f",{r['id1']},{r['id2']},0,"
                    + ','.join(repr(float(x)) for x in (*fn, *fn, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, r['area'], r['delta'], *cp)) + '\n')
    if mesh:
        with open(os.path.join(d, 'mesh_info.json'), 'w') as f:
            json.dump({'plate_z': PLATE}, f)
    if box:
        with open(os.path.join(d, 'input_params.json'), 'w') as f:
            json.dump({'box_x': BOX, 'box_y': BOX}, f)


# ══════════════════════════════════════════════════════════════════════════════
#  [S] 부호
# ══════════════════════════════════════════════════════════════════════════════
def section_sign():
    print('[S] 접촉 법선력 부호 — 최소영상 · 접촉점 대체 · 0 힘')
    import numpy as np
    import viewer3d_data as V
    f = getattr(V, 'contact_force_sign', None)
    if not chk('S0 viewer3d_data.contact_force_sign 있다', callable(f)):
        return
    p1 = np.array([[0.0, 0, 0], [0.0, 0, 0], [0.5, 0, 0], [0.5, 0, 0], [0.0, 0, 0], [0.0, 0, 0]])
    p2 = np.array([[1.9, 0, 0], [1.9, 0, 0], [9.6, 0, 0], [9.6, 0, 0], [1.9, 0, 0], [0.0, 0, 0]])
    fn = np.array([[-1.0, 0, 0], [1.0, 0, 0], [1.0, 0, 0], [-1.0, 0, 0], [0.0, 0, 0], [1.0, 0, 0]])
    r1 = np.array([1.0, 1.0, 0.5, 0.5, 1.0, 1.0])
    r2 = r1.copy()
    cp = np.array([[0.95, 0, 0], [0.95, 0, 0], [0.05, 0, 0], [0.05, 0, 0], [0.95, 0, 0], [0.0, 0, 0]])
    s_box = f(fn, p1, p2, r1, r2, box_xy=(10.0, 10.0))
    s_nobox = f(fn, p1, p2, r1, r2)
    s_cp = f(fn, p1, p2, r1, r2, cp=cp)
    chk(f'S1 상자 최소영상 — 압축 · 당김 · 주기 너머 압축 · 당김 · 힘 0 · 거리 0 = [1, −1, 1, −1, 0, 0] ({list(s_box)})',
        list(s_box) == [1, -1, 1, -1, 0, 0])
    chk(f'S2 상자 없음 · 접촉점 없음 → 주기 너머 두 접촉은 판정 불가 0 (원 좌표 차로 거꾸로 읽지 않는다) ({list(s_nobox)})',
        list(s_nobox) == [1, -1, 0, 0, 0, 0])
    chk(f'S3 상자 없음 · 접촉점 있음 → 주기 너머도 접촉점 쪽 가지로 판정 ({list(s_cp)})', list(s_cp) == [1, -1, 1, -1, 0, 0])
    chk('S4 규약 문구 — 덤프 fn = id1 이 받는 법선력 · 밀어냄 = 압축 · 최소영상', all(
        x in str(getattr(V, 'CONTACT_SIGN_RULE', '')) for x in ('id1', '압축', '당김', '최소영상')))


# ══════════════════════════════════════════════════════════════════════════════
#  [W] [F] [L] 합성 침대
# ══════════════════════════════════════════════════════════════════════════════
def section_synth(tmp):
    print('[W · F · L] 합성 침대 — 최대 접촉 압력 (압축만) · 최대 AM–AM 힘 · Love–Weber (정본 함수)')
    import viewer3d_data as V
    P, rows = synth_bed()
    d = os.path.join(tmp, 'synth')
    write_bed(d, P, rows)
    fn_ = getattr(V, 'particle_load_view_for_case', None)
    if not chk('W0 viewer3d_data.particle_load_view_for_case 있다', callable(fn_)):
        return None
    lv = fn_(d, TM, SCALE)
    chk(f'W1 스키마 · 입력 기록 ({lv.get("schema")} · {(lv.get("inputs") or {}).get("box_source")} · '
        f'{(lv.get("inputs") or {}).get("plate_z_source")})',
        lv.get('schema') == 'particle_load_view/v1' and (lv.get('inputs') or {}).get('box_source') == 'input_params'
        and (lv.get('inputs') or {}).get('plate_z_source') == 'mesh')
    pr = lv.get('pressure') or {}
    conv = SCALE / 1e6
    want = {}
    for r in rows:
        mag = math.sqrt(sum(x * x for x in r['fn']))
        comp = (r['id1'], r['id2']) in ((1, 2), (4, 5), (1, 11), (12, 13))
        if comp and r['area'] > 0 and r['delta'] > 0 and mag > 0:
            p = mag / r['area'] * conv
            for i in (r['id1'], r['id2']):
                want[i] = max(want.get(i, 0.0), p)
    got = ikeys(pr.get('max_MPa'))
    chk(f'W2 입자별 최대 압력 = 압축 접촉만 손 계산 (당김 1–10 · 2–3 · δ = 0 행 · 힘 0 행 제외 · 전 입자 맵 = 유효 6 자리) ({len(got)} 입자)',
        set(got) == set(want) and all(rel(got[i], want[i]) < 1e-6 for i in want), repr((got, want))[:400])
    chk(f'W3 셈 — 압축 4 · 당김 2 · 판정 불가 0 · 겹침 없음 / 면적 0 / 힘 0 = 2 ({pr.get("n_used")} · {pr.get("n_excluded_attractive")} · '
        f'{pr.get("n_excluded_unknown")} · {pr.get("n_excluded_no_overlap")})',
        pr.get('n_used') == 4 and pr.get('n_excluded_attractive') == 2 and pr.get('n_excluded_unknown') == 0
        and pr.get('n_excluded_no_overlap') == 2)
    # 옛 stress_max (aggregate_particle_metrics) — 바뀌지 않는다 (당김 포함 · 부호 없음)
    import pandas as pd
    cdf = pd.read_csv(os.path.join(d, 'contacts.csv'))
    atoms_by_id = {int(i): {'type': TYPE[i], 'radius': RAD[i], 'x': P[i][0], 'y': P[i][1], 'z': P[i][2]} for i in P}
    agg = V.aggregate_particle_metrics((dict(zip(cdf.columns, t)) for t in cdf.itertuples(index=False, name=None)),
                                       atoms_by_id, TM, scale=SCALE)
    legacy = {}
    for r in rows:
        mag = math.sqrt(sum(x * x for x in r['fn']))
        p = (mag / r['area'] * conv) if r['area'] > 0 else 0.0
        for i in (r['id1'], r['id2']):
            legacy[i] = max(legacy.get(i, 0.0), p)
    chk('W4 옛 stress_max = |Fn| / A 의 입자별 최대 (당김 포함 · 2 자리 반올림) — 이 묶음은 그 키를 바꾸지 않는다',
        {int(k): v for k, v in agg['stress_max'].items() if v} == {i: round(v, 2) for i, v in legacy.items() if round(v, 2)})
    n_hi = sum(1 for i, v in legacy.items() if v > want.get(i, 0.0) * (1 + 1e-12))
    chk(f'W5 당김 · δ = 0 행 때문에 옛 값이 더 큰 입자 수 = {n_hi} (1 · 2 · 3 · 4 · 5 · 10) ({pr.get("n_particles_legacy_higher")})',
        pr.get('n_particles_legacy_higher') == n_hi == 6)
    chk('W6 규칙 문구 — |Fn| / A · 압축만 · 당김 · δ ≤ 0 제외 · k/(2πR*) · 하중이 아니다 (WEB-06)',
        all(x in str(pr.get('rule')) for x in ('|Fn|', '압축', '당김', 'k/(2πR*)', '하중이 아니다', 'WEB-06')))

    am = lv.get('am') or {}
    fmax = ikeys(am.get('fn_max_uN'))
    fconv = 1e6 / SCALE
    want_f = {1: 0.02 * fconv, 2: 0.02 * fconv, 4: 0.01 * fconv, 5: 0.01 * fconv}
    chk(f'F1 최대 AM–AM 접촉 힘 (µN) = 압축 AM–AM 만 손 계산 — 2–3 당김 (0.5) · 4–5 δ = 0 행 (0.05) 은 뺀다 ({fmax})',
        set(fmax) == set(want_f) and all(rel(fmax[i], want_f[i]) < 1e-12 for i in want_f))
    chk(f'F2 AM 수 7 · 압축 AM–AM 접촉 없는 AM 3 (3 · 15 · 16) ({am.get("n_am")} · {am.get("n_am_without_am_contact")})',
        am.get('n_am') == 7 and am.get('n_am_without_am_contact') == 3)
    chk('F3 힘 규칙 문구 — |Fn| × 1e6 / scale (µN · calc_contact_force_distribution 환산) · 압축 AM–AM · 당김 제외',
        all(x in str(am.get('fn_rule')) for x in ('1e6 / scale', 'calc_contact_force_distribution', '압축', '당김')))

    # Love–Weber — 정본 함수 (같은 읽기 · 같은 판 · 같은 상자)
    import analyze_contacts as AC
    import dem_analysis_core as D
    atoms_raw, _ = AC.load_atoms_raw(os.path.join(d, 'atoms.csv'))
    contacts_raw, _ = AC.load_contacts_raw(os.path.join(d, 'contacts.csv'))
    ref = D.calc_love_weber_stress(atoms_raw, contacts_raw, TM, PLATE, box_x=BOX, box_y=BOX, plate_z_source='mesh', return_arrays=True)
    chk(f'L1 LW 상태 = 정본 ({am.get("lw_status")} · {ref.get("status")})', am.get('lw_status') == ref.get('status') == 'OK')
    if ref.get('status') == 'OK':
        vm = {int(i): float(v) for i, v in zip(ref['ids'], ref['arrays_vm'])}
        mean_all = float(ref['arrays_vm'].mean())
        am_ids = [i for i in P if 'AM' in TM[TYPE[i]]]
        got_vm, got_r = ikeys(am.get('lw_vm_MPa')), ikeys(am.get('lw_ratio'))
        chk('L2 AM 입자마다 σ_VM (MPa) = 정본 배열 × scale / 1e6 (비트 같음) · SE 는 싣지 않는다',
            set(got_vm) == set(am_ids) and all(got_vm[i] == vm[i] * SCALE / 1e6 for i in am_ids), repr(got_vm)[:300])
        chk('L3 비 = σ_VM,i / ⟨σ_VM⟩ (전 입자 · 접촉 없는 입자 포함 — stress_ratio_<상>_lw 와 같은 분모)',
            set(got_r) == set(am_ids) and all(rel(got_r[i], vm[i] / mean_all) < 1e-12 for i in am_ids))
        tr = am.get('lw_type_ratio') or {}
        chk(f'L4 상 비 = 정본 type_stress 비 ({tr})', all(rel(tr.get(k), v['ratio']) < 1e-12 for k, v in ref['type_stress'].items()))
        chk('L4b ⟨σ_VM⟩ (MPa) = 정본 배열 평균 × scale / 1e6', rel(am.get('lw_mean_all_MPa'), mean_all * SCALE / 1e6) < 1e-12)
    w = ikeys(am.get('wall'))
    chk(f'L5 벽 표지 (AM 만) — 15 바닥 · 16 판 ({w})', w == {15: 'floor', 16: 'plate'})
    wc = am.get('wall_counts') or {}
    chk(f'L6 벽 수 (전 입자) = 정본 벽 수 (바닥 {ref.get("wall", {}).get("n_floor")} · 판 {ref.get("wall", {}).get("n_plate")}) · 일치 표지',
        wc.get('n_floor') == ref.get('wall', {}).get('n_floor') and wc.get('n_plate') == ref.get('wall', {}).get('n_plate')
        and am.get('wall_counts_match_lw') is True, repr(wc))
    chk('L7 LW 규칙 문구 — calc_love_weber_stress · 벽 힘 없음 · stress_ratio · 전 입자 평균',
        all(x in str(am.get('lw_rule')) for x in ('calc_love_weber_stress', '벽', 'stress_ratio', '전 입자')))
    # 예산 초과 — LW 를 계산하지 않는다 (상태) · 압력 · 힘은 계산
    lv2 = fn_(d, TM, SCALE, row_budget=3)
    am2 = lv2.get('am') or {}
    chk(f'L8 행 수 > 예산 → LW = NOT_COMPUTED (예산) · 값 없음 · 압력 · 힘은 그대로 ({am2.get("lw_status")})',
        str(am2.get('lw_status', '')).startswith('NOT_COMPUTED') and '예산' in str(am2.get('lw_status')) and not am2.get('lw_vm_MPa')
        and ikeys((lv2.get('pressure') or {}).get('max_MPa')) == got and ikeys(am2.get('fn_max_uN')) == fmax)
    # 판 메시 없음 — 판 표지 없음 (바닥만) · LW 의 판 규칙과 같다
    d3 = os.path.join(tmp, 'synth_nomesh')
    write_bed(d3, P, rows, mesh=False)
    lv3 = fn_(d3, TM, SCALE)
    am3 = lv3.get('am') or {}
    chk(f'L9 mesh_info 없음 → plate_z 추정 · 판 표지 없음 · 바닥 표지만 ({(lv3.get("inputs") or {}).get("plate_z_source")} · {ikeys(am3.get("wall"))})',
        (lv3.get('inputs') or {}).get('plate_z_source') != 'mesh' and ikeys(am3.get('wall')) == {15: 'floor'})
    # 상자 없음 — 0.05 기본 (정본 _get_box_xy) · 표지
    d4 = os.path.join(tmp, 'synth_nobox')
    write_bed(d4, P, rows, box=False)
    lv4 = fn_(d4, TM, SCALE)
    chk(f'L10 input_params 없음 → 상자 = 0.05 기본 표지 ({(lv4.get("inputs") or {}).get("box_source")})',
        (lv4.get('inputs') or {}).get('box_source') == 'default_0.05')
    return lv


# ══════════════════════════════════════════════════════════════════════════════
#  [R] real14
# ══════════════════════════════════════════════════════════════════════════════
def section_real14(tmp):
    print('[R] real14 커밋 원자료 — WEB-06 점검 · LW 상 비 · 벽 표지')
    import numpy as np
    import pandas as pd
    import viewer3d_data as V
    from test_viewer_coordination import build_real14_case
    d = os.path.join(tmp, 'real14')
    os.makedirs(d)
    if not chk('R0 real14 덤프 → parse_liggghts (웹앱 파서)', build_real14_case(d)):
        return None
    fn_ = getattr(V, 'particle_load_view_for_case', None)
    if not callable(fn_):
        chk('R1 particle_load_view_for_case', False)
        return None
    lv = fn_(d, TM, SCALE)
    # WEB-06 점검 (docs/data/contact_pressure_check_20261007) — 주기 너머 (거리 > 1.5 (r1 + r2)) 를 뺀 행의 부호 = 그 스크립트의 셈
    cdf = pd.read_csv(os.path.join(d, 'contacts.csv'))
    adf = pd.read_csv(os.path.join(d, 'atoms.csv'))
    pos = {int(r.id): (r.x, r.y, r.z, r.radius) for r in adf.itertuples(index=False)}
    p1 = np.array([pos[int(i)][:3] for i in cdf['id1']])
    p2 = np.array([pos[int(i)][:3] for i in cdf['id2']])
    r1 = np.array([pos[int(i)][3] for i in cdf['id1']])
    r2 = np.array([pos[int(i)][3] for i in cdf['id2']])
    fn = cdf[['fn_x', 'fn_y', 'fn_z']].to_numpy(float)
    s = V.contact_force_sign(fn, p1, p2, r1, r2, box_xy=(0.05, 0.05), cp=cdf[['cp_x', 'cp_y', 'cp_z']].to_numpy(float))
    #  점검 스크립트의 "주기 너머" = 접촉 덤프 pos1 · pos2 (c_cpl[1–6]) 의 거리 > 1.5 (r1 + r2) — 덤프 위치는 고스트 영상 좌표일 수 있어
    #  (atoms.csv 와 최대 한 상자 차이) 같은 집합을 그 열로 고른다 · 부호는 최소영상이라 어느 위치로 재도 같다
    dp1 = cdf[['p1_x', 'p1_y', 'p1_z']].to_numpy(float)
    dp2 = cdf[['p2_x', 'p2_y', 'p2_z']].to_numpy(float)
    raw_d = np.linalg.norm(dp1 - dp2, axis=1)
    near = raw_d <= 1.5 * (r1 + r2)
    s_dump = V.contact_force_sign(fn, dp1, dp2, r1, r2, box_xy=(0.05, 0.05))
    chk(f'R1a 부호는 atoms.csv 위치 · 덤프 위치 (고스트 영상) 어느 쪽으로 재도 같다 (최소영상 · 다른 행 {int((s != s_dump).sum())})',
        int((s != s_dump).sum()) == 0)
    ok = (cdf['contact_area'].to_numpy(float) > 0) & (np.linalg.norm(fn, axis=1) > 0)
    n_c, n_a = int(((s > 0) & near & ok).sum()), int(((s < 0) & near & ok).sum())
    chk(f'R1 부호 (주기 너머 뺀 행) = WEB-06 점검 셈 — 압축 95,277 · 당김 6,757 ({n_c:,} · {n_a:,})', n_c == 95277 and n_a == 6757)
    sg = lv.get('sign') or {}
    chk(f'R2 최소영상으로 주기 너머도 판정 — 판정 불가 0 ({sg})', sg.get('n_unknown') == 0 and sg.get('n_compressive', 0) > 95277)
    pr = lv.get('pressure') or {}
    mx = ikeys(pr.get('max_MPa'))
    big = sum(1 for v in mx.values() if v >= 1e4)
    chk(f'R3 압축만 입자별 최대 ≥ 1e4 MPa = 0 개 (옛 계산 104 개 = 전부 당김 · 점검 §4) ({big} · 최대 {max(mx.values()) if mx else None:.1f} MPa)',
        bool(mx) and big == 0)
    am = lv.get('am') or {}
    tr = am.get('lw_type_ratio') or {}
    chk(f'R4 LW 상 비 = 2.737 (AM_P) · 2.341 (AM_S) · 0.981 (SE) — 정본 · full_metrics stress_ratio_<상>_lw ({tr})',
        am.get('lw_status') == 'OK' and abs(tr.get('AM_P', 0) - 2.736942775110707) < 1e-9
        and abs(tr.get('AM_S', 0) - 2.340938047338784) < 1e-9 and abs(tr.get('SE', 0) - 0.9809008023320659) < 1e-9)
    r = ikeys(am.get('lw_ratio'))
    ty = {int(i): TM[int(t)] for i, t in zip(adf['id'], adf['type'])}
    for ph, want in (('AM_P', 2.736942775110707), ('AM_S', 2.340938047338784)):
        v = [x for i, x in r.items() if ty[i] == ph]
        chk(f'R5 {ph} 입자 {len(v)} 개의 비 평균 = 상 비 {want:.4f} (뷰어 값의 평균 = 보고값)', bool(v) and rel(sum(v) / len(v), want) < 1e-12)
    w = ikeys(am.get('wall'))
    cnt = {(ph, k): sum(1 for i, x in w.items() if ty[i] == ph and k in x) for ph in ('AM_P', 'AM_S') for k in ('floor', 'plate')}
    chk(f'R6 벽 표지 = 정본 벽 규칙 (AM_P 바닥 7 · 판 8 · AM_S 46 · 38) ({cnt})',
        cnt == {('AM_P', 'floor'): 7, ('AM_P', 'plate'): 8, ('AM_S', 'floor'): 46, ('AM_S', 'plate'): 38}
        and am.get('wall_counts_match_lw') is True)
    fm = ikeys(am.get('fn_max_uN'))
    chk(f'R7 최대 AM–AM 힘 — AM 457 개 중 {len(fm)} 개 (압축 AM–AM 접촉 있는 AM) · 최대 {max(fm.values()) if fm else 0:.0f} µN',
        0 < len(fm) <= 457 and am.get('n_am') == 457)
    return lv


# ══════════════════════════════════════════════════════════════════════════════
#  [J] 뷰어 (node)
# ══════════════════════════════════════════════════════════════════════════════
JS_NAMES = ('netCurrentFmtJ', 'netCurrentT', 'netCurrentTicks', 'jeEscH', 'jetColor', 'coolwarmColor', 'loadViewAmMetric', 'amOnlyRange',
            'amOnlyLegendHtml', 'amOnlyMissingHtml', 'amOnlyColorbarSpec', 'pressureViewTip', 'pressureViewInfo', 'pressureLegendHtml')


def section_js(lv):
    print('[J] 뷰어 — 드롭다운 · AM 만 보기 · 최대 접촉 압력 범례 (node)')
    js = open(VIEWER_JS, encoding='utf-8').read()
    try:
        bc = js_fn(js, 'buildControls')
    except (ValueError, AssertionError):
        bc = ''
    sels = re.findall(r'<select id="view-mode".*?</select>', bc, re.S)
    mpm_sel, dem_sel = (sels + ['', ''])[:2]
    m_st = re.search(r'<option value="stress">([^<]*)</option>', dem_sel)
    m_sb = re.search(r'<option value="stress_brittle">([^<]*)</option>', dem_sel)
    chk(f'J1 이름 정정 — "Stress Concentration" → "Max contact pressure (|Fn|/A)" · 겹침 보기도 ({m_st.group(1) if m_st else None} · '
        f'{m_sb.group(1) if m_sb else None})',
        m_st is not None and 'Max contact pressure' in m_st.group(1) and '|Fn|/A' in m_st.group(1)
        and m_sb is not None and 'Contact pressure' in m_sb.group(1) and 'Stress Concentration' not in dem_sel)
    m_am = re.search(r'<option value="am_only">([^<]*)</option>', dem_sel)
    chk(f'J2 DEM 드롭다운에 am_only (AM 만 · LW · AM–AM 힘) · MPM 드롭다운엔 없음 ({m_am.group(1) if m_am else None})',
        m_am is not None and 'AM 만' in m_am.group(1) and 'am_only' not in mpm_sel)
    try:
        avm = js_fn(js, 'applyViewMode')
    except (ValueError, AssertionError):
        avm = ''
    chk("J3 applyViewMode — 'am_only' → applyAmOnlyView · 머리에서 _amOnlyTeardown (SE 보이기 되돌림)",
        re.search(r"mode === 'am_only'\)\s*\{\s*applyAmOnlyView\(state\);\s*return;", avm) is not None
        and '_amOnlyTeardown(state);' in avm[:7000])
    try:
        ao = js_fn(js, 'applyAmOnlyView')
        td = js_fn(js, '_amOnlyTeardown')
    except (ValueError, AssertionError):
        ao = td = ''
    chk('J4 AM 만 보기 = SE 숨김 (meshes.SE.visible = false) · 되돌림은 SE 체크박스대로',
        re.search(r'SE\.visible\s*=\s*false', ao) is not None and 'data-layer="SE"' in td)
    chk("J5 'stress' · 'stress_brittle' 둘 다 pressureViewInfo(aux) 로 (같은 자료 · 같은 규칙)",
        len(re.findall(r'pressureViewInfo\(aux\)', avm)) >= 2)
    parts, miss = [], []
    for n in JS_NAMES:
        try:
            parts.append(js_fn(js, n))
        except (ValueError, AssertionError):
            miss.append(n)
    if not chk(f'J6 viewer3d.js 에서 함수를 잘라 냈다 (없음 {miss})', not miss):
        return
    if not chk('J7 자료 (합성 침대 load_view) 가 있다', bool(lv)):
        return
    lv = copy.deepcopy(lv)
    script = '\n'.join(parts) + '\n' + r"""
const LV = __LV__;
const out = {};
out.mLw = loadViewAmMetric(LV, 'lw');
out.mFn = loadViewAmMetric(LV, 'fn');
const bad = JSON.parse(JSON.stringify(LV)); bad.am.lw_status = 'NOT_COMPUTED (행 수 200 > 예산 3)'; bad.am.lw_ratio = {};
out.mBad = loadViewAmMetric(bad, 'lw');
const v100 = Array.from({length: 100}, (_, i) => i + 1);
out.rP = amOnlyRange(v100, 'p5p95');
out.rM = amOnlyRange(v100, 'minmax');
out.rNone = amOnlyRange([0, -1], 'p5p95');
const ui = {metric: 'lw', range: 'p5p95', wall: true};
const st = {n: 7, nColored: 4, nWall: 2, nNoValue: 1, lo: -0.5, hi: 0.5};
out.leg = amOnlyLegendHtml(LV, ui, st);
out.legFn = amOnlyLegendHtml(LV, {metric: 'fn', range: 'minmax', wall: false}, st);
out.legBad = amOnlyLegendHtml(bad, ui, st);
out.miss = amOnlyMissingHtml();
out.spec = amOnlyColorbarSpec(LV, ui, -0.5, 0.5);
out.specFn = amOnlyColorbarSpec(LV, {metric: 'fn', range: 'p5p95', wall: true}, 1, 2);
out.pNew = pressureViewInfo({stress_max: {1: 5}, load_view: LV});
out.pOld = pressureViewInfo({stress_max: {1: 5, 2: 1e6}});
out.legNew = pressureLegendHtml(out.pNew, 22.5, 447.8, 666.0);
out.legOld = pressureLegendHtml(out.pOld, 22.5, 447.8, 666.0);
console.log(JSON.stringify(out));
""".replace('__LV__', json.dumps(lv, ensure_ascii=False))
    res = run_node(script)
    if not chk('J8 node 실행', res is not None):
        return
    mlw, mfn = res['mLw'] or {}, res['mFn'] or {}
    chk(f'J9 양 (a) LW — 맵 = load_view.am.lw_ratio · 이름 σ_VM · 비 (단위 없음) · log ({mlw.get("label")} · {mlw.get("unit")!r})',
        mlw.get('ok') is True and ikeys(mlw.get('map')) == ikeys(lv['am']['lw_ratio']) and 'σ_VM' in str(mlw.get('label'))
        and mlw.get('scale') == 'log')
    chk(f'J10 양 (b) 최대 AM–AM 힘 — 맵 = fn_max_uN · 단위 µN · log ({mfn.get("label")} · {mfn.get("unit")})',
        mfn.get('ok') is True and ikeys(mfn.get('map')) == ikeys(lv['am']['fn_max_uN']) and mfn.get('unit') == 'µN'
        and 'AM–AM' in str(mfn.get('label')))
    chk(f'J11 LW 상태가 OK 가 아니면 ok false + 그 상태 (0 으로 칠하지 않는다) ({res["mBad"]})',
        (res['mBad'] or {}).get('ok') is False and '예산' in str((res['mBad'] or {}).get('reason')))
    chk(f'J12 범위 = AM 값만 · p5–p95 (가장 가까운 순위) = log10 5 · 95 / 최소–최대 = 0 · 2 ({res["rP"]} · {res["rM"]}) · 양수 없음 = null',
        res['rP'] and abs(res['rP'][0] - math.log10(5)) < 1e-12 and abs(res['rP'][1] - math.log10(95)) < 1e-12
        and res['rM'] and abs(res['rM'][0]) < 1e-12 and abs(res['rM'][1] - 2) < 1e-12 and res['rNone'] is None)
    leg = res['leg']
    chk('J13 범례 (LW) — AM 만 · SE 숨김 · Love–Weber σ_VM · ⟨σ_VM⟩ (MPa) · stress_ratio 와 같은 정의 · 색 범위 = AM 만 · 벽 접촉 회색 + 수 · 벽 힘 없음',
        all(x in leg for x in ('AM 만', 'SE 숨김', 'Love–Weber', 'σ_VM', 'MPa', 'stress_ratio', '색 범위', 'AM 만의', '벽 접촉', '벽 힘'))
        and '2 개' in leg, leg[:600])
    chk('J14 범례 조작 — 양 고르기 (amonly-metric: lw · fn) · 범위 (amonly-range: p5p95 · minmax) · 벽 표지 (amonly-wall) · 컬러바 ⬇ (amonly-cbar)',
        'id="amonly-metric"' in leg and 'value="lw"' in leg and 'value="fn"' in leg and 'id="amonly-range"' in leg
        and 'value="p5p95"' in leg and 'value="minmax"' in leg and 'id="amonly-wall"' in leg and 'id="amonly-cbar"' in leg)
    lf = res['legFn']
    chk('J15 범례 (힘) — 최대 AM–AM 접촉 법선력 · µN · 압축 접촉만 (당김 제외) · 모델 단위 (덱 축척 환산 · 조성 비교 절대값 금지)',
        all(x in lf for x in ('AM–AM', 'µN', '압축', '당김', '덱 축척')), lf[:600])
    chk('J16 LW 미계산 → 사유 (예산) · 칠하지 않는다는 문구', '예산' in res['legBad'] and '칠하지 않' in res['legBad'], res['legBad'][:400])
    ms = res['miss']
    chk('J17 자료 없음 안내 — 3D 데이터에 load_view 없음 · 봉인 파일 app.py · 194 발사 뒤 패치 경로',
        all(x in ms for x in ('load_view', 'app.py', '194', 'webapp_load_view_deferred_20261007.patch')), ms[:400])
    sp, sf = res['spec'] or {}, res['specFn'] or {}
    chk('J18 컬러바 (LW) — jet · 영문 제목 (AM only · Love–Weber · σ_VM / ⟨σ_VM⟩ all particles) · 부제 (AM-only range · wall)',
        sp.get('map') == 'jet' and all(x in sp.get('title', '') for x in ('AM only', 'Love–Weber', 'σ_VM')) and 'all particles' in sp.get('title', '')
        and 'AM particles only' in sp.get('sub', '') and len(sp.get('ticks') or []) >= 2, repr(sp)[:400])
    chk('J19 컬러바 (힘) — 제목 max AM–AM contact normal force (µN) · 부제 compressive only · model units',
        all(x in sf.get('title', '') for x in ('AM–AM', 'normal force', 'µN')) and 'compressive' in sf.get('sub', '')
        and 'model' in sf.get('sub', ''), repr(sf)[:400])
    pn, po = res['pNew'] or {}, res['pOld'] or {}
    chk(f'J20 최대 접촉 압력 자료 — load_view 있으면 압축만 (pressure.max_MPa) · 없으면 옛 stress_max (rule legacy) ({pn.get("rule")} · {po.get("rule")})',
        pn.get('rule') == 'compressive' and ikeys(pn.get('map')) == ikeys(lv['pressure']['max_MPa'])
        and po.get('rule') == 'legacy' and ikeys(po.get('map')) == {1: 5, 2: 1e6})
    ln, lo_ = res['legNew'], res['legOld']
    chk('J21 범례 제목 = Max contact pressure (|Fn|/A) · 툴팁 (title) 한정어 = k/(2πR*) · 쌍 유형 표지 · 하중이 아니다 · AM 만 보기 안내',
        'Max contact pressure' in ln and '|Fn|/A' in ln and re.search(r'title="[^"]*k/\(2πR\*\)[^"]*하중이 아니다', ln) is not None
        and 'AM 만' in ln, ln[:600])
    chk('J22 압축만 범례 — 당김 접촉 · 판정 불가 수를 적는다 (범위에서 뺐다)',
        '당김' in ln and '뺐' in ln and str(lv['pressure']['n_excluded_attractive']) in ln, ln[:600])
    chk('J23 옛 계산 범례 — ⚠ 당김 (접착) 접촉 포함 · 옛 계산 · 10⁴ MPa 넘는 값 = 당김 · 발사 뒤 패치 안내',
        '⚠' in lo_ and '당김' in lo_ and '옛 계산' in lo_ and '10⁴' in lo_ and 'app.py' in lo_, lo_[:600])
    m_tab = re.search(r'<button class="zh-tab" data-tab="stress"[^>]*>([^<]*)</button>', js)
    chk(f'J24 Z-profile 창의 탭 이름도 Max contact pressure · 툴팁 = 당김 포함 (그 z 그림 · CSV 는 옛 계산) · 하중 아님 '
        f'({m_tab.group(1) if m_tab else None})',
        m_tab is not None and 'Max contact pressure' in m_tab.group(1) and 'Stress hotspots' not in js
        and re.search(r'data-tab="stress"[^>]*title="[^"]*당김[^"]*하중이 아니다', js) is not None)


def section_zprofile_title(tmp):
    print('[Z] Z-profile 그림 제목 — 이름 정정 (값 = 옛 계산 그대로 · 당김 포함 표기)')
    P, rows = synth_bed()
    d = os.path.join(tmp, 'z_case')
    write_bed(d, P, rows)
    import plot_stress_z_distribution as Z
    prof = Z.compute_stress_zprofile(d, bins=5)
    fig = Z.render_stress_figure(prof)
    title = fig._suptitle.get_text() if fig._suptitle is not None else ''
    import matplotlib.pyplot as plt
    plt.close(fig)
    chk(f'Z1 PNG 제목 = Max contact pressure |Fn|/A z-profile · incl. attractive · not a load ({title[:80]!r})',
        'Max contact pressure' in title and 'attractive' in title and 'not a load' in title and 'Stress-hotspot' not in title)


# ══════════════════════════════════════════════════════════════════════════════
#  [P] 발사 뒤 패치 — 패치한 app 의 /3d-data
# ══════════════════════════════════════════════════════════════════════════════
DRIVER = r'''
import json, os, shutil, sys
tree, work, case_src = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, os.path.join(tree, 'webapp'))
sys.path.insert(0, os.path.join(tree, 'scripts'))
up, rs, ar = (os.path.join(work, k) for k in ('uploads', 'results', 'archive'))
for p in (up, rs, ar):
    os.makedirs(p, exist_ok=True)
os.environ['WEBAPP_UPLOAD_FOLDER'], os.environ['WEBAPP_RESULTS_FOLDER'], os.environ['WEBAPP_ARCHIVE_FOLDER'] = up, rs, ar
os.environ['WEBAPP_MPM_LAB_FOLDER'] = os.path.join(work, 'mpm_lab')
import app as A
assert os.path.realpath(A.__file__).startswith(os.path.realpath(tree)), A.__file__
A.app.config['UPLOAD_FOLDER'], A.app.config['RESULTS_FOLDER'], A.app.config['ARCHIVE_FOLDER'] = up, rs, ar
c = A.app.test_client()
meta = {'name': 'lv_synth', 'type_map': '1:AM_P,2:AM_S,3:SE', 'scale': 1000, 'status': 'done', 'mode': 'standard'}
cid = '261007_000001_lvsynth'
os.makedirs(os.path.join(up, cid))
json.dump(meta, open(os.path.join(up, cid, 'meta.json'), 'w'))
shutil.copytree(case_src, os.path.join(rs, cid))
out = {}
def aux_of(url):
    j = c.get(url).get_json(silent=True) or {}
    return j.get('aux') or {}
cache = os.path.join(rs, cid, 'viewer_aux.json')
out['live1'] = aux_of(f'/results/{cid}/3d-data').get('load_view')
blob = json.load(open(cache)) if os.path.exists(cache) else {}
out['cache_schema'] = blob.get('_schema')
out['cache_has_lv'] = 'load_view' in blob
out['live2'] = aux_of(f'/results/{cid}/3d-data').get('load_view')
blob['_schema'] = 12
blob.pop('load_view', None)
json.dump(blob, open(cache, 'w'))
out['live_old'] = aux_of(f'/results/{cid}/3d-data').get('load_view')
af = os.path.join(ar, 'lv_case')
shutil.copytree(case_src, af)
json.dump(meta, open(os.path.join(af, 'meta.json'), 'w'))
out['arch1'] = aux_of('/archive/results/lv_case/3d-data').get('load_view')
out['arch2'] = aux_of('/archive/results/lv_case/3d-data').get('load_view')
print('@@JSON@@' + json.dumps(out))
'''


def _mirror_tree(dst):
    """ROOT 의 최상위 항목을 dst 에 심볼릭 링크 — webapp/ 만 진짜 폴더 (그 안도 링크 · app.py · test_viewer_coordination.py 는 사본)."""
    os.makedirs(dst)
    for n in os.listdir(ROOT):
        if n in ('webapp', '.git'):
            continue
        os.symlink(os.path.join(ROOT, n), os.path.join(dst, n))
    w = os.path.join(dst, 'webapp')
    os.makedirs(w)
    for n in os.listdir(HERE):
        src = os.path.join(HERE, n)
        if n in ('app.py', 'test_viewer_coordination.py'):
            shutil.copy2(src, os.path.join(w, n))
        elif n != '__pycache__':
            os.symlink(src, os.path.join(w, n))


def section_patch(tmp):
    print('[P] 발사 뒤 패치 (webapp/app.py = 194 봉인 파일) — 적용 · 패치한 app 의 /3d-data')
    if not chk(f'P0 패치 파일 {os.path.relpath(PATCH, ROOT)}', os.path.exists(PATCH)):
        return
    ptxt = open(PATCH, encoding='utf-8').read()
    files = sorted(set(re.findall(r'^diff --git a/(\S+) b/', ptxt, re.M)))
    chk(f'P1 패치가 바꾸는 파일 = app.py · test_viewer_coordination.py 뿐 ({files})',
        files == ['webapp/app.py', 'webapp/test_viewer_coordination.py'])
    applied = 'particle_load_view_for_case' in open(os.path.join(HERE, 'app.py'), encoding='utf-8').read()
    if applied:
        tree = ROOT
        print('      (패치가 이미 적용된 트리 — 진짜 app.py 를 본다)')
    else:
        tree = os.path.join(tmp, 'tree')
        _mirror_tree(tree)
        r = subprocess.run(['git', 'apply', '--check', PATCH], cwd=tree, capture_output=True, text=True)
        if not chk(f'P2 패치가 지금 app.py 에 깨끗이 맞는다 (git apply --check · rc {r.returncode})', r.returncode == 0, r.stderr[-400:]):
            return
        r = subprocess.run(['git', 'apply', PATCH], cwd=tree, capture_output=True, text=True)
        chk('P3 임시 사본에 적용', r.returncode == 0, r.stderr[-400:])
    src = open(os.path.join(tree, 'webapp', 'app.py'), encoding='utf-8').read()
    n13 = len(re.findall(r"_schema'\)\s*==\s*13\b", src))
    w13 = len(re.findall(r"\['_schema'\]\s*=\s*13\b", src))
    n12 = len(re.findall(r"_schema'\)\s*==\s*12\b", src)) + len(re.findall(r"\['_schema'\]\s*=\s*12\b", src))
    chk(f'P4 패치한 app — 두 경로 캐시 스키마 13 읽기 · 쓰기 · 12 는 남지 않는다 ({n13} · {w13} · {n12})', n13 == 2 and w13 == 2 and n12 == 0)
    P, rows = synth_bed()
    case_src = os.path.join(tmp, 'p_case')
    write_bed(case_src, P, rows)
    drv = os.path.join(tmp, 'driver.py')
    with open(drv, 'w', encoding='utf-8') as f:
        f.write(DRIVER)
    work = os.path.join(tmp, 'p_work')
    env = dict(os.environ)
    env.pop('PYTHONPATH', None)
    r = subprocess.run([sys.executable, drv, tree, work, case_src], capture_output=True, text=True, timeout=600, env=env, cwd=tmp)
    m = re.search(r'@@JSON@@(.*)$', r.stdout, re.M)
    if not chk(f'P5 패치한 app 실행 (rc {r.returncode})', r.returncode == 0 and m is not None, (r.stderr or r.stdout)[-800:]):
        return
    out = json.loads(m.group(1))
    l1 = out.get('live1') or {}
    chk(f'P6 live /3d-data → aux.load_view (스키마 {l1.get("schema")} · 압축만 최대 압력 · AM LW · 힘 · 벽)',
        l1.get('schema') == 'particle_load_view/v1' and bool((l1.get('pressure') or {}).get('max_MPa'))
        and (l1.get('am') or {}).get('lw_status') == 'OK' and bool((l1.get('am') or {}).get('fn_max_uN')))
    chk(f'P7 캐시 = 스키마 13 · load_view 를 담는다 ({out.get("cache_schema")} · {out.get("cache_has_lv")})',
        out.get('cache_schema') == 13 and out.get('cache_has_lv') is True)
    chk('P8 두 번째 요청 (캐시 HIT) 도 같은 load_view (live)', out.get('live2') == out.get('live1') and bool(out.get('live1')))
    chk('P9 옛 캐시 (스키마 12 · load_view 없음) → 다시 계산 · load_view 산다', out.get('live_old') == out.get('live1'))
    a1, a2 = out.get('arch1') or {}, out.get('arch2') or {}
    chk('P10 archive 경로도 load_view (첫 요청 = 계산 · 캐시 HIT = 같은 값 — archive 의 키 목록 복원에 더했다)',
        a1.get('schema') == 'particle_load_view/v1' and a2 == a1)


def section_registration():
    print('[X] check_all 배선')
    s = open(CHECK_ALL, encoding='utf-8').read()
    chk('X1 scripts/check_all.sh 가 이 시험을 돈다', 'webapp/test_viewer_load_view.py' in s)


def main():
    tmp = tempfile.mkdtemp(prefix='viewer_load_')
    try:
        for k, v in (('WEBAPP_RESULTS_FOLDER', 'results'), ('WEBAPP_UPLOAD_FOLDER', 'uploads'),
                     ('WEBAPP_ARCHIVE_FOLDER', 'archive'), ('WEBAPP_MPM_LAB_FOLDER', 'mpm_lab')):
            os.environ[k] = os.path.join(tmp, v)
            os.makedirs(os.environ[k], exist_ok=True)
        lv = None
        for fn in (section_sign, ):
            try:
                fn()
            except Exception as e:                               # noqa: BLE001 — 옛 코드에서도 나머지 절을 돈다
                chk(f'{fn.__name__} 실행', False, f'{type(e).__name__}: {e}')
        try:
            lv = section_synth(tmp)
        except Exception as e:                                   # noqa: BLE001
            chk('section_synth 실행', False, f'{type(e).__name__}: {e}')
        try:
            section_real14(tmp)
        except Exception as e:                                   # noqa: BLE001
            chk('section_real14 실행', False, f'{type(e).__name__}: {e}')
        try:
            section_js(lv)
        except Exception as e:                                   # noqa: BLE001
            chk('section_js 실행', False, f'{type(e).__name__}: {e}')
        try:
            section_zprofile_title(tmp)
        except Exception as e:                                   # noqa: BLE001
            chk('section_zprofile_title 실행', False, f'{type(e).__name__}: {e}')
        try:
            section_patch(tmp)
        except Exception as e:                                   # noqa: BLE001
            chk('section_patch 실행', False, f'{type(e).__name__}: {e}')
        section_registration()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print()
    print(f'{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        print('FAIL — ' + ' | '.join(_fail))
        return 1
    print('ALL PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
