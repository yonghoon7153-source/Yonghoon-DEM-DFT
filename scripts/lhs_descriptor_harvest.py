#!/usr/bin/env python3
"""LHS 130 구조 디스크립터 수확기 — **일곱 등록 열을 원 dump 에서** 낸다.

    python3 scripts/lhs_descriptor_harvest.py --atom post/atom_2425000.liggghts \\
        --contact post/contact_2425000.liggghts --mesh post/mesh.stl \\
        --n-types 3 --case lhs00_000
    python3 scripts/lhs_descriptor_harvest.py --selftest

이 파일은 **판정문 §7 의 최소 계약 6개**를 도구에 고정한 것이다.
판정 = `docs/reviews/codex_verdict_lhs_descriptors_20260913.md` (HOLD) · 원장 `DESC-01~09`.
선례 = `lhs_perc_extract.py` — *"추출기와 경계 fixture 를 **결과 전에** 커밋해야 이 규약이
실재한다"* (Codex R11 B1).  그 파일의 덤프 읽기·경계 검사·쌍 찾기를 **재사용**한다
(규율 ①: 새로 짜기 전에 리포에 있는 것부터 — 어댑터에서 `run_contract.py` 를 못 보고 새로
짠 것이 `PA12-01~05` 의 절반이었다).

═══ 왜 `full_metrics.json` 을 읽지 않나 ═══

`DESC-01` 이 재현한 것: `dem_analysis_core.py:938` 이 `phi_se` 를 **이미 계산해 놓고**
`:941` 에서 τ 가 없으면 `return None` 하고, `analyze_contacts.py:430` 의 `if eff_cond:`
가드가 **기하량인 φ 두 개를 통째로 누락**시킨다.  `NET_MERGE_KEYS` 에도 φ 가 없어 복구되지
않는다.  ⇒ 완전행 필터로 학습셋을 만들면 **연결성이 약한 침대가 구조 타깃째 탈락**한다
= 결측이 물리와 상관된다.  파생물을 읽으면 그 결함을 그대로 상속한다.

═══ 계약 ① — 일곱 별칭 ↔ 실제 계산량 ═══

기호: `V_B = L_x·L_y·H` (H = **플래튼 높이**, §계약⑤) · `V_i = 4πr_i³/3`.

| 등록 별칭 | 이 도구가 내는 양 |
|---|---|
| `phi_se`  | `Σ_{i∈SE} V_i / V_B`.  **τ·전도도와 무관하게** 항상 낸다 (계약②) |
| `phi_am`  | `Σ_{i∈AM} V_i / V_B` — **직접 합**이다.  `1−φ_SE−ε/100` 같은 잔차가 아니다 |
| `coverage_AM_P_hertz_pct` | 아래 `c_i` 의 **AM_P 입자별 산술평균** (유효 분모만) |
| `coverage_AM_S_hertz_pct` | 같은 계산의 AM_S 평균 |
| `coverage_AM_total_hertz_pct` | `(N_P·C_P + N_S·C_S)/(N_P+N_S)`, **실측 입자수** 가중 |
| `tortuosity_dijkstra_SE` | SE 접촉그래프 최단경로 / 끝점 z 거리 — 아래 §τ |
| `porosity_sphere_pct_RECORD_ONLY` | `100(1 − Σ_i V_i / V_B)`.  겹침을 빼지 않는다 |

**Hertz 피복률의 정확한 정의** (`dem_analysis_core.py:172` 규약):
```
F_i = 4π r_i²  −  Σ(i 에 붙은 AM–AM 접촉면적)
c_i = min(100, 100 · Σ(i 에 붙은 AM–SE 접촉면적) / F_i)      [F_i > 0]
c_i = FREE_SURFACE_INVALID                                    [F_i ≤ 0]
```
분자는 **LIGGGHTS 가 보고한 `contact_area`**(`c_cpl[22]`)다 — 이 도구가 `πR*δ` 를 다시
계산하는 것이 **아니다**.  ⚠ `F_i ≤ 0` 을 **0 으로 접지 않는다** (`DESC-05`: 실제 무접촉과
분모 붕괴가 섞인다).  cap 발동 횟수와 분모붕괴 횟수를 **따로** 보고한다.

⚠⚠ **`hertz` 라는 별칭은 물려받은 오해다** (`L1-04`, 2026-09-13 L1 판정).  공식 LIGGGHTS
문서·구현에서 `contactArea` 는 역학 해가 아니라 **기하학적 교차 원판**이다:
`A_LIGG = π(rδ − δ²/4)` vs `A_Hertz = πR*δ` ⇒ 동일 반경에서 비 = `2 − δ/(2r)`
(r = 0.5 µm · δ/R\* = 0.05 에서 **1.9875배**, 이 리포에서 재현).  등록 별칭은 **바꾸지
않지만**(판정문: *"기존 키와 frozen feature 를 세대 표시 없이 바꾸면 안 된다"*) 매 행에
`area_channel` 을 박아 **무엇을 센 값인지**를 남긴다.  권고 이름 구분은
`A_dem_geometric` / `A_hertz_elastic` / `A_plastic_model` 이다.

⚠ **전체 평균의 함정** (판정문 반례): P 1개·10 % · S 3개·각 90 % 이면 **전체 70 %** 다.
상 평균의 평균은 50 %, 총면적비는 30 %, 질량가중은 18 % — **넷이 다른 양**이다.

⚠ **Physics 피복률은 여기서 계산하지 않는다** (계약④).  `DESC-03` 이 `plastic_coverage.py`
의 `A_volume = V_overlap / H_FILM_MIN` 에서 **확대 DEM 길이 ÷ 미확대 5 nm** 혼용을
재현했고, 그 때문에 `min(caps)` 의 binding cap 이 `tabor ↔ volume` 로 뒤집힌다.  Hertz 는
그 영향 밖이지만(재현 결과 불변), **섞지 않기 위해** 이 도구는 Physics 를 아예 안 부른다.

═══ §τ — 계약 ③ ═══

`DESC-02` 가 양방향 반례를 냈다:
① `dem_analysis_core.py:502-509` 가 바닥판 source 가 없으면 **위판에 닿는 성분의 최저 z**
   를 새 source 로 승격한다 ⇒ `percolation_pct = 0` 인데 `τ = 1` 이 나온다.
② 같은 함수 `:517-522` 가 `src × top` 전수 쌍을 shuffle 해 앞 200 개만 남기므로 **서로 다른
   성분의 무경로 쌍**이 예산을 먹는다 ⇒ 관통 성분이 200 개여도 `τ = None` 이 된다.

이 도구의 규약 (**legacy 와 다르다 — 같은 컬럼에 섞지 말 것**, `DESC-04`):
- **fallback source 승격 없음.**  source = 아래 슬래브의 SE **이면서** 위 슬래브에 닿는
  성분의 구성원.  없으면 `NOT_PERCOLATING` 이고 **유한 τ 를 내지 않는다**.
- **쌍은 같은 성분 안에서만** 뽑는다 ⇒ 예산이 무경로 쌍에 소진되지 않는다.
- **간선 가중치와 경로 길이는 xy 최소영상**(`_mi_dist`) — 쌍 찾기와 **같은 규약**이다.
  (`P1-HARV-01`: 초판은 raw 좌표차를 써서 평행이동만으로 τ 가 9.66배 바뀌었다.)
- 슬래브 = 고체(AM ∪ SE) z 범위 `[min(z−r), max(z+r)]` 의 양 끝, 두께 = `r_SE,max`.
  (`lhs_perc_extract` ④ 와 같은 사고 — AM 만의 범위를 쓰면 희박한 침대에서 판정이 쉬워진다.)
  ⚠⚠ **이 규약은 아직 정당화되지 않았다** (`LHS-08`, 열림).  z 범위는 **전 입자(AM 포함)**
  가 정하는데 밴드 소속은 **SE 만** 보므로, AM 이 SE 보다 위로 솟은 침대는 위 밴드가
  구조적으로 빌 수 있다 — 실제 전극면인 `plate_z_sim` 은 이미 출력에 있는데 **안 쓴다**.
  ⇒ 산출물에 `band_detail.alt_n_top`(plate_z 규약이면 몇 명인지)을 **진단으로만** 적는다.
  규약을 바꾸는 것은 재측정 **뒤**다 — 먼저 바꾸면 바꾼 규약으로 잰 수로 그 규약을
  정당화하게 된다 (`규율 ⑤`: 후보를 고르는 코드가 곧 사각지대).
- 통계량을 **이름으로 가른다**: `tau_mean`(절단본, legacy 호환) · `tau_median` ·
  `tau_mean_untruncated` · `n_truncated`.  등록 별칭 `tortuosity_dijkstra_SE` = **`tau_mean`**.
  ⚠ 판정문 반례: `[1,1,10]` → mean **4** / recommended **1**; `[1, 20.024984]` → 절단 후
  mean **1** vs 무절단 **10.512492**.  이름이 통계량을 정하지 않으면 target 이 갈린다.

═══ 계약 ⑤ — 프로비넌스 fail-closed ═══

- atom · contact 덤프의 **TIMESTEP 이 같아야** 한다.  다르면 거부.
  (`DESC-06`: `parse_liggghts.py:243` 은 종류별 최신 파일을 **독립 선택**해 `atom_100 +
  contact_200` 을 rc=0 으로 받았다.  그리고 그 파서는 **모든 프레임 행을 이어 붙인다**.)
- `H`(플래튼 높이)는 **mesh STL 또는 명시 `--plate-z`** 로만 받는다.  **추정 금지** —
  `dem_analysis_core.py:110` 의 "mesh 없으면 최고 입자 중심" 이 부피분율에 **5.263 %**
  상대차를 낸다.
- 모든 원파일의 **sha256** 과 상별 입자수, **target 별 상태**를 함께 낸다.
- `--n-types` **필수** (`lhs_perc_extract` ⑥ 과 같은 이유: AM_P 가 우연히 0개면 2-type 으로
  보이고 AM_S 가 SE 로 오사상된다).

═══ 계약 ⑥ — 130 단독 ═══

출력은 자기 CSV/JSON 이다.  `design_performance_corpus.csv` 291 행과 **합치지 않는다**
(`DESC-08`: `d_am=0` 40 건이 지금도 학습 입력에 들어가고 `use_porosity_pct` closure 잔차가
ε SD 의 77.82 % 다).  `docs/lhs_design_dataset_20260818.md` §O-4 ⑤ 와 같은 결론.

═══ 상태 코드 ═══

`OK` · `N_A_PHASE_ABSENT`(없는 상 — 존재하는데 무접촉인 `0` 과 다르다) ·
`NOT_PERCOLATING` · **`ELECTRODE_BAND_EMPTY`** · `NO_VALID_SAMPLED_PAIR` ·
`FREE_SURFACE_INVALID` · `INPUT_MISSING`.
⚠ 한 타깃이 미정의라고 **다른 타깃이 있는 행을 통째로 버리지 않는다** (`DESC-01` 의 교훈).
⚠ `ELECTRODE_BAND_EMPTY` 는 `NOT_PERCOLATING` 의 **하위분류가 아니라 다른 사유**다
(`LHS-08`): 전자는 **규약(밴드 정의)** 을, 후자는 **물리(연결성)** 를 겨눈다.  둘을 같은
값으로 내면 *"코드 문제냐"* 에 답할 수 없다 — 실제로 130 중 116 이 그 상태였다.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

#  ★ 규율 ①: 덤프 읽기·경계 검사·주기 쌍 찾기·상 사상은 **이미 봉인돼 있다**.
from lhs_perc_extract import (  # noqa: E402
    AM_LABELS, BedRefusal, REQUIRED_BC, TYPE_MAP,
    _pairs_within, check_boundary_flags, read_atom_dump,
)

#: 계약 ③ — τ 표본 예산.  legacy 와 같은 수지만 **같은 성분 안에서만** 쓴다.
N_TAU_PAIRS = 200
#: 계약 ③ — legacy 절단 구간 (`dem_analysis_core.py:533`).
TAU_LO, TAU_HI = 1.0, 20.0
#: 접촉 덤프의 면적·겹침 열 (`parse_liggghts.py:47` 과 같은 규약).
COL_AREA, COL_D1, COL_D2 = 'c_cpl[22]', 'c_cpl[7]', 'c_cpl[8]'
#: L1-04 — 이 열이 **무엇인지** 매 행에 박는다 (별칭의 `hertz` 는 물려받은 오해다).
AREA_CHANNEL = ('dem_geometric_c_cpl22 — LIGGGHTS 기하 교차 원판 pi(r d - d^2/4); '
                'Hertz 탄성 pi R* d 가 **아니다** (동일 반경 비 = 2 - d/(2r))')

STATUS_OK = 'OK'
STATUS_ABSENT = 'N_A_PHASE_ABSENT'
STATUS_NOPERC = 'NOT_PERCOLATING'
#: LHS-08 — `NOT_PERCOLATING` 이 접고 있던 **다른 원인**: 전극 밴드에 SE 가 0 명이라
#: 성분을 볼 것도 없이 끝난 경우.  ⓐ(밴드 빔)/ⓑ(진짜 미관통)를 같은 값으로 내면
#: 실물 116 건이 어느 쪽인지 **산출물만으로 판별 불가**다.
STATUS_BAND_EMPTY = 'ELECTRODE_BAND_EMPTY'
STATUS_NOPAIR = 'NO_VALID_SAMPLED_PAIR'
STATUS_MISSING = 'INPUT_MISSING'


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for blk in iter(lambda: fh.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()


def last_timestep(path):
    """마지막 `ITEM: TIMESTEP` 값.  atom·contact 덤프 모두에 쓴다 (계약⑤)."""
    ts = None
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        want = False
        for ln in fh:
            if want:
                try:
                    ts = int(float(ln.split()[0]))
                except (ValueError, IndexError):
                    pass
                want = False
            elif ln.startswith('ITEM: TIMESTEP'):
                want = True
    if ts is None:
        raise BedRefusal(f'{path}: `ITEM: TIMESTEP` 이 없다')
    return ts


def read_contact_dump(path):
    """**마지막 프레임만**의 (id1, id2, contact_area).

    ⚠ `parse_liggghts.parse_contact_file` 은 모든 프레임 행을 **이어 붙인다**
    (`DESC-06`).  여기서는 마지막 `ITEM: ENTRIES` 블록만 읽는다.
    """
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        lines = fh.read().splitlines()
    starts = [i for i, ln in enumerate(lines) if ln.startswith('ITEM: ENTRIES')]
    if not starts:
        raise BedRefusal(f'{path}: `ITEM: ENTRIES` 가 없다 — LIGGGHTS local 덤프가 아니다')
    i = starts[-1]
    headers = lines[i].replace('ITEM: ENTRIES', '').strip().split()
    for col in (COL_D1, COL_D2, COL_AREA):
        if col not in headers:
            raise BedRefusal(
                f'{path}: 접촉 열 {col} 이 없다 (있는 열: {headers}).  '
                'DEM contact-area 규약을 모르는 채로 피복률을 내지 않는다')
    ia, i1, i2 = headers.index(COL_AREA), headers.index(COL_D1), headers.index(COL_D2)
    id1, id2, area = [], [], []
    i += 1
    while i < len(lines) and not lines[i].startswith('ITEM:'):
        v = lines[i].split()
        if len(v) == len(headers):
            id1.append(int(float(v[i1])))
            id2.append(int(float(v[i2])))
            area.append(float(v[ia]))
        i += 1
    return (np.asarray(id1, dtype=np.int64), np.asarray(id2, dtype=np.int64),
            np.asarray(area, dtype=np.float64), tuple(headers))


def plate_z_from_stl(path):
    """`parse_liggghts.parse_mesh_stl` 과 **같은 정의** — 전 꼭짓점 z 평균."""
    zs = []
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        for ln in fh:
            p = ln.split()
            if len(p) == 4 and p[0] == 'vertex':
                zs.append(float(p[3]))
    if not zs:
        raise BedRefusal(f'{path}: STL 에 vertex 가 없다')
    return float(np.mean(zs))


def phase_labels(types, n_types):
    """계약⑤ — 선언 밖 type 이 있으면 거부한다."""
    tmap = TYPE_MAP[n_types]
    seen = set(int(t) for t in np.unique(types))
    bad = sorted(seen - set(tmap))
    if bad:
        raise BedRefusal(f'선언(--n-types {n_types}) 밖 type {bad} 이 파일에 있다')
    return np.asarray([tmap[int(t)] for t in types], dtype=object), tmap


Z_FLOOR = 0.0      # 바닥 벽 — LHS 덱 `wall/gran … zplane 0.0`.  웹앱 `dem_analysis_core.calc_porosity` 의 V_box = L²·plate_z 와 같은 규약


def volumes_and_phi(atoms, labels, box_lo, box_hi, plate_z):
    """계약② — φ 는 **기하만**으로, τ·전도도 성공과 무관하게.

    ⛔ LHS-10 (2026-09-24): 옛 판은 분모 높이를 `plate_z − box_lo[2]` (덤프 상자 바닥) 로 쟀다.  덱 상자가 벽보다 10 µm 아래서
      시작해 (`region … -0.01 1.0`) 입자가 없는 층이 분모에 들어갔다 — φ 가 0.742–0.825 배, porosity 중앙 30.65 % (벽 기준 9.89 %).
      이제 **벽 (Z_FLOOR)** 에서 잰다.  입자가 벽 아래 (z − r < Z_FLOOR − ½·r_max) 에 있으면 그 가정이 안 맞는 덱이라 거부한다.
    """
    r = atoms['radius']
    v = (4.0 / 3.0) * np.pi * r ** 3
    lx = float(box_hi[0] - box_lo[0])
    ly = float(box_hi[1] - box_lo[1])
    zb = float((atoms['z'] - r).min())
    if zb < Z_FLOOR - 0.5 * float(r.max()):
        raise BedRefusal(f'입자가 벽 (z = {Z_FLOOR}) 아래에 있다: min(z − r) = {zb:.6g} — 벽 = 0 가정이 이 덱에 맞지 않는다 (LHS-10)')
    h = float(plate_z - Z_FLOOR)
    if not (lx > 0 and ly > 0 and h > 0):
        raise BedRefusal(f'전극 부피가 양수가 아니다: lx={lx} ly={ly} H={h}')
    v_box = lx * ly * h
    is_se = labels == 'SE'
    is_am = np.asarray([l in AM_LABELS for l in labels])
    phi_se = float(v[is_se].sum() / v_box)
    phi_am = float(v[is_am].sum() / v_box)
    eps = 100.0 * (1.0 - float(v.sum()) / v_box)
    return dict(phi_se=phi_se, phi_am=phi_am,
                porosity_sphere_pct_RECORD_ONLY=eps,
                V_box_sim=v_box, H_sim=h, lx_sim=lx, ly_sim=ly, z_floor_sim=Z_FLOOR, solid_bot_sim=zb,
                closure_residual=phi_se + phi_am + eps / 100.0 - 1.0)


def coverage_hertz(ids, labels, radius, c1, c2, carea):
    """계약① — Hertz 피복률.  단위는 면적/면적이라 **scale 에 불변**이다."""
    pos = {int(a): k for k, a in enumerate(ids)}
    n = len(ids)
    free = 4.0 * np.pi * radius ** 2
    am_se = np.zeros(n)
    for a, b, ar in zip(c1, c2, carea):
        ka, kb = pos.get(int(a)), pos.get(int(b))
        if ka is None or kb is None:
            continue
        la, lb = labels[ka], labels[kb]
        a_am, b_am = la in AM_LABELS, lb in AM_LABELS
        if a_am and b_am:
            free[ka] -= ar
            free[kb] -= ar
        elif a_am and lb == 'SE':
            am_se[ka] += ar
        elif b_am and la == 'SE':
            am_se[kb] += ar

    out, n_cap, n_bad = {}, 0, 0
    per = np.full(n, np.nan)
    for k in range(n):
        if labels[k] not in AM_LABELS:
            continue
        if free[k] <= 0:
            n_bad += 1
            continue
        c = 100.0 * am_se[k] / free[k]
        if c > 100.0:
            c, n_cap = 100.0, n_cap + 1
        per[k] = c

    counts = {}
    for lab in ('AM_P', 'AM_S', 'AM'):
        sel = np.asarray([l == lab for l in labels])
        n_exist = int(sel.sum())
        vals = per[sel & ~np.isnan(per)]
        counts[lab] = dict(n_particles=n_exist, n_valid=int(vals.size))
        if n_exist == 0:
            out[lab] = (None, STATUS_ABSENT)
        elif vals.size == 0:
            out[lab] = (None, 'FREE_SURFACE_INVALID')
        else:
            out[lab] = (float(vals.mean()), STATUS_OK)

    #  ★ 전체 = **실측 입자수 가중** (상 평균의 평균도, 총면적비도, 질량가중도 아니다).
    num = den = 0.0
    for lab in ('AM_P', 'AM_S', 'AM'):
        val, st = out[lab]
        if st == STATUS_OK:
            w = counts[lab]['n_valid']
            num += w * val
            den += w
    total = (float(num / den), STATUS_OK) if den > 0 else (None, 'FREE_SURFACE_INVALID')
    return dict(per_phase=out, total=total, counts=counts,
                n_capped=n_cap, n_free_surface_invalid=n_bad)


def _mi_dist(p, q, lx, ly):
    """xy **주기** · z 개방의 최소영상 거리.

    ⚠ `P1-HARV-01` (L4/L5 판정, 2026-09-13): 초판은 쌍 찾기만 주기로 하고 **간선 가중치와
    경로 길이는 raw 좌표차**로 계산했다.  그래서 **같은 침대를 평행이동만 해도** τ 가
    9.850888284819803 → 1.0198039027185568 (**9.6596배**) 로 바뀌었다.
    `_pairs_within` 이 minimum-image 로 이웃을 찾는 한, 길이도 같은 규약이어야 한다.
    """
    d = p - q
    d[0] -= lx * round(d[0] / lx)
    d[1] -= ly * round(d[1] / ly)
    return float(np.linalg.norm(d))


def tortuosity_se(atoms, labels, box_lo, box_hi, n_pairs=N_TAU_PAIRS, seed=42,
                  plate_z=None):
    """계약③ — fallback source 승격 **없음**, 쌍은 **같은 성분 안에서만**.

    ★ `LHS-08` (2026-09-19): 초판은 **두 개의 `return base`** 가 같은 `NOT_PERCOLATING`
    을 냈다 — ⓐ 전극 밴드에 SE 가 0 명이라 **볼 성분이 애초에 없던** 경우와 ⓑ 밴드는
    찼는데 어떤 성분도 두 밴드를 못 잇던 경우.  실물 130 중 **116** 이 그 값이었고
    산출물만으로는 어느 쪽인지 알 수 없었다 ⇒ *"우리 코드 문제냐"* 에 답할 수가 없었다.
    ⓐ 는 규약(밴드 정의)을 겨누고 ⓑ 는 물리를 겨누는데 **처방이 정반대**다.
    ⇒ ⓐ = `ELECTRODE_BAND_EMPTY`, ⓑ = `NOT_PERCOLATING`, 그리고 두 경우 모두
    `band_detail` 에 **왜 그랬는지 세는 수**를 남긴다.

    ⚠ `plate_z` 는 **진단 전용**이다.  보고되는 τ 도 `tau_convention` 도 `solid_zrange`
    규약 **그대로**다 (selftest ⑭ 가 그것을 강제한다).  규약 판단은 재측정 **뒤**다 —
    LHS-08 처방 순서 = 진단 분리 → 재측정 → 규약 판단.  순서를 바꾸면 규약을 바꾼 뒤
    그 규약으로 잰 수로 규약을 정당화하게 된다.
    """
    import networkx as nx

    sel = np.flatnonzero(np.asarray([l == 'SE' for l in labels]))
    band = dict(
        n_se=int(sel.size), z_lo=None, z_hi=None, band_t=None,
        se_z_lo=None, se_z_hi=None, n_bot=0, n_top=0,
        n_components=0, n_span_components=0,
        largest_comp_frac=None, largest_comp_z_span_frac=None,
        alt_plate_z=(None if plate_z is None else float(plate_z)),
        alt_n_top=None, alt_plate_above_solid=None,
        alt_note=('진단 전용 (LHS-08) — 위 전극면을 plate_z 로 뒀을 때의 밴드 인원. '
                  '보고 τ 는 solid_zrange 규약 그대로이며 이 수는 τ 에 안 들어간다.'))
    base = dict(tau_mean=None, tau_median=None, tau_mean_untruncated=None,
                n_sampled=0, n_valid=0, n_truncated=0, status=STATUS_NOPERC,
                tau_convention='harvest_v1/solid_zrange/rSEmax/no_fallback/same_component',
                band_detail=band)
    if sel.size < 2:
        base['status'] = STATUS_ABSENT
        return base

    r_all, z_all = atoms['radius'], atoms['z']
    z_lo = float((z_all - r_all).min())
    z_hi = float((z_all + r_all).max())
    xyz = np.column_stack([atoms['x'][sel], atoms['y'][sel], atoms['z'][sel]])
    rad = r_all[sel]
    t = float(rad.max())
    lx = float(box_hi[0] - box_lo[0])
    ly = float(box_hi[1] - box_lo[1])
    band.update(z_lo=z_lo, z_hi=z_hi, band_t=t,
                se_z_lo=float((xyz[:, 2] - rad).min()),
                se_z_hi=float((xyz[:, 2] + rad).max()))

    pairs = _pairs_within(xyz, rad, lx, ly, z_pad=t)
    G = nx.Graph()
    G.add_nodes_from(range(sel.size))
    for i, j in pairs:
        d = _mi_dist(xyz[i].copy(), xyz[j].copy(), lx, ly)   # ★ P1-HARV-01
        G.add_edge(int(i), int(j), distance=d)

    #  ★ LHS-08: 성분 통계를 **밴드 검사 전에** 낸다 — ⓐ 로 빠져도 "SE 가 한 덩어리였나
    #  산산조각이었나" 를 알아야 밴드 정의가 용의자인지 판별된다.
    comps = list(nx.connected_components(G))
    band['n_components'] = int(len(comps))
    if comps:
        big = max(comps, key=len)
        bi = np.fromiter(big, dtype=np.int64, count=len(big))
        band['largest_comp_frac'] = float(len(big) / sel.size)
        _span = float((xyz[bi, 2] + rad[bi]).max() - (xyz[bi, 2] - rad[bi]).min())
        band['largest_comp_z_span_frac'] = (
            float(_span / (z_hi - z_lo)) if z_hi > z_lo else None)

    bot = set(np.flatnonzero((xyz[:, 2] - rad) <= z_lo + t).tolist())
    top = set(np.flatnonzero((xyz[:, 2] + rad) >= z_hi - t).tolist())
    band.update(n_bot=int(len(bot)), n_top=int(len(top)))
    if plate_z is not None:                    # ⚠ 진단만 — τ 에 안 들어간다
        band['alt_n_top'] = int(np.count_nonzero(
            (xyz[:, 2] + rad) >= float(plate_z) - t))
        band['alt_plate_above_solid'] = bool(float(plate_z) >= z_hi)
    if not bot or not top:
        base['status'] = STATUS_BAND_EMPTY      # ⓐ — 규약(밴드 정의)이 용의자
        return base

    cands = []
    for comp in comps:
        cb, ct = comp & bot, comp & top
        if cb and ct:
            cands.append((sorted(cb), sorted(ct)))
    band['n_span_components'] = int(len(cands))
    if not cands:                                   # ⓑ — 유한 τ 를 내지 않는다 (물리)
        return base

    rng = np.random.default_rng(seed)
    allp = [(s, tt) for cb, ct in cands for s in cb for tt in ct if s != tt]
    if not allp:
        base['status'] = STATUS_NOPAIR
        return base
    idx = rng.permutation(len(allp))[:n_pairs]
    taus = []
    for k in idx:
        s, tt = allp[int(k)]
        try:
            path = nx.shortest_path(G, s, tt, weight='distance')
        except nx.NetworkXNoPath:                   # 같은 성분이라 원래 안 난다
            continue
        plen = sum(_mi_dist(xyz[path[m]].copy(), xyz[path[m + 1]].copy(), lx, ly)
                   for m in range(len(path) - 1))              # ★ P1-HARV-01
        dz = abs(float(xyz[tt, 2] - xyz[s, 2]))
        if dz > 0:
            taus.append(plen / dz)

    if not taus:
        base['status'] = STATUS_NOPAIR
        base['n_sampled'] = int(len(idx))
        return base
    raw = np.asarray(taus)
    keep = raw[(raw >= TAU_LO) & (raw < TAU_HI)]
    base.update(n_sampled=int(len(idx)), n_valid=int(raw.size),
                n_truncated=int(raw.size - keep.size),
                tau_mean_untruncated=float(raw.mean()))
    if keep.size == 0:
        base['status'] = STATUS_NOPAIR
        return base
    base.update(tau_mean=float(keep.mean()), tau_median=float(np.median(keep)),
                status=STATUS_OK)
    return base


def harvest(atom_path, contact_path, n_types, case, plate_z=None, mesh_path=None,
            allow_any_bc=False, n_pairs=N_TAU_PAIRS):
    for p in (atom_path, contact_path):
        if not os.path.exists(p):
            raise BedRefusal(f'{p}: 없다')
    ts_a, ts_c = last_timestep(atom_path), last_timestep(contact_path)
    if ts_a != ts_c:
        raise BedRefusal(
            f'TIMESTEP 불일치: atom={ts_a} contact={ts_c}.  '
            '종류별 최신 파일을 독립 선택하면 다른 프레임이 섞인다 (DESC-06)')

    atoms, box_lo, box_hi, bc = read_atom_dump(atom_path)
    bc_note = check_boundary_flags(bc, allow_any_bc)
    if 'id' not in atoms:
        pass
    labels, tmap = phase_labels(atoms['type'], n_types)

    if (plate_z is None) == (mesh_path is None):
        raise BedRefusal('플래튼 높이는 --mesh 또는 --plate-z 로 **정확히 하나** 주어야 한다.  '
                         '추정하지 않는다 (DESC-06: 최고 입자 중심 추정은 5.263 % 상대차)')
    if mesh_path is not None:
        if not os.path.exists(mesh_path):
            raise BedRefusal(f'{mesh_path}: 없다')
        plate_z = plate_z_from_stl(mesh_path)
        h_src = 'mesh_stl'
    else:
        h_src = 'cli_explicit'

    phi = volumes_and_phi(atoms, labels, box_lo, box_hi, plate_z)

    ids = _atom_ids(atom_path)
    c1, c2, carea, cheaders = read_contact_dump(contact_path)
    cov = coverage_hertz(ids, labels, atoms['radius'], c1, c2, carea)
    #  plate_z 는 **진단 전용**으로만 넘긴다 (LHS-08) — 보고 τ 의 규약은 안 바뀐다.
    tau = tortuosity_se(atoms, labels, box_lo, box_hi, n_pairs=n_pairs,
                        plate_z=plate_z)

    raw = {'atom': dict(path=os.path.basename(atom_path), sha256=sha256_of(atom_path)),
           'contact': dict(path=os.path.basename(contact_path),
                           sha256=sha256_of(contact_path))}
    if mesh_path:
        raw['mesh'] = dict(path=os.path.basename(mesh_path), sha256=sha256_of(mesh_path))

    cp, sp = cov['per_phase']['AM_P']
    cs, ss = cov['per_phase']['AM_S']
    ca, sa = cov['per_phase']['AM']
    ct, st = cov['total']
    if n_types == 2:                       # 2-type 침대는 AM 이 한 상이다
        cp, sp = None, STATUS_ABSENT
        cs, ss = None, STATUS_ABSENT
        ct, st = (ca, sa)

    return dict(
        case=case, timestep=ts_a, n_types=n_types, type_map=tmap,
        phase_counts={k: int(sum(1 for l in labels if l == k)) for k in tmap.values()},
        boundary=bc_note, plate_z_sim=float(plate_z), plate_z_source=h_src,
        phi_se=phi['phi_se'], phi_am=phi['phi_am'],
        porosity_sphere_pct_RECORD_ONLY=phi['porosity_sphere_pct_RECORD_ONLY'],
        closure_residual=phi['closure_residual'],
        coverage_AM_P_hertz_pct=cp, coverage_AM_S_hertz_pct=cs,
        coverage_AM_total_hertz_pct=ct, coverage_AM_only_hertz_pct=ca,
        tortuosity_dijkstra_SE=tau['tau_mean'],
        status=dict(phi=STATUS_OK, porosity=STATUS_OK,
                    coverage_AM_P=sp, coverage_AM_S=ss, coverage_AM_total=st,
                    tortuosity=tau['status']),
        tau_detail=tau, coverage_detail=dict(
            n_capped=cov['n_capped'],
            n_free_surface_invalid=cov['n_free_surface_invalid'],
            counts=cov['counts'], contact_headers=cheaders),
        V_box_sim=phi['V_box_sim'], raw=raw, area_channel=AREA_CHANNEL,
        contract='codex_verdict_lhs_descriptors_20260913 §7 (1~6)')


def _atom_ids(path):
    """원자 덤프의 `id` 열 (접촉 덤프의 id 와 맞춘다)."""
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        lines = fh.read().splitlines()
    starts = [i for i, ln in enumerate(lines) if ln.startswith('ITEM: ATOMS')]
    i = starts[-1]
    headers = lines[i].replace('ITEM: ATOMS', '').strip().split()
    if 'id' not in headers:
        raise BedRefusal(f'{path}: `id` 열이 없다 — 접촉 덤프와 입자를 맞출 수 없다')
    k = headers.index('id')
    out = []
    i += 1
    while i < len(lines) and not lines[i].startswith('ITEM:'):
        v = lines[i].split()
        if len(v) == len(headers):
            out.append(int(float(v[k])))
        i += 1
    return np.asarray(out, dtype=np.int64)


# ──────────────────────────────────────────────────────────────────────────────
# 자기검사 — **각 P1 의 반례를 먼저 재현**한다 (규율 ②)
# ──────────────────────────────────────────────────────────────────────────────

_FAILS = []


def chk(name, ok):
    print(('  ✓ ' if ok else '  ✗ ') + name)
    if not ok:
        _FAILS.append(name)


def neg(name, fn, want=BedRefusal):
    """음성대조 — **그 오류 종류로** 거부해야 통과.  아무 예외나 세지 않는다.

    (`PA12-09`: 어댑터의 ⑨ 가 `SystemExit` 이면 전부 성공으로 세어 **장식**이었다.)
    """
    try:
        fn()
    except want as e:
        print(f'  ✓ {name} — 거부: {str(e)[:72]}')
        return
    except Exception as e:                                    # noqa: BLE001
        chk(f'{name} (기대 {want.__name__}, 실제 {type(e).__name__}: {e})', False)
        return
    chk(f'{name} (거부하지 않았다)', False)


def _atom_file(tmp, rows, name='atom_100.liggghts', ts=100,
               lo=(0.0, 0.0, 0.0), hi=(10.0, 10.0, 20.0), bc='pp pp ff'):
    """rows = (id, x, y, z, radius, type)"""
    p = os.path.join(tmp, name)
    with open(p, 'w') as fh:
        fh.write(f'ITEM: TIMESTEP\n{ts}\nITEM: NUMBER OF ATOMS\n{len(rows)}\n')
        fh.write(f'ITEM: BOX BOUNDS {bc}\n')
        for k in range(3):
            fh.write(f'{lo[k]} {hi[k]}\n')
        fh.write('ITEM: ATOMS id x y z radius type\n')
        for r in rows:
            fh.write(' '.join(str(x) for x in r) + '\n')
    return p


def _contact_file(tmp, rows, name='contact_100.liggghts', ts=100, headers=None):
    """rows = (id1, id2, area)"""
    p = os.path.join(tmp, name)
    hd = headers or [COL_D1, COL_D2, COL_AREA]
    with open(p, 'w') as fh:
        fh.write(f'ITEM: TIMESTEP\n{ts}\nITEM: NUMBER OF ENTRIES\n{len(rows)}\n')
        fh.write('ITEM: ENTRIES ' + ' '.join(hd) + '\n')
        for r in rows:
            fh.write(' '.join(str(x) for x in r) + '\n')
    return p


def _stl(tmp, z=20.0, name='mesh.stl'):
    p = os.path.join(tmp, name)
    with open(p, 'w') as fh:
        fh.write('solid p\nfacet normal 0 0 1\nouter loop\n')
        for xy in ((0, 0), (1, 0), (0, 1)):
            fh.write(f'vertex {xy[0]} {xy[1]} {z}\n')
        fh.write('endloop\nendfacet\nendsolid p\n')
    return p


def selftest():
    import tempfile

    print('lhs_descriptor_harvest — 자기검사 (계약 6개 + P1 반례)')
    with tempfile.TemporaryDirectory() as tmp:

        # ── ① DESC-01 반례: τ 가 없어도 φ 는 나온다 ──────────────────────────
        #  SE 두 알이 서로 안 닿고 슬래브도 못 채운다 ⇒ τ = NOT_PERCOLATING.
        rows = [(1, 2.0, 2.0, 1.0, 0.5, 1), (2, 8.0, 8.0, 18.0, 0.5, 2)]
        a = _atom_file(tmp, rows)
        c = _contact_file(tmp, [])
        r = harvest(a, c, 2, 'desc01', mesh_path=_stl(tmp))
        chk('① DESC-01: τ 실패인데 phi_se 가 나온다',
            r['status']['tortuosity'] != STATUS_OK and r['phi_se'] is not None)
        chk('① DESC-01: phi_am 도 나온다', r['phi_am'] is not None)
        v = (4 / 3) * np.pi * 0.5 ** 3
        chk('① phi 값이 기하 그대로 (V_i/V_B)',
            abs(r['phi_se'] - v / 2000.0) < 1e-12 and abs(r['phi_am'] - v / 2000.0) < 1e-12)
        chk('① 공극률 closure 가 항등식', abs(r['closure_residual']) < 1e-12)

        # ── ② DESC-02 ①: 비관통에 유한 τ 를 주지 않는다 ────────────────────
        #  아래판에 닿는 SE 3알(고립) + 위쪽에 닿는 기둥 3알(아래판 미연결).
        rows = [(1, 1.0, 1.0, 0.5, 0.5, 2), (2, 3.0, 1.0, 0.5, 0.5, 2),
                (3, 5.0, 1.0, 0.5, 0.5, 2),
                (4, 9.0, 9.0, 18.5, 0.5, 2), (5, 9.0, 9.0, 19.4, 0.5, 2),
                (6, 9.0, 9.0, 19.9, 0.5, 2), (7, 5.0, 5.0, 10.0, 0.5, 1)]
        a2 = _atom_file(tmp, rows, name='atom_200.liggghts', ts=200)
        c2 = _contact_file(tmp, [], name='contact_200.liggghts', ts=200)
        r2 = harvest(a2, c2, 2, 'desc02a', mesh_path=_stl(tmp))
        chk('② DESC-02①: 비관통 → τ = None · NOT_PERCOLATING',
            r2['tortuosity_dijkstra_SE'] is None
            and r2['status']['tortuosity'] == STATUS_NOPERC)

        # ── ③ DESC-02 ②: 관통 성분이 있으면 예산이 무경로 쌍에 안 샌다 ──────
        #  관통 기둥 하나 + 무관한 고립 SE 덩어리 300알.
        col = [(i + 1, 5.0, 5.0, 0.5 + 0.9 * i, 0.5, 2) for i in range(22)]
        junk = [(1000 + i, 1.0 + 0.01 * i, 1.0, 10.0, 0.05, 2) for i in range(300)]
        a3 = _atom_file(tmp, col + junk, name='atom_300.liggghts', ts=300,
                        hi=(10.0, 10.0, 21.0))
        c3 = _contact_file(tmp, [], name='contact_300.liggghts', ts=300)
        r3 = harvest(a3, c3, 2, 'desc02b', mesh_path=_stl(tmp, z=21.0))
        chk('③ DESC-02②: 무경로 쌍이 예산을 안 먹는다 (τ 가 나온다)',
            r3['status']['tortuosity'] == STATUS_OK and r3['tortuosity_dijkstra_SE'] is not None)
        chk('③ 직선 기둥이면 τ ≈ 1', abs(r3['tortuosity_dijkstra_SE'] - 1.0) < 1e-6)
        chk('③ 표본이 전부 유효 (무경로 0건)',
            r3['tau_detail']['n_valid'] == r3['tau_detail']['n_sampled'])

        # ── ④ 계약①: 전체 피복률은 **실측 입자수 가중** ─────────────────────
        #  판정문 반례: P 1개 10 % · S 3개 90 % → 70 % (상평균평균 50 · 면적비 30).
        #  자유표면 4πr² = 4π, AM–SE 면적을 c% 가 되게 준다.
        fp = 4.0 * np.pi
        rows = [(1, 1.0, 1.0, 5.0, 1.0, 1), (2, 3.0, 1.0, 5.0, 1.0, 2),
                (3, 5.0, 1.0, 5.0, 1.0, 2), (4, 7.0, 1.0, 5.0, 1.0, 2),
                (90, 1.0, 5.0, 5.0, 1.0, 3), (91, 3.0, 5.0, 5.0, 1.0, 3),
                (92, 5.0, 5.0, 5.0, 1.0, 3), (93, 7.0, 5.0, 5.0, 1.0, 3)]
        con = [(1, 90, 0.10 * fp), (2, 91, 0.90 * fp),
               (3, 92, 0.90 * fp), (4, 93, 0.90 * fp)]
        a4 = _atom_file(tmp, rows, name='atom_400.liggghts', ts=400)
        c4 = _contact_file(tmp, con, name='contact_400.liggghts', ts=400)
        r4 = harvest(a4, c4, 3, 'cov', mesh_path=_stl(tmp))
        chk('④ P 평균 = 10 %', abs(r4['coverage_AM_P_hertz_pct'] - 10.0) < 1e-9)
        chk('④ S 평균 = 90 %', abs(r4['coverage_AM_S_hertz_pct'] - 90.0) < 1e-9)
        chk('④ 전체 = 70 % (상평균평균 50 이 아니다)',
            abs(r4['coverage_AM_total_hertz_pct'] - 70.0) < 1e-9)

        # ── ⑤ 계약④: Hertz 는 길이 scale 에 불변 ────────────────────────────
        k = 1000.0
        rows_s = [(r[0], r[1] * k, r[2] * k, r[3] * k, r[4] * k, r[5]) for r in rows]
        con_s = [(x[0], x[1], x[2] * k * k) for x in con]
        a5 = _atom_file(tmp, rows_s, name='atom_500.liggghts', ts=500,
                        hi=(10.0 * k, 10.0 * k, 20.0 * k))
        c5 = _contact_file(tmp, con_s, name='contact_500.liggghts', ts=500)
        r5 = harvest(a5, c5, 3, 'scale', plate_z=20.0 * k)
        chk('⑤ 계약④: scale ×1000 에도 Hertz 피복률 불변',
            abs(r5['coverage_AM_total_hertz_pct']
                - r4['coverage_AM_total_hertz_pct']) < 1e-9)
        chk('⑤ φ 도 불변 (무차원)', abs(r5['phi_se'] - r4['phi_se']) < 1e-12)

        # ── ⑥ DESC-05: 없는 상 = N/A, 존재하는데 무접촉 = 0 ─────────────────
        rows = [(1, 1.0, 1.0, 5.0, 1.0, 2), (90, 5.0, 5.0, 5.0, 1.0, 3)]
        a6 = _atom_file(tmp, rows, name='atom_600.liggghts', ts=600)
        c6 = _contact_file(tmp, [], name='contact_600.liggghts', ts=600)
        r6 = harvest(a6, c6, 3, 'absent', mesh_path=_stl(tmp))
        chk('⑥ DESC-05: 없는 AM_P → N/A (0 이 아니다)',
            r6['coverage_AM_P_hertz_pct'] is None
            and r6['status']['coverage_AM_P'] == STATUS_ABSENT)
        chk('⑥ DESC-05: 존재하는데 무접촉 AM_S → 0.0',
            r6['coverage_AM_S_hertz_pct'] == 0.0
            and r6['status']['coverage_AM_S'] == STATUS_OK)

        # ── ⑦ DESC-05: free surface ≤ 0 은 0 이 아니라 invalid ──────────────
        rows = [(1, 1.0, 1.0, 5.0, 1.0, 1), (2, 3.0, 1.0, 5.0, 1.0, 1),
                (90, 5.0, 5.0, 5.0, 1.0, 3)]
        con = [(1, 2, 99.0 * fp), (1, 90, 0.5 * fp)]
        a7 = _atom_file(tmp, rows, name='atom_700.liggghts', ts=700)
        c7 = _contact_file(tmp, con, name='contact_700.liggghts', ts=700)
        r7 = harvest(a7, c7, 3, 'freebad', mesh_path=_stl(tmp))
        chk('⑦ DESC-05: 분모붕괴가 0 으로 안 접힌다',
            r7['coverage_detail']['n_free_surface_invalid'] == 2)

        # ── ⑧ 음성대조: DESC-06 — 프레임이 섞이면 거부 ──────────────────────
        neg('⑧ DESC-06: atom_100 + contact_200 을 거부',
            lambda: harvest(a, c2, 2, 'mix', mesh_path=_stl(tmp)))

        # ── ⑨ 음성대조: 플래튼 높이 추정 금지 ───────────────────────────────
        neg('⑨ 계약⑤: mesh 도 --plate-z 도 없으면 거부',
            lambda: harvest(a, c, 2, 'noh'))
        neg('⑨ 계약⑤: 둘 다 주면 거부',
            lambda: harvest(a, c, 2, 'bothh', plate_z=20.0, mesh_path=_stl(tmp)))

        # ── ⑩ 음성대조: 선언 밖 type · 경계 플래그 ──────────────────────────
        bad = _atom_file(tmp, [(1, 1.0, 1.0, 5.0, 0.5, 9)],
                         name='atom_900.liggghts', ts=900)
        neg('⑩ 계약⑤: 선언 밖 type 을 거부',
            lambda: harvest(bad, _contact_file(tmp, [], name='contact_900.liggghts', ts=900),
                            2, 'badtype', mesh_path=_stl(tmp)))
        bbc = _atom_file(tmp, [(1, 1.0, 1.0, 5.0, 0.5, 1)],
                         name='atom_950.liggghts', ts=950, bc='pp pp pp')
        neg('⑩ 경계 플래그가 규약과 다르면 거부',
            lambda: harvest(bbc, _contact_file(tmp, [], name='contact_950.liggghts', ts=950),
                            2, 'badbc', mesh_path=_stl(tmp)))

        # ── ⑪ 음성대조: 접촉 면적 열이 없으면 거부 ──────────────────────────
        noarea = _contact_file(tmp, [(1, 2)], name='contact_960.liggghts', ts=960,
                               headers=[COL_D1, COL_D2])
        a11 = _atom_file(tmp, [(1, 1.0, 1.0, 5.0, 0.5, 1), (2, 2.0, 1.0, 5.0, 0.5, 2)],
                         name='atom_960.liggghts', ts=960)
        neg('⑪ 계약④: contact_area 열이 없으면 거부 (규약을 모른 채 안 낸다)',
            lambda: harvest(a11, noarea, 2, 'noarea', mesh_path=_stl(tmp)))

        # ── ⑫ 음성대조가 장식이 아닌지 (PA12-09 의 교훈) ────────────────────
        #  ⑧ 의 가드를 퇴행시키면 ⑧ 이 **반드시** 깨져야 한다.
        import lhs_descriptor_harvest as M
        keep = M.last_timestep
        M.last_timestep = lambda p: 0                     # 항상 같은 값 = 검사 무력화
        broke = False
        try:
            M.harvest(a, c2, 2, 'mut', mesh_path=_stl(tmp))
        except BedRefusal:
            broke = True
        except Exception:                                 # noqa: BLE001
            broke = True
        M.last_timestep = keep
        chk('⑫ PA12-09: TIMESTEP 가드를 퇴행시키면 ⑧ 이 실제로 뚫린다 (대조가 살아있다)',
            not broke)

        # ── ⑬a P1-HARV-01: τ 가 **평행이동에 불변**인가 ─────────────────────
        #  L4/L5 판정 반례: 쌍 찾기는 주기인데 길이를 raw 좌표차로 재면 같은 침대를
        #  옮기기만 해도 τ 가 9.850888284819803 → 1.0198039027185568 (9.6596배).
        def _chain(xs):
            n = len(xs)
            at = dict(x=np.array(xs, float), y=np.full(n, 5.0),
                      z=np.arange(1.0, n + 1.0), radius=np.full(n, 0.55),
                      type=np.full(n, 2, dtype=np.int64))
            return at, np.array(['SE'] * n, dtype=object)

        _lo, _hi = np.array([0., 0., 0.]), np.array([10., 10., 10.])
        _xs = [0.1, 9.9, 0.1, 9.9, 0.1]
        _t1 = tortuosity_se(*_chain(_xs), _lo, _hi)['tau_mean']
        _t2 = tortuosity_se(*_chain([(x + 5.0) % 10.0 for x in _xs]), _lo, _hi)['tau_mean']
        chk('⑬a P1-HARV-01: τ 가 xy 평행이동에 불변',
            _t1 is not None and _t2 is not None and abs(_t1 - _t2) < 1e-12)
        #  참값은 minimum-image 로 독립 계산한 것
        def _mi_ref(p, q):
            d = np.asarray(p, float) - np.asarray(q, float)
            d[0] -= 10.0 * round(d[0] / 10.0); d[1] -= 10.0 * round(d[1] / 10.0)
            return float(np.linalg.norm(d))
        _pts = np.column_stack([_xs, [5.] * 5, np.arange(1., 6.)])
        _ref = sum(_mi_ref(_pts[k], _pts[k + 1]) for k in range(4)) / 4.0
        chk('⑬a τ 가 minimum-image 해석값과 일치 (1.019803903)',
            _t1 is not None and abs(_t1 - _ref) < 1e-12 and abs(_ref - 1.019803903) < 1e-9)

        # ── ⑬b L1-04: 면적 채널 라벨이 매 행에 박히는가 ─────────────────────
        chk('⑬b L1-04: area_channel 이 출력에 있다',
            'dem_geometric_c_cpl22' in str(r4.get('area_channel', '')))
        chk('⑬b L1-04: 그 라벨이 Hertz 가 아님을 명시한다',
            'Hertz' in str(r4.get('area_channel', ''))
            and '2 - d/(2r)' in str(r4.get('area_channel', '')))
        #  기하 교차면적 ÷ Hertz = 2 − δ/(2r) 을 실제로 확인 (판정문 1.9875)
        _r, _d = 0.5, 0.05 * 0.25
        _ratio = (np.pi * (_r * _d - _d * _d / 4)) / (np.pi * (_r / 2) * _d)
        chk('⑬b L1-04: A_LIGG/A_Hertz = 2 − δ/(2r) = 1.9875',
            abs(_ratio - 1.9875) < 1e-9)

        # ── ⑭ LHS-08: 미관통의 **두 원인**을 산출물이 가르는가 ───────────────
        #  초판은 ⓐ 전극 밴드가 비어 **표본이 애초에 없는** 경우와 ⓑ 밴드는 찼는데
        #  성분이 안 이어진 경우를 **같은 `NOT_PERCOLATING`** 으로 접었다 (두 `return
        #  base` 가 같은 값을 낸다).  실물 130 중 **116** 이 그 값이었고 어느 쪽인지
        #  산출물만으로는 알 수 없었다 — φ_SE 로도 안 갈린다 (τ-OK 최소 φ_SE 0.1860
        #  보다 SE 가 많은데 실패한 케이스가 **53건**).
        def _bed(rows):
            """rows = (x, y, z, r, label) — 라벨을 직접 준다 (AM 이 z 범위를 정하는 경우)"""
            at = dict(x=np.array([q[0] for q in rows], float),
                      y=np.array([q[1] for q in rows], float),
                      z=np.array([q[2] for q in rows], float),
                      radius=np.array([q[3] for q in rows], float),
                      type=np.ones(len(rows), dtype=np.int64))
            return at, np.array([q[4] for q in rows], dtype=object)

        _lo8, _hi8 = np.array([0., 0., 0.]), np.array([10., 10., 20.])
        #  ⓐ 밴드가 빔 — SE 는 **하나로 이어져 있는데** 위 전극 밴드에 닿지 않는다.
        #    z_hi 를 **AM** 이 정한다 = 고체 z 범위 규약이라 SE 만 봐선 안 보이는 실패.
        _a_rows = [(5.0, 5.0, 0.5 + 0.9 * k, 0.5, 'SE') for k in range(11)]
        _a_rows += [(1.0, 1.0, 19.0, 0.5, 'AM_S')]
        _ta = tortuosity_se(*_bed(_a_rows), _lo8, _hi8)
        #  ⓑ 진짜 미관통 — 양 밴드에 SE 가 **있는데** 두 덩어리가 끊겼다.
        _b_rows = [(5.0, 5.0, 0.5 + 0.9 * k, 0.5, 'SE') for k in range(5)]
        _b_rows += [(5.0, 5.0, 15.5 + 0.9 * k, 0.5, 'SE') for k in range(5)]
        _tb = tortuosity_se(*_bed(_b_rows), _lo8, _hi8)
        _bda = _ta.get('band_detail') or {}
        _bdb = _tb.get('band_detail') or {}
        chk('⑭ LHS-08 ★재현: ⓐ(밴드 빔) 과 ⓑ(진짜 미관통) 의 status 가 **다르다**',
            _ta['status'] != _tb['status'])
        chk('⑭ LHS-08: ⓐ = ELECTRODE_BAND_EMPTY', _ta['status'] == STATUS_BAND_EMPTY)
        chk('⑭ LHS-08: ⓑ = NOT_PERCOLATING', _tb['status'] == STATUS_NOPERC)
        chk('⑭ LHS-08: 둘 다 유한 τ 를 내지 않는다 (판정은 그대로 보수적)',
            _ta['tau_mean'] is None and _tb['tau_mean'] is None)
        chk('⑭ LHS-08: 진단 블록 band_detail 이 붙는다', bool(_bda) and bool(_bdb))
        #  ⓐ 는 **한 덩어리인데도** 실패했다 = 규약(밴드 정의)이 용의자라는 신호
        chk('⑭ LHS-08 ⓐ: 위 밴드가 0 명 · 아래는 있다 · 성분은 하나',
            _bda.get('n_top', -1) == 0 and _bda.get('n_bot', -1) >= 1
            and _bda.get('n_components', -1) == 1)
        #  ⓑ 는 양쪽 밴드가 찼는데 성분이 둘 = 물리
        chk('⑭ LHS-08 ⓑ: 양 밴드가 차 있고 성분이 둘, 관통 성분 0',
            _bdb.get('n_bot', -1) >= 1 and _bdb.get('n_top', -1) >= 1
            and _bdb.get('n_components', -1) == 2
            and _bdb.get('n_span_components', -1) == 0)
        #  규약 판단(LHS-08 3단계)에 필요한 수치가 같은 수확에서 나온다 — 그러나
        #  **보고되는 τ 는 건드리지 않는다**.  이 두 줄이 그것을 강제한다.
        _tb2 = tortuosity_se(*_bed(_b_rows), _lo8, _hi8, plate_z=12.0)
        chk('⑭ LHS-08: plate_z 진단은 보고값·규약 문자열을 **안 바꾼다**',
            _tb2['status'] == _tb['status'] and _tb2['tau_mean'] == _tb['tau_mean']
            and _tb2['tau_convention'] == _tb['tau_convention'])
        chk('⑭ LHS-08: 규약 문자열이 solid_zrange 그대로다 (규약 판단은 재측정 뒤)',
            _tb['tau_convention']
            == 'harvest_v1/solid_zrange/rSEmax/no_fallback/same_component')
        chk('⑭ LHS-08: 그래도 plate_z 밴드 인원은 따로 적힌다 (규약 판단용)',
            (_tb2.get('band_detail') or {}).get('alt_n_top', -1)
            != (_tb2.get('band_detail') or {}).get('n_top', -1))
        #  ★ 날카로운 쪽 — ⓐ 는 규약을 바꾸면 **판정이 뒤집히는** 침대다 (BAND_EMPTY →
        #  OK, τ None → 유한).  여기서 plate_z 가 무해해야 "진단 전용"이 실재한다.
        #  (ⓑ 로만 검사하면 규약을 바꿔도 답이 안 변해 **통과해 버린다** = 약한 가드.)
        _ta2 = tortuosity_se(*_bed(_a_rows), _lo8, _hi8, plate_z=10.5)
        chk('⑭ LHS-08 ★가드: 판정이 뒤집히는 침대에서도 plate_z 가 τ 를 안 건드린다',
            _ta2['status'] == _ta['status'] and _ta2['tau_mean'] is None
            and (_ta2.get('band_detail') or {}).get('n_top', -1) == 0)
        chk('⑭ LHS-08: 그 침대의 alt_n_top 이 **규약을 바꾸면 몇 명인지**를 적는다',
            (_ta2.get('band_detail') or {}).get('alt_n_top', -1) >= 1
            and (_ta2.get('band_detail') or {}).get('alt_plate_above_solid') is False)
        #  양성 대조 — 진단을 붙였다고 성공 경로가 깨지면 안 된다
        _c_rows = [(5.0, 5.0, 0.5 + 0.9 * k, 0.5, 'SE') for k in range(22)]
        _tc = tortuosity_se(*_bed(_c_rows), _lo8, _hi8)
        chk('⑭ LHS-08: 관통 침대는 그대로 OK (진단이 성공을 안 깬다)',
            _tc['status'] == STATUS_OK
            and (_tc.get('band_detail') or {}).get('n_span_components', -1) == 1)

        # ── ⑬ 계약⑥: 291 코퍼스를 읽지 않는다 (정적) ────────────────────────
        src = open(os.path.abspath(__file__), encoding='utf-8').read()
        chk('⑬ 계약⑥: design_performance_corpus 를 읽는 코드가 없다',
            'design_performance_corpus' not in src.split('"""')[2])
        chk('⑬ full_metrics.json 을 읽는 코드가 없다',
            'full_metrics' not in src.split('"""')[2])
        chk('⑬ DESC-03: plastic_coverage 를 부르지 않는다',
            'plastic_coverage' not in src.split('"""')[2])

        # ── ⑭ LHS-10 (2026-09-24): 분모 바닥 = 벽 z = 0 (웹앱 `V_box = L²·plate_z`) — 덤프 상자 바닥이 아니다 ──
        rows14 = [(1, 2.0, 2.0, 1.0, 0.5, 1), (2, 5.0, 5.0, 2.0, 0.5, 2), (3, 8.0, 3.0, 3.0, 0.5, 3)]
        at14, lo14, hi14, _bc14 = read_atom_dump(
            _atom_file(tmp, rows14, name='atom_14.liggghts', lo=(0.0, 0.0, -1.0), hi=(10.0, 10.0, 20.0)))
        v14 = volumes_and_phi(at14, phase_labels(at14['type'], 3)[0], lo14, hi14, 5.0)
        chk('⑭ LHS-10: 상자 바닥이 −1 이어도 분모 높이 = plate_z − 벽 = 5', abs(v14['H_sim'] - 5.0) < 1e-12)
        _vs = 3 * (4.0 / 3.0) * np.pi * 0.5 ** 3
        chk('⑭ porosity = 1 − ΣV / (L²·plate_z) — 웹앱 calc_porosity 와 같은 식',
            abs(v14['porosity_sphere_pct_RECORD_ONLY'] - 100.0 * (1.0 - _vs / (10.0 * 10.0 * 5.0))) < 1e-9)
        at14b, lo14b, hi14b, _bc14b = read_atom_dump(_atom_file(
            tmp, [(1, 2.0, 2.0, -0.9, 0.5, 1)] + rows14[1:], name='atom_14b.liggghts',
            lo=(0.0, 0.0, -1.0), hi=(10.0, 10.0, 20.0)))
        neg('⑭ 입자가 벽 아래 (z − r = −1.4 < −½·r_max) 면 거부 — 벽 = 0 가정이 안 맞는 덱',
            lambda: volumes_and_phi(at14b, phase_labels(at14b['type'], 3)[0], lo14b, hi14b, 5.0))

    print()
    if _FAILS:
        print(f'✗ {len(_FAILS)} 건 실패')
        for f in _FAILS:
            print('   -', f)
        return 1
    print('✓ 전부 통과   ⚠ 이 통과는 **계약이 도구에 박혔다**는 뜻이지 '
          '실제 130 배치가 깨끗하다는 뜻이 아니다')
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        description='LHS 130 구조 디스크립터 수확 — 판정문 §7 계약 6개를 고정한다')
    ap.add_argument('--atom')
    ap.add_argument('--contact')
    ap.add_argument('--mesh', help='플래튼 STL (--plate-z 와 택일)')
    ap.add_argument('--plate-z', type=float, help='플래튼 높이 직접 지정 (--mesh 와 택일)')
    ap.add_argument('--n-types', type=int, choices=(2, 3),
                    help='필수 — 자동 추론은 거부한다 (AM_P 가 0개면 오사상된다)')
    ap.add_argument('--case', default='')
    ap.add_argument('--allow-any-bc', action='store_true')
    ap.add_argument('--n-pairs', type=int, default=N_TAU_PAIRS)
    ap.add_argument('--out', help='결과 JSON 경로')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()
    if not (a.atom and a.contact and a.n_types):
        ap.error('--atom · --contact · --n-types 는 필수다')
    try:
        r = harvest(a.atom, a.contact, a.n_types, a.case or os.path.basename(a.atom),
                    plate_z=a.plate_z, mesh_path=a.mesh,
                    allow_any_bc=a.allow_any_bc, n_pairs=a.n_pairs)
    except BedRefusal as e:
        print(f'거부 — {e}', file=sys.stderr)
        return 2
    txt = json.dumps(r, ensure_ascii=False, indent=1, default=str)
    if a.out:
        open(a.out, 'w', encoding='utf-8').write(txt + '\n')
        print(f'→ {a.out}')
    else:
        print(txt)
    return 0


if __name__ == '__main__':
    sys.exit(main())
