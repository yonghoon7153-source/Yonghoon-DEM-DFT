"""What the fitted numbers mean, once you say what kind of cell it was.

A fit gives ``R1`` and ``R2``.  Only the measurement says whether those are an
SEI film and a charge transfer, or a grain interior and a grain boundary --
they are the same two arcs and different physics (ADR 0019).  Naming them is a
separate step from finding them, and it happens here so the fitter never has to
know what was in the cell.

Conductivity is computed here too, not stored: it needs a thickness and an area
and those get corrected (ADR 0001).  Fixing a micrometer reading has to move
every sigma without re-reading a single file.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .circuit import CircuitError, parse_circuit
from .fit import FitResult

__all__ = ["CONFIGS", "FULL", "HALF", "LIQUID", "SOLID", "SYMMETRIC",
           "ArcMeaning", "KINDS", "conductivity", "ionic_conductivity",
           "label_arcs", "total_resistance"]

LIQUID = "liquid"
SOLID = "solid"

#: Which cell was measured.  A different question from what the electrolyte
#: was, and it changes what the arcs are.
SYMMETRIC = "sym"
FULL = "full"
HALF = "half"
CONFIGS = (SYMMETRIC, FULL, HALF)


@dataclass
class ArcMeaning:
    """One fitted resistance, named for what it is in this kind of cell."""

    parameter: str
    label: str
    note: str
    value_ohm: float
    determined: bool


#: Arc names by measurement kind, high frequency first.  The order matches the
#: order ``fit_circuit`` puts the branches in, which is why that ordering is
#: enforced there rather than left to the optimiser.
KINDS: dict[str, dict] = {
    LIQUID: {
        "label": "액체 전해질",
        "series": ("전해질 저항", "R_s — 전해질을 통한 이온 이동"),
        "arcs": [
            ("SEI 저항", "R_f — 전극 표면 필름을 통한 리튬 이동 (고주파 아크)"),
            ("전하이동 저항", "R_ct — 전자를 주고받는 반응 (저주파 아크)"),
            ("세 번째 아크", "이 회로가 무엇을 뜻하는지는 셀이 정합니다"),
        ],
        "tail": ("확산", "Warburg — 전극 내부 리튬 확산 (45° 꼬리)"),
    },
    SOLID: {
        "label": "전고체",
        "series": ("직렬 저항", "배선·접촉 저항 — 전해질 저항이 아닙니다"),
        "arcs": [
            ("고주파 아크", "이온 블로킹 대칭셀이면 벌크입니다 — 셀 구성을 정해 주세요"),
            ("저주파 아크", "이온 블로킹 대칭셀이면 입계입니다 — 셀 구성을 정해 주세요"),
            ("세 번째 아크", "전극 계면일 수 있습니다 — 셀 구성을 보고 판단합니다"),
        ],
        "tail": ("이온 블로킹", "리튬이 막혀 생기는 커패시터 거동 — 저항이 아닙니다"),
    },
}

#: What the arcs are once the **cell** is known as well as the electrolyte.
#:
#: Two arcs in a solid symmetric cell with ion-blocking electrodes are grain
#: interior and grain boundary.  The same two arcs in a solid *full* cell are
#: not: the electrodes are active, so their interfaces contribute, and the
#: second arc is at least as likely to be an interface as a boundary.  Naming
#: it "grain boundary" there and dividing a thickness by it produces an ionic
#: conductivity for something that is not ionic transport.
#:
#: So the specific names appear only where the cell earns them, and where it
#: does not the label says which question is unanswered (§0.4).
BY_CONFIG: dict[tuple[str, str], list[tuple[str, str]]] = {
    (SOLID, SYMMETRIC): [
        ("벌크 저항", "R_b — grain 내부 이온 이동 (고주파 아크)"),
        ("입계 저항", "R_gb — grain boundary 를 넘는 이동 (저주파 아크)"),
        ("세 번째 아크", "전극 계면일 수 있습니다"),
    ],
    (SOLID, FULL): [
        ("전해질 저항", "고체 전해질의 이온 이동 — 벌크와 입계가 합쳐져 보입니다"),
        ("계면 저항", "전극/전해질 계면 — 풀셀에서는 이것이 저주파 아크를 지배합니다"),
        ("세 번째 아크", "두 전극 중 어느 쪽인지는 이 측정만으로 못 가릅니다"),
    ],
    (SOLID, HALF): [
        ("전해질 저항", "고체 전해질의 이온 이동"),
        ("계면 저항", "작동 전극/전해질 계면"),
        ("세 번째 아크", "상대 전극 쪽일 수 있습니다"),
    ],
    (LIQUID, SYMMETRIC): [
        ("필름 저항", "양쪽 전극이 같으므로 한쪽 값은 절반입니다"),
        ("계면 저항", "양쪽 전극이 같으므로 한쪽 값은 절반입니다"),
        ("세 번째 아크", "셀 구성을 보고 판단합니다"),
    ],
}

#: Which (kind, config) pairs let a thickness be divided by a resistance.
#: Only the ion-blocking symmetric cell: there the arcs *are* the electrolyte,
#: end to end, which is what a conductivity means.
CONDUCTIVITY_CONFIGS = {(SOLID, SYMMETRIC)}


def label_arcs(result: FitResult, kind: str, config: str = "") -> list[ArcMeaning]:
    """Name each fitted resistance for the cell it came from.

    Resistances are taken in circuit order: the first plain ``R`` is the series
    element and the rest are arcs.  That is the same convention the guess and
    the fit use, so a circuit written any other way gets the labels its own
    order implies -- and the note says what the label rests on rather than
    asserting a physics we cannot check.

    ``config`` is what the cell was (``sym`` / ``full`` / ``half``).  Without
    it the solid-electrolyte arcs are named "high-frequency" and
    "low-frequency" and the note asks for the missing answer, because the same
    two arcs mean different things in a blocking symmetric cell and in a full
    cell.
    """
    if kind not in KINDS:
        raise ValueError(f"unknown measurement kind {kind!r}; "
                         f"known: {', '.join(sorted(KINDS))}")
    if config and config not in CONFIGS:
        raise ValueError(f"unknown cell configuration {config!r}; "
                         f"known: {', '.join(CONFIGS)}")
    scheme = dict(KINDS[kind])
    specific = BY_CONFIG.get((kind, config))
    if specific:
        scheme["arcs"] = specific
    series = _series_resistor_names(result)
    plain = [p for p in result.parameters if "_" not in p.name and p.name[0] == "R"]
    out: list[ArcMeaning] = []
    arc_index = 0
    for parameter in plain:
        if parameter.name in series:
            label, note = scheme["series"]
        else:
            names = scheme["arcs"]
            label, note = names[min(arc_index, len(names) - 1)]
            arc_index += 1
        out.append(ArcMeaning(parameter=parameter.name, label=label, note=note,
                              value_ohm=parameter.value,
                              determined=parameter.determined))
    return out


def _series_resistor_names(result: FitResult) -> set[str]:
    """Which plain resistances sit in the top-level series path.

    Structure, not position: the first version asked "does the circuit text
    start with R", and ``p(R1,CPE1)-p(R2,CPE2)-R0`` -- physically identical, a
    series resistor written last -- got its wiring resistance labelled as an
    arc and summed into the ionic conductivity (review reproduction: σ_total
    off by 8 %, R0 labelled "세 번째 아크").
    """
    try:
        parsed = parse_circuit(result.circuit)
    except CircuitError:
        text = result.circuit.strip()
        if text and text[0] == "R" and not text.startswith("p("):
            first = next((p.name for p in result.parameters
                          if "_" not in p.name and p.name[0] == "R"), None)
            return {first} if first else set()
        return set()
    return {name for name in parsed.series_element_names()
            if name and name[0] == "R" and "_" not in name}


def _has_series_element(result: FitResult) -> bool:
    return bool(_series_resistor_names(result))


def total_resistance(result: FitResult) -> float | None:
    """Every plain resistance added up -- the DC limit the arcs imply.

    ``None`` when any of them is undetermined: a total built from a number
    that was not measured is not a measurement either (§0.4).
    """
    plain = [p for p in result.parameters if "_" not in p.name and p.name[0] == "R"]
    if not plain or any(not p.determined for p in plain):
        return None
    return float(sum(p.value for p in plain))


def conductivity(resistance_ohm: float, *, thickness_cm: float | None,
                 area_cm2: float | None) -> float | None:
    """``sigma = L / (R A)`` in S/cm, or ``None`` with nothing invented.

    Both the thickness and the area are needed and neither is in the impedance
    file -- the ``.mps`` carries an "Electrode surface area" that is EC-Lab's
    default 0.001 cm² unless somebody typed the real one, so it is not a source
    we can trust for this.  Missing means missing.
    """
    if not resistance_ohm or resistance_ohm <= 0:
        return None
    if not thickness_cm or not area_cm2 or thickness_cm <= 0 or area_cm2 <= 0:
        return None
    return thickness_cm / (resistance_ohm * area_cm2)


#: 저주파 끝의 위상이 이보다 **깊으면** 블로킹이다 (순수 커패시터는 -90°).
BLOCKING_PHASE_DEG = -60.0
#: 이보다 **얕으면** 블로킹이 아니다 — 스펙트럼이 실수축 위에서 끝난다.
RESISTIVE_PHASE_DEG = -30.0


def blocking_verdict(frequency_hz, z_re, z_im, *, lowest: int = 3) -> dict:
    """이 셀이 저주파에서 **정말로 이온을 막는가** — 스펙트럼이 스스로 말한다.

    `(SOLID, SYMMETRIC)` 이라는 셀 구성만으로는 모른다.  대칭셀에는 두 종류가
    있다: SS|전해질|SS 처럼 이온을 막는 것과, Li|전해질|Li 처럼 막지 않는 것.
    전도도를 벌크·입계로 나눠 낼 수 있는 것은 **앞쪽뿐**인데, 화면의 "대칭셀"
    은 둘을 가르지 않는다.

    가르는 것은 저주파 끝의 위상이다.

    * 막으면 전류가 결국 멈추므로 커패시터처럼 보인다 — 위상이 -90° 로 가고
      ``|Z|`` 가 끝없이 커진다.
    * 안 막으면 DC 가 흐른다 — 위상이 0° 로 돌아오고 스펙트럼이 **실수축
      위에서 끝난다**.

    실측 2026-09-23 (`2600922_No1_55_sym_60um_#1_C01`): 10 mHz 에서 위상이
    약 0° 이고 ``|Z|`` 가 약 20 Ω 로 평평했다 — 맞춘 R0+R1+R2 = 21.95 Ω 과
    같다.  그런데 기본 회로 `R0-p(R1,CPE1)-p(R2,CPE2)-CPE3` 가 끝에 블로킹
    CPE 를 달고 있어서, 맞춤은 그것을 **지우는** 쪽으로 갔다 (Q=1000, n=1.00
    둘 다 경계에 붙음 — 10 mHz 에서 0.016 Ω, 전체의 0.07 %).  화면은 그것을
    "물리적 한계에 붙은 파라미터" 로만 적었고, 두 아크를 벌크·입계라 부르며
    σ 를 냈다.

    ``z_im`` 은 **물리 규약의** Im(Z) 다 (용량성이면 음수).  가장 낮은 주파수
    ``lowest`` 개의 위상 중앙값으로 본다 — 한 점은 잡음에 흔들린다.

    돌려주는 것::

        {"blocking": True | False | None, "phase_deg": float | None,
         "reason": str}

    ``None`` 은 **애매하다**는 뜻이다 (-60° 와 -30° 사이).  그때는 막는다고도
    안 막는다고도 하지 않는다 (§0.4).
    """
    frequency = np.asarray(frequency_hz, dtype=np.float64).ravel()
    real = np.asarray(z_re, dtype=np.float64).ravel()
    imag = np.asarray(z_im, dtype=np.float64).ravel()
    if not (frequency.size == real.size == imag.size) or frequency.size == 0:
        return {"blocking": None, "phase_deg": None,
                "reason": "점이 없어 저주파 끝을 볼 수 없습니다"}
    good = np.isfinite(frequency) & np.isfinite(real) & np.isfinite(imag)
    frequency, real, imag = frequency[good], real[good], imag[good]
    if frequency.size < lowest:
        return {"blocking": None, "phase_deg": None,
                "reason": f"저주파 점이 {frequency.size}개뿐이라 판단할 수 없습니다"}

    order = np.argsort(frequency)[:lowest]          # 가장 낮은 주파수부터
    phase = float(np.median(np.degrees(np.arctan2(imag[order], real[order]))))
    lowest_hz = float(frequency[order[0]])

    if phase <= BLOCKING_PHASE_DEG:
        return {"blocking": True, "phase_deg": phase,
                "reason": f"{lowest_hz:.3g} Hz 에서 위상 {phase:.0f}° — 블로킹입니다"}
    if phase >= RESISTIVE_PHASE_DEG:
        return {"blocking": False, "phase_deg": phase,
                "reason": (f"{lowest_hz:.3g} Hz 에서 위상 {phase:.0f}° — 스펙트럼이 "
                           f"실수축 위에서 끝납니다. 이 셀은 저주파에서 **이온을 "
                           f"막지 않습니다** (DC 가 흐릅니다). Li|전해질|Li 처럼 "
                           f"막지 않는 전극이거나, 막는 셀에 전자가 새는 길이 "
                           f"있습니다")}
    return {"blocking": None, "phase_deg": phase,
            "reason": (f"{lowest_hz:.3g} Hz 에서 위상 {phase:.0f}° — 블로킹인지 "
                       f"애매합니다 (더 낮은 주파수까지 재면 갈립니다)")}


def ionic_conductivity(result: FitResult, *, thickness_cm: float | None,
                       area_cm2: float | None, config: str = SYMMETRIC,
                       blocking: dict | None = None) -> dict:
    """Bulk, boundary and total ionic conductivity of a solid electrolyte.

    The total is what the lecture calls for, and it is **not** the sum of the
    two conductivities -- the two resistances are in series, so they add and
    the conductivity comes from the sum::

        sigma_total = L / ((R_bulk + R_gb) A)

    Adding sigmas instead would over-state the total by the ratio of the two
    resistances, and it is the kind of mistake that looks right.

    The series element is excluded on purpose: wiring and contact resistance
    are not ionic transport, and dividing a cell thickness by them produces a
    number with the units of a conductivity and the meaning of nothing.
    """
    series = _series_resistor_names(result)
    arcs = [meaning for meaning in label_arcs(result, SOLID, config)
            if meaning.parameter not in series]
    out: dict = {"bulk_s_cm": None, "grain_boundary_s_cm": None,
                 "total_s_cm": None, "missing": [], "excluded": []}
    if (SOLID, config) not in CONDUCTIVITY_CONFIGS:
        # 풀셀의 저주파 아크는 계면이지 전해질이 아니다.  거기에 두께를 나누면
        # 단위는 S/cm 이고 뜻은 전도도가 아니다.
        out["missing"].append("이온 블로킹 대칭셀" if config
                              else "셀 구성 (대칭셀이어야 전도도를 냅니다)")
        return out
    # **셀 구성이 대칭셀이어도 스펙트럼이 블로킹이 아니면 내지 않는다.**
    # 대칭셀에는 막는 것(SS|전해질|SS)과 안 막는 것(Li|전해질|Li)이 있는데
    # 벌크·입계로 나눌 수 있는 것은 앞쪽뿐이다.  실측 2026-09-23: 저주파
    # 위상이 0° 인 셀에서 두 아크를 벌크·입계라 부르고 σ 를 냈는데, 커패시턴스
    # 로 보면 "벌크" 는 입계 범위, "입계" 는 전극 계면 범위였다 (Irvine–Sinclair–
    # West).  모르면 내지 않는다 -- `blocking` 을 안 주면 예전처럼 셀 구성만 본다.
    if blocking is not None and blocking.get("blocking") is False:
        out["missing"].append(blocking.get("reason")
                              or "저주파에서 블로킹이 아닙니다")
        out["not_blocking"] = True
        return out
    if not thickness_cm or thickness_cm <= 0:
        out["missing"].append("두께")
    if not area_cm2 or area_cm2 <= 0:
        out["missing"].append("면적")
    if not arcs:
        out["missing"].append("아크")
    if out["missing"]:
        return out
    if not all(meaning.determined for meaning in arcs):
        out["missing"].append("결정되지 않은 저항")
        return out

    # 전해질은 벌크와 입계, 두 아크다.  세 번째 아크는 자기 라벨부터
    # "전극 계면일 수 있습니다" 인데 σ 합계에 넣으면 전해질 전도도가 그만큼
    # 과소평가된다 -- 리뷰 재현에서 100 Ω 계면 아크 하나가 σ_total 을 2.7배
    # 깎았다, 아무 표시 없이.  넣지 않고, 뺐다는 사실을 함께 낸다.
    electrolyte = arcs[:2]
    out["excluded"] = [f"{meaning.parameter} ({meaning.label}, "
                       f"{meaning.value_ohm:.4g} Ω)" for meaning in arcs[2:]]
    for key, meaning in zip(("bulk_s_cm", "grain_boundary_s_cm"), electrolyte,
                            strict=False):
        out[key] = conductivity(meaning.value_ohm, thickness_cm=thickness_cm,
                                area_cm2=area_cm2)
    total_ohm = sum(meaning.value_ohm for meaning in electrolyte)
    out["total_s_cm"] = conductivity(total_ohm, thickness_cm=thickness_cm,
                                     area_cm2=area_cm2)
    out["total_ohm"] = total_ohm
    return out


