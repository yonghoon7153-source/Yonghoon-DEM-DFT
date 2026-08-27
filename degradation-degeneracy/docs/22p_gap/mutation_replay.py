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
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
PRESERVE = ROOT / "tools" / "preserve.py"
RP = ROOT / "docs" / "22p_gap" / "row_projection.py"
TDL = ROOT / "tests" / "test_docs_lint.py"

#: 단일 지점 변이 — (이름, 파일, old, new, 빨개져야 하는 -k)
MUTANTS = [
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
     "    _assert_sealable(cohort)\n    return hashlib.sha256(json.dumps(",
     "    return hashlib.sha256(json.dumps(",
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
     "pointer_moved_by_another"),
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
     "    if pending and set(rec) != _PENDING_KEYS:",
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
    "proof-until-equals-lease":
        "horizon 의 정본은 lease record 이고 verifier 가 exact ID 로 다시 "
        "확인한다. 이 assert 는 필드가 이름만 갖지 않게 하는 계약이며, "
        "현재 production 경로에서 둘이 갈라지는 반례가 없다.",
    "warm-consumer-wiring":
        "positive wiring 회귀는 배선이 **끊길 때** 빨개진다. assert 를 지우는 "
        "변이는 그 시험 자신만 무력화하므로 다른 시험이 물지 않는다 — "
        "이것은 회귀의 성질이지 결함이 아니다.",
}


def _run(k: str) -> tuple[int, str]:
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q", "-k", k,
         "-p", "no:randomly", "--no-header", "-x"],
        cwd=ROOT, capture_output=True, text=True, timeout=1800)
    return r.returncode, (r.stdout or "")[-400:]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("-k", default="", help="이름 부분일치로 고른다")
    a = ap.parse_args()

    items = [m for m in MUTANTS if a.k in m[0]]
    multi = [m for m in MULTI if a.k in m[0]]
    if a.list:
        for name, path, _o, _n, kexpr in items:
            tag = "  (관측 안 됨 — 신고)" if kexpr is None else ""
            print(f"{name:30s} {path.name:20s} -k {kexpr}{tag}")
        for name, path, _pairs, kexpr in multi:
            print(f"{name:30s} {path.name:20s} -k {kexpr}  (2-site)")
        return 0

    bad = []
    for name, path, old, new, kexpr in items:
        if kexpr is None:
            print(f"{'신고':10s} {name:30s} — {DECLARED_MASKED[name]}")
            continue
        src = path.read_text(encoding="utf-8")
        if old not in src:
            print(f"{'★ 지점없음':10s} {name}")
            bad.append(name)
            continue
        path.write_text(src.replace(old, new, 1), encoding="utf-8")
        try:
            rc, tail = _run(kexpr)
        finally:
            path.write_text(src, encoding="utf-8")
        print(f"{'물었다' if rc else '★ 안 물었다':10s} {name:30s} -k {kexpr}")
        if rc == 0:
            bad.append(f"{name}: {tail}")

    for name, path, pairs, kexpr in multi:
        src = path.read_text(encoding="utf-8")
        mutated, ok = src, True
        for old, new in pairs:
            if old not in mutated:
                ok = False
                break
            mutated = mutated.replace(old, new, 1)
        if not ok:
            print(f"{'★ 지점없음':10s} {name}")
            bad.append(name)
            continue
        path.write_text(mutated, encoding="utf-8")
        try:
            rc, tail = _run(kexpr)
        finally:
            path.write_text(src, encoding="utf-8")
        print(f"{'물었다' if rc else '★ 안 물었다':10s} {name:30s} -k {kexpr} (2-site)")
        if rc == 0:
            bad.append(f"{name}: {tail}")

    print()
    if bad:
        print("=== 안 문 변이 ===")
        for b in bad:
            print(b)
        return 1
    print("모든 변이가 물었다 (신고 항목 제외)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
