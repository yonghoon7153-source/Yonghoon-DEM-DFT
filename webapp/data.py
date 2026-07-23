"""
data.py — DFT 지식 인프라 데이터 계층 (Flask 라우트가 이걸 호출).

핵심 철학: db/ 를 실시간으로 읽어 "조성 × 물성" 매트릭스를 구성한다.
db 파일이 바뀌면(계산 등록) 사이트가 자동으로 최신값을 반영 = "계속 동기화".
canonical 방법 메타(kb/methodology/computational_methods_canonical.md)와 연동해
각 값에 pseudo/k/cell·비교가능성·stale 배지를 붙일 수 있게 한다.
"""
from __future__ import annotations
import json, csv, re, os
from pathlib import Path
from functools import lru_cache

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db"
KB = ROOT / "kb"
LITDB = ROOT / "litdb"
CONCEPTS = KB / "concepts"


# ─────────────────────────────────────────────────────────────
# 개념 상세 페이지 (Glossary '더보기' → kb/concepts/<id>.md)
# ─────────────────────────────────────────────────────────────
def concept_ids() -> set:
    """kb/concepts/*.md 로 존재하는 개념 id 집합 (더보기 링크 노출 판단)."""
    return {f.stem for f in CONCEPTS.glob("*.md")} if CONCEPTS.exists() else set()

def read_concept(cid: str) -> str | None:
    """개념 원본 마크다운. 경로 탈출 방어."""
    p = (CONCEPTS / f"{cid}.md").resolve()
    if not p.is_relative_to(CONCEPTS.resolve()) or not p.exists():
        return None
    return p.read_text(errors="ignore")

# ─────────────────────────────────────────────────────────────
# 로더 (캐시 없음 — 항상 최신 db 반영; 무거우면 mtime 캐시로 교체)
# ─────────────────────────────────────────────────────────────
def _load_json(p: Path):
    try:
        return json.loads(p.read_text())
    except Exception:
        return None

def load_index() -> dict:
    return _load_json(DB / "_index.json") or {}

def load_compositions() -> dict:
    out = {}
    for f in sorted((DB / "compositions").glob("*.json")):
        d = _load_json(f)
        if d is not None:
            out[f.stem] = d
    return out

def load_properties() -> dict:
    """db/properties/*.json 전부 (하위폴더 포함 최상위만)."""
    out = {}
    for f in sorted((DB / "properties").glob("*.json")):
        d = _load_json(f)
        if d is not None:
            out[f.stem] = d
    return out

def load_canonical_methods() -> str:
    p = KB / "methodology" / "computational_methods_canonical.md"
    return p.read_text() if p.exists() else ""

# ─────────────────────────────────────────────────────────────
# 조성 노드 정의 (표시 메타)
# ─────────────────────────────────────────────────────────────
COMPOSITIONS = {
    "comp1":       {"formula": "Li₆PS₅Cl",             "label": "LPSCl",     "family": "argyrodite", "cell": "cubic-52",  "color": "#2563eb"},
    "comp2":       {"formula": "Li₆PS₅Cl₀.₅Br₀.₅",     "label": "LPSClBr",   "family": "argyrodite", "cell": "cubic-52",  "color": "#0d9488"},
    "comp3":       {"formula": "Li₆PS₅Cl₀.₅I₀.₅",      "label": "LPSClI",    "family": "argyrodite", "cell": "rhombo-62", "color": "#7c3aed"},
    "comp4":       {"formula": "Li₆PS₅Br",             "label": "LPSBr",     "family": "argyrodite", "cell": "rhombo-62", "color": "#c05621"},
    "comp5":       {"formula": "Li₆PS₅I",              "label": "LPSI",      "family": "argyrodite", "cell": "rhombo-62", "color": "#be123c"},
    "modelc":      {"formula": "Li₅.₄PS₄.₄Cl₁.₆",      "label": "LPSCl1.6",  "family": "argyrodite", "cell": "rhombo-62", "color": "#0284c7"},
    "modelc_v3":   {"formula": "Li₅.₄PS₄.₄Cl₁.₆ (v3)", "label": "LPSCl1.6 v3","family": "argyrodite","cell": "rhombo-62", "color": "#0369a1"},
    "modelc_nd_doped": {"formula": "Nd-doped LPSCl1.6","label": "NdO-LPSCl", "family": "doped",     "cell": "rhombo-62", "color": "#65a30d"},
    "lpsocl":      {"formula": "Li₂₇P₅S₂₁OCl₈",        "label": "LPSOCl (+O)","family": "doped",     "cell": "rhombo-62", "color": "#be123c"},
    "b2o3":        {"formula": "B₂O₃-doped LPSCl1.6",  "label": "B₂O₃-LPSCl","family": "doped",      "cell": "128-SC",    "color": "#0284c7"},
    "vgcf_hbn":    {"formula": "VGCF / h-BN + Li",     "label": "VGCF-hBN",  "family": "anode",      "cell": "slab",      "color": "#6b7280"},
    "li3n":        {"formula": "Li₃N",                 "label": "Li₃N interphase", "family": "interphase", "cell": "—",   "color": "#7c3aed"},
    "lic6":        {"formula": "LiC₆",                 "label": "LiC₆ interphase", "family": "interphase", "cell": "—",   "color": "#c05621"},
    "sdcp":        {"formula": "SDCP molecules",       "label": "SDCP (ORCA IR)",  "family": "molecular",  "cell": "—",   "color": "#65a30d"},
}

# 조성군(family) 표시 순서/그룹
FAMILY_ORDER = ["argyrodite", "doped", "anode", "interphase", "molecular"]

# ─────────────────────────────────────────────────────────────
# 물성 카테고리 (post-processing 축) — 파일명 키워드로 분류
# ─────────────────────────────────────────────────────────────
CATEGORIES = [
    {"id": "electronic", "label": "Electronic",  "icon": "⚡", "keys": ["electronic", "dos", "pdos", "bader", "elf", "xps"]},
    {"id": "mechanical", "label": "Mechanical",  "icon": "🔩", "keys": ["elastic", "eos", "thermal_thprime"]},
    {"id": "bonding",    "label": "Bonding",     "icon": "🔗", "keys": ["bonds", "icohp", "cohp", "nd_icohp"]},
    {"id": "ionic",      "label": "Ionic",       "icon": "🔋", "keys": ["diffusion", "li_transport", "md_arrhenius", "bvse", "msd", "dualx"]},
    {"id": "interface",  "label": "Interface",   "icon": "🧩", "keys": ["adhesion", "oxidation", "sei", "interface", "esw", "anode"]},
    {"id": "structural", "label": "Structural",  "icon": "🧊", "keys": ["phonon", "voronoi", "coordination", "bond_lengths", "eos_dft"]},
    {"id": "cascade",    "label": "Cascade/ML",  "icon": "🤖", "keys": ["cascade", "doping", "alpha_sensitivity"]},
    {"id": "literature", "label": "Literature",  "icon": "📚", "keys": ["literature", "audit"]},
]

def categorize(prop_name: str) -> str:
    n = prop_name.lower()
    for c in CATEGORIES:
        if any(k in n for k in c["keys"]):
            return c["id"]
    return "other"

# ─────────────────────────────────────────────────────────────
# 조성 → 관련 파일 매핑 (구조 / property / csv)
# ─────────────────────────────────────────────────────────────
_PREFIX = {
    "comp1": ["comp1"], "comp2": ["comp2"], "comp3": ["comp3"], "comp4": ["comp4"],
    "comp5": ["comp5"], "modelc": ["modelc", "modelC"], "modelc_v3": ["modelc_v3", "modelC_v3"],
    "modelc_nd_doped": ["modelc_nd", "nd_"], "lpsocl": ["lpsocl"], "b2o3": ["b2o3"],
    "vgcf_hbn": ["vgcf", "hbn", "li3n", "lic6"],
}

# 파일이 여러 조성 prefix에 걸릴 때 "가장 긴(구체적) prefix"가 소유
# — modelc 페이지가 modelc_nd_doped_* / modelc_v3_* 파일을 끌어오지 않게.
_ALL_PREFIXES = sorted(
    {p.lower() for cid in COMPOSITIONS for p in _PREFIX.get(cid, [cid])},
    key=len, reverse=True)

def _blocked_by_longer(fname_lower: str, p: str) -> bool:
    return any(len(q) > len(p) and fname_lower.startswith(q) for q in _ALL_PREFIXES)

def _prefix_starts(fname: str, pref: list) -> bool:
    n = fname.lower()
    return any(n.startswith(p.lower()) and not _blocked_by_longer(n, p.lower()) for p in pref)


def structures_for(cid: str) -> list[dict]:
    pref = _PREFIX.get(cid, [cid])
    sd = DB / "structures"
    out = []
    if sd.exists():
        for f in sorted(sd.iterdir()):
            if f.is_file() and f.suffix.lower() in (".cif", ".xyz", ".vasp", ".vesta", ".cube"):
                if _prefix_starts(f.name, pref):
                    out.append({"name": f.name, "ext": f.suffix.lstrip("."), "viewable": f.suffix.lower() in (".cif", ".xyz")})
    return out

def datafiles_for(cid: str) -> list[dict]:
    """조성 관련 CSV/데이터 (차트용) — properties 전역에서 prefix 매칭."""
    pref = _PREFIX.get(cid, [cid])
    out = []
    for f in (DB / "properties").rglob("*"):
        if f.is_file() and f.suffix.lower() in (".csv",):
            # startswith는 최장 prefix 소유규칙 적용, 공유파일은 _infix_ 로 허용
            if _prefix_starts(f.name, pref) or any(f"_{p.lower()}" in f.name.lower() for p in pref):
                kind = _csv_kind(f.name)
                out.append({"name": f.name, "rel": str(f.relative_to(DB)), "kind": kind})
    return out

def _csv_kind(name: str) -> str:
    n = name.lower()
    for k, tag in [("pdos", "PDOS"), ("dos", "DOS"), ("arrhenius", "Arrhenius"),
                   ("msd", "MSD"), ("eos", "EOS"), ("phonon", "Phonon"),
                   ("bvse", "BVSE"), ("elf", "ELF"), ("bader", "Bader"),
                   ("xps", "XPS"), ("voronoi", "Voronoi"), ("ir", "IR")]:
        if k in n:
            return tag
    return "data"

# ─────────────────────────────────────────────────────────────
# 조성별 메트릭 (평탄 인덱스 + canonical 앵커)
# ─────────────────────────────────────────────────────────────
def index_metrics_by_comp(index: dict) -> dict:
    m = {}
    for dp in index.get("data_points", []):
        m.setdefault(dp.get("comp"), []).append(dp)
    return m

# canonical 앵커값 (kb 나침반과 일치 — 사이트 상단 요약/비교용)
CANONICAL = {
    "gap_eV":     {"comp1": 2.066, "comp2": 2.04, "modelc": 2.099, "lpsocl": 2.2309},
    "B0_GPa":     {"comp1": 26.23, "comp2": 25.8, "modelc": 21.71, "lpsocl": 24.71, "b2o3": 24.48},
    "E_VRH_GPa":  {"comp1": 22.06, "modelc": 27.66, "lpsocl": 35.04},  # relaxed-ion USPP; comp2 재측정중
    "MD_Ea_eV":   {"comp1": 0.253, "modelc": 0.224, "lpsocl": 0.279},  # UMA
    "ICOHP_PS":   {"comp1": -6.0, "comp2": -5.913, "modelc": -6.0, "lpsocl": -6.04, "modelc_nd_doped": -5.976},
}
CANONICAL_META = {
    "gap_eV":    "fixed-occ eigenvalue (DOS-threshold 금지)",
    "B0_GPa":    "DFT BM3 EOS",
    "E_VRH_GPa": "DFT relaxed-ion USPP·k444(comp1)/셀별·0.005 — comp1↔comp2만 완전비교",
    "MD_Ea_eV":  "UMA-s-1p1, 600/800/1000K 3-seed (pseudo 무관)",
    "ICOHP_PS":  "LOBSTER all-PAW ext-basis",
}

# ─────────────────────────────────────────────────────────────
# Cascade / ML 도핑 스크리닝 (디지털 트윈) — UMA 상대 스크리닝 번들
# ─────────────────────────────────────────────────────────────
CASCADE_FILES = {
    "ranked":      "cascade_v23_ranked.csv",       # 조성 합성점수 리더보드
    "champions":   "cascade_v23_champions.csv",    # 챔피언별 EOS·탄성·anneal
    "litransport": "cascade_v23_litransport.csv",  # Li 수송 프록시
    "synergy":     "cascade_v23_synergy_pairs.csv",# 공동도핑 시너지 가설
    "oxidation":   "oxidation_stability_cascade.csv",  # grand-potential ESW
}
CASCADE_META = {
    "title": "Doping Cascade — UMA 스크리닝 디지털 트윈",
    "scope": "Model C (Li₅.₄PS₄.₄Cl₁.₆) 기반 산화물/불화물 도펀트 스크리닝, x=0.25",
    "engine": "UMA-s-1p1 (task=omat) · anneal→champion→EOS/elastic/ESW/Li-proxy 캐스케이드",
    "score_formula": "score = 0.30·ox + 0.25·stable + 0.20·soft + 0.15·ductile + 0.10·window (min–max 정규화)",
    "caveat": "절대 탄성값은 실험(AFM/UPE 12–22 GPa) 대비 높게 나옴 — 캐스케이드 내부(UMA-vs-UMA) 순위·상대비교만. EOS B0 ≠ elastic B_VRH.",
    "verified": "직접 확인된 검증 서브셋은 doping_cascade_verified.json (41 챔피언 all-converged).",
}
# 조성 노드 ↔ 캐스케이드 도펀트 (스크리닝 히트의 DFT 심층검증)
CASCADE_DOPANT = {"modelc_nd_doped": "Nd2O3", "b2o3": "B2O3"}


def load_cascade() -> dict:
    out = {"meta": CASCADE_META}
    for k, fn in CASCADE_FILES.items():
        out[k] = read_csv(f"properties/{fn}")
    out["trivalent"] = _load_json(DB / "properties" / "doping_cascade_trivalent_M3.json")
    out["verified"] = _load_json(DB / "properties" / "doping_cascade_verified.json")
    out["alpha"] = _load_json(DB / "properties" / "alpha_sensitivity_FINAL.json")
    return out


def cascade_rows_for(dopant: str) -> dict:
    """특정 도펀트(예: Nd2O3)의 캐스케이드 행만 추림 — 조성 심층페이지용."""
    if not dopant:
        return {}
    d = dopant.lower()
    def _match(rows, cols):
        hit = []
        for r in rows.get("data", []):
            for c in cols:
                v = str(r.get(c, "")).lower()
                if v == d or v.startswith(d + "_") or v.startswith(d + "+"):
                    hit.append(r); break
        return hit
    casc = load_cascade()
    return {
        "dopant": dopant,
        "total": len(casc.get("ranked", {}).get("data", [])),
        "ranked": _match(casc["ranked"], ["dopant"]),
        "champions": _match(casc["champions"], ["dopant", "_dir"]),
        "litransport": _match(casc["litransport"], ["_dir"]),
        "oxidation": _match(casc["oxidation"], ["dopant"]),
    }


def icohp_for(cid: str):
    """조성별 LOBSTER ICOHP JSON (있으면) — bonds 테이블 렌더용. 공통 스키마."""
    pref = _PREFIX.get(cid, [cid])
    for f in sorted((DB / "properties").glob("*_icohp.json")):
        stem = f.stem.lower()
        if any(p.lower() in stem for p in pref):
            d = _load_json(f)
            if d and isinstance(d.get("bonds"), dict):
                return d
    return None


def build_matrix() -> dict:
    """사이트 전역 데이터 번들."""
    idx = load_index()
    comps = load_compositions()
    props = load_properties()
    # property → 카테고리
    prop_cat = {name: categorize(name) for name in props}
    return {
        "compositions": COMPOSITIONS,
        "categories": CATEGORIES,
        "comp_data": comps,
        "properties": props,
        "prop_category": prop_cat,
        "index_metrics": index_metrics_by_comp(idx),
        "canonical": CANONICAL,
        "canonical_meta": CANONICAL_META,
        "built": idx.get("built"),
        "literature_count": (sum(1 for _ in (LITDB / "papers").glob("*.md"))
                             if (LITDB / "papers").exists() else idx.get("literature_count", 0)),
    }

# ─────────────────────────────────────────────────────────────
# CSV → Plotly 시리즈 (차트 API)
# ─────────────────────────────────────────────────────────────
def _has_category_data(cid, cat_id, props, prop_cat, idx_metrics) -> bool:
    pref = _PREFIX.get(cid, [cid])
    # (a) property 파일 중 이 조성+카테고리
    for name in props:
        if prop_cat.get(name) == cat_id and any(p.lower() in name.lower() for p in pref):
            return True
    # (b) index_metrics path에 카테고리 키워드
    cat = next((c for c in CATEGORIES if c["id"] == cat_id), None)
    if cat:
        for dp in idx_metrics.get(cid, []):
            if any(k in str(dp.get("path", "")).lower() for k in cat["keys"]):
                return True
    # (c) 구조/CSV 존재 (structural/electronic 등)
    if cat_id in ("structural", "electronic") and structures_for(cid):
        return True
    if datafiles_for(cid):
        # 어떤 CSV가 이 카테고리에 속하면
        for df in datafiles_for(cid):
            kind = df["kind"].lower()
            if cat and any(k in kind for k in cat["keys"]):
                return True
    # (d) 캐스케이드 히트 조성(Nd2O3/B2O3 …) = 스크리닝 심층검증 대상
    if cat_id == "cascade" and cid in CASCADE_DOPANT:
        return True
    return False

def build_coverage(props, prop_cat, idx_metrics) -> dict:
    """{comp: {category_id: bool}} — True=데이터有, False=TODO(옅은색)."""
    cov = {}
    for cid in COMPOSITIONS:
        cov[cid] = {c["id"]: _has_category_data(cid, c["id"], props, prop_cat, idx_metrics)
                    for c in CATEGORIES}
    return cov

def coverage_stats(cov: dict) -> dict:
    total = sum(len(v) for v in cov.values())
    done = sum(1 for v in cov.values() for ok in v.values() if ok)
    return {"done": done, "total": total, "pct": round(100 * done / total) if total else 0}


# ─────────────────────────────────────────────────────────────
# 문헌 트랙 분류 (DEM·MPM 미세구조/역학  ↔  DFT·MLIP 전해질 화학)
# 각 논문 digest 의 자기신고 `type` 필드 + 슬러그 키워드로 점수화, 애매한 건 override.
# ─────────────────────────────────────────────────────────────
LIT_DEM_KW = [
    "dem", "mpm", "fem", "czm", "lbm", "rnm", " continuum", "contact", "percolation",
    "calender", "calendering", "compaction", "densification", "packing", "tortuosity",
    "impedance", "tlm", "de levie", "equivalent-circuit", "equivalent circuit",
    "microstructure", "drying", "mixer", "powder", "sps", "indentation", "adhesive",
    "cohesive", "binder", "dry electrode", "dry-electrode", "dry process", "dry-process",
    "dryprocess", "manufacturing", "multiphysics", "hertz", "holm", "constriction",
    "geodict", "elastoplastic", "sand", "snow", "co-rolling", "corolling", "mold",
    "sintering", "slurry", "morphology", "porosity", "digital twin", "digital-twin",
]
LIT_DFT_KW = [
    "dft", "mlip", "aimd", "first-principles", "first principles", "bvse", "pdos",
    "elf", "argyrodite", "orbital", "sevennet", "vasp", "screening", "thermodynamic",
    "migration", "bond order", "bond-order", "homo", "lumo", "haxpes", " ups ", "ups)",
    "band structure", "band gap", "bandgap", "cohp", "icohp", "oxidation", "esw",
    "halide", "iodide", "chlorination", "electron redistribution", "convex hull",
    "phase-stability", "phase stability", "adsorption", "hybridization", "dualdoping",
    "dual-doping", "dopant", "conductivity", "diffusion barrier", "hopping",
]
# 스코어로 못 가르는(또는 오분류되는) 논문 수동 지정
LIT_TRACK_OVERRIDE = {
    # 역학/미세구조/제조 쪽(내용에 DFT·ML 보조가 있어도 주제는 DEM 트랙)
    "han2025_icep_conductive_elastic_binder": "dem",
    "kang2025_bollard_anchored_binder_dry_electrode": "dem",
    "duquesnoy2023_ml_multiobjective_manufacturing_optimization": "dem",
    "schneider2023_particle_size_pressure_transport": "dem",
    "lee2026_eecfp_dnn_electrolyte_ce_lmb": "dem",
    "hollmann2025_tabpfn_tabular_foundation_model": "dem",
    "bzox_dry_zro2x_nmc_shell_coating_sulfide_assb": "dem",
    "jung2023_single_crystal_ncm_morphology": "dem",
    "kim2024_carbon_volumetric_occupation_se_domain": "dem",
    "reisacher2023_percolation_sulfide_carbon_matrix": "dem",
    "minnmann2024_microstructure_porosity_visualization": "dem",
    "mcgeary1961_bimodal_sphere_packing": "dem",
    "taufactor_tortuosity_factor_tomography_tool": "dem",
    "kim2025_conductive_agent_se_coating_cathode": "dem",   # 전극 미세구조/제조 (type의 'DFT 없음'이 kw 오탐)
    "kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review": "dem",  # echemo-역학 총설
    "deysher2022_transport_mechanical_aspects_assb_review": "dem",  # 전극 전달+역학 총설
    # 전해질 화학/전자구조/전기화학 쪽(순수 exp·경험식이어도 DFT 트랙 주제)
    "wang2022_sulfide_thermal_stability_th_descriptor": "dft",
    "kang2025_highvoltage_parasitic_reaction_benefit_sulfide_assb": "dft",
    "kim2026_iccf_molten_salt_sei_lpscl_sheet": "dft",
    "fan2026_sulfide_assb_stability_review_ECERD2600097": "dft",
    "whitten2023_ups_practical_best_practices": "dft",
    "hikima2022_operando_band_structure_assb": "dft",
    "ishikawa2025_site_percolation_cooperative_ion_conduction": "dft",
    "dyre2004_hopping_models_ion_conduction_noncrystals": "dft",
    "rao2011_argyrodite_se_studies_bvse": "dft",
    "cha2024_dualcompatible_halide_ncm_lpscl_interface": "dft",
    "yang2025_lao_dualdoping_argyrodite_lacl3": "dft",
    "liu2013_cage_methane_adsorption_hydrate_nucleation": "dft",
}


def literature_track(slug: str, type_str: str = "", title: str = "") -> str:
    if slug in LIT_TRACK_OVERRIDE:
        return LIT_TRACK_OVERRIDE[slug]
    hay = f" {slug} {type_str} {title} ".lower().replace("_", " ")
    dem = sum(1 for k in LIT_DEM_KW if k in hay)
    dft = sum(1 for k in LIT_DFT_KW if k in hay)
    if dem != dft:
        return "dem" if dem > dft else "dft"
    t = (type_str or "").lower().lstrip()
    if t.startswith(("dem", "mpm", "fem", "czm", "continuum", "tool")):
        return "dem"
    if t.startswith(("dft", "mlip", "aimd", "theory")):
        return "dft"
    return "dft"


def list_papers() -> list:
    """litdb/papers/*.md → [{id, title, type, track}] (DEM/DFT 분류 포함)."""
    out = []
    pd = LITDB / "papers"
    if not pd.exists():
        return out
    for f in sorted(pd.glob("*.md")):
        if f.stem.startswith("_"):
            continue
        title, type_str = f.stem.replace("_", " "), ""
        got_title = False
        try:
            head = f.read_text(errors="ignore").splitlines()[:18]
        except Exception:
            head = []
        for line in head:
            if not got_title and line.startswith("#"):
                title = line.lstrip("# ").strip()
                got_title = True
            m = re.search(r"type `([^`]+)`", line)
            if m and not type_str:
                type_str = m.group(1)
        out.append({"id": f.stem, "title": title, "type": type_str,
                    "track": literature_track(f.stem, type_str, title)})
    return out


def read_csv(rel: str) -> dict:
    p = (DB / rel).resolve()
    if not p.is_relative_to(DB.resolve()) or not p.exists():
        return {"error": "not found"}
    rows = list(csv.reader(p.open()))
    # 선행 주석(#)·빈 줄 제거 — cascade CSV들이 헤더 앞에 # 메타줄을 둠
    rows = [r for r in rows if r and not r[0].lstrip().startswith("#")]
    if not rows:
        return {"columns": [], "data": []}
    header = rows[0]
    data = []
    for r in rows[1:]:
        rec = {}
        for i, h in enumerate(header):
            v = r[i] if i < len(r) else ""
            try:
                rec[h] = float(v)
            except (ValueError, TypeError):
                rec[h] = v
        data.append(rec)
    return {"columns": header, "data": data, "n": len(data)}


# ═════════════════════════════════════════════════════════════
# 신규 기능 데이터층 (검색 / 주기율표 / Compute)
# ═════════════════════════════════════════════════════════════

# ── 조성별 원소 구성 (주기율표 explorer) ──
COMP_ELEMENTS = {
    "comp1": ["Li", "P", "S", "Cl"],
    "comp2": ["Li", "P", "S", "Cl", "Br"],
    "comp3": ["Li", "P", "S", "Cl", "I"],
    "comp4": ["Li", "P", "S", "Br"],
    "comp5": ["Li", "P", "S", "I"],
    "modelc": ["Li", "P", "S", "Cl"],
    "modelc_v3": ["Li", "P", "S", "Cl"],
    "modelc_nd_doped": ["Li", "P", "Nd", "S", "O", "Cl"],
    "lpsocl": ["Li", "P", "S", "O", "Cl"],
    "b2o3": ["Li", "P", "S", "Cl", "B", "O"],
    "vgcf_hbn": ["Li", "C", "B", "N", "H"],
    "li3n": ["Li", "N"],
    "lic6": ["Li", "C"],
    "sdcp": ["C", "H", "O", "S", "N", "Li"],
}

# 주기율표 배치 (sym, Z, group=열1..18, period=행; 란탄=8행·악티늄=9행 표시)
PERIODIC = [
    ("H",1,1,1),("He",2,18,1),
    ("Li",3,1,2),("Be",4,2,2),("B",5,13,2),("C",6,14,2),("N",7,15,2),("O",8,16,2),("F",9,17,2),("Ne",10,18,2),
    ("Na",11,1,3),("Mg",12,2,3),("Al",13,13,3),("Si",14,14,3),("P",15,15,3),("S",16,16,3),("Cl",17,17,3),("Ar",18,18,3),
    ("K",19,1,4),("Ca",20,2,4),("Sc",21,3,4),("Ti",22,4,4),("V",23,5,4),("Cr",24,6,4),("Mn",25,7,4),("Fe",26,8,4),("Co",27,9,4),("Ni",28,10,4),("Cu",29,11,4),("Zn",30,12,4),("Ga",31,13,4),("Ge",32,14,4),("As",33,15,4),("Se",34,16,4),("Br",35,17,4),("Kr",36,18,4),
    ("Rb",37,1,5),("Sr",38,2,5),("Y",39,3,5),("Zr",40,4,5),("Nb",41,5,5),("Mo",42,6,5),("Tc",43,7,5),("Ru",44,8,5),("Rh",45,9,5),("Pd",46,10,5),("Ag",47,11,5),("Cd",48,12,5),("In",49,13,5),("Sn",50,14,5),("Sb",51,15,5),("Te",52,16,5),("I",53,17,5),("Xe",54,18,5),
    ("Cs",55,1,6),("Ba",56,2,6),("La",57,3,6),("Hf",72,4,6),("Ta",73,5,6),("W",74,6,6),("Re",75,7,6),("Os",76,8,6),("Ir",77,9,6),("Pt",78,10,6),("Au",79,11,6),("Hg",80,12,6),("Tl",81,13,6),("Pb",82,14,6),("Bi",83,15,6),("Po",84,16,6),("At",85,17,6),("Rn",86,18,6),
    ("Fr",87,1,7),("Ra",88,2,7),("Ac",89,3,7),("Rf",104,4,7),("Db",105,5,7),("Sg",106,6,7),("Bh",107,7,7),("Hs",108,8,7),("Mt",109,9,7),("Ds",110,10,7),("Rg",111,11,7),("Cn",112,12,7),("Nh",113,13,7),("Fl",114,14,7),("Mc",115,15,7),("Lv",116,16,7),("Ts",117,17,7),("Og",118,18,7),
    ("Ce",58,4,8),("Pr",59,5,8),("Nd",60,6,8),("Pm",61,7,8),("Sm",62,8,8),("Eu",63,9,8),("Gd",64,10,8),("Tb",65,11,8),("Dy",66,12,8),("Ho",67,13,8),("Er",68,14,8),("Tm",69,15,8),("Yb",70,16,8),("Lu",71,17,8),
    ("Th",90,4,9),("Pa",91,5,9),("U",92,6,9),("Np",93,7,9),("Pu",94,8,9),("Am",95,9,9),("Cm",96,10,9),("Bk",97,11,9),("Cf",98,12,9),("Es",99,13,9),("Fm",100,14,9),("Md",101,15,9),("No",102,16,9),("Lr",103,17,9),
]

def element_to_comps() -> dict:
    out = {}
    for cid, els in COMP_ELEMENTS.items():
        for e in els:
            out.setdefault(e, []).append(cid)
    return out

def campaign_elements() -> set:
    return {e for els in COMP_ELEMENTS.values() for e in els}


# ── 전역 검색 인덱스 (⌘K) ──
def search_index() -> list:
    import glossary as G
    idx = []
    pages = [
        ("페이지", "Dashboard", "커버리지 매트릭스·조성 요약", "/"),
        ("페이지", "Property Explorer", "정렬·필터 물성 표 + provenance", "/explorer"),
        ("페이지", "Periodic Table", "원소별 조성 탐색", "/elements"),
        ("페이지", "Comparison", "조성 간 비교 + 레이더", "/compare"),
        ("페이지", "Cascade/ML", "UMA 도핑 스크리닝", "/cascade"),
        ("페이지", "Compute", "원클릭 계산 입력 생성", "/compute"),
        ("페이지", "Methods", "계산 방법 canonical", "/methods"),
        ("페이지", "Literature", "DEM/DFT 문헌", "/literature"),
        ("페이지", "Glossary", "용어 설명집", "/glossary"),
        ("페이지", "Work Log", "작업 기록", "/log"),
    ]
    for t, label, sub, url in pages:
        idx.append({"t": t, "label": label, "sub": sub, "url": url, "kw": label})
    for cid, c in COMPOSITIONS.items():
        idx.append({"t": "조성", "label": c["label"], "sub": c["formula"],
                    "url": f"/composition/{cid}",
                    "kw": f"{cid} {c['family']} {c['cell']} " + " ".join(COMP_ELEMENTS.get(cid, []))})
    have = concept_ids()
    for g in G.GLOSSARY:
        url = f"/concept/{g['id']}" if g["id"] in have else "/glossary"
        idx.append({"t": "용어", "label": g["term"], "sub": g["full"],
                    "url": url, "kw": f"{g['id']} {g['cat']}"})
    for cid in sorted(have):
        idx.append({"t": "개념", "label": cid.upper(), "sub": "상세 개념 문서",
                    "url": f"/concept/{cid}", "kw": cid})
    for p in list_papers():
        idx.append({"t": "논문", "label": p["title"][:70], "sub": p["type"][:40],
                    "url": f"/literature?open={p['id']}", "kw": f"{p['id']} {p['track']}"})
    return idx


# ── Compute: 계산 입력 자동생성 (디지털 트윈 원클릭 스캐폴드) ──
PSEUDO_LIB = {
    "Li": "li_pbe_v1.4.uspp.F.UPF", "P": "P.pbe-n-rrkjus_psl.1.0.0.UPF",
    "S": "s_pbe_v1.4.uspp.F.UPF", "Cl": "cl_pbe_v1.4.uspp.F.UPF",
    "Br": "br_pbe_v1.4.uspp.F.UPF", "I": "i_pbe_v1.4.uspp.F.UPF",
    "O": "O.pbe-n-kjpaw_psl.1.0.0.UPF", "B": "b_pbe_v1.4.uspp.F.UPF",
    "N": "N.pbe-n-radius_5.UPF", "C": "C.pbe-n-kjpaw_psl.1.0.0.UPF",
    "H": "H.pbe-rrkjus_psl.1.0.0.UPF", "Nd": "Nd.GGA-PBE-paw.UPF",
}
# 조성별 canonical 계산 설정 (methods 문서와 정합)
COMPUTE_SETTINGS = {
    "comp1":  {"ecutwfc": 52, "ecutrho": 520, "k": [4, 4, 4], "struct": "comp1_V0_relaxed.cif",  "server": "kgy (RTX3090, QE-GPU)"},
    "comp2":  {"ecutwfc": 52, "ecutrho": 520, "k": [4, 4, 4], "struct": "comp2_V0_v3_candidate.xyz", "server": "gabia (A6000, QE-GPU)"},
    "modelc": {"ecutwfc": 60, "ecutrho": 480, "k": [2, 2, 1], "struct": "modelc_V0_k663.cif",     "server": "kgy (RTX3090, QE-GPU)"},
    "modelc_v3": {"ecutwfc": 60, "ecutrho": 480, "k": [2, 2, 1], "struct": "modelc_v3_62atom_V0.cif", "server": "kgy (RTX3090, QE-GPU)"},
    "modelc_nd_doped": {"ecutwfc": 60, "ecutrho": 480, "k": [6, 6, 1], "struct": "modelc_nd_doped_DFTrelax.cif", "server": "KISTI neuron", "dftu": True},
    "lpsocl": {"ecutwfc": 60, "ecutrho": 480, "k": [2, 2, 1], "struct": "lpsocl_candidates",      "server": "KISTI neuron"},
    "b2o3":   {"ecutwfc": 60, "ecutrho": 480, "k": [1, 1, 1], "struct": "b2o3 128-SC",            "server": "KISTI neuron"},
}
COMPUTE_CALCS = [
    {"id": "scf",     "label": "SCF (총에너지)",       "engine": "QE pw.x"},
    {"id": "gap",     "label": "Band gap (fixed-occ nscf)", "engine": "QE pw.x"},
    {"id": "vcrelax", "label": "EOS / vc-relax (구조·B₀)",  "engine": "QE pw.x"},
    {"id": "md",      "label": "MLIP-MD (UMA, 확산)",   "engine": "UMA + ASE"},
]

def compute_preview(cid: str, calc: str) -> dict:
    comp = COMPOSITIONS.get(cid)
    if not comp:
        return {"error": "unknown composition"}
    st = COMPUTE_SETTINGS.get(cid, {"ecutwfc": 60, "ecutrho": 480, "k": [2, 2, 1],
                                    "struct": f"{cid}.cif", "server": "KISTI neuron"})
    els = COMP_ELEMENTS.get(cid, [])
    kx, ky, kz = st["k"]
    species = "\n".join(f"  {e}  {_mass(e)}  {PSEUDO_LIB.get(e, e + '.UPF')}" for e in els)
    prefix = f"{cid}_{calc}"
    warn = []

    if calc == "md":
        body = _md_template(cid, comp, st)
        runner = _runner_uma(cid, prefix, st)
        note = "UMA-s-1p1(omat) · Langevin NVT dt 2fs · equilib 5ps / prod 200ps · MSD 2–50ps. ⚠ 절대값 인용 금지(멀티시드 판정만)."
        if cid == "li3n":
            warn.append("Li₃N에는 UMA 사용 금지 (2026-06 편향 판정) — 이 조합은 생성하지 않는 게 원칙.")
        return {"cid": cid, "calc": calc, "engine": "UMA + ASE", "server": st["server"],
                "input_name": f"md_{cid}.py", "input": body, "runner_name": f"run_md_{cid}.sh",
                "runner": runner, "note": note, "warn": warn}

    calc_kw = {"scf": "scf", "gap": "nscf", "vcrelax": "vc-relax"}[calc]
    occ = ("  occupations = 'fixed'\n" if calc == "gap" else
           "  occupations = 'smearing'\n  smearing = 'mv'\n  degauss = 0.01\n")
    extra_sys = "  nbnd = <VBM+여유>\n" if calc == "gap" else ""
    cell_block = ("&CELL\n  cell_dofree = 'all'\n/\n" if calc == "vcrelax" else "")
    ions_block = ("&IONS\n  ion_dynamics = 'bfgs'\n/\n" if calc == "vcrelax" else "")
    if calc == "gap":
        note = "정본 gap = 이 nscf의 VBM/CBM 고유값 차. ⚠ DOS-threshold 판독 금지(~0.3 eV 과소). scf 먼저 수렴 후 nscf."
    elif calc == "vcrelax":
        note = "Birch–Murnaghan EOS는 여러 부피 고정셀 relax로. vc-relax는 V₀ 확정용. B₀ ≠ elastic B_VRH."
    else:
        note = "기본 SCF. conv_thr 1e-8, forc_conv 필요시 relax로 전환."
    if st.get("dftu"):
        warn.append("Nd 4f: DFT+U (U_eff≈6 eV) + ISPIN=2 필요 (litdb Nd 교훈) — &SYSTEM에 Hubbard 블록 추가.")

    inp = f"""&CONTROL
  calculation = '{calc_kw}'
  prefix = '{prefix}'
  pseudo_dir = '/scratch/x3430a02/kgy/manuscript_support/pseudo'
  outdir = './out_{prefix}'
  tprnfor = .true.
  tstress = .true.
/
&SYSTEM
  ibrav = 0
  nat = <구조에서>   ntyp = {len(els)}
  ecutwfc = {st['ecutwfc']}
  ecutrho = {st['ecutrho']}
{occ}{extra_sys}/
&ELECTRONS
  conv_thr = 1.0d-8
  mixing_beta = 0.3
/
{ions_block}{cell_block}ATOMIC_SPECIES
{species}

K_POINTS automatic
  {kx} {ky} {kz} 0 0 0

! CELL_PARAMETERS / ATOMIC_POSITIONS ← 구조파일에서 삽입:
!   db/structures/{st['struct']}
"""
    return {"cid": cid, "calc": calc, "engine": "QE pw.x", "server": st["server"],
            "input_name": f"{prefix}.in", "input": inp,
            "runner_name": f"run_{prefix}.sh", "runner": _runner_qe(cid, prefix, st),
            "note": note, "warn": warn}

_MASS = {"Li": 6.94, "P": 30.97, "S": 32.06, "Cl": 35.45, "Br": 79.90, "I": 126.90,
         "O": 16.00, "B": 10.81, "N": 14.01, "C": 12.01, "H": 1.008, "Nd": 144.24}
def _mass(e): return _MASS.get(e, 1.0)

def _runner_qe(cid, prefix, st):
    return f"""#!/bin/bash
# {cid} · {prefix} — {st['server']}
#SBATCH -J {prefix}
#SBATCH -p cas_v100_4     # 서버별 파티션 확인
#SBATCH --time=24:00:00
set -e
pgrep -f "{prefix}.in" && {{ echo "이미 실행중"; exit 1; }}   # 중복실행 가드
export OMP_NUM_THREADS=1
mpirun -np 4 pw.x -in {prefix}.in | tee {prefix}.out
grep -a "JOB DONE" {prefix}.out && echo "완료"
"""

def _runner_uma(cid, prefix, st):
    return f"""#!/bin/bash
# {cid} MLIP-MD — {st['server']} (uma env)
set -e
pgrep -f "md_{cid}.py" && {{ echo "이미 실행중"; exit 1; }}
nvidia-smi | grep -q pw.x && {{ echo "pw.x 실행중 — VRAM 충돌 회피, 대기"; exit 1; }}
conda run -n uma python md_{cid}.py 2>&1 | tee md_{cid}.log
"""

def _md_template(cid, comp, st):
    return f"""# {cid} ({comp['formula']}) — UMA MLIP-MD (Langevin NVT)
from ase.io import read
from ase.md.langevin import Langevin
from ase import units
from fairchem.core import OCPCalculator   # UMA-s-1p1

atoms = read('db/structures/{st['struct']}')
atoms.calc = OCPCalculator(model_name='uma-s-1p1', task='omat')

for T in (600, 800, 1000):            # 아레니우스 3점
    for seed in (1, 2, 3):            # 멀티시드
        dyn = Langevin(atoms, timestep=2*units.fs, temperature_K=T,
                       friction=0.02, rng=__import__('numpy').random.default_rng(seed))
        dyn.run(2500)                 # 5 ps 평형
        # 생산 200 ps + MSD(2–50ps) 저장 …
"""


# ═════════════════════════════════════════════════════════════
# 원소 브리핑 시스템 (Periodic Table → 원소별/조합별 정보 + 우리 db 앵커 + 문헌)
# ═════════════════════════════════════════════════════════════
ELEMENTS_KB = KB / "elements"

def load_element_kb() -> dict:
    out = {}
    if ELEMENTS_KB.exists():
        for f in ELEMENTS_KB.glob("*.json"):
            d = _load_json(f)
            if d and d.get("symbol"):
                out[d["symbol"]] = d
    return out

@lru_cache(maxsize=1)
def _all_icohp_bonds():
    """모든 *_icohp.json 의 bonds → [(system, bond, data)]."""
    out = []
    for f in sorted((DB / "properties").glob("*_icohp.json")):
        d = _load_json(f)
        if d and isinstance(d.get("bonds"), dict):
            sysn = f.stem.replace("_icohp", "")
            for bond, v in d["bonds"].items():
                if isinstance(v, dict):
                    out.append((sysn, bond, v))
    return out

# 원소 → 문헌 매칭 토큰 (slug/title/type 소문자에 substring)
ELEMENT_TOKENS = {
    "Cl": ["chlor", "chloride", "chlorinat", "cl-rich", "cl_rich", "cl_cryst", "cucl", "constricted_esw"],
    "Br": ["brom", "cubr", "lpsclbr", "bromide"],
    "I":  ["iodide", "iodine", "lpsi_", "rao2025_iodide"],
    "O":  ["oxide", "oxygen", "o-doping", "lpsocl", "b2o3", "bzox", "zro2_", "mgf2", "lao_"],
    "S":  ["sulfid", "argyrodite", "ps4", "sulfur", "thio"],
    "P":  ["phosph", "ps4", "argyrodite", "sb_doping"],
    "B":  ["b2o3", "boron", "borate", "bzox"],
    "Nd": ["neodym", "nd2o3", "nd-dop", "nd dop", "lanthan", "rare earth", "rare-earth"],
    "C":  ["carbon", "graphit", "graphene", "vgcf", "conductive_additive", "conductive agent", "conductive_agent"],
    "N":  ["nitrid", "li3n", "hbn", "h-bn", "nitrogen"],
    "H":  ["hydride", "lih ", "moisture", "air stability", "air_stability", "dry_process", "dryprocess"],
    "Li": ["lithium argyrodite", "li-metal", "li metal", "lithiophobic", "cl_rich_anode"],
}

# 기법명 → glossary id (litdb-curator의 '> methods:' 태그 파싱용)
METHOD_MAP = {
    "dft": "dft", "first-principles": "dft", "first principles": "dft", "density functional": "dft",
    "vasp": "dft", "quantum espresso": "dft", "qe": "dft",
    "scf": "scf", "pseudopotential": "pseudo", "paw": "pseudo", "uspp": "pseudo", "ultrasoft": "pseudo",
    "k-point": "kpoint", "kpoint": "kpoint",
    "pbe": "functional", "gga": "functional", "hse": "functional", "scan": "functional", "r2scan": "functional",
    "band gap": "bandgap", "bandgap": "bandgap", "gap": "bandgap",
    "dos": "dos", "density of states": "dos", "pdos": "pdos", "projwfc": "pdos",
    "elf": "elf", "bader": "bader",
    "cohp": "cohp", "icohp": "cohp", "lobster": "cohp", "cobi": "cobi", "icobi": "cobi",
    "eos": "eos", "birch-murnaghan": "eos", "equation of state": "eos",
    "elastic": "elastic", "elastic constants": "elastic",
    "bvse": "bvse", "bond valence": "bvse",
    "md": "md", "aimd": "md", "molecular dynamics": "md", "mlip": "mlip", "uma": "mlip", "sevennet": "mlip",
    "msd": "msd", "arrhenius": "arrhenius", "phonon": "phonon", "phonons": "phonon",
    "neb": "neb", "ci-neb": "neb", "nudged elastic band": "neb",
    "esw": "esw", "grand-potential": "esw", "grand potential": "esw",
    "adhesion": "adhesion",
}
_PSYMS = {s[0] for s in PERIODIC}

@lru_cache(maxsize=1)
def _paper_index():
    """[{id,title,type,track,blob,el_tags,method_tags}]. blob=slug+title+type+본문앞60줄(소문자).
    litdb-curator가 digest 헤더에 '> elements:'/'> methods:' 태그를 넣으면 정밀 링크(토큰스캔은 보조).
    캐시 — 새 digest는 프로세스 리로드(개발서버 auto-reload) 때 갱신."""
    idx = []
    pd = LITDB / "papers"
    for p in list_papers():
        blob = f"{p['id']} {p['title']} {p['type']}"
        el_tags, method_tags = set(), set()
        try:
            head = (pd / f"{p['id']}.md").read_text(errors="ignore").splitlines()[:60]
            blob += " " + " ".join(head)
            for line in head:
                m = re.search(r"(?:elements|원소)\s*[:：]\s*(.+)", line, re.I)
                if m:
                    for t in re.split(r"[,\s/·]+", m.group(1)):
                        t = t.strip("`*_ ")
                        if t in _PSYMS:
                            el_tags.add(t)
                m2 = re.search(r"(?:methods|기법|기술)\s*[:：]\s*(.+)", line, re.I)
                if m2:
                    for t in re.split(r"[,/·]+", m2.group(1).lower()):
                        gid = METHOD_MAP.get(t.strip("`*_ ").strip())
                        if gid:
                            method_tags.add(gid)
        except Exception:
            pass
        idx.append({**p, "blob": blob.lower(), "el_tags": el_tags, "method_tags": method_tags})
    return idx

def element_papers(sym: str, limit: int = 14) -> list:
    """이 원소 관련 litdb 논문 — 태그(정밀) ∪ 토큰스캔(보조). 클릭 → digest."""
    toks = ELEMENT_TOKENS.get(sym, [])
    hits = []
    for p in _paper_index():
        if sym in p["el_tags"] or (toks and any(t in p["blob"] for t in toks)):
            hits.append({"id": p["id"], "title": p["title"], "track": p["track"]})
    return hits[:limit]

# 용어(기법) → 논문 매칭 토큰 (그 기법을 쓴 논문 링크)
GLOSSARY_TOKENS = {
    "dft": ["dft", "first-principles", "first principles", "density functional"],
    "scf": ["self-consistent", "scf convergence"],
    "pseudo": ["pseudopotential", "paw", "ultrasoft", "norm-conserving", "projector augmented"],
    "kpoint": ["k-point", "brillouin", "monkhorst"],
    "functional": ["pbe", "gga", "hse", "r2scan", "scan functional", "hybrid functional", "meta-gga"],
    "bandgap": ["band gap", "bandgap", "vbm", "cbm", "valence band maximum"],
    "dos": ["density of states"],
    "pdos": ["projected density", "pdos", "projwfc", "projected dos"],
    "elf": ["electron localization", "elf"],
    "bader": ["bader"],
    "cohp": ["cohp", "icohp", "crystal orbital hamilton", "lobster"],
    "cobi": ["cobi", "icobi", "bond index", "mayer bond"],
    "lobster": ["lobster"],
    "eos": ["equation of state", "birch-murnaghan", "birch murnaghan", "bulk modulus"],
    "elastic": ["elastic constant", "elastic tensor", "stress-strain", "stress–strain", "voigt", "reuss", "pugh", "young's modulus", "shear modulus"],
    "bvse": ["bvse", "bond valence", "bond-valence"],
    "md": ["molecular dynamics", "aimd", "ab initio molecular", "machine-learned potential"],
    "msd": ["mean squared displacement", "mean-squared displacement", "diffusion coefficient"],
    "arrhenius": ["arrhenius", "activation energy", "ionic conductivity"],
    "phonon": ["phonon", "dynamical matrix", "imaginary frequenc", "vibrational"],
    "neb": ["neb", "nudged elastic", "climbing image", "migration barrier", "transition-state", "transition state"],
    "esw": ["electrochemical stability window", "grand potential", "grand-potential", "stability window"],
    "adhesion": ["work of adhesion", "interfacial energy", "adhesion energy"],
    "mlip": ["mlip", "machine-learned", "foundation model", "sevennet", "uma", "chgnet", "m3gnet", "neural network potential"],
}

def glossary_papers(term_id: str, limit: int = 14) -> list:
    """이 기법(용어)을 쓴 litdb 논문 — 태그(정밀) ∪ 토큰스캔(보조). 클릭 → digest."""
    toks = GLOSSARY_TOKENS.get(term_id, [])
    hits = []
    for p in _paper_index():
        if term_id in p["method_tags"] or (toks and any(t in p["blob"] for t in toks)):
            hits.append({"id": p["id"], "title": p["title"], "track": p["track"]})
    return hits[:limit]

def element_db_anchors(sym: str) -> dict:
    """우리 db에서 이 원소가 나오는 결과 앵커 (실시간 스캔 = 자동 갱신)."""
    comps = [cid for cid, els in COMP_ELEMENTS.items() if sym in els]
    bonds = []
    for system, bond, v in _all_icohp_bonds():
        if sym in re.split(r"[-–]", bond):
            bonds.append({"system": system, "bond": bond,
                          "icohp": v.get("ICOHP_total_eV_per_bond"),
                          "d": v.get("d_mean_A"), "N": v.get("N")})
    pdos = []
    for f in sorted((DB / "properties").glob("*pdos_element*smooth.csv")):
        try:
            hdr = f.open().readline().strip().lower().split(",")
            if any(sym.lower() == h.strip().split()[0] if h.strip() else False for h in hdr) or sym.lower() in [h.strip() for h in hdr]:
                pdos.append(str(f.relative_to(DB)))
        except Exception:
            pass
    xps = []
    for f in sorted((DB / "properties").glob("*xps*.csv")):
        try:
            if re.search(rf"(^|[^A-Za-z]){re.escape(sym)}([^A-Za-z]|$)", f.read_text(errors="ignore")):
                xps.append(str(f.relative_to(DB)))
        except Exception:
            pass
    return {"compositions": comps, "icohp": bonds,
            "pdos": pdos, "xps": sorted(set(xps)), "papers": element_papers(sym)}

def element_briefing(syms: list) -> dict:
    kb = load_element_kb()
    syms = [s for s in syms if s in {p[0] for p in PERIODIC}]
    elems = [{"symbol": s, "kb": kb.get(s), "anchors": element_db_anchors(s)} for s in syms]
    out = {"elements": elems, "multi": None}
    if len(syms) >= 2:
        common = [cid for cid, els in COMP_ELEMENTS.items() if all(s in els for s in syms)]
        sset = set(syms)
        pair = []
        for system, bond, v in _all_icohp_bonds():
            parts = set(re.split(r"[-–]", bond))
            if len(parts) == 2 and parts <= sset:
                pair.append({"system": system, "bond": bond,
                             "icohp": v.get("ICOHP_total_eV_per_bond"), "d": v.get("d_mean_A")})
        papers = {}
        for e in elems:
            for p in e["anchors"]["papers"]:
                papers[p["id"]] = p
        out["multi"] = {"syms": syms, "compositions": common,
                        "bonds": pair, "papers_union": list(papers.values())}
    return out
