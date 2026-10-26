# 세대 2 T12 — 외부 설계 검토·통합 인계 자료 (2026-10-26)

이 문서는 이미 비준된 설계 결정을 재선택하는 요청이 아니다. 수령한 ULPRI 종결을 반영하여 기존 T12 준비의 **소비자 계약·합성 시험·남은 사실 경계**를 외부 검토할 수 있도록 고정한다. 실제 P2 `T12=NOT_RUN`, `physical_ready=false`다. 외부 설계 검토 결과·검토자 신원·P2 등록·실행 자격을 이 문서가 생성하지 않는다.

## 검토 대상과 이미 있는 근거

| 대상 | 고정 신원·범위 |
| --- | --- |
| 수용된 소비자 | `4c29705fa1c4ba94737a858b206fa4f4c5bb2bde`, `codex/unloading-ulpri`. ULPRI-01/02 표지 경계 무결성만 외부 GO. |
| 기존 T12 전달본 | `2b4b40ea5e375659bfad8243c1ccb6fe0ef2853f`, `codex/dem-gen2-t12`. 합성 계약 준비이며 실제 복원 시험 아님. |
| T12 전체 게이트 대상 | 코드 후보 `f1da507e8ab8bf812a242b9749d4c320be90fd73`: 기존 영수증 155 PASS/0 FAIL/rc 0. 새 문서 트리의 전체 게이트 결과로 전용하지 않음. |
| T12 직접·독립 근거 | 고정 소비자 52/52, 독립 같은 결과·소스 거부 5·계약 결손 3·표적 변이 13. 공유 155와 별개이고 새 문서 작업에서 재실행하지 않음. |
| 계획·비준 기준 | DEM 준비 `2443a63eaa87d52e385a35f8bab4225efa0d25fe`, 최초 설계 provenance `962caea2d1857b0e34fe724e38815661936b7183`; 비준 A1–A5 및 Q1–Q16 선택 유지. |

[고정 T12 계약](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/2b4b40ea5e375659bfad8243c1ccb6fe0ef2853f/docs/reviews/dem_gen2_t12_consumer_contract_20261024.md), [직접 결과](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/2b4b40ea5e375659bfad8243c1ccb6fe0ef2853f/docs/reviews/dem_gen2_t12_consumer_contract_evidence_20261024/fixture-results.json), [현재 독립 검토 재현 안내](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/2b4b40ea5e375659bfad8243c1ccb6fe0ef2853f/docs/reviews/dem_gen2_t12_consumer_contract_evidence_20261024/independent-ulpri/REPRODUCE.md), [전체 게이트 영수증](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/2b4b40ea5e375659bfad8243c1ccb6fe0ef2853f/docs/reviews/dem_gen2_t12_consumer_contract_evidence_20261024/full_gate/result.json)을 서로 다른 증거로 읽는다. 이들 과거 문서의 외부 대기/HOLD는 당시 상태이며 새 종결 기록이 날짜별 후속 상태를 제공한다.

## 외부 검토 요청 범위

1. 고정 P1 계약 발췌가 P2 등록·생산자 구현으로 잘못 취급되지 않았는지 검토한다. 실제 P2 명명·h0 환산·시간창·중력 예외·resume 전이는 아직 사실 자료가 필요하다.
2. 52개 합성 관측의 결론과 한계가 일치하는지 검토한다. G2 기본 비교는 mass·omega 변경을 인증하지 않는다. G2c 접촉 관측은 숨은 δmax 이력 동일성의 단독 증명이 아니다. `_atom_frame`의 ID/step 확인도 전체 S0 질량·상 재고 인증이 아니다.
3. 새 외부 GO가 ULPRI-01/02의 원문 표지·줄 경계와 인증/옛 행 제외에만 적용되는지 검토한다. 임의 CSV 문법·모든 사건명·실제 restart 자격으로 확대하지 않는다.
4. 아래 남은 사실과 연결 후 작성할 생산자/소비자 시험의 순서가 충분한지 의견을 남긴다. 미수령 자료는 결손으로 표시하고 합성값·P1값으로 채우지 않는다.

요청한 설계 검토의 응답에는 검토 대상 pin·문서, 범위별 수용/수정 필요/미검토, 근거와 한계가 필요하다. 지정 검토자 신원은 아직 기록하지 않았으며 임의의 canonical verifier를 만들지 않는다. 이 자료 준비는 외부 전달·Claude 반입 완료가 아니다.

## 다음 자료와 작업

| 구분 | 구체 자료·다음 작업 | 완료를 뜻하지 않는 것 |
| --- | --- | --- |
| 외부 설계 검토 | 위 고정 문서·영수증과 새 표지 종결 기록을 함께 검토하고 범위별 판정을 기록 | 이미 비준된 결정을 재승인받거나 물리 GO를 대신하지 않음 |
| P2 인터페이스 | 실제 bed/arm·params·활성 머리, h0 기준/환산/정수 step화, 시간 정의·중력 예외·개발 사례·resume 상태 전이 원문 수령 후 계약 대조 | P1 이름/값을 P2 등록으로 복사하지 않음 |
| R-a/S0 | 생산자 덱·바이너리·run 신원, 고정판 R-a 완료 step, 원자/상/질량 재고 및 atom/contact/wall/mesh/restart/state·fix 이력/hash 연결 | 서보 정지 즉시를 R-a 완료/S0로 간주하지 않음 |
| 실제 자격 | 지정 바이너리 문법·이력 음성 대조, T10 같은 시간 dt/2, T11, 실제 T12 복원/판독/관문, T13 재개 증거가 제공되면 항목별 검토 | 합성 52 또는 외부 208건으로 실제 실행 자격을 닫지 않음 |
| Q7–Q9 측정 | 세 펠릿 질량·직경·두께·불확도/상태, 랩 기준 원기록·공극률 정의, 하중/탈형/EIS 상태·이력/시각 수령 | 1.64 또는 10–13%에 맞춰 측정값 추정하지 않음 |
| Claude 통합 | 추후 실제 통합 대상·합친 파일을 대조하고 직접 검사/공유 CI 연결 여부를 확인 | 현재 source head 관찰을 merge·통합 트리 PASS로 해석하지 않음 |

[기존 빈 사실 양식](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/2b4b40ea5e375659bfad8243c1ccb6fe0ef2853f/docs/reviews/dem_gen2_t12_consumer_contract_evidence_20261024/factual-input-form.blank.json)은 그대로 보존한다. 원기록은 원래 형식으로 받을 수 있으며 양식을 먼저 완성하는 절차를 추가하지 않는다. 좁은 표지 GO를 `unloading_go_report_path/hash` 같은 범용 GO 칸에 넣지 않는다. 실행 가능한 P2 생산기·등록이 없는 상태에서 물리 발사 명령을 제시하지 않는다.
