# LHS214 B7 — 등록 §5 판정 (받은 기록만 · 2026-11-02) · ⛔ 배포 HOLD 그대로

- 무엇: 10-30 발사 기록 (이 폴더의 위 README) 에 **194 등록 §5 (활성 개정 §9-8 ①–⑦)** · **보충 등록 §5 (활성 개정 §9-3)** 규칙을 그대로 적용한 판정 (1저자 11-01 주간보고 Q4 권고 — *"§5 판정 → τ · 압력 → 인계표 순서 · 배포 HOLD 는 그대로 · L214P-02 한 줄을 같은 묶음에"*).
- 방법: 받은 묶음 둘 (194 · 보충 20 · sha256 = 위 README 표와 같음) 을 리포 밖 **빈 폴더**에 풀어 `python3 -I` 로 읽기만 · 판정 함수 = 리포 것 그대로 (사본 금지 — §9 도구가 부른다).
- 분석 트리의 봉인 32 파일 · 인계 도구 2 (`scripts/lhs_design_dataset.py` · `scripts/g2_network_reread.py`) · 배포 빌더 (`scripts/lhs_release_build.py`) = 승인 핀 B7 `35f0327377a4213774010a090df4d224e50d29e1` 과 바이트 같음 (manifest code_hashes · handover_code_hashes sha256 대조 · code_fp `2149f873…c3eb`).
- ⛔ 이 폴더 = **진단 기록** — 인계표 · 배포 산출물이 아니다 · v1.3 배포 HOLD 그대로 · 등록 기준을 고치거나 넓히지 않았다.

## 0. 요약

| 항목 | 결과 |
|---|---|
| §5-1 · §5-2 · §5-3 (기록 판정) | 두 배치 모두 충족 — done 194 · 20 · failed 0 · SEALED 194 · 20 · 다시 읽기 n_fail 0 · 집합 일치 |
| ⓪ · ⓪b 배포 관문 같은 함수 재판정 | 내용 문제 0 · 남은 2 건 = 경로 결합 (기록의 배치 뿌리 = WSL 경로 ≠ 사본 위치 — WSL 에서만 닫힌다) |
| τ 상태 (§5-4) | 표지 유지 · BAND_FALLBACK 0 · 기술 실패 NOT_COMPUTED 0 · Physics FULL 모형 한계 14 (lhsx 8 · lhss 6) · **H0 모형 한계 0** |
| §9-8 ⑤ 주 타깃 관문 | `v13_primary_model_limit_problems` 문제 **0** (세 데이터셋) → 배포 HOLD 의 근거가 이 관문이 아니게 됐다 (Q2) |
| §5-7 회귀 (v1.2 대비 · 레코드 수준) | 망 밖 열 = 같음 (다른 두 열은 설명됨) · **H0 이온 배포값 2 행이 선언 문턱 1.5e-4 를 넘음** (Q1) |
| 압력 기록 · 인계표 v1.3 생성 | 입력이 묶음에 없음 → 미실행 · WSL 명령 = §5 · §6 |
| L214P-02 | 시험 먼저 139/141 → 고친 뒤 141/141 · 봉인 무변경 (§7) |

## 1. §5 판정 표

| 등록 칸 | 규칙 요지 (등록 문구) | 194 (lhs 130 · lhsx 64) | 보충 20 (lhss) | 판정 |
|---|---|---|---|---|
| §5-1 케이스 | done / failed (+ failure_kind) · failed 는 빈칸 + 사유 · 재실행 = retry 만 | done 194 · failed 0 · 시도 1 (worker.json · progress.tsv) · runs = run_001 한 번 (retry 0) · 단계 실패 0 (`Network Merge` 줄 = ok 칸 없이 rc 0 — `webapp/app.py` `_network_merge_log` · v1.2 기록도 같음) | done 20 · failed 0 · 같음 | 충족 (기록) |
| §5-2 감사 | rc 0 = 형식 current · 전부 SEALED · 세대 g2 · 입력 지문 = 발사 (보충: + 관측 문제 0 · 결합 expected = observed) | 등록 §4 덧붙임 확인 스니펫 그대로: 케이스 194 · `{'SEALED': 194}` · 결합 = 완료 시도 True 194/194 · expected ≠ observed `[]` · 감사 문제 `[]` · 미최종 0 · 시작 · 끝맺음 970/970 · 자격 current · merged same 194 · 세대 g2 194 · 세대 · 입력 문제 `[]` | 20 · `{'SEALED': 20}` · True 20/20 · `[]` · `[]` · 0 · 100/100 · 나머지 같음 | 충족 (기록 · audit rc 0 = 1저자 화면 — import 관측 로그가 묶음 밖이라 여기서 audit 를 다시 돌리지 않았다) |
| §5-3 다시 읽기 | rc 0 · M0 · M-plan · M-reg · M1 · M2 · M3 · K1–K7 · H1 | 스키마 v3 · n_fail 0 · production194 기대 194 = 읽음 194 · set_equal · missing · extra `[]` · meta 10/10 · K1–K7 194/194 · manifest_sha256 = 받은 manifest · seal_fp · launch_sha 일치 | supp20 20 = 20 · meta 7/7 · K1–K7 20/20 · 결합 일치 | 충족 (기록 · 다시 읽기 재실행 = WSL — 케이스 결과 원본 필요) |
| ⓪ · ⓪b 같은 함수 | `lhs_release_build.v13_batch_gate_problems` (build · 단계 A · check 공용) | 문제 2 = 경로 결합 2 · 그 밖 0 | 문제 2 = 경로 결합 2 · 그 밖 0 | 내용 판정 통과 (경로 결합은 WSL 실제 뿌리에서) |
| §5-4 τ 진단 | 상태 표지 (NOT_PERCOLATING · NOT_COMPUTED · BAND_FALLBACK · MODEL_BELOW_CONTINUUM_BOUND) 유지 | §2 표 | §2 표 | 기록 (다시 읽기 H1 = `load_tau_results` 칸) · `tau_flux.py --tsv` 진단 표 자체 = WSL |
| §5-5 인계 생성기 관문 | ⑤F1 · ⑥R1–R3 · ⑦A1–A5 · τ 출처 P0–P4 · `--tau-batch-manifest` | 미실행 (§6 입력 결손) | 미실행 | WSL 단계 A |
| §5-6 계약 상수 | 봉인 파일 안 (실행기 재선언 없음) | manifest 봉인 32 = 등록 §3 ✅ 지문 · 분석 트리 바이트 같음 | 같음 | 충족 |
| §5-7 회귀 | 망 밖 열 같은 값 · 허용 = 선언된 변경 · *"그 밖의 차이는 보고하고 원인을 밝힌 뒤에만 싣는다"* | §4 — 2 행 문턱 초과 | v1.2 기준 없음 (lhss = v1.3 새 데이터셋) | **1저자 결정 Q1** |
| §9-8 ①–③ | 모형 한계 범주 · 공용 판정 · 우선순위 | Physics FULL 모형 한계 8 (lhsx) · H0 0 · 전자 FULL 모형 한계 0 · 다른 채널 실패 0 · CF · 협착-only `model_over_conduction` 값 유지 | Physics 6 · H0 0 · 전자 0 | 규칙과 어긋남 0 (공용 판정 = 다시 읽기 K2 · K6 통과) |
| §9-8 ④ 공란 | 모형 한계 = NOT_COMPUTED + 사유 정확히 `full_over_conduction` · f · f_gap · tau2 · tau 빈칸 · 표지 True | 위반 0 | 위반 0 | 충족 (`blank_rule.txt` · 214 × 3 모드) |
| §9-8 ⑤ 주 타깃 | H0 모형 한계 = 진단 레코드 · v1.3 주 타깃 배포 HOLD 관문 | 문제 0 (표지 `full_model_limit_hertz` False 194) | 문제 0 (False 20) | 관문 문제 없음 → **Q2** |
| §9-8 ⑥ 결과 보고 | Hertz 가용 수 · Physics 모형 한계 수 따로 | §3 | §3 | 이 문서 §3 |

## 2. τ 상태 (다시 읽기 H1 칸 · `tau_status_by_case.tsv`)

| 데이터셋 (n) | Hertz (H0 · 주 타깃) | Physics (부록) | H12 (민감도) |
|---|---|---|---|
| lhs (130) | OK 106 · NOT_PERCOLATING 24 | OK 99 · MBCB 7 · NOT_PERCOLATING 24 | OK 106 · NOT_PERCOLATING 24 |
| lhsx (64) | OK 64 | OK 5 · MBCB 51 · NOT_COMPUTED (full_over_conduction) 8 | OK 52 · MBCB 12 |
| lhss (20) | OK 17 · NOT_PERCOLATING 3 | OK 7 · MBCB 4 · NOT_COMPUTED (full_over_conduction) 6 · NOT_PERCOLATING 3 | OK 11 · MBCB 6 · NOT_PERCOLATING 3 |
| 합 (214) | OK 187 · NOT_PERCOLATING 27 | OK 111 · MBCB 62 · 모형 한계 14 · NOT_PERCOLATING 27 | OK 169 · MBCB 18 · NOT_PERCOLATING 27 |

- MBCB = MODEL_BELOW_CONTINUUM_BOUND (값 유지 + 표지 · 등록된 모형 한계 표지 — 오류 아님) · NOT_COMPUTED 사유는 전부 `full_over_conduction` (기술 실패 0) · BAND_FALLBACK 0 (띠 규칙 L0 214 × 3 모드) · basis_check ok 214 × 3 · σ₀ 3.0 mS/cm · 25 °C · φ = mass_conserving · L = L_mc · 세대 g2 = 214.
- 가지 표 (모드 × 가지 · 214 침대 합): FULL — hertz computed 187 · valid_zero 27 / physics computed 173 · not_computed (full_over_conduction) 14 · valid_zero 27 / H12 computed 187 · valid_zero 27.  CF — hertz · physics computed 150 · `model_over_conduction` 37 · valid_zero 27 / H12 computed 175 · MOC 12 · valid_zero 27.  협착-only — hertz computed 187 · valid_zero 27 / physics not_computed (`zero_resistance_requires_contraction` · GEN2-01) 187 · valid_zero 27 / H12 computed 133 · MOC 54 · valid_zero 27.
- 채널 (metrics_flat): 이온 · 전자 · 열 판정 ok 214 · 솔버 success 214 · failed_channels 없음 · 전자 FULL 모형 한계 0 (두 모드) · 전자 valid_zero (no_through_path) lhsx 7 · lhss 6.
- Physics 모형 한계 14 = lhsx_051 · 053 · 054 · 060 · 061 · 062 · 063 · 064 · lhss_001 · 003 · 008 · 009 · 011 · 014 — 14 행 모두 Hertz OK · H12 MBCB.  관찰: 10-14 실행의 실패 14 건 (194 등록 §9-8 이력 · 보충 등록 §9-3 이력) 과 이름이 같다 — 옛 레코드의 전환이 아니라 새 실행이 사례마다 다시 판정한 결과 (등록 §9-8 *"새 214 실행이 사례마다 다시 판정"*).

## 3. 결과 보고 (§9-8 ⑥ · C9)

| 수 | lhs | lhsx | lhss | 합 |
|---|---|---|---|---|
| Hertz 주 타깃 값 상태 (OK · MBCB · f_ion_hertz 숫자) | 106 | 64 | 17 | 187 |
| Hertz 비관통 (f = 0.0 = 물리적 0 · T · √T 빈칸 = ∞ 저장 표현) | 24 | 0 | 3 | 27 |
| Hertz FULL 모형 한계 (주 타깃 HOLD 대상) | 0 | 0 | 0 | **0** |
| Physics FULL 모형 한계 (부록 공란 `NA_MODEL_LIMIT`) | 0 | 8 | 6 | **14** |
| Physics MBCB · H12 MBCB | 7 · 0 | 51 · 12 | 4 · 6 | 62 · 18 |

- 한정: 발사 영수증 rc 0 (입력 대조) ≠ 결과 완료 증서 · Physics 모형 한계 14 는 무작위 결측이 아니다 (q 높은 쪽 — 남은 Physics 행만으로 코호트를 대표한다고 쓰지 않는다).

## 4. §5-7 회귀 — v1.2 배치 (`11fcf91e8`) 대비 · 레코드 수준

원천 = 두 배치의 `merged/<ds>/metrics_flat.csv` (v1.2 = `docs/data/lhs_network194_11fcf91e8/merged/lhs/metrics_flat.csv` · lhsx 같은 자리) · H0 이온 배포값 = v1.2 배포 `docs/data/lhs_release_20261006_v12/lhs_release_20261006_v12.csv` (lhsx 같은 자리) ↔ B7 다시 읽기 칸.  망 단계 열 = `webapp/pipeline_service.py` `NET_MERGE_KEYS` (+ 펼친 자식) ∪ network_dual.* ∪ 채널 판정 · 사유 ∪ 솔버 상태 · 실행 id (리포 정의).  상대 차 = |B7 − v1.2| / max(|B7|, |v1.2|).

| 대조 | lhs | lhsx | 판정 |
|---|---|---|---|
| 케이스 집합 | 130 = 130 | 64 = 64 | 같음 |
| 망 단계 밖 공통 열 386 의 칸 | 50,180 중 49,963 글자 같음 · 다름 217 = `physics_solver_at` 130 (실행 시각) + `warning_count` 87 (+1) | 24,704 중 24,584 · 다름 120 = 64 + 56 | 다른 두 열은 인계 열이 아니다 · `warning_count` +1 = Physics/Hertz 경고 (`webapp/app.py` 3563–3570 · \|σ_P/σ_H − 1\| > 0.5) 가 B7 에서만 켜진 행과 **194/194 일치** (`warning_cause.json` · 선언된 Physics 변경의 결과) |
| B7 에만 있는 열 | 43 = 세대 2 표기 6 · C2-⑥ 합집합 cap 25 · L214 전자 · 열 FULL 상태 · 사유 12 | 46 = 6 · 25 · 14 + `sigma_full_reason_physics` 1 (값 = 모형 한계 사유 8 행) | 전부 선언된 변경 범주 (`reg_detail.json`) |
| H0 이온 상태 쌍 (v1.2 → B7) | NOT_PERCOLATING → 같음 24 · OK → OK 106 | OK → OK 64 | 바뀐 상태 0 |
| **H0 이온 배포값 f_ion_hertz** (17 자리) | 106 대조 · 중앙 2.75e-5 · 최대 **1.5258e-4 (lhs00_123)** · 1.5e-4 초과 1 · 증가 103 · 같음 3 · 감소 0 | 64 대조 · 중앙 5.14e-5 · 최대 **1.5228e-4 (lhsx_026)** · 초과 1 · 증가 64 · 감소 0 | 선언 문턱 1.5e-4 를 2 행이 넘음 (문턱의 1.7 % · 1.5 %) → **Q1** (`tau_vs_v12_summary.json`) |
| H0 전자 σ (인계 열 아님) | 130 전부 증가 · 중앙 0.11 % · p90 0.40 % · 최대 1.41 % | 57 전부 증가 · 중앙 0.09 % · 최대 2.19 % | 관찰 — 선언 목록에 전자 · 열의 크기 범위가 없다 · 원인 미확인 (부호 = 전극 변경과 같은 방향 · 추정) |
| H0 열 σ (인계 열 아님) | 130 증가 · 중앙 0.71 % · p90 2.48 % · 최대 6.78 % | 64 증가 · 중앙 0.54 % · 최대 3.70 % | 같음 |

- 한정: 이것은 원천 (metrics_flat · 다시 읽기 칸) 수준 대조다 — 인계표 수준 대조 (v1.3 인계표 ↔ v1.2 인계표 공통 칸) 는 단계 A 생성 뒤 (생성기 판이 v1.2 와 달라 유도 열이 달라질 수 있다).  v1.2 인계표에 실린 망 값 열은 이온 τ 뿐이다 (전자 · 열 σ · `warning_count` · `physics_solver_at` 는 인계 열 아님).
- 참고: 옛 전극 (가상 전원 · 싱크 g_b = max(100·Σg/n_el, 10·g_max, 1e-6)) 은 모든 간선에서 나온 값이라 망마다 효과 크기가 다르다 (`scripts/network_conductivity.py` 1114–1115 · 세대 1 σ 재현 = git 이력의 옛 모듈뿐).

## 5. 압력 기록 (②a · DESC-06) — 묶음에 없음

- `scripts/lhs_pressure_record.py` 는 침대마다 덱 · LIGGGHTS 로그 (WSL 원자료) 의 압밀 루프 판정 줄을 읽는다 — 받은 묶음에는 원자료가 없다.  metrics_flat 의 `target_pressure_mpa` · `inp.target_press_sim` 은 입력값이지 도달 기록이 아니다 (DESC-06).
- ⇒ 미실행 · WSL 명령 = §6 의 ②a 세 줄 (실행기 `print_followups` 가 받은 manifest 에서 찍은 것 그대로 · `python3` → `$PY`).

## 6. 인계표 v1.3 생성 (단계 A) — 입력 결손 · 미실행

| 입력 | 있나 | 비고 |
|---|---|---|
| 배치 manifest · merged/<ds>/metrics_flat.csv · status.json · seal_audit.json · reread.json | 있음 (묶음) | 경로 결합은 WSL 뿌리에서만 |
| 수확 · union · 설계 | 있음 (리포) | `lhs_release_build.V13_INPUTS` |
| **`merged/{lhs,lhsx}/results` · `merged/lhss/results`** (τ 출처 P0–P4 · `--tau-results`) | **없음** | 케이스 결과 원본 = 1저자 WSL ROOT 에만 (위 README) |
| **압력 기록 3 TSV** (`pressure/<ds>_pressure_record.tsv`) | **없음** | §5 · `--pressure-unverified` 는 1저자 결정 (v1.3 계획 Q2 = 쓰지 않는다) |
| (전체 `--v13` 한 명령을 쓸 때만) `--codex-verdict` GO 판정문 | **없음** | v1.3 배포 GO 판정문은 아직 없다 (Q3) |

WSL 명령 (발사 체크아웃 그대로 · 단계마다 따로 · 화면을 본 뒤 다음):

```bash
cd ~/dem-audit
git rev-parse HEAD                                                     # 35f0327377a4213774010a090df4d224e50d29e1 이어야 (발사 체크아웃)
echo "dirty 줄 수 = $(git status --porcelain --untracked-files=no | wc -l)"   # 0 이어야
PY=/home/yonghoon71/Yonghoon-DEM-DFT/.venv/bin/python3
R=/home/yonghoon71/net194_35f032737_1028; RS=/home/yonghoon71/netsupp20_35f032737_1028
mkdir -p "$R/pressure" "$R/tau" "$RS/pressure" "$RS/tau"
# ②a 완료 압력 기록 — 침대마다 OK 여야 (rc 1 = OK 아닌 침대 → 단계 A 가 거부) · 로그가 덱 폴더의 log* 가 아니면 --log-glob
$PY scripts/lhs_pressure_record.py --cohort /home/yonghoon71/dem-audit/docs/data/area_s2_cohort.tsv --harvest-dir /home/yonghoon71/dem-audit/docs/data/lhs_descriptors_cov_1e09f661d --out "$R/pressure/lhs_pressure_record.tsv"; echo "rc=$?"
$PY scripts/lhs_pressure_record.py --cohort /home/yonghoon71/dem-audit/docs/data/lhsx_descriptors_20260925/_cohort.tsv --harvest-dir /home/yonghoon71/dem-audit/docs/data/lhsx_descriptors_cov_1e09f661d --out "$R/pressure/lhsx_pressure_record.tsv"; echo "rc=$?"
$PY scripts/lhs_pressure_record.py --cohort /home/yonghoon71/dem-audit/docs/data/lhss_descriptors_cov_1e09f661d/_cohort.tsv --harvest-dir /home/yonghoon71/dem-audit/docs/data/lhss_descriptors_cov_1e09f661d --out "$RS/pressure/lhss_pressure_record.tsv"; echo "rc=$?"
# ① τ 진단 표 (진단 전용 · 등록 §5-4 · 인계표에 손으로 잇지 않는다)
$PY scripts/tau_flux.py "$R"/merged/lhs/results/* --tsv "$R/tau/lhs_tau_flux.tsv" --json "$R/tau/lhs_tau_flux.json"; echo "rc=$?"
$PY scripts/tau_flux.py "$R"/merged/lhsx/results/* --tsv "$R/tau/lhsx_tau_flux.tsv" --json "$R/tau/lhsx_tau_flux.json"; echo "rc=$?"
$PY scripts/tau_flux.py "$RS"/merged/lhss/results/* --tsv "$RS/tau/lhss_tau_flux.tsv" --json "$RS/tau/lhss_tau_flux.json"; echo "rc=$?"
# 단계 A 인계표 셋 — (가) 단계 A 만 (배포 묶음 안 만듦 · Q3 권고): CLI 에 단계 A 만 돌리는 옵션이 없어 같은 함수를 직접 부른다
#   (그 함수가 ⓪ 감사 · ⓪b 다시 읽기 · 발사 봉인 · 배치 교차 관문을 먼저 돈다 · 압력 기록은 <ROOT>/pressure/ 에서 찾는다)
D=$(date +%Y%m%d)
$PY -c "import sys; sys.path.insert(0, 'scripts'); import lhs_release_build as L; L.stage_handovers_v13(sys.argv[1], sys.argv[1] + '/handover_v13_' + sys.argv[3], sys.argv[3], supp_batch_root=sys.argv[2])" "$R" "$RS" "$D"; echo "stage A rc=$?"
# 묶음 → 다운로드 폴더 (배치마다 따로 — 같은 이름 겹침 방지)
tar czf ~/net194_35f032737_v13handover_$D.tar.gz -C "$R" "handover_v13_$D" pressure tau
tar czf ~/netsupp20_35f032737_v13handover_$D.tar.gz -C "$RS" pressure tau
cp ~/net194_35f032737_v13handover_$D.tar.gz ~/netsupp20_35f032737_v13handover_$D.tar.gz /mnt/c/Users/Administrator/Downloads/
```

- (나) 등록된 한 명령 (v1.3 계획 §2b · `--v13 --batch-root "$R" --supp-batch-root "$RS" --codex-verdict … --handover-out … --out-dir …`) = 단계 A + 단계 B (WSL 에 배포 묶음 생성) + 대조 — H0 모형 한계 0 이라 단계 B 가 그 관문으로 멈추지 않는다 · `--codex-verdict` 판정문이 필요 (Q3).
- 반입 뒤 (메인): 인계표 → 이 폴더 옆 `s5_v13/` · 인계표 수준 §5-7 대조 (v1.2 인계표 공통 칸) · 등록 §9 결과 칸.

## 7. L214P-02 — `launch_eligibility` 의 manifest git.sha 끝 LF (`scripts/run_network_194_parallel.py` 1140 행)

| 단계 | 실행기 selftest | 비고 |
|---|---|---|
| 기준 트리 (시험 넣기 전) | 139/139 · rc 0 | |
| 시험 먼저 (㊳ 두 검사 · 1140 행 `_HEX40.match` 그대로) | **139/141** · rc 1 — 실패 = ㊳ 둘 뿐: 경계 7 형 중 `40 hex + LF` 만 current · 실제 audit CLI 자격 current (rc 1 = UNSEALED 경로) | 실행 파일 sha256 `359670ff…` |
| 고친 뒤 (`.match` → `.fullmatch` 한 줄) | **141/141** · rc 0 | 실행 파일 sha256 `e250ba1b…` |
| 의존 소비자 `scripts/supp20_input_receipt.py --selftest` (F1 · G1 = `launch_eligibility`) | 123/123 PASS (고친 뒤) | |
| 봉인 | code_fp `2149f873…c3eb` 그대로 — 실행기 = CODE_FILES 32 · HANDOVER_FILES 2 밖 · 대기 지문 없음 | 실행기 sha256 `3220be53…` → `e250ba1b…` (영수증 runner.sha256 = 기록 전용 칸) |

- ㊳ 경계 7 형 = 정확한 40 hex · 다른 유효 40 hex (형식만 · 승인 대조는 F7 · G7 몫) = current / + LF · + CRLF · + 공백 · + NUL · 39 hex = invalid (git.sha 문제 한 줄) · 원문 SHA 를 strip 하지 않는다.
- Codex S1 반례 (두 manifest SHA + LF · 승인값 생략 → rc 0) 의 경로: 영수증 F1 · G1 이 같은 함수를 부른다 (`scripts/supp20_input_receipt.py` 338–339) → 형식에서 거부될 것 — 영수증 전체 rc 재현은 하지 않았다 (**미확인**).
- 같은 부류 관찰 (고치지 않음 · 반례 시험 안 함): 같은 함수의 `_HEX64.match` 1128 · 1137 · 1159 · 1161 행 (code_hashes · handover_code_hashes · cohort_tsv_sha256 · raw_sha256_table_sha256 값) 도 끝 LF 를 받는다 — 뒤 단계의 같음 대조가 막는 구조로 보인다 (추정) → Q5.
- 원장 `L214P-02` 상태 변경 = 메인 (반입 뒤 본 가지 커밋으로 claimed_fixed · Codex 확인 전 verified 아님 — `docs/reviews/findings.json`).

## 8. 1저자 결정 필요

1. **[§5-7] Q1 — H0 이온 배포값 2 행이 선언 문턱을 넘는다.**  194 등록 §5-7: *"허용되는 다름은 선언된 변경뿐: 전극 정확 Dirichlet (H0 σ 상대 ≤ 1.5e-4 · 설계 기록 §1) … 그 밖의 차이는 보고하고 원인을 밝힌 뒤에만 싣는다."* · 설계 기록 §1 (`docs/reviews/gen2_network_design_20261006.md`): *"배포값 변화 ≤ 1.5e-4 (194 행 5–6 째 자리)"*.  실측 lhs00_123 1.5258e-4 · lhsx_026 1.5228e-4 (비교한 관통 170 행 중 나머지 168 행 ≤ 1.35e-4 · 증가 167 · 같음 3 · 감소 0 = 전극 변경과 같은 방향 · 비관통 24 = 둘 다 0.0).  설계 기록의 *"194 행"* 계산 원천을 리포에서 찾지 못했다 (`docs/data/gen2_design_20261006/c1/lhs194_estimates.py` = H1 · H12 추정 · 전극 아님 · 전극 실측 = 설계 기록 §3 real_14 ×1.0000219) — 문턱 근거 **미확인**.  선택: (가) 1.5e-4 를 "5–6 째 자리" 의 어림 서술로 보고 두 행을 선언된 전극 변경으로 싣는다 (한정어) · (나) 싣기 전에 두 침대에서 원인 확인 (같은 덤프 · 옛 모듈 ↔ B7 모듈의 H0 간선 비트 같음 확인 — WSL) · 권고: **(나)** — 등록 글자 (*"원인을 밝힌 뒤에만"*) 그대로 · 배포 HOLD 중이라 일정 영향 없음.
2. **[§9-8 ⑤] Q2 — 배포 HOLD 의 근거.**  위 README: *"v1.3 배포 = 따로 HOLD · H0 모형 한계 행"* · 등록 §9-8 ⑤: *"v1.3 주 타깃 배포 HOLD (`lhs_release_build.v13_primary_model_limit_problems` — 실제 빌드 거부 …)"*.  이번 기록의 H0 모형 한계 = 0 행 (관문 문제 0) — 그 관문으로는 HOLD 가 걸리지 않는다.  Codex S2 §4 는 *"v1.3 주 학습 인계·FULL 모형 한계·S3 — 기존 별도 판정 유지. 이번 GO로 해제하지 않음"*.  권고: 배포 HOLD 그대로 (1저자 11-01) — 푸는 조건을 "Q1 처리 · 압력 기록 OK · 단계 A 인계표 · 인계표 수준 회귀 뒤 Codex v1.3 배포 확인" 으로 적는다.
3. **[인계표] Q3 — 단계 A 경로.**  (가) 단계 A 함수만 (§6 · 인계표 셋 · 배포 묶음 없음 · `--codex-verdict` 불요) · (나) 등록된 한 명령 (v1.3 계획 §2b · WSL 에 배포 묶음까지 · GO 판정문 필요 — 재검증 7 GO = 194 발사 범위 · S2 GO = 발사 확인 범위 · 둘 다 v1.3 배포 GO 아님).  권고: **(가)** (*"배포 HOLD · 생성만"* 과 같은 뜻).
4. **[압력] Q4 — 압력 기록에 OK 아닌 침대가 나오면.**  권고: 단계 A 를 돌리지 않고 화면 그대로 보고 (`--pressure-unverified` 쓰지 않음 · v1.3 계획 Q2).
5. **[원장] Q5 — 같은 부류 `_HEX64.match` 4 행을 새 P3 로 등재하나.**  권고: 등재 (관찰 · P3) · 고칠지는 L214P-02 의 Codex 확인 때 함께 묻는다.

## 9. 관찰 (결정 불요)

- 실행기 `print_followups` 의 ③ 묶음 이름이 배치와 무관하게 `net194_<sha>_<날짜>` 로 고정 — 보충 배치의 ③ 를 같은 날 돌리면 194 묶음을 덮어쓴다 (코드 미수정 · §6 명령은 배치마다 다른 이름).

## 10. 산출 · 재현

| 파일 | 내용 |
|---|---|
| `s5_summary.json` | §5-1 · §5-2 (등록 §4 스니펫 값) · §5-3 · 같은 함수 관문 · τ 상태 · 모형 한계 · 채널 |
| `tau_status_by_case.tsv` | 214 행 · 상태 · 사유 · 표지 · 띠 규칙 (값 칸 없음 — 인계표 아님) |
| `regression_v12_summary.json` · `regression_v12_nonnet_diffs.tsv` | §5-7 망 밖 열 대조 · 다른 칸 전부 (337 = 217 + 120) |
| `tau_vs_v12_summary.json` · `reg_detail.json` · `warning_cause.json` · `blank_rule.txt` | H0 이온 배포값 · 새 열 범주 · 부호 · 경고 원인 · §9-8 ④ 규칙 |
| `tools/` | 위 산출을 만든 도구 일곱 (읽기 전용 · 리포 함수 호출) |
| `q1_records_summary.json` · `q1_electrode_by_case.tsv` (§11-1 · `tools/s5_q1_records.py`) | 입력 · 띠 · 풀이 경로 같음 · 저장 칸 · 가지 동조 · 띠 비율 관계 · 두 행 (TSV = 상대 차 · 칸만 — σ 값 칸 없음) |
| `q1_settle_validation.json` (§11-1 (g) · `tools/s5_q1_validate_real14.sh` + `tools/s5_q1_validate_fixtures.py`) | 확정 도구 `tools/s5_q1_electrode_settle.py` 의 real_14 여덟 경우 (기대 rc 와 같음 8/8) |

```bash
X=$(mktemp -d); mkdir "$X/x194" "$X/xsupp"; F=docs/data/lhs_network214_35f032737_20261030
tar xzf $F/net194_35f032737_1028_20261030_records.tar.gz -C "$X/x194"; tar xzf $F/netsupp20_35f032737_1028_20261030_records.tar.gz -C "$X/xsupp"
T=$F/s5_judgment/tools; O=$(mktemp -d)
python3 -I $T/s5_records_judge.py --repo "$PWD" --root194 "$X/x194" --rootsupp "$X/xsupp" --out "$O"
python3 -I $T/s5_regression_v12.py --repo "$PWD" --root194 "$X/x194" --out "$O"
python3 -I $T/s5_tau_vs_v12.py --repo "$PWD" --root194 "$X/x194" --out "$O"
python3 -I $T/s5_reg_detail.py --repo "$PWD" --root194 "$X/x194" > "$O/reg_detail.json"
python3 -I $T/s5_warning_cause.py --repo "$PWD" --root194 "$X/x194" > "$O/warning_cause.json"
python3 -I $T/s5_blank_rule.py --root194 "$X/x194" --rootsupp "$X/xsupp" > "$O/blank_rule.txt"
python3 -I $T/s5_followups.py --repo "$PWD" --root194 "$X/x194" --rootsupp "$X/xsupp"      # §6 명령의 원천 (cd 줄 · python3 는 WSL 에 맞게)
Y=$(mktemp -d); tar xzf docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/net194_tau_sources_20261006.tar.gz -C "$Y"
python3 -I $T/s5_q1_records.py --repo "$PWD" --root194 "$X/x194" --v12src "$Y" --out "$O"          # §11-1 (b) (c)
bash $T/s5_q1_validate_real14.sh "$PWD" "$(mktemp -d)/v" "$X/x194/manifest.json"                   # §11-1 (g) — 여덟 경우 · 수 분
```

## 11. 1저자 11-02 *"다 권고대로 해봐"* — Q1–Q5 처리

§8 의 Q1–Q5 = 권고대로 비준 (1저자 11-02).  배포 HOLD 그대로 · 받은 자료는 읽기만 · 원장 (`docs/reviews/findings.json`) · CLAUDE.md 는 이 묶음에서 건드리지 않는다 (등재 = 메인).

### 11-1. Q1 — H0 이온 1.5e-4 초과 두 행: 기록으로 가를 수 있는 데까지

**(a) 1.5e-4 의 출처 = 설계 침대 둘의 관측 최댓값을 반올림한 수 — 유도한 상한도 194 행 계산도 아니다**

| 자리 | 글자 · 값 |
|---|---|
| 194 등록 §5-7 (`docs/reviews/lhs_network_batch_registration_20261007_g2.md` 294 행) | *"전극 정확 Dirichlet (H0 σ 상대 ≤ 1.5e-4 · 설계 기록 §1)"* |
| 설계 기록 §1 (`docs/reviews/gen2_network_design_20261006.md` 15 행) = 원본 요약 `docs/data/gen2_design_20261006/c1/DECISIONS_C1.md` 5 행 | *"배포값 변화 ≤ 1.5e-4 (194 행 5–6 째 자리)"* |
| 인계 생성기 열 사전 `CAVEAT_TAU_NET` (`scripts/lhs_design_dataset.py` 1737 행 · 봉인 인계 도구 · 세대 2 구현 커밋 a0a24c538 에서 들어옴) | *"배포값 변화 ≤ 1.5e-4 = 5–6 째 자리"* |
| 설계 근거 숫자 = 두 침대의 `dirichlet_over_adaptive` − 1 (`docs/data/gen2_design_20261006/c1/net_beds_case15.json` · `net_beds_real14.json`) | case15 (얇은 모서리 침대 · n_top 45): H0 FULL 7.66e-5 · CF0 **1.545e-4** · CF2 1.532e-4 / real_14: H0 FULL 2.15e-5 · CF0 2.25e-5 |
| 194 행 전극 효과 계산 | 리포에 없음 — `docs/data/gen2_design_20261006/c1/lhs194_estimates.py` 머리글 *"raw contacts are not in the repo"* · 그 도구는 H1 · H12 추정만 (전극 없음) |
| git 이력 (문구 `≤ 1.5e-4` 를 넣은 커밋) | 같은 날 (10-06) 셋 — 생성기 문구 a0a24c538 · 설계 기록 c13da95a3 · 194 등록 9d25757dc · 근거 자료 폴더 (`docs/data/gen2_design_20261006/`) 에 194 침대 전극 계산 없음 |

- 최댓값 1.5447e-4 (case15 CF0) 자체가 1.5e-4 보다 크다 · H0 FULL 만 보면 설계 최댓값은 7.66e-5 였다.

**(b) 받은 기록이 말하는 것** (도구 `tools/s5_q1_records.py` · 산출 `q1_records_summary.json` · `q1_electrode_by_case.tsv` — σ 값 칸 없음 · 상대 차 · 저장 칸만)

| 검사 | 결과 | 뜻 |
|---|---|---|
| 입력 같음 — 원 덤프 sha256 (atom · contact · mesh · deck) · type_map · contact_scan (v1.2 merged status ↔ B7) | 194/194 같음 | 같은 원자료 · 구문 분석 도구 (`scripts/parse_liggghts.py` · `scripts/analyze_contacts.py`) 도 v1.2 커밋 ↔ B7 바이트 같음 |
| 띠 같음 — 이온 Hertz 띠 규칙 · 띠 비율 (v1.2 dual ↔ B7 row_cells) | 170/170 같음 (L0) | 경계 집합 크기 같음 |
| 풀이 경로 — v1.2 옛 모듈 (관통 N + 2 > 30,000 → CG) · B7 증서 method | v1.2 직접해 104 · CG 66 (문턱 근처 0) / B7 직접해 116 · CG 54 | 두 행은 두 배치 모두 직접해 (v1.2 관통 ≈ 11,228 · 11,613 · B7 spsolve) |
| 저장 해상도 | σ_ratio = 소수 8 자리 (두 배치 · 칸 격자 어긋남 최대 1.75e-8 칸) | 기록 차 k 칸 → 참 차 ∈ ((k−1), (k+1)) 칸 |
| FULL 방향 (170) | 증가 167 · 같음 3 · 감소 0 | |
| 가지 동조 (세 가지 모두 3 칸 이상인 135 행) | 부호 셋 같음 135/135 · CF/FULL 중앙 0.982 (p05 0.968 · p95 1.109 · 범위 0.845–2.71) · 협착-only/FULL 중앙 1.007 (0.72–1.016) | 셋이 같이 움직인다 = 공통 경계층 (전극) 의 꼴 · 협착만 바뀌면 CF 가, bulk 만 바뀌면 협착-only 가 가만있어야 한다 |
| 띠 비율과의 관계 (FULL 3 칸 이상 164 행) | Spearman +0.892 · log–log 기울기 2.14 · R² 0.836 · 잔차 sd 0.256 (자연로그) | 옛 가상 전극의 경계 저항 몫이 얇은 침대 (띠 비율 큼) 에서 큰 것과 맞다 — 일관성 (원인 확정 아님) |

**(c) 두 행**

| 행 | 기록 (v1.2 → B7 · H0 이온 σ_ratio) | 저장 칸 (FULL · CF · 협착-only) | 읽음 |
|---|---|---|---|
| lhs00_123 (lhs · 띠 0.0638 · n_bottom 1,385 · n_top 165) | FULL 6.553e-05 → 6.554e-05 · CF 0.00086916 → 0.00086918 · 협착-only 7.102e-05 → 7.102e-05 | **1** · 2 · 0 | 1.5258e-4 = 저장 **한 칸**의 크기 (1e-8 / 6.554e-5) — 참 차 ∈ (0, 3.05e-4) · 같은 침대 CF ∈ (1.15e-5, 3.45e-5) · 협착-only < 1.41e-4 · 다른 행의 가지 비 범위를 빌리면 FULL ≤ 4.1e-5 · 띠 적합 예측 1.8e-5 (**추정** — 측정 아님) |
| lhsx_026 (lhsx · 띠 0.157 = lhsx 64 중 1 위 · n_bottom 1,024 · n_top 994) | FULL 0.42381246 → 0.42387701 · CF 1.30440817 → 1.30460134 · 협착-only 0.64031046 → 0.64040901 | 6,455 · 19,317 · 9,855 | 실제 변화 1.5228e-4 (해상도 위) · 세 가지 1.52 · 1.48 · 1.54e-4 같은 부호 · lhsx 에서 Δ 1 위 = 띠 비율 1 위 · 띠 적합 예측 1.24e-4 · 잔차 +0.21 (z +0.82 · 164 중 14 위) = 흩어짐 안 |

**(d) 판정** — 기록으로 닫힌 것: 입력 · 띠 · 풀이 경로가 같다 · lhs00_123 의 1.5258e-4 는 저장 해상도 (한 칸) 다 · lhsx_026 의 1.5228e-4 는 실제 변화이고 전극 변경의 꼴 (세 가지 동조 · 띠 비율 추세 안) 이다.  기록으로 못 닫는 것: **H0 간선 · 노드가 두 세대에서 같은지** (설계 기록의 주장 · 194 침대 실측 없음) — 그래서 *"차이 = 전극뿐"* 은 아직 **추정**이다.  → 아래 WSL 확정 명령.

**(e) WSL 확정 명령** (읽기 전용 · 쓰기 = `<새 빈 폴더>` 안만 · 경로 = 자리표시 · 침대당 수 초) — 파일로 저장 → 자리표시를 바꾼 뒤 `bash 파일` (자리표시가 남으면 문법 오류로 아무것도 돌지 않는다 · 셸에 붙여 넣지 않는다 — `exit` 가 셸을 닫는다)

```bash
B7=<발사 체크아웃 — 승인 핀 B7 · 깨끗>
MAIN=<이 판정 문서가 있는 리포 체크아웃>
R=<194 배치 ROOT>
PY=<B7 manifest 의 python — 3.12.3 · numpy 2.5.2 · scipy 1.18.1>
Q=<새 빈 폴더>
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
test "$(git -C "$B7" rev-parse HEAD)" = 35f0327377a4213774010a090df4d224e50d29e1 || { echo '⛔ B7 체크아웃 아님'; exit 1; }
test "$(git -C "$B7" status --porcelain --untracked-files=no | wc -l)" -eq 0 || { echo '⛔ dirty'; exit 1; }
test ! -e "$Q" || { echo '⛔ Q 가 이미 있다'; exit 1; }
mkdir -p "$Q/v12" && tar -xzf "$MAIN/docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/net194_tau_sources_20261006.tar.gz" -C "$Q/v12"
cd "$Q" || exit 1
for C in lhs00_123 lhsx_026; do
  V12="$Q/v12/cases/$C/work/results/$C"
  "$PY" -I "$MAIN/docs/data/lhs_network214_35f032737_20261030/s5_judgment/tools/s5_q1_electrode_settle.py" \
      --repo "$B7" --case-dir "$R/cases/$C/work/results/$C" \
      --v12-dual "$V12/network_conductivity_dual.json" --v12-prov "$V12/network_provenance.json" \
      --b7-manifest "$R/manifest.json" --b7-reread "$R/reread.json" --case "$C" --out "$Q/out_$C"
  echo "$C rc=$?"
done
tar czf "$Q/q1_settle_$(date +%Y%m%d).tar.gz" -C "$Q" out_lhs00_123 out_lhsx_026      # 이 묶음 + 화면을 메인에 반입
```

- 도구가 하는 일: B7 실행 자신의 입력 (`atoms.csv` · `contacts.csv` · `mesh_info.json` · `input_params.json`) 으로 B7 코드 (`_run_all_networks(contact_mode='hertzian')`) 를 안에서 부르고, H0 이온 망의 세 가지 풀이마다 **같은 망 · 같은 간선 저항**을 옛 전극 (`docs/data/gen2_design_20261006/c1/netsolve.py` `solve_adaptive` — 옛 g_b 규칙 재구현) 과 새 전극 (B7 값 + `solve_dirichlet` 교차 확인) 으로 푼다.  검사: A0 입력 지문 = B7 provenance · A 안에서 부른 값 = B7 기록 (저장 반폭 0.5e-8 안) · A_code 불러온 리포 모듈 sha256 = 봉인 code_hashes · A_run provenance run id = reread run id ∧ reread 표 값 = dual 기록 · B 같은 망의 옛 전극 값 = v1.2 기록 · case-dir 안 바뀜.
- 결과 전 기대 (**추정**): 두 행 INCLUDE · lhs00_123 Δ_전극 ≈ 1e-5–4e-5 · lhsx_026 Δ_전극 ∈ (1.5226e-4, 1.5231e-4) (기록 차 ± 한 칸).

**(f) 결과의 뜻 — 싣는가 · 보류하는가**

| 도구 결과 (`settle_<case>.json` · rc) | 뜻 | 처리 |
|---|---|---|
| INCLUDE (rc 0) — A0 · A · A_code · A_run · B 모두 참 | 같은 입력 · 같은 봉인 코드 · 같은 망에서 v1.2 → B7 차이 = 전극 모형뿐 · 정확한 Δ = `rows.full.d_electrode` | **싣는다** — 등록 §5-7 *"그 밖의 차이는 보고하고 원인을 밝힌 뒤에만 싣는다"* 의 원인 = 선언된 전극 변경 (Δ 와 1.5e-4 대비를 결과 칸에 적는다 · lhsx_026 은 전극만이어도 1.5e-4 를 넘는다 → (h) 문구 정정) |
| HOLD (rc 3) — A0 · A · A_code · A_run 중 거짓 | B7 기록을 그 입력 · 코드로 다시 만들지 못한다 = 원인을 가를 바탕이 없다 | **보류** — 입력 자리 · 체크아웃을 확인하고 다시 (화면 그대로 보고) |
| HOLD (rc 3) — B 거짓 | 같은 망을 옛 전극으로 풀어도 v1.2 값이 안 나온다 = 전극 밖의 차이 (간선 · 노드 · 띠) 가 있다 | **보류** — 원인 조사 (간선 대조) · 1저자 보고 |
| INCONCLUSIVE (rc 4) | v1.2 가 CG 경로 (옛 반복해 오차) — B 를 판정하지 않는다 | 두 행은 해당 없음 (관통 < 30,000) |
| rc 2 | 입력 결손 · `--out` 이 비어 있지 않음 | 자리 확인 |

**(g) 도구 검증 (이 컨테이너 · 커밋된 real_14 덤프)** — `tools/s5_q1_validate_real14.sh` (`tools/s5_q1_validate_fixtures.py` 보조) · 산출 `q1_settle_validation.json`

| 경우 | 픽스처 | 결과 (기대) |
|---|---|---|
| cg | v1.2 기록 = 11fcf91e8 모듈 그대로 (real_14 관통 32,234 → CG 경로) | INCONCLUSIVE rc 4 (4) |
| inc · incfull | 같은 모듈의 CG 문턱만 끈 사본 (직접해) + `--assume-v12-direct` (검증 전용) · incfull = + 받은 B7 manifest 의 code_hashes · reread 픽스처 | INCLUDE rc 0 (0) · A_code = 불러온 봉인 모듈 8 개 모두 = B7 manifest |
| negA · negA0 · negB · negRun · negCode | B7 기록 +3 칸 · 입력 지문 0 · v1.2 기록 +3 칸 · run id 다름 · 망 코드 지문 0 (사본) | HOLD rc 3 (3) 다섯 |

- 값: B7 CLI = 0.02102106 · 안에서 부른 B7 = 0.0210210554 (기록과 같은 칸) · 옛 모듈 기록 (CG · 직접해 사본 둘 다) = 0.0210206 · 같은 망 옛 전극 = 0.0210206038 · Δ_전극 FULL **2.1488e-5** = 설계 기록 §3 (×1.0000219) · `net_beds_real14.json` 과 같다 · netsolve Dirichlet ↔ B7 상대 7e-15.

**(h) 관찰 · 1저자 확인**

- 열 사전 문구 반례: 인계 생성기 `CAVEAT_TAU_NET` 의 *"배포값 변화 ≤ 1.5e-4"* 는 lhsx_026 (1.5228e-4 · 해상도 위) 에서 원인과 무관하게 틀린다 (배포값 변화를 말하는 문장이다).  고치면 봉인 인계 도구 지문 (`scripts/lhs_design_dataset.py` d1815155…) 이 바뀌어 단계 A 의 manifest 대조가 막힌다 → **1저자 결정 (§11-6 Q6)**.
- v1.2 의 CG 66 행: 옛 모듈의 `cg(…, tol=1e-8)` 이 scipy 1.18.1 (두 배치 manifest) 에서 TypeError (`tol` 은 1.14 에서 빠짐) → `cg(…, atol=1e-8)` (기본 rtol 1e-5) 로 풀렸다.  크기: 설계 침대 module_check real_14 −3.1e-9 · case15 −1.3e-7 · 이 컨테이너 real_14 = 직접해 사본과 같은 칸 → 1.5e-4 판단에 영향 없음 · 두 행은 직접해 · B7 은 rtol 1e-10 + 증서 (관찰 · 결정 불요).

### 11-2. Q2 — v1.3 배포 HOLD 그대로 · 해제 조건

- 근거: Codex S2 §4 (`docs/reviews/codex_lhs214_relaunch_review_20261030/codex_review_lhs214_relaunch_20261030.md` 193 행) *"v1.3 주 학습 인계·FULL 모형 한계·S3 — 기존 별도 판정 유지. 이번 GO로 해제하지 않음"* · 같은 문서 §3-3 *"실제 F/G/H, 완료 audit, 등록 §5, 배포 관문이 아직 수행되지 않았다는 사실을 바꾸지 않는다."*  §9-8 ⑤ 주 타깃 관문은 문제 0 이므로 HOLD 의 근거는 그 관문이 아니라 이 판정 유지다.
- 해제 조건 (모두 · 이 순서):

| # | 조건 | 닫는 기록 |
|---|---|---|
| 1 | Q1 — WSL 확정 명령 (§11-1 (e)) 두 행 INCLUDE · 결과 반입 · 등록 §5-7 결과 칸 (보고 + 원인) | `settle_<case>.json` 둘 |
| 2 | 압력 기록 214 OK (lhs 130 · lhsx 64 · lhss 20 · `scripts/lhs_pressure_record.py` rc 0 셋) — §11-4 규칙 | 압력 TSV 셋 |
| 3 | 단계 A (§11-3) rc 0 — 배치 관문 ⓪ · ⓪b · 교차 + 생성기 관문 (⑤F1 · ⑥R1–R3 · ⑦A1–A5 · τ 출처 P0–P4) 통과 · 인계표 셋 반입 | 인계표 셋 + 화면 |
| 4 | 인계표 수준 §5-7 회귀 (v1.3 ↔ v1.2 인계표 공통 칸) — 선언된 변경 밖 차이 0 또는 원인 기록 | 대조 표 |
| 5 | 열 사전 문구 (§11-1 (h)) 처리 결정 | 1저자 Q6 |
| 6 | Codex v1.3 배포 GO 판정문 (배포 관문 `--v13` 의 `--codex-verdict` 입력) — 재검증 7 GO = 194 발사 범위 · S2 GO = 발사 확인 범위 · 둘 다 배포 GO 아님 | 판정문 |
| 7 | 1저자 배포 승인 | 채팅 · 진행 기록 |

- 해제 전에는 단계 B (배포 묶음) · ZIP · 전달 없음.  S3 (봉인 창) = 별도 HOLD — 이 조건으로 풀지 않는다.

