"""Reading what EC-Lab wrote.

The sign of the imaginary part is the trap this file exists for: BioLogic
stores ``-Im(Z)`` because that is the Nyquist y axis, and reading it as
``Im(Z)`` flips every spectrum through the real axis.  Nothing crashes -- the
arcs simply point the wrong way and no fit converges.
"""

import numpy as np
import pytest
import synthetic_eis as S

from wrdkit.eis import UnknownColumn, read_mpr_bytes, read_mps_text, read_mpt_text


@pytest.fixture
def spectrum_bytes():
    frequency = S.log_sweep()
    z = S.randles(frequency)
    return S.build_mpr(S.spectrum_columns(frequency, z)), frequency, z


def test_the_rows_survive_the_round_trip(spectrum_bytes):
    data, frequency, z = spectrum_bytes
    read = read_mpr_bytes(data)
    assert len(read) == len(frequency)
    assert read.frequency_hz == pytest.approx(frequency, rel=1e-6)
    assert read.z_re == pytest.approx(z.real, rel=1e-5, abs=1e-6)


def test_the_imaginary_part_comes_back_negative_for_a_capacitor(spectrum_bytes):
    """The file says -Im(Z); we hand back Im(Z).  A capacitive arc is negative."""
    data, _, z = spectrum_bytes
    read = read_mpr_bytes(data)
    assert read.z_im == pytest.approx(z.imag, rel=1e-5, abs=1e-6)
    assert np.all(read.z_im < 0)
    # And the raw column is still there, under its own name, still positive.
    assert np.all(read.columns["-Im(Z)/Ohm"] > 0)


def test_the_rows_are_found_whatever_the_preamble_is():
    """Module versions pad differently.  Anchoring on the end is why we cope."""
    frequency = S.log_sweep(1e5, 1.0)
    z = S.randles(frequency)
    columns = S.spectrum_columns(frequency, z)
    for preamble in (64, 405, 1007, 4096):
        read = read_mpr_bytes(S.build_mpr(columns, preamble=preamble))
        assert read.frequency_hz[0] == pytest.approx(frequency[0], rel=1e-6)
        assert read.z_re[-1] == pytest.approx(z.real[-1], rel=1e-5)


def test_a_column_we_cannot_size_stops_the_read():
    """One unknown width shifts every column after it.

    The frequencies would still look plausible and the impedances would be
    garbage, so this must not be a warning (§0.4).
    """
    frequency = S.log_sweep(1e5, 1e2)
    columns = S.spectrum_columns(frequency, S.randles(frequency))
    data = bytearray(S.build_mpr(columns))
    # Rewrite the first column id (freq/Hz, 32) as one nobody has mapped.
    at = data.find(b"MODULE" + b"VMP data".ljust(10)) + 65 + 6
    data[at:at + 2] = (911).to_bytes(2, "little")
    with pytest.raises(UnknownColumn, match="911"):
        read_mpr_bytes(bytes(data))


def test_a_file_without_a_data_module_says_so():
    frequency = S.log_sweep(1e5, 1e2)
    columns = S.spectrum_columns(frequency, S.randles(frequency))
    data = S.build_mpr(columns).replace(b"VMP data  ", b"VMP other ")
    with pytest.raises(ValueError, match="no data module"):
        read_mpr_bytes(data)


def test_something_that_is_not_an_mpr_is_refused():
    with pytest.raises(ValueError, match="magic"):
        read_mpr_bytes(b"PK\x03\x04 this is a zip")


def test_a_cycling_record_is_not_read_as_a_spectrum():
    """No frequency column means this was not an impedance sweep."""
    n = 5
    columns = {"time/s": np.arange(n, dtype=float),
               "cycle number": np.ones(n),
               "Ns": np.zeros(n)}
    with pytest.raises(ValueError, match="freq/Hz"):
        read_mpr_bytes(S.build_mpr(columns))


# --- the ASCII export ------------------------------------------------------

def test_the_text_export_reads_the_same_numbers():
    frequency = S.log_sweep(1e6, 1e-1)
    z = S.randles(frequency)
    columns = S.spectrum_columns(frequency, z)
    read = read_mpt_text(S.build_mpt(columns))
    assert read.frequency_hz == pytest.approx(frequency, rel=1e-6)
    assert read.z_im == pytest.approx(z.imag, rel=1e-5, abs=1e-6)


def test_a_comma_decimal_export_is_still_numbers():
    """EC-Lab writes the PC's locale separator, and half this lab is Korean
    Windows.  Read as text those rows become NaN and every fit fails."""
    frequency = S.log_sweep(1e4, 1e1)
    z = S.randles(frequency)
    columns = S.spectrum_columns(frequency, z)
    read = read_mpt_text(S.build_mpt(columns, comma_decimal=True))
    assert read.z_re == pytest.approx(z.real, rel=1e-5, abs=1e-6)


def test_the_column_names_are_the_last_header_line():
    """`Nb header lines` counts the name row too.  Off by one and the names
    become the first data row -- the read then fails looking for freq/Hz."""
    frequency = S.log_sweep(1e4, 1e1)
    columns = S.spectrum_columns(frequency, S.randles(frequency))
    read = read_mpt_text(S.build_mpt(columns))
    assert "freq/Hz" in read.columns
    assert len(read) == len(frequency)


def test_a_file_that_is_not_an_export_says_so():
    with pytest.raises(ValueError, match="Nb header lines"):
        read_mpt_text("just some text\n1\t2\t3\n")


# --- the settings file -----------------------------------------------------

MPS = """EC-LAB SETTING FILE

Number of linked techniques : 1

Device : VSP-300
Electrode surface area : 0.001 cm2

Technique : 1
Potentio Electrochemical Impedance Spectroscopy
Mode                Single sine
E (V)               0.0000
fi                  7.000
unit fi             MHz
ff                  10.000
unit ff             mHz
Nd                  10
Va (mV)             5.0
Na                  2
"""


def test_the_settings_carry_the_sweep():
    """The instrument knows the frequency range; nobody should retype it (§0.3)."""
    read = read_mps_text(MPS)
    assert read["technique"] == "Potentio Electrochemical Impedance Spectroscopy"
    assert read["frequency_start_hz"] == pytest.approx(7e6)
    assert read["frequency_end_hz"] == pytest.approx(1e-2)
    assert read["amplitude_mv"] == "5.0"
    assert read["Device"] == "VSP-300"


def test_an_unknown_unit_is_left_alone_rather_than_guessed():
    read = read_mps_text(MPS.replace("unit ff             mHz",
                                     "unit ff             furlongs"))
    assert "frequency_end_hz" not in read
    assert read["frequency_end_unit"] == "furlongs"


# --- against a real instrument file ----------------------------------------
#
#     WRDKIT_EIS_SAMPLE=/path/to/file.mpr pytest
#
# Physics, not values: these hold for any PEIS record.

def test_a_real_sweep_goes_high_to_low(sample_mpr):
    frequency = sample_mpr.frequency_hz
    assert np.all(np.diff(frequency) < 0), "EC-Lab sweeps downward"
    assert frequency[0] > frequency[-1]


def test_a_real_spectrum_is_capacitive_somewhere(sample_mpr):
    """Some part of any cell spectrum sits below the real axis.

    If the sign were read the wrong way round this would still pass on an
    inductive-only record, so it is paired with the magnitude check below --
    together they say the two columns describe the same complex number.
    """
    assert np.any(sample_mpr.z_im < 0)


def test_a_real_magnitude_matches_its_own_parts(sample_mpr):
    """|Z| is stored as well as Re and Im.  They have to agree."""
    stored = sample_mpr.columns.get("|Z|/Ohm")
    if stored is None:
        pytest.skip("this file carries no |Z| column")
    assert sample_mpr.magnitude == pytest.approx(stored, rel=1e-4)


def test_a_real_phase_matches_its_own_parts(sample_mpr):
    stored = sample_mpr.columns.get("Phase(Z)/deg")
    if stored is None:
        pytest.skip("this file carries no phase column")
    assert sample_mpr.phase_deg == pytest.approx(stored, rel=1e-3, abs=1e-2)
