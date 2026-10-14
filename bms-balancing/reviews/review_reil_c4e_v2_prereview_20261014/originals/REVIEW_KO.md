# REIL C4E v2 사전 재검토 회신

2026-10-14. 판정은 **REQUEST_REVISION_BEFORE_E0_APPROVAL**이다. 성공 정의와 입력 결속의 주요 정정은 수용한다. E0 승인 전 남은 것은 회귀시험 권한표의 계수 단위, 마지막 쓰기까지의 예산 판정, 중지 후 완료 메시지 수신의 세 문서 경계다. 기존 기능 검증을 다시 요구하거나 E0 구현을 시작하라는 회신이 아니다.

## 검토 기준과 식별

저장소 `yonghoon7153-source/Yonghoon-DEM-DFT`, 브랜치 `claude/14-gate-code-review-9qkx05`의 검토 HEAD는 `dc6e5b7e043ff11b73095ddb9d60db7837e665c7`로 고정했다. 두 첨부는 이 커밋의 파일과 바이트가 같다.

| 첨부 | 바이트 | SHA-256 |
|---|---:|---|
| 승인 요청 v2 | 35,172 | `a4fb202549e6f785080c0e0feab09f930a2f0afd288cb3a3e5005096dd6d8e28` |
| 발송문 v2 | 4,272 | `56644c3888f7345c26cf41a3a4177d55305d47591a2b5c0de123f3df39991f68` |

좌표는 [승인 요청 v2 원문](C:/Users/Administrator/Downloads/REIL_C4E_APPROVAL_REQUEST_v2_20261014.md)의 1부터 시작하는 행 번호다. 이전 검토 HEAD `89d18f546cef0172ee53105ae04ba66d1e224370`에서 5커밋의 완전 비교를 확인했다. 생산 소스와 기존 시험 일곱은 불변이며, h/hb는 이번 HEAD에서 직접 읽어 이전 참조 사본과도 일치했다. `STATIC_AUDIT.json`에 현재 자료 5개와 재사용 식별 자료 25개의 바이트 결속을 구분했다.

## 질문에 대한 답

| 질문 | 답 |
|---|---|
| Q1 지금 E0 승인 가능한가 | 아직 세 문서 경계를 보완해야 한다. 정정본 재검토 후 사용자 E0 승인, E0 결과 검토 후 사용자 E1 별도 GO 순서는 적절하다. |
| Q2 계산 예외표가 충분한가 | 예외 범주·이번 GREEN 1회·환경 변수·실패 중지는 반영됐다. 다만 실제 fork 집계, COBYQA 내부/독립 평가 구분, 보존 util의 “몇 회”를 정정해야 한다. |
| Q3 두 계측 구간과 늦은 완료 처리는 맞는가 | 서로 다른 두 관측 구간임을 명시한 정책은 수용한다. 마지막 drain에서 도착한 done의 상태와 초과 목록까지 보존하도록 보완해야 한다. |
| Q4 COMPLETE 여섯 조건이 권장과 같은가 | 66 returned와 운영 조건의 논리는 일치한다. 그러나 현재 순서의 final_record는 그 뒤 끝 재해시·끝 기록을 포괄하지 않아 최종 기록 수용 경계는 아직 같지 않다. |

## 닫을 수 있는 정정

| 이전 지적 | 문서상 판정 | 근거 |
|---|---|---|
| C4E-N1 권한 분리와 시험 환경 | 부분 닫힘 | 270–299, 343행. 기존 승인의 자동 재사용을 부정하고 이번 GREEN 예외를 새로 묻는다. `03_green.nsga2_synthetic_outcome.json`의 부재 확인·보존과 E1 별도 승인이 명확하다. |
| C4E-N2 관측 완료와 E3a 성공 | 닫힘 | 185, 208–218행. 지역 오류는 완료 관측 행으로 남을 수 있으나 E3a는 INCOMPLETE이며 C4-A 관문은 false다. 66 returned에도 전역 중지·구조·작업자·기록·식별 조건을 모두 요구한다. |
| C4E-N3 좌표와 비용 규칙 | 대부분 닫힘 | 85–91, 132–169행. 공통 run 원점, 두 계측 구간, 엄격한 초과, 표본 감시 한계, 유효성 검사, 최소 8개 통계, progress 진입 proxy, 원시 판정 근거, 정리 reserve를 명시했다. |
| C4E-N4 NE와 실제 소비 입력 | 닫힘 | 114–119, 189–204, 244–248행. reference 둘, NE 최대, 네 배열의 순서·slice·배율, 실제 Model/halfcell digest와 기대/시작/끝 식별이 연결된다. 구현 수용 때 d_3는 실제 소비 객체를 검사해야 한다. |
| M1 바이트 관계와 인용 | 닫힘 | 원본 33,754 B의 CRLF 정규화와 끝 LF 추가로 사본 32,909 B가 되는 관계, 원본 선호 이유 축소, v2 §6-3 인용이 정정됐다. |

이는 문서 조건의 닫힘이다. E0 기능 PASS, C4 전체 7-1/7-2 닫힘, E1 또는 C4-A/B 실행 승인으로 확대하지 않는다. 수렴·feasible·success=True를 E3a의 추가 성공 조건으로 만들지 않은 것도 적절하다.

## C4E N1 잔여 회귀시험 계수 단위

우선순위 P2. 요청문 289–293행과 발송문 예외표 요약을 함께 정정한다.

1. **실제 fork는 기존 10세션이며 신규 5를 더하면 15다.** 문서의 11/16은 모사 Process와 두 파의 실제 실행을 혼합한 숫자다. 0a 3 + 0a 보완 1 + 0b1 보완 3 + 보완2 1 + 0b2 2 = 10이다. 0a 보완 n3_a/n3_b는 `_ScriptedCtx`가 Process를 대체하므로 실제 fork 0이고, 0b2 c_8은 두 파에서 각각 supervise_runner를 호출하므로 2다. 기존 GREEN 상한 17은 충분하므로 늘릴 이유가 없다.
2. **COBYQA 14회는 맞지만 50은 내부 목적평가 상한이다.** 정상 반환 뒤 독립 재평가가 최대 1회 더 있다. “실행당 내부 목적평가 ≤50, 정상 반환 뒤 독립 재평가 ≤1”로 구분한다. 14×50은 내부의 보수 상한이며 전체 목적 호출 상한이라고 부르지 않는다.
3. **“≤120 평가 + test_06의 몇 회”는 단위와 유한 상한이 닫히지 않는다.** 고정 소스의 보수 상한을 아래처럼 쓸 수 있다. 중첩 함수 진입을 별도로 세므로 이를 독립 optimizer 평가 수로 더하지 않는다.

| 비최적화 합성 경로 | extract_battery_data | objective_fun | dVdQ_hc | optimizer |
|---|---:|---:|---:|---:|
| 0b1 test_06 | ≤5 | ≤3 | ≤9 | 0 |
| 0b2 h_1–h_4 | ≤4 | 0 | ≤48 | 0 |

후자의 기존 ≤120을 보수 상한으로 유지할 수 있지만 무엇을 세는지 적어야 한다. 위 수는 관측 결과가 아닌 소스의 유한 루프·호출 경로 상한이다. 가짜 minimize ≤995 = 8+4+982+1은 정적 상한으로 수용한다. Sobol 관련 15는 현재처럼 “시험” 수로 수용하며 생성 함수 15회라는 뜻으로 바꾸지 않는다.

근거: [0a 보완 시험](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/reil_c4e_v2_prereview_20261014/source/tests/test_reil_c4_0a_fix.py:176) 176–177, 219–235행; [0b2 시험](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/reil_c4e_v2_prereview_20261014/source/tests/test_reil_c4_0b2.py:774) 774–779행; [h/hb 연결 소스](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/reil_c4e_v2_prereview_20261014/source/scripts/reil_c4_hb.py:1074) 1074–1078, 1105, 1165행. 내부/독립 평가는 [h 소스](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/reil_c4e_v2_prereview_20261014/source/scripts/reil_c4_h.py:773) 781, 840–841, 875행이다. util 상한은 0b1 시험 260–313, 0b2 시험 523–571, h 467–471/518–560, hb 640–695, c5 256–259행을 연결한 것이다.

## C4E N2 잔여 마지막 쓰기 뒤의 수용 판정

우선순위 P2. 요청문 111–112, 133–136, 174, 214–215, 251행.

순서는 `final_record → 끝 sha → 판정 → 끝 기록`인데, final_record는 자신의 parts 쓰기·재읽기·해시·용량 조회 뒤 한 번만 시간과 크기를 판정한다. 그 뒤 새로 쓰는 끝 기록까지 검사했다고 할 수 없다. [monitor 원문](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/reil_c4e_v2_prereview_20261014/source/scripts/reil_c4_monitor.py:344) 344–379행이 이 경계다.

실행 없는 상수 반례: 최초 검사에서 산출이 1 GiB−100 B이면 통과한다. 뒤의 끝 기록이 1,024 B이면 실제 합은 상한보다 924 B 크다. 기존 final_record 반환은 여전히 COMPLETE/위반 없음이고 끝 sha도 같을 수 있어, 여섯 조건만으로는 이 마지막 크기 초과를 거르지 못한다. 끝 재해시와 쓰기가 지연되는 시간 경계도 동일하다.

정정은 끝 식별과 모든 단계 내 끝 기록의 저장·재읽기를 포함한 뒤 **같은 산출 루트의 크기와 최종 monotonic snapshot으로 수용을 확정**하는 것이다. 9,900초 기록 마감과 10,800초 단계 끝이 각각 어느 마지막 작업까지 적용되는지도 고정한다. 끝 재해시·끝 기록을 먼저 포함해 마지막 final_record로 닫거나, 명시적인 후속 종결 검사를 두는 방식 모두 가능하다. 초과·쓰기·재읽기·식별 실패이면 이전 COMPLETE를 확정하지 않고 INCOMPLETE/C4-A=false로 남긴다.

자기 자신의 미래 저장·도구 반환까지 재귀적으로 측정할 필요는 없다. 유한한 마지막 저장·재읽기·해시·크기 확인 뒤 snapshot과 그 이후 stdout/외부 반환을 구분하면 된다. 후속 기록은 그 snapshot에 포함됐다고 하지 않는다.

s_3에는 record_state를 인위적으로 넘기는 경우뿐 아니라 **끝 재해시 지연 및 끝 기록 추가로 시간/크기가 초과하는 종결 경로**를 명시한다. 66 returned이지만 global_stop/freshness만 실패한 운영 음성도 같은 ID의 하위 사례로 적을 수 있다. 21 ID를 자동으로 늘리라는 요구는 아니다.

## C4E N3 잔여 중지 뒤 도착한 완료 행

우선순위 P2. 요청문 144–145, 216, 241행.

144행은 active 초과가 보이면 곧바로 그 호출을 STARTED_INTERRUPTED로 확정한다. 하지만 기존 monitor는 중지·정리 뒤 마지막 drain을 수행하며, done이 있으면 COMPLETED 원행을 우선한다. [상태 집계](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/reil_c4e_v2_prereview_20261014/source/scripts/reil_c4_monitor.py:194) 194–199행과 중지·마지막 drain 313–335행을 함께 보아야 한다.

정적 경합 예: 부모가 active 1,800.01초를 관측해 중지를 요청한 직후 worker가 반환하고, 마지막 drain에서 done이 수신된다. 이 행은 COMPLETED다. 감지 순간 active였다는 이유로 원행을 지우면 216행과도 충돌한다.

active 초과는 우선 “중단 요청 대상”으로 기록하고, 최종 drain 뒤 done이 없을 때만 STARTED_INTERRUPTED로 둔다. done이 있으면 원래 COMPLETED 및 termination을 보존한다. returned뿐 아니라 error 반환도 보존하며, active 초과 감지와 global_stop은 취소하지 않는다. 마지막 drain에서 새로 받은 완료 행의 wall도 대조하여 늦은 완료 초과 목록을 완성한다.

이 경합에서도 global_stop이 남으므로 E3a는 INCOMPLETE다. **새 성공 판정 우회가 아니라 원행과 초과 증거를 보존하는 명세 충돌**이다. r_6의 현재 “계속 active”와 “다음 tick 전에 이미 done” 외에 “active 초과 → 중지 요청 → 마지막 drain에서만 done 수신”을 추가한다. 순수 집계 fixture로 고정할지 추가 fork로 고정할지 택하고 횟수를 맞춘다. 추가 fork를 택해도 새 6/전체 16으로 기존 상한 안이며, 이는 실행 허가가 아니다.

## 다음 순서

요청문과 발송문만 위 세 항목에 맞게 정정하여 재검토받는다. 후보 구현, 기존 시험 재실행, 과거 관측 보충은 이번 회신의 요구가 아니다. 정정 수용 뒤 사용자가 E0를 명시 승인하며, E0 결과 수용 뒤 E1을 별도 승인한다.

검토자는 문서·JSON·소스 텍스트·바이트 해시·상수 산술과 자체 PowerShell 자료 도구만 사용했다. 받은 코드 import/호출, 기능 시험, Python/optimizer/Sobol, xlsx/pickle/노트북 반입·개봉, COMSOL/JVM/compile/solve, 설치·환경 재구축은 0회다. 원 요청문과 저장소 생산 소스를 수정하거나 외부에 회신을 발송하지 않았다.
