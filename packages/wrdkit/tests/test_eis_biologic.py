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
from wrdkit.eis.biologic import read_mpr_sweeps


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


# --- 리뷰 재현 회귀 (Codex #10·#11) ------------------------------------------

def test_a_corrupted_module_length_is_refused_not_reanchored():
    """길이 필드 1바이트가 어긋나면 모든 행이 한 바이트씩 밀린다.

    밀린 행도 float 로는 읽히므로, 숫자만 보고는 모른다 — 모듈 끝이 다음
    MODULE 헤더나 EOF 에 정확히 닿는지가 컨테이너의 자기 검증이다.  리뷰
    재현: N+1 로 만든 파일이 31점짜리 쓰레기 스펙트럼으로 수용됐다.
    """
    frequency = S.log_sweep(1e6, 1e-2, 8)
    z = S.randles(frequency)
    data = bytearray(S.build_mpr(S.spectrum_columns(frequency, z)))
    import re as _re
    import struct as _struct
    for m in _re.finditer(b"MODULE", bytes(data)):
        short = bytes(data[m.start() + 6:m.start() + 16]).decode().strip()
        if short == "VMP data":
            length_at = m.start() + 41 + 4
            (length,) = _struct.unpack_from("<I", bytes(data), length_at)
            _struct.pack_into("<I", data, length_at, length + 1)
            break
    with pytest.raises(ValueError, match="module boundary"):
        read_mpr_bytes(bytes(data))


def test_magnitude_that_disagrees_with_its_parts_is_refused():
    """|Z| 는 계측기가 같은 행에서 쓴 잉여값이다.  Re/Im 과 안 맞으면 행이
    밀렸거나 파일이 손상된 것이므로, 그럴듯한 숫자를 내보내지 않는다."""
    frequency = S.log_sweep(1e6, 1e-2, 8)
    z = S.randles(frequency)
    columns = S.spectrum_columns(frequency, z)
    columns["|Z|/Ohm"] = columns["|Z|/Ohm"] * 1.5
    with pytest.raises(ValueError, match="does not match"):
        read_mpr_bytes(S.build_mpr(columns))


def test_ec_labs_trailing_tab_on_the_header_is_not_damage():
    """EC-Lab 은 머리글 줄 끝에도 탭을 하나 더 찍는다.

    데이터 줄의 꼬리 탭은 떼면서 머리글의 것은 안 떼서, 이름 46 개와 값 45 개가
    어긋나 **멀쩡한 파일이 "the export is damaged" 로 거절**됐다 -- 실측
    `Dry_1.mpt` (EC-Lab v11.63, 89점) 가 그랬다.  서식이지 데이터가 아니다.
    """
    frequency = S.log_sweep(1e5, 1e0, 4)
    z = S.randles(frequency)
    columns = S.spectrum_columns(frequency, z)
    read = read_mpt_text(S.build_mpt(columns, trailing_tab=True))
    assert len(read) == len(frequency)
    assert read.z_re[0] == pytest.approx(z.real[0], rel=1e-5)

    # 그래도 **진짜** 어긋남은 여전히 거절해야 한다 -- 위 관용이 그 가드를
    # 열어 주면 열 이동이 측정값으로 수용된다.
    lines = S.build_mpt(columns, trailing_tab=True).splitlines()
    first = next(i for i, line in enumerate(lines) if line and line[0].isdigit())
    lines[first] = "123\t" + lines[first]
    with pytest.raises(ValueError, match=r"line \d+ has"):
        read_mpt_text("\n".join(lines))


def test_an_mpt_row_with_the_wrong_column_count_is_refused_with_its_line():
    """모자란 행은 조용한 삭제였고 남는 행은 열 이동이었다.

    리뷰 재현: 앞에 셀 하나를 끼우면 Re(Z)=123 이 측정값으로 수용됐다.
    이제 줄 번호와 함께 거절한다.  (꼬리 탭 하나는 서식이므로 눈감는다.)
    """
    frequency = S.log_sweep(1e5, 1e0, 4)
    z = S.randles(frequency)
    text = S.build_mpt(S.spectrum_columns(frequency, z))
    lines = text.splitlines()
    first_data = next(i for i, line in enumerate(lines)
                      if line and line[0].isdigit())
    lines[first_data] = "123\t" + lines[first_data]
    with pytest.raises(ValueError, match=r"line \d+ has"):
        read_mpt_text("\n".join(lines))

    # 모자란 행도 같은 대접
    lines = text.splitlines()
    lines[first_data] = "\t".join(lines[first_data].split("\t")[:-1])
    with pytest.raises(ValueError, match=r"line \d+ has"):
        read_mpt_text("\n".join(lines))


def test_a_blank_essential_cell_is_refused_at_the_boundary():
    """빈 주파수 셀은 NaN 이 되어 업로드는 통과하고 fit 에서야 죽었다.

    파서 경계에서 행 번호와 함께 거절한다 (§0.4).
    """
    frequency = S.log_sweep(1e5, 1e0, 4)
    z = S.randles(frequency)
    text = S.build_mpt(S.spectrum_columns(frequency, z))
    lines = text.splitlines()
    first_data = next(i for i, line in enumerate(lines)
                      if line and line[0].isdigit())
    cells = lines[first_data].split("\t")
    cells[0] = ""
    lines[first_data] = "\t".join(cells)
    with pytest.raises(ValueError, match="not a number at row 1"):
        read_mpt_text("\n".join(lines))


# --- SOC 스캔: 한 파일에 스펙트럼 여럿 (ADR 0022) -----------------------------

def test_a_soc_scan_comes_back_as_one_spectrum_per_sweep():
    """사이클링 사이에 끼어 있는 스윕들을 각각 꺼낸다.

    한 스펙트럼만 돌려주면 실측 파일에서 15~20개를 조용히 버린다.
    """
    sweeps = read_mpr_sweeps(S.build_mpr_soc_scan(sweeps=4, points=10))
    assert len(sweeps) == 4
    assert [len(sw.spectrum) for sw in sweeps] == [10, 10, 10, 10]
    assert [sw.index for sw in sweeps] == [1, 2, 3, 4]
    # 스윕을 가르는 것은 전위·용량이므로 스펙트럼과 함께 다닌다.
    assert [round(sw.potential_v, 2) for sw in sweeps] == [3.6, 3.7, 3.8, 3.9]
    assert all(sw.sequence is not None for sw in sweeps)
    assert sweeps[0].start_time_s < sweeps[-1].start_time_s


def test_a_repeated_sweep_inside_one_sequence_is_still_two_sweeps():
    """주파수가 다시 올라가면 새 스윕이다 — 한 Ns 안에 아홉 번 반복하는
    파일이 실제로 있다."""
    sweeps = read_mpr_sweeps(S.build_mpr_soc_scan(sweeps=2, points=6, cycling_rows=0))
    assert len(sweeps) == 2


def test_the_row_block_may_end_short_of_the_module():
    """실측 파일은 모듈 끝에서 5바이트 앞에서 끝난다.

    5바이트가 밀리면 모든 실수가 다른 실수가 되는데 그것도 float 로는 읽힌다.
    끝에 딱 붙어 있다고 가정하면 이 파일 전체가 쓰레기가 된다.
    """
    for trailer in (0, 5, 11):
        sweeps = read_mpr_sweeps(S.build_mpr_soc_scan(sweeps=2, points=8,
                                                      trailer=trailer))
        assert len(sweeps) == 2, trailer
        assert sweeps[0].spectrum.z_re[0] == pytest.approx(5.0, abs=1e-3), trailer


def test_re_and_im_are_recovered_from_magnitude_and_phase():
    """반쪽셀 파일은 |Z| 와 위상만 싣는다.  Re=|Z|cosφ 는 추정이 아니라 정의다."""
    sweeps = read_mpr_sweeps(S.build_mpr_soc_scan(sweeps=1, points=12))
    spectrum = sweeps[0].spectrum
    # 픽스처의 모델: R_s=5 직렬에 R=20 / C=1e-3 병렬.
    assert spectrum.z_re[0] == pytest.approx(5.0, abs=1e-3)      # 고주파 극한
    assert spectrum.z_re[-1] == pytest.approx(25.0, rel=1e-2)    # 저주파 극한
    assert np.all(spectrum.z_im <= 1e-6)                          # 용량성


def test_an_unknown_column_in_the_middle_is_still_fatal():
    """맨 뒤의 미지 컬럼만 넘어간다.  중간에 있으면 뒤 컬럼을 전부 밀기
    때문에 종전대로 거절한다 (§0.6)."""
    frequency = S.log_sweep(1e5, 1e-1, 6)
    z = S.randles(frequency)
    columns = S.spectrum_columns(frequency, z)
    renamed = {}
    for name, values in columns.items():
        renamed[name] = values
    data = bytearray(S.build_mpr(renamed))
    # freq(32) 를 등록되지 않은 id 로 바꾼다 — 목록 맨 앞이므로 치명적이어야 한다.
    at = data.find(b"VMP data")
    import struct as _struct
    head = data.find(b"MODULE", at - 16)
    _struct.pack_into("<H", data, head + 65 + 6, 999)
    with pytest.raises(UnknownColumn):
        read_mpr_sweeps(bytes(data))


def test_reading_a_scan_as_one_spectrum_says_to_use_the_list():
    """조용히 첫 스윕만 주면 나머지를 잃는다."""
    data = S.build_mpr_soc_scan(sweeps=3, points=8)
    with pytest.raises(ValueError, match="3 impedance sweeps"):
        read_mpr_bytes(data)


# --- 실측 SOC 스캔 파일 ------------------------------------------------------

def test_a_real_scan_holds_many_sweeps_each_a_full_decade_range(sample_mpr_scan):
    assert len(sample_mpr_scan) > 1
    for sw in sample_mpr_scan:
        f = sw.spectrum.frequency_hz
        assert np.all(f > 0)
        assert f[0] > f[-1]                       # 하강 스윕
        assert f[0] / f[-1] > 1e3                 # 여러 decade
        assert len(sw.spectrum) >= 8


def test_a_real_scan_walks_its_capacity_axis(sample_mpr_scan):
    """SOC 스캔의 x축은 용량이다.  스윕마다 달라야 의미가 있다."""
    capacities = [sw.capacity_mah for sw in sample_mpr_scan]
    assert all(q is not None for q in capacities)
    assert max(capacities) - min(capacities) > 0.1
    potentials = [sw.potential_v for sw in sample_mpr_scan]
    assert all(p is not None and np.isfinite(p) for p in potentials)
