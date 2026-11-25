#!/usr/bin/env python3
"""check_adsorption_sanity.py — 이완된 복합체가 **흡착인가 반응인가**.

왜 필요한가 (2026-08-06)
  Phase-A 를 `--freeze_frac 1.0`(슬랩 전체 고정)로 돌리면 doped sulfonate E_bind = −0.258 eV
  인데, `0.6`(표면 2개 층 자유)으로 풀면 **−1.089 eV** 로 4.2배 깊어졌다.
  ⚠ 이걸 곧바로 "화학흡착" 이라고 읽으면 **비약**이다. 깊어진 이유가 셋일 수 있다:
    (a) 진짜 화학흡착 — 표면이 분자를 향해 이완하며 결합이 형성됨
    (b) **분자가 깨졌거나 표면에 삽입/O 를 뽑아냄** = 흡착이 아니라 **반응**
        (얼렸을 땐 표면이 못 움직여 이 경로가 막혀 있었다. 풀면 열린다.)
    (c) 슬랩 기준의 **이완이 미수렴** → 기준 에너지가 임의값이라 E_bind 가 통째로 오염
  이 도구는 (b)(c)를 배제해야만 (a)를 주장할 수 있게 한다.

무엇을 보나
  1) **분자 내부 결합 보존** — 가스상 기준 분자와 결합거리를 대조. 끊기거나 새로 생기면 반응이다.
  2) **분자–표면 최단거리** — 화학결합 급(< 2.2 Å)인가 vdW 급(> 2.8 Å)인가, 어느 원자쌍인가.
  3) **표면 이동량** — 복합체의 슬랩부가 **맨 슬랩(같은 구속으로 이완한 것)** 대비 얼마나 움직였나.
     ⚠ 맨 슬랩 자체가 원본(DFT+U)에서 얼마나 움직였는지도 같이 본다 — 그게 크면
       '분자가 끌어당긴 것' 이 아니라 'UMA 가 자기 최소로 간 것' 이다.
  4) 로그에서 **FIRE converged** 확인 안내.

  python3 tools/sdcp/check_adsorption_sanity.py \\
      --complex /data/work/runs/sdcp_v2/phaseA_freeslab/complex_doped_sulfonate_down_r90_g00.xyz \\
      --mol /data/work/runs/sdcp_linio2_binding/inputs/sdcp_v7c/sdcp_v7c_doped.xyz \\
      --slab db/structures/linio2_104_sym_1x4L4_relaxed.vasp
"""
import argparse
import sys

import numpy as np
from ase.io import read

# 공유결합 반경 (Å) — 결합 판정용. 넉넉히 잡고 1.25 배까지 결합으로 본다.
RCOV = {"H": 0.31, "C": 0.76, "N": 0.71, "O": 0.66, "F": 0.57, "S": 1.05, "P": 1.07,
        "Li": 1.28, "Ni": 1.24, "Cl": 1.02, "Si": 1.11, "B": 0.84}


def bonds_of(at, scale=1.25):
    p, s = at.get_positions(), at.get_chemical_symbols()
    out = set()
    for i in range(len(at)):
        for j in range(i + 1, len(at)):
            d = np.linalg.norm(p[i] - p[j])
            if d < scale * (RCOV.get(s[i], 1.0) + RCOV.get(s[j], 1.0)):
                out.add((i, j))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--complex", required=True, help="이완된 복합체 xyz (슬랩 뒤에 분자)")
    ap.add_argument("--mol", required=True, help="가스상 기준 분자 xyz")
    ap.add_argument("--slab", required=True, help="복합체를 만들 때 쓴 원본 슬랩 (DFT+U 이완본)")
    ap.add_argument("--slab-relaxed", help="같은 구속으로 UMA 이완한 맨 슬랩 (있으면 더 정확)")
    a = ap.parse_args()

    cx = read(a.complex)
    mol0 = read(a.mol)
    sl0 = read(a.slab)
    nm, ns = len(mol0), len(sl0)
    if len(cx) != ns + nm:
        sys.exit(f"⛔ 원자수 불일치: 복합체 {len(cx)} != 슬랩 {ns} + 분자 {nm}")
    sl_c, mol_c = cx[:ns], cx[ns:]
    print(f"복합체 {len(cx)} = 슬랩 {ns} + 분자 {nm}")

    # ── 1) 분자 내부 결합 보존 ─────────────────────────────────────────────
    b0, b1 = bonds_of(mol0), bonds_of(mol_c)
    broke, formed = b0 - b1, b1 - b0
    sym = mol0.get_chemical_symbols()
    print(f"\n① 분자 내부 결합  기준 {len(b0)}개 → 이완 후 {len(b1)}개")
    for tag, st in (("끊김", broke), ("새로 생김", formed)):
        for i, j in sorted(st):
            d0 = np.linalg.norm(mol0.positions[i] - mol0.positions[j])
            d1 = np.linalg.norm(mol_c.positions[i] - mol_c.positions[j])
            print(f"   ⛔ {tag}: {sym[i]}{i}–{sym[j]}{j}  {d0:.2f} → {d1:.2f} Å")
    if not broke and not formed:
        print("   ✅ 결합 위상 동일 — 분자가 깨지지 않았다")
    else:
        print("   ⛔ **분자가 변했다 = 흡착이 아니라 반응.** E_bind 를 흡착에너지로 부르면 안 된다.")

    # ── 2) 분자–표면 최단거리 ──────────────────────────────────────────────
    ps, pm = sl_c.get_positions(), mol_c.get_positions()
    ss, sm = sl_c.get_chemical_symbols(), mol_c.get_chemical_symbols()
    d = np.linalg.norm(ps[:, None, :] - pm[None, :, :], axis=2)
    k = np.unravel_index(np.argmin(d), d.shape)
    dmin = d[k]
    print(f"\n② 분자–표면 최단거리 {dmin:.2f} Å  ({ss[k[0]]}(슬랩) ⋯ {sm[k[1]]}{k[1]}(분자))")
    near = sorted({(round(d[i, j], 2), ss[i], sm[j]) for i, j in zip(*np.where(d < 2.8))})[:6]
    for dd, a_, b_ in near:
        print(f"   {dd:.2f} Å  {a_}⋯{b_}")
    if dmin < 2.2:
        print("   → 화학결합 급 거리. ①이 ✅ 라면 **화학흡착**과 정합.")
    elif dmin < 2.8:
        print("   → 경계. 강한 정전/수소결합일 수 있다.")
    else:
        print("   ⚠ vdW 급 거리인데 E_bind 가 깊다면 **에너지의 출처가 접촉이 아니다** — "
              "슬랩 이완 몫이 섞였을 가능성(③ 확인).")

    # ── 3) 표면이 얼마나 움직였나 ──────────────────────────────────────────
    dv_orig = np.linalg.norm(sl_c.get_positions() - sl0.get_positions(), axis=1)
    print(f"\n③ 표면 이동량 (복합체 슬랩부 vs 원본 DFT+U 슬랩)  최대 {dv_orig.max():.3f} Å "
          f"· 평균 {dv_orig.mean():.3f}")
    if a.slab_relaxed:
        slr = read(a.slab_relaxed)
        base = np.linalg.norm(slr.get_positions() - sl0.get_positions(), axis=1)
        extra = np.linalg.norm(sl_c.get_positions() - slr.get_positions(), axis=1)
        print(f"   맨 슬랩이 UMA 로 이미 움직인 양   최대 {base.max():.3f} Å  ← 분자와 무관")
        print(f"   분자가 **추가로** 끌어당긴 양      최대 {extra.max():.3f} Å  ← 이게 흡착의 몫")
        if extra.max() < 0.05:
            print("   ⛔ **분자가 표면을 거의 안 움직였다.** 그런데 E_bind 가 깊어졌다면 그 차이는")
            print("      흡착이 아니라 **기준(맨 슬랩) 이완 처리**에서 왔다 — 정의를 다시 봐야 한다.")
        elif extra.max() < 0.2:
            print("   → 약한 유도 이완. 강한 물리흡착~약한 화학흡착 경계.")
        else:
            print("   ✅ 분자가 표면을 유의하게 끌어당겼다 — 화학흡착과 정합.")
    else:
        print("   ⚠ --slab-relaxed 를 주면 'UMA 가 원래 움직인 양' 과 '분자가 추가로 끌어당긴 양' 을")
        print("      가를 수 있다. 그게 없으면 위 최대값에 **둘이 섞여 있다**.")

    # ── ③b ★ 누가 움직였나 — 평균은 작은데 최대가 크면 **몇 개만** 크게 움직인 것이다 ──
    #   그건 균일한 표면 이완이 아니라 **원자 이탈**(예: Li 가 뽑혀 분자로 감)의 신호다.
    #   그러면 E_bind 는 흡착에너지가 아니라 **추출/반응 에너지**이므로 이름을 바꿔야 한다.
    ssl = sl_c.get_chemical_symbols()
    top = np.argsort(dv_orig)[::-1][:6]
    dm_atom = d.min(axis=1)                      # 각 슬랩 원자의 분자까지 최단거리
    print(f"   ③b 가장 많이 움직인 슬랩 원자 (평균 {dv_orig.mean():.3f} vs 최대 "
          f"{dv_orig.max():.3f} — 격차가 크면 이탈 의심)")
    ejected = []
    for i in top:
        near_mol = dm_atom[i]
        tag = ""
        if dv_orig[i] > 0.5 and near_mol < 2.4:
            tag = "  ⛔ **분자 쪽으로 이탈**"
            ejected.append((ssl[i], dv_orig[i], near_mol))
        elif dv_orig[i] > 0.5:
            tag = "  ⚠ 크게 움직임(분자와는 멂)"
        print(f"      {ssl[i]:2s}[{i}]  이동 {dv_orig[i]:.3f} Å · 분자까지 {near_mol:.2f} Å{tag}")
    if ejected:
        sp = ", ".join(f"{s}({dd:.2f} Å 이동, 분자와 {nn:.2f} Å)" for s, dd, nn in ejected)
        print(f"   ⛔ **{len(ejected)}개 원자가 표면에서 분자로 끌려 나왔다**: {sp}")
        print("      → 이건 '흡착' 이 아니라 **추출/배위 반응**이다. E_bind 를 흡착에너지로 부르지 말 것.")
        print("      → 물리적으로는 더 중요한 현상일 수 있으나(예: Li+ 추출), 그렇다면")
        print("         참여 이온의 산화상태·전하 이동을 봐야 하고 **UMA 로는 판정 못 한다**(DFT+U 필요).")
    else:
        print("   ✅ 크게 이탈한 원자 없음 — 균일한 표면 이완으로 읽힌다.")

    print("\n④ 반드시 로그에서 확인할 것")
    print("   grep -n 'E_slab' ~/logs/phaseA_freeslab.log   → 'FIRE converged=True' 여야 한다.")
    print("   False 면 기준 에너지가 임의값이고 E_bind 는 통째로 무효다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
