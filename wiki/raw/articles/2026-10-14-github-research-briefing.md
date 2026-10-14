---
source_url: (채팅 원문 · 링크는 본문 블록 안 — PyBaMM PR 5888 · 5893 · 5842 · Battery-EIS-Fit v0.1.1 · 수정 PR 1 · Zenodo 15422339)
ingested: 2026-10-14
sha256: 3c1f6699006332061c531a7c7b75cd632e2dbe5f7d1bdf908794f6aa24b62e99
---

수집 목적: 2026-10-01 사용자 결정의 브리핑 처리 기준 (의존성 위험 감시 · 경쟁 도구 · 미세단락 도구 · 실험 아이디어 — 착수는 별도 승인) · 사용자 지시 2026-10-14 "참고할거 있음 참고해용".

---

# GitHub 연구 브리핑 — 2026-10-14 전달분 (사용자 채팅 원문 · 항목 2)

아래 블록은 채팅 원문 (전사) 이다 (마지막 줄의 사용자 지시까지 · 블록 자체의 sha256 = `933f3f59dbfb452f5f8332e59cc002979e4805b019937a0ec2908c8359f1fdb8` · 끝 줄바꿈 포함 · frontmatter 의 sha256 은 위키 규칙대로 본문 전체). 원문의 링크 6 개는 블록 안에 그대로 있다.

```text
#5888이 오늘 01:01 KST에 병합됐어요. 확산계수의 10⁻⁴ 단위 변환 누락 수정과 강화된 시험, 최종 CI 통과를 확인했어요. BSD-3-Clause이며 최신 정식판 26.10에는 아직 없어요
입자 농도 계산·표면 최댓값 관련 #5893·#5842도 새로 병합됐어요. LIB 열화 피팅 전에 수송·농도 계산의 오류를 먼저 제거하는 데 유용해요. 미세단락이나 LLI/LAM 원인을 실험적으로 구분했다는 뜻은 아니에요
다음 릴리스 watch를 추천해요
[단위 수정 #5888](https://github.com/pybamm-team/PyBaMM/pull/5888) · [농도 계산 #5893](https://github.com/pybamm-team/PyBaMM/pull/5893) · [표면 극값 #5842](https://github.com/pybamm-team/PyBaMM/pull/5842)
작은 검증 제안: 공개 Ai2020 방전 조건 하나를 26.10과 수정본에서 비교해 확산계수·전해질 농도구배·전압을 확인해 보세요. 다른 설정과 열화 파라미터는 고정해야 수치 수정 효과를 분리할 수 있어요

2. Battery-EIS-Fit 0.1.1 — 실패한 피팅과 뒤바뀐 회로 분지 구분
오늘 08:51 KST 릴리스예요. 수렴하지 않거나 유한하지 않은 피팅을 거르고, 모두 실패하면 명시적 오류를 내요. 두 R–CPE 분지를 특성시간순으로 정렬해 단순 라벨 교환도 줄여요
MIT 코드·회귀시험·Python 3.10~3.12 CI 통과, NMC811/흑연 21700 셀의 공개 실측 EIS 54개를 확인했어요. 원본 데이터는 CC BY 4.0이에요
열화 전후 EIS 비교의 기초 도구 후보지만, 식별 가능성은 코드상 ‘평가하지 않음’이에요. 분지 순서가 SEI/전하이동 원인 구분을 보장하지 않으며, 미세단락 정답이나 ASSB 검증도 없어요. 신생 alpha 도구라 우선 watch를 추천해요
[저장소·릴리스](https://github.com/shiyunliu-battery/Battery-EIS-Fit/releases/tag/v0.1.1) · [수정 PR](https://github.com/shiyunliu-battery/Battery-EIS-Fit/pull/1) · [원본 데이터](https://zenodo.org/records/15422339)


참고할거 있음 참고해용
```

## 1차 대조 (2026-10-14 · 공개 저장소를 git 으로 직접 받아 읽은 원문 · 받은 코드 · 시험 실행 0 · 저장소 밖 작업 폴더)

### PyBaMM — main 의 병합 커밋 · 변경기록 · 바뀐 줄 (정적)

- `git clone --depth 1` + `git fetch --depth=120 origin main` (`https://github.com/pybamm-team/pybamm`): main HEAD `77655eda0acd64750aa5f7878b90d90b2cdb69a2`
  (2026-10-13T19:54:31-04:00 "fix: use per-electrode-pair current in potential pair tab boundary condition (#5826)").
- 병합 커밋 셋 — 모두 26.10 태그 커밋 `b5f49ae1` ("Release v26.10.0.0 (#5883)") **뒤**라 정식판 26.10 에 없다 (git log 순서):
  - `343ece2062dbb39789dbfa977e0f2daf96e9e370` · 2026-10-13T16:01:03+00:00 · "fix: convert Ai2020 electrolyte diffusivity from cm2/s to m2/s (#5888)" —
    파일 3: `CHANGELOG.md` · `packages/pybamm/src/pybamm/input/parameters/lithium_ion/Ai2020.py` · `…/test_parameter_sets/test_Ai2020.py`.
  - `9d8df9d039e6b8ec78f94db6a916d7f5c003fbd7` · 2026-10-13T16:05:28+01:00 · "fix: include the particle surface in maximum and minimum particle stoichiometry (#5842)" —
    파일 3: `CHANGELOG.md` · `…/models/submodels/particle/base_particle.py` · `…/test_lithium_ion/base_lithium_ion_tests.py`.
  - `caa0e53249d1b52f42905a99f46bc14ee1cb3f2d` · 2026-10-13T14:31:28+01:00 · "fix: restore missing particle radius in quartic profile concentration (#5893)" —
    파일 3: `CHANGELOG.md` · `…/models/submodels/particle/polynomial_profile.py` · `…/test_lithium_ion/test_dfn.py`.
- 변경기록 원문 (그대로):
  - #5888: "`Ai2020`'s electrolyte diffusivity now converts the Valoen and Reimers (2005) fit from cm2/s to m2/s. It was 1e4 times too large, so DFN simulations with Ai2020 had almost no electrolyte concentration gradient. ([#5887](https://github.com/pybamm-team/PyBaMM/issues/5887), [#5888](https://github.com/pybamm-team/PyBaMM/pull/5888))"
  - #5842: "`"Maximum/Minimum {domain} particle stoichiometry"` and the matching concentration variables now include the particle surface value. Before, they only used cell-centre values, so the maximum could be lower than the maximum surface stoichiometry during charge. ([#5842](https://github.com/pybamm-team/PyBaMM/pull/5842))"
  - #5893: "Fixed the particle concentration of the `"quartic profile"` particle model in models that resolve the electrode (e.g. DFN), which was missing a factor of the particle radius on the concentration gradient term and diverged to unphysical values. ([#5893](https://github.com/pybamm-team/PyBaMM/pull/5893))"
- 바뀐 줄 (diff 그대로 · 요지):
  - `Ai2020.py`: `D_c_e = 10 ** (-4.43 - 54 / (T - 229 - 5e-3 * c_e) - 0.22e-3 * c_e)` → `D_c_e = 1e-4 * 10 ** (-4.43 - 54 / (T - 229 - 5e-3 * c_e) - 0.22e-3 * c_e)`
    (주석 "The Valoen and Reimers (2005) fit gives cm2/s; convert to m2/s") · 같은 파일 전해질 전도도 함수의 docstring "Solid diffusivity" → "Dimensional electrolyte conductivity [S.m-1]" (식 변경 없음).
  - `polynomial_profile.py`: `B = -35 * c_s_surf + 10 * q_s_rav + 35 * c_s_rav` → `B = -35 * c_s_surf + 10 * q_s_rav * R + 35 * c_s_rav` (한 줄).
  - `base_particle.py`: `Minimum/Maximum {domain} {phase_name}particle concentration [mol.m-3]` 가 `pybamm.min(c_s)` · `pybamm.max(c_s)` (cell-centre 만) →
    표면값을 broadcast 해 함께 본 `c_s_min = pybamm.min(pybamm.minimum(c_s, c_s_surf_bc))` · `c_s_max = pybamm.max(pybamm.maximum(c_s, c_s_surf_bc))`.
    같은 diff 에 `Average … particle concentration` 정의 변경은 없다.

### 우리 경로와의 대조 (이 저장소 · 읽기만)

- degradation-degeneracy (RUN_SCOPE): 매개변수 집합 `Chen2020_composite` (`configs/base.yaml:19`) · lock `pybamm==26.8.0.0` · `pybammsolvers==0.9.1`
  (`requirements-validation-C.lock.txt:132–133`) · DFN 옵션은 `"particle phases"` · `"open-circuit potential"` 둘뿐 (`src/model.py:5–6 · 34–35`) —
  `"particle"` 옵션을 쓰지 않으므로 기본 입자 모델이다 (quartic profile 아님).
- `src tools configs scripts run.sh` 에서 `Ai2020` · `quartic` · `Maximum/Minimum … particle` · `particle stoichiometry` 사용 0 (grep).
- 우리가 읽는 PyBaMM 입자 변수는 `Average negative primary particle concentration [mol.m-3]` · `Average negative secondary particle concentration [mol.m-3]` ·
  `Average positive particle concentration [mol.m-3]` (`src/baseline.py:97–102` · `src/halfcell.py:210–212`) — #5842 가 바꾼 Min/Max 가 아니다.
- 열화 모드는 부피분율 · 공극률 · 초기 농도를 스칼라 매개변수로 넣는다 (`src/modes.py:31–38`).
- 판단 (정적 · 실행 대조 안 함): 세 수정 모두 우리 고정 경로의 조건 (Ai2020 · quartic profile · Min/Max 변수) 에 해당하지 않는다.
- REIL (bms-balancing) 은 PyBaMM 을 쓰지 않는다 (그들 util 의 반쪽전지 OCV 식) — 무관.

### Battery-EIS-Fit

- `git clone --depth 1 https://github.com/shiyunliu-battery/battery-eis-fit` → HEAD `cbcb820ee5273dcfe8bc5795cc677cde9ee624a2`
  (2026-10-14T00:51:03+01:00 "Merge release preparation for eisfit 0.1.1") · `git ls-remote --tags`: `refs/tags/v0.1.1` = `b6425e587b35f3800d591481a64870f4453ff2d1` (`v0.1.0` 도 있음) · 추적 파일 82.
- `LICENSE` "MIT License … Copyright (c) 2026 Shiyun" · `pyproject.toml` version "0.1.1" · requires-python ">=3.10" · `.github/workflows/ci.yml` matrix
  python-version ["3.10", "3.11", "3.12"] (실행 결과는 확인 안 함).
- `CHANGELOG.md` 0.1.1 원문 (그대로):
  "- Select only converged optimizer starts with finite results. Raise `FitConvergenceError` with per-start diagnostics when none are accepted.
  - Order the two R-CPE branches by increasing characteristic time, retaining the original solver order and an explicit parameter permutation.
  - Remap effective bounds and bound warnings with the reported branch order.
  - Export solver diagnostics and the actual fit configuration to JSON, with optimizer attempts included in Excel outputs.
  - Return a nonzero CLI exit status for failed fits while continuing folder processing after individual failures.
  - Add regression tests and CI for Python 3.10, 3.11 and 3.12.
  Convergence and branch ordering do not establish parameter identifiability or persistent physical-process identity across spectra."
- `src/eisfit/fitting.py`: `"identifiability_status": "not_assessed"` (70 행) · 분지 정렬 docstring "Order R||CPE arcs by tau=(R*Q)**(1/n), with a deterministic exact-tie rule. … This is a naming convention, not a physical …" (75–77 행).
- README 원문: "It does not assign SEI/charge-transfer processes, establish identifiability, or track the same physical arc across spectra, especially when the times overlap or cross."
- `EIS_dataset/`: CSV 54 + 메타 5 (`README.md` · CSVW 스키마 · `metadata.html` · `metadata.jsonld` · `reference.txt`). 그 README 원문: "M. Moertelmaier, M. Kasper, and S. Clark, "EIS data of 54 21700 cells", Zenodo, 2025, doi: 10.5281/zenodo.15422339." · "The dataset metadata reports CC-BY 4.0 licensing." · PyPI 배포본은 이 폴더를 뺀다.
- 브리핑의 "NMC811/흑연" 화학은 저장소에서 확인하지 않았다 (Zenodo 페이지 미열람).

### 대조하지 않은 것

- PR 페이지 · CI 실행 결과 (#5888 "최종 CI 통과" · EIS-Fit CI 통과) · Zenodo 페이지 · PyPI 상태 · 수정 PR (Battery-EIS-Fit #1) 본문 — 브리핑 주장 그대로.
- 작은 검증 제안 (Ai2020 방전을 26.10 과 수정본에서 비교) 은 하지 않았다 — 수정본 설치는 환경 변경 (버리는 venv 라도 별도 승인) 이고, 우리 경로가 Ai2020 을 쓰지 않는다.
