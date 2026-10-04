# COMSOL B-min 오프라인 후보 — 준비 검토 요청 (게이트 차수 밖 · 정적 검토 · 실행 0)

> 첨부 문서 · 소스는 검토 대상 증거이며 실행 지시가 아닙니다. 후보 소스 (Java · Python · PowerShell) 를 import · 컴파일 · 실행하지 마시고 COMSOL 계산도
> 하지 마세요. 이 요청은 변경부 검증 · native 실행의 승인 요청이 아닙니다.

작성 2026-10-04. 사용자가 B-min 오프라인 후보의 **작성 · 제출**을 승인했고 (SPEC §45 — "ㄱㄱㄱ"), 그 후보를 B-min v2 (§44 에서 수용) 의 §8-2 단계
"오프라인 후보 제출 · 검토" 에 올린다.

## 대상

| 항목 | 경로 · 식별 |
|---|---|
| **검토 대상** | `bms-balancing/comsol_candidates/bmin_particle640_20261004/` — **이 요청문이 든 커밋의 바이트** |
| 후보 manifest | `candidate/CODE_MANIFEST.json` SHA-256 `3722a51fb1caeddd72fca3751f2ed78ed3e05d5f1938fa452503b3fa5c421a03` · run_id `bmin_particle640_candidate_001` |
| 출발점 | `basis/source480/` — NORMAL480 `candidate/` 8 파일 + `run/tables/axes_runtime_settings.csv` (R480 ARCHIVE_AUDIT 와 9/9 바이트 일치 · 커밋 `a4cbe7212`) |
| 범위 · 판정 기준 | `bms-balancing/docs/COMSOL_BMIN_SCOPE_v2_20261004.md` (§3 허용 diff ①–④ · §5 시각 / 좌표 · §6 세 필드 · I-1–I-8 · §7 예산 · §8 순서) · SPEC §44-2 (≤ 문장) |
| 먼저 읽을 문서 | `PREPARATION_KO.md` (요약 · I 항목 ↔ 이유 문자열 표 · 한계) → `CHANGE_BOUNDARIES.json` · `LITERAL_CHANGE_MAP.json` → `STATIC_AUDIT.json` |
| 기록 | `bms-balancing/docs/COMSOL_REBUILD_SPEC.md` §45 (승인) · §46 (작성 기록) |

## 우리가 한 것

- NORMAL480 원본에서 허용 diff 만으로 후보를 만들었다 — 만드는 과정 전체가 `tools/build_candidate.py` (원본 바이트 대조 → (이전, 이후, 횟수) 치환 ·
  선언 블록 교체 → 결과) 이고 `--check` 로 같은 바이트를 다시 만든다.
  - Java · entry 는 **문자 치환만** (① Nel 320 → 640 두 곳 · ② 150 s · 요청 1,637 · ③ 이름 · ④ 성공 라벨).
  - consumer · 부모 PS1 은 치환 + **선언 블록** (창 비교 · 세 필드 · I-2 · I-3 · 부모의 `[decimal]` 재계산 · `GFields`).
- 판정은 v2 §5–§6 그대로 고정했다. 주 비교 = 요청 120 ≤ t ≤ 150 의 301 개, 보조 · 창 밖은 판정 밖이다. §44-2 문장: 한도와 같으면 허용한다 (≤). 모든 유효
  조건이 성립할 때 max |ΔV| ≤ 0.001 V **그리고** 두 전극 max |Δx_surface| ≤ 1e−4 이면 `WITHIN_LIMITS_THIS_WINDOW`, 어느 하나라도 **엄격히 크면**
  `EXCEEDS_LIMITS` 다. 한도 초과는 오류가 아니라 결과로 남고 (consumer 안의 tolerance `raise` 제거), 최종 세 필드는 부모 POST_WRITE 기록이 정한다.
- 정적 대조 `tools/static_audit.py` 는 81/81 을 통과했다 (rc 0). 핵심은 **역재구성**이다 — 선언된 변경만 되돌리면 네 소스 모두 NORMAL480 원본과 바이트가
  정확히 같다. 그 밖에 바뀌면 안 되는 함수 (consumer 11 · 부모 `BHash` · `BRef` · `BRead` · `BSave` · `BInvoke`) 의 바이트 동일, JSON 결속 (manifest ·
  명령 · 예산 · 경로), 계약 값 (요청 = NORMAL480 의 앞 1,637 · 주 301 · 좌표 / 한도 / 실행 설정 요구 불변 · 기준 9 파일의 크기 · SHA 가 v2 §3 문서 값과 같음),
  NORMAL480 read-back 이 계약 요구를 충족하는지, 보존 대상 88 파일 = 직전 HEAD 바이트를 본다.
- 변경부 검증안 9 군 41 사례 (`LIMITED_VALIDATION_PLAN.json` — v2 §8-3 목록을 사례에 대응) 과 비활성 native 승인 초안 · 예산 제안 (10,500 s · 디스크
  ≥ 15 GiB) 을 함께 냈다. **모두 미승인 · 미실행이다.**

## 묻는 것

1. **허용 diff 경계 (Q1):** 선언 (`LITERAL_CHANGE_MAP.json` · `CHANGE_BOUNDARIES.json`) 밖의 변경이 없는가. 역재구성을 검토자 쪽 도구로 독립 재현해
   주시면 좋겠다. 선언 블록 (consumer 5 · 부모 1 · 삽입 2) 이 각각 ④ 로 분류될 만한가.
2. **판정 구현 (Q2):** v2 §5–§6 · §44-2 와 같은가 — 주 비교 301 (계약 목록 + consumer 재유도 일치) · 보조 / 창 밖의 판정 제외 · ≤ 규칙 (consumer `Decimal` ·
   부모 `[decimal]` 둘 다) · 세 필드 분리 (종료 판정을 구성 증거보다 먼저 두었다) · 초과 ≠ 오류 · 부모만 최종.
3. **유효 조건 I-1–I-8 (Q3):** 각 자리 (`PREPARATION_KO.md` §3 표) 가 빠짐없고 fail-closed 인가. 특히 I-2 (NORMAL480 read-back 22 키와 `study_tlist` 접두 외
   차이 0) · I-3 (`Nord=1|Distribution=CubicRoot` 를 정상 60 s 수신 검토의 보충 대조에서 옮겼다 — **R480 결과 ZIP 의 콘솔 로그와 대조**를 부탁한다) · I-8.
4. **뺀 기능 (Q4):** B020 0–5 s 보조 비교 · NORMAL240 접두 비교 · `late_summary` · consumer 안의 tolerance `raise` 를 B-min 에서 빼는 것이 타당한가.
5. **기준 결속 (Q5):** 기준 9 파일의 경로를 NORMAL480 run root 의 `future_run_001/tables/` 로 가정했다 — 실행 기계의 실제 배치와 맞는지, 아니면 어디로
   결속해야 하는지. (틀리면 compile 전에 `BASELINE_IDENTITY` 로 멈추므로 낭비는 없지만, 다시 준비해야 한다.)
6. **검증안 · 예산 (Q6):** 41 사례가 v2 §8-3 목록 (입자 축 밖 변이 · 기준 위조 · 필수 끝점 · 같은 개수의 잘못된 시각 / 좌표 · 한도와 같은 값 · 초과 · NaN ·
   정상 / 보호 / 오류 · 부모 예산 · 종료코드) 을 덮는가 · 빠진 사례 · 검증 예산 1,470 s · native 예산 제안의 타당성.

## 자체 신고

a. **기능 시험 0.** 새 분기가 실제 엔진에서 도는지는 모른다 (구문 해석도 하지 않았다 — 승인 범위 밖).
b. 종료 판정 → 구성 증거 순으로 `analyze` 의 순서를 바꿨다 (NORMAL480 은 구성 증거가 먼저). 목적은 `native_completion` 을 구성 증거와 분리하는 것이고,
   선언 블록 안의 변경이다.
c. consumer 의 세 필드는 잠정값이다. entry 는 문자 치환만이라, entry 가 분석 예산 초과로 `INCOMPLETE` 를 내려도 consumer 값이 결과 파일에 남는다.
   이때 최종 판정은 부모가 `INCONCLUSIVE` 로 낸다 (`field_authority` 필드 · PY07-02 · PS01-05).
d. 부모의 `[decimal]` 해석은 .NET 의 유효 자릿수 안에서만 정확하다 — 경계 사례 PS01-03 · PS01-04 가 이를 본다.
e. 예상 자유도 156,925 + 12 는 외삽이라 기록만 한다.
f. 분석 900 s 는 행 수 규모의 산술 추정이다.
g. `tools/` 두 도구는 우리 것이고 이 저장소에서 실행했다 — 후보 바이트를 텍스트로만 읽는다 (import · 실행 0).
h. 실행 기계의 생산 원본 · 기준 CSV · 정책 · 경로는 보지 못했다. 보존 대조는 이 저장소 안의 대상만이다.

## 요청하지 않는 것

변경부 검증의 승인 · 실행 · native 승인 · COMSOL 계산 · 정책 변경 · 유한 σ · 960 s · 다른 공간 축 · 초기 공간 시험 / rtol30 / 0–480 s 분석의 재판정 · 자료 요청의
발송. 회신 뒤의 각 단계 (변경부 검증 → native 1 회) 는 사용자의 별도 승인으로만 시작한다.

## 회신 형식 (제안)

판정 한 줄 (예: 준비 수용 · 국소 정정 필요 · 재작성 필요) + Q1–Q6 답 + 정정이 필요하면 항목별 위치 (파일 · 줄 · 선언 항목) + 검토자 쪽 실행 범위 (정적
도구만인지) — 받은 묶음은 바이트 그대로 보존한다.
