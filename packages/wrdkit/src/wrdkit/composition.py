"""Electrode composition: what the film is made of, and how much of it counts.

A dry-processed cathode is a blend -- active material, solid electrolyte, a
conductive additive, a binder -- and only the active fraction belongs in the
denominator of mAh/g.  That fraction is the single most error-prone number in
the whole pipeline: it lives in a lab notebook, changes between batches, and
is written down in half a dozen shorthands.

So this module accepts the shorthands people actually use::

    "80:17:3"                       -> AM 80, SE 17, conductive 3
    "AM:SE:VGCF = 80:17:3"
    "NCM811:LPSCl:VGCF:PTFE 78:17:3:2"
    "AM 80 / SE 17 / VGCF 3"

and turns them into components with roles, one of which is active.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

__all__ = ["Component", "Composition", "Role", "PRESETS", "parse_composition"]


class Role:
    """What a component does in the electrode."""

    ACTIVE = "active"
    ELECTROLYTE = "electrolyte"
    CONDUCTIVE = "conductive"
    BINDER = "binder"
    OTHER = "other"

    ALL = (ACTIVE, ELECTROLYTE, CONDUCTIVE, BINDER, OTHER)


#: Substances whose role is unambiguous, so a bare name gets classified.
#: Matched case-insensitively; see :func:`_hint_matches` for how.
_ROLE_HINTS: tuple[tuple[str, str], ...] = (
    # active materials
    ("ncm", Role.ACTIVE), ("nmc", Role.ACTIVE), ("nca", Role.ACTIVE),
    ("lco", Role.ACTIVE), ("lfp", Role.ACTIVE), ("lmo", Role.ACTIVE),
    ("lmr", Role.ACTIVE), ("lni", Role.ACTIVE), ("graphite", Role.ACTIVE),
    ("silicon", Role.ACTIVE), ("sio", Role.ACTIVE), ("am", Role.ACTIVE),
    ("cam", Role.ACTIVE),
    # solid / liquid electrolytes and their common names
    ("lpscl", Role.ELECTROLYTE), ("li6ps5cl", Role.ELECTROLYTE),
    ("li3ps4", Role.ELECTROLYTE), ("argyrodite", Role.ELECTROLYTE),
    ("llzo", Role.ELECTROLYTE), ("latp", Role.ELECTROLYTE),
    ("lgps", Role.ELECTROLYTE), ("se", Role.ELECTROLYTE),
    ("electrolyte", Role.ELECTROLYTE),
    # conductive additives
    ("vgcf", Role.CONDUCTIVE), ("super p", Role.CONDUCTIVE),
    ("superp", Role.CONDUCTIVE), ("super-p", Role.CONDUCTIVE),
    ("ketjen", Role.CONDUCTIVE), ("cnt", Role.CONDUCTIVE),
    ("carbon black", Role.CONDUCTIVE), ("acetylene", Role.CONDUCTIVE),
    ("cb", Role.CONDUCTIVE), ("cnf", Role.CONDUCTIVE),
    # binders
    ("ptfe", Role.BINDER), ("pvdf", Role.BINDER), ("nbr", Role.BINDER),
    ("sbr", Role.BINDER), ("cmc", Role.BINDER), ("binder", Role.BINDER),
    ("paa", Role.BINDER),
)


_TOKENS = re.compile(r"[^a-z0-9]+")


def _hint_matches(needle: str, lowered: str, tokens: list[str]) -> bool:
    """Is *needle* really this substance, or only buried inside another word?

    Short acronyms are the trap.  A bare substring test makes ``am`` fire
    inside "cer-am-ic", "amorphous" and "foam", so "LPS glass-ceramic" comes
    back as active material and joins the mAh/g denominator with no warning --
    the exact silent corruption ADR 0007 forbids.  So a one-word hint has to
    be a whole token, optionally followed by digits, because "NCM811" and
    "SiO2" are the same substance as "NCM" and "SiO".  Hints that already
    contain a space or hyphen ("super p", "carbon black") are long enough to
    be unambiguous and stay substring matches.
    """
    if _TOKENS.search(needle):
        return needle in lowered
    for token in tokens:
        if token == needle or (token.startswith(needle)
                               and token[len(needle):].isdigit()):
            return True
    return False


def infer_role(name: str) -> str:
    """Classify a component from its name, defaulting to ``other``.

    The default matters: an unrecognised name must not silently become active
    material, because that would put it in the mAh/g denominator.
    """
    lowered = name.strip().lower()
    tokens = [t for t in _TOKENS.split(lowered) if t]
    for needle, role in _ROLE_HINTS:
        if _hint_matches(needle, lowered, tokens):
            return role
    return Role.OTHER


@dataclass
class Component:
    """One ingredient and its weight fraction of the electrode film."""

    name: str
    wt_percent: float
    role: str = Role.OTHER

    def __post_init__(self) -> None:
        if self.role not in Role.ALL:
            self.role = infer_role(self.name)


@dataclass
class Composition:
    """The blend, as weight percentages of the whole electrode film."""

    components: list[Component] = field(default_factory=list)

    # -- derived ------------------------------------------------------------
    @property
    def total_wt_percent(self) -> float:
        return sum(c.wt_percent for c in self.components)

    @property
    def active_wt_percent(self) -> float | None:
        """Combined weight percent of everything marked active.

        ``None`` when nothing is marked active -- the caller must not guess.
        """
        active = [c for c in self.components if c.role == Role.ACTIVE]
        if not active:
            return None
        return sum(c.wt_percent for c in active)

    @property
    def active_names(self) -> list[str]:
        return [c.name for c in self.components if c.role == Role.ACTIVE]

    @property
    def present(self) -> list[Component]:
        """Components actually in the film.

        A 0 wt% entry is meaningful metadata -- "this batch had no PTFE" is a
        deliberate record, not a blank -- so it is kept in the composition and
        only filtered out for compact display.
        """
        return [c for c in self.components if c.wt_percent > 0]

    @property
    def absent(self) -> list[Component]:
        """Components recorded at 0 wt%, i.e. deliberately left out."""
        return [c for c in self.components if c.wt_percent <= 0]

    def is_empty(self) -> bool:
        return not self.components

    # -- quality ------------------------------------------------------------
    def problems(self) -> list[str]:
        """Reasons this composition should not be trusted, in plain words.

        A component at 0 wt% is not a problem: a binder-free or additive-free
        electrode is a normal thing to record.
        """
        issues: list[str] = []
        if not self.components:
            return issues
        total = self.total_wt_percent
        if abs(total - 100.0) > 0.5:
            issues.append(f"weight percentages add up to {total:g}, not 100")
        if any(c.wt_percent < 0 for c in self.components):
            issues.append("a component has a negative weight percent")
        if self.active_wt_percent is None:
            issues.append("no component is marked as the active material")
        elif self.active_wt_percent <= 0:
            issues.append("the active material is 0 wt%")
        names = [c.name.strip().lower() for c in self.components]
        if len(names) != len(set(names)):
            issues.append("a component name is repeated")
        return issues

    def normalized(self) -> Composition:
        """Rescale to 100 % -- for when a notebook records parts, not percent.

        Zero-weight components stay at zero and stay in the list.
        """
        total = self.total_wt_percent
        if total <= 0:
            return Composition(list(self.components))
        return Composition([
            Component(c.name, c.wt_percent * 100.0 / total, c.role)
            for c in self.components
        ])

    # -- text ---------------------------------------------------------------
    def label(self, *, with_names: bool = True, skip_zero: bool = False) -> str:
        """``NCM811:LPSCl:VGCF = 80:17:3`` -- how a lab actually says it.

        ``skip_zero`` drops components recorded at 0 wt%, for places where the
        blend is shown in one line and "PTFE 0" would only add noise.
        """
        components = self.present if skip_zero else self.components
        if not components:
            return ""
        ratios = ":".join(_trim(c.wt_percent) for c in components)
        if not with_names:
            return ratios
        names = ":".join(c.name for c in components)
        return f"{names} = {ratios}"

    def to_json(self) -> list[dict]:
        return [asdict(c) for c in self.components]

    @classmethod
    def from_json(cls, payload) -> Composition:
        if not payload:
            return cls()
        components = []
        for entry in payload:
            if not isinstance(entry, dict):
                continue
            name = str(entry.get("name", "")).strip()
            if not name:
                continue
            try:
                wt = float(entry.get("wt_percent", 0) or 0)
            except (TypeError, ValueError):
                continue
            role = entry.get("role") or infer_role(name)
            components.append(Component(name, wt, role))
        return cls(components)


def _trim(value: float) -> str:
    """Render 80.0 as ``80`` but 17.5 as ``17.5``."""
    return f"{value:g}"


# ``AM:SE:VGCF = 80:17:3`` and its relatives.
_NAMES_THEN_RATIOS = re.compile(
    r"^\s*([A-Za-z0-9가-힣][^=]*?)\s*[=:]?\s*"
    r"((?:\d+(?:\.\d+)?\s*:\s*)+\d+(?:\.\d+)?)\s*%?\s*$"
)
# ``AM 80 / SE 17 / VGCF 3`` and ``AM 80, SE 17``.
_PAIRS = re.compile(r"([A-Za-z0-9가-힣][A-Za-z0-9가-힣 _\-+.]*?)\s*[: ]\s*(\d+(?:\.\d+)?)\s*%?")
#: A component name has to contain a letter -- "80" is a ratio, not a substance.
_HAS_LETTER = re.compile(r"[A-Za-z가-힣]")

#: Default names when only a ratio is given.  Order follows how the blend is
#: written in practice: active first, then electrolyte, conductive, binder.
_POSITIONAL = ("AM", "SE", "VGCF", "Binder", "Other")


def parse_composition(text: str) -> Composition:
    """Read a composition from the shorthand a researcher would type.

    Understands ``80:17:3``, ``AM:SE:VGCF = 80:17:3``,
    ``NCM811:LPSCl:VGCF:PTFE 78:17:3:2`` and ``AM 80 / SE 17 / VGCF 3``.
    Returns an empty :class:`Composition` when nothing can be read, rather
    than guessing.
    """
    text = (text or "").strip()
    if not text:
        return Composition()

    # Bare ratio: 80:17:3
    if re.fullmatch(r"\s*(?:\d+(?:\.\d+)?\s*:\s*)+\d+(?:\.\d+)?\s*%?\s*", text):
        ratios = [float(v) for v in re.split(r"\s*:\s*", text.strip().rstrip("%").strip())]
        return _positional(ratios)

    match = _NAMES_THEN_RATIOS.match(text)
    if match:
        names = [n.strip() for n in re.split(r"\s*[:/]\s*", match.group(1)) if n.strip()]
        ratios = [float(v) for v in re.split(r"\s*:\s*", match.group(2))]
        if len(names) == len(ratios):
            return Composition([
                Component(name, ratio, infer_role(name))
                for name, ratio in zip(names, ratios, strict=True)
            ])
        if len(names) == 1 and len(ratios) > 1:
            # "cathode = 80:17:3" -- one label for the whole blend.
            return _positional(ratios)
        # Names and ratios in unequal numbers means a typo ("AM:SE:VGCF =
        # 80:17").  Falling through would let the pair reader carve a
        # component out of the ratio digits themselves; an empty composition
        # is the honest answer.
        return Composition()

    pairs = [(name.strip(), value) for name, value in _PAIRS.findall(text)
             if _HAS_LETTER.search(name)]
    # A blend has at least two ingredients.  A lone "word number" is far more
    # often a sample label ("cell 01") than a composition, and inventing a
    # component from it would persist a number nobody entered.
    if len(pairs) >= 2:
        return Composition([
            Component(name, float(value), infer_role(name))
            for name, value in pairs
        ])

    return Composition()


def _positional(ratios: list[float]) -> Composition:
    components = []
    for index, ratio in enumerate(ratios):
        name = _POSITIONAL[index] if index < len(_POSITIONAL) else f"Component {index + 1}"
        components.append(Component(name, ratio, infer_role(name)))
    return Composition(components)


#: Formulations common enough to be worth one click.  Editable afterwards.
PRESETS: tuple[dict, ...] = (
    {
        "label": "건식 ASSB · AM:SE:VGCF = 80:17:3",
        "text": "AM:SE:VGCF = 80:17:3",
    },
    {
        "label": "건식 ASSB · AM:SE:VGCF:PTFE = 78:17:3:2",
        "text": "AM:SE:VGCF:PTFE = 78:17:3:2",
    },
    {
        "label": "건식 ASSB · AM:SE:VGCF:PTFE = 80:15:3:2",
        "text": "AM:SE:VGCF:PTFE = 80:15:3:2",
    },
    {
        "label": "ASSB · AM:SE:Super P = 70:27:3",
        "text": "AM:SE:Super P = 70:27:3",
    },
    {
        "label": "ASSB · AM:SE = 70:30",
        "text": "AM:SE = 70:30",
    },
    {
        "label": "습식 슬러리 · AM:Super P:PVDF = 90:5:5",
        "text": "AM:Super P:PVDF = 90:5:5",
    },
    {
        "label": "습식 슬러리 · AM:Super P:PVDF = 96:2:2",
        "text": "AM:Super P:PVDF = 96:2:2",
    },
    {
        "label": "음극 · Graphite:Super P:CMC:SBR = 95:1:2:2",
        "text": "Graphite:Super P:CMC:SBR = 95:1:2:2",
    },
)
