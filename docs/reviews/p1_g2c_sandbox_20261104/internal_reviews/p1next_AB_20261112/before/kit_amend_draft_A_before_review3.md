# 언로딩 등록 개정 4 (§15) — 복원 쌍 관문 = G2c′ [왕복] (키트 적용)

> **초안 · 결과 0 건 · 1저자 비준 전 (QA7 다시 물음 · 15-11) · Codex 설계 확인 전 · 내부 반박 리뷰 1 · 2 회차 반영 (11-12 · Codex 아님 · 1 회차 `docs/reviews/p1_g2c_sandbox_20261104/internal_reviews/p1next_AB_20261112/review1_AB.md` → `docs/reviews/p1_g2c_sandbox_20261104/internal_reviews/p1next_AB_20261112/disposition1_AB.md` · 2 회차 `docs/reviews/p1_g2c_sandbox_20261104/internal_reviews/p1next_AB_20261112/review2_AB.md` (P2 3 · P3 6) → `docs/reviews/p1_g2c_sandbox_20261104/internal_reviews/p1next_AB_20261112/disposition2_AB.md`)** — 2026-11-12 · 문서만 (실행 · 제출 · 키트 파일 · 리포 변경 없음).  고치기 전 판 = `kit_amend_draft_A_before_review2.md` (sha256 앞 12 `2831568d3d53`) · 1 회차 전 판 = `kit_amend_draft_A_before_review.md` (`ecd528e3c4c2`).
> ⚠ **15-5b 문턱은 결과를 본 뒤 정했다 (2 회차 · 11-12)** — 정하기 전에 본 값: 7:3 [연속] 사후 (11-02 · reset_like 몫 685/562605 = 0.0012 · r 중앙 7.8e-5 · 빠짐 · 더함 0) · 11-12 직렬 샌드박스 정직 흐름 (B 주기 파일 ↔ A(N) = 몫 48/3111 = 0.0154 · r 중앙 6.2e-4 · \|Ft\| 가중 몫 W 0.0031 · 무너짐 몫 0.0061 · \|Ft_원\| 하위 10 % 뺀 몫 0.0075 / C 명령 파일 ↔ A(N) = 0.0016 · 0 · 0.0004 · 0.0013 · 0.0014) · 소실 반례 산술 (리뷰 `docs/reviews/p1_g2c_sandbox_20261104/internal_reviews/p1next_AB_20261112/r2_cont_guard.py` · `docs/reviews/p1_g2c_sandbox_20261104/internal_reviews/p1next_AB_20261112/r2_alt_metrics.py` · 이 고침 `docs/reviews/p1_g2c_sandbox_20261104/internal_reviews/p1next_AB_20261112/f2_guard_power.py` → `docs/reviews/p1_g2c_sandbox_20261104/internal_reviews/p1next_AB_20261112/f2_guard_power_out.txt`).  결과 전으로 남은 것 = 7:3 의 W (계산 안 함) · 남은 네 침대 · 10:0 RJ · RJ2 · ⓣ 전부.  1 회차 문턱 (몫 ≤ 0.03 ∧ r 중앙 ≤ 1e-2) = 거둠 (정직 B 몫 0.0154 = 문턱의 ×1.9 아래 · P1G2-01).
> 트랙 = [DEM 우선] Ⓐ 언로딩 P1 (Claude 세션 · 1저자 11-04 오후 Q1) · 자리 = 메모 `docs/reviews/p1_g2c_compare_definition_20261105.md` §5-3 (1저자 11-12 *"권고대로"*).
> 대상 = 등록 `docs/reviews/dem_unloading_ps45_prereg_20261009.md` (이하 REG) 의 G2c 자리 — §3-2 표 G2c 행 (229 행) · §12-1 G2c 문장 (614 행) · §13-7 C7 (798 행) · §14-10 복원 판정 · §14-11 ② · §14-12 `ULPR-04`.  비준되면 REG 끝 §15 로 붙이고 그 자리마다 "⛔ 개정 4 §15" 표지 (원문 보존 · 앞 개정과 같은 꼴).  GO 문구 자리 (REG 1 행 · 962 행 · 키트 `run_unload.sh` 2 행 · `run_unload_ibb.sbatch` 8 행 · README §2 · §3 머리) = 그대로 (QA5 = 1저자 11-12 Codex GO 유지 · 표지 없음).
> 리포 경로 표지: 11-12 결과 = 대피 세션 커밋 L `bfd9b3bbd` (가린 사본 `docs/reviews/p1_g2c_sandbox_20261104/run_ibb_40000_20261112/` · 메모 §8) — 이 컨테이너 원격 추적 ref (`ef68eb7da`) 에 없음 = push 전 → 아래 그 경로 = **push 뒤 경로**.  덤프 · 로그 원본 = 리포 밖 (받은 묶음 sha256 3caf3e05… · 그 폴더 README 3 행).

| 이번에 닫는 것 | 닫지 않는 것 |
|---|---|
| 복원 쌍 관문의 기준쪽 (원 런 덤프 → 같은 경로 재계산) · RT1 · RT2 단계 (UN 뒤 · UK 앞) · G2cp 판정 규칙 · rt.bin 결합 (RT2 로그 파일의 전체 경로) · 옛 G2c = [연속] 보고 + 거친 이력 소실 문턱 (15-5b · \|Ft\| 가중 몫 · QA7) · RT 문법 fixture 를 RJ 전에 (15-4b · 새 파일 · 검사 20) · 바뀌는 코드 · 시험 · 봉인 자리 | 원 런 ↔ 재개 연속성 · MPI 지연 크기 · 쓴 NP ≠ 읽는 NP (초안 B · 따로) · C12 중력 팔 (개정 5 · QA2) · 벽 이력 판정 · 허용폭 · RJ 323957 소급 · 언로딩 물리 · 발사 승인 (QA5 = Codex GO · 리셋 뒤 · B 결과 붙여) · 10:0 출발 체크포인트 (C18 · §12-11) |

## 15-0. 한 줄

- RJ · RJ2 의 R 흐름 (PRE · POST · G1–G3 · UN) 은 바이트 그대로 두고, **UN 바로 뒤 (UK 앞)** 에 RT1 (S0 → P → `write_restart`) · RT2 (그 파일 → P) 를 더해 쌍 접촉 관문을 RT2 ↔ RT1 (G2c′ · 판독기 키 `G2cp`) 로 판정한다.
- 옛 G2c (R `g2/contact_S0` ↔ 원 `contact_S0`) 는 같은 식으로 계산해 [연속] 보고로 내리고, 거친 이력 소실만 막는 결과 전 문턱 (15-5b · \|Ft\| 가중 reset 몫 · R · RT1 각각) 을 둔다 (QA7).

## 15-1. 근거

| 무엇 | 값 | 출처 · 표지 |
|---|---|---|
| 옛 G2c 가 원리상 못 서는 까닭 | ㉠ 주기 restart 쌍 이력 = 힘 계산 전 사본 (직렬 B shear = A(N−1) 3111/3111) · ㉡ 스텝 끝 덤프는 고스트 쌍을 setup 과 다르게 다시 계산 (직렬 C ↔ A = 주기 표지 334 쌍 전부) · ㉢ `force_normal` = 쌍 전체 힘 사영 | 메모 §1 표 · 노트 `docs/reviews/p1_g2c_source_check_20261104.md` §7 · `docs/reviews/p1_g2c_sandbox_20261104/run_40000/compare.json` · `diag_out.txt` |
| 같은 경로 재계산이 서는가 (직렬 · 11-12 ibb 잡 359243 · 생산 `lmp_mpi` 1 프로세스 · N 40000) | 판정 다 · 라 PASS (n_mismatch 0 · 비트 같은 쌍 3111/3111) · 원자 1220 · 판독 가능한 예측 13 모두 맞음 · 가 · 라-재현 (나) = 해당 없음 (실행 파일 md5 0c0daccc ≠ 11-04 f4ba3ec0) | `docs/reviews/p1_g2c_sandbox_20261104/run_ibb_40000_20261112/compare_g2cp.json` `judgment` · `predictions` · 메모 §8 (223–236 행) — push 뒤 경로 |
| 명령 체크포인트여도 옛 꼴은 실패 | 11-12 [연속] 키트 26 열 옛 식: B (주기 파일) FAIL n_mismatch 3107 · C (명령 파일) FAIL 331 (힘 다른 쌍 334 = 주기 표지 334) | 같은 JSON `reports.연속` |
| RJ 323957 | G2c FAIL 545583/562605 (빠짐 · 더함 0) · `VALUE_MISMATCH` · reader_rc 2 — 그대로 · 소급 PASS 없음 | `docs/reviews/codex_p1_g2c_diagnosis_20261027/restore_verdict.user-relayed.json` · `run_manifest.user-relayed.txt` 26 · 28 행 |
| 7:3 [연속] 이력 소실 지표 (11-02 사후 · 판정 자료 아님) | reset_like 685 / 562605 (0.12 %) · ΔFt/Ft 중앙 7.8e-5 (q95 4.0e-3) · 내부 고착 쌍 352663 · \|Ft\| 가중 몫 W = 계산 안 함 (결과 전) | `docs/reviews/dem_unloading_rj_g2c_cause_20261102/RESULT_20261102.md` 8 · 12 행 · 정의 = 같은 폴더 `rj_g2c_cause_check.py` 336–341 행 |
| 11-12 직렬 정직 흐름의 15-5b 지표 (문턱을 정하기 전에 본 값 · 머리 표지) | B (주기 파일 · 한 step 늦은 이력) ↔ A(N): 공통 3111 · 빠짐 · 더함 0 · reset_like 48 (0.0154 · 그 중 27 쌍 = \|Ft_원\| 하위 10 %) · r 중앙 6.2e-4 · W 0.0031 · 무너짐 몫 0.0061 / C (명령 파일) ↔ A(N): 5 (0.0016 · 5 쌍 전부 주기 표지 1) · r 중앙 0 · W 0.0004 · 무너짐 몫 0.0013 | 받은 묶음 (리포 밖) `A` · `B` · `C` 의 `post/c_40000.txt` (sha256 앞 12 = 65d1b67daad3 · 2714944d9cc7 · 3074648b4633) · 산술 `docs/reviews/p1_g2c_sandbox_20261104/internal_reviews/p1next_AB_20261112/r2_cont_guard.py` · `docs/reviews/p1_g2c_sandbox_20261104/internal_reviews/p1next_AB_20261112/r2_alt_metrics.py` · `docs/reviews/p1_g2c_sandbox_20261104/internal_reviews/p1next_AB_20261112/f2_guard_power.py` → `docs/reviews/p1_g2c_sandbox_20261104/internal_reviews/p1next_AB_20261112/f2_guard_power_out.txt` |
| S0 꼴 | 다섯 침대 S0 = 주기 `restart 50000` (명령 없음) · **10:0 RJ2 의 S0′ 3,650,000 · S0″ 3,700,000 도 주기** (`docs/data/ps45_unload_20261009/decks/ps_10_0_r45/in.EXT.liggghts` 79 행 `restart 50000` → 81 행 `run 60000` · `in.EXT2.liggghts` 79 · 81 행) · 명시 `write_restart` = 3,660,000 (EXT 끝 = EXT2 출발) · 3,710,000 (EXT2 끝) (두 덱 85 행) | 메모 §2 (11-05) · 키트 README 220 행 · 표 `ext_10_0` (s0p · end1 · s0pp · end2) · `ul_reader.py` 1765–1775 행 (S0′ = `restart_ext_<s0p>.bin`) · REG §12-11 692 행 ("체크포인트 3,650,000") · C18 815 행 |
| 키트 실행 꼴 | NP 6 · `processors * * 1` · `mpirun --oversubscribe --bind-to none` · 7:3 RJ 격자 3×2×1 | `docs/data/ps45_unload_20261009/run_unload_ibb.sbatch` 23 행 · `run_unload.sh` 37–39 행 · `docs/data/ps45_unload_20261009/decks/ps_7_3_r45/in.R.liggghts` 25 행 · `docs/reviews/dem_unloading_rj_g2c_cause_20261102/ibb_result_20261102.json` `rj_screen_processor_grid` (646 행) |
| 이력 열 꼴 | 머리 → `uncompute cpl` → 새 `pair/gran/local … history` → 첫 `run 0` (pair/local 은 하나만 = 10-13 job 281180 실측 · local compute 는 read_restart 뒤 첫 run 전) | `docs/data/ps45_unload_20261009/history_test/in.hist_consumer.liggghts` 68–78 행 · 키트 README §1-5 · §2 덱 언어 규칙 · REG 827 행 |
| 치환된 `read_restart` 경로가 찍히는 곳 | 로그 파일만 — 화면 = `Reading restart file ...` 뿐 (경로 없음) · 로그 = `read_restart ${…}` 줄 + 치환 줄 · 키트 덱에 `echo` · `log` 명령 없음 · 키트 단계 = 화면 `<단계>/screen.txt` · 로그 `-log <단계>/log_screen.liggghts` | 받은 묶음 BR `out.txt` 2 행 ↔ `log.txt` 11–12 행 · `run_unload.sh` 190–193 행 · 키트 R 머리 `read_restart ${ckpt}` (27 행) · LIGGGHTS 3d5c00f 메아리 소스 줄 = [미확인] (받은 로그로 본 것) |

- 판정 G2cp 는 S0 꼴과 무관하게 같은 꼴이다 (11-12 다시 확인) — RT1 · RT2 가 같은 S0 (RJ2 = 주기 S0′) 를 읽고 왕복만 본다 = 직렬 다 (주기 파일 BW → F′ → BR) PASS 와 같은 길.  S0′ 꼴이 바꾸는 것 = [연속] 예측 (A-5) · 15-8 한정어뿐.
- 관찰 (판정 아님): 11-12 덤프 12 개 = 11-04 덤프 바이트 같음 (실행 파일 · 기계 다름) · 다른 3 개 = restart `.bin` 셋 (까닭 [미확인]) — 같은 JSON `predictions.가` · 메모 §8 225 행.

## 15-2. 바뀌는 것

| 자리 | 지금 | 개정 뒤 |
|---|---|---|
| RJ · RJ2 단계 (`run_unload.sh` 229–244 행) | G0 → (7:3) Ut0 → R → UN → (UK · 10:0 RJ 는 없음) → 판독 | G0 → (7:3) Ut0 → R → UN → **RT1 → RT2** → (UK) → 판독 · 앞 단계 실패 (PRE_OK 0) 면 RT 둘 다 안 돎 (기록 `stage=RT1 skipped` · `stage=RT2 skipped`) · RT1 실패면 RT2 안 돎 · RT 실패 = PRE_OK 0 (UK 안 돎 · 복원 = SYNTAX_FAIL 이라 U 없음) · UK 기술 실패는 복원 판정 밖 그대로 (`ul_reader.py` 1566–1569 행) |
| rt.bin 결합 (러너) | — (`run_deck` 은 읽은 restart 경로를 잡 기록 `run_manifest.txt` (`note` 201 행) 에 안 적고 잡 로그 (`say` 187 행) 에 파일 이름만 · 단계 화면 = `<단계>/screen.txt` · 단계 로그 = `-log <단계>/log_screen.liggghts` · 190–193 행) | 잡 기록 머리에 `job_dir=$JD` 한 줄 · RT1 뒤 `rt_bin=$JD/RT1/rt.bin sha256=<…>` · RT2 앞 같은 파일 sha256 다시 `stage=RT2 ckpt=$JD/RT1/rt.bin sha256=<…>` (`note` 두 줄 · 경로 = 러너가 `-var ckpt` 로 주는 글자 그대로) |
| 덱 · 봉인 | 덱 64 · `SHA256SUMS` 76 줄 (KIT_FILES 12 + 덱 64) | 덱 74 (+ RT1 · RT2 × 다섯 침대) · 86 줄 (KIT_FILES 12 그대로) |
| 생성기 (`make_unload_decks.py`) | 148 행: 10:0 `ul_s0` = 3,600,000 은 kind ∈ (R · UNread · EXT) 만 · 그 밖 = `s0_candidates[0]` 3,650,000 · GD1 (810 행) 덱 64 · 593 행 글 "덱 64" · GD1–GD16 | 148 행 튜플에 RT1 · RT2 — 빼면 10:0 **RJ** (러너가 `-var ul_s0` 를 안 준다 · `run_unload.sh` 146–151 행) 의 RT1 = `UL_ABORT reason=start_step` → SYNTAX_FAIL → 10:0 EXT (관문 = RJ RESTORED · `ul_reader.py` 1247–1251 행) · RJ2 · U 막힘 · RT 덱 생성 (15-4) · GD1 · 593 행 = 74 · GD17 · GD18 |
| 복원 쌍 관문 | G2c = R `g2/contact_S0` (26 열 · `%g`) ↔ 원 `in/contact_S0` (`ul_reader.py` 1590 행) | **G2cp** (화면 표기 G2c′ · JSON · 셸에서 U+2032 를 쓰지 않는다) = RT2 ↔ RT1 (30 열 · `%.17g` · 15-5) |
| 옛 G2c | 판정 입력 (`ul_reader.py` 1619 행 목록) | [연속] 보고 `checks['G2c_cont']` — 식 · 함수 그대로 · 1619 행 목록 'G2c' → 'G2cp' + (QA7 예면) `cont_guard` (15-5b) |
| 판독기 (`restore_verdict` 1555 행) | 단계 기술 R · UN · (7:3) Ut0 · reset 로그 = R 화면만 (1570–1573 행) | + RT1 · RT2 (`_stage_tech` 1348 행 · 표지 `UL_RT_DONE`) · RT1 · RT2 화면 reset 로그 (같은 함수 · `EXPECTED_RESETS` 1336–1338 행 · 경로 증거) · rt.bin 결합 (잡 기록 두 줄 + RT2 **로그 파일** 의 치환 `read_restart` 줄 · 15-5) · post 목록 (1604–1607 행 꼴) · G2cp · [연속] · 15-5b (W) · 증서 판 표지 `restore_rule = "rev4_g2cp"` |
| 관문 (`_job_restored` 1212–1226 행) | 증서 status RESTORED + 잡 완료 영수증 (`_job_receipt` · fails=0 · reader_rc=0) + 잡 기록 `grammar_prereq=PASS` 줄 (1217–1226 행) | + 판 표지 `restore_rule = "rev4_g2cp"` (없거나 다르면 = 옛 판독기 증서 · 거부 · 새 시도) + 잡 기록 `rt_grammar_prereq=PASS` 줄 (없으면 거부 · 새 시도 — `grammar_prereq` 줄과 같은 꼴 · 부르는 곳 = RJ · RJ2 뿐) |
| 비교기 (`ul_gates.py`) | `g2c_compare` (26 열 · 339 행) | 그대로 ([연속]) + `g2cp_compare` (15-5) + `cont_guard` (15-5b · W · 26 열 또는 30 열의 26 열 사영 ↔ 원 · 키 · 방향 · 중복 = `_contacts` 그대로 · 299–325 행) |
| 이력 시험 폴더 (`history_test/`) | 문법 fixture (Q5 · 검사 19) — 덱 `in.hist_producer` · `in.hist_grammar` · `plate_hist.stl` = 봉인 `GRAMMAR_INPUTS` · 판독기 · 표 `read_history.py` · `history_params.json` = 봉인 `GRAMMAR_READER` (`ul_reader.py` 60–72 행 · R36 3779–3782 행) | + RT 문법 fixture (15-4b) = **새 파일만**: 덱 `in.hist_rt1.liggghts` · `in.hist_rt2.liggghts` (`make_history_decks.py` 가 만든다 · 지금 덱 9 · STL 바이트 그대로) · 표 `rt_grammar_params.json` · 판독기 `read_rt_grammar.py` · 러너 모드 `run_history.sh --rt-grammar-only` · `history_test/SHA256SUMS` 다시 — `read_history.py` · `history_params.json` 무변경 ⇒ `GRAMMAR_READER` · `GRAMMAR_INPUTS` · R36 · 지금 `GRAMMAR_VERDICT` (10-15 job 285533 · 286802) 사전 점검 그대로 |
| 러너 사전 점검 | 문법 fixture PASS (Q5 · `GRAMMAR_VERDICT` · `run_unload.sh` 92–100 행 · 잡 기록 `grammar_prereq=PASS`) | + RT 문법 PASS (`RT_GRAMMAR_VERDICT` · `ul_reader.py rt_grammar` (새 · `grammar` 명령 꼴) — 판정 JSON 검사 20 전부 참 · 같은 LMP · 덱 셋 + STL = 봉인 `RT_GRAMMAR_INPUTS` · 승인된 판독기 (`RT_GRAMMAR_READER`) 로 그 런 원자료 다시 읽기 · RJ · RJ2 만 (EXT 아님) · 잡 기록 `rt_grammar_prereq=PASS`) · `run_unload_ibb.sbatch` 13 행 주석 |
| 기존 시험 — 판독기 (`_mk_rj` 2095 행 = RT 없는 합성 RJ · 리뷰 표기 `_synth_rj` 2096 = 같은 함수) | R14 · R17 · R18 · R29 · R30 = RT 없이 RESTORED 등 단언 · R35 (3472–3530 행) = R/g2 · 원 덤프 열 결손 → UNCONFIRMED · 시점 S0 + 1 → VALUE_MISMATCH · 접선력 하나 → VALUE_MISMATCH · 열 결손 + UN 실패 → SYNTAX_FAIL · R16 중력 팔 (3784 행부터 · chk 3806–3828 행) | `_mk_rj` 가 정상 RT1 · RT2 출력도 쓴다 (실제 꼴 — 화면 `screen.txt` 에 경로 없음 · `log_screen.liggghts` 에 `read_restart ${ckpt}` + 치환 줄 · 잡 기록 `job_dir` · `rt_bin=` · `stage=RT2 ckpt=` · `rt_grammar_prereq=PASS`) → R14 · R17 · R18 · R29 · R30 기대 그대로 · R35 사례를 RT 덤프 (`post/rt_pair_S0`) 자리로 옮겨 같은 기대 (G2cp) · R/g2 · 원 덤프 쪽 같은 사례 = QA7 예면 15-5b 로 같은 기대 (열 결손 = UNCONFIRMED · 시점 = VALUE_MISMATCH) · 접선력 한 쌍 = 15-5b 문턱 안이면 통과 (보고) · QA7 아니오면 [연속] 보고만 (기대 바뀜을 시험 글에 적음) · 거부 쪽 사례 수 줄지 않음 (자리 이동 = 시험 약화 아님) · R16 그대로 (C12 = 개정 5) |
| 기존 시험 — 러너 (`ul_runner_test.py`) | M4 (RJ 차례 Ut0 → R → UN → UK · 단계 rc) · M15 · M16 (G0 · Ut0 실패 = R · UN · UK 안 돎) · M22 · M25 (문법 사전 점검) | M4 차례 · 단계 rc 에 RT1 · RT2 · M15 · M16 안 돈 단계에 RT1 · RT2 · M22 · M25 그대로 |
| 새 시험 | — | 판독기 R41 (G2cp 네 상태 · 15-5b (W 위반 · Σ\|Ft_원\| = 0 · 공통 쌍 0 · 다른 값 중복) · 판 표지 · 쌍 0 · post 목록 · rt.bin 결합 (sha256 다름 · 로그 경로 글자 다름 · 앞 시도 폴더 `<잡>.<꼬리>/RT1/rt.bin` · 로그 파일 없음 · 치환 줄 없음 · 둘 · 경로가 화면에만 (실제 꼴 아님) · `job_dir` ≠ 이 잡 폴더) · `rt_grammar_prereq` 줄 없음) · R42 (RT 봉인 값 = 실제 sha256 = `history_test/SHA256SUMS` 줄 · 판독기 · 표 · 덱 고침 → 사전 점검 거부 · R36 꼴) · 러너 M26 (RT 단계 · 건너뜀 · 실패 · 잡 기록 세 줄 (전체 경로) · 차례 UN → RT1 → RT2 → UK · 10:0 **RJ** = 덮어쓰기 없음 · 덱 기본 `ul_s0` 3,600,000 = CKPT0 / **RJ2** = `-var ul_s0 <S0′>` · CKPT0 = `restart_ext_<S0′>.bin` 두 꼴) · M27 (RT 문법 사전 점검 — `RT_GRAMMAR_VERDICT` 없음 · 판정 FAIL · 검사 ≠ 20 · 봉인 다름 = 거부 · 런 없음) · 생성기 GD17 (15-4 · 15-10 반례) · GD18 (생산 RT ↔ fixture RT 블록 rt 바이트 · 15-4) |
| 차등 시험 | — | 새 파일 `docs/reviews/p1_g2c_sandbox_20261104/test_g2cp_kitdiff.py` — 키트 `g2cp_compare` ↔ 샌드박스 `compare_g2cp.py` §3 판정 (둘 다 읽기만 · 합성 침대 · 30 열 · t07 꼴 변이) · 샌드박스 실행기 · 대조기 · `test_g2cp.py` 무변경 (초안 B 가 고치는 파일과 겹치지 않음 · 실행기 `inputs.md5` 목록 밖 — `run_g2cp.sh` 171 행) |
| 활성 규칙 (`active_rules.json` · 규칙 표 = `seal_kit.py` `RULES` 34–117 행) | 24 | 26 = + `g2cp_roundtrip` (15-5 · 15-5b · 증인 R41 · 차등) · `rt_grammar_prereq` (15-4b · 증인 R42 · M27) · 글 고침 = `restore_complete` (107 행 — RT 단계 · G2cp · 15-5b · 판 표지 · rt.bin 결합 · 관문 `rt_grammar_prereq=PASS`) · `parse_complete` (50 행 — G2c ULPR-04 → G2cp · 15-5b · 증인 R35 옮긴 사례 · R41) · `stage_rc` (103 행 — RT1 · RT2 단계 rc · 앞 단계 실패 = `stage=RT1 skipped` · `stage=RT2 skipped` · RT1 실패 = RT2 안 돎 · 증인 M26) · `grammar_prereq` (112 행 — 끝에 "RJ · RJ2 의 RT 문법 = `rt_grammar_prereq` (따로)" 한 줄) |
| 봉인 (`seal_kit.py`) | K1 "덱 64" (293–295 행) · 10 행 글 | K1 · 10 행 = 74 → `--write` (SHA256SUMS 86 줄 · active_rules.json) |
| 키트 README | §0 · §2 · §3 · §4 · 135 행 "덱 64" | 이름 (RT1 · RT2 · `rt.bin` · `post/rt_*` · `RT_GRAMMAR_VERDICT`) · 덱 표 · 단계 · 복원 판정 행 · 덱 74 (GO 문구 그대로 · QA5) |

## 15-3. 그대로

- R 덱 바이트 (PRE · POST · G1 · G2 · 26 열 쌍 덤프 · mesh · G3 · R_END · UN 소거) · UNread · UK · Ut0.
- G0 = 원 마지막 조각 덱 ↔ R 덱 (지금 그대로 · RT 는 GD17 lint 로 R 의 head · r_params 에 묶음 — 초안이 정함 · QA1 에 포함).
- 허용폭 식 1e-5 × max(\|D1\|, 그 열 \|D1\| 중앙값) · 이력 4 열도 같은 식 (메모 §3 · Q2) · `%.17g` 에서 좁히지 않음.
- NP 6 · LMP sha256 · S0 · 판정 범주 넷 · 다른 복원 입력 (reset 로그 다섯 · PRE = POST · UN 소거 · 이력 시험 H0–H5 + SYN + 총힘 시점 · 문법 fixture 사전 점검).
- REG §14 머리의 "바꾸지 않는 것" 전부 · 언로딩 팔 · 순서 §13-6 · RJ 323957 기록.

## 15-4. RT 덱 꼴 (생성기가 만든다 · 손으로 고치지 않는다 · 숫자 = 표에서만)

```
# (머리 주석 — 생성기가 종류를 적음 · RT1 ↔ RT2 는 이 주석만 다름)
# >>> block head      ← 같은 침대 R 의 head 블록과 바이트 같음 (r8 머리 글자 · read_restart ${ckpt} · compute cpl … 26 열 정의 포함)
# >>> block r_params  ← 같은 침대 R 의 r_params 블록과 바이트 같음 (ul_bed · ul_s0 (index · 10:0 = 3,600,000 = 148 행 튜플) · ul_atoms0 · ul_big)
# >>> block rt        ← 같은 경로 P (메모 §2) · 이력 열 = 이력 시험 소비자 꼴 · fixture RT 덱과 바이트 같음 (GD18)
thermo_style custom step atoms ke cpu
variable ul_step equal step
variable ul_step equal ${ul_step}
variable ul_na equal atoms
variable ul_na equal ${ul_na}
if "${ul_step} != ${ul_s0}" then "print 'UL_ABORT reason=start_step …'" "quit"
if "${ul_na} != ${ul_atoms0}" then "print 'UL_ABORT reason=start_atoms …'" "quit"
uncompute cpl
compute ul_ph all pair/gran/local pos id force force_normal force_tangential torque history contactArea delta contactPoint
dump ul_rp all local ${ul_big} ${out}/post/rt_pair_*.dump c_ul_ph[1] … c_ul_ph[30]
dump_modify ul_rp first yes format "%.17g × 30"
dump ul_ra all custom ${ul_big} ${out}/post/rt_atom_*.dump id type x y z vx vy vz omegax omegay omegaz radius
dump_modify ul_ra first yes format "%d %d %.17g × 10"
(QA4 = 넣되 보고만 — 원자 덤프 끝에 f_history_zwall_bot[1–4] · compute ul_wh … wall/gran/local id history force_normal + 판 local 덤프 = R 꼴)
run 0
undump ul_rp
undump ul_ra
write_restart ${out}/rt.bin          ← RT1 만 (RT2 = 이 한 줄 없음 · 나머지 바이트 같음 = 샌드박스 BW ↔ BR 꼴)
print "UL_RT_DONE bed=${ul_bed} step=${ul_step}"
```

- 키워드 차례 = 샌드박스 R · fresh 덱과 같음 → 30 열 차례 같음 (pos 1–6 · id 7–9 · force 10–12 · force_normal 13–15 · force_tangential 16–18 · torque 19–21 · history 22–25 · contactArea 26 · delta 27 · contactPoint 28–30).
- **GD17 lint** (생성된 덱에서): head · r_params 블록 바이트 = 같은 침대 R · 주석 · 빈 줄 빼고 RT1 − RT2 = `write_restart ${out}/rt.bin` 한 줄 · `uncompute cpl` < `compute ul_ph` < 덤프 < `run 0` < `write_restart` · ⑮ 셋 (함께 사는 pair/gran/local ≤ 1 · wall/gran/local ≤ 1 · 내린 compute 를 쓰는 덤프 없음 — 키트 README 132 · 392 행) · 블록 rt 밖 새 명령 0 · 새 ID = `ul_` 접두 · 반례 = 148 행 튜플에서 RT 빼기 (10:0 r_params ≠ R → 실패).
- **GD18 lint** (생성기 사이 · 2 회차): 생산 RT1 · RT2 (다섯 침대) 의 블록 rt 바이트 = `history_test/in.hist_rt1.liggghts` · `in.hist_rt2.liggghts` 의 블록 rt 바이트 (`make_unload_decks.py` ↔ `make_history_decks.py` 두 생성기 · 생산 쪽 selftest 가 history_test 덱을 읽기만) · 반례 = fixture 블록 rt 한 글자 다름 → 실패.
- 러너: RT1 = `run_deck "$JD/RT1" RT1 "$CKPT0" - 0` → 잡 기록 `rt_bin=$JD/RT1/rt.bin sha256=<…>` → RT2 앞 같은 파일 sha256 다시 `stage=RT2 ckpt=$JD/RT1/rt.bin sha256=<…>` → RT2 = `run_deck "$JD/RT2" RT2 "$JD/RT1/rt.bin" - 0` — 같은 NP 6 · LMP · mpirun 줄 · `EXTRA_VARS` (RJ2 = `-var ul_s0 <S0′>` 그대로 · 10:0 RJ = 없음) · `Loop time … on 6 procs` 검사 (`run_deck` 그대로 · 191–199 행) · 머리 `read_restart ${ckpt}` → RT2 로그 파일에 `read_restart ${ckpt}` 줄 + 치환 줄 (받은 BR `log.txt` 11–12 행 꼴).
- 덤프 = `post/` (경량 묶음에서 빠진다 · `run_unload.sh` 215 행) · `rt.bin` = `*.bin` 제외 · 단계 로그 `log_screen.liggghts` = 묶음에 들어감.  크기 어림 (7:3): 쌍 562605 × 30 열 ≈ 350–370 MB × 2 (11-12 625 B/쌍 산술) · 원자 ≈ 40 MB × 2 · rt.bin ≈ 80 MB [추정].

## 15-4b. RT 문법 fixture (RJ 전 · 결과 0 건)

- 까닭: RT 문법의 **조합** (판 mesh 머리 + `uncompute cpl` → 30 열 `pair/gran/local … history` → `%.17g` 덤프 → `write_restart` → 새 프로세스 `read_restart rt.bin`) 이 어느 시험에서도 함께 돈 적이 없다 — 요소는 흩어져 지났다 (이력 소비자 = 판 mesh + `uncompute cpl` + 7 열 `id history` · `in.hist_consumer.liggghts` 68–78 행 · job 283122 PASS / 문법 fixture = `write_restart` · 새 프로세스 `read_restart` · `%.17g` · `in.hist_grammar.liggghts` 27 · 95 · 139 행 · `uncompute` 없음 / 샌드박스 = 30 열 · 판 mesh 없음) · 키트 selftest 는 LIGGGHTS 를 안 돌린다 · REG §14-9 (909 행) = 문법 fixture "본 R 전 PASS (생산 침대 쓰기 전)".
- 덱 둘 (새 파일 · `make_history_decks.py` 가 만든다): 이력 소비자 머리 (`in.hist_consumer.liggghts` 10–54 행 글자 · 판 mesh · `read_restart ${ckpt}` · `compute cpl` 26 열 정의 포함 · 그 뒤 소비자 관측 · `print` 는 뺌) + 블록 r_params (fixture 표 `rt_grammar_params.json` — `ul_bed` = `hist_rt` · `ul_s0` = 2000 (생산자 최종 step = `history_params.json` steps 10 + 1000 + 990) · `ul_atoms0` = 20 (입자 20) · `ul_big` = 1000000000 (`grammar_probe.big` 과 같음) · 생성기가 `history_params.json` 값과 같은지 대조 (읽기만)) + 블록 rt (생산 RT 와 바이트 같음 · GD18).
- 흐름: 생산자 (`in.hist_producer.liggghts` · step 2000 · `write_restart fixture.bin` = 명령 파일) → RT1 (fixture.bin) → `rt.bin` → 새 프로세스 RT2 (RT1/rt.bin) · NP 6 · 러너 `run_history.sh --rt-grammar-only` (런 폴더 `rtg_<시각>` · 단계 `ckpt.txt` · 화면 `screen.out` · 로그 `-log <단계>/log.liggghts` = 지금 꼴 · RT1 끝 · RT2 앞 rt.bin sha256 두 줄 = 그 런 `run_manifest.txt`).
- 판정 (결과 전 · 검사 20 · 판독기 `read_rt_grammar.py` → `rt_grammar_verdict.json` · schema `ps45_unload_rt_grammar_verdict_v1` · PASS ⇔ 20 전부 참 · exit_code 0 · 기존 `grammar_verdict.json` 과 따로):

| # | 검사 | 참의 조건 |
|---|---|---|
| 1 | `P_tech` | 생산자 rc 0 · `fixture.bin` 있음 |
| 2–3 | `RT1_exists` · `RT2_exists` | 단계 폴더 · `deck.txt` = 그 덱 이름 |
| 4–5 | `RT1_args` · `RT2_args` | `ckpt.txt` 글자 = `<런>/P/fixture.bin` · `<런>/RT1/rt.bin` · `np.txt` = 6 |
| 6–7 | `RT1_tech` · `RT2_tech` | rc 0 · 배너 · ERROR · UL_ABORT 없음 · `Loop time … on 6 procs` |
| 8–9 | `RT1_marker` · `RT2_marker` | `UL_RT_DONE bed=hist_rt step=2000` 정확히 하나 |
| 10–11 | `RT1_resets` · `RT2_resets` | 화면 reset 줄 = 표 `expected_reset_fixes` (이력 시험 표 값 복사 + 대조) |
| 12 | `bind_sha` | 런 기록 rt.bin sha256 RT1 끝 = RT2 앞 = 파일 실제 |
| 13 | `bind_path` | RT2 **로그 파일** `log.liggghts` 의 `${` 없는 `read_restart` 줄 정확히 하나 · 그 경로 글자 = RT2 `ckpt.txt` = `<런>/RT1/rt.bin` |
| 14 | `post_list` | 두 단계 각각 `post/` = `rt_pair_2000.dump` · `rt_atom_2000.dump` 하나씩 |
| 15 | `pair_read` | 두 쌍 덤프 머리 · 열 이름 = `c_ul_ph[1]`–`[30]` 차례 · 행 수 · 유한 · ID 정확한 양의 정수 |
| 16 | `atom_read` | 두 원자 덤프 전부 읽힘 · 원자 20 |
| 17 | `step` | TIMESTEP 넷 = 2000 |
| 18 | `pairs` | 쌍 > 0 |
| 19 | `g2cp` | 키트 `g2cp_compare` (RT2 ↔ RT1) PASS |
| 20 | `hist_value` | RT1 shear 3 열 = 생산자 끝 이력 (`P/producer/pair_2000.dump` · 이력 시험 소비자 판독 규칙 · 허용폭 = `history_params.json` `tolerances` 그대로 · 판독 함수 = 새 판독기에 복사 · `read_history.py` 무변경) · deltaMax = 판정 밖 (setup 이 올림 · 메모 §0-1 ①) |

- 봉인 (`ul_reader.py` · 새 값 · 지금 `GRAMMAR_*` 꼴): `RT_GRAMMAR_CHECKS` (위 20 이름) · `RT_GRAMMAR_INPUTS` (`in.hist_producer` · `in.hist_rt1` · `in.hist_rt2` · `plate_hist.stl` sha256) · `RT_GRAMMAR_READER` (`read_rt_grammar.py` · `rt_grammar_params.json` sha256) · `rt_grammar_prereq()` (`grammar_prereq` 꼴 — 판정 JSON · 같은 LMP · 덱 봉인 · 승인된 판독기로 그 런 원자료 다시 읽어 검사 20 = JSON) · 시험 R42 (R36 꼴).
- 실행: ibb 한 번 (1저자 GO · 수 분 · 10-15 '문법 실행 2' 꼴 · 지금 문법 fixture 와 같은 지위 = Codex GO 와 무관 · REG 909 행) · PASS = RJ · RJ2 러너 사전 점검 조건 (15-2).
- 실패 = 덱 · 판독 고침 (시험 먼저) → 다시 · RJ 시도 셈 밖 (QA6).

## 15-5. 판정 규칙 (결과 전 · 키트 판독기)

| G2cp | 조건 | 복원 판정 |
|---|---|---|
| PASS | RT1 · RT2 기술 성공 (러너 단계 기록 PASS · rc 0 · ERROR · UL_ABORT 없음 · 배너 · `on 6 procs` · `UL_RT_DONE`) ∧ rt.bin 결합 (잡 기록 sha256 RT1 끝 = RT2 앞 = 파일 실제 ∧ 경로 셋 글자 같음 = 잡 기록 `rt_bin=` · `stage=RT2 ckpt=` · RT2 **로그 파일** `RT2/log_screen.liggghts` 의 `${` 없는 `read_restart` 줄 (정확히 하나) — 셋 = 잡 기록 `job_dir` + `/RT1/rt.bin` 이고 `job_dir` 의 실제 경로 = 판독기가 받은 잡 폴더 (`<루트>/<침대>/<잡>`) · 꼬리 대조 아님: 이름 바꾼 앞 시도 `<잡>.<꼬리>/RT1/rt.bin` 은 다름 · 화면 `screen.txt` 는 대조 자리 아님 — 경로를 안 찍음: 받은 묶음 BR `out.txt` 2 행 ↔ `log.txt` 11–12 행) ∧ post 목록 = `[rt_pair_<S0>.dump]` · `[rt_atom_<S0>.dump]` 하나씩 (두 단계 각각) ∧ 두 쌍 덤프 전부 읽힘 (머리 · 열 이름 = 정확히 `c_ul_ph[1]` … `[30]` 차례대로 · 행 수 · 유한 · ID 정확한 양의 정수) ∧ 쌍 수 > 0 ∧ TIMESTEP 둘 다 = S0 (RJ2 = S0′) ∧ 쌍 집합 같음 ∧ 다른 값 중복 키 0 ∧ 공통 쌍 · 열마다 \|D2 − D1\| ≤ 1e-5 × max(\|D1\|, 그 열 \|D1\| 중앙값) | 다른 관문 (15-5b · QA7 예면 포함) 모두 PASS 면 RESTORED |
| FAIL | 값 · 집합 · 다른 값 중복 · TIMESTEP 위반 · 덤프 구조 · 읽기 문제 (필수 열 결손을 뺀 것 — 비유한 · ID 꼴 · 머리 · 행 수 · 열 수 · 열 이름 더함 (31 열) · 중복 이름 · 차례) — ULPR-04 범위 그대로 (REG 961 행 · `ul_gates.py` 343–348 행 동작) | VALUE_MISMATCH |
| NOT_COMPUTED | 쌍 덤프 없음 · 필수 열 (`c_ul_ph[1]`–`[30]`) 하나라도 없음 (ULPR-04 꼴) · 쌍 0 (두 쪽 0 행 = 지금 `g2c_compare` 꼴이면 PASS 가 되므로 따로 막음 · `ul_gates.py` 352–371 행) · post 목록 어긋남 · rt.bin 결합 기록 없음 (잡 기록 `job_dir` · `rt_bin=` · `stage=RT2 ckpt=` · RT2 로그 파일 · 로그의 치환 줄 중 하나라도 없음) | UNCONFIRMED |
| (계산 안 함) | RT1 · RT2 기술 실패 · rt.bin 결합 어긋남 (sha256 다름 · 경로 셋 글자 다름 · 치환 줄 둘 이상 · `job_dir` 실제 경로 ≠ 이 잡 폴더 = 등록된 왕복이 아님) | SYNTAX_FAIL (REG §14-10) |

- 정규화 = 지금 G2c 와 같음: 무순서 키 (작은 id, 큰 id) · 방향 바뀐 행 = 위치 맞바꿈 · 힘 9 · shear 3 부호 반전 · deltaMax 그대로 · 위치 · 접점 = 상자 (0.05 × 0.05) 로 감음 · torque · 주기 표지 = 판정 밖 · 집합 차를 "MPI 끝자리" 로 면제하지 않음 (REG §12-1).
- D1 = RT1 (기준쪽) · D2 = RT2.  [왕복] 의 주장은 D2 = D1 (D1 = 파일 원값이 아님 — setup 이 deltaMax 를 올린다 · 메모 §0-1 ①).
- 복원 판정 사상 = 지금 그대로 (`ul_gates.restoration_verdict` 413 행): G2cp 는 1619 행 목록의 G2c 자리 (FAIL → VALUE_MISMATCH · NOT_COMPUTED → UNCONFIRMED) · 단계 기술 = R · UN · (7:3) Ut0 · RT1 · RT2 · reset 로그 = R · RT1 · RT2 셋 다 (결손 = VALUE_MISMATCH · 지금 R 규칙 그대로) · G1 · G2 · mesh md5 · G3 그대로 · 증서에 `restore_rule = "rev4_g2cp"` (15-2 관문).
- 함께 적음 (판정 아님): 비트 같은 쌍 수 · 원자 12 열 비트 같음 · 두 덤프 sha256 같음 · 열별 최대 상대차 · 판별력 (D1 접선력 0 아닌 몫 · \|shear\| > 0 몫) · 주기 표지 쌍 수 · (QA4) 벽 열.
- [연속] = `ul_gates.g2c_compare(R/g2/contact_S0, in/contact_S0)` 그대로 → `checks['G2c_cont']` · 상태 · n_mismatch · 열별 수 — 판정 · 다음 제출 관문 · `restoration_verdict` 입력 아님 (QA7 예면 15-5b 만 입력).

## 15-5b. [연속] 결과 전 문턱 — 거친 이력 소실 막이 (QA7 · 거부 쪽 새 규칙 · 2 회차에 지표 · 문턱 바꿈)

- 까닭: [왕복] 은 두 쪽이 같이 잃으면 통과한다 (메모 §2 맹점).  reset 로그 = 경로 증거 (값 아님 · 지금 R 화면만 — `ul_reader.py` 1570–1573 행) · H0–H5 = 20 입자 · 명령 파일 fixture (REG 787 행 · §13-7-4) · RT 문법 fixture (15-4b) = fixture 수준 → 생산 경로에서 "이력이 값으로 읽혔다" 의 값 수준 증거는 [연속] 분포뿐.  작은 반례: RT1 이 shear 를 0 으로 읽음 → rt.bin 0 → RT2 0 → G2cp PASS · R 화면 reset 다섯 → RESTORED (이 막이 없으면).
- 대상 (침대마다 · RJ · RJ2): **ⓡ** R `g2/contact_S0` ↔ 원 `contact_S0` (= [연속] 입력 그대로) · **ⓣ** RT1 `post/rt_pair_S0` 의 26 열 사영 (30 열에서 history 22–25 를 뺀 차례 = c_cpl 1–26) ↔ 원 `contact_S0`.
- 쌍 판단 (11-02 도구 정의 그대로 · `rj_g2c_cause_check.py` 336–341 행): 공통 쌍마다 방향 맞춘 접선력 (열 16–18) · r = \|Ft − Ft_원\| / \|Ft_원\| (\|Ft_원\| > 0 인 쌍) · reset_like = r > 0.5 인 쌍.  키 · 방향 · 중복 = 15-5 · `ul_gates._contacts` 와 같은 규칙 (같은 값 중복 = 한 행 · 수 보고 / 다른 값 중복 = FAIL).
- **판정 지표 W (2 회차)** = Σ\_{reset_like 쌍} \|Ft_원\| ÷ Σ\_{공통 쌍} \|Ft_원\| (\|Ft\| 가중 reset 몫 — 쌍 판단은 그대로 · 모으는 법만 \|Ft_원\| 가중).
- **문턱 (결과를 본 뒤 정함 · 2026-11-12 2 회차 · 머리 표지 · ⓡ · ⓣ 각각)**: W ≤ **0.05** ∧ 쌍 집합 같음 (빠짐 · 더함 0).  보고만 (판정 아님): reset_like 수 · 몫 (1 회차 판정 0.03 = 거둠) · r 중앙 (1 회차 판정 1e-2 = 거둠) · q95 · 무너짐 몫.
- 왜 W 인가 (같은 쌍 판단 · 모으는 법 다섯 · 값 = 15-1 · 머리):

| 지표 | 정직 B ↔ A(N) | 정직 C ↔ A(N) | 7:3 사후 | 전부 잃음 | 정직 쪽 약점 |
|---|---|---|---|---|---|
| reset_like 몫 (1 회차 판정) | 0.0154 | 0.0016 | 0.0012 | 1.0 | 갓 닿은 · 접선 하중 작은 쌍이 걸림 (B 48 중 27 = \|Ft_원\| 하위 10 %) — 움직이는 침대일수록 오름 |
| r 중앙 (1 회차 판정) | 6.2e-4 | 0 | 7.8e-5 | 1.0 | 전형 쌍의 한 step 증분 — 침대 움직임에 비례 (샌드박스 = 7:3 의 8 배) |
| 무너짐 몫 (\|Ft_t\| < 0.5 \|Ft_원\|) | 0.0061 | 0.0013 | [미확인] | ≈ 1 | 쌍 수 기준 — 갓 닿은 쌍 (setup 힘 ≈ 감쇠뿐) 이 걸림 |
| \|Ft_원\| 하위 10 % 뺀 몫 | 0.0075 | 0.0014 | [미확인] | ≈ 1 | 자르는 점 (10 %) 이 침대마다 다름 |
| **W (고름)** | **0.0031** | **0.0004** | [미확인 · 계산 안 함 = 결과 전] | **1.0** | 정직하게 걸리는 쌍 = 하중 작은 쌍 → 무게가 작다 |

- 정직 여유: 0.05 = B 의 ×16 · C 의 ×128 (1 회차 r 중앙 문턱의 B 여유 ×16 과 같은 크기) · 샌드박스 (중력 정착 침대) 는 7:3 보다 많이 움직인다 (r 중앙 ×8 · 몫 ×13) → 생산 침대 여유는 더 클 것 [추정].
- 소실 반례를 막는 힘 (산술 `docs/reviews/p1_g2c_sandbox_20261104/internal_reviews/p1next_AB_20261112/f2_guard_power.py` → `docs/reviews/p1_g2c_sandbox_20261104/internal_reviews/p1next_AB_20261112/f2_guard_power_out.txt` · 정직 B 위에 시험 Ft → 0 · 감쇠 몫 무시 [추정]):

| 반례 (잃는 쌍) | W | 0.05 대비 | 1 회차 몫 (0.03) |
|---|---|---|---|
| 전부 (RT1 shear 0 → rt.bin 0 → RT2 0 · R · RT1 둘 다) | 1.0 | 잡힘 ×20 | 잡힘 |
| 주기 표지 1 쌍만 (334 · 쌍 10.7 %) | 0.106 | 잡힘 ×2.1 | 잡힘 (0.12) |
| NP 6 격자 (3×2×1) 하위영역 하나 | 0.142–0.213 | 잡힘 ×2.8–4.3 | 잡힘 (0.149–0.223) |
| 2×2×1 하위영역 하나 | 0.209–0.295 | 잡힘 | 잡힘 |
| 6×4×1 하위영역 하나 (7:3 원 격자 꼴) | 0.015–0.081 | 24 중 8 만 | 잡힘 (0.040–0.072 · 정직 배경 0.0154 포함) |
| 무작위 쌍 5 % · 2 % | 0.056 · 0.020 | 잡힘 (가장자리) · 못 잡음 | 잡힘 · 잡힘 (0.063 · 0.033) |
| \|Ft\| 상위 1 % · 2 % | 0.109 · 0.175 | 잡힘 | 못 잡음 (0.025) · 잡힘 (0.035) |
| \|Ft\| 하위 25 % · 50 % | 0.018 · 0.081 | 못 잡음 · 잡힘 | 잡힘 · 잡힘 |

- 7:3 은 W 를 아직 안 쟀다 (11-02 도구는 몫 · r 만) → 7:3 도 결과 전 (A-4) · 판별 = 다섯 침대 · RJ2 · ⓣ.
- 10:0 RJ: S0 3,600,000 = 판 압력 조건 1.03 % (조건 1 % 를 못 채움 = 미이완 판정 · REG 93 · 527 행 · PHASE 4 + 59,999 ↔ 7:3 S0 = + 75,000 · 조건 채움) — 여기서 위반이면 EXT 관문 (`ul_reader.py` 1247–1251 행) 이 닫혀 10:0 전체 (EXT · RJ2 · U) 멈춤.  정직하게 W > 0.05 가 되려면 접선력 총합의 5 % 를 진 쌍들이 한 step 에 자기 \|Ft\| 의 절반 넘게 바뀌어야 한다 — W = 한 step 증분의 두 배보다 작은 \|Ft\| 를 진 쌍들의 하중 몫이라 침대 움직임과 함께 오르지만, 7:3 보다 8 배 움직이는 샌드박스에서 0.0031 · 위험 = 15-12 [추정].
- 결과: 위반 = 복원 VALUE_MISMATCH (이력 소실 의심 · U 없음 · 멈춤 → 1저자) · 그 시도는 VALUE_MISMATCH 그대로 — 뒤에 "늦은 이력 · 정직한 움직임이었다" 로 다시 읽어 RESTORED 로 바꾸지 않는다 · 지표 · 문턱을 바꿔 다시 = 새 등록 (개정) / 계산 못 함 (파일 없음 · 필수 열 결손 · 공통 쌍 0 · Σ\|Ft_원\| = 0) = UNCONFIRMED / 덤프 구조 · 시점 · 다른 값 중복 = FAIL (15-5 와 같은 분류).
- 주장 안 함: 원 런 H(S) 복구 · 한 step 늦은 이력 같은 작은 차를 가름 (문턱이 일부러 넓다) · \|Ft\| 몫 0.05 밑에 갇힌 부분 소실 (위 표 — 무작위 쌍 2 % · \|Ft\| 하위 25 % 쌍 · 6×4 하위영역 24 중 16) · 모든 쌍 r < 0.5 인 넓은 중간 크기 차 (여러 step 늦은 이력 = 초안 B 결론 ② 가 샌드박스에서 잼 · 재료 상수 = G0) · 다른 침대의 r · W 분포가 샌드박스 · 7:3 과 같음.

## 15-6. 결과 전 예측 (ibb RJ · RJ2 · NP 6)

| # | 대상 | 예측 = 맞음 기준 | 근거 · 표지 | 틀리면 |
|---|---|---|---|---|
| A-1 | RT1 · RT2 기술 | rc 0 · `on 6 procs` · step = S0 (RJ2 = S0′) · 원자 = 표 `ul_atoms0` · 화면 reset 로그 다섯 · rt.bin 결합 같음 (sha256 · 로그 파일 경로 셋) · 쌍 수 = R `g2/contact_S0` 쌍 수 | R 과 같은 머리 · 같은 파일 · rt.bin 이 같은 fix 상태를 담음 [추정] · RT 문법 fixture PASS (15-4b) | SYNTAX_FAIL · 그 침대 멈춤 (REG 그대로) |
| A-2 | G2cp 판정 | PASS · n_mismatch 0 | 직렬 다 · 라 PASS (11-12) + 초안 B §4 결론 ① (두 NP 모두) · NP 6 · 상자 0.05 로 옮김 = [추정] | VALUE_MISMATCH = 그 침대 U 없음 · 멈춤 → 1저자 · 직렬 · 초안 B 와 다른 까닭부터 |
| A-3 | 비트 · 바이트 | 비트 같은 쌍 = 전부 · 원자 12 열 비트 같음 · 두 쌍 덤프 sha256 같음 | [추정] — 직렬 다-값 · 다-바이트 · 라-값 · 라-바이트 맞음 (11-12) + 초안 B M-다/라-바이트 (NP 2 · 4 · 결과 전) · NP 6 은 직접 근거 없음 | 비트 · 바이트 예측만 거둠 (판정 PASS 면 판정 그대로) |
| A-4 | [연속] · 주기 S0 다섯 (RJ) | FAIL (n_mismatch > 0) · 7:3 = n_mismatch 545583 · R 쌍 덤프 sha256 `193e6e6ca2e6833d3204fd26615b61b5de32f6e65d931fcdbd560c215365951f` (323957 과 같음 · `docs/reviews/dem_unloading_rj_g2c_cause_20261102/ibb_result_20261102.json` 21 행) · 15-5b ⓡ = W ≤ 0.05 (7:3 W 계산 안 함 = 결과 전) · 보고 칸 reset_like 685 · r 중앙 7.8e-5 (같은 덤프 · 같은 정의면 산술) | ㉠ + ㉡ · 7:3 재현 = 같은 LMP · R 덱 · NP · 격자 · S0 → 같은 R 덤프 [추정 · 결정성] · 정직 reset 쌍 = 하중 작은 쌍 (샌드박스 B 48 중 27 = \|Ft_원\| 하위 10 %) → W ≪ 몫 [추정] | 보고만 (W > 0.05 = 15-5b 규칙 → VALUE_MISMATCH) · 7:3 수 · sha256 다르면 결정성 서술만 거둠 |
| A-5 | [연속] · 10:0 RJ2 (S0′ = **주기** 파일 · 쓴 NP 6 = 읽는 NP 6) | FAIL (n_mismatch > 0) · 불일치는 넓게 (A-4 꼴 · 크기 · 자리는 미리 안 정함) | ㉠ + ㉡ — 주기 파일 (15-1 S0 꼴) · 직렬 같은 꼴 = B [연속] FAIL 3107/3111 (11-12 `reports.연속`) · MPI 크기 = 초안 B | 보고만 |
| A-6 | 나머지 관문 | REG 기대 그대로 | R 덱 · 판독 안 바꿈 | REG 규칙 그대로 |
| A-7 | 벽 (QA4 · 보고) | RT2 = RT1 (바닥 4 열 · 판 local · 비트) | 첫 setup 뒤 상태를 rt.bin 이 담음 [추정 · 샌드박스 밖 · 메모 §0-1 ③] | 벽 왕복 서술만 거둠 |
| A-8 | 15-5b (QA7 예면) | ⓡ · ⓣ 모두 W ≤ 0.05 · 쌍 집합 같음 (다섯 침대 RJ · **10:0 RJ (S0 3,600,000)** · RJ2) · ⓣ 지표 ≈ ⓡ (같은 경로 · 둘 다 setup) | 샌드박스 정직 W 0.0031 (×16) · 7:3 몫 0.0012 · r 중앙 7.8e-5 (샌드박스의 8 분의 1 움직임) · 10:0 S0 = 판 압력 조건 1.03 % (1 % 를 0.03 %p 넘음) = 7:3 과 같은 자릿수 [추정 · 다른 침대 미확인] | VALUE_MISMATCH (규칙) → 그 시도 RESTORED 안 됨 · 멈춤 → 1저자 (10:0 RJ 면 EXT 관문 닫힘 = 10:0 전체 멈춤) · 이력 소실 ↔ 정직한 움직임의 큰 차 가름부터 · 지표 · 문턱 바꿔 다시 = 새 등록 |

- [이력] 앵커 = 해당 없음 (원 덤프 · EXT 덤프에 이력 열 없음).  "이력이 실제로 읽혔다" 는 [왕복] 밖 — 15-5b (값 수준 · 거친 소실만) · H0–H5 · RT 문법 fixture (fixture 수준) · reset 로그 (경로).

## 15-7. C12 중력 팔 — 이번 밖 (QA2 · 개정 5 예고)

- 지금: `_g_restore` (`ul_reader.py` 1096–1118 행) 가 G_ 팔 setup 덤프 ↔ 출처 팔 R_M **창 끝 (in-run)** 덤프로 G2c → ㉡ 때문에 예측된 실패 (R_M = `write_restart` 명령 파일 · `make_unload_decks.py` 410 행 — 명령이어도 직렬 [연속] C 가 kit26 FAIL 331).
- 이번 밖으로 두는 까닭: GT1 · GT2 덱 꼴이 15-4 수준으로 안 정해졌다 — G_ 덱 머리 뒤 `arm_dt` 블록 (G_UVb · G_UT3 = 5e-07) · `ul_params` 의 `include ${ul_base}` · `g_start` 의 `include ${ul_state}` · 관측 블록의 `compute ul_wh … wall/gran/local` 을 GT 에 어떻게 둘지 · 덱 수 (출처 팔 넷 × 침대 다섯 또는 침대마다 한 쌍) · GT 실패 때 G_ 덱 처리.  G_ 팔은 U 뒤라 RJ 와 무관.
- 남기는 것: **G_ 팔 제출 전에** 개정 5 (GT1 · GT2 · 판정 = GT2 ↔ GT1 · 옛 C12 G2c = [연속] 보고 · 15-5 · 15-5b 와 같은 규칙) 비준 필요 — 지금 규칙이면 예측된 실패 (11-02 보고 §6 Q3) · [이력] 후보 (출처 팔 R_M 창 끝 쌍 덤프에 이력 열) = U 덱 변경 · 그때.

## 15-8. 주장하지 않는 것

- 원 런 스텝 끝 덤프 ↔ 재개 setup 의 연속성 · `write_restart` 비트 동일성 (비트 · 바이트 = 예측일 뿐).
- G2cp PASS = 이력이 실제로 읽혔다 (맹점 — 두 쪽이 같이 잃으면 통과 · H0–H5 = 20 입자 · 명령 파일 fixture (REG §13-7-4) · reset 로그 = 경로 증거 (값 아님) · RT 문법 fixture = fixture 수준 · 생산 경로의 값 수준 막이 = 15-5b (QA7 · \|Ft\| 가중 몫 · 거친 소실만 · 한 step 늦은 이력 같은 작은 차는 못 가름)).
- 15-5b 가 모든 소실을 잡는다 — **\|Ft\| 몫 0.05 밑에 갇힌 부분 소실은 못 잡는다** (산술: 무작위 쌍 2 % W 0.020 · \|Ft\| 하위 25 % 쌍 0.018 · 7:3 원 격자 꼴 6×4 하위영역 하나 = 24 중 16 · 15-5b 표) · 모든 쌍 r < 0.5 인 넓은 중간 크기 차도 못 잡는다 (여러 step 늦은 이력 · 크기 바뀐 이력).
- 주기 S0 파일이 원 런 H(S) 를 담는다 — **S 상태 = 파일 상태** (다섯 S0 · 10:0 S0′ · S0″ 모두 주기 · x · v · ω · 벽 이력 = S 끝 · 쌍 shear = S 힘 계산 전 사본 · 직렬 = H(S−1) · MPI = 초안 B) · 10:0 결과를 "동기한 이력에서 출발" 로 적지 않는다 (동기 출발 = S0′ 를 끝 3,660,000 명령 파일로 바꾸는 C18 · §12-11 개정 · 이번 밖).
- RJ 323957 소급 PASS · "등록 기대 오류로 설명됨" (11-02 보고 §4 — 표지로만).
- 허용폭 변경 · P1 수치 인증 · 언로딩 물리 결과 · 벽 이력 판정 (QA4 = 보고만) · `force_normal` 차이 = 법선 모델 힘 차이 · 15-5b 통과 = 원 런 이력 복구.
- NP 2 · 4 (초안 B) 결과가 NP 6 · 생산 침대에서 같다는 것 (추정으로만 씀).
- 넘김 (원장 후보 · 지우지 않음): REG §3-2 237 행 — ㉠ 확인 뒤, 주기 restart 로 이은 ps45 압축 조각 (7:3 r3 · r6–r8) 은 조각 경계마다 늦은 이력으로 이어졌을 것 [추정 · 직렬 = 1 step · MPI · NP 바뀜 = 초안 B · 크기 미측정] · 이 개정은 다루지 않음 · 등재 = 다음 원장 커밋.

## 15-9. 순서

1. 이 판 (2 회차 고침) → 1저자 비준 (QA7 다시 물음 · 나머지 = 1저자 11-12 정함 · 15-11) — 초안 B 비준과 함께.
2. **Codex 설계 확인** (A · B 함께 · Codex 지금 남은 한 번 · 비준 뒤 · 구현 전 · 1저자 11-12) — 요청서 머리 = 15-13 · B §14.  HOLD 면 고침 → 1저자 (구현 시작 = 1저자 GO).
3. 키트 수정 (시험 먼저 — 고치기 전 실패 → 고친 뒤 통과 · 변이 시험): 생성기 (148 행 · RT 덱 · GD1 · GD17 · GD18) · 러너 (RT 단계 · `job_dir` · rt.bin 결합 두 줄 · RT 문법 사전 점검 · M4 · M15 · M16 · M26 · M27) · 판독기 (G2cp · [연속] · 15-5b · 판 표지 · rt.bin 결합 (로그 파일) · `rt_grammar_prereq` · R14–R35 옮김 · R41 · R42) · `ul_gates` (`g2cp_compare` · `cont_guard`) · 활성 규칙 26 · `seal_kit.py` K1 · README · 봉인 다시 → 게이트 → 커밋 · push.
4. 차등 시험 (`test_g2cp_kitdiff.py`) · RT 문법 fixture 덱 · 표 · 판독기 · 러너 모드 (`history_test/` · 시험 먼저).
5. 내부 반박 리뷰 (코드 · CLAUDE.md 사전 공격 ①–③ · Codex 아님).
6. RT 문법 fixture ibb 한 번 (1저자 GO · 15-4b) → PASS.
7. 초안 B (B §12 차례 · 단계마다 1저자 GO · 3–6 과 나란히 가능 = 파일 겹침 없음) → B §4 결론 ① (정의 그대로 — 두 NP 모두 판정 다 · 라 PASS ∧ M-다-값 · M-라-값 맞음 · 부분 결론 없음 · 쓰는 시도 = B §9 시도 셈).  판정 PASS ∧ 값 틀림 = 선행 조건 아님 → 멈춤 → 1저자 (결과 전 · 11-12).
8. **Codex 발사 GO** (리셋 약 11-15 뒤 · Rint ② 봉인 전 묶음과 함께 · B 결과 + RT 문법 fixture 결과 붙여 · 1저자 11-12) → 1저자 발사 승인.
9. ibb RJ (새 폴더 · 새 시도 · 침대 차례 = REG §13-5 ② 그대로 · 7:3 = QA6).

- 단계마다 1저자 GO · 자동 다음 단계 없음 · B 결론 ① 이 안 서면 RJ 보류 — 그 NP 의 기술 실패 · NOT_COMPUTED = 그 NP 다시 (새 빈 폴더 · 1저자 승인 · B §9 시도 셈 · 한도) / FAIL · 판정 PASS ∧ M-값 틀림 = 멈춤 → 1저자 (같은 등록으로 다시 돌려 결론 ① 을 세우지 않는다 = B §9).

## 15-10. 보장 · 작은 반례 (구현 뒤 내부 반박 리뷰 · Codex 설계 확인이 깨 볼 것)

| 보장 | 깨 볼 작은 반례 |
|---|---|
| RT1 · RT2 는 읽는 파일만 다르다 | RT1 = RT2 + 두 줄 · `write_restart` 가 `run 0` 앞 (setup 없이 F′ = F → 맹점 통과) · 러너가 두 단계에 다른 `-var` · NP · 10:0 RT 의 r_params ≠ R (148 행 튜플 빠짐 → RJ RT1 = UL_ABORT) · 머리 주석만 다른 RT1 · RT2 를 GD17 이 실패로 봄 · fixture 블록 rt 만 한 글자 다름 (GD18) |
| RT2 가 RT1 의 rt.bin 을 읽었다 | RT2 ckpt = 이름 바꾼 앞 시도 폴더 `<잡>.<꼬리>/RT1/rt.bin` (꼬리 같음 · 전체 경로 다름) · 다른 폴더의 같은 이름 파일 · RT1 뒤 rt.bin 바뀜 · 결합 기록 없음 · RT2 로그 파일 없음 · 로그에 치환 줄 없음 · 둘 · 경로가 화면에만 있는 합성 꼴 (실제 꼴 아님) · `job_dir` 에 `//` 가 섞인 정직한 글자 (세 글자 같고 실제 경로 같음 → 통과해야) |
| G2cp PASS = 같은 경로 재현 | 두 쪽 쌍 0 (→ NOT_COMPUTED 인가) · post 에 rt_pair 둘 (다른 step) · 옛 판독기 증서 (판 표지 없음) 로 관문 통과 · `rt_grammar_prereq` 줄 없는 잡으로 관문 통과 |
| 이력 소실 막이 (15-5b · QA7 예) | RT1 만 shear 0 · R · RT1 둘 다 shear 0 · \|Ft\| 상위 1 % 만 잃음 (W 0.109 → 잡혀야) · 하위 25 % 만 잃음 (W 0.018 → 통과 = 주장 안 함) · 원 덤프 열 결손 · 공통 쌍 0 · Σ\|Ft_원\| = 0 · 다른 값 중복 · 샌드박스 정직 B (W 0.0031 → 통과) |
| 옛 G2c 는 판정 밖 | 1619 행 목록에 'G2c' 가 남음 · 다음 제출 관문이 `G2c_cont` 를 읽음 · [연속] 열 결손이 (QA7 아니오인데) UNCONFIRMED 로 샘 |
| 필수 열 결손 = NOT_COMPUTED · 구조 = FAIL | 열 이름 하나 중복 · `c_ul_ph[30]` 없음 · 31 열 · 26 열 덤프를 RT 자리에 둠 · 비유한 값 (FAIL 인가) |
| 30 열 판정 = 샌드박스 §3 판정 | 같은 합성 침대에서 상태 · n_mismatch 다름 (차등) · shear 부호 반전 빼기 · deltaMax 부호 반전 넣기 변이 |
| TIMESTEP = S0 | RT2 가 S0 + 1 · RT1 덤프가 `run 0` 전 `write_dump` |
| RT 차례 (UN 뒤 · UK 앞) | UK 기술 실패가 복원 판정을 바꿈 · RT 실패인데 UK 가 돎 |
| RT 문법 fixture = 생산 RT 문법 | fixture 표가 `history_params.json` 과 다름 (생성기 대조) · 검사 20 중 `bind_path` 를 화면에서 읽음 · 봉인 값과 다른 판독기 사본으로 PASS (R42 · M27) · `read_history.py` 가 바뀌어 R36 이 깨짐 |
| 거부 쪽 사례 수 줄지 않음 (R35 자리 이동) | 옮긴 사례 하나를 빼도 시험이 초록 |

## 15-11. 1저자가 정할 것 (1저자 11-12 결정 반영 · 이번 고침이 바꾼 것만 다시 물음)

- 초안이 정한 것 (질문 아님 · QA1 비준에 포함): G0 = R 만 (지금 그대로) + RT 는 GD17 lint 로 R 의 head · r_params 에 묶음 (고치기 전 판 QA3) · 리뷰 자리 = 내부 반박 리뷰 (독립 조수 · "Codex 아님" · 1저자 11-10 *"이건 우리 자체 리뷰로 다시 해"*).

| 질문 | 내용 · 권고 | 1저자 11-12 | 이번 고침 (2 회차) | 지금 |
|---|---|---|---|---|
| QA1 | 이 개정 비준 (RT1 · RT2 (UN 뒤) · G2cp · rt.bin 결합 · 옛 G2c = [연속] 보고 · RT 문법 fixture 순서 · 판 표지) · 권고 예 | 권고대로 | 내용 고침 = rt.bin 결합 자리 (RT2 로그 파일 · 전체 경로) · RT 문법 fixture 새 파일 · 검사 20 · GD18 · 활성 규칙 26 · 관문 `rt_grammar_prereq` — 권고 그대로 | 정함 (비준 = 이 판으로) |
| QA2 | C12 를 이 개정에 · 권고 아니오 (개정 5 · G_ 제출 전 비준) | 권고대로 | 그대로 | 정함 |
| QA4 | 벽 이력을 RT 덤프에 · 권고 넣되 보고만 | 권고대로 | 그대로 | 정함 |
| QA5 | 발사 GO 자리 | **1저자 결정** = Codex GO 유지 (발사 기준을 Codex GO 아래로 낮추지 않음 · 1 회차 (나) "예외 하나 더" = 지움) · Codex 쓰는 법 = 지금 남은 한 번 = 이 두 초안 설계 확인 (비준 뒤 · 구현 전) · 리셋 (약 11-15) 뒤 = Rint ② 봉인 전 묶음 + P1 실제 RJ 발사 GO (B 결과 붙여) (*"3일 뒤에 리셋돼서 더 필요하면 그 이후에 하면돼"* · *"권고대로 해주고 지금 뭐뭐 남았는지"* · 세션 기록) | 15-9 ② · ⑧ 에 반영 · 1 회차 (나) 문안 = 지움 | 정함 (질문 아님) |
| QA6 | 7:3 다음 RJ 의 시도 셈 · 권고 = 323957 = 시도 1 · 다음 = 새 폴더 시도 2 (15-9 ⑨) · RT 문법 fixture 런 = 셈 밖 · RT SYNTAX_FAIL = 그 시도의 기술 실패 (다시 = 새 폴더 · 1저자) · VALUE_MISMATCH (G2cp · 15-5b) = 멈춤 → 1저자 · 한도 = 1저자 | 권고대로 | 한 줄 보탬 (15-5b 위반 = 그 시도 RESTORED 안 됨 · 다시 읽어 뒤집지 않음 · 지표 · 문턱 바꿔 다시 = 새 등록) — 권고 그대로 | 정함 |
| **QA7** | 15-5b 를 거부 쪽 새 규칙으로 | 권고대로 (1 회차 내용 = 몫 ≤ 0.03 ∧ r 중앙 ≤ 1e-2 · "여유 ×20 이상") | **내용 바뀜** — 지표 W (\|Ft\| 가중 reset 몫) ≤ 0.05 ∧ 쌍 집합 같음 (ⓡ · ⓣ 각각) · 몫 · r 중앙 = 보고만 · 결과를 본 뒤 정한 문턱 (머리) · 1 회차 "여유 ×20 이상" = 거둠 (정직 몫 여유가 샌드박스에서 ×1.9) | **다시 물음** — 권고: 예 (생산 경로의 값 수준 이력 증거가 이것뿐 · 정직 여유 샌드박스 B ×16 · C ×128 (7:3 W 계산 안 함) · 소실 쪽 전부 ×20 · 주기 표지 쌍 ×2.1 · NP 6 랭크 하나 ×2.8–4.3 · 한계 = \|Ft\| 몫 0.05 밑 소실 (15-8) · 10:0 RJ 정직 위반 = 낮음 [추정 · 15-12]) |

## 15-12. [미확인] · [추정]

- [추정] 생산 머리 (판 mesh 벽) + 30 열 키워드 조합의 문법 — RT 문법 fixture (15-4b · 입자 20) 가 RJ 전에 확인 · 생산 침대 (7:3 원자 160417 · NP 6) 에서의 조합은 첫 RJ 가 처음.
- [추정] NP 6 · 상자 0.05 의 [왕복] (초안 B = NP 2 · 4 · 상자 0.012) · 7:3 R 덤프 재현 (결정성) · 벽 왕복 · RT2 화면 reset 로그 다섯 (rt.bin 이 같은 fix 상태) · 15-5b 소실 모형 (감쇠 몫 무시) · 크기 어림.
- [추정] 15-5b 정직 W — 생산 침대 (다섯 RJ · 10:0 RJ · RJ2) 와 7:3 은 안 쟀다 · 근거 = 샌드박스 B 0.0031 (×16) · 정직 reset 쌍 = 하중 작은 쌍 · 샌드박스가 7:3 보다 많이 움직임 (r 중앙 ×8).  **10:0 RJ (S0 3,600,000 · 판 압력 조건 1.03 % 미이완)** 에서 정직하게 위반이면 EXT 관문이 닫혀 10:0 전체 멈춤 → 1저자 (문턱을 결과 뒤 옮기지 않음 · 다시 = 새 등록).
- [미확인] RT 단계 시간 (ibb · RJ 323957 전체 = 36 분 · manifest 20 · 28 행 · RT 둘 = 읽기 + setup 두 번 + 덤프 ≈ 370 MB × 2) · restart `.bin` 3 개 바이트 차이 까닭 (메모 §8 225 행) · LIGGGHTS 3d5c00f 의 명령 메아리 소스 줄 (로그 파일만 = 받은 로그로 본 것) · 7:3 의 W · 무너짐 몫.
- 11-12 결과 = 커밋 L `bfd9b3bbd` 반입 (가린 사본 · 메모 §8) · push 전 → 리포 경로 = push 뒤 경로 (머리 표지) · 덤프 · 로그 원본 = 리포 밖.

## 15-13. Codex 설계 확인 요청서용 — 이번에 닫는 것 / 닫지 않는 것 (A · 1저자 11-12 "지금 남은 한 번")

| 이번에 닫는 것 (설계 · 결과 0 건 · 구현 전) | 닫지 않는 것 |
|---|---|
| RT1 · RT2 단계 자리 (UN 뒤 · UK 앞) · 실패 · 건너뜀 처리 (15-2) · RT 덱 꼴 · GD17 · GD18 · 148 행 튜플 (15-4) | 구현 (코드 · 시험은 이 확인 뒤) · 실제 RJ 발사 GO (리셋 뒤 · B 결과 붙여 · 15-9 ⑧) |
| G2cp 판정 규칙 · 네 상태 · 복원 사상 · 판 표지 (15-5) | 15-5b 문턱의 생산 침대 정직 여유 (본 것 = 샌드박스 · 7:3 몫 · r 중앙 / 다섯 침대 · 10:0 RJ · RJ2 = [추정]) |
| rt.bin 결합 = 잡 기록 sha256 두 줄 + RT2 로그 파일 치환 `read_restart` 전체 경로 = `job_dir/RT1/rt.bin` (15-5) | 원 런 ↔ 재개 연속성 · MPI 지연 크기 · NP 6 [왕복] (A-2 · A-3 = 예측 · 초안 B) |
| 15-5b 지표 · 문턱 (W ≤ 0.05 · ⓡ · ⓣ · 쌍 집합 · 결과를 본 뒤 정함 = 머리 표지) · 옛 G2c = [연속] 보고 | C12 중력 팔 (개정 5) · 벽 이력 판정 (QA4 = 보고만) · 허용폭 · RJ 323957 소급 · 언로딩 물리 · 10:0 출발 체크포인트 (C18 · §12-11) |
| RT 문법 fixture 설계 (새 파일 · 표 · 검사 20 · 봉인 값 · 사전 점검 · 지금 문법 fixture 봉인 무변경) (15-4b) | RT 문법 fixture 결과 (ibb 한 번 = 15-9 ⑥) |
| 바뀌는 코드 · 시험 · 봉인 · 활성 규칙 목록 (15-2 · 거부 쪽 사례 수 안 줄임) · 순서 (15-9) · 정한 질문 (15-11) | P1 수치 인증 · 15-5b 통과 = 원 런 이력 복구 (15-8) |
