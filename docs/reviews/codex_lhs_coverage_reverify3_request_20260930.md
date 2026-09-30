# Codex 재검증 3 요청 — LHS 피복률 · LHSC-03 R3 · LHSC-04 R3a · R3b · P3 수정 (2026-09-30 밤)

> 대상 판정: `docs/reviews/codex_lhs_coverage_reverify2_verdict_20260930.md` (HOLD · 새 P1 없음 · P2 R3 셋 + P3 둘).  이 요청서는 그 잔여 전부에 대한
> 수정 (1저자 비준 09-30 밤 *"비준이야"* · 반례를 셀프테스트로 먼저) 과 Codex 스크립트의 고친 트리 재실행 결과다.  실제 병합 · 재수확 · DEM 은 하지 않았다.

## §0 핀 (전부 실제로 계산한 값 — `codex_lhs_coverage_reverify3_request_20260930/source_manifest.json`)

| 항목 | 값 |
|---|---|
| 적용 기준 (base) | `ca0471d19a5a9d914c6a31006a001d515267f3be` = 재검증 2 의 tip — Codex 후보 10 파일과 CRLF 정규화 뒤 sha256 10/10 동일 (재검증 2 반입 README) |
| 패치 | `0014-LHS-item-2-Codex-LHSC-04-R3a-R3b-P3.patch` (커밋 `044220b1a`) → `0015-run_pipeline-coverage-v2-Codex-LHSC-03-R3-P2-P3.patch` (커밋 `220b1426e`) · `git format-patch` · base 위에 순서대로 `git am` 또는 `git apply` |
| 결과 tip | `220b1426ea39eae13f077e9f0585388f3eb61d08` (로컬 검토 브랜치 `review-coverage-20260930` · 원격에 없음 — 인증 대상은 패치 바이트 · 적용 후 파일 sha) |
| 바뀐 파일 | `scripts/lhs_descriptor_harvest.py` · `webapp/app.py` · `webapp/test_pipeline_provenance.py` (sha256 · git blob = manifest) |
| 셀프테스트 (고친 트리) | `selftests_220b1426e.log` — lens 7 · plastic 28 · coverage 16 · 수확기 **160** (옛 149 + ㉑‴ 10 + ㉑′ 개정) · 파이프라인 **212** (옛 209 + T11n · o · p) · 배치 30 · rc 전부 0 |

## §1 LHSC-04 R3a — 생산자 부동소수 오차 (패치 0014)

재검증 2 요청서 §5 Q2 의 답 (*"고정 여유 32·eps·π·max(r)² 가 생산자 오차를 덮는다"*) 은 **철회**했다.  계약:

1. **생산 식을 핀한다** — `PRODUCER_AREA_MODEL` = 공개 PUBLIC master `compute_pair_gran_local.cpp add_pair` (Codex 열람 09-30): `A = −π/4·(r−r1−r2)(r+r1−r2)(r−r1+r2)(r+r1+r2)/rsq · r = sqrt(rsq) · δ = r1 + r2 − r` (binary64 · 음수 · 0 을 자르지 않음 · C++ 괄호 · 좌결합 순서).  `producer_area_binary64` 가 그 순서대로 옮긴 스칼라 (Codex `audit_producer.py` 의 `emitted` 와 같음 · DEM 실행 아님).
2. **설치 빌드는 pin 파일로만 인증** — `producer_pin()`: `docs/data/liggghts_add_pair_pin.json` (또는 `LHS_PRODUCER_PIN_FILE`) 의 `schema liggghts_add_pair_pin/1 · source_file · sha256 (64 hex) · host · date · build · formula_confirmed: true`.  없거나 깨지면 결과 `contact_area_check.producer_model.installed_build_pinned = False` + 사유 (짐작하지 않는다).  ⚠ 지금은 **핀 없음** — 사용자가 WSL · ibb 빌드의 sha 를 주면 채운다 (§7).
3. **상자 전체의 절대 오차 상한 E** (`_producer_abs_error`): 인수 m_k = (δ, 2r1−δ, 2r2−δ, 2r1+2r2−δ) 의 상자 최대 절댓값, Δ_k = eps·(3S + m_k) (sqrt 뒤 두 뺄셈의 인수 형성 절대오차 · S = r + r1 + r2 = 2r1+2r2−δ 의 상자 최대 · 단위 반올림 u = eps/2 로 세면 2.75 · 0.5 라 여유), 13·eps ≥ 곱 3 · rsq 5 · 나눗셈 1 · π/4 2 (= 11u), **E = (π/4)/d_min² · [Π(m_k + Δ_k)·(1 + 13·eps) − Π m_k]** — 전개를 항별 합 (15 항 · 전부 양수 · 상쇄 없음 · 2 차 이상 포함) 으로 계산한다.  허용 구간 = [lo − E, hi + E].
4. **δ 상자 확장** — 덤프의 δ 는 binary64 로 만들어져 정확한 δ 와 Δδ = eps·(3S + |δ|) 만큼 다를 수 있으므로 δ 상자를 h(δ) + Δδ 로 잡는다 (상자가 정확한 δ 를 담아야 [lo, hi] 가 정확한 면적을 담는다).
5. **미인증** — 상자의 d 하한 ≤ 0 (동심 · 그 너머를 담음) 이면 1/rsq 가 서지 않아 E = ∞ → `n_producer_uncertified` 로 따로 세고 시험 · 초과에서 뺀다.  **거리 하한이 0 에 닿는 상자는 인증하지 않는다** (Codex 최소 해제 그대로).  ⚠ 그 결과 옛 깊은 겹침 예 (r .0005 · δ .000999999 · Hertz / 3e-5 치환) 두 행은 이제 **미인증** (옛: Hertz 0 · 3e-5 초과 1) — 그 상자에서는 생산자 자신의 출력이 π r² 를 넘을 수 있어 치환과 구별할 수 없다.  실 LHS 접촉 (δ ≪ r1 + r2) 에는 없는 영역이다.
6. **음수 덤프 면적** = `n_area_dump_negative` (정의역 밖 생산값 · 초과 아님 · 시험에서 뺌) — Codex 의 "의미 차이" 구분 그대로.
7. **고정 32·eps 여유 제거.**  남은 바깥 여유는 **기준 평가 여유** 16·eps·π·max(r)² 하나 — 정확한 A 의 포괄에는 불필요하고, 원판을 부동소수 덧셈형 (`lens_geometry` 의 a² − p² · 큰 반지름끼리 상쇄) 으로 평가해 대조할 때 (㉑″ · Codex `audit_geometry` 의 `actual_float`) 극값 근처에서 ~2·eps·(max r)² 만큼 넘는 것을 막는다 (생산자 여유가 아니다 · 규칙 문자열에 명시).

실증 (㉑‴ · 고친 트리): 공개 add_pair binary64 재현 **4000 점 (여섯 영역 · 동심 근접 d/r 1e-12 · 포함 경계 · 얕음 1e-9 · 비접촉)** 의 |A_p − A_e| (Decimal 60 자리) ≤ E(점) 위반 **0** · 실측/상한 최대 비 **0.08** · E/A 중앙 1e-10 (얕은 접촉은 E/A ∝ S/δ · 출력 반올림 5e-7 의 1/1000 아래) · 6 자리 토큰 경로에서 인증 행 2436 의 거짓 초과 **0** · 미인증 563 (동심 근접).

| Codex `audit_producer.py` 사례 (고친 트리 재실행 · `docs/reviews/codex_lhs_coverage_reverify3_request_20260930/fixed_tree_reproduction/producer_results.json`) | 재검증 2 | 지금 |
|---|---|---|
| normal (.001 · .001 · d .0019) | 초과 0 | 초과 0 · 검출 보증 1 |
| equal_deep_1e-12 (d 1e-15 · 생산 식 A 3.142020e-6 > π r²) | **초과 1 (변조 없음)** | **미인증 1 · 초과 0 · 시험 0** |
| equal_deep_1e-13 | 초과 0 (아래쪽 오차) | 미인증 1 |
| contained (생산 식 −1.5088e-6) | 초과 1 | **음수 면적 1 · 초과 0** |
| no_contact (생산 식 −3.22e-7) | 초과 1 | 음수 면적 1 · 초과 0 |

## §2 LHSC-04 R3b · P3 — 검출 보증 · 라벨 (패치 0014)

- `n_power_1pct` **제거** → **`n_detect_1pct`** = 참 면적이 [lo, hi] 어디에 있어도 ±1 % 치환의 **토큰 구간**이 허용 구간과 분리: `1.01·(lo − E) − 2h₊ > hi + E ∧ 0.99·(hi + E) + 2h₋ < lo − E` (h± = 그 크기 범위의 출력 반올림 반폭 최대 · 인증 행 · lo − E > 0) — **A_dump 와 무관** (치환해도 분류가 안 바뀐다).
- `n_wide_enclosure` = (hi − lo) > 1 %·**lo** (기술량 · lo > 0) · `n_lower_bound_zero` = **실제 lo == 0** (Codex 예 (.002, .001, .0021, 0) = 1) · `n_boundary_branch` = ④ 가지 진입 수 (신설) · `producer_bound_rel_median/max` = E/lo 보고.
- Codex 431 상자 (seed 4813): 정상 토큰 → 초과 0 · wide 1 · **보증 0** / +1 % 토큰 → 초과 0 · wide 1 · **보증 0** (옛: wide 0 · power 1) — 분류 동일.  같은 탐색을 새 키로 5만 상자 (`audit_power_r3.py`): 보증 행 32,853 · **보증했는데 ±1 % 를 놓친 행 0** · 분류가 A_dump 에 따라 바뀐 행 0.  합성 3000 행: 보증 3000 · +1 % · −1 % 토큰 전부 실제 초과 (보증 ⇒ 검출).
- ⚠ 원본 `audit_power.py` 는 없앤 키 `n_power_1pct` 를 읽어 KeyError (`audit_power_original_keyerror.out`) — 의도된 제거.

## §3 LHSC-03 R3 · P3 — 검증기 (패치 0015 · `webapp/app.py`)

계약 (Codex 최소 해제 그대로 · 재계산이 아니라 장부 구조 대조): 분율 키 둘 **필수** · 분모 > 0 이면 유한값 = `round(개수 비, 6)` (생산자 규약 `COVERAGE_V2_FRAC_ROUND` · T11p 가 생산자 상수와 대조) · 분모 0 이면 None 만 · 개수 dict = 생산자 분류 집합 (`PAIRS` · `BINDINGS`) **정확히** + 명시 정수 · Σ 쌍별 충돌 = nconf · Σ 결속 = n · AM–SE 결속 ≤ 총 결속 (분류마다) · 접촉 0 → 면적 0 · AM–SE 면적 > 0 → AM–SE 결속 ≥ 1 · n_amse + [SE–SE > 0] + [AM–AM > 0] ≤ n · n_am 0 → AM 이 낀 면적 · 결속 · 충돌 0 (SE-only 의 정상 0 과 구별) · blank `h_film` = None 또는 유한 양수 · 10^400 은 예외 없이 거부 · 결손을 0 으로 채우지 않는다.  blank 의 rule None · 내부 오류 경로의 h_film 부재는 그대로 받는다 (Codex 동의).

| Codex `audit_schema.py` (고친 트리 · `docs/reviews/codex_lhs_coverage_reverify3_request_20260930/fixed_tree_reproduction/schema_results.json`) | 재검증 2 | 지금 |
|---|---|---|
| 실제 생산자 양성 8 종 | 8 받음 | **8 받음** |
| 옛 변이 10 종 | 0 받음 | 0 받음 |
| missing_fractions · none_fractions · wrong_fractions · empty_count_dicts · unknown_binding_keys · contradictory_count_totals · n_am_zero_positive_area · zero_contacts_positive_area · blank_bad_film · huge_integer_area | 전부 True (10^400 은 예외) | **전부 False (예외 없음)** |
| 필수 단계 (none_fractions · empty_count_dicts · n_am_zero_positive_area · huge_integer_area) | done · done · done · failed | **failed 4** |
| blank_none_rule · blank_missing_film | True | True (양성) |

추가 반례 3 (T11n): AM–SE 결속 > 총 · 충돌 쌍 합 ≠ nconf · AM–SE 면적인데 결속 0 → 거부.

## §4 Codex 스크립트 고친 트리 재실행 (`fixed_tree_reproduction/` · 스크립트 무변경 · Linux)

| 스크립트 | 결과 |
|---|---|
| `audit_schema.py` | §3 표 |
| `audit_producer.py` | §1 표 · `producer_model.installed_build_pinned = False` (핀 없음) |
| `audit_geometry.py` | 12,000 상자 × 24 점 = 288,000 점 · Decimal 80 / 부동소수 이탈 **0 / 0** · corner 6,489 · zero 4,099 · interval 429 · boundary 983 · 옛 R2 반례 초과 0 · 옛 rounding 0 · hertz_deep · 3e-5_deep = **미인증** · 경계 대조 (δ = 0 양수 면적 초과 1 · 그 밖 0) |
| `audit_power.py` | KeyError (의도된 키 제거) → `audit_power_r3.py` §2 |

## §5 질문

1. **오차 모델의 유도** — 인수 형성 Δ_k = eps·(3S + m_k) · 13·eps · 항별 전개 · 1/d_min² 가 공개 add_pair 의 연산 순서에 대해 빈틈없는가 (특히 sqrt 의 오차 전파 · rsq 의 dy · dz 항 · 상수 −π/4 의 형성).  컴파일러 재배열 (FMA · `-ffast-math`) 은 설치 빌드 핀에서 확인할 항목으로 남긴 것이 맞는가.
2. **미인증 기준** — d 하한 ≤ 0 (Δδ 확장 뒤) 만으로 충분한가, 아니면 E 가 유한하되 커서 (예: E > h(A)) 검출력이 없는 행도 따로 표시해야 하는가 (지금은 `producer_bound_rel_*` 보고 + `n_detect_1pct` 0 으로만 드러난다).
3. **검출 보증 정의** — 양쪽 2h · E 포함 · A_dump 무관.  ±1 % 치환의 토큰 구간이 허용 구간과 겹치면서 보증 1 인 반례가 있는가.
4. **LHSC-03 항등식** — 남은 구멍 (예: per-AM 피복률 열 ↔ 개수 · `n_coverage_clipped_100 ≤ n_am` 밖의 것) 이 있는가.
5. **pin 프로토콜** — "설치 빌드 소스 sha256 + 사람이 add_pair 본문을 대조했다는 `formula_confirmed`" 가 "실제 생산 빌드의 식 · 컴파일 규약 핀" 으로 충분한가.  GO 뒤 병합 순서 0001 → … → 0015 → 게이트 → 트리 해시 고정 → 새 디렉터리 재수확.

## §6 한정

- 설치 빌드 (WSL `lmp_serial` · ibb `lmp_mpi`) 는 **아직 핀 안 됨** — 결과에 `installed_build_pinned: False` 가 실린다.  사용자가 `sha256sum src/compute_pair_gran_local.cpp` 와 add_pair 본문 대조를 주면 pin 파일을 만든다.
- 합성 CPU 시험이다 — DEM · 실 130/64 재수확 · coverage 배치 없음.  생산자 오차 모델의 "실증" 은 공개 식의 binary64 이식에 대한 것이지 설치 바이너리의 실행이 아니다.
- 03 · 04 의 status 는 그대로 open (claimed_fixed 는 재검증 3 GO · 병합 뒤).

## §7 파일

`docs/reviews/codex_lhs_coverage_reverify3_request_20260930/` — 패치 0014 · 0015 · `source_manifest.json` · `selftests_220b1426e.log` · `fixed_tree_reproduction/` (schema · producer · geometry 결과 · `audit_power_r3.py` + 결과 · 로그) · `SHA256SUMS` · `README.md`.

## §8 덧붙임 (09-30 밤 · 요청서 커밋 뒤) — 설치 빌드 pin 확보

§6 첫 한정 ("설치 빌드는 아직 핀 안 됨") 은 **해소**됐다 — `docs/data/liggghts_add_pair_pin.json` (이 묶음에도 사본).
- 두 기계 (WSL DESKTOP-IK8J81H `~/src/LIGGGHTS-PUBLIC` · lmp_serial · lmp_auto / ibb-master `/lustre/home/yonghoon/LIGGGHTS-PUBLIC` · lmp_mpi) 의
  `src/compute_pair_gran_local.cpp` sha256 = **`71c4d3b511be5df504888819079d55daa3e3816ea9ad7c4e0d81c30b548dbae9`** (1저자 셸 출력) · 두 트리 git HEAD
  `3d5c00f20519e6bb6eb6756f51f1ad36564e649d` · 공개 LIGGGHTS-PUBLIC 그 커밋 사본과 master 사본 (09-30 받음) 도 **같은 sha256**.
- 그 사본의 `add_pair` (555–558 · 573 행) = 수확기 `PRODUCER_AREA_MODEL`: `del = x[i] − x[j]` · `rsq = vectorMag3DSquared(del)` (세 제곱의 합) ·
  `r = sqrt(rsq)` · `contactArea = − M_PI/4 * (…4 인수…)/rsq` · δ 열 = `radi+radj-vectorMag3D(del)` (= (r1 + r2) − r).  852 행 (M_PI) 은 `add_wall_2` 의
  벽 접촉 면적이라 쌍 덤프 (`c_cpl`) 와 무관.  검토 브랜치의 `producer_pin()` 이 이 파일을 `pinned: True` 로 읽는다 (확인함).
- 남은 한정 (pin 파일 `limits`): 바이너리 해시 · 빌드 로그 · 컴파일 플래그는 대조하지 않았다 (오차 상한은 FMA 축약 · 인수 안 재결합 · 역수 곱에
  견디게 잡았다 — §5 Q1) · 두 기계의 `vector_liggghts.h` 는 해시하지 않았다 · LHS 130 · 64 를 돌린 ibb 바이너리 경로는 대조하지 않았다.
- §5 Q5 에 더하는 질문: 이 pin (소스 sha 3 곳 일치 + 식 대조 + 한정 명시) 이 R3a 의 "실제 생산 빌드의 식 · 컴파일 규약 핀" 요구를 채우는가,
  컴파일 플래그까지 요구하는가.

