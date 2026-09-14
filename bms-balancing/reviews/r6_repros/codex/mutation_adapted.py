"""고친 코드를 하나씩 되돌리면 **Codex 의 probe(적응판)** 가 다시 '열림' 을 봐야 한다.

`replay_codex_r6_adapted.py` 는 닫힌 트리에서 전부 '닫힘' 이다 — 그것만으로는 probe 가 **아무것도 못 재는** 상태인지
구분이 안 된다. 그래서 수정 조각을 되돌리고 같은 probe 를 다시 돌린다. 되돌린 자리에서 해당 probe 가 '열림' 이면
그 probe 는 실제로 그 성질을 재고 있는 것이다. 트리는 매번 원상복구한다 (finally).

    python3 reviews/r6_repros/codex/mutation_adapted.py     # bms-balancing 에서
"""
from __future__ import annotations
import json, pathlib, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parents[3]               # bms-balancing
ADAPTED = pathlib.Path(__file__).resolve().parent / "replay_codex_r6_adapted.py"

MUTATIONS = [
    ("R6-01 read_unit 이 검증 뒤 경로를 다시 읽는다", "R6-01a", "scripts/provenance.py",
     "    ok, why = verify_unit_bytes(p.name, data, meta, rid)\n    return ok, why, data, meta",
     "    ok, why = verify_unit_bytes(p.name, data, meta, rid)\n    return ok, why, p.read_bytes(), meta"),
    ("R6-01 독자가 스냅샷 뒤 행을 다시 읽는다", "R6-01b", "scripts/compare_states.py",
     "        all_rows = list(csv.DictReader(io.StringIO(data.decode(\"utf-8-sig\"))))",
     "        all_rows = list(csv.DictReader(io.StringIO(f.read_bytes().decode(\"utf-8-sig\"))))"),
    ("R6-02 현행 산출 + meta 없음 → 옛 산출로", "R6-02", "scripts/provenance.py",
     "    if meta is None:\n        if modern:\n            return False,",
     "    if meta is None:\n        if False:\n            return False,"),
    ("R6-03 ne_shape 이 반쪽전지를 다시 열어 해시", "R6-03a", "scripts/ne_shape.py",
     "                    \"half_cell\": hb[s].identity()}",
     "                    \"half_cell\": {\"path\": hb[s].path, \"sha256\": __import__('hashlib').sha256(pathlib.Path(hb[s].path).read_bytes()).hexdigest()}}"),
    # d431404 의 모양 그대로 되돌린다: 로더가 읽은 뒤 **호출한 쪽**이 경로를 다시 열어 해시 (R6-03 의 원래 자리)
    ("R6-03 build 가 로더 뒤에 경로로 해시", "R6-03b", "bms_balancing/verify.py",
     "    c, v = D.load_full_cell(root, state, workbook=wb, identity=fc_id)",
     "    c, v = D.load_full_cell(root, state, workbook=wb)\n    import hashlib as _h\n    fc_id.update({\"path\": str(wb), \"sha256\": _h.sha256(wb.read_bytes()).hexdigest()})"),
]


def run_adapted():
    with tempfile.NamedTemporaryFile(suffix=".json") as out:
        subprocess.run([sys.executable, str(ADAPTED), "--target", str(ROOT), "--output", out.name],
                       capture_output=True, text=True)
        return {k.split()[0]: v["상태"] for k, v in json.loads(pathlib.Path(out.name).read_text(encoding="utf-8"))["probes"].items()}


def main() -> int:
    base = run_adapted()
    print("baseline:", json.dumps(base, ensure_ascii=False))
    assert all(s == "닫힘" for s in base.values()), base
    missed = 0
    for what, probe, rel, old, new in MUTATIONS:
        p = ROOT / rel; bak = p.read_bytes()
        try:
            s = p.read_text(encoding="utf-8")
            assert s.count(old) == 1, (rel, s.count(old))
            p.write_text(s.replace(old, new), encoding="utf-8")
            got = run_adapted().get(probe)
            ok = got == "열림"
            print(("CAUGHT " if ok else "MISSED ") + f"| {what} | {probe} → {got}")
            missed += (not ok)
        finally:
            p.write_bytes(bak)
    after = run_adapted()
    print("restored:", json.dumps(after, ensure_ascii=False))
    assert all(s == "닫힘" for s in after.values()), after
    print("MISSED:", missed)
    return 1 if missed else 0


if __name__ == "__main__":
    sys.exit(main())
