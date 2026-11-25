"""Tests for the reg1 (contact mini) execution block and its reader, written before the block.

    python3 -I -X utf8 -B docs/reviews/suyoung_next_registrations_20261125/reg1_block/test_reg1_block.py

DEVELOPMENT_ONLY.  No registered arm is run and no MPM step is taken: the reader is fed
format-faithful synthetic runs (synth_runs.py, invented numbers), and the end-to-end GO path
uses a test-only fake worker (fake_worker.py) in place of `driver.py RUN`.  The shipped block has
no test switch: every test path is a modified copy of the package (environment constant set to
this container, worker path set to the fake worker), with its manifest regenerated.
"""
import atexit
import collections
import contextlib
import copy
import gzip
import hashlib
import importlib.util
import io
import json
import math
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import unittest

import numpy as np


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
BLOCK_REL = "docs/reviews/suyoung_next_registrations_20261125/reg1_block/"
REG1 = HERE.parent / "reg1_contact_mini_20261125.md"
FAKE_PIN = "0123456789abcdef0123456789abcdef01234567"
CONTAINER_ENV = (platform.python_version(), np.__version__)
SHIPPED_ENV = ("3.12.3", "2.5.2")
_CACHE = {}


def load(name):
    """A module from this folder, loaded by path (cached)."""
    if name not in _CACHE:
        spec = importlib.util.spec_from_file_location("reg1_block_test_" + name, HERE / (name + ".py"))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _CACHE[name] = module
    return _CACHE[name]


def bb():
    return load("build_block")


def qu():
    return load("reg1_queue")


def rd():
    return load("reg1_reader")


def synth():
    return load("synth_runs")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read_repo(relative):
    return (REPO / relative).read_bytes()


def scratch(test, prefix="reg1_block_"):
    path = Path(tempfile.mkdtemp(prefix=prefix))
    test.addCleanup(shutil.rmtree, path, True)
    return path


def lasting(prefix):
    path = Path(tempfile.mkdtemp(prefix=prefix))
    atexit.register(shutil.rmtree, path, True)
    return path


def write_tree(files, dst):
    dst = Path(dst)
    for relative, data in files.items():
        path = dst / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return dst


def replace_once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)


def test_files(environment=None, worker=False, scenario=None, pin=FAKE_PIN):
    """Package files; optionally the test path (environment constant, fake worker), manifest regenerated."""
    files = bb().collect(read_repo, pin)
    if environment is None and not worker:
        return files
    queue = files["reg1_queue.py"].decode("utf-8")
    if environment is not None:
        queue = replace_once(queue, f"TARGET_ENVIRONMENT = {SHIPPED_ENV!r}", f"TARGET_ENVIRONMENT = {tuple(environment)!r}")
    if worker:
        queue = replace_once(queue, "WORKER = DRIVER", 'WORKER = "fake_worker.py"')
        files["fake_worker.py"] = (HERE / "fake_worker.py").read_bytes()
        files["synth_runs.py"] = (HERE / "synth_runs.py").read_bytes()
        files["fake_scenario.json"] = json.dumps(scenario or {}, sort_keys=True).encode("ascii")
    files["reg1_queue.py"] = queue.encode("utf-8")
    del files["SOURCE_SHA256SUMS"]
    files["SOURCE_SHA256SUMS"] = bb().manifest(files)
    return files


def write_txt(files, folder, pin=FAKE_PIN):
    txt = bb().operator(bb().package(files), pin)
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / bb().txt_name(pin)
    path.write_bytes(txt)
    (folder / (path.name + ".sha256")).write_bytes(bb().manifest({path.name: txt}))
    return path


def make_home(top):
    """A scratch HOME whose ~/Yonghoon-DEM-DFT/venv/bin/python logs its arguments and runs this Python."""
    home = Path(top) / "home"
    venv = home / "Yonghoon-DEM-DFT" / "venv" / "bin"
    venv.mkdir(parents=True)
    log = Path(top) / "python_calls.log"
    shim = venv / "python"
    shim.write_text(f"#!/bin/sh\nprintf '%s\\n' \"$*\" >> '{log}'\nexec '{sys.executable}' \"$@\"\n")
    shim.chmod(0o755)
    return home, log


def run_txt(txt, home, *args, cwd=None, timeout=1800):
    env = {"HOME": str(home), "PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LC_ALL": "C.UTF-8"}
    return subprocess.run(["bash", str(txt), *args], cwd=str(cwd or Path(txt).parent), env=env,
                          capture_output=True, text=True, timeout=timeout)


def make_root(dst):
    """A package root (block files at the top, pinned files at repo paths, RELEASE, manifest)."""
    return write_tree(test_files(), dst)


def base_run():
    """One unperturbed synthetic run over a package root, shared by the reader tests."""
    if "base" not in _CACHE:
        top = lasting("reg1_block_base_")
        root = make_root(top / "root")
        run = synth().write_run(root, top / "base_run")
        _CACHE["base"] = (root, run)
    return _CACHE["base"]


def scenario_run(test, specs=None, **kw):
    root, base = base_run()
    run = scratch(test, "reg1_block_run_") / "run"
    synth().write_run(root, run, specs=specs, base=base, **kw)
    return root, run


def summarize(root, run, environment=CONTAINER_ENV):
    return rd().summarize(root, run, target_environment=environment)


def base_summary():
    if "base_summary" not in _CACHE:
        root, run = base_run()
        _CACHE["base_summary"] = summarize(root, run)
    return _CACHE["base_summary"]


def ctx():
    if "ctx" not in _CACHE:
        root, _ = base_run()
        _CACHE["ctx"] = rd().load(root)
    return _CACHE["ctx"]


def one_arm(test, name, spec=None, cpu=0):
    """Write one synthetic arm and read it back with the reader (small arms: fast)."""
    root, _ = base_run()
    folder = scratch(test, "reg1_block_arm_") / name
    rc = synth().write_arm(root, name, folder, cpu, spec)
    row = dict(arm=name, cpu=cpu, physical_core=[0, cpu], threads=1, rc=rc, killed=False, attempts=1)
    record = rd().read_arm(ctx(), name, folder, row, {0: [0, 0], 1: [0, 1]}, CONTAINER_ENV)
    return record, folder


def rewrite_trace(folder, transform):
    """Rewrite trace.csv through `transform(lines) -> lines` and rebind result/receipt hashes to it."""
    folder = Path(folder)
    lines = (folder / "trace.csv").read_bytes().decode("ascii").splitlines(keepends=True)
    raw = "".join(transform(lines)).encode("ascii")
    (folder / "trace.csv").write_bytes(raw)
    result = json.loads((folder / "result.json").read_bytes())
    result["trace_sha256"] = sha(raw)
    (folder / "result.json").write_bytes((json.dumps(result, indent=2, sort_keys=True) + "\n").encode("ascii"))
    receipt = json.loads((folder / "receipt.json").read_bytes())
    receipt.update(trace_sha256=sha(raw), result_sha256=sha((folder / "result.json").read_bytes()))
    (folder / "receipt.json").write_bytes((json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode("ascii"))


class BuildTests(unittest.TestCase):
    def test_package_holds_pinned_files_and_block(self):
        files = test_files()
        driver_sources = bb().literal_assignment(read_repo(qu().DRIVER), "SOURCES")
        self.assertEqual(len(driver_sources), 7)
        for relative, digest in {**qu().PINS, **driver_sources}.items():
            self.assertEqual(sha(files[relative]), digest, relative)
            self.assertEqual(files[relative], read_repo(relative))
        for name in ("run.sh", "reg1_queue.py", "reg1_reader.py"):
            self.assertEqual(files[name], (HERE / name).read_bytes())
        self.assertNotIn("fake_worker.py", files)
        self.assertNotIn("synth_runs.py", files)
        self.assertEqual(files["RELEASE"], (FAKE_PIN + "\n").encode())
        rest = {k: v for k, v in files.items() if k != "SOURCE_SHA256SUMS"}
        self.assertEqual(files["SOURCE_SHA256SUMS"], bb().manifest(rest))
        lines = files["SOURCE_SHA256SUMS"].decode().splitlines()
        self.assertEqual([line.split("  ", 1)[1] for line in lines], sorted(rest))

    def test_pins_cover_registration_driver_rule_and_reused_coordinate(self):
        pins = qu().PINS
        for relative in (qu().DRIVER, qu().REGISTRATION, qu().FORCE_RULE, qu().RULE_JSON, qu().DOUBLING, qu().COORDINATE):
            self.assertIn(relative, pins)
            self.assertEqual(sha(read_repo(relative)), pins[relative], relative)
        self.assertEqual(pins[qu().FORCE_RULE], "145b5fe6f456e8b66c2a8cc422ff88648c82d07c4420482f06bc6da7a5b1b6db")
        self.assertEqual(pins[qu().RULE_JSON], "1736322b4b2f4cef384becd97099998668137c19272e504edd951b698502a8f4")
        self.assertEqual(pins[qu().DOUBLING], "9d664ed38a70295b9bd04ecbf5dae4ffda663c5efbc348c30a77bf6b99fa1bda")

    def test_txt_round_trip_is_byte_identical(self):
        files = test_files()
        package = bb().package(files)
        self.assertEqual(package, bb().package(files), "deterministic package")
        txt = bb().operator(package, FAKE_PIN)
        decoded, embedded, pin = bb().decode_operator(txt)
        self.assertEqual((decoded, embedded, pin), (package, sha(package), FAKE_PIN))
        with tarfile.open(fileobj=io.BytesIO(decoded), mode="r:gz") as archive:
            members = {m.name: archive.extractfile(m).read() for m in archive if m.isfile()}
        self.assertEqual(members, files)
        self.assertRegex(bb().txt_name(FAKE_PIN), r"^PASTE_SUYOUNG_CONTACT_MINI_0123456789ab_1125\.txt$")

    def test_build_refuses_a_changed_pinned_file(self):
        def tampered(relative):
            data = read_repo(relative)
            return data + b"\n" if relative.endswith("material_floor.py") else data
        with self.assertRaises(ValueError):
            bb().collect(tampered, FAKE_PIN)
        def tampered_rule(relative):
            data = read_repo(relative)
            return data.replace(b"20", b"21", 1) if relative.endswith("force_rule.py") else data
        with self.assertRaises(ValueError):
            bb().collect(tampered_rule, FAKE_PIN)

    def test_one_character_closes_the_gate(self):
        top = scratch(self)
        txt = write_txt(test_files(), top / "txt")
        home, _ = make_home(top)
        intact = run_txt(txt, home, "CHECK_ONLY")
        self.assertIn("source.tar.gz: OK", intact.stdout)
        self.assertIn("RELEASE=" + FAKE_PIN, intact.stdout)
        raw = txt.read_bytes()
        start = raw.index(b"<<'CONTACT_MINI_SOURCES'\n") + len(b"<<'CONTACT_MINI_SOURCES'\n") + 200
        flipped = bytearray(raw)
        flipped[start] = ord("A") if raw[start] != ord("A") else ord("B")
        bad = top / "bad" / txt.name
        bad.parent.mkdir()
        bad.write_bytes(bytes(flipped))
        shutil.copy(str(txt) + ".sha256", str(bad) + ".sha256")
        check = subprocess.run(["sha256sum", "--strict", "-c", bad.name + ".sha256"], cwd=bad.parent,
                               capture_output=True, text=True)
        self.assertNotEqual(check.returncode, 0)
        refused = run_txt(bad, home, "CHECK_ONLY")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("FAILED", refused.stdout + refused.stderr)
        self.assertNotIn("RELEASE=", refused.stdout)
        pin_changed = top / "pin" / txt.name
        pin_changed.parent.mkdir()
        pin_changed.write_bytes(raw.replace(f"== '{FAKE_PIN}'".encode(), f"== '{'f' * 40}'".encode()))
        refused_pin = run_txt(pin_changed, home, "CHECK_ONLY")
        self.assertNotEqual(refused_pin.returncode, 0)
        self.assertNotIn("RELEASE=", refused_pin.stdout)
        self.assertFalse(any(p.name.startswith("suyoung_contact_mini") for p in home.iterdir()))

    def test_packaged_file_change_closes_the_manifest_gate(self):
        top = scratch(self)
        root = write_tree(test_files(), top / "pkg")
        home, log = make_home(top)
        data = bytearray((root / qu().FORCE_RULE).read_bytes())
        data[100] ^= 1
        (root / qu().FORCE_RULE).write_bytes(bytes(data))
        env = {"HOME": str(home), "PATH": os.environ["PATH"]}
        result = subprocess.run(["bash", "run.sh", "CHECK_ONLY"], cwd=root, env=env, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(log.exists(), "no Python started after a manifest failure")

    def test_mode_is_required(self):
        top = scratch(self)
        txt = write_txt(test_files(), top / "txt")
        home, log = make_home(top)
        for args in ((), ("GO",), ("CHECK_ONLY", "extra"), ("READBACK",)):
            result = run_txt(txt, home, *args)
            self.assertEqual(result.returncode, 2, args)
        self.assertFalse(log.exists())

    @unittest.skipUnless(subprocess.run(["git", "-C", str(REPO), "cat-file", "-e", "HEAD:" + BLOCK_REL + "reg1_reader.py"],
                                        capture_output=True).returncode == 0, "block not committed at HEAD")
    def test_git_build_reads_the_pinned_commit(self):
        out = scratch(self)
        built = bb().build(REPO, "HEAD", out)
        head = subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "HEAD"]).decode().strip()
        self.assertEqual(built["pin"], head)
        txt = out / built["name"]
        decoded, embedded, pin = bb().decode_operator(txt.read_bytes())
        self.assertEqual(pin, head)
        self.assertEqual(sha(txt.read_bytes()), built["txt_sha256"])
        check = subprocess.run(["sha256sum", "--strict", "-c", built["name"] + ".sha256"], cwd=out, capture_output=True)
        self.assertEqual(check.returncode, 0)


class EnvironmentGateTests(unittest.TestCase):
    def test_shipped_target_equals_driver_and_registration(self):
        driver = qu().load_pinned(REPO, qu().DRIVER)
        self.assertEqual(qu().TARGET_ENVIRONMENT, SHIPPED_ENV)
        self.assertEqual(tuple(driver.WSL_ENVIRONMENT), SHIPPED_ENV)
        self.assertIn("Python 3.12.3 · NumPy 2.5.2", REG1.read_text("utf-8"))

    def test_shipped_block_stops_at_the_environment_gate_here(self):
        if CONTAINER_ENV == SHIPPED_ENV:
            self.skipTest("this machine has the WSL environment")
        top = scratch(self)
        txt = write_txt(test_files(), top / "txt")
        home, log = make_home(top)
        result = run_txt(txt, home, "CHECK_ONLY")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("ENVIRONMENT_MISMATCH", result.stdout)
        self.assertIn("target=3.12.3/2.5.2", result.stdout)
        self.assertNotIn("CHECK_ONLY_OK", result.stdout)
        self.assertNotIn("PLAN ", result.stdout)
        self.assertEqual(len(log.read_text().splitlines()), 1)


class CheckOnlyTests(unittest.TestCase):
    """CHECK_ONLY on the test path (environment constant = this container, worker = fake worker)."""

    @classmethod
    def setUpClass(cls):
        cls.top = lasting("reg1_block_check_")
        cls.txt = write_txt(test_files(environment=CONTAINER_ENV, worker=True), cls.top / "txt")
        cls.home, cls.log = make_home(cls.top)
        cls.before = sorted(p.name for p in cls.home.iterdir())
        cls.result = run_txt(cls.txt, cls.home, "CHECK_ONLY")

    def test_check_only_passes_with_plan_seeds_and_reader_self_check(self):
        out = self.result.stdout
        self.assertEqual(self.result.returncode, 0, out + self.result.stderr)
        # The driver's own sub-check also prints CHECK_ONLY_OK mid-way; the block's last line is distinct.
        self.assertEqual(out.strip().splitlines()[-1], "CONTACT_MINI_CHECK_ONLY_OK")
        for text in ("CHECK_ONLY_OK", "MPM_STEPS 0", "PLAN_MATCHES_REGISTRATION reg1 50/50", "READER_SELFCHECK_OK",
                     "ENVIRONMENT_OK", "CORES ", "SEED G1 cells=48 points_per_disk=7213 outline=256",
                     "SEED G2 cells=48 points_per_disk=7213 outline=512", "QUEUE_TOTAL arms=50"):
            self.assertIn(text, out)
        queue = [line.split()[2].split("=")[1] for line in out.splitlines() if line.startswith("QUEUE order=")]
        driver, engine = synth().load_driver(REPO)
        expected = [a.name for a in sorted(driver.reg1_arms(), key=lambda a: (-engine.plan(a)["est_high_s"], a.name))]
        self.assertEqual(queue, expected)
        self.assertEqual(queue[:2], ["R1-G2-S-E-V4-48", "R1-G2-S-P-V4-48"])
        self.assertEqual(len(queue), 50)

    def test_check_only_runs_no_arm(self):
        calls = self.log.read_text().splitlines()
        self.assertTrue(calls)
        self.assertFalse([c for c in calls if " RUN " in f" {c} " or " go " in f" {c} "], calls)
        self.assertFalse((self.home / "fake_worker_calls.log").exists())
        after = sorted(p.name for p in self.home.iterdir())
        self.assertEqual(after, self.before, "no reservation, work or return folder")


class QueueTests(unittest.TestCase):
    def test_queue_follows_the_driver_plan_longest_first(self):
        driver, engine = synth().load_driver(REPO)
        jobs = qu().queue_plan(driver, engine)
        self.assertEqual(len(jobs), 50)
        arms = {a.name: a for a in driver.reg1_arms()}
        self.assertEqual({j["arm"] for j in jobs}, set(arms))
        keys = [(-j["est_high_s"], j["arm"]) for j in jobs]
        self.assertEqual(keys, sorted(keys))
        for j in jobs:
            plan = engine.plan(arms[j["arm"]])
            self.assertEqual((j["limit_s"], j["steps"], j["est_high_s"]), (plan["limit_s"], plan["steps"], plan["est_high_s"]))
        self.assertEqual(jobs[0]["limit_s"], 5640)
        self.assertEqual(qu().GRACE_S, 30)
        import inspect
        self.assertEqual(inspect.signature(qu().run_queue).parameters["grace_s"].default, 30)

    def worker(self, folder, sleep, rc):
        script = folder / "worker.py"
        script.write_text(
            "import json,os,sys,time\n"
            "arm=sys.argv[1]\n"
            "folder=sys.argv[2]\n"
            "open(os.path.join(folder,'starts.log'),'a').write(arm+'\\n')\n"
            "open(os.path.join(folder,arm+'.aff'),'w').write(json.dumps(sorted(os.sched_getaffinity(0))))\n"
            f"time.sleep({sleep!r}.get(arm, .2))\n"
            f"sys.exit({rc!r}.get(arm, 0))\n")
        return script

    def run_jobs(self, jobs, sleep=None, rc=None, grace=.5):
        top = scratch(self)
        script = self.worker(top, sleep or {}, rc or {})
        run = top / "run"
        run.mkdir()
        def command(arm, cpu):
            return ["taskset", "-c", str(cpu), sys.executable, "-I", str(script), arm, str(top)]
        coord = qu().load_pinned(REPO, qu().COORDINATE)
        cpus = coord.choose_cores({c: coord.topology(c) for c in os.sched_getaffinity(0)})
        cpus = (cpus["S"], cpus["F"])
        cores = {c: list(coord.topology(c)) for c in cpus}
        with contextlib.redirect_stdout(io.StringIO()):
            execution = qu().run_queue(jobs, cpus, cores, command, run, grace_s=grace, poll_s=.05)
        self.assertEqual(json.loads((run / "execution.json").read_bytes()), json.loads(json.dumps(execution)))
        starts = (top / "starts.log").read_text().split()
        return execution, starts, top, cpus

    @unittest.skipUnless(hasattr(os, "sched_getaffinity") and len(os.sched_getaffinity(0)) >= 2, "two CPUs")
    def test_each_arm_once_on_two_cores_and_a_failure_does_not_stop_the_rest(self):
        jobs = [dict(arm=f"A{i}", limit_s=30) for i in range(6)]
        execution, starts, top, cpus = self.run_jobs(jobs, sleep={"A0": .6, "A1": .6}, rc={"A2": 4})
        self.assertTrue(execution["complete"])
        self.assertEqual(execution["retries"], 0)
        self.assertEqual(collections.Counter(starts), collections.Counter(f"A{i}" for i in range(6)))
        rows = execution["arms"]
        self.assertEqual(sorted(rows, key=lambda a: rows[a]["started_ns"]), [j["arm"] for j in jobs])
        self.assertEqual({a: r["rc"] for a, r in rows.items()}, {"A0": 0, "A1": 0, "A2": 4, "A3": 0, "A4": 0, "A5": 0})
        self.assertEqual({r["attempts"] for r in rows.values()}, {1})
        self.assertEqual({r["cpu"] for r in rows.values()}, set(cpus))
        for a, r in rows.items():
            self.assertEqual(json.loads((top / (a + ".aff")).read_text()), [r["cpu"]])
            self.assertEqual(r["threads"], 1)
            self.assertFalse(r["killed"])
        a0, a1 = rows["A0"], rows["A1"]
        self.assertLess(max(a0["started_ns"], a1["started_ns"]), min(a0["ended_ns"], a1["ended_ns"]), "parallel")
        self.assertEqual(execution["queue_order"], [j["arm"] for j in jobs])

    @unittest.skipUnless(hasattr(os, "sched_getaffinity") and len(os.sched_getaffinity(0)) >= 2, "two CPUs")
    def test_limit_plus_grace_kills_and_the_queue_goes_on(self):
        jobs = [dict(arm="SLOW", limit_s=.3), dict(arm="FAST", limit_s=30), dict(arm="NEXT", limit_s=30)]
        begin = time.monotonic()
        execution, starts, _, _ = self.run_jobs(jobs, sleep={"SLOW": 60.}, grace=.3)
        self.assertLess(time.monotonic() - begin, 20)
        rows = execution["arms"]
        self.assertEqual((rows["SLOW"]["rc"], rows["SLOW"]["killed"]), (124, True))
        self.assertEqual((rows["FAST"]["rc"], rows["NEXT"]["rc"]), (0, 0))
        self.assertEqual(collections.Counter(starts), collections.Counter(["SLOW", "FAST", "NEXT"]))
        self.assertGreaterEqual(rows["SLOW"]["elapsed_including_wrapper_s"], .6)

    def test_a_closed_screen_does_not_lose_the_execution_record(self):
        # Added after the first implementation (reproduced before the fix): if the screen pipe
        # closes (terminal gone), the queue still finishes and execution.json is still written.
        run = scratch(self) / "run"
        run.mkdir()

        class Closed(io.TextIOBase):
            def write(self, text):
                raise BrokenPipeError("screen closed")
        with contextlib.redirect_stdout(Closed()):
            execution = qu().run_queue([dict(arm="A", limit_s=30), dict(arm="B", limit_s=30)], (0, 1),
                                       {0: [0, 0], 1: [0, 1]}, lambda a, c: [sys.executable, "-c", "pass"], run,
                                       poll_s=.05)
        self.assertTrue(execution["complete"])
        self.assertEqual(set(json.loads((run / "execution.json").read_bytes())["arms"]), {"A", "B"})

    def test_same_physical_core_is_refused(self):
        run = scratch(self) / "run"
        run.mkdir()
        with self.assertRaises(ValueError):
            qu().run_queue([dict(arm="A", limit_s=1)], (0, 1), {0: [0, 0], 1: [0, 0]}, lambda a, c: ["true"], run)

    def test_reused_core_choice(self):
        coord = qu().load_pinned(REPO, qu().COORDINATE)
        self.assertEqual(coord.choose_cores({2: (0, 1), 3: (0, 1), 7: (0, 4)}), {"S": 2, "F": 7})
        with self.assertRaises(ValueError):
            coord.choose_cores({2: (0, 1), 3: (0, 1)})


class UnpackTests(unittest.TestCase):
    def make_return(self, last=b"COMMAND_RC=0", extra=None):
        top = scratch(self)
        work = top / "work"
        run = work / "run"
        run.mkdir(parents=True)
        (run / "a.txt").write_bytes(b"alpha")
        (run / "screen.txt").write_bytes(b"line\n" + last + b"\n")
        subprocess.run("find . -type f ! -path './SHA256SUMS' -printf '%P\\0' | LC_ALL=C sort -z | xargs -0 sha256sum > SHA256SUMS",
                       shell=True, cwd=run, check=True)
        ret = top / "ret"
        ret.mkdir()
        shutil.copy(run / "screen.txt", ret / "screen.txt")
        with tarfile.open(ret / qu().RESULT_TAR, "w:gz") as archive:
            archive.add(run, arcname="run")
            if extra:
                info = tarfile.TarInfo(extra)
                info.size = 1
                archive.addfile(info, io.BytesIO(b"x"))
        subprocess.run(["bash", "-c", f"sha256sum {qu().RESULT_TAR} screen.txt > SHA256SUMS"], cwd=ret, check=True)
        return top, ret

    def unpack(self, ret, top):
        temp = top / "unpacked"
        temp.mkdir()
        return qu().unpack_return(REPO, ret, temp)

    def test_good_return(self):
        top, ret = self.make_return()
        run, tar_sha, screen_sha = self.unpack(ret, top)
        self.assertEqual((run / "a.txt").read_bytes(), b"alpha")
        self.assertEqual(tar_sha, sha((ret / qu().RESULT_TAR).read_bytes()))
        self.assertEqual(screen_sha, sha((ret / "screen.txt").read_bytes()))

    def test_bad_returns(self):
        top, ret = self.make_return(last=b"COMMAND_RC=4")
        with self.assertRaises(ValueError):
            self.unpack(ret, top)
        top, ret = self.make_return(extra="elsewhere/file")
        with self.assertRaises(ValueError):
            self.unpack(ret, top)
        top, ret = self.make_return()
        data = bytearray((ret / qu().RESULT_TAR).read_bytes())
        data[-10] ^= 1
        (ret / qu().RESULT_TAR).write_bytes(bytes(data))
        with self.assertRaises(ValueError):
            self.unpack(ret, top)
        top, ret = self.make_return()
        (ret / "screen.txt").write_bytes(b"other\nCOMMAND_RC=0\n")
        subprocess.run(["bash", "-c", f"sha256sum {qu().RESULT_TAR} screen.txt > SHA256SUMS"], cwd=ret, check=True)
        with self.assertRaises(ValueError):
            self.unpack(ret, top)


class ReaderRuleTests(unittest.TestCase):
    def rec(self, curve, forces=None, usable=True, name="X"):
        return dict(name=name, usable=usable, curve=curve, forces=forces or [(s, s) for _, s in curve],
                    trace_sha256="0" * 64, reasons=[] if usable else ["TEST"])

    def test_j1_pair_is_the_u6c_force_rule(self):
        force = ctx().force
        rng = np.random.default_rng(7)
        for _ in range(5):
            a = np.concatenate(([0.], np.cumsum(rng.uniform(.1, 1., 40))))
            b = np.concatenate(([0.], np.cumsum(rng.uniform(.1, 1., 60))))
            coarse = [(float(u), float(abs(v))) for u, v in zip(a, rng.normal(1, .3, len(a)))]
            fine = [(float(u), float(abs(v))) for u, v in zip(b, rng.normal(1, .3, len(b)))]
            got = rd().j1_pair(ctx(), self.rec(coarse, name="C"), self.rec(fine, name="F"))
            expected = force.compare(coarse, fine)
            self.assertEqual({k: got[k] for k in expected}, expected)
            self.assertEqual((got["coarse_arm"], got["fine_arm"]), ("C", "F"))

    def test_j1_exact_five_percent_boundary(self):
        fine = self.rec([(0., 0.), (1., 20.), (2., 1000.)])
        within = rd().j1_pair(ctx(), self.rec([(0., 0.), (1., 21.)]), fine)
        above = rd().j1_pair(ctx(), self.rec([(0., 0.), (1., 21.01)]), fine)
        self.assertEqual((within["comparison"], within["fine_peak_MPa"], within["union_knots"]), ("WITHIN", 20., 2))
        self.assertEqual(above["comparison"], "EXCEEDS")
        self.assertEqual(above["first_exceedance_u"], 1.)

    def test_j1_hold_for_held_arm_zero_reference_nan_and_missing(self):
        good = self.rec([(0., 0.), (1., 1.)])
        held = rd().j1_pair(ctx(), self.rec([(0., 0.), (1., 1.)], usable=False), good)
        self.assertEqual((held["comparison"], held["reason"]), ("HOLD", "ARM_HELD"))
        zero = rd().j1_pair(ctx(), self.rec([(0., 0.), (1., 0.)]), self.rec([(0., 0.), (1., 0.)]))
        self.assertEqual((zero["comparison"], zero["reason"]), ("HOLD", "ZERO_REFERENCE"))
        nan = rd().j1_pair(ctx(), self.rec([(0., 0.), (1., math.nan)]), good)
        self.assertEqual(nan["comparison"], "HOLD")
        empty = rd().j1_pair(ctx(), self.rec([]), good)
        self.assertEqual(empty["comparison"], "HOLD")

    def test_j1_verdict_uses_only_judged_pairs_with_force_rule_combination(self):
        W, E, H = ({"comparison": c} for c in ("WITHIN", "EXCEEDS", "HOLD"))
        # (16_32, 24_48, 8_16, 32_48): the two report pairs never judge.
        cases = [((W, W, E, E), "CONVERGED"), ((W, E, W, W), "EXCEEDS"), ((E, W, W, W), "EXCEEDS"),
                 ((E, H, W, W), "EXCEEDS"), ((W, H, W, W), "HOLD"), ((H, W, E, W), "HOLD")]
        for (j1632, j2448, r816, r3248), expected in cases:
            pairs = {"8_16": r816, "16_32": j1632, "24_48": j2448, "32_48": r3248}
            self.assertEqual(rd().j1_verdict(ctx(), pairs), expected)
        self.assertEqual(rd().J1_JUDGED, ((16, 32), (24, 48)))
        self.assertEqual(rd().J1_REPORTED, ((8, 16), (32, 48)))

    def test_j2_exact_boundary_and_zero(self):
        rec = self.rec([(0., 0.), (1., 20.)], forces=[(0., 0.), (21., 20.)])
        self.assertIs(rd().j2(ctx(), rec)["quasi_static"], True)
        rec = self.rec([(0., 0.), (1., 20.)], forces=[(0., 0.), (21.000001, 20.)])
        self.assertIs(rd().j2(ctx(), rec)["quasi_static"], False)
        rec = self.rec([(0., 0.), (1., 0.)], forces=[(0., 0.), (1., 0.)])
        self.assertEqual((rd().j2(ctx(), rec)["status"], rd().j2(ctx(), rec)["quasi_static"]), ("HOLD", None))
        held = rd().j2(ctx(), self.rec([(0., 0.), (1., 1.)], usable=False))
        self.assertEqual((held["status"], held["quasi_static"]), ("HOLD", None))

    def test_j3_maps_u_to_half_and_judges_32_and_48(self):
        g1 = self.rec([(0., 0.), (1., 1.), (2., 3.)])
        g2 = self.rec([(0., 0.), (2., 1.), (4., 3.)])
        cell = rd().j3_cell(ctx(), g2, g1, True, True)
        self.assertEqual((cell["comparison"], cell["max_abs_difference_MPa"]), ("WITHIN", 0.))
        W = dict(comparison="WITHIN", hold_kind=None)
        E = dict(comparison="EXCEEDS", hold_kind=None)
        J = dict(comparison="HOLD", hold_kind="J2")
        T = dict(comparison="HOLD", hold_kind="TECHNICAL")
        def cells(**kw):
            base = {str(n): W for n in (8, 16, 24, 32, 48)}
            base.update({k[1:]: v for k, v in kw.items()})
            return base
        self.assertEqual(rd().j3_verdict(ctx(), cells(c24=E)), ("MATCH", None))
        self.assertEqual(rd().j3_verdict(ctx(), cells(c32=E)), ("MISMATCH", None))
        self.assertEqual(rd().j3_verdict(ctx(), cells(c32=J)), ("HOLD", "J2"))
        self.assertEqual(rd().j3_verdict(ctx(), cells(c32=J, c48=T)), ("HOLD", "TECHNICAL"))
        self.assertEqual(rd().j3_verdict(ctx(), cells(c32=E, c48=J)), ("MISMATCH", None))
        held = rd().j3_cell(ctx(), g2, g1, False, True)
        self.assertEqual((held["comparison"], held["hold_kind"]), ("HOLD", "J2"))
        tech = rd().j3_cell(ctx(), self.rec(g2["curve"], usable=False), g1, True, True)
        self.assertEqual((tech["comparison"], tech["hold_kind"]), ("HOLD", "TECHNICAL"))
        self.assertEqual(rd().J3_CELLS, (32, 48))

    def test_first_force_is_strictly_above_the_noise_floor(self):
        rows = [(0., 0.), (1e-6, .008), (2e-6, .0081), (3e-6, .02)]
        first = rd().first_force(rows, .008, 5e-7, .1)
        self.assertEqual((first["u_on"], first["u_on_minus_u_geo"]), (2e-6, 2e-6 - 5e-7))
        self.assertIsNone(rd().first_force(rows[:2], .008, 5e-7, .1)["u_on"])

    def test_hinge_recovers_an_exact_bilinear_curve(self):
        x = np.linspace(0., .2, 401)
        y = np.where(x <= .08, 5. * x, .4 + .7 * (x - .08))
        fit = rd().hinge(x.tolist(), y.tolist())
        self.assertAlmostEqual(fit["knee_eps"], .08, places=12)
        self.assertAlmostEqual(fit["knee_MPa"], .4, places=9)
        self.assertAlmostEqual(fit["pre_knee_slope_MPa"], 5., places=6)
        self.assertAlmostEqual(fit["post_knee_slope_MPa"], .7, places=6)
        self.assertIsNone(rd().hinge([0., 1., 2.], [0., 1., 2.]))


class DecisionTests(unittest.TestCase):
    SERIES = ("G1-PLATE-P-V0", "G1-PLATE-P-V4", "G1-PLATE-E-V4", "G2-S-P-V0", "G2-F2-P-V0", "G2-S-P-V4",
              "G2-S-E-V4", "G2-F2-P-V4", "G2-F2-E-V4", "G2-F1-P-V4")

    def verdicts(self, **kw):
        j1 = {s: "CONVERGED" for s in self.SERIES}
        j3 = {k: dict(verdict="MATCH", hold_kind=None) for k in ("S-P", "F2-P", "S-E", "F2-E", "F1-P")}
        for key, value in kw.items():
            if key.startswith("j3_"):
                name = key[3:].replace("_", "-")
                j3[name] = dict(verdict=value[0], hold_kind=value[1])
            else:
                j1[key.replace("_", "-")] = value
        return j1, j3

    def decide(self, **kw):
        return rd().decide(*self.verdicts(**kw))

    def test_series_names(self):
        self.assertEqual(tuple(rd().SERIES), self.SERIES)

    def test_each_code(self):
        cases = [
            ({}, "MINI_TWO_BODY_CONVERGED"),
            ({"G1_PLATE_P_V4": "EXCEEDS"}, "MINI_PLATE_NOT_CONVERGED"),
            ({"G1_PLATE_P_V0": "EXCEEDS"}, "MINI_SPEED_BRANCH_PLATE"),
            ({"j3_S_P": ("HOLD", "J2"), "j3_F2_P": ("HOLD", "J2")}, "MINI_IDENTITY_HELD"),
            ({"j3_S_P": ("MISMATCH", None), "j3_F2_P": ("MISMATCH", None)}, "MINI_CONVERGED_OFF_IDENTITY"),
            ({"G2_S_P_V0": "EXCEEDS", "G2_F2_P_V0": "EXCEEDS"}, "MINI_SPEED_BRANCH_CONTACT"),
            ({"G2_S_P_V4": "EXCEEDS", "G2_F2_P_V4": "EXCEEDS"}, "MINI_INTERPARTICLE_NOT_CONVERGED"),
            ({"G1_PLATE_P_V4": "HOLD"}, "MINI_HELD"),
        ]
        for kw, code in cases:
            self.assertEqual(self.decide(**kw)["decision"], code, kw)

    def test_precedence_and_three_valued_rows(self):
        both = self.decide(G1_PLATE_P_V0="EXCEEDS", G2_S_P_V0="EXCEEDS")
        self.assertEqual(both["decision"], "MINI_SPEED_BRANCH_PLATE")
        four_five = self.decide(j3_S_P=("HOLD", "J2"), j3_F2_P=("MISMATCH", None))
        self.assertEqual(four_five["decision"], "MINI_IDENTITY_HELD")
        one_good = self.decide(j3_S_P=("MISMATCH", None))
        self.assertEqual(one_good["decision"], "MINI_TWO_BODY_CONVERGED")
        technical = self.decide(j3_S_P=("HOLD", "TECHNICAL"), j3_F2_P=("HOLD", "TECHNICAL"))
        self.assertEqual(technical["decision"], "MINI_HELD")
        held_v0 = self.decide(G1_PLATE_P_V0="HOLD", G2_S_P_V4="EXCEEDS", G2_F2_P_V4="EXCEEDS")
        self.assertEqual(held_v0["decision"], "MINI_INTERPARTICLE_NOT_CONVERGED")
        unknown = self.decide(G1_PLATE_P_V4="HOLD")
        self.assertEqual(unknown["decision"], "MINI_HELD")
        self.assertEqual(unknown["undetermined_rows_before_decision"], [1, 3])
        values = {r["row"]: r["value"] for r in unknown["rows"]}
        self.assertEqual(values, {1: None, 2: False, 3: None, 4: False, 5: False, 6: False, 7: False})
        unknown = self.decide(G1_PLATE_P_V4="HOLD", j3_S_P=("HOLD", "TECHNICAL"), j3_F2_P=("HOLD", "TECHNICAL"))
        self.assertEqual(unknown["undetermined_rows_before_decision"], [1, 3, 4, 5])
        only_s = self.decide(G2_S_P_V4="EXCEEDS")
        self.assertEqual(only_s["decision"], "MINI_TWO_BODY_CONVERGED")
        plate_v4_hold = self.decide(G1_PLATE_P_V4="HOLD", G2_S_P_V4="CONVERGED", G2_S_P_V0="EXCEEDS")
        self.assertEqual(plate_v4_hold["decision"], "MINI_SPEED_BRANCH_CONTACT")

    def test_gap_flag(self):
        flagged = self.decide(G2_S_P_V4="EXCEEDS", G2_F2_P_V4="EXCEEDS")
        self.assertEqual(flagged["flags"], ["MINI_GAP_CORRECTION_HURTS"])
        self.assertEqual(self.decide(G2_F2_P_V4="EXCEEDS", G2_F1_P_V4="EXCEEDS")["flags"], [])
        self.assertEqual(self.decide(G2_F2_P_V4="EXCEEDS", G2_F1_P_V4="HOLD")["flags"], [])
        self.assertEqual(self.decide()["flags"], [])


class ReaderArmTests(unittest.TestCase):
    def test_clean_small_arm(self):
        rec, _ = one_arm(self, "R1-G2-S-P-V0-08")
        self.assertTrue(rec["usable"], rec["reasons"])
        self.assertEqual(rec["monitors"]["max_abs_upper_dx_over_D"], 0.)
        self.assertEqual(len(rec["curve"]), 909)

    def test_nonfinite_is_held(self):
        rec, _ = one_arm(self, "R1-G2-S-P-V0-08", synth().Spec(nan_at=100))
        self.assertFalse(rec["usable"])
        self.assertIn("NONFINITE", rec["reasons"])

    def test_nonfinite_displacement_does_not_break_the_summary(self):
        # Added after the first implementation (reproduced before the fix): a held arm's report
        # fields must stay JSON-safe when its first-force sample has a non-finite displacement.
        rec, folder = one_arm(self, "R1-G1-PLATE-P-V0-08")
        step = rec["first_force"]["step_on"]

        def poison(lines):
            cells = lines[step + 1].split(",")
            cells[6] = "nan"
            lines[step + 1] = ",".join(cells)
            return lines
        rewrite_trace(folder, poison)
        row = dict(arm=rec["name"], cpu=0, physical_core=[0, 0], threads=1, rc=0, killed=False, attempts=1)
        again = rd().read_arm(ctx(), rec["name"], folder, row, {0: [0, 0], 1: [0, 1]}, CONTAINER_ENV)
        self.assertFalse(again["usable"])
        self.assertIn("NONFINITE", again["reasons"])
        self.assertIsNone(again["first_force"])
        json.dumps(rd().canonical({k: again[k] for k in ("first_force", "monitors", "reasons")}), allow_nan=False)
        self.assertEqual(rd().canonical({"a": math.nan, "b": [math.inf, 1.5]}), {"a": None, "b": [None, 1.5]})

    def test_missing_column_is_held(self):
        rec, folder = one_arm(self, "R1-G2-S-P-V0-08")
        def drop(lines):
            out = []
            for line in lines:
                cells = line.rstrip("\r\n").split(",")
                del cells[11]
                out.append(",".join(cells) + "\r\n")
            return out
        rewrite_trace(folder, drop)
        row = dict(arm=rec["name"], cpu=0, physical_core=[0, 0], threads=1, rc=0, killed=False, attempts=1)
        again = rd().read_arm(ctx(), rec["name"], folder, row, {0: [0, 0], 1: [0, 1]}, CONTAINER_ENV)
        self.assertFalse(again["usable"])
        self.assertIn("TRACE_FORMAT", again["reasons"])

    def test_empty_incomplete_and_time_limited_arms_are_held(self):
        for spec, reason in ((synth().Spec(empty=True), "MISSING_FILES"),
                             (synth().Spec(status="INCOMPLETE"), "RC_4"),
                             (synth().Spec(status="TIME_LIMIT"), "RC_3")):
            rec, _ = one_arm(self, "R1-G1-PLATE-P-V0-08", spec)
            self.assertFalse(rec["usable"], spec)
            self.assertIn(reason, rec["reasons"])
            self.assertEqual(rec["block_errors"], [])

    def test_lateral_offset_holds_two_disks_only(self):
        rec, _ = one_arm(self, "R1-G2-S-P-V0-08", synth().Spec(lateral_D=.011))
        self.assertFalse(rec["usable"])
        self.assertIn("LATERAL_OFFSET", rec["reasons"])
        rec, _ = one_arm(self, "R1-G2-S-P-V0-08", synth().Spec(lateral_D=.009))
        self.assertTrue(rec["usable"], rec["reasons"])
        rec, _ = one_arm(self, "R1-G1-PLATE-P-V0-08", synth().Spec(lateral_D=.02))
        self.assertTrue(rec["usable"], rec["reasons"])
        self.assertGreater(rec["monitors"]["max_abs_upper_dx_over_D"], .019)
        self.assertFalse(rec["monitors"]["lateral_watch_applies"])

    def test_side_wall_and_penetration_are_held(self):
        rec, _ = one_arm(self, "R1-G1-PLATE-P-V0-08", synth().Spec(side_hits_at=40))
        self.assertIn("SIDE_WALL_CONTACT", rec["reasons"])
        rec, _ = one_arm(self, "R1-G1-PLATE-P-V0-08", synth().Spec(penetration=3e-12))
        self.assertIn("FLOOR_PENETRATION", rec["reasons"])
        rec, _ = one_arm(self, "R1-G1-PLATE-P-V0-08", synth().Spec(penetration=2e-12))
        self.assertTrue(rec["usable"], rec["reasons"])

    def test_record_mismatches_are_held(self):
        rec, folder = one_arm(self, "R1-G1-PLATE-P-V0-08")
        raw = bytearray((folder / "trace.csv").read_bytes())
        raw[-5] = ord("7") if raw[-5] != ord("7") else ord("8")
        (folder / "trace.csv").write_bytes(bytes(raw))
        row = dict(arm=rec["name"], cpu=0, physical_core=[0, 0], threads=1, rc=0, killed=False, attempts=1)
        again = rd().read_arm(ctx(), rec["name"], folder, row, {0: [0, 0], 1: [0, 1]}, CONTAINER_ENV)
        self.assertFalse(again["usable"])
        self.assertIn("TRACE_SHA", again["reasons"])
        rec, folder = one_arm(self, "R1-G1-PLATE-P-V0-08")
        def shift(lines):
            cells = lines[5].split(",")
            cells[2] = repr(float(cells[2]) + 1e-9)
            lines[5] = ",".join(cells)
            return lines
        rewrite_trace(folder, shift)
        again = rd().read_arm(ctx(), rec["name"], folder, row, {0: [0, 0], 1: [0, 1]}, CONTAINER_ENV)
        self.assertFalse(again["usable"])
        self.assertIn("SCHEDULE", again["reasons"])

    def test_block_errors_from_one_arm(self):
        rec, _ = one_arm(self, "R1-G1-PLATE-P-V0-08", synth().Spec(tamper_sources=True))
        self.assertTrue(any(e.startswith("SOURCE_IDENTITY") for e in rec["block_errors"]))
        rec, _ = one_arm(self, "R1-G1-PLATE-P-V0-08", synth().Spec(affinity=[0, 1]))
        self.assertTrue(any(e.startswith("CORE_ASSIGNMENT") for e in rec["block_errors"]))
        rec, _ = one_arm(self, "R1-G1-PLATE-P-V0-08", synth().Spec(status="INCOMPLETE", rc=2))
        self.assertTrue(any(e.startswith("WORKER_RC_2") for e in rec["block_errors"]))

    def test_j4_and_j5_on_small_arms(self):
        rec, _ = one_arm(self, "R1-G1-PLATE-E-V4-08")
        j2 = rd().j2(ctx(), rec)
        j4 = rd().j4(ctx(), rec, j2)
        self.assertEqual([p["category"] for p in j4["points"]], ["WITHIN_20_PERCENT"] * 3)
        self.assertEqual([p["eps"] for p in j4["points"]], [.01, .02, .04])
        for p in j4["points"]:
            self.assertAlmostEqual(p["rho"], 1., places=6)
        rec, _ = one_arm(self, "R1-G1-PLATE-E-V4-08", synth().Spec(scale=1.3))
        j4 = rd().j4(ctx(), rec, rd().j2(ctx(), rec))
        self.assertEqual([p["category"] for p in j4["points"]], ["OUTSIDE_20_PERCENT"] * 3)
        rec, _ = one_arm(self, "R1-G1-PLATE-P-V4-08")
        j5 = rd().j5(ctx(), rec, rd().j2(ctx(), rec))
        # 8 cells: the invented knee falls between samples, so the hinge sits within one sample of it.
        self.assertAlmostEqual(j5["sigma_b"]["knee_MPa"], .40, delta=.003)
        self.assertAlmostEqual(j5["sigma_b"]["post_knee_slope_MPa"], .7, delta=.03)
        self.assertAlmostEqual(j5["compression_positive_sigma_yy_avg"]["knee_MPa"], .36, delta=.003)
        rec, _ = one_arm(self, "R1-G1-PLATE-P-V4-08", synth().Spec(top_scale=1.2))
        self.assertEqual(rd().j5(ctx(), rec, rd().j2(ctx(), rec))["status"], "HOLD")


class ReaderSummaryTests(unittest.TestCase):
    def test_base_run_two_body_converged_and_summary_fields(self):
        s = base_summary()
        self.assertEqual(s["decision"], "MINI_TWO_BODY_CONVERGED")
        self.assertEqual(s["flags"], [])
        for key, value in (("label", "DEVELOPMENT_ONLY"), ("after_result_amendment", True), ("stage3_go", False),
                           ("three_dimensional_go", False), ("solver_calls_during_read", 0)):
            self.assertEqual(s[key], value, key)
        self.assertEqual(s["block_errors"], [])
        self.assertEqual(set(s["J1"]), set(rd().SERIES))
        for series, entry in s["J1"].items():
            self.assertEqual(entry["verdict"], "CONVERGED", series)
            self.assertEqual(set(entry["pairs"]), {"8_16", "16_32", "24_48", "32_48"})
            pair = entry["pairs"]["24_48"]
            for field in ("common_end_u", "union_knots", "max_abs_difference_MPa", "fine_peak_MPa", "ratio",
                          "first_exceedance_u", "comparison", "coarse_arm", "fine_arm", "judged"):
                self.assertIn(field, pair)
            self.assertTrue(pair["judged"])
            self.assertFalse(entry["pairs"]["8_16"]["judged"])
            self.assertLess(pair["ratio"], 1e-3)
        self.assertEqual({k: v["verdict"] for k, v in s["J3"].items()},
                         {"S-P": "MATCH", "F2-P": "MATCH", "S-E": "MATCH", "F2-E": "MATCH", "F1-P": "MATCH"})
        self.assertEqual(len(s["J2"]), 50)
        self.assertTrue(all(v["quasi_static"] is True for v in s["J2"].values()))
        self.assertEqual(sorted(s["J4"]), [f"R1-G1-PLATE-E-V4-{n:02d}" for n in (8, 16, 24, 32, 48)])
        for entry in s["J4"].values():
            self.assertEqual([p["category"] for p in entry["points"]], ["WITHIN_20_PERCENT"] * 3)
        self.assertEqual(sorted(s["J5"]["arms"]), [f"R1-G1-PLATE-P-V4-{n:02d}" for n in (8, 16, 24, 32, 48)])
        knee = s["J5"]["arms"]["R1-G1-PLATE-P-V4-48"]["sigma_b"]
        self.assertAlmostEqual(knee["knee_MPa"], .4, places=3)
        self.assertEqual(s["J5"]["nz22_reference"]["post_knee_slope_MPa"], .7)
        self.assertEqual(len(s["first_force"]), 50)
        self.assertEqual(len(s["monitors"]), 50)
        self.assertEqual(len(s["trace_sha256"]), 50)
        self.assertEqual({v["usable"] for v in s["arms"].values()}, {True})
        self.assertEqual(s["contacts"]["S"]["converging_contact"], True)
        rows = {r["row"]: r["value"] for r in s["decision_rows"]}
        self.assertEqual(rows[3], True)
        text = json.dumps(s, sort_keys=True, allow_nan=False)
        for pattern in (r"/home/", r"/tmp/", r"/root/"):
            self.assertIsNone(re.search(pattern, text), pattern)

    def test_scenario_row7_with_gap_flag(self):
        root, run = scenario_run(self, {"R1-G2-S-P-V4-48": synth().Spec(scale=1.2),
                                        "R1-G2-F2-P-V4-48": synth().Spec(scale=1.2)})
        s = summarize(root, run)
        self.assertEqual(s["decision"], "MINI_INTERPARTICLE_NOT_CONVERGED")
        self.assertEqual(s["flags"], ["MINI_GAP_CORRECTION_HURTS"])
        pair = s["J1"]["G2-S-P-V4"]["pairs"]["24_48"]
        self.assertEqual(pair["comparison"], "EXCEEDS")
        self.assertAlmostEqual(pair["ratio"], .2 / 1.2, places=4)
        self.assertEqual(s["J1"]["G2-S-P-V4"]["pairs"]["16_32"]["comparison"], "WITHIN")
        self.assertEqual(s["J3"]["S-P"]["verdict"], "MISMATCH")

    def test_scenario_row4_identity_held_by_j2(self):
        root, run = scenario_run(self, {"R1-G1-PLATE-P-V4-32": synth().Spec(top_scale=1.1)})
        s = summarize(root, run)
        self.assertEqual(s["decision"], "MINI_IDENTITY_HELD")
        self.assertIs(s["J2"]["R1-G1-PLATE-P-V4-32"]["quasi_static"], False)
        self.assertAlmostEqual(s["J2"]["R1-G1-PLATE-P-V4-32"]["Q"], .1, places=9)
        self.assertEqual((s["J3"]["S-P"]["verdict"], s["J3"]["S-P"]["hold_kind"]), ("HOLD", "J2"))
        self.assertEqual(s["J1"]["G1-PLATE-P-V4"]["verdict"], "CONVERGED")
        self.assertEqual(s["undetermined_rows_before_decision"], [3])

    def test_scenario_row9_time_limited_arm(self):
        root, run = scenario_run(self, {"R1-G1-PLATE-P-V4-48": synth().Spec(status="TIME_LIMIT")})
        s = summarize(root, run)
        self.assertEqual(s["decision"], "MINI_HELD")
        self.assertEqual(s["J1"]["G1-PLATE-P-V4"]["pairs"]["24_48"]["comparison"], "HOLD")
        self.assertEqual(s["J1"]["G1-PLATE-P-V4"]["verdict"], "HOLD")
        self.assertFalse(s["arms"]["R1-G1-PLATE-P-V4-48"]["usable"])
        self.assertEqual(s["block_errors"], [])

    def test_technical_incomplete_cases(self):
        root, base = base_run()
        cases = {
            "missing arm": dict(omit=("R1-G2-F1-P-V4-16",)),
            "same core": dict(cores={0: [0, 0], 1: [0, 0]}),
            "retry": dict(retries=1),
            "sources": dict(specs={"R1-G1-PLATE-P-V0-08": synth().Spec(tamper_sources=True)}),
            "worker rc 2": dict(specs={"R1-G1-PLATE-P-V0-08": synth().Spec(status="INCOMPLETE", rc=2)}),
        }
        for label, kw in cases.items():
            run = scratch(self, "reg1_block_tech_") / "run"
            synth().write_run(root, run, base=base, **kw)
            s = summarize(root, run)
            self.assertEqual(s["decision"], "TECHNICAL_INCOMPLETE", label)
            self.assertTrue(s["block_errors"], label)
            self.assertIsNone(s["J1"], label)
        run = scratch(self, "reg1_block_tech_") / "run"
        synth().write_run(root, run, base=base)
        (run / "RELEASE").write_bytes(b"f" * 40 + b"\n")
        s = summarize(root, run)
        self.assertEqual(s["decision"], "TECHNICAL_INCOMPLETE")
        self.assertIn("RUN_RELEASE_DIFFERS", s["block_errors"])
        s = summarize(*base_run(), environment=SHIPPED_ENV)
        if CONTAINER_ENV != SHIPPED_ENV:
            self.assertEqual(s["decision"], "TECHNICAL_INCOMPLETE")
            self.assertTrue(any(e.startswith("ENVIRONMENT_IDENTITY") for e in s["block_errors"]))

    def test_summary_cli_and_replay(self):
        root, base = base_run()
        run = scratch(self, "reg1_block_cli_") / "run"
        synth().write_run(root, run, base=base)
        rd().write_summary(root, run, target_environment=CONTAINER_ENV)
        self.assertEqual(json.loads((run / "summary.json").read_bytes()), json.loads(json.dumps(base_summary())))
        self.assertEqual(rd().replay_summary(root, run, target_environment=CONTAINER_ENV)["decision"],
                         "MINI_TWO_BODY_CONVERGED")
        changed = json.loads((run / "summary.json").read_bytes())
        changed["decision"] = "MINI_HELD"
        (run / "summary.json").write_text(json.dumps(changed, indent=2, sort_keys=True) + "\n")
        with self.assertRaises(ValueError):
            rd().replay_summary(root, run, target_environment=CONTAINER_ENV)

    def test_reader_never_runs_the_solver(self):
        c = rd().load(base_run()[0])
        with self.assertRaises(RuntimeError):
            c.driver.run_arm()
        with self.assertRaises(RuntimeError):
            c.driver.ArmRunner()
        self.assertEqual(c.solver_calls["count"], 2)


class EndToEndTests(unittest.TestCase):
    """GO -> ALREADY_RESERVED -> READBACK on the test path with the fake worker (invented numbers)."""

    @classmethod
    def setUpClass(cls):
        cls.top = lasting("reg1_block_e2e_")
        cls.failed = "R1-G2-F1-P-V4-08"
        files = test_files(environment=CONTAINER_ENV, worker=True, scenario={cls.failed: {"status": "INCOMPLETE"}})
        cls.txt = write_txt(files, cls.top / "txt")
        cls.home, cls.log = make_home(cls.top)
        cls.go = run_txt(cls.txt, cls.home, "GO_SUYOUNG_CONTACT_MINI_ONCE")
        found = re.findall(r"^RETURN_DIRECTORY=(.*)$", cls.go.stdout, re.M)
        cls.ret = Path(found[-1]) if found else None

    def archive(self, member):
        with tarfile.open(self.ret / "suyoung_contact_mini_result.tar.gz", "r:gz") as archive:
            return archive.extractfile(member).read()

    def test_go_runs_every_arm_once_and_returns_a_bundle(self):
        self.assertEqual(self.go.returncode, 0, self.go.stdout[-3000:] + self.go.stderr[-3000:])
        self.assertEqual(sorted(p.name for p in self.ret.iterdir()),
                         ["SHA256SUMS", "screen.txt", "suyoung_contact_mini_result.tar.gz"])
        execution = json.loads(self.archive("run/execution.json"))
        rows = execution["arms"]
        self.assertEqual(len(rows), 50)
        self.assertTrue(execution["complete"])
        self.assertEqual(execution["retries"], 0)
        self.assertEqual(rows[self.failed]["rc"], 4)
        self.assertEqual({a for a, r in rows.items() if r["rc"] != 0}, {self.failed})
        self.assertEqual({r["attempts"] for r in rows.values()}, {1})
        self.assertEqual(len(set(execution["cpus"])), 2)
        self.assertEqual(len({tuple(v) for v in execution["physical_cores"].values()}), 2)
        calls = collections.Counter((self.home / "fake_worker_calls.log").read_text().split())
        self.assertEqual(set(calls), set(rows))
        self.assertEqual(set(calls.values()), {1})
        driver, engine = synth().load_driver(REPO)
        expected = [a.name for a in sorted(driver.reg1_arms(), key=lambda a: (-engine.plan(a)["est_high_s"], a.name))]
        self.assertEqual(execution["queue_order"], expected)
        by_cpu = collections.defaultdict(list)
        for r in rows.values():
            by_cpu[r["cpu"]].append((r["started_ns"], r["ended_ns"]))
        a, b = by_cpu.values()
        self.assertTrue(any(max(x[0], y[0]) < min(x[1], y[1]) for x in a for y in b), "two cores at once")
        summary = json.loads(self.archive("run/summary.json"))
        self.assertEqual(summary["decision"], "MINI_TWO_BODY_CONVERGED")
        self.assertFalse(summary["arms"][self.failed]["usable"])
        screen = self.archive("run/screen.txt").decode()
        self.assertTrue(screen.rstrip().endswith("COMMAND_RC=0"))
        self.assertIn("AUTOMATIC_RETRIES=0", screen)

    def test_second_go_is_already_reserved(self):
        before = sorted(p.name for p in self.home.iterdir())
        again = run_txt(self.txt, self.home, "GO_SUYOUNG_CONTACT_MINI_ONCE")
        self.assertEqual(again.returncode, 2)
        self.assertIn("ALREADY_RESERVED", again.stdout)
        self.assertEqual(sorted(p.name for p in self.home.iterdir()), before)

    def test_readback_from_a_relative_path_reproduces_the_summary(self):
        calls_before = (self.home / "fake_worker_calls.log").read_text()
        relative = os.path.relpath(self.ret, self.home)
        result = run_txt(self.txt, self.home, "READBACK", relative, cwd=self.home)
        self.assertEqual(result.returncode, 0, result.stdout[-3000:] + result.stderr[-3000:])
        self.assertIn("READBACK_COMPLETE", result.stdout)
        self.assertIn("DECISION MINI_TWO_BODY_CONVERGED", result.stdout)
        receipt_path = Path(re.findall(r"RETURN_RECEIPT=(\S+)", result.stdout)[-1])
        receipt = json.loads(receipt_path.read_bytes())
        for key, value in (("scope", "DEVELOPMENT_ONLY"), ("mode", "READBACK"), ("readback_rc", 0),
                           ("solver_runs_during_readback", 0), ("retries", 0), ("timeouts", 0),
                           ("release", FAKE_PIN)):
            self.assertEqual(receipt[key], value, key)
        self.assertEqual(receipt["return_tar_sha256"], sha((self.ret / "suyoung_contact_mini_result.tar.gz").read_bytes()))
        self.assertEqual(receipt["screen_sha256"], sha((self.ret / "screen.txt").read_bytes()))
        self.assertEqual(len(receipt["arms"]), 50)
        failed = receipt["arms"][self.failed]
        self.assertEqual((failed["rc"], failed["status"]), (4, "INCOMPLETE"))
        good = receipt["arms"]["R1-G2-S-P-V4-48"]
        for field in ("cpu", "physical_core", "threads", "rc", "steps", "status", "native_elapsed_s", "started_ns",
                      "ended_ns", "elapsed_including_wrapper_s"):
            self.assertIn(field, good)
        self.assertEqual((good["steps"], good["status"]), (21775, "COMPLETE"))
        self.assertEqual((self.home / "fake_worker_calls.log").read_text(), calls_before, "no arm during readback")
        text = json.dumps(receipt)
        self.assertIsNone(re.search(r"/home/|/tmp/|/root/", text))

    def repack(self, edit):
        """Copy the return with `edit(run_folder)` applied inside the TAR, every hash rebuilt."""
        top = Path(tempfile.mkdtemp(prefix="reg1_block_repack_"))
        self.addCleanup(shutil.rmtree, top, True)
        work = top / "work"
        work.mkdir()
        with tarfile.open(self.ret / "suyoung_contact_mini_result.tar.gz", "r:gz") as archive:
            archive.extractall(work, filter="data")
        edit(work / "run")
        subprocess.run("find . -type f ! -path './SHA256SUMS' -printf '%P\\0' | LC_ALL=C sort -z | xargs -0 sha256sum > SHA256SUMS",
                       shell=True, cwd=work / "run", check=True)
        ret = top / "ret"
        ret.mkdir()
        subprocess.run(["tar", "-czf", str(ret / "suyoung_contact_mini_result.tar.gz"), "-C", str(work), "run"], check=True)
        shutil.copy(work / "run" / "screen.txt", ret / "screen.txt")
        subprocess.run("sha256sum suyoung_contact_mini_result.tar.gz screen.txt > SHA256SUMS", shell=True, cwd=ret, check=True)
        return ret

    def test_readback_refuses_an_altered_summary(self):
        def edit(run):
            summary = json.loads((run / "summary.json").read_bytes())
            summary["decision"] = "MINI_HELD"
            (run / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
        ret = self.repack(edit)
        result = run_txt(self.txt, self.home, "READBACK", str(ret))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ARCHIVED_SUMMARY_MISMATCH", result.stdout + result.stderr)

    def test_readback_refuses_an_altered_trace(self):
        def edit(run):
            path = run / "arms" / "R1-G2-S-P-V0-08" / "trace.csv"
            raw = bytearray(path.read_bytes())
            raw[-5] = ord("7") if raw[-5] != ord("7") else ord("8")
            path.write_bytes(bytes(raw))
        ret = self.repack(edit)
        result = run_txt(self.txt, self.home, "READBACK", str(ret))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ARCHIVED_SUMMARY_MISMATCH", result.stdout + result.stderr)

    def test_readback_refuses_a_changed_archive_byte(self):
        top = Path(tempfile.mkdtemp(prefix="reg1_block_bytes_"))
        self.addCleanup(shutil.rmtree, top, True)
        ret = top / "ret"
        shutil.copytree(self.ret, ret)
        data = bytearray((ret / "suyoung_contact_mini_result.tar.gz").read_bytes())
        data[len(data) // 2] ^= 1
        (ret / "suyoung_contact_mini_result.tar.gz").write_bytes(bytes(data))
        result = run_txt(self.txt, self.home, "READBACK", str(ret))
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("READBACK_COMPLETE", result.stdout)


class PrivacyTests(unittest.TestCase):
    PATTERNS = (r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                r"/home/", r"/root/", r"/Users/", r"/mnt/", r"[A-Za-z]:\\\\", r"DESKTOP-", r"\bssh\b", r"-p \d{2,5}\b")

    def scan(self, name, text):
        for pattern in self.PATTERNS:
            self.assertIsNone(re.search(pattern, text), f"{name}: {pattern}")
        for match in re.finditer(r"(?i)yonghoon", text):
            self.assertEqual(text[match.start():match.start() + 16], "Yonghoon-DEM-DFT", name)

    def test_block_files_and_built_txt_have_no_private_strings(self):
        for name in ("run.sh", "reg1_queue.py", "reg1_reader.py", "build_block.py", "README.md"):
            path = HERE / name
            if path.is_file():
                self.scan(name, path.read_text("utf-8"))
        files = test_files()
        for relative, data in files.items():
            self.scan(relative, data.decode("utf-8"))
        txt = bb().operator(bb().package(files), FAKE_PIN).decode("ascii")
        self.scan("txt", txt.split("<<'CONTACT_MINI_SOURCES'")[0] + txt.split("\nCONTACT_MINI_SOURCES\n")[1])


if __name__ == "__main__":
    unittest.main()
