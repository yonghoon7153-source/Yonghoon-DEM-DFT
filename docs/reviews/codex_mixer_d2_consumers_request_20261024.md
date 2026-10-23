# Codex 재확인 요청 — D2 개발 소비자의 실제 덱 결합 검사 (2026-10-24)

> 현재 canonical 전체 gate: **PASS, 155/0, rc 0**. [완료 기록](mixer_d2_consumers_evidence_20261024/completion.md)을 따른다. 아래 작성자/초기 반입 시점의 예정·대기 문구는 원 스냅샷의 범위이며 현재 상태를 대신하지 않는다.


**검토 대상은 MXD2-01의 개발 소비자 부분이다.** lab 밀도 덱이 구 되읽기에 거부되고, D2 코팅 쌍을 비교할 경로가 없으며, 스모크가 gen1 계획수를 사용하는 문제에 개발 전용 경로를 추가했다. 기존 등록 계약은 유지한다. 새 S1 셀·코호트·정책 구현·등록까지 MXD2-01 전체가 닫혔다고 주장하지 않는다.

사용자의 “다 비준이야”는 제시된 설계·정책 방향의 비준으로 반영했다. 후속 개발을 반복 승인 대기에 두지 않는다. 구체적인 S1 수치·시드·코호트와 필요한 실물 입력, 실행 정책 구현·등록·독립 검증 산출물이 아직 완성되지 않았다는 사실은 별도로 기록한다. 새 확인 런, LIGGGHTS, 실제 믹서·장비 실행, 외부 발송·외부 GO는 이 작업의 실적이 아니다.

## 1. 범위와 핀

기준 핀은 `codex/mixer-mxd2`의 `486a57cf58d3e0d93ef79be6aae50968929099c0`이다. 저장소 밖 scratch에 그 핀을 내보내 작업했고, 작성자는 checkout·refs·commit·push를 변경하지 않았다. root가 최종 반입·전체 관문·커밋·`codex/*` push를 담당한다. 받을 커밋의 예정 설명은 `Add explicit mixer D2 development consumers`, 쪽지 자리표시는 `<<sha:Add mixer D2 consumers>>`이다. 새 자기 SHA는 commit 후 외부 전달 PIN에 기록한다.

생산 변경은 `scripts/mixer_deck_readback.py`, `scripts/mixer_deck_diff.py`, `scripts/mixer_smoke_blind.py`와 신규 회귀 `scripts/test_mixer_d2_consumers.py`다. `/mixer` 이력은 `docs/mixer_devlog/v18_20261024.md`다. 생성기·additives·webapp/app.py·봉인 32파일·공유 원장·전역 관문·실행 정책은 수정하지 않았다. 실제 밀도·중력·벽 계수·새 캠페인 수치는 정하지 않았다.

정본은 인계서 §5-3, `docs/hetero_thesis.md`의 D2, `docs/mixer_d2_wall_gamma_derivation_20261014.md`, 밀도 세대 정본이다. 원래 `MXD2-02`–`06` 생성기 수정과 `MXD2-07` D3 설계 검토의 범위를 이번 소비자 작업과 합산하지 않는다.

## 2. 개발 계약

| 경로 | 실제 검증 | 한정 |
|---|---|---|
| `mixer_deck_readback.py --d2 DECK META` | 실제 텍스트 SHA·바이트; 정확한 밀도 세대/표와 실제 template 밀도; 활성 상·E·ν·반경·CGF; 실제 중력·인쇄 CED로 계산한 절대 Bo·기하평균 쌍 힘·벽 규칙·정적 겹침; 시간·step·주기; 분포·삽입 계획 | AM_P+AM_S+SE 및 기존 AM_P+SE. 등록 표 E/E0/DT/B/U를 확장하지 않음 |
| `mixer_deck_diff.py OLD NEW --allow D2 --meta-ref A --meta-new B` | 양쪽 독립 절대 검산, 같은 밀도·ρ·Bo·CGF·강성·시드·시간·계획수, NCM γ가 ρ→1, CED 밖 명령 토큰 동일 | 구 A/B/U/E/EB·등록 셀·cohort는 그대로. ρ=1 퇴화 비교를 명시 |
| `mixer_smoke_blind.py --d2-plan DECK --d2-meta META` | 위 개발 되읽기와 실제 분포·삽입 명령의 상별 계획수 | 덤프의 관측 입자수, 접촉·정착 해제·확인 런 증서를 만들지 않음 |

공통 출력은 `registered: null`, `execution_authorized: false`다. JSON 중복 키와 계약 의미를 바꿀 미지원 키, 숫자의 Unicode/underscore·비유한·잘못된 타입을 변환 전에 거부한다. 실제 덱의 밀도나 SHA를 메타 값으로 대체하여 검증하지 않는다.

계획수는 활성 원 배합 질량비 AM_P:AM_S:SE=56:24:18과 밀도·반경에 따른 입자수 비를 독립 계산한다. 실제 덱의 6자리 질량 분율은 반올림 한계 `0.500001e-6` 안에서 배합에 묶는다. 단일 삽입은 인쇄된 요청 총수를 사용한다. 층상 삽입은 인쇄된 두 그룹 합계에서 최대 2개 반올림 구간의 후보를 열거하고, 각 그룹 수와 일치하는 상별 계획 벡터가 하나일 때만 통과한다. 이는 입자의 확률적 실제 삽입 결과를 관측했다는 뜻이 아니다.

덱의 run 구조는 삽입→정착 두 단계→회전이다. 실제 영역·메시·분포 참조와 정의 순서, 삽입 fix 제거 시점, 삽입 전 구 적분기, 정착 후 메시 회전을 검사한다. 전체 기하의 실물 적합성·STL 내용은 별도 대상이다.

CED 6유효숫자·반경 6유효숫자의 인쇄 오차 때문에 절대 Bo 상대 허용폭은 `2e-5`, 쌍별 힘은 기존 `3e-5`다. 밀도표·실제 밀도·E·ν는 정확히 비교한다. 시간은 기존 인쇄 규칙의 허용폭을 쓴다. 이 폭은 결과에 맞춰 넓히지 않았다.

## 3. 실패에서 통과까지

증거 루트는 [mixer_d2_consumers_evidence_20261024/](mixer_d2_consumers_evidence_20261024/)다. Python 3.11.17, `python -I`, BLAS/OMP 1, 합성 덱·텍스트·계획 검사만 사용했다.

| 구분 | 관찰 | 근거 |
|---|---|---|
| 원래 3제한 | 핀 기준 lab 표 E FAIL, A/B/U/E/EB의 D2 코팅 쌍 모두 FAIL, gen1 고정 계획수 불일치 | [원자료](mixer_d2_consumers_evidence_20261024/author/logs/baseline-reproduction.json) |
| 수치 반례 | N=100000·CGF151.4에서 gen1 `(176,859,98965)`와 lab `(143,699,99158)` | 같은 JSON. 메타 라벨만 바꾸지 않고 실제 덱과 계획 대조 |
| 첫 시험 먼저 | 신규 API/CLI 미구현: 8메서드에서 failure 1·error 134 | `author/logs/test-first.log`; 위 물리 반례와 별개의 API 부재 red |
| 후속 작성자 red | 숫자 표기·dt_factor=1/2, 명령 범위의 실패 재현 뒤 수정 | `author/tests_first/`와 `author/logs/edge-tests-first.log`, `command-scope-red.log` |
| 독립 v1 red | run 전 삽입 제거, 적분기 삭제, 정착 전 회전, 존재하지 않는 삽입 영역이 공통 변형이면 PASS | 독립 `command-order-v1/` 원본 및 작성자 `lifecycle-red.log`(13메서드·9실패) |
| 최종 신규 회귀 | 13메서드 PASS: 정상 128덱, N/CGF/삽입/밀도 48조합, 정상 D2 32쌍, 경계·CLI·명령·생명주기 반례 | `author/logs/ceiling-coverage-green.log`. 서로 다른 조합 수를 고유 덱 총수로 합산하지 않음 |
| 최종 작성자 변이 | 실제 guard 제거 19/19 검출, clean PASS | [원자료](mixer_d2_consumers_evidence_20261024/author/mutation-final/results.json) 및 해당 로그. 초기 실행 환경 실패·생존 변이는 아래 기록 |
| 구 계약 회귀 | readback 24/24, diff 55/55, smoke 자체시험 rc0 | `author/logs/{readback,diff,smoke}-v2-final.log` |
| 웹앱 v18 | 실제 `/mixer` route, scratch 문서 조회·데이터 폴더: 9/9와 CLI·개발 한계 표시 | `author/logs/render-v18-final.log`, [원자료](mixer_d2_consumers_evidence_20261024/author/render-summary.json) |
| 독립 검토 | frozen v3 개발 소비자 범위 GO. 9개 유효 변이 검출, 최종 신규·구 자체시험 PASS | [독립 보고서](codex_review_mxd2_consumers_independent_20261024.md)와 [원본 증거](codex_mxd2_consumers_independent_evidence_20261024/) |
| 저장소 FULL gate | root의 최종 반입 후 기록. 현재 소비자 패키지만으로 FULL PASS를 주장하지 않음 | `full_gate_receipt.json` |

작성자 초기 변이 v1은 의존 모듈 누락으로 clean부터 실패했으므로 효력 증거가 아니다. 의존성을 갖춘 v2에서는 밀도·중력 guard 제거가 생존했다. 모든 밀도를 같은 배율로 바꾸고 힘·시간까지 일관되게 재계산하는 반례와 중력 벡터 반전을 추가했다. 첫 밀도 배율 1.001은 밀도 정수 인쇄 오차가 Bo 검사에 걸려 guard 효과를 가렸으므로, 실제 밀도가 정확히 인쇄되는 1.1 배율로 시험했다. 이는 실험 수준 제안이 아니다. 최종 19변이에는 두 guard와 생명주기 4개, 정적 천장이 포함된다.

독립 검토가 지적한 천장 시험 공백도 별도로 보강했다. CED를 ×100, 선언 Bo를 ×100³하고 hash/bytes를 일관 갱신하면 절대 Bo가 일치해도 실제 정적 겹침이 1%를 넘는다. 이 입력은 천장 guard에서 실패하며 그 guard 제거 변이는 회귀가 잡는다. v2→v3는 이 시험 보강만 있고 생산 3파일은 같다.

독립 덱 행렬은 90사례·249호출이며, 그중 2사례·6호출은 공통 기하와 둘째 삽입 시드의 범위를 관찰한 것이므로 PASS/FAIL 정답을 부여한 공격 수로 세지 않는다. 정상 48조합은 구현자의 기본 입력과 다른 N=100003·CGF125·seed49979687·Bo1.125를 사용했다. 생명주기 별도 6대조·18호출도 기대와 일치했다. 행렬·생명주기는 v2에서 실행했고 v3의 생산 SHA가 동일함을 대조했다. v3 신규/구 자체시험·변이는 직접 재실행했다. 다른 계획 검토자의 관찰을 추가 독립 GO나 추가 시험 수로 합산하지 않았다.

## 4. 남은 경계와 요청 판정

개발 보고서는 실제 덱의 검증 대상 필드를 열거한다. 모든 메타 설명문·발행 도구 SHA·생성기 argv·부차 난수열을 인증하지 않는다. 둘째 삽입 시드 등 모든 생성기 난수 서명, STL/장비 형상, 실행 바이너리·재개 이력·실측 접촉과 혼합 결과는 이 경로의 범위 밖이다. 공통 기하 토큰이 두 덱에서 같다는 사실은 그 기하가 실물에 맞는다는 인증이 아니다.

AM_P+SE 양성을 보존했다. AM_S+SE의 기존 생성기 `AM_P` KeyError는 이 변경에서 새로운 지원으로 바꾸지 않았다. 실제 입자 실행·관측값은 0건이다.

MXD2-01의 (1) 밀도 세대·실제 계획수 결합, (2) 명시적 D2 개발 쌍 비교를 `claimed_fixed` 하위 범위로 검토해 달라. (3) 새 S1 셀·코호트·정책 구현·등록·실물 입력은 구체 산출물과 함께 후속 검토한다. 원장 전체 상태를 verified/closed로 자동 전환하지 않는다. 이전 25개 claimed_fixed나 MXD2-02–07을 이번 13메서드·19변이로 다시 검증했다고 주장하지 않는다.

재현 절차와 파일 해시는 증거 README·manifest에 있다. 내부 독립 최종 판정은 동봉했으며, 신규 consumer pin의 최종 FULL gate·통합 pin 대조가 남아 있다. 그 결과 없이 전달 패키지 전체 검증이 끝났다고 표시하지 않는다.
