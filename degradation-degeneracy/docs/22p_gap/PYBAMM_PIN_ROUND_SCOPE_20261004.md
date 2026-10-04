# PyBaMM 환경 고정 라운드 — 범위 초안 · 사용자 결정 요청 (89차 뒤 · 구현 전 · RUN_SCOPE 0)

> **범위 제안이다.** `requirements*.txt` · RUN_SCOPE · 운영 환경 · 설치 상태를 바꾸지 않았고, 사용자 승인 전에는 바꾸지 않는다. 버전 비교 계산 ·
> 재생산 · 영수증 재생성도 하지 않았다.

## §0 왜 지금 · 무엇을 묻나

- 89차 회신 (원장 §134) 이 G88-N1 과 단계 3 라운드 2b 를 닫았고, 사용자가 "다음은 PyBaMM 고정의 별도 범위 · 승인 단계 · 이번 종결은 새 계산이나
  requirements 변경 승인이 아니다" 라고 정했다.
- 사전 검토 회신 기록 (`PYBAMM_PIN_PREREVIEW_REPLY_20261003.md` §1 · §4) 이 틀을 정해 두었다 — 목적별 프로필 **C** (현재 검증 환경의 정확 고정) ·
  **B** (역사 정본 환경 — producer 기록에서) · **D** (새 truth 생산의 guard — 봉인 profile 에 결속). 그 라운드의 첫 커밋은 고정 표 (C lock 범위 · B 증거
  출처 · D 결속 자리와 음성 사례) 다.
- 이 문서는 그 고정 표의 **초안**과 비용 · 영향, 그리고 사용자가 정할 항목 (§5) 이다.

## §1 지금의 사실 (우리 실측 · 저장소 기록 — 2026-10-04)

| 묶음 | 출처 | Python · 플랫폼 | pybamm | pybammsolvers | casadi | numpy | scipy | pandas |
|---|---|---|---|---|---|---|---|---|
| **v4 정본** (truth `grid_curves_v4` · fits `grid_fit_v4` · `halfcell_fit_v4` · `paired_fixed5_v4`) | 네 묶음의 producer manifest (`artifacts/grid_curves_v4/curves_manifest.yaml` 등 — 네 기록이 서로 같다) | 3.10.12 · Linux-5.15.0-130 (glibc 2.35 · x86_64 — V100 서버, `docs/05_HANDOFF.md` §7) | 26.7.1.0 | 0.9.0 | 3.7.2 | 2.2.6 | 1.15.3 | 2.3.3 |
| `grid_fit_v5` (진단 전용 · 자체 curves `29da452a…`) | `artifacts/grid_fit_v5/manifest.yaml` | 3.12.14 · Linux-6.8.0-110 | 26.8.0.0 | 0.9.1 | 3.7.2 | 2.5.3 | 1.18.1 | — |
| warm probe 일부 | `docs/22p_gap/warm_probe/*.manifest.yaml` | 3.12.3 · WSL2 | 26.7.1.0 | 0.9.0 | 3.7.2 | 2.5.2 | 1.17.1 | — |
| **이 검증 컨테이너** (pytest · smoke · 변이 재생을 돌린 곳) | 이번 실측 (`importlib.metadata` · `pip freeze` 167 배포판) | 3.11.15 · Linux-6.18 x86_64 | 26.8.0.0 | 0.9.1 | 3.7.2 | 2.4.6 | 1.17.1 | 3.0.5 |

- v4 정본 기록의 나머지 축: joblib 1.5.3 · pyarrow 25.0.1 · matplotlib 3.10.9 · PyYAML 6.0.3 · solver `IDAKLUSolver` (effective_solver 기록) · smoothing backend
  필드 없음 (지문에 그 축이 생기기 전 기록).
- `requirements.txt` 는 하한만 둔다 (`pybamm[all]>=24.5` · `numpy>=1.24` · `scipy>=1.11` · …). 그 주석의 "검증 완료 조합 (2026-08-05): pybamm 26.7.1.0 / numpy
  2.4.6 / scipy 1.17.1 / pandas 3.0.5 / Python 3.11" 은 **v4 정본 producer 기록 (numpy 2.2.6 · scipy 1.15.3 · pandas 2.3.3 · Python 3.10.12) 과 다르다** — 그 주석은
  정본 생산 환경의 기록이 아니다 (이번에 고치지 않는다 · §5 D5).
- 코드가 이미 하는 것 (사전 검토 P3 — 좌표는 현재 HEAD): `src/io.py:233` `env_fingerprint()` 가 Python · 플랫폼 · machine · smoothing backend · numpy · scipy ·
  pandas · joblib · pyarrow · pybamm · matplotlib · yaml · pybammsolvers · casadi 를 기록 · `src/io.py:1344–1348` 이 서명의 effective_solver 존재를 검사 ·
  `src/grid.py:264–266` 이 effective_solver 와 env 를 grid 서명에 넣음 · `src/grid.py:751` `_assert_worker_solvers` 가 worker ↔ parent solver 를 대조 ·
  `src/runner.py:37–55` 는 IDAKLU 생성 실패 시 경고 뒤 CasADi 로 fallback.
- **빠진 것:** 독립적으로 승인된 expected profile ↔ 실제 실행 환경의 대조 (사전 검토 P3). 지금은 "무엇으로 돌렸나" 는 기록되지만 "그 환경이 허용된
  것인가" 를 묻는 곳이 없다.
- identity: `requirements*.txt` 는 RUN_SCOPE 다 (`src/io.py:38`) → `source_digest` 에 들어간다. requirements 파일을 바꾸거나 같은 glob 의 새 파일을 더하면
  source_digest 가 바뀐다.

## §2 라운드의 비용 · 영향

- RUN_SCOPE 가 바뀌므로 지금까지의 게이트 루프와 같은 비용이 든다 (G88-N1 의 실측 — 원장 §133): 영수증 history 보존 + 새 세대 1 회 (paired · grid) ·
  전체 pytest (≈53 분) · strict smoke (≈2.5 분) · 등록부 전체 변이 재생 (≈2.5 시간) · 게이트 요청 · 회신.
- **기존 정본 수용은 소급 취소하지 않는다** (사전 검토 §3). 기존 artifacts 의 재생산 (10 시간급) 은 이 라운드 범위가 아니다 — 재생산은 "B 프로필로 정본
  재생성" 이든 "새 세대 생산" 이든 별도 결정이다. 현 validator 가 옛 producer 자료를 검사할 수 있다는 것과 현 환경으로 옛 자료를 같게 다시 만들 수 있다는
  것은 다른 주장이다.
- C 를 **실패로 강제**하면 C 와 다른 기계 (사용자 Windows · 생산 서버) 에서 시험이 시작하지 않게 된다. 그래서 C 의 쓰임 (기록 대조 / fail-closed) 이
  결정 항목이다 (§5 D3).

## §3 고정 표 초안 (승인되면 라운드 첫 커밋에서 확정 — 코드 변경 전)

### 3-A. C 프로필 — 현재 검증 환경의 정확 고정

| 항목 | 초안 |
|---|---|
| 내용 | Python 3.11.15 · 플랫폼 (OS · glibc · machine) · 위 표의 배포판 + 전이 의존성 전부 (`pip freeze` 167 줄의 정확 목록) · 설치된 배포판의 RECORD 해시 (설치 뒤 파일 변경 감지의 범위는 그만큼으로 한정 — 사전 검토 P2) |
| 자리 (선택) | (a) 새 파일 `requirements-validation-C.lock.txt` — glob `requirements*.txt` 에 걸려 RUN_SCOPE · source_digest 에 들어간다 · `requirements.txt` 의 하한은 그대로 · (b) `requirements.txt` 자체를 정확 고정 — 생산 서버 · 다른 기계에도 강제된다 |
| 쓰임 (선택) | (i) **기록 대조** — 영수증 · 게이트 증거 · smoke 기록에 "실행 환경 = C lock 인가" 를 일치 / 불일치 목록으로 남긴다 (불일치여도 시험은 돈다) · (ii) **fail-closed** — 불일치면 검증 실행을 시작하지 않는다 |
| 선언하지 않는 것 | C 가 정본 생산 환경과 같다는 것 · C 로 만든 수치가 B 와 같다는 것 |

### 3-B. B 프로필 — 역사 정본 환경 (기록 파일만)

| 항목 | 초안 |
|---|---|
| 출처 | v4 producer manifest 4 묶음의 env 블록 — 원문을 그대로 옮기고 네 기록이 같음을 대조 (위 표 · 나머지 축 포함) |
| 한계 | 기록된 축만의 프로필이다 — 전이 의존성 · 배포 파일 해시 · 로컬 패치 · native 라이브러리는 당시 기록에 없다 (사전 검토 P2). "B 를 다시 설치하면 정본이 같게 나온다" 를 주장하지 않는다 |
| 쓰임 | 정본 재생성을 시도할 때의 기준 · 재생성 동등성을 주장하려면 그때 사전 고정 비교가 따로 필요 (사전 검토 Q2) — 이번 범위 아님 |

### 3-C. D guard — 새 truth 생산의 허가 검사 (설계 초안 · 별도 라운드 권고)

| 항목 | 초안 |
|---|---|
| 결속 사슬 | 봉인 profile 파일 SHA → prospective 계획 (v6 계획 index 의 `planned_envelope` 옆에 profile digest) → parent 실제 env → worker 실제 env → 산출물 · 영수증 |
| 자리 후보 | 생산 진입 (첫 solve 전) · resume 진입 · worker 서명 대조 (`src/grid.py:751` 주변) · solver 생성 (`src/runner.py:37–55` 의 fallback) |
| 음성 사례 (사전 검토 그대로) | 잘못된 배포판 · 허용하지 않은 fallback (CasADi) · 같은 버전의 변조 · 계획의 profile SHA 변경 · worker 불일치 · identity 누락 · resume 환경 변경 — **허가 전 불일치가 solve 에 닿지 않는지**와 저장 후 evidence 검사를 따로 본다 |
| 권고 | 생산 경로 코드 (`src/grid.py` · `src/runner.py`) 를 건드리고 음성 사례가 일곱이라, C · B 와 다른 라운드로 — 새 truth 생산 계획이 생길 때 (지금은 없다) |

## §4 순서 (승인 뒤 · 게이트 루프 그대로)

승인 기록 (원장 새 절) → 고정 표 확정 커밋 (코드 전) → RED (lock 파일 · 대조 함수 · 영수증 필드가 없어서 실패하는 시험 — 실패를 눈으로 본다) → 최소
구현 → 변이 등록 · 재현 → 영수증 history 보존 + 새 세대 1 회 → 전체 pytest · strict smoke · 등록부 전체 재생 (clean 커밋 · 시작 = 끝 HEAD) → GATE90
요청. 같은 라운드에 다른 보완을 끼우지 않는다.

## §5 사용자 결정 (각각)

| # | 결정 | 우리 권고 |
|---|---|---|
| D1 | 환경 고정 라운드 착수 | — (사용자) |
| D2 | 이번 라운드 범위 | **C + B** (D 는 새 생산 계획이 생길 때 별도 라운드) |
| D3 | C 의 쓰임 | **기록 대조** — pytest 는 막지 않고, 영수증 · 게이트 증거에 일치 / 불일치를 남긴다 (fail-closed 는 다른 기계의 시험을 막는다) |
| D4 | C 의 자리 | **새 lock 파일** (`requirements.txt` 하한 유지 — C 는 생산 환경 선언이 아니다) |
| D5 | `requirements.txt` 주석 "검증 완료 조합" 정정 | 같은 라운드에서 정정 (정본 producer 기록과 다름을 주석에 적는다) — 또는 그대로 |
| D6 | 정본 재생성 · 새 세대 생산 · 26.7.1 ↔ 26.8 비교 | 이번 범위 밖 · 각각 별도 결정 |

## §6 이 문서가 하지 않는 것

`requirements*.txt` · RUN_SCOPE · 운영 환경 · 설치 · 버전 비교 계산 · 재생산 · 영수증 · 기존 정본 수용의 변경 없음. 89차 종결 · 2b 종결 · `grid_fit_v5`
진단 전용 지위 · 실행 GO 아님 · 기존 과학적 주장의 한계 그대로.

## §7 결정 (2026-10-04 · 덧붙임 — 위 §0–§6 은 제출 원문 그대로)

사용자 "권고대로 너가 순서대로 해줘 같이 쳐내가자" — §5 의 권고 그대로 (D1 착수 · D2 C + B · D3 기록 대조 · D4 새 lock 파일 · D5 같은 라운드
정정 · D6 범위 밖). 승인 기록은 원장 §135, 확정한 고정 표는 `PYBAMM_PIN_ROUND_SPEC.md` (코드 변경 전 커밋). 초안에서 확정 때 더한 세부 —
대조 목록은 `pip freeze` 가 아니라 `importlib.metadata` 전체 (유효 170 · 가려진 2) · 사전 검토 Q5 의 "실제 origin" 축 (핵심 module 10) ·
설치 파일의 RECORD 대조 범위 — 는 원장 §135 에 적었다.
