# 실행 담당 Codex 발송 프롬프트 — S1 OPEN 연결부 한정 오프라인 준비 · 2026-10-09

> **사용자가 §0 의 채택 문구를 승인한 뒤에만 보낸다.** 승인 전에는 초안이다. 원장 `COMSOL_REBUILD_SPEC.md` §84.
> 아래 `---` 사이가 붙여 넣을 본문이다. 같이 첨부: R1_004 보충 검토 회신 zip (`COMSOL_MICROSHORT_S1O_R1_004_SUPPLEMENT_REVIEW_20261009.zip` · 1,609,510 B · sha256 `17779cbd…5e0e`).
> 그 안의 `NEXT_APPROVAL_DRAFT_KO.md` 가 이 승인의 세부 조건이고, `reference/PRIOR_REVIEW.zip` 이 앞선 R1_004 검토 회신이다.
> 네트워크 읽기는 초안대로 **넣지 않았다**. 공식 문서 온라인 열람까지 허용하려면 승인 전에 §2 의 해당 줄을 바꾼다.

---

첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

## 0. 승인 범위 (사용자 채택 문구 — 독립 검토 초안 원문 그대로)

> 수용된 S1O R1 기능과 실패 기록을 보존한 채, 남은 설치본 관측·raw 증거·OS 자원/중단 연결부의 한정 오프라인 준비 한 건을 승인합니다. 기존 전체 검증을 반복하지 말고, 설치본 정적 근거와 최소 diff의 비활성 연결 후보, 아직 관측이 필요한 항목 및 변경부 한정 검증안을 제출한 뒤 멈추세요. 실제 COMSOL/JVM/compile/solve·입력 gate·process/Job 실험·정책 변경·approval/release/runtime/token 생성·native 실행은 승인하지 않습니다. 설치본 호출 없이는 확정할 수 없는 API/관측은 추정하지 말고 별도 승인 항목으로 남기세요.

세부 조건은 첨부 회신의 `NEXT_APPROVAL_DRAFT_KO.md` (5,756 B · sha256 `f634ba2133f9b0e8eda78b23ba7870f3468e65c13be0499f03e14435e76df79b`) 의 "경로와 보존" · "이번에 고정할 연결" ·
"새 제안 한도와 종료" · "S1-P로 넘어갈 조건" 을 그대로 따른다.

## 1. 고정 식별

| 대상 | 식별 |
|---|---|
| 새 폴더 (하나) | `C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/microshort_s1_open_connection_candidate_20261009/` — 이미 있으면 생성 · 덮어쓰기 · 삭제 · 재사용 · 이름 우회 없이 중지 |
| 수용 소스 (고치지 않음) | CODE_MANIFEST sha256 `4ce5c08dbde5153027819b5a651e3995ec82417b4429b9bb0f789082b440f5da` + 구성원 21 (Parent sha256 `e9f8d366ca9931b84ded5753a560369b72fea8737a77075bc2b80ec771bc56ff`) |
| 기준 기록 | R1_003 결과 zip `11a27f3034fed763442ccce9730f7e008058b819bfbffd9d58a5d2994b875d4b` · R1_004 결과 zip `cb85fa123395caf9ea323b0c531144bf30754322ba9b0362f1bbac3e5bc8ff2c` · 앞선 검토 회신 zip `9524f8ce7e5cef2722675806a2d92ac69b27188012bf50c758de7a260dee1486` · 보충 검토 회신 zip `17779cbd61b2d592c15195d6b9810402042d790a6badd43bc9c5df1512bb5e0e` |
| 판정 | `LIMITED_VALIDATION_CLOSED_WITH_DOCUMENTED_SCOPE` · OPEN 4: `installed_post_consistency_t0` · `installed_effective_coefficient_mapping` · `raw_native_evidence_adapter` · `OS_resource_ownership_stop_adapters` |

## 2. 요점 (세부는 초안 문서)

- **할 일 넷:** (1) 설치본 t0 / CDI 경로 (2) 계수와 raw 증거의 대응 (3) native / OS 연결의 비활성 후보 (4) 변경부 한정 검증안. 시험 · native probe 는 실행하지 않는다.
- **읽기만:** 기존 자료 · 설치본 문서 / 텍스트 / API 설명 · 파일 식별의 정적 대조. MPH 를 COMSOL 로 열지 않고 받은 모듈을 import / 실행하지 않는다. 기존 source / manifest / 계약 / 상태 /
  기준 결과 / MPH / prefs / 원장은 고치지 않는다. 새 코드는 새 폴더의 비활성 사본으로만 쓰고 원본과의 최소 diff 를 낸다.
- **네트워크:** 설치 · fetch · 네트워크 조회 · 환경 재구축 · 권한 상승은 포함되지 않는다. 로컬에 없는 문서가 필요하면 추정하지 말고 "별도 허용 목록" 에 적는다.
- **확정 못 하는 것:** 설치본 호출 · 추가 initialization / solve 가 필요한 관측, 확인되지 않은 cooperative stop 은 미확인으로 남기고 별도 허용 목록에 적는다. 강제 종료를 graceful 로 기록하지 않는다.
- **예산 (새 원점 · 한 번 · 3,600 초):** 준비 / 비활성 후보 작성 2,400 · 정적 대조 600 · 보존 · 전달 480 · 미완 정리 120. 단계 사이 전용은 없고, 과거 1,200 초나 native 예산의 연장이 아니다.
- **자원:** 새 폴더 ≤ 50 MiB · 대형 원자료 복사 0 · native / JVM / 기능 시험 0 · 시작 디스크 여유 ≥ 512 MiB 를 읽기 전용으로 관측 · 지원되지 않는 자원 관측을 0 / PASS 로 채우지 않는다.
- **제출물:** OPEN 별 근거 / API / 산출 / 소비 대응표 · 새 파일과 최소 diff / 원본 불변표 · 고정 식별 · 정적 대조 · 새 원점 / 시간 기록 · 변경부 검증안 · 실제 관측에 필요한 별도 허용 목록.
  경로 / 식별 불일치 · 예정에 없던 변경 · 예산 초과가 나면 첫 오류와 자료를 보존하고 중지한다.
- **전달 기록:** 마지막 쓰기 · 재읽기 뒤 snapshot 과 외부 반환 경계를 구분한다. ZIP 밖 기록 (영수증 · 포장 도구 반환 · 최종 확인) 은 모두 파일로 남기고 그 링크를 한 번에 알려 주세요
  — 지난번에는 최종 확인 파일 링크가 빠져 검토가 한 번 더 왕복했습니다.

## 3. 유지

`native_ready=false` · 전체 / 정상 gate INCOMPLETE · 실효 정책 / 실제 코어 UNVERIFIED. 이 준비를 통과해도 `native_ready` 를 바꾸지 않는다. P0 조차 실행 미승인이고, P1–P3 · K cohort ·
장시간 cohort · 미세단락 효과의 결과 주장은 없다. 초안 문구로 approval JSON 이나 permission token 을 만들지 않는다. 제출 뒤 멈춘다.

---
