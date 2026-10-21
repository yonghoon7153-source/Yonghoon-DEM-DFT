# Rint ② (탄소 접합 + 첨가제 물리) — 설계 v1 · 등록 R 초안 · Codex 설계 리뷰 요청서 초안 (문서만 · 10-20)

## 기반
- `git reset --hard tmp-rq7-int` (로컬 가지 · `f507bdc74`) → `git log -3 --oneline` 확인.  `git fetch` 하지 않는다.
- 1저자 결정: 통합 계획 v1 `docs/reviews/rint_carbon_additive_plan_20261020.md` §2 = **Q1–Q12 권고대로** (§2 머리의 두 보탬 포함 — Q1 DBE 4.68 holdout 한정어 · Q12 조인 수정 재확인 같은 회차).  근거 초안 둘: `docs/reviews/rint_carbon_junction_brief_20261020.md` (S2 v0 설계 §3 · Codex 질문 초안 §6) · `docs/reviews/additive_physics_brief_20261020.md` (P1 PTFE · P3 SDCP · P6 표현 회계 · 부록 A 정본 카드 값).
- 꼭 읽을 교훈 (지난 HOLD): Codex R18 `docs/reviews/codex_r18_verdict_20260831.md` (PTFE A · B 기각 · **Q6 보존형 capsule face 연산자** 권고 · 종료조건) · PTFE 규약 `docs/reviews/ptfe_convention_prereg_20260829.md` (`CL-60` centerline) · Rint G2 판정문 `docs/reviews/codex_review_rint_g2_design_20261006.md` · `docs/reviews/codex_review_rint_g2_v3_20261007.md` · `docs/reviews/codex_review_rint_g2_impl_20261014.md` · `docs/reviews/codex_review_rint_g2_impl_fix_recheck_20261015.md` · `docs/reviews/codex_review_rint_join_rimpr_q7_recheck_20261020.md` (원장 `RINTG-*` · `RINTV-*` · `RIMP-*` · `RIMPR-*`) · 설계 정본 `docs/reviews/contact_resistance_pipeline_draft_v2_20261006.md` · `…_v3_20261006.md` · `…_v3_1_20261007.md` · SDCP 등록 v2 `docs/reviews/sdcp_sigma_e_dcp_anchor_registration_v2_20261019.md` (S2 사다리 규칙 · §7 결과) · 복셀 σ 지위 `docs/voxel_contact_free_gap.md` (`CL-81`).
- 코드 (읽기만 · 붙을 자리 확인): `scripts/step3_sigma.py` (`solve_sigma_z` · `am_iface_ledger` · `am_iface_plan` · PTFE centerline 스탬프 · SDCP 구 스탬프 · fibre 처리 · 매니페스트 · `physics_protocol_id`) · `scripts/rint_iface_join.py` · `scripts/sdcp_gain_vox015_8arm.sh` · 웹앱에서 이 값들을 보여 주는 자리 (grep).

## 만들 것 (새 문서 셋 · 커밋 하나)
1. **설계 v1** `docs/reviews/rint_carbon_additive_design_v1_20261020.md` — 단계마다 (S0 · S1 · S2 v0 · S3) ① 식 · 단위 ② 입력 · 출력 · 스위치 (전부 기본 끔 · 끄면 비트 동일) ③ 계약 (불변식 · 거부 조건 · 영수증 결합 — 지난 HOLD 부류: NaN · inf · 넘침 · 빈 · 중복 · 검사 전 정규화 · 증서 ↔ 결과 결합 · 다른 판본 증서 · 세대 섞임) ④ 먼저 쓸 시험 (고치기 전 실패해야 할 것 · R18 종료조건 8 · no-op · 극한 · 상호성 · KCL · 회전/반사 · 주기 seam · 고정 기하 격자 조임 · origin 불변 · 투여 단조) ⑤ 한계 · 지원 범위 ⑥ 웹앱 표지 (J20-l).
2. **등록 R 초안** `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` (결과 0 건 · 1저자 비준 전 · Codex 검토 대상) — 손잡이 원장 · 보정 절차 · holdout · 예측 구간 · 합격 기준 · 금지 문장 · 불합격 보고 · 기계 · 명령 꼴.
3. **Codex 설계 리뷰 요청서** `docs/reviews/codex_rint_carbon_additive_design_request_20261020.md` — 맨 위에 **"이번에 닫는 것 / 닫지 않는 것"** · 범위 (설계만 · 다음 세대 · 10-20 제출본 소급 없음 · 생산 규약 그대로) · 질문 Q 목록 (단계별 GO/HOLD · 아래 쟁점 하나하나) · **Part B = 조인 수정 재확인 자리 (뼈대만)**: 대상 = RIMPR-R01 · RIMPR-03 · RIMPR-04 (부분) · SELF-124 (커밋 `12d894c09` 시험 먼저 · `a2cfd0365` 수정 · `654385e4c` 기록 — 이 셋은 fast-forward 로 원격에 올라간다) · 탐침 재실행 요청 (`docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/probes/` 넷 · 계획 `docs/reviews/rimprr_fix_plan_20261020.md` §3-4 기대) · 사전 리뷰 결과 · 리뷰 핀 = `⬜ (메인이 채운다)` 표지로 남긴다.

## 반드시 명시적으로 풀어 적을 쟁점 (Codex 가 HOLD 를 낼 자리 — 애매하게 두지 않는다)
- **식별성 = 한 점 · 한 손잡이**: SBE 1.63 한 점으로 정하는 손잡이는 **R_j,0 하나**.  σ_VGCF = Endo 단섬유 값 고정 (Q5) — 통합 계획 §1 의 *"σ* 재보정 고리 (σ*_VGCF 가 바뀐다)"* 문장과 충돌하므로 어느 쪽인지 한 문장으로 정리하고 (권고: 다음 세대에서 묶음 σ* 는 손잡이가 아니다 · 새 `physics_protocol_id`), 모든 매개변수를 표로: {문헌 고정 · S0 기하로 σ 보기 전 고정 · SBE 보정 · 시나리오 끝 · 민감도만}.  두 손잡이가 한 점으로 정해지는 꼴이 남으면 안 된다.
- **holdout 오염**: DBE 4.68 은 10-20 현 세대 보정 (σ_VGCF 2.618 · ×7.54) 에 이미 쓰였다 — 등록에 *"값을 알고 있었다 (맹검 아님)"* · PTFE · SDCP 법칙과 구간을 그 보정값 · 배수를 보고 고르지 않는다 · 결과 뒤 다시 고르지 않는다.
- **예측 구간의 정보량**: 구간 = SDCP 시나리오 두 끝 × PTFE 법칙 밴드 — 너무 넓으면 통과가 무의미.  런 전에 구간 폭의 보고 기준 (예: 보정 없는 현 세대 DBE 1.8877 ↔ 4.68 차이 대비 폭) 과 4.68 이 구간 어디에 떨어지는지 보고하는 꼴을 등록한다.  측정 불확도 (두 시편 · 두께 90 / 80 µm · 지름 10 mm) 를 어떻게 넣는지.
- **이중 계상**: S1 PTFE 면 연산자를 켜면 생산 centerline 셀 스탬프 (`CL-60`) 를 끄는지 · 대체하는지 — 둘 다 켜면 PTFE 를 두 번 센다.  Q8 (S0 로 크기만 · 규약 변경은 S1 등록 때) 과 맞춘다.  SDCP 구 스탬프 (부피) 와 S3 접점 수정자 (막) 도 같은 질문.
- **S2 v0 범위**: VGCF–VGCF 만 — VGCF–AM · VGCF–SDCP · 탄소–SE (전자 0) 는 어떻게 되나 (지금 규약 그대로인지) · 접점 검출 문턱 (tol_ff · L_par · r_port) 을 S0 분포로 σ 보기 전에 고정하는 절차 · 연속 중심선 원천 (MPM 끝 점 + `fibre.npy`) 이 없는 침대는 거부.
- **격자 의존**: 접합을 간선으로 넣으면 격자 의존이 줄어야 한다 — 확인 방법 (두 vox) 을 등록에 넣을지 · 못 넣으면 한정.
- **풀이 조건수**: σ 대비 ≈ 2e6 (AM 0.0041 ↔ 7,854 S/cm) · 수렴 기준 · AMG / maxiter · 보조 풀이까지 수렴 증명 (`RGL-01` 교훈) · 미수렴 = 미게시.
- **S3 SDCP**: c = 0 비트 동일 · SBE (SDCP 없음) 셀 단위 no-op · c 단조 · 원고 펠릿 LPSCl:SDCP 9:1 비퍼콜 유지 (퍼콜시키면 기각) · "SDCP 재료값" 이라 부르지 않는다.
- **측정 꼴**: DC 2-전극 R 에는 집전체 접촉이 들어간다 — 모델에 그 항이 없다 (Q11 실험 요청은 선택 · holdout 판정 한정어).
- **세대 · 영수증**: 새 세대 결과를 옛 세대 표 · 인계 · 웹앱 비교에 섞지 않는 강제 (세대 도장 · 거부) · 끄면 옛 매니페스트 바이트 그대로.

## 규칙
- **코드는 고치지 않는다** (문서 셋만) · push 안 함 · `scripts/check_all.sh` 안 돌림 · 무거운 계산 안 함 (다른 에이전트가 돈다).
- 값 · 서지는 litdb 정본 카드에서만 (`git fetch origin claude/friendly-meitner-lldvar` 는 해도 된다 — 정본 읽기 전용 · `git show FETCH_HEAD:litdb/papers/<card>.md`) — 카드가 없으면 `[미확인]` (CLAUDE.md 규율 ⑥).  원고 펠릿 값 (LPSCl:PTFE 9:1 · LPSCl:SDCP 9:1) 은 리포 안 자리를 찾아 경로를 적는다 · 못 찾으면 `[미확인 — 1저자 자료]`.
- 원격에 없는 커밋 번호를 쓰지 않는다 (`SELF-116`) — `12d894c09` · `a2cfd0365` · `654385e4c` · `f507bdc74` 는 fast-forward 로 올라갈 예정이라 써도 된다 · 네 커밋 번호는 쓰지 않는다.
- `python3 scripts/check_doc_refs.py` 통과 (`✓ 깨진 참조 없음`) 뒤 커밋 하나 (영어 메시지 · 모델 이름 없음 · 끝 두 줄 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` / `Claude-Session: https://claude.ai/code/session_01H191Ni4xzj9H5ftstAm7Ft`).
- 보고 (한국어 · 짧게 · 표): 커밋 SHA · 문서 셋 크기 · 쟁점마다 정한 것 (한 줄) · 1저자에게 새로 물어야 할 것 (권고 한 줄씩) · `[미확인]` 목록.
