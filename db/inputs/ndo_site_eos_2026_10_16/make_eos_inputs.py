#!/usr/bin/env python3
"""make_eos_inputs.py — Nd 자리 비교 Q1 · G3 고정셀 + EOS 1 단계: 부피 격자 입력 (두 모델 최저 셀 × 부피 6 점)

  카드: db/properties/ndo_lpscl16_site_stability_estimand_2026_10_14.json §4 G3 (개정 2026-10-15 · 결과 전) · §6 계산 설정
  설계 (결과 전): eos_plan.json (같은 폴더) — 사용자 2026-10-16 '2로해' (설계안 + GPU 자리 ② kgy · cascade 와 같이)
  대상: Q1 단일점 판독 (db/properties/ndo_site_dft_q1_readout_2026_10_16.json) 의 모델별 최저 MP_07 · MLi_04

무엇을 쓰나 (tools/doping/run_force_check_scf.sh 가 읽는 꼴 = <out>/<이름>_x<XXX>/scf.in)
  · 셀 = 1저자 Rietveld 정수화 셀 (db/inputs/ndo_site_2026_10_14/candidates/<종류>/<이름>.xyz 의 셀 —
    6.928 × 6.928 × 34.640 Å · 세 각 60° · 1175.66 Å³) 을 부피 비 x 의 세제곱근으로 **등방 스케일** (모양 고정 · vc-relax 안 씀)
  · 원자 = UMA 이완 구조 (db/raw/ndo_site_2026_10_14/uma_rietveld_2026_10_15/structures/<이름>.xyz — Q1 단일점과 같은 원본) 의
    **분율 좌표 그대로** (UMA 가 바꾼 셀 모양 — MP_07 은 c 가 +5 % — 을 Rietveld 모양으로 되돌린다)
  · calculation 'relax' (이온만 · BFGS) · forc_conv_thr 1.0d-3 · etot_conv_thr 1.0d-5 · nstep 200 · &CELL 블록 없음
  · 전자 설정 · PP · k (2 2 1 — G4 탐침으로 확인) = 카드 §6 — Q1 의 make_inputs.card_settings · check_input 을 그대로 쓴다
  · prefix 는 Q1 과 같은 이름 (점마다 폴더 · ./tmp 가 따로라 겹치지 않는다)

검사 (하나라도 어긋나면 아무것도 안 쓰고 멈춘다 · 종료 1)
  · Rietveld 셀 = 6.928 · 6.928 · 34.640 Å · 60 · 60 · 60° (허용 1e-3) · 두 후보의 원본 셀이 같다
  · 원자 수 · 조성 = Q1 판독 모델 화학식 (MP Cl8Li31Nd2O3P3S19 66 · MLi Cl8Li21Nd2O3P5S19 58)
  · 격자에 1.04 가 있다 (바닥 확인의 기준점 · eos_plan.json)
  · 점마다 부피 = x × V_Rietveld (상대 1e-9) · 각 60° (1e-6) · check_input (카드 §6 · PP · nosym · nspin 없음 · k)
  · **Q1 단일점 입력 (db/inputs/ndo_site_dft_2026_10_15/<이름>/scf.in) 에서 정해진 곳만 바뀌었다** —
    calculation · etot/forc 문턱 · CELL_PARAMETERS 3 줄 · &IONS 블록 추가. 좌표 · PP · 전자 설정 · k 줄은 바이트가 같아야 한다

⛔ 이 도구가 못 하는 것
  · 계산하지 않는다 · BM3 맞춤 · V₀ 입력 · ΔG 를 내지 않는다 (2 · 3 단계 — 규칙은 eos_plan.json 에 결과 전에 적었다)
  · 격자가 바닥을 감싸는지 모른다 (끝점 연장 규칙은 eos_plan.json — 결과 뒤 같은 생성기 --extra 로)
  · 이완이 다른 바닥으로 가는지 모른다 (바닥 확인은 2 단계)

  python3 make_eos_inputs.py --selftest
  python3 make_eos_inputs.py --out <폴더>                 # 기본 격자 0.98 … 1.08 (eos_plan.json)
  python3 make_eos_inputs.py --out <폴더> --extra 0.96    # 끝점 연장 (eos_plan.json 규칙이 발동했을 때만)
"""
import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "db/inputs/ndo_site_dft_2026_10_15"))
import make_inputs as MI  # noqa: E402  (카드 §6 설정 · 대조 함수 · tools/doping 경로)

PLAN = HERE / "eos_plan.json"
CARD = MI.CARD
UMA = MI.UMA
CAND = REPO / "db/inputs/ndo_site_2026_10_14/candidates"
Q1 = REPO / "db/inputs/ndo_site_dft_2026_10_15"
TARGETS = (("MLi", "MLi_04", "Cl8Li21Nd2O3P5S19", 58), ("MP", "MP_07", "Cl8Li31Nd2O3P3S19", 66))
RIETVELD_CELLPAR = (6.928, 6.928, 34.640, 60.0, 60.0, 60.0)
FORC, ETOT = "1.0d-3", "1.0d-5"
IONS = "&IONS\n    ion_dynamics = 'bfgs'\n/\n"


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def plan_grid(plan=PLAN):
    g = json.loads(Path(plan).read_text())["격자"]["x"]
    return [float(x) for x in g]


def tag(name, x):
    return f"{name}_x{int(round(x * 100)):03d}"


def comp_of(atoms):
    return "".join(f"{e}{c}" for e, c in sorted(Counter(atoms.get_chemical_symbols()).items()))


def cell_block(text):
    m = re.search(r"CELL_PARAMETERS angstrom\n((?:.*\n){3})", text)
    return m.group(0) if m else None


def expected_from_q1(q1_text, new_text):
    """Q1 단일점 입력에 '바뀌어도 되는 것' 만 적용한 글 — 새 입력과 바이트가 같아야 한다."""
    t = q1_text.replace("    calculation = 'scf'\n", "    calculation = 'relax'\n", 1)
    t = t.replace("    etot_conv_thr = 1.0d-6\n", f"    etot_conv_thr = {ETOT}\n", 1)
    t = t.replace("    forc_conv_thr = 1.0d-4\n", f"    forc_conv_thr = {FORC}\n", 1)
    old_c, new_c = cell_block(q1_text), cell_block(new_text)
    if old_c is None or new_c is None:
        return None
    t = t.replace(old_c, new_c, 1)
    i = t.find("&ELECTRONS")
    j = t.find("\n/\n", i)
    return None if i < 0 or j < 0 else t[:j + 3] + IONS + t[j + 3:]


def build(out=None, write=True, xs=None, card_path=CARD, uma=UMA, cand=CAND, q1=Q1, gen=None):
    from ase.io import read
    if gen is None:
        from generate_dft_inputs import generate_pwin as gen
    xs = plan_grid() if xs is None else [float(x) for x in xs]
    card = json.loads(Path(card_path).read_text())
    cfg = MI.card_settings(card)
    pdir = cfg["pseudo_dir"]
    bad, texts, man = [], {}, {"점": {}}
    if not out and write:
        raise SystemExit("⛔ --out 이 필요하다")
    if 1.04 not in [round(x, 6) for x in xs] and xs == plan_grid():
        bad.append("격자에 1.04 (바닥 확인 기준점) 가 없다")
    hosts = {}
    for kind, name, formula, nat in TARGETS:
        hp = Path(cand) / kind / f"{name}.xyz"
        host = read(hp)
        cp = host.cell.cellpar()
        if not np.allclose(cp, RIETVELD_CELLPAR, atol=1e-3):
            bad.append(f"{name} Rietveld 셀 {np.round(cp, 4).tolist()} ≠ {list(RIETVELD_CELLPAR)}")
        hosts[name] = host.cell.array.copy()
        src = Path(uma) / "structures" / f"{name}.xyz"
        at = read(src)
        if comp_of(at) != formula or len(at) != nat:
            bad.append(f"{name} 조성 {comp_of(at)} ({len(at)} 원자) ≠ Q1 {formula} ({nat})")
        q1_in = Path(q1) / name / "scf.in"
        q1_text = q1_in.read_text()
        frac = at.get_scaled_positions(wrap=True)
        H = hosts[name]
        VR = abs(np.linalg.det(H))
        for x in xs:
            a2 = at.copy()
            a2.set_cell(H * x ** (1.0 / 3.0), scale_atoms=False)
            a2.set_scaled_positions(frac)
            try:
                t = gen(a2, name, cfg["ecutwfc"], cfg["ecutrho"], cfg["kpoints"], pseudo_dir=pdir,
                        pp_names=cfg["pp"], calculation="relax", nosym=True,
                        smearing=cfg["smearing"], degauss=cfg["degauss"],
                        conv_thr=cfg["conv_thr"], mixing_beta=cfg["mixing_beta"])
            except ValueError as ex:
                bad.append(f"{tag(name, x)}: {ex}")
                continue
            n_cell = len(re.findall(r"^&CELL\n(?:.*\n)*?/\n", t, re.M))
            t = re.sub(r"^&CELL\n(?:.*\n)*?/\n", "", t, flags=re.M)
            t = t.replace("    etot_conv_thr = 1.0d-6\n", f"    etot_conv_thr = {ETOT}\n", 1)
            t = t.replace("    forc_conv_thr = 1.0d-4\n", f"    forc_conv_thr = {FORC}\n", 1)
            tg = tag(name, x)
            if n_cell != 1 or "&CELL" in t:
                bad.append(f"{tg}: &CELL 블록을 정확히 하나 지우지 못했다 ({n_cell})")
            for key, val in (("etot_conv_thr", ETOT), ("forc_conv_thr", FORC)):
                if re.findall(rf"^\s*{key}\s*=\s*(\S+)", t, re.M) != [val]:
                    bad.append(f"{tg}: {key} ≠ {val}")
            if t.count(IONS) != 1:
                bad.append(f"{tg}: &IONS bfgs 블록이 하나가 아니다")
            bad += [f"{tg}: {b}" for b in MI.check_input(t, cfg, pdir, "relax", nat, cfg["kpoints"])]
            cb = cell_block(t)
            M = np.array([[float(v) for v in ln.split()] for ln in cb.splitlines()[1:4]]) if cb else None
            if M is None or abs(abs(np.linalg.det(M)) / (x * VR) - 1) > 1e-9:
                bad.append(f"{tg}: 부피가 x × V_Rietveld 가 아니다")
            else:
                ang = [np.degrees(np.arccos(np.dot(M[i], M[j]) / np.linalg.norm(M[i]) / np.linalg.norm(M[j])))
                       for i, j in ((1, 2), (0, 2), (0, 1))]
                if not np.allclose(ang, 60.0, atol=1e-6):
                    bad.append(f"{tg}: 각이 60° 가 아니다 {np.round(ang, 6).tolist()}")
            exp = expected_from_q1(q1_text, t)
            if exp is None or exp != t:
                bad.append(f"{tg}: Q1 단일점 입력에서 정해진 곳 (calculation · 문턱 · CELL · &IONS) 밖이 바뀌었다")
            texts[tg] = t
            man["점"][tg] = {"이름": name, "종류": kind, "x": x, "V_A3": round(x * VR, 6),
                            "셀_길이_A": [round(float(v), 6) for v in np.linalg.norm(H * x ** (1 / 3), axis=1)],
                            "원자": nat, "조성": formula}
    if bad:
        raise SystemExit("⛔ 입력을 쓰지 않았다 —\n   " + "\n   ".join(bad))
    man.update({"카드": str(Path(card_path).relative_to(REPO)) if Path(card_path).is_relative_to(REPO) else str(card_path),
                "카드_sha256": sha256(card_path), "설계": "db/inputs/ndo_site_eos_2026_10_16/eos_plan.json",
                "설계_sha256": sha256(PLAN), "설정_카드_6": cfg, "격자_x": xs,
                "relax": {"forc_conv_thr": FORC, "etot_conv_thr": ETOT, "nstep": 200, "ion_dynamics": "bfgs", "CELL": "없음"},
                "생성_함수": "tools/doping/generate_dft_inputs.py::generate_pwin (+ &CELL 제거 · 문턱 두 줄)",
                "생성_함수_sha256": sha256(REPO / "tools/doping/generate_dft_inputs.py"),
                "출처": {name: {"UMA_구조": f"db/raw/ndo_site_2026_10_14/uma_rietveld_2026_10_15/structures/{name}.xyz",
                                "UMA_구조_sha256": sha256(Path(uma) / "structures" / f"{name}.xyz"),
                                "Rietveld_셀": f"db/inputs/ndo_site_2026_10_14/candidates/{kind}/{name}.xyz",
                                "Rietveld_셀_sha256": sha256(Path(cand) / kind / f"{name}.xyz"),
                                "Q1_입력_sha256": sha256(Path(q1) / name / "scf.in")}
                         for kind, name, _, _ in TARGETS}})
    for tg, t in texts.items():
        man["점"][tg]["입력_sha256"] = hashlib.sha256(t.encode()).hexdigest()
    if write:
        o = Path(out)
        for tg, t in texts.items():
            (o / tg).mkdir(parents=True, exist_ok=True)
            (o / tg / "scf.in").write_text(t)
        mp = o / ("inputs_manifest.json" if xs == plan_grid() else f"inputs_manifest_extra_{'_'.join(tag('x', x)[2:] for x in xs)}.json")
        mp.write_text(json.dumps(man, ensure_ascii=False, indent=2) + "\n")
    return man, texts


def _selftest():
    import copy
    import shutil
    import tempfile
    ok = []

    def chk(c, m):
        ok.append(bool(c))
        print(("  ✓ " if c else "  ✗ ") + m)

    def must_stop(fn, m, needle):
        try:
            fn()
        except SystemExit as ex:
            chk(needle in str(ex), m + f" — {str(ex).splitlines()[-1].strip()[:90]}")
            return
        chk(False, m + " → 멈추지 않았다")

    man, texts = build(write=False)
    chk(len(texts) == 12 and sorted({m["이름"] for m in man["점"].values()}) == ["MLi_04", "MP_07"], f"입력 12 개 (2 셀 × 6 부피) — {len(texts)}")
    chk([m["x"] for m in man["점"].values() if m["이름"] == "MP_07"] == [0.98, 1.0, 1.02, 1.04, 1.06, 1.08], "격자 0.98 … 1.08 (eos_plan.json)")
    chk(all("calculation = 'relax'" in t and "&CELL" not in t and t.count(IONS) == 1 for t in texts.values()), "전부 relax · &CELL 없음 · &IONS bfgs 하나")
    chk(all(abs(m["V_A3"] / (m["x"] * 1175.662) - 1) < 1e-5 for m in man["점"].values()), "부피 = x × 1175.66 Å³")
    keys = "ecutwfc|ecutrho|occupations|smearing|degauss|nosym|conv_thr|mixing_mode|mixing_beta|electron_maxstep|diagonalization|nspin"
    sig = lambda t: tuple(sorted(re.sub(r"\s", "", x) for x in re.findall(rf"^ *(?:{keys}) *=.*$", t, re.M)))  # noqa: E731
    q1sig = sig((Q1 / "MP_07" / "scf.in").read_text())
    chk(all(sig(t) == q1sig for t in texts.values()), "러너 설정 균일성 키가 12 개 모두 Q1 단일점과 같다")
    t0 = texts["MP_07_x104"]
    pos_new = re.search(r"ATOMIC_POSITIONS crystal\n(.*?)K_POINTS", t0, re.S).group(1)
    pos_q1 = re.search(r"ATOMIC_POSITIONS crystal\n(.*?)K_POINTS", (Q1 / "MP_07" / "scf.in").read_text(), re.S).group(1)
    chk(pos_new == pos_q1, "좌표 줄이 Q1 단일점 입력과 바이트가 같다 (분율 좌표 그대로)")
    # ── 음성 ──
    tmp = Path(tempfile.mkdtemp())
    try:
        c2 = tmp / "cand"
        shutil.copytree(CAND, c2)
        from ase.io import read, write as awrite
        a = read(c2 / "MP" / "MP_07.xyz")
        cp = a.cell.cellpar()
        cp[5] = 59.0
        a.set_cell(cp, scale_atoms=True)
        awrite(c2 / "MP" / "MP_07.xyz", a)
        must_stop(lambda: build(write=False, cand=c2), "[음성] Rietveld 셀 각이 59° 면 멈춘다", "Rietveld 셀")
        u2 = tmp / "uma"
        (u2 / "structures").mkdir(parents=True)
        for f in (UMA / "structures").glob("*.xyz"):
            (u2 / "structures" / f.name).write_bytes(f.read_bytes())
        (u2 / "structures" / "MLi_04.xyz").write_bytes((UMA / "structures" / "MP_07.xyz").read_bytes())
        must_stop(lambda: build(write=False, uma=u2), "[음성] MLi_04 자리에 MP_07 구조가 끼면 (조성 다름) 멈춘다", "조성")
        q2 = tmp / "q1"
        shutil.copytree(Q1, q2)
        p = q2 / "MP_07" / "scf.in"
        lines = p.read_text().splitlines(keepends=True)
        k = next(i for i, ln in enumerate(lines) if ln.startswith("ATOMIC_POSITIONS"))
        lines[k + 1] = lines[k + 1].replace("0.", "0.1", 1)
        p.write_text("".join(lines))
        must_stop(lambda: build(write=False, q1=q2), "[음성] Q1 입력과 좌표 한 줄이 다르면 멈춘다", "Q1 단일점 입력에서")
        import generate_dft_inputs as g
        orig = g.generate_pwin
        must_stop(lambda: build(write=False, gen=lambda *a, **k: orig(*a, **{**k, "degauss": 0.02})),
                  "[음성] 생성 함수가 degauss 를 바꾸면 멈춘다", "degauss")
        must_stop(lambda: build(write=False, gen=lambda *a, **k: orig(*a, **k).replace("&CELL\n", "&CELL \n")),
                  "[음성] &CELL 블록을 못 지우면 멈춘다", "&CELL")
        must_stop(lambda: build(write=False, gen=lambda *a, **k: orig(*a, **{**k, "calculation": "vc-relax"})),
                  "[음성] 생성 결과가 vc-relax 면 멈춘다", "calculation")
        cardp = tmp / "card.json"
        cj = json.loads(CARD.read_text())
        cj2 = copy.deepcopy(cj)
        cj2["6_규약_대조"]["계산_설정"]["K_POINTS"] = "automatic 3 3 1 0 0 0"
        cardp.write_text(json.dumps(cj2, ensure_ascii=False))
        must_stop(lambda: build(write=False, card_path=cardp), "[음성] 카드 k 가 Q1 과 달라지면 (Q1 입력과 어긋남) 멈춘다", "Q1 단일점 입력에서")
        m3, t3 = build(write=False, xs=[0.96])
        chk(sorted(t3) == ["MLi_04_x096", "MP_07_x096"], "--extra 0.96 은 두 셀 끝점 하나씩만 만든다")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"selftest: {sum(ok)}/{len(ok)}")
    return 0 if all(ok) else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--extra", nargs="+", type=float, help="끝점 연장 (eos_plan.json 규칙이 발동했을 때만)")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    man, texts = build(a.out, xs=a.extra)
    print(f"입력 {len(texts)} 개 → {a.out}")
    for tg, m in man["점"].items():
        print(f"  {tg}  x {m['x']:.2f}  V {m['V_A3']:.3f} Å³  셀 {m['셀_길이_A']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
