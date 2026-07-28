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
    return p.read_text(encoding="utf-8", errors="ignore")

# ─────────────────────────────────────────────────────────────
# 로더 (캐시 없음 — 항상 최신 db 반영; 무거우면 mtime 캐시로 교체)
# ─────────────────────────────────────────────────────────────
def _load_json(p: Path):
    """실패 시 None. 단 '파일 없음'과 '깨진 JSON/인코딩'은 구분해 로그를 남긴다
    (예전엔 둘 다 조용히 None → app.py 가 똑같이 404 로 뭉갰다)."""
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        import sys as _s
        print(f"[data] 손상된 파일 무시: {p} — {type(e).__name__}: {e}", file=_s.stderr)
        return None
    except Exception:
        return None

# ── 실시간 동기화용 mtime 시그니처 (캐시 키로 써서 db 변경 즉시 반영) ──
def _mtime_ns(p: Path) -> int:
    try:
        return p.stat().st_mtime_ns
    except Exception:
        return 0

def _dir_sig(path: Path, pattern: str):
    """(파일수, 최신 mtime) — add/modify/delete 모두 값이 바뀌므로 캐시 무효화에 충분."""
    if not path.exists():
        return (0, 0)
    fs = list(path.glob(pattern))
    return (len(fs), max((f.stat().st_mtime_ns for f in fs), default=0))

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
    """db/properties/**.json 전부 (하위폴더 per_bond_json/·bvse_*/ 포함 — rglob)."""
    out = {}
    for f in sorted((DB / "properties").rglob("*.json")):
        d = _load_json(f)
        if d is not None:
            out.setdefault(f.stem, d)  # 스템 충돌 시 최상위 우선
    return out

def load_canonical_methods() -> str:
    p = KB / "methodology" / "computational_methods_canonical.md"
    return p.read_text(encoding="utf-8") if p.exists() else ""


OPEN_ITEMS_MD = KB / "open_items.md"


def load_open_items_md() -> str:
    return OPEN_ITEMS_MD.read_text(encoding="utf-8") if OPEN_ITEMS_MD.exists() else ""


def open_items_summary() -> dict:
    """kb/open_items.md → 대시보드 카드용 요약. mtime 캐시(실시간 동기)."""
    return _open_items_c(_mtime_ns(OPEN_ITEMS_MD))


@lru_cache(maxsize=4)
def _open_items_c(_mt) -> dict:
    txt = load_open_items_md()
    secs, cur = [], None
    for line in txt.splitlines():
        if line.startswith("## "):
            title = line[3:].strip()
            cur = None
            if not title.startswith("✅"):          # 닫힌 항목은 카드에서 제외
                cur = {"title": title, "items": []}
                secs.append(cur)
        elif line.startswith("### ") and cur is not None:
            cur["items"].append(line[4:].strip())
    secs = [s for s in secs if s["items"]]
    return {"sections": secs, "total": sum(len(s["items"]) for s in secs)}

# ─────────────────────────────────────────────────────────────
# 조성 노드 정의 (표시 메타)
# ─────────────────────────────────────────────────────────────
COMPOSITIONS = {
    "comp1":       {"formula": "Li₆PS₅Cl",             "label": "LPSCl",     "family": "argyrodite", "cell": "cubic-52",  "color": "#2563eb"},
    "comp2":       {"formula": "Li₆PS₅Cl₀.₅Br₀.₅",     "label": "LPSClBr",   "family": "argyrodite", "cell": "cubic-52",  "color": "#0d9488"},
    "comp3":       {"formula": "Li₆PS₅Cl₀.₅I₀.₅",      "label": "LPSClI",    "family": "argyrodite", "cell": "rhombo-62", "color": "#7c3aed"},
    "comp4":       {"formula": "Li₆PS₅Br",             "label": "LPSBr",     "family": "argyrodite", "cell": "rhombo-62", "color": "#c05621"},
    "comp5":       {"formula": "Li₆PS₅I",              "label": "LPSI",      "family": "argyrodite", "cell": "rhombo-62", "color": "#be123c"},
    "modelc":      {"formula": "Li₅.₄PS₄.₄Cl₁.₆",      "label": "Cl-rich LPSCl1.6",  "family": "argyrodite", "cell": "rhombo-62", "color": "#0284c7"},
    "modelc_v3":   {"formula": "Li₅.₄PS₄.₄Cl₁.₆ (v3)", "label": "Cl-rich LPSCl1.6 v3","family": "argyrodite","cell": "rhombo-62", "color": "#0369a1"},
    # 표기 규칙: label/formula = 아래첨자(표시용), 키·앵커(#Nd2O3)·db 파일명 = ASCII.
    #   'NdO' 는 화학식마저 틀렸었다(실제 도펀트 Nd₂O₃) — B₂O₃-LPSCl 과 규칙을 맞춘다.
    "modelc_nd_doped": {"formula": "Nd₂O₃-doped LPSCl1.6", "label": "Nd₂O₃-LPSCl", "family": "doped", "cell": "rhombo-62", "color": "#65a30d"},
    "lpsocl":      {"formula": "Li₂₇P₅S₂₁OCl₈",        "label": "O-doped LPSCl (LPSOCl)","family": "doped",     "cell": "rhombo-62", "color": "#be123c"},
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
    {"id": "ionic",      "label": "Ionic",       "icon": "🔋", "keys": ["diffusion", "li_transport", "md_arrhenius", "bvse", "msd", "dualx", "neb", "barrier", "drag", "conductivity"]},
    {"id": "interface",  "label": "Interface",   "icon": "🧩", "keys": ["adhesion", "oxidation", "sei", "interface", "esw", "anode", "binding", "adsorption"]},
    {"id": "structural", "label": "Structural",  "icon": "🧊", "keys": ["phonon", "voronoi", "coordination", "bond_lengths", "eos_dft"]},
    {"id": "cascade",    "label": "Screening·ML",  "icon": "🤖", "keys": ["cascade", "doping", "alpha_sensitivity"]},
]
# 참고: 'literature' 열은 제거함 — 조성별 문헌 유무는 원소 기반이라 항상 True(vanity)였음.
# 문헌은 Literature 페이지 + 원소/용어 논문칩으로 충분히 노출.

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
    "comp5": ["comp5"], "modelc": ["modelc", "modelC", "lpscl16"], "modelc_v3": ["modelc_v3", "modelC_v3"],
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


# 3Dmol.js 에 넘길 파서 이름. .vasp(POSCAR)를 'xyz'로 넘기면 첫 줄이 원자수가 아니라 제목이라
# 조용히 깨진다 — 확장자별로 명시 매핑하고, 파서가 없는 건 다운로드 전용으로.
_VIEWER_FMT = {".cif": "cif", ".xyz": "xyz", ".vasp": "vasp", ".cube": "cube"}


def structures_for(cid: str) -> list[dict]:
    pref = _PREFIX.get(cid, [cid])
    sd = DB / "structures"
    out = []
    if sd.exists():
        for f in sorted(sd.iterdir()):
            if f.is_file() and f.suffix.lower() in (".cif", ".xyz", ".vasp", ".vesta", ".cube"):
                if _prefix_starts(f.name, pref):
                    sfx = f.suffix.lower()
                    out.append({"name": f.name, "ext": f.suffix.lstrip("."),
                                "fmt": _VIEWER_FMT.get(sfx, ""),
                                # 자동로드/기본 선택은 파서가 확실한 cif/xyz 만 (vasp 는 클릭 시 시도)
                                "viewable": sfx in (".cif", ".xyz")})
    return out

# 사이트 차트에서 제외할 폐기 CSV (db엔 traceability로 남기되 사용자에겐 안 보이게).
# ⚠ 하위폴더 이동으로는 못 막는다 — 아래 rglob("*")가 db/properties 를 재귀 탐색하기 때문.
_SUPERSEDED_CSV = {
    # 철회된 단일시드 σ 1.33× 계보 (SEMIFINAL 2026-07-09) — 정본: b2o3_vs_lpscl16_conductivity.csv
    "b2o3_vs_lpscl16_D_decomposition.csv",
    "b2o3_vs_lpscl16_D0_decomposition.csv",
    # 폐기된 5–40 ps 창 (canonical = 2–50). b2o3 Ea 우위를 가짜로 만들었던 표.
    "b2o3_vs_modelc_arrhenius.csv",
    # 단일시드 절대 σ (CLAUDE.md: σ 절대값 인용 금지)
    "md_conductivity_SUPERSEDED_single_seed_2026_06_30.csv",
}


def datafiles_for(cid: str) -> list[dict]:
    """조성 관련 CSV/데이터 (차트용) — properties + spectra 전역에서 prefix 매칭.
    폐기 표(_SUPERSEDED_CSV)는 제외 — db엔 남기되 사이트로는 내보내지 않는다.

    build_coverage 1회당 ~84번 호출되고 매번 db 두 트리를 rglob 하므로 mtime 캐시를 건다.
    ⚠ 캐시 키에 properties **와 spectra 둘 다** 넣어야 한다 — 한쪽만 넣으면 다른 트리에
    CSV를 추가해도 사이트에 안 뜨는, 원래 없던 동기화 버그가 새로 생긴다.
    (_dir_sig 는 (파일수, 최신 mtime)이라 add/modify/delete 를 모두 잡는다 =
     data.py 모듈 독스트링·app.py 의 '요청마다 읽어 db 변경 즉시 반영' 계약 유지.)
    """
    return _datafiles_for_c(cid,
                            _dir_sig(DB / "properties", "**/*"),
                            _dir_sig(DB / "spectra", "**/*"))


@lru_cache(maxsize=64)
def _datafiles_for_c(cid: str, _sig_prop, _sig_spec) -> tuple:
    pref = _PREFIX.get(cid, [cid])
    out, seen = [], set()
    for base in ("properties", "spectra"):
        d = DB / base
        if not d.exists():
            continue
        for f in d.rglob("*"):
            if f.name in _SUPERSEDED_CSV:
                continue
            if f.is_file() and f.suffix.lower() == ".csv" and f.name not in seen:
                # startswith는 최장 prefix 소유규칙 적용, 공유파일은 _infix_ 로 허용
                if _prefix_starts(f.name, pref) or any(f"_{p.lower()}" in f.name.lower() for p in pref):
                    seen.add(f.name)
                    out.append({"name": f.name, "rel": str(f.relative_to(DB)), "kind": _csv_kind(f.name)})
    return tuple(out)

def _csv_kind(name: str) -> str:
    n = name.lower()
    for k, tag in [("pdos", "PDOS"), ("dos", "DOS"), ("arrhenius", "Arrhenius"),
                   ("conductivity", "Conductivity"), ("msd", "MSD"), ("eos", "EOS"),
                   ("phonon", "Phonon"), ("bvse", "BVSE"), ("elf", "ELF"),
                   ("charge", "Charge"), ("bader", "Bader"), ("xps", "XPS"),
                   ("voronoi", "Voronoi"), ("neb", "NEB"), ("barrier", "Barrier"),
                   ("drag", "Drag"), ("diffusion", "Diffusion"), ("binding", "Binding"),
                   ("_ir", "IR")]:  # "_ir"로 "pairs" 오탐 방지
        if k in n:
            return tag
    return "data"

# ─────────────────────────────────────────────────────────────
# 조성별 메트릭 (평탄 인덱스 + canonical 앵커)
# ─────────────────────────────────────────────────────────────
# _index.json 은 2026-06-02 스냅샷이라 eigenvalue gap canonical(2026-06-16) 이전 값을 담고 있다.
# 값을 손으로 고치면 스냅샷이 거짓말을 하게 되므로, 렌더 단계에서 '폐기·canonical 아님' 플래그만 붙인다.
_STALE_PATH = re.compile(r"band_?gap", re.I)


def index_metrics_by_comp(index: dict) -> dict:
    """평탄 인덱스 → 조성별 메트릭. canonical 과 어긋나는 폐기 항목엔 stale 플래그를 실어 보낸다."""
    m = {}
    for dp in index.get("data_points", []):
        cid = dp.get("comp")
        rec = dict(dp)
        if _STALE_PATH.search(str(dp.get("path", ""))):
            canon = CANONICAL.get("gap_eV", {}).get(cid)
            try:
                same = canon is not None and abs(float(dp.get("value")) - canon) < 5e-3
            except (TypeError, ValueError):
                same = False
            if not same:
                rec["stale"] = ("폐기 — canonical 아님. 정본은 fixed-occ nscf 고유값"
                                + (f" {canon} eV" if canon is not None else "")
                                + " (DOS-threshold/legacy k-mesh 판독 금지)")
        m.setdefault(cid, []).append(rec)
    return m

# canonical 앵커값 (kb 나침반과 일치 — 사이트 상단 요약/비교용)
CANONICAL = {
    "gap_eV":     {"comp1": 2.066, "comp2": 2.04, "modelc": 2.099, "lpsocl": 2.2309, "b2o3": 1.9671},
    "B0_GPa":     {"comp1": 26.23, "comp2": 25.8, "modelc": 21.71, "lpsocl": 24.71, "b2o3": 24.48},
    # relaxed-ion USPP. comp2_v3 완료 2026-07-26 (elastic.json) — comp1과 동일 USPP·k444·cubic-52.
    "E_VRH_GPa":  {"comp1": 22.06, "comp2": 20.03, "modelc": 27.66, "lpsocl": 35.04},
    # UMA — ⚠절대값 인용주의. 시드 프로토콜이 조성마다 다르다(아래 CANONICAL_PROVISIONAL 참조):
    #   comp1/modelc = 단일 궤적 deck 앵커 / lpsocl = 4-seed×3-T / comp2 = 3-seed(잠정).
    "MD_Ea_eV":   {"comp1": 0.253, "modelc": 0.224, "lpsocl": 0.287},
    "ICOHP_PS":   {"comp1": -5.938, "comp2": -5.913, "modelc": -6.000, "lpsocl": -6.04,
                   "modelc_nd_doped": -5.976},  # per_bond_json/lobster
}
# 잠정/시드-프로토콜 표시 — (property, comp) : 사유. composition/explorer/compare 에서 '잠정' 배지·툴팁.
CANONICAL_PROVISIONAL = {
    ("gap_eV", "comp2"): "잠정 — legacy band_gaps, fixed-occ nscf 재확인중 (eigenvalue canonical 아님)",
    # ⚠ MD Ea는 조성별로 시드 프로토콜이 달라, 값마다 그 사실을 달고 다녀야 비교 오독을 막는다.
    ("MD_Ea_eV", "comp1"):
        "단일 궤적(온도당 1개, 시드 오차막대 없음) — legacy 단일시드 기준값. modelc(단일시드 0.224)와만 짝지어 비교",
    ("MD_Ea_eV", "modelc"):
        "단일 궤적 legacy 기준값. modelc는 3-seed×3-T 값(0.197±0.032)도 있음 — "
        "b2o3(0.199±0.034)·LPSOCl(0.287±0.024)과 비교할 땐 그쪽을 써야 함(같은 시드 프로토콜끼리만)",
    ("MD_Ea_eV", "comp2"):
        "잠정 — 3-seed지만 800 K 시드 산포가 비물리(s3 800K 2.15e-6 < 자기 600K 2.44e-6). "
        "300 K 외삽 σ비는 0.12–1.48× inconclusive → 확정값 취급 금지 (reseed s5/s6 권고)",
}
# CANONICAL 에 넣기엔 품질 플래그가 붙었지만 db엔 등록된 값 (사이트 표시는 PROVISIONAL 사유와 함께).
CANONICAL_PROVISIONAL_VALUES = {
    ("MD_Ea_eV", "comp2"): 0.275,
}
# (metric, comp) : 사유 — 이 값은 '아직 안 한 것'이 아니라 '하면 안 되거나 정의되지 않는 것'.
# composition/explorer 에서 TODO 가 아니라 'N/A' 로 렌더된다.
CANONICAL_NA = {
    ("MD_Ea_eV", "li3n"):  "UMA MLIP 금지 조성 (2026-06 편향 판정) — DFT-AIMD/QE-NEB 축으로만. TODO 아님",
    ("MD_Ea_eV", "sdcp"):  "분자계(ORCA) — 격자 Li 확산 축이 없음",
    ("MD_Ea_eV", "lic6"):  "interphase 상 — 격자 Li 확산 Arrhenius 축 아님",
    ("gap_eV", "sdcp"):    "분자계 — 주기 밴드갭 대신 HOMO–LUMO 축",
    ("B0_GPa", "sdcp"):    "분자계 — 주기셀 EOS 정의 안 됨",
    ("E_VRH_GPa", "sdcp"): "분자계 — 탄성텐서 정의 안 됨",
    ("B0_GPa", "vgcf_hbn"): "슬랩 — 주기 벌크 EOS 정의 안 됨",
    ("E_VRH_GPa", "vgcf_hbn"): "슬랩 — 벌크 탄성텐서 정의 안 됨",
}
CANONICAL_META = {
    "gap_eV":    "fixed-occ eigenvalue (DOS-threshold 금지) · comp2는 잠정(legacy, 재확인중)",
    "B0_GPa":    "DFT BM3 EOS",
    "E_VRH_GPa": "DFT relaxed-ion USPP·k444(comp1·comp2)/셀별·0.005 — comp1↔comp2만 완전비교쌍",
    "MD_Ea_eV":  "UMA-s-1p1 · 600/800/1000 K 3점 피팅 · ⚠절대값 인용 금지. "
                 "시드 프로토콜 혼재: comp1/modelc=단일 궤적(오차막대 없음), lpsocl=4-seed×3-T, "
                 "comp2=3-seed(잠정) — 조성 간 비교는 같은 프로토콜끼리만",
    "ICOHP_PS":  "LOBSTER all-PAW ext-basis (comp2 = comp2_icohp_origin.csv, 2026-07-25 커밋)",
}

# ─────────────────────────────────────────────────────────────
# Cascade / ML 도핑 스크리닝 (AI 계산 기반) — UMA 상대 스크리닝 번들
# ─────────────────────────────────────────────────────────────
def canonical_values(cid: str) -> dict:
    """조성 하나의 canonical 값 — 잠정값(CANONICAL_PROVISIONAL_VALUES)도 채워 넣는다.
    잠정값은 템플릿에서 CANONICAL_PROVISIONAL 사유와 '잠정' 배지를 달고 렌더된다."""
    out = {k: v.get(cid) for k, v in CANONICAL.items()}
    for (k, c), val in CANONICAL_PROVISIONAL_VALUES.items():
        if c == cid and out.get(k) is None:
            out[k] = val
    return out


def canonical_table() -> dict:
    """explorer/compare 표용 — CANONICAL 전체 + 잠정값 병합."""
    out = {k: dict(v) for k, v in CANONICAL.items()}
    for (k, c), val in CANONICAL_PROVISIONAL_VALUES.items():
        out.setdefault(k, {}).setdefault(c, val)
    return out


CASCADE_FILES = {
    "ranked":      "cascade_v23_ranked.csv",       # 조성 합성점수 리더보드
    "champions":   "cascade_v23_champions.csv",    # 챔피언별 EOS·탄성·anneal
    "litransport": "cascade_v23_litransport.csv",  # Li 수송 프록시
    "synergy":     "cascade_v23_synergy_pairs.csv",# 공동도핑 시너지 가설
    "oxidation":   "oxidation_stability_cascade.csv",  # grand-potential ESW
}
CASCADE_META = {
    "title": "Doping Cascade — AI 계산 기반 도핑 스크리닝 (UMA)",
    "scope": "Model C (Li₅.₄PS₄.₄Cl₁.₆) 기반 산화물/불화물 도펀트 스크리닝, x=0.25",
    "engine": "UMA-s-1p1 (task=omat) · anneal→champion→EOS/elastic/ESW/Li-proxy 캐스케이드",
    "score_formula": "score = 0.30·ox + 0.25·stable + 0.20·soft + 0.15·ductile + 0.10·window (min–max 정규화)",
    "caveat": "절대 탄성값은 실험(AFM/UPE 12–22 GPa) 대비 높게 나옴 — 캐스케이드 내부(UMA-vs-UMA) 순위·상대비교만. EOS B0 ≠ elastic B_VRH.",
    "verified": "doping_cascade_verified.json 은 UMA-내부(EOS·elastic·anneal) 수렴 감사 서브셋 (상위 후보 41종 all-converged, DFT 검증 아님) — DFT 심층검증은 Nd₂O₃·B₂O₃ 2건뿐.",
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
    # 테마별 재구성 (13종 + 도펀트별 norm[theme]∈[0,1]) — 🎯 테마 탭 + 조합 UI 데이터
    out["themes"] = _load_json(DB / "properties" / "cascade_v23_themes.json")
    # co-doping ML v2 (교호작용) — 파일이 아직 없을 수 있음(동시 생성 중) → 존재할 때만 노출 (graceful)
    v2_csv = DB / "properties" / "codoping_ml_v2.csv"
    if v2_csv.exists():
        t = read_csv("properties/codoping_ml_v2.csv")
        out["codoping_v2"] = t if t.get("data") else None
    else:
        out["codoping_v2"] = None
    out["codoping_v2_meta"] = _load_json(DB / "properties" / "codoping_ml_v2_meta.json")
    # 🔻 문헌 표준 게이트 깔때기 (재표현 뷰) — 빌더가 아직 안 돌았을 수 있음 → 없으면 None (탭 숨김)
    out["funnel"] = _load_json(DB / "properties" / "cascade_screening_funnel.json")
    # T9-T11 안정성 3축 — 깔때기 G6/G7 후보. M6 의 vacuous 판정을 뒤집은 데이터.
    out["stability"] = _load_json(DB / "properties" / "cascade_stability_axes_verdict.json")
    return out


# ── 방법 계보 (스크리닝 문헌 → 우리 cascade) ────────────────────────
#  각 항목의 paper 는 litdb/papers/<slug>.md — /api/paper/<slug> 로 뷰어 재사용.
#  ⚠ 정직성: "우리가 이 문헌을 재현했다"가 아니라 "어느 축을 물려받고 어느 축을 바꿨나"를 적는다.
METHOD_LINEAGE = {
    "note": ("문헌 방법의 **계보**이지 성능 비교가 아니다. 우리 cascade 는 이들 중 "
             "**게이트 정의 방식**(Zhu 의 grand-potential 창, Xiao 의 순차 필터 배치)을 물려받았고, "
             "풀 크기·발견 성격은 물려받지 않았다."),
    "chains": [
        {
            "id": "gates",
            "icon": "🧪",
            "title": "게이트 계보 — 조성족 스캔 → grand-potential ESW → 계면 → HT 깔때기",
            "steps": [
                {"paper": "ong2013_lgps_family_substitution", "year": "2013", "who": "Ong",
                 "what": "LGPS 골격 M×X 치환 11 조성 — 조성족 스캔의 원형",
                 "ours": "우리 47종 도펀트 로스터가 정확히 이 체급·이 성격(발견 깔때기 아님)"},
                {"paper": "zhu2015_esw_grand_potential_origin", "year": "2015", "who": "Zhu",
                 "what": "μ_Li(φ) grand-potential 전기화학 창 — ESW 계산의 원전",
                 "ours": "우리 ESW(ox_V·red_V·window_V)의 직계 조상 — 방법 그대로, 좌표계만 host 상대"},
                {"paper": "richards2016_interface_stability_pseudobinary", "year": "2016", "who": "Richards",
                 "what": "pseudo-binary ΔE_rxt 계면 반응성",
                 "ours": "⛔ **우리 게이트에 없음** — 47종 전수 ΔE_rxt 미보유 (추가 1순위)"},
                {"paper": "xiao2019_cathode_coating_screening", "year": "2019", "who": "Xiao",
                 "what": "104,082 → 3종 HT 코팅 깔때기 (F1 gap → F2 hull → F3 ESW → F4 반응성 → F6 NEB)",
                 "ours": "게이트 **순서**를 물려받아 우리 G1–G4 를 배치. 풀 크기·발견 성격은 물려받지 않음"},
            ],
            "end": {"title": "우리 cascade v23 (G1–G5)",
                    "what": "47종 큐레이션 로스터 · UMA 상대 Δe/탄성 + MP grand-potential ESW + BVSE proxy"},
        },
        {
            "id": "ml",
            "icon": "🤖",
            "title": "ML 3세대 — 기술자 설계 → 대규모 분류 → 표형 파운데이션 모델",
            "steps": [
                {"paper": "fujimura2013_ml_conductivity_origin", "year": "2013", "who": "Fujimura",
                 "what": "γ-LISICON 92 조성 · 실험 σ 95점, 손수 설계한 기술자 + SVR",
                 "ours": "특징을 사람이 고른다는 점에서 우리 ridge 특징셋(Δe·ox·window·E·G/B·BVS)과 동세대"},
                {"paper": "sendek2017_ml_screening_12k_conductors", "year": "2017", "who": "Sendek",
                 "what": "12,831 → 21종. 훈련셋 40종 소표본 방어 절차(농축배수·라벨셔플·적용영역)",
                 "ours": "**절차만** 계승 — 농축배수/AD/라벨셔플을 codoping ML v2 에 이식. 수치·특징은 이식 금지"},
                {"paper": "hollmann2025_tabpfn_tabular_foundation_model", "year": "2025", "who": "Hollmann",
                 "what": "표형 데이터 파운데이션 모델 (소표본 in-context 학습)",
                 "ours": "🔜 미적용 — 후보 방향으로만 등록 (co-doping 라벨 자체가 없어 아직 무의미)"},
            ],
            "end": {"title": "우리 co-doping ML v2",
                    "what": "ridge(47 단일도펀트) 계수 이식 + 8개 물리 교호작용 항 — **HYPOTHESIS GENERATOR, 미검증**"},
        },
        {
            "id": "md",
            "icon": "🌡️",
            "title": "MD 통계 규율",
            "steps": [
                {"paper": "kahle2020_ht_aimd_screening", "year": "2020", "who": "Kahle",
                 "what": "15,855 → FPMD 132 → 5종. pinball 대리모델은 랭킹용, 값은 상위 이론으로",
                 "ours": "이 자기검증 원칙이 우리 BVSE proxy(랭킹만)·UMA-MD(절대값 인용 금지) 규율의 근거"},
            ],
            "end": {"title": "우리 MLIP-MD 규율",
                    "what": "MSD 창 2–50 ps 고정 · 600/800/1000 K 아레니우스 · 멀티시드 판정 · σ 절대값 인용 금지"},
        },
    ],
    # 우리가 문헌 대비 추가한 축 / 아직 없는 축 — 과장 방지의 핵심 표
    "axes_added": [
        {"axis": "기계 (E·Pugh G/B)", "why": "Xiao·Sendek 은 축 자체가 없고 Kahle 2020 은 명시 배제(p930).",
         "caveat": "host 앵커가 없어 로스터 median 컷 — 우리 게이트 중 유일하게 자의적."},
        {"axis": "테마 조합 (13 테마 기하평균)", "why": "문헌은 순차 hard gate 만 — 경계값 정보가 소실된다.",
         "caveat": "가중치·테마 정의는 수작업 설계."},
        {"axis": "co-doping 교호작용 ML", "why": "문헌 스크리닝은 전부 단일 조성 단위.",
         "caveat": "라벨이 없어 검증 불가 — 가설 생성기."},
        {"axis": "UMA(MLIP) 전수 릴랙스", "why": "2013–2020 문헌엔 없던 도구 — 273 cascade 실행을 가능케 함.",
         "caveat": "절대값 인용 금지, 상대 순위만."},
    ],
    "axes_missing": [
        {"axis": "양극 반응성 게이트 (ΔE_rxt)", "lit": "Richards 2016 · Xiao F4 (|ΔE_rxt| < 100 meV/atom)",
         "status": "우리 interface_reactivity 는 vs LCO 만 — 47종 전수 없음. 추가 1순위."},
        {"axis": "전자 절연 게이트 (band gap)", "lit": "Xiao F1 (>0.5 eV) · Sendek (≥1 eV)",
         "status": "canonical gap 은 fixed-occ nscf 로 host/챔피언 소수만. 진단으로만 표기, 게이트 미채택."},
        {"axis": "대규모 발견 풀", "lit": "Xiao 104,082 · Sendek 12,831 · Kahle 15,855",
         "status": "우리는 큐레이션 47종. 체급이 다른 물건이며 앞으로도 이 repo 범위 밖."},
    ],
}


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
        "canonical": canonical_table(),      # CANONICAL + 잠정값 병합 (compare 표)
        "canonical_meta": CANONICAL_META,
        "built": idx.get("built"),
        # ⚠ list_papers() 와 같은 정의를 써야 대시보드 카운트와 /literature 목록이 안 어긋난다
        #   (예전엔 _TEMPLATE.md 를 세서 106 vs 105 로 갈렸음).
        "literature_count": (sum(1 for f in (LITDB / "papers").glob("*.md")
                                 if not f.stem.startswith("_"))
                             if (LITDB / "papers").exists() else idx.get("literature_count", 0)),
    }

# ─────────────────────────────────────────────────────────────
# CSV → Plotly 시리즈 (차트 API)
# ─────────────────────────────────────────────────────────────
# 집계형 property JSON — 파일명엔 조성토큰이 없고 내부 results/id/key 에 조성별 값이 있음
AGGREGATES = {
    "electronic": "electronic", "bonds": "bonding", "eos": "mechanical", "elastic": "mechanical",
    "oxidation_stability": "interface", "adhesion": "interface",
    "li_transport": "ionic", "diffusion": "ionic",
}
_AGG_CONTAINER = re.compile(r"(result|system|eigenvalue|band_?gap)", re.I)
_COMP_ALIASES = {
    "comp1": ["comp1"], "comp2": ["comp2"], "comp3": ["comp3"], "comp4": ["comp4"], "comp5": ["comp5"],
    "modelc": ["modelc", "lpscl16"], "modelc_v3": ["modelc_v3"],
    "modelc_nd_doped": ["modelc_nd_doped", "nd_doped", "nd2o3", "nd_pair"],
    "lpsocl": ["lpsocl"], "b2o3": ["b2o3"], "vgcf_hbn": ["vgcf", "hbn", "li3n", "lic6"],
    "li3n": ["li3n"], "lic6": ["lic6"], "sdcp": ["sdcp"],
}

def _agg_ids(fname):
    """집계 JSON의 실제 '레코드 id'만 추출 — 결과 컨테이너(results/eigenvalue_gaps/band_gaps)의
    하위키(값이 dict일 때) + 어디든 'id' 필드. 최상위 prose 제목(comp1_vs_modelc_comparison 등)은 제외."""
    return _agg_ids_c(fname, _mtime_ns(DB / "properties" / f"{fname}.json"))

@lru_cache(maxsize=64)
def _agg_ids_c(fname, _mt):
    d = _load_json(DB / "properties" / f"{fname}.json")
    if not isinstance(d, dict):
        return frozenset()
    ids = set()
    def walk(x, pk):
        if isinstance(x, dict):
            vals = list(x.values())
            # '레코드 컨테이너'(키명이 result/eigenvalue/…, 값이 전부 dict)면 하위키=id
            if _AGG_CONTAINER.search(pk or "") and vals and all(isinstance(v, dict) for v in vals):
                ids.update(str(k).lower() for k in x.keys())
            for k, v in x.items():
                if k == "id" and isinstance(v, str):
                    ids.add(v.lower())
                walk(v, k)
        elif isinstance(x, list):
            for it in x:
                walk(it, pk)
    walk(d, "")
    return frozenset(ids)

_ALL_ALIASES = sorted({a.lower() for v in _COMP_ALIASES.values() for a in v}, key=len, reverse=True)


def _alias_hits(rec_id: str, alias: str) -> bool:
    """레코드 id 가 이 별칭 소유인가.

    substring 매칭('modelc' in 'modelc_v3')은 최장-prefix 소유규칙을 우회해서
    modelc 페이지가 modelc_v3 레코드만으로 커버리지 True 가 됐다. 그렇다고
    startswith(alias+'_') 로 좁히면 nd_pair01_nd2o3_doped 같은 실제 id 를 놓쳐
    modelc_nd_doped/ionic 이 ✓→✗ 로 회귀한다. 그래서 세 가지만 허용한다:
      (1) 정확 일치  (2) alias 뒤가 숫자거나 비-영숫자인 접두  (3) 언더스코어로 끊긴 infix
    그 위에 _ALL_ALIASES 최장 양보를 얹어 더 구체적인 별칭이 있으면 넘겨준다.
    """
    if rec_id == alias:
        return True
    ok = False
    if rec_id.startswith(alias):
        nxt = rec_id[len(alias):len(alias) + 1]
        ok = (not nxt) or nxt.isdigit() or not nxt.isalnum()
    if not ok and f"_{alias}" in rec_id:
        j = rec_id.index(f"_{alias}") + 1 + len(alias)
        nxt = rec_id[j:j + 1]
        ok = (not nxt) or nxt.isdigit() or not nxt.isalnum()
    if not ok:
        return False
    # 더 긴(구체적) 별칭이 같은 id 를 접두로 소유하면 양보 — modelc ↛ modelc_v3
    return not any(len(q) > len(alias) and rec_id.startswith(q) for q in _ALL_ALIASES)


def _aggregate_covers(cid, cat_id):
    aliases = _COMP_ALIASES.get(cid, [cid])
    for fname, fcat in AGGREGATES.items():
        if fcat == cat_id:
            ids = _agg_ids(fname)
            if any(_alias_hits(i, a) for i in ids for a in aliases):
                return True
    return False

# (_lit_covers 삭제 — 'literature' 커버리지 열이 제거되면서 남은 죽은 코드였고,
#  무효화 키 없는 lru_cache 라 되살리면 litdb 갱신이 반영 안 되는 버그가 됐을 것.
#  문헌 파생 계산은 list_papers() 한 군데로 통일한다.)


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
    # (c) 구조파일 존재 → structural 만 (electronic은 실제 dos/pdos/gap 데이터가 있어야 True)
    if cat_id == "structural" and structures_for(cid):
        return True
    dfs = datafiles_for(cid)          # ⚠ 두 번 호출하면 db 전체 rglob 이 두 배가 된다
    if dfs:
        # 어떤 CSV가 이 카테고리에 속하면
        for df in dfs:
            kind = df["kind"].lower()
            if cat and any(k in kind for k in cat["keys"]):
                return True
    # (d) 캐스케이드 히트 조성(Nd2O3/B2O3 …) = 스크리닝 심층검증 대상
    if cat_id == "cascade" and cid in CASCADE_DOPANT:
        return True
    # (e) 집계형 JSON 의 실제 레코드에 조성별 값 (electronic/bonds/eos/elastic/oxidation/li_transport/diffusion)
    if _aggregate_covers(cid, cat_id):
        return True
    return False

def build_coverage(props, prop_cat, idx_metrics) -> dict:
    """{comp: {category_id: bool}} — True=데이터有, False=TODO(옅은색)."""
    cov = {}
    for cid in COMPOSITIONS:
        cov[cid] = {c["id"]: _has_category_data(cid, c["id"], props, prop_cat, idx_metrics)
                    for c in CATEGORIES}
    return cov

# 물성이 그 조성에 애초에 성립하지 않는 칸 = N/A (미계산 TODO 와 구분).
# 1순위 이유는 진척률 정확도가 아니라 **금지된 계산을 TODO 로 광고하지 않기**다
# (예: li3n × ionic — CLAUDE.md 상 UMA 는 Li₃N 에 사용 금지).
NOT_APPLICABLE = {
    ("sdcp", "mechanical"): "분자계(ORCA) — 주기셀 EOS·탄성 정의 안 됨",
    ("sdcp", "ionic"):      "분자계 — 격자 Li 수송 축이 없음",
    ("sdcp", "cascade"):    "도핑 스크리닝 대상 아님 (호스트가 argyrodite 아님)",
    ("sdcp", "electronic"): "분자 MO 축 — 주기 밴드/PDOS 정의 안 됨",
    # ⚠ li3n/lic6 의 ionic 은 N/A 가 아니다 — NEB barrier 등 실제 데이터가 있다.
    #    '금지된 계산'은 카테고리가 아니라 특정 metric(MD_Ea_eV) 축이라 CANONICAL_NA 로 처리한다.
    ("li3n", "cascade"):    "interphase 상 — 도펀트 스크리닝 로스터 밖",
    ("li3n", "mechanical"): "interphase 상 — 벌크 EOS 비교축 아님",
    ("lic6", "cascade"):    "interphase 상 — 도펀트 스크리닝 로스터 밖",
    ("lic6", "mechanical"): "interphase 상 — 벌크 EOS 비교축 아님",
    ("vgcf_hbn", "cascade"): "anode 슬랩 — 도펀트 스크리닝 로스터 밖",
    ("vgcf_hbn", "mechanical"): "슬랩 — 주기 벌크 EOS 정의 안 됨",
}
for _c in COMPOSITIONS:
    if _c not in ("modelc_nd_doped", "b2o3"):
        NOT_APPLICABLE.setdefault((_c, "cascade"), "DFT 심층검증 대상 도핑 히트가 아님")


def coverage_stats(cov: dict) -> dict:
    """진척률은 '해당되는 칸' 기준. N/A 는 분모에서 뺀다."""
    total = done = na = 0
    for cid, row in cov.items():
        for k, ok in row.items():
            if (cid, k) in NOT_APPLICABLE:
                na += 1
                continue
            total += 1
            done += 1 if ok else 0
    return {"done": done, "total": total, "na": na,
            "pct": round(100 * done / total) if total else 0}


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


def external_benchmarks() -> dict:
    """db/properties/external_benchmarks_symposium_2026.json → 재현 표적 + 덱 정정 원장.

    ⚠ 이 파일의 수치는 **외부 소환값**이다 — 우리 db 절대값과 같은 표에 넣지 않는다.
    페이지에서도 그 경고를 최상단에 띄운다(honesty_header).
    """
    return _load_json(DB / "properties" / "external_benchmarks_symposium_2026.json")


def deck_correction_ledger() -> list:
    """발표 덱 값이 논문 실물과 어긋난 사례를 모아 한 표로.

    '덱을 정본으로 쓰지 않는다'는 규율이 **추상적 원칙이 아니라 실측된 오류율**임을
    보이는 것이 목적이다. 근거는 각 digest 안에 이미 있고, 여기서는 모으기만 한다.
    """
    return [
        {"case": 1, "deck": "코팅 스크리닝 입구 풀 = 17,233 **Li·P·S·O**",
         "actual": "17,230 **Li·O**",
         "what": "개수(3 차이)와 **원소집합** 둘 다 오기",
         "paper": "kim2026_hts_li3sc2po43_coating_midni_ncm",
         "impact": "우리 cascade 대조군의 체급·화학 범위를 잘못 잡을 뻔"},
        {"case": 2, "deck": "Li|LPSCl 계면 D = 0.4e-6 / 1.1e-6 cm²/s",
         "actual": "0.4e-7 / 1.1e-7 cm²/s",
         "what": "**자릿수 10배 오기** (두 값 모두)",
         "paper": "kim2026_li_argyrodite_sei_reactive_md",
         "impact": "**우리 db 에 이미 들어가 있던 값** — 정정 완료"},
        {"case": 3, "deck": "계면 MD 실험 대조 = TEM, 25 °C vs 80 °C",
         "actual": "본문은 '~12 nm Li₂S interphase, cryo-TEM' 한 문장뿐",
         "what": "**'25 vs 80 °C' 는 논문 어디에도 없음** → 판독 불가로 격하",
         "paper": "kim2026_li_argyrodite_sei_reactive_md",
         "impact": "서지(ACS Energy Lett. 2022, 7, 3064)는 정확했으나 조건이 창작됨"},
        {"case": 5, "deck": "Li₂SiS₃ σ = 1e-4 (corner) → **2.4 mS/cm** (edge) = **4자릿수 상승**",
         "actual": "**논문에 σ 가 아예 없다.** 어떤 조성·어떤 상에도 보고 안 함. "
                   "본문이 말하는 건 'D_600K 가 최소 **2자릿수** 높다' 뿐이고, "
                   "'3자릿수'는 자기 측정이 아니라 Huang JACS 2022(Kanno) **소환값**",
         "what": "🔴 **존재하지 않는 수치** — 2도 3도 아닌 '4자릿수'는 어디서도 안 나온다. "
                 "SI 의 Arrhenius·NE 식은 결과에 한 번도 안 쓰인 보일러플레이트(단일 온도 600 K라 "
                 "Arrhenius 자체가 불가능)",
         "paper": "kim2025_csp_metastable_edge_sharing_sse",
         "impact": "**우리 db 에 등록돼 있던 값 3개를 철회.** 등급이 다른 오류 — 앞의 1~4는 "
                   "'틀린 값'이고 이건 '없는 값'이다"},
        {"case": 6, "deck": "준안정 고전도 3 기술자 = dead volume / distance of cation / Li–S₄ distortion",
         "actual": "논문 결론부 + SI eq 9–11 은 **packing ratio α / Li–S₄ 부격자 부피 / CSM**",
         "what": "**세 개 중 두 개가 다르다.** 덱의 ①②는 기술자가 아니라 **기구**이고, "
                 "`d_c > d_e` 는 정의식도 수치표도 없는 기하 논증",
         "paper": "kim2025_csp_metastable_edge_sharing_sse",
         "impact": "덱 목록을 그대로 썼으면 **논문에 없는 기술자 2개를 만들어내 47종에 계산할 뻔**"},
        {"case": 4, "deck": "Li₃YCl₆ 논문 = MTP · CSP(USPEX + GA + active learning)",
         "actual": "**CALYPSO + PSO + 직접 DFT** (50세대 × 100개체). MTP·USPEX·GA 한 글자도 없음",
         "what": "**방법 계열 자체가 다름**",
         "paper": "kim2025_li3ycl6_new_crystal_structure",
         "impact": "랩이 CSP 파이프라인을 최소 2개 운영 — '그들은 CSP 에도 MTP 를 쓴다'를 전제로 삼으면 안 됨"},
    ]


def verdict_revisions() -> list:
    """**우리가 냈다가 뒤집은 판정** 이력.

    덱 정정 원장이 '외부 자료가 틀렸다'면 이건 '우리가 틀렸다'다. 둘을 나란히 두는 것이
    핵심이다 — 한쪽만 있으면 정직성이 아니라 남 탓이 된다.
    각 항목은 (무엇을 주장했나 / 무엇이 틀렸나 / 어떻게 알았나 / 지금 무엇을 아나)로 쓴다.
    """
    return [
        {
            "id": "V1",
            "date": "2026-07-28",
            "title": "M6 계면 반응성 게이트를 'vacuous'라고 판정했다가 철회",
            "claimed": (
                "47 코팅 × 양극(만충 LiCoO₂ / 반충 Li₀.₅CoO₂) 94쌍을 돌려 **89/94가 통과**하고, "
                "탈락 5종(BaO·MnO·Na₂O·Sb₂O₅·TiF₄)이 전부 이미 G1–G4에서 죽어 있어 "
                "**unique_kill = 0 → 완전 중복 게이트**라고 판정했다. "
                "'황화물 SE ↔ 산화물 양극은 큰 구동력이지만 산화물 코팅 ↔ 산화물 양극은 거의 0이라 "
                "47종 안에서 줄 세우는 데는 못 쓴다'고 썼다."),
            "wrong": (
                "**게이트의 성질이 아니라 우리가 가장 쉬운 상대만 계산한 결과였다.** "
                "코팅이 실제로 마주하는 상대는 양극만이 아니다 — SE(LPSCl)와 Li 금속 음극이 있고, "
                "그쪽이 훨씬 가혹하다."),
            "how_found": (
                "Kim 2026 (Nano Convergence 13, 27) **Table S1** — 88 후보의 ΔE_rxn을 "
                "NCM523과 LPSCl **양쪽**에 대해 싣는데, 다수가 양극과는 0인데 LPSCl과는 −50~−99 meV였다 "
                "(Li₂TiO₃ 0/−60 · Li₃NbO₄ 0/−96 · Li₂SO₄ 0/−99 · LiSrBO₃ 0/−96). "
                "본문도 *\"many materials exhibited stable interfaces with the NCM523, "
                "a substantial fraction fail to maintain stability against LPSC\"*라고 명시한다."),
            "now_known": (
                "축을 5상대로 확장해 47종을 다시 돌린 결과 **위력이 축마다 극단적으로 다르다**: "
                "양극 만충 2종 탈락 · 양극 반충 3종 · **SE(LPSCl) 29종** · **Li 음극 35종** · LNO 대조 4종. "
                "코어 생존자 11종이 **3종(CaF₂·LiF·MgO)으로 줄었다** — SE·Li 축이 8종을 새로 죽인다. "
                "즉 이 게이트는 vacuous의 반대이고, 그것을 우리 데이터로 확정했다."),
            "table": {
                "cols": ["축", "통과", "탈락", "중앙값 (meV/atom)"],
                "rows": [["양극 만충 (LiCoO₂)", "45/47", "2", "−0.0"],
                         ["양극 반충 (Li₀.₅CoO₂)", "44/47", "3", "0.0"],
                         ["**SE (Li₆PS₅Cl)**", "**18/47**", "**29**", "**−163.4**"],
                         ["**Li 금속 음극**", "**12/47**", "**35**", "**−447.1**"],
                         ["LiNbO₃ (상용 코팅 대조)", "43/47", "4", "−13.7"]]},
            "caveat": (
                "⚠ **Li 음극 축의 적용 조건**: 도펀트가 SE 벌크에 분산돼 Li 금속과 접촉하는 구성에서만 "
                "유효하다. 양극 표면에만 있는 코팅이면 Li와 만나지 않으므로 과도하게 엄격하다. "
                "우리 cascade는 'LPSCl 도펀트' 구도라 성립하지만 인용 시 전제를 밝힐 것. "
                "⚠ 생존 3종이라는 **숫자 자체도 결론으로 쓰지 말 것** — 100 meV 컷 하나에 지배된다."),
            "lesson": "**축을 하나만 계산하고 '게이트가 무력하다'고 말하지 말 것.** "
                      "무력해 보이면 먼저 '내가 쉬운 쪽만 봤나'를 의심한다.",
            "papers": ["kim2026_hts_li3sc2po43_coating_midni_ncm"],
            "artifacts": ["db/properties/cascade_stability_axes_verdict.json",
                          "db/properties/cascade_stability_axes.csv"],
        },
        {
            "id": "V2",
            "date": "2026-07-28",
            "title": "T10(E_hull 합성가능성 필터)이 G1의 vacuous를 고칠 거라 예측했다가 빗나감",
            "claimed": (
                "깔때기의 G1(구조 안정)이 unique_kill 0으로 아무도 못 떨어뜨리는 이유를 "
                "**'우리 G1이 convex hull이 아니라 host 상대 Δe를 쓰기 때문'**이라고 진단하고, "
                "Lee 2024(JMCA 12, 7272)의 `E_hull < 50 meV/atom` 합성가능성 기술자를 도입하면 "
                "실제로 걸러질 거라고 예측했다 (T10, 우선순위 1)."),
            "wrong": "**hull로 바꿔도 탈락이 0종이다.** 최대가 CrO₃ 46 meV이고 나머지는 사실상 0.",
            "how_found": "T9·T11과 함께 47종 전수 계산(`tools/cascade/stability_axes.py`)을 돌려 직접 확인.",
            "now_known": (
                "**원인은 기준이 아니라 풀이다.** 우리 47종은 애초에 안정한 흔한 이성분 산화물·불화물로 "
                "큐레이션돼 있어 **어떤 열역학 안정성 기준을 걸어도 통과한다**. "
                "→ **T10은 접는다.** 대신 이 음성 결과 자체를 `cascade_screening_funnel.json`의 "
                "`pool_provenance` 논증에 **정량 근거**로 전환한다: "
                "'우리 풀에서 안정성 축이 무력한 것은 게이트 설계 문제가 아니라 큐레이션의 성질이다.'"),
            "caveat": "⚠ 이건 '안정성이 중요하지 않다'는 뜻이 **아니다**. "
                      "Xiao(104,082)·Sendek(12,831)·Kahle(15,855) 같은 **발견 깔때기**에서는 "
                      "안정성이 압도적으로 센 게이트다(Kim 2026도 ECW에서 94.3% 제거). "
                      "우리 풀은 그 단계를 **이미 통과한 상태에서 시작**할 뿐이다.",
            "lesson": "**음성 결과도 결과다.** 예측이 빗나간 것을 지우지 않고 논증으로 전환한다.",
            "papers": ["lee2024_multicomponent_argyrodite_mixed_oxidation_mtp"],
            "artifacts": ["db/properties/cascade_stability_axes_verdict.json"],
        },
        {
            "id": "V3",
            "date": "2026-07-28",
            "title": "'MLIP σ 절대값 인용 금지'의 근거를 재정의 (규율은 유지, 이유가 바뀜)",
            "claimed": (
                "규율의 근거를 `kim2024` 하나로 세웠다 — **같은 MTP 프레임에서 훈련 functional만 바꿔도 "
                "σ₈₀%가 8배 갈린다**(PBE 4.19 / PBE-D3 0.55 / optB88 2.46 mS/cm). "
                "'경쟁 그룹의 데이터가 우리 규율을 증명한다'고 썼다."),
            "wrong": (
                "**절반만 맞았다.** `lee2024` ESI Table S1이 반대 방향의 데이터를 준다 — "
                "optB88로 학습한 MTP는 **8개 계에서 실험과 잘 맞고**, 크게 틀리는 쪽은 **AIMD**다."),
            "how_found": "lee2024 (JMCA 12, 7272) ESI Table S1 실물 대조.",
            "table": {
                "cols": ["조성", "AIMD", "MTP_optB88", "실험", "AIMD 오차"],
                "rows": [["Li₆PS₅I", "0.84", "**0.001**", "**0.001**", "**840×**"],
                         ["Li₆PS₅Cl", "4.6", "**2.46**", "**2.3–2.5**", "1.9×"],
                         ["Li₃YCl₆", "14", "**0.56**", "**0.51**", "**27×**"],
                         ["Li₇P₃S₁₁", "57", "6.5", "4–17", "~5×"]]},
            "now_known": (
                "정확한 명제는 이것이다 — **\"MLIP σ 절대값은 (a) 훈련 functional이 그 계에 맞고 "
                "(b) 같은 물질군에서 실험 검증을 거친 경우에만 신뢰할 수 있다.\"** "
                "**우리 UMA는 둘 다 미충족**이다: OMat24는 PBE 계열이라 optB88이 아니고, "
                "우리 계에 대한 실험 대조 검증을 한 적이 없다. "
                "→ **인용 금지 규율은 그대로 유지된다. 다만 이유가 '멀립은 원래 못 믿는다'가 아니라 "
                "'우리 특정 설정이 검증되지 않았다'로 바뀐다.**"),
            "caveat": "⚠ 이 재정의는 규율을 **약화시키지 않는다. 정확하게 만든다.** "
                      "그리고 T1(UMA 외삽·검증 대리지표)의 필요성을 한층 강하게 만든다 — "
                      "'검증이 없다'가 문제라면 검증을 만들면 되기 때문이다.",
            "lesson": "**우리에게 유리한 문헌만 근거로 삼지 말 것.** "
                      "같은 랩의 다른 논문이 반대 방향을 가리키면 명제를 다시 써야 한다.",
            "papers": ["kim2024_mtp_argyrodite_disorder_gb",
                       "lee2024_multicomponent_argyrodite_mixed_oxidation_mtp"],
            "artifacts": ["kb/open_items.md"],
        },
        {
            "id": "V4",
            "date": "2026-07-28",
            "title": "T1(외삽 등급)을 'γ 확보'로 세웠다가 'UMA용 대리지표 설계'로 재정의",
            "claimed": (
                "이상욱 랩이 MTP-MD 스냅샷마다 관리하는 **extrapolation grade γ**를 우리도 확보하면 "
                "T1(우리 최대 방법론 구멍)이 닫힌다고 봤다. 논문에서 실제 값도 찾았다 — "
                "γ_select = 2, γ_break = 10 → 5 → 2."),
            "wrong": (
                "**γ는 UMA에 이식할 수 없다.** γ는 MTP의 **선형 기저 위 maxvol / D-optimality**로 "
                "정의되는데, UMA는 비선형 등변 GNN이라 **정의 자체가 존재하지 않는다**. "
                "숫자를 구해도 쓸 데가 없다."),
            "how_found": "kim2026 SEI 논문(SSRN) 실물에서 γ 정의를 확인.",
            "now_known": (
                "이식할 수 있는 것은 **논리 구조**뿐이다 — ①대리지표를 하나 정한다 "
                "②**선별 문턱과 중단 문턱을 분리**한다 ③중단 문턱을 조여 수렴을 판정한다. "
                "채택한 대리지표는 **모델 위원회 불일치**(UMA + MACE-MP-0 + SevenNet-0의 힘 예측 분산). "
                "기존 궤적 후처리라 새 MD가 필요 없다."),
            "caveat": (
                "⚠ 위원회는 **절대 정확도를 말하지 않는다.** 세 모델이 전부 PBE 계열이라 "
                "V3의 functional 각인 문제를 풀지 못한다 — **일치해도 절대 σ 인용 금지는 그대로**. "
                "이 지표가 재는 것은 '이 배열이 훈련 분포에서 이상한가'뿐이고, "
                "**그 목적에는 같은 functional 계열인 것이 오히려 무해하다**."),
            "lesson": "**남의 지표를 그대로 가져오기 전에 그것이 우리 도구에서 정의되는지 먼저 확인할 것.**",
            "papers": ["kim2026_li_argyrodite_sei_reactive_md"],
            "artifacts": ["tools/ionic/mlip_committee.py", "kb/open_items.md"],
        },
    ]


def list_talks() -> list:
    """litdb/talks/*.md → [{id, title, speaker, session, digested}].

    발표 덱은 peer-review를 거치지 않아 papers/ 와 **분리 보관**한다
    (litdb/talks/README.md 의 인용 규율). 목록도 따로 낸다 — 논문 수에 합산하면
    소환값 등급이 섞인다.
    """
    out = []
    td = LITDB / "talks"
    if not td.exists():
        return out
    for f in sorted(td.glob("*.md")):
        if f.stem.startswith("_") or f.stem.upper() == "README":
            continue
        title, speaker, session, digested = f.stem.replace("_", " "), "", "", ""
        got_title = False
        try:
            head = f.read_text(encoding="utf-8", errors="ignore").splitlines()[:14]
        except Exception:
            head = []
        for line in head:
            if not got_title and line.startswith("#"):
                raw = line.lstrip("# ").strip()
                # "제목 — 발표자 (소속)" 형태에서 뒤쪽을 발표자로 분리
                if "—" in raw:
                    title, _, speaker = (s.strip() for s in raw.partition("—"))
                else:
                    title = raw
                got_title = True
            m = re.search(r"발표 (\d{4}-\d{2}-\d{2}) \(([^)]+)\)", line)
            if m and not session:
                session, digested = m.group(2), digested or ""
            md = re.search(r"digested `?(\d{4}-\d{2}-\d{2})`?", line)
            if md and not digested:
                digested = md.group(1)
        out.append({"id": f.stem, "title": title, "speaker": speaker,
                    "session": session, "digested": digested})
    return out


def list_papers() -> list:
    """litdb/papers/*.md → [{id, title, type, track}] (DEM/DFT 분류 포함)."""
    out = []
    pd = LITDB / "papers"
    if not pd.exists():
        return out
    for f in sorted(pd.glob("*.md")):
        if f.stem.startswith("_"):
            continue
        title, type_str, digested = f.stem.replace("_", " "), "", ""
        got_title = False
        try:
            head = f.read_text(encoding="utf-8", errors="ignore").splitlines()[:18]
        except Exception:
            head = []
        for line in head:
            if not got_title and line.startswith("#"):
                title = line.lstrip("# ").strip()
                got_title = True
            m = re.search(r"type `([^`]+)`", line)
            if m and not type_str:
                type_str = m.group(1)
            md = re.search(r"digest(?:ed)?\s*`?(\d{4}-\d{2}-\d{2})`?", line, re.I)
            if md and not digested:
                digested = md.group(1)
        out.append({"id": f.stem, "title": title, "type": type_str,
                    "track": literature_track(f.stem, type_str, title),
                    "digested": digested})
    return out


def _is_blank(r):
    return (not r) or (not any((c or "").strip() for c in r))


# 데이터 행이 아니라 '요약/파생' 행 (ratio_…, => sigma_ratio 등). 차트 데이터에서 빼고 각주로 보낸다.
# 이걸 안 빼면 요약행의 문자열 셀('1.08+/-0.18')이 열 타입 판정을 오염시켜 진짜 값 열이
# categorical 로 떨어진다(= σ·Ea 열이 차트에서 통째로 사라지는 원인).
_SUMMARY_ROW = re.compile(r"^\s*(=>|ratio[_/]|delta[_ ]|Δ|d?Ea\s*=)", re.I)

def read_csv(rel: str) -> dict:
    p = (DB / rel).resolve()
    if not p.is_relative_to(DB.resolve()) or not p.exists():
        return {"error": "not found"}
    rows = list(csv.reader(p.open(encoding="utf-8")))
    # 헤더 = 선행 주석(#)·빈 줄을 건너뛴 첫 실질 행
    i = 0
    while i < len(rows) and (_is_blank(rows[i]) or rows[i][0].lstrip().startswith("#")):
        i += 1
    if i >= len(rows):
        return {"columns": [], "data": []}
    header = rows[i]
    data, summary = [], []
    for r in rows[i + 1:]:
        if _is_blank(r):
            break                    # 첫 빈 줄에서 멈춤 — 한 파일 속 두번째 표 누수 방지
        if r[0].lstrip().startswith("#"):
            continue
        if r == header:
            break                    # 두번째 헤더 = 다른 표 시작
        rec = {}
        for j, h in enumerate(header):
            v = r[j] if j < len(r) else ""
            try:
                rec[h] = float(v)
            except (ValueError, TypeError):
                rec[h] = v
        (summary if _SUMMARY_ROW.match(str(r[0])) else data).append(rec)
    return {"columns": header, "data": data, "n": len(data), "summary": summary}


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
        ("페이지", "Screening·ML", "AI 계산 도핑 스크리닝 (cascade)", "/cascade"),
        ("페이지", "Compute", "원클릭 계산 입력 생성", "/compute"),
        ("페이지", "Methods", "계산 방법 canonical", "/methods"),
        ("페이지", "Literature", "DEM/DFT 문헌", "/literature"),
        ("페이지", "Glossary", "용어 설명집", "/glossary"),
        ("페이지", "Work Log", "작업 기록", "/log"),
    ]
    for t, label, sub, url in pages:
        idx.append({"t": t, "label": label, "sub": sub, "url": url, "kw": label})
    for cid, c in COMPOSITIONS.items():
        # 아래첨자 표기와 ASCII 표기를 둘 다 kw 에 (Nd₂O₃ ↔ Nd2O3, B₂O₃ ↔ B2O3 …)
        _sub = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
        _ascii = f"{c['label']} {c['formula']}".translate(_sub)
        idx.append({"t": "조성", "label": c["label"], "sub": c["formula"],
                    "url": f"/composition/{cid}",
                    "kw": f"{cid} {c['family']} {c['cell']} {_ascii} "
                          f"{CASCADE_DOPANT.get(cid, '')} " + " ".join(COMP_ELEMENTS.get(cid, []))})
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


# ── Compute: 계산 입력 자동생성 (AI 계산 원클릭 스캐폴드) ──
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
    if calc not in ("scf", "gap", "vcrelax", "md"):
        return {"error": f"unknown calc '{calc}'"}
    st = COMPUTE_SETTINGS.get(cid, {"ecutwfc": 60, "ecutrho": 480, "k": [2, 2, 1],
                                    "struct": f"{cid}.cif", "server": "KISTI neuron"})
    els = COMP_ELEMENTS.get(cid, [])
    kx, ky, kz = st["k"]
    species = "\n".join(f"  {e}  {_mass(e)}  {PSEUDO_LIB.get(e, e + '.UPF')}" for e in els)
    prefix = f"{cid}_{calc}"
    warn = []
    _none = {"input_name": None, "input": None, "runner_name": None, "runner": None}

    # 분자계(SDCP) = ORCA r²SCAN-3c. 평면파 QE/k-point 부적합 → 스크립트 생성 안 함.
    if comp.get("family") == "molecular" or cid == "sdcp":
        return dict(_none, cid=cid, calc=calc, engine="ORCA r²SCAN-3c", server="desktop WSL (ORCA)",
                    note="SDCP는 분자계라 ORCA r²SCAN-3c(SDCP 분자 계열)로 계산해. 평면파 QE·k-point 입력은 부적합해서 만들지 않아 — desktop WSL에서 ORCA 입력을 써.",
                    warn=["평면파 QE는 분자에 안 맞음 (진공 셀·k-point 무의미)."])
    # Li₃N + UMA-MD = 금지 조합 → 경고만, 스크립트 생성 안 함.
    if calc == "md" and cid == "li3n":
        return dict(_none, cid=cid, calc=calc, engine="—", server=st["server"],
                    note="Li₃N에는 UMA MLIP 금지 (2026-06 결정론적 편향 판정). 이 조합은 스크립트를 생성하지 않아.",
                    warn=["Li₃N 확산은 UMA 대신 DFT-AIMD / QE-NEB 로. (CLAUDE.md 규율)"])

    if calc == "md":
        body = _md_template(cid, comp, st)
        runner = _runner_uma(cid, prefix, st)
        note = "UMA-s-1p1(omat) · Langevin NVT dt 2fs · equilib 5ps / prod 200ps · MSD 2–50ps. ⚠ 절대값 인용 금지(멀티시드 판정만)."
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
  pseudo_dir = '{_pseudo_dir(st["server"])}'
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

def _pseudo_dir(server):
    # KISTI = Slurm scratch 경로; kgy/gabia = 로컬(경로 확인 필요)
    return ("/scratch/x3430a02/kgy/manuscript_support/pseudo" if "KISTI" in server
            else "./pseudo   # ← 이 서버(kgy/gabia)의 pseudo 경로로 교체")

def _runner_qe(cid, prefix, st):
    server = st["server"]
    guard = f'pgrep -f "{prefix}.in" && {{ echo "이미 실행중"; exit 1; }}   # 중복실행 가드'
    if "KISTI" in server:   # Slurm 클러스터
        return f"""#!/bin/bash
# {cid} · {prefix} — {server} (Slurm)
#SBATCH -J {prefix}
#SBATCH -p <파티션 확인>   # scancel 직후 재제출 금지(QOS 카운터 지연)
#SBATCH --time=24:00:00
#SBATCH -o {prefix}.out
set -e
{guard}
export OMP_NUM_THREADS=1
srun pw.x -in {prefix}.in
grep -a "JOB DONE" {prefix}.out && echo "완료"
"""
    # kgy / gabia = 비-Slurm 인터랙티브 GPU 박스 (ssh, QE-GPU)
    return f"""#!/bin/bash
# {cid} · {prefix} — {server} (ssh, non-Slurm)
set -e
{guard}
nvidia-smi | grep -qE "python|md_" && {{ echo "UMA/MD 실행중 — VRAM 충돌 회피, 대기"; exit 1; }}   # ⚠ pw.x·UMA 동시 실행 금지 (_runner_uma 가드의 대칭형)
export OMP_NUM_THREADS=1
mpirun -np 1 pw.x -in {prefix}.in | tee {prefix}.out    # GPU 빌드는 보통 1 rank
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

def _icohp_val(v):
    """결합값 — 파일마다 키가 갈려 있어(ICOHP_total_eV_per_bond vs ICOHP_eV) 폴백으로 읽는다."""
    if not isinstance(v, dict):
        return None
    for k in ("ICOHP_total_eV_per_bond", "ICOHP_eV"):
        if v.get(k) is not None:
            return v[k]
    return None


def _all_icohp_bonds():
    return _all_icohp_bonds_c(_dir_sig(DB / "properties", "*_icohp.json"))

@lru_cache(maxsize=2)
def _all_icohp_bonds_c(_sig):
    """모든 *_icohp.json 의 bonds → [(system, bond, data)]. mtime-keyed (실시간)."""
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

def _paper_index():
    return _paper_index_c(_dir_sig(LITDB / "papers", "*.md"))

@lru_cache(maxsize=2)
def _paper_index_c(_sig):
    """[{id,title,type,track,blob,el_tags,method_tags}]. blob=slug+title+type+본문앞60줄(소문자).
    litdb-curator가 digest 헤더에 '> elements:'/'> methods:' 태그를 넣으면 정밀 링크(토큰스캔은 보조).
    mtime-keyed 캐시 — 새 digest push 시 즉시 반영(실시간 동기화)."""
    idx = []
    pd = LITDB / "papers"
    for p in list_papers():
        blob = f"{p['id']} {p['title']} {p['type']}"
        el_tags, method_tags = set(), set()
        try:
            head = (pd / f"{p['id']}.md").read_text(encoding="utf-8", errors="ignore").splitlines()[:60]
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
    """이 원소 관련 litdb 논문 — 태그(정밀) ∪ KB litdb_slugs(authored) ∪ 토큰스캔(보조). 클릭 → digest."""
    toks = ELEMENT_TOKENS.get(sym, [])
    kb_slugs = set()
    try:                          # KB의 authored litdb_slugs — cascade 원소 논문 링크의 주 소스
        d = _load_json(KB / "elements" / f"{sym}.json")
        if d:
            kb_slugs = set(d.get("litdb_slugs") or [])
    except Exception:
        pass
    hits, seen = [], set()
    for p in _paper_index():
        if sym in p["el_tags"] or p["id"] in kb_slugs or (toks and any(t in p["blob"] for t in toks)):
            if p["id"] not in seen:
                seen.add(p["id"])
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
                          "icohp": _icohp_val(v),
                          "d": v.get("d_mean_A"), "N": v.get("N")})
    pdos = []
    for f in sorted((DB / "properties").glob("*pdos_element*smooth.csv")):
        try:
            hdr = f.open(encoding="utf-8").readline().strip().lower().split(",")
            if any(sym.lower() == h.strip().split()[0] if h.strip() else False for h in hdr) or sym.lower() in [h.strip() for h in hdr]:
                pdos.append(str(f.relative_to(DB)))
        except Exception:
            pass
    xps = []
    for f in sorted((DB / "properties").glob("*xps*.csv")):
        try:
            if re.search(rf"(^|[^A-Za-z]){re.escape(sym)}([^A-Za-z]|$)", f.read_text(encoding="utf-8", errors="ignore")):
                xps.append(str(f.relative_to(DB)))
        except Exception:
            pass
    return {"compositions": comps, "icohp": bonds,
            "pdos": pdos, "xps": sorted(set(xps)), "papers": element_papers(sym)}

def load_molecular_orbitals() -> dict:
    """kb/molecular_orbitals.json — 화합물 formula → MO 정의 (칩 클릭 팝업용). mtime 캐시(실시간)."""
    return _mo_cache(_mtime_ns(KB / "molecular_orbitals.json"))

@lru_cache(maxsize=2)
def _mo_cache(_mt) -> dict:
    raw = _load_json(KB / "molecular_orbitals.json") or {}
    out = dict(raw)
    for v in raw.values():                       # aliases → 같은 데이터로 키 확장 (formula 표기차 흡수)
        if isinstance(v, dict):
            for a in (v.get("aliases") or []):
                out.setdefault(a, v)
    return out


def element_briefing(syms: list) -> dict:
    kb = load_element_kb()
    syms = [s for s in syms if s in {p[0] for p in PERIODIC}]
    elems = [{"symbol": s, "kb": kb.get(s), "info": element_info(s),
              "anchors": element_db_anchors(s), "cascade": cascade_for_element(s)}
             for s in syms]
    out = {"elements": elems, "multi": None}
    if len(syms) >= 2:
        common = [cid for cid, els in COMP_ELEMENTS.items() if all(s in els for s in syms)]
        sset = set(syms)
        pair = []
        for system, bond, v in _all_icohp_bonds():
            parts = set(re.split(r"[-–]", bond))
            if len(parts) == 2 and parts <= sset:
                pair.append({"system": system, "bond": bond,
                             "icohp": _icohp_val(v), "d": v.get("d_mean_A")})
        papers = {}
        for e in elems:
            for p in e["anchors"]["papers"]:
                papers[p["id"]] = p
        out["multi"] = {"syms": syms, "compositions": common,
                        "bonds": pair, "papers_union": list(papers.values())}
    return out


# ── 전체 주기율표 원소 데이터 (캠페인 밖 원소도 클릭 가능하게) ──
ELEMENT_NAMES = {
 1:"Hydrogen",2:"Helium",3:"Lithium",4:"Beryllium",5:"Boron",6:"Carbon",7:"Nitrogen",8:"Oxygen",9:"Fluorine",10:"Neon",
 11:"Sodium",12:"Magnesium",13:"Aluminium",14:"Silicon",15:"Phosphorus",16:"Sulfur",17:"Chlorine",18:"Argon",19:"Potassium",20:"Calcium",
 21:"Scandium",22:"Titanium",23:"Vanadium",24:"Chromium",25:"Manganese",26:"Iron",27:"Cobalt",28:"Nickel",29:"Copper",30:"Zinc",
 31:"Gallium",32:"Germanium",33:"Arsenic",34:"Selenium",35:"Bromine",36:"Krypton",37:"Rubidium",38:"Strontium",39:"Yttrium",40:"Zirconium",
 41:"Niobium",42:"Molybdenum",43:"Technetium",44:"Ruthenium",45:"Rhodium",46:"Palladium",47:"Silver",48:"Cadmium",49:"Indium",50:"Tin",
 51:"Antimony",52:"Tellurium",53:"Iodine",54:"Xenon",55:"Cesium",56:"Barium",57:"Lanthanum",58:"Cerium",59:"Praseodymium",60:"Neodymium",
 61:"Promethium",62:"Samarium",63:"Europium",64:"Gadolinium",65:"Terbium",66:"Dysprosium",67:"Holmium",68:"Erbium",69:"Thulium",70:"Ytterbium",
 71:"Lutetium",72:"Hafnium",73:"Tantalum",74:"Tungsten",75:"Rhenium",76:"Osmium",77:"Iridium",78:"Platinum",79:"Gold",80:"Mercury",
 81:"Thallium",82:"Lead",83:"Bismuth",84:"Polonium",85:"Astatine",86:"Radon",87:"Francium",88:"Radium",89:"Actinium",90:"Thorium",
 91:"Protactinium",92:"Uranium",93:"Neptunium",94:"Plutonium",95:"Americium",96:"Curium",97:"Berkelium",98:"Californium",99:"Einsteinium",100:"Fermium",
 101:"Mendelevium",102:"Nobelium",103:"Lawrencium",104:"Rutherfordium",105:"Dubnium",106:"Seaborgium",107:"Bohrium",108:"Hassium",109:"Meitnerium",110:"Darmstadtium",
 111:"Roentgenium",112:"Copernicium",113:"Nihonium",114:"Flerovium",115:"Moscovium",116:"Livermorium",117:"Tennessine",118:"Oganesson",
}
ELEMENT_EN = {"H":2.20,"Li":0.98,"Be":1.57,"B":2.04,"C":2.55,"N":3.04,"O":3.44,"F":3.98,"Na":0.93,"Mg":1.31,"Al":1.61,
 "Si":1.90,"P":2.19,"S":2.58,"Cl":3.16,"K":0.82,"Ca":1.00,"Sc":1.36,"Ti":1.54,"V":1.63,"Cr":1.66,"Mn":1.55,"Fe":1.83,
 "Co":1.88,"Ni":1.91,"Cu":1.90,"Zn":1.65,"Ga":1.81,"Ge":2.01,"As":2.18,"Se":2.55,"Br":2.96,"Rb":0.82,"Sr":0.95,"Y":1.22,
 "Zr":1.33,"Nb":1.60,"Mo":2.16,"Tc":1.90,"Ru":2.20,"Rh":2.28,"Pd":2.20,"Ag":1.93,"Cd":1.69,"In":1.78,"Sn":1.96,"Sb":2.05,
 "Te":2.10,"I":2.66,"Cs":0.79,"Ba":0.89,"La":1.10,"Ce":1.12,"Pr":1.13,"Nd":1.14,"Sm":1.17,"Eu":1.20,"Gd":1.20,"Tb":1.10,
 "Dy":1.22,"Ho":1.23,"Er":1.24,"Tm":1.25,"Yb":1.10,"Lu":1.27,"Hf":1.30,"Ta":1.50,"W":2.36,"Re":1.90,"Os":2.20,"Ir":2.20,
 "Pt":2.28,"Au":2.54,"Hg":2.00,"Tl":1.62,"Pb":2.33,"Bi":2.02,"Po":2.00,"At":2.20,"Fr":0.70,"Ra":0.90,"Ac":1.10,"Th":1.30,
 "U":1.38,"Np":1.36,"Pu":1.28}
_METALLOID = {"B","Si","Ge","As","Sb","Te","Po","At"}
_NONMETAL = {"H","C","N","O","P","S","Se"}
_ELEM_GP = {p[0]: (p[1], p[2]) for p in PERIODIC}  # sym -> (Z, group)

def element_category(sym: str) -> str:
    z, grp = _ELEM_GP.get(sym, (0, 0))
    if 57 <= z <= 71:  return "lanthanide"
    if 89 <= z <= 103: return "actinide"
    if sym in _METALLOID: return "metalloid"
    if grp == 1: return "nonmetal" if sym == "H" else "alkali metal"
    if grp == 2: return "alkaline earth"
    if grp == 18: return "noble gas"
    if grp == 17: return "halogen"
    if 3 <= grp <= 12: return "transition metal"
    if sym in _NONMETAL: return "nonmetal"
    if grp >= 13: return "post-transition metal"
    return "other"

def element_info(sym: str) -> dict:
    z = _ELEM_GP.get(sym, (None, None))[0]
    return {"name": ELEMENT_NAMES.get(z, sym), "Z": z,
            "category": element_category(sym), "en": ELEMENT_EN.get(sym),
            "in_campaign": sym in campaign_elements()}

def _cascade_by_element() -> dict:
    return _cascade_by_element_c(_mtime_ns(DB / "properties" / CASCADE_FILES["ranked"]))

@lru_cache(maxsize=2)
def _cascade_by_element_c(_mt) -> dict:
    """캐스케이드 도펀트(Sc2O3, Fe2O3…) → 그 금속 원소별 랭킹 행. mtime-keyed (실시간)."""
    rows = load_cascade().get("ranked", {}).get("data", [])
    out = {}
    for r in rows:
        m = re.match(r"([A-Z][a-z]?)", str(r.get("dopant", "")))
        if m:
            out.setdefault(m.group(1), []).append({
                "dopant": r.get("dopant"), "rank": r.get("rank"), "score": r.get("score"),
                "ox_V": r.get("ox_V"), "E_GPa": r.get("E_GPa"), "pugh": r.get("pugh"), "group": r.get("group")})
    return out

def cascade_for_element(sym: str) -> list:
    return _cascade_by_element().get(sym, [])


# ── 대시보드 '핵심 발견' 하이라이트 (커버리지% 대신 히어로로) ──
def dashboard_highlights() -> list:
    C, L = CANONICAL, {k: v["label"] for k, v in COMPOSITIONS.items()}
    hi = []
    g = sorted(((v, cid) for cid, v in C["gap_eV"].items() if v is not None), reverse=True)
    if g:
        hi.append({"t": "Band gap", "v": f"{L.get(g[0][1], g[0][1])} {g[0][0]} eV",
                   "n": "+O(LPSOCl)가 전자 절연 최강 · fixed-occ eigenvalue (comp2 잠정)"})
    hi.append({"t": "P–S 골격 vs Li–X 이온", "v": "ICOHP −6.0 ≫ −2.1 eV",
               "n": "강한 공유 골격 + 약한 이온결합 · comp2 Li–Br(−1.93)이 Li–Cl(−2.11)보다 약해 "
                    "격자 연화(E_VRH 22.06→20.03, B_VRH −18.2%) — 단 Pugh B/G는 3.14→2.79로 오히려 "
                    "감소라 '연성 이득'은 아님"})
    e = sorted((v, cid) for cid, v in C["MD_Ea_eV"].items() if v is not None)
    if e:
        hi.append({"t": "이온 전도 Ea (UMA)", "v": f"{L.get(e[0][1], e[0][1])} {e[0][0]} eV 최저",
                   "n": "Cl-rich가 Li 이동 유리 · ⚠멀티시드 판정(절대값 인용주의)"})
    ce = _cascade_by_element()
    top = None
    for rows in ce.values():
        for r in rows:
            if r.get("rank") == 1:
                top = r
    if top:
        hi.append({"t": "도핑 스크리닝 1위 후보", "v": f"{top['dopant']} (UMA #1)",
                   "n": "코팅 후보 상위 · Nd₂O₃·B₂O₃는 DFT 검증됨 (절대값은 상대비교만)"})
    # ⚠ hBN은 db가 수치 인용을 금지한 값 — 경로 전체 폭 7 meV < 이미지당 힘오차 46 meV/Å
    #   (vgcf_hbn_neb.json: "Report as '< 0.01 eV, effectively barrierless'"). 2L2L은 층수 미수렴 상한.
    hi.append({"t": "VGCF/hBN Li 확산 (CI-NEB)",
               "v": "hBN <0.01(사실상 무장벽) · graphene(1L) 0.273 · gallery 2L2L 0.147 eV (대표)",
               "n": "hBN은 수치 분해능 이하 · 2L2L은 층수 미수렴=상한 · barrier 층수 민감 −209 meV 반증 "
                    "→ 혼합층 2건·graphene 2L NEB 진행중"})
    # comp2 disorder ensemble — ⚠ 단일 config Ea/σ 수치 인용 금지(멀티 config 판정 전, 데이터 규율)
    hi.append({"t": "comp2 disorder ensemble", "v": "d=0.50 anneal+relax 파이프라인 가동",
               "n": "cfg0 3온도 완료 · 멀티 config 판정 대기"})
    return hi
