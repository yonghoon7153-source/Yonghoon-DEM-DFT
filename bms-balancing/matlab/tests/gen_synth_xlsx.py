"""합성 **xlsx** 트리 — Python 쪽(`data.py` + `verify.py eval`)이 실제로 도는지 보려고.

`gen_synth_data.py` 는 Octave 대역품이 읽을 CSV 를 만든다. 이쪽은 같은 내용을
진짜 xlsx 로 써서 `bms_balancing.data` 의 적재 경로(2행 헤더·컬럼쌍·dropna)를
실제로 통과시킨다. 원자료가 없는 기계에서 **배관이 도는지**만 보는 용도다 —
여기서 나오는 수는 물리적으로 아무 뜻이 없다.
"""
import numpy as np, pandas as pd, pathlib, sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "synthxlsx")
for sub in ("data/half_cell/GITT", "data/half_cell/step_005C",
            "data/literature/Si_OCP_sources", "data/full_cell/large_cell_033C"):
    (root / sub).mkdir(parents=True, exist_ok=True)

STATES = ["pristine", "100", "200", "300_0009", "300_0147"]

for src, suf in (("GITT", ""), ("step_005C", "_005C")):
    for si, st in enumerate(STATES):
        n = 160
        pe_c = np.linspace(0, 1, n)
        ne_c = np.linspace(0, 1, n)
        # ⚠ 이 fixture 의 양극은 용량이 늘수록 전압이 **내려간다** → 방향
        #   정규화를 지나면 x 가 내림차순이 된다. **실제 파우치 자료는 반대**다
        #   (오름차순). 2026-09-10 에 `_interp_lin_extrap` 이 내림차순을 조용히
        #   틀리게 처리하던 버그가 여기서 안 드러난 이유이기도 하고, 원통형 셀을
        #   붙이고 나서야 드러난 이유이기도 하다. 방향을 일부러 양쪽 다 두어
        #   두 경로가 모두 밟히게 한다 (음극은 정규화 뒤 오름차순이다).
        pd.DataFrame({"PE_capacity": pe_c,
                      "PE_voltage": 4.25 - 0.85 * pe_c ** 1.3 - 0.004 * si,
                      "NE_capacity": ne_c,
                      "NE_voltage": 0.05 + 0.9 * (1 - ne_c) ** 2.1 + 0.003 * si}
                     ).to_excel(root / f"data/half_cell/{src}/{st}{suf}.xlsx", index=False)

# ⚠ Si 와 Gr 은 **모양이 서로 달라야** 한다. 둘 다 전압에 선형이면 Blend 의
#   min-max 정규화 뒤 두 곡선이 겹치고, 그러면 γ_Si 가 목적함수에 전혀 닿지
#   않는다 (2026-09-10 실측: max|Si-Gr| = 4.4e-16, γ=0.1 과 0.9 의 q 가 같았다).
#   그 상태로 두면 스모크가 블렌드 경로를 **통과한 척**만 한다.
n = 120
gr_v = np.linspace(0.02, 0.60, n)              # 흑연: 계단(스테이지) 모양
u = (gr_v - gr_v.min()) / (gr_v.max() - gr_v.min())
gr_c = 1.0 - (0.45 / (1 + np.exp(-(u - 0.13) / 0.020))
              + 0.33 / (1 + np.exp(-(u - 0.24) / 0.030))
              + 0.22 / (1 + np.exp(-(u - 0.52) / 0.120)))
gr_c = (gr_c - gr_c.min()) / (gr_c.max() - gr_c.min())
pd.DataFrame({"Gr_capacity": gr_c, "Gr_voltage": gr_v}).to_excel(
    root / "data/literature/Si_Gr_literature_OCP.xlsx", index=False)
for name, k in (("Baggetto",0.55),("Friedrich",0.70),("Jiang",0.85),("Kunz",1.00),
                ("Li",1.20),("Lu",1.45),("Sethuraman",1.75),("Wetjen",2.10)):
    si_v = np.linspace(0.05, 0.85, n)          # 실리콘: 완만한 한 덩이 경사
    t = (si_v - si_v.min()) / (si_v.max() - si_v.min())
    si_c = 1.0 - (0.5 * t ** k + 0.5 * (1 - np.cos(np.pi * t)) / 2)
    si_c = (si_c - si_c.min()) / (si_c.max() - si_c.min())
    pd.DataFrame({"normalizedCapacity": si_c, "voltage": si_v}).to_csv(
        root / f"data/literature/Si_OCP_sources/{name}.csv", index=False)

# ⚠ 풀셀 전압은 **평탄부(스테이지)가 있어야** 한다. 매끈한 단조 곡선이면
#   dQ/dV 에 봉우리가 하나도 안 생기고(`find_peaks` → 0개), 그러면 피크
#   가중이 전부 1 이 되어 **가중 경로가 무가중과 구별되지 않는다**. 그 상태로
#   두면 dQ/dV 대조가 통과한 척만 한다 (2026-09-10 실측: n_peaks=0 으로
#   test_py_smoke 의 "피크 가중이 무가중과 다르다" 가 처음부터 FAIL 이었다).
#   그래서 흑연 스테이지를 닮은 완만한 계단 둘을 넣는다. 진폭·폭은 기울기가
#   양수로 남도록 잡았다 (단조가 깨지면 `unique(v_smooth)` 가 점을 버린다).
def _stage(x, x0, w):
    return 1.0 / (1.0 + np.exp(-(x - x0) / w))


n, cols = 300, []
for si, st in enumerate(STATES):
    cap_end = 74.671 - 2.5 * si
    c = np.linspace(0, cap_end, n)
    x = c / cap_end
    v = (3.05 + 1.15 * x ** 0.8 - 0.01 * si
         - 0.060 * _stage(x, 0.30, 0.035) - 0.055 * _stage(x, 0.62, 0.040))
    drop = si * 7
    if drop:
        c, v = c.copy(), v.copy()
        c[-drop:] = np.nan; v[-drop:] = np.nan
    cols += [c, v]
M = np.column_stack(cols)
hdr = pd.DataFrame([sum(([s, s] for s in STATES), []), ["mAh", "V"] * 5])
body = pd.DataFrame(M)
with pd.ExcelWriter(root / "data/full_cell/large_cell_033C/fullcell_states.xlsx") as w:
    hdr.to_excel(w, index=False, header=False, startrow=0)
    body.to_excel(w, index=False, header=False, startrow=2)
print(f"wrote synthetic xlsx tree under {root}")
