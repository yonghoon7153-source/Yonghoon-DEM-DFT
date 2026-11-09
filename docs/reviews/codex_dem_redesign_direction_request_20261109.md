# Codex 반박 리뷰 요청 — [DEM 우선 (수영)] 방향 메모 3.1 판: 가압부터 탈압까지 한 모델로 (2026-11-09 · 발송 = 1저자)

> **한 줄**: 11-09 주간보고 피드백 (DEM 에서 MPM 으로 넘기는 지금 방식은 후처리다 · 가압부터 탈압까지 한 모델이 AM 과 SE 를 다 계산해야 한다) 에 따라 새로 연 트랙 [DEM 우선 (수영)] 의 방향 메모를 반박 리뷰해 주십시오.  메모는 결과 0 건 · 새 계산 0 건 · 실행 GO 요청이 아닙니다.  묻는 것은 방향 (단계 0–3 의 설계 · 갈림 규칙 · 단위 시험 · 단계 4 의 판정 꼴) 이 기록 · 카드 · 코드와 맞는지, 갈림 표가 닫혀 있는지입니다.
> **리뷰 핀** = 이 요청서가 든 커밋 (작업 가지 B `claude/sdcp-dem-manuscript-si-pqwtv8` · push · stoic `claude/stoic-knuth-NObVQ` = 복귀 전까지 `6a81f0c55` 동결) · 번호 = ZIP 의 PIN.txt.  문헌 카드는 litdb 정본 가지 `claude/friendly-meitner-lldvar` 의 `099116169` 에서 가져온 사본입니다 (PIN.txt 둘째 줄).
> **1저자** — 11-09 밤 *"날 설득시키는 파이프라인이랑 codex 반박 리뷰등을 통해서 한번 방향성 잡아보자"* · 이미 정한 것 (다시 열지 않음) = 진행 기록 1413–1414 행 (랩 표준 공극 10–13 % · 진밀도 1.64 g/cm³ · 질량 기준 · 두 트랙 따로 · 이 트랙은 MPM 기공률이 주 출력 · 느슨한 출발 · 질량 보존 심기 · MPM 재료값은 같은 기준에 따로 · 상용 FE 없음 · 문헌 = 1저자가 준 PDF 7 편).

## 0. 이번에 닫는 것 / 닫지 않는 것

| 이번에 닫으려는 것 (판정 요청) | 닫지 않는 것 (이 회차 범위 밖) |
|---|---|
| ① 방향: 단계 0–3 (등록 · 셈 · 2D 코드와 단위 시험 · 2D 벤치마크) 의 설계가 기록 · 카드 · 코드와 맞는가 | 수치 문턱의 값 (전부 [제안 · 봉인 전]) · 등록 · 봉인 |
| ② 갈림 규칙: 2D 벤치마크의 등급 · 점 묶기 · 충전 · 해상도 · 미도달 · F 정합 · 덧규칙이 모든 결과를 정확히 한 갈림으로 보내는가 (§0 표 = §4 표) | 3D 비용 · A′ 구현 · 단계 4–7 의 결과 |
| ③ 단위 시험 U0–U6 이 입자별 장 (F) 의 본체를 시험하고, 단계 3 문과 단계 6 (탈압) 문이 맞게 나뉘었는가 | 랩 기준의 측정 상태 (다이 안 · 밖) · 복합 펠릿의 외부 기준 |
| ④ 단계 4 (3D 순수 SE) 의 판정 꼴: σ_y 훑기 · 가로지름 · σ_y* 정의 · 자격 | 단계 5 의 판정 (따로 등록) · 실행 승인 |
| ⑤ 우리 코드 판독 (얼린 AM · 판 · 벽 경계 · 항복 판정 · 응력 식) 과 일축 항복 환산값 | 1저자 질문 Q1 · Q2 의 답 |

## 1. 보내는 것 (ZIP · repo/ = 리뷰 핀 blob 그대로 · litdb/ = 정본 가지 `099116169` blob 그대로 · PIN.txt · SHA256SUMS)

| 묶음 | 파일 |
|---|---|
| 이 요청서 | `docs/reviews/codex_dem_redesign_direction_request_20261109.md` |
| 메모와 이력 (판정 대상 = memo_v3_1.md) | `docs/reviews/dem_redesign_direction_20261109/` (memo_v1 · preattack1_on_v1 · memo_v2 · changelog_v2 · preattack2_on_v2 · memo_v3 · changelog_v3 · preattack3_on_v3 · memo_v3_1 · changelog_v3_1) |
| 메모가 인용하는 리포 기록 | `CLAUDE.md` · `docs/session_20260923_progress.md` · `docs/reviews/dem_mpm_one_way_sequential_definition_20261109.md` · `docs/reviews/fam_platen_prereg_20260812.md` · `docs/reviews/dem_protocol_gen2_plan_draft_20261014.md` · `docs/mpm3d_calibration.md` · `docs/mpm_dpc_cap_crosscheck.md` · `docs/reviews/dem_unloading_ps45_prereg_20261009.md` · `docs/reviews/mpm_coverage_interface_design_memo_20261103.md` · `docs/data/se_pellet_eis_20261026/README.md` · `docs/data/real14_se_scaffold.csv` · `docs/data/real14_am_scaffold.csv` · `docs/reviews/findings.json` |
| 메모가 판독한 코드 | `scripts/mpm3d_compaction.py` · `scripts/mpm_dem_match.py` · `scripts/dem3d_plastic.py` |
| 문헌 카드 (litdb/) | 1저자가 준 7 편 (Bardenhagen 2000 · 2001 · Nezamabadi 2022 · Nguyen 2017 · Cárdenas-Barrantes 2020 · 2021 · 2022) + 메모가 인용하는 다른 카드 (ZIP 의 litdb/ 목록) |

## 2. 무엇을 거쳤나

- 메모 1 판 → 독립 사전 공격 37 건 → 2 판 (고침 30 · 한정 6 · 기각 1 = 11-09 결정과 충돌) → 독립 재공격 (P1 3 · P2 14 · P3 20) → 3 판 → 좁은 재확인 (P1 0 · P2 4 · P3 14 · 갈림 표 256 조합 나열 = 모두 한 갈림) → 3.1 판 (18 건 모두 고침 · 그중 넷은 재확인의 제안과 다른 방식 · 남는 한정 다섯은 메모의 해당 자리에 적음 · 3.1 판 규칙을 그대로 코드로 옮겨 단계 3 의 131,072 조합 · 단계 4 의 16 조합을 돌려 모두 한 갈림으로 가는 것을 확인 = changelog_v3_1 에만 적음 · 메모의 판정 근거 아님).  처분 = 각 changelog.
- 재공격이 메인 세션의 판독 오류 하나를 잡았다: 일축 항복 환산을 √(3/2)·σ_y 로 적었는데, 응력이 fixed-corotated 이고 항복 판정만 Hencky 편차 변형이라 생산 연화 재료에서는 맞지 않는다 (σ_y 0.30 에서 압축 0.318 · 인장 0.454 GPa).  원장 `SELF-160` · litdb 정본은 `099116169` 에서 제자리 정정.
- 코드 변경 0 · 런 0.

## 3. 질문

메모 3.1 판 §7 의 질문 전부에 답해 주십시오.  특히 셋을 먼저 봐 주십시오.

| # | 질문 |
|---|---|
| Q1 | 단계 3 의 S/F 판정 (같은 2D 코드 · 같은 출발 충전 · 정한 수의 충전 · 마찰 팔) 이 "한 속도장이 주원인인가" 를 실제로 가르는가.  2D · 암시적 ↔ 명시 · CD ↔ Bardenhagen · neo-Hookean ↔ Hencky · 등방 ↔ 일축 차이가 판정을 뒤집을 수 있는가. |
| Q2 | 갈림 표가 닫혀 있는가.  두 갈림으로 가거나 아무 데도 안 가는 조합, 결과를 본 뒤 등급을 옮길 수 있는 틈 (충전 추가 · 해상도 · 미도달 처리) 이 남았는가. |
| Q3 | 이 방향 전체가 1저자의 11-09 결정 (MPM 기공률 주 출력 · 느슨한 출발 · 질량 보존 심기 · 따로 보정) 과 frame [4] (모델끼리 맞추지 않음) 를 지키는가.  순환 (씨앗이 답을 품음 · 옛 MPM 보정값 계보) 이 남은 곳이 있는가. |

## 4. 사전 점검 (보내기 전)

- 독립 사전 공격 세 번 (위 §2) · 메모의 숫자 · 코드 줄 번호 = 핀의 파일과 대조 (각 공격 보고서 §4 · §2).
- `docs/reviews/claims.json` `quotation_ban` 42 패턴 = 메모 · 공격 보고서 · changelog 에서 적중 0.
- 코드 변경이 없어 CLAUDE.md 사전 공격 ② (바뀐 함수의 HOLD 부류) · 변이 시험은 해당 없음.
