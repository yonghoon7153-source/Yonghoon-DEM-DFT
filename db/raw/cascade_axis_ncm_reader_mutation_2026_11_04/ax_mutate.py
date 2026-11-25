"""cascade 축 ① 판독기 (analyze_cathode_reactivity.py --axis_ncm) 변이 검사 — 저장소 밖 복사본에서 규칙을 하나씩 되돌려
--selftest 가 빨개지는지 본다. --dry : 자리만 확인."""
import pathlib, shutil, subprocess, sys, os

SP = pathlib.Path("/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/mut_ax")
REPO = pathlib.Path("/home/user/Yonghoon-DEM-DFT")
REL = "tools/cascade/analyze_cathode_reactivity.py"
MUT = [
 ("A1_tracked_keeps_cathode_tm", [("    return sorted(set(_ax_pf(formula)) - AX_HOST_ELEMS - ({tm} if tm else set()))", "    return sorted(set(_ax_pf(formula)) - AX_HOST_ELEMS)")]),
 ("A5_tm_rule_off", [("    if set(el) & AX_TM_U:\n        return \"undetermined\", \"+U", "    if False:\n        return \"undetermined\", \"+U")]),
 ("A6_elemental_metal_off", [("    if len(el) == 1 and next(iter(el)) not in AX_NONMETAL:", "    if False:")]),
 ("A7_4f_rule_off", [("    if set(el) & AX_4F:", "    if False:")]),
 ("A8_g4_flip", [("\"discriminates\": (q3 - q1) >= AX[\"iqr_meV\"]}", "\"discriminates\": (q3 - q1) < AX[\"iqr_meV\"]}")]),
 ("A9_g1b_order_off", [("and AX[\"anchor_lo\"] <= rh <= AX[\"anchor_hi\"] and h_ < f_),", "and AX[\"anchor_lo\"] <= rh <= AX[\"anchor_hi\"]),")]),
 ("A10_g1b_ratio_off", [("        g1b = {\"ok\": bool(f_ < 0 and h_ < 0 and AX[\"anchor_lo\"] <= rf <= AX[\"anchor_hi\"]", "        g1b = {\"ok\": bool(f_ < 0 and h_ < 0 and True")]),
 ("A11_dup_allowed", [("            if len(rs) != 1 or not _ax_ok(rs[0]):\n                prob.append(f\"{sp} × {st}: 행", "            if not rs or not _ax_ok(rs[0]):\n                prob.append(f\"{sp} × {st}: 행")]),
 ("A12_mode_ignored", [("and isinstance(r.get(\"reaction\"), str) and r.get(\"mode\") == \"closed_0V\")", "and isinstance(r.get(\"reaction\"), str))")]),
 ("A13_g3_version_off", [("and vb not in (None, \"\") and vb == va,", "and vb not in (None, \"\"),")]),
 ("A14_g5_off", [("    G[\"G5\"] = {\"ok\": not miss5,", "    G[\"G5\"] = {\"ok\": True,")]),
 ("A15_decision_off", [("    G = {\"decision\": {\"ok\": decision_state == \"active\" and", "    G = {\"decision\": {\"ok\": True or decision_state == \"active\" and")]),
 ("A16_mass_balance_off", [("            if nl <= 0 or nr <= 0 or abs(nr - nl) > 0.01 * nl:", "            if nl <= 0 or nr <= 0:")]),
 ("A17_r4_sign_off", [("            r4 = bool(cls_c != cls_l or (abs(d_lh) >= AX[\"delta_meV\"] and abs(d_ch) >= AX[\"delta_meV\"] and (d_lh > 0) != (d_ch > 0)))", "            r4 = bool(cls_c != cls_l)")]),
 ("A18_r5_class_off", [("\"differs\": bool(abs(dd) >= AX[\"delta_meV\"] or co != cs)", "\"differs\": bool(abs(dd) >= AX[\"delta_meV\"])")]),
 ("A19_endpoint_off", [("    if ep is True:\n        return \"no_reaction\"", "    if False:\n        return \"no_reaction\"")]),
 ("A20_g6_bounds_off", [("    ok6 = all(v is not None and AX[\"proxy_lo\"] <= v <= AX[\"proxy_hi\"] for v in rat.values())", "    ok6 = all(v is not None for v in rat.values())")]),
 ("A21_load_problems_off", [("    G[\"G1\"] = {\"ok\": not miss and not L[\"problems\"],", "    G[\"G1\"] = {\"ok\": not miss,")]),
 ("A22_formula_check_off", [("            elif rs[0].get(\"formula\") != expected[sp]:", "            elif False:")]),
 ("A23_tool_drift_off", [("    if drift:\n        miss.append(", "    if False:\n        miss.append(")]),
 ("A24_roster_conflict_off", [("            if f.setdefault(r[\"species\"], r[\"formula\"]) != r[\"formula\"]:\n                raise ValueError", "            if False:\n                raise ValueError")]),
 ("A25_wide_before_metal", [("    if any(s[\"metallic\"] >= AX[\"frac_metal\"] for s in raw):\n        cls = \"metallic\"\n    elif all(s[\"wide\"] >= AX[\"frac_wide\"] for s in raw):\n        cls = \"wide\"",
                             "    if all(s[\"wide\"] >= AX[\"frac_wide\"] for s in raw):\n        cls = \"wide\"\n    elif any(s[\"metallic\"] >= AX[\"frac_metal\"] for s in raw):\n        cls = \"metallic\"")]),
 ("A26_frac_wide_085", [("\"frac_wide\": 0.90,", "\"frac_wide\": 0.85,")]),
 ("A27_metal_eV_0", [("AX = {\"wide_eV\": 2.0, \"metal_eV\": 0.1,", "AX = {\"wide_eV\": 2.0, \"metal_eV\": 0.0,")]),
 ("A28_extra_species_ok", [("    if extra:\n        prob.append(f\"카드에 없는 종", "    if False:\n        prob.append(f\"카드에 없는 종")]),
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
