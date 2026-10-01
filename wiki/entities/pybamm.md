---
title: PyBaMM (합성 truth 엔진 · 의존성)
description: "degradation-degeneracy 의 합성 truth 를 만드는 전기화학 모델 라이브러리 — 우리가 쓰는 경로(full DFN · composite 음극 · 기본 uniform submesh · LLI 자체 계산)와 릴리스별 영향 판정, 그리고 requirements 상한 부재라는 재현성 위험"
created: 2026-10-01
updated: 2026-10-01
type: entity
tags: [pybamm, tooling, degradation]
sources: [raw/articles/2026-10-01-github-research-briefing.md, raw/repositories/2026-10-01-pybamm-26.8-vs-26.9-synthetic-truth.md]
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

### 위험과 할 일

- **재현성 위험 (실재 · 실측됨):** 새 환경에서 `pip install -r requirements.txt` 를 하면 26.9 + CasADi 3.8.1 이 깔리고,
  합성 truth 가 **최대 2.7 mV** 다른 숫자로 나온다 (위 표). manifest 가 버전을 기록하므로 사후에 드러나기는 하지만
  막지는 않는다.
- **고치려면 게이트를 거친다:** 상한 고정 (예: `pybamm[all]>=24.5,<26.9` 또는 `==26.8.0.0`) 은 `requirements*.txt`
  변경 = **RUN_SCOPE 변경**이다 (CLAUDE.md 하드룰 3) → source_digest 가 바뀌고 기존 영수증 재생성이 따른다.
  브리핑만으로 바꾸지 않는다. 다음 코드 라운드의 사용자 승인 범위에 넣을 후보로 둔다.
- ~~#5755 열린 물음을 닫는 가장 싼 방법~~ → 2026-10-01 실측으로 닫았다 (위). 남는 것은 **상한 고정의 게이트 승인** 하나.

## 이 위키와의 관계

- 판정 대상 프로젝트: [[degradation-degeneracy]] · 질문: [[22p-physics-or-degeneracy]] · 방법 축: [[fitting-degeneracy]]
- 브리핑 처리 기준: [[daily-github-briefing-triage]]
- 같은 브리핑의 경쟁 도구: [[pyprobe]]

## 관련
- [[degradation-degeneracy]]
- [[fitting-degeneracy]]
- [[daily-github-briefing-triage]]
- [[pyprobe]]
