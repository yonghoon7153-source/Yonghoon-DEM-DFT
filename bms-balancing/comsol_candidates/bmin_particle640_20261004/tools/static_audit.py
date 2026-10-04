"""B-min 후보 꾸러미의 정적 대조 — 텍스트 · JSON · 해시만. 후보 코드의 import · 구문 해석 · 컴파일 · 실행 0, COMSOL · JVM 0.

  python3 tools/static_audit.py            # 패키지 루트에서 — STATIC_AUDIT.json 을 쓰고, 실패가 하나라도 있으면 rc 1

핵심 검사는 역재구성이다: CHANGE_BOUNDARIES.json 의 순서대로 선언된 블록을 원본 블록으로 되돌리고, 선언된 삽입을 지우고,
LITERAL_CHANGE_MAP.json 의 치환을 거꾸로 적용하면 NORMAL480 원본 바이트와 정확히 같아야 한다. 선언 밖의 변경은 여기서 걸린다.
"""
import hashlib
import json
import pathlib
import subprocess
import sys

PKG = pathlib.Path(__file__).resolve().parent.parent
REPO_BMS = PKG.parent.parent  # bms-balancing/
BASIS = PKG / "basis/source480/candidate"
CAND = PKG / "candidate"
checks = []

BASIS_FULL = {
    "CODE_MANIFEST.json": (1046, "7a5cc2f1717ae7a80cd7e423861965ad51c5f639272eab7f3a3c7680499ae22c"),
    "COMMAND_MAP.json": (6045, "e29109239edc0246657d41a097ea2ed369fa446c559286dad5aa5b7e3d925fec"),
    "CONTRACT.json": (125504, "58d398a663ceb35e49154c32ab04ce0ea5720f7fe0664db0e0fa09f1dfdf3b08"),
    "NATIVE_APPROVAL_FIELD_SPEC.json": (4125, "8f4c90fb13382bde3f11a307e4247a829a00f1a5caa7558b9597ffb2f5d5a327"),
    "PARENT_COMMAND.ps1": (19213, "e8a770f5908c30a981875c49d92e4e6657efc6bf0273c217001fbadb69d667c9"),
    "src/Normal480Candidate.java": (99959, "c70526cf6884eabc57b63dd43dce4b47fb0decf59af68d3f550f1b987d053797"),
    "src/candidate_entry.py": (13999, "6178a0c5b6ce79b22dc3e1a1ee717536fb8ef055834c2a28e1221c1b4b0937e5"),
    "src/diagnostic_consumer.py": (20369, "c952e7c2674efd45f31d534998a4b63629558d45ec47d03d37b3e08682ed835c"),
}
RUNTIME_CSV = PKG / "basis/source480/run/tables/axes_runtime_settings.csv"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def check(name, ok, detail=None):
    checks.append({"check": name, "status": "STATIC_MATCH" if ok else "FAIL", **({"detail": detail} if detail is not None else {})})
    return ok


def text_of(raw, crlf):
    return raw.decode("ascii").replace("\r\n", "\n") if crlf else raw.decode("ascii")


def seg(text, start, end):
    if text.count(start) != 1 or (end is not None and text.count(end) != 1):
        raise ValueError(f"marker not unique: {start!r} / {end!r}")
    a = text.index(start)
    b = len(text) if end is None else text.index(end)
    if b <= a:
        raise ValueError("marker order")
    return a, b


def line_range(text, a, b):
    return [text.count("\n", 0, a) + 1, text.count("\n", 0, b)]


def main():
    lit = json.loads((PKG / "LITERAL_CHANGE_MAP.json").read_text(encoding="utf-8"))
    bound = json.loads((PKG / "CHANGE_BOUNDARIES.json").read_text(encoding="utf-8"))

    # 1. 원본 바이트 — 고정값 · 저장소 SPEC §45-2 의 앞 16 자리와 교차
    spec = (REPO_BMS / "docs/COMSOL_REBUILD_SPEC.md").read_text(encoding="utf-8")
    basis = {}
    for rel, (size, h) in BASIS_FULL.items():
        b = (BASIS / rel).read_bytes()
        basis[rel] = b
        check(f"basis bytes {rel}", len(b) == size and sha(b) == h, {"bytes": len(b), "sha256": sha(b)})
        check(f"basis sha prefix in SPEC §45-2 {rel}", h[:16] in spec)
    rt = RUNTIME_CSV.read_bytes()
    check("basis run/tables/axes_runtime_settings.csv bytes", len(rt) == 28190 and sha(rt) == "19f32130a461b65aca63af0f96f7e4b80a871f5256149e861f2923e7c6d758dc")

    # 2. 재생성 — 변환 스크립트가 지금 바이트를 그대로 다시 만든다 (우리 도구 · 후보 코드 실행 아님)
    r = subprocess.run([sys.executable, str(PKG / "tools/build_candidate.py"), "--check"], capture_output=True, text=True)
    check("build_candidate.py --check reproduces candidate/ and LITERAL_CHANGE_MAP.json", r.returncode == 0, r.stdout.strip().splitlines()[-1:] + r.stderr.strip().splitlines()[-1:])

    # 3. 역재구성
    reconstruction = {}
    for rel, spec_f in bound["files"].items():
        crlf = spec_f["line_endings"] == "CRLF"
        raw = (CAND / rel).read_bytes()
        braw = basis[spec_f["basis"]]
        if crlf:
            check(f"{rel} all CRLF", raw.count(b"\r\n") == raw.count(b"\n") > 0)
        else:
            check(f"{rel} LF only", b"\r" not in raw)
        try:
            raw.decode("ascii")
            ascii_ok = True
        except UnicodeDecodeError:
            ascii_ok = False
        check(f"{rel} ASCII only (Windows PowerShell 5.1 / javac / python -X utf8 read without BOM)", ascii_ok)
        text = text_of(raw, crlf)
        orig = text  # 줄 번호는 손대기 전 후보 파일 기준으로 적는다
        btext = text_of(braw, crlf)
        regions = []
        try:
            for op in spec_f["reverse"]:
                if op["op"] == "restore_block":
                    a, b = seg(text, *op["new"])
                    oa, ob = seg(btext, *op["old"])
                    ca, cb = seg(orig, *op["new"])
                    regions.append({"op": "restore_block", "category": op["category"], "candidate_lines": line_range(orig, ca, cb),
                                    "candidate_block_sha256": sha(text[a:b].encode()), "basis_lines": line_range(btext, oa, ob),
                                    "basis_block_sha256": sha(btext[oa:ob].encode())})
                    text = text[:a] + btext[oa:ob] + text[b:]
                elif op["op"] == "remove_insert":
                    if text.count(op["after"]) != 1:
                        raise ValueError(f"insert anchor not unique: {op['after'][:40]!r}")
                    i = text.index(op["after"]) + len(op["after"])
                    j = text.index(op["before"], i)
                    ci = orig.index(op["after"]) + len(op["after"])
                    cj = orig.index(op["before"], ci)
                    regions.append({"op": "remove_insert", "category": op["category"], "candidate_lines": line_range(orig, ci, cj),
                                    "inserted_sha256": sha(text[i:j].encode()), "inserted_line_count": text[i:j].count("\n")})
                    text = text[:i] + text[j:]
                elif op["op"] == "inverse_literals":
                    for e in reversed(lit["files"][op["table"]]):
                        if text.count(e["after"]) != e["count"]:
                            raise ValueError(f"literal count {e['after'][:40]!r}: {text.count(e['after'])} != {e['count']}")
                        text = text.replace(e["after"], e["before"])
                    regions.append({"op": "inverse_literals", "entries": len(lit["files"][op["table"]]),
                                    "occurrences": sum(e["count"] for e in lit["files"][op["table"]])})
                else:
                    raise ValueError("unknown op")
            ok = text == btext
        except ValueError as e:
            ok = False
            regions.append({"error": str(e)})
        check(f"{rel}: undoing only the declared changes gives the exact basis bytes", ok)
        reconstruction[rel] = {"basis": spec_f["basis"], "kind": spec_f["kind"], "regions": regions}

    # 4. 바뀌지 않아야 할 함수 — 바이트 그대로
    def blocks(text, prefix, stop_markers):
        out = {}
        lines = text.split("\n")
        idx = [i for i, ln in enumerate(lines) if ln.startswith(prefix)]
        for k, i in enumerate(idx):
            name = lines[i][len(prefix):].split("(")[0].split(" ")[0]
            j = idx[k + 1] if k + 1 < len(idx) else len(lines)
            for m in range(i + 1, j):
                if any(lines[m].startswith(s) for s in stop_markers):
                    j = m
                    break
            out[name] = "\n".join(lines[i:j])
        return out
    old_c = blocks(text_of(basis["src/diagnostic_consumer.py"], True), "def ", [])
    new_c = blocks(text_of((CAND / "src/diagnostic_consumer.py").read_bytes(), True), "def ", [])
    for name in ("need", "number", "identity", "pinned", "rows", "timed", "extract_tables", "rounded_contains", "binding_evidence", "profile", "units_evidence"):
        check(f"consumer {name} byte-identical", old_c.get(name) is not None and old_c.get(name) == new_c.get(name))
    check("consumer function set", sorted(set(new_c) - set(old_c)) == ["extreme", "mesh_evidence", "three_fields", "window_coverage"]
          and sorted(set(old_c) - set(new_c)) == ["coverage", "late_summary"], {"added": sorted(set(new_c) - set(old_c)), "removed": sorted(set(old_c) - set(new_c))})
    old_p = blocks(text_of(basis["PARENT_COMMAND.ps1"], True), "function ", ["try {"])
    new_p = blocks(text_of((CAND / "PARENT_COMMAND.ps1").read_bytes(), True), "function ", ["try {"])
    for name in ("BHash", "BRef", "BRead", "BSave", "BInvoke"):
        check(f"parent {name} byte-identical", old_p.get(name) is not None and old_p.get(name) == new_p.get(name))
    check("parent function set", sorted(set(new_p) - set(old_p)) == ["GFields"] and not (set(old_p) - set(new_p)))

    # 5. JSON — 플래그 · 결속 · 키 차이
    c = json.loads((CAND / "CONTRACT.json").read_bytes())
    oc = json.loads(basis["CONTRACT.json"])
    m_raw = (CAND / "CODE_MANIFEST.json").read_bytes()
    m = json.loads(m_raw)
    cmd = json.loads((CAND / "COMMAND_MAP.json").read_bytes())
    fs = json.loads((CAND / "NATIVE_APPROVAL_FIELD_SPEC.json").read_bytes())
    msha = sha(m_raw)
    check("approved/usable false (CONTRACT · CODE_MANIFEST · FIELD_SPEC)", c["approved"] is False and c["usable"] is False and m["approved"] is False
          and m["usable"] is False and fs["approved"] is False and fs["usable"] is False and c["preparation_only"] is True)
    check("manifest lists the five sealed files with exact sizes / SHA-256",
          [f["file"] for f in m["files"]] == ["src/Bmin640Candidate.java", "src/diagnostic_consumer.py", "src/candidate_entry.py", "PARENT_COMMAND.ps1", "CONTRACT.json"]
          and all(len((CAND / f["file"]).read_bytes()) == f["bytes"] and sha((CAND / f["file"]).read_bytes()) == f["sha256"] for f in m["files"]))
    check("previous_manifest_sha256 = NORMAL480 manifest", m["previous_manifest_sha256"] == BASIS_FULL["CODE_MANIFEST.json"][1])
    check("COMMAND_MAP / FIELD_SPEC carry the manifest SHA", cmd["manifest_sha256"] == msha and fs["code_manifest_sha256"] == msha
          and cmd["parent"]["argv"][-1] == msha and cmd["execute"]["argv"][-1] == msha and cmd["analyze"]["argv"][-1] == msha)
    check("native commands equal in CONTRACT / COMMAND_MAP / FIELD_SPEC", c["commands"]["compile"] == cmd["native"]["compile"]["argv"] == fs["required_future_fields"]["commands"]["compile"]
          and c["commands"]["batch"] == cmd["native"]["batch"]["argv"] == fs["required_future_fields"]["commands"]["batch"])
    check("budgets equal in CONTRACT / FIELD_SPEC and sum to overall", c["budgets_seconds"] == fs["required_future_fields"]["budgets_seconds"]
          and sum(v for k, v in c["budgets_seconds"].items() if k != "overall") == c["budgets_seconds"]["overall"] == 10500, c["budgets_seconds"])
    check("approval / release paths agree", fs["future_approval_path"] == c["approval_path"] and fs["future_release_path"] == c["release_path"]
          and c["approval_path"] in cmd["execute"]["argv"] and c["approval_path"] in cmd["analyze"]["argv"])
    check("candidate_java pin = candidate source bytes", c["candidate_java"]["bytes"] == len((CAND / "src/Bmin640Candidate.java").read_bytes())
          and c["candidate_java"]["sha256"] == sha((CAND / "src/Bmin640Candidate.java").read_bytes()))
    decl = bound["json_files"]["CONTRACT.json"]
    check("CONTRACT key diff = declared", sorted(k for k in oc if k in c and oc[k] != c[k]) == sorted(decl["changed"])
          and sorted(k for k in oc if k not in c) == sorted(decl["removed"]) and sorted(k for k in c if k not in oc) == sorted(decl["added"]))
    check("CONTRACT inner changes: resource_proposal only disk_start_gib, policy only native_permission_status",
          {k for k in oc["resource_proposal"] if oc["resource_proposal"][k] != c["resource_proposal"].get(k)} == {"disk_start_gib"}
          and {k for k in oc["policy"] if oc["policy"][k] != c["policy"].get(k)} == {"native_permission_status"} and c["resource_proposal"]["disk_start_gib"] == 15)
    req = c["requested_times_s"]
    check("requested_times_s = first 1,637 NORMAL480 entries, ends at 150", req == oc["requested_times_s"][:1637] and req[-1] == "150" and oc["requested_times_s"][1637] == "150.1")
    win = [t for t in req if 120 <= float(t) <= 150]
    check("primary 301 = requested times in [120,150] incl. 120, 149.9, 150", c["primary_comparison_times_s"] == win and len(win) == 301 == c["primary_comparison_count"]
          and win[0] == "120" and win[-2:] == ["149.9", "150"] and c["comparison_window_s"] == {"start": "120", "end": "150"})
    check("coordinates, limits, runtime_settings_required, guard and solver contract unchanged", all(c[k] == oc[k] for k in (
        "coordinates", "limits", "runtime_settings_required", "guard_expression", "storestopcondsol", "threshold_mol_m3", "lagrange_order", "domains",
        "guard_stop_descriptions", "known_native_evidence_format", "native_executable_pins", "python", "cwd", "legacy_gate", "legacy_contract", "external_source_pins")))
    check("limits 0.001 V / 1e-4 strings", c["limits"]["voltage_V"] == "0.001" and c["limits"]["surface_x"] == "0.0001")
    check("comparison rule states equal-is-within and strictly-greater-exceeds", "(a value equal to a limit is within)" in c["comparison_rule"] and "strictly greater" in c["comparison_rule"])
    v2 = (REPO_BMS / "docs/COMSOL_BMIN_SCOPE_v2_20261004.md").read_text(encoding="utf-8")
    bad = [n for n, e in c["baseline_files"].items() if e["sha256"] not in v2 or f"{e['bytes']:,}" not in v2]
    check("baseline_files sizes / SHA-256 appear in B-min v2 section 3", not bad and len(c["baseline_files"]) == 9, bad)
    check("baseline_files point at NORMAL480 run tables", all(e["path"].startswith(oc["root"] + "/future_run_001/tables/") and e["path"].endswith("/" + n)
                                                             for n, e in c["baseline_files"].items()))
    check("runtime settings baseline entry = basis read-back bytes", c["baseline_files"]["axes_runtime_settings.csv"]["sha256"] == sha(rt)
          and c["baseline_files"]["axes_runtime_settings.csv"]["bytes"] == len(rt))
    import csv as _csv
    import io as _io
    rb = {r["key"]: r["actual_value"] for r in _csv.DictReader(_io.StringIO(rt.decode("utf-8-sig")))}
    check("NORMAL480 read-back satisfies runtime_settings_required and its tlist prefix = requested", all(rb.get(k) == v for k, v in c["runtime_settings_required"].items())
          and rb["study_tlist"].split()[:1637] == req and len(rb) == 22)

    # 6. Java 텍스트
    j = (CAND / "src/Bmin640Candidate.java").read_text(encoding="ascii")
    import re as _re
    tl = _re.findall(r'set\("tlist","([^"]*)"\)', j)
    check("Java tlist = CONTRACT requested_times_s", len(tl) == 1 and tl[0].split(" ") == req)
    check("Java particle Nel 640 twice, 320 none", j.count('set("Nel","640")') == 2 and 'set("Nel","320")' not in j)
    check("Java physical mesh 120/60/120 unchanged", 'set("numelem",domain==2 ? 60 : 120)' in j)
    check("Java one runAll, no loadCopy, class name = file name", j.count(".runAll();") == 1 and "loadCopy" not in j and "public class Bmin640Candidate {" in j)
    check("Java prints the read-back prefixes the consumer requires", all(p in j for p in ('"AXES_PHYSICAL_MESH_DOMAIN="', '"AXES_PARTICLE="', '"AXES_ACTUAL_MESH="', '"BMIN640_PRODUCER_COMPLETE"')))
    check("mesh_readback_required = physical 120/60/120, Nel 640/640, mesh1 300 edges", c["mesh_readback_required"] == [
        "AXES_PHYSICAL_MESH_DOMAIN=1|numelem=120", "AXES_PHYSICAL_MESH_DOMAIN=2|numelem=60", "AXES_PHYSICAL_MESH_DOMAIN=3|numelem=120",
        "AXES_PARTICLE=pce1|Nel=640|Nord=1|Distribution=CubicRoot", "AXES_PARTICLE=pce2|Nel=640|Nord=1|Distribution=CubicRoot",
        "AXES_ACTUAL_MESH=mesh1|edges=300|vertices=301"])
    check("expected transient DOF = 2045 + 242*640 (record only)", c["expected_transient_dof"]["solved"] == 2045 + 242 * 640 and c["expected_transient_dof"]["status"] == "RECORD_ONLY")
    ps = (CAND / "PARENT_COMMAND.ps1").read_text(encoding="ascii")
    check("parent root and approval field", "$bRoot='" + c["root"] + "'" in ps and "$a.native_bmin640_one_shot" in ps and "11400" not in ps)
    ent = (CAND / "src/candidate_entry.py").read_text(encoding="ascii")
    check("entry approval field and success label", "a.get('native_bmin640_one_shot') is True" in ent and "=='BMIN640_150S_COMPARISON_COMPLETE' else 1" in ent)

    # 7. 보존 — 이 저장소 안의 보존 대상은 후보 작성 직전 커밋 (REFERENCE) 의 바이트 그대로 · SPEC 는 덧붙이기만 (REFERENCE 바이트가 접두)
    #    (정상 60 s 준비본의 PRESERVATION before / after 에 해당 — 실행 기계의 생산 원본 · 기준 CSV 는 여기서 볼 수 없다).
    #    기준을 HEAD 가 아니라 고정 커밋으로 두어, 커밋 뒤에 다시 돌려도 같은 결과 · 같은 바이트가 나오게 한다.
    root = REPO_BMS.parent
    REFERENCE = "899f966de97f37541d37e39b3dfc53e41b0f72fb"
    def head(rel):
        r = subprocess.run(["git", "-C", str(root), "show", REFERENCE + ":" + rel], capture_output=True)
        return r.stdout if r.returncode == 0 else None
    protected = []
    for d in ("bms-balancing/comsol_candidates/bmin_particle640_20261004/basis",
              "bms-balancing/reviews/r14_repros/codex63/normal480_native_recipient_review_20261001",
              "bms-balancing/reviews/r14_repros/codex63/normal60_preparation_recipient_review_20260930",
              "bms-balancing/reviews/r14_repros/codex63/comsol_a0_bmin_documents_20261004"):
        ls = subprocess.run(["git", "-C", str(root), "ls-tree", "-r", "--name-only", REFERENCE, "--", d], capture_output=True, text=True).stdout.split()
        protected += ls
    protected += ["bms-balancing/docs/" + n for n in ("COMSOL_BMIN_SCOPE_20261004.md", "COMSOL_BMIN_SCOPE_v2_20261004.md", "COMSOL_EXPERIMENT_CORRESPONDENCE_v1_20261004.md",
                                                      "COMSOL_EXPERIMENT_CORRESPONDENCE_v2_20261004.md", "COMSOL_DATA_REQUEST_DRAFT_20261004.md",
                                                      "COMSOL_DATA_REQUEST_DRAFT_v2_20261004.md", "COMSOL_NEXT_PLAN_20261004.md")]
    changed = [rel for rel in protected if head(rel) is None or head(rel) != (root / rel).read_bytes()]
    check("preservation: protected repository files = bytes at the pre-candidate commit", not changed and len(protected) > 30,
          {"reference_commit": REFERENCE, "protected_count": len(protected), "changed": changed})
    spec_head = head("bms-balancing/docs/COMSOL_REBUILD_SPEC.md")
    spec_now = (REPO_BMS / "docs/COMSOL_REBUILD_SPEC.md").read_bytes()
    check("preservation: COMSOL_REBUILD_SPEC.md only appended since the pre-candidate commit (its bytes are a prefix)", spec_head is not None and spec_now.startswith(spec_head),
          {"reference_commit": REFERENCE, "reference_bytes": None if spec_head is None else len(spec_head)})

    plan = json.loads((PKG / "LIMITED_VALIDATION_PLAN.json").read_text(encoding="utf-8"))
    check("validation plan bound to this manifest, approvals false, counts consistent", plan["manifest_sha256"] == msha and plan["approved"] is False
          and plan["usable"] is False and plan["cases"] == sum(len(g["cases"]) for g in plan["groups"]) and plan["logical_groups"] == len(plan["groups"]))

    docs = {n: (PKG / n).read_text(encoding="utf-8") for n in ("PREPARATION_KO.md", "VALIDATION_REQUEST_KO.md", "NATIVE_BMIN640_APPROVAL_DRAFT_KO.md")}
    check("package documents name this manifest SHA", all(msha in v for v in docs.values()), [n for n, v in docs.items() if msha not in v])
    check("package documents carry the SPEC section 44-2 sentence", all("한도와 같으면 허용한다 (≤)" in v for v in docs.values()))

    failed = [x for x in checks if x["status"] != "STATIC_MATCH"]
    out = {"kind": "SOURCE_TEXT_JSON_HASH_DIFF_ONLY", "candidate_manifest_sha256": msha, "checks_total": len(checks), "checks_failed": len(failed),
           "candidate_imports": 0, "candidate_parse_compile_tests": 0, "JVM_COMSOL_gate_calls": 0, "native_compatibility": "UNTESTED",
           "functional_status": "UNTESTED", "reverse_reconstruction": reconstruction, "checks": checks}
    (PKG / "STATIC_AUDIT.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"checks": len(checks), "failed": len(failed), "manifest": msha}, ensure_ascii=False))
    for x in failed:
        print("FAIL", x["check"], x.get("detail"))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
