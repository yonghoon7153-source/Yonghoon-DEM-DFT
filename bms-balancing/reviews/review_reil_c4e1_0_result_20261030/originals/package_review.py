"""Build and verify this review delivery only; no received program execution."""
from pathlib import Path,PurePosixPath
import json,hashlib,zipfile,zlib,stat
R=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(p):
    b=p.read_bytes()
    return {"bytes":len(b),"sha256":sha(b)}
def jload(p):return json.loads(p.read_text(encoding="utf-8"))
def write(name,data):
    with (R/name).open("x",encoding="utf-8",newline="\n") as f:f.write(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
capture=jload(R/"SOURCE_IDENTITIES.json")
post=[]
for row in capture["files"]:
    p=R/row["local"]
    current=ident(p)
    assert current["bytes"]==row["bytes"] and current["sha256"]==row["sha256"]
    post.append({"relative_path":row["local"],**current})
basis=jload(R/"BASIS_COPY_IDENTITIES.json")
assert len(basis["files"])==17
for row in basis["files"]:
    assert ident(R/row["relative_path"])=={"bytes":row["bytes"],"sha256":row["sha256"]}
attachment=R/"basis/USER_ATTACHMENT.md"
remote=R/"source/bms-balancing/docs/REIL_C4E1_0_RESULT_REVIEW_SEND_20261030.md"
same_bytes=attachment.read_bytes()==remote.read_bytes()
same_text=attachment.read_text(encoding="utf-8-sig")==remote.read_text(encoding="utf-8-sig")
assert same_text
write("ATTACHMENT_BINDING.json",{"source":"C:/Users/Administrator/Downloads/REIL_C4E1_0_RESULT_REVIEW_SEND_20261030.md",
"captured":"basis/USER_ATTACHMENT.md",**ident(attachment),"same_bytes_as_pinned_repository_request":same_bytes,
"same_decoded_text_universal_newline":same_text,"repository_request":str(remote.relative_to(R)).replace("\\","/")})
audit=jload(R/"STATIC_AUDIT.json")
assert audit["matched"]==audit["conditions"]==129
cases=jload(R/"CASE_RESULT_MAP.json")
assert cases["case_count"]==103 and cases["distinct_test_functions"]==65
decision=jload(R/"REVIEW_DECISION.json")
assert decision["q1"]["green_passed"]==65
assert decision["q2"]["full_approved_procedure_compliance"] is False
assert decision["q3"]["new_execution_authorized"] is False
archive=R/"REIL_C4E1_0_RESULT_REVIEW_20261030.zip"
excluded={archive.name,"PACKAGE_MANIFEST.json","DELIVERY_RECEIPT.json","FINAL_PACKAGE_TOOL_RETURN.json","SELECTED_CAPTURES_POST_PACKAGE.json"}
payloads=sorted(p for p in R.rglob("*") if p.is_file() and p.name not in excluded)
rows=[]
for p in payloads:
    assert not p.is_symlink()
    rel=p.relative_to(R).as_posix()
    assert not PurePosixPath(rel).is_absolute() and ".." not in PurePosixPath(rel).parts
    b=p.read_bytes()
    rows.append({"path":rel,"bytes":len(b),"sha256":sha(b),"crc32":f"{zlib.crc32(b)&0xffffffff:08x}"})
assert len({r["path"].casefold() for r in rows})==len(rows)
write("PACKAGE_MANIFEST.json",{"kind":"REVIEW_PACKAGE_MANIFEST","payload_count":len(rows),"files":rows,
"received_program_execution":0,"new_execution_approval":False})
with zipfile.ZipFile(archive,"x",compression=zipfile.ZIP_DEFLATED) as z:
    for p in payloads+[R/"PACKAGE_MANIFEST.json"]:
        z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(archive) as z:
    names=z.namelist()
    assert len(names)==len(rows)+1 and len({s.casefold() for s in names})==len(names)
    assert set(names)=={r["path"] for r in rows}|{"PACKAGE_MANIFEST.json"}
    assert z.testzip() is None
    for info in z.infolist():
        assert not stat.S_ISLNK(info.external_attr>>16)
        p=PurePosixPath(info.filename)
        assert not p.is_absolute() and ".." not in p.parts
    for row in rows:
        b=z.read(row["path"])
        assert len(b)==row["bytes"] and sha(b)==row["sha256"]
        assert f"{zlib.crc32(b)&0xffffffff:08x}"==row["crc32"]
    assert z.read("PACKAGE_MANIFEST.json")==(R/"PACKAGE_MANIFEST.json").read_bytes()
for row in post:
    assert ident(R/row["relative_path"])=={k:row[k] for k in ("bytes","sha256")}
write("SELECTED_CAPTURES_POST_PACKAGE.json",{"scope":"43 reviewer-side received source captures only; not remote filesystem preservation",
"count":len(post),"all_match":True,"files":post})
receipt={"kind":"E1_0_REVIEW_DELIVERY_RECEIPT","recipient":None,"archive":{"name":archive.name,**ident(archive)},
"manifest":{"name":"PACKAGE_MANIFEST.json",**ident(R/"PACKAGE_MANIFEST.json")},
"payload_count":len(rows),"entries":len(rows)+1,"verification":{"exact_set":True,"size_sha256_crc32":True,
"safe_unique_paths_no_links":True},"selected_captures_preserved":len(post),
"decision":decision["decision"],"reviewed_head":decision["reviewed_head"],
"received_program_execution":0,"new_execution_authorized":False,
"boundary":"After archive readback and selected capture rehash; before receipt write and this tool return",
"whole_review_elapsed_or_budget_claim":None}
write("DELIVERY_RECEIPT.json",receipt)
assert jload(R/"DELIVERY_RECEIPT.json")==receipt
print(json.dumps({"kind":"E1_0_REVIEW_PACKAGE_RETURN","archive":receipt["archive"],"receipt":ident(R/"DELIVERY_RECEIPT.json"),
"payload_count":len(rows),"entries":len(rows)+1,"verification":receipt["verification"],
"selected_captures_preserved":len(post),"audit_matched":audit["matched"],"attachment_same_bytes":same_bytes,
"decision":decision["decision"],"received_program_execution":0,"boundary":"After receipt write/readback; before tool return"},ensure_ascii=False))
