"""cascade 축 ② 판독기 + 합치는 규칙 (analyze_cathode_reactivity.py --axis_hyd · ax_combine) 변이 검사 — 저장소 밖 복사본에서 규칙을 하나씩 되돌려
--selftest 가 빨개지는지 본다. --dry : 자리만 확인."""
import pathlib, shutil, subprocess, sys, os

SP = pathlib.Path("/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/mut_hy")
REPO = pathlib.Path("/home/user/Yonghoon-DEM-DFT")
REL = "tools/cascade/analyze_cathode_reactivity.py"
MUT = [
 ("H1_h2s_any_HS", [("        n_h2s = sum(c for c, f in parse_side(rhs) if _ax_pf(f) == {\"H\": 2.0, \"S\": 1.0})",
                     "        n_h2s = sum(c for c, f in parse_side(rhs) if \"H\" in _ax_pf(f) and \"S\" in _ax_pf(f))")]),
 ("H2_design_term_check_off", [("        if len(hit) != 1 or not hit[0][1].get(\"S\"):\n            return None, \"좌변에서 설계 항을", "        if False:\n            return None, \"좌변에서 설계 항을")]),
 ("H4_g1b_h2s_off", [("        g1b = {\"ok\": bool(h[\"dE_eV_per_atom\"] < 0 and fh is not None and fh > 0),", "        g1b = {\"ok\": bool(h[\"dE_eV_per_atom\"] < 0),")]),
 ("H5_g1b_sign_off", [("        g1b = {\"ok\": bool(h[\"dE_eV_per_atom\"] < 0 and fh is not None and fh > 0),", "        g1b = {\"ok\": bool(fh is not None and fh > 0),")]),
 ("H6_f1_sign", [("\"F1_hyd\": d_ <= -HY[\"delta_meV\"]", "\"F1_hyd\": d_ <= HY[\"delta_meV\"]")]),
 ("H7_f2_off", [("\"F2_H2S\": bool(df_ is not None and df_ >= HY[\"df_flag\"])", "\"F2_H2S\": False")]),
 ("H8_g4_flip", [("\"iqr_meV\": round(q3 - q1, 2), \"discriminates\": (q3 - q1) >= HY[\"iqr_meV\"],", "\"iqr_meV\": round(q3 - q1, 2), \"discriminates\": (q3 - q1) < HY[\"iqr_meV\"],")]),
 ("H9_g7_never_overlap", [("               \"overlap\": None if rho is None else abs(rho) >= HY[\"rho_overlap\"],", "               \"overlap\": None if rho is None else abs(rho) >= 2.0,")]),
 ("H10_flags_ignored", [("    cand = [r for r in rows if not r[\"flags\"]]", "    cand = rows")]),
 ("H11_pareto_flip", [("        return any(all(o[k] >= r[k] for k in keys) and any(o[k] > r[k] for k in keys) for o in cand if o is not r)",
                       "        return any(all(o[k] <= r[k] for k in keys) and any(o[k] < r[k] for k in keys) for o in cand if o is not r)")]),
 ("H12_r4_off", [("    if len(axes) < 2:\n        out.update({\"selection\": None, \"rule\": \"R4", "    if len(axes) < 1:\n        out.update({\"selection\": None, \"rule\": \"R4")]),
 ("H13_g7_ignored", [("    if hyd[\"gates\"].get(\"G4\", {}).get(\"discriminates\") and g7.get(\"overlap\") is False:", "    if hyd[\"gates\"].get(\"G4\", {}).get(\"discriminates\"):")]),
 ("H14_pair_f_off", [("\"differs\": bool(abs(dd) >= HY[\"delta_meV\"] or (dfp is not None and abs(dfp) >= HY[\"pair_df\"]))})", "\"differs\": bool(abs(dd) >= HY[\"delta_meV\"])})")]),
 ("H15_g5_off", [("    G[\"G5\"] = {\"ok\": not miss5, \"missing_in_card\": miss5, \"card_sha256\": hashlib.sha256((card_text or \"\").encode(\"utf-8\")).hexdigest()}\n    return G\n\n\ndef _zhu_dg",
                  "    G[\"G5\"] = {\"ok\": True, \"missing_in_card\": miss5, \"card_sha256\": hashlib.sha256((card_text or \"\").encode(\"utf-8\")).hexdigest()}\n    return G\n\n\ndef _zhu_dg")]),
 ("H16_decision_off", [("    G = {\"decision\": {\"ok\": decision_state == \"active\" and decision_card == \"db/properties/\" + HYD_CARD.name,", "    G = {\"decision\": {\"ok\": True,")]),
 ("H17_formula_check_off", [("        elif rs[0].get(\"formula\") != expected[sp]:\n            prob.append(f\"{sp} × H2O: 조성", "        elif False:\n            prob.append(f\"{sp} × H2O: 조성")]),
 ("H18_tool_drift_off", [("        if len(v) != 1 or None in v:\n            miss.append(f\"물리 도구 sha 가 실행마다 다르거나 없다 ({t})\")", "        if False:\n            miss.append(f\"물리 도구 sha 가 실행마다 다르거나 없다 ({t})\")")]),
 ("H19_host_row_check_off", [("    if h is None:\n        prob.append(\"HOST × H2O: 정상 행 하나가 아니다\")", "    if False:\n        prob.append(\"HOST × H2O: 정상 행 하나가 아니다\")")]),
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
