#!/usr/bin/env python3
"""cascade_f9adc9d2_codex_review_repro.py — Codex f9 리뷰 숫자 재현 (읽기 전용).

    python3 docs/reviews/cascade_f9adc9d2_codex_review_repro.py            # 현재 워킹트리
    python3 docs/reviews/cascade_f9adc9d2_codex_review_repro.py f9adc9d2   # 동결본

기대 출력:
    family 253 17
    raised 17 / 253 vs 11 / 17
    exact ratio 9.629757... one decimal 9.6
    eligible slots 33 champions 16 17 ratio 2.588235...
    matched 10 unmatched 7
    G2 43 algorithmic G3 25 18 attribution 24 18 1

이 스크립트가 **못 하는 것**
  · 값이 왜 그런지는 말하지 않는다. 숫자가 리뷰와 같은지만 본다.
  · 인과 해석을 하지 않는다 — 두 비율 모두 사후 기술통계다.
"""
import csv, io, json, subprocess, sys


def main():
    rev = sys.argv[1] if len(sys.argv) > 1 else None

    def blob(path):
        if rev:
            return subprocess.check_output(["git", "show", f"{rev}:{path}"]).decode("utf-8-sig")
        return open(path, encoding="utf-8-sig").read()

    rows = list(csv.DictReader(io.StringIO(blob("db/properties/cascade_v23_all.csv"))))
    champ = [r for r in rows if r.get("rank_combined") == "1"]
    plain = [r for r in champ if r["charge_compensation"] == "compound_set"]
    chain = [r for r in champ if r["charge_compensation"] == "compound_set_chain"]
    gp = json.loads(blob("db/properties/oxidation_stability_cascade_v3_pinned.json"))["results"]
    raised = lambda r: (gp[r["name"]]["delta_ox_vs_host_V"] or 0) > 0

    print("family", len(plain), len(chain))
    np_, nc = sum(map(raised, plain)), sum(map(raised, chain))
    ratio = (nc / len(chain)) / (np_ / len(plain))
    print("raised", np_, "/", len(plain), "vs", nc, "/", len(chain))
    print("exact ratio", ratio, "one decimal", round(ratio, 1))

    base = lambda s: s[:-len("+Clrich")] if s.endswith("+Clrich") else s
    slot = lambda r: (base(r["dopant"]), r["concentration_label"])
    eligible = {slot(r) for r in rows if r["charge_compensation"] == "compound_set_chain"}
    ech = [r for r in champ if slot(r) in eligible]
    ep = [r for r in ech if r["charge_compensation"] == "compound_set"]
    ec = [r for r in ech if r["charge_compensation"] == "compound_set_chain"]
    er = (sum(map(raised, ec)) / len(ec)) / (sum(map(raised, ep)) / len(ep))
    print("eligible slots", len(eligible), "champions", len(ep), len(ec), "ratio", er)

    els = [k[len("composition_"):] for k in rows[0] if k.startswith("composition_")]
    v = lambda r, e: float(r.get("composition_" + e) or 0)
    want = {"Li": -1, "S": -1, "Cl": 1}
    paired, unpaired = [], []
    for c in chain:
        ps = [p for p in rows
              if base(p["dopant"]) == base(c["dopant"])
              and p["charge_compensation"] == "compound_set"]
        ok = any(all(abs((v(c, e) - v(p, e)) - want.get(e, 0)) < 1e-9 for e in els) for p in ps)
        (paired if ok else unpaired).append(c["name"])
    print("matched", len(paired), "unmatched", len(unpaired))
    for name in unpaired:
        print(" ", name)

    funnel = json.loads(blob("db/properties/cascade_screening_funnel.json"))
    g2 = [r for r in funnel["pool"] if "G2" in r["gates_passed"]]
    g3 = [r for r in g2 if "G3" in r["gates_passed"]]
    unres = {r["dopant"] for r in g3 if r.get("ox_family_confounded")}
    print("G2", len(g2), "algorithmic G3", len(g3), len(g2) - len(g3),
          "attribution", len(g3) - len(unres), len(g2) - len(g3), len(unres))


if __name__ == "__main__":
    main()
