---
source_url: https://github.com/NatLabRockies/ampworks
ingested: 2026-10-05
sha256: 215a56041b83ad4628f11e945fddf7deca979e791c4a31168bbf1d362026e6be
---

수집 목적: (1) 의존성 위험 감시 — 우리가 쓰는 도구(PyBaMM 등) 릴리스가 합성 truth·재현성에 주는 영향 판정 · (2) 방법 비교·경쟁 도구 — OCV/DVA 피팅 도구를 degeneracy 질문과 비교 · (3) 미세단락 도구 탐색 · (4) 실험 아이디어 저장 (착수는 별도 승인). 2026-10-01 사용자 결정 — 앞으로 매일 오는 브리핑의 처리 기준.

---

# GitHub 연구 브리핑 — 2026-10-05 전달분 (사용자가 2026-10-05 채팅으로 전달한 원문 · 항목 2 만)

사용자 채팅 원문: "관련해서 github 인사이트 내용 왔어 확인해봐" — 아래 브리핑 본문은 항목 **2** 부터 붙여 넣은 것이다 (항목 1 은 이 채팅에 없다 ·
끝 문단의 "두 도구" 중 하나는 받지 못한 항목 1 의 도구다).

2. ampworks: LLI/LAM 분석 후보, 우선 watch만
저율 전지·반쪽전지 곡선의 전압·ICA·DVA 피팅 도구예요. BSD-3-Clause, NMC/흑연 초기·열화 예제와 CSV·테스트가 있고 최신 main 변경은 9월 23일이에요. 오늘 새로 찾은 후보예요.
주의점도 발견했어요. LLI 불확도 계산에서 xp1 기여항에 xn1_std가 쓰여 정적 코드상 변수 혼동 가능성이 있어요. 직접 실행해 재현하진 않았으므로, 불확도 출력을 검증하기 전 분석 채택은 보류하는 편이 좋아요. 미세단락 판별이나 ASSB 열화 원인 확정 도구로 볼 수도 없어요.
[저장소](https://github.com/NatLabRockies/ampworks) · [확인할 계산부](https://github.com/NatLabRockies/ampworks/blob/0f7a31c62cc89d8e8aac3bf1068e56044fed2bd7/src/ampworks/dqdv/_lam_lli.py#L104-L111)

이번 조사에서는 추가 추천할 만큼 검증된 미세단락 전용 새 후보는 없었어요. 보유 저장소의 기본 브랜치 검색에서는 두 도구 사용을 확인하지 못했지만, 다른 브랜치까지 중복 여부를 확인한 것은 아니에요.

---

## 수집 시 1차 대조 (2026-10-05 · 공개 저장소를 git 으로 직접 받아 읽은 원문 — WebFetch 요약 아님 · GitHub API 아님 · ampworks 코드 실행 0)

### 2. ampworks

- `NatLabRockies/ampworks` 를 얕게 clone (`/home/user/natlabrockies/ampworks` · 우리 저장소 밖). 기본 가지 `main` 끝
  `0f7a31c62cc89d8e8aac3bf1068e56044fed2bd7` — 커밋 시각 2026-09-23 09:51:59 −0600 · 작성자 Corey R. Randall · 제목 "Merge pull request #39
  from NatLabRockies/feature/interactive-show". 브리핑 링크의 커밋이 수집 시점의 main 끝 그대로다.
- `LICENSE` 첫 줄 "BSD 3-Clause License" · "Copyright (c) 2025, Alliance for Energy Innovation, LLC". `pyproject.toml`: `license = "BSD-3-Clause"` ·
  `requires-python = ">=3.11,<3.16"` · `src/ampworks/__init__.py` `__version__ = '0.2.0.dev0'` · 의존 `tqdm` `xlrd` `numpy` `bokeh` `polars` `plotly`
  `IPython` `pyarrow` `seaborn` `openpyxl` `fastexcel` `matplotlib` `numdifftools` `pandas >= 3.0` `scipy >= 1.13` · 선택 `gui` (`dash` `dash-ag-grid` …).
- `CHANGELOG.md` 원문 한 줄: "Rebrand NREL to NLR, and include name change for Alliance as well ([#15](https://github.com/NatLabRockies/ampworks/pull/15))".
- 원격 ref (`git ls-remote`): 가지 `main` · `v0.0.x` · `v0.1.x` · 태그 `v0.0.1` · `v0.1.0` · PR head `pull/1` … `pull/39` (#39 = main 끝의 병합).
- 모듈: `src/ampworks/` 아래 `dqdv` · `gitt` · `ici` · `hppc` · `ocv` · `datasets` · `plotutils` · `utils` · `columns` · `_core`.
- 예제: `examples/simple_dQdV_example.py` + `examples/dqdv_data/` — `gr.csv` (187 줄) · `nmc.csv` (344 줄) = 반쪽전지 (이미 평활) · `charge2.csv`
  (793 줄 · 예제 주석 원문 "beginning of life (BOL, cycle 2)") · `charge3866.csv` (1,049 줄 · "end of life (EOL, cycle 3866)") · 각 `_smooth.csv`.
  예제 주석 원문: "Calculating LAM and LLI by fitting dQdV curves requires low-rate data from negative and positive electrode half cells, as well as
  for the full cell." 패키지 자료 `src/ampworks/datasets/resources/dqdv/` 의 parquet 6.
- 시험: `tests/test_dqdv/test_fitter.py` 377 줄 · 시험 함수 11 (`test_check_dataframe` · `test_build_splines` · `test_check_initialized` ·
  `test_err_func` · `test_data_setters` · `test_cost_terms_setter` · `test_get_funcs` · `test_err_terms` · `test_grid_search` ·
  `test_constrainted_fit` · `test_plot`). `grep -rn "calc_lam_lli\|LLI_std\|xp1_std\|xn1_std" tests/` → **0 건** — LAM/LLI 계산과 그 불확도를
  부르는 시험은 없다.
- `src/ampworks/dqdv/_lam_lli.py` (218 줄) 원문 81–111행:

```python
    xn0, xn0_std = df.xn0.to_numpy(), df.xn0_std.to_numpy()
    xn1, xn1_std = df.xn1.to_numpy(), df.xn1_std.to_numpy()
    xp0, xp0_std = df.xp0.to_numpy(), df.xp0_std.to_numpy()
    xp1, xp1_std = df.xp1.to_numpy(), df.xp1_std.to_numpy()

    Qn = Ah / (xn1 - xn0)
    Qp = Ah / (xp1 - xp0)

    dQn = Ah / (xn1 - xn0)**2  # ignore lead -1 for xn1 b/c **2 below
    Qn_std = np.sqrt((dQn*xn1_std)**2 + (dQn*xn0_std)**2)

    dQp = Ah / (xp1 - xp0)**2  # ignore lead -1 for xp1 b/c **2 below
    Qp_std = np.sqrt((dQp*xp1_std)**2 + (dQp*xp0_std)**2)

    LAMn = 1. - Qn / Qn[0]
    LAMp = 1. - Qp / Qp[0]

    LAMn_std = Qn_std / Qn[0]
    LAMp_std = Qp_std / Qp[0]

    inv = xn0*Qn + (1. - xp0)*Qp
    LLI = 1. - inv / inv[0]

    inv_std = np.sqrt(
        ((Qn + xn0*dQn)*xn0_std)**2           # contribution from xn0
        + ((xn0*dQn)*xn1_std)**2                # contribution from xn1
        + ((-Qp + (1. - xp0)*dQp)*xp0_std)**2   # contribution from xp0
        + (((1. - xp0)*dQp)*xn1_std)**2         # contribution from xp1
    )

    LLI_std = inv_std / inv[0]
```

- 같은 108행 ("contribution from xp1" 항이 `xn1_std` 를 곱함) 이 태그 `v0.1.0` · 가지 `v0.1.x` (둘 다 `e7124d4` · 2026-04-28 10:44:42 −0600) 의
  같은 파일에도 있다. `v0.0.1` (`1bfab87`) · `v0.0.x` (`afb6d20`) 의 `src/` 에는 `LLI_std` · `inv_std` 가 없다.
- 표준편차의 출처 `src/ampworks/dqdv/_dqdv_fitter.py` 원문 588–596행: `opt_result.hess = Hessian(ssr)(opt_result.x)` (numdifftools) ·
  `scale = 1e-16*np.max(np.abs(evals))` · `cov = np.linalg.inv(opt_result.hess + scale*np.eye(size))` · `std = np.sqrt(0.5*np.abs(np.diag(cov)))`.
  같은 함수 docstring 원문: "all fitting routines use a mean absolute percent error (MAPE) function, but the uncertainty approximation needs a sum
  of squared residuals error function" · "These bounds provide more of a heuristic interpretation of the confidence intervals rather than a
  statistical interpretation." `constrained_fit` 의 제약 원문: `opt.LinearConstraint([[1, -1, 0, 0, 0]], -np.inf, 0.)` ·
  `opt.LinearConstraint([[0, 0, 1, -1, 0]], -np.inf, 0.)` (전극마다 x0 < x1) + 초기값 ± `bounds` 상자 (`np.clip(bounds, 1e-3, 1.)` · [0, 1] 안) ·
  `method='trust-constr'` · 파라미터 `x_map=['xn0', 'xn1', 'xp0', 'xp1', 'iR']`.
- `calc_lam_lli` docstring 원문 (불확도 부분): "If standard deviations of the x0/x1 stoichiometries are available in `results` (and are not NaN),
  then they are propagated to give uncertainty estimates for the LAM/LLI values. Reported uncertainties come from first-order Taylor series
  assumptions. If you trust your x0/x1 fits but see large or inconsistent uncertainties then it is also safe to trust the LAM/LLI values, but you
  may want to neglect LAM/LLI uncertainties."

### 우리 저장소에서의 사용 (브리핑이 "다른 브랜치까지는 확인하지 않았다" 고 한 부분)

로컬 원격 추적 가지 28 개 (마지막 fetch 시점의 끝) 를 `git grep -l -i ampworks <가지> -- <텍스트 · 코드 확장자>` 로 읽었다 (데이터 blob 은
읽지 않았다 · 확장자 목록은 아래 첫 줄). 첫 검색 (가지당 240 s 제한) 에서 시간 초과한 가지는 같은 pathspec · 1800 s 제한으로 다시 읽었다.
결과: **없음 (28 가지 모두 · 첫 검색에서 시간 초과한 3 가지는 재시도에서 없음)**. 원문 출력 둘:

```
# 2026-10-05T00:14:11Z · pathspec: *.py *.md *.txt *.toml *.cfg *.ini *.yaml *.yml *.ipynb *.json *.sh *.ps1 *.js *.ts *.tsx *.html
origin/Codex/dem-mpm-crosscheck | 2026-08-07 | 없음
origin/Codex/friendly-meitner-lldvar | 2026-08-08 | 없음
origin/claude/14-gate-code-review-9qkx05 | 2026-10-02 | 없음
origin/claude/battery-charge-discharge-webapp-dq4ja3 | 2026-09-25 | 없음
origin/claude/battery-charge-discharge-webapp-vag24d | 2026-08-24 | 없음
origin/claude/bms-alpha-beta-verify | 2026-09-14 | 없음
origin/claude/dashboard-standby-e2f56971 | 2026-10-04 | 없음
origin/claude/dft-script-generator-webapp-GPSAG | 2026-03-26 | 없음
origin/claude/evac-2026-09-28 | 2026-09-28 | 없음
origin/claude/friendly-meitner-lldvar | 2026-09-28 | 없음
origin/claude/gate80-standby-9a26dd5f | 2026-09-30 | 없음
origin/claude/li2s-assb-wiki | 2026-09-11 | 없음
origin/claude/market-research-presentation-bC9Yi | 2026-04-17 | 없음
origin/claude/md-status-monitoring-q2xbu1 | 2026-08-24 | 없음
origin/claude/midni-formation-wiki | 2026-09-11 | 없음
origin/claude/phase-a-96arm-kgy | 2026-09-12 | TIMEOUT
origin/claude/resistor-network-solver-LDjW6 | 2026-07-21 | 없음
origin/claude/review-ml-migration-1BN1c | 2026-05-06 | 없음
origin/claude/sdcp-dem-manuscript-si-pqwtv8 | 2026-09-28 | TIMEOUT
origin/claude/solid-state-cathode-improvement-hevry0 | 2026-07-15 | 없음
origin/claude/stoic-knuth-NObVQ | 2026-09-28 | TIMEOUT
origin/claude/windows-reinstall-backup-oducnh | 2026-08-24 | 없음
origin/claude/zip-git-gpu-setup-vdqdtd | 2026-08-28 | 없음
origin/main | 2026-03-25 | 없음
origin/manuscript-track | 2026-09-03 | 없음
origin/nihonchizu | 2026-09-27 | 없음
origin/rescue/lineage-2026-06-nd-pair01 | 2026-06-16 | 없음
origin/review/defective-cell-ml-v2.0.0 | 2026-09-16 | 없음
# DONE 2026-10-05T00:42:59Z · origin 의 현재 가지 수 29
```

```
# 2026-10-05T01:35:10Z · 재시도 (첫 검색 TIMEOUT 셋) · 같은 pathspec · timeout 1800 s
origin/claude/phase-a-96arm-kgy | 2026-09-12 | 없음 | 20 s
origin/claude/sdcp-dem-manuscript-si-pqwtv8 | 2026-09-28 | 없음 | 161 s
origin/claude/stoic-knuth-NObVQ | 2026-09-28 | 없음 | 3 s
# DONE 2026-10-05T01:38:14Z
```
