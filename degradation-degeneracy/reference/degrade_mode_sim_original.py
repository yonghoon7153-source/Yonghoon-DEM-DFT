import os
import timeit
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.widgets import Slider, Button
from scipy.interpolate import interp1d
import matplotlib.ticker as ticker

import pybamm
# pybamm.set_logging_level("INFO")
plt.rcParams.update({
    'font.family':          'Arial',
    'font.size':            11,
    'axes.linewidth':       1.0,
    'xtick.direction':      'in',
    'ytick.direction':      'in',
    'xtick.major.size':     4,
    'ytick.major.size':     4,
    'xtick.minor.visible':  False,
    'ytick.minor.visible':  False,
    'xtick.top':            False,
    'ytick.right':          False,
    'legend.frameon':       False,
    'legend.fontsize':      9,
    'axes.facecolor':       'white',
    'figure.facecolor':     'white',
    'mathtext.fontset':     'stix',
})
os.chdir(pybamm.__path__[0] + "/..")

start = timeit.default_timer()
model = pybamm.lithium_ion.DFN(
    {
        "particle phases": ("2", "1"),
        "open-circuit potential": (("single", "current sigmoid"), "single"),
    }
)
param = pybamm.ParameterValues("Chen2020_composite")


param.update(
    {
        "Upper voltage cut-off [V]": 4.2,
        "Lower voltage cut-off [V]": 2.5,
        # 전극 두께는 손대지 않음 -> Chen2020_composite 기본값 그대로 사용됨
        # (기본값: Negative current collector 1.2e-05 m, Negative electrode 8.52e-05 m,
        #          Positive electrode 7.56e-05 m, Positive current collector 1.6e-05 m)
    }
)
experiment = (
    [
        "Discharge at 0.05 C until 2.5 V",
        "Rest for 10 minutes",
        "Charge at 0.05 C until 4.2 V",
        "Rest for 10 minutes",
        "Discharge at 0.05 C until 2.5 V",
    ]
)
experiment2 = (
    [
        "Charge at 0.05 C until 4.2 V",
        "Rest for 10 minutes",
        "Discharge at 0.05 C until 2.5 V",
    ]
)

def initialization():
    param.update(
        {
            "Primary: Initial concentration in negative electrode [mol.m-3]": 27700.0,
            "Primary: Maximum concentration in negative electrode [mol.m-3]": 28700.0,
            "Secondary: Initial concentration in negative electrode [mol.m-3]": 276610.0,
            "Secondary: Maximum concentration in negative electrode [mol.m-3]": 278000.0,
            "Initial concentration in positive electrode [mol.m-3]": 17038.0,
            "Negative electrode porosity": 0.25,
            "Primary: Negative electrode active material volume fraction": 0.735,
            "Secondary: Negative electrode active material volume fraction": 0.015,
            "Positive electrode porosity": 0.335,
            "Positive electrode active material volume fraction": 0.665,
        }
    )

initialization()  # 완충 기준 초기상태로 세팅

sim_discharge = pybamm.Simulation(
    model,
    parameter_values=param,
    experiment=pybamm.Experiment(["Discharge at 0.05C until 2.5V", "Discharge at 2.5 V until 0.02 C"]),
)
sol_discharge = sim_discharge.solve()

c_gr = sol_discharge["Average negative primary particle concentration [mol.m-3]"].entries
c_si = sol_discharge["Average negative secondary particle concentration [mol.m-3]"].entries
c_pe = sol_discharge["Average positive particle concentration [mol.m-3]"].entries

print(f"방전 후 흑연 농도: {c_gr[-1]:.1f} mol/m3 "
      f"(x = {c_gr[-1]/28700:.4f})")
print(f"방전 후 Si 농도:   {c_si[-1]:.1f} mol/m3 "
      f"(x = {c_si[-1]/278000:.4f})")
print(f"방전 후 양극 농도: {c_pe[-1]:.1f} mol/m3 "
      f"(y = {c_pe[-1]/63104:.4f})")

# initialization()

C_rate = 0.05
capacity = param["Nominal cell capacity [A.h]"]
I_load = C_rate * capacity

# t_eval = [0, 100000]

param["Current function [A]"] = I_load

def run_sweep(experiment, sweep_values, update_fn):
    """
    sweep_values : 반복할 값 리스트 (예: LLI 리스트)
    update_fn    : 값 하나(i)를 받아서 param.update에 넣을 딕셔너리를 반환하는 함수
    """
    solutions = []
    for i in sweep_values:
        param.update(update_fn(i))
        print(i)
        sim = pybamm.Simulation(model, parameter_values=param, experiment=experiment)
        solutions.append(sim.solve())
        initialization()
    return solutions

sim_ref = pybamm.Simulation(model, parameter_values=param, experiment=experiment)
solution_ref = [sim_ref.solve()]
initialization()  # 다음 sweep 위해 리셋

LLI = [0, 0.1, 0.2, 0.3]
solution_LLI = run_sweep(
    experiment, LLI,
    update_fn=lambda i: {
        "Primary: Initial concentration in negative electrode [mol.m-3]": 27700 * (1 - i),
        "Secondary: Initial concentration in negative electrode [mol.m-3]": 276610 * (1 - i),
    },
)

# --- 진단: Reference와 LLI=0(동일 파라미터여야 함)이 실제로 같은 용량인지 확인 ---
_ref_step_dbg = solution_ref[0].cycles[-1].steps[-1]
_lli0_step_dbg = solution_LLI[0].cycles[-1].steps[-1]
_ref_cap_dbg = np.abs(_ref_step_dbg["Discharge capacity [A.h]"].entries -
                       _ref_step_dbg["Discharge capacity [A.h]"].entries[0])[-1] * 1000
_lli0_cap_dbg = np.abs(_lli0_step_dbg["Discharge capacity [A.h]"].entries -
                        _lli0_step_dbg["Discharge capacity [A.h]"].entries[0])[-1] * 1000
print(f"[진단] Reference 실측 용량 = {_ref_cap_dbg:.4f} mAh, "
      f"LLI=0 실측 용량 = {_lli0_cap_dbg:.4f} mAh, "
      f"차이 = {abs(_ref_cap_dbg - _lli0_cap_dbg):.4f} mAh "
      f"({'동일 시뮬레이션인데 값이 다름 -> 진짜 버그' if abs(_ref_cap_dbg-_lli0_cap_dbg) > 1e-2 else '일치'})")

initialization()

# ====================================================================
# 주의: baseline(초기농도/부피분율)이 바뀌었으므로, 아래 LAM_ne_de/LAM_pe_li/LAM_ne_li에서
# 쓰는 "완방 상태" 하드코딩 값(428, 82591, 62877.0)은 예전(잘못된) baseline 기준으로
# 뽑았던 값이라 더 이상 정확하지 않음. 아래 코드로 다시 뽑아서 교체해야 함:
#
# sim_discharge = pybamm.Simulation(
#     model, parameter_values=param,
#     experiment=pybamm.Experiment(["Discharge at 0.05C until 2.5V"]),
# )
# sol_discharge = sim_discharge.solve()
# c_gr = sol_discharge["Average negative primary particle concentration [mol.m-3]"].entries[-1]
# c_si = sol_discharge["Average negative secondary particle concentration [mol.m-3]"].entries[-1]
# c_pe = sol_discharge["Average positive particle concentration [mol.m-3]"].entries[-1]
# print(f"흑연 완방농도={c_gr:.1f}, Si 완방농도={c_si:.1f}, 양극 완방농도={c_pe:.1f}")
# initialization()  # 되돌리기 잊지 말 것
# ====================================================================

LAM_pe_de = [0, 0.1, 0.2, 0.3]
solution_LAM_pe_de = run_sweep(
    experiment, LAM_pe_de,
    update_fn=lambda i: {
        "Positive electrode porosity": 0.335+0.665*i,
        "Positive electrode active material volume fraction": 0.665*(1-i),
        "Initial concentration in positive electrode [mol.m-3]": 17038.0 / (1-i),
    },
)

LAM_ne_de = [0, 0.1, 0.2, 0.3]
solution_LAM_ne_de = run_sweep(
    experiment2, LAM_ne_de,
    update_fn=lambda i: {
        "Negative electrode porosity": 0.25+(0.735+0.015)*i,
        "Primary: Negative electrode active material volume fraction": 0.735*(1-i),
        "Secondary: Negative electrode active material volume fraction": 0.015*(1-i),
        "Primary: Initial concentration in negative electrode [mol.m-3]": 36.7 / (1-i),
        "Secondary: Initial concentration in negative electrode [mol.m-3]": 3446.3 / (1-i),
        "Initial concentration in positive electrode [mol.m-3]": 58439.9,
    },
)

LAM_pe_li = [0, 0.1, 0.2, 0.3]
solution_LAM_pe_li = run_sweep(
    experiment2, LAM_pe_li,
    update_fn=lambda i: {
        "Positive electrode porosity": 0.335+0.665*i,
        "Positive electrode active material volume fraction": 0.665*(1-i),
        "Primary: Initial concentration in negative electrode [mol.m-3]": 36.7,
        "Secondary: Initial concentration in negative electrode [mol.m-3]": 3446.3,
        "Initial concentration in positive electrode [mol.m-3]": 58439.9,
    },
)

LAM_ne_li = [0, 0.1, 0.2, 0.3]
solution_LAM_ne_li = run_sweep(
    experiment, LAM_ne_li,
    update_fn=lambda i: {
        "Negative electrode porosity": 0.25+(0.735+0.015)*i,
        "Primary: Negative electrode active material volume fraction": 0.735*(1-i),
        "Secondary: Negative electrode active material volume fraction": 0.015*(1-i),
    },
)

# 파라미터 및 solution 저장
with open(r"C:\Users\ga117\OneDrive\!BML\python\params.txt", "w", encoding="utf-8") as f:
    for k, v in param.items():
        f.write(f"{k}: {v}\n")
with open(r"C:\Users\ga117\OneDrive\!BML\python\variable_names.txt", "w", encoding="utf-8") as f:
    for name in model.variable_names():
        f.write(name + "\n")
print("저장 완료")



ltype = ["k-", "r--", "b-.", "g:", "m-", "c--", "y-."]

fig = plt.figure(figsize=(16, 10))

def plot_ocp(solution_list, value_list, label_name, norm_cap=None, ax=None, show_fullcell=True):
    if ax is None:
        ax = plt.gca()

    for i in range(len(value_list)):
        step = solution_list[i].cycles[-1].steps[-1]

        cap = step["Discharge capacity [A.h]"].entries * 1000
        cap = np.abs(cap - cap[0])
        if norm_cap is not None:
            cap = cap / norm_cap

        ocp_ne = step["Battery negative electrode bulk open-circuit potential [V]"].entries
        ocp_pe = step["X-averaged positive electrode open-circuit potential [V]"].entries

        color = ltype[i][0]
        ax.plot(cap, ocp_ne, color + "-", label=f"{label_name}={value_list[i]}")
        ax.plot(cap, ocp_pe, color + "-")

        if show_fullcell and i == 0:  # 0% 풀셀 곡선 (회색 점선)
            ax.plot(cap, ocp_pe - ocp_ne, color="gray", linestyle=":", lw=1.5,
                    label=f"Full cell ({value_list[i]})")
        if show_fullcell and i == len(value_list) - 1:  # 최대 열화(0.3) 풀셀 곡선 (검정 파선)
            ax.plot(cap, ocp_pe - ocp_ne, "k--", lw=1.5,
                    label=f"Full cell ({value_list[i]})")

    ax.set_xlabel("Normalized Capacity" if norm_cap is not None else "Capacity [mAh]")
    ax.set_ylabel("Potential [V]")
    ax.legend()
    ax.set_title(label_name)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:g}"))

ref_step = solution_ref[0].cycles[-1].steps[-1]
ref_cap = ref_step["Discharge capacity [A.h]"].entries * 1000
Q_ref = np.abs(ref_cap - ref_cap[0])[-1]

# ====================================================================
# 각 그래프 데이터를 엑셀로 export (시트 하나 = subplot 하나)
# ====================================================================
def _extract_columns(solution_list, value_list, label_name):
    """한 그룹(예: LLI 전체)의 데이터를 {열이름: Series} 딕셔너리로 반환"""
    data = {}
    for i, v in enumerate(value_list):
        step = solution_list[i].cycles[-1].steps[-1]
        cap = step["Discharge capacity [A.h]"].entries * 1000
        cap = np.abs(cap - cap[0]) / Q_ref
        ocp_ne = step["Battery negative electrode bulk open-circuit potential [V]"].entries
        ocp_pe = step["X-averaged positive electrode open-circuit potential [V]"].entries
        data[f"NormCap_{label_name}={v}"] = pd.Series(cap)
        data[f"PE[V]_{label_name}={v}"] = pd.Series(ocp_pe)
        data[f"NE[V]_{label_name}={v}"] = pd.Series(ocp_ne)
        data[f"FullCell[V]_{label_name}={v}"] = pd.Series(ocp_pe - ocp_ne)
    return data


excel_groups = {
    "Reference": (solution_ref, [0], "Ref"),
    "LLI": (solution_LLI, LLI, "LLI"),
    "LAM_ne_li": (solution_LAM_ne_li, LAM_ne_li, "LAM_ne_li"),
    "LAM_ne_de": (solution_LAM_ne_de, LAM_ne_de, "LAM_ne_de"),
    "LAM_pe_li": (solution_LAM_pe_li, LAM_pe_li, "LAM_pe_li"),
    "LAM_pe_de": (solution_LAM_pe_de, LAM_pe_de, "LAM_pe_de"),
}

_excel_path = r"C:\Users\ga117\OneDrive\!BML\python\degradation_data.xlsx"
with pd.ExcelWriter(_excel_path, engine="openpyxl") as _writer:
    for sheet_name, (sol_list, val_list, label_name) in excel_groups.items():
        _df = pd.DataFrame(_extract_columns(sol_list, val_list, label_name))
        _df.to_excel(_writer, sheet_name=sheet_name[:31], index=False)
print(f"엑셀 저장 완료: {_excel_path}")

ax_ref = plt.subplot(2, 3, 1)
ax_ref.set_xlabel("Normalized Capacity")
ax_ref.set_ylabel("Potential [V]")
ax_ref.set_title("Reference")
ax_ref.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:g}"))
plt.subplot(2, 3, 2)
plot_ocp(solution_LLI, LLI, "LLI", norm_cap=Q_ref)
plt.subplot(2, 3, 3)
plot_ocp(solution_LAM_ne_li, LAM_ne_li, "LAM$_{ne,li}$", norm_cap=Q_ref)
plt.subplot(2, 3, 4)
plot_ocp(solution_LAM_ne_de, LAM_ne_de, "LAM$_{ne,de}$", norm_cap=Q_ref)
plt.subplot(2, 3, 5)
plot_ocp(solution_LAM_pe_li, LAM_pe_li, "LAM$_{pe,li}$", norm_cap=Q_ref)
plt.subplot(2, 3, 6)
plot_ocp(solution_LAM_pe_de, LAM_pe_de, "LAM$_{pe,de}$", norm_cap=Q_ref)


# ====================================================================
# Reference subplot(ax_ref)에 α/β 슬라이더로 windowing 적용
# -> 관측 범위(x0_ref~x100_ref, y0_ref~y100_ref) 안: 실제 시뮬레이션 데이터 사용
#    (alpha=1,beta=0일 때 실제 곡선과 정확히 일치 보장)
# -> 관측 범위 밖: raw OCP 파라미터 함수 사용, 단 경계에서 실측값과
#    관측 범위 밖은 확장하지 않고 그냥 안 보이게(NaN) 처리
# ====================================================================
ref_cap_norm = np.abs(ref_cap - ref_cap[0]) / Q_ref
ref_ne = ref_step["Battery negative electrode bulk open-circuit potential [V]"].entries
ref_pe = ref_step["X-averaged positive electrode open-circuit potential [V]"].entries

# 전압 cutoff 이벤트 직전 마지막 몇 포인트는 solver가 다시 맞추는 과정에서
# 미세하게 튀는 경우가 있어서 끝단 n_trim개를 잘라내고 보간
n_trim = 3
ref_cap_norm_trim = ref_cap_norm[:-n_trim]
ref_pe_trim = ref_pe[:-n_trim]
ref_ne_trim = ref_ne[:-n_trim]

f_pe_ref = interp1d(ref_cap_norm_trim, ref_pe_trim, bounds_error=False,
                     fill_value=(ref_pe_trim[0], ref_pe_trim[-1]))
f_ne_ref = interp1d(ref_cap_norm_trim, ref_ne_trim, bounds_error=False,
                     fill_value=(ref_ne_trim[0], ref_ne_trim[-1]))


def windowed_curve(f_ref, x_cell_norm, alpha, beta):
    """alpha/beta로 window를 옮긴 뒤, 창 밖으로 나간 구간은 NaN 처리해서
    x축과 평행한 인위적인 평평한 선이 그려지지 않게 함"""
    sto = (x_cell_norm - beta) / alpha
    y = f_ref(np.clip(sto, 0, 1))
    y = np.where((sto >= 0) & (sto <= 1), y, np.nan)
    return y


x_cell_norm = np.linspace(0, 1, 300)

# 정적 reference 곡선 (검정, 실선/점선)
ax_ref.plot(ref_cap_norm_trim, ref_pe_trim, "k-", lw=1.2, label="PE (ref.)")
ax_ref.plot(ref_cap_norm_trim, ref_ne_trim, "k--", lw=1.2, label="NE (ref.)")

# 재구성 곡선 (동적, 슬라이더로 조절) - alpha=1,beta=0이면 위 검정 곡선과 정확히 겹침
l_pe_recon, = ax_ref.plot(x_cell_norm, windowed_curve(f_pe_ref, x_cell_norm, 1.0, 0.0),
                           color="tab:red", lw=1.8, label="PE (recon.)")
l_ne_recon, = ax_ref.plot(x_cell_norm, windowed_curve(f_ne_ref, x_cell_norm, 1.0, 0.0),
                           color="tab:blue", lw=1.8, label="NE (recon.)")
l_fc_recon, = ax_ref.plot(x_cell_norm, np.full_like(x_cell_norm, np.nan),
                           color="k", lw=1.5, linestyle=":", label="Full cell (recon.)")

ax_ref.legend(fontsize=6, loc="lower left")

# 슬라이더/버튼/텍스트 넣을 공간 확보
fig.subplots_adjust(bottom=0.32, hspace=0.5, wspace=0.3)

ax_aPE = fig.add_axes([0.06, 0.22, 0.32, 0.02])
ax_bPE = fig.add_axes([0.06, 0.18, 0.32, 0.02])
ax_aNE = fig.add_axes([0.06, 0.14, 0.32, 0.02])
ax_bNE = fig.add_axes([0.06, 0.10, 0.32, 0.02])
ax_btn = fig.add_axes([0.06, 0.03, 0.10, 0.04])

s_aPE = Slider(ax_aPE, r"$\alpha_{PE}$", 0.5, 1.0, valinit=1.0, color="tab:red")
s_bPE = Slider(ax_bPE, r"$\beta_{PE}$", -0.3, 0.3, valinit=0.0, color="tab:red")
s_aNE = Slider(ax_aNE, r"$\alpha_{NE}$", 0.5, 1.0, valinit=1.0, color="tab:blue")
s_bNE = Slider(ax_bNE, r"$\beta_{NE}$", -0.3, 0.3, valinit=0.0, color="tab:blue")
btn_reset = Button(ax_btn, "Reset", color="#f0f0f0", hovercolor="#d0d0d0")

txt_lam = fig.text(0.20, 0.03, "", fontsize=11,
                    bbox=dict(boxstyle="round", facecolor="white", edgecolor="gray"))


def _update_slider(_):
    a_pe, b_pe = s_aPE.val, s_bPE.val
    a_ne, b_ne = s_aNE.val, s_bNE.val

    y_pe = windowed_curve(f_pe_ref, x_cell_norm, a_pe, b_pe)
    y_ne = windowed_curve(f_ne_ref, x_cell_norm, a_ne, b_ne)

    if _ is None:  # 초기 렌더링(기본값 alpha=1,beta=0) 시에만 진단 출력
        n_nan_pe = np.sum(np.isnan(y_pe))
        n_nan_ne = np.sum(np.isnan(y_ne))
        print(f"[진단] 기본값(alpha=1,beta=0)에서 NaN 개수: PE={n_nan_pe}, NE={n_nan_ne} "
              f"(둘 다 0이어야 정상)")
        if n_nan_pe > 0:
            idx = np.where(np.isnan(y_pe))[0]
            print(f"       PE NaN 위치(x_cell_norm): {x_cell_norm[idx[:5]]} ...")
        if n_nan_ne > 0:
            idx = np.where(np.isnan(y_ne))[0]
            print(f"       NE NaN 위치(x_cell_norm): {x_cell_norm[idx[:5]]} ...")

    l_pe_recon.set_ydata(y_pe)
    l_ne_recon.set_ydata(y_ne)
    l_fc_recon.set_ydata(y_pe - y_ne)  # 둘 중 하나라도 NaN이면 자동으로 NaN

    LAM_PE = (1 - a_pe) * 100
    LAM_NE = (1 - a_ne) * 100
    # Birkl et al. 2017 (J. Power Sources 341, Eq.7-10) 기반: 순수 LLI일 때
    # beta_PE는 양의 방향, beta_NE는 음의 방향으로 움직여야 함
    # (NE가 EoD에서 pristine보다 더 탈리튬화되는 방향, PE는 EoC에서 더 delithiated)
    # -> LLI = (1-alpha_PE) + (beta_PE - beta_NE)  (기존 부호가 반대였음)
    LLI = ((1 - a_pe) + (b_pe - b_ne)) * 100

    txt_lam.set_text(
        rf"LAM$_{{PE}}$ = {LAM_PE:.1f}%    LAM$_{{NE}}$ = {LAM_NE:.1f}%    "
        rf"LLI = {LLI:.1f}%"
    )
    fig.canvas.draw_idle()


def _reset(_):
    for _s in (s_aPE, s_bPE, s_aNE, s_bNE):
        _s.reset()


for _s in (s_aPE, s_bPE, s_aNE, s_bNE):
    _s.on_changed(_update_slider)
btn_reset.on_clicked(_reset)

_update_slider(None)

plt.show()