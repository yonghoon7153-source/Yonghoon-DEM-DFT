---
source_url: https://github.com/NatLabRockies/ampworks
ingested: 2026-10-05
sha256: 37e30513aa589a4c57a0874a5d568108f62394789c3c66d3b845a7e678eb2232
---

수집 목적: 경쟁 도구 · 판정 대상 (일일 브리핑 ② 축) — 2026-10-05 사용자 승인 "ㄱㄱ" (판정 실험 A1–A3 은 버리는 venv 에서만 · upstream 알림은 초안만 · 발송은 사용자).

---

# ampworks 0.2.0.dev0 (main 0f7a31c6) 를 우리 PyBaMM 합성 truth 에 적용 — A1–A3 (2026-10-05 실측) + upstream 예제 자료 재현

## 조건 · 격리

- ampworks: `NatLabRockies/ampworks` main `0f7a31c62cc89d8e8aac3bf1068e56044fed2bd7` 를 스크래치패드의 버리는 venv 에 설치 (0.2.0.dev0 ·
  설치본 `_lam_lli.py` sha256 `ccbd3c5bf53d5d7ca67632ed4212e5147cf5eef705823f1b662e5cca4c6947b4` · 설치본 `src/ampworks` 는 clone 과 파일 동일).
  Python 3.11.15 · numpy 2.4.6 · scipy 1.17.1 · pandas 3.0.6 · numdifftools 0.11.1 · 재현 시험용 pytest 9.1.1 (같은 venv). 운영 환경 · 저장소 ·
  등록부에는 설치 · 쓰기 0 (읽기만: 아래 parquet).
- 곡선: `degradation-degeneracy/artifacts/grid_curves_v4/curves.parquet` (sha256 `b69dc7bee0bb2e32aba73b6ace91255d964bceb41f9361886de7275bf48aa8b8` —
  스크립트가 시작 때 대조) · noise 0 · pristine + LLI 단독 0.10 · LAM_NE 단독 0.10 · 혼합 0.10/0.10/0.10 · LAM_PE 단독 (있는 최대 0.06).
- 반쪽전지 OCP: `git archive f27006370 degradation-degeneracy/src degradation-degeneracy/configs` 를 풀어
  `compute_halfcell_from_ocp(load_config("configs/base.yaml"))` → npz (`y_pe` · `u_pe` · `z_ne` · `u_ne` · sha256
  `9f606a6f2cce6ff589ead366489decf0edc695a5d1ebd92b582b9941f204ac39`).
- 피팅: 비용 항 4 (all = voltage + dqdv + dvdq 기본값 · voltage · dqdv · dvdq) × 경로 2 (carry = pristine 적합 창 이어받기 · grid =
  `grid_search(21)`) · 경로마다 `constrained_fit` 2 회 → `calc_lam_lli`. A2 는 설치본 `_lam_lli.py` 의 108행만 `xp1_std` 로 바꾼 사본 (줄 diff 를
  결과 JSON `identity.line_diff` 에 남김). A3 은 같은 Hessian 으로 전체 공분산 전파 (+ 기준 행 불확도 포함판).
- 결과 JSON (이 파일 옆 · 바이트 그대로): `2026-10-05-ampworks-on-synthetic-truth.results.json` sha256 `bad4f3fa201155ac40664c2ea47546503f39c601f7d33e98133c352f929fcb61` · `2026-10-05-ampworks-on-synthetic-truth.passes.json` sha256 `ee283fdc0d7f1ba1b86ffeba09dbf6254c1a56f7d12be9dcfed2fbdda6607d81`.
- 시간: A1–A3 293 s · 보충 (재시작 반복) 129 s · upstream 재현 네 판 112 s · Hessian 16 s.

## 결과 A1–A3 (summarize.py 출력 원문)

```text
identity: {'ampworks': '0.2.0.dev0', 'numpy': '2.4.6', 'pandas': '3.0.6', 'parquet': '/home/user/Yonghoon-DEM-DFT/degradation-degeneracy/artifacts/grid_curves_v4/curves.parquet', 'parquet_sha256': 'b69dc7bee0bb2e32aba73b6ace91255d964bceb41f9361886de7275bf48aa8b8', 'ref_npz_sha256': '9f606a6f2cce6ff589ead366489decf0edc695a5d1ebd92b582b9941f204ac39', 'installed_file': '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/a45978e3-3a6e-5e3d-af55-7c9b61e0d809/scratchpad/amp_venv/lib/python3.11/site-packages/ampworks/dqdv/_lam_lli.py', 'installed_sha256': 'ccbd3c5bf53d5d7ca67632ed4212e5147cf5eef705823f1b662e5cca4c6947b4'}
line_diff: [{'line': 108, 'before': '        + (((1. - xp0)*dQp)*xn1_std)**2         # contribution from xp1', 'after': '        + (((1. - xp0)*dQp)*xp1_std)**2         # contribution from xp1'}]
wall_s: 293.1

cases: {'pristine': {'lli': 0.0, 'lam_pe': 0.0, 'lam_ne': 0.0, 'lam_pe_type': 'de', 'lam_ne_type': 'de', 'q_mah': 5621.073220520553}, 'LLI_only_0.10': {'lli': 0.1, 'lam_pe': 0.0, 'lam_ne': 0.0, 'lam_pe_type': 'de', 'lam_ne_type': 'de', 'q_mah': 4929.232595557144}, 'LAMNE_only_0.10': {'lli': 0.0, 'lam_pe': 0.0, 'lam_ne': 0.1, 'lam_pe_type': 'de', 'lam_ne_type': 'de', 'q_mah': 5191.540711559133}, 'mixed_0.10_0.10_0.10': {'lli': 0.1, 'lam_pe': 0.1, 'lam_ne': 0.1, 'lam_pe_type': 'de', 'lam_ne_type': 'de', 'q_mah': 5054.161474110272}, 'LAMPE_only_max': {'lli': 0.0, 'lam_pe': 0.06, 'lam_ne': 0.0, 'lam_pe_type': 'de', 'lam_ne_type': 'de', 'q_mah': 5673.286135134836}}

== A1 참값 복원 (est − truth, 백분율 포인트) · fun = ampworks 목적함수 (MAPE 합) · 경로 carry = pristine 창 이어받기 · grid = grid_search(21)
cost     case                   path        fun |     LLI   LAMpe   LAMne |    dLLI  dLAMpe  dLAMne
all      pristine                        0.1168 | x = [0.0032, 0.9548, 0.0711, 0.7153, 0.0002] · truth_window ≈ {'xn0': 0.0021, 'xn1': 0.9782, 'xp0': 0.0713, 'xp1': 0.719}
all      LLI_only_0.10          carry_   0.3271 |   13.24   10.07    7.79 |   +3.24  +10.07   +7.79
all      LLI_only_0.10          grid21   0.5781 |   -5.67   -7.76   -0.73 |  -15.67   -7.76   -0.73
all      LAMNE_only_0.10        carry_   0.1229 |    0.14    0.27   10.68 |   +0.14   +0.27   +0.68
all      LAMNE_only_0.10        grid21   0.1229 |    0.14    0.28   10.68 |   +0.14   +0.28   +0.68
all      mixed_0.10_0.10_0.10   carry_   0.1184 |    9.99    9.96   10.17 |   -0.01   -0.04   +0.17
all      mixed_0.10_0.10_0.10   grid21   0.1196 |    9.97    9.97   10.09 |   -0.03   -0.03   +0.09
all      LAMPE_only_max         carry_   0.1195 |    0.02    6.03    0.43 |   +0.02   +0.03   +0.43
all      LAMPE_only_max         grid21   0.1195 |    0.01    6.00    0.44 |   +0.01   -0.00   +0.44
voltage  pristine                        0.0023 | x = [0.0021, 0.8626, 0.0493, 0.7137, -0.0178] · truth_window ≈ {'xn0': 0.0021, 'xn1': 0.9782, 'xp0': 0.0713, 'xp1': 0.719}
voltage  LLI_only_0.10          carry_   0.0029 |   10.86   -0.06    4.34 |   +0.86   -0.06   +4.34
voltage  LLI_only_0.10          grid21   0.0029 |   10.66   -0.50    3.39 |   +0.66   -0.50   +3.39
voltage  LAMNE_only_0.10        carry_   0.0025 |   -0.93   -1.87   10.43 |   -0.93   -1.87   +0.43
voltage  LAMNE_only_0.10        grid21   0.0025 |   -0.81   -2.25   13.10 |   -0.81   -2.25   +3.10
voltage  mixed_0.10_0.10_0.10   carry_   0.0025 |    9.75    8.39   12.95 |   -0.25   -1.61   +2.95
voltage  mixed_0.10_0.10_0.10   grid21   0.0025 |    9.74    8.51   12.96 |   -0.26   -1.49   +2.96
voltage  LAMPE_only_max         carry_   0.0019 |   -0.65    2.51    4.24 |   -0.65   -3.49   +4.24
voltage  LAMPE_only_max         grid21   0.0019 |   -0.51    3.05    4.94 |   -0.51   -2.95   +4.94
dqdv     pristine                        0.0702 | x = [0.0029, 0.9563, 0.0703, 0.7154, 0.0] · truth_window ≈ {'xn0': 0.0021, 'xn1': 0.9782, 'xp0': 0.0713, 'xp1': 0.719}
dqdv     LLI_only_0.10          carry_   0.0714 |    9.78   -0.18   -0.53 |   -0.22   -0.18   -0.53
dqdv     LLI_only_0.10          grid21   0.0714 |    9.78   -0.18   -0.53 |   -0.22   -0.18   -0.53
dqdv     LAMNE_only_0.10        carry_   0.0715 |    0.16    0.27   10.70 |   +0.16   +0.27   +0.70
dqdv     LAMNE_only_0.10        grid21   0.0715 |    0.17    0.27   10.70 |   +0.17   +0.27   +0.70
dqdv     mixed_0.10_0.10_0.10   carry_   0.0727 |    9.95    9.93   10.08 |   -0.05   -0.07   +0.08
dqdv     mixed_0.10_0.10_0.10   grid21   0.0727 |    9.96    9.97   10.08 |   -0.04   -0.03   +0.08
dqdv     LAMPE_only_max         carry_   0.0740 |   -0.04    5.92    0.54 |   -0.04   -0.08   +0.54
dqdv     LAMPE_only_max         grid21   0.0740 |   -0.03    5.95    0.50 |   -0.03   -0.05   +0.50
dvdq     pristine                        0.0400 | x = [0.0026, 0.9553, 0.072, 0.7153, 0.0] · truth_window ≈ {'xn0': 0.0021, 'xn1': 0.9782, 'xp0': 0.0713, 'xp1': 0.719}
dvdq     LLI_only_0.10          carry_   0.0459 |    9.82   -0.13   -0.53 |   -0.18   -0.13   -0.53
dvdq     LLI_only_0.10          grid21   0.1814 |    2.57   -4.89  -36.61 |   -7.43   -4.89  -36.61
dvdq     LAMNE_only_0.10        carry_   0.0466 |   -0.11    0.04   10.08 |   -0.11   +0.04   +0.08
dvdq     LAMNE_only_0.10        grid21   0.0466 |   -0.10    0.06   10.10 |   -0.10   +0.06   +0.10
dvdq     mixed_0.10_0.10_0.10   carry_   0.0435 |    9.96   10.07    9.93 |   -0.04   +0.07   -0.07
dvdq     mixed_0.10_0.10_0.10   grid21   0.0435 |    9.96   10.06    9.93 |   -0.04   +0.06   -0.07
dvdq     LAMPE_only_max         carry_   0.0420 |    0.01    6.14    0.14 |   +0.01   +0.14   +0.14
dvdq     LAMPE_only_max         grid21   0.0420 |    0.02    6.16    0.16 |   +0.02   +0.16   +0.16

== A2 LLI_std: 원본 (108행 xn1_std) ↔ 고친 사본 (xp1_std) · 다른 열은 같은가
cost     case                   path   |      orig     fixed   ratio |   xn1_std   xp1_std | others_same
all      LLI_only_0.10          carry_ |    0.4959    0.5357   0.926 |  5.80e-05  1.47e-03 | True
all      LLI_only_0.10          grid21 |    3.9074    3.9828   0.981 |  6.64e-05  3.83e-03 | True
all      LAMNE_only_0.10        carry_ |    1.1214    1.9088   0.587 |  8.63e-04  9.29e-03 | True
all      LAMNE_only_0.10        grid21 |    1.0959    1.8397   0.596 |  8.29e-04  8.88e-03 | True
all      mixed_0.10_0.10_0.10   carry_ |    0.5472    0.5748   0.952 |  4.69e-04  1.34e-03 | True
all      mixed_0.10_0.10_0.10   grid21 |    0.5615    0.5778   0.972 |  9.31e-04  1.35e-03 | True
all      LAMPE_only_max         carry_ |    0.0186    0.0791   0.235 |  1.08e-04  5.46e-04 | True
all      LAMPE_only_max         grid21 |    0.0992    0.2176   0.456 |  6.62e-04  1.50e-03 | True
voltage  LLI_only_0.10          carry_ |   66.0711   14.9464   4.421 |  4.26e-01  6.41e-02 | True
voltage  LLI_only_0.10          grid21 |   19.8267   14.0392   1.412 |  1.13e-01  6.74e-02 | True
voltage  LAMNE_only_0.10        carry_ |  120.4148   19.2771   6.247 |  7.18e-01  1.07e-01 | True
voltage  LAMNE_only_0.10        grid21 |  115.8816   17.3526   6.678 |  6.90e-01  9.57e-02 | True
voltage  mixed_0.10_0.10_0.10   carry_ |   81.2503   15.2404   5.331 |  5.86e-01  9.66e-02 | True
voltage  mixed_0.10_0.10_0.10   grid21 |   82.0390   15.3247   5.353 |  5.92e-01  9.74e-02 | True
voltage  LAMPE_only_max         carry_ |   95.6214   17.8619   5.353 |  6.52e-01  1.06e-01 | True
voltage  LAMPE_only_max         grid21 |   91.4525   16.4715   5.552 |  6.28e-01  1.00e-01 | True
dqdv     LLI_only_0.10          carry_ |    2.3563    1.6010   1.472 |  1.10e-02  1.58e-03 | True
dqdv     LLI_only_0.10          grid21 |    2.3562    1.6011   1.472 |  1.10e-02  1.58e-03 | True
dqdv     LAMNE_only_0.10        carry_ |    5.0197    3.0461   1.648 |  2.53e-02  8.31e-03 | True
dqdv     LAMNE_only_0.10        grid21 |    5.0982    3.0620   1.665 |  2.58e-02  8.34e-03 | True
dqdv     mixed_0.10_0.10_0.10   carry_ |    3.8513    3.2911   1.170 |  1.44e-02  1.72e-03 | True
dqdv     mixed_0.10_0.10_0.10   grid21 |    3.8532    3.2933   1.170 |  1.44e-02  1.72e-03 | True
dqdv     LAMPE_only_max         carry_ |    2.1092    1.8843   1.119 |  6.61e-03  5.37e-04 | True
dqdv     LAMPE_only_max         grid21 |    1.9326    1.8259   1.058 |  4.46e-03  7.13e-04 | True
dvdq     LLI_only_0.10          carry_ |    1.1293    1.2357   0.914 |  8.36e-05  3.14e-03 | True
dvdq     LLI_only_0.10          grid21 |    2.4314    1.4781   1.645 |  1.18e-02  3.28e-03 | True
dvdq     LAMNE_only_0.10        carry_ |    1.5296    1.9701   0.776 |  7.88e-04  7.43e-03 | True
dvdq     LAMNE_only_0.10        grid21 |    1.5246    1.9677   0.775 |  7.99e-04  7.45e-03 | True
dvdq     mixed_0.10_0.10_0.10   carry_ |    0.9637    1.0655   0.904 |  7.45e-04  3.34e-03 | True
dvdq     mixed_0.10_0.10_0.10   grid21 |    0.9658    1.0675   0.905 |  7.39e-04  3.34e-03 | True
dvdq     LAMPE_only_max         carry_ |    0.3268    0.6445   0.507 |  2.17e-03  4.43e-03 | True
dvdq     LAMPE_only_max         grid21 |    0.3261    0.6419   0.508 |  2.17e-03  4.41e-03 | True
ratio original/fixed: min 0.235 · median 1.089 · max 6.678 (n 32)

== A3 불확도 (백분율 포인트): ampworks 대각 (108행 고침) ↔ 전체 공분산 (기준 행 정확) ↔ 전체 + 기준 행 불확도 · 참값 오차와 비교
cost     case                   path   |  |dLLI|    diag    full  full+0 | |dLAMn|    diag    full | |dLAMp|    diag    full |   min eig  neg | corr(xn0,xp0) corr(xn1,xp1) corr(xp0,xp1)
all      LLI_only_0.10          carry_ |   3.243   0.536   0.647   0.900 |   7.789   0.014   0.170 |  10.066   1.732   1.863 | -3.55e+05    1 | +0.029 -1.547 -0.651
all      LLI_only_0.10          grid21 |  15.667   3.983     nan     nan |   0.726   0.008   0.046 |   7.758   9.431     nan | -6.52e+06    3 | +0.380 -0.904 -0.965
all      LAMNE_only_0.10        carry_ |   0.140   1.909   2.186   2.301 |   0.678   0.106   0.200 |   0.274   3.464   3.830 | -2.50e+05    0 | +0.180 -0.479 -0.277
all      LAMNE_only_0.10        grid21 |   0.141   1.840   2.042   2.165 |   0.682   0.119   0.207 |   0.277   3.370   3.601 | -2.50e+05    0 | +0.101 -0.393 -0.179
all      mixed_0.10_0.10_0.10   carry_ |   0.015   0.575   0.664   0.928 |   0.171   0.046   0.196 |   0.043   1.781   1.886 | -2.51e+05    0 | -0.534 -0.570 -0.574
all      mixed_0.10_0.10_0.10   grid21 |   0.028   0.578   0.663   0.928 |   0.088   0.088   0.289 |   0.027   1.791   1.897 | -1.21e+05    1 | -4.452 -0.577 -0.580
all      LAMPE_only_max         carry_ |   0.018   0.079     nan     nan |   0.434   0.011   0.052 |   0.026   0.081   0.086 | -4.08e+06    3 | -4.276 +2.977 -2.917
all      LAMPE_only_max         grid21 |   0.008   0.218   0.214   0.752 |   0.444   0.068   0.096 |   0.001   0.221   0.216 | -3.23e+06    0 | +0.534 -0.055 +0.061
voltage  LLI_only_0.10          carry_ |   0.856  14.946   5.862  12.846 |   4.340  53.977  44.049 |   0.061  21.705  20.793 | -1.48e+01    1 | +1.443 +0.282 +0.094
voltage  LLI_only_0.10          grid21 |   0.657  14.039   7.550  13.720 |   3.390  14.618     nan |   0.496  34.659  28.415 | -3.58e+01    1 | +0.112 -0.376 +0.517
voltage  LAMNE_only_0.10        carry_ |   0.931  19.277  19.057  23.037 |   0.429  73.052  71.743 |   1.870  20.678  25.123 | -1.64e+01    1 | +4.366 +0.690 -0.559
voltage  LAMNE_only_0.10        grid21 |   0.811  17.353  18.775  22.795 |   3.099  65.929  65.565 |   2.250  19.673  25.921 | -1.86e+01    1 | +4.061 +0.651 -0.794
voltage  mixed_0.10_0.10_0.10   carry_ |   0.252  15.240  12.115  16.755 |   2.950  58.185  56.389 |   1.606  15.277  18.195 | -1.64e+01    1 | +4.283 +0.600 -0.513
voltage  mixed_0.10_0.10_0.10   grid21 |   0.258  15.325  12.232  16.839 |   2.958  58.802  57.036 |   1.485  15.347  18.305 | -1.64e+01    1 | +4.256 +0.605 -0.519
voltage  LAMPE_only_max         carry_ |   0.653  17.862  21.400  24.991 |   4.243  69.720  74.489 |   3.493  18.330  23.905 | -2.14e+01    0 | +3.330 +0.635 -0.748
voltage  LAMPE_only_max         grid21 |   0.512  16.472  19.528  23.398 |   4.939  66.037  69.960 |   2.949  17.657  23.330 | -2.08e+01    0 | +3.625 +0.603 -0.775
dqdv     LLI_only_0.10          carry_ |   0.216   1.601   1.520   3.734 |   0.527   2.665   2.689 |   0.178   2.518   2.703 |  0.00e+00    0 | -0.198 +0.229 -0.688
dqdv     LLI_only_0.10          grid21 |   0.216   1.601   1.520   3.734 |   0.528   2.665   2.689 |   0.178   2.518   2.703 |  0.00e+00    0 | -0.198 +0.229 -0.688
dqdv     LAMNE_only_0.10        carry_ |   0.164   3.046   2.603   4.585 |   0.702   3.224   3.934 |   0.267   6.221   7.005 |  0.00e+00    0 | -0.586 -0.454 -0.617
dqdv     LAMNE_only_0.10        grid21 |   0.167   3.062   2.611   4.589 |   0.703   3.263   3.992 |   0.272   6.258   7.050 |  0.00e+00    0 | -0.591 -0.461 -0.621
dqdv     mixed_0.10_0.10_0.10   carry_ |   0.050   3.291   3.399   4.811 |   0.083   4.916   5.340 |   0.066   0.424     nan | -1.81e+04    1 | +0.984 +0.457 +4.665
dqdv     mixed_0.10_0.10_0.10   grid21 |   0.038   3.293   3.401   4.812 |   0.079   4.919   5.344 |   0.030   0.423     nan | -1.81e+04    1 | +0.985 +0.456 +4.673
dqdv     LAMPE_only_max         carry_ |   0.044   1.884   1.795   4.186 |   0.541   2.559   2.463 |   0.084   2.243   2.163 | -2.95e+04    1 | -0.150 +3.466 +1.039
dqdv     LAMPE_only_max         grid21 |   0.032   1.826   1.806   4.191 |   0.504   2.458   2.108 |   0.053   2.031   1.917 | -4.73e+03    2 | -0.044 +4.440 +1.102
dvdq     LLI_only_0.10          carry_ |   0.184   1.236   1.304   1.811 |   0.534   0.069     nan |   0.131   3.893   3.980 | -9.03e+04    1 | -0.068 +0.466 -0.160
dvdq     LLI_only_0.10          grid21 |   7.427   1.478   1.594   2.094 |  36.607   2.656   2.450 |   4.887   4.573   4.731 | -1.43e+05    1 | +0.101 -0.063 -0.254
dvdq     LAMNE_only_0.10        carry_ |   0.113   1.970   0.833   1.625 |   0.083   0.076   0.196 |   0.037   4.412   4.037 | -2.61e+05    2 | -0.187 +0.169 +0.005
dvdq     LAMNE_only_0.10        grid21 |   0.100   1.968   0.823   1.620 |   0.103   0.077   0.196 |   0.063   4.399   4.024 | -2.60e+05    2 | -0.186 +0.164 +0.003
dvdq     mixed_0.10_0.10_0.10   carry_ |   0.037   1.065   1.171   1.716 |   0.067   0.071   0.201 |   0.074   3.155   3.279 | -2.59e+05    0 | -0.557 -0.285 -0.275
dvdq     mixed_0.10_0.10_0.10   grid21 |   0.042   1.068   1.173   1.718 |   0.068   0.071   0.201 |   0.064   3.162   3.287 | -2.59e+05    0 | -0.561 -0.285 -0.276
dvdq     LAMPE_only_max         carry_ |   0.013   0.644   0.626   1.528 |   0.136   0.226   0.309 |   0.144   0.670   0.649 | -3.61e+05    0 | +0.547 -0.084 +0.079
dvdq     LAMPE_only_max         grid21 |   0.018   0.642   0.635   1.532 |   0.160   0.226   0.307 |   0.157   0.668   0.679 | -3.61e+05    0 | +0.469 +0.037 -0.042

std_reproduced_max_abs_diff (ampworks x_std 와 이 스크립트가 같은 식으로 다시 만든 std 의 차 — 0 이면 같은 공분산): 0.0
```

## 보충 — 결과에서 다시 시작하는 constrained_fit 반복 (amp_exp_passes.py 출력 원문)

```text
2026-10-05T00:38:10Z
all pristine fun 0.1151
  pass  1 fun 0.1664 LLI  10.12 LAMpe   0.87 LAMne   2.35
  pass  2 fun 0.1175 LLI   9.86 LAMpe  -0.06 LAMne  -0.30
  pass  3 fun 0.1227 LLI   9.82 LAMpe  -0.07 LAMne  -0.40
  pass  4 fun 0.1228 LLI   9.82 LAMpe  -0.07 LAMne  -0.40
  pass  5 fun 0.1227 LLI   9.82 LAMpe  -0.06 LAMne  -0.41
  pass  6 fun 0.1227 LLI   9.82 LAMpe  -0.06 LAMne  -0.40
  pass  7 fun 0.1228 LLI   9.82 LAMpe  -0.08 LAMne  -0.41
  pass  8 fun 0.1176 LLI   9.83 LAMpe  -0.15 LAMne  -0.29
  pass  9 fun 0.1181 LLI   9.83 LAMpe  -0.10 LAMne  -0.33
  pass 10 fun 0.1227 LLI   9.82 LAMpe  -0.08 LAMne  -0.40
  pass 11 fun 0.1227 LLI   9.82 LAMpe  -0.08 LAMne  -0.40
  pass 12 fun 0.1227 LLI   9.82 LAMpe  -0.07 LAMne  -0.40
  pass 13 fun 0.1228 LLI   9.82 LAMpe  -0.08 LAMne  -0.41
  pass 14 fun 0.1227 LLI   9.82 LAMpe  -0.08 LAMne  -0.41
  pass 15 fun 0.1227 LLI   9.82 LAMpe  -0.07 LAMne  -0.40
  pass 16 fun 0.1180 LLI   9.86 LAMpe  -0.02 LAMne  -0.36
  pass 17 fun 0.1199 LLI   9.98 LAMpe   0.34 LAMne  -0.23
  pass 18 fun 0.1183 LLI   9.90 LAMpe   0.10 LAMne  -0.34
  pass 19 fun 0.1178 LLI   9.92 LAMpe   0.08 LAMne  -0.31
  pass 20 fun 0.1182 LLI   9.88 LAMpe   0.05 LAMne  -0.33
voltage+dqdv pristine fun 0.0708
  pass  1 fun 0.1038 LLI  10.42 LAMpe   1.82 LAMne   2.98
  pass  2 fun 0.0725 LLI   9.77 LAMpe  -0.20 LAMne  -0.68
  pass  3 fun 0.0726 LLI   9.74 LAMpe  -0.28 LAMne  -0.63
  pass  4 fun 0.0762 LLI   9.84 LAMpe  -0.14 LAMne  -0.47
  pass  5 fun 0.0746 LLI   9.76 LAMpe  -0.17 LAMne  -0.71
  pass  6 fun 0.0728 LLI   9.74 LAMpe  -0.31 LAMne  -0.78
  pass  7 fun 0.0726 LLI   9.74 LAMpe  -0.30 LAMne  -0.68
  pass  8 fun 0.0746 LLI   9.76 LAMpe  -0.17 LAMne  -0.71
  pass  9 fun 0.0724 LLI   9.79 LAMpe  -0.14 LAMne  -0.63
  pass 10 fun 0.0724 LLI   9.78 LAMpe  -0.17 LAMne  -0.66
  pass 11 fun 0.0746 LLI   9.76 LAMpe  -0.17 LAMne  -0.71
  pass 12 fun 0.0759 LLI   9.86 LAMpe  -0.12 LAMne  -0.41
  pass 13 fun 0.0724 LLI   9.79 LAMpe  -0.13 LAMne  -0.63
  pass 14 fun 0.2906 LLI  -0.82 LAMpe  -0.02 LAMne  -0.93
  pass 15 fun 0.2665 LLI   0.90 LAMpe   7.08 LAMne  -1.39
  pass 16 fun 0.2665 LLI   0.89 LAMpe   7.07 LAMne  -1.40
  pass 17 fun 0.2707 LLI   1.26 LAMpe   6.45 LAMne  -1.39
  pass 18 fun 0.2651 LLI   0.88 LAMpe   7.69 LAMne  -2.13
  pass 19 fun 0.2647 LLI   0.66 LAMpe   7.21 LAMne  -1.66
  pass 20 fun 0.2663 LLI   0.78 LAMpe   6.74 LAMne  -1.26
rc=0
2026-10-05T00:40:18Z
```

## upstream 예제 자료 재현 (ampworks 자체 `examples/dqdv_data` · 패키지 데이터셋만)

### 네 판 (배포본 · 108행만 고침 · x0 복사만 고침 · 둘 다) — run_issue_checks.sh 출력 원문

```text
# 2026-10-05T00:51:28Z · clone 0f7a31c · Python 3.11.15 · numpy 2.4.6 · scipy 1.17.1 · pandas 3.0.6
# git apply --check: issue1 rc 0 · issue2 rc 0

=================== released
ampworks from <scratch>/amp_venv/lib/python3.11/site-packages/ampworks/__init__.py
--- issue1_partA.py
only xn0_std = 0.01:  LLI_std = 0.011254   first-order expected = 0.011254
only xn1_std = 0.01:  LLI_std = 0.011161   first-order expected = 0.000662
only xp0_std = 0.01:  LLI_std = 0.001173   first-order expected = 0.001173
only xp1_std = 0.01:  LLI_std = 0.000000   first-order expected = 0.011142
rc=0
--- issue1_partB.py (cwd examples/)
 Cycle      LLI  LLI_std
     2 0.000000 0.019061
  3866 0.110284 0.005784
rc=0
--- issue2_repro.py (cwd examples/)
fitres2.x[-1] right after the BOL fit: 0.02783
fitres2.x[-1] after the EOL fit:       0.01530
 Cycle       iR
     2 0.015299
  3866 0.021082
rc=0
--- pytest tests/test_dqdv (upstream 11 + proposed 5)
FAILED tests/test_dqdv/test_fitter.py::test_constrained_fit_does_not_modify_x0
FAILED tests/test_dqdv/test_lam_lli.py::test_lli_std_single_parameter[xn1] - ...
FAILED tests/test_dqdv/test_lam_lli.py::test_lli_std_single_parameter[xp1] - ...
3 failed, 13 passed in 5.72s
rc=1

=================== fix108
ampworks from <scratch>/amp_fix_variants/fix108/ampworks/__init__.py
--- issue1_partA.py
only xn0_std = 0.01:  LLI_std = 0.011254   first-order expected = 0.011254
only xn1_std = 0.01:  LLI_std = 0.000662   first-order expected = 0.000662
only xp0_std = 0.01:  LLI_std = 0.001173   first-order expected = 0.001173
only xp1_std = 0.01:  LLI_std = 0.011142   first-order expected = 0.011142
rc=0
--- issue1_partB.py (cwd examples/)
 Cycle      LLI  LLI_std
     2 0.000000 0.009471
  3866 0.110284 0.008352
rc=0
--- issue2_repro.py (cwd examples/)
fitres2.x[-1] right after the BOL fit: 0.02783
fitres2.x[-1] after the EOL fit:       0.01530
 Cycle       iR
     2 0.015299
  3866 0.021082
rc=0
--- pytest tests/test_dqdv (upstream 11 + proposed 5)
FAILED tests/test_dqdv/test_fitter.py::test_constrained_fit_does_not_modify_x0
1 failed, 15 passed in 5.74s
rc=1

=================== fixx0
ampworks from <scratch>/amp_fix_variants/fixx0/ampworks/__init__.py
--- issue1_partA.py
only xn0_std = 0.01:  LLI_std = 0.011254   first-order expected = 0.011254
only xn1_std = 0.01:  LLI_std = 0.011161   first-order expected = 0.000662
only xp0_std = 0.01:  LLI_std = 0.001173   first-order expected = 0.001173
only xp1_std = 0.01:  LLI_std = 0.000000   first-order expected = 0.011142
rc=0
--- issue1_partB.py (cwd examples/)
 Cycle      LLI  LLI_std
     2 0.000000 0.019061
  3866 0.110284 0.005784
rc=0
--- issue2_repro.py (cwd examples/)
fitres2.x[-1] right after the BOL fit: 0.02783
fitres2.x[-1] after the EOL fit:       0.02783
 Cycle       iR
     2 0.027830
  3866 0.021082
rc=0
--- pytest tests/test_dqdv (upstream 11 + proposed 5)
FAILED tests/test_dqdv/test_lam_lli.py::test_lli_std_single_parameter[xn1] - ...
FAILED tests/test_dqdv/test_lam_lli.py::test_lli_std_single_parameter[xp1] - ...
2 failed, 14 passed in 9.03s
rc=1

=================== both
ampworks from <scratch>/amp_fix_variants/both/ampworks/__init__.py
--- issue1_partA.py
only xn0_std = 0.01:  LLI_std = 0.011254   first-order expected = 0.011254
only xn1_std = 0.01:  LLI_std = 0.000662   first-order expected = 0.000662
only xp0_std = 0.01:  LLI_std = 0.001173   first-order expected = 0.001173
only xp1_std = 0.01:  LLI_std = 0.011142   first-order expected = 0.011142
rc=0
--- issue1_partB.py (cwd examples/)
 Cycle      LLI  LLI_std
     2 0.000000 0.009471
  3866 0.110284 0.008352
rc=0
--- issue2_repro.py (cwd examples/)
fitres2.x[-1] right after the BOL fit: 0.02783
fitres2.x[-1] after the EOL fit:       0.02783
 Cycle       iR
     2 0.027830
  3866 0.021082
rc=0
--- pytest tests/test_dqdv (upstream 11 + proposed 5)
16 passed in 8.93s
rc=0

# clone dirty files: 0 · end 2026-10-05T00:53:20Z
```

### Hessian — issue3_hessian.py 출력 원문

```text
# 2026-10-05T00:53:48Z issue3_hessian.py
=================== released
BOL x      [0.0377 0.8486 0.0177 0.9072 0.0278]
BOL eig(H) [ -1959.1474    397.9259   1197.564    7445.6618 157368.5997]
BOL diag(0.5*inv(H)) [-4.4398e-08  3.1014e-04 -1.5072e-04  7.5021e-05  1.2548e-03]
BOL x_std  [0.0002 0.0176 0.0123 0.0087 0.0354]  (equal to sqrt|diag|: True )
BOL max |offdiag(0.5*inv(H)) / outer(x_std, x_std)| over xn0..xp1: 10.461
EOL x      [0.0053 0.7566 0.002  0.9088 0.0211]
EOL eig(H) [-142847.1627     398.8669    4540.1683  157745.7603  267796.5603]
EOL diag(0.5*inv(H)) [-5.0080e-08  3.5096e-05  4.2365e-06  7.3265e-05  1.2527e-03]
EOL x_std  [0.0002 0.0059 0.0021 0.0086 0.0354]  (equal to sqrt|diag|: True )
EOL max |offdiag(0.5*inv(H)) / outer(x_std, x_std)| over xn0..xp1: 1.734
rc=0
=================== both
BOL x      [0.0377 0.8486 0.0177 0.9072 0.0278]
BOL eig(H) [ -1959.1474    397.9259   1197.564    7445.6618 157368.5997]
BOL diag(0.5*inv(H)) [-4.4398e-08  3.1014e-04 -1.5072e-04  7.5021e-05  1.2548e-03]
BOL x_std  [0.0002 0.0176 0.0123 0.0087 0.0354]  (equal to sqrt|diag|: True )
BOL max |offdiag(0.5*inv(H)) / outer(x_std, x_std)| over xn0..xp1: 10.461
EOL x      [0.0053 0.7566 0.002  0.9088 0.0211]
EOL eig(H) [-142847.1627     398.8669    4540.1683  157745.7603  267796.5603]
EOL diag(0.5*inv(H)) [-5.0080e-08  3.5096e-05  4.2365e-06  7.3265e-05  1.2527e-03]
EOL x_std  [0.0002 0.0059 0.0021 0.0086 0.0354]  (equal to sqrt|diag|: True )
EOL max |offdiag(0.5*inv(H)) / outer(x_std, x_std)| over xn0..xp1: 1.734
rc=0
# clone dirty files: 0 · end 00:54:04Z
```

### x0 덮어쓰기 첫 확인 — amp_upstream_mutation.py 출력 원문

```text
2026-10-05T00:46:51Z
grid.x before constrained_fit: [0.05 0.85 0.   0.9  0.  ]
grid.x after  constrained_fit: [0.05    0.85    0.      0.9     0.02617] · same object as input: True
fitres2.x right after BOL fit : [0.03771 0.84857 0.01767 0.90718 0.02783]
fitres2.x after EOL fit       : [0.03771 0.84857 0.01767 0.90718 0.0153 ]
only iR changed: True
table iR column: [0.0153, 0.02108] · BOL fitted iR was 0.02783
with a copy passed in, fitres2b.x unchanged: True
rc=0
```

## 실험 스크립트 (실행한 그대로)

### amp_exp.py

```python
"""ampworks 판정 실험 A1–A3 (2026-10-05 · 사용자 승인 "ㄱㄱ").

우리 PyBaMM 합성 truth (artifacts/grid_curves_v4/curves.parquet · 읽기만 · 시작 때 sha256 대조) 를 ampworks
(NatLabRockies/ampworks main 0f7a31c6 · 스크래치패드의 버리는 venv) 의 dQdV 피팅 → calc_lam_lli 에 넣어
  A1  참값 LLI · LAM 을 되찾는가 — cost terms 4 가지 (all · voltage · dqdv · dvdq) × 시작점 2 경로 (grid_search(21) · pristine 창 이어받기)
  A2  원본 calc_lam_lli 의 LLI_std ↔ 108행만 고친 사본 (xn1_std → xp1_std) 의 LLI_std
  A3  대각 전파 (ampworks 근사 · 108행 고친 식) ↔ 전체 공분산 전파 (같은 Hessian · 같은 0.5 배율 · 같은 대각 안정화) — 참값 오차와 비교
를 잰다. 쓰는 곳은 argv[1] (스크래치패드) 의 JSON 하나뿐. 저장소 · 등록부 · 운영 환경에는 아무것도 쓰지 않는다.

  사용: amp_venv/bin/python amp_exp.py <출력 디렉터리> <halfcell_ocp_ref.npz>
"""
import hashlib
import json
import os
import sys
import time
import types
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")

import numpy as np
import pandas as pd

import ampworks as amp
import ampworks.dqdv._lam_lli as lamlli

REPO = Path("/home/user/Yonghoon-DEM-DFT/degradation-degeneracy")
PARQ = REPO / "artifacts/grid_curves_v4/curves.parquet"
PARQ_SHA = "b69dc7bee0bb2e32aba73b6ace91255d964bceb41f9361886de7275bf48aa8b8"
OUT = Path(sys.argv[1])
REF = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

COSTS = {"all": ["voltage", "dqdv", "dvdq"], "voltage": ["voltage"], "dqdv": ["dqdv"], "dvdq": ["dvdq"]}
BUG = "        + (((1. - xp0)*dQp)*xn1_std)**2         # contribution from xp1\n"
FIX = "        + (((1. - xp0)*dQp)*xp1_std)**2         # contribution from xp1\n"


def fixed_calc_lam_lli():
    """설치된 _lam_lli.py 원문에서 108행 한 줄만 바꾼 사본 — 그 밖의 바이트는 같다 (아래 identity 에 줄 diff 를 남긴다)."""
    src = Path(lamlli.__file__).read_text(encoding="utf-8")
    assert src.count(BUG) == 1, "108행 원문이 예상과 다르다"
    fixed = src.replace(BUG, FIX)
    diff = [(i + 1, a, b) for i, (a, b) in enumerate(zip(src.splitlines(), fixed.splitlines())) if a != b]
    assert len(diff) == 1 and diff[0][0] == 108, diff
    mod = types.ModuleType("lam_lli_fixed")
    exec(compile(fixed, "lam_lli_fixed.py", "exec"), mod.__dict__)
    return mod.calc_lam_lli, {"installed_file": str(lamlli.__file__), "installed_sha256": hashlib.sha256(src.encode()).hexdigest(),
                              "line_diff": [{"line": d[0], "before": d[1], "after": d[2]} for d in diff]}


def windows_from_hess(fr, opt):
    """ampworks 와 같은 공분산 (cov = inv(H + 1e-16·max|eig|·I) · std = sqrt(0.5·|diag|)) — 대각만 버리지 않고 전체를 남긴다."""
    H = np.asarray(opt.hess, float)
    ev = np.linalg.eigvalsh(0.5 * (H + H.T))
    scale = 1e-16 * np.max(np.abs(np.linalg.eig(H)[0]))
    cov = np.linalg.inv(H + scale * np.eye(H.shape[0]))
    C = 0.5 * cov                                             # ampworks 의 std² = 0.5·|diag(cov)| 와 같은 배율
    std_amp = np.asarray(fr.x_std, float)
    return {"C": C, "hess_eig": ev, "diag_negative": [int(i) for i in np.where(np.diag(C) < 0)[0]],
            "std_reproduced_max_abs_diff": float(np.max(np.abs(np.sqrt(np.abs(np.diag(C)))[:4] - std_amp[:4])))}


def propagate(x, C, Ah):
    """Inv · Qn · Qp 의 1차 전파 — 대각 (독립 가정) 과 전체 공분산. 창 4 개 블록만 (iR 은 Inv · Q 에 들어가지 않는다)."""
    xn0, xn1, xp0, xp1 = x[:4]
    Qn, Qp = Ah / (xn1 - xn0), Ah / (xp1 - xp0)
    dQn, dQp = Ah / (xn1 - xn0) ** 2, Ah / (xp1 - xp0) ** 2
    C4 = C[:4, :4]
    g_inv = np.array([Qn + xn0 * dQn, -xn0 * dQn, -Qp + (1 - xp0) * dQp, -(1 - xp0) * dQp])
    g_qn = np.array([dQn, -dQn, 0, 0])
    g_qp = np.array([0, 0, dQp, -dQp])
    out = {"Inv": xn0 * Qn + (1 - xp0) * Qp, "Qn": Qn, "Qp": Qp}
    for name, g in (("Inv", g_inv), ("Qn", g_qn), ("Qp", g_qp)):
        out[name + "_std_diag"] = float(np.sqrt(np.sum(g ** 2 * np.abs(np.diag(C4)))))
        vf = float(g @ C4 @ g)
        out[name + "_std_full"] = float(np.sqrt(vf)) if vf >= 0 else float("nan")
        out[name + "_var_full_raw"] = vf
    d = np.sqrt(np.abs(np.diag(C4)))
    out["corr_windows"] = (C4 / np.outer(d, d)).tolist()
    return out


def run_fit(fitter, x0, passes=2):
    """constrained_fit 을 결과에서 다시 시작해 passes 번 (예제 권고). 마지막 결과 · opt (Hessian) 를 돌려준다."""
    hist = []
    fr = opt = None
    x = np.asarray(x0, float)
    for _ in range(passes):
        fr, opt = fitter.constrained_fit(x, return_full=True)
        hist.append({"x": [float(v) for v in fr.x], "fun": float(fr.fun), "success": bool(fr.success)})
        x = np.asarray(fr.x, float)
    return fr, opt, hist


def truth_window(ref, v_pe, v_ne):
    """DFN 전극 전위 (0.05 C · 과전압 포함) 를 평형 OCP 표로 역보간 — ampworks 규약 (xn = 음극 리튬화 분율 · xp = 1 − y) 으로. SOC 오름차순 입력."""
    y, u, z, w = ref["y_pe"], ref["u_pe"], ref["z_ne"], ref["u_ne"]
    ype = np.interp(v_pe, u[::-1], y[::-1])
    zne = np.interp(v_ne, w[::-1], z[::-1])
    return {"xn0": float(zne[0]), "xn1": float(zne[-1]), "xp0": float(1 - ype[0]), "xp1": float(1 - ype[-1])}


def main():
    t0 = time.time()
    raw = PARQ.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PARQ_SHA, "곡선 파일이 manifest 의 sha256 과 다르다"
    calc_fixed, ident = fixed_calc_lam_lli()
    ref = np.load(REF)
    neg = pd.DataFrame({"SOC": ref["z_ne"], "Volts": ref["u_ne"]})
    pos = pd.DataFrame({"SOC": 1.0 - ref["y_pe"], "Volts": ref["u_pe"]}).sort_values("SOC").reset_index(drop=True)

    cols = ["cond_id", "lli", "lam_pe", "lam_ne", "lam_pe_type", "lam_ne_type", "noise", "q_mah", "x_norm", "v_pe", "v_ne", "v_full"]
    df = pd.read_parquet(PARQ, columns=cols)
    conds = df.drop_duplicates("cond_id")
    z = conds[conds.noise == 0]

    def pick(lli, pe, ne):
        r = z[(z.lli == lli) & (z.lam_pe == pe) & (z.lam_ne == ne)]
        return None if r.empty else r.iloc[0]
    pe_only = z[(z.lli == 0) & (z.lam_ne == 0) & (z.lam_pe > 0)].sort_values("lam_pe")
    cases = {"pristine": pick(0, 0, 0), "LLI_only_0.10": pick(0.10, 0, 0), "LAMNE_only_0.10": pick(0, 0, 0.10),
             "mixed_0.10_0.10_0.10": pick(0.10, 0.10, 0.10), "LAMPE_only_max": None if pe_only.empty else pe_only.iloc[-1]}

    def cell(c):
        r = df[df.cond_id == c.cond_id].sort_values("x_norm")
        soc = 1.0 - r.x_norm.to_numpy()                       # x_norm 0 = 충전 끝 → SOC 1
        o = np.argsort(soc)
        q = float(c.q_mah) / 1000.0
        frame = pd.DataFrame({"Ah": soc[o] * q, "SOC": soc[o], "Volts": r.v_full.to_numpy()[o]})
        return frame, q, truth_window(ref, r.v_pe.to_numpy()[o], r.v_ne.to_numpy()[o])

    out = {"identity": {"ampworks": amp.__version__, "numpy": np.__version__, "pandas": pd.__version__, "parquet": str(PARQ),
                        "parquet_sha256": PARQ_SHA, "ref_npz_sha256": hashlib.sha256(REF.read_bytes()).hexdigest(), **ident},
           "cases": {k: (None if v is None else {kk: (v[kk] if isinstance(v[kk], str) else float(v[kk]))
                                                  for kk in ("cond_id", "lli", "lam_pe", "lam_ne", "lam_pe_type", "lam_ne_type", "q_mah")})
                     for k, v in cases.items()},
           "runs": {}}
    cell0, q0, tw0 = cell(cases["pristine"])
    for cname, terms in COSTS.items():
        rec = {"cost_terms": terms, "pristine": {}, "aged": {}}
        fitter = amp.dqdv.DqdvFitter(neg, pos, cell0, cost_terms=terms)
        t1 = time.time()
        g0 = fitter.grid_search(21)
        fr0, opt0, h0 = run_fit(fitter, g0.x)
        cov0 = windows_from_hess(fr0, opt0)
        p0 = propagate(np.asarray(fr0.x, float), cov0["C"], q0)
        rec["pristine"] = {"grid_x": [float(v) for v in g0.x], "fits": h0, "x_std": [float(v) for v in fr0.x_std],
                           "truth_window_approx": tw0, "hess_eig": cov0["hess_eig"].tolist(), "diag_negative": cov0["diag_negative"],
                           "std_reproduced_max_abs_diff": cov0["std_reproduced_max_abs_diff"],
                           "prop": {k: v for k, v in p0.items() if k != "corr_windows"}, "corr_windows": p0["corr_windows"],
                           "seconds": time.time() - t1}
        for name, c in cases.items():
            if name == "pristine" or c is None:
                continue
            t2 = time.time()
            cframe, q, tw = cell(c)
            fitter.cell = cframe
            paths = {}
            fr_c, opt_c, h_c = run_fit(fitter, fr0.x)
            paths["carry_pristine"] = (fr_c, opt_c, h_c, None)
            g = fitter.grid_search(21)
            fr_g, opt_g, h_g = run_fit(fitter, g.x)
            paths["grid21"] = (fr_g, opt_g, h_g, [float(v) for v in g.x])
            prec = {}
            for pname, (fr, opt, hist, gx) in paths.items():
                table = amp.dqdv.DqdvFitTable()
                table.append(fr0)
                table.append(fr)
                orig = amp.dqdv.calc_lam_lli(table).df
                fixd = calc_fixed(table).df
                cv = windows_from_hess(fr, opt)
                pa = propagate(np.asarray(fr.x, float), cv["C"], q)
                truth = {"LLI": float(c.lli), "LAM_pe": float(c.lam_pe), "LAM_ne": float(c.lam_ne), "SOH": q / q0}
                est = {"LLI": float(orig.LLI.iloc[1]), "LAM_pe": float(orig.LAMp.iloc[1]), "LAM_ne": float(orig.LAMn.iloc[1]),
                       "Qc_ratio": float(orig.Qc.iloc[1] / orig.Qc.iloc[0])}
                inv0 = p0["Inv"]
                lli_full_ref_exact = pa["Inv_std_full"] / inv0
                lli_full_both = float(np.sqrt((pa["Inv_std_full"] / inv0) ** 2 + (pa["Inv"] * p0["Inv_std_full"] / inv0 ** 2) ** 2))
                prec[pname] = {
                    "grid_x": gx, "fits": hist, "x": [float(v) for v in fr.x], "x_std": [float(v) for v in fr.x_std],
                    "truth_window_approx": tw, "truth": truth, "estimate": est,
                    "error": {k: est[k] - truth[k] for k in ("LLI", "LAM_pe", "LAM_ne")},
                    "A2": {"LLI_std_original": float(orig.LLI_std.iloc[1]), "LLI_std_fixed": float(fixd.LLI_std.iloc[1]),
                           "ratio_original_over_fixed": float(orig.LLI_std.iloc[1] / fixd.LLI_std.iloc[1]),
                           "xn1_std": float(fr.x_std[1]), "xp1_std": float(fr.x_std[3]),
                           "other_columns_identical": bool(orig.drop(columns=["LLI_std"]).equals(fixd.drop(columns=["LLI_std"])))},
                    "A3": {"LLI_std_diag_fixed_formula": pa["Inv_std_diag"] / inv0, "LLI_std_full_ref_exact": lli_full_ref_exact,
                           "LLI_std_full_incl_reference_fit": lli_full_both,
                           "LAMn_std_diag": pa["Qn_std_diag"] / p0["Qn"], "LAMn_std_full": pa["Qn_std_full"] / p0["Qn"],
                           "LAMp_std_diag": pa["Qp_std_diag"] / p0["Qp"], "LAMp_std_full": pa["Qp_std_full"] / p0["Qp"],
                           "LAMn_std_ampworks": float(orig.LAMn_std.iloc[1]), "LAMp_std_ampworks": float(orig.LAMp_std.iloc[1]),
                           "corr_windows": pa["corr_windows"], "hess_eig": cv["hess_eig"].tolist(), "diag_negative": cv["diag_negative"],
                           "std_reproduced_max_abs_diff": cv["std_reproduced_max_abs_diff"]},
                }
            rec["aged"][name] = {"paths": prec, "seconds": time.time() - t2}
            print(json.dumps({"cost": cname, "case": name,
                              **{p: {"est": v["estimate"], "err": v["error"], "fun": v["fits"][-1]["fun"]} for p, v in prec.items()}},
                             ensure_ascii=False), flush=True)
        out["runs"][cname] = rec
    out["wall_s"] = time.time() - t0
    (OUT / "ampworks_exp_results.json").write_text(json.dumps(out, indent=1, ensure_ascii=False, default=float), encoding="utf-8")
    print(json.dumps({"wall_s": round(out["wall_s"], 1), "identity": {k: v for k, v in out["identity"].items() if k != "line_diff"}},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
```

### summarize.py

```python
"""ampworks_exp_results.json → 사람이 읽는 표 (A1 · A2 · A3). 계산은 하지 않고 JSON 값을 옮기기만 한다."""
import json
import sys

import numpy as np

d = json.load(open(sys.argv[1], encoding="utf-8"))
print("identity:", {k: v for k, v in d["identity"].items() if k != "line_diff"})
print("line_diff:", d["identity"]["line_diff"])
print("wall_s:", round(d["wall_s"], 1))
print()
print("cases:", {k: (v and {kk: v[kk] for kk in ("lli", "lam_pe", "lam_ne", "lam_pe_type", "lam_ne_type", "q_mah")}) for k, v in d["cases"].items()})
print()

print("== A1 참값 복원 (est − truth, 백분율 포인트) · fun = ampworks 목적함수 (MAPE 합) · 경로 carry = pristine 창 이어받기 · grid = grid_search(21)")
print(f"{'cost':8s} {'case':22s} {'path':6s} {'fun':>8s} | {'LLI':>7s} {'LAMpe':>7s} {'LAMne':>7s} | {'dLLI':>7s} {'dLAMpe':>7s} {'dLAMne':>7s}")
for cost, rec in d["runs"].items():
    p = rec["pristine"]
    print(f"{cost:8s} {'pristine':22s} {'':6s} {p['fits'][-1]['fun']:8.4f} | x = {[round(v, 4) for v in p['fits'][-1]['x']]} · truth_window ≈ "
          f"{ {k: round(v, 4) for k, v in p['truth_window_approx'].items()} }")
    for case, a in rec["aged"].items():
        for path, v in a["paths"].items():
            e, er = v["estimate"], v["error"]
            print(f"{cost:8s} {case:22s} {path[:6]:6s} {v['fits'][-1]['fun']:8.4f} | {e['LLI']*100:7.2f} {e['LAM_pe']*100:7.2f} {e['LAM_ne']*100:7.2f} | "
                  f"{er['LLI']*100:+7.2f} {er['LAM_pe']*100:+7.2f} {er['LAM_ne']*100:+7.2f}")
print()

print("== A2 LLI_std: 원본 (108행 xn1_std) ↔ 고친 사본 (xp1_std) · 다른 열은 같은가")
print(f"{'cost':8s} {'case':22s} {'path':6s} | {'orig':>9s} {'fixed':>9s} {'ratio':>7s} | {'xn1_std':>9s} {'xp1_std':>9s} | others_same")
ratios = []
for cost, rec in d["runs"].items():
    for case, a in rec["aged"].items():
        for path, v in a["paths"].items():
            x = v["A2"]
            ratios.append(x["ratio_original_over_fixed"])
            print(f"{cost:8s} {case:22s} {path[:6]:6s} | {x['LLI_std_original']*100:9.4f} {x['LLI_std_fixed']*100:9.4f} {x['ratio_original_over_fixed']:7.3f} | "
                  f"{x['xn1_std']:9.2e} {x['xp1_std']:9.2e} | {x['other_columns_identical']}")
print(f"ratio original/fixed: min {min(ratios):.3f} · median {float(np.median(ratios)):.3f} · max {max(ratios):.3f} (n {len(ratios)})")
print()

print("== A3 불확도 (백분율 포인트): ampworks 대각 (108행 고침) ↔ 전체 공분산 (기준 행 정확) ↔ 전체 + 기준 행 불확도 · 참값 오차와 비교")
print(f"{'cost':8s} {'case':22s} {'path':6s} | {'|dLLI|':>7s} {'diag':>7s} {'full':>7s} {'full+0':>7s} | {'|dLAMn|':>7s} {'diag':>7s} {'full':>7s} | "
      f"{'|dLAMp|':>7s} {'diag':>7s} {'full':>7s} | {'min eig':>9s} {'neg':>4s} | corr(xn0,xp0) corr(xn1,xp1) corr(xp0,xp1)")
for cost, rec in d["runs"].items():
    for case, a in rec["aged"].items():
        for path, v in a["paths"].items():
            x, er = v["A3"], v["error"]
            c = np.array(x["corr_windows"])
            print(f"{cost:8s} {case:22s} {path[:6]:6s} | {abs(er['LLI'])*100:7.3f} {x['LLI_std_diag_fixed_formula']*100:7.3f} {x['LLI_std_full_ref_exact']*100:7.3f} "
                  f"{x['LLI_std_full_incl_reference_fit']*100:7.3f} | {abs(er['LAM_ne'])*100:7.3f} {x['LAMn_std_diag']*100:7.3f} {x['LAMn_std_full']*100:7.3f} | "
                  f"{abs(er['LAM_pe'])*100:7.3f} {x['LAMp_std_diag']*100:7.3f} {x['LAMp_std_full']*100:7.3f} | {min(x['hess_eig']):9.2e} {len(x['diag_negative']):4d} | "
                  f"{c[0, 2]:+.3f} {c[1, 3]:+.3f} {c[2, 3]:+.3f}")
print()
print("std_reproduced_max_abs_diff (ampworks x_std 와 이 스크립트가 같은 식으로 다시 만든 std 의 차 — 0 이면 같은 공분산):",
      max(v["A3"]["std_reproduced_max_abs_diff"] for rec in d["runs"].values() for a in rec["aged"].values() for v in a["paths"].values()))
```

### amp_exp_passes.py

```python
"""보충 (A1): 기본 비용 'all' 의 LLI 단독 조건 — constrained_fit 을 결과에서 다시 시작하는 반복을 목적함수가 멈출 때까지 (최대 20 회).
예제 권고 ("pass the output from a previous routine back in to see if the fit continues to improve") 를 끝까지 따른다. 출력은 argv[1] JSON 하나.
"""
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")
import numpy as np
import pandas as pd
import ampworks as amp

PARQ = Path("/home/user/Yonghoon-DEM-DFT/degradation-degeneracy/artifacts/grid_curves_v4/curves.parquet")
ref = np.load(sys.argv[2])
neg = pd.DataFrame({"SOC": ref["z_ne"], "Volts": ref["u_ne"]})
pos = pd.DataFrame({"SOC": 1.0 - ref["y_pe"], "Volts": ref["u_pe"]}).sort_values("SOC").reset_index(drop=True)
df = pd.read_parquet(PARQ, columns=["cond_id", "lli", "lam_pe", "lam_ne", "noise", "q_mah", "x_norm", "v_full"])
z = df[df.noise == 0]


def cell(lli, pe, ne):
    r = z[(z.lli == lli) & (z.lam_pe == pe) & (z.lam_ne == ne)].sort_values("x_norm")
    soc = 1.0 - r.x_norm.to_numpy()
    o = np.argsort(soc)
    q = float(r.q_mah.iloc[0]) / 1000.0
    return pd.DataFrame({"Ah": soc[o] * q, "SOC": soc[o], "Volts": r.v_full.to_numpy()[o]})


out = {}
for cname, terms in (("all", ["voltage", "dqdv", "dvdq"]), ("voltage+dqdv", ["voltage", "dqdv"])):
    f = amp.dqdv.DqdvFitter(neg, pos, cell(0, 0, 0), cost_terms=terms)
    g = f.grid_search(21)
    x = np.asarray(g.x, float)
    prev = None
    for _ in range(20):
        fr0 = f.constrained_fit(x)
        x = np.asarray(fr0.x, float)
        if prev is not None and abs(prev - fr0.fun) < 1e-7:
            break
        prev = fr0.fun
    f.cell = cell(0.10, 0, 0)
    rows = []
    x = np.asarray(fr0.x, float)
    prev = None
    for k in range(20):
        fr = f.constrained_fit(x)
        t = amp.dqdv.DqdvFitTable()
        t.append(fr0)
        t.append(fr)
        dm = amp.dqdv.calc_lam_lli(t).df.iloc[1]
        rows.append({"pass": k + 1, "fun": float(fr.fun), "x": [float(v) for v in fr.x], "LLI": float(dm.LLI),
                     "LAM_pe": float(dm.LAMp), "LAM_ne": float(dm.LAMn)})
        x = np.asarray(fr.x, float)
        if prev is not None and abs(prev - fr.fun) < 1e-7:
            break
        prev = fr.fun
    out[cname] = {"pristine_fun": float(fr0.fun), "pristine_x": [float(v) for v in fr0.x], "aged_passes": rows}
    print(cname, "pristine fun", round(fr0.fun, 4))
    for r in rows:
        print(f"  pass {r['pass']:2d} fun {r['fun']:.4f} LLI {r['LLI']*100:6.2f} LAMpe {r['LAM_pe']*100:6.2f} LAMne {r['LAM_ne']*100:6.2f}")
Path(sys.argv[1]).write_text(json.dumps(out, indent=1), encoding="utf-8")
```

### amp_upstream_mutation.py

```python
"""upstream issue 2 후보 확인 — constrained_fit 이 넘겨받은 x0 배열 (앞 결과의 .x) 의 iR 을 제자리에서 덮어쓰는가.

ampworks 자신의 예제 자료 (examples/dqdv_data) 와 예제 스크립트의 순서 그대로:
fitres2 = constrained_fit(grid.x) → fitter.cell = EOL → fitres3866 = constrained_fit(fitres2.x) → table.append(fitres2) …
fitres2.x 를 EOL 적합 전 · 후로 복사해 비교하고, 표의 BOL 행 iR 이 BOL 적합의 iR 인지 본다.
"""
import os
import sys
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")
import numpy as np
import pandas as pd
import ampworks as amp

EX = Path(sys.argv[1])
neg = pd.read_csv(EX / "gr.csv")
pos = pd.read_csv(EX / "nmc.csv")
bol = pd.read_csv(EX / "charge2_smooth.csv")
eol = pd.read_csv(EX / "charge3866_smooth.csv")

fitter = amp.dqdv.DqdvFitter(neg, pos, bol)
fitter.cost_terms = ["voltage", "dqdv", "dvdq"]
grid = fitter.grid_search(21)
grid_x_before = grid.x.copy()
fitres2 = fitter.constrained_fit(grid.x)
print("grid.x before constrained_fit:", np.round(grid_x_before, 5))
print("grid.x after  constrained_fit:", np.round(grid.x, 5), "· same object as input:", True)

bol_x_after_fit = fitres2.x.copy()
fitter.cell = eol
fitres3866 = fitter.constrained_fit(fitres2.x)
print("fitres2.x right after BOL fit :", np.round(bol_x_after_fit, 5))
print("fitres2.x after EOL fit       :", np.round(fitres2.x, 5))
print("only iR changed:", bool(np.array_equal(bol_x_after_fit[:4], fitres2.x[:4]) and bol_x_after_fit[4] != fitres2.x[4]))

table = amp.dqdv.DqdvFitTable(extra_cols=["Cycle"])
table.append(fitres2, Cycle=2)
table.append(fitres3866, Cycle=3866)
print("table iR column:", table.df.iR.round(5).tolist(), "· BOL fitted iR was", round(float(bol_x_after_fit[4]), 5))

# 사본을 넘기면 덮어쓰기가 없다 — 해결 방향 확인 (np.array(x0, dtype=float) 와 같은 효과)
fitter.cell = bol
fitres2b = fitter.constrained_fit(grid_x_before.copy())
keep = fitres2b.x.copy()
fitter.cell = eol
_ = fitter.constrained_fit(fitres2b.x.copy())
print("with a copy passed in, fitres2b.x unchanged:", bool(np.array_equal(keep, fitres2b.x)))
```

## upstream 재현 스크립트 · 제안 시험 · 수정 diff (실행한 그대로)

### run_issue_checks.sh

```bash
#!/usr/bin/env bash
# upstream issue 초안의 모든 출력 · 시험 결과를 한 로그로 — 배포본 (site-packages = main 0f7a31c6) · fix108 · fixx0 · both.
# 저장소 (Yonghoon-DEM-DFT) 는 건드리지 않는다. ampworks clone 도 읽기만 (PYTHONDONTWRITEBYTECODE · -p no:cacheprovider).
S=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/a45978e3-3a6e-5e3d-af55-7c9b61e0d809/scratchpad
C=/home/user/natlabrockies/ampworks
I=$S/amp_exp/issue
A=$S/amp_fix_variants
PY=$S/amp_venv/bin/python
export OMP_NUM_THREADS=1 MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1

# 제안 시험을 upstream tests/ 배치 그대로에 얹은 사본
rm -rf $I/tests_layout && mkdir -p $I/tests_layout && cp -r $C/tests $I/tests_layout/tests
cp $S/amp_exp/upstream_tests/test_dqdv/test_lam_lli.py $I/tests_layout/tests/test_dqdv/test_lam_lli.py
cat $I/proposed_test_fitter_append.py >> $I/tests_layout/tests/test_dqdv/test_fitter.py

echo "# $(date -u +%Y-%m-%dT%H:%M:%SZ) · clone $(git -C $C rev-parse --short HEAD) · $($PY -V 2>&1) · numpy $($PY -c 'import numpy; print(numpy.__version__)') · scipy $($PY -c 'import scipy; print(scipy.__version__)') · pandas $($PY -c 'import pandas; print(pandas.__version__)')"
echo "# git apply --check: issue1 rc $(git -C $C apply --check $A/issue1_fix.diff >/dev/null 2>&1; echo $?) · issue2 rc $(git -C $C apply --check $A/issue2_fix.diff >/dev/null 2>&1; echo $?)"
for v in released fix108 fixx0 both; do
  if [ $v = released ]; then PP=""; else PP=$A/$v; fi
  echo
  echo "=================== $v"
  ( cd $C/examples && PYTHONPATH=$PP nice -n 10 $PY -c "import ampworks; print('ampworks from', ampworks.__file__.replace('$S', '<scratch>'))" )
  echo "--- issue1_partA.py"
  ( cd $C/examples && PYTHONPATH=$PP nice -n 10 $PY $I/issue1_partA.py; echo "rc=$?" )
  echo "--- issue1_partB.py (cwd examples/)"
  ( cd $C/examples && PYTHONPATH=$PP nice -n 10 $PY $I/issue1_partB.py; echo "rc=$?" )
  echo "--- issue2_repro.py (cwd examples/)"
  ( cd $C/examples && PYTHONPATH=$PP nice -n 10 $PY $I/issue2_repro.py; echo "rc=$?" )
  echo "--- pytest tests/test_dqdv (upstream 11 + proposed 5)"
  ( cd $I/tests_layout && PYTHONPATH=$PP nice -n 10 $PY -m pytest -q -p no:cacheprovider tests/test_dqdv 2>&1 | grep -E "^FAILED|passed|failed"; echo "rc=${PIPESTATUS[0]}" )
done
echo
echo "# clone dirty files: $(git -C $C status --short | wc -l) · end $(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

### issue1_partA.py

```python
import numpy as np
import ampworks as amp

x = {'xn0': 0.05, 'xn1': 0.85, 'xp0': 0.05, 'xp1': 0.90}


def inventory(xn0, xn1, xp0, xp1, Ah=1.0):
    return xn0*Ah/(xn1 - xn0) + (1.0 - xp0)*Ah/(xp1 - xp0)


def lli_std(x_std):
    result = amp.dqdv.DqdvFitResult(
        success=True, message='', fun=0.0, Ah=1.0,
        x=np.array([*x.values(), 0.0]), x_std=np.array([*x_std, 0.0]),
        x_map=['xn0', 'xn1', 'xp0', 'xp1', 'iR'],
    )
    table = amp.dqdv.DqdvFitTable()
    table.append(result)
    return amp.dqdv.calc_lam_lli(table).df['LLI_std'].iloc[0]


h = 1e-6
for i, name in enumerate(x):
    std = [0.0]*4
    std[i] = 0.01
    up, dn = dict(x), dict(x)
    up[name] += h
    dn[name] -= h
    expected = abs(inventory(**up) - inventory(**dn))/(2*h)*0.01/inventory(**x)
    print(f"only {name}_std = 0.01:  LLI_std = {lli_std(std):.6f}"
          f"   first-order expected = {expected:.6f}")
```

### issue1_partB.py

```python
import pandas as pd
import ampworks as amp

# run from examples/ (pre-smoothed CSVs shipped in examples/dqdv_data)
neg = pd.read_csv('dqdv_data/gr.csv')
pos = pd.read_csv('dqdv_data/nmc.csv')
bol = pd.read_csv('dqdv_data/charge2_smooth.csv')
eol = pd.read_csv('dqdv_data/charge3866_smooth.csv')

fitter = amp.dqdv.DqdvFitter(neg, pos, bol)
fitter.cost_terms = ['voltage', 'dqdv', 'dvdq']
fitres2 = fitter.constrained_fit(fitter.grid_search(21).x)
fitter.cell = eol
fitres3866 = fitter.constrained_fit(fitres2.x)

table = amp.dqdv.DqdvFitTable(extra_cols=['Cycle'])
table.append(fitres2, Cycle=2)
table.append(fitres3866, Cycle=3866)

deg = amp.dqdv.calc_lam_lli(table).df
print(deg[['Cycle', 'LLI', 'LLI_std']].to_string(index=False))
```

### issue2_repro.py

```python
import pandas as pd
import ampworks as amp

# run from examples/ (pre-smoothed CSVs shipped in examples/dqdv_data)
neg = pd.read_csv('dqdv_data/gr.csv')
pos = pd.read_csv('dqdv_data/nmc.csv')
bol = pd.read_csv('dqdv_data/charge2_smooth.csv')
eol = pd.read_csv('dqdv_data/charge3866_smooth.csv')

fitter = amp.dqdv.DqdvFitter(neg, pos, bol)
fitter.cost_terms = ['voltage', 'dqdv', 'dvdq']
fitres2 = fitter.constrained_fit(fitter.grid_search(21).x)
iR_bol = float(fitres2.x[-1])

fitter.cell = eol
fitres3866 = fitter.constrained_fit(fitres2.x)  # as in simple_dQdV_example.py

print(f"fitres2.x[-1] right after the BOL fit: {iR_bol:.5f}")
print(f"fitres2.x[-1] after the EOL fit:       {fitres2.x[-1]:.5f}")

table = amp.dqdv.DqdvFitTable(extra_cols=['Cycle'])
table.append(fitres2, Cycle=2)
table.append(fitres3866, Cycle=3866)
print(table.df[['Cycle', 'iR']].to_string(index=False))
```

### issue3_hessian.py

```python
import numpy as np
import pandas as pd
import ampworks as amp

# run from examples/ (pre-smoothed CSVs shipped in examples/dqdv_data)
neg = pd.read_csv('dqdv_data/gr.csv')
pos = pd.read_csv('dqdv_data/nmc.csv')
bol = pd.read_csv('dqdv_data/charge2_smooth.csv')
eol = pd.read_csv('dqdv_data/charge3866_smooth.csv')

fitter = amp.dqdv.DqdvFitter(neg, pos, bol)
fitter.cost_terms = ['voltage', 'dqdv', 'dvdq']
x0 = fitter.grid_search(21).x

np.set_printoptions(precision=4, suppress=False)
for label, cell in [('BOL', bol), ('EOL', eol)]:
    fitter.cell = cell
    fit, opt = fitter.constrained_fit(x0, return_full=True)
    x0 = fit.x.copy()

    # same matrix constrained_fit uses for x_std = sqrt(0.5*|diag(cov)|)
    H = opt.hess
    scale = 1e-16*np.max(np.abs(np.linalg.eigvals(H)))
    cov = np.linalg.inv(H + scale*np.eye(H.shape[0]))
    C = 0.5*cov
    s = np.sqrt(np.abs(np.diag(C)))
    rho = C / np.outer(s, s)
    off = np.abs(rho[:4, :4] - np.diag(np.diag(rho[:4, :4])))

    print(label, 'x     ', fit.x)
    print(label, 'eig(H)', np.linalg.eigvalsh(0.5*(H + H.T)))
    print(label, 'diag(0.5*inv(H))', np.diag(C))
    print(label, 'x_std ', fit.x_std, ' (equal to sqrt|diag|:', np.allclose(fit.x_std, s), ')')
    print(label, 'max |offdiag(0.5*inv(H)) / outer(x_std, x_std)| over xn0..xp1:', round(float(off.max()), 3))
```

### 제안 시험 tests/test_dqdv/test_lam_lli.py

```python
import pytest
import numpy as np
import ampworks as amp

X = {'xn0': 0.05, 'xn1': 0.85, 'xp0': 0.05, 'xp1': 0.90}


def _inventory(xn0, xn1, xp0, xp1, Ah=1.):
    return xn0*Ah/(xn1 - xn0) + (1. - xp0)*Ah/(xp1 - xp0)


@pytest.mark.parametrize('name', ['xn0', 'xn1', 'xp0', 'xp1'])
def test_lli_std_single_parameter(name):
    std = 1e-3
    x_std = [std if key == name else 0. for key in X] + [0.]

    result = amp.dqdv.DqdvFitResult(
        success=True, message='', fun=0., Ah=1.,
        x=np.array([*X.values(), 0.]), x_std=np.array(x_std),
        x_map=['xn0', 'xn1', 'xp0', 'xp1', 'iR'],
    )

    table = amp.dqdv.DqdvFitTable()
    table.append(result)
    deg = amp.dqdv.calc_lam_lli(table).df

    # first-order reference from a central finite difference of Inv
    h = 1e-6
    up, dn = dict(X), dict(X)
    up[name] += h
    dn[name] -= h
    dinv = (_inventory(**up) - _inventory(**dn)) / (2.*h)
    expected = abs(dinv)*std / _inventory(**X)

    assert np.isclose(deg['LLI_std'].iloc[0], expected, rtol=1e-6)
```

### 제안 시험 (test_fitter.py 끝에 덧붙임)

```python


def test_constrained_fit_does_not_modify_x0(datasets):
    gr, nmc, cell = datasets['gr_s'], datasets['nmc_s'], datasets['cell1_s']

    fitter = amp.dqdv.DqdvFitter(gr, nmc, cell)
    assert 'voltage' in fitter.cost_terms

    # a float array with iR, e.g. a previous fit's x, should not be modified
    x0 = np.array([0.0, 0.8, 0.0, 0.9, 0.0])
    result = fitter.constrained_fit(x0)
    assert np.array_equal(x0, [0.0, 0.8, 0.0, 0.9, 0.0])

    x_saved = result.x.copy()
    _ = fitter.constrained_fit(result.x)
    assert np.array_equal(result.x, x_saved)
```

### issue1_fix.diff

```diff
--- a/src/ampworks/dqdv/_lam_lli.py
+++ b/src/ampworks/dqdv/_lam_lli.py
@@ -105,7 +105,7 @@
         ((Qn + xn0*dQn)*xn0_std)**2           # contribution from xn0
         + ((xn0*dQn)*xn1_std)**2                # contribution from xn1
         + ((-Qp + (1. - xp0)*dQp)*xp0_std)**2   # contribution from xp0
-        + (((1. - xp0)*dQp)*xn1_std)**2         # contribution from xp1
+        + (((1. - xp0)*dQp)*xp1_std)**2         # contribution from xp1
     )
 
     LLI_std = inv_std / inv[0]
```

### issue2_fix.diff

```diff
--- a/src/ampworks/dqdv/_dqdv_fitter.py
+++ b/src/ampworks/dqdv/_dqdv_fitter.py
@@ -506,7 +506,7 @@
 
         self._check_initialized('constrained_fit')
 
-        x0 = np.asarray(x0, dtype=float)
+        x0 = np.array(x0, dtype=float)
         eps = np.finfo(x0.dtype).eps
 
         # check and build bounds
```

## upstream 알림 초안 원문 (2026-10-05 · 미발송 · 발송은 사용자)

사용자에게 보낸 파일 그대로 (`fill_drafts.py` 가 위 로그 · 파일에서 기계적으로 채움). 권고 순서 (사용자 "1,2는 우리가 할 수 있는걸로 하자" ·
우리 몫은 기록까지): 이 기록으로 고정 → 사용자 중복 검색 → 1 · 2 를 같은 날 따로 → URL 을 entity 에 덧붙임 → 3 은 보류 → PR 은 maintainer 가 원할 때.

`````markdown
# ampworks upstream 알림 초안 — 미발송 (보내는 것은 사용자)

- 작성 2026-10-05 · 대상 `https://github.com/NatLabRockies/ampworks` (main `0f7a31c6` · 같은 코드가 `v0.1.0` 에도 있음)
- 들어 있는 것:

  | # | 어디에 | 내용 | 근거 |
  |---|---|---|---|
  | 1 | Issue (Bug Report 양식) | `calc_lam_lli` 의 `LLI_std` — xp1 항이 `xn1_std` 를 곱함 (브리핑이 짚은 그 줄) | 편미분 대조 + 실행 재현 + 제안 시험 (고치기 전 실패 · 고친 뒤 통과) |
  | 2 | Issue (Bug Report 양식) | `constrained_fit` 이 넘겨받은 `x0` 배열의 iR 을 제자리에서 덮어씀 — **재현하다 새로 발견** (브리핑에 없던 것) | 실행 재현 + 제안 시험 (고치기 전 실패 · 고친 뒤 통과) |
  | 3 | Discussion (선택) | 예제 자료에서 SSR Hessian 이 양정치가 아님 · `abs()` 가 음의 분산을 가림 · 대각만 전파 | 실행 출력 |

- 양식: 이 저장소의 이슈는 Bug Report 양식 (필드 다섯 개: ampworks Version · Python Version · Describe the bug · Steps to Reproduce ·
  Relevant log output) 입니다. 아래 ▶ 표시 블록의 **안쪽 글**을 해당 필드에 그대로 붙이면 됩니다. 제목 앞 `[bug]: ` 은 양식이 미리
  채워 둡니다. "Relevant log output" 필드는 자동으로 코드 블록이 되므로 백틱 없이 붙입니다.
- 3 은 질문 성격이라 Issues 가 아니라 Discussions (양식 설정의 "I just have a question..." 링크가 가리키는 곳) 가 맞습니다.
  안 보내도 됩니다. 보낸다면 1 · 2 를 먼저 보내는 편이 낫습니다.
- **넣지 않은 것**: 우리 자료 (PyBaMM 합성 truth) · A1–A3 결과 · 우리 저장소 경로 · 이름 · 연락처. 모든 재현은 ampworks 가 함께
  배포하는 예제 CSV (`examples/dqdv_data`) 와 패키지 데이터셋만 씁니다.
- PR: 초안은 "원하면 PR 을 열겠다" 는 제안까지만 합니다. 실제 PR 은 fork 가 필요하고 (이 세션은 upstream 에 push 권한이 없습니다)
  별도 결정입니다.

## 보내기 전에 확인해 주실 것 (제가 확인하지 못한 것 하나)

- **중복 여부**: git 으로 볼 수 있는 범위에서는 번호 1–39 가 전부 PR 이고 (`refs/pull/1..39/head` · `refs/pull/*/merge` 가 하나도 없어 열린 PR 도 없어 보임) — issue ·
  discussion 은 PR 과 번호를 같이 쓰므로 #39 까지는 issue 가 없습니다. #40 이후는 이 세션에서 GitHub API 로 볼 수 없어 확인하지
  못했습니다. Issues 에서 `LLI_std` · `xn1_std` · `asarray` 를 한 번 검색해 주세요.

## 검증 (모두 방금 실행한 출력 — 버리는 venv)

- 환경: ampworks 0.2.0.dev0 (main `0f7a31c6` 설치본과 파일 동일) · Python 3.11.15 · numpy 2.4.6 · scipy 1.17.1 · pandas 3.0.6.
  운영 환경 · 우리 저장소에는 아무것도 설치하지 않았습니다.
- 수정 diff 두 개는 upstream 원본에 `git apply --check` rc 0.
- 시험 — upstream `tests/test_dqdv` 기존 11 개 + 제안 5 개 (issue 1 의 4 개 · issue 2 의 1 개):

  | 변형 | 결과 |
  |---|---|
  | 배포본 (main) | 3 실패 (x0 · xn1 · xp1) · 13 통과 |
  | 108 행만 고친 사본 | 1 실패 (x0) · 15 통과 |
  | x0 복사만 고친 사본 | 2 실패 (xn1 · xp1) · 14 통과 |
  | 둘 다 고친 사본 | 16 통과 |

  기존 11 개는 네 경우 모두 통과 — 두 수정 모두 기존 시험을 깨지 않습니다.
- 로그 (스크래치패드): `amp_exp/issue/issue_checks.log` · `amp_exp/issue/issue3_hessian.log`. 아래 출력 블록은 이 로그에서 기계적으로
  옮긴 것입니다 (손으로 옮겨 적지 않음).

---

## 1. Issue — `LLI_std` uses `xn1_std` for the xp1 term

▶ **Title**

````text
[bug]: calc_lam_lli uses xn1_std for the xp1 term of LLI_std
````

▶ **ampworks Version**

````text
0.2.0.dev0 (main @ 0f7a31c); the same line is in v0.1.0
````

▶ **Python Version**

````text
3.11.15 (numpy 2.4.6, scipy 1.17.1, pandas 3.0.6)
````

▶ **Describe the bug**

````markdown
In `calc_lam_lli` ([`src/ampworks/dqdv/_lam_lli.py#L104-L111`](https://github.com/NatLabRockies/ampworks/blob/0f7a31c62cc89d8e8aac3bf1068e56044fed2bd7/src/ampworks/dqdv/_lam_lli.py#L104-L111), same line in v0.1.0), the term commented "contribution from xp1" is multiplied by `xn1_std` instead of `xp1_std`:

```python
inv_std = np.sqrt(
    ((Qn + xn0*dQn)*xn0_std)**2           # contribution from xn0
    + ((xn0*dQn)*xn1_std)**2                # contribution from xn1
    + ((-Qp + (1. - xp0)*dQp)*xp0_std)**2   # contribution from xp0
    + (((1. - xp0)*dQp)*xn1_std)**2         # contribution from xp1  <-- xn1_std
)
```

With `Inv = xn0*Qn + (1 - xp0)*Qp` and `Qp = Ah/(xp1 - xp0)`, the derivative is `dInv/dxp1 = -(1 - xp0)*Ah/(xp1 - xp0)**2 = -(1 - xp0)*dQp`, so the coefficient on that line is right and only the standard deviation is the wrong one. As a result `LLI_std` ignores the uncertainty in `xp1` and counts the uncertainty in `xn1` a second time, with the positive-electrode coefficient.

Only the `LLI_std` column is affected. `LLI`, `LAMn`, `LAMp`, `Qn`, `Qp` and their other `*_std` columns do not use this line (`xp1_std` is currently used only in `Qp_std`). On the example data in `examples/dqdv_data` (logs below), `LLI_std` changes from 0.0191 to 0.0095 at cycle 2 and from 0.0058 to 0.0084 at cycle 3866 with the fix.

**Suggested fix** (one word):

```diff
--- a/src/ampworks/dqdv/_lam_lli.py
+++ b/src/ampworks/dqdv/_lam_lli.py
@@ -105,7 +105,7 @@
         ((Qn + xn0*dQn)*xn0_std)**2           # contribution from xn0
         + ((xn0*dQn)*xn1_std)**2                # contribution from xn1
         + ((-Qp + (1. - xp0)*dQp)*xp0_std)**2   # contribution from xp0
-        + (((1. - xp0)*dQp)*xn1_std)**2         # contribution from xp1
+        + (((1. - xp0)*dQp)*xp1_std)**2         # contribution from xp1
     )
 
     LLI_std = inv_std / inv[0]
```

No test currently calls `calc_lam_lli`. A possible regression test, e.g. `tests/test_dqdv/test_lam_lli.py`, turns on one standard deviation at a time and compares `LLI_std` with a finite-difference derivative of `Inv`. On main the `xn1` and `xp1` cases fail; with the fix all four pass, and the existing tests in `tests/test_dqdv` pass either way:

```python
import pytest
import numpy as np
import ampworks as amp

X = {'xn0': 0.05, 'xn1': 0.85, 'xp0': 0.05, 'xp1': 0.90}


def _inventory(xn0, xn1, xp0, xp1, Ah=1.):
    return xn0*Ah/(xn1 - xn0) + (1. - xp0)*Ah/(xp1 - xp0)


@pytest.mark.parametrize('name', ['xn0', 'xn1', 'xp0', 'xp1'])
def test_lli_std_single_parameter(name):
    std = 1e-3
    x_std = [std if key == name else 0. for key in X] + [0.]

    result = amp.dqdv.DqdvFitResult(
        success=True, message='', fun=0., Ah=1.,
        x=np.array([*X.values(), 0.]), x_std=np.array(x_std),
        x_map=['xn0', 'xn1', 'xp0', 'xp1', 'iR'],
    )

    table = amp.dqdv.DqdvFitTable()
    table.append(result)
    deg = amp.dqdv.calc_lam_lli(table).df

    # first-order reference from a central finite difference of Inv
    h = 1e-6
    up, dn = dict(X), dict(X)
    up[name] += h
    dn[name] -= h
    dinv = (_inventory(**up) - _inventory(**dn)) / (2.*h)
    expected = abs(dinv)*std / _inventory(**X)

    assert np.isclose(deg['LLI_std'].iloc[0], expected, rtol=1e-6)
```

I'm happy to open a PR with the fix and the test if that helps.
````

▶ **Steps to Reproduce**

````markdown
1. A single table row with one nonzero standard deviation (no fitting needed):

```python
import numpy as np
import ampworks as amp

x = {'xn0': 0.05, 'xn1': 0.85, 'xp0': 0.05, 'xp1': 0.90}


def inventory(xn0, xn1, xp0, xp1, Ah=1.0):
    return xn0*Ah/(xn1 - xn0) + (1.0 - xp0)*Ah/(xp1 - xp0)


def lli_std(x_std):
    result = amp.dqdv.DqdvFitResult(
        success=True, message='', fun=0.0, Ah=1.0,
        x=np.array([*x.values(), 0.0]), x_std=np.array([*x_std, 0.0]),
        x_map=['xn0', 'xn1', 'xp0', 'xp1', 'iR'],
    )
    table = amp.dqdv.DqdvFitTable()
    table.append(result)
    return amp.dqdv.calc_lam_lli(table).df['LLI_std'].iloc[0]


h = 1e-6
for i, name in enumerate(x):
    std = [0.0]*4
    std[i] = 0.01
    up, dn = dict(x), dict(x)
    up[name] += h
    dn[name] -= h
    expected = abs(inventory(**up) - inventory(**dn))/(2*h)*0.01/inventory(**x)
    print(f"only {name}_std = 0.01:  LLI_std = {lli_std(std):.6f}"
          f"   first-order expected = {expected:.6f}")
```

2. The dQdV example data — run from `examples/`, using the pre-smoothed CSVs shipped in `examples/dqdv_data` (same flow as `simple_dQdV_example.py`):

```python
import pandas as pd
import ampworks as amp

# run from examples/ (pre-smoothed CSVs shipped in examples/dqdv_data)
neg = pd.read_csv('dqdv_data/gr.csv')
pos = pd.read_csv('dqdv_data/nmc.csv')
bol = pd.read_csv('dqdv_data/charge2_smooth.csv')
eol = pd.read_csv('dqdv_data/charge3866_smooth.csv')

fitter = amp.dqdv.DqdvFitter(neg, pos, bol)
fitter.cost_terms = ['voltage', 'dqdv', 'dvdq']
fitres2 = fitter.constrained_fit(fitter.grid_search(21).x)
fitter.cell = eol
fitres3866 = fitter.constrained_fit(fitres2.x)

table = amp.dqdv.DqdvFitTable(extra_cols=['Cycle'])
table.append(fitres2, Cycle=2)
table.append(fitres3866, Cycle=3866)

deg = amp.dqdv.calc_lam_lli(table).df
print(deg[['Cycle', 'LLI', 'LLI_std']].to_string(index=False))
```
````

▶ **Relevant log output**

````text
# step 1, main @ 0f7a31c
only xn0_std = 0.01:  LLI_std = 0.011254   first-order expected = 0.011254
only xn1_std = 0.01:  LLI_std = 0.011161   first-order expected = 0.000662
only xp0_std = 0.01:  LLI_std = 0.001173   first-order expected = 0.001173
only xp1_std = 0.01:  LLI_std = 0.000000   first-order expected = 0.011142

# step 1, with the fix
only xn0_std = 0.01:  LLI_std = 0.011254   first-order expected = 0.011254
only xn1_std = 0.01:  LLI_std = 0.000662   first-order expected = 0.000662
only xp0_std = 0.01:  LLI_std = 0.001173   first-order expected = 0.001173
only xp1_std = 0.01:  LLI_std = 0.011142   first-order expected = 0.011142

# step 2, main @ 0f7a31c
 Cycle      LLI  LLI_std
     2 0.000000 0.019061
  3866 0.110284 0.005784

# step 2, with the fix
 Cycle      LLI  LLI_std
     2 0.000000 0.009471
  3866 0.110284 0.008352
````

---

## 2. Issue — `constrained_fit` modifies the caller's `x0`

▶ **Title**

````text
[bug]: constrained_fit overwrites iR in the caller's x0 array (e.g. a previous fit's x)
````

▶ **ampworks Version**

````text
0.2.0.dev0 (main @ 0f7a31c); the same two lines are in v0.1.0
````

▶ **Python Version**

````text
3.11.15 (numpy 2.4.6, scipy 1.17.1, pandas 3.0.6)
````

▶ **Describe the bug**

````markdown
`DqdvFitter.constrained_fit` converts the starting guess with `x0 = np.asarray(x0, dtype=float)` ([L509](https://github.com/NatLabRockies/ampworks/blob/0f7a31c62cc89d8e8aac3bf1068e56044fed2bd7/src/ampworks/dqdv/_dqdv_fitter.py#L509)) and later sets `x0[-1] = iR0` ([L528](https://github.com/NatLabRockies/ampworks/blob/0f7a31c62cc89d8e8aac3bf1068e56044fed2bd7/src/ampworks/dqdv/_dqdv_fitter.py#L528)). When `x0` is already a float64 NumPy array of length 5, `np.asarray` returns the same object, so the caller's array is changed in place. That is exactly the case when a previous result is passed back in, as the example does with `fitter.constrained_fit(fitres2.x)`: the previous result's fitted iR is replaced by the new starting iR. A `grid_search` result passed in is changed the same way.

In `examples/simple_dQdV_example.py` this means `fitres2.x[-1]` changes when `fitres3866` is fitted, so the cycle-2 row that is appended to `fit_table` afterwards carries the starting iR of the EOL fit instead of the fitted BOL iR (with the pre-smoothed CSVs: 0.0153 instead of 0.0278, logs below). The window values (`xn0` … `xp1`), `x_std` and the LAM/LLI results are not affected; the iR stored in `fitres2.x` and in the table's `iR` column are.

The existing `test_constrainted_fit` passes an int array or a list, for which `np.asarray(..., dtype=float)` already makes a copy, so it does not exercise this case.

**Suggested fix:** copy the input.

```diff
--- a/src/ampworks/dqdv/_dqdv_fitter.py
+++ b/src/ampworks/dqdv/_dqdv_fitter.py
@@ -506,7 +506,7 @@
 
         self._check_initialized('constrained_fit')
 
-        x0 = np.asarray(x0, dtype=float)
+        x0 = np.array(x0, dtype=float)
         eps = np.finfo(x0.dtype).eps
 
         # check and build bounds
```

A possible test, appended to `tests/test_dqdv/test_fitter.py` (uses the existing `datasets` fixture). It fails on main and passes with the fix:

```python
def test_constrained_fit_does_not_modify_x0(datasets):
    gr, nmc, cell = datasets['gr_s'], datasets['nmc_s'], datasets['cell1_s']

    fitter = amp.dqdv.DqdvFitter(gr, nmc, cell)
    assert 'voltage' in fitter.cost_terms

    # a float array with iR, e.g. a previous fit's x, should not be modified
    x0 = np.array([0.0, 0.8, 0.0, 0.9, 0.0])
    result = fitter.constrained_fit(x0)
    assert np.array_equal(x0, [0.0, 0.8, 0.0, 0.9, 0.0])

    x_saved = result.x.copy()
    _ = fitter.constrained_fit(result.x)
    assert np.array_equal(result.x, x_saved)
```

I'm happy to include this in the same PR as the `LLI_std` fix if that is easier.
````

▶ **Steps to Reproduce**

````markdown
Run from `examples/` (pre-smoothed CSVs shipped in `examples/dqdv_data`, same order as `simple_dQdV_example.py`):

```python
import pandas as pd
import ampworks as amp

# run from examples/ (pre-smoothed CSVs shipped in examples/dqdv_data)
neg = pd.read_csv('dqdv_data/gr.csv')
pos = pd.read_csv('dqdv_data/nmc.csv')
bol = pd.read_csv('dqdv_data/charge2_smooth.csv')
eol = pd.read_csv('dqdv_data/charge3866_smooth.csv')

fitter = amp.dqdv.DqdvFitter(neg, pos, bol)
fitter.cost_terms = ['voltage', 'dqdv', 'dvdq']
fitres2 = fitter.constrained_fit(fitter.grid_search(21).x)
iR_bol = float(fitres2.x[-1])

fitter.cell = eol
fitres3866 = fitter.constrained_fit(fitres2.x)  # as in simple_dQdV_example.py

print(f"fitres2.x[-1] right after the BOL fit: {iR_bol:.5f}")
print(f"fitres2.x[-1] after the EOL fit:       {fitres2.x[-1]:.5f}")

table = amp.dqdv.DqdvFitTable(extra_cols=['Cycle'])
table.append(fitres2, Cycle=2)
table.append(fitres3866, Cycle=3866)
print(table.df[['Cycle', 'iR']].to_string(index=False))
```
````

▶ **Relevant log output**

````text
# main @ 0f7a31c
fitres2.x[-1] right after the BOL fit: 0.02783
fitres2.x[-1] after the EOL fit:       0.01530
 Cycle       iR
     2 0.015299
  3866 0.021082

# with np.array(x0, dtype=float)
fitres2.x[-1] right after the BOL fit: 0.02783
fitres2.x[-1] after the EOL fit:       0.02783
 Cycle       iR
     2 0.027830
  3866 0.021082
````

---

## 3. Discussion (선택) — `x_std` when the SSR Hessian is not positive definite

▶ **Title**

````text
x_std when the SSR Hessian is not positive definite (dQdV example data)
````

▶ **Body**

````markdown
While checking the uncertainty outputs on the dQdV example data (pre-smoothed CSVs, `cost_terms = ['voltage', 'dqdv', 'dvdq']`, BOL from `grid_search(21)`, EOL started from the BOL result), I noticed that the numerical SSR Hessian that `constrained_fit` inverts for `x_std` is not positive definite at the returned `x`:

- cycle 2: smallest eigenvalue -1959.1; the diagonal of `0.5*inv(H)` is negative for `xn0` and `xp0`
- cycle 3866: smallest eigenvalue -142847.2; the diagonal is negative for `xn0`

Since `x_std = sqrt(0.5*|diag(inv(H))|)`, the negative entries become positive standard deviations (e.g. `xp0_std` = 0.0123 at cycle 2 comes from a negative entry), and the off-diagonal entries of `0.5*inv(H)` divided by the corresponding products of the reported `x_std` reach magnitudes of 10.461 (cycle 2) and 1.734 (cycle 3866), so the matrix is not a valid covariance at these points. I assume this is because `x` minimizes the MAPE objective rather than the SSR (the docstring already describes the estimate as a heuristic).

Two suggestions, in case they are useful:

1. Warn (or return NaN) when the Hessian is not positive definite or `diag(cov)` has negative entries, instead of taking `abs()`.
2. `calc_lam_lli` propagates the four window standard deviations as independent, while the fitter has the full matrix. Where the covariance is valid, propagating with it (`g @ C @ g`) would include the correlations between the window parameters. Similarly, `LAM*_std` and `LLI_std` include only the current row's uncertainty, not that of the reference row 0.

Script (run from `examples/`):

```python
import numpy as np
import pandas as pd
import ampworks as amp

# run from examples/ (pre-smoothed CSVs shipped in examples/dqdv_data)
neg = pd.read_csv('dqdv_data/gr.csv')
pos = pd.read_csv('dqdv_data/nmc.csv')
bol = pd.read_csv('dqdv_data/charge2_smooth.csv')
eol = pd.read_csv('dqdv_data/charge3866_smooth.csv')

fitter = amp.dqdv.DqdvFitter(neg, pos, bol)
fitter.cost_terms = ['voltage', 'dqdv', 'dvdq']
x0 = fitter.grid_search(21).x

np.set_printoptions(precision=4, suppress=False)
for label, cell in [('BOL', bol), ('EOL', eol)]:
    fitter.cell = cell
    fit, opt = fitter.constrained_fit(x0, return_full=True)
    x0 = fit.x.copy()

    # same matrix constrained_fit uses for x_std = sqrt(0.5*|diag(cov)|)
    H = opt.hess
    scale = 1e-16*np.max(np.abs(np.linalg.eigvals(H)))
    cov = np.linalg.inv(H + scale*np.eye(H.shape[0]))
    C = 0.5*cov
    s = np.sqrt(np.abs(np.diag(C)))
    rho = C / np.outer(s, s)
    off = np.abs(rho[:4, :4] - np.diag(np.diag(rho[:4, :4])))

    print(label, 'x     ', fit.x)
    print(label, 'eig(H)', np.linalg.eigvalsh(0.5*(H + H.T)))
    print(label, 'diag(0.5*inv(H))', np.diag(C))
    print(label, 'x_std ', fit.x_std, ' (equal to sqrt|diag|:', np.allclose(fit.x_std, s), ')')
    print(label, 'max |offdiag(0.5*inv(H)) / outer(x_std, x_std)| over xn0..xp1:', round(float(off.max()), 3))
```

Output (main @ 0f7a31c):

```text
BOL x      [0.0377 0.8486 0.0177 0.9072 0.0278]
BOL eig(H) [ -1959.1474    397.9259   1197.564    7445.6618 157368.5997]
BOL diag(0.5*inv(H)) [-4.4398e-08  3.1014e-04 -1.5072e-04  7.5021e-05  1.2548e-03]
BOL x_std  [0.0002 0.0176 0.0123 0.0087 0.0354]  (equal to sqrt|diag|: True )
BOL max |offdiag(0.5*inv(H)) / outer(x_std, x_std)| over xn0..xp1: 10.461
EOL x      [0.0053 0.7566 0.002  0.9088 0.0211]
EOL eig(H) [-142847.1627     398.8669    4540.1683  157745.7603  267796.5603]
EOL diag(0.5*inv(H)) [-5.0080e-08  3.5096e-05  4.2365e-06  7.3265e-05  1.2527e-03]
EOL x_std  [0.0002 0.0059 0.0021 0.0086 0.0354]  (equal to sqrt|diag|: True )
EOL max |offdiag(0.5*inv(H)) / outer(x_std, x_std)| over xn0..xp1: 1.734
```
````
`````

(해석은 raw 가 아니라 위키 페이지 `entities/ampworks.md` 에 둔다.)
