# Rint ② 설계 v1 · 등록 R 초안 · Codex 요청서 — 사전 공격 리뷰 (Codex 대역 · 읽기 전용 · 10-20)

너는 Codex 를 대신하는 **적대 설계 검토자**다.  목표 = 이 설계 요청서가 Codex 에 가면 HOLD 를 받을 자리를 **먼저** 찾는 것.  작성자 설명은 주지 않는다 — 문서 · 코드 · 지난 판정문만 보고 판단한다.

## 대상
- 커밋 `b694369b5` (부모 `f507bdc74` · 로컬 · 원격에 아직 없음): `docs/reviews/rint_carbon_additive_design_v1_20261020.md` · `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` · `docs/reviews/codex_rint_carbon_additive_design_request_20261020.md`.
- 작업 자리: `git -C /home/user/Yonghoon-DEM-DFT worktree add --detach /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/wt_prerev2_attack b694369b5` · 끝나면 `git -C /home/user/Yonghoon-DEM-DFT worktree remove --force <그 경로>`.  임시 파일 = `…/scratchpad/prerev2_attack/` 만 · **큰 사본을 만들지 말고 끝나면 지운다 (디스크 여유가 작다)**.
- 1저자 결정: `docs/reviews/rint_carbon_additive_plan_20261020.md` §2 (Q1–Q12 권고대로 · 머리의 두 보탬) · `docs/reviews/rimprr_fix_plan_20261020.md` Q6 (나).
- Codex 가 지난번 이 분야에서 낸 판정 (이 꼴로 읽어라): `docs/reviews/codex_r18_verdict_20260831.md` (PTFE A · B 기각 이유 · Q6 face 연산자) · `docs/reviews/codex_review_rint_g2_design_20261006.md` (RINTG-01–10: 순서 불변 ↔ OFF 보존 충돌 · 총량 정규화 ≠ 국소 막 연산자 · 문서식 단위 25 배 · 희석 극한이 막 삭제 오답도 통과 · 고정 ↔ 1.2h 브리지 혼동 · 결과 전 · 후 문장 공존) · `docs/reviews/codex_review_rint_g2_v3_20261007.md` (RINTV-01–03: ε 동률 비추이 · 동결 마스크 반올림 · β↔q 분리) · `docs/reviews/codex_review_rint_g2_impl_20261014.md` · `docs/reviews/codex_review_rint_g2_impl_fix_recheck_20261015.md` · `docs/reviews/codex_review_rint_join_rimpr_q7_recheck_20261020.md` · 원장 `docs/reviews/findings.json` 의 `RINT*` · `RIMP*` · `L214*` (증서 결합 · 판본 · 세대 부류).
- 코드 (설계가 붙을 자리 · 읽기만): `scripts/step3_sigma.py` · `scripts/rint_iface_join.py` · `scripts/sdcp_gain_vox015_8arm.sh` · `scripts/sdcp_anchor_v2_chain.py`.

## 할 일 — 찾은 것마다 (자리 · 왜 HOLD 인가 · Codex 예상 등급 · 최소 수정 또는 한정 문안)
1. **식별성 · 순환**: 손잡이 표의 모든 매개변수가 실제로 한 범주에만 있는가 · SBE 한 점으로 둘 이상이 정해지는 숨은 길 (예: 문턱 · α · c 를 σ 본 뒤 고를 수 있는 틈 · "S0 분포를 보고 고정" 의 시점 증명 방법) · 네 모서리 재보정이 정말 모서리마다 손잡이 하나인지 · 보정 사다리가 단조 · 유일해를 보장하는지 (해가 없거나 둘이면?).
2. **holdout**: 4.68 사용 이력 선언이 충분한가 · 정보량 등급 (G0 = ln(4.68/1.8877)) 정의가 판정을 쉽게 통과하게 만들지 않는가 · 영 모형 대비 점수 정의 · 불합격 · 무정보 처리 · 결과 뒤 바꿀 수 있는 자리가 남았는가.
3. **이중 계상 · 표현**: `face_alpha` ↔ centerline · off 격자 동일 조건이 실제 코드 경로로 강제 가능한가 · SDCP 부피 스탬프 ↔ S3 막 · 탄소 '자르기' 인공물 · 브리지 0.48 (고정 vs 1.2h · RINTG-05 부류) · 주기 seam.
4. **연산자 수학**: S1 면 개구율 `G = α·G0` 의 정의역 (α 계산 기하 · 캡슐 교차 · 한 면에 여러 피브릴 · 겹침 합 > 1) · 상호성 · KCL · 단위 (RINTG-03 부류 — 식마다 차원 확인) · S2 R_j 간선의 조립 (교차 셀 멤버십 dof · 융합 면 절단 · 실제 그래프 가지치기) — 같은 접합을 두 번 세거나 빠뜨리는 꼴 · 순서 · 동률 · 반올림 (RINTV-01 · 02 부류) · c = 1 "정확한 축약" 주장이 수학적으로 맞는가.
5. **시험 판별력**: 설계가 적은 "먼저 쓸 시험" 이 오답 구현을 실제로 떨어뜨리는가 (RINTG-04 부류 — 희석 극한처럼 오답도 통과하는 시험) · no-op · 비트 동일 주장 범위 · 펠릿 9:1 시험이 v0 에서 no-op 이라 판별력 없음을 적었다는데 그럼 무엇이 지키나.
6. **수렴 · 수치**: σ 대비 1.9e6 · 증서 셋 (CG info 0 · 판 전류 균형 · rtol 재풀이) 이 미수렴을 놓치는 꼴 · NaN · inf · 빈 · 중복 (지난 HOLD 부류).
7. **세대 · 영수증 · 판본**: `ca_ext` · `p3ca-` 접두 · 끄면 매니페스트 바이트 같음 주장 · 옛 세대와 섞기 거부가 소비자 (판정기 · 인계 · 웹앱) 전부에서 강제되는가 · 다른 판본 증서를 받는 틈.
8. **요청서 자체**: "닫는 것 / 닫지 않는 것" 이 정확한가 · 질문 A1–A20 이 Codex 가 답할 수 있는 꼴인가 · 결과 전 · 후 문장 공존 (RINTG-06 부류) · 범위 과장.

## 규칙
- **리포 · 다른 작업 트리를 고치지 않는다 · 커밋 · push 안 함 · `scripts/check_all.sh` 안 돌림.**  필요하면 작은 수치 탐침 (스크래치 · 몇 초) 은 돌려도 된다 — 큰 침대 사본 금지.
- 다른 게이트가 돈다 — CPU · 디스크 적게.
- 보고 (한국어 · 표 중심 · 짧게): ① 찾은 것 표 (번호 · 자리 (파일:줄) · 무엇 · Codex 예상 등급 · 최소 수정 / 한정 문안) ② "보내기 전 반드시 고칠 것" · "한정으로 적으면 될 것" 두 목록 ③ 1저자에게 물어야 할 새 결정이 생기면 (권고 한 줄).
