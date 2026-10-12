# Codex 짧은 검토 요청 — 보충 20 지원 (세대 2 접촉망 · v1.3 = 194 + 보충 20) (2026-10-12 · 발송 = 1저자 10-12 · 리뷰 핀 `b429c3c1d`)

> 근거: Codex 재검증 6 판정 Q9 (`docs/reviews/codex_review_gen2_network_reverify6_20261011.md` — *"194 + 보충 20 두 배치 권고 · 짧은 추가 검토 가능"* · 최소 목록 =
> 고정 집합 · 같은 세대 교차 · 관측 강제 · 배치별 완결 · 결합 214 고유 · 회귀) · 재검증 7 GO 의 범위 (`docs/reviews/codex_review_gen2_network_reverify7_20261012.md` —
> 핀 `3cedd40a5` 의 **기존 194** 발사 승인 · 사전 점검 단계 · 보충 20 / 214 배포 GO 아님).
> 1저자 10-12 **(나)** — 보충 지원 구현 + 이 짧은 검토 먼저 → 194 · 보충 20 **두 배치 같은 날 연달아** 발사 → v1.3 한 번에.  Q4 = (가) `lhss` 별도 데이터셋 ·
> Q5 = (가) 194 와 같은 수확기 판 `1e09f661d` 로 재수확 + r2 키별 대조 · Q6 = (가) lhss 배포 = lhs 와 같은 132 열 · 부피분율 규칙 행 하중 빈칸.
> **리뷰 핀** = 이 요청서를 담은 커밋 (발송 때 `git rev-parse HEAD` 로 적는다) = **`b429c3c1d`** (10-12 발송 · 1저자) · **기준** = `3cedd40a5` (재검증 7 핀).

## 1. 바뀐 것 (기준 → 리뷰 핀 · 봉인 32 무변경 · `code_fp e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71`)

| 단위 | 커밋 | 파일 | 무엇 | 시험 (고치기 전 → 뒤) |
|---|---|---|---|---|
| U1 실행기 | `28492841f` | `scripts/run_network_194_parallel.py` (봉인 밖) | 등록 집합 `supp20` (20 쌍 · ids_sha256 `991cf115…` · 커밋된 lhss 수확 폴더 열거 = production194 규칙) · `PRODUCTION_SETS` = production194 · supp20 = import 관측 필수 (preflight · audit) · 후속 `--expect-set supp20` · `COHORT_SPECS['lhss']` (`--cohorts` 기본 lhs,lhsx 그대로) | 124/126 → 130/130 |
| U2 다시 읽기 | `28492841f` | `scripts/g2_network_reread.py` (HANDOVER) | `--expect-set supp20` 합성 양성 · 상세 계약 · 결손 / 후막 반례 · 문구 (sha256 `248ee5c0…` → 바뀜) | 고치기 전 실행기 1 실패 → 30 통과 |
| U3 설계 어댑터 | `74a44aa12` · `b9ee7ac97` | `scripts/lhss_design_adapter.py` · `docs/data/lhss_design_adapted_20261012.csv` | lhsx `adapt_row` 재사용 (사본 없음) · 설계 sha256 고정 · 후막 · 결손 · 중복 · ins_scale ≠ 1 거부 · 본 하중 열 (Q6 (가) · 2mAh_fixed 2.0 = 생성기 기본 하중 · volfrac_free 빈칸 · 규칙 ↔ pdd_SE (SE_SPLIT 0.30) ↔ am_pct 70 대조) · 20 × 40 | 0/22 → 23/23 → 22/27 → 27/27 |
| U4 인계 생성기 | `8c19276ca` | `scripts/lhs_design_dataset.py` (HANDOVER) | 열 사전 — lhss_* 17 뜻 (lhsx 와 이름만 같은 열은 그 뜻) · 하중 열 뜻 · 원천 문구 · 배포에 없는 인계표 열 참조 표지 | 385/388 → 389/389 |
| U5 배포 생성기 | `b429c3c1d` (리뷰 핀) | `scripts/lhs_release_build.py` · `scripts/test_lhs_release_v13.py` | 데이터셋 셋 · 배치 둘 (`V13_BATCHES`) · 배치 뿌리 둘 필수 · 배치마다 자기 등록 집합 관문 · 교차 · 결합 · ML 표 `network_batch` · 하중 빈칸 코드 `NA_NOT_DESIGN_INPUT` · 재적합 214 + 194 참고 줄 · README · 그림 · check_v13 두 뿌리 다시 · CLI `--supp-batch-root` | 55/207 → 234/234 (자체 selftest 31/31) |

## 2. 최소 목록 (재검증 6 Q9) ↔ 구현

| 최소 목록 | 구현 (함수 · 시험) |
|---|---|
| 고정 집합 | 실행기 `REGISTERED_ID_SETS['supp20']` · `registered_id_set` (커밋된 수확 폴더 열거 → 수 · 코호트 · 지문) · 배포 관문 = 감사 행 · 다시 읽기 상세가 supp20 (V21j 19 행 · 다른 집합 거부) · 등록 문서 `docs/reviews/lhs_network_batch_registration_20261012_supp20.md` §2 |
| 같은 세대 교차 | `v13_cross_batch_problems` (다른 위치 · manifest seal.code_fp 같음 · 기대 세대 g2 · 발사 sha 다름 = 경고) · `v13_combined_problems` (σ₀ · T · 기준 한 값 · 전 행 세대 섞임 · 공유 열 정의 같음 — 설계 열은 '원천 = …' 꼬리 뺌) — V21d · d2 · j |
| 관측 강제 | 실행기 preflight · audit (`production_observation_problem` → 등록 생산 집합 둘) · 배포 `V13_IMPORT_OBS_REQUIRED` = 실행기 `PRODUCTION_SETS` (V21a 사본 표류) · 보충 관측 끔 · 관측 객체 없음 = 거부 (V21j) |
| 배치별 완결 | `v13_prepare_batches` — 배치마다 manifest g2 · 원천 (manifest 코호트 = 그 배치 데이터셋 정확히) · 발사 봉인 · ⓪ 감사 · ⓪b 다시 읽기 (`expect_set` = 그 배치) · check_v13 = 두 뿌리 다시 판정 (`v13_batch_gate_recheck`) — 기존 V16–V20 (194 변이 · 보충 정상) + V21j (보충 변이 · 194 정상) |
| 결합 214 고유 | `v13_batch_roots` (보충 없이 · 같은 뿌리 = 거부) · `v13_composition` (실제 = 셋 전부) · `v13_combined_problems` ① ID 교집합 공집합 · 고유 = 행 합 · ML 표 `dataset` · `network_batch` (V21f) |
| 회귀 | 기존 194 행 주 표 · 부록 · 열 사전 = 보충 없이 같은 명세로 만든 것과 **바이트 같음** (V21g) · 재적합 = 214 + 194 만 참고 줄 `reference_without_supp` (V21i — 원 행 불변과 요약 변화 구분) · 기존 시험 전부 (V12–V20 은 정상 보충 배치를 붙여 214 로 돈다) |

## 3. 자체 검토 — 알고 있는 한계 (판단 부탁)

1. **등록 집합 supp20 은 r3 수확 반입 뒤에만 세워진다** — 그 전에는 보충 계획이 등록 생산이 아니라서 실행기 사전 점검이 관측을 강제하지 않는다 (production194 와 같은 성질 · U1).  최종 차단 = 배포 관문 (감사 관측 판정이 `registered_id_set('supp20')` 필수 · 못 세우면 문제).  시험은 합성 20 파일 폴더를 시험 프로세스 안에서만 끼운다.
2. **같은 발사 커밋은 경고만** — 강제는 같은 봉인 지문 (code_fp) · 기대 세대.  등록 §4 = 같은 발사 커밋 (다르면 §8 이탈 기록).
3. **하중 빈칸 규칙 = am_pct 경계** (100·(1 − `lhs_supp_design.SE_SPLIT`) = 70) — 설계 규칙의 정본 경계를 읽는다 (사본 없음) · 130 (AM 70–95 · 전부 2.0) · 64 (< 70 · 열 없음) 와 같은 규칙 · 어댑터가 규칙 표지 ↔ pdd_SE ↔ am_pct 를 원천에서 대조.
4. **열 정의 교차의 설계 열** — 뜻 끝의 '원천 = <설계 CSV>' 꼬리는 데이터셋마다 달라 떼고 비교한다 (나머지 출처 · 판정 · 주의는 그대로).  v1.2 lhs · lhsx 공유 241 열은 전부 같았다.
5. **실제 lhss 원천 (r3 수확 · union · 보충 세대 2 배치) 은 아직 없다** — 이 검토의 시험은 합성 lhss 인계표 (lhs · lhsx 행에서 ID · 출처 열만 바꿈) 로 경로 · 관문을 돈다 (값 아님).
6. **자기 결함 `SELF-106`** — v1.3 계획 §2-4 의 컨테이너 `--v13-check` rc 0 은 G2RR3-01 뒤 거짓 (배치 뿌리 재판정) → 같은 커밋에서 정정 표지 · 대조는 WSL.
7. 재검증 7 의 한정 (S0b 12 자리 접두 · 평면 τ 최상위 칸 · case15 fixture) 은 그대로 · 이 diff 는 그 함수들을 건드리지 않았다.
8. **옛 탐침 호환** — 재검증 3–5 의 배포 관문 탐침 (`release_gate.py` · `r5_release_contract.py` · `r5_release_real_binding.py` · `release_gate_detailed.py`) 은 `build_v13(…, batch_root=…)` 만 부른다 → 이 핀에서는 `--supp-batch-root` 결손으로 **먼저** 거부된다 (그 탐침이 겨눈 194 관문 판정에 닿기 전).  같은 판정을 보려면 탐침에 정상 보충 배치 (`supp_batch_root=` · 시험의 `make_supp_batch_root` 꼴) 를 붙인다 — 기존 시험 V12–V20 이 그렇게 돈다.  `v13_batch_gate_problems(root)` · `v13_batch_gate_files(root)` 의 한 인자 호출은 그대로 (기본 등록 집합 production194).

## 4. 질문

- **Q1** 같은 발사 sha 를 강제할까 (지금 = 같은 code_fp 강제 · 다른 sha 는 경고)?
- **Q2** 열 정의 교차에서 설계 열의 원천 꼬리를 떼는 규칙이 맞나 (설계 열 정의 본문은 같아야 · 원천 경로만 다르다)?
- **Q3** 하중 열 (Q6 (가)) — 역할 X_DERIVED (하중 규칙 표지 = am_pct 의 재표현) · 빈칸 코드 `NA_NOT_DESIGN_INPUT` 이 ML 계약으로 충분한가?
- **Q4** 재적합 = 214 관통 행 (등록된 두 식 · 규칙 그대로) + 194 참고 줄 — 재검증 6 의 "214 재적합 요약은 달라질 수 있다" 와 맞나?
- **Q5** 최소 목록에서 빠진 것 · 이 diff 로 194 발사 GO (재검증 7) 의 근거가 약해진 곳이 있나?  두 배치 발사 · v1.3 배포 GO 조건을 적어 달라.
- **Q6** 등록 §2 의 재수확 지문 (원자료 sha256 표 · 코호트 TSV sha256) 은 r3 수확 반입 뒤에 채운다 (값은 이 diff 와 무관 · 실행기 `registered_id_set('supp20')` 이 커밋된 수확 폴더를 열거해 지문과 맞대고 · 사전 점검 dry-run 이 입력 지문을 찍는다).  그 채움 + 1저자 등록 비준 + 발사 핀 사전 점검 통과로 두 배치 발사에 충분한가, 아니면 채운 등록을 다시 봐야 하나?

## 5. 재현 (리뷰 핀 · 컨테이너 Linux · Python 3.11)

```bash
python3 scripts/test_lhs_release_v13.py                       # 234 PASS · 0 FAIL
python3 scripts/lhs_release_build.py --selftest                # 31/31
python3 scripts/run_network_194_parallel.py --selftest         # 130/130
python3 scripts/g2_network_reread.py --selftest                # 30 ✓
python3 scripts/lhss_design_adapter.py --selftest              # 27/27
python3 scripts/lhs_design_dataset.py --selftest               # 389/389
python3 scripts/lhsx_design_adapter.py --selftest              # 14/14 (무변경)
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 bash scripts/check_all.sh   # ✓ 전부 통과
```

## 6. 이 검토 뒤 (등록 §0 순서)

⬜ 1저자 WSL 재수확 (`1e09f661d` · 명령 = `docs/data/lhs_supp_runs_20261006/README.md` 끝) → 반입 · r2 키별 대조 → 등록 §2 지문 (raw sha256 표 · 코호트 TSV) →
등록 비준 (1저자) → Codex GO → 발사 핀 사전 점검 (fast16 + real4 · 깨끗한 트리 · 새 ROOT 둘) → 같은 날 194 먼저 → 보충 20 → 배치마다 관문 → v1.3 (명령 =
`docs/reviews/lhs_release_v13_plan_20261007.md` §2b · 대조는 WSL).
