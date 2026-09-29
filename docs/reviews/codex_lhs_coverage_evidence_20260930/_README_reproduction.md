# 우리 쪽 재현 기록 — Codex LHS 피복률 병합 전 리뷰 (2026-09-30)

이 폴더의 나머지 파일은 Codex 가 보낸 zip (`codex_lhs_coverage_review_20260930.zip` · 862,690 B ·
sha256 `c6cadd76539e8dd364331c6d96a2c520b242e4faf118313693ff24e1fb52a99c`) 에서 **그대로** 옮긴 것이다
(`PACKAGE_SHA256SUMS.json` 이 파일마다의 해시).  판정문 = `../codex_lhs_coverage_verdict_20260930.md`
(266 행 · sha256 `f14bd44a0415de31ba62f357f4a4b0e0146fe12cb515fccd1786575f17faaa09`).
`_reproduction_*` 넉 장만 우리가 만들었다.

## zip 에서 옮기지 않은 것

- `lhs_coverage_review_20260930/{baseline,candidate}/` — 패치 대상 8 파일의 사본 (각 ~1.1 MB).  git 에 이미 있다:
  baseline = `da4670594` 의 8 파일 (CRLF 정규화 뒤 바이트 동일 8/8), candidate = `da4670594` + 패치 0001–0007
  (= 우리 검토 브랜치 `review-coverage-20260930` = `64ae3cba8` 의 8 파일 · CRLF 정규화 뒤 바이트 동일 8/8 · zip 사본은 Windows CRLF).
- `submitted_bundle/` — 우리가 보낸 요청서 · 패치 7 · `SHA256SUMS` · `selftests.log` · `gate.log` 의 사본 = 커밋된
  `../codex_lhs_coverage_request_20260930/` 와 패치 sha 7/7 일치.
- `fixtures/` · `pipeline_fixtures/` · `cli_fixtures/` — 감사 스크립트가 실행 때 다시 만드는 합성 입력 · 출력.

## 우리 재현 (2026-09-30 · Linux 컨테이너)

- 트리: `2e57dff90` 위에 `git am` 으로 패치 7 을 붙인 임시 worktree (`wt_cand` · 커밋 `914a95c5c`) — 8 파일이 `64ae3cba8` 과 바이트 동일.
  리뷰 README 의 지시대로 **브랜치 끝이 아니라 별도 사본**에 붙였다 (현 HEAD `c9ecda799` 는 이 패치를 담지 않는다).
- 환경: Python 3.11.15 · NumPy 2.4.6 · pandas 3.0.5 · SciPy 1.17.1 · NetworkX 3.6.1 · Flask 3.1.3 (Codex: Windows · Python 3.12.14 · NumPy 2.3.5 · pandas 3.0.1).
- 명령 (증거 폴더 사본에서 · `LHS_REVIEW_REPO=<wt_cand>` · `LHS_REVIEW_BASELINE=<zip baseline>` · `PYTHONUTF8=1`):
  `audit.py` → `audit_pipeline.py` → `audit_cli.py` → `audit_harvest.py` (rc 전부 0).

| 결과 파일 | Codex (zip) ↔ 우리 (`_reproduction_*_cand_64ae3cba8.json`) |
|---|---|
| `audit_results.json` | **동일** (12 항 전부 — `denominator_zero` 0.0·ok · `nan_isolated_radius` 0.0·ok · `valid_isolated_zero` 0.0 · `wall_outside_numerator` 31.626275510204017 · `rounding_sweep` 0/0 · `hertz_miss` · `3e-5_miss_deep` 미포착 · `rounding_only_false_alarm` diff/tol 1,177,958 · `ast_guard` 두 우회 · `yield_jump` 0.05656867318424044 · `legacy_comparison` 6/6 same) |
| `pipeline_results.json` | **동일** (`stale_standard` · `stale_bimodal` = failed · `atoms_only` = success/done · `status_schema` 4/4 True · 배치 copy-shim 29/29) |
| `cli_results.json` | 값 동일 — 차이는 stdout 의 절대 경로뿐 (`nested_archive_all` rc 0 · skip · v2 미작성 · `external_case_id` rc 0 · v2 작성 · `bad_json_case_dir` rc 0 · 파일 그대로) |
| `harvest_comparison.json` | 값 동일 · **플랫폼 항목만 다름**: 수확기 selftest 가 여기서는 **139/139** (Codex 는 Windows CRLF 로 137/139 → LF 통제 138/139) · τ 중앙값이 여기서는 **2.0805329527696066 = 핀** (Codex 는 1 ULP 위 2.080532952769607) · 기준 ↔ 후보 legacy 키 15 호출 불일치 0 · τ base = candidate |

⇒ Codex 판정의 반례 · 대조 · 수치는 우리 트리에서 **전부 재현된다**.  Codex 가 플랫폼 문제로 남긴 두 항목 (CRLF · 1 ULP) 은 Linux 에서 없다.

## 배치 selftest (symlink)

Codex 는 Windows symlink 권한 때문에 `lhs_webapp_batch.py --selftest` 를 copy-shim 으로만 돌렸다 (29/29).  우리 쪽 원형 실행은
제출 묶음의 `selftests.log` (Linux · symlink 그대로 · 29/29) 와 이번 재현의 `audit_pipeline.py` (shim 포함 29/29) 둘 다 초록이다.

## 원장

`LHSC-01`~`LHSC-10` (`docs/reviews/findings.json`) — P1 2 (`01` v2 분모 무효 → 0.0·ok · `02` atoms-only 가 `stop_after='coverage'` 우회) · P2 3 (`03` 상태 문자열 검증 ·
`04` item 2 허용폭 경계 · `05` AST 가드 우회) · P3 5 (`06` 벽 제외 = 분모 보정 proxy · `07` CLI 옛 조용한 경로 + `WEBAPP_*_FOLDER` 행위 변경 고지 · `08` 벽 규칙 접선 근처 수 ·
`09` 접촉 문 단일 영상 전제 · `10` v2 = 미검증 후보 연산자 라벨).
