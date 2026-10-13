"""Self-test of bms-balancing/scripts/reil_c4env_compare (stdlib, synthetic + committed seals only)."""
import base64, hashlib, importlib.util, json, sys, zipfile
from pathlib import Path
REPO = Path("/home/user/Yonghoon-DEM-DFT")
spec = importlib.util.spec_from_file_location("cmp", REPO / "bms-balancing/scripts/reil_c4_env_compare.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
W = Path(sys.argv[1])
fails = []
def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond: fails.append(msg)

# 1 artifacts: expected names from the P0 install log
names = m.log_wheel_names((REPO / "bms-balancing/evidence/reil_p0_20261006/01_venv_pip_install.stdout").read_text(encoding="utf-8"))
check(len(names) == 28 and all(n.endswith(".whl") for n in names), f"P0 log -> {len(names)} wheel names")
d = W / "wh"; d.mkdir()
for n in names: (d / n).write_bytes(b"x")
check(m.artifacts(d, names)["ok"], "artifacts: exact set ok")
(d / "extra-1.0-py3-none-any.whl").write_bytes(b"y")
r = m.artifacts(d, names); check(not r["ok"] and r["problems"][0]["extra"] == ["extra-1.0-py3-none-any.whl"], "artifacts: extra wheel caught")

# 1b artifacts by dist (test tool: old filenames unknown)
t = W / "wt"; t.mkdir()
for n in ["pytest-9.1.1-py3-none-any.whl", "Pygments-2.21.0-py3-none-any.whl", "pluggy-1.6.0-py3-none-any.whl", "iniconfig-2.3.0-py3-none-any.whl"]:
    (t / n).write_bytes(b"x")
want = ["pytest==9.1.1", "pluggy==1.6.0", "iniconfig==2.3.0", "pygments==2.21.0"]
check(m.artifacts(t, want, by="dist")["ok"], "artifacts by dist: case-insensitive name ok")
check(not m.artifacts(t, ["pytest==9.1.0"] + want[1:], by="dist")["ok"], "artifacts by dist: wrong version caught")
(t / "pluggy-1.6.0.tar.gz").write_bytes(b"s")
check(not m.artifacts(t, want, by="dist")["ok"], "artifacts by dist: sdist caught")

# 2 lock/PROFILE/MANIFEST on committed seals: 20261005 -> rebuild_20261006 (known: collision line keys + 4 RECORD sha)
o, n = REPO / "bms-balancing/reil_c6_20261005", REPO / "bms-balancing/reil_c6_rebuild_20261006"
ld = m.lock_diff((o / m.LOCK).read_bytes(), (n / m.LOCK).read_bytes(), "3.11.15")
kinds = sorted({l["kind"] for l in ld["lines"]})
check(ld["record_sha_differs"] == ["cffi", "fonttools", "numpy", "pip"], f"lock: record_sha_differs {ld['record_sha_differs']}")
check(not ld["allowed"] and "disallowed" in kinds and any(l["old"].startswith("#@ collision") for l in ld["lines"] if l["kind"] == "disallowed"),
      "lock: collision-line change is disallowed under the C4-ENV rule")
check((o / m.PROFILE).read_bytes() == (n / m.PROFILE).read_bytes(), "PROFILE identical between the two committed seals")
# synthetic python-line change: allowed only for the exact expected version
old_lock = (n / m.LOCK).read_bytes()
new_lock = old_lock.replace(b'#@ python "3.11.15"', b'#@ python "3.11.17"')
check(m.lock_diff(old_lock, new_lock, "3.11.17")["allowed"], "lock: python line 3.11.15->3.11.17 allowed")
check(not m.lock_diff(old_lock, new_lock, "3.11.18")["allowed"], "lock: python line with unexpected version disallowed")
check(not m.lock_diff(old_lock, old_lock.replace(b"numpy==2.4.6", b"numpy==2.4.7"), "3.11.15")["allowed"], "lock: version change disallowed")
check(not m.lock_diff(old_lock, old_lock.replace(b'"verified": 7187', b'"verified": 7186'), "3.11.15")["allowed"], "lock: files aggregate change disallowed")
# PROFILE: only version+build may change, byte-exact regeneration
po = json.loads((n / m.PROFILE).read_bytes())
pn = json.loads((n / m.PROFILE).read_bytes()); pn["python"]["version"] = "3.11.17"; pn["python"]["build"] = ["main", "Oct  1 2026 15:41:07"]
check(m.profile_diff((n / m.PROFILE).read_bytes(), m._dump(pn), "3.11.17", ["main", "Oct  1 2026 15:41:07"])["allowed"], "PROFILE: version+build change allowed")
pn2 = json.loads(m._dump(pn)); pn2["platform"]["libc"] = "glibc 2.40"
check(not m.profile_diff((n / m.PROFILE).read_bytes(), m._dump(pn2), "3.11.17", ["main", "Oct  1 2026 15:41:07"])["allowed"], "PROFILE: libc change disallowed")
pn3 = json.loads(m._dump(pn)); pn3["build_dependencies"]["numpy"]["blas"]["version"] = "0.3.32"
check(not m.profile_diff((n / m.PROFILE).read_bytes(), m._dump(pn3), "3.11.17", ["main", "Oct  1 2026 15:41:07"])["allowed"], "PROFILE: BLAS change disallowed")
check(not m.profile_diff((n / m.PROFILE).read_bytes(), m._dump(pn)[:-1] + b" \n", "3.11.17", ["main", "Oct  1 2026 15:41:07"])["allowed"], "PROFILE: formatting-only change disallowed")

# 3 RECORD rows on a synthetic venv + wheel
def h(b): return "sha256=" + base64.urlsafe_b64encode(hashlib.sha256(b).digest()).rstrip(b"=").decode()
def build(root, shebang_venv, tamper=None):
    venv = root / "venv"; site = venv / "lib/python3.11/site-packages"; (site / "foo").mkdir(parents=True); (venv / "bin").mkdir()
    init = b"x = 1\n"; meta = b"Metadata-Version: 2.1\nName: Foo_Bar\nVersion: 1.0\n\nName: not-this\n"
    di = site / "foo_bar-1.0.dist-info"; di.mkdir()
    (site / "foo/__init__.py").write_bytes(init); (di / "METADATA").write_bytes(meta); (di / "INSTALLER").write_bytes(b"pip\n")
    script = f"#!{shebang_venv}/bin/python\nimport foo\n".encode(); (venv / "bin/foo").write_bytes(script)
    wrec = f"foo/__init__.py,{h(init)},{len(init)}\nfoo_bar-1.0.dist-info/METADATA,{h(meta)},{len(meta)}\nfoo_bar-1.0.dist-info/RECORD,,\n"
    whl = root / "wheels"; whl.mkdir()
    with zipfile.ZipFile(whl / "foo_bar-1.0-py3-none-any.whl", "w") as z:
        z.writestr("foo/__init__.py", init); z.writestr("foo_bar-1.0.dist-info/METADATA", meta); z.writestr("foo_bar-1.0.dist-info/RECORD", wrec)
    rows = [f"foo/__init__.py,{h(init)},{len(init)}", f"foo_bar-1.0.dist-info/METADATA,{h(meta)},{len(meta)}",
            f"foo_bar-1.0.dist-info/INSTALLER,{h(b'pip' + chr(10).encode())},4", "foo/__pycache__/__init__.cpython-311.pyc,,",
            f"../../../bin/foo,{h(script)},{len(script)}", "foo_bar-1.0.dist-info/RECORD,,"]
    if tamper == "hash": rows[0] = f"foo/__init__.py,{h(b'other')},{len(init)}"
    if tamper == "extra": rows.append("foo_bar-1.0.dist-info/direct_url.json,sha256=abc,10")
    if tamper == "hashed_pyc": rows[3] = "foo/__pycache__/__init__.cpython-311.pyc,sha256=abc,5"
    (di / "RECORD").write_text("\r\n".join(rows) + "\r\n", encoding="utf-8", newline="")
    return venv, site, whl
for case, want_ok in [("clean", True), ("hash", False), ("extra", False), ("hashed_pyc", False), ("shebang", False)]:
    root = W / f"rec_{case}"; root.mkdir()
    venv, site, whl = build(root, "/elsewhere/venv" if case == "shebang" else str(root / "venv"), tamper=None if case in ("clean", "shebang") else case)
    res = m.record_rows(site, str(venv), [whl], root / "records")["foo-bar"]
    ok = not res["problems"]
    check(ok == want_ok and res["bin_rows"] == ["../../../bin/foo"] and (root / "records/foo-bar-1.0.RECORD").is_file(),
          f"record_rows[{case}] problems={res['problems'][:1]}")
    if case == "clean":
        txt = (site / "foo_bar-1.0.dist-info/RECORD").read_text(encoding="utf-8")
        check(res["record_text_sha256"] == hashlib.sha256(txt.encode()).hexdigest() != res["record_raw_sha256"], "record text sha = env_profile-style (CRLF normalized) and differs from raw")
print("FAILS", len(fails)); sys.exit(1 if fails else 0)
