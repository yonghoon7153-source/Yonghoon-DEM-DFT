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


class WireError(ValueError):
    """wire schema 위반. 조용히 넘어가지 않는다."""


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
                          coordinate_unit: str) -> dict:
    """계약 §4.2 표의 최소 구성. 빠진 항목이 있으면 만들 수 없다."""
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
        "label": label,                     # 사람용 별칭 — 정본은 digest
        "coordinate": {
            "unit": coordinate_unit,
            "representation": "exact_decimal_string",
            "binary_float_allowed": False,
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
        },
    }


def pairing_design_sha256(spec: dict) -> str:
    if spec.get("schema") != SCHEMA:
        raise WireError(f"schema 가 {SCHEMA} 가 아니다: {spec.get('schema')!r}")
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
    if source not in ("base_init", "warm", "random"):
        raise WireError(f"모르는 restart source: {source!r}")
    return digest({"schema": "candidate/v1", "bank_id": bank,
                   "exact_bounds_sha256": exact_bounds_sha,
                   "source": source, "source_payload": source_payload})


__all__ = ["SCHEMA", "ARM_REGISTRY", "EXCLUDED_FROM_PAIR_ID", "WireError",
           "canonical_design_spec", "pairing_design_sha256",
           "parameter_order_sha256", "pair_group_id", "bank_id", "candidate_id",
           "canonical_bytes"]
