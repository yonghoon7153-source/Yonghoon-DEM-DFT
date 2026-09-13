Codex R13 (대상 94add7b) 수정 뒤 재생 — 코드 커밋 d5d143f03f06ddc38abc8776f513881d259c3014 (tree 6c978e8d5ec8…) 에서 만들었다.

왜 코드 커밋에서 만드나: 러너가 `--expected-head` 의 커밋을 materialize 해서 돌고, 도구 자신
(`replay_codex_r*.py` · `reviews/evidence_gate.py`)의 bytes 가 그 커밋의 blob 과 같아야 `evidence_eligible: true` 다.
작업트리는 실행 전후 clean (`git status --porcelain` 0 줄, 이 디렉터리 제외).

    git diff d5d143f HEAD --name-only -- '*.py' '*.sh'      # → 0 개여야 한다 (증거 커밋은 이 디렉터리만 더한다)

⚠ **이번 라운드가 러너의 종결 계약을 바꿨다** (Codex R13 P1-3) — 옛 기대치로 읽으면 오판한다:
  · rc 0  = `report_complete` (요청 leaf 마다 판정이 있고 `오류` 없음). **closed 가 아니다.**
  · `closed` = 요청 leaf **전부** 반례 소멸 (엄격). 전제 변경·환경상 불가·우리 코드 밖·미실행은 `excluded` 로 적고 closed 에서 뺀다.
  · `closed_with_substitutes` = 제외마다 대체 증거의 **이름**이 있을 때만 참. 없는 것은 없다고 적었다.
  · `rc_reason` 은 문자 그대로 "보고 완료 — 반례 소멸 N/M · 제외 K (…)". "모든 case 가 닫혔다" 는 더 이상 없다.
  · 집계는 `evidence_gate.summarize_verdicts` 한 자리 (네 러너 공용).
  GO 소비자는 rc 가 아니라 `closed` / `closed_with_substitutes` 를 읽는다.

네 재생기 전부 evidence_eligible: true · instrument_sealed: true · package_digest_ok: true · ran_in "격리 snapshot".

  replay_codex_r7.json    반례 소멸 5/6 · 제외 1 — R7-03 전제 변경 (대체 test_d7_03 회귀)
                          report_complete true · closed **false** · closed_with_substitutes true
  replay_codex_r9.json    반례 소멸 12/12 · closed **true**
  replay_codex_r10.json   반례 소멸 20/22 · 제외 2 — snapshot:argv 우리 코드 밖 (대체 adapted:argv-vector) ·
                          u18:shape_duplicates 전제 변경 (fingerprint "TypeError: 'NoneType' object is not subscriptable",
                          대체 adapted:duplicate-states) · closed **false** · closed_with_substitutes true
  replay_codex_r11.json   leaf **37** (전 판 record 35 — publish:* 가 3 leaf 를 숨겼다) · 반례 소멸 32/37 · 제외 5 —
                          root:profile_grid 전제 변경 · data:shape_wrapper 환경상 불가 (fingerprint "wsl.exe", 대체 publish:shape_step) ·
                          publish:matrix_filtered_canonical 전제 변경 (fingerprint, 대체 data:matrix_subset) ·
                          publish:profile_grid1_canonical **미실행 (그룹 중단)** (대체 data:profile_grid) ·
                          publish:profile_partial_stdout **미실행 (그룹 중단)** — **대체 증거 없음**
                          → closed **false** · closed_with_substitutes **false** (정직하게)
                          data:shape_wrapper 의 `세부` 는 이제 문장 전체다 (전 판은 `[0]` 절단으로 "원" 한 글자).

  replay_codex_r6_adapted.json   "mode": "full" 6/6  (R6_OLD_OUT = `git archive bfc4623^ out`, 26 파일)
  codex_r6_mutation_audit.txt    8/8 CAUGHT · MISSED 0
  mutation_adapted.txt           5/5 CAUGHT · MISSED 0  (같은 R6_OLD_OUT)
  check_u14_out_schema_only.txt  rc 2 · promotion_eligible false · blocked_by schema 59 · provenance_cols 27 · content 5 · provenance 1
                                 — R12 보관본과 **동일**. 이번 라운드의 검사 추가(구성원·감사 내용·타입/모양·env 축·BOM)로
                                 현행 out/ 의 숫자는 하나도 안 움직였다.
  pytest_full.txt                253 passed  (PYTHONDONTWRITEBYTECODE=1 · -p no:cacheprovider — 트리를 더럽히지 않게)
  matlab_smoke.txt               Octave 전 단계 "전부 통과"

각 파일 옆의 `*.rc.txt` 가 그 실행의 종료 코드다. 남은 R13 항목: §5 Q6 (ne_shape 전용 kind/schema) — 열려 있다.
