# LHS ML 인계 배포 v1.3 (최종판) — 생성기 미리 준비 · GO 뒤 실행 계획 (2026-10-07)

> 1저자 10-07 *"v1.3 생성기를 Codex 판정과 동시에 미리 준비"* · v1.3 범위 = CLAUDE.md LHS 줄 (10-06 밤 비준 — *"v1.3 에 최종이라고 하고 확실하게 넘겨주자"*):
> 세대 2 망 값 + **#1 ML 표 (빈칸 뜻대로)** · **#2 f 타깃 안내** · **#5 porosity–σ–CN 재적합** · **τ 표시 이름 (수송 tortuosity)** · 새 열 **`se_isolated_pct`**.
> ⛔ 이 문서 = **코드 · 시험만 준비한 상태**의 기록 + GO 뒤 명령이다.  v1.3 자료 (세대 2 인계표 · 배포 폴더) 는 아직 없다 — Codex 세대 2 GO +
> 새 194 배치 (세대 2 실행 등록 `docs/reviews/lhs_network_batch_registration_20261007_g2.md` · 봉인 manifest `expected_network_generation = g2`) 뒤에만 만든다.
> 리포에 v1.3 산출은 하나도 쓰지 않았다 (DRY RUN 은 스크래치에서만 · §4).
> ⚠ **이 커밋은 `webapp/app.py` 를 바꾼다 — 세대 2 발사 봉인 29 파일 중 하나다** (등록 §3).  들이는 순서는 §7 (발사 전에 통째로 push 하지 말 것).

## 0. 이 커밋의 상태

| 항목 | 상태 | 근거 |
|---|---|---|
| v1.3 생성기 (단계 A 인계표 · 단계 B 배포 · 대조) | 구현 · 시험 — 기준 코드 1/77 → 77/77 (기준의 1 = V13b "거부된 실행은 폴더를 남기지 않는다" — 옛 코드는 아무것도 안 만들어 저절로 참) | `scripts/lhs_release_build.py` (`--v13` · `--v13-check`) · `scripts/test_lhs_release_v13.py` |
| 발사 봉인 대조 (등록 §3 · §5 — 이 커밋 안에서 추가) | 배치 manifest `code_hashes` ↔ 빌드 체크아웃 (다르면 거부 · `--allow-seal-diff` 명시 승인 · 철자 정규화 · 기록) · `handover_code_hashes` 다름 = 경고 · ⓪b 다시 읽기 기록 `reread.json` 실패 = 거부 — 관문 넣기 전 판 63/77 (V0 · V16a–m 14 실패) → 77/77 | 같은 시험 V16 |
| 새 열 `se_isolated_pct` | 인계 생성기 유도 묶음 `se_isolation` (명시 opt-in · 옛 인계표 바이트 불변 · 단계 역량 표 · 실행기 ㉕ 짝 불변) · 관문 S0–S2 · 열 사전 — selftest 시험 먼저 378/385 → 385/385 | `scripts/lhs_design_dataset.py` selftest ㉝a–g |
| τ 표시 이름 | 열 사전 (tau2 = 수송 tortuosity · 제곱근 아님 · √ 값은 그 이름 아님 · 벽 τ 사전의 "이 표에 없음" 정정) · COMSOL 2D 내보내기 · 5 조성 러너 README — 기준 43/46 → 46/46 | `webapp/test_tau_labels.py` K6–K8 |
| 웹앱 화면 (J20-l) | 고립 전해질 (케이스 표 줄 · 영문 라벨 · 툴팁 · 그룹 비교 열 · MD 보고서 · 쉬운 설명 · 표 재구성기) + τ 표시 이름 (논문 라벨 · 툴팁 · 별칭 · 쉬운 설명) — 기준 2/20 → 20/20 (기준의 2 = 줄을 안 만드는 경우 · 옛 라벨끼리의 별칭 — 저절로 참) | 화면 시험 `test_v13_webapp_display` (패치 안 · 발사 뒤 추가) (app.py · single.html 을 읽는 시험은 이 파일에만 — §7) |
| 기준 커밋 | `beffa8a67` (세대 2 실행 등록 · 봉인 지문 갱신판 · 새 실행기 · 다시 읽기 도구 포함) 위로 다시 얹음 — 실행기 selftest · `g2_network_reread --selftest` · `test_reread_v12` · 압력 기록 시험 · 같은 날 들어온 웹앱 시험 (atoms-only porosity · τ 후보 경로 보기) 그대로 통과 | — |
| DRY RUN | 커밋된 v1.2 인계표 (세대 1) 로 경로만 — 스크래치에서 · 리포 산출 없음 | §4 |

## 1. v1.3 항목 → 생성기가 만드는 것

| 항목 | 산출 (실제 = 접두 없음 · dry run = `DRYRUN_`) | 정의 · 한정 |
|---|---|---|
| 세대 2 값 | `<ds>_release_<D>_v13.csv` (주 표 = v1.2 주 표 열 순서 그대로 + `se_isolated_pct` + 세대 칸 `ion_net_generation` + 주 Hertz 역할 표기 넷 + 완료 압력 셋) · `<ds>_release_<D>_v13_physics.csv` (opt-in 부록 = v1.2 부록 + 세대 2 표기 다섯) · (선택) `_h12.csv` | 행마다 공용 세대 계약 (`tau_flux.row_generation_problems`) · 섞임 거부 · v1.3 = g2 만 |
| #1 ML 표 (빈칸 뜻대로) | `<ds>_mltable_<D>_v13.csv` + `_columns.tsv` (열 역할 · 빈칸 코드 개수) | 배포 값 칸은 그대로 (채우지 않는다) · 빈칸이 있는 열마다 바로 뒤 `<열>__blank` · 닫힌 어휘 7 (`NA_PHASE_ABSENT` · `NA_ZERO_CONTACTS` · `NA_NOT_PERCOLATING` · `INF_NOT_PERCOLATING` · `NOT_COMPUTED` · `HOLD_BAND_FALLBACK` · `EMPTY_NO_REASON`) · 둘째 열 `dataset` · 열 역할 닫힌 표 (모르는 열 = 거부) |
| #2 f 타깃 · 관통 분류 | ML 표 끝 열 `ion_percolates_hertz` (1 관통 · 0 비관통 · 빈칸 + 코드 = 기술 실패 · HOLD) · README §3 · 열 사전 `f_ion_hertz` 뜻 끝 "ML 1차 타깃" | 타깃 = `f_ion_hertz` (유한 · 비관통 0.0 = 물리적 0) · T · √T 는 비관통에서 ∞ — 타깃 · 특징 금지 (T = φ_SE,mc/f 항등식) · 2 단계 (분류 → 관통 행 회귀) · 고립 열은 비관통에 몰린다 (README 가 수로 보인다) |
| #5 porosity–σ–CN 재적합 | `lhs_v13_refit_porosity_sigma_cn_rows.csv` · `_summary.json` · `origin/` (워크시트 셋 · 1 줄 Long Name · 2 줄 Units · utf-8-sig · LF · GUIDE) · `previews/…png` · `.svg` | 대상 ln f_ion_hertz · 관통 행 (OK · MODEL_BELOW_CONTINUUM_BOUND) · φ_eff = σ_ionic T1 등록식의 SAT-blend 관통 거리 (φ = `phi_se_mass_conserving` · 동결 φc_P 0.200 · φc_S 0.195 · δ 0.040 · 크기 게이트 — 생산 `generate_comparison_plots` 에서 읽는다) · **locked** ln f = a + ½ ln φ_eff + 2 ln CN (등록식 지수 · 매개변수 1) · **free** ln f = a + α ln φ_eff + β ln CN · LOOCV = hat 행렬 · 데이터셋별 편향 · f_p · coverage · τ 항 없음 (τ = f 의 항등식) |
| τ 표시 이름 | 열 사전 · README §4 · 웹앱 · COMSOL 2D | `tau2_ion_*` = 수송 tortuosity T (제곱근 아님 · 문헌 tortuosity factor) · `tau_ion_*` = √T (그 이름 아님) · `tortuosity_SE_wall` = 기하학적 tortuosity · 키는 그대로 |
| `se_isolated_pct` | 주 표 · ML 표 · 웹앱 | = 100 − `top_reachable_pct` (AM 경로 고립과 같은 규칙 · 재실행 없음) · 외톨이 SE 를 연결로 세어 약간 적게 · 비관통에 몰린다 → 관통 분류 먼저 |
| README · 빌드 manifest | `README.md` (수 · 파일 · sha256 은 산출에서 센다) · `v13_build_manifest.json` (인계표 · 코드 · 파일 sha256 · 세대 · τ 다시 읽기 · **코드 신원** (발사 봉인 대조 · 명시 승인 · 인계 도구 지문 · git HEAD) · **배치 관문 기록** (`seal_audit.json` · `reread.json` sha256 + n_fail) · 경고) | 손으로 고치지 않는다 (sha256) — 판정문 전달 문안은 `--transfer-text` |

관문 (하나라도 걸리면 폴더를 세우지 않는다 — 임시 폴더에 다 만들고 `check_v13` 통과 뒤에만 옮긴다):
배치 manifest 기대 세대 = g2 · manifest plan.cohorts ↔ v1.3 입력 (수확 · union · 설계) · **발사 봉인 대조** (manifest `code_hashes` ↔ 빌드 체크아웃 — 다르면 거부 · 명시 승인만 통과) ·
**⓪b 다시 읽기 기록** (`reread.json` 이 있고 n_fail ≠ 0 · 기대 세대 ≠ g2 면 거부) · 단계 A 생성기의 `load_tau_results(expected_generation='g2')` (P0–P4) ·
행마다 세대 계약 + 섞임 · 웹앱 배치 done · partial 만 · τ 출처 부록 = 지금 검사 목록 · τ 다시 읽기 (`load_tau_results` 한 번 더 · 인계표 τ 칸과 글자 대조) ·
`se_isolated_pct` S1 · S2 · 빈칸 양방향 · 프로필 ml_v1 (키 · 기대 ID · 적격성 · 사전 참조 표지) · 열 역할 · ML 되읽기 · 재적합 재현 (상대 1e-9) · 파일 sha256 · README 표지.
단계 A 도 생성기를 부르기 전에 같은 봉인 · 다시 읽기 관문을 지난다 (몇 분짜리 생성을 헛돌리지 않게).

## 2. GO 뒤 명령 (순서 그대로 · 세대 2 등록 §4–§6 을 따른다)

### 2-0 전제

- Codex 세대 2 재검증 **GO** 판정문 (`docs/reviews/` 에 반입 · 경로를 `--codex-verdict` 로).
- 새 194 배치 = 세대 2 실행 등록 §4 그대로 (발사 체크아웃 `~/dem-audit` · 봉인 지문 = 등록 §3 의 값 (지금 `b313e61a…`) · 194/194 done) — 이 계획은 그 manifest 를 **소비만** 한다.
- 파이썬 = 배치 venv (`PY=$(ls ~/Yonghoon-DEM-DFT/venv/bin/python ~/Yonghoon-DEM-DFT/.venv/bin/python3 2>/dev/null | head -1)` — 시스템 python3 에는 numpy 가 없다 · 등록 §6).
- 이 v1.3 생성기 커밋이 어느 체크아웃에 있나 = §7 (발사 전에 생성기만 들였나 · 발사 뒤 통째로 들였나).

### 2-1 WSL · 발사 체크아웃 — 등록 §5 관문 (실행기 merge 가 찍는 후속 명령 ⓪ · ⓪b · ① · ②a 그대로)

```
R=~/net194_<발사 sha>; cd ~/dem-audit                       # 발사 체크아웃 (retry 가 거부하지 않게 그대로 둔다)
$PY scripts/run_network_194_parallel.py audit --root "$R" --tsv "$R/seal_audit.tsv" --json "$R/seal_audit.json"      # ⓪ rc 0 이어야
$PY scripts/g2_network_reread.py --launcher-root "$R" --expect-set production194 --json "$R/reread.json"           # ⓪b rc 0 이어야 (10-07 G2RR2-02 — 등록 집합 필수 · 생성기가 집합 = 194 를 요구)
$PY scripts/lhs_pressure_record.py --cohort docs/data/area_s2_cohort.tsv --harvest-dir docs/data/lhs_descriptors_cov_1e09f661d \
    --out "$R/pressure/lhs_pressure_record.tsv"                                                                  # ②a (--root-from · --root-to 는 실행기 출력 그대로)
$PY scripts/lhs_pressure_record.py --cohort docs/data/lhsx_descriptors_20260925/_cohort.tsv --harvest-dir docs/data/lhsx_descriptors_cov_1e09f661d \
    --out "$R/pressure/lhsx_pressure_record.tsv"
```

- ① τ 진단 표 (`tau_flux.py … --tsv`) 는 진단 전용 — 원하면 실행기 출력 그대로.
- ⚠ 실행기 출력의 **② 생성기 명령 (`_handover_v13_` 이름) 은 쓰지 않는다** — 그 명령의 묶음 (`HANDOVER_GROUPS` = contact · percolation · f1 · fracture · area · tau) 에는
  `se_isolation` 이 없어서 그 인계표로는 v1.3 빌드가 거부한다 ("인계표에 없는 v1.3 열 ['se_isolated_pct']").  2-2 의 한 명령이 단계 A 로 같은 생성기를 같은 출처 관문
  (`--tau-results` · `--tau-batch-manifest` · `--pressure-record`) 에 `se_isolation` 을 더해 부른다.

### 2-2 WSL — v1.3 한 명령 (단계 A + B + 대조)

```
D=$(date +%Y%m%d)
# (가) 발사 전에 생성기만 들인 경우 (§7 권고) — 발사 체크아웃에서 그대로:
cd ~/dem-audit
# (나) 발사 뒤 통째로 들인 경우 — 발사 체크아웃은 그대로 두고 별도 작업 트리에서:
#   git -C ~/dem-audit fetch origin claude/stoic-knuth-NObVQ && git -C ~/dem-audit worktree add --detach ~/v13-build <v1.3 커밋> && cd ~/v13-build
$PY scripts/lhs_release_build.py --v13 --batch-root "$R" \
    --codex-verdict docs/reviews/<GO 판정문>.md [--transfer-text <판정문 전달 문안>.txt] \
    --handover-out "$R/handover_v13_$D" --out-dir "$R/release_v13_$D" --date $D \
    [--allow-seal-diff webapp/app.py]          # (나) 만 — 화면 문구만 바뀐 봉인 파일 (값과 무관) · README · 빌드 manifest 에 기록
```

- 단계 A (`stage_handovers_v13`) — 먼저 manifest 기대 세대 · 원천 · **발사 봉인 대조** · **⓪b 다시 읽기 기록** 을 본 뒤, 데이터셋마다 인계표 생성기 CLI:
  `--webapp-groups contact,percolation,f1,fracture,area,tau,se_isolation` · `--tau-results $R/merged/<ds>/results` · `--tau-batch-manifest $R/manifest.json` ·
  `--pressure-record $R/pressure/<ds>_pressure_record.tsv` → `$R/handover_v13_$D/<ds>_handover_v13_$D.csv` (+ 열 사전 · 제외 노트 · τ 출처 부록).
  세대 2 아닌 · 섞인 배치는 생성기 `load_tau_results` 가 거부.
- 단계 B (`build_v13`) — 같은 관문 + τ 다시 읽기 (`load_tau_results` · 같은 기대 세대) → 배포 · ML 표 · 재적합 · README · 빌드 manifest → `check_v13` → `$R/release_v13_$D`.
- 봉인 대조가 거부하면 메시지가 다른 파일을 적는다 — `webapp/app.py` (이 커밋의 화면 문구) 말고 다른 파일이 나오면 **승인하지 말고** 멈춘다 (τ · 망 코드가 발사 뒤 바뀐 것).
- (나) 의 README · 빌드 manifest 에는 `handover_code_hashes` ≠ 발사 기록 경고가 남는다 (v1.3 생성기가 발사 뒤 들어왔다) — 등록 §9 에 v1.3 커밋을 적는다 (등록 §3 ⚠ 그대로).

### 2-3 WSL → 리포

```
tar czf ~/lhs_v13_$D.tar.gz -C "$R" handover_v13_$D release_v13_$D seal_audit.json reread.json
cp ~/lhs_v13_$D.tar.gz /mnt/c/Users/Administrator/Downloads/
```

### 2-4 컨테이너 — 반입 · 대조 · 커밋

```
# 반입: handover_v13_<D>/ → docs/data/lhs_network194_<sha>/handover_v13_<D>/ · release_v13_<D>/ → docs/data/lhs_release_<D>_v13/
python3 scripts/lhs_release_build.py --v13-check --release-dir docs/data/lhs_release_<D>_v13 \
    --handover-dir docs/data/lhs_network194_<sha>/handover_v13_<D>        # rc 0 = 통과 (τ 다시 읽기 · 봉인 대조는 빌드 manifest 의 WSL 기록)
```

- 커밋 하나 → 게이트 → 바로 push (컨테이너 재시작 대비) · ZIP (수영 님) = 배포 폴더 그대로 (`DRYRUN_` 파일 없음 확인).
- 원장 · CLAUDE.md LHS 줄 · 진행 기록 · 등록 §9 (v1.3 커밋) 는 그 커밋에서 (이 커밋은 손대지 않았다).

## 3. 생성기가 거부하는 것 (막히면 볼 곳)

| 메시지 (요지) | 뜻 | 할 일 |
|---|---|---|
| `배치 manifest — … expected_network_generation …` | manifest 에 기대 세대 선언이 없다 (예: v1.2 배치 11fcf91e8) | 새 194 봉인 manifest 로 |
| `기대 세대 'inferred_legacy' ≠ g2` | 세대 1 배치 | 세대 2 배치만 |
| `발사 봉인 코드 지문 (code_hashes) 이 없다` | 194 실행기 manifest 가 아니다 | 실행기 manifest 로 |
| `발사 봉인 파일 N 이 이 체크아웃과 다르다 [...]` | 빌드 체크아웃의 봉인 파일이 발사 때와 다르다 (τ 출처 관문 · 다시 읽기가 다른 코드로 돈다) | 발사 체크아웃에서 만들거나 · 값과 무관한 변경 (화면 문구) 만 `--allow-seal-diff <파일>` |
| `⓪b 다시 읽기 기록 … n_fail …` | `reread.json` 이 실패 · 다른 기대 세대를 적었다 (등록 §5-3) | 다시 읽기 rc 0 이 될 때까지 인계하지 않는다 |
| `세대 관문 … 세대 계약 위반` · `세대 섞임` | 행 표기가 세대 계약 밖 · 한 표에 두 세대 | 배치 · 생성기 세대 확인 (G2R-01 · 02) |
| `τ 다시 읽기 문제` | 인계표 τ 칸 ≠ 지금 폴더에서 다시 읽은 값 · 또는 load_tau_results 거부 | 배치 뒤 폴더가 바뀌었다 — 재계산 · 다시 생성 |
| `완료 압력 기록이 없다` · `완료 압력 열 (press_*) 이 없다` | DESC-06 | 2-1 의 압력 기록 (명시 승인 `--pressure-unverified` 는 1저자 결정) |
| `인계표에 없는 v1.3 열 ['se_isolated_pct' …]` | 실행기 출력의 ② 명령 (`se_isolation` 없음) 이나 옛 생성기로 만든 인계표 | 2-2 의 한 명령 (단계 A) 으로 |
| `se_isolated_pct 항등식` | 인계표 값 ≠ 100 − top_reachable_pct | 생성기 세대 확인 |
| `설명 안 되는 빈칸` · `빈칸 (…) 이어야 한다` | 빈칸 뜻 규칙 밖 (#1) | 원천 확인 — 규칙을 넓히려면 먼저 시험 (추측으로 코드를 달지 않는다) |
| `열 … 의 ML 역할을 모른다` | 새 열이 역할 표에 없다 | `V13_ROLE_FIXED` 에 등재 (1저자 확인) |
| `dry-run 산출을 리포 안 … 에 쓰지 않는다` | DRY RUN 이 docs/data 의 배포 폴더와 섞이거나 커밋되지 않게 | 리포 밖 스크래치에 |

경고 (만들기는 한다 · README "경고" 절 · 빌드 manifest): `handover_code_hashes` ≠ 발사 기록 (§7 (나)) · `seal_audit.json` · `reread.json` 이 배치 뿌리에 없음 (2-1 을 건너뜀) ·
쓰이지 않은 `--allow-seal-diff` · 커밋 안 된 추적 파일 변경 (빌드 신원 = git HEAD + 코드 지문).

## 4. DRY RUN (세대 1 원천 · 시험 전용 — 값 인용 금지)

```
python3 scripts/lhs_release_build.py --v13 --dry-run --handover-dir docs/data/lhs_network194_11fcf91e8/handover_v12_20261006 \
    --out-dir <스크래치>/dryrun_v12 --date <D>
python3 scripts/lhs_release_build.py --v13-check --dry-run --handover-dir docs/data/lhs_network194_11fcf91e8/handover_v12_20261006 \
    --release-dir <스크래치>/dryrun_v12
```

- 결과 (10-07 · 컨테이너 · 기준 `beffa8a67` 위): 만들기 · 대조 통과 (rc 0 · 둘 다) · 파일 22 (빌드 manifest 포함 · 전부 `DRYRUN_` · README 첫 줄 "DRY RUN — not a release") · 세대 = inferred_legacy (두 데이터셋) ·
  빠진 v1.3 열 11 (se_isolated_pct · 세대 2 표기 · 완료 압력 — 세대 1 인계표에 없다 · 기록하고 뺐다) · 재적합 적합 행 170 (130 중 관통 106 + 64) · 비관통 24 제외 ·
  ML 표 비관통 24 = `INF_NOT_PERCOLATING` (T) · `NA_NOT_PERCOLATING` (기하 τ) · mono 30 = `NA_PHASE_ABSENT` · 코드 신원 · 배치 관문 기록 = 없음 (dry run 은 봉인 대조를 하지 않는다 ·
  `--allow-seal-diff` 를 주면 거부).
- 같은 명령에 `--dry-run` 이 없으면 거부된다 (세대 1 · Codex 판정문 · 배치 뿌리 — 폴더 안 만듦) — 시험 V14a · V15c.
- v1.2 인계표의 열 사전 문구 (표지 전) 는 프로필 ml_v1 의 사전 참조 표지 문제를 낸다 — dry run 은 경고로만 · 실제 v1.3 은 지금 생성기 사전 (표지 있음 — selftest ㉛h · 시험 V12 의 합성 세대 2 인계표가 프로필 통과) 이라 문제로 막는다.

## 5. 1저자가 정할 것

| # | 질문 | 권고 |
|---|---|---|
| Q1 | H12 민감도 부록을 v1.3 에 싣나 (`--h12-appendix`) | 싣지 않는다 — 정본 인계표에는 있다 · 기본 학습 열 아님 · H0 와 짝인 시나리오 (구간 아님 · G2R-04) |
| Q2 | 완료 압력 (DESC-06) | 194 전부 기록 (2-1) — `--pressure-unverified` 는 쓰지 않는다 |
| Q3 | #5 재적합 식 | 이 커밋의 두 식 (locked = 등록식 지수 ½ · 2 · free = 지수 재적합 · φ_eff 동결 상수) 을 세대 2 값을 보기 **전** 등록으로 둔다.  "porosity–σ–CN" 이 다른 관계 (예: 기공률 · CN 만의 거듭제곱) 를 뜻했다면 GO 전에 말해 주면 그 식으로 바꾼다 |
| Q4 | README 전달 문단 | GO 판정문에 전달 문안이 있으면 그 문단을 텍스트 파일로 `--transfer-text` (README 를 손으로 고치지 않는다 — 빌드 manifest sha256) |
| Q5 | 빈칸 코드 열 이름 · ML 표 형식 | `<열>__blank` (값 칸 그대로 · 넓은 표) — 다른 꼴 (긴 표 · 열마다 결측 표지 0/1) 이 필요하면 수영 님 쪽 학습 코드에 맞춰 바꾼다 |
| Q6 | 이 커밋을 언제 들이나 (`webapp/app.py` = 세대 2 발사 봉인 파일 · §7) | (가) 발사 **전에** 생성기 · 배포 · 시험 · 문서 (봉인 파일 없음) 만 들이고, 화면 넷 (app.py · single.html · 화면 시험 · check_all 한 줄) 은 발사 **뒤** — 발사 코드 = Codex 검토 코드 · 발사 manifest 의 인계 도구 지문 = v1.3 생성기 · v1.3 을 발사 체크아웃에서 승인 없이 만든다 · 등록 §9 에 발사 커밋의 봉인 밖 변경 한 줄.  등록 글자 ("문서 · 원장만") 를 그대로 지키려면 (나) · 선례 (`beffa8a67`) 대로 다시 봉인하려면 (다) |

## 6. 코드 지도 (`scripts/lhs_release_build.py`)

`v13_columns` (열 명세) · `v13_blank_reason` · `v13_blank_problems` (#1 규칙 · 양방향) · `v13_role` (열 역할 닫힌 표) · `v13_ml_table` · `v13_ml_decode` ·
`v13_se_isolated_problems` (생성기 관문 `_se_iso_gates` 를 다시 부른다) · `refit_porosity_sigma_cn` · `refit_from_csv` (#5 — 아무 인계표 · 배포 CSV) ·
`v13_generation_problems` · `v13_manifest_generation` · `v13_manifest_inputs_problems` · `v13_seal_drift` · `v13_seal_gate` (발사 봉인 대조) ·
`v13_batch_gate_files` · `v13_batch_gate_check` (⓪ · ⓪b 기록) · `v13_handover_argv` · `stage_handovers_v13` (단계 A) ·
`v13_reread_tau` (`load_tau_results` 다시 읽기) · `build_v13` (단계 B) · `check_v13` (대조) · `_v13_readme` (README 틀).
생성기 (`scripts/lhs_design_dataset.py`): `WA_SE_ISO_GROUP` · `WA_DERIVED_SE_ISO` · `_se_iso_gates` · 열 사전 τ 문구 (`_TAU_PER_MODE` · `TAU_F_TARGET_NOTE`).
실행기 (`scripts/run_network_194_parallel.py`) · 다시 읽기 도구 (`scripts/g2_network_reread.py`) 는 이 커밋이 손대지 않았다 — manifest (`expected_network_generation` · `code_hashes` ·
`handover_code_hashes`) 와 배치 뿌리 파일 (`seal_audit.json` · `reread.json`) 을 읽기만 한다.

## 7. 들이는 순서 — `webapp/app.py` 는 세대 2 발사 봉인 파일

- 세대 2 실행 등록 §3 의 봉인 29 파일에 `webapp/app.py` 가 있다 (워커 `lhs_webapp_batch` → `app` 전이 의존) — 화면 문구만 바꿔도 봉인 지문이 바뀐다.
  기준 `beffa8a67` (등록 §3 갱신판 — app.py `bd4c25e5…` · `code_fp b313e61a…`) 위에서 이 커밋의 app.py 로 다시 재면 app.py `55e28d22…` · `code_fp 7702f4e5…`
  (나머지 28 파일은 등록 값 그대로 · 이 컨테이너에서 실행기와 같은 식 `code_fp` 로 계산 — 그 사이 다른 봉인 파일이 바뀌면 들일 때 실행기 `--dry-run` 으로 다시 잰다).
  ⇒ 통째로 발사 **전에** 가지에 들이면 1저자 사전 점검 (등록 §1 단계 2 — 봉인 지문이 §3 값과 같아야) 과 등록 봉인이 어긋난다.
- 인계 단계 코드는 봉인 밖이다 — `scripts/lhs_design_dataset.py` 지문 `a678994861a1…` (등록 §3) → `a4b40dcd10c1…` (이 커밋) 은 등록이 예상한 변화다 (§3 ⚠ "그 커밋을 §9 에 적는다").
- 그래서 화면 쪽만 따로 들일 수 있게 묶었다 — **{`webapp/app.py` · `webapp/templates/single.html` · 화면 시험 `test_v13_webapp_display` (패치 안 · 발사 뒤 추가) · `scripts/check_all.sh` 의
  `webapp: v13_webapp_display` 한 줄}**.  이 넷을 빼고 들여도 나머지 시험은 초록이다 (컨테이너 실측 — app.py · single.html 을 기준 판으로 둔 채
  `test_lhs_release_v13` 77/77 · 생성기 selftest 385/385 · `lhs_release_build --selftest` 31/31 · `test_tau_labels` 46/46 · `webapp_network_batch --selftest` · 그 밖 웹앱 시험 넷 통과 ·
  화면 시험만 4/20).
  single.html 이 화면 쪽에 들어가는 까닭 = 논문 라벨 별칭 (PAPER_TO_ORIG) 이 app.py 의 새 라벨과 짝이다.
- 경우별:
  (가) **권고** — 발사 전에 화면 넷을 뺀 나머지를 들인다 → 봉인 파일 = Codex 가 본 그대로 (발사 코드 = 검토 코드) · 발사 manifest `handover_code_hashes` = v1.3 생성기 ·
  2-2 를 발사 체크아웃에서 `--allow-seal-diff` 없이 · v1.3 뒤 화면 넷을 들인다.  ⚠ 등록 §3 첫 줄의 "그 뒤 **문서 · 원장만** 바뀐 커밋" 과 글자로는 어긋난다
  (봉인 밖 스크립트가 바뀐 커밋) — 등록 §3 ⚠ 가 예상한 인계 도구 변경이므로 발사 직후 §9 에 "발사 커밋 = 등록 커밋 + v1.3 인계 단계 코드 (봉인 밖 · code_fp 같음)" 를 적는다 (1저자 확인).
  (나) 등록 글자 그대로 — 발사는 등록 커밋 (또는 문서만 바뀐 뒤 커밋) 에서 · 이 커밋은 발사 뒤 통째로 → 2-2 를 별도 작업 트리에서 `--allow-seal-diff webapp/app.py` ·
  `handover_code_hashes` 경고 (등록 §9 에 v1.3 커밋).
  (다) 발사 전에 통째로 + 등록 §3 의 app.py 행 · code_fp 를 다시 적는다 (선례 `beffa8a67` — 같은 날 atoms-only porosity 의 app.py 변경을 그렇게 다뤘다) → 가장 단순한 끝 상태
  (한 체크아웃 · 승인 없음) 이지만 Codex 가 본 봉인 지문과 발사 지문이 또 갈린다 (값과 무관한 화면 문구라는 설명이 필요).
- (다) 를 고르면 사전 점검 (등록 §1 단계 2) 의 기대 code_fp 가 바뀐다 — 사전 점검 전에 등록을 고치거나, 이미 돌렸으면 단계 2 (dry-run) 만 다시.
- 이 커밋을 push 하지 않고 들고 있는 동안은 컨테이너 재시작에 잃는다 (CLAUDE.md "컨테이너 재시작 대비") — 곁가지에 올려 두는 것은 주 세션 판단.

## 1저자 결정 (10-07 05:5x · *"권고대로 해"*) · 반입 방식

- Q1 H12 부록 = v1.3 에 넣지 않는다 · Q2 압력 기록 = 194 전부 (`--pressure-unverified` 쓰지 않음) · **Q3 재적합 = 위 두 형태 (지수 고정 ½ · 2 / 자유) 를 세대 2 값을 보기 전에 이 문서로 등록** ·
  Q4 README 전달 문구 = Codex GO 판정 문구 그대로 (`--transfer-text`) · Q5 ML 표 = 넓은 표 + `<열>__blank` · Q6 = (a) 화면 부분은 발사 뒤.
- 반입 (메인 세션): 생성기 · 시험 · 계획서는 지금 반입 — 화면 네 항목 (`webapp/app.py` · `webapp/templates/single.html` · 화면 시험 `test_v13_webapp_display` (패치 안 · 발사 뒤 추가) ·
  `scripts/check_all.sh` 의 `run 'webapp: v13_webapp_display' python3 test_v13_webapp_display (패치 안 · 발사 뒤 추가)` 한 줄) 은 봉인 파일 `app.py` 를 바꾸므로 **194 발사 뒤**
  `git apply docs/reviews/lhs_release_v13_display_deferred_20261007.patch` + 그 check_all 한 줄로 넣는다 (패치 = 원 커밋 10aa3ba69 의 세 파일 diff 그대로).
