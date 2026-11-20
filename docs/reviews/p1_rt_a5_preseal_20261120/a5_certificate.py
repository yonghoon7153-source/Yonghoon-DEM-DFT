"""Bind an exclusive rev5 certificate and its completed production receipt."""
import hashlib
import json
import os
from pathlib import Path
import re

from a5_precheck import ANCHORS, LMP
from rt_publish import publish_new

MARK = b"a5_certificate_sha256="

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def unique(lines, key):
    values = [line[len(key)+1:] for line in lines if line.startswith(key + "=")]
    if len(values) != 1 or not values[0]:
        raise ValueError("receipt field missing or repeated: " + key)
    return values[0]

def checked_prefix(prefix, job, kit):
    if not prefix.endswith(b"\n") or MARK in prefix:
        raise ValueError("invalid or previously issued manifest")
    lines = prefix.decode("utf8").splitlines()
    if any(line.startswith(("end=", "reader_restore_rc=")) for line in lines):
        raise ValueError("completed or repeated attempt")
    expected = {"bed":"ps_7_3_r45", "job":"RJ", "np":"6", "resume":"0", "gate":"ALLOW",
                "sums_sha256":digest((kit/"A5_SHA256SUMS").read_bytes()), "lmp_sha256":LMP,
                "grammar_prereq":"PASS","rt_grammar_prereq":"PASS","orig_grid_prereq":"PASS",
                "rt_grammar_verdict_sha256":ANCHORS["a3_return.json"],
                "a3_readback_reader_sha256":ANCHORS["a3_corrected_reader.py"],
                "a4_historical_sha256":ANCHORS["a4_continuity.json"]}
    if not all(unique(lines,key)==value for key,value in expected.items()):
        raise ValueError("wrong candidate or attempt")
    recorded=Path(unique(lines,"job_dir"))
    if not recorded.is_absolute() or recorded.resolve(strict=True)!=job or job.name!="RJ" or job.parent.name!="ps_7_3_r45":
        raise ValueError("wrong production job path")
    unique(lines,"start")

def checked_result(report):
    if any(report.get(k)!=v for k,v in {"schema":"rt_restore_candidate_v1","restore_rule":"rev5_g2cp",
                                         "status":"RESTORED","bed":"ps_7_3_r45","job":"RJ"}.items()):
        raise ValueError("wrong certificate scope")
    if type(report.get("s0")) is not int or report["s0"]<=0 or report.get("certificate_published") is not True:
        raise ValueError("missing checkpoint or publication")
    checks=report["checks"]
    for k in ("G1","G2","G3","mesh_md5","G2cp","cont_R","cont_RT1","rt_binding"):
        if checks[k]["status"]!="PASS":
            raise ValueError("required check incomplete: "+k)
    for k,field in (("g0","ok"),("syntax","ok"),("pre_post","equal"),("rt_resets","ok"),("rt_post_list","ok"),
                    ("history_test","pass"),("un_erasure","seen")):
        if checks[k][field] is not True:
            raise ValueError("required check incomplete: "+k)
    for stage in ("R","UN","RT1","RT2","Ut0"):
        if checks["rt_technical"][stage]["ok"] is not True:
            raise ValueError("required stage incomplete")
    for key in ("G2cp","cont_R","cont_RT1"):
        numeric=checks[key]
        hashes=numeric["input_sha256"]
        if (not isinstance(hashes,list) or len(hashes)!=2 or
                not all(isinstance(h,str) and re.fullmatch("[a-f0-9]{64}",h) for h in hashes) or
                type(numeric["n_common"]) is not int or numeric["n_common"]<=0 or
                numeric["n_orig"]!=numeric["n_common"] or numeric["n_test"]!=numeric["n_common"]):
            raise ValueError("numeric input evidence incomplete")
    if (checks["G2cp"]["input_sha256"][0]!=checks["cont_RT1"]["input_sha256"][1] or
            checks["cont_R"]["input_sha256"][0]!=checks["cont_RT1"]["input_sha256"][0]):
        raise ValueError("numerical input identity mismatch")

def issue(job, report, kit):
    if report["status"]!="RESTORED":
        return publish_new(job,report)
    job=job.resolve(strict=True)
    manifest=job/"run_manifest.txt"
    prefix=manifest.read_bytes()
    checked_prefix(prefix,job,kit)
    checked_result(report)
    report["a5_receipt_prefix_sha256"]=digest(prefix)
    raw=(json.dumps(report,ensure_ascii=False,allow_nan=False,sort_keys=True,indent=2)+"\n").encode("utf8")
    cert=publish_new(job,report)
    if cert.read_bytes()!=raw:
        raise ValueError("published bytes differ from the issued certificate")
    # An interrupted publication leaves no usable success receipt. A retry cannot overwrite the certificate.
    with manifest.open("r+b") as handle:
        if handle.read()!=prefix:
            raise ValueError("attempt receipt changed during publication")
        handle.seek(0,os.SEEK_END)
        handle.write(MARK+digest(raw).encode("ascii")+b"\n")
        handle.flush()
        os.fsync(handle.fileno())
    return cert

def admits(job, kit):
    try:
        job=job.resolve(strict=True)
        raw=(job/"restore_verdict.json").read_bytes()
        report=json.loads(raw)
        checked_result(report)
        receipt=(job/"run_manifest.txt").read_bytes()
        if receipt.count(MARK)!=1:
            return False
        prefix,tail=receipt.split(MARK)
        checked_prefix(prefix,job,kit)
        tail=tail.decode("utf8").splitlines()
        return (tail[0]==digest(raw) and report.get("a5_receipt_prefix_sha256")==digest(prefix) and
                tail[1]=="reader_restore_rc=0" and unique(tail,"reader_restore_rc")=="0" and
                tail[-1].startswith("end=") and unique(tail,"end") and
                re.fullmatch(r"end=\S+ fails=0 reader_rc=0",tail[-1]) is not None)
    except (OSError,ValueError,UnicodeError,KeyError,TypeError,IndexError,AttributeError):
        return False
