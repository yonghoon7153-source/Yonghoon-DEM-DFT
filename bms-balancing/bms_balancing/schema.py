"""산출물 스키마의 **한 정본** (Codex R9-03) — producer 가 쓰는 열/키와 checker·reader 가 요구하는 열/키는 여기서만 나온다.

전 판은 `check_u14.MATRIX_COLS` 가 producer 와 따로 살아서 (i) 과학 열(`LLI_pct`)이 사라져도 (ii) 출처 열 값이 비어도
(iii) 실행 조건이 바뀌어도 "전부 갖췄다 · 게시·서명만 바뀌었다" 였고, `ne_shape` 는 중복 key 의 첫 행을 과학 결과로 썼다
(R9-05). producer·checker·reader 가 같은 함수를 부른다.
"""
from __future__ import annotations
import hashlib, json, math, re

# ── 행/키 스키마 (producer 의 dict 키 순서 그대로) ─────────────────────────────────────────────
MATRIX_ROW = (
    "half_cell", "si", "w_dqdv", "run_id", "inputs_sha", "ref_inputs_sha", "consumed_inputs", "ref_consumed_inputs",
    "scale_seed", "n_scale_samples", "scale_pocv_target", "scale_dvdq_target", "scale_dqdv_target",
    "scale_pocv_ref", "scale_dvdq_ref", "scale_dqdv_ref", "scale_audit_target", "scale_audit_ref",
    "obj", "rmse_pocv", "a_PE", "b_PE", "a_NE", "b_NE", "gamma_Si", "c_cell", "bounds",
    "ref_a_PE", "ref_b_PE", "ref_a_NE", "ref_b_NE", "ref_gamma_Si", "ref_obj", "ref_rmse_pocv", "ref_c_cell", "ref_bounds",
    "LAM_PE_pct", "LAM_NE_pct", "LLI_pct",
    #: ⚠ 자체 리뷰 C05 (렌즈 2곳): 실패·부재 조합은 행에서 빠지므로 **행만 보면 모집단을 알 수 없다**.
    #:   profile 의 `gamma_roster` 와 같은 축인데 matrix 는 stdout `SUMMARY` 한 줄에만 있었다 (소비자 0) —
    #:   `out/matrix_300_0147.csv` 의 분모가 16 인 이유(`HALF_CELL_ABSENT`)가 산출물에 없었고, 2/32 행 묶음이
    #:   canonical 자리에서 "전부 갖췄다" 였다. 행마다 봉인한다.
    "combo_roster")
PROFILE_ROW = (
    "gamma_Si", "obj", "obj_ratio_to_best", "rmse_pocv", "a_PE", "b_PE", "a_NE", "b_NE", "bounds",
    "LAM_PE_pct", "LAM_NE_pct", "LLI_pct", "n_ok", "n_tried", "run_id", "profile_scale",
    "inputs_sha", "ref_inputs_sha", "consumed_inputs", "ref_consumed_inputs",
    #: ⚠ Codex R10 P1-3: 실패한 γ 는 행에서 빠지므로 **행만 보면 모집단을 알 수 없다**. 요청·성공·누락을 행마다
    #:   봉인한다 — 사라지는 stdout 요약이 아니라 검증되는 묶음이 스스로 말한다 (R8-04 와 같은 축).
    "gamma_roster")
DEGENERACY_KEYS = (
    "state", "si_source", "half_cell", "w_dqdv", "tol_percent_of_best", "n_starts", "seed", "n_grid", "n_samples",
    "run_id", "env", "consumed_inputs", "ref_consumed_inputs", "inputs_sha",
    "n_accepted", "best_obj", "best_p", "ref_p", "best_modes_percent",
    "LAM_PE_percent", "LAM_NE_percent", "LLI_percent")
#: 재실행이 "같은 실행" 이려면 같아야 하는 조건 (수치가 아니라 **조건** — 다르면 승격 대상이 아니다)
DEGENERACY_CONTROLS = ("state", "si_source", "half_cell", "w_dqdv", "tol_percent_of_best", "n_starts", "seed", "n_grid", "n_samples")
#: 값이 **비어 있으면 안 되는** 열 — 존재만으로는 provenance 가 아니다 (R9-03 B)
PROVENANCE_COLS = ("ref_inputs_sha", "consumed_inputs", "ref_consumed_inputs")
#: receipt 가 반드시 담아야 하는 **역할** — `build()` 가 소비하는 입력 전부 (Codex R10 P1-6). 역할이 빠지거나 모르는
#: 역할이 끼면 그것은 다른 계산이다; decoy 하나로 provenance 를 참칭할 수 없다.
REQUIRED_ROLES = ("full_cell", "half_cell", "literature.gr", "literature.si")
#: 승격 판정에서 **같아야 하는** 환경 축 (R6 내부 F3: scipy 1.11↔1.17 에서 최적점이 갈린다)
#: 비교하는 실행 환경 축 — `provenance.env_signature()` 가 **적는 것 전부**여야 한다.
#: ⚠ 자체 리뷰 C18: 전 판은 pandas 를 서명에는 적고 비교 축에서 뺐다. 과학 입력이 전부 `pd.read_excel` 로
#:   읽히므로 pandas 는 입력 파싱을 바꿀 수 있는 축이다 — 적고 안 대면 그 서명은 무엇을 고정하는지 말할 수 없다.
ENV_KEYS = ("python", "numpy", "scipy", "pandas", "platform")

#: ⚠ Codex R13 P2-1: 유한성 검사 **앞에** 타입·모양 계약이 없었다. `best_obj=true` 는 `float(True)==1.0`
#: 이라 정상 scalar 1.0 인 정본과 "같다" 로 읽혔고, `best_p=[]`·`LLI_percent={}` 도 문제 0 이었다.
#: 과학 값의 계약은 (a) 무엇인지 (b) 몇 개인지 (c) 유한한지 — 셋 다다.
DEGENERACY_NUMERIC = ("w_dqdv", "tol_percent_of_best", "n_starts", "seed", "n_grid",
                      "n_samples", "n_accepted", "best_obj")
DEGENERACY_VECTORS = {"best_p": 5, "ref_p": 5}          # 5-파라미터 모델 (model.LB5/UB5)
DEGENERACY_STATS = ("LAM_PE_percent", "LAM_NE_percent", "LLI_percent")
DEGENERACY_STAT_KEYS = ("min", "max")


def _is_num(x) -> bool:
    """bool 은 숫자가 아니다 (`isinstance(True, int)` 가 참이라 개수·값으로 새는 통로였다)."""
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def check_degeneracy_shape(j: dict) -> list:
    """degeneracy JSON 의 **타입·모양** 계약 (Codex R13 P2-1 · P2-4). 유한성보다 앞이다."""
    p = []
    for k in DEGENERACY_NUMERIC:
        if k in j and not _is_num(j[k]):
            p.append(f"{k} 가 유한 숫자가 아니다 ({j[k]!r}) — bool·문자열·비유한은 과학 값이 아니다")
    for k, n in DEGENERACY_VECTORS.items():
        if k not in j:
            continue
        v = j[k]
        if not isinstance(v, list) or len(v) != n or not all(_is_num(x) for x in v):
            p.append(f"{k} 가 유한 숫자 {n} 개의 목록이 아니다 ({v!r})")
    for k in DEGENERACY_STATS:
        if k not in j:
            continue
        v = j[k]
        if not isinstance(v, dict):
            p.append(f"{k} 가 객체가 아니다 ({v!r})"); continue
        miss = [q for q in DEGENERACY_STAT_KEYS if q not in v]
        if miss:
            p.append(f"{k} 에 필수 칸이 없다 ({miss}) — 빈 객체는 통계가 아니다")
        p += [f"{k}.{q} 가 유한 숫자가 아니다 ({v[q]!r})"
              for q in DEGENERACY_STAT_KEYS if q in v and not _is_num(v[q])]
    if "best_modes_percent" in j:
        v = j["best_modes_percent"]
        if not isinstance(v, dict) or not v or not all(_is_num(x) for x in v.values()):
            p.append(f"best_modes_percent 가 유한 숫자 객체가 아니다 ({v!r})")
    # ⚠ Codex R13 P2-4: 필수 env 축의 **존재**는 baseline 없이도 candidate 혼자 지켜야 하는 계약이다.
    #   전 판은 "비어 있지 않은 dict 인가" 만 보고 필수 key 는 비교 모드에서만 봤다.
    if "env" in j:
        e = j["env"]
        if not isinstance(e, dict):
            p.append(f"env 가 객체가 아니다 ({e!r})")
        else:
            miss = [k for k in ENV_KEYS if not str(e.get(k) or "").strip()]
            if miss:
                p.append(f"env 에 필수 축이 없다 ({miss}) — 요구: {' · '.join(ENV_KEYS)}")
    return p

#: sidecar 가 반드시 담아야 하는 실행 조건 — **양쪽에 있어야** 비교가 성립한다 (Codex R10 P1-7: 지우면 검사가 잠들었다)
META_CONTROLS = ("state", "half_cell_source", "si_source", "starts", "seed")
#: success 행에는 없어야 하는 열 — 있으면 그 행은 error 행이고 묶음은 승격 대상이 아니다 (Codex R10 P1-5)
ERROR_COL = "error"
#: 산출 version — digest 규칙이 바뀌면 올린다 (옛 digest 와 새 digest 가 섞여 보이지 않게)
RECEIPT_SCHEMA_VERSION = "r10.1"
#: 비어 있어도 되는 열 — producer 가 감사 dict 가 없으면 "" 를 쓴다 (`cmd_matrix` 의 scale_audit_*)
#: ⚠ 자체 리뷰 C33: `scale_audit_*` 는 `MAY_BE_EMPTY` 와 `ROW_SKIP` **양쪽**에 있었다 — 정본에는 R5-06 의 동치
#:   감사가 있고 재실행에는 빈 칸이어도 "전부 같다 · rc 0 · promotion true" 였다. 한쪽 carve-out 은 이유가 있어도
#:   둘 다면 그 열은 존재하지 않는 것과 같다. 빈 칸 허용을 뺀다 — producer 가 감사 없이 돌면 그것이 문제다.
MAY_BE_EMPTY: frozenset = frozenset()
#: 숫자가 **아닌** 열 (라벨·출처·감사 문자열). 나머지는 전부 유한한 숫자여야 한다 — 목록을 반대로 두면 새 숫자 열이
#: 생겼을 때 검사에서 조용히 빠진다 (Codex R11 P1-8: `a_NE="not-a-number"` 가 통과했다).
MATRIX_NON_NUMERIC = ("half_cell", "si", "run_id", "inputs_sha", "ref_inputs_sha", "consumed_inputs",
                      "ref_consumed_inputs", "scale_audit_target", "scale_audit_ref", "bounds", "ref_bounds",
                      "combo_roster")
PROFILE_NON_NUMERIC = ("bounds", "run_id", "profile_scale", "inputs_sha", "ref_inputs_sha",
                       "consumed_inputs", "ref_consumed_inputs", "gamma_roster")
MATRIX_NUMERIC = tuple(c for c in MATRIX_ROW if c not in MATRIX_NON_NUMERIC)
PROFILE_NUMERIC = tuple(c for c in PROFILE_ROW if c not in PROFILE_NON_NUMERIC)
#: 숫자 대조에서 뺄 열 (출처·감사 문자열 — 숫자가 아니다)
ROW_SKIP = frozenset({"run_id", "inputs_sha", "ref_inputs_sha", "consumed_inputs", "ref_consumed_inputs",
                      "scale_audit_target", "scale_audit_ref"})

#: profile 의 **정본 γ 격자** — 개수와 끝점이 계약이다 (Codex R11 P1-3: `--grid 1` 이 1 점짜리 산출을 complete 로
#: 게시했다; 모든 span 이 0 인 것은 당연하다). 다른 격자는 진단이고 canonical 이 아니다.
CANONICAL_GAMMA_GRID_N = 21

#: 정본 **자리** 규칙 위반(좁힌 실행이 canonical 이름에 앉음)은 산출 내용의 결함이 아니다.
#: reader 는 정직한 subset 을 소비할 수 있어야 하고, 승격 gate 만 이것을 막는다.
CANONICAL_SLOT_PREFIX = "canonical 자리: "

#: γ 격자·조합 모집단의 **정본은 여기 한 곳**이다 (Codex R13 P1-1).
#: 전 판은 `authority` 를 `CANONICAL_GAMMA_GRID_N` 과 **숫자끼리** 댔다 — 그래서 γ 21 개를 0~0.4 로
#: 잘못 깔아도, 32 조합 중 하나를 미등록 Si 로 바꿔도, 1 행이 "authority=1" 이라 스스로 적어도 전부
#: 통과했다 (모집단 주장이 산출 안에서만 닫혀 있었다). 이제 producer 와 checker 가 **같은 함수**로
#: 구성원 집합을 만들고, checker 는 본문의 key 집합을 그것과 **exact** 로 댄다.
#: (lazy import — `schema` 는 stdlib 만 top-level 로 쓴다. `data`·`model` 은 `schema` 를 import 하지
#:  않으므로 순환은 없다.)

def canonical_gamma_grid() -> list:
    """정본 γ 격자의 **값** (개수가 아니라). producer 의 `np.linspace(LB5[4], UB5[4], N)` 과 같은 식."""
    import numpy as _np

    from .model import LB5, UB5
    return [float(x) for x in _np.linspace(LB5[4], UB5[4], CANONICAL_GAMMA_GRID_N)]


def canonical_combo_keys(state: str) -> set:
    """그 상태의 정본 조합 집합 `{(half_cell, si, w_dqdv)}` — caller 옵션 밖이다 (Codex R11 P1-2 와 같은 축).

    알려진 부재(`HALF_CELL_ABSENT`)만 빠진다. 상태를 모르면 **빈 집합이 아니라 예외**다 —
    모집단을 말할 수 없으면 canonical 주장을 검증할 수 없고, 그때는 fail-closed 여야 한다.
    """
    from . import data as D
    if not state:
        raise ValueError("상태 없이 정본 조합 모집단을 말할 수 없다")
    out = set()
    for hc in D.HALF_FILE:
        if state not in D.HALF_FILE.get(hc, {}):
            continue
        if (hc, state) in D.HALF_CELL_ABSENT:
            continue
        out |= {(hc, si, float(w)) for si in D.SI_SOURCES for w in (0.0, 1.0)}
    return out


def state_of(name: str) -> str:
    """산출 파일 이름 → 상태. `matrix_<state>.csv` · `profile_gamma_<state>_<si>.csv`."""
    stem = (name or "").rsplit("/", 1)[-1]
    for pre in ("matrix_", "profile_gamma_", "degeneracy_"):
        if stem.startswith(pre):
            rest = stem[len(pre):].rsplit(".", 1)[0]
            if pre == "matrix_":
                return rest
            from . import data as D
            for st in sorted(D.STATES if hasattr(D, "STATES") else [], key=len, reverse=True):
                if rest == st or rest.startswith(st + "_"):
                    return st
            return rest.rsplit("_", 1)[0] if "_" in rest else rest
    return ""


def _gamma_set(rows: list) -> list:
    return [float(r["gamma_Si"]) for r in rows if r.get("gamma_Si") not in (None, "")]


def _same_grid(a: list, b: list, tol: float = 1e-9) -> bool:
    if len(a) != len(b):
        return False
    return all(abs(x - y) <= tol * max(1.0, abs(y)) for x, y in zip(sorted(a), sorted(b)))


_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_HEX12 = re.compile(r"^[0-9a-f]{12}$")


def receipt_leaves(consumed, problems: list | None = None) -> list:
    """receipt → `[(역할, leaf dict)]`. 중첩 한 단계까지 `literature.gr` 처럼 점으로 이어 붙인 **역할 이름**이 key 다.

    ⚠ Codex R11 P2-3: 전 판은 top-level 에 점이 든 key(`"literature.gr"`)를 그대로 역할로 삼아, 중첩된 진짜
      `literature.gr` 와 **같은 논리 역할이 둘** 인데도 집합 비교라 통과했다. top-level 에 점이 있으면 그것은 역할
      이름이 아니고, 같은 논리 역할이 두 번 나오면 그 receipt 는 모호하다 — 둘 다 문제로 센다.
    """
    out, seen = [], {}
    if not isinstance(consumed, dict):
        return out
    for role, v in consumed.items():
        role = str(role)
        if "." in role and problems is not None:
            problems.append(f"top-level 역할 이름에 점이 있다: {role!r} — 역할은 중첩으로 쓴다 (Codex R11 P2-3)")
        if isinstance(v, dict) and "sha256" in v:
            out.append((role, v))
        elif isinstance(v, dict):
            out += [(f"{role}.{k}", w) for k, w in v.items() if isinstance(w, dict)]
        else:
            out.append((role, v))
    for role, _ in out:
        seen[role] = seen.get(role, 0) + 1
    if problems is not None:
        for role, n in seen.items():
            if n > 1:
                problems.append(f"논리 역할 {role!r} 이 {n} 번 나온다 — 역할마다 정확히 하나여야 한다 (Codex R11 P2-3)")
    return out


def receipt_text(consumed):
    """receipt 를 **한 모양으로** 정규화한다 — `validate_receipt` 와 같은 규칙 (JSON 문자열이면 한 겹 decode).

    ⚠ 자체 리뷰 C13: `validate_receipt` 는 str 을 `json.loads` 하는데 `receipt_map` 은 안 했다. degeneracy JSON 의
      `consumed_inputs` 가 문자열로 들어오면 `receipt_map` 이 `{}` 를 내고, 양쪽 다 `{}` 라 입력 비교가 "둘 다
      receipt 가 없다" 로 **조용히 잠들었다** — `inputs_uncomparable` 조차 안 찍혔고 `check_degeneracy` 도 `[]`
      였다. 서로 다른 반쪽전지를 먹은 두 실행이 승격 가능이었다. 정규화를 한 자리에 둔다.
    """
    if isinstance(consumed, str):
        try:
            return json.loads(consumed)
        except json.JSONDecodeError:
            return None
    return consumed


def receipt_map(consumed) -> dict:
    """`{역할: sha256}` — 두 실행의 **입력 identity** 를 이것으로 댄다 (Codex R11 P1-1)."""
    return {role: (str(leaf.get("sha256", "")) if isinstance(leaf, dict) else "")
            for role, leaf in receipt_leaves(receipt_text(consumed))}


def receipt_paths(consumed) -> dict:
    """`{역할: path}` — digest 에는 안 들어가지만 역할별 locator 가 바뀌면 그것도 말한다 (Codex R11 Q1)."""
    return {role: (str(leaf.get("path", "")) if isinstance(leaf, dict) else "")
            for role, leaf in receipt_leaves(receipt_text(consumed))}


def inputs_digest(consumed: dict) -> str:
    """소비한 입력의 **역할별** identity 를 묶은 digest 앞 12 자리.

    ⚠ Codex R10 P1-6: 전 판은 sha256 **값만** 정렬해 이어 붙였다 — half_cell 과 full_cell 을 바꿔치기해도 같은 값
      (`76be1dcab00e`) 이었고, 어떤 역할이 있어야 하는지도 묶이지 않아 `{"decoy": …}` 하나가 provenance 로 통과했다.
      이제 `(역할, sha256)` 쌍을 역할 이름으로 정렬해 버전 태그와 함께 해시한다.
    ⚠ **경로는 일부러 digest 에 넣지 않는다.** R6 내부 F4 는 "같은 bytes 면 같은 실행" 을 고정했고
      (`test_i6p_04`: 이름만 다른 사본은 같은 digest), 경로를 넣으면 byte 가 같은 재-export 가 다른 실행으로 읽힌다.
      경로는 receipt 안에 그대로 남고 `validate_receipt` 가 비어 있지 않은지 본다 — identity 는 bytes 다 (R6 내부 F1).
    """
    items = sorted((role, str(leaf.get("sha256", "")) if isinstance(leaf, dict) else "")
                   for role, leaf in receipt_leaves(consumed))
    payload = RECEIPT_SCHEMA_VERSION + "\n" + "\n".join(f"{role}={sha}" for role, sha in items)
    return hashlib.sha256(payload.encode()).hexdigest()[:12]


def env_problems(old: dict | None, new: dict | None, where: str = "env") -> list:
    """두 실행의 환경이 **같은가** (Codex R10 P1-7: 전 판은 존재만 봤다). 축마다 값을 대 본다."""
    p = []
    if not isinstance(old, dict) or not isinstance(new, dict):
        return [f"{where}: 환경 서명이 없다 (정본 {type(old).__name__} · 새 산출 {type(new).__name__})"]
    for k in ENV_KEYS:
        a, b = old.get(k), new.get(k)
        if a in (None, "") or b in (None, ""):
            p.append(f"{where}.{k}: 환경 축이 비어 있다 (정본 {a!r} · 새 산출 {b!r})")
        elif a != b:
            p.append(f"{where}.{k}: 환경이 다르다 — 정본 {a!r} → 새 {b!r}")
    return p


def required_columns(kind: str) -> tuple:
    return {"matrix": MATRIX_ROW, "profile": PROFILE_ROW}[kind]


def matrix_key(row: dict) -> tuple:
    """정규화한 identity — `w_dqdv` 는 숫자다 ("0" 과 "0.0" 은 같은 행이다, R9-05)."""
    return (row.get("half_cell"), row.get("si"), float(row.get("w_dqdv") if row.get("w_dqdv") not in (None, "") else "nan"))


def profile_key(row: dict) -> float:
    return float(row.get("gamma_Si") if row.get("gamma_Si") not in (None, "") else "nan")


def unique_rows(rows, key):
    """(key → 행, 중복 key 목록, 행 수). 중복은 **조용히 합치지 않는다** — checker(R8-05)·reader(R9-05)가 같은 함수를 쓴다."""
    seen, dup, out = {}, [], {}
    for r in rows:
        k = key(r)
        seen[k] = seen.get(k, 0) + 1
        if seen[k] > 1 and k not in dup:
            dup.append(k)
        out.setdefault(k, r)
    return out, dup, len(rows)


def validate_receipt(text, digest, where="", roles=REQUIRED_ROLES) -> list:
    """`consumed_inputs` (JSON 문자열 또는 dict) + 그 digest → 문제 목록.

    비어 있으면 안 되고, **역할 집합이 정확히** `roles` 와 같아야 하며 (빠진 역할·모르는 역할 둘 다 문제),
    역할마다 path 와 64-hex sha256 이 있어야 하고, digest 는 그 (역할, sha256) 에서 **다시 계산한 값**과 같아야 한다
    (R9-03 B · Codex R10 P1-6).
    """
    p = []
    if text in (None, ""):
        return [f"{where}: 출처(receipt)가 비어 있다"]
    try:
        d = json.loads(text) if isinstance(text, str) else text
    except (TypeError, ValueError) as e:
        return [f"{where}: receipt 가 JSON 이 아니다 ({e})"]
    if not isinstance(d, dict) or not d:
        return [f"{where}: receipt 가 빈 dict 이거나 dict 가 아니다"]
    leaves = receipt_leaves(d, p)                                          # 점 key·중복 역할을 여기서 센다 (R11 P2-3)
    got = {role for role, _ in leaves}
    if roles:
        missing = [r for r in roles if r not in got]
        unknown = sorted(got - set(roles))
        if missing:
            p.append(f"{where}: 필수 입력 역할이 없다 — {missing} (있는 역할: {sorted(got)})")
        if unknown:
            p.append(f"{where}: 모르는 역할이 끼어 있다 — {unknown} (요구 역할: {list(roles)})")
    for role, leaf in leaves:
        if not isinstance(leaf, dict):
            p.append(f"{where}: 역할 {role!r} 이 dict 가 아니다"); continue
        if not str(leaf.get("path") or "").strip():
            p.append(f"{where}: {role} 의 path 가 비어 있다")
        if not _HEX64.match(str(leaf.get("sha256") or "")):
            p.append(f"{where}: {role} 의 sha256 이 64-hex 가 아니다")
    if digest in (None, "") or not _HEX12.match(str(digest)):
        p.append(f"{where}: aggregate digest 가 12-hex 가 아니다 ({digest!r})")
    elif not p and inputs_digest(d) != digest:
        p.append(f"{where}: aggregate digest 불일치 — 재계산 {inputs_digest(d)} ≠ 기록 {digest}")
    return p


def check_rows(kind: str, rows: list, header: list, name: str = "") -> list:
    """CSV 산출 한 파일의 exact schema 검사 → 문제 목록.

    **success / error 는 exact tagged union 이다** (Codex R10 P1-5). 전 판은 truthy `error` 한 칸이 그 행의 필수 셀·
    숫자·receipt 검사를 전부 `continue` 로 건너뛰게 했고, 열이 하나 늘어난 것은 "정보성" 으로 셌다 — 정상 수치 행에
    `error=skip` 을 붙이고 receipt 네 칸을 비우면 U18 gate 가 "전부 갖췄다 · 전부 같다 · rc 0" 이었다. 이제:

    - success 행에는 `error` 가 **없어야** 한다. 있으면 그 행은 error 행이고,
    - error 행이 하나라도 있으면 그 묶음은 success 가 아니다 → 승격 대상이 아니라고 **말한다** (문제로 센다),
    - 요구 열도 모르는 열도 아닌 것은 없어야 한다 (열이 조용히 늘면 그것이 다음 우회로다).
    """
    need = required_columns(kind)
    p = [f"열 없음: {c}" for c in need if c not in header]
    unknown = [c for c in header if c not in need and c != ERROR_COL]
    if unknown:
        p.append(f"모르는 열 {unknown} — producer 스키마에 없는 열이다 (`bms_balancing/schema.py` 가 정본)")
    numeric = MATRIX_NUMERIC if kind == "matrix" else PROFILE_NUMERIC
    n_error = 0
    for i, r in enumerate(rows):
        if str(r.get(ERROR_COL) or "").strip():
            n_error += 1
            continue                                                       # 실패한 조합의 행 — 아래 union 규칙이 센다
        for c in need:
            if c in header and c not in MAY_BE_EMPTY and (r.get(c) is None or str(r.get(c)) == ""):
                p.append(f"행 {i}: 필수 셀 {c} 이 비어 있다")
        for c in numeric:
            if c in header and str(r.get(c) or "") != "":
                # ⚠ Codex R11 P1-8: `float()` 은 inf·nan 을 받고 비교기는 `inf == inf` 라 그대로 승격됐다.
                #   과학 값은 **유한**해야 한다 — producer 와 consumer 가 같은 검사를 쓴다.
                try:
                    x = float(r[c])
                except ValueError:
                    p.append(f"행 {i}: {c} 가 숫자가 아니다 ({r[c]!r})"); continue
                if not math.isfinite(x):
                    p.append(f"행 {i}: {c} 가 유한한 값이 아니다 ({r[c]!r}) — 과학 값이 아니다")
        if all(c in header for c in ("consumed_inputs", "inputs_sha")):
            p += validate_receipt(r.get("consumed_inputs"), r.get("inputs_sha"), f"행 {i} consumed_inputs")
        if all(c in header for c in ("ref_consumed_inputs", "ref_inputs_sha")):
            p += validate_receipt(r.get("ref_consumed_inputs"), r.get("ref_inputs_sha"), f"행 {i} ref_consumed_inputs")
    if n_error:
        p.append(f"`{ERROR_COL}` 행 {n_error}/{len(rows)} — 이 묶음은 success 가 아니다 (부분/실패이고 승격 대상이 "
                 f"아니다; success 행에 `{ERROR_COL}` 칸이 있으면 그것도 error 행이다, Codex R10 P1-5)")
    if kind == "profile" and "gamma_roster" in header:
        p += check_gamma_roster([r for r in rows if not str(r.get(ERROR_COL) or "").strip()])
    if kind == "matrix" and "combo_roster" in header:            # 자체 리뷰 C05 — profile 과 같은 축
        p += check_combo_roster([r for r in rows if not str(r.get(ERROR_COL) or "").strip()],
                                state=state_of(name))
    _, dup, _ = unique_rows([r for r in rows if not str(r.get(ERROR_COL) or "").strip()],
                            matrix_key if kind == "matrix" else profile_key)
    p += [f"중복 key {k}" for k in dup]
    return p


def body_roster(name: str, data: bytes) -> dict:
    """산출 **본문**에서 유도한 exact 명부 (Codex R9 P2-4). sidecar 의 singular 필드는 wrapper 의 환경값이지 본문의
    명부가 아니다. `run_states.sh` 의 `write_meta` 와 `check_u14` 가 **같은 함수**를 쓴다 — 두 벌로 두면 갈린다."""
    if name.endswith(".json"):
        j = json.loads(data.decode("utf-8"))
        return {"kind": "degeneracy", "state": j.get("state"),
                "half_cell": [j["half_cell"]] if j.get("half_cell") else [],
                "si": [j["si_source"]] if j.get("si_source") else [],
                "w_dqdv": [j["w_dqdv"]] if j.get("w_dqdv") is not None else []}
    import csv as _csv, io as _io
    rows = list(_csv.DictReader(_io.StringIO(data.decode("utf-8-sig"))))
    r = {"kind": "matrix" if name.startswith("matrix_") else "profile", "rows": len(rows)}
    for c in ("half_cell", "si", "w_dqdv", "profile_scale", "state"):
        if rows and c in rows[0]:
            r[c] = sorted({row.get(c) or "" for row in rows})
    if rows and "gamma_Si" in rows[0]:
        g = [float(row["gamma_Si"]) for row in rows if row.get("gamma_Si") not in (None, "")]
        r["gamma_Si"] = [min(g), max(g), len(g)] if g else []
    return r


def check_combo_roster(rows: list, state: str = "") -> list:
    """matrix 의 `combo_roster` — `gamma_roster` 와 같은 계약 (자체 리뷰 C05).

    exact key · 개수는 정수(bool 아님) · 산술(`succeeded + |missing_input| + |failed| == requested`) ·
    행마다 같은 roster · **본문과의 결속**(성공 수 = 행 수, canonical 주장이면 requested == authority).
    """
    p, seen = [], set()
    keys = {"authority", "requested", "succeeded", "missing_input", "failed", "absent"}
    for i, r in enumerate(rows):
        raw = r.get("combo_roster")
        try:
            d = json.loads(raw) if isinstance(raw, str) else raw
        except (TypeError, ValueError) as e:
            p.append(f"행 {i}: combo_roster 가 JSON 이 아니다 ({e})"); continue
        if not isinstance(d, dict) or set(d) != keys:
            p.append(f"행 {i}: combo_roster 의 key 가 계약과 다르다 — "
                     f"{sorted(d) if isinstance(d, dict) else type(d).__name__} (요구: {' · '.join(sorted(keys))})")
            continue
        if not all(isinstance(d[k], list) and all(isinstance(x, str) for x in d[k])
                   for k in ("missing_input", "failed", "absent")):
            p.append(f"행 {i}: combo_roster 의 목록이 문자열 목록이 아니다 ({d!r})"); continue
        if not all(isinstance(d[k], int) and not isinstance(d[k], bool) for k in ("authority", "requested", "succeeded")):
            p.append(f"행 {i}: combo_roster 의 개수가 정수가 아니다 ({d!r})"); continue
        if d["succeeded"] + len(d["missing_input"]) + len(d["failed"]) != d["requested"]:
            p.append(f"행 {i}: combo_roster 산술이 안 맞는다 — 성공 {d['succeeded']} + 입력 없음 "
                     f"{len(d['missing_input'])} + 실패 {len(d['failed'])} ≠ 요청 {d['requested']}")
        seen.add(json.dumps(d, sort_keys=True))
    if len(seen) > 1:
        p.append(f"combo_roster 가 행마다 다르다 ({len(seen)} 가지) — 한 실행의 모집단은 하나다")
    # ⚠ Codex R13 P1-1: 아래까지가 전 판이다 — 전부 **산출이 스스로 적은 수끼리**의 대조라,
    #   32 행 중 하나를 미등록 Si 로 바꾸거나 1 행이 "authority=1" 이라고 적으면 그대로 통과했다.
    #   구성원을 독립적으로 정하지 않으면 개수 검사는 모집단을 지키지 못한다.
    from . import data as D
    bad_member = []
    for i, r in enumerate(rows):
        hc, si, w = r.get("half_cell"), r.get("si"), r.get("w_dqdv")
        try:
            wf = float(w) if w not in (None, "") else None
        except (TypeError, ValueError):
            wf = None
        if hc not in D.HALF_FILE or si not in D.SI_SOURCES or wf not in (0.0, 1.0):
            bad_member.append(f"행 {i}: 선언되지 않은 조합 ({hc!r}, {si!r}, {w!r}) — "
                              f"half_cell ∈ {sorted(D.HALF_FILE)} · si ∈ {D.SI_SOURCES} · w_dqdv ∈ {{0.0, 1.0}}")
    p += bad_member

    if seen and len(seen) == 1 and not p:
        d = json.loads(next(iter(seen)))
        if d["succeeded"] != len(rows):
            p.append(f"combo_roster.succeeded {d['succeeded']} ≠ 실제 행 수 {len(rows)} — 모집단 주장이 본문과 다르다")
        if d["requested"] != d["authority"]:
            p.append(f"{CANONICAL_SLOT_PREFIX}combo_roster.requested {d['requested']} ≠ authority "
                     f"{d['authority']} — 좁힌 실행은 정본이 아니다 (subset 이고 canonical 자리에 있으면 안 된다)")
        elif not p:
            # canonical 주장 → 본문 key 집합을 **독립 유도한 정본 집합**과 exact 로 댄다.
            try:
                want = canonical_combo_keys(state)
            except ValueError:
                # 상태는 **파일 이름**에서 온다. gate(`check_u14`)와 reader 는 언제나 이름을 넘기므로 여기 오지
                # 않는다 (`test_g06` 이 그것을 고정한다). 이름 없이 부른 content-only 호출에서는 구성원 집합을
                # 댈 근거가 없으므로 그 검사만 건너뛴다 — 위의 구성원 유효성 검사는 이미 돌았다.
                return p
            got = {matrix_key(r) for r in rows}
            if d["authority"] != len(want):
                p.append(f"combo_roster.authority {d['authority']} ≠ 상태 {state!r} 의 정본 조합 수 {len(want)} "
                         f"(Codex R13 P1-1)")
            extra, lack = sorted(got - want), sorted(want - got)
            if extra:
                p.append(f"본문에 정본 모집단 밖 조합이 있다 ({extra[:4]}{' 외' if len(extra) > 4 else ''})")
            if lack:
                p.append(f"canonical 주장인데 본문에 정본 조합이 빠졌다 ({lack[:4]}{' 외' if len(lack) > 4 else ''}) — "
                         f"{len(got)}/{len(want)}")
    return p


def check_gamma_roster(rows: list) -> list:
    """`gamma_roster` 는 **파싱되는 계약**이다 (Codex R11 P2-4: `"not-json"` 이 비어 있지 않다는 이유로 통과했다).

    exact key · 정본 격자 대비 requested · 산술(succeeded + |missing| == requested) · 행마다 같은 roster 를 본다.
    """
    p, seen = [], set()
    for i, r in enumerate(rows):
        raw = r.get("gamma_roster")
        try:
            d = json.loads(raw) if isinstance(raw, str) else raw
        except (TypeError, ValueError) as e:
            p.append(f"행 {i}: gamma_roster 가 JSON 이 아니다 ({e})"); continue
        if not isinstance(d, dict) or set(d) != {"authority", "requested", "succeeded", "missing"}:
            p.append(f"행 {i}: gamma_roster 의 key 가 계약과 다르다 — {sorted(d) if isinstance(d, dict) else type(d).__name__} "
                     f"(요구: authority · requested · succeeded · missing)"); continue
        miss = d["missing"]
        if not isinstance(miss, list) or not all(isinstance(x, (int, float)) and math.isfinite(x) for x in miss):
            p.append(f"행 {i}: gamma_roster.missing 이 유한 숫자 목록이 아니다 ({miss!r})"); continue
        # ⚠ 자체 리뷰 C04: `isinstance(True, int)` 이 참이라 bool 이 개수로 셌다.
        if not all(isinstance(d[k], int) and not isinstance(d[k], bool)
                   for k in ("authority", "requested", "succeeded")):
            p.append(f"행 {i}: gamma_roster 의 개수가 정수가 아니다 ({d!r})"); continue
        if d["succeeded"] + len(miss) != d["requested"]:
            p.append(f"행 {i}: gamma_roster 산술이 안 맞는다 — 성공 {d['succeeded']} + 누락 {len(miss)} ≠ 요청 {d['requested']}")
        if d["authority"] != CANONICAL_GAMMA_GRID_N:
            p.append(f"행 {i}: gamma_roster.authority {d['authority']} ≠ 정본 격자 {CANONICAL_GAMMA_GRID_N}")
        seen.add(json.dumps(d, sort_keys=True))
    if len(seen) > 1:
        p.append(f"gamma_roster 가 행마다 다르다 ({len(seen)} 가지) — 한 실행의 모집단은 하나다")
    # ⚠ 자체 리뷰 C04 (렌즈 3곳): 전 판은 roster 를 **본문과 한 번도 대보지 않았다** — 행 3 개짜리가
    #   "requested 3 · authority 21" 로 통과했고(좁힌 격자가 canonical 자리로), 21 행인데 "성공 1 · 누락 20" 도,
    #   "γ=0.5 는 실패했다" 면서 본문에 그 행이 있는 것도 전부 문제 0 이었다. 방어가 producer 한 자리뿐이었다.
    if seen and len(seen) == 1 and not p:
        d = json.loads(next(iter(seen)))
        if d["succeeded"] != len(rows):
            p.append(f"gamma_roster.succeeded {d['succeeded']} ≠ 실제 행 수 {len(rows)} — 모집단 주장이 본문과 다르다")
        if d["requested"] != d["authority"]:
            p.append(f"{CANONICAL_SLOT_PREFIX}gamma_roster.requested {d['requested']} ≠ authority "
                     f"{d['authority']} — 좁힌 격자는 정본이 아니다 (subset 이고 canonical 자리에 있으면 안 된다)")
        body = {float(r["gamma_Si"]) for r in rows if r.get("gamma_Si") not in (None, "")}
        miss = [float(x) for x in d["missing"]]
        ghost = sorted(body & set(miss))
        if ghost:
            p.append(f"gamma_roster.missing 이 본문에 있는 γ 를 누락이라 한다 ({ghost}) — 둘 중 하나가 거짓이다")
        # ⚠ Codex R13 P1-1: 여기까지가 전 판이다 — `authority` 를 **개수**하고만 댔으므로 γ 21 개를
        #   0~0.4 로 깔아도 정본이었고, `missing` 20 개가 전부 같은 값이어도 산술(1+20=21)만 맞으면 통과했다.
        if len(set(miss)) != len(miss):
            dup = sorted({x for x in miss if miss.count(x) > 1})
            p.append(f"gamma_roster.missing 에 중복이 있다 ({dup}) — 누락은 격자의 서로 다른 점이다 (Codex R13 P1-1)")
        want = canonical_gamma_grid()
        if d["requested"] == d["authority"]:          # canonical 주장
            union = sorted(body | set(miss))
            if not _same_grid(union, want):
                p.append(f"canonical 주장인데 본문 ∪ missing 이 정본 γ 격자가 아니다 — "
                         f"{len(union)} 점 [{min(union) if union else float('nan'):.4g}, "
                         f"{max(union) if union else float('nan'):.4g}] ≠ 정본 {len(want)} 점 "
                         f"[{want[0]:.4g}, {want[-1]:.4g}] (Codex R13 P1-1)")
    return p


def _finite_problems(x, where: str) -> list:
    """중첩 구조 안의 모든 숫자가 유한한가 (Codex R11 P1-8)."""
    if isinstance(x, bool):
        return []
    if isinstance(x, (int, float)):
        return [] if math.isfinite(x) else [f"{where}: 유한하지 않은 값 ({x!r})"]
    if isinstance(x, dict):
        return [m for k, v in x.items() for m in _finite_problems(v, f"{where}.{k}")]
    if isinstance(x, (list, tuple)):
        return [m for i, v in enumerate(x) for m in _finite_problems(v, f"{where}[{i}]")]
    if isinstance(x, str):
        # ⚠ 자체 리뷰 C06: 전 판은 str 을 그냥 통과시켜 손으로 쓴 JSON 의 `"1e999"`·`"Infinity"`·`"nan"` 이
        #   문제 0 이었다 (CSV 쪽은 `float()` 로 강제 파싱하는데 JSON 쪽만 비대칭). `_num_diff` 도 `float()` 를
        #   쓰므로 양쪽 다 `"1e999"` 면 `inf == inf` 로 숫자 차이까지 0 이 된다. 같은 규칙을 적용한다 —
        #   숫자로 **파싱되면** 유한해야 하고, 애초에 숫자가 아닌 라벨은 이 검사의 대상이 아니다.
        try:
            v = float(x)
        except (TypeError, ValueError):
            return []
        return [] if math.isfinite(v) else [f"{where}: 유한하지 않은 값 ({x!r})"]
    return []


def check_degeneracy(j: dict) -> list:
    # ⚠ Codex R13 P1-2: 전 판은 `in (None, "")` 이라 **빈 컨테이너**(`{}`·`[]`)가 "있음" 으로 셌다 —
    #   `ref_consumed_inputs: {}` 가 필수 키 검사도, 아래 truthy 가지도 둘 다 빠져나갔다.
    p = [f"키 없음: {k}" for k in DEGENERACY_KEYS
         if j.get(k) is None or (isinstance(j.get(k), (str, dict, list, tuple)) and len(j[k]) == 0)]
    p += check_degeneracy_shape(j)
    p += _finite_problems({k: v for k, v in j.items() if k not in ("env", "consumed_inputs", "ref_consumed_inputs")},
                          "degeneracy")
    if "consumed_inputs" in j:
        p += validate_receipt(j.get("consumed_inputs"), j.get("inputs_sha"), "consumed_inputs")
    # ⚠ Codex R13 P1-2: reference 는 **키가 있으면 언제나** 검증한다. 전 판은 (a) truthy 일 때만,
    #   (b) dict 일 때만 봤다 — 같은 불완전 reference 가 dict 면 걸리고 JSON 문자열이면 통과했다
    #   (`consumed_inputs` 쪽은 `receipt_text` 로 정규화하는데 여기만 비대칭이었다). candidate 의
    #   자기 계약은 baseline 의 나이와 무관하다.
    if "ref_consumed_inputs" in j:
        ref = receipt_text(j["ref_consumed_inputs"])
        if not ref:
            p.append("ref_consumed_inputs: 기준 실행의 입력 출처가 비어 있다 — 새 산출의 계약 위반이다 "
                     "(baseline 이 옛 스키마인 것과 별개다, Codex R13 P1-2)")
        else:
            p += [x for x in validate_receipt(ref, inputs_digest(ref), "ref_consumed_inputs") if "digest" not in x]
    return p
