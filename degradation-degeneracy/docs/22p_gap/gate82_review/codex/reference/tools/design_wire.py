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

import hashlib
import re
import unicodedata
from decimal import Decimal, InvalidOperation

import numpy as np

from tools.preserve import canonical_bytes, digest

SCHEMA = "pairing-design/v6.3"

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
    if isinstance(obj, str):
        # ★ 27차 P1-9 — wire 가 `nfc_utf8_no_escape` 를 선언만 하고 강제하지
        #   않았다. NFC 로 같은 `é` 와 `e\u0301` 가 다른 digest 를 냈다.
        if unicodedata.normalize("NFC", obj) != obj:
            raise WireError(f"{path}: NFC 정규화되지 않은 문자열이다 ({obj!r})")
        return
    if isinstance(obj, bool) or obj is None or isinstance(obj, int):
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
            # ★ 28차 P1-6 — 값만 NFC 검사하고 **키는 안 봤다**. 분해형 키가
            #   그대로 통과해 같은 이름이 다른 digest 를 냈다.
            if unicodedata.normalize("NFC", k) != k:
                raise WireError(f"{path}: dict 키가 NFC 가 아니다 ({k!r})")
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
        elif kind == "int" and k == "bank_index" and v < 0:
            bad.append(f"{k}: 음수 bank index 는 없다 ({v!r})")
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
    if isinstance(decimal_places, bool) or not isinstance(decimal_places, int) \
            or not 1 <= decimal_places <= 30:
        raise WireError(f"decimal_places 는 1~30 정수여야 한다: {decimal_places!r}")
    if len(set(objective_plan)) != len(objective_plan) or not objective_plan:
        raise WireError(f"objective_plan 이 비었거나 중복이다: {objective_plan}")

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
        # ★ 27차 P1-9 — 초판은 정렬해서 **순서를 지웠다**. 계약의 objective
        #   order 와 warm provider 의미를 design identity 가 잃는다.
        "objective_plan": list(objective_plan),
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
        # 계약 §4.2 최소 구성 — 초판이 통째로 빠뜨렸다 (27차 P1-9)
        "parameter_coordinate_schema": {
            "pair_axes": ["lli", "lam_pe", "lam_ne", "lam_pe_type", "lam_ne_type"],
            "value_type": "exact_decimal_string",
            "type_axes_value_type": "str",
        },
    }


#: design spec 의 **닫힌** 키 집합. ★ 27차 P1-9 — 초판은 schema 문자열과
#: label 부재만 봤다. `{"schema": "pairing-design/v6.0"}` 하나로도 정상 digest 가
#: 나왔고 extra key 도 통과했다.
_DESIGN_KEYS = frozenset({
    "schema", "coordinate", "arms", "excluded_from_pair_id", "parameter_order",
    "bounds_equivalence_policy", "objective_plan", "bank", "serialization",
    "candidate_payload_schema", "parameter_coordinate_schema",
})


def pairing_design_sha256(spec: dict) -> str:
    if not isinstance(spec, dict):
        raise WireError(f"design spec 이 dict 가 아니다: {type(spec).__name__}")
    if spec.get("schema") != SCHEMA:
        raise WireError(f"schema 가 {SCHEMA} 가 아니다: {spec.get('schema')!r}")
    if "label" in spec:
        raise WireError("label 은 hash 대상이 아니다 — 별칭을 바꾸면 모든 "
                        "pair ID 가 바뀐다 (계약 §4.2 / 26차 P1-7)")
    if set(spec) != _DESIGN_KEYS:
        raise WireError(
            f"design spec 키 집합이 닫혀 있지 않다: 남음 {sorted(set(spec) - _DESIGN_KEYS)} "
            f"· 모자람 {sorted(_DESIGN_KEYS - set(spec))}")
    bad = _check_design_nested(spec)
    if bad:
        raise WireError("design spec nested schema 위반: " + "; ".join(bad[:4]))
    assert_wire_safe(spec)
    return digest(spec)


def _nonempty_str(v) -> bool:
    return isinstance(v, str) and bool(v) and \
        unicodedata.normalize("NFC", v) == v


def _exact_bool(v) -> bool:
    """`False == 0` 이므로 bool 을 따로 본다 (29차 P1-6)."""
    return isinstance(v, bool)


def _check_design_nested(spec: dict) -> list[str]:
    """★ 28차 P1-6 — 초판 validator 는 **top-level 키만** 닫았다.

    factory 는 엄격했지만 역직렬화한 외부 spec 을 해시하는 validator 는 nested
    를 다시 보지 않았다. 리뷰가 준 다섯 변이가 전부 정상 digest 를 냈다:
    `empty_coordinate` · `fake_arm` · `duplicate_objectives` ·
    `open_serialization` · `empty_candidate_schema`.
    """
    bad = []
    co = spec.get("coordinate")
    if not isinstance(co, dict) or set(co) != {
            "unit", "representation", "binary_float_allowed", "decimal_places"}:
        bad.append(f"coordinate 블록이 닫혀 있지 않다: {co!r}")
    elif (not _nonempty_str(co.get("unit"))
          or co["representation"] != "exact_decimal_string"
          or not _exact_bool(co.get("binary_float_allowed"))
          or co["binary_float_allowed"]):
        bad.append(f"coordinate 정책이 계약과 다르다: {co!r}")
    elif isinstance(co["decimal_places"], bool) or \
            not isinstance(co["decimal_places"], int) or \
            not 1 <= co["decimal_places"] <= 30:
        bad.append(f"decimal_places: {co['decimal_places']!r}")

    arms = spec.get("arms")
    if not isinstance(arms, dict) or not arms:
        bad.append("arms 가 비었다")
    else:
        for a, v in arms.items():
            if a not in ARM_REGISTRY:
                bad.append(f"등록되지 않은 arm: {a!r}")
            elif v != dict(ARM_REGISTRY[a], arm_id=a):
                bad.append(f"arm {a} 의 내용이 registry 와 다르다")

    for name in ("parameter_order", "objective_plan"):
        v = spec.get(name)
        if not isinstance(v, list) or not v or len(set(v)) != len(v):
            bad.append(f"{name} 이 비었거나 중복이다: {v!r}")
        elif not all(_nonempty_str(x) for x in v):
            bad.append(f"{name} 의 원소가 비어 있거나 NFC 가 아니다: {v!r}")
    if not _nonempty_str(spec.get("bounds_equivalence_policy")):
        bad.append(f"bounds_equivalence_policy: {spec.get('bounds_equivalence_policy')!r}")
    ex = spec.get("excluded_from_pair_id")
    if ex != dict(EXCLUDED_FROM_PAIR_ID):
        bad.append("excluded_from_pair_id 가 정본과 다르다 — 제외 결정 자체가 설계다")

    ser = spec.get("serialization")
    want_ser = {"encoding": "utf-8", "key_order": "sorted",
                "separators": [",", ":"], "trailing_newline": False,
                "nan_inf": "forbidden", "binary_float": "forbidden",
                "dict_keys": "string_only", "unicode": "nfc_utf8_no_escape"}
    if ser != want_ser:
        bad.append("serialization 블록이 정본과 다르다")

    cps = spec.get("candidate_payload_schema")
    if cps != {k: dict(v) for k, v in CANDIDATE_PAYLOAD_SCHEMA.items()}:
        bad.append("candidate_payload_schema 가 정본과 다르다")

    pcs = spec.get("parameter_coordinate_schema")
    if not isinstance(pcs, dict) or set(pcs) != {
            "pair_axes", "value_type", "type_axes_value_type"}:
        bad.append("parameter_coordinate_schema 가 닫혀 있지 않다")
    elif (pcs["pair_axes"] != ["lli", "lam_pe", "lam_ne",
                               "lam_pe_type", "lam_ne_type"]
          or pcs["value_type"] != "exact_decimal_string"
          or pcs["type_axes_value_type"] != "str"):
        bad.append(f"parameter_coordinate_schema 값이 계약과 다르다: {pcs!r}")

    ba = spec.get("bank")
    if not isinstance(ba, dict) or set(ba) != {
            "generator", "version", "seed_derivation", "dtype", "endian", "space"}:
        bad.append("bank 블록이 닫혀 있지 않다")
    elif (ba["endian"] not in ("little", "big") or ba["space"] != "unit_cube"
          or not all(_nonempty_str(ba[k]) for k in
                     ("generator", "version", "seed_derivation", "dtype"))):
        bad.append(f"bank 정책이 계약과 다르다: {ba!r}")
    return bad


def parameter_order_sha256(order: list[str]) -> str:
    if not isinstance(order, list) or not order or len(set(order)) != len(order) \
            or not all(_nonempty_str(x) for x in order):
        raise WireError(f"parameter_order 가 비었거나 중복이거나 NFC 문자열이 "
                        f"아니다: {order!r}")
    return digest({"schema": "parameter-order/v1", "order": list(order)})


def pair_group_id(design_sha: str, coords: dict, param_order_sha: str) -> str:
    """계약 §4.2 — `H(design_sha, canonical(좌표), parameter_order_sha)`.

    좌표는 `lli · lam_pe · lam_ne` 와 두 `*_type` 이다. 값은 십진 문자열이어야
    하고, type 은 문자열이다.
    """
    # ★ 28차 P1-6 — 부모 digest 의 domain 을 검사하지 않았다.
    for name, v in (("design_sha", design_sha), ("param_order_sha", param_order_sha)):
        if not _is_hex64(v):
            raise WireError(f"{name} 가 64-hex 가 아니다: {v!r}")
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
        if unicodedata.normalize("NFC", coords[k]) != coords[k]:
            raise WireError(f"{k}: NFC 가 아니다 ({coords[k]!r}) — 같은 글자의 "
                            "두 표현이 다른 pair_group_id 를 받는다")
        canon[k] = coords[k]
    return digest({"schema": "pair-group/v1", "design": design_sha,
                   "coords": canon, "parameter_order": param_order_sha})


def bank_id(pair_group: str, bank_version: str, unit_cube_bank_sha: str) -> str:
    for name, v in (("pair_group_id", pair_group),
                    ("unit_cube_bank_sha256", unit_cube_bank_sha)):
        if not _is_hex64(v):
            raise WireError(f"{name} 가 64-hex 가 아니다: {v!r}")
    if not _nonempty_str(bank_version):
        raise WireError(f"bank_version 이 비었거나 NFC 가 아니다: {bank_version!r}")
    return digest({"schema": "bank/v1", "pair_group_id": pair_group,
                   "bank_version": bank_version,
                   "unit_cube_bank_sha256": unit_cube_bank_sha})


def design_binding(*, design: dict, coords: dict,
                   unit_cube_bank_sha256: str) -> dict:
    """**봉인된 design 에서** ID chain 을 통째로 유도한다.

    ★ 30차 P1-4 — `candidate_id` 의 `objective_plan` 이 caller 의 자유
      인자였다. 다른 design 의 bank 에, design 밖 목적함수를 쓰면서, 그
      목적함수를 담은 plan 을 자기가 같이 넘기면 통과했다.

    ★ 31차 P1-4 — 30차판은 그것을 **dict 로 한 겹 포장했을 뿐**이었다.
      `candidate_id` 가 key set 과 `bank == binding["bank_id"]` 만 봐서,
      나머지를 아무 값으로 채운 dict 가 그대로 통했다. 그리고
      `parameter_order_sha256` 과 `bank_version` 도 여전히 caller 인자여서,
      design 안의 `parameter_order` · `bank.version` 과 다른 값을 주장해도
      chain 이 만들어졌다.

      이제 **design 봉인물 안에 있는 것은 밖에서 받지 않는다.** order 와
      bank version 은 design 에서 읽고, `candidate_id` 는 preimage 를 받아
      chain 을 **자기가 다시 유도**한다 (`binding` 을 신뢰하지 않는다).

    `unit_cube_bank_sha256` 만 밖에서 받는다 — bank 바이트는 design 이 아니라
    생성기의 산출물이라 봉인물 안에 없다.
    """
    if not isinstance(design, dict):
        raise WireError(f"design 이 dict 가 아니다: {type(design).__name__}")
    for k in ("objective_plan", "parameter_order", "bank"):
        if k not in design:
            raise WireError(f"design 봉인물이 아니다 — {k} 가 없다")
    bank_version = (design.get("bank") or {}).get("version")
    if not _nonempty_str(bank_version):
        raise WireError(f"design 의 bank.version 이 이상하다: {bank_version!r}")
    pos = parameter_order_sha256(design["parameter_order"])
    d_sha = pairing_design_sha256(design)
    pg = pair_group_id(d_sha, coords, pos)
    bk = bank_id(pg, bank_version, unit_cube_bank_sha256)
    return {"pairing_design_sha256": d_sha, "pair_group_id": pg, "bank_id": bk,
            "parameter_order_sha256": pos, "bank_version": bank_version,
            "objective_plan": list(design["objective_plan"])}


def candidate_id(exact_bounds_sha: str, source: str, source_payload: dict, *,
                 design: dict, coords: dict,
                 unit_cube_bank_sha256: str) -> str:
    """source 별 **닫힌** provenance schema 를 강제한다 (계약 §4.2 / P1-8).

    ★ 30차 P1-4 — `objective_plan` 이 caller 의 자유 인자였다.
    ★ 31차 P1-4 — 30차판은 그것을 **dict 로 한 겹 포장했을 뿐**이었다.
      `binding` 의 key set 과 `bank == binding["bank_id"]` 만 봤으므로, 나머지를
      아무 값으로 채운 dict 가 그대로 통했다 (리뷰가 준 `forged` 반례).

      규칙은 두 회차째 같다 — **받을 수 있다는 것 자체가 결함이다.** 그래서
      `binding` 인자를 없앴다. 이 함수는 봉인물(design·coords·bank 바이트)만
      받고 chain 을 **자기가 유도**한다. 위조할 자리가 없다.
    """
    if not _is_hex64(exact_bounds_sha):
        raise WireError(f"exact_bounds_sha256 는 64-hex 여야 한다: {exact_bounds_sha!r}")
    b = design_binding(design=design, coords=coords,
                       unit_cube_bank_sha256=unit_cube_bank_sha256)
    if source == "warm":
        po = (source_payload or {}).get("provider_objective")
        if po not in b["objective_plan"]:
            raise WireError(f"provider_objective 가 design 의 objective 가 "
                            f"아니다: {po!r} ∉ {b['objective_plan']}")
    bad = check_candidate_payload(source, source_payload)
    if bad:
        raise WireError(f"{source} payload: " + "; ".join(bad))
    assert_wire_safe(source_payload)
    return digest({"schema": "candidate/v2", "bank_id": b["bank_id"],
                   "exact_bounds_sha256": exact_bounds_sha,
                   "source": source, "source_payload": source_payload})


__all__ = ["SCHEMA", "ARM_REGISTRY", "EXCLUDED_FROM_PAIR_ID",
           "CANDIDATE_PAYLOAD_SCHEMA", "WireError", "assert_wire_safe",
           "check_candidate_payload", "decimal_from_float",
           "coords_from_condition", "canonical_design_spec",
           "pairing_design_sha256", "parameter_order_sha256", "pair_group_id",
           "bank_id", "design_binding", "candidate_id", "canonical_bytes"]


# ─────────────────────────────────────────────────────────────────────────────
# 81차 — 단계 3 라운드 1 (G81-N1·N3 · Q1) : unit-cube bank · 후보 배열 · planned roster · provider edge
# 고정 표: docs/22p_gap/STAGE3_IMPL_ROUND1_SPEC.md §3·§4. ID 도메인(pair-group/v1 · bank/v1 ·
# candidate/v2)과 golden 은 여기서 바꾸지 않는다 — 아래는 그 preimage 에 **실물 바이트**를 공급하는 쪽이다.
# ─────────────────────────────────────────────────────────────────────────────

STAGE3_STAGES = ("condition", "p_ini")
ROSTER_SCHEMA = "planned-roster/v1"
OBS_KEY_FIELDS = ("comparison_family_id", "pair_group_id", "treatment_id",
                  "noise_level", "noise_realization_id", "replicate_id")
PROVIDER_EDGE_KEYS = frozenset({
    "stage", "arm", "consumer_objective", "provider_objective",
    "provider_artifact_sha256", "solution_map_sha256", "provider_protocol_sha256"})
_RESTART_SOURCES_ORDERED = ("base_init", "warm", "random")


def _pos_int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool) and v > 0


def _bank_seed(pair_group_id: str, bank_version: str) -> int:
    """seed derivation `H(pair_group_id, bank_version)` — 공유 pair group 기준.

    조건별 `cond_id` seed(noise·seed 포함)를 여기 쓰지 않는다: 같은 물리좌표의 다른 잡음 실현이
    **같은 bank** 를 받아야 짝 비교가 성립한다 (계약 §4.2 · 리뷰 §6).
    """
    if not _is_hex64(pair_group_id):
        raise WireError(f"pair_group_id 가 64-hex 가 아니다: {pair_group_id!r}")
    if not _nonempty_str(bank_version):
        raise WireError(f"bank_version 이 비었거나 NFC 가 아니다: {bank_version!r}")
    h = digest({"schema": "bank-seed/v1", "pair_group_id": pair_group_id,
                "bank_version": bank_version})
    return int(h[:16], 16)


def unit_cube_bank(pair_group_id: str, bank_version: str, length: int,
                   n_params: int) -> np.ndarray:
    """봉인 **full bank** — `(length, n_params)` float64, unit cube `[0, 1)`.

    B 마다 짧은 bank 를 다시 만들지 않는다. 계획은 이 full bank 의 prefix 를 소비하고,
    소비한 길이는 실현 기록(`random_bank_prefix_len`)에만 적는다 (리뷰 §6).
    """
    for name, v in (("length", length), ("n_params", n_params)):
        if not _pos_int(v):
            raise WireError(f"{name} 는 양의 정수여야 한다: {v!r}")
    rng = np.random.Generator(np.random.PCG64(_bank_seed(pair_group_id, bank_version)))
    return rng.uniform(0.0, 1.0, size=(int(length), int(n_params))).astype(np.float64)


def bank_bytes(bank) -> bytes:
    arr = np.ascontiguousarray(np.asarray(bank, dtype="<f8"))
    if arr.ndim != 2 or arr.size == 0:
        raise WireError(f"bank 는 비어 있지 않은 2차원 배열이어야 한다: shape {arr.shape}")
    if not np.isfinite(arr).all():
        raise WireError("bank 에 비유한 값이 있다")
    return arr.tobytes(order="C")


def unit_cube_bank_sha256(bank) -> str:
    """full-bank identity. prefix 길이와 무관하다."""
    return hashlib.sha256(bank_bytes(bank)).hexdigest()


def unit_cube_bytes_sha256(row) -> str:
    """선택한 **실제 row** 의 바이트 digest — `candidate/v2` random payload 의 preimage."""
    arr = np.ascontiguousarray(np.asarray(row, dtype="<f8"))
    if arr.ndim != 1 or arr.size == 0 or not np.isfinite(arr).all():
        raise WireError(f"bank row 는 유한한 1차원 배열이어야 한다: shape {arr.shape}")
    return hashlib.sha256(arr.tobytes()).hexdigest()


def _bounds_arrays(lb, ub) -> tuple[np.ndarray, np.ndarray]:
    lb = np.ascontiguousarray(np.asarray(lb, dtype="<f8"))
    ub = np.ascontiguousarray(np.asarray(ub, dtype="<f8"))
    if lb.ndim != 1 or lb.shape != ub.shape or lb.size == 0:
        raise WireError(f"lb/ub 는 같은 길이의 1차원 배열이어야 한다: {lb.shape} vs {ub.shape}")
    if not (np.isfinite(lb).all() and np.isfinite(ub).all()) or (lb > ub).any():
        raise WireError("lb/ub 가 비유한이거나 lb > ub 인 자리가 있다")
    return lb, ub


def exact_bounds_sha256(lb, ub) -> str:
    """실제 ordered `lb/ub` 바이트의 digest — preset 이름이 아니다 (계약 §4.2)."""
    lb, ub = _bounds_arrays(lb, ub)
    return hashlib.sha256(b"exact-bounds/v1" + lb.tobytes() + ub.tobytes()).hexdigest()


def map_unit_to_bounds(u, lb, ub) -> np.ndarray:
    """`x0 = lb + u·(ub − lb)` — unit cube 행을 실제 bounds 로 사상한다 (float64)."""
    lb, ub = _bounds_arrays(lb, ub)
    u = np.asarray(u, dtype=np.float64)
    if u.shape != lb.shape:
        raise WireError(f"unit row 길이 {u.shape} ≠ bounds 길이 {lb.shape}")
    if not np.isfinite(u).all() or (u < 0.0).any() or (u > 1.0).any():
        raise WireError("unit row 는 [0, 1] 안의 유한값이어야 한다")
    return (lb + u * (ub - lb)).astype(np.float64)


def x0_sha256(x0) -> str:
    """solver 에 **실제로 전달한** 초기값의 바이트 digest (표 C x0 결속)."""
    arr = np.ascontiguousarray(np.asarray(x0, dtype="<f8"))
    if arr.ndim != 1 or arr.size == 0 or not np.isfinite(arr).all():
        raise WireError(f"x0 는 유한한 1차원 배열이어야 한다: shape {arr.shape}")
    return hashlib.sha256(arr.tobytes()).hexdigest()


def candidate_plan(mode: str, budget: int, has_provider: bool) -> list[tuple[str, int | None]]:
    """계약 §3 표의 후보 배열 — `(source, bank_index)` 순서 목록.

    provider 가 없는 연쇄 첫 번째는 어느 mode 든 `[base] + bank[:B-1]` 다. random 의 index 는
    0 부터 순서대로이고, J 정렬 순서와 무관하다. 지원하지 않는 mode/B 는 **거부**한다 — legacy
    난수 경로로 조용히 대체하지 않는다 (리뷰 §6).
    """
    from tools.preserve import candidate_modes
    if mode not in candidate_modes():
        raise WireError(f"candidate_mode 가 계약 §3 enum 이 아니다: {mode!r}")
    if not _pos_int(budget):
        raise WireError(f"총 시작점 예산 B 는 양의 정수여야 한다: {budget!r}")
    if not isinstance(has_provider, bool):
        raise WireError(f"has_provider 는 bool 이어야 한다: {has_provider!r}")
    if not has_provider:
        head, n_random = ["base_init"], budget - 1
    elif mode == "legacy_slot_replace":
        head, n_random = ["warm"], budget - 1
    elif mode == "equal_start_count_base_retained":
        if budget < 2:
            raise WireError("equal_start_count_base_retained 는 provider 가 있을 때 B ≥ 2 여야 한다")
        head, n_random = ["base_init", "warm"], budget - 2
    elif mode == "union":
        head, n_random = ["base_init", "warm"], budget - 1
    else:                                                   # pragma: no cover — enum 이 늘면 여기서 멈춘다
        raise WireError(f"이번 라운드가 지원하지 않는 mode: {mode!r}")
    plan: list[tuple[str, int | None]] = [(s, None) for s in head]
    plan += [("random", i) for i in range(n_random)]
    return plan


def planned_counts(mode: str, budget_by_objective: dict, warm_provider_map: dict) -> dict:
    """계획 count — mode · B · provider 유무에서 **유도**한다. 실행 결과가 아니다 (G81-N1)."""
    if not isinstance(budget_by_objective, dict) or not budget_by_objective:
        raise WireError("budget_by_objective 가 비었다")
    if not isinstance(warm_provider_map, dict) or set(warm_provider_map) != set(budget_by_objective):
        raise WireError("warm_provider_map 의 objective 집합이 budget_by_objective 와 다르다")
    out = {}
    for obj, b in budget_by_objective.items():
        plan = candidate_plan(mode, b, warm_provider_map[obj] is not None)
        out[obj] = {s: sum(1 for src, _ in plan if src == s) for s in _RESTART_SOURCES_ORDERED}
    return out


def obs_key(*, comparison_family_id: str, pair_group_id: str, treatment_id: str,
            noise_level, noise_realization_id: str, replicate_id: int) -> dict:
    """79차 합의 관측 쌍 key (GATE78 §2.1). objective 는 key 의 값이 아니다 — 비교의 두 열이다."""
    for name, v in (("comparison_family_id", comparison_family_id), ("treatment_id", treatment_id),
                    ("noise_realization_id", noise_realization_id)):
        if not _nonempty_str(v):
            raise WireError(f"{name} 가 비었거나 NFC 문자열이 아니다: {v!r}")
    if not _is_hex64(pair_group_id):
        raise WireError(f"pair_group_id 가 64-hex 가 아니다: {pair_group_id!r}")
    if isinstance(replicate_id, bool) or not isinstance(replicate_id, int) or replicate_id < 0:
        raise WireError(f"replicate_id 는 0 이상의 정수여야 한다: {replicate_id!r}")
    return {"comparison_family_id": comparison_family_id, "pair_group_id": pair_group_id,
            "treatment_id": treatment_id, "noise_level": _check_decimal("noise_level", noise_level),
            "noise_realization_id": noise_realization_id, "replicate_id": int(replicate_id)}


def _check_roster_entry(i: int, e) -> list[str]:
    bad = []
    if not isinstance(e, dict) or set(e) != {"obs_key", "cond_id", "pair_group_id"}:
        return [f"roster[{i}]: 항목 키가 {{obs_key, cond_id, pair_group_id}} 가 아니다"]
    k = e["obs_key"]
    if not isinstance(k, dict) or set(k) != set(OBS_KEY_FIELDS):
        return [f"roster[{i}]: obs_key 필드가 {list(OBS_KEY_FIELDS)} 가 아니다 "
                f"(objective 는 key 의 값이 아니다): {sorted(k) if isinstance(k, dict) else k!r}"]
    try:
        obs_key(**k)
    except WireError as ex:
        bad.append(f"roster[{i}]: {ex}")
    if not _nonempty_str(e["cond_id"]):
        bad.append(f"roster[{i}]: cond_id 가 비었다")
    if e["pair_group_id"] != k.get("pair_group_id"):
        bad.append(f"roster[{i}]: pair_group_id 가 obs_key 의 것과 다르다")
    return bad


def check_roster(entries) -> list[str]:
    """planned roster 의 구조 오류 — 중복 obs_key · cond_id 충돌(교차 seed) · key 안의 objective 는 **거부**."""
    if not isinstance(entries, list) or not entries:
        return ["roster 가 비어 있거나 목록이 아니다"]
    bad = []
    seen_key: dict[tuple, str] = {}
    seen_cond: dict[str, int] = {}
    for i, e in enumerate(entries):
        bad += _check_roster_entry(i, e)
        if not isinstance(e, dict) or not isinstance(e.get("obs_key"), dict):
            continue
        kt = tuple(e["obs_key"].get(f) for f in OBS_KEY_FIELDS)
        if kt in seen_key:
            bad.append(f"roster[{i}]: obs_key 중복 (cond_id {e.get('cond_id')!r} 와 {seen_key[kt]!r})")
        else:
            seen_key[kt] = e.get("cond_id")
        c = e.get("cond_id")
        if c in seen_cond:
            bad.append(f"roster[{i}]: cond_id {c!r} 가 roster[{seen_cond[c]}] 와 충돌 — 한 cond_id 는 한 obs_key 다")
        else:
            seen_cond[c] = i
    return bad


def _canonical_roster(entries) -> list[dict]:
    return sorted(({"obs_key": {f: e["obs_key"][f] for f in OBS_KEY_FIELDS},
                    "cond_id": e["cond_id"], "pair_group_id": e["pair_group_id"]} for e in entries),
                  key=lambda e: e["cond_id"])


def roster_sha256(entries) -> str:
    """사전 roster 의 내용 주소. 구조 오류가 있는 roster 는 digest 를 내지 않는다."""
    bad = check_roster(entries)
    if bad:
        raise WireError("roster 구조 오류: " + "; ".join(bad[:4]))
    return digest({"schema": ROSTER_SCHEMA, "entries": _canonical_roster(entries)})


def roster_from_conditions(conds, *, design: dict, comparison_family_id: str,
                           treatment_id: str, replicate_id: int) -> list[dict]:
    """`src.grid.Condition` 목록 → planned roster. `cond_id ↔ obs_key ↔ pair_group_id` 일대일."""
    if not isinstance(design, dict) or "coordinate" not in design:
        raise WireError("design 봉인물이 아니다 — coordinate 블록이 없다")
    places = int(design["coordinate"]["decimal_places"])
    d_sha = pairing_design_sha256(design)
    pos = parameter_order_sha256(design["parameter_order"])
    entries = []
    for c in conds:
        coords = coords_from_condition(c, places)
        pg = pair_group_id(d_sha, coords, pos)
        entries.append({"obs_key": obs_key(comparison_family_id=comparison_family_id, pair_group_id=pg,
                                           treatment_id=treatment_id,
                                           noise_level=decimal_from_float(float(c.noise), places),
                                           noise_realization_id=str(int(c.seed)),
                                           replicate_id=replicate_id),
                        "cond_id": str(c.cond_id), "pair_group_id": pg})
    bad = check_roster(entries)
    if bad:
        raise WireError("조건 집합이 roster 가 되지 못한다: " + "; ".join(bad[:4]))
    return _canonical_roster(entries)


def check_provider_edges(edges, *, objective_order: list, warm_provider_map: dict, arm: str) -> list[str]:
    """provider edge 선언 ↔ warm_provider_map ↔ arm 의 정합성 (표 C).

    no-provider 는 (a) `objective_order[0]` 이거나 (b) arm 의 `condition_warm_start=False` 일 때만이다.
    warm 이 필요한 자리(warm arm 의 두 번째 이후 objective)의 null 은 **오류**다 — no-warm 으로
    전환하지 않는다 (G81-N3). `stage="p_ini"` edge 는 이번 라운드 명시 거부다.
    """
    bad = []
    if arm not in ARM_REGISTRY:
        return [f"등록되지 않은 arm: {arm!r}"]
    warm_on = ARM_REGISTRY[arm]["condition_warm_start"] is True
    if not isinstance(objective_order, list) or not objective_order or \
            len(set(objective_order)) != len(objective_order):
        return [f"objective_order 가 비었거나 중복이다: {objective_order!r}"]
    if not isinstance(warm_provider_map, dict) or set(warm_provider_map) != set(objective_order):
        return [f"warm_provider_map 의 objective 집합이 objective_order 와 다르다: "
                f"{sorted(warm_provider_map) if isinstance(warm_provider_map, dict) else warm_provider_map!r}"]
    pos = {o: i for i, o in enumerate(objective_order)}
    for obj, prov in warm_provider_map.items():
        if prov is None:
            if warm_on and pos[obj] > 0:
                bad.append(f"warm arm {arm} 의 {obj!r} 에 provider 가 없다 — no-warm 전환 금지 (첫 objective 만 null 가능)")
            continue
        if not warm_on:
            bad.append(f"arm {arm} 은 condition warm 이 꺼져 있는데 {obj!r} 에 provider {prov!r} 가 있다")
        if prov not in pos:
            bad.append(f"{obj!r} 의 provider {prov!r} 가 objective_order 에 없다")
        elif prov == obj:
            bad.append(f"{obj!r} 가 자기 자신을 provider 로 삼는다")
        elif pos[prov] >= pos[obj]:
            bad.append(f"provider {prov!r} 가 consumer {obj!r} 보다 앞서지 않는다 (순환/역방향)")
    if not isinstance(edges, list):
        return bad + [f"provider_edges 가 목록이 아니다: {type(edges).__name__}"]
    seen: set[str] = set()
    for i, e in enumerate(edges):
        if not isinstance(e, dict) or set(e) != PROVIDER_EDGE_KEYS:
            bad.append(f"edge[{i}]: 키 집합이 닫혀 있지 않다: "
                       f"{sorted(e) if isinstance(e, dict) else type(e).__name__}")
            continue
        if e["stage"] == "p_ini":
            bad.append(f"edge[{i}]: stage='p_ini' 는 이번 라운드 명시 거부 (선언만 · 구현 다음 라운드)")
        elif e["stage"] not in STAGE3_STAGES:
            bad.append(f"edge[{i}]: stage {e['stage']!r} 는 {STAGE3_STAGES} 가 아니다")
        if e["arm"] != arm:
            bad.append(f"edge[{i}]: arm {e['arm']!r} ≠ {arm!r}")
        c, p = e["consumer_objective"], e["provider_objective"]
        if c not in pos:
            bad.append(f"edge[{i}]: consumer {c!r} 가 objective_order 에 없다")
        elif warm_provider_map.get(c) != p:
            bad.append(f"edge[{i}]: provider {p!r} 가 warm_provider_map[{c!r}]={warm_provider_map.get(c)!r} 와 다르다")
        if c in seen:
            bad.append(f"edge[{i}]: consumer {c!r} 의 edge 가 중복이다")
        seen.add(c)
        for k in ("provider_artifact_sha256", "solution_map_sha256", "provider_protocol_sha256"):
            if not _is_hex64(e[k]):
                bad.append(f"edge[{i}]: {k} 가 64-hex 가 아니다")
    want = {o for o, p in warm_provider_map.items() if p is not None}
    missing = sorted(want - seen)
    if missing:
        bad.append(f"warm_provider_map 은 provider 를 말하는데 edge 가 없는 consumer: {missing}")
    return bad


__all__ += ["STAGE3_STAGES", "ROSTER_SCHEMA", "OBS_KEY_FIELDS", "PROVIDER_EDGE_KEYS",
            "unit_cube_bank", "bank_bytes", "unit_cube_bank_sha256", "unit_cube_bytes_sha256",
            "exact_bounds_sha256", "map_unit_to_bounds", "x0_sha256", "candidate_plan",
            "planned_counts", "obs_key", "check_roster", "roster_sha256",
            "roster_from_conditions", "check_provider_edges"]
