# 86차 독립 검토 — G85-N1 종결 · 라운드 2a 수용

2026-10-01. 판정: **ACCEPTED_ROUND2A_CLOSED_NO_EXECUTION_GO**.

G85-N1의 구성원 독립 결속 누락은 제출된 코드와 회귀/원문 로그 범위에서 닫혔다. 85차의 나머지 수용 항목과 합쳐 **라운드 2a를 종결 수용**한다. 새 차단 P1/P2는 발견하지 않았다. C1은 주장 범위를 좁히는 비차단 기록 사항이다. 최종 회귀 원문에 관한 C2는 검토 도중 받은 보충 커밋으로 해소했다. 같은 계산이나 전체 시험을 다시 돌릴 필요는 없다.

**2b·p_ini 구현·새 연구 leg·실행 GO·class 변경·투영 게시·복원은 승인하지 않는다.** 76차·라운드 1 종결과 grid_fit_v5 진단 전용 상태를 유지한다.

## 1. 고정 식별 및 직접 확인 범위

| 항목 | 확인 |
|---|---|
| 요청문 HEAD | `27bfeed68ea516e5c5a50f2475c8cc2b4f80ff3b` |
| 판정 코드 | `b4876b0b2098c9e87630fc715b44ab65336b73a2` |
| 생산 변경 | `19bf1c15`의 `src/io.py` +77/−2만. 58개 RUN_SCOPE 파일의 Git blob 및 4개 디렉터리 tree를 대조 |
| source_digest | 수신자가 파일 경로·실제 바이트로 재계산: `f1f4378f46610f08` |
| 계보 | GREEN→판정 코드, 판정 코드→요청 HEAD의 RUN_SCOPE diff 0 |
| 수신 검사 | 자체 바이트·AST·로그 데이터 검사 228건 + 보충 대조 45건 = 273건 통과. 제품 기능 시험 수가 아님 |
| 원문 로그 | 최초 12개 + 후속 5개, 총 17개 payload의 크기와 전체 SHA-256 일치. 두 세대 README도 Git blob 확인 |
| 보존 | 직전 현지 Gate85 검토 파일의 전후 SHA 동일. 원격 작업 트리/전체 PC의 직접 보존 관측 아님 |

기존 검토와 동일하게 **수신 소스 import/실행, pytest, 변이, restore, 영수증 재생성, COMSOL은 0회**다. GitHub의 고정 커밋을 읽었고, 자체 검사기는 받은 코드를 AST/문자열과 데이터로만 읽었다. 검사 자료는 `SOURCE_IDENTITIES.json`, `STATIC_AUDIT.json`, `LOG_AUDIT.json`, `PRODUCTION.diff`, `SUPPLEMENT_AUDIT.json`에 남겼다. `LOG_AUDIT.json`은 보충 전 관측이며, 마지막 회귀에 대한 최신 상태는 `SUPPLEMENT_AUDIT.json`이다.

근거: [고정 요청문](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/27bfeed68ea516e5c5a50f2475c8cc2b4f80ff3b/degradation-degeneracy/docs/22p_gap/GATE86_REQUEST.md), [고정 src/io.py](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/27bfeed68ea516e5c5a50f2475c8cc2b4f80ff3b/degradation-degeneracy/src/io.py#L1806).

## 2. Q1 — G85-N1 종결 수용

기존 결함은 목록과 두 digest를 함께 바꾸면, 선택한 스냅샷만 재해시하는 검사가 자기일관성을 그대로 받아들이는 것이었다. 이번에는 판단의 출발점이 달라졌다.

1. `base_config_closure_members`(:1806–1859)는 `run_spec.base_config`에서 시작한다. 제출된 `base_config_closure_keys`는 함수 입력이 아니다.
2. 각 논리 키의 봉인 스냅샷 YAML에서 `extends`를 읽고 posix 정규화·부모 기준 결합으로 다음 키를 유도한다. 순환·저장소 밖·깊이·봉인/스냅샷 부재·문서 형식·extends 타입을 거부한다. 현재 디스크의 config를 찾는 fallback 호출은 없다.
3. 호출부(:2023–2034)는 기록된 목록의 중복과 유도 집합 대비 누락/추가를 이름으로 거부한다. 목록은 증거에 대한 주장이지 정답이 아니다.
4. closure digest 재료는 `members`(:2036)이며, 그 스냅샷의 실제 SHA를 만든 뒤 기존 run_spec/계획 두 값과 비교한다(:2042–2048).
5. 입력 스냅샷의 봉인 SHA 대조와 시작/spec/종료 봉인 교차 검사는 기존 전체 validator에 남아 있다. 새 helper 하나만을 완전한 봉인 검증기로 부르지는 않는다.

AST 대조에서 기존 함수 중 본문이 달라진 것은 `_stage3_checks` 하나이고 추가 함수는 `base_config_closure_members` 하나다. `src/fitting.py`, 수치 함수, v5 경로, 시작 전 검사, tools/configs/scripts 등 나머지 생산 바이트는 불변이다.

### 회귀가 겨냥한 경계

`tests/test_gate85_closure_members.py`는 실제 leaf→parent v6 시험 산출에서 목록·두 digest·계획 사슬뿐 아니라 `run_signature`, fits 행 `run_sig`, fits 봉인까지 맞춘다. `_only_this_check_fails`는 전체 `validate_provenance`를 호출하고 실패 목록이 정확히 `[base_config_결속]`임을 요구한다. 따라서 다른 서명 검사에 먼저 걸려 성공처럼 보이는 시험과 구분된다.

원문 RED에서는 네 위조가 실제로 `fail=[]`이어서 assertion에 실패한다. 새 helper 부재의 m05 AttributeError는 실제 결함 RED로 세지 않는다. GREEN 23 passed 로그는 이 네 음성과 두 양성, 경계 시험을 포함한 gate85+gate84 집합이다. 새 변이 7개의 preimage가 현 코드에 각각 한 번인 것은 수신자 정적 확인, 7/7 kill 및 전체 352/352는 제출자 원문 로그 확인이며 독립 재실행은 아니다.

`m05`의 직접 경계 사례는 순환·미봉인 부모·없는 스냅샷·밖 경로·비문자열 extends·없는 root다. 깊이 32, 잘못된 YAML/mapping/UTF-8 처리는 코드상 확인했지만 각각 별도 실행한 회귀로 확대하지 않는다. 고정 §12-3의 요구와 핵심 위조 네 건은 충족하므로 이를 새 차단 항목으로 만들지 않는다.

첫 RED는 동일 파일 `tee`로 덮였다는 README 고지를 유지한다. 보존된 것은 두 번째 RED이며 첫 호출 전체 원문까지 보존됐다고 쓰지 않는다.

## 3. Q2 — 라운드 2a 종결

85차에서 보류한 마지막 P1이 위 범위에서 해소됐다. G84-N1의 사후 구성원 부분까지 수용하며, 이미 수용한 G84-N3·N4·R2-e·R2-f를 다시 열지 않는다. **2a 종결은 2b 구현 허가나 연구 실행 GO가 아니다.**

다음은 2b의 별도 범위/승인 절차다. R2-a 실물 v6 leg gate, R2-c 세대표, G84-N2의 v5 preimage 불변·v6 명시 분기를 한정해 제시할 수 있으나, 이번 회신만으로 구현·등록·새 leg를 시작하지 않는다.

## 4. Q3 — 탐침 기록과 c/d/e

### C1 (비차단): §6-b의 “영향 없음”은 좁혀 기록

사본은 240 bytes, SHA-256 `050a719e1b7baee3f0b1b2cd7fa6d2b7bf90a1f9edaf46bf82940b9e9d3ab0a0`이며 `execution_class=canonical`, `sealed=true`, `leg=L phase=grid`를 담는다. 즉 단순 로그가 아니라 운영 등록부의 실질적인 등록 기록이었다. `tools/preserve.py`의 reader는 Git 추적 여부가 아니라 파일 내용으로 등록을 읽으므로 **미커밋이라는 이유만으로 당시 영향이 없었다고 할 수 없다.**

제출 고정 커밋의 승인→HEAD diff에는 운영 `_exec_class`, `_claims`, `COHORT_LIFECYCLE.jsonl` 변경이 없다. 역사 두 leg의 producer/bundle/outputs/restore 내용도 영수증 대조에서 유지된다. 따라서 **현재 제출 자료에서 기존 수치/판정을 뒤집을 근거는 발견하지 않았으며, 2a 종결을 재차 막지는 않는다.**

다만 원격 당시 `find -newermt` 출력, 삭제 작업 원문, local 항목의 전후 전체 집합을 수신자가 직접 관측한 것은 아니다. mtime 창 관측도 독립적인 모든 파일 바이트 불변 증명은 아니다. 권고 기록 문구:

> pytest 밖 production 탐침이 운영 등록부에 일시적인 canonical 기록 1개를 남긴 격리 절차 이탈이 있었다. 원문 사본 보존 후 제거했다고 보고했으며, 제출된 고정 이력과 영수증 범위에서는 기존 판정/산출의 오염이 확인되지 않았다. 당시 원격 전체 상태의 무영향까지 입증한 것은 아니다. 이후 production 탐침은 pytest의 시험 authority 또는 격리된 git archive 사본에서만 수행한다.

이 회신은 과거 삭제를 새로 승인하거나 현재 local 기록을 정리하라는 지시가 아니다. 새 연구 leg 0과 작은 회귀/탐침 실행 0은 다른 주장이다.

### §6-c / d / e

- **c 수용:** helper가 먼저 보는 스냅샷 부재의 루프 내 방어를 남겨도 허용을 넓히지 않는다. 별도 동적 도달·변이 증거로 세지 않는 전제다. 파일이 두 확인 사이 사라질 가능성까지 없다는 의미의 “영구 불도달”로 일반화하지 않는다.
- **d 수용:** 키 목록을 기록하되 독립 유도 결과와 대조하는 것은 설명 가능한 설계다. 형식 변경이나 삭제가 필요하지 않다.
- **e 한정 수용:** basename `configs/` fallback을 재현하지 않는 것은 현재 지원 경로에서 fail-closed인 더 좁은 계약이다. “모든 load_config 경로와 동등”이 아니라 “정규화된 봉인 closure만 지원, fallback 필요 경로는 거부”로 표현한다. 향후 해당 경로가 필요하면 별도 결정 대상이며 live fallback을 이번에 추가하지 않는다.

## 5. Q4 — 새 세대 영수증 한정 수용

이전 두 영수증의 history 바이트는 수신자 보유 Gate85 원문과 완전히 같다. 새 core 텍스트에서 validator identity 두 필드를 빼면 나머지가 같고, 검사 수 35/34, producer/bundle/outputs/restore가 유지된다. 전체 파일 diff에는 이에 따른 core_sha256 및 stamp commit/time 변경도 포함된다.

| leg | 새 선언 core SHA-256 | stamp dirty |
|---|---|---|
| paired_fixed5_v4 | `adf0ce1fff69f7b36d955234b3eb16be3235e165b7a1512255bc377d32ed0fdc` | false |
| grid_fit_v5 | `01bd53eb85b6c1cf6753d40dfd6bac9ef5eb965922f0148968b158083e3e3463` | true |

원장에 각 core와 `f1f4378f46610f08` 앵커가 연결돼 있다. clean 시작과 두 번째 영수증 기록 당시 dirty stamp를 혼동하지 않는다. 이 수용은 기존 정확 바이트·core 텍스트·원장 결속의 대조다. 수신자가 YAML canonical core hash를 재생성하거나 bundle restore/재채점을 실행한 것은 아니다. 역사 v5 두 leg의 영수증을 새 v6 검사의 기능 시험으로 읽지 않는다.

## 6. C2 해소 — 최종 실행 원문 보충과 출처 구분

| 근거 | 수신 확인 수준 |
|---|---|
| 0be169b1 전체 pytest | 원문 1 failed / 2045 passed / 1 xfailed, rc1. 증인 형식 실패이며 숨기지 않음 |
| 같은 러너 smoke | 원문 및 부모 기록 rc0, 184초 |
| 같은 러너 전체 변이 | 원문 줄머리 집계 352 hit / 0 survivor / 0 error. 별도 신고 11개는 실행 352개와 구분 |
| b4876b0b 증인 정정 | clean 시작/끝, gate67 17 passed 및 해당 변이 1회 rc0 원문 확인 |
| 요청문 HEAD 27bfeed6 | 후속 보존 커밋 `92c50f9035db79143f7f5aca65072b3adffdee26`에서 원문 확인. pytest 2046 passed / 1 xfailed, rc0, 3543.27초; smoke rc0, 168초 |

보충은 evidence/README와 5개 기록만 추가하며 RUN_SCOPE 변경 0이다. 부모 로그의 시작/끝 HEAD는 모두 `27bfeed6`, status 0, 22:38:32Z→23:40:38Z다. pytest 전문에는 예상 xfail의 node 이름도 있다. 각 파일 전체 SHA가 보충 README와 일치하고 기존 12개 식별은 유지된다. 따라서 마지막 전체 회귀 수치는 이제 단순 발송문 보고가 아니라 **제출자 원문 확인**으로 올린다. [최종 부모 로그](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/92c50f9035db79143f7f5aca65072b3adffdee26/degradation-degeneracy/docs/22p_gap/gate86_evidence/request_commit_27bfeed6/g86_send.log).

22:32:40Z에 시작한 첫 시도는 시작 줄 하나만 보존됐다. 컨테이너 재시작이 원인이라는 설명은 제출자 보고이며, 부분 pytest stdout은 두 번째 실행이 덮어 미보존이다. 그 첫 시도를 PASS나 0회로 바꾸지 않는다. 앞선 첫 RED 원문 미보존과도 별개의 사건이다.

“최종 HEAD에서 수신자가 전체 pytest/352 변이를 다시 실행해 통과”라고 쓰지는 않는다. 전체 변이 352/352는 `0be169b1`, 증인 정정 한정 재생은 `b4876b0b`, 최종 전체 pytest/smoke는 `27bfeed6`의 기록이다. 이번 원문 보충으로 C2의 자료 요청은 닫혔으며, 추가 실행이나 자료 재생성을 요구하지 않는다.

## 7. 다음 전달 문구

`CLAUDE_REPLY.md`를 전달하면 된다. 운영 등록부 탐침 문구를 위 범위로 정정하고, 기존 실패·덮인 RED의 한계·dirty stamp를 그대로 보존한다. 다음 라운드는 별도 사용자 승인 아래 진행하며, 이번 검토에서 원본이나 운영 상태를 수정하지 않았다.
