# 실행 담당 Codex 발송 프롬프트 — S1O-R1 검증안 정정 · 봉인 + 변경부 한정 기능 검증 1 건 · 2026-10-08

> **사용자가 §0 의 채택 문구를 승인한 뒤에만 보낸다.** 승인 전에는 초안이다. 원장 `COMSOL_REBUILD_SPEC.md` §80.
> 아래 `---` 사이가 붙여 넣을 본문이다. 같이 첨부: R1 소스 검토 회신 zip (`COMSOL_MICROSHORT_S1O_R1_SOURCE_REVIEW_20261008.zip` · sha256 `4a30055f…`) — 그 안의
> `VALIDATION_APPROVAL_DRAFT_KO.md` 가 이 승인의 세부 조건이다.

---

첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

## 0. 승인 범위 (사용자 채택 문구 — 독립 검토 초안 원문 그대로)

> S1O-R1의 생산 소스는 바꾸지 않고, 독립 검토 R1-V1–V3의 검증안 정정과 사전 봉인 명확화를 포함한 변경부 한정 검증1건을 승인합니다. 새 원점 전체1860초, Python99사례1세션/Windows PowerShell5.1 31사례1세션, 총8군130고유 입력을 상한으로 합니다. 정적 봉인 조건이 충족되지 않거나 더 많은 입력·세션·생산 코드 변경이 필요하면 기능 시험 전에 중지해 새 승인을 요청하세요. 최초 예상 밖 실패·예산 초과 후 수정·재시험·부분 probe·다른 엔진 fallback은 승인하지 않습니다. COMSOL/JVM/Java 컴파일/native/실제 콘솔·Job·정책 변경 및 실제 approval/release/runtime/token 생성은 승인하지 않습니다. 결과와 첫 실패를 보존하여 제출한 뒤 멈추세요.

세부 조건은 첨부 회신의 `VALIDATION_APPROVAL_DRAFT_KO.md` (7,332 B · sha256 `4b32d38a3090db4c7b22f08b927b89d3a0ee3adf9458a9e85952b5ea68ac3910`) §1–§5 를 그대로 따른다
(고정 출발점 · fixture 폴더 · 첫 기능 호출 전 필수 정정 · 두 단계 봉인 · 예산 표 · 중단 · 제출).

## 1. 고정 식별

| 대상 | 식별 |
|---|---|
| 수용된 R1 소스 | 본체 zip sha256 `0a18cb64f8bcbcd4725b45088ee310f85e9292a1ffdced2332b5102f5fd6f9dc` · CODE_MANIFEST sha256 `4ce5c08dbde5153027819b5a651e3995ec82417b4429b9bb0f789082b440f5da` |
| 고정 생산 소스 | consumer `0cb1aa3cc4593dcb041115baf208c4dd09186fcc75055ddcde53c68086cc6b79` · Parent `e9f8d366ca9931b84ded5753a560369b72fea8737a77075bc2b80ec771bc56ff` · control `8ec75e57336c4ffa33e61d513076fb1facd1cf90430b1e1ce1c15f9bb57ac00d` (그 밖은 CODE_MANIFEST 로 대조) |
| fixture 폴더 (새로 · 하나) | `C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/microshort_s1o_r1_20261008/future_validation_fixture_R1_001/` — 이미 있으면 재사용 · 삭제 · 덮어쓰기 · 이름 우회 없이 중지 |
| 검토 회신 · 승인 | R1 소스 검토 zip sha256 `4a30055f50990df5265ca2944ac3320966aff850d5efb35d78038e0f4a6da48f` · 원장 §79 · §80 |

## 2. 첫 기능 호출 전 필수 정정 (생산 코드 불변 · 하네스 720 초 안)

1. **R1-V1:** `VALIDATION_PLAN_R1.json` 의 S1Sha 추출 23–22 (빈 범위 · 적힌 sha `e3b0c442…` 는 빈 문자열의 해시) → 23–23 · LF 정규화 · 끝 LF 제외 90 B · sha256 `13c6456b30805e3b02063ca8cb804b201d948c5518bf01b102610297236d8eed`.
   추출 범위가 비어 있지 않음 · 함수 이름 · 범위 · 필수 집합 · 원문 해시를 정적으로 대조. 원래의 잘못된 감사 결과는 보존하고 정정 이력을 더한다.
2. **R1-V2:** PARENT12 는 없는 `return_value.status` 가 아니라 실제 `S1FinalReturn` 반환의 `return_value.limited` 와 final-boundary 관측 모드를 본다. 생산 반환을 시험에 맞춰 바꾸지 않는다.
3. **R1-V3:** 계수 음성 INIT07 · 08 · 10 의 양성 대조 = 같은 함수 (`verify_coefficient_evidence`) 의 INIT09 · `S1FinalReturn` 음성 PARENT09 · 10 · 11 · 16 의 양성 대조 = 정정한 PARENT12.
   나머지 대조도 함수 · 입력 · 도달 단계별로 확인하고 PARENT14 의 실제 analyze INCONCLUSIVE producer 와 복수 leaf 변이 목록을 사전 명시. 130 입력 안에서 해결되지 않으면 **시험 전에 중지**.

## 3. 유지

`native_ready=false` · 설치본 t0 / 계수 · native / raw / OS 어댑터 OPEN · 전체 / 정상 gate INCOMPLETE · 정책 / 실제 코어 UNVERIFIED. 이 검증이 모두 통과해도 실제 P0 · native 승인과 무관하다.
이전 R1 전달의 `SUPPLEMENT_FINAL_TOOL_RETURN.json` · `SUPPLEMENT_CLOSEOUT.json` 원파일은 (있다면) 기존 파일 그대로 별도 보충할 수 있다 — 이번 검증으로 과거 시간을 다시 재지 않는다.

---
