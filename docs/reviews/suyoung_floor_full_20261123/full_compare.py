"""Compare complete development loading traces on their native common displacement knots."""
from bisect import bisect_left
import csv
import io
import math


FIXED_REFERENCE_MPA = 0.6636991102836952
COLUMNS = ("step", "time_code", "height", "bottom_pressure_E", "phi_m")
TERMINALS = ("TARGET_BRACKETED", "GEOMETRY_LIMIT")


def require(value, message):
    if not value:
        raise ValueError(message)


def exceeds(error, reference):
    """Compare positive binary64 inputs against exactly 1/20 without rounding the ratio."""
    en, ed = error.as_integer_ratio()
    rn, rd = reference.as_integer_ratio()
    return 20 * en * rd > rn * ed


def read_native(raw, width, speed, dt, terminal):
    require(isinstance(raw, bytes) and terminal in TERMINALS, "incomplete or unsupported native arm")
    reader = csv.reader(io.StringIO(raw.decode("ascii"), newline=""), strict=True)
    require(tuple(next(reader, ())) == COLUMNS, "unexpected trace columns")
    displacements, pressures = [], []
    for step, row in enumerate(reader):
        require(len(row) == len(COLUMNS) and row[0] == str(step), "non-contiguous native steps")
        t, height, pressure_e, phi = map(float, row[1:])
        require(t == dt*step and height == width-t*speed and height >= .75*width,
                "inconsistent native clock or wall geometry")
        require(math.isfinite(phi) and math.isclose(phi, .78*width/height, rel_tol=1.e-12),
                "unexpected area fraction")
        u, pressure = width-height, pressure_e * 10.
        require(math.isfinite(pressure) and pressure >= 0. and (step > 0 or pressure == 0.),
                "invalid native pressure")
        require(not displacements or (u > displacements[-1] and pressures[-1] < 1.2),
                "extra sample after first target crossing or non-increasing displacement")
        displacements.append(u)
        pressures.append(pressure)
    require(len(pressures) >= 2, "missing loading trace")
    if terminal == "TARGET_BRACKETED":
        require(pressures[-1] >= 1.2, "missing first native target crossing")
    else:
        require(pressures[-1] < 1.2 and width-len(pressures)*dt*speed < .75*width,
                "geometry limit appears before the final feasible step")
    return displacements, pressures


def arm_info(u, p, terminal):
    positive = [i for i, v in enumerate(p) if v > 0.]

    def item(i):
        return dict(step=i, u=u[i], pressure_MPa=p[i])

    return dict(terminal=terminal, steps=len(u)-1, end_u=u[-1], end_pressure_MPa=p[-1],
                positive_samples=len(positive), first_positive=item(positive[0]) if positive else None,
                last_positive=item(positive[-1]) if positive else None)


def interpolate(u, x, p):
    i = bisect_left(x, u)
    if i < len(x) and x[i] == u:
        return p[i], True
    require(0 < i < len(x), "extrapolation is not allowed")
    a = (u-x[i-1])/(x[i]-x[i-1])
    return p[i-1]+a*(p[i]-p[i-1]), False


def summarize(knots, fine_peak):
    if not knots:
        return dict(samples=0, first_worst=None, max_abs_difference_MPa=None,
                    fixed_reference_comparison="NO_SAMPLES", fine_peak_comparison="NO_SAMPLES")
    worst = max(knots, key=lambda k: abs(k["F8_minus_F16_MPa"]))
    error = abs(worst["F8_minus_F16_MPa"])
    fixed_above = [k for k in knots if exceeds(abs(k["F8_minus_F16_MPa"]), FIXED_REFERENCE_MPA)]
    fine_above = ([k for k in knots if exceeds(abs(k["F8_minus_F16_MPa"]), fine_peak)]
                  if fine_peak else [])
    return dict(samples=len(knots), start_u=knots[0]["u"], end_u=knots[-1]["u"], first_worst=worst,
                max_abs_difference_MPa=error, fixed_reference_ratio=error/FIXED_REFERENCE_MPA,
                fixed_reference_comparison="EXCEEDS" if fixed_above else "WITHIN",
                fixed_reference_exceeding_samples=len(fixed_above),
                fixed_reference_first_exceedance=fixed_above[0] if fixed_above else None,
                fine_peak_ratio=error/fine_peak if fine_peak else None,
                fine_peak_comparison=("HOLD_ZERO_REFERENCE" if not fine_peak else
                                      ("EXCEEDS" if fine_above else "WITHIN")),
                fine_peak_exceeding_samples=len(fine_above) if fine_peak else None,
                fine_peak_first_exceedance=fine_above[0] if fine_above else None)


def compare_pair(coarse_rows, fine_rows, *, width, speed, dt8, dt16, terminal8, terminal16):
    """CSV bytes are in solver units. Reported pressures and pressure differences are MPa.

    The native union includes zero, the last common displacement and every interior
    coarse and fine sample. The both-positive view is a subset of these same knots.
    """
    require(all(math.isfinite(v) and v > 0. for v in (width, speed, dt8, dt16)) and dt8 == 2*dt16,
            "invalid native clocks for F8/F16")
    a, pa = read_native(coarse_rows, width, speed, dt8, terminal8)
    b, pb = read_native(fine_rows, width, speed, dt16, terminal16)
    end = min(a[-1], b[-1])
    native_union = sorted({v for x in (a, b) for v in x if v <= end})
    samples = []
    for u in native_union:
        f8, native8 = interpolate(u, a, pa)
        f16, native16 = interpolate(u, b, pb)
        samples.append(dict(u=u, F8_MPa=f8, F16_MPa=f16, F8_minus_F16_MPa=f8-f16,
                            F8_native=native8, F16_native=native16))
    fine_peak = max(row["F16_MPa"] for row in samples)
    contact = [s for s in samples if s["F8_MPa"] > 0. and s["F16_MPa"] > 0.]
    return dict(label="DEVELOPMENT_ONLY", pair="F8_F16", fixed_reference_MPa=FIXED_REFERENCE_MPA,
                fixed_5percent_MPa=FIXED_REFERENCE_MPA/20., fine_peak_on_common_support_MPa=fine_peak,
                arms={"F8": arm_info(a, pa, terminal8), "F16": arm_info(b, pb, terminal16)},
                common=summarize(samples, fine_peak), both_positive_knots=summarize(contact, fine_peak),
                u6_qualified=False, stage3_go=False)
