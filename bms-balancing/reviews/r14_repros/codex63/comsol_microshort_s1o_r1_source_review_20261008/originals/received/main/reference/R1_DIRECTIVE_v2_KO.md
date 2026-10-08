# 실행 담당 Codex 발송 프롬프트 v2 — S1-O 판정 코드 좁은 오프라인 정정 (S1O-R1 · N1–N4) · 2026-10-08

> **사용자가 §0 의 채택 문구를 승인한 뒤에만 보낸다.** 승인 전에는 초안이다. 원장 `COMSOL_REBUILD_SPEC.md` §76 · §77.
> v1 (`…S1O_R1_SEND_TO_CODEX_20261007.md` · sha256 `6e3a9ca3…`) 은 그대로 둔다. v2 는 범위 검토 회신 (`…comsol_microshort_s1o_r1_scope_review_20261008/` · 판정 수용 · 새 차단 0) 의
> 비차단 명확화 넷만 반영했다: ① 새 폴더 절대경로 한 줄 + 시간 원점 · 단계 경계 · snapshot 범위 ② "98 사례" → 갱신 검증안의 실제 사례 수 ③ N3 에 "범위" ④ "실행 0" 의 대상. 그 밖은 v1 과 같다.
> 아래 `---` 사이가 붙여 넣을 본문이다. 같이 첨부: 준비본 검토 회신 zip (`COMSOL_MICROSHORT_S1O_PREPARATION_REVIEW_20261007.zip` · sha256 `dee50be8…`).

---

첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

## 0. 승인 범위 (사용자 채택 문구 — 승인 시 원문 그대로 붙인다)

> S1-O 준비본 정적 검토 회신의 S1O-N1–N4 만 고치는 좁은 오프라인 정정 (S1O-R1) 을 승인합니다. 대상은 준비본 (zip sha256 `0cae7accaf26397d883e0d8b732357fc2dc640553c603825a6a155bf8d4aaf53` · CODE_MANIFEST sha256 `54c61d10b3bb11e0501e9933b220eca76d9f7cee503953a6f909185e04f965fe`) 이고, 원본은 그대로 두고 새 폴더 **`C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/microshort_s1o_r1_20261008`** 에서만 정정본을 만듭니다 — 이미 있으면 중지하고, 삭제 · 재사용 · 다른 이름으로의 자동 우회는 하지 않습니다. 새 monotonic 시간 원점 · 단계별 경계 · 포장 뒤 snapshot 과 그 뒤 반환 전사의 범위를 `TIMING.json` 에 구분해 적습니다. 허용치 · deadband · 물리 · 초기조건 · σ · OCP · 해상도 · cap · 출력 API 는 바꾸지 않습니다. 정적 확인 (구문 parse · 해시 · 텍스트 대조) 만 하고, 후보 / 받은 코드의 import · 함수 호출 · 기능 시험 · Java 컴파일 · JVM · COMSOL · approval / release / runtime / token 생성은 하지 않습니다 ("실행 0" 은 이 대상에 대한 것이며, 정적 구문 parse · 해시 · 포장 도구의 사용은 따로 기록합니다 — 그 도구가 후보를 import / call 하는 경로는 허용하지 않습니다). 시도 1 회 · 상한 총 2,700 초 (정정 작성 1,200 · 정적 확인 600 · 검증안 갱신 · 봉인 600 · 전달 300) — 이전 준비의 3,600 초 · 미실행 검증 1,500 초를 다시 쓰지 않으며, 넘으면 멈추고 미완으로 보고합니다. 제출 뒤 멈춥니다. 갱신 검증안의 기능 검증 (기존 98 ID 와의 대응 및 새 실제 사례 수 명시) · S1-P · M · N 은 각각 별도 승인입니다.

## 1. 고정 식별

| 대상 | 식별 |
|---|---|
| 정정 대상 준비본 | zip sha256 `0cae7acc…aaf53` · CODE_MANIFEST sha256 `54c61d10…965fe` (21 파일) · MANIFEST 112 |
| 준비본 검토 회신 | `COMSOL_MICROSHORT_S1O_PREPARATION_REVIEW_20261007.zip` · 805,653 B · sha256 `dee50be8d7dd1bcfd14323878deaeda1d31729f4f850cda5d6158bf64dfda46f` (특히 `REVIEW_KO.md` · `NEXT_SCOPE_DRAFT_KO.md` · `notes/`) |
| 원 발송문 · 승인 | v2 (커밋 `f2d6fa0a9` · sha256 `16797cc1…`) · 원장 §73 · §75 · §76 |

## 2. 고칠 것 — 회신 N1–N4 와 다음 범위 초안 1–5 그대로

1. **S1O-N1 (P1) · 수지 시각 결속** — `consumer.py` `charge_balance` (218–255) 와 `analyze` (295–317): charge 행의 **시작 · 끝 · 정확 격자**를 native 의 실제 저장 격자와 같은 집합으로 결속 · 정상 끝 / 보호중단 실제 끝 / 수치 비교 safe prefix 구분 ·
   charge 행의 LiN / LiP / LiE 와 같은 시각의 `global` Li 원자료의 동일 출처 · 시각 대조. 부모 (`Parent.ps1` 112) 의 charge 기록 검사도 같은 구조를 본다.
2. **S1O-N2 (P2) · 구간 역행** — 누적 q (237–238) 와 별도로 직전 행 대비 signed Δq_N · Δq_P 의 방향 / deadband 검사 · 최초 위반 구간 기록. 기존 단위 · deadband · 잔차 허용치는 완화하지 않는다.
3. **S1O-N3 (P2) · 부모 coverage 내용** — `Parent.ps1` 117–124: 기대 목록을 고정 요청 목록과 검증된 safe end 에서 **유도** (결과의 count 에서 복사하지 않음) · 유한성 · 순서 · 중복 · 정확 시각 · **범위** (각 원소가 고정 요청 창과 검증된 safe end 안) ·
   전체 교집합 포함 관계를 원소 단위로 검사.
4. **S1O-N4 (경미) · P0 문구** — `P0.java` 416 은 `tout = tsteps` 인데 439 의 요약이 "requested tlist storage" — 문구만 실제 설정에 맞춘다.
5. 영향받는 출력 schema · 계약 (`CHARGE_BALANCE.json` 등) · 검증안 · CODE_MANIFEST 만 함께 갱신. 소비자와 부모가 같은 새 구조를 본다. 원본 의미를 조용히 바꾸지 않는다.

## 3. 갱신 검증안 (제시 · 봉인만 — 실행하지 않음)

- 새 반례: 정상 전체 charge · 끝 / 중간 누락 · 같은 길이 격자 변이 / 양의 누적 속 역방향 증분 (회신 예: t=100 q 25.001 → t=100.001 25.00025) · 정확 deadband 경계 · deadband 안 미세 변화 /
  실제 Python 출력 → 봉인 JSON → PowerShell 양성 · 같은 길이 중복 / 다른 시각 / 비유한 음성 / 보호중단 safe-prefix 기대 개수의 독립 유도와 PROTECTIVE_STOP 분기 도달 (PARENT03) /
  PAIRED04 의 D · S · E_D · E_S 전부 / Decimal → double 경계의 명시적 fail-closed 판정.
- 각 ID 의 양성 · 음성 · 정확한 이유 · 도달 단계 · 엔진 · 상한 · 기존 98 ID 와의 대응 · 새 실제 사례 수 (98 에 맞추지 않는다). 생산 코드 · harness · 추출 범위 · 이유 · 도달 단계를 첫 시험 전에 봉인하는 원칙 유지.

## 4. 유지 · 하지 않는 것

설치본 t0 / 계수 연결 · raw / native 어댑터 · OS 자원 감시 / 중지는 **명시된 OPEN 그대로** (몰래 완성하지 않는다 · true 로 채우지 않는다). `native_ready=false` · 전체 / 정상 gate INCOMPLETE · 정책 / 실제 코어 UNVERIFIED 유지.
P0–P3 / K / 비용 설계의 정합한 부분은 그대로. 전체 suite · 기존 native 재실행 없음. 24 회 / 60 시간은 미승인 명목 상한 그대로.

## 5. 회신 형식

`R1_REPORT_KO.md` (N1–N4 · 고친 파일:줄 · 전 / 후 diff 요약) · 정정본 전체 + 새 `CODE_MANIFEST.json` (원본 대비 바뀐 파일 목록 · sha256) · `VALIDATION_PLAN_R1.json` / `_KO.md` (§3) ·
원본 불변 증거 (작업 전 / 후 sha) · `TIMING.json` (새 monotonic 원점 · 단계별 경계 · 상한 대비 · 포장 뒤 snapshot 과 반환 전사의 범위 구분) · `DECISION.json` (`r1_status` · N1–N4 별 `fixed / partial / open` · `functional_validation: NOT_RUN` · `native_ready: false` · 후보 / 받은 코드 함수 · 기능 시험 · COMSOL / JVM 실행 0 확인 · 정적 도구 사용은 따로 기록).

---
