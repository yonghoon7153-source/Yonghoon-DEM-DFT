# 검토 담당 Codex 발송 프롬프트 — S1O-R1 정정본 소스 검토 · 2026-10-08

> 원장 `COMSOL_REBUILD_SPEC.md` §79. 아래 `---` 사이가 붙여 넣을 본문이다.
> 같이 첨부: ① `COMSOL_MICROSHORT_S1O_R1_OFFLINE_CORRECTIONS_20261008.zip` ② `COMSOL_MICROSHORT_S1O_R1_DELIVERY_SUPPLEMENT_20261008.zip`
> ③ `SUPPLEMENT_FINAL_TOOL_RETURN.json` (실행 PC 의 원 파일 — 이 저장소에는 사용자 채팅 전사만 있다).

---

첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

S1O-R1 (준비본 정적 검토의 S1O-N1–N4 좁은 오프라인 정정) 의 제출물을 검토해 주세요. **이번 요청은 검토만이며, 기능 검증 · COMSOL · native 의 승인이 아닙니다.**

## 고정 식별

| 대상 | 식별 |
|---|---|
| 정정본 본체 | `COMSOL_MICROSHORT_S1O_R1_OFFLINE_CORRECTIONS_20261008.zip` · 813,053 B · sha256 `0a18cb64f8bcbcd4725b45088ee310f85e9292a1ffdced2332b5102f5fd6f9dc` · 117 항목 · PACKAGE_MANIFEST sha256 `027375361a4c…` · 새 CODE_MANIFEST sha256 `4ce5c08dbde5153027819b5a651e3995ec82417b4429b9bb0f789082b440f5da` |
| 전달 보충 | `COMSOL_MICROSHORT_S1O_R1_DELIVERY_SUPPLEMENT_20261008.zip` · 3,750 B · sha256 `4cfd310ae5c019cce63a2ce012debfa9307f44ac739c1253cc07a5cf0c8d73b2` |
| 마지막 반환 · 종결 | `SUPPLEMENT_FINAL_TOOL_RETURN.json` (closeout `SUPPLEMENT_CLOSEOUT.json` 1,888 B · sha256 `a386eb3b…46ef`) |
| 정정 대상 준비본 | zip sha256 `0cae7acc…aaf53` · CODE_MANIFEST `54c61d10…965fe` (이전 검토 회신 `dee50be8…` 에 펼친 사본) |
| 지시 · 승인 | 발송문 v2 sha256 `eac2eb0adbc39b608a65b8db154947dc9ee5a8cb9f40bddc7644d42f9b227499` (= 정정본 `reference/R1_DIRECTIVE_v2_KO.md`) · 원장 §77 · §78 |

## 이 저장소가 먼저 확인한 것 (데이터 대조만 · 받은 코드 실행 0)

- 두 zip 의 크기 · sha256 = 종결 기록 · manifest 116 / 116 · CODE 21 / 21 · 보충 4 / 4 · 비밀 패턴 0.
- 바뀐 파일 7 (`CHANGED_FILES.json`): consumer · Parent · P0 diff / java · `CHARGE_BALANCE.json` · `EXECUTION_BINDING.json` · `SOURCE_CONTRACT_LINKS.json` — 7 개의 "이전" sha 는 모두 준비본 원본과 같고,
  바뀌지 않은 코드 13 파일은 준비본과 바이트 동일 · `VALIDATION_PLAN_R1.json` 은 새 파일.
- 새 판정 이유 코드가 N1 (`CHARGE_GRID_BINDING` · `CHARGE_ENDPOINT_BINDING` · `CHARGE_GLOBAL_LI_MISMATCH` …) · N2 (`REVERSE_LI_INCREMENT` · `REVERSED_BEYOND_DEADBAND`) ·
  N3 (`COMPARISON_TIME_CONTENT` · `COMPARISON_TIME_ORDER_OR_RANGE` · `COMPARISON_NOT_INTERSECTION_SUBSET` · `EXPECTED_REQUEST_VECTOR` …) 에 생겼고, N4 는 P0 439 의 문구가 "accepted tsteps storage" 로 바뀌었다
  (이름의 존재만 본 것 — 분기 정확성은 검토 몫).

## 검토해 주실 것

1. **N1–N4 의 정적 종결** — 이전 회신의 반례 (charge 0–1 s 만 · 누적 양수 속 증분 −0.00075 · 같은 길이 `"0"` 255 개 · P0 문구) 가 새 코드의 어느 분기에서 어떤 이유로 거부되는지 추적.
   정상 경로 (정상 끝 · 보호중단 safe prefix) 를 잘못 거부하지 않는지. 소비자와 부모가 같은 새 구조 (`S1O_CHARGE_BUDGET_R1` 등) 를 보는지.
2. **범위 준수** — 바뀐 7 파일이 승인 범위 (판정 코드 · 영향 계약 · manifest) 안인지 · 허용치 · deadband · 물리 · 초기조건 · σ · OCP · 해상도 · cap · 출력 API 불변인지 · 설치본 / 어댑터 OPEN 을 몰래 채우지 않았는지.
3. **갱신 검증안** — 8 군 130 사례 (Python 99 · PowerShell 31 · 옛 98 매핑 + 새 32) 의 ID · 양성 / 음성 · 정확한 이유 · 도달 단계 · 엔진 · 봉인 규칙 · PARENT03 safe-prefix 기대 개수 · PAIRED04 D / S / E_D / E_S 전부 ·
   Decimal → double 경계의 fail-closed · 제안 예산 1,860 s (별도 승인 대상) 의 적정성.
4. **기록** — 시간 원점 · 단계 경계 (작성 693.8 · 정적 343.3 · 봉인 392.0 · 전달 36.4 s · 상한 2,700) · snapshot 과 반환 전사의 범위 구분 · 원본 불변 (`ORIGINALS_BEFORE` / `AFTER`) ·
   승인 근거 `USER_OFFLINE_SCOPE.txt` 가 v2 §0 전문이 아닌 요약 문장이라는 점 (v2 전문은 `reference/` 에 sha 로 결속 — 의견 바람) · 사용자 메시지의 "1,541.319 / 2,700 초" 와 전사의 `post_return_capture` 1,541.2375 s 의 관계.

## 하지 않는 것 · 회신 형식

받은 코드 import · 함수 호출 · 검증안 실행 · Java 컴파일 · JVM · COMSOL · approval / release / runtime 생성. 회신: 판정 · 발견 (P1 / P2 / 경미 · 파일:줄 · 최소 조치) · 기능 검증 승인 문안 초안 (사례 수 · 엔진 · 예산 · 중단 조건) · `DECISION.json`.

---
