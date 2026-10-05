# LHS 194 망 단계 배치 — 실행 등록 (amendment 봉인 · 2026-10-05 밤 · 결과 0 건)

- 근거: Codex 판정 Q8 (`docs/reviews/codex_review_rint_g1_lhs_network_20261005.md` — *수정 → 통합 게이트 → 필요한 등록 개정/봉인 → 그 봉인으로 배치*) · 3차 재검증 §6-5 (`docs/reviews/codex_review_rglr_reverify_20261005.md` — ⑤⑥⑦ · 망 τ 만 · LW 제외 · 수정 파일을 승인된 amendment 로 재봉인 → 별도 승인된 194 배치 → τ 관문 → 실제 숫자 인계 왕복).
- 1저자: *"망 194건 인계는 무조건 되게 만들어야돼"* · *"1코어 20개로 20개"* (10-05 밤).
- 이 문서는 **배치 전에** 커밋한다.  결과를 본 뒤 고치지 않는다 (고치면 덧붙임 절 + 사유).

## 1. 대상 (동결 inventory 그대로)

- `lhs` 130 · `lhsx` 64 — 수확 폴더 `docs/data/lhs_descriptors_cov_1e09f661d/` · `docs/data/lhsx_descriptors_cov_1e09f661d/` · 코호트 `docs/data/area_s2_cohort.tsv` · `docs/data/lhsx_descriptors_20260925/_cohort.tsv` (10-01 접촉 · 피복 배치와 같은 집합 · 같은 프레임 관문 sha · 09-17 23:59 KST cutoff 무변경 · 새 코호트 없음).

## 2. 계산

- 웹앱 `run_pipeline(stop_after='network')` = 접촉 → 피복 → 망 솔버 → 망 정지 계약 (Stage E 없음).
- 실행기 `scripts/run_network_194_parallel.py run --root ~/net194_<sha>` — 케이스마다 `lhs_webapp_batch.py --stop-after network --case <c>` 한 번 · 동적 큐 (접촉 수 큰 순) · 갈래 기본 20 × 1 스레드 (OMP · MKL · OPENBLAS · NUMEXPR · VECLIB = 1) · 케이스별 TMPDIR (망 lock 이 케이스 안에서만 — 기계 전체 하나씩 잠금 대신 메모리 예산 입장 관문) · 갈래별 작업 폴더 · 산출 `merged/{lhs,lhsx}/` (배치 자신의 writer).
- 시범 실측 (WSL · 고치기 전 코드 `05fbf15aa` · 시간 · 메모리는 수정과 무관): 가장 큰 `lhsx_040` (접촉 62 만) 171 s · RSS 2.6 GB · real_14 망 정지 29 s · 0.58 GB · WSL MemTotal 15.5 GB ⇒ 큰 케이스 동시 ≈ 5.

## 3. 코드 신원 (봉인)

- 발사 커밋 = **이 문서를 담은 커밋** (푸시됨 · 추적 파일 작업트리 깨끗해야 발사 — 실행기가 거부한다).  실행기 `manifest.json` 이 git sha · 아래 19 파일 sha256 · 스레드 · lock · 레인을 남긴다 — **이 표와 같아야 한다** (다르면 이 봉인의 배치가 아니다).  merge 는 케이스 사이 코드 sha 가 섞이면 거부한다.
- 인계 생성기 (`scripts/lhs_design_dataset.py` · τ 묶음 `tau` · `--tau-results`) 와 τ 관문 (`scripts/tau_flux.py`) 도 같은 커밋.

| 파일 | sha256 |
|---|---|
| `scripts/network_conductivity.py` | `b0555f7f7a65c2d327b4cca15791586e980d0b6b75b47c846457d628f19b7592` |
| `scripts/plastic_coverage.py` | `fdb00df699d30cf7a24bcbf0485e9e6713955eecc0703ad4aa75fa3fabe91cc3` |
| `scripts/audit_constriction_deleted.py` | `7028be8f10d491071e512767987bbcd7d74b47fa227badeded99916c7af512bd` |
| `scripts/extract_se_network_diagnostics.py` | `db7151b51252e60c42c2bc2a2b3173ae6f4b97a94226b51a97b1e357e028ea9a` |
| `scripts/dem_analysis_core.py` | `39fb19cb7eb962f11fe88546fa0ad93c4a9074846be13d15b27c2eae44fb620f` |
| `scripts/analyze_contacts.py` | `a383ada7aef3d13ba08bd84728a20b6207f9b124a01ce3852c01ae2518ca1aa9` |
| `scripts/analyze_contacts_bimodal.py` | `8afcc76030b747d8632014fa5b6cae1c1f066007b9247902caefb05288cf1ca5` |
| `scripts/coverage_physics_vs_hertzian.py` | `4341b03b38ec1f811a3087d699471860cad366323ae9eb419cf76457e6cd6d01` |
| `scripts/parse_liggghts.py` | `4fe3f1f32ebc4168978c7278b7a1d37b072d64fbf00e97d0933351337d223425` |
| `scripts/se_material.py` | `767a6a383d4581274b07ee79146a53fbe118f1f6eb0acb9ec0a5af21c9c9930c` |
| `scripts/metrics_json.py` | `baa671f895dd6103cf95c25647ee45877d98306f00ab15cd3968fbe4354a7702` |
| `scripts/tau_flux.py` | `550dab08bcea0e35c3b84cdf51f797a4d4987d5d5738413347af09d4e4abc863` |
| `scripts/lhs_webapp_batch.py` | `b9d0199cc1bd23cd1ed5405a283081c2c3a31bc6ce256670c8a9b63d177b5668` |
| `scripts/lhs_harvest_batch.py` | `4d798c631ac893ca32018fde58145bc5c8a2e3e2a6423da61cb87bd13599148e` |
| `scripts/lhs_descriptor_harvest.py` | `27624b8a39ab8807645f819776ea0125f423d4d4f61a90e8c3a3fc45b357178b` |
| `webapp/app.py` | `3eca948001600a2f73b4057da30d1f0aff1141cad286c13701560c885600e4e3` |
| `webapp/pipeline_service.py` | `60e0f9785c475eac542d8fffe4928350248ef39cd8aa829db49031611dc56413` |
| `scripts/export_master_csv.py` | `2899dc2410ad8840dadf41993511c225d60f29f77edfdb2fac6703b25ccf767b` |
| `scripts/type_map_resolve.py` | `4a289c6412e4b8e1bc0fba573cb287966dfa00a053399097b587f1e14726bfe5` |

## 4. 판정 · 관문 (결과 전 등록)

1. 케이스마다 `done` / `failed` (+ `failure_kind`) — failed 는 빈칸 + 사유로 싣고 고르지 않는다.
2. τ = `tau_flux` 관문 G0–G6 그대로 (`NOT_PERCOLATING` · `NOT_COMPUTED` · `BAND_FALLBACK` · `MODEL_BELOW_CONTINUUM_BOUND` 표지 유지).
3. 인계 생성기 관문 (⑤F1 · ⑥R1–R3 · ⑦A1–A5 + τ 묶음 관문).
4. 회귀: `d1ec42fba` 접촉 배치와 **같아야 할 열은 같은 값** — 허용되는 다름은 선언된 변경뿐: 옛 σ_VM (`stress_cv`) 무효 · 미정의 입력 null (LHS-33) · 반올림 한계 입자 안정식 (RGLR2-03 · real_14 기준 0 입자) · LW 열 명시 제외 (frame_unverified) · 단일 스레드 BLAS 의 마지막 자리 · 망 단계 새 열.  그 밖의 차이는 보고하고 원인을 밝힌 뒤에만 싣는다.

## 5. 배포

- 인계 (ML 담당 전달) = Codex 4차 GO 뒤.  GO 전 결과는 격리 폴더에만 둔다.
- Codex 가 σ · τ 값에 영향을 주는 결함을 찾으면 해당 케이스 재실행 (이 등록에 덧붙임).

## 6. 이탈 기록

- **194 배치를 Codex 4차 재검증과 병렬로 돌린다** — 1저자 *"나로 진행하자"* (10-05 21:1x KST · 제안 (나)).  등록 순서 (Codex GO → 재봉인 → 배치) 에서 벗어난다.
  사유: 4차 대상 수정 셋 (일반 게시 경로 검사 · 복원 실패 표지 · 옛 σ_VM 경계) 은 망 σ · τ 수치 경로를 바꾸지 않는다 (원시 해 비트 동일 = Codex 3차 §4-1 확인) · 아침 마감.
  통제: 발사 봉인 (이 문서 §3) · 격리 출력 · 인계 (배포) = 4차 GO 뒤 · 4차가 값에 영향 주는 결함을 찾으면 해당 케이스 재실행 + 덧붙임.

## 7. 덧붙임 — 인계 생성 커밋 (10-05 밤 · 배치 결과 뒤 · 사유)

- Codex 4차 (`docs/reviews/codex_review_rglr2_reverify_20261005.md` §5 · §8) = **배치 재실행 불요 · 인계 검사를 보강해 다시 읽기**.  고친 것: 실행기 `scripts/run_network_194_parallel.py` (RGLR3-01 재시도 봉인 · 시도별 지문 · `audit` 부명령 · RGLR3-03 후속 명령) · 인계 생성기 `scripts/lhs_design_dataset.py` (RGLR3-02 τ 로더 P4 = 같은 `pipeline_service.network_stop_verdict` 재호출 · 세대 · 읽기 안정).
- ⇒ 인계 v1.2 는 **고친 커밋**의 생성기로 만든다 (§3 의 "인계 생성기 · τ 관문도 같은 커밋" 에서 벗어남).  두 파일은 §3 의 19 봉인 파일이 아니고, 고친 커밋에서 19 파일 sha256 은 §3 표와 **19/19 같다** — 인계 때 다시 부르는 정지 계약 · τ 관문 (`pipeline_service.py` · `tau_flux.py`) 은 배치가 쓴 바이트 그대로다.
- 194 결과 (`~/net194_11fcf91e8`) 는 그대로 둔다.  봉인 감사 (`audit`) 로 케이스마다 계산 코드를 확인한 뒤 인계 — UNSEALED 가 있으면 그 케이스만 retry (발사 체크아웃 `~/dem-audit` 을 봉인 커밋에 둔 채 다른 체크아웃의 실행기로).
