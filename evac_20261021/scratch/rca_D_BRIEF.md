# D — 사슬 · 배선 통합 (A · B · C 결과를 사슬 · payload · 러너 · 웹앱에 잇기 · 시험 먼저)

먼저 `rca_common.md` (같은 폴더 · 기한 10-31 · *"더 꼼꼼하게"* · 규칙) 를 읽는다.

## 기반
- 너의 작업 트리에서 `git reset --hard <BASE>` (메인이 알려 준 통합 HEAD · A 20 커밋 + B 8 커밋 + C 문서 3 판 + 기록 둘 + B 픽스처 패치 · 같은 저장소 · fetch 안 함).
- 정본: 등록 R 3 판 `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` (§2-1 · §2-1b · §3-2 · §3-2b · §3-2c · §3-3 · §4-2 · §5-0 – §5-7 · §7-1 · §7-2 · §10-2 · §10-3 · §11 · §13) · 설계 v1 3 판 · 수정 계획 `docs/reviews/rint2_design_fix_plan_20261021.md` §5 · 판정문 `docs/reviews/codex_review_rint2_carbon_additive_design_20261021.md`.
- A 보고 요지: `sv_dominant` 철회 → `sv_local_dissipation` (진단) · 반사실 노브 `cjunc_plan(sv_counterfactual={'threshold': None | 유한 ≥ 1})` → 기록 `sv_counterfactual` {status · `sv_counterfactual_ratio` · flag `SV_DEPENDENT` (문턱 있을 때만) · conv_cert · …} · counts 간선 단위 (`n_sdcp_near` 포함) · 판 `r3-carbon-junction-port-v2` · schema `cjunc-v2`.
- B 보고 요지: 해 상태 `POSITIVE_SOLVED` · `VALID_ZERO_TOPOLOGY` · `ELECTRODE_SHORT` · `NOT_CERTIFIABLE` · `zero_source` · 증서 판 `conv-cert-v2` · `target-cert-v1` · `fsum-bfs-defect-margin-v2` · 계약 `next_gen_cert_ok` 는 영값을 이미 받는다.

## 할 일 (묶음마다 시험 먼저 → 구현 · 고치기 전 실패 확인 · 기본 끔 = 옛 동작 바이트 같음)
1. **SV 가드 사슬 반영** — `scripts/rint_r_chain.py` 가 철회된 `sv_dominant` 를 읽어 실제 런에서 SV_DOMINANT 가 늘 걸린다 (A 보고 §6).  등록 R §5-6 · §5-6a 대로: 반사실 비 · `SV_DEPENDENT` · 문턱이 등록되지 않았으면 (⬜ 1저자 숫자) `SV_UNCHECKED` 로 차단 (닫힌 집합).  반사실 결과 상태 (`no_through_without_sv` · `unconverged` · …) 마다 사슬 동작을 정한다 (등록 문장 그대로 · 문장이 정하지 않으면 차단 + 보고).
2. **영값 · 단락 상태** — 사슬 (`rint_r_chain.py` 586–591 · 621–623 부근) 이 σ = 0 을 ARM_UNREADABLE · NOT_COMPUTED 로 멈춘다 → `status == VALID_ZERO_TOPOLOGY` 이면 받는다 (등록 R §5-0 결정표: zero · short 를 확장 실수 끝으로 · `UNINFORMATIVE` · `FAIL`).  천장 J11 단락이 지금 `CA_EXT_RECORD` 로 멈추는 것도 결정표대로.  payload (`scripts/mpm_webapp_payload.py` 2398–2401 부근) 의 사유 있는 조기 반환이 `conv_cert` 를 복사하지 않는 것 고침 (B 보고).
3. **등록 3 판의 사슬 규칙** — 끝 규칙 (§3-2b: 보간 = 후보 → 1.63 × 1.02 · × 0.98 끝 확인 런 → 바깥 실측 이웃 · 넓은 역상 = 미식별 · 예산 끝 = 미완료) · e_min = 국소 진단만 (빠른 멈춤 아님) · origin 세 R (§4-2 · 8 팔 평균) · 감도 = 주 판정과 같은 판정 함수 (§5-6) · `GAP_ENVELOPE_ONLY` (§5-5) · `ASSUMED_UNVALIDATED` 닫힌 집합 (§5-6a) · `SENTENCE_PASS` = §5-3 판정문 문안 (§7-1) · 결정표 (§5-7) · 두 계획 대조 (§2-1 · §10-2 ⑪ · S0 `ca-cjunc-plan-v1` ↔ R `rint-r-plan-v1`).  숫자가 ⬜ 인 곳 (점 수 상한 · 역상 폭 상한 · SV 반사실 문턱) 은 숫자를 고르지 않는다 — 계획 파일 칸 + 없으면 사슬이 멈추는 꼴로.
4. **반사실 노브 배선** — payload · 러너 env (이름 = 등록 R §10-3 에 맞추거나, 없으면 너가 정하고 §10-3 표에 날짜 표지로 적음) · 매니페스트 · `run_contract` 회계 (`CLI_ACCOUNTING` · 규칙 M) · JSON 에 inf 비 (위상 사유) 를 쓰는 꼴 · 영수증 대조 · REQUIRE_GPU 에서 반사실 솔브 실패 시 동작 (런 전체 정지 vs 상태 기록 — 등록 문장 따라 · 없으면 차단 + 보고) · 메모리 (계 두 번 조립) 를 실침대 크기로 어림해 보고.
5. **허용 목록 · 이름** — `scripts/test_ca_ext_b6.py` B1 · `scripts/test_ca_ext_z3.py` O2 의 `--old-scripts` 비교 허용 목록에 B 의 새 칸 (증서 `version` · `status` · `pass_d` · `scale` · `target_*` · S1 `capsules.volume_basis` · `volume.capsule_nominal_um3` / `capsule_union_um3` / `capsule_union_status` / `capsule_volume_basis` / `ratio_basis` · `faces.*.alpha_zero_faces` / `alpha_zero_open_at_refine` / `alpha_refine_K` · `exempt_assumptions`) 과 A 의 새 칸.  문서 ↔ 코드 이름 어긋남 (예 B `ELECTRODE_SHORT` ↔ 문서 `short`) 은 **등록 R §10-3 표 · 해당 문장만** 날짜 표지로 코드 이름에 맞춘다 (뜻은 안 바꿈).
6. **웹앱** — 새 상태 · 표지 (`SV_DEPENDENT` · `SV_UNCHECKED` · `VALID_ZERO_TOPOLOGY` · `ELECTRODE_SHORT` · `GAP_ENVELOPE_ONLY` · `ASSUMED_UNVALIDATED` …) 가 화면 (`webapp/` 의 ca_ext 표지 · 툴팁) 에 같은 이름 · 한정어로 (`webapp/test_ca_ext_labels.py` 시험 먼저).  화면이 없으면 보고에 적는다.

## 회귀 (끝에 한 번 · 하나씩 · nice -n 19 · 스레드 1)
`test_rint_r_chain` · `test_rint_r_chain_e2e` (실제 러너 · 바닥 → 천장 → 점 → 확인 → origin — 새 규칙으로 끝까지 도는지) · `test_ca_ext_b6` · `test_ca_ext_runner` · `test_ca_ext_z1` · `test_ca_ext_z3` · `test_ca_ext_verdict` · `test_carbon_junction` · `test_ca_s0_census` · `test_step3_target_cert` · `test_step3_conv_cert` · `test_ptfe_face_alpha --old-scripts …/scratchpad/s1/old/scripts` · `step3_sigma --selftest` · `--selftest-rint` · `run_contract --selftest` · `webapp/test_ca_ext_labels.py` · `check_method_discipline` (`--selftest` + 인자 없이 · 오류 0) · 끈 경로 비트 대조 (새 노브 다 끄면 매니페스트 · 러너 영수증 · 팔 이름 · σ = `<BASE>` 와 같음).
변이 시험: 사슬의 새 분기마다 한 줄씩 틀리게 해 시험이 옳은 이유로 실패하는지 (되돌림) 표로.

## 규칙
- push · `scripts/check_all.sh` · `git fetch` · GPU 런 · kgy 접속 없음.  ⛔ 봉인 32 파일 · 원장 · CLAUDE.md · 진행 기록 · 수정 계획 금지 (등록 R §10-3 표 이름 맞춤만 허용).
- ⚠ 메인이 "게이트 창" 을 알리면 그 동안 60 s 넘는 실행 금지.
- 커밋 메시지 영어 · 모델 이름 없음 · "pre-fix N/M (fails = K checks from J counterexamples)" 꼴 · 끝 두 줄 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` / `Claude-Session: https://claude.ai/code/session_01H191Ni4xzj9H5ftstAm7Ft`.
- 보고 (한국어 · 표 · 짧게): 커밋 SHA · 고치기 전 → 뒤 · 등록 문장 ↔ 사슬 동작 대조표 (§마다) · 문장이 정하지 않아 차단으로 둔 자리 · 이름 표 · 변이 표 · 회귀 · 끈 경로 대조 · 줄이거나 건너뛴 것.
