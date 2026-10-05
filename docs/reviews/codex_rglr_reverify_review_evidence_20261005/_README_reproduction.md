# Codex RGLR 3차 재검증 — 반입 + 우리 트리 재현 (2026-10-05 밤)

- 판정문: `docs/reviews/codex_review_rglr_reverify_20261005.md` (= zip 의 `codex_review_rglr_reverify_20261005.md` · sha256 `b4fde73d97ca1bc4472b317159f1437cd956c298ff93886a37b696513a33fa0d`) —
  **기존 RGLR-01 · 02 · 03 닫힘 · 새 P1 없음 · 새 P2 셋 (`RGLR2-01` ~ `03`) · WEB-03 · LHS-33 부분 · LW 194 제외 닫힘 (제외 기능만)**.
  격리된 WSL 소형 통합시험만 **조건부 GO** · 공식 재봉인 · 194 건 생산 · 인계 **HOLD**.
- 반입 원본: 사용자 전달 zip `1cb4d1b9-codex_rglr_reverify_review_20261005.zip` — 5,521,273 B · sha256 `762bfe7c03f0b3af7bfa02dc69005646ade17c4af2d983d3ce9f6cdc837336e7` · `package_manifest.json` 669/669 일치.
- 핀 `dbe0f076d7b948b8ebcfa85a02a391125b104fe2` — `source_manifest.json` 의 443 파일 git blob 이 **핀의 blob 과 443/443 같다**.
- 이 폴더 = zip 에서 아래 467 개를 뺀 나머지 + 이 README + `_reproduction_compare_linux.json`.
  뺀 것 (sha256 은 그 JSON 의 `excluded_from_repo`): 핀 소스 사본 443 (blob 동일) · `diffs/` 20 (핀 사이 git diff · 재생성 가능) ·
  `inputs/` 3 (우리 요청서 · 2차 판정문 사본 · 원장 발췌) · 판정문 원본 (위 경로로 반입).  ⇒ 탐침 재실행은 **zip 원본**을 풀어 그 안에서.

## 우리 트리 재현 — 탐침 무변경 (Linux · HEAD `02913f060`)

- `verify_source.py` 를 우리 HEAD 내보내기 (`git archive`) 에 대고: **441/443 같음** — 다른 둘 = `CLAUDE.md` · 요청서 (핀 SHA 줄 · 믹서 행) · 코드 차이 없음.
- `run_probes.py` (network · lw · vm · precision · raw18 · handover · handover_diff) **rc 0** · `run_tests.py` 13 묶음 **rc 0**
  (tau 51/51 · pipeline 265/265 · tau_status 32/32 · chain 10/10 · network 30/30 · boundary 8/8 (⑨ SKIP = 내보내기에 git 객체 없음 · raw18 이 대신 대조) ·
  **lw 118/118** (Codex 는 real14 fixture 부재로 108/109 — 우리는 fixture 가 있어 전체 재인증) · lw_labels 70/70 · lhs 281/281 · stress_audit 12/12 · group 44/44 · grade 19/19 · receipts 102/102).
- 증거 JSON 10 개 대조 — **미분류 차이 0** · 값 차이 최대 1.6e-16 (부동소수 1 ULP) · 나머지 차이는 분류 안
  (run_id · 합성 산출 파일 해시 · 시각 · 합성 입력 다이제스트 · 임시 폴더 이름 · 경로 구분자 · 단계 stdout · 화면 행 안 run_id · 실행 시간 · Python/NumPy 버전 · Windows ↔ Linux 원시 hex).
  raw18: 같은 플랫폼 안 옛 ↔ 새 18/18 경계 · 원시 hex 동일 · `solve_network` AST 동일 (Codex 와 같다).

### 망 경로 (실 CLI · 실 helper · Stage E 대역)

| 경우 | stop | 상태 | failure_kind | active_status | previous_generation_kept |
|---|---|---|---|---|---|
| `positive` | true | done | — | success | — |
| `no_through` | true | done | — | success | — |
| `legitimate_band` | true | done | — | success | — |
| `solver_failed_stop` | true | failed | solver | none | false |
| `solver_failed_general` | false | failed | solver | none | false |
| `ratio_times4` | true | failed | candidate_rejected | none | false |
| `band_ratio_missing` · `nan` · `negative` · `band_fraction_above1` | true | failed | candidate_rejected | none | false |
| `rejected_retry_preserves_generation` | true | failed | candidate_rejected | success | true (6 파일 동일) |
| `write_failure_after_stamp` | true | failed | publish_exception | success | true (6 파일 동일) |
| `write_failure_first_run` | true | failed | publish_exception | none | false |
| **`general_ratio_times4`** (RGLR2-01) | false | **done** | — | success | — |
| **`general_band_ratio_missing`** (RGLR2-01) | false | **done** | — | success | — |
| **`rollback_destination_failure`** (RGLR2-02) | true | failed | publish_exception | **success** | **true** (실제 = 혼합 세대) |

- RGLR2-01: 일반 경로가 σ_ratio ×4 (0.01601552 · 차원 0.012012 mS/cm 그대로) 와 L1 σ_ratio None 을 **done** 으로 게시 — τ 인계는 두 경우 모두 NOT_COMPUTED (invalid_input) ·
  등급 getter τ² 는 10.984589697866408 · 6.081410125544994 (차원 σ 로 계산 · 손상을 못 본다).
- RGLR2-02: 실패 사유에 *"full_metrics 되돌림 실패"* 가 있는데 attempt 는 `previous_generation_kept = true` · `active_status = success` ·
  화면 행 *"활성 세대 … 의 값 (이전 성공 세대 그대로)"* · full_metrics run_id ≠ provenance run_id · 등급 getter τ² 15.071032718534699 (새 full_metrics 값).

### LW · VM · 정밀도 · 인계

- LW (실 CSV → 파서 → LW): `lw_replay.json` Codex 와 차이 0 — NaN · 문자열 · Inf · 틀린 virial · NaN 이 가린 틀린 virial · 직접 dict 결손 = FAILED.
- VM (RGLR2-03): 입자 `(1073.1, 1073.1, 1073.1000001073098)` 의 전개식 근호 −4.656612873077393e-10 → clamp 0 · 정확한 근호 1.1515417990400524e-14 ·
  둘째 입자 `(0, 0, 1.0730991562013514e-07)` 와 정확 VM 같음 (정확 CV 0 %) → 실 함수 **vm_cv 100.0 · computed** (Python float · NumPy float64 둘 다) · 양성 대조 (둘 다 둘째 응력) CV 0.0 computed.
- 정밀도: `precision_boundary.json` 차이 0 (936 경우 · 양수 648 수용 · 반올림 0 288 거부 · 잔차/허용폭 최대 0.9872210615678688).
- 인계: `handover_before_after.json` · `handover_replay.json` 차이 0 (130 · 64 × 두 묶음 · 표 · 열 사전 바이트 동일).

## 한정 (Codex 그대로)

- 합성 fixture · 소형 CLI · 탐침 변조다 — 운영 코퍼스에 이 손상이 있다는 증거가 아니다.  일반 경로 반례는 Stage E 대역 (실 Stage E 수치 재현 아님).
- RGLR2-02 는 I/O 실패 둘 (성공 기록 쓰기 · full_metrics 복원) 이 함께 필요하다 — 한 번 실패의 보통 경로는 6 파일을 보존한다.
- RGLR2-03 은 거의 정수압인 아주 작은 편차응력 경계 — 194 침대에서의 빈도 · 크기는 측정 안 함.
- WSL · 실 Stage E · real14 원자료 회귀 · 재봉인 · 194 건 실행은 이 판정 범위 밖.
