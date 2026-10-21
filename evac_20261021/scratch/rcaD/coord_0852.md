The coordinator sent a message while you were working:
다음 일 — B (증서 결합 · PRE-impl-07) 를 네 가지에 합쳐라 (메인 지시). Q1 (단락 상태) · Q2 (4 판 사슬 규칙 6 개) 는 1저자 답을 기다리는 중이니 **아직 손대지 않는다** — 답이 오면 따로 보낸다.

1. 네 작업 트리 (`5dabe6156` 위) 에 B 의 커밋 둘을 차례로 cherry-pick: `cd78c008d` (시험 먼저 — T21 · T22 · T23 · T18 변이 14) → `60c0c952b` (구현 — `run_contract.py` · `step3_conv_cert.py` · `step3_sigma.py` 증서 쪽). 기반은 둘 다 `a76f59d0d`. `run_contract.py` 충돌이 나면 두 쪽 뜻을 다 살려 풀고, 푼 자리를 보고에 적는다.
2. B 가 남긴 픽스처 패치를 같은 묶음에 넣는다: `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaB/fixtures_bind_b7.patch` (sha256 `6475a7d4…` · `test_ca_ext_b6.py` +16/−8 · `test_rint_r_chain.py` +19/−4 · B 판 위에서 `git apply --check` 깨끗이라고 함 — 네 판 위에서 다시 확인). 네 b6 · chain 시험 변경과 겹치면 합친다.
3. S07 — B 수정 뒤 `rint_r_chain.read_run` 이 `next_gen_cert_ok` (증서 결합) 를 세대 · ca_ext 기록 검사보다 먼저 불러, `unknown:ca_ext` 팔이 GENERATION 대신 `NOT_COMPUTED` (`CERT|bind| 매니페스트에 격자 지문 칸이 없다`) 에서 멈춘다 (패치 넣어도 chain 88/89 라고 함). B 권고 = 기록 검사를 증서 검사 앞으로 (결합은 맞는 세대 · 맞는 기록 위에서만 뜻이 있다). 시험 먼저 꼴로: 지금 판에서 S07 실패 재현 → 순서 고침 → 139+ 전부 통과 · 다른 멈춤 코드 (S06 · S08 · S09 · S12 · S26 · S27 · X09) 그대로인지 확인.
4. 회귀를 다시: chain · e2e · b6 · runner · z1 · z3 · verdict · carbon_junction · target_cert 빠른 판 · conv_cert · step3 selftest 둘 · run_contract selftest · 웹앱 둘 · check_method_discipline. **target_cert `--long` 은 4 스레드 탐침이 있으니 `HEAVY_EXCLUSIVE=1 bash <scratchpad>/heavy.sh …`** (heavy.sh v3 · 기본 = 두 자리 중 하나 · 1 스레드). 끈 경로 비트 대조 (`--expect-identical`) 도 다시.
5. 커밋은 cherry-pick 둘 + 패치 · S07 한 커밋 (시험 먼저면 둘). push · fetch · check_all 안 함. 문서에 작업 트리 SHA 를 쓰지 않는다.
6. A (S2 branch · port · 분산 · SV 가드) 는 아직 돌고 있다. A 가 끝나면 메인이 너에게 A 커밋을 합치라고 보낼 것이다 — 지금은 A 파일 (`carbon_junction.py` · `ca_ext_cjunc.py` 의 A 쪽 · `fibre_segment_raster.py`) 을 더 고치지 않는다.

보고: 커밋 · 충돌 · 고치기 전 → 뒤 · 회귀 표 · 끈 경로 대조.

Address this before completing your current task.