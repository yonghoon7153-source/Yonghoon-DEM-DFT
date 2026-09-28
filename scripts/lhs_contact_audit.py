#!/usr/bin/env python3
"""lhs_contact_audit.py — LHS 접촉 덤프 **읽기 전용** 점검 (J20-a ⓐ · 1저자 비준 2026-09-28 밤 *"권고하는걸로 진행하자"*).

왜 — 인계표의 웹앱 CN · 접촉 수 열 (`dem_analysis_core.calc_se_se_cn` · `calc_am_isolation_risk` · `calc_am_am_cn` ·
`calc_interface_area`) 은 접촉 덤프의 **행을 거르지 않고** 행마다 두 입자에 +1 한다.  웹앱 파서는 파일 안 **모든 프레임을
이어 붙인다** (DESC-06 — 합성 2 프레임에서 SE-SE CN 정확히 2 배).  ⇒ 값을 뽑기 전에 입력이 "한 프레임 · 쌍마다 한 행 ·
접촉만" 인지 원자료에서 센다.  **인계 값은 만들지 않는다.**

케이스마다 (코호트 봉인 파일 — 수확과 같은 atom · contact · 같은 step mesh):
  ① 프레임 수 — 접촉 `ITEM: ENTRIES` · 원자 `ITEM: TIMESTEP`
  ② 마지막 프레임의 중복 무순서 쌍 · 자기쌍 · δ ≤ 0 행 · 주기 플래그 (`c_cpl[9]`) 행  (`lhs_descriptor_harvest.scan_contact_dump`)
  ③ ★ **기하 재계수** (1저자 09-28 밤: *"contact 파일에 flag 로 잘 되어 있으니 그걸로 판단해서 CN 확인하면 되지 않나"*) —
     원자 좌표로 x·y **최소 영상** (z 개방) 겹침 쌍을 다시 세어 (`lhs_perc_extract._pairs_within`) 덤프 쌍과 **쌍 단위로** 맞댄다:
     기하에만 · 덤프에만 있는 쌍 · 경계를 넘는 기하 쌍 ↔ 주기 플래그 행 (쌍마다) · 상별 CN (덤프 행 = 웹앱 방식 / 기하).
     ★ v2 (09-29): 불일치 쌍은 덤프 **자릿수에서 실측한 반올림 폭**으로 판별한다 (폭 안 = rounding · 폭 밖 = far → FLAG) ·
     양쪽에 있는 쌍은 δ 를 대조한다 · 경계를 안 넘는데 플래그가 켜진 쌍은 MPI 고스트 규칙 (주기면 띠 + 최소 균일 격자) 으로
     설명되면 결함이 아니다 (`audit_case` docstring · 원장 SELF-63 · LHS-16).
  ④ 상별 바닥 벽 · 플래튼 접촉 입자 비율 (`lhs_descriptor_harvest.wall_touch_fractions` — J20-a ⓓ 새 열과 **같은 함수**).
     ⚠ 옆면 (x·y) 은 주기 경계라 ③ 이 검증하지만, 바닥 벽 · 플래튼 (z) 은 주기가 아니다 — 그 너머에 입자가 없어 CN 이 낮은 것은
     **정의상** 그렇다 (결함 아님).  ④ 는 그 몫을 가르는 설명 변수다.

출력: <out>/contact_audit.tsv (케이스당 한 행) · contact_audit.json (행 + 요약 + 실행 정보).
rc 0 = 전부 깨끗 · rc 3 = ①②③ 중 하나라도 어긋난 케이스가 있다 (보고용 — 거부는 배치 관문 `lhs_webapp_batch` 가 한다) ·
rc 2 = 입력 오류 (코호트 · 경로).

    python3 scripts/lhs_contact_audit.py --out ~/lhs_contact_audit_$(date +%Y%m%d)        # 코호트 전 건 (수 분)
    python3 scripts/lhs_contact_audit.py --case lhs00_000 --out /tmp/audit_one             # 한 건
    python3 scripts/lhs_contact_audit.py --selftest
"""
from __future__ import annotations

import argparse
import csv
import datetime
import decimal
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

_SCR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCR))
import lhs_descriptor_harvest as H                      # noqa: E402  같은 읽기 · 같은 규칙 (규율 ①)
import lhs_harvest_batch as HB                          # noqa: E402  코호트 · 경로 치환 · 같은 step 메시
from lhs_perc_extract import BedRefusal, read_atom_dump, _pairs_within   # noqa: E402

SCHEMA = 'lhs_contact_audit/v2'
#: v2 (2026-09-29 비준) — 불일치 쌍의 판별은 고정 상대 폭이 아니라 **덤프 자릿수에서 계산한 반올림 폭**으로 한다.
#:   v1 의 `NEAR_REL = 1e-6·Σr` (= 0.01 nm) 는 실물 덤프 (LIGGGHTS `%g` 6 유효숫자 · x ≈ 0.03 mm → 마지막 자리 0.1 nm ·
#:   반폭 0.05 nm/좌표) 보다 좁아 WSL 130 건 중 113 을 FLAG 로 냈다 (원장 `SELF-63`).  ⇒ 폭은 파일에서 **실측**한 유효숫자로.
#: 분할 격자 추정 상한 (x · y · z) — LIGGGHTS 기본 분할은 균일 벽돌 (`processors * * *` · balance 없음).
GRID_MAX = (8, 8, 64)
#: 유효숫자 바닥 — 관측 최대 자릿수 S_obs 는 형식 정밀도의 **하한**이라 (끝 0 이 지워진다) 그대로 쓰면 폭이 헐거워지는 쪽 (false-green).
#: LIGGGHTS 기본 `%g` = 6 이므로 S = max(S_obs, 6) — 참 정밀도가 더 낮은 파일 (%.4g 등) 은 폭이 좁아져 FLAG 쪽 (fail-closed).  자기리뷰 #3.
SIGFIG_FLOOR = 6
#: 이 감사가 전제하는 상자 경계 — LHS 덱 `boundary p p f`.  다르면 최소영상 재계수 자체가 무효 (자기리뷰 #11).
BOX_FLAGS = ('pp', 'pp', 'ff')
TSV_COLS = (
    'case', 'design_family', 'n_types', 'n_atoms', 'status', 'verdict', 'why', 'note',
    'contact_frames', 'atom_frames', 'rows_last', 'unique_pairs', 'dup_pairs', 'dup_rows', 'self_pairs',
    'delta_nonpos', 'delta_min', 'periodic_rows',
    'step_atom', 'step_contact', 'orphan_rows', 'entries_declared', 'nonfinite_rows',
    'sigfigs_obs', 'sigfigs', 'sigfigs_delta', 'bound_max',
    'geom_pairs', 'geom_only', 'dump_only', 'rounding_pairs', 'geom_only_far', 'dump_only_far',
    'both_inconsistent', 'both_max_dev',
    'geom_cross', 'flag_and_cross', 'flag_not_cross', 'cross_not_flag', 'flag_id_order_bad',
    'skin', 'newton', 'cutneighmax', 'processors_line', 'flag_only_in_band_id2', 'flag_only_in_band_any', 'flag_only_straddle',
    'mpi_grid_min', 'predicted_flag_missing', 'flag_only_explained',
    'cn_se_se_dump', 'cn_se_se_geom', 'cn_am_se_dump', 'cn_am_se_geom', 'cn_am_am_dump', 'cn_am_am_geom',
    'wt_SE_floor', 'wt_SE_plate', 'wt_AM_P_floor', 'wt_AM_P_plate', 'wt_AM_S_floor', 'wt_AM_S_plate',
    'wt_AM_floor', 'wt_AM_plate',
)


# ──────────────────────────────────────────────────────────────────────────────
# v2 — 반올림 폭 (덤프 자릿수 실측) · 덱 (skin) · 분할 격자 추정
# ──────────────────────────────────────────────────────────────────────────────
def _sigfigs(tok: str) -> int:
    """숫자 토큰의 유효숫자 수 — **문자열**로 센다 (`0.0304637` → 6 · `0.005` → 1 · `3.34479e-06` → 6 · `0` → 0)."""
    d = decimal.Decimal(tok.strip())
    if d == 0:
        return 0
    return len(d.as_tuple().digits)


def _half_ulp(tok: str, sigfigs: int) -> float:
    """토큰 값의 반올림 **반폭** = 0.5 · 10^(십진 지수 − S + 1).  S = 파일 전체의 최대 유효숫자 (토큰 자신의 자릿수가 아니다 —
    `%g` 는 끝의 0 을 지우므로 `0.005` 는 S=6 에서 0.00500000 이고 반폭은 5e-9 다.  토큰 자신의 1 자리로 재면 5e-4 =
    폭이 10⁵ 배 헐거워져 진짜 불일치를 삼킨다 = false-green).  값 0 → 0."""
    d = decimal.Decimal(tok.strip())
    if d == 0 or sigfigs <= 0:
        return 0.0
    return 0.5 * 10.0 ** (d.adjusted() - sigfigs + 1)


def _atom_tokens(path, cols=('x', 'y', 'z', 'radius')):
    """마지막 프레임 ATOMS 블록의 `cols` 토큰 **문자열** (행 순서 = `read_atom_dump` · `_atom_ids` 와 같은 규칙:
    마지막 `ITEM: TIMESTEP` 뒤 · 열 수가 맞는 행만)."""
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        lines = fh.read().splitlines()
    frames = [i for i, ln in enumerate(lines) if ln.startswith('ITEM: TIMESTEP')]
    if not frames:
        raise BedRefusal(f'{path}: `ITEM: TIMESTEP` 이 없다')
    i = frames[-1]
    out = {c: [] for c in cols}
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('ITEM: ATOMS'):
            headers = ln.replace('ITEM: ATOMS', '').strip().split()
            miss = [c for c in cols if c not in headers]
            if miss:
                raise BedRefusal(f'{path}: 원자 덤프에 열 {miss} 이 없다 (있는 열: {headers})')
            ix = {c: headers.index(c) for c in cols}
            i += 1
            while i < len(lines) and not lines[i].startswith('ITEM:'):
                v = lines[i].split()
                if len(v) == len(headers):
                    for c in cols:
                        out[c].append(v[ix[c]])
                i += 1
            break
        i += 1
    return out


def _contact_delta_tokens(path):
    """마지막 ENTRIES 블록의 `c_cpl[23]` (δ) 토큰 문자열 (행 순서 = `read_contact_dump` 와 같은 규칙).  열이 없으면 None."""
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        lines = fh.read().splitlines()
    starts = [i for i, ln in enumerate(lines) if ln.startswith('ITEM: ENTRIES')]
    if not starts:
        raise BedRefusal(f'{path}: `ITEM: ENTRIES` 가 없다')
    i = starts[-1]
    headers = lines[i].replace('ITEM: ENTRIES', '').strip().split()
    if H.COL_DELTA not in headers:
        return None
    k = headers.index(H.COL_DELTA)
    toks = []
    i += 1
    while i < len(lines) and not lines[i].startswith('ITEM:'):
        v = lines[i].split()
        if len(v) == len(headers):
            toks.append(v[k])
        i += 1
    return toks


_RE_SKIN = re.compile(r'^\s*neighbor\s+([0-9.eE+\-]+)\s+\S+', re.M)
_RE_PROCS = re.compile(r'^\s*processors\s+(.*?)\s*$', re.M)
_RE_NEWTON = re.compile(r'^\s*newton\s+(on|off)\b', re.M)


def _deck_info(deck_path):
    """덱에서 `neighbor <skin> …` · `processors …` · `newton on|off` 를 읽는다 — **마지막** 줄 (재시작 머리 + 본문에서 다시 선언될 수 있다 ·
    자기리뷰 #9).  없으면 None (추정으로 메우지 않는다).  processors 는 축별 제약 ('*' 또는 정수) 로도 돌려준다."""
    if deck_path is None or not Path(deck_path).is_file():
        return dict(skin=None, processors_line=None, procs=None, newton=None, deck=None)
    txt = Path(deck_path).read_text(encoding='utf-8', errors='replace')
    sk = _RE_SKIN.findall(txt)
    pr = _RE_PROCS.findall(txt)
    nw = _RE_NEWTON.findall(txt)
    procs = None
    if pr:
        tk = pr[-1].split()
        if len(tk) >= 3 and all(t == '*' or t.isdigit() for t in tk[:3]):
            procs = tuple(('*' if t == '*' else int(t)) for t in tk[:3])
    try:
        skin = float(sk[-1]) if sk else None
    except ValueError:
        skin = None
    return dict(skin=skin, processors_line=(pr[-1] if pr else None), procs=procs, newton=(nw[-1] if nw else None), deck=str(deck_path))


def _cells(u_lo, u_hi, n):
    """[u_lo, u_hi] (상자 단위 0–1) 구간이 n 균일 분할의 어느 칸에 걸치는가 → (칸_lo, 칸_hi)."""
    return (np.minimum(np.floor(u_lo * n), n - 1).astype(np.int64), np.minimum(np.floor(u_hi * n), n - 1).astype(np.int64))


def _infer_grid(xyz, lo, hi, pairs, tau, procs=None):
    """플래그만 켜진 (경계를 안 넘는) 쌍 전부가 균일 분할면을 걸치는 **최소** 격자 (Px, Py, Pz) — 없으면 None.

    LIGGGHTS 는 `balance` 가 없으면 상자를 축마다 균일하게 자른다.  쌍 (i, j) 가 축 a 의 n 분할면을 **걸칠 수 있다** ⇔
    [min(u_i, u_j) − τ, max(u_i, u_j) + τ] 가 두 칸에 걸친다.  τ (쌍마다 · 상자 단위) = 좌표 반올림 반폭 합 + skin/2 (소유권 지연 —
    입자는 재이웃 step 에만 옮겨 가므로 덤프 시각엔 분할면 너머 skin/2 까지 옛 소유자가 갖고 있을 수 있다).  ★ 자기리뷰 #1: τ 없이
    (반올림된 좌표로 floor) 하면 `%g` 토큰이 분할면 위에 떨어진 원자 하나가 전 격자를 죽인다 (합성 2×2×16 실측 · 무작위 플래그의
    설명률은 τ 로 바뀌지 않는다).  `procs` (덱 processors 줄) 가 정수인 축은 그 값만 후보 (자기리뷰 #5a).
    N = Px·Py·Pz 최소를 고른다 — n 의 배수 격자도 전부 설명하므로 **분해의 증명이 아니라 최소 설명 격자**다 (필드 이름 mpi_grid_min).
    반환: (grid 또는 None, 그 격자 기준 걸치는 쌍 수 (없으면 축별 최대))."""
    if len(pairs) == 0:
        return None, 0
    P = np.asarray(pairs, dtype=np.int64)
    tau = np.asarray(tau, dtype=np.float64).reshape(-1)
    cells = {}
    for a, nmax in zip(range(3), GRID_MAX):
        L = float(hi[a] - lo[a])
        u = (xyz[:, a] - lo[a]) / L
        ui, uj = u[P[:, 0]], u[P[:, 1]]
        u_lo, u_hi = np.clip(np.minimum(ui, uj) - tau / L, 0.0, 1.0), np.clip(np.maximum(ui, uj) + tau / L, 0.0, 1.0)
        diff = np.zeros((nmax + 1, len(P)), dtype=bool)
        for n in range(2, nmax + 1):
            c_lo, c_hi = _cells(u_lo, u_hi, n)
            diff[n] = c_lo != c_hi
        cells[a] = diff
    cand = []
    for a, nmax in zip(range(3), GRID_MAX):
        fixed = procs[a] if (procs is not None and isinstance(procs[a], int)) else None
        cand.append([fixed] if (fixed is not None and 1 <= fixed <= nmax) else list(range(1, nmax + 1)))
    best = None
    for px in cand[0]:
        for py in cand[1]:
            for pz in cand[2]:
                n_tot = px * py * pz
                if n_tot < 2 or (best is not None and n_tot >= best[0]):
                    continue
                ok = cells[0][px] | cells[1][py] | cells[2][pz]
                if ok.all():
                    best = (n_tot, (px, py, pz))
    if best is None:
        n_str = int(max(cells[a][2:].sum(axis=1).max() if cells[a].shape[0] > 2 else 0 for a in range(3)))
        return None, n_str
    return best[1], int(len(P))


def _clear_straddle(xyz, lo, hi, pairs, tau, grid):
    """격자 `grid` 의 분할면을 **분명히** 걸치는 쌍 (구간을 τ 만큼 안으로 줄여도 두 칸) — 충분성 검사용 (자기리뷰 #5c)."""
    if len(pairs) == 0:
        return np.zeros(0, dtype=bool)
    P = np.asarray(pairs, dtype=np.int64)
    tau = np.asarray(tau, dtype=np.float64).reshape(-1)
    out = np.zeros(len(P), dtype=bool)
    for a in range(3):
        n = grid[a]
        if n < 2:
            continue
        L = float(hi[a] - lo[a])
        u = (xyz[:, a] - lo[a]) / L
        ui, uj = u[P[:, 0]], u[P[:, 1]]
        u_lo, u_hi = np.minimum(ui, uj) + tau / L, np.maximum(ui, uj) - tau / L
        m = u_hi > u_lo
        c_lo, c_hi = _cells(np.clip(u_lo, 0, 1), np.clip(u_hi, 0, 1), n)
        out |= m & (c_lo != c_hi)
    return out


def _cn(labels, idx_i, idx_j, ph_a, ph_b):
    """무순서 쌍 (i, j) 목록 → 상 ph_a 입자당 상 ph_b 이웃 수 평균 (ph_a 전 입자 · 접촉 0 포함 — 웹앱과 같은 분모)."""
    in_a = np.asarray([l in ph_a for l in labels])
    in_b = np.asarray([l in ph_b for l in labels])
    n_a = int(in_a.sum())
    if n_a == 0:
        return None
    cnt = np.zeros(len(labels), dtype=np.int64)
    m1 = in_a[idx_i] & in_b[idx_j]
    m2 = in_a[idx_j] & in_b[idx_i]
    np.add.at(cnt, idx_i[m1], 1)
    np.add.at(cnt, idx_j[m2], 1)
    return float(cnt[in_a].sum() / n_a)


def audit_case(atom_path, contact_path, n_types, mesh_path=None, deck_path=None):
    """한 케이스 — 읽기만 한다.  반환 dict (TSV_COLS 키 + 세부).

    v2 판별 (09-29 비준 · 자기리뷰 12 항 반영):
      · 불일치 쌍마다 **반올림 폭** B 를 그 쌍의 토큰에서 계산한다 — 위치: 분리 벡터 방향으로 투영한 좌표 반폭의 합
        (Σ_k |u_k|·(h_ik + h_jk))/|u| (1차) + 반지름 반폭 h_ri + h_rj.  S = max(원자 덤프 전체의 최대 유효숫자, 6).
        ① 덤프에만: 재계산 틈 g ≥ 0 · LIGGGHTS δ > 0 — 반올림이면 g + δ ≤ B + h_δ
        ② 기하에만: 재계산 겹침 o > 0 · 덤프 행 없음 (LIGGGHTS 는 d' ≥ Σr) — 반올림이면 o ≤ B
        ③ 양쪽: |δ_덤프 − o| ≤ B + h_δ
        폭 밖 = far (FLAG) · 폭 안 = rounding (불일치로 세지 않는다 — 웹앱 CN 은 덤프 행 기준이라 LIGGGHTS 쪽이 옳다).
      · 주기 플래그 (`c_cpl[9]`) = LIGGGHTS `compute_pair_gran_local.cpp` add_pair: 두 입자가 다 local 이면 0, 아니면
        `is_periodic_ghost(i) || is_periodic_ghost(j)` · `domain_I.h`: 고스트이고 어느 주기 축에서 lo + cutneighmax 안쪽 /
        hi − cutneighmax 바깥쪽이면 1 (master 2026-09-29 열람 · ibb/WSL 빌드 3.8 과의 동일성은 미확인).  `newton off` (LHS 덱) 에서
        고스트 쌍은 tag[i] > tag[j] 인 소유자가 한 번 쓴다 ⇒ **id1 = local · id2 = 고스트 · id1 > id2**.  직렬 런은 고스트 = 주기
        영상뿐이라 플래그 = 경계 넘음.  MPI 런은 내부 분할면 너머 고스트 (상자 안) 도 주기면 띠 (cutneighmax = 2 r_max + skin) 안이면 1
        ⇒ "플래그만" 쌍은 (id2 가 띠 안) ∧ (균일 분할 격자의 분할면을 걸칠 수 있음 — τ 허용) ∧ (그 격자가 플래그를 **예측**하는 쌍에
        플래그가 빠지지 않음 = 충분성) 이면 **설명됨** (결함 아님 · 인계 값 무영향 — 리포에 이 플래그의 소비자는 없다).
        ⚠ 설명됨 ≠ MPI 실행의 증명 (실행 기록이 없다) — note 에 그렇게 적는다.  skin 은 덱에서 · 없으면 fail-closed (FLAG).
    """
    out = {}
    pre_bad = []
    scan = H.scan_contact_dump(contact_path)
    out.update(contact_frames=scan['n_frames'], rows_last=scan['n_rows_last'], unique_pairs=scan['n_unique_pairs'],
               dup_pairs=scan['n_dup_pairs'], dup_rows=scan['n_dup_rows'], self_pairs=scan['n_self_pairs'],
               delta_nonpos=scan['n_delta_nonpos'], delta_min=scan['delta_min'], periodic_rows=scan['n_periodic_flag'])
    out['atom_frames'] = H.count_blocks(atom_path, 'ITEM: TIMESTEP')
    out['step_atom'], out['step_contact'] = H.last_timestep(atom_path), H.last_timestep(contact_path)
    out['entries_declared'] = _entries_declared(contact_path)

    atoms, lo, hi, _bc = read_atom_dump(atom_path)
    if tuple(_bc or ()) != BOX_FLAGS:
        pre_bad.append(f'상자 경계 플래그 {_bc} ≠ {BOX_FLAGS} (x·y 주기 · z 개방 전제)')
    ids = H._atom_ids(atom_path)
    labels, _tmap = H.phase_labels(atoms['type'], int(n_types))
    labels = [str(l) for l in labels]
    n = len(ids)
    out['n_atoms'] = n
    lx, ly = float(hi[0] - lo[0]), float(hi[1] - lo[1])
    xyz = np.column_stack([atoms['x'], atoms['y'], atoms['z']])
    r = atoms['radius']

    #  자릿수 실측 → 반올림 반폭 (토큰 문자열 · S = max(파일 전체 최대, 6))
    tok = _atom_tokens(atom_path)
    if any(len(tok[c]) != n for c in tok):
        raise BedRefusal(f'{atom_path}: 토큰 행 수 {[len(tok[c]) for c in tok]} ≠ 원자 수 {n}')
    S_obs = max((_sigfigs(t) for c in tok for t in tok[c]), default=0)
    S = max(S_obs, SIGFIG_FLOOR)
    out.update(sigfigs_obs=int(S_obs), sigfigs=int(S))
    hpos = np.column_stack([[_half_ulp(t, S) for t in tok[c]] for c in ('x', 'y', 'z')])
    hrad = np.asarray([_half_ulp(t, S) for t in tok['radius']])

    #  ③ 기하 재계수 — x·y 최소 영상 · z 개방 (수확의 퍼콜 그래프와 같은 함수)
    gp = _pairs_within(xyz, r, lx, ly, 0.0)
    gi, gj = (gp[:, 0].astype(np.int64), gp[:, 1].astype(np.int64)) if len(gp) else (np.empty(0, np.int64),) * 2
    pos = {int(a): k for k, a in enumerate(ids)}
    c1, c2, _ca, _hd, ex = H.read_contact_dump(contact_path, extra_cols=(H.COL_PERIODIC, H.COL_DELTA))
    known = np.asarray([(int(a) in pos) and (int(b) in pos) for a, b in zip(c1, c2)], dtype=bool)
    out['orphan_rows'] = int((~known).sum())
    di = np.asarray([pos[int(a)] for a in c1[known]], dtype=np.int64)
    dj = np.asarray([pos[int(b)] for b in c2[known]], dtype=np.int64)
    flag = ex[H.COL_PERIODIC]
    flag = None if flag is None else flag[known]
    dl = ex[H.COL_DELTA]
    dl = None if dl is None else dl[known]
    nonfin = int((~np.isfinite(_ca[known])).sum()) + (0 if flag is None else int((~np.isfinite(flag)).sum())) \
        + (0 if dl is None else int((~np.isfinite(dl)).sum()))
    out['nonfinite_rows'] = nonfin                                   # NaN/inf 는 어떤 비교도 조용히 False 다 — 따로 센다 (자기리뷰 #2)
    if dl is not None:
        out['delta_nonpos'] = int((~(dl > 0.0)).sum())              # NaN 도 "양수 아님" 으로 (scan 의 `<= 0` 은 NaN 을 놓친다)
    dtok = _contact_delta_tokens(contact_path)
    if dtok is not None:
        dtok = [t for t, k in zip(dtok, known) if k]
        S_d = max(max((_sigfigs(t) for t in dtok), default=0), SIGFIG_FLOOR)
        hdel = np.asarray([_half_ulp(t, S_d) for t in dtok])
    else:
        S_d, hdel = None, None
    out['sigfigs_delta'] = S_d

    def key(i, j):
        return (min(int(i), int(j)), max(int(i), int(j)))

    gset = {key(a, b) for a, b in zip(gi, gj)}
    dset = {key(a, b) for a, b in zip(di, dj)}
    drow = {}                     # 무순서 쌍 → 마지막 덤프 행 번호 (중복 행은 따로 센다)
    for k_, (a, b) in enumerate(zip(di, dj)):
        drow[key(a, b)] = k_
    only_g, only_d = gset - dset, dset - gset

    def geom(P):
        """쌍 배열 (m, 2) → (재계산 틈 g = d − Σr, 반올림 폭 B) — 최소 영상 · 1차 투영 폭.  벡터화 (양쪽 쌍 = 덤프 전 행)."""
        P = np.asarray(P, dtype=np.int64).reshape(-1, 2)
        if not len(P):
            return np.empty(0), np.empty(0)
        a, b = P[:, 0], P[:, 1]
        u = xyz[b] - xyz[a]
        u[:, 0] -= lx * np.round(u[:, 0] / lx)
        u[:, 1] -= ly * np.round(u[:, 1] / ly)
        d = np.linalg.norm(u, axis=1)
        hsum = hpos[a] + hpos[b]
        proj = (np.abs(u) * hsum).sum(axis=1)
        bound = np.where(d > 0, proj / np.where(d > 0, d, 1.0), hsum.sum(axis=1)) + hrad[a] + hrad[b]
        return d - (r[a] + r[b]), bound

    rounding = far_g = far_d = 0
    bound_max = 0.0
    examples = []
    od = sorted(only_d)
    g_d, B_d = geom(od)
    for k, g, B in zip(od, g_d, B_d):
        g, B = float(g), float(B)
        row = drow[k]
        dd = float(dl[row]) if dl is not None else None
        hd_ = float(hdel[row]) if hdel is not None else 0.0
        bound_max = max(bound_max, B)
        #  ① LIGGGHTS 가 접촉 (δ > 0) 인데 재계산은 떨어짐: 반올림이면 g + δ ≤ B + h_δ.  δ 열이 없으면 g ≤ B 만.  NaN δ 는 far.
        dd_ok = dd is not None and np.isfinite(dd)
        lhs_ = max(g, 0.0) + (max(dd, 0.0) if dd_ok else 0.0)
        if (dd is None or dd_ok) and lhs_ <= B + hd_:
            rounding += 1
        else:
            far_d += 1
            if len(examples) < 5:
                examples.append(dict(kind='dump_only', id1=int(ids[k[0]]), id2=int(ids[k[1]]), gap=g, delta_dump=dd, bound=B))
    og = sorted(only_g)
    g_g, B_g = geom(og)
    for k, g, B in zip(og, g_g, B_g):
        g, B = float(g), float(B)
        bound_max = max(bound_max, B)
        #  ② 재계산은 겹침 (o = −g > 0) 인데 덤프 행이 없다: 반올림이면 o ≤ B
        if -g <= B:
            rounding += 1
        else:
            far_g += 1
            if len(examples) < 5:
                examples.append(dict(kind='geom_only', id1=int(ids[k[0]]), id2=int(ids[k[1]]), overlap=-g, bound=B))
    both_bad, both_max = 0, 0.0
    common = sorted(gset & dset)
    if common:
        g_c, B_c = geom(common)
        bound_max = max(bound_max, float(B_c.max()))
        if dl is not None:
            rows_c = np.asarray([drow[k] for k in common], dtype=np.int64)
            dev = np.abs(dl[rows_c] - (-g_c))
            bad_c = ~(dev <= B_c + hdel[rows_c])                    # NaN → True (불일치) — 자기리뷰 #2
            both_bad, both_max = int(bad_c.sum()), float(np.nanmax(dev)) if np.isfinite(dev).any() else float('nan')
            for idx in np.flatnonzero(bad_c)[:5]:
                if len(examples) < 5:
                    k = common[idx]
                    examples.append(dict(kind='both', id1=int(ids[k[0]]), id2=int(ids[k[1]]), overlap_geom=float(-g_c[idx]),
                                         delta_dump=float(dl[rows_c[idx]]), bound=float(B_c[idx])))
    out.update(geom_pairs=len(gset), geom_only=len(only_g), dump_only=len(only_d), rounding_pairs=int(rounding),
               geom_only_far=int(far_g), dump_only_far=int(far_d), both_inconsistent=int(both_bad),
               both_max_dev=(float(both_max) if dl is not None else None), bound_max=float(bound_max), far_examples=examples)

    def crosses(a, b):
        return abs(xyz[b, 0] - xyz[a, 0]) > lx / 2 or abs(xyz[b, 1] - xyz[a, 1]) > ly / 2

    gcross = {k for k in gset if crosses(*k)}
    out['geom_cross'] = len(gcross)
    dk = _deck_info(deck_path)
    out.update(skin=dk['skin'], newton=dk['newton'], processors_line=dk['processors_line'], deck=dk['deck'])
    per = [bool(f and f[0] == 'p') for f in (_bc or BOX_FLAGS)]      # 덤프 BOX BOUNDS 플래그 (pp pp ff) — 주기 축만 띠 검사
    band = (2.0 * float(r.max()) + dk['skin']) if (dk['skin'] is not None and n) else None
    out['cutneighmax'] = band
    out.update(flag_only_in_band_id2=None, flag_only_in_band_any=None, flag_only_straddle=None, mpi_grid_min=None,
               predicted_flag_missing=None, flag_only_explained=None, flag_id_order_bad=None)
    if flag is not None:
        fmask = np.isfinite(flag) & (flag != 0.0)
        fset = {key(a, b) for a, b, f in zip(di, dj, fmask) if f}
        dcross = {k for k in dset if crosses(*k)}
        out.update(flag_and_cross=len(fset & dcross), flag_not_cross=len(fset - dcross), cross_not_flag=len(dcross - fset))
        if dk['newton'] == 'off':                                   # newton off: 고스트 행은 tag[i] > tag[j] 인 소유자가 쓴다 → id1 > id2
            out['flag_id_order_bad'] = int(sum(1 for a, b, f in zip(c1[known], c2[known], fmask) if f and not (int(a) > int(b))))
        fonly = [(int(a), int(b)) for a, b, f in zip(di, dj, fmask) if f and key(a, b) not in dcross]   # (id1=local, id2=고스트) 순서 유지
        if fonly:
            if band is None:
                out['flag_only_explained'] = False
            else:
                def in_band(p):
                    return any(per[ax] and (xyz[p, ax] < lo[ax] + band or xyz[p, ax] > hi[ax] - band) for ax in range(3))
                nb2 = sum(1 for a, b in fonly if in_band(b))
                nba = sum(1 for a, b in fonly if in_band(a) or in_band(b))
                P_f = np.asarray(fonly, dtype=np.int64)
                tau_f = hpos[P_f[:, 0]].max(axis=1) + hpos[P_f[:, 1]].max(axis=1) + 0.5 * dk['skin']
                grid, n_str = _infer_grid(xyz, lo, hi, fonly, tau_f, dk['procs'])
                pfm = None
                if grid is not None:
                    #  충분성 (자기리뷰 #5c): 이 격자가 플래그를 예측하는 쌍 (분명히 걸침 · 고스트 후보 = 작은 id 쪽이 띠 안) 에 플래그가 빠지면 안 된다
                    unf = [(int(a), int(b)) for a, b, f in zip(di, dj, fmask) if not f and key(a, b) not in dcross]
                    if unf:
                        P_u = np.asarray(unf, dtype=np.int64)
                        tau_u = hpos[P_u[:, 0]].max(axis=1) + hpos[P_u[:, 1]].max(axis=1) + 0.5 * dk['skin']
                        cs = _clear_straddle(xyz, lo, hi, unf, tau_u, grid)
                        ghost = np.where(ids[P_u[:, 0]] < ids[P_u[:, 1]], P_u[:, 0], P_u[:, 1])      # newton off: 작은 tag 가 고스트
                        pfm = int(sum(1 for q, c_ in zip(ghost, cs) if c_ and in_band(int(q))))
                    else:
                        pfm = 0
                out.update(flag_only_in_band_id2=nb2, flag_only_in_band_any=nba, flag_only_straddle=n_str,
                           mpi_grid_min=(None if grid is None else 'x'.join(str(v) for v in grid)), predicted_flag_missing=pfm,
                           flag_only_explained=bool(nb2 == len(fonly) and grid is not None and pfm == 0))
    else:
        out.update(flag_and_cross=None, flag_not_cross=None, cross_not_flag=None)

    AM = {'AM', 'AM_P', 'AM_S'}
    for nm, pa, pb in (('se_se', {'SE'}, {'SE'}), ('am_se', AM, {'SE'}), ('am_am', AM, AM)):
        out[f'cn_{nm}_dump'] = _cn(labels, di, dj, pa, pb)          # 덤프 **행** 기준 (중복 행 포함) = 웹앱 방식 (마지막 프레임)
        out[f'cn_{nm}_geom'] = _cn(labels, gi, gj, pa, pb)          # 기하 기준

    if mesh_path is not None:
        pz = H.plate_z_from_stl(str(mesh_path))
        wt = H.wall_touch_fractions(labels, atoms['z'], r, pz)
        for ph in ('SE', 'AM_P', 'AM_S', 'AM'):
            for side in ('floor', 'plate'):
                out[f'wt_{ph}_{side}'] = (wt.get(ph) or {}).get(side)
        out['plate_z_sim'] = pz

    bad, note = list(pre_bad), []
    if out['contact_frames'] != 1:
        bad.append(f"접촉 프레임 {out['contact_frames']}")
    if out['atom_frames'] != 1:
        bad.append(f"원자 프레임 {out['atom_frames']}")
    if out['step_atom'] != out['step_contact']:
        bad.append(f"원자 step {out['step_atom']} ≠ 접촉 step {out['step_contact']}")
    if out['entries_declared'] is not None and out['entries_declared'] != out['rows_last']:
        bad.append(f"NUMBER OF ENTRIES {out['entries_declared']} ≠ 읽은 행 {out['rows_last']} (잘린 파일?)")
    if out['dup_rows']:
        bad.append(f"중복 행 {out['dup_rows']}")
    if out['self_pairs']:
        bad.append(f"자기쌍 {out['self_pairs']}")
    if out['orphan_rows']:
        bad.append(f"고아 행 {out['orphan_rows']}")
    if nonfin:
        bad.append(f'비유한 (NaN/inf) 값 행 {nonfin}')
    if dl is None:
        bad.append('δ 열 (c_cpl[23]) 없음 — ① ③ 판별 불가')
    if flag is None:
        bad.append('주기 플래그 열 (c_cpl[9]) 없음 — 경계 넘음 대조 불가')
    far = far_g + far_d + both_bad
    if far:
        bad.append(f'기하≠덤프 (반올림 폭 밖) {far} (기하에만 {far_g} · 덤프에만 {far_d} · δ 불일치 {both_bad})')
    if rounding:
        note.append(f'반올림 폭 안 {rounding} (유효숫자 관측 {S_obs} → 적용 {S} · 폭 최대 {bound_max:.3g})')
    if out['delta_nonpos']:
        bad.append(f"δ≤0 행 {out['delta_nonpos']}")
    if flag is not None:
        if out['cross_not_flag']:
            bad.append(f"경계를 넘는데 플래그 0: {out['cross_not_flag']}")
        if out['flag_id_order_bad']:
            bad.append(f"플래그 행인데 id1 > id2 가 아님 {out['flag_id_order_bad']} (newton off 규칙)")
        if out['flag_not_cross']:
            if out['flag_only_explained']:
                note.append(f"플래그만 {out['flag_not_cross']} = MPI 고스트 가설과 정합 (id2 띠 안 {out['flag_only_in_band_id2']}/{out['flag_not_cross']} · "
                            f"최소 설명 격자 {out['mpi_grid_min']} · 예측 누락 0 · 띠 {band:.4g}) — 실행 기록 (rank 수) 없음 · 인계 무영향")
            else:
                bad.append(f"플래그만 {out['flag_not_cross']} 설명 안 됨 (skin {dk['skin']} · id2 띠 안 {out['flag_only_in_band_id2']} · "
                           f"격자 {out['mpi_grid_min']} · 예측 누락 {out['predicted_flag_missing']})")
    out['verdict'] = 'CLEAN' if not bad else 'FLAG'
    out['why'] = ' · '.join(bad)
    out['note'] = ' · '.join(note)
    return out


def _entries_declared(path):
    """마지막 ENTRIES 블록의 `ITEM: NUMBER OF ENTRIES` 값 (없으면 None) — 읽은 행 수와 대조 (잘린 파일 · 자기리뷰 #11)."""
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        lines = fh.read().splitlines()
    val = None
    for i, ln in enumerate(lines):
        if ln.startswith('ITEM: NUMBER OF ENTRIES') and i + 1 < len(lines):
            try:
                val = int(lines[i + 1].split()[0])
            except (ValueError, IndexError):
                val = None
    return val


def _write(out_dir: Path, rows, meta):
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / 'contact_audit.tsv').open('w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh, delimiter='\t')
        w.writerow(TSV_COLS)
        for r in rows:
            w.writerow(['' if r.get(c) is None else r.get(c) for c in TSV_COLS])
    (out_dir / 'contact_audit.json').write_text(
        json.dumps(dict(schema=SCHEMA, meta=meta, rows=rows), ensure_ascii=False, indent=1, default=str) + '\n',
        encoding='utf-8')


def _summary(rows):
    s = dict(n=len(rows), status={}, verdict={})
    for r in rows:
        s['status'][r['status']] = s['status'].get(r['status'], 0) + 1
        if r['status'] == 'OK':
            s['verdict'][r['verdict']] = s['verdict'].get(r['verdict'], 0) + 1
    ok = [r for r in rows if r['status'] == 'OK']
    for k in ('contact_frames', 'atom_frames', 'dup_rows', 'self_pairs', 'delta_nonpos', 'geom_only', 'dump_only',
              'rounding_pairs', 'geom_only_far', 'dump_only_far', 'both_inconsistent', 'flag_not_cross', 'cross_not_flag',
              'orphan_rows', 'nonfinite_rows', 'flag_id_order_bad', 'predicted_flag_missing'):
        vals = [r.get(k) for r in ok if r.get(k) is not None]
        s[k] = dict(max=(max(vals) if vals else None), n_nonzero=sum(1 for v in vals if v and (k not in ('contact_frames', 'atom_frames') or v != 1)))
    s['n_periodic_rows_total'] = sum(int(r.get('periodic_rows') or 0) for r in ok)
    s['n_geom_cross_total'] = sum(int(r.get('geom_cross') or 0) for r in ok)
    s['sigfigs'] = sorted({r.get('sigfigs') for r in ok if r.get('sigfigs') is not None})
    s['bound_max'] = max((r.get('bound_max') or 0.0) for r in ok) if ok else None
    fo = [r for r in ok if r.get('flag_not_cross')]
    s['flag_only_cases'] = dict(n=len(fo), explained=sum(1 for r in fo if r.get('flag_only_explained') is True),
                                grids=sorted({str(r.get('mpi_grid_min')) for r in fo}))
    s['skin_missing'] = sum(1 for r in ok if r.get('skin') is None)
    return s


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
    out = []
    for k, row in enumerate(rows, 1):
        rec = dict(case=row['case'], design_family=row.get('design_family'), n_types=row.get('n_types'), status='OK',
                   verdict='', why='', note='')
        st = (row.get('status') or '').strip()
        if st and st != 'RAW_OK':                      # 봉인이 원자료 없음/결손으로 적은 행 — 감사 대상이 아니다 (자기리뷰 #6 · rc 를 가리지 않게 SKIPPED)
            rec.update(status='SKIPPED', why=f'코호트 status {st}')
            out.append(rec)
            print(f"  [{k}/{len(rows)}] {rec['case']}: SKIPPED ({st})")
            continue
        atom = HB.remap(row['atom_file'], args.root_from, args.root_to)
        contact = HB.remap(row['contact_file'], args.root_from, args.root_to)
        #  덱 (skin · processors · newton) — 코호트 `deck` 열 · 없으면 케이스 폴더의 input_<case>.liggghts · 그것도 없으면 None (fail-closed)
        deck = HB.remap(row['deck'], args.root_from, args.root_to) if row.get('deck') else atom.parent.parent / f"input_{row['case']}.liggghts"
        try:
            for lab, p in (('atom', atom), ('contact', contact)):
                if not p.is_file():
                    raise BedRefusal(f'{lab} 파일 없음: {p}')
            #  봉인 sha256 대조 — CLEAN 이 봉인된 바이트에 묶이게 (자기리뷰 #6)
            for lab, p, col in (('atom', atom, 'atom_sha256'), ('contact', contact, 'contact_sha256'), ('deck', deck, 'deck_sha256')):
                want_h = (row.get(col) or '').strip()
                if want_h and p.is_file() and HB.sha256_of(p) != want_h:
                    raise BedRefusal(f'{lab} sha256 ≠ 코호트 봉인 ({p})')
            mesh, pick, why = HB.pick_mesh(atom)
            rec['mesh_pick'] = pick
            if mesh is None:                           # 같은 step 메시 없음 = 수확이 거부하는 입력 (LHS-11) — CLEAN 을 내지 않는다 (자기리뷰 #7)
                rec.update(status='NO_MESH', why=f'메시 없음 ({why})')
                out.append(rec)
                print(f"  [{k}/{len(rows)}] {rec['case']}: NO_MESH {rec['why']}"[:300])
                continue
            rec.update(audit_case(str(atom), str(contact), int(row['n_types']), mesh,
                                  deck_path=(str(deck) if deck.is_file() else None)))
        except (BedRefusal, OSError, ValueError, KeyError) as e:
            rec.update(status='INPUT_ERROR', verdict='', why=str(e))
        out.append(rec)
        print(f"  [{k}/{len(rows)}] {rec['case']}: {rec['status']} {rec.get('verdict', '')} {rec.get('why', '')}"
              f"{(' ‖ ' + rec['note']) if rec.get('note') else ''}"[:300])
    s = _summary(out)
    meta = dict(generated=datetime.datetime.now().isoformat(timespec='seconds'), cohort=str(cohort),
                root_from=args.root_from, root_to=args.root_to, grid_max=list(GRID_MAX), sigfig_floor=SIGFIG_FLOOR,
                code=_git_rev(), summary=s)
    _write(Path(args.out), out, meta)
    print(f"→ {args.out}/contact_audit.tsv · contact_audit.json\n  요약: {json.dumps(s, ensure_ascii=False)}")
    #  rc: FLAG (3) 가 입력 오류 (2) 보다 앞선다 — 결손 행 하나가 어긋난 케이스를 가리지 않게 (자기리뷰 #6).  SKIPPED 는 오류가 아니다.
    if s['verdict'].get('FLAG'):
        return 3
    if s['status'].get('INPUT_ERROR') or s['status'].get('NO_MESH'):
        return 2
    return 0


def _git_rev():
    try:
        rev = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=str(_SCR), capture_output=True, text=True).stdout.strip()
        dirty = bool(subprocess.run(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=str(_SCR),
                                    capture_output=True, text=True).stdout.strip())
        return dict(sha=rev or None, dirty=dirty)
    except OSError:
        return dict(sha=None, dirty=None)


# ──────────────────────────────────────────────────────────────────────────────
# 자기검사 — 반례를 합성 덤프로 심고 잡히는지 본다
# ──────────────────────────────────────────────────────────────────────────────
def _atoms(tmp, rows, lx=10.0, ly=10.0, lz=20.0, name='atom_100.liggghts', frames=1):
    """rows = (id, x, y, z, radius, type)"""
    p = os.path.join(tmp, name)
    with open(p, 'w') as fh:
        for f in range(frames):
            fh.write(f'ITEM: TIMESTEP\n{100 * (f + 1)}\nITEM: NUMBER OF ATOMS\n{len(rows)}\n')
            fh.write(f'ITEM: BOX BOUNDS pp pp ff\n0 {lx}\n0 {ly}\n0 {lz}\n')
            fh.write('ITEM: ATOMS id x y z radius type\n')
            for rr in rows:
                fh.write(' '.join(str(x) for x in rr) + '\n')
    return p


def _contacts(tmp, rows, name='contact_100.liggghts', frames=1):
    """rows = (id1, id2, periodic_flag, area, delta)"""
    p = os.path.join(tmp, name)
    hd = ['c_cpl[7]', 'c_cpl[8]', 'c_cpl[9]', 'c_cpl[22]', 'c_cpl[23]']
    with open(p, 'w') as fh:
        for f in range(frames):
            fh.write(f'ITEM: TIMESTEP\n{100 * (f + 1)}\nITEM: NUMBER OF ENTRIES\n{len(rows)}\n')
            fh.write('ITEM: BOX BOUNDS pp pp ff\n0 10\n0 10\n0 20\n')
            fh.write('ITEM: ENTRIES ' + ' '.join(hd) + '\n')
            for rr in rows:
                fh.write(' '.join(str(x) for x in rr) + '\n')
    return p


def selftest():
    fails = []

    def chk(name, ok):
        print(('  ✓ ' if ok else '  ✗ ') + name)
        if not ok:
            fails.append(name)

    #  침대: 반경 1 · 상자 10×10×20 (xy 주기).  1–2 는 x 경계를 넘어 접촉 (x = 0.5 · 9.7 → 최소영상 거리 0.8 < 2),
    #  2–3 은 안쪽 접촉 (거리 1.9) · 4 는 외톨이 · 5 는 플래튼 (z 20) 에 닿는다 · 1 · 2 · 3 은 바닥 (z − r ≤ 0) 에 닿는다.
    #  type 1 = AM_P · 2 = AM_S · 3 = SE
    A = [(1, 0.5, 5.0, 0.9, 1.0, 3), (2, 9.7, 5.0, 0.9, 1.0, 3), (3, 7.8, 5.0, 0.9, 1.0, 1),
         (4, 5.0, 1.5, 10.0, 1.0, 2), (5, 5.0, 8.5, 19.5, 1.0, 3)]
    clean = [(1, 2, 1, 0.1, 1.2), (2, 3, 0, 0.1, 0.1)]      # δ = 기하 겹침 (1–2: 2 − 0.8 · 2–3: 2 − 1.9) — v2 ③ 이 대조한다
    with tempfile.TemporaryDirectory() as td:
        stl = H._stl(td, z=20.0)
        a1 = _atoms(td, A)
        r = audit_case(a1, _contacts(td, clean), 3, stl)
        chk('① 깨끗한 침대 → CLEAN (프레임 1 · 중복 0 · 기하 = 덤프 · 플래그 = 경계 넘음)', r['verdict'] == 'CLEAN' and r['why'] == '')
        chk('①b 경계를 넘는 기하 쌍 1 = 플래그 행 1 (쌍 단위로 일치)',
            r['geom_cross'] == 1 and r['flag_and_cross'] == 1 and r['flag_not_cross'] == 0 and r['cross_not_flag'] == 0)
        chk('①c CN: SE-SE 덤프 = 기하 = 2/3 (SE 3 개 · 1–2 쌍 하나 · 외톨이 5 포함 분모)',
            abs(r['cn_se_se_dump'] - 2 / 3) < 1e-12 and abs(r['cn_se_se_geom'] - 2 / 3) < 1e-12)
        chk('①d 벽 접촉 비율: SE 바닥 2/3 · 플래튼 1/3 · AM_P 바닥 1 · AM_S 0 · AM (합친) 바닥 1/2',
            abs(r['wt_SE_floor'] - 2 / 3) < 1e-12 and abs(r['wt_SE_plate'] - 1 / 3) < 1e-12
            and r['wt_AM_P_floor'] == 1.0 and r['wt_AM_S_floor'] == 0.0 and abs(r['wt_AM_floor'] - 0.5) < 1e-12)

        r2 = audit_case(a1, _contacts(td, clean, name='contact_2f.liggghts', frames=2), 3, stl)
        chk('② ★ 접촉 프레임 2 개 → FLAG (웹앱 파서는 이어 붙여 CN 이 2 배가 된다)',
            r2['verdict'] == 'FLAG' and r2['contact_frames'] == 2 and '접촉 프레임 2' in r2['why'])

        r3 = audit_case(a1, _contacts(td, clean + [(2, 1, 1, 0.1, 1.2)], name='contact_dup.liggghts'), 3, stl)
        chk('③ ★ 같은 쌍이 두 행 (순서 뒤집힘) → FLAG · 덤프 행 CN > 기하 CN',
            r3['verdict'] == 'FLAG' and r3['dup_rows'] == 1 and r3['cn_se_se_dump'] > r3['cn_se_se_geom'])

        r4 = audit_case(a1, _contacts(td, [(2, 3, 0, 0.1, 0.1)], name='contact_noper.liggghts'), 3, stl)
        chk('④ ★ 경계를 넘는 접촉이 덤프에 없다 → 기하에만 1 · FLAG · 덤프 CN < 기하 CN',
            r4['verdict'] == 'FLAG' and r4['geom_only'] == 1 and r4['cn_se_se_dump'] < r4['cn_se_se_geom'])

        r5 = audit_case(a1, _contacts(td, clean + [(4, 5, 0, 0.0, -0.3)], name='contact_neg.liggghts'), 3, stl)
        chk('⑤ ★ 떨어진 쌍 (δ ≤ 0) 이 행으로 있다 → 덤프에만 1 · δ≤0 1 · FLAG',
            r5['verdict'] == 'FLAG' and r5['dump_only'] == 1 and r5['delta_nonpos'] == 1)

        r6 = audit_case(a1, _contacts(td, [(1, 2, 0, 0.1, 1.2), (2, 3, 1, 0.1, 0.1)], name='contact_badflag.liggghts'), 3, stl)
        chk('⑥ ★ 플래그가 뒤바뀐 덤프 (넘는 쌍 0 · 안쪽 쌍 1) → 플래그만 1 · 넘음만 1 · FLAG',
            r6['verdict'] == 'FLAG' and r6['flag_not_cross'] == 1 and r6['cross_not_flag'] == 1)

        a2 = _atoms(td, A, name='atom_2f.liggghts', frames=2)
        r7 = audit_case(a2, _contacts(td, clean, name='contact_c7.liggghts'), 3, stl)
        chk('⑦ 원자 프레임 2 개 → FLAG (웹앱 atoms.csv 에 id 가 두 번)', r7['verdict'] == 'FLAG' and r7['atom_frames'] == 2)

        #  ⑧ 접촉 판정 경계 쌍 (δ ≈ 0, 출력 자릿수로 갈림) 은 불일치로 세지 않는다
        B = [(1, 3.0, 5.0, 5.0, 1.0, 3), (2, 5.0 + 1e-9, 5.0, 5.0, 1.0, 3)]
        a3 = _atoms(td, B, name='atom_near.liggghts')
        r8 = audit_case(a3, _contacts(td, [(1, 2, 0, 0.0, 1e-9)], name='contact_near.liggghts'), 3, stl)
        chk('⑧ 접촉 판정 경계 쌍 (틈 1e-9 · 토큰 10 자리 → 폭 2e-9) 은 반올림으로 센다 · CLEAN',
            r8['rounding_pairs'] == 1 and r8['dump_only'] == 1 and r8['verdict'] == 'CLEAN')

        #  ⑨ 2-type (mono) 침대 — AM 한 상
        C = [(1, 2.0, 5.0, 0.9, 1.0, 1), (2, 3.8, 5.0, 0.9, 1.0, 2)]
        a4 = _atoms(td, C, name='atom_mono.liggghts')
        r9 = audit_case(a4, _contacts(td, [(1, 2, 0, 0.1, 0.2)], name='contact_mono.liggghts'), 2, stl)
        chk('⑨ 2-type 침대: AM–SE CN 1 · AM_P · AM_S 벽 비율은 빈칸 (N/A · 0 아님)',
            r9['verdict'] == 'CLEAN' and r9['cn_am_se_geom'] == 1.0 and r9['wt_AM_P_floor'] is None and r9['wt_AM_floor'] == 1.0)

        #  ⑩ 웹앱 경로 실증 — 같은 2 프레임 파일을 웹앱 파서로 읽으면 CN 이 정확히 2 배 (감사가 잡는 이유)
        import parse_liggghts as PL
        import dem_analysis_core as C_
        c2f = os.path.join(td, 'contact_2f.liggghts')
        hd, rows = PL.parse_contact_file(c2f)
        cons = [dict(id1=int(float(x[hd.index('id1')])), id2=int(float(x[hd.index('id2')])),
                     contact_area=float(x[hd.index('contact_area')]), delta=float(x[hd.index('delta')])) for x in rows]
        at = {k: dict(id=k, type=t, x=x, y=y, z=z, radius=rad) for (k, x, y, z, rad, t) in A}
        cn2 = C_.calc_se_se_cn(at, cons, [3])['mean']
        chk('⑩ 웹앱 경로 (parse_liggghts → calc_se_se_cn) 는 2 프레임 파일에서 SE-SE CN = 2 × 기하 (4/3 vs 2/3)',
            abs(cn2 - 2 * (2 / 3)) < 1e-12)

        #  ⑪ CLI 한 건 — 코호트 TSV · 산출 파일 · rc
        post = Path(td) / 'cohort' / 'c1' / 'post'
        post.mkdir(parents=True)
        import shutil
        shutil.copy(a1, post / 'atom_100.liggghts')
        shutil.copy(os.path.join(td, 'contact_100.liggghts'), post / 'contact_100.liggghts')
        shutil.copy(stl, post / 'mesh_100.stl')
        tsv = Path(td) / 'cohort.tsv'
        tsv.write_text('# 합성 코호트\ncase\tn_types\tdesign_family\tatom_file\tcontact_file\n'
                       f'c1\t3\tlhs\t{post / "atom_100.liggghts"}\t{post / "contact_100.liggghts"}\n', encoding='utf-8')
        od = Path(td) / 'out'
        rc = main(['--cohort', str(tsv), '--out', str(od)])
        js = json.loads((od / 'contact_audit.json').read_text(encoding='utf-8'))
        chk('⑪ CLI: rc 0 · TSV · JSON (schema · 요약 · 코드 sha 칸)',
            rc == 0 and (od / 'contact_audit.tsv').is_file() and js['schema'] == SCHEMA
            and js['meta']['summary']['verdict'].get('CLEAN') == 1 and 'code' in js['meta'])

        # ── v2 (09-29 비준) — 반올림 판별 · 고스트 플래그.  실물 흉내: mm 단위 · %g 6 유효숫자 (WSL 실측 `0.0304637`) ──
        chk('⑫a 유효숫자 · 반올림 반폭: "0.0304637"→6 · "0.005"→1 · "3.34479e-06"→6 · "0"→0 · 반폭(0.005, S=6) = 5e-9',
            _sigfigs('0.0304637') == 6 and _sigfigs('0.005') == 1 and _sigfigs('3.34479e-06') == 6 and _sigfigs('0') == 0
            and abs(_half_ulp('0.005', 6) - 5e-9) < 1e-24 and abs(_half_ulp('0.0304637', 6) - 5e-8) < 1e-23)
        #  1–2: 재계산 틈 1e-7 (x 만 다름) · LIGGGHTS δ 5e-9.  반폭: x 5e-8 ×2 · 반지름 5e-9 ×2 → 폭 1.1e-7 ≥ 1.05e-7 ⇒ 반올림
        R = [(1, '0.0200004', '0.025', '0.005', '0.005', 3), (2, '0.0300005', '0.025', '0.005', '0.005', 3),
             (3, '0.0100001', '0.01', '0.005', '0.005', 1)]
        a5 = _atoms(td, R, lx=0.05, ly=0.05, lz=0.2, name='atom_round.liggghts')
        r12 = audit_case(a5, _contacts(td, [(1, 2, 0, '1e-09', '5e-09')], name='contact_round.liggghts'), 3, None)
        chk('⑫ ★ 반올림 폭 안의 "덤프에만" 쌍 (틈 1e-7 + δ 5e-9 ≤ 1.1e-7) → rounding 1 · far 0 · CLEAN · 유효숫자 6',
            r12.get('rounding_pairs') == 1 and r12.get('dump_only_far') == 0 and r12['verdict'] == 'CLEAN'
            and r12.get('sigfigs') == 6 and r12.get('dump_only') == 1)
        F = [(1, '0.02', '0.025', '0.005', '0.005', 3), (2, '0.030005', '0.025', '0.005', '0.005', 3),
             (3, '0.0100001', '0.01', '0.005', '0.005', 1)]
        r13 = audit_case(_atoms(td, F, lx=0.05, ly=0.05, lz=0.2, name='atom_far.liggghts'),
                         _contacts(td, [(1, 2, 0, '1e-09', '1e-06')], name='contact_far.liggghts'), 3, None)
        chk('⑬ ★ 반올림 폭 (1.1e-7) 밖의 "덤프에만" 쌍 (틈 5e-6) → dump_only_far 1 · FLAG · 예시 기록',
            r13.get('dump_only_far') == 1 and r13['verdict'] == 'FLAG' and len(r13.get('far_examples') or []) == 1)
        Fg = [(1, '0.02', '0.025', '0.005', '0.005', 3), (2, '0.029995', '0.025', '0.005', '0.005', 3),
              (3, '0.0100001', '0.01', '0.005', '0.005', 1)]
        r13b = audit_case(_atoms(td, Fg, lx=0.05, ly=0.05, lz=0.2, name='atom_gfar.liggghts'),
                          _contacts(td, [], name='contact_gfar.liggghts'), 3, None)
        chk('⑬b ★ 반올림 폭 밖의 "기하에만" 쌍 (겹침 5e-6 · 덤프 행 없음) → geom_only_far 1 · FLAG',
            r13b.get('geom_only_far') == 1 and r13b['verdict'] == 'FLAG')
        D = [(1, '0.02', '0.025', '0.005', '0.005', 3), (2, '0.0299', '0.025', '0.005', '0.005', 3),
             (3, '0.0100001', '0.01', '0.005', '0.005', 1)]
        a7 = _atoms(td, D, lx=0.05, ly=0.05, lz=0.2, name='atom_dev.liggghts')
        r14 = audit_case(a7, _contacts(td, [(1, 2, 0, '1e-09', '9e-05')], name='contact_dev.liggghts'), 3, None)
        chk('⑭ ★ 양쪽에 있는 쌍의 δ_덤프 9e-5 ≠ 재계산 겹침 1e-4 (차 1e-5 ≫ 폭 1.1e-7) → both_inconsistent 1 · FLAG',
            r14.get('both_inconsistent') == 1 and r14['verdict'] == 'FLAG' and abs((r14.get('both_max_dev') or 0) - 1e-5) < 1e-9)
        r14b = audit_case(a7, _contacts(td, [(1, 2, 0, '1e-09', '0.0001')], name='contact_dev_ok.liggghts'), 3, None)
        chk('⑭b 같은 쌍 · δ_덤프 = 재계산 겹침 → both_inconsistent 0 · CLEAN', r14b.get('both_inconsistent') == 0 and r14b['verdict'] == 'CLEAN')

        #  ⑮ MPI 런의 고스트 플래그 — LIGGGHTS `compute_pair_gran_local.cpp` add_pair: 두 입자 다 local 이면 0, 아니면
        #    `is_periodic_ghost(i)||is_periodic_ghost(j)`; `domain_I.h`: 고스트이고 어느 **주기** 축에서 x < lo + cutneighmax 또는
        #    x > hi − cutneighmax 이면 1.  ⇒ z 분할면 너머의 고스트 (상자 안) 도 주기면 띠 안이면 1.  cutneighmax = 2 r_max + skin.
        G = [(1, '0.04', '0.025', '0.0995', '0.0005', 3), (2, '0.04', '0.025', '0.1004', '0.0005', 3),
             (3, '0.0100001', '0.01', '0.005', '0.005', 1)]        # r_max 0.005 · skin 0.002 → 띠 0.012 · x 0.04 > 0.05 − 0.012
        deck = Path(td) / 'input_g.liggghts'
        deck.write_text('boundary        p p f\nnewton          off\nneighbor        0.002 bin\nprocessors * * *\n', encoding='utf-8')
        a6 = _atoms(td, G, lx=0.05, ly=0.05, lz=0.2, name='atom_ghost.liggghts')
        c15 = _contacts(td, [(2, 1, 1, '1e-09', '0.0001')], name='contact_ghost.liggghts')     # newton off: 고스트 행 id1 > id2
        r15 = audit_case(a6, c15, 3, None, deck_path=str(deck))
        chk('⑮ ★ 플래그만 1 쌍 = id2 주기면 띠 안 · 내부 z 분할면 걸침 → 설명됨 (격자 1x1x2) · CLEAN · cutneighmax 0.012 · skin 0.002',
            r15.get('flag_only_explained') is True and r15.get('mpi_grid_min') == '1x1x2' and r15['verdict'] == 'CLEAN'
            and abs((r15.get('cutneighmax') or 0) - 0.012) < 1e-12 and r15.get('skin') == 0.002 and r15.get('flag_not_cross') == 1)
        Gi = [(1, '0.025', '0.025', '0.0995', '0.0005', 3), (2, '0.025', '0.025', '0.1004', '0.0005', 3),
              (3, '0.0100001', '0.01', '0.005', '0.005', 1)]       # 같은 쌍인데 x 0.025 = 띠 밖 (안쪽)
        r15b = audit_case(_atoms(td, Gi, lx=0.05, ly=0.05, lz=0.2, name='atom_ghost_in.liggghts'), c15, 3, None, deck_path=str(deck))
        chk('⑮b ★ 플래그만 1 쌍인데 id2 가 띠 밖 (안쪽) → 설명 안 됨 · FLAG',
            r15b.get('flag_only_explained') is False and r15b['verdict'] == 'FLAG')
        r15c = audit_case(a6, c15, 3, None, deck_path=None)
        chk('⑮c ★ 덱 (skin) 없으면 띠를 못 정한다 → fail-closed FLAG (skin · cutneighmax 빈칸)',
            r15c['verdict'] == 'FLAG' and r15c.get('skin') is None and r15c.get('flag_only_explained') is False)
        r15d = audit_case(a6, _contacts(td, [(1, 2, 0, '1e-09', '0.0001')], name='contact_ghost0.liggghts'), 3, None, deck_path=str(deck))
        chk('⑮d 같은 침대 · 플래그 0 → 플래그만 0 · 설명 대상 없음 (None) · CLEAN',
            r15d['verdict'] == 'CLEAN' and r15d.get('flag_not_cross') == 0 and r15d.get('flag_only_explained') is None)

        # ── 자기리뷰 (09-29) 반례 ──
        #  ⑯ NaN δ (LIGGGHTS 발산 시 -nan) → 어떤 비교도 조용히 False — 따로 세어 FLAG
        r16 = audit_case(a7, _contacts(td, [(1, 2, 0, '1e-09', 'nan')], name='contact_nan.liggghts'), 3, None)
        chk('⑯ ★ δ = nan 행 → nonfinite 1 · FLAG (자기리뷰 #2)', r16['verdict'] == 'FLAG' and r16.get('nonfinite_rows') == 1)
        #  ⑰ 원자 step ≠ 접촉 step → FLAG
        c17 = _contacts(td, [(1, 2, 0, '1e-09', '0.0001')], name='contact_step.liggghts')
        Path(c17).write_text(Path(c17).read_text(encoding='utf-8').replace('ITEM: TIMESTEP\n100\n', 'ITEM: TIMESTEP\n200\n'), encoding='utf-8')
        r17 = audit_case(a7, c17, 3, None)
        chk('⑰ ★ 접촉 step 200 ≠ 원자 step 100 → FLAG (자기리뷰 #4)', r17['verdict'] == 'FLAG' and '≠ 접촉 step' in r17['why'])
        #  ⑱ 플래그 열 없음 → FLAG (조용히 건너뛰지 않는다)
        c18 = os.path.join(td, 'contact_noflag.liggghts')
        with open(c18, 'w') as fh:
            fh.write('ITEM: TIMESTEP\n100\nITEM: NUMBER OF ENTRIES\n1\nITEM: BOX BOUNDS pp pp ff\n0 10\n0 10\n0 20\n'
                     'ITEM: ENTRIES c_cpl[7] c_cpl[8] c_cpl[22] c_cpl[23]\n1 2 1e-09 0.0001\n')
        r18 = audit_case(a7, c18, 3, None)
        chk('⑱ 주기 플래그 열 없음 → FLAG (자기리뷰 #8)', r18['verdict'] == 'FLAG' and 'c_cpl[9]' in r18['why'])
        #  ⑲ 분할면 위의 반올림 토큰 — τ 없이는 격자를 못 찾는다 (자기리뷰 #1): z 0.1 (= Lz/2 정확히) · 0.1004
        Gt = [(1, '0.04', '0.025', '0.1', '0.0005', 3), (2, '0.04', '0.025', '0.1004', '0.0005', 3),
              (3, '0.0100001', '0.01', '0.005', '0.005', 1)]
        r19 = audit_case(_atoms(td, Gt, lx=0.05, ly=0.05, lz=0.2, name='atom_ghost_plane.liggghts'),
                         _contacts(td, [(2, 1, 1, '1e-09', '0.0006')], name='contact_ghost_plane.liggghts'), 3, None, deck_path=str(deck))
        chk('⑲ ★ 한 원자의 토큰이 분할면 (z = Lz/2) 위 → τ (반폭 + skin/2) 로 걸침 인정 · 설명됨 · CLEAN',
            r19['verdict'] == 'CLEAN' and r19.get('flag_only_explained') is True and r19.get('mpi_grid_min') == '1x1x2')
        #  ⑳ 충분성: 격자가 플래그를 예측하는 쌍 (분명히 걸침 · 작은 id 가 띠 안) 에 플래그가 없다 → FLAG
        #  4 (AM_P · r 0.005) – 5 (SE) 가 z = 0.1 을 **분명히** (τ = 반폭 + skin/2 ≈ 1 µm 보다 크게) 걸친다 — SE–SE 쌍은 간격이 ~1 µm 라 τ 안이다
        Gs = [(1, '0.04', '0.025', '0.0995', '0.0005', 3), (2, '0.04', '0.025', '0.1004', '0.0005', 3),
              (3, '0.0100001', '0.01', '0.005', '0.005', 1),
              (4, '0.045', '0.015', '0.0965', '0.005', 1), (5, '0.045', '0.015', '0.1015', '0.0005', 3)]
        r20 = audit_case(_atoms(td, Gs, lx=0.05, ly=0.05, lz=0.2, name='atom_ghost_suff.liggghts'),
                         _contacts(td, [(2, 1, 1, '1e-09', '0.0001'), (5, 4, 0, '1e-09', '0.0005')], name='contact_suff.liggghts'), 3, None,
                         deck_path=str(deck))
        chk('⑳ ★ 같은 격자가 플래그를 예측하는 쌍 (4–5: 분명히 걸침 · 작은 id 4 띠 안) 에 플래그 0 → 예측 누락 1 · FLAG (자기리뷰 #5c)',
            r20['verdict'] == 'FLAG' and r20.get('predicted_flag_missing') == 1)
        r20b = audit_case(_atoms(td, Gs, lx=0.05, ly=0.05, lz=0.2, name='atom_ghost_suff2.liggghts'),
                          _contacts(td, [(2, 1, 1, '1e-09', '0.0001'), (5, 4, 1, '1e-09', '0.0005')], name='contact_suff2.liggghts'), 3, None,
                          deck_path=str(deck))
        chk('⑳b 둘 다 플래그 → 예측 누락 0 · 설명됨 · CLEAN · newton off 규칙 (id1 > id2) 위반 0',
            r20b['verdict'] == 'CLEAN' and r20b.get('predicted_flag_missing') == 0 and r20b.get('flag_id_order_bad') == 0)
        r20c = audit_case(_atoms(td, Gs, lx=0.05, ly=0.05, lz=0.2, name='atom_ghost_suff3.liggghts'),
                          _contacts(td, [(1, 2, 1, '1e-09', '0.0001'), (5, 4, 1, '1e-09', '0.0005')], name='contact_suff3.liggghts'), 3, None,
                          deck_path=str(deck))
        chk('⑳c 플래그 행의 id 순서가 뒤집힘 (1 < 2) → newton off 규칙 위반 1 · FLAG (자기리뷰 #11)',
            r20c['verdict'] == 'FLAG' and r20c.get('flag_id_order_bad') == 1)
        #  ㉑ 짧은 토큰 침대 (S_obs 2) 에 0.2 µm 겹침 접촉 누락 → S 바닥 6 으로 폭이 좁아 FLAG (자기리뷰 #3)
        Sh = [(1, '0.02', '0.025', '0.005', '0.005', 3), (2, '0.0298', '0.025', '0.005', '0.005', 3)]
        r21 = audit_case(_atoms(td, Sh, lx=0.05, ly=0.05, lz=0.2, name='atom_short.liggghts'),
                         _contacts(td, [], name='contact_short.liggghts'), 3, None)
        chk('㉑ ★ 토큰 자릿수 ≤ 3 인 침대 (S_obs 3 → 적용 6): 겹침 2e-4 접촉 누락 → geom_only_far 1 · FLAG',
            r21['verdict'] == 'FLAG' and r21.get('sigfigs_obs') == 3 and r21.get('sigfigs') == 6 and r21.get('geom_only_far') == 1)
        #  ㉒ CLI: SKIPPED 행 (status ≠ RAW_OK) 은 rc 를 가리지 않고 · sha 불일치는 INPUT_ERROR · FLAG 가 rc 3 으로 앞선다
        post2 = Path(td) / 'cohort' / 'c2' / 'post'
        post2.mkdir(parents=True)
        shutil.copy(a1, post2 / 'atom_100.liggghts')
        shutil.copy(os.path.join(td, 'contact_2f.liggghts'), post2 / 'contact_100.liggghts')    # 2 프레임 → FLAG
        shutil.copy(stl, post2 / 'mesh_100.stl')
        tsv2 = Path(td) / 'cohort2.tsv'
        tsv2.write_text('# 합성\ncase\tstatus\tn_types\tdesign_family\tatom_file\tatom_sha256\tcontact_file\n'
                        f'c1\tRAW_OK\t3\tlhs\t{post / "atom_100.liggghts"}\t\t{post / "contact_100.liggghts"}\n'
                        f'c2\tRAW_OK\t3\tlhs\t{post2 / "atom_100.liggghts"}\t\t{post2 / "contact_100.liggghts"}\n'
                        f'perc\tDECK_MISSING+RAW_MISSING_ATOM\t\tUNKNOWN\t.\t\t.\n'
                        f'c3\tRAW_OK\t3\tlhs\t{post / "atom_100.liggghts"}\t{"0" * 64}\t{post / "contact_100.liggghts"}\n', encoding='utf-8')
        od2 = Path(td) / 'out2'
        rc2 = main(['--cohort', str(tsv2), '--out', str(od2)])
        js2 = json.loads((od2 / 'contact_audit.json').read_text(encoding='utf-8'))
        st2 = {r_['case']: r_['status'] for r_ in js2['rows']}
        chk('㉒ CLI: perc → SKIPPED · c3 (sha 불일치) → INPUT_ERROR · c2 FLAG → rc 3 (FLAG 가 입력 오류보다 앞선다 · 자기리뷰 #6)',
            rc2 == 3 and st2 == {'c1': 'OK', 'c2': 'OK', 'perc': 'SKIPPED', 'c3': 'INPUT_ERROR'}
            and js2['meta']['summary']['verdict'] == {'CLEAN': 1, 'FLAG': 1})
        os.remove(post / 'mesh_100.stl')
        od3 = Path(td) / 'out3'
        rc3 = main(['--cohort', str(tsv), '--out', str(od3)])
        js3 = json.loads((od3 / 'contact_audit.json').read_text(encoding='utf-8'))
        chk('㉒b 같은 step 메시 없음 → NO_MESH (CLEAN 아님) · rc 2 (자기리뷰 #7)', rc3 == 2 and js3['rows'][0]['status'] == 'NO_MESH')

    print()
    if fails:
        print(f'✗ {len(fails)} 건 실패')
        return 1
    print('✓ 전부 통과 — 감사기가 반례 (다중 프레임 · 중복 · 주기 누락 · δ≤0 · 플래그 어긋남) 를 잡는다.  '
          '⚠ 실제 130 덤프가 깨끗하다는 뜻은 아니다 (WSL 실행 결과를 볼 것)')
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description='LHS 접촉 덤프 읽기 전용 점검 (J20-a ⓐ) — 프레임 수 · 중복 쌍 · δ≤0 · '
                                             '주기 플래그 ↔ 기하 재계수 · 상별 벽 접촉 비율.  인계 값은 만들지 않는다')
    ap.add_argument('--cohort', default=str(HB.COHORT), help='코호트 TSV (기본: 봉인 area_s2_cohort.tsv)')
    ap.add_argument('--case', action='append', default=[], help='이 case 만 (여러 번 줄 수 있다)')
    ap.add_argument('--root-from', default='', help='코호트 경로 접두사 (치환 전)')
    ap.add_argument('--root-to', default='', help='실제 경로 접두사로 치환')
    ap.add_argument('--out', help='산출 폴더 (contact_audit.tsv · contact_audit.json)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.out:
        ap.error('--out 이 필요하다')
    return run(a)


if __name__ == '__main__':
    sys.exit(main())
