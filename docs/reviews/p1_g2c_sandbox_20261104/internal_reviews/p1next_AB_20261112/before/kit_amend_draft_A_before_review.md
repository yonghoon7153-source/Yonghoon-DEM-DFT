# 언로딩 등록 개정 4 (§15) — 복원 쌍 관문 = G2c′ [왕복] (키트 적용)

> **초안 · 결과 0 건 · 1저자 비준 전 · 내부 반박 리뷰 전** — 2026-11-12 · 문서만 (실행 · 제출 · 키트 파일 · 리포 변경 없음).
> 트랙 = [DEM 우선] Ⓐ 언로딩 P1 (Claude 세션 · 1저자 11-04 오후 Q1) · 자리 = 메모 `docs/reviews/p1_g2c_compare_definition_20261105.md` §5-3 (1저자 11-12 *"권고대로"*).
> 대상 = 등록 `docs/reviews/dem_unloading_ps45_prereg_20261009.md` (이하 REG) 의 G2c 자리 — §3-2 표 G2c 행 (229 행) · §12-1 G2c 문장 (614 행) · §13-7 C7 (798 행) · §14-10 복원 판정 · §14-11 ② · §14-12 `ULPR-04`.  비준되면 REG 끝 §15 로 붙이고 그 자리마다 "⛔ 개정 4 §15" 표지 (원문 보존 · 앞 개정과 같은 꼴).

| 이번에 닫는 것 | 닫지 않는 것 |
|---|---|
| 복원 쌍 관문의 기준쪽 (원 런 덤프 → 같은 경로 재계산) · RT1 · RT2 단계 · G2c′ 판정 규칙 · 옛 G2c = [연속] 보고 · 바뀌는 코드 자리 | 원 런 ↔ 재개 연속성 · MPI 지연 크기 · 쓴 NP ≠ 읽는 NP (초안 B · 따로) · 벽 이력 판정 · 허용폭 · RJ 323957 소급 · 언로딩 물리 · 실행 승인 |

## 15-0. 한 줄

- RJ · RJ2 의 R 흐름 (PRE · POST · G1–G3 · UN) 은 바이트 그대로 두고, 그 뒤 (UK 가 있으면 UK 뒤 · 10:0 RJ 는 UN 뒤) 에 RT1 (S0 → P → `write_restart`) · RT2 (그 파일 → P) 를 더해 쌍 접촉 관문을 RT2 ↔ RT1 (G2c′) 로 판정한다.
- 옛 G2c (R POST ↔ 원 `contact_S0`) 는 같은 식으로 계산해 [연속] 보고로만 남긴다.

## 15-1. 근거

| 무엇 | 값 | 출처 · 표지 |
|---|---|---|
| 옛 G2c 가 원리상 못 서는 까닭 | ㉠ 주기 restart 쌍 이력 = 힘 계산 전 사본 (직렬 B shear = A(N−1) 3111/3111) · ㉡ 스텝 끝 덤프는 고스트 쌍을 setup 과 다르게 다시 계산 (직렬 C ↔ A = 주기 표지 334 쌍 전부) · ㉢ `force_normal` = 쌍 전체 힘 사영 | 메모 §1 표 · 노트 `docs/reviews/p1_g2c_source_check_20261104.md` §7 · `docs/reviews/p1_g2c_sandbox_20261104/run_40000/compare.json` · `diag_out.txt` |
| 같은 경로 재계산이 서는가 (직렬 · 11-12 ibb · 생산 `lmp_mpi` 1 프로세스 · N 40000) | 판정 다 · 라 PASS (n_mismatch 0 · 비트 같은 쌍 3111/3111) · 원자 1220 · 판독 가능한 예측 13 모두 맞음 · 가 · 라-재현 (나) = 해당 없음 (실행 파일 md5 0c0daccc ≠ 11-04 f4ba3ec0) | 받은 묶음 (리포 반입 전 · 메모 §8 빈칸) `…/scratchpad/intake/g2cp_run40000_return_20261112/x/run40000/compare_g2cp.json` · 화면 `…/scratchpad/g2c_dry/compare_run40000.log` |
| 명령 체크포인트여도 옛 꼴은 실패 | 11-12 [연속] 키트 26 열 옛 식: B (주기 파일) FAIL n_mismatch 3107 · C (명령 파일) FAIL 331 (≤ 주기 표지 334) | 같은 JSON `reports.연속` |
| RJ 323957 | G2c FAIL 545583/562605 · `VALUE_MISMATCH` · reader_rc 2 — 그대로 · 소급 PASS 없음 | `docs/reviews/codex_p1_g2c_diagnosis_20261027/restore_verdict.user-relayed.json` |
| S0 꼴 | 다섯 침대 S0 = 주기 `restart 50000` (명령 없음) · 10:0 RJ2 의 S0′ = EXT 끝 명시 `write_restart` | 메모 §2 (11-05 확인) · 키트 README §2 EXT 행 |
| 키트 실행 꼴 | NP 6 · `processors * * 1` · `mpirun --oversubscribe --bind-to none` · 7:3 RJ 격자 3×2×1 | `docs/data/ps45_unload_20261009/run_unload_ibb.sbatch` 23 행 · `run_unload.sh` 37–39 행 · `docs/data/ps45_unload_20261009/decks/ps_7_3_r45/in.R.liggghts` 25 행 · `docs/reviews/dem_unloading_rj_g2c_cause_20261102/ibb_result_20261102.json` `rj_screen_processor_grid` |
| 이력 열 꼴 | 머리 → `uncompute cpl` → 새 `pair/gran/local … history` → 첫 `run 0` (pair/local 은 하나만 = 10-13 job 281180 실측 · local compute 는 read_restart 뒤 첫 run 전) | `docs/data/ps45_unload_20261009/history_test/in.hist_consumer.liggghts` 68–78 행 · 키트 README §1-5 · §2 덱 언어 규칙 |

- 관찰 (판정 아님 · 받은 묶음): 11-12 덤프 12 개 = 11-04 덤프 바이트 같음 (실행 파일 · 기계 다름) · 다른 3 개 = restart `.bin` 셋 (까닭 = 머리 글자 [추정]) — 같은 JSON `predictions.가`.

## 15-2. 바뀌는 것

| 자리 | 지금 | 개정 뒤 |
|---|---|---|
| RJ · RJ2 단계 (`run_unload.sh` 229–244 행) | G0 → (7:3) Ut0 → R → UN → (UK · 10:0 RJ 는 없음) → 판독 | 같음 + 판독 앞에 RT1 → RT2 · 앞 단계 실패 (PRE_OK 0) 면 둘 다 안 돎 (기록 `stage=RT1 skipped`) · RT1 실패면 RT2 안 돎 |
| 덱 | 64 | + RT1 · RT2 × 다섯 침대 = 74 (C12 = 15-7) |
| 복원 쌍 관문 | G2c = R `g2/contact_S0` (26 열 · `%g`) ↔ 원 `in/contact_S0` (`ul_reader.py` 1590 행) | G2c′ = RT2 ↔ RT1 (30 열 · `%.17g` · 15-5) |
| 옛 G2c | 판정 입력 (`ul_reader.py` 1619 행 목록) | [연속] 보고 `checks['G2c_cont']` — 식 · 함수 그대로 · 판정 · 다음 제출 관문 밖 |
| 판독기 (`restore_verdict`) | 단계 기술 R · UN · (7:3) Ut0 | + RT1 · RT2 (`UL_RT_DONE`) · G2c′ · [연속] 보고 · 1619 행 목록 'G2c' → 'G2c′' |
| 비교기 (`ul_gates.py`) | `g2c_compare` (26 열 · 339 행) | 그대로 ([연속]) + `g2cp_compare` (30 열 · 필수 열 `c_ul_ph[1–30]` · ID 열 7 · 8 = 정확한 양의 정수 · 이력 4 열 포함 · shear 부호 반전 · deltaMax 그대로) |
| 생성기 (`make_unload_decks.py`) | GD1–GD16 | + GD17 (15-4 꼴 lint) |
| 시험 | 판독기 R1–R40 · 러너 M1–M25 | + R41 (G2c′ 조립 네 상태 · [연속] 이 판정을 안 바꿈) · M26 (RT 단계 · 건너뜀 · 실패) · 차등 시험 (샌드박스 `test_g2cp.py` 에 키트 `g2cp_compare` ↔ 대조기 §3 판정 · 30 열 · t07 꼴) |
| 활성 규칙 (`active_rules.json`) | 24 | 25 (`g2c_roundtrip`) · `restore_complete` 글 바뀜 |
| 봉인 | `SHA256SUMS` 76 | 다시 (`seal_kit.py --write`) |
| 키트 README | §0 · §2 · §3 · §4 | 이름 (RT1 · RT2 · `rt.bin` · `post/rt_*`) · 덱 표 · 단계 · 복원 판정 행 |

## 15-3. 그대로

- R 덱 바이트 (PRE · POST · G1 · G2 · 26 열 쌍 덤프 · mesh · G3 · R_END · UN 소거) · UNread · UK · Ut0.
- G0 = 원 마지막 조각 덱 ↔ R 덱 (지금 그대로 · RT 는 15-4 lint 로 — QA3).
- 허용폭 식 1e-5 × max(\|D1\|, 그 열 \|D1\| 중앙값) · 이력 4 열도 같은 식 (메모 §3 · Q2) · `%.17g` 에서 좁히지 않음.
- NP 6 · LMP sha256 · S0 · 판정 범주 넷 · 다른 복원 입력 (reset 로그 다섯 · PRE = POST · UN 소거 · 이력 시험 H0–H5 + SYN + 총힘 시점 · 문법 fixture 사전 점검).
- REG §14 머리의 "바꾸지 않는 것" 전부 · 언로딩 팔 · 순서 §13-6 · RJ 323957 기록.

## 15-4. RT 덱 꼴 (생성기가 만든다 · 손으로 고치지 않는다 · 숫자 = 표에서만)

```
# >>> block head      ← R 의 head 블록과 바이트 같음 (r8 머리 글자 · compute cpl … 26 열 정의 포함)
# >>> block r_params  ← R 과 같음 (ul_bed · ul_s0 (index) · ul_atoms0 · ul_big)
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
- GD17 lint: head 블록 = R head 블록 바이트 · RT1 − RT2 = `write_restart ${out}/rt.bin` 한 줄 · `uncompute cpl` < `compute ul_ph` < 덤프 < `run 0` < `write_restart` · 함께 사는 pair/gran/local ≤ 1 (⑮ 규칙) · 블록 rt 밖 새 명령 0 · 새 ID = `ul_` 접두.
- 러너: RT1 = `run_deck "$JD/RT1" RT1 "$CKPT0" - 0` · RT2 = `run_deck "$JD/RT2" RT2 "$JD/RT1/rt.bin" - 0` — 같은 NP 6 · LMP · mpirun 줄 · `Loop time … on 6 procs` 검사 (지금 `run_deck` 그대로 · 191–199 행).
- 덤프 = `post/` (경량 묶음에서 빠진다 · `run_unload.sh` 215 행) · `rt.bin` = `*.bin` 제외.  크기 어림 (7:3): 쌍 562605 × 30 열 ≈ 370 MB × 2 · 원자 ≈ 40 MB × 2 · rt.bin ≈ 80 MB [추정].

## 15-5. 판정 규칙 (결과 전 · 키트 판독기)

| G2c′ | 조건 | 복원 판정 |
|---|---|---|
| PASS | RT1 · RT2 기술 성공 (rc 0 · ERROR · UL_ABORT 없음 · 배너 · `on 6 procs`) ∧ 두 쌍 덤프 전부 읽힘 (머리 · 열 이름 `c_ul_ph[1–30]` · 행 수 · 유한 · ID 정확한 양의 정수) ∧ TIMESTEP 둘 다 = S0 (RJ2 = S0′) ∧ 쌍 집합 같음 ∧ 다른 값 중복 키 0 ∧ 공통 쌍 · 열마다 \|D2 − D1\| ≤ 1e-5 × max(\|D1\|, 그 열 \|D1\| 중앙값) | 다른 관문 모두 PASS 면 RESTORED |
| FAIL | 값 · 집합 · 다른 값 중복 · TIMESTEP 중 하나 위반 | VALUE_MISMATCH |
| NOT_COMPUTED | 쌍 덤프 없음 · 필수 열 결손 (`ULPR-04` 꼴) | UNCONFIRMED |
| (계산 안 함) | RT1 · RT2 기술 실패 | SYNTAX_FAIL (REG §14-10) |

- 정규화 = 지금 G2c 와 같음: 무순서 키 (작은 id, 큰 id) · 방향 바뀐 행 = 위치 맞바꿈 · 힘 9 · shear 3 부호 반전 · deltaMax 그대로 · 위치 · 접점 = 상자 (0.05 × 0.05) 로 감음 · torque · 주기 표지 = 판정 밖 · 집합 차를 "MPI 끝자리" 로 면제하지 않음 (REG §12-1).
- D1 = RT1 (기준쪽) · D2 = RT2.  [왕복] 의 주장은 D2 = D1 (D1 = 파일 원값이 아님 — setup 이 deltaMax 를 올린다 · 메모 §0-1 ①).
- 함께 적음 (판정 아님): 비트 같은 쌍 수 · 원자 12 열 비트 같음 · 두 덤프 sha256 같음 · 열별 최대 상대차 · 판별력 (D1 접선력 0 아닌 몫 · \|shear\| > 0 몫) · 주기 표지 쌍 수 · (QA4) 벽 열.
- [연속] = `ul_gates.g2c_compare(R/g2/contact_S0, in/contact_S0)` 그대로 → `checks['G2c_cont']` · 상태 · n_mismatch · 열별 수 — 판정 · 다음 제출 관문 · `restoration_verdict` 입력 아님 · 열 결손이어도 "계산 못 함" 보고만 · 새 문턱 없음.
- 다른 입력 (`ul_gates.restoration_verdict`) 그대로 · G1 · G2 · mesh md5 · G3 그대로.

## 15-6. 결과 전 예측 (ibb RJ · RJ2 · NP 6)

| # | 대상 | 예측 = 맞음 기준 | 근거 · 표지 | 틀리면 |
|---|---|---|---|---|
| A-1 | RT1 · RT2 기술 | rc 0 · `on 6 procs` · step = S0 (RJ2 = S0′) · 원자 = 표 `ul_atoms0` | R 과 같은 머리 · 같은 파일 | SYNTAX_FAIL · 그 침대 멈춤 (REG 그대로) |
| A-2 | G2c′ 판정 | PASS · n_mismatch 0 | 직렬 다 · 라 PASS (11-12) + 초안 B 결론 ① (NP 2 · 4) · NP 6 · 상자 0.05 로 옮김 = [추정] | VALUE_MISMATCH = 그 침대 U 없음 · 멈춤 → 1저자 · 직렬 · 초안 B 와 다른 까닭부터 |
| A-3 | 비트 · 바이트 | 비트 같은 쌍 = 전부 · 원자 12 열 비트 같음 · 두 쌍 덤프 sha256 같음 | 직렬 다-값 · 다-바이트 · 라-값 · 라-바이트 맞음 (11-12) | 비트 · 바이트 예측만 거둠 (판정 PASS 면 판정 그대로) |
| A-4 | [연속] · 주기 S0 다섯 (RJ) | FAIL (n_mismatch > 0) · 7:3 = n_mismatch 545583 · R 쌍 덤프 sha256 `193e6e6c…` (323957 과 같음 · `docs/reviews/codex_p1_g2c_diagnosis_20261027/real_run_20261027/README.md` 5 행) | ㉠ + ㉡ · 7:3 재현 = 같은 LMP · R 덱 · NP · 격자 · S0 → 같은 R 덤프 [추정 · 결정성] | 보고만 · 7:3 수 · sha256 다르면 결정성 서술만 거둠 |
| A-5 | [연속] · 10:0 RJ2 (S0′ = 명령 파일) | FAIL (n_mismatch > 0) · 불일치는 고스트 쌍 쪽 (주기 표지 ∪ EXT 격자 랭크 경계) 에 몰림 = [추정] (랭크 경계 분류는 이번 판독기 밖 · 주기 표지 쪽 수만 함께 적음) | ㉡ 만 (명령 파일 = 동기한 이력) · 직렬 C kit26 FAIL 331 ≤ 표지 334 | 보고만 |
| A-6 | 나머지 관문 | REG 기대 그대로 | R 덱 · 판독 안 바꿈 | REG 규칙 그대로 |
| A-7 | 벽 (QA4 예면 · 보고) | RT2 = RT1 (바닥 4 열 · 판 local · 비트) | 첫 setup 뒤 상태를 rt.bin 이 담음 [추정 · 샌드박스 밖 · 메모 §0-1 ③] | 벽 왕복 서술만 거둠 |

- [이력] 앵커 = 해당 없음 (원 덤프 · EXT 덤프에 이력 열 없음).  "이력이 실제로 읽혔다" 는 [왕복] 밖 — H0–H5 PASS · reset 로그 (지금도 판정 입력) · [연속] 분포 (보고).

## 15-7. C12 중력 팔 — QA2 에 달림

- 지금: `_g_restore` (`ul_reader.py` 1096–1118 행) 가 G_ 팔 setup 덤프 ↔ 출처 팔 R_M **창 끝 (in-run)** 덤프로 G2c → ㉡ 때문에 예측된 실패 (R_M = `write_restart` 명령 파일 · `make_unload_decks.py` 410 행 — 명령이어도 직렬 [연속] C 가 kit26 FAIL 331).
- 개정 (예면): G_ 잡의 G_ 덱 앞에 GT1 (R_M → P → `write_restart`) · GT2 (그 파일 → P) · 판정 = GT2 ↔ GT1 (15-5 같은 규칙 · TIMESTEP = R_M) · 옛 C12 G2c = [연속] 보고 · G1 · G2 그대로 · G3 해당 없음 그대로.  덱 + 10 · 생성기 GD18 · 판독기 R42 · 러너 M27.
- [이력] 후보 (출처 팔 R_M 창 끝 쌍 덤프에 이력 열) = U 덱 변경이라 이번 밖.

## 15-8. 주장하지 않는 것

- 원 런 스텝 끝 덤프 ↔ 재개 setup 의 연속성 · `write_restart` 비트 동일성 (비트 · 바이트 = 예측일 뿐).
- G2c′ PASS = 이력이 실제로 읽혔다 (맹점 — 두 쪽이 같이 잃으면 통과 · 막는 것 = H0–H5 · reset 로그).
- 주기 S0 파일이 원 런 H(S) 를 담는다 — **S 상태 = 파일 상태** (x · v · ω · 벽 이력 = S 끝 · 쌍 shear = S 힘 계산 전 사본 · 직렬 = H(S−1) · MPI = 초안 B).
- RJ 323957 소급 PASS · "등록 기대 오류로 설명됨" (11-02 보고 §4 — 표지로만).
- 허용폭 변경 · P1 수치 인증 · 언로딩 물리 결과 · 벽 이력 판정 (QA4 = 보고만) · `force_normal` 차이 = 법선 모델 힘 차이.
- NP 2 · 4 (초안 B) 결과가 NP 6 · 생산 침대에서 같다는 것 (추정으로만 씀).

## 15-9. 순서

1. 이 초안 → 내부 반박 리뷰 (문서) → 1저자 비준 (QA1–QA6).
2. 키트 수정 (시험 먼저 — 고치기 전 실패 → 고친 뒤 통과 · 변이 시험): 생성기 GD17 · 러너 M26 · 판독기 R41 · `g2cp_compare` · 차등 시험 · 활성 규칙 25 · README · 봉인 다시 → 게이트 → 커밋.
3. 내부 반박 리뷰 (코드 · CLAUDE.md 사전 공격 ①–③).
4. 초안 B 결론 ① (NP 2 · 4 같은 NP [왕복] PASS) 확인.
5. 1저자 GO → ibb RJ (새 폴더 · 새 시도 · 침대 차례 = REG §13-5 ② 그대로 · 7:3 = QA6).

## 15-10. 보장 · 작은 반례 (내부 반박 리뷰가 깨 볼 것)

| 보장 | 깨 볼 작은 반례 |
|---|---|
| RT1 · RT2 는 읽는 파일만 다르다 | RT1 = RT2 + 두 줄 · `write_restart` 가 `run 0` 앞 (setup 없이 F′ = F → 맹점 통과) · 러너가 두 단계에 다른 `-var` · NP |
| G2c′ PASS = 같은 경로 재현 | 두 쪽 shear 가 같이 0 (읽기에서 잃음) → PASS — 그 몫을 H0–H5 · reset 로그가 막는다는 것이 시험 · 문서에 보이는가 |
| 옛 G2c 는 판정 밖 | 1619 행 목록에 'G2c' 가 남음 · 다음 제출 관문이 `G2c_cont` 를 읽음 · [연속] 열 결손이 UNCONFIRMED 로 샘 |
| 필수 열 결손 = NOT_COMPUTED | 열 이름 하나 중복 · `c_ul_ph[30]` 없음 · 31 열 · 26 열 덤프를 RT 자리에 둠 |
| 30 열 판정 = 샌드박스 §3 판정 | 같은 합성 침대에서 상태 · n_mismatch 다름 (차등) · shear 부호 반전 빼기 · deltaMax 부호 반전 넣기 변이 |
| TIMESTEP = S0 | RT2 가 S0 + 1 · RT1 덤프가 `run 0` 전 `write_dump` |

## 15-11. 1저자가 정할 것

- [Ⓐ 언로딩] **QA1** — 이 개정 (RJ · RJ2 에 RT1 · RT2 · G2c′ 판정 · 옛 G2c = [연속] 보고) 을 비준할지.  권고: 예 · 키트 수정 (시험 먼저) 은 바로 · ibb RJ 는 초안 B 결론 ① 뒤.
- **QA2** — C12 (중력 팔) 도 같은 개정에 (15-7).  권고: 예 (지금 규칙이면 고스트 쌍 때문에 예측된 실패 · 봉인 한 번에).
- **QA3** — G0 처리.  권고: G0 는 R 만 (지금 그대로) + RT 머리 = R 머리 바이트 lint (GD17 · 봉인) — G0 허용목록을 넓히지 않는다.
- **QA4** — 벽 이력 (바닥 4 열 · 판 local) 을 RT 덤프에.  권고: 넣되 보고만 (샌드박스가 안 본 길 · 메모 §0-1 ③ · Q12).
- **QA5** — 리뷰 자리.  권고: 내부 반박 리뷰 (독립 조수 · "Codex 아님" 표기 · 1저자 11-10 운영 결정) · Codex 남은 한 번 = Rint ② 봉인 전 묶음 그대로.
- **QA6** — 7:3 다음 RJ (323957 = VALUE_MISMATCH 그대로).  권고: 15-9 의 2–4 뒤 1저자 GO 로 새 폴더 새 시도 · 재시도 수 셈 = 1저자 · 이 초안은 실행을 승인하지 않는다.

## 15-12. [미확인] · [추정]

- [추정] 생산 머리 (판 mesh 벽) + 30 열 키워드 조합의 문법 — 요소는 확인됨 (이력 시험 소비자 job 283122 PASS · 샌드박스 30 열) · 조합은 키트 시험 · 첫 RJ 가 처음.
- [추정] NP 6 · 상자 0.05 의 [왕복] (초안 B = NP 2 · 4 · 상자 0.012) · 7:3 R 덤프 재현 (결정성) · 벽 왕복 · restart `.bin` 차이 = 머리 글자 · 크기 어림.
- [미확인] RT 단계 시간 (ibb) · 11-12 결과의 리포 반입 (메모 §8 빈칸 — 이 초안의 11-12 숫자는 받은 묶음에서 읽음).
