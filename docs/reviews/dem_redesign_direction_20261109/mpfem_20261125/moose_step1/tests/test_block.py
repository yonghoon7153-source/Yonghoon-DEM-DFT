#!/usr/bin/env python3
"""Tests for the WSL paste block (written before ../build_block.py).

Runs the block with bash in a sandbox HOME that holds a fake conda.sh; `conda activate`
puts tests/fake_moose.py on PATH as moose-opt.  No MOOSE, no network.
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOP = os.path.dirname(HERE)
BUILDER = os.path.join(TOP, "build_block.py")
BLOCK = os.path.join(TOP, "moose_step1_block.txt")
FILES = ["step1_disk.i", "make_disk_msh.py", "check_step1.py", "run_step1.sh"]
REFUSAL = "아무것도 안 함"


def build(out):
    p = subprocess.run([sys.executable, BUILDER, "--out", out], capture_output=True, text=True)
    assert p.returncode == 0, p.stdout + p.stderr
    with open(out, encoding="utf-8") as f:
        return f.read()


def sandbox(root):
    home = os.path.join(root, "home")
    fake_bin = os.path.join(root, "bin")
    prof = os.path.join(home, "miniforge", "etc", "profile.d")
    os.makedirs(prof)
    os.makedirs(fake_bin)
    with open(os.path.join(prof, "conda.sh"), "w") as f:
        f.write('conda() { if [ "$1" = activate ]; then export PATH="$FAKE_BIN:$PATH"; fi; return 0; }\n')
    exe = os.path.join(fake_bin, "moose-opt")
    with open(exe, "w") as f:
        f.write('#!/bin/sh\nexec "%s" "%s" "$@"\n' % (sys.executable, os.path.join(HERE, "fake_moose.py")))
    os.chmod(exe, 0o755)
    return home, fake_bin


def run_block(root, text, mode="pass", extra_env=None):
    home, fake_bin = sandbox(root)
    path = os.path.join(root, "block.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    env = {"HOME": home, "PATH": os.environ["PATH"], "FAKE_BIN": fake_bin,
           "FAKE_MOOSE_MODE": mode, "FAKE_MOOSE_ARGLOG": os.path.join(root, "args.log"),
           "LANG": "C.UTF-8"}
    env.update(extra_env or {})
    p = subprocess.run(["bash", path], capture_output=True, text=True, env=env, cwd=root)
    return p.returncode, p.stdout + p.stderr, home


def runs(home):
    return sorted(p for p in glob.glob(os.path.join(home, "moose_step1", "run_*")) if os.path.isdir(p))


# ---------------------------------------------------------------- tests
def t_committed_block_is_current(root):
    text = build(os.path.join(root, "b.txt"))
    with open(BLOCK, encoding="utf-8") as f:
        assert f.read() == text, "moose_step1_block.txt is stale: rebuild with build_block.py"


def t_round_trip_and_full_flow(root):
    text = build(os.path.join(root, "b.txt"))
    rc, out, home = run_block(root, text)
    assert rc == 0, out
    for name in FILES:
        with open(os.path.join(TOP, name), "rb") as a, \
                open(os.path.join(home, "moose_step1", name), "rb") as b:
            assert a.read() == b.read(), "extracted %s differs" % name
    assert "gate OK" in out, out
    r = runs(home)
    assert len(r) == 1, r
    for sub in ("smoke_m13", "m13", "m26"):
        for fn in ("out.csv", "run.log", "rc.txt", "disk.msh", "disk.mesh.json", "step1_disk.i"):
            assert os.path.exists(os.path.join(r[0], sub, fn)), (sub, fn)
    with open(os.path.join(r[0], "check_step1.json"), encoding="utf-8") as f:
        data = json.load(f)
    assert data["all_pass"] is True, data
    assert re.search(r"ALL .*PASS", out), out
    assert os.path.exists(os.path.join(r[0], "inputs", "SHA256SUMS"))
    import tarfile
    with tarfile.open(os.path.join(r[0], "result_small.tgz")) as tf:
        names = tf.getnames()
    for want in ("check_step1.json", "run_info.txt", "m13/out.csv", "m26/run.log",
                 "smoke_m13/out.csv", "inputs/SHA256SUMS"):
        assert any(n.endswith(want) for n in names), (want, names)
    assert not any(n.endswith(".e") or n.endswith(".msh") for n in names), names
    with open(os.path.join(root, "args.log")) as f:
        calls = f.read()
    assert "Executioner/end_time=12" in calls, calls          # the smoke
    assert calls.count("-i step1_disk.i") == 3, calls          # smoke + m13 + m26


def t_one_flipped_character_closes_gate(root):
    text = build(os.path.join(root, "b.txt"))
    i = text.index("nu = 0.45")
    bad = text[:i] + "nu = 0.46" + text[i + len("nu = 0.45"):]
    rc, out, home = run_block(root, bad)
    assert REFUSAL in out, out
    assert runs(home) == [], runs(home)
    assert not os.path.exists(os.path.join(root, "args.log")), "runner must not start"


def t_flipped_character_in_checker_closes_gate(root):
    text = build(os.path.join(root, "b.txt"))
    i = text.index("1e-3")
    bad = text[:i] + "1e-2" + text[i + 4:]
    rc, out, home = run_block(root, bad)
    assert REFUSAL in out and runs(home) == [], out


def t_damaged_md5_line_closes_gate(root):
    text = build(os.path.join(root, "b.txt"))
    m = re.search(r"\b[0-9a-f]{32}\b", text.splitlines()[-1])
    assert m, "md5 not on the last line"
    h = m.group(0)
    bad = text.replace(h, ("0" if h[0] != "0" else "1") + h[1:])
    rc, out, home = run_block(root, bad)
    assert REFUSAL in out and runs(home) == [], out


def t_smoke_reject_stops(root):
    text = build(os.path.join(root, "b.txt"))
    rc, out, home = run_block(root, text, mode="reject")
    assert rc != 0, out
    assert "SMOKE FAIL" in out and "not a valid parameter" in out, out
    r = runs(home)
    assert len(r) == 1 and not os.path.exists(os.path.join(r[0], "m13")), r
    assert not os.path.exists(os.path.join(r[0], "m26"))


def t_full_run_divergence_is_c_fail(root):
    text = build(os.path.join(root, "b.txt"))
    rc, out, home = run_block(root, text, mode="diverge")
    assert rc != 0, out
    r = runs(home)
    with open(os.path.join(r[0], "check_step1.json"), encoding="utf-8") as f:
        data = json.load(f)
    assert data["all_pass"] is False
    for case in ("m13", "m26"):
        c = data["cases"][case]["checks"]
        assert c["C_all_converged"]["pass"] is False and c["C_reached_end"]["pass"] is False, c


def t_fix_dt_half_manual(root):
    text = build(os.path.join(root, "b.txt"))
    rc, out, home = run_block(root, text)
    assert rc == 0, out
    env = {"HOME": home, "PATH": os.environ["PATH"], "FAKE_BIN": os.path.join(root, "bin"),
           "FAKE_MOOSE_MODE": "pass", "FAKE_MOOSE_ARGLOG": os.path.join(root, "args2.log"),
           "FIX": "dt_half"}
    p = subprocess.run(["bash", os.path.join(home, "moose_step1", "run_step1.sh")],
                       capture_output=True, text=True, env=env, cwd=root)
    assert p.returncode == 0, p.stdout + p.stderr
    r = runs(home)
    assert len(r) == 2, r
    new = [x for x in r if "dt_half" in x]
    assert len(new) == 1, r
    with open(os.path.join(new[0], "check_step1.json"), encoding="utf-8") as f:
        data = json.load(f)
    assert data["all_pass"] is True and data["cases"]["m13"]["checks"]["C_all_converged"]["steps"] == 814
    with open(os.path.join(root, "args2.log")) as f:
        calls = f.read()
    assert calls.count("Executioner/dt=0.5") == 3, calls
    env["FIX"] = "bogus"
    p = subprocess.run(["bash", os.path.join(home, "moose_step1", "run_step1.sh")],
                       capture_output=True, text=True, env=env, cwd=root)
    assert p.returncode != 0 and "STOP" in p.stdout + p.stderr


def t_no_conda_stops(root):
    text = build(os.path.join(root, "b.txt"))
    home, fake_bin = sandbox(root)
    os.remove(os.path.join(home, "miniforge", "etc", "profile.d", "conda.sh"))
    path = os.path.join(root, "block.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    env = {"HOME": home, "PATH": os.environ["PATH"], "FAKE_BIN": fake_bin}
    p = subprocess.run(["bash", path], capture_output=True, text=True, env=env, cwd=root)
    assert p.returncode != 0 and "STOP" in p.stdout + p.stderr, p.stdout + p.stderr


def t_block_has_no_network_or_personal_strings(root):
    text = build(os.path.join(root, "b.txt"))
    low = text.lower()
    for bad in ("curl", "wget", "http://", "https://", "pip install", "apt-get", "apt install",
                "conda create", "conda install", "ssh ", "scp "):
        assert bad not in low, bad
    assert not re.search(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", text), "IPv4-like string"
    assert not re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text), "e-mail-like"
    assert "/home/" not in text and "/mnt/c/" not in text, "absolute user path"


def t_block_safe_for_interactive_paste(root):
    """No '!' history-expansion trigger and no TAB anywhere in the block (any bash version)."""
    text = build(os.path.join(root, "b.txt"))
    assert "\t" not in text, "TAB in block"
    hits = [l for l in text.splitlines() if re.search(r"!(?![ =(]|$)", l)]
    assert not hits, hits[:3]


def _skip(d, names):
    return [n for n in names if n in ("__pycache__", "tests")
            or (n.startswith("run_") and os.path.isdir(os.path.join(d, n)))]


def t_builder_refuses_hazards(root):
    clean = os.path.join(root, "clean")
    shutil.copytree(TOP, clean, ignore=_skip)
    r = subprocess.run([sys.executable, os.path.join(clean, "build_block.py"),
                        "--out", os.path.join(clean, "x.txt")], capture_output=True, text=True)
    assert r.returncode == 0, "unmodified copy must build: " + r.stdout + r.stderr
    for bad, word in (("# use !important here\n", "history"), ("x = 1\t# tab\n", "TAB")):
        dst = os.path.join(root, "copy_" + word)
        shutil.copytree(TOP, dst, ignore=_skip)
        p = os.path.join(dst, "check_step1.py")
        with open(p, encoding="ascii") as f:
            text = f.read()
        with open(p, "w", encoding="ascii") as f:
            f.write(bad + text)
        r = subprocess.run([sys.executable, os.path.join(dst, "build_block.py"),
                            "--out", os.path.join(dst, "x.txt")], capture_output=True, text=True)
        msg = r.stdout + r.stderr
        assert r.returncode != 0 and not os.path.exists(os.path.join(dst, "x.txt")), msg
        assert word in msg, msg


TESTS = [v for k, v in sorted(globals().items()) if k.startswith("t_")]


def main():
    npass = nfail = 0
    for t in TESTS:
        root = tempfile.mkdtemp(prefix="blk_")
        try:
            t(root)
            npass += 1
            print("PASS", t.__name__)
        except Exception as exc:
            nfail += 1
            print("FAIL", t.__name__, "-", type(exc).__name__, str(exc)[:400].replace("\n", " | "))
        finally:
            shutil.rmtree(root, ignore_errors=True)
    print("block tests: %d passed, %d failed, %d total" % (npass, nfail, npass + nfail))
    return 0 if nfail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
