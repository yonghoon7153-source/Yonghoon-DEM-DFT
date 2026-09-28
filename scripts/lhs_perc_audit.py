#!/usr/bin/env python3
"""lhs_perc_audit.py — LHS 퍼콜레이션 묶음 (②) **읽기 전용** 점검 (J20-b · 1저자 비준 대기).

왜 — 인계표의 ② 열 (`percolation_pct` · `n_components` · `n_large_components` · `electronic_active_fraction` ·
`electronic_percolating_fraction` · `se_se_cn_*_perc`) 은 웹앱의 **경계 규칙**으로 정해진다 — 바닥 = z ≤ 2·r_i (바닥 벽 z = 0 을 암묵
가정) · 위 = z ≥ plate_z − 2·r_i.  그런데 어느 한쪽 밴드에 입자가 3 개 미만이면 코드가 **조용히** 밴드를 바꾼다 (L1 = plate_z 의
15 %/85 % · L2 = 관측 z-범위의 15 %/85 %) 하고, 어느 규칙이 쓰였는지 **산출물 어디에도 남기지 않는다** (`dem_analysis_core.calc_percolation` ·
`network_conductivity.build_network`).  같은 이름의 열이 케이스마다 다른 정의로 채워질 수 있다 ⇒ 값을 뽑기 전에 케이스마다 **어느 규칙이
발동하는가** 를 원자료에서 센다.  **인계 값은 만들지 않는다** (값은 웹앱 정본 함수를 그대로 불러 재현 대조에만 쓴다).

케이스마다 (코호트 봉인 파일 — 수확과 같은 atom · contact · 같은 step mesh · 덱):
  ① 프레임 수 (atom `ITEM: TIMESTEP` · contact `ITEM: ENTRIES`) · 원자에 없는 id 를 가진 접촉 행 (웹앱은 조용히 버린다)
  ② 바닥 벽 = 0 확인 (`lhs_descriptor_harvest.check_deck_floor` — 웹앱은 확인 없이 z = 0 을 쓴다)
  ③ ★ **경계 규칙 재현** — SE (이온 · `calc_percolation`) · AM (전자 · `build_network`) 각각 L0 → L1 → L2 중 어느 단계가 쓰였는지 ·
     L0 밴드 인원 · 쓰인 밴드 인원 · bottom∩top 겹침 (겹친 입자는 자기 성분을 통째로 "관통" 으로 만든다).
     재현 값은 웹앱 정본 (`calc_percolation` · `calc_se_se_cn` · `build_network` + `run_decomposition` 의 성분 셈) 과 **케이스마다 대조**한다 —
     다르면 재현이 틀린 것이므로 FLAG (내 판독을 정본이 검증한다).
  ④ 교차 대조 2×2 — 접촉 원천 {덤프 행, 기하 재계수 (`lhs_perc_extract._pairs_within`)} × 경계 규칙 {웹앱 밴드, 수확기 밴드}.
     AM: 수확기 정본 `lhs_perc_extract.percolation` (고체 외피 슬래브 t = r_AM,max · 폴백 없음) ↔ 웹앱 전자 관통.
     SE: 수확기 벽 밴드 (`tortuosity_se` 의 `wall_n_span_components` — 벽 z = 0 · 플래튼 · t = r_SE,max) ↔ 웹앱 SE 관통.
     ★ SE 가 단분산이면 웹앱 L0 밴드와 수확기 벽 밴드는 **같은 집합**이다 (z ≤ 2r ⇔ z − r ≤ 0 + r) — 다르면 재현 오류로 FLAG.
     불일치는 '밴드' · '접촉' · '둘 다' 로 귀속한다 (정보 — 결함 판정은 아니다).
  ⑤ 09-15 생산 솔버 legacy 팔 (`docs/data/lhs_percolation_measured_20260915.csv` 의 `ionic_percolates`) 과 대조 (있으면).

출력: <out>/perc_audit.tsv (케이스당 한 행) · perc_audit.json (행 + 요약 + 실행 정보).
rc 0 = 전부 CLEAN · rc 3 = FLAG 케이스가 있다 (보고용 — 인계 열의 정의가 그 케이스에서 명목과 다르다) · rc 2 = 입력 오류.

    python3 scripts/lhs_perc_audit.py --out ~/lhs_perc_audit_$(date +%Y%m%d)        # 코호트 전 건
    python3 scripts/lhs_perc_audit.py --case lhs00_000 --out /tmp/perc_one           # 한 건
    python3 scripts/lhs_perc_audit.py --selftest
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import datetime
import io
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

_SCR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCR))
import lhs_descriptor_harvest as H                      # noqa: E402  같은 읽기 · 같은 규칙 (규율 ①)
import lhs_harvest_batch as HB                          # noqa: E402  코호트 · 경로 치환 · 같은 step 메시
from lhs_perc_extract import (BedRefusal, read_atom_dump, _pairs_within,    # noqa: E402
                              percolation as harv_percolation, AM_LABELS)
import dem_analysis_core as DAC                         # noqa: E402  웹앱 정본 — calc_percolation · calc_se_se_cn
import network_conductivity as NC                       # noqa: E402  웹앱 정본 — build_network (전자망 경계)

SCHEMA = 'lhs_perc_audit/v1'
#: 웹앱 기본값들 — 재현은 이 값을 쓰고, 정본 호출은 기본값 그대로다 (변이 시험 ⑮ 가 둘의 대조를 확인한다)
BOUNDARY_FACTOR = 2.0        # calc_percolation · build_network 의 boundary_factor 기본
MIN_BAND = 3                 # 폴백 문턱: len(bottom) < 3 or len(top) < 3
LARGE_COMP = 10              # n_large_components 의 문턱 (코드 안 상수 · 출처 없음 — 기록만)
WEBAPP_BOX_DEFAULT = 0.05    # input_params.json 이 없을 때 `_get_box_xy` 가 쓰는 상자 (sim) — 배치는 그 파일을 만들지 않는다
SCALE = 1000.0               # sim → µm (parse_liggghts · 수확기 SIM_TO_UM 과 같은 규약)
LEGACY_CSV = _SCR.parent / 'docs' / 'data' / 'lhs_percolation_measured_20260915.csv'
LEVELS = ('L0', 'L1', 'L2')

TSV_COLS = (
    'case', 'status', 'verdict', 'why', 'note', 'design_family', 'n_types', 't_s',
    'atom_frames', 'contact_frames', 'orphan_rows', 'n_rows', 'has_delta_col',
    'floor_z_deck', 'floor_wall_type', 'plate_z_sim', 'thickness_um', 'mesh_pick', 'box_lx', 'box_ly', 'box_is_webapp_default',
    'n_se', 'n_am', 'r_se_classes', 'r_se_max_um', 'r_am_max_um',
    # SE (이온) — 웹앱 calc_percolation 규칙
    'se_level', 'se_n_bot_L0', 'se_n_top_L0', 'se_n_bot', 'se_n_top', 'se_overlap',
    'se_perc_pct', 'se_top_reach_pct', 'se_n_components', 'se_n_isolated', 'se_n_large', 'se_largest_pct',
    'se_edges_dump', 'se_edges_geom', 'se_geom_only', 'se_dump_only',
    'se_perc_webapp_dump', 'se_perc_webapp_geom', 'se_perc_wall_geom', 'se_perc_wall_dump', 'se_wall_n_bot', 'se_wall_n_top',
    'se_wall_band_equal', 'se_xcheck',
    'se_cn_perc', 'se_cn_n_perc', 'se_cn_eff_area_perc', 'se_cn_perc_keys',
    # AM (전자) — 웹앱 build_network 규칙
    'am_level', 'am_n_bot_L0', 'am_n_top_L0', 'am_n_bot', 'am_n_top', 'am_overlap',
    'am_active_frac', 'am_perc_frac', 'am_n_components', 'am_n_isolated',
    'am_edges_dump', 'am_edges_geom', 'am_geom_only', 'am_dump_only', 'am_rows_dropped_zero',
    'am_perc_webapp_dump', 'am_perc_webapp_geom', 'am_perc_harv_geom', 'am_perc_harv_dump',
    'harv_perc', 'harv_n_bot', 'harv_n_top', 'harv_overlap', 'harv_slab_t_um', 'harv_z_lo_um', 'harv_z_hi_um', 'harv_reason',
    'am_xcheck',
    # 재현 대조 · legacy
    'replica_ok', 'replica_why', 'legacy_ionic_percolates', 'legacy_status', 'legacy_agree',
)


# ──────────────────────────────────────────────────────────────────────────────
# 재현 — 웹앱 경계 규칙 · 성분 통계 (정본과 케이스마다 대조한다)
# ──────────────────────────────────────────────────────────────────────────────
def _bands(z, r, plate_z, factor=BOUNDARY_FACTOR, min_band=MIN_BAND):
    """`calc_percolation` / `build_network` 의 경계 규칙을 그대로 — L0 (z ≤ f·r_i · z ≥ plate_z − f·r_i) → 부족하면 L1 (plate_z 의
    15 %/85 %) → 여전히 부족하면 L2 (관측 z-범위의 15 %/85 %).  L1 · L2 는 **두 밴드를 함께** 바꾼다 (한쪽만 모자라도)."""
    z = np.asarray(z, dtype=np.float64)
    r = np.asarray(r, dtype=np.float64)
    n = int(z.size)
    if n == 0:
        return dict(level='NA', bot=np.zeros(0, bool), top=np.zeros(0, bool), n_bot_L0=0, n_top_L0=0, n_bot=0, n_top=0, overlap=0)
    bot0 = z <= r * factor
    top0 = z >= plate_z - r * factor
    lvl, bot, top = 'L0', bot0, top0
    if bot.sum() < min_band or top.sum() < min_band:
        lvl = 'L1'
        bot = z <= plate_z * 0.15
        top = z >= plate_z * 0.85
    if bot.sum() < min_band or top.sum() < min_band:
        lvl = 'L2'
        z_min, z_max = float(z.min()), float(z.max())
        span = z_max - z_min
        bot = z <= z_min + span * 0.15
        top = z >= z_max - span * 0.15
    return dict(level=lvl, bot=bot, top=top, n_bot_L0=int(bot0.sum()), n_top_L0=int(top0.sum()),
                n_bot=int(bot.sum()), n_top=int(top.sum()), overlap=int((bot & top).sum()))


def _graph_stats(n, pairs, bot, top, singletons=True, large=LARGE_COMP):
    """성분 통계.  `singletons=True` = `calc_percolation` (모든 노드를 그래프에 넣는다 — 외톨이도 성분 · 겹친 외톨이는 관통) ·
    `False` = `run_decomposition` 의 전자 셈 (간선이 있는 노드만 `G_active` 에 들어가 외톨이는 active/percolating 에서 빠진다)."""
    n = int(n)
    out = dict(n=n, n_components=0, n_isolated=0, n_large=0, largest_pct=0.0, perc_pct=0.0, active_pct=0.0,
               top_reach_pct=0.0, n_span_components=0, n_edges=int(len(pairs)))
    if n == 0:
        return out
    pairs = np.asarray(pairs, dtype=np.int64).reshape(-1, 2)
    if len(pairs):
        adj = coo_matrix((np.ones(len(pairs)), (pairs[:, 0], pairs[:, 1])), shape=(n, n))
        adj = adj + adj.T
    else:
        adj = coo_matrix((n, n))
    ncomp, comp = connected_components(adj, directed=False)
    sizes = np.bincount(comp, minlength=ncomp)
    bot = np.asarray(bot, bool)
    top = np.asarray(top, bool)
    bot_c = np.zeros(ncomp, bool)
    bot_c[comp[bot]] = True
    top_c = np.zeros(ncomp, bool)
    top_c[comp[top]] = True
    if not singletons:                       # 간선 없는 노드는 G_active 에 없다
        bot_c &= sizes >= 2
        top_c &= sizes >= 2
    span_c = bot_c & top_c
    out.update(n_components=int(ncomp), n_isolated=int((sizes == 1).sum()), n_large=int((sizes >= large).sum()),
               largest_pct=float(sizes.max() / n * 100.0), perc_pct=float(span_c[comp].sum() / n * 100.0),
               active_pct=float(bot_c[comp].sum() / n * 100.0), top_reach_pct=float(top_c[comp].sum() / n * 100.0),
               n_span_components=int(span_c.sum()))
    return out


def _electronic_fractions(net):
    """`network_conductivity.run_decomposition` 의 active/percolating 셈 그대로 (:1101–1120) — 정본 대조용."""
    import networkx as nx
    G = nx.Graph()
    for e in net['edges']:
        G.add_edge(e['id1'], e['id2'])
    n_nodes = len(net['nodes'])
    bottom_reachable, perc_nodes = set(), set()
    for comp in nx.connected_components(G):
        has_bot = len(comp & net['bottom']) > 0
        has_top = len(comp & net['top']) > 0
        if has_bot:
            bottom_reachable |= comp
        if has_bot and has_top:
            perc_nodes |= comp
    return (len(bottom_reachable) / n_nodes if n_nodes else 0.0,
            len(perc_nodes) / n_nodes if n_nodes else 0.0)


def _unique_pairs(a, b):
    if len(a) == 0:
        return np.empty((0, 2), dtype=np.int64)
    lo = np.minimum(a, b)
    hi = np.maximum(a, b)
    return np.unique(np.column_stack([lo, hi]), axis=0)


def _pair_set(pairs):
    return {(int(i), int(j)) for i, j in np.asarray(pairs, dtype=np.int64).reshape(-1, 2)}


def _xcheck(webapp_dump, webapp_geom, other_geom, other_dump):
    """2×2 귀속 — 정본 둘 (webapp_dump · other_geom) 이 같으면 'agree'.  다르면 밴드만 바꿔서 뒤집히면 'band', 접촉 원천만
    바꿔서 뒤집히면 'contact', 그 밖은 'both' (교호)."""
    if webapp_dump == other_geom:
        return 'agree'
    contact_matters = (webapp_dump != webapp_geom) or (other_geom != other_dump)
    band_matters = (webapp_dump != other_dump) or (webapp_geom != other_geom)
    if band_matters and not contact_matters:
        return 'band'
    if contact_matters and not band_matters:
        return 'contact'
    return 'both'


def _read_legacy(path):
    """09-15 legacy 팔 CSV → {case_id: (ionic_percolates: bool|None, ionic_status)}."""
    if not path or not os.path.isfile(path):
        return None
    with open(path, encoding='utf-8') as fh:
        lines = [l for l in fh if not l.startswith('#')]
    out = {}
    for r in csv.DictReader(lines):
        v = (r.get('ionic_percolates') or '').strip()
        out[r['case_id']] = ((True if v == 'True' else False if v == 'False' else None), (r.get('ionic_status') or '').strip())
    return out


# ──────────────────────────────────────────────────────────────────────────────
# 케이스 하나
# ──────────────────────────────────────────────────────────────────────────────
def audit_case(atom_path, contact_path, n_types, mesh_path, deck_path=None, legacy=None, case=None, _replica_factor=BOUNDARY_FACTOR):
    """한 케이스의 ②-묶음 정의 점검 → dict (TSV_COLS 의 키 + 부가 키).  `_replica_factor` 는 변이 시험 전용 (정본은 언제나 기본값)."""
    t0 = time.perf_counter()
    rec = dict(case=case, verdict='', why='', note='', status='OK')
    flags, notes = [], []

    # ① 프레임 · 원자료
    rec['atom_frames'] = int(H.count_blocks(atom_path, 'ITEM: TIMESTEP'))
    rec['contact_frames'] = int(H.count_blocks(contact_path, 'ITEM: ENTRIES'))
    if rec['atom_frames'] != 1 or rec['contact_frames'] != 1:
        flags.append(f"프레임 atom {rec['atom_frames']} · contact {rec['contact_frames']} ≠ 1 (웹앱 파서는 전 프레임을 이어 붙인다 · DESC-06)")
    atoms, box_lo, box_hi, _bc = read_atom_dump(atom_path)
    ids = H._atom_ids(atom_path)
    n = int(atoms['x'].size)
    if ids.size != n or np.unique(ids).size != n:
        raise BedRefusal(f'{atom_path}: id 열 {ids.size} 개 / 고유 {np.unique(ids).size} 개 ≠ 입자 {n} 개')
    labels, tmap = H.phase_labels(atoms['type'], int(n_types))
    se_types = [t for t, l in tmap.items() if l == 'SE']
    am_types = [t for t, l in tmap.items() if l in AM_LABELS]
    is_se = np.asarray([l == 'SE' for l in labels])
    is_am = np.asarray([l in AM_LABELS for l in labels])
    lx = float(box_hi[0] - box_lo[0])
    ly = float(box_hi[1] - box_lo[1])
    rec.update(box_lx=lx, box_ly=ly, box_is_webapp_default=bool(abs(lx - WEBAPP_BOX_DEFAULT) < 1e-12 and abs(ly - WEBAPP_BOX_DEFAULT) < 1e-12),
               n_se=int(is_se.sum()), n_am=int(is_am.sum()), n_types=int(n_types))
    if not rec['box_is_webapp_default']:
        notes.append(f'상자 {lx:.6g}×{ly:.6g} ≠ 웹앱 기본 {WEBAPP_BOX_DEFAULT} (input_params.json 부재 시) — ② 값에는 무영향 · τ 묶음으로 이월')
    r_all = atoms['radius']
    r_se = r_all[is_se]
    r_am = r_all[is_am]
    rec['r_se_classes'] = int(np.unique(np.round(r_se, 12)).size) if r_se.size else 0
    rec['r_se_max_um'] = float(r_se.max() * SCALE) if r_se.size else None
    rec['r_am_max_um'] = float(r_am.max() * SCALE) if r_am.size else None
    if rec['r_se_classes'] > 1:
        notes.append(f"SE 반지름 {rec['r_se_classes']} 계급 — 웹앱 L0 밴드 (2·r_i, 중심) 와 수확기 벽 밴드 (r_max, 표면) 가 같은 집합이 아니다")

    c1, c2, carea, _hd, ex = H.read_contact_dump(contact_path, extra_cols=(H.COL_DELTA,))
    delta = ex[H.COL_DELTA]
    rec['has_delta_col'] = bool(delta is not None)
    if delta is None:
        flags.append('접촉 덤프에 δ 열 (c_cpl[23]) 이 없다 — 웹앱 contacts.csv 의 delta 열이 비어 파이프라인이 선다')
        delta = np.zeros(c1.size)
    rec['n_rows'] = int(c1.size)
    idx_of = {int(i): k for k, i in enumerate(ids.tolist())}
    k1 = np.asarray([idx_of.get(int(i), -1) for i in c1.tolist()], dtype=np.int64)
    k2 = np.asarray([idx_of.get(int(i), -1) for i in c2.tolist()], dtype=np.int64)
    known = (k1 >= 0) & (k2 >= 0)
    rec['orphan_rows'] = int((~known).sum())
    if rec['orphan_rows']:
        flags.append(f"원자에 없는 id 의 접촉 행 {rec['orphan_rows']} (웹앱은 조용히 버린다)")

    # ② 바닥 벽 (웹앱은 확인 없이 z = 0 을 쓴다)
    rec['floor_z_deck'] = rec['floor_wall_type'] = None
    if deck_path and os.path.isfile(deck_path):
        try:
            df = H.check_deck_floor(deck_path)
            rec['floor_z_deck'] = df['z']
            rec['floor_wall_type'] = df['wall_type']
        except BedRefusal as e:
            flags.append(f'덱 바닥 벽 확인 실패 — {e}')
    else:
        flags.append('덱 없음 — 바닥 벽 z 미확인 (웹앱은 z = 0 을 가정한다 · fail-closed)')

    # 플래튼 — 수확과 같은 정의 (꼭짓점 z 평균 · 평판 검사 HND-06)
    plate_z = float(H.plate_z_from_stl(mesh_path))
    rec['plate_z_sim'] = plate_z
    rec['thickness_um'] = plate_z * SCALE

    # 웹앱 입력 모양 — parse_liggghts → atoms.csv / contacts.csv → analyze_contacts.load_*_raw 와 같은 dict
    atoms_d = {int(ids[k]): dict(type=int(atoms['type'][k]), x=float(atoms['x'][k]), y=float(atoms['y'][k]),
                                 z=float(atoms['z'][k]), radius=float(r_all[k])) for k in range(n)}
    contacts_l = [dict(id1=int(c1[k]), id2=int(c2[k]), contact_area=float(carea[k]), delta=float(delta[k])) for k in range(c1.size)]

    replica_bad = []
    z_all = atoms['z']
    xyz = np.column_stack([atoms['x'], atoms['y'], z_all])

    # ③-SE — 웹앱 calc_percolation (정본) · 재현 · 벽 밴드 · 기하
    se_idx = np.flatnonzero(is_se)
    if se_idx.size:
        pos_se = {int(g): k for k, g in enumerate(se_idx.tolist())}   # 전체 색인 → SE 부분 색인
        both_se = known & is_se[np.where(known, k1, 0)] & is_se[np.where(known, k2, 0)]
        dump_se = _unique_pairs(np.asarray([pos_se[int(g)] for g in k1[both_se]], dtype=np.int64),
                                np.asarray([pos_se[int(g)] for g in k2[both_se]], dtype=np.int64))
        geom_se = _pairs_within(xyz[se_idx], r_se, lx, ly, z_pad=float(r_se.max()))
        b = _bands(z_all[se_idx], r_se, plate_z, factor=_replica_factor)
        st_dump = _graph_stats(se_idx.size, dump_se, b['bot'], b['top'], singletons=True)
        st_geom = _graph_stats(se_idx.size, geom_se, b['bot'], b['top'], singletons=True)
        # 수확기 벽 밴드 (tortuosity_se 의 wall_bot/wall_top — 표면 기준 · t = r_SE,max)
        t_se = float(r_se.max())
        wall_bot = (z_all[se_idx] - r_se) <= H.Z_FLOOR + t_se
        wall_top = (z_all[se_idx] + r_se) >= plate_z - t_se
        st_wall_geom = _graph_stats(se_idx.size, geom_se, wall_bot, wall_top, singletons=True)
        st_wall_dump = _graph_stats(se_idx.size, dump_se, wall_bot, wall_top, singletons=True)
        sd, sg = _pair_set(dump_se), _pair_set(geom_se)
        rec.update(se_level=b['level'], se_n_bot_L0=b['n_bot_L0'], se_n_top_L0=b['n_top_L0'], se_n_bot=b['n_bot'], se_n_top=b['n_top'],
                   se_overlap=b['overlap'], se_perc_pct=st_dump['perc_pct'], se_top_reach_pct=st_dump['top_reach_pct'],
                   se_n_components=st_dump['n_components'], se_n_isolated=st_dump['n_isolated'], se_n_large=st_dump['n_large'],
                   se_largest_pct=st_dump['largest_pct'], se_edges_dump=len(sd), se_edges_geom=len(sg),
                   se_geom_only=len(sg - sd), se_dump_only=len(sd - sg),
                   se_perc_webapp_dump=bool(st_dump['perc_pct'] > 0), se_perc_webapp_geom=bool(st_geom['perc_pct'] > 0),
                   se_perc_wall_geom=bool(st_wall_geom['n_span_components'] > 0), se_perc_wall_dump=bool(st_wall_dump['n_span_components'] > 0),
                   se_wall_n_bot=int(wall_bot.sum()), se_wall_n_top=int(wall_top.sum()))
        rec['se_wall_band_equal'] = bool(np.array_equal(wall_bot, b['bot']) and np.array_equal(wall_top, b['top'])) if b['level'] == 'L0' else None
        if b['level'] == 'L0' and rec['r_se_classes'] == 1 and not rec['se_wall_band_equal']:
            replica_bad.append('SE 단분산 · L0 인데 웹앱 밴드 ≠ 수확기 벽 밴드 (같아야 한다)')
        rec['se_xcheck'] = _xcheck(rec['se_perc_webapp_dump'], rec['se_perc_webapp_geom'], rec['se_perc_wall_geom'], rec['se_perc_wall_dump'])
        # 정본 대조
        perc = DAC.calc_percolation(atoms_d, contacts_l, se_types, plate_z, box_x=lx, box_y=ly)
        prod_bot = {int(ids[se_idx[k]]) for k in np.flatnonzero(b['bot'])}
        prod_top = {int(ids[se_idx[k]]) for k in np.flatnonzero(b['top'])}
        for name, mine, theirs in (('percolation_pct', st_dump['perc_pct'], perc['percolation_pct']),
                                   ('top_reachable_pct', st_dump['top_reach_pct'], perc['top_reachable_pct']),
                                   ('largest_pct', st_dump['largest_pct'], perc['largest_pct'])):
            if abs(float(mine) - float(theirs)) > 1e-9:
                replica_bad.append(f'SE {name} 재현 {mine:.6g} ≠ 정본 {theirs:.6g}')
        for name, mine, theirs in (('n_components', st_dump['n_components'], perc['n_components']),
                                   ('n_large_components', st_dump['n_large'], perc['n_large_components'])):
            if int(mine) != int(theirs):
                replica_bad.append(f'SE {name} 재현 {mine} ≠ 정본 {theirs}')
        if set(perc['bottom_se']) != prod_bot or set(perc['top_se']) != prod_top:
            replica_bad.append(f"SE 밴드 집합 재현 ≠ 정본 (bottom {len(prod_bot)}/{len(perc['bottom_se'])} · top {len(prod_top)}/{len(perc['top_se'])})")
        cn = DAC.calc_se_se_cn(atoms_d, contacts_l, se_types, perc_set=perc.get('percolating_se'), scale=SCALE, h_spread_sim=0.0)
        rec.update(se_cn_perc=cn.get('mean_perc'), se_cn_n_perc=cn.get('n_perc'), se_cn_eff_area_perc=cn.get('cn_eff_area_perc'),
                   se_cn_perc_keys=bool('mean_perc' in cn))
        n_perc_nodes = int(round(st_dump['perc_pct'] / 100.0 * se_idx.size))
        if cn.get('n_perc') is not None and int(cn['n_perc']) != n_perc_nodes:
            replica_bad.append(f"se_se_cn_n_perc {cn['n_perc']} ≠ 관통 SE 수 {n_perc_nodes}")
        if (cn.get('n_perc') is None) != (n_perc_nodes == 0):
            replica_bad.append('se_se_cn_*_perc 키 유무가 관통 여부와 어긋난다')
    else:
        rec.update(se_level='NA', se_xcheck=None, se_cn_perc_keys=False)
        flags.append('SE 입자 0')

    # ③-AM — 웹앱 build_network (정본) · 재현 · 수확기 슬래브 · 기하
    am_idx = np.flatnonzero(is_am)
    hp = harv_percolation(atoms, box_lo, box_hi, int(n_types))
    rec.update(harv_perc=int(hp['perc']), harv_n_bot=hp['n_bottom'], harv_n_top=hp['n_top'], harv_reason=hp.get('reason'),
               harv_slab_t_um=(None if hp.get('slab_t') is None else hp['slab_t'] * SCALE),
               harv_z_lo_um=hp['z_lo'] * SCALE, harv_z_hi_um=hp['z_hi'] * SCALE)
    if am_idx.size:
        pos_am = {int(g): k for k, g in enumerate(am_idx.tolist())}
        both_am = known & is_am[np.where(known, k1, 0)] & is_am[np.where(known, k2, 0)]
        keep = both_am & ((carea > 0) | (delta > 0))              # build_network: ca > 0 or δ > 0 인 행만 간선
        rec['am_rows_dropped_zero'] = int(both_am.sum() - keep.sum())
        dump_am = _unique_pairs(np.asarray([pos_am[int(g)] for g in k1[keep]], dtype=np.int64),
                                np.asarray([pos_am[int(g)] for g in k2[keep]], dtype=np.int64))
        geom_am = _pairs_within(xyz[am_idx], r_am, lx, ly, z_pad=float(r_am.max()))
        b = _bands(z_all[am_idx], r_am, plate_z, factor=_replica_factor)
        st_dump = _graph_stats(am_idx.size, dump_am, b['bot'], b['top'], singletons=False)
        st_geom = _graph_stats(am_idx.size, geom_am, b['bot'], b['top'], singletons=False)
        # 수확기 슬래브 (고체 외피 · t = r_AM,max · 표면 기준 · 외톨이 포함)
        t_am = float(r_am.max())
        hb = (z_all[am_idx] - r_am) <= hp['z_lo'] + t_am
        ht = (z_all[am_idx] + r_am) >= hp['z_hi'] - t_am
        st_h_geom = _graph_stats(am_idx.size, geom_am, hb, ht, singletons=True)
        st_h_dump = _graph_stats(am_idx.size, dump_am, hb, ht, singletons=True)
        ad, ag = _pair_set(dump_am), _pair_set(geom_am)
        rec.update(am_level=b['level'], am_n_bot_L0=b['n_bot_L0'], am_n_top_L0=b['n_top_L0'], am_n_bot=b['n_bot'], am_n_top=b['n_top'],
                   am_overlap=b['overlap'], am_active_frac=st_dump['active_pct'] / 100.0, am_perc_frac=st_dump['perc_pct'] / 100.0,
                   am_n_components=st_dump['n_components'], am_n_isolated=st_dump['n_isolated'],
                   am_edges_dump=len(ad), am_edges_geom=len(ag), am_geom_only=len(ag - ad), am_dump_only=len(ad - ag),
                   am_perc_webapp_dump=bool(st_dump['perc_pct'] > 0), am_perc_webapp_geom=bool(st_geom['perc_pct'] > 0),
                   am_perc_harv_geom=bool(hp['perc']), am_perc_harv_dump=bool(st_h_dump['n_span_components'] > 0),
                   harv_overlap=int((hb & ht).sum()))
        if bool(st_h_geom['n_span_components'] > 0) != bool(hp['perc']):
            replica_bad.append(f"AM 수확기 슬래브 재현 {st_h_geom['n_span_components'] > 0} ≠ 정본 perc {hp['perc']}")
        if int(hb.sum()) != int(hp['n_bottom']) or int(ht.sum()) != int(hp['n_top']):
            replica_bad.append(f"AM 수확기 슬래브 인원 재현 {int(hb.sum())}/{int(ht.sum())} ≠ 정본 {hp['n_bottom']}/{hp['n_top']}")
        rec['am_xcheck'] = _xcheck(rec['am_perc_webapp_dump'], rec['am_perc_webapp_geom'], rec['am_perc_harv_geom'], rec['am_perc_harv_dump'])
        # 정본 대조 — build_network (전자) + run_decomposition 의 성분 셈
        net = NC.build_network(atoms_d, contacts_l, am_types, SCALE, plate_z, lx, ly, BOUNDARY_FACTOR,
                               mode='electronic', type_map=tmap, results_dir=None, contact_mode='hertzian')
        if net is None:
            replica_bad.append('build_network 가 None (AM 없음?) — 재현과 어긋난다')
        else:
            prod_bot = {int(ids[am_idx[k]]) for k in np.flatnonzero(b['bot'])}
            prod_top = {int(ids[am_idx[k]]) for k in np.flatnonzero(b['top'])}
            if set(net['bottom']) != prod_bot or set(net['top']) != prod_top:
                replica_bad.append(f"AM 밴드 집합 재현 ≠ 정본 (bottom {len(prod_bot)}/{len(net['bottom'])} · top {len(prod_top)}/{len(net['top'])})")
            if int(net.get('n_boundary_overlap') or 0) != b['overlap']:
                replica_bad.append(f"AM 겹침 재현 {b['overlap']} ≠ 정본 {net.get('n_boundary_overlap')}")
            if len(net['edges']) != len(ad):
                replica_bad.append(f"AM 간선 수 재현 {len(ad)} ≠ 정본 {len(net['edges'])}")
            act, pf = _electronic_fractions(net)
            if abs(act - rec['am_active_frac']) > 1e-9 or abs(pf - rec['am_perc_frac']) > 1e-9:
                replica_bad.append(f"AM active/percolating 재현 {rec['am_active_frac']:.6g}/{rec['am_perc_frac']:.6g} ≠ 정본 {act:.6g}/{pf:.6g}")
    else:
        rec.update(am_level='NA', am_xcheck=None)
        notes.append('AM 입자 0 — 전자망 열은 비어야 한다')

    # ⑤ legacy 팔
    rec.update(legacy_ionic_percolates=None, legacy_status=None, legacy_agree=None)
    if legacy is not None and rec.get('case') in legacy:
        lp, ls = legacy[rec['case']]
        rec.update(legacy_ionic_percolates=lp, legacy_status=ls)
        if lp is not None and rec.get('se_perc_webapp_dump') is not None:
            rec['legacy_agree'] = bool(lp == rec['se_perc_webapp_dump'])

    # 판정
    rec['replica_ok'] = not replica_bad
    rec['replica_why'] = ' · '.join(replica_bad)
    if replica_bad:
        flags.append('재현 ≠ 정본: ' + rec['replica_why'])
    for ph in ('se', 'am'):
        lvl = rec.get(f'{ph}_level')
        if lvl in ('L1', 'L2'):
            flags.append(f"{ph.upper()} 경계 폴백 {lvl} 발동 (L0 밴드 아래 {rec[f'{ph}_n_bot_L0']} · 위 {rec[f'{ph}_n_top_L0']} · 문턱 {MIN_BAND}) — 산출물에 기록되지 않는다")
        ov = rec.get(f'{ph}_overlap')
        if ov:
            flags.append(f"{ph.upper()} bottom∩top 겹침 {ov} — 겹친 입자의 성분은 통째로 관통으로 센다 (두께 < 4·r)")
    if rec.get('harv_overlap'):
        notes.append(f"수확기 슬래브 겹침 {rec['harv_overlap']} (같은 부류 · 수확기 AM perc 쪽)")
    for ph in ('se', 'am'):
        xc = rec.get(f'{ph}_xcheck')
        if xc and xc != 'agree':
            notes.append(f'{ph.upper()} 교차 대조 불일치 = {xc}')
    if rec.get('legacy_agree') is False:
        notes.append(f"legacy 09-15 ionic_percolates {rec['legacy_ionic_percolates']} ≠ 웹앱 SE 관통 {rec['se_perc_webapp_dump']}")
    rec['verdict'] = 'FLAG' if flags else 'CLEAN'
    rec['why'] = ' · '.join(flags)
    rec['note'] = ' · '.join(notes)
    rec['t_s'] = round(time.perf_counter() - t0, 2)
    return rec


# ──────────────────────────────────────────────────────────────────────────────
# 실행 · 출력
# ──────────────────────────────────────────────────────────────────────────────
def _write(out_dir: Path, rows, meta):
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / 'perc_audit.tsv').open('w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh, delimiter='\t')
        w.writerow(TSV_COLS)
        for r in rows:
            w.writerow(['' if r.get(c) is None else r.get(c) for c in TSV_COLS])
    (out_dir / 'perc_audit.json').write_text(
        json.dumps(dict(schema=SCHEMA, meta=meta, rows=rows), ensure_ascii=False, indent=1, default=str) + '\n', encoding='utf-8')


def _summary(rows):
    s = dict(n=len(rows), status={}, verdict={})
    for r in rows:
        s['status'][r['status']] = s['status'].get(r['status'], 0) + 1
        if r['status'] == 'OK':
            s['verdict'][r['verdict']] = s['verdict'].get(r['verdict'], 0) + 1
    ok = [r for r in rows if r['status'] == 'OK']
    for ph in ('se', 'am'):
        s[f'{ph}_level'] = {lv: sum(1 for r in ok if r.get(f'{ph}_level') == lv) for lv in LEVELS + ('NA',)}
        s[f'{ph}_overlap_cases'] = sum(1 for r in ok if r.get(f'{ph}_overlap'))
        s[f'{ph}_xcheck'] = {}
        for r in ok:
            k = r.get(f'{ph}_xcheck')
            if k:
                s[f'{ph}_xcheck'][k] = s[f'{ph}_xcheck'].get(k, 0) + 1
        s[f'{ph}_geom_only_max'] = max((r.get(f'{ph}_geom_only') or 0) for r in ok) if ok else None
        s[f'{ph}_dump_only_max'] = max((r.get(f'{ph}_dump_only') or 0) for r in ok) if ok else None
    s['se_perc_true'] = sum(1 for r in ok if r.get('se_perc_webapp_dump'))
    s['am_perc_true'] = sum(1 for r in ok if r.get('am_perc_webapp_dump'))
    s['harv_perc_true'] = sum(1 for r in ok if r.get('harv_perc'))
    s['harv_overlap_cases'] = sum(1 for r in ok if r.get('harv_overlap'))
    s['replica_ok_all'] = all(r.get('replica_ok') for r in ok) if ok else None
    s['se_polydisperse_cases'] = sum(1 for r in ok if (r.get('r_se_classes') or 0) > 1)
    s['box_default_cases'] = sum(1 for r in ok if r.get('box_is_webapp_default'))
    s['legacy'] = dict(compared=sum(1 for r in ok if r.get('legacy_agree') is not None),
                       agree=sum(1 for r in ok if r.get('legacy_agree') is True),
                       disagree=sum(1 for r in ok if r.get('legacy_agree') is False))
    s['floor_z_deck'] = sorted({str(r.get('floor_z_deck')) for r in ok})
    s['t_total_s'] = round(sum(float(r.get('t_s') or 0) for r in ok), 1)
    return s


def _git_rev():
    try:
        rev = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=str(_SCR), capture_output=True, text=True).stdout.strip()
        dirty = bool(subprocess.run(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=str(_SCR),
                                    capture_output=True, text=True).stdout.strip())
        return dict(sha=rev or None, dirty=dirty)
    except OSError:
        return dict(sha=None, dirty=None)


def run(args):
    cohort = Path(args.cohort)
    rows = HB.read_cohort(cohort)
    if not rows:
        print(f'⛔ 코호트가 0 행이다 — {cohort}', file=sys.stderr)
        return 2
    if args.case:
        want = set(args.case)
        rows = [r for r in rows if r['case'] in want]
        if len(rows) != len(want):
            print(f'⛔ 코호트에 없는 case: {sorted(want - {r["case"] for r in rows})}', file=sys.stderr)
            return 2
    legacy = None if args.no_legacy else _read_legacy(args.legacy_csv)
    out = []
    for k, row in enumerate(rows, 1):
        rec = dict(case=row['case'], design_family=row.get('design_family'), n_types=row.get('n_types'), status='OK',
                   verdict='', why='', note='')
        st = (row.get('status') or '').strip()
        if st and st != 'RAW_OK':
            rec.update(status='SKIPPED', why=f'코호트 status {st}')
            out.append(rec)
            print(f"  [{k}/{len(rows)}] {rec['case']}: SKIPPED ({st})")
            continue
        atom = HB.remap(row['atom_file'], args.root_from, args.root_to)
        contact = HB.remap(row['contact_file'], args.root_from, args.root_to)
        deck = HB.remap(row['deck'], args.root_from, args.root_to) if row.get('deck') else atom.parent.parent / f"input_{row['case']}.liggghts"
        try:
            for lab, p in (('atom', atom), ('contact', contact)):
                if not p.is_file():
                    raise BedRefusal(f'{lab} 파일 없음: {p}')
            for lab, p, col in (('atom', atom, 'atom_sha256'), ('contact', contact, 'contact_sha256'), ('deck', deck, 'deck_sha256')):
                want_h = (row.get(col) or '').strip()
                if want_h and p.is_file() and HB.sha256_of(p) != want_h:
                    raise BedRefusal(f'{lab} sha256 ≠ 코호트 봉인 ({p})')
            mesh, pick, why = HB.pick_mesh(atom)
            rec['mesh_pick'] = pick
            if mesh is None:
                rec.update(status='NO_MESH', why=f'메시 없음 ({why})')
                out.append(rec)
                print(f"  [{k}/{len(rows)}] {rec['case']}: NO_MESH {rec['why']}"[:300])
                continue
            r = audit_case(str(atom), str(contact), int(row['n_types']), str(mesh),
                           deck_path=(str(deck) if deck.is_file() else None), legacy=legacy, case=rec['case'])
            rec.update(r)
        except (BedRefusal, OSError, ValueError, KeyError) as e:
            rec.update(status='INPUT_ERROR', verdict='', why=str(e))
        out.append(rec)
        print(f"  [{k}/{len(rows)}] {rec['case']}: {rec['status']} {rec.get('verdict', '')} "
              f"SE {rec.get('se_level', '')} {rec.get('se_perc_pct', '')} · AM {rec.get('am_level', '')} {rec.get('am_perc_frac', '')} "
              f"· {rec.get('t_s', '')} s {rec.get('why', '')}{(' ‖ ' + rec['note']) if rec.get('note') else ''}"[:400])
    s = _summary(out)
    meta = dict(generated=datetime.datetime.now().isoformat(timespec='seconds'), cohort=str(cohort), root_from=args.root_from,
                root_to=args.root_to, boundary_factor=BOUNDARY_FACTOR, min_band=MIN_BAND, large_comp=LARGE_COMP,
                legacy_csv=(None if legacy is None else str(args.legacy_csv)), code=_git_rev(), summary=s)
    _write(Path(args.out), out, meta)
    print(f"→ {args.out}/perc_audit.tsv · perc_audit.json\n  요약: {json.dumps(s, ensure_ascii=False)}")
    if s['verdict'].get('FLAG'):
        return 3
    if s['status'].get('INPUT_ERROR') or s['status'].get('NO_MESH'):
        return 2
    return 0


# ──────────────────────────────────────────────────────────────────────────────
# 자기검사 — 반례를 합성 덤프로 심고 잡히는지 본다 (규율 ②: 재현 먼저)
# ──────────────────────────────────────────────────────────────────────────────
_HD = [H.COL_D1, H.COL_D2, H.COL_AREA, H.COL_DELTA]
_LO, _HI = (0.0, 0.0, -1.0), (20.0, 20.0, 25.0)


def _deck(tmp, z=0.0, name='input_c.liggghts'):
    p = os.path.join(tmp, name)
    with open(p, 'w') as fh:
        fh.write(f'units si\nfix zwall all wall/gran model hertz tangential history primitive type 3 zplane {z}\nrun 1\n')
    return p


def _contacts2(tmp, rows, name='contact_2f.liggghts'):
    p = os.path.join(tmp, name)
    with open(p, 'w') as fh:
        for f in range(2):
            fh.write(f'ITEM: TIMESTEP\n{100 * (f + 1)}\nITEM: NUMBER OF ENTRIES\n{len(rows)}\nITEM: ENTRIES ' + ' '.join(_HD) + '\n')
            for r in rows:
                fh.write(' '.join(str(x) for x in r) + '\n')
    return p


def _bed_f1():
    """기준 침대 (상자 20×20 · 플래튼 z 20) — SE r 1 (type 3) · AM_P r 2 (type 1) · AM_S r 0.5 (type 2).
    SE: 사슬 (2,2,0.9+1.9k · k 0..10) 11 개 + 바닥 외톨이 2 + 위 외톨이 2 → L0 밴드 3/3 · 관통 11/15.
    AM_P: 사슬 (14,14,2.0+3.9k · k 0..4) 5 개 + 바닥 외톨이 2 + 위 외톨이 2 · AM_S 외톨이 1 → L0 3/3 · active = perc = 5/10."""
    atoms = [(1 + k, 2.0, 2.0, round(0.9 + 1.9 * k, 6), 1.0, 3) for k in range(11)]
    atoms += [(12, 6.0, 2.0, 0.9, 1.0, 3), (13, 10.0, 2.0, 0.9, 1.0, 3), (14, 6.0, 10.0, 19.9, 1.0, 3), (15, 10.0, 10.0, 19.9, 1.0, 3)]
    atoms += [(21 + k, 14.0, 14.0, round(2.0 + 3.9 * k, 6), 2.0, 1) for k in range(5)]
    atoms += [(26, 14.0, 6.0, 2.0, 2.0, 1), (27, 6.0, 14.0, 2.0, 2.0, 1), (28, 14.0, 6.0, 17.6, 2.0, 1), (29, 6.0, 14.0, 17.6, 2.0, 1)]
    atoms += [(30, 10.0, 14.0, 10.0, 0.5, 2)]
    contacts = [(1 + k, 2 + k, 0.1, 0.1) for k in range(10)] + [(21 + k, 22 + k, 0.4, 0.1) for k in range(4)]
    return atoms, contacts


def _run(td, atoms, contacts, plate=20.0, deck=True, deck_z=0.0, tag='c', legacy=None, contact_path=None, **kw):
    a = H._atom_file(td, atoms, name=f'atom_{tag}.liggghts', lo=_LO, hi=_HI)
    c = contact_path or H._contact_file(td, contacts, name=f'contact_{tag}.liggghts', headers=_HD)
    m = H._stl(td, z=plate, name=f'mesh_{tag}.stl')
    d = _deck(td, z=deck_z, name=f'input_{tag}.liggghts') if deck else None
    return audit_case(a, c, 3, m, deck_path=d, legacy=legacy, **kw)


def selftest():
    fails = []

    def chk(name, ok):
        print(('  ✓ ' if ok else '  ✗ ') + name)
        if not ok:
            fails.append(name)

    A, C = _bed_f1()
    with tempfile.TemporaryDirectory() as td:
        r = _run(td, A, C)
        chk('① 기준 침대 → CLEAN · SE L0 (3/3) · AM L0 (3/3) · 겹침 0 · 재현 = 정본',
            r['verdict'] == 'CLEAN' and r['se_level'] == 'L0' and r['am_level'] == 'L0' and r['se_overlap'] == 0 and r['am_overlap'] == 0
            and r['replica_ok'] and r['why'] == '')
        #    top_reachable 은 위 밴드에 앉은 외톨이 SE (14 · 15) 도 센다 — 관통 (11) 과 다른 양이다 (정본 실측: 13/15)
        chk('①b SE 관통 11/15 · top_reach 13/15 (위 밴드 외톨이 2 포함) · 성분 5 (외톨이 4 포함) · ≥10 성분 1 · 최대 성분 11/15',
            abs(r['se_perc_pct'] - 11 / 15 * 100) < 1e-9 and abs(r['se_top_reach_pct'] - 13 / 15 * 100) < 1e-9
            and r['se_n_components'] == 5 and r['se_n_isolated'] == 4 and r['se_n_large'] == 1 and abs(r['se_largest_pct'] - 11 / 15 * 100) < 1e-9)
        chk('①c AM active = percolating = 5/10 (바닥 밴드의 외톨이 AM_P 2 는 active 에 안 든다 — G_active 규약) · 성분 6',
            abs(r['am_active_frac'] - 0.5) < 1e-12 and abs(r['am_perc_frac'] - 0.5) < 1e-12 and r['am_n_components'] == 6 and r['am_n_isolated'] == 5)
        chk('①d 교차 대조 SE · AM 모두 agree · 수확기 AM perc 1 · 단분산 SE 라 웹앱 L0 밴드 = 수확기 벽 밴드',
            r['se_xcheck'] == 'agree' and r['am_xcheck'] == 'agree' and r['harv_perc'] == 1 and r['se_wall_band_equal'] is True)
        chk('①e se_se_cn_*_perc 키 있음 · n_perc = 관통 SE 11 · 덱 바닥 0 (SE 벽 type 3) · 상자 20 ≠ 웹앱 기본 0.05 는 note 만',
            r['se_cn_perc_keys'] and r['se_cn_n_perc'] == 11 and r['floor_z_deck'] == 0.0 and r['floor_wall_type'] == 3
            and r['box_is_webapp_default'] is False and '상자' in r['note'] and r['verdict'] == 'CLEAN')

        # ★ 정본 run_decomposition 과 전자 분율 대조 (재현 셈이 정본과 같은가)
        atoms_d = {i: dict(type=t, x=x, y=y, z=z, radius=rr) for (i, x, y, z, rr, t) in A}
        contacts_l = [dict(id1=i, id2=j, contact_area=a, delta=dl) for (i, j, a, dl) in C]
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                rd = NC.run_decomposition(atoms_d, contacts_l, [1, 2], SCALE, 20.0, 20.0, 20.0, sigma_bulk=NC.SIGMA_AM_ELECTRONIC,
                                          type_map={1: 'AM_P', 2: 'AM_S', 3: 'SE'}, mode='electronic')
        except Exception as e:                                    # noqa: BLE001 — 실패 원인을 화면에 남긴다
            rd, _err = None, f'{type(e).__name__}: {e}'
            print(f'    run_decomposition 예외: {_err}')
        chk('①f 정본 run_decomposition(electronic) active/percolating = 재현 (0.5/0.5)',
            rd is not None and abs(rd['active_fraction'] - r['am_active_frac']) < 1e-9 and abs(rd['percolating_fraction'] - r['am_perc_frac']) < 1e-9)
        #    수확기 tortuosity_se 의 벽 밴드 관통 성분 수 = 재현
        atoms_arr, blo, bhi, _ = read_atom_dump(os.path.join(td, 'atom_c.liggghts'))
        labels, _ = H.phase_labels(atoms_arr['type'], 3)
        ts = H.tortuosity_se(atoms_arr, labels, blo, bhi, n_pairs=3, plate_z=20.0)
        chk('①g 정본 tortuosity_se wall_n_span_components > 0 = 재현 se_perc_wall_geom (True)',
            ts['band_detail']['wall_n_span_components'] > 0 and r['se_perc_wall_geom'] is True)

        # ② L1 — 바닥 L0 밴드에 SE 2 개 (사슬 시작 + 외톨이 1) → L1 (z ≤ 3) 에서 3 개
        A2 = [a for a in A if a[0] != 13]
        r2 = _run(td, A2, C, tag='l1')
        chk('② ★ SE 바닥 L0 밴드 2 < 3 → 폴백 L1 · FLAG (산출물에 기록되지 않는 정의 변경) · 재현 = 정본',
            r2['verdict'] == 'FLAG' and r2['se_level'] == 'L1' and r2['se_n_bot_L0'] == 2 and r2['se_n_bot'] == 3 and r2['replica_ok']
            and 'SE 경계 폴백 L1' in r2['why'])
        # ③ L2 — 플래튼을 침대 위 멀리 (z 60) → L0 · L1 위 밴드 0 → L2 (관측 z-범위)
        r3 = _run(td, A, C, plate=60.0, tag='l2')
        chk('③ ★ 플래튼이 침대 위 멀리 → SE·AM 모두 L2 · FLAG',
            r3['verdict'] == 'FLAG' and r3['se_level'] == 'L2' and r3['am_level'] == 'L2' and r3['se_n_top_L0'] == 0 and r3['replica_ok'])
        # ④ 겹침 — 얇은 침대 (플래튼 3.5 · SE r 1): 외톨이 SE 3 개가 두 밴드에 동시에 든다 → 간선 0 인데 관통 100 %
        A4 = [(1, 2.0, 5.0, 1.8, 1.0, 3), (2, 6.0, 5.0, 1.8, 1.0, 3), (3, 10.0, 5.0, 1.8, 1.0, 3)]
        r4 = _run(td, A4, [], plate=3.5, tag='ov')
        chk('④ ★ bottom∩top 겹침 3 → FLAG · 정본 percolation_pct = 100 인데 간선 0 (겹침 인공물 재현) · AM 0 → am_level NA',
            r4['verdict'] == 'FLAG' and r4['se_overlap'] == 3 and abs(r4['se_perc_pct'] - 100.0) < 1e-9 and r4['se_edges_dump'] == 0
            and r4['replica_ok'] and r4['am_level'] == 'NA' and '겹침 3' in r4['why'])
        # ⑤ ≥10 문턱 — 사슬 10 개 → 1 · 9 개 → 0 (정본과 같은 값)
        A5 = [(1 + k, 2.0, 2.0, round(0.9 + 1.9 * k, 6), 1.0, 3) for k in range(10)] + [a for a in A if 12 <= a[0] <= 15] + [a for a in A if a[0] >= 21]
        C5 = [(1 + k, 2 + k, 0.1, 0.1) for k in range(9)] + [c for c in C if c[0] >= 21]
        r5 = _run(td, A5, C5, tag='ten')
        A5b = [a for a in A5 if a[0] != 10]
        C5b = [c for c in C5 if c[1] != 10]
        r5b = _run(td, A5b, C5b, tag='nine')
        chk('⑤ n_large_components: 사슬 10 → 1 · 9 → 0 (문턱 10 · 정본 대조 통과)',
            r5['se_n_large'] == 1 and r5b['se_n_large'] == 0 and r5['replica_ok'] and r5b['replica_ok'])
        # ⑥ AM 교차 대조 'band' — AM_S (r 0.5) 사슬이 수확기 슬래브 (t = r_AM,max = 2 · 외피 기준) 로는 관통하고 웹앱 밴드 (z ≤ 1 · z ≥ 19) 로는 못 미친다
        #    AM_P 는 사슬 없이 외톨이 6 (바닥 3 · 위 3 — L0 를 유지) · AM_S 사슬 z 1.4 … 18.5 (r 0.5 · 간격 0.9)
        A6 = [a for a in A if a[5] == 3] + [a for a in A if a[0] in (21, 25, 26, 27, 28, 29)]
        A6 += [(40 + k, 10.0, 10.0, round(1.4 + 0.9 * k, 6), 0.5, 2) for k in range(20)]
        C6 = [(1 + k, 2 + k, 0.1, 0.1) for k in range(10)] + [(40 + k, 41 + k, 0.05, 0.1) for k in range(19)]
        r6 = _run(td, A6, C6, tag='band')
        chk('⑥ ★ AM 교차 대조 = band (웹앱 관통 0 · 수확기 관통 1 · 접촉 원천을 바꿔도 안 뒤집힘) · 웹앱은 L0 (AM_P 3/3) · CLEAN',
            r6['am_xcheck'] == 'band' and r6['am_perc_webapp_dump'] is False and r6['am_perc_harv_geom'] is True and r6['am_level'] == 'L0'
            and r6['verdict'] == 'CLEAN' and 'AM 교차 대조 불일치 = band' in r6['note'])
        # ⑦ AM 교차 대조 'contact' — 덤프에서 AM 사슬 간선 하나를 뺀다 (기하는 그대로)
        C7 = [c for c in C if c != (22, 23, 0.4, 0.1)]
        r7 = _run(td, A, C7, tag='contact')
        chk('⑦ ★ AM 교차 대조 = contact (덤프 관통 0 · 기하 관통 1 · geom_only 1) · 정본 percolating 0',
            r7['am_xcheck'] == 'contact' and r7['am_geom_only'] == 1 and r7['am_perc_webapp_dump'] is False
            and r7['am_perc_webapp_geom'] is True and r7['am_perc_frac'] == 0.0 and r7['replica_ok'])
        # ⑧ SE 비관통 → se_se_cn_*_perc 키 없음 · SE 교차 대조 contact
        C8 = [c for c in C if c != (5, 6, 0.1, 0.1)]
        r8 = _run(td, A, C8, tag='secut')
        chk('⑧ ★ SE 덤프 사슬 끊김 → 정본 percolation 0 · se_se_cn_*_perc 키 없음 · SE 교차 대조 = contact',
            r8['se_perc_pct'] == 0.0 and r8['se_cn_perc_keys'] is False and r8['se_cn_n_perc'] is None and r8['se_xcheck'] == 'contact'
            and r8['replica_ok'])
        # ⑨ 덱 — 바닥 0.5 → FLAG · 덱 없음 → FLAG
        r9 = _run(td, A, C, deck_z=0.5, tag='floor')
        r9b = _run(td, A, C, deck=False, tag='nodeck')
        chk('⑨ ★ 덱 바닥 z = 0.5 → FLAG (웹앱은 0 을 가정) · 덱 없음 → FLAG (fail-closed)',
            r9['verdict'] == 'FLAG' and '바닥 벽' in r9['why'] and r9b['verdict'] == 'FLAG' and '덱 없음' in r9b['why'])
        # ⑩ SE 다분산 → note · 벽 밴드 동일성은 판정하지 않는다
        A10 = [(a[0], a[1], a[2], a[3], (1.2 if a[0] == 14 else a[4]), a[5]) for a in A]
        r10 = _run(td, A10, C, tag='poly')
        chk('⑩ SE 반지름 2 계급 → note 만 (CLEAN 유지) · 재현 = 정본',
            r10['verdict'] == 'CLEAN' and r10['r_se_classes'] == 2 and 'SE 반지름 2 계급' in r10['note'] and r10['replica_ok'])
        # ⑪ 프레임 2 · 고아 행
        r11 = _run(td, A, C, tag='fr2', contact_path=_contacts2(td, C))
        r11b = _run(td, A, C + [(1, 999, 0.1, 0.1)], tag='orphan')
        chk('⑪ ★ 접촉 프레임 2 → FLAG · 원자에 없는 id 의 행 → FLAG (orphan 1)',
            r11['verdict'] == 'FLAG' and r11['contact_frames'] == 2 and r11b['verdict'] == 'FLAG' and r11b['orphan_rows'] == 1)
        # ⑫ 변이 — 재현의 밴드 폭만 3.0 으로 바꾸면 정본과 어긋나 FLAG (재현이 정본에 묶여 있다)
        r12 = _run(td, A, C, tag='mut', _replica_factor=3.0)
        chk('⑫ ★ 변이 (재현 boundary_factor 3.0) → replica_ok False · FLAG',
            r12['replica_ok'] is False and r12['verdict'] == 'FLAG' and '재현 ≠ 정본' in r12['why'])
        # ⑬ legacy 대조 — run() 이 채운다 (아래 ⑭ 에서 확인)
        # ⑭ CLI: 코호트 · sha · SKIPPED · NO_MESH · rc
        post = Path(td) / 'lhs' / 'c1' / 'post_c1'
        post.mkdir(parents=True)
        for src, dst in (('atom_c.liggghts', 'atom_100.liggghts'), ('contact_c.liggghts', 'contact_100.liggghts'), ('mesh_c.stl', 'mesh_100.stl')):
            (post / dst).write_bytes(Path(td, src).read_bytes())
        deck1 = Path(td) / 'lhs' / 'c1' / 'input_c1.liggghts'
        deck1.write_bytes(Path(td, 'input_c.liggghts').read_bytes())
        post2 = Path(td) / 'lhs' / 'c2' / 'post_c2'
        post2.mkdir(parents=True)
        for src, dst in (('atom_l1.liggghts', 'atom_100.liggghts'), ('contact_l1.liggghts', 'contact_100.liggghts'), ('mesh_l1.stl', 'mesh_100.stl')):
            (post2 / dst).write_bytes(Path(td, src).read_bytes())
        deck2 = Path(td) / 'lhs' / 'c2' / 'input_c2.liggghts'
        deck2.write_bytes(Path(td, 'input_c.liggghts').read_bytes())
        cols = ['case', 'status', 'design_family', 'n_types', 'deck', 'deck_sha256', 'atom_file', 'atom_sha256', 'contact_file', 'contact_sha256']

        def _row(case, post_dir, deck, status='RAW_OK', sha_ok=True):
            return dict(case=case, status=status, design_family='bimodal', n_types='3', deck=str(deck),
                        deck_sha256=HB.sha256_of(deck) if deck.exists() else '',
                        atom_file=str(post_dir / 'atom_100.liggghts'), atom_sha256=(HB.sha256_of(post_dir / 'atom_100.liggghts') if sha_ok else 'deadbeef'),
                        contact_file=str(post_dir / 'contact_100.liggghts'), contact_sha256=HB.sha256_of(post_dir / 'contact_100.liggghts'))
        rows = [_row('c1', post, deck1), _row('c2', post2, deck2), _row('perc', post, deck1, status='DECK_MISSING'), _row('c3', post, deck1, sha_ok=False)]
        tsv = Path(td) / 'cohort.tsv'
        with tsv.open('w', encoding='utf-8', newline='') as fh:
            fh.write('# 봉인 주석\n')
            w = csv.DictWriter(fh, fieldnames=cols, delimiter='\t')
            w.writeheader()
            w.writerows(rows)
        leg = Path(td) / 'legacy.csv'
        leg.write_text('# 주석\ncase_id,ionic_status,ionic_percolates\nc1,OK,True\nc2,SOLVE_NONE,False\n', encoding='utf-8')
        od = Path(td) / 'out'
        rc = main(['--cohort', str(tsv), '--out', str(od), '--legacy-csv', str(leg)])
        js = json.loads((od / 'perc_audit.json').read_text(encoding='utf-8'))
        st = {r_['case']: r_['status'] for r_ in js['rows']}
        byc = {r_['case']: r_ for r_ in js['rows']}
        chk('⑭ CLI: c1 CLEAN · c2 FLAG (L1) · perc SKIPPED · c3 sha 불일치 INPUT_ERROR · rc 3 (FLAG 가 입력 오류보다 앞선다)',
            rc == 3 and st == {'c1': 'OK', 'c2': 'OK', 'perc': 'SKIPPED', 'c3': 'INPUT_ERROR'}
            and js['meta']['summary']['verdict'] == {'CLEAN': 1, 'FLAG': 1} and byc['c2']['se_level'] == 'L1')
        chk('⑭b legacy 대조: c1 True = 웹앱 관통 True (agree) · c2 False ≠ 웹앱 관통 True (disagree → note) · 요약 compared 2',
            byc['c1']['legacy_agree'] is True and byc['c2']['legacy_agree'] is False and 'legacy 09-15' in byc['c2']['note']
            and js['meta']['summary']['legacy'] == {'compared': 2, 'agree': 1, 'disagree': 1})
        chk('⑭c TSV 열 = TSV_COLS · 요약에 level 분포 · 재현 전부 정본과 일치',
            (od / 'perc_audit.tsv').read_text(encoding='utf-8').splitlines()[0].split('\t') == list(TSV_COLS)
            and js['meta']['summary']['se_level']['L1'] == 1 and js['meta']['summary']['replica_ok_all'] is True)
        os.remove(post / 'mesh_100.stl')
        od2 = Path(td) / 'out2'
        rc2 = main(['--cohort', str(tsv), '--case', 'c1', '--out', str(od2), '--no-legacy'])
        js2 = json.loads((od2 / 'perc_audit.json').read_text(encoding='utf-8'))
        chk('⑭d 같은 step 메시 없음 → NO_MESH (CLEAN 아님) · rc 2', rc2 == 2 and js2['rows'][0]['status'] == 'NO_MESH')
        # ⑮ 2-type 침대 (AM · SE) 도 같은 경로
        A15 = [(a[0], a[1], a[2], a[3], a[4], (1 if a[5] in (1, 2) else 2)) for a in A]
        a15 = H._atom_file(td, A15, name='atom_t2.liggghts', lo=_LO, hi=_HI)
        r15 = audit_case(a15, H._contact_file(td, C, name='contact_t2.liggghts', headers=_HD), 2, H._stl(td, z=20.0, name='mesh_t2.stl'),
                         deck_path=_deck(td, name='input_t2.liggghts'))
        chk('⑮ 2-type (AM · SE) 침대 → CLEAN · AM 10 · 재현 = 정본',
            r15['verdict'] == 'CLEAN' and r15['n_am'] == 10 and r15['replica_ok'])

    print()
    if fails:
        print(f'✗ {len(fails)} 건 실패')
        return 1
    print('✓ 전부 통과 — 검사기가 반례 (폴백 L1/L2 · 겹침 인공물 · ≥10 문턱 · 밴드/접촉 귀속 · 덱 바닥 · 프레임 · 고아 행 · 변이) 를 잡고 '
          '재현이 웹앱 정본 · 수확기 정본에 묶여 있다.  ⚠ 실제 130 덤프의 상태는 WSL 실행 결과가 말한다')
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description='LHS 퍼콜레이션 묶음 (②) 읽기 전용 점검 — 경계 규칙 단계 (L0/L1/L2) · 겹침 · '
                                             '재현 대조 · 접촉 원천 × 경계 규칙 2×2 · legacy 대조.  인계 값은 만들지 않는다')
    ap.add_argument('--cohort', default=str(HB.COHORT), help='코호트 TSV (기본: 봉인 area_s2_cohort.tsv)')
    ap.add_argument('--case', action='append', default=[], help='이 case 만 (여러 번 줄 수 있다)')
    ap.add_argument('--root-from', default='', help='코호트 경로 접두사 (치환 전)')
    ap.add_argument('--root-to', default='', help='실제 경로 접두사로 치환')
    ap.add_argument('--legacy-csv', default=str(LEGACY_CSV), help='09-15 legacy 팔 CSV (기본: docs/data/lhs_percolation_measured_20260915.csv)')
    ap.add_argument('--no-legacy', action='store_true', help='legacy 대조 생략')
    ap.add_argument('--out', help='산출 폴더 (perc_audit.tsv · perc_audit.json)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.out:
        ap.error('--out 이 필요하다')
    return run(a)


if __name__ == '__main__':
    sys.exit(main())
