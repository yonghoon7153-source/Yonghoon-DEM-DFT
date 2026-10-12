"""보고서 3.3 · 5.4 절의 산술 — ps45 덱 값 × LIGGGHTS 식 (9) · (11) · Rayleigh 시간 (4).

실행: python3 deck_numbers.py   (덱 단위 · 길이 표는 실제 단위 µm 로도 출력)
덱: docs/reviews/codex_ps45_porosity_evidence_20261001/reference/dem_scripts/ps_sweep_6mah_20260914/in.ps_7_3_r45.liggghts
    57–58 · 60–90 · 107–109 행.  식: normal_model_hooke_hysteresis.h 138–163 · fix_check_timestep_gran.cpp 261–262.
"""
import math

T = {"AM_P": dict(r=4.5e-3, rho=4800, E=1.4e8, nu=0.25),
     "AM_S": dict(r=2.0e-3, rho=4800, E=1.4e8, nu=0.25),
     "SE": dict(r=0.5e-3, rho=2000, E=1.35e6, nu=0.30)}
IDX = {"AM_P": 0, "AM_S": 1, "SE": 2}
K2M = [[1.5, 1.5, 3.0], [1.5, 1.5, 3.0], [3.0, 3.0, 5.0]]   # coefficientMaxElasticStiffness
KC = [[1e5, 1e5, 2e5], [1e5, 1e5, 2e5], [2e5, 2e5, 1e6]]     # coefficientAdhesionStiffness
PHI = [[0.05, 0.05, 0.01], [0.05, 0.05, 0.01], [0.01, 0.01, 0.005]]  # coefficientPlasticityDepth
V, E_REST, DT = 2.0, 0.3, 1.0e-6
SCALE_LEN = 1000.0   # 덱 길이 = 실제 × 1000


def mass(t):
    return T[t]["rho"] * 4.0 / 3.0 * math.pi * T[t]["r"] ** 3


def estar(a, b):
    return 1.0 / ((1 - T[a]["nu"] ** 2) / T[a]["E"] + (1 - T[b]["nu"] ** 2) / T[b]["E"])


def pair(a, b, wall=False):
    rs = T[a]["r"] if wall else T[a]["r"] * T[b]["r"] / (T[a]["r"] + T[b]["r"])
    ms = mass(a) if wall else mass(a) * mass(b) / (mass(a) + mass(b))
    es = estar(a, b)
    kn = 16 / 15 * math.sqrt(rs) * es * (15 * ms * V * V / (16 * math.sqrt(rs) * es)) ** 0.2
    gn = math.sqrt(4 * ms * kn / (1 + (math.pi / math.log(E_REST)) ** 2))
    i, j = IDX[a], IDX[b]
    a2 = K2M[i][j]
    dlim = a2 / (a2 - 1) * PHI[i][j] * 2 * rs
    d0 = (1 - 1 / a2) * dlim
    da = dlim * (a2 - 1) / (a2 + KC[i][j])
    return rs, ms, es, kn, gn, dlim, d0, da


def main():
    zeta = -math.log(E_REST) / math.sqrt(math.pi ** 2 + math.log(E_REST) ** 2)
    print(f"zeta(e={E_REST}) = {zeta:.4f}")
    print(f"{'pair':16s} {'k1 (deck)':>11s} {'gamma_n':>11s} {'dlim/2R*':>9s} {'dlim um':>9s} {'d0 um':>9s} {'da um':>10s}")
    for a, b, w in [("AM_P", "AM_P", 0), ("AM_P", "AM_S", 0), ("AM_S", "AM_S", 0), ("AM_P", "SE", 0),
                    ("AM_S", "SE", 0), ("SE", "SE", 0), ("SE", "AM_P", 1)]:
        rs, ms, es, kn, gn, dlim, d0, da = pair(a, b, bool(w))
        tag = ("wall(type1)-" + a) if w else f"{a}-{b}"
        um = 1e6 / SCALE_LEN
        print(f"{tag:16s} {kn:11.4e} {gn:11.4e} {dlim / (2 * rs):9.5f} {dlim * um:9.5f} {d0 * um:9.5f} {da * um:10.3e}")
    for t, p in T.items():
        g = p["E"] / (2 * (1 + p["nu"]))
        dtr = math.pi * p["r"] * math.sqrt(p["rho"] / g) / (0.1631 * p["nu"] + 0.8766)
        print(f"Rayleigh {t:5s} dt_R = {dtr:.4e} (deck)  dt/dt_R = {100 * DT / dtr:.2f} %")


if __name__ == "__main__":
    main()
