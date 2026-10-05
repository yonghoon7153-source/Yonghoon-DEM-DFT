"""B-min 후보 r2 — r1 (manifest 9dcb47f0…) 에서 재검토 회신의 국소 보완 (BMIN-R1-N1) 만 결정적으로 적용한다.
텍스트 치환만 — 후보 코드의 import · 구문 해석 · 컴파일 · 실행 0.

  python3 tools/build_candidate_r2.py            # r2 꾸러미 루트 (comsol_candidates/bmin_particle640_r2_20261005) 에서
  python3 tools/build_candidate_r2.py --check    # 쓰지 않고 지금 candidate/ 와 R2_LITERAL_CHANGES.json 이 이 결과와 같은지만 본다

입력: ../bmin_particle640_r1_20261005/candidate/ (r1 — CODE_MANIFEST 와 5 파일 · 결속 두 파일 바이트를 먼저 대조, 다르면 멈춘다).
바뀌는 것: src/diagnostic_consumer.py (mesh_evidence 안 두 자리 — transient DOF 줄의 전체 줄 문법 · 그 정책 문구) · 봉인 셋 (manifest SHA).
그대로: src/Bmin640Candidate.java · src/candidate_entry.py · PARENT_COMMAND.ps1 · CONTRACT.json (바이트 동일).
"""
import hashlib
import json
import pathlib
import sys

PKG = pathlib.Path(__file__).resolve().parent.parent
R1 = PKG.parent / "bmin_particle640_r1_20261005" / "candidate"
OUT = PKG / "candidate"
R1_MANIFEST = "9dcb47f0ec3ec346b491d90c2836e3b30f54eb88fd5e4fbd216fc34782275cdb"
R1_SIDE = {"COMMAND_MAP.json": "f1381cb781b2de507052b595c913a0d9f7428b8fe261c4d1d22df6877f0833f6",
           "NATIVE_APPROVAL_FIELD_SPEC.json": "ddeb04ab6efe1006d4df21a7c1435b1974b649f11438973e9928d37caaaaa416"}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def stop(msg):
    raise SystemExit("✗ " + msg)


def apply(text, table, label):
    for before, after, count, _finding in table:
        got = text.count(before)
        if got != count:
            stop(f"{label}: {before[:60]!r} 횟수 {got} ≠ {count}")
        text = text.replace(before, after)
    return text


def crlf_text(raw, label):
    if raw.count(b"\r\n") != raw.count(b"\n") or b"\r\n" not in raw:
        stop(f"{label}: r1 이 전부 CRLF 가 아니다")
    return raw.decode("ascii").replace("\r\n", "\n")


# (이전, 이후, 횟수, 발견) — consumer mesh_evidence 안 (LF 로 바꾼 텍스트 위에서 · 결과는 다시 CRLF)
CONSUMER_LITERALS = [
    ("    hit=re.search(pattern,mentions[0]);need(hit is not None,'TRANSIENT_DOF_READBACK_FORMAT')\n",
     "    # BMIN-R1-N1: the whole line must be one DOF statement (surrounding whitespace allowed); a second statement or any trailing text on that line is malformed.\n"
     "    hit=re.fullmatch(r'\\s*'+pattern+r'\\s*',mentions[0]);need(hit is not None,'TRANSIENT_DOF_READBACK_FORMAT')\n", 1, "BMIN-R1-N1"),
    ("'dof_policy':'I-3: exactly one well-formed DOF line inside the single Time-Dependent Solver section is required (missing, outside-only, "
     "ambiguous or malformed is incomplete); a difference from the extrapolated expectation is recorded, not a gate.'}",
     "'dof_policy':'I-3: exactly one DOF line inside the single Time-Dependent Solver section is required and its whole content (surrounding "
     "whitespace allowed) must be one well-formed DOF statement (missing, outside-only, ambiguous - two lines or two statements on one line - "
     "or malformed, including trailing text, is incomplete); a difference from the extrapolated expectation is recorded, not a gate.'}",
     1, "BMIN-R1-N1"),
]


def dump(obj):
    return (json.dumps(obj, indent=2, ensure_ascii=True) + "\n").encode("ascii")


def main():
    check_only = "--check" in sys.argv[1:]
    r1m_raw = (R1 / "CODE_MANIFEST.json").read_bytes()
    if sha(r1m_raw) != R1_MANIFEST:
        stop("r1 CODE_MANIFEST 바이트 불일치")
    r1m = json.loads(r1m_raw)
    r1 = {}
    for f in r1m["files"]:
        b = (R1 / f["file"]).read_bytes()
        if len(b) != f["bytes"] or sha(b) != f["sha256"]:
            stop(f"r1 바이트 불일치: {f['file']}")
        r1[f["file"]] = b
    for name, h in R1_SIDE.items():
        b = (R1 / name).read_bytes()
        if sha(b) != h:
            stop(f"r1 바이트 불일치: {name}")
        r1[name] = b

    # BMIN-R1-N1 — consumer (두 자리 · 다른 함수 · 부모 · Java · entry · CONTRACT 는 바이트 그대로)
    c_text = apply(crlf_text(r1["src/diagnostic_consumer.py"], "consumer"), CONSUMER_LITERALS, "consumer")
    consumer = c_text.replace("\n", "\r\n").encode("ascii")

    files = [("src/Bmin640Candidate.java", r1["src/Bmin640Candidate.java"]), ("src/diagnostic_consumer.py", consumer),
             ("src/candidate_entry.py", r1["src/candidate_entry.py"]), ("PARENT_COMMAND.ps1", r1["PARENT_COMMAND.ps1"]),
             ("CONTRACT.json", r1["CONTRACT.json"])]
    if [f for f, _ in files] != [f["file"] for f in r1m["files"]]:
        stop("manifest 파일 순서")
    manifest_obj = dict(r1m)
    manifest_obj["previous_manifest_sha256"] = R1_MANIFEST
    manifest_obj["files"] = [{"file": f, "bytes": len(raw), "sha256": sha(raw)} for f, raw in files]
    if manifest_obj["approved"] is not False or manifest_obj["usable"] is not False:
        stop("승인 플래그")
    manifest = dump(manifest_obj)
    msha = sha(manifest)

    cmd = json.loads(r1["COMMAND_MAP.json"])
    cmd["manifest_sha256"] = msha
    for k in ("parent", "execute", "analyze"):
        if cmd[k]["argv"][-1] != R1_MANIFEST:
            stop(f"command map argv {k}")
        cmd[k]["argv"][-1] = msha
    if R1_MANIFEST in json.dumps(cmd):
        stop("command map 에 r1 manifest 가 남았다")
    spec = json.loads(r1["NATIVE_APPROVAL_FIELD_SPEC.json"])
    spec["code_manifest_sha256"] = msha
    if R1_MANIFEST in json.dumps(spec):
        stop("field spec 에 r1 manifest 가 남았다")
    if dump(cmd) != r1["COMMAND_MAP.json"].replace(R1_MANIFEST.encode(), msha.encode()):
        stop("command map 직렬화가 r1 바이트의 SHA 치환과 다르다")
    if dump(spec) != r1["NATIVE_APPROVAL_FIELD_SPEC.json"].replace(R1_MANIFEST.encode(), msha.encode()):
        stop("field spec 직렬화가 r1 바이트의 SHA 치환과 다르다")

    outputs = {
        "src/Bmin640Candidate.java": r1["src/Bmin640Candidate.java"], "src/candidate_entry.py": r1["src/candidate_entry.py"],
        "src/diagnostic_consumer.py": consumer, "PARENT_COMMAND.ps1": r1["PARENT_COMMAND.ps1"], "CONTRACT.json": r1["CONTRACT.json"],
        "CODE_MANIFEST.json": manifest, "COMMAND_MAP.json": dump(cmd), "NATIVE_APPROVAL_FIELD_SPEC.json": dump(spec),
    }
    literal_doc = {"from": "../bmin_particle640_r1_20261005/candidate (r1 · manifest " + R1_MANIFEST + " · reviewed at commit 741dde19b)",
                   "to": "candidate (r2)",
                   "src/diagnostic_consumer.py": [{"before": b0, "after": a0, "count": n, "finding": k} for b0, a0, n, k in CONSUMER_LITERALS],
                   "unchanged_bytes": ["src/Bmin640Candidate.java", "src/candidate_entry.py", "PARENT_COMMAND.ps1", "CONTRACT.json"],
                   "binding_only": {"CODE_MANIFEST.json": "previous_manifest_sha256 = r1 manifest; size / SHA-256 of the consumer",
                                    "COMMAND_MAP.json": "manifest SHA only", "NATIVE_APPROVAL_FIELD_SPEC.json": "manifest SHA only"}}
    package_outputs = {"R2_LITERAL_CHANGES.json": (json.dumps(literal_doc, indent=2, ensure_ascii=False) + "\n").encode("utf-8")}
    bad = []
    for rel, raw in list(outputs.items()) + list(package_outputs.items()):
        p = (PKG if rel in package_outputs else OUT) / rel
        if check_only:
            if not p.is_file() or p.read_bytes() != raw:
                bad.append(rel)
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(raw)
        print(f"{'✗' if rel in bad else ('=' if check_only else '+')} {rel:36s} {len(raw):>9,d} B  {sha(raw)}")
    print(f"manifest {msha}")
    if bad:
        stop(f"재생성 바이트 불일치 {len(bad)}: {bad}")


if __name__ == "__main__":
    main()
