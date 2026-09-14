"""합성 데이터 트리를 만든다 — dd_eval.m 과 Python 전사본이 **같은 파일**을 읽게.

확장자는 `.xlsx` 로 두되 내용은 CSV 다. Octave 쪽 `readmatrix`/`readtable`
대역품(`oct_stubs/`)이 dlmread 로 읽으므로 확장자를 안 본다. 이렇게 해야
`local_halfcell_name` 이 만드는 **파일명 규약**까지 실제로 검사된다.
"""
import numpy as np, pathlib, sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "synthdata")
(root / "data/half_cell/GITT").mkdir(parents=True, exist_ok=True)
(root / "data/half_cell/step_005C").mkdir(parents=True, exist_ok=True)
(root / "data/literature/Si_OCP_sources").mkdir(parents=True, exist_ok=True)
(root / "data/full_cell/large_cell_033C").mkdir(parents=True, exist_ok=True)

STATES = ["pristine", "100", "200", "300_0009", "300_0147"]
rng = np.random.default_rng(20260910)

# ── 반쪽전지 (GITT 와 005C 둘 다) ───────────────────────────────────────
for src, suf in (("GITT", ""), ("step_005C", "_005C")):
    for si, st in enumerate(STATES):
        n = 160
        pe_c = np.linspace(0, 1, n)
        pe_v = 4.25 - 0.85 * pe_c ** 1.3 - 0.004 * si
        ne_c = np.linspace(0, 1, n)
        ne_v = 0.05 + 0.9 * (1 - ne_c) ** 2.1 + 0.003 * si
        M = np.column_stack([pe_c, pe_v, ne_c, ne_v])
        p = root / f"data/half_cell/{src}/{st}{suf}.xlsx"
        with open(p, "w") as fh:
            fh.write("PE_capacity,PE_voltage,NE_capacity,NE_voltage\n")
            np.savetxt(fh, M, delimiter=",", fmt="%.17g")

# ── 문헌 ────────────────────────────────────────────────────────────────
n = 120
gr_v = np.linspace(0.02, 0.60, n)
gr_c = 1.0 - (gr_v - gr_v.min()) / (gr_v.max() - gr_v.min())
with open(root / "data/literature/Si_Gr_literature_OCP.xlsx", "w") as fh:
    fh.write("Gr_capacity,Gr_voltage\n")
    np.savetxt(fh, np.column_stack([gr_c, gr_v]), delimiter=",", fmt="%.17g")
for name, k in (("Li", 1.0), ("Kunz", 1.15)):
    si_v = np.linspace(0.05, 0.85, n)
    si_c = 1.0 - ((si_v - si_v.min()) / (si_v.max() - si_v.min())) ** k
    with open(root / f"data/literature/Si_OCP_sources/{name}.csv", "w") as fh:
        fh.write("normalizedCapacity,voltage\n")
        np.savetxt(fh, np.column_stack([si_c, si_v]), delimiter=",", fmt="%.17g")

# ── 풀셀 워크북: 2행 헤더 + 상태 5개 컬럼쌍, NaN 꼬리 길이를 서로 다르게 ──
n = 300
cols = []
for si, st in enumerate(STATES):
    cap_end = 74.671 - 2.5 * si
    c = np.linspace(0, cap_end, n)
    v = 3.05 + 1.15 * (c / cap_end) ** 0.8 - 0.01 * si
    drop = si * 7                      # 상태마다 유효 길이를 다르게 → NaN 마스크 검사
    if drop:
        c = c.copy(); v = v.copy()
        c[-drop:] = np.nan; v[-drop:] = np.nan
    cols += [c, v]
M = np.column_stack(cols)
p = root / "data/full_cell/large_cell_033C/fullcell_states.xlsx"
with open(p, "w") as fh:
    fh.write(",".join(f"{s},{s}" for s in STATES) + "\n")
    fh.write(",".join(["mAh", "V"] * 5) + "\n")
    np.savetxt(fh, M, delimiter=",", fmt="%.17g")
# 걸러져야 하는 미끼 파일 둘 (이름에 pristine / 300cycle)
for decoy in ("pristine_raw.xlsx", "300cycle_dump.xlsx"):
    (root / "data/full_cell/large_cell_033C" / decoy).write_text("0,0\n1,1\n2,2\n")

print(f"wrote synthetic tree under {root}")
