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
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
PRESERVE = ROOT / "tools" / "preserve.py"
RP = ROOT / "docs" / "22p_gap" / "row_projection.py"
TDL = ROOT / "tests" / "test_docs_lint.py"

#: 단일 지점 변이 — (이름, 파일, old, new, 빨개져야 하는 -k)
MUTANTS = [
    # ── 45차 (게이트 44차 반증 조건) ──────────────────────────────────────
    ("authority-frozenset", RP,
     "    auth.roster = frozenset(cohort.get(\"legs\") or ())",
     "    auth.roster = set(cohort.get(\"legs\") or ())",
     "frozen_authority_holds_only_immutable"),
    ("sink-subset-of-roster", RP,
     "    undeclared = sorted(seen - auth.roster)\n    if undeclared:",
     "    undeclared = []\n    if undeclared:",
     "complete_undeclared_leg_never_reaches_pending"),
    ("staging-not-inside-gen", RP,
     "    if not allow_inside_gen and (st_res == gen_res or gen_res in st_res.parents):",
     "    if False:",
     "current_generation_cannot_be_used_as_its_own_staging"),
    ("staging-regular-only", RP,
     "        if not stat.S_ISREG(st.st_mode):        # symlink·FIFO·directory",
     "        if False:",
     "staging_aliases_never_become_an_immutable_generation"),
    ("staging-nlink-one", RP,
     "        if st.st_nlink != 1:\n            bad.append(f\"{name}: 다른 이름과 inode 를 공유한다 \"",
     "        if False:\n            bad.append(f\"{name}: 다른 이름과 inode 를 공유한다 \"",
     "staging_aliases_never_become_an_immutable_generation"),
    ("generation-owns-its-bytes", RP,
     "        for name in sorted(entries):\n            _write_owned(tmp / name, entries[name])",
     "        shutil.move(str(stage), str(tmp))",
     "a_published_generation_owns_its_bytes"),
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
    """`-k` 가 고르는 **정확한 node ID 목록** (실행하지 않고 수집만)."""
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q", "-k", kexpr,
         "--collect-only", "-p", "no:randomly", "--no-header"],
        cwd=ROOT, capture_output=True, text=True, timeout=1800)
    if r.returncode != 0:
        raise _ReplayError(f"수집 실패 (rc={r.returncode}): {r.stdout[-400:]}")
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
            cwd=ROOT, capture_output=True, text=True, timeout=1800)
        if rep.is_file() and rep.stat().st_size:
            data = json.loads(rep.read_text(encoding="utf-8"))
            out = {"rc": r.returncode, "nodes": {}}
            for t in data.get("tests", []):
                phases = {ph: t[ph]["outcome"] for ph in
                          ("setup", "call", "teardown") if ph in t}
                out["nodes"][t["nodeid"]] = {
                    "outcome": t.get("outcome"), "phases": phases}
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
           nodes: list[str]) -> list[str]:
    """변이가 **정확히 그 node 들만** 빨갛게 만들었는가."""
    bad = []
    base_fail = sorted(n for n, v in before["nodes"].items()
                       if v["outcome"] != "passed")
    if base_fail:
        bad.append(f"{name}: baseline 이 이미 빨갛다 — {base_fail[:3]}")
        return bad
    if sorted(before["nodes"]) != nodes:
        bad.append(f"{name}: baseline 이 수집 목록과 다르다")
        return bad
    failed, errored = [], []
    for n, v in after["nodes"].items():
        if v["outcome"] == "passed":
            continue
        # setup/teardown/collection 오류는 "물었다" 가 아니다
        if v["phases"].get("call") == "failed":
            failed.append(n)
        else:
            errored.append(f"{n}:{v['phases']}")
    if errored:
        bad.append(f"{name}: call 단계가 아닌 실패가 있다 — {errored[:3]}")
    if not failed:
        bad.append(f"{name}: 아무 시험도 물지 않았다 (-k {kexpr})")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--list", action="store_true")
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
    plan = [(n, p, [(o, w)], k) for n, p, o, w, k in executed]
    plan += [(n, p, pairs, k) for n, p, pairs, k in multi]

    for name, path, pairs, kexpr in plan:
        src = path.read_text(encoding="utf-8")
        before_hash = hashlib.sha256(src.encode("utf-8")).hexdigest()
        mutated, miss = src, None
        for old, new in pairs:
            c = mutated.count(old)
            if c != 1:
                miss = f"preimage 가 {c}번 나타난다"
                break
            mutated = mutated.replace(old, new, 1)
        if miss:
            print(f"{'★ 지점불량':10s} {name:30s} {miss}")
            bad.append(f"{name}: {miss}")
            continue
        try:
            nodes = _nodes(kexpr)
            if not nodes:
                raise _ReplayError(f"`-k {kexpr}` 가 아무 시험도 안 고른다")
            before = _run(kexpr)
            path.write_text(mutated, encoding="utf-8")
            after = _run(kexpr)
        except _ReplayError as e:
            print(f"{'★ 실행오류':10s} {name:30s} {e}")
            bad.append(f"{name}: {e}")
            continue
        finally:
            path.write_text(src, encoding="utf-8")
        post = hashlib.sha256(
            path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
        if post != before_hash:
            bad.append(f"{name}: 원복이 바이트 동일하지 않다")
        errs = _check(name, kexpr, before, after, nodes)
        ran += 1
        print(f"{'물었다' if not errs else '★ 안 물었다':10s} {name:30s} "
              f"node {len(nodes)} · -k {kexpr}")
        bad += errs

    for name, _p, _o, _n, _k in declared:
        print(f"{'신고':10s} {name:30s} — {DECLARED_MASKED[name]}")

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
