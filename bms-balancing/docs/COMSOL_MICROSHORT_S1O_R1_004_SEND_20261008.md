# 실행 담당 Codex 발송 프롬프트 — S1O-R1 검증 잔여 보완 (R1_004 · Python 양성 4 + PowerShell 미완 3) · 2026-10-08

> **사용자가 §0 의 채택 문구를 승인한 뒤에만 보낸다.** 승인 전에는 초안이다. 원장 `COMSOL_REBUILD_SPEC.md` §81.
> 아래 `---` 사이가 붙여 넣을 본문이다. 같이 첨부: R1_003 중지 검토 회신 zip (`COMSOL_MICROSHORT_S1O_R1_003_STOP_REVIEW_20261008.zip` · sha256 `56c52add…`) — 그 안의
> `NEXT_LIMITED_APPROVAL_DRAFT_KO.md` 가 이 승인의 세부 조건이다.

---

첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

## 0. 승인 범위 (사용자 채택 문구 — 독립 검토 초안 원문 그대로)

> R1_003 원본·실패·127개 PASS와 생산 코드를 그대로 보존하고, 검토 회신 S1O003-N1/N2의 하네스 및 동일 기본 입력 양성 보완을 승인합니다. 새 원점1200초 안에서 Python 양성4개1세션, Windows PowerShell5.1 미완3개1세션만 수행하세요. 기존99개/28개와 실패한 세션을 통째로 다시 돌리지 마세요. 사전 봉인 또는 기존 결과 재사용 조건을 충족하지 못하면 시험 전에 중지하고, 최초 예상 밖 실패 뒤 수정·재시도·부분probe는 하지 마세요. COMSOL/JVM/Java컴파일/native/실제입력·Job·정책 변경 및 실제 approval/release/runtime/token 생성은 승인하지 않습니다. 결과와 원문을 제출한 뒤 멈추세요.

세부 조건은 첨부 회신의 `NEXT_LIMITED_APPROVAL_DRAFT_KO.md` (7,819 B · sha256 `8bd02f0fbecbd3612635be2a234ac250533f404db7b7cf98b1f1d5b394912015`) 의 "경로와 불변" · "사전 고정할 새 입력7개" ·
"R113 하네스 정정과 결과 재사용" · "예산과 중단 및 제출" 을 그대로 따른다.

## 1. 고정 식별

| 대상 | 식별 |
|---|---|
| 새 fixture 폴더 (하나) | `C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/microshort_s1o_r1_20261008/future_validation_fixture_R1_004/` — 이미 있으면 생성 · 덮어쓰기 · 삭제 · 재사용 · 이름 우회 없이 중지 · 001 / 002 / 003 은 변경하지 않음 |
| 수용 소스 | CODE_MANIFEST sha256 `4ce5c08dbde5153027819b5a651e3995ec82417b4429b9bb0f789082b440f5da` · Parent sha256 `e9f8d366ca9931b84ded5753a560369b72fea8737a77075bc2b80ec771bc56ff` (나머지 생산 파일은 원 manifest 21 로 대조) |
| 재사용 출처 | R1_003 zip sha256 `11a27f3034fed763442ccce9730f7e008058b819bfbffd9d58a5d2994b875d4b` (876,456 B · 153 payload) 의 FIRST_SEAL · 하네스 · results · producer seal |
| 검토 회신 | R1_003 중지 검토 zip sha256 `56c52add014684850a533136d1add01e1a937db1cebcbc0236d40413cc5eaffe` · 원장 §81 |

## 2. 요점 (세부는 초안 문서)

- **새 입력 7 개만:** Python 보조 양성 4 (READ_CTRL_CSV · READ_CTRL_TIME · READ_CTRL_COVERAGE · READ_CTRL_PROFILE — READ02–12 와 같은 기본 입력) 1 세션 →
  모두 기대대로면 PowerShell 5.1 미완 3 (PARENT_R115 → 개정 PARENT_R113 → PARENT_R114 순서) 1 세션. 기존 99 / 28 과 실패 세션은 다시 돌리지 않는다.
- **R113 정정 (S1O003-N1):** 원 POLICY02 producer 를 바이트 그대로 읽고, 따옴표만 지운 JSON 숫자 변이를 만든 뒤 **타입 assertion 전에** parse 직후 실제 CLR 타입 · 값을 기록 →
  유한한 해당 숫자인지 확인 → fixture 단계에서 단일 leaf 만 명시적으로 Double 로 변환 (전후 타입 · 값 · 64 비트 기록). parser 가 Double 을 만들었다고 쓰지 않는다 · cast 로 잘못된 입력을 숨기지 않는다.
- **결과 재사용:** R114 의 양성은 기존 PARENT02 (같은 소스 · 함수 · 엔진 · POLICY03 · 도달 기록) 를 재사용 표로 결속 — 몰래 다시 부르지 않는다. 재사용 조건이 깨지면 시험 전에 중지.
- **예산 (새 원점 · 1,200 초):** 계획 · 하네스 정정 · 봉인 600 · Python 120 · PowerShell 180 · 보존 · 전달 240 · 미완 정리 60.
- **집계:** 성공 시 "원 127 재사용 + 원 미완 3 신규 충족 · 보조 양성 4 별도" — 130 을 한 번에 통과했다고 쓰지 않는다. 원 R1_003 의 INCOMPLETE · 하네스 실패는 그대로 둔다.

## 3. 유지

`native_ready=false` · 설치본 t0 / 계수 / native / raw / OS 어댑터 OPEN · 전체 / 정상 gate INCOMPLETE. 실제 S1-P · COMSOL · microshort 계산은 별도 승인. 제출 뒤 멈춘다.

---
