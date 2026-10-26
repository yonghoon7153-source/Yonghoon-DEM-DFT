# DEM 언로딩 키트 — ps45 다섯 침대 (등록 개정 2 · 시험 먼저) · ⛔ 본 R · 10:0 이완 연장 · 개발 / 생산 U = Codex (키트 증거 + 개정 2) 뒤

- 등록 (정본): `docs/reviews/dem_unloading_ps45_prereg_20261009.md` (이하 REG — §12 개정 1 · §13 개정 2) · 반영 계획 `docs/reviews/dem_unloading_ulr1_fix_plan_20261012.md` (✅ 1저자 10-12 Q1–Q4 권고대로) ·
  Codex 판정문 `docs/reviews/codex_review_dem_unloading_prereg_20261011.md` (CX1) · `docs/reviews/codex_review_dem_unloading_prereg_rereview_20261012.md` (CX2).
- ⛔ **10-14 Codex 키트 재검토 (핀 `2783061ea`) = HOLD** — 이력 시험은 수용 · 본 키트 판독 · 복원 · 후속 · 러너에 P1 여섯 (`ULKR-01`~`06`) · P2 여섯 · 판정문 `docs/reviews/codex_review_dem_unloading_kit_20261014.md` · 수정 계획 `docs/reviews/dem_unloading_kit_fix_plan_20261014.md` (✅ 1저자 10-14 Q1–Q9 권고대로 = 전부 (가)).
  → ✅ **수정 10-14 (시험 먼저 · 등록 개정 3 = REG §14 · 실행 기록 = 계획 §5)** — §2–§5 = 수정 뒤 판 · ⬜ 문법 fixture ibb (§1-6 · 실행 1 = fixture 결함 `SELF-115` · 고침 `039abb141` → 실행 2 · 1저자) · ⬜ Codex 짧은 재확인
  (`docs/reviews/codex_dem_unloading_kit_fix_recheck_request_20261014.md` · 발송 = 1저자) · ⛔ 본 R · 10:0 연장 · U = 재확인 GO 뒤.
  → ⛔ **Codex 재확인 (10-14 · 핀 `a30fe150e`) = HOLD** — ULKR-01–12 원 수정 대부분 좁게 닫힘 · 새 P1 셋 (`ULKRR-01` 문법 fixture 스칼라 ↔ 벡터 = `039abb141` ·
  `ULKRR-02` RESUME 없는 중복 행 소거 · `ULKRR-03` 판독기 rc 를 다음 관문이 안 읽음) · P2 하나 (`ULKRR-04` 소수 ID · 필수 열) · 판정문 codex_review_dem_unloading_kit_reverify_20261014.md ·
  수정 계획 dem_unloading_kit_reverify_fix_plan_20261014.md (✅ 1저자 10-14 Q1–Q7 권고대로).
  → ✅ **수정 10-14 밤 (시험 먼저 · 이 README §3 · §4 · §5 · §9 = 수정 뒤 판)** — 이어 돌림 경계 · 잡 완료 영수증 (fails=0 · reader_rc=0) · ID 정확한 양의 정수 ·
  창 연속 (w · 간격) · 문법 fixture PASS = RJ · RJ2 · EXT 사전 점검 (Q5 강제) · UC = fresh-attempt-only · Linux 전체 로그
  (`docs/reviews/dem_unloading_kit_reverify_fix_evidence_20261014/`) → ⬜ ibb 문법 fixture 실행 2 (실제 바이너리) · ⬜ Codex 짧은 재확인
  (`docs/reviews/codex_dem_unloading_kit_reverify_fix_recheck_request_20261014.md` · 발송 = 1저자).
  → ⛔ **Codex 수정 재확인 (10-15 · 코드 핀 `eaecfba2a`) = HOLD** — 앞 반례 대부분 닫힘 (ULKRR-03 원반례 닫힘) · 새 P2 셋 (`ULKRF-01` 같은 RESUME 사건 두 줄이 승인
  하나를 둘로 · `ULKRF-02` 승인된 재개의 유지 창이 늘면 새 단 기록 거부 · `ULKRF-03` G2c 열 결손 = KeyError) · Q2 영수증 범위 · Q4 문법 사전 점검 = 판정 JSON 만 (캐시 신뢰 경계) ·
  판정문 docs/reviews/codex_review_dem_unloading_kit_fix_recheck_20261015.md · 수정 계획 docs/reviews/dem_unloading_kit_fix_recheck_fix_plan_20261015.md (✅ 1저자 10-15 Q1–Q4 권고대로).
  → ✅ **수정 10-15 (시험 먼저 · 이 README §1-6 · §3 · §4 · §5 · §9 = 수정 뒤 판 · 등록 §14-11)** — 경계 하나에 승인 한 번 · k 되돌아옴 = 새 시도 시작 · G2c 파서 문제 먼저 ·
  문법 사전 점검이 그 런 원자료를 승인된 판독기로 다시 읽음 (Q3) · ID 정수 토큰 정확 (Q4) · Linux 전체 로그 (`docs/reviews/dem_unloading_kit_fix_recheck_fix_evidence_20261015/`)
  → ⬜ Codex 짧은 재확인 (`docs/reviews/codex_dem_unloading_kit_fix_recheck2_request_20261015.md` · 발송 = 1저자) · ⬜ ibb 문법 fixture 실행 2.
- **10-23 ULPR 보완**: 재개 중단의 창·단·사건 소속을 대조하고, G2 입력과 요청 시점 검증 및 G2c 열 결손 분류를 보완한다. 현재 재확인 요청은 `docs/reviews/codex_dem_unloading_ulpr_recheck_request_20261023.md`이며, 본 실행은 외부 재확인 GO 뒤다. 과거 시험 수는 아래 이력의 해당 판에만 적용한다.
- **10-24 외부 정수 재검토와 표지 경계 보완**: `01c1aaf5be8acdf7d1716f34cc86fc77d8e27362`의 정확한 정수 파싱 교정은 수용됐고, 기록 무결성 종결은 새 P2 `ULPRI-01/02` 때문에 HOLD다. 이번 R40은 변형 RESUME 표지와 다른 문자열 뒤 manifest 줄 구분자의 우회를 막는 로컬 수정이다. 새 요청서 `docs/reviews/codex_dem_unloading_ulpri_recheck_request_20261024.md`의 재확인 대상이며 외부 GO를 받았다는 뜻은 아니다. 이전 검토 핀·제출 ZIP·NOTE는 보존한다.
- 이 README 가 **이름의 정본**이다 (REG §8-2 "이름은 가칭 · 키트 README 가 정본").
- 지금 할 수 있는 것 = **§1 작은 침대 이력 시험 (H0–H5) 만** — 본 키트 봉인과 따로 봉인 (`history_test/SHA256SUMS`) 해서 먼저 돌릴 수 있다.
  ⛔ 이 시험이 PASS 여도 본 R · 10:0 연장 · U 의 GO 가 아니다 (CX2 §0 · REG §13-6 — 키트 증거 → Codex 재검토 → 본 실행).
- 본 키트 (§2–§6) = 만들고 합성 · 모의 시험까지 (10-13).  ⛔ 실행 = 부록 초안 (권고 기본값) 1저자 비준 → Codex 키트 재검토 GO 뒤.
  부록 초안 `docs/reviews/dem_unloading_kit_section13_appendix_draft_20261013.md` · 요청서 초안 `docs/reviews/codex_dem_unloading_kit_request_20261013.md`.
- 이 컨테이너에는 LIGGGHTS 가 없다 — 덱 문법은 소스 판독 (CX2 §5 · 노트 · 3d5c00f 원문) + 생성기 selftest 까지이고, 실제 바이너리는 §1 의 ibb 시험이 처음이다.

## 0. 이름 (정본)

| 무엇 | 이름 |
|---|---|
| 키트 폴더 | `docs/data/ps45_unload_20261009/` |
| 이력 시험 (H0–H5 · 따로 봉인) | `history_test/` — `make_history_decks.py` (생성기 · `--check` · `--selftest`) · `read_history.py` (읽는 쪽 · `--selftest` · `--grammar`) · `run_history.sh` (러너 · `--grammar-only`) · `run_history_ibb.sbatch` (ibb 래퍼 · 둘째 인자 `grammar`) · `history_params.json` (fixture 표) · 덱 아홉 `in.hist_*.liggghts` (H0–H5 여덟 + 문법 fixture `in.hist_grammar.liggghts` · §1-6) · `plate_hist.stl` · `SHA256SUMS` |
| ibb 작업 폴더 (이력 시험) | `~/ps45_unload_hist_20261013` (런 = 그 아래 `hist_<시각>/` · 보고 묶음 `hist_<시각>.report.tgz` · 문법 fixture = `gram_<시각>/` · `gram_<시각>.report.tgz`) |
| SLURM job 이름 | `ulHist` (이력 시험) · `ulU` (본 키트 — 잡 하나에 sbatch 하나) |
| 본 키트 표 (하나뿐) | `unload_params.json` — 덱 생성기 · 러너 · 읽는 쪽이 여기서만 읽는다 |
| 덱 생성기 · 덱 | `make_unload_decks.py` (`--check` · `--selftest`) · `decks/<침대>/in.<종류>.liggghts` 64 (손으로 고치지 않는다) |
| 공용 · 판정 모듈 | `ul_lib.py` (덱 언어 · 덤프 · thermo) · `ul_s3.py` (K5 S3 총힘) · `ul_observers.py` (K6 σ_P · 표면 · S4 · ε · W_proxy · KE 기준) · `ul_gates.py` (K7 G0 · G1 · G2 · G2c · G3 · S0′) · `ul_reader.py` (K4 판독 · 선택 · 관문 · 복원 판정) |
| 러너 · 래퍼 · 모의 시험 | `run_unload.sh` · `run_unload_ibb.sbatch` · `ul_runner_test.py` (가짜 mpirun · lmp) |
| 봉인 · 활성 규칙 | `seal_kit.py` · `SHA256SUMS` (76 파일) · `active_rules.json` (규칙 24 · 폐기 규칙 0 건) |
| ibb 작업 폴더 (본 키트) | `~/ps45_unload_20261009/` — `<침대>/in/` (원 파일 여섯) · `<침대>/<잡>/` (런 폴더) · `kit_<시각>_<침대>_<잡>_XXXX/` (러너 kit 사본) · `logs/` (SLURM 출력) |
| 잡 (`run_unload.sh <침대> <잡>`) | `RJ` (복원 시험 — 7:3 은 Ut0 먼저) · `EXT` · `RJ2` (10:0) · `UB` · `UT` · `UC` · `UVa` · `UVb` · `UT3` · `UTc` · `G_UB` · `G_UVa` · `G_UVb` · `G_UT3` |
| 덱 종류 | `R` · `UNread` · `UK` · `UC` · `U_UB` · `U_UVa` · `U_UVb` · `U_UT3` · `G_<팔>` · (7:3) `UT` · `Ut0` · (10:0) `EXT` · `EXT2` |
| 판정 JSON · 파일 | `<침대>/RJ/g0.json` · `restore_verdict.json` · `<침대>/ul_base.in` (KE 기준 · S2) · `<침대>/<팔>/arm_verdict.json` (주 값 · 보조 — 분리 · 표면 · ε · W_proxy) · `<루트>/ps_7_3_r45/selection.json` · `<루트>/ps_10_0_r45/s0_decision.json` · `report.json` · `ps_7_3_r45/UTc/parent_UT.sha256` (UT 부모 관측 목록 · §14-3) |
| 런 폴더 기록 (덱이 쓴다) | `ul_windows.csv` · `ul_steps.csv` · `ul_events.csv` (머리 = 표 records) · `ul_summary.txt` · `dump/` (창 끝 atom · wall · contact · mesh) · `restart/` (단 끝 `restart_unload_<step>.bin` + `state_unload_<step>.in` · `restart_RM_*` · `state_RM_*`) |
| 런 폴더 기록 (러너가 쓴다) | `screen.txt` (이어 돌림 `screen_a2.txt`) · `log_*.liggghts` · `deck.liggghts` · `deck.txt` · `run_manifest.txt` · `run_check.txt` · `<잡>.report.tgz` |
| 문법 fixture 판정 (RJ · RJ2 · EXT 의 사전 점검 입력 · Q5) | 환경 변수 `GRAMMAR_VERDICT` = `~/ps45_unload_hist_20261013/gram_<시각>/grammar_verdict.json` (§1-6 실행 2 의 PASS 런 · 이름으로 고정) · 통과하면 잡 기록에 `grammar_prereq=PASS` · `grammar_verdict=` · `grammar_verdict_sha256=` |

## 1. 작은 침대 이력 시험 (H0–H5) — 먼저 · 1저자 ibb · 결과 0 건

**왜** (REG §12-1 ③ · §13-6 ③ · CX2 §5 · 계획 §2 마지막 줄): 복원 관문의 관측자 (primitive 바닥 `history_zwall_bot` · mesh 판 `wall/gran/local` · 입자쌍) 가
**알려진 이력을 실제로 보는지** · **지워진 이력과 가를 수 있는지** 를 작은 침대에서 먼저 확인한다.  생산 S0 에는 과거 이력 열이 없으므로 (CX2 §5-4)
관측자의 판별력은 이 시험이 증거다.

### 1-1. fixture (`history_test/history_params.json` · 생성기가 자리 계산 · 산술 검사)

- 입자 20 · **적분하지 않는다** (운동학 fixture — 위치 · 속도는 명령으로만 바뀐다).  모델 머리 (재료 m1–m9 · pair · 바닥 primitive 벽 · 판 메시 벽 · 중력 9.81 · 감쇠 1.0e-5 · `fix_modify zwall_top energy yes`)
  = r8 원 덱 글자 그대로 (리포 tgz 멤버 sha256 `097658aa…` · 숫자를 다시 적지 않는다) · 머리 fix 순서 = 원 PHASE 4 (zwall_bot → integr → gravi → top_mesh → zwall_top → damp).
- 집합: B 넷 (바닥 접촉 · AM_P · AM_S · SE 포화 · SE 비포화) · T 넷 (판 접촉 · 같은 네 종) · 쌍 다섯 (AM_P–AM_P · AM_P–SE · SE–SE · AM_S–SE · AM_P–AM_S · 셋은 NP 분할면을 걸친다) · Z 둘 (접촉 없음).
- 만드는 법: ① 설계 deltaMax 겹침 자리에서 run 10 (setup 에서 history[0] = max(0, δ)) ② `set atom` 으로 부분 제하 (현재 δ < deltaMax) ③ 접선 속도 (법선에 수직) 로 run 1000 → shear += v_t·dt
  ④ 속도 0 · run 990 → 마지막 step 2000 의 in-run 덤프 = **봉인할 기대값** · write_dump 묶음 · `write_restart fixture.bin`.
- 생성기 산술 검사 (selftest ③): 의도한 접촉만 (바닥 4 · 판 4 · 쌍 5) · 의도 밖 이웃 0 (setup 분리 소거 경로 회피) · 판 대각 이음매 · 주기 경계 밖 · 모든 sentinel 이 압축 가지 (이력 식 · 덱 m6 · m8) ·
  접선 ≤ Coulomb 한도의 50 % · 접선 ⊥ 법선 · 포화 · 비포화 둘 다.

### 1-2. 단계 (한 job · `#SBATCH -n 6` ↔ `mpirun --oversubscribe --bind-to none -np 6` · H2 만 `-np 4`)

| 단계 | 덱 | NP | 무엇 | 행 |
|---|---|---|---|---|
| P | `in.hist_producer` | 6 | fixture 생산 · 끝 덤프 · `fixture.bin` · 자동 restart 1500 (run 끝 자동 쓰기 확인) | H0 · 기대값 |
| C6 | `in.hist_consumer` | 6 | 별도 프로세스 재개 — PRE_SETUP (write_dump · primitive 배열 그대로) · POST_SETUP (run 0 · mesh · pair local) | H1 |
| C4 | 같은 소비자 | **4** | NP 바꿈 재개 (행 순서 무시 · pair 무순서 키 + 방향 바뀐 shear 부호 정규화) | H2 |
| Ebot → Cbot | `in.hist_erase_bot` → 소비자 | 6 | 진단 사본: run 0 → undump · uncompute → `unfix zwall_bot` → 진단 restart → 새 프로세스 | H3 |
| Etop → Ctop | `in.hist_erase_top` → 소비자 | 6 | 같은 꼴 · `unfix zwall_top` (top_mesh 기하는 그대로) | H4 |
| Enone → Cnone | `in.hist_erase_none` → 소비자 | 6 | 양성 대조 — 같은 직렬화 횟수 · unfix 없음 | H3 · H4 대조 |
| BAD | `in.hist_badid` | 6 | 잘못된 내부 ID (`history_zwallbot`) — ERROR 가 나야 한다 (rc ≠ 0 이 기대값) | H5 |
| SYN | `in.hist_syntax_probe` | 6 | 본 키트 덱 문법 미리 지나가기 (read_restart 뒤 dt 5e-7 · erotate/sphere · ave/time · 부호 있는 Ps · 영역 개수 판 접촉 ↔ 벽 local 덤프 · move/mesh +z · mesh 덤프 · 명시 write_restart) + **판 접촉 법선력 부호** (입자가 받는 fn_z · 압축 상태) | 정보 (판정 밖) |
| PZ → CZ | `in.hist_producer_zero` → 소비자 | 6 | 0 뿐 fixture (모든 겹침 −1e-4) | H5 |

### 1-3. 판정 (읽는 쪽 `read_history.py` · 결과 전 고정 · CX2 §5-2 표 그대로)

| 행 | PASS 조건 | 아니면 |
|---|---|---|
| H0 문법 | 단계마다 rc 0 · 배너 LIGGGHTS-PUBLIC 3.8.0 · 3d5c00f · ERROR 0 · `Loop time … on N procs` 의 N = 그 단계 NP · 덤프 머리 · 열 이름 · 행 수 · 소비자에 내부 이력 fix 다섯의 restart reset 로그 (global · per-atom) · 생산자 write_dump 묶음 = in-run 덤프 | TECH (성공했다고 값 보존까지 통과시키지 않는다) |
| H1 · H2 | 원자 상태 · primitive PRE_SETUP = 생산자 끝 (글자 → float 정확히) · primitive · mesh · pair POST_SETUP = 생산자 끝 (상대 1e-12 · 절대 1e-18 덱 m) · 키 집합 같음 · 다른 값 중복 키 0 | FAIL (값) · TECH (열 · 키 · 비유한) · **INCONCLUSIVE (그 종류에 sentinel 0)** |
| H3 바닥 소거 | Cbot PRE 바닥 이력 전부 0 · POST shear 0 · deltaMax = 현재 겹침 (다시 찰 수 있다 — **"setup 뒤 4 열 0" 을 기대하지 않는다**) · sentinel 전부 deltaMax 감소 · 판 · 쌍 = 생산자 · 양성 대조 PASS · 소거 전 관측 = 생산자 · Cbot 에 `history_zwall_bot` reset 로그 없음 | FAIL · INCONCLUSIVE · TECH |
| H4 판 소거 | 같은 꼴 (mesh) · 바닥 PRE · POST = 생산자 · Ctop 에 `tracker_top_mesh` reset 로그 없음 | 같음 |
| H5 | 잘못된 ID → **TECH** (rc ≠ 0 · fix ID ERROR) 로 · 0 뿐 → **INCONCLUSIVE** 로 (0/0 PASS 아님) 분류됨 | FAIL (잘못된 ID 를 받아들임 · 0 뿐을 PASS 로) |

- sentinel = 생산자 끝에서 저장 deltaMax − 현재 겹침 ≥ 1e-9 이고 \|shear\| ≥ 1e-9 (덱 m) 인 접촉 (CX2 §5-2 비퇴화 조건).  설계상 primitive 4 · mesh 4 · pair 5.
- 정보 (판정 밖): ⓐ **run 끝 자동 restart** — 생산자 run 끝 (10 · 1010 · 2000 · 1500 의 배수 아님) 에 `auto_*.bin` 이 생기는가 (CX2 §6 — 10:0 연장 끝 3,660,000 은 50,000 배수가 아니다 · 본 키트 연장 덱은 어느 쪽이든 끝에서 **명시 write_restart** 하고 러너가 파일을 확인한다)
  ⓑ **총힘 출력 시점** — 접촉 없는 Z 입자의 덤프 fz = −m g · fx = fy = 0 (덤프 f 가 중력까지 더한 총힘 = S3 함수 입력 · K5) ⓒ SYN 문법
  ⓓ **판 접촉 법선력 부호** `plate_fn_sign` — 압축 중인 판 접촉에서 입자가 받는 fn_z 가 모두 음수면 −1 · 모두 양수면 +1 · 섞이면 SYN FAIL.  본 키트 상쇄 (TENSION) 판별이 이 약속을 쓴다 —
  결과가 표의 `plate_fn_compressive_sign` 과 다르면 표를 고친다 (결과 0 건 상태 · 판정 전).
- 결과 전 기대: H0–H5 PASS · ⓑ PASS · SYN = 판 접촉 4 → 3 (T4 가 1e-5 들어 올림에서 떨어진다) · ⓓ −1 (판이 위에서 누르면 입자가 받는 힘은 −z — 내 추정 · 미확인) · ⓐ 미리 정하지 않는다.  다르면 그대로 보고한다 — 덱을 손으로 고치지 않는다 (생성기 → 새 SHA256SUMS → 다시).

### 1-4. ibb 명령 (1저자 · 꺾쇠 자리표시 = 접속 정보뿐 · 나머지는 그대로 붙여 넣는다)

```bash
# ① 이 커밋의 새 작업 트리 (커밋마다 새 폴더 · 이미 있으면 다시 체크아웃하지 않는다)
cd ~/Yonghoon-DEM-DFT && git fetch -q origin claude/stoic-knuth-NObVQ && W=$HOME/unload_src_$(git rev-parse --short FETCH_HEAD) && { [ -d "$W" ] || git worktree add -q --detach "$W" FETCH_HEAD; } && cd "$W" && git log --oneline -1
H=$W/docs/data/ps45_unload_20261009/history_test
conda activate myenv && python3 -I $H/make_history_decks.py --check && python3 -I $H/read_history.py --selftest | tail -1   # "✓ check … 14 파일" · "selftest: PASS (0 실패)"
# ② 작업 폴더 · 제출 전 사전 점검 (로그인 노드 · 런 없음 · LMP = /lustre$HOME/LIGGGHTS-PUBLIC/src/lmp_mpi · sha256 = 등록 §11-1 ⓖ 빌드여야)
R=$HOME/ps45_unload_hist_20261013 && mkdir -p $R/logs
bash $H/run_history_ibb.sbatch $H                       # 끝 줄 "✓ 사전 점검만 — 통과" 를 본 뒤 ③
# ③ 제출 (작업 폴더에서 — logs/ 는 제출 폴더 기준) · 다른 job 은 끄지 않는다 · cpu-60 이 차 있으면 PD 로 기다리다 저절로 시작
cd $R && J=$(sbatch --parsable $H/run_history_ibb.sbatch $H) && echo "job $J"
# ④ 진행 · 끝 (수 분)
squeue -u $USER
tail -5 $(ls -t $R/logs/ulHist_*.out | head -1)
cat $(ls -dt $R/hist_*/ | head -1)history_verdict.txt
sha256sum $(ls -t $R/hist_*.report.tgz | head -1)
```

**보낼 것**: `hist_<시각>.report.tgz` (단계마다 화면 · 로그 · 덤프 · 작은 restart · 판정 JSON · kit SHA256SUMS — 입자 20 이라 작다) + sha256 + `logs/ulHist_<job>.out`.
WSL 로 가져오는 꼴 (접속 정보는 자리표시): `scp -P <port> <user>@<ibb-host>:~/ps45_unload_hist_20261013/hist_<시각>.report.tgz ~/`

- rc 0 = H0–H5 전부 기대대로 · rc 2 = 하나라도 아님 (화면 `HISTORY_VERDICT …` 줄 · 행마다 사유).  H0 가 TECH 면 대개 문법 (바이너리) 문제다 — 화면 그대로 보낸다.
- `bash $H/run_history_ibb.sbatch $H` 가 LMP sha256 불일치로 멈추면 다른 바이너리다 — 등록 빌드를 찾는다 (이탈로 진행하려면 `ALLOW_OTHER_LMP=1` · run_manifest 에 남는다 · 1저자 결정).

### 1-5. 실행 기록

- **첫 실행 10-13 (job 281180) = H0–H5 전부 TECH** — sacct FAILED 00:00:11 (ExitCode 2:0) · 읽는 쪽 rc 2 · H0 사유 = rc 1 ·
  `ERROR: Pair gran allows only one compute of type pair/local (../pair_gran.cpp:581)` · SYN = NOT_RUN.  보고 묶음 `hist_20261013_170458.report.tgz`
  sha256 `ae4a77c40e94c564b95d98200d40c044d905330a7a5085f6721ad4d99fc3ec3b` (ibb 에 둠 · 반입 안 함 — 받은 것은 화면 출력뿐).
- **원인 = 이력 시험 덱 결함 (판정 규칙 아님)**: 생성기가 r8 머리 글자 그대로 `compute cpl … pair/gran/local …` 을 넣고 관측용 `compute hb_ph all pair/gran/local id history` 를 더했다.
  LIGGGHTS 는 compute 를 **만드는 순간** pair gran 에 등록하고 하나만 받는다 (3d5c00f `pair_gran.cpp` 581 · `compute_pair_gran_local.cpp` `post_create → init_cpgl` ·
  읽은 원본 sha256 `71c4d3b5…` = `docs/data/liggghts_add_pair_pin.json` 의 ibb · WSL 소스).  SYN 을 뺀 덱 일곱이 같은 꼴이었고 생성기 selftest 는 이 등록 규칙을 몰랐다 (원장 `ULK-02`).
- **고침 (1저자 10-13 Q1 *"권고대로 해"*)**: 덱 일곱에서 `hb_ph` 정의 바로 앞에 `uncompute cpl` (cpl 을 쓰는 덤프는 없다 · `uncompute` 의 `pre_delete` 가 등록을 푼다) · 머리 글자는 그대로.
  시험 먼저 ⑮ (함께 사는 pair/gran/local ≤ 1 · wall/gran/local ≤ 1 · 내리는 compute 를 쓰는 덤프 없음 · 규칙 자체 반례 넷) = 고치기 전 131 중 7 실패 (덱 일곱 · SYN 만 통과) →
  고친 뒤 139 / 139 (+ 머리 cpl 글자 그대로 8) · 읽는 쪽 38 / 38 그대로.  바뀐 파일 = 덱 일곱 · 생성기 · `SHA256SUMS` (SYN · 판 STL · 표 · 읽는 쪽 · 러너 · 래퍼 = 바이트 그대로) ·
  판정 규칙 (§1-3 · 읽는 쪽) 변경 없음.
- 본 키트 덱 64 = 같은 ⑮ 규칙으로 문제 0 (pair/gran/local = 머리 cpl 하나).
- 새 봉인 `history_test/SHA256SUMS` sha256 `241277b20aaccb8d1ab73c79fb9e0758138a3bed64751add98f7849b44697bf6` · 재실행 = §1-4 그대로 (새 커밋 = 새 작업 트리 · 결과는 `hist_<시각>/` 로 갈린다).
- **재실행 10-14 (job 283122 · 작업 트리 `f9edcc416` · dirty 0 · kit 봉인 `241277b2…` · 등록 빌드 LMP) = H0–H5 전부 PASS** · 읽는 쪽 rc 0 · 30 초 ·
  ⓐ run 끝 자동 restart 없음 (1500 배수만 — 본 키트 연장 덱의 명시 write_restart 그대로) · ⓑ 총힘 출력 시점 PASS (S3 C1 가정과 같음) · SYN PASS (판 접촉 4 → 3) ·
  ⓓ 판 법선력 부호 **−1** = 표 `plate_fn_compressive_sign` (표 바꿀 것 없음) — 결과 전 기대와 전부 같다.  컨테이너 재판독 = 같은 판정 JSON (`run_dir` 만 다름) ·
  본 키트 복원 판정의 이력 시험 칸 식 = 통과.  반입 · 대조 = `docs/reviews/dem_unloading_history_test_20261014/README.md` (보고 묶음 sha256 `be0acbd7…` · 바이트 그대로).
  ⛔ 본 R · 10:0 연장 · U 의 GO 아님 — 다음 = Codex 키트 재검토.  ibb 의 런 폴더 `hist_20261014_094731/` 는 지우지 않는다 (§3 ③ 7:3 `RJ` 의 `HIST_VERDICT`).

### 1-6. 문법 fixture (Q8 · 등록 개정 3 §14-9 · Codex 판정문 10-14 §6) — ⬜ 1저자 ibb 한 번 · 본 R 전 PASS · 결과 0 건

> **실행 1 (10-14 19:26 · ibb job 285220 · 작업 트리 `a30fe150e`) = FAIL (rc 2) — fixture 결함 (`SELF-115`)**: P ✓ · GA 기술 ✗ = 첫 창 (step 2100) 뒤 `ERROR: Mismatched fix in variable formula (../variable.cpp:1315)` — fixture 의 `gr_av` ave/time 입력이 하나 (= 전역 스칼라) 인데 `f_gr_av[1]` (벡터) 로 읽었다 · 그 뒤 표지 · 상태 파일 · restart · GB = 돌지 않음 (판정 칸 ✗ 는 전부 이 한 원인의 뒤따름) · 보고 묶음 `gram_20261014_192604.report.tgz` sha256 `015bd82b…` (반입 대기).  본 키트 덱 (`ul_av` 입력 셋) 은 해당 없음.  고침 `039abb141` = 본 키트 꼴 그대로 (입력 셋) + 검사 ⑰ (f_ID 읽는 꼴 ↔ fix 전역 출력 꼴 · `--selftest` · `--check`) · 판정 규칙 · 기대값 변경 없음 → ⬜ **실행 2** (같은 명령 · 새 핀).

**왜**: SYN 은 move/mesh 한 번만 · 상태 파일 복귀 · 변수 주기 덤프를 지나가지 않았다 (판정문 §6 — *"SYN이 지나가지 않은 경로까지 실제 바이너리 PASS라고 확대하지 말 것"*).
빠진 경로만 이 fixture 가 한 번씩 지나간다 · H0–H5 는 다시 돌리지 않는다.

- 덱 `in.hist_grammar.liggghts` (생성기 · 봉인 · 입자 20 · 적분 없음) = 본 키트 U 덱 상태 기계 꼴 그대로 (`ul_` → `gr_`): 맨 바깥 `include ${gr_state}` + `if "${gr_resume} == 1" then "jump SELF gr_resumed"` ·
  변수 주기 덤프 `dump_modify gr_da · gr_dw every v_gr_dnext` (창 전 = 다음 창 끝 · 이동 전 = step + big) · 단마다 `fix gr_mv … move/mesh` → `run` → `unfix` · 단 끝 `write_restart` + 상태 파일 (`print … file` · `append`) ·
  단마다 판 접촉 영역 다시 만들기 · 판 mesh/stl 고정 주기 덤프 (판 z 관측).
- 단계 (한 job · `run_history.sh --grammar-only` · 런 폴더 `gram_<시각>/` · NP 6): **P** (생산자 — H0–H5 의 P 와 같은 덱 · `fixture.bin`) → **GA** (처음 · 빈 상태 파일 · `gr_resume 0` · 창 → 이동 → 창 → 이동 → 창) →
  **GB** (GA 마지막 단 끝 `restart_g_4300.bin` + 짝 `state_g_4300.in` · `gr_resume 1` · 새 프로세스 · 이동 → 창).  GA 가 실패하면 GB 를 돌리지 않는다
  (러너 = 앞 단계 rc 0 **과** 그 산출물 둘 다 — 파일을 다 쓴 뒤 실패한 단계에서 이어 가지 않는다 · P → GA 도 같다 · Codex 판정문 10-14 §6-2 · Q4 (나) · 읽는 쪽 S38–S40).
- 판정 (`read_history.py --grammar` · 표 `grammar_probe` 에서 결과 전 고정 · 전부 참 = PASS · 아니면 FAIL · rc 2):

  | 검사 | PASS 조건 |
  |---|---|
  | 기술 | P · GA · GB rc 0 · 배너 · ERROR 없음 · `Loop time … on 6 procs` · run 수 (GA 5 · GB 2) |
  | 표지 | GA `GRAM_START` (2000 · k 0 · 0.03) · GB `GRAM_RESUMED` (4300 · k 2 · 0.03002 = 상태 파일 값) · `GRAM_STEP` · `GRAM_STATE_WRITTEN` · `GRAM_DONE` · 다른 경로 표지 · `GRAM_ABORT` 없음 |
  | 변수 주기 덤프 | 원자 · 판 local 덤프 step = 창 끝만 (GA 2100 · 3200 · 4300 · GB 5400) — setup · 이동 중 덤프 없음 · 머리 step = 파일 step · 전부 읽힘 |
  | 판 z (mesh/stl · 허용 1e-6) | GA 2000 · 2100 = 0.03 · 2600 = 0.030005 · 3100 · 3200 = 0.03001 · 3700 = 0.030015 · 4200 · 4300 = 0.03002 (두 번째 이동이 앞 이동 위로 쌓인다 · 창 동안 그대로) · GB 4300 = 0.03002 (새 프로세스 첫 setup = restart 의 판) · 4800 = 0.030025 · 5300 · 5400 = 0.03003 |
  | restart · 상태 파일 | 창 끝마다 `restart_g_<step>.bin` + `state_g_<step>.in` = (`gr_rstep` · `gr_k` · `gr_pz`) 세 줄 |
  | 판 접촉 개수 | 덱 영역 공식 (단마다 다시 만든 영역) = 판 local 덤프 (판 아래 중심) |
  | 입력 | GA = 생산자 `fixture.bin` · 빈 상태 파일 · `gr_resume 0` · GB = GA 마지막 단 끝 restart + 짝 상태 파일 · `gr_resume 1` |

- 결과 전 기대 = 전부 PASS (생성기 모의기 ⑯ · 읽는 쪽 합성 S33 이 같은 숫자) · 다르면 그대로 보고한다 — 덱을 손으로 고치지 않는다 (생성기 → 새 SHA256SUMS → 다시).
  ⚠ 짧은 문법 런 = 물리 검증 아님 (C19) · 7:3 `Ut0` 는 그대로 (이중 확인) · PASS 여도 본 R · U 의 GO 아님 (Codex 키트 재확인 뒤).
- **PASS 판정 = 본 R · 10:0 연장의 사전 점검 입력 (Q5 · 1저자 10-14 강제)**: §3 러너는 `RJ` · `RJ2` · `EXT` 의 LIGGGHTS 전에 `GRAMMAR_VERDICT` (이 런의
  `grammar_verdict.json`) 를 `ul_reader.py grammar` 로 대조한다 — 판정 schema · status PASS · exit_code 정수 0 · 검사 19 전부 참 · run_dir = 그 판정 파일 폴더 ·
  run_manifest `mode=gram` · `end` · **LMP sha256 = 지금 돌릴 바이너리** · 단계 P · GA · GB 의 rc 0 · 덱 사본 (`in.hist_producer` · `in.hist_grammar`) + 판 STL sha256 =
  봉인 값 (`039abb141` 판 · 그 런의 kit `SHA256SUMS` 도 같은 값) — 아니면 런 없이 멈춘다.  ~~러너 · 읽는 쪽 스크립트 sha256 은 대조하지 않는다~~ (10-14 판 — 아래 10-15 로 바뀜).
- ✅ **Q3 (1저자 10-15 · Codex 수정 재확인 Q4) — 원자료 재판독**: 사전 점검은 판정 JSON 대조에 더해 **그 런 폴더 원자료를 승인된 판독기로 다시 읽는다** —
  승인된 판독기 = 그 런 `kit_<시각>/` 사본의 `read_history.py` · `history_params.json` 이 봉인 값 (`ul_reader.GRAMMAR_READER` = 이 `history_test/SHA256SUMS` 의 그 두 줄 ·
  selftest R36 이 실제 파일과 대조) 이고 그 런 kit `SHA256SUMS` 에도 같은 값일 때만 `python3 -I <kit>/read_history.py <런> --grammar --params … --out <임시>` 로 다시 읽고
  (런 폴더에 쓰지 않는다) 검사 19 = 판정 JSON (둘 다 참) · status PASS · rc 0 이어야 통과.  판독기가 봉인 값이 아니면 실행하지 않고 거부한다 · 러너 (`run_history.sh`) sha256 은
  여전히 대조하지 않는다.  ⇒ 판정 JSON 만 반입해서 실제 실행 PASS 를 인증하지 않는다 (GA 화면 ERROR · GB mesh · GB 화면 · GB 상태 파일을 판정 뒤에 고친 런 = 거부 ·
  R36 · M25).  ⚠ 실행 2 는 판독기 · 표 sha256 이 이 봉인 값인 판으로 돌린다 — `b1121b6b6` 이후 판 (그 뒤 `read_history.py` · `history_params.json` 바이트 그대로) ·
  그 앞 판 (`039abb141` 등) 의 판독기로 낸 런은 승인된 판독기 재판독이 서지 않아 거부된다 (덱은 같다 — 다시 돌리면 된다) · 다시 읽기는 런 폴더 원래 자리에서
  (GA · GB 입력 기록 `ckpt.txt` · `vars.txt` 가 절대 경로 — 옮긴 사본은 입력 대조가 거짓).  런 폴더 · `kit_<시각>/` 은 지우지 않는다.
- 봉인 `history_test/SHA256SUMS` sha256 `debe83877657978cdaf87b18e08edda501e520979dd40876f5e100c24e902163` (H0–H5 덱 여덟 · 판 STL = 바이트 그대로 ·
  더해진 것 = 문법 덱 · 표 `grammar_probe` · 생성기 ⑯ · 읽는 쪽 `--grammar` · 러너 `--grammar-only` · 래퍼 둘째 인자 `grammar`).
  → `039abb141` (문법 덱 입력 셋 · 검사 ⑰) sha256 `dba635721503dd614d92cd6b9b184c028030335163e360b9991b340b25fde027` →
  10-14 밤 (러너 Q4 나 · 읽는 쪽 모의 S38–S40 — **덱 아홉 · 판 STL · 표 · 생성기 = 바이트 그대로**) sha256 `8ff722d24096c6bd929682842e3b93907951ad29943f180709c914404cdb928d`.
  실행 2 는 어느 판으로 돌려도 같은 덱 (문법 · 생산자 · 판 STL sha256 = 위 사전 점검 봉인 값) 이다.

```bash
# ① 이 커밋의 새 작업 트리 (커밋마다 새 폴더 · 이미 있으면 다시 체크아웃하지 않는다)
cd ~/Yonghoon-DEM-DFT && git fetch -q origin claude/stoic-knuth-NObVQ && W=$HOME/unload_src_$(git rev-parse --short FETCH_HEAD) && { [ -d "$W" ] || git worktree add -q --detach "$W" FETCH_HEAD; } && cd "$W" && git log --oneline -1
H=$W/docs/data/ps45_unload_20261009/history_test
conda activate myenv && python3 -I $H/make_history_decks.py --check && python3 -I $H/read_history.py --selftest | tail -1   # "✓ check: 덱 9 …" · "selftest: PASS (0 실패)"
# ② 작업 폴더 · 제출 전 사전 점검 (로그인 노드 · 런 없음 · 같은 LMP 확인)
R=$HOME/ps45_unload_hist_20261013 && mkdir -p $R/logs
bash $H/run_history_ibb.sbatch $H grammar                      # 끝 줄 "✓ 사전 점검만 — 통과" 를 본 뒤 ③
# ③ 제출 (작업 폴더에서 — logs/ 는 제출 폴더 기준) · 다른 job 은 끄지 않는다
cd $R && J=$(sbatch --parsable $H/run_history_ibb.sbatch $H grammar) && echo "job $J"
# ④ 진행 · 끝 (수 분)
squeue -u $USER
tail -5 $(ls -t $R/logs/ulHist_*.out | head -1)
cat $(ls -dt $R/gram_*/ | head -1)grammar_verdict.txt
sha256sum $(ls -t $R/gram_*.report.tgz | head -1)
```

**보낼 것**: `gram_<시각>.report.tgz` (단계마다 화면 · 로그 · 덤프 · 작은 restart · 상태 파일 · 판정 JSON · kit SHA256SUMS) + sha256 + `logs/ulHist_<job>.out`.
WSL 로 가져오는 꼴 (접속 정보는 자리표시): `scp -P <port> <user>@<ibb-host>:~/ps45_unload_hist_20261013/gram_<시각>.report.tgz ~/` · rc 0 = 전부 기대대로 · rc 2 = 화면 `GRAMMAR_VERDICT …` 의 ✗ 줄 · 사유.

## 2. 덱 (K2 · `make_unload_decks.py`) — 결과 0 건 · 실행은 Codex GO 뒤

| 종류 | 무엇 | 런 |
|---|---|---|
| `R` | 복원 시험 (S0 · REG §3-2 · §12-1): PRE_SETUP `write_dump` (바닥 primitive 이력 그대로) → `run 0` (G1 setup 줄 · G2 원 형식 atom · G2c 원 형식 쌍 26 열 · 판 mesh md5 · mesh 벽 이력 · 총힘) → `run 2000` (G3) → R_END 관측 → 보조 소거 (uncompute → unfix 두 벽 → `un_diag.bin`) | RJ · RJ2 |
| `UNread` | 보조 소거 진단 restart 를 새 프로세스로 · 같은 머리 · PRE · POST (진단 전용 — S0 복원 증명 아님) | RJ · RJ2 |
| `UK` | 회전 KE 기준 — S0 무이동 3 창 (choice C4) | RJ · RJ2 |
| `UC` | 무이동 50,000 step × dt₀/dt (판 압력 표류 · 잡음 · KE) | UC |
| `U_UB` · `U_UVa` · `U_UVb` · `U_UT3` | 언로딩 상태 기계 · 전체 멈춤 규칙 (튜플 t1 · t2 · t4 · t3) | 팔 잡 · UTc (U_UT3) |
| `UT` (7:3) | dt₀/2 · 첫 교차 + 확인 두 단 → R_M restart + 상태 → 멈춤 (`RM_STOP` · §13-5 ③) | UT |
| `Ut0` (7:3) | 문법 (판정 자료 아님) — 표 `ut0` (창 100 step · A 400 · B 100 · P_meas 1 덱 MPa · 분리 문턱 크게) → 머리 · k = 0 · A 한 단 · 교차 · 확인 두 단 · R_M · 분리 · 분리 뒤 · 끝을 한 번씩 | RJ (7:3 첫 단계) |
| `G_<팔>` | 중력 팔 — 그 팔의 R_M (restart + 상태) → `run 0` (G1 · G2 · G2c) → `fix gravi … 9.81e-06` 제자리 교체 → 유지 (4–12 창) → 정상 · P̄ > P_meas 면 B 단 교차 · 아니면 `NO_BRACKET` (재압축 없음) → 분리 → 분리 뒤 4 창 | G_ 잡 |
| `EXT` · `EXT2` (10:0) | 3,600,000 → `run 60000` (restart 50,000 = 3,650,000 · 끝 3,660,000 명시 `write_restart`) · 3,660,000 → `run 50000` (3,700,000 · 끝 3,710,000 명시) · 원 덱 출력 꼴 | EXT |

- **모델 머리** = r8 원 덱 글자 (리포 tgz sha256 `097658aa…` · 재료 m1–m9 · pair · 바닥 · 판 · 중력 9.81 · 감쇠 1.0e-5 · `fix_modify zwall_top energy yes` · fix 순서 = 원 PHASE 4) — 판 STL 경로만 `${plate_stl}` (메시 자료는 restart 에서).  G0 = 원 r8 (0:10 · 3:7 · 5:5 · 7:3 꼴) · r2 (10:0 꼴) 와 비교해 PASS (GD5 · ibb 에서는 러너가 그 침대의 진짜 원 마지막 조각 덱으로 다시 — `<루트>/<침대>/RJ/g0.json`).
- **숫자는 표에서만** — 덱의 숫자 낱말은 표 · r8 원 글자 · 구조 상수 (0 · 1 · 2 · 3 · 4 · −1 · 0.0025 · 1000000 …) 중 하나여야 한다 (GD4 표 밖 상수 lint).
- **물리 창** (§13-4 · 생성된 덱에서 다시 계산 = GD6 · 판독기 R9):

  | 팔 | dt | v (덱 m/s) | 창 W | Δz_A · Δz_B (step) | k = 0 | 단 유지 | ave/time | thermo |
  |---|---|---|---|---|---|---|---|---|
  | UB | 1e-6 | 0.01 | 5,000 | 20,000 · 5,000 | 3–12 창 | 4–12 창 | 100 × 50 | 500 |
  | UVa | 1e-6 | 0.005 | 5,000 | 40,000 · 10,000 | 3–24 | 8–24 | 100 × 50 | 500 |
  | UVb | 5e-7 | 0.005 | 10,000 | 80,000 · 20,000 | 3–24 | 8–24 | 200 × 50 | 1,000 |
  | UT · UT3 | 5e-7 | 0.01 | 10,000 | 40,000 · 10,000 | 3–12 | 4–12 | 200 × 50 | 1,000 |
  | UC | 1e-6 | 0 | 5,000 | — | 50,000 step = 10 창 | | 100 × 50 | 500 |

  창 물리 시간 = 0.005 덱 s (모든 팔) · 분리 선언 2 창 · 분리 뒤 4 창 · 중력 팔 = **중력 교체 뒤 첫 재평형 유지만** 4–12 창 (× 2 없음) · 그 뒤 B 단 = 부모 팔 튜플 그대로
  (G_UVa · G_UVb 8–24 창 · 개정 3 §14-5 · Q4 · 생성기 GD16 이 덱별 표로 확인).
- **상태 기계** (단계 `ul_phase`: 4 HOLD0 · 0 SEARCH · 1 CONFIRM · 2 SEPARATE · 3 POST): 창 (`run W`) 마다 Ps · KE (ave/time 창 평균) · 기하 판 접촉 수 · 원자 · 새어 나감 → S1 (|ΔP̄| ≤ max(0.5 % · |P̄|, 0.05 P_meas)) ∧ S2 (KE ≤ 10 · KE_base) → 두 창 연속 + 최소 창 = 정상 · 최대 = UNSTEADY (k = 0 이면 TECH) → 단 끝 = P̄ (마지막 두 창 평균) · 교차 (P̄ ≤ P_meas) · B 전환 (P̄ ≤ 3 P_meas 다음 단부터) · 확인 두 단 → R_M (`restart_RM_*` + `state_RM_*`) → 분리 (기하 접촉 0 두 창 · 둘째 창 끝 선언 · **선언은 유지 예산 안**) → 분리 뒤 4 창 (**예산 밖 별도 관측** · 재접촉 = SEPARATE 로 되돌림 · **같은 높이 · 남은 예산에서 다시 — k + 1 로 옮기지 않는다** · 예산 끝 = `SEP_INCOMPLETE`) → 끝 (개정 3 §14-7 · Q6 · 생성기 모의기 GD15).  들어 올림 상한 16 µm (choice C11) · 가드 (원자 잃음 > 50 · 새어 나감 > 100 · 병진 KE > 1.7e-3 J) = restart + 요약 · 멈춤.
- **덱 언어 규칙** (selftest 가 지킨다): 상태 파일은 늘 **맨 바깥** `include ${ul_state}` (3d5c00f input.cpp 845 — if 안 include = ERROR · 처음이면 러너가 빈 파일) · run 뒤 읽는 값은 다음 줄에서 즉시 치환으로 얼린다 (⑭b) · `write_restart` 뒤 `ke` · compute 를 run 전에 읽지 않는다 · `run 0` 뒤 판 힘을 읽지 않는다 (⑭a) · if 조건은 숫자 · 비교뿐 · local compute 는 read_restart 뒤 첫 run 전에 정의 (compute_pair_gran_local.cpp 126) · 창 끝 덤프 = `dump_modify … every v_ul_dnext` (이동 중 없음 · setup 덤프 없음).
- **기록 머리** = 표 `records` (창 19 열 · 단 15 열 · 사건 6 열) · thermo 머리 = `Step Atoms KinEng ul_erot ul_Ps pressMPa CPU` (GD13 · LIGGGHTS c_ · v_ 열 이름 = ID 앞 8 글자).
- **벽 local 열** = id (mesh · 삼각형 · 입자) → force_normal (입자가 받는 법선력 3) → (R 만) history 4 (compute_pair_gran_local.cpp add_wall_2 순서 — 키워드 순서와 무관).  법선력 = (f·n̂) n̂ = n̂ 부호와 무관한 입자에 걸린 힘의 법선 성분 → 판이 누르면 fn_z < 0 (표 `plate_fn_compressive_sign` −1 · 이력 시험 SYN ⓓ 가 잰다).

## 3. 러너 · ibb 명령 (⛔ 1저자 비준 → Codex 키트 재검토 GO 뒤 · 꺾쇠 자리표시 = 접속 정보 · 고를 잡뿐)

- `run_unload.sh <침대> <잡>` 이 지키는 것: kit 사본 (SHA256SUMS 목록 그대로) · LMP sha256 = 표 (`ALLOW_OTHER_LMP=1` = 이탈 기록) · in/ 원 파일 sha256 = 표 ·
  **문법 fixture 사전 점검** (`RJ` · `RJ2` · `EXT` — `GRAMMAR_VERDICT` 의 PASS 판정 · 덱 출처 · 같은 LMP · `ul_reader.py grammar` · 아니면 LIGGGHTS 전에 멈춤 · §1-6 · Q5) ·
  **관문** (`ul_reader.py gate` — 거부면 런 없음) ·
  `"$MPIRUN" $MPIRUN_FLAGS -np "$NP" "$LMP"` (기본 `--oversubscribe --bind-to none` · NP 6) · 화면의 `Loop time … on N procs` 의 N = NP · `ERROR` · `UL_ABORT` 없음 · 런 뒤 읽는 쪽 · 보고 묶음 + sha256.
- 순서 (REG §13-5 ② · §13-6): 침대마다 원 파일 → `RJ` (복원 판정 RESTORED 여야 다음) → **7:3** `UB` · `UT` · `UC` (따로따로 제출 · 서로 독립) → 선택 판독 → 관문이 허락하는 **UV 하나** (`UVa` 또는 `UVb`) → 선택 (튜플) → (t3 면) `UTc` → `G_<최종 팔>` →
  **나머지 넷** = `RJ` → 최종 튜플의 팔 하나 → `G_<그 팔>` · **10:0** = `RJ` (3,600,000) → `EXT` (→ S0′) → `RJ2` (S0′) → 최종 팔 → `G_`.
- 이어 돌림 (기계 실패 · 한 번 · 개정 3 §14-4): `RESUME=1` — **일반 팔 (UB · UT · UVa · UVb · UT3) 만** · 같은 승인 팔 (첫 시도 기록 `gate=ALLOW` · `resume=0` · 덱 요약 없음) ·
  마지막 `restart_unload_<step>.bin` + 짝 `state_unload_<step>.in` 에서 같은 덱 (화면 `screen_a2.txt` · 첫 시도 화면 · 기록 그대로 · 잡 기록 `resume_from=<step>`) · 두 번째 = 거부 ·
  **`UC=fresh-attempt-only`** (UC 덱은 단 끝 restart 를 쓰지 않는다 — RESUME 은 앞에서 거부 · Q6) · **UTc · G_* · RJ · RJ2 · EXT = RESUME 거부**
  (다시 = 지금 폴더를 이름 바꿔 보존 (예 `UTc.try1`) → RESUME 없이 새 제출 · 관문 다시).
  **새 폴더 = 새 시도** — 등록된 재시도 한도 (REG §13-1 잡 실패 두 번 → EXECUTION_FAILED · §4 재시도 한도) · 결과 선택 (먼저 나온 유효 결과) 을 **초기화하지 않는다** ·
  러너가 보존된 앞 시도 폴더 (`<잡>.<꼬리>`) 를 새 잡 기록 `prior_attempts=` 에 남긴다 (판단 = 1저자 · 기술 실패 · 승인 이력 유지).
- 판독기 행 교체 (ULKRR-02): 끊긴 시도가 남긴 기록 줄은 **승인된 이어 돌림 경계** (RESUME 사건 + 위 `resume_from` + 그 상태 파일의 `ul_k`) 에서만 버린다 —
  그 밖 중복 · 역행 (step · k · w) = 버리지 않고 주 값 미식별 (사유).
  **경계 하나에 승인 한 번** (ULKRF-01 · 10-15): `resume_from` 의 step 마다 RESUME 사건 정확히 한 줄 — 같은 경계의 RESUME 둘 이상 (같은 k = 중복 · 다른 k = 상충) ·
  사건 k ↔ 상태 파일 불일치 · `resume_from` 밖 step 의 RESUME = 승인 없음 + 사유 (주 값 미식별 · 다음 관문 거부) · 사건 되감기도 같은 규칙.
  **새 시도 시작** (ULKRF-02 · 10-15) = 승인 경계 뒤 먼저 오는 쪽 — step 역행 (창 · 단 CSV) 또는 단 CSV 에서 k 가 k_r + 1 로 되돌아옴 (새 시도의 유지 창이 늘어
  옛 단 끝보다 늦게 끝나도 · 덱은 단 줄 → 사건 → restart · 상태 파일 순서로 쓴다) · 승인 없는 되돌아옴 · 중복 = 그대로 미식별.
- **재개 식별자 정수 확인 (10-24 · R39)**: RESUME 사건의 k/step과 상태 파일의 ul_k/ul_rstep은 원문이 정확한 비음수 정수값인지 확인한다. `3.49`나 `3.0000000000000001`을 3으로 반올림하지 않는다.
  ASCII decimal/scientific 정수값 (`3`, `3.0`, `3e0`, `+3`)과 바깥 ASCII 공백은 허용한다. 실제 소수·비유한·넘침·Unicode 숫자/비ASCII 공백·underscore는 경계로 승인하지 않는다.
  기존 유한 수 범위 검사와 토큰 4096자 비용 한도 뒤 Decimal로 정수성을 확인하여 큰 지수를 거대 int로 확장하지 않는다. 같은 상태 식별자의 중복 정의, 정상 사건과 비정수 RESUME의 공존,
  잘못된 `resume_from=` 표지를 정상 승인 근거에서 조용히 빼지 않는다. 러너 표지는 생성 형식인 ASCII 십진 숫자만 허용한다. 이 한정은 재개 승인 식별자에만 적용하며 공용 관측 CSV 파서와 물리 기준은 그대로다.
- **재개 표지 인식 경계 (10-24 · R40 · ULPRI-01/02)**: `RESUME `·NBSP 등 RESUME의 앞뒤 whitespace 변형은 정상 표지로 고치지 않고 오류로 남긴다. 공용 CSV의 `splitlines()`가 앞의 Unicode 구분자를 지우기 전에 원 event 셀을 검사한다. 정상 RESUME와 함께 있어도 승인 경계와 옛 행 제외는 0이다. 임의의 다른 사건명 전체를 금지하는 규칙은 추가하지 않았다.
  manifest는 키를 골라 읽기 전에 VT(U+000B)·FF(U+000C)·FS/GS/RS(U+001C–001E)·NEL(U+0085)·LS(U+2028)·PS(U+2029)를 거부한다. 다른 글 뒤 숨은 `resume_from=`도 무관한 줄로 버리지 않는다. LF·CRLF·CR은 유지한다. 이 여덟 구분자를 정상 LF로 바꿔 수용하지 않는다.
  R39의 정수성 보장과 R40의 표지/줄 구분 보장은 서로 다른 검사다. 예를 들어 정확한 0인 `0e1000000000`은 수용되지만 비정수 `3e-1000000000`은 거부된다. 모든 큰 지수 표기를 무조건 거부한다는 뜻이 아니다. 실제 arm CLI의 미식별/null·rank 불가와 원 CSV 불변을 확인한 합성 증거이며 실물 재개 자격은 아니다.
- **새 단 줄 전에 끊긴 재개 (ULPR-01)**: 승인된 경계의 창·단 CSV와 RESUME 앞뒤 사건을 함께 대조한다. 옛 시도의 완료 단을 새 시도의 정상 관측으로 쓰지 않는다.
  CSV에 시도 표지가 없으므로 동일 시각·창 수만으로 소속을 확정하지 않는다. 필요한 관측의 소속이 불명확하면 사유를 남겨 미식별로 처리한다. 원 CSV를 고치거나 삭제하지 않는다.
  경계 앞에서 교차와 확인 두 단까지 끝난 유효 주 값은 보존하되, 불명확한 꼬리를 제외한 범위만 분석한다(`resume_tail`에 경계·제외 행 수·사유). 전체 궤적의 union·비단조·최종 분리·표면 관측은 미확인이다.
  `rank_eligible`만으로 순위가 인증되지는 않는다. 쌍 비교는 유효한 union까지 요구하므로 해당 쌍은 UNIDENTIFIED로 남는다. RESUME 소수 k 반올림은 10-23 ULPR 보완 당시 남긴 한계이며, 10-24 R39의 정확한 정수 파싱 교정은 위 외부 재검토에서 수용됐다. ULPRI-01/02 표지 무결성의 새 외부 재확인은 별도다.
- **G2/G2c (ULPR-03·04)**: G2 원자 비교는 전체 관측 검증 뒤 원 토큰을 비교한다. 수치가 같아도 다른 원 토큰을 같다고 정규화하지 않는다.
  복원과 중력 복원에서는 요청한 S0/R_M 시점에 결합한다. G2c 필수 열 결손은 비교 미계산이며 복원 UNCONFIRMED다. 구조 파손·다른 시점 및 완전한 관측의 값 불일치는 VALUE_MISMATCH, 기술 실패는 SYNTAX_FAIL을 유지한다.
  완료되어 바뀌지 않는 직교 덤프를 대상으로 한다. BOX의 유한·순서·구조를 확인하지만 박스 수치나 경계 표지를 특정 물리 조건으로 고정하지 않는다.
- 잡 기록 (`run_manifest.txt` · 덧붙이기만 · 개정 3 §14-10): `gate=ALLOW` (+ `gate_why=`) · (RJ · RJ2 · EXT) `grammar_prereq=PASS` · `grammar_verdict=` · `grammar_verdict_sha256=` ·
  단계마다 `stage=<덱 종류> screen=… rc=… check=PASS|…` · `stage=G0 rc=…` · 판독기 `reader_<명령>_rc=` (0 = 정상 판독 · 미식별도 JSON 으로 0 · ≠ 0 = 프로그램 오류 → 러너 rc ≠ 0) ·
  끝 줄 `end=… fails=… reader_rc=…`.  **G0 · Ut0 기술 실패 = R · UN · UK 를 돌리지 않는다** (복원 판정 RESTORED 아님 · kebase 건너뜀 기록).
- 다음 제출 관문이 읽는 **잡 완료 영수증** (ULKRR-03): 끝 줄의 `fails=0` **과** `reader_rc=0` — 둘 다 한 번씩 있고 · 정수 · 0 (누락 · 비정수 · 비영 = 거부) ·
  판독기가 증서 · 기준 파일을 쓴 뒤 실패한 RJ · RJ2 · EXT 잡 (예: 출력 실패 rc 120) 의 증서는 다음 제출 승인으로 쓰지 않는다 (새 시도) · RESTORED 는 그 잡 기록의 `grammar_prereq=PASS` 도 ·
  `RJ2` = S0′ 결정 PASS + 그 `EXT` 잡 영수증.
  **범위 (Q2 (가) · 1저자 10-15 · Codex 수정 재확인 Q2 권고 문구 그대로)**: *복원 / EXT 증서는 성공 완료 영수증이 필수이며, 일반 팔의 주 관측은 원 폴더에서 재판독한다.
  재판독 가능성이 잡의 기술 성공을 뜻하지는 않는다.*  (지금 동작 그대로 — 일반 팔 (UB · UT · UC · UV · UT3 · UTc · G_) 관문은 영수증 대신 런 폴더를 다시 판독한다 ·
  유효 주 값은 보존 (등록 허용) · "기술 실패 잡의 산출물은 어떤 승인에도 다시 쓰이지 않는다" 는 전칭 보증이 아니다 · 등록 §14-11.)
- `EXT` (Q4 다): 첫 `s0p` 판독 rc **2** (등록된 연장 요청) + 끝 체크포인트일 때만 `EXT2` · 그 밖 비영 rc (판독기 프로그램 오류) = EXT2 없이 멈춤 · 판독기 rc 보존.
  ⚠ rc 2 = **PASS 아닌 모든 s0p 판정** (조건 미달 FAIL · 조건 미계산 (로그 · 창 밖) · S0′ 체크포인트 없음 포함) — 물리 조건을 유효하게 재서 실패한 경우만이 아니다
  (예상 못 한 rc 1 과 rc 2 를 구분해 멈추는 것까지가 이 규칙이다 · Codex 수정 재확인 10-15 §6 · 등록 §14-11).
- UTc (개정 3 §14-3): UT 의 기록 · 덤프 · thermo 를 **복사하지 않는다** — `parent_UT.sha256` (UT 판독 대상 sha256 목록) + `run_manifest` 의 `continues=UT` · `parent_dir` · `rm_step` ·
  `parent_sums_sha256` · 판독기가 UT 폴더에서 읽으며 대조 (불일치 · 경계 step 중복 · 누락 = 이어 돌림 무효 → UTc 주 값 미식별 · 최종 t3 = UT 주 값 그대로 + 보조 `SEP_INCOMPLETE`).
- §1-6 문법 fixture 는 본 R (생산 침대) 전 PASS 여야 한다 (개정 3 §14-9) — ✅ **1저자 10-14 Q5 = 러너 사전 점검으로 강제** (`RJ` · `RJ2` · `EXT` · 위 첫 줄 ·
  R 뒤 `restore_verdict` 에 붙이지 않는다 — "본 R 전" 이어야 하므로).

```bash
# ① 이 커밋의 새 작업 트리 · 봉인 확인 (커밋마다 새 폴더)
cd ~/Yonghoon-DEM-DFT && git fetch -q origin claude/stoic-knuth-NObVQ && W=$HOME/unload_src_$(git rev-parse --short FETCH_HEAD) && { [ -d "$W" ] || git worktree add -q --detach "$W" FETCH_HEAD; } && cd "$W" && git log --oneline -1
K=$W/docs/data/ps45_unload_20261009
conda activate myenv && python3 -I $K/make_unload_decks.py --check && python3 -I $K/seal_kit.py --check
# ② 원 파일 여섯 (침대마다 한 번 · 표에서 만든 명령을 보고 붙여 넣는다 · cp -n = 있으면 덮지 않는다) → 대조
python3 -I $K/ul_reader.py copycmd ps_7_3_r45
U=$HOME/ps45_unload_20261009 && mkdir -p $U/logs && python3 -I $K/ul_reader.py inputs $U ps_7_3_r45
# ③ 7:3 복원 시험 (G0 → Ut0 → R → UN → UK · G0 · Ut0 실패 = 멈춤) — 이력 시험 판정 JSON 을 넘긴다 (없으면 복원 판정 UNCONFIRMED) ·
#    §1-6 문법 fixture 실행 2 의 PASS 판정을 넘긴다 (없음 · FAIL · 덱 · LMP 다름 = 사전 점검이 LIGGGHTS 전에 멈춘다 · Q5)
HV=$HOME/ps45_unload_hist_20261013/hist_20261014_094731/history_verdict.json        # 10-14 재실행 PASS 런 (§1-5) — 이름으로 고정 (ls -dt 로 고르지 않는다 · 10-13 TECH 런이 같은 폴더에 있다)
GV=$HOME/ps45_unload_hist_20261013/gram_<시각>/grammar_verdict.json                  # §1-6 실행 2 의 PASS 런 — 이름으로 고정 (실행 1 FAIL 런이 같은 폴더에 있다)
cd $U && GRAMMAR_VERDICT=$GV bash $K/run_unload_ibb.sbatch $K ps_7_3_r45 RJ               # 사전 점검만 (끝 줄 "통과" · "✓ 문법 fixture PASS" 줄)
cd $U && sbatch --export=ALL,HIST_VERDICT=$HV,GRAMMAR_VERDICT=$GV $K/run_unload_ibb.sbatch $K ps_7_3_r45 RJ
head -3 $U/ps_7_3_r45/RJ/restore_verdict.json
# ④ 7:3 개발 팔 — 한 줄에 하나씩 (서로 독립)
cd $U && sbatch $K/run_unload_ibb.sbatch $K ps_7_3_r45 UB
cd $U && sbatch $K/run_unload_ibb.sbatch $K ps_7_3_r45 UT
cd $U && sbatch $K/run_unload_ibb.sbatch $K ps_7_3_r45 UC
# ⑤ UB · UT 끝난 뒤 — 선택 판독 · 관문이 ALLOW 하는 UV 하나만 낸다
python3 -I $K/ul_reader.py select $U
python3 -I $K/ul_reader.py gate $U ps_7_3_r45 UVa
python3 -I $K/ul_reader.py gate $U ps_7_3_r45 UVb
cd $U && sbatch $K/run_unload_ibb.sbatch $K ps_7_3_r45 <UVa 또는 UVb — 위에서 ALLOW 한 것>
# ⑥ 튜플 (selection.json) → t3 면 UTc · 그다음 중력 팔 (관문이 고른 팔만 ALLOW)
python3 -I $K/ul_reader.py select $U
cd $U && sbatch $K/run_unload_ibb.sbatch $K ps_7_3_r45 <UTc — t3 일 때만>
cd $U && sbatch $K/run_unload_ibb.sbatch $K ps_7_3_r45 <G_UB · G_UVa · G_UVb · G_UT3 중 관문이 ALLOW 한 것>
# ⑦ 나머지 침대 (원 파일 · RJ 뒤 최종 팔 · G_) · 10:0 = RJ → EXT → RJ2 → 최종 팔 → G_ — RJ · RJ2 · EXT 는 늘 GRAMMAR_VERDICT 를 함께 (Q5)
cd $U && sbatch --export=ALL,HIST_VERDICT=$HV,GRAMMAR_VERDICT=$GV $K/run_unload_ibb.sbatch $K <침대> RJ
cd $U && sbatch --export=ALL,GRAMMAR_VERDICT=$GV $K/run_unload_ibb.sbatch $K ps_10_0_r45 EXT
cd $U && sbatch --export=ALL,HIST_VERDICT=$HV,GRAMMAR_VERDICT=$GV $K/run_unload_ibb.sbatch $K ps_10_0_r45 RJ2
# 이어 돌림 (기계 실패 한 번 · 일반 팔 UB · UT · UVa · UVb · UT3 만 — UC = fresh-attempt-only)
cd $U && sbatch --export=ALL,RESUME=1 $K/run_unload_ibb.sbatch $K <침대> <팔>
# 끝난 잡마다 보낼 것 (꺾쇠 = 접속 정보)
sha256sum $U/<침대>/<잡>.report.tgz
scp -P <port> <user>@<ibb-host>:~/ps45_unload_20261009/<침대>/<잡>.report.tgz ~/
```

- 보고 묶음 = 런 폴더에서 큰 덤프 (원자 · 쌍 · obs · G2 원자 / 쌍 · post) 와 restart 를 뺀 것 (기록 CSV · 요약 · 화면 · 로그 · 벽 · mesh 덤프 · 판정 JSON · manifest · run_check).  큰 파일은 ibb 에 둔다.
  ⚠ **경량 묶음 = 모든 관측을 다시 검증하는 원천이 아니다** (개정 3 §14-8 · `ULKR-12`) — S3 · ε · 표면 · 복원 G2 를 다시 계산하려면 ibb 의 원자료 (큰 덤프 · restart) 가 필요하다.
  판정에 쓴 결정 파일은 함께 넣는다: `EXT` 묶음 = `EXT2/` · `s0_decision.json` · `RJ` · `RJ2` 묶음 = `ul_base.in` · 7:3 묶음 = `selection.json` (러너 `bundle` · 모의 M19).
- 디스크 어림 (§13-3 Q4 (가) 매 창 끝): 창마다 원자 ≈ 35 MB + 쌍 ≈ 175 MB → 팔 하나 ≈ 150–200 창 ≈ 30–40 GB · 단 끝 restart 81 MB × 단 수 · 7:3 개발 팔 넷 + UTc · G ≈ 200 GB 안팎 (/lustre 남음 148 T · quota 없음 — 1 차 점검 ⓖ).

## 4. 읽는 쪽 (K4 · `ul_reader.py`) — 판정 규칙 (등록 §12 · §13 · 권고 기본값 = 부록 초안)

| 판정 | 규칙 |
|---|---|
| 창 접촉 상태 | 창 끝 벽 local 덤프: 접촉 ≥ 1 · 창 평균 P > 0 = CONTACT · ≥ 1 · P ≤ 0 = TENSION · 0 = ZERO · 덤프 없음 · 깨짐 · 머리 step ≠ 창 끝 = OBS_MISSING (0 으로 세지 않는다) |
| 분리 | 같은 단 (k) 안 연속 두 ZERO 창 (SEPARATE 단계 창) 의 둘째 창 끝 · 판 이동 (k 바뀜) = 연속 초기화 (덱과 같은 규칙) · 그 창부터 분리 뒤 창 · 재접촉 = 계수 · 분리 뒤 창 · 표면 관측 초기화 · OBS_MISSING = 연속을 끊는다 (§14-7) · 창 기록 = 같은 k 안 고유 · 연속 w (앞 + 1) + 창 끝 step 간격 = 그 팔 W (덱 사본 · 없으면 표) — 빈 구간 = 연속 끊김 (CSV 줄 인접 ≠ 물리 창 연속 · 예산 끝 선언 w 12 → 분리 뒤 w 15 는 그대로 DONE · Q4 가) |
| 이어 돌림 경계 | 기록 줄 교체 (끊긴 시도가 남긴 줄 버림) = 승인된 경계에서만 — RESUME 사건 (k_r · s_r) + 러너 `resume_from=s_r` + 상태 파일 `state_unload_<s_r>.in` 의 `ul_rstep` · `ul_k` 가 맞고 · 버릴 줄 = s_r 뒤 (k > k_r) · 버린 뒤 앞 줄 = (k_r, s_r) · 새 시도 첫 줄 = k_r + 1 · 그 밖 중복 · 역행 (step · k · w) = 버리지 않고 주 값 미식별 (ULKRR-02) · **경계 하나에 승인 한 번** — 같은 경계 RESUME 사건 중복 · 상충 (같은 step 다른 k) · 사건 ↔ 상태 파일 불일치 · `resume_from` 밖 RESUME = 승인 없음 + 사유 · 사건 되감기 같은 규칙 (ULKRF-01) · **새 시도 시작** = step 역행 또는 (단 CSV) k 가 k_r + 1 로 되돌아옴 — 먼저 오는 쪽 (새 시도가 옛 시도보다 늦게 끝나도 · ULKRF-02) |
| 끝점 유효 | 덱 정상 (S1 ∧ S2 두 창) ∧ S3 PASS (단 끝 원자 + 쌍 덤프 · K5) ∧ P̄ · 높이 유한 ∧ 판 접촉 (CONTACT · TENSION) ∧ (k*) NOISE_FLOOR 아님 (σ_P = k* 마지막 두 창 thermo 정규 줄 `ul_Ps` · ddof 1 · 최소 10) |
| 확인 두 단 | 실제로 이어지는 k* + 1 · k* + 2 (B · CONFIRM) 의 등록 정상 완료 = 덱 정상 · S3 PASS · 유한 · 순서 · 누락 없음 — **판 접촉 요구 없음** (분리 = 확인) · 아니면 주 값 UNIDENTIFIED · 선택 UNRESOLVED (§14-1 · Q1) |
| 교차 · 괄호 | P̄ − P_meas 부호 바뀜 (> ↔ ≤) · 첫 교차 = P 두 점 선형 보간 (점 추정) + 실제 괄호 [h_lo, h_hi] · A 단 교차 = A 괄호 그대로 · 비단조 = **k = 0 부터** 모든 교차 괄호의 외곽 구간 [최소, 최대] ⊇ 첫 교차 괄호 + 표지 (b 판정 없음 · 기록 단 비유한 = 미계산 · §14-2) |
| 관측 파싱 | 모든 경로에서 덤프 전부 읽힘 (머리 · 열 · 행 수 · 유한) · 머리 step = 요청 step · ID 고유 · S0 밖 ID 없음 · CSV 결손 · 단 k 불연속 = 주 값 미식별 · 버린 행을 정상 부분 관측으로 쓰지 않는다 (§14-10) · 필수 열 · 파서 문제를 먼저 (열 결손 = 사유 있는 미식별 · 미계산 — 예외 없음 · G2c 쌍 덤프 필수 26열 중 하나라도 결손 = NOT_COMPUTED + 사유 → 복원 UNCONFIRMED · ULPR-04 · 등록 §14-12) · ID = 유한 · 양의 정확한 정수 (S0 · 원자 · 복원 관측 · 쌍 참조 — 소수를 정수로 자르지 않는다 · ULKRR-04 · ID 열 정수 토큰은 float 를 거치지 않는다 — `9007199254740993` 거부 · Q4) |
| S3 무게 항 | 분모의 m g 의 g = 그 팔의 실제 중력 (중력 팔 G_* = g_aux 9.81e-6 · 그 밖 9.81 · §14-6 · Q5) |
| 상태 두 축 | `primary_status` OK · NOISE_FLOOR · LOWER_BOUND (교차 전 끝 + 정상 · 접촉 · 단조) · UNIDENTIFIED (사유) · NO_CROSSING · TECH · NO_BRACKET (중력 팔만) ↔ `trajectory_status` DONE · TIMEOUT (요약 없음) · LIFT_CAP · GUARD · TECH · RM_STOP · **SEP_INCOMPLETE** (재접촉 뒤 예산 끝 · 덱 DONE 인데 판독기 최종 분리 · 분리 뒤 4 창 · 선언 창 ≤ 예산 · SEPARATED · POST_DONE 사건이 맞지 않음 = 보조 미완료 · 주 ρ 무영향 · §14-7) |
| 보조 ε · W_proxy | ε_sphere,all = 1 − C_all / h (C_all = 검증한 S0 에서 봉인 · 프레임마다 다시 계산 없음) · 자리 S0 · 교차 끝점 둘 (S0 ID 전부 · 같은 반경 아니면 그 자리 NOT_COMPUTED) · M (ε_all 만) · ε_sphere,inside 따로 · W_proxy = k 0 → M 정착 단 사다리꼴 (끝 조각 P_meas) × 1e-6 J (비정상 · 비유한 = 미계산 · 판이 받은 일 아님) — 팔 판정 · 최종 보고 (§14-8 · Q7) |
| 7:3 t3 | 최종 = UT 주 값 (UT 폴더 판독) + UTc 보조 (분리 · 표면 · 합집합 — 이어 돌림 OK · UTc 가 다시 읽은 주 값 = UT 일 때만 · 아니면 보조 SEP_INCOMPLETE) (§14-3) |
| KE 기준 | UK = 정확히 S0 무이동 완전 세 창 (단계 기술 성공 · 요약 DONE · START = S0 · arm UK · k 0 · 단계 4 · w 1–3 · step = S0 + w · W0 · 판 h0 · 들어 올림 0 · 결손 줄 없음) 일 때만 `ul_base.in` · 아니면 미발행 (rc 2 → S2 쓰는 팔 관문 거부 · 계수 10 그대로 · §14-10) |
| 상쇄 | 교차 끝점 마지막 창 인장 합 ≥ 0.5 · P_meas · A (= 1.25 N 덱) → 표지 · 처분 = 진단값 (`rank_eligible` 거짓 · 10 쌍 표 미식별) — 접촉 상태 · 자격과 따로 |
| 선택 | 유효 ρ 둘 (UB · UT) → δ_dt → dt* → 그 dt* 의 UV 하나 → δ_v → 튜플 t1–t4 · 끝점 무효 · NaN · 결손 · 무교차 = SELECTION_UNRESOLVED (다음 팔 · 본 런 없음) · 경계 = ≤ (부동소수 1e-9 %p · choice C13) |
| 관문 | 복원 RESTORED + 그 RJ · RJ2 잡 완료 영수증 (끝 줄 `fails=0` · `reader_rc=0` 둘 다 · 정수 · ULKRR-03) + 그 잡 기록 `grammar_prereq=PASS` (Q5) · KE 기준 파일 있어야 · 7:3 UB · UT · UC → UV (선택이 정한 하나) → 최종 팔 · t3 = UTc (S0 에서 새 UT3 없음) · G_ = 최종 팔의 R_M · 나머지 넷 = 최종 튜플 팔만 · 10:0 = S0′ 결정 PASS + 그 EXT 잡 완료 영수증 뒤 · 범위 (Q2 (가)): 복원 / EXT 증서는 성공 완료 영수증이 필수이며, 일반 팔의 주 관측은 원 폴더에서 재판독한다 — 재판독 가능성이 잡의 기술 성공을 뜻하지는 않는다 |
| 문법 fixture 사전 점검 (Q5 · Q3) | `ul_reader.py grammar <판정> --lmp-sha <지금 바이너리>` — 판정 schema · status PASS · exit_code 정수 0 · 검사 19 전부 참 · run_dir = 판정 파일 폴더 · run_manifest `mode=gram` · `end` · LMP sha256 같음 · 단계 P · GA · GB rc 0 · deck.txt · 덱 둘 + 판 STL 사본 = 봉인 값 (`GRAMMAR_INPUTS` = `039abb141` 판) · 그 런의 kit `SHA256SUMS` (sha256 = run_manifest `sums_sha256`) 도 같은 값 · **원자료 재판독** (Q3 · 10-15) = 그 런 kit 사본 `read_history.py` · `history_params.json` = 봉인 값 (`GRAMMAR_READER`) 일 때만 그 판독기로 런 폴더를 다시 읽어 검사 19 = 판정 JSON · status PASS (판독기가 봉인 값 아니면 실행하지 않고 거부 · 화면 줄에 `reread=` · `reader_sha256=`) → rc 0 · 아니면 rc 2 (러너가 RJ · RJ2 · EXT 의 LIGGGHTS 전에 멈춘다) |
| 복원 판정 | reset 로그 다섯 (history_zwall_bot · top_mesh · n_neighs_mesh_top_mesh · tracker_top_mesh · contacthistory) · G0 · G1 · G2 · G2c · mesh md5 · G3 · 바닥 이력 PRE = POST · UN 소거 보임 · PRE · POST · R_END · UN 전부 읽힘 · 머리 step (S0 · S0 + 2,000) · 고유 ID · ID 집합 = S0 · R_END ↔ UN 같은 대상 · Ut0 (7:3) · R · UN 기술 성공 · 이력 시험 H0–H5 PASS · rc 0 · **SYN PASS + 측정 부호 = 표** · 총힘 시점 PASS (SYN 없음 = 자격 없음) → RESTORED · UNCONFIRMED (관측 결손) · SYNTAX_FAIL (기술 실패) · VALUE_MISMATCH (수치) · 다음 제출 관문 = RESTORED + 그 RJ 잡 완료 영수증 (fails=0 · reader_rc=0 · ULKRR-03) + 문법 fixture 사전 점검 PASS 기록 · 중력 팔 = R_M 의 run 0 setup 에서 G1 · G2 · G2c (출처 팔 R_M 창 끝 · G3 해당 없음 · C12 · 실패 = TECH) (§14-10) |
| 10 쌍 표 | 둘 다 OK · 순위 자격일 때만 합집합 괄호 비교 — 겹침 = 미구분 (동률 아님) · 분리 = 구분 · 아니면 미식별 |

## 5. 봉인 (K8 · `seal_kit.py`) — 활성 규칙 목록 · 폐기 규칙 부재

- `SHA256SUMS` = 러너가 ibb 로 복사하는 묶음 76 파일 (표 · 모듈 · 생성기 · 러너 · 래퍼 · 시험 · `active_rules.json` · 덱 64 · README · 이력 시험 폴더 제외).
- `active_rules.json` = 활성 규칙 24 (선택 · 제출 순서 · UT R_M 멈춤 · UTc · 비단조 합집합 · 확인 두 단 · 관측 파싱 · 이어 돌림 경계 · 분리 · 재접촉 · 예산 · 중력 팔 유지 · S3 팔 g · TIMEOUT · 상쇄 · 물리 창 · S3 · σ_P ·
  이어 돌림 한 번 · 단계 rc · 복원 완전성 · ε · W_proxy · 경량 묶음 범위 · KE 기준 UK 세 창 · 문법 fixture 사전 점검) — 규칙마다 코드 자리 (실재 확인) · 증인 시험.
  10-14 밤 +2 = `resume_boundary` (ULKRR-02) · `grammar_prereq` (Q5) · 바뀐 글 = `parse_complete` · `separation` · `resume_once` · `stage_rc` · `restore_complete`.
  10-15 (Codex 수정 재확인 반영 · 규칙 수 24 그대로) 바뀐 글 · 증인 = `resume_boundary` (ULKRF-01 · 02 · R33 · R34) · `parse_complete` (ULKRF-03 · Q4 · R35 · C4 · L14) ·
  `grammar_prereq` (Q3 원자료 재판독 · R36 · M25) · `restore_complete` (Q2 범위) · `stage_rc` (EXT rc 2 범위).
- 폐기 규칙 검사 (ULR1-05): 옛 띠 b (덱 · 러너 글자 · 파이썬 AST — selftest 안 부재 단언은 제외) · 동시 UV 제출 (러너 · 래퍼 · 이 README 의 `UB … UV` 를 도는 고리 · 한 줄 sbatch 둘) = **0 건** 이어야 `--check` rc 0.

## 6. 권고 기본값 (1저자 비준 대기) — 정본 = 부록 초안

`docs/reviews/dem_unloading_kit_section13_appendix_draft_20261013.md` (choice C1–C18 · 기본값 · 그 기본값을 고정한 fixture · 비준되면 등록 §13 덧붙임 · 결과 0 건).

## 9. 시험 먼저 기록 (고치기 전 실패 → 고친 뒤)

| 대상 | 고치기 전 (빈 구현 · 없는 파일) | 고친 뒤 |
|---|---|---|
| `history_test/make_history_decks.py --selftest` (덱 · 설계 · run 사이 읽기 · 러너 짝 · 검사기 자신) | 121 중 115 실패 (표 검사 6 만 통과) | 121 / 121 |
| `history_test/read_history.py --selftest` 판정 24 시나리오 (S1–S24) | 27 중 27 실패 | 27 / 27 |
| 같은 파일 러너 모의 (S25–S29 · 가짜 mpirun · lmp) | 8 중 8 실패 (덱 · SHA256SUMS 없음) | 8 / 8 |
| 판 접촉 법선력 부호 (생성기 ⑨ 1 · 읽는 쪽 S30–S32 3) | 4 중 4 실패 | 생성기 122 / 122 · 읽는 쪽 38 / 38 |
| `ul_s3.py --selftest` (K5 S3 총힘 — 중력 평형 사슬 · 쌍 전용 0.0400 · 불평형 · 단위 · 결손) | 14 중 13 실패 | 14 / 14 |
| `ul_observers.py --selftest` (K6 σ_P · 표면 · S4 · ε · W_proxy · KE 기준) | 16 중 16 실패 | 16 / 16 |
| 같은 파일 O4b (σ_P 기본 열 = 실제 thermo 머리 `ul_Ps` — `ULK-01`) | 1 실패 (기본 `v_Ps`) | 17 / 17 |
| `ul_gates.py --selftest` (K7 G0 · G1 · G2 · G2c · G3 · 판 z · S0′ · 복원 판정) | 34 중 34 실패 | 34 / 34 |
| `make_unload_decks.py --selftest` (K2 덱 64 · G0 · ⑭a · ⑭b · if · 표 밖 상수 · 물리 창 · 멈춤 규칙 · 기록 머리 · 러너 짝 · thermo 머리) | 284 중 282 실패 (빈 덱에서 공허한 음성 2) | 285 / 285 |
| 같은 파일 GD7 정정 + GD3b (if 안 include = 3d5c00f input.cpp 845 ERROR — 처음 쓴 시험이 금지된 꼴을 요구했다) | 고친 시험이 고치기 전 덱에서 2 실패 | 285 / 285 |
| `ul_reader.py --selftest` (K4 ULR1-01~05 종단 · S3 · NOISE_FLOOR · 관문 · 이어 돌림 · 10 쌍 · KE 기준 · S0′) | 33 중 33 실패 | 33 / 33 |
| 같은 파일 R14 (복원 판정 조립 4) · R15 (원 파일 복사 명령 1) | 2 실패 (부정 3 은 옛 구현에서도 참 — 판별 = R14 첫 줄) | 38 / 38 |
| 같은 파일 R16 (중력 팔 R_M 복원 G1 · G2 · G2c 2 — choice C12) | 2 실패 | 40 / 40 |
| `ul_runner_test.py --selftest` (K3 러너 모의 · 가짜 mpirun · lmp · 임시 키트 다시 봉인) | 12 중 12 실패 (러너 · 봉인 없음) | 12 / 12 |
| `seal_kit.py --selftest` (K8 봉인 · 활성 규칙 · 폐기 규칙 판별력) | 10 중 10 실패 | 10 / 10 |
| `history_test/make_history_decks.py --selftest` ⑮ (함께 사는 pair/gran/local ≤ 1 · wall/gran/local ≤ 1 · 첫 ibb 실행 TECH — §1-5 · `ULK-02`) | 131 중 7 실패 (덱 일곱 · SYN 만 통과) | 139 / 139 |
| **10-14 Codex 키트 재검토 반영 (개정 3 · 계획 §5)** — `ul_reader.py --selftest` R14 · R17–R19 + `ul_gates.py` F2 (`ULKR-05` · `08` — 복원 완전성 · 이력 자격 SYN) | 57 중 15 실패 · 35 중 1 실패 | 57 / 57 · 35 / 35 |
| `ul_runner_test.py --selftest` 러너 모의 (`ULKR-06` · `11` — RESUME 정책 · 같은 승인 팔 · 단계 rc · 판독기 rc · G0 · Ut0 실패 = R 없음) | 21 중 11 실패 | 21 / 21 |
| `ul_reader.py --selftest` R20–R22 (`ULKR-01` · `02` · `04` — 확인 두 단 · k = 0 합집합 · 관측 파싱) | 74 중 13 실패 | 74 / 74 |
| `ul_reader.py` R23 + `ul_runner_test.py` M9 (`ULKR-03` — UTc 부모 해시 · t3 보고) | 83 중 8 실패 · 23 중 2 실패 | 83 / 83 · 23 / 23 |
| `make_unload_decks.py --selftest` GD15 · GD16 (`ULKR-07` 덱 · `ULKR-10` A — 덱 제어문 모의기) | 291 중 3 실패 | 291 / 291 |
| `ul_reader.py` R24 · R25 · R26 + `ul_runner_test.py` M18 (`ULKR-07` 판독기 · `ULKR-09` UK · `ULKR-10` B 팔 g) | 106 중 21 실패 · 24 중 1 실패 | 106 / 106 · 24 / 24 |
| `ul_observers.py` O11–O12 · `ul_reader.py` R27 · `ul_runner_test.py` M19 (`ULKR-12` — ε 봉인 · W_proxy 보고 · 묶음) | 21 중 5 실패 · 111 중 5 실패 · 25 중 1 실패 | 21 / 21 · 111 / 111 · 25 / 25 |
| `history_test/make_history_decks.py --selftest` ⑯ 문법 fixture (Q8 · §1-6 — 덱 꼴 · 모의기 GA → GB · 모의기 판별력) | 149 중 10 실패 (⑯ 전부 · 덱 없음) | 156 / 156 (+ 아홉째 덱 일반 검사 7) |
| `history_test/read_history.py --selftest` S33–S37 (문법 판정 · 반례 아홉 · GB 없음 · GA 없음 · 러너 모의 `--grammar-only` 셋) | 53 중 15 실패 (새 시험 전부) | 53 / 53 |
| **10-14 밤 Codex 재확인 반영 (계획 dem_unloading_kit_reverify_fix_plan_20261014.md · 시험 먼저 `b1121b6b6` → 수정 `e271bdd48`)** — `ul_reader.py --selftest` R28 (`ULKRR-02` 이어 돌림 경계 · 양성 대조 진짜 RESUME) · R29 (`ULKRR-03` 영수증 · 실제 CLI stdout 닫힘 rc 120 · RJ2) · R30 (`ULKRR-04` 소수 ID · 열 결손) · R31 (Q4 가 창 연속) · R32 (Q5 문법 사전 점검 19 반례 · 봉인 값) | 158 중 44 실패 | 158 / 158 |
| 같은 묶음 `ul_lib.py` L13 · `ul_s3.py` F12 · `ul_gates.py` C3 (`ULKRR-04` 정확한 양의 정수 ID · 쌍 참조) | 21 중 2 · 16 중 2 · 37 중 1 실패 | 21 / 21 · 16 / 16 · 37 / 37 |
| 같은 묶음 `history_test/read_history.py --selftest` S38–S40 (Q4 나 — 파일을 다 쓴 뒤 실패한 GA · P 에서 이어 가지 않는다) | 56 중 3 실패 | 56 / 56 |
| 같은 묶음 `ul_runner_test.py --selftest` M20 (`ULKRR-03` 판독기가 증서 · 기준 파일을 쓴 뒤 rc 120) · M21 (Q4 다 EXT) · M22 (Q5 — 양성 = 지금 history_test 러너 · 읽는 쪽 판정 · 같은 가짜 바이너리) · M23 (`ULKRR-02` 러너 수준 RESUME) · M24 (Q6 UC) | 37 중 9 실패 | 37 / 37 |
| **10-15 Codex 수정 재확인 반영 (계획 dem_unloading_kit_fix_recheck_fix_plan_20261015.md · 등록 §14-11 · 로그 = docs/reviews/dem_unloading_kit_fix_recheck_fix_evidence_20261015/)** — `ul_reader.py --selftest` R33 (`ULKRF-01` 같은 RESUME 두 줄 · 묶음 둘 · 되감기 한 번 중복 · 같은 step 다른 k · 양성 · 한 줄 대조) · R34 (`ULKRF-02` 생성 UT 덱 제어 흐름 4 · 5 창 · 4 → 5 · 4 → 4 · 5 → 4 · 무승인) · R35 (`ULKRF-03` 복원 G2c 열 결손 넷 · 실제 restore CLI) · R36 (Q3 원자료 재판독 양성 · 변조 넷 · 승인 밖 판독기 셋 · 봉인 값) | 182 중 18 실패 | 182 / 182 |
| 같은 묶음 `ul_lib.py` L14 (Q4 정수 토큰 2^53 + 1 · 쌍 참조 · 긴 토큰) · `ul_gates.py` C4 (`ULKRF-03` G2c 열 결손 양쪽 · 두 열) · `ul_runner_test.py` M25 (Q3 판정 뒤 GA 화면 ERROR = 실제 러너가 LIGGGHTS 전 거부) | 24 중 2 · 41 중 4 · 38 중 1 실패 | 24 / 24 · 41 / 41 · 38 / 38 |
