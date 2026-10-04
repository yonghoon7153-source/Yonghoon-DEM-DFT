# 89차 게이트 독립 검토 결과

2026-10-04. **G88-N1 종결 수용, 단계 3 라운드 2b 종결 수용. 이번 범위의 새 차단 지적 없음. 실행 GO는 아니다.**

고정 커밋의 코드·회귀 소스·원문 로그·영수증을 읽고, 파일 해시와 AST를 독립 대조했다. 제출자의 시험을 검토자가 재실행한 것은 아니다. 87·88차에서 이미 수용한 부분 및 2a 종결을 유지한다.

## 고정 대상과 확인 범위

- 요청 커밋: 8113f12bd8f3e457670117ceef53501967e8594c.
- 코드 커밋: 26c11d6fc7feeb92bd68fce4c3972d849ada2774.
- 발송 후 docs-lint 원문 추가: 9fa175f3e7fb7c8dcdee46ce132d98b07bcdf563.
- 독립 재계산 source_digest: 803e2b7781cbc9cd.
- RUN_SCOPE 58개 파일의 경로 집합과 Git blob을 대조했다. 88차 대비 변경은 tools/preserve.py의 +4/-0뿐이며, 57개는 동일하다.
- 코드 커밋에서 요청 커밋까지 RUN_SCOPE diff 0. 동결 본진 e2f5697192b2008d0a11b7334c2d3f3546a85809의 후손임은 GitHub compare의 merge-base로 확인했다. 로컬 checkout이나 branch 전환은 하지 않았다.
- 고정 표 §15는 코드 변경 전 abf857752의 원문과 동일하다.

## G88 N1 판정

추가 호출은 tools/preserve.py:9146의 _assert_external_input_binding(_fit_ent.get("receipt") or {})다.

같은 함수의 snap(:9042) → phases(:9066) → fit entry(:9132) → receipt가 검사 대상이며, 그 snap의 receipt를 원장으로 옮긴다(:9180). 새 호출은 fit-only 분기(:9130), lifecycle lock(:9010), ledger lock(:9098) 안에 있다. 기존 세 digest 결속 비교(:9136–9142) 뒤이며 plan의 executed 전환(:9157), 원장 쓰기(:9210), claim 삭제(:9216)보다 앞이다.

호출한 공통 검사는 키 집합·hex64·입력 묶음 재계산을 검사하며, phase_done이 사용하는 함수와 같다. 새 함수나 두 번째 계산 공식은 없다. 추가 호출 하나를 제거한 전체 모듈 AST가 88차 모듈 AST와 같음을 독립 확인했다. 바뀐 최상위 함수는 finalize_leg 하나뿐이다.

따라서 기록 시점의 입력 검사를 통과한 뒤 durable claim의 inputs만 바뀌어 최종화되는 기존 빈틈은 이 고정 코드에서 닫혔다고 판정한다.

## 회귀와 기존 거부 이유

| 증거 | 확인한 내용 | 판정 |
|---|---|---|
| d01 | 실제 기록·재개·최종화를 거쳐 원장 receipt가 기록된 receipt와 같음을 검사 | 양성 대조 적합 |
| d02 네 경우 | inputs 삭제·다른 hex64·추가 키·비hex를 기록 뒤 변경, 실제 finalize_leg 호출, 이유와 원장·claim 바이트 불변 검사 | 잔여 결함을 직접 겨냥 |
| d03 | inputs와 package digest를 함께 바꾼 자기일관 위조를 기존 receipt 대 consumed 결속 비교가 거부 | 기존 검사 필요성 유지 |
| 88차 회귀 | 시험 소스 바이트 불변, f03_06 이유 단언과 v2 대조 유지, 제출 로그 24 passed | 기존 이유와 v2 수용 유지 |

원문 RED의 4 failed는 d02 네 건의 DID NOT RAISE이며 d01·d03은 처음부터 통과한다. GREEN은 새 모듈 6 passed다. 이 수치는 제출자 실행 로그의 확인 결과이지 검토자 실행 횟수가 아니다.

등록부에는 신규 두 시나리오와 사전 고지한 g88 증인 한 건 변경만 있다. g88 비교를 제거해도 새 검사가 다른 이유로 거부하는 현상을 이유 단언으로 잡고, d03은 새 검사를 통과하는 위조에서 기존 비교가 여전히 필요함을 별도로 고정한다. 같은 치환 지점의 g88·g89 두 시나리오를 서로 다른 독립 지점 둘로 세지 않는다.

## 원문 로그와 영수증

새로 수신한 29개 파일의 UTF-8 바이트를 Git blob과 대조했다. evidence README의 15개 로그는 크기·전체 SHA-256 모두 일치했다. README 표 밖의 발송 후 추가 로그 14번도 1,163 bytes, SHA-256 d7d276afe86dbb96d98671890d0f6ec47636069413d38baa64ad6948d226be95로 별도 확인했다.

| 원문 | 확인한 실행 기록 |
|---|---|
| 10번 | clean 66129fc6a, 2139 passed / 1 xfailed, pytest rc0 |
| 11번 | 같은 HEAD, strict smoke rc0 |
| 12번 | 같은 HEAD, 순차 전체 재생, 물었다 397줄 / 신고 11줄, ran397, rc0 |
| 14번 | 요청 HEAD 8113f12bd의 시작·끝 동일 및 dirty0, docs-lint 358 passed, rc0 |

397은 executable 시나리오 수다. scenario 전체 408, declared 11, site 전체 446과 구분한다. 1 xfailed는 기존 저장소 밖 입력 staging 미지원 사례이며 성공으로 합산하지 않는다. 13번으로 추가된 88차 발송 docs-lint 원문도 검증하여 이전의 제출자 보고 수준과 구분했다.

두 영수증의 history 사본은 88차 현행 영수증과 바이트 동일하다. 새 영수증의 차이는 각각 core_sha256, validator_source_digest, validator_commit, generated_at_utc뿐이다. producer·bundle·검사 결과·outputs·restore·runtime 및 dirty stamp는 보존됐다. paired 35 / grid 34 검사 수도 그대로다. 원장 변경은 두 leg의 receipt core SHA와 validator source_digest, 총 네 값이다. 이 범위에서 새 세대 영수증을 수용한다. 검토자가 make_receipt나 복원·재채점을 실행하거나 YAML core 직렬화 해시를 다시 계산한 것은 아니다.

## 자체 신고 a부터 h까지

a의 잘못된 RED 머리와 정정 후 재실행은 각각 보존돼 있으며 합산하지 않는다. b의 or-empty fallback은 앞선 비교에 가려 독립 방어 효과를 주장하지 않는 것이 맞다. c의 순서는 소스 및 이유·바이트 단언으로 확인되지만 줄 이동 변이를 실행한 증거로 확대하지 않는다.

d의 중복 치환 지점과 e의 낡은 영수증 identity로 인한 7 실패는 구분·보존돼 있다. 새 영수증 이후 해당 모듈 41 passed와 최종 전체 회귀 기록을 함께 수용한다.

f의 일반적인 durable 자료형 손상, 다른 read/view 경로의 추가 검사, g의 동시 실행 안전성은 이번에 검증 완료로 올리지 않는다. 그러나 이번 잔여와 고정 표 밖의 새 차단 조건으로도 만들지 않는다. h의 REIL·COMSOL·PyBaMM 건은 별도이며, 이번 종결로 수용하거나 승인하지 않는다.

## 다음 단계와 금지 범위

이번 결과는 **제한 구현 라운드 2b의 종결**이다. 동일 잔여를 다시 검증하는 라운드나 전체 회귀 반복을 추가 요구하지 않는다.

사용자가 정한 다음 순서인 PyBaMM 고정은 별도 범위·기준 identity·검증안·승인을 정하는 라운드로 넘길 수 있다. 이 회신이 requirements 변경이나 구현 착수를 승인하지는 않는다.

실행 GO, 새 연구 leg, 운영 원장 v6 계획, 세대표 등록, p_ini, class 변경, 투영 게시, COMSOL 계산은 승인하지 않는다. grid_fit_v5의 진단 전용 지위와 기존 과학적 주장 한계를 유지한다.

## 검토 방법의 한계

수신 코드는 데이터로 읽고 AST만 분석했다. 받은 모듈 import, pytest, smoke, 변이 재생, 복원, 영수증 재생성, COMSOL 실행은 모두 0회다. 원문 로그는 제출자가 보존한 실행 증거이며 검토자가 당시 OS를 직접 관측한 기록이 아니다.

검토자 정적 도구의 첫 출력은 Windows CP949 인코딩에서 실패했다. 같은 데이터 검사를 UTF-8로 출력했고, 재현 자료를 묶은 뒤 같은 결과를 재확인했다. 이 오류는 생산 코드나 제출 시험의 실패가 아니다. 관련 반환은 별도 보존했다.

문서 작성 지침에 따라 직접 대조 결과, 제출 로그, 잔여 한계를 분리했다. 원문·코드·실행 상태를 수정하거나 외부 발송하지 않았다.
