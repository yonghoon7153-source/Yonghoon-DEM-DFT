"""Regression for the success receipt of a fresh 7:3 RJ. Requires A5R01_KIT.

Run with python3 -I -X utf8 -B test_a5r01.py -v. The producer tests execute
only the generated Bash receipt path; the numeric readers and bundle are stubs.
"""
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


KIT = Path(os.environ["A5R01_KIT"]).resolve(strict=True)
sys.path.insert(0, str(KIT))
import a5_certificate as certificate


RESTORE = "reader_restore_rc=0"
KEBASE = "reader_kebase_rc=0"
SELECT = "reader_select_rc=0"
END = "end=2026-11-20T00:01:00Z fails=0 reader_rc=0"
BED = "ps_7_3_r45"


def synthetic_report():
    # Internal synthetic values isolate the completion protocol from the numeric reader.
    checks = {key: {"status": "PASS"} for key in ("G1", "G2", "G3", "mesh_md5", "rt_binding")}
    for key in ("G2cp", "cont_R", "cont_RT1"):
        checks[key] = dict(status="PASS", input_sha256=["a" * 64] * 2,
                           n_common=1, n_orig=1, n_test=1)
    for key, field in (("g0", "ok"), ("syntax", "ok"), ("pre_post", "equal"),
                       ("rt_resets", "ok"), ("rt_post_list", "ok"),
                       ("history_test", "pass"), ("un_erasure", "seen")):
        checks[key] = {field: True}
    checks["rt_technical"] = {key: {"ok": True} for key in ("R", "UN", "RT1", "RT2", "Ut0")}
    return dict(schema="rt_restore_candidate_v1", restore_rule="rev5_g2cp", status="RESTORED",
                bed=BED, job="RJ", s0=2000, certificate_published=True, checks=checks)


def prepare_job(root, select=False):
    job = root / BED / "RJ"
    job.mkdir(parents=True)
    fields = dict(bed=BED, job="RJ", np="6", resume="0", gate="ALLOW", job_dir=job.as_posix(),
                  start="2026-11-20T00:00:00Z",
                  sums_sha256=hashlib.sha256((KIT / "A5_SHA256SUMS").read_bytes()).hexdigest(),
                  lmp_sha256=certificate.LMP, grammar_prereq="PASS", rt_grammar_prereq="PASS",
                  orig_grid_prereq="PASS", rt_grammar_verdict_sha256=certificate.ANCHORS["a3_return.json"],
                  a3_readback_reader_sha256=certificate.ANCHORS["a3_corrected_reader.py"],
                  a4_historical_sha256=certificate.ANCHORS["a4_continuity.json"])
    if select:
        fields["a5_select_required"] = "1"
    (job / "run_manifest.txt").write_bytes("".join(f"{k}={v}\n" for k, v in fields.items()).encode())
    return job


class CompletionConsumer(unittest.TestCase):
    def tail(self, rows, expected, *, select=False, last_newline=True):
        with tempfile.TemporaryDirectory() as tmp:
            job = prepare_job(Path(tmp), select)
            certificate.issue(job, synthetic_report(), KIT)
            with (job / "run_manifest.txt").open("ab") as handle:
                handle.write(("\n".join(rows) + ("\n" if last_newline else "")).encode())
            self.assertIs(certificate.admits(job, KIT), expected)

    def test_normal_orders(self):
        self.tail([RESTORE, KEBASE, END], True)
        self.tail([RESTORE, KEBASE, SELECT, END], True, select=True)

    def test_required_kebase(self):
        for middle in ([], [KEBASE, KEBASE], ["reader_kebase_rc=2"]):
            with self.subTest(middle=middle):
                self.tail([RESTORE, *middle, END], False)

    def test_select_obligation(self):
        self.tail([RESTORE, KEBASE, END], False, select=True)
        self.tail([RESTORE, KEBASE, SELECT, END], False)

    def test_unknown_or_misordered(self):
        for rows in ((KEBASE, RESTORE), (RESTORE, SELECT, KEBASE),
                     (RESTORE, KEBASE, "reader_other_rc=0"), (RESTORE, KEBASE, KEBASE),
                     (RESTORE, KEBASE, SELECT, SELECT), (RESTORE, KEBASE, "reader_select_rc=2")):
            with self.subTest(rows=rows):
                self.tail([*rows, END], False, select=any("select" in item for item in rows))

    def test_final_line_must_be_complete(self):
        self.tail([RESTORE, KEBASE, END], False, last_newline=False)
        self.tail([RESTORE, KEBASE, END, END], False)


def extract_rj_runner():
    """Use text from the candidate, excluding preflight, stage execution and archival I/O."""
    source = (KIT / "run_unload_a5_candidate.sh").read_text(encoding="utf8")
    note = source.split('MAN="$JD/run_manifest.txt"\n', 1)[1].split("# ── 2.", 1)[0]
    reader = source.split("\nRRC=0\n", 1)[1].split('\ncase "$JOB" in\n', 1)[0]
    branch = source.split('\n    HV=(); [ -n ', 1)[1].split("\n", 1)[1].split("\n    ;;", 1)[0]
    end = source.rsplit("\nesac\n", 1)[1]
    return "MAN=\"$JD/run_manifest.txt\"\n" + note + "\nRRC=0\n" + reader + "\n" + branch + "\n" + end


HEADER = r'''set -uo pipefail
JD="$WORK_ROOT/ps_7_3_r45/RJ"
MAN="$JD/run_manifest.txt"
KIT="$A5R01_KIT"
BED=ps_7_3_r45
JOB=RJ
FAILS=0
HV=()
NEED_UK=1
PRE_OK=1
PY=fake_reader
say() { :; }
die() { echo "$*" >&2; exit 1; }
bundle() { :; }
date() {
    if [ "$FAULT" = final ] && [ "$1" = -Iseconds ]; then
        mv "$MAN" "$JD/saved_manifest" && mkdir "$MAN" || exit 89
    elif [ -d "$MAN" ] && [ "$FAULT" = kebase ]; then
        rmdir "$MAN" && mv "$JD/saved_manifest" "$MAN" || exit 89
    fi
    command date "$@"
}
fake_reader() {
    case "$3" in
        restore)
            "$TEST_PY" -I -X utf8 -B "$TEST_SCRIPT" --issue "$JD" || exit 89
            case "$CHANGE_UB" in
                create) mkdir "$WORK_ROOT/$BED/UB" || exit 89;;
                remove) rmdir "$WORK_ROOT/$BED/UB" || exit 89;;
            esac
            return "$RESTORE_RC";;
        kebase)
            if [ "$FAULT" = kebase ]; then
                mv "$MAN" "$JD/saved_manifest" && mkdir "$MAN" || exit 89
            fi
            return "$KEBASE_RC";;
        select) return 0;;
        *) exit 89;;
    esac
}
'''


@unittest.skipUnless(os.name == "posix", "requires a POSIX Bash and native path semantics")
class CompletionProducer(unittest.TestCase):
    def exercise(self, *, restore_rc=0, kebase_rc=0, select=False, change_ub="", fault="", expected_rc=0, admits=True):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            job = prepare_job(root)
            if select:
                (job.parent / "UB").mkdir()
            env = dict(os.environ, WORK_ROOT=str(root), TEST_PY=sys.executable,
                       TEST_SCRIPT=str(Path(__file__).resolve()), FAULT=fault, LC_ALL="C", CHANGE_UB=change_ub,
                       RESTORE_RC=str(restore_rc), KEBASE_RC=str(kebase_rc))
            run = subprocess.run(["bash"], input=HEADER + extract_rj_runner(), text=True,
                                 capture_output=True, env=env, timeout=30)
            saved = job / "saved_manifest"
            manifest = job / "run_manifest.txt"
            if saved.is_file():
                manifest.rmdir()
                saved.rename(manifest)
            self.assertNotEqual(run.returncode, 89, run.stderr)
            if fault:
                self.assertIn("Is a directory", run.stderr)
            if expected_rc is None:
                self.assertNotEqual(run.returncode, 0, run.stdout + run.stderr)
            else:
                self.assertEqual(run.returncode, expected_rc, run.stdout + run.stderr)
            self.assertIs(certificate.admits(job, KIT), admits, manifest.read_text())
            if change_ub:
                lines = manifest.read_text().splitlines()
                self.assertEqual(lines.count(SELECT), int(select))
                self.assertEqual(lines.count("a5_select_required=1"), int(select))

    def test_success_then_optional_select(self):
        self.exercise()
        self.exercise(select=True)

    def test_failed_reader_remains_failed(self):
        self.exercise(kebase_rc=2, expected_rc=2, admits=False)
        self.exercise(restore_rc=120, expected_rc=120, admits=False)

    def test_ub_appearing_after_restore_does_not_add_a_reader(self):
        self.exercise(change_ub="create")

    def test_ub_disappearing_after_restore_does_not_drop_a_reader(self):
        self.exercise(select=True, change_ub="remove")

    def test_kebase_row_append_io_failure(self):
        self.exercise(fault="kebase", expected_rc=None, admits=False)

    def test_final_row_append_io_failure(self):
        self.exercise(fault="final", expected_rc=None, admits=False)


if __name__ == "__main__":
    if sys.argv[1:2] == ["--issue"]:
        certificate.issue(Path(sys.argv[2]), synthetic_report(), KIT)
    else:
        unittest.main()
