# G2RR5-01 수정 — Codex 탐침 무변경 재실행 (배포 관문 · 10-08 밤)

- 대상 = Codex 세대 2 재검증 5 §1 G2RR5-01 (판정문 `docs/reviews/codex_review_gen2_network_reverify5_20261007.md`) · 수정 계획 `docs/reviews/g2rr5_fix_plan_20261008.md` §1 (1저자 10-08 밤 "권고대로").
- 고친 트리 = 커밋 `8b6453671` (시험 + 수정 한 커밋 · 바탕 커밋 `45230ce20`).  바뀐 파일 셋 = `scripts/lhs_release_build.py` · `scripts/run_network_194_parallel.py` · `scripts/test_lhs_release_v13.py`.
  봉인 32 (실행기 CODE_FILES) · 인계 도구 둘 (HANDOVER_FILES) 무변경 — 고친 트리에서 다시 잰 봉인 지문 code_fp = e8b2496b… (32 파일 · 발사 봉인과 같다).  감사 (cmd_audit · import_observation_problems) 무변경.
- 핀 결과 = Codex 원본 (반입본) `docs/reviews/codex_gen2_network_reverify5_evidence_20261007/evidence/r5_release_contract/results.json` ·
  `docs/reviews/codex_gen2_network_reverify5_evidence_20261007/evidence/r5_release_real_binding/results.json` · `docs/reviews/codex_gen2_network_reverify5_evidence_20261007/evidence/r5_observation_run2/results.json`.
- 요약 JSON (변이마다 핀 ↔ 고친 트리 · 명령 · 커밋 · 절대 경로 없음) = `docs/reviews/codex_g2rr5_fix_probe_rerun_20261008/release/probe_rerun_summary.json`.

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
