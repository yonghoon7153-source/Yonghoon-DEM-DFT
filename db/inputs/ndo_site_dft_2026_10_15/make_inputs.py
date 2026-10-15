#!/usr/bin/env python3
"""make_inputs.py — Nd 자리 비교 Q1 의 DFT 입력 8 개 (후보 6 scf + 기준상 2 vc-relax) · 카드 §6 에 결속

  카드: db/properties/ndo_lpscl16_site_stability_estimand_2026_10_14.json
        (§3 '모델별 UMA 상위 3 → DFT 단일점 → 모델별 최저' · §4 G1 '6 + 기준상 2 가 다 있어야 Q1' · §6 계산 설정)
  UMA 판독: db/raw/ndo_site_2026_10_14/uma_rietveld_2026_10_15/ (site_dg_rietveld.json 의 모델별 top · structures/*.xyz)
  기준상: db/structures/sei_li2s_mp-1153.cif · db/structures/li3ps4_mp-985583.cif (카드 §2 Q1 참조_구조)

무엇을 쓰나 (tools/doping/run_force_check_scf.sh 가 읽는 꼴 = <out>/<이름>/scf.in)
  · 후보 6 — UMA post_relax 의 셀 · 좌표 그대로 · calculation 'scf' · K_POINTS = 카드 §6 (2 2 1)
  · 기준상 2 — MP CIF 에서 · calculation 'vc-relax' · 축마다 k = ceil(13.9 Å / 축 길이) (카드 §6 규칙 'kxL ≥ 13.9 Å')
    (파일 이름은 러너에 맞춰 scf.in 이다 — 안의 calculation 이 vc-relax 다)
  · 전 점 nosym = .true. — 러너의 설정 균일성 검사 (nosym 포함) 를 그대로 통과시키려고. 기준상은 작아서 비용 차가 작다
  · 설정 (ecut · smearing · degauss · conv_thr · mixing_beta · pseudo_dir · PP) 은 **카드 §6 에서 읽는다** —
    생성 함수는 tools/doping/generate_dft_inputs.py::generate_pwin (O 배치 카드 6 점과 같은 함수)
  · <out>/inputs_manifest.json — 점마다 출처 파일 · sha256 · 조성 · k · calculation

검사 (하나라도 어긋나면 아무것도 안 쓰고 멈춘다 · 종료 1)
  · ATOMIC_SPECIES 의 PP 이름이 카드 §6 PP 와 정확히 같다
    ⛔ generate_dft_inputs.PSEUDOS 의 Nd 기본값은 4f-원자가 (Nd.paw.z_14.atompaw…) 다 — 카드는 4f-in-core
       (Nd.pbe-spdn-kjpaw_psl.1.0.0.UPF). 덮지 않으면 조용히 다른 계산이 된다
  · ecutwfc · ecutrho · smearing · degauss · conv_thr · mixing_beta · pseudo_dir · nspin(미지정 = 1) 줄이 카드 값과 같다
  · 후보 이름 = 판독 요약의 모델별 top (3 개씩) · 조성 = 요약의 모델 화학식 · 원자 수 66 / 58
  · 기준상 조성 Li2S · Li12P4S16

⛔ 이 도구가 못 하는 것
  · 계산하지 않는다 · k 수렴을 판정하지 않는다 (G4 탐침은 결과 뒤 카드 규칙대로)
  · kgy 원본 nd_scf scf.in (O 배치 카드 6 점) 과의 글자 대조는 못 한다 — 원본이 저장소에 없다. kgy 에서 대조한다
  · UMA 기하가 DFT 바닥과 가까운지 모른다 (G3 · vc-relax 는 결과 뒤 규칙대로)

  python3 make_inputs.py --selftest
  python3 make_inputs.py --out <폴더>            # 기본 pseudo_dir = 카드 §6 (kgy) · 다른 기계면 --pseudo_dir
"""
import argparse
import hashlib
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "tools" / "doping"))
CARD = REPO / "db/properties/ndo_lpscl16_site_stability_estimand_2026_10_14.json"
UMA = REPO / "db/raw/ndo_site_2026_10_14/uma_rietveld_2026_10_15"
REFS = {"Li2S": (REPO / "db/structures/sei_li2s_mp-1153.cif", "Li2S"),
        "Li3PS4": (REPO / "db/structures/li3ps4_mp-985583.cif", "Li12P4S16")}
KXL_MIN = 13.9            # 카드 §6 규칙 '기준상 k 는 kxL ≥ 13.9 Å'
N_ATOMS = {"MP": 66, "MLi": 58}


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def card_settings(card):
    s = card["6_규약_대조"]["계산_설정"]
    occ = s["occupations"]                       # "smearing · mv · degauss 0.01 Ry"
    m = re.match(r"smearing\s*·\s*(\w+)\s*·\s*degauss\s*([0-9.]+)", occ)
    if not m:
        raise SystemExit(f"⛔ 카드 occupations 를 못 읽는다: {occ!r}")
    k = s["K_POINTS"].split("(")[0].split()      # "automatic 2 2 1 0 0 0 (…)"
    if k[0] != "automatic":
        raise SystemExit(f"⛔ 카드 K_POINTS 가 automatic 이 아니다: {s['K_POINTS']!r}")
    pp = {el: v.split(" (")[0].strip() for el, v in s["PP"].items()}
    return {"ecutwfc": float(s["ecutwfc_Ry"]), "ecutrho": float(s["ecutrho_Ry"]),
            "smearing": m.group(1), "degauss": float(m.group(2)),
            "conv_thr": s["conv_thr"], "mixing_beta": float(s["mixing_beta"]),
            "kpoints": " ".join(k[1:4]), "pseudo_dir": s["pseudo_dir"], "pp": pp}


def ref_kpoints(atoms):
    return " ".join(str(max(1, math.ceil(KXL_MIN / L))) for L in atoms.cell.lengths())


def check_input(text, cfg, pseudo_dir, calc, natoms, kpts):
    """생성된 입력을 카드 값과 대조 — 어긋난 항목 목록 (빈 목록이면 통과)."""
    bad = []
    want = {"ecutwfc": f"{cfg['ecutwfc']:g}", "ecutrho": f"{cfg['ecutrho']:g}",
            "smearing": f"'{cfg['smearing']}'", "degauss": f"{cfg['degauss']:g}",
            "conv_thr": cfg["conv_thr"], "mixing_beta": f"{cfg['mixing_beta']:g}",
            "occupations": "'smearing'", "calculation": f"'{calc}'", "nat": str(natoms),
            "pseudo_dir": f"'{pseudo_dir}'", "nosym": ".true."}
    for key, val in want.items():
        got = re.findall(rf"^\s*{key}\s*=\s*(\S+)", text, re.M)
        if len(got) != 1:
            bad.append(f"{key} 줄이 {len(got)} 개")
            continue
        g = got[0]
        try:
            same = float(g.replace("d", "e")) == float(val.replace("d", "e"))
        except ValueError:
            same = g == val
        if not same:
            bad.append(f"{key} = {g} (카드 {val})")
    if re.search(r"^\s*nspin\s*=", text, re.M):
        bad.append("nspin 줄이 있다 (카드: 미지정 = 1)")
    sp = re.search(r"ATOMIC_SPECIES\n(.*?)\nCELL_PARAMETERS", text, re.S)
    got_pp = {ln.split()[0]: ln.split()[2] for ln in sp.group(1).splitlines()} if sp else {}
    for el, f in got_pp.items():
        if cfg["pp"].get(el) != f:
            bad.append(f"PP {el} = {f} (카드 {cfg['pp'].get(el)})")
    k = re.search(r"K_POINTS automatic\n\s*(\d+ \d+ \d+)", text)
    if not k or k.group(1) != kpts:
        bad.append(f"K_POINTS {k.group(1) if k else '없음'} (기대 {kpts})")
    return bad


def build(out, pseudo_dir=None, card_path=CARD, uma=UMA, write=True):
    from ase.io import read
    from generate_dft_inputs import generate_pwin
    card = json.loads(Path(card_path).read_text())
    cfg = card_settings(card)
    pdir = pseudo_dir or cfg["pseudo_dir"]
    summ = json.loads((Path(uma) / "site_dg_rietveld.json").read_text())
    models = summ["dopants"]["Nd"]["models"]
    jobs, bad = [], []
    for kind in ("MP", "MLi"):
        mdl = models[kind]
        top = mdl["top"]
        if len(top) != 3:
            bad.append(f"{kind} top 이 3 개가 아니다: {top}")
        for name in top:
            src = Path(uma) / "structures" / f"{name}.xyz"
            at = read(src)
            comp = "".join(f"{e}{c}" for e, c in sorted(Counter(at.get_chemical_symbols()).items()))
            if comp != mdl["formula"] or len(at) != N_ATOMS[kind]:
                bad.append(f"{name} 조성 {comp} ({len(at)} 원자) ≠ 요약 {mdl['formula']} ({N_ATOMS[kind]})")
            jobs.append((name, at, "scf", cfg["kpoints"], src, kind))
    for name, (src, formula) in REFS.items():
        at = read(src)
        if at.get_chemical_formula() != formula:
            bad.append(f"{name} 조성 {at.get_chemical_formula()} ≠ {formula}")
        jobs.append((name, at, "vc-relax", ref_kpoints(at), src, "ref"))
    texts = {}
    for name, at, calc, kp, src, kind in jobs:
        try:
            t = generate_pwin(at, name, cfg["ecutwfc"], cfg["ecutrho"], kp, pseudo_dir=pdir,
                              pp_names=cfg["pp"], calculation=calc, nosym=True,
                              smearing=cfg["smearing"], degauss=cfg["degauss"],
                              conv_thr=cfg["conv_thr"], mixing_beta=cfg["mixing_beta"])
        except ValueError as ex:
            bad.append(f"{name}: {ex}")
            continue
        b = check_input(t, cfg, pdir, calc, len(at), kp)
        bad += [f"{name}: {x}" for x in b]
        texts[name] = t
    if bad:
        raise SystemExit("⛔ 입력을 쓰지 않았다 —\n   " + "\n   ".join(bad))
    man = {"카드": str(Path(card_path).relative_to(REPO)) if Path(card_path).is_relative_to(REPO) else str(card_path),
           "카드_sha256": sha256(card_path), "설정_카드_6": cfg, "pseudo_dir_실제": pdir,
           "생성_함수": "tools/doping/generate_dft_inputs.py::generate_pwin",
           "생성_함수_sha256": sha256(REPO / "tools/doping/generate_dft_inputs.py"),
           "점": {}}
    for name, at, calc, kp, src, kind in jobs:
        man["점"][name] = {"종류": kind, "calculation": calc, "K_POINTS": kp,
                          "원자": len(at), "조성": at.get_chemical_formula(),
                          "출처": str(Path(src).relative_to(REPO)) if Path(src).is_relative_to(REPO) else str(src),
                          "출처_sha256": sha256(src),
                          "scf_in_sha256": hashlib.sha256(texts[name].encode()).hexdigest()}
    if write:
        out = Path(out)
        for name in texts:
            (out / name).mkdir(parents=True, exist_ok=True)
            (out / name / "scf.in").write_text(texts[name])
        (out / "inputs_manifest.json").write_text(json.dumps(man, indent=1, ensure_ascii=False) + "\n")
    return man, texts


def _selftest():
    import copy
    import tempfile
    ok = []

    def chk(c, m):
        ok.append(bool(c))
        print(("  ✓ " if c else "  ✗ ") + m)

    def must_stop(fn, m, needle):
        try:
            fn()
        except SystemExit as ex:
            chk(needle in str(ex), f"{m} → {str(ex).splitlines()[-1].strip()[:90]}")
        else:
            chk(False, m + " → 멈추지 않았다")

    man, texts = build(None, write=False)
    chk(len(texts) == 8, f"입력 8 개 (후보 6 + 기준상 2) — {sorted(texts)}")
    chk(all("Nd.pbe-spdn-kjpaw_psl.1.0.0.UPF" in texts[n] for n in texts if n.startswith("M")),
        "후보 6 개 모두 카드의 4f-in-core Nd PP")
    chk(all("wentzcovitch" not in t for t in texts.values()), "4f-원자가 Nd PP (generate_dft_inputs 기본값) 가 안 들어갔다")
    chk(man["점"]["Li2S"]["K_POINTS"] == "4 4 4" and man["점"]["Li3PS4"]["K_POINTS"] == "3 2 2",
        f"기준상 k = ceil(13.9/L) — Li2S {man['점']['Li2S']['K_POINTS']} · Li3PS4 {man['점']['Li3PS4']['K_POINTS']}")
    chk(all(man["점"][n]["K_POINTS"] == "2 2 1" for n in texts if n.startswith("M")), "후보 k = 카드 2 2 1")
    chk(all("calculation = 'vc-relax'" in texts[n] for n in ("Li2S", "Li3PS4")) and
        all("calculation = 'scf'" in texts[n] for n in texts if n.startswith("M")), "후보 scf · 기준상 vc-relax")
    # 러너 균일성 키가 8 개 모두 같다 (run_force_check_scf.sh::_settings_key 와 같은 화이트리스트)
    keys = "ecutwfc|ecutrho|occupations|smearing|degauss|nosym|conv_thr|mixing_mode|mixing_beta|electron_maxstep|diagonalization|nspin"
    sig = {n: tuple(sorted(re.sub(r"\s", "", x) for x in re.findall(rf"^ *(?:{keys}) *=.*$", t, re.M))) for n, t in texts.items()}
    chk(len(set(sig.values())) == 1, "러너 설정 균일성 키가 8 개 모두 같다")
    # ── 음성: 카드와 어긋나면 멈춘다 ──
    card = json.loads(CARD.read_text())
    tmp = Path(tempfile.mkdtemp())

    def with_card(mut):
        c = copy.deepcopy(card)
        mut(c)
        p = tmp / "card.json"
        p.write_text(json.dumps(c, ensure_ascii=False))
        return p

    import generate_dft_inputs as g
    keep = dict(g.PSEUDOS)
    p_wrong = with_card(lambda c: c["6_규약_대조"]["계산_설정"]["PP"].pop("Nd"))
    must_stop(lambda: build(None, card_path=p_wrong, write=False),
              "[음성] 카드에서 Nd PP 가 빠지면 (생성기 기본값 4f-원자가로 떨어짐) 멈춘다", "PP Nd")
    g.PSEUDOS.update(keep)
    orig_gen = g.generate_pwin
    g.generate_pwin = lambda *a, **k: orig_gen(*a, **{**k, "degauss": 0.02})
    must_stop(lambda: build(None, write=False), "[음성] 생성 함수가 degauss 를 바꾸면 멈춘다", "degauss")
    g.generate_pwin = lambda *a, **k: orig_gen(*a, **{**k, "nspin": 2, "start_mag": {"Nd": 0.5}})
    must_stop(lambda: build(None, write=False), "[음성] nspin 2 가 끼면 멈춘다 (카드: 미지정 = 1)", "nspin")
    g.generate_pwin = orig_gen
    p_k = with_card(lambda c: c["6_규약_대조"]["계산_설정"].__setitem__("K_POINTS", "automatic 3 3 1 0 0 0"))
    man_k, t_k = build(None, card_path=p_k, write=False)
    chk(man_k["점"]["MP_07"]["K_POINTS"] == "3 3 1", "카드 K_POINTS 를 바꾸면 후보 입력이 따라간다 (값을 카드에서 읽는다)")
    uma2 = tmp / "uma"
    (uma2 / "structures").mkdir(parents=True)
    s = json.loads((UMA / "site_dg_rietveld.json").read_text())
    s["dopants"]["Nd"]["models"]["MLi"]["top"] = ["MLi_03", "MLi_04"]
    (uma2 / "site_dg_rietveld.json").write_text(json.dumps(s))
    for f in (UMA / "structures").glob("*.xyz"):
        (uma2 / "structures" / f.name).write_bytes(f.read_bytes())
    must_stop(lambda: build(None, uma=uma2, write=False), "[음성] 모델 top 이 3 개가 아니면 멈춘다", "top 이 3 개가 아니다")
    s["dopants"]["Nd"]["models"]["MLi"]["top"] = ["MLi_03", "MLi_04", "MP_07"]
    (uma2 / "site_dg_rietveld.json").write_text(json.dumps(s))
    must_stop(lambda: build(None, uma=uma2, write=False), "[음성] M@Li 자리에 M@P 구조가 끼면 (조성 다름) 멈춘다", "조성")
    print(f"selftest: {sum(ok)}/{len(ok)}")
    return 0 if all(ok) else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--pseudo_dir", help="기본 = 카드 §6 (kgy /home/kgy/work/pseudo) · 다른 기계면 그 기계 경로 (같은 파일 이름이어야 한다)")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if not a.out:
        ap.error("--out 이 필요하다")
    man, texts = build(a.out, pseudo_dir=a.pseudo_dir)
    for n, v in man["점"].items():
        print(f"  {n:<7} {v['종류']:<4} {v['calculation']:<9} {v['원자']:>3} 원자 · {v['조성']:<20} · K {v['K_POINTS']}")
    print(f"✓ 입력 {len(texts)} 개 → {a.out}/<이름>/scf.in · 기록 inputs_manifest.json · pseudo_dir {man['pseudo_dir_실제']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
