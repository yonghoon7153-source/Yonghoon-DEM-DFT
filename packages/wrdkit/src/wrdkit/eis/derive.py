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

from .fit import FitResult

__all__ = ["LIQUID", "SOLID", "ArcMeaning", "KINDS", "conductivity",
           "ionic_conductivity", "label_arcs", "total_resistance"]

LIQUID = "liquid"
SOLID = "solid"


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
            ("벌크 저항", "R_b — grain 내부 이온 이동 (고주파 아크)"),
            ("입계 저항", "R_gb — grain boundary 를 넘는 이동 (저주파 아크)"),
            ("세 번째 아크", "전극 계면일 수 있습니다 — 셀 구성을 보고 판단합니다"),
        ],
        "tail": ("이온 블로킹", "리튬이 막혀 생기는 커패시터 거동 — 저항이 아닙니다"),
    },
}


def label_arcs(result: FitResult, kind: str) -> list[ArcMeaning]:
    """Name each fitted resistance for the cell it came from.

    Resistances are taken in circuit order: the first plain ``R`` is the series
    element and the rest are arcs.  That is the same convention the guess and
    the fit use, so a circuit written any other way gets the labels its own
    order implies -- and the note says what the label rests on rather than
    asserting a physics we cannot check.
    """
    if kind not in KINDS:
        raise ValueError(f"unknown measurement kind {kind!r}; "
                         f"known: {', '.join(sorted(KINDS))}")
    scheme = KINDS[kind]
    plain = [p for p in result.parameters if "_" not in p.name and p.name[0] == "R"]
    out: list[ArcMeaning] = []
    for i, parameter in enumerate(plain):
        if i == 0 and _has_series_element(result):
            label, note = scheme["series"]
        else:
            arc_index = i - 1 if _has_series_element(result) else i
            names = scheme["arcs"]
            label, note = names[min(arc_index, len(names) - 1)]
        out.append(ArcMeaning(parameter=parameter.name, label=label, note=note,
                              value_ohm=parameter.value,
                              determined=parameter.determined))
    return out


def _has_series_element(result: FitResult) -> bool:
    """Whether the circuit starts with a bare resistance.

    ``R0-p(R1,CPE1)`` does; ``p(R1,CPE1)-p(R2,CPE2)`` does not, and in that one
    the first resistance is an arc, not a series term.  Read from the circuit
    text because that is what the person wrote.
    """
    text = result.circuit.strip()
    return bool(text) and text[0] == "R" and not text.startswith("p(")


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


def ionic_conductivity(result: FitResult, *, thickness_cm: float | None,
                       area_cm2: float | None) -> dict:
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
    arcs = [meaning for meaning in label_arcs(result, SOLID)
            if meaning.parameter != _series_name(result)]
    out: dict = {"bulk_s_cm": None, "grain_boundary_s_cm": None,
                 "total_s_cm": None, "missing": []}
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

    for key, meaning in zip(("bulk_s_cm", "grain_boundary_s_cm"), arcs,
                            strict=False):
        out[key] = conductivity(meaning.value_ohm, thickness_cm=thickness_cm,
                                area_cm2=area_cm2)
    total_ohm = sum(meaning.value_ohm for meaning in arcs)
    out["total_s_cm"] = conductivity(total_ohm, thickness_cm=thickness_cm,
                                     area_cm2=area_cm2)
    out["total_ohm"] = total_ohm
    return out


def _series_name(result: FitResult) -> str | None:
    if not _has_series_element(result):
        return None
    for parameter in result.parameters:
        if "_" not in parameter.name and parameter.name[0] == "R":
            return parameter.name
    return None
