# D-2 — DEM Q3 M1–M9 리포 근거 미리 채운 표

**문서 메타 9행을 채웠다. 실제 빌드/실행 신원·자격·측정값을 수령한 표가 아니다.** 바탕은 `13eb293cd9ac44502517c81e8f5e9b7ae02d817f`이며, 1저자가 11-10 적용한 비 Rint 상시 요청서 D-2에 따른다. 원자료·원로그·실제 값·현장 조회·시험·계산0, 연구 결과0, 전체 HOLD다. 1저자는 아래 답안에서 고르거나 다른 부분만 고치면 된다.

## 1. 남은 선택과 준비 전제

| Q | 1저자가 고르거나 고칠 것 | 권고 한 줄 / 답 전 준비 |
|---|---|---|
| Q-D2-01 | M3–M6의 **역사 50kg/batch 비교 설계**를 새 gen2 0.7/1 µm 비교의 출발안으로 삼을지 | **권고안 전제 (Q-D2-01):** 과제 이름은 하중으로 환산하지 않고, 역사 선언 입력을 후보 표에만 이어 쓴다. 실제 빌드·압력 면적·표본·단계 신원은 미수립으로 남긴다. |
| Q-D2-02 | M1–M2에서 이미 보유한 **현행 gen2 빌드/자격 기록 메타**가 있으면 어떤 ID/판인지 | **권고안 전제 (Q-D2-02):** 아직 받은 현행 기록은 없으므로 UNKNOWN을 유지하고 문서·합성 준비를 계속한다. 새 조회·실행이나 원로그 제공은 요청하지 않는다. |

이 두 답을 기다리며 문서·합성 준비를 멈추지 않는다. 답이 다르면 해당 후보 칸만 바꾼다. D9′의 표적·단계·진밀도·랩 표준 출처는 이미 결정됐으므로 다시 비준을 묻지 않는다. 다음 D-3에서 필요한 T5/T11 정량 선택은 별도 권고안 전제와 미정 칸으로 다룬다.

## 2. 출처와 읽은 범위

아래 경로는 모두 **고정 B `13eb293cd9ac44502517c81e8f5e9b7ae02d817f`의 문서**다. 파일별 Git blob은 `provenance.json`에 적었다. 소스 식별자 목록은 과거 문서에 적힌 신원의 인용이며 현장 파일을 새로 해시하거나 실행했다는 뜻이 아니다.

| 근거 | 경로 | 사용한 § / 허용된 내용 |
|---|---|---|
| S1 | `docs/50kg/dem_plan_20261026.md` | 제목·도입, §0·3·4-1·4-2: 과제명·4차년도 선언 조건·PSD 한정·저자 결정·역사 seed/단계 규약 |
| S2 | `docs/50kg/codex_kg50_decks_request_20261026.md` | §1–3: 덱 변경의 선언 항목·반경/영역·검토 대상 프로그램 표지 |
| S3 | `docs/reviews/dem_protocol_gen2_plan_draft_20261014.md` | §0-1 D9′, §2-0·2-5–2-7, §4-4·4-5, §12 A2–A5: 현재 비준·계획 정의·합성/실제 사실 경계 |
| S4 | `docs/collab/claude_to_codex/20261109-2230_nonrint-first-link-sha-map.md` | §1–2: 첫 연결 B 반입·시험의 범위와 11-09 D9′ 결정 |
| S5 | `docs/reviews/dem_gen2_preparation_20261109/README.md` | §생산자 경계·§같은 정적 압력의 입경 비교·§아직 필요한 사실: gen2 편입과 실제 신원/정의 미정 |
| S6 | `docs/reviews/dem_gen2_limited_acceptance_20261109/README.md` | §신원과 반입·§지적별 수령 범위·§남은 경계와 원장 제안: 오프라인 수용과 실제 자격 분리 |
| S7 | `docs/reviews/dem_gen2_t12_consumer_contract_20261024.md` | 도입·§1–3: 역사 P1 소비자 코드 핀·합성 검사 범위·실제 P2 입력 요구. 당시 외부 대기 문구를 현재 미해결 상태로 복원하지 않음 |
| S8 | `docs/reviews/nonrint_approved_preparation_20261109/dem_nonresult_intake_form.md` | §1–5: 1저자 제공자 지정·허용 메타·누락/값 접근 경계 |

자료/증거 폴더의 원자·접촉·로그·결과 JSON·CSV, 실제 덱/체크포인트, 외부 업로드 원본은 열지 않았다. 계획 문서 안의 결과 인용이나 어림을 새 측정값·보정 표적·자격 판정으로 추출하지 않는다. litdb 정본이나 Rint 자료를 조회/변경하지 않았다.

## 3. M1–M9 — 바로 고칠 수 있는 답안

상태: **CURRENT_POLICY**=이미 비준된 현재 규칙, **HISTORICAL_DECLARATION**=해당 과거 과제/검토의 선언, **CODE_RECORD**=코드·문서 신원 기록, **UNKNOWN**=이번 허용 문서 범위에서 확인하지 못한 실제 사실. 어느 상태도 실제 자격 PASS가 아니다.

| M | 미리 채운 답 | 상태·근거 | 1저자가 고칠 부분 / 다음 준비 |
|---|---|---|---|
| **M1 프로그램·빌드·계약 판** | 역사 50kg 요청은 **LIGGGHTS-PUBLIC 3.8**을 문법 검토 대상으로 부른다. 현재 오프라인 gen2 후보 기록은 원 준비 `9241933b983605e3210753369a7cae5d6fc43432`, 네 수정 `6adf932499cd`, 첫 관측 연결 `708add516725cd3566d3b6c0ca3c1b7d15a10435`이며 첫 연결은 B `3900da4e000a3bc5b1234038a493aab2c869d05e` 사본으로 반입됐다. **실제 사용할 gen2 binary·소스 빌드 SHA·컴파일러/옵션·기록자/시각=UNKNOWN.** | HISTORICAL_DECLARATION / CODE_RECORD / UNKNOWN. S2 §3 Q4, S4 §1, S5 §생산자 경계, S6 §신원과 반입. | 이미 가진 현행 빌드 메타 ID만 추가/정정. **권고안 전제 (Q-D2-02):** 문서의 3.8 표지를 현재 바이너리 버전으로 확정하지 않고 오프라인 핀과 실제 빌드를 따로 둔다. |
| **M2 기존 자격 기록** | 기록 목록은 ① G2PREP-01–04 오프라인 수정/독립 한정 수용(2026-11-09), ② 첫 bridge 합성 검사/B 반입(11-09), ③ P1 ULPR 소비 계약의 고정 코드 `4c29705fa1c4ba94737a858b206fa4f4c5bb2bde` 및 합성 경계 문서(10-24; ULPRI 후속10-26)까지 연결할 수 있다. **현행 gen2 지정 빌드의 실제 T0·이력·복원·재개·dt/2 영수증=UNKNOWN. 실제 T0/T5/T11/T12=NOT_RUN.** | CODE_RECORD / UNKNOWN. S4 §1, S6 §지적별 수령 범위·§남은 경계, S7 도입·§2–3. | 원로그 대신 기존 자격 기록 ID·날짜·대상 빌드·P1/P2·합성/실제 범위만 보완. **권고안 전제 (Q-D2-02):** 과거 P1/합성 기록을 P2 물리 자격으로 승계하지 않는다. 기존 ULPRI/T12R 좁은 종결도 다시 열지 않는다. |
| **M3 “50 kg”의 뜻** | 리포의 문서 제목은 **“50kg/batch 과제”**다. 그 과제의 선언 가압 조건은 **300 MPa**로 별도 적혀 있다. 따라서 리포에서 확인한 것은 과제 표지이며 **50 kg를 압축 질량·힘 또는 300 MPa의 환산 입력으로 쓸 근거는 없다.** “batch 50 kg”의 정확한 사업/장치 의미는 UNKNOWN. | HISTORICAL_DECLARATION / UNKNOWN. S1 제목·§0, S5 §같은 정적 압력의 입경 비교. | **권고안 전제 (Q-D2-01):** 비교 이름은 `50kg/batch 과제의 D0.7/D1`로 두고 압축 하중은 별도 압력 규약으로 취급. 제목의 뜻이 다르면 그 설명만 정정. |
| **M4 면적·영역** | 역사 4차년도 계획은 **50×50 µm 기준과 40×40 µm 비교**를 구분한다. 요청서는 reg_box/reg_mix·판 꼭짓점·압력 면적 두 곳을 영역과 함께 바꾼 기록이다. **현행 gen2 0.7/1 µm 비교의 확정 영역·압력 면적·고정/시간의존 규칙·단위 사상은 UNKNOWN.** 실험 펠릿 면적과 DEM RVE 면적을 같은 칸에 넣지 않는다. | HISTORICAL_DECLARATION / UNKNOWN. S1 §0·4-1·4-2, S2 §1–2, S8 §4. | **권고안 전제 (Q-D2-01):** 역사 D0.7/D1의 명목40×40 µm를 비교 설계 후보 칸에 적되 실제/확정 면적으로 등록하지 않는다. 대체 영역/면적 규약이 있으면 고친다. 현장 면적 측정·환산 계산0. |
| **M5 입경 정의** | 사업/실험 비교 축의 명칭은 **SE D50 0.7·1·2·3 µm**. 역사 DEM 덱 변경 기록은 **r_SE=0.35/0.5/1.0/1.5 µm**와 AM r=3 µm다. 즉 D0.7/D1 모델 표지는 반경0.35/0.5 µm의 구 직경에 대응하는 **명목 단일 크기 입력**이고, 실제 PSD를 읽어 D50만 맞춘 분포 모델이라는 근거는 없다. 현재 실제 PSD·절삭·로트/시료 대응은 UNKNOWN. | HISTORICAL_DECLARATION / UNKNOWN. S1 도입·§0·§3의 PSD 한정, S2 §1. | **권고안 전제 (Q-D2-01):** 새 비교 초안에도 DEM 단일 크기와 실험 D50 표지를 별도 필드로 적는다. 같은 실제 입도분포/시료라고 인증하지 않는다. |
| **M6 재료·레시피** | 역사4차년도 선언은 **AM D6 단일, AM:SE=85:15 wt%, 면적당 용량6.5 mAh/cm², SE=LPSCl 하나, 선언 진밀도 AM4.85/SE1.64 g/cm³**다. 3차년도82:18·과거 D1–D3와 다른 설계다. 새 gen2 **E_SE 보정 침대는 순수 SE**이며 50kg 복합 비교 침대와 같은 역할이 아니다. 실제 새 팔의 recipe/단계/질량 신원은 UNKNOWN. | HISTORICAL_DECLARATION + CURRENT_POLICY / UNKNOWN. S1 §0·4-1, S3 §0-1 D9′·§4-4, S4 §2. | **권고안 전제 (Q-D2-01):** 50kg 0.7/1 비교에서는 역사 레시피의 선언 항목을 같은 후보로 유지하고 입경·gen2 프로토콜 차이를 명시. 실제 N만 같게 맞추지 않는다(S5). 새 물성 보정 결과·처방 계산은 없음. |
| **M7 단계·측정 상태** | 역사50kg 보고의 결정은 **가압→고정판 이완, 언로딩 제외**였다. 현재 gen2는 **삽입→안정화→압축→서보→R-a→언로딩→판 분리**이며, S0는 **고정판 R-a 끝**이다. 0.7/1 비교는 같은 실제 정적 압력·같은 관측 단계여야 한다. 실험의 실제 in-die/out-of-die/EIS 지그 상태·이력은 UNKNOWN. | HISTORICAL_DECLARATION + CURRENT_POLICY / UNKNOWN. S1 §4-1, S3 §2-5–2-7, S5 §같은 정적 압력의 입경 비교, S7 §3. | 새 준비는 현재 gen2 순서를 따른다. 역사 “언로딩 없음”을 gen2 언로딩 삭제 권한으로 이어 쓰지 않는다. 실제 측정 상태는 허용된 규약 문장만 보완. |
| **M8 관측 연산자·분모** | 현재 D9′: **순수 SE, 300 MPa 가압+이완 끝, DEM 자신의 질량 기준 ε_sphere, 선언 진밀도1.64, 외부 랩 표준10–13%가 E_SE 보정 표적**. **ε_union은 함께 기록만.** 현재 계획의 전체/안쪽 관측 구분은 유지하되 각 영역의 완전 재고·분모·벽 절단 규약은 T5 등록에 결속해야 한다. 복합50kg 팔의 실제 측정 연산자·분모는 UNKNOWN. | CURRENT_POLICY / UNKNOWN. S3 §0-1 D9′·§2-5·§12 A2–A3, S4 §2. | 이미 비준된 표적·진밀도·출처를 재질문하지 않는다. 정본의 옛 §4-4·4-5 등에 남은 union 표적 서술을 현재 보정 목표로 다시 채택하지 않는다. 기존 결과값으로 정의/분모를 추정하지 않는다. |
| **M9 대응·seed·불확실성·책임** | 역사50kg 본 비교는 **seed1**, D3 영역 비교는 **각 영역 seed3**로 목적을 나눴다. gen2 계획은 사다리 짝 seed·E마다 새 준비를 설명하며, §12 A2–A3는 공통 계통오차와 T5 coverage/다중사례·결손 처리를 요구한다. **현재 새 비교의 실제 seed 값·쌍 명부·반복 수·불확도/허용폭/coverage 수치는 미정. 제공자는1저자.** | HISTORICAL_DECLARATION / CURRENT_POLICY / UNKNOWN. S1 §4-1·4-2, S3 §4-4·4-5·§12 A2–A3, S8 §1–3. | 기존 seed1/3을 새 통계 자격의 자동 비준으로 쓰지 않는다. D-3 등록 초안에서 목적별 계획과 권고안 전제를 분리한다. 책임/기존 규약 ID가 다르면 그 부분만 정정하고 결과·원로그는 보내지 않는다. |

## 4. 그대로 붙여 답할 짧은 판

아래는 답의 빈칸을 줄인 문서 초안이다. **권고안 전제 (Q-D2-01/02)**인 역사 입력의 승계와 미확인 처리만 고르거나 수정한다. 기존 비준을 재승인하라는 요청은 아니다.

```text
M1 = historical LIGGGHTS-PUBLIC 3.8 reference; actual gen2 build identity UNKNOWN
M2 = offline/P1 document records identified; actual gen2 qualification receipts UNKNOWN
M3 = 50kg/batch project label; not a compression load conversion; exact batch meaning UNKNOWN
M4 = historical 40x40/50x50 um domains; current gen2 pressure-area contract UNKNOWN
M5 = DEM nominal sphere diameter 0.7/1 um; experimental D50 and actual PSD remain distinct
M6 = historical AM D6, AM:SE 85:15 wt%, LPSCl, declared TD 4.85/1.64; gen2 inheritance is a proposal
M7 = gen2 servo then fixed-plate R-a, then unloading and plate separation; actual measurement state UNKNOWN
M8 = adopted D9-prime: pure-SE mass-based epsilon_sphere, TD 1.64, external target 10-13 percent; union recording only
M9 = historical seed roles recorded; new paired roster, repetitions, uncertainty and coverage registration remain unset
Q-D2-01 = accept the historical-input proposal / correction: ...
Q-D2-02 = keep UNKNOWN / existing metadata reference: ...
```

## 5. 다음

D-2의 산출물은 **근거 있는 문서 답안9행·출처8개·남은 선택2개**다. 실제 M1–M9 수령 완료나 실행 신원 확립으로 표시하지 않는다. 다음은 D-3 표 순서의 **T0 고정 계약**이며, 빌드/실제 극성의 UNKNOWN을 합성 숫자로 채우지 않고 정상/반대 부호·원신원·단위/단계 결손의 합성 반례부터 준비한다. 이 문서의 작성 시험0, 실제 값 열람0, 운영 봉인0, 원장 수정0, 전체 HOLD.
