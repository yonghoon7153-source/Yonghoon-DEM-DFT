#!/usr/bin/env python3
"""
Coverage computed in BOTH "Hertzian" (LIGGGHTS `contact_area`) and Physics
(Tabor A = F_real/H with caps) modes for every AM particle.

★★ L1-04 — **이름 주의 (계산은 바뀌지 않았다)**.  여기서 `hertz`/`hertzian` 이라고 부르는
채널이 먹는 것은 LIGGGHTS 의 `contact_area` = `c_cpl[22]` = **기하학적 교차 원판**이고
**Hertz 탄성 해가 아니다** (`compute_pair_gran_local.cpp#L509-L517` 가 그렇게 구분한다).
두 값의 비는 해석적으로 `A_LIGG / A_Hertz = 2 − d/(2r)` 이고 r=0.5 µm · δ/R*=0.05 에서
**1.9875배**다 (이 리포에서 재현).
⇒ **무너지는 읽기 두 가지**: ⓐ 이 열을 `π R* δ` 로 환산해 인용하는 것 ⓑ `physics − hertz`
차이를 **추가 소성면적**으로만 읽는 것 (`plastic_coverage.py` 의 elastic 반환은 LIGG floor
를 쓰지 않아 *'Physics 는 항상 DEM-native 보다 크다'* 가 전 구간 계약이 아니다 — 비 0.50003536
인 구간이 있다).
⚠ 산출 **키 이름은 그대로 둔다** (`coverage_hertzian_pct`, `coverage_AM_*_hertz_pct` …) —
판정문이 *"기존 키와 frozen feature 를 세대 표시 없이 바꾸면 안 된다"* 고 했다.  개명은
세대 표시와 함께 별건으로 한다.  새 수확기 `lhs_descriptor_harvest.py` 는 매 행에
`area_channel` 을 박아 소비자에게 이 사실을 강제한다.

★★ physics **v2** — legacy 옆에 **나란히** (2026-09-29, 1저자 결정 *"권고대로"*) ★★
legacy `*_physics` 키 · 값 · 순서 · `coverage_per_am.csv` · 반환값은 **바이트 그대로**다 (코퍼스 physics σ ·
Stage E · σ_thermal T1 physics 타깃이 그 위에 서 있다 — `--selftest` ① 이 v2 이전 코드의 실측 핀으로 강제).
v2 는 `plastic_coverage.film_area_physics_v2` 로 접촉마다 다시 계산해 **새 키 (`*_physics_v2`)** 로만 쓴다:
  • cap = **전체 접촉면적**의 한계 — 전이 · 소성 가지에서 A = U = min(Tabor, 부피, 기하); L = max(πR*δ, A_LIGG) > U
    이면 **U** 를 내고 충돌로 센다 (`L1-01`).  항복 전 (δ/R* < DR_YIELD_ONSET) 은 πR*δ (legacy 와 같다).
  • 부피 = **정확한 전체 lens** (두 반경, `L1-02`) · 막 두께 5 nm 를 δ · r 과 **같은 덤프 단위**로 (`DESC-03`).
  • 분모 = 4πr² − Σ **v2** AM–AM 면적 (분자와 같은 장부 — legacy 는 native `c_cpl[22]` 를 뺀다).
  • 조용한 대체 없음 — 접촉 하나라도 v2 함수가 거부하면 그 침대의 v2 는 **빈칸** + `coverage_status_physics_v2` 에 사유.
    scale ≠ 1000 (µm = sim×scale 와 SI = sim/scale 가 1000 에서만 같다) · `delta` / `contact_area` 열 없음도 빈칸.
⚠⚠ 귀결 — **v2 면적은 LIGGGHTS 기하면적보다 (얕은 겹침에서는 πR*δ 보다도) 작을 수 있다**: 얕은 lens 는 5 nm 막보다
  얇아 V_lens/h ≈ πR*δ·(δ/h) 이다.  항복 개시에서 면적이 불연속으로 떨어진다 (r 0.5 µm SE–SE: ×0.0566).
  모든 상 쌍에 AM–SE E* · SE 경도를 쓰는 것 (`L1-03`) 은 v2 에서도 그대로다.
새 키 (한 침대): `coverage_<AM 상>_{mean,std}_physics_v2` · `coverage_AM_mean_physics_v2` (legacy 와 같은 입자 수 가중) ·
  `area_{AM전체_SE,SE_SE,AM전체_AM}_total_physics_v2` (µm²) · `n_contacts_physics_v2` · `n_cap_branch_physics_v2` ·
  `cap_conflict_n_physics_v2` · `cap_conflict_frac_physics_v2` (÷ 접촉) · `cap_conflict_frac_cap_branch_physics_v2`
  (÷ cap 가지) · `cap_conflict_n_by_pair_physics_v2` · `A_binding_counts_{total,AM_SE}_physics_v2` (**정수** 개수 —
  legacy 비율은 소수 첫째 자리 반올림이라 개수를 못 되살린다, `AREA-07`) · `am_denominator_physics_v2` ·
  `n_contacts_unknown_id_physics_v2` · `n_contact_failures_physics_v2` · `coverage_status_physics_v2` ·
  `rule_physics_v2` · `h_film_sim_physics_v2`.

★ 데이터 폴더 — `<case_id>` 로 부르면 **`WEBAPP_RESULTS_FOLDER` · `_ARCHIVE_FOLDER` · `_UPLOAD_FOLDER`** (와 webapp/.env) 를
따른다 (`run_network_full_corrections.py` 와 같은 규약).  옛 코드는 스크립트 옆 `webapp/` 만 봐서, 코드와 데이터가
갈린 배치 (`run_dem_webapp.sh` worktree · `lhs_webapp_batch.py`) 에서 이 단계가 "[skip]" 을 찍고 **rc 0 으로 아무것도
안 썼다** (`--selftest` ⑩).  환경변수가 없으면 경로는 예전과 같다.

Addresses two open questions:
  • H1: does plastic deformation change AM surface coverage?
        (dual-mode values per case → Δ% reported)
  • COMSOL input: per-AM A_AM_SE for electrochemically-active area
        (one CSV row per AM particle with both mode values)

Per case outputs:
  • full_metrics.json — adds coverage_AM_P_mean_physics,
                         coverage_AM_S_mean_physics,
                         coverage_AM_mean_physics (+ std)
  • coverage_per_am.csv — one row per AM particle:
        am_id, am_type, radius_um, surface_area_um2,
        A_AM_SE_hertzian_um2, A_AM_SE_physics_um2,
        coverage_hertzian_pct, coverage_physics_pct,
        delta_pct_physics_vs_hertzian

Usage:
  python3 scripts/coverage_physics_vs_hertzian.py <case_id>
  python3 scripts/coverage_physics_vs_hertzian.py --all
"""
from __future__ import annotations
import math
import os, sys, json, argparse
from pathlib import Path
from collections import defaultdict
import numpy as np
import pandas as pd

SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))
from plastic_coverage import film_area_from_overlap  # noqa: E402
from plastic_coverage import film_area_physics_v2, PHYSICS_V2_RULE, H_FILM_MIN  # noqa: E402
from dem_analysis_core import SHAPE_FACTOR  # noqa: E402

WEBAPP = Path(__file__).parent.parent / 'webapp'

# Mirror app.py / run_network_full_corrections.py: load webapp/.env, then honor WEBAPP_*_FOLDER so a
# `<case_id>` call finds the SAME data the webapp serves (worktree runner · LHS batch whose data live
# outside the code tree).  Without this the stage printed "[skip]" and exited 0 having written nothing.
_envf = WEBAPP / '.env'
if _envf.exists():
    for _l in _envf.read_text().splitlines():
        _l = _l.strip()
        if _l and not _l.startswith('#') and '=' in _l:
            _k, _v = _l.split('=', 1)
            os.environ.setdefault(_k.strip(), _v.strip())


def _webapp_dirs() -> tuple:
    """(results, archive, uploads) — 부를 때마다 환경변수를 읽는다 (없으면 스크립트 옆 webapp/ — 예전 경로)."""
    return (Path(os.environ.get('WEBAPP_RESULTS_FOLDER') or (WEBAPP / 'results')),
            Path(os.environ.get('WEBAPP_ARCHIVE_FOLDER') or (WEBAPP / 'archive')),
            Path(os.environ.get('WEBAPP_UPLOAD_FOLDER') or (WEBAPP / 'uploads')))


def find_case_dir(cid: str) -> Path | None:
    results, archive, _uploads = _webapp_dirs()
    for base in (results, archive):
        p = base / cid
        if p.exists() and (p / 'atoms.csv').exists() and (p / 'contacts.csv').exists():
            return p
    return None


def load_meta(cid: str) -> dict:
    results, _archive, uploads = _webapp_dirs()
    for base in (uploads, results):
        m = base / cid / 'meta.json'
        if m.exists():
            try:
                return json.load(open(m))
            except Exception:
                pass
    return {}


def parse_type_map(s: str) -> dict:
    tm = {}
    for pair in (s or '').split(','):
        if ':' in pair:
            k, v = pair.split(':', 1)
            try:
                tm[int(k.strip())] = v.strip()
            except ValueError:
                pass
    return tm


def _recompute_path_metrics_physics(case_dir: Path,
                                     pair_h: dict, pair_p: dict,
                                     scale: float,
                                     verbose: bool = False) -> dict:
    """Re-evaluate path_hop_area_mean / min_mean / path_conductance in Physics mode.

    Path topology (the sequence of SE ids along each shortest path) is fixed.
    Only the per-hop contact area differs. We read se_clusters.json for the
    existing paths and swap A_ligg → A_phys at each hop.
    """
    sc_path = case_dir / 'se_clusters.json'
    if not sc_path.exists():
        if verbose:
            print(f'  [path phys] skip: {sc_path} missing')
        return {}
    try:
        sc = json.load(open(sc_path))
    except Exception as e:
        if verbose:
            print(f'  [path phys] skip: {e}')
        return {}

    area_conv = (scale * scale) * 1.0  # sim m² → μm² (consistent with caller)
    # Note: analyze_contacts uses area_conv = 1/scale² * 1e12, which for
    # scale=1000 gives 1e6. Our scale² is also 1e6 — they match.

    hop_areas_p_all: list[float] = []
    hop_mins_p_all: list[float] = []
    conductances_p: list[float] = []

    for cl in sc.get('clusters', []):
        for p in cl.get('paths', []) or []:
            ids = p.get('ids') or []
            if len(ids) < 2:
                continue
            hop_p = []
            sum_inv_p = 0.0
            for k in range(len(ids) - 1):
                key = (min(ids[k], ids[k+1]), max(ids[k], ids[k+1]))
                A_p_sim = pair_p.get(key)
                if A_p_sim is None:
                    # SE-SE pair not seen (e.g. AM-SE hop in mixed paths) — skip
                    continue
                A_p_um2 = A_p_sim * area_conv
                hop_p.append(A_p_um2)
                if A_p_um2 > 0:
                    sum_inv_p += 1.0 / A_p_um2
            if not hop_p:
                continue
            hop_areas_p_all.append(float(np.mean(hop_p)))
            hop_mins_p_all.append(float(min(hop_p)))
            if sum_inv_p > 0:
                conductances_p.append(1.0 / sum_inv_p)

    out = {}
    if hop_areas_p_all:
        out['path_hop_area_mean_physics']     = round(float(np.mean(hop_areas_p_all)), 4)
    if hop_mins_p_all:
        out['path_hop_area_min_mean_physics'] = round(float(np.mean(hop_mins_p_all)), 4)
    if conductances_p:
        out['path_conductance_mean_physics']  = round(float(np.mean(conductances_p)), 6)
    if verbose and out:
        print(f'  [path phys] hop_mean={out.get("path_hop_area_mean_physics")}  '
              f'bottleneck={out.get("path_hop_area_min_mean_physics")}  '
              f'g_path={out.get("path_conductance_mean_physics")}')
    return out


def _all_finite(obj) -> bool:
    """중첩 dict/list 안의 실수가 전부 유한한가 (None · 문자열 · 정수는 통과)."""
    if isinstance(obj, dict):
        return all(_all_finite(v) for v in obj.values())
    if isinstance(obj, (list, tuple)):
        return all(_all_finite(v) for v in obj)
    if isinstance(obj, float):
        return math.isfinite(obj)
    return True


class _PhysicsV2Book:
    """physics **v2** 장부 — legacy 누적과 **따로** 센다 (legacy 합의 덧셈 순서 · 값을 건드리지 않는다).

    접촉마다 `film_area_physics_v2` 를 부른다.  거부 (예외) 는 **조용히 넘기지 않고** 세며 첫 사례를 사유로 남긴다 —
    하나라도 있으면 그 침대의 v2 는 빈칸이다 (legacy 는 같은 자리에서 native 면적으로 조용히 대체한다).
    침대 수준 전제 (scale == 1000 · `delta` / `contact_area` 열) 가 깨지면 접촉을 계산하지 않고 빈칸 사유만 남긴다.
    """
    PAIRS = ('AM_SE', 'SE_SE', 'AM_AM', 'other')
    BINDINGS = ('elastic', 'tabor', 'volume', 'geom', 'none')

    def __init__(self, scale, contact_columns):
        self.reasons = []
        try:
            s = float(scale)
        except (TypeError, ValueError):
            s = float('nan')
        self.length_scale = s if (math.isfinite(s) and s == 1000.0) else None
        if self.length_scale is None:
            self.reasons.append(
                f'scale={scale!r} ≠ 1000 — 이 코드의 두 길이 규약 (µm = sim×scale · SI = sim/scale) 이 1000 에서만 '
                f'같아 5 nm 막을 덤프 단위로 옮길 수 없다')
        cols = set(contact_columns)
        for col in ('delta', 'contact_area'):
            if col not in cols:
                self.reasons.append(f'contacts.csv 에 {col} 열이 없다')
        self.on = not self.reasons
        self.am_se = defaultdict(float)          # AM id → Σ A_v2 (AM–SE)   (sim 단위²)
        self.am_am = defaultdict(float)          # AM id → Σ A_v2 (AM–AM)   (분모 — 분자와 같은 장부)
        self.tot = {'AM_SE': 0.0, 'SE_SE': 0.0, 'AM_AM': 0.0}
        self.n = self.n_cap = self.n_conf = 0
        self.conf_pair = {p: 0 for p in self.PAIRS}
        self.bind_total = {b: 0 for b in self.BINDINGS}
        self.bind_am_se = {b: 0 for b in self.BINDINGS}
        self.n_fail = 0
        self.first_fail = None
        self.n_unknown_id = 0

    @staticmethod
    def _cell(v, name):
        """접촉 칸 → float.  빈 칸은 0 으로 읽지 않는다 (legacy 의 `or 0` 과 다르다) — 예외로."""
        if v is None or (isinstance(v, str) and not v.strip()):
            raise ValueError(f'{name} 칸이 비었다')
        return float(v)

    def add(self, c, i1, i2, r1, r2, pair, am_id):
        if not self.on:
            return
        try:
            A, comp = film_area_physics_v2(self._cell(c.get('delta'), 'delta'), r1, r2,
                                           ligg_area=self._cell(c.get('contact_area'), 'contact_area'),
                                           length_scale=self.length_scale)
        except Exception as e:                   # noqa: BLE001 — 조용히 넘기지 않는다: 세고, 침대 v2 를 빈칸으로
            self.n_fail += 1
            if self.first_fail is None:
                self.first_fail = f'{i1}–{i2}: {type(e).__name__}: {e}'
            return
        self.n += 1
        b = comp['binding']
        self.bind_total[b] += 1
        if comp['cap_conflict'] is not None:
            self.n_cap += 1
            if comp['cap_conflict']:
                self.n_conf += 1
                self.conf_pair[pair] += 1
        if pair == 'AM_SE':
            self.bind_am_se[b] += 1
            self.tot['AM_SE'] += A
            self.am_se[am_id] += A
        elif pair == 'SE_SE':
            self.tot['SE_SE'] += A
        elif pair == 'AM_AM':
            self.tot['AM_AM'] += A
            self.am_am[i1] += A
            self.am_am[i2] += A

    def coverage(self, id_to_r, id_to_t, am_types, type_map, am_surf):
        """AM 입자별 v2 피복률 — legacy physics 와 같은 식 · 같은 클립 · 같은 순서, 분모만 **v2** AM–AM."""
        by_lbl = defaultdict(list)
        n_am = n_free0 = n_clip = 0
        for aid, _r in id_to_r.items():
            t = id_to_t.get(aid)
            if t not in am_types:
                continue
            lbl = type_map.get(t, f'T{t}')
            surf = am_surf.get(aid, 0.0)
            free = max(surf - self.am_am.get(aid, 0.0), 0.0)
            A = self.am_se.get(aid, 0.0)
            n_am += 1
            if free > 0:
                raw = A / free * 100
                n_clip += int(raw > 100.0)
                cov = min(raw, 100.0)
            else:
                n_free0 += 1
                cov = 0.0
            by_lbl[lbl].append(cov)
        return by_lbl, {'n_am': n_am, 'n_free_surface_nonpositive': n_free0, 'n_coverage_clipped_100': n_clip}

    def keys(self, by_lbl, am_diag, area_conv) -> dict:
        """full_metrics 에 실을 v2 키 — 전부 `*_physics_v2`.  빈칸 침대는 값 키가 None 이고 사유가 status 에 있다."""
        reasons = list(self.reasons)
        if self.n_fail:
            reasons.append(f'{self.n_fail} 접촉을 film_area_physics_v2 가 거부했다 — 첫 사례 {self.first_fail}')
        out = {}
        for lbl, arr in by_lbl.items():
            out[f'coverage_{lbl}_mean_physics_v2'] = round(float(np.mean(arr)), 3)
            out[f'coverage_{lbl}_std_physics_v2'] = round(float(np.std(arr)), 3)
        all_v = [v for arr in by_lbl.values() for v in arr]
        if all_v:                                # legacy 와 같은 가중: AM 입자 수 가중 평균
            out['coverage_AM_mean_physics_v2'] = round(float(np.mean(all_v)), 3)
        out['area_AM전체_SE_total_physics_v2'] = round(self.tot['AM_SE'] * area_conv, 2)
        out['area_SE_SE_total_physics_v2'] = round(self.tot['SE_SE'] * area_conv, 2)
        out['area_AM전체_AM_total_physics_v2'] = round(self.tot['AM_AM'] * area_conv, 2)
        out['n_contacts_physics_v2'] = self.n
        out['n_cap_branch_physics_v2'] = self.n_cap
        out['cap_conflict_n_physics_v2'] = self.n_conf
        out['cap_conflict_frac_physics_v2'] = round(self.n_conf / self.n, 6) if self.n else None
        out['cap_conflict_frac_cap_branch_physics_v2'] = (round(self.n_conf / self.n_cap, 6)
                                                          if self.n_cap else None)
        out['cap_conflict_n_by_pair_physics_v2'] = dict(self.conf_pair)
        out['A_binding_counts_total_physics_v2'] = dict(self.bind_total)
        out['A_binding_counts_AM_SE_physics_v2'] = dict(self.bind_am_se)
        out['am_denominator_physics_v2'] = dict(am_diag)
        if not reasons and not _all_finite(out):
            reasons.append('비유한 v2 산출 (내부 검사)')
        if reasons:                              # 빈칸 — 부분 합은 싣지 않는다
            out = {k: None for k in out}
        out['n_contacts_unknown_id_physics_v2'] = self.n_unknown_id
        out['n_contact_failures_physics_v2'] = self.n_fail
        out['coverage_status_physics_v2'] = 'ok' if not reasons else 'blank: ' + ' · '.join(reasons)
        out['rule_physics_v2'] = PHYSICS_V2_RULE
        out['h_film_sim_physics_v2'] = (H_FILM_MIN * self.length_scale) if self.length_scale else None
        return out


def compute_case(cid: str, case_dir: Path, type_map: dict, scale: float = 1000.0,
                 write_csv: bool = True, update_metrics: bool = True,
                 verbose: bool = False) -> dict:
    """Compute per-AM coverage in Hertzian and Physics modes, return summary dict.

    ★ physics v2 (2026-09-29) 는 **같은 접촉 순회에서 따로** 센다 (`_PhysicsV2Book`) — legacy 키 · 값 · CSV · 반환값은
    그대로이고 v2 는 `*_physics_v2` 키로만 full_metrics.json 에 실린다 (모듈 docstring).
    """
    atoms_df = pd.read_csv(case_dir / 'atoms.csv')
    contacts_df = pd.read_csv(case_dir / 'contacts.csv', low_memory=False)
    v2 = _PhysicsV2Book(scale, contacts_df.columns)

    # Index radii and types by id
    id_to_r = dict(zip(atoms_df['id'].astype(int), atoms_df['radius'].astype(float)))
    id_to_t = dict(zip(atoms_df['id'].astype(int), atoms_df['type'].astype(int)))

    am_types = [k for k, v in type_map.items() if 'AM' in v]
    se_types = [k for k, v in type_map.items() if v == 'SE']

    # Per-AM surface area (sim units, m²)
    am_surf = {}
    for aid, r in id_to_r.items():
        if id_to_t.get(aid) in am_types:
            am_surf[aid] = 4.0 * np.pi * r * r

    # Scan ALL contacts: compute both A_hertzian and A_physics per AM particle
    # AND global sums (AM-SE total, SE-SE total, AM-AM total).
    #  ⚠ L1-04 — 이름은 `hertz` 지만 담기는 것은 LIGGGHTS `contact_area`
    #    = **기하 교차 원판** (Hertz 탄성 아님, 비 = 2 − d/(2r)).
    am_se_hertz = defaultdict(float)   # per-AM AM-SE DEM-native area (sim m²)
    am_se_phys  = defaultdict(float)   # per-AM AM-SE Physics area (sim m²)
    am_am_hertz = defaultdict(float)   # per-AM AM-AM area (for free-surface deduction)

    # SE-SE pair → (A_hertz_sim, A_phys_sim) for path hop recomputation (Physics mode)
    se_pair_area_h: dict = {}
    se_pair_area_p: dict = {}

    # Per-AM-type buckets for totals (used by UI rows "AM-SE Total" etc.)
    total_am_se_h = 0.0
    total_am_se_p = 0.0
    total_se_se_h = 0.0
    total_se_se_p = 0.0
    total_am_am_h = 0.0
    total_am_am_p = 0.0

    # 5-case decomposition for AM-SE contacts only (sim units, converted later).
    # Lower bounds and upper caps from film_area_from_overlap return_components.
    am_se_5case = {
        'A_hertzian': 0.0,   # π R*δ          (lower bound 1)
        'A_ligg':     0.0,   # LIGGGHTS DEM   (lower bound 2)
        'A_tabor':    0.0,   # F/H            (upper cap 1)
        'A_volume':   0.0,   # V/h_min        (upper cap 2, capped at A_geom for safety)
        'A_geom':     0.0,   # 2π R_min²      (upper cap 3)
        'A_final':    0.0,   # max(lower, min(caps)) — same as total_am_se_p
    }
    # Binding (= which of the 5 cases was selected per contact).
    # Tracked twice: AM-SE only vs all contact pairs (total).
    _binding_template = lambda: {
        'hertzian': 0, 'liggghts': 0,
        'tabor': 0, 'volume': 0, 'geom': 0,
        'elastic': 0, 'other': 0,
    }
    am_se_binding_counts = _binding_template()
    total_binding_counts = _binding_template()
    am_se_n_contacts = 0
    total_n_contacts  = 0

    for _, c in contacts_df.iterrows():
        i1, i2 = int(c['id1']), int(c['id2'])
        if i1 not in id_to_t or i2 not in id_to_t:
            v2.n_unknown_id += 1                 # legacy 와 같은 모집단 (둘 다 건너뛴다) — v2 는 세어 둔다
            continue
        t1, t2 = id_to_t[i1], id_to_t[i2]
        r1 = id_to_r[i1]; r2 = id_to_r[i2]
        delta_sim = float(c.get('delta', 0) or 0)
        A_ligg_sim = float(c.get('contact_area', 0) or 0)
        R_star = (r1 * r2) / (r1 + r2) if (r1 + r2) > 0 else 0
        R_min = min(r1, r2)
        A_phys_sim = A_ligg_sim
        comp = None  # 5-case components (sim units) when available
        if delta_sim > 0 and R_star > 0 and R_min > 0:
            try:
                A_p, _regime, comp = film_area_from_overlap(
                    delta_sim, R_star, R_min=R_min,
                    ligg_area=A_ligg_sim, mode='physics',
                    return_components=True)
                A_phys_sim = A_p
            except Exception:
                pass

        # Bucket by contact-type pair
        am1 = t1 in am_types;  am2 = t2 in am_types
        se1 = t1 in se_types;  se2 = t2 in se_types

        # Track binding selection across ALL contacts (total) — independent
        # of contact-type bucket so SE-SE / AM-AM also count.
        if comp is not None:
            total_n_contacts += 1
            bk_t = comp.get('binding') or 'other'
            if bk_t in total_binding_counts:
                total_binding_counts[bk_t] += 1
            else:
                total_binding_counts['other'] += 1

        if (am1 and se2) or (am2 and se1):
            total_am_se_h += A_ligg_sim
            total_am_se_p += A_phys_sim
            if comp is not None:
                am_se_n_contacts += 1
                bk = comp.get('binding') or 'other'
                if bk in am_se_binding_counts:
                    am_se_binding_counts[bk] += 1
                else:
                    am_se_binding_counts['other'] += 1
            if am1:
                am_se_hertz[i1] += A_ligg_sim
                am_se_phys[i1]  += A_phys_sim
            else:
                am_se_hertz[i2] += A_ligg_sim
                am_se_phys[i2]  += A_phys_sim
        elif se1 and se2:
            total_se_se_h += A_ligg_sim
            total_se_se_p += A_phys_sim
            key = (min(i1, i2), max(i1, i2))
            se_pair_area_h[key] = A_ligg_sim
            se_pair_area_p[key] = A_phys_sim
        elif am1 and am2:
            total_am_am_h += A_ligg_sim
            total_am_am_p += A_phys_sim
            am_am_hertz[i1] += A_ligg_sim
            am_am_hertz[i2] += A_ligg_sim

        # ── physics v2 — legacy 값은 위에서 이미 끝났다; v2 는 **따로** 센다 (같은 접촉 · 같은 상 쌍 분류) ──
        v2.add(c, i1, i2, r1, r2,
               ('AM_SE' if ((am1 and se2) or (am2 and se1)) else
                'SE_SE' if (se1 and se2) else 'AM_AM' if (am1 and am2) else 'other'),
               i1 if am1 else i2)

    # Per-AM coverage (% of non-AM-occluded surface) + per-AM CSV
    # Convert to μm²: multiply by scale² (if sim units are m and scale=1000)
    area_conv = scale * scale  # sim m² → μm²
    rows = []
    # Three coverage versions per AM type:
    #   hertz : Hertzian numerator + 4πr² surface
    #   phys  : Physics numerator + 4πr² surface (raw, no roughness)
    #   rough : Physics numerator + factor × 4πr² surface (B3 shape factor)
    covs_by_type = defaultdict(lambda: {'hertz': [], 'phys': [], 'rough': []})
    for aid, r_sim in id_to_r.items():
        t = id_to_t.get(aid)
        if t not in am_types:
            continue
        lbl = type_map.get(t, f'T{t}')
        surf = am_surf.get(aid, 0.0)
        sf = SHAPE_FACTOR.get(lbl, 1.0)
        surf_rough = sf * surf
        am_am = am_am_hertz.get(aid, 0.0)
        free = max(surf - am_am, 0.0)
        free_rough = max(surf_rough - am_am, 0.0)
        A_h = am_se_hertz.get(aid, 0.0)
        A_p = am_se_phys.get(aid, 0.0)
        cov_h     = min(A_h / free       * 100, 100.0) if free       > 0 else 0.0
        cov_p     = min(A_p / free       * 100, 100.0) if free       > 0 else 0.0
        cov_rough = min(A_p / free_rough * 100, 100.0) if free_rough > 0 else 0.0
        covs_by_type[lbl]['hertz'].append(cov_h)
        covs_by_type[lbl]['phys'].append(cov_p)
        covs_by_type[lbl]['rough'].append(cov_rough)
        rows.append({
            'am_id': aid,
            'am_type': lbl,
            'shape_factor': sf,
            'radius_um': round(r_sim * scale, 3),
            'surface_area_um2':         round(surf * area_conv, 3),
            'surface_area_rough_um2':   round(surf_rough * area_conv, 3),
            'A_AM_SE_hertzian_um2':     round(A_h * area_conv, 4),
            'A_AM_SE_physics_um2':      round(A_p * area_conv, 4),
            'coverage_hertzian_pct':    round(cov_h, 3),
            'coverage_physics_pct':     round(cov_p, 3),
            'coverage_physics_rough_pct': round(cov_rough, 3),
            'delta_pct_physics_vs_hertzian': round(
                ((cov_p - cov_h) / cov_h * 100) if cov_h > 0 else 0, 2),
            'delta_pct_rough_vs_physics': round(
                ((cov_rough - cov_p) / cov_p * 100) if cov_p > 0 else 0, 2),
        })

    # Summary
    summary = {}
    for lbl, arrs in covs_by_type.items():
        if not arrs['hertz']:
            continue
        h = np.array(arrs['hertz'])
        p = np.array(arrs['phys'])
        rg = np.array(arrs['rough'])
        summary[lbl] = {
            'n':              int(len(h)),
            'hertzian_mean':  float(np.mean(h)),
            'hertzian_std':   float(np.std(h)),
            'physics_mean':   float(np.mean(p)),
            'physics_std':    float(np.std(p)),
            'rough_mean':     float(np.mean(rg)),
            'rough_std':      float(np.std(rg)),
            'delta_mean_pct': float((np.mean(p) - np.mean(h)) / np.mean(h) * 100)
                                if np.mean(h) > 0 else 0.0,
            'delta_rough_pct': float((np.mean(rg) - np.mean(p)) / np.mean(p) * 100)
                                if np.mean(p) > 0 else 0.0,
        }

    # Write per-AM CSV
    if write_csv and rows:
        df_out = pd.DataFrame(rows)
        csv_path = case_dir / 'coverage_per_am.csv'
        df_out.to_csv(csv_path, index=False)
        if verbose:
            print(f'  → {csv_path}  ({len(df_out)} AM particles)')

    # Recompute percolation-path metrics (Physics mode) using se_clusters.json
    # Paths (graph edges) are topology-only — they do NOT change between modes;
    # only the area at each hop differs. So we reuse the existing path lists
    # and swap in A_physics per hop.
    path_phys = _recompute_path_metrics_physics(
        case_dir, se_pair_area_h, se_pair_area_p, scale, verbose=verbose)

    # physics v2 키 — legacy 쓰기와 **따로** 만든다 (v2 의 내부 결함이 legacy 쓰기를 막지 않게, 그리고 조용히 넘기지 않게)
    try:
        _v2_by_lbl, _v2_am = v2.coverage(id_to_r, id_to_t, am_types, type_map, am_surf)
        v2_keys = v2.keys(_v2_by_lbl, _v2_am, area_conv)
    except Exception as e:                       # noqa: BLE001 — 사유를 status 에 남긴다
        v2_keys = {'coverage_status_physics_v2': f'blank: v2 집계 내부 오류 — {type(e).__name__}: {e}',
                   'n_contact_failures_physics_v2': v2.n_fail, 'rule_physics_v2': PHYSICS_V2_RULE}

    # Update full_metrics.json
    if update_metrics:
        fm_path = case_dir / 'full_metrics.json'
        if fm_path.exists():
            try:
                m = json.load(open(fm_path))
                for lbl, s in summary.items():
                    base = f'coverage_{lbl}'
                    m[f'{base}_mean_physics']    = round(s['physics_mean'], 3)
                    m[f'{base}_std_physics']     = round(s['physics_std'], 3)
                    m[f'{base}_delta_pct_physics'] = round(s['delta_mean_pct'], 2)
                    # ── B3 shape-factor (roughness) version ──
                    m[f'{base}_mean_physics_rough'] = round(s['rough_mean'], 3)
                    m[f'{base}_std_physics_rough']  = round(s['rough_std'], 3)
                    m[f'{base}_delta_pct_rough']    = round(s['delta_rough_pct'], 2)
                # Aggregate total-AM coverage ("coverage_AM_mean_physics")
                all_h = [v for arrs in covs_by_type.values() for v in arrs['hertz']]
                all_p = [v for arrs in covs_by_type.values() for v in arrs['phys']]
                all_r = [v for arrs in covs_by_type.values() for v in arrs['rough']]
                if all_h:
                    m['coverage_AM_mean_physics'] = round(float(np.mean(all_p)), 3)
                    m['coverage_AM_delta_pct_physics'] = round(
                        float((np.mean(all_p) - np.mean(all_h)) /
                              max(np.mean(all_h), 1e-9) * 100), 2)
                    m['coverage_AM_mean_physics_rough'] = round(float(np.mean(all_r)), 3)
                    m['coverage_AM_delta_pct_rough'] = round(
                        float((np.mean(all_r) - np.mean(all_p)) /
                              max(np.mean(all_p), 1e-9) * 100), 2)
                # Global area totals (Physics mode) — feeds UI rows
                #   "AM-SE Total(μm²)" and "SE-SE Total(μm²)".
                # Keys match the existing Hertzian keys + _physics suffix.
                m['area_AM전체_SE_total_physics'] = round(total_am_se_p * area_conv, 2)
                m['area_SE_SE_total_physics']    = round(total_se_se_p * area_conv, 2)
                m['area_AM전체_AM_total_physics'] = round(total_am_am_p * area_conv, 2)

                # ── Per-contact binding distribution ──
                # For each contact, exactly one of the five candidate areas
                # is selected by max(lower_bounds, min(upper_caps)). We tally
                # which case won across the population of contacts and
                # report it as a percentage. Reported twice:
                #   - AM-SE only (the contacts that drive the analysis-summary
                #     interface metrics)
                #   - Total (all SE-SE + AM-SE + AM-AM contact pairs)
                if am_se_n_contacts > 0:
                    m['A_binding_share_AM_SE_pct'] = {
                        k: round(100.0 * v / am_se_n_contacts, 1)
                        for k, v in am_se_binding_counts.items()
                    }
                    m['A_binding_AM_SE_n_contacts'] = am_se_n_contacts
                if total_n_contacts > 0:
                    m['A_binding_share_total_pct'] = {
                        k: round(100.0 * v / total_n_contacts, 1)
                        for k, v in total_binding_counts.items()
                    }
                    m['A_binding_total_n_contacts'] = total_n_contacts
                # Δ% (reference): only meaningful if Hertzian total > 0
                if total_am_se_h > 0:
                    m['area_AM전체_SE_total_delta_pct_physics'] = round(
                        (total_am_se_p - total_am_se_h) / total_am_se_h * 100, 2)
                if total_se_se_h > 0:
                    m['area_SE_SE_total_delta_pct_physics'] = round(
                        (total_se_se_p - total_se_se_h) / total_se_se_h * 100, 2)
                # Percolation-path metrics (Physics mode)
                if path_phys:
                    for k, v in path_phys.items():
                        m[k] = v
                # ── physics v2 — legacy 키 옆에 새 키로.  옛 v2 세대는 통째로 걷는다 (이 스크립트가 소유한다) ──
                for _k in [k for k in m if k.endswith('_physics_v2')]:
                    del m[_k]
                m.update(v2_keys)
                with open(fm_path, 'w') as f:
                    json.dump(m, f, indent=2, default=str)
                if verbose:
                    print(f'  → {fm_path}  (updated physics keys)')
                    print(f'    physics_v2: {m.get("coverage_status_physics_v2")} · '
                          f'AM-SE total {m.get("area_AM전체_SE_total_physics_v2")} µm² · '
                          f'cap_conflict {m.get("cap_conflict_n_physics_v2")}/{m.get("n_cap_branch_physics_v2")} '
                          f'(cap 가지) · 거부 {m.get("n_contact_failures_physics_v2")}')
                    print(f'    AM-SE total: H={total_am_se_h*area_conv:,.1f}  '
                          f'P={total_am_se_p*area_conv:,.1f}  '
                          f'Δ={(total_am_se_p/total_am_se_h-1)*100 if total_am_se_h else 0:+.1f}%')
                    print(f'    SE-SE total: H={total_se_se_h*area_conv:,.1f}  '
                          f'P={total_se_se_p*area_conv:,.1f}  '
                          f'Δ={(total_se_se_p/total_se_se_h-1)*100 if total_se_se_h else 0:+.1f}%')
            except Exception as e:
                print(f'  [warn] failed to update full_metrics.json: {e}')

    return summary


def process_one(cid: str, *, verbose: bool = False) -> dict | None:
    case_dir = find_case_dir(cid)
    if case_dir is None:
        print(f'  [skip] {cid}: no atoms.csv/contacts.csv')
        return None
    meta = load_meta(cid)
    type_map = parse_type_map(meta.get('type_map', ''))
    scale = meta.get('scale', 1000)
    if not type_map:
        print(f'  [skip] {cid}: no type_map in meta.json')
        return None
    name = meta.get('name', cid)
    if verbose:
        print(f'\n=== {name}  ({cid}) ===')
    return compute_case(cid, case_dir, type_map, scale=scale, verbose=verbose)


def process_dir(case_dir: Path, *, verbose: bool = False) -> dict | None:
    """Alt entry point: operate directly on a case directory (archive reanalyze).

    Reads meta.json from the case directory itself (no results/<cid> lookup).
    """
    if not (case_dir / 'atoms.csv').exists() or not (case_dir / 'contacts.csv').exists():
        print(f'  [skip] {case_dir}: no atoms.csv/contacts.csv')
        return None
    meta_path = case_dir / 'meta.json'
    if not meta_path.exists():
        print(f'  [skip] {case_dir}: no meta.json')
        return None
    try:
        meta = json.load(open(meta_path))
    except Exception as e:
        print(f'  [skip] {case_dir}: meta.json unreadable ({e})')
        return None
    type_map = parse_type_map(meta.get('type_map', ''))
    scale = meta.get('scale', 1000)
    if not type_map:
        print(f'  [skip] {case_dir}: no type_map in meta.json')
        return None
    if verbose:
        print(f'\n=== {meta.get("name", case_dir.name)}  ({case_dir}) ===')
    return compute_case(case_dir.name, case_dir, type_map, scale=scale, verbose=verbose)


# ───────────────────────────────── selftest ─────────────────────────────────
#: v2 이전 코드 (`e72067854` 의 이 파일 + `plastic_coverage.film_area_from_overlap`) 가 **base 합성 침대**에서 낸
#: legacy 산출의 sha256.  ⚠ **실측 핀이다** — 옛 `compute_case` 를 같은 fixture 에 돌려 찍었다 (손으로 짓지 않는다:
#: `plastic_coverage` selftest ⑨ 의 교훈).  v2 를 더한 뒤에도 legacy 키 · 값 · 순서 · per-AM CSV · 반환값이 이 핀과
#: 바이트 동일해야 한다 (코퍼스 physics σ · Stage E · σ_thermal T1 physics 타깃이 legacy 위에 서 있다).
_PIN_LEGACY = {
    'full_metrics': 'a2f0d685d1e1bcf5099289f85535338a181f069702cde916a559a0c13c933d08',     # json.dumps({v2 키를 뺀 full_metrics}, indent=2, default=str) — 옛 파일 바이트와 같다
    'per_am_csv':   '3c27b2a79117eba0785a3c33d8d0bfe4728ddd6006aeb3a6a83d79f25056efa9',    # coverage_per_am.csv (줄끝 \n 정규화)
    'summary':      '6624d46ed2ce5c9470f086d6f83b633dc9561ec0d0c9df012ade0c299a659ef1',    # json.dumps(compute_case 반환값, sort_keys=True)
}


def _selftest_fixture(case_dir: Path, *, variant: str = 'base') -> tuple:
    """합성 침대 — 덤프 단위 (= SI × 1000, scale 1000).  반환 `(case_dir, type_map, scale)`.

    AM_P (id 1, r 2 µm) · AM_S (id 2, r 1 µm) · SE (id 3–10, r 0.5 µm).  접촉 δ/R* 는 v2 결속 다섯 가지
    (elastic · tabor · volume · geom · none) 와 L > U 충돌 두 건 (1–4 · 2–6, 둘 다 AM–SE) 을 낸다.
    ligg = 기하 교차원판 (LIGGGHTS `contact_area` 규약, `L1-04`).  미지 id 행 (99–3) 하나 · δ = 0 행 (7–8) 하나.
    variant: base · amam_x2 (AM–AM 의 native 면적만 2 배) · nan_delta (1–5 의 δ = NaN) · scale1 (meta scale 1) ·
             no_ligg_col (contact_area 열 없음) · stale_v2 (옛 v2 키를 미리 심는다)
    """
    import csv as _csv
    from plastic_coverage import _intersection_disc_area
    um = 1e-3
    radii = {1: 2.0 * um, 2: 1.0 * um}
    types = {1: 1, 2: 2}
    for i in range(3, 11):
        radii[i], types[i] = 0.5 * um, 3
    spec = [(1, 3, 0.2), (1, 4, 0.01), (1, 5, 0.05), (2, 6, 0.004), (2, 7, 0.0005), (2, 8, 0.1),
            (3, 4, 0.05), (5, 6, 0.3), (9, 10, 0.9), (1, 2, 0.3), (7, 8, 0.0), (99, 3, 0.05)]
    case_dir.mkdir(parents=True, exist_ok=True)
    with open(case_dir / 'atoms.csv', 'w', newline='') as fh:
        w = _csv.writer(fh, lineterminator='\n')
        w.writerow(['id', 'type', 'radius', 'x', 'y', 'z'])
        for i in sorted(radii):
            w.writerow([i, types[i], repr(radii[i]), 0.0, 0.0, 0.0])
    cols = ['id1', 'id2', 'delta'] + ([] if variant == 'no_ligg_col' else ['contact_area'])
    with open(case_dir / 'contacts.csv', 'w', newline='') as fh:
        w = _csv.writer(fh, lineterminator='\n')
        w.writerow(cols)
        for a, b, dr in spec:
            ra, rb = radii.get(a, 0.5 * um), radii.get(b, 0.5 * um)
            rs = ra * rb / (ra + rb)
            d = dr * rs
            lg = _intersection_disc_area(ra, rb, d)
            if variant == 'amam_x2' and {a, b} == {1, 2}:
                lg *= 2.0
            if variant == 'nan_delta' and (a, b) == (1, 5):
                d = float('nan')
            w.writerow([a, b, repr(d)] + ([] if variant == 'no_ligg_col' else [repr(lg)]))
    fm = {'porosity': 15.6, 'coverage_AM_P_mean': 1.0, 'kept_key': 'keep'}
    if variant == 'stale_v2':
        fm.update({'coverage_AM_P_mean_physics_v2': 999.0, 'bogus_physics_v2': 1})
    (case_dir / 'full_metrics.json').write_text(json.dumps(fm, indent=2))
    (case_dir / 'se_clusters.json').write_text(json.dumps(
        {'clusters': [{'paths': [{'ids': [3, 4]}, {'ids': [5, 6]}, {'ids': [1, 3, 4]}]}]}))
    scale = 1 if variant == 'scale1' else 1000
    (case_dir / 'meta.json').write_text(json.dumps(
        {'name': case_dir.name, 'type_map': '1:AM_P,2:AM_S,3:SE', 'scale': scale}))
    return case_dir, {1: 'AM_P', 2: 'AM_S', 3: 'SE'}, scale


def _legacy_digests(case_dir: Path, summary) -> dict:
    """legacy 산출의 sha256 셋 — v2 키 (`*_physics_v2`) 를 뺀 full_metrics · per-AM CSV · 반환값."""
    import hashlib
    fm = json.loads((case_dir / 'full_metrics.json').read_text())
    leg = {k: v for k, v in fm.items() if not k.endswith('_physics_v2')}
    csv_txt = (case_dir / 'coverage_per_am.csv').read_text().replace('\r\n', '\n')
    return {'full_metrics': hashlib.sha256(json.dumps(leg, indent=2, default=str).encode()).hexdigest(),
            'per_am_csv': hashlib.sha256(csv_txt.encode()).hexdigest(),
            'summary': hashlib.sha256(json.dumps(summary, sort_keys=True).encode()).hexdigest()}


def _selftest() -> int:
    """physics v2 병기 (1저자 결정 2026-09-29) — legacy 바이트 동일 · DESC-03 · L1-01 전파 · 분모 장부 · 조용한 대체 없음 ·
    데이터 폴더 (WEBAPP_*_FOLDER).  반례를 먼저 옮기고 옛 코드에서 실패를 확인한 뒤 고쳤다."""
    import tempfile
    import shutil
    fails = []

    def chk(name, cond, extra=''):
        print(('  ✓ ' if cond else '  ✗ ') + name + (f'   {extra}' if extra else ''))
        if not cond:
            fails.append(name)

    _v2 = film_area_physics_v2           # 기대 장부를 **접촉별 직접 호출**로 다시 센다 (compute_case 의 집계와 독립)
    v2_suffix = '_physics_v2'
    tmp = Path(tempfile.mkdtemp(prefix='covv2_'))
    env_keep = {k: os.environ.get(k) for k in ('WEBAPP_RESULTS_FOLDER', 'WEBAPP_UPLOAD_FOLDER',
                                                'WEBAPP_ARCHIVE_FOLDER')}
    try:
        def run(variant, sub=None):
            cd, tm, sc = _selftest_fixture(tmp / (sub or variant), variant=variant)
            summ = compute_case(cd.name, cd, tm, scale=sc, write_csv=True, update_metrics=True)
            raw = (cd / 'full_metrics.json').read_text()
            return cd, summ, json.loads(raw), raw

        def expected_v2(cd, scale=1000):
            """fixture 의 접촉을 **직접** v2 함수에 넣어 기대 장부를 다시 센다 (compute_case 의 집계와 독립)."""
            if _v2 is None:
                return None
            at = pd.read_csv(cd / 'atoms.csv')
            ct = pd.read_csv(cd / 'contacts.csv')
            r = dict(zip(at['id'].astype(int), at['radius'].astype(float)))
            t = dict(zip(at['id'].astype(int), at['type'].astype(int)))
            e = dict(n=0, n_cap=0, n_conf=0, conf_pair={'AM_SE': 0, 'SE_SE': 0, 'AM_AM': 0, 'other': 0},
                     bind={b: 0 for b in ('elastic', 'tabor', 'volume', 'geom', 'none')},
                     bind_amse={b: 0 for b in ('elastic', 'tabor', 'volume', 'geom', 'none')},
                     amse=defaultdict(float), amam=defaultdict(float), tot={'AM_SE': 0.0, 'SE_SE': 0.0, 'AM_AM': 0.0},
                     unknown=0)
            for _, c in ct.iterrows():
                i1, i2 = int(c['id1']), int(c['id2'])
                if i1 not in t or i2 not in t:
                    e['unknown'] += 1
                    continue
                A, comp = _v2(float(c['delta']), r[i1], r[i2], ligg_area=float(c['contact_area']),
                              length_scale=scale)
                am1, am2 = t[i1] in (1, 2), t[i2] in (1, 2)
                pair = ('AM_SE' if (am1 != am2) else 'AM_AM' if am1 else 'SE_SE')
                e['n'] += 1
                e['bind'][comp['binding']] += 1
                if comp['cap_conflict'] is not None:
                    e['n_cap'] += 1
                if comp['cap_conflict']:
                    e['n_conf'] += 1
                    e['conf_pair'][pair] += 1
                e['tot'][pair] += A
                if pair == 'AM_SE':
                    e['bind_amse'][comp['binding']] += 1
                    e['amse'][i1 if am1 else i2] += A
                elif pair == 'AM_AM':
                    e['amam'][i1] += A
                    e['amam'][i2] += A
            cov = {}
            for aid in (1, 2):
                surf = 4.0 * np.pi * r[aid] * r[aid]
                free = max(surf - e['amam'][aid], 0.0)
                cov[aid] = min(e['amse'][aid] / free * 100, 100.0) if free > 0 else 0.0
            e['cov'] = cov
            return e

        # ① legacy 바이트 동일 — v2 를 더해도 legacy 키 · 값 · 순서 · CSV · 반환값이 v2 이전 코드의 실측 핀과 같다
        cd, summ, fm, raw = run('base')
        dg = _legacy_digests(cd, summ)
        bad = [k for k in _PIN_LEGACY if dg[k] != _PIN_LEGACY[k]]
        chk('① legacy 바이트 동일: full_metrics(v2 키 제외) · per-AM CSV · 반환값 = v2 이전 코드의 실측 핀',
            not bad, f'다름: {bad}' if bad else '')
        chk('①b 원래 있던 키는 그대로 (porosity · kept_key · coverage_AM_P_mean)',
            fm.get('porosity') == 15.6 and fm.get('kept_key') == 'keep' and fm.get('coverage_AM_P_mean') == 1.0)

        # ② v2 키 — 이름 규약 · 상태 ok · 전부 유한 (NaN/Infinity 토큰 없음)
        v2k = sorted(k for k in fm if k.endswith(v2_suffix))
        want_keys = {f'coverage_{lb}_{s}_physics_v2' for lb in ('AM_P', 'AM_S') for s in ('mean', 'std')} | {
            'coverage_AM_mean_physics_v2', 'area_AM전체_SE_total_physics_v2', 'area_SE_SE_total_physics_v2',
            'area_AM전체_AM_total_physics_v2', 'n_contacts_physics_v2', 'n_cap_branch_physics_v2',
            'cap_conflict_n_physics_v2', 'cap_conflict_frac_physics_v2', 'cap_conflict_frac_cap_branch_physics_v2',
            'cap_conflict_n_by_pair_physics_v2', 'A_binding_counts_total_physics_v2',
            'A_binding_counts_AM_SE_physics_v2', 'am_denominator_physics_v2', 'n_contacts_unknown_id_physics_v2',
            'n_contact_failures_physics_v2', 'coverage_status_physics_v2', 'rule_physics_v2',
            'h_film_sim_physics_v2'}
        strict_ok = True
        try:
            json.loads(raw, parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))
        except ValueError:
            strict_ok = False
        chk('② v2 키가 legacy 옆에 선다 — 이름 규약 (*_physics_v2) · status ok · NaN/Infinity 토큰 없음',
            set(v2k) == want_keys and fm.get('coverage_status_physics_v2') == 'ok' and strict_ok,
            f'없음 {sorted(want_keys - set(v2k))} · 남음 {sorted(set(v2k) - want_keys)} · '
            f'status={fm.get("coverage_status_physics_v2")!r} · strict={strict_ok}')

        e = expected_v2(cd)
        # ③ DESC-03 (침대 수준) — legacy 는 덤프 단위라 부피 cap 이 **한 번도** 결속하지 않는다; v2 는 결속한다
        leg_vol = (fm.get('A_binding_share_total_pct') or {}).get('volume')
        got_b = fm.get('A_binding_counts_total_physics_v2')
        chk('③ ★ DESC-03: legacy 부피 결속 0.0 % (단위 교란) ↔ v2 결속 수 = 접촉별 직접 호출과 같다 (volume ≥ 1)',
            leg_vol == 0.0 and e is not None and got_b == e['bind'] and got_b.get('volume', 0) >= 1
            and fm.get('A_binding_counts_AM_SE_physics_v2') == e['bind_amse'],
            f'legacy volume {leg_vol} % · v2 {got_b} · 기대 {e and e["bind"]}')

        # ④ L1-01 전파 — legacy 는 충돌을 산출에 싣지 않는다; v2 는 수 · 분율 (두 분모) · 상 쌍별로 싣는다
        leg_conf = [k for k in fm if 'conflict' in k and not k.endswith(v2_suffix)]
        chk('④ ★ L1-01: legacy 산출에는 충돌 키가 없다 ↔ v2 = 직접 호출 장부 (n · 분율 · cap 가지 분율 · 상 쌍별)',
            not leg_conf and e is not None
            and fm.get('cap_conflict_n_physics_v2') == e['n_conf'] == 2
            and fm.get('n_contacts_physics_v2') == e['n'] and fm.get('n_cap_branch_physics_v2') == e['n_cap']
            and fm.get('cap_conflict_frac_physics_v2') == round(e['n_conf'] / e['n'], 6)
            and fm.get('cap_conflict_frac_cap_branch_physics_v2') == round(e['n_conf'] / e['n_cap'], 6)
            and fm.get('cap_conflict_n_by_pair_physics_v2') == e['conf_pair'],
            f"legacy {leg_conf} · v2 n={fm.get('cap_conflict_n_physics_v2')} / {fm.get('n_contacts_physics_v2')} · "
            f"cap {fm.get('n_cap_branch_physics_v2')} · pair {fm.get('cap_conflict_n_by_pair_physics_v2')}")

        # ⑤ 분모 장부 — AM–AM 의 native 면적만 두 배로 (δ 는 그대로 ⇒ physics 면적은 같다)
        _cd5, _s5, fm5, _r5 = run('amam_x2')
        leg_moved = [lb for lb in ('AM_P', 'AM_S')
                     if fm5.get(f'coverage_{lb}_mean_physics') != fm.get(f'coverage_{lb}_mean_physics')]
        v2_same = all(fm5.get(k) == fm.get(k) and fm.get(k) is not None
                      for k in ('coverage_AM_P_mean_physics_v2', 'coverage_AM_S_mean_physics_v2',
                                'coverage_AM_mean_physics_v2'))
        chk('⑤ ★ 분모 장부: native AM–AM 면적만 바꾸면 legacy physics 피복률이 움직인다 (분자 physics · 분모 native) '
            '↔ v2 는 그대로 (같은 장부)',
            leg_moved == ['AM_P', 'AM_S'] and fm5.get('area_AM전체_AM_total_physics') == fm.get('area_AM전체_AM_total_physics')
            and v2_same,
            f"legacy AM_P {fm.get('coverage_AM_P_mean_physics')}→{fm5.get('coverage_AM_P_mean_physics')} · "
            f"v2 AM_P {fm.get('coverage_AM_P_mean_physics_v2')}→{fm5.get('coverage_AM_P_mean_physics_v2')}")

        # ⑥ v2 피복률 = 직접 호출로 다시 센 값 (분모 = 4πr² − Σ A_v2(AM–AM)) · 전체 = 입자 수 가중 평균 (legacy 와 같은 가중)
        ok6 = e is not None and all(
            fm.get(f'coverage_{lb}_mean_physics_v2') == round(float(e['cov'][aid]), 3)
            for lb, aid in (('AM_P', 1), ('AM_S', 2))) and fm.get('coverage_AM_mean_physics_v2') == round(
            float(np.mean([e['cov'][1], e['cov'][2]])), 3) and fm.get('area_AM전체_SE_total_physics_v2') == round(
            e['tot']['AM_SE'] * 1e6, 2) and fm.get('area_SE_SE_total_physics_v2') == round(e['tot']['SE_SE'] * 1e6, 2) \
            and fm.get('area_AM전체_AM_total_physics_v2') == round(e['tot']['AM_AM'] * 1e6, 2)
        chk('⑥ v2 피복률 · 면적 합 = 접촉별 직접 호출로 다시 센 값 (분모 v2 AM–AM · 전체 = 입자 수 가중 평균)', ok6,
            (f"AM_P {fm.get('coverage_AM_P_mean_physics_v2')} vs {round(float(e['cov'][1]), 3)} · "
             f"AM_S {fm.get('coverage_AM_S_mean_physics_v2')} vs {round(float(e['cov'][2]), 3)}") if e else 'v2 함수 없음')

        # ⑦ 조용한 대체 없음 — δ = NaN 한 행: legacy 는 그 접촉을 native 면적으로 **조용히** 넣고 정상 값을 낸다;
        #    v2 는 그 침대를 빈칸으로 두고 사유를 적는다
        _cd7, _s7, fm7, _r7 = run('nan_delta')
        st7 = str(fm7.get('coverage_status_physics_v2'))
        chk('⑦ ★ 접촉 하나가 v2 함수에서 실패 → 침대 v2 = 빈칸 + 사유 (legacy 는 native 로 조용히 대체해 값을 낸다)',
            isinstance(fm7.get('coverage_AM_P_mean_physics'), float)
            and st7.startswith('blank') and 'delta' in st7 and fm7.get('n_contact_failures_physics_v2') == 1
            and all(fm7.get(k) is None for k in ('coverage_AM_P_mean_physics_v2', 'coverage_AM_mean_physics_v2',
                                                 'area_AM전체_SE_total_physics_v2', 'cap_conflict_n_physics_v2',
                                                 'A_binding_counts_total_physics_v2')),
            f'status={st7!r} · 실패 {fm7.get("n_contact_failures_physics_v2")}')

        # ⑧ scale ≠ 1000 → v2 빈칸 (두 길이 규약 µm = sim×scale · SI = sim/scale 이 1000 에서만 같다) · legacy 는 그대로 계산
        _cd8, _s8, fm8, _r8 = run('scale1')
        st8 = str(fm8.get('coverage_status_physics_v2'))
        chk('⑧ scale ≠ 1000 → v2 빈칸 + 사유 (길이 규약이 모호하다) · legacy 는 계산된다',
            st8.startswith('blank') and 'scale' in st8 and fm8.get('coverage_AM_mean_physics_v2') is None
            and fm8.get('coverage_AM_mean_physics') is not None, f'status={st8!r}')

        # ⑨ contact_area 열이 없으면 v2 빈칸 (충돌 하한 L 을 조용히 Hertz 로 낮추지 않는다) · legacy 는 계산된다
        _cd9, _s9, fm9, _r9 = run('no_ligg_col')
        st9 = str(fm9.get('coverage_status_physics_v2'))
        chk('⑨ contacts.csv 에 contact_area 열이 없으면 v2 빈칸 + 사유 · legacy 는 계산된다',
            st9.startswith('blank') and 'contact_area' in st9 and fm9.get('coverage_AM_mean_physics') is not None,
            f'status={st9!r}')

        # ⑩ 데이터 폴더 — 웹앱과 LHS 배치는 WEBAPP_*_FOLDER 로 코드 밖 폴더를 쓴다.  `<case_id>` 로 부르면 그 폴더에서 찾아야 한다
        #    (옛 코드는 스크립트 옆 webapp/ 만 봐서 "[skip]" 을 찍고 rc 0 = 조용히 아무것도 안 썼다)
        res, up = tmp / 'wa' / 'results', tmp / 'wa' / 'uploads'
        cid = 'covv2_env_case'
        cd10, _tm10, _sc10 = _selftest_fixture(res / cid)
        (up / cid).mkdir(parents=True)
        shutil.move(str(cd10 / 'meta.json'), str(up / cid / 'meta.json'))     # 웹앱 배치: meta 는 uploads 에
        os.environ['WEBAPP_RESULTS_FOLDER'] = str(res)
        os.environ['WEBAPP_UPLOAD_FOLDER'] = str(up)
        os.environ['WEBAPP_ARCHIVE_FOLDER'] = str(tmp / 'wa' / 'archive')
        s10 = process_one(cid)
        fm10 = json.loads((cd10 / 'full_metrics.json').read_text())
        chk('⑩ ★ WEBAPP_*_FOLDER 를 따른다 — `<case_id>` 호출이 코드 밖 results/uploads 에서 침대를 찾아 v2 까지 쓴다',
            s10 is not None and fm10.get('coverage_status_physics_v2') == 'ok',
            f'반환 {"None (조용한 skip)" if s10 is None else "summary"} · status={fm10.get("coverage_status_physics_v2")!r}')

        # ⑪ 옛 v2 세대가 남지 않는다 — v2 키는 이 스크립트가 통째로 소유한다
        _cd11, _s11, fm11, _r11 = run('stale_v2')
        chk('⑪ 미리 있던 *_physics_v2 키는 전부 걷고 새로 쓴다 (bogus 없음 · 999 덮임)',
            'bogus_physics_v2' not in fm11 and fm11.get('coverage_AM_P_mean_physics_v2') == fm.get('coverage_AM_P_mean_physics_v2'),
            f"bogus={'bogus_physics_v2' in fm11} · AM_P={fm11.get('coverage_AM_P_mean_physics_v2')}")

        # ⑫ δ = 0 행은 v2 결속 none (면적 0) · 미지 id 행은 세어 둔다 (legacy 와 같은 모집단 — 둘 다 건너뛴다)
        chk('⑫ δ = 0 행 → v2 결속 none 1 · 미지 id 행 1 (세어 둔다)',
            (fm.get('A_binding_counts_total_physics_v2') or {}).get('none') == 1
            and fm.get('n_contacts_unknown_id_physics_v2') == 1 == (e or {}).get('unknown'),
            f"none={(fm.get('A_binding_counts_total_physics_v2') or {}).get('none')} · "
            f"unknown={fm.get('n_contacts_unknown_id_physics_v2')}")
    finally:
        for k, v in env_keep.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        shutil.rmtree(tmp, ignore_errors=True)
    print(f'\ncoverage_physics_vs_hertzian SELFTEST {"PASS" if not fails else f"FAIL ({len(fails)})"}')
    return 0 if not fails else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cases', nargs='*', help='case_id(s) to process')
    ap.add_argument('--all', action='store_true',
                    help='Process every case in webapp/results and webapp/archive')
    ap.add_argument('--case-dir', default=None,
                    help='Operate directly on a case directory (for archive '
                         'folders not under webapp/results or webapp/archive/<cid>).')
    ap.add_argument('--selftest', action='store_true',
                    help='physics v2 병기 회귀 (legacy 바이트 동일 · DESC-03 · L1-01 · 분모 장부 · 데이터 폴더)')
    args = ap.parse_args()
    if args.selftest:
        sys.exit(_selftest())

    # --case-dir short-circuit: one-shot mode for archive reanalyze
    if args.case_dir:
        case_dir = Path(args.case_dir).resolve()
        s = process_dir(case_dir, verbose=True)
        if s is None:
            sys.exit(1)
        for lbl, v in s.items():
            print(f'  {lbl:5s}  H={v["hertzian_mean"]:5.2f}%  '
                  f'P={v["physics_mean"]:5.2f}%  '
                  f'Δ={v["delta_mean_pct"]:+6.2f}%  n={v["n"]}')
        return

    cases: list[str] = []
    if args.all:
        for root in _webapp_dirs()[:2]:                       # results · archive (WEBAPP_*_FOLDER 를 따른다)
            if root.exists():
                # Recursive depth search — covers webapp/archive/category/case/
                # Categorized cases were silently skipped under depth-1 scan.
                for atoms_p in root.rglob('atoms.csv'):
                    case_dir = atoms_p.parent
                    if (case_dir / 'contacts.csv').exists():
                        cases.append(case_dir.name)
    cases.extend(args.cases)
    cases = list(dict.fromkeys(cases))  # dedup, preserve order

    if not cases:
        ap.error('No cases selected. Pass case_id(s) or use --all.')

    print(f'Processing {len(cases)} case(s) ...')
    summary_rows = []
    for cid in cases:
        s = process_one(cid, verbose=True)
        if s is None:
            continue
        meta = load_meta(cid)
        nm = meta.get('name', cid)
        for lbl, v in s.items():
            print(f'  {nm:34s} {lbl:5s}  H={v["hertzian_mean"]:5.2f}%  '
                  f'P={v["physics_mean"]:5.2f}%  '
                  f'Δ={v["delta_mean_pct"]:+6.2f}%  n={v["n"]}')
            summary_rows.append({
                'case_id': cid, 'name': nm, 'am_type': lbl,
                'n_AM': v['n'],
                'cov_hertzian_pct': round(v['hertzian_mean'], 3),
                'cov_physics_pct':  round(v['physics_mean'], 3),
                'delta_pct':        round(v['delta_mean_pct'], 2),
            })

    if summary_rows:
        out_dir = Path('docs/figures/physics_regime')
        out_dir.mkdir(parents=True, exist_ok=True)
        out_csv = out_dir / 'coverage_hertz_vs_physics_summary.csv'
        pd.DataFrame(summary_rows).to_csv(out_csv, index=False)
        print(f'\n→ {out_csv}  ({len(summary_rows)} rows)')

        # Quick stats
        df = pd.DataFrame(summary_rows)
        print('\n=== Summary (Δ coverage % : physics vs hertzian) ===')
        for lbl, sub in df.groupby('am_type'):
            print(f'  {lbl:5s}  n_cases={len(sub):3d}  '
                  f'Δ median={sub["delta_pct"].median():+6.2f}%  '
                  f'mean={sub["delta_pct"].mean():+6.2f}%  '
                  f'max={sub["delta_pct"].abs().max():6.2f}%')

        # Verdict
        mean_all = df['delta_pct'].mean()
        print(f'\nVERDICT: Across all AM types and cases, '
              f'coverage in Physics mode differs from Hertzian by '
              f'mean Δ = {mean_all:+.2f}%.')


if __name__ == '__main__':
    main()
