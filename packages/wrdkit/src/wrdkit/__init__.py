"""wrdkit -- read and analyse WonATech / Zive ``.wrd`` battery cycler files.

Typical use::

    from wrdkit import read_wrd, summarize_cycles, CellSpec, Basis, normalize_capacity

    wrd = read_wrd("cell.wrd")
    cell = CellSpec(total_mass_mg=31.6, active_wt_percent=80,
                    diameter_mm=13).resolve()
    for cycle in summarize_cycles(wrd):
        print(cycle.cycle_number,
              normalize_capacity(cycle.discharge_capacity_mah, cell, Basis.SPECIFIC))
"""

from .composition import PRESETS, Component, Composition, Role, parse_composition
from .cycles import (
    CycleSummary,
    Profile,
    StepSegment,
    extract_profile,
    segment_steps,
    summarize_cycles,
)
from .downsample import lttb, lttb_indices
from .export import (
    cycles_csv_string,
    profiles_csv_string,
    raw_csv_string,
    write_cycles_csv,
    write_profiles_csv,
    write_raw_csv,
    write_xlsx,
)
from .normalize import (
    BASES,
    Basis,
    CellSpec,
    ResolvedCell,
    areal_loading,
    basis_label,
    c_rate,
    normalize_capacity,
    retention,
)
from .nrbf import NrbfError
from .reference import (
    REFERENCE_ELECTRODES,
    ReferenceElectrode,
    offset_for,
)
from .schedule import Schedule, ScheduleStep
from .wrd import CellStatus, WrdColumn, WrdError, WrdFile, WrdMetadata, read_wrd, read_wrd_bytes

__version__ = "0.1.0"

__all__ = [
    "__version__",
    # reading
    "read_wrd", "read_wrd_bytes", "WrdFile", "WrdMetadata", "WrdColumn",
    "WrdError", "NrbfError", "CellStatus",
    # schedule
    "Schedule", "ScheduleStep",
    # analysis
    "segment_steps", "summarize_cycles", "extract_profile",
    "CycleSummary", "StepSegment", "Profile",
    # normalisation
    "CellSpec", "ResolvedCell", "REFERENCE_ELECTRODES", "ReferenceElectrode", "offset_for", "Basis", "BASES", "basis_label",
    "normalize_capacity", "c_rate", "areal_loading", "retention",
    # composition
    "Composition", "Component", "Role", "parse_composition", "PRESETS",
    # plotting / export
    "lttb", "lttb_indices", "write_raw_csv", "write_cycles_csv",
    "write_profiles_csv", "raw_csv_string", "cycles_csv_string",
    "profiles_csv_string", "write_xlsx",
]
