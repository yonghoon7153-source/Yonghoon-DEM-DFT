수정 뒤 재생 — 코드 커밋 418595591846b8a0e9888486625d449c69c0b165 에서 만들었다.

왜 코드 커밋에서 만드나: 러너가 `--expected-head` 의 커밋을 sparse worktree 로 materialize 해서 돌고, 도구 자신
(`replay_codex_r*.py` · `reviews/evidence_gate.py`)의 bytes 도 그 커밋의 blob 과 같아야 `evidence_eligible: true` 가
된다. 그래서 코드 커밋을 먼저 만들고 그 커밋을 대상으로 증거를 생성한 뒤, 증거 파일만 다음 커밋에 얹는다.

    git diff 4185955 HEAD --name-only -- '*.py' '*.sh'      # → 0 개 (코드는 그대로다)

네 재생기 전부 evidence_eligible: true · instrument_sealed: true · package_digest_ok: true ·
expected_tree efa727fac821… · ran_in "격리 snapshot".

  replay_codex_r7.json    반례 소멸 5 · 전제 변경 1 (R7-03)
  replay_codex_r9.json    반례 소멸 12
  replay_codex_r10.json   반례 소멸 20 · 우리 코드 밖 1 (snapshot:argv) · 전제 변경 1 (u18:shape_duplicates)
  replay_codex_r11.json   반례 소멸 32 · 전제 변경 2 (publish:* · root:profile_grid) · 환경상 불가 1 (data:shape_wrapper)

"전제 변경" 은 전부 **fingerprint 를 봉인**해 두었다 — 그 case 에서 기대하는 문자열이 전부 맞을 때만 그렇게
적히고, 아무 예외나 닫힘으로 읽히지 않는다. 무엇이 대신 그 축을 보는지는 각 러너의 표와 `reviews/R6_LEDGER.md`
"Codex R11" 절에 적었다.

`dirty` 는 true 다 — 이 디렉터리(증거 파일)가 실행 중 untracked 로 있었기 때문이고, `dirty_paths` 에 그 한 줄만
있다. 실행 bytes 는 snapshot 에서 왔으므로 오염원이 아니다 (Codex R10 P2-5 의 계약).

그 밖:
  pytest_full.txt              202 passed in 157.98s
  matlab_smoke.txt             Octave 전 단계 통과 ("전부 통과")
  codex_r6_mutation_audit.txt  8/8 CAUGHT · MISSED 0
  mutation_adapted.txt         5/5 CAUGHT · MISSED 0 · baseline/복구 6/6 닫힘 (R6_OLD_OUT = bfc4623^ 의 out)
  replay_codex_r6_adapted.json "mode": "full" 6/6 닫힘
  check_u14_out_schema_only.txt rc 2 · promotion_eligible false
      새 스키마 누락 28 = sidecar `argv` 12 + sidecar `roster` 12 + profile `gamma_roster` 4
      기준/대상 입력 출처 열 누락 24
      내용 검사 실패 4 (degeneracy 의 옛 `inputs_sha` — R10 에서 digest 규칙이 바뀌었다; 숫자는 안 움직였다)

11차 패키지의 네 스크립트를 **그대로** 돌린 결과는 `replay_codex_r11.json` 안에 case 별로 들어 있다 (러너가
자식으로 그 스크립트를 부르고 stdout payload 를 그대로 담는다). 수정 **전** 재현은
`reviews/r11_repros/replay_ours_2add074_before/`.
