자체 적대적 리뷰(6 렌즈, 35 건) 수정 뒤 재생 — 코드 커밋 c7217c04f939889e88b915575fce6997005072aa 에서 만들었다.

왜 코드 커밋에서 만드나: 러너가 `--expected-head` 의 커밋을 sparse worktree 로 materialize 해서 돌고, 도구 자신
(`replay_codex_r*.py` · `reviews/evidence_gate.py`)의 bytes 도 그 커밋의 blob 과 같아야 `evidence_eligible: true` 다.
이번 라운드는 그 봉인 자체를 두 곳 고쳤다 — `instrument_sealed` 이 `--no-filters` 를 쓰게 했고(C07), 러너가
`-P -E` 로 재실행해 봉인을 import 앞에 두게 했다(C08).

    git diff c7217c0 HEAD --name-only -- '*.py' '*.sh'      # → 0 개 (코드는 그대로다)

네 재생기 전부 evidence_eligible: true · instrument_sealed: true · package_digest_ok: true ·
expected_tree ae9e48479805… · ran_in "격리 snapshot".

  replay_codex_r6_adapted.json  "mode": "full" 6/6
  replay_codex_r7.json          반례 소멸 5 · 전제 변경 1 (R7-03)
  replay_codex_r9.json          반례 소멸 12
  replay_codex_r10.json         반례 소멸 20 · 우리 코드 밖 1 (snapshot:argv) · 전제 변경 1 (u18:shape_duplicates)
  replay_codex_r11.json         반례 소멸 32 · 전제 변경 2 (publish:* · root:profile_grid) · 환경상 불가 1
                                (data:shape_wrapper — 원본이 wsl.exe 를 부른다)

"전제 변경" 과 "환경상 불가" 는 닫힘으로 세지 않았고, 각각 fingerprint 를 봉인해 두어 아무 예외나 그렇게
읽히지 않는다.

⚠ 이번 라운드가 재생기의 계약을 둘 바꿨다:
  · 러너 rc 가 `evidence_eligible` 을 반영한다 (증거가 아닌 실행은 0 이 아니라 3, 자체 리뷰 C19)
  · `-O`(PYTHONOPTIMIZE) 는 재실행 **전에** 거부한다 (`-E` 가 그 환경값을 무시하므로, R10 P2-4 를 지키려면
    거부를 앞에 둬야 한다)

그 밖:
  pytest_full.txt              236 passed
  matlab_smoke.txt             Octave 전 단계 통과 ("전부 통과")
  codex_r6_mutation_audit.txt  8/8 CAUGHT · MISSED 0
  mutation_adapted.txt         5/5 CAUGHT · MISSED 0 (R6_OLD_OUT = bfc4623^ 의 out)
  check_u14_out_schema_only.txt rc 2 · promotion_eligible false
      새 스키마 누락 59 · 기준/대상 입력 출처 열 27 · 내용 5 · provenance 1
      ⚠ R11 라운드(28 · 24 · 4)보다 커진 것은 **요구하는 축이 늘었기 때문**이다 (matrix 행의 `combo_roster`,
        명부가 `ne_shape_*.csv` 까지 세는 것, provenance 부재를 unsafe 로 세는 것). 숫자는 하나도 안 움직였다.

각 파일 옆의 `*.rc.txt` 가 그 실행의 종료 코드다 — 전 판은 그것을 `.json` 꼬리에 붙여 유효 JSON 이 아니었다
(자체 리뷰 C24).
