---
source_url: https://github.com/ImperialCollegeLondon/PyProBE
ingested: 2026-10-01
sha256: 1493085b26072e8663746952cff094a78db91225faacba85e2f45d04d9532119
---

수집 목적: 경쟁 도구 · 판정 대상 (일일 브리핑 ② 축) + 실험 아이디어 (④ 축) — 브리핑이 제안한 "OCV 와 DVA 로 각각 피팅하고 평활화 · 피팅 범위를 바꿔도 LLI/LAM 결론이 유지되는가" 를 **참값을 아는 우리 합성 truth** 로 PyProBE 에 대해 잰다. 사용자 승인 2026-10-01 ("ㅇㅇ 진행하고 관련해서 저장해두자").

# PyProBE 2.6.0 DMA 를 우리 PyBaMM 합성 truth 에 적용 (2026-10-01 실측)

## 조건 · 격리

- PyProBE 2.6.0 (`PyProBE-Data`, PyPI) 을 버리는 별도 venv 에 설치. 운영 환경 · 저장소 · 등록부에 쓰지 않았다 (읽기만: `results/grid_curves_v4/curves.parquet`, 쓴 것은 스크래치패드 JSON).
- 전극 OCP 표: 우리 `src.halfcell.compute_halfcell_from_ocp(configs/base.yaml)` (파라미터셋 OCP 함수를 화학량론 0~1 전 범위에서 평가 · 복합 음극은 Gr/Si 평형 분배 · Si 탈리튬화 가지) — `git archive 9ca6df54` 사본에서 만들어 `.npz` 로 넘김. PE 400 점 (u 2.487–5.678 V) · NE 800 점 (u 0.024–3.577 V) · 둘 다 단조.
- full-cell 곡선: grid_curves_v4 (protocol `charge_first` 0.05 C · 300 점 · DFN 동적 전압 — **평형 OCV 가 아니다**). x_norm 은 0 = 충전 끝 (4.16 V) → 1 = 방전 끝 (2.54 V) 이라 PyProBE 규약 (SOC 0 = 방전 끝) 으로 `SOC = 1 − x_norm` 뒤집어 넣었다 (첫 실행은 뒤집지 않아 전극 용량이 음수로 나왔다 — 비율은 같았지만 DE 의 하드코딩 bounds 가 무의미해져 다시 돌렸다).
- 용량 축: 참값 `q_mah` 를 그대로 준다 (`Capacity [Ah] = SOC · q`) — PyProBE 는 `Cell Capacity = ptp(Capacity)/ptp(SOC)` 로 쓴다. 즉 **절대 용량은 참값으로 알려 준 조건**이다.
- 조건 (noise 0): pristine (0,0,0) q 5621.07 mAh · LLI_only (0.10,0,0) · LAMNE_only (0,0,0.10) · mixed (0.10,0.10,0.10) · LAMPE_only = lli 0 · lam_ne 0 에서 있는 최대 lam_pe = **0.06** (완방 guard 로 저 LLI 코너의 고 LAM_PE 가 비어 있다). 노이즈: LLI_only 의 noise 0.001 · 0.005 (`v_full_noisy`) × Savitzky–Golay 없음 / 창 11 / 창 31 (차수 3).
- 피팅: `pyprobe.analysis.degradation_mode_analysis.run_ocv_curve_fit` (공개 API · `Result(lf=…)`) → `quantify_degradation_modes([pristine, degraded])`. target OCV / dVdQ × SOC 범위 [0,1] / [0.05,0.95] / [0.10,0.90] × 초기값 8 (PyProBE 기본 x0 = [0.9, 0.1, 0.1, 0.9] + 균일 난수 7, seed 20261001) · 최적화 `minimize` (bounds [0,1]⁴). 추가로 `differential_evolution` 1 회 — PyProBE 가 bounds 를 **[(0.75,0.95),(0.2,0.3),(0,0.05),(0.85,0.95)] 로 하드코딩** 한다 (`analysis/base/degradation_mode_analysis_functions.py` `ocv_curve_fit`).
- truth 창: 각 조건의 `v_pe` · `v_ne` (DFN 전극 전위 · 0.05 C 과전압 포함) 를 평형 OCP 표로 역보간한 화학량론 — 참값 창의 근사.
- 전체 8.5 s.

## 결과 (summarize.py 출력 원문)

```
pristine fit (OCV, default x0): {'x_pe low SOC': 0.9372, 'x_pe high SOC': 0.2769, 'x_ne low SOC': 0.0021, 'x_ne high SOC': 0.8936, 'Cell Capacity [Ah]': 5.6211, 'Cathode Capacity [Ah]': 8.5126, 'Anode Capacity [Ah]': 6.3056, 'Li Inventory [Ah]': 7.9916} rmse 10.03 mV
pristine truth window: {'x_pe_lo': 0.9287, 'x_pe_hi': 0.281, 'x_ne_lo': 0.0021, 'x_ne_hi': 0.9782}

== LLI_only_0.10  truth LLI=0.100 LAM_pe=0.000 LAM_ne=0.000 SOH=0.8769
   truth window {'x_pe_lo': 0.8369, 'x_pe_hi': 0.2685, 'x_ne_lo': 0.0021, 'x_ne_hi': 0.8664}
   default OCV fit: LLI=0.1011 LAM_pe=0.0032 LAM_ne=-0.0183 SOH=0.8769 rmse=12.75 mV  limits={'x_pe low SOC': 0.845, 'x_pe high SOC': 0.264, 'x_ne low SOC': 0.002, 'x_ne high SOC': 0.77}
   OCV   [0.0, 1.0]: n=8 LLI [+0.101,+0.101] LAM_pe [+0.003,+0.003] LAM_ne [-0.018,-0.018] | rmse mV [12.75,12.75] | best-rmse: LLI=+0.101 LAM_pe=+0.003 LAM_ne=-0.018
   OCV   [0.05, 0.95]: n=8 LLI [+0.033,+0.105] LAM_pe [-0.515,+0.002] LAM_ne [-1.882,-0.012] | rmse mV [9.37,23.10] | best-rmse: LLI=+0.105 LAM_pe=+0.001 LAM_ne=-0.013
   OCV   [0.1, 0.9]: n=8 LLI [+0.044,+0.102] LAM_pe [-0.529,-0.006] LAM_ne [-2.027,-0.010] | rmse mV [8.70,18.91] | best-rmse: LLI=+0.102 LAM_pe=-0.006 LAM_ne=-0.010
   dVdQ  [0.0, 1.0]: n=8 LLI [-13.920,+0.116] LAM_pe [-0.492,+0.216] LAM_ne [-30.818,+0.213] | rmse mV [24.21,166.20] | best-rmse: LLI=+0.116 LAM_pe=+0.068 LAM_ne=+0.177
   dVdQ  [0.05, 0.95]: n=8 LLI [-0.047,+0.113] LAM_pe [-0.468,+0.042] LAM_ne [+0.081,+0.218] | rmse mV [18.20,157.05] | best-rmse: LLI=+0.110 LAM_pe=+0.042 LAM_ne=+0.152
   dVdQ  [0.1, 0.9]: n=8 LLI [-0.209,+0.126] LAM_pe [-0.428,+0.280] LAM_ne [-0.778,+0.208] | rmse mV [18.18,242.65] | best-rmse: LLI=+0.097 LAM_pe=+0.029 LAM_ne=+0.118
   DE (hard-coded bounds): {'SOH': 0.8769, 'LAM_pe': 0.0046, 'LAM_ne': -0.0149, 'LLI': 0.1015} rmse 12.75

== LAMNE_only_0.10  truth LLI=0.000 LAM_pe=0.000 LAM_ne=0.100 SOH=0.9236
   truth window {'x_pe_lo': 0.9288, 'x_pe_hi': 0.3304, 'x_ne_lo': 0.0021, 'x_ne_hi': 0.9936}
   default OCV fit: LLI=0.0045 LAM_pe=0.0067 LAM_ne=0.1016 SOH=0.9236 rmse=11.11 mV  limits={'x_pe low SOC': 0.939, 'x_pe high SOC': 0.326, 'x_ne low SOC': 0.002, 'x_ne high SOC': 0.919}
   OCV   [0.0, 1.0]: n=8 LLI [-0.080,+0.005] LAM_pe [-0.635,+0.009] LAM_ne [-2.650,+0.106] | rmse mV [11.11,39.72] | best-rmse: LLI=+0.004 LAM_pe=+0.007 LAM_ne=+0.102
   OCV   [0.05, 0.95]: n=8 LLI [-0.078,-0.005] LAM_pe [-0.731,-0.016] LAM_ne [-3.020,+0.095] | rmse mV [9.44,25.58] | best-rmse: LLI=-0.006 LAM_pe=-0.016 LAM_ne=+0.095
   OCV   [0.1, 0.9]: n=8 LLI [-0.332,-0.010] LAM_pe [-1.128,-0.026] LAM_ne [-2.321,+0.095] | rmse mV [8.46,22.85] | best-rmse: LLI=-0.010 LAM_pe=-0.026 LAM_ne=+0.095
   dVdQ  [0.0, 1.0]: n=8 LLI [-3.785,+0.063] LAM_pe [-0.440,+0.348] LAM_ne [-8.708,+0.170] | rmse mV [72.67,267.39] | best-rmse: LLI=-0.045 LAM_pe=-0.167 LAM_ne=+0.167
   dVdQ  [0.05, 0.95]: n=8 LLI [-0.090,+0.069] LAM_pe [-0.461,-0.052] LAM_ne [+0.044,+0.177] | rmse mV [77.34,265.55] | best-rmse: LLI=-0.090 LAM_pe=-0.263 LAM_ne=+0.177
   dVdQ  [0.1, 0.9]: n=8 LLI [-0.217,+0.090] LAM_pe [-0.434,+0.237] LAM_ne [-0.735,+0.177] | rmse mV [27.16,208.96] | best-rmse: LLI=+0.013 LAM_pe=-0.011 LAM_ne=+0.177
   DE (hard-coded bounds): {'SOH': 0.9236, 'LAM_pe': 0.006, 'LAM_ne': 0.098, 'LLI': 0.0044} rmse 11.11

== mixed_0.10_0.10_0.10  truth LLI=0.100 LAM_pe=0.100 LAM_ne=0.100 SOH=0.8991
   truth window {'x_pe_lo': 0.9289, 'x_pe_hi': 0.2815, 'x_ne_lo': 0.0021, 'x_ne_hi': 0.9776}
   default OCV fit: LLI=0.1008 LAM_pe=0.1014 LAM_ne=0.0955 SOH=0.8991 rmse=10.68 mV  limits={'x_pe low SOC': 0.938, 'x_pe high SOC': 0.277, 'x_ne low SOC': 0.002, 'x_ne high SOC': 0.888}
   OCV   [0.0, 1.0]: n=8 LLI [+0.004,+0.101] LAM_pe [-0.466,+0.101] LAM_ne [-2.160,+0.096] | rmse mV [10.68,39.50] | best-rmse: LLI=+0.101 LAM_pe=+0.101 LAM_ne=+0.096
   OCV   [0.05, 0.95]: n=8 LLI [+0.017,+0.099] LAM_pe [-0.542,+0.094] LAM_ne [-2.592,+0.101] | rmse mV [9.40,25.91] | best-rmse: LLI=+0.099 LAM_pe=+0.094 LAM_ne=+0.101
   OCV   [0.1, 0.9]: n=8 LLI [+0.032,+0.093] LAM_pe [-0.556,+0.083] LAM_ne [-2.778,+0.102] | rmse mV [8.67,20.64] | best-rmse: LLI=+0.093 LAM_pe=+0.083 LAM_ne=+0.101
   dVdQ  [0.0, 1.0]: n=8 LLI [-4.105,+0.239] LAM_pe [-0.350,+0.364] LAM_ne [-9.449,+0.193] | rmse mV [49.45,244.08] | best-rmse: LLI=+0.077 LAM_pe=+0.011 LAM_ne=+0.143
   dVdQ  [0.05, 0.95]: n=8 LLI [-0.007,+0.080] LAM_pe [-0.398,-0.008] LAM_ne [+0.078,+0.198] | rmse mV [38.23,245.98] | best-rmse: LLI=+0.057 LAM_pe=-0.008 LAM_ne=+0.181
   dVdQ  [0.1, 0.9]: n=8 LLI [+0.089,+0.131] LAM_pe [-0.434,+0.130] LAM_ne [+0.073,+0.198] | rmse mV [12.83,282.79] | best-rmse: LLI=+0.108 LAM_pe=+0.130 LAM_ne=+0.198
   DE (hard-coded bounds): {'SOH': 0.8991, 'LAM_pe': 0.101, 'LAM_ne': 0.0953, 'LLI': 0.1005} rmse 10.68

== LAMPE_only_max  truth LLI=0.000 LAM_pe=0.060 LAM_ne=0.000 SOH=1.0093
   truth window {'x_pe_lo': 0.9856, 'x_pe_hi': 0.2903, 'x_ne_lo': 0.0039, 'x_ne_hi': 0.9866}
   default OCV fit: LLI=-0.0055 LAM_pe=0.0440 LAM_ne=-0.0006 SOH=1.0093 rmse=8.59 mV  limits={'x_pe low SOC': 0.985, 'x_pe high SOC': 0.288, 'x_ne low SOC': 0.003, 'x_ne high SOC': 0.902}
   OCV   [0.0, 1.0]: n=8 LLI [-0.014,-0.006] LAM_pe [+0.021,+0.044] LAM_ne [-0.061,-0.001] | rmse mV [8.59,9.28] | best-rmse: LLI=-0.006 LAM_pe=+0.044 LAM_ne=-0.001
   OCV   [0.05, 0.95]: n=8 LLI [-0.087,-0.005] LAM_pe [-0.669,+0.044] LAM_ne [-3.385,+0.023] | rmse mV [7.57,24.96] | best-rmse: LLI=-0.005 LAM_pe=+0.044 LAM_ne=+0.023
   OCV   [0.1, 0.9]: n=8 LLI [-0.283,-0.009] LAM_pe [-0.942,+0.035] LAM_ne [-2.595,+0.021] | rmse mV [7.24,29.19] | best-rmse: LLI=-0.009 LAM_pe=+0.035 LAM_ne=+0.021
   dVdQ  [0.0, 1.0]: n=8 LLI [-4.374,+0.142] LAM_pe [-0.500,+0.283] LAM_ne [-9.916,+0.095] | rmse mV [83.66,262.09] | best-rmse: LLI=-0.029 LAM_pe=-0.107 LAM_ne=+0.047
   dVdQ  [0.05, 0.95]: n=8 LLI [-0.171,-0.025] LAM_pe [-0.602,-0.130] LAM_ne [-0.033,+0.100] | rmse mV [62.80,268.77] | best-rmse: LLI=-0.073 LAM_pe=-0.130 LAM_ne=+0.048
   dVdQ  [0.1, 0.9]: n=8 LLI [-0.095,+0.042] LAM_pe [-0.430,-0.020] LAM_ne [-0.083,+0.100] | rmse mV [51.09,210.62] | best-rmse: LLI=-0.095 LAM_pe=-0.169 LAM_ne=-0.083
   DE (hard-coded bounds): {'SOH': 1.0093, 'LAM_pe': 0.044, 'LAM_ne': -0.0005, 'LLI': -0.0055} rmse 8.59

== noise (LLI_only 0.10 · truth LLI 0.10)
   noise=0.001 savgol=None: OCV LLI=+0.101 LAM_pe=+0.004 LAM_ne=-0.018 rmse=12.9mV | dVdQ LLI=+0.026 LAM_pe=-0.243 LAM_ne=+0.209 rmse=105.1mV
   noise=0.001 savgol=11: OCV LLI=+0.101 LAM_pe=+0.003 LAM_ne=-0.018 rmse=12.8mV | dVdQ LLI=+0.026 LAM_pe=-0.244 LAM_ne=+0.211 rmse=103.5mV
   noise=0.001 savgol=31: OCV LLI=+0.101 LAM_pe=+0.003 LAM_ne=-0.018 rmse=12.5mV | dVdQ LLI=-0.008 LAM_pe=-0.306 LAM_ne=+0.207 rmse=108.9mV
   noise=0.005 savgol=None: OCV LLI=+0.100 LAM_pe=-0.001 LAM_ne=-0.022 rmse=14.0mV | dVdQ LLI=+0.008 LAM_pe=-0.276 LAM_ne=+0.209 rmse=105.9mV
   noise=0.005 savgol=11: OCV LLI=+0.100 LAM_pe=-0.001 LAM_ne=-0.022 rmse=13.2mV | dVdQ LLI=+0.002 LAM_pe=-0.288 LAM_ne=+0.210 rmse=105.9mV
   noise=0.005 savgol=31: OCV LLI=+0.100 LAM_pe=-0.001 LAM_ne=-0.023 rmse=12.8mV | dVdQ LLI=+0.004 LAM_pe=-0.283 LAM_ne=+0.208 rmse=106.8mV

wall_s 8.5
```

(rmse 는 모든 행에서 **전압 RMSE** — dVdQ target 의 적합이라도 전압으로 환산해 적었다. `[a,b]` 는 8 초기값에 걸친 최솟값 · 최댓값. "best-rmse" 는 그 8 개 중 전압 RMSE 최소인 답.)

전체 결과 JSON (모든 적합의 화학량론 창 · 용량 · DMA · rmse): 같은 폴더 `2026-10-01-pyprobe-dma-on-synthetic-truth.results.json`.

## 실험 스크립트 (pyprobe_dma_exp.py — 실행한 그대로)

```python
"""PyProBE 판정 대상 실험 (2026-10-01 · 브리핑 후속 B).

우리 PyBaMM 합성 truth (참값을 아는 full-cell 곡선, results/grid_curves_v4 · 읽기만) 를 PyProBE 의 OCV 피팅
(`run_ocv_curve_fit` → `quantify_degradation_modes`) 에 넣어
  (1) 참값 LLI · LAM 을 되찾는가
  (2) 초기값 · 피팅 target(OCV / dVdQ) · SOC 범위 · 노이즈에 따라 답이 얼마나 흔들리는가 (flat valley)
  (3) 적합된 화학량론 창이 truth 창 (v_pe · v_ne 를 OCP 표로 역보간) 과 맞는가
를 잰다. 쓰는 것은 argv[1] 디렉터리의 JSON · MD 뿐. 저장소 · 등록부에는 아무 것도 쓰지 않는다.
"""
import itertools
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl

import pyprobe
from pyprobe.analysis import degradation_mode_analysis as dma
from pyprobe.result import Result

REPO = Path("/home/user/Yonghoon-DEM-DFT/degradation-degeneracy")
PARQ = REPO / "results/grid_curves_v4/curves.parquet"
REF = Path(sys.argv[2])
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)

ref = np.load(REF)
ocp_pe = dma.OCP.from_data(ref["y_pe"], ref["u_pe"])
ocp_ne = dma.OCP.from_data(ref["z_ne"], ref["u_ne"])


def truth_window(v_pe, v_ne):
    """DFN 전극 전위 (0.05 C · 과전압 포함) 를 평형 OCP 표로 역보간한 화학량론 — 참값 창의 근사. 입력은 SOC 오름차순 (lo = 방전 끝)."""
    y, u = ref["y_pe"], ref["u_pe"]          # u 감소 → 뒤집어 보간
    z, w = ref["z_ne"], ref["u_ne"]
    xpe = np.interp(v_pe, u[::-1], y[::-1]); xne = np.interp(v_ne, w[::-1], z[::-1])
    return dict(x_pe_lo=float(xpe[0]), x_pe_hi=float(xpe[-1]), x_ne_lo=float(xne[0]), x_ne_hi=float(xne[-1]))


def make_result(soc, v, q_mah):
    """soc 는 full-cell SOC (0 = 방전 끝 · 1 = 충전 끝) — PyProBE 의 lo/hi 규약과 같다."""
    o = np.argsort(soc)
    df = pl.DataFrame({"Voltage [V]": np.asarray(v, float)[o], "Capacity [Ah]": np.asarray(soc, float)[o] * q_mah / 1000.0,
                       "SOC": np.asarray(soc, float)[o]})
    return Result(lf=df.lazy(), info={})


def fit(res, target="OCV", x0=(0.9, 0.1, 0.1, 0.9), optimizer="minimize"):
    opts = {"x0": np.array(x0), "bounds": [(0, 1)] * 4} if optimizer == "minimize" else {"bounds": [(0, 1)] * 4}
    lim, fitted = dma.run_ocv_curve_fit(res, ocp_pe, ocp_ne, fitting_target=target, optimizer=optimizer, optimizer_options=opts)
    d = lim.data.to_dicts()[0]
    f = fitted.data
    rmse = float(np.sqrt(np.mean((f["Fitted Voltage [V]"].to_numpy() - f["Input Voltage [V]"].to_numpy()) ** 2)))
    return lim, {k: float(d[k]) for k in ("x_pe low SOC", "x_pe high SOC", "x_ne low SOC", "x_ne high SOC",
                                           "Cell Capacity [Ah]", "Cathode Capacity [Ah]", "Anode Capacity [Ah]", "Li Inventory [Ah]")}, rmse


def dma_of(lim0, lim1):
    q = dma.quantify_degradation_modes([lim0, lim1]).data.to_dicts()[1]
    return {k: float(q[k]) for k in ("SOH", "LAM_pe", "LAM_ne", "LLI")}


def main():
    t0 = time.time()
    cols = ["cond_id", "lli", "lam_pe", "lam_ne", "noise", "q_mah", "x_norm", "v_pe", "v_ne", "v_full", "v_full_noisy"]
    df = pd.read_parquet(PARQ, columns=cols)
    conds = df.drop_duplicates("cond_id")[["cond_id", "lli", "lam_pe", "lam_ne", "noise", "q_mah"]]
    z = conds[conds.noise == 0]

    def pick(lli, pe, ne):
        r = z[(z.lli == lli) & (z.lam_pe == pe) & (z.lam_ne == ne)]
        return None if r.empty else r.iloc[0]
    # LAM_PE 단독은 완방 guard 로 저 LLI 코너가 비어 있다 — lli=0 · lam_ne=0 에서 있는 최대 lam_pe 를 고른다
    pe_only = z[(z.lli == 0) & (z.lam_ne == 0) & (z.lam_pe > 0)].sort_values("lam_pe")
    cases = {"pristine": pick(0, 0, 0), "LLI_only_0.10": pick(0.10, 0, 0), "LAMNE_only_0.10": pick(0, 0, 0.10),
             "mixed_0.10_0.10_0.10": pick(0.10, 0.10, 0.10)}
    cases["LAMPE_only_max"] = None if pe_only.empty else pe_only.iloc[-1]
    cases = {k: v for k, v in cases.items() if v is not None}

    def curve(cid, noisy=False):
        """★ grid 곡선은 x_norm 0 = 충전 끝(4.16 V) → 1 = 방전 끝(2.54 V) 순서다 (v_pe · v_ne 끝값으로 확인).
        PyProBE 규약 (SOC 0 = 방전 끝) 으로 뒤집어 돌려준다. v_pe · v_ne 도 같은 순서로 뒤집는다."""
        r = df[df.cond_id == cid].sort_values("x_norm")
        soc = 1.0 - r.x_norm.to_numpy()
        v = (r.v_full_noisy if noisy else r.v_full).to_numpy()
        return soc[::-1], v[::-1], r.v_pe.to_numpy()[::-1], r.v_ne.to_numpy()[::-1], float(r.q_mah.iloc[0])

    out = {"pyprobe": pyprobe.__version__, "parquet": str(PARQ), "ref_npz": str(REF), "cases": {}, "notes": []}
    # ── 기준: pristine
    xn, v, vpe, vne, q0 = curve(cases["pristine"].cond_id)
    res0 = make_result(xn, v, q0)
    lim0, d0, rmse0 = fit(res0)
    out["cases"]["pristine"] = {"cond": cases["pristine"].to_dict(), "truth_window": truth_window(vpe, vne),
                                "fit_OCV_default_x0": d0, "rmse_V": rmse0}
    # ── 열화 조건: target × 초기값 다중 시작 × SOC 범위
    rng = np.random.default_rng(20261001)
    starts = [(0.9, 0.1, 0.1, 0.9)] + [tuple(rng.uniform(0, 1, 4)) for _ in range(7)]
    for name, c in cases.items():
        if name == "pristine":
            continue
        xn, v, vpe, vne, q = curve(c.cond_id)
        truth = {"LLI": float(c.lli), "LAM_pe": float(c.lam_pe), "LAM_ne": float(c.lam_ne), "SOH": q / q0}
        rec = {"cond": c.to_dict(), "truth": truth, "truth_window": truth_window(vpe, vne), "fits": []}
        for target in ("OCV", "dVdQ"):
            for lo, hi in ((0.0, 1.0), (0.05, 0.95), (0.10, 0.90)):
                m = (xn >= lo) & (xn <= hi)
                res = make_result(xn[m], v[m], q)  # 용량은 참값 그대로 준다 (SOC 열을 주므로 PyProBE 가 ptp 로 정규화)
                for i, x0 in enumerate(starts):
                    try:
                        lim, d, rmse = fit(res, target, x0)
                        rec["fits"].append({"target": target, "soc_range": [lo, hi], "start": i, "x0": list(map(float, x0)),
                                            "limits": d, "rmse_V": rmse, "dma": dma_of(lim0, lim)})
                    except Exception as e:  # noqa: BLE001
                        rec["fits"].append({"target": target, "soc_range": [lo, hi], "start": i, "error": f"{type(e).__name__}: {e}"})
        # differential_evolution — PyProBE 가 bounds 를 **하드코딩** 한다 (base 함수 기준 [(0.75,0.95),(0.2,0.3),(0,0.05),(0.85,0.95)])
        try:
            lim, d, rmse = fit(make_result(xn, v, q), "OCV", optimizer="differential_evolution")
            rec["fit_DE"] = {"limits": d, "rmse_V": rmse, "dma": dma_of(lim0, lim)}
        except Exception as e:  # noqa: BLE001
            rec["fit_DE"] = {"error": f"{type(e).__name__}: {e}"}
        out["cases"][name] = rec
    # ── 노이즈 변형 (LLI_only 0.10 · noise 0.001 · 0.005) — 평활화 없음 ↔ Savitzky–Golay
    from scipy.signal import savgol_filter
    nz = conds[(conds.lli == 0.10) & (conds.lam_pe == 0) & (conds.lam_ne == 0) & (conds.noise > 0)]
    out["noise"] = []
    for _, c in nz.iterrows():
        xn, v, vpe, vne, q = curve(c.cond_id, noisy=True)
        for smooth in (None, 11, 31):
            vv = v if smooth is None else savgol_filter(v, smooth, 3)
            row = {"noise": float(c.noise), "savgol_window": smooth, "fits": {}}
            for target in ("OCV", "dVdQ"):
                try:
                    lim, d, rmse = fit(make_result(xn, vv, q), target)
                    row["fits"][target] = {"dma": dma_of(lim0, lim), "rmse_V": rmse}
                except Exception as e:  # noqa: BLE001
                    row["fits"][target] = {"error": f"{type(e).__name__}: {e}"}
            out["noise"].append(row)
    out["wall_s"] = time.time() - t0
    (OUT / "pyprobe_dma_results.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"pyprobe": out["pyprobe"], "wall_s": round(out["wall_s"], 1), "cases": list(out["cases"]),
                      "pristine_fit": d0, "pristine_truth": out["cases"]["pristine"]["truth_window"], "rmse0": rmse0}, ensure_ascii=False))


if __name__ == "__main__":
    main()
```

(해석은 raw 가 아니라 위키 페이지 `entities/pyprobe.md` · 질문 카드 `22p-physics-or-degeneracy` 에 둔다.)
