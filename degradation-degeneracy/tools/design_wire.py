"""design_wire.py — pairing design 의 **canonical wire schema** 와 ID 도메인.

계약 v4 묶음 2. 25차 Q3: "묶음 9 는 planned leg index 를 key 로 쓰므로 묶음 2 의
wire schema · arm registry · hash domain · golden vector 가 먼저 고정돼야 한다."

무엇을 정하는가
───────────────
1. **직렬화 도메인** — 같은 설계가 언제나 같은 바이트가 되게 하는 규칙
2. **arm registry** — 어떤 arm 이 존재하고 각각 무엇을 분리하는가 (계약 §5)
3. **ID 사슬** — `pair_group_id → bank_id → candidate_id` (계약 §4.2)
4. **golden vector** — 위 셋이 조용히 바뀌지 않게 고정한 입력→digest 쌍

가장 중요한 규칙: **wire 에 이진 부동소수를 넣지 않는다.**
────────────────────────────────────────────────────────────
물리좌표를 float 로 실으면 `0.13` 이 처리 경로에 따라 다른 바이트가 되고, 같은
조건이 다른 `pair_group_id` 를 받는다. 계약 §4.2 가 "float 표현이 갈리면 같은
조건이 다른 ID 가 된다" 고 적은 것이 이것이다. 그래서 좌표는 **정확한 십진
문자열**로 싣고, 검증기가 float 를 거부한다.

`pair_group_id` 에서 **제외**하는 것과 그 이유도 wire 에 적는다 — 제외 결정
자체가 설계이기 때문이다 (계약 §4.2 표).
"""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation

from tools.preserve import canonical_bytes, digest

SCHEMA = "pairing-design/v6.0"

#: 좌표로 허용되는 십진 문자열. 지수표기·후행 쓰레기를 막는다.
_DECIMAL = re.compile(r"^-?(0|[1-9][0-9]*)(\.[0-9]+)?$")

#: 계약 §5 의 2×2. `p_ini` 가 있는 것은 half-cell 기준뿐이다.
ARM_REGISTRY: dict[str, dict] = {
    "A": {"p_ini_warm_start": False, "condition_warm_start": False,
          "role": "기준선", "reference": "halfcell"},
    "B": {"p_ini_warm_start": True, "condition_warm_start": False,
          "role": "원점 이동 단독", "reference": "halfcell"},
    "C": {"p_ini_warm_start": False, "condition_warm_start": True,
          "role": "조건 warm 단독", "reference": "halfcell"},
    "D": {"p_ini_warm_start": True, "condition_warm_start": True,
          "role": "상호작용 (현재 기본값)", "reference": "halfcell"},
    # 격자 기준에는 `p_ini` 가 없다 → C vs A 한 축만 필요하다 (계약 §5)
    "G_A": {"p_ini_warm_start": None, "condition_warm_start": False,
            "role": "격자 기준선", "reference": "grid"},
    "G_C": {"p_ini_warm_start": None, "condition_warm_start": True,
            "role": "격자 조건 warm", "reference": "grid"},
}

#: `pair_group_id` 에서 **제외**하는 축과 이유. 제외 결정 자체가 설계다.
EXCLUDED_FROM_PAIR_ID: dict[str, str] = {
    "arm": "arm 값을 넣으면 같은 물리 조건의 짝이 arm 마다 갈린다 — 짝을 만드는 것이 목적인데 그것을 부순다",
    "noise_realization": "잡음 실현은 지형을 바꾸지만 조건 정체성은 아니다 (계약 §12)",
    "objective": "같은 조건을 여러 목적함수로 재는 것이 설계다",
    "seed": "bank 는 조건 단위로 고정된다 — seed 는 bank_id 로 내려간다",
}


#: ★ 26차 P1-8 — source 마다 **다른** provenance 가 필요하다 (계약 §4.2).
#:   초판은 source enum 만 보고 임의 dict 를 그대로 해시했다. golden 도 셋 다
#:   같은 placeholder `{"i": 0}` 을 썼으므로 "candidate provenance 를 고정했다"
#:   는 말이 성립하지 않았다. 닫힌 schema 로 만든다 — 남거나 모자라면 거부.
CANDIDATE_PAYLOAD_SCHEMA: dict[str, dict[str, str]] = {
    "base_init": {
        "base_coord_sha256": "hex64",       # base 좌표의 exact-bytes digest
    },
    "warm": {
        "provider_objective": "str",        # 어느 목적함수가 seed 를 줬는가
        "provider_artifact_sha256": "hex64",
        "solution_map_sha256": "hex64",
    },
    "random": {
        "bank_index": "int",               # unit cube bank 의 행
        "unit_cube_bytes_sha256": "hex64",
    },
}


class WireError(ValueError):
    """wire schema 위반. 조용히 넘어가지 않는다."""


def _is_hex64(v) -> bool:
    return (isinstance(v, str) and len(v) == 64
            and all(c in "0123456789abcdef" for c in v))


def assert_wire_safe(obj, path: str = "$") -> None:
    """wire 에 실을 수 있는 형태인가 — **재귀적으로** 본다.

    ★ 26차 P1-8 — 공통 serializer 가 좌표 **밖**의 이진 float 를 그대로
      받았다. 좌표만 막아 봐야 payload 로 들어오면 같은 문제다.
    """
    if isinstance(obj, bool) or obj is None or isinstance(obj, (int, str)):
        return
    if isinstance(obj, float):
        raise WireError(f"{path}: wire 에 이진 부동소수를 넣을 수 없다 ({obj!r})")
    if isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            assert_wire_safe(v, f"{path}[{i}]")
        return
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not isinstance(k, str):
                raise WireError(f"{path}: dict 키가 문자열이 아니다 ({k!r})")
            assert_wire_safe(v, f"{path}.{k}")
        return
    raise WireError(f"{path}: wire 에 실을 수 없는 타입 {type(obj).__name__}")


def check_candidate_payload(source: str, payload) -> list[str]:
    """source 별 **닫힌** schema. 키가 남거나 모자라면 거부한다."""
    spec = CANDIDATE_PAYLOAD_SCHEMA.get(source)
    if spec is None:
        return [f"모르는 restart source: {source!r}"]
    if not isinstance(payload, dict):
        return [f"payload 가 dict 가 아니다: {type(payload).__name__}"]
    bad = []
    for k in sorted(set(payload) - set(spec)):
        bad.append(f"schema 에 없는 키: {k}")
    for k, kind in sorted(spec.items()):
        if k not in payload:
            bad.append(f"필수 키 없음: {k}")
            continue
        v = payload[k]
        if kind == "hex64" and not _is_hex64(v):
            bad.append(f"{k}: 64-hex 가 아니다 ({v!r})")
        elif kind == "int" and (isinstance(v, bool) or not isinstance(v, int)):
            bad.append(f"{k}: 정수가 아니다 ({v!r})")
        elif kind == "str" and (not isinstance(v, str) or not v):
            bad.append(f"{k}: 비어 있지 않은 문자열이어야 한다 ({v!r})")
    return bad


def decimal_from_float(x: float, places: int) -> str:
    """float 좌표 → **정확한 십진 문자열**. 왕복하지 않으면 거부한다.

    ★ 26차 P1-8 — `src/grid.py` 의 `Condition` 은 float 다. 그것을 wire 로
      옮기는 다리가 없으면 ID 체계가 실제 격자와 결속되지 않는다. 다만 조용히
      반올림하면 **다른 조건이 같은 ID 로 합쳐질 수 있다.** 그래서 변환 뒤
      `float(s) == x` 를 확인하고, 어긋나면 실패한다 — 자릿수를 올리든 격자를
      고치든 사람이 결정하게 만든다.
    """
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise WireError(f"좌표가 수가 아니다: {x!r}")
    s = _canon_decimal(f"{float(x):.{int(places)}f}")
    if float(s) != float(x):
        raise WireError(
            f"{x!r} 을 {places}자리 십진으로 왕복시키지 못했다 (얻은 값 {s!r}). "
            "조용히 반올림하면 다른 조건이 같은 ID 로 합쳐진다 — "
            "`decimal_places` 를 올리거나 격자 값을 고쳐라")
    return s


def coords_from_condition(cond, places: int) -> dict:
    """`src.grid.Condition` → wire 좌표. 제외 축(noise·seed)은 담지 않는다."""
    return {
        "lli": decimal_from_float(cond.lli, places),
        "lam_pe": decimal_from_float(cond.lam_pe, places),
        "lam_ne": decimal_from_float(cond.lam_ne, places),
        "lam_pe_type": cond.lam_pe_type,
        "lam_ne_type": cond.lam_ne_type,
    }


def _check_decimal(name: str, v) -> str:
    if isinstance(v, float):
        raise WireError(
            f"{name}: wire 에 이진 부동소수를 넣을 수 없다 ({v!r}). "
            "정확한 십진 문자열로 실어라 — float 표현이 갈리면 같은 조건이 "
            "다른 pair_group_id 를 받는다 (계약 §4.2)")
    if isinstance(v, bool) or not isinstance(v, (str, int, Decimal)):
        raise WireError(f"{name}: 좌표는 십진 문자열이어야 한다 ({v!r})")
    s = str(v)
    if not _DECIMAL.match(s):
        raise WireError(f"{name}: 십진 표기가 아니다 ({s!r}) — 지수표기·후행문자 금지")
    try:
        Decimal(s)
    except InvalidOperation as e:                       # pragma: no cover
        raise WireError(f"{name}: 십진 변환 실패 ({s!r})") from e
    return _canon_decimal(s)


def _canon_decimal(s: str) -> str:
    """`0.170` 과 `0.17` 을 같은 문자열로 만든다.

    ★ 이진 float 를 금지하는 것만으로는 부족하다 — 후행 0 이 남으면 같은 수가
      다른 `pair_group_id` 를 받아 조건이 조용히 split 된다. 계약 §4.2 가
      경고한 "오타 하나로 조용히 merge/split" 의 숫자판이다.

    `Decimal.normalize()` 는 `100` → `1E+2` 로 지수표기를 만들어 못 쓴다.
    문자열 수준에서 정규화한다.
    """
    if "." in s:
        head, _, frac = s.partition(".")
        frac = frac.rstrip("0")
        s = f"{head}.{frac}" if frac else head
    if s in ("-0", "-0.0"):
        s = "0"
    return s


def canonical_design_spec(*, label: str, arms: list[str],
                          parameter_order: list[str],
                          bounds_policy: str,
                          objective_plan: list[str],
                          bank_generator: str, bank_version: str,
                          seed_derivation: str, dtype: str, endian: str,
                          coordinate_unit: str, decimal_places: int = 12) -> dict:
    """계약 §4.2 표의 최소 구성. 빠진 항목이 있으면 만들 수 없다.

    ★ 26차 P1-7 — `label` 은 **hash 에 들어가지 않는다.** 계약 §4.2 가
      `pairing_design_label`(사람용)과 `pairing_design_sha256`(정본)을 나누라고
      했는데 초판은 label 을 해시 대상 dict 안에 넣었다. 그러면 뜻이 같은
      설계의 별칭만 바꿔도 모든 pair ID 가 바뀐다.
    """
    unknown = [a for a in arms if a not in ARM_REGISTRY]
    if unknown:
        raise WireError(f"등록되지 않은 arm: {unknown} (registry: {sorted(ARM_REGISTRY)})")
    if len(set(arms)) != len(arms):
        raise WireError(f"arm 중복: {arms}")
    if len(set(parameter_order)) != len(parameter_order):
        raise WireError(f"parameter 중복: {parameter_order}")
    if endian not in ("little", "big"):
        raise WireError(f"endian: {endian!r}")

    return {
        "schema": SCHEMA,
        # ★ `label` 은 여기 없다 — 사람용 별칭은 hash 밖이다 (P1-7).
        #   `design_label()` 로 따로 들고 다닌다.
        "coordinate": {
            "unit": coordinate_unit,
            "representation": "exact_decimal_string",
            "binary_float_allowed": False,
            "decimal_places": int(decimal_places),
        },
        "arms": {a: dict(ARM_REGISTRY[a], arm_id=a) for a in sorted(arms)},
        "excluded_from_pair_id": dict(EXCLUDED_FROM_PAIR_ID),
        "parameter_order": list(parameter_order),
        "bounds_equivalence_policy": bounds_policy,
        "objective_plan": sorted(objective_plan),
        "bank": {
            "generator": bank_generator,
            "version": bank_version,
            "seed_derivation": seed_derivation,
            "dtype": dtype,
            "endian": endian,
            "space": "unit_cube",
        },
        "serialization": {
            "encoding": "utf-8",
            "key_order": "sorted",
            "separators": [",", ":"],
            "trailing_newline": False,
            "nan_inf": "forbidden",
            "binary_float": "forbidden",
            "dict_keys": "string_only",
            "unicode": "nfc_utf8_no_escape",
        },
        "candidate_payload_schema": {k: dict(v)
                                     for k, v in CANDIDATE_PAYLOAD_SCHEMA.items()},
    }


def pairing_design_sha256(spec: dict) -> str:
    if spec.get("schema") != SCHEMA:
        raise WireError(f"schema 가 {SCHEMA} 가 아니다: {spec.get('schema')!r}")
    if "label" in spec:
        raise WireError("label 은 hash 대상이 아니다 — 별칭을 바꾸면 모든 "
                        "pair ID 가 바뀐다 (계약 §4.2 / 26차 P1-7)")
    assert_wire_safe(spec)
    return digest(spec)


def parameter_order_sha256(order: list[str]) -> str:
    return digest({"schema": "parameter-order/v1", "order": list(order)})


def pair_group_id(design_sha: str, coords: dict, param_order_sha: str) -> str:
    """계약 §4.2 — `H(design_sha, canonical(좌표), parameter_order_sha)`.

    좌표는 `lli · lam_pe · lam_ne` 와 두 `*_type` 이다. 값은 십진 문자열이어야
    하고, type 은 문자열이다.
    """
    need = ("lli", "lam_pe", "lam_ne", "lam_pe_type", "lam_ne_type")
    missing = [k for k in need if k not in coords]
    if missing:
        raise WireError(f"좌표에 빠진 키: {missing}")
    extra = sorted(set(coords) - set(need))
    if extra:
        raise WireError(f"좌표에 없어야 할 키: {extra} — "
                        f"제외 축은 {sorted(EXCLUDED_FROM_PAIR_ID)} 이다")
    canon = {k: _check_decimal(k, coords[k]) for k in ("lli", "lam_pe", "lam_ne")}
    for k in ("lam_pe_type", "lam_ne_type"):
        if not isinstance(coords[k], str) or not coords[k]:
            raise WireError(f"{k}: 문자열이어야 한다 ({coords[k]!r})")
        canon[k] = coords[k]
    return digest({"schema": "pair-group/v1", "design": design_sha,
                   "coords": canon, "parameter_order": param_order_sha})


def bank_id(pair_group: str, bank_version: str, unit_cube_bank_sha: str) -> str:
    return digest({"schema": "bank/v1", "pair_group_id": pair_group,
                   "bank_version": bank_version,
                   "unit_cube_bank_sha256": unit_cube_bank_sha})


def candidate_id(bank: str, exact_bounds_sha: str, source: str,
                 source_payload: dict) -> str:
    """source 별 **닫힌** provenance schema 를 강제한다 (계약 §4.2 / P1-8)."""
    if not _is_hex64(bank) or not _is_hex64(exact_bounds_sha):
        raise WireError("bank_id·exact_bounds_sha256 는 64-hex 여야 한다")
    bad = check_candidate_payload(source, source_payload)
    if bad:
        raise WireError(f"{source} payload: " + "; ".join(bad))
    assert_wire_safe(source_payload)
    return digest({"schema": "candidate/v2", "bank_id": bank,
                   "exact_bounds_sha256": exact_bounds_sha,
                   "source": source, "source_payload": source_payload})


__all__ = ["SCHEMA", "ARM_REGISTRY", "EXCLUDED_FROM_PAIR_ID",
           "CANDIDATE_PAYLOAD_SCHEMA", "WireError", "assert_wire_safe",
           "check_candidate_payload", "decimal_from_float",
           "coords_from_condition", "canonical_design_spec",
           "pairing_design_sha256", "parameter_order_sha256", "pair_group_id",
           "bank_id", "candidate_id", "canonical_bytes"]
