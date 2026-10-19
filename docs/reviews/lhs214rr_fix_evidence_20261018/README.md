# 증거 — LHS214 재확인 반례 수정 (L214R-R01–R03 · Codex 표기 L214RR-01–03 · WEB-09 잔여) (2026-10-18)

근거 = Codex 재확인 판정문 `docs/reviews/codex_review_lhs214r_fix_recheck_20261017.md` §1–§3 · 보충 판정 `docs/reviews/codex_lhs214r_evidence_supplement_20261017.md` §3 ·
수정 계획 `docs/reviews/lhs214rr_fix_plan_20261018.md` (1저자 10-18 Q1–Q5 권고대로) · 요청서 `docs/reviews/codex_lhs214rr_fix_recheck_request_20261018.md`.
코드: R01 `91e732517` · R02 `43223d823` · R03 `f8871224b` · ★ 10-19 같은 부류 R04 `155534744` (최종 코드 = `155534744`) · 기준 = Codex 코드 핀 `60ba39e22` · 화면 기준 트리 `6cb256956`.
기계 = 이 컨테이너 (Linux · Python 3.11.17 · NumPy 2.4.6 · SciPy 1.17.1 · `OMP_NUM_THREADS=1`).

## 1. 시험 먼저 (`docs/reviews/lhs214rr_fix_evidence_20261018/tests/`)

| 항목 | 고치기 전 | 고친 뒤 | 기록 |
|---|---|---|---|
| `L214R-R01` | `scripts/test_l214r_r01_restored_full.py` 9/27 (대조 · 준비 9 만 통과) | 27/27 | `docs/reviews/lhs214rr_fix_evidence_20261018/tests/r01_before.log` · `docs/reviews/lhs214rr_fix_evidence_20261018/tests/r01_after.log` |
| `L214R-R02` | `webapp/test_web09_accepted_refresh.py` 17/18 (⑧) | 18/18 | `docs/reviews/lhs214rr_fix_evidence_20261018/tests/r02_before.log` · `docs/reviews/lhs214rr_fix_evidence_20261018/tests/r02_after.log` |
| `L214R-R03` | `scripts/supp20_input_receipt.py --selftest` 112/113 (S12g) | 113/113 | `docs/reviews/lhs214rr_fix_evidence_20261018/tests/r03_before.log` · `docs/reviews/lhs214rr_fix_evidence_20261018/tests/r03_after.log` |
| `L214R-R04` (10-19 · 같은 부류) | `scripts/test_l214r_r04_cf_label.py` 4/12 (대조 · 준비만) | 12/12 | `docs/reviews/lhs214rr_fix_evidence_20261018/tests/r04_before.log` · `docs/reviews/lhs214rr_fix_evidence_20261018/tests/r04_after.log` |

- "고치기 전" = 본 가지 작업 트리에서 새 시험 (또는 selftest 블록) 을 먼저 넣고 그 항목의 고칠 함수는 부모 커밋 판 그대로 둔 실행 (커밋 전 · R01 = 부모 `96b7d5ae9` 코드 ·
  R02 = 부모 `91e732517` 의 `webapp/app.py` · R03 = 부모 `43223d823` 의 `_md_section`).  "고친 뒤" = 그 커밋 내용.  커밋마다 `bash scripts/check_all.sh` 139 단계 "✓ 전부 통과" 뒤 push.
- R01 뒤 `webapp/test_pipeline_provenance.py` 가 269/284 — 가짜 solver 의 게시 FULL 값 999 mS/cm (q 333) · 5.0 (q 1.67) 이 생산자가 낼 수 없는 값 (q > 1.5 = 보류) 이라 새 규칙이 거부.
  그 파일의 fixture-drift 규약대로 표지 값을 4.2 (q 1.4) · 3.6 (q 1.2) 로 (단언 뜻 그대로) → 284/284 · push 전 (`91e732517` 에 같이).

## 2. Codex 탐침 무변경 재실행 (`docs/reviews/lhs214rr_fix_evidence_20261018/probe_rerun/`)

- 작업 공간 = 리포 밖 scratch: 반입 폴더 `docs/reviews/codex_lhs214r_fix_recheck_evidence_20261017/` 의 묶음 뿌리 그대로 (단 `evidence/consumers_fixtures/` 는 빼서
  `consumer_chain_derivative.py` 가 우리 기계 · 최종 코드로 생산자 fixture 를 다시 만들게) + `source/` = `f8871224b` 의 `git archive` (묶음 `source_manifest.json` 의 1,920 경로 · 없음 0) +
  `base/` = `6cb256956` 사본 (10-18 재현 때와 같음).  실행 = `python3 -E -X utf8 -B <탐침>` · 순서 = 묶음 README.  탐침 파일 바이트 무변경.
- 종료코드 (`docs/reviews/lhs214rr_fix_evidence_20261018/probe_rerun/rc.tsv`): receipt_fences 0 · numeric_adversarial 0 · display_fresh source 0 · base 0 · consumer_chain_derivative 0 · **consumer_h0_resurrection 1** —
  복원 레코드를 인계 원천 관문 (`load_tau_results` P4) 이 `FillRefusal` (세대 계약 위반 · R01 사유) 로 거부해 탐침이 그 자리에서 멈춘다 (탐침은 옛 동작 = 통과를 전제 · `docs/reviews/lhs214rr_fix_evidence_20261018/probe_rerun/consumer_h0_resurrection.stderr`).
  멈추기 전 판정값을 남기려고 파생 래퍼 `docs/reviews/lhs214rr_fix_evidence_20261018/probe_rerun/run_h0_resurrection_capture.py` (탐침을 바이트 그대로 compile · exec · 예외 시 그때까지의 report 저장 · 탐침 sha256 기록) 로 다시 돌렸다
  → `docs/reviews/lhs214rr_fix_evidence_20261018/probe_rerun/consumer_h0_resurrection_capture.json`.
- 판정값 대조 = `docs/reviews/lhs214rr_fix_evidence_20261018/probe_rerun/cmp_codex_vs_final.py` (읽기 전용 · Codex 원 출력 ↔ 최종 출력) → `docs/reviews/lhs214rr_fix_evidence_20261018/probe_rerun/cmp_codex_vs_final.json`.  최종 출력 원본 = `docs/reviews/lhs214rr_fix_evidence_20261018/probe_rerun/out/`.

| 탐침 | Codex (고치기 전 `60ba39e22`) | 최종 (`f8871224b`) |
|---|---|---|
| receipt_fences — 네 백틱 안 세 백틱 예시 §3 | rc 0 · 실패 칸 [] · 읽은 code_fp = 체크아웃 값 | rc 1 · R0 · D1 · 읽은 code_fp None |
| — 세 백틱 예시 (대조) | rc 1 · R0 · D1 | 같음 |
| numeric — H0 복원 (8 leaf) | 증서 결합 [] · 세대 g2 · τ OK · f 1.62317474 · 표지 False · 레코드 판정 True | 결합 거부 (R01 사유 · raw q `1.6231747351909949`) · 세대 invalid · τ NOT_COMPUTED · f 공란 · 레코드 판정 False |
| — Physics 복원 | 결합 [] · τ OK · f 2.5934685 | 결합 거부 (raw q `2.593468501694396`) · τ NOT_COMPUTED |
| — 경계 (라벨 복원 뒤 게시 증서 판정) | raw q 1.5 · 1.4999999999999998 · 1.5000000000000002 · 2.0 = 넷 다 None | 1.5 · 1.4999999999999998 = None · 1.5000000000000002 · 2.0 = 사유 |
| — 채택 시도 252 변이 · 장부 36 | 수용 0 · 예외 0 · 실패 0 | 같음 |
| — 주 타깃 모형 한계 관문 (복원 행) | [] | [] — 그 행은 이제 모형 한계가 아니라 기술 무효 (NOT_COMPUTED invalid_input · 세대 invalid) — 세대 관문 · τ 다시 읽기 · 배치 관문이 거부 (새 시험 B6–B9) |
| display_fresh source (13 검사) | 실패 7 (세 레이아웃 · 두 유도값 모두 옛 값의 Δ) | 실패 0 |
| display_fresh base | 실패 10 | 같음 (기준 트리) |
| consumer_chain (생산자 다시 만듦) — 다섯 사례 (`docs/reviews/lhs214rr_fix_evidence_20261018/probe_rerun/out/consumers_probe.json` 전체 — 게시 · τ · 표지 · 다시 읽기 K1–K7 · 인계 · 주 타깃 HOLD) | 주 타깃 HOLD = ml_hertz · independent_l1_h0 · independent_l2_h0 | 같음 — 다른 곳 = 다시 읽기 K1 문구 안의 실행 ID 다섯뿐 (실행 ID · 경로 · 해시 키를 뺀 전 칸 대조) |
| consumer_h0_resurrection — 10 leaf 복원 | 내용 · 레코드 판정 True · True · 정지 ①–⑨ ok · case_row OK · build_v13 27 파일 · check_v13 [] | 내용 True (구조 검사 — 설계상 그대로) · 레코드 False · 정지 False (⑦ τ — 세대 계약 · R01 사유) · case_row NOT_COMPUTED · 세대 invalid · 증서 수치 무변경 True · 인계 원천 관문 P4 FillRefusal (배포까지 못 간다) |
| — 8 leaf 만 | 정지 ④ 거부 | 같음 |

- ★ 10-19 R04 뒤 다시 (최종 `155534744` · 같은 방식 · 새 작업 공간): `probe_rerun_155534744/` — 종료코드 같음 (`rc.tsv`) · 10-18 판정값 (`f8871224b`) 과 경로 · 탐침 sha256 을 뺀 전 칸 대조 = **차이 0 칸** (`probe_rerun_155534744/cmp_f8871224b_vs_155534744.txt`) — Codex 탐침은 CF 표지 반전을 다루지 않는다 (R04 는 우리 시험이 지킨다).
- 판정값이 아닌 차이: 원 q 끝자리 (`…09949` ↔ Codex `…09995` — 10-18 재현 때와 같은 플랫폼 차) · 실행 ID · 경로 (scratch 절대 경로가 출력 JSON 에 남는다).

## 3. 무영향 대조 (`docs/reviews/lhs214rr_fix_evidence_20261018/a4_final.log` · `docs/reviews/lhs214rr_fix_evidence_20261018/a4_final.json`)

- 도구 = `docs/reviews/lhs214r_fix_evidence_20261016/a4_l214r_no_impact.py` (무변경 · 읽기 전용 · `--base 6cb256956`) — 기준 `6cb256956` ↔ 최종 트리 (`f8871224b` 체크아웃 · 깨끗) = **PASS 36/36 (159.0 s)**.
- N 생산자 16 (결과 JSON 전체 비트 같음) · T τ 소비자 6 (v1.2 194 옛 50 칸 · 새 생산자 레코드 넷 · lhsx_054) · R 배포 빌더 6 (의도 변경 2 = 10-16 L214R-02 그대로) · W 웹앱 변환 8 —
  10-16 의 같은 도구 결과 (36/36) 와 같은 판정 = R01–R03 은 정상 사례 출력을 바꾸지 않았다 (R02 는 최종 split 병합 단계 — 화면 전체는 §2 display 탐침).
- ★ 10-19 R04 뒤 (`155534744` 깨끗한 체크아웃 · 같은 도구 · 같은 기준) = **PASS 36/36 (185.7 s)** — `a4_155534744.log` · `a4_155534744.json`.

## 4. 한정

- 계약 시험 · 탐침의 합성 범위 (작은 사슬 · φ_SE > 1 합성 기하 · 배포 fixture 의 선택 1 행만 실제 경로) 는 판정문 · `docs/reviews/codex_lhs214r_fix_recheck_evidence_20261017/notes/consumers.md` 의 한정 그대로.  실제 214 오염 · 발생률 주장 아님.
- 전자 FULL 의 같은 보류 → 게시 복원 = 이번 범위 밖 (1저자 10-18 Q4).
- 새 214 · WSL · 재봉인 · 등록 비준 없음 (대기 지문만 `755325e1f24488bb…` 로 갱신 · 등록 §3 `e8b2496b…` 그대로).
