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
    # ── 47차 (게이트 46차 반증 조건) ──────────────────────────────────────
    ("generation-root-nofollow", RP,
     "        return os.open(d, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)",
     "        return os.open(d, os.O_RDONLY)",
     "generation_root_symlink_is_never_read_as_a_generation"),
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
    ("claim-is-atomic", PRESERVE,
     "        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)",
     "        fd = os.open(path, os.O_CREAT | os.O_WRONLY, 0o644)",
     "exactly_one_attempt_enters_compute"),
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
     "    _assert_grid_authorized(cfg, out_dir, dry_run=dry_run)\n",
     "",
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
     "    got = {n: _sha(b) for n, b in _generation_entries(gdir, out).items()}\n"
     "    if got != rec[\"files\"]:",
     "    got = {q.name: _sha(q.read_bytes())\n"
     "           for q in sorted(gdir.iterdir()) if q.is_file()}\n"
     "    if got != rec[\"files\"]:",
     "generation_reader_refuses_an_aliased"),
    ("idempotent-shares-the-validator", RP,
     "        got = {n: _sha(b) for n, b in _generation_entries(gdir, out).items()}",
     "        got = {q.name: _sha(q.read_bytes())\n"
     "               for q in sorted(gdir.iterdir()) if q.is_file()}",
     "idempotent_branch_refuses_an_aliased"),
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
     '    if e["status"] != "planned":',
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
     "            if st.st_nlink != 1:\n                bad.append(f\"{name}: 다른 이름과 inode 를 공유한다 \"",
     "            if False:\n                bad.append(f\"{name}: 다른 이름과 inode 를 공유한다 \"",
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
    ("ledger-seal-record", RP,
     "        if auth.ledger_seal_now() != auth.seal:",
     "        if set(_ledger_cohort(out).get('legs') or ()) != auth.roster:",
     "same_roster_ledger_change"),
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
]

#: 여러 지점을 **함께** 되돌려야 관측되는 변이 (심층 방어라 하나만 지우면
#: 다른 하나가 가린다). 41·42·43차에 실측했다.
MULTI = [
    # ★ 47차 — `dir_fd` 는 두 자리에 있다(`os.stat` · `os.open`). 하나만
    #   되돌리면 다른 철자가 남아 구조 검사가 통과한다 — 실측했다.
    ("children-read-through-dirfd", RP, [
        ("            st = os.stat(name, dir_fd=dfd, follow_symlinks=False)",
         "            st = os.stat(Path(stage) / name, follow_symlinks=False)"),
        ("            fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=dfd)",
         "            fd = os.open(Path(stage) / name, os.O_RDONLY | os.O_NOFOLLOW)"),
     ], "holds_a_directory_fd_for_its_children"),
    # ★ 47차 — 46차의 두 mutant 는 **옛 exploit 을 복원하지 않았다.**
    #   `generation-owns-its-bytes` 는 이미 만들어진 tmp 안으로 stage 를
    #   move 해서 중첩 디렉터리를 만들었고, 그 "extra directory" 오류가
    #   성공 증인으로 승인됐다. `staging-regular-only` 는 predicate 만 지워도
    #   `O_NOFOLLOW` 가 ELOOP 를 냈고 그 오류가 증인이 됐다. 둘 다 44차 이전
    #   동작을 그대로 되살리는 multi-site 로 고친다.
    ("staging-regular-only", RP, [
        ("            if not stat.S_ISREG(st.st_mode):        # symlink·FIFO·directory",
         "            if False:"),
        ("            fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=dfd)",
         "            fd = os.open(name, os.O_RDONLY, dir_fd=dfd)"),
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
    "complete-current-supersedes-pending": {
        "fail": [
            "tests/test_docs_lint.py::test_a_complete_current_supersedes_a_leftover_pending"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_a_complete_current_supersedes_a_leftover_pending": "SystemExit: ✗ 남아 있는 `.PENDING` 이 다른 base 위에서 만들어졌다 (pending base None ≠ 현재 f71b9a788c32) — 승인되지 않은 구성을 이어받지 않는다. `.PENDING` 을 지우고 지금의 base 에서 다시 쌓아라"
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
            "tests/test_docs_lint.py::test_a_generation_root_symlink_is_never_read_as_a_generation"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_a_generation_root_symlink_is_never_read_as_a_generation": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "guard-before-commit": {
        "fail": [
            "tests/test_docs_lint.py::test_a_same_roster_ledger_change_is_refused",
            "tests/test_docs_lint.py::test_replacing_the_lock_pathname_after_the_check_refuses_the_commit"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_a_same_roster_ledger_change_is_refused": "AssertionError: 원장이 frozen 이 됐는데 게시됐다",
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
            "tests/test_docs_lint.py::test_a_same_roster_ledger_change_is_refused": "AssertionError: 원장이 frozen 이 됐는데 게시됐다"
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
    "pin-is-publication-authority": {
        "fail": [
            "tests/test_docs_lint.py::test_the_producer_pin_is_part_of_the_publication_authority"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_producer_pin_is_part_of_the_publication_authority": "Failed: DID NOT RAISE SystemExit"
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
            "tests/test_docs_lint.py::test_a_frozen_cohort_publish_writes_nothing_before_it_refuses": "Failed: DID NOT RAISE SystemExit"
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
    "producer-cut-is-declared": {
        "fail": [
            "tests/test_docs_lint.py::test_the_producer_semantic_digest_excludes_the_publication_path"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_the_producer_semantic_digest_excludes_the_publication_path": "Failed: DID NOT RAISE SystemExit"
        }
    },
    "producer-semantic-sealed": {
        "fail": [
            "tests/test_docs_lint.py::test_a_producer_change_cannot_mix_two_producers_in_one_generation",
            "tests/test_docs_lint.py::test_the_producer_semantic_identity_is_sealed"
        ],
        "witness": {
            "tests/test_docs_lint.py::test_a_producer_change_cannot_mix_two_producers_in_one_generation": "Failed: DID NOT RAISE SystemExit",
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
    a = ap.parse_args()

    items = [m for m in MUTANTS if a.k in m[0]]
    multi = [m for m in MULTI if a.k in m[0]]
    executed = [m for m in items if m[4] is not None]
    declared = [m for m in items if m[4] is None]
    if a.list:
        for name, path, _o, _n, kexpr in items:
            tag = "  (관측 안 됨 — 신고)" if kexpr is None else ""
            print(f"{name:30s} {path.name:20s} -k {kexpr}{tag}")
        for name, path, _pairs, kexpr in multi:
            print(f"{name:30s} {path.name:20s} -k {kexpr}  (2-site)")
        print(f"\n총 {len(items) + len(multi)} scenario "
              f"({len(executed) + len(multi)} 실행 · {len(declared)} 신고) · "
              f"{sum(1 for m in items) + sum(len(m[2]) for m in multi)} site")
        return 0

    bad, ran = [], 0
    observed_all: dict = {}
    plan = [(n, p, [(o, w)], k) for n, p, o, w, k in executed]
    plan += [(n, p, pairs, k) for n, p, pairs, k in multi]

    SANDBOX = _make_sandbox()
    print(f"sandbox: {SANDBOX}\n")
    try:
        rc = _replay(plan, bad, observed_all, a)
    finally:
        if a.keep_sandbox:
            print(f"\nsandbox 를 남긴다: {SANDBOX}")
        else:
            shutil.rmtree(SANDBOX.parent, ignore_errors=True)
    return rc


def _replay(plan, bad, observed_all, a) -> int:
    items = [m for m in MUTANTS if a.k in m[0]]
    multi = [m for m in MULTI if a.k in m[0]]
    executed = [m for m in items if m[4] is not None]
    declared = [m for m in items if m[4] is None]
    ran = 0

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
        print(f"{'물었다' if not errs else '★ 안 물었다':10s} {name:30s} "
              f"node {len(nodes)} · -k {kexpr}")
        bad += errs

    for name, _p, _o, _n, _k in declared:
        print(f"{'신고':10s} {name:30s} — {DECLARED_MASKED[name]}")

    if a.emit_expect:
        print("\n=== 관측한 EXPECT (그대로 붙여 넣어라) ===")
        print(json.dumps(
            {k: {"fail": v["fail"], "witness": v["witness"]}
             for k, v in sorted(observed_all.items())},
            ensure_ascii=False, indent=4, sort_keys=True))

    print(f"\nscenario {len(items) + len(multi)} · 실행 {ran} · "
          f"신고 {len(declared)} · site "
          f"{len(executed) + sum(len(m[2]) for m in multi)}")
    if bad:
        print("\n=== 문제 ===")
        for b in bad:
            print(b)
        return 1
    print("실행한 변이가 전부 기대 node 를 call 단계에서 물었다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
