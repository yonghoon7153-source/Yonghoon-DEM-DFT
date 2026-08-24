"""Equivalent circuits, written the way people say them out loud.

``R0-p(R1,CPE1)-p(R2,CPE2)`` is a series resistance followed by two arcs.  The
notation is the one ``impedance.py`` uses, so a circuit copied out of a paper
or a colleague's script means here what it meant there: ``-`` puts elements in
series, ``p(a,b,...)`` puts them in parallel.

Elements carry their own parameter count and their own physical bounds.  That
matters more than it looks: a CPE exponent above 1 is not a slightly odd
capacitor, it is an inductor wearing a capacitor's name, and a fitter allowed
to go there will happily "fit" a spectrum with a shape it cannot have.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import numpy as np

__all__ = ["Circuit", "Element", "ELEMENTS", "parse_circuit", "CircuitError"]


class CircuitError(ValueError):
    """A circuit string that cannot be read, or names an unknown element."""


@dataclass(frozen=True)
class Element:
    """One circuit element: how many numbers it takes and what they mean."""

    kind: str
    #: Suffixes appended to the instance name, in order.  A single-parameter
    #: element uses the bare name (``R1``), not ``R1_R``.
    suffixes: tuple[str, ...]
    #: ``(low, high)`` per parameter.  Physical, not numerical: these are the
    #: values the element can actually take, so a fit that leaves the range has
    #: stopped describing a circuit.
    bounds: tuple[tuple[float, float], ...]
    #: Units, for the screen.
    units: tuple[str, ...]
    description: str

    @property
    def size(self) -> int:
        return len(self.suffixes)

    def impedance(self, values: np.ndarray, omega: np.ndarray) -> np.ndarray:
        raise NotImplementedError


class _R(Element):
    def impedance(self, values, omega):
        return np.full(omega.shape, values[0], dtype=complex)


class _C(Element):
    def impedance(self, values, omega):
        return 1.0 / (1j * omega * values[0])


class _L(Element):
    def impedance(self, values, omega):
        return 1j * omega * values[0]


class _CPE(Element):
    """``Z = 1 / (Q (jw)^n)``.

    ``n = 1`` is an ideal capacitor with ``C = Q``; below that the arc is
    depressed, which is what a porous or rough electrode does.  The procedure
    sheet calls these CPE-T and CPE-P.
    """

    def impedance(self, values, omega):
        q, n = values
        return 1.0 / (q * (1j * omega) ** n)


class _W(Element):
    """Semi-infinite Warburg: the 45-degree tail.  ``Z = s (1-j) / sqrt(w)``."""

    def impedance(self, values, omega):
        return values[0] * (1 - 1j) / np.sqrt(omega)


class _Ws(Element):
    """Finite-length Warburg, transmissive ("short") boundary.

    ``Z = R tanh(sqrt(j w T)) / sqrt(j w T)`` -- the 45-degree line that bends
    back to the real axis, which is what a thin diffusion layer gives.
    """

    def impedance(self, values, omega):
        r, tau = values
        x = np.sqrt(1j * omega * tau)
        return r * np.tanh(x) / x


class _Wo(Element):
    """Finite-length Warburg, reflective ("open") boundary.

    ``Z = R coth(sqrt(j w T)) / sqrt(j w T)``.  It differs from ``Ws`` only in
    that ``coth`` where ``Ws`` has ``tanh``, and they mean opposite physics --
    a blocked boundary that turns capacitive at low frequency versus a
    transmissive one that returns to the real axis.  Written next to each other
    so the inversion is visible rather than buried.
    """

    def impedance(self, values, omega):
        r, tau = values
        x = np.sqrt(1j * omega * tau)
        return r / (x * np.tanh(x))


#: Registry.  Bounds are physical claims, so they are written down once here
#: rather than passed in at each call site where they could drift apart.
ELEMENTS: dict[str, Element] = {
    "R": _R("R", ("",), ((1e-9, 1e9),), ("Ω",), "저항"),
    "C": _C("C", ("",), ((1e-15, 1e3),), ("F",), "커패시터"),
    "L": _L("L", ("",), ((1e-12, 1e3),), ("H",), "인덕터 (고주파 배선)"),
    "CPE": _CPE("CPE", ("_Q", "_n"), ((1e-15, 1e3), (0.3, 1.0)), ("S·sⁿ", ""),
                "상수위상소자 — 찌그러진 반원"),
    "W": _W("W", ("",), ((1e-9, 1e9),), ("Ω·s^-½",), "확산 (45° 꼬리)"),
    "Ws": _Ws("Ws", ("_R", "_tau"), ((1e-9, 1e9), (1e-6, 1e6)), ("Ω", "s"),
              "유한 확산 (짧은 경계)"),
    "Wo": _Wo("Wo", ("_R", "_tau"), ((1e-9, 1e9), (1e-6, 1e6)), ("Ω", "s"),
              "유한 확산 (열린 경계)"),
}


# --- the little language ---------------------------------------------------

_NAME = re.compile(r"^([A-Za-z]+)\d*$")


@dataclass(frozen=True)
class _Series:
    parts: tuple


@dataclass(frozen=True)
class _Parallel:
    parts: tuple


@dataclass(frozen=True)
class _Leaf:
    name: str
    kind: str


def _split_top(text: str, separator: str) -> list[str]:
    """Split on *separator*, ignoring anything inside brackets."""
    out, depth, current = [], 0, []
    for char in text:
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth < 0:
                raise CircuitError(f"unbalanced ')' in {text!r}")
        if char == separator and depth == 0:
            out.append("".join(current))
            current = []
        else:
            current.append(char)
    if depth:
        raise CircuitError(f"unbalanced '(' in {text!r}")
    out.append("".join(current))
    return out


def _node(text: str):
    text = text.strip()
    if not text:
        raise CircuitError("empty element in the circuit")
    parts = _split_top(text, "-")
    if len(parts) > 1:
        return _Series(tuple(_node(part) for part in parts))
    if text.startswith("p(") and text.endswith(")"):
        inner = text[2:-1]
        members = _split_top(inner, ",")
        if len(members) < 2:
            raise CircuitError("p(...) needs at least two elements")
        return _Parallel(tuple(_node(member) for member in members))
    match = _NAME.match(text)
    if not match:
        raise CircuitError(f"{text!r} is not an element name")
    kind = match.group(1)
    if kind not in ELEMENTS:
        raise CircuitError(
            f"unknown element {kind!r}; known: " + ", ".join(sorted(ELEMENTS)))
    return _Leaf(text, kind)


@dataclass(frozen=True)
class Circuit:
    """A parsed circuit: names its parameters and evaluates its impedance."""

    text: str
    _root: object
    parameter_names: tuple[str, ...]
    parameter_units: tuple[str, ...]
    lower: np.ndarray
    upper: np.ndarray

    def impedance(self, values, frequency_hz) -> np.ndarray:
        values = np.asarray(values, dtype=float)
        if len(values) != len(self.parameter_names):
            raise CircuitError(
                f"{self.text} takes {len(self.parameter_names)} parameters, "
                f"got {len(values)}")
        omega = 2 * np.pi * np.asarray(frequency_hz, dtype=float)
        taken = {"i": 0}

        def walk(node) -> np.ndarray:
            if isinstance(node, _Leaf):
                element = ELEMENTS[node.kind]
                start = taken["i"]
                taken["i"] += element.size
                return element.impedance(values[start:start + element.size], omega)
            if isinstance(node, _Series):
                total = np.zeros(omega.shape, dtype=complex)
                for part in node.parts:
                    total = total + walk(part)
                return total
            admittance = np.zeros(omega.shape, dtype=complex)
            for part in node.parts:
                admittance = admittance + 1.0 / walk(part)
            return 1.0 / admittance

        return walk(self._root)

    def element_names(self) -> list[str]:
        """Instance names in evaluation order -- ``['R0', 'R1', 'CPE1']``."""
        names: list[str] = []

        def walk(node):
            if isinstance(node, _Leaf):
                names.append(node.name)
                return
            for part in node.parts:
                walk(part)

        walk(self._root)
        return names


def parse_circuit(text: str) -> Circuit:
    """Read a circuit string.  Raises ``CircuitError`` rather than guessing."""
    root = _node(text)
    names: list[str] = []
    units: list[str] = []
    lower: list[float] = []
    upper: list[float] = []

    def walk(node):
        if isinstance(node, _Leaf):
            element = ELEMENTS[node.kind]
            for suffix, unit, (low, high) in zip(element.suffixes, element.units,
                                                 element.bounds, strict=True):
                names.append(node.name + suffix)
                units.append(unit)
                lower.append(low)
                upper.append(high)
            return
        for part in node.parts:
            walk(part)

    walk(root)
    seen = [name for name in names if names.count(name) > 1]
    if seen:
        raise CircuitError(
            "two elements share the name " + sorted(set(seen))[0]
            + " -- give them different numbers")
    return Circuit(text=text.strip(), _root=root,
                   parameter_names=tuple(names), parameter_units=tuple(units),
                   lower=np.array(lower), upper=np.array(upper))
