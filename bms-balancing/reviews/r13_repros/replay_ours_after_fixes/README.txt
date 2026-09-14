Codex R13 (대상 94add7b) 수정 뒤 재생 — 코드 커밋 df6413d649ef51ace16d634c3856f857d598c79d 에서 만들었다
(**U18b 실데이터 재실행·승격(37a889b) 뒤** 판. 직전 판은 ef8e8f6 에서 만든 것이고 이 디렉터리는 그것을 **덮어쓴다** —
옛 판은 git 이력에 있다).

왜 다시 뽑았나: 조건 7 의 실데이터 재실행이 끝나 정본 `out/` 이 새 계약으로 바뀌었다. 이 묶음의
`check_u14_out_schema_only.txt` 는 바로 그 `out/` 을 재는 것이라 **승격 전 숫자를 그대로 두면 증거가 거짓이 된다.**
러너 넷의 leaf 별 판정은 ef8e8f6 판과 **동일**하다 (아래) — 바뀐 것은 정본의 상태뿐이다.

왜 코드 커밋에서 만드나: 러너가 `--expected-head` 의 커밋을 materialize 해서 돌고, 도구 자신
(`replay_codex_r*.py` · `reviews/evidence_gate.py`)의 bytes 가 그 커밋의 blob 과 같아야 `evidence_eligible: true` 다.
작업트리는 실행 전후 clean (`git status --porcelain` 은 이 디렉터리의 파일뿐 — 러너 JSON 의 `dirty_paths` 가 그것을 적는다).

    git diff ef8e8f6 HEAD --name-only -- '*.py' '*.sh'      # → 0 개여야 한다 (증거 커밋은 이 디렉터리만 더한다)

만든 명령 (bms-balancing 에서, HEAD=$(git rev-parse HEAD), R6_OLD_OUT=`git archive bfc4623^ out` 26 파일):
    python3 reviews/r6_repros/codex_r6_mutation_audit.py                          > codex_r6_mutation_audit.txt
    python3 reviews/r6_repros/codex/replay_codex_r6_adapted.py --target . --output replay_codex_r6_adapted.json
    python3 reviews/r6_repros/codex/mutation_adapted.py                           > mutation_adapted.txt
    python3 reviews/r{7,9,10,11}_repros/replay_codex_r*.py --target . --expected-head "$HEAD" --output replay_codex_r*.json
    python3 scripts/check_u14.py --new out --schema-only                          > check_u14_out_schema_only.txt
    PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/ -q -p no:cacheprovider      > pytest_full.txt
    bash matlab/tests/run_all.sh                                                  > matlab_smoke.txt 2> matlab_smoke.txt.stderr.txt

종결 계약 (Codex R13 P1-3) — 옛 기대치로 읽으면 오판한다:
  · rc 0  = `report_complete` (요청 leaf 마다 판정이 있고 `오류` 없음). **closed 가 아니다.**
  · `closed` = 요청 leaf **전부** 반례 소멸 (엄격). 전제 변경·환경상 불가·우리 코드 밖·미실행은 `excluded` 로 적고 closed 에서 뺀다.
  · `closed_with_substitutes` = 제외마다 대체 증거의 **이름**이 있을 때만 참. 없는 것은 없다고 적었다.
  · 집계는 `evidence_gate.summarize_verdicts` 한 자리 (네 러너 공용). GO 소비자는 rc 가 아니라 `closed` / `closed_with_substitutes` 를 읽는다.

네 재생기 전부 evidence_eligible: true · instrument_sealed: true · package_digest_ok: true · target_head df6413d6….

  replay_codex_r7.json    반례 소멸 5/6 · 제외 1 — R7-03 전제 변경 (대체 test_d7_03 회귀)
                          report_complete true · closed **false** · closed_with_substitutes true
  replay_codex_r9.json    반례 소멸 12/12 · closed **true**
  replay_codex_r10.json   반례 소멸 20/22 · 제외 2 — snapshot:argv 우리 코드 밖 (대체 adapted:argv-vector) ·
                          u18:shape_duplicates 전제 변경 (fingerprint "TypeError: 'NoneType' object is not subscriptable",
                          대체 adapted:duplicate-states) · closed **false** · closed_with_substitutes true
  replay_codex_r11.json   leaf 37 · 반례 소멸 32/37 · 제외 5 — root:profile_grid 전제 변경 · data:shape_wrapper 환경상 불가
                          (fingerprint "wsl.exe", 대체 publish:shape_step) · publish:matrix_filtered_canonical 전제 변경
                          (대체 data:matrix_subset) · publish:profile_grid1_canonical 미실행 (그룹 중단, 대체 data:profile_grid) ·
                          publish:profile_partial_stdout 미실행 (그룹 중단) — **대체 증거 없음**
                          → closed **false** · closed_with_substitutes **false** (정직하게). ef8e8f6 판과 leaf 별 판정 동일.

  replay_codex_r6_adapted.json   "mode": "full" 6/6 닫힘  (R6_OLD_OUT = `git archive bfc4623^ out`, 26 파일)
  codex_r6_mutation_audit.txt    8/8 CAUGHT · MISSED 0
  mutation_adapted.txt           5/5 CAUGHT · MISSED 0  (같은 R6_OLD_OUT)
  check_u14_out_schema_only.txt  **rc 0** · blocked_by 전부 0 (`baseline_absent` 1 만 — schema-only 는 baseline 을 안 본다)
                                 — 조건 7 의 실데이터 재실행(U18b)이 정본을 새 계약으로 다시 서명했다. 직전 판의 40 · 25 · 6 · 1 은
                                 **없어진 것이 아니라 옮겨갔다**: 옛 정본은 `out/archive/legacy_r6_u14/` 에 얼려 보존했고
                                 (`check_u14 --new out/archive/legacy_r6_u14 --schema-only` 가 그 네 수를 그대로 낸다), 회귀
                                 `test_d8_02` 가 이제 그 경로를 표본으로 쓴다. **산출 숫자는 하나도 안 움직였다**
                                 (`--new out_u18b --old out` 의 `numbers 0`, 명부 13/13/13). 옛 sidecar 는 소급 보수하지 않았다.
  pytest_full.txt                277 passed  (PYTHONDONTWRITEBYTECODE=1 · -p no:cacheprovider — 트리를 더럽히지 않게)
  matlab_smoke.txt               Octave 전 단계 "전부 통과"

각 파일 옆의 `*.rc.txt` 가 그 실행의 종료 코드다 — 이번엔 **전부 0** 이다 (직전 판은 check_u14 만 2 였고, 그것이 승격으로 0 이 됐다).
⚠ 재생성할 때 `tests/` 전체 실행과 러너를 **동시에 돌리지 않는다** — `test_d8_07` 이 같은 `replay_codex_r7.py` 를 부르므로
  겹치면 그 테스트만 거짓으로 빨개진다 (U18-04, 2026-09-14 실측).
R13 항목: P1-1~P1-4 · P2-1~P2-5 · §5 Q6 전부 닫음 — 회신은 `reviews/R13_RESPONSE.md`.
