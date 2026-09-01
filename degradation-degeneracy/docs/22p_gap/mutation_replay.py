#!/usr/bin/env python3
"""변이 재생 — 각 불변식을 되돌리면 **정확히 그 시험**이 빨개지는가.

★ 43차 리뷰 Q5 답변: 한 구조 변경이 여러 조건을 함께 닫았을 때, 조건마다
  시간순 RED 커밋을 요구하지는 않는다. 대신 **격리·결정적·재생 가능한**
  mutant artifact 가 있어야 한다. 44차 리뷰가 "prose-only 기록은 독립 replay
  까지 못 간다" 고 했으므로 그 artifact 를 저장소에 둔다.

  이 파일은 RUN_SCOPE 밖(`docs/`)이다 — code identity 를 움직이지 않는다.

사용::

    python3 docs/22p_gap/mutation_replay.py            # 전부
    python3 docs/22p_gap/mutation_replay.py --list     # 목록만
    python3 docs/22p_gap/mutation_replay.py -k warm    # 이름으로 고르기

각 항목은 (불변식 이름, 파일, 되돌릴 조각, 되돌린 값, 빨개져야 하는 -k) 다.
실행은 원본을 복원하고 끝난다 (실패해도 `finally` 로).
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
PRESERVE = ROOT / "tools" / "preserve.py"
RP = ROOT / "docs" / "22p_gap" / "row_projection.py"
TDL = ROOT / "tests" / "test_docs_lint.py"
GRID = ROOT / "src" / "grid.py"
FITTING = ROOT / "src" / "fitting.py"

#: ★ 46차 #9 조건 9 — 변이는 **작업 트리에 손대지 않는다.** 45차 runner 는
#:   실제 저장소 파일을 고쳤다가 `finally` 로 되돌렸다. 그러면 (a) 중단되면
#:   변이된 트리가 남고 (b) 그 사이 다른 프로세스가 변이된 코드를 보고
#:   (c) 복원이 text mode 를 지나 개행·인코딩이 접힐 수 있다. 이제 저장소를
#:   임시 sandbox 로 복사해 **그 안에서만** 변이하고, 원본은 읽기만 한다.
SANDBOX: pathlib.Path | None = None


def _sandboxed(path: pathlib.Path) -> pathlib.Path:
    """저장소 경로를 sandbox 안 같은 상대 위치로 옮긴다."""
    return path if SANDBOX is None else SANDBOX / path.relative_to(ROOT)


def _make_sandbox() -> pathlib.Path:
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="mutation_replay_"))
    dst = tmp / ROOT.name
    shutil.copytree(
        ROOT, dst, symlinks=True,
        ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache",
                                      ".mypy_cache", "*.pyc", ".ruff_cache"))
    return dst

#: 단일 지점 변이 — (이름, 파일, old, new, 빨개져야 하는 -k)
MUTANTS = [
    # ── 48차 (게이트 47차 반증 조건) ──────────────────────────────────────
    #   P0-2: producer 닫힘의 네 구멍. 각 자리를 47차 상태로 되돌린다.
    ("producer-crosses-into-scoring", RP,
     '_PRODUCER_MODULES = ("src.scoring",)',
     '_PRODUCER_MODULES = ()',
     "producer_digest_crosses_into_src_scoring"),
    ("producer-crossing-is-fail-closed", RP,
     "    alias_missing = sorted({v for v in alias.values() if v not in sdefs})",
     "    alias_missing = []",
     "breaking_the_crossing_into_src_scoring_is_fail_closed"),
    ("producer-cut-is-sealed", RP,
     '                             "_PRODUCER_CUT": list(_PRODUCER_CUT),\n'
     '                             "_PRODUCER_MODULES": list(_PRODUCER_MODULES)',
     '                             "_PRODUCER_MODULES": list(_PRODUCER_MODULES)',
     "widening_the_producer_cut_moves_the_digest"),
    ("producer-canon-drops-empty-fields", RP,
     "            if not isinstance(node, ast.Constant):\n"
     "                if v is None or (isinstance(v, list) and not v):\n"
     "                    continue\n",
     "",
     "producer_digest_is_the_same_on_every_python_here"),

    # ── 47차 (게이트 46차 반증 조건) ──────────────────────────────────────
    # ★ 48차 P0-7 — generation namespace 는 이제 **성분마다** 붙잡는다
    #   (`_open_child_dir`). 그래서 옛 자리(`_open_dir_nofollow`)를 되돌려도
    #   generation root 경로는 더 이상 그곳을 지나지 않아 아무 시험도 안 깨진다
    #   — 변이가 **코드가 옮겨가 죽은** 경우다. 성질이 실제로 사는 자리로
    #   옮긴다: 성분 열기에서 `O_NOFOLLOW` 를 뺀다.
    ("generation-root-nofollow", RP,
     "        return os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,\n"
     "                       dir_fd=dfd)",
     "        return os.open(name, os.O_RDONLY | os.O_DIRECTORY, dir_fd=dfd)",
     "generation_root_symlink_is_never_read_as_a_generation or "
     "symlinked_gen_ancestor_never_holds_a_generation"),
    ("producer-semantic-sealed", RP,
     '_PIN_SEALED = ("schema_version", "analysis_spec_sha256",\n'
     '               "producer_semantic_sha256")',
     '_PIN_SEALED = ("schema_version", "analysis_spec_sha256")',
     "producer_change_cannot_mix_two_producers or producer_semantic_identity_is_sealed"),
    ("producer-cut-is-declared", RP,
     '    cut_missing = [x for x in _PRODUCER_CUT if x not in defs]\n'
     "    if cut_missing:",
     "    cut_missing = []\n    if cut_missing:",
     "producer_semantic_digest_excludes_the_publication_path"),
    ("policy-binds-the-roster", RP,
     '        elif k == "cross_leg_comparison" and v == "not_applicable_single_leg" \\\n'
     "                and len(rec.get(\"legs\") or ()) != 1:",
     "        elif False:",
     "single_leg_policy_must_match_the_roster_cardinality"),
    ("pre-write-authority", RP,
     '    if _pre.get("status") != "active":',
     "    if False:",
     "frozen_cohort_publish_writes_nothing_before_it_refuses"),
    ("complete-current-supersedes-pending", RP,
     "    auth.pend_stale = auth.pend_raw is not None and auth.cur_raw is not None",
     "    auth.pend_stale = False",
     "complete_current_supersedes_a_leftover_pending"),
    ("repair-source-uses-the-snapshot", PRESERVE,
     "        for v in self._version_candidates(key, required=False):\n"
     "            if self._bytes_match(key, v, dg):\n                return v",
     "        for v in (self.provider.versions(key) or []):\n"
     "            if self._bytes_match(key, v, dg):\n                return v",
     "repair_lookups_go_through_the_validated_version_snapshot or "
     "no_version_enumeration_bypasses_the_helper"),
    ("claim-seals-the-run-spec", PRESERVE,
     '    if e["run_spec_digest"] != want:',
     "    if False:",
     "claim_seals_the_exact_run_spec"),
    ("claim-checks-the-whole-index", PRESERVE,
     "    assert_planned_index_consistent(ledger)          # 전체가 먼저",
     "    pass                                             # 전체가 먼저",
     "whole_index_must_be_consistent_before_any_leg_is_claimed"),
    ("plan-index-exact-equality", PRESERVE,
     "    phantom = sorted(l for l, e in idx.items()\n"
     '                     if e["status"] == "executed" and l not in set(executed))',
     "    phantom = []",
     "phantom_executed_plan_without_an_execution_record"),
    ("plan-parser-dir-hygiene", PRESERVE,
     "    if posixpath.isabs(raw) or posixpath.normpath(raw) != raw \\\n"
     '            or ".." in raw.split("/"):',
     "    if False:",
     "plan_parser_requires_a_canonical_relative_dir or "
     "plan_parser_refuses_a_cohort_dir_outside_the_repository"),
    ("namespace-check-rejects-symlinks", PRESERVE,
     "        if stat.S_ISLNK(st.st_mode):\n            return False                # alias 는",
     "        if False:\n            return False                # alias 는",
     "symlinked_path_is_not_inside_the_smoke_namespace or "
     "namespace_check_is_fail_closed_on_a_symlinked_component"),
    ("module-gate-before-side-effects", GRID,
     # ★ 48차 P0-5 — gate 호출이 조건 집합·다리 이름을 넘기고 claim 을 돌려주도록
     #   바뀌었다. 호출 지점을 통째로 지우는 것이 이 변이의 뜻이다.
     "    _claim = _assert_grid_authorized(cfg, out_dir, conditions=conditions,\n"
     "                                     dry_run=dry_run, leg=leg,\n"
     "                                     token_file=token_file)\n",
     "    _claim = None\n",
     "run_grid_calls_the_gate_before_its_first_side_effect"),
    # ── 46차 (게이트 45차 반증 조건) ──────────────────────────────────────
    ("caller-stage-safe-read", RP,
     "    fresh_bytes = _staging_entries(stage, out)\n"
     "    fresh = set(fresh_bytes)",
     "    fresh_bytes = {p.name: p.read_bytes()\n"
     "                   for p in stage.iterdir() if p.is_file()}\n"
     "    fresh = set(fresh_bytes)",
     "dangling_symlink_in_the_caller"),
    ("publisher-owns-the-merge-temp", RP,
     "            _write_owned(work / name, merged[name])",
     "            _write_owned(stage / name, merged[name])",
     "caller_stage_is_untouched"),
    ("reader-shares-the-validator", RP,
     # ★ 48차 — 검증 통로가 helper 하나로 모였고 call site 가 셋이다. 한 자리만
     #   되돌리면 나머지 둘이 성질을 지켜 시험이 초록이다 — 성질이 사는 곳은
     #   이제 helper 자신이므로 그 body 를 되돌린다.
     "    with _generation_dirfd(out, gid) as dfd:\n"
     "        return _entries_from_dirfd(dfd, \"generation\")",
     "    return {q.name: q.read_bytes()\n"
     "            for q in sorted((Path(out) / \"gen\" / gid).iterdir()) if q.is_file()}",
     "generation_reader_refuses_an_aliased"),
    ("idempotent-shares-the-validator", RP, None, None, None),
    ("generation-namespace-guard", RP,
     "        hit = forbidden.get(key)\n        if hit is not None:",
     "        hit = None\n        if hit is not None:",
     "current_generation_cannot_be_used_as_its_own_staging"),
    ("pointer-loss-is-terminal", RP,
     "        if lost:\n            raise SystemExit(",
     "        if False:\n            raise SystemExit(",
     "losing_the_pointer_of_a_cohort"),
    ("pin-is-publication-authority", RP,
     '_LEDGER_AUTHORITY = ("cohort_id", "dir", "status", "legs",\n'
     '                     "pin", "cross_leg_comparison")',
     '_LEDGER_AUTHORITY = ("cohort_id", "dir", "status", "legs",\n'
     '                     "cross_leg_comparison")',
     "producer_pin_is_part"),
    ("ledger-status-enum", RP,
     '        elif k == "status" and v not in _LEDGER_STATUS:',
     "        elif False:",
     "status_is_an_exact_enum"),
    ("ledger-dir-contained", RP,
     "    if posixpath.isabs(raw) or posixpath.normpath(raw) != raw \\\n"
     '            or ".." in raw.split("/"):',
     "    if False:",
     "dir_that_is_not_contained"),
    ("version-candidates-typed", PRESERVE,
     '        bad = [v for v in got if not _nonempty_str(v if isinstance(v, str) else "")]',
     "        bad = []",
     "every_enumerated_version_candidate or falsy_version_never_reaches_lock"),
    ("planned-status-is-not-standing", PRESERVE,
     '    if e["status"] not in allow:',
     "    if False:",
     "standing_authorization"),
    ("planned-binds-the-code-identity", PRESERVE,
     '    if e["authorized_source_digest"] != source_digest:',
     "    if False:",
     "plan_to_the_code_identity"),
    ("planned-binds-the-execution-record", PRESERVE,
     '        if e["authorized_source_digest"] != real:',
     "        if False:",
     "planned_index_is_bound_to_the_real"),
    ("warm-edges-are-declared", TDL,
     '    "test_warm_probe_records_the_protocol_axes": {"_warm_manifest"},',
     "",
     "warm_consumers_go_through_the_accessors"),
    # ── 45차 (게이트 44차 반증 조건) ──────────────────────────────────────
    ("authority-frozenset", RP,
     "    auth.roster = frozenset(cohort.get(\"legs\") or ())",
     "    auth.roster = set(cohort.get(\"legs\") or ())",
     "frozen_authority_holds_only_immutable"),
    ("sink-subset-of-roster", RP,
     "    undeclared = sorted(seen - auth.roster)\n    if undeclared:",
     "    undeclared = []\n    if undeclared:",
     "complete_undeclared_leg_never_reaches_pending"),
    ("staging-nlink-one", RP,
     "        if st.st_nlink != 1:\n            bad.append(f\"{name}: 다른 이름과 inode 를 공유한다 \"",
     "        if False:\n            bad.append(f\"{name}: 다른 이름과 inode 를 공유한다 \"",
     "staging_aliases_never_become_an_immutable_generation"),
    ("seal-exact-types", RP,
     "    if t is list:",
     "    if t in (list, tuple):",
     "an_omap_and_a_list_of_lists_do_not_share_a_seal"),
    ("seal-finite-floats", RP,
     "        if not math.isfinite(node):",
     "        if False:",
     "seal_domain_is_exact_not_isinstance"),
    ("pointer-binds-the-ledger", RP,
     "        if rec[\"ledger_seal\"] != live:",
     "        if False:",
     "expanding_a_roster_over_an_active_cohort_requires_a_new_cohort"),
    ("prelock-version-id-is-a-string", PRESERVE,
     "            if not _nonempty_str(vid if isinstance(vid, str) else \"\"):",
     "            if False:",
     "falsy_version_id"),
    ("trust-boundary-declared", RP,
     "_TRUST_BOUNDARY = \"\"\"cohort 출력 디렉터리",
     "_TRUST_BOUNDARY_DISABLED = \"\"\"cohort 출력 디렉터리",
     "publisher_declares_its_trust_boundary"),
    ("public-lifecycle-in-two-publisher-fixture", TDL,
     "res = rp.promote_cohort_generation(stage, out, leg,\n"
     "                                   roster=rp._ledger_roster(out))",
     "res = (rp._promote_cohort_locked(stage, __import__('contextlib')\n"
     "       .nullcontext(), leg) if False else\n"
     "       rp.promote_cohort_generation(stage, out, leg,\n"
     "                                    roster=rp._ledger_roster(out)))",
     None),
    ("warm-consumer-uses-accessor", TDL,
     "    missing = [l for l, _ in _WARM_CLAIMS if not _warm_has_summary(l)]",
     "    missing = [l for l, _ in _WARM_CLAIMS\n"
     "               if not (_REPO / 'docs' / '22p_gap' / 'warm_probe'\n"
     "                       / f'{l}.summary.yaml').is_file()]",
     "warm_consumers_go_through_the_accessors"),
    # ── 44차 (게이트 43차 반증 조건) ──────────────────────────────────────
    ("sink-validates-itself", RP,
     "    assert_cohort_complete(\n"
     "        files, gid, expect_legs=auth.roster if seen == auth.roster else None)",
     "    pass",
     "sink_refuses_an_incomplete"),
    ("authority-frozen", RP,
     '        if getattr(self, "_sealed", False):',
     "        if False:",
     "frozen_authority_cannot_be_edited"),
    ("seal-typed-input", RP,
     "    _assert_sealable(cohort)\n    rec = {}",
     "    rec = {}",
     "types_differ_is_not_folded"),
    ("recheck-before-rename", RP,
     "    if auth is not None:\n        _Authority.assert_pointers_unmoved(auth)\n"
     "    os.replace(tmp, out / name)",
     "    os.replace(tmp, out / name)",
     "rechecked_immediately_before_the_rename"),
    ("proof-until-equals-lease", PRESERVE,
     '            if proof.until != lease["retain_until_utc"]:',
     "            if False:",
     None),          # 계약 확인 — 아래 주석 참조
    # ── 43차 (게이트 42차 반증 조건) ──────────────────────────────────────
    ("proof-handoff-to-verify", PRESERVE,
     "                lease_version=proof.lease_version,\n"
     "                lease_content_version=proof.content_version)",
     "                lease_version=self.recover_lease_version(leg_id, extra[0]),\n"
     "                lease_content_version=self.recover_content_version(extra[0]))",
     "repaired_proof_is_handed or pre_journal_finalize or journal_seals_the_content"),
    ("prelock-digest-check", PRESERVE,
     "            if hashlib.sha256(data).hexdigest() != dg:\n"
     "                raise PreserveError(",
     "            if False:\n                raise PreserveError(",
     "wrong_bytes_are_never_locked"),
    ("prelock-readback-check", PRESERVE,
     "            if not self._bytes_match(key, vid, dg):\n"
     "                raise PreserveError(",
     "            if False:\n                raise PreserveError(",
     "returns_the_wrong_version"),
    ("authority-registry", RP,
     "    if type(auth) is not _Authority or id(auth) not in _Authority._ACTIVE:",
     "    if False:",
     "raw_publisher_takes_no"),
    ("both-pointers-checked", RP,
     "        if live_cur != self.cur_raw or live_pend != self.pend_raw:",
     "        if live_pend != self.pend_raw:",
     "pointer_moved_by_another"),
    ("guard-before-commit", RP,
     "    _commit_guard()\n    _publish_pointer(out, rec, auth=auth)",
     "    _publish_pointer(out, rec, auth=auth)",
     "pathname_after_the_check or same_roster_ledger_change"),
    ("inner-unbound-sentinel", RP,
     "        _PublishLock._assert_plain_sentinel(self.fd)",
     "        self._assert_plain_sentinel(self.fd)",
     "blank_its_sentinel_check"),
    ("inner-unbound-kernel", RP,
     "        _PublishLock._reassert_kernel_lock(self)",
     "        self._reassert_kernel_lock()",
     "blank_its_own_inner_check"),
    ("pending-base-generation", RP,
     '        if pend["base_generation"] != auth.cur_gid:\n            raise SystemExit(',
     "        if False:\n            raise SystemExit(",
     "stale_bootstrap_pending"),
    ("pending-closed-schema", RP,
     "    if set(rec) != want_keys:",
     "    if False:",
     "stale_bootstrap_pending"),
    ("warm-consumer-wiring", TDL,
     '    assert {"_warm_summary", "_warm_manifest", "_warm_has_summary"} <= calls, (',
     "    assert True or (",
     None),          # 아래 주석 참조
    # ── 49차 (게이트 48차 반증 조건) ──────────────────────────────────────
    ("precheck-tells-new-from-resume", PRESERVE,
     "    path = _claim_path(leg_id, claims_root)\n"
     "    if path.is_file():\n"
     "        if token_file is None:",
     "    path = _claim_path(leg_id, claims_root)\n"
     "    if False:\n"
     "        if token_file is None:",
     "precheck_tells_a_new_run_from_an_owned_resume"),
    ("claim-stores-a-verifier-not-the-token", PRESERVE,
     '           "attempt_id": attempt_id, "attempt_verifier": _token_verifier(token),',
     '           "attempt_id": attempt_id, "attempt_verifier": token,',
     "claim_file_never_stores_the_resume_credential"),
    ("resume-compares-the-verifier", PRESERVE,
     "        if not secrets.compare_digest(_token_verifier(token),\n"
     '                                      str(rec["attempt_verifier"])):',
     "        if False:",
     "phase_cannot_be_recorded_without_the_owner_token or "
     "crash_after_grid_resumes_and_finalizes"),
    ("diagnostic-hides-the-credential", PRESERVE,
     "        if self._token is None:\n"
     "            raise PreserveError(\n"
     '                "plan", f"{self.leg_id!r} 의 claim 을 소유 증명 없이 열었다 — "\n'
     '                        "진단용 읽기에는 재개 credential 이 없다")',
     "        if False:\n"
     "            raise PreserveError(\n"
     '                "plan", f"{self.leg_id!r} 의 claim 을 소유 증명 없이 열었다 — "\n'
     '                        "진단용 읽기에는 재개 credential 이 없다")',
     "the_diagnostic_reader_never_hands_out_the_credential"),
    ("finalize-requires-the-credential", PRESERVE,
     "    if (token is None) == (token_file is None):\n"
     "        raise TypeError(\n"
     '            "finalize_leg() 는 `token` 또는 `token_file` 중 정확히 하나를 "',
     "    if False:\n"
     "        raise TypeError(\n"
     '            "finalize_leg() 는 `token` 또는 `token_file` 중 정확히 하나를 "',
     "finalize_requires_the_owner_credential"),
    ("finalize-holds-the-claim-lock", PRESERVE,
     "    with _ledger_lock(_claim_path(leg_id, claims_root)):",
     "    if True:",
     "canonical_lock_order_is_declared_and_finalize_holds_the_claim"),
    ("finalize-rechecks-in-the-ledger-lock", PRESERVE,
     "            assert_planned_index_consistent(ledger)\n"
     "            live = assert_planned_leg(leg_id, claim.source_digest,\n"
     "                                      ledger=ledger,\n"
     '                                      allow=("planned", "running"))',
     '            live = {"cohort_id": claim.cohort_id,\n'
     '                    "run_spec_digest": claim.run_spec_digest}',
     "finalize_rechecks_the_whole_authority_inside_the_ledger_lock"),
    ("crash-recovery-is-idempotent", PRESERVE,
     "    done = _already_finalized(leg_id, token, ledger=ledger,\n"
     "                              claims_root=claims_root)",
     "    done = None",
     "finalize_is_idempotent_after_a_crash_before_cleanup"),
    ("crash-recovery-needs-the-credential", PRESERVE,
     '    if not secrets.compare_digest(want, str(rec["attempt_verifier"])):\n'
     "        raise PreserveError(\n"
     "            \"plan\",\n"
     '            f"{leg_id!r} 은 이미 닫혔고, 그 실행의 소유 증명이 아니다 — "',
     "    if False:\n"
     "        raise PreserveError(\n"
     "            \"plan\",\n"
     '            f"{leg_id!r} 은 이미 닫혔고, 그 실행의 소유 증명이 아니다 — "',
     "the_crash_recovery_needs_the_owner_credential"),
    ("preservation-status-inside-the-contract", PRESERVE,
     'PRESERVATION_STATUS = ("full_bundle", "recorded_projection",\n'
     '                       "preservation_pending", "missing")',
     'PRESERVATION_STATUS = ("full_bundle", "recorded_projection",\n'
     '                       "no_bundle", "missing")',
     "the_runtime_preservation_enum_is_inside_the_contract"),
    ("finalize-writes-the-whole-tuple", PRESERVE,
     '                 "validation_status": PENDING_VALIDATION_STATUS,\n'
     '                 "inference_role": PENDING_INFERENCE_ROLE,',
     "",
     "finalize_writes_a_complete_contract_status_tuple"),
    ("fit-axis-is-the-real-policy", PRESERVE,
     'LEG_SPEC_FIT_KEYS = ("config_digest", "objective_order", "objectives_digest",\n'
     '                     "reference",\n'
     '                     "halfcell_recipe", "halfcell_cache_sha256",\n'
     '                     "base_config_digest", "bounds_preset", "bounds_digest",\n'
     '                     "optimizer", "use_noisy", "row_selection",\n'
     '                     "in", "in_digest", "out")',
     'LEG_SPEC_FIT_KEYS = ("config_digest", "objective_order", "out")',
     "fit_axis_seals_every_intent_that_changes_the_answer"),
    ("phase-input-binding", PRESERVE,
     "        if not secrets.compare_digest(str(sealed), str(got)):",
     "        if False:",
     "fit_refuses_curves_that_its_grid_phase_did_not_produce"),
    ("phase-input-binding-needs-a-receipt", PRESERVE,
     "    rec = claim.phase_receipt(\"grid\")\n"
     "    if rec is None:",
     "    rec = claim.phase_receipt(\"grid\")\n"
     "    if False:",
     "fit_refuses_when_its_grid_phase_is_missing"),
    ("release-returns-the-plan", PRESERVE,
     "    claim = resume_claim(leg_id, claims_root, token=token, ledger=ledger)\n"
     "    _abandon_claim(claim, ledger=ledger)",
     "    claim = resume_claim(leg_id, claims_root, token=token, ledger=ledger)",
     "released_run_returns_the_plan_to_planned"),
    ("dry-run-releases-the-claim", GRID,
     "        if _claim is not None:\n"
     "            from tools.preserve import release_leg_run",
     "        if False:\n"
     "            from tools.preserve import release_leg_run",
     "dry_run_does_not_strand_the_plan_in_running"),
    ("roster-is-a-set", RP,
     "            dup = sorted({x for x in v if v.count(x) > 1})\n"
     "            if dup:",
     "            dup = []\n            if dup:",
     "ledger_roster_is_a_set_not_a_multiset"),
    ("thaw-transition-is-unrepresentable", RP,
     "    if (frm, to) not in _LIFECYCLE_MOVES:",
     "    if False:",
     "frozen_cohort_cannot_be_thawed_and_published"),
    ("lifecycle-chain-is-verified", RP,
     '        if rec["prev"] != prev:',
     "        if False:",
     "the_lifecycle_journal_is_a_hash_chain"),
    ("lifecycle-head-anchors-the-tip", RP,
     "    if head != prev:",
     "    if False:",
     "the_lifecycle_journal_is_a_hash_chain"),
    ("closure-follows-module-aliases", RP,
     "            if kind == \"rp\" and isinstance(sub_node, ast.Attribute) \\\n"
     "                    and isinstance(sub_node.value, ast.Name) \\\n"
     "                    and sub_node.value.id in mods:",
     "            if False:",
     "closure_follows_a_module_alias_attribute"),
    ("closure-unresolved-attr-is-fail-closed", RP,
     "                if attr not in sdefs:\n"
     "                    raise SystemExit(",
     "                if False:\n"
     "                    raise SystemExit(",
     "unresolved_producer_module_reference_is_fail_closed"),
    ("closure-refuses-dynamic-resolution", RP,
     "        _assert_no_dynamic_resolution(node, key, mods)",
     "        pass",
     "dynamic_name_resolution_inside_the_closure_is_fail_closed"),
    ("interpreter-set-is-pinned", RP,
     "    if sys.version_info[:2] not in SUPPORTED_PYTHON:",
     "    if False:",
     None),          # 아래 주석 참조
    # ── 50차 (게이트 49차 반증 조건) ──────────────────────────────────────
    ("phase-write-checks-the-credential", PRESERVE,
     "            if not secrets.compare_digest(_token_verifier(self._token),\n"
     '                                          str(rec["attempt_verifier"])):',
     "            if False:",
     "forged_claim_object_cannot_write_a_phase"),
    ("phase-write-refuses-a-closed-claim", PRESERVE,
     "            if not self.path.is_file():\n"
     "                raise PreserveError(",
     "            if False:\n"
     "                raise PreserveError(",
     "closed_run_cannot_be_resurrected_by_a_late_phase or "
     "released_run_cannot_be_resurrected_by_a_late_phase"),
    ("token-is-written-before-the-claim", PRESERVE,
     "        token = _new_token()\n"
     "        write_token_file(token_file, token)\n"
     "        try:\n"
     "            return claim_planned_leg(leg_id, run_spec, source_digest,\n"
     "                                     ledger=ledger, claims_root=claims_root,\n"
     "                                     token=token)",
     "        token = _new_token()\n"
     "        try:\n"
     "            claim = claim_planned_leg(leg_id, run_spec, source_digest,\n"
     "                                      ledger=ledger, claims_root=claims_root,\n"
     "                                      token=token)\n"
     "            write_token_file(token_file, token)\n"
     "            return claim",
     "crash_between_the_claim_and_the_token_leaves_nothing_stranded"),
    ("fit-axis-seals-the-input-content", PRESERVE,
     '                     "halfcell_recipe", "halfcell_cache_sha256",\n'
     '                     "base_config_digest", "bounds_preset", "bounds_digest",',
     '                     "halfcell_recipe", "bounds_preset", "bounds_digest",',
     "fit_axis_seals_the_input_content_axes"),
    ("row-selection-seals-its-content", PRESERVE,
     'LEG_SPEC_SELECTION_KEYS = ("mode", "limit", "subset_sha256")',
     'LEG_SPEC_SELECTION_KEYS = ("mode", "limit")',
     "fit_axis_seals_the_row_selection_content"),
    ("phase-input-binding-covers-the-package", PRESERVE,
     'PHASE_INPUT_KEYS = ("curves_sha256", "curves_manifest_sha256",\n'
     '                    "curves_manifest_start_sha256")',
     'PHASE_INPUT_KEYS = ("curves_sha256",)',
     "grid_receipt_binds_every_curve_input_not_just_the_parquet"),
    ("missing-journal-with-a-live-anchor", RP,
     "        if _lifecycle_head_path().is_file():\n"
     "            raise SystemExit(",
     "        if False:\n"
     "            raise SystemExit(",
     "deleting_the_journal_does_not_erase_the_freeze"),
    ("module-defs-see-tuple-targets", RP,
     "                for t in node.targets:\n"
     "                    for name in _target_names(t):\n"
     "                        defs[name] = top or node",
     "                for t in node.targets:\n"
     "                    if isinstance(t, ast.Name):\n"
     "                        defs[t.id] = top or node",
     "producer_closure_sees_tuple_targets or "
     "producer_closure_follows_a_tuple_defined_constant"),
    # ★ 51차 P0-I — 복합문 안으로 들어가지 않으면 `for X in ...` 이 묶은
    #   계산 상수가 identity 밖이다 (리뷰어 반례).
    ("module-defs-enter-compound-statements", RP,
     "            elif kind in _MODULE_COMPOUND:",
     "            elif kind in _MODULE_COMPOUND:\n"
     "                continue\n"
     "            elif False:",
     "producer_closure_sees_every_module_binding_form"),
    # ★ 51차 P0-I — 모르는 문을 조용히 지나치면 열거가 곧 구멍이다.
    ("module-defs-fail-closed-on-unknown", RP,
     "            else:\n"
     "                raise SystemExit(\n"
     "                    f\"✗ producer 소스의 module scope 에 모델링하지 않은 binding \"",
     "            else:\n"
     "                continue\n"
     "            if False:\n"
     "                raise SystemExit(\n"
     "                    f\"✗ producer 소스의 module scope 에 모델링하지 않은 binding \"",
     "unmodelled_module_binding_form_is_fail_closed"),
    # ★ 51차 P0-I — docstring 을 버리면 alias 로 읽어 identity 를 우회한다.
    ("canon-keeps-docstrings", RP,
     "def _keep_docstrings(tree):",
     "def _keep_docstrings(tree):\n"
     "    import ast\n"
     "    for node in ast.walk(tree):\n"
     "        body = getattr(node, \"body\", None)\n"
     "        if not isinstance(body, list) or not body:\n"
     "            continue\n"
     "        if not isinstance(node, (ast.Module, ast.FunctionDef,\n"
     "                                 ast.AsyncFunctionDef, ast.ClassDef)):\n"
     "            continue\n"
     "        first = body[0]\n"
     "        if isinstance(first, ast.Expr) \\\n"
     "                and isinstance(first.value, ast.Constant) \\\n"
     "                and isinstance(first.value.value, str):\n"
     "            node.body = body[1:] or [ast.Pass()]\n"
     "    return tree\n"
     "def _unused_keep(tree):",
     "docstring_the_computation_reads_is_inside_the_identity"),
    # ─────────────────────────────────────────────────────────────────────
    # 51차 방어
    # ─────────────────────────────────────────────────────────────────────
    # ★ P0-L1 — 발급이 살아 있는 claim 을 보기 **전에** token 을 덮으면, 두
    #   번째 정상 호출이 owner 의 소유 증명을 파괴한다 (리뷰어 실측).
    ("open-checks-the-live-claim-first", PRESERVE,
     "        if cp.is_file():\n"
     "            raise PreserveError(\n"
     "                \"plan\",\n"
     "                f\"{leg_id!r} 은 이미 실행 중이다 (claim: {cp}) — 두 번째 실행을 \"",
     "        if False:\n"
     "            raise PreserveError(\n"
     "                \"plan\",\n"
     "                f\"{leg_id!r} 은 이미 실행 중이다 (claim: {cp}) — 두 번째 실행을 \"",
     "second_open_never_touches_the_live_owners_token"),
    # ★ P0-L1/P1-P — 전달 통로가 authority 경로를 점유할 수 있으면 claim reader
    #   전체가 malformed JSON 을 만난다.
    ("token-path-is-disjoint-from-authority", PRESERVE,
     "    _assert_token_path_disjoint(token_file, claims_root, ledger)",
     "    pass",
     "token_path_cannot_alias_the_claim_authority"),
    # ★ P0-L2 — 삭제는 상태 전이다. 경로만 보고 지우면 남의 generation 을 지운다.
    ("token-unlink-is-generation-scoped", PRESERVE,
     "    if not secrets.compare_digest(cur, str(token)):\n"
     "        return False",
     "    if False:\n"
     "        return False",
     "late_release_cleanup_cannot_delete_the_next_attempts_token"),
    # ★ P0-L2 — mutator 가 쓰기 지점에서 live attempt 를 재확인하지 않으면
    #   stale handle 과 위조 handle 이 남의 실행을 취소한다.
    ("abandon-rechecks-the-live-attempt", PRESERVE,
     "        _assert_live_attempt(json.loads(claim.path.read_text(encoding=\"utf-8\")),\n"
     "                             claim, \"발급 되돌림\")",
     "        pass",
     "stale_claim_handle_cannot_cancel_the_next_attempt or "
     "readonly_claim_cannot_abandon_the_live_owner"),
    # ★ P0-L3 — claim 을 먼저 지우면 crash 가 회수 불가능한 running orphan 을
    #   남긴다. 원장이 먼저여야 중간 상태가 재시도 가능하다.
    ("release-moves-the-ledger-before-the-claim", PRESERVE,
     "        # 원장이 `planned` 로 굳은 **뒤에만** claim 을 놓는다.\n"
     "        claim.path.unlink(missing_ok=True)",
     "        pass",
     "crash_inside_release_leaves_a_recoverable_state"),
    # ★ P0-L3 — `os.replace` 뒤의 오류를 미커밋으로 보면 claim/token 을 지운다.
    ("rollback-rereads-the-committed-state", PRESERVE,
     "        if _plan_status(leg_id, ledger=ledger) != \"running\":\n"
     "            path.unlink(missing_ok=True)",
     "        path.unlink(missing_ok=True)",
     "durability_error_after_the_ledger_commit_keeps_the_claim"),
    # ★ P0-A1 — 목적함수 payload 가 승인 밖이면 같은 이름으로 다른 J 를 낸다.
    ("fit-axis-seals-the-objective-payload", FITTING,
     '        "objectives_digest": _dg({str(k): objectives[k]\n'
     '                                  for k in sorted(objectives)}),',
     '        "objectives_digest": "0" * 16,',
     "objective_payload_is_inside_the_approval_digest"),
    # ★ P0-A2 — leaf 만 해시하면 `extends` 부모로 행을 옮길 수 있다.
    ("fit-axis-seals-the-config-closure", FITTING,
     '        "base_config_digest": _config_closure_digest(\n'
     '            base_config or "configs/base.yaml", repo_root=bytes_root),',
     '        "base_config_digest": _file_digest16(\n'
     '            base_config or "configs/base.yaml"),',
     "base_config_parent_is_inside_the_approval_digest"),
    # ★ P0-A3 — 검사한 pathname 을 나중에 다시 열면 그 사이가 무방비다.
    ("fit-stages-its-inputs-before-the-gate", FITTING,
     "    _staged = _stage_fit_inputs(in_dir, base_config, reference,\n"
     "                                halfcell_method, halfcell_kw)",
     "    _staged = {\"root\": None, \"in_dir\": Path(in_dir),\n"
     "               \"base_config\": base_config,\n"
     "               \"origin_in_dir\": str(in_dir),\n"
     "               \"origin_base_config\": str(base_config)}",
     "run_fit_hands_the_body_the_staged_copies_not_the_originals"),
    # ★ P1-E1 — 외부 입력 분기가 곡선 하나만 보면 manifest 를 갈아 끼울 수 있다.
    ("external-binding-covers-the-package", FITTING,
     "    got = fit_input_package_digest(got_map)",
     '    got = got_map["curves_sha256"]',
     "external_input_binding_covers_the_whole_package"),
    # ★ P0-A4 — 완방상태 캐시가 승인 밖이면 격자 truth 기준점이 조용히 움직인다.
    ("grid-axis-seals-the-discharged-cache", GRID,
     '        "discharged_cache_sha256": (\n'
     "            _h.sha256(cache.read_bytes()).hexdigest()\n"
     "            if use_cache and cache.is_file() else None),",
     '        "discharged_cache_sha256": None,',
     "grid_axis_binds_the_discharged_state_cache"),
    # ★ P0-F — 얼린 것은 이름이 아니라 그 디렉터리다.
    ("freeze-seals-the-output-directory", RP,
     "    for d, cid in frozen_dirs_from_journal().items():\n"
     "        out.setdefault(cid, (REPO / d).resolve())",
     "    pass",
     "frozen_directory_cannot_be_republished_under_a_new_cohort_id"),
    # ★ P1-O — fail-closed 는 정지가 아니다. 남은 전이를 완주해야 한다.
    ("freeze-completes-a-half-written-transition", RP,
     "    if recorded == \"frozen\":\n"
     "        if row.get(\"status\") == \"active\":",
     "    if recorded == \"frozen\":\n"
     "        if False:",
     "freeze_is_retryable_after_a_crash_between_its_two_writes"),
        ("canon-absorbs-the-pep701-empty-piece", RP,
     "            if isinstance(node, ast.JoinedStr) and f == \"values\" \\\n"
     "                    and isinstance(v, list):\n"
     "                v = [x for x in v\n"
     "                     if not (isinstance(x, ast.Constant) and x.value == \"\")]",
     "            pass",
     "canonical_form_agrees_on_every_supported_interpreter"),
]

#: 여러 지점을 **함께** 되돌려야 관측되는 변이 (심층 방어라 하나만 지우면
#: 다른 하나가 가린다). 41·42·43차에 실측했다.
MULTI = [
    # ★ 48차 — 이것도 방벽이 둘이 됐다. 42차 버그(재확인이 `set(legs)` 만 본다)를
    #   복원해도, 48차가 임계 구역에 넣은 **살아 있는 status 재조회**가 freeze 를
    #   먼저 잡아 시험이 초록이다. 즉 내가 이번에 더한 검사가 이 변이를 가린다.
    #   둘 다 남기고(하나는 record 전체의 digest, 하나는 현재 쓰기 권한) 변이는
    #   47차 상태를 복원한다.
    ("ledger-seal-record", RP, [
        ("        if auth.ledger_seal_now() != auth.seal:",
         "        if set(_ledger_cohort(out).get('legs') or ()) != auth.roster:"),
        ("        if _live.get(\"status\") != \"active\":",
         "        if False:"),
     ], "same_roster_ledger_change"),
    # ★ 48차 — `O_EXCL` **혼자로는** 더 이상 관측되지 않는다. 48차 P0-6 이
    #   claim 뒤에 `planned → running` 전이를 더했고, 그 전이는 원장 lock 안에서
    #   일어나므로 두 번째 claim 을 거기서 막는다. 즉 배타성을 지키는 것이 둘이
    #   됐다 — 하나만 지우면 다른 하나가 시험을 초록으로 유지한다.
    #
    #   중복이라서 하나를 지우는 것이 아니다: `O_EXCL` 은 **원자적 primitive**
    #   이고 상태 전이는 lock 에 기대는 두 번째 방벽이다. 둘 다 남기되, 변이는
    #   47차 상태(둘 다 없음)를 복원해 그 쌍이 실제로 일하는지 본다.
    ("claim-is-atomic", PRESERVE, [
        ("        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)",
         "        fd = os.open(path, os.O_CREAT | os.O_WRONLY, 0o644)"),
        ("        row[\"status\"] = \"running\"",
         "        row[\"status\"] = \"planned\""),
     ], "exactly_one_attempt_enters_compute"),
    # ★ 48차 P0-2 — decorator 축은 **정규형이 node 를 보는가**에 달렸다.
    #   47차처럼 source segment 로 되돌리면 `FunctionDef.lineno` 가 `def`
    #   줄이라 `decorator_list` 가 통째로 빠진다.
    # ★ 51차 — 50차까지 이것은 단일 변이였다. P0-F 가 journal 의 목적지 봉인을
    #   더하면서 같은 게시를 막는 자리가 둘이 됐다 (`assert_not_thawed()` 의 ID
    #   조회 · `_frozen_cohort_dirs()` 의 journal 합집합). 하나만 지우면 다른
    #   쪽이 여전히 거부하므로 단일 변이는 더 이상 안 문다 — 심층 방어의 정상
    #   신호다. 함께 되돌려야 관측된다.
    ("thaw-is-refused-before-the-first-write", RP, [
        ('    assert_not_thawed(_pre["cohort_id"])', "    pass"),
        ("    for d, cid in frozen_dirs_from_journal().items():\n"
         "        out.setdefault(cid, (REPO / d).resolve())",
         "    pass"),
     ], "publisher_refuses_a_thawed_cohort_before_the_first_write"),
    ("producer-normalizes-the-node", RP, [
        ("def _ast_normal_node(node) -> str:",
         "def _ast_normal_node(node, _src=None) -> str:"),
        ("    return _ast_canon(_keep_docstrings(copy.deepcopy(node)))",
         "    import ast\n"
         "    seg = ast.unparse(node)\n"
         "    body = ast.parse(seg).body[0]\n"
         "    body.decorator_list = []\n"
         "    return _ast_canon(_keep_docstrings(body))"),
     ], "producer_digest_sees_decorators"),
    # ★ 47차 — `dir_fd` 는 두 자리에 있다(`os.stat` · `os.open`). 하나만
    #   되돌리면 다른 철자가 남아 구조 검사가 통과한다 — 실측했다.
    ("children-read-through-dirfd", RP, [
        ("        st = os.stat(name, dir_fd=dfd, follow_symlinks=False)",
         "        st = os.stat(name, follow_symlinks=False)"),
        ("        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=dfd)",
         "        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW)"),
     ], "holds_a_directory_fd_for_its_children"),
    # ★ 47차 — 46차의 두 mutant 는 **옛 exploit 을 복원하지 않았다.**
    #   `generation-owns-its-bytes` 는 이미 만들어진 tmp 안으로 stage 를
    #   move 해서 중첩 디렉터리를 만들었고, 그 "extra directory" 오류가
    #   성공 증인으로 승인됐다. `staging-regular-only` 는 predicate 만 지워도
    #   `O_NOFOLLOW` 가 ELOOP 를 냈고 그 오류가 증인이 됐다. 둘 다 44차 이전
    #   동작을 그대로 되살리는 multi-site 로 고친다.
    # ★ 48차 — 신고 항목도 **scenario 로 등록**한다. 47차에는 `DECLARED_MASKED`
    #   에 설명만 있고 registry 에 이름이 없어서, 이름으로 고르면 0건을 고르고
    #   rc 0 이었다 (신고가 아니라 침묵이었다). `-k None` 은 "실행하지 않고
    #   신고한다" 는 뜻이고, registry 에 있으므로 목록·집계·선택에 나타난다.
    ("generation-owns-its-bytes", RP, [
        ("        for name in sorted(entries):\n"
         "            _write_owned(tmp / name, entries[name])",
         "        shutil.move(str(stage), str(tmp))"),
     ], None),
    ("staging-regular-only", RP, [
        ("        if not stat.S_ISREG(st.st_mode):        # symlink·FIFO·directory",
         "        if False:"),
        ("        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=dfd)",
         "        fd = os.open(name, os.O_RDONLY, dir_fd=dfd)"),
     ], "staging_aliases_never_become_an_immutable_generation"),
    ("flock-two-publisher", RP, [
        ("            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)\n"
         "        except OSError:\n            os.close(fd)\n            raise SystemExit(",
         "            pass\n"
         "        except OSError:\n            os.close(fd)\n            raise SystemExit("),
        ("            fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)\n"
         "        except OSError as e:",
         "            pass\n        except OSError as e:"),
     ], "two_independent_publishers"),
]

#: **관측되지 않는다고 신고하는** 항목. 왜 안 보이는지와 그래도 왜 남기는지를
#: 여기 적는다 — "masked but retained" 를 조용히 두지 않는다.
DECLARED_MASKED = {
    "idempotent-shares-the-validator":
        "48차 P0-7 이 generation 읽기를 helper 하나(`_generation_entries_by_id`)로 "
        "모았다. 그래서 idempotent 분기에 **고유한** 검증 자리가 더 이상 없고, "
        "그 성질은 `reader-shares-the-validator` 가 helper body 에서 이미 "
        "관측한다. 호출 지점만 되돌려도 시험이 초록인 것은 시험이 약해서가 "
        "아니라 **자리가 하나로 합쳐졌기** 때문이다. 없는 자리를 만들어 내는 "
        "대신 신고한다 — 회귀"
        "(`..._idempotent_branch_refuses_an_aliased_generation_file`)는 남긴다.",
    "generation-owns-its-bytes":
        "옛 exploit(스테이징 디렉터리를 통째로 rename)을 **복원할 수 없다**. "
        "46차에 caller staging 이 sink 에 도달하지 않게 바뀌었고(병합은 "
        "메모리, 자재화는 publisher 소유 temp), 그래서 sink 가 옮길 수 있는 "
        "것은 이미 `_write_owned` 로 만든 owned 파일뿐이다. 47차에 2-site 로 "
        "충실히 되살리려 했으나 결과가 여전히 owned inode 라 관측되지 않았다 "
        "— 이것은 시험이 약한 것이 아니라 그 상태가 **표현 불가능**해진 "
        "것이다. 회귀(`..._published_generation_owns_its_bytes`)는 남긴다.",
    "public-lifecycle-in-two-publisher-fixture":
        "이 mutant 는 fixture 를 내부 helper 직호출로 되돌리는 것인데, 그러면 "
        "fixture 가 문법적으로 다른 코드가 되어 '같은 시험을 다른 코드로 "
        "돌린' 것이 된다. 대신 `..._two_independent_publishers_lose_no_leg` 가 "
        "두 child 가 **public entry 를 지났다는 marker** 를 남기는지 실행 중에 "
        "확인하도록 시험을 보강했다 (45차).",
    "proof-until-equals-lease":
        "horizon 의 정본은 lease record 이고 verifier 가 exact ID 로 다시 "
        "확인한다. 이 assert 는 필드가 이름만 갖지 않게 하는 계약이며, "
        "현재 production 경로에서 둘이 갈라지는 반례가 없다.",
    "interpreter-set-is-pinned":
        "이 변이는 **지금 도는 인터프리터에서 관측할 수 없다.** 검사를 지우면 "
        "지원 집합 밖 버전에서 identity 를 계산하게 되는데, 이 기계에는 그 "
        "버전이 없다 — 관측하려면 지원 집합 밖 인터프리터를 하나 설치해 같은 "
        "시험을 거기서 돌려야 한다. 대신 회귀"
        "(`..._supported_interpreter_set_is_pinned_with_golden_vectors`)가 "
        "(a) 지금 인터프리터가 선언 집합 안이고 (b) 대표 구문 넷의 정규형이 "
        "golden 과 같음을 매번 확인한다. 즉 '정규형이 버전에 안 묶인다' 는 "
        "주장이 깨지면 golden 이 먼저 빨개진다.",
    "warm-consumer-wiring":
        "positive wiring 회귀는 배선이 **끊길 때** 빨개진다. assert 를 지우는 "
        "변이는 그 시험 자신만 무력화하므로 다른 시험이 물지 않는다 — "
        "이것은 회귀의 성질이지 결함이 아니다.",
}


def _nodes(kexpr: str) -> list[str]:
    """`-k` 가 고르는 **정확한 node ID 목록** (실행하지 않고 수집만).

    ★ 46차 — rc 를 **정확히** 본다. pytest 의 수집 성공은 rc 0 이고, rc 5 는
      "아무것도 안 골랐다" 다. 45차는 `rc != 0` 만 봤으므로 5 와 2(중단)·
      3(내부 오류)을 구별하지 못했다.
    """
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q", "-k", kexpr,
         "--collect-only", "-p", "no:randomly", "--no-header"],
        cwd=_sandboxed(ROOT), capture_output=True, text=True, timeout=1800)
    if r.returncode != 0:
        raise _ReplayError(f"수집 rc 가 0 이 아니다 ({r.returncode}): "
                           f"{r.stdout[-400:]}")
    return sorted(l.strip() for l in r.stdout.splitlines()
                  if "::" in l and l.strip().startswith("tests/"))


def _run(kexpr: str) -> dict:
    """`-k` 를 실행하고 **node 별 결과**를 JSON report 로 돌려준다.

    ★ 45차 — 44차 runner 는 baseline 없이 `rc != 0` 이면 전부 "물었다" 로
      셌다. 그러면 다음이 모두 성공으로 보인다: 아무 시험도 안 골라진 rc=5,
      syntax/collection/import 오류, 변이 **전부터** 있던 실패, 기대한 것이
      아닌 다른 시험의 실패. 그래서 node 단위로 본다.
    """
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh:
        rep = pathlib.Path(fh.name)
    try:
        r = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-q", "-k", kexpr,
             "-p", "no:randomly", "--no-header",
             "--json-report", f"--json-report-file={rep}"],
            cwd=_sandboxed(ROOT), capture_output=True, text=True, timeout=1800)
        if rep.is_file() and rep.stat().st_size:
            data = json.loads(rep.read_text(encoding="utf-8"))
            out = {"rc": r.returncode, "nodes": {}, "collect_errors": []}
            # ★ 46차 — collector 오류를 **따로** 본다. 수집이 깨지면 test
            #   node 가 아예 없고, 45차 판정은 그것을 "아무도 안 물었다" 와
            #   구별하지 못했다 (둘 다 실패로 보이지만 원인이 전혀 다르다).
            for c in data.get("collectors", []):
                if c.get("outcome") != "passed":
                    out["collect_errors"].append(
                        f"{c.get('nodeid')}:{c.get('outcome')}")
            for t in data.get("tests", []):
                phases = {ph: t[ph]["outcome"] for ph in
                          ("setup", "call", "teardown") if ph in t}
                out["nodes"][t["nodeid"]] = {
                    "outcome": t.get("outcome"), "phases": phases,
                    "longrepr": str((t.get("call") or {}).get("longrepr") or "")}
            return out
        # json-report 플러그인이 없으면 **조용히 넘어가지 않는다**
        raise _ReplayError(
            "pytest-json-report 가 필요하다 — `pip install pytest-json-report` "
            f"(rc={r.returncode})")
    finally:
        rep.unlink(missing_ok=True)


class _ReplayError(RuntimeError):
    pass


def _check(name: str, kexpr: str, before: dict, after: dict,
           nodes: list[str]) -> tuple[list[str], dict]:
    """변이가 **정확히 선언한 node 들만** · **선언한 이유로** 빨개졌는가.

    ★ 46차 #9 조건 9 — 45차 판정은 "call 단계에서 하나라도 빨개졌다" 였다.
      그것으로는 두 가지를 구별할 수 없다:

        · 기대한 시험이 물었는가, 아니면 **다른** 시험이 물었는가
        · 물었다면 **그 불변식 때문에** 물었는가, 아니면 변이가 만든 엉뚱한
          부수효과(다른 assert·다른 예외) 때문인가

      그래서 mutant 마다 **기대 실패 집합**과 **의미 증인**(실패 메시지에
      반드시 있어야 하는 문자열)을 선언하고 정확히 대조한다.
    """
    bad = []
    observed = {"fail": [], "witness": {}}
    base_fail = sorted(k for k, v in before["nodes"].items()
                       if v["outcome"] != "passed")
    if before["rc"] != 0:
        bad.append(f"{name}: baseline rc 가 0 이 아니다 ({before['rc']})")
    if before["collect_errors"]:
        bad.append(f"{name}: baseline 수집 오류 — {before['collect_errors'][:3]}")
    if base_fail:
        bad.append(f"{name}: baseline 이 이미 빨갛다 — {base_fail[:3]}")
    if sorted(before["nodes"]) != nodes:
        bad.append(f"{name}: baseline 이 수집 목록과 다르다")
    if bad:
        return bad, observed
    if after["collect_errors"]:
        bad.append(f"{name}: 변이가 수집을 깼다 — {after['collect_errors'][:3]}")
        return bad, observed
    if sorted(after["nodes"]) != nodes:
        bad.append(f"{name}: 변이 뒤 node 목록이 달라졌다 — "
                   f"사라짐 {sorted(set(nodes) - set(after['nodes']))[:3]}")
        return bad, observed
    # pytest rc: 0 = 전부 통과 · 1 = 시험 실패 · 2 중단 · 3 내부 오류 · 5 미수집
    if after["rc"] != 1:
        bad.append(f"{name}: 변이 rc 가 1(시험 실패)이 아니다 ({after['rc']})")
    failed, errored = [], []
    for k, v in after["nodes"].items():
        if v["outcome"] == "passed":
            continue
        if v["phases"].get("call") == "failed":
            failed.append(k)
            observed["witness"][k] = _last_line(v["longrepr"])
        else:
            errored.append(f"{k}:{v['phases']}")
    observed["fail"] = sorted(failed)
    if errored:
        bad.append(f"{name}: call 단계가 아닌 실패가 있다 — {errored[:3]}")
    exp = EXPECT.get(name)
    if exp is None:
        bad.append(f"{name}: 기대 실패 집합이 선언되지 않았다 "
                   "(`--emit-expect` 로 관측한 값을 EXPECT 에 적어라)")
        return bad, observed
    # ★ 50차 P1 — **빈 기대 집합**은 "아무 시험도 안 물어야 한다" 는 선언이고,
    #   그것은 곧 "안 물었다" 다. 실행 가능 변이로 등록해 놓고 그렇게 적으면
    #   전수 인증이 거짓이 된다 — 관측이 안 되면 `DECLARED_MASKED` 로 신고하라.
    if not exp["fail"]:
        bad.append(f"{name}: 기대 실패 집합이 비었다 — 실행 가능 변이는 반드시 "
                   "무언가를 물어야 한다 (관측 안 되면 신고로 옮겨라)")
        return bad, observed
    if sorted(failed) != sorted(exp["fail"]):
        bad.append(
            f"{name}: 실패 집합이 선언과 다르다 — 더 빨개짐 "
            f"{sorted(set(failed) - set(exp['fail']))[:3]} · 안 빨개짐 "
            f"{sorted(set(exp['fail']) - set(failed))[:3]}")
    # ★ 46차 — 증인은 **node 마다** 다르다. 한 mutant 가 여러 시험을 빨갛게
    #   만들면 (parametrize·다중 대상) 그 메시지들은 서로 다른 문장이다.
    #   증인 하나를 전부에 요구하면, 통과시키려고 증인을 가장 약한 공통
    #   부분문자열로 깎게 된다 — 그러면 "그 이유로 물었다" 를 증명하지 못한다.
    wit = exp["witness"]
    if not isinstance(wit, dict):
        bad.append(f"{name}: 증인이 node→문자열 map 이 아니다")
        return bad, observed
    for k in failed:
        want = wit.get(k)
        if want is None:
            bad.append(f"{name}: {k} 의 증인이 선언되지 않았다")
            continue
        if want not in (after["nodes"][k]["longrepr"] or ""):
            bad.append(
                f"{name}: {k} 이 빨개졌지만 **선언한 이유**가 아니다 — "
                f"증인 {want!r} 이 실패 메시지에 없다 "
                f"({_last_line(after['nodes'][k]['longrepr'])!r})")
    return bad, observed


def _select(k: str):
    """고른 scenario 를 **한 곳에서** 분류한다 (49차 P1).

    48차는 `main()` 과 `_replay()` 가 각자 분류했고, `_replay()` 쪽만
    `MULTI` 의 declared 항목을 빠뜨렸다. 그래서 declared MULTI 하나만 고르면
    `scenario_declared 0 · ran 0` 에 rc 0, 그리고 "실행한 변이가 전부 물었다"
    라는 성공 문장이 나왔다 — **아무 것도 돌지 않았는데** 통과 보고였다.
    같은 분류를 두 곳에서 하면 약한 쪽이 실효 규칙이 된다.
    """
    items = [m for m in MUTANTS if k in m[0]]
    multi = [m for m in MULTI if k in m[0]]
    executed = [m for m in items if m[4] is not None]
    declared = [m for m in items if m[4] is None] + \
        [m for m in multi if m[3] is None]
    return items, multi, executed, declared


def _registry() -> dict:
    """전체 등록부 — 이름 → 분류·site 수·selector. 조각 합집합의 대조 기준이다."""
    reg: dict = {}
    for name, path, _o, _n, kexpr in MUTANTS:
        reg[name] = {"class": "executable" if kexpr is not None else "declared",
                     "sites": 1, "kexpr": kexpr, "file": path.name}
    for name, path, pairs, kexpr in MULTI:
        reg[name] = {"class": "executable" if kexpr is not None else "declared",
                     "sites": len(pairs), "kexpr": kexpr, "file": path.name}
    dup = len(MUTANTS) + len(MULTI) - len(reg)
    if dup:
        raise SystemExit(
            f"✗ 등록부에 같은 이름이 {dup}건 겹친다 — 뒤엣것이 앞엣것을 덮으므로 "
            "조각 합집합이 전수를 덮었는지 셀 수 없다")
    return reg


def _print_counts(items, multi, executed, declared, ran=None) -> None:
    """total · executable · declared site 를 **서로 다른 이름**으로 (48차).

    47차는 `--list` 가 declared 까지 세어 61, full run 이 executable 만 세어 58
    을 **같은 `site` 이름**으로 찍었다. 같은 단어가 두 값을 가리키면 요청문의
    숫자를 믿을 수 없다.
    """
    exec_multi = [m for m in multi if m[3] is not None]
    decl_multi = [m for m in multi if m[3] is None]
    total_sites = len(items) + sum(len(m[2]) for m in multi)
    exec_sites = len(executed) + sum(len(m[2]) for m in exec_multi)
    line = (f"\nscenario_total {len(items) + len(multi)} · "
            f"scenario_executable {len(executed) + len(exec_multi)} · "
            f"scenario_declared {len(declared)} · "
            f"site_total {total_sites} · site_executable {exec_sites} · "
            f"site_declared {total_sites - exec_sites}")
    if ran is not None:
        line += f" · ran {ran}"
    print(line)


def _last_line(text: str) -> str:
    """실패의 **의미**를 담은 줄 — 위치 줄(`file.py:12: X`)이 아니다.

    ★ 46차 — 증인이 위치 줄이면 편집 한 번에 줄 번호가 밀려 깨진다.
      pytest 는 assert/예외 메시지를 `E ` 로 시작하는 줄에 찍는다.
    """
    lines = [l.rstrip() for l in (text or "").splitlines()]
    for line in lines:
        if line.startswith("E "):
            return line[2:].strip()[:200]
    for line in reversed(lines):
        if line.strip():
            return line.strip()[:200]
    return ""


#: ★ 46차 #9 조건 9 — mutant 마다 **기대 실패 node 집합**과 **의미 증인**.
#:   `python3 docs/22p_gap/mutation_replay.py --emit-expect` 가 관측값을
#:   그대로 찍어 준다. 선언이 없는 mutant 는 오류다 (조용히 통과시키지
#:   않는다) — "물었다" 와 "**그 이유로** 물었다" 는 다른 주장이다.
#:
#:   `witness` 는 **node → 실패 메시지 부분문자열** map 이다. 시각·임시 경로
#:   처럼 실행마다 달라지는 부분은 손으로 잘라 안정한 접두만 남긴다.
EXPECT: dict = {
    "authority-frozen": {
        "fail": [
            "tests/test_docs_lint.py::test_a_frozen_authority_cannot_be_edited_by_its_holder"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_a_frozen_authority_cannot_be_edited_by_its_holder": "Failed: DID NOT RAISE any of (SystemExit, AttributeError)"
        }
    },
    "authority-frozenset": {
        "fail": [
            "tests/test_docs_lint.py::test_a_frozen_authority_holds_only_immutable_values"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_a_frozen_authority_holds_only_immutable_values": "AssertionError: authority 가 mutable 값을 들고 있다"
        }
    },
    "authority-registry": {
        "fail": [
            "tests/test_docs_lint.py::test_the_raw_publisher_takes_no_caller_authority"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_raw_publisher_takes_no_caller_authority": "AssertionError: ✗ 명부에 없는 다리를 게시하려 한다: ['a'] (roster=['caller-chosen-leg']) — 원장을 먼저 고쳐라"
        }
    },
    "both-pointers-checked": {
        "fail": [
            "tests/test_docs_lint.py::test_a_pointer_moved_by_another_writer_is_never_overwritten[ledger_seal]",
            "tests/test_docs_lint.py::test_a_pointer_moved_by_another_writer_is_never_overwritten[writable]"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_a_pointer_moved_by_another_writer_is_never_overwritten[ledger_seal]": "Failed: DID NOT RAISE SystemExit",
            "tests/test_docs_lint.py::test_a_pointer_moved_by_another_writer_is_never_overwritten[writable]": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "caller-stage-safe-read": {
        "fail": [
            "tests/test_docs_lint.py::test_a_dangling_symlink_in_the_caller_stage_never_creates_an_outside_file"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_a_dangling_symlink_in_the_caller_stage_never_creates_an_outside_file": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "canon-absorbs-the-pep701-empty-piece": {
        "fail": [
            "tests/test_docs_lint.py::test_the_canonical_form_agrees_on_every_supported_interpreter"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_canonical_form_agrees_on_every_supported_interpreter": "AssertionError: 정규형이 지원 선언한 인터프리터에서 golden 과 다르다:"
        }
    },
    "children-read-through-dirfd": {
        "fail": [
            "tests/test_docs_lint.py::test_the_generation_reader_holds_a_directory_fd_for_its_children"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_generation_reader_holds_a_directory_fd_for_its_children": "AssertionError: child stat 이 dirfd 를 쓰지 않는다"
        }
    },
    "claim-checks-the-whole-index": {
        "fail": [
            "tests/test_preserve.py::test_the_whole_index_must_be_consistent_before_any_leg_is_claimed"
        ],
        "witness": {
            "tests/test_preserve.py::test_the_whole_index_must_be_consistent_before_any_leg_is_claimed": "Failed: DID NOT RAISE PreserveError"
        }
    },
    "claim-is-atomic": {
        "fail": [
            "tests/test_preserve.py::test_exactly_one_attempt_enters_compute"
        ],
        "witness": {
            "tests/test_preserve.py::test_exactly_one_attempt_enters_compute": "Failed: DID NOT RAISE PreserveError"
        }
    },
    "claim-seals-the-run-spec": {
        "fail": [
            "tests/test_preserve.py::test_the_claim_seals_the_exact_run_spec"
        ],
        "witness": {
            "tests/test_preserve.py::test_the_claim_seals_the_exact_run_spec": "Failed: DID NOT RAISE PreserveError"
        }
    },
    "claim-stores-a-verifier-not-the-token": {
        "fail": [
            "tests/test_preserve.py::test_the_claim_file_never_stores_the_resume_credential"
        ],
        "witness": {
            "tests/test_preserve.py::test_the_claim_file_never_stores_the_resume_credential": "AssertionError: claim 파일이 재개 credential 을 평문으로 담았다"
        }
    },
    "closure-follows-module-aliases": {
        "fail": [
            "tests/test_docs_lint.py::test_the_closure_follows_a_module_alias_attribute"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_closure_follows_a_module_alias_attribute": "AssertionError: module alias 로 부른 채점 함수가 닫힘 밖이다 — `from ... import` 만 따라가면 문법 하나로 identity 를 빠져나간다"
        }
    },
    "closure-refuses-dynamic-resolution": {
        "fail": [
            "tests/test_docs_lint.py::test_dynamic_name_resolution_inside_the_closure_is_fail_closed[__import__('src.scoring').scoring.add_error_columns(df)]",
            "tests/test_docs_lint.py::test_dynamic_name_resolution_inside_the_closure_is_fail_closed[eval('add_error_columns')(df)]",
            "tests/test_docs_lint.py::test_dynamic_name_resolution_inside_the_closure_is_fail_closed[exec('pass')]",
            "tests/test_docs_lint.py::test_dynamic_name_resolution_inside_the_closure_is_fail_closed[getattr(sc, 'add_error_columns')(df)]",
            "tests/test_docs_lint.py::test_dynamic_name_resolution_inside_the_closure_is_fail_closed[globals()['add_error_columns'](df)]",
            "tests/test_docs_lint.py::test_dynamic_name_resolution_inside_the_closure_is_fail_closed[vars(sc)['add_error_columns'](df)]"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_dynamic_name_resolution_inside_the_closure_is_fail_closed[__import__('src.scoring').scoring.add_error_columns(df)]": "Failed: DID NOT RAISE SystemExit",
            "tests/test_docs_lint.py::test_dynamic_name_resolution_inside_the_closure_is_fail_closed[eval('add_error_columns')(df)]": "Failed: DID NOT RAISE SystemExit",
            "tests/test_docs_lint.py::test_dynamic_name_resolution_inside_the_closure_is_fail_closed[exec('pass')]": "Failed: DID NOT RAISE SystemExit",
            "tests/test_docs_lint.py::test_dynamic_name_resolution_inside_the_closure_is_fail_closed[getattr(sc, 'add_error_columns')(df)]": "Failed: DID NOT RAISE SystemExit",
            "tests/test_docs_lint.py::test_dynamic_name_resolution_inside_the_closure_is_fail_closed[globals()['add_error_columns'](df)]": "Failed: DID NOT RAISE SystemExit",
            "tests/test_docs_lint.py::test_dynamic_name_resolution_inside_the_closure_is_fail_closed[vars(sc)['add_error_columns'](df)]": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "canon-keeps-docstrings": {
        "fail": [
            "tests/test_docs_lint.py::test_a_docstring_the_computation_reads_is_inside_the_identity"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_a_docstring_the_computation_reads_is_inside_the_identity": "AssertionError: `score_canonical.__doc__` 로 읽는 docstring 을 바꿨는데 producer digest 가 그대로다 — 계산이 쓰는 값이 identity 밖에 있다"
        }
    },
    "external-binding-covers-the-package": {
        "fail": [
            "tests/test_fitting.py::test_the_external_input_binding_covers_the_whole_package"
        ],
        "witness": {
            "tests/test_fitting.py::test_the_external_input_binding_covers_the_whole_package": "tools.preserve.PreserveError: [plan] 계획이 승인한 입력 묶음과 지금 읽는 묶음이 다르다"
        }
    },
    "fit-axis-seals-the-config-closure": {
        "fail": [
            "tests/test_fitting.py::test_the_base_config_parent_is_inside_the_approval_digest"
        ],
        "witness": {
            "tests/test_fitting.py::test_the_base_config_parent_is_inside_the_approval_digest": "AssertionError: `extends` 부모를 바꿔도 승인 digest 가 같다 — 승인은 실제로 읽히는 파일 전부를 담아야 한다"
        }
    },
    "fit-axis-seals-the-objective-payload": {
        "fail": [
            "tests/test_fitting.py::test_the_objective_payload_is_inside_the_approval_digest"
        ],
        "witness": {
            "tests/test_fitting.py::test_the_objective_payload_is_inside_the_approval_digest": "AssertionError: 같은 이름 아래 다른 가중치가 같은 승인 digest 를 냈다 — 승인한 것은 계산이 아니라 이름이다"
        }
    },
    "fit-stages-its-inputs-before-the-gate": {
        "fail": [
            "tests/test_fitting.py::test_run_fit_hands_the_body_the_staged_copies_not_the_originals"
        ],
        "witness": {
            "tests/test_fitting.py::test_run_fit_hands_the_body_the_staged_copies_not_the_originals": "AssertionError: 본체가 staging 뿌리를 못 받았다"
        }
    },
    "freeze-completes-a-half-written-transition": {
        "fail": [
            "tests/test_docs_lint.py::test_freeze_is_retryable_after_a_crash_between_its_two_writes"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_freeze_is_retryable_after_a_crash_between_its_two_writes": "SystemExit: ✗ cohort 'gZ' 는 이미 frozen 으로 기록됐다 — 두 번 얼릴 수 없다"
        }
    },
    "freeze-seals-the-output-directory": {
        "fail": [
            "tests/test_docs_lint.py::test_a_frozen_directory_cannot_be_republished_under_a_new_cohort_id"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_a_frozen_directory_cannot_be_republished_under_a_new_cohort_id": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "grid-axis-seals-the-discharged-cache": {
        "fail": [
            "tests/test_grid.py::test_the_grid_axis_binds_the_discharged_state_cache"
        ],
        "witness": {
            "tests/test_grid.py::test_the_grid_axis_binds_the_discharged_state_cache": "AssertionError: 완방상태 캐시를 갈아도 승인 digest 가 같다 — 승인 밖에서 격자 truth 의 기준점이 움직인다"
        }
    },
    "module-defs-enter-compound-statements": {
        "fail": [
            "tests/test_docs_lint.py::test_the_producer_closure_sees_every_module_binding_form"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_producer_closure_sees_every_module_binding_form": "AssertionError: module-level `for` 이 묶은 계산 상수를 바꿨는데 producer digest 가 그대로다 — 그 문법으로 identity 밖에 나갈 수 있다"
        }
    },
    "module-defs-fail-closed-on-unknown": {
        "fail": [
            "tests/test_docs_lint.py::test_an_unmodelled_module_binding_form_is_fail_closed"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_an_unmodelled_module_binding_form_is_fail_closed": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "open-checks-the-live-claim-first": {
        "fail": [
            "tests/test_preserve.py::test_a_second_open_never_touches_the_live_owners_token"
        ],
        "witness": {
            "tests/test_preserve.py::test_a_second_open_never_touches_the_live_owners_token": "AssertionError: 두 번째 발급이 살아 있는 owner 의 소유 증명을 덮었다"
        }
    },
    "release-moves-the-ledger-before-the-claim": {
        "fail": [
            "tests/test_preserve.py::test_a_crash_inside_release_leaves_a_recoverable_state"
        ],
        "witness": {
            "tests/test_preserve.py::test_a_crash_inside_release_leaves_a_recoverable_state": "AssertionError: assert not True"
        }
    },
    "rollback-rereads-the-committed-state": {
        "fail": [
            "tests/test_preserve.py::test_a_durability_error_after_the_ledger_commit_keeps_the_claim"
        ],
        "witness": {
            "tests/test_preserve.py::test_a_durability_error_after_the_ledger_commit_keeps_the_claim": "AssertionError: 커밋된 전이인데 claim 을 지웠다 — 회수 불가능한 running orphan"
        }
    },
    "token-path-is-disjoint-from-authority": {
        "fail": [
            "tests/test_preserve.py::test_the_token_path_cannot_alias_the_claim_authority"
        ],
        "witness": {
            "tests/test_preserve.py::test_the_token_path_cannot_alias_the_claim_authority": "AssertionError: assert not True"
        }
    },
    "token-unlink-is-generation-scoped": {
        "fail": [
            "tests/test_preserve.py::test_a_late_release_cleanup_cannot_delete_the_next_attempts_token"
        ],
        "witness": {
            "tests/test_preserve.py::test_a_late_release_cleanup_cannot_delete_the_next_attempts_token": "AssertionError: 옛 release 의 cleanup 이 새 attempt 의 token 을 지웠다"
        }
    },
    "abandon-rechecks-the-live-attempt": {
        "fail": [
            "tests/test_preserve.py::test_a_readonly_claim_cannot_abandon_the_live_owner",
            "tests/test_preserve.py::test_a_stale_claim_handle_cannot_cancel_the_next_attempt"
        ],
        "witness": {
            "tests/test_preserve.py::test_a_readonly_claim_cannot_abandon_the_live_owner": "Failed: DID NOT RAISE PreserveError",
            "tests/test_preserve.py::test_a_stale_claim_handle_cannot_cancel_the_next_attempt": "Failed: DID NOT RAISE PreserveError"
        }
    },
    "closure-unresolved-attr-is-fail-closed": {
        "fail": [
            "tests/test_docs_lint.py::test_an_unresolved_producer_module_reference_is_fail_closed"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_an_unresolved_producer_module_reference_is_fail_closed": "KeyError: '그런것은없다'"
        }
    },
    "complete-current-supersedes-pending": {
        "fail": [
            "tests/test_docs_lint.py::test_a_complete_current_supersedes_a_leftover_pending"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_a_complete_current_supersedes_a_leftover_pending": "SystemExit: ✗ 남아 있는 `.PENDING` 이 다른 base 위에서 만들어졌다 (pending base None ≠ 현재 70ec079e9fd6) — 승인되지 않은 구성을 이어받지 않는다. `.PENDING` 을 지우고 지금의 base 에서 다시 쌓아라"
        }
    },
    "crash-recovery-is-idempotent": {
        "fail": [
            "tests/test_preserve.py::test_finalize_is_idempotent_after_a_crash_before_cleanup"
        ],
        "witness": {
            "tests/test_preserve.py::test_finalize_is_idempotent_after_a_crash_before_cleanup": "tools.preserve.PreserveError: [plan] 'L' 의 계획 상태가 'executed' 이라 승인이 아니다 (허용 ['planned', 'running']) — 실행 기록은 다음 실행의 승인이 아니고, 이미 running 인 다리를 새로 시작할 수도 없다. 다시 돌리려면 새 계획 항목을 적어라"
        }
    },
    "crash-recovery-needs-the-credential": {
        "fail": [
            "tests/test_preserve.py::test_the_crash_recovery_needs_the_owner_credential"
        ],
        "witness": {
            "tests/test_preserve.py::test_the_crash_recovery_needs_the_owner_credential": "Failed: DID NOT RAISE PreserveError"
        }
    },
    "diagnostic-hides-the-credential": {
        "fail": [
            "tests/test_preserve.py::test_the_diagnostic_reader_never_hands_out_the_credential"
        ],
        "witness": {
            "tests/test_preserve.py::test_the_diagnostic_reader_never_hands_out_the_credential": "Failed: DID NOT RAISE PreserveError"
        }
    },
    "dry-run-releases-the-claim": {
        "fail": [
            "tests/test_grid.py::test_a_dry_run_does_not_strand_the_plan_in_running"
        ],
        "witness": {
            "tests/test_grid.py::test_a_dry_run_does_not_strand_the_plan_in_running": "AssertionError: dry-run 이 계획을 running 에 남겼다 — 그 다리는 다시 시작할 수도 닫을 수도 없다"
        }
    },
    "finalize-holds-the-claim-lock": {
        "fail": [
            "tests/test_preserve.py::test_the_canonical_lock_order_is_declared_and_finalize_holds_the_claim"
        ],
        "witness": {
            "tests/test_preserve.py::test_the_canonical_lock_order_is_declared_and_finalize_holds_the_claim": "AssertionError: finalize 가 claim lock 을 쥐지 않고 지나갔다 — 검사한 receipt 와 기록한 receipt 가 다를 수 있다"
        }
    },
    "finalize-rechecks-in-the-ledger-lock": {
        "fail": [
            "tests/test_preserve.py::test_finalize_rechecks_the_whole_authority_inside_the_ledger_lock"
        ],
        "witness": {
            "tests/test_preserve.py::test_finalize_rechecks_the_whole_authority_inside_the_ledger_lock": "AssertionError: 얼어붙은 cohort 에 실행 기록을 썼다: 'ok'"
        }
    },
    "finalize-requires-the-credential": {
        "fail": [
            "tests/test_preserve.py::test_finalize_requires_the_owner_credential"
        ],
        "witness": {
            "tests/test_preserve.py::test_finalize_requires_the_owner_credential": "AssertionError: Regex pattern did not match."
        }
    },
    "finalize-writes-the-whole-tuple": {
        "fail": [
            "tests/test_preserve.py::test_finalize_writes_a_complete_contract_status_tuple"
        ],
        "witness": {
            "tests/test_preserve.py::test_finalize_writes_a_complete_contract_status_tuple": "AssertionError: 계약 §8 의 validation_status 축이 비었다 — 튜플이 불완전하다"
        }
    },
    "fit-axis-is-the-real-policy": {
        "fail": [
            "tests/test_preserve.py::test_the_fit_axis_seals_every_intent_that_changes_the_answer"
        ],
        "witness": {
            "tests/test_preserve.py::test_the_fit_axis_seals_every_intent_that_changes_the_answer": "tools.preserve.PreserveError: [plan] leg run spec 의 fit 축이 계약과 다르다"
        }
    },
    "fit-axis-seals-the-input-content": {
        "fail": [
            "tests/test_preserve.py::test_the_fit_axis_seals_the_input_content_axes[base_config_digest-0000000000000000]",
            "tests/test_preserve.py::test_the_fit_axis_seals_the_input_content_axes[halfcell_cache_sha256-0000000000000000000000000000000000000000000000000000000000000000]"
        ],
        "witness": {
            "tests/test_preserve.py::test_the_fit_axis_seals_the_input_content_axes[base_config_digest-0000000000000000]": "AssertionError: base_config_digest 가 승인 축에 없다",
            "tests/test_preserve.py::test_the_fit_axis_seals_the_input_content_axes[halfcell_cache_sha256-0000000000000000000000000000000000000000000000000000000000000000]": "AssertionError: halfcell_cache_sha256 가 승인 축에 없다"
        }
    },
    "flock-two-publisher": {
        "fail": [
            "tests/test_docs_lint.py::test_two_independent_publishers_lose_no_leg"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_two_independent_publishers_lose_no_leg": "AssertionError: A 가 lock 을 든 동안 B 가 게시에 성공했다: {\"published\": false, \"public\": true}"
        }
    },
    "generation-namespace-guard": {
        "fail": [
            "tests/test_docs_lint.py::test_the_current_generation_cannot_be_used_as_its_own_staging[nested]",
            "tests/test_docs_lint.py::test_the_current_generation_cannot_be_used_as_its_own_staging[self]"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_current_generation_cannot_be_used_as_its_own_staging[nested]": "Failed: DID NOT RAISE SystemExit",
            "tests/test_docs_lint.py::test_the_current_generation_cannot_be_used_as_its_own_staging[self]": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "generation-root-nofollow": {
        "fail": [
            "tests/test_docs_lint.py::test_a_symlinked_gen_ancestor_never_holds_a_generation"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_a_symlinked_gen_ancestor_never_holds_a_generation": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "guard-before-commit": {
        "fail": [
            "tests/test_docs_lint.py::test_a_same_roster_ledger_change_is_refused",
            "tests/test_docs_lint.py::test_replacing_the_lock_pathname_after_the_check_refuses_the_commit"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_a_same_roster_ledger_change_is_refused": "Failed: DID NOT RAISE SystemExit",
            "tests/test_docs_lint.py::test_replacing_the_lock_pathname_after_the_check_refuses_the_commit": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "idempotent-shares-the-validator": {
        "fail": [
            "tests/test_docs_lint.py::test_the_idempotent_branch_refuses_an_aliased_generation_file"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_idempotent_branch_refuses_an_aliased_generation_file": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "inner-unbound-kernel": {
        "fail": [
            "tests/test_docs_lint.py::test_an_exact_lock_cannot_blank_its_own_inner_check"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_an_exact_lock_cannot_blank_its_own_inner_check": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "inner-unbound-sentinel": {
        "fail": [
            "tests/test_docs_lint.py::test_an_exact_lock_cannot_blank_its_sentinel_check"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_an_exact_lock_cannot_blank_its_sentinel_check": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "ledger-dir-contained": {
        "fail": [
            "tests/test_docs_lint.py::test_the_ledger_parser_refuses_a_dir_that_is_not_contained[./docs/22p_gap/coh]",
            "tests/test_docs_lint.py::test_the_ledger_parser_refuses_a_dir_that_is_not_contained[docs//22p_gap/coh]",
            "tests/test_docs_lint.py::test_the_ledger_parser_refuses_a_dir_that_is_not_contained[docs/22p_gap/../../outside]"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_ledger_parser_refuses_a_dir_that_is_not_contained[./docs/22p_gap/coh]": "Failed: DID NOT RAISE SystemExit",
            "tests/test_docs_lint.py::test_the_ledger_parser_refuses_a_dir_that_is_not_contained[docs//22p_gap/coh]": "Failed: DID NOT RAISE SystemExit",
            "tests/test_docs_lint.py::test_the_ledger_parser_refuses_a_dir_that_is_not_contained[docs/22p_gap/../../outside]": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "ledger-seal-record": {
        "fail": [
            "tests/test_docs_lint.py::test_a_same_roster_ledger_change_is_refused"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_a_same_roster_ledger_change_is_refused": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "ledger-status-enum": {
        "fail": [
            "tests/test_docs_lint.py::test_the_ledger_status_is_an_exact_enum[ACTIVE]",
            "tests/test_docs_lint.py::test_the_ledger_status_is_an_exact_enum[Active]",
            "tests/test_docs_lint.py::test_the_ledger_status_is_an_exact_enum[retired]"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_ledger_status_is_an_exact_enum[ACTIVE]": "Failed: DID NOT RAISE SystemExit",
            "tests/test_docs_lint.py::test_the_ledger_status_is_an_exact_enum[Active]": "Failed: DID NOT RAISE SystemExit",
            "tests/test_docs_lint.py::test_the_ledger_status_is_an_exact_enum[retired]": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "lifecycle-chain-is-verified": {
        "fail": [
            "tests/test_docs_lint.py::test_the_lifecycle_journal_is_a_hash_chain"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_lifecycle_journal_is_a_hash_chain": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "lifecycle-head-anchors-the-tip": {
        "fail": [
            "tests/test_docs_lint.py::test_the_lifecycle_journal_is_a_hash_chain"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_lifecycle_journal_is_a_hash_chain": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "missing-journal-with-a-live-anchor": {
        "fail": [
            "tests/test_docs_lint.py::test_deleting_the_journal_does_not_erase_the_freeze"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_deleting_the_journal_does_not_erase_the_freeze": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "module-defs-see-tuple-targets": {
        "fail": [
            "tests/test_docs_lint.py::test_the_producer_closure_follows_a_tuple_defined_constant",
            "tests/test_docs_lint.py::test_the_producer_closure_sees_tuple_targets"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_producer_closure_follows_a_tuple_defined_constant": "AssertionError: tuple 로 정의한 계산 상수를 바꿨는데 producer digest 가 그대로다",
            "tests/test_docs_lint.py::test_the_producer_closure_sees_tuple_targets": "AssertionError: ['C', 'G']"
        }
    },
    "module-gate-before-side-effects": {
        "fail": [
            "tests/test_preserve.py::test_run_grid_calls_the_gate_before_its_first_side_effect"
        ],
        "witness": {
            "tests/test_preserve.py::test_run_grid_calls_the_gate_before_its_first_side_effect": "KeyError: 'discharged_state'"
        }
    },
    "namespace-check-rejects-symlinks": {
        "fail": [
            "tests/test_preserve.py::test_a_symlinked_path_is_not_inside_the_smoke_namespace",
            "tests/test_preserve.py::test_the_namespace_check_is_fail_closed_on_a_symlinked_component"
        ],
        "witness": {
            "tests/test_preserve.py::test_a_symlinked_path_is_not_inside_the_smoke_namespace": "AssertionError: symlink 을 지나 밖으로 나가는 경로가 안이라고 판정됐다",
            "tests/test_preserve.py::test_the_namespace_check_is_fail_closed_on_a_symlinked_component": "AssertionError: symlink 성분을 지난 경로를 안으로 봤다 — 나중에 target 을 바꾸면 밖이다"
        }
    },
    "pending-base-generation": {
        "fail": [
            "tests/test_docs_lint.py::test_a_stale_bootstrap_pending_is_refused_not_inherited[wrong_base]"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_a_stale_bootstrap_pending_is_refused_not_inherited[wrong_base]": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "pending-closed-schema": {
        "fail": [
            "tests/test_docs_lint.py::test_a_stale_bootstrap_pending_is_refused_not_inherited[missing_base_key]"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_a_stale_bootstrap_pending_is_refused_not_inherited[missing_base_key]": "KeyError: 'base_generation'"
        }
    },
    "phase-input-binding": {
        "fail": [
            "tests/test_preserve.py::test_fit_refuses_curves_that_its_grid_phase_did_not_produce"
        ],
        "witness": {
            "tests/test_preserve.py::test_fit_refuses_curves_that_its_grid_phase_did_not_produce": "Failed: DID NOT RAISE PreserveError"
        }
    },
    "phase-input-binding-covers-the-package": {
        "fail": [
            "tests/test_preserve.py::test_the_grid_receipt_binds_every_curve_input_not_just_the_parquet"
        ],
        "witness": {
            "tests/test_preserve.py::test_the_grid_receipt_binds_every_curve_input_not_just_the_parquet": "AssertionError: 결속 대상이 바뀌었다: ['curves_sha256'] — fit 이 읽는 입력이 늘거나 줄었다면 그 사실이 여기 보여야 한다"
        }
    },
    "phase-input-binding-needs-a-receipt": {
        "fail": [
            "tests/test_preserve.py::test_fit_refuses_when_its_grid_phase_is_missing"
        ],
        "witness": {
            "tests/test_preserve.py::test_fit_refuses_when_its_grid_phase_is_missing": "AttributeError: 'NoneType' object has no attribute 'get'"
        }
    },
    "phase-write-checks-the-credential": {
        "fail": [
            "tests/test_preserve.py::test_a_forged_claim_object_cannot_write_a_phase"
        ],
        "witness": {
            "tests/test_preserve.py::test_a_forged_claim_object_cannot_write_a_phase": "Failed: DID NOT RAISE PreserveError"
        }
    },
    "phase-write-refuses-a-closed-claim": {
        "fail": [
            "tests/test_preserve.py::test_a_closed_run_cannot_be_resurrected_by_a_late_phase",
            "tests/test_preserve.py::test_a_released_run_cannot_be_resurrected_by_a_late_phase"
        ],
        "witness": {
            "tests/test_preserve.py::test_a_closed_run_cannot_be_resurrected_by_a_late_phase": "FileNotFoundError: [Errno 2] No such file or directory: '",
            "tests/test_preserve.py::test_a_released_run_cannot_be_resurrected_by_a_late_phase": "FileNotFoundError: [Errno 2] No such file or directory: '"
        }
    },
    "pin-is-publication-authority": {
        "fail": [
            "tests/test_docs_lint.py::test_the_producer_pin_is_part_of_the_publication_authority"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_producer_pin_is_part_of_the_publication_authority": "KeyError: 'pin'"
        }
    },
    "plan-index-exact-equality": {
        "fail": [
            "tests/test_preserve.py::test_a_phantom_executed_plan_without_an_execution_record_is_refused"
        ],
        "witness": {
            "tests/test_preserve.py::test_a_phantom_executed_plan_without_an_execution_record_is_refused": "AssertionError: [plan] 'Z' 의 계획 digest 가 실행 기록과 다르다 (계획 fedcba9876543210 ≠ 기록 aabbccddeeff0011) — 계획 index 가 실물을 가리키지 않으면 장식이다"
        }
    },
    "plan-parser-dir-hygiene": {
        "fail": [
            "tests/test_preserve.py::test_the_plan_parser_requires_a_canonical_relative_dir[./docs/22p_gap/coh]",
            "tests/test_preserve.py::test_the_plan_parser_requires_a_canonical_relative_dir[docs//22p_gap/coh]"
        ],
        "witness": {
            "tests/test_preserve.py::test_the_plan_parser_requires_a_canonical_relative_dir[./docs/22p_gap/coh]": "Failed: DID NOT RAISE PreserveError",
            "tests/test_preserve.py::test_the_plan_parser_requires_a_canonical_relative_dir[docs//22p_gap/coh]": "Failed: DID NOT RAISE PreserveError"
        }
    },
    "planned-binds-the-code-identity": {
        "fail": [
            "tests/test_preserve.py::test_the_gate_binds_the_plan_to_the_code_identity"
        ],
        "witness": {
            "tests/test_preserve.py::test_the_gate_binds_the_plan_to_the_code_identity": "Failed: DID NOT RAISE PreserveError"
        }
    },
    "planned-binds-the-execution-record": {
        "fail": [
            "tests/test_preserve.py::test_the_planned_index_is_bound_to_the_real_execution_record"
        ],
        "witness": {
            "tests/test_preserve.py::test_the_planned_index_is_bound_to_the_real_execution_record": "Failed: DID NOT RAISE PreserveError"
        }
    },
    "planned-status-is-not-standing": {
        "fail": [
            "tests/test_preserve.py::test_an_already_executed_leg_is_not_a_standing_authorization"
        ],
        "witness": {
            "tests/test_preserve.py::test_an_already_executed_leg_is_not_a_standing_authorization": "Failed: DID NOT RAISE PreserveError"
        }
    },
    "pointer-binds-the-ledger": {
        "fail": [
            "tests/test_docs_lint.py::test_expanding_a_roster_over_an_active_cohort_requires_a_new_cohort"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_expanding_a_roster_over_an_active_cohort_requires_a_new_cohort": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "pointer-loss-is-terminal": {
        "fail": [
            "tests/test_docs_lint.py::test_losing_the_pointer_of_a_cohort_that_has_generations_is_terminal"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_losing_the_pointer_of_a_cohort_that_has_generations_is_terminal": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "policy-binds-the-roster": {
        "fail": [
            "tests/test_docs_lint.py::test_the_single_leg_policy_must_match_the_roster_cardinality"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_single_leg_policy_must_match_the_roster_cardinality": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "pre-write-authority": {
        "fail": [
            "tests/test_docs_lint.py::test_a_frozen_cohort_publish_writes_nothing_before_it_refuses"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_a_frozen_cohort_publish_writes_nothing_before_it_refuses": "AssertionError: 거부하기 전에 무언가를 만들었다: ['.publish.lock', 'gen']"
        }
    },
    "precheck-tells-new-from-resume": {
        "fail": [
            "tests/test_preserve.py::test_the_precheck_tells_a_new_run_from_an_owned_resume"
        ],
        "witness": {
            "tests/test_preserve.py::test_the_precheck_tells_a_new_run_from_an_owned_resume": "tools.preserve.PreserveError: [plan] 'L' 의 계획 상태가 'running' 이라 승인이 아니다 (허용 ['planned']) — 실행 기록은 다음 실행의 승인이 아니고, 이미 running 인 다리를 새로 시작할 수도 없다. 다시 돌리려면 새 계획 항목을 적어라"
        }
    },
    "prelock-digest-check": {
        "fail": [
            "tests/test_preserve.py::test_wrong_bytes_are_never_locked"
        ],
        "witness": {
            "tests/test_preserve.py::test_wrong_bytes_are_never_locked": "AssertionError: digest 와 다른 바이트로 version 을 만들었다"
        }
    },
    "prelock-readback-check": {
        "fail": [
            "tests/test_preserve.py::test_a_provider_that_returns_the_wrong_version_locks_nothing"
        ],
        "witness": {
            "tests/test_preserve.py::test_a_provider_that_returns_the_wrong_version_locks_nothing": "AssertionError: provider 가 신고한 version 을 확인 없이 잠갔다"
        }
    },
    "prelock-version-id-is-a-string": {
        "fail": [
            "tests/test_preserve.py::test_a_falsy_version_id_from_put_is_refused[0]",
            "tests/test_preserve.py::test_a_falsy_version_id_from_put_is_refused[None]",
            "tests/test_preserve.py::test_a_falsy_version_id_from_put_is_refused[]"
        ],
        "witness": {
            "tests/test_preserve.py::test_a_falsy_version_id_from_put_is_refused[0]": "AssertionError: falsy version ID 로 잠갔다",
            "tests/test_preserve.py::test_a_falsy_version_id_from_put_is_refused[None]": "AssertionError: falsy version ID 로 잠갔다",
            "tests/test_preserve.py::test_a_falsy_version_id_from_put_is_refused[]": "AssertionError: falsy version ID 로 잠갔다"
        }
    },
    "preservation-status-inside-the-contract": {
        "fail": [
            "tests/test_preserve.py::test_the_runtime_preservation_enum_is_inside_the_contract"
        ],
        "witness": {
            "tests/test_preserve.py::test_the_runtime_preservation_enum_is_inside_the_contract": "AssertionError: 계약 §8 에 없는 보존 상태를 runtime 이 쓴다: ['no_bundle'] — 어휘의 정본이 둘이면 원장이 자기 lint 를 통과하지 못한다"
        }
    },
    "producer-canon-drops-empty-fields": {
        "fail": [
            "tests/test_docs_lint.py::test_the_producer_digest_is_the_same_on_every_python_here"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_producer_digest_is_the_same_on_every_python_here": "AssertionError: producer 의미 digest 가 인터프리터마다 다르다"
        }
    },
    "producer-crosses-into-scoring": {
        "fail": [
            "tests/test_docs_lint.py::test_the_producer_digest_crosses_into_src_scoring"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_producer_digest_crosses_into_src_scoring": "AssertionError: src.scoring 의 채점 허용오차를 바꿨는데 producer digest 가 그대로다 — 닫힘이 모듈 경계에서 멈춰 있다"
        }
    },
    "producer-crossing-is-fail-closed": {
        "fail": [
            "tests/test_docs_lint.py::test_breaking_the_crossing_into_src_scoring_is_fail_closed"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_breaking_the_crossing_into_src_scoring_is_fail_closed": "KeyError: 'DEFAULT_TOL'"
        }
    },
    "producer-cut-is-declared": {
        "fail": [
            "tests/test_docs_lint.py::test_the_producer_semantic_digest_excludes_the_publication_path"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_producer_semantic_digest_excludes_the_publication_path": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "producer-cut-is-sealed": {
        "fail": [
            "tests/test_docs_lint.py::test_widening_the_producer_cut_moves_the_digest"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_widening_the_producer_cut_moves_the_digest": "AssertionError: 절단면을 넓혔는데 producer digest 가 그대로다 — 절단면 정의가 봉인 preimage 밖이다"
        }
    },
    "producer-normalizes-the-node": {
        "fail": [
            "tests/test_docs_lint.py::test_the_producer_digest_sees_decorators"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_producer_digest_sees_decorators": "AssertionError: 계산 함수에 decorator 를 붙였는데 producer digest 가 그대로다 — 정규형이 source segment 라 decorator 를 못 본다"
        }
    },
    "producer-semantic-sealed": {
        "fail": [
            "tests/test_docs_lint.py::test_a_producer_change_cannot_mix_two_producers_in_one_generation",
            "tests/test_docs_lint.py::test_the_producer_semantic_identity_is_sealed"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_a_producer_change_cannot_mix_two_producers_in_one_generation": "SystemExit: ✗ 게시하려는 generation 의 producer 가 원장 봉인과 다르다 — 한 cohort 안에 서로 다른 producer 가 만든 leg 를 섞지 않는다:",
            "tests/test_docs_lint.py::test_the_producer_semantic_identity_is_sealed": "AssertionError: producer 의미 identity 가 봉인 밖이다: ('schema_version', 'analysis_spec_sha256')"
        }
    },
    "proof-handoff-to-verify": {
        "fail": [
            "tests/test_preserve.py::test_a_pre_journal_finalize_uses_the_repaired_pin_proof"
        ],
        "witness": {
            "tests/test_preserve.py::test_a_pre_journal_finalize_uses_the_repaired_pin_proof": "tools.preserve.PreserveError: [retention] lease pin 의 기한이 짧다:"
        }
    },
    "publisher-owns-the-merge-temp": {
        "fail": [
            "tests/test_docs_lint.py::test_the_caller_stage_is_untouched_when_the_final_guard_fails"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_caller_stage_is_untouched_when_the_final_guard_fails": "FileExistsError: [Errno 17] File exists:"
        }
    },
    "reader-shares-the-validator": {
        "fail": [
            "tests/test_docs_lint.py::test_the_generation_reader_refuses_an_aliased_generation_file"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_generation_reader_refuses_an_aliased_generation_file": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "recheck-before-rename": {
        "fail": [
            "tests/test_docs_lint.py::test_the_pointer_is_rechecked_immediately_before_the_rename"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_pointer_is_rechecked_immediately_before_the_rename": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "release-returns-the-plan": {
        "fail": [
            "tests/test_preserve.py::test_a_released_run_returns_the_plan_to_planned"
        ],
        "witness": {
            "tests/test_preserve.py::test_a_released_run_returns_the_plan_to_planned": "AssertionError: 되돌렸는데 계획이 running 에 남았다 — 그 다리는 영영 못 돌린다"
        }
    },
    "repair-source-uses-the-snapshot": {
        "fail": [
            "tests/test_preserve.py::test_no_version_enumeration_bypasses_the_helper",
            "tests/test_preserve.py::test_repair_lookups_go_through_the_validated_version_snapshot"
        ],
        "witness": {
            "tests/test_preserve.py::test_no_version_enumeration_bypasses_the_helper": "AssertionError: version 열거 우회가 2곳 있다 (['self.provider.versions(', 'getattr(self.provider, \"versions\"']) — 모든 열거는 `_version_candidates()` 를 지나야 한다",
            "tests/test_preserve.py::test_repair_lookups_go_through_the_validated_version_snapshot": "Failed: DID NOT RAISE PreserveError"
        }
    },
    "resume-compares-the-verifier": {
        "fail": [
            "tests/test_preserve.py::test_a_crash_after_grid_resumes_and_finalizes"
        ],
        "witness": {
            "tests/test_preserve.py::test_a_crash_after_grid_resumes_and_finalizes": "Failed: DID NOT RAISE PreserveError"
        }
    },
    "roster-is-a-set": {
        "fail": [
            "tests/test_docs_lint.py::test_the_ledger_roster_is_a_set_not_a_multiset"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_ledger_roster_is_a_set_not_a_multiset": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "row-selection-seals-its-content": {
        "fail": [
            "tests/test_preserve.py::test_the_fit_axis_seals_the_row_selection_content"
        ],
        "witness": {
            "tests/test_preserve.py::test_the_fit_axis_seals_the_row_selection_content": "AssertionError: 행 선택의 **내용**이 승인 밖이다 — 다른 표본으로 돌려도 같은 digest 다"
        }
    },
    "seal-exact-types": {
        "fail": [
            "tests/test_docs_lint.py::test_an_omap_and_a_list_of_lists_do_not_share_a_seal"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_an_omap_and_a_list_of_lists_do_not_share_a_seal": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "seal-finite-floats": {
        "fail": [
            "tests/test_docs_lint.py::test_the_seal_domain_is_exact_not_isinstance[nonfinite]"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_seal_domain_is_exact_not_isinstance[nonfinite]": "AssertionError: ✗ 원장 cohort 의 `pin` 이 계약 필드 집합이 아니다: None — ['analysis_spec_sha256', 'compute_sha256', 'producer_semantic_sha256', 'row_projection_py_sha256', 'schema_version', 'src_scoring_py_sha256'"
        }
    },
    "seal-typed-input": {
        "fail": [
            "tests/test_docs_lint.py::test_a_ledger_whose_types_differ_is_not_folded_into_one_seal[date_leg]",
            "tests/test_docs_lint.py::test_a_ledger_whose_types_differ_is_not_folded_into_one_seal[date_scalar]"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_a_ledger_whose_types_differ_is_not_folded_into_one_seal[date_leg]": "AssertionError: ✗ 원장 cohort 의 `legs` 가 문자열 목록이 아니다: [datetime.date(2026, 8, 28)]",
            "tests/test_docs_lint.py::test_a_ledger_whose_types_differ_is_not_folded_into_one_seal[date_scalar]": "AssertionError: ✗ 원장 cohort 의 `pin` 이 계약 필드 집합이 아니다: None — ['analysis_spec_sha256', 'compute_sha256', 'producer_semantic_sha256', 'row_projection_py_sha256', 'schema_version', 'src_scoring_py_sha256'"
        }
    },
    "sink-subset-of-roster": {
        "fail": [
            "tests/test_docs_lint.py::test_a_complete_undeclared_leg_never_reaches_pending"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_a_complete_undeclared_leg_never_reaches_pending": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "sink-validates-itself": {
        "fail": [
            "tests/test_docs_lint.py::test_the_sink_refuses_an_incomplete_generation_with_a_genuine_authority"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_sink_refuses_an_incomplete_generation_with_a_genuine_authority": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "staging-nlink-one": {
        "fail": [
            "tests/test_docs_lint.py::test_staging_aliases_never_become_an_immutable_generation[hardlink]"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_staging_aliases_never_become_an_immutable_generation[hardlink]": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "staging-regular-only": {
        "fail": [
            "tests/test_docs_lint.py::test_staging_aliases_never_become_an_immutable_generation[symlink]"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_staging_aliases_never_become_an_immutable_generation[symlink]": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "thaw-is-refused-before-the-first-write": {
        "fail": [
            "tests/test_docs_lint.py::test_the_publisher_refuses_a_thawed_cohort_before_the_first_write"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_publisher_refuses_a_thawed_cohort_before_the_first_write": "AssertionError: 거부하면서 무언가를 만들었다 — 판정이 첫 write 뒤에 있다"
        }
    },
    "thaw-transition-is-unrepresentable": {
        "fail": [
            "tests/test_docs_lint.py::test_a_frozen_cohort_cannot_be_thawed_and_published"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_a_frozen_cohort_cannot_be_thawed_and_published": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "token-is-written-before-the-claim": {
        "fail": [
            "tests/test_preserve.py::test_a_crash_between_the_claim_and_the_token_leaves_nothing_stranded"
        ],
        "witness": {
            "tests/test_preserve.py::test_a_crash_between_the_claim_and_the_token_leaves_nothing_stranded": "AssertionError: claim 은 남았는데 소유 증명이 없다 — 이어받을 수도 되돌릴 수도 닫을 수도 없는 다리가 생겼다"
        }
    },
    "trust-boundary-declared": {
        "fail": [
            "tests/test_docs_lint.py::test_the_publisher_declares_its_trust_boundary"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_publisher_declares_its_trust_boundary": "AssertionError: publisher 가 신뢰 경계를 선언하지 않는다"
        }
    },
    "version-candidates-typed": {
        "fail": [
            "tests/test_preserve.py::test_a_falsy_version_never_reaches_lock",
            "tests/test_preserve.py::test_every_enumerated_version_candidate_must_be_a_nonempty_string"
        ],
        "witness": {
            "tests/test_preserve.py::test_a_falsy_version_never_reaches_lock": "Failed: DID NOT RAISE PreserveError",
            "tests/test_preserve.py::test_every_enumerated_version_candidate_must_be_a_nonempty_string": "Failed: DID NOT RAISE PreserveError"
        }
    },
    "warm-consumer-uses-accessor": {
        "fail": [
            "tests/test_docs_lint.py::test_the_warm_consumers_go_through_the_accessors"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_warm_consumers_go_through_the_accessors": "AssertionError: warm 소비자 → accessor 배선이 선언과 다르다. 새 소비자를 넣거나 호출을 뺐다면 `_WARM_CONSUMER_EDGES` 를 함께 고쳐라 (그 diff 가 리뷰에 보여야 한다)."
        }
    },
    "warm-edges-are-declared": {
        "fail": [
            "tests/test_docs_lint.py::test_the_warm_consumers_go_through_the_accessors"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_warm_consumers_go_through_the_accessors": "AssertionError: warm 소비자 → accessor 배선이 선언과 다르다. 새 소비자를 넣거나 호출을 뺐다면 `_WARM_CONSUMER_EDGES` 를 함께 고쳐라 (그 diff 가 리뷰에 보여야 한다)."
        }
    }
}


def main() -> int:
    global SANDBOX
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--emit-expect", action="store_true",
                    help="관측한 기대 실패 집합·증인을 JSON 으로 찍는다")
    ap.add_argument("--keep-sandbox", action="store_true")
    ap.add_argument("-k", default="", help="이름 부분일치로 고른다")
    ap.add_argument("--emit-coverage", default=None, metavar="PATH",
                    help="이 조각이 덮은 scenario 를 기계 판독 JSON 으로 남긴다 "
                         "(49차 P1 — 조각 합집합 증명용)")
    ap.add_argument("--check-coverage", nargs="+", default=None, metavar="PATH",
                    help="조각 JSON 들을 합쳐 등록부 전체를 덮었는지 답한다")
    ap.add_argument("--slice", default=None, metavar="I/N",
                    help="등록부를 이름순 N 조각으로 나눠 I 번째만 돈다 "
                         "(1부터). 전수를 한 번에 돌리면 시간이 넘치므로 "
                         "조각으로 나누고 `--check-coverage` 로 합집합을 "
                         "증명한다")
    ap.add_argument("--check-preimages", action="store_true",
                    help="모든 변이 지점이 **정확히 한 번** 나타나는지만 본다 "
                         "(pytest 를 돌리지 않는다 — 코드가 옮겨가 죽은 변이를 "
                         "싸게 찾는다)")
    a = ap.parse_args()

    if a.check_coverage:
        return check_coverage(a.check_coverage)
    if a.check_preimages:
        return check_preimages(a.k)

    items, multi, executed, declared = _select(a.k)
    if a.slice:
        i, n = (int(x) for x in a.slice.split("/"))
        if not (1 <= i <= n):
            print(f"✗ --slice {a.slice} 가 범위 밖이다")
            return 2
        names = sorted(m[0] for m in items + multi)
        keep = {nm for j, nm in enumerate(names) if j % n == i - 1}
        items = [m for m in items if m[0] in keep]
        multi = [m for m in multi if m[0] in keep]
        executed = [m for m in items if m[4] is not None]
        declared = [m for m in items if m[4] is None] + \
            [m for m in multi if m[3] is None]
    # ★ 48차 — **0건을 고르면 실패한다.** 47차 runner 는 `-k` 가 아무것도 고르지
    #   않아도 "전부 물었다" 를 찍고 rc 0 이었다 — 오타 하나로 증거 전체가
    #   조용히 사라지는 구조였다.
    if not items and not multi:
        print(f"✗ `-k {a.k}` 가 아무 scenario 도 고르지 않았다 — 이름을 "
              "확인하라 (0건을 성공으로 세지 않는다)")
        return 2
    if a.list:
        for name, path, _o, _n, kexpr in items:
            tag = "  (관측 안 됨 — 신고)" if kexpr is None else ""
            print(f"{name:30s} {path.name:20s} -k {kexpr}{tag}")
        for name, path, _pairs, kexpr in multi:
            print(f"{name:30s} {path.name:20s} -k {kexpr}  (2-site)")
        _print_counts(items, multi, executed, declared)
        return 0

    bad, ran = [], 0
    observed_all: dict = {}
    plan = [(n, p, [(o, w)], k) for n, p, o, w, k in executed]
    # ★ 48차 — `-k None` 인 MULTI 는 **신고**다. 실행 계획에 넣지 않는다.
    plan += [(n, p, pairs, k) for n, p, pairs, k in multi if k is not None]

    SANDBOX = _make_sandbox()
    print(f"sandbox: {SANDBOX}\n")
    try:
        rc = _replay(plan, bad, observed_all, a,
                     sel=(items, multi, executed, declared))
    finally:
        if a.keep_sandbox:
            print(f"\nsandbox 를 남긴다: {SANDBOX}")
        else:
            shutil.rmtree(SANDBOX.parent, ignore_errors=True)
    return rc


def _is_semantic_noop(src: str, old: str, new: str) -> bool:
    """이 치환이 **계산을 안 바꾸는가** (51차 P1-E2).

    50차는 `old == new` 만 봤다 — 바이트 부등식이다. 리뷰어가 주석 한 줄만
    더한 mutant 를 등록해 `check_preimages_rc=0` 를 받았다: 변이가 계산을 안
    바꾸면 시험은 당연히 초록이고, 그것을 "물었다" 로 세면 전수 인증이 거짓이
    된다.

    정규형(AST → `ast.unparse`)이 같으면 그 치환은 주석·공백·따옴표 서식만
    바꾼 것이다. 파싱이 안 되면 **변이로 인정한다** — 문법을 깨는 치환은
    적어도 no-op 은 아니다 (그 경우는 재생이 잡는다).
    """
    import ast

    if old not in src:
        return False
    try:
        a = ast.unparse(ast.parse(src))
        b = ast.unparse(ast.parse(src.replace(old, new, 1)))
    except SyntaxError:
        return False
    return a == b


def _registry_digest() -> str:
    """등록부 **전체**의 내용 주소 — 이름·파일·preimage·기대 node 까지 (51차)."""
    body = json.dumps(
        [[n, p.name, o, w, k] for n, p, o, w, k in MUTANTS]
        + [[n, p.name, list(map(list, pairs)), k] for n, p, pairs, k in MULTI],
        ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def _expect_digest() -> str:
    return hashlib.sha256(json.dumps(EXPECT, ensure_ascii=False, sort_keys=True)
                          .encode("utf-8")).hexdigest()


def _runner_digest() -> str:
    return hashlib.sha256(
        pathlib.Path(__file__).read_bytes()).hexdigest()


def _head() -> str:
    """이 증거가 어느 트리에서 나왔는가. git 이 없으면 빈 문자열."""
    import subprocess

    try:
        r = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                           text=True, cwd=str(pathlib.Path(__file__).parent))
        return r.stdout.strip() if r.returncode == 0 else ""
    except OSError:                                       # pragma: no cover
        return ""


def check_preimages(k: str = "") -> int:
    """변이 지점이 **살아 있는가** — pytest 없이 (49차).

    코드가 옮겨 가면 preimage 가 0번 또는 2번 나타나게 되고, 그 변이는 조용히
    "지점불량" 이 된다. 전수 재생은 비싸므로 그 전에 싸게 훑는다.
    """
    bad = []
    for name, path, old, new, kexpr in MUTANTS:
        if k not in name:
            continue
        if kexpr is None:
            continue                       # 신고 — 지점을 요구하지 않는다
        # ★ 50차 P1 — **아무 것도 안 바꾸는 변이**를 거부한다. `old == new` 면
        #   시험은 당연히 초록이고, 그것을 "물었다" 로 세면 전수 인증이 거짓이
        #   된다 (49차 리뷰어 지적). 변이가 아닌 것을 변이로 셀 수 없다.
        src = path.read_text(encoding="utf-8")
        if old == new:
            bad.append(f"{name:34s} {path.name:20s} 변이가 아무 것도 안 바꾼다")
        elif _is_semantic_noop(src, old, new):
            bad.append(f"{name:34s} {path.name:20s} 변이가 **의미**를 안 바꾼다 "
                       "(주석·공백·문자열 서식만)")
        c = src.count(old)
        if c != 1:
            bad.append(f"{name:34s} {path.name:20s} preimage {c}회")
    for name, path, pairs, kexpr in MULTI:
        if k not in name or kexpr is None:
            continue
        src = path.read_text(encoding="utf-8")
        for i, (old, new) in enumerate(pairs):
            if old == new:
                bad.append(f"{name:34s} {path.name:20s} site {i} 변이가 아무 "
                           "것도 안 바꾼다")
            elif _is_semantic_noop(src, old, new):
                bad.append(f"{name:34s} {path.name:20s} site {i} 변이가 "
                           "**의미**를 안 바꾼다 (주석·공백만)")
            c = src.count(old)
            if c != 1:
                bad.append(f"{name:34s} {path.name:20s} site {i} preimage {c}회")
    if bad:
        print("=== 죽은 변이 지점 ===")
        for b in bad:
            print(b)
        return 1
    print("모든 변이 지점이 정확히 한 번 나타난다")
    return 0


def _replay(plan, bad, observed_all, a, sel=None) -> int:
    items, multi, executed, declared = sel or _select(a.k)
    ran = 0
    bit: dict = {}

    for name, repo_path, pairs, kexpr in plan:
        path = _sandboxed(repo_path)
        # ★ 46차 — **raw bytes** 로 읽고 쓴다. text mode 는 개행·인코딩을
        #   접을 수 있어서 "원복이 바이트 동일하다" 를 증명할 수 없다.
        src = path.read_bytes()
        before_hash = hashlib.sha256(src).hexdigest()
        mutated, miss = src, None
        for old, new in pairs:
            ob, nb = old.encode("utf-8"), new.encode("utf-8")
            c = mutated.count(ob)
            if c != 1:
                miss = f"preimage 가 {c}번 나타난다"
                break
            mutated = mutated.replace(ob, nb, 1)
        if miss:
            print(f"{'★ 지점불량':10s} {name:30s} {miss}")
            bad.append(f"{name}: {miss}")
            continue
        try:
            nodes = _nodes(kexpr)
            if not nodes:
                raise _ReplayError(f"`-k {kexpr}` 가 아무 시험도 안 고른다")
            before = _run(kexpr)
            path.write_bytes(mutated)
            after = _run(kexpr)
        except _ReplayError as e:
            print(f"{'★ 실행오류':10s} {name:30s} {e}")
            bad.append(f"{name}: {e}")
            continue
        finally:
            path.write_bytes(src)
        post = hashlib.sha256(path.read_bytes()).hexdigest()
        if post != before_hash:
            bad.append(f"{name}: 원복이 바이트 동일하지 않다")
        errs, observed = _check(name, kexpr, before, after, nodes)
        observed_all[name] = observed
        ran += 1
        bit[name] = not errs
        print(f"{'물었다' if not errs else '★ 안 물었다':10s} {name:30s} "
              f"node {len(nodes)} · -k {kexpr}")
        bad += errs

    for decl in declared:
        name = decl[0]
        reason = DECLARED_MASKED.get(name)
        if not reason:
            # 신고에 **이유가 없으면** 그것은 신고가 아니라 누락이다.
            print(f"{'★ 사유없음':10s} {name:30s} — DECLARED_MASKED 에 항목이 없다")
            bad.append(f"{name}: 신고인데 DECLARED_MASKED 에 사유가 없다")
            continue
        print(f"{'신고':10s} {name:30s} — {reason}")

    if a.emit_expect:
        print("\n=== 관측한 EXPECT (그대로 붙여 넣어라) ===")
        print(json.dumps(
            {k: {"fail": v["fail"], "witness": v["witness"]}
             for k, v in sorted(observed_all.items())},
            ensure_ascii=False, indent=4, sort_keys=True))

    _print_counts(items, multi, executed, declared, ran=ran)

    n_exec = len(executed) + len([m for m in multi if m[3] is not None])
    # ★ 50차 P1 — **성공한 조각만** coverage 를 남긴다. 49차는 실패해도 파일을
    #   썼으므로, rc 를 안 보는 사람에게는 "덮었다" 로 읽혔다. 증거 파일은
    #   그 자체로 참이어야 한다.
    if a.emit_coverage and not bad and ran == n_exec:
        _write_coverage(a.emit_coverage, a.k, items, multi, declared, bit)

    if bad:
        print("\n=== 문제 ===")
        for b in bad:
            print(b)
        return 1
    # ★ 49차 P1 — **0건 실행을 성공으로 세지 않는다.** 48차는 실행 가능한
    #   scenario 를 하나도 돌리지 않고도 "전부 물었다" 를 찍고 rc 0 이었다.
    if ran != n_exec:
        print(f"✗ 실행 가능한 scenario {n_exec}건 중 {ran}건만 돌았다 — "
              "돌지 않은 것을 통과로 셀 수 없다")
        return 1
    if ran == 0:
        print(f"이 조각에는 실행 가능한 변이가 없다 (신고 {len(declared)}건뿐) "
              "— rc 0 이 '전부 물었다' 를 뜻하지 않는다")
        return 0
    print(f"실행한 변이 {ran}건이 전부 기대 node 를 call 단계에서 물었다")
    return 0


def _write_coverage(path, selector, items, multi, declared, bit) -> None:
    """이 조각이 **무엇을 덮었는지** 기계 판독 가능하게 남긴다 (49차 P1).

    전수(64건)를 한 번에 돌리면 시간이 넘치므로 조각으로 나눠 돌린다. 그러면
    "조각 합집합이 등록부 전체를 덮었는가" 를 사람이 로그를 눈으로 세어 답하게
    되는데, 그것은 증거가 아니다. `--check-coverage` 가 이 파일들을 합쳐 답한다.
    """
    decl_names = {d[0] for d in declared}
    scen = {}
    for name, _p, _o, _n, kexpr in items:
        scen[name] = {"class": "declared" if name in decl_names else "executable",
                      "sites": 1, "kexpr": kexpr,
                      "ran": name in bit, "bit": bit.get(name)}
    for name, _p, pairs, kexpr in multi:
        scen[name] = {"class": "declared" if name in decl_names else "executable",
                      "sites": len(pairs), "kexpr": kexpr,
                      "ran": name in bit, "bit": bit.get(name)}
    # ★ 51차 P1-E2 — 증거를 **이 등록부·이 코드·이 실행**에 묶는다. 50차
    #   artifact 는 아무 것에도 안 묶여 있어서, 과거 JSON 만으로 99/99 가
    #   나왔다 (리뷰어 실측 `replay_calls=0`). "무엇을 덮었다" 가 아니라
    #   "무엇이 실제로 돌았다" 가 증거다.
    transcript = json.dumps(
        [[n, bool(v["ran"]), (None if v["bit"] is None else bool(v["bit"]))]
         for n, v in sorted(scen.items())], ensure_ascii=False, sort_keys=True)
    rec = {"schema": "mutation-coverage/v2",
           "selector": selector,
           "at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "binding": {
               "registry_digest": _registry_digest(),
               "expect_digest": _expect_digest(),
               "runner_digest": _runner_digest(),
               "head": _head(),
               "transcript_digest": hashlib.sha256(
                   transcript.encode("utf-8")).hexdigest()},
           "scenarios": scen}
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rec, ensure_ascii=False, indent=2, sort_keys=True)
                 + "\n", encoding="utf-8")
    print(f"\ncoverage 조각을 남겼다: {p}")


def check_coverage(paths) -> int:
    """조각 합집합이 **등록부 전체**를 덮었는가 (49차 P1).

    덮었다는 주장을 로그 눈대중이 아니라 파일로 답한다. 실행 가능한 scenario 는
    전부 한 번 이상 **돌았고 물었어야** 하고, 신고는 전부 신고로 나타나야 한다.
    """
    reg = _registry()
    # ★ 50차 P1 — 합집합을 세기 전에 **등록부 자체**가 성립하는지 본다.
    #   no-op 변이·죽은 지점·빈 기대 집합이 있으면 그 위에서 센 수는 뜻이 없다.
    if check_preimages() != 0:
        print("✗ 등록부의 변이 지점이 성립하지 않는다 — 합집합을 셀 수 없다")
        return 1
    empty = sorted(n for n, m in reg.items()
                   if m["class"] == "executable"
                   and not (EXPECT.get(n) or {}).get("fail"))
    if empty:
        print("✗ 실행 가능 변이인데 기대 실패 집합이 비었거나 없다: "
              + ", ".join(empty))
        return 1
    # ★ 51차 P1-E2 — 조각이 **지금 이 등록부·이 runner** 에서 나왔는지 먼저 본다.
    want = {"registry_digest": _registry_digest(),
            "expect_digest": _expect_digest(),
            "runner_digest": _runner_digest()}
    seen: dict = {}
    for path in paths:
        rec = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
        if rec.get("schema") != "mutation-coverage/v2":
            print(f"✗ {path}: coverage schema 가 아니다: {rec.get('schema')!r} "
                  "(51차부터 v2 — 결속 없는 v1 은 증거가 아니다)")
            return 1
        binding = rec.get("binding") or {}
        for key, w in want.items():
            if binding.get(key) != w:
                print(f"✗ {path}: {key} 가 살아 있는 값과 다르다 "
                      f"({str(binding.get(key))[:16]} ≠ {w[:16]}) — 이 조각은 "
                      "지금 등록부/코드가 아닌 것에서 나왔다")
                return 1
        scen = rec.get("scenarios") or {}
        transcript = json.dumps(
            [[n, bool(v.get("ran")),
              (None if v.get("bit") is None else bool(v.get("bit")))]
             for n, v in sorted(scen.items())], ensure_ascii=False,
            sort_keys=True)
        got = hashlib.sha256(transcript.encode("utf-8")).hexdigest()
        if binding.get("transcript_digest") != got:
            print(f"✗ {path}: transcript_digest 가 담긴 결과와 다르다 "
                  f"({str(binding.get('transcript_digest'))[:16]} ≠ "
                  f"{got[:16]}) — 결과를 나중에 고쳤다")
            return 1
        for name, v in scen.items():
            cur = seen.setdefault(name, {"class": v["class"], "ran": False,
                                         "bit": None, "slices": []})
            if cur["class"] != v["class"]:
                print(f"✗ {name}: 조각마다 분류가 다르다 "
                      f"({cur['class']} ≠ {v['class']})")
                return 1
            cur["slices"].append(rec["selector"])
            if v.get("ran"):
                cur["ran"] = True
                cur["bit"] = bool(v.get("bit")) if cur["bit"] is None \
                    else (cur["bit"] and bool(v.get("bit")))

    bad = []
    for name, meta in sorted(reg.items()):
        got = seen.get(name)
        if got is None:
            bad.append(f"{name}: 어느 조각에도 나타나지 않았다 ({meta['class']})")
            continue
        if got["class"] != meta["class"]:
            bad.append(f"{name}: 분류가 등록부와 다르다 "
                       f"({got['class']} ≠ {meta['class']})")
        if meta["class"] == "executable" and not got["ran"]:
            bad.append(f"{name}: 실행 가능한데 어느 조각에서도 돌지 않았다")
        if meta["class"] == "executable" and got["ran"] and got["bit"] is False:
            bad.append(f"{name}: 돌았지만 물지 않았다")
    extra = sorted(set(seen) - set(reg))
    for name in extra:
        bad.append(f"{name}: 등록부에 없는 scenario 가 조각에 있다 (이름이 바뀌었나)")

    n_exec = sum(1 for m in reg.values() if m["class"] == "executable")
    n_decl = len(reg) - n_exec
    print(f"등록부 scenario {len(reg)} (executable {n_exec} · declared {n_decl}) · "
          f"조각 {len(paths)}개에서 관측 {len(seen)}")
    if bad:
        print("\n=== 덮이지 않은 것 ===")
        for b in bad:
            print(b)
        return 1
    print("조각 합집합이 등록부 전체를 정확히 덮었다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
