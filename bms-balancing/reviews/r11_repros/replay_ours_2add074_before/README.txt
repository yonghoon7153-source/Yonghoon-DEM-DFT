수정 전 재현 — clean 체크아웃(sparse worktree at 2add074cf0c3ebfaa02b22d2311dd4330f0879b0, dirty 0)에서 실행.
root rc=0 · data rc=1 (shape_wrapper 만 `wsl.exe` 부재로 환경상 실행 불가 — 그 축은 publish 의 shape_step 과
적응 probe 가 대신 재현한다) · publish rc=0 · evidence 8 case rc=0.
열여덟 건이 전부 재현됐다: 각 결과의 `promotion_eligible`·`*_accepted`·`*_promoted`·`false_identity`·
`nonzero_children_certified_closed`·`unrelated_assertion_certified_closed` 필드가 그 관측이다.
