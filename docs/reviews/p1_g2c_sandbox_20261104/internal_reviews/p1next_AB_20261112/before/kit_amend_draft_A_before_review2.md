# 언로딩 등록 개정 4 (§15) — 복원 쌍 관문 = G2c′ [왕복] (키트 적용)

> **초안 · 결과 0 건 · 1저자 비준 전 · 내부 반박 리뷰 1 회차 반영 (11-12 · Codex 아님 · `docs/reviews/p1_g2c_sandbox_20261104/internal_reviews/p1next_AB_20261112/review1_AB.md` P1 1 · P2 8 · P3 16 → 처분 `docs/reviews/p1_g2c_sandbox_20261104/internal_reviews/p1next_AB_20261112/disposition1_AB.md`) · 2 회차 전** — 2026-11-12 · 문서만 (실행 · 제출 · 키트 파일 · 리포 변경 없음).  고치기 전 판 = `kit_amend_draft_A_before_review.md` (sha256 앞 12 `ecd528e3c4c2`).
> 트랙 = [DEM 우선] Ⓐ 언로딩 P1 (Claude 세션 · 1저자 11-04 오후 Q1) · 자리 = 메모 `docs/reviews/p1_g2c_compare_definition_20261105.md` §5-3 (1저자 11-12 *"권고대로"*).
> 대상 = 등록 `docs/reviews/dem_unloading_ps45_prereg_20261009.md` (이하 REG) 의 G2c 자리 — §3-2 표 G2c 행 (229 행) · §12-1 G2c 문장 (614 행) · §13-7 C7 (798 행) · §14-10 복원 판정 · §14-11 ② · §14-12 `ULPR-04`.  비준되면 REG 끝 §15 로 붙이고 그 자리마다 "⛔ 개정 4 §15" 표지 (원문 보존 · 앞 개정과 같은 꼴).  QA5 결과에 따라 GO 문구 자리 (REG 1 행 · 962 행 · 키트 `run_unload.sh` 2 행 · `run_unload_ibb.sbatch` 8 행 · README §2 · §3 머리) 에도 표지.
> 리포 경로 표지: 11-12 결과 = 대피 세션 커밋 L `bfd9b3bbd` (가린 사본 `docs/reviews/p1_g2c_sandbox_20261104/run_ibb_40000_20261112/` · 메모 §8) — 이 컨테이너 원격 추적 ref (`ef68eb7da`) 에 없음 = push 전 → 아래 그 경로 = **push 뒤 경로**.  덤프 · 로그 원본 = 리포 밖 (받은 묶음 sha256 3caf3e05… · 그 폴더 README 3 행).

| 이번에 닫는 것 | 닫지 않는 것 |
|---|---|
| 복원 쌍 관문의 기준쪽 (원 런 덤프 → 같은 경로 재계산) · RT1 · RT2 단계 (UN 뒤 · UK 앞) · G2cp 판정 규칙 · rt.bin 결합 · 옛 G2c = [연속] 보고 + 거친 이력 소실 문턱 (15-5b · QA7) · RT 문법 fixture 를 RJ 전에 (15-4b) · 바뀌는 코드 · 시험 · 봉인 자리 | 원 런 ↔ 재개 연속성 · MPI 지연 크기 · 쓴 NP ≠ 읽는 NP (초안 B · 따로) · C12 중력 팔 (개정 5 · QA2) · 벽 이력 판정 · 허용폭 · RJ 323957 소급 · 언로딩 물리 · 발사 승인 (QA5) · 10:0 출발 체크포인트 (C18 · §12-11) |

## 15-0. 한 줄

- RJ · RJ2 의 R 흐름 (PRE · POST · G1–G3 · UN) 은 바이트 그대로 두고, **UN 바로 뒤 (UK 앞)** 에 RT1 (S0 → P → `write_restart`) · RT2 (그 파일 → P) 를 더해 쌍 접촉 관문을 RT2 ↔ RT1 (G2c′ · 판독기 키 `G2cp`) 로 판정한다.
- 옛 G2c (R POST ↔ 원 `contact_S0`) 는 같은 식으로 계산해 [연속] 보고로 내리고, 거친 이력 소실만 막는 결과 전 문턱 (15-5b · R · RT1 각각) 을 둔다 (QA7).

## 15-1. 근거

| 무엇 | 값 | 출처 · 표지 |
|---|---|---|
| 옛 G2c 가 원리상 못 서는 까닭 | ㉠ 주기 restart 쌍 이력 = 힘 계산 전 사본 (직렬 B shear = A(N−1) 3111/3111) · ㉡ 스텝 끝 덤프는 고스트 쌍을 setup 과 다르게 다시 계산 (직렬 C ↔ A = 주기 표지 334 쌍 전부) · ㉢ `force_normal` = 쌍 전체 힘 사영 | 메모 §1 표 · 노트 `docs/reviews/p1_g2c_source_check_20261104.md` §7 · `docs/reviews/p1_g2c_sandbox_20261104/run_40000/compare.json` · `diag_out.txt` |
| 같은 경로 재계산이 서는가 (직렬 · 11-12 ibb 잡 359243 · 생산 `lmp_mpi` 1 프로세스 · N 40000) | 판정 다 · 라 PASS (n_mismatch 0 · 비트 같은 쌍 3111/3111) · 원자 1220 · 판독 가능한 예측 13 모두 맞음 · 가 · 라-재현 (나) = 해당 없음 (실행 파일 md5 0c0daccc ≠ 11-04 f4ba3ec0) | `docs/reviews/p1_g2c_sandbox_20261104/run_ibb_40000_20261112/compare_g2cp.json` `judgment` · `predictions` · 메모 §8 (223–236 행) — push 뒤 경로 |
| 명령 체크포인트여도 옛 꼴은 실패 | 11-12 [연속] 키트 26 열 옛 식: B (주기 파일) FAIL n_mismatch 3107 · C (명령 파일) FAIL 331 (힘 다른 쌍 334 = 주기 표지 334) | 같은 JSON `reports.연속` |
| RJ 323957 | G2c FAIL 545583/562605 (빠짐 · 더함 0) · `VALUE_MISMATCH` · reader_rc 2 — 그대로 · 소급 PASS 없음 | `docs/reviews/codex_p1_g2c_diagnosis_20261027/restore_verdict.user-relayed.json` · `run_manifest.user-relayed.txt` 26 · 28 행 |
| 7:3 [연속] 이력 소실 지표 (11-02 사후 · 판정 자료 아님) | reset_like 685 / 562605 (0.12 %) · ΔFt/Ft 중앙 7.8e-5 (q95 4.0e-3) · 내부 고착 쌍 352663 | `docs/reviews/dem_unloading_rj_g2c_cause_20261102/RESULT_20261102.md` 8 · 12 행 · 정의 = 같은 폴더 `rj_g2c_cause_check.py` 336–341 행 |
| S0 꼴 | 다섯 침대 S0 = 주기 `restart 50000` (명령 없음) · **10:0 RJ2 의 S0′ 3,650,000 · S0″ 3,700,000 도 주기** (`docs/data/ps45_unload_20261009/decks/ps_10_0_r45/in.EXT.liggghts` 79 행 `restart 50000` → 81 행 `run 60000` · `in.EXT2.liggghts` 79 · 81 행) · 명시 `write_restart` = 끝 3,660,000 · 3,710,000 (두 덱 85 행 · EXT2 출발용) | 메모 §2 (11-05) · 키트 README 220 행 · 표 `ext_10_0` (s0p · end1 · s0pp · end2) · `ul_reader.py` 1765–1775 행 (S0′ = `restart_ext_<s0p>.bin`) · REG §12-11 692 행 ("체크포인트 3,650,000") · C18 815 행 |
| 키트 실행 꼴 | NP 6 · `processors * * 1` · `mpirun --oversubscribe --bind-to none` · 7:3 RJ 격자 3×2×1 | `docs/data/ps45_unload_20261009/run_unload_ibb.sbatch` 23 행 · `run_unload.sh` 37–39 행 · `docs/data/ps45_unload_20261009/decks/ps_7_3_r45/in.R.liggghts` 25 행 · `docs/reviews/dem_unloading_rj_g2c_cause_20261102/ibb_result_20261102.json` `rj_screen_processor_grid` (646 행) |
| 이력 열 꼴 | 머리 → `uncompute cpl` → 새 `pair/gran/local … history` → 첫 `run 0` (pair/local 은 하나만 = 10-13 job 281180 실측 · local compute 는 read_restart 뒤 첫 run 전) | `docs/data/ps45_unload_20261009/history_test/in.hist_consumer.liggghts` 68–78 행 · 키트 README §1-5 · §2 덱 언어 규칙 · REG 827 행 |

- 판정 G2cp 는 S0 꼴과 무관하게 같은 꼴이다 (11-12 다시 확인) — RT1 · RT2 가 같은 S0 (RJ2 = 주기 S0′) 를 읽고 왕복만 본다 = 직렬 다 (주기 파일 BW → F′ → BR) PASS 와 같은 길.  S0′ 꼴이 바꾸는 것 = [연속] 예측 (A-5) · 15-8 한정어뿐.
- 관찰 (판정 아님): 11-12 덤프 12 개 = 11-04 덤프 바이트 같음 (실행 파일 · 기계 다름) · 다른 3 개 = restart `.bin` 셋 (까닭 [미확인]) — 같은 JSON `predictions.가` · 메모 §8 225 행.

## 15-2. 바뀌는 것

| 자리 | 지금 | 개정 뒤 |
|---|---|---|
| RJ · RJ2 단계 (`run_unload.sh` 229–244 행) | G0 → (7:3) Ut0 → R → UN → (UK · 10:0 RJ 는 없음) → 판독 | G0 → (7:3) Ut0 → R → UN → **RT1 → RT2** → (UK) → 판독 · 앞 단계 실패 (PRE_OK 0) 면 RT 둘 다 안 돎 (기록 `stage=RT1 skipped` · `stage=RT2 skipped`) · RT1 실패면 RT2 안 돎 · RT 실패 = PRE_OK 0 (UK 안 돎 · 복원 = SYNTAX_FAIL 이라 U 없음) · UK 기술 실패는 복원 판정 밖 그대로 (`ul_reader.py` 1566–1569 행) |
| rt.bin 결합 (러너) | — (`run_deck` 은 읽은 restart 를 잡 기록 `run_manifest.txt` (201 행) 에 안 적고 잡 로그 (`say` · 187 행) 에 파일 이름만) | RT1 뒤 `rt_bin=RT1/rt.bin sha256=<…>` · RT2 앞 같은 파일 sha256 다시 `stage=RT2 ckpt=RT1/rt.bin sha256=<…>` (잡 기록 `note` 두 줄) |
| 덱 · 봉인 | 덱 64 · `SHA256SUMS` 76 줄 (KIT_FILES 12 + 덱 64) | 덱 74 (+ RT1 · RT2 × 다섯 침대) · 86 줄 (KIT_FILES 12 그대로) |
| 생성기 (`make_unload_decks.py`) | 148 행: 10:0 `ul_s0` = 3,600,000 은 kind ∈ (R · UNread · EXT) 만 · 그 밖 = `s0_candidates[0]` 3,650,000 · GD1 (810 행) 덱 64 · 593 행 글 "덱 64" · GD1–GD16 | 148 행 튜플에 RT1 · RT2 — 빼면 10:0 **RJ** (러너가 `-var ul_s0` 를 안 준다 · `run_unload.sh` 146–151 행) 의 RT1 = `UL_ABORT reason=start_step` → SYNTAX_FAIL → 10:0 EXT (관문 = RJ RESTORED · `ul_reader.py` 1247–1251 행) · RJ2 · U 막힘 · RT 덱 생성 (15-4) · GD1 · 593 행 = 74 · GD17 |
| 복원 쌍 관문 | G2c = R `g2/contact_S0` (26 열 · `%g`) ↔ 원 `in/contact_S0` (`ul_reader.py` 1590 행) | **G2cp** (화면 표기 G2c′ · JSON · 셸에서 U+2032 를 쓰지 않는다) = RT2 ↔ RT1 (30 열 · `%.17g` · 15-5) |
| 옛 G2c | 판정 입력 (`ul_reader.py` 1619 행 목록) | [연속] 보고 `checks['G2c_cont']` — 식 · 함수 그대로 · 1619 행 목록 'G2c' → 'G2cp' + (QA7 예면) `cont_guard` (15-5b) |
| 판독기 (`restore_verdict` 1555 행) | 단계 기술 R · UN · (7:3) Ut0 · reset 로그 = R 화면만 (1570–1573 행) | + RT1 · RT2 (`_stage_tech` 1348 행 · 표지 `UL_RT_DONE`) · RT1 · RT2 화면 reset 로그 (같은 함수 · `EXPECTED_RESETS` 1336–1338 행 · 경로 증거) · rt.bin 결합 · post 목록 (1604–1607 행 꼴) · G2cp · [연속] · 15-5b · 증서 판 표지 `restore_rule = "rev4_g2cp"` |
| 관문 (`_job_restored` 1214–1226 행) | 증서 status 만 | + 판 표지 요구 (없거나 다르면 = 옛 판독기 증서 · 거부 · 새 시도) |
| 비교기 (`ul_gates.py`) | `g2c_compare` (26 열 · 339 행) | 그대로 ([연속]) + `g2cp_compare` (15-5) + `cont_guard` (15-5b · 26 열 또는 30 열의 26 열 사영 ↔ 원) |
| 이력 시험 폴더 (`history_test/`) | 문법 fixture (Q5 · 검사 19) | + RT 문법 fixture (15-4b · 덱 · 판정 파일 따로 · 기존 문법 fixture · 판독기 봉인 값 GRAMMAR_READER 그대로) · `history_test/SHA256SUMS` 다시 |
| 러너 사전 점검 | 문법 fixture PASS (Q5 · `GRAMMAR_VERDICT`) | + RT 문법 PASS (`RT_GRAMMAR_VERDICT` · 같은 꼴 · RJ · RJ2 만) · `run_unload_ibb.sbatch` 13 행 주석 |
| 기존 시험 — 판독기 (`_mk_rj` 2095 행 = RT 없는 합성 RJ · 리뷰 표기 `_synth_rj` 2096 = 같은 함수) | R14 · R17 · R18 · R29 · R30 = RT 없이 RESTORED 등 단언 · R35 (3472–3530 행) = R/g2 · 원 덤프 열 결손 → UNCONFIRMED · 시점 S0 + 1 → VALUE_MISMATCH · 접선력 하나 → VALUE_MISMATCH · 열 결손 + UN 실패 → SYNTAX_FAIL · R16 중력 팔 (3784 행부터 · chk 3806–3828 행) | `_mk_rj` 가 정상 RT1 · RT2 출력도 쓴다 → R14 · R17 · R18 · R29 · R30 기대 그대로 · R35 사례를 RT 덤프 (`post/rt_pair_S0`) 자리로 옮겨 같은 기대 (G2cp) · R/g2 · 원 덤프 쪽 같은 사례 = QA7 예면 15-5b 로 같은 기대 (열 결손 = UNCONFIRMED · 시점 = VALUE_MISMATCH) · 접선력 한 쌍 = 15-5b 문턱 안이면 통과 (보고) · QA7 아니오면 [연속] 보고만 (기대 바뀜을 시험 글에 적음) · 거부 쪽 사례 수 줄지 않음 (자리 이동 = 시험 약화 아님) · R16 그대로 (C12 = 개정 5) |
| 기존 시험 — 러너 (`ul_runner_test.py`) | M4 (RJ 차례 Ut0 → R → UN → UK · 단계 rc) · M15 · M16 (G0 · Ut0 실패 = R · UN · UK 안 돎) | M4 차례 · 단계 rc 에 RT1 · RT2 · M15 · M16 안 돈 단계에 RT1 · RT2 |
| 새 시험 | — | 판독기 R41 (G2cp 네 상태 · 15-5b · 판 표지 · 쌍 0 · post 목록 · rt.bin 결합) · 러너 M26 (RT 단계 · 건너뜀 · 실패 · rt.bin 결합 기록 · 차례 UN → RT1 → RT2 → UK · 10:0 **RJ** = 덮어쓰기 없음 · 덱 기본 `ul_s0` 3,600,000 = CKPT0 / **RJ2** = `-var ul_s0 <S0′>` · CKPT0 = `restart_ext_<S0′>.bin` 두 꼴) · 생성기 GD17 (15-4 · 15-10 반례) |
| 차등 시험 | — | 새 파일 `docs/reviews/p1_g2c_sandbox_20261104/test_g2cp_kitdiff.py` — 키트 `g2cp_compare` ↔ 샌드박스 `compare_g2cp.py` §3 판정 (둘 다 읽기만 · 합성 침대 · 30 열 · t07 꼴 변이) · 샌드박스 실행기 · 대조기 · `test_g2cp.py` 무변경 (초안 B 가 고치는 파일과 겹치지 않음 · 실행기 `inputs.md5` 목록 밖 — `run_g2cp.sh` 171 행) |
| 활성 규칙 (`active_rules.json` · 규칙 표 = `seal_kit.py` 60–102 행) | 24 | 25 (`g2cp_roundtrip` — 15-5 · 15-5b) · `restore_complete` 글 (RT 단계 · G2cp · 판 표지) · `parse_complete` 글 (G2c ULPR-04 → G2cp · 15-5b · 증인 R35 옮긴 사례 · R41) |
| 봉인 (`seal_kit.py`) | K1 "덱 64" (293–294 행) · 10 행 글 | K1 · 10 행 = 74 → `--write` (SHA256SUMS 86 줄 · active_rules.json) |
| 키트 README | §0 · §2 · §3 · §4 · 135 행 "덱 64" | 이름 (RT1 · RT2 · `rt.bin` · `post/rt_*`) · 덱 표 · 단계 · 복원 판정 행 · 덱 74 · (QA5 결과) GO 문구 표지 |

## 15-3. 그대로

- R 덱 바이트 (PRE · POST · G1 · G2 · 26 열 쌍 덤프 · mesh · G3 · R_END · UN 소거) · UNread · UK · Ut0.
- G0 = 원 마지막 조각 덱 ↔ R 덱 (지금 그대로 · RT 는 GD17 lint 로 R 의 head · r_params 에 묶음 — 초안이 정함 · QA1 에 포함).
- 허용폭 식 1e-5 × max(\|D1\|, 그 열 \|D1\| 중앙값) · 이력 4 열도 같은 식 (메모 §3 · Q2) · `%.17g` 에서 좁히지 않음.
- NP 6 · LMP sha256 · S0 · 판정 범주 넷 · 다른 복원 입력 (reset 로그 다섯 · PRE = POST · UN 소거 · 이력 시험 H0–H5 + SYN + 총힘 시점 · 문법 fixture 사전 점검).
- REG §14 머리의 "바꾸지 않는 것" 전부 · 언로딩 팔 · 순서 §13-6 · RJ 323957 기록.

## 15-4. RT 덱 꼴 (생성기가 만든다 · 손으로 고치지 않는다 · 숫자 = 표에서만)

```
# (머리 주석 — 생성기가 종류를 적음 · RT1 ↔ RT2 는 이 주석만 다름)
# >>> block head      ← 같은 침대 R 의 head 블록과 바이트 같음 (r8 머리 글자 · compute cpl … 26 열 정의 포함)
# >>> block r_params  ← 같은 침대 R 의 r_params 블록과 바이트 같음 (ul_bed · ul_s0 (index · 10:0 = 3,600,000 = 148 행 튜플) · ul_atoms0 · ul_big)
# >>> block rt        ← 같은 경로 P (메모 §2) · 이력 열 = 이력 시험 소비자 꼴
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
(QA4 예면 — 원자 덤프 끝에 f_history_zwall_bot[1–4] · compute ul_wh … wall/gran/local id history force_normal + 판 local 덤프 = R 꼴 · 보고만)
run 0
undump ul_rp
undump ul_ra
write_restart ${out}/rt.bin          ← RT1 만 (RT2 = 이 한 줄 없음 · 나머지 바이트 같음 = 샌드박스 BW ↔ BR 꼴)
print "UL_RT_DONE bed=${ul_bed} step=${ul_step}"
```

- 키워드 차례 = 샌드박스 R · fresh 덱과 같음 → 30 열 차례 같음 (pos 1–6 · id 7–9 · force 10–12 · force_normal 13–15 · force_tangential 16–18 · torque 19–21 · history 22–25 · contactArea 26 · delta 27 · contactPoint 28–30).
- **GD17 lint** (생성된 덱에서): head · r_params 블록 바이트 = 같은 침대 R · 주석 · 빈 줄 빼고 RT1 − RT2 = `write_restart ${out}/rt.bin` 한 줄 · `uncompute cpl` < `compute ul_ph` < 덤프 < `run 0` < `write_restart` · ⑮ 셋 (함께 사는 pair/gran/local ≤ 1 · wall/gran/local ≤ 1 · 내린 compute 를 쓰는 덤프 없음 — 키트 README 132 · 392 행) · 블록 rt 밖 새 명령 0 · 새 ID = `ul_` 접두 · 반례 = 148 행 튜플에서 RT 빼기 (10:0 r_params ≠ R → 실패).
- 러너: RT1 = `run_deck "$JD/RT1" RT1 "$CKPT0" - 0` → rt.bin sha256 기록 → RT2 앞 다시 → RT2 = `run_deck "$JD/RT2" RT2 "$JD/RT1/rt.bin" - 0` — 같은 NP 6 · LMP · mpirun 줄 · `EXTRA_VARS` (RJ2 = `-var ul_s0 <S0′>` 그대로 · 10:0 RJ = 없음) · `Loop time … on 6 procs` 검사 (`run_deck` 그대로 · 191–199 행).
- 덤프 = `post/` (경량 묶음에서 빠진다 · `run_unload.sh` 215 행) · `rt.bin` = `*.bin` 제외.  크기 어림 (7:3): 쌍 562605 × 30 열 ≈ 350–370 MB × 2 (11-12 625 B/쌍 산술) · 원자 ≈ 40 MB × 2 · rt.bin ≈ 80 MB [추정].

## 15-4b. RT 문법 fixture (RJ 전 · 결과 0 건)

- 까닭: RT 문법의 **조합** (판 mesh 머리 + `uncompute cpl` → 30 열 `pair/gran/local … history` → `%.17g` 덤프 → `write_restart` → 새 프로세스 `read_restart rt.bin`) 이 어느 시험에서도 함께 돈 적이 없다 — 요소는 흩어져 지났다 (이력 소비자 = 판 mesh + `uncompute cpl` + 7 열 `id history` · `in.hist_consumer.liggghts` 68–78 행 · job 283122 PASS / 문법 fixture = `write_restart` · 새 프로세스 `read_restart` · `%.17g` · `in.hist_grammar.liggghts` 27 · 95 · 139 행 · `uncompute` 없음 / 샌드박스 = 30 열 · 판 mesh 없음) · 키트 selftest 는 LIGGGHTS 를 안 돌린다 · REG §14-9 (909 행) = 문법 fixture "본 R 전 PASS (생산 침대 쓰기 전)".
- fixture: 이력 시험 생산자 restart (알려진 이력 · 입자 20 · 판 mesh) → RT1 꼴 덱 (이력 소비자 머리 + 15-4 블록 rt 그대로) → `rt.bin` → 새 프로세스 RT2 꼴 덱.
- 판정 (결과 전): 두 rc 0 · `UL_RT_DONE` · 30 열 전부 읽힘 · 쌍 > 0 · G2cp PASS (키트 `g2cp_compare`) · RT1 shear = 생산자 이력 (이력 시험 판독 규칙 그대로 · fixture 수준의 값 증거) · 판정 파일 `rt_grammar_verdict.json` (기존 `grammar_verdict.json` 과 따로).
- 실행: ibb 한 번 (1저자 GO · 수 분 · 10-15 '문법 실행 2' 꼴 · 지금 문법 fixture 와 같은 지위 = Codex GO 와 무관 · REG 909 행) · PASS = RJ · RJ2 러너 사전 점검 조건 (15-2).
- 실패 = 덱 · 판독 고침 (시험 먼저) → 다시 · RJ 시도 셈 밖 (QA6).

## 15-5. 판정 규칙 (결과 전 · 키트 판독기)

| G2cp | 조건 | 복원 판정 |
|---|---|---|
| PASS | RT1 · RT2 기술 성공 (러너 단계 기록 PASS · rc 0 · ERROR · UL_ABORT 없음 · 배너 · `on 6 procs` · `UL_RT_DONE`) ∧ rt.bin 결합 (러너 기록 sha256 RT1 끝 = RT2 시작 · RT2 화면의 치환된 `read_restart` 줄 경로 꼬리 = `RT1/rt.bin` — LIGGGHTS 가 치환 경로를 찍는다: 받은 묶음 BR `log.txt` 12 행) ∧ post 목록 = `[rt_pair_<S0>.dump]` · `[rt_atom_<S0>.dump]` 하나씩 (두 단계 각각) ∧ 두 쌍 덤프 전부 읽힘 (머리 · 열 이름 = 정확히 `c_ul_ph[1]` … `[30]` 차례대로 · 행 수 · 유한 · ID 정확한 양의 정수) ∧ 쌍 수 > 0 ∧ TIMESTEP 둘 다 = S0 (RJ2 = S0′) ∧ 쌍 집합 같음 ∧ 다른 값 중복 키 0 ∧ 공통 쌍 · 열마다 \|D2 − D1\| ≤ 1e-5 × max(\|D1\|, 그 열 \|D1\| 중앙값) | 다른 관문 (15-5b · QA7 예면 포함) 모두 PASS 면 RESTORED |
| FAIL | 값 · 집합 · 다른 값 중복 · TIMESTEP 위반 · 덤프 구조 · 읽기 문제 (필수 열 결손을 뺀 것 — 비유한 · ID 꼴 · 머리 · 행 수 · 열 수 · 열 이름 더함 (31 열) · 중복 이름 · 차례) — ULPR-04 범위 그대로 (REG 961 행 · `ul_gates.py` 343–348 행 동작) | VALUE_MISMATCH |
| NOT_COMPUTED | 쌍 덤프 없음 · 필수 열 (`c_ul_ph[1]`–`[30]`) 하나라도 없음 (ULPR-04 꼴) · 쌍 0 (두 쪽 0 행 = 지금 `g2c_compare` 꼴이면 PASS 가 되므로 따로 막음 · `ul_gates.py` 352–371 행) · post 목록 어긋남 · rt.bin 결합 기록 없음 | UNCONFIRMED |
| (계산 안 함) | RT1 · RT2 기술 실패 · rt.bin 결합 어긋남 (sha256 다름 · 경로 꼬리 다름 = 등록된 왕복이 아님) | SYNTAX_FAIL (REG §14-10) |

- 정규화 = 지금 G2c 와 같음: 무순서 키 (작은 id, 큰 id) · 방향 바뀐 행 = 위치 맞바꿈 · 힘 9 · shear 3 부호 반전 · deltaMax 그대로 · 위치 · 접점 = 상자 (0.05 × 0.05) 로 감음 · torque · 주기 표지 = 판정 밖 · 집합 차를 "MPI 끝자리" 로 면제하지 않음 (REG §12-1).
- D1 = RT1 (기준쪽) · D2 = RT2.  [왕복] 의 주장은 D2 = D1 (D1 = 파일 원값이 아님 — setup 이 deltaMax 를 올린다 · 메모 §0-1 ①).
- 복원 판정 사상 = 지금 그대로 (`ul_gates.restoration_verdict` 413 행): G2cp 는 1619 행 목록의 G2c 자리 (FAIL → VALUE_MISMATCH · NOT_COMPUTED → UNCONFIRMED) · 단계 기술 = R · UN · (7:3) Ut0 · RT1 · RT2 · reset 로그 = R · RT1 · RT2 셋 다 (결손 = VALUE_MISMATCH · 지금 R 규칙 그대로) · G1 · G2 · mesh md5 · G3 그대로 · 증서에 `restore_rule = "rev4_g2cp"` (15-2 관문).
- 함께 적음 (판정 아님): 비트 같은 쌍 수 · 원자 12 열 비트 같음 · 두 덤프 sha256 같음 · 열별 최대 상대차 · 판별력 (D1 접선력 0 아닌 몫 · \|shear\| > 0 몫) · 주기 표지 쌍 수 · (QA4) 벽 열.
- [연속] = `ul_gates.g2c_compare(R/g2/contact_S0, in/contact_S0)` 그대로 → `checks['G2c_cont']` · 상태 · n_mismatch · 열별 수 — 판정 · 다음 제출 관문 · `restoration_verdict` 입력 아님 (QA7 예면 15-5b 만 입력).

## 15-5b. [연속] 결과 전 문턱 — 거친 이력 소실 막이 (QA7 · 거부 쪽 새 규칙)

- 까닭: [왕복] 은 두 쪽이 같이 잃으면 통과한다 (메모 §2 맹점).  reset 로그 = 경로 증거 (값 아님 · 지금 R 화면만 — `ul_reader.py` 1570–1573 행) · H0–H5 = 20 입자 · 명령 파일 fixture (REG 787 행 · §13-7-4) · RT 문법 fixture (15-4b) = fixture 수준 → 생산 경로에서 "이력이 값으로 읽혔다" 의 값 수준 증거는 [연속] 분포뿐.  작은 반례: RT1 이 shear 를 0 으로 읽음 → rt.bin 0 → RT2 0 → G2cp PASS · R 화면 reset 다섯 → RESTORED (이 막이 없으면).
- 대상 (침대마다 · RJ · RJ2): **ⓡ** R `g2/contact_S0` ↔ 원 `contact_S0` (= [연속] 입력 그대로) · **ⓣ** RT1 `post/rt_pair_S0` 의 26 열 사영 (30 열에서 history 22–25 를 뺀 차례 = c_cpl 1–26) ↔ 원 `contact_S0`.
- 지표 (11-02 도구 정의 그대로 · `rj_g2c_cause_check.py` 336–341 행): 공통 쌍마다 방향 맞춘 접선력 (열 16–18) · r = \|Ft − Ft_원\| / \|Ft_원\| (\|Ft_원\| > 0 인 쌍) · reset_like = r > 0.5 인 쌍 수.
- **문턱 (결과 전 · 2026-11-12 이 초안 · ⓡ · ⓣ 각각)**: reset_like ÷ 공통 쌍 ≤ **0.03** ∧ r 중앙값 ≤ **1e-2** ∧ 쌍 집합 같음 (빠짐 · 더함 0).
- 근거: 7:3 사후 (11-02 · 판정 자료 아님) 0.0012 · 7.8e-5 · 빠짐 · 더함 0 (15-1) ↔ 소실 모형 (shear 0 → 고착 쌍 r ≈ 1 [추정 · 감쇠 몫 무시] · 7:3 내부 고착 쌍 352663 / 562605 = 0.63 → reset_like ≈ 0.6 · r 중앙 ≈ 1) → 두 쪽의 기하 중앙 (0.027 · 8.8e-3) 을 둥근 값으로 · 여유 = 측정 쪽 ×25 · ×128 / 소실 쪽 ×20 · ×100 [추정] · 쌍 집합 = 323957 빠짐 · 더함 0 · 샌드박스 새 쌍 · 사라진 쌍 0 (메모 §8 233 행).
- 7:3 은 이미 본 값이다 (A-4 가 같은 덤프를 예측) → 7:3 에서는 회귀 확인뿐 · 판별 = 남은 네 침대 · RJ2 · ⓣ.
- 결과: 위반 = 복원 VALUE_MISMATCH (이력 소실 의심 · U 없음 · 멈춤 → 1저자) · 계산 못 함 (파일 없음 · 필수 열 결손 · 공통 쌍 0) = UNCONFIRMED · 덤프 구조 · 시점 문제 = FAIL (15-5 와 같은 분류).
- 주장 안 함: 원 런 H(S) 복구 · 한 step 늦은 이력 같은 작은 차를 가름 (문턱이 일부러 넓다) · 다른 침대의 r 분포가 7:3 과 같음.

## 15-6. 결과 전 예측 (ibb RJ · RJ2 · NP 6)

| # | 대상 | 예측 = 맞음 기준 | 근거 · 표지 | 틀리면 |
|---|---|---|---|---|
| A-1 | RT1 · RT2 기술 | rc 0 · `on 6 procs` · step = S0 (RJ2 = S0′) · 원자 = 표 `ul_atoms0` · 화면 reset 로그 다섯 · rt.bin 결합 같음 · 쌍 수 = R POST 쌍 수 | R 과 같은 머리 · 같은 파일 · rt.bin 이 같은 fix 상태를 담음 [추정] · RT 문법 fixture PASS (15-4b) | SYNTAX_FAIL · 그 침대 멈춤 (REG 그대로) |
| A-2 | G2cp 판정 | PASS · n_mismatch 0 | 직렬 다 · 라 PASS (11-12) + 초안 B §4 결론 ① (두 NP 모두) · NP 6 · 상자 0.05 로 옮김 = [추정] | VALUE_MISMATCH = 그 침대 U 없음 · 멈춤 → 1저자 · 직렬 · 초안 B 와 다른 까닭부터 |
| A-3 | 비트 · 바이트 | 비트 같은 쌍 = 전부 · 원자 12 열 비트 같음 · 두 쌍 덤프 sha256 같음 | [추정] — 직렬 다-값 · 다-바이트 · 라-값 · 라-바이트 맞음 (11-12) + 초안 B M-다/라-바이트 (NP 2 · 4 · 결과 전) · NP 6 은 직접 근거 없음 | 비트 · 바이트 예측만 거둠 (판정 PASS 면 판정 그대로) |
| A-4 | [연속] · 주기 S0 다섯 (RJ) | FAIL (n_mismatch > 0) · 7:3 = n_mismatch 545583 · R 쌍 덤프 sha256 `193e6e6ca2e6833d3204fd26615b61b5de32f6e65d931fcdbd560c215365951f` (323957 과 같음 · `docs/reviews/dem_unloading_rj_g2c_cause_20261102/ibb_result_20261102.json` 21 행) · 15-5b ⓡ = reset_like 685 · r 중앙 7.8e-5 (같은 덤프 · 같은 정의면 산술) | ㉠ + ㉡ · 7:3 재현 = 같은 LMP · R 덱 · NP · 격자 · S0 → 같은 R 덤프 [추정 · 결정성] | 보고만 · 7:3 수 · sha256 다르면 결정성 서술만 거둠 |
| A-5 | [연속] · 10:0 RJ2 (S0′ = **주기** 파일 · 쓴 NP 6 = 읽는 NP 6) | FAIL (n_mismatch > 0) · 불일치는 넓게 (A-4 꼴 · 크기 · 자리는 미리 안 정함) | ㉠ + ㉡ — 주기 파일 (15-1 S0 꼴) · 직렬 같은 꼴 = B [연속] FAIL 3107/3111 (11-12 `reports.연속`) · MPI 크기 = 초안 B | 보고만 |
| A-6 | 나머지 관문 | REG 기대 그대로 | R 덱 · 판독 안 바꿈 | REG 규칙 그대로 |
| A-7 | 벽 (QA4 예면 · 보고) | RT2 = RT1 (바닥 4 열 · 판 local · 비트) | 첫 setup 뒤 상태를 rt.bin 이 담음 [추정 · 샌드박스 밖 · 메모 §0-1 ③] | 벽 왕복 서술만 거둠 |
| A-8 | 15-5b (QA7 예면) | ⓡ · ⓣ 모두 문턱 안 (다섯 침대 · RJ2) · ⓣ 지표 ≈ ⓡ (같은 경로 · 둘 다 setup) | 7:3 ⓡ 사후 값 · 같은 머리 · 같은 S0 [추정 · 다른 침대 미확인] | VALUE_MISMATCH (규칙) → 멈춤 → 1저자 (이력 소실 ↔ 늦은 이력의 큰 차 가름부터) |

- [이력] 앵커 = 해당 없음 (원 덤프 · EXT 덤프에 이력 열 없음).  "이력이 실제로 읽혔다" 는 [왕복] 밖 — 15-5b (값 수준 · 거친 소실만) · H0–H5 · RT 문법 fixture (fixture 수준) · reset 로그 (경로).

## 15-7. C12 중력 팔 — 이번 밖 (QA2 · 개정 5 예고)

- 지금: `_g_restore` (`ul_reader.py` 1096–1118 행) 가 G_ 팔 setup 덤프 ↔ 출처 팔 R_M **창 끝 (in-run)** 덤프로 G2c → ㉡ 때문에 예측된 실패 (R_M = `write_restart` 명령 파일 · `make_unload_decks.py` 410 행 — 명령이어도 직렬 [연속] C 가 kit26 FAIL 331).
- 이번 밖으로 두는 까닭: GT1 · GT2 덱 꼴이 15-4 수준으로 안 정해졌다 — G_ 덱 머리 뒤 `arm_dt` 블록 (G_UVb · G_UT3 = 5e-07) · `ul_params` 의 `include ${ul_base}` · `g_start` 의 `include ${ul_state}` · 관측 블록의 `compute ul_wh … wall/gran/local` 을 GT 에 어떻게 둘지 · 덱 수 (출처 팔 넷 × 침대 다섯 또는 침대마다 한 쌍) · GT 실패 때 G_ 덱 처리.  G_ 팔은 U 뒤라 RJ 와 무관.
- 남기는 것: **G_ 팔 제출 전에** 개정 5 (GT1 · GT2 · 판정 = GT2 ↔ GT1 · 옛 C12 G2c = [연속] 보고 · 15-5 · 15-5b 와 같은 규칙) 비준 필요 — 지금 규칙이면 예측된 실패 (11-02 보고 §6 Q3) · [이력] 후보 (출처 팔 R_M 창 끝 쌍 덤프에 이력 열) = U 덱 변경 · 그때.

## 15-8. 주장하지 않는 것

- 원 런 스텝 끝 덤프 ↔ 재개 setup 의 연속성 · `write_restart` 비트 동일성 (비트 · 바이트 = 예측일 뿐).
- G2cp PASS = 이력이 실제로 읽혔다 (맹점 — 두 쪽이 같이 잃으면 통과 · H0–H5 = 20 입자 · 명령 파일 fixture (REG §13-7-4) · reset 로그 = 경로 증거 (값 아님) · RT 문법 fixture = fixture 수준 · 생산 경로의 값 수준 막이 = 15-5b (QA7 · 거친 소실만 · 한 step 늦은 이력 같은 작은 차는 못 가름)).
- 주기 S0 파일이 원 런 H(S) 를 담는다 — **S 상태 = 파일 상태** (다섯 S0 · 10:0 S0′ · S0″ 모두 주기 · x · v · ω · 벽 이력 = S 끝 · 쌍 shear = S 힘 계산 전 사본 · 직렬 = H(S−1) · MPI = 초안 B) · 10:0 결과를 "동기한 이력에서 출발" 로 적지 않는다 (동기 출발 = S0′ 를 끝 3,660,000 명령 파일로 바꾸는 C18 · §12-11 개정 · 이번 밖).
- RJ 323957 소급 PASS · "등록 기대 오류로 설명됨" (11-02 보고 §4 — 표지로만).
- 허용폭 변경 · P1 수치 인증 · 언로딩 물리 결과 · 벽 이력 판정 (QA4 = 보고만) · `force_normal` 차이 = 법선 모델 힘 차이 · 15-5b 통과 = 원 런 이력 복구.
- NP 2 · 4 (초안 B) 결과가 NP 6 · 생산 침대에서 같다는 것 (추정으로만 씀).
- 넘김 (원장 후보 · 지우지 않음): REG §3-2 237 행 — ㉠ 확인 뒤, 주기 restart 로 이은 ps45 압축 조각 (7:3 r3 · r6–r8) 은 조각 경계마다 늦은 이력으로 이어졌을 것 [추정 · 직렬 = 1 step · MPI · NP 바뀜 = 초안 B · 크기 미측정] · 이 개정은 다루지 않음 · 등재 = 다음 원장 커밋.

## 15-9. 순서

1. 이 판 → 내부 반박 리뷰 2 회차 (고친 곳 · Codex 아님) → 1저자 비준 (QA1 · QA2 · QA4 · QA5 · QA6 · QA7).
2. 키트 수정 (시험 먼저 — 고치기 전 실패 → 고친 뒤 통과 · 변이 시험): 생성기 (148 행 · RT 덱 · GD1 · GD17) · 러너 (RT 단계 · rt.bin 결합 · RT 문법 사전 점검 · M4 · M15 · M16 · M26) · 판독기 (G2cp · [연속] · 15-5b · 판 표지 · R14–R35 옮김 · R41) · `ul_gates` (`g2cp_compare` · `cont_guard`) · 활성 규칙 · `seal_kit.py` K1 · README · 봉인 다시 → 게이트 → 커밋 · push.
3. 차등 시험 (`test_g2cp_kitdiff.py`) · RT 문법 fixture 덱 · 판독 (`history_test/` · 시험 먼저).
4. 내부 반박 리뷰 (코드 · CLAUDE.md 사전 공격 ①–③ · Codex 아님).
5. RT 문법 fixture ibb 한 번 (1저자 GO · 15-4b) → PASS.
6. 초안 B §4 결론 ① (정의 그대로 — 두 NP 모두 판정 다 · 라 PASS ∧ M-다-값 · M-라-값 맞음 · 부분 결론 없음).  판정 PASS ∧ 값 틀림 = 선행 조건 아님 → 멈춤 → 1저자 (결과 전 · 11-12).
7. 발사 GO (QA5) → ibb RJ (새 폴더 · 새 시도 · 침대 차례 = REG §13-5 ② 그대로 · 7:3 = QA6).

- 단계마다 1저자 GO · 자동 다음 단계 없음 · B 결론 ① 이 안 서면 (한 NP 라도 기술 실패 · NOT_COMPUTED · FAIL · 값 틀림) RJ 보류 → B 다시 = 새 빈 폴더 · 1저자 승인.

## 15-10. 보장 · 작은 반례 (내부 반박 리뷰 2 회차가 깨 볼 것)

| 보장 | 깨 볼 작은 반례 |
|---|---|
| RT1 · RT2 는 읽는 파일만 다르다 | RT1 = RT2 + 두 줄 · `write_restart` 가 `run 0` 앞 (setup 없이 F′ = F → 맹점 통과) · 러너가 두 단계에 다른 `-var` · NP · 10:0 RT 의 r_params ≠ R (148 행 튜플 빠짐 → RJ RT1 = UL_ABORT) · 머리 주석만 다른 RT1 · RT2 를 GD17 이 실패로 봄 |
| RT2 가 RT1 의 rt.bin 을 읽었다 | RT2 ckpt = 다른 폴더의 같은 이름 파일 · RT1 뒤 rt.bin 바뀜 · 결합 기록 없음 · 화면 `read_restart` 줄 꼬리 다름 |
| G2cp PASS = 같은 경로 재현 | 두 쪽 쌍 0 (→ NOT_COMPUTED 인가) · post 에 rt_pair 둘 (다른 step) · 옛 판독기 증서 (판 표지 없음) 로 관문 통과 |
| 이력 소실 막이 (15-5b · QA7 예) | RT1 만 shear 0 · R · RT1 둘 다 shear 0 · 늦은 이력의 큰 차 (r 중앙 1e-2 바로 위 · 아래) · 원 덤프 열 결손 · 공통 쌍 0 · 7:3 사후 값 그대로 = 통과 |
| 옛 G2c 는 판정 밖 | 1619 행 목록에 'G2c' 가 남음 · 다음 제출 관문이 `G2c_cont` 를 읽음 · [연속] 열 결손이 (QA7 아니오인데) UNCONFIRMED 로 샘 |
| 필수 열 결손 = NOT_COMPUTED · 구조 = FAIL | 열 이름 하나 중복 · `c_ul_ph[30]` 없음 · 31 열 · 26 열 덤프를 RT 자리에 둠 · 비유한 값 (FAIL 인가) |
| 30 열 판정 = 샌드박스 §3 판정 | 같은 합성 침대에서 상태 · n_mismatch 다름 (차등) · shear 부호 반전 빼기 · deltaMax 부호 반전 넣기 변이 |
| TIMESTEP = S0 | RT2 가 S0 + 1 · RT1 덤프가 `run 0` 전 `write_dump` |
| RT 차례 (UN 뒤 · UK 앞) | UK 기술 실패가 복원 판정을 바꿈 · RT 실패인데 UK 가 돎 |
| 거부 쪽 사례 수 줄지 않음 (R35 자리 이동) | 옮긴 사례 하나를 빼도 시험이 초록 |

## 15-11. 1저자가 정할 것

- 초안이 정한 것 (질문 아님 · QA1 비준에 포함): G0 = R 만 (지금 그대로) + RT 는 GD17 lint 로 R 의 head · r_params 에 묶음 (고치기 전 판 QA3) · 리뷰 자리 = 내부 반박 리뷰 (독립 조수 · "Codex 아님" · 1저자 11-10 — G2c′ *"이건 우리 자체 리뷰로 다시 해"* · 운영 결정) (고치기 전 판 QA5 앞 반쪽).
- [Ⓐ 언로딩] **QA1** — 이 개정 비준 (RT1 · RT2 (UN 뒤) · G2cp · rt.bin 결합 · 옛 G2c = [연속] 보고 · RT 문법 fixture 순서 · 판 표지).  권고: 예 — 키트 수정 (시험 먼저) 은 비준 뒤 바로 · 발사는 15-9 ⑦.
- **QA2** — C12 (중력 팔) 를 이 개정에.  권고: 아니오 — 개정 5 로 따로 (G_ 팔은 U 뒤 · RJ 와 무관 · GT 덱 꼴 미정 (15-7) · G_ 제출 전 비준).
- **QA4** — 벽 이력 (바닥 4 열 · 판 local) 을 RT 덤프에.  권고: 넣되 보고만 (판정 밖 · 메모 Q12 "§5-3 때 따로" · 샌드박스가 안 본 길 · ⑮ lint).
- **QA5** — 발사 GO 자리 (RJ · 그 뒤 EXT · RJ2).  지금 등록 = Codex GO 뒤 (REG 1 행 · 962 행 *"자체시험이나 내부 사전 리뷰는 외부 반박 세션 GO를 대신하지 않는다"* · 키트 `run_unload.sh` 2 행 · `run_unload_ibb.sbatch` 8 행 · README §2 · §3 머리) ↔ 1저자 11-10 운영 결정 (내부 리뷰가 GO 를 대신하는 것 = 믹서 E0 pilot 한 팔뿐 · Codex 남은 한 번 = Rint ② 봉인 전 묶음).  고를 것: (가) Codex 토큰을 기다린다 · (나) 예외 하나 더 (내부 반박 리뷰 + 1저자 GO · 범위와 "Codex 아님" 을 §15 에 · 위 자리 표지).  권고: (가) — 발사 기준을 Codex GO 아래로 낮추는 안을 내지 않는다 (1저자 10-20 · CLAUDE.md 사전 공격 리뷰 블록) · 기다리는 동안 15-9 ①–⑥ 은 막히지 않는다 · (나) 를 고르면 범위를 RJ (복원 시험 · 물리 값 없음) 로 좁히기를 권함.
- **QA6** — 7:3 다음 RJ 의 시도 셈.  권고: 323957 = 시도 1 (VALUE_MISMATCH 그대로) · 다음 = 새 폴더 시도 2 (15-9 ⑦ 뒤) · RT 문법 fixture 런 = 셈 밖 · RJ 의 RT 단계 SYNTAX_FAIL = 그 시도의 기술 실패 (다시 = 새 폴더 · 1저자 승인) · VALUE_MISMATCH (G2cp · 15-5b) = 멈춤 → 1저자 · 한도 = 1저자.
- **QA7** — 15-5b (ⓡ · ⓣ · reset_like 몫 ≤ 0.03 · r 중앙 ≤ 1e-2 · 쌍 집합 같음 · 위반 = VALUE_MISMATCH · 계산 못 함 = UNCONFIRMED) 를 거부 쪽 새 규칙으로.  권고: 예 — 생산 경로의 값 수준 이력 증거가 이것뿐 (reset 로그 = 경로 · H0–H5 · RT 문법 = fixture) · 여유 ×20 이상 [추정] · 7:3 은 회귀 확인뿐.

## 15-12. [미확인] · [추정]

- [추정] 생산 머리 (판 mesh 벽) + 30 열 키워드 조합의 문법 — RT 문법 fixture (15-4b · 입자 20) 가 RJ 전에 확인 · 생산 침대 (7:3 원자 160417 · NP 6) 에서의 조합은 첫 RJ 가 처음.
- [추정] NP 6 · 상자 0.05 의 [왕복] (초안 B = NP 2 · 4 · 상자 0.012) · 7:3 R 덤프 재현 (결정성) · 벽 왕복 · RT2 화면 reset 로그 다섯 (rt.bin 이 같은 fix 상태) · 15-5b 소실 모형 (감쇠 몫 무시) · 다른 침대 지표 · 크기 어림.
- [미확인] RT 단계 시간 (ibb · RJ 323957 전체 = 36 분 · manifest 20 · 28 행 · RT 둘 = 읽기 + setup 두 번 + 덤프 ≈ 370 MB × 2) · restart `.bin` 3 개 바이트 차이 까닭 (메모 §8 225 행).
- 11-12 결과 = 커밋 L `bfd9b3bbd` 반입 (가린 사본 · 메모 §8) · push 전 → 리포 경로 = push 뒤 경로 (머리 표지) · 덤프 · 로그 원본 = 리포 밖.
