"""interactive_ab.py — α·β 슬라이더 UI (로컬 전용, 서버 실행 경로에서 분리).

★ 02_CODE_AUDIT.md M2: 원본의 Slider/Button UI를 메인 경로에서 분리한 것.
headless 서버에서는 실행하지 말 것 (matplotlib 인터랙티브 백엔드 필요).

사용:
    python tools/interactive_ab.py --in results/sweep1d_v1
    (curves.parquet의 reference 곡선 위에서 α·β를 조작해 LAM/LLI를 읽는다)
"""

from __future__ import annotations

import sys
from pathlib import Path

# run.sh 없이 직접 실행해도 src/tools를 찾도록 (PYTHONPATH 미설정 대비)
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib.widgets import Button, Slider
from scipy.interpolate import interp1d

# 인터랙티브 전용 — Agg 강제하지 않음
import matplotlib.pyplot as plt  # noqa: E402

from src.curves import windowed_curve  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_path", required=True,
                    help="sweep1d 결과 디렉터리 (curves.parquet 포함)")
    args = ap.parse_args()

    p = Path(args.in_path)
    df = pd.read_parquet(p / "curves.parquet" if p.is_dir() else p)
    ref = df[df["mode"] == "reference"]
    x = ref["x_norm"].to_numpy()
    pe = ref["v_pe"].to_numpy()
    ne = ref["v_ne"].to_numpy()

    f_pe = interp1d(x, pe, bounds_error=False, fill_value=(pe[0], pe[-1]))
    f_ne = interp1d(x, ne, bounds_error=False, fill_value=(ne[0], ne[-1]))
    xg = np.linspace(0, 1, 300)

    fig, ax = plt.subplots(figsize=(9, 7))
    ax.plot(x, pe, "k-", lw=1.2, label="PE (ref.)")
    ax.plot(x, ne, "k--", lw=1.2, label="NE (ref.)")
    l_pe, = ax.plot(xg, windowed_curve(f_pe, xg, 1.0, 0.0), "tab:red", lw=1.8,
                    label="PE (recon.)")
    l_ne, = ax.plot(xg, windowed_curve(f_ne, xg, 1.0, 0.0), "tab:blue", lw=1.8,
                    label="NE (recon.)")
    l_fc, = ax.plot(xg, np.full_like(xg, np.nan), "k:", lw=1.5,
                    label="Full cell (recon.)")
    ax.set_xlabel("Normalized Capacity")
    ax.set_ylabel("Potential [V]")
    ax.legend(fontsize=8, loc="lower left")

    fig.subplots_adjust(bottom=0.34)
    axes = [fig.add_axes([0.12, y, 0.6, 0.03]) for y in (0.22, 0.17, 0.12, 0.07)]
    s_ape = Slider(axes[0], r"$\alpha_{PE}$", 0.5, 1.1, valinit=1.0, color="tab:red")
    s_bpe = Slider(axes[1], r"$\beta_{PE}$", -0.3, 0.3, valinit=0.0, color="tab:red")
    s_ane = Slider(axes[2], r"$\alpha_{NE}$", 0.5, 1.1, valinit=1.0, color="tab:blue")
    s_bne = Slider(axes[3], r"$\beta_{NE}$", -0.3, 0.3, valinit=0.0, color="tab:blue")
    btn = Button(fig.add_axes([0.8, 0.07, 0.12, 0.05]), "Reset")
    txt = fig.text(0.12, 0.005, "", fontsize=10)

    def update(_):
        a_pe, b_pe, a_ne, b_ne = s_ape.val, s_bpe.val, s_ane.val, s_bne.val
        y_pe = windowed_curve(f_pe, xg, a_pe, b_pe)
        y_ne = windowed_curve(f_ne, xg, a_ne, b_ne)
        l_pe.set_ydata(y_pe)
        l_ne.set_ydata(y_ne)
        l_fc.set_ydata(y_pe - y_ne)
        # 원본 부호 규약 (Birkl 2017): LLI = (1-a_PE) + (b_PE - b_NE)
        txt.set_text(
            f"LAM_PE = {(1-a_pe)*100:.1f}%   LAM_NE = {(1-a_ne)*100:.1f}%   "
            f"LLI = {((1-a_pe)+(b_pe-b_ne))*100:.1f}%")
        fig.canvas.draw_idle()

    for s in (s_ape, s_bpe, s_ane, s_bne):
        s.on_changed(update)
    btn.on_clicked(lambda _: [s.reset() for s in (s_ape, s_bpe, s_ane, s_bne)])
    update(None)
    plt.show()


if __name__ == "__main__":
    main()
