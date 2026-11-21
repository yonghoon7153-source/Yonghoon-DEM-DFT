"""Write a local development comparison from the files the author actually returned."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tarfile
import zipfile

ARMS = ("UB", "UT", "UC", "UVa", "UVb", "UTc")
MAPPING = {"t1":"UB","t2":"UVa","t3":"UT","t4":"UVb"}


def bound_verdict(z, arm, checksums):
    name = "reports/" + arm + ".report.tgz"
    receipt_path = "state/jobs/" + arm + "/receipt.json"
    if receipt_path not in checksums:
        return {"status":"INCOMPLETE_TECHNICAL_RECEIPT"}
    receipt = json.loads(z.read(receipt_path))
    if (receipt.get("arm") != arm or receipt.get("state") != "COMPLETED" or receipt.get("exit_code") != "0:0"
            or receipt.get("technical_ok") is not True or receipt.get("report_sha256") != checksums[name]):
        raise ValueError("report and technical receipt differ for " + arm)
    wanted = {arm+"/arm_verdict.json": receipt["verdict_sha256"],
              arm+"/run_manifest.txt": receipt["manifest_sha256"],
              "selection.json": receipt["selection_sha256"]}
    seen = {}
    with z.open(name) as src, tarfile.open(fileobj=src, mode="r|gz") as report:
        for m in report:
            if m.name in wanted:
                if m.name in seen or not m.isfile() or m.size>32*1024*1024:
                    raise ValueError("unexpected report member")
                data = report.extractfile(m).read()
                if hashlib.sha256(data).hexdigest()!=wanted[m.name]:
                    raise ValueError("changed report member for " + arm)
                seen[m.name] = data
    if seen.keys() != wanted.keys():
        raise ValueError("missing report member")
    v = json.loads(seen[arm+"/arm_verdict.json"])
    if v.get("bed") != "ps_7_3_r45" or v.get("job") != arm:
        raise ValueError("wrong arm in report")
    return {"status":"TECHNICAL_RECEIPT_MATCH","job_id":receipt["job_id"],
            "report_sha256":checksums[name], "origin_verdict_sha256":receipt["verdict_sha256"],
            "primary_status":v.get("primary_status"),"recorded_rho_pct":v.get("rho_pct"),
            "bracket_pct":v.get("bracket_pct"),"trajectory_status":v.get("trajectory_status"),
            "surface_um":v.get("surface_um"), "union_bracket_pct":v.get("union_bracket_pct")}


def summarize(path):
    spec = importlib.util.spec_from_file_location("verify_package",Path(__file__).with_name("check_return.py"))
    reader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reader)
    reader.verify(path)
    with zipfile.ZipFile(path) as z:
        sums = {n:h for h,n in (s.split("  ",1) for s in z.read("SHA256SUMS").decode("ascii").splitlines())}
        rows = {a:bound_verdict(z,a,sums) for a in ARMS if "reports/"+a+".report.tgz" in sums}
        final = json.loads(z.read("state/sequence_result.json")) if "state/sequence_result.json" in sums else {}
        plan = final.get("plan",{})
        result = {"scope":"DEVELOPMENT_ONLY", "source_job":"368315","bed":"ps_7_3_r45",
                  "pressure_endpoint_MPa":1,"sequence_status":final.get("status","PARTIAL_RETURN"),
                  "sequence_reason":plan.get("reason"),"arms":rows,"selected_comparison":None,
                  "requires_endpoint_and_bracket_review":True, "gravity_qualification":"GT1_GT2_AMENDMENT_PENDING",
                  "validation_against_experiment":"NOT_ESTABLISHED"}
        if final.get("status") == "REVIEW":
            row = plan["tuple"]
            if row not in MAPPING or "reports/selection.json" not in sums:
                raise ValueError("missing final registration choice")
            s = json.loads(z.read("reports/selection.json"))
            last = "UTc" if row=="t3" else "UVa" if row in ("t1","t2") else "UVb"
            last_r = json.loads(z.read("state/jobs/"+last+"/receipt.json"))
            required = ["UB","UT","UC","UVa" if row in ("t1","t2") else "UVb"]
            if row == "t3":
                required.append("UTc")
            if (plan.get("completed") != required or set(rows) != set(required)
                    or any(rows[a].get("status") != "TECHNICAL_RECEIPT_MATCH" for a in required)
                    or s.get("stage")!="resolved" or s.get("tuple")!=row
                    or sums["reports/selection.json"]!=last_r["selection_sha256"]):
                raise ValueError("final selection does not match final arm")
            arm = MAPPING[row]
            aux = "UTc" if row=="t3" else arm
            if any(rows.get(k,{}).get("status")!="TECHNICAL_RECEIPT_MATCH" for k in (arm,aux,last)):
                raise ValueError("selected arm missing")
            result["selected_comparison"] = {"tuple":row,"primary_arm":arm,"auxiliary_arm":aux,
                "rho_pct":rows[arm]["recorded_rho_pct"],"bracket_pct":rows[arm]["bracket_pct"],
                "trajectory_status":rows[aux]["trajectory_status"],"surface_um":rows[aux]["surface_um"],
                "delta_dt_pct_points":s.get("delta_dt"),"delta_v_pct_points":s.get("delta_v")}
        return result


if __name__ == "__main__":
    try:
        result=summarize(sys.argv[1])
        with Path(sys.argv[2]).open("x",encoding="utf-8") as f:
            json.dump(result,f,indent=2,allow_nan=False)
            f.write("\n")
        print("DEVELOPMENT_READBACK="+result["sequence_status"])
    except (OSError, ValueError, KeyError, EOFError, tarfile.TarError, zipfile.BadZipFile) as err:
        print("INCOMPLETE_READBACK",err,file=sys.stderr)
        sys.exit(2)
