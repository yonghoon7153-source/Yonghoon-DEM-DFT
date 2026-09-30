# Codex 재검증 요청 — LHS 피복률 두 묶음 · HOLD 3 건 수정 (2026-09-30)

**요청 범위** — 09-30 판정 (`codex_lhs_coverage_verdict_20260930.md` · 묶음 HOLD · 새 P1 2 · P2 3) 의 §7 최소 수정 목록 3 항
(패치 **0006** `LHSC-01` P1 · **0007** `LHSC-02` P1 + `LHSC-03` P2 · **0003** `LHSC-04` · `LHSC-05` P2) 을 고쳤고, P3 `LHSC-06` 의 문서
정정을 더했다.  요청 = **같은 반례 · 같은 스크립트로 재검증** + 새 패치 0008–0011 의 GO 여부.  GO 로 판정된 0001 · 0002 · 0004 · 0005 는
재검토 요청이 아니다 (판정 그대로 받는다).  생산 코드의 **값 · 물성 · 문턱은 바꾸지 않았다** — 바뀐 것은 무효 입력의 처리 (빈칸 · failed ·
경계 분류) · 검증 스키마 · 모듈 분리 · 문구다.

> ⛔ **재판정 도착 (09-30 밤) = HOLD** — `docs/reviews/codex_lhs_coverage_reverify_verdict_20260930.md` (LHSC-01 · 02 · 05 · 06 닫힘 · 03 · 04 부분 R2 ·
> 0008 · 0011 GO · 0009 · 0010 HOLD).  아래 §0 의 *"바이트 동일 · sha 7/7"* 은 **거짓이었다** (원장 `SELF-67`) — 정정문을 그 자리에 적었다.

- 고정 스냅샷 = 이 요청서가 든 main 커밋 (본문 §4 의 해시 — ⚠ 요청서가 제 커밋 해시를 적을 수 없어 실제 해시는 없었다 · Codex 가 파일 이력에서 `ac484ba5c` 로 고정).
  검토 트리 = **`da4670594` + `patches/0001–0011`** (`SHA256SUMS`).
  ~~0001–0007 은 09-30 제출본과 **바이트 동일** (앞 요청 폴더 `codex_lhs_coverage_request_20260930/patches/` 와 sha 7/7 같다 · Codex 도
  7/7 일치 확인)~~ ⛔ **정정 (SELF-67)**: 0001–0007 은 앞 제출본과 **diff 본문만 동일**하다 (`diff --git` 이후 7/7 같음) — `git format-patch` 를 11 개로 다시 뽑아
  머리 번호 (`[PATCH n/7]` → `[PATCH nn/11]`) · 제목 줄 접기가 바뀌어 **파일 sha 는 7/7 모두 다르다** (확인하지 않고 쓴 주장 · "Codex 도 일치 확인" 은 첫 판정이
  첫 제출본에 대해 한 말이었다) · 0008–0011 이 이번 수정.  검토 브랜치 `review-coverage-20260930` (로컬) = 같은 내용 · 커밋 `aba311054` · `471ad778b` ·
  `c125254a9` · `002cc2881`.
- 저자 결정 (09-30 · 1저자 *"권고대로"*): `LHSC-01` 계약 = **(a) 침대 전체 빈칸 + 사유 + 제외 수** (유효 부분집합 통계 (b) 아님) ·
  `LHSC-05` = **(a) 순수 기하를 별도 모듈로 분리** (AST 강화만 (b) 아님) · 셋 다 고친 뒤 재검증 → GO 뒤 의존 순서대로 한 항목씩 병합.
- 방법은 앞 라운드와 같다: 반례를 **셀프테스트로 먼저** 옮겨 옛 코드에서 실패를 확인한 뒤 고쳤다 (`selftests.log` · 커밋 메시지에 옛/새 수치).
  Codex 의 네 감사 스크립트를 **고친 트리**에 다시 돌린 결과 = `fixed_tree_reproduction/` (§3).

## 1. 수정 요약

| 패치 | 원장 | 무엇 | 반례 → 지금 |
|---|---|---|---|
| **0008** | `LHSC-01` P1 | `coverage_physics_vs_hertzian.py` v2 `coverage()`: AM 마다 반경 · 표면적이 유한 양수인지, 자유 표면 4πr² − Σ A_v2(AM–AM) > 0 인지 먼저 본다 · 아니면 피복률로 세지 않고 사유 (첫 사례 · 개수) → `keys()` 가 침대 v2 **빈칸** · 진단 `am_denominator_physics_v2` (n_am · n_free_surface_nonpositive · **n_radius_invalid** (새) · clipped) 는 빈칸에도 싣는다 · `PHYSICS_V2_RULE` · 모듈 docstring · `docs/area_contract_20260913.md` 에 계약 | `denominator_zero` (정사면체 AM 4 · 1.2 µm) → **blank** "AM 4 개의 v2 자유 표면 ≤ 0 = 분모 무효 (첫 사례 id 1: 4πr² 1.257e-05 − ΣA_v2 1.885e-05 = −6.283e-06 …)" · diag 4/4 · `nan_isolated_radius` → **blank** "AM 1 개의 반경 · 표면적이 유한 양수가 아니다 (id 1: r=nan)" · n_radius_invalid 1 · `valid_isolated_zero` → **ok · 0.0** (양성 대조) · legacy 6 변형 × 3 종 **동일** |
| **0009** | `LHSC-02` P1 | `webapp/app.py run_pipeline`: 접촉 파일이 없는 두 atoms-only 경로 (raw atom-only · CSV-only) 는 `stop_after` 가 있으면 `_atoms_only_refused` → `{success: False, status: 'failed', stopped_after, atoms_only: True, error, failed_stages: ['contact files missing']}` · 계산 · 도장 · 러너 · subprocess 호출 없음 · full_metrics 미작성 · `stop_after=None` (viewer) 은 그대로 | `atoms_only` (CSV-only · stop_after='coverage') → **failed** · success False · 배치 상태식 failed · 파일 없음 (T11g 4 경우 · T11h 양성 대조 2) |
| **0009** | `LHSC-03` P2 | `_coverage_v2_written`: `'ok'` 면 `COVERAGE_V2_OK_KEYS` 14 키가 None 이 아니고 (AM 이 있으면 `coverage_AM_mean_physics_v2` 유한 실수) · `'blank: <비지 않은 사유>'` 면 `COVERAGE_V2_DIAG_KEYS` 4 키 존재 · 그 밖은 False.  생산자: `compute_case` 내부 오류 경로도 진단 키 4 를 낸다 · 시험의 가짜 producer 는 실제 키 집합을 쓴다 (`_healthy_cov_v2` — 검증기가 엄해지자 status 한 줄 producer 가 거짓 실패한 fixture-drift 정정) | `status_schema` `''` · `'not_run'` · `'ok'` (키 없음) · `'blank: cause'` (진단 없음) → **4/4 False** (T11i 9 가지 False · T11j 양성 3 True) |
| **0010** | `LHSC-04` P2 | `lhs_descriptor_harvest.py`: **지원 범위** `_in_domain_rows` = d − \|r1 − r2\| > 2h(r1) + 2h(r2) + h(δ) (d = r1 + r2 − δ · h = 6 유효숫자 반올림 반폭) · `contact_area_check` 가 범위 밖 행 (포함 경계 · d → 0 깊은 겹침) 을 `n_boundary_excluded` 로 **따로** 세고 초과 · 상대차 · diff/tol 통계에서 뺀다 · `AREA_CHECK_TOL_RULE` 에 범위 명시 · `AREA_CHECK_MARGIN` 은 그대로 · 행 수준 `_contact_area_rows` 의 반환은 그대로 (`audit.py` 호출 호환) | `rounding_only_false_alarm` 행 (.002 / .0010000049 / .0020000051 → 토큰 .002/.001/.00200001) → `contact_area_check` 에서 **boundary** (초과 아님) · 깊은 겹침 (.0005/.0005/.000999999) → **boundary** (판정 대상 아님 = 놓친 것이 아니라 범위 밖) · 범위 안 1 % 치환 → 초과 1 · 무작위 3000 행 = 범위 안 0 밖 (**범위 안** 성적임을 시험이 명시) |
| **0010** | `LHSC-05` P2 | 계약 (a): 새 순수 기하 모듈 **`scripts/lens_geometry.py`** (`intersection_disc_area` · 같은 식 · `math.pi == np.pi` · selftest 5) · `plastic_coverage._intersection_disc_area` 는 그 **별칭** (같은 객체 · plastic ⑲) · 수확기는 `lens_geometry` 에서만 가져온다 (`PLASTIC_COVERAGE_ALLOWED` = **없음**) · 가드 `_plastic_coverage_uses` 는 패키지 경유 (`from scripts import plastic_coverage as pc`) · importlib **별칭** (`from importlib import import_module as im` 1 패스 수집) · 점 경로도 잡는다 · 독스트링에 "lint 이지 완전 증명 아님" | `ast_guard` 두 우회 → **둘 다 위반** (`bad` 비지 않음) · 수확기 소스 = plastic_coverage 사용 0 (소스 전체 AST · ⑬) · coverage_physics_vs_hertzian ① legacy 바이트 핀 그대로 (값 불변) |
| **0011** | `LHSC-06` P3 | `coverage_wall` 독스트링 · `WALLEXCL_FORMULA`: 벽 제외 = **분모 보정 proxy** — 분자 = 원 AM–SE 합 그대로 (벽 자체 접촉을 더하지 않을 뿐 ROI 밖 원판을 잘라내지 않는다) · 분모 ≤ 0 제외 뒤 편향 방향 미정 · `OK` = 계산 상태 · `mean_wallexcl_pct` = 두 벽 다 뺀 입자값의 등급별 평균 | 값 · 키 변경 없음 (문구만) |

## 2. 판정문 §7 최소 수정 목록 ↔ 대조

1. **0006** — "v2 의 비유한 입자/분모 ≤ 0 을 `0.0 · ok` 로 내지 않기.  무효 분모 · 고립 NaN · 정상 접촉 0 의 세 대조" → 셀프테스트 ⑬ ⑭ ⑮ (옛 코드 ⑬ ⑭ 실패 · ⑮ 통과 → 15/15) · Codex `audit.py` 세 픽스처 §1 표.  legacy 경로는 손대지 않았다 (요청대로).
2. **0007** — "명시적 coverage/contact 요청에서 atoms-only 성공 우회를 막기 · viewer 기본 모드 보존 · raw-atom-only 와 CSV-only 모두 · 상태 검증은 빈 문자열/임의 문자열 거부" → T11g (2 경로 × contact · coverage) · T11h (None 2 경로) · T11i · T11j (옛 코드 201/206 → 206/206).
3. **0003** — "포함 경계 반올림 반례를 검사 범위 계약 또는 공동 구간 계산으로 · 두 import 우회 회귀 추가 · 15,000 건 성적을 전역 보증으로 쓰지 않기" → 범위 계약 쪽을 택했다 (`_in_domain_rows` · 범위 밖 = 따로 셈 · 공동 구간 계산은 하지 않았다 — 포함 경계에서 면적이 r1 − r2 에 불연속이라 구간 상한 자체가 서지 않는다) · 수확기 ㉑′ 5 항 (우회 5 모양 · 옛 코드 5 실패) · 3000 행 성적은 범위 안으로 라벨.

문서 · 인계 명료화 (판정문 §7 끝): `wallexcl` = 분모 보정 proxy (0011) · v2 = 미검증 후보 연산자 · `OK` = 계산 상태 ≠ 물리 적격성 · 실제 reharvest 는 새 디렉터리 — 원장 `LHSC-06` · `LHSC-10` 과 `docs/lhs_handover_checklist_20260929.md` 에 적었다.  130/64 코퍼스 값 (접선 근처 수 · 무효 분모율 · cap 충돌률 · 제외율 · `LHSC-08`) 은 병합 뒤 재수확 · 배치에서 원자료로 보고한다 (추정으로 채우지 않는다).

## 3. Codex 스크립트를 고친 트리에 다시 돌린 결과 (`fixed_tree_reproduction/`)

환경: Linux 컨테이너 · Python 3.11.15 · NumPy 2.4.6 · pandas 3.0.5 · SciPy 1.17.1 · NetworkX 3.6.1 · Flask 3.1.3.  `LHS_REVIEW_REPO` = `da4670594` + 패치 0001–0011 ·
`LHS_REVIEW_BASELINE` = zip 의 baseline.  실 DEM · 130/64 원자료 없음.

| 스크립트 | 결과 (고친 트리) | 비고 |
|---|---|---|
| `audit.py` | `denominator_zero` / `nan_isolated_radius` = **blank** + 사유 · `valid_isolated_zero` = ok 0.0 · `legacy_comparison` 6/6 same · `ast_guard` **두 우회 = 위반** · `rounding_sweep` 0/0 · `wall_outside_numerator` 31.626… (값 그대로 — 0011 은 문구 정정) · `yield_jump` 0.0566 (그대로 — 물리 · 값 변경 없음) | `rounding_only_false_alarm` · `hertz_miss` · `3e-5_miss_deep` 는 **행 수준** `_contact_area_rows` 를 직접 불러 옛 값 그대로 (`caught` True / False / False) — 설계상 행 함수는 안 바꿨고 분류는 `contact_area_check` 에서 한다.  같은 세 행을 `contact_area_check` 에 넣으면 `n_beyond_tol` 1 (범위 안 1 % 행) · `n_boundary_excluded` 2 · `_in_domain_rows` = [False, False, True] (요청서 §1 · 수확기 ㉑′) |
| `audit_pipeline.py` | `atoms_only` = **failed** · success False · 배치 상태식 failed · stopped_after coverage · **full_metrics.json 미작성** · `status_schema` 4/4 **False** · `stale_standard` / `stale_bimodal` = failed (그대로) · 배치 copy-shim 29/29 | ⚠ 원 스크립트는 `atoms_only` 에서 `full_metrics.json` 을 `read_text()` 해 **크래시**한다 (거부가 파일을 안 쓰는 것이 기대 동작) — `read_text` 한 줄만 guard 한 사본 `audit_pipeline_tolerant.py` 로 돌렸다 (다른 줄 변경 없음) |
| `audit_harvest.py` | 수확기 selftest 0 실패 (Linux · 145 항) · 기준 ↔ 후보 legacy 키 16 호출 불일치 0 · τ base = candidate (2.0805329527696066 = 핀) | Windows 의 CRLF · 1 ULP 문제 없음 |
| `audit_cli.py` | `nested_archive_all` rc 0 · skip · `bad_json_case_dir` rc 0 (옛 CLI 경로 — `LHSC-07` 그대로 · 이번 범위 아님) · `external_case_id` rc 0 · v2 작성 | |

셀프테스트 (`selftests.log` · 검토 트리 HEAD): lens_geometry 5/5 · plastic_coverage 28/28 · coverage_physics_vs_hertzian 15/15 · lhs_descriptor_harvest 전부 통과 (㉑′ 5 항 포함) ·
lhs_webapp_batch 29/29 · test_pipeline_provenance 206/206.  전체 게이트 (검토 worktree · `check_all.sh`) = `gate.log`: **169/170** — 이 패치와 무관한 `litdb_promote.py --selftest` 가 fast 드라이버 (6 병렬 · 180 s) 에서 타임아웃 (두 번 재현 · git clone/worktree 를 하는 검사라 병렬 I/O 경합) · 같은 worktree 에서 **단독 실행은 28 s 통과** (`gate_litdb_promote_alone.log`) · main 트리 게이트 (이 요청서 커밋 전) 는 그 검사 포함 전부 통과.  "전부 통과" 로 적지 않는다.

## 4. 재현 명령

```bash
git fetch origin claude/stoic-knuth-NObVQ && git checkout -b cov-reverify <이 요청서가 든 커밋>
git am docs/reviews/codex_lhs_coverage_reverify_request_20260930/patches/*.patch     # 0001–0011 · da4670594 위에 그대로 붙는다
python3 scripts/lens_geometry.py --selftest && python3 scripts/plastic_coverage.py --selftest
python3 scripts/coverage_physics_vs_hertzian.py --selftest && python3 scripts/lhs_descriptor_harvest.py --selftest
python3 scripts/lhs_webapp_batch.py --selftest && python3 webapp/test_pipeline_provenance.py
# Codex 감사 스크립트 (zip 의 lhs_coverage_evidence_20260930/ · 별도 사본에서)
export LHS_REVIEW_REPO=<cov-reverify 트리> LHS_REVIEW_BASELINE=<zip baseline> PYTHONUTF8=1
python3 audit.py && python3 fixed_tree_reproduction/audit_pipeline_tolerant.py && python3 audit_harvest.py && python3 audit_cli.py
```

## 5. 질문

- **Q1** `LHSC-01` 계약 (a) (침대 전체 빈칸 + 사유 · 제외 수는 진단에) 가 §2 최소 해제를 만족하는가.  `am_denominator_physics_v2` 를 빈칸 침대에도 싣는 것이 "부분 합을 싣지 않는다" 와 충돌하지 않는가 (정수 개수뿐 · 면적 · 피복률 값은 전부 None).
- **Q2** `LHSC-02` 거부 반환의 모양 (`status: 'failed'` · `stopped_after` · `atoms_only: True` · `failed_stages: ['contact files missing']`) — 배치 (`lhs_webapp_batch`) 가 재개 때 다시 도는 것이 맞는가, 아니면 접촉 파일이 없는 케이스는 `partial` 류의 별도 상태여야 하는가.
- **Q3** `LHSC-03` 스키마: `cap_conflict_frac_*` 두 키를 필수에서 뺐다 (접촉 0 인 침대에서 None 이 정상).  'ok' + AM 0 개 침대 (`coverage_AM_mean_physics_v2` 없음) 를 통과시키는 것이 맞는가.
- **Q4** `LHSC-04` 지원 범위 규칙 = d − |r1 − r2| > 2h(r1) + 2h(r2) + h(δ).  두 반례를 덮는다 (오탐 행 −1e-5 · 깊은 겹침 1e-6 ≤ 2.5e-6).  안 닿음 경계 (d ≥ r1 + r2 · A = 0) 는 δ ≤ 0 행이 어차피 0 이라 규칙에 넣지 않았다 — 빠진 경계가 있는가.  "공동 구간 계산" 대신 범위 계약을 택한 것에 이의가 있는가.
- **Q5** `LHSC-05` (a) 분리 + 가드 (lint 표기) 로 DESC-03 · 계약④ 의 "Physics 호출 금지" 가 충분히 서는가.  가드가 못 보는 모양 (getattr · exec · 문자열 조립) 을 더 막을 값이 있는가.
- **Q6** 병합 순서 = 패치 순서 그대로 (0001 → 0011 · 한 항목씩 게이트) · 병합 뒤 `LHSC-01`~`06` 을 claimed_fixed 로 · 그 뒤 WSL 재수확 v3 + `--stop-after coverage` 배치 (새 디렉터리) — 이의가 있는가.

## 6. 병합 뒤

- 재수확 · coverage 배치 (새 디렉터리) → 기준선 (옛 코드 배치 `4b42179ec`) 과 비교 · 130/64 의 접선 근처 수 · 무효 분모 침대 수 · cap 충돌률 · 경계 행 수 를 원자료로 보고 (`LHSC-08` · `LHSC-10`).
- v2 열은 인계표에서 **후보 연산자** 로 라벨 (`LHSC-10`) · `wallexcl` 은 분모 보정 proxy (`LHSC-06`) — 열 사전 문구 = 생성기 7c 단계에서.
