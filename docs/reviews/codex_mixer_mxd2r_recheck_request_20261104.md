# 믹서 D2 개발 소비자 — MXD2R 수정 짧은 재확인 요청 (2026-11-04)

| 이번에 닫는 것 (종결 **요청**, 현재 claimed_fixed) | 닫지 않는 것 |
|---|---|
| MXD2R-01 시간·삽입·공동 회전, MXD2R-02 접촉 제외·재료 완비성, MXD2R-03 실제 파일 바이트 결합 | MXD2-01 전체, 새 S1 셀·코호트·정책·등록·실물 입력 |
| MXD2R-04 생성기 토큰·문자 꼴 및 **neighbor skin까지** 고정한 개발 소비자 범위 | 실제 DEM/LIGGGHTS 실행, WSL/ibb 실행, 물리 결과·실행 GO |

이 창은 구현·요청 준비 창이다. 아래 재실행은 구현 측 증거이며 **외부 독립 재검토나 CLOSED 판정이 아니다**. 원장 MXD2R-01–04는 claimed_fixed, MXD2-01은 open 그대로다.

리뷰 핀은 **배포 ZIP 루트 `PIN.txt`의 전체 SHA**로 확정한다 (이 문서의 자기 SHA를 쓰지 않음). 이번 실행의 고정 기반은 `7b51e591e6482484d1b85b237dc0c73936fa96b6`; 비교 기준 `80095a7f0`부터 그 기반까지의 네 소비자·시험 파일 변경을 동봉했다. 최종 리뷰 핀의 해당 파일 SHA-256이 실행 증거와 같은지 먼저 대조해 달라.

**공용 게이트 상태 = HOLD · 이번 게시 = 검토용.** 전체 게이트 통과를 주장하지 않는다. 초기 LHS는 기존 미커밋 README를 감지한 청결 조건에서, 초기 믹서는 자기검사 세 항목의 시간 제한에서 실패했다. 깨끗한 LHS 후보의 추가 격리 검사도 기존 Rint E13d에서 `GROUP_UNCONFIRMED`로 실패했고, 원인 미확정 상태로 범위 밖 구현을 늘리지 않고 중단했다(rc 143). 직접 시험과 이 실패를 합산하지 않는다. 11-04 인계서 §1-6의 문서 참조·원장·변경 시험 근거를 별도로 제공하며, §1-5의 Claude 통합 전체 게이트와 실행·배포 GO는 남아 있다. 실패·중단 원문은 전달 ZIP의 `DELIVERY_VALIDATION/`에 포함한다.

## 1. 수정과 증거

| 항목 | 수정 | 근거 |
|---|---|---|
| MXD2R-01 | run 두 토큰, 첫 run 전 유일 dt, 삽입 생성기 꼴, 세 메시 공동 주기 | `c03de45c3`; 11-03 증거 상위 README §2·§4 |
| MXD2R-02 | 접촉 제외 거부, pair 꼴, 재료 fix 완비성·중복·순서·상수 | `708bf881a`; 같은 README §2; 후속 `f2f63e7cd` |
| MXD2R-03 | 실제 bytes의 SHA·길이 먼저 확인 → CR 거부 → 엄격 UTF-8, 세 CLI 바이트 읽기 | `f7c9c81b1`; 같은 README §2·§4 |
| MXD2R-04 | 모든 명령의 순서·개수·토큰 및 문자 꼴; neighbor skin = `min(활성 상 지름) * 0.5`의 `.6g` | `49608570a`, 후속 `52d84d9eb`, skin `b74fc9b75`; 하위 `docs/reviews/mxd2r_fix_evidence_20261103/mxd2r04/README.md` **§9가 최신** |

시험 먼저 커밋과 고치기 전 실패는 기존 증거에 보존했다. 이번에 과거 실패 실행을 다시 했다고 세지 않는다. skin의 예전 단일 덱 PASS 기대는 새 계약에 따라 FAIL로 바뀌었다; 짝 비교 FAIL은 그대로다 (§9-2).

## 2. 독립 검토 질문

1. 지난 HOLD의 공통 변조 (run 옵션·dt 위치·삽입 start·끝판 주기·접촉 제외·재료 누락)를 **양쪽 덱에 같이** 적용해도 세 소비자가 올바른 사유로 거부하는가? MXD2R-01·02를 닫을 수 있는가?
2. CRLF 파일에 LF 메타를 붙인 경우는 실제 바이트 SHA로, 정확한 CRLF 메타를 붙인 경우는 LF-only 사유로 거부하는가? 정상 LF는 보존되는가? MXD2R-03을 닫을 수 있는가?
3. MXD2R-04의 생성기 꼴 제한과 neighbor skin 후속이 같은 부류의 공백을 닫는가? 메타를 함께 고친 공통 변조·문자/표기·NaN/inf/빈값/중복/공백을 더 공격하고, 정상 48조합·옵션·skin 양성 및 약화/강화 변이를 직접 확인해 달라.
4. 위 네 항목별 **CLOSED / PARTIAL / OPEN**과 남은 반례·한정을 적어 달라. 모두 닫히더라도 결론은 MXD2-01의 **D2 개발 소비자 하위 범위**에만 한정되는가? 새 S1이나 실제 실행 승인을 발행하지 않는다.

## 3. 읽을 파일 · 재현

- 지난 외부 판정: `docs/reviews/codex_mixer_d2_review_20261027/codex_review_mixer_d2_20261027.md` (HOLD) 및 그 `d2/evidence/cases/` 원본.
- 기존 수정 증거: `docs/reviews/mxd2r_fix_evidence_20261103/README.md`, `docs/reviews/mxd2r_fix_evidence_20261103/mxd2r04/README.md` §9, `mxd2r04/q4_skin/`, 두 `SHA256SUMS`.
- **이번 재실행·수치·명령·환경·소스 해시·사전 공격 ①②④ 대조:** `docs/reviews/mxd2r_recheck_evidence_20261104/README.md`와 `docs/reviews/mxd2r_recheck_evidence_20261104/current/run_summary.json`.
- 코드: `scripts/mixer_deck_readback.py`, `scripts/mixer_deck_diff.py`, `scripts/mixer_smoke_blind.py`, `scripts/test_mixer_d2_consumers.py`; 변경 전체는 새 증거의 `consumer_changes.patch`, 커밋 목록은 `relevant_commits.txt`.

**한정:** 뜻이 같아도 표기가 다르면 거부한다 (생성기 꼴 엄격). 토큰 사이 ASCII 공백·빈 줄·주석 내용은 허용 범위가 있다. 생성기 식·상수 사본의 양성 대조이지 범용 LIGGGHTS 파서 증명이 아니다. LIGGGHTS 실행·Windows·Python 3.8 실행은 확인하지 않았다. 전체 게이트와 과거 55/55 변이를 이번의 새 실행 실적으로 합산하지 않는다. 실행 경계나 실패 사유가 다르면 종결 전에 그 반례를 보고해 달라.
