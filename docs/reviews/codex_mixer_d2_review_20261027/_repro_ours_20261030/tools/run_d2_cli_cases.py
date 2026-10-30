"""Run the three D2 consumer CLIs on named case folders, exactly as the verdict's
commands do (readback --d2 DECK META; diff OLD NEW --allow D2 --meta-ref --meta-new;
smoke --d2-plan DECK --d2-meta META; no --json), and record rc + output.

Usage: python3 -I run_d2_cli_cases.py <scripts_dir> <cases_dir> <label> <out_dir>
"""
import hashlib
import json
import os
import subprocess
import sys

CASES = ["run_upto", "late_timestep", "insert_start_late", "front_period",
         "exclude_SE_SE", "crlf_lf_metadata", "crlf_crlf_metadata"]
# Extra controls (not named in the task, kept separate in the report).
CONTROLS = ["normal", "friction_missing", "negative_control_bad_gravity",
            "negative_control_remove_integrator"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main(S, C, label, out):
    os.makedirs(out, exist_ok=True)
    rep = {"label": label, "scripts_dir_sha256": {}, "python": sys.version.split()[0],
           "cases": {}, "controls": {}}
    for f in ("mixer_deck_readback.py", "mixer_deck_diff.py", "mixer_smoke_blind.py"):
        rep["scripts_dir_sha256"][f] = sha(os.path.join(S, f))
    for group, names in (("cases", CASES), ("controls", CONTROLS)):
        for name in names:
            d = os.path.join(C, name)
            cmds = {
                "readback": [os.path.join(S, "mixer_deck_readback.py"), "--d2",
                             os.path.join(d, "old.in"), os.path.join(d, "old.meta.json")],
                "pair": [os.path.join(S, "mixer_deck_diff.py"), os.path.join(d, "old.in"),
                         os.path.join(d, "new.in"), "--allow", "D2",
                         "--meta-ref", os.path.join(d, "old.meta.json"),
                         "--meta-new", os.path.join(d, "new.meta.json")],
                "plan": [os.path.join(S, "mixer_smoke_blind.py"), "--d2-plan",
                         os.path.join(d, "old.in"), "--d2-meta", os.path.join(d, "old.meta.json")],
            }
            r = {"inputs": {f: {"sha256": sha(os.path.join(d, f)),
                                "bytes": os.path.getsize(os.path.join(d, f))}
                            for f in ("old.in", "new.in", "old.meta.json", "new.meta.json")},
                 "rc": {}, "first_line": {}}
            for key, args in cmds.items():
                p = subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", *args],
                                   capture_output=True)
                logp = os.path.join(out, "%s__%s.log" % (name, key))
                with open(logp, "wb") as f:
                    f.write(p.stdout + p.stderr)
                r["rc"][key] = p.returncode
                txt = (p.stdout + p.stderr).decode("utf-8", "replace").strip().splitlines()
                r["first_line"][key] = txt[0][:200] if txt else ""
                r["traceback"] = r.get("traceback", False) or (b"Traceback" in p.stderr)
            rep[group][name] = r
    with open(os.path.join(out, "cli_rc_%s.json" % label), "w", encoding="utf-8") as f:
        json.dump(rep, f, ensure_ascii=False, indent=1)
    for group in ("cases", "controls"):
        for name, r in rep[group].items():
            print("%-9s %-36s readback=%d pair=%d plan=%d traceback=%s" % (
                group, name, r["rc"]["readback"], r["rc"]["pair"], r["rc"]["plan"], r["traceback"]))


if __name__ == "__main__":
    main(*sys.argv[1:5])
