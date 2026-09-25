# Gate72 회신 — E9-R 수용 / E3-R 원장 결속 P1 한 건만 잔여

대상 요청/HEAD `c4b77ccf71d736dec9162cd5a5377f60f66c0782`, 코드 `82854571d0240951c929d4a9b90260e53ca38e88`, 직접 byte 계산 source_digest `518d4f63076b77e3`. 코드→HEAD RUN_SCOPE diff 0을 확인했다.

**§3 답: ① E3-R 종결 아니오(아래 한 항목), ② E9-R 예, ③ 현재 한정 실행 GO 아니오.** E1/E2/E4나 과거 class 정리를 다시 여는 판정이 아니다.

## 수용

두 산출 역할/닫힌 키, 같은 schema·canonicalizer의 semantic 값 실제 비교, source fits 결속, identity hex16, restore_map와 복원 자리, sealed summary의 실물 SHA를 확인했다. 지정 reader/helper 국소 검사 14건에서 실물 양성 1건 수용·결손/불일치 13건 거부. 묶음 index25 구성원과 26파일 전체 크기/SHA를 데이터로 확인했다.

E9는 최초 실행 실패 즉시 정지 → 같은 plan/token/source 및 재개 가능한 부분 산출 확인 → 명시 `--resume` 최대1회 → 재실패 시 재승인으로 수용한다. finalize/archive/receipt/attach 실패를 자동 resume한다는 의미는 아니다. D7 최종 승인 HEAD, D8 unset, D9 11표본, E6 requirements 복사 정정도 수용한다.

## E3-R 잔여 [P1] — 실행 자리 결속이 필수가 아님

`tools/preserve.py:7936`이 `if "out" in ev:`다. 앞선 LIFECYCLE_OWNED_EVIDENCE_KEYS(:7386)에는 out이 없다. pending 원장에서 out을 빼면 대조 없이 :7959–7961 full_bundle/current_validated 쓰기 경로에 도달한다.

또 :7917–7921의 full_bundle 멱등 반환이 out 대조보다 앞선다. 같은 영수증 path/core SHA만 남아 있으면 원장 out이 다르거나 없어도 idempotent=True를 반환한다. 첫 문제는 신규 승격 조건 누락, 둘째는 현재 모순을 확인하지 않는 멱등 성공이다. 같은 E3-R 원장 결속의 두 분기이며 별도 신규 과제를 늘리지 않는다.

수신자는 실제 attach 본문을 추출해 명시적 inert collaborators/쓰기 차단 sink로 6경우를 확인했다:

| 상태 | 일치 out | 다른 out | out 누락 |
|---|---|---|---|
| pending | 쓰기 지점 도달(양성, 실제 쓰기 차단) | 거부 | **쓰기 지점 도달(실제 쓰기 차단)** |
| full_bundle + 같은 영수증 | 멱등 성공 | **멱등 성공** | **멱등 성공** |

운영 원장 write/복원/class 변경은 0회다. Linux 전체 attach/lock 경로를 재현한 실험이 아니며 stub 목록·본문 SHA·결과는 RECEIVER_CHECKS.json에 공개했다. 새 test_g71_e3r_07b와 그 변이는 ‘필드가 있는 불일치’만 검사하므로 기존 3/3 통과와 모순되지 않는다.

### 최소 종결

1. 신규 승격에서 `evidence.out` 존재·유효 문자열·묶음/영수증 실행 자리 일치를 필수로 한다. 부재 시 skip 금지.
2. 멱등 성공 이전에도 실행 결속을 확인한다. out 없는 역사적 자료는 소급 추정/재작성하지 않고 미결속/거부를 명시한다. 과거 자료 읽기와 신규 승격 성공을 구분한다.
3. 위 6경우의 정상·누락·불일치 회귀와 거부 시 원장 바이트 불변을 제출한다. 이 좁은 수정 diff와 새 commit/source_digest를 받으면 된다. E9 재설계·서명/OS principal·E1/E2/E4 전면 구현·367개 재작성은 요구하지 않는다.

현재 실물 paired_fixed5_v4 원장에 out이 없다는 사실도 확인했다. 이를 신규 실패 실행/과학 결과 오류로 단정하거나 사람이 지금 채우라는 요청으로 읽지 말라. 해당 실물 양성 시험은 reader/helper 범위여서 이번 out/멱등 분기를 보지 않는다.

1869/2·smoke·370 등은 송신 실행 증거로 유지한다. 테스트 보고 HEAD b9213333→요청 HEAD의 변경이 문서3개뿐인 것은 직접 확인했다. 전체 suite/본 계산은 재실행하지 않았다. 이전71차 ZIP과 펼친37 payload가 원본과 동일하고 등록부367 바이트도 동일하다.

**이번 회신은 검토 결과이며 수정·복원·class 변경·prospective 작성/커밋·본 실행의 대리 승인이 아니다. 현재 한정 GO 보류는 위 E3-R 한 항목 때문이다.**
