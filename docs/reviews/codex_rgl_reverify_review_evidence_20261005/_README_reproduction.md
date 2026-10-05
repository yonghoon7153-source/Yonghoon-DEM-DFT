# Codex RGL 재검증 — 반입 + 우리 트리 재현 (2026-10-05)

- 판정문: `docs/reviews/codex_review_rgl_reverify_20261005.md` (= zip 의 `codex_review_rgl_reverify_20261005.md` · sha256 `96df03b5130e8ccbf4bfe8fe31ee9da3baab076f8f2c86aeb775fbc6554ef799`) — **HOLD · 새 P1 없음 · 기존 P1 4 (RGL-01 ~ 04) 원 반례 기준 닫힘 · 새 P2 3 (`RGLR-01` ~ `03`) · RGL-06 · 08 부분**.
  194 건 실행 · 새 봉인 · WSL 통합 · real14 실데이터 회귀 승인 아님.
- 반입 원본: 사용자 전달 zip `04e45fe0-codex_rgl_reverify_review_20261005.zip` — 5,568,601 B · sha256 `748ebabd5dbfaa1d8f38376525201c207db0e1cb1e8937f88f04b3e71d791cbf` · `package_manifest.json` 685/685 일치.
- 핀 `bf4fb6aee0b388375ddf65694ac405e63e0e381c` — `source_manifest.json` 의 432 파일 git blob 이 **핀의 blob 과 432/432 같다**.
- 이 폴더 = zip 에서 아래 466 개를 뺀 나머지 + 이 README + `_reproduction_compare_linux.json`.
  뺀 것 (sha256 은 그 JSON 의 `excluded_from_repo`): 핀 소스 사본 432 (blob 동일) · `diffs/` (핀 사이 git diff · 재생성 가능) · `inputs/` (우리 요청서 사본 · fixture 목록) ·
  판정문 원본 (위 경로로 반입) · 합성 payload JSON 4 (`evidence_g1/` · 탐침이 재생성) · 구식 망 모듈 사본 (`git show eedada5d3:scripts/network_conductivity.py` 와 같음).
  ⇒ 탐침 재실행은 **zip 원본**을 풀어 그 안에서.

## 우리 트리 재현 — 탐침 무변경 (Linux · 같은 blob 사본)

`run_probes.py new_network independent_lw original_g4 raw18 handover` (rc 0) · 빈 폴더에서 `original_g1` (rc 0).  비교 JSON 19 개 · 미분류 차이 **0** ·
수치 최대 상대차 5.2e-08 (CG 잔차 · 플랫폼) · 나머지 차이는 분류 안 (합성 산출 파일 해시 · run_id · 시각 · 플랫폼 간 원시 hex · 입력 경로 · 문자열 실수 1 ULP).

### RGLR-01 · 02 · 망 경로 (실 CLI · 실 helper)

| 경우 | stop | 상태 |
|---|---|---|
| `positive` | true | done |
| `no_through` | true | done |
| `legitimate_band` | true | done |
| `solver_failed_stop` | true | failed |
| `solver_failed_general` | false | done |
| `ratio_times4` | true | done |
| `band_ratio_missing` | true | done |
| `band_ratio_nan` | true | done |
| `band_ratio_negative` | true | done |
| `band_fraction_above1` | true | done |
| `rejected_retry_preserves_generation` | true | failed |
| `write_failure_after_stamp` | true | EXCEPTION |

### RGLR-03 · LW (실 CSV → 실 파서 → LW)

| 경우 | status | virial_status |
|---|---|---|
| `normal` | OK | null |
| `nan_plate` | FAILED (invalid_input: plate_z = nan — plate_z_source=mesh 면 판 높이는 바닥 z = 0 위의 유한값) | null |
| `isolated_nan_radius` | FAILED (invalid_input: bad_radius 1 (id 3) — 비유한 · 0 이하 · c_strs 결측 1 (id 3) / 3 입자 — 일부만  | null |
| `true_zero_load` | UNDEFINED (zero_load: max|F| = 0 — 평균 σ_VM = 0 → CV · 상 비 = 0/0 미정의 · 0 으로 채우지 않음) | null |
| `false_zero_force` | FAILED (force_columns: max|F| = 0 인데 max|F − (Fn+Ft)| = 1 — 영 척도 · 절대 잔차 > 0 · 상대 차 정의 안 됨 | null |
| `two_dimers_correct` | OK | null |
| `two_dimers_swapped` | OK | null |
| `finite_cstr` | OK | null |
| `nan_cstr_first` | OK | null |
| `text_cstr_first` | OK | null |
| `inf_cstr_first` | FAILED (invalid_input: non_finite c_strs 2 (id 1, 2)) | null |
| `finite_wrong_virial` | FAILED (virial_mismatch: |Σ V σ_LW − Σ c_strs| / Σ|Σ c_strs| = 0.667 > 0.01 — 원자 · 접촉 덤프의  | null |
| `nan_hides_wrong_virial` | OK | null |
| `all_cstr_absent` | OK | null |
| `partial_cstr_tuple` | OK | null |

- 유한 전극 전력 몫 (Q4 · raw18): 이상 전극 대비 **+12.0517607674 %** (판정문 +12.0517607674 %).

## 한정 (Codex 그대로)

- 합성 fixture · 소형 CLI 검산이다 — 운영 코퍼스에 이 손상이 있다는 증거가 아니다 (RGLR-01 · 02 · 03 scope_limit).
- 일반 경로 (Stage E) 반례는 Stage E 를 대역으로 바꾼 것 — 실 Stage E 수치 재현이 아니다 (Q1 · `WEB-03`).
- `test_love_weber_stress` 는 real14 fixture 부재로 Codex 쪽 68/69 — 전체 76/76 을 재인증하지 않았다.
- 194 행 산술은 커밋된 요약표 검산이다 — 원 dump 재분석 · 인계 재생성이 아니다.
