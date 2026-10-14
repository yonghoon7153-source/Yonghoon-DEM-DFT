#!/usr/bin/env python3
"""site_dg.py — 자리 비교 2 단계: UMA 어닐 결과 → 모델별 최저 · ΔG_site(UMA) (조성 균형 · Li₂S/Li₃PS₄ 교환)

  ΔG_site = { [E(M@P) − E(M@Li)] − [a·e(Li₂S) + b·e(Li₃PS₄)] } / n_M        (eV / 도펀트 · > 0 ⇒ P 자리 불리)
  M@P − M@Li 의 조성차를 a·Li₂S + b·Li₃PS₄ 로 **정확히** 닫는다 (P 로 b · S 로 a · Li 검산 · 다른 원소 차 0).
  이번 캠페인의 두 모델은 n·(+5 Li −1 P) = n·(4 Li₂S − Li₃PS₄) 다 (a = 4n · b = −n).
  카드: db/properties/b2o3_site_screen_estimand_2026_10_14.json · db/properties/ndo_lpscl16_site_stability_estimand_2026_10_14.json

입력
  --anneal  run_anneal.py 의 anneal_results.json (여러 개) — 이름 [M]MP_ii · [M]MLi_ii · [M]host_ii
  --refs    기준상 이완 (run_uma_kgy.sh --refs) 의 anneal_results.json
  종류는 이름으로, 도펀트는 조성 (Li P S O Cl 밖의 원소) 으로 가른다. 조성은 각 레코드의 post_relax.xyz 에서 센다
  (그래서 결과 폴더가 있는 기계 — kgy — 에서 돌린다).

게이트 (카드가 결과 전에 정한 것 중 기계로 볼 수 있는 것만)
  · 오류 레코드 · 미수렴 이완이 하나라도 있으면 ΔG 를 내지 않는다 (B 카드 G1 '다 있어야 계산한다').
    --allow_incomplete 면 그것들을 빼고 내되 뺀 이름을 찍는다.
  · --expect N: 모델마다 N 개 (오류 · 미수렴 포함 셈) 가 있어야 한다.
  · 같은 모델 안 조성이 다르면 · 조성차가 Li₂S/Li₃PS₄ 로 안 닫히면 · 도펀트 수가 다르면 멈춘다.
  · 모델별 최저와 둘째의 차를 찍는다 (B G3).
  · --thresholds: |ΔG| 가 판정 문턱에서 0.11 eV 안이면 '다형 재확인 발동' (B G4 · Nd G7 · 0.11 = MP 다형 차 0.0138 eV/atom × 8).
    'B=0.20 Nd=0' 처럼 도펀트별로, 또는 '0.20' 처럼 전부에.

⛔ 이 도구가 못 하는 것
  · 판정 문장을 쓰지 않는다 — 허용 · 금지 서술은 카드에서만 가져온다.
  · UMA 가 맞는지 모른다 (UMA 내부 비교다) · DFT 를 하지 않는다.
  · 최저가 진짜 바닥인지 모른다 — 모델마다 같은 탐색 예산 (N 개) 안의 최저다.
  · 저장소는 Li₂S/Li₃PS₄ 교환 하나다 (회신 BG — 다른 μ 꼭짓점은 안 본다).
  · Li₃PS₄ 다형을 스스로 바꾸지 않는다 — --refs 에 준 다형 하나를 쓴다.

  종료 코드: 0 모든 도펀트 ΔG 냄 · 3 하나라도 거절 (위 게이트 · 화면에 이유) · 1 멈춤 (⛔ 조성 · 기준상 · 이름 이상)
  --out · --bundle 파일은 화면 출력 **전에** 쓴다 (출력이 끊겨도 남는다).

  python3 site_dg.py --selftest
  python3 site_dg.py --anneal $R/uma_anneal/anneal_results.json --refs $R/uma_ref_relax/anneal_results.json \
      --expect 10 --top 3 --out $R/site_dg_rietveld.json --bundle <폴더>
"""
import argparse
import hashlib
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

HOST_EL = {"Li", "P", "S", "O", "Cl"}
NAME = re.compile(r"^(?P<pre>[A-Za-z]*?)(?P<kind>MP|MLi|host)_(?P<i>\d+)$")
POLY_MARGIN = 0.11          # eV/도펀트 — 카드 B G4 · Nd G7
KIND_LABEL = {"MP": "M@P", "MLi": "M@Li"}


def _read_comp(path):
    from ase.io import read
    return Counter(read(path).get_chemical_symbols())


def formula(c):
    return "".join(f"{e}{c[e]}" for e in sorted(c))


def ref_energies(records, comp=_read_comp):
    """기준상 레코드 → {'Li2S': e/f.u., 'Li3PS4': e/f.u.} — 오류 · 미수렴 · 조성 이상 · 빠짐은 멈춘다."""
    e = {}
    for r in records:
        if "error" in r:
            raise SystemExit(f"⛔ 기준상 {r['name']} 오류: {r['error']}")
        if not r.get("converged"):
            raise SystemExit(f"⛔ 기준상 {r['name']} 이완 미수렴")
        c = comp(r["post_relax_xyz"])
        if set(c) == {"Li", "S"} and c["Li"] == 2 * c["S"]:
            f, n = "Li2S", c["S"]
        elif set(c) == {"Li", "P", "S"} and c["Li"] == 3 * c["P"] and c["S"] == 4 * c["P"]:
            f, n = "Li3PS4", c["P"]
        else:
            raise SystemExit(f"⛔ 기준상 {r['name']}: 조성 {formula(c)} 이 Li2S · Li3PS4 가 아니다")
        if f in e:
            raise SystemExit(f"⛔ 기준상 {f} 가 둘이다")
        e[f] = r["E_post_relax"] / n
    if set(e) != {"Li2S", "Li3PS4"}:
        raise SystemExit(f"⛔ 기준상 Li2S · Li3PS4 가 다 있어야 한다 (있는 것 {sorted(e)})")
    return e


def close_with_refs(cP, cLi):
    """cP − cLi = a·Li2S + b·Li3PS4 를 정확히 푼다. 안 닫히면 ValueError."""
    d = Counter(cP)
    d.subtract(cLi)
    other = {k: v for k, v in d.items() if k not in ("Li", "P", "S") and v}
    if other:
        raise ValueError(f"Li P S 밖의 원소 차 {other}")
    b = d["P"]
    a = d["S"] - 4 * b
    if 2 * a + 3 * b != d["Li"]:
        raise ValueError(f"Li 가 안 맞는다 (차 Li {d['Li']} · P {d['P']} · S {d['S']})")
    return a, b


def classify(records, comp=_read_comp):
    """레코드 → ({(도펀트, 종류): [레코드]}, 오류 이름들). 이름 · 조성이 안 맞으면 멈춘다."""
    groups, errors = {}, []
    for r in records:
        if "error" in r:
            errors.append(r["name"])
            continue
        m = NAME.match(r["name"])
        if not m:
            raise SystemExit(f"⛔ 이름 {r['name']} 이 [M]MP_ii · [M]MLi_ii · [M]host_ii 꼴이 아니다")
        c = comp(r["post_relax_xyz"])
        dop = sorted(set(c) - HOST_EL)
        if m["kind"] == "host":
            if dop:
                raise SystemExit(f"⛔ {r['name']}: host 이름인데 도펀트 {dop}")
            key = ("host", "host")
        else:
            if len(dop) != 1:
                raise SystemExit(f"⛔ {r['name']}: 도펀트 원소가 하나가 아니다 {dop}")
            if m["pre"] and m["pre"] != dop[0]:
                raise SystemExit(f"⛔ {r['name']}: 이름 앞머리 {m['pre']} 와 조성의 도펀트 {dop[0]} 가 다르다")
            key = (dop[0], m["kind"])
        groups.setdefault(key, []).append(dict(r, _comp=c))
    return groups, errors


def parse_thresholds(items):
    out = {}
    for it in items or []:
        k, _, v = it.rpartition("=")
        out[k or "*"] = float(v)
    return out


def analyze(anneal_records, ref_records, expect=None, allow_incomplete=False, top=3,
            thresholds=None, comp=_read_comp):
    """→ 요약 dict. 판정 문장은 없다 — 숫자 · 게이트 표지만."""
    eref = ref_energies(ref_records, comp)
    groups, errors = classify(anneal_records, comp)
    thr = thresholds or {}
    out = {"refs_eV_per_fu": eref,
           "reservoir_4Li2S_minus_Li3PS4_eV": 4 * eref["Li2S"] - eref["Li3PS4"],
           "error_records": errors, "dopants": {}, "hosts": []}
    for r in sorted(groups.get(("host", "host"), []), key=lambda r: r["E_post_relax"]):
        out["hosts"].append({"name": r["name"], "E_eV": r["E_post_relax"], "converged": r["converged"],
                             "formula": formula(r["_comp"]), "post_relax_xyz": r["post_relax_xyz"]})
    for dop in sorted({k[0] for k in groups if k[0] != "host"}):
        blk = {"models": {}, "refusals": []}
        if errors and not allow_incomplete:
            blk["refusals"].append(f"오류 레코드 {len(errors)} 개 ({' '.join(errors)}) — 다 있어야 계산한다")
        mins = {}
        for kind in ("MP", "MLi"):
            recs = groups.get((dop, kind), [])
            if not recs:
                blk["refusals"].append(f"{KIND_LABEL[kind]} 후보 0 개")
                continue
            forms = {formula(r["_comp"]) for r in recs}
            if len(forms) != 1:
                raise SystemExit(f"⛔ {dop} {KIND_LABEL[kind]}: 같은 모델 안 조성이 다르다 {sorted(forms)}")
            bad = [r["name"] for r in recs if not r.get("converged")]
            if bad and not allow_incomplete:
                blk["refusals"].append(f"{KIND_LABEL[kind]} 미수렴 {len(bad)} 개 ({' '.join(bad)})")
            n_err = sum(1 for nm in errors if (m := NAME.match(nm)) and m["kind"] == kind and m["pre"] in ("", dop))
            if expect is not None and len(recs) + n_err != expect:
                blk["refusals"].append(f"{KIND_LABEL[kind]} {len(recs) + n_err} 개 (--expect {expect})")
            # 미수렴은 --allow_incomplete 일 때만 뺀다 — 아니면 표에 남기고 (위에서) ΔG 를 거절한다
            use = sorted((r for r in recs if r.get("converged") or not allow_incomplete),
                         key=lambda r: r["E_post_relax"])
            if not use:
                blk["refusals"].append(f"{KIND_LABEL[kind]} 쓸 후보 0 개")
                continue
            e0 = use[0]["E_post_relax"]
            blk["models"][kind] = {
                "formula": forms.pop(), "n": len(recs), "n_converged": len(recs) - len(bad),
                "excluded_unconverged": bad if allow_incomplete else [],
                "gap_min_second_eV": (use[1]["E_post_relax"] - e0) if len(use) > 1 else None,
                "top": [r["name"] for r in use[:top]],
                "ranked": [{"name": r["name"], "E_eV": r["E_post_relax"], "dE_from_min_eV": r["E_post_relax"] - e0,
                            "converged": r["converged"], "n_relax_steps": r.get("n_relax_steps"),
                            "post_relax_xyz": r["post_relax_xyz"]} for r in use]}
            mins[kind] = use[0]
        if set(mins) == {"MP", "MLi"}:
            cP, cL = mins["MP"]["_comp"], mins["MLi"]["_comp"]
            if cP[dop] != cL[dop]:
                raise SystemExit(f"⛔ {dop}: 두 모델의 도펀트 수가 다르다 ({cP[dop]} · {cL[dop]})")
            try:
                a, b = close_with_refs(cP, cL)
            except ValueError as ex:
                raise SystemExit(f"⛔ {dop}: 조성차가 Li₂S/Li₃PS₄ 로 안 닫힌다 — {ex}")
            n = cP[dop]
            blk["closure"] = {"a_Li2S": a, "b_Li3PS4": b, "n_dopant": n}
            if not blk["refusals"]:
                dg = (mins["MP"]["E_post_relax"] - mins["MLi"]["E_post_relax"]
                      - (a * eref["Li2S"] + b * eref["Li3PS4"])) / n
                blk["dG_site_eV_per_dopant"] = dg
                ts = [thr[k] for k in (dop, "*") if k in thr]
                blk["polymorph_recheck"] = [{"threshold": t, "distance": abs(abs(dg) - t),
                                             "triggered": abs(abs(dg) - t) <= POLY_MARGIN} for t in ts]
        out["dopants"][dop] = blk
    return out


def report(s):
    print(f"== 기준상 e(Li₂S) {s['refs_eV_per_fu']['Li2S']:.5f} · e(Li₃PS₄) {s['refs_eV_per_fu']['Li3PS4']:.5f} eV/f.u. "
          f"· 저장소 항 4·e(Li₂S) − e(Li₃PS₄) = {s['reservoir_4Li2S_minus_Li3PS4_eV']:.5f} eV")
    if s["error_records"]:
        print(f"   ⛔ 오류 레코드: {' '.join(s['error_records'])}")
    for dop, b in s["dopants"].items():
        cl = b.get("closure")
        print(f"== {dop}" + (f" (n {cl['n_dopant']} · 조성차 = {cl['a_Li2S']} Li₂S {cl['b_Li3PS4']:+d} Li₃PS₄ ✓)" if cl else ""))
        for kind, m in b["models"].items():
            gap = "—" if m["gap_min_second_eV"] is None else f"{m['gap_min_second_eV']:+.4f}"
            print(f"   {KIND_LABEL[kind]:<5} {m['formula']} · {m['n']} 개 (수렴 {m['n_converged']}) · "
                  f"최저 {m['ranked'][0]['name']} · 둘째와 차 {gap} eV · 상위 {' '.join(m['top'])}")
            if m["excluded_unconverged"]:
                print(f"         ⚠ 미수렴 빼고 계산: {' '.join(m['excluded_unconverged'])}")
            print("         " + " · ".join(f"{x['name']} {x['dE_from_min_eV']:+.3f}" for x in m["ranked"]))
        for why in b["refusals"]:
            print(f"   ⛔ ΔG 안 냄 — {why}")
        if "dG_site_eV_per_dopant" in b:
            print(f"   ΔG_site(UMA) = {b['dG_site_eV_per_dopant']:+.3f} eV/{dop}  (> 0 ⇒ P 자리 불리 · UMA 내부 · Li₃PS₄/Li₂S 교환 기준)")
            for p in b["polymorph_recheck"]:
                print(f"   문턱 {p['threshold']:.2f} 과의 거리 {p['distance']:.3f} eV → 다형 재확인 "
                      + ("**발동** (Li₃PS₄ 다른 다형 둘도 이완)" if p["triggered"] else "안 함"))
    for h in s["hosts"]:
        print(f"   host {h['name']} {h['formula']} · 수렴 {h['converged']}")


def bundle(s, inputs, dest):
    """결과 json · 요약 · 모든 post_relax.xyz 를 한 폴더로 (repo 에 올리기용)."""
    dest = Path(dest)
    (dest / "structures").mkdir(parents=True, exist_ok=True)
    for p in inputs:
        p = Path(p)
        shutil.copy2(p, dest / f"{p.parent.name}.anneal_results.json")
        for r in json.loads(p.read_text())["results"]:
            if "post_relax_xyz" in r and Path(r["post_relax_xyz"]).exists():
                shutil.copy2(r["post_relax_xyz"], dest / "structures" / f"{r['name']}.xyz")
    (dest / "site_dg_summary.json").write_text(json.dumps(s, indent=1, ensure_ascii=False, default=str))
    return dest


def _selftest():
    import tempfile
    import numpy as np
    from ase import Atoms
    from ase.io import write
    ok = []

    def chk(c, m):
        ok.append(bool(c))
        print(("  ✓ " if c else "  ✗ ") + m)

    def expect_exit(fn, m):
        try:
            fn()
        except SystemExit as ex:
            chk(str(ex).startswith("⛔"), m + f" → {str(ex)[:70]}")
        else:
            chk(False, m + " → 멈추지 않았다")

    tmp = Path(tempfile.mkdtemp())
    rng = np.random.default_rng(0)

    def xyz(name, form):
        sym = [e for e, k in re.findall(r"([A-Z][a-z]?)(\d+)", form) for _ in range(int(k))]
        p = tmp / f"{name}.xyz"
        write(p, Atoms(sym, positions=rng.random((len(sym), 3)) * 20, cell=[20] * 3, pbc=True))
        return str(p)

    def rec(name, form, E, conv=True):
        return {"name": name, "E_post_relax": E, "converged": conv, "n_relax_steps": 10,
                "post_relax_xyz": xyz(name, form)}

    P, L = "Cl8Li31Nd2O3P3S19", "Cl8Li21Nd2O3P5S19"
    refs = [rec("li2s", "Li2S1", -12.0), rec("li3ps4", "Li12P4S16", -140.0)]       # e = −12 · −35 → 저장소 −13
    base = [rec("MP_00", P, -400.0), rec("MP_01", P, -399.9), rec("MLi_00", L, -374.5), rec("MLi_01", L, -374.0),
            rec("host_00", "Cl8Li27P5S20", -300.0)]
    s = analyze(base, refs, expect=2, thresholds={"*": 0.20})
    b = s["dopants"]["Nd"]
    chk(abs(s["reservoir_4Li2S_minus_Li3PS4_eV"] + 13.0) < 1e-12, "저장소 항 4(−12) − (−35) = −13")
    chk(abs(b.get("dG_site_eV_per_dopant", 9) - 0.25) < 1e-12, "ΔG = [(−400 + 374.5) − 2·(−13)] / 2 = +0.25")
    chk(b["closure"] == {"a_Li2S": 8, "b_Li3PS4": -2, "n_dopant": 2}, "조성차 = 8 Li₂S − 2 Li₃PS₄ · n 2")
    chk(abs(b["models"]["MP"]["gap_min_second_eV"] - 0.1) < 1e-9 and b["models"]["MP"]["top"][0] == "MP_00", "최저 · 둘째 차")
    chk(b["polymorph_recheck"][0]["triggered"], "|0.25 − 0.20| ≤ 0.11 → 다형 재확인 발동")
    s2 = analyze(base, refs, thresholds={"Nd": 0.50, "B": 0.0})
    chk(not s2["dopants"]["Nd"]["polymorph_recheck"][0]["triggered"], "도펀트별 문턱 0.50 → 거리 0.25 · 안 함")
    chk(len(s["hosts"]) == 1, "host 는 ΔG 밖 목록")
    # 음성 — 막아야 하는 것
    s3 = analyze(base[:1] + [rec("MP_02", P, -401.0, conv=False)] + base[1:], refs)
    chk("dG_site_eV_per_dopant" not in s3["dopants"]["Nd"] and s3["dopants"]["Nd"]["refusals"], "미수렴 있으면 ΔG 안 냄")
    s4 = analyze(base[:1] + [rec("MP_02", P, -401.0, conv=False)] + base[1:], refs, allow_incomplete=True)
    chk(abs(s4["dopants"]["Nd"]["dG_site_eV_per_dopant"] - 0.25) < 1e-12
        and s4["dopants"]["Nd"]["models"]["MP"]["excluded_unconverged"] == ["MP_02"],
        "--allow_incomplete: 미수렴 (더 낮아도) 빼고 계산 · 뺀 이름 기록")
    s5 = analyze(base + [{"name": "MLi_02", "error": "CUDA OOM"}], refs)
    chk("dG_site_eV_per_dopant" not in s5["dopants"]["Nd"], "오류 레코드 있으면 ΔG 안 냄")
    s6 = analyze(base, refs, expect=3)
    chk("dG_site_eV_per_dopant" not in s6["dopants"]["Nd"], "--expect 3 인데 2 개 → ΔG 안 냄")
    expect_exit(lambda: analyze(base + [rec("MP_03", L, -1.0)], refs), "같은 모델 안 조성 다름")
    expect_exit(lambda: analyze([rec("MP_00", "Cl8Li31Nd2O4P3S18", -1.0)] + base[2:], refs), "조성차가 안 닫힘 (O 차)")
    expect_exit(lambda: analyze(base, refs[:1]), "기준상 Li₃PS₄ 빠짐")
    expect_exit(lambda: analyze(base, [refs[0], rec("li3ps4", "Li12P4S16", -140.0, conv=False)]), "기준상 미수렴")
    expect_exit(lambda: analyze([rec("BMP_00", P, -1.0)] + base[1:], refs), "이름 앞머리 B 인데 조성은 Nd")
    expect_exit(lambda: analyze([rec("MP_00", "Cl8Li31Nd2O3P3S19Y1", -1.0)] + base[1:], refs), "도펀트 원소 둘")
    print(f"selftest: {sum(ok)}/{len(ok)}")
    return 0 if all(ok) else 1


def main():
    if "--selftest" in sys.argv[1:]:
        return _selftest()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--anneal", nargs="+", required=True)
    ap.add_argument("--refs", required=True)
    ap.add_argument("--expect", type=int)
    ap.add_argument("--allow_incomplete", action="store_true")
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--thresholds", nargs="*", default=[])
    ap.add_argument("--out")
    ap.add_argument("--bundle")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    recs = [r for p in a.anneal for r in json.loads(Path(p).read_text())["results"]]
    refs = json.loads(Path(a.refs).read_text())["results"]
    s = analyze(recs, refs, a.expect, a.allow_incomplete, a.top, parse_thresholds(a.thresholds))
    s["inputs"] = {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in a.anneal + [a.refs]}
    s["args"] = {"expect": a.expect, "allow_incomplete": a.allow_incomplete, "top": a.top, "thresholds": a.thresholds}
    # 파일을 **먼저** 쓴다 — 화면 출력이 `| head` 등으로 끊겨도 (BrokenPipe) 요약 · 묶음은 남게 (로컬 시험에서 묶음이 통째로 빠졌다)
    if a.out:
        Path(a.out).write_text(json.dumps(s, indent=1, ensure_ascii=False, default=str))
    dest = bundle(s, a.anneal + [a.refs], a.bundle) if a.bundle else None
    report(s)
    if a.out:
        print(f"   요약 → {a.out}")
    if dest:
        print(f"   묶음 → {dest}")
    refused = [d for d, b in s["dopants"].items() if "dG_site_eV_per_dopant" not in b]
    if refused or not s["dopants"]:
        print(f"   ⛔ ΔG 를 못 낸 도펀트: {' '.join(refused) or '(후보 없음)'} — 종료 3")
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
