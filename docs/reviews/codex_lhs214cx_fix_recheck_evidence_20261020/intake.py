"""Retrieve a fixed review snapshot without Git mutation; verify all reused bytes."""
from pathlib import Path
import concurrent.futures
import hashlib
import json
import os
import shutil
import time
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent / "lhs214s_recheck_20261019"
REPO = "yonghoon7153-source/Yonghoon-DEM-DFT"
PIN = "34713ac9650ece7c8d59b7c4d9a2aefccee693ea"
BASE = "685c2bbdbbfee82898a9ec062bb9c2bc94612fc8"


def native(p):
    s = str(p.resolve())
    return Path("\\\\?\\" + s) if os.name == "nt" and not s.startswith("\\\\?\\") else Path(s)


def blob(b):
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()


def get(url):
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "read-only-scientific-review"})
            with urllib.request.urlopen(req, timeout=45) as r:
                return r.read()
        except Exception:
            if attempt == 3:
                raise
            time.sleep(attempt + 1)


for name in ("source", "evidence", "probes", "notes", "tmp", "submitted", "support"):
    (ROOT / name).mkdir(parents=True, exist_ok=True)
shutil.copyfile(
    "C:/Users/Administrator/Downloads/codex_lhs214cx_fix_recheck_request_20261019_send.md",
    ROOT / "submitted/codex_lhs214cx_fix_recheck_request_20261019_send.md")


def fetch_json(name, url):
    p = ROOT / "evidence" / name
    if not p.exists():
        p.write_bytes(get(url))
    return json.loads(p.read_text(encoding="utf8"))


commit = fetch_json("commit.json", f"https://api.github.com/repos/{REPO}/commits/{PIN}")
assert commit["sha"] == PIN
tree = fetch_json("tree.json", f"https://api.github.com/repos/{REPO}/git/trees/{PIN}?recursive=1")
assert not tree.get("truncated")
old_tree = json.loads((OLD / "evidence/tree.json").read_text(encoding="utf8"))
entries = {e["path"]: e for e in tree["tree"] if e["type"] == "blob"}
old_entries = {e["path"]: e for e in old_tree["tree"] if e["type"] == "blob"}
changed = sorted(p for p in entries if p not in old_entries or entries[p]["sha"] != old_entries[p]["sha"])
diff = dict(pin=PIN, base=BASE, changed=changed, deleted=sorted(set(old_entries) - set(entries)))
(ROOT / "evidence/tree_diff.json").write_text(json.dumps(diff, ensure_ascii=False, indent=2), encoding="utf8")
old_manifest = json.loads((OLD / "source_manifest.json").read_text(encoding="utf8"))
paths = {e["path"] for e in old_manifest["files"] if e["path"] in entries}
paths |= {p for p in entries if "lhs214cx" in p or p.endswith("AGENTS.md")}
paths |= {p for p in changed if p.startswith(("scripts/", "webapp/"))}
paths |= {p for p in changed if p.endswith(".md")}
caches = [ROOT / "source", OLD / "source", ROOT.parent / "rint_join_q7_recheck_20261020/source"]


def one(p):
    b = None
    reused = False
    for cache in caches:
        f = native(cache / p)
        if f.is_file():
            candidate = f.read_bytes()
            if blob(candidate) == entries[p]["sha"]:
                b = candidate
                reused = True
                break
    if b is None:
        b = get(f"https://raw.githubusercontent.com/{REPO}/{PIN}/" + urllib.parse.quote(p))
    assert blob(b) == entries[p]["sha"], p
    target = native(ROOT / "source" / p)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        assert target.read_bytes() == b, p
    else:
        target.write_bytes(b)
    return dict(path=p, bytes=len(b), sha256=hashlib.sha256(b).hexdigest(),
                git_blob=entries[p]["sha"], reused=reused)


print(json.dumps(dict(pin=PIN, changed_code=[p for p in changed if p.startswith(("scripts/", "webapp/"))],
                      files_requested=len(paths)), ensure_ascii=False), flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
    rows = list(pool.map(one, sorted(paths)))
(ROOT / "source_manifest.json").write_text(
    json.dumps(dict(pin=PIN, base=BASE, files=rows), ensure_ascii=False, indent=2), encoding="utf8")
print(json.dumps(dict(files=len(rows), bytes=sum(x["bytes"] for x in rows),
                      reused=sum(x["reused"] for x in rows))), flush=True)
