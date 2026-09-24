"""Was the cell at rest? -- the DC record of a sweep (ADR 0043, 보완 7).

The sweeps here are *measured*, not written down: `synthetic_eis.measure_peis`
drives a known impedance with a sine, adds the DC current of a cell that is
still settling, and reads the first harmonic the way a lock-in does.  So the
error the drift puts into each point is known, and the record can be checked
against it rather than against itself.
"""

import numpy as np
import pytest
from synthetic_eis import measure_peis

from wrdkit.eis.audit import audit_spectrum
from wrdkit.eis.circuit import parse_circuit
from wrdkit.eis.spectrum import Spectrum
from wrdkit.eis.stationarity import dc_record

#: 실측 풀셀 #15 (Dcell12_4_C06) 의 쓰는 맞춤 — 0.01 Hz 에서 |Z| ≈ 160 Ω.
FULL_15 = ("L1-R0-p(R1,CPE1)-TL1",
           {"L1": 5.46e-07, "R0": 0.000817, "R1": 120, "CPE1_Q": 0.000102,
            "CPE1_n": 0.669, "TL1_Ri": 34.9, "TL1_Re": 18.1, "TL1_Rct": 4.73,
            "TL1_Q": 7.61e-06, "TL1_n": 0.82, "TL1_Wr": 50.4, "TL1_Wn": 0.282,
            "TL1_Wt": 234})


def sweep(fmax=7e6, fmin=0.01, per_decade=10):
    count = int(round(np.log10(fmax / fmin) * per_decade)) + 1
    return np.logspace(np.log10(fmax), np.log10(fmin), count)


def true_impedance(f):
    circuit, values = FULL_15
    model = parse_circuit(circuit)
    return model.impedance([values[name] for name in model.parameter_names], f)


def measured(columns):
    return Spectrum(columns["freq/Hz"], columns["Re(Z)/Ohm"], -columns["-Im(Z)/Ohm"],
                    columns=columns)


def settling(start_a=300e-6, tau_s=600.0):
    """A potentiostatic hold on a cell that is not at equilibrium: the current
    it draws decays as it settles."""
    return lambda t: start_a * np.exp(-t / tau_s)


def test_a_settling_cell_is_seen_in_its_dc_current_where_kk_sees_nothing():
    """0.01 Hz 의 점이 6 % 틀어졌는데 KK 는 판정이 없다 — 매끄러운 드리프트는
    KK 를 만족하는 꼴로 들어간다.  직류 전류 기록은 그것을 본다: 300 → 95 µA,
    가장 낮은 주파수에서 한 주기 동안 교류 진폭의 19 % 가 움직였다."""
    f = sweep()
    true = true_impedance(f)
    columns = measure_peis(f, true, dc_current_a=settling())
    spectrum = measured(columns)
    error = np.abs(spectrum.z - true) / np.abs(true)
    assert error[-1] > 0.05

    audit = audit_spectrum(spectrum)
    assert not [one for one in audit.findings if one.code.startswith("kk_")]
    (drift,) = [one for one in audit.findings if one.code == "dc_drift"]
    assert drift.severity == "note"
    assert drift.message.startswith("직류 전류가 스윕 동안 300 → 95.5 µA 로 변했습니다")
    assert "0.01–" in drift.message and "약 6 % 틀어져" in drift.message

    record = dc_record(spectrum)
    assert record.judged and record.source == "current"
    start, end = record.current_ends_a
    assert start == pytest.approx(300e-6, rel=0.01)
    # 끝은 마지막 세 점의 가운데 값 — 한 점의 흔들림이 머리말이 되지 않게.
    assert end == pytest.approx(np.median(columns["<I>/mA"][-3:]) * 1e-3)
    assert 90e-6 < end < 100e-6
    assert record.at_hz == pytest.approx(0.01)
    assert 0.15 < record.max_share < 0.25


def test_the_share_over_pi_is_the_error_a_lock_in_makes():
    """잰 대로의 오차와 ``share / π`` 가 같다.  기울기를 점의 시각(구간의 끝)
    사이에서 재므로, 구간이 점마다 길어지는 저주파에서는 ``share / π`` 가 실제
    오차보다 10 % 쯤 작다 (π·오차/share = 1.11–1.12, 한쪽 차분인 마지막 점 0.96)."""
    f = sweep()
    true = true_impedance(f)
    spectrum = measured(measure_peis(f, true, dc_current_a=settling()))
    record = dc_record(spectrum)
    error = np.abs(spectrum.z - true) / np.abs(true)
    low = f < 0.1
    assert np.allclose(np.pi * error[low] / record.share[low], 1.1, atol=0.15)


@pytest.mark.parametrize("current", [None, lambda t: 5e-6 + 0.0 * t])
def test_a_cell_at_rest_or_under_a_steady_current_does_not_move(current):
    """쉰 셀, 그리고 늘 같은 새는 전류(5 µA) — 둘 다 스윕 동안 움직이지 않는다.
    직류 전류의 크기가 아니라 그것이 **변하는 것**이 드리프트다."""
    f = sweep()
    true = true_impedance(f)
    spectrum = measured(measure_peis(f, true, dc_current_a=current))
    record = dc_record(spectrum)
    assert record.judged
    assert record.max_share < 1e-3
    # 늘 같은 직류는 한 주기의 적분에서 빠진다 — 점도 틀어지지 않는다.
    assert (np.abs(spectrum.z - true) / np.abs(true)).max() < 1e-6
    assert "dc_drift" not in [one.code for one in audit_spectrum(spectrum).findings]


def test_without_the_columns_it_says_what_is_missing():
    f = sweep(1e5, 1, 5)
    z = true_impedance(f)
    bare = Spectrum(f, z.real, z.imag)
    assert dc_record(bare).reason == "파일에 점마다의 시각이 없습니다"
    timed = Spectrum(f, z.real, z.imag, columns={"time/s": np.arange(f.size, dtype=float)})
    assert dc_record(timed).reason == "파일에 직류 전류·전위 기록이 없습니다"
    zeros = Spectrum(f, z.real, z.imag, columns={"time/s": np.arange(f.size, dtype=float),
                                                 "<I>/mA": np.zeros(f.size)})
    assert not dc_record(zeros).judged              # 0 만 적힌 열은 안 잰 것이다


def test_without_an_ac_amplitude_the_levels_are_still_read():
    f = sweep()
    columns = measure_peis(f, true_impedance(f), dc_current_a=settling())
    del columns["|I|/A"], columns["|Ewe|/V"]
    record = dc_record(measured(columns))
    assert record.judged and record.share is None and record.source == ""
    assert record.current_ends_a[0] == pytest.approx(300e-6, rel=0.01)


def test_a_galvanostatic_sweep_is_read_from_its_potential():
    """전류를 잡고 재면 (GEIS) 움직이는 것은 전위다 — 0 만 적힌 ``<I>`` 는 안
    잰 것이고, 기울기는 ``<Ewe>`` 와 ``|Ewe|`` 로 잰다."""
    f = sweep(1e5, 0.01, 5)
    z = true_impedance(f)
    time = np.cumsum(2.0 / f)
    columns = {"time/s": time, "<I>/mA": np.zeros(f.size),
               "<Ewe>/V": 3.70 - 1e-5 * time,          # 10 µV/s 로 이완
               "|Ewe|/V": np.full(f.size, 0.01), "freq/Hz": f}
    record = dc_record(Spectrum(f, z.real, z.imag, columns=columns))
    assert record.judged and record.source == "potential" and record.current_a is None
    # 0.01 Hz 한 주기 100 s 동안 1 mV — 10 mV 진폭의 10 %.
    assert record.max_share == pytest.approx(0.10, rel=0.01)
    assert record.at_hz == pytest.approx(0.01)
    (drift,) = [one for one in audit_spectrum(Spectrum(f, z.real, z.imag, columns=columns)
                                              ).findings if one.code == "dc_drift"]
    assert drift.message.startswith("직류 전위가 스윕 동안 3.7")
    assert drift.message.endswith("직류 전위가 멈출 때까지 쉬게 한 뒤 다시 재세요")


def test_the_audit_carries_the_record():
    f = sweep()
    spectrum = measured(measure_peis(f, true_impedance(f), dc_current_a=settling()))
    dc = audit_spectrum(spectrum).dc
    assert dc["judged"] and dc["source"] == "current"
    assert dc["current_ua"][0] == pytest.approx(300, rel=0.01)
    assert dc["share"] == pytest.approx(dc_record(spectrum).max_share)
    assert dc["at_hz"] == pytest.approx(0.01)
    assert dc["duration_s"] == pytest.approx(dc_record(spectrum).duration_s)
    assert audit_spectrum(Spectrum(f, spectrum.z_re, spectrum.z_im)).dc == {
        "judged": False, "reason": "파일에 점마다의 시각이 없습니다"}
