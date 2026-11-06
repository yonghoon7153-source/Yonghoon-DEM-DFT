# Own findings before reading PREATTACK_7.md (written 2026-11-04, from diff + code only)

H1 (PC7-02 class) found_attempts_problem AL07 exception = (result line rejected) AND (any file named attempt_<k>.rejected.json in that base).
    No check that r['folder'] == side name, no digest check, no content check. Under the PE02 threat model (ledger reset + re-append),
    attacker re-appends result line 1 as "rejected" instead of "그대로", deletes attempt.json, touches side file -> hidden attempt passes.
    -> probe via real path (ledger + lad_att + ver_led).

H2 (PC7-04 class) token/name binding only in recover_group (only reached for unconfirmed/missing end records).
    attempt_groups_problem / orphan_cause / stage_recover todo selection never compare end.json token/name with launch.json.
    A foreign *confirmed* end record (copy) -> group counted as confirmed exit, cause from foreign record, resume_ok from it.
    -> probe unit + recover_ledger path.

H3 (PC7-04) unknown `by` in old end record (not chain/recover) -> silently ignored (no `other`), new end written w/o chain_end.

H4 (PC7-01) start record base check only in recover_ledger; host field never compared (display only). Multi-clone ledgers:
    guard only works if all machines share one ledger repo (same path / synced before attempt_open).

H5 (RINT2-E01) byte_diff_view: Python equality (True == 1 == 1.0, -0.0 == 0) -> bool<->int value change reported as 'format';
    results_differ / public_keys_differ / grade_differ same semantics. value short-circuits other kinds (E18i file also lacks final
    newline; test asserts ['value'] only, despite docstring "여럿 가능"). RecursionError on deep nesting not caught (pre-existing r0 parse too).

H6 (BAN8) qualifier text now says "전달 길이 = 해석 시험 통과 (분산판 = 전송선 · 식 검증)" but test covers only: identical rails
    (R̄sh2 = 1), straight parallel axis-aligned fibres one cell apart, L_c exact multiple of L_par. Unequal rails / k = ceil not
    integer / tilted fibres not tested against Eq. 8. Check mutation strength (port placement, half-cell end, tolerance factor).
