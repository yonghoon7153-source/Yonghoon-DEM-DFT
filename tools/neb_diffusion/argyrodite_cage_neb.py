#!/usr/bin/env python3
"""argyrodite_cage_neb.py — argyrodite **벌크 Li 공공 hop** 의 CI-NEB (UMA).

왜 새 파일인가 (2026-08-19, 코드 규율 사다리 ①~④ 확인)
  `tools/neb_diffusion/` 의 기존 NEB 는 전부 **Li₃N / LiC6 표면 adatom** 용이다
  (`li3n_seeded_neb.py`, `adatom_diffusion.py`, `li3n_uma_investigate.py`).
  거기엔 슬래브 고정·adatom 3-DOF 가 박혀 있어 벌크 공공 hop 에 못 쓴다.
  `tools/sei/run_sei_neb.sh` 는 QE `neb.x` (DFT) 라 다른 엔진이다.
  `tools/ionic/cage_jump_descriptors.py` 는 **케이지 기하 기술자**(NEB 없음) —
  케이지 판정 규약(PS4 결합 2.30 Å, 자유 음이온 = 케이지 중심)은 거기서 가져왔다.

무엇을 하나
  ① 케이지 중심(자유 S + Cl)을 잡고 Li 를 케이지에 배정
  ② **intra-cage**(같은 케이지) / **inter-cage**(다른 케이지) hop 짝을 고른다
  ③ 공공 하나(Li 제거) + 이웃 Li 를 그 자리로 → 두 끝점을 **위치만** 이완
  ④ IDPP 보간 → NEB → CI-NEB, 장벽 = max(E) − E(시작)

⭐ **셀은 절대 이완하지 않는다.** 2026-08-19 실측: UMA 는 canonical Li₆PS₅Cl 셀을
   +32.7 %(27.478 Å³/atom) 로 부풀린다. argyrodite 장벽은 부피에 극도로 민감해서
   (Wu 2026 이 26 % 팽창 격자에서 NEB 를 돌린 것을 우리가 지적했다) 셀을 풀면
   장벽이 의미를 잃는다. **DFT V0 셀에서 출발하고 고정한다.**

⚠ 이미지 거리. 60° 셀은 `|a|` 와 실제 이미지 거리가 다르다 — modelC 계열은
   |a|=6.98 인데 **수직폭 5.70 Å** 다. inter-cage hop 이 ~4 Å 이므로 그대로 쓰면
   이동 Li 가 자기 이미지와 겹친다. 이 도구는 수직폭을 **항상 같이 찍고**,
   `--min_width` 아래면 **거부한다**(`--force` 로만 통과).

이 도구가 **못 하는 것**
  · DFT 가 아니다. UMA-s-1p1(omat) 이다. 절대 장벽을 DFT/실험과 등가로 인용 금지.
  · **단일 배열·단일 경로**다. 무질서계의 유효 장벽은 배열 앙상블의 최소경로가
    지배한다 — Wu 2026 의 NEB 0.59 eV vs 자기 EIS 0.32 eV 불일치가 그 사례다.
    앙상블은 `--seeds` 로 여러 짝을 돌려 **분포**로 보고할 것.
  · 전하 보상을 하지 않는다(UMA 는 전하를 모른다). Li 하나를 그냥 뺀다.
  · 케이지 배정은 **최근접 자유음이온**이다. 경계 Li 는 애매할 수 있다 —
    `cage_margin` 으로 애매한 짝을 걸러낸다.
  · 협동 이동(다중 Li 동시)을 못 본다. 단일 Li 경로만 본다.

  python3 tools/neb_diffusion/argyrodite_cage_neb.py --selftest
  # 셀 수렴 시험 (comp1, cubic)
  python3 tools/neb_diffusion/argyrodite_cage_neb.py \
      --struct db/structures/comp1_V0_k444.cif --kind inter \
      --supercell 1 1 1 --force --tag conv_111
"""
import argparse, json, os, sys, time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUTDIR = ROOT / "db" / "properties"

#: cage_jump_descriptors.py 와 같은 값 — P–S 결합 판정 (PS4 는 2.04–2.11 Å)
PS_BOND = 2.30
#: 이미지 거리 하한 (수직폭). 4 Å hop 의 2.5배 여유. 아래면 거부한다.
MIN_WIDTH_A = 10.0
#: NEB 기본값
N_IMAGES = 7          # 내부 이미지 (끝점 제외)
FMAX_ENDPOINT = 0.03
FMAX_NEB = 0.05
FMAX_CI = 0.03
STEPS_NEB = 400
SPRING_K = 0.1
#: ⚠ ASE 3.29 는 기본 탄젠트가 'aseneb'(비권장, 밴드가 자주 망가짐)라고 스스로 경고한다.
#: 명시적으로 improvedtangent 를 쓴다 (Henkelman 2000). 재현성을 위해 기록도 남긴다.
NEB_METHOD = "improvedtangent"


# ── 기하 ─────────────────────────────────────────────────────────────────────
def perp_widths(cell):
    """면간 **수직거리** d_i = V / |a_j × a_k|.

    ⚠ `|a_i|` 가 아니다. α=β=γ=60° 셀에서 둘은 크게 다르다 (6.98 vs 5.70 Å).
    """
    c = np.asarray(cell, float)
    V = abs(np.linalg.det(c))
    return np.array([V / np.linalg.norm(np.cross(c[(i + 1) % 3], c[(i + 2) % 3]))
                     for i in range(3)])


def mic_vec(atoms, i, j):
    """i → j 최소이미지 벡터 (데카르트)."""
    c = np.array(atoms.cell)
    d = atoms.positions[j] - atoms.positions[i]
    f = np.linalg.solve(c.T, d)
    f -= np.round(f)
    return f @ c


def cage_assign(atoms):
    """(케이지중심 인덱스, Li 인덱스, Li→케이지 배정, Li–중심 거리).

    케이지 중심 = **자유 음이온** = P 와 결합하지 않은 S + 모든 Cl (+Br/I/O 는
    할라이드 자리에 있을 수 있으므로 같이 센다). cage_jump_descriptors 규약.
    """
    sym = np.array(atoms.get_chemical_symbols())
    P = np.where(sym == "P")[0]
    S = np.where(sym == "S")[0]
    HAL = np.where(np.isin(sym, ["Cl", "Br", "I"]))[0]
    Li = np.where(sym == "Li")[0]
    if len(Li) == 0:
        raise ValueError("Li 가 없다 — argyrodite 가 아니다")
    bonded = set()
    if len(P) and len(S):
        D = atoms.get_all_distances(mic=True)
        for p in P:
            bonded.update(int(s) for s in S[D[p, S] < PS_BOND])
    freeS = np.array([s for s in S if s not in bonded], int)
    centers = np.concatenate([freeS, HAL]).astype(int)
    if len(centers) == 0:
        raise ValueError("케이지 중심(자유 음이온)이 없다 — PS_BOND 를 확인할 것")
    D = atoms.get_all_distances(mic=True)
    sub = D[np.ix_(Li, centers)]
    assign = np.argmin(sub, axis=1)
    return centers, Li, assign, sub[np.arange(len(Li)), assign]


def find_hops(atoms, kind, rmax=5.0, cage_margin=0.3):
    """(i, j, 거리) 후보 목록. kind: 'intra' 같은 케이지 · 'inter' 다른 케이지.

    `cage_margin`: 두 케이지 중심까지 거리 차가 이보다 작은 Li 는 **배정이 애매**하므로
    뺀다 (경계 Li 를 inter/intra 로 잘못 부르지 않기 위해).
    """
    centers, Li, assign, _ = cage_assign(atoms)
    D = atoms.get_all_distances(mic=True)
    sub = D[np.ix_(Li, centers)]
    srt = np.sort(sub, axis=1)
    ambiguous = (srt[:, 1] - srt[:, 0]) < cage_margin if sub.shape[1] > 1 else \
        np.zeros(len(Li), bool)
    out = []
    for a in range(len(Li)):
        if ambiguous[a]:
            continue
        for b in range(a + 1, len(Li)):
            if ambiguous[b]:
                continue
            d = D[Li[a], Li[b]]
            if d > rmax:
                continue
            same = assign[a] == assign[b]
            if (kind == "intra") != same:
                continue
            out.append((int(Li[a]), int(Li[b]), float(d)))
    out.sort(key=lambda t: (round(t[2], 4), t[0], t[1]))
    return out


def build_endpoints(atoms, i_vac, j_mig):
    """(시작, 끝). 시작 = Li_i 제거. 끝 = 거기서 Li_j 를 i 자리로 옮긴 것.

    **원자 목록·인덱스가 두 끝점에서 동일**해야 NEB 보간이 성립한다. 그래서
    한쪽에서만 원자를 빼고, 다른 쪽은 그 결과를 복사해 위치만 바꾼다.
    이동은 **최소이미지 벡터**로 하므로 셀 경계를 가로지르는 hop 도 짧은 길로 간다.
    """
    if atoms.get_chemical_symbols()[i_vac] != "Li" or \
       atoms.get_chemical_symbols()[j_mig] != "Li":
        raise ValueError("i_vac · j_mig 는 둘 다 Li 여야 한다")
    if i_vac == j_mig:
        raise ValueError("같은 원자를 공공이자 이동체로 쓸 수 없다")
    v = mic_vec(atoms, j_mig, i_vac)          # j → i (짧은 길)
    ini = atoms.copy()
    del ini[i_vac]
    j2 = j_mig - 1 if j_mig > i_vac else j_mig   # 삭제로 밀린 인덱스
    fin = ini.copy()
    fin.positions[j2] = ini.positions[j2] + v
    return ini, fin, j2, float(np.linalg.norm(v))


# ── 실행 ─────────────────────────────────────────────────────────────────────
def load_calc(device="cuda"):
    from fairchem.core import pretrained_mlip, FAIRChemCalculator
    pred = pretrained_mlip.get_predict_unit("uma-s-1p1", device=device)
    return FAIRChemCalculator(pred, task_name="omat")


def relax_positions(atoms, calc, fmax=FMAX_ENDPOINT, steps=800):
    """⭐ **위치만** 이완한다. 셀은 절대 건드리지 않는다 (모듈 docstring 참조)."""
    from ase.optimize import FIRE
    atoms = atoms.copy()
    atoms.calc = calc
    opt = FIRE(atoms, logfile=None)
    opt.run(fmax=fmax, steps=steps)
    return atoms, bool(opt.converged()), int(opt.get_number_of_steps())


def run_neb(ini, fin, calc, n_images=N_IMAGES, climb_from=FMAX_NEB):
    from ase.mep import NEB
    from ase.optimize import FIRE
    images = [ini] + [ini.copy() for _ in range(n_images)] + [fin]
    for im in images:
        im.calc = calc
    neb = NEB(images, k=SPRING_K, climb=False, method=NEB_METHOD,
              allow_shared_calculator=True)
    neb.interpolate("idpp", apply_constraint=False)
    opt = FIRE(neb, logfile=None)
    opt.run(fmax=climb_from, steps=STEPS_NEB)
    neb.climb = True                                    # CI-NEB
    opt2 = FIRE(neb, logfile=None)
    opt2.run(fmax=FMAX_CI, steps=STEPS_NEB)
    E = np.array([im.get_potential_energy() for im in images])
    return images, E, bool(opt2.converged()), int(opt.get_number_of_steps() +
                                                  opt2.get_number_of_steps())


def one_run(args):
    from ase.io import read, write
    base = read(args.struct if os.path.isabs(args.struct) else str(ROOT / args.struct))
    sc = tuple(args.supercell)
    atoms = base.repeat(sc) if sc != (1, 1, 1) else base.copy()
    W = perp_widths(atoms.cell)
    print(f"── {Path(args.struct).name}  ×{sc}  n={len(atoms)}  "
          f"수직폭 ({W[0]:.2f}, {W[1]:.2f}, {W[2]:.2f}) Å  최소 {W.min():.2f}")
    if W.min() < args.min_width and not args.force:
        raise SystemExit(f"⛔ 최소 수직폭 {W.min():.2f} Å < {args.min_width} Å — "
                         f"이동 Li 가 자기 이미지와 겹친다. 슈퍼셀을 키우거나 "
                         f"--force (수렴시험 목적이면 정당하다)")

    cands = find_hops(atoms, args.kind, rmax=args.rmax, cage_margin=args.cage_margin)
    if not cands:
        raise SystemExit(f"⛔ '{args.kind}' hop 후보가 없다 (rmax={args.rmax})")
    if args.pair:
        i_vac, j_mig = (int(x) for x in args.pair.split(","))
        d = float(atoms.get_distance(i_vac, j_mig, mic=True))
    else:
        i_vac, j_mig, d = cands[args.pick]
    print(f"   후보 {len(cands)}개 · 선택 ({i_vac}, {j_mig}) d={d:.3f} Å  [{args.kind}]")

    ini0, fin0, j2, hop = build_endpoints(atoms, i_vac, j_mig)
    assert ini0.get_chemical_symbols() == fin0.get_chemical_symbols()

    calc = load_calc(args.device)
    t0 = time.time()
    ini, c1, s1 = relax_positions(ini0, calc)
    fin, c2, s2 = relax_positions(fin0, calc)
    E_i, E_f = ini.get_potential_energy(), fin.get_potential_energy()
    print(f"   끝점 이완: {s1}/{s2} steps  ΔE(끝−시작) = {1000*(E_f-E_i):+.1f} meV")
    images, E, conv, nst = run_neb(ini, fin, calc, args.n_images)
    Ea_f = float(E.max() - E[0])
    Ea_r = float(E.max() - E[-1])
    dt = time.time() - t0

    tag = args.tag or f"{Path(args.struct).stem}_{args.kind}_{sc[0]}{sc[1]}{sc[2]}"
    xyz = OUTDIR / f"neb_{tag}.xyz"
    write(str(xyz), images)
    rec = {
        "tag": tag, "struct": args.struct, "supercell": list(sc),
        "n_atoms": len(atoms), "n_atoms_neb": len(ini),
        "perp_widths_A": [round(float(x), 3) for x in W],
        "min_perp_width_A": round(float(W.min()), 3),
        "kind": args.kind, "pair": [i_vac, j_mig],
        "pair_distance_A": round(d, 4), "hop_distance_A": round(hop, 4),
        "n_hop_candidates": len(cands),
        "Ea_forward_eV": round(Ea_f, 4), "Ea_reverse_eV": round(Ea_r, 4),
        "dE_endpoints_meV": round(1000 * (E_f - E_i), 2),
        "energies_eV": [round(float(x), 6) for x in E],
        "profile_eV_rel": [round(float(x - E[0]), 4) for x in E],
        "n_images_total": len(images),
        "endpoint_converged": [c1, c2], "neb_converged": conv,
        "neb_steps": nst, "seconds": round(dt, 1),
        "engine": "uma-s-1p1(omat)", "cell_relaxed": False,
        "neb_method": NEB_METHOD, "spring_k": SPRING_K,
        "fmax": {"endpoint": FMAX_ENDPOINT, "neb": FMAX_NEB, "ci": FMAX_CI},
        "images_file": str(xyz),
    }
    print(f"   **Ea(정) {Ea_f:.4f} eV**  Ea(역) {Ea_r:.4f} eV   "
          f"({nst} steps, {'수렴' if conv else '미수렴'}, {dt:.0f}s)")
    return rec


# ── selftest ─────────────────────────────────────────────────────────────────
def selftest():
    ok = True

    def chk(c, m):
        nonlocal ok
        print(("  ✓ " if c else "  ✗ ") + m)
        ok &= bool(c)

    # 수직폭 — 양성/음성. 60° 셀에서 |a| 를 쓰면 틀린다는 것을 못 박는다.
    cube = np.eye(3) * 10.0
    chk(np.allclose(perp_widths(cube), 10.0), "[양성] 정육면체 수직폭 = 모서리 길이")
    a = 6.984
    rh = np.array([[a, 0, 0], [a * .5, a * np.sqrt(3) / 2, 0],
                   [a * .5, a / (2 * np.sqrt(3)), a * np.sqrt(2. / 3)]])
    W = perp_widths(rh)
    chk(W.min() < a * 0.95,
        f"[음성] 60° 셀은 수직폭이 |a| 보다 **작다** ({W.min():.2f} < {a})")

    try:
        from ase.io import read
        f = ROOT / "db" / "structures" / "comp1_V0_k444.cif"
        chk(f.exists(), "[전제] comp1_V0_k444.cif 가 있다")
        at = read(f)
        chk(abs(perp_widths(at.cell).min() - 10.06) < 0.05,
            f"[양성] comp1 수직폭 10.06 Å (얻은 것 {perp_widths(at.cell).min():.2f})")
        cen, Li, asg, _ = cage_assign(at)
        chk(len(cen) == 8 and len(Li) == 24,
            f"[양성] 케이지 8개(자유 S 4 + Cl 4) · Li 24 (얻은 것 {len(cen)}, {len(Li)})")
        # ★ 음성 — PS4 의 S 를 케이지 중심으로 세면 안 된다
        chk(len(cen) < (np.array(at.get_chemical_symbols()) == "S").sum(),
            "[음성] PS₄ 결합 S 는 케이지 중심에서 빠진다")
        intra = find_hops(at, "intra"); inter = find_hops(at, "inter")
        chk(len(intra) > 0 and len(inter) > 0,
            f"[양성] intra {len(intra)}개 · inter {len(inter)}개 후보")
        chk(intra[0][2] < inter[0][2],
            f"[양성] 최단 intra({intra[0][2]:.2f}) < 최단 inter({inter[0][2]:.2f}) — "
            "케이지 안이 더 가깝다")
        # 끝점 — 조성 보존 + 인덱스 정렬
        i, j, _ = inter[0]
        ini, fin, j2, hop = build_endpoints(at, i, j)
        chk(ini.get_chemical_symbols() == fin.get_chemical_symbols(),
            "[양성] 두 끝점의 원자 목록이 같다 (NEB 보간 전제)")
        chk(len(ini) == len(at) - 1, "[양성] 공공이 정확히 하나 생긴다")
        moved = np.linalg.norm(fin.positions - ini.positions, axis=1)
        chk(int((moved > 1e-8).sum()) == 1,
            f"[양성] 움직인 원자가 정확히 하나 (얻은 것 {int((moved>1e-8).sum())})")
        chk(abs(moved.max() - hop) < 1e-6 and hop < 5.0,
            f"[양성] 이동거리 = 최소이미지 hop ({hop:.3f} Å)")
        # ★ 음성 — 잘못된 입력을 막아야 한다
        for bad, why in (((i, i), "같은 원자"), ):
            try:
                build_endpoints(at, *bad); chk(False, f"[음성] {why} 를 막지 못했다")
            except ValueError:
                chk(True, f"[음성] {why} 는 ValueError 로 막는다")
        p_idx = int(np.where(np.array(at.get_chemical_symbols()) == "P")[0][0])
        try:
            build_endpoints(at, p_idx, j); chk(False, "[음성] Li 아닌 원자를 막지 못했다")
        except ValueError:
            chk(True, "[음성] Li 가 아닌 자리는 ValueError 로 막는다")
        # ★ 음성 — Li 없는 구조는 케이지 배정이 죽어야 한다
        noli = at[[k for k, s in enumerate(at.get_chemical_symbols()) if s != "Li"]]
        try:
            cage_assign(noli); chk(False, "[음성] Li 없는 구조를 통과시켰다")
        except ValueError:
            chk(True, "[음성] Li 없는 구조는 ValueError")
        # ★ 음성 — 좁은 셀 거부 로직 (min_width 비교 자체)
        chk(perp_widths(read(ROOT / "db" / "structures" /
                             "modelC_DFT_EOS_V0.cif").cell).min() < MIN_WIDTH_A,
            f"[음성] modelC 원본 셀은 {MIN_WIDTH_A} Å 기준에 걸린다 (걸려야 정상)")
    except ImportError:
        print("  ⚠ ase 없음 — 구조 시험 건너뜀")
    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--struct", default="db/structures/comp1_V0_k444.cif")
    ap.add_argument("--supercell", nargs=3, type=int, default=[1, 1, 1])
    ap.add_argument("--kind", choices=["intra", "inter"], default="inter")
    ap.add_argument("--pick", type=int, default=0, help="후보 목록에서 몇 번째 (0=최단)")
    ap.add_argument("--pair", help="'i,j' 로 짝을 직접 지정 (재현·앙상블용)")
    ap.add_argument("--n_images", type=int, default=N_IMAGES)
    ap.add_argument("--rmax", type=float, default=5.0)
    ap.add_argument("--cage_margin", type=float, default=0.3)
    ap.add_argument("--min_width", type=float, default=MIN_WIDTH_A)
    ap.add_argument("--force", action="store_true", help="좁은 셀도 실행 (수렴시험용)")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--tag")
    ap.add_argument("--out", default=str(OUTDIR / "argyrodite_cage_neb.json"))
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    a = ap.parse_args()
    rec = one_run(a)
    p = Path(a.out)
    db = json.loads(p.read_text()) if p.exists() else {
        "what": "UMA-s-1p1(omat) CI-NEB for a single Li vacancy hop in bulk "
                "argyrodite. Cell is NEVER relaxed - see module docstring.",
        "caveat": "Single arrangement, single path. NOT a percolation barrier. "
                  "Absolute values are MLIP, not DFT.",
        "runs": []}
    db["runs"] = [r for r in db.get("runs", []) if r.get("tag") != rec["tag"]] + [rec]
    p.write_text(json.dumps(db, ensure_ascii=False, indent=2))
    print(f"\n→ {p}   (누적 {len(db['runs'])}건)")


if __name__ == "__main__":
    main()
