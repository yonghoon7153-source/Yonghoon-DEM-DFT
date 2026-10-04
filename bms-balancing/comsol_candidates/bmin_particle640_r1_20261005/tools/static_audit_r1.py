"""B-min r1 정적 대조 — 텍스트 · JSON · 해시만. 후보 코드의 import · 구문 해석 · 컴파일 · 실행 0, COMSOL · JVM 0.

  python3 tools/static_audit_r1.py     # r1 꾸러미 루트에서 — STATIC_AUDIT.json 을 쓰고, 실패가 하나라도 있으면 rc 1

1. v1 꾸러미가 검토받은 커밋 (74502af93) 의 바이트 그대로인지 · v1 자신의 정적 대조 (81) 를 다시 돌려 v1 → NORMAL480 사슬을 잇는다.
2. R1_CHANGE_BOUNDARIES.json 의 순서대로 r1 의 선언 변경만 되돌리면 v1 바이트와 정확히 같아야 한다 (r1 → v1 역재구성).
3. r1 의 결속 (manifest · 명령 · 계약 · 검증안 · 문서) 과 바뀌면 안 되는 부분.
"""
import hashlib
import json
import pathlib
import subprocess
import sys

PKG = pathlib.Path(__file__).resolve().parent.parent
V1PKG = PKG.parent / "bmin_particle640_20261004"
V1 = V1PKG / "candidate"
R1 = PKG / "candidate"
ROOT = PKG.parent.parent.parent  # 저장소 루트
V1_MANIFEST = "3722a51fb1caeddd72fca3751f2ed78ed3e05d5f1938fa452503b3fa5c421a03"
REVIEWED = "74502af93db0f01bb3ae99eca981cc215300b8bf"
checks = []


def sha(b):
    return hashlib.sha256(b).hexdigest()


def check(name, ok, detail=None):
    checks.append({"check": name, "status": "STATIC_MATCH" if ok else "FAIL", **({"detail": detail} if detail is not None else {})})
    return ok


def seg(text, start, end, offset=0):
    if text.count(start) != 1 or (end is not None and text.count(end) != 1):
        raise ValueError(f"marker not unique: {start!r} / {end!r}")
    a = text.index(start)
    b = len(text) if end is None else text.index(end) + offset
    if b <= a:
        raise ValueError("marker order")
    return a, b


def lines_of(text, a, b):
    return [text.count("\n", 0, a) + 1, text.count("\n", 0, b)]


def git_show(rev, rel):
    r = subprocess.run(["git", "-C", str(ROOT), "show", f"{rev}:{rel}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def main():
    bound = json.loads((PKG / "R1_CHANGE_BOUNDARIES.json").read_text(encoding="utf-8"))
    lit = json.loads((PKG / "R1_LITERAL_CHANGES.json").read_text(encoding="utf-8"))

    # 1. v1 — 검토받은 바이트 · v1 → NORMAL480 사슬
    v1rel = "bms-balancing/comsol_candidates/bmin_particle640_20261004"
    listed = subprocess.run(["git", "-C", str(ROOT), "ls-tree", "-r", "--name-only", REVIEWED, "--", v1rel], capture_output=True, text=True).stdout.split()
    changed = [rel for rel in listed if git_show(REVIEWED, rel) != (ROOT / rel).read_bytes()]
    check("v1 package = bytes at the reviewed commit 74502af93", len(listed) > 20 and not changed, {"files": len(listed), "changed": changed})
    v1m = (V1 / "CODE_MANIFEST.json").read_bytes()
    check("v1 CODE_MANIFEST = 3722a51f…", sha(v1m) == V1_MANIFEST)
    r = subprocess.run([sys.executable, str(V1PKG / "tools/static_audit.py")], capture_output=True, text=True)
    after = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--", v1rel], capture_output=True, text=True).stdout.strip()
    check("v1 static audit re-run: 81 checks, 0 failed, rc 0 (v1 -> NORMAL480 chain) and its STATIC_AUDIT.json unchanged",
          r.returncode == 0 and '"checks": 81, "failed": 0' in r.stdout and after == "", {"stdout": r.stdout.strip()[-120:], "git_status": after})

    # 2. r1 재생성 · r1 -> v1 역재구성
    r = subprocess.run([sys.executable, str(PKG / "tools/build_candidate_r1.py"), "--check"], capture_output=True, text=True)
    check("build_candidate_r1.py --check reproduces candidate/ and R1_LITERAL_CHANGES.json", r.returncode == 0,
          r.stdout.strip().splitlines()[-1:] + r.stderr.strip().splitlines()[-1:])
    regions = {}
    for rel, spec in bound["files"].items():
        if spec["kind"] == "JSON":
            continue
        raw, v1raw = (R1 / rel).read_bytes(), (V1 / rel).read_bytes()
        try:
            raw.decode("ascii")
            check(f"{rel} ASCII only", True)
        except UnicodeDecodeError:
            check(f"{rel} ASCII only", False)
        if spec["kind"] == "UNCHANGED":
            check(f"{rel} byte-identical to v1", raw == v1raw)
            continue
        check(f"{rel} all CRLF", raw.count(b"\r\n") == raw.count(b"\n") > 0)
        text, orig, v1text = raw.decode("ascii").replace("\r\n", "\n"), None, v1raw.decode("ascii").replace("\r\n", "\n")
        orig = text
        rr = []
        try:
            for op in spec["reverse"]:
                if op["op"] == "restore_block":
                    off = op.get("end_offset", 0)
                    a, b = seg(text, op["new"][0], op["new"][1], off)
                    oa, ob = seg(v1text, op["old"][0], op["old"][1], off)
                    ca, cb = seg(orig, op["new"][0], op["new"][1], off)
                    rr.append({"op": "restore_block", "finding": op["finding"], "r1_lines": lines_of(orig, ca, cb), "r1_block_sha256": sha(orig[ca:cb].encode()),
                               "v1_lines": lines_of(v1text, oa, ob), "v1_block_sha256": sha(v1text[oa:ob].encode())})
                    text = text[:a] + v1text[oa:ob] + text[b:]
                elif op["op"] == "inverse_literals":
                    for e in reversed(lit[op["table"]]):
                        if text.count(e["after"]) != e["count"]:
                            raise ValueError(f"literal count {e['after'][:50]!r}: {text.count(e['after'])} != {e['count']}")
                        text = text.replace(e["after"], e["before"])
                    rr.append({"op": "inverse_literals", "entries": len(lit[op["table"]]), "occurrences": sum(e["count"] for e in lit[op["table"]])})
            ok = text == v1text
        except ValueError as e:
            ok = False
            rr.append({"error": str(e)})
        check(f"{rel}: undoing only the declared r1 changes gives the exact v1 bytes", ok)
        regions[rel] = rr

    # 3. 바뀌면 안 되는 부분 · 결속
    def blocks(text, prefix, stops):
        out, lines = {}, text.split("\n")
        idx = [i for i, ln in enumerate(lines) if ln.startswith(prefix)]
        for k, i in enumerate(idx):
            name = lines[i][len(prefix):].split("(")[0].split(" ")[0]
            j = idx[k + 1] if k + 1 < len(idx) else len(lines)
            for m in range(i + 1, j):
                if any(lines[m].startswith(s) for s in stops):
                    j = m
                    break
            out[name] = "\n".join(lines[i:j])
        return out
    cv1 = blocks((V1 / "src/diagnostic_consumer.py").read_bytes().decode("ascii").replace("\r\n", "\n"), "def ", [])
    cr1 = blocks((R1 / "src/diagnostic_consumer.py").read_bytes().decode("ascii").replace("\r\n", "\n"), "def ", [])
    same = sorted(n for n in cv1 if n != "mesh_evidence" and cv1[n] == cr1.get(n))
    check("consumer: every function except mesh_evidence byte-identical to v1", set(cv1) == set(cr1) and len(same) == len(cv1) - 1, {"identical": len(same)})
    pv1 = blocks((V1 / "PARENT_COMMAND.ps1").read_bytes().decode("ascii").replace("\r\n", "\n"), "function ", ["try {"])
    p1 = (R1 / "PARENT_COMMAND.ps1").read_bytes().decode("ascii").replace("\r\n", "\n")
    pr1 = blocks(p1, "function ", ["try {"])
    for name in ("BHash", "BRef", "BRead", "BSave", "BInvoke"):
        check(f"parent {name} byte-identical to v1", pv1.get(name) is not None and pv1.get(name) == pr1.get(name))
    check("parent function set = v1 + GNativeAxis", sorted(set(pr1) - set(pv1)) == ["GNativeAxis"] and not (set(pv1) - set(pr1)))
    gd = pr1["GDecision"]
    helpers = gd[gd.index("    function GHas("):gd.index("    if (-not (GNumber $Overall")]
    check("GNativeAxis repeats GDecision's three nested helpers byte for byte", helpers in pr1["GNativeAxis"])
    gd_v1 = pv1["GDecision"]
    e = [x for x in lit["PARENT_COMMAND.ps1"] if x["finding"] == "BMIN-N2"][0]
    check("GDecision differs from v1 only by the declared transient_dof condition", gd.replace(e["after"], e["before"]) == gd_v1 and gd.count(e["after"]) == 1)
    check("GFields is called three times with the native axis", p1.count("fields=(GFields $limited $bNativeAxis $result)") == 3 and "GFields $limited $result" not in p1)
    check("GNativeAxis is computed once, right after GDecision", p1.count("$bNativeAxis=GNativeAxis $bRunReturn $result") == 1
          and p1.index("$limited=GDecision $bRunReturn") < p1.index("$bNativeAxis=GNativeAxis") < p1.index("BSave 'PARENT_LOCAL_DECISION.json'"))
    for cause in ("NATIVE_CHILD_RETURN_MISSING_OR_ERROR", "NATIVE_CHILD_RC", "TERMINATION_EVIDENCE_MISSING", "RESULT_IDENTITY", "TERMINATION_EVIDENCE_INVALID",
                  "CONSUMER_NATIVE_LABEL_MISMATCH", "NATIVE_AXIS_NOT_EVALUATED"):
        check(f"parent names the native-axis cause {cause}", cause in p1)
    c1 = (R1 / "src/diagnostic_consumer.py").read_bytes().decode("ascii")
    for reason in ("TRANSIENT_DOF_READBACK_COUNT", "TRANSIENT_DOF_READBACK_FORMAT", "TRANSIENT_DOF_READBACK_VALUE"):
        check(f"consumer names {reason}", reason in c1)
    cv, cr = json.loads((V1 / "CONTRACT.json").read_bytes()), json.loads((R1 / "CONTRACT.json").read_bytes())
    cv["expected_transient_dof"]["status"] = "OBSERVATION_REQUIRED_DIFFERENCE_RECORD_ONLY"
    check("CONTRACT differs from v1 only in expected_transient_dof.status", cv == cr)
    m_raw = (R1 / "CODE_MANIFEST.json").read_bytes()
    m, mv1, msha = json.loads(m_raw), json.loads(v1m), sha(m_raw)
    check("r1 manifest: flags false, previous = v1, five files with exact bytes", m["approved"] is False and m["usable"] is False
          and m["previous_manifest_sha256"] == V1_MANIFEST and [f["file"] for f in m["files"]] == [f["file"] for f in mv1["files"]]
          and all(len((R1 / f["file"]).read_bytes()) == f["bytes"] and sha((R1 / f["file"]).read_bytes()) == f["sha256"] for f in m["files"]))
    for name in ("COMMAND_MAP.json", "NATIVE_APPROVAL_FIELD_SPEC.json"):
        a = (R1 / name).read_text(encoding="ascii")
        b = (V1 / name).read_text(encoding="ascii")
        check(f"{name}: v1 bytes with only the manifest SHA replaced", a == b.replace(V1_MANIFEST, msha) and msha in a)
    plan = json.loads((PKG / "LIMITED_VALIDATION_PLAN.json").read_text(encoding="utf-8"))
    ids = {c["id"] for g in plan["groups"] for c in g["cases"]}
    need_ids = {"PS01-09", "PS01-10", "PS01-11", "PS01-12", "PS01-13", "PS01-14", "PS01-15", "PS01-16", "PS01-17",
                "PY03-05", "PY03-06", "PY03-07", "PY03-08", "PY03-09", "PY03-10"}
    check("validation plan: bound to r1 manifest, approvals false, counts consistent, N1 / N2 / C1 cases present", plan["manifest_sha256"] == msha
          and plan["approved"] is False and plan["usable"] is False and plan["cases"] == len(ids) == sum(len(g["cases"]) for g in plan["groups"])
          and need_ids <= ids and sum(v for k, v in plan["budget_seconds"].items() if k != "overall") == plan["budget_seconds"]["overall"],
          sorted(need_ids - ids))
    docs = {n: (PKG / n).read_text(encoding="utf-8") for n in ("PREPARATION_KO.md", "VALIDATION_REQUEST_KO.md", "NATIVE_BMIN640_APPROVAL_DRAFT_KO.md")}
    check("r1 documents name the r1 manifest SHA", all(msha in v for v in docs.values()), [n for n, v in docs.items() if msha not in v])
    check("r1 documents carry the SPEC section 44-2 sentence", all("한도와 같으면 허용한다 (≤)" in v for v in docs.values()))

    failed = [x for x in checks if x["status"] != "STATIC_MATCH"]
    out = {"kind": "SOURCE_TEXT_JSON_HASH_DIFF_ONLY", "candidate_manifest_sha256": msha, "previous_manifest_sha256": V1_MANIFEST,
           "checks_total": len(checks), "checks_failed": len(failed), "candidate_imports": 0, "candidate_parse_compile_tests": 0,
           "JVM_COMSOL_gate_calls": 0, "native_compatibility": "UNTESTED", "functional_status": "UNTESTED",
           "reverse_reconstruction_r1_to_v1": regions, "checks": checks}
    (PKG / "STATIC_AUDIT.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"checks": len(checks), "failed": len(failed), "manifest": msha}, ensure_ascii=False))
    for x in failed:
        print("FAIL", x["check"], x.get("detail"))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
