"""
data.py — DFT 지식 인프라 데이터 계층 (Flask 라우트가 이걸 호출).

핵심 철학: db/ 를 실시간으로 읽어 "조성 × 물성" 매트릭스를 구성한다.
db 파일이 바뀌면(계산 등록) 사이트가 자동으로 최신값을 반영 = "계속 동기화".
canonical 방법 메타(kb/methodology/computational_methods_canonical.md)와 연동해
각 값에 pseudo/k/cell·비교가능성·stale 배지를 붙일 수 있게 한다.
"""
from __future__ import annotations
import json, csv, re
from pathlib import Path
from functools import lru_cache

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db"
KB = ROOT / "kb"
LITDB = ROOT / "litdb"

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
    {"id": "electronic", "label": "Electronic",  "icon": "⚡", "keys": ["electronic", "dos", "pdos", "bader", "elf"]},
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

def structures_for(cid: str) -> list[dict]:
    pref = _PREFIX.get(cid, [cid])
    sd = DB / "structures"
    out = []
    if sd.exists():
        for f in sorted(sd.iterdir()):
            if f.is_file() and f.suffix.lower() in (".cif", ".xyz", ".vasp", ".vesta", ".cube"):
                if any(f.name.lower().startswith(p.lower()) for p in pref):
                    out.append({"name": f.name, "ext": f.suffix.lstrip("."), "viewable": f.suffix.lower() in (".cif", ".xyz")})
    return out

def datafiles_for(cid: str) -> list[dict]:
    """조성 관련 CSV/데이터 (차트용) — properties 전역에서 prefix 매칭."""
    pref = _PREFIX.get(cid, [cid])
    out = []
    for f in (DB / "properties").rglob("*"):
        if f.is_file() and f.suffix.lower() in (".csv",):
            if any(f.name.lower().startswith(p.lower()) or f"_{p.lower()}" in f.name.lower() for p in pref):
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
    "ICOHP_PS":   {"comp1": -6.0, "comp2": -5.913, "modelc": -6.0, "lpsocl": -6.04},
}
CANONICAL_META = {
    "gap_eV":    "fixed-occ eigenvalue (DOS-threshold 금지)",
    "B0_GPa":    "DFT BM3 EOS",
    "E_VRH_GPa": "DFT relaxed-ion USPP·k444(comp1)/셀별·0.005 — comp1↔comp2만 완전비교",
    "MD_Ea_eV":  "UMA-s-1p1, 600/800/1000K 3-seed (pseudo 무관)",
    "ICOHP_PS":  "LOBSTER all-PAW ext-basis",
}

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


def read_csv(rel: str) -> dict:
    p = (DB / rel).resolve()
    if not str(p).startswith(str(DB.resolve())) or not p.exists():
        return {"error": "not found"}
    rows = list(csv.reader(p.open()))
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
