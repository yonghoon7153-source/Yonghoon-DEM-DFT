# 수영 단계 3 갈림 메모 · 1저자 결정용 · 2026-11-25

① 지금 관문　설정 ② U6(b)의 같은 충전율 압력비와 U6(c) ⑥의 역사 판정을 함께 정리했다. 한 쪽 정본은 docs/reviews/suyoung_stage3_fork_20261125/decision.md 에 있다.

② 결과　기존 S·F 네 격자 자료에서 Φ_m 0.84·0.90은 모두 도달했으나 두 팔 모두 A·B가 성립하지 않는다. ⑥의 원 F 두 쌍은 79.25%·19.25%로 5%를 넘었다. 새 가압·현장 실행·새 연구 결과는 0건이다.

③ 다음 한 걸음　1저자가 후속 **2D 전용** 개정안 비준 여부를 정한다. 비준 전에는 현행 U6(c) 중단 규칙이 적용된다. 비준하는 경우에도 Q13의 두 팔 비용 수용과 발사는 별도이며, 미수렴이면 구간 미확정으로 보고한다. 원 메모, 규칙 파일, 판정 원장과 주간보고 문단은 원 담당자가 관리한다.

## 근거와 기존 기록 검산

설정 ②의 1저자 반환 TAR 두 개를 기존 docs/reviews/suyoung_u6b_return_20261123/verify_return.py 로 다시 읽었다. 원곡선 8개의 해시·세 목표 × 두 팔의 압력 행 6개·영수증의 모든 필드가 일치했다(실수는 상대 1e−12, 절대 1e−15로 대조). 24칸 S/F는 각각 1.0384928381, 1.0087910256이었다.

- 정의·입구는 docs/reviews/dem_redesign_direction_20261109/memo_v3_2.md §3-2, §4 단계 0·2·3, §7 Q13, 부록 D-1이다. 현행 U6(b)는 양팔의 수렴 조건이 성립하지 않으면 단계 3 전에 보고하도록 한다. 본 제안은 후속 자료에서 2D 조밀 U6(c) ⑥의 단계 3 진입 효력만 옮기는 동시에 U6(b) 구간 산출을 명시적 조건으로 둔다. 독립된 U5(c)의 ⑥, U6(c) 나머지 일곱 의무, 단계 4의 3D 문은 유지한다. 36칸·단계 3·3D는 현재 보류다.
- docs/reviews/suyoung_u6a_setting2_return_20261123/weekly_u6a.md 및 docs/reviews/suyoung_u6b_return_20261123/u6b_targets.tsv 의 압력을 docs/reviews/suyoung_u6b_return_20261123/receipt.json 과 대조했다. d₁·d₂는 12→16·16→24칸의 자연로그 압력 변화다. 0.84에서 S (−0.03933, −0.16741), F (−0.05174, −0.15735), 0.90에서 S (+0.00582, −0.08329), F (+0.00326, −0.08141)이다. A는 같은 부호와 변화비, B는 작은 변화와 부호 규칙을 요구한다. 모든 |d₂|가 τ=0.02를 넘으므로 현재 B와 올린 사다리의 B는 모두 배제된다. 두 점 모두 같은 24칸에서 단순 S/F를 나눈 값은 방향을 설명하는 데만 썼다. 0.95는 기존 8칸 두 팔이 상한에 먼저 닿았고, Q13 개정 사다리를 쓰게 되면 새 네 단의 공통 도달 여부부터 같은 규칙으로 다시 본다.
- 부족한 팔의 근거는 docs/reviews/suyoung_u6b_setting2_20261123/README.md 및 docs/data/suyoung_q13_return_20261122/S36_result.json 과 docs/data/suyoung_q13_return_20261122/F36_result.json 이다. 이전 36칸은 모두 설정 ①이며 기존 S 아래판은 현재의 단일장 결합 벽 조건과 다르다. 현재 설정 ②의 24칸 실측 S 4,426초·F 3,003초에 (36/24)³을 곱하면 S 약 4시간 9분·F 약 2시간 49분, 한 CPU에서 순차 약 7시간이다. 원 Q13의 3.29배는 단계 3 판정 사다리 전체의 비용비다.
- S 대조·접촉 후보는 docs/reviews/suyoung_setting2_contact_20261124/diagnosis.md 및 docs/reviews/suyoung_grid_diagnosis_20261124/common_support_result.md, 속도 대조는 docs/reviews/suyoung_speed_ladder_20261123/pressure_ladder.json 에 있다. 공통 구간·기존 분모에서 후보 변화는 −2.48·−4.23%p였다. 8↔16에서 실제 종료 구간을 반영하면 부호가 돌아선다. 기존의 변위 대조를 반복하지 않았다. F32·F48 기록은 먼저 반입한 ㊵의 docs/reviews/suyoung_higher_grid_return_20261125/README.md 를 함께 읽는다.
- U6(c) 의무는 docs/reviews/suyoung_u6c_development_20261121/README.md 및 docs/reviews/suyoung_u6c_f8_review_receipt_20261122/README.md 와 비교했다. 과거 설정 ①의 일부 걸음 다물체 표본·번호 순열은 설정 ②의 전 항목 위반 수·분모 영수증을 대신하지 못한다. 등록 누락/관측 누락은 보류, 등록 허용폭 초과는 불합격이다. U7은 강체–소성·소성–소성 두 배치 모두 가압을 유지하며, F와 늘-붙음 F의 차이가 작으면 등록된 옆밀기 거리를 한 번만 두 배로 한다. U8은 단위 질량, 판 −1·노드 −2인 예에서 일방향은 속도 −2/충격량 0, 양방향은 −1/−1이고 조밀 입력의 같은 충전율 반력도 보고한다. docs/reviews/suyoung_shape_cycle_20261120/README.md 는 판 상승 시험이며 scripts/test_suyoung_u6_first_dev.py 는 일방향 벽 단위 시험을 담는다. 이 자료에서 정식 U7·U8 통과 기록은 확인되지 않았다. 단계 3 설계는 docs/reviews/suyoung_stage3_section_plan_20261123/stage3_section_plan.md 를 따른다.
- 한 충전의 점비를 단계 3 ‘같음/다름’으로 승격하지 않는다. 단계 3에서는 독립 충전 셋과 등록한 F(마찰 0) 문헌 띠를 함께 판독한다. 단계 2에서 미확정이 지속되면 적용 조건과 모형 대안을 1저자에게 돌린다. 입자별 유한요소는 작은 상자 검산부터라는 원 메모 §3-2의 대안이다.

## 반입

가지 codex/suyoung-stage3-fork-1125 · 바탕 7b208b19c (작성 직전 fetch한 stoic 원격 추적 끝). 반입 ㊵·㊶이 준비된 점은 1저자 확인을 따랐다. 순서와 stable patch-id는 전달 ZIP의 HANDOFF.md 에 있다. 공유 기록 제안은 “수영 설정 ②의 0.84·0.90에서 양팔 격자 구간 미확정, ⑥ 미통과 유지. 단계 3 격자 조건 개정은 결과 확인 뒤 작성한 1저자 비준 전 초안”이다.
