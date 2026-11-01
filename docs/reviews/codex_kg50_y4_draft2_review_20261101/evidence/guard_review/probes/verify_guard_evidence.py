"""Read-only Q4 evidence verification; no scheduler, shell, network, or DEM calls."""
from pathlib import Path
import hashlib
import json
import re

BASE = Path(__file__).resolve().parents[2]
SRC = BASE / "source"
REPO = SRC / "repo"
OUT = BASE / "guard_review" / "evidence"
G = REPO / "docs/50kg/d07_guard"
OUT.mkdir(parents=True, exist_ok=True)

def sha(b):
    return hashlib.sha256(b).hexdigest()

def read(p):
    return p.read_text(encoding="utf-8")

checks = []
def check(name, ok, details):
    checks.append({"name": name, "pass": bool(ok), "details": details})

raw = read(G / "t_test_20261031/attempts_and_identity.txt")
receipts = {}
for name, expected in [
    ("attempt_r56_1030_152123_2568313", "29ff619a666f29131a9d582f27e555590316e8516dcf9d0a7d2af01715bde6fa"),
    ("attempt_r56_1031_215830_2483798", "a22a9b9fa18782f1a02b5728c05272ef735f46fd3dba8f2441b0213b2b6a94c9"),
]:
    body = raw.split("== kg50_d07_b50/" + name + "\n", 1)[1]
    lines = body.splitlines()[:5]
    assert all(re.fullmatch(r"[0-9a-f]{64}  /\S+", line) for line in lines)
    b = ("\n".join(lines) + "\n").encode()
    actual = sha(b)
    receipts[name] = {"sha256": actual, "lines": lines, "evidence_type": "reconstructed from received transcript, not server file"}
    check("receipt " + name, actual == expected, {"actual": actual, "expected": expected})
    (OUT / (name + ".main_inputs.reconstructed.sha256")).write_bytes(b)

filled = read(G / "d07_guard_v2_1031.sh")
template = read(G / "d07_guard_v2.sh")
vals = dict(re.findall(r"^(INHERIT|OLDATT|OKR|OKL|OKD|OKK)=(\S+)$", filled, re.M))
r = receipts[vals["OLDATT"]]
check("filled receipt", vals["OKR"] == r["sha256"], vals["OKR"])
check("filled deck", vals["OKD"] == r["lines"][0].split()[0], vals["OKD"])
check("filled checkpoint", vals["OKK"] == r["lines"][4].split()[0], vals["OKK"])
last_identity = [x for x in raw.splitlines() if x.startswith("LMP_IDENTITY ")][-1]
id_hashes = re.findall(r"sha256=([0-9a-f]{64})", last_identity)
check("filled lmp from trial identity", vals["OKL"] == id_hashes[0], vals["OKL"])
check("checkpoint receipt = trial identity", vals["OKK"] == id_hashes[2], id_hashes[2])
check("trial deck receipt = trial identity", r["lines"][2].split()[0] == id_hashes[1], id_hashes[1])
changes = [i for i, (a, b) in enumerate(zip(template.splitlines(), filled.splitlines()), 1) if a != b]
check("template differences exactly approvals", changes == [16,17,18,19] and len(template.splitlines()) == len(filled.splitlines()), changes)

block = read(G / "d07_guard_v2_block.txt")
payload = block.split("<<'D07_GUARD_V2_EOF'\n",1)[1].split("D07_GUARD_V2_EOF\n",1)[0]
md5 = hashlib.md5(payload.encode()).hexdigest()
check("block payload byte equality LF", payload.encode() == (G / "d07_guard_v2_1031.sh").read_bytes(), {"payload_md5": md5})
check("block md5 gate", md5 == "35371e83472905553df3455a2267c501" and md5 in block, md5)
roundtrip = payload.replace("\n", "\r\n").replace("\r\n", "\n")
check("block CRLF normalization", roundtrip == filled, "text normalization only; installer Bash was not executed")

tool_path = REPO / "scripts/resume_ckpt.sh"
tool_hash = sha(tool_path.read_bytes())
check("resume_ckpt.sh full bytes", tool_hash == "2dc7f693263708d7788ab721386182c6109a8f9278797ecc43f5165d6715f1e8", tool_hash)
tool = read(tool_path)
check("decision written after main_job", tool.index('echo "$JM" > $AD/main_job.txt; echo "결정: 본 제출 job $JM"') > 0, "no result/main_job ordering race in the shown production branch")
check("compression mode rejects", '[ "$M" = compress ] && { rej "압축 체크포인트 (Q3)"' in tool, "resume_ckpt.sh:1898")

file_inventory = []
for p in sorted((G / "t_test_20261031").iterdir()):
    if p.is_file():
        file_inventory.append({"path": p.relative_to(REPO).as_posix(), "bytes": p.stat().st_size, "sha256": sha(p.read_bytes())})

for rel in ["docs/50kg/d07_guard/d07_guard_v2_1031.sh", "docs/50kg/d07_guard/t_test_20261031/report_resume_r56_1031_215830.md", "docs/50kg/d07_guard/t_test_20261031/attempts_and_identity.txt"]:
    p = REPO / rel
    (OUT / (p.name + ".numbered.txt")).write_text("\n".join(f"{i:4}: {line}" for i,line in enumerate(read(p).splitlines(),1)) + "\n", encoding="utf-8")

timing = []
for name, c in [("D1-shaped",2285000),("D2-shaped",3515000),("D3-shaped",4075000)]:
    n = 200000+c+100000
    timing.append({"scenario":name,"compression_steps":c,"remaining_steps":n,"hours_at_31570_steps_h":n/31570,"days_at_31570_steps_h":n/31570/24,"days_compression_cost_x1.07":(300000+1.07*c)/31570/24,"days_compression_cost_x1.19":(300000+1.19*c)/31570/24})

result={"pin":read(SRC/"PIN.txt").strip(),"checks":checks,"passed":sum(x["pass"] for x in checks),"total":len(checks),"approval_values":vals,"receipts":receipts,"received_T_inventory":file_inventory,"timing":timing,"limitations":["10-31 raw trial stdout, generated main/trial decks, runners, checkpoint binary and dem_restart.py are absent from this received T folder.","Hashes of those absent files are transcript consistency checks only, not independent file-byte hashes.","Bash guard simulation was not run by this script. No scheduler or DEM calls occur."]}
(OUT/"verification.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"passed":result["passed"],"total":result["total"],"timing":timing,"output":str(OUT/"verification.json")},ensure_ascii=False,indent=2))
assert result["passed"] == result["total"]
