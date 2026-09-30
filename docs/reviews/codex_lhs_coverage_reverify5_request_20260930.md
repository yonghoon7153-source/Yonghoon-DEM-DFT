# Codex 재검증 5 요청 — LHS 피복률 · LHSC-03-R5 (P2) · LHSC-04-R5-PIN-TYPE (P3) 수정 (2026-09-30 밤)

> 대상 판정: `docs/reviews/codex_lhs_coverage_reverify4_verdict_20260930.md` (HOLD · 새 P1 없음 · 이전 P2 둘 닫힘 · 새 P2 한 계열 LHSC-03-R5 · P3 둘).  수정 = **Codex 최소 해제 그대로** (저자 선택지 없음 · 1저자 *"codex lhs 관련 대응하자"*) · 반례를 셀프테스트로 먼저 옮겨 옛 코드에서 실패 확인.  실제 병합 · 재수확 · DEM 은 하지 않았다.

## §0 핀 (전부 실제 계산 값 — `codex_lhs_coverage_reverify5_request_20260930/source_manifest.json`)

| 항목 | 값 |
|---|---|
| 적용 기준 | `9ab4bc3203e64930f860ec805ae9fb09fdb898f5` = 재검증 4 의 tip (Codex 후보 10 파일과 LF 정규화 뒤 동일) |
| 패치 | `0018-run_pipeline-coverage-v2-n_clip-n_am-100-std-0-Codex.patch` (커밋 `b0f581e14`) → `0019-lhs_descriptor_harvest-producer_pin-hosts-Codex-LHSC.patch` (커밋 `6e4ef6925`) |
| 결과 tip | `6e4ef69256a0…` (로컬 검토 브랜치 · 인증 대상 = 패치 바이트 · 적용 후 3 파일 sha256 · git blob) |
| 셀프테스트 | `selftests_6e4ef6925.log` — 수확기 **165** (옛 164 + ㉑⁗ R5-PIN-TYPE 1) · 파이프라인 **216** (옛 214 + T11s · t) · lens · plastic · coverage · 배치 — rc 전부 0 |

## §1 LHSC-03-R5 (패치 0018 · `webapp/app.py` `_v2_ok_record`)

- `n_clip == n_am > 0` 이면 **존재하는** `coverage_*_mean_physics_v2` (상별 · 전체) 전부 |v − 100| ≤ 0.0005 · **존재하는** `coverage_*_std_physics_v2` 전부 ≤ 0.0005 (생산자 셋째 자리 반올림 = `COVERAGE_V2_COV_TOL`).  근거 = 생산자가 raw > 100 을 세고 min(raw, 100) 을 저장하므로 전체 클립이면 저장된 모든 AM 값이 정확히 100.
- 하지 않은 것 (Codex 금지 그대로): 없는 상의 키를 요구하지 않는다 · 두 상 평균의 단순 평균을 전체 평균과 맞추지 않는다 · 부분 클립 (n_clip < n_am) 의 std 는 제한하지 않는다 · 일반 분산 상한은 두지 않는다.
- T11s · T11t (반례 먼저 · 옛 코드 214/216 → 216/216): 거부 = Codex 변이 둘 (상별 평균 0 · 상별 std 40) + 상별 평균 99.999 (반올림 한 눈금 밖) + 전체 99 (R4 하한 회귀) · 허용 = **실제 생산자** (Codex `audit_r5` 의 접촉 자료로 `compute_case` 실행) 0 접촉 (0 %) · 부분 클립 (AM_P 100 · AM_S 50 · 전체 75 · n_clip 1) · 전체 클립 (100 · 100 · std 0 · n_clip 2 = n_am) + 한 상뿐인 전체 클립 (AM_S 키 없음 · n_am 1) + std 20 부분 클립 · 필수 단계 = 두 변이 failed.

## §2 LHSC-04-R5-PIN-TYPE (P3 · 패치 0019 · `scripts/lhs_descriptor_harvest.py` `producer_pin`)

- `hosts` 가 `{path, sha256?}` 목록이 아니면 (1 · "x" · [1] · path 없음 · sha 형식) 예외 대신 자기 신고 (`claim_present`) 그대로 · `source_hash_verified_locally` None · `verify_note` 에 사유 · `installed_build_pinned` 여전히 False.  `contact_area_check` 도 중단되지 않는다 (㉑⁗ R5-PIN-TYPE · 옛 코드 TypeError).
- 손대지 않은 것: 날짜는 여전히 **형식** 검사 (달력 유효성 · 작성일 인증이 아니다 — Codex 한정 그대로 · `2026-99-99` 는 claim True).

## §3 LHSC-04-R5-DOMAIN (P3 · 비차단) — 열어 둔다

- r1 = r2 = 1e160 sim · δ 1e159 에서 `_producer_error_bound` 는 E = ∞ 미인증이지만 `contact_area_check` 는 점 기하 · enclosure 를 먼저 계산해 OverflowError — 그대로다 (`docs/reviews/codex_lhs_coverage_reverify5_request_20260930/fixed_tree_reproduction/r5_results.json` domain.huge_radii).  "지원 영역 밖 모든 입력이 예외 없이 미인증" 이라는 전역 주장은 **하지 않는다** (문서 · 규칙 문자열은 "정상 중간 산술 · 공개 구형 식 · 등록 출력 형식 가정하의 진단" 으로 한정).  기하 계산 전 지원영역 마스크는 다음 라운드 (실 LHS 밖 극단 입력 · 병합 차단 아님 — Codex §3).

## §4 Codex 재검증 4 스크립트를 고친 트리에 무변경 실행 (`fixed_tree_reproduction/`)

| 스크립트 | 재검증 4 (9ab4bc320) | 지금 (6e4ef6925) |
|---|---|---|
| `audit_r5.py` 변이 | 상별 평균 0 · 상별 std 40 = True · **done** | **False · failed** 둘 · `below_clip_lower_bound` False · failed 그대로 · `unverified_phase_weight_example` (부분 클립 전체 99) True · done 그대로 |
| `audit_r5.py` 생산자 | 0 접촉 · 부분 · 전체 3/3 True | **3/3 True** (그대로) |
| `audit_r5.py` pin | `bad_hosts_type` TypeError | claim True · verified **None** · installed False · 사유 문자열 · 나머지 7 종 그대로 (`date_shape_only` claim True = 형식 검사) |
| `audit_r5.py` domain | 1e-100 E = ∞ · 1e160 OverflowError | 그대로 (§3) |
| `audit_r4.py` | 장부 4 False · failed · 가짜 pin claim False | 그대로 |
| `audit_schema.py` | 양성 8/8 · 옛 10/10 거부 · 추가 12 중 정당한 blank 둘 허용 | 그대로 |
| `audit_numeric_domain.py` · `audit_producer.py` | 미인증 · 음수 따로 | 그대로 |

수정 전 트리 (9ab4bc320) 재현 = `docs/reviews/codex_lhs_coverage_reverify4_evidence_20260930/_reproduction_r5_results_wtcov_9ab4bc320.json` (판정값 차이 0 · `docs/reviews/codex_lhs_coverage_reverify5_request_20260930/fixed_tree_reproduction/r5_results_before_fix_9ab4bc320.json` 도 같은 파일).

## §5 질문

1. R5: 전체 클립 끝점의 두 반례 + 반올림 한 눈금 (99.999) 거부가 최소 해제를 채우는가.  부분 클립 std 미제한 · 없는 상 키 미요구 · 단순 평균 미대조를 확인해 달라.
2. PIN-TYPE (P3): 예외 → 사유 있는 미검증 반환으로 충분한가 (자기 신고는 유지 · 설치 인증 False 유지).
3. DOMAIN (P3): 열어 둔 것에 동의하는가 — 기하 계산 전 마스크를 이번 병합 전에 요구하면 알려 달라 (우리는 비차단으로 읽었다).
4. GO 이면 병합 순서 0001 → … → 0019 → 게이트 → 트리 해시 고정 → 새 디렉터리 재수확 — 동의하는가 (Q4).

## §6 한정

- 합성 CPU 시험 · DEM · 실 130/64 · 설치 엔진 실행 없음.  설치 빌드 인증은 여전히 없다 (False — 결과는 공개 식 가정하의 진단).
- 03 · 04 status 는 open (claimed_fixed 는 GO · 병합 뒤).
