# 묶음 A′ — 사전 공격 리뷰 C1–C5 고치기 (Rint ② RR · 10-23 · 1저자 *"권고대로 해"* = Q12–Q16 전부 (가))

## 비준 (1저자 10-23)
- Q12 (가) C1 을 Codex 회차 ① 전에 고친다 (C2 · C4 와 함께 · 에이전트 하나 · 시험 먼저).
- Q13 (가) C3 — R 단조 검사를 origin 마다로 넓힌다 (이미 구한 값 · 추가 풀이 없음).
- Q14 (가) C5 — SV 끊기 정의 이름 (kind · rule) 을 등록값에 묶는다 (옛 이름 쓰는 시험 고정물 3 곳 고침).
- (Q15 · Q16 = Q9 설계 문서 몫 · 메인이 한다 · 너는 손대지 않는다.)

## 입력 (먼저 다 읽는다)
- 사전 공격 리뷰 `docs/reviews/rint2_rr_fix_evidence_20261023/preattack/PREATTACK_A.md` (§A C1–C5 · §B) · 탐침 `docs/reviews/rint2_rr_fix_evidence_20261023/preattack/tools/` (`atk_sv.py` · `atk_edges.py` · `atk_m7.py` · `atk_divdir.py` · `atk_rmono.py` · `atk_rmono2.py`) · 메인 재확인 `docs/reviews/rint2_rr_fix_evidence_20261023/preattack/README.md`.
- 지난 묶음 지시서 `docs/reviews/rint2_rr_fix_evidence_20261023/BRIEF.md` (§작업 트리 · 커밋 · §보고 · §규칙 = 그대로 따른다) · 묶음 A 보고 `docs/reviews/rint2_rr_fix_evidence_20261023/REPORT_A.md` (회귀 목록 · 끈 경로 · 변이 · 탐침 재실행 방법).
- Codex 판정문 `docs/reviews/codex_review_rint2_rereview_20261022.md` §4 RCA2-04 · §8 (DBE R 단조) · §9.
- 등록 R `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` §5-6 SV 행 · §5-6a · §10 멈춤 목록 · Q8 관련 줄.
- 원장 `docs/reviews/findings.json` RCA2-01 · 04 · 09.

## 작업 트리 · 커밋
- 시작 SHA = `fdb48d378` · 가지 이름 = `rr-fix-a2`.  `git rev-parse HEAD` 가 다르면 `git checkout -B rr-fix-a2 fdb48d378`.
- 항목마다 시험 먼저 (고치기 전 판에서 실패 확인) → 구현 → 커밋 하나.  커밋 메시지에 `author 10-23 ratified Q12-Q16` + BRIEF 의 끝 두 줄.
- 메인은 네 가지를 fast-forward 로 받는다 (SHA 그대로).

## A7. C1 (P2 · Q12 (가)) — 끝 증서를 끊은 그래프에 묶는다
- 문제: `scripts/ca_ext_svcf.py` `_pos_cert_problem` (끝 ↔ 증서 결합 = `I_bot == G` 하나) · `_cert_problem` 끝 반복 (런 단위 `BIND_FIELDS` 만).  같은 런의 주 해 증서를 끝 자리에 복사하고 G_cut = G_full · 비 1 · 판정 근거 칸을 다시 세면 `sv_cf_problem` · `read_run` 둘 다 통과 → 거짓 clear (`atk_sv.py` A2).
- 고침: 증서 자신의 위상 수 (`target_n_edges` · `target_n_dof` · `target_n_plate_bot` · `target_n_plate_top` 중 증서에 있는 것) 를 투영하고, 끝마다 주 해 증서 · 기록의 끊은 수와 대조한다.
  - 생산자 (`scripts/carbon_junction.py` 의 아래 끝 · 위 끝 그래프 만들기 · 떠 있는 성분 버림) 를 읽어 **생산자가 보장하는 정확한 관계**를 찾는다 — 등식은 생산자가 보장할 때만 · 아니면 부등식.  참고 실측 (리뷰): SVX 주 44 · 아래 42 = 44 − `n_sv_faces_cut` 2 · QD2-3 위 16 ≤ 23 − `n_edges_cut` 6 · 다섯째 rail 위 32 = 44 − 12 · 끊은 것 없음 = 주와 같음.
  - 핵심 조건: 무엇이든 끊었으면 그 끝 증서의 그래프는 주 해 증서보다 작아야 한다 (같은 수 = 거부) · 끊은 것이 없으면 같아야 한다.
  - 끊은 수 칸까지 함께 고친 편집 (예: 바꿔 끼우며 `n_sv_faces_cut` 를 0 으로) 도 잡을 수 있는지 본다 — census 등 기록 안의 독립 출처가 있으면 묶는다.  독립 출처가 없으면 고르지 말고 "결정 필요" 로 보고한다.
- 시험 먼저: A2 (아래 끝 바꿔 끼우기) · 위 끝 바꿔 끼우기 · 위 끝이 있는 기록의 아래 끝 바꿔 끼우기 · 끊은 수까지 고친 꼴 → 거부 (자기 사유 문장) · 모든 기존 생산자 기록 (SVX · QD2-1 · QD2-2 · QD2-3 · QD4 · 다섯째 rail · 진단 기록 · census 불일치 꼴) → 계약 None 그대로.
- 문서: 등록 R §5-6 SV 행의 계약 문장 · `_pos_cert_problem` 주석 · 모듈 머리.

## A8. C2 (P3 · 시험만) — 방향 반올림 칼날을 상주 회귀로
- `_div_dir` 코드는 맞다.  실제 증서 기록 (SVX nu 0 · QD2-3 위 끝 유한) 에서 t = 정확한 위 몫 U 이하의 가장 큰 float 이면 사슬 = `SV_UNCHECKED` (표지 없음 아님) · t = 정확한 아래 몫 L 이상의 가장 작은 float 이면 `SV_DEPENDENT` 아님 (`atk_m7.py` 꼴 · 정확 몫 = `Fraction`).
- 변이 M7 (방향 맞바꿈) · M1 (그냥 a/b) 이 새 시험에 걸려야 한다 (리뷰: 지금 시험은 M7 에서 전부 통과).

## A9. C3 (P3 · Q13 (가)) — R 단조 검사를 origin 마다
- 지금 `Predict._r_monotone` = 최종 추정량 (arm 0 또는 8 팔 평균) 만.  더한다: 같은 모서리의 이미 구한 origin 마다 (arm 0 · arm 1 · 2 = 모든 모서리 · 8 origin = 넘친 모서리) 세 R 의 증서 구간 단조.  최종 추정량 검사는 그대로 둔다.
- 새 숫자 · 추가 풀이 없음 · 멈춤 이름 그대로 `R_MONOTONE_VIOLATION` (사유에 origin 이름) · `checks['r_monotone']` 에 origin 칸 · 판정 단계의 다시 계산이 같은 검사를 다시 낸다.
- 시험 먼저: 리뷰 R1 (넘침 없는 모서리 arm 1 비단조) · R1c (넘친 모서리의 arm 0 비단조) · R1d (넘친 모서리의 origin 3 비단조) → 멈춤 · 정상 · 띠 안 비단조 · 평탄 → 통과.
- 문서: 등록 R 의 Q8 행 · §10 멈춤 목록 문장 (같은 origin = origin 마다 + 최종 추정량).

## A10. C4 (P3) — 단조 띠 = 증서 구간 그 자체
- 지금 `arm_band` = [σ(1 − e), σ(1 + e)] (e = float `err_rel`) — 증서 구간보다 좁을 수 있어, 구간이 한 점에서 맞닿는 칼날에서 거짓 멈춤 (`atk_rmono.py` R2).  주석 "정확 분수 끝" 과 등록 문장 "증서 구간끼리 · 모순일 때만 멈춤" 이 성립하게, 팔 기록이 가진 증서의 목표량 구간 (`target_lo` · `target_hi` 를 σ 로 옮긴 정확 분수) 을 직접 쓴다.  팔 기록에 그 칸이 없으면 `read_run` 이 증서에서 같이 옮겨 싣는다 (게시 값 · 판정 함수는 그대로).
- 시험 먼저: R2 (맞닿음) → 멈춤 없음 · 떨어짐 → 멈춤 · 8 팔 평균 띠 · 영값 · err 없음 꼴.

## A11. C5 (P3 · Q14 (가)) — kind · rule 을 등록값에 묶는다
- 지금 `sv_cf_problem` 은 kind 접두어만 본다 (`ca_ext_svcf.py:224`) · `rule` 은 투영 (`_COPY`) 에서 빠진다.  고침: kind = `carbon_junction.CJUNC_SV_CF_KIND` · rule = `CJUNC_SV_CF_RULE` 만 받는다 (검증기 상수 = 생산자 상수 · 시험이 대조 · S8q 꼴) · 투영이 rule 을 옮긴다 · 다른 값 = 자기 사유 문장으로 거부.  검증기는 여전히 끊는 면의 뜻에 기대지 않는다 (이름 대조뿐) — 모듈 머리 문장을 그만큼 고친다.
- 옛 이름 `counterfactual_cut_sv_faces` 를 쓰는 시험 고정물 3 곳 (`scripts/test_ca_ext_b6.py:729` · `scripts/test_rint_r_chain.py:256` · `:2388` 근처) 을 등록 이름으로 바꾸고, 옛 이름 기록 = 거부 시험을 더한다.
- 문서: 등록 R §5-6 SV 행.

## A12. 원장 · 회귀 · 보고
- 원장: RCA2-04 (C1 · C5) · RCA2-09 (C3 · C4) = note 끝에 "★ 10-23 사전 공격 리뷰 (`docs/reviews/rint2_rr_fix_evidence_20261023/preattack/PREATTACK_A.md`) C… 고침 `<sha>`" + evidence_tests 더함 + claimed_fixed_sha = 새 고침 커밋 · RCA2-01 (C2) = evidence_tests 만 더함.  새 ID 없음.
- 웹앱: 화면 문구가 바뀌는 자리가 있으면 같은 묶음 (SV 줄 · 설명 페이지 · 시험 먼저) · 없으면 "웹앱 해당 화면 없음" 을 보고.
- 회귀 · 끈 경로 · 변이 · 탐침 재실행 = 묶음 A 의 A6 와 같다 (`REPORT_A.md` §3 · §4 · §5 · §6).  끈 경로의 "고치기 전" = `fdb48d378`.  리뷰 탐침 재실행: `atk_sv.py` (A1 다섯 = 계약 None 그대로 · A2 = 거부 · A4 kind · rule = 거부) · `atk_rmono.py` · `atk_rmono2.py` (R1 · R1c · R1d = 멈춤 · R2 = 멈춤 없음).
- 등록 R 머리 줄에 "10-23 묶음 A′ (사전 공격 리뷰 C1–C5 · 1저자 Q12–Q14 (가))" 를 덧붙인다.
- `S0_SAME_FILES` (`scripts/rint_r_chain.py:161`) 일곱 중 바뀐 파일을 보고한다.
- 보고 = BRIEF §보고 그대로 (마지막 메시지 · 표 위주 · 메인이 `REPORT_A2.md` 로 옮겨 적는다 · 결정 필요 목록 포함).
- 규칙 = BRIEF §규칙 그대로 (python `-I` · `nice -n 19` · BLAS 스레드 1 · push · fetch · `scripts/check_all.sh` 금지 · 봉인 32 파일 손대지 않음 · 등록에 없는 새 규칙 · 숫자 금지 (Q12–Q14 (가) 범위만) · 숫자 · 전칭은 실행 출력으로만 · 도달 못 하는 SHA 금지 · 커밋마다 `python3 scripts/check_doc_refs.py` · `python3 scripts/check_review_findings.py` rc 0 · 사본은 다 쓴 뒤 지움).
