# 우리 트리 재현 — Codex LHS214RR 재확인 새 P3 넷 (L214R-S01–S04 · 2026-10-19)

- 우리 트리 = `298a73197` 체크아웃 (리포 밖 복제본 · 반입 문서만 더함 · 봉인 32 = `155534744` 와 같음 · 대기 지문 `2149f8738bb20b6a…`) · 이 컨테이너 (Linux · Python 3.11.17 · NumPy 2.4.6 · SciPy 1.17.1 · `OMP_NUM_THREADS=1`).
- Codex 탐침 파일은 실행하지 않았다 — 같은 절차의 파생 스크립트 넷 (이 폴더) 이 Codex 증거의 입력 (반례 문서 · 정상 레코드) 을 **읽기만** 하고 우리 코드로 다시 판정한다.
- 실행 = `python3 -B <스크립트> <우리 트리> docs/reviews/codex_lhs214rr_fix_recheck_evidence_20261019 …` (`repro_single_null.py` 는 웹앱을 import 해 `docs/db/` 에 초기 파일을 만든다 → 리포 밖 복제본에서).

| 항목 | 스크립트 → 출력 | 결과 | Codex 와 대조 |
|---|---|---|---|
| `L214R-S01` 등록 파서 공백 | `repro_fences.py` → `fences_ours.json` | 114 문서 중 CommonMark 와 활성 §3 판정이 다른 것 32 · 그 32 모두 완전한 영수증 rc 0 (현재 지문 `2149f873…` 수용) | parser_accept · 사유 · rc · bad · code_fp 차이 0 (`differences_vs_codex` = []) |
| `L214R-S02` R01 경계 시험 환경 의존 | `repro_boundary.py` → `boundary_ours.json` | 우리 등록 입력 (면적 0.500000001 · box_y …4881/82/83) = 이 환경 raw q 정확히 1.5000000000000002 · 1.5 · 1.4999999999999998 / Codex 정확 경계 입력 (면적 0.500000001001 · box_y …80614/15/16) = 이 환경 1.5000000000000044 · 1.5000000000000042 · 1.5000000000000038 (18–19 ULP 위 · 셋 다 보류) | 판정문 §2 의 Codex 환경 값 (우리 입력 → 17–19 ULP 아래) 과 방향만 반대 — 실 사슬 풀이의 끝자리가 환경마다 ~18 ULP 다르다 · 두 환경 모두 생산자 판정 (엄격 >) 은 옳다 |
| `L214R-S03` 이온 채널 요약 표지 | `repro_scope.py` → `scope_ours.json` | 정상 레코드 (H0 FULL computed · f 0.09025782) 의 `ionic_status` 를 valid_zero · valid_null · no_result (+ `no_through_path`) 로 바꿔도 content · record · stop True · τ OK · f 그대로 | 판정 칸 10 × 4 차이 0 |
| `L214R-S04` 과거 null → /single 500 | `repro_single_null.py` → `single_null_ours.json` | 정상 200 · `sigma_ratio` null 500 · 키 없음 200 · null + `phi_se` 없음 500 · `R_brug_over_full` null 200 | 판정문 §5 와 같음 |

- 한정: S01 은 Codex 가 만든 반례 문서를 그대로 읽었다 (CommonMark 기준값 = Codex 판정표의 markdown-it-py 결과 — 우리는 markdown-it-py 를 다시 돌리지 않았다).  S02 는 실 사슬 E 입력 두 묶음만 · 3 노드 정확 경계 (E5) 는 이 환경에서 기존 시험이 통과.  S03 · S04 는 Codex 의 합성 fixture 꼴 (실제 214 레코드 아님).
