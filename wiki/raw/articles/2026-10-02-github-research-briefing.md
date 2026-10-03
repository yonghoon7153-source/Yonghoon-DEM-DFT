---
source_url: https://github.com/pybamm-team/PyBaMM/pull/5813
ingested: 2026-10-03
sha256: 5f599c6c365e0532b64e4b96355d8e13b66ff823798a9309264f6f6fbbe1a6f9
---

수집 목적: (1) 의존성 위험 감시 — 우리가 쓰는 도구(PyBaMM 등) 릴리스가 합성 truth·재현성에 주는 영향 판정 · (2) 방법 비교·경쟁 도구 — OCV/DVA 피팅 도구를 degeneracy 질문과 비교 · (3) 미세단락 도구 탐색 · (4) 실험 아이디어 저장 (착수는 별도 승인). 2026-10-01 사용자 결정 — 앞으로 매일 오는 브리핑의 처리 기준.

---

# GitHub 연구 브리핑 — 2026-10-02 조사분 (사용자가 2026-10-03 채팅으로 전달한 원문)

10월 2일 조사한 GitHub 인사이트도 전해드려요 ⚡ 중요한 업데이트 1개와 새 후보 1개예요.

1. PyBaMM: LLI 해석에 영향을 줄 수 있는 수정
9월 30일 병합된 PR #5813은 전극 두께 방향으로 활물질 체적분율이 달라질 때 리튬 재고·LLI 계산이 틀어지는 문제를 수정했어요. 조사 당시 26.9.0.0 릴리스에는 미포함이었어요. 구배 전극을 쓰신다면 우선 확인할 항목이며, 릴리스 watch를 추천해요.
작은 검증: 부반응을 끈 동일 구배 전극에서 수정 전후 총 리튬 보존과 LLI≈0 여부를 비교해 보세요. 이미 하신 일반 버전 비교와는 다른 조건이에요.
[해당 PR](https://github.com/pybamm-team/PyBaMM/pull/5813)
2. pyimpspec: EIS 열화 정량화 보조 후보
9월 24일 공개된 v5.2.0을 확인했어요. 코드·테스트·문서가 있고, 선형 Kramers–Kronig 검사, DRT, 피크 면적·등가회로 분석을 지원해요. 동일 SOC·온도의 초기/열화 EIS에서 저항 기여 변화가 정규화 조건을 바꿔도 유지되는지 살펴보는 데 유용해요. 우선 watch·예제 검토를 추천해요.
GPL-3.0-or-later이며 Python 3.12 이상이 필요해요. DRT 피크는 정규화에 민감하고, 피크만으로 LLI/LAM·미세단락 원인을 확정할 수 없어요. ASSB도 접촉 손실·계면 반응을 별도 증거로 검증해야 해요.
[저장소](https://github.com/vyrjana/pyimpspec) · [DRT 사용 안내](https://vyrjana.github.io/pyimpspec/guide_drt.html)

직접 실행한 결과는 아니에요. 기존 보유 저장소와의 중복은 확인하지 못했고, 이번 조사에서 추가로 추천할 만큼 검증된 미세단락 전용 새 후보는 찾지 못했어요.

2. REIL-UConn: 알려진 제작 조건으로 LLI/LAM 추정 검증
새로 찾은 후보이며 최근 변경은 7월 13일이에요. LFP/흑연 셀의 전극 면적·리튬화 상태를 달리한 실험 데이터와 전압·DVA 다목적 피팅 코드가 있어요. 기존 합성 데이터 검증에서 한 단계 나아가, 피팅 오차뿐 아니라 알려진 제작 변화량을 복원하는지 확인할 수 있어요.
코드는 MIT, 데이터는 CC BY 4.0이고 노트북·결과 파일이 있어요. 자동 테스트·고정 실행환경은 확인하지 못했어요. 자연 열화의 원인 입증이나 미세단락 검증까지 제공하진 않으며 ASSB에 바로 옮기기도 어려워요. 화학계별 조건을 검토한 뒤 분석용 fork 후보로 추천해요.
[저장소](https://github.com/REIL-UConn/Multi-Objective-Optimization-for-Lithium-Ion-Battery-Degradation-Diagnostics) · [실험 데이터](https://digitalcommons.lib.uconn.edu/reil_datasets/6/)

두 후보는 조회된 보유 저장소 목록과 중복되지 않았어요. 직접 설치·실행한 결과는 아니며, 이번에도 추가 추천할 만큼 검증된 실제 미세단락 전용 새 도구는 확인하지 못했어요.

사용자 지시 (같은 메시지 끝줄 · 원문): "관련해서도 확인을 해보고 사용가능한지 판단을 해보고 추가로 필요한거 있음 codex 리뷰 받자"

---

## 수집 시 1차 대조 (2026-10-03 · 공개 저장소를 git 으로 직접 받아 읽은 원문 — WebFetch 요약 아님 · GitHub API 아님)

### 1. PyBaMM PR #5813

- 병합 커밋 `bd572504ebf6619e14d4e0f26d4809ee407fd685` — 커밋 시각 2026-09-30 13:30:57 +0000 · 제목 "Fix x_average splitting products that vary in x via auxiliary domains (#5813)" · 메시지 "Fixes #5810".
- 커밋 메시지 첫 단락 원문:
  "`_is_independent_of` only checked each leaf's primary domain, so a particle variable with secondary domain "negative electrode" counted as x-constant and `x_average(eps_s * r_average(c_s))` was split into a product of averages. This made DFN `LLI [%]` and total particle lithium wrong whenever the active material volume fraction varies in x. Check all domains instead, and split a Division only when its denominator is constant."
- develop `CHANGELOG.md` (`# [Unreleased]` 아래) 에 더해진 줄 원문:
  "`x_average`, `z_average`, `yz_average` and `r_average` no longer pull a factor out of a product when that factor depends on the averaged coordinate through an auxiliary domain (e.g. a particle concentration varying in x), and split a quotient only when its denominator is constant. This fixes nonzero `LLI [%]` and wrong total particle lithium in the DFN when the active material volume fraction varies in x. ([#5813](https://github.com/pybamm-team/PyBaMM/pull/5813))"
- 바뀐 파일 넷 (`git show --stat`): `CHANGELOG.md` +1 · `packages/pybamm/src/pybamm/expression_tree/averages.py` 21 줄 변경 · `tests/.../test_lithium_ion/test_dfn.py` +12 · `tests/unit/test_expression_tree/test_averages.py` 40 줄 변경.
- 릴리스 포함 여부: 원격 태그 `pybamm-v26.9.0.0` = 커밋 `26778979` "Release v26.9.0.0 and pybammsolvers v0.10.0 (#5819)" (2026-09-28 12:02:42 −0700). `git merge-base --is-ancestor bd572504 pybamm-v26.9.0.0` → 거짓. **26.9.0.0 에 들어 있지 않다** (브리핑과 같음). 2026-10-03 원격 태그 목록에 26.9.0.0 뒤 릴리스 없음.

### 2. pyimpspec

- `vyrjana/pyimpspec` 기본 가지 끝 `c822717` (2026-09-24 10:13:29 +0300 "Updated changelog").
- `pyproject.toml`: `version = "5.2.0"` · `license = "GPL-3.0-or-later"` · `requires-python = ">=3.12"` · 의존 `numpy >=2.5, <3` · `scipy >=1.17, <2` (주석 원문 "Note that 1.18 introduced issues with constrained fitting") · 선택 `cvxopt` · `kvxopt`.
- `CHANGELOG.md` 5.2.0 (2026/09/24) 원문 항목:
  - "Added support for `.crv` files from OrigaLys."
  - "Fixed a bug where performing Kolmogorov-Smirnov test would raise an exception with SciPy 1.18+ installed."
  - "Note that constrained fitting appears to not work properly across all platforms and appears to also depend on the version of SciPy that is installed. The exact cause is currently unknown."
  - "Updated supported range of Python versions: 3.12, 3.13, and 3.14." · "Support for version 3.11 was dropped due to packages such as NumPy dropping support for that version."
  - "Deprecated the CNLS implementation of the Kramers-Kronig test."
- `tests/` 폴더 있음 (자료 파일 다수 — 실행은 안 함). 이 컨테이너 운영 Python 은 3.11.15 — pyimpspec 5.2 는 설치 불가 (3.12 · 3.13 인터프리터와 `uv` 는 있다).

### 3. REIL-UConn `Multi-Objective-Optimization-for-Lithium-Ion-Battery-Degradation-Diagnostics`

- 끝 커밋 `1188c37` (2026-07-12 23:24:04 −0400 = 2026-07-13 UTC · "Update README to include dataset link and citation") — 브리핑의 "최근 변경 7월 13일" 과 같다.
- `LICENSE`: MIT ("Copyright (c) 2026 REIL-UConn"). 파일: `Benchmarking_LFP_final.ipynb` · `util_LFP.py` · `LFP_Data.xlsx` · `results/` (pkl · pdf). 자동 테스트 · 잠금 파일 없음 (README 설치 안내는 `pip install numpy pandas scipy matplotlib seaborn pymoo openpyxl` · "Python 3.9+").
- README 원문 발췌: "Code and data repository for the journal article **"Benchmarking half-cell model fitting approaches for lithium-ion battery degradation diagnostics"**, published in *eTransportation*." · "Half-cell PE/NE voltage curves are fit to full-cell experimental data by optimizing electrode mass-scaling and capacity-offset parameters. Optimization is performed with a genetic algorithm (GA) for single-objective case…" · 논문 인용 "T. Li, Y. Zhang, B. Nowacki, S. Navidi, T. Schmitt, S. Hu, C. Hu … *eTransportation*, vol. 29, p. 100593, 2026" (doi `10.1016/j.etran.2026.100593`) · 자료 인용 "Zhang, Yifan; Li, Tingkai; Hu, Shan; and Hu, Chao, "ISU-UConn LFP/Graphite Emulated Degradation Dataset" (2026). *REIL Datasets*. 6." (CC BY 4.0).
- `LFP_Data.xlsx` 시트 19 개 (이름 원문): '12-LFP Half-cell @ C_20' · '12-Graphite Half-cell @ C_30' · '12-Graphite Half-cell @ C_20' · '12-LFP 16-Gr Full-cell @ C_20' · '15-LFP 12-Gr Full-cell @ C_20' · '15-LFP 16-Gr Full-cell @ C_20' · '15-LFP 16-Gr SOC-10' · '15-LFP 16-Gr SOC-20' · '12-LFP 16-Gr SOC-10' · '12-LFP 12-Gr SOC-10' · '12-LFP 12-Gr SOC-20' · '12-LFP 16-Gr SOC-100' · '15-LFP 12-Gr SOC-10' · '15-LFP 12-Gr SOC-20' · '12-LFP C_20 Updated' · '12-14 12-15' · 'Half cell after FM' · 'Full cell after FM SOC 0' · 'Full cell after FM SOC 10'.
- `util_LFP.py`: 반쪽전지 곡선의 질량 배율 `m_P` · `m_N` 과 오프셋 `d_P` · `d_N` 을 맞추고 `LII = (Q_max - (d_P - d_N))/max_q` 로 리튬 재고를 낸다 · `pymoo` GA / NSGA2 / NSGA3 · `plot_nsga_results` 의 선택 튜플이 "(LFP_size, Gr_size, LII)" — 설계 변수는 전극 원판 지름 (LFP 12 · 15 mm · Gr 12 · 16 mm) 과 사전 리튬화 SOC (10 · 20 · 100 %).
- 디지털 커먼즈 자료 페이지는 받지 않았다 — 저장소 안 `LFP_Data.xlsx` 가 그 자료와 같은지는 대조하지 않았다.
