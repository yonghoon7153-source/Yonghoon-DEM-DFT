# Codex 재검증 요청 (5차) — RGLR3-01 · 02 · 03 수정 + 194 실행 증거 · 인계 v1.2 다시 읽기 + 194 값 사용 가능성 (2026-10-06)

- 기준 판정: `docs/reviews/codex_review_rglr2_reverify_20261005.md` (핀 `11fcf91e8` · RGLR2-01 · 02 · 03 · RGL-06 · RGL-08 닫힘 · 새 P1 없음 · 새 P2 둘 `RGLR3-01` · `RGLR3-02` · P3 `RGLR3-03` · 194 인계 · 배포 HOLD · **전체 재실행 불요 — 인계 검사를 보강해 다시 읽기**).
- 이번에 한 것: 판정문 §8 최소 해제 목록 1–3 (코드) + 4–5 (증거).  194 배치는 **다시 돌리지 않았다** — 고친 로더로 인계표만 다시 만들고 (1저자 WSL) 다시 읽어 검산했다 (§2-4).
- 1저자 비준: *"비준이얌"* (10-05 밤 — A 재시도 봉인 · B τ 로더가 망 정지 계약의 사본 · 투영 · σ₀ 검사를 다시 부른다 · C 후속 명령 · D 배치 재실행 없이 인계만 다시 생성 + 증거 묶음).
- 1저자 추가 요청: *"이 값들이 사용가능한지에 대해서도 codex에 물어봤으면"* (10-05 밤) → **§6** · *"codex한테 물어보자"* (10-06 새벽 — Physics 모드 τ 를 배포에 넣을지) → **§6-5 QV3**.
- 검토 대상 = 이 요청서를 담은 커밋 (브랜치 `claude/sdcp-dem-manuscript-si-pqwtv8` · 1저자가 발송 때 sha 를 적는다).  봉인 19 파일은 `11fcf91e8` 와 바이트가 같다 (실행 등록 `docs/reviews/lhs_network_batch_registration_20261005.md` §7).

## 1. 패치 (오래된 순)

| 커밋 | 원장 | 내용 | 시험 |
|---|---|---|---|
| `0c48297f9` | RGLR3-01 · RGLR3-03 | 194 실행기 `scripts/run_network_194_parallel.py` — retry **시작 관문** = 워커 체크아웃의 HEAD · 봉인 19 파일 sha256 · dirty 를 발사 봉인과 대조, 다르면 rc 2 (아무것도 띄우지 않는다 · 넘김 `--allow-mixed-generation` · `--allow-dirty` 는 기록된다) · 시도마다 지문 (`worker.json` attempts[].seal = 시작 · 끝 지문 · git sha · dirty · 이 시도가 쓴 기록 sha256) · 케이스 판정 `case_seal` (SEALED · SEALED_DIRTY_ALLOWED · SEALED_LEGACY · UNSEALED · NO_RECORD — merge · audit · retry 공용 · UNSEALED 가 있으면 merge rc 2) · 읽기 전용 `audit --root R --tsv` · 후속 명령 = ⓪ 봉인 감사 · ① τ 진단 표 · ② 생성기 `--webapp-groups contact,percolation,f1,fracture,area,tau --tau-results <ROOT>/merged/<c>/results` · ③ 묶음 (인계 파일 · 봉인 감사) · ③b τ 원천 | selftest 28 → **51/51** (반례 22 먼저 — 옛 코드에서 22 실패) |
| `74ef3c8a7` | RGLR3-02 | τ 인계 로더 `scripts/lhs_design_dataset.py` `load_tau_results` — P0–P3 그대로 + **P4** = 배치가 done 을 준 **같은 함수** `pipeline_service.network_stop_verdict` 재호출 (사본 · 투영 · σ₀ · 띠) · `tau_flux.network_generation_problem` (활성 세대) · 읽기 안정 (`file_digest` 앞뒤).  하나라도 실패하면 인계 **전체** 거부 (FillRefusal — NOT_COMPUTED 로 싣지 않는다) · 출처 부록 새 열 `same_generation_checks` · `same_generation_basis = current_files_no_publish_hash` · 스키마 `lhs_tau_net/v2` · 웹앱 툴팁 같은 묶음 | selftest 312 → **326/326** (새 반례 15) · `webapp/test_network_handover_chain.py` 12 → **19/19** (④c = Codex 탐침 그대로) |
| `061ec1b58` | 기록 | 원장 RGLR3-01 · 02 · 03 claimed_fixed · 실행 등록 §7 덧붙임 (인계 = 고친 커밋에서 생성 · 봉인 19 파일 HEAD 에서 19/19 같음) · 194 값 미리보기 `docs/data/lhs_network194_11fcf91e8/overview_20261005/` | — |
| (이 커밋) | 증거 | 인계 v1.2 · 봉인 감사 · 다시 읽기 검산 · τ 원천 · WSL 기록 · τ < 1 점검 (`docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/`) · 4차 탐침 재실행 (`docs/reviews/codex_rglr3_fix_probe_rerun_20261006/`) · 원장 증거 줄 · 이 요청서 | — |

## 2. 판정문 §8 최소 해제 목록 대응

| §8 | 무엇을 했나 | 증거 (수정 전 → 수정 뒤) |
|---|---|---|
| 1 RGLR3-01 | 시작 관문 · 시도별 지문 · 케이스 판정 · 감사 부명령 (§1) | 4차 탐침 그대로 (같은 HEAD + 봉인 파일 dirty): retry **rc 0 · 워커 실행 · run_002 기록 → rc 2 · 워커 안 띄움 · run_002 없음** (사유 "세대: 코드가 발사 봉인과 다르다 (HEAD 가 같아도)" · "dirty: 추적 파일이 바뀐 트리") · 실제 194 = 봉인 감사 **SEALED_LEGACY 194 · merged = 케이스 폴더 194 같음** (`seal_audit.tsv` · rc 0).  SEALED_LEGACY = 옛 형식 (시도 지문 이전 실행기) 의 첫 run 유일 시도 · 깨끗한 사전 점검 · run_001 실행 중 코드 변화 0 · 워커 runs 1 건 (발사 sha · dirty false) — 이 배치는 retry 를 탄 적이 없다 |
| 2 RGLR3-02 | τ 로더 P4 (§1) | 4차 탐침 두 변조 (dual 만 띠 L0 → L1 · dual 만 σ₀ × 2) **수용 → 인계 전체 거부** (P4: 정지 계약 ⑥ 모드 파일 ↔ dual 사본 불일치) · 입력 · σ_ratio · run id 변조는 그대로 거부 (P2 · P3 · P1) · 정상 그대로 수용 · 실제 194 = 거부 없이 생성 (§2-4) |
| 3 RGLR3-03 | 후속 명령 (§1) | 탐침 재실행의 실행기 출력 (`docs/reviews/codex_rglr3_fix_probe_rerun_20261006/new_probes_after_fix.json` → `launcher.followups`) · 1저자 WSL 실행 = 같은 생성기 호출 (`--webapp-groups contact,percolation,f1,fracture,area,tau --tau-results "$R/merged/<c>/results"`) · 명령 · 출력 그대로 `docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/wsl_run_20261006.md` (묶음은 인계 파일 · 봉인 감사 · τ 원천만 — 배치 manifest · 실행 · 시도 기록은 이미 리포 `docs/data/lhs_network194_11fcf91e8/` 에 있다) |
| 4 실제 194 | 배치 증거 (`docs/data/lhs_network194_11fcf91e8/` — manifest · `docs/data/lhs_network194_11fcf91e8/runs/run_001.json` · progress · merge_report · status · metrics_flat · `cases/*/worker.json` 194 · log) + **인계 v1.2** + **봉인 감사** + **τ 원천** (`net194_tau_sources_20261006.tar.gz` · 케이스마다 dual · full_metrics · 망 도장) + **다시 읽기 검산** `reread_v12.py` (모두 `docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/`) | **PASS · 실패 0** (§2-4 표) |
| 5 WSL 소형 원 보고서 | `docs/data/lhs_network194_11fcf91e8/smoke_postfix/` — `smoke_report.json` · 요약 · 로그 · 음성 대조 · 케이스 기록 (원 tgz sha256 `0c77bc22…` · 작업 폴더 · 임시 파일만 제외) | 26/26 PASS · rc 0 (고친 코드 `11fcf91e8`) |

### 2-4 다시 읽기 검산 (인계 v1.2 · 1저자 WSL 10-06 02:11 KST 생성 · 검산 = 이 컨테이너)

| 검사 | LHS 130 | LHSx 64 |
|---|---|---|
| C1 행 = 배치 `metrics_flat` 집합 · 중복 | 130 · 0 | 64 · 0 |
| C2 LW 열 · 제외 노트 frame_unverified | 0 · 있음 | 0 · 있음 |
| C3 열 사전 ↔ 표 · 빈 뜻 | 251 = 251 · 0 | 253 = 253 · 0 |
| C4 옛 인계 (`docs/data/{lhs,lhsx}_handover_20261001.csv` = d1ec42fba 접촉 배치) 공통 열 값 (문자열 같음 · 부동소수 상대 1e-12) | 188 열 · **24,440 칸 같음** · 차이 0 | 190 열 · **12,160 칸 같음** · 차이 0 |
| C4 새 열 · 빠진 열 | 62 (⑤⑥⑦ 34 + 망 τ 묶음 28) · 0 | 62 · 0 |
| C5 τ 상태 Hertz · Physics | OK 106 · NP 24 · OK 106 · NP 24 | OK 64 · **OK 54 · MODEL_BELOW_CONTINUUM_BOUND 10** |
| C5 NOT_COMPUTED · BAND_FALLBACK | 0 · 0 | 0 · 0 |
| C5 값 (metrics_flat 에서 다시 계산 · 상대 1e-9 · tau = √tau2 · OK ⇒ ≥ 1 · MBCB ⇒ < 1 · 비관통 f = 0 · tau2 빈칸) | 어긋남 0 | 어긋남 0 |
| C5 비관통 집합 = 퍼콜 감사 `se_perc_webapp_dump` · 공통 메타 (σ₀ 3.0 mS/cm · 25 °C · mass_conserving · L_mc) | 같음 | 같음 |
| C6 출처 부록 = 표 집합 · run id = 배치 status · `tau_flux.py` sha256 = 발사 봉인 | 어긋남 0 | 어긋남 0 |
| C7 τ 원천 sha256 = 출처 부록 · `tau_flux.ion_columns` 독립 재계산 = 표 칸 (완전 일치) | 130 / 130 | 64 / 64 |
| C8 봉인 감사 | SEALED_LEGACY 194 · merged 같음 194 | (공통) |

- 생성기 출력 (WSL 기록 그대로): mono 30 · 16 행 = 설계에 없는 상 빈칸 (`N_A_PHASE_ABSENT`) · `tortuosity_dijkstra_SE` 보류 (LHS-08) · LW 명시 제외 · union 설계 밖 행 `perc` 1 개 (인계표에 안 넣음 · LHS).
- 인계표 · 열 사전 sha256 = `reread_20261006.json` `files`.

## 3. 4차 탐침 재실행 — 고친 트리 (`docs/reviews/codex_rglr3_fix_probe_rerun_20261006/`)

판정 묶음 (`docs/reviews/codex_rglr2_reverify_review_evidence_20261005/`) 을 복사하고 source/ 를 `061ec1b58` 의 같은 456 경로로 채워 묶음 실행기 그대로 (`drive_fix_probe.py` 한 번).  결함 단언 두 줄 (40 · 79 행) 만 뒤집은 사본 `new_probes_after_fix.py`.

| 사례 | 핀 `11fcf91e8` | 고친 트리 |
|---|---|---|
| τ 로더 dual 만 띠 L0 → L1 · dual 만 σ₀ × 2 | 수용 | **인계 전체 거부** (P4 ⑥) |
| τ 로더 atoms 변조 · σ_ratio × 4 · run id 불일치 · 정상 | 거부 · 거부 · 거부 · 수용 | 그대로 |
| retry 같은 HEAD dirty | rc 0 · 워커 실행 · run_002 | **rc 2 · 워커 없음 · run_002 없음** |
| merge (시도 사이 지금 트리만 바뀜) | rc 0 · `code_changed_since_launch` 기록 | 그대로 |
| 실행 등록 19 파일 · VM 유리수 5,000 | 19/19 · 경계 위반 0 | 그대로 |
| 독립 탐침 7 (network_adversarial · lw · vm · precision · raw18 · handover_replay · handover_before_after) | rc 0 | rc 0 |
| 원본 `new_probes.py` | rc 0 | rc 1 (40 행 = 결함이 없어졌다) |

## 4. 194 배치 실행 기록 (요약 · 숫자는 증거 폴더 README 그대로)

- WSL `~/dem-audit` (detached `11fcf91e8`) · 22:13–22:49 KST (wall 0.60 h) · 갈래 20 × 1 스레드 · 최대 동시 18 · 예산 대기 3,777 · backfill 96.
- **194/194 done** · 실패 0 · 실행 한 번 (`kind run`) · **retry 0** (RGLR3-01 의 우회 경로를 타지 않았다) · `code_changed_during_run []` · merge `code_changed_since_launch []` · `mixed_generation []` · `anomalies []`.
- 메모리 (§5 지적): 실측/추정 RSS 중앙 1.1 · 1.4 · **최대 2.1 · 2.55** (lhs · lhsx) — 추정식이 큰 침대를 낮게 잡는다.  OOM 없음 (WSL MemTotal 15.5 GB) — 그러나 동시 프로세스 트리 RSS 합은 기록하지 않았다 ⇒ "20 레인 메모리 안전" 을 독립 검증으로 쓰지 않는다 (판정문 §5 그대로).

## 5. WEB-03 · LHS-33 — 닫힘 명시 요청

두 항목은 3차 판정에서 **부분 닫힘 → 재개방**이었고, 남은 부분이 각각 RGLR2-02 · RGLR2-03 이었다.  4차 판정은 그 둘을 닫았지만 항목 자체의 닫힘은 따로 적지 않았다 (원장 = open).  닫힘 여부를 명시해 달라.

- **WEB-03** (관통 풀이 실패 채널 · 게시 원자성): 3차 = 실패 채널 게시 거부 (일반 · 정지) 닫힘 · 단일 쓰기 실패 복원 수용 · 남은 것 = 복원 자체 실패 표지 (RGLR2-02) → 4차 닫힘.  알려진 한계 (닫힘을 막는가, 한계 기록으로 충분한가): kill -9 · 정전 같은 비동기 중단의 원자성 (세대별 후보 디렉터리 + 단일 포인터 미구현) · 남은 `.publish_backup_*` 청소 없음 · 실패 기록 쓰기 자체가 실패하면 단계 로그에만 남음 (읽는 쪽은 디스크로 판정 — `network_generation_problem`).
- **LHS-33** (옛 σ_VM 열 거짓 0): 3차 = 결손 · NaN · 0/0 → None + 상태 · 소비자 연동 · 균일 VM CV 0 보존 수용 · 남은 것 = 음수 근호 clamp (RGLR2-03) → 4차 닫힘 (K = 2^20 수용).  **194 인계 v1.2 에 `stress` 로 시작하는 열은 0 개다** (`stress_cv` 계열 없음 · 10-01 판에도 없었다 · C4 빠진 열 0) — 옛 σ_VM 은 194 metrics (`merged/*/metrics_flat.csv`) 에만 있고 인계되지 않는다.

## 6. ★ 194 값 — 쓸 수 있는가 (1저자 요청)

### 6-1 보낸 것

- 그림 `net194_overview.png` (svg 같이) · 값 `net194_overview_data.csv` (케이스 194 행) · 코호트별 요약 `net194_value_summary.tsv` · 스크립트 `plot_overview.py` (`docs/data/lhs_network194_11fcf91e8/overview_20261005/`) — **커밋된 `merged/*/metrics_flat.csv` 만 읽는다 (계산 0)** · 수송 tortuosity = `tau_flux.ion_columns` 와 같은 식 (φ_mc / f_mc · f_mc = σ_ratio · L_gap / L_mc).  띠 규칙 (G1) 은 metrics_flat 에 없어 그림에선 안 걸렀다 → 인계 v1.2 상태 칸과 대조 = 같다 (BAND_FALLBACK 0 · Physics < 1 = 같은 10 건).
- 표기: 1저자 10-05 밤 *"τ² 이라 표현하지 말고 수송 tortuosity"* — 그림 · 보고 자료의 tau2 표시 이름 = **수송 tortuosity (= φ_SE·σ₀/σ_eff · 제곱근 아님 = 문헌의 tortuosity factor)** · 키 `tau2_*` 그대로.

### 6-2 숫자 (Hertz 가 주 모드 · 결정 16-3)

| 양 | LHS 130 | LHSx 64 (SE 많은 쪽) |
|---|---|---|
| SE 관통 (이온 망) | 106 · 비관통 24 (전부 φ_SE < 0.17) | 64 |
| σ_ion (mS/cm) | 1.4e-4 – 0.78 (중앙 0.23) | 0.62 – 2.14 (중앙 1.41) |
| σ_e (mS/cm) | 1.19 – 15.8 (중앙 5.96) | 0.011 – 4.75 (중앙 0.52) · AM 비관통 7 (φ_AM 0.14–0.23) |
| 수송 tortuosity (이온) | 1.97 – 1868 (중앙 4.77) | 1.25 – 2.56 (중앙 1.59) |
| Bruggeman a (이온 · ln f / ln φ_SE) | 1.89 – 4.82 (중앙 2.37) | 1.84 – 2.52 (중앙 2.09) |
| σ_ion Physics / Hertz | 0.25 – 1.11 (중앙 0.69) | 0.93 – 1.43 (중앙 1.23) |
| 협착 전력 몫 (이온 · Hertz) | 67.2 – 92.3 % (중앙 69.7) | 66.3 – 67.9 % (중앙 66.8) |
| 협착 전력 몫 (이온 · Physics) | 25.3 – 93.0 % (중앙 67.9) | 13.6 – 34.8 % (중앙 20.3) |
| 수송 tortuosity (이온 · Physics) | 1.79 – 2127 (중앙 7.35) | **0.89** – 2.47 (중앙 1.28) — **1 미만 10 건** (φ_SE,mc 0.72–0.80 · `MODEL_BELOW_CONTINUUM_BOUND`) |

### 6-3 우리가 본 것 (데이터 현상만)

1. 관통 집합 — 망 단계의 SE 비관통 24 (LHS) · AM 비관통 7 (LHSx) 이 **독립 퍼콜 감사** (`docs/data/lhs_perc_audit_20261001/*_d1ec42fba/perc_audit.tsv` · `se_perc_webapp_dump` · `am_perc_webapp_dump`) 와 **같은 케이스 집합**이다 (130 · 64 집합도 같다).
2. basis — 망 φ (`phi_se`) 와 장부 φ_mc·L_mc/L_gap 의 차 최대 2.2e-16 (194 전부).
3. Hertz 수송 tortuosity < 1 = 0 건 · Bruggeman a 는 170 건 모두 1.5 보다 크다.
4. 같은 φ_SE 안의 σ_ion 퍼짐: φ_SE ≈ 0.17 (16 건) 25 배 → 0.47 (17 건) 1.3 배.
5. Physics / Hertz (σ_ion) 는 φ_SE ≈ 0.47 근처에서 1 을 넘는다 (LHS 90/106 < 1 · LHSx 60/64 > 1).  코드상 두 모드는 면적과 협착식이 함께 다르다: Physics 면적 (`scripts/plastic_coverage.py` `film_area_from_overlap` mode physics) = 항복 전 (δ/R* < `DR_YIELD_ONSET` ≈ 0.11 %) πR*δ (Hertz 모드 면적 = LIGGGHTS 기하 교차원판보다 작을 수 있다) · 그 뒤 max(πR*δ, A_LIGG, min(Tabor · 부피 · 기하 2πR_min²)) · 협착 = Hertz Maxwell 1/(2σa) ↔ Physics 1세대 ψ 배치 1/(2σaψ) · ψ = (1 − a/r_min)^1.5 (s = a/r_min > 0.4 에서 a 가 클수록 커진다 · s ≥ 0.998 이면 0 — a ≥ r_min 은 r_min 으로 잘려 여기 든다 — `network_conductivity.py` `build_network` · `L2-01`).  어느 쪽이 갈림을 만드는지는 접촉별 분포가 metrics 에 없어 가르지 않았다.
6. 협착 전력 몫 (이온 · Hertz) 은 LHSx 에서 66–68 % 로 거의 평탄하고, LHS 는 SE 가 줄수록 커진다 (최대 92 %).  Physics 모드는 LHSx 에서 14–35 %.
7. **같은 망의 CONTACT_FREE 해가 이미 연속체 한계 아래다** (`tau_below1_check.py` · metrics_flat 만): `sigma_bulk_net` (협착 항 0 · 간선 · R_bulk 는 두 모드 같음 — 194 행에서 차 0) 이 σ_cf > φ_sphere 인 것이 LHS 43/106 · LHSx 계산된 35/35, σ_cf > 1 (고체 SE 펠릿보다 큼) 이 LHSx 24 건 (최대 1.497).  더 SE 가 많은 LHSx 29 건 (φ_mc 0.67–0.80) 은 `sigma_bulk_net` 빈칸 — 계산된 최댓값이 솔버 거부선 (`sigma_ratio > 1.5` · `network_conductivity.py` `solve_network`) 바로 아래라 그 거부로 **보이나** 사유는 metrics 에 없다 (미확인).  ⇒ FULL 을 수송 tortuosity ≥ 1 에 붙잡는 것은 협착 항이다: τ < 1 10 건의 협착 전력 몫 Hertz 66.3–66.7 % ↔ Physics 13.6–16.3 % (수송 tortuosity Hertz 1.25–1.39 ↔ Physics 0.89–1.00).  R_bulk = 입자마다 단면 πr² 원기둥 × 중심 간 거리 반 (`build_network`) — 맞닿은 같은 구의 단순 입방 배열이면 협착 0 에서 수송 tortuosity 2/3 (원기둥 πr²·2r = 구 부피의 1.5 배).  10 건은 겹침이 큰 (`porosity_spheresum` −4.9 ~ −8.4 % · `porosity_union` 4.5–5.5 %) · SE–SE 이웃 10–11 개인 침대.  같은 10 건 Hertz 1.25–1.39 는 등방 HS 한계 (3−φ_mc)/2 = 1.10–1.14 보다도 위.

### 6-4 지금의 인계 계획 (확인 요청)

- 등록된 인계 범위 = ⑤⑥⑦ + **망 τ 묶음** (`f_ion_<m>` · `f_ion_<m>_gap` · `tau2_ion_<m>` · `tau_ion_<m>` · 상태 · 메타 · 두 모드) · LW 제외.  σ_e · σ_th · 협착 전력 몫은 **등록 범위 밖** (194 metrics 에는 있다).
- 용도 = ML 기술자 (이 모델 안의 상대 비교) · **물리 타깃 (실험 절대 대조) HOLD** 유지 (10-01 최종 판정 · G6 · 1세대 협착식 · σ₀ = 펠릿값 3.0 mS/cm).

### 6-5 질문

- **QV1 (기술)**: 봉인 감사 · 고친 로더 · 다시 읽기 검산 (§2-4) 이 등록 범위 194 값 (망 τ 묶음 + ⑤⑥⑦) 의 ML 기술자 인계를 받치는가 — 막는 것이 남았다면 무엇인가.
- **QV2 (열 단위)**: 빼거나 표지를 더 달아야 할 열이 있는가 — (a) 문턱 근처 수송 tortuosity 수백–2000 (값은 유효 · ML 쪽에 로그 변환 권고를 열 사전에 적을 것인가) (b) 비관통의 f = 0 · tau2 빈칸 (= ∞) 과 기술 실패 빈칸의 구분이 열 사전 · 상태 칸만으로 충분한가.  (Physics τ 는 QV3.)
- **QV3 (Physics 모드 τ — 1저자가 정하지 않고 Codex 판단을 묻는다)**: 6-3 의 5 · 6 · 7.  Physics 가 조밀 SE 침대에서 연속체 한계 아래로 가는 주된 원인이 면적 상한 (Tabor · 부피 · 기하) 의 과대인지, 6-3 의 7 (CONTACT_FREE 해가 이미 한계 아래 = 원기둥 R_bulk 근사가 겹친 조밀 침대에서 전도를 과대 계상하고 협착 항이 그것을 가린다) 인지.  두 안:
  - **안 1 (등록 그대로 · 역할 표기)**: 두 모드 모두 넘긴다 · τ 주 지표 = Hertz (값 170 건 모두 ≥ 1.25 · 협착 = Maxwell 이라 ψ 배치 결정과 무관) · Physics = 소성 접촉 면적 **민감도** 로 표기 (Hertz 의 한 방향 보정이 아니다 — 6-3 의 5 · 1세대 ψ 배치 `L2-01` 이 바뀌면 Physics 만 움직인다) · τ < 1 10 건 = 값 유지 + 상태 칸 + 열 사전 설명 (6-6).
  - **안 2 (배포 축소)**: 배포 τ = Hertz 만 · Physics τ 는 내부 인계표에만 (표지와 함께).
  - 1저자의 고려: Physics 는 써야 한다고 보지만 10 건 때문에 열 전체를 빼는 것도 과하다고 본다.  어느 안이 맞는가 · 안 1 이면 표기 · 거름 규칙에 더 필요한 것 · 6-3 의 7 이 Hertz 값의 기술자 지위에도 한정어를 요구하는가.
- **QV4 (범위 확장 후보)**: 등록 범위 밖 σ_e · σ_th · 협착 전력 몫 (Hertz) 을 다음 인계에 넣는다면, 이번 봉인 · 검산으로 충분한가 · 새 등록이 필요한가.
- **QV5 (절대값)**: 실험 절대 대조 금지 유지에 동의하는가 · 상대 서술 (조성 · 입경 경향) 은 어디까지 허용되는가.
- **QV6 (표기)**: 열 사전 · 웹앱의 tau2 표시 이름을 "수송 tortuosity (= tortuosity factor · 제곱근 아님)" 로 바꾸는 것이 τ 명명 규약 (판정 v2 · 'tortuosity factor' 는 τ² 에만) 과 충돌하는가 (키는 그대로).

### 6-6 안 1 일 때 열 사전 · 배포 README 에 넣을 설명 (초안 · 검토 요청)

- 수송 tortuosity (`tau2_ion_<m>`) = φ_SE·σ₀/σ_ion (제곱근 아님).  정의상 **1 이 바닥**이다 — 같은 양의 SE 를 전류 방향의 곧은 기둥으로 세운 경우 (어떤 미세구조도 그보다 잘 통할 수 없다).
- τ 를 하나만 쓴다면 **Hertz** (값 170 건 모두 1.25 이상).  Physics 는 소성 접촉 면적을 넣은 **민감도** 열이다 — Hertz 의 한 방향 보정이 아니다 (SE 적은 침대 대부분에서 Hertz 보다 덜 통하고, SE 많은 침대에서 더 통한다).
- Physics 10 건 (LHSx · SE 고체 부피분율 0.72–0.80) 은 1 아래 (0.89–1.00) = **물리값이 아니라 모델 한계**: 망 모델이 입자 내부 경로를 넉넉하게 세고, Physics 의 큰 접촉 면적이 그것을 가리던 접촉 저항을 거의 지운다.  상태 칸 `MODEL_BELOW_CONTINUUM_BOUND` · 값은 남겼다 (지우면 남은 값이 1 위쪽으로 골라진다) · 특징으로 쓸 때는 이 상태로 거른다.

## 7. 남긴 것 · 한정

- 판정문 §6 경계 그대로: 배포 원천 = 검증된 배치 + 고친 τ 로더뿐 · 웹앱 그룹 비교 · COMSOL export · regime DB 의 미가드 소비자는 범위 밖 (홍보 금지).
- P4 같은 세대 검사의 근거 = 지금 파일들 (`current_files_no_publish_hash`) — 모든 사본을 일관되게 고친 변조는 게시 때 해시 없이는 못 잡는다 (일관된 띠 변경은 상태 칸 BAND_FALLBACK 으로 드러난다).
- 다시 읽기 검산은 생성된 표를 커밋된 배치 증거 · τ 원천과 대조한 것이다 — 망을 다시 푼 것이 아니다.  인계표 생성은 1저자 WSL (`061ec1b58`) 이고, 이 컨테이너는 생성 · 실행을 하지 않았다.
- LW = frame_unverified · 194 인계 제외 유지.  메모리 추정식 = 진단만.
- §6 의 숫자는 metrics_flat 미리보기 · 점검 스크립트 값이다 — 인계 v1.2 의 상태 칸으로 거른 값이 정본 (C5 가 같은 식임을 확인).

## 8. 재현 (Linux · 리포 뿌리)

```bash
# (1) 다시 읽기 검산 — 인계 v1.2 · 봉인 감사 · τ 원천 (C1–C8)
mkdir -p /tmp/net194_tau && tar -xzf docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/net194_tau_sources_20261006.tar.gz -C /tmp/net194_tau
python3 docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/reread_v12.py \
  --handover-dir docs/data/lhs_network194_11fcf91e8/handover_v12_20261006 \
  --seal-audit docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/seal_audit.tsv \
  --tau-sources /tmp/net194_tau --out /tmp/reread.json                         # verdict PASS · fails []

# (2) 4차 탐침 — 고친 트리 재실행 (기대 rc: 7 탐침 0 · 뒤집은 사본 0 · 원본 1)
python3 docs/reviews/codex_rglr3_fix_probe_rerun_20261006/drive_fix_probe.py /tmp/rglr3_probe_rerun

# (3) 단위 시험
python3 scripts/run_network_194_parallel.py --selftest      # 51/51
python3 scripts/lhs_design_dataset.py --selftest            # 326/326
python3 webapp/test_network_handover_chain.py               # 19/19

# (4) 6-3 의 7 숫자 (metrics_flat 만)
python3 docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/tau_below1_check.py
```
