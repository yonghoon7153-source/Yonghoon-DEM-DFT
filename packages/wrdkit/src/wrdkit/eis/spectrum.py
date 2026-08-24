"""One impedance spectrum, in the units the instrument wrote.

Raw only: ohms and hertz (ADR 0001).  Conductivity needs a thickness and an
area, and those change -- a pellet gets re-measured, someone corrects a
micrometer reading -- so they are applied when the number is asked for, not
baked into what we store.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class Spectrum:
    """Frequency-domain impedance of one measurement.

    ``z_im`` is the **imaginary part itself**, not its negative.  Instruments
    disagree about this: BioLogic's exports carry ``-Im(Z)`` because that is
    what a Nyquist plot wants on its y axis, and reading that column as
    ``Im(Z)`` flips every spectrum through the real axis -- a capacitive arc
    becomes an inductive one and no fit converges.  The readers negate on the
    way in so that everything downstream can assume the physics convention
    (``Z = Z' + jZ''`` with ``Z'' < 0`` for a capacitor).
    """

    #: Hz, as measured.  Not necessarily sorted.
    frequency_hz: np.ndarray
    #: Ohm.
    z_re: np.ndarray
    #: Ohm, signed.  Negative for capacitive behaviour.
    z_im: np.ndarray
    #: What the file said about how it was measured.  Free-form on purpose:
    #: the two formats carry different fields and we do not invent the rest.
    metadata: dict = field(default_factory=dict)
    #: Every column the file carried, by its own name.  Kept so a question we
    #: have not thought of yet can still be answered from the parsed file
    #: instead of a re-parse.
    columns: dict[str, np.ndarray] = field(default_factory=dict)

    def __post_init__(self) -> None:
        n = len(self.frequency_hz)
        if len(self.z_re) != n or len(self.z_im) != n:
            raise ValueError("frequency, Re(Z) and Im(Z) must be the same length")

    def __len__(self) -> int:
        return len(self.frequency_hz)

    @property
    def z(self) -> np.ndarray:
        """Complex impedance, physics convention."""
        return self.z_re + 1j * self.z_im

    @property
    def magnitude(self) -> np.ndarray:
        return np.abs(self.z)

    @property
    def phase_deg(self) -> np.ndarray:
        return np.degrees(np.angle(self.z))

    def sorted_by_frequency(self, descending: bool = True) -> Spectrum:
        """The same points, ordered.  EC-Lab writes high-to-low; a hand-made
        CSV may not, and every arc-finding heuristic assumes an order."""
        order = np.argsort(self.frequency_hz)
        if descending:
            order = order[::-1]
        return Spectrum(
            frequency_hz=self.frequency_hz[order],
            z_re=self.z_re[order],
            z_im=self.z_im[order],
            metadata=dict(self.metadata),
            columns={name: values[order] for name, values in self.columns.items()},
        )

    def select(self, mask: np.ndarray) -> Spectrum:
        """The subset ``mask`` keeps.  Used to drop the inductive tail."""
        return Spectrum(
            frequency_hz=self.frequency_hz[mask],
            z_re=self.z_re[mask],
            z_im=self.z_im[mask],
            metadata=dict(self.metadata),
            columns={name: values[mask] for name, values in self.columns.items()},
        )
