#!/usr/bin/env python3
"""make_inputs.py — Nd Q3′ (Nd@P vs 같은 셀 Nd@Li) 의 Bader · ELF SCF 입력과 자리 역할표를 만든다.

카드 db/properties/nd_q3p_same_cell_card_2026_10_27.json · 결정 D-2026-10-27-nd-q3p-same-cell (proposed).
트랙 CEI/Nd · 1저자 = 실험 쪽 · 결정은 '사용자' (10-27 '권고대로 해').

무엇을 하나
  · 구조 = Q1 V₀ 이온 이완 끝 기하 (db/raw/ndo_site_eos_v0_2026_10_23/<모델>/scf.out 의 마지막 'Begin final coordinates' ·
    셀은 같은 폴더 scf.in 의 CELL_PARAMETERS — 고정셀 relax 라 셀은 입력 그대로다).
  · 원자 순서가 이완 전 후보 (db/inputs/ndo_site_2026_10_14/candidates/<MP|MLi>/<모델>.xyz) 와 **원소 열까지 같아야** 쓴다 —
    자리 역할 (원래 어느 사면체의 S 였나) 을 이완 전 기하에서 읽기 때문이다.
  · 역할 (이완 전 · 결과 전에 고정): 음이온 S·O 가 P 에서 2.4 Å 안 → PX4 · 아니고 (Nd@P 모델만) Nd 에서 2.4 Å 안 → NdT
    (Nd 가 들어간 4b 사면체의 S) · 둘 다 아니면 free. Nd@Li 모델에는 NdT 가 없다 (Nd 가 4b 가 아니다).
  · 입력 둘: bader/<모델>/scf.in (Q3 Bader 와 같은 PAW psl 세트 · 70/560 · mv 0.01 · nosym · conv 1e-9 · β 0.3 · k 3 3 1 ·
    tprnfor · tstress) / elf/<모델>/scf.in (Q3 ELF 와 같은 NC 세트 · 80/320 · conv 1e-10 · electron_maxstep 200 · k 3 3 1).

⛔ 못 하는 것
  · 계산하지 않는다 · Bader · ELF 를 읽지 않는다 (후처리는 bader_summary_zval.py · sample_elf_bonds.py 몫).
  · 이완 끝 기하의 품질을 판정하지 않는다 (Q1 판독 몫) · pseudo 파일이 그 기계에 있는지 모른다 (러너가 본다).
  · 역할 분류는 거리 하나다 — 이완 뒤 자리가 바뀐 원자는 이완 전 역할을 그대로 단다 (그게 '원래 자리' 정의다).

  python3 db/inputs/nd_q3p_2026_10_27/make_inputs.py            # 만든다 (같은 폴더)
  python3 db/inputs/nd_q3p_2026_10_27/make_inputs.py --selftest
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys, tempfile
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
V0 = REPO / "db/raw/ndo_site_eos_v0_2026_10_23"
CAND = REPO / "db/inputs/ndo_site_2026_10_14/candidates"
MODELS = {"MP_07": "MP", "MLi_04": "MLi"}
R_ROLE = 2.4                     # 이완 전 사면체 소속 (P–S 2.05 · 4b 자리에 넣은 Nd–S 2.10 · 그다음 음이온 ≥ 3.6 Å)
KGY_PAW = "/home/kgy/work/pseudo"
KGY_NC = "/home/kgy/work/runs/nd_q3p_1027/pseudo_nc"
PAW = {"Li": "Li.pbe-sl-kjpaw_psl.1.0.0.UPF", "P": "P.pbe-n-kjpaw_psl.1.0.0.UPF", "S": "S.pbe-nl-kjpaw_psl.1.0.0.UPF",
       "Cl": "Cl.pbe-nl-kjpaw_psl.1.0.0.UPF", "O": "O.pbe-n-kjpaw_psl.0.1.UPF", "Nd": "Nd.pbe-spdn-kjpaw_psl.1.0.0.UPF"}
NC = {"Li": "Li_ONCV_PBE-1.2.upf", "P": "P_ONCV_PBE-1.2.upf", "S": "S_ONCV_PBE-1.2.upf",
      "Cl": "Cl_ONCV_PBE-1.2.upf", "O": "O_ONCV_PBE-1.0.upf", "Nd": "Nd3plus_f-in-core.dojo_psp8_conv.upf"}
MASS = {"Li": 6.941, "P": 30.974, "S": 32.065, "Cl": 35.453, "O": 15.999, "Nd": 144.242}
BADER_BLOCK = ("&CONTROL\n  calculation='scf'\n  prefix='{pfx}'\n  pseudo_dir='{pdir}'\n  outdir='./tmp/'\n"
               "  tprnfor=.true.\n  tstress=.true.\n  verbosity='high'\n/\n"
               "&SYSTEM\n  ibrav=0\n  nat={nat}\n  ntyp={ntyp}\n  ecutwfc=70.0\n  ecutrho=560.0\n"
               "  occupations='smearing'\n  smearing='mv'\n  degauss=0.01\n  nosym=.true.\n/\n"
               "&ELECTRONS\n  conv_thr=1.0d-9\n  mixing_beta=0.3\n/\n")
ELF_BLOCK = ("&CONTROL\n  calculation='scf'\n  prefix='{pfx}'\n  pseudo_dir='{pdir}'\n  outdir='./tmp/'\n"
             "  tprnfor=.true.\n  verbosity='high'\n/\n"
             "&SYSTEM\n  ibrav=0\n  nat={nat}\n  ntyp={ntyp}\n  ecutwfc=80.0\n  ecutrho=320.0\n"
             "  occupations='smearing'\n  smearing='mv'\n  degauss=0.01\n  nosym=.true.\n/\n"
             "&ELECTRONS\n  conv_thr=1.0d-10\n  mixing_beta=0.3\n  electron_maxstep=200\n/\n")


def final_coords(out: Path):
    t = out.read_text(errors="ignore")
    if "bfgs converged" not in t:
        raise SystemExit(f"⛔ {out}: 'bfgs converged' 가 없다 — 이완 끝 기하가 아니다")
    i = t.rfind("Begin final coordinates")
    blk = t[i:t.find("End final coordinates", i)]
    m = re.search(r"ATOMIC_POSITIONS\s*\(?\s*(\w+)", blk)
    rows = []
    for ln in blk[m.end():].splitlines():
        p = ln.split()
        if len(p) >= 4 and re.match(r"^[A-Z][a-z]?$", p[0]):
            rows.append((p[0], [float(x) for x in p[1:4]]))
    return m.group(1).lower(), rows


def cell_of(inp: Path):
    t = inp.read_text()
    i = t.index("CELL_PARAMETERS")
    if "angstrom" not in t[i:i + 40].lower():
        raise SystemExit(f"⛔ {inp}: CELL_PARAMETERS 단위가 angstrom 이 아니다")
    return np.array([[float(x) for x in ln.split()[:3]] for ln in t[i:].splitlines()[1:4]])


def mic_dist(cell, a, b):
    f = (b - a) @ np.linalg.inv(cell)
    f -= np.round(f)
    return float(np.linalg.norm(f @ cell))


def roles(cand_sym, cand_pos, cand_cell, model_kind):
    """이완 전 기하에서 음이온 역할 — PX4 · NdT · free (+ 그 밖 원소는 원소 이름)."""
    out = []
    for i, s in enumerate(cand_sym):
        if s not in ("S", "O"):
            out.append(s); continue
        dP = min([mic_dist(cand_cell, cand_pos[i], cand_pos[j]) for j, t in enumerate(cand_sym) if t == "P"] or [9.9])
        dN = min([mic_dist(cand_cell, cand_pos[i], cand_pos[j]) for j, t in enumerate(cand_sym) if t == "Nd"] or [9.9])
        if dP < R_ROLE:
            out.append(f"{s}_PX4")
        elif model_kind == "MP" and dN < R_ROLE:
            out.append(f"{s}_NdT")
        else:
            out.append(f"{s}_free")
    return out


def build(outdir: Path, v0=V0, cand=CAND):
    from ase.io import read
    man = {"card": "db/properties/nd_q3p_same_cell_card_2026_10_27.json",
           "decision": "D-2026-10-27-nd-q3p-same-cell", "R_role_A": R_ROLE, "models": {}}
    for mdl, kind in MODELS.items():
        unit, rows = final_coords(v0 / mdl / "scf.out")
        cell = cell_of(v0 / mdl / "scf.in")
        c = read(cand / kind / f"{mdl}.xyz")
        if c.cell.rank != 3:
            raise SystemExit(f"⛔ {mdl}: 후보 xyz 에 셀이 없다 — 역할을 못 읽는다")
        csym = c.get_chemical_symbols()
        fsym = [r[0] for r in rows]
        if csym != fsym:
            raise SystemExit(f"⛔ {mdl}: 이완 끝 원소 열이 후보 xyz 와 다르다 — 원자 순서를 믿을 수 없어 만들지 않는다")
        rl = roles(csym, c.get_positions(), c.cell.array, kind)
        els = sorted(set(fsym), key=lambda e: list(MASS).index(e))
        pos = "".join(f"  {s:3s} {x:14.10f} {y:14.10f} {z:14.10f}\n" for s, (x, y, z) in rows)
        tail = (f"ATOMIC_POSITIONS {unit}\n{pos}K_POINTS automatic\n  3 3 1 0 0 0\nCELL_PARAMETERS angstrom\n"
                + "".join(f"  {a:16.10f} {b:16.10f} {d:16.10f}\n" for a, b, d in cell))
        for kindname, block, pdir, pp in (("bader", BADER_BLOCK, KGY_PAW, PAW), ("elf", ELF_BLOCK, KGY_NC, NC)):
            spec = "ATOMIC_SPECIES\n" + "".join(f"  {e:3s} {MASS[e]:8.3f}  {pp[e]}\n" for e in els)
            txt = block.format(pfx=f"q3p_{mdl}_{kindname}", pdir=pdir, nat=len(rows), ntyp=len(els)) + spec + tail
            d = outdir / kindname / mdl
            d.mkdir(parents=True, exist_ok=True)
            (d / "scf.in").write_text(txt)
        from collections import Counter
        man["models"][mdl] = {
            "kind": kind, "nat": len(rows), "unit": unit,
            "v0_scf_out_sha256": hashlib.sha256((v0 / mdl / "scf.out").read_bytes()).hexdigest(),
            "candidate_xyz_sha256": hashlib.sha256((cand / kind / f"{mdl}.xyz").read_bytes()).hexdigest(),
            "role_counts": dict(sorted(Counter(rl).items())), "roles": rl}
    (outdir / "roles_manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n")
    return man


def _selftest():
    n = bad = 0
    def ck(name, got, want):
        nonlocal n, bad
        n += 1
        if got != want:
            bad += 1; print(f"  ✗ {name}: got {got!r} want {want!r}")
    with tempfile.TemporaryDirectory() as td:
        m = build(Path(td))
        ck("MP role counts", m["models"]["MP_07"]["role_counts"],
           {"Cl": 8, "Li": 31, "Nd": 2, "O_PX4": 3, "P": 3, "S_NdT": 8, "S_PX4": 9, "S_free": 2})
        ck("MLi role counts (NdT 없음)", m["models"]["MLi_04"]["role_counts"],
           {"Cl": 8, "Li": 21, "Nd": 2, "O_PX4": 3, "P": 5, "S_PX4": 17, "S_free": 2})
        for mdl, nat in (("MP_07", 66), ("MLi_04", 58)):
            for k in ("bader", "elf"):
                t = (Path(td) / k / mdl / "scf.in").read_text()
                ck(f"{k}/{mdl} nat", int(re.search(r"nat=(\d+)", t).group(1)), nat)
                ck(f"{k}/{mdl} k 331", "3 3 1 0 0 0" in t, True)
                _blk = t[t.index("ATOMIC_POSITIONS"):t.index("K_POINTS")]   # ATOMIC_SPECIES 줄을 세지 않게 블록만
                ck(f"{k}/{mdl} 원자 줄 수", len(re.findall(r"^  (Li|P|S|Cl|O|Nd)\s+-?\d", _blk, re.M)), nat)
            tb = (Path(td) / "bader" / mdl / "scf.in").read_text()
            te = (Path(td) / "elf" / mdl / "scf.in").read_text()
            ck(f"bader/{mdl} PAW Nd", "Nd.pbe-spdn-kjpaw_psl.1.0.0.UPF" in tb and "ecutrho=560.0" in tb, True)
            ck(f"elf/{mdl} NC Nd", "Nd3plus_f-in-core.dojo_psp8_conv.upf" in te and "ecutrho=320.0" in te, True)
        # 두 모델의 방법 노브가 같다 (러너 균일성 검사가 보는 열쇠)
        keys = r"^ *(ecutwfc|ecutrho|occupations|smearing|degauss|nosym|conv_thr|mixing_beta|electron_maxstep)="
        for k in ("bader", "elf"):
            a = sorted(re.findall(keys + ".*$", (Path(td) / k / "MP_07" / "scf.in").read_text(), re.M))
            b = sorted(re.findall(keys + ".*$", (Path(td) / k / "MLi_04" / "scf.in").read_text(), re.M))
            ck(f"{k} 두 모델 방법 노브 같음", a, b)
    # 음성 ①: 원자 순서가 다르면 만들지 않는다
    with tempfile.TemporaryDirectory() as td:
        from ase.io import read, write
        for kind in ("MP", "MLi"):
            (Path(td) / "cand" / kind).mkdir(parents=True)
        for mdl, kind in MODELS.items():
            a = read(CAND / kind / f"{mdl}.xyz")
            if mdl == "MP_07":
                a = a[list(range(1, len(a))) + [0]]          # 첫 원자를 끝으로
            write(Path(td) / "cand" / kind / f"{mdl}.xyz", a)
        try:
            build(Path(td) / "out", cand=Path(td) / "cand")
            ck("음성: 원자 순서가 다르면 멈춘다", "built", "stopped")
        except SystemExit:
            ck("음성: 원자 순서가 다르면 멈춘다", "stopped", "stopped")
    # 음성 ②: 미수렴 relax 출력이면 멈춘다
    with tempfile.TemporaryDirectory() as td:
        for mdl in MODELS:
            (Path(td) / "v0" / mdl).mkdir(parents=True)
            src = (V0 / mdl / "scf.out").read_text(errors="ignore")
            if mdl == "MLi_04":
                src = src.replace("bfgs converged", "bfgs NOT-converged")
            (Path(td) / "v0" / mdl / "scf.out").write_text(src)
            (Path(td) / "v0" / mdl / "scf.in").write_text((V0 / mdl / "scf.in").read_text())
        try:
            build(Path(td) / "out", v0=Path(td) / "v0")
            ck("음성: 미수렴 이완이면 멈춘다", "built", "stopped")
        except SystemExit:
            ck("음성: 미수렴 이완이면 멈춘다", "stopped", "stopped")
    print(f"{'✅' if bad == 0 else '⛔'} selftest {n - bad}/{n}")
    return 1 if bad else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(_selftest())
    m = build(HERE)
    for mdl, v in m["models"].items():
        print(f"{mdl}: nat {v['nat']} · {v['role_counts']}")
