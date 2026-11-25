"""cascade 축 ③ 판독기 + 세 축 합치기 (analyze_cathode_reactivity.py --axis_li · ax_combine) 변이 검사 — 저장소 밖 복사본에서 규칙을 하나씩 되돌려
--selftest 가 빨개지는지 본다. --dry : 자리만 확인."""
import pathlib, shutil, subprocess, sys, os

SP = pathlib.Path("/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/mut_li")
REPO = pathlib.Path("/home/user/Yonghoon-DEM-DFT")
REL = "tools/cascade/analyze_cathode_reactivity.py"
MUT = [
 ("L1_alloy_rule_off", [("    if el and not (set(el) & AX_NONMETAL):\n        return \"metallic\", (\"원소 금속\"", "    if el and len(el) == 1 and not (set(el) & AX_NONMETAL):\n        return \"metallic\", (\"원소 금속\"")]),
 ("L2_anion_list_narrow", [("    if el and not (set(el) & AX_NONMETAL):\n        return \"metallic\", (\"원소 금속\"", "    if el and not (set(el) & {\"O\", \"S\", \"Cl\", \"P\"}):\n        return \"metallic\", (\"원소 금속\"")]),
 ("L3_classify_not_passed", [("        cls, det = ax_design_class(r, trk, gaps, classify=li_product_class)", "        cls, det = ax_design_class(r, trk, gaps)")]),
 ("L4_g1b_products_off", [("        g1b = {\"ok\": bool(h[\"dE_eV_per_atom\"] < 0 and prods is not None and all(have.values())),", "        g1b = {\"ok\": bool(h[\"dE_eV_per_atom\"] < 0),")]),
 ("L5_g1b_sign_off", [("        g1b = {\"ok\": bool(h[\"dE_eV_per_atom\"] < 0 and prods is not None and all(have.values())),", "        g1b = {\"ok\": bool(prods is not None and all(have.values())),")]),
 ("L6_has_ratio_off", [("        if c and set(c) == set(want) and all(abs(c[k] - want[k]) <= 1e-6 for k in want):", "        if c and set(c) == set(want):")]),
 ("L7_f1_off", [("                     \"F1_Li\": cls == \"metallic\", \"F2_Li\": d_ <= -LIA[\"delta_meV\"],", "                     \"F1_Li\": False, \"F2_Li\": d_ <= -LIA[\"delta_meV\"],")]),
 ("L8_f2_sign", [("                     \"F1_Li\": cls == \"metallic\", \"F2_Li\": d_ <= -LIA[\"delta_meV\"],", "                     \"F1_Li\": cls == \"metallic\", \"F2_Li\": d_ <= LIA[\"delta_meV\"],")]),
 ("L9_unknown_narrow", [("                     \"unknown\": cls in (\"undetermined\", \"na\", \"fate_error\")})", "                     \"unknown\": cls in (\"undetermined\", \"na\")})")]),
 ("L10_g4_flip", [("                   \"discriminates\": (q3 - q1) >= LIA[\"iqr_meV\"], \"method\"", "                   \"discriminates\": (q3 - q1) < LIA[\"iqr_meV\"], \"method\"")]),
 ("L11_g7_never_overlap", [("               \"overlap\": None if rho is None else abs(rho) >= LIA[\"rho_overlap\"],", "               \"overlap\": None if rho is None else abs(rho) >= 2.0,")]),
 ("L12_gaps_check_off", [("    if not (isinstance(L.get(\"gaps\"), dict) and isinstance(L[\"gaps\"].get(\"gaps\"), dict)):\n        prob.append(", "    if False:\n        prob.append(")]),
 ("L13_formula_check_off", [("        elif rs[0].get(\"formula\") != expected[sp]:\n            prob.append(f\"{sp} × Li: 조성", "        elif False:\n            prob.append(f\"{sp} × Li: 조성")]),
 ("L14_host_row_check_off", [("    if h is None:\n        prob.append(\"HOST × Li: 정상 행 하나가 아니다\")", "    if False:\n        prob.append(\"HOST × Li: 정상 행 하나가 아니다\")")]),
 ("L15_g5_off", [("    miss5 = [t for t in LI_CARD_TEXT if t not in (card_text or \"\")]", "    miss5 = []")]),
 ("L16_decision_off", [("    G = {\"decision\": {\"ok\": decision_state == \"active\" and decision_card == \"db/properties/\" + LI_CARD.name,", "    G = {\"decision\": {\"ok\": True,")]),
 ("L17_g3_off", [("    G[\"G3\"] = {\"ok\": man.get(\"same_mp_version\") is True and vb not in (None, \"\") and vb == va, \"before\": vb, \"after\": va}\n    ixd, ixh = ax_index(L.get(\"designs_li\"))",
                   "    G[\"G3\"] = {\"ok\": True, \"before\": vb, \"after\": va}\n    ixd, ixh = ax_index(L.get(\"designs_li\"))")]),
 ("L18_combine_li_flags_off", [("            fl += [f for f, c in ((\"축③F1_Li금속성\", ld[s_][\"F1_Li\"]), (\"축③F2_Li반응증가\", ld[s_][\"F2_Li\"])) if c]", "            fl += []")]),
 ("L19_combine_li_g7_ignored", [("        if li[\"gates\"].get(\"G4\", {}).get(\"discriminates\") and g7l.get(\"overlap\") is False:", "        if li[\"gates\"].get(\"G4\", {}).get(\"discriminates\"):")]),
 ("L20_combine_li_blocking_off", [("    if li is not None and li.get(\"blocking\"):", "    if False:")]),
 ("L21_full_reduction_max", [("    k = min(inner, key=lambda d: d[\"x\"])", "    k = max(inner, key=lambda d: d[\"x\"])")]),
 ("L22_pair_class_off", [("                      \"differs\": bool(abs(dd) >= LIA[\"delta_meV\"] or a[\"class\"] != b[\"class\"])})", "                      \"differs\": bool(abs(dd) >= LIA[\"delta_meV\"])})")]),
 ("L23_tool_drift_off", [("            miss.append(f\"물리 도구 sha 가 실행마다 다르거나 없다 ({t})\")\n    G[\"G1\"] = {\"ok\": not miss and not L[\"problems\"], \"missing\": miss, \"load_problems\": L[\"problems\"][:10]}\n    vb, va = man.get(\"mp_db_version_before\"), man.get(\"mp_db_version_after\")\n    G[\"G3\"] = {\"ok\": man.get(\"same_mp_version\") is True and vb not in (None, \"\") and vb == va, \"before\": vb, \"after\": va}\n    ixd, ixh = ax_index(L.get(\"designs_li\"))",
                          "            pass\n    G[\"G1\"] = {\"ok\": not miss and not L[\"problems\"], \"missing\": miss, \"load_problems\": L[\"problems\"][:10]}\n    vb, va = man.get(\"mp_db_version_before\"), man.get(\"mp_db_version_after\")\n    G[\"G3\"] = {\"ok\": man.get(\"same_mp_version\") is True and vb not in (None, \"\") and vb == va, \"before\": vb, \"after\": va}\n    ixd, ixh = ax_index(L.get(\"designs_li\"))")]),
 ("L24_dopant_products_all", [("        dop = [f for f in prods if set(_ax_pf(f)) & set(trk)]", "        dop = list(prods)")]),
]


def main():
    src = (REPO / REL).read_text(encoding="utf-8")
    bad = [f"{n}: 자리 {src.count(o)} 개" for n, reps in MUT for o, _ in reps if src.count(o) != 1]
    if bad:
        print("\n".join(bad)); return 2
    print(f"변이 {len(MUT)} 개 · 자리 모두 한 번씩", flush=True)
    if "--dry" in sys.argv:
        return 0
    if SP.exists():
        shutil.rmtree(SP)
    (SP / "tools").mkdir(parents=True)
    shutil.copytree(REPO / "tools", SP / "tools", dirs_exist_ok=True)
    os.symlink(REPO / "db", SP / "db")
    f = SP / REL
    n_red = 0
    for name, reps in MUT:
        s = src
        for o, nw in reps:
            s = s.replace(o, nw, 1)
        f.write_text(s, encoding="utf-8")
        r = subprocess.run([sys.executable, str(f), "--selftest"], capture_output=True, text=True, timeout=600, cwd=str(SP))
        out = r.stdout + r.stderr
        reds = [ln for ln in out.splitlines() if ln.startswith("  ⛔ ")]
        red = r.returncode != 0
        n_red += red
        print(f"{name:<30s} {'⭕ 빨강' if red else '⛔ 초록 (못 잡음)'} · {(reds[0][:120] if reds else out.strip().splitlines()[-1][:120])}", flush=True)
    f.write_text(src, encoding="utf-8")
    print(f"끝: 빨강 {n_red} / {len(MUT)}")
    return 0 if n_red == len(MUT) else 1


if __name__ == "__main__":
    raise SystemExit(main())
