from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,stat
ROOT=Path(__file__).resolve().parent
ZIP=Path("C:/Users/Administrator/Downloads/COMSOL_MICROSHORT_S1O_OFFLINE_PREPARATION_20261007.zip")
DEST=ROOT/"received"
if DEST.exists(): raise RuntimeError("Existing destination")
raw=ZIP.read_bytes()
assert len(raw)==761798 and hashlib.sha256(raw).hexdigest()=="0cae7accaf26397d883e0d8b732357fc2dc640553c603825a6a155bf8d4aaf53"
with zipfile.ZipFile(ZIP) as z:
    names=z.namelist()
    assert len(names)==len(set(names))==len(set(n.casefold() for n in names))
    for info in z.infolist():
        p=PurePosixPath(info.filename)
        assert not p.is_absolute() and ".." not in p.parts and ":" not in info.filename and "\\" not in info.filename
        assert not stat.S_ISLNK(info.external_attr>>16) and not info.is_dir()
    assert sum(i.file_size for i in z.infolist())<20*1024*1024
    mraw=z.read("MANIFEST.json"); m=json.loads(mraw)
    entries={i["path"]:i for i in m["files"]}
    assert len(entries)==112 and set(names)==set(entries)|{"MANIFEST.json"}
    assert hashlib.sha256(mraw).hexdigest()=="0ee9d38b0e0cfd30576eb9e1c5e69e33b80c7c69ee513b4b621c7f9aa5f8286b"
    payload={}
    for name in names:
        data=z.read(name)
        if name in entries:
            item=entries[name]
            assert len(data)==item["bytes"] and hashlib.sha256(data).hexdigest()==item["sha256"],name
        payload[name]=data
    assert z.testzip() is None
    for name,data in payload.items():
        p=DEST/Path(name); p.parent.mkdir(parents=True,exist_ok=True)
        with p.open("xb") as f: f.write(data)
r={"kind":"RECIPIENT_ARCHIVE_DATA_CHECK","archive_bytes":len(raw),"archive_sha256":hashlib.sha256(raw).hexdigest(),"payload_count":112,"entries":113,"exact_set":True,"all_member_bytes_sha256":True,"CRC":True,"safe_paths_case_links":True,"received_programs_executed":0}
with (ROOT/"ARCHIVE_CHECK.json").open("x",encoding="utf8") as f: json.dump(r,f,indent=2)
print(json.dumps(r))

