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


def _coth(x: np.ndarray) -> np.ndarray:
    """``coth`` that does not overflow.

    ``sinh``/``cosh`` overflow above |x| ~ 710 and lose the answer well before
    that, but ``coth(x) -> ±1`` as ``Re x -> ±inf``.  Cutting over at 30 is exact
    to double precision (``|coth(30)| - 1 < 1e-26``) and keeps the high-frequency
    end of a transmission line finite instead of NaN.

    부호를 ``Re x`` 에서 가져온다.  이 파일의 호출자들은 실수부가 양수인 ``x``
    만 넘기지만, 절댓값으로 자르고 +1 을 돌려주면 음의 실수부에서 **부호가
    뒤집힌 답**이 나온다 -- 새 원소가 하나 붙는 날 조용히 틀리는 종류다.
    """
    out = np.where(x.real < 0, -1.0, 1.0).astype(complex)
    near = np.abs(x.real) < 30
    out[near] = np.cosh(x[near]) / np.sinh(x[near])
    return out


def _over_sinh(x: np.ndarray) -> np.ndarray:
    """``1/sinh(x)``, which is 0 for large ``Re x`` rather than an overflow."""
    out = np.zeros_like(x)
    near = np.abs(x.real) < 30
    out[near] = 1.0 / np.sinh(x[near])
    return out


def transmission_line(r_ion: float, r_electron: float,
                      interfacial: np.ndarray) -> np.ndarray:
    """Bisquert's general transmission line — two rails and what joins them.

    A composite electrode is not a surface.  Ions travel through the pore
    network (``r_ion``) and electrons through the solid (``r_electron``), and
    the reaction happens *along the way*, distributed over the thickness.  The
    45-degree stub at high frequency and the ``R_ion/3`` offset at low
    frequency both come out of this geometry -- an R-CPE circuit can only
    imitate them with numbers that mean nothing.

    Rails are given as **totals** (Ω), which is the same as PyEIS's per-length
    values with the thickness set to 1: only the products enter the formula, and
    a separate thickness parameter would be one more number the spectrum cannot
    determine.

    **두 레일은 서로 바꿔도 같은 곡선이다.**  식에 들어가는 것은 두 값의 합과
    곱과 제곱합뿐이라 ``r_ion`` 과 ``r_electron`` 을 맞바꾸면 임피던스가 **정확히**
    같다 (합성 스펙트럼에서 차이 0.0).  그래서 한 스펙트럼은 둘의 **짝**만
    정하고 어느 쪽이 이온인지는 말하지 않는다 -- 피팅이 그 사실을 `reason` 에
    적는다.  물리로 가르려면 전자 전도도를 따로 재거나 블로킹 셀이 있어야 한다.

    Ref.: Bisquert, J. Phys. Chem. B 104 (2000) 2287; de Levie (1973).
    Cross-checked term by term against PyEIS 1.0.10 ``cir_RsTL``.
    """
    total = r_ion + r_electron
    lam = np.sqrt(interfacial / total)
    x = 1.0 / lam
    joint = (r_electron * r_ion) / total
    rails = (r_electron ** 2 + r_ion ** 2) / total
    return joint * (1.0 + 2.0 * lam * _over_sinh(x)) + lam * rails * _coth(x)


class _TLR(Element):
    """전송선 — 계면이 ``Rct ∥ CPE`` 인 것.  확산 꼬리가 안 보일 때.

    이온 레일(``Ri``)·전자 레일(``Re``)과 그 사이의 계면 임피던스.  전고체
    복합전극처럼 반응이 두께 전체에 퍼져 있는 전극의 모양이다.
    """

    def impedance(self, values, omega):
        r_ion, r_electron, rct, q, n = values
        z_cpe = 1.0 / (q * (1j * omega) ** n)
        interfacial = 1.0 / (1.0 / z_cpe + 1.0 / rct)
        return transmission_line(r_ion, r_electron, interfacial)


class _TL(Element):
    """전송선 — 계면이 ``CPE ∥ (Rct + 유한확산 W)`` 인 것.

    PyEIS 의 ``cir_RsTL_1Dsolid`` 와 같은 계면 구성이다: 전하이동 저항과 유한
    공간 Warburg 가 **직렬**이고, 그 둘에 CPE 가 **병렬**이다.  Warburg 는
    ``Z = Wr·coth(x)/x``, ``x = (Wt·jω)^Wn`` -- 이상적인 1D 확산이면
    ``Wn = 0.5`` 이고, 그보다 낮으면 입자 크기가 고르지 않다는 뜻이다.

    **``Wn`` 의 상한이 0.8 인 것은 취향이 아니라 극점 때문이다.**  ``coth`` 는
    허수축의 ``b = kπ`` 마다 극점을 가지고, ``|coth(a+jb)| <= coth(a)`` 이므로
    실수부 ``a`` 가 1 보다 크면 그 근처에서도 1.31 을 넘지 않는다.  여기서는

        Im x / Re x = tan(Wn·π/2)

    이라, ``tan(Wn·π/2) < π`` 이면 ``Im x`` 가 π 를 넘는 순간 ``Re x`` 도 1 을
    넘는다 -- 즉 극점에 닿을 수 없다.  그 경계가 ``Wn = 2·atan(π)/π = 0.8038``
    이다.

    상한이 1.0 이었을 때 실제로 일어난 일: ``Wn = 1`` 이면 ``x`` 가 **순허수**가
    되어 (``Re x = 0``) ``coth(jb) = -j·cot(b)`` 가 되고, 이것은 확산 임피던스가
    아니라 **무손실 선로**다.  주파수 점 사이에서 극점을 오가며 값이 튀는데,
    적합도로는 그것이 이득이라 최적화가 상한에 눌러붙었다.  랩의 전고체 풀셀
    스펙트럼에서 나이퀴스트 곡선이 저주파에서 톱니로 꺾인 것이 그 자국이다
    (톱니 지표 15.6 vs 매끄러운 곡선의 1.0).  ``Wn <= 0.8`` 에서는 1.03 이다.

    랩의 PyEIS 피팅이 실제로 낸 값도 0.75 로, 이 상한 안에 있다.
    """

    def impedance(self, values, omega):
        r_ion, r_electron, rct, q, n, w_r, w_n, w_tau = values
        x = (w_tau * 1j * omega) ** w_n
        z_w = w_r * _coth(x) / x
        z_cpe = 1.0 / (q * (1j * omega) ** n)
        interfacial = 1.0 / (1.0 / z_cpe + 1.0 / (rct + z_w))
        return transmission_line(r_ion, r_electron, interfacial)


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
    "TLR": _TLR("TLR", ("_Ri", "_Re", "_Rct", "_Q", "_n"),
                ((1e-9, 1e9), (1e-9, 1e9), (1e-9, 1e9), (1e-15, 1e3), (0.3, 1.0)),
                ("Ω", "Ω", "Ω", "S·sⁿ", ""),
                "전송선 — 이온·전자 레일 + 계면 (Rct∥CPE)"),
    # `_Wn` 의 상한이 1.0 이 아니라 0.8 인 이유는 `_TL` 의 docstring 에 있다:
    # 그 위는 확산이 아니라 극점이 늘어선 무손실 선로다.
    "TL": _TL("TL", ("_Ri", "_Re", "_Rct", "_Q", "_n", "_Wr", "_Wn", "_Wt"),
              ((1e-9, 1e9), (1e-9, 1e9), (1e-9, 1e9), (1e-15, 1e3), (0.3, 1.0),
               (1e-9, 1e9), (0.1, 0.8), (1e-6, 1e6)),
              ("Ω", "Ω", "Ω", "S·sⁿ", "", "Ω", "", "s"),
              "전송선 — 계면에 유한 확산까지 (CPE∥(Rct+W))"),
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

    def parallel_rc_branches(self) -> list[tuple[str, str]]:
        """(R 이름, CPE 이름) — ``p(...)`` 블록 안에서 실제로 짝인 것들.

        분기 정렬이 이것을 쓴다.  "CPE 바로 앞의 맨 R" 같은 **이름 순서**로
        짝을 찾으면 ``p(CPE1,R1)`` 처럼 논문에서 베낀 표기(우리 파서가 허용
        한다)에서 CPE1 이 직렬저항 R0 와 짝지어져, 직렬저항 값이 아크 슬롯과
        맞바꿔진 채 보고된다 — 리뷰 재현에서 R0=5 가 40 으로 나왔다.  짝은
        괄호가 정의하므로 괄호에서 읽는다.
        """
        out: list[tuple[str, str]] = []

        def walk(node) -> None:
            if isinstance(node, _Leaf):
                return
            if isinstance(node, _Parallel):
                leaves = [part for part in node.parts if isinstance(part, _Leaf)]
                resistors = [leaf.name for leaf in leaves if leaf.kind == "R"]
                cpes = [leaf.name for leaf in leaves if leaf.kind == "CPE"]
                if len(resistors) == 1 and len(cpes) == 1:
                    out.append((resistors[0], cpes[0]))
            for part in getattr(node, "parts", ()):
                walk(part)

        walk(self._root)
        return out

    def series_element_names(self) -> list[str]:
        """최상위 직렬 경로에 그대로 놓인 소자들의 이름.

        "회로 문자열이 R 로 시작하는가" 는 위치 휴리스틱이고,
        ``p(R1,CPE1)-p(R2,CPE2)-R0`` 처럼 직렬 R 을 뒤에 쓴 (물리적으로 동일한)
        회로에서 틀린다.  직렬인지 아닌지는 구조가 정한다.
        """
        if isinstance(self._root, _Leaf):
            return [self._root.name]
        if isinstance(self._root, _Series):
            return [part.name for part in self._root.parts
                    if isinstance(part, _Leaf)]
        return []

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


def series_blocks(circuit: Circuit) -> list[tuple[str, tuple[int, ...]]]:
    """Top-level series parts, in written order, with the parameters each owns.

    ``R0-p(R1,CPE1)-Ws1`` gives three blocks: ``R0`` with one parameter,
    ``p(R1,CPE1)`` with three, ``Ws1`` with two.  A circuit that is not a
    series at the top (one element, or a single parallel block) gives one.

    The order matters and it is not arbitrary.  Impedance circuits are written
    high frequency first -- the series resistance, then the fast arc, then the
    slow one, then whatever diffuses -- because that is the order the features
    appear in as the sweep comes down.  Staged fitting walks these blocks in
    that order, and a circuit written backwards would simply stage backwards;
    nothing here enforces the convention, it only follows what was written.
    """
    root = circuit._root
    parts = root.parts if isinstance(root, _Series) else (root,)

    sizes: list[int] = []
    for part in parts:
        count = 0

        def walk(node):
            nonlocal count
            if isinstance(node, _Leaf):
                count += ELEMENTS[node.kind].size
                return
            for child in node.parts:
                walk(child)

        walk(part)
        sizes.append(count)

    out: list[tuple[str, tuple[int, ...]]] = []
    at = 0
    for size in sizes:
        names = circuit.parameter_names[at:at + size]
        # 이름표는 사람이 읽는 것뿐이다 -- 한 원소면 그 이름, 여러 개면
        # 접미사를 뗀 이름들을 모은다 (`p(R1,CPE1)` -> "R1+CPE1").
        label = "+".join(dict.fromkeys(
            name.split("_")[0] for name in names))
        out.append((label, tuple(range(at, at + size))))
        at += size
    return out


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
