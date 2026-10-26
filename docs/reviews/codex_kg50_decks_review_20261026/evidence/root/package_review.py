from pathlib import Path
import json, hashlib, zipfile
root=Path("kg50_review_20261026").resolve()
intake=json.loads((root/"evidence/intake.json").read_text(encoding="utf-8-sig"))
mismatches=[]
for f in intake["files"]:
 p=root/"snapshot"/f["path"]
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=f["sha256"]:
  mismatches.append(f["path"])
assert not mismatches, mismatches
files=[p for p in root.rglob("*") if p.is_file() and p.name not in ("MANIFEST.sha256","PACKAGING.json","write_probe.txt") and "__pycache__" not in p.parts]
stat={"input_snapshot_files_verified":len(intake["files"]),"snapshot_mismatches":mismatches,"payload_files_excluding_manifest_and_packaging":len(files),"physical_simulation_runs":0,"production_edits":0,"git_mutations":0,"report":"codex_review_kg50_decks_20261026.md"}
(root/"PACKAGING.json").write_text(json.dumps(stat,indent=2)+"\n",encoding="utf-8")
files.append(root/"PACKAGING.json")
files.sort(key=lambda p:p.relative_to(root).as_posix())
lines=[hashlib.sha256(p.read_bytes()).hexdigest()+"  "+p.relative_to(root).as_posix() for p in files]
(root/"MANIFEST.sha256").write_text("\n".join(lines)+"\n",encoding="utf-8")
files.append(root/"MANIFEST.sha256")
out=root.parent/"codex_kg50_decks_review_20261026.zip"
with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in files:
  z.write(p,root.name+"/"+p.relative_to(root).as_posix())
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 for line in lines:
  h,n=line.split("  ",1)
  assert hashlib.sha256(z.read(root.name+"/"+n)).hexdigest()==h,n
res={**stat,"zip":str(out),"zip_bytes":out.stat().st_size,"zip_sha256":hashlib.sha256(out.read_bytes()).hexdigest(),"zip_files":len(files),"all_packaged_hashes_verified":True}
(root.parent/"codex_kg50_decks_review_20261026_receipt.json").write_text(json.dumps(res,indent=2)+"\n",encoding="utf-8")
print(json.dumps(res,indent=2))

