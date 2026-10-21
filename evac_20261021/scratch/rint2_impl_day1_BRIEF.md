# Rint ② 구현 1 일 차 (1저자 10-20 밤 *"1주내로 해결해"* · 구현은 Codex 설계 리뷰와 병렬 · 발사는 Codex GO + 등록 R 비준 뒤)

## 공통
- 기반 = 너의 작업 트리 HEAD (`d1768cf0c` = 원격).  `git fetch` 하지 않는다.  push · `scripts/check_all.sh` 안 돌림 · 커밋은 네 작업 트리에서만 (메인이 나중에 옮긴다 · 다른 에이전트가 같은 파일 근처를 고칠 수 있으니 **새 모듈에 몰고 `scripts/step3_sigma.py` 에는 최소 훅만**).
- 설계 정본 (전부 읽는다): `docs/reviews/rint_carbon_additive_design_v1_20261020.md` (§0 쟁점 결론 · §1-2 매개변수 분류 · S0 · S1 · S2 v0 · S3 · 수렴 · 세대 · §10 질문) · `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` · `docs/reviews/rint_carbon_additive_plan_20261020.md` · 계약 정본 `docs/reviews/contact_resistance_pipeline_draft_v2_20261006.md` · `…_v3_20261006.md` · `…_v3_1_20261007.md` · R18 `docs/reviews/codex_r18_verdict_20260831.md` Q6.
- **1저자 결정**: 설계 §10 N1–N18 = 1저자 10-20 *"다 권고대로 해"* — 문서의 `⬜ 1저자 (권고)` 는 전부 권고안이 확정.  추가 규칙 (1저자 10-20): 다음 세대 침대 = **SBE · DBE 둘 다 VGCF E 100 GPa 로 다시 압밀** · **VGCF voxel σ = 두 전극 같은 값 하나 (직경 보존 · Endo 단섬유 → 7,854 S/cm · Q5)** · 보정 손잡이 = **R_j,0 하나 (SBE 1.63 만)** · DBE 4.68 에 맞추지 않음.  동기 한 줄: 지금 σ_ion SBE 0.137 ↔ DBE 0.138 (PTFE 0.5 wt% 차이가 안 보임 — 원고 펠릿 9:1 PTFE −73 % · SDCP −20 %).
- 규율: **시험 먼저** (고치기 전 실패 확인 · 커밋 메시지에 판 · 수 · 실패 집합) · 전부 **기본 끔 · 끄면 옛 경로 비트 동일** (코드 지문 칸 `code_sha` · `exec_env` 만 다름) · 지난 HOLD 부류 (NaN · inf · 넘침 · 빈 · 중복 · 검사 전 정규화 · 유니코드 · 증서 ↔ 결과 결합 · 다른 판본 · 세대 섞임) 를 계약 · 시험에 · 웹앱 표지 = 같은 묶음 (화면 없으면 보고에 적기) · 커밋 메시지 영어 · 모델 이름 없음 · 끝 두 줄 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` / `Claude-Session: https://claude.ai/code/session_01H191Ni4xzj9H5ftstAm7Ft`.
- 디스크 여유가 작다 — 큰 임시 사본 금지 · 쓰고 지움.  CPU — 다른 에이전트 셋이 같이 돈다.
- 보고 (한국어 · 표 · 짧게): 커밋 SHA · 시험 고치기 전 → 뒤 · 비트 동일 대조 · 설계와 다르게 한 곳 · 남은 것.

## A — S1 PTFE 면 개구율 연산자 `face_alpha` (전자 · 이온 플래그 따로)
- 설계 S1 그대로: `G = α·G0` · 캡슐 (중심선 + 지름 0.248 · 길이 = 시더 처방 그대로 · K = 8 봉인) · 셀을 찍지 않음 · `ptfe_stamp` 새 값 `face_alpha` (centerline 과 동시 불가 · 이때 sid 격자 = `off` 격자 · PTFE 셀 0) · `--sigma-ptfe` · `PTFE_BLOCK_*` 조합 거부 · `!= 'off'` 분기 세 곳 (`scripts/mpm_webapp_payload.py` 1492 · 1913 · 3014 근처 · 541 selftest) 정리 · 세대 = `ca_ext` 블록 · id 접두 `p3ca-` · 블록 결손이면 `unknown:ca_ext`.
- 시험: R18 종료조건 8 (α = 1/0 극한 · 상호성 · KCL · 회전/반사 · 주기 seam · 고정 기하 격자 조임 · origin 불변 · 투여 단조) + PTFE 없음 no-op + **F16 해석 α 픽스처** (캡슐 축 ∥ 면 · 원 ∩ 정사각형 정확 면적비 · 두 셀 직렬 g = α·g0 해석해 · 판 근처 캡슐) + 변이 시험 (α² · α^p · 반 셀 어긋남 · 판에 α 를 떨어뜨리는지).
- 새 모듈 예 `scripts/ptfe_face_alpha.py` + `solve_sigma_z` 최소 훅.

## B — S2 탄소 접합 R_j v0 + S3 SDCP 접합 수정자 + 수렴 증서
- 설계 S2 v0 · S3 · 수렴 절 그대로: VGCF–VGCF 접합 instance 마다 간선 하나 · 교차 셀 멤버십 dof · 등록 쌍 융합 면 절단 · 실제 그래프 가지치기 · J1–J12 (J8 = 긴 접촉이 있으면 정량 거부) · 직접 간선에 반셀 없음 (RINTG-09) · canonical 키 반올림 경계 · 포트 동률 · 같은 fid 비연속 구간 지름길 금지 · gap_tol 끊기 / S3: c ∈ {0, 1} · c = 1 = 같은 그래프 축약 (정량 허용 예외 · instance 수 기록) · (c1, P1) = PTFE 절단 먼저 · SV 면 = 융합 그대로 + `SV_DOMINANT` (SV 경로 소산 ≥ VV 접합 소산 → PASS 문장 금지 표지) + SV 소산 몫 · SDCP 경유 연결 수 보고 / 수렴: `--step3-rtol` 노브 (numeric) · 판정 해 rtol ≤ 1e-12 · 판 전류 불균형 ε_I 봉인 절차 (합성 직접해 대조) · ⓒ 재풀이 대조 · 미수렴 = 미게시.
- 시험: 위상 ON · R_j 0 = 축약 그래프와 같음 · T1-6 · T1-7 · T1-8 · T2-3 · c = 0 비트 동일 · SBE 셀 단위 no-op · c 단조 · Rayleigh 단조 (허용폭 봉인) · 합성 수렴 탐침 (24×24×72 · 섬유 7,854 · 1e-8 에서 거짓 수렴을 시험이 잡는지).
- 새 모듈 예 `scripts/carbon_junction.py` + 최소 훅.

## C — S0 표현 원장 + kgy 명령 (재압밀 · S0)
- S0 도구 (raster-only · 솔브 없음 · CPU): PTFE 가 덮은 탄소 셀 · SDCP 가 덮은 VGCF/AM 셀 · PTFE 가 끊은 VGCF 경로 · SDCP 표현 부피 · 섬유 접합 기하 census (접점 수 · 길이 · 평행 접촉 · 긴 접촉 수 = J8) · 문턱 식 (설계 N17 = 식 지금 고정 · 숫자는 SBE 기하로 계산 · DBE 분포는 문턱 개정 커밋 뒤에만 연다 · 계획 해시) · 시험 먼저 (교차 fixture 손계산).
- kgy 명령 문서 (`docs/reviews/rint2_kgy_commands_20261020.md`): ① **SBE · DBE 두 침대 VGCF E 100 GPa 재압밀** — 등록 v2 §7 의 R1 재압밀 명령 (10-19 · 다섯째 시도) · SBE 원 침대 명령을 찾아 `--add-e-override VGCF=10` 을 빼거나 100 으로 · 새 OUTDIR · 시간 어림 · 같은 시드 · 결과 검사 (porosity · 두께 · 점 수) ② S0 실행 ③ (발사 전 금지 표지) 런 사슬 꼴만.  1저자가 kgy 에서 그대로 붙일 수 있게 · kgy 경로 (`~/sdcp/kit_SBE` · `~/sdcp/kit_DBE_sdcp1um` · `~/dem-anchor1019b`) 는 이번 세션 기록 그대로 · 주소 · 포트는 적지 않는다.
