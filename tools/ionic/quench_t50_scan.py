#!/usr/bin/env python3
"""quench_t50_scan.py — 담금질 궤적에서 T₅₀ (Li 이동 비율이 0.5 를 지나는 온도 · 저희 조작 정의) 을 낸다.

왜 있나 (2026-10-19 · li2s 회신 CX Q-CX-3d ①)
  'B 중앙 408 K − A ≈ 384 K = +24 K 라 100 K 사전 문장에 닿지 않는다' 가 A **한 시드** 대 B 다섯 시드 위에 서 있다.
  A 나머지 네 시드를 같은 정의로 낸다. B 다섯 (2026-10-13 · repo_checks/t50_scan_B.json) 과 A seed1 (09-21 스캔) 은
  세션 안 손 계산이었고 도구가 저장소에 없었다 → 같은 명령을 그대로 부르는 도구로 묶고, **옛 기록을 재현하는지부터** 본다
  (대조 잡 · 상시 절차 · CLAUDE.md 코드 규율).

정의 (B 기록 `method` 그대로)
  궤적을 50 ps 창으로 나눠 (0–50, 50–100, …) 창마다
    tools/ionic/aimd_jump_stats.py --save_fs 1000 --t_from_ps a --t_to_ps a+50 --hop_census_lag_ps 5.0 --hop_min_dist 2.0 --hop_events_all
  → `<label>_hop_census.json` 의 frac_moved (n_moved / n_Li) · 창 T = thermo.csv `T_set_K` 의 창 **양 끝 평균**.
  0.5 를 지나는 곳을 이웃 두 창 사이 T 로 선형 보간 · 교차가 하나면 T₅₀ · 둘 이상이면 T₅₀ 없음 (전부 적는다).

  python3 tools/ionic/quench_t50_scan.py --traj A/seed2/traj.xyz --thermo A/seed2/thermo.csv --label A_s2 --out t50_A_s2.json
  python3 tools/ionic/quench_t50_scan.py --control_B      # B 다섯을 저장소 궤적으로 다시 내 t50_scan_B.json 과 대조
  python3 tools/ionic/quench_t50_scan.py --control_A1 --traj <kgy A/seed1/traj.xyz> --thermo <같은 폴더 thermo.csv>
                                                           # A seed1 을 09-21 스캔 표 (21 창) 와 대조 — 창마다 이동 수 · p90
  대조 잡 (상시 · 회신 CX): 시드를 새로 내기 전에 그 기계에서 옛 기록 하나를 먼저 재현한다 — gabia 는 --control_B
  (궤적이 저장소에 있다) · kgy 는 --control_A1 (A seed1 궤적이 kgy 에만 있다). ✗ 면 그 기계에서 A 를 내지 않는다.
  python3 tools/ionic/quench_t50_scan.py --selftest

⛔ 이 도구가 못 하는 것
  · 평형 D 가 아니다 — 비평형 NPT 램프의 이동 비율이다 (B 기록 '⛔' 그대로). Tg 도 아니다 (저희 조작 정의).
  · 이동 판정은 aimd_jump_stats.py 의 hop_census (lag 5 ps · 2.0 Å) 가 한다 — 이 도구는 부르고 모을 뿐이다.
  · 교차가 둘 이상이면 하나를 고르지 않는다 (None + 전부 기록).
"""
import argparse
import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
JUMP = REPO / "tools" / "ionic" / "aimd_jump_stats.py"
B_RECORD = REPO / "db/raw/lpscl_glass_control_li3ps4_2026_10_05/repo_checks_2026_10_13/t50_scan_B.json"
A1_RECORD = REPO / "db/properties/lpscl_smallcell_quench_scan_2026_09_21.json"   # A seed1 · 21 창 표 (V100 · 09-21)
A1_BYTES = 20139827          # 같은 기록 '1_무엇을_스캔했나' — kgy A/seed1/traj.xyz 크기 (다른 파일이면 대조가 아니다)
WIN_PS, LAG_PS, MIN_DIST, LEVEL, SAVE_FS = 50.0, 5.0, 2.0, 0.5, 1000.0


def read_tset(thermo):
    """thermo.csv → {t_ps (반올림 3 자리): T_set_K}."""
    out = {}
    with open(thermo) as f:
        for row in csv.DictReader(f):
            out[round(float(row["t_ps"]), 3)] = float(row["T_set_K"])
    if not out:
        raise SystemExit(f"{thermo}: 행이 없다")
    return out


def window_T(tset, a, b):
    ka, kb = round(a, 3), round(b, 3)
    if ka not in tset or kb not in tset:
        raise SystemExit(f"thermo 에 t = {a} 또는 {b} ps 행이 없다 — 창 경계가 기록 간격과 안 맞는다")
    return [tset[ka], tset[kb]], 0.5 * (tset[ka] + tset[kb])


def traj_frames(traj):
    """extxyz 프레임 수 — 첫 줄 원자 수 n 으로 (n + 2) 줄 단위를 센다 (나머지가 남으면 멈춘다)."""
    with open(traj) as f:
        first = f.readline()
        n_lines = 1 + sum(1 for _ in f)
    nat = int(first.split()[0])
    if n_lines % (nat + 2):
        raise SystemExit(f"{traj}: 줄 수 {n_lines} 가 (원자 {nat} + 2) 의 배수가 아니다")
    return n_lines // (nat + 2)


def check_spacing(traj, tset):
    """궤적 저장 간격이 SAVE_FS (1 ps) 인지 — 프레임 수 = thermo 끝 시간 / 1 ps + 1 (B · A seed1 기록 = 1051 · 1050 ps).
    다르면 멈춘다: --save_fs 1000 으로 창을 자르면 창이 조용히 틀린다."""
    want = int(round(max(tset) / (SAVE_FS / 1000.0))) + 1
    got = traj_frames(traj)
    if got != want:
        raise SystemExit(f"{traj}: 프레임 {got} ≠ thermo 끝 {max(tset)} ps / {SAVE_FS / 1000.0} ps + 1 = {want} — 저장 간격이 다르다 · 창을 자르지 않는다")
    return got


def crossings(rows, level=LEVEL):
    """시간순 창 → frac_moved 가 level 을 지나는 T (이웃 두 창 사이 선형 보간) 의 목록."""
    out = []
    for r0, r1 in zip(rows, rows[1:]):
        f0, f1 = r0["frac_moved"], r1["frac_moved"]
        if (f0 - level) * (f1 - level) < 0 or (f1 == level and f0 != level):
            t0, t1 = r0["T_mean_K"], r1["T_mean_K"]
            out.append(t0 + (level - f0) * (t1 - t0) / (f1 - f0))
    return out


def scan(traj, thermo, label, py=sys.executable, win=WIN_PS, t_end=None, jump=JUMP):
    tset = read_tset(thermo)
    check_spacing(traj, tset)
    t_end = t_end if t_end is not None else max(tset)
    rows, a = [], 0.0
    with tempfile.TemporaryDirectory(prefix="t50_") as td:
        while a + win <= t_end + 1e-9:
            od = Path(td) / f"scan_{int(a)}"
            cmd = [py, str(jump), "--traj", str(traj), "--label", f"{label}_{int(a)}", "--out_dir", str(od),
                   "--save_fs", str(SAVE_FS), "--t_from_ps", str(a), "--t_to_ps", str(a + win),
                   "--hop_census_lag_ps", str(LAG_PS), "--hop_min_dist", str(MIN_DIST), "--hop_events_all"]
            p = subprocess.run(cmd, capture_output=True, text=True)
            hc = od / f"{label}_{int(a)}_hop_census.json"
            if p.returncode != 0 or not hc.exists():
                raise SystemExit(f"aimd_jump_stats 실패 (창 {a}–{a + win} ps · rc {p.returncode}): {p.stderr[-400:]}")
            h = json.loads(hc.read_text())
            ts, tm = window_T(tset, a, a + win)
            rows.append({"t_from_ps": a, "t_to_ps": a + win, "T_set_K": ts, "T_mean_K": tm,
                         "n_moved": h.get("n_moved"), "n_Li": h.get("n_Li"), "frac_moved": h["frac_moved"],
                         "p90_A": (h.get("per_ion_max_A") or {}).get("p90")})
            a += win
    cr = crossings(rows)
    return {"rows": rows, "crossings_K_all": cr, "T50_K": cr[0] if len(cr) == 1 else None,
            "note": None if len(cr) == 1 else f"교차 {len(cr)} 개 — T₅₀ 을 고르지 않는다"}


def control_B(py=sys.executable, tol_K=0.05):
    rec = json.loads(B_RECORD.read_text())
    out, ok = {}, True
    for sd, src in rec["sources"].items():
        traj = REPO / src["traj"]
        r = scan(traj, traj.parent / "thermo.csv", f"B_{sd}", py=py)
        want = rec["T50_K"][sd]
        got = r["T50_K"]
        full = (rec.get("crossings_K_all") or {}).get(sd) or []   # 반올림 전 값이 있으면 그걸로 1e-6 대조
        good = got is not None and (abs(got - full[0]) <= 1e-6 if len(full) == 1 else abs(got - want) <= tol_K)
        ok &= good
        out[sd] = {"기록": want, "재현": got, "차": None if got is None else round(got - want, 4), "ok": good}
        print(f"  {'✓' if good else '✗'} B {sd}: 기록 {want} · 재현 {got if got is None else round(got, 2)}")
    return ok, out


def a1_record(path=A1_RECORD):
    return json.loads(Path(path).read_text())["2_실측"]["표"]


def compare_a1(rows, ref, size=None):
    """창마다 09-21 표와 맞춘다 — 창 경계 · T_set (같음) · 이동 수 (같음) · p90 (±0.005 · 기록은 둘째 자리). 다른 것의 목록."""
    diffs = []
    if size is not None and size != A1_BYTES:
        diffs.append(f"궤적 크기 기록 {A1_BYTES} B · 지금 {size} B — 다른 파일이다")
    if len(rows) != len(ref):
        diffs.append(f"창 수 기록 {len(ref)} · 지금 {len(rows)}")
    for r, w in zip(rows, ref):
        tag = f"{w['t_from_ps']}–{w['t_to_ps']} ps"
        if (r["t_from_ps"], r["t_to_ps"]) != (w["t_from_ps"], w["t_to_ps"]) or list(r["T_set_K"]) != list(w["T_set_K"]):
            diffs.append(f"{tag}: 창 · T_set 기록 {w['T_set_K']} · 지금 {r['t_from_ps']}–{r['t_to_ps']} {r['T_set_K']}")
            continue
        if r["n_moved"] != w["n_moved"]:
            diffs.append(f"{tag}: 이동 수 기록 {w['n_moved']} · 지금 {r['n_moved']}")
        pw, pr = (w.get("per_ion_max_A") or {}).get("p90"), r.get("p90_A")
        if pw is None or pr is None or abs(pr - pw) > 0.005 + 1e-9:
            diffs.append(f"{tag}: p90 기록 {pw} · 지금 {pr}")
    return diffs


def a1_t50_from_record(ref):
    return crossings([{"T_mean_K": 0.5 * (w["T_set_K"][0] + w["T_set_K"][1]), "frac_moved": w["n_moved"] / w["n_Li"]}
                      for w in ref])


def control_A1(traj, thermo, py=sys.executable):
    ref = a1_record()
    r = scan(traj, thermo, "A_s1", py=py)
    diffs = compare_a1(r["rows"], ref, size=Path(traj).stat().st_size)
    want = a1_t50_from_record(ref)
    ok = not diffs and len(want) == 1 and r["T50_K"] is not None and abs(r["T50_K"] - want[0]) <= 1e-6
    for d in diffs[:8]:
        print("  ✗", d)
    print(f"  {'✓' if ok else '✗'} A seed1: 기록 표로 낸 T₅₀ {[round(x, 3) for x in want]} · 재현 "
          f"{None if r['T50_K'] is None else round(r['T50_K'], 3)} · 다른 창 {len(diffs)}")
    return ok, {"diffs": diffs, "T50_K": r["T50_K"], "T50_from_record_K": want, "rows": r["rows"]}


def selftest():
    n = [0, 0]

    def ck(name, cond):
        n[0 if cond else 1] += 1
        print(f"  {'✓' if cond else '✗'} {name}")

    rows = [{"T_mean_K": t, "frac_moved": f} for t, f in ((1200, 1.0), (475, 0.9), (425, 0.792), (375, 0.438), (325, 0.2))]
    c = crossings(rows)
    ck("교차 하나 · A seed1 기록 (425 K 0.792 → 375 K 0.438) → 383.8 K", len(c) == 1 and abs(c[0] - 383.757) < 0.01)
    rows2 = [{"T_mean_K": t, "frac_moved": f} for t, f in ((475, 0.6), (425, 0.45), (375, 0.55), (325, 0.3))]
    ck("⛔음성: 교차 셋이면 셋을 다 낸다 (고르지 않는다)", len(crossings(rows2)) == 3)
    rows3 = [{"T_mean_K": t, "frac_moved": f} for t, f in ((475, 0.9), (425, 0.8))]
    ck("⛔음성: 교차가 없으면 빈 목록", crossings(rows3) == [])
    with tempfile.TemporaryDirectory() as td:
        th = Path(td) / "thermo.csv"
        th.write_text("t_ps,T_K,T_set_K\n0.000,1000,1200.0\n50.000,1200,1200.0\n100.000,1150,1150.0\n")
        ts = read_tset(th)
        ck("창 T = 양 끝 T_set 평균 (50–100 ps → 1175)", window_T(ts, 50, 100) == ([1200.0, 1150.0], 1175.0))
        try:
            window_T(ts, 100, 150)
            ck("⛔음성: 기록에 없는 창 끝이면 멈춘다", False)
        except SystemExit:
            ck("⛔음성: 기록에 없는 창 끝이면 멈춘다", True)
        tr = Path(td) / "t.xyz"
        tr.write_text("".join(f"1\nframe {k}\nLi 0 0 0\n" for k in range(101)))
        ck("저장 간격: 101 프레임 · thermo 끝 100 ps → 1 ps 간격 (통과)", check_spacing(tr, {0.0: 1.0, 100.0: 1.0}) == 101)
        tr.write_text("".join(f"1\nframe {k}\nLi 0 0 0\n" for k in range(51)))
        try:
            check_spacing(tr, {0.0: 1.0, 100.0: 1.0})
            ck("⛔음성: 51 프레임 · 100 ps (2 ps 간격) 이면 멈춘다", False)
        except SystemExit:
            ck("⛔음성: 51 프레임 · 100 ps (2 ps 간격) 이면 멈춘다", True)
    ref = a1_record()
    ck("A seed1 기록 표 (21 창 · 이동 수 정수) 로 낸 T₅₀ = 383.824 K (교차 하나 · 38/48 → 21/48 · 카드의 ≈ 384 는 반올림 비율로 낸 383.76)",
       len(ref) == 21 and [round(x, 3) for x in a1_t50_from_record(ref)] == [383.824])
    same = [{"t_from_ps": w["t_from_ps"], "t_to_ps": w["t_to_ps"], "T_set_K": [float(x) for x in w["T_set_K"]],
             "n_moved": w["n_moved"], "p90_A": w["per_ion_max_A"]["p90"] + 0.004} for w in ref]
    ck("A1 대조: 같은 표 (p90 반올림 안 차이) · 같은 크기면 다른 것이 없다", compare_a1(same, ref, size=A1_BYTES) == [])
    bad = [dict(x) for x in same]; bad[18]["n_moved"] = 22
    ck("⛔음성 A1 대조: 창 하나의 이동 수가 다르면 잡는다", len(compare_a1(bad, ref)) == 1)
    bad = [dict(x) for x in same]; bad[3]["p90_A"] += 0.01
    ck("⛔음성 A1 대조: p90 이 0.01 다르면 잡는다", len(compare_a1(bad, ref)) == 1)
    ck("⛔음성 A1 대조: 창이 하나 모자라거나 파일 크기가 다르면 잡는다",
       compare_a1(same[:-1], ref) != [] and compare_a1(same, ref, size=A1_BYTES + 1) != [])
    print(f"{'✅' if n[1] == 0 else '⛔'} quench_t50_scan selftest {n[0]}/{n[0] + n[1]}")
    return 0 if n[1] == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--traj"); ap.add_argument("--thermo"); ap.add_argument("--label", default="scan")
    ap.add_argument("--out"); ap.add_argument("--py", default=sys.executable)
    ap.add_argument("--control_B", action="store_true", help="B 다섯을 저장소 궤적으로 다시 내 기록과 대조 (±0.05 K)")
    ap.add_argument("--control_A1", action="store_true", help="A seed1 (--traj · --thermo) 을 09-21 스캔 표와 대조")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.control_B:
        ok, out = control_B(a.py)
        print("✅ B 다섯 재현" if ok else "⛔ B 기록을 재현 못 했다 — 이 도구로 A 를 내지 않는다")
        if a.out:
            Path(a.out).write_text(json.dumps({"control_B": out, "ok": ok}, ensure_ascii=False, indent=1) + "\n")
        return 0 if ok else 1
    if a.control_A1:
        if not (a.traj and a.thermo):
            ap.error("--control_A1 에는 --traj · --thermo 가 필요하다")
        ok, out = control_A1(a.traj, a.thermo, a.py)
        print("✅ A seed1 재현 (09-21 표 21 창)" if ok else "⛔ A seed1 기록을 재현 못 했다 — 이 기계에서 A 를 내지 않는다")
        if a.out:
            Path(a.out).write_text(json.dumps({"control_A1": out, "ok": ok}, ensure_ascii=False, indent=1) + "\n")
        return 0 if ok else 1
    if not (a.traj and a.thermo and a.out):
        ap.error("--traj · --thermo · --out (또는 --control_B · --selftest)")
    r = scan(a.traj, a.thermo, a.label, py=a.py)
    r.update({"traj": str(a.traj), "label": a.label, "method": "50 ps 창 · aimd_jump_stats --save_fs 1000 --hop_census_lag_ps 5.0 --hop_min_dist 2.0 --hop_events_all · 창 T = T_set 양 끝 평균 · 0.5 교차 선형 보간"})
    Path(a.out).write_text(json.dumps(r, ensure_ascii=False, indent=1) + "\n")
    print(f"{a.label}: T₅₀ = {r['T50_K'] if r['T50_K'] is None else round(r['T50_K'], 1)} K · 교차 {[round(x, 1) for x in r['crossings_K_all']]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
