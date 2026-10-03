# pybamm 상한 · 고정 — Codex 사전 검토 요청 (2026-10-03 · 게이트 차수 밖 · RUN_SCOPE 0 · 결정 전 의견 요청)

> 첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

## §0 무엇을 묻나

`degradation-degeneracy/requirements.txt` 의 `pybamm[all]>=24.5` 에 상한 · 고정을 둘지, 둔다면 **어떤 꼴로 · 어느 라운드에**
넣을지에 대한 **사전 의견**이다. 구현 · 실행 승인 요청이 아니다. 진행 중인 G87-N1 보완 (원장 §129 · 고정 표
`STAGE3_IMPL_ROUND1_SPEC.md` §14 · GATE88 예정) 과 **섞지 않는다** — 이 의견은 그 다음 라운드의 범위 판단에 쓴다. 결정은 사용자
(`HANDOFF_2026_10_02_DASHBOARD.md` §1-2 · `STAGE3_IMPL_ROUND1_SPEC.md` §13-7 보류).

## §1 사실 (저장소 원문 기준)

| 항목 | 값 | 근거 |
|---|---|---|
| requirements | `pybamm[all]>=24.5` · solver 배포판 (`pybammsolvers` · `casadi`) 직접 고정 0 · 주석 "검증 완료 조합 (2026-08-05): pybamm 26.7.1.0 / numpy 2.4.6 / scipy 1.17.1 / pandas 3.0.5 / Python 3.11" | `degradation-degeneracy/requirements.txt` |
| 정본 grid 생산 identity | `IDAKLUSolver` · pybamm **26.7.1.0** · pybammsolvers **0.9.0** · casadi 3.7.2 (3069 조건 · 1023 family) | 원장 `docs/08_REVIEW_RESPONSE.md` §20.2 · `docs/GATE14_WORKING_STATE.md:272` · `docs/05_HANDOFF.md:267` (Python 3.10.12) |
| grid_fit_v5 WSL 시도 | pybamm **26.8.0.0** · pybammsolvers **0.9.1** | `docs/22p_gap/run_windows/grid_fit_v5/wsl/discharged_cache_from_attempt1.json` · `attempt4_partial_results/manifest.yaml` |
| 지금 검증 환경 (87차 요청의 2109 passed · smoke · 변이 374) | pybamm 26.8.0.0 · pybammsolvers 0.9.1 · casadi 3.7.2 · Python 3.11.15 | 87차 증거 `docs/22p_gap/gate87_evidence/` |
| 지금 새로 설치하면 | `pip install -r requirements.txt` → pybamm 26.9.0.0 + CasADi 3.8.1 | `wiki/raw/repositories/2026-10-01-pybamm-26.8-vs-26.9-synthetic-truth.md` (버리는 venv 실측) |
| 26.8 ↔ 26.9 (#5755 · x 격자 접합부) | 우리 합성 truth 두 조건 (`src.grid._solve_condition`): 기본 x submesh 에서 full-cell 최대 **2.7 mV** (방전 끝) · 균일 격자면 6e-8 V | 같은 raw |
| #5813 (develop 2026-09-30 · 26.9.0.0 미포함) | 26.8 + 패치: 같은 두 조건 용량 Δ0 · 전압 ≤4.9e-8 V · **비트는 바뀜** (수정 전 재실행은 비트 동일) | `wiki/raw/repositories/2026-10-03-pybamm-pr5813-graded-electrode-and-synthetic-truth.md` |
| **26.7.1 ↔ 26.8** | **측정 없음** — 정본 grid 와 지금 검증 환경 사이 | — |
| 지금 검사가 묻는 것 | validator: grid spec 의 `effective_solver` identity (class · pybamm · pybammsolvers · casadi) **존재** (`src/io.py` `effective_solver_identity`) · producer: worker 가 실제로 쓴 solver 가 parent 서명과 같은가 (`src/grid.py` `_assert_worker_solvers`). **실행 환경 ↔ 정본 생산 환경의 동일성은 아무 곳도 묻지 않는다** — 다른 판에서 만든 truth 도 identity 만 다르게 적힌 채 유효하다 | 코드 (`b8d4b6933` = 현재 RUN_SCOPE) |

## §2 선택지 (우리 초안 — 고르지 않았다)

| # | 꼴 | 막는 것 | 못 막는 것 · 비용 |
|---|---|---|---|
| A | 상한만 `pybamm[all]>=24.5,<26.9` | 26.9 (#5755 2.7 mV) · 그 뒤 #5813 바이트 변동 | 26.7.1 ↔ 26.8 혼재 (측정 0) · solver 배포판 미고정 (0.9.0 ↔ 0.9.1) |
| B | 정본 생산 identity 정확 고정 `pybamm[all]==26.7.1.0` · `pybammsolvers==0.9.0` · `casadi==3.7.2` | 정본 재생성 환경의 drift 전부 | 지금 검증 환경 (26.8) 과 다름 → 전체 회귀 · smoke · 변이 재생 · 영수증을 그 환경에서 다시 · Python 3.11 에서 그 조합 설치 가능성 확인 필요 · 이후 버그 수정 차단 |
| C | 검증 환경 identity 정확 고정 `==26.8.0.0` · `pybammsolvers==0.9.1` · `casadi==3.7.2` | 검증 환경 drift | 정본 grid (26.7.1) 재생성은 여전히 다른 환경 · 26.7.1 ↔ 26.8 차이 미측정 |
| D | A (또는 C) + producer 쪽 fail-closed guard — 계획 · 세대가 선언한 solver identity 와 실행 환경이 다르면 truth 생산 거부 | 어떤 판이든 조용한 drift | RUN_SCOPE 코드 변경 (`src/grid.py` · `tools/preserve.py`) · 계획 schema 에 identity 축 추가 |
| E | 바꾸지 않음 + 운영 문서에 "26.9 금지" 메모 | — | 재현성 위험 그대로 |

**선행 측정 제안 (우리 쪽 · RUN_SCOPE 0 · 승인되면):** 26.7.1.0 (+ pybammsolvers 0.9.0) ↔ 26.8.0.0 (+ 0.9.1) 의 같은 두 조건 비교 —
10-01 과 같은 드라이버 · 버리는 venv · 운영 환경 불변 · 약 10 s. 결과가 A/C 와 B 를 가른다.

## §3 묻는 것

| # | 질문 |
|---|---|
| Q1 | 상한 · 고정이 필요한가 (지금 재현성 위험을 실재로 보는가). 필요하면 A–E 중 무엇이고 왜 |
| Q2 | 26.7.1 ↔ 26.8 측정이 선행 조건인가. 그렇다면 판정 문턱 (예: 두 조건 ΔV ≤1e-6 V 이면 A 또는 C, 넘으면 B) 을 무엇으로 |
| Q3 | solver 배포판 (`pybammsolvers` · `casadi`) 도 함께 고정해야 하는가 — 12차 발견 2 (같은 pybamm 에서도 backend 가 값을 바꾼다) 와의 정합 |
| Q4 | 라운드 배치: G87-N1 종결 뒤 별도 라운드 (우리 초안 — 범위가 섞이면 판정이 흐려진다) ↔ G87-N1 의 영수증 재생성 사이클에 함께 |
| Q5 | 바꾼 뒤 증거 묶음: 두 leg 영수증 재생성 · 전체 회귀 · smoke · 등록부 전체 재생 외에 필요한 것 (예: 정본 grid 의 일부 조건을 새 환경에서 다시 만들어 대조) |
| Q6 | D 가 필요하다면, guard 의 기준 identity 는 어디서 오는가 (계획 · 세대표 · 정본 grid spec) |

## §4 이 요청이 아닌 것

구현 · 실행 승인 · requirements 변경 · G87-N1 범위 · 실행 GO · 새 연구 leg · 운영 원장 변경. 받은 코드 · 시험 · COMSOL 을 실행할
필요가 없다 (근거는 위 파일 원문과 wiki raw 의 출력 원문).
