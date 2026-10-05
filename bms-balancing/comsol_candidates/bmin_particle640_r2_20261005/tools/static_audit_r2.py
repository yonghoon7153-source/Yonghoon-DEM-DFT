"""B-min r2 정적 대조 — 텍스트 · JSON · 해시만. 후보 코드의 import · 구문 해석 · 컴파일 · 실행 0, COMSOL · JVM 0.

  python3 tools/static_audit_r2.py     # r2 꾸러미 루트에서 — STATIC_AUDIT.json 을 쓰고, 실패가 하나라도 있으면 rc 1

1. r1 꾸러미가 검토받은 커밋 (741dde19b) 의 바이트 그대로인지 · r1 자신의 정적 대조 (42 — 그 안에서 v1 의 81 도 다시 돈다) 를 다시 돌려
   r1 → v1 → NORMAL480 사슬을 잇는다.
2. R2_CHANGE_BOUNDARIES.json 의 선언 변경만 되돌리면 r1 바이트와 정확히 같아야 한다 (r2 → r1 역재구성).
3. r2 의 결속 (manifest · 명령 · 검증안 · 문서) 과 바뀌면 안 되는 부분.
4. 문자열 모형 — 이 도구 자신의 정규식으로 재검토 회신의 여섯 사례 (`INDEPENDENT_STATIC_AUDIT.json` `static_string_cases`) 와 r2 사례의 기대
   이유를 적는다. 모형이 후보 소스와 같은 규칙인지는 소스의 네 문장을 **글자로** 대조해서만 본다 — 후보 함수를 실행한 결과가 아니다.
"""
import hashlib
import json
import pathlib
import re
import subprocess
import sys

PKG = pathlib.Path(__file__).resolve().parent.parent
R1PKG = (PKG.parent / "bmin_particle640_r1_20261005").resolve()
R1 = R1PKG / "candidate"
R2 = PKG / "candidate"
ROOT = pathlib.Path(subprocess.run(["git", "-C", str(R1PKG), "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip())
R1_MANIFEST = "9dcb47f0ec3ec346b491d90c2836e3b30f54eb88fd5e4fbd216fc34782275cdb"
REVIEWED = "741dde19b5d07be1872e8bdcedaa90611cbf5b71"
R1REL = "bms-balancing/comsol_candidates/bmin_particle640_r1_20261005"
V1REL = "bms-balancing/comsol_candidates/bmin_particle640_20261004"
REVIEW = ROOT / "bms-balancing/reviews/r14_repros/codex63/comsol_bmin_r1_review_20261005/INDEPENDENT_STATIC_AUDIT.json"
SPEC_44_2 = "한도와 같으면 허용한다 (≤)"
checks = []


def sha(b):
    return hashlib.sha256(b).hexdigest()


def check(name, ok, detail=None):
    checks.append({"check": name, "status": "STATIC_MATCH" if ok else "FAIL", **({"detail": detail} if detail is not None else {})})
    return ok


def git_show(rev, rel):
    r = subprocess.run(["git", "-C", str(ROOT), "show", f"{rev}:{rel}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def lf(raw):
    return raw.decode("ascii").replace("\r\n", "\n")


def blocks(text, prefix):
    out, lines = {}, text.split("\n")
    idx = [i for i, ln in enumerate(lines) if ln.startswith(prefix)]
    for k, i in enumerate(idx):
        name = lines[i][len(prefix):].split("(")[0].split(" ")[0]
        out[name] = "\n".join(lines[i:idx[k + 1] if k + 1 < len(idx) else len(lines)])
    return out


# ── 4. 문자열 모형 (이 도구의 정규식 · 후보 소스의 네 문장과 글자 대조) ──────────────────────────────
PATTERN = r"Number of degrees of freedom solved for: (\d+) \(plus (\d+) internal DOFs\)\."
SOURCE_STATEMENTS = (
    "    pattern=r'" + PATTERN + "'",
    "    mentions=[x for x in section.splitlines() if 'Number of degrees of freedom' in x]",
    "    need(len(mentions)==1,'TRANSIENT_DOF_READBACK_COUNT:'+str(len(mentions)))",
    "    hit=re.fullmatch(r'\\s*'+pattern+r'\\s*',mentions[0]);need(hit is not None,'TRANSIENT_DOF_READBACK_FORMAT')",
    "    solved,internal=int(hit.group(1)),int(hit.group(2));need(solved>0,'TRANSIENT_DOF_READBACK_VALUE')",
)


def model(section, whole_line=True):
    mentions = [x for x in section.splitlines() if "Number of degrees of freedom" in x]
    if len(mentions) != 1:
        return f"TRANSIENT_DOF_READBACK_COUNT:{len(mentions)}"
    hit = re.fullmatch(r"\s*" + PATTERN + r"\s*", mentions[0]) if whole_line else re.search(PATTERN, mentions[0])
    if hit is None:
        return "TRANSIENT_DOF_READBACK_FORMAT"
    if int(hit.group(1)) <= 0:
        return "TRANSIENT_DOF_READBACK_VALUE"
    return f"PASS solved {hit.group(1)} internal {hit.group(2)}"


def main():
    bound = json.loads((PKG / "R2_CHANGE_BOUNDARIES.json").read_text(encoding="utf-8"))
    lit = json.loads((PKG / "R2_LITERAL_CHANGES.json").read_text(encoding="utf-8"))

    # 1. r1 — 검토받은 바이트 · r1 → v1 → NORMAL480 사슬
    listed = subprocess.run(["git", "-C", str(ROOT), "ls-tree", "-r", "--name-only", REVIEWED, "--", R1REL],
                            capture_output=True, text=True).stdout.split()
    changed = [rel for rel in listed if git_show(REVIEWED, rel) != (ROOT / rel).read_bytes()]
    check("r1 package = bytes at the reviewed commit 741dde19b", len(listed) > 15 and not changed, {"files": len(listed), "changed": changed})
    r1m = (R1 / "CODE_MANIFEST.json").read_bytes()
    check("r1 CODE_MANIFEST = 9dcb47f0…", sha(r1m) == R1_MANIFEST)
    r = subprocess.run([sys.executable, str(R1PKG / "tools/static_audit_r1.py")], capture_output=True, text=True)
    after = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--", R1REL, V1REL], capture_output=True, text=True).stdout.strip()
    check("r1 static audit re-run: 42 checks, 0 failed, rc 0 (it re-runs v1's 81: r1 -> v1 -> NORMAL480) and both STATIC_AUDIT.json unchanged",
          r.returncode == 0 and '"checks": 42, "failed": 0' in r.stdout and after == "", {"stdout": r.stdout.strip()[-120:], "git_status": after})

    # 2. r2 재생성 · r2 -> r1 역재구성
    r = subprocess.run([sys.executable, str(PKG / "tools/build_candidate_r2.py"), "--check"], capture_output=True, text=True)
    check("build_candidate_r2.py --check reproduces candidate/ and R2_LITERAL_CHANGES.json", r.returncode == 0,
          r.stdout.strip().splitlines()[-1:] + r.stderr.strip().splitlines()[-1:])
    regions = {}
    for rel, spec in bound["files"].items():
        if spec["kind"] == "JSON":
            continue
        raw, r1raw = (R2 / rel).read_bytes(), (R1 / rel).read_bytes()
        try:
            raw.decode("ascii")
            check(f"{rel} ASCII only", True)
        except UnicodeDecodeError:
            check(f"{rel} ASCII only", False)
        if spec["kind"] == "UNCHANGED":
            check(f"{rel} byte-identical to r1", raw == r1raw)
            continue
        check(f"{rel} all CRLF", raw.count(b"\r\n") == raw.count(b"\n") > 0)
        text, r1text, rr = lf(raw), lf(r1raw), []
        try:
            for op in spec["reverse"]:
                if op["op"] != "inverse_literals":
                    raise ValueError(f"unexpected op {op['op']}")
                for e in reversed(lit[op["table"]]):
                    if text.count(e["after"]) != e["count"]:
                        raise ValueError(f"literal count {e['after'][:50]!r}: {text.count(e['after'])} != {e['count']}")
                    text = text.replace(e["after"], e["before"])
                rr.append({"op": "inverse_literals", "entries": len(lit[op["table"]]), "occurrences": sum(e["count"] for e in lit[op["table"]])})
            ok = text == r1text
        except ValueError as e:
            ok = False
            rr.append({"error": str(e)})
        check(f"{rel}: undoing only the declared r2 changes gives the exact r1 bytes", ok)
        regions[rel] = rr

    # 3. 바뀌면 안 되는 부분 · 결속
    c1, c2 = lf((R1 / "src/diagnostic_consumer.py").read_bytes()), lf((R2 / "src/diagnostic_consumer.py").read_bytes())
    b1, b2 = blocks(c1, "def "), blocks(c2, "def ")
    same = sorted(n for n in b1 if n != "mesh_evidence" and b1[n] == b2.get(n))
    check("consumer: every function except mesh_evidence byte-identical to r1", set(b1) == set(b2) and len(same) == len(b1) - 1,
          {"identical": len(same)})
    me = b2["mesh_evidence"]
    check("consumer mesh_evidence: whole-line match once, no first-partial-match search left, three reason names kept",
          me.count("re.fullmatch(r'\\s*'+pattern+r'\\s*',mentions[0])") == 1 and "re.search(pattern,mentions[0])" not in c2
          and all(x in me for x in ("TRANSIENT_DOF_READBACK_COUNT", "TRANSIENT_DOF_READBACK_FORMAT", "TRANSIENT_DOF_READBACK_VALUE")))
    check("consumer mesh_evidence: record-only policy for a valid different value kept (same / difference / review_note / outside record)",
          all(x in me for x in ("'transient_dof_matches_expected':same", "'transient_dof_difference':", "'review_note':None if same else",
                                "'dof_outside_transient_section':outside")))
    m_raw = (R2 / "CODE_MANIFEST.json").read_bytes()
    m, mr1, msha = json.loads(m_raw), json.loads(r1m), sha(m_raw)
    diff_files = [f["file"] for f, g in zip(m["files"], mr1["files"]) if f != g]
    check("r2 manifest: flags false, previous = r1, five files with exact bytes, only the consumer entry differs from r1",
          m["approved"] is False and m["usable"] is False and m["previous_manifest_sha256"] == R1_MANIFEST
          and [f["file"] for f in m["files"]] == [f["file"] for f in mr1["files"]] and diff_files == ["src/diagnostic_consumer.py"]
          and all(len((R2 / f["file"]).read_bytes()) == f["bytes"] and sha((R2 / f["file"]).read_bytes()) == f["sha256"] for f in m["files"])
          and {k: v for k, v in m.items() if k not in ("previous_manifest_sha256", "files")} == {k: v for k, v in mr1.items() if k not in ("previous_manifest_sha256", "files")},
          {"differing_files": diff_files})
    for name in ("COMMAND_MAP.json", "NATIVE_APPROVAL_FIELD_SPEC.json"):
        a = (R2 / name).read_text(encoding="ascii")
        b = (R1 / name).read_text(encoding="ascii")
        check(f"{name}: r1 bytes with only the manifest SHA replaced", a == b.replace(R1_MANIFEST, msha) and msha in a and R1_MANIFEST not in a)

    # 4. 문자열 모형
    src_ok = all(c2.count(s + "\n") == 1 for s in SOURCE_STATEMENTS)
    check("string model: the consumer source carries the model's five statements verbatim (pattern, mentions, count, whole-line match, value)", src_ok)
    rev = json.loads(REVIEW.read_text(encoding="utf-8"))
    want = {"valid": "PASS solved 79485 internal 12", "two_lines": "TRANSIENT_DOF_READBACK_COUNT:2",
            "two_same_line": "TRANSIENT_DOF_READBACK_FORMAT", "valid_then_malformed_same_line": "TRANSIENT_DOF_READBACK_FORMAT",
            "zero": "TRANSIENT_DOF_READBACK_VALUE", "missing_internal": "TRANSIENT_DOF_READBACK_FORMAT"}
    table = []
    for case in rev["static_string_cases"]:
        r2v, r1v = model(case["text"]), model(case["text"], whole_line=False)
        table.append({"id": case["id"], "source": "re-review static_string_cases", "r1_rule": r1v, "r2_rule": r2v, "expected_r2": want.get(case["id"]),
                      "re_review_r1_prediction": case.get("statically_predicted_branch")})
    n480 = rev["normal480_dof"]["transient_mentions"][0]
    extra = [("whitespace_padded", " \t  Number of degrees of freedom solved for: 156925 (plus 12 internal DOFs).   \r\n", "PASS solved 156925 internal 12"),
             ("trailing_text", "Number of degrees of freedom solved for: 156925 (plus 12 internal DOFs). (retry 1)", "TRANSIENT_DOF_READBACK_FORMAT"),
             ("normal480_line_131", n480, "PASS solved 79485 internal 12")]
    for cid, text, exp in extra:
        table.append({"id": cid, "source": "r2 plan PY03-12 / PY03-13" if cid != "normal480_line_131" else "re-review normal480_dof (batch.log line 131)",
                      "r1_rule": model(text, whole_line=False), "r2_rule": model(text), "expected_r2": exp})
    check("string model: the six re-review cases and three r2 cases give the expected reasons under the r2 rule",
          len(table) == 9 and all(t["r2_rule"] == t["expected_r2"] for t in table), [t["id"] for t in table if t["r2_rule"] != t["expected_r2"]])
    check("string model: under the r1 rule the two same-line cases took the first value (the re-review finding, reproduced)",
          [t["r1_rule"] for t in table if t["id"] in ("two_same_line", "valid_then_malformed_same_line")] == ["PASS solved 79485 internal 12"] * 2)

    # 검증안
    plan = json.loads((PKG / "LIMITED_VALIDATION_PLAN.json").read_text(encoding="utf-8"))
    r1plan = json.loads((R1PKG / "LIMITED_VALIDATION_PLAN.json").read_text(encoding="utf-8"))
    cases = {c["id"]: c for g in plan["groups"] for c in g["cases"]}
    r1cases = {c["id"]: c for g in r1plan["groups"] for c in g["cases"]}
    per_group = {g["id"]: len(g["cases"]) for g in plan["groups"]}
    check("validation plan: bound to the r2 manifest, approvals false, still a proposal", plan["manifest_sha256"] == msha
          and plan["approved"] is False and plan["usable"] is False and plan["status"] == "PROPOSAL_NO_TESTS_RUN")
    check("validation plan: 62 unique IDs (Python 39 + Java helper 2 + PowerShell 21) in 9 groups",
          plan["cases"] == len(cases) == sum(per_group.values()) == 62 and plan["logical_groups"] == len(per_group) == 9
          and per_group == {"PY01": 4, "PY02": 5, "PY03": 14, "PY04": 3, "PY05": 7, "PY06": 4, "PY07": 2, "JV01": 2, "PS01": 21}, per_group)
    multi_ok = all((c["inputs"] == 1 and "input_expectations" not in c) or (c["inputs"] == len(c.get("input_expectations", [])) >= 2)
                   for c in cases.values())
    check("validation plan: 77 inputs; every multi-input ID lists one expected reason per input", plan["inputs"] == 77
          == sum(c["inputs"] for c in cases.values()) and multi_ok)
    kept = [i for i, c in r1cases.items() if i != "PS01-16" and (cases[i]["fixture"], cases[i]["expected"]) != (c["fixture"], c["expected"])]
    check("validation plan: the 54 r1 IDs are kept with r1 fixture / expected text except the declared C1 edit of PS01-16",
          set(r1cases) <= set(cases) and not kept, kept)
    new_ids = {"PY03-11", "PY03-12", "PY03-13", "PY03-14", "PS01-18", "PS01-19", "PS01-20", "PS01-21"}
    check("validation plan: the r2 IDs are exactly PY03-11..14 and PS01-18..21", set(cases) - set(r1cases) == new_ids)
    ps16 = cases["PS01-16"]
    texts = [x for c in cases.values() for x in (c["fixture"], c["expected"])]
    check("validation plan: PS01-16 = 30 decimal places / 28 significant digits, out of the exact-equality item, in precision_mismatch_items",
          "30 decimal places (28 significant digits)" in ps16["fixture"] and not any("31 significant" in t for t in texts)
          and "PS01-16" not in plan["v2_section_8_required_items"]["value exactly equal to a limit"]
          and list(plan["precision_mismatch_items"].values()) == [["PS01-16"]])
    causes = {"PS01-12": "NATIVE_CHILD_RC", "PS01-13": "TERMINATION_EVIDENCE_MISSING", "PS01-14": "CONSUMER_NATIVE_LABEL_MISMATCH",
              "PS01-18": "NATIVE_CHILD_RETURN_MISSING_OR_ERROR", "PS01-19": "RESULT_IDENTITY", "PS01-20": "TERMINATION_EVIDENCE_INVALID",
              "PS01-21": "NATIVE_AXIS_NOT_EVALUATED"}
    p2 = (R2 / "PARENT_COMMAND.ps1").read_bytes().decode("ascii")
    check("validation plan: each of the seven native-axis cause names in the parent has its own PowerShell case",
          all(cause in cases[i]["expected"] and cause in p2 for i, cause in causes.items()))
    check("validation plan: the consumer DOF value path (solved 0) has its own Python case", "TRANSIENT_DOF_READBACK_VALUE" in cases["PY03-14"]["expected"])
    bud = plan["budget_seconds"]
    check("validation plan: budget parts sum to the overall 1,660 s and the sessions match", sum(v for k, v in bud.items() if k != "overall")
          == bud["overall"] == 1660 and plan["sessions"]["python"]["seconds"] == bud["python"]
          and plan["sessions"]["windows_powershell_5_1"]["seconds"] == bud["powershell"])
    check("validation plan: harness not written, preseal items listed", plan["harness_sha256"] is None and len(plan["preseal_before_first_test"]) >= 5)
    docs = {n: (PKG / n).read_text(encoding="utf-8") for n in ("PREPARATION_KO.md", "VALIDATION_REQUEST_KO.md", "NATIVE_BMIN640_APPROVAL_DRAFT_KO.md")}
    check("r2 documents name the r2 manifest SHA", all(msha in v for v in docs.values()), [n for n, v in docs.items() if msha not in v])
    check("r2 documents carry the SPEC section 44-2 sentence", all(SPEC_44_2 in v for v in docs.values()))
    check("r2 preparation / request state 30 decimal places and 28 significant digits, and 62 IDs / 77 inputs / 1,660 s",
          all("소수점 아래 30 자리" in docs[n] and "유효숫자 28 자리" in docs[n] and "62" in docs[n] and "77" in docs[n] and "1,660" in docs[n]
              for n in ("PREPARATION_KO.md", "VALIDATION_REQUEST_KO.md")))
    check("R2_CHANGE_BOUNDARIES c1_wording states 30 decimal places (28 significant digits)",
          "30 decimal places (28 significant digits)" in bound["c1_wording"])

    failed = [x for x in checks if x["status"] != "STATIC_MATCH"]
    out = {"kind": "SOURCE_TEXT_JSON_HASH_DIFF_ONLY", "candidate_manifest_sha256": msha, "previous_manifest_sha256": R1_MANIFEST,
           "checks_total": len(checks), "checks_failed": len(failed), "candidate_imports": 0, "candidate_parse_compile_tests": 0,
           "JVM_COMSOL_gate_calls": 0, "native_compatibility": "UNTESTED", "functional_status": "UNTESTED",
           "reverse_reconstruction_r2_to_r1": regions,
           "static_string_model": {"kind": "AUDIT_OWNED_REGEX_MODEL_NOT_CANDIDATE_EXECUTION", "rule_r1": "re.search (first partial match)",
                                   "rule_r2": "re.fullmatch with surrounding whitespace allowed", "cases": table},
           "checks": checks}
    (PKG / "STATIC_AUDIT.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"checks": len(checks), "failed": len(failed), "manifest": msha}, ensure_ascii=False))
    for x in failed:
        print("FAIL", x["check"], x.get("detail"))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
