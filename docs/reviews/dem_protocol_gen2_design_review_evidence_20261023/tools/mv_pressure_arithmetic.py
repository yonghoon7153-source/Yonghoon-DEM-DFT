"""Review-only algebraic counterexamples; no DEM, no deck/data writes."""
from math import pi, sin, cos, sqrt
import json

F, area, dt, chunk, kp, vmax = 750.0, 0.0025, 1e-6, 5000, 30.0, 0.01
mass = 0.904
ke_ref = 1.695918e-5

def admitted(samples):
    conv_n = 0
    previous_ke = ke_ref
    for n, force, dz, kinetic in samples:
        # Exact relevant comparisons from in.branch_B.liggghts:297-305.
        abort = (kinetic > 1.0 or
                 (n > 10 and kinetic > 1e-2) or
                 (n > 10 and kinetic > 10*previous_ke and kinetic > 1e-3) or
                 force > 2*F)
        if abort:
            return {"status": "GUARD", "chunk": n}
        conv_n = conv_n + 1 if abs(force/F-1) <= .01 and dz <= 5e-6 else 0
        previous_ke = kinetic
        if conv_n >= 4 and n >= 10:
            return {"status": "CONVERGED", "chunk": n, "kinetic_J": kinetic}
    return {"status": "RUNNING"}

warmup = [(n, 700 if n < 7 else 750, 1e-5 if n < 7 else 0, .5) for n in range(1, 11)]
late = [(n, 700 if n < 11 else 750, 1e-5 if n < 11 else 0, .009) for n in range(1, 15)]
T = dt*chunk
osc_amplitude = vmax*kp*.03*T/(2*pi)
outputs = {
    "boundary_force_units": {
        "Pdeck_Pa": F/area,
        "Pphysical_MPa": F/area*1000/1e6,
        "target165MPa_force_N": 165e6/1000*area,
        "physical_force_50um_square_N": 300e6*(50e-6)**2,
    },
    "warmup_counterexample": admitted(warmup),
    "late_counterexample": admitted(late),
    "warmup_KE_ratio_to_reference": .5/ke_ref,
    "warmup_mass_rms_velocity_m_s": sqrt(2*.5/mass),
    "late_KE_ratio_to_reference": .009/ke_ref,
    "late_mass_rms_velocity_m_s": sqrt(2*.009/mass),
    "sampling_counterexample": {
        "description": "F(t)=750[1+0.03sin(2pi t/T)], v=0.009sin(2pi t/T), T=.005 s; servo-compatible sinusoidal input, not DEM solution",
        "period_steps": T/dt,
        "relative_force_peak": .03,
        "velocity_peak_m_s": .009,
        "height_amplitude_deck_m": osc_amplitude,
        "height_amplitude_physical_um": osc_amplitude*1000,
        "sample_force_errors": [abs(.03*sin(2*pi*n)) for n in range(1, 5)],
        "sample_height_deltas_m": [abs(osc_amplitude*(cos(2*pi*n)-cos(2*pi*(n-1)))) for n in range(1, 5)],
    },
    "linear_servo_estimates": [
        {"K_N_m": K, "tau_s": F/(kp*vmax*K),
         "tau_steps": F/(kp*vmax*K)/dt,
         "residual_h_um_at_dz_gate_approx": 5e-6/(dt*chunk)*F/(kp*vmax*K)*1000}
        for K in [47000, 4700, 141000]
    ],
    "gravity_budget": {
        "weight_N": mass*9.81,
        "bottom_minus_top_physical_MPa": mass*9.81/area*1000/1e6,
        "fraction_of300": mass*9.81/F,
    },
    "count_guard_can_admit_volume_loss": {
        "50_AM_r45_porosity_pp_at111052nm": 100*50*(4*pi/3)*4.5**3/(2500*111.052),
        "one_AM_r45_porosity_pp_at111052nm": 100*(4*pi/3)*4.5**3/(2500*111.052),
    },
    "normal_history_reset_example_dimensionless": {
        "kn": 1, "k2Max": 3, "deltaMaxLim": 1, "current_overlap": .4,
        "old_deltaMax": .6, "old_k2": 1+2*.6,
        "old_fHys": (1+2*.6)*(.4-.6)+.6,
        "reset_deltaMax": .4, "reset_fHys": .4,
    },
}
assert outputs["warmup_counterexample"]["status"] == "CONVERGED"
assert outputs["warmup_counterexample"]["chunk"] == 10
assert outputs["late_counterexample"]["status"] == "CONVERGED"
assert outputs["late_counterexample"]["chunk"] == 14
print(json.dumps(outputs, ensure_ascii=False, indent=2))
