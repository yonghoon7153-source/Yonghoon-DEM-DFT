---
source_url: (채팅 원문 · 링크는 본문 블록 안 — PyBaMM PR 5835 · 5875 · 5883 · 5888 · 릴리스 26.10.0.0 · ocvfit · Short-circuit-resistance-estimator · impedance.py)
ingested: 2026-10-13
sha256: 892524f4d5af10c4d6fc99d4ded291aef0a334e4ca65464679aff83e8a1ecf59
---

수집 목적: 2026-10-01 사용자 결정의 브리핑 처리 기준 (의존성 위험 감시 · 경쟁 도구 · 미세단락 도구 · 실험 아이디어 — 착수는 별도 승인) · 사용자 지시 2026-10-13 "좀 많은데 천천히 훑어보고 우리가 참고할만한것 있으면 가져오자".

---

# GitHub 연구 브리핑 — 2026-10-12~13 전달분 (사용자 채팅 원문 · 항목 7)

아래 블록은 채팅 원문 그대로다 (마지막 줄의 사용자 지시까지 · 블록 자체의 sha256 = `5691e7e80a0a9106cb29d716486f1f1e57b9d7373e9b8552a37ecb6e71785be6` · 끝 줄바꿈 포함 · frontmatter 의 sha256 은 위키 규칙대로 본문 전체). 원문의 링크 13 개는 블록 안에 그대로 있다.

```text
PyBaMM #5835: 이방성 수송계수 지원
10월 6일 병합된 PR이에요. 코드·추가 테스트와 CI 통과를 확인했으며 BSD-3-Clause예요. 아직 정식판 26.9.0.0에 포함되지 않은 main 변경이에요
DEM→voxel에서 얻은 방향별 유효 수송계수를 연속체 모델에 연결할 후보예요. 다만 면 법선 성분만 사용하고 접선 성분은 생략하므로, 회전된 일반 이방성 텐서에 그대로 적용하면 안 돼요. ASSB 접촉손실·균열 모델 자체가 추가된 것도 아니에요
즉시 적용보다는 정식 릴리스와 후속 수치 구현 watch를 추천해요
해당 PR · CI
https://github.com/pybamm-team/PyBaMM/pull/5835
https://github.com/pybamm-team/PyBaMM/actions/runs/37505719417

PyBaMM #5875 — 열화 발열 누락 수정
10월 8일 열린 PR로, SEI 성장·균열 위 SEI·리튬 도금의 발열을 추가해요. 실제 코드와 DFN 에너지수지 시험 3개, 해당 버전 CI 통과를 확인했어요. BSD-3-Clause예요
정상 열화의 발열을 미세단락 신호로 오인하지 않도록 기준 모델을 점검하는 데 유용하겠어요. 아직 미병합이며, 선행 #5841의 최신 보완도 모두 포함된 상태는 아니에요. 실험 검증이나 ASSB 계면 열화 모델은 아니므로 우선 PR watch를 추천해요
PR #5875 · CI
https://github.com/pybamm-team/PyBaMM/pull/5875
https://github.com/pybamm-team/PyBaMM/actions/runs/37823061290

Short-circuit-resistance-estimator — 누설저항 추정 비교용
최신 코드는 2024년 6월 4일로 오래됐지만, 전처리·학습·평가 코드와 분할 데이터 파일이 있어요. MIT 코드이며 외부 병렬저항을 연결한 실험을 바탕으로 해요. 자연 발생 내부단락 검증과는 구분해야 해요
코드에서 중첩창 생성 후 무작위 분할하고 전체 입력으로 정규화를 학습하는 부분을 확인했어요. 데이터 누출 위험 때문에 기존 정확도를 새 셀 성능으로 받아들이기 어려워요. 자동시험·의존성 명세와 데이터 별도 라이선스도 확인되지 않아, 바로 fork해 채택하기보다 셀별 분할로 재검증할 비교 대상으로만 권해요
저장소
https://github.com/orDrink/Short-circuit-resistance-estimator

PyBaMM 26.10.0.0 — LLI 계산 수정이 정식판에 포함됐어요
한국시간 오늘 00:20에 출시됐어요. 공간적으로 활물질 분율이 다른 전극에서 LLI가 잘못 계산되던 #5813 수정이 포함됐어요. 프로젝트가 이전 변경기록의 버전 배치를 정정했고, 이 수정은 26.9가 아닌 26.10에 처음 포함된다고 밝혔어요
코드·회귀시험과 주요 CI·배포 성공을 확인했어요. 다만 벤치마크 작업 2개는 실패했어요. BSD-3-Clause이며 릴리스 watch를 추천해요. 어제 소개한 열화 발열 #5875는 아직 미병합이라 이번 판에도 없어요
적용: 조성 구배 전극의 LLI를 해석하기 전 계산 오차를 제거하는 데 유용해요. 실험에서 열화 원인을 판별했다는 증거는 아니에요
릴리스 · 변경기록 정정 PR
https://github.com/pybamm-team/PyBaMM/releases/tag/pybamm-v26.10.0.0
https://github.com/pybamm-team/PyBaMM/pull/5883

ocvfit — LLI/LAM과 ‘구분할 수 없는 경우’를 함께 보는 신생 후보
10월 9일 공개된 MIT 저장소예요. 전지·반쪽전지 OCV를 맞춰 LLI와 양극·음극 LAM을 추정하고, 불확실성과 반쪽전지 곡선 오차를 점검해요. 코드·예제 5개·다중 Python 버전 CI 통과를 확인했어요
특히 LFP 평탄부의 끝이 관측되지 않으면 양극 LAM을 식별 불가로 표시하는 시험이 있어요. 단순 SOH 예측보다 열화 원인 분리 연구에 직접적인 후보라 우선 watch를 추천해요
아직 정식 릴리스와 실측 검증은 없고 예제는 합성 데이터예요. OCV만으로 부반응에 의한 Li 손실과 비활성 물질에 갇힌 Li를 완전히 분리할 수는 없어요. 코드의 R도 저항이 아니라 전압 오프셋이므로 미세단락 누설저항으로 해석하면 안 돼요
저장소 · 식별 가능성 시험 · CI
https://github.com/catnap042/ocvfit
https://github.com/catnap042/ocvfit/blob/main/tests/test_lfp_identifiability.py
https://github.com/catnap042/ocvfit/actions/runs/37951935842
작은 검증 제안: ocvfit에 알려진 LLI·LAM을 넣은 합성 곡선을 만들고, 전체 SOC 구간과 잘린 구간을 비교해 보세요. 반쪽전지 곡선에 작은 전압 오차도 넣어, 정답을 포함하는 불확실성 범위를 주는지와 식별 불가를 제대로 표시하는지부터 확인하는 편이 좋아요

피카 ⚡ 10월 12일 GitHub 인사이트는 2건이에요

1. impedance.py v1.8.0 — EIS 검증 도구, 배포 복구를 기다려 주세요
오늘 03:46 KST GitHub 릴리스가 나왔어요. NumPy 2에서 Lin-KK 계산이 깨지던 기존 수정 #322를 포함해요. MIT이며 문서·예제 데이터·시험 코드가 있고, 태그 CI는 Python 3.10~3.14에서 통과했어요
다만 PyPI 게시 작업은 실패했고, 확인 시점 PyPI는 아직 1.7.1이에요. 바로 업그레이드하기보다 배포 복구 watch를 추천해요
활용: 열화 셀 EIS를 해석하기 전 데이터의 Lin-KK 일관성을 점검하는 후보예요. 통과 자체가 미세단락·LLI/LAM·ASSB 접촉손실의 원인을 구분해 주지는 않아요
[릴리스](https://github.com/ECSHackWeek/impedance.py/releases/tag/v1.8.0) · [수정 PR](https://github.com/ECSHackWeek/impedance.py/pull/322) · [배포 작업](https://github.com/ECSHackWeek/impedance.py/actions/runs/38165210646/job/114548096985)

https://github.com/ECSHackWeek/impedance.py/releases/tag/v1.8.0
https://github.com/ECSHackWeek/impedance.py/pull/322
https://github.com/ECSHackWeek/impedance.py/actions/runs/38165210646/job/114548096985

작은 검증 제안: 제공된 스펙트럼과 합성 RC 데이터를 NumPy 2 환경에서 처리하고, 같은 설정의 pyimpspec 결과와 잔차를 비교해 보세요. 이후 실측 셀에 적용할 때는 SOC·온도를 맞추고, 미세단락 여부는 독립적인 자기방전·누설 측정으로 확인해야 해요

PyBaMM #5888 — Ai2020 수정에 검증 근거가 추가됐어요
앞서 소개한 확산계수 단위 수정에 10월 12일 리뷰 승인·본체 CI 통과와 실험 비교가 추가됐어요. BSD-3-Clause이며 여전히 미병합이라 26.10 릴리스에는 없어요
기여자는 공개 Enertech 2C 비교에서 전압 RMSE가 123.0→54.2 mV로 줄었다고 보고했어요. 제가 직접 재실행한 수치는 아니에요. Ai2020 기반 열화 피팅에서 잘못된 수송계수를 열화 파라미터가 대신 보상하는 위험을 줄일 근거가 보강됐어요
병합·다음 릴리스 watch를 추천해요. 미세단락 판별 기능이 추가된 것은 아니에요
PR · 기여자의 실험 비교
https://github.com/pybamm-team/PyBaMM/pull/5888
https://github.com/pybamm-team/PyBaMM/pull/5888#issuecomment-6119558212

좀 많은데 천천히 훑어보고 우리가 참고할만한것 있으면 가져오자
```

## 1차 대조 (2026-10-13 · 공개 저장소를 git 으로 직접 받아 읽은 원문 · 받은 코드 · 시험 실행 0 · 저장소 밖 스크래치패드)

### PyBaMM — 태그 · 변경기록 · 소스 (정적)

- `git ls-remote --tags https://github.com/pybamm-team/pybamm`: `refs/tags/pybamm-v26.10.0.0` = `b5f49ae19442ca5a8c53c853bcf39cfdb347344d` ·
  `refs/tags/pybamm-v26.9.0.0` = `26778979a057ec9f18e9c8dba6d2c26ac892bea3`.
- 26.10 태그 커밋 (depth 1 fetch): `b5f49ae1… 2026-10-09T16:12:53+01:00 Release v26.10.0.0 (#5883)` · `CHANGELOG.md` 머리 "# [v26.10.0.0](https://github.com/pybamm-team/PyBaMM/tree/pybamm-v26.10.0.0) - 2026-10-09".
- 26.10 절 원문 발췌 (그대로):
  - Breaking changes: "`pybamm` now requires `pybammsolvers>=0.11.0`, for the IDAKLU solver statistics and self-scheduled input-set sweeps. Upgrade `pybammsolvers` together with `pybamm`."
  - Features: "`FiniteVolumeUnstructured` accepts anisotropic coefficients in `div(K * grad(u))`: a `VectorField` with one value per axis (a diagonal tensor, as `FiniteVolume2D` takes) or a rank-2 `TensorField` (the full tensor), each component a cell field. Each face uses its normal conductivity n·K·n from the cells on either side, combined by the same distance-weighted harmonic mean as a scalar coefficient, which is exact when the principal axes of K are aligned with the faces; the tangential part of K n is not included. Previously a `VectorField` coefficient raised `DiscretisationError`. ([#5835](https://github.com/pybamm-team/PyBaMM/pull/5835))"
  - Bug fixes: "The total surface area to volume ratio of an electrode with several particle phases is now the sum of the phases' ratios. It was computed as `sum(eps_k * R_k**2) / (3 * sum(R_k**3))`, which weights each phase by its volume fraction instead of its particle number density and puts the factor of 3 in the denominator, so it came out 18 times too small for two identical phases. It sets the double-layer charging of a composite electrode under `"surface form": "differential"`. ([#5802](https://github.com/pybamm-team/PyBaMM/issues/5802), [#5805](https://github.com/pybamm-team/PyBaMM/pull/5805))"
  - Bug fixes: "`x_average`, `z_average`, `yz_average` and `r_average` no longer pull a factor out of a product when that factor depends on the averaged coordinate through an auxiliary domain (e.g. a particle concentration varying in x), and split a quotient only when its denominator is constant. This fixes nonzero `LLI [%]` and wrong total particle lithium in the DFN when the active material volume fraction varies in x. ([#5813](https://github.com/pybamm-team/PyBaMM/pull/5813))"
- 26.10 절에 #5875 · #5888 · #5841 은 없다 (grep).
- 26.10 소스 (`packages/pybamm/src/pybamm/…` · 읽기만): 기본 옵션 `"surface form": "false"` (`models/full_battery_models/base_battery_model.py:473`) ·
  DFN 은 `"false"` 일 때 surface-form 이 아닌 전도도 submodel (`models/full_battery_models/lithium_ion/dfn.py:118–127`) ·
  다상 총 표면적비 `"{Domain} electrode surface area to volume ratio [m-1]"` 는 `models/submodels/active_material/total_active_material.py:64` 에서 정의되고
  surface-form 전도도 submodel (`electrolyte_conductivity/surface_potential_form/full_surface_form_conductivity.py:290` · composite · leading) 이 읽는다.
- 우리 경로 (이 저장소 · 읽기만): `degradation-degeneracy/src/model.py` 의 DFN 옵션 = `"particle phases": ("2", "1")` · `"open-circuit potential": (("single", "current sigmoid"), "single")`
  (surface form 미지정 → 기본 `"false"`) · 매개변수 집합 `Chen2020` (`configs/base.yaml:19,24`) · lock `pybamm==26.8.0.0` · `pybammsolvers==0.9.1`
  (`requirements-validation-C.lock.txt:132–133`) · `src tools configs scripts` 에서 PyBaMM `LLI [%]` · `Total lithium` 변수 사용 0 (grep) — 우리 LLI 는 `src/fitting.py` 의 자체 식.

### ocvfit

- `git clone --depth 1 https://github.com/catnap042/ocvfit` → HEAD `2b898cc62293cb35dfe82f351fe9b0103c643d28` (2026-10-09T23:27:55+08:00 "Fix README math rendering on GitHub") · 추적 파일 37 ·
  `LICENSE` "MIT License … Copyright (c) 2026 catnap42" · `pyproject.toml` version "0.1.0" · requires-python ">=3.10" · dependencies ["numpy>=1.22", "scipy>=1.9"].
- `examples/` 스크립트 4 (`quickstart.py` · `cathode_fixed.py` · `blended_cathode.py` · `make_example_csv.py`) + `examples/data/` CSV 3 — 브리핑의 "예제 5개" 와 셈이 다르다 (셈 기준 확인 안 함).
- `.github/workflows/ci.yml`: matrix python-version ["3.10", "3.12", "3.13"] · `pytest -q`. 실행 결과 (통과) 는 브리핑 주장 — 확인 안 함.
- `src/ocvfit/uncertainty.py` 머리 docstring 원문: "1. **Correlation-corrected profile interval** - fix one parameter on a grid, refit all others, and accept values whose chi-square increase is below ``3.84 * (1 + rho) / (1 - rho)`` (inflation capped at 100), where ``rho`` is the lag-1 autocorrelation of the best-fit residuals. 2. **Reference-curve bias budget** - perturb each half-cell curve with a random offset (default +/-3 mV) and a smooth shape error (default 2 mV), refit, and take the largest deviation of each quantity. 3. **Decision** - final interval = profile interval +/- bias budget; a quantity whose half-width exceeds a threshold (default 1 percentage point) is reported as *not identifiable* (interval only, no point value)."
- 같은 파일: `MODE_PARAMETERS = {"LLI": "n_li", "LAM_PE": "Q_pe", "LAM_NE": "Q_ne"}` · `bias_budget(…, n_draws: int = 8, offset: float = 3e-3, shape: float = 2e-3, seed: int = 0)` (8 번 섭동의 최대 편차) ·
  `perturb_curve` = 균일 오프셋 + `sin(πu)` · `sin(2πu)` · `sin(3πu)` 세 항 형상 왜곡 · `is_identifiable(half_width, threshold=0.01)` ·
  `mode_interval` = `[1 - aged_hi / bol_lo, 1 - aged_lo / bol_hi]`.
- `tests/test_lfp_identifiability.py` docstring 원문: "The LFP plateau is almost flat, so the positive capacity is only determined if the steep lithiation end of the LFP curve lies inside the measured window. In the headline (negative-limited) design it does not: LLI and LAM_NE remain identifiable thanks to the graphite staging features, but LAM_PE is dominated by the reference-curve bias budget." ·
  음극 제한 설계 `assert not of.is_identifiable(half["LAM_PE"])` · 양극 제한 설계 (`synthesize_discharge` 합성 · noise 1e-3) 에서 LAM_PE · LLI 를 ±0.005 로 회수.
- `src/ocvfit/models.py`: OCV 모델 "V(s) = U_p(y(s)) - U_n(x(u_n(s))) + V_{offset}" · `param_names = ["Kn", "Sn", "v_offset"]` — 오프셋은 전압 상수 (저항 아님).

### Short-circuit-resistance-estimator

- `git clone --depth 1 https://github.com/orDrink/Short-circuit-resistance-estimator` → HEAD `78ccbfbf9b4c72214122e25516cb6da97f60eaf3` (2024-06-04T10:23:32+08:00 "Add files via upload") · 추적 파일 21 ·
  `LICENSE` "MIT License … Copyright (c) 2024 orDrink" · README "This repository contains the code for the paper: Data-driven short circuit resistance estimation in battery safety issues, Y. Jia, J. Xu, Journal of Energy Chemistry, Volume 79, April 2023, Pages 37-44" ·
  데이터 `Data.7z.001`–`Data.7z.011` (데이터 전용 라이선스 파일 없음) · 의존성 명세 · 자동 시험 파일 없음 (파일 목록).
- `Data_generation.ipynb`: `generate_sample(…, generate_step_len=10, sigement_size=300, …)` · 조건 `step%generate_step_len==0` 마다 길이 `sigement_size` 창 생성 · `sigement_sizes=[10,20,30]` (주석에 `[60,120,180,300,600]`) — 창 간격이 창 길이보다 짧으면 겹친다.
- `Data Split.py`: 실험 파일 30 개 (`R000N001` … `R500N001`) 의 창을 모두 쌓은 뒤 `idx = np.random.permutation(len(sample))` → `test_size = 0.1` 분할 — 실험 · 셀 단위 분리 없음.
- `Training in hpc.py:65–75`: 반복마다 `np.random.RandomState(seed=repeat).permutation` 분할 · `norm_layer = layers.experimental.preprocessing.Normalization(axis=-1)` · `adapt_data=input` · `norm_layer.adapt(adapt_data)` — 분할 전 전체 입력으로 정규화 통계를 맞춘다.
- 브리핑의 세 지적 (중첩 창 · 무작위 분할 · 전체 입력 정규화) 은 원문과 맞다.

### 대조하지 않은 것

- #5875 · #5888 · #5835 의 PR · CI 페이지 · impedance.py v1.8.0 (릴리스 · PyPI 상태) · #5888 기여자의 RMSE 수치 · 26.10 벤치마크 실패 2 건 — 브리핑 주장 그대로.
  (#5835 의 26.10 포함은 위 변경기록으로 확인했다.)
