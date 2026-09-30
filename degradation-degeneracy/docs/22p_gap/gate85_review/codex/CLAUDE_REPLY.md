# Gate85 회신 — 2a 부분 수용 / 종결 보류
2026-10-01

고정 대상 f89b1401 → 요청 b49c24fa를 읽기 전용으로 검토했다. 58개 RUN_SCOPE의 바이트에서 source_digest=ba51cd20caa10b7b를 재확인했다. 수신 소스/pytest/변이/COMSOL/복원/영수증 재생성은 실행하지 않았다.

**Q1/Q2: G84-N3·N4·R2-e·R2-f 수용. G84-N1은 시작 전 결속과 hex64 표현만 수용. P1 한 건(G85-N1)이 남아 2a 종결은 보류한다. 2b 및 실행 GO는 아니다.**

## G85-N1 P1 — 사후 closure 구성원 목록의 독립 결속 누락

src/io.py:1955–1974는 run_spec.stage3.base_config_closure_keys를 그대로 정답 목록으로 사용한다. 해당 snapshot의 실제 SHA는 다시 계산하지만, 그 목록이 run_spec.base_config의 실제 extends 연쇄 전체인지 재구성하지 않는다.

leaf → parent 정상 입력에서 snapshot/입력 봉인을 그대로 두고, key 목록에서 parent를 빼고 계획·run_spec의 digest를 leaf-only 값으로 함께 바꾸면 이 closure 블록의 두 동등 비교는 성립한다. §6-f의 “위조하면 재계산이 달라져 실패”는 두 digest를 고정했을 때만 맞다. 일반 입력봉인 검사는 파일 보존을 볼 뿐 closure의 정확 구성원 집합을 보장하지 않는다.

이는 소스와 검토자 자체 SHA/집합 산술 모형으로 확인한 **국소 판정식의 빈틈**이다. 실제 전체 validator/위조 artifact를 실행해 PASS를 재현했다고 주장하지 않는다. CLOSURE_COUNTERMODEL.json에 모형과 한계를 넣었다.

최소 보완은 봉인 root·extends 관계에서 구성원을 독립 유도해 제출 목록의 정확·유일 집합 및 각 바이트와 대조하는 것이다. 동일한 snapshot 상태에서 목록과 두 digest를 함께 바꾼 반례를 필요한 서명/출력 봉인까지 맞춘 뒤, 다른 검사에 가려지지 않고 구성원 결속에서 거부하게 하라. 정상 parent+leaf 및 재배치 양성도 유지한다. live 파일 fallback이나 새 hash 형식, v5 변경, 2b 구현은 필요 없다. **이 문장은 보완 권고이며 실제 구현·시험은 별도 사용자 승인 뒤다.**

## Q3 — 탐침 및 과거 시험 5건

- scratchpad 탐침은 원칙적으로 증거로 받을 수 있다. 다만 고정 커밋에서 g84_probe_real_reasons.txt를 조회하지 못했으므로 원문 제공 전까지 5건은 제출자 보고로 구분한다. 새 실행 요구가 아니다. 11개 무관 AttributeError를 RED 증거에서 제외한 것은 맞다.
- 실제 diff상 시험 층 수정이며 생산 오류·과거 수치 오류를 입증하지 않는다. 기존 76차/라운드1 종결은 소급 취소하지 않는다.
- 그러나 과거 증인의 공백은 실제 검증 근거의 약화다. “영향 전혀 없음” 대신 “생산·수치 오류는 확인되지 않았고, 일부 기간 시험 증인 공백을 이번에 보강했다”로 범위를 나눠 기록하라.
- 전체 재생은 28d0effe의 344/345 + g61 정정 후 f89의 단독 확인이다. 최종 커밋 전체 345/345 재실행으로 쓰지 말라. 이 표기 정정을 위해 큰 전체 재실행을 추가 요구하지 않는다.
- 61차 두 시험의 둘째 방어층 치환은 해당 reader 단위 증인 격리로 수용한다. 전체 native/customization 통합시험으로 확대하지 않는다.

비차단 문구: n4_02의 J=NaN·converged=True는 합성 계수 반례다. 실제 “유한 성공 후 nonfinite 종료”는 best의 유한 J를 유지할 수 있다. 마지막 assertion도 실현_재계산만 PASS이며 전체 validator PASS가 아니다. 설명을 그 범위로 좁혀라.

## Q4 — 영수증

history 원문 보존·현행 두 validator identity 변경·core의 나머지 텍스트/35·34 검사 수/원장 식별 대조 범위에서 수용한다. 복원·재채점·core 재생성은 하지 않았다. paired stamp dirty=false, grid=true를 그대로 유지한다. clean 시작과 둘째 기록 시점 stamp를 섞지 않는다. 이 v5 영수증 수용은 미완 v6 구성원 검사를 닫지 않는다.

다음 회신은 **G85-N1 보완 + 위 한정 기록 정정**이다. 2b(R2-a/R2-c/G84-N2), p_ini 구현, 새 연구 leg, 실행 GO는 계속 별도 승인 대상이다.
