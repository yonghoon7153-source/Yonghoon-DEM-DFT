# LHS 감쇠 관측 companion 등록칸 초안 — 한정 검토

2026-11-05 · 대상 `bb6e86ac44f70a27b154db62fc14a624cab944df` · `codex/lhs-v13-1104`

**문서·정적 정의 범위 수용. 새 P1/P2/P3 없음. 전체 HOLD와 실제 값 열람·실행·등록·배포·통합·원장 종결 미승인을 유지한다.**

이번 판정은 새 companion의 정의·출처·비활성 경계에만 적용한다. pressure_inventory 명령은 실행/import하지 않았고 LPI를 재감사하지 않았다. 실제 압력·감쇠 원자료, ibb/WSL, 회귀·전체 게이트에는 접근/실행하지 않았다.

## 1. 핀·바이트·변경 범위

| 대조 | 결과 |
|---|---|
| 입력 ZIP | `codex_lhs_damping_draft_20261105_bb6e86ac44f7.zip` · 119,393 B |
| SHA256 | `4369eec3be7e8df50a11f45d0cff53584a1202be036de1c2499149d47b59f491` |
| 포장 | 27멤버, 자기 해시목록 제외 26개 일치 |
| 스냅샷 | 11파일 크기·SHA256·Git blob 일치; 원격 고정 핀의 11개 SHA/크기도 일치 |
| 부모 | `73895add198eae4926b1944b6e1f05a54ca57d13` — PARENT_PIN과 원격 commit 일치 |
| 실제 commit 변경 | docs 아래 7파일 추가만. 기존 inventory·등록·공유 기록 수정 없음 |
| 요청서 | REQUEST.md와 저장소 review_request.md 바이트 동일 |

근거는 `intake_verification.json`, `remote_verification.json`, [검토 commit](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/commit/bb6e86ac44f70a27b154db62fc14a624cab944df)의 변경 목록이다.

## 2. REQUEST 질문별 답

### Q1. 공통 c_v·동일 실행/시점/그룹/단위/부호·실측 판힘 — 수용

초안 README:7–14와 companion:25–46,51–54는 **검증된 공통·균일한 선형 입자 외력 `F=-c_v v`**에만 `-c_vΣv_z`를 후보 분자로 둔다. 타입/질량별 계수, 상대속도, 접촉 dashpot이면 정의를 다시 정한다. c_v는 표면에너지 gamma와 다르다. 공식 fix viscous 문서의 힘/속도 계수와 타입별 scale 설명에도 맞는 제한이다. [LIGGGHTS 공식 문서](https://www.cfdem.com/media/DEM/docu/fix_viscous.html)

이 식이 모든 감쇠 법칙의 보편식은 아니다. 합성 계수 [1,2], 속도 [1,1]일 때 올바른 순힘은 -3이고 공통 계수 1로 잘못 묶으면 -2다. 초안은 이 반례를 적용조건 밖으로 분리한다. 실제 케이스에서 균일 계수가 확인됐다고 주장하지 않는다.

실제 덱/fix·재개 구간·파일 해시, 동일 정지 사건·표본 step, 그룹/입자 ID, 속도 기준계, 판힘의 성분·방향·단위·접촉 반력/구동력 정의가 선행 조건이다. 단순 재고 줄 수를 동일 실행 증명으로 쓰지 않는다. 명목 750 N은 `nominal_load_if_separately_documented`로 실측 판힘과 분리되며 분모 대체에 쓰이지 않았다. 타 트랙 D0.7 숫자가 LHS 관측값으로 들어간 필드도 없다.

“정지 판정 시점의 부호 있는 비율”이라는 이름은 수집 전 정의 후보로 수용할 수 있다. 최종 물리 기여율·소산율 또는 0–1의 분담률이란 뜻은 아니다. 반대 방향 속도가 상쇄되는 순힘은 0일 수 있어도 소산은 양수일 수 있다. 초안은 clamp와 자동 힘 분담 해석을 금지한다.

### Q2. 결측·0 분모·비유한 처리와 비활성 template — 수용

직접 JSON을 읽은 결과 `measured_rows=0`, `rows=[]`, template status `NOT_COLLECTED`이며 **status 외 26개 실제 자료 필드는 전부 null**이다. 실행·값 열람·활성 등록 변경·새 reader 제공은 false다.

README:15–17과 companion:57은 미수집을 NOT_COLLECTED/null, 수집 후 0/비유한 분모 또는 비유한 결과를 UNDEFINED/null과 사유로 남긴다. 결측을 숫자 0으로 채우거나 clamp하지 않고 새 문턱도 없다. 반대로 유한한 실제 분자 0/비영 분모의 계산 결과 0까지 금지하는 규칙은 아니다. 이 구별은 정합적이다.

평균 창을 나중에 정할 때는 샘플 step 집합·가중치·누락 처리와 평균 연산 순서를 명시해야 한다. 같은 두 시점의 합성 분자 [1,9]/분모 [1,3]도 `평균 후 나눔=2.5`, `비율의 평균=2`다. 현재 README는 순간/구간 통계와 수집 정의를 사전에 정하게 하고 `window_definition=null`로 남겨 두었다. 따라서 이번 문서 수용은 그 선택이 끝났다는 판정이 아니다. 실제 수집 비준의 남은 구체화이지 새 P등급 결함은 아니다.

### Q3. D0.7 전용 방지·재고 순서·LPI 경계 — 수용

봉인 명령의 SHA256은 `2305bd2194b29ac5439008906a17b1c673968a59fd52dcdde35b03ff4da20634`로 README·companion·스냅샷과 일치한다. 원격 부모 대비 명령 변경도 없다. 기존 `lhs_pressure_inventory/v1`에 새 key를 추가한 생산 코드 변경은 없고, companion은 별도 비활성 문서다. 실제 inventory 출력의 신규 관측을 했다는 뜻은 아니다.

companion README:23·35 및 JSON:59–62는 `s5_judgment/README.md` §11-8의 순서를 보존한다:

1. 기존 재고 절차와 1저자 승인 결과.
2. A/C 선택 및 값 열람 규칙 비준.
3. 별도로 승인된 자료 수집·관측.

기존 거부 TSV·Q1/Q7 결정·압력 적격성 규칙을 우회하지 않는다. LPI-01/02의 출력/종료·시간위험 문구 한정 수용도 실제 호스트/압력 적격성/배포 GO로 확대하지 않는다. regex·디렉터리·파일시스템 시간 위험, OBS-AUDIT-01 최초 원인 미확정, 전체 HOLD를 유지한다. ledger_proposal은 apply_now/closure_claimed/활성 등록 변경 제안이 모두 false이고 새 finding 적용도 없다.

고정 원격 `cc1a96796bc8dcffaf035af81168fccf405c1fc9`의 [D0.7 README](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/cc1a96796bc8dcffaf035af81168fccf405c1fc9/docs/data/kg50_d07_end_20261105/README.md) bytes SHA256은 `87bde2a8c169f6e56b203ed14f3040d9c47b26a06cd937bca1382d50a96c06a3`이며 context에 적힌 것과 일치한다. §1–3만 있고 §4는 없다. 문서는 job 338349/끝 2,135,002와 압축 정지 2,035,002를 기록한다. 이는 문서 대조이며 실제 호스트 완료를 새로 인증한 것이 아니다.

전달된 감쇠 표본 2,000,000과 정지는 35,002 step 다르다. 전달 93.4%·계수·속도·입자수를 재계산하거나 LHS 값으로 쓰지 않았다. 다른 시점의 압력으로 같은 정지 사건의 비율을 채울 근거도 없다. source_context의 숫자는 타 트랙 전달 출처 기록이고 실제 companion 필드는 null이다.

60/60 자원 사용도 전달 관찰이다. 4+56=60이라는 산술은 현재 큐/가용 자원 확인이 아니며 D0.7 완료는 LHS의 실행 승인 조건을 자동 해제하지 않는다. Rint② 우선·새 제출 계획 없음·통합 미승인은 유지된다.

## 3. 수행·증거·남는 경계

LHS 경계 담당의 25개 정적 술어는 JSON 상태·필드·해시·순서 검사다. 회귀 시험 25개나 실제 관측 25건으로 세지 않는다. `task/lhs_boundary/static_comparison.json`에 결과가 있다. source_context bytes와 companion의 SHA는 맞지만, 초안 작성 때의 별도 scratch 원문 자체가 제공되지 않아 그 최초 원본과의 동일성은 인증하지 않는다.

같이 검토한 믹서 초안의 메모리 8덱 대조는 별도 범위다. 그 결과를 LHS 실행·pressure_inventory 시험으로 전용하지 않았다. LHS에서 명령 실행, 원자료·호스트 접근, 압력/감쇠의 실제 계산, suite/full gate는 0건이다.

새 지적 ID·필수 최소 수정은 없다. 실제 수집 계약에서 위 미정 정의를 비준하고 수집 권한을 별도로 정해야 한다. 이 판정은 그 비준을 대신하지 않는다.

**문서·정적 범위 수용 / 전체 HOLD / 값 열람·실행·등록·배포·통합·원장 종결 미승인.**
