"""
data.py — DFT 지식 인프라 데이터 계층 (Flask 라우트가 이걸 호출).

핵심 철학: db/ 를 실시간으로 읽어 "조성 × 물성" 매트릭스를 구성한다.
db 파일이 바뀌면(계산 등록) 사이트가 자동으로 최신값을 반영 = "계속 동기화".
canonical 방법 메타(kb/methodology/computational_methods_canonical.md)와 연동해
각 값에 pseudo/k/cell·비교가능성·stale 배지를 붙일 수 있게 한다.
"""
from __future__ import annotations
import json, csv, re, os
import datetime as _dt
from urllib.parse import quote as _urlquote
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

#: 이 status 만 정본으로 본다. 나머지는 **전부** release 화면에서 뺀다.
#: (status 가 아예 없는 legacy record 는 당분간 정본으로 취급 — legacy debt)
_STATUS_OK = {"", "none", "canonical", "ok"}
#: 아는 비정본 status. 여기 없는 낯선 값은 **fail-closed** 로 뺀다.
_STATUS_KNOWN_BAD = {"rejected", "retracted", "superseded", "deprecated",
                     "historical", "diagnostic", "provisional", "skipped"}


def record_shown(rec):
    """(보여줄까, 숨긴 이유) — db record 하나의 release 노출 판정.

    ⚠ **allowlist 다.** denylist(`status != "rejected"`)로 두면 새 status 가 생길 때마다
      조용히 뚫린다. 2026-08-12 에 실제로 그랬다: retracted 로 표시한 4f-in-valence 갭
      −6.46 eV 가 webapp 에 밴드갭으로 계속 나오고 있었다.

    이 함수가 **못 하는 것**: status 가 없는 legacy record 를 검증하지 못한다.
      지금은 정본으로 통과시킨다(legacy debt). schema v1 이 들어오면 fail-closed 로 바꾼다.
    """
    if not isinstance(rec, dict):
        return True, None
    s = str(rec.get("status") or "").strip().lower()
    if s in _STATUS_OK:
        return True, None
    if s in _STATUS_KNOWN_BAD:
        return False, s
    return False, f"unknown status {s!r} (fail-closed)"

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

def load_tq_ledger() -> list:
    """db/properties/tq_ledger_*.json 전부를 **날짜 역순 리스트**로 (최신이 [0]).

    내일 tq_ledger_2026_08_27.json 이 추가되면 코드 수정 없이 잡힌다 (glob).
    파일이 하나도 없으면 빈 리스트. 깨진 파일은 조용히 빼지 않고
    {"_file", "_error"} 항목으로 남긴다 — "원장이 없다" 와 "원장을 못 읽었다" 는
    화면에서 **다른 문장**이어야 한다 (governance_page 교훈, 2026-08-20).

    이 로더가 **못 하는 것**:
      · 스키마(tq_ledger/v1) 검증 — schema 문자열을 그대로 실을 뿐 거르지 않는다.
      · 상태·결과 문자열의 옳고 그름 판정 — 원장을 그대로 옮긴다.
      · 여러 날짜 원장의 병합/중복 제거 — 하루치 파일 단위로만 준다.
    """
    out = []
    for f in (DB / "properties").glob("tq_ledger_*.json"):
        d = _load_json(f)
        if not isinstance(d, dict):
            d = {"_error": "JSON 을 읽지 못했다 (깨졌거나 dict 가 아니다)"}
        d = dict(d)
        d["_file"] = f.name
        out.append(d)
    # date 필드 우선, 없으면 파일명(tq_ledger_YYYY_MM_DD)이 정렬을 대신한다
    out.sort(key=lambda d: (str(d.get("date") or ""), d["_file"]), reverse=True)
    return out


def load_canonical_methods() -> str:
    p = KB / "methodology" / "computational_methods_canonical.md"
    return p.read_text(encoding="utf-8") if p.exists() else ""


SDCP_WAVE1_MD = KB / "results" / "sdcp_wave1_explainer_2026_08_25.md"
#: 자기도핑 개념 해설 — 배경지식 0 기준. 원고 문장("proton" vs "hydrogen atom")
#:   하나가 charge/multiplicity 를 바꾸는 문제라 화면에 둔다.
SDCP_SELFDOPING_MD = KB / "concepts" / "sdcp_self_doping_explainer_2026_08_26.md"
SDCP_WAVE1_JSON = DB / "properties" / "sdcp_wave1_results.json"


def load_sdcp_wave1_md() -> str:
    return SDCP_WAVE1_MD.read_text(encoding="utf-8") if SDCP_WAVE1_MD.exists() else ""


def load_sdcp_selfdoping_md() -> str:
    """자기도핑 개념 해설 md. 없으면 빈 문자열 — 화면이 그렇게 말한다."""
    return (SDCP_SELFDOPING_MD.read_text(encoding="utf-8")
            if SDCP_SELFDOPING_MD.exists() else "")


def sdcp_wave1_rows() -> dict:
    """wave1 잡 표를 **basin 일치 여부와 함께** 낸다.

    ⛔ 이 함수가 못 하는 것: basin 이 어긋난 잡의 값을 보정하지 않는다.
      50 meV 벌점을 알고 있어도 빼지 않는다 — 4점 추정으로 결론을 만들면
      측정이 아니라 가정이 된다. 어긋난 행은 값과 함께 **경고를 달아** 낸다.
    """
    if not SDCP_WAVE1_JSON.exists():
        return {}
    d = json.loads(SDCP_WAVE1_JSON.read_text(encoding="utf-8"))
    jobs = d.get("jobs", [])
    # 자리 선호 ΔE = E(Ni_top) − E(Li_top) — 같은 조각·같은 seed 끼리만
    by = {}
    for j in jobs:
        by.setdefault((j["fragment"], j["seed"]), {})[j["pose"]] = j
    dE = []
    for (frag, seed), d2 in sorted(by.items()):
        if "Nitop" not in d2 or "Litop" not in d2:
            continue
        ni, li = d2["Nitop"], d2["Litop"]
        same = ni["basin"] == li["basin"]
        dE.append({"fragment": frag, "seed": seed,
                   "dE_meV": round((ni["E_total_eV"] - li["E_total_eV"]) * 1000, 1),
                   "basin_pair": f'{li["basin"]}/{ni["basin"]}', "valid": same})
    return {"meta": d, "jobs": jobs, "dE": dE,
            "n_valid": sum(1 for r in dE if r["valid"]), "n_dE": len(dE)}


OPEN_ITEMS_MD = KB / "open_items.md"


def load_open_items_md() -> str:
    return OPEN_ITEMS_MD.read_text(encoding="utf-8") if OPEN_ITEMS_MD.exists() else ""


#: 1저자 요청 대장. 이 캠페인에서 **가장 자주 되돌아오는 문서**라 라우트를 준다
#: (그동안 경로를 기억하거나 grep 해서 찾아야 했다).
REQUESTS_MD = KB / "reports" / "paper_first_author_requests_2026_08.md"


def load_requests_md() -> str:
    return REQUESTS_MD.read_text(encoding="utf-8") if REQUESTS_MD.exists() else ""


def requests_ledger() -> list:
    """요청 대장 표(§ '📋 요청 대장')를 파싱해 요청별 상태만 뽑는다.

    ⚠ 본문 전체를 읽기 전에 **어디가 닫혔고 어디가 안 닫혔나**를 먼저 보여주려는 것이다.
    ⛔ 이 함수가 못 하는 것: 상태의 옳고 그름을 판정하지 않는다. 표를 옮길 뿐이다.
      표 형식이 바뀌면 조용히 빈 리스트가 되므로, 화면은 비었을 때 그렇게 말해야 한다.
    """
    md = load_requests_md()
    rows, seen = [], False
    for ln in md.splitlines():
        if ln.startswith("| 요청 |"):
            seen = True
            continue
        if seen:
            if not ln.startswith("|"):
                if rows:
                    break
                continue
            c = [x.strip() for x in ln.strip().strip("|").split("|")]
            if len(c) < 4 or set(c[0]) <= set("-: "):
                continue
            num = c[0].replace("*", "").strip()
            if not num or not num[0].isdigit():
                continue
            st = c[2]
            mark = ("done" if "✅" in st else "blocked" if "🔴" in st
                    else "partial" if ("🟡" in st or "⚠" in st) else "open")
            # ⚠ 이모지와 문장이 어긋나는 행이 실제로 있다 (요청 5: 🔴 인데 "재작성 완료").
            #   한쪽을 골라 조용히 정하면 화면이 원문과 다른 말을 하게 된다.
            #   → 어긋났다고 **표시**하고 판단은 사람에게 넘긴다.
            says_done = ("완료" in st or "닫" in st) and "미완" not in st
            conflict = (mark == "blocked" and says_done) or (mark == "done" and "미완" in st)
            rows.append({"n": num, "what": c[1].replace("**", ""),
                         "status": st, "mark": mark, "conflict": conflict,
                         "where": c[3] if len(c) > 3 else ""})
    return rows


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
        # ⚠ iterdir() 은 **하위 디렉터리를 안 들어간다**. 실측(2026-07-29): vgcf_hbn 페이지에
        #   VGCF/hBN 구조가 하나도 안 뜨고 Li₃N 것만 떴다 — 진짜 구조는
        #   db/structures/vgcf_hbn/ 안에 있었고 /api/structure 로는 200 으로 서빙되는데
        #   목록에만 없었다. db/structures/lpsocl_candidates/ 도 같은 이유로 통째로 숨었다.
        #   rglob 으로 바꾸고, 이름은 sd 기준 상대경로로 준다(라우트가 path 를 받는다).
        for f in sorted(sd.rglob("*")):
            if f.is_file() and f.suffix.lower() in (".cif", ".xyz", ".vasp", ".vesta", ".cube"):
                rel = f.relative_to(sd).as_posix()
                # 하위 폴더면 폴더명도 prefix 매칭 대상 (vgcf_hbn/Li_on_graphene… 처럼
                # 파일명 자체엔 조성 토큰이 없는 경우가 있다)
                if _prefix_starts(f.name, pref) or _prefix_starts(rel.replace("/", "_"), pref):
                    sfx = f.suffix.lower()
                    out.append({"name": rel, "ext": f.suffix.lstrip("."),
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
    # ⚠ phonon 을 dos 보다 **먼저** 봐야 한다 — b2o3_phonon_dos.csv 가 전자 DOS 로 라벨됐다.
    #   icohp/cohp 순서 함정과 같은 계열이다 (아래 주석 참조).
    for k, tag in [("phonon", "Phonon"), ("pdos", "PDOS"), ("dos", "DOS"), ("arrhenius", "Arrhenius"),
                   ("conductivity", "Conductivity"), ("msd", "MSD"), ("eos", "EOS"),
                   # ⚠ bv_path_* (BVSE 경로·구간표) 가 'data' 로 떨어져 있었다 — 같은 BVSE 자료다.
                   ("bvse", "BVSE"), ("bv_path", "BVSE"), ("bv_3d", "BVSE"), ("bv_vs_pmf", "PMF"),
                   ("pmf", "PMF"), ("elf", "ELF"),
                   ("charge", "Charge"), ("bader", "Bader"), ("xps", "XPS"),
                   ("voronoi", "Voronoi"), ("neb", "NEB"), ("barrier", "Barrier"),
                   ("drag", "Drag"), ("diffusion", "Diffusion"), ("binding", "Binding"),
                   # ⚠ icohp 를 cohp 보다 **먼저** 봐야 한다 — 'icohp' 안에 'cohp' 가 들어 있어서
                   #   순서가 뒤집히면 ICOHP 표가 COHP 칩으로 잘못 붙는다.
                   ("icohp", "ICOHP"), ("cohp", "COHP"),
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

# ─────────────────────────────────────────────────────────────
# canonical 앵커값 — **db/properties/canonical_registry.json 이 유일한 원천이다.**
#
# 2026-08-07 (Codex 코드리뷰 P1) 이전에는 이 자리에 숫자가 하드코딩돼 있었다. 그러면
# db 에 새 계산을 등록해도 화면이 안 바뀐다 — 교차검증 도구에서 제일 위험한 조용한 drift.
#
# ★ 이관하면서 리뷰가 짚은 것보다 한 겹 더 나쁜 걸 찾았다. 옛 `MD_Ea_eV` 딕셔너리 안에서
#   **프로토콜이 섞여 있었다**: comp1 0.253·modelc 0.224 는 단일 궤적인데 lpsocl 0.287 은
#   4-seed×3-T 였다. 대시보드가 `sorted()` 로 고른 "최저값"은 라벨을 고쳐도 무효였다 —
#   단일시드와 멀티시드를 한 줄에 세운 순위였기 때문이다.
#   → 지금은 metric 을 나눴다. `MD_Ea_eV` = 멀티시드 정본(modelc 0.197±0.032 ·
#     b2o3 0.199±0.034 · lpsocl 0.2867±0.024), `MD_Ea_eV_singleseed` = 같은 창 단일 궤적 앵커.
#     comp1 은 멀티시드 실행이 없으므로 `MD_Ea_eV` 에서 **빠지는 게 맞다**(빈칸 = 정직).
#
# ⚠ 값을 고치려면 이 파일이 아니라 레지스트리를 고친다. 그리고 반드시:
#     python3 tools/db/validate_canonical.py
#   가 통과해야 한다 — 레지스트리가 원자료(source_path/source_key)와 맞는지 검사한다.
# ─────────────────────────────────────────────────────────────
try:
    import canonical as _C
except ImportError:                                    # 도구가 webapp 밖에서 import 할 때
    import sys as _sys
    _sys.path.insert(0, str(ROOT / "webapp"))
    import canonical as _C

if not _C.registry().get("entries"):
    raise RuntimeError(
        "db/properties/canonical_registry.json 이 비었거나 없다 — 정본을 만들 수 없다. "
        "이 파일에 숫자를 되돌려 넣지 말고 레지스트리를 복구할 것.")


# ⚠ 전역 상수로 만들면 **import 때 한 번**이라, 오래 사는 gunicorn worker 에서
#   db 를 고쳐도 재시작 전까지 화면이 안 바뀐다 (2026-08-07 Codex 3라운드 실측).
#   → 매번 mtime 캐시를 통해 읽는다. 파일이 안 바뀌었으면 캐시라 사실상 공짜다.
class _LazyMap(dict):
    """`CANONICAL[...]` 이라는 기존 사용법을 유지하면서 매 접근마다 최신을 읽는다."""

    def _now(self):
        m = {}
        for e in _C.registry()["entries"]:
            if e.get("value") is not None:
                m.setdefault(e["metric"], {})[e["system"]] = e["value"]
        return m

    def __getitem__(self, k):
        return self._now()[k]

    def get(self, k, d=None):
        return self._now().get(k, d)

    def __iter__(self):
        return iter(self._now())

    def keys(self):
        return self._now().keys()

    def items(self):
        return self._now().items()

    def values(self):
        return self._now().values()

    def __len__(self):
        return len(self._now())

    def __contains__(self, k):
        return k in self._now()

    def __repr__(self):
        return repr(self._now())


# 표시용 union (정본 + 잠정 + 미검토). 순위·비교에는 쓰지 말 것 — canonical_comparable() 참조.
CANONICAL = _LazyMap()


def canonical_entry_index():
    """(metric, system) → 항목 전체. 배지·툴팁·출처 링크·그룹 강제가 여기서 나온다."""
    return _C.index(_C.registry())


class _LazyIndex(dict):
    """CANONICAL_ENTRY 도 같은 이유로 지연 평가한다."""

    def __getitem__(self, k):
        return canonical_entry_index()[k]

    def get(self, k, d=None):
        return canonical_entry_index().get(k, d)

    def items(self):
        return canonical_entry_index().items()

    def keys(self):
        return canonical_entry_index().keys()

    def values(self):
        return canonical_entry_index().values()

    def __iter__(self):
        return iter(canonical_entry_index())

    def __len__(self):
        return len(canonical_entry_index())

    def __contains__(self, k):
        return k in canonical_entry_index()


CANONICAL_ENTRY = _LazyIndex()

# ★ 자동판정(순위·차트·레이더)에서 **반드시 빠지는** 상태들.
#   unreviewed_drift = 원자료가 바뀌었는데 아직 검토 안 됨
#   source_error     = 원자료를 못 읽어 레지스트리 값이 stale 일 수 있음
#   나머지(provisional·source_pending·superseded)도 정본이 아니다.
NON_CANONICAL_STATUS = ("unreviewed_drift", "source_error", "provisional",
                        "source_pending", "superseded")


def canonical_group(metric: str, system: str):
    """이 값이 어느 비교 묶음에 속하나. 다르면 **같은 축에 올리면 안 된다.**"""
    e = CANONICAL_ENTRY.get((metric, system))
    return (e or {}).get("comparison_group")


def canonical_comparable(metric: str, group: str = None, status=("canonical",)) -> dict:
    """{system: value} — **같은 프로토콜끼리만**. 순위·최저값·레이더는 이걸 쓴다.

    group 을 생략하면 그 metric 에서 항목이 제일 많은 그룹을 고른다(기본 비교 집합).
    """
    reg = _C.registry()
    if group is None:
        gs = _C.groups_of(reg, metric)
        gs = {k: [x for x in v if x.get("status") in status] for k, v in gs.items()}
        gs = {k: v for k, v in gs.items() if v}
        if not gs:
            return {}
        group = max(gs, key=lambda k: len(gs[k]))
    return _C.canonical_map(reg, metric, group=group, status=status)
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
# ⚠ 여기에 숫자를 다시 넣지 말 것 — 정본은 db/properties/canonical_registry.json 이다.
#   2026-08-07 (Codex 5라운드): `("MD_Ea_eV","comp2"): 0.275` 가 남아 있어서, 레지스트리에서
#   ordered/disorder 로 쪼갠 뒤에도 화면에 **옛 0.275 가 계속 나왔다.** 레지스트리 이관의
#   전형적인 잔재다. 잠정값도 레지스트리의 status=provisional 로 표현한다.
CANONICAL_PROVISIONAL_VALUES = {}
# (metric, comp) : 사유 — 이 값은 '아직 안 한 것'이 아니라 '하면 안 되거나 정의되지 않는 것'.
# composition/explorer 에서 TODO 가 아니라 'N/A' 로 렌더된다.
CANONICAL_NA = {
    ("MD_Ea_eV", "li3n"):  "UMA MLIP 금지 조성 (2026-06 편향 판정) — DFT-AIMD/QE-NEB 축으로만. TODO 아님",
    # ⛔ 2026-08-25 — b2o3 는 **두 번째 UMA 실패 조성**이다. 값이 없는 게 아니라 있는 값을
    #   내렸다: 골격(비-Li)이 800 K 부터 같이 움직여 D_Li 가 이온수송이 아니다.
    ("MD_Ea_eV", "b2o3"): (
        "⛔ 2026-08-25 철회 — 골격이 같이 움직인다. 비-Li β: 800 K [0.51·0.79·0.54] · "
        "1000 K [0.50·0.78·0.47] · 1200 K 6/6 이 0.63–1.15 (기준 0.30). "
        "같은 포텐셜·온도의 modelc 는 7/7 rigid(≤0.27) ⇒ b2o3 고유. "
        "공동계(COM 제거) 구제 시도도 9/9 재배열(남는 몫 0.95–1.00)로 실패. "
        "⚠ 덧셈 오염이 아니다(골격 MSD 는 Li 의 2–6 %). 골격 RMS 변위가 800 K 에서 "
        "1.7–3.1 Å 로 **결합 길이보다 커** 원자가 제 자리를 떠난다 ⇒ 런 도중 자리 지도가 "
        "바뀌어 **Ea 가 이동 장벽이 아니게** 된다(구간 Ea 0.224→0.078→0.371 비단조). TODO 아님"),
    ("sigma_300K_mS_cm", "b2o3"): (
        "⛔ 2026-08-25 철회 — MD_Ea_eV 와 같은 사유(골격 재배열). 단일시드 1.33× 는 "
        "2026-07-09 에 이미 철회됐고 멀티시드로 modelc 와 동등이었다. TODO 아님"),
    ("MD_Ea_eV", "sdcp"):  "분자계(ORCA) — 격자 Li 확산 축이 없음",
    ("MD_Ea_eV", "lic6"):  "interphase 상 — 격자 Li 확산 Arrhenius 축 아님",
    ("gap_eV", "sdcp"):    "분자계 — 주기 밴드갭 대신 HOMO–LUMO 축",
    ("B0_GPa", "sdcp"):    "분자계 — 주기셀 EOS 정의 안 됨",
    ("E_VRH_GPa", "sdcp"): "분자계 — 탄성텐서 정의 안 됨",
    ("B0_GPa", "vgcf_hbn"): "슬랩 — 주기 벌크 EOS 정의 안 됨",
    ("E_VRH_GPa", "vgcf_hbn"): "슬랩 — 벌크 탄성텐서 정의 안 됨",
}
# ── metric 표시 메타 — 화면 세 곳(compare/explorer/composition)이 각자 하드코딩하던 것.
#   레지스트리에 metric 이 늘면(ordered/disorder 처럼) 화면이 자동으로 따라와야 한다
#   (2026-08-07 Codex 5라운드: 새 두 metric 이 label·unit 없이 렌더됐다).
_METRIC_LABEL = {
    "gap_eV": ("Band gap", "eV", "gap"),
    "B0_GPa": ("EOS B₀", "GPa", "B₀"),
    "E_VRH_GPa": ("E_VRH", "GPa", "E_VRH"),
    "MD_Ea_eV": ("MD Ea", "eV", "MD Ea"),
    "MD_Ea_eV_ordered": ("MD Ea (ordered)", "eV", "Ea-ord"),
    "MD_Ea_eV_disorder": ("MD Ea (disorder d=0.50)", "eV", "Ea-dis"),
    "MD_Ea_eV_singleseed": ("MD Ea (단일시드 앵커)", "eV", "Ea-1seed"),
    "ICOHP_PS": ("ICOHP P–S", "eV", "ICOHP"),
}


def metric_meta() -> dict:
    """레지스트리에 있는 **모든** metric 의 (label, unit, short). 없으면 metric 이름 그대로."""
    out = {}
    for m in sorted({e.get("metric") for e in _C.registry()["entries"] if e.get("metric")}):
        lab, unit, short = _METRIC_LABEL.get(m, (m, "", m))
        out[m] = {"label": lab, "unit": unit, "short": short}
    return out


CANONICAL_META = {
    "gap_eV":    "fixed-occ eigenvalue (DOS-threshold 금지) · comp2는 잠정(legacy, 재확인중)",
    "B0_GPa":    "DFT BM3 EOS",
    "E_VRH_GPa": "DFT relaxed-ion USPP·k444(comp1·comp2)/셀별·0.005 — comp1↔comp2만 완전비교쌍",
    "MD_Ea_eV":  "UMA-s-1p1 · 600/800/1000 K 3점 피팅 · ⚠절대값 인용 금지. "
                 "시드 프로토콜 혼재: comp1/modelc=단일 궤적(오차막대 없음), lpsocl=4-seed×3-T, "
                 "comp2=3-seed(잠정) — 조성 간 비교는 같은 프로토콜끼리만",
    "ICOHP_PS":  "LOBSTER all-PAW ext-basis (comp2 = comp2_icohp_origin.csv, 2026-07-25 커밋)",
    "MD_Ea_eV_ordered":    "UMA 3-seed · **ordered single-champion baseline** — disorder ensemble 과 "
                           "다른 계산이다(원자료가 'anion disorder 를 샘플링하지 않았다'고 명시)",
    "MD_Ea_eV_disorder":   "UMA 3-**config** · anion disorder d=0.50 · 게이트 통과했으나 config 산포 45% "
                           "— 'ordered 보다 낮다'까지만, 값 정밀 인용 금지",
    "MD_Ea_eV_singleseed": "UMA 단일 궤적 deck 앵커 — 같은 창의 단일 궤적끼리만 짝짓는다",
}

# ── 세부 분석 열 (explorer '더 보기') ────────────────────────────────────
# 1저자 요청(2026-08-06): "dos, pdos, elf 등등 많잖아 — 세분화하고 매칭시켜줘".
# ⚠ CANONICAL(위 5개)은 kb 나침반과 짝이 맞는 **앵커**다. 여기 값을 거기 섞으면
#   compare·metric 카드가 '미계산 TODO' 를 잘못 띄운다 → **별도 그룹**으로 둔다.
#   빈칸은 TODO 가 아니라 '—' (그 계에 그 분석을 안 했거나 정의가 다르다).
_ELF_SYS2CID = {"comp1": "comp1", "modelc": "modelc", "lpsocl": "lpsocl",
                "lpscl1.6": "modelc", "b2o3": "b2o3"}
_BADER_FILES = {"modelc": "bader_ae_modelc_LPSCl16.csv", "b2o3": "bader_ae_b2o3.csv",
                "lpsocl": "bader_ae_lpsocl.csv"}


@lru_cache(maxsize=2)
# ─────────────────────────────────────────────────────────────
# 방법 검증 앵커 (2026-08-20 신설) — **조성 물성 표와 섞지 않는다.**
#   왜 따로인가: canonical_registry 는 "이 물질의 값이 얼마냐" 이고, 여기는
#   "우리 계산기가 얼마나 맞나" 다. 축이 다르다 — 섞으면 'UMA 힘 오차' 가 comp1 의
#   물성인 것처럼 읽힌다. 그래서 metric 표에 넣지 않고 별도 섹션으로 뽑는다.
#   ⚠ 여기 값은 **재료 비교에 쓰는 수치가 아니다.** 전부 한계를 같이 싣는다.

def method_anchors() -> list:
    """UMA 검증 앵커 목록. 파일이 없으면 그 항목만 빠진다(빈 화면이 되지 않게).

    각 항목: {key, title, value, verdict, note, limit, src}
    """
    out = []

    b = _load_json_safe("db/properties/mlip_bench_li3ps4_uma.json")
    if b:
        r = (b.get("results") or {})
        f = (r.get("forces") or {})
        pe = (f.get("per_element") or {})
        li = (pe.get("Li") or {}).get("MAE")
        e = (r.get("energy_after_reference_correction") or {})
        out.append({
            "key": "force_mae",
            "title": "UMA 힘 정확도 (Li₃PS₄ DFT 라벨)",
            "value": (f"{1000*f['MAE_eV_per_A']:.1f} meV/Å"
                      + (f"  ·  Li {1000*li:.1f}" if li else "")) if f.get("MAE_eV_per_A") else "—",
            "verdict": "⭕ 전용 모델보다 정확",
            "note": (f"같은 test set 공표값: bespoke **35.6** · LoRA 39.2 · PET-MAD 기저 63.9 "
                     f"(우리는 이 데이터를 **학습한 적이 없다**). test {r.get('n_structures','?')}구조, "
                     f"실패 {r.get('n_failed','?')}. 보정 후 에너지 "
                     f"{1000*e.get('MAE_eV_per_atom', 0):.1f} meV/atom."),
            "limit": ("**힘 축에서만**이다 — 에너지는 전용 모델이 앞선다. **응력·장벽은 안 쟀다.** "
                      "조성에 **Cl 이 없다**(Li₃PS₄). 상대에너지 RRMSE 는 분모가 크기 차이로 "
                      "부풀어 약한 지표다 — RMSE 를 볼 것."),
            "src": "db/properties/mlip_bench_li3ps4_uma.json",
        })

    for tag in ("comp1", "li3p"):
        pr = _load_json_safe(f"db/properties/mlip_engine_probe_{tag}.json")
        if not pr:
            continue
        c = pr.get("conservativeness")
        if c:
            bd = c.get("by_delta") or {}
            ds = sorted(bd, key=float)
            val = " · ".join(f"δ={d} {100*bd[d]['rel_mean']:.2f}%" for d in ds)
            out.append({
                "key": f"conservative_{tag}", "title": f"보존성 (힘 = −∇E) — {tag}",
                "value": val or "—", "verdict": "⭕ 보존적" if c.get("verdict") == "conservative"
                                                else f"⚠ {c.get('verdict')}",
                "note": ("δ 를 키우면 편차가 줄어든다 = **에너지 수치잡음**이지 비보존이 아니다. "
                         "비보존이면 δ 를 키워도 남아야 한다. ⇒ PET-MAD 가 보고한 직접힘 병리"
                         "(기하최적화 미수렴·종별 온도 분리·MSD 과대)는 UMA 에 안 걸린다."),
                "limit": c.get("limitation", ""), "src": f"db/properties/mlip_engine_probe_{tag}.json"})
        t = pr.get("timing")
        if t:
            rows = t.get("rows") or []
            val = " → ".join(f"{x['n_atoms']}원자 {x['us_per_atom_step']:.0f}" for x in rows)
            out.append({
                "key": f"timing_{tag}", "title": f"셀 비용 (µs/atom·step) — {tag}",
                "value": val or "—",
                "verdict": "⭕ 오버헤드 지배" if t.get("verdict") == "overhead_bound" else "⚠ 연산 지배",
                "note": (t.get("message", "") + "  ⚠ 단 **상자를 키우면 D 자체가 이동한다**"
                         "(LPSOCl 600 K 에서 1.65배) — 승격하면 전 조성을 다시 돌려야 한다. "
                         "1런 = 시드 1개라 멀티시드 규율상 **2–3시드 × 큰 셀**이 맞다."),
                "limit": t.get("limitation", ""), "src": f"db/properties/mlip_engine_probe_{tag}.json"})
        rd = pr.get("residual_at_dft_minimum")
        if rd:
            out.append({
                "key": f"residual_{tag}", "title": f"DFT 최소점 잔여력 — {tag}",
                "value": f"fmax {rd['fmax_eV_per_A']:.4f} · frms {rd['frms_eV_per_A']:.4f} eV/Å",
                "verdict": {"agrees": "⭕ 두 PES 가 같은 자리", "mild": "⚠ 잔여력 보임",
                            "disagrees": "⛔ 최소점이 다르다"}.get(rd.get("verdict"), "—"),
                "note": (rd.get("message", "") + f"  ({rd.get('n_atoms','?')}원자, "
                         + " · ".join(f"{k} n={v['n']}" for k, v in (rd.get("per_element") or {}).items()) + ")"),
                "limit": (rd.get("limitation", "") + "  ⚠ 고대칭 소형 셀이면 대칭으로 0 이 되는 "
                          "원소가 있어 **사실상 일부 원소만** 시험한 것이다. **장벽은 미검증**"
                          "(Li₃Nd 에서 UMA 는 1.76배 과대였다)."),
                "src": f"db/properties/mlip_engine_probe_{tag}.json"})

    sc = _load_json_safe("db/properties/sei_neb_uma_scout.json")
    if sc and sc.get("runs"):
        by = {}
        for r in sc["runs"]:
            if r.get("Ea_forward_eV") is None:
                continue
            by.setdefault((r.get("tag"), r.get("shell")), {})[tuple(r.get("supercell") or [])] = r
        ratios = []
        for k, v in by.items():
            a, b2 = v.get((1, 1, 1)), v.get((2, 2, 2))
            if a and b2 and b2["Ea_forward_eV"] > 0:
                ratios.append(a["Ea_forward_eV"] / b2["Ea_forward_eV"])
        if ratios:
            out.append({
                "key": "neb_cell_trend", "title": "NEB 셀 크기 추세 (1×1×1 → 2×2×2)",
                "value": f"{min(ratios):.2f}–{max(ratios):.2f}× 하락  ·  {len(ratios)}홉",
                "verdict": f"⭕ 예외 {sum(1 for x in ratios if x < 1.0)}/{len(ratios)}",
                "note": ("셀을 키우면 장벽이 **예외 없이 내려간다**. ⇒ 미수렴 NEB 가 수렴값보다 "
                         "**위에** 있으면 그건 값이 아니라 미수렴이다. `MIN_WIDTH_A=10 Å` 는 "
                         "**최소 요건이지 수렴 보증이 아니다**."),
                "limit": ("⛔ **UMA 장벽 절대값 인용 금지** — 용도는 경로 선택이다. 2점뿐이라 "
                          "수렴을 못 봤고, 끝점 비대칭이 큰 홉(⚠ 2건)은 끝점을 한 번만 이완한 "
                          "값이라 따로 재실행 대상이다."),
                "src": "db/properties/sei_neb_uma_scout.json"})
    return out


def _load_json_safe(rel: str):
    """repo 상대경로 json 을 읽는다. 없거나 깨지면 None (화면이 통째로 죽지 않게)."""
    p = ROOT / rel
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def elf_central_min() -> dict:
    """조성 → P–S 결합 **중앙 최솟값** ELF.

    ⚠ 판별력이 있는 건 midpoint 가 아니라 central_min 이다(CSV 머리 주석) —
      midpoint 는 짧은 결합에서 lone-pair 에 걸려 다 0.94 로 뭉친다.
    """
    f = DB / "properties" / "elf_bonds_3sys_origin.csv"
    if not f.exists():
        return {}
    out = {}
    for r in csv.DictReader(x for x in f.read_text(encoding="utf-8-sig").splitlines()
                            if not x.startswith("#")):
        cid = _ELF_SYS2CID.get((r.get("system") or "").strip().lower())
        if cid and (r.get("bond") or "").strip().upper() == "P-S":
            try: out[cid] = round(float(r["ELF_central_min"]), 3)
            except (TypeError, ValueError): pass
    return out


@lru_cache(maxsize=2)
def bader_charge(species: str = "P") -> dict:
    """조성 → Bader 净전하 (all-electron). 기본 P — 도펀트에 반응하는 자리다
    (Li 는 3계 모두 +0.88 로 불변이라 열로 쓰면 정보가 없다)."""
    out = {}
    for cid, fn in _BADER_FILES.items():
        f = DB / "properties" / fn
        if not f.exists():
            continue
        for r in csv.DictReader(x for x in f.read_text(encoding="utf-8-sig").splitlines()
                                if not x.startswith("#")):
            if (r.get("species_or_site") or "").strip() == species:
                try: out[cid] = round(float(r["bader_net_e"]), 3)
                except (TypeError, ValueError): pass
    return out


# 조성별 '어떤 분석을 갖고 있나' — **실물 파일**이 기준.
#   ⚠ 새 판정 규칙을 만들지 않는다. datafiles_for()/_csv_kind() 가 이미 prefix 별칭과
#     icohp↔cohp·phonon↔dos 순서 함정까지 처리한 정본이다 (거기에 맞춰야 조성 페이지의
#     'Charts' 탭 칩과 같은 말을 한다).
EXTRA_META = {
    "ELF_PS": "ELF 결합 **중앙 최솟값** (P–S) — QE pp.x plot_num=8. "
              "⚠ midpoint 는 짧은 결합에서 lone-pair 에 걸려 다 0.94 로 뭉친다(판별력 없음)",
    "BADER_P": "Bader 净전하, all-electron (P 자리) — Li 는 3계 모두 +0.88 로 불변이라 정보가 없다",
}
_ANALYSIS_ORDER = ["DOS", "PDOS", "ELF", "ICOHP", "COHP", "Bader", "Charge", "BVSE",
                   "MSD", "Arrhenius", "Diffusion", "NEB", "Barrier", "EOS", "Phonon", "XPS", "IR"]
ANALYSIS_WHY = {
    "DOS": "상태밀도 (fixed-occ nscf)", "PDOS": "원소분해 상태밀도",
    "ELF": "전자국재함수 — P–S 중앙 최솟값이 판별량",
    "ICOHP": "결합 세기 적분값 (LOBSTER)", "COHP": "결합 세기 곡선",
    "Bader": "원자별 净전하 (all-electron)", "Charge": "전하 밀도·분해",
    "BVSE": "결합원자가 에너지 지도 — ⚠ 순위·정량은 원본 주기셀 값만, 계 간 순위 인용 금지",
    "MSD": "평균제곱변위 (창 2–50 ps 고정)", "Arrhenius": "MLIP-MD 아레니우스 (600/800/1000 K)",
    "Diffusion": "확산계수", "NEB": "전이상태 장벽", "Barrier": "장벽",
    "EOS": "상태방정식 B₀", "Phonon": "포논 — 동역학 안정성", "XPS": "코어레벨", "IR": "적외",
}


def analysis_matrix() -> dict:
    """조성 → {분석종류: 파일수}. 숫자 하나로 못 줄이는 것(DOS·PDOS·ELF 곡선)을
    표에 억지 스칼라로 넣는 대신 '갖고 있나'로 맞춰 보여준다."""
    # canonical 앵커가 있으면 그 계산은 한 것이다 — comp1 처럼 결과가 **집계 JSON**
    # (electronic.json·eos.json·elastic.json)에 든 계는 CSV 만 보면 통째로 비어 보인다.
    CANON_TAG = {"gap_eV": "Gap", "B0_GPa": "EOS", "E_VRH_GPa": "탄성",
                 "ICOHP_PS": "ICOHP", "MD_Ea_eV": "MD"}
    out = {}
    for cid in COMPOSITIONS:
        kinds = {}
        for f in datafiles_for(cid):
            k = f.get("kind")
            if k and k != "data":
                kinds[k] = kinds.get(k, 0) + 1
        for prop, tag in CANON_TAG.items():
            if CANONICAL.get(prop, {}).get(cid) is not None:
                kinds.setdefault(tag, 0)          # 0 = 값은 있는데 CSV 는 따로 없다
        out[cid] = kinds
    return out


# ─────────────────────────────────────────────────────────────
# Cascade / ML 도핑 스크리닝 (AI 계산 기반) — UMA 상대 스크리닝 번들
# ─────────────────────────────────────────────────────────────
def canonical_values(cid: str) -> dict:
    """조성 하나의 canonical 값 — 잠정값(CANONICAL_PROVISIONAL_VALUES)도 채워 넣는다.
    잠정값은 템플릿에서 CANONICAL_PROVISIONAL 사유와 '잠정' 배지를 달고 렌더된다."""
    idx = CANONICAL_ENTRY
    out = {k: _display(v.get(cid), (idx.get((k, cid)) or {}).get("uncertainty"))
           for k, v in CANONICAL.items()}
    for (k, c), val in CANONICAL_PROVISIONAL_VALUES.items():
        if c == cid and out.get(k) is None:
            out[k] = val
    return out


# 상태 배지 표시안 — compare.html 의 SLAB 과 같은 어휘를 쓴다(화면마다 다른 말 금지).
_STATUS_BADGE = {
    "unreviewed_drift": ("미검토", "#b45309", "#fef3c7",
                         "원자료가 바뀌었는데 아직 검토 전이다. 순위·차트·레이더에서 제외됨."),
    "source_error":     ("출처오류", "#b91c1c", "#fee2e2",
                         "원자료를 못 읽었다 — 이 값은 stale 일 수 있다. 자동판정 제외."),
    "provisional":      ("잠정", "#7c3aed", "#f3e8ff", "정본이 아니다 — 자동판정 제외."),
    "source_pending":   ("출처미배선", "#6b7280", "#f3f4f6",
                         "원자료를 아직 못 가리킨다 — 검증되지 않은 값이다."),
    "superseded":       ("철회", "#b91c1c", "#fee2e2", "철회된 값이다."),
}


#: 게이트 문구는 canonical.gate_prefix() 가 **단일 출처**다 (2026-08-20 codex 동결감사).
#:   이전에는 이 파일에 사본이 있었고 compare.html·canonical.py·test_webapp.py 가 각자
#:   옛 의미("blocking_gate 있으면 미통과")를 들고 있었다. 어휘를 한 곳으로 모은다.
def _gate_prefix(e: dict) -> str:
    import canonical as _C
    return _C.gate_prefix(e)


def canonical_status_for(cid: str) -> dict:
    """조성 하나의 metric 별 상태 배지. 정본이면 항목이 없다(배지도 없다)."""
    out = {}
    for (metric, system), e in CANONICAL_ENTRY.items():
        if system != cid:
            continue
        st = e.get("status")
        b = _STATUS_BADGE.get(st)
        if not b:
            continue
        why = (f"등록 묶음 [{e['comparison_group']}]. " if e.get("comparison_group") else "") + b[3]
        why = _gate_prefix(e) + why
        if e.get("note"):
            why += " " + e["note"]
        out[metric] = {"status": st, "label": b[0], "fg": b[1], "bg": b[2],
                       "why": why[:400], "group": e.get("comparison_group")}
    return out


def sei_summary() -> dict:
    """SEI 분해상 캠페인 요약 — 갭 × 형성전위를 한 표로 (2026-08-07).

    ⚠ 두 축의 출처가 **다르다**: 갭은 우리 QE(fixed-occ nscf 고유값), 형성전위는
      MP(GGA/GGA+U) 대분배 위상도다. 한 표에 나란히 두되 화면에 그 사실을 적는다
      — 섞어 인용하면 안 된다 (CLAUDE.md 문헌·db 분리 규율).
    ⛔ Nd 3종의 갭은 status=rejected 다. 표에 값을 넣지 않고 사유만 남긴다.
    """
    import json as _j
    gp = ROOT / "db" / "properties" / "sei_electronic.json"
    vp = ROOT / "db" / "properties" / "sei_formation_voltage.json"
    if not gp.is_file():
        return {}
    G = _j.loads(gp.read_text(encoding="utf-8"))
    V = _j.loads(vp.read_text(encoding="utf-8")).get("results", {}) if vp.is_file() else {}
    # tag(li3po4g_mp-2878) → 표시명 · 형성전위 키
    NAME = {"licl": ("LiCl", "LiCl"), "li3po4": ("Li₃PO₄ (β)", "Li3PO4"),
            "li3po4g": ("Li₃PO₄ (γ)", "Li3PO4g"), "li2o": ("Li₂O", "Li2O"),
            "li2s": ("Li₂S", "Li2S"), "li3p": ("Li₃P", "Li3P"),
            "lindo2": ("LiNdO₂", "LiNdO2"), "nd2o3": ("Nd₂O₃", "Nd2O3"),
            "nd2s3": ("Nd₂S₃", "Nd2S3")}
    rows, rejected = [], []
    for tag, g in G.get("results", {}).items():
        # ★ status allowlist — denylist 는 새 status 가 생길 때마다 뚫린다.
        #   2026-08-12: status=='rejected' 만 걸러서 **retracted 인 −6.46 eV 가
        #   밴드갭으로 서빙되고 있었다**. 모르는 status 는 fail-closed 로 뺀다.
        _shown, _why_hidden = record_shown(g)
        if not _shown:
            rejected.append({"tag": tag, "name": tag, "mp": "",
                             "gap": g.get("gap"), "gap_rejected": True,
                             "why": g.get("reason") or f"status={_why_hidden}",
                             "vlo": None, "vhi": None, "vstatus": None, "decomp": ""})
            continue
        stem = tag.split("_mp")[0]
        disp, vkey = NAME.get(stem, (stem, stem))
        v = V.get(vkey, {})
        r = {"tag": tag, "name": disp, "mp": "mp-" + tag.split("mp-")[-1],
             "gap": None if g.get("status") == "rejected" else g.get("gap"),
             "gap_rejected": g.get("status") == "rejected",
             "why": g.get("do_not_cite") or g.get("dos_provenance_warning"),
             "vlo": v.get("stable_V_min"), "vhi": v.get("stable_V_max"),
             "vstatus": v.get("status"),
             "decomp": " + ".join(v.get("decomposition_products_above_window")
                                  or v.get("decomposition_products_at_min") or [])}
        (rejected if r["gap_rejected"] else rows).append(r)
    rows.sort(key=lambda x: -(x["gap"] or 0))
    return {
        "rows": rows, "rejected": rejected,
        "gap_method": G.get("method", ""),
        "figs": ["docs/figures/sei/sei_gap_ladder.png", "docs/figures/sei/sei_dos_pdos.png"],
        "csv": ["db/properties/sei_gap_ladder_origin.csv",
                "db/properties/sei_dos_panels_origin.csv"],
        "note": ("갭 = **우리 QE** fixed-occ nscf 고유값 (PBE — 넓은 갭에서 30–50% 과소, "
                 "**순위로만**). 형성전위 = **Materials Project** GGA/GGA+U 대분배 위상도. "
                 "★ 출처가 다르므로 두 축의 절대값을 섞어 인용하지 말 것."),
    }


def canonical_provenance_flags() -> dict:
    """(metric, system) → 출처 경고. **status 와 별개다.**

    ★ 왜 별도인가 (2026-08-07 Codex 6라운드 후속): `provenance_open` 은 **값이 틀렸다는
      뜻이 아니다** — 값은 정본 파일과 일치한다. 다만 그 값을 만든 실행을 파일로 재현할 수
      없다. 그래서 status 를 내리면 안 되고(순위·차트에서 빼면 과잉), 대신 **눈에 보이는
      표식**만 붙인다. validator 만 고치고 화면을 안 고치면 사이트에서는 여전히 무경고다.
    """
    out = {}
    for (metric, system), e in CANONICAL_ENTRY.items():
        po = e.get("provenance_open")
        if po:
            out[(metric, system)] = {"why": str(po)[:500]}
    return out


def sei_axes() -> dict:
    """협업자 요청 3축의 진행 상태. **뭐가 됐고 뭐가 남았나**를 대시보드가 직접 말한다."""
    import json as _j
    gp = ROOT / "db" / "properties" / "sei_electronic.json"
    vp = ROOT / "db" / "properties" / "sei_formation_voltage.json"
    np_ = ROOT / "db" / "properties" / "sei_neb.json"
    n_gap = 0
    if gp.is_file():
        try:
            n_gap = sum(1 for v in _j.loads(gp.read_text(encoding="utf-8"))
                        .get("results", {}).values()
                        if record_shown(v)[0] and v.get("gap") is not None)
        except (OSError, ValueError):
            pass
    n_v = 0
    if vp.is_file():
        try:
            n_v = sum(1 for v in _j.loads(vp.read_text(encoding="utf-8"))
                      .get("results", {}).values() if v.get("status") == "ok")
        except (OSError, ValueError):
            pass
    neb, neb_retracted, neb_reason = {}, False, None
    if np_.is_file():
        try:
            _nj = _j.loads(np_.read_text(encoding="utf-8"))
            neb = _nj.get("results", {})
            # ⛔ 2026-08-11 — 이 파일은 철회될 수 있다 (전하 규약 오류 + 끝점 미이완).
            #   철회본은 results 를 results_OLD_INVALID 로 옮겨 두므로 위 get 이 {} 가 되는데,
            #   그러면 대시보드가 "계산 중" 이라고 **거짓말**을 한다. 철회는 철회라고 말한다.
            neb_retracted = bool(_nj.get("retracted"))
            neb_reason = _nj.get("retraction_reason")
        except (OSError, ValueError):
            neb = {}
    n_neb = sum(1 for v in neb.values() if v.get("citable"))
    # ⛔ 2026-08-16 — citable 0 을 "계산 안 됐다" 로 읽히게 두면 안 된다. 셀 수렴 축을
    #   따로 세우면서 li2s·li3nd 가 provisional_single_cell 로 내려가 citable 이 0 이 됐는데,
    #   **경로 자체는 수치적으로 유효**하다. 두 수를 나란히 보여야 거짓말이 안 된다.
    n_neb_path_ok = sum(1 for v in neb.values()
                        if v.get("status") == "converged"
                        and v.get("Ea_effective_eV") is not None
                        and not v.get("blocking_checks"))
    return {"axes": [
        {"n": "① Li⁺ 확산장벽",
         "state": ("⛔ 철회 — 재계산 중" if neb_retracted else
                   ("완료" if n_neb >= 6 else "진행 중")),
         "done": (not neb_retracted) and n_neb >= 6,
         "detail": ("⛔ 기존 NEB 결과 전건 철회 (2026-08-11) — 재계산 대기. "
                    "협업자 요청 6종: Li₂O · Li₃PO₄γ · LiNdO₂ · LiCl · Li₂S · Li₃P"
                    if neb_retracted else
                    (f"DFT CI-NEB — 경로 수치 유효 {n_neb_path_ok}/6 · "
                     f"셀 수렴 확인 {n_neb}/6 (인용 가능)"
                     if neb else
                     "DFT CI-NEB 계산 중 (협업자 요청 6종)")),
         "why": ("BVSE 는 화학계를 넘나드는 비교에 못 쓴다 — 하필 Figure 5 의 주인공 "
                 "Li₂S(BVS 1.56)·LiCl(2.74)이 못 쓰는 쪽이고 Li₃P 는 파라미터가 없다. "
                 "그래서 NEB 이 대안이 아니라 유일한 경로다."
                 + (f"  ⛔ 철회 사유: {str(neb_reason)[:400]}" if neb_retracted else ""))},
        {"n": "② 형성 전위", "state": "완료", "done": True,
         "detail": f"{n_v}종 + 분해 산물 (MP 대분배 위상도)",
         "why": "열역학적 안정 구간이지 생성 속도가 아니다 — '이 전위 밖에서는 존재할 수 없다'로 읽는다."},
        {"n": "③ 밴드갭 + DOS/PDOS", "state": "완료", "done": True,
         "detail": f"{n_gap}종 (fixed-occ nscf 고유값) + Origin CSV·그림",
         "why": "⛔ Nd 3종은 제외 — 4f 를 원자가에 둔 PBE(+U) 의 SCF 해가 금속이라 "
                "fixed-occ 갭이 정의되지 않는다. MP frozen-4f 인용."},
    ], "neb": neb}


def canonical_status_all() -> dict:
    """(metric, system) → 배지. explorer 표처럼 전 조성을 한 번에 그리는 화면용."""
    out = {}
    for (metric, system), e in CANONICAL_ENTRY.items():
        b_ = _STATUS_BADGE.get(e.get("status"))
        if not b_:
            continue
        # ★ 등록 묶음 ID 를 툴팁 맨 앞에 (2026-08-07 Codex 6라운드) — 의미를 나눠 놓고도
        #   그 사실이 화면에 안 보이면 나눈 의미가 없다.
        why = (f"등록 묶음 [{e['comparison_group']}]. " if e.get("comparison_group") else "") + b_[3]
        why = _gate_prefix(e) + why
        if e.get("note"):
            why += " " + e["note"]
        out[(metric, system)] = {"status": e.get("status"), "label": b_[0],
                                 "fg": b_[1], "bg": b_[2], "why": why[:400],
                                 "group": e.get("comparison_group")}
    return out


def _display(value, unc=None):
    """표시용 반올림. **저장은 정밀, 화면은 유효자릿수** (2026-08-07 Codex 5라운드 권고).

    오차막대가 있으면 **그 자릿수에 맞춘다** — 0.2754597563 ± 0.0327 을 그대로 찍으면
    있지도 않은 정밀도를 주장하는 셈이다. 오차가 없으면 소수 4자리로 자른다.
    """
    if value is None:
        return None
    try:
        v = float(value)
    except (TypeError, ValueError):
        return value
    if unc:
        try:
            import math
            d = max(0, -int(math.floor(math.log10(abs(float(unc))))) + 1)
            return round(v, min(d, 6))
        except (TypeError, ValueError, OverflowError):
            pass
    r = round(v, 4)
    return int(r) if r == int(r) and abs(r) >= 1 else r


def canonical_table() -> dict:
    """explorer/compare 표용 — CANONICAL 전체 + 잠정값 병합. **표시용으로 반올림한다.**"""
    idx = CANONICAL_ENTRY
    out = {}
    for k, v in CANONICAL.items():
        out[k] = {c: _display(val, (idx.get((k, c)) or {}).get("uncertainty"))
                  for c, val in v.items()}
    for (k, c), val in CANONICAL_PROVISIONAL_VALUES.items():
        out.setdefault(k, {}).setdefault(c, _display(val))
    return out


CASCADE_FILES = {
    "ranked":      "cascade_v23_ranked.csv",       # 조성 합성점수 리더보드
    "champions":   "cascade_v23_champions.csv",    # 챔피언별 EOS·탄성·anneal
    "litransport": "cascade_v23_litransport.csv",  # Li 수송 프록시
    "synergy":     "cascade_v23_synergy_pairs.csv",# 공동도핑 시너지 가설
    "oxidation":   "oxidation_stability_cascade.csv",  # grand-potential ESW
}
#: 회수분 = **완주한 전체 90종 · 270 champion**. 2026-08-13 조사로 273 슬롯 중 270 이
#:  완주했음이 확인됐고(빠진 43종도 STAGE_12 까지), ESW 를 다시 돌려 90종을 채웠다.
#:  ⚠ 파생물의 완성도가 서로 다르다 — 아래 status 를 화면에 **그대로** 띄운다.
#:  근거: kb/methodology/cascade_pipeline_anatomy_2026_08_13.md
CASCADE_FILES_V2 = {
    "champions":   "cascade_v23_champions_v2.csv",
    "litransport": "cascade_v23_litransport_v2.csv",
    "oxidation":   "oxidation_stability_cascade_v2.csv",
    "ranked":      "cascade_v23_ranked_v2.csv",
}
CASCADE_V2_META = {
    # ⛔ 2026-08-14 Codex 감사 반영 — "90종 funnel" 은 과장이었다.
    #    ESW 는 90종이지만 gate 입력이 비면 조용히 빠진다: AlI₃ 전면 결측 → 랭킹·깔때기 89종.
    #    부분 결측종은 남은 라벨 평균으로 평가돼 있다. 화면은 이 구분을 그대로 쓴다.
    #: ⛔ 2026-08-14 두 번째 정정 (Codex P0-3). 옛 "부분 결측 18" 은 gate 가 **안 쓰는**
    #:  eos_B0_GPa 를 세고 실제로 쓰는 pugh 를 빼서 나온 허수였다. 바로잡으니 1종(MgI₂)이다.
    "headline": "90종 회수 → 89종 평가 가능 (완전 88 · 부분 결측 1 MgI₂ · 전면 결측 1 AlI₃)",
    "scope": "완주한 전체 90종 · 270 champion (273 슬롯 중 270 완주; As₂S₃ 3건은 stage-01 seed 실패)",
    #: ✅ 2026-08-14 해소 — 빌더가 풀 크기를 하드코딩하던 것을 NP 로 바꿔 두 판을 다시 만들었다.
    #:  그 과정에서 47종 문안이 숨기고 있던 사실 하나가 드러났다(아래 recovered_facts).
    "inherited_text_warning": ("✅ v2 JSON 의 description·honesty_header·source_files 는 2026-08-14 에 "
                               "풀 크기 연동으로 재생성됐다 — 더 이상 '47종' 문안을 물려받지 않는다. "
                               "각 JSON 의 status 필드로 지위를 구분한다 "
                               "(superseded_47species / recovered_unvalidated_diagnostic)."),
    #: 회수 후 **판정이 뒤집힌** 서술. 47종 문안을 그대로 뒀으면 계속 틀린 채로 남았을 것들.
    "recovered_facts": [
        ("⛔ 철회 — Na₂S 연성", "2026-08-14 오전에 내가 '90종에서는 Na₂S 가 B/G 2.50 으로 연성 경험칙을 "
                          "넘는다' 고 올렸다. **틀렸다** (Codex 재감사에서 잡힘). 두 겹의 잘못이었다: "
                          "① `Na2S_x100` 은 **B_hill = −36.27 GPa** — 음의 체적탄성률, 즉 탄성 계산 "
                          "실패 행인데 3점 평균에 들어갔다. ② 그 평균을 역수 취했는데 1/mean(G/B) 는 "
                          "mean(B/G) 가 아니다. 실패 행을 빼면 Na₂S 는 **B/G 1.22** 이고 "
                          "'89종 어느 것도 1.75 를 못 넘는다' 가 다시 참이다. "
                          "생성기(`plot_cascade_insights.py`)에 B_hill·G_hill ≤ 0 차단을 넣었다 — "
                          "270행 중 이 한 행이 유일한 비물리 행이다."),
        ("결측 규모", "옛 감사가 말한 '부분 결측 18종' 은 **허수**였다 — gate 가 안 쓰는 eos_B0_GPa 를 "
                  "세고 실제로 쓰는 pugh 를 빼서 나온 수다. 바로잡으면 부분 결측은 **MgI₂ 1종**이고 "
                  "88종이 완전하다 (Codex 리뷰 P0-3)."),
        ("G4 라벨", "'Li 수송 유지' 라는 게이트 이름을 폐기했다. 입력은 legacy BVS(Adams-2003) + "
                  "4 Å foreign-center count 두 정적 프록시뿐이고 MD·NEB 는 하나도 안 들어갔다."),
    ],
    "why": ("정본 47종은 물리 판정이 아니라 **취합 경계**였다. 등록이 2026-06-29 에 멈췄고 "
            "계산은 7-11 에 끝났다. 빠져 있던 43종도 STAGE_12 까지 완주해 있었다."),
    "recovered_on": "2026-08-13",
    "status": {
        # 축별 완성도를 다르게 표시한다 — 89종 파생을 90종 최종판처럼 보이게 하지 않는다.
        "raw":       ("complete",   "90종 원자료 (champions · litransport) — 270 champion 전수 회수"),
        # ★ 2026-08-16 — phase_set_id 를 싣고 host 를 같은 실행에서 재면서 method 비교는
        #   270/270 으로 닫혔다. 대신 **효과 귀속**이 열려 있다 (Codex f9 재감사).
        "oxidation": ("partial",    "**record-complete 90 · phase-set comparable 270/270 · 효과 귀속 0/17.** "
                                    "candidate 와 host 를 같은 실행·같은 pinned entry set 에서 재고 "
                                    "phase_set_id 를 기록해 method 비교는 닫혔다. 그러나 챔피언 270행 중 "
                                    "17행이 compound_set_chain generator 산물이고 그중 10행만 plain 형제와 "
                                    "정확히 ΔLi=-1·ΔS=-1·ΔCl=+1 이다 — 7행(B₂O₃·MoO₃·WO₃)은 치환 자리와 "
                                    "Li/P 까지 다르다. 회수 270 반응 중 124건에 LiS4 가 있고 빼면 host onset 이 "
                                    "2.140 → 2.256 V — 'complete · 그대로 사용 가능' 이 아니다"),
        "ranked":    ("incomplete", "89 of 90 — 완결성은 사실상 해결(완전 88 · 부분 1 MgI₂). "
                                    "AlI₃ 만 champion(rank_combined==1) 에 gate 입력이 없다. "
                                    "⛔ 남은 blocker 는 결측이 아니라 **점수의 타당성**이다 — score_blockers 참조"),
        "funnel":    ("partial",    "89종 waterfall 89–89–84–45–28–1 (47종판 47–47–43–25–11–1). "
                                    "⛔ 게이트 정의 자체가 미해결: G4 순환(blocking 이 BVS 를 덮어씀) · "
                                    "G5 median 컷이 로스터 의존 · G3 phase set 미기록"),
        "figures":   ("partial",    "docs/figures/cascade_v2/ — insights 1종만 재생성, 나머지 18종 대기"),
    },
    #: ESW 의 재현성 한계 — **v2 회귀가 아니라 v1·v2 공통**이다 (Codex 리뷰 지적 확인).
    "esw_limits": ("반응식은 화학식 문자열로만 남고 **경쟁상의 mp-ID·MP 스냅샷 버전이 기록돼 있지 않다**"
                   " (v1 141건·v2 270건 모두 같은 필드셋). 같은 onset 을 다시 만들려면 MP 를 다시 "
                   "질의해야 하고, 그 사이 hull 이 바뀌면 값이 달라질 수 있다 — 재현 가능한 인용을 "
                   "하려면 entry id 를 남기도록 esw_cascade_batch.py 를 고쳐 다시 돌려야 한다."),
    #: ⛔ "왜 90종 랭킹을 확정 안 하나" 에 대한 답 — 결측이 아니라 **점수**가 막고 있다.
    "score_blockers": [
        ("G4 순환", "blocking 컷 탈락자는 transport_norm 이 0.05 로 강제돼 BVS 값이 버려진다. "
                  "두 독립 신호의 AND 가 아니라 한 신호가 다른 신호를 덮어쓴 합성값이다."),
        ("G5 로스터 의존", "기계 게이트가 median 컷이라 **풀이 바뀌면 문턱이 같이 움직인다.** "
                       "47종 판과 89종 판의 G5 통과자를 같은 기준으로 비교할 수 없다."),
        ("가중치 수작업", "score = 0.30·ox + 0.25·stable + 0.20·soft + 0.15·ductile + 0.10·window 는 "
                     "물리에서 유도한 값이 아니라 손으로 정한 값이다. soft+ductile 0.35 는 "
                     "'연질일수록 좋다'는 단조 가정인데 bucci2017 이 반증한다."),
        ("ox_V 축퇴", "호스트 S²⁻ 가 onset 을 pin 해서 여러 종이 같은 ox_V 로 뭉친다 — 변별력이 낮다."),
        ("절대값 부풀림", "UMA 탄성이 실험(AFM/UPE 12–22 GPa) 대비 높다. 캐스케이드 내부 상대비교만 유효."),
    ],
    #: 90종 waterfall 에서 **판정이 아닌 이유로** 통과한 종. 화면에 반드시 병기한다.
    "artifacts": {
        "Li2S": "blocking = 0.0 (구성 원소가 전부 host Li/P/S/Cl → dopant 원자 0개). 판정 아님",
        "LiCl": "blocking = 0.0 (동일 사유). 판정 아님",
    },
    "funnel_v2": {
        "waterfall": [89, 89, 84, 45, 28, 1],
        "canonical": [47, 47, 43, 25, 11, 1],
        "endpoint_n": 28,
        "endpoint": ["Ag2O", "AlCl3", "CaCl2", "CaF2", "CaO", "CaS", "CrCl3", "Ga2S3",
                     "GeS2", "Li2O", "Li2S", "LiBr", "LiCl", "LiF", "LiI", "MgCl2",
                     "MgF2", "MgO", "MgS", "MoO3", "ScCl3", "SiO2", "SiS2", "SnO2",
                     "SnS2", "WO3", "YCl3", "ZnO"],
        "gate_power": {"G1": (0, 0), "G2": (5, 0), "G3": (44, 5), "G4": (36, 7)},
        "note": ("G1 은 90종에서도 0종 탈락 — vacuous 판정 유지. G2 도 unique kill 0. "
                 "G3·G4 만 고유 기여가 있다 (각 5 · 7종). "
                 "⚠ G4 의 36종 탈락은 blocking kill 과 bvs kill 이 섞인 수다 — 순환 때문에 "
                 "분리해서 인용해야 한다 (funnel JSON 의 G4 selection_pressure 블록)."),
    },
    #: AlI₃ 를 90번째로 넣을 수 있는 유일한 경로 — **비-champion 대체**. 쓰려면 명시해야 한다.
    "ali3_fallback": ("AlI₃ 는 rank_combined==1 (champion) 행에 탄성·EOS·BVS 가 없지만 "
                      "**rank_combined==2 행에는 전부 있다**(E 45.05·43.60·42.21 GPa, B0 20.98·17.04·18.03). "
                      "그 행으로 대체하면 90/90 이 되지만, 다른 종은 champion 인데 AlI₃ 만 2위 배치가 되어 "
                      "**동일 기준 비교가 깨진다.** 쓰려면 표에 그 사실을 병기할 것. "
                      "(같은 상황인 다른 종은 La₂O₃+Clrich 변형 하나뿐 — 종 수준에선 AlI₃ 단 1건.)"),
    "downloads": [
        ("db/properties/cascade_v23_all.csv",                "전체 원자료 (90종 · 3615행 · 102열)"),
        ("db/properties/cascade_v23_champions_v2.csv",       "champion 270행"),
        ("db/properties/cascade_v23_litransport_v2.csv",     "G4 정적 프록시 270행 (BVS + 4 Å blocking) ⚠ 전도도 아님"),
        ("db/properties/oxidation_stability_cascade_v2.csv", "grand-potential ESW 90종"),
        ("db/properties/oxidation_stability_cascade_v2.json","ESW 원본 (분해 반응식 포함, 270 champion)"),
        ("db/properties/cascade_v23_ranked_v2.csv",          "합성점수 랭킹 89종 ⚠ 점수 타당성 미해결 (score_blockers)"),
        ("db/properties/cascade_v23_all_20260629_47species.csv", "옛 47종 판 (2026-06-29, 대조용)"),
        ("db/properties/cascade_pool_audit_v2.json",          "완결성 감사 (전면/부분 결측 판정)"),
    ],
    "caveat": ("⚠ 89종 랭킹을 90종 최종판으로 인용하지 말 것. 다만 **막고 있는 것은 결측이 아니다** — "
               "완결성은 완전 88 · 부분 1 · 전면결측 1 로 사실상 해결됐고, 남은 blocker 는 "
               "게이트·점수의 타당성이다 (score_blockers). 원자료와 ESW 는 90종 전수라 그대로 쓸 수 있다."),
}
#: ── 파이프라인 실측 — 화면 최상단 수치의 **유일한 출처** ────────────────────
#:  2026-08-14 개정. 이전 화면은 "47 랭킹 / 4 Pareto / 141 champion / 14 verified" 를
#:  최신 승인 결과처럼 띄웠는데, 그건 2026-06-29 에 멈춘 **취합 경계**의 숫자였다.
#:  근거: kb/methodology/cascade_pipeline_anatomy_2026_08_13.md
#: ⛔ 2026-08-14 (Codex 리뷰 P1) — 예전엔 이 네 수가 여기 하드코드였다. 그건 "정본" 이
#:  아니라 또 하나의 사본이다. 지금은 **manifest 에서 파생**하고, manifest 가 없거나
#:  status 어휘 밖의 값이 있으면 화면을 fail-closed 한다.
CASCADE_MANIFEST_PATH = DB / "properties" / "cascade_audit_manifest.json"
_MANIFEST_STATUS = ("historical", "recovered_unvalidated", "approved",
                    "superseded", "invalid", "audit_current")
_MANIFEST_USE_SCOPE = ("default_visible", "archive_only", "diagnostic_only", "blocked")

CASCADE_TRUTH_LABELS = {
    "planned_slots":        ("계획 슬롯", "91종 PLANNED INPUT ROSTER × 3 라벨 — shortlist 아님"),
    "completed_slots":      ("완주 슬롯 (enabled-workflow)", "As₂S₃ 3건만 stage-01 seed 생성 실패"),
    "completed_species":    ("완주 종", "ESW 회수분에서 센다 — 91종 중 90종"),
    "historical_snapshot_species": ("역사 스냅샷", "2026-06-29 취합 경계. 재현 가능하나 superseded"),
    "approved_current_leaderboard_species": ("승인된 ranking", "결측이 아니라 점수·게이트 타당성이 미해결"),
    "explicit_pair_property_labels": ("explicit pair 라벨", "두 도펀트를 함께 넣고 계산한 셀 = 0"),
}
CASCADE_TRUTH_WHY_ZERO = (
    "승인 0 은 '실패' 가 아니라 **현재 상태의 정확한 이름**이다. 47종 리더보드는 "
    "계산이 덜 끝난 시점의 취합 경계였고, 89종 재랭킹은 게이트 정의(G4 순환 · G5 로스터 "
    "상대 · G3 phase set 미기록)가 닫히기 전의 진단물이다. 어느 쪽도 '우리 스크리닝 결과' "
    "로 인용할 수 없다.")


def load_cascade_manifest() -> dict:
    """artifact manifest. 없거나 status 어휘가 어긋나면 `ok=False` 로 fail-closed."""
    m = _load_json(CASCADE_MANIFEST_PATH) or {}
    problems = []
    if not m:
        problems.append("manifest 파일이 없다 — tools/cascade/rebuild_pool_inputs.py 로 생성할 것")
    for a in m.get("artifacts", []):
        # ⚠ 2026-08-14 — 필드가 `status` → `approval_status` 로 갈렸다 (릴리스 지위와
        #   artifact 승인 지위를 나눈 결과). 옛 이름을 폴백으로 두면 조용히 통과하므로 안 둔다.
        if a.get("approval_status") not in _MANIFEST_STATUS:
            problems.append(f"{a.get('source_path')}: 알 수 없는 approval_status "
                            f"{a.get('approval_status')!r}")
        if a.get("use_scope") not in _MANIFEST_USE_SCOPE:
            problems.append(f"{a.get('source_path')}: 알 수 없는 use_scope {a.get('use_scope')!r}")
    # sha256/rows 대조 — 파일이 바뀌었는데 manifest 가 안 따라오면 stale 이다.
    import hashlib
    stale = []
    for a in m.get("artifacts", []):
        p = ROOT / (a.get("source_path") or "")
        if not p.is_file():
            stale.append((a.get("source_path"), "파일 없음")); continue
        b = p.read_bytes()
        if hashlib.sha256(b).hexdigest() != a.get("sha256"):
            stale.append((a.get("source_path"), "sha256 불일치 — manifest 재생성 필요"))
    m["_problems"], m["_stale"] = problems, stale
    m["ok"] = not problems and not stale
    return m


def cascade_truth() -> dict:
    """화면 타일. manifest 가 정상일 때만 값이 나오고, 아니면 빈 dict (fail-closed)."""
    m = load_cascade_manifest()
    if not m.get("ok"):
        return {"ok": False, "problems": m.get("_problems", []), "stale": m.get("_stale", []), "tiles": []}
    h = m.get("headline", {})
    return {
        "ok": True,
        "tiles": [(k, h[k], *CASCADE_TRUTH_LABELS[k]) for k in CASCADE_TRUTH_LABELS if k in h],
        "basis": m.get("headline_basis", ""),
        "why_zero": CASCADE_TRUTH_WHY_ZERO,
        "actual_x": m.get("actual_x"), "actual_x_note": m.get("actual_x_note", ""),
        "host": m.get("host", {}),
        "artifacts": m.get("artifacts", []),
    }
#: 감사 5축 — 기본 화면으로 승격한다 (전에는 90종 탭 안에만 있었다).
#:  라벨은 CASCADE_V2_META['status'] 의 (등급, 문장) 을 그대로 쓴다.
CASCADE_AUDIT_AXES = ["raw", "oxidation", "ranked", "funnel", "figures"]
#: ── G4 분해 — 화면에서 "Li transport" 라는 이름을 **쓰지 않는다** ──────────
#:  그 이름이 이온전도 측정처럼 읽혔다. 실제 입력은 아래 두 정적 프록시뿐이다.
G4_DECOMP = {
    "old_name": "Li transport",
    "why_renamed": ("'Li 수송' 은 전도도·확산을 잰 것처럼 읽힌다. G4 에 들어가는 값은 "
                    "**어닐 기하 위에서 계산한 정적 프록시 두 개**이고, 둘 다 이온이 "
                    "움직이는 계산이 아니다. MD·NEB 는 이 축에 하나도 안 들어갔다."),
    "gate": "G4 = transport_norm > 0.30  (blocking 은 그 안에 이미 접혀 있다 — 아래 순환 참조)",
    #: ⛔⛔ 2026-08-14 (Codex 리뷰 P0-5) — G4 는 **독립 두 신호의 AND 가 아니다.**
    #:  build_screening_funnel.py:139-142 가 blocking 컷을 통과 못 하면 BVS 값을 버리고
    #:  transport_norm 을 GATE_FLOOR(0.05)로 **강제**한다. TRANSPORT_CUT 이 0.30 이므로
    #:  blocking 탈락 = G4 탈락이 결정론적으로 따라온다.
    "circularity": {
        "code": "if blocking < 0.60:  n = 0.05+0.05 + n*(1-0.05-0.05)\nelse:              n = 0.05   # ← BVS 값 폐기",
        "why_it_matters": ("blocking 에서 떨어진 종의 transport_norm 은 **전부 정확히 0.05** 다 — "
                           "BVS 가 아무리 좋아도 같은 값이 된다. 그래서 '두 개의 독립적인 수송 신호가 "
                           "일치했다'(예: 6/6 trade-off)로 읽으면 안 된다. 한 신호가 다른 신호를 "
                           "덮어쓴 뒤의 합성값이다."),
        "consequence": "G4 탈락 사유를 인용할 때는 blocking kill / bvs kill 을 반드시 분리할 것.",
    },
    "inputs": [
        {
            "col": "bvs_li_proxy_score",
            "name": "legacy BVS (Adams-2003 파라미터)",
            # ⛔ P0-6 — 'x005' 는 **디렉터리 라벨**이고 실제 치환율이 아니다.
            "what": "어닐 후 기하에서 Li 자리의 bond-valence sum. transport_norm = min–max(이 값 @라벨 x005). "
                    "⚠ 라벨 x002/x005/x010 은 셋 다 **실측 x = 0.25** 로 뭉개져 있다 (dualx_v23 실측). "
                    "'x=0.05 에서 쟀다'는 서술은 틀렸다.",
            "warn": ("⛔ **정본 BVSE 와 다른 파라미터다.** cascade 는 tools/doping/bvse_proxy.py 의 "
                     "Adams-2003 값(R₀ Li–S 1.94 · Li–Cl 1.91 · b_S 0.40)을 쓰고, 우리 정본은 "
                     "softBV(R₀ S 2.105 · Cl 2.249 · O 1.466 · b 0.37)다. "
                     "**이 값을 comp1 BVSE 결과와 같은 표에 올리면 안 된다.**"),
        },
        {
            "col": "tier2_dopant_blocking_fraction",
            "name": "4 Å foreign-center 프록시",
            "what": "도펀트 원자 4 Å 안에 있는 Li 의 비율. 순수 기하 count 이고 장벽·경로가 아니다.",
            "warn": ("⛔ 도펀트 **원자 수에 거의 비례**한다 — 물성이 아니라 농도의 대리값에 가깝다. "
                     "그래서 host 원소만 든 종(Li₂S·LiCl)은 도펀트 원자가 0개라 "
                     "**blocking = 0.0 으로 자동 통과**한다. 판정이 아니다."),
        },
    ],
    "not_measured": ["MD 확산계수 D", "CI-NEB 이동장벽 E_m", "Nernst–Einstein σ", "임피던스"],
}
CASCADE_META = {
    "title": "Doping Cascade — AI 계산 기반 도핑 스크리닝 (UMA)",
    # ⛔ 2026-08-14 정정 (Codex 리뷰 P0-7). 옛 문구는 "Model C (Li₅.₄PS₄.₄Cl₁.₆) 기반 … x=0.25" 였다.
    #    ESW 반응식 좌변이 Li22P4(S5Cl)4 계열 = **Cl:P = 1.0** 이라 Model C(Cl 1.6)가 아니다.
    #    그리고 x002/x005/x010 은 라벨일 뿐 실측은 셋 다 x=0.25 다 (P0-6).
    "scope": ("Li₆PS₅Cl 계열 아지로다이트 호스트(Cl:P = 1.0, ESW 반응식 좌변 실측) 위의 "
              "산화물·할로겐화물·황화물 도펀트 91종 스크리닝. 농도 라벨 x002/x005/x010 은 "
              "셋 다 실측 x = 0.25 — Model C(Cl₁.₆) 가 아니고 x=0.05 도 아니다"),
    "engine": "UMA-s-1p1 (task=omat) · anneal→champion→EOS/elastic/ESW/Li-proxy 캐스케이드",
    "score_formula": "score = 0.30·ox + 0.25·stable + 0.20·soft + 0.15·ductile + 0.10·window (min–max 정규화)",
    "caveat": "절대 탄성값은 실험(AFM/UPE 12–22 GPa) 대비 높게 나옴 — 캐스케이드 내부(UMA-vs-UMA) 순위·상대비교만. EOS B0 ≠ elastic B_VRH.",
    "verified": "doping_cascade_verified.json 은 UMA-내부(EOS·elastic·anneal) 수렴 감사 서브셋 (상위 후보 41종 all-converged, DFT 검증 아님) — DFT 심층검증은 Nd₂O₃·B₂O₃ 2건뿐.",
}
# 조성 노드 ↔ 캐스케이드 도펀트 (스크리닝 히트의 DFT 심층검증)
CASCADE_DOPANT = {"modelc_nd_doped": "Nd2O3", "b2o3": "B2O3"}

# ⛔⛔ 2026-08-16 (Codex f9 재감사 P0-3) — **도펀트 이름은 조성이 아니다.**
#   위 표는 조성 페이지와 캐스케이드 챔피언을 라벨로 잇는다. B2O3 에서 그 둘은
#   서로 다른 조성이다:
#       DFT-deep 페이지  Li58 P8 S41 Cl16 B2 O3   onset 2.03  V (host 아래)
#       cascade 챔피언   Li17 B2 P4 S16 Cl5 O3    onset 2.317 V (host 위)
#   그래서 "스크리닝이 고른 조성의 DFT 심층검증" 이라고 쓰면 거짓이다. 링크는 남기되
#   (다음 계산 대상 선정에 쓰인다) **validation 이라고 부르지 않는다.**
#   validation 으로 인정하려면 composition_formula + composition_hash + method_id +
#   phase_set_id 가 모두 일치해야 한다.
# ── 2026-08-16 세미나 최종 핸드오프 (17d9a373) ───────────────────────────────
#   G3 상태는 **네 층**이다. 하나로 합치면 곧바로 자기모순이 생긴다 (실제로 생겼었다).
CASCADE_G3_STATE = {
    "phase_set_comparable": "270/270",
    "operational_factorial_coverage": "17/17 chain rows · 11 recipe systems",
    "structural_realization_validated": "0/11",
    "approved_current_ranking": 0,
    "allowed": ["phase-set comparable 270/270",
                "17/17 chain rows have formula-level operational contrasts "
                "across 11 recipe systems"],
    "forbidden": ["effect attribution closed", "11/11 species validated",
                  "current G3 ranking approved", "Cl effect = 0"],
}

#: matched 2×2 — 값은 db 가 원본이고 여기엔 **설계와 문구**만 둔다.
CASCADE_FACTORIAL_CONTRACT = {
    "cells": {"H_plain": "Li24P4S20Cl4", "H_Cl": "Li23P4S19Cl5",
              "D_plain": "Li18M2P4S17Cl4O3", "D_Cl": "Li17M2P4S16Cl5O3"},
    "contrasts": {
        "baseline_cl_recipe_contrast": "H_Cl − H_plain   (도펀트 없는 기준)",
        "plain_dopant_recipe_contrast": "D_plain − H_plain",
        "conditional_cl_recipe_contrast": "D_Cl − D_plain   (도펀트가 있을 때)",
        "recipe_interaction": "conditional − baseline",
    },
    "caveats": [
        "11 expanded rosters 는 **독립 host 실험 11개가 아니다** — 같은 두 조성의 반복이다",
        "total 이 historical chain delta 와 일치하는 것은 **round-trip consistency** 다",
        "actual structure/site validation 은 **0/11** 이다",
        "'main effect' 가 아니라 recipe contrast 다 — 원소 수준 인과를 함의하지 않는다",
    ],
}

#: 두 enrichment 비율 — 반드시 분모와 non-causal 라벨을 붙여 같은 패널에.
CASCADE_ENRICHMENT = {
    "full_pool": {"plain": "17/253", "chain": "11/17", "ratio": 9.63,
                  "denominator_note": "chain 후보가 없던 237 슬롯도 분모에 들어 있다"},
    "eligible_slots": {"plain": "4/16", "chain": "11/17", "ratio": 2.59,
                       "denominator_note": "chain 후보가 실제 있던 33 슬롯만"},
    "label": "post-selection descriptive association",
    "why_not_causal": ("챔피언은 combined_score 최대값으로 **사후 선택**됐고, "
                       "x 라벨은 독립 반복이 아니다 (270행 전부 loading 0.25)."),
    "never_call_it": ["Cl effect size", "causal enrichment", "success rate"],
}

#: 20 스테이지 해설 — 네 그룹. stage_status 와 gate_status 를 한 enum 으로 합치지 않는다.
CASCADE_STAGE_GROUPS = [
    {"id": "00-04", "name": "Generate and anneal",
     "question": "라벨 하나를 어닐된 후보군으로 바꿀 수 있는가",
     "input_output": "parent structure + dopant recipe → 후보 구조 · post-anneal geometry/energy",
     "cost_class": "저비용 (UMA relax 1500 step · 500 K 50 ps FIRE)",
     "why_before_next": "비싼 정적/유한변형 계산에 넣기 전에 후보 수를 줄인다",
     "cannot_claim": "열역학적 formation energy · DFT 검증 · 전도도",
     "warnings": ["01: COMPOUND_FILTER 누락 시 ~85종 전수 열거 = 5000+ 구조"]},
    {"id": "05-08", "name": "Static pathway and mechanics",
     "question": "어닐된 기하에서 Li 환경과 역학이 어떻게 보이는가",
     "input_output": "post-anneal 구조 → legacy BVS · 4 Å blocking · EOS B0 · Cij",
     "cost_class": "중간 (유한변형 계산)",
     "why_before_next": "정적 프록시로 걸러 비싼 MD/계면 계산의 순서를 정한다",
     "cannot_claim": "장시간 Li 확산 · 실제 BVSE barrier · 전자절연성 · 계면 접착",
     "warnings": ["05: post-anneal geometry 를 쓴다 (BVS 는 결합길이에 지수민감) · "
                  "legacy/noncanonical BVS · **전도도가 아니다**"]},
    {"id": "09a-09f", "name": "Assemble and propose",
     "question": "모은 자료로 다음 계산을 무엇으로 제안할 것인가",
     "input_output": "스테이지 산출물 → combine/collect · predictor · dft_inputs · ehull",
     "cost_class": "저비용 (조립)",
     "why_before_next": "후보를 검증하는 단계가 아니라 **자료를 조립**하는 단계다",
     "cannot_claim": "후보 검증 · current G2/G3 source",
     "warnings": ["09f: **NOT A TRUE GRAND-POTENTIAL ESW** — current G3 는 pipeline 밖의 "
                  "esw_cascade_batch.py 가 pinned MP roster 에서 다시 계산한 값이다",
                  "09e: decomposition audit 이지 후보 E_above_hull 이 아니다",
                  "09d: dft_inputs 존재는 DFT 완료가 아니다"]},
    {"id": "10-12b", "name": "Expensive tail and final collection",
     "question": "가장 비싼 축을 돌고 최종 수집을 했는가",
     "input_output": "TOP_K_SIGMA 후보 → σ MD · W_ad → collect_final · train_final",
     "cost_class": "최고 (σ MD ≈12 h · W_ad 5–15 h)",
     "why_before_next": "여기가 실제 물성 검증 꼬리다",
     "cannot_claim": "v23 에서는 아무것도 — 10·11 이 안 돌았다",
     "warnings": ["10: **NOT RUN · 0/270** (TOP_K_SIGMA=0, STAGE_10.DONE 0개)",
                  "11: **NOT RUN · 0/270** (STAGE_11.DONE 0개)",
                  "12/12b 의 'final' 은 모든 물리축이 계산됐다는 뜻이 아니다"]},
]

#: 스테이지 ↔ 게이트는 **다른 체계**다. 매핑을 따로 둔다.
CASCADE_STAGE_GATE_MAP = [
    ("G1", "historical input ← stage 06 rerank"),
    ("G2 / G3 (current)", "**pipeline 밖** — esw_cascade_batch.py 가 pinned MP roster 에서. "
                          "stage 09f 가 아니다"),
    ("G4", "legacy input ← stage 05 BVS + geometry-derived 4 Å proximity"),
    ("G5", "legacy input ← stage 08 elastic"),
    ("—", "09a–d = aggregation/predictor/input prep · 09e = decomposition audit · "
          "10/11 = intended validation tail, v23 미실행"),
]

CASCADE_JOIN_STATUS = {
    "b2o3": {
        "validation_link_status": "different_composition",
        "composition_match": False,
        "phase_set_match": "unverified",
        "method_family_match": "reported",
        "dft_deep_formula": "Li58P8S41Cl16B2O3",
        "dft_deep_ox_V": 2.03,
        "cascade_formula": "Li17B2P4S16Cl5O3",
        "cascade_ox_V": 2.317,
        "cascade_generator_variant": "compound_set_chain",
        "cascade_substitution_site": "Li_24g",
        "host_ox_V": 2.14,
        "why": ("도펀트 라벨만 같고 조성이 다르다. legacy DFT 기록에는 phase_set_id·entry_ids·"
                "MP 버전이 없어 같은 경쟁상 집합이었다는 증거도 없다 — 부호 반전은 관측됐지만 "
                "원인을 조성 하나로 확정할 수 없다."),
    },
    "modelc_nd_doped": {
        "validation_link_status": "same_family_unverified",
        "composition_match": None,
        "phase_set_match": "unverified",
        "method_family_match": "reported",
        "cascade_formula": "Li18Nd2P4S17Cl4O3",
        "cascade_ox_V": 1.92,
        "cascade_generator_variant": "compound_set",
        "why": ("chain 변형이 아니라 plain 챔피언이라 조성족 혼동은 없다. 다만 DFT 셀과 "
                "캐스케이드 조성이 같다는 것도 아직 조성식 대조로 확인하지 않았다."),
    },
}


def load_factorial() -> dict:
    """matched 2×2 두 판(LiS4 포함/제외)을 같이 읽는다.

    ⚠ 두 판은 **다른 phase set** 이다 (host 2.140 vs 2.256). 절대 onset 을 섞지 않도록
      roster 를 값과 함께 돌려준다.
    """
    import json as _j
    out = {}
    for key, fn in (("included", "oxidation_matched_factorial.json"),
                    ("excluded", "oxidation_matched_factorial_nolis4.json")):
        p = ROOT / "db" / "properties" / fn
        if not p.is_file():
            continue
        try:
            d = _j.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        out[key] = {"exclusions": d.get("exclusions") or [],
                    "ladder_steps": d.get("ladder_steps") or 0,
                    "decomposition": {k: v for k, v in (d.get("decomposition") or {}).items()
                                      if v.get("complete")},
                    "ladder": sorted(
                        ({"cell": k.split("/")[-1],
                          "formula": r.get("formula"),
                          "ox_V": r.get("oxidation_limit_V"),
                          "rxn": r.get("oxidation_onset_rxn")}
                         for k, r in (d.get("results") or {}).items()
                         if "ladder" in k and "error" not in r),
                        key=lambda x: x["cell"]),
                    "source": fn}
        # 사다리는 종마다 중복 기록된다 (같은 host 칸) — cell 이름으로 유일화
        seen, uniq = set(), []
        for row in out[key]["ladder"]:
            if row["cell"] in seen:
                continue
            seen.add(row["cell"]); uniq.append(row)
        out[key]["ladder"] = uniq
    return out


def load_cascade() -> dict:
    out = {"meta": CASCADE_META, "truth": cascade_truth(), "g4": G4_DECOMP,
           "audit_axes": CASCADE_AUDIT_AXES}
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
    # 🔁 회수분 (완주한 전체 90종 · 270 champion). 정본 47종과 **나란히** 싣고,
    #    축별 완성도(status)를 그대로 노출한다 — 89종 파생을 최종판처럼 보이게 하지 않는다.
    v2 = {"meta": CASCADE_V2_META, "present": False}
    for k, fn in CASCADE_FILES_V2.items():
        if (DB / "properties" / fn).exists():
            v2[k] = read_csv(f"properties/{fn}")
            v2["present"] = True
    v2["funnel"] = _load_json(DB / "properties" / "cascade_screening_funnel_v2.json")
    v2["themes"] = _load_json(DB / "properties" / "cascade_v23_themes_v2.json")
    # 완결성 감사 — 화면은 "90종 funnel" 이 아니라 이 판정(전면/부분 결측)을 표시한다.
    v2["audit"] = _load_json(DB / "properties" / "cascade_pool_audit_v2.json")
    #: 게이트별 완결성 (Codex 2026-08-14 인계). 내 단일 88/1/1 보다 정밀하다 —
    #:  축마다 분모가 다르고, G3 는 "onset 90건 있으나 method-complete 0" 을 구분한다.
    v2["gate_completeness"] = read_csv("properties/cascade_audit_gate_completeness.csv")
    #: 5개 audit 패널 — **원장의 figures 를 그대로 따른다.** 여기 목록을 따로 두면
    #:  Round-3 익명화 같은 정책 변경이 화면에만 반영 안 되는 일이 생긴다.
    _man = load_cascade_manifest()
    v2["audit_figures"] = [(f["image"], f["csv"], f["title"])
                           for f in (_man.get("figures") or [])
                           if (ROOT / f["image"]).is_file()] if _man.get("ok") else []
    #: 공개 표 — Round-3 gate denominator 계약 (record_present ≠ method_valid)
    v2["gate_denominators"] = read_csv("properties/cascade_seminar_gate_denominators_round3.csv")
    out["v2"] = v2
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


def _adapt_per_bond(d: dict):
    """per_bond_json/bonds_*.json → icohp_for 공통 스키마.

    ⚠ 키 이름만 옮긴다. **값을 바꾸거나 합치지 않는다** — 그쪽 파일이 원자료(Raw)이고
      bonds.json 쪽이 파생본이라, 둘이 어긋나면 원자료를 보여주는 게 맞다.
    """
    pb = next((v for k, v in d.items()
               if "per_bond" in k.lower() and isinstance(v, dict)), None)
    if not isinstance(pb, dict):
        return d
    bonds = {}
    for k, v in pb.items():
        if isinstance(v, dict):
            bonds[k] = v
        elif isinstance(v, (int, float)):
            bonds[k] = {"ICOHP_total_eV_per_bond": v}
    if not bonds:
        return d
    out = dict(d)
    out["bonds"] = bonds
    bd = next((v for k, v in d.items()
               if "bader" in k.lower() and isinstance(v, dict)), None)
    if bd:
        flat = {}
        for k, v in bd.items():
            if isinstance(v, (int, float)):
                flat[k] = v
            elif isinstance(v, dict):        # {"Li": {"mean": ...}} 같은 중첩 한 겹
                m = v.get("mean", v.get("net", v.get("charge")))
                if isinstance(m, (int, float)):
                    flat[k] = m
        if flat:
            out.setdefault("bader", flat)
    out.setdefault("system", d.get("system") or d.get("_provenance", "")[:80])
    out.setdefault("method", d.get("_provenance", ""))
    return out


def icohp_for(cid: str):
    """조성별 LOBSTER ICOHP JSON (있으면) — bonds 테이블 렌더용. 공통 스키마.

    ⚠ 계마다 비교표 키 이름이 다르다 (b2o3 comparison_vs_modelc /
      lpsocl comparison_vs_family / nd comparison_vs_modelc_comp1_PAW_4.0A).
      템플릿에 키를 하드코딩하면 한 계만 보이고 나머지는 조용히 사라지므로
      여기서 `comparison_vs_` 접두로 찾아 `_comparison` 으로 정규화해 넘긴다.
      per_site / bader 도 lpsocl 에만 있어서 렌더가 아예 안 되고 있었다.
    """
    pref = _PREFIX.get(cid, [cid])
    # ⚠ ICOHP 가 db 에 **세 가지 형태**로 있다: *_icohp.json / per_bond_json/bonds_*.json /
    #   comp2_icohp_origin.csv. 예전엔 첫 형태만 봐서 **comp1 은 Bonding 탭 자체가 없었고**
    #   canonical ICOHP_PS 의 출처(comp1 -5.938 / modelc -6.000)가 화면 어디에도 없었다.
    #   (2026-07-29 감사) → per_bond 스키마를 공통 스키마로 변환해 받는다.
    cands = list(sorted((DB / "properties").glob("*_icohp.json")))
    cands += list(sorted((DB / "properties" / "per_bond_json").glob("bonds_*.json")))
    for f in cands:
        stem = f.stem.lower()
        if any(p.lower() in stem for p in pref):
            d = _load_json(f)
            if d and not isinstance(d.get("bonds"), dict):
                d = _adapt_per_bond(d)          # per_bond_json 스키마 → 공통 스키마
            if d and isinstance(d.get("bonds"), dict):
                d = dict(d)
                ck = next((k for k in d if k.startswith("comparison_vs_")), None)
                if ck:
                    # 비교표는 결합행만 남긴다 — bader_* 나 _comp1_caveat 같은 주석행이
                    # 같은 dict 에 섞여 있어서 그대로 그리면 표가 깨진다.
                    cmpv = d[ck]
                    d["_comparison"] = {k: v for k, v in cmpv.items()
                                        if isinstance(v, dict) and not k.startswith("_")
                                        and not k.startswith("bader")}
                    d["_comparison_bader"] = {k[6:]: v for k, v in cmpv.items()
                                              if k.startswith("bader_") and isinstance(v, dict)}
                    # ⚠ 비교블록 안의 _ 주석만 보면 **최상위 caveat 을 놓친다**.
                    #   nd_icohp.json 은 "Absolute Li-X differs (PAW vs USPP basis);
                    #   trust WITHIN-nd comparisons" 를 최상위에 뒀는데, 절대값 비교표는
                    #   그대로 렌더되면서 그 경고만 사라졌다 (2026-07-29 감사).
                    notes = [v for k, v in cmpv.items()
                             if k.startswith("_") and isinstance(v, str)]
                    for k in ("caveat", "_caveat"):
                        if isinstance(d.get(k), str):
                            notes.append(d[k])
                    notes += [v for k, v in d.items()
                              if k.startswith("_CORRECTION") and isinstance(v, str)]
                    d["_comparison_note"] = " · ".join(notes) if notes else None
                    d["_comparison_key"] = ck
                    # 열 = 비교에 등장하는 모든 계 (note 제외), 등장 순서 유지
                    cols = []
                    for row in d["_comparison"].values():
                        for k in row:
                            if k != "note" and k not in cols:
                                cols.append(k)
                    d["_comparison_cols"] = cols
                d["_curves"] = cohp_curves_for(cid)
                return d
    return None


# 3계 공유 BVSE 자료 — 어느 한 조성의 것이 아니라 **비교표**라서 조성 prefix 로는
# 안 잡힌다(파일명이 bvse_ 로 시작). 실제로 CLAUDE.md 가 canonical 이라 부르는
# 3계 채널% 표가 사이트 어디에도 안 떴다 (2026-07-29 감사).
BVSE_SHARED = [
    ("bvse_3system_channel_origin.csv", "3계 채널 부피 % (원본 주기셀, canonical)",
     "modelc → LPSOCl(+O) → +B₂O₃. **정량·순위는 이 표만** — 큐빅 근사 인용 금지."),
    ("bvse_channel_volume.csv", "채널 부피 iso 사다리", "2026-07-27 보정 이력 포함"),
    ("bvse_cubic_approx/bvse_orig_vs_cubic.csv", "원본 vs 큐빅 근사 대조",
     "⛔ 큐빅은 **표시용**이다 — b2o3 가 6.73 vs 23.83 으로 3.5배 벌어진다. 인용 금지의 실증."),
]


def bvse_shared() -> list:
    """3계 공유 BVSE 표 + 정본 onset. 조성 페이지가 아니라 공용 카드에 붙는다."""
    out = []
    for rel, title, note in BVSE_SHARED:
        f = DB / "properties" / rel
        if f.exists():
            out.append({"rel": f"properties/{rel}", "title": title, "note": note})
    onset = _load_json(DB / "properties" / "bvse_onset_canonical_modelc.json")
    return {"tables": out, "onset": onset}


def cohp_curves_for(cid: str):
    """에너지 분해 COHP 곡선 CSV (tools/figures/extract_cohp_curves.py 산출) + 메타.

    없으면 None — gabia 에서 COHPCAR.lobster 를 회수해야 생긴다. 그 상태를
    템플릿이 그대로 알려 주게 한다(빈 탭 대신 '왜 없는지'를 띄운다).
    """
    pref = _PREFIX.get(cid, [cid])
    # db/properties 가 정본. docs/figures/icohp 는 예전 그림 스크립트가 CSV 를 거기 두던
    # 시절의 산출물(modelc/nd/b2o3)이라 **후순위로만** 본다 — 정규화 규약이 sum 이고
    # 열 이름도 '-pCOHP_*' 로 달라서, 같은 계에 db 판이 생기면 그쪽이 이긴다.
    cands = [(f, str(f.relative_to(DB)))
             for f in sorted((DB / "properties").glob("*cohp_curves*.csv"))]
    docs = DB.parent / "docs" / "figures" / "icohp"
    if docs.exists():
        cands += [(f, "docs/figures/icohp/" + f.name)
                  for f in sorted(docs.glob("*COHP*.csv"))]
    for f, rel in cands:
        if not _prefix_starts(f.name, pref):
            continue
        meta = _load_json(f.with_suffix(".meta.json")) or {}
        if not meta:                       # 사이드카가 없으면 CSV 머리말에서 긁는다
            head = f.read_text(encoding="utf-8", errors="ignore").splitlines()[:8]
            for ln in head:
                s = ln.lstrip("# ").strip()
                if s.startswith("{"):
                    try:
                        meta = {"pairs": json.loads(s)}
                    except json.JSONDecodeError:
                        pass
                    break
            if not meta:                   # 구형 머리말: "ICOHP(eV/bond): P–S -6.000, …"
                m = re.search(r"ICOHP\s*\(eV/bond\)\s*:\s*(.+)", " ".join(head))
                if m:
                    pairs = {}
                    for tok in m.group(1).rstrip('"').split(","):
                        mm = re.match(r"\s*([A-Za-z]+)[–-]([A-Za-z]+)\s+(-?[\d.]+)", tok)
                        if mm:
                            pairs[f"{mm.group(1)}-{mm.group(2)}"] = {
                                "ICOHP_per_bond_eV": float(mm.group(3))}
                    meta = {"pairs": pairs, "smooth_eV": 0.10}
        return {"rel": rel, "name": f.name, "legacy": rel.startswith("docs/"),
                "pairs": meta.get("pairs", {}), "smooth_eV": meta.get("smooth_eV"),
                "window_eV": meta.get("window_eV")}
    return None


# ELF 프로파일 판정 창 — tools/figures/sample_elf_bonds.py:103 과 **같아야** 한다.
#   창을 넓히면 Li 결합의 1s|2s 코어 노드(0.03~0.08)를 집어 순위가 뒤집힌다.
ELF_WIN = (0.40, 0.60)
ELF_COV, ELF_ION = 0.70, 0.30
# 프로파일 CSV 열 이름 → 중점 CSV 의 bond 키. 열 이름은 sample 쪽 표기와 순서가 달라서
# (예: 열 'S(free)-Li' ↔ 중점 'Li-S') 원소집합으로 맞춘다.
_ELF_COL = re.compile(r"^ELF_(.+?)_([\d.]+)A$")


def _elf_bond_key(label: str) -> frozenset:
    """'S(free)-Li' → {'S','Li'} — 자리 수식어와 방향을 지운 원소쌍."""
    return frozenset(re.sub(r"\(.*?\)", "", p).strip() for p in label.split("-"))


def elf_curves_for(cid: str):
    """결합별 ELF 프로파일 CSV + 중점 CSV 의 평균값(인용 표준)을 묶어 준다.

    ⚠ 곡선에서 읽는 값은 **[0.40,0.60] 최솟값**이지 곡선 전체 최솟값이 아니다.
      Li 결합은 frac 0.65 부근에 Li 1s|2s 코어 노드가 있어서(Li 1s 가 valence)
      전체 최솟값으로 줄을 세우면 Li–Cl < Li–O < Li–S 로 **순서가 뒤집힌다.**
      그림·표 어디서도 그 골을 결합 세기로 쓰지 않게 여기서 창을 고정한다.
    """
    pref = _PREFIX.get(cid, [cid])
    prof = next((f for f in sorted((DB / "properties").glob("*elf_profiles*.csv"))
                 if _prefix_starts(f.name, pref)), None)
    if prof is None:
        return None
    # 중점 CSV (n개 평균 = 인용 표준). 없으면 곡선만 그린다.
    mids = {}
    mid_f = next((f for f in sorted((DB / "properties").glob("*elf_bond_midpoint*.csv"))
                  if _prefix_starts(f.name, pref)), None)
    if mid_f:
        for r in csv.DictReader(mid_f.open(encoding="utf-8-sig")):
            mids[_elf_bond_key(r["bond"])] = r

    lines = [l for l in prof.read_text(encoding="utf-8-sig").splitlines()
             if not l.lstrip("﻿").startswith("#")]
    rdr = csv.DictReader(lines)
    cols = rdr.fieldnames or []
    rows = list(rdr)
    if len(cols) < 2 or not rows:
        return None
    xk = cols[0]
    frac = [float(r[xk]) for r in rows]

    bonds = {}
    for c in cols[1:]:
        m = _ELF_COL.match(c)
        if not m:
            continue
        label, dist = m.group(1), float(m.group(2))
        vals = [float(r[c]) for r in rows]
        win = [v for x, v in zip(frac, vals) if ELF_WIN[0] - 1e-9 <= x <= ELF_WIN[1] + 1e-9]
        cmin = min(win) if win else None
        # Li 쪽 코어 노드 — **표시만** 하고 순위엔 안 쓴다.
        # ⚠ Li 가 없는 결합(P–S/P–O)의 같은 구간은 코어 노드가 아니라 그냥 상대 핵으로
        #   내려가는 꼬리다 (P–S 0.015). 라벨을 붙이면 오독하므로 Li 결합만 계산한다.
        has_li = "Li" in _elf_bond_key(label)
        node = ([v for x, v in zip(frac, vals) if 0.60 <= x <= 0.90] if has_li else [])
        mid = mids.get(_elf_bond_key(label), {})
        bonds[c] = {
            "label": label.replace("-", "–"), "dist_A": dist,
            "central_min": round(cmin, 3) if cmin is not None else None,
            "core_node": round(min(node), 3) if node else None,
            "has_li": has_li,
            "n_bonds": int(mid["n_bonds"]) if mid.get("n_bonds") else None,
            "mean_central_min": float(mid["ELF_central_min"]) if mid.get("ELF_central_min") else None,
            "mean_midpoint": float(mid["ELF_midpoint"]) if mid.get("ELF_midpoint") else None,
            "verdict": (None if cmin is None else
                        "covalent" if cmin > ELF_COV else
                        "ionic" if cmin < ELF_ION else "polar / intermediate"),
        }
    if not bonds:
        return None
    return {"rel": str(prof.relative_to(DB)), "name": prof.name, "xk": xk,
            "window": list(ELF_WIN), "cov": ELF_COV, "ion": ELF_ION,
            "mid_rel": str(mid_f.relative_to(DB)) if mid_f else None,
            "bonds": bonds}


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
        {
            "id": "V5",
            "date": "2026-07-28",
            "title": "`gap_lit_eV` 스칼라 자체가 부실했다 — 라벨 없는 밴드갭은 값이 아니다",
            "claimed": (
                "47 도펀트의 밴드갭을 `gap_lit_eV` **단일 스칼라**로 들고 있었다. "
                "깔때기에서 전자절연 축을 '게이트가 아니라 진단'으로 둔 것은 "
                "'gap_lit_eV가 큐레이션 값이라 신뢰도가 낮아서'라는 정도의 이유였다."),
            "wrong": (
                "**이유가 그것보다 훨씬 깊다.** 밴드갭은 (a) **정의**(fundamental / optical / "
                "absorption / spectroscopic ellipsometry)와 (b) **시료**(단결정 벌크 / 박막 / "
                "비정질)를 명시하지 않으면 **값 자체가 성립하지 않는다**. "
                "게다가 도핑된 실물질에서는 **캐리어 농도에 따라 비단조로 변한다**."),
            "how_found": (
                "Spencer et al., *Appl. Phys. Rev.* **9**, 011315 (2022) 127쪽 전수 판독. "
                "이 리뷰가 다루는 9종 중 **8종이 우리 cascade 로스터**다 "
                "(Sc₂O₃·Al₂O₃·In₂O₃·Ga₂O₃·ZnO·SnO₂·NiO·CuO)."),
            "table": {
                "cols": ["도펀트", "우리 gap_lit_eV", "리뷰", "판정"],
                "rows": [
                    ["**Ga₂O₃**", "4.8", "SE **5.10 / 5.39 / 5.66** (b>a>c), absorption 4.50–4.73",
                     "**진짜 불일치.** 리뷰가 'absorption은 exciton 결합에너지를 놓쳐 계통적으로 낮고 SE가 진짜 fundamental'이라고 **명시 판정**. 방향별로 0.5 eV 이상 갈려 **스칼라 자체가 불완전**"],
                    ["**Cu₂O**", "2.1", "**없음 — 리뷰 주역은 CuO**",
                     "**대조 불가.** gap type부터 다르다(Cu₂O direct / CuO indirect). 우리 2.1의 출처를 따로 확인해야 한다"],
                    ["Al₂O₃", "8.8", "bulk 8.8–9.9 / **비정질 박막 6.2–6.8**",
                     "bulk 기준 정확 일치. 그러나 우리 문맥의 Al₂O₃는 대개 **비정질 ALD** → 절연성 **2 eV 과대평가** 위험"],
                    ["In₂O₃", "2.9", "fundamental **2.93** / optical 3.55",
                     "**일치.** 문헌 다수가 쓰는 3.6–3.7은 optical(VBM→CBM이 **dipole 금지**라 구조적으로 갈림) — 라벨이 없으면 In₂O₃만 부당하게 낮게 평가된다"],
                    ["SnO₂", "3.6", "3.614", "정확 일치 (8종 중 최고)"],
                    ["Sc₂O₃", "6.0", "박막 5.7–5.84",
                     "값 차이가 아니라 **시료 차이** — 우리 6.0은 단결정 RT(Tippins 1966)와 일치"]]},
            "now_known": (
                "**β-Ga₂O₃의 gap은 캐리어 농도에 따라 4.69 → 4.716 → 4.68 → 다시 증가로 비단조 변한다** "
                "(Burstein–Moss ↔ Mott 전이 ↔ band-gap renormalization). SnO₂·In₂O₃도 Burstein–Moss를 보인다. "
                "→ **단일 스칼라 gap은 도핑된 실물질에서 성립하지 않는다.** "
                "우리가 전자절연을 게이트로 안 쓰고 진단으로만 둔 판단이 **결과적으로 옳았고, 이제 근거가 생겼다**. "
                "다음 작업: `gap_lit_eV`에 `definition`(fundamental/optical/absorption/SE) + "
                "`sample`(단결정/박막/비정질) 두 필드 추가 — **계산 불필요, 라벨링만**."),
            "caveat": (
                "⚠ 이 리뷰에는 **전기화학이 통째로 없다.** ESW·산화 onset·Li 수송·계면 반응성을 한 줄도 "
                "말하지 않는다 — 우리 cascade의 산화안정 축을 **대체하지도 보조하지도 못한다**. "
                "⚠ 리뷰의 '코팅'은 반사방지막·MOSFET 게이트 유전체이지 **전기화학 보호막이 아니다**. "
                "⚠ Sc₂O₃ 순수 벌크 E 214–228 GPa를 우리 도핑 호스트 `E_VRH` 42.082 GPa와 같은 표에 놓으면 오독 "
                "— **물리적 대상이 다르다**. "
                "⚠ 재인용이고 리뷰 자체에 내부 불일치가 있다(ZnO gap 본문 3.54 vs 표 3.45 등)."),
            "lesson": "**단위가 맞다고 값이 맞는 게 아니다.** 밴드갭처럼 '한 숫자'로 보이는 물성일수록 "
                      "정의와 시료 라벨이 값의 일부다.",
            "papers": ["spencer2022_review_tco_band_structure_oxides"],
            "artifacts": ["db/properties/oxide_literature_properties_spencer2022.json"],
        },
        {
            "id": "V6",
            "date": "2026-07-28",
            "title": "NiO 탈락 사유가 하나 더 있었다 — Li 도핑되면 p-type 전도체가 된다",
            "claimed": ("cascade에서 NiO가 46위인 근거는 **산화안정성과 역학** 축이었다. "
                        "전자절연 축은 진단으로만 두고 순위에 반영하지 않았다."),
            "wrong": "틀린 게 아니라 **불완전했다** — 더 결정적인 사유를 놓치고 있었다.",
            "how_found": (
                "Spencer 2022 p.78: *\"**Lithium is a very common dopant of NiO** and acts as a "
                "substitute for the nickel ions... often the lithium doped samples will exhibit "
                "higher conductivity values.\"*"),
            "now_known": (
                "Li⁺는 NiO에서 **acceptor**이고 Li_xNi₁₋ₓO는 **p-type 전도체**다. "
                "즉 **Li-rich 계에 NiO를 넣으면 정공 전도 경로가 생길 수 있다** — "
                "고체전해질에서 가장 피해야 할 것(전자 전도)이 도핑 자체로 유도된다. "
                "이건 산화안정·역학과 **독립된 별개 사유**이고, 순위가 아니라 **탈락 근거**에 가깝다."),
            "caveat": ("⚠ **이건 리뷰의 주장이 아니라 리뷰 서술을 우리 문맥으로 옮긴 해석이다.** "
                       "Spencer 2022는 전고체전지를 다루지 않는다. 인용할 때 반드시 '리뷰가 보고한 "
                       "Li-doped NiO의 p-type 거동으로부터 우리가 추론한 것'으로 쓸 것. "
                       "⚠ 실제 검증은 Li 화학퍼텐셜 하에서의 NiO 전자구조 계산이 필요하다."),
            "lesson": "**같은 물질이 다른 문맥에서 다른 이유로 탈락할 수 있다.** "
                      "물성 리뷰는 우리 축에 없는 탈락 사유를 준다.",
            "papers": ["spencer2022_review_tco_band_structure_oxides"],
            "artifacts": ["db/properties/oxide_literature_properties_spencer2022.json"],
        },
        {
            "id": "V7",
            "date": "2026-07-29",
            "title": "위원회 불일치 온도 스윕을 '⚠⚠ 급증'으로 경보했다가 철회",
            "claimed": ("watch_all.py 가 800 K 59/200 · 1000 K 118/200 프레임이 문턱을 넘었다며 "
                        "'급증' 경보를 냈다. 읽히기로는 '고온 배열이 UMA 훈련 분포 밖' = "
                        "600/800/1000 K 3점 아레니우스의 상단 두 점이 신뢰 불가."),
            "wrong": ("문턱이 **600 K 표본의 절대 p95**(0.3669 eV/Å)인데, 조화 고체의 RMS 힘은 "
                      "√T 로 커진다. 모델 간 **상대** 오차가 완전히 같아도 고정 절대 문턱을 넘는 "
                      "프레임은 온도와 함께 늘어난다. 즉 열적 스케일링을 외삽으로 오독했다."),
            "how_found": (
                "mlip_committee.py 가 이미 '같은 표본에서 뽑은 백분위를 그 표본에 적용하면 정보가 0' "
                "이라는 순환성을 주석으로 못 박아 뒀는데, **같은 함정이 온도 축에서 재발**한 것이다. "
                "npz 에서 힘 크기를 직접 재서 확인: 400→1000 K 실측 ×1.324 vs 조화 예측 √(T/600)=1.291 "
                "(2.6% 초과 = 가벼운 비조화). 문턱을 힘 크기에 비례해 옮겨 다시 세면 "
                "**T800 8/200 · T1000 4/200 로 기준선 10/200 보다 오히려 적다** — 고정문턱 판독과 방향이 반대."),
            "now_known": (
                "**어느 온도에서도 외삽 신호가 없다.** 600/800/1000 K 3점 아레니우스는 이 지표로 "
                "막히지 않는다. 다만 '상대 불일치가 −8.3% 로 준다'를 '고온이 더 안전하다'로 읽으면 "
                "**또 틀린다** — D = a + b·F 적합에서 온도무관 절편 a = +0.102 eV/Å 이고 이것이 "
                "600 K 불일치의 **32%** 다. 바닥이 있으면 D/F = a/F + b 라서 F 가 커질수록 자동으로 준다. "
                "그 바닥은 별개 발견이다: 열운동이 0 이어도 남는 모델 간 불일치 = **평형 구조 PES 자체의 불일치**."),
            "caveat": ("⚠ 절대 σ 인용 금지 규율은 그대로다 — 세 엔진(UMA/MACE-MP-0/SevenNet-0)이 "
                       "전부 PBE 계열이라 계통오차를 공유한다. 일치는 '훈련 분포 안'만 말한다."),
            "lesson": "**분포의 스케일이 변하는 축(온도)에 고정 절대 문턱을 그대로 쓰면 안 된다.** "
                      "watch 는 이제 초과 수를 '(정규화 전)' 으로만 표시하고 경보하지 않는다 — "
                      "판정은 힘 크기로 정규화하는 committee_sweep_verdict.py 가 한다.",
            "papers": ["kim2026_li_argyrodite_sei_reactive_md"],
            "artifacts": ["db/properties/committee_temperature_sweep.json",
                          "db/properties/committee_temperature_sweep_origin.csv",
                          "tools/ionic/committee_sweep_verdict.py"],
        },
    ]


# ── PI(교수) 레지스트리 ──────────────────────────────────────
# digest 헤더의 저자/소속 줄에서 이 이름들을 찾아 논문에 태그를 붙인다.
# `our` = 우리 연구실 계보. ⚠ 같은 학교라도 그룹이 다르면 our=False (정윤석 ≠ 이용민).
PI_REGISTRY = [
    {"key": "ymlee",  "ko": "이용민", "en": "Yong Min Lee",  "aff": "연세대 화공·배터리공학 / DGIST",
     "our": True,  "color": "#0d9488",
     "alias": ["Yong Min Lee", "Yong-Min Lee", "yongmin@yonsei", "이용민"]},
    {"key": "kycho",  "ko": "조국영", "en": "Kuk Young Cho", "aff": "한양대 (ERICA·안산)",
     "our": True,  "color": "#7c3aed",
     "alias": ["Kuk Young Cho", "Kuk-Young Cho", "조국영"]},
    {"key": "jwlee",  "ko": "이종원", "en": "Jong-Won Lee",  "aff": "한양대",
     "our": True,  "color": "#c05621",
     "alias": ["Jong-Won Lee", "Jong Won Lee", "J-W Lee", "이종원"]},
    {"key": "sulee",  "ko": "이상욱", "en": "Sang Uck Lee",  "aff": "성균관대 화공 (CMS Lab)",
     "our": False, "color": "#be123c",
     "alias": ["Sang Uck Lee", "Sang-Uck Lee", "suleechem@skku", "이상욱"]},
    {"key": "jhmoon", "ko": "문장혁", "en": "Janghyuk Moon", "aff": "중앙대 에너지시스템공학",
     "our": False, "color": "#0284c7",
     "alias": ["Janghyuk Moon", "Jang-hyuk Moon", "문장혁"]},
    {"key": "ysjung", "ko": "정윤석", "en": "Yoon Seok Jung", "aff": "연세대 (⚠ 이용민 랩 아님)",
     "our": False, "color": "#65a30d",
     "alias": ["Yoon Seok Jung", "Yoon-Seok Jung", "정윤석"]},
    {"key": "ceder",  "ko": "—",     "en": "Gerbrand Ceder", "aff": "UC Berkeley / LBNL",
     "our": False, "color": "#6b7280", "alias": ["Ceder"]},
    {"key": "ong",    "ko": "—",     "en": "Shyue Ping Ong", "aff": "UC San Diego",
     "our": False, "color": "#6b7280", "alias": ["Shyue Ping Ong", "S. P. Ong"]},
    {"key": "zeier",  "ko": "—",     "en": "Wolfgang Zeier", "aff": "Münster",
     "our": False, "color": "#6b7280", "alias": ["Zeier"]},
]
PI_BY_KEY = {p["key"]: p for p in PI_REGISTRY}


def _paper_pis(slug: str) -> list:
    """digest 앞부분(저자·소속 블록)에서 PI 이름을 찾는다.

    ⚠ 두 가지 오탐을 막아야 한다.
      ① 본문 전체를 스캔하면 **참고문헌으로 인용된 사람**이 저자로 잡힌다 → 머리말 25줄만.
      ② 머리말에도 **소속 판정 문장**이 있어 부정문 안의 이름이 잡힌다 —
         실제 사례: son2025 digest 의 `[외부] ... 우리 그룹(... Yong Min Lee ...) **아님**`.
         이름 문자열만 보면 이용민 교수님 논문으로 오분류된다.
         → **저자/발표자 줄만** 보고, 판정·부정 문장이 든 줄은 제외한다.
    """
    f = LITDB / "papers" / f"{slug}.md"
    if not f.exists():
        f = LITDB / "talks" / f"{slug}.md"
    if not f.exists():
        return []
    try:
        lines = f.read_text(encoding="utf-8", errors="ignore").splitlines()[:35]
    except Exception:
        return []
    # 부정 표지 — 줄을 통째로 버리지 않고 **이 지점에서 자른다**.
    #   실측 사례: taklu2021 은 `소속: NTUST ... · 외부 그룹 (≠ 우리 한양/Jong-Won Lee/...)`.
    #   줄 앞부분(진짜 소속)은 살려야 하고 `≠` 뒤(비교용 나열)만 버려야 한다.
    #   ("우리 그룹" 만 걸러서는 "우리 한양" 을 놓친다 — 실제로 놓쳤다.)
    #   추가 실측(2026-07-29): oh2026_bimodal 은 `"Yoon Seok Jung 공저"라 적혀 있었으나 **오류** —
    #   실제 저자에 Yoon Seok Jung은 **없고**...` 라 적혀 있는데 그 줄에서 정윤석 태그가 붙었다.
    #   "오류"/"없고" 도 부정 표지다.
    #   ⚠ NEG(잘라내기)로는 **이름이 부정어보다 앞에 오는 경우**를 못 잡는다.
    #   실측: `TIER 리스트 초안에 "Yoon Seok Jung 공저"라 적혀 있었으나 **오류** — 실제 저자에
    #   Yoon Seok Jung은 **없고**...` → 앞부분만 남겨도 이름이 그대로 살아 태그가 붙었다.
    #   **정정 문장은 줄 전체를 버린다** (그 줄의 존재 이유가 "그 이름이 틀렸다"이므로).
    DROP = ("저자 정정", "오류 —", "**오류**", "잘못 적", "라 적혀 있었으나")
    NEG = ("≠", "아님", "외부 그룹", "소속 판정",
           "우리 그룹", "우리 연구실", "우리 한양")
    #   INCLUDE 가 좁아서 서지 블록(`**인용:**`)과 `우리 랩(Hanyang, **Jong-Won Lee** 그룹)`
    #   형식을 통째로 버렸다 — 실측 15편에서 실제 공저 PI 를 놓쳤다.
    #   ⚠ "우리 랩" 은 NEG 가 아니라 INCLUDE 다. 뒤에 진짜 PI 이름이 온다.
    INCLUDE = ("저자", "발표자", "author", "Author", "corr.", "@", "인용:", "우리 랩")
    cand = []
    for ln in lines:
        if any(d in ln for d in DROP):
            continue
        for tok in NEG:
            i = ln.find(tok)
            if i >= 0:
                ln = ln[:i]
        if not ln.strip():
            continue
        # 제목 줄(#) 과 저자·소속 줄(>)만. 저자 표지가 있거나 소속이 명시된 줄.
        if ln.startswith("#") or any(x in ln for x in INCLUDE) or "University" in ln or "대학" in ln:
            cand.append(ln)
    head = "\n".join(cand)
    return [pi["key"] for pi in PI_REGISTRY if any(a in head for a in pi["alias"])]


@lru_cache(maxsize=512)
def _paper_pis_c(slug, _mt):
    return tuple(_paper_pis(slug))


def paper_pis(slug: str) -> list:
    f = LITDB / "papers" / f"{slug}.md"
    if not f.exists():
        f = LITDB / "talks" / f"{slug}.md"
    return list(_paper_pis_c(slug, _mtime_ns(f) if f.exists() else 0))


def mlip_committee() -> dict:
    """T1 모델 위원회 기준선. /benchmarks 의 방법론 축에 붙는다 (물성이 아니라 방법).

    온도 스윕 판정(committee_temperature_sweep.json)이 있으면 `_sweep` 으로 얹는다.
    ⚠ 기준선(600 K 단일 표본)만 보여주면 '고정 문턱 초과 = 나쁨' 오독이 그대로 남는다 —
      그 오독을 우리가 실제로 했고(판정이력 V7), 스윕이 그걸 뒤집은 자료다. 같이 보여야 한다.
    """
    d = _load_json(DB / "properties" / "mlip_committee_baseline.json")
    if not d:
        return d
    sw = _load_json(DB / "properties" / "committee_temperature_sweep.json")
    if sw:
        d = dict(d)
        d["_sweep"] = _sweep_view(sw)
    return d


def _sweep_view(sw: dict) -> dict:
    """온도 스윕 JSON 을 화면용으로 정규화한다.

    ⚠ 도구(committee_sweep_verdict.py)가 2026-09-01 이전엔 D=a+b·F 적합(force_model)을
      **콘솔에만 찍고 JSON 에 안 남겼다** — /benchmarks 템플릿이 그 없는 키를 읽다
      깨진 회귀의 원인. 구판 JSON 이면 by_T 에 이미 있는 (힘크기, 중앙불일치) 5점에서
      도구와 같은 최소제곱으로 재계산한다. **파생값이지 새 측정이 아니다** — 재생성한
      JSON 에 force_model 이 있으면 그쪽이 이긴다.

    이 함수가 못 하는 것: by_T 가 3점 미만이거나 로그가 정의 안 되면(비양수) fit 을
    만들지 않는다 — 템플릿은 그 절을 통째로 접는다.
    """
    sw = dict(sw)
    bt = sw.get("by_T") or {}
    base = str(sw.get("base_T", ""))
    if base in bt:
        sw["_els_base"] = bt[base].get("by_element_relative")
    if not sw.get("force_model") and len(bt) >= 3:
        try:
            import math
            Ts = sorted(bt, key=int)
            F = [float(bt[t]["force_scale_eV_per_A"]) for t in Ts]
            D = [float(bt[t]["median"]) for t in Ts]
            n = len(F)
            mF, mD = sum(F) / n, sum(D) / n
            sxx = sum((f - mF) ** 2 for f in F)
            b = sum((f - mF) * (d_ - mD) for f, d_ in zip(F, D)) / sxx
            a = mD - b * mF
            sst = sum((d_ - mD) ** 2 for d_ in D)
            r2 = 1 - sum((d_ - (a + b * f)) ** 2 for f, d_ in zip(F, D)) / sst
            lF, lD = [math.log(f) for f in F], [math.log(d_) for d_ in D]
            mlF, mlD = sum(lF) / n, sum(lD) / n
            pn = sum((x - mlF) * (y - mlD) for x, y in zip(lF, lD)) \
                / sum((x - mlF) ** 2 for x in lF)
            pc = mlD - pn * mlF
            pr2 = 1 - sum((y - (pc + pn * x)) ** 2 for x, y in zip(lF, lD)) \
                / sum((y - mlD) ** 2 for y in lD)
            sw["force_model"] = {
                "linear_intercept_eV_per_A": a, "linear_slope": b, "linear_R2": r2,
                "power_exponent": pn, "power_R2": pr2,
                "floor_share_at_base_T": a / float(bt[base]["median"]),
                "_derived": "webapp 파생 (구판 JSON — 도구가 fit 을 지속하지 않던 판)",
            }
        except (KeyError, ValueError, ZeroDivisionError, ArithmeticError):
            pass
    return sw


def uma_force_benchmark() -> dict:
    """db/properties/uma_force_benchmark.json — 우리 포텐셜의 힘 정확도(문헌 DFT 라벨 대비).

    /benchmarks 의 **방법 축**에 붙는다. T1b("softening 이 GNN 공통인가")의 자료다:
    같은 프레임·같은 정답지에서 UMA 와 SevenNet-0 을 나란히 놓은 것이 요점이라
    두 엔진을 **한 표**로 보여줘야 의미가 산다.

    이 함수가 못 하는 것: 값의 옳고 그름을 판정하지 않는다. JSON 을 그대로 옮긴다.
    """
    return _load_json(DB / "properties" / "uma_force_benchmark.json") or {}


def nd_survey() -> dict:
    """db/properties/nd_substitution_survey_index.json — 원소 치환 문헌 54편 색인.

    ⚠ 대부분이 **우리 화학(황화물 Li)이 아니다** — 양성자·산화물이온·불화물이온 전도체가 다수다.
    그래서 페이지에서 `system_class` 를 앞세우고 우리 화학 순으로 정렬해 보여준다.
    """
    return _load_json(DB / "properties" / "nd_substitution_survey_index.json")


SYSCLASS_LABEL = {
    "sulfide_Li":         ("황화물 Li", "#c05621", "우리 화학 — 직접 이식 검토 가능"),
    "halide_Li":          ("할라이드 Li", "#7c3aed", "인접 — 음이온 화학이 다름"),
    "garnet_Li":          ("가넷 (LLZO)", "#2563eb", "Li 전도체지만 산화물 골격"),
    "perovskite_Li":      ("페로브스카이트 Li", "#0284c7", "Li 전도체, 산화물"),
    "Li_cathode_or_cell": ("Li 양극·셀", "#be123c", "전해질이 아님 — 다른 층"),
    "other_ion_carrier":  ("타 이온 운반체", "#65a30d", "Na⁺·F⁻ 등 — 운반체가 다름"),
    "proton_or_oxide_ion": ("양성자·산화물이온", "#6b7280", "⛔ 운반체·온도역이 완전히 다름"),
    "other":              ("기타", "#9ca3af", "분류 보류"),
}


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
        out.append({"id": f.stem, "title": title_plain(title), "title_html": title_html(title),
                    "speaker": speaker,
                    "session": session, "digested": digested, "pis": paper_pis(f.stem)})
    return out



# ═══ litdb 주제 태그 (손 큐레이션) ═════════════════════════════════════════
# ⚠ UI 검색은 제목/id/type 만 훑는다. 'screening' 을 쳐도 **제목에 그 단어가 있는 7편**만
#   잡히는데, 본문 전수 감사에서 실제 스크리닝 계열은 13편이었다. 휴리스틱으로 늘리면
#   또 틀리므로 litdb/topics.json 에 **명시적으로 등록**하고 그것만 믿는다.
_TOPICS_CACHE = {}


def litdb_topics() -> dict:
    if not _TOPICS_CACHE:
        f = LITDB / "topics.json"
        try:
            _TOPICS_CACHE.update(json.loads(f.read_text(encoding="utf-8")))
        except Exception:
            _TOPICS_CACHE["_topics"] = {}
    return _TOPICS_CACHE


def topic_meta() -> dict:
    return litdb_topics().get("_topics", {})


def topic_primer() -> dict:
    return litdb_topics().get("_primer", {})


def paper_topics(pid: str) -> dict:
    """→ {topics: [...], gloss: str|None, caution: str|None}"""
    e = litdb_topics().get(pid)
    if not isinstance(e, dict):
        return {"topics": [], "gloss": None, "caution": None}
    return {"topics": e.get("topics", []), "gloss": e.get("gloss"),
            "caution": e.get("caution")}


_EM_STRONG = re.compile(r"\*\*(.+?)\*\*", re.S)
_EM_ITAL = re.compile(r"(?<![\w*])\*(?!\s)([^*]+?)(?<!\s)\*(?![\w*])")


def title_plain(t: str) -> str:
    """제목에서 마크다운 강조 기호를 걷어낸다 — 검색·⌘K·tooltip 은 이걸 쓴다.

    ⚠ `**` 가 남아 있으면 "Jong-Won Lee" 로 검색해도 안 걸린다.
    """
    return _EM_ITAL.sub(r"\1", _EM_STRONG.sub(r"\1", t or ""))


def title_html(t: str) -> str:
    """제목의 강조를 **색**으로 (1저자 2026-08-06: "여기에서는 다 볼드이니까 색깔로 분류").

    목록 카드의 제목은 이미 굵어서 볼드를 더 줘도 안 갈린다 —
    `**우리 랩·우리 그림**` 같은 표시가 눈에 들어와야 그게 표시로서 값을 한다.
    """
    s = (t or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    s = _EM_STRONG.sub(r'<span class="t-em">\1</span>', s)
    return _EM_ITAL.sub(r'<span class="t-it">\1</span>', s)


def list_papers() -> list:
    """litdb/papers/*.md → [{id, title, type, track}] (DEM/DFT 분류 포함)."""
    out = []
    pd = LITDB / "papers"
    if not pd.exists():
        return out
    for f in sorted(pd.glob("*.md")):
        if f.stem.startswith("_"):
            continue
        # `<slug>__seminar_*` 는 digest 의 **동반 발표대본**이다 (2026-08-28 규약).
        # digest 로 세면 인덱스 정합 점검이 '미등재 digest' 오탐을 낸다 — 본체에서 링크된다.
        if "__seminar" in f.stem:
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
        tp = paper_topics(f.stem)
        # title 은 **평문**(검색·⌘K·tooltip), title_html 은 강조를 색으로 바꾼 것(카드)
        out.append({"id": f.stem, "title": title_plain(title), "title_html": title_html(title),
                    "type": type_str,
                    "track": literature_track(f.stem, type_str, title),
                    "digested": digested, "pis": paper_pis(f.stem),
                    "topics": tp["topics"], "gloss": tp["gloss"],
                    "caution": tp["caution"]})
    return out


def _is_blank(r):
    return (not r) or (not any((c or "").strip() for c in r))


# 데이터 행이 아니라 '요약/파생' 행 (ratio_…, => sigma_ratio 등). 차트 데이터에서 빼고 각주로 보낸다.
# 이걸 안 빼면 요약행의 문자열 셀('1.08+/-0.18')이 열 타입 판정을 오염시켜 진짜 값 열이
# categorical 로 떨어진다(= σ·Ea 열이 차트에서 통째로 사라지는 원인).
_SUMMARY_ROW = re.compile(r"^\s*(=>|ratio[_/]|delta[_ ]|Δ|d?Ea\s*=)", re.I)

def read_csv(rel: str) -> dict:
    """rel 은 db/ 기준 경로. 예외로 'docs/figures/' 접두는 그림 산출 CSV 트리를 읽는다.

    ⚠ 루트를 넓히는 게 아니라 **두 개만** 허용한다 — 임의 경로 탈출을 막는
      is_relative_to 검사는 양쪽 다 유지한다. db/ 안엔 docs 디렉터리가 없어서
      기존 호출(properties/…, spectra/…)과 충돌하지 않는다.
    """
    if rel.startswith("docs/figures/"):
        root = (DB.parent / "docs" / "figures").resolve()
        p = (DB.parent / rel).resolve()
    else:
        root, p = DB.resolve(), (DB / rel).resolve()
    if not p.is_relative_to(root) or not p.exists():
        return {"error": "not found"}
    # ⚠ utf-8-**sig**. 하우스 스타일 CSV 는 Origin 호환을 위해 BOM 을 붙여 쓰는데,
    #   'utf-8' 로 열면 첫 셀이 '﻿# …' 이 되어 lstrip('# ') 검사에 안 걸린다.
    #   그러면 **첫 줄 주석이 헤더로 잡혀** 표가 통째로 1열짜리가 된다 (2026-07-30 발견).
    rows = list(csv.reader(p.open(encoding="utf-8-sig")))
    # 헤더 = 선행 주석(#)·빈 줄을 건너뛴 첫 실질 행
    # ⚠ 주석줄을 **버리지 않고 모은다.** CSV 가 자기 안에 적어 둔 규율 캐비앳
    #   (예: "absolute sigma = MLIP Nernst-Einstein upper bound; RT extrapolation NOT reportable")
    #   이 UI 에 도달하지 못해 절대 σ 가 무경고로 그려질 수 있었다 (2026-07-29 감사).
    notes = [",".join(r).lstrip("# ").strip()
             for r in rows if r and r[0].lstrip().startswith("#")]
    i = 0
    while i < len(rows) and (_is_blank(rows[i]) or rows[i][0].lstrip().startswith("#")):
        i += 1
    if i >= len(rows):
        return {"columns": [], "data": [], "notes": notes}
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
    return {"columns": header, "data": data, "n": len(data),
            "summary": summary, "notes": notes}


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
    # ⚠ 발표덱(litdb/talks)이 검색 인덱스에 통째로 빠져 있었다 — 논문 156편은 들어가는데
    #   덱 2편은 안 들어갔다. 인용 규율이 다르므로 track 을 '발표'로 구분해 넣는다.
    talks = [("발표", t_["title"], f"{t_.get('speaker','')} · {t_.get('session','')}",
              f"/literature#{t_['id']}") for t_ in list_talks()]
    # 순서·묶음은 사이드바(base.html)와 같게 — 두 군데가 어긋나면 찾는 사람이 헷갈린다
    pages = [
        ("페이지", "Dashboard", "커버리지 매트릭스·조성 요약", "/"),
        # 결과 보기
        ("페이지", "Property Explorer", "정렬·필터 물성 표 + provenance", "/explorer"),
        ("페이지", "Comparison", "조성 간 비교 + 레이더", "/compare"),
        ("페이지", "Periodic Table", "원소별 조성 탐색", "/elements"),
        # 계산 돌리기
        ("페이지", "Compute", "원클릭 계산 입력 생성", "/compute"),
        ("페이지", "Screening·ML", "AI 계산 도핑 스크리닝 (cascade)", "/cascade"),
        ("페이지", "Methods", "계산 방법 canonical", "/methods"),
        # 문헌·검증  (⚠ Benchmarks·Nd 서베이는 사이드바엔 있는데 검색으론 못 찾던 것, 2026-07-29 감사)
        ("페이지", "Literature", "DEM/DFT 문헌", "/literature"),
        ("페이지", "Benchmarks", "외부 재현 표적 · 덱 정정 원장 · 판정 이력 · 위원회 온도 스윕", "/benchmarks"),
        ("페이지", "Nd 치환 서베이", "원소 치환 문헌 54편 색인", "/nd-survey"),
        # 자료·기록
        ("페이지", "Files", "그림·데이터·구조 전체 갤러리 (💬 코멘트)", "/files"),
        ("페이지", "Glossary", "용어 설명집", "/glossary"),
        ("페이지", "미결 리스트 (Open Items)", "판정 대기 · PDF 확보 대기 · ML 후속 · 심포지엄 대응", "/todo"),
        ("페이지", "Work Log", "작업 기록", "/log"),
    ]
    for t, label, sub, url in pages + talks:
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
        # 자기 문서가 없어도 내용이 다른 개념 문서에 있으면 거기로 (doc 필드, 2026-08-04)
        url = (f"/concept/{g['id']}" if g["id"] in have
               else f"/concept/{g['doc']}" if g.get("doc") else "/glossary")
        idx.append({"t": "용어", "label": g["term"], "sub": g["full"],
                    "url": url, "kw": f"{g['id']} {g['cat']}"})
    for cid in sorted(have):
        idx.append({"t": "개념", "label": cid.upper(), "sub": "상세 개념 문서",
                    "url": f"/concept/{cid}", "kw": cid})
    for p in list_papers():
        idx.append({"t": "논문", "label": p["title"][:70], "sub": p["type"][:40],
                    "url": f"/literature?open={p['id']}", "kw": f"{p['id']} {p['track']}"})
    # 내가 적어 둔 코멘트·메모 (1저자 요청 2026-08-06 "그 comment 도 검색에서 걸리게",
    # 2026-08-17 "메모 내용들도 search 에서 잡히게"). 링크 규칙은 comment_origin 한 곳.
    # ⚠ 여백 메모는 **붙인 자리(anchor)도 kw 에** 넣는다 — 형광펜 친 문장으로도 찾는다.
    idx.append({"t": "페이지", "label": "메모", "sub": "날짜별 메모·코멘트 모음",
                "url": "/notes", "kw": "notes memo 메모 코멘트"})
    for c in comment_all():
        anc = c.get("anchor") or ""
        idx.append({"t": "메모" if anc else "코멘트",
                    "label": c["text"][:70],
                    "sub": ("📝 " if anc else "💬 ") + f"{c['where']} · {c['at']}",
                    "url": c["url"], "kw": f"{c['rel']} {anc}"})
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
    "comp1":  {"ecutwfc": 52, "ecutrho": 520, "k": [4, 4, 4], "struct": "comp1_V0_k444.cif",  "server": "kgy (RTX3090, QE-GPU)"},
    "comp2":  {"ecutwfc": 52, "ecutrho": 520, "k": [4, 4, 4], "struct": "comp2_V0_v3_candidate.xyz", "server": "gabia (A6000, QE-GPU)"},
    "modelc": {"ecutwfc": 60, "ecutrho": 480, "k": [2, 2, 1], "struct": "modelC_DFT_EOS_V0.cif",     "server": "kgy (RTX3090, QE-GPU)"},
    "modelc_v3": {"ecutwfc": 60, "ecutrho": 480, "k": [2, 2, 1], "struct": "modelc_v3_62atom_V0.cif", "server": "kgy (RTX3090, QE-GPU)"},
    "modelc_nd_doped": {"ecutwfc": 60, "ecutrho": 480, "k": [6, 6, 1], "struct": "modelc_nd_doped_DFTrelax.cif", "server": "KISTI neuron", "dftu": True},
    "lpsocl": {"ecutwfc": 60, "ecutrho": 480, "k": [2, 2, 1], "struct": "lpsocl_v0.cif",      "server": "KISTI neuron"},
    "b2o3":   {"ecutwfc": 60, "ecutrho": 480, "k": [1, 1, 1], "struct": "b2o3_relaxV0.cif",            "server": "KISTI neuron"},
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
        has_el_decl = has_method_decl = False
        try:
            head = (pd / f"{p['id']}.md").read_text(encoding="utf-8", errors="ignore").splitlines()[:60]
            blob += " " + " ".join(head)
            for line in head:
                m = re.search(r"(?:elements|원소)\s*[:：]\s*(.+)", line, re.I)
                if m:
                    has_el_decl = True
                    for t in re.split(r"[,\s/·]+", m.group(1)):
                        t = t.strip("`*_ ")
                        if t in _PSYMS:
                            el_tags.add(t)
                m2 = re.search(r"(?:methods|기법|기술)\s*[:：]\s*(.+)", line, re.I)
                if m2:
                    has_method_decl = True
                    for t in re.split(r"[,/·]+", m2.group(1).lower()):
                        gid = METHOD_MAP.get(t.strip("`*_ ").strip())
                        if gid:
                            method_tags.add(gid)
        except Exception:
            pass
        idx.append({**p, "blob": blob.lower(), "el_tags": el_tags, "method_tags": method_tags,
                    "has_el_decl": has_el_decl, "has_method_decl": has_method_decl})
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
        # 선언(elements:)이 있으면 그것이 정본 — 토큰스캔은 끈다 (glossary_papers 와 같은 이유).
        # kb_slugs 는 사람이 쓴 authored 소스라 그대로 둔다.
        declared = (sym in p["el_tags"]) or (p["id"] in kb_slugs)
        if declared or (not p.get("has_el_decl") and toks and any(t in p["blob"] for t in toks)):
            if p["id"] not in seen:
                seen.add(p["id"])
                hits.append({"id": p["id"], "title": p["title"], "track": p["track"],
                             "_rank": 0 if declared else 1})
    # ⛔ 2026-08-28 — **선언한 논문을 먼저 낸다.** 예전에는 파일 순서라, 원소를 명시 선언한
    #   논문이 본문에 스쳐 언급만 한 논문에 밀려 limit 밖으로 잘렸다 (deng2026 이 Li 에서
    #   145편 중 21위였다). 잘리는 것 자체는 limit 의 문제지만, **무엇이 먼저 잘리느냐**는
    #   우리가 정할 수 있다.
    hits.sort(key=lambda h: h.pop("_rank"))
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
    """이 기법(용어)을 쓴 litdb 논문 — **선언이 있으면 선언만**, 없을 때만 토큰스캔. 클릭 → digest.

    ⛔⛔ 2026-08-28 — 예전에는 `태그 ∪ 토큰스캔` 이라 **선언을 토큰스캔이 덮어썼다.**
      두 가지로 망가졌다:
      · `deng2026` 은 §11-D 에 *"이 논문은 NEB·Bader·COHP·ELF·BVSE·phonon 을 **하지 않는다**"*
        라고 적었는데, 그 **부정문이 긁혀** 여섯 기법 페이지에 전부 링크됐다.
      · `kim2025_csp` 는 methods 를 바르게 선언해 놓고, 바로 아래 *"종전 methods 줄은
        `bader, bvse, cohp, dos, elf, esw, neb, pdos` 였다"* 는 **정정 주석이 다시 긁혔다.**
        정정문 자체가 버그를 되살린 것이다.
      ⇒ 부정문 필터로는 못 고친다(표현이 무한하고 한국어·영어가 섞인다).
        **선언이 있으면 그것이 정본**이고 스캔은 끈다. 스캔은 선언이 없는 옛 digest 용 보조다.
    """
    toks = GLOSSARY_TOKENS.get(term_id, [])
    hits = []
    for p in _paper_index():
        declared = term_id in p["method_tags"]
        if declared or (not p.get("has_method_decl") and toks and any(t in p["blob"] for t in toks)):
            hits.append({"id": p["id"], "title": p["title"], "track": p["track"],
                         "_rank": 0 if declared else 1})
    hits.sort(key=lambda h: h.pop("_rank"))      # 선언한 논문이 먼저 (element_papers 와 같은 규약)
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
    # ⚠ 순위는 **같은 비교 묶음 안에서만**. union 을 정렬하면 legacy DOS-문턱 판독(comp2)이
    #   fixed-occ 정본과 같은 줄에 선다 (2026-08-07 리뷰 P1).
    gm = canonical_comparable("gap_eV", "gap-fixedocc-eigenvalue-v1")
    g = sorted(((v, cid) for cid, v in gm.items() if v is not None), reverse=True)
    if g:
        hi.append({"d": "2026-08-07", "t": "Band gap", "v": f"{L.get(g[0][1], g[0][1])} {g[0][0]} eV",
                   "n": f"+O(LPSOCl)가 전자 절연 최강 · **fixed-occ nscf 고유값 {len(gm)}종 안에서의 순위**다. "
                        "comp2(2.04)는 legacy DOS-문턱 판독이라 같은 축에 안 올린다 "
                        "— DOS 문턱은 ~0.3 eV 과소평가한다."})
    hi.append({"d": "2026-07-16", "t": "P–S 골격 vs Li–X 이온", "v": "ICOHP −6.0 ≫ −2.1 eV",
               "n": "강한 공유 골격 + 약한 이온결합 · comp2 Li–Br(−1.93)이 Li–Cl(−2.11)보다 약해 "
                    "격자 연화(E_VRH 22.06→20.03, B_VRH −18.2%) — 단 Pugh B/G는 3.14→2.79로 오히려 "
                    "감소라 '연성 이득'은 아님"})
    # ★ 2026-08-07 수정 (Codex 리뷰 P1 + 그보다 한 겹 더 나쁜 것).
    #   옛 카드는 `sorted(CANONICAL["MD_Ea_eV"])` 로 modelc 0.224 를 "최저"로 뽑고
    #   "⚠멀티시드 판정" 이라고 붙였다. 그런데 0.224 는 **단일 궤적 legacy 앵커**였고
    #   같은 딕셔너리의 lpsocl 0.287 은 4-seed 값이었다 — 라벨만 틀린 게 아니라
    #   **비교 자체가 프로토콜을 넘나들어서 무효**였다.
    #   지금은 멀티시드 묶음 안에서만 읽고, 오차막대가 겹치면 순위를 매기지 않는다.
    em = canonical_comparable("MD_Ea_eV", "md-ea-multiseed-v1")
    if em:
        rows = sorted(((v, cid) for cid, v in em.items() if v is not None))
        ent = {cid: CANONICAL_ENTRY.get(("MD_Ea_eV", cid), {}) for _, cid in rows}
        def _fmt(cid):
            e_ = ent.get(cid, {}); u = e_.get("uncertainty")
            return (f"{L.get(cid, cid)} {em[cid]:.3f}"
                    + (f"±{u:.3f}" if u is not None else "")
                    + (f" ({e_['n_seed']}-seed)" if e_.get("n_seed") else ""))
        lo, hi_ = rows[0], rows[-1]
        # 오차막대가 겹치는지 — 겹치면 "최저"라고 말하면 안 된다
        u0 = ent.get(lo[1], {}).get("uncertainty") or 0.0
        tied = [cid for v, cid in rows[1:]
                if abs(v - lo[0]) <= (u0 + (ent.get(cid, {}).get("uncertainty") or 0.0))]
        # ⛔ 2026-08-20 (codex 동결감사) — **상대가 비교군에서 빠지면 '최저' 는 무의미하다.**
        #   b2o3 를 게이트 미평가로 내리자 이 묶음에 modelc 만 남았고, 카드는 그 하나를
        #   "최저" 라고 쓰면서 바로 아래 설명에서는 "둘은 구분 안 된다" 고 말했다.
        #   화면 한 장 안의 자기모순이다. 보류된 멤버를 세어 순위 주장을 아예 막는다.
        import canonical as _Cg
        _GRP = "md-ea-multiseed-v1"
        held = sorted(cid for (k_, cid), e_ in CANONICAL_ENTRY.items()
                      if k_ == "MD_Ea_eV" and e_.get("comparison_group") == _GRP
                      and cid not in em)
        _held_txt = " · ".join(
            f"{L.get(c, c)}({_Cg.gate_outcome(CANONICAL_ENTRY.get(('MD_Ea_eV', c), {})) or '보류'})"
            for c in held)
        if held:
            head = ("순위 보류 — " + " · ".join(_fmt(c) for _, c in rows)
                    + f"  [비교 상대 {_held_txt} 가 비교군에서 빠졌다]")
        elif tied:
            head = "구분 안 됨: " + " ≈ ".join(_fmt(c) for c in [lo[1]] + tied)
        else:
            head = f"{_fmt(lo[1])} 최저"
        hi.append({
            # ⚠ 테스트가 이 카드를 **key 로** 집는다. 제목 문자열("Ea")로 고르면 다른 카드가
            #   먼저 걸린다 — 2026-08-25 에 b2o3 굽음 카드("단일 Ea 철회")가 그렇게 오검됐다.
            "key": "md_ea_ranking",
            "d": "2026-08-07", "t": "이온 전도 Ea (UMA) — **멀티시드 묶음 안에서만 비교**",
            "v": head,
            "n": " · ".join(_fmt(c) for _, c in rows)
                 + ". ★ 이 카드는 **같은 시드 프로토콜(md-ea-multiseed-v1)** 만 세운다 — "
                   "예전엔 단일 궤적 앵커(modelc 0.224)와 4-seed 값(lpsocl 0.287)을 한 줄에 세우고 "
                   "'멀티시드 판정'이라 적었다(2026-08-07 수정). "
                   "modelc vs b2o3 는 db 가 직접 **Δ=+0.002±0.047** 이라 적고 있으니 "
                   "둘 사이 순위를 주장하면 안 된다 — ⚠ 그 ±0.047 은 신뢰구간도 표준오차도 아니라 "
                   "**3×3×3 시드조합 분포의 표준편차**다. comp1 은 멀티시드 실행이 없어 **빠져 있다**. "
                   "★ **b2o3 도 2026-08-20 에 빠졌다** — 골격(비-Li) 게이트가 **미평가**다"
                   "(실패가 아니다). 게이트 입력인 high-T 궤적 6런(800·1000 K × 3시드)이 "
                   "--save_traj 누락으로 미보존이라 평가 자체가 성립하지 않는다. 재실행 없이는 "
                   "안 닫힌다. 그래서 이 카드는 남은 하나를 '최저' 라고 쓰지 않고 **순위 보류**다. "
                   "★ **LPSOCl(0.287)도 빠졌다** — 600 K 의 β=0.615 가 Fickian 게이트(0.8–1.2)를 "
                   "못 넘어 kb/open_items.md 가 인용 보류로 묶어 둔 값인데, 레지스트리 첫 판에서 "
                   "그 대조를 빠뜨려 정본으로 올렸던 걸 Codex 재검증이 잡았다(2026-08-07). "
                   "케이지 오염된 600 K 점을 포함한 3점 적합이라 게이트 통과 전엔 못 쓴다. "
                   "⚠ σ 절대값 인용 금지 (Nernst–Einstein, Haven=1). "
                   "출처: db/properties/canonical_registry.json"})
    # SDCP doped — ⛔ 2026-09-01 카드 교체. 옛 카드(2026-08-06)는 "doped 는 Li 를 뽑고
    # neutral 은 안 뽑는다" 를 제목으로 걸고 ΔE_extract·'neutral O↔Li 2.09 Å 배위' 를
    # 본론으로 서술했다 — 전자는 회신 P 로 부호 해석이 철회됐고(마감 문서 dE_endpoint_raw
    # citable: no), 후자는 회신 T P0-1 로 철회된 접촉 기하다(실측 4.88–5.39 Å).
    # 대시보드는 현재-facing 표면이라 철회·마감 이후 상태를 보여야 한다.
    # 정본: db/properties/sdcp_doped_closed_2026_08_28.json · sdcp_neutral_closed_2026_08_28.json
    hi.append({"d": "2026-08-28", "t": "SDCP doped × LiNiO₂(104) — **캠페인 마감** (인용 가능한 값 0건)",
               "v": "doped E_ads·ΔE 부호 전부 비인용 · 본류는 중성 C-12 로",
               "n": "08-06 UMA 재스캔이 doped 상위 자세에서 Li 2.37 Å 변위(겉보기 추출)를 관측해 "
                    "Phase-B(DFT+U 추출 에너지)를 열었지만, 회신 P 가 두 endpoint 의 자기상태"
                    "(총자화 2.378 vs 0.518 μB)·basin 동등성 미입증을 들어 **부호 해석을 철회**시켰고 "
                    "(+0.34 eV 는 내부 기록 전용), 2026-08-28 캠페인을 **조건 명시로 마감**했다. "
                    "⛔ 금지 서술 5종: doped E_ads 수치 일체 · '중성보다 강/약하게 붙는다' · "
                    "홀 위치('슬랩으로 이동/분자에 남음') · 자리선호 방향('무선호' 포함) · n=1 외삽. "
                    "허용은 회신 P 문구 4문장뿐 (마감 문서 이대로만). "
                    "⚠ neutral 쪽도 'O···Li 2.09 Å 배위' 가 08-29 철회됐다 — 좌표 실측에서 술포네이트 O 는 "
                    "표면 Li 에서 4.88–5.39 Å, wave1 실제 최단 접촉은 C–H···표면 O/Ni 2.44 Å. "
                    "반대 방향('상호작용하지 않는다')도 못 쓴다 — 신규 동결 후보 최저 자세에선 산성 O–H 가 "
                    "표면 O 와 1.83 Å 수소결합한다(MLIP 기하, DFT 미확인). "
                    "이후 본류는 **중성 C-12 외주 VASP**(사전 고정 네 잡 직접 대입의 조각 대비 D, "
                    "adsorption/binding energy 로 부르지 않는 고정기하 차등에너지)로 옮겨갔다 — "
                    "VASP 0잡 · v19 재생성 대기. "
                    "출처: db/properties/sdcp_doped_closed_2026_08_28.json · sdcp_neutral_closed_2026_08_28.json · "
                    "sdcp_c12_claim_prereg_2026_08_31.json"})
    # SEI 분해상 갭 (2026-08-07 gabia) — 협업 요청 3종 중 "band gap" 축.
    # ⚠ 값은 **fixed-occ nscf 고유값**(CLAUDE.md 규율: DOS 문턱 판독 금지). PBE 라 절대값은
    #   넓은갭 절연체에서 30–50% 과소 — 실험값과 나란히 놓지 말고 **순위**로만 쓴다.
    # ⚠ Nd 계 3종은 4f 를 원자가에 넣은 PBE 라 갭이 −0.02 eV 로 닫힌다. 이건 물리가 아니라
    #   방법의 한계다(진단용). Nd 상의 갭은 MP 의 frozen-4f 값을 인용한다.
    hi.append({"d": "2026-08-11", "t": "SEI 분해상 밴드갭 — **전자 절연의 약한 고리는 Li₃P**",
               "v": "LiCl 6.26 ▸ Li₃PO₄ 5.91/5.82 ▸ Li₂O 4.99 ▸ Li₂S 3.44 ▸ **Li₃P 0.71 eV**",
               "n": "협업 요청(Li₂O·Li₃PO₄·LiNdO₂·LiCl·Li₂S·Li₃P) 중 갭 축을 gabia 에서 완주했다 "
                    "(9종 × 6단계, 8/9 완주 · licl 은 DOS k-mesh 단계만 재실행 대기). "
                    "SEI 가 해야 할 일은 **Li⁺ 는 통과·전자는 차단** 인데, Li₃P 만 0.71 eV 로 "
                    "한 자릿수 좁다 — 전자가 새면 전해질 분해가 멈추지 않는다. "
                    "Li₃PO₄·LiCl·Li₂O 는 5–6 eV 급 절연체라 이 역할에 맞다. "
                    "Li₃PO₄ 는 β(mp-13725) 5.912 vs γ(mp-2878) 5.821 로 다형체 차이가 0.09 eV 뿐 "
                    "— 갭 축에서는 다형체 선택이 결론을 안 바꾼다. "
                    "⛔ **Nd 계 3종(LiNdO₂·Nd₂O₃·Nd₂S₃)의 갭은 우리 계산으로 정의되지 않는다** "
                    "— 두 번 시도해 둘 다 실패했다(2026-08-07). 스핀 없이는 4f³ 가 분수 점유가 되어 "
                    "갭이 닫히고(−0.02 eV), 스핀+U 로는 5원자 셀만 수렴했는데 그마저 VBM>CBM "
                    "(−6.460 eV, 물리적으로 불가능)이고 16·20원자는 전자 SCF 가 200 iteration 안에 "
                    "수렴하지 않았다. 표준 해법인 frozen-4f 를 우리 pseudo 가 안 쓴다. "
                    "→ **Nd 상 갭은 MP frozen-4f 인용.** 우리 숫자는 인용 금지. "
                    "⚠ PBE 갭은 절대값 과소 → **순위로만** 쓴다. "
                    "형성전위(대분배 phase diagram)는 별도 축으로 완료, Li⁺ 확산장벽은 BVSE 가 "
                    "화학계를 넘나드는 비교에 못 쓰인다는 게 확인돼 **NEB 3종**(Li₂S·Li₃P·Li₃PO₄)으로 간다. "
                    "상세: kb/projects/sei_products_2026_08_06.md"})
    # 파이프라인 체급 — 발표에서 제일 자주 받는 질문("문헌은 10만종인데 우리는 47종?")의 답.
    hi.append({"d": "2026-08-13", "t": "우리 체급 — **문헌의 10만 종은 계산이 아니라 조회다**",
               "v": "비싼 계산이 돈 대상: Xiao **6/104,082** · 우리 **47/47**",
               "n": "Sendek(12,831→317→21)도 Xiao(104,082→…→66→3)도 출발 풀의 물성은 "
                    "**MP·ICSD 에서 소환**한 값이라 한 종을 더 보는 한계비용이 ≈0 이다. "
                    "깔때기는 비용 피라미드라 비싼 계산(CI-NEB)은 맨 끝 소수에만 돌았다 — "
                    "Xiao 6종, Sendek 자체 DFT-MD 1종·자체 실험 0종. "
                    "우리는 조회할 DB 가 없어서(도핑 아지로다이트 x=0.05 의 E_hull·V_ox·탄성은 "
                    "어느 DB 에도 없다) **47종 × 3축을 전부 직접 쟀다** — 피라미드가 아니라 직사각형이다. "
                    "★ 발표 문장: '그들의 **훈련셋 40종**과 우리 47종이 같은 체급' + "
                    "'Sendek 의 12,831 전수에 **argyrodite 가 하나도 없다**(2016 MP 스냅샷 밖) "
                    "— DB 스크리닝의 상한은 DB 커버리지다'. "
                    "상세: docs/cascade_pipeline_guide.md §3"})
    ce = _cascade_by_element()
    top = None
    for rows in ce.values():
        for r in rows:
            if r.get("rank") == 1:
                top = r
    # ⛔ 2026-08-14 (Codex Round-3 P0-4) — 여기 "UMA #1" 이 지위 없이 홈에 떠 있었다.
    #   그 1위는 2026-06-29 취합 경계의 **역사 47종 스냅샷** 값이고, 승인된 current
    #   ranking 은 0종이다. 이름을 지우지는 않되(다음 계산 대상 선정에 쓰인다) 지위를 박는다.
    if top:
        hi.append({"d": "2026-08-14", "t": "도핑 스크리닝 — 승인된 current ranking 0종",
                   "v": f"역사 47종 스냅샷 1위: {top['dopant']} ⚠ superseded",
                   "n": ("2026-06-29 취합 경계의 순위다 — 완주분은 90종이고 재랭킹은 게이트 정의"
                         "(G3 효과 귀속 0/17 · G4 순환 · G5 로스터 상대)가 닫힌 뒤에 한다. "
                         "DFT 심층검증은 Nd₂O₃·B₂O₃ 2건뿐 · UMA 절대값은 상대비교 전용")})
    # ⚠ hBN은 db가 수치 인용을 금지한 값 — 경로 전체 폭 7 meV < 이미지당 힘오차 46 meV/Å
    #   (vgcf_hbn_neb.json: "Report as '< 0.01 eV, effectively barrierless'"). 2L2L은 층수 미수렴 상한.
    hi.append({"d": "2026-07-30", "t": "VGCF/hBN Li 확산 (CI-NEB) — 기전 판정 완료",
               "v": "gallery 2L2L 0.147 eV · 209 meV 는 **confinement** (2026-07-30)",
               "n": "같은 그래핀 1L→2L 이 자유 표면에선 +12 meV(허용오차 ~20 안 = 0), "
                    "갤러리 안에선 −207 meV → 벽 두께는 **갇힌 Li 에만** 작동한다. "
                    "hBN(<0.01)은 수치 분해능 이하 · 3L 미측정이라 0.147 은 '수렴값' 아닌 **2L 값**"})
    # comp2 disorder ensemble — ⚠ 단일 config Ea/σ 수치 인용 금지(멀티 config 판정 전, 데이터 규율)
    hi.append({"d": "2026-08-01", "t": "comp2 disorder ensemble", "v": "d=0.50 anneal+relax 파이프라인 가동",
               "n": "cfg0 3온도 완료 · 멀티 config 판정 대기"})

    # ── 2026-08-19~20 MLIP 검증 축 ────────────────────────────────────────────
    # 왜 대시보드에 올리나: 하루 동안 **모델을 의심하던 가설이 셋 다 죽었다.** 그 결과
    #   남은 논쟁이 전부 방법론으로 옮겨갔는데, 그게 안 보이면 "UMA 가 문제" 라는 옛 프레임이
    #   계속 인용된다. 값은 하드코딩하지 않고 db 에서 읽는다(파일이 없으면 카드가 안 뜬다).
    bench = _load_json(DB / "properties" / "mlip_bench_li3ps4_uma.json")
    if bench and bench.get("results", {}).get("forces"):
        f = bench["results"]["forces"]
        li = f.get("per_element", {}).get("Li", {})
        hi.append({
            "d": "2026-08-19", "t": "UMA 힘 정확도 — **범용이 전용을 이겼다**",
            "v": f"{f['MAE_eV_per_A']*1000:.1f} meV/Å"
                 + (f"  ·  Li {li['MAE']*1000:.1f}" if li else ""),
            "n": "vs 같은 test set: bespoke **35.6** · LoRA 39.2 · PET-MAD 63.9. "
                 "우리 모델은 **이 데이터를 학습한 적이 없다**. DFT 0회 (PET-MAD 공개 라벨).\n"
                 "⇒ **\"황화물 PES 연화\" 알리바이 철회.**\n"
                 "⚠ 힘 축에서만 — 에너지는 bespoke 가 앞선다. **응력·장벽은 안 쟀다.**"})

    scout = _load_json(DB / "properties" / "sei_neb_uma_scout.json")
    if scout and scout.get("runs"):
        hi.append({
            "d": "2026-08-20", "t": "NEB 셀 크기 — **작은 셀이 장벽을 부풀린다**",
            "v": "1×1×1 → 2×2×2 에서 **1.3–3.3배 하락**",
            "n": "6홉 / 4화합물, **예외 0**. li3p 0.287→**0.088** · li2o 0.648→**0.270** · "
                 "licl 0.686→**0.491** · li3po4g 0.666→**0.463**.\n"
                 "⇒ `cc333`(li3nd 3×3×3)은 **08-27 중단 — 폐기 아님**: Fmax 가 0.20–0.33 "
                 "정체 후 역주행(0.23→0.45), 마지막 7스텝이 GPU 50 h. restart 로 이어달리기 "
                 "가능하나 재개 판단 전까지 멈춤 (neb_cc333_force_history_2026_08_27.json).\n"
                 "⇒ `MIN_WIDTH_A=10 Å` 는 **최소 요건이지 수렴 보증이 아니다**.\n"
                 "⚠ UMA 값 — **장벽 절대값 인용 금지**, 셀 의존성만."})

    hi.append({
        "d": "2026-08-18", "t": "⚠ 상자 크기가 **D 를 1.65배 움직인다** (LPSOCl 600 K)",
        "v": "MSD@50ps  25.3 → **41.7 Å²**",
        "n": "3×3×1(558원자·3시드)로 확대. **기울기(D)가 1.64±0.14배** 움직인다.\n"
             "⇒ **D 절대값은 상자 크기에 묶여 있다.** 조성 간 비교도 같은 상자에서만.\n"
             "⇒ \"416원자 승격\" 처방(통계 2.7배/비용 0.6배)에 **단서** — 통계만 느는 게 "
             "아니라 **D 자체가 이동**하므로 승격하면 전 조성을 다시 돌려야 한다. "
             "1런=1시드라 **2–3시드 × 큰 셀**이 맞다.\n"
             "⚠ LPSOCl **600 K 한 점**이다 — modelc·b2o3 에 **이식 금지**(f 는 그 계의 D 에 걸린다).\n"
             "🔎 초판의 \"β 는 안 변한다\"(STO)·\"상자는 β 의 원인이 아니다\"는 둘 다 교차리뷰로 "
             "철회·완화됐다 — MTO 잣대로는 β 가 +0.05 움직인다."})

    hi.append({
        "d": "2026-08-18", "t": "⚠ 챔피언 점수 = **후보를 몇 개 뽑았느냐**",
        "v": "종별 후보 수 **15 ~ 150** (10배)",
        "n": "후보 수 ↔ 챔피언 score **r = +0.321** · 후보 수 ↔ 중앙값 score r = −0.212.\n"
             "많이 뽑힌 종이 최댓값도 높다 = **best-of-N 인공물**. 그리고 후보 수는 "
             "성능이 아니라 **화학**(치환 가능 자리 수)이 정한다.\n"
             "⛔ 세미나의 \"이건 원소 순위가 아니다\"는 **경고가 아니라 차단 사유**다."})

    # ⛔ 2026-08-25 — 옛 카드는 "b2o3 아레니우스 판정 보류(08-20)" 라고 적혀 있었다.
    #   판정은 08-23 에 났고, 보류 대상이던 Ea 0.199 는 그때 **철회**됐다.
    #   화면이 낡은 채로 "보류" 를 말하면 이미 끝난 논의를 다시 하게 된다.
    hi.append({
        "d": "2026-08-23", "t": "b2o3 아레니우스가 **굽는다** — 단일 Ea 철회",
        "v": "600→800 **0.222** · 800→1000 **0.077** eV",
        "n": "145 meV 차. **600–1000 K 를 하나의 직선으로 기술하지 않는다.**\n"
             "3시드 × 3온도 실측이고 **세 시드 모두 같은 경향**이다 (1000/800 비 1.09·1.22·1.45).\n"
             "인공물 가설 셋을 각각 실측으로 반증: β 게이트 6/6 통과 · MSD 창 스캔에서 "
             "m 은 오히려 +4 % (포화면 떨어져야 한다) · 1000 K 궤적 P 배위수 8/8 CN=4 (해리 0).\n"
             "⛔ **철회**: `Ea 0.199±0.034` · `0.206` · `0.1732` — 전부 전구간 단일 적합이다.\n"
             "✅ 쓸 수 있는 것: **저온 구간 0.2241±0.0606**(600→800, 3시드 각각 적합).\n"
             "⚠ σ(300 K) 도 같이 철회 — 재계산하니 **38±51 mS/cm**, 시드 스윙 11.5배다. "
             "표준편차가 평균보다 크다 ⇒ 절대값은 자릿수도 안 잡힌다."})

    hi.append({
        "d": "2026-08-25", "t": "⚠ β 는 **시간·이온 대조를 못 가른다**",
        "v": "MTO·STO 가 **순위를 뒤집는다**",
        "n": "LPSOCl 600 K 에서 시간 4배(200→800 ps) vs 이온 9배(27→243) 를 비교했다. "
             "생산시간을 맞춰 축이 하나씩만 움직인 깨끗한 대조였는데 —\n"
             "MTO 기준 0.76 / 0.76 / **0.81**(이온판 1등) · STO 기준 **0.85** / 0.83 / 0.80(기준판 1등).\n"
             "효과 크기(≤0.09)가 **추정자 간 차이(≤0.09)와 같은 규모**다 ⇒ 안 갈렸다.\n"
             "⛔ 중간보고의 \"시간 0/3 · 이온 2/3\" 은 **개별 시드**로 판정한 것이라 철회. "
             "앙상블 평균(AVG3)이 정본이다.\n"
             "✅ 대신 건진 것: c-행 잔차 검정에서 **modelc 700 K(0.029) · 900 K(0.041) 가 "
             "케이지 절편** ⇒ D 인용 가능. 다만 \"세 계 같은 온도 집합\" 규칙 때문에 "
             "modelc 만 5점으로 그릴 수는 없다."})

    hi.append({
        "d": "2026-08-21", "t": "단일 Li NEB 은 이 계에서 **성립하지 않는다**",
        "v": "홉 100 % 인데 이웃이 **2.41 Å** 같이 움직인다",
        "n": "comp1(Li₆PS₅Cl, 무질서) 에서 Li 공공 홉은 **elementary 과정이 아니다.**\n"
             "설정 넷으로 갈랐다 — 독립 이완 끝점은 밴드가 2.71 eV 로 찢어지고, "
             "결합 끝점 + 자유 이완은 홉이 **35 % 만** 일어나 \"고쳐진 것처럼\" 보였다. "
             "이동 Li 를 고정해 100 % 홉을 시키자 협동 이동이 2.41 Å 로 되돌아왔다.\n"
             "수렴한 밴드가 **시작점보다 0.283 eV 낮은 구간**을 지난다 ⇒ "
             "\"Li 하나가 이웃 자리로 간다\" 가 이 계의 반응좌표가 아니다.\n"
             "⛔ 우리 NEB 장벽을 원고·발표에 **인용하지 않는다.**\n"
             "✅ comp1 정본 Ea 0.2532 는 **MD/MSD 아레니우스** 값이다 — 협동 이동이 지배적인 "
             "계에서는 MD 가 옳은 관측이고, 이 결과가 그걸 지지한다."})

    hi.append({
        "d": "2026-08-24", "t": "⭐ comp1 갭을 **재현했다** — provenance 구멍 닫힘",
        "v": "VBM 2.1281 · CBM 4.1937 · **gap 2.0656 eV**",
        "n": "정본 기록(2.066)과 소수 넷째 자리까지 일치. irr k-point **170** 도 기록과 같다 "
             "— 셋업 계보까지 확인됐다.\n"
             "⇒ 두 가지가 **동시에** 닫혔다: (1) 실행 입력·출력이 없던 provenance 구멍, "
             "(2) \"DOS 문턱 오염 아닌가\" 하는 방법 비동질 의심. 재계산이 둘 다 증명했다.\n"
             "⚠ PBE 갭은 넓은 갭 절연체에서 30–50 % 과소평가한다 — 실험과 나란히 놓지 말 것."})

    # ── 2026-08-26 ────────────────────────────────────────────────────────
    hi.append({
        "d": "2026-08-26", "t": "🔴 β 문턱 **0.8 을 폐기한다** — 근거가 없었다",
        "v": "우리 운영점에서 **거짓탈락 50 %**",
        "n": "문헌을 뒤졌더니 **β 문턱을 쓰는 데가 없다.** He/Zhu/Mo 2018 은 *확산 이벤트 수*로, "
             "Kahle 2020 은 *창 스캔 + 자동수렴*으로 거른다. 0.8 은 **우리 관례**였고 "
             "\"문헌도 0.9·0.95 를 쓴다\" 던 우리 문서의 문장은 **출처가 없어 철회**했다.\n"
             "귀무 스윕으로 재봤다 — **완벽히 Fickian 인 계**에 우리 실측 절편만 넣으면:\n"
             "· 절편 2 Å² · 홉 13.9(=modelc·b2o3 600 K) → 귀무 β 중앙값 **0.80**, P(β<0.8) = **50 %**\n"
             "· 절편 4 Å² · 홉 8.4(=LPSOCl 600 K) → 귀무 중앙값 **0.58**. "
             "관측 0.615 는 오히려 **그 위**다 ⇒ 탈락이 아니라 정상이었다.\n"
             "⛔ **정정(08-27 Codex 회신 F)**: 초판이 붙인 *\"시드 산포는 홉 수(−0.78)를 따른다 — "
             "He 2018 재현\"* 은 **철회**한다. `n_hop` 은 사실상 평균 D 이고(ρ=**+0.95**), "
             "`CV = sd/mean` 의 **분모가 그 평균 D** 라 상관의 상당 부분이 기계적이다 — "
             "평균 D 를 그대로 넣어도 −0.73 이 나온다. 두 상관의 차도 유의하지 않다(p≈0.09).\n"
             "✅ 대체 (08-27 개정): **① `D_inc` 구간 증분기울기** — 상수 절편이 대수적으로 소거돼 "
             "케이지면 창 따라 평평하다 ② 실제 점프 수 ③ block/seed CI. "
             "β 는 **경보**, c 행은 t=0 외삽이라 **보조**다.\n"
             "⛔ β=1 자체는 물리다(MSD=6Dt) — 폐기하는 건 **0.8 이라는 칸막이**뿐이다.\n"
             "⛔⛔ **면죄부가 아니다.** 게이트는 **양방향으로** 틀렸다 — modelc/700 K 는 탈락(0.76)했지만 "
             "케이지 절편이라 D 인용 가능이고, b2o3/700 K 는 통과(0.85)했지만 여섯 창 전부 β 평평·m −22.8% 다. "
             "⚠ **단 b2o3 쪽은 약해졌다(08-27)** — 그 '여섯 창' 중 늦은 둘은 100 ps 궤적에서 "
             "**같은 구간을 두 번 찍은 것**이었다(도구 버그, 수정됨). 최대 lag 이 궤적 길이에 닿아 "
             "시간원점이 거의 없는 구간이라 **거짓 통과의 확정 사례가 아니라 시사**로 낮춘다. "
             "modelc/700 의 거짓 탈락 쪽은 그대로다. "
             "인용 위험 **18건 중 β 사유는 2건**뿐이고, 그 2건조차 안 풀린다 — LPSOCl 600 K 는 MTO 곡선에서 "
             "**c 3.05→7.02 · m −24.5%** 라 β 와 무관하게 아확산 서명이 남는다.\n"
             "→ 바뀐 건 목록이 아니라 **진단명**이다: \"β 가 낮다\"(원인 불명) → **표본 부족**(홉 수).\n"
             "⚠ 처방이 \"셀을 키워라\" 하나인 것은 **아니다** — 레버가 넷이고 각각 다른 병을 고친다. "
             "**MTO·창 스캔은 공짜로 잡음**을 줄이고(시드 산포 0.52→0.06, 8.7배), "
             "**셀은 편향**을 건드린다(D 가 1.64–1.70배 움직인다). **잡음은 표본으로 줄지만 편향은 안 준다.** "
             "시간 연장만 역효과였다(β 0.64→0.37).\n"
             "⛔ 그리고 **셀이 β 를 고친다는 건 아직 미확정**이다 — 창 스캔은 오히려 큰 셀이 나쁘다"
             "(작은 셀 β 0.76→0.98 회복 vs 큰 셀 0.87 정체·c +128 %). 가르는 건 800 ps 런이다."})

    hi.append({
        "d": "2026-08-26", "t": "UMA 힘 softening — **아키텍처가 아니라 훈련셋**이다",
        "v": "UMA 0.987–0.999 vs **SevenNet-0 0.790**",
        "n": "같은 251 프레임·같은 DFT 정답지(Batzner 2022 LiPS)에서 두 GNN 을 나란히 놓았다. "
             "softening slope(1.0 = 무연화)가 **UMA 0.9874 / SevenNet-0 0.7899** — "
             "SevenNet 은 힘을 **21 % 무르게** 본다.\n"
             "Li₃PO₄(Musaelian 2023)에서도 UMA 는 melt 0.9995 · quench 0.9973 로 "
             "비평형 구간까지 안 무너진다(Δ −0.002).\n"
             "⇒ OMat24 의 \"softening 은 아키텍처가 아니라 훈련 데이터\" 주장이 "
             "**우리 화학계에서 독립 재현**됐다 (T1b).\n"
             "⚠ Pearson r 로는 안 보인다 — r 은 스케일 불변이라 0.979 로 멀쩡해 보인다. "
             "기울기를 따로 재야 잡힌다.\n"
             "⛔ 그래서 b2o3 골격 붕괴는 softening 으로 설명 안 된다 — 다른 원인이다."})

    hi.append({
        "d": "2026-08-26", "t": "심포지엄 판독 하루치 — **T·Q 원장**",
        "v": "T 17건 · 우리 기록 **정정 8건**",
        "n": "이상욱 교수님 세션(덱 18 p + 구술 31:44)을 판독하고 논문 6건을 litdb 에 넣었다. "
             "그 과정에서 **우리 기록 8건이 틀렸다는 걸 확인**했다 — 그게 이 날의 실제 산출이다.\n"
             "· T2 **전제 붕괴**: 양성자는 PS₄ 말단 S 가 아니라 자유 S²⁻(4d)로 간다 ⇒ PS₄₋ₓOₓ = 0\n"
             "· T1b **닫힘**: 위 softening 카드\n"
             "· Y 자리 선호 **닫힘**: UMA 28.3 ↔ DFT 30.5 meV/atom (방향·크기 일치)\n"
             "· #1/#2 **막힌 게 시간이 아니라 셀 크기**였다 — 3×3×1 이 원자 9배에 벽시계 1.2배\n"
             "⚠ `Q` 번호는 **문서마다 다른 뜻**이다 (같은 Q3 이 네 문서에서 네 가지). "
             "부를 때 문서명을 붙인다 — 체계는 `kb/CODES.md`.\n"
             "→ 전체 원장은 **T·Q 원장** 페이지에서."})

    hi.append({
        "d": "2026-08-27", "t": "NEB 3×3×3 중단 — **장벽이 아니라 힘이 말했다**",
        "v": "50 GPU-시간이 Fmax 를 **2배 나쁘게**",
        "n": "li3nd c→c 셀 수렴 확인용 3×3×3 NEB 를 step 30 에서 멈췄다. 두 지표가 반대를 가리켰다:\n"
             "· **장벽**: 3.00 → 0.880 → **0.128 eV 단조 감소** (수렴처럼 보인다)\n"
             "· **힘**: 4.64 → 0.277 로 잘 내려오다 **step 14–27 정체**, "
             "step 28–30 에 0.245 → 0.288 → **0.451 역주행**. 문턱은 0.05.\n"
             "마지막 7스텝 = **GPU 50시간**을 써서 Fmax 를 0.2296 → 0.4514 로 만들었다.\n"
             "⇒ 장벽이 내려가는데 힘이 커지면 **경로가 아직 움직이는 중**이다 — 0.128 은 "
             "수렴값이 아니라 **지나가는 값**이다. 미수렴 profile 에 오차막대가 없다는 "
             "교차리뷰 판정이 우리 런에서 확인됐다.\n"
             "⛔ **0.128 eV 인용 금지** (힘 9배 초과 · CI 꺼짐 · 힘 역주행 중). "
             "2×2×2 수렴값 0.229 와 나란히 놓아 '셀 효과' 를 말하는 것도 금지 — 같은 수렴 상태가 아니다.\n"
             "⛔ 우리가 붙였던 *\"QE 문턱 0.05 는 인용에 느슨하다\"* 는 **철회** — "
             "그건 VASP 의 EDIFFG 를 잘못 옮긴 것이고 **0.05 가 QE neb.x 기본값**이다. "
             "중단 근거는 힘 역주행 하나로 충분하다.\n"
             "✅ 폐기가 아니라 **중단** — restart 가능하고 체크포인트(step 30 path)를 떴다."})

    hi.append({
        "d": "2026-08-27", "t": "유한크기 — **modelc 도 같은 방향**, 단 구분은 못 한다",
        "v": "셀 확대 시 D 가 **1.40×** (lpsocl 1.64–1.70×)",
        "n": "*'세 계를 같은 5.67 Å 상자에 두는 게 공정하다'* 는 가정을 재려고 "
             "**modelc 3×3×1 600 K** 를 돌렸다(558원자, 완주).\n"
             "· 큰 셀 **1.449e-5** vs 작은 셀 3시드 평균 1.037e-5 ⇒ 비 **1.40**\n"
             "· lpsocl 은 **1.64–1.70**\n"
             "⛔ **정정(08-27 회신 H)**: 초판이 붙인 `1.40 ± 0.35` 의 **오차막대를 뗀다.** "
             "큰 셀이 1시드라 **모집단 비의 CI 는 만들 수 없다** — 분모 산포만으로 만든 구간을 "
             "비의 CI 처럼 쓰면 안 된다. 표기는 `R_obs = 1.40` (탐색적 관측비) · "
             "분모 민감도만 제시 · **분자 시드간 불확실도 = 추정 불가** 다.\n"
             "⚠ 모집단 CI 를 시작하려면 **matched-size pair 가 최소 3개**(가능하면 4개 이상) "
             "필요하고, pairing 은 속도 시드가 아니라 **quenched-disorder realization** 에 걸어야 한다.\n"
             "✅ 말할 수 있는 것: **modelc 도 셀을 키우면 D 가 커진다** — 유한크기 민감성이 "
             "lpsocl 만의 현상이 아니다.\n"
             "⛔ 말할 수 없는 것: 공정성 가정의 검정. 그건 f(T) 의 **T-기울기**(dΔ/d(1/T))라 "
             "**두 온도가 최소**인데 이건 600 K 한 점이다.\n"
             "⛔ **1.40 vs 1.64 를 가르는 건 포기한다** — 차이가 log 로 **0.158** 인데 실용 "
             "허용폭 log(1.2)=0.182 **안**에 있고, 작은 셀 CV 25–33 %(log SD 0.25–0.32)로는 "
             "80 % 검정력에 **집단당 76–130 런**이 필요하다. 우리 상한은 6런이다. "
             "그 6런은 대신 **같은 셀 형상·matched disorder 에서 Δ_s(T) 의 큰 변화를 탐색**하는 데 쓴다.\n"
             "⛔ `Ea_eV: null` 은 오류가 아니다 — 한 온도라 아레니우스가 성립하지 않는다."})

    hi.append({
        "d": "2026-08-27", "t": "⚠ 100 ps 궤적은 **c-추세 판정을 못 한다**",
        "v": "창 6개 중 primary **2개** — 추세표가 안 나온다",
        "n": "lag 이 궤적 길이에 가까우면 **그 lag 의 시간원점이 ≈(T−t)/Δt 로 0 에 수렴한다.** "
             "그래서 창을 등급으로 나눴다 — primary(t₂≤0.5T) · sensitivity(0.5–0.7T) · "
             "**exploratory_only(>0.7T, 판정에서 제외)**.\n"
             "결과가 아프다: **100 ps 에서는 primary 가 2개**뿐이고 추세 판정에 4개가 필요해 "
             "**표가 아예 안 나온다.** 우리 `arrhenius_6pt` **12런이 전부 100 ps** 라 "
             "그 c-추세 판독은 **형식적으로 판정 불가**가 됐다.\n"
             "800 ps 면 9창 중 7개가 살아 정상 작동한다 — **지금 800 ps 를 도는 직접적 이유다.**\n"
             "⛔ 계기는 우리 도구 버그였다: 창 목록이 고정이라 tmax 100 ps 에서 `50-150` 과 "
             "`50-200` 이 **같은 50–100 을 두 번 찍고** 다른 라벨로 나왔다. 값이 같으니 "
             "\"두 창이 일치한다\" 로 읽혔고, 그게 어제 c-추세 주장의 근거였다."})

    hi.append({
        "d": "2026-08-27", "t": "⛔ 철회 — \"NEB 우회로가 없다\" 는 확인 안 하고 한 말",
        "v": "1.240 Å ← **물리인지 미확정**",
        "n": "🔴 **이 카드는 같은 날 저녁 교차리뷰 I 로 두 군데가 무너졌다.** 원문은 아래 보존.\n"
             "① **\"싼 우회로가 물리적으로 막혔다\" 는 틀렸다.** 막힌 건 *중점법*과 *saddle 이식* "
             "둘뿐이고, 그 둘만 '변위장이 국소' 라는 전제를 쓴다. "
             "**dimer / minimum-mode following 은 전 원자를 자유롭게 두므로 그 전제를 안 쓴다** — "
             "step 19/30 의 최고에너지 image 와 tangent 를 출발점으로 1차 안장을 직접 찾는다. "
             "*\"제3의 길이 없다\"* 는 우리가 **확인하지 않고** 한 말이다.\n"
             "② ~~1.240 Å 자체가 물리인지 미확정이다~~ → **저녁 측정에서 기각.** 그 가설(원자 순서 zip "
             "이라 강체 표류·라벨 교환이 섞였다)은 그럴듯했지만 **틀렸다**: 병진 **0.0065–0.052 Å** · "
             "라벨 재대응 **0 개**. → 아래 08-27 저녁 카드.\n"
             "───────── 이하 원문 (2026-08-27 낮) ─────────\n"
             "3×3×3 NEB 를 멈추고 나서 '싼 대안이 있나' 를 다시 뒤졌다. **이미 있었고, "
             "이미 시도됐고, 옳게 거부됐다.**\n"
             "`tools/sei/symmetric_saddle.py` (2026-08-16) — 대칭 홉이면 중점에 뛰는 원자를 "
             "고정하고 나머지를 이완해 **끝점 1 + 안장 1 = 2 relax** 로 끝낸다. "
             "full NEB 의 ~560 SCF 대신. 반경 수렴 스캔까지 들어 있다.\n"
             "⛔ 그런데 cc333 에서 **`고정 대상 원자가 1.240 Å 움직인다`** 로 막혔다. "
             "원인은 반경이 아니라 물리다 — **Li 하나가 뛸 때 Nd 부격자가 재배열한다** "
             "(변위 0.547×7 · 0.64×2 · **1.12×6** · 1.28×1, 대칭 다중도를 따른다 ⇒ 무질서 아님).\n"
             "⇒ *'뛰는 원자 외에는 가만있다'* 는 전제가 이 계에서 성립하지 않는다. "
             "R 을 천장(λ₁/2 = 7.78 Å)까지 올리면 자유영역이 셀을 다 먹어 방법이 소멸한다.\n"
             "🔑 **그래서 교차리뷰가 준 saddle 이식 계획도 같은 벽에 부딪힌다** — "
             "'2×2×2 국소 변위를 3×3×3 에 이식' 은 변위가 국소일 때만 성립하는데 "
             "Nd 6개가 1.1 Å 씩 움직인다. 회신도 실패조건을 명시했다: "
             "*'반경이 셀 최소길이의 절반까지 가도 안정 안 되면 국소 이식 가정이 실패'*. "
             "**우리는 그 답을 이미 갖고 있다.**\n"
             "⚠ 그리고 이건 3주 NEB 가 낭비였다는 뜻이 **아니다** — 싼 길이 먼저 시도됐고 "
             "물리적 이유로 막혀서 비싼 길로 간 것이다. 순서가 맞았다."})

    hi.append({
        "d": "2026-08-27", "t": "🔴 **2×2×2 도 똑같이 움직인다** — 우리가 안 재봤을 뿐이다",
        "v": "ccpath **1.035 Å** (한 번도 안 잼)",
        "n": "P0-1 정렬 진단을 gabia 에서 돌렸다. **회신의 가설이 먼저 기각됐다**: "
             "강체 병진 **0.0065–0.052 Å** · 라벨 재대응 **0 개** ⇒ 1.240 은 correspondence 오류가 아니다. "
             "그런데 같은 실행이 **2×2×2 대조군**을 재면서 우리 쪽을 무너뜨렸다.\n"
             "| 이완 좌표 (정렬 후) | ccpath 2×2×2 | cc333 3×3×3 |\n"
             "| 홉 제외 최대 | **1.035 Å** | 1.234 Å |\n"
             "| 이완 후 홉 거리 | 4.207 Å | 4.203 Å |\n"
             "| 끝점 이완 | **수렴** | ⛔ 미수렴 |\n"
             "⛔ **반증된 문장**: *\"3×3×3 에서만 Nd 가 재배열한다 ⇒ 작은 셀에서 억제됐던 이완이 "
             "큰 셀에서 풀린 것\"*. 그 대조는 **ccpath 의 갓 지은 좌표(0.000)** 와 "
             "**cc333 의 이완 좌표(1.240)** 를 나란히 놓은 것이었다 — 08-17 표의 ccpath 칸은 "
             "**`—`(안 잼)** 이다. **오늘만 세 번째로 나온 같은 종류의 실수: 다른 것을 비교하고 "
             "그 차이를 물리라고 불렀다.**\n"
             "🔧 **게이트가 cc333 만 막은 이유도 물리가 아니라 장부였다.** `build_frozen` 은 "
             "`endpoint_dir()` 가 고른 폴더의 `relax.in` 을 읽는데, cc333 은 `_r2` 가 있어 "
             "**이완 좌표**를, ccpath 는 없어서 **갓 지은 좌표**를 봤다. 같은 기준으로 재면 "
             "이완 좌표에선 **둘 다 막히고**(1.035·1.234, 문턱의 20배) 갓 지은 좌표에선 "
             "**둘 다 거저 통과**한다(정의상 0 이라 검사가 성립 안 함).\n"
             "🚨 이건 **살아있는 위험**이었다 — ccpath 에 고정셸을 걸었으면 0.000 으로 통과시키고 "
             "1.035 Å 어긋난 원자를 못박아 그 차이가 **Ea 에 직접** 들어갔다. 게이트를 "
             "이완 좌표 기준으로 고쳤다(회귀 3건, 전부 음성 경로).\n"
             "✅ **결론 ① 은 살아남는다 — 근거를 바꿔서**: 고정셸을 못 쓰는 이유는 "
             "*3×3×3 이라서*가 아니라 **두 셀 다 이완하면 홉 외 원자가 1 Å 움직여서**다."})

    hi.append({
        "d": "2026-08-27", "t": "🔑 변위장이 **거리에 따라 안 준다** — P0-2 가 급해졌다",
        "v": "6–8 Å 이 4–6 Å 보다 **높다**",
        "n": "크기가 아니라 **모양**이 점결함 응답인지 전역 재배열인지를 가른다.\n"
             "| 거리 [Å] | ccpath (수렴) | cc333 (미수렴) |\n"
             "| 2–4 | 0.954 | 0.441 |\n"
             "| 4–6 | **0.316** | 0.375 |\n"
             "| 6–8 | (셀 밖) | **0.439** ← n=50, 가장 큰 껍질 |\n"
             "| 8–∞ | — | 0.160 |\n"
             "ccpath 는 **단조감소** = 점결함 응답의 교과서 모양. cc333 은 **안 준다.**\n"
             "해석 둘, **못 가른다**: ① **회신 P0-2 가 맞다** — 3×3×3 이 여는 q≈1/3 모드로 "
             "**전역 재배열**. 그러면 **끝점 정의 자체가 무효**고 **MD 로 옮겨도 해결 안 된다** "
             "(같은 불안정한 구조에서 낸 MD Ea 도 조건부 값이다). ② 단순히 **미수렴 optimizer 의 "
             "배회** — cc333 끝점 둘 다 nstep 한도에서 끝났다.\n"
             "⇒ **다음 한 수는 P0-2 control**: 공공 없는 pristine 3×3×3 에 대칭 끄고 rattle 여러 개 → 이완. "
             "**3주 재개보다 먼저다.**\n"
             "🧩 그리고 아직 설명 못 하는 게 하나 남는다: ccpath 는 **수렴한** 이완에서 1.035 Å 협동 "
             "변위를 보이는데, 그 셀에서 **CI 가 장벽을 1 μeV 만 바꿨다**(0.228980 → 0.228981). "
             "협동 변위가 있는데 안장이 중점에 있었다 — 이 둘이 어떻게 양립하나."})

    hi.append({
        "d": "2026-08-27", "t": "회신 I — **협동 이동은 장벽을 무효화하지 않는다**",
        "v": "우리 잠정판단 **기각**",
        "n": "우리 주장은 *\"li3nd 도 comp1 처럼 협동 이동이니 NEB 는 틀린 관측량이다 ⇒ 3주 재개 말자\"* 였다. "
             "**기각됐다.**\n"
             "📐 정적 장벽은 전 원자 3N 차원 PES 에서 두 metastable basin 을 잇는 경로다 — "
             "**\"한 원자만 움직여야 한다\" 는 조건이 없다.** Nd 집단이완이 무효화하는 것은 "
             "*중점법 · 국소 frozen-shell · saddle 이식 · \"단일 Li 직선 홉\" 이라는 이름* 이지, "
             "**전 원자를 자유롭게 둔 full NEB 의 collective MEP 자체가 아니다.** "
             "(실제 superionic 계에서도 concerted pathway 를 NEB 로 계산한다 — He–Zhu–Mo 2017)\n"
             "🔍 **comp1 과 li3nd 는 다르다.** comp1 은 근거가 셋이었다: 이동 Li 를 **고정해야** "
             "100 % 홉 유지 · 나머지 Li **2.41 Å** 재배열 · 수렴 밴드가 시작점보다 **0.283 eV 낮은** "
             "basin 통과 ⇒ **반응좌표가 붕괴**했다. li3nd 는 반대 증거다: 대칭 등가 c→c 끝점 · "
             "끝점 ΔE **4.4 meV** · 이동 Li 가 놓인 자리에서 **0.03 Å** 만 이동. **자동 이식 불가.**\n"
             "✅ 우리가 부탁한 자기검증(*\"3주가 비싸서 안 하고 싶은 것과 안 해야 하는 것은 다르다 — "
             "거기를 봐 달라\"*)에 답이 왔다: **우리는 비싸서 안 하고 싶은 쪽이었다.**\n"
             "⇒ 판정은 **HOLD**(영구 폐기 아님). 먼저 1–2 일짜리 P0 셋: ① 끝점 정렬 진단 "
             "② pristine 3×3×3 rattle control ③ 체크포인트 완전성. 그 뒤 조건부 재개."})

    hi.append({
        "d": "2026-08-27", "t": "P0-2 — Nd 재배열이 **공공 때문인지 셀 때문인지** 안 갈렸다",
        "v": "MD 로 옮겨도 **해결 안 됨**",
        "n": "*\"2×2×2 엔 없고 3×3×3 에만 나타났다\"* 는 사실은 **두 해석과 모두 양립한다**:\n"
             "① 공공이 더 넓은 셀에서 Nd 이완을 **유발**했다\n"
             "② 2×2×2 가 표현하지 **못하는** q≈1/3 구조 모드가 3×3×3 에서 열린 것이다\n"
             "②라면 Li 홉이 Nd 를 끌고 간 게 아니라 **큰 Fm-3m 셀 자체가 숨은 재구성에 불안정**한 것이고, "
             "그때는 **끝점 정의 자체가 무효**다.\n"
             "🔴 그리고 이 경우 **MD 로 바꿔도 자동 해결이 안 된다** — 같은 불안정한 구조에서 낸 "
             "MD Ea 도 조건부 값이다. 우리가 이 지점을 못 봤다 (\"NEB 대신 MD\" 가 탈출구인 줄 알았다).\n"
             "⇒ 가장 싼 control: **공공 없는 pristine 3×3×3** 에 대칭 끄고 작은 random rattle 여러 개 → 이완. "
             "관측한 Nd 변위모드 방향으로 ±δ. 공공 끝점도 서로 다른 rattle 에서 **같은 basin 으로 복귀**하는지."})

    hi.append({
        "d": "2026-08-27", "t": "NEB 재개 방법 — **좌표는 살리고 Broyden 만 초기화**",
        "v": "Fmax 0.200→0.451 은 **위상 변화 신호가 아니다**",
        "n": "우리는 (a) step 30 이어달리기 vs (b) 처음부터 둘 중 고르려 했는데 **제3안이 답이다.**\n"
             "🔧 `li3nd.path` 와 **이미지별 SCF 상태는 유지**, `li3nd.broyden` **만** 따로 보존 후 "
             "활성 폴더에서 제거 → `restart_mode='restart'` 명시 → **`CI_scheme='no-CI'` 로 먼저** → "
             "필요하면 `ds` 를 줄여 **5–10 스텝만** stage-1 예산으로.\n"
             "❌ 처음 선형보간으로 돌아가면 이미 찾은 **collective displacement field 를 버리므로 더 나쁘다.**\n"
             "📉 **Fmax 역주행은 위상 변화의 증거가 아니다** — Broyden overshoot · 최대잔여력 image 교체 · "
             "auto-CI 최고점 교체 · image spacing kink · SCF force noise 전부 같은 모양을 낸다. "
             "그리고 **장벽이 내려가면서 힘이 올라가는 것도 모순이 아니다: NEB barrier 는 최적화 중 "
             "단조 목적함수가 아니다.**\n"
             "🔎 진단할 값: 최고에너지 image 번호 · 최대잔여력 image 번호 · Li 의 hop-axis 진행도 · "
             "인접 image PBC-unwrap 거리 · tangent 각도 · Nd collective-order amplitude · site occupancy.\n"
             "⚠ 경고선: `max(dᵢ)/median(dᵢ) > 2` · tangent 회전 > 60° · Li 진행도 **역행** · 새 site occupancy. "
             "**중단·분할**: 90° 이상 kink 또는 새 stable basin.\n"
             "📦 체크포인트는 `li3nd.path` **하나가 아니다** — `.broyden` · **이미지별 SCF(tmp/)** · "
             "`neb.in`/`neb.out` · protocol/meta/hash 까지."})

    hi.append({
        "d": "2026-08-27", "t": "생성기가 `--restart` 를 **조용히 버리고 있었다**",
        "v": "no-CI + restart → `from_scratch`",
        "n": "🐛 `build_neb_inputs.py` 는 `ci_scheme != \"no-CI\" and restart` 일 때만 "
             "`restart_mode='restart'` 를 썼다. `--restart` 를 **2단계 CI 전용 플래그**로 설계했기 때문인데, "
             "실제 용례는 둘이다: ① **중단된 no-CI 런 이어달리기** ② no-CI 수렴본 위에 CI. "
             "①이 조용히 `from_scratch` 로 샜다 — 체크포인트를 두고 **처음부터** 도는 길이다.\n"
             "✅ 고쳤다: `--restart` 단독 존중 + **`<tag>.path` 가 없으면 거부**(QE 는 없어도 조용히 처음부터 돈다).\n"
             "🟢 **다만 멈춰 있는 체크포인트는 멀쩡하다** — 러너 `prep_resume` 이 2026-08-24 부터 "
             "실행 직전에 `neb.in` 의 `restart_mode` 를 고쳐 쓴다(같은 사고를 한 번 겪고 넣은 장치). "
             "생성기 버그는 *다음 재빌드* 때 물었을 것이다.\n"
             "🐛 대신 러너에 **세 번째 구멍**이 있었다: `prep_resume` 은 이력을 `neb.out` 에서 센다. "
             "`ci` 단계가 `mv neb.out neb.out.noCI` 를 하고 나면 이력이 0 으로 보여 **손을 떼고**, "
             "그러면 `from_scratch` 가 살아있는 `.path` 위에 그대로 선다. 백업 폴백으로 고쳤다 (selftest ⑦)."})

    hi.append({
        "d": "2026-08-27", "t": "공공 농도 분모가 틀렸다 + `degauss` 가 장벽과 **같은 자릿수**",
        "v": "1/24 · 1/81 (Li 부격자)",
        "n": "🔢 `1/32`·`1/108` 은 **전체 원자 자리** 기준 결손률이었다. 공공은 Li 자리에만 있으므로 "
             "분모는 **Li 부격자**여야 한다: **2×2×2 = 1/24 = 4.17 %** · **3×3×3 = 1/81 = 1.23 %**. "
             "비(3.375)는 같아 결론은 안 흔들리지만 적힌 숫자가 틀렸다. "
             "(검산: 8셀×4원자=32자리 중 Li 24 · 27셀×4=108 중 Li 81 — 우리 원자 수 31·107 과 정확히 맞는다)\n"
             "⚠ 그리고 **이걸 '교란' 이라 부른 것이 반쯤 틀렸다**: 목표가 *희박한 단일공공 장벽*이면 "
             "'공공 1개를 두고 셀을 키운다' 는 **dilute limit 으로 가는 표준 경로**지 가려야 할 두 교란이 아니다. "
             "다만 **두 점으로는 sensitivity 까지**이고 희박한계 수렴·상한·하한은 못 말한다 "
             "(두 크기에서 장벽이 단조일 이유가 없다).\n"
             "⚡ **`degauss = 0.02 Ry ≈ 0.272 eV` 이고 장벽이 0.229 eV 다 — 같은 자릿수다.** "
             "그게 곧 0.272 eV 오차라는 뜻은 아니지만, 같은 k-point 밀도에서 "
             "`0.02 → 0.01 → 0.005 Ry` 사다리를 타야 한다. **우리는 이 검사를 한 적이 없다.**\n"
             "📌 또 하나: NEB 가 주는 건 **이미 있는 공공의 이동 장벽 E_m** 이다. intrinsic 평형 공공 수송은 "
             "`E_f^v + E_m` 이라 **0.229 를 MD 아레니우스 Ea 와 바로 동일시하면 안 된다.**"})

    hi.append({
        "d": "2026-08-28", "t": "🔴 **3,615개가 설계 3,615개가 아니었다**",
        "v": "고유 설계 **1,145**",
        "n": "교차리뷰 K 가 코드를 짚었고 **실측으로 확인했다.** "
             "`substitute_compound.py` 가 `n_units = max(1, round(n_fu_actual × x))` 로 자리 수를 정하는데, "
             "우리 셀은 **`n_fu_actual = 4` 가 전 행**이다. 그러면 `round(4 × 0.02) = 0 → max(1,0) = 1` 이라 "
             "**x020 · x050 · x100 이 전부 실제 x = 0.25 로 붕괴**한다.\n"
             "| 실측 | |\n| 명목 x 분포 | x020 1205 · x050 1205 · x100 1205 |\n"
             "| 명목 x 지운 고유 설계 | **1,145** |\n| Li 자리 alias 까지 정규화 | **1,035** |\n"
             "⇒ 3,615 행은 **1,145 설계 × 중복 라벨 3개**다. 이걸 독립 후보처럼 순위·CV 에 넣으면 "
             "**pseudo-replication** 이다. `concentration` 열이 전 행 0.25 인 것을 우리는 "
             "*'축이 얼어 있다'* 로 읽었는데, 실제로는 **세 라벨이 한 설계로 겹친 것**이었다.\n"
             "⛔ **당분간 못 쓰는 말**: \"3,615개 중 상위\" · \"전체 설계공간 최적\" · "
             "결측을 예측한 전역 leaderboard. 먼저 `실제 조성 + 원자매핑 시작구조 해시`로 묶고 "
             "반복 branch 의 중앙값·산포를 같이 보고해야 한다."})

    hi.append({
        "d": "2026-08-28", "t": "A3 Pareto — **160/681 은 물리 결론이 아니라 진단이다**",
        "v": "유효 3축이면 **18/681**",
        "n": "낮에 A3 를 돌리고 *'front 가 23.5 % 라 Pareto 가 후보를 못 좁혔다'* 고 적었다. "
             "교차리뷰 K 가 **축 두 개가 이미 무효 판정된 것**이라고 짚었다 — "
             "`screen_dV_over_V0`(무의미) · `screen_de_per_atom` 절대값(인용 금지), "
             "근거는 `cascade_pipeline_fixes_2026_08_19.md`.\n"
             "| 축 조합 | front |\n| 기록된 5축 | 160 / 681 |\n| dV 만 제거 | **34 / 681** |\n"
             "| 유효 3축(BVS·migration·Pugh) | **18 / 681** |\n"
             "⇒ 160 은 *'Pareto 가 못 좁혔다'* 는 물리가 아니라 **축 계약과 분석 단위가 아직 "
             "안 정해졌다**는 진단이다. 그리고 681 자체도 위 카드대로 **~3배 부풀려져** 있다.\n"
             "⛔ 정본은 이미 **승인된 ranking 0종**을 기록하고 있고 발표 대본도 leaderboard·Pareto·winner 를 "
             "전부 NO-GO 로 선언해 뒀다 — A3 를 공개 결론으로 올리면 그 계약과 충돌한다."})

    hi.append({
        "d": "2026-08-28", "t": "van Hove — **고원에서는 D 를 대체 못 한다**",
        "v": "600→800 K 에 **3 %**",
        "n": "MSD 기울기 하나로 *'확산 구간인가'* 를 가르던 것을 대신할 독립 관측으로 들였다. "
             "33궤적을 돌렸고, 온도 검증은 통과했다 — *'갇힘'* 으로 판정된 유일한 궤적이 "
             "**세트 최저온(lpsocl 500 K)** 이다.\n"
             "🔴 **그런데 지표가 포화한다.** modelc 600 K Δ=3.18 vs 800 K Δ=3.27 — **200 K 차이에 3 %**. "
             "lpsocl 은 600/700/900 이 3.13/3.44/3.16 으로 평평하다. 최종 봉우리가 전부 "
             "**3.6–4.4 Å(자리 간격)** 에 몰린다 — 50 ps 안에 홉이 한 번 수준이면 최빈값이 "
             "'한 번 홉' 자리에 앉고 안 움직인다.\n"
             "⇒ 체제가 셋이다: **갇힘 / 홉 고원 / 확산**. 그리고 **우리 생산 온도(600–800 K)가 "
             "대부분 고원 안**이다. 이 지표는 *'움직이나'* 를 답하지 *'얼마나 빠르나'* 를 답하지 않는다.\n"
             "🔑 교차리뷰 L 이 더 아픈 반례를 줬다 — 같은 modelc 600 K 세 시드에서 "
             "**mode 산포 2.5 % 인데 D 산포는 101 %** 다. 고원의 '3 %' 는 물리 산포가 작다는 뜻이 아니라 "
             "**mode 가 D 차이를 압축해 숨긴다**는 직접 증거다.\n"
             "⛔ **원고 사용 NO-GO** — 내부 진단으로만. 그리고 `G_s` 가 아니라 "
             "`P_s = 4πr²G_s`(radial density)라 표기도 고쳤다."})

    hi.append({
        "d": "2026-08-28", "t": "⛔ 내 van Hove 증거 **절반이 무효 데이터** 위에 있었다",
        "v": "b2o3 골격 β **0.5–1.15**",
        "n": "\"시드 산포 96 %\" 와 \"1200 K 독립 재현\" 을 오늘 새 발견으로 적었다. "
             "교차리뷰 L 이 **우리 장부를 가리켰다** — `md_run_ledger` 에 "
             "**사전 등록된**(2026-08-25, 결과 보기 전 확정) 골격 게이트 판정이 있다:\n"
             "| b2o3 골격 β | 시드별 |\n| 800 K | 0.51 / 0.79 / 0.54 |\n| 1000 K | 0.50 / 0.78 / 0.47 |\n"
             "| 1200 K | 0.88 – 1.15 |\n"
             "문턱 0.30 을 **3/3 전부** 넘는다. 장부 판정: *\"800·1000 모두 오염. 1200 만의 문제가 아니었다\"* — "
             "**UMA-MD 수송축 전체 인용 금지**.\n"
             "⇒ 골격이 움직이는 계에서 잰 Li 변위는 **고정 자리망 위의 홉이 아니다.** "
             "내 두 발견은 그 위에 서 있었다. **철회한다** — stress test 로만 남긴다.\n"
             "🔴 그리고 더 급한 것: **modelc 골격은 아직 안 쟀다.** 살아남은 발견(고원)도 "
             "**그 게이트를 통과해야 유효**하다. 궤적은 이미 있어서 재실행 없이 잴 수 있다 "
             "(`msd_diffusive_check.py --framework`)."})

    hi.append({
        "d": "2026-08-28", "t": "🔑 **절대 바닥 없는 백분율** — 하루에 세 번 밟았다",
        "v": "비율은 **크기를 버린다**",
        "n": "백분율은 `차이 ÷ 크기` 다. 분모가 작아지면 두 가지가 일어나는데, "
             "**방향이 반대**라 더 안 보인다.\n"
             "**① 없는 차이가 커 보인다** — 끝점 A 0.0641 Å vs B 0.0723 Å 은 "
             "**차이 0.008 Å 인데 12 %** 다. 0.008 Å 은 원자 반지름의 1/100 — 잡음이다. "
             "그런데 '12 % 어긋남' 이라고 쓰면 *대칭이 깨졌다* 로 읽힌다.\n"
             "**② 비율이 엉뚱한 이유로 1 에 붙는다** — 골격 MSD 0.4 Å² 에서 질량중심을 빼도 "
             "0.4 Å² 라 `kept = 1.00` 이다. 원래 논리는 *'COM 을 빼도 안 줄면 재배열'* 인데, "
             "**골격이 애초에 안 움직였으면 뺄 드리프트가 없어** 당연히 1.0 이다. "
             "`kept=1.0` 이 *재배열했다* 와 *안 움직였다* 두 뜻을 갖는다.\n"
             "⇒ **비율은 '얼마나 다른가' 를 말하지 '다르다고 할 만한가' 를 말하지 않는다.** "
             "후자는 절대 크기가 답한다. 그래서 판정마다 **이 질문이 성립하는 최소 크기**를 "
             "같이 걸어야 한다.\n"
             "| 판정 | 넣은 바닥 | 없을 때 |\n"
             "| 끝점 스칼라 일치도 | 0.02 Å | 잡음이 \"어긋남\" (실제로 그랬다) |\n"
             "| 골격 COM (흐름/재배열) | 2 Å² (RMS 1.4) | 진동이 \"재배열 — 구제 불가\" (8/9 오판) |\n"
             "| 모드 스캔 잡음문턱 | ~~10 meV 선언~~ → **재서 정한다** | 안 재고 선언하면 그것도 임의 |\n"
             "🔍 골격 건은 **두 검사가 정반대를 말해서** 잡혔다 — 골격 β 는 9/9 rigid 인데 "
             "COM 검사는 8/9 재배열이었다. 한 실행 안에서 두 지표가 반대를 가리키면 "
             "**데이터가 아니라 도구를 먼저 본다.**"})

    hi.append({
        "d": "2026-08-28", "t": "✅ modelc 골격 게이트 통과 — **9/9 rigid**",
        "v": "β **−0.05 ~ 0.27** (문턱 0.30)",
        "n": "b2o3 궤적이 골격 오염으로 무효 판정된 뒤, **modelc 는 한 번도 안 쟀다**는 것이 "
             "드러났다. 궤적이 이미 있어 재실행 없이 쟀다.\n"
             "| modelc | 600 K | 800 K | 1000 K |\n"
             "| worst β (s2/s3/s4) | −0.01 / 0.13 / −0.02 | 0.03 / −0.05 / −0.01 | 0.27 / 0.04 / 0.01 |\n"
             "**9/9 전부 `framework_rigid`** — 그 온도의 Li 변위는 **고정 자리망 위의 진짜 확산**이다.\n"
             "⇒ van Hove 에서 살아남은 발견(**자리 간격 고원**)은 유효한 궤적 위에 있다. "
             "b2o3 기반 발견 두 개는 철회한 채로 둔다.\n"
             "🔄 **b2o3 600 K 는 2/3 rigid** 다 (s2 만 P(8) β=0.55 인데 8원자 경계값이고 "
             "같은 런의 Cl(16)=−0.04 · S(41)=0.20 은 rigid). **800 K 이상만 확실히 무효** — "
             "어제 내가 쓴 것보다 좁다."})

    # ── 최신순 정렬 (1저자 요청 2026-08-20) ────────────────────────────────
    #   대시보드는 훑는 화면이라 **새로 안 것이 위**에 있어야 한다. 날짜가 없는 카드는
    #   맨 뒤로 보내되 서로의 상대 순서는 유지한다(안정 정렬) — 임의로 섞이면
    #   "왜 이 순서지" 를 매번 다시 물어야 한다.
    hi.sort(key=lambda c: c.get("d") or "", reverse=True)
    return hi

# ─────────────────────────────────────────────────────────────
# 개념 문서 첨부 (2026-08-05) — 그림·데이터를 웹에서 직접 열고 내려받기
# ─────────────────────────────────────────────────────────────
_ATT_EXT_RE = r"(?:png|jpg|jpeg|svg|csv|json|xyz|vasp|cif|pdf)"
_ATT_RE = re.compile(r"(?<![\w/.])((?:docs|db)/[\w./*-]+\." + _ATT_EXT_RE + r")")
# ⚠ 위 정규식은 **공백이 든 파일명**을 못 잡는다 (`pmf 관련 설명.pdf` → `docs/…/pmf` 에서 끊김).
#   이름 바꾸기로 한글·공백 이름이 생기면서 첨부가 통째로 사라졌다(2026-08-06 1저자 신고).
#   우리 문서 관례는 경로를 백틱으로 감싸는 것이므로, 백틱 안은 공백까지 통째로 받는다.
_ATT_TICK_RE = re.compile(r"`((?:docs|db)/[^`\n]+\." + _ATT_EXT_RE + r")`")
#   litdb/figures = 논문 PDF 에서 잘라낸 그림(tools/litdb/extract_figures.py). 서빙만 허용하고
#   갤러리(_GAL_DIRS)에는 안 넣는다 — 남의 논문 그림이 우리 산출물 목록을 덮으면 안 된다.
_ATT_ROOTS = ("docs", "db", "litdb/figures")
_IMG_EXT = (".png", ".jpg", ".jpeg", ".svg")


def _att_kind(rel: str) -> str:
    e = rel.lower()
    if e.endswith(_IMG_EXT):
        return "image"
    if e.endswith(".csv"):
        return "csv"
    if e.endswith(".pdf"):
        return "pdf"
    return "file"


#: 여백 메모(docnote.js)를 **달 수 있는** 문서. 읽는 문서에만 붙는다.
#: ⚠ safe_repo_path(파일 **서빙**용 화이트리스트)를 넓히지 않는다 — 그건
#:   /api/file 다운로드 경로라, 메모를 달려고 넓히면 배포판이 kb 전체를
#:   내려받을 수 있게 된다. 게이트를 나누는 게 맞다 (2026-08-17).
_NOTE_DOC_DIRS = ("litdb/papers/", "litdb/talks/", "kb/concepts/")


def safe_note_target(rel: str) -> Path | None:
    """메모를 달아도 되는 파일이면 실제 경로, 아니면 None.

    ① 기존 코멘트 대상(docs · db · litdb/figures) — safe_repo_path 그대로
    ② 우리가 화면에서 읽는 문서(_NOTE_DOC_DIRS 바로 밑의 .md) — 하위 폴더 불가

    이 함수가 못 하는 것: 파일 내용을 보지 않는다. 존재·위치만 본다.
    """
    rel = (rel or "").lstrip("/")
    p = safe_repo_path(rel)
    if p is not None:
        return p
    if not rel.endswith(".md"):
        return None
    for d in _NOTE_DOC_DIRS:
        if not rel.startswith(d):
            continue
        if "/" in rel[len(d):]:          # 하위 폴더는 허용 안 함 (`..` 우회 차단의 일부)
            return None
        q = (ROOT / rel).resolve()
        base = (ROOT / d).resolve()
        if q.is_relative_to(base) and q.is_file():
            return q
    return None


def safe_repo_path(rel: str) -> Path | None:
    """docs/ · db/ 안의 파일만 허용 (경로 탈출·심볼릭 탈출 차단)."""
    rel = (rel or "").lstrip("/")
    if not rel.startswith(_ATT_ROOTS):
        return None
    p = (ROOT / rel).resolve()
    for r in _ATT_ROOTS:
        base = (ROOT / r).resolve()
        if p.is_relative_to(base) and p.is_file():
            return p
    return None


# 파일명 → 개념 자동 연결 규칙 (2026-08-05)
#   본문에 경로를 적어야만 첨부되던 걸 보완한다 — 새 그림·CSV 를 만들면 문서를 안 고쳐도
#   해당 개념 페이지에 뜬다. 본문 언급분은 "cited", 규칙 매칭분은 "auto" 로 구분 표시.
#   ⚠ 과다 첨부를 막으려고 계열 접두사만 쓴다(와일드카드 남발 금지). 개념당 상한 24개.
_CONCEPT_FILE_RULES = {
    "bvse":   ("bv_path_", "bvse_", "bv_structure_", "bv_3d_", "bv_vs_pmf"),
    "md":     ("msd_", "pmf", "arrhenius", "hops_per_ion", "bv_vs_pmf", "li_density"),
    "beta-gate": ("msd_", "hops_per_ion", "diffusive"),
    "dft":    ("bv_path_annotated", "bv_path_segments", "bv_vs_pmf"),
    "cohp":   ("cohp", "icohp"),
    "bandgap": ("dos", "pdos", "gap", "bandstructure"),
    "elastic": ("elastic", "eos"),
    "neb":    ("neb",),
    "ordered_vs_disordered": ("disorder", "voronoi", "antisite"),
}
_AUTO_MAX = 24


def _auto_matched(cid: str) -> list[str]:
    pats = _CONCEPT_FILE_RULES.get(cid)
    if not pats:
        return []
    hits = []
    for d in ("docs/figures", "db/properties"):
        base = ROOT / d
        if not base.exists():
            continue
        for f in base.rglob("*"):
            if not f.is_file() or f.suffix.lower() not in _UP_EXT:
                continue
            n = f.name.lower()
            if any(p in n for p in pats):
                hits.append((f.stat().st_mtime, f.relative_to(ROOT).as_posix()))
    hits.sort(reverse=True)
    return [r for _m, r in hits[:_AUTO_MAX]]


def concept_attachments(cid: str) -> list[dict]:
    """개념 마크다운이 **본문에서 언급한** docs/·db/ 파일을 첨부로 모은다.

    왜 자동 수집인가 — 별도 목록을 두면 문서와 어긋난다. 우리 개념 문서는 관례상
    본문에 산출물 경로를 적어두므로(그림 `docs/figures/…png`, 데이터 `db/properties/…csv`)
    그걸 그대로 긁으면 **문서와 항상 동기**된다. 실존하는 파일만 남긴다.
    """
    md = read_concept(cid)
    if not md:
        return []
    seen, out = set(), []
    # 백틱 안(공백 허용)을 먼저, 그다음 백틱 없이 적힌 것 — 둘 다 seen 으로 중복 제거된다
    toks = [m.group(1) for m in _ATT_TICK_RE.finditer(md)]
    toks += [m.group(1) for m in _ATT_RE.finditer(md)]
    for tok in toks:
        # 문서가 `bv_path_annotated_*.png` 처럼 와일드카드로 적은 경우도 펼친다
        rels = ([q.relative_to(ROOT).as_posix() for q in sorted(ROOT.glob(tok))]
                if "*" in tok else [tok])
        for rel in rels:
            if rel in seen:
                continue
            seen.add(rel)
            p = safe_repo_path(rel)
            if not p:
                continue
            st = p.stat()
            # ⚠ 이 append 가 for 밖에 있었다 (2026-08-06 발견): 와일드카드가 N개로
            #   펼쳐져도 마지막 1개만 등록됐고, 마지막 것이 없는 파일이면 직전 것의
            #   크기·날짜를 달고 잘못 올라갔다.
            out.append({"rel": rel, "name": p.name, "kind": _att_kind(rel), "src": "cited",
                        "size_kb": round(st.st_size / 1024, 1), "mtime": int(st.st_mtime),
                        "day": _dt.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d")})
    for rel in _auto_matched(cid):                 # 규칙 자동 연결
        if rel in seen:
            continue
        p = safe_repo_path(rel)
        if not p:
            continue
        seen.add(rel)
        st = p.stat()
        out.append({"rel": rel, "name": p.name, "kind": _att_kind(rel), "src": "auto",
                    "size_kb": round(st.st_size / 1024, 1), "mtime": int(st.st_mtime),
                    "day": _dt.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d")})

    # 같은 이름 png ↔ csv 페어링 (하우스 관례: 그림과 Origin-ready CSV 가
    #   같은 stem — `_origin` 접미는 무시하고 비교). 페어된 CSV 는 이미지 카드에
    #   업혀 나가고 데이터 탭에서 빠진다.
    by_stem = {os.path.splitext(x["name"])[0]: x for x in out if x["kind"] == "image"}
    merged = []
    for x in out:
        if x["kind"] == "csv":
            stem = os.path.splitext(x["name"])[0]
            base = stem[:-7] if stem.endswith("_origin") else stem
            host = by_stem.get(base) or by_stem.get(stem)
            if host is not None and "pair" not in host:
                host["pair"] = x
                continue
        merged.append(x)
    merged.sort(key=lambda x: -x.get("mtime", 0))      # 최근순 (날짜 그룹용)
    return merged

_UP_EXT = {".png", ".jpg", ".jpeg", ".svg", ".csv", ".json", ".xyz", ".vasp", ".cif", ".pdf"}
_UP_MAX = 50 * 1024 * 1024        # 50 MB/파일


def _find_same_content(blob: bytes, name: str) -> str | None:
    """내용이 같은 파일이 이미 repo(docs/·db/)에 있으면 그 경로를 돌려준다.

    ⚠ 왜 필요한가 (2026-08-05 실측): 사용자가 webapp 에서 받은 그림을 다시 끌어올려
      **20개 전부 repo 원본의 복사본**이 됐다. 같은 파일이 두 경로에 살면 어느 게
      정본인지 흐려지고 용량도 두 배다. 같은 내용이면 **복사하지 않고 원본을 가리킨다**.
      1차로 파일명, 2차로 크기+md5 로 확인 (오탐 0).
    """
    import hashlib
    h = hashlib.md5(blob).hexdigest()
    n = len(blob)
    cands = list((ROOT / "docs").rglob(name)) + list((ROOT / "db").rglob(name))
    for q in cands:
        if "uploads" in q.parts or not q.is_file() or q.stat().st_size != n:
            continue
        if hashlib.md5(q.read_bytes()).hexdigest() == h:
            return q.relative_to(ROOT).as_posix()
    return None


# 파일명 정규화 — 예전엔 [A-Za-z0-9._-] 외를 전부 `_` 로 바꿔서 한글 이름이
#   `pmf______.pdf` 처럼 뭉개졌다(2026-08-06 1저자 지적). 경로를 깨뜨리는 글자만 막는다.
#   `#`·`%`·`&`·백틱도 막는다: 파일 이름으로는 되지만 URL(/api/file/…) 이 그 앞에서 잘리고,
#   백틱은 본문에 경로를 감싸 적는 우리 관례를 깨뜨린다.
_BAD_NAME = re.compile(r'[\x00-\x1f/\\:*?"<>|#%&`]')


def safe_filename(raw: str) -> str:
    """업로드/이름변경용 파일명 정규화. 한글·공백은 살리고 경로 문자만 막는다."""
    name = _BAD_NAME.sub("_", os.path.basename(raw or "")).strip()
    name = re.sub(r"\s+", " ", name).strip(". ")
    if name in ("", ".", ".."):
        return ""
    stem, ext = os.path.splitext(name)          # ⚠ 통째로 자르면 확장자가 날아간다
    return (stem[:120 - len(ext)] + ext) if len(name) > 120 else name


def rename_upload(rel: str, newname: str) -> dict:
    """`docs/uploads/**` 파일 이름 바꾸기 + 본문에 적힌 경로도 같이 고친다.

    ⚠ uploads 밖(docs/figures, db/properties …)은 **금지**한다: 그 경로들은 도구
      스크립트가 그 이름으로 다시 만들어 내므로, 바꿔봐야 다음 실행 때 원래 이름이
      또 생겨 두 벌이 된다. 표시 이름만 바꾸고 싶은 파일은 문서에서 캡션으로 쓴다.
    """
    if not str(rel).startswith("docs/uploads/"):
        return {"error": "업로드한 파일(docs/uploads/)만 이름을 바꿀 수 있어요 — "
                         "repo 산출물은 도구가 같은 이름으로 다시 만들어서 두 벌이 됩니다."}
    src = safe_repo_path(rel)
    if src is None:
        return {"error": "그 파일을 찾을 수 없어요"}
    # safe_filename 이 디렉터리 성분을 떼므로 "../../x" 는 폴더 밖으로 못 나간다(그냥 x 가 된다)
    name = safe_filename(newname)
    if not name:
        return {"error": "이름이 비어 있어요"}
    if os.path.splitext(name)[1].lower() != src.suffix.lower():
        name += src.suffix                      # 확장자를 지웠으면 되살린다
    if os.path.splitext(name)[1].lower() not in _UP_EXT:
        return {"error": f"허용 확장자가 아니에요: {os.path.splitext(name)[1]}"}
    dst = src.parent / name
    if dst == src:
        return {"ok": True, "rel": rel, "name": src.name, "unchanged": True}
    if dst.exists():
        return {"error": f"같은 이름이 이미 있어요: {name}"}
    old_rel = src.relative_to(ROOT).as_posix()
    new_rel = dst.relative_to(ROOT).as_posix()
    src.rename(dst)
    # 본문이 진실의 근원이므로 경로를 적어둔 문서도 같이 고친다
    touched = []
    for md in list(CONCEPTS.glob("*.md")) + list((ROOT / "kb").rglob("*.md")):
        try:
            t = md.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if old_rel in t:
            md.write_text(t.replace(old_rel, new_rel), encoding="utf-8")
            touched.append(md.relative_to(ROOT).as_posix())
    return {"ok": True, "rel": new_rel, "name": name, "docs": touched}


def save_concept_upload(cid: str, files) -> dict:
    """드래그 업로드 저장 — docs/uploads/<cid>/ 에 쓰고 **문서 끝에 경로를 append**.

    왜 문서에 쓰나: 첨부 목록은 본문에서 자동 수집되므로(불변식 "본문 = 진실의 근원"),
    파일만 두면 안 보인다. '## 첨부 (업로드)' 절을 만들어 경로를 한 줄씩 쌓는다.
    파일명은 [A-Za-z0-9._-] 로 정규화, 충돌 시 -2, -3 … 접미.
    """
    if read_concept(cid) is None:
        return {"error": "no such concept", "saved": [], "rejected": []}
    updir = ROOT / "docs" / "uploads" / cid
    saved, rejected, linked = [], [], []
    for f in files:
        name = safe_filename(f.filename or "")
        ext = os.path.splitext(name)[1].lower()
        if not name or ext not in _UP_EXT:
            rejected.append(f.filename or "(이름 없음)")
            continue
        blob = f.read()
        if not blob or len(blob) > _UP_MAX:
            rejected.append(f"{name} (빈 파일 또는 >50MB)")
            continue
        dup = _find_same_content(blob, name)
        if dup:                       # 이미 repo 에 같은 파일 → 복사 대신 그 경로 참조
            linked.append(dup)
            continue
        updir.mkdir(parents=True, exist_ok=True)
        stem, k = os.path.splitext(name)[0], 1
        q = updir / name
        while q.exists():
            k += 1
            q = updir / f"{stem}-{k}{ext}"
        q.write_bytes(blob)
        saved.append(q.relative_to(ROOT).as_posix())
    refs = saved + linked
    if refs:
        mdp = CONCEPTS / f"{cid}.md"
        txt = mdp.read_text(encoding="utf-8", errors="ignore")
        if "## 첨부 (업로드)" not in txt:
            txt = txt.rstrip() + "\n\n---\n## 첨부 (업로드)\n"
        have = set(re.findall(r"`((?:docs|db)/[^`]+)`", txt))
        new = [r for r in refs if r not in have]          # 같은 경로 재기록 방지
        if new:
            txt = txt.rstrip() + "\n" + "\n".join(f"- `{r}`" for r in new) + "\n"
            mdp.write_text(txt, encoding="utf-8")
    return {"saved": saved, "linked": linked, "rejected": rejected}

_GAL_DIRS = [("docs/figures", "그림"), ("db/properties", "데이터"),
             ("db/structures", "구조"), ("docs/uploads", "업로드")]


def gallery_files(q: str = "", kind: str = "", used: str = "",
                  folder: str = "", cmt: str = "") -> list[dict]:
    """repo 의 그림·데이터·구조 파일 전수 목록 (webapp 갤러리용).

    개념 문서 첨부는 '본문이 언급한 것'만 보여준다 — 그래서 나머지를 볼 길이 없어
    사용자가 받은 파일을 다시 끌어올리는 일이 생겼다(2026-08-05). 이 목록이 그 구멍을 메운다.
    """
    cidx = _file_concept_index()
    # 코멘트도 검색 대상 (1저자 요청 2026-08-06) — 파일명엔 없는 말로도 걸리게
    cmts, ccnt = comment_index(), comment_counts()
    ql = q.lower()
    out = []
    for rel_dir, group in _GAL_DIRS:
        base = ROOT / rel_dir
        if not base.exists():
            continue
        for f in base.rglob("*"):
            if not f.is_file() or f.name.startswith("."):
                continue
            if f.suffix.lower() not in _UP_EXT:
                continue
            k = _att_kind(str(f))
            rel = f.relative_to(ROOT).as_posix()
            cmt_hit = False
            if q:
                if ql not in rel.lower():
                    cmt_hit = ql in cmts.get(rel, "")
                    if not cmt_hit:
                        continue
            if kind and k != kind:
                continue
            if folder and not rel.startswith(folder):
                continue
            if cmt == "yes" and not ccnt.get(rel):
                continue
            st = f.stat()
            cons = cidx.get(rel, [])
            if used == "yes" and not cons:
                continue
            if used == "no" and cons:
                continue
            out.append({"rel": rel, "name": f.name, "kind": k, "group": group,
                        "dir": f.parent.relative_to(ROOT).as_posix(), "concepts": cons,
                        "comments": ccnt.get(rel, 0), "cmt_hit": cmt_hit,
                        "size_kb": round(st.st_size / 1024, 1), "mtime": int(st.st_mtime),
                        "day": _dt.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d")})
    out.sort(key=lambda x: -x["mtime"])          # 날짜 그룹 기본 = 최근순
    return out


def gallery_days(files: list[dict]) -> list[dict]:
    """날짜별 묶음 (최근 날짜부터). 템플릿에서 구분선 헤더로 쓴다."""
    days: dict[str, list[dict]] = {}
    for f in files:
        days.setdefault(f["day"], []).append(f)
    today = _dt.date.today()
    out = []
    for d in sorted(days, reverse=True):
        dd = _dt.date.fromisoformat(d)
        delta = (today - dd).days
        label = "오늘" if delta == 0 else ("어제" if delta == 1 else f"{delta}일 전")
        out.append({"day": d, "label": label, "files": days[d], "n": len(days[d])})
    return out


def gallery_folders() -> list[str]:
    return [d for d, _g in _GAL_DIRS if (ROOT / d).exists()]

def _file_concept_index() -> dict[str, list[dict]]:
    """파일 → 그 파일을 첨부로 가진 개념 문서들 (역인덱스).

    concept_attachments 를 전 개념에 돌려 뒤집는다. 페어(png↔csv)로 업힌 CSV 도
    같은 문서에 속하므로 함께 넣는다. 갤러리에서 '이 그림이 어느 개념 것인지'를
    보여주고 바로 그 페이지로 보내기 위한 것 (2026-08-05).
    """
    idx: dict[str, list[dict]] = {}
    for cid in sorted(concept_ids()):
        term = None
        try:
            import glossary as _G
            term = next((g["term"] for g in _G.GLOSSARY if g["id"] == cid), None)
        except Exception:
            pass
        for a in concept_attachments(cid):
            for rel in [a["rel"]] + ([a["pair"]["rel"]] if a.get("pair") else []):
                lst = idx.setdefault(rel, [])
                if not any(x["cid"] == cid for x in lst):
                    lst.append({"cid": cid, "term": term or cid})
    return idx


# ── 논문 그림 크로핑 (litdb/figures/<slug>/) ──────────────────────────────
#   tools/litdb/extract_figures.py 가 PDF 캡션을 앵커로 잘라 넣은 것.
#   digest 본문의 "Fig. 5e" 같은 언급 위에 마우스를 올리면 오른쪽 여백에 뜬다.

# digest 본문에서 그림별 주석 뽑기 — 그림을 눌렀을 때 "논문 캡션"과 함께
#   "우리 digest 가 뭐라 썼나"를 같이 보여준다 (2026-08-06 1저자 요청).
_FIGREF_RE = re.compile(
    r"\b(?:Fig(?:ures?|s)?\.?|FIGS?\.?|Tables?|Schemes?)\s*\.?\s*\(?(S?\d{1,3})\)?", re.I)
_FIGTBL_HEAD = re.compile(r"^\s*\|\s*\**\s*(fig|그림|figure)\b", re.I)


def _kind_of(word: str) -> str:
    w = word.lower()
    return "t" if w.startswith("tab") else ("s" if w.startswith("scheme") else "f")


def _keys_in(text: str, default_kind: str = "f", bare: bool = False) -> list[str]:
    """문장 안의 그림 참조 → ['f3','tS1'] (부분 패널 a/b 는 본 그림으로 합친다).

    ⚠ bare 는 **Figure set 표 첫 칸에만** 쓴다(`1a,b`·`S2` 처럼 Fig 없이 번호만 적는 칸).
      소제목에까지 켜면 `### 1. 한 줄 요약` 이 Fig 1 로 붙는다 (2026-08-06 실측).
    """
    out, pos = [], 0
    for m in _FIGREF_RE.finditer(text):
        out.append(_kind_of(m.group(0).strip()) + m.group(1).upper())
        pos = 1
    if not pos and bare:              # 'Fig' 없이 숫자만 적힌 표 첫칸 (예: `1a,b`, `S2`)
        out = [default_kind + n.upper() for n in re.findall(r"\bS?\d{1,3}", text)]
    seen, uniq = set(), []
    for k in out:
        if k not in seen:
            seen.add(k); uniq.append(k)
    return uniq


def _plain(md: str) -> str:
    """마크다운 장식을 벗겨 렌더된 본문과 대조 가능한 평문으로."""
    t = re.sub(r"[`*_~]+", "", md or "")
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)      # [글](링크) → 글
    return " ".join(t.split())


def paper_figure_notes(pid: str) -> dict:
    """slug → {figure key: [주석 문자열]}.

    두 갈래로 모은다:
      ① `## Figure set` 표 (`| Fig | 내용 | 우리 활용 |`) — 그림당 한 줄로 정리돼 있어 제일 정확
      ② 그 그림을 언급한 **소제목**(`### 5.3 … (Fig 6a) …`) — 어느 절에서 다루는지
    본문 문장까지 다 긁으면(zhou2026 은 한 그림에 16줄) 팝업이 넘치므로 3개까지만.
    """
    for sub in ("papers", "talks"):
        f = LITDB / sub / f"{pid}.md"
        if f.exists():
            break
    else:
        return {}
    try:
        md = f.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return {}
    notes: dict[str, list[str]] = {}

    def put(k, txt, src, find=""):
        """src: 'set' = Figure set 표 한 줄, 'sec' = 그 그림을 다루는 본문 절 제목.

        find = 렌더된 본문(HTML)에서 그 줄을 되찾을 **실마리 문자열**. 마크다운은 HTML 로
        바뀌면서 `**`·백틱이 사라지므로 그것들을 벗겨 평문으로 남긴다 — 클릭하면
        브라우저가 이걸로 해당 줄을 찾아 스크롤한다(옵시디언식 점프).
        ⚠ 표는 칸마다 <td> 로 쪼개지므로 실마리는 **한 칸 안에서만** 떼어야 한다.
        """
        txt = " ".join(txt.split())
        if not txt or len(txt) < 4:
            return
        lst = notes.setdefault(k, [])
        if len(lst) < 3 and not any(x["text"] == txt for x in lst):
            lst.append({"src": src, "text": txt[:400], "find": _plain(find or txt)[:70]})

    in_tbl = False
    for ln in md.splitlines():
        if ln.startswith("#"):                      # ② 소제목 (명시적 Fig 언급만)
            head_txt = ln.lstrip("# ").strip()
            for k in _keys_in(ln):
                put(k, head_txt, "sec", head_txt)
            in_tbl = False
            continue
        if _FIGTBL_HEAD.match(ln):                  # ① Figure set 표 시작
            in_tbl = True
            continue
        if in_tbl:
            if not ln.lstrip().startswith("|"):
                in_tbl = False
                continue
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) < 2 or set(cells[0]) <= set("-: "):
                continue                            # 구분선
            head = cells[0].replace("*", "")
            body = " · ".join(c.replace("*", "") for c in cells[1:] if c)
            kind = "t" if re.search(r"tab", head, re.I) else "f"
            for k in _keys_in(head, default_kind=kind, bare=True):
                put(k, body, "set", cells[1] if len(cells) > 1 else head)
    for lst in notes.values():                      # 표(정확) → 절 제목(맥락) 순
        lst.sort(key=lambda x: x["src"] != "set")
    return notes


def paper_figures(pid: str) -> list[dict]:
    """<pid> 논문의 크로핑된 그림 목록. 없으면 빈 리스트."""
    d = LITDB / "figures" / pid
    j = d / "figures.json"
    if not j.exists():
        return []
    try:
        meta = json.loads(j.read_text(encoding="utf-8"))
    except Exception:
        return []
    notes = paper_figure_notes(pid)
    cc = comment_counts()                  # 그림 카드에 💬N 을 바로 찍기 위해
    out = []
    for f in meta.get("figures", []):
        # file 이 **없을 수도, None 일 수도** 있다. None 은 중복 크롭을 지우면서
        # `dup_of` 표식만 남긴 항목이다 (extract_figures.py --dedupe, 2026-08-19).
        # `.get("file","")` 는 키가 있고 값이 None 이면 None 을 돌려줘 Path / None 으로 터졌다.
        fn = f.get("file") or ""
        if not fn:
            continue
        p = d / fn
        if not p.is_file():
            continue                       # json 만 남고 png 가 지워진 경우 방어
        rel = f"litdb/figures/{pid}/{fn}"
        out.append({
            "comments": cc.get(rel, 0),
            "key": f.get("key") or f"f{f.get('label','')}",
            "kind": f.get("kind", "figure"),
            "label": str(f.get("label", "")),
            "page": f.get("page"),
            "caption": f.get("caption", ""),
            "w": f.get("w"), "h": f.get("h"),
            "rel": rel,
            "size": p.stat().st_size,
            "notes": notes.get(f.get("key") or "", []),
        })
    return out


def paper_figure_search() -> dict[str, str]:
    """slug → 그 논문 그림·표 **캡션을 이어붙인 검색용 문자열** (소문자).

    1저자 요청(2026-08-06): "figure 사진에 있는 논문 캡션도 검색되나?"
    제목만으로는 "Nyquist 그림 있는 논문" 같은 걸 못 찾는다. 캡션 1,126장이 좋은 색인이다.
    ⚠ 목록 페이지 HTML 에 통째로 실리므로 **캡션당 앞 110자**만 (전체를 넣으면 300 KB+).
      figures.json 만 읽는다 — digest 는 안 읽는다(papers_with_figures 와 같은 이유).
    """
    base = LITDB / "figures"
    if not base.is_dir():
        return {}
    out = {}
    for j in base.glob("*/figures.json"):
        try:
            figs = json.loads(j.read_text(encoding="utf-8")).get("figures", [])
        except (OSError, ValueError):
            continue
        # 그림 단위로 셀 수 있게 "<key> <캡션>" 을 ¦ 로 이어 붙인다 — 검색 결과에
        # "몇 장에서 걸렸나 / 어느 그림인가" 를 표시하기 위해 (2026-08-06 1저자 요청).
        parts = []
        for f in figs:
            c = " ".join((f.get("caption") or "").split())[:110]
            if c:
                parts.append((f.get("key") or "") + " " + c)
        if parts:
            out[j.parent.name] = "\u00a6".join(parts).lower()[:9000]
    return out


def papers_with_figures() -> dict[str, int]:
    """slug → 그림 개수 (목록 화면 배지용).

    ⚠ paper_figures() 를 부르면 안 된다: 그건 digest 마크다운까지 읽어 주석을 뽑으므로
      논문이 늘면 /literature 한 번에 수십 MB 를 읽는다(53편 환산 ~124 ms → 아래로 ~5 ms).
      배지엔 개수만 필요하니 figures.json 만 훑는다.
    """
    base = LITDB / "figures"
    if not base.is_dir():
        return {}
    out = {}
    for j in base.glob("*/figures.json"):
        try:
            n = len(json.loads(j.read_text(encoding="utf-8")).get("figures", []))
        except (OSError, ValueError):
            continue
        if n:
            out[j.parent.name] = n
    return out


# ── 파일 코멘트 (Notion 식 💬) ─────────────────────────────────────────────
#   1저자 요청(2026-08-06): "files나 figure 사진 확대하면 comment 적어놓을 수 있게".
#   그림·CSV 를 보다가 든 판단("이건 아티팩트 의심", "이 축은 log")을 그 파일 옆에 붙여
#   둔다. repo 에 파일로 두므로 세션이 바뀌어도, 다른 머신에서도 그대로 보인다.
COMMENTS_PATH = DB / "file_comments.json"
HIGHLIGHTS_PATH = DB / "file_highlights.json"


def _clean_note_text(s: str) -> str:
    """메모 글 정리 — **줄바꿈은 살린다.**

    ⛔ 2026-08-27 정정 (1저자 신고: "shift enter 가 안 먹힌다")
      옛 판은 `" ".join(text.split("\\n"))` 으로 줄바꿈을 전부 공백으로 뭉갰다.
      저장이 JSON 이라 줄바꿈을 못 담을 이유가 없었는데도 그랬다. 게다가
      **화면과 입력창은 이미 줄을 그릴 준비가 돼 있었다** — `.dn-text` 는 `pre-wrap`
      이고 입력창은 `textarea` 라 Shift+Enter 가 네이티브로 먹는다. 서버만 몰랐고,
      그래서 세미나 메모가 전부 한 줄로 뭉쳐 나왔다. 증상은 입력에서 보이는데
      원인은 저장에 있던 경우다.

    지금 하는 것: CRLF 통일 · 줄 끝 공백 제거 · **빈 줄은 최대 하나**까지.
    안 하는 것: 줄 수 제한은 두지 않는다 (2000자 상한이 이미 있다).
    """
    s = (s or "").replace("\r\n", "\n").replace("\r", "\n")
    s = "\n".join(ln.rstrip() for ln in s.split("\n"))
    return re.sub(r"\n{3,}", "\n\n", s).strip()


def _load_comments(path=None) -> dict:
    p = path or COMMENTS_PATH
    if not p.exists():
        return {}
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def _save_comments(d: dict, path=None) -> None:
    """임시파일에 쓰고 os.replace 로 갈아끼운다 — 쓰는 도중 죽어도 반쪽 JSON 이 안 남는다.

    ⚠⚠ Windows 에서 `os.replace` 는 대상 파일을 **누가 잠깐 열고만 있어도**
      `PermissionError [WinError 5]` 를 낸다 (백신·인덱서·에디터). 우리 락은 별도
      `.lock` 파일에 걸리므로 그런 외부 handle 까지는 못 막는다.
      실측(2026-08-07 Codex 3라운드): 12프로세스 × 100건을 10회 돌려 6회 실패,
      합계 992/1000. 락은 멀쩡했고(임계구역 동시 진입 1) 실패는 전부 이 지점이었다.
      → 짧은 backoff 로 제한 재시도한다. POSIX 에서는 애초에 안 나는 경로다.
    """
    import time
    P = path or COMMENTS_PATH
    P.parent.mkdir(parents=True, exist_ok=True)
    tmp = P.with_suffix(P.suffix + f".tmp{os.getpid()}")
    tmp.write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True),
                   encoding="utf-8")
    delay, last = 0.005, None
    for _ in range(8):                       # 총 ~0.6 s. 그 이상 걸리면 진짜 문제다
        try:
            os.replace(tmp, P)
            return
        except PermissionError as ex:        # Windows 일시 점유
            last = ex
            time.sleep(delay)
            delay = min(delay * 2, 0.2)
        except OSError as ex:
            last = ex
            break
    try:
        tmp.unlink()                         # 실패했으면 임시파일을 남기지 않는다
    except OSError:
        pass
    raise last


# ─────────────────────────────────────────────────────────────
# 코멘트 쓰기 잠금 (2026-08-07, Codex 코드리뷰 P1)
#
# 저장이 read-modify-write 인데 잠금이 없었다. 배포는 gunicorn **worker 2개**라 동시에
# 달면 나중 저장이 앞선 저장을 통째로 덮는다. 리뷰의 실측: 40건 요청 → 2건만 남음.
#
# ⚠ 스레드 락으론 부족하다 — gunicorn 은 다중 **프로세스**다. 프로세스 간에도 걸리는
#   OS 파일 락(fcntl.flock)을 쓴다. 같은 호스트 안에서만 유효하다는 한계는 있지만
#   우리 배포 형태(단일 인스턴스 다중 worker)에는 그게 정확히 맞다.
#   여러 인스턴스로 늘릴 거면 그때는 SQLite WAL 이나 Postgres 로 가야 한다.
# ─────────────────────────────────────────────────────────────
import contextlib as _ctx

_CMT_LOCK = None


def process_alive(pid) -> bool:
    """PID 가 살아 있나. **판단 불가면 '살아 있다'** 로 본다(회수 안 함 = 안전한 쪽).

    ⚠⚠ POSIX 관례인 `os.kill(pid, 0)` 을 **Windows 에서 쓰면 안 된다** (2026-08-07
      Codex 4라운드). CPython 의 Windows 구현은 sig 가 CTRL_C_EVENT/CTRL_BREAK_EVENT 가
      아니면 `TerminateProcess(handle, sig)` 로 간다 — 즉 `os.kill(pid, 0)` 은
      **존재 확인이 아니라 종료 요청**이다. stale lock 을 검사하다 살아 있는 주인
      프로세스를 죽일 수 있었다. 실제 사고는 아직 없지만 설계상 가능했다.
      → Windows 는 OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION) +
        WaitForSingleObject(0) 로 **읽기만** 한다.
    """
    if os.name == "nt":
        # ⚠⚠ 2차 수정 (2026-08-07 Codex 5라운드 Windows 실기).
        #   1차는 PROCESS_QUERY_LIMITED_INFORMATION 만 열고 WaitForSingleObject 를
        #   불렀는데, **그 권한에는 SYNCHRONIZE 가 없어서** Wait 가
        #   WAIT_FAILED(0xFFFFFFFF, GetLastError=5) 를 돌려준다. 코드는
        #   "WAIT_TIMEOUT 아니면 죽음" 으로 봐서 **살아 있는 주인의 lock 을 뺏었다.**
        #   실기 확인:
        #     QUERY_LIMITED 만  → Wait = WAIT_FAILED, GetLastError 5
        #     GetExitCodeProcess → STILL_ACTIVE (0x103)   ← 이건 된다
        #     SYNCHRONIZE 포함  → Wait = WAIT_TIMEOUT      ← 이것도 된다
        #   → 둘 다 쓴다: SYNCHRONIZE 를 같이 요청하고, Wait 가 실패하면
        #     GetExitCodeProcess 로 떨어진다. **어느 단계든 판단 불가면 '살아 있다'.**
        try:
            import ctypes
            from ctypes import wintypes
            k32 = ctypes.WinDLL("kernel32", use_last_error=True)
            PROCESS_QUERY_LIMITED_INFORMATION, SYNCHRONIZE = 0x1000, 0x00100000
            ERROR_INVALID_PARAMETER = 87
            WAIT_TIMEOUT, WAIT_FAILED, STILL_ACTIVE = 0x102, 0xFFFFFFFF, 259
            k32.OpenProcess.restype = wintypes.HANDLE
            k32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
            h = k32.OpenProcess(
                PROCESS_QUERY_LIMITED_INFORMATION | SYNCHRONIZE, False, int(pid))
            if not h:                     # SYNCHRONIZE 가 거부되면 조회 권한만으로 재시도
                h = k32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid))
            if not h:
                # 그런 PID 가 아예 없을 때만 "죽었다". 나머지(권한 거부 등)는 살아 있다.
                return ctypes.get_last_error() != ERROR_INVALID_PARAMETER
            try:
                rc = k32.WaitForSingleObject(h, 0) & 0xFFFFFFFF
                if rc == WAIT_TIMEOUT:
                    return True           # 아직 안 끝났다
                if rc != WAIT_FAILED:
                    return False          # WAIT_OBJECT_0 = 끝났다
                # Wait 가 실패했다(권한 부족 등) — 종료코드로 다시 본다
                code = wintypes.DWORD()
                if k32.GetExitCodeProcess(h, ctypes.byref(code)):
                    return code.value == STILL_ACTIVE
                return True               # 그것도 안 되면 회수하지 않는다
            finally:
                k32.CloseHandle(h)
        except Exception:
            return True                   # ctypes 가 안 되면 회수하지 않는다
    try:
        os.kill(pid, 0)                  # POSIX 에서는 이게 존재 확인 관례가 맞다
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True                      # 남의 프로세스지만 살아 있다
    except OSError:
        return True                      # 판단 불가면 살아 있다고 본다(회수 안 함)


@_ctx.contextmanager
def _comments_locked(timeout=10.0, path=None):
    """읽기→수정→쓰기 전체를 한 임계구역으로 묶는다.

    ⚠ Windows 에는 fcntl 이 없다. 첫 판은 "없으면 그냥 진행" 이었는데, 그러면 Windows
      로컬에서 잠금이 **조용히 사라진다** — Codex 재검증에서 24 요청 중 16 저장으로 재현됐다.
      → msvcrt.locking 으로 대체한다. 그것도 없으면 **디렉터리 생성 락**으로 떨어진다
        (mkdir 은 POSIX·Windows 양쪽에서 원자적이라 최후 수단으로 쓸 만하다).
      어느 경우에도 "락 없이 진행" 은 하지 않는다.
    """
    import time
    lock_path = (path or COMMENTS_PATH).with_suffix((path or COMMENTS_PATH).suffix + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        import fcntl
    except ImportError:
        fcntl = None
    try:
        import msvcrt
    except ImportError:
        msvcrt = None

    if fcntl is not None:
        f = open(lock_path, "a+")
        try:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            yield
        finally:
            try:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            finally:
                f.close()
        return

    if msvcrt is not None:
        # msvcrt.locking 은 락이 잡혀 있으면 즉시 OSError 를 낸다 — 직접 재시도한다.
        f = open(lock_path, "a+b")
        f.seek(0)
        t0 = time.monotonic()
        while True:
            try:
                msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                break
            except OSError:
                if time.monotonic() - t0 > timeout:
                    f.close()
                    raise TimeoutError("코멘트 락을 못 잡았다 (Windows msvcrt)")
                time.sleep(0.01)
        try:
            yield
        finally:
            try:
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            finally:
                f.close()
        return

    # 최후 수단 — mkdir 은 원자적이다 (이미 있으면 FileExistsError)
    # ⚠ 첫 판은 stale lock 을 못 풀었다 (2026-08-07 Codex 3라운드): 프로세스가 hard kill
    #   되면 .lock.d 가 남고, 이후 모든 요청이 timeout 으로 죽는다. → owner 정보를 남기고,
    #   충분히 오래된 lock 은 **주인이 살아 있는지 확인한 뒤에만** 회수한다.
    d = lock_path.with_suffix(lock_path.suffix + ".d")
    own = d / "owner"
    STALE = max(timeout * 3, 30.0)

    t0 = time.monotonic()
    while True:
        try:
            d.mkdir()
            try:
                own.write_text(f"{os.getpid()} {time.time()}", encoding="utf-8")
            except OSError:
                pass
            break
        except FileExistsError:
            # 주인이 죽었고 충분히 오래됐으면 회수한다
            try:
                pid_s, ts_s = own.read_text(encoding="utf-8").split()
                if time.time() - float(ts_s) > STALE and not process_alive(int(pid_s)):
                    own.unlink(missing_ok=True)
                    d.rmdir()
                    continue
            except (OSError, ValueError):
                # owner 파일이 없다 = mkdir 직후 크래시. 나이를 디렉터리 mtime 으로 본다.
                try:
                    if time.time() - d.stat().st_mtime > STALE:
                        d.rmdir()
                        continue
                except OSError:
                    pass
            if time.monotonic() - t0 > timeout:
                raise TimeoutError(
                    f"코멘트 락을 못 잡았다 (mkdir 폴백). stale 이면 {STALE:.0f}s 뒤 자동 회수되고, "
                    f"급하면 {d} 를 지워라")
            time.sleep(0.01)
    try:
        yield
    finally:
        try:
            own.unlink(missing_ok=True)      # owner 를 먼저 지워야 rmdir 이 성공한다
            d.rmdir()
        except OSError:
            pass


#: 메모·코멘트에 붙이는 그림. 붙여넣기(Ctrl+V)한 캡처가 대부분이라 **png 가 기본**이다.
#: ⛔ svg 는 뺐다 — 첨부는 남이 만든 파일일 수 있고, svg 는 스크립트를 품는다.
NOTE_IMG_EXT = {"png": ".png", "jpeg": ".jpg", "jpg": ".jpg",
                "gif": ".gif", "webp": ".webp"}
NOTE_IMG_MAX = 8 * 1024 * 1024          # 8 MB/장 — 캡처 한 장이 이걸 넘을 일은 없다
NOTE_IMG_DIR = DB / "note_images"


def save_note_image(blob: bytes, kind: str) -> dict:
    """메모·코멘트에 붙일 그림 한 장을 저장 → {"url", "name", "bytes"} 또는 {"error"}.

    파일명이 **내용의 sha256** 이다. 같은 캡처를 여러 메모에 붙여도 한 벌만 남고,
    이름 충돌 처리가 필요 없다.

    ⛔ 못 하는 것
      · **참조 계수를 세지 않는다.** 메모에서 그림을 지워도 파일은 남는다
        (다른 메모가 같은 해시를 쓸 수 있어서 지우면 그쪽이 깨진다). 정리는 수동이다.
      · 확장자는 **선언(kind)이 아니라 매직바이트**로 정한다 — 클라이언트 말을 안 믿는다.
      · 크기를 줄이거나 다시 인코딩하지 않는다. 원본 그대로다.
    """
    if not blob:
        return {"error": "빈 파일"}
    if len(blob) > NOTE_IMG_MAX:
        return {"error": f"{len(blob)//1024//1024} MB — {NOTE_IMG_MAX//1024//1024} MB 를 넘는다"}
    sniff = _sniff_image(blob)
    if not sniff:
        return {"error": "그림 파일이 아니다 (png/jpeg/gif/webp 만)"}
    if kind and NOTE_IMG_EXT.get(str(kind).lower().split("/")[-1]) not in (None, sniff):
        # 선언과 실제가 다르면 **실제를 쓴다**. 다만 조용히 넘어가지는 않는다.
        pass
    import hashlib                      # 모듈 상단에 없다 — 기존 관례를 따른다
    h = hashlib.sha256(blob).hexdigest()[:32]
    NOTE_IMG_DIR.mkdir(parents=True, exist_ok=True)
    name = h + sniff
    q = NOTE_IMG_DIR / name
    if not q.exists():
        q.write_bytes(blob)
    return {"url": "/api/note-image/" + name, "name": name, "bytes": len(blob)}


def _sniff_image(b: bytes) -> str | None:
    """매직바이트로 확장자를 정한다 → ".png" 등. 모르면 None.

    클라이언트가 보낸 MIME 을 믿지 않는 이유: 첨부는 남이 만든 파일일 수 있다.
    """
    if b[:8] == b"\x89PNG\r\n\x1a\n":
        return ".png"
    if b[:3] == b"\xff\xd8\xff":
        return ".jpg"
    if b[:6] in (b"GIF87a", b"GIF89a"):
        return ".gif"
    if b[:4] == b"RIFF" and b[8:12] == b"WEBP":
        return ".webp"
    return None


def note_image_path(name: str):
    """저장된 그림의 실제 경로. 이름이 규격(해시+확장자)이 아니면 None — 경로 탈출 차단."""
    if not re.fullmatch(r"[0-9a-f]{32}\.(png|jpg|gif|webp)", name or ""):
        return None
    q = NOTE_IMG_DIR / name
    return q if q.is_file() else None


def file_comments(rel: str) -> list[dict]:
    """그 파일에 달린 코멘트 (오래된 순)."""
    return _load_comments().get((rel or "").lstrip("/"), [])


def add_file_comment(rel: str, text: str, who: str = "", anchor: str = "") -> dict:
    """코멘트 추가. ⚠ 실존하는 repo 파일에만 — 경로 탈출·유령 키를 막는다.

    anchor = **본문 여백 메모**(docnote.js)가 붙은 자리의 글 지문. 고른 글이 있으면
      그 글, 없으면 문단 앞머리다. 좌표가 아니라 글로 잡는 이유: digest 는 다시
      렌더될 때마다 DOM 이 새로 생기고 문단 번호도 편집으로 밀린다 — 글로 잡으면
      문단이 밀려도 따라간다. 그림 코멘트는 빈 값이라 예전 기록과 그대로 섞인다.
    """
    rel = (rel or "").lstrip("/")
    if safe_note_target(rel) is None:
        return {"error": "그 파일을 찾을 수 없어요"}
    text = _clean_note_text(text)          # ⛔ 줄바꿈을 **살린다** (_clean_note_text docstring)
    if not text:
        return {"error": "내용이 비어 있어요"}
    # ⚠ 읽기→수정→쓰기를 통째로 잠근다. 그리고 id 를 밀리초 타임스탬프로만 만들면
    #   동시 요청이 같은 밀리초에 걸려 **id 가 겹친다**(삭제가 엉뚱한 걸 지운다).
    #   락 안에서 기존 id 와 충돌하지 않을 때까지 뒤에 일련번호를 붙인다.
    with _comments_locked():
        d = _load_comments()
        lst = d.setdefault(rel, [])
        used = {c.get("id") for v in d.values() for c in v}
        base = f"c{int(_dt.datetime.now().timestamp() * 1000)}"
        cid, n = base, 0
        while cid in used:
            n += 1
            cid = f"{base}-{n}"
        item = {"id": cid,
                "text": text[:2000],
                "at": _dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "who": (who or "").strip()[:40]}
        anc = " ".join((anchor or "").split())[:160]
        if anc:
            item["anchor"] = anc      # ⚠ 없을 땐 키 자체를 안 넣는다 (옛 기록과 같은 모양)
        lst.append(item)
        _save_comments(d)
        return {"ok": True, "item": item, "n": len(lst)}


def edit_file_comment(rel: str, cid: str, text: str) -> dict:
    """메모·코멘트 글 고치기. **옛 글을 지우지 않고 history 에 쌓는다.**

    왜 이력을 남기나: 이 글들은 판단 기록이라, 나중에 "내가 그때 뭐라고 봤더라" 가
    질문이 된다. 덮어쓰면 그 답이 사라진다. 자리(anchor)·시각(at)·id 는 그대로 둔다
    — 그래야 딥링크와 검색 색인이 안 끊긴다.

    이 함수가 못 하는 것: anchor(붙인 자리)는 못 바꾼다. 자리를 옮기려면 지우고 다시 단다.
    """
    rel = (rel or "").lstrip("/")
    text = _clean_note_text(text)          # ⛔ 줄바꿈을 **살린다**
    if not text:
        return {"error": "내용이 비어 있어요"}
    with _comments_locked():
        d = _load_comments()
        lst = d.get(rel) or []
        for c in lst:
            if c.get("id") != cid:
                continue
            if c.get("text") == text:
                return {"ok": True, "item": c, "n": len(lst), "unchanged": True}
            c.setdefault("history", []).append(
                {"text": c.get("text", ""), "at": c.get("edited_at") or c.get("at", "")})
            c["text"] = text[:2000]
            c["edited_at"] = _dt.datetime.now().strftime("%Y-%m-%d %H:%M")
            _save_comments(d)
            return {"ok": True, "item": c, "n": len(lst)}
    return {"error": "그 메모를 못 찾았어요"}


# ── 형광펜 (2026-08-27, 논문세미나 준비) ──────────────────────────────────────
#   메모와 **다른 파일**에 담는다. 같은 파일에 섞으면 `file_comments()` 를 쓰는 곳
#   (검색 색인·📝 배지·paper 색인)이 전부 형광펜을 메모로 세게 된다 — 그 셋을 다
#   고치는 것보다 저장소를 가르는 게 싸고 되돌리기 쉽다.
#   대신 **락·원자쓰기는 메모 것을 그대로 재사용**한다(경로만 갈아끼운다).
#   자리 잡는 방식은 메모와 같다: 좌표가 아니라 **글 지문**. 문서가 다시 렌더돼도 따라간다.
HL_COLORS = ("yellow", "green", "pink", "blue")


def file_highlights(rel: str) -> list:
    return _load_comments(HIGHLIGHTS_PATH).get((rel or "").lstrip("/"), [])


def add_file_highlight(rel: str, text: str, color: str = "yellow") -> dict:
    """형광펜 한 줄. text = 칠한 글 그대로(자리를 다시 찾는 지문이자 내용).

    이 함수가 못 하는 것
      · 한 문단 안에 **같은 글이 여러 번** 나오면 첫 번째만 칠한다 (메모 anchor 와 같은 한계).
      · 문단을 가로지르는 선택은 저장은 되지만 다시 찾을 때 한 문단 안에서만 찾는다.
      · 색은 4종 고정. 임의 색을 받으면 CSS 클래스가 없어 조용히 안 칠해진다 — 그래서 막는다.
    """
    rel = (rel or "").lstrip("/")
    if safe_note_target(rel) is None:
        return {"error": "그 파일을 찾을 수 없어요"}
    t = " ".join((text or "").split())[:400]     # 형광펜은 한 줄짜리 지문이라 접는다
    if len(t) < 2:
        return {"error": "칠할 글이 너무 짧아요"}
    if color not in HL_COLORS:
        color = "yellow"
    with _comments_locked(path=HIGHLIGHTS_PATH):
        d = _load_comments(HIGHLIGHTS_PATH)
        lst = d.setdefault(rel, [])
        for c in lst:                            # 같은 글을 두 번 칠하면 색만 바꾼다
            if c.get("text") == t:
                c["color"] = color
                _save_comments(d, HIGHLIGHTS_PATH)
                return {"ok": True, "item": c, "n": len(lst), "recolored": True}
        used = {c.get("id") for v in d.values() for c in v}
        base = f"h{int(_dt.datetime.now().timestamp() * 1000)}"
        hid, n = base, 0
        while hid in used:
            n += 1
            hid = f"{base}-{n}"
        item = {"id": hid, "text": t, "color": color,
                "at": _dt.datetime.now().strftime("%Y-%m-%d %H:%M")}
        lst.append(item)
        _save_comments(d, HIGHLIGHTS_PATH)
        return {"ok": True, "item": item, "n": len(lst)}


def del_file_highlight(rel: str, hid: str) -> dict:
    rel = (rel or "").lstrip("/")
    with _comments_locked(path=HIGHLIGHTS_PATH):
        d = _load_comments(HIGHLIGHTS_PATH)
        lst = d.get(rel) or []
        keep = [c for c in lst if c.get("id") != hid]
        if len(keep) == len(lst):
            return {"error": "그 형광펜을 못 찾았어요"}
        if keep:
            d[rel] = keep
        else:
            d.pop(rel, None)
        _save_comments(d, HIGHLIGHTS_PATH)
        return {"ok": True, "n": len(keep)}


def del_file_comment(rel: str, cid: str) -> dict:
    rel = (rel or "").lstrip("/")
    with _comments_locked():
        d = _load_comments()
        lst = d.get(rel)
        if not lst:
            return {"error": "코멘트가 없어요"}
        keep = [c for c in lst if c.get("id") != cid]
        if len(keep) == len(lst):
            return {"error": "그 코멘트를 못 찾았어요"}
        if keep:
            d[rel] = keep
        else:
            d.pop(rel, None)                 # 빈 배열을 남기지 않는다
        _save_comments(d)
        return {"ok": True, "n": len(keep)}


def comment_counts() -> dict[str, int]:
    """rel → 코멘트 수 (배지용)."""
    return {k: len(v) for k, v in _load_comments().items() if v}


def comment_index() -> dict[str, str]:
    """rel → 그 파일 코멘트를 이어붙인 소문자 문자열 (검색용).

    1저자 요청(2026-08-06): "그 comment 도 검색에서 걸리게".
    적어 둔 판단("이 축은 log", "다른 조성 — 비교 인용 금지")은 파일명에 없는 말이라
    이름 검색으로는 절대 안 걸린다. 코멘트 자체가 색인이 된다.
    """
    return {rel: " ".join(c.get("text", "") for c in items).lower()
            for rel, items in _load_comments().items() if items}


def comment_all() -> list[dict]:
    """코멘트·메모 전체를 최근순으로 (⌘K 색인 · /notes 목록용).

    `anchor` 가 있으면 **본문 여백 메모**(docnote.js), 없으면 파일·그림 코멘트다.
    출처(kind·where·url)를 여기서 한 번만 정해 둔다 — 화면마다 rel 을 다시 파싱하면
    규칙이 갈라진다(⌘K 와 /notes 가 서로 다른 링크를 주는 식으로).
    """
    out = []
    for rel, items in _load_comments().items():
        meta = comment_origin(rel)
        for c in items:
            out.append({"rel": rel, "text": c.get("text", ""),
                        "at": c.get("at", ""), "id": c.get("id", ""),
                        "anchor": c.get("anchor", ""), **meta})
    out.sort(key=lambda x: x["at"], reverse=True)
    return out


def comment_origin(rel: str) -> dict:
    """rel → {kind, where, url}. 코멘트가 **어디에 달렸는지**의 단일 출처.

    kind: '논문' (digest 본문·그림) · '개념' (kb/concepts) · '파일' (그 밖)
    """
    seg = (rel or "").split("/")
    if rel.startswith("litdb/figures/") and len(seg) == 4:
        return {"kind": "논문", "where": seg[2], "url": f"/literature?open={seg[2]}"}
    if (len(seg) == 3 and seg[0] == "litdb"
            and seg[1] in ("papers", "talks") and seg[2].endswith(".md")):
        s = seg[2][:-3]
        return {"kind": "논문", "where": s, "url": f"/literature?open={s}"}
    if len(seg) == 3 and seg[0] == "kb" and seg[1] == "concepts" and seg[2].endswith(".md"):
        c = seg[2][:-3]
        return {"kind": "개념", "where": c, "url": f"/concept/{c}"}
    return {"kind": "파일", "where": seg[-1],
            "url": "/files?q=" + _urlquote(seg[-1])}


def note_url(c: dict) -> str:
    """메모 한 건의 **딥링크** — 그 문서를 열고 그 메모 자리까지 데려간다.

    여백 메모만 `?note=<id>` 를 붙인다(docnote.js 가 그걸 읽는다). 파일·그림
    코멘트는 붙일 자리가 없어 문서만 연다.
    """
    u = c.get("url") or "/"
    if not c.get("anchor"):
        return u
    return u + ("&" if "?" in u else "?") + "note=" + _urlquote(str(c.get("id", "")))


def notes_by_date() -> list[dict]:
    """메모·코멘트를 **날짜별로 묶어** 최신 날짜부터 (Notion 식 목록).

    ⚠ 같은 날 안에서는 시각 역순이다 — 하루 안에서도 나중에 쓴 게 위로 와야
      "방금 쓴 것" 을 찾는다.
    이 함수가 못 하는 것: 날짜가 없는 옛 기록은 '날짜 없음' 한 묶음으로 밀어 둔다.
    """
    groups: dict[str, list[dict]] = {}
    for c in comment_all():
        c["deep"] = note_url(c)
        day = (c.get("at") or "")[:10] or "날짜 없음"
        groups.setdefault(day, []).append(c)
    for v in groups.values():
        v.sort(key=lambda x: x.get("at", ""), reverse=True)
    return [{"date": d, "items": groups[d], "n": len(groups[d])}
            for d in sorted(groups, reverse=True)]


def _fig_keys(slug: str) -> dict[str, str]:
    """<slug> 의 파일이름 → 그림 키(f3 · t1 …). figures.json 한 번만 읽는다."""
    j = LITDB / "figures" / slug / "figures.json"
    try:
        figs = json.loads(j.read_text(encoding="utf-8")).get("figures", [])
    except (OSError, ValueError):
        return {}
    # file 이 None 인 항목(중복 크롭을 지우고 dup_of 만 남긴 것)은 파일이 없으니 뺀다
    return {f["file"]: (f.get("key") or "") for f in figs if f.get("file")}


def paper_comment_search() -> dict[str, str]:
    """slug → 그 논문에 달아 둔 **내 글**을 이어붙인 검색용 문자열.

    두 갈래를 한 색인에 담는다:
      · 그림 코멘트   `litdb/figures/<slug>/<file>` → 키 = 그림 키(f3 · t1 …)
      · 본문 여백 메모 `litdb/papers|talks/<slug>.md` → 키 = `@` (docnote.js)

    캡션 색인(paper_figure_search)과 같은 형식 "<key> <글>" ¦ 이어붙이기 —
    /literature 검색이 "몇 장에서, 어디서 걸렸나"를 그대로 표시할 수 있다.

    ⚠ 여백 메모는 **메모 글 + 붙인 자리(anchor)** 를 둘 다 넣는다. 형광펜 친 문장으로
      검색해도 걸려야 하기 때문 — 그게 Word 메모를 쓰는 실제 방식이다.
    ⚠ 메모 한 건씩 따로 넣는다(그림처럼 파일 단위로 뭉치지 않는다). 안 그러면
      검색 결과의 "메모 N건" 이 파일 수가 돼서 실제 건수와 어긋난다.
    """
    cm = _load_comments()
    if not cm:
        return {}
    parts: dict[str, list[str]] = {}
    keys: dict[str, dict[str, str]] = {}
    for rel, items in cm.items():
        if not items:
            continue
        seg = rel.split("/")
        if rel.startswith("litdb/figures/") and len(seg) == 4:
            slug, fname = seg[2], seg[3]
            if slug not in keys:
                keys[slug] = _fig_keys(slug)
            k = keys[slug].get(fname, "")
            txt = " ".join(" ".join((c.get("text") or "").split()) for c in items)[:300]
            if txt:
                parts.setdefault(slug, []).append(f"{k} {txt}")
        elif (len(seg) == 3 and seg[0] == "litdb"
              and seg[1] in ("papers", "talks") and seg[2].endswith(".md")):
            slug = seg[2][:-3]
            for c in items:
                txt = " ".join((c.get("text") or "").split())
                anc = " ".join((c.get("anchor") or "").split())
                if txt or anc:
                    parts.setdefault(slug, []).append(f"@ {txt} {anc}"[:400])
    return {s: "¦".join(v).lower()[:9000] for s, v in parts.items()}

def md_to_html(md: str) -> str:
    """세미나/용어 문서를 페이지에 그대로 싣기 위한 **최소** 마크다운 렌더러.

    ⚠ 범용 파서가 아니다 — 우리 kb 문서가 쓰는 문법(제목·표·불릿·인용·굵게·코드)만 처리한다.
      외부 입력이 아니라 **repo 안의 우리 문서**만 넣으므로 escape 후 화이트리스트로 되살린다.
    """
    import html as _h
    import re as _re
    out = []
    para, quote, li, code = [], [], [], []      # 여러 줄에 걸친 블록의 누적 버퍼
    in_tbl, lst, fence = False, None, None      # lst: None|'ul'|'ol' · fence: None|언어

    def inline(t):
        t = _h.escape(t)
        t = _re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
        t = _re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
        t = _re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", t)
        return t

    # ⚠ 문단은 **줄 단위가 아니라 블록 단위**로 합쳐서 inline 을 건다 (2026-08-06).
    #   줄마다 처리하면 `**굵게**` 가 줄바꿈을 넘는 순간 여는 별표를 못 닫아 원문에
    #   `**` 가 그대로 노출된다 — 우리 kb 문서는 문장 중간에서 줄을 접으므로 흔하다.
    #   합칠 때는 공백으로 잇는다(마크다운의 soft line break 관례. 우리 문서도 어절
    #   경계에서 접으므로 이게 맞다).
    def flush_para():
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>"); para.clear()

    def flush_quote():
        if quote:
            out.append("<blockquote>" + inline(" ".join(quote)) + "</blockquote>"); quote.clear()

    def flush_li():
        if li:
            out.append("<li>" + inline(" ".join(li)) + "</li>"); li.clear()

    def flush_list():
        nonlocal lst
        flush_li()
        if lst:
            out.append(f"</{lst}>"); lst = None

    def flush_tbl():
        nonlocal in_tbl
        if in_tbl:
            out.append("</tbody></table></div>"); in_tbl = False

    def close():
        flush_para(); flush_quote(); flush_list(); flush_tbl()

    for ln in md.splitlines():
        st = ln.rstrip()

        # ── 코드 펜스 — 안쪽은 아무것도 해석하지 않는다 (파이프라인 ASCII 그림용)
        m = _re.match(r"^\s*```\s*(\S*)\s*$", st)
        if m:
            if fence is None:
                close(); fence = m.group(1) or ""; code.clear()
            else:
                cls = f' class="lang-{_h.escape(fence)}"' if fence else ""
                out.append(f"<pre{cls}><code>" + _h.escape("\n".join(code)) + "</code></pre>")
                fence = None
            continue
        if fence is not None:
            code.append(ln.rstrip("\n")); continue

        # ── 표
        if _re.match(r"^\|.*\|$", st):
            cells = [c.strip() for c in st.strip("|").split("|")]
            if all(_re.fullmatch(r":?-{2,}:?", c) for c in cells):
                continue                                  # 구분행
            if not in_tbl:
                flush_para(); flush_quote(); flush_list()
                out.append('<div class="tbl-scroll"><table class="data-table"><tbody>')
                in_tbl = True
                out.append("<tr>" + "".join(f"<th>{inline(c)}</th>" for c in cells) + "</tr>")
            else:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>")
            continue
        flush_tbl()

        # ── 제목
        m = _re.match(r"^(#{1,4})\s+(.*)$", st)
        if m:
            close(); n = len(m.group(1))
            out.append(f"<h{min(n+1,5)}>{inline(m.group(2))}</h{min(n+1,5)}>"); continue

        # ── 인용 (연속 줄은 한 blockquote 로 합친다)
        if st.startswith(">"):
            flush_para(); flush_list()
            quote.append(st[1:].lstrip()); continue
        flush_quote()

        # ── 목록 — 불릿과 **번호 목록** 둘 다
        m = _re.match(r"^(\s*)([-*]|\d+[.)])\s+(.*)$", st)
        if m:
            kind = "ul" if m.group(2) in ("-", "*") else "ol"
            flush_para()
            if lst != kind:
                flush_list(); out.append(f"<{kind}>"); lst = kind
            else:
                flush_li()
            li.append(m.group(3)); continue

        # ── 목록 항목의 접힌 줄 (들여쓴 채 이어지는 본문)
        if lst and li and st.startswith((" ", "\t")) and st.strip():
            li.append(st.strip()); continue

        # ── 수평선 · 빈 줄
        if _re.fullmatch(r"-{3,}", st.strip()):
            close(); out.append("<hr>"); continue
        if not st.strip():
            close(); continue

        flush_list()
        para.append(st.strip())

    if fence is not None:                                  # 닫히지 않은 펜스도 살려서 낸다
        out.append("<pre><code>" + _h.escape("\n".join(code)) + "</code></pre>")
    close()
    return "\n".join(out)


# ── 세미나 진행표 ────────────────────────────────────────────────────────────────
SEMINAR_DECK = "Research_Seminar_2026_08_cascade_release.pptx"   # 정본 29장
SEMINAR_SCRIPT = "cascade_speaker_script_FINAL_ko.md"            # 29장 전수 대조본

#: 세미나 탭 — (키, 라벨, 경로, 한 줄 설명). 파일이 없으면 탭을 만들지 않는다.
SEMINAR_DOCS = [
    ("script", "🎙 발표 대본", KB / "seminars" / SEMINAR_SCRIPT,
     "29장 전수 대조 · 슬라이드별 초 배분 · 리허설 카드"),
    ("qa", "🛡 Defense Q&A", KB / "seminars" / "Research_Seminar_2026_08_cascade_final_defense_QA_ko.md",
     "예상 질문 24건과 방어 답변"),
    ("terms", "📖 용어 · 기호", KB / "seminars" / "Research_Seminar_2026_08_cascade_final_terminology_symbols.md",
     "기호 규약과 claim boundary"),
    ("ledger", "🧾 출처 원장", KB / "seminars" / "Research_Seminar_2026_08_cascade_final_source_ledger.md",
     "슬라이드별 정본 출처 — 숫자가 어디서 왔는지"),
    ("pipeline", "🧭 파이프라인", ROOT / "docs" / "cascade_pipeline_guide_codex_2026_08_11.md",
     "cascade 전체 절차"),
    ("ml", "🤖 ML 통합", ROOT / "docs" / "cascade_ml_integration_guide.md",
     "co-doping ML 과 acquisition"),
]

#: 2026-08-25 cascade 재랭킹이 이 덱에 걸리는가 — **감사 결과**.
#:   왜 화면에 박나: 재랭킹으로 캐스케이드 1등이 24 % 에서 바뀌었다. 덱을 다시 볼 때
#:   "그럼 내 발표 숫자도 바뀐 거 아닌가" 가 **반드시** 나온다. 그 답을 파일 어딘가가
#:   아니라 덱 화면 첫 자리에 둔다. 근거 없이 "안 바뀐다" 라고만 쓰면 그게 더 위험하다.
#:   ⛔ 이 상수가 못 하는 것: 자동 검사가 아니다. 덱이 새 CSV 를 읽도록 바뀌면
#:     이 문구는 조용히 거짓이 된다 — verified_by 의 경로가 바뀌었는지 사람이 본다.
SEMINAR_RERANK_AUDIT = {
    "date": "2026-08-25",
    "verdict": "unaffected",
    "headline": "이 덱은 2026-08-25 cascade 재랭킹의 영향을 받지 않는다.",
    "what_changed_elsewhere": [
        ("이동도 축", "0/3615 전원 상수 0.5 (기여 0) → 741행에 실제 기여"),
        ("캐스케이드 1등", "225개 중 **53개(24 %)** 에서 바뀜"),
        ("순위 갖는 행", "3,615 (미측정에 조작된 0.0 점) → 741 (측정된 것만)"),
        ("풀 정의", "47종 → 302 캐스케이드 · 4,125 구조"),
    ],
    "why_deck_is_safe": [
        ("덱은 결합점수를 안 쓴다",
         "발표의 funnel 은 가중합 score_combined 가 아니라 **post-hoc G1–G4 게이트**다 "
         "(47 → 25 → 11). 바뀐 것은 score_combined / rank_combined 쪽이다."),
        ("덱은 자기 CSV 를 읽는다",
         "plot_cascade_seminar_47.py 가 읽는 것은 cascade_seminar_*.csv (2026-06-25 "
         "frozen) 이고 cascade_v23_all.csv 가 아니다. 그림을 다시 그려도 같은 숫자다."),
        ("게이트 입력이 파생값이 아니다",
         "G4 의 transport_norm 은 **bvs_li_proxy_score**(BVSE 원출력)에서 나온다. "
         "깨져 있던 것은 li_mobility_score = 3×mvf + bvs 라는 **파생값**이다."),
        ("backfill 은 추가만 했다",
         "① 은 li_mobility_score 를 채웠을 뿐 bvs_li_proxy_score · "
         "migration_volume_fraction 을 건드리지 않았다 — 덱의 입력은 문자 그대로 그대로다."),
    ],
    "still_watch_out": "덱이 '3축 랭킹' 이라는 표현을 쓰면 그건 2026-08-25 이전엔 "
                       "사실이 아니었다 (실제로는 안정성+탄성 2축이었다). 현재 대본·Q&A 는 "
                       "그 표현을 쓰지 않는다 — 게이트 방식으로 간 것이 결과적으로 이 결함을 피했다.",
    "verified_by": [
        "tools/figures/plot_cascade_seminar_47.py (입력 CSV 경로 확인)",
        "db/properties/cascade_seminar_scorecard_47.csv (열 구성 확인)",
        "tools/doping/bvse_proxy.py::backfill_one (li_mobility_score 만 기록)",
    ],
    "card": "kb/methodology/cascade_rerank_runbook_2026_08_25.md",
    "decision": "db/governance/decisions.json → D-2026-08-25-missing-axis-is-unknown-not-worst",
}

#: 🎤 논문세미나 준비 — 심포지엄 세션 판독 (덱 + 구술 STT)
#
#  왜 여기 있나: 이 패널은 **우리 발표 준비**의 일부다. 남의 강의를 정리한 것이지만
#    쓰임새가 "우리가 어디에 서 있는지" 를 세미나에서 말하는 데 있다.
#  ⛔ 이 패널이 못 하는 것: 인용 허가를 주지 않는다. 아래 항목은 전부 citable=no 이고,
#    발표에서 **"저 교수님이 그랬다"** 를 논거로 쓰면 안 된다 (§12-1).
SEMINAR_TALK_PREP = {
    "date": "2026-08-26",
    "headline": "이상욱 교수님(성균관대 CMS Lab) 세션 — 덱 31장 + 구술 31:44 전수 판독",
    "slug": "lee2026_skku_mlip_materials_design",
    "citable": False,
    "why": "2026 전지기술 심포지엄 기술세션 3-3. **같은 물질(argyrodite)·같은 도구(MLIP)·다른 축** — "
           "정면 경쟁이자 우리 방법론의 벤치마크다. 구술에서 사용자가 직접 질문했고, "
           "그 답이 우리 b2o3 판정과 T1/T1b 에 바로 걸린다.",
    "takeaways": [
        ("★★★ MTP vs universal potential 분업",
         "이 랩은 **MTP = 동력학 / uMLIP(M3GNet·SevenNet·MACE) = static** 으로 용도를 나눈다 `[STT 26:50]`. "
         "덱 슬 8 이 배경을 인쇄해 놓았다 — `DFT PES ──softening──▶ uMLIP PES`. "
         "우리 b2o3 β≥0.60 @700 K 은 **uMLIP 으로 얻은 동역학 결과**다."),
        ("⛔ 그런데 우리 판정은 안 바뀐다",
         "A1 은 STT 전용(citable=no)이고, 이유가 **속도인지 PES 품질인지도 미확정**(Q-T2). "
         "근거는 여전히 우리 데이터 — modelc 12/12 rigid · lpsocl 12/12 rigid · b2o3 만 붕괴. "
         "**정황이 늘었을 뿐이므로 T1b(vdW DFT 대조)를 실제로 돌려야 한다.**"),
        ("★★ 멀티스케일은 '아직 요원하다'",
         "좌장 질문에 대한 답 `[STT 28:47]`: 10여 년째 꿈이고 AI 로도 곧 안 된다, "
         "적어도 **입계·입자까지 확장**하는 것도 큰 의미. → 우리 T8(P2D export)의 목표를 "
         "'셀까지'가 아니라 '한 칸 위까지'로 다시 쓴다."),
        ("★★ 지금 필요한 기초는 수학·코딩이 아니다",
         "`[STT 30:34]` 도메인 지식 + LLM 활용력, 그리고 **만들어준 코드를 이해하고 쓰는 것**. "
         "우리 repo 운영 방식(규율은 사람이 kb 에, 코드는 LLM 이, 검증은 --selftest)과 같은 모양."),
        ("🔑 계면 결정화의 기구 — 음이온이 먼저",
         "`[STT 18:09]` S 가 Li 보다 커서 **큰 음이온이 먼저 close-packing** → 핵생성 → "
         "격자간에 Li 진입 → Li₂S interphase. 덱 슬 18 은 시점만 보여주고 이유를 안 적었다. "
         "우리 **골격 β 게이트**가 이 순서의 정량판이다."),
        ("🔴 우리 기록 정정 1건",
         "계면 셀을 `3 nm × (10 nm 방향)` 으로 적어 왔는데 슬 18 을 **9× 확대**하니 "
         "**Li 6 nm + LPSCl 10 nm = 총 16 nm**. STT `6나노 16나노` 가 독립 확인. "
         "→ T3(Li|LPSCl 반응 MD)의 셀 규격 목표가 바뀐다."),
        ("🔧 AI×소재 3병목 ↔ 우리 정직성 장치",
         "`[STT 05:54]` ① DB 편재성·불일치 ② descriptor 문턱 ③ 자체생성 데이터 부족 — "
         "우리 쪽 대응물이 각각 ① MP/QE 혼용 금지 ② G5 컷 지배 경고 ③ 302 cascade + "
         "'결측은 최악이 아니다' 판정. **정직성 장치를 본론으로 낼 근거가 하나 늘었다.**"),
    ],
    "needed": [
        ("1", "Adv. Funct. Mater. (revision) — argyrodite 가수분해 SevenNet",
         "3부작 중 유일한 공백. Q4(H₂S 정량) + T2(ICOHP 기술자)가 한 번에 닫힌다"),
        ("2", "자료집 목차 페이지 (이상욱 섹션 앞뒤 1–2 pp)",
         "다음 발표자 이름 불일치(문장혁 vs STT `김장현`) 확인. 비용 0"),
        ("3", "Shapeev 2016 MTP + Novikov 2021 MLIP package",
         "γ(maxvol/D-optimality) 원정의 — 지금은 덱 숫자만 안다. T1 설계에 필요"),
        ("4", "Merchant 2023 GNoME (Nature 624, 80)", "강의 서사의 출발점인데 자체 digest 없음"),
        ("5", "Park 2024 SevenNet (JCTC 20, 4857)",
         "우리 UMA 와 같은 GNN 계열 → 'softening 이 GNN 공통인가'의 T1b 대조군"),
        ("6", "Luo 2022 ACS Energy Lett. 7, 3064", "슬 19 실험 앵커 ~12 nm = T3 대조군"),
    ],
    "blockers": "음성 미보유 · 권리 미상 · **Q&A 동의 미상** → 외부 사용·직접 인용 전면 금지",
    "card": "litdb/talks/lee2026_skku_mlip_materials_design.md §99",
    "analysis": "kb/projects/symposium_2026_competitive_analysis.md §8",
}

#: 다운로드 허용 덱 (경로 주입 차단 — 화이트리스트 밖은 404)
SEMINAR_DECKS = {
    "release": (SEMINAR_DECK, "정본 · 29장 (본문 21 + 부록 8)"),
    "codex28": ("Research_Seminar_2026_08_cascade_final.pptx", "Codex final · 28장 (레이더 없음)"),
}


def seminar_runsheet(md: str) -> list[dict]:
    """대본에서 Part/슬라이드 구조를 **파싱해서** 진행표를 만든다.

    하드코딩하지 않는 이유 — 대본을 고치면 화면이 따라와야 한다. 어긋나면 그게 바로
    "화면과 정본이 갈라진" 상태고, 우리가 제일 싫어하는 종류의 오류다.

    형식:  `# Part A. 제목 (P1–P4, ≈4분)`  ·  `## P1. 제목 ⏱40 ★`
    """
    import re
    parts: list[dict] = []
    cur: dict | None = None
    for line in md.splitlines():
        m = re.match(r"^#\s+(Part\s+([A-Z])\.\s*(.+?))\s*$", line)
        if m:
            title = m.group(3)
            rng = re.search(r"\(([^)]*)\)", title)          # 괄호가 끝이 아닐 수 있다
            clean = re.sub(r"\s*\([^)]*\)\s*", " ", title).strip(" —·-")
            cur = {"letter": m.group(2), "title": clean,
                   "meta": rng.group(1) if rng else "", "slides": []}
            parts.append(cur)
            continue
        if line.startswith("# ") and cur is not None:      # 부록·리허설 등 Part 밖 구획
            cur = None
            continue
        m = re.match(r"^##\s+(P(\d+))\.\s*(.+?)\s*$", line)
        if m and cur is not None:
            t = m.group(3)
            sec = re.search(r"⏱\s*(\d+)", t)
            cur["slides"].append({
                "id": m.group(1), "n": int(m.group(2)),
                "title": re.sub(r"\s*[⏱★].*$", "", t).strip(),
                "sec": int(sec.group(1)) if sec else None,
                "stars": t.count("★"),
            })
    for p in parts:
        tot = sum(s["sec"] or 0 for s in p["slides"])
        p["seconds"] = tot
        p["minutes"] = round(tot / 60.0, 1)
        p["span"] = (f"{p['slides'][0]['id']}–{p['slides'][-1]['id']}" if p["slides"] else "")
    return parts
