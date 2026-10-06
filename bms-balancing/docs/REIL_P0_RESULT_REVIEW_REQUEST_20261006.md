# REIL 외부 검증 — P0 결과 수용 — Codex 검토 요청 (문서 · 결과 · 좁은 정적 코드 열람 · 실행 0 · 게이트 차수 밖)

> 첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.
> REIL 자료 (`LFP_Data.xlsx` · `results/*.pkl`) · 노트북을 열지 마시고, 맞춤 · 계산 · 설치 · 환경 재구축 · 시험 실행도 하지 마세요.
> 이 요청은 비용 측정 (C5) · 맞춤 · E3a / E3b · 실행의 승인 요청이 아닙니다.

C6 보충 검토 회신 (`prereview_reil_v2_c6_supplement_20261006` — C6 사전 준비 종결 · 다음 = P0 의 범위 · 예산 · 중단 조건 별도 승인) 뒤의 일입니다.
사용자가 P0 를 승인했고 (§17), 환경 단계에서 미리 정한 중단 조건에 한 번 걸려 멈췄다가 (§18) 사용자 결정 (가) 로 허용 차이 한 줄을 보완해 (§19) P0 를
**한 번** 실행했습니다 (§20 · rc 0). 이 요청은 그 결과와 실행 중 내린 결정을 확인받는 것입니다. 작성 2026-10-06. 발송은 사용자 · 발송문 (고정 커밋
SHA 포함) 은 저장소 밖.

## 대상

| 항목 | 값 |
|---|---|
| **확인 대상** | 이 요청문이 든 커밋의 바이트 (SHA 는 발송문에) |
| 승인 요청문 (범위 · 예산 · 중단 조건 · 보존) | `bms-balancing/docs/REIL_P0_APPROVAL_REQUEST_20261006.md` (커밋 `694db0673`) |
| 승인 · 진행 기록 | `bms-balancing/docs/REIL_PREREQUISITES_STATUS_20261004.md` §16 (초안) · §17 (사용자 승인) · §18 (§6-1 정지) · §19 (사용자 결정 (가)) · **§20 (결과)** |
| **결과 정본** | `bms-balancing/evidence/reil_p0_20261006/P0_RESULT.json` (sha256 `3875e65092b38c9b08c907926bd8d1f4ee25674c97c28b5ada935e9027d12a90` · blob `2aa50f0b…`) |
| 사람용 raw | `wiki/raw/repositories/2026-10-06-reil-p0.md` (결과 JSON 에서 기계로 뽑은 사본) |
| 원문 로그 | `bms-balancing/evidence/reil_p0_20261006/` 01–13 (설치 · emit · check · 옛 봉인 대조 · 변이 증명 · RED / GREEN · bms 전체 · 식별 · 정적 열람 · 실행 meta / stdout / stderr · 수 정정) |
| 환경 봉인 | 새 봉인 `bms-balancing/reil_c6_rebuild_20261006/` (MANIFEST sha256 `a14617ec…`) · 옛 봉인 `reil_c6_20261005/` 은 바이트 그대로 |
| P0 스크립트 · 시험 | `bms-balancing/scripts/reil_p0.py` (sha256 `793b326e…` · blob `b7ef272f…` · 마지막 변경 `ac62645dc` = 실행에 쓴 판) · `bms-balancing/tests/test_reil_p0.py` (blob `7af83d88…`) |
| 기준 문서 | v2 §1-3 · §1-5 · §3 · §4-2 · 부속 A §2-5 · §5-1–§5-4 · 부속 C §4 · 부속 D §3 |

## 정적 열람 허용 (이번 요청에 한해 · 읽기만 · 실행 · import 금지)

| 파일 | 줄 | 무엇 |
|---|---|---|
| `bms-balancing/scripts/reil_p0.py` | 1–432 | 판정 함수 (`prior_compat` 91 · `sigma_v` 120 · `cycle_state` 142 · `direction_state` 166 · `util_static_check` 185 · `_notebook_check` 217 · `_raw_entry` 268) · 실행 흐름 `run` 307 |
| `bms-balancing/tests/test_reil_p0.py` | 1–244 | 합성 시험 37 (부속 A §5-1–§5-3 의 분수 경계표가 기대값) |
| `bms-balancing/reil_c6_rebuild_20261006/REIL_C6.lock.txt` · `bms-balancing/evidence/reil_p0_20261006/04_seal_compare.txt` | 전부 | 옛 봉인과의 차이 |

## 결과 요지 (정본은 결과 JSON · 사본은 상태 §20)

| 출력 | 결과 |
|---|---|
| 식별 | xlsx (10,841,377 B · `fd50e095…`) · `util_LFP.py` (`3c19e45e…`) · 노트북 (4,134,001 B · `388f2a6f…`) **셋 다 기대값과 일치** · 노트북 셀 3 · 4 · 6 · 8 · 9 · 11 원문 = 검토 발췌 · 상수 (시트 · `cell_idx` · `step_idx` · `theoretical` · 장전량 · 지름 · 인자) 전부 일치 · 시트 19 개 = 부속 D §3-3 집합 |
| max_q | **3.149013767655145** (정확 유리수 886368576912267/281474976710656) · 노트북 셀 6 그대로 (`LFP_data[1]` · `[argmin:argmax]` · `/ LFP_mass_12 × 20.16`) + util 718–719 `np.max` · q_PE_hc 1313 점 |
| 추출 기록 | 입력 13 모두 그들 함수로 성공 (UNFIT 0) · 점 수 · 끝점 전압 · 버린 열 · NaN 분절 · 우리 재계산 배열 = 그들 출력 13 / 13 |
| σ̂_v | 11 셀 모두 OK · 0.000315 – 0.00128 V |
| 사전 양립성 | 99 칸 = PRIOR_COMPATIBLE 83 · PRIOR_INCOMPATIBLE 16 · P0_UNFIT 0. 배제: #0 · #4 · #5 (τ 0 · A0 · A1) · #3 (τ 전부 · A0 · A1) · #2 · #8 (τ 0 · 0.02 · A0). 부속 A §5-1 · §5-2 · §5-3 의 분수 경계표와 그대로 맞는다 (max_q 3.149… > 25/8) |
| 대응표 | 13 입력의 원래 열 머리에 cycle · step · 모드 · 전류 열이 **없다** → cycle · 방향 · 종합 13 / 13 `판정 불가` |
| 밖 6 시트 | 이름 · 열 머리 · 행 수만 |
| 실행 | 2026-10-06T08:02:41Z → 08:03:09Z · rc 0 · 맞춤 · 목적함수 · 최적화 호출 0 · 시도 한 번 |

## 확인받을 결정 · 공개 사항

1. **환경 허용 차이 보완 (사용자 결정 (가) · §18 · §19).** 새 venv 의 lock 이 옛 봉인과 RECORD sha 4 개 (cffi · fonttools · numpy · pip) 에서 달랐고,
   승인 요청문 §2-4 의 "RECORD 가 하나라도 다르면 멈춤" 에 걸려 자료를 열기 전에 멈췄습니다. 그 넷은 30 배포판 중 RECORD 에 `../../../bin/` 콘솔
   스크립트 항목이 있는 배포판과 정확히 같습니다 (스크립트 첫 줄 = venv 절대 경로 · 옛 venv 경로는 어디에도 남지 않음). 사용자가 보완 규칙 —
   (i) 차이 집합 = bin 항목 배포판 집합 (ii) Sobol 배열 6 · `SOBOL_PHASE_A.json` · `PROFILE.json` · `COBYQA_OPTIONS.json` 바이트 동일 (iii) 배포판 집합 · 판 ·
   `#@ files` 집계 동일 — 을 **자료를 열기 전에** 정했고 셋 다 충족했습니다. **한계:** 옛 RECORD 원문이 없어 네 배포판의 bin 밖 항목이 옛 설치와 같았는지는
   직접 대조하지 못했습니다. 새 봉인의 변이 증명 12 / 12 (rc 0).
2. **실행 전 점검에서 고친 규칙 하나.** 내려받은 `util_LFP.py` 최상위에 `ElementwiseProblem` 하위 클래스 셋 (594 · 616 · 637 줄 — 메서드 정의만) 이 있어
   제 AST 검사 (최상위 = import · 함수 정의 · 문서 문자열만) 가 이를 부작용 후보로 잡았습니다. 이대로면 실행이 §6-3 으로 멈추므로, **xlsx 를 열기 전에**
   RED 시험 1 (메서드 전용 클래스 허용 · 데코레이터 · 계산된 base · 본문 코드는 거부) → 규칙 수정 → GREEN 37 로 고쳤습니다 (`ac62645dc`). 위험 호출 grep
   (open · pickle load/dump · os · subprocess · socket · urllib · eval · exec · savefig · to_csv …) 0 · P0 가 부르는 세 함수 (`visualize_LFP_data` ·
   `extract_battery_data` · `filter_first_occurrences_by_column`) 는 전문 열람.
3. **제가 정한 구현 규칙 (자료를 열기 전에 시험으로 고정 — 부속 D 문장에 없는 세부):**
   - cycle 축: 원래 열 머리에 "cycle" 이 든 열이 **정확히 하나**이고 시트의 셀이 **하나**일 때만 선택 행에 결속해 일치 / 불일치를 판정 · 그 밖 (열 0 ·
     둘 이상 · 셀 둘 이상 · 비수치 · 결측) 은 `판정 불가`. 실제 자료에서는 cycle 열이 0 이라 이 세부가 결과를 정하지 않았습니다.
   - 방향 축: P0 입력에 장비 · 전지의 부호 규약 문서가 없으므로 raw (step / 모드 열 · 전류 부호) 만 적고 항상 `판정 불가`. 실제 자료에는 그런 열도 없습니다.
   - raw 칸의 행 범위는 그들 함수가 돌려주지 않아 같은 분절 규칙을 다시 계산했고, 그 배열이 그들 출력과 같은지 대조했습니다 (13 / 13 같음).
4. **기록 보존의 결함 (신고).** 첫 RED (모듈 부재로 수집 오류 · rc 2) 로그는 다음 RED (함수 껍데기 · 30 failed / 1 passed) 로 덮였고, `07_green.stdout.log`
   도 시험을 더할 때마다 덮어 마지막 판 (시스템 python · 35 passed / 1 skipped) 만 남았습니다. venv python 의 GREEN 은 `07_green_venv` (36) 와
   `11_green_venv` (37) 가 원문입니다. bms 전체는 583 passed · 1 failed (문서의 시험 수 줄) · 1 skipped (시스템 python 에 pymoo 없음) — 수를 586 으로
   고친 뒤 그 시험만 다시 돌려 통과했고 전체 재실행은 하지 않았습니다.
5. 실행 stderr 의 RuntimeWarning 은 그들 `extract_battery_data` 의 `np.gradient` (dQ/dV) 에서 나왔습니다 — P0 출력에 쓰지 않는 배열입니다.

## 묻는 것

1. P0 출력이 v2 §4-2 · 부속 A §2-5 · 부속 C §4 · 부속 D §3 의 출력 칸과 판정 규칙을 채우는가 — **C3 (P0 출력 고정) 을 수용**할 수 있는가.
2. 결정 1 (허용 차이 보완 · 새 봉인을 P0 기준으로) 을 수용할 수 있는가. 수용하지 않으면 무엇이 더 필요한가.
3. 결정 2 · 3 (AST 규칙 수정 · cycle 결속 규칙 · 방향 판정 불가) 이 승인 범위와 부속 D 의 뜻 안인가.
4. 대응표 13 / 13 `판정 불가` 가 C5 (비용 측정 · 부속 A §3-9) · E3a 승인 요청의 **제한 표기로 충분**한가, 아니면 그 전에 필요한 것이 있는가 (예: 저자 문서 ·
   C1-core 의 해당 절 · 자료 페이지 설명).
5. 다음 C5 승인 요청에 반드시 담아야 할 것 (셀 하나 · A0 · J_V · Phase A 128 실행 제안 · 예산 · 중단 조건 · 보존) 에 추가 조건이 있는가.

## 요청하지 않는 것

비용 측정 · 맞춤 · E3a / E3b · H1–H4 · Sobol 정식 봉인 · label seed · REIL 자료 · pickle · 노트북 열기 · 실행 · 설치 · 환경 재구축 · 시험 실행 ·
P0 재실행.
