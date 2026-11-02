#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEM 3D 뷰어 — 입자 응력 σ_VM ÷ P_ref · 고정 색 범위 · SE 만 보기 (1저자 11-02 비준).

  계기: View Mode "AM 만 — 입자 응력 (LW)" 는 σ_VM / ⟨σ_VM⟩ (그 침대 전 입자 평균) 을 그 침대만의 색 범위 (p5–p95 · 최소–최대 · log) 로
    칠한다 → 침대마다 늘 파랑 → 빨강을 다 써서 침대끼리 색으로 비교할 수 없다 (1저자 "D3 도 파란 게 많다" = 침대별 범위의 인공물 ·
    D3 AM σ_VM 55–1050 MPa (19×) ↔ D1 8.9–804 MPa (90×)).  50kg 침대는 이완 뒤 판 압력도 다르다 (로그 끝 정규 thermo 줄
    D1 156.15118 · D2 279.79158 · D3 291.3744 MPa).
  더한 것 (기존 양 · 기본값 · 색은 그대로 — 저장된 선택이 없으면 오늘과 같은 그림):
    ① 양 σ_VM ÷ P_ref — P_ref = 그 침대 그 프레임의 ⟨σzz⟩ 상자 평균 (압축 양수) = −Σ_p V_p σ_p,zz / (box_x · box_y · plate_z) ·
       V_p σ_p = calc_love_weber_stress 텐서 × 4/3 π r³ = Σ_접촉 branch ⊗ 힘 (입자 부피 선택과 무관) — 케이스 폴더에 로그 판 압력이
       없어서 같은 접촉 자료로 낸다 · 벽 (바닥 · 판) 접촉은 덤프에 없어 그 항이 빠진다 (판 압력과 몇 % 다르다 — 50kg 끝 상태 실측
       D1 · D2 · D3 = 0.980 · 0.970 · 0.968 배 · D1 묶음은 리포 밖이라 이 시험은 D2 · D3 만 다시 잰다).
    ② 색 범위 "고정 (모든 케이스 공통)" — lo · hi (기본 0 … 3 · 선형) · 양마다 localStorage (모든 접근 try/catch) — 케이스를 바꿔도 같은 눈금.
    ③ View Mode "SE 만 — 입자 응력 (LW)" — 같은 양 · 같은 고정 범위 · AM 숨김 · 벽 접촉 SE 회색 · SE 값 = load_view.se (id 구간 + 유효 4 자리).
    ④ /3d-data 에 load_view 싣기 = 발사 뒤 패치 docs/reviews/webapp_load_view_deferred_20261007.patch 적용 (194 발사 10-30 끝) + 캐시 스키마 14 → 15.

  [A] P_ref — 합성 기둥 침대 (손 계산 −Σ (z_id2 − z_id1) F_z / V_상자 · 정본 텐서 Σ V σzz · 상태: mesh 없음 · 예산 · 인장 침대).
  [B] SE 값 — id 구간 (오름차순 연속 · 틈) · 유효 4 자리 = 정본 배열 · 벽 표지 (LW 규칙) · ⟨σ_VM⟩ · 기존 키 그대로 (새 묶음 둘만 더함).
  [R] 50kg D2 · D3 끝 세트 (리포 tgz · 로그 끝 정규 thermo 줄) — ⟨σzz⟩ / 판 압력 (±5 % 안 = 출하 관문 · 기록값) · AM σ_VM ÷ P_ref
      중앙값 · 평균 (벽 제외) · SE 값 수 = SE 수 · ★ 접촉 압력 요약 (AM–SE · AM–AM · 1저자 쪽 도구 D2 평균 ≈ 369.6 · 중앙 ≈ 385.7 MPa) ·
      보낸 행의 p_MPa = 압축 행만 (R5–R7).
  [JP] ★ 접촉마다 압력 (같은 묶음) — p_MPa = |Fn| / A · 양 contact_p · contact_se_p · 고정 0 … 800 (선형) · 진짜 cap 그리기 (THREE 흉내) · 힘 양 그대로 ·
      고정 범위 밖 수 (AM–AM 압력 ≈ 4000 MPa 는 기본 0 … 800 에서 다 잘린다 — 화면이 그 수를 적는다 · JP18 · JP19).
  [J] 뷰어 (node) — 드롭다운 se_only · applyViewMode 분기 · 걷기 · 양 lw_p (= lw_vm_MPa / P_ref) · 고정 범위 (선형 · 0 … 3 · 저장 · 깨진 저장 ·
      막힌 저장 · 없는 저장) · 기본 그림 = 옛 알고리즘 색 그대로 · 고정 색 = 선형 jet · SE 만 (AM 숨김 · SE 색 · 벽 회색 · 값 0 · log) ·
      범례 (P_ref 정의 · MPa) · 컬러바 (선형 눈금 0 · 1 · 2 · 3 · 기본 컬러바 글 그대로) · 조작 배선 (범위 · lo · hi → 저장 · 다시 그림).
  [P] webapp/app.py — 패치 적용 · 두 경로 캐시 스키마 15 (12 · 13 · 14 안 남음) · /3d-data aux.load_view 에 p_ref · se (live · HIT · archive ·
      옛 스키마 14 캐시 → 다시 계산).
  [X] check_all 배선.

  python3 webapp/test_viewer_lw_pnorm.py      # 종료코드 0 = PASS
"""
import copy
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = os.path.join(ROOT, 'scripts')
VIEWER_JS = os.path.join(HERE, 'static', 'js', 'viewer3d.js')
APP = os.path.join(HERE, 'app.py')
CHECK_ALL = os.path.join(SCRIPTS, 'check_all.sh')
sys.path.insert(0, HERE)
sys.path.insert(0, SCRIPTS)
from test_closed_param_labels import js_const, js_fn, run_node   # noqa: E402  (렌더된 JS 를 잘라 node 로 — 같은 도구)

_ok, _fail = 0, []
TM = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
SCALE = 1000.0
BOX, PLATE, DL = 0.05, 0.0296, 1e-5


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
    if not (math.isfinite(a) and math.isfinite(b)):
        return math.inf
    return abs(a - b) / max(abs(a), abs(b), 1e-300)


def ikeys(d):
    return {int(k): v for k, v in (d or {}).items()}


def expand_runs(runs):
    """[[시작, 개수], …] → id 목록 (이 시험의 독립 펼치기)."""
    out = []
    for a, c in runs or []:
        out.extend(range(int(a), int(a) + int(c)))
    return out


# ══════════════════════════════════════════════════════════════════════════════
#  합성 기둥 침대 (sim 단위 · scale 1000 → µm) — 상자 0.05 · 판 0.0296 (mesh) · 접촉은 모두 기하가 맞다 (접촉점이 두 입자 안)
#    1 AM_P (r 0.006 · 바닥) → 2 AM_S (r 0.002) → SE 10 … 23 (r 0.0005 · 23 = 판에 닿음) = 세로 압축 기둥 (|F| 0.01) ·
#    2–3 옆 (x) 압축 · 4–5 x 주기 경계 너머 x–z 45° 압축 · 31 · 32 바닥 SE 옆 압축 · 33–34 세로 당김 · 30 접촉 없음 (σ_VM = 0) ·
#    덤프 행 (10, 2) = SE 먼저 (순서와 무관해야 한다)
# ══════════════════════════════════════════════════════════════════════════════
RAD = {1: 0.006, 2: 0.002, 3: 0.002, 4: 0.002, 5: 0.002}
TYPE = {1: 1, 2: 2, 3: 2, 4: 2, 5: 2}
for _i in list(range(10, 24)) + [30, 31, 32, 33, 34]:
    RAD[_i], TYPE[_i] = 0.0005, 3
SE_IDS = sorted(i for i in TYPE if TYPE[i] == 3)
OLD_TOP_KEYS = {'schema', 'status', 'inputs', 'sign', 'pressure', 'am'}
OLD_AM_KEYS = {'n_am', 'n_am_by_type', 'fn_max_uN', 'fn_rule', 'n_am_without_am_contact', 'contacts', 'contacts_se', 'wall', 'wall_rule',
               'wall_counts', 'lw_rule', 'lw_vm_MPa', 'lw_ratio', 'lw_mean_all_MPa', 'lw_type_ratio', 'wall_counts_match_lw',
               'lw_definition', 'lw_contract', 'lw_quantity', 'lw_status'}


def _mi(d):
    d = list(d)
    for ax in (0, 1):
        d[ax] -= BOX * round(d[ax] / BOX)
    return d


def column_bed():
    P = {}
    P[1] = [0.020, 0.020, 0.0059]                                             # 바닥 (z − r < 0)
    P[2] = [0.020, 0.020, P[1][2] + RAD[1] + RAD[2] - DL]
    P[3] = [P[2][0] + RAD[2] + RAD[3] - DL, 0.020, P[2][2]]                   # 2–3 옆 (x)
    P[4] = [0.0485, 0.035, 0.0100]
    s2 = (RAD[4] + RAD[5] - DL) / math.sqrt(2.0)
    P[5] = [P[4][0] + s2 - BOX, 0.035, P[4][2] + s2]                          # 4–5 x 주기 너머 · x–z 45°
    z = P[2][2] + RAD[2] + 0.0005 - DL
    for i in range(10, 24):                                                    # SE 기둥 — 23 = 판 (z + r > 0.0296)
        P[i] = [0.020, 0.020, z]
        z += 0.001 - DL
    P[30] = [0.040, 0.040, 0.015]                                             # 접촉 없음
    P[31] = [0.030, 0.005, 0.0004]                                            # 바닥 SE
    P[32] = [0.030, 0.005 + 0.001 - DL, 0.0004]                               # 바닥 SE
    P[33] = [0.010, 0.010, 0.020]
    P[34] = [0.010, 0.010, 0.020 + 0.001 - DL]                                # 33–34 세로 당김
    rows = []

    def con(i, j, mag, sign, area=1e-8):
        d = _mi([P[i][k] - P[j][k] for k in range(3)])
        dist = math.sqrt(sum(x * x for x in d))
        u = [x / dist for x in d]
        ov = RAD[i] + RAD[j] - dist
        fn = [sign * mag * x for x in u]                                    # id1 이 받는 법선력 (+ = 밀어냄)
        cp = [P[i][k] - (RAD[i] - ov / 2.0) * u[k] for k in range(3)]       # 접촉점 = 겹침의 가운데 (두 입자 안)
        rows.append(dict(id1=i, id2=j, fn=fn, area=area, delta=ov, cp=cp))
    con(1, 2, 0.01, +1)
    con(10, 2, 0.01, +1)
    for i in range(10, 23):
        con(i, i + 1, 0.01, +1)
    con(2, 3, 0.004, +1)
    con(4, 5, 0.003, +1)
    con(31, 32, 0.001, +1)
    con(33, 34, 0.0005, -1)
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


def pref_hand(P, rows, box=BOX, plate=PLATE):
    """손 계산 ⟨σzz⟩ (압축 양수 · MPa) = −Σ_c (z_id2 − z_id1) F_z(id1) / (box² · plate) × scale / 1e6 — z 는 주기가 아니다."""
    s = sum((P[r['id2']][2] - P[r['id1']][2]) * r['fn'][2] for r in rows)
    return -s / (box * box * plate) * SCALE / 1e6


# ══════════════════════════════════════════════════════════════════════════════
#  [A] P_ref
# ══════════════════════════════════════════════════════════════════════════════
def section_pref(tmp):
    print('[A] P_ref — ⟨σzz⟩ 상자 평균 (합성 기둥 침대 · 손 계산 · 정본 텐서 · 상태)')
    import numpy as np
    import viewer3d_data as V
    import analyze_contacts as AC
    import dem_analysis_core as D
    P, rows = column_bed()
    d = os.path.join(tmp, 'col')
    write_bed(d, P, rows)
    lv = V.particle_load_view_for_case(d, TM, SCALE)
    pr = lv.get('p_ref') or {}
    want = pref_hand(P, rows)
    chk(f'A1 load_view.p_ref 있다 · 상태 OK ({pr.get("status")})', pr.get('status') == 'OK')
    chk(f'A2 P_ref = 손 계산 −Σ (z_id2 − z_id1) F_z / (box_x · box_y · plate_z) × scale/1e6 — 압축 양수 ({pr.get("MPa")} · 손 {want:.9g} MPa) · '
        f'덤프 순서 (10, 2) · 주기 너머 4–5 · 당김 33–34 포함', want > 0 and rel(pr.get('MPa'), want) < 1e-9)
    atoms_raw, _ = AC.load_atoms_raw(os.path.join(d, 'atoms.csv'))
    contacts_raw, _ = AC.load_contacts_raw(os.path.join(d, 'contacts.csv'))
    ref = D.calc_love_weber_stress(atoms_raw, contacts_raw, TM, PLATE, box_x=BOX, box_y=BOX, plate_z_source='mesh', return_arrays=True)
    ok_ref = ref.get('status') == 'OK'
    if ok_ref:
        vol = np.array([4.0 / 3.0 * math.pi * atoms_raw[a]['radius'] ** 3 for a in ref['ids']])
        szz = float(np.sum(vol * ref['tensor'][:, 2, 2]))
        p_lw = -szz / (BOX * BOX * PLATE) * SCALE / 1e6
    else:
        p_lw = math.nan
    chk(f'A3 정본 calc_love_weber_stress 텐서 × 4/3 π r³ 의 합 (Σ V σzz) = 접촉 합 = P_ref (입자 부피 선택과 무관) ({p_lw:.9g})',
        ok_ref and rel(p_lw, want) < 1e-9 and rel(p_lw, pr.get('MPa')) < 1e-12)
    rule = str(pr.get('rule') or '')
    chk(f'A4 기록 — 상자 [0.05, 0.05] (input_params) · 판 0.0296 (mesh) · 규칙 문구 (⟨σzz⟩ · 상자 평균 · 판 압력 · 벽 · calc_love_weber_stress) '
        f'({pr.get("box_xy")} · {pr.get("box_source")} · {pr.get("plate_z")} · {pr.get("plate_z_source")})',
        pr.get('box_xy') == [BOX, BOX] and pr.get('box_source') == 'input_params' and rel(pr.get('plate_z'), PLATE) < 1e-12
        and pr.get('plate_z_source') == 'mesh'
        and all(x in rule for x in ('⟨σzz⟩', '상자 평균', '판 압력', '벽', 'calc_love_weber_stress', '압축 양수')), rule[:300])
    d2 = os.path.join(tmp, 'col_nomesh')
    write_bed(d2, P, rows, mesh=False)
    lv2 = V.particle_load_view_for_case(d2, TM, SCALE)
    pr2 = lv2.get('p_ref') or {}
    chk(f'A5 mesh_info 없음 (plate_z = 입자 중심 추정) → P_ref = NOT_COMPUTED · 값 없음 · LW 는 그대로 OK ({pr2.get("status")})',
        str(pr2.get('status', '')).startswith('NOT_COMPUTED') and 'mesh' in str(pr2.get('status')) and pr2.get('MPa') is None
        and (lv2.get('am') or {}).get('lw_status') == 'OK')
    lv3 = V.particle_load_view_for_case(d, TM, SCALE, row_budget=3)
    pr3 = lv3.get('p_ref') or {}
    chk(f'A6 LW 예산 초과 (LW 없음) → P_ref = NOT_COMPUTED · 값 없음 ({pr3.get("status")})',
        str(pr3.get('status', '')).startswith('NOT_COMPUTED') and pr3.get('MPa') is None)
    from test_viewer_load_view import synth_bed, write_bed as write_bed_lv     # 10-07 합성 침대 — 세로 당김 1–10 이 이긴다 (Σ V σzz > 0)
    P4, rows4 = synth_bed()
    d4 = os.path.join(tmp, 'tension')
    write_bed_lv(d4, P4, rows4)
    lv4 = V.particle_load_view_for_case(d4, TM, SCALE)
    pr4 = lv4.get('p_ref') or {}
    want4 = pref_hand(P4, rows4, plate=0.03)
    chk(f'A7 축 하중이 인장 (손 계산 ⟨σzz⟩ = {want4:.3g} MPa < 0) 인 침대 → P_ref = UNDEFINED · 값 없음 (음수 · 0 으로 나누지 않는다) '
        f'({pr4.get("status")})', want4 < 0 and str(pr4.get('status', '')).startswith('UNDEFINED') and pr4.get('MPa') is None)
    return lv, P, rows, ref


# ══════════════════════════════════════════════════════════════════════════════
#  [B] SE 값
# ══════════════════════════════════════════════════════════════════════════════
def section_se(tmp, lv, ref):
    print('[B] SE 값 — id 구간 · 유효 4 자리 · 벽 표지 · ⟨σ_VM⟩ · 기존 키 그대로')
    import viewer3d_data as V
    se = (lv or {}).get('se') or {}
    chk(f'B1 load_view.se — n_se {se.get("n_se")} = SE {len(SE_IDS)} · lw_status OK · digits 4',
        se.get('n_se') == len(SE_IDS) and se.get('lw_status') == 'OK' and se.get('digits') == 4)
    chk(f'B2 id_runs = 오름차순 연속 구간 [[10, 14], [30, 5]] (틈 하나) ({se.get("id_runs")})', se.get('id_runs') == [[10, 14], [30, 5]])
    ids = expand_runs(se.get('id_runs'))
    vals = se.get('lw_vm_MPa') or []
    chk(f'B3 펼친 id = SE id 전부 (오름차순 · 중복 없음) · 값 수 = id 수 ({len(ids)} · {len(vals)})', ids == SE_IDS and len(vals) == len(ids))
    if (ref or {}).get('status') == 'OK' and ids == SE_IDS and len(vals) == len(ids):
        vm = {int(i): float(v) * SCALE / 1e6 for i, v in zip(ref['ids'], ref['arrays_vm'])}
        chk('B4 값 = 정본 배열 × scale/1e6 을 유효 4 자리로 (float(f"{v:.4g}")) — 같은 수',
            all(vals[k] == float(f'{vm[i]:.4g}') for k, i in enumerate(ids)))
        err = max((abs(vals[k] - vm[i]) / vm[i]) for k, i in enumerate(ids) if vm[i] > 0)
        chk(f'B5 유효 4 자리 상대 오차 최대 {err:.2e} ≤ 5e-4 · 접촉 없는 SE 30 = 0', err <= 5e-4 and vals[ids.index(30)] == 0.0)
    else:
        chk('B4 값 = 정본 배열 (유효 4 자리)', False, 'se 또는 정본 없음')
    chk(f'B6 ⟨σ_VM⟩ (전 입자 · MPa) = am.lw_mean_all_MPa — SE ÷ ⟨σ_VM⟩ 분모 = AM 만 보기와 같다 ({se.get("lw_mean_all_MPa")})',
        se.get('lw_mean_all_MPa') is not None and se.get('lw_mean_all_MPa') == ((lv or {}).get('am') or {}).get('lw_mean_all_MPa'))
    w = se.get('wall') or {}
    chk(f'B7 SE 벽 표지 = LW 규칙 (바닥 z − r < 0 · 판 z + r > plate_z) — 바닥 [31, 32] · 판 [23] · AM 벽 표지 그대로 {{1: floor}} ({w})',
        w.get('floor') == [31, 32] and w.get('plate') == [23] and w.get('plate_flag') is True
        and ikeys(((lv or {}).get('am') or {}).get('wall')) == {1: 'floor'})
    rule = str(se.get('rule') or '')
    chk('B8 규칙 문구 — calc_love_weber_stress · 유효 4 자리 · id 구간 · 벽 힘 없음',
        all(x in rule for x in ('calc_love_weber_stress', '유효 4 자리', 'id_runs', '벽')), rule[:300])
    am = (lv or {}).get('am') or {}
    chk(f'B9 기존 키 그대로 — 최상위 = 옛 6 키 + p_ref · se · am 안은 새 키 없음 ({sorted(set(lv or {}) - OLD_TOP_KEYS)} · '
        f'{sorted(set(am) ^ OLD_AM_KEYS)})', set(lv or {}) == OLD_TOP_KEYS | {'p_ref', 'se'} and set(am) == OLD_AM_KEYS)
    f = getattr(V, 'id_runs', None)
    bad_ok = True
    if callable(f):
        for b in ([3, 2], [1, 1]):
            try:
                f(b)
                bad_ok = False
            except ValueError:
                pass
    chk('B10 id_runs — [5, 6, 7, 10, 11, 20] → [[5, 3], [10, 2], [20, 1]] · [] → [] · 내림 · 중복 = ValueError (펼치면 값이 어긋난다)',
        callable(f) and f([5, 6, 7, 10, 11, 20]) == [[5, 3], [10, 2], [20, 1]] and f([]) == [] and bad_ok)
    P, rows = column_bed()
    d2 = os.path.join(tmp, 'col_nomesh_b')
    write_bed(d2, P, rows, mesh=False)
    se2 = (V.particle_load_view_for_case(d2, TM, SCALE).get('se') or {})
    w2 = se2.get('wall') or {}
    chk(f'B11 mesh 없음 → 판 표지 없음 (plate_flag False · 판 목록 빈칸) · 바닥은 그대로 · 값은 그대로 ({w2})',
        w2.get('plate_flag') is False and w2.get('plate') == [] and w2.get('floor') == [31, 32] and se2.get('lw_status') == 'OK'
        and len(se2.get('lw_vm_MPa') or []) == len(SE_IDS))
    se3 = (V.particle_load_view_for_case(os.path.join(tmp, 'col'), TM, SCALE, row_budget=3).get('se') or {})
    chk(f'B12 LW 예산 초과 → SE 값 없음 (빈 목록) · lw_status = NOT_COMPUTED · 벽 표지는 낸다 ({str(se3.get("lw_status"))[:40]})',
        str(se3.get('lw_status', '')).startswith('NOT_COMPUTED') and se3.get('lw_vm_MPa') == [] and se3.get('id_runs') == []
        and (se3.get('wall') or {}).get('floor') == [31, 32])


# ══════════════════════════════════════════════════════════════════════════════
#  [R] 50kg D2 · D3 끝 세트 (리포 tgz)
# ══════════════════════════════════════════════════════════════════════════════
#  기록값 (11-02 · 이 코드 · 끝 세트 sha256 = 각 README) — D1 (묶음 리포 밖 · 62.7 MB): P_ref 153.02496 MPa · 로그 156.15118 · 비 0.97998 ·
#  AM σ_VM ÷ P_ref 중앙값 1.12486 · 평균 1.22837 (벽 제외 1409 개 · ÷ 로그 판 압력 중앙값 1.10234)
#  ★ 11-02 (같은 묶음) 접촉 압력 |Fn|/A — 압축 AM–SE · AM–AM 평균 · 중앙 (같은 압축 행 규칙 · 이 코드로 잰 값) · D2 AM–SE 는 1저자 쪽 오프라인
#  도구 값 (평균 ≈ 369.6 · 중앙 ≈ 385.7 MPa) 과 맞춰 본다 · D1 (리포 밖) AM–SE 321.8047 · 337.1103 · AM–AM 3895.034 · 4074.546 (n 142519 · 2676)
KG50 = {
    'D2': dict(tgz='docs/data/kg50_d2_end_20261030/kg50_d2_end_20261030_4files.tgz', case='kg50_d2_b50', step=4015002,
               log='docs/data/kg50_d2_end_20261030/kg50_d2_b50_log.liggghts', p_log=279.79158, pzz=271.36632420059635,
               am_med=1.23393477052794, am_mean=1.2972342310707643, am_med_log=1.1967777693005395, n_am=1481, n_se=20872,
               p_se=(34833, 369.5820, 385.6721), p_am=(3293, 4140.6865, 4242.2487)),
    'D3': dict(tgz='docs/data/kg50_d3_cell_verdict_20261027/kg50_d3_end_20261027.tgz', case='kg50_d3_b50_s1', step=4575002,
               log='docs/data/kg50_d3_cell_verdict_20261027/kg50_d3_b50_s1_log.liggghts', p_log=291.3744, pzz=282.10228692713997,
               am_med=1.2570485725641372, am_mean=1.3296172186350599, am_med_log=1.217046786192747, n_am=1482, n_se=6184,
               p_se=(15054, 398.0276, 414.7896), p_am=(3389, 4166.0750, 4252.5255)),
}


def log_end_pressure(path):
    """로그 → (step, MPa) — 끝 정규 thermo 줄 (step atoms ke cpu v_pressMPa · cpu ≠ 0 — 끝 `run 0` 설정 줄 제외) · 판 압력 = 끝 열 × 1000."""
    pat = re.compile(r'^\s*(\d+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s*$')
    last = None
    with open(path, encoding='utf-8', errors='replace') as f:
        for ln in f:
            m = pat.match(ln)
            if not m:
                continue
            try:
                v = [float(x) for x in m.groups()]
            except ValueError:
                continue
            if v[3] != 0.0:
                last = (int(v[0]), v[4] * 1000.0)
    return last


def build_kg50_case(spec, dst):
    """리포 tgz → 끝 세트 넷 (이름 고정 · 묶음 경로는 쓰지 않는다) → parse_liggghts (웹앱 파서)."""
    raw = os.path.join(dst, '_raw')
    os.makedirs(raw, exist_ok=True)
    c, s = spec['case'], spec['step']
    want = {f'{c}/post_{c}/atom_end_{s}.liggghts': f'atom_end_{s}.liggghts',
            f'{c}/post_{c}/contact_end_{s}.liggghts': f'contact_end_{s}.liggghts',
            f'{c}/post_{c}/mesh_end_{s}.stl': f'mesh_end_{s}.stl',
            f'{c}/input_{c}.liggghts': f'input_{c}.liggghts'}
    with tarfile.open(os.path.join(ROOT, spec['tgz']), 'r:gz') as tf:
        for name, out in want.items():
            m = tf.getmember(name)
            if not m.isfile():
                return False
            with tf.extractfile(m) as fi, open(os.path.join(raw, out), 'wb') as fo:
                shutil.copyfileobj(fi, fo)
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, 'parse_liggghts.py')] + [os.path.join(raw, o) for o in want.values()]
                       + ['-o', dst], capture_output=True, text=True, timeout=600)
    shutil.rmtree(raw, ignore_errors=True)
    return r.returncode == 0


def section_kg50(tmp):
    print('[R] 50kg D2 · D3 끝 세트 — ⟨σzz⟩ ↔ 로그 판 압력 (출하 관문 ±5 %) · AM σ_VM ÷ P_ref')
    import statistics
    import viewer3d_data as V
    for bed, sp in KG50.items():
        d = os.path.join(tmp, 'kg50_' + bed)
        if not chk(f'R0 {bed} 리포 tgz → 끝 세트 넷 → parse_liggghts', build_kg50_case(sp, d)):
            continue
        le = log_end_pressure(os.path.join(ROOT, sp['log'])) or (None, None)
        chk(f'R1 {bed} 로그 끝 정규 thermo 줄 = step {sp["step"]} · 판 압력 {sp["p_log"]} MPa ({le})',
            le[0] == sp['step'] and rel(le[1], sp['p_log']) < 1e-9)
        lv = V.particle_load_view_for_case(d, TM, SCALE)
        pr = lv.get('p_ref') or {}
        p = pr.get('MPa')
        ratio = (p / sp['p_log']) if isinstance(p, (int, float)) else math.nan
        chk(f'R2 {bed} P_ref = ⟨σzz⟩ {p} MPa · 로그 판 압력 {sp["p_log"]} 의 {ratio:.5f} 배 — ±5 % 안 (벽 접촉 항 제외 몫) · 기록 {sp["pzz"]:.8g}',
            pr.get('status') == 'OK' and abs(ratio - 1.0) <= 0.05 and rel(p, sp['pzz']) < 1e-7)
        am = lv.get('am') or {}
        wall = ikeys(am.get('wall'))
        v = [float(x) / p for i, x in ikeys(am.get('lw_vm_MPa')).items() if i not in wall] if pr.get('status') == 'OK' else []
        med = statistics.median(v) if v else math.nan
        mean = sum(v) / len(v) if v else math.nan
        vlog = [float(x) / sp['p_log'] for i, x in ikeys(am.get('lw_vm_MPa')).items() if i not in wall]
        mlog = statistics.median(vlog) if vlog else math.nan
        chk(f'R3 {bed} AM σ_VM ÷ P_ref (벽 접촉 AM 제외 {len(v)} 개) 중앙값 {med:.5f} · 평균 {mean:.5f} = 기록 · ÷ 로그 판 압력 중앙값 '
            f'{mlog:.4f} (앞선 점검값과 같다)', rel(med, sp['am_med']) < 1e-7 and rel(mean, sp['am_mean']) < 1e-7
            and rel(mlog, sp['am_med_log']) < 1e-9 and am.get('n_am') == sp['n_am'])
        se = lv.get('se') or {}
        ids = expand_runs(se.get('id_runs'))
        chk(f'R4 {bed} SE 값 {len(se.get("lw_vm_MPa") or [])} 개 = SE {sp["n_se"]} 개 · id 구간 {len(se.get("id_runs") or [])} 개 · '
            f'펼친 id 오름차순 · 중복 없음', se.get('n_se') == sp['n_se'] and len(ids) == sp['n_se']
            and len(se.get('lw_vm_MPa') or []) == sp['n_se'] and ids == sorted(set(ids)))
        cs, ca = am.get('contacts_se') or {}, am.get('contacts') or {}
        ps_, pa_ = cs.get('p_MPa_stats') or {}, ca.get('p_MPa_stats') or {}
        chk(f'R5 {bed} ★ 접촉 압력 |Fn|/A (압축 · 상한과 무관) — AM–SE n {ps_.get("n")} · 평균 {ps_.get("mean")} · 중앙 {ps_.get("median")} · '
            f'AM–AM n {pa_.get("n")} · 평균 {pa_.get("mean")} · 중앙 {pa_.get("median")} MPa = 기록 {sp["p_se"]} · {sp["p_am"]} (서버 = 유효 6 자리)',
            ps_.get('n') == sp['p_se'][0] == cs.get('n_compressive') and rel(ps_.get('mean'), sp['p_se'][1]) < 1e-5
            and rel(ps_.get('median'), sp['p_se'][2]) < 1e-5 and pa_.get('n') == sp['p_am'][0] == ca.get('n_compressive')
            and rel(pa_.get('mean'), sp['p_am'][1]) < 1e-5 and rel(pa_.get('median'), sp['p_am'][2]) < 1e-5)
        if bed == 'D2':
            chk(f'R6 D2 AM–SE 압축 접촉 압력 평균 ≈ 369.6 · 중앙 ≈ 385.7 MPa (1저자 쪽 오프라인 도구 · 반올림 ±0.05) ({ps_.get("mean")} · {ps_.get("median")})',
                abs(ps_.get('mean', 0) - 369.6) <= 0.05 and abs(ps_.get('median', 0) - 385.7) <= 0.05)
        rows = [dict(zip(cs.get('fields') or [], r)) for r in cs.get('rows') or []]
        chk(f'R7 {bed} AM–SE 보낸 행 {len(rows)} (상한 {cs.get("cap")}) — 압축 행만 p_MPa 양수 · 나머지 null · 보낸 압축 행 수 = {cs.get("n_compressive_sent")}',
            bool(rows) and all((r.get('p_MPa') is not None and r['p_MPa'] > 0) == (int(r['flag']) == 1) for r in rows)
            and sum(1 for r in rows if r.get('p_MPa') is not None) == cs.get('n_compressive_sent'))


# ══════════════════════════════════════════════════════════════════════════════
#  [J] 뷰어 (node)
# ══════════════════════════════════════════════════════════════════════════════
JS_NAMES = ('netCurrentFmtJ', 'netCurrentT', 'netCurrentTicks', 'jeEscH', 'jetColor', 'setLegend', 'loadViewAmMetric', 'amOnlyRange',
            'amOnlyLegendHtml', 'amOnlyColorbarSpec', '_amOnlyControlsHtml', '_amOnlyBasis', 'loadViewAmContacts', 'amOnlyContactLegendHtml',
            'amOnlyContactColorbarSpec', 'amOnlyContactRange', '_amOnlyCapDispose', '_amOnlyTeardown', 'applyAmOnlyView', '_amOnlyWireLegend',
            # ★ 11-02
            'lwIsLwMetric', 'lwRangeValid', 'lwRangeKey', 'lwRangeLoad', 'lwRangeSave', 'lwRangeSync', 'lwRangeRemember', 'lwRangeSetLim',
            'lwFixedLim', 'lwFin', 'lwLinT', 'lwLinTicks', 'lwPref', 'lwPrefNote', 'lwLimInputsHtml', 'seLwExpand', 'seWallSet',
            'loadViewSeMetric', 'applySeOnlyView', '_seOnlyTeardown', 'seOnlyLegendHtml', 'seOnlyMissingHtml', 'seOnlyColorbarSpec',
            '_seOnlyWireLegend',
            # ★ 11-02 접촉마다 압력 (같은 묶음) — applyAmOnlyView · amOnlyLegendHtml · lwRangeSync 가 부르는 갈래 도우미
            'lwFixedCapable', 'amOnlyContactKind')
JS_CONSTS = ('COL', 'OPA', 'AMONLY_CONTACT_OPT', 'LW_RANGE_DEFAULT')

JS_SHIM = r"""
const THREE = { Color: class { constructor(h) { this.hex = (h === undefined ? 0 : h); } setHex(h) { this.hex = h; return this; } } };
const EL = {};
const LEG = { innerHTML: '', querySelector: sel => (EL[sel] || (EL[sel] = { sel: sel, h: {}, addEventListener(ev, fn) { this.h[ev] = fn; } })) };
const CB = { SE: { checked: true }, AM_P: { checked: true }, AM_S: { checked: true } };
const document = { getElementById: id => (id === 'view-mode-legend' ? LEG : null),
                   querySelector: sel => { const m = /data-layer="(\w+)"/.exec(sel); return m ? (CB[m[1]] || null) : null; } };
const STORE = {};
const MEMSTORE = { getItem: k => (Object.prototype.hasOwnProperty.call(STORE, k) ? STORE[k] : null), setItem: (k, v) => { STORE[k] = String(v); } };
const THROWSTORE = { getItem() { throw new Error('SecurityError'); }, setItem() { throw new Error('QuotaExceededError'); } };
function mkMesh(parts) {
  return { visible: true, material: { opacity: 0.85, transparent: true }, instanceColor: { needsUpdate: false },
           userData: { particles: parts }, cols: parts.map(() => null), setColorAt(i, c) { this.cols[i] = c.hex; } };
}
function fire(sel, ev, value, checked) { const e = EL[sel]; if (!e || !e.h[ev]) return false; e.h[ev]({ target: { value: value, checked: checked } }); return true; }
"""


def section_js(tmp, lv, P):
    print('[J] 뷰어 — 드롭다운 · SE 만 · 양 σ_VM ÷ P_ref · 고정 범위 (저장) · 기본 그림 그대로 (node)')
    js = open(VIEWER_JS, encoding='utf-8').read()
    try:
        bc = js_fn(js, 'buildControls')
    except (ValueError, AssertionError):
        bc = ''
    sels = re.findall(r'<select id="view-mode".*?</select>', bc, re.S)
    mpm_sel, dem_sel = (sels + ['', ''])[:2]
    m_se = re.search(r'<option value="se_only">([^<]*)</option>', dem_sel)
    m_am = re.search(r'<option value="am_only">([^<]*)</option>', dem_sel)
    chk(f'J1 DEM 드롭다운에 se_only (SE 만 · LW) · am_only 바로 뒤 · MPM 드롭다운엔 없음 ({m_se.group(1) if m_se else None})',
        m_se is not None and 'SE 만' in m_se.group(1) and 'LW' in m_se.group(1) and 'se_only' not in mpm_sel
        and m_am is not None and dem_sel.index('value="se_only"') > dem_sel.index('value="am_only"')
        and re.search(r'value="am_only">[^<]*</option>\s*<option value="se_only">', dem_sel) is not None)
    try:
        avm = js_fn(js, 'applyViewMode')
    except (ValueError, AssertionError):
        avm = ''
    head = avm[:avm.find("if (!mode || mode === 'default')")] if "if (!mode || mode === 'default')" in avm else ''
    chk("J2 applyViewMode — 'se_only' → applySeOnlyView · 머리 (default 분기 앞) 에서 _seOnlyTeardown · AM 보이기 = 머리의 체크박스 되돌림 (그대로)",
        re.search(r"mode === 'se_only'\)\s*\{\s*applySeOnlyView\(state\);\s*return;", avm) is not None
        and '_seOnlyTeardown(state);' in head and '_amOnlyTeardown(state);' in head
        and re.search(r'm\.visible = cb \? cb\.checked : true;', head) is not None)
    m_init = re.search(r"state\._amOnlyUi = \{ metric: 'lw', range: 'p5p95', wall: true,", js)
    chk('J3 AM 만 보기 기본 ui 그대로 — metric lw · range p5p95 · wall (저장된 선택이 없으면 오늘과 같은 그림)', m_init is not None)
    parts, miss = [], []
    for n in JS_CONSTS:
        try:
            parts.append(js_const(js, n))
        except (ValueError, AssertionError):
            miss.append(n)
    for n in JS_NAMES:
        try:
            parts.append(js_fn(js, n))
        except (ValueError, AssertionError):
            miss.append(n)
    if not chk(f'J4 viewer3d.js 에서 함수 · 상수를 잘라 냈다 (없음 {miss})', not miss):
        return
    if not chk('J5 자료 (합성 기둥 침대 load_view · p_ref OK · se OK) 가 있다',
               bool(lv) and (lv.get('p_ref') or {}).get('status') == 'OK' and (lv.get('se') or {}).get('lw_status') == 'OK'):
        return
    lv = copy.deepcopy(lv)
    parts_js = [{'id': i, 'type': TM[TYPE[i]]} for i in sorted(P)]
    script = JS_SHIM + '\n'.join(parts) + '\n' + r"""
const LV = __LV__;
const PARTS = __PARTS__;
const out = {};
function mkState() {
  const by = t => PARTS.filter(p => p.type === t);
  return { data: { aux: { load_view: LV } }, meshes: { AM_P: mkMesh(by('AM_P')), AM_S: mkMesh(by('AM_S')), SE: mkMesh(by('SE')) } };
}
const P_REF = LV.p_ref.MPa;
// ── 양 lw_p
out.mP = loadViewAmMetric(LV, 'lw_p');
out.mLw = loadViewAmMetric(LV, 'lw');
const noP = JSON.parse(JSON.stringify(LV)); delete noP.p_ref;
out.mNoP = loadViewAmMetric(noP, 'lw_p');
const badP = JSON.parse(JSON.stringify(LV)); badP.p_ref = { status: 'UNDEFINED (⟨σzz⟩ ≤ 0)', MPa: null };
out.mBadP = loadViewAmMetric(badP, 'lw_p');
out.pref = lwPref(LV);
// ── 저장소 — 없음 (node 기본) · 깨진 값 · 막힘 · 정상
out.loadNone = lwRangeLoad('lw_p');
out.saveNone = lwRangeSave('lw_p', 'fixed', 0, 3);
globalThis.localStorage = THROWSTORE;
out.loadThrow = lwRangeLoad('lw_p');
out.saveThrow = lwRangeSave('lw_p', 'fixed', 0, 3);
globalThis.localStorage = MEMSTORE;
STORE[lwRangeKey('lw_p')] = '{not json';
out.loadBad = lwRangeLoad('lw_p');
STORE[lwRangeKey('lw_p')] = JSON.stringify({ mode: 'sideways', lo: 0, hi: 3 });
out.loadBadMode = lwRangeLoad('lw_p');
STORE[lwRangeKey('lw_p')] = JSON.stringify({ mode: 'fixed', lo: 2, hi: 1 });
out.loadBadLim = lwRangeLoad('lw_p');
delete STORE[lwRangeKey('lw_p')];
out.keys = [lwRangeKey('lw'), lwRangeKey('lw_p')];
out.saveOk = lwRangeSave('lw_p', 'fixed', 0.5, 2.5);
out.loadOk = lwRangeLoad('lw_p');
out.loadOther = lwRangeLoad('lw');
delete STORE[lwRangeKey('lw_p')];
out.valid = [lwRangeValid(0, 3), lwRangeValid(3, 3), lwRangeValid(NaN, 3), lwRangeValid(0, Infinity), lwRangeValid('1', '2')];
out.linT = [lwLinT(0, 0, 3), lwLinT(1.5, 0, 3), lwLinT(3, 0, 3), lwLinT(9, 0, 3), lwLinT(-1, 0, 3)];
out.fin = [lwFin(0), lwFin(1.2), lwFin(undefined), lwFin(null), lwFin(''), lwFin(NaN), lwFin('2')];
out.ticks03 = lwLinTicks(0, 3);
out.ticksOdd = lwLinTicks(0.5, 2.5);
out.limDef = lwFixedLim({ metric: 'lw_p' });
out.limDefLw = lwFixedLim({ metric: 'lw' });
// ── 기본 그림 (저장 없음) — 새 applyAmOnlyView 색 = 옛 알고리즘 (lw · p5p95 · 벽 회색 · v > 0 · log jet)
const s0 = mkState();
applyAmOnlyView(s0);
const ui0 = s0._amOnlyUi;
out.ui0 = { metric: ui0.metric, range: ui0.range, wall: ui0.wall };
const wall0 = LV.am.wall || {};
const mLw = loadViewAmMetric(LV, 'lw');
const vals0 = [];
['AM_P', 'AM_S'].forEach(t => s0.meshes[t].userData.particles.forEach(p => { if (wall0[p.id]) return; const v = mLw.map[p.id]; if (v > 0) vals0.push(v); }));
const r0 = amOnlyRange(vals0, 'p5p95');
const want0 = {};
['AM_P', 'AM_S'].forEach(t => { want0[t] = s0.meshes[t].userData.particles.map(p => {
  if (wall0[p.id]) return 0x9ca3af; const v = mLw.map[p.id]; return v > 0 ? jetColor(netCurrentT(v, r0[0], r0[1])) : 0x4b5563; }); });
out.def = { got: { AM_P: s0.meshes.AM_P.cols.slice(), AM_S: s0.meshes.AM_S.cols.slice() }, want: want0, seVis: s0.meshes.SE.visible,
            leg: LEG.innerHTML, last: s0._amOnlyLast.st };
out.specDef = amOnlyColorbarSpec(LV, { metric: 'lw', range: 'p5p95', wall: true }, -0.5, 0.5);
out.specDefMM = amOnlyColorbarSpec(LV, { metric: 'lw', range: 'minmax', wall: false }, -0.5, 0.5);
// ── AM lw_p · 고정 (선형) — 범위 [lo, hi] = 이 침대 값의 최소–최대 (안쪽 색까지 본다)
const mP = loadViewAmMetric(LV, 'lw_p');
const pv = Object.keys(mP.map).map(k => mP.map[k]).filter(v => v > 0).sort((a, b) => a - b);
const LO = pv[0], HI = pv[pv.length - 1];
lwRangeSave('lw_p', 'fixed', LO, HI);
const s1 = mkState();
s1._amOnlyUi = { metric: 'lw_p', range: 'p5p95', wall: false, top: 5000, basis: 'drawn' };
applyAmOnlyView(s1);
const want1 = {};
['AM_P', 'AM_S'].forEach(t => { want1[t] = s1.meshes[t].userData.particles.map(p => {
  const v = mP.map[p.id]; return jetColor(Math.max(0, Math.min(1, (v - LO) / (HI - LO)))); }); });
out.fixAm = { range: s1._amOnlyUi.range, got: { AM_P: s1.meshes.AM_P.cols.slice(), AM_S: s1.meshes.AM_S.cols.slice() }, want: want1,
              st: Object.assign({}, s1._amOnlyLast.st),
              leg: LEG.innerHTML, LO: LO, HI: HI };
out.specFix = amOnlyColorbarSpec(LV, { metric: 'lw_p', range: 'fixed', wall: false }, 0, 3);
// 조작 배선 — 범위 → p5p95 (저장) · 다시 고정 · hi 입력 (저장 · 다시 그림) · 깨진 입력 (그대로)
out.wire = {};
out.wire.toP = fire('#amonly-range', 'change', 'p5p95');
out.wire.afterP = { range: s1._amOnlyUi.range, stored: lwRangeLoad('lw_p') };
fire('#amonly-range', 'change', 'fixed');
out.wire.lo = fire('#amonly-lo', 'change', '0');               // lo 먼저 — 이 침대의 σ_VM ÷ P_ref 최소가 2.5 보다 커서 hi 2.5 를 먼저 주면 hi ≤ lo (거부가 맞다)
out.wire.hi = fire('#amonly-hi', 'change', '2.5');
out.wire.afterLim = { stored: lwRangeLoad('lw_p'), st: Object.assign({}, s1._amOnlyLast.st) };
out.wire.badHi = fire('#amonly-hi', 'change', '-1');
out.wire.badEmpty = fire('#amonly-lo', 'change', '');
out.wire.afterBad = { stored: lwRangeLoad('lw_p'), st: Object.assign({}, s1._amOnlyLast.st) };
// 다른 양 (fn) 으로 — 고정을 받지 않는다 → p5p95 · 저장된 lw_p 고정은 그대로
fire('#amonly-metric', 'change', 'fn');
out.wire.fn = { range: s1._amOnlyUi.range, stored: lwRangeLoad('lw_p'), leg: LEG.innerHTML };
fire('#amonly-metric', 'change', 'lw_p');
out.wire.backP = { range: s1._amOnlyUi.range };
// 새 케이스 (새 state) — 같은 저장 → 같은 눈금 (모드 · lo · hi)
const s2 = mkState();
s2._amOnlyUi = { metric: 'lw_p', range: 'p5p95', wall: true, top: 5000, basis: 'drawn' };
applyAmOnlyView(s2);
out.newCase = { range: s2._amOnlyUi.range, st: s2._amOnlyLast.st };
// P_ref 없음 → 칠하지 않는다 (AM 기본색) · 사유
const s3 = mkState(); s3.data.aux.load_view = noP;
s3._amOnlyUi = { metric: 'lw_p', range: 'fixed', wall: true, top: 5000, basis: 'drawn' };
applyAmOnlyView(s3);
out.noPref = { leg: LEG.innerHTML, cols: s3.meshes.AM_S.cols.slice() };
// ── SE 만 — 기본 (lw_p · 고정 · 벽 회색) · 저장 없음 = 0 … 3
Object.keys(STORE).forEach(k => delete STORE[k]);
const s4 = mkState();
s4.meshes.AM_P.visible = true; s4.meshes.AM_S.visible = true; s4.meshes.SE.visible = false;
applySeOnlyView(s4);
const ex = seLwExpand(LV.se);
const wallSe = seWallSet(LV.se);
const want4 = s4.meshes.SE.userData.particles.map(p => {
  if (wallSe.has(p.id)) return 0x9ca3af; const v = ex.map.get(p.id) / P_REF; return jetColor(Math.max(0, Math.min(1, v / 3))); });
out.se = { ui: { metric: s4._seOnlyUi.metric, range: s4._seOnlyUi.range, wall: s4._seOnlyUi.wall },
           amVis: [s4.meshes.AM_P.visible, s4.meshes.AM_S.visible], seVis: s4.meshes.SE.visible,
           seMat: [s4.meshes.SE.material.opacity, s4.meshes.SE.material.transparent], got: s4.meshes.SE.cols.slice(), want: want4,
           st: Object.assign({}, s4._seOnlyLast.st), leg: LEG.innerHTML, exN: ex.n, exOk: ex.ok, wall: Array.from(wallSe).sort((a, b) => a - b) };
// SE log (p5p95) — 0 = 값 없음 (어두운 회색) · 벽 뺀 v > 0 의 가장 가까운 순위
s4._seOnlyUi.range = 'p5p95';
applySeOnlyView(s4);
const v5 = [];
s4.meshes.SE.userData.particles.forEach(p => { if (wallSe.has(p.id)) return; const v = ex.map.get(p.id) / P_REF; if (v > 0) v5.push(v); });
const r5 = amOnlyRange(v5, 'p5p95');
out.seLog = { got: s4.meshes.SE.cols.slice(), want: s4.meshes.SE.userData.particles.map(p => {
  if (wallSe.has(p.id)) return 0x9ca3af; const v = ex.map.get(p.id) / P_REF; return v > 0 ? jetColor(netCurrentT(v, r5[0], r5[1])) : 0x4b5563; }),
  st: Object.assign({}, s4._seOnlyLast.st) };
// SE lw (÷ ⟨σ_VM⟩) — 분모 = AM 만 보기와 같은 전 입자 평균
const mSe = loadViewSeMetric(LV, 'lw');
out.seLw = { ok: mSe.ok, v34: mSe.map.get(34), want34: ex.map.get(34) / LV.am.lw_mean_all_MPa, label: mSe.label };
out.seSpec = seOnlyColorbarSpec(LV, { metric: 'lw_p', range: 'fixed', wall: true }, 0, 3);
out.seSpecLog = seOnlyColorbarSpec(LV, { metric: 'lw', range: 'p5p95', wall: false }, -0.5, 0.5);
// 걷기 — SE 체크박스대로 보이기 · 반투명 · 기본색 (AM 보이기 = applyViewMode 머리)
CB.SE.checked = false;
_seOnlyTeardown(s4);
out.td = { seVis: s4.meshes.SE.visible, seMat: [s4.meshes.SE.material.opacity, s4.meshes.SE.material.transparent],
           cols: Array.from(new Set(s4.meshes.SE.cols)) };
CB.SE.checked = true;
// SE 자료 없음 (옛 캐시) — 사유 · SE 기본색 · AM 숨김
const noSe = JSON.parse(JSON.stringify(LV)); delete noSe.se;
const s6 = mkState(); s6.data.aux.load_view = noSe;
applySeOnlyView(s6);
out.noSe = { leg: LEG.innerHTML, cols: Array.from(new Set(s6.meshes.SE.cols)), amVis: [s6.meshes.AM_P.visible, s6.meshes.AM_S.visible] };
// 깨진 id 구간 — 값 수와 어긋나면 ok false
const brk = JSON.parse(JSON.stringify(LV.se)); brk.lw_vm_MPa = brk.lw_vm_MPa.slice(1);
out.brk = seLwExpand(brk);
console.log(JSON.stringify(out));
""".replace('__LV__', json.dumps(lv, ensure_ascii=False)).replace('__PARTS__', json.dumps(parts_js))
    res = run_node(script)
    if not chk('J6 node 실행', res is not None):
        return
    pref = lv['p_ref']['MPa']
    mp = res['mP'] or {}
    want_map = {int(k): float(v) / pref for k, v in lv['am']['lw_vm_MPa'].items()}
    got_map = ikeys(mp.get('map'))
    chk(f'J7 양 lw_p — 맵 = am.lw_vm_MPa ÷ P_ref ({pref:.6g} MPa) · 이름 σ_VM ÷ P_ref · ok ({mp.get("label")})',
        mp.get('ok') is True and set(got_map) == set(want_map) and all(rel(got_map[i], want_map[i]) < 1e-12 for i in want_map)
        and 'P_ref' in str(mp.get('label')) and rel(mp.get('pref'), pref) < 1e-15)
    ml = res['mLw'] or {}
    chk('J8 양 lw (옛) 그대로 — 맵 = am.lw_ratio · 이름 σ_VM / ⟨σ_VM⟩ (전 입자) · ⟨σ_VM⟩ MPa',
        ml.get('ok') is True and ikeys(ml.get('map')) == ikeys(lv['am']['lw_ratio'])
        and ml.get('label') == 'Love–Weber 입자 응력 σ_VM / ⟨σ_VM⟩ (전 입자)' and rel(ml.get('mpa'), lv['am']['lw_mean_all_MPa']) < 1e-15)
    chk(f'J9 P_ref 없음 (옛 캐시) · UNDEFINED → ok false + 사유 (0 으로 칠하지 않는다) ({(res["mNoP"] or {}).get("reason")} · '
        f'{(res["mBadP"] or {}).get("reason")})', (res['mNoP'] or {}).get('ok') is False and '15' in str((res['mNoP'] or {}).get('reason'))
        and (res['mBadP'] or {}).get('ok') is False and 'UNDEFINED' in str((res['mBadP'] or {}).get('reason')))
    chk(f'J10 저장소 없음 (node · localStorage 정의 안 됨) · 막힘 (throw) → 읽기 null · 쓰기 false · 예외를 밖으로 내지 않는다 '
        f'({res["loadNone"]} · {res["saveNone"]} · {res["loadThrow"]} · {res["saveThrow"]})',
        res['loadNone'] is None and res['saveNone'] is False and res['loadThrow'] is None and res['saveThrow'] is False)
    chk(f'J11 깨진 저장값 → 무시 (JSON 아님 · 모르는 모드 = null · lo ≥ hi = 기본 0 … 3) ({res["loadBad"]} · {res["loadBadMode"]} · '
        f'{res["loadBadLim"]})', res['loadBad'] is None and res['loadBadMode'] is None
        and res['loadBadLim'] == {'mode': 'fixed', 'lo': 0, 'hi': 3})
    chk(f'J12 양마다 다른 키 · 저장 → 읽기 같은 값 · 다른 양은 영향 없음 ({res["keys"]} · {res["loadOk"]} · {res["loadOther"]})',
        res['keys'][0] != res['keys'][1] and res['saveOk'] is True and res['loadOk'] == {'mode': 'fixed', 'lo': 0.5, 'hi': 2.5}
        and res['loadOther'] is None)
    chk(f'J13 lo · hi 검사 (유한 · hi > lo) {res["valid"]} · 선형 t = (v − lo)/(hi − lo) 자름 {res["linT"]} · 값 있음 판정 {res["fin"]}',
        res['valid'] == [True, False, False, False, True] and res['linT'] == [0, 0.5, 1, 1, 0]
        and res['fin'] == [True, True, False, False, False, False, True])
    t3 = res['ticks03'] or []
    chk(f'J14 선형 컬러바 눈금 0 … 3 = 0 · 1 · 2 · 3 (4 개 — 7–8 개는 많다) · 0.5 … 2.5 = 양 끝 + 안쪽 ({[t["label"] for t in t3]} · '
        f'{[t["label"] for t in res["ticksOdd"] or []]})',
        [t['label'] for t in t3] == ['0', '1', '2', '3'] and all(abs(t['p'] - k / 3) < 1e-12 for k, t in enumerate(t3))
        and (res['ticksOdd'] or [{}])[0].get('label') == '0.5' and (res['ticksOdd'] or [{}])[-1].get('label') == '2.5'
        and len(res['ticksOdd']) <= 6)
    chk(f'J15 고정 범위 기본 = 0 … 3 (σ_VM ÷ P_ref · σ_VM / ⟨σ_VM⟩) ({res["limDef"]} · {res["limDefLw"]})',
        res['limDef'] == [0, 3] and res['limDefLw'] == [0, 3])
    d0 = res['def']
    chk(f'J16 기본 그림 (저장 없음) — ui = lw · p5p95 · 벽 ({res["ui0"]}) · AM 색 = 옛 알고리즘 (p5–p95 log jet · 벽 회색 · v ≤ 0 어두운 회색) 그대로 · '
        f'SE 숨김', res['ui0'] == {'metric': 'lw', 'range': 'p5p95', 'wall': True} and d0['got'] == d0['want'] and d0['seVis'] is False
        and 'lin' not in d0['last'])
    leg0 = re.sub(r'<select.*?</select>', '', d0['leg'], flags=re.S)
    chk('J17 기본 범례 (선택 상자 뺀 글) — × ⟨σ_VM⟩ · (jet · log) · 색 범위 = AM 만의 p5–p95 (벽 접촉 입자 뺌) · P_ref · 선형 · 고정 문구 없음',
        '× ⟨σ_VM⟩' in leg0 and '(jet · log)' in leg0 and '색 범위 = AM 만의 p5–p95 (벽 접촉 입자 뺌)' in leg0
        and 'P_ref' not in leg0 and '선형' not in leg0 and '고정' not in leg0, leg0[:500])
    chk('J18 기본 범례 조작 — 양 고르기에 σ_VM ÷ P_ref (lw_p) 더함 · 범위 고르기에 고정 (fixed) 더함 · 기본 선택 = lw · p5p95',
        re.search(r'<option value="lw" selected>', d0['leg']) is not None and 'value="lw_p"' in d0['leg'] and 'P_ref' in d0['leg']
        and re.search(r'<option value="p5p95" selected>', d0['leg']) is not None and 'value="fixed"' in d0['leg']
        and '고정 (모든 케이스 공통)' in d0['leg'])
    sd = res['specDef'] or {}
    chk('J19 기본 컬러바 글 그대로 (제목 · 부제 · 눈금 = log)',
        sd.get('title') == 'AM only — Love–Weber particle stress σ_VM / ⟨σ_VM⟩ (all particles)'
        and sd.get('sub') == ('Colour range = AM particles only (p5–p95, wall-touching AM greyed and excluded).  Love–Weber (same definition '
                              'as stress_ratio_<phase>_lw) · wall forces absent for wall-touching particles · model contact forces.  Log colour scale.')
        and (res['specDefMM'] or {}).get('sub', '').startswith('Colour range = AM particles only (min–max).  ')
        and len(sd.get('ticks') or []) >= 2, repr(sd)[:400])
    fa = res['fixAm']
    chk(f'J20 AM σ_VM ÷ P_ref · 고정 (저장된 모드 = fixed · lo {fa["LO"]:.4g} … hi {fa["HI"]:.4g}) — 색 = 선형 jet (자름) · st.lin',
        fa['range'] == 'fixed' and fa['got'] == fa['want'] and fa['st'].get('lin') is True and rel(fa['st'].get('lo'), fa['LO']) < 1e-15
        and rel(fa['st'].get('hi'), fa['HI']) < 1e-15)
    lf = fa['leg']
    chk('J21 범례 (σ_VM ÷ P_ref · 고정) — P_ref = ⟨σzz⟩ 상자 평균 = 판 압력 (힘 평형 · 벽 접촉 항 제외) · MPa 값 · 색 범위 = 고정 (선형 · 모든 케이스 공통) · '
        'lo · hi 입력 · 고정 선택',
        all(x in lf for x in ('P_ref', '⟨σzz⟩ 상자 평균', '판 압력', '힘 평형', '벽 접촉 항 제외', 'MPa', '색 범위 = 고정', '선형',
                              '모든 케이스 공통', 'id="amonly-lo"', 'id="amonly-hi"'))
        and re.search(r'<option value="fixed" selected>', lf) is not None and re.search(r'<option value="lw_p" selected>', lf) is not None,
        lf[:600])
    sf = res['specFix'] or {}
    chk(f'J22 컬러바 (σ_VM ÷ P_ref · 고정) — jet · 제목 σ_VM / P_ref + P_ref MPa · 눈금 0 · 1 · 2 · 3 (선형) · 부제 Linear · common to all cases '
        f'({sf.get("title")})', sf.get('map') == 'jet' and 'σ_VM / P_ref' in str(sf.get('title')) and 'MPa' in str(sf.get('title'))
        and [t['label'] for t in sf.get('ticks') or []] == ['0', '1', '2', '3'] and 'Linear colour scale' in str(sf.get('sub'))
        and 'common to all cases' in str(sf.get('sub')) and 'box-average' in str(sf.get('title')) + str(sf.get('sub')))
    w = res['wire']
    chk(f'J23 조작 — 범위 → p5p95 = 그 양에 저장 (모드) · 다시 고정 · hi 2.5 · lo 0 입력 = 저장 + 다시 그림 ({w["afterP"]} · {w["afterLim"]["stored"]})',
        w['toP'] is True and w['afterP']['range'] == 'p5p95' and (w['afterP']['stored'] or {}).get('mode') == 'p5p95'
        and w['hi'] is True and w['lo'] is True and w['afterLim']['stored'] == {'mode': 'fixed', 'lo': 0, 'hi': 2.5}
        and w['afterLim']['st'].get('lin') is True and w['afterLim']['st'].get('hi') == 2.5 and w['afterLim']['st'].get('lo') == 0)
    chk(f'J24 깨진 입력 (hi ≤ lo · 빈칸) → 저장 · 그림 그대로 ({w["afterBad"]["stored"]})',
        w['afterBad']['stored'] == {'mode': 'fixed', 'lo': 0, 'hi': 2.5} and w['afterBad']['st'].get('hi') == 2.5
        and w['afterBad']['st'].get('lo') == 0)
    chk(f'J25 고정을 받지 않는 양 (최대 AM–AM 힘) → p5p95 · 고정 선택지 · lo · hi 없음 · 저장된 σ_VM ÷ P_ref 고정은 그대로 · 되돌아오면 고정 '
        f'({w["fn"]["range"]} · {w["backP"]["range"]})', w['fn']['range'] == 'p5p95' and 'value="fixed"' not in w['fn']['leg']
        and 'amonly-lo' not in w['fn']['leg'] and (w['fn']['stored'] or {}).get('mode') == 'fixed' and w['backP']['range'] == 'fixed')
    nc = res['newCase']
    chk(f'J26 새 케이스 (새 state · 같은 저장) — 같은 눈금 (고정 0 … 2.5) ({nc["range"]} · {nc["st"].get("lo")} … {nc["st"].get("hi")})',
        nc['range'] == 'fixed' and nc['st'].get('lo') == 0 and nc['st'].get('hi') == 2.5 and nc['st'].get('lin') is True)
    npf = res['noPref']
    chk('J27 P_ref 없음 → AM 기본색 · 사유 (캐시 스키마 15) · 칠하지 않는다', set(npf['cols']) == {0x888888} and '15' in npf['leg']
        and '칠하지 않' in npf['leg'], npf['leg'][:300])
    se = res['se']
    chk(f'J28 SE 만 기본 (저장 없음) — ui = lw_p · 고정 · 벽 ({se["ui"]}) · AM 숨김 {se["amVis"]} · SE 보임 · 불투명 {se["seMat"]}',
        se['ui'] == {'metric': 'lw_p', 'range': 'fixed', 'wall': True} and se['amVis'] == [False, False] and se['seVis'] is True
        and se['seMat'] == [1, False] and se['exOk'] is True and se['exN'] == len(SE_IDS))
    chk(f'J29 SE 색 = σ_VM ÷ P_ref 선형 jet 0 … 3 (자름) · 벽 접촉 SE {se["wall"]} = 회색 · 접촉 없는 SE 30 (σ = 0) = 맨 아래 색 · 수 '
        f'({se["st"]})', se['got'] == se['want'] and se['wall'] == [23, 31, 32] and se['st'].get('nWall') == 3
        and se['st'].get('nColored') == len(SE_IDS) - 3 and se['st'].get('nZero') == 1 and se['st'].get('lin') is True)
    ls = se['leg']
    chk('J30 SE 범례 — SE 만 · AM 숨김 · P_ref = ⟨σzz⟩ 상자 평균 = 판 압력 (MPa) · 고정 0 … 3 (선형 · AM 만 보기와 같은 값) · 벽 접촉 회색 조작 · '
        '컬러바 단추 · 유효 4 자리',
        all(x in ls for x in ('SE 만', 'AM 숨김', 'P_ref', '⟨σzz⟩ 상자 평균', '판 압력', 'MPa', '색 범위 = 고정', '선형', 'AM 만 보기와 같은',
                              'id="seonly-wall"', '벽 접촉 입자 회색', 'id="seonly-cbar"', '유효 4 자리', 'id="seonly-lo"', 'id="seonly-hi"')),
        ls[:600])
    sl = res['seLog']
    chk(f'J31 SE log (p5–p95) — 벽 뺀 v > 0 의 가장 가까운 순위 · σ = 0 = 값 없음 (어두운 회색) · 벽 회색 ({sl["st"]})',
        sl['got'] == sl['want'] and 'lin' not in sl['st'] and sl['st'].get('nNoValue') == 1)
    sw = res['seLw']
    chk(f'J32 SE σ_VM / ⟨σ_VM⟩ — 분모 = am.lw_mean_all_MPa (AM 만 보기와 같은 전 입자 평균) ({sw["v34"]} · {sw["want34"]})',
        sw['ok'] is True and rel(sw['v34'], sw['want34']) < 1e-15 and '⟨σ_VM⟩' in str(sw['label']))
    ss, sg = res['seSpec'] or {}, res['seSpecLog'] or {}
    chk(f'J33 SE 컬러바 — SE only · σ_VM / P_ref · 눈금 0 · 1 · 2 · 3 · log 판 = σ_VM / ⟨σ_VM⟩ ({ss.get("title")})',
        ss.get('map') == 'jet' and 'SE only' in str(ss.get('title')) and 'σ_VM / P_ref' in str(ss.get('title'))
        and [t['label'] for t in ss.get('ticks') or []] == ['0', '1', '2', '3'] and 'SE only' in str(sg.get('title'))
        and '⟨σ_VM⟩' in str(sg.get('title')) and 'Log colour scale' in str(sg.get('sub')))
    td = res['td']
    chk(f'J34 SE 만 걷기 — SE 보이기 = 체크박스 (끔) · 반투명 OPA.SE · 기본색 ({td})',
        td['seVis'] is False and td['seMat'] == [0.85, True] and td['cols'] == [0xf5e6a3])
    ns = res['noSe']
    chk('J35 SE 자료 없음 (옛 캐시) → 사유 (캐시 스키마 15) · SE 기본색 · AM 숨김', '15' in ns['leg'] and ns['cols'] == [0xf5e6a3]
        and ns['amVis'] == [False, False], ns['leg'][:300])
    chk(f'J36 깨진 id 구간 (값 수 ≠ id 수) → ok false + 사유 ({(res["brk"] or {}).get("reason")})',
        (res['brk'] or {}).get('ok') is False and bool((res['brk'] or {}).get('reason')))
    try:
        wa, ws = js_fn(js, '_amOnlyWireLegend'), js_fn(js, '_seOnlyWireLegend')
    except (ValueError, AssertionError):
        wa = ws = ''
    chk('J37 배선 — SE 조작 (seonly-metric · range · wall · lo · hi · cbar) · 컬러바 파일 이름에 양 · 고정',
        all(f"'seonly-{k}'" in ws for k in ('metric', 'range', 'wall', 'lo', 'hi', 'cbar'))
        and all(f"'amonly-{k}'" in wa for k in ('lo', 'hi')) and 'colorbar_se_only_' in ws and "'_fixed'" in ws + wa)


# ══════════════════════════════════════════════════════════════════════════════
#  [JP] ★ 11-02 (같은 묶음) 접촉마다 압력 — 뷰어 (node · THREE 흉내로 진짜 cap 그리기를 돌린다)
#    자료 = 10-07 합성 침대 (test_viewer_load_view.synth_bed) — AM–SE 압축 3–17 = 150 · 1–11 = 80 MPa · AM–AM 1–2 · 4–5 = 100 MPa
# ══════════════════════════════════════════════════════════════════════════════
JP_NAMES = JS_NAMES + ('renderAmOnlyContactCaps', 'netCurrentPct', 'amOnlyContactPressureColorbarSpec')
JP_SHIM = r"""
const THREE = {
  Color: class { constructor(h) { this.hex = (h === undefined ? 0 : h); } setHex(h) { this.hex = h; return this; } },
  SphereGeometry: class { constructor() { this.attributes = { position: { count: 3, array: [0, 1, 0, 0.3, 0.97, 0, 0, 0.96, 0.3] } }; }
                          setAttribute(k, v) { this.attributes[k] = v; } dispose() {} },
  BufferAttribute: class { constructor(a, n) { this.array = a; this.itemSize = n; } },
  Group: class { constructor() { this.children = []; this.userData = {}; } add(c) { this.children.push(c); }
                 traverse(fn) { fn(this); this.children.forEach(c => fn(c)); } },
  MeshBasicMaterial: class { constructor(o) { Object.assign(this, o); } dispose() {} },
  InstancedMesh: class { constructor(g, m, n) { this.geometry = g; this.material = m; this.count = n; this.cols = new Array(n).fill(null);
                         this.instanceMatrix = {}; this.instanceColor = {}; this.isInstancedMesh = true; }
                         setMatrixAt() {} setColorAt(i, c) { this.cols[i] = c.hex; } dispose() {} },
  Vector3: class { constructor(x, y, z) { this.x = x || 0; this.y = y || 0; this.z = z || 0; } set(x, y, z) { this.x = x; this.y = y; this.z = z; return this; }
                   lengthSq() { return this.x * this.x + this.y * this.y + this.z * this.z; } normalize() { return this; } },
  Quaternion: class { setFromUnitVectors() { return this; } },
  Matrix4: class { compose() { return this; } },
  FrontSide: 0,
};
const EL = {};
const LEG = { innerHTML: '', querySelector: sel => (EL[sel] || (EL[sel] = { sel: sel, h: {}, addEventListener(ev, fn) { this.h[ev] = fn; } })) };
const document = { getElementById: id => (id === 'view-mode-legend' ? LEG : null), querySelector: () => null };
const EXPORTS = [];
function exportColorbarPNG(spec, fname) { EXPORTS.push({ fname: fname, title: spec.title }); }
function mkMesh(parts) {
  return { visible: true, material: { opacity: 0.85, transparent: true }, instanceColor: { needsUpdate: false },
           userData: { particles: parts }, cols: parts.map(() => null), setColorAt(i, c) { this.cols[i] = c.hex; } };
}
function fire(sel, ev, value) { const e = EL[sel]; if (!e || !e.h[ev]) return false; e.h[ev]({ target: { value: value } }); return true; }
"""


def section_js_pressure(tmp):
    print('[JP] 접촉마다 압력 (AM–SE · AM–AM · MPa) — 뷰어 양 · 고정 0 … 800 (선형) · 진짜 cap 그리기 · 힘 양 그대로 (node)')
    import viewer3d_data as V
    from test_viewer_load_view import synth_bed, write_bed as write_bed_lv, RAD as RAD_LV, TYPE as TYPE_LV
    P, rows = synth_bed()
    d = os.path.join(tmp, 'jp_synth')
    write_bed_lv(d, P, rows)
    lv = V.particle_load_view_for_case(d, TM, SCALE)
    js = open(VIEWER_JS, encoding='utf-8').read()
    parts, miss = [], []
    for n in JS_CONSTS:
        try:
            parts.append(js_const(js, n))
        except (ValueError, AssertionError):
            miss.append(n)
    for n in JP_NAMES:
        try:
            parts.append(js_fn(js, n))
        except (ValueError, AssertionError):
            miss.append(n)
    if not chk(f'JP0 viewer3d.js 에서 함수 · 상수를 잘라 냈다 (없음 {miss})', not miss):
        return
    parts_js = [{'id': i, 'type': TM[TYPE_LV[i]], 'r': RAD_LV[i] * SCALE} for i in sorted(P)]
    idx = {i: {'x': P[i][0] * SCALE, 'y': P[i][1] * SCALE, 'z': P[i][2] * SCALE, 'r': RAD_LV[i] * SCALE} for i in P}
    script = JP_SHIM + '\n'.join(parts) + '\n' + r"""
const LV = __LV__, PARTS = __PARTS__, IDX = __IDX__;
const out = {};
function mkState() {
  const by = t => PARTS.filter(p => p.type === t);
  return { data: { aux: { load_view: LV } }, meshes: { AM_P: mkMesh(by('AM_P')), AM_S: mkMesh(by('AM_S')), SE: mkMesh(by('SE')) },
           idIndex: IDX, scene: { add(g) { this.g = g; }, remove() {} } };
}
const capCols = s => (s.amOnlyCapGroup && s.amOnlyCapGroup.children[0]) ? s.amOnlyCapGroup.children[0].cols.slice() : null;
out.kinds = ['lw', 'lw_p', 'fn', 'contact', 'contact_se', 'contact_p', 'contact_se_p'].map(m => amOnlyContactKind(m));
out.cap = ['lw', 'lw_p', 'fn', 'contact', 'contact_se', 'contact_p', 'contact_se_p'].map(m => lwFixedCapable(m));
out.clSP = loadViewAmContacts(LV, 'contact_se_p', 'all');
out.clS = loadViewAmContacts(LV, 'contact_se', 'all');
out.clAP = loadViewAmContacts(LV, 'contact_p', 'all');
out.clSP1 = loadViewAmContacts(LV, 'contact_se_p', 1);
const old14 = JSON.parse(JSON.stringify(LV));
['contacts', 'contacts_se'].forEach(k => { const c = old14.am[k]; c.fields = c.fields.slice(0, 7); c.rows = c.rows.map(r => r.slice(0, 7)); delete c.p_MPa_stats; });
out.clOldP = loadViewAmContacts(old14, 'contact_se_p', 'all');
out.clOldF = loadViewAmContacts(old14, 'contact_se', 'all');
out.limSP = lwFixedLim({ metric: 'contact_se_p' });
out.limAP = lwFixedLim({ metric: 'contact_p' });
out.rSPall = amOnlyContactRange(out.clSP, 'p5p95', 'all');
out.rSPallMM = amOnlyContactRange(out.clSP, 'minmax', 'all');
out.rSPdrawnMM = amOnlyContactRange(out.clSP, 'minmax', 'drawn');
// AM–SE 압력 · 고정 0 … 800 (선형) — 진짜 cap 그리기
const s1 = mkState();
s1._amOnlyUi = { metric: 'contact_se_p', range: 'fixed', wall: true, top: 'all', basis: 'drawn' };
applyAmOnlyView(s1);
out.capsSP = { cols: capCols(s1), st: Object.assign({}, s1._amOnlyLast.st), leg: LEG.innerHTML, amSE: s1.meshes.SE.visible,
               amCols: s1.meshes.AM_S.cols.slice() };
fire('#amonly-cbar', 'click');
// AM–SE 힘 (옛 양) · 최소–최대 log — 옛 알고리즘 (그린 압축 |Fn| 의 최소–최대 · 약한 것 먼저 · log jet)
const s2 = mkState();
s2._amOnlyUi = { metric: 'contact_se', range: 'minmax', wall: true, top: 'all', basis: 'drawn' };
applyAmOnlyView(s2);
const r2 = amOnlyContactRange(out.clS, 'minmax', 'drawn');
out.capsS = { cols: capCols(s2), want: out.clS.rows.map(r => r.f).sort((a, b) => a - b).map(f => jetColor(netCurrentT(f, r2[0], r2[1]))),
              st: Object.assign({}, s2._amOnlyLast.st), leg: LEG.innerHTML };
fire('#amonly-cbar', 'click');
// AM–AM 압력 · 최소–최대 log (넷 다 100 MPa → 한 점 범위 = 맨 위 색)
const s3 = mkState();
s3._amOnlyUi = { metric: 'contact_p', range: 'minmax', wall: true, top: 'all', basis: 'drawn' };
applyAmOnlyView(s3);
out.capsAP = { cols: capCols(s3), st: Object.assign({}, s3._amOnlyLast.st), leg: LEG.innerHTML };
// 옛 캐시 (스키마 14 · 압력 열 없음) — 압력 양 = 사유 · 칠하지 않는다
const s4 = mkState(); s4.data.aux.load_view = old14;
s4._amOnlyUi = { metric: 'contact_se_p', range: 'fixed', wall: true, top: 'all', basis: 'drawn' };
applyAmOnlyView(s4);
out.capsOld = { cols: capCols(s4), leg: LEG.innerHTML };
// AM–AM 압력 · 고정 0 … 90 (이 화면에서 고친 값) — 넷 다 100 MPa = hi 위 (맨 위 색으로 잘림) · 범례가 범위 밖 수를 적는다
const s5 = mkState(); s5._lwRange = { lim: { contact_p: [0, 90] }, mode: { contact_p: 'fixed' } };
s5._amOnlyUi = { metric: 'contact_p', range: 'fixed', wall: true, top: 'all', basis: 'drawn' };
applyAmOnlyView(s5);
out.capsAPclip = { cols: capCols(s5), st: Object.assign({}, s5._amOnlyLast.st), leg: LEG.innerHTML };
out.specSP = amOnlyColorbarSpec(LV, { metric: 'contact_se_p', range: 'fixed', wall: true, top: 'all', basis: 'drawn' }, 0, 800, out.clSP);
out.specS = amOnlyColorbarSpec(LV, { metric: 'contact_se', range: 'minmax', wall: true, top: 'all', basis: 'drawn' }, r2[0], r2[1], out.clS);
out.exports = EXPORTS;
out.jet = { a: jetColor(80 / 800), b: jetColor(150 / 800), one: jetColor(1) };
console.log(JSON.stringify(out));
""".replace('__LV__', json.dumps(lv, ensure_ascii=False)).replace('__PARTS__', json.dumps(parts_js)).replace('__IDX__', json.dumps(idx))
    res = run_node(script)
    if not chk('JP1 node 실행', res is not None):
        return
    kinds = res['kinds']
    chk(f'JP2 양 갈래 — 접촉마다 넷 (contact · contact_se · contact_p · contact_se_p) · AM–SE 둘 · 압력 둘 · 고정 범위 = lw · lw_p · 압력 둘 ({kinds} · {res["cap"]})',
        kinds[:3] == [None, None, None] and kinds[3] == {'se': False, 'press': False} and kinds[4] == {'se': True, 'press': False}
        and kinds[5] == {'se': False, 'press': True} and kinds[6] == {'se': True, 'press': True}
        and res['cap'] == [True, True, False, False, False, True, True])
    sp, sf = res['clSP'] or {}, res['clS'] or {}
    rsp = [(r['a'], r['b'], r['f'], r['fn']) for r in sp.get('rows') or []]
    chk(f'JP3 AM–SE 압력 목록 — 그릴 행 = 힘 양과 같은 행 (압축 · |Fn| 큰 순 · 같은 방향) · 색 값 f = p_MPa (150 · 80 MPa) · fn = |Fn| µN ({rsp})',
        sp.get('ok') is True and rsp == [(3, 17, 150.0, 6.0), (1, 11, 80.0, 4.0)]
        and [(r['a'], r['b'], r['u']) for r in sp.get('rows') or []] == [(r['a'], r['b'], r['u']) for r in sf.get('rows') or []]
        and sp.get('capsPerContact') == 1 and sp.get('nComp') == 2 and abs((sp.get('share') or 0) - 1.0) < 1e-12 and sp.get('press') is True)
    q = sp.get('q') or {}
    chk(f'JP4 압력 백분위 (범위 기준 = 압축 전체) = 서버 p_MPa_stats (p5 · p95 · 최소 80 · 최대 150) · 평균 115 · 중앙 115 ({q})',
        q.get('p5') == 80.0 and q.get('p95') == 80.0 and q.get('min') == 80.0 and q.get('max') == 150.0 and q.get('mean') == 115.0
        and q.get('median') == 115.0 and sp.get('fSent') == [150.0, 80.0])
    ap = res['clAP'] or {}
    chk(f'JP5 AM–AM 압력 목록 — 1–2 · 4–5 = 100 MPa · cap 둘 (두 AM 표면) ({[(r["a"], r["b"], r["f"]) for r in ap.get("rows") or []]})',
        ap.get('ok') is True and [(r['a'], r['b'], r['f']) for r in ap.get('rows') or []] == [(1, 2, 100.0), (4, 5, 100.0)]
        and ap.get('capsPerContact') == 2 and (res['clSP1'] or {}).get('nDrawn') == 1)
    chk(f'JP6 옛 캐시 (스키마 14 · 압력 열 없음) → 압력 양 ok false + 사유 (캐시 스키마 15) · 힘 양은 그대로 산다 ({(res["clOldP"] or {}).get("reason")})',
        (res['clOldP'] or {}).get('ok') is False and '15' in str((res['clOldP'] or {}).get('reason'))
        and (res['clOldF'] or {}).get('ok') is True and len((res['clOldF'] or {}).get('rows') or []) == 2)
    chk(f'JP7 고정 범위 기본 (압력) = 0 … 800 MPa (AM–SE · AM–AM) ({res["limSP"]} · {res["limAP"]})', res['limSP'] == [0, 800] and res['limAP'] == [0, 800])
    a, b, c_ = res['rSPall'], res['rSPallMM'], res['rSPdrawnMM']
    chk(f'JP8 압력 log 범위 — 압축 전체 기준 = 서버 백분위 (p5–p95 = log 80 · 80 · 최소–최대 = log 80 · 150) · 그린 것 기준 = 그린 값 ({a} · {b} · {c_})',
        bool(a) and abs(a[0] - math.log10(80)) < 1e-12 and abs(a[1] - math.log10(80)) < 1e-12 and bool(b)
        and abs(b[0] - math.log10(80)) < 1e-12 and abs(b[1] - math.log10(150)) < 1e-12 and bool(c_) and abs(c_[1] - math.log10(150)) < 1e-12)
    cs1 = res['capsSP']
    want1 = [res['jet']['a'], res['jet']['b']]
    chk(f'JP9 AM–SE 압력 cap (진짜 그리기 · 고정 0 … 800 선형) = jet(80/800) · jet(150/800) (약한 것 먼저) · AM 기본색 · SE 숨김 ({cs1["cols"]} · {want1})',
        cs1['cols'] == want1 and cs1['st'].get('lin') is True and cs1['st'].get('lo') == 0 and cs1['st'].get('hi') == 800
        and cs1['st'].get('nCaps') == 2 and cs1['amSE'] is False and set(cs1['amCols']) == {0x888888})
    lg = cs1['leg']
    chk('JP10 범례 (AM–SE 압력 · 고정) — 접촉 압력 |Fn|/A · MPa · 고정 0 … 800 · 선형 · 평균 · 중앙 (압축 전체) · k/(2πR*) · 하중이 아니다 · lo · hi 입력 · 고정 선택',
        all(x in lg for x in ('접촉 압력', '|Fn|/A', 'MPa', '고정 0 … 800', '선형', '평균 115', '중앙 115', 'k/(2πR*)', '하중이 아니다',
                              'id="amonly-lo"', 'id="amonly-hi"'))
        and re.search(r'<option value="fixed" selected>', lg) is not None and re.search(r'<option value="contact_se_p" selected>', lg) is not None,
        lg[:700])
    chk('JP11 양 고르기에 압력 둘 — AM–AM 접촉마다 (접촉 압력 MPa) · AM–SE 접촉마다 (접촉 압력 MPa)',
        re.search(r'<option value="contact_p"[^>]*>AM–AM 접촉마다 \(접촉 압력 MPa\)</option>', lg) is not None
        and re.search(r'<option value="contact_se_p"[^>]*>AM–SE 접촉마다 \(접촉 압력 MPa\)</option>', lg) is not None)
    cs2 = res['capsS']
    chk(f'JP12 힘 양 (AM–SE 접촉마다 µN) 그대로 — cap 색 = 옛 알고리즘 (그린 |Fn| 최소–최대 · log jet · 약한 것 먼저) · st 에 lin 없음 · 범례에 압력 한정어 없음 '
        f'({cs2["cols"]} · {cs2["want"]})', cs2['cols'] == cs2['want'] and 'lin' not in cs2['st']
        and '법선력 |Fn| · µN' in cs2['leg'] and 'k/(2πR*)' not in cs2['leg'] and 'value="fixed"' not in cs2['leg'])
    cs3 = res['capsAP']
    chk(f'JP13 AM–AM 압력 cap (log 최소–최대 · 넷 다 100 MPa = 한 점 범위 → 맨 위 색) · cap 4 개 ({cs3["cols"]})',
        cs3['cols'] == [res['jet']['one']] * 4 and cs3['st'].get('nCaps') == 4 and 'lin' not in cs3['st'])
    co = res['capsOld']
    chk('JP14 옛 캐시 압력 양 → cap 없음 · 사유 (캐시 스키마 15) · 칠하지 않는다', co['cols'] is None and '15' in co['leg'], co['leg'][:300])
    ss, sfs = res['specSP'] or {}, res['specS'] or {}
    chk(f'JP15 컬러바 (AM–SE 압력 · 고정) — 제목 contact pressure |Fn|/A (MPa) · 눈금 0 · 200 · 400 · 600 · 800 (선형) · 부제 Linear · k/(2πR*) · not a load '
        f'({ss.get("title")})', 'contact pressure |Fn|/A (MPa)' in str(ss.get('title')) and 'AM–SE' in str(ss.get('title'))
        and [t['label'] for t in ss.get('ticks') or []] == ['0', '200', '400', '600', '800'] and 'Linear colour scale' in str(ss.get('sub'))
        and 'k/(2πR*)' in str(ss.get('sub')) and 'not a load' in str(ss.get('sub')))
    chk(f'JP16 힘 컬러바 글 그대로 — 제목 AM only — AM–SE contact normal force |Fn| (µN) · 끝 Log colour scale. ({sfs.get("title")})',
        sfs.get('title') == 'AM only — AM–SE contact normal force |Fn| (µN)' and str(sfs.get('sub')).endswith('Log colour scale.')
        and 'Colour range = min–max of the 2 drawn contacts (top 2 by |Fn| of 2 compressive; loaded rows capped at' in str(sfs.get('sub')))
    cc = res['capsAPclip']
    chk(f'JP18 AM–AM 압력 · 고정 0 … 90 (이 화면 값) — 넷 다 100 MPa → cap 4 개 = 맨 위 색 (잘림) · 범례 = 범위 밖 hi 위 2 개 접촉 · lo 아래 0 '
        f'(AM–AM 압력은 실침대 ≈ 4000 MPa — 고정 기본 0 … 800 이면 다 잘린다는 것을 화면이 말한다) ({cc["cols"]})',
        cc['cols'] == [res['jet']['one']] * 4 and cc['st'].get('lin') is True and cc['st'].get('hi') == 90
        and '범위 밖' in cc['leg'] and 'hi 90 MPa 위 2 개' in cc['leg'] and 'lo 0 MPa 아래 0 개' in cc['leg'], cc['leg'][:900])
    chk('JP19 범위 안이면 (AM–SE 압력 · 고정 0 … 800 · 80 · 150 MPa) 범위 밖 줄 = 0 · 0 개 (그대로 적는다)',
        'hi 800 MPa 위 0 개' in res['capsSP']['leg'] and 'lo 0 MPa 아래 0 개' in res['capsSP']['leg'])
    ex = [e['fname'] for e in res['exports']]
    chk(f'JP17 컬러바 파일 이름 — 압력 고정 = …_contact_se_p_topall_drawn_fixed.png · 힘 = 옛 꼴 …_contact_se_topall_drawn.png ({ex})',
        ex == ['colorbar_am_only_contact_se_p_topall_drawn_fixed.png', 'colorbar_am_only_contact_se_topall_drawn.png'])


# ══════════════════════════════════════════════════════════════════════════════
#  [P] webapp/app.py — 발사 뒤 패치 + 캐시 스키마 15
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
meta = {'name': 'lwp_col', 'type_map': '1:AM_P,2:AM_S,3:SE', 'scale': 1000, 'status': 'done', 'mode': 'standard'}
cid = '261102_000001_lwpcol'
os.makedirs(os.path.join(up, cid))
json.dump(meta, open(os.path.join(up, cid, 'meta.json'), 'w'))
shutil.copytree(case_src, os.path.join(rs, cid))
out = {}
def lv_of(url):
    j = c.get(url).get_json(silent=True) or {}
    return (j.get('aux') or {}).get('load_view')
cache = os.path.join(rs, cid, 'viewer_aux.json')
out['live1'] = lv_of(f'/results/{cid}/3d-data')
blob = json.load(open(cache)) if os.path.exists(cache) else {}
out['cache_schema'] = blob.get('_schema')
out['cache_has'] = sorted(k for k in ('p_ref', 'se') if k in (blob.get('load_view') or {}))
out['live2'] = lv_of(f'/results/{cid}/3d-data')
blob['_schema'] = 14
lv14 = json.loads(json.dumps(blob.get('load_view') or {}))
lv14.pop('p_ref', None)
lv14.pop('se', None)
blob['load_view'] = lv14
json.dump(blob, open(cache, 'w'))
out['live_14'] = lv_of(f'/results/{cid}/3d-data')
out['cache_schema_after14'] = json.load(open(cache)).get('_schema')
af = os.path.join(ar, 'lwp_case')
shutil.copytree(case_src, af)
json.dump(meta, open(os.path.join(af, 'meta.json'), 'w'))
out['arch1'] = lv_of('/archive/results/lwp_case/3d-data')
out['arch2'] = lv_of('/archive/results/lwp_case/3d-data')
print('@@JSON@@' + json.dumps(out))
'''


def section_app(tmp):
    print('[P] webapp/app.py — 발사 뒤 패치 적용 · 캐시 스키마 15 · /3d-data 에 p_ref · se')
    src = open(APP, encoding='utf-8').read()
    chk(f'P1 발사 뒤 패치가 app.py 에 들어갔다 — particle_load_view_for_case 호출 둘 (live · archive) ({src.count("particle_load_view_for_case(")})',
        src.count('particle_load_view_for_case(') == 2 and src.count("'load_view': {},") == 2)
    n15 = len(re.findall(r"_schema'\)\s*==\s*15\b", src))
    w15 = len(re.findall(r"\['_schema'\]\s*=\s*15\b", src))
    n_old = sum(len(re.findall(rf"_schema'\)\s*==\s*{v}\b", src)) + len(re.findall(rf"\['_schema'\]\s*=\s*{v}\b", src)) for v in (12, 13, 14))
    chk(f'P2 두 경로 캐시 스키마 15 (load_view 에 p_ref · se) 읽기 · 쓰기 · 12 · 13 · 14 는 남지 않는다 ({n15} · {w15} · {n_old})',
        n15 == 2 and w15 == 2 and n_old == 0)
    P, rows = column_bed()
    case_src = os.path.join(tmp, 'p_case')
    write_bed(case_src, P, rows)
    drv = os.path.join(tmp, 'driver_lwp.py')
    with open(drv, 'w', encoding='utf-8') as f:
        f.write(DRIVER)
    work = os.path.join(tmp, 'p_work')
    env = dict(os.environ)
    env.pop('PYTHONPATH', None)
    r = subprocess.run([sys.executable, drv, ROOT, work, case_src], capture_output=True, text=True, timeout=600, env=env, cwd=tmp)
    m = re.search(r'@@JSON@@(.*)$', r.stdout, re.M)
    if not chk(f'P3 app 실행 (rc {r.returncode})', r.returncode == 0 and m is not None, (r.stderr or r.stdout)[-800:]):
        return
    out = json.loads(m.group(1))
    l1 = out.get('live1') or {}
    want = pref_hand(P, rows)
    chk(f'P4 live /3d-data → aux.load_view.p_ref (OK · 손 계산 값) · se (SE {len(SE_IDS)} 값 · id 구간)',
        (l1.get('p_ref') or {}).get('status') == 'OK' and rel((l1.get('p_ref') or {}).get('MPa'), want) < 1e-9
        and len((l1.get('se') or {}).get('lw_vm_MPa') or []) == len(SE_IDS) and (l1.get('se') or {}).get('id_runs') == [[10, 14], [30, 5]])
    chk(f'P5 캐시 = 스키마 15 · load_view 에 p_ref · se ({out.get("cache_schema")} · {out.get("cache_has")})',
        out.get('cache_schema') == 15 and out.get('cache_has') == ['p_ref', 'se'])
    chk('P6 두 번째 요청 (캐시 HIT) 도 같은 load_view (live)', bool(l1) and out.get('live2') == l1)
    chk(f'P7 옛 캐시 (스키마 14 · load_view 에 p_ref · se 없음 — 10-08 판 패치) → 다시 계산 · p_ref · se 산다 · 캐시 = 15 '
        f'({out.get("cache_schema_after14")})', out.get('live_14') == l1 and out.get('cache_schema_after14') == 15)
    a1, a2 = out.get('arch1') or {}, out.get('arch2') or {}
    chk('P8 archive 경로도 load_view 에 p_ref · se (첫 요청 = 계산 · 캐시 HIT = 같은 값)',
        (a1.get('p_ref') or {}).get('status') == 'OK' and bool((a1.get('se') or {}).get('lw_vm_MPa')) and a2 == a1)


def section_registration():
    print('[X] check_all 배선')
    s = open(CHECK_ALL, encoding='utf-8').read()
    chk('X1 scripts/check_all.sh 가 이 시험을 돈다', 'webapp/test_viewer_lw_pnorm.py' in s)


def main():
    tmp = tempfile.mkdtemp(prefix='viewer_lwp_')
    try:
        for k, v in (('WEBAPP_RESULTS_FOLDER', 'results'), ('WEBAPP_UPLOAD_FOLDER', 'uploads'),
                     ('WEBAPP_ARCHIVE_FOLDER', 'archive'), ('WEBAPP_MPM_LAB_FOLDER', 'mpm_lab')):
            os.environ[k] = os.path.join(tmp, v)
            os.makedirs(os.environ[k], exist_ok=True)
        lv, P, ref = None, None, None
        try:
            lv, P, _rows, ref = section_pref(tmp)
        except Exception as e:                                   # noqa: BLE001 — 옛 코드에서도 나머지 절을 돈다
            chk('section_pref 실행', False, f'{type(e).__name__}: {e}')
        try:
            section_se(tmp, lv, ref)
        except Exception as e:                                   # noqa: BLE001
            chk('section_se 실행', False, f'{type(e).__name__}: {e}')
        try:
            section_kg50(tmp)
        except Exception as e:                                   # noqa: BLE001
            chk('section_kg50 실행', False, f'{type(e).__name__}: {e}')
        try:
            section_js(tmp, lv, P or column_bed()[0])
        except Exception as e:                                   # noqa: BLE001
            chk('section_js 실행', False, f'{type(e).__name__}: {e}')
        try:
            section_js_pressure(tmp)
        except Exception as e:                                   # noqa: BLE001
            chk('section_js_pressure 실행', False, f'{type(e).__name__}: {e}')
        try:
            section_app(tmp)
        except Exception as e:                                   # noqa: BLE001
            chk('section_app 실행', False, f'{type(e).__name__}: {e}')
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
