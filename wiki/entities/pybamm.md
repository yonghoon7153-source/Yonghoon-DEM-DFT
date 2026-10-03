---
title: PyBaMM (합성 truth 엔진 · 의존성)
description: "degradation-degeneracy 의 합성 truth 를 만드는 전기화학 모델 라이브러리 — 우리가 쓰는 경로(full DFN · composite 음극 · 기본 uniform submesh · LLI 자체 계산)와 릴리스별 영향 판정, 그리고 requirements 상한 부재라는 재현성 위험"
created: 2026-10-01
updated: 2026-10-03
type: entity
tags: [pybamm, tooling, degradation]
sources: [raw/articles/2026-10-01-github-research-briefing.md, raw/repositories/2026-10-01-pybamm-26.8-vs-26.9-synthetic-truth.md, raw/articles/2026-10-02-github-research-briefing.md, raw/repositories/2026-10-03-pybamm-pr5813-graded-electrode-and-synthetic-truth.md]
confidence: medium
explored: false
verificationStatus: unverified
model: claude-opus-5-5
effort: medium
claimType: empirical
evidenceScope: multi-source-mixed
---

# PyBaMM (합성 truth 엔진 · 의존성)

## 개요

[[degradation-degeneracy]] 의 **합성 truth 엔진**이다. 열화 모드(LLI · LAM_PE · LAM_NE)를 알고 있는 곡선을
PyBaMM 으로 만든 뒤, 그 곡선만 보고 모드를 되찾을 수 있는지 ([[fitting-degeneracy]]) 를 판정한다. 그래서
PyBaMM 의 수치가 바뀌면 "참값" 자체가 움직인다 — 이 페이지는 **릴리스가 우리 truth 에 닿는가**를 판정해 두는
자리다 ([[daily-github-briefing-triage]] 의 의존성 축).

수치의 정본은 artifact 와 `degradation-degeneracy/docs/RESULTS*.md` 다. 여기 숫자는 사본이다.

## 핵심 사실

### 우리가 쓰는 경로 (2026-10-01 · 코드 대조)

| 항목 | 값 | 근거 (repo-root 상대) |
|---|---|---|
| 모델 | `pybamm.lithium_ion.DFN` (full · `Basic*` 아님) · `"particle phases": ("2", "1")` (음극 2상) · OCP 옵션 | `degradation-degeneracy/src/model.py` |
| 격자 | `submesh_types` · `var_pts` 를 **설정하지 않는다** → PyBaMM 기본 (입자 반경 uniform) | `src/` · `configs/` 전수 grep 0 건 |
| LLI · LAM | PyBaMM 의 LLI 변수를 쓰지 않는다 — 초기 농도를 우리 코드가 직접 줄인다 (순서 LAM_PE → LAM_NE → LLI) | `degradation-degeneracy/src/modes.py` |
| 반쪽전지 | PyBaMM half-cell 모델을 쓰지 않는다 — "halfcell" reference 는 우리 OCV 테이블 경로 | `degradation-degeneracy/src/halfcell.py` · `src/fitting.py` |
| 버전 요구 | `pybamm[all]>=24.5` — **상한 없음** · 파일 머리말에 기록된 검증 환경 26.7.1.0 | `degradation-degeneracy/requirements.txt` |
| 이 컨테이너 설치본 | 26.8.0.0 (2026-10-01 실측) | `python -c "import pybamm; print(pybamm.__version__)"` |
| 산출 기록 | 실행 manifest 의 환경 지문에 `pybamm_version` 이 들어간다 | `degradation-degeneracy/src/io.py` (`env_fingerprint`) |

### 26.9.0.0 (2026-09-28 공개) — 우리 영향 판정

1차 대조는 릴리스 페이지와 PR #5755 를 WebFetch 로 읽은 것이다 (raw 파일 하단 — 작은 모델의 인용이라 원문 그대로라고
보장하지 않는다). **26.9 를 설치하거나 돌려 보지 않았다.**

| 변경 | 우리 경로에 닿는가 | 이유 |
|---|---|---|
| #5745 `BasicDFNHalfCell` · `BasicDFNComposite` 전해질 flux 의 migration 항 | 아니오 (추정 높음) | 우리는 `Basic*` 가 아니라 full `DFN` 을 쓴다 |
| #5765 positive half-cell 의 전해질 리튬 · 총 리튬 손실 · 전해질 포함 LLI | 아니오 | half-cell 모델도, PyBaMM LLI 변수도 안 쓴다 |
| #5755 `FiniteVolume` node-to-edge shift 가 실제 node 간격 사용 | **예 — 실측으로 닫힘 (아래)** | 입자 격자는 uniform 이지만 **x 격자는 subdomain 접합부에서 비균일** (4.26 / 0.60 / 3.78 µm) 이고 그 접합부가 보정을 받는다. 우리 합성 truth 가 0.8–2.7 mV 움직인다 |
| #5694 phase 별 particle mechanics · #5770 phase 합산 열원 · OCP 문자열 | 아니오 (추정) | mechanics · 열 모델 옵션을 켜지 않는다 |
| Breaking: `pybammsolvers>=0.10.0` (#5783) · CasADi 3.7.2 → 3.8.1 (#5761) | **간접적으로 예** | 상한이 없어 **새 환경 설치가 26.9 를 끌어온다** → solver 경로가 바뀐다 |

### 26.9 실측 (2026-10-01 · `raw/repositories/2026-10-01-pybamm-26.8-vs-26.9-synthetic-truth.md`)

버리는 venv 에 26.9.0.0 을 깔고 `git archive` 사본에서 **같은 함수** (`src.grid._solve_condition`) 로 두 조건을 26.8 과 나란히 돌렸다 (운영 환경 · 산출물 불변 · 조건당 ≈2.4 s).

| 격자 | 조건 | full-cell ΔV 최대 (위치) | ΔV 중위 | Δq |
|---|---|---:|---:|---:|
| 기본 (접합부 비균일) | pristine | **0.78 mV** (방전 끝) | 1.3e-5 V | +0.002 % |
| 기본 | lli 0.10 · lam 0.13 · 0.13 | **2.71 mV** (방전 끝) | 5.2e-5 V | +0.012 % |
| x 간격 균일 강제 (1.2 µm) | pristine | 0.36 mV (방전 끝 한 점) | 4.6e-6 V | −0.001 % |
| x 간격 균일 강제 | lli 0.10 · lam 0.13 · 0.13 | **6.0e-8 V** | 8.8e-10 V | 3e-7 % |

- 차이는 **방전 끝 (x_norm → 1)** 에 몰려 있고 음극 전위가 끌고 간다 (v_ne ΔV 2.64 mV ↔ v_pe 0.07 mV). 방전 끝은 우리 피팅이 가장 민감한 자리다 (컷오프 등식 — [[birkl-ocv-degradation-diagnostic]]).
- x 간격을 균일하게 하면 열화 조건의 차이가 다섯 자릿수 내려간다 → 기본 격자의 차이는 거의 전부 **#5755**, solver 스택 (pybammsolvers 0.10 · CasADi 3.8.1) 의 몫은 1e-7 V 대.
- PR 의 "uniform mesh 는 bit-for-bit 불변" 은 **우리 기본 격자에 해당하지 않는다** — subdomain 안은 균일, 접합부는 비균일.
- 2.7 mV 는 우리 허용치 감각 (ΔV ≤ 1 mV 급) 으로 **무시할 수 없다**. 두 조건만 봤고, 격자 수렴 (어느 쪽이 더 참값에 가까운가) 은 묻지 않았다 — 26.9 는 수치적으로 더 보존적인 쪽이지만 그것이 우리 truth 의 "정답" 을 바꾸는지는 별도 물음.

### develop #5813 (2026-09-30 병합 · **26.9.0.0 미포함**) — 우리 영향 판정 · 실측 (2026-10-03 · `raw/repositories/2026-10-03-pybamm-pr5813-graded-electrode-and-synthetic-truth.md`)

무엇을 고쳤나 (커밋 `bd572504` · CHANGELOG 원문은 `raw/articles/2026-10-02-github-research-briefing.md` 하단): `x_average` · `r_average` 등의
기호 단순화가 **보조 도메인으로 평균 좌표에 의존하는 인자** (예: x 로 변하는 입자 농도) 를 상수로 보고 곱을 평균들의 곱으로
쪼갰다 · 분모가 변하는 나눗셈도 쪼갰다. 그래서 **활물질 분율이 x 로 변하면** DFN 의 `LLI [%]` · 총 입자 리튬이 틀린다.

| 판정 축 | 우리 경로 | 근거 |
|---|---|---|
| 구배 활물질 분율 | **없다** — 전극마다 스칼라 상수 (`float(b[key])`) · LAM 도 스칼라 배율 (`b.pe_vf * (1 - lam_pe)`) | `degradation-degeneracy/src/baseline.py` · `src/modes.py` |
| PyBaMM 리튬 재고 · LLI 변수 | **안 쓴다** — `src` · `tests` · `tools` · `scripts` 에서 `Total lithium` · `Loss of lithium` · `LLI [%]` grep 0 건 | 2026-10-03 grep |
| PyBaMM 열화 서브모델 (SEI · LAM · 도금) | **안 켠다** — 옵션 grep 0 건 | 같은 grep |

실측 (설치본 26.8 ↔ 같은 설치본 사본에 #5813 의 `averages.py` 고침만 덧댄 것 · 운영 환경 불변):

| 시험 A — 구배 음극 (0.675→0.825 · 부반응 0 · Chen2020 · 1 h 방전) | 수정 전 (26.8) | 수정 후 |
|---|---|---|
| `LLI [%]` 최대 (참값 0) | **0.273 %** | 9e-13 % |
| 총 리튬 표류 (상대) | **8.1e-5** | −8.6e-15 |
| PyBaMM 음극 리튬 ↔ 손 적분 Σ ε·c̄·Δx·A (상대 최대) | **0.92 %** (t=0 은 1e-16 — 초기 농도가 균일해서) | 1.6e-15 |
| 균일 음극 (대조) — 위 셋 | 9e-13 % · −8e-15 · 1.6e-15 | 같음 |

| 시험 B — 우리 합성 truth (`src.grid._solve_condition` · 10-01 과 같은 드라이버 · 두 조건) | 수정 전 ↔ 수정 후 차이 |
|---|---|
| 용량 | Δq = **0** (두 조건 모두) |
| full-cell ΔV 최대 (위치) | **2.7e-8 · 4.9e-8 V** (방전 끝 한 점 · 중위 1.8e-10 · 8.5e-11 V) · 차이는 전부 양극 전위 (음극 전위 · x 축 동일) |
| 결정성 대조 — 수정 전 ↔ 수정 전 다시 실행 | 비트 동일 (Δ 0) |

- **브리핑의 '작은 검증' 결론**: 버그는 우리 설치본 (26.8) 에 있고, 구배 전극에서 실제로 LLI 를 0.27 % 까지 만든다 · #5813 이 고친다.
- **우리 truth 에는 사실상 닿지 않는다** — 용량 동일 · 전압 최대 5e-8 V (#5755 의 2.7 mV 의 약 5 만 분의 1). 다만 결정적
  재실행이 비트 동일한데 패치 뒤는 비트가 달라진다 → **#5813 이 든 릴리스로 올리면 합성 truth 바이트가 바뀐다** (영수증 ·
  산출물 해시 재생성 대상). 버전 상한 결정은 여전히 #5755 (2.7 mV) 가 주인이고, #5813 은 그 결정을 바꾸지 않는다.
- **앞으로 닿는 조건** (그때는 #5813 이 든 버전 · 또는 리튬 재고를 손으로 계산): 구배 전극 · x 로 변하는 활물질 분율을 truth 에
  넣을 때 (예: ASSB 접촉 손실 truth 에서 비연결 입자 몫을 활물질 분율 `ε_p` 로 넣되 두께 방향으로 다르게 줄 때 — 그 표현은 [[assb-synthetic-truth-contact-loss-requirements]] 표의 '활물질 분율' 행),
  또는 PyBaMM `LLI [%]` · `Total lithium` 변수를 라벨 · 보존 검사로 쓰기 시작할 때.
- 열린 물음: #5813 이 든 첫 릴리스 번호 (2026-10-03 원격 태그에 26.9.0.0 뒤 릴리스 없음 — watch).

### 위험과 할 일

- **재현성 위험 (실재 · 실측됨):** 새 환경에서 `pip install -r requirements.txt` 를 하면 26.9 + CasADi 3.8.1 이 깔리고,
  합성 truth 가 **최대 2.7 mV** 다른 숫자로 나온다 (위 표). manifest 가 버전을 기록하므로 사후에 드러나기는 하지만
  막지는 않는다.
- **고치려면 게이트를 거친다:** 상한 고정 (예: `pybamm[all]>=24.5,<26.9` 또는 `==26.8.0.0`) 은 `requirements*.txt`
  변경 = **RUN_SCOPE 변경**이다 (CLAUDE.md 하드룰 3) → source_digest 가 바뀌고 기존 영수증 재생성이 따른다.
  브리핑만으로 바꾸지 않는다. 다음 코드 라운드의 사용자 승인 범위에 넣을 후보로 둔다.
- ~~#5755 열린 물음을 닫는 가장 싼 방법~~ → 2026-10-01 실측으로 닫았다 (위). 남는 것은 **상한 고정의 게이트 승인** 하나.
- **#5813 (2026-10-03 실측)**: 우리 truth 에는 용량 0 · 전압 ≤5e-8 V — 경로 밖이지만 바이트는 바뀐다. 구배 활물질 분율 ·
  PyBaMM 리튬 재고 변수를 쓰게 되면 그 전에 #5813 이 든 버전 (26.9.0.0 에는 없다) 을 요구 조건으로 적는다. 상한 고정 판단은 그대로.

## 이 위키와의 관계

- 판정 대상 프로젝트: [[degradation-degeneracy]] · 질문: [[22p-physics-or-degeneracy]] · 방법 축: [[fitting-degeneracy]]
- 브리핑 처리 기준: [[daily-github-briefing-triage]]
- 같은 브리핑의 경쟁 도구: [[pyprobe]]

## 관련
- [[degradation-degeneracy]]
- [[fitting-degeneracy]]
- [[daily-github-briefing-triage]]
- [[pyprobe]]
