#!/usr/bin/env python3
"""build_neb_inputs.py — SEI 분해상의 **Li 공공 매개 이동** CI-NEB 입력을 만든다.

왜 NEB 인가 (2026-08-06 판정)
  BVSE 는 화학계를 넘나드는 비교에 못 쓴다 — 하필 Figure 5 의 주인공인 Li₂S(BVS 1.56)·
  LiCl(2.74) 이 못 쓰는 쪽이고 Li₃P 는 파라미터 자체가 없다. 그래서 NEB 이 대안이 아니라
  **유일한 경로**다. 대상 3종은 논증 축 그대로다:
    Li₂S      = 공통 산물
    Li₃P      = NdO 도핑으로 **줄어든** 것 (전자 절연 0.709 eV 로 제일 나쁜 상)
    Li₃PO₄ γ  = NdO 도핑으로 **생긴** 것
  ⛔ Nd 상은 하지 않는다 — 갭조차 정의 안 되는 계에서 안장점을 믿을 수 없다(§Nd 판정).
  ⛔ Li₃PO₄ β 는 안 한다 — BVSE 에서 β 0.100 vs γ 0.092(8% 차)로 다형체가 결론을 안 바꾼다.

기구: **공공 매개(vacancy-mediated)**. Li 하나를 빼고, 그 빈자리로 최근접 Li 가 뛴다.
  · 처음: 공공 A · Li 는 B 에 있음
  · 끝  : Li 가 A 로 이동 · 공공은 B
  같은 원자 목록을 쓰고 **좌표 하나만** 바꾼다 (QE NEB 은 first/last 의 원자 순서가 같아야 한다).

⚠⚠ 두 개의 함정을 코드가 직접 막는다
  ① **주기 경계**: 뛰는 거리가 셀 경계를 넘으면 감싼 좌표(wrapped)를 그대로 끝점으로 쓰면
    NEB 이 셀을 한 바퀴 도는 엉뚱한 경로를 만든다. 끝점은 반드시
    `시작점 + 최소이미지 벡터` 로 쓴다 (감싸지 않은 좌표).
  ② **전하**: 중성 Li 를 빼면 넓은 갭 절연체의 원자가띠에 정공이 생겨 계가 가짜 금속이 된다.
    Li⁺ 를 빼는 게 맞다 → `tot_charge = +1` (jellium 보정). 닫힌 껍질이 유지된다.
    ⚠ jellium 은 유한 셀 보정이 근사다 — 셀을 충분히 키워 공공-공공 상호작용을 줄인다.

  python3 tools/sei/build_neb_inputs.py --plan          # 비용만 먼저 본다 (실행 안 함)
  python3 tools/sei/build_neb_inputs.py
  python3 tools/sei/build_neb_inputs.py --min_l 12 --images 9
"""
import argparse
import glob
import os
import sys

import numpy as np

WORK = os.environ.get("WORK", "/data/work/runs/sei_neb")
# 갭 계산과 **같은 사양**을 쓴다 — 다른 축과 섞어 쓸 수 있어야 한다
ECUTWFC, ECUTRHO = 60.0, 480.0
TARGETS = {                       # tag → (구조 파일 glob, 표시명)
    "li2s":    ("db/structures/sei_li2s_mp-1153.vasp", "Li2S"),
    "li3p":    ("db/structures/sei_li3p_mp-736.vasp", "Li3P"),
    "li3po4g": ("db/structures/sei_li3po4g_mp-2878.vasp", "Li3PO4-gamma"),
}


def zval(upf):
    import re
    try:
        t = open(upf, errors="ignore").read(400000)
    except OSError:
        return None
    m = re.search(r'z_valence\s*=\s*"?\s*([\d.eE+-]+)', t, re.I)
    if not m:
        m = re.search(r"([\d.eE+-]+)\s+Z valence", t, re.I)
    return float(m.group(1)) if m else None


def find_pseudos(pdir):
    pool = {}
    if not os.path.isdir(pdir):
        return pool
    for f in sorted(os.listdir(pdir)):
        if not f.lower().endswith(".upf"):
            continue
        el = f.split(".")[0].split("_")[0].capitalize()
        pool.setdefault(el, f)
    return pool


def kmesh(cell, dens=0.03):
    """역격자 밀도 기준 k 메쉬. ⚠ round 가 아니라 ceil — 0 이나 1 로 무너지면 안 된다."""
    rec = np.linalg.norm(np.linalg.inv(cell).T, axis=1)
    return [max(1, int(np.ceil(r / dens))) for r in rec]


def pick_hop(at, min_sep=None):
    """공공 자리 A 와 그리로 뛸 Li B 를 고른다.

    최근접 Li–Li 쌍을 쓴다 = **기본 홉**. 더 긴 경로는 이것들의 조합이므로 먼저 이걸 잰다.
    ⚠ 끝점은 감싼 좌표가 아니라 `pos[B] + 최소이미지 벡터` 로 만든다(위 함정 ①).
    """
    sym = at.get_chemical_symbols()
    li = [i for i, s in enumerate(sym) if s == "Li"]
    if len(li) < 2:
        return None
    D = at.get_all_distances(mic=True)
    best = None
    for n, i in enumerate(li):
        for j in li[n + 1:]:
            d = D[i][j]
            if best is None or d < best[0]:
                best = (d, i, j)
    d, A, B = best
    # 최소이미지 변위 벡터 (B → A). ASE 의 get_distance(vector=True) 가 mic 을 처리한다.
    vec = at.get_distance(B, A, mic=True, vector=True)
    return {"d": float(d), "vac": A, "hop": B, "vec": np.asarray(vec, float)}


def build(tag, path, disp, a, pool):
    from ase.io import read
    at0 = read(path)
    L = at0.cell.lengths()
    rep = tuple(max(1, int(np.ceil(a.min_l / x))) for x in L)
    at = at0.repeat(rep)
    els = sorted(set(at.get_chemical_symbols()))
    miss = [e for e in els if e not in pool]
    if miss:
        return {"tag": tag, "skip": f"pseudo 없음: {','.join(miss)}"}

    hop = pick_hop(at)
    if hop is None:
        return {"tag": tag, "skip": "Li 가 2개 미만"}

    # 전자 수 = (완전 셀) − (뺀 Li 의 z_valence) − (tot_charge 1)
    #   Li 원자를 지우면 QE 는 그 z_valence 만큼 전자를 뺀다 = 중성 Li 제거.
    #   거기에 tot_charge=+1 로 전자를 하나 더 빼야 **Li⁺** 를 뺀 게 된다.
    #   그래야 닫힌 껍질이 유지되고 원자가띠에 정공이 안 생긴다 (아래 함정 ②).
    nelec_full = sum(zval(os.path.join(a.pseudo_dir, pool[s])) or 0
                     for s in at.get_chemical_symbols())
    z_li = zval(os.path.join(a.pseudo_dir, pool["Li"])) or 3.0
    nelec_vac = nelec_full - z_li - 1.0
    nat = len(at) - 1

    info = {"tag": tag, "disp": disp, "rep": rep, "nat": nat,
            "cell": at.cell.array.copy(), "els": els,
            "hop_d": hop["d"], "nelec": nelec_vac,
            "L": at.cell.lengths().round(2).tolist(),
            "kpts": kmesh(at.cell.array, a.kdens)}
    if a.plan:
        return info

    # ── 좌표 두 벌 (원자 순서 동일, 좌표 하나만 다름) ────────────────────────
    pos = at.get_positions().copy()
    sym = at.get_chemical_symbols()
    vac, hopi = hop["vac"], hop["hop"]
    start = pos[hopi].copy()
    end = start + hop["vec"]                  # ⚠ 감싸지 않은 끝점 (함정 ①)
    keep = [i for i in range(len(at)) if i != vac]

    first = [(sym[i], pos[i]) for i in keep]
    last = [(sym[i], end if i == hopi else pos[i]) for i in keep]
    # 검산: 마지막 이미지에서 뛴 Li 가 공공 자리에 도달했나 (최소이미지 기준)
    err = np.linalg.norm(end - pos[vac])
    cellv = at.cell.array
    for s in (-1, 0, 1):
        for t in (-1, 0, 1):
            for u in (-1, 0, 1):
                err = min(err, np.linalg.norm(end - (pos[vac] + s * cellv[0]
                                                     + t * cellv[1] + u * cellv[2])))
    info["arrival_err"] = float(err)

    d = os.path.join(a.work, tag)
    os.makedirs(d, exist_ok=True)
    from ase.data import atomic_masses, atomic_numbers

    def block(imgs):
        s = "ATOMIC_POSITIONS angstrom\n"
        for e, p in imgs:
            s += f"  {e:3s} %16.10f %16.10f %16.10f\n" % tuple(p)
        return s

    body = ["BEGIN", "BEGIN_PATH_INPUT", "&PATH",
            "  string_method   = 'neb'",
            f"  nstep_path      = {a.nstep}",
            "  opt_scheme      = 'broyden'",
            f"  num_of_images   = {a.images}",
            "  k_max           = 0.3", "  k_min           = 0.2",
            # CI = climbing image. 안장점을 직접 올라타므로 barrier 가 이미지 격자에
            # 안 걸린다 — 'auto' 는 첫 몇 스텝 뒤 최고점 이미지를 자동 지정한다.
            "  CI_scheme       = 'auto'",
            f"  path_thr        = {a.path_thr}",
            "/", "END_PATH_INPUT", "BEGIN_ENGINE_INPUT",
            "&CONTROL", "    calculation     = 'scf'",
            f"    prefix          = '{tag}'", "    outdir          = './tmp'",
            f"    pseudo_dir      = '{a.pseudo_dir}'",
            "    tprnfor         = .true.", "/",
            "&SYSTEM", "    ibrav           = 0", f"    nat             = {nat}",
            f"    ntyp            = {len(els)}",
            f"    ecutwfc         = {ECUTWFC}", f"    ecutrho         = {ECUTRHO}",
            # ★ Li⁺ 를 뺐으므로 전자도 하나 적다. 중성으로 두면 원자가띠에 정공이 생겨
            #   넓은 갭 절연체가 가짜 금속이 된다 (위 함정 ②).
            "    tot_charge      = 1.0",
            "    occupations     = 'smearing'", "    smearing        = 'gaussian'",
            "    degauss         = 0.005", "/",
            "&ELECTRONS", "    conv_thr        = 1.0d-8",
            "    mixing_beta     = 0.3", "    electron_maxstep = 200", "/",
            "", "ATOMIC_SPECIES"]
    for e in els:
        body.append(f"  {e:3s} {atomic_masses[atomic_numbers[e]]:8.3f}  {pool[e]}")
    body += ["", "BEGIN_POSITIONS", "FIRST_IMAGE", block(first).rstrip(),
             "LAST_IMAGE", block(last).rstrip(), "END_POSITIONS", ""]
    body.append("K_POINTS automatic")
    body.append("  %d %d %d 0 0 0" % tuple(info["kpts"]))
    body += ["", "CELL_PARAMETERS angstrom"]
    for v in at.cell.array:
        body.append("  %16.10f %16.10f %16.10f" % tuple(v))
    body += ["END_ENGINE_INPUT", "END", ""]
    open(os.path.join(d, "neb.in"), "w").write("\n".join(body))

    # 사람이 눈으로 검산할 수 있게 두 끝 이미지를 구조 파일로도 남긴다
    from ase import Atoms
    from ase.io import write
    for name, imgs in (("initial", first), ("final", last)):
        write(os.path.join(d, f"{name}.xyz"),
              Atoms(symbols=[e for e, _ in imgs],
                    positions=[p for _, p in imgs], cell=at.cell, pbc=True))
    return info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default=WORK)
    ap.add_argument("--pseudo_dir", default="/data/work/pseudo")
    ap.add_argument("--min_l", type=float, default=10.0,
                    help="셀 축 최소 길이 [Å] — 공공-공공 주기 상호작용을 줄인다")
    ap.add_argument("--images", type=int, default=7, help="NEB 이미지 수 (끝 2개 포함)")
    ap.add_argument("--nstep", type=int, default=100)
    ap.add_argument("--path_thr", type=float, default=0.05, help="경로 수렴 [eV/Å]")
    ap.add_argument("--kdens", type=float, default=0.04,
                    help="k 밀도 [Å⁻¹] — 슈퍼셀이라 성기게 잡는다")
    ap.add_argument("--only", nargs="*", help="일부만")
    ap.add_argument("--plan", action="store_true",
                    help="⚠ 비용만 보고 **입력을 만들지 않는다** (돌리기 전에 이걸 먼저)")
    a = ap.parse_args()

    pool = find_pseudos(a.pseudo_dir)
    print(f"pseudo 디렉터리 {a.pseudo_dir}" + ("" if pool else "  ⚠ 비어 있다"))
    for e, f in sorted(pool.items()):
        print(f"  {e:3s} {f}")
    if not a.plan:
        os.makedirs(a.work, exist_ok=True)

    rows = []
    for tag, (path, disp) in TARGETS.items():
        if a.only and tag not in a.only:
            continue
        if not os.path.isfile(path):
            print(f"\n⛔ {tag}: 구조 없음 — {path}")
            continue
        r = build(tag, path, disp, a, pool)
        rows.append(r)
        if r.get("skip"):
            print(f"\n⏭  {tag:10s} {r['skip']}")
            continue
        print(f"\n{'(계획)' if a.plan else '✓'} {tag:10s} {r['disp']:16s} "
              f"{r['rep'][0]}×{r['rep'][1]}×{r['rep'][2]} → {r['nat']:4d}원자 "
              f"(공공 1개 제거) · 셀 {r['L']} Å")
        print(f"     최근접 Li–Li 홉 {r['hop_d']:.3f} Å · 전자 {r['nelec']:.0f} "
              f"· k {r['kpts']} · 이미지 {a.images}")
        if "arrival_err" in r:
            ok = r["arrival_err"] < 1e-6
            print(f"     끝점 검산: 뛴 Li 가 공공 자리에 도달 "
                  f"{'✅' if ok else '⛔ 오차 %.4f Å' % r['arrival_err']}")

    if a.plan:
        print("\n" + "═" * 72)
        print("⚠ 계획 모드다 — 입력을 만들지 않았다. 비용을 보고 판단할 것:")
        print("   NEB 은 이미지마다 SCF 를 돌린다 = 대략 (이미지 수) × (scf 1회) × (경로 스텝).")
        print("   원자·전자 수가 위 표다. 너무 크면 --min_l 을 줄이되, 공공-공공 거리가")
        print("   짧아지면 장벽이 오염된다는 걸 기억할 것.")
        print("   진행하려면 --plan 을 빼고 다시 실행한다.")
        return 0

    print("\n" + "═" * 72)
    print(f"→ {a.work}")
    print("실행:  bash tools/sei/run_sei_neb.sh")
    print("⚠ 돌리기 전에 initial.xyz / final.xyz 를 VESTA 로 열어 **경로가 셀을 가로지르지")
    print("  않는지** 눈으로 볼 것 — 주기 경계를 넘는 홉은 코드가 최소이미지로 폈지만,")
    print("  뛴 Li 가 다른 원자를 관통하는 경로면 중간 이미지가 무너진다.")
    print("⚠ tot_charge=+1 (Li⁺ 공공) 이다. jellium 보정은 유한 셀 근사라 셀 크기 의존이 남는다")
    print("  — 장벽의 **상 사이 비교**에는 쓰되 절대값은 셀 수렴을 확인하고 인용할 것.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
