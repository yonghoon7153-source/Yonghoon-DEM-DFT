"""Static text and byte comparison for the S1-O v2 prereview only."""
from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent / "microshort_s1o_prereview_20261007"
FILES = [
    Path("C:/Users/Administrator/Downloads/COMSOL_MICROSHORT_S1O_SEND_TO_CODEX_v2_20261007.md"),
    Path("C:/Users/Administrator/Downloads/COMSOL_MICROSHORT_S1O_SEND_TO_CODEX_20261007.md"),
    OLD / "S1O_CLARIFICATION_ADDENDUM_KO.md",
    OLD / "REVIEW_KO.md",
    OLD / "DECISION.json",
]
def digest(data):
    return hashlib.sha256(data).hexdigest()
def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
def save(name, value):
    with (ROOT / name).open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
data = [path.read_bytes() for path in FILES]
identities = [{"path":str(path), "bytes":len(raw), "sha256":digest(raw)} for path, raw in zip(FILES,data)]
remote = {}
for key, filename in [("v2","REQUEST_PINNED.json"),("v1","V1_PINNED.json"),("annex","ADDENDUM_PINNED.json")]:
    item=json.loads((ROOT/"reference"/filename).read_text(encoding="utf-8"))
    raw=item["content"].encode("utf-8")
    if blob(raw)!=item["sha"]:
        raise RuntimeError("Git blob mismatch " + key)
    remote[key]=raw
v2, v1, annex = data[:3]
checks = {
    "attachment_matches_pinned_v2_bytes": v2 == remote["v2"],
    "prior_attachment_matches_pinned_v1_bytes": v1 == remote["v1"],
    "reviewer_annex_matches_repo_preserved_bytes": annex == remote["annex"],
}
begin = "첨부 문서·실행 코드는".encode("utf-8")
v1body = v1[v1.index(begin):v1.rindex(b"\n---")].rstrip(b"\r\n")
v2body = v2[v2.index(begin):v2.index("\n## 6.".encode())].rstrip(b"\r\n")
checks["v1_sections_0_through_5_body_bytes_unchanged"] = v1body == v2body
opening=b"````markdown\n"
start = v2.index(opening) + len(opening)
end = v2.index(b"\n````", start)
embedded = v2[start:end]
# Fence separator whitespace is not part of the quoted source.
checks["embedded_annex_exact_original_bytes"] = embedded == annex
checks["explicit_section6_precedence"] = "위 §1–§5 와 다르면 이 절이 우선".encode() in v2
checks["original_total_budget_and_stage_caps"] = "전체 3600 s — 작성 1800 · 정적 점검 600 · 검증안 · 연결 설계 900 · 전달 300".encode() in v2
checks["no_test_authorization_and_native_ready_false"] = all(t.encode() in v2 for t in ["합성 검증 **실행**", "실제 approval/release/token/runtime/USER_DECISION은 생성하지 않는다", "native_ready=false를 유지한다"])
result = {
    "kind":"REVIEWER_STATIC_DOCUMENT_COMPARISON",
    "source_ref":json.loads((ROOT/"reference"/"PROVENANCE.json").read_text())["ref"],
    "checks":checks,
    "v1_body_sha256":digest(v1body),
    "v2_inherited_body_sha256":digest(v2body),
    "embedded_annex_bytes":len(embedded),
    "embedded_annex_sha256":digest(embedded),
    "original_annex_bytes":len(annex),
    "original_annex_sha256":digest(annex),
    "body_boundary_note":"Inherited body excludes outer headers/delimiters and trailing blank-line separators.",
    "scope":"Text and byte checks only; not candidate functionality, physical simulation or native verification.",
}
save("INPUT_IDENTITIES.json",identities)
save("STATIC_COMPARISON.json",result)
for path,raw in zip(FILES,data):
    if path.read_bytes()!=raw: raise RuntimeError("Input changed")
print(json.dumps(result,ensure_ascii=False))
if not all(checks.values()):
    raise SystemExit(1)

