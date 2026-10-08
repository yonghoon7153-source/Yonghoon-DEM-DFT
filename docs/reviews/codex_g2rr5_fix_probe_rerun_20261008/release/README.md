# G2RR5-01 수정 — Codex 탐침 무변경 재실행 (배포 관문 · 10-08 밤)

- 대상 = Codex 세대 2 재검증 5 §1 G2RR5-01 (판정문 `docs/reviews/codex_review_gen2_network_reverify5_20261007.md`) · 수정 계획 `docs/reviews/g2rr5_fix_plan_20261008.md` §1 (1저자 10-08 밤 "권고대로").
- 고친 트리 = 커밋 `8b6453671` (시험 + 수정 한 커밋 · 바탕 커밋 `45230ce20`).  바뀐 파일 셋 = `scripts/lhs_release_build.py` · `scripts/run_network_194_parallel.py` · `scripts/test_lhs_release_v13.py`.
  봉인 32 (실행기 CODE_FILES) · 인계 도구 둘 (HANDOVER_FILES) 무변경 — 고친 트리에서 다시 잰 봉인 지문 code_fp = e8b2496b… (32 파일 · 발사 봉인과 같다).  감사 (cmd_audit · import_observation_problems) 무변경.
- 핀 결과 = Codex 원본 (반입본) `docs/reviews/codex_gen2_network_reverify5_evidence_20261007/evidence/r5_release_contract/results.json` ·
  `docs/reviews/codex_gen2_network_reverify5_evidence_20261007/evidence/r5_release_real_binding/results.json` · `docs/reviews/codex_gen2_network_reverify5_evidence_20261007/evidence/r5_observation_run2/results.json`.
- 요약 JSON (변이마다 핀 ↔ 고친 트리 · 명령 · 커밋 · 절대 경로 없음) = `docs/reviews/codex_g2rr5_fix_probe_rerun_20261008/release/probe_rerun_summary.json`.
- ★ 10-08 밤 잔여 수정 (1저자 Q6 (가) — §4 의 남는 것) = 커밋 `7153a7d6a` (결합 기록 v2 · 바탕 커밋 `93d1370d1`) · 같은 탐침 무변경 재실행 = §7 ·
  요약 JSON = `docs/reviews/codex_g2rr5_fix_probe_rerun_20261008/release/probe_rerun_summary_residual.json`.  §1–§6 은 `8b6453671` 재실행 기록 그대로.

## 1. 방법

- 탐침 셋 = **무변경** — `docs/reviews/codex_gen2_network_reverify5_evidence_20261007/probes/r5_release_contract.py` · `docs/reviews/codex_gen2_network_reverify5_evidence_20261007/probes/r5_observation.py` ·
  `docs/reviews/codex_gen2_network_reverify5_evidence_20261007/probes/r5_release_real_binding.py`.
- driver = 메인 세션 스크래치 (리포 밖) 의 setup_repro · run_repro — 반입 기록 `docs/reviews/codex_gen2_network_reverify5_evidence_20261007/_README_reproduction.md` §3 의 우리 트리 재현과 같은 driver.
  소스 = 고친 커밋에서 source_manifest 469 경로를 git archive (핀과 459 같음 · 10 다름 = 반입 기록 §3 의 7 + 이번 셋) · evidence/ 는 빈 폴더에서 · 탐침 = python3 -I -X utf8 -B · 차례로 (동시 실행 없음).
- r5_release_real_binding 이 먹는 실패 감사 JSON = 같은 재현 뿌리에서 r5_observation 이 **새로** 만든 것 (Codex 의 것이 아니다) — 그 실패 binding (expected parser 1 · observed parser 없음) 은 핀 원본과 **같다**.
- 비교 = 스크래치의 읽기 전용 스크립트 (두 results.json 을 행마다 맞대고 · 고친 커밋의 계약 함수를 r5_observation 의 결합 17 에 적용) — 산출이 위 요약 JSON.

```
# S = 메인 세션 스크래치 · R = 새 빈 재현 뿌리 · WT = 이 worktree
python3 -I $S/r5tools/setup_repro.py $S/r5x/slim/gen2_network_reverify5_20261007 $R $WT 8b6453671d3a17e3ab53046e57d42fbe0af1f4b8
python3 -I $S/r5tools/run_repro.py $R r5_release_contract       # rc 0 · 19.6 s
python3 -I $S/r5tools/run_repro.py $R r5_observation            # rc 0 · 9.8 s
python3 -I $S/r5tools/run_repro.py $R r5_release_real_binding   # rc 0 · 0.8 s
```

## 2. 결과 — r5_release_contract (상세 production194 픽스처 · v13_reread_tau 만 대역)

| 변이 | 핀 (`aa7ec7fe9`) | 고친 트리 (`8b6453671`) |
|---|---|---|
| control | 생성 · check [] | 생성 · check [] |
| 기존 계약 변이 11 (reread 8 · 관측 내부 문제 · outside · 결합 시도 하나 결손) | 거부 · 산출 없음 | 거부 · 산출 없음 (관문 문제 수 같음) |
| binding_payload_null | **생성 · check []** | 거부 · 산출 없음 (관문 문제 1 · G2RR5-01 시도 값) |
| binding_parser_absent | **생성 · check []** | 거부 (1 · 시도 값 observed ≠ expected) |
| binding_parser_zero | **생성 · check []** | 거부 (1 · 시도 값) |
| binding_unplanned_process | **생성 · check []** | 거부 (2 · 시도 값 계획 밖 + 합계 Σ observed 971 > n_finalized 970) |
| binding_count_bool | **생성 · check []** | 거부 (1 · 시도 값 bool) |
| observation_finalized_zero | **생성 · check []** | 거부 (1 · 합계 Σ observed 970 > n_finalized 0) |
| 재판정 — 좋은 묶음의 증거를 위 여섯으로 바꾸고 빌드 manifest 의 캐시 sha256 을 지금 파일에 맞춘 위조 | 문제 0 (여섯 모두) | 문제 1 · 1 · 1 · 2 · 1 · 1 (G2RR5-01) |
| control 되돌림 · 제출 상세 두 기록 (계약) | [] · 문제 0 | [] · 문제 0 |

## 3. 결과 — r5_release_real_binding (실제 audit CLI 가 낸 실패 binding 을 상세 194 픽스처에 이식)

| 행 | 핀 | 고친 트리 |
|---|---|---|
| real_failure_summary_present (최상위 요약 유지) | 거부 · 산출 없음 | 거부 · 산출 없음 (관문 문제 2 = 최상위 요약 + G2RR5-01 시도 값) |
| only_top_failure_list_cleared (최상위 요약 하나만 []) | **생성 · check []** | 거부 · 산출 없음 (관문 문제 1 = G2RR5-01 시도 값) |

## 4. 결과 — r5_observation (감사 CLI · 이번 수정 밖 — 무변경 확인)

- 17/17 기대 결과 (핀 17/17) · 행마다 rc · 관측 문제 문자열 · stage_binding = 핀과 **차이 0** (감사 출력 그대로).
- 고친 커밋의 계약 함수를 그 17 감사의 결합 시도에 적용 (읽기만): rc 0 통제 다섯 (control_old_fallback · control_new_plan · plan_missing_current_fallback · csv_fallback_legitimate ·
  noncompleted_unfinalized) = 계약 문제 0 (**과잉차단 없음** — 두 계획 출처 · CSV 정당한 생략 · 죽은 시도의 미최종 영수증 포함) · 개수 불일치 열 (pair_missing 다섯 · parser_final_missing ·
  coverage_pair_missing_contact_duplicate · unexpected_duplicate_parser · only_worker_solver · plan_mismatch) = 시도마다 계약 문제.
- ⚠ **남는 것 (관찰 · 함수 수준 확인 · G2RR5-01 범위 밖)**: unknown_stage · stage_e_out_of_scope (감사 rc 1 — 분류 밖 단계 이름) 의 결합 값은 자기모순이 없어 계약 문제 0 이다 —
  실행기가 분류 밖 단계를 executed 에서 빼고 결합 기록에 그 칸이 없다.  그 결합을 상세 194 픽스처에 넣고 최상위 요약만 [] 로 하면 고친 배포 관문도 문제 0 (요약 JSON residual_out_of_scope · 대조 = 같은 방법의 parser 결손 = 문제 1).
  막으려면 결합 기록에 칸을 더해야 한다 = 감사 출력 (cmd_audit) 변경 → 판정문 §7 "범위를 늘리지 않는다" · 계획 §1 "감사 쪽은 바꾸지 않는다" 밖 — 메인 세션 · 1저자 판단.
  → ✅ **닫힘 (10-08 밤 · 1저자 Q6 (가) · 커밋 `7153a7d6a` · §7)** — 결합 기록 v2 에 그 칸 (unclassified) 을 더했다 · 같은 두 결합 + 최상위 요약 [] = 고친 관문 문제 1.

## 5. 같은 커밋의 시험

| 시험 | 고치기 전 (시험 먼저) | 고친 뒤 |
|---|---|---|
| `scripts/test_lhs_release_v13.py` | 173/173 (V20 전) → V20 추가 178 PASS · 17 FAIL (V20a00–a07 build · check 16 + V20e) | 195/195 |
| `scripts/run_network_194_parallel.py` --selftest | 117/117 (㉟i 전) → ㉟i 추가 117/120 | 120/120 |
| `scripts/lhs_release_build.py` --selftest | — | 31/31 (이 변경과 무관) |

## 6. 한정

- 이 재실행은 **배포 관문 증거의 수용 · 거부**만 본다 (판정문 §8 과 같은 한정) — 194 생산 · WSL 실덤프 · S3 · DEM/MPM 을 돌린 것이 아니다.
- 핀 쪽 = Codex 원본 JSON (Windows) · 고친 쪽 = 이 컨테이너 (Linux · Python 3.11.15) — 관문 판정 (생성 · 거부 · 문제 수) 만 맞댄다.
- 실제 감사 JSON 은 r5_observation 의 한 케이스 합성 감사다 — 실제 194 의 감사가 아니다.

## 7. 잔여 수정 재실행 — 결합 기록 v2 (커밋 `7153a7d6a` · 10-08 밤)

- 수정 = 실행기 audit 가 완료 시도 결합 기록마다 분류 밖 단계 이름 unclassified (정상 = []) 를 싣는다 · 결합 기록 스키마 np194_import_obs/stage_binding/v1 → v2 ·
  옛 v1 = 실행기 이름 표 (IMPORT_OBS_STAGE_SCHEMA_RETIRED) · 계약이 그 칸 (문자열 목록 · 빈 목록) 을 요구 · 배포 관문이 옛 v1 감사를 "고친 실행기로 감사를 다시
  돌릴 것 (re-run audit with the fixed runner)" 로 거부.  감사 판정 (rc · 봉인 판정 · merged) · 사유 문구는 그대로.  바뀐 파일 = 이번에도 셋 (봉인 32 · 인계 도구
  무변경 · code_fp = e8b2496b… 그대로).
- 방법 = §1 과 같은 driver · 같은 탐침 셋 무변경 · 새 빈 재현 뿌리 · 소스 = 커밋 `7153a7d6a` 의 469 경로 (핀과 456 같음 · 13 다름 = §1 의 10 + 병합된 G2RR5-02 · 03 의
  셋 (CLAUDE.md · g2_network_reread · wsl_network_smoke)) · setup_repro 의 rev 만 7153a7d6a17104688c1e3fd7e560c59d2f64f279 · 실행 시간 18.1 · 8.7 · 0.7 s (전부 rc 0).

| 탐침 · 검사 | 핀 (`aa7ec7fe9`) | `8b6453671` (§2–§4) | 잔여 수정 (`7153a7d6a`) |
|---|---|---|---|
| r5_observation — 기대 결과 · rc · 사유 문자열 · 봉인 판정 · merged | 17/17 | 핀과 차이 0 | 17/17 · rc 17/17 · 사유 문자열 **바이트 같음** 17/17 · 판정 · merged 17/17 |
| r5_observation — 결합 기록 | v1 | 핀과 같음 | 스키마 값 (v1 → v2) · 시도마다 새 칸 unclassified **만** 다름 17/17 · unclassified = [] 15 행 · ['Mystery Stage'] (unknown_stage) · ['Stage E (literature-grounded grain corrections)'] (stage_e_out_of_scope) |
| 그 17 결합에 계약 (읽기만) | — | rc 0 다섯 = 0 · 개수 불일치 열 = 문제 · **분류 밖 둘 = 0** | rc 0 다섯 = 0 (과잉차단 없음) · 개수 불일치 열 = 문제 · **분류 밖 둘 = 문제** |
| 분류 밖 두 결합 + 최상위 요약 [] → 고친 배포 관문 (상세 194 픽스처) | — | **문제 0 (통과)** | 문제 1 · G2RR5-01 (거부) — 대조 parser 결손 = 문제 1 |
| 옛 v1 감사 (픽스처 · 스키마 v1 · unclassified 없음) → 배포 관문 | — | 통과 (그때 지금 형식) | 거부 1 — "고친 실행기로 감사를 다시 돌릴 것 (re-run audit with the fixed runner …)" |
| r5_release_contract | control 생성 · binding 변이 여섯 생성 | control 생성 · 여섯 거부 | 같음 (control 생성 · check [] · 기존 11 거부 · 여섯 거부 · 캐시 위조 재판정 1 · 1 · 1 · 2 · 1 · 1 · 되돌림 []) |
| r5_release_real_binding | 요약 유지 거부 · 요약만 [] 생성 | 두 행 거부 | 두 행 거부 · 우리 실패 binding = 핀과 같음 (새 칸 unclassified [] 만 더) |

- 같은 커밋의 시험 (시험 먼저 — 지금 코드 `93d1370d1` 에서 먼저 확인):
  `scripts/test_lhs_release_v13.py` 195/195 → V20f · V20g 추가 + V19b 스키마 기대 v2 = 고치기 전 198 PASS · 7 FAIL (V20f1 · f2 · g1 build · check 6 + V19b) → 205/205 ·
  `scripts/run_network_194_parallel.py` --selftest 120/120 → ㉟j 추가 = 고치기 전 120/124 → 124/124 · `scripts/lhs_release_build.py` --selftest 31/31.
- ⚠ 영향: 이미 있는 v1 감사 기록 (예: 기존 pilot ROOT 의 seal_audit.json) 은 이제 배포 관문이 거부한다 — WSL 에서 같은 ROOT 에 읽기 전용 audit 를 다시 돌리면
  v2 기록이 나온다 (계산 재실행 불요).  한정은 §6 그대로.
