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
  ② **전하**: 중성 Li 를 빼면 넓은 갭 절연체의 원자가띠에 정공이 생긴다(V_Li⁰).
    ★★ 2026-08-11 정정 — 그 정공을 없애려면 전자를 **더해야** 한다: `tot_charge = -1` (V_Li⁻).
    옛 코드는 `+1`(전자를 하나 더 뺌)이라 정공이 **2개**가 됐다 — 의도와 전자 2개 차이.
    QE 규약: +1 = 전자 부족, −1 = 전자 추가. (Codex 착수전 검토 P0-1, 전자 수 검산으로 확인)
    ⚠ 기존 li2s 0.272 eV 는 옛 규약 산물이라 **provisional** 이다. q=0/−1 파일럿 후 재판정.
    ⚠ jellium 은 유한 셀 보정이 근사다 — 셀을 충분히 키워 공공-공공 상호작용을 줄인다.

  python3 tools/sei/build_neb_inputs.py --plan          # 비용만 먼저 본다 (실행 안 함)
  python3 tools/sei/build_neb_inputs.py
  python3 tools/sei/build_neb_inputs.py --min_l 12 --images 9
"""
import argparse
import glob
import json
import os
import re
import sys
from pathlib import Path      # ⚠ 2026-08-20 — uma_scout 저장부가 이걸 쓰는데 빠져 있었다.
#   li2o 두 셀을 다 돌고 **결과를 쓰는 줄에서** NameError 로 죽어 li3p/li3po4g/licl 이
#   아예 안 돌았다. 저장은 계마다 하므로(루프 안), 이 한 줄이면 부분 결과가 살아남는다.

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import electronic_class as EC          # noqa: E402  (금속/절연체 단일 출처)

WORK = os.environ.get("WORK", "/data/work/runs/sei_neb")
# 갭 계산과 **같은 사양**을 쓴다 — 다른 축과 섞어 쓸 수 있어야 한다
ECUTWFC, ECUTRHO = 60.0, 480.0
TARGETS = {                       # tag → (구조 파일, 표시명)
    "li2s":    ("db/structures/sei_li2s_mp-1153.vasp", "Li2S"),
    "li3p":    ("db/structures/sei_li3p_mp-736.vasp", "Li3P"),
    "li3po4g": ("db/structures/sei_li3po4g_mp-2878.vasp", "Li3PO4-gamma"),
    # 2026-08-11 협업자 요청 확장 — 확산장벽 6종 채우기 (li2s 는 이미 citable)
    "li2o":    ("db/structures/sei_li2o_mp-1960.vasp", "Li2O"),
    "licl":    ("db/structures/sei_licl_mp-22905.vasp", "LiCl"),
    # lindo2 는 Nd PP 가 frozen-4f 일 때만 열린다 (아래 게이트, todo #27)
    "lindo2":  ("db/structures/sei_lindo2_mp-1222355.vasp", "LiNdO2"),
    # 2026-08-11 — Xu 2026 의 "Li–Nd alloy 계면상" 주장을 우리가 직접 잰다.
    # ⚠ **금속**이라 전하 규약이 다르다 (아래 electronic_class 분기). 같은 Nd PP 게이트를 탄다.
    "li3nd":   ("db/structures/sei_li3nd_mp-976264.vasp", "Li3Nd"),
    # 2026-09-01 (1저자 요청) — **순수 Li 금속**의 공공 이동. 음극 본체의 기준선이다.
    #   ⚠ 금속이므로 **중성 공공 + 금속 smearing** 이고 jellium 을 쓰지 않는다
    #     → 하전 결함의 1/L 이미지 항이 없어 유한크기에 훨씬 둔감하다.
    #   ⚠ 게이트 통과 최소단위는 **관용셀 3×3×3 (54원자 · λ₁ 10.53 Å)** 이다
    #     (primitive 3×3×3 은 9.12 Å 로 탈락 — 같은 "3×3×3" 이라도 기저가 다르면 갈린다).
    "li_metal": ("db/structures/sei_li_metal_bcc.vasp", "Li metal (bcc)"),
}
DFT_WORK = "/data/work/runs/sei_dft"      # run_sei_dft.sh 의 vc-relax 산출물 (이완본 출처)
#: ⚠ Nd 계는 **frozen-4f PP** 로 따로 돌아서 이완본이 다른 뿌리에 있다
#: (2026-08-19 실측: li3nd 를 sei_dft 에서 찾다 "이완본 없음" — 실제로는 여기 있다).
DFT_WORK_ALT = "/data/work/runs/sei_dft_frozen4f"


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


#: ⛔⛔ 2026-08-11 — **원소별 PP 를 이름으로 못 박는다.**
#:   옛 코드는 `sorted(...)` + `setdefault` 라 **알파벳 첫 번째**를 조용히 골랐다.
#:   실측: `Nd.paw.z_14.atompaw...` < `Nd.pbe-spdn-kjpaw_psl.1.0.0.UPF` 이므로
#:   frozen-4f(z=11) 를 pseudo 디렉터리에 **넣기만 하면 옛 z=14 가 그대로 이긴다.**
#:   그러면 "frozen-4f 로 돌렸다" 고 믿으면서 4f-in-valence 결과를 얻는다 — 조용히 틀린다.
#:   ⚠ 여기에 넣은 이름은 **정확히 그 파일만** 쓴다. 없으면 그 원소는 skip 된다.
PP_PIN = {
    # Nd frozen-4f (z_valence 11 · 4f in core) — QE PSLibrary
    #   출처: pseudopotentials.quantum-espresso.org/legacy_tables/ps-library/nd
    #   sha256 18a3835e6437aa953c8a5b783aae1f5b8c83e48f0fa699f8992f6754bdc35101
    #   suggested cutoff 38 / 202 Ry  ⚠ 우리 표준 60/480 은 그 위라 안전
    #   ⚠ Topsakal–Wentzcovitch z=14 계열과 **다른 PP** 다 — LiNdO₂·Li₃Nd 각각 검증 필요
    "Nd": "Nd.pbe-spdn-kjpaw_psl.1.0.0.UPF",
}


def find_pseudos(pdir):
    pool = {}
    if not os.path.isdir(pdir):
        return pool
    files = sorted(os.listdir(pdir))
    for f in files:
        if not f.lower().endswith(".upf"):
            continue
        el = f.split(".")[0].split("_")[0].capitalize()
        pool.setdefault(el, f)
    # ★ 핀이 있으면 알파벳 선택을 **덮어쓴다** (없으면 그 원소를 아예 뺀다 — 조용히
    #   옛 PP 로 돌기보다 안 도는 게 낫다)
    for el, want in PP_PIN.items():
        if el not in pool:
            continue
        if want in files:
            if pool[el] != want:
                print(f"   ★ {el} PP 를 핀으로 교체: {pool[el]} → {want}")
            pool[el] = want
        else:
            print(f"   ⛔ {el} 은 핀({want})이 pseudo 디렉터리에 없다 — "
                  f"이 원소를 빼고 진행한다 (옛 {pool[el]} 로 조용히 돌지 않는다)")
            pool.pop(el)
    return pool


def kmesh(cell, dens=0.03):
    """역격자 밀도 기준 k 메쉬. ⚠ round 가 아니라 ceil — 0 이나 1 로 무너지면 안 된다."""
    rec = np.linalg.norm(np.linalg.inv(cell).T, axis=1)
    return [max(1, int(np.ceil(r / dens))) for r in rec]


def li_orbits(at0):
    """원본(슈퍼셀 아님) 셀에서 Li 가 **몇 종류 자리**에 있는지.

    ★ 이게 왜 필요한가 (2026-08-07): 공공 매개 홉의 정·역 장벽이 같아야 하는 건
      **끝점 두 자리가 대칭적으로 같을 때뿐**이다. 실측:
        Li₂S     Fm-3m    Li 궤도 1개 (Wyckoff c)        → 대칭 · 정=역 이어야 한다
        Li₃P     P6₃/mmc  Li 궤도 2개 (b, f)             → **비대칭이 정상**
        Li₃PO₄γ  Pnma     Li 궤도 2개 (d, c)             → **비대칭이 정상**
      이걸 모르고 "정·역 차 < 0.02 eV" 를 일괄로 걸면 멀쩡한 Li₃P·Li₃PO₄ 결과를
      의심스럽다고 잘못 판정한다. 그래서 궤도 수를 입력 단계에서 기록해 둔다.
    """
    try:
        import spglib
    except ImportError:
        return None
    try:
        cell = (at0.cell.array, at0.get_scaled_positions(), at0.get_atomic_numbers())
        d = spglib.get_symmetry_dataset(cell, symprec=1e-3)
        eq = d.equivalent_atoms if hasattr(d, "equivalent_atoms") else d["equivalent_atoms"]
        wy = d.wyckoffs if hasattr(d, "wyckoffs") else d["wyckoffs"]
        sg = d.international if hasattr(d, "international") else d["international"]
        li = [i for i, z in enumerate(at0.get_atomic_numbers()) if z == 3]
        orb = sorted({(int(eq[i]), wy[i]) for i in li})
        return {"spacegroup": str(sg), "n_li_orbits": len(orb),
                "wyckoffs": [w for _, w in orb]}
    except Exception:
        return None


def orbit_map(at0):
    """원본 셀의 원자 index → (orbit id, Wyckoff). spglib 없으면 None."""
    try:
        import spglib
        cell = (at0.cell.array, at0.get_scaled_positions(), at0.get_atomic_numbers())
        d = spglib.get_symmetry_dataset(cell, symprec=1e-3)
        eq = d.equivalent_atoms if hasattr(d, "equivalent_atoms") else d["equivalent_atoms"]
        wy = d.wyckoffs if hasattr(d, "wyckoffs") else d["wyckoffs"]
        return {i: (int(eq[i]), wy[i]) for i in range(len(at0))}
    except Exception:
        return None


def pick_hop(at, nat0=None, omap=None, want_shell=None):
    """공공 자리 A 와 그리로 뛸 Li B 를 고른다.

    최근접 Li–Li 쌍을 쓴다 = **기본 홉**. 더 긴 경로는 이것들의 조합이므로 먼저 이걸 잰다.
    ⚠ 끝점은 감싼 좌표가 아니라 `pos[B] + 최소이미지 벡터` 로 만든다(위 함정 ①).

    ★ 2026-08-11 (Codex 검토 P0-4) — **선택한 쌍의 등가성**을 기록한다.
      구조 전체에 Li orbit 이 2종이라는 사실은 "선택된 A/B 가 비등가"라는 뜻이 **아니다**.
      Li₃P 의 최단 2.512 Å 쌍은 실제로 f–f **동등자리**이고 b–f 는 2.741 Å 다.
      옛 코드는 전역 orbit 수만 보고 비등가로 판정해 `site_energy_diff==0` 차단을
      false positive 로 걸었다. 이제 쌍 자체의 orbit 을 본다.
      (ASE repeat 는 블록 타일링이라 supercell index % nat0 = 원본 index.)

    ★★ 2026-08-12 — **전역 최단이 전도 경로가 아닐 수 있다.** li3nd 실측:
      b–c 3.176 Å(최단) 을 골랐는데 그 홉은 공공을 c(안정)에서 b(불안정, +2.05 eV)로
      밀어낸다. 즉 애초에 갈 일이 없는 경로를 잰 것이다. 실제 전도는 공공이 c 부격자에
      머무는 c–c 3.667 Å 이다. `want_shell="c-c"` 로 shell 을 지정할 수 있다.
      (kb/results/li3nd_endpoint_asymmetry_2026_08_12.md)
    """
    sym = at.get_chemical_symbols()
    li = [i for i, s in enumerate(sym) if s == "Li"]
    if len(li) < 2:
        return None
    D = at.get_all_distances(mic=True)
    def shell_of(i, j):
        if not (omap and nat0):
            return None
        oi, oj = omap.get(i % nat0), omap.get(j % nat0)
        if oi is None or oj is None:
            return None
        return "-".join(sorted((oi[1], oj[1])))

    best = None
    for n, i in enumerate(li):
        for j in li[n + 1:]:
            if want_shell and shell_of(i, j) != want_shell:
                continue
            d = D[i][j]
            if best is None or d < best[0]:
                best = (d, i, j)
    if best is None:
        raise SystemExit(f"⛔ shell '{want_shell}' 인 Li–Li 쌍이 없다 — "
                         f"neighbor_shells 를 먼저 볼 것 (--hop_shell 없이 한 번 돌리면 "
                         f"meta.json 에 목록이 남는다). 추정해서 다른 쌍을 쓰지 않는다")
    d, A, B = best
    vec = at.get_distance(B, A, mic=True, vector=True)
    out = {"d": float(d), "vac": A, "hop": B, "vec": np.asarray(vec, float),
           "pair_orbits": None, "pair_equivalent": None,
           "requested_shell": want_shell, "shell": shell_of(A, B)}
    if omap and nat0:
        oa, ob = omap.get(A % nat0), omap.get(B % nat0)
        out["pair_orbits"] = {"vac": list(oa) if oa else None,
                              "hop": list(ob) if ob else None}
        out["pair_equivalent"] = (oa is not None and ob is not None and oa[0] == ob[0])
    # 같은 shell 의 다른 대칭구별 쌍이 있는지 — "전역 최단"이 대표가 아닐 수 있다는 경고용
    if omap and nat0:
        shells = {}
        for n, i in enumerate(li):
            for j in li[n + 1:]:
                oi, oj = omap.get(i % nat0), omap.get(j % nat0)
                if oi is None or oj is None:
                    continue
                k = tuple(sorted((oi[1], oj[1])))
                shells.setdefault(k, []).append(round(float(D[i][j]), 4))
        out["neighbor_shells"] = {f"{a}-{b}": {"d_min": min(v), "n": len(v)}
                                  for (a, b), v in sorted(shells.items(), key=lambda t: min(t[1]))
                                  if min(v) < min(D[i][j] for n, i in enumerate(li)
                                                  for j in li[n + 1:]) * 1.35}
    return out


def load_relaxed(tag, path, relaxed_from):
    """vc-relax 이완본에서 벌크를 읽는다. 없으면 (None, 이유).

    ★ 2026-08-11 — li3p Ea=0 사고의 절반이 여기다: 비이완 MP 구조로 끝점을 만들면
      끝점이 경로에서 가장 높은 점이 되고, NEB 은 끝점을 고정하므로 내리막만 남아
      max(E)−E_first = 0 이 나온다. NEB 은 **이완본에서 출발해야** 한다.
    """
    import re
    from ase import Atoms
    cands = sorted(glob.glob(os.path.join(relaxed_from, f"{tag}_mp-*"))) \
        or ([os.path.join(relaxed_from, tag)] if os.path.isdir(os.path.join(relaxed_from, tag)) else [])
    if not cands:
        return None, f"{relaxed_from}/{tag}_mp-* 없음"
    outp = os.path.join(cands[0], "01_vcrelax.out")
    if not os.path.isfile(outp):
        return None, f"{outp} 없음"
    txt = open(outp, errors="ignore").read()
    if "JOB DONE" not in txt:
        return None, f"{outp} 미완료 (JOB DONE 없음)"
    i = txt.rfind("Begin final coordinates")
    if i < 0:
        return None, f"{outp} 에 final coordinates 블록 없음"
    blk = txt[i:txt.find("End final coordinates", i)]
    mc = re.search(r"CELL_PARAMETERS\s*\(?(\w+)[^\n]*\n((?:\s*[-\d.eE+]+\s+[-\d.eE+]+\s+[-\d.eE+]+\n){3})", blk)
    ma = re.search(r"ATOMIC_POSITIONS\s*\(?(\w+)", blk)
    if not mc or not ma:
        return None, f"{outp} final 블록 파싱 실패"
    cunit = mc.group(1).lower()
    cell = np.array([[float(x) for x in l.split()] for l in mc.group(2).strip().splitlines()])
    if cunit == "bohr":
        cell *= 0.529177210903
    elif cunit not in ("angstrom",):
        return None, f"CELL_PARAMETERS 단위 미지원: {cunit} (alat 는 splice 불가)"
    punit = ma.group(1).lower()
    rows = []
    for l in blk[ma.end():].splitlines():
        p = l.split()
        if len(p) >= 4 and re.match(r"^[A-Z][a-z]?$", p[0]):
            rows.append((p[0], [float(p[1]), float(p[2]), float(p[3])]))
    if not rows:
        return None, f"{outp} 좌표 없음"
    pos = np.array([r[1] for r in rows])
    if punit == "crystal":
        pos = pos @ cell
    elif punit == "bohr":
        pos = pos * 0.529177210903
    elif punit != "angstrom":
        return None, f"ATOMIC_POSITIONS 단위 미지원: {punit}"
    at = Atoms(symbols=[r[0] for r in rows], positions=pos, cell=cell, pbc=True)
    # 검증된 승계(verified-carry): 원본과 조성이 같아야 한다 — 다르면 파싱이 틀린 것
    from ase.io import read as _read
    ref = _read(path)
    if sorted(at.get_chemical_symbols()) != sorted(ref.get_chemical_symbols()):
        return None, f"{outp} 조성 불일치 — 파싱 오류로 간주"
    return at, outp


def shortest_translation(cell, R=3, _grow=True):
    """최단 비영 격자 병진 λ₁ = min |n₁a+n₂b+n₃c| [Å].

    ⛔⛔ 2026-08-16 (Codex 리뷰 P0) — **점결함의 최근접 주기 이미지는 여기 있다.**
    앞선 판은 면 높이 V/|a_j×a_k| 를 "실제 이미지 거리" 라고 썼는데 그건 격자 **평면**
    사이 거리라 슬랩 분리에나 맞는 양이고, 점-이미지 거리가 아니며 basis 의존이다.
    실측 차이가 1.22배라 판정이 뒤집혔다:

      Li₃Nd 2×2×2  면높이 8.469 → **λ₁ 10.372**   (10 Å 기준 통과)
      Li₂S  3×3×3  면높이 9.880 → **λ₁ 12.100**   (통과)
      lpsocl 1×1×1 면높이 5.672 → **λ₁  6.940**

    즉 "기존 셀이 10 Å 에 미달한다" 는 서술은 틀렸다. 면 높이는 **보수적 하한**으로만 쓴다.

    ⛔⛔ 2026-08-20 (Codex 2차) — **고정 R 은 기운 셀에서 틀린다.** 반례:
        a=(10,0,0) · b=(2.49,0.1,0) · c=(0,0,10)
        R=3 탐색 → 2.492 Å      실제 λ₁ = **0.402 Å** at n=(−1,4,0)

    ⛔⛔ 2026-08-20 (Codex 3차) — **R 을 키우는 수렴 탐색도 부적격이다.** 두 R 에서 값이
    같다고 수렴한 게 아니다 (연속 두 반경이 **둘 다** 최단벡터를 놓치면 조용히 종료한다).
    실측 반례:
        a=(10,0,0) · b=(0.5,0.001,0) · c=(0,0,10)
        R=3 = R=6 = 0.500001 로 **조기 종료**   실제 λ₁ = **0.020 Å** at n=(−1,20,0)
    같은 이유로 `|nᵢ| ≤ k` 유한 상자 전수검사도 **certificate 가 아니다** — 상자 밖을
    배제하지 못한다.

    ⇒ **exact 로 간다.** 3차원 격자의 SVP 는 Minkowski 축약으로 정확히 풀린다:
      기약기저의 첫 벡터가 정의상 최단 비영 벡터다 (Nguyen–Stehlé 2004, dim ≤ 4 에서
      greedy 가 Minkowski-reduced 를 다항시간에 준다). 우리는 그 알고리즘을 **다시 쓰지
      않고** ASE 정본 `ase.geometry.minkowski_reduce` 를 얇게 감싼다 — canonical 구현을
      복제하지 않는다는 같은 규율이 외부 라이브러리에도 적용된다.

    반환: λ₁ [Å] (full precision — 문턱 비교 전에 반올림하지 말 것).
    정수 계수 n 과 unimodular 변환이 필요하면 `shortest_translation_full()` 을 쓴다.

    ⚠ 이 함수가 **못 하는 것**: (1) 4차원 이상 — 3×3 셀 전용이다. (2) 특이/준특이 셀 —
      부피비가 EPS 미만이면 계산하지 않고 예외를 던진다(hard fail, 경고 후 계속 아님).
      (3) 물리적 타당성 판단 — λ₁ 이 작다는 사실만 알려주지 그 셀을 써도 되는지는 말 안 한다.
      (4) ASE 없이 동작 — import 실패는 fallback 재구현이 아니라 즉사다 (2026-08-19 F6 교훈).
    """
    return shortest_translation_full(cell)[0]


#: 준특이 셀 판정 문턱 — |det| / (|a||b||c|). 정육면체 1.0, 완전 평평 0.0.
LAMBDA1_DEGENERACY_EPS = 1e-8


def shortest_translation_full(cell):
    """(λ₁, n, reduced_cell) — exact. n 은 원래 기저에 대한 정수 계수.

    ⛔ 못 하는 것: `shortest_translation` 의 docstring 참조 (같은 한계).
    """
    import numpy as _np
    C = _np.asarray(cell, float)
    if C.shape != (3, 3):
        raise ValueError(f"3x3 셀만 받는다 (받은 것: {C.shape})")

    norms = _np.linalg.norm(C, axis=1)
    if not _np.all(_np.isfinite(C)) or float(_np.min(norms)) <= 0.0:
        raise ValueError(f"⛔ 셀에 비유한/영 벡터가 있다:\n{C}")
    ratio = abs(float(_np.linalg.det(C))) / float(_np.prod(norms))
    if ratio < LAMBDA1_DEGENERACY_EPS:
        raise ValueError(
            f"⛔ 준특이 셀이다 — |det|/(|a||b||c|) = {ratio:.3e} < {LAMBDA1_DEGENERACY_EPS:.0e}.\n"
            f"   이런 셀에서 λ₁ 은 부동소수로 신뢰할 수 없다. 경고 후 계속하지 않는다.\n{C}")

    try:
        from ase.geometry import minkowski_reduce, is_minkowski_reduced
    except Exception as exc:                       # noqa: BLE001 — 진단을 통째로 보여준다
        raise RuntimeError(
            "⛔ ase.geometry.minkowski_reduce 를 못 불렀다 — λ₁ 은 정본 구현으로만 잰다.\n"
            "   여기서 축약을 재구현하지 않는다 (fallback 금지, 2026-08-19 F6).\n"
            f"   원인: {exc!r}") from exc

    rcell, op = minkowski_reduce(C)                # rcell = op @ C, op 는 unimodular
    if not is_minkowski_reduced(rcell):
        raise RuntimeError(f"⛔ minkowski_reduce 결과가 기약이 아니라고 ASE 가 답한다:\n{rcell}")
    # ⛔ 2026-08-20 (codex 동결감사) — 옛 검사는 `abs(round(det)) == 1` 이었다. round 를
    #   **먼저** 하면 정수성 검사가 사라져 det=1.4 도 det=0.6 도 통과한다(실측).
    #   unimodular 는 두 조건이다: (a) 성분이 정수 (b) |det| = 1. 따로 본다.
    op_arr = _np.asarray(op, float)
    if not _np.allclose(op_arr, _np.round(op_arr), atol=1e-9):
        raise RuntimeError(f"⛔ 변환 행렬이 정수가 아니다:\n{op_arr}")
    det_op = float(_np.linalg.det(op_arr))
    if abs(abs(det_op) - 1.0) > 1e-9:
        raise RuntimeError(f"⛔ 변환이 unimodular 가 아니다 (|det| = {abs(det_op)} ≠ 1)")
    # 계약 검증: rcell = op @ cell (ASE 문서). 어긋나면 매핑 해석이 틀린 것이다.
    if not _np.allclose(op_arr @ C, rcell, rtol=1e-8, atol=1e-8):
        raise RuntimeError("⛔ rcell = op @ cell 계약이 깨졌다 — ASE 판이 바뀌었을 수 있다")

    order = _np.argsort(_np.linalg.norm(rcell, axis=1))
    i = int(order[0])
    return float(_np.linalg.norm(rcell[i])), tuple(int(v) for v in op[i]), rcell


def cell_metrics(cell):
    """(λ₁, 면높이 3개). λ₁ 이 점결함 기준, 면높이는 보수적 하한."""
    import numpy as _np
    C = _np.asarray(cell, float)
    V = abs(float(_np.linalg.det(C)))
    faces = [V / float(_np.linalg.norm(_np.cross(C[(i+1) % 3], C[(i+2) % 3]))) for i in range(3)]
    return shortest_translation(C), faces


#: λ₁ 구현의 정체성. ASE Minkowski 축약 래퍼 (2026-08-20). 알고리즘이 바뀌면 이 ID 를
#: 바꾼다 — ASE **판**이 바뀌는 것은 아래 `ase_version` 이 따로 잡는다.
LAMBDA1_METHOD_ID = "M-2026-08-20-lambda1-exact-3d-ase-minkowski"

#: 지문 스키마 판. 올리면 **기존 런의 이월이 전부 한 번 끊긴다** — 의도된 동작이다
#: (hash-bound carry 의 취지). 옛 해시와 새 해시를 구분해 진단에 쓴다.
PROTOCOL_HASH_SCHEMA = 2


def protocol_payload(tag, a, q, kpts, nat, cell, smear=None, degauss=None,
                     ecls=None, pps=None, hop=None, endpoints=None) -> dict:
    """지문의 **원재료**. 해시가 안 맞을 때 무엇이 바뀌었는지 보여주려면 필요하다.

    ⛔ 2026-08-20 (codex 동결감사) — 이전에는 payload 가 protocol_hash 안의 지역변수라
      불일치 진단이 "5f78… → a3c2…" 밖에 못 냈다. 무엇이 바뀌었는지 말하려면 두 payload
      를 비교해야 하므로 밖으로 뺀다.
    """
    return _protocol_payload(tag, a, q, kpts, nat, cell, smear, degauss, ecls, pps, hop, endpoints)


def protocol_diff(p_old: dict, p_new: dict) -> list:
    """두 payload 에서 달라진 키. 이월 거부 사유를 사람 말로 만들 때 쓴다."""
    out = []
    for k in sorted(set(p_old) | set(p_new)):
        a_, b_ = p_old.get(k, "<없음>"), p_new.get(k, "<없음>")
        if a_ != b_:
            out.append(f"{k}: {a_!r} → {b_!r}")
    return out


def _protocol_payload(tag, a, q, kpts, nat, cell, smear=None, degauss=None,
                      ecls=None, pps=None, hop=None, endpoints=None) -> dict:
    """지문 원재료 — 프로토콜이 바뀌면 옛 neb.out/tmp/prefix.path 를 재사용하면 안 된다.

    ★ 2026-08-11 (Codex 검토 P0-3) — 같은 WORK 에 새 입력을 쓰면 runner 가 옛 neb.out 의
      'convergence achieved' 만 보고 건너뛴다. 그러면 **새 meta.json 과 옛 에너지가 결합**된다.
      기존 li2s 는 min_cell 8.02 인데 새 기본은 --min_l 10 이라 실제로 일어날 수 있었다.
    """
    # ★ 2026-08-11 자체검토 P0-5 / P1-1 — 두 가지를 고쳤다.
    #  P0-5: `ci` 를 지문에서 **뺀다**. 문서화된 2단계(no-CI 수렴 → restart+CI)가
    #        지문을 바꿔 러너에게 거부당했고, 러너 안내대로 prefix.path 를 지우면
    #        restart 자체가 깨진다. CI 단계는 물리(계·전하·격자)가 아니라 **수렴 전략**이다.
    #        → 별도로 `.ci_stage` 파일에 기록한다.
    #  P1-1: smearing/degauss/electronic_class/PP 파일명이 빠져 있었다. 실측 충돌:
    #        `--vacancy_charge neutral` 이면 insulator(q=0,gaussian 0.005)와
    #        metal(q=0,mv 0.02)의 지문이 **동일**했다. PP 를 frozen-4f 로 갈아끼워도
    #        지문이 그대로였다(todo #27 이 오면 바로 물릴 함정).
    payload = {"tag": tag, "ecutwfc": ECUTWFC, "ecutrho": ECUTRHO, "q": q,
               "images": a.images, "path_thr": a.path_thr, "kpts": list(kpts),
               "nat": nat, "min_l": a.min_l, "min_l_basis": a.min_l_basis,
               # ⛔ 2026-08-16 (Codex P0) — perp 는 build() 지역변수였다. 여기서 참조해
               #   **NameError 로 죽었고**, 그 시점엔 이미 새 neb.in 을 쓴 뒤라
               #   새 입력 + 옛 meta 조합이 남을 수 있었다. 셀 지표는 인자로 받은
               #   cell 에서 직접 계산한다.
               "lambda1_A": round(shortest_translation(cell), 3),
               "face_heights_A": [round(x, 3) for x in cell_metrics(cell)[1]],
               # ⛔ 2026-08-16 (Codex P0) — 홉 정체성이 지문에 없었다. 실측: Li₃Nd 의
               #   b→c (2.07173 eV) 와 c→c (0.228981 eV) 가 **같은 해시 5f78cec0339e**
               #   였다. 작업 폴더가 달라 우연히 안 섞였을 뿐이다.
               "hop_shell": (hop or {}).get("shell"),
               "hop_pair_orbits": (hop or {}).get("pair_orbits"),
               "hop_vac_index": (hop or {}).get("vac"),
               "hop_moving_index": (hop or {}).get("hop"),
               "hop_distance_A": (round(float((hop or {}).get("d", 0)), 4) if hop else None),
               "endpoint_coords_sha": endpoints,
               "cell": [round(float(x), 6) for v in cell for x in v],
               "smearing": smear, "degauss": degauss,
               "electronic_class": (ecls or {}).get("class"),
               "pseudos": dict(sorted((pps or {}).items())),
               "endpoints_relaxed": not a.allow_unrelaxed_endpoints,
               # ⛔ 2026-08-20 (codex 동결감사) — λ₁ 은 이제 ASE Minkowski 축약이 낸다.
               #   구현 정체성(method_id)과 라이브러리 판(ase_version)이 지문에 없으면
               #   "같은 프로토콜" 이라는 주장이 검증 불가다. ASE 가 축약을 바꾸면 λ₁ 이
               #   달라질 수 있고 그건 다른 프로토콜이다.
               "hash_schema": PROTOCOL_HASH_SCHEMA,
               "lambda1_method_id": LAMBDA1_METHOD_ID,
               "ase_version": _ase_version()}
    return payload


def _ase_version() -> str:
    try:
        import ase
        return str(ase.__version__)
    except Exception as exc:                        # noqa: BLE001
        raise RuntimeError(f"⛔ ASE 판을 못 읽는다 — λ₁ 정본이 ASE 다: {exc!r}") from exc


def protocol_hash(tag, a, q, kpts, nat, cell, smear=None, degauss=None,
                  ecls=None, pps=None, hop=None, endpoints=None) -> str:
    """입력 규약 지문. 원재료는 protocol_payload() 참조."""
    import hashlib
    payload = _protocol_payload(tag, a, q, kpts, nat, cell, smear, degauss,
                                ecls, pps, hop, endpoints)
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:12]


def build(tag, path, disp, a, pool):
    from ase.io import read
    # ★★ 2026-08-11 — **금속/절연체 분기가 제일 먼저다.** 전하 규약·smearing·회수기
    #   차단이 전부 여기서 갈린다. 미등록 상은 추측하지 않고 막는다 (Li₃Nd 함정의 입구).
    ecls = EC.get(tag)
    why_blocked = EC.blocked_reason(tag)
    # ⚠ --plan(비용 산정)은 입력을 안 만드니 게이트를 걸지 않는다 — 막으면 li3nd 비용을
    #   재 볼 수조차 없다. 다만 사유는 찍어서 "계획엔 있지만 지금은 못 돈다" 를 보이게 한다.
    if why_blocked and not a.ignore_electronic_class and not a.plan:
        return {"tag": tag, "skip": f"electronic_class 게이트 — {why_blocked}"}
    is_metal = ecls.get("class") == "metal"
    # ── 이완본 출발 (기본). --allow_unrelaxed 는 계획/디버그 전용 탈출구다 ──────
    relaxed_out = None
    if a.allow_unrelaxed:
        at0 = read(path)
    else:
        at0, why = load_relaxed(tag, path, a.relaxed_from)
        if at0 is None:
            return {"tag": tag,
                    "skip": f"이완본 없음({why}) — run_sei_dft.sh 먼저. "
                            f"(비이완으로 강행하려면 --allow_unrelaxed · li3p Ea=0 사고 참조)"}
        relaxed_out = why                      # 성공 시 why 자리에 출처 경로가 온다
    # ⛔⛔ 2026-08-16 — 옛 판은 **격자벡터 길이**로 슈퍼셀을 골랐다. 그런데 공공-공공
    #   주기 상호작용을 정하는 건 벡터 길이가 아니라 **주기면 사이 수직 거리**
    #   d_i = V / |a_j × a_k| 다. 비직교 셀에서 둘은 크게 다르다:
    #     li3nd 2×2×2 : 벡터 10.37 Å → 실제 이미지 거리 **8.47 Å**  (min_l 10 을 통과했지만 미달)
    #     li2s  3×3×3 : 벡터 12.10 Å → 실제 **9.88 Å**              (역시 미달)
    #   같은 규칙을 통과한 두 상의 실제 이미지 거리가 1.17배 달랐다 — 규칙이 재려던 걸
    #   안 재고 있었다. 이제 수직 폭으로 고른다.
    #   ⚠ 그래서 같은 --min_l 값이라도 옛 판보다 큰 셀이 나온다 (의도된 변화).
    #   옛 동작이 필요하면 --min_l_basis vector.
    # ⛔⛔ 2026-08-16 (Codex 리뷰 P0) — 기준을 **λ₁(최단 격자 병진)** 으로 되돌린다.
    #   직전 판은 면 높이(perp)를 "실제 이미지 거리" 라며 기본으로 삼았는데, 그건
    #   격자 평면 사이 거리지 점-이미지 거리가 아니다. 실측 1.22배 차이로 판정이 뒤집혔다:
    #   Li₃Nd 2×2×2 는 면높이 8.47 로는 미달인데 λ₁ 10.37 로는 **통과**다.
    #   면 높이는 버리지 않고 보수적 하한으로 meta 에 같이 싣는다.
    L = at0.cell.lengths()
    if a.min_l_basis == "vector":
        base_rep = tuple(max(1, int(np.ceil(a.min_l / x))) for x in L)
    else:
        # λ₁ 은 배수의 단순 함수가 아니므로 **배수를 키워가며 실제로 만족하는 최소**를 찾는다
        base_rep = None
        for m in range(1, 9):
            C = np.asarray(at0.repeat((m, m, m)).cell.array, float)
            if shortest_translation(C) >= a.min_l:
                base_rep = (m, m, m)
                break
        if base_rep is None:
            return {"tag": tag, "skip": f"λ₁ ≥ {a.min_l} Å 를 8배 안에서 못 만든다"}
    rep = base_rep
    at = at0.repeat(rep)
    _lam1, perp = cell_metrics(at.cell.array)
    els = sorted(set(at.get_chemical_symbols()))
    miss = [e for e in els if e not in pool]
    if miss:
        return {"tag": tag, "skip": f"pseudo 없음: {','.join(miss)}"}

    # ⛔ Nd 는 frozen-4f PP 일 때만 연다 — 4f 를 원자가에 두면 SCF 가 안 붙고,
    #    붙어도 안장점을 믿을 수 없다 (todo #27 · Nd 판정).
    if "Nd" in els:
        zn = zval(os.path.join(a.pseudo_dir, pool["Nd"]))
        if zn is None or zn > 12:
            return {"tag": tag,
                    "skip": f"Nd PP 가 frozen-4f 가 아니다 (z_valence={zn}) — "
                            f"frozen-4f(z≈11) 확보 후 열 것 (todo #27)"}

    omap = orbit_map(at0)
    hop = pick_hop(at, nat0=len(at0), omap=omap,
                   want_shell=(a.hop_shell or {}).get(lab)
                   if isinstance(a.hop_shell, dict) else a.hop_shell)
    if hop is None:
        return {"tag": tag, "skip": "Li 가 2개 미만"}

    # ★★ 2026-08-11 부호 정정 (Codex 착수전 검토 P0-1) — 이전 규약이 **틀렸다**.
    #   QE 규약: tot_charge = +1 → 전자 1개 **부족**, −1 → 1개 **추가**.
    #   Li **원자**를 지우면 QE 가 z_valence(=3) 만큼 전자도 뺀다 → 셀은 중성이고,
    #   이온 관점으로는 Li⁺ 가 빠지며 전자 1개가 남아 **원자가띠에 정공 1개** = V_Li⁰.
    #   옛 코드는 이 정공을 없애려고 tot_charge=+1 로 전자를 **하나 더 뺐다** — 반대 방향이라
    #   정공이 2개가 됐다. 닫힌 껍질 V_Li⁻ 를 원하면 전자를 **더해야** 한다(tot_charge = −1).
    #   실측 검산(Li₂S 216전자 셀): 옛 212 vs 의도 214 → **전자 2개 차이**.
    #   ⚠ 그래서 기존 li2s 0.272 eV 는 정공 2개짜리 계산이다 — provisional 로 내린다.
    CHARGE = {"minus1": -1.0, "neutral": 0.0}      # V_Li⁻ (닫힌 껍질) / V_Li⁰ (정공 1개)
    q = CHARGE[a.vacancy_charge]
    # ★★ 금속 분기 (2026-08-11, Li₃Nd 착수) — 위 전하 논리는 **넓은 갭 절연체 전용**이다.
    #   근거였던 "중성 Li 를 빼면 원자가띠에 정공이 생겨 가짜 금속이 된다" 가 금속엔
    #   적용되지 않는다: 금속은 애초에 원자가띠 정공이라는 개념이 없고, 공공을 만들어도
    #   전도전자가 스스로 가려 준다. jellium 배경전하는 인위적 상수를 더할 뿐이다.
    #   → 금속: tot_charge = 0 · Marzari–Vanderbilt smearing · degauss 를 키운다.
    #   ⚠ 절연체에 mv 를 쓰면 안 된다(음의 점유수) — 그래서 분기이지 기본값 변경이 아니다.
    smear, degauss = "gaussian", 0.005
    if is_metal:
        if a.vacancy_charge != "neutral":
            print(f"   ⚠ {tag} 는 metal 이라 vacancy_charge 를 neutral(tot_charge=0) 로 "
                  f"강제한다 (요청값 {a.vacancy_charge} 무시 — 금속에 jellium 은 틀렸다)")
        q = 0.0
        smear, degauss = "mv", 0.02
    nelec_full = sum(zval(os.path.join(a.pseudo_dir, pool[s])) or 0
                     for s in at.get_chemical_symbols())
    z_li = zval(os.path.join(a.pseudo_dir, pool["Li"])) or 3.0
    nelec_vac = nelec_full - z_li - q      # q=−1 이면 +1 개(정공 0) · q=0 이면 그대로(정공 1)
    nat = len(at) - 1

    orb = li_orbits(at0)
    info = {"tag": tag, "disp": disp, "rep": rep, "nat": nat,
            "cell": at.cell.array.copy(), "els": els,
            "hop_d": hop["d"], "nelec": nelec_vac,
            # ⚠ 계획 화면이 쓰는 dict 는 **이것**이다 (meta.json 쪽이 아니다).
            #   여기 안 실으면 --plan 이 "미상" 으로 찍힌다 (2026-08-12 실측).
            "hop_shell": hop.get("shell"),
            "pair_equivalent": hop.get("pair_equivalent"),
            "L": at.cell.lengths().round(2).tolist(),
            "kpts": kmesh(at.cell.array, a.kdens),
            "li_orbits": orb,
            "geometry_source": ("UNRELAXED (--allow_unrelaxed)" if a.allow_unrelaxed
                                else relaxed_out)}
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

    # ★★ P0-2 (Codex) — vacancy **끝점 자체**를 먼저 이완해야 한다.
    #   지금까지는 완전 벌크만 이완하고, Li 를 뺀 두 끝점은 **미이완**으로 NEB 에 넣었다.
    #   미이완 끝점이 경로 최고점이 되면 NEB 은 끝점을 고정하므로 내리막만 남아 Ea=0 이 된다
    #   — 그게 li3p 사고의 미해결 절반이다. 같은 셀·같은 q·같은 k·같은 PP 로 고정셀 relax.
    ep_files, ep_ready = {}, True
    for name, imgs in (("ep_initial", first), ("ep_final", last)):
        epd = os.path.join(d, name)
        os.makedirs(epd, exist_ok=True)
        ep_files[name] = epd
        rel = ["&CONTROL", "    calculation     = 'relax'",
               f"    prefix          = '{tag}_{name}'", "    outdir          = './tmp'",
               f"    pseudo_dir      = '{a.pseudo_dir}'",
               "    tprnfor         = .true.", "    forc_conv_thr   = 1.0d-3", "/",
               "&SYSTEM", "    ibrav           = 0", f"    nat             = {nat}",
               f"    ntyp            = {len(els)}",
               f"    ecutwfc         = {ECUTWFC}", f"    ecutrho         = {ECUTRHO}",
               f"    tot_charge      = {q:.1f}",
               "    occupations     = 'smearing'", f"    smearing        = '{smear}'",
               f"    degauss         = {degauss}", "/",
               "&ELECTRONS", "    conv_thr        = 1.0d-8",
               "    mixing_beta     = 0.3", "    electron_maxstep = 200", "/",
               "&IONS", "    ion_dynamics    = 'bfgs'", "/", "", "ATOMIC_SPECIES"]
        for e in els:
            rel.append(f"  {e:3s} {atomic_masses[atomic_numbers[e]]:8.3f}  {pool[e]}")
        rel += ["", "ATOMIC_POSITIONS angstrom"]
        for e, pp in imgs:
            rel.append(f"  {e:3s} %16.10f %16.10f %16.10f" % tuple(pp))
        rel += ["", "K_POINTS automatic", "  %d %d %d 0 0 0" % tuple(info["kpts"]),
                "", "CELL_PARAMETERS angstrom"]
        for v in at.cell.array:
            rel.append("  %16.10f %16.10f %16.10f" % tuple(v))
        open(os.path.join(epd, "relax.in"), "w").write("\n".join(rel) + "\n")
        # 이미 이완된 게 있으면 그 좌표를 끝점으로 승계한다 (verified-carry)
        # ★ 끝점 이완 지문 (자체검토 P1-4) — relax.in 은 매 실행 덮어써지는데 relax.out 은
        #   그대로다. 원자 수만 같으면 **옛 설정(다른 q·k·PP)의 좌표가 조용히 승계**된다.
        #   그러면 끝점과 경로가 다른 조건이 되는데, 그게 이번 리뷰의 1번 걱정이었다.
        import hashlib as _hl
        ep_sig = _hl.sha256(json.dumps(
            {"q": q, "smear": smear, "degauss": degauss, "kpts": list(info["kpts"]),
             "nat": nat, "ecut": [ECUTWFC, ECUTRHO],
             "cell": [round(float(x), 6) for v in at.cell.array for x in v],
             "pps": {e: pool[e] for e in els}}, sort_keys=True).encode()).hexdigest()[:12]
        sigp = os.path.join(epd, ".ep_hash")
        # ⛔⛔ 2026-08-17 — 끝점 이완 **이어달리기**는 `ep_initial_r2/` 처럼 새 디렉터리에
        #   들어간다(미수렴 원본을 덮지 않으려고). 이 함수는 `ep_initial/relax.out` 만 봤고,
        #   그건 스텝을 소진한 1차 패스라 `Begin final coordinates` 가 없다 →
        #   **수렴본을 옆에 두고 "끝점 미이완" 으로 조기 반환**했다. cc333 이 정확히 그 상태.
        #   판정 규칙은 symmetric_saddle.endpoint_dir() 하나뿐이다 — 복사하지 말고 쓴다.
        from symmetric_saddle import endpoint_dir as _epdir   # noqa: E402
        srcd = _epdir(d, name)
        outp = os.path.join(srcd, "relax.out")
        if srcd != epd and os.path.isfile(outp):
            print(f"   ↳ {tag}/{name}: 이어달리기 수렴본을 승계한다 "
                  f"({os.path.basename(srcd)}/relax.out)")
        got = None
        old_sig = open(sigp).read().strip() if os.path.isfile(sigp) else ""
        if os.path.isfile(outp) and old_sig and old_sig != ep_sig:
            print(f"   ⚠ {tag}/{name}: 끝점 이완 설정이 바뀌었다 ({old_sig} → {ep_sig}) "
                  f"— 옛 relax.out 을 승계하지 않는다. 다시 이완할 것")
        elif os.path.isfile(outp):
            txt = open(outp, errors="ignore").read()
            if "JOB DONE" in txt and "Begin final coordinates" in txt:
                i2 = txt.rfind("Begin final coordinates")
                e2 = txt.find("End final coordinates", i2)
                blk = txt[i2:e2 if e2 > 0 else len(txt)]
                rows2 = []
                import re as _re
                mm = _re.search(r"ATOMIC_POSITIONS\s*\(?(\w+)", blk)
                if mm:
                    for l in blk[mm.end():].splitlines():
                        pr = l.split()
                        if len(pr) >= 4 and _re.match(r"^[A-Z][a-z]?\d*$", pr[0]):
                            rows2.append((pr[0], [float(pr[1]), float(pr[2]), float(pr[3])]))
                # ⚠ 개수만 맞추면 **다른 상의 relax.out** 이나 종별 재정렬본이 통과해
                #   좌표가 엉뚱한 원소에 붙는다. 심볼 열까지 대조한다 (P1-2).
                if len(rows2) == nat and mm.group(1).lower() == "angstrom" \
                        and [r[0] for r in rows2] == [e for e, _ in imgs]:
                    got = rows2
                elif rows2:
                    print(f"   ⚠ {tag}/{name}: relax.out 의 원자 목록이 입력과 다르다 "
                          f"— 승계하지 않는다 (다른 계의 산출물이 섞였는지 볼 것)")
        open(sigp, "w").write(ep_sig + "\n")
        if got is None:
            ep_ready = False
        else:
            if name == "ep_initial":
                first = got
            else:
                last = got
    info["endpoints_relaxed"] = ep_ready
    # ★ 자체검토 P1-3 — **이완 뒤에** 두 끝점이 아직 서로 다른 구조인지 본다.
    #   끝점 이완에서 뛰는 Li 가 공공으로 굴러떨어지면(무장벽) first ≈ last 가 되어
    #   Ea≈0 이 나온다 — collect_neb 가 사후에 잡는 그 붕괴를, 여기서 공짜로 잡는다.
    #   ⚠ 옛 코드의 arrival_err 는 **이완 전** 좌표로 계산돼 meta 에 실렸다(provenance 거짓).
    if ep_ready:
        dmax = max(float(np.linalg.norm(np.asarray(f[1], float) - np.asarray(l[1], float)))
                   for f, l in zip(first, last))
        info["endpoint_displacement_max_A"] = dmax
        if dmax < 0.5:
            info["skip"] = (f"이완된 두 끝점이 사실상 같은 구조다 (최대 변위 {dmax:.3f} Å < 0.5) "
                            f"— 뛰는 Li 가 이완 중 공공으로 굴러떨어졌을 수 있다. "
                            f"NEB 을 걸면 Ea≈0 이 나온다. 끝점 좌표를 직접 볼 것: "
                            f"{os.path.join(d, 'ep_initial')} · {os.path.join(d, 'ep_final')}")
            return info
        # 이완 후 좌표로 도달 검산을 다시 한다 (meta 에 실리는 값이 실제 끝점이어야 한다)
        info["arrival_err_pre_relax"] = info.get("arrival_err")
    else:
        info["endpoint_displacement_max_A"] = None
    if not ep_ready and not a.allow_unrelaxed_endpoints:
        info["skip"] = ("vacancy 끝점 미이완 — 먼저 `bash tools/sei/run_sei_neb.sh endpoints "
                        f"{tag}` 로 {tag}/ep_initial · ep_final 을 이완할 것. "
                        "(강행하려면 --allow_unrelaxed_endpoints · li3p Ea=0 사고 참조)")
        info["endpoint_inputs"] = ep_files
        return info

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
            f"  CI_scheme       = '{a.ci_scheme}'",
            # ⛔ 2026-08-27 (교차리뷰 I · P0-3) — 옛 조건은 `ci_scheme != "no-CI" and restart`
            #   였다. 즉 **중단된 no-CI 런을 이어달리려고 --restart 를 줘도 조용히
            #   from_scratch 로 써서** 체크포인트(prefix.path)를 두고 처음부터 돌았다.
            #   (--restart 를 "2단계 CI 전용" 으로만 본 설계였는데, 실제 용례는 둘이다:
            #    ① no-CI 중단 재개  ② no-CI 수렴본 위에 CI. 둘 다 restart_mode='restart' 다.)
            #   러너(run_sei_neb.sh)는 반대로 "*.path 가 있으면 이어진다" 고 안내하고 있었다.
            ("  restart_mode    = 'restart'" if a.restart
             else "  restart_mode    = 'from_scratch'"),
            f"  path_thr        = {a.path_thr}",
            "/", "END_PATH_INPUT", "BEGIN_ENGINE_INPUT",
            "&CONTROL", "    calculation     = 'scf'",
            f"    prefix          = '{tag}'", "    outdir          = './tmp'",
            f"    pseudo_dir      = '{a.pseudo_dir}'",
            "    tprnfor         = .true.", "/",
            "&SYSTEM", "    ibrav           = 0", f"    nat             = {nat}",
            f"    ntyp            = {len(els)}",
            f"    ecutwfc         = {ECUTWFC}", f"    ecutrho         = {ECUTRHO}",
            # ★ 전하 규약은 electronic_class 로 갈린다 (위 금속 분기 참조):
            #   절연체 → V_Li⁻ (tot_charge = −1) + jellium · gaussian smearing
            #   금속   → 중성 공공 (tot_charge = 0) · mv smearing (jellium 은 틀리다)
            f"    tot_charge      = {q:.1f}",
            "    occupations     = 'smearing'", f"    smearing        = '{smear}'",
            f"    degauss         = {degauss}", "/",
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
    # ⛔ 2026-08-27 (교차리뷰 I · P0-3) — restart 는 **체크포인트가 실재할 때만** 뜻이 있다.
    #   QE 는 prefix.path 없이 restart_mode='restart' 를 받으면 조용히 처음부터 도는데,
    #   그러면 우리는 "이어달린다" 고 믿으면서 몇 주를 다시 태운다. 여기서 먼저 막는다.
    if a.restart:
        _pf = os.path.join(d, f"{tag}.path")
        info["restart_checkpoint"] = _pf
        info["restart_checkpoint_exists"] = os.path.isfile(_pf)
        if not info["restart_checkpoint_exists"]:
            info["skip"] = (f"⛔ --restart 인데 체크포인트가 없다: {_pf}\n"
                            f"      restart_mode='restart' 는 이 파일이 있어야 이어달린다. "
                            f"처음부터 도는 것이 맞다면 --restart 를 빼라 "
                            f"(빼면 from_scratch 로 명시된다).")
            return info
    open(os.path.join(d, "neb.in"), "w").write("\n".join(body))
    # ★ 회수기가 대칭 게이트를 켤지 말지 여기서 판단한다 (위 li_orbits 주석 참조).
    #   지문 인자는 한 번만 만든다 — 해시와 payload 가 **같은 재료**여야 diff 가 의미 있다.
    _pargs = dict(
        tag=tag, a=a, q=q, kpts=info["kpts"], nat=nat, cell=at.cell.array,
        smear=smear, degauss=degauss, ecls=ecls,
        pps={e: pool[e] for e in els},
        # ⛔ 홉 정체성 — 이게 없어서 b→c 와 c→c 가 같은 해시를 가졌다
        hop={"shell": hop.get("shell"), "pair_orbits": hop.get("pair_orbits"),
             "vac": hop.get("vac"), "hop": hop.get("hop"), "d": hop.get("d")},
        # 끝점 좌표 자체도 지문에 넣는다 (같은 shell 이어도 다른 쌍일 수 있다)
        endpoints=_hl.sha256(
            json.dumps([[s, [round(x, 6) for x in p]] for s, p in first]
                       + [[s, [round(x, 6) for x in p]] for s, p in last],
                       sort_keys=True).encode()).hexdigest()[:16])
    _j = json
    _j.dump({"tag": tag, "disp": disp, "supercell": list(rep), "nat": nat,
             "hop_distance_A": hop["d"], "hop_shell": hop.get("shell"),
             "pair_equivalent": hop.get("pair_equivalent"),
             "hop_shell_requested": hop.get("requested_shell"), "nelec": nelec_vac,
             "protocol_hash": protocol_hash(**_pargs),
             # ⛔ 2026-08-20 (codex 동결감사) — 지문의 **원재료**도 남긴다. 해시만 있으면
             #   이월 거부 사유가 "5f78… → a3c2…" 로 끝나 무엇이 바뀌었는지 말할 수 없다.
             #   protocol_diff(old, new) 가 이 필드를 먹는다.
             "protocol_payload": protocol_payload(**_pargs),
             "lambda1_A": round(_lam1, 3),
             "face_heights_A": [round(x, 3) for x in perp],
             "min_face_height_A": round(min(perp), 3),
             "cell_metric_note": ("점결함 이미지 거리는 **λ₁(최단 격자 병진)** 이다. "
                                  "면 높이는 격자 평면 간 거리라 보수적 하한으로만 쓴다 "
                                  "(둘의 비가 fcc 에서 1.22배 — 2026-08-16 Codex 리뷰)."),
             "endpoints_relaxed": info.get("endpoints_relaxed"),
             "ci_scheme": a.ci_scheme,
             "tot_charge": q, "vacancy_charge": ("neutral" if is_metal else a.vacancy_charge),
             "electronic_class": ecls.get("class"),
             "electronic_class_evidence": ecls.get("evidence"),
             "smearing": smear, "degauss": degauss,
             "charge_convention": "QE: +1=전자 부족, -1=전자 추가. V_Li- 는 -1 이다. "
                                  "2026-08-11 이전 입력은 +1(정공 2개)이라 무효.",
             "num_of_images": a.images,
             "min_cell_A": min(info["L"]), "kpts": info["kpts"],
             "li_orbits": orb,
             # ★ 전역 orbit 수가 아니라 **선택된 쌍**의 등가성 (Codex P0-4)
             "endpoints_symmetry_equivalent": hop.get("pair_equivalent"),
             "global_n_li_orbits": (orb or {}).get("n_li_orbits"),
             "pair_orbits": hop.get("pair_orbits"),
             "neighbor_shells": hop.get("neighbor_shells"),
             "arrival_err_A": info["arrival_err"],
             "arrival_err_is_pre_relax": ep_ready,
             "endpoint_displacement_max_A": info.get("endpoint_displacement_max_A"),
             "geometry_source": info["geometry_source"],
             "_note": ("endpoints_symmetry_equivalent=false 면 정·역 장벽이 다른 게 정상이다 "
                       "— 그 차이는 두 Li 자리의 에너지 차다. 장거리 수송에 걸리는 유효 장벽은 "
                       "max(정, 역) 이다(가장 낮은 자리에서 안장점까지).")},
            open(os.path.join(d, "meta.json"), "w"), ensure_ascii=False, indent=2)

    # 사람이 눈으로 검산할 수 있게 두 끝 이미지를 구조 파일로도 남긴다
    from ase import Atoms
    from ase.io import write
    for name, imgs in (("initial", first), ("final", last)):
        write(os.path.join(d, f"{name}.xyz"),
              Atoms(symbols=[e for e, _ in imgs],
                    positions=[p for _, p in imgs], cell=at.cell, pbc=True))
    return info


# ── UMA 정찰 (2026-08-19) ────────────────────────────────────────────────────
def _atomic_rows(text, start=0, end=None):
    """ATOMIC_POSITIONS 블록 하나 → [(심볼, [x,y,z]), …]. 단위가 angstrom 이 아니면 None."""
    seg = text[start:end if end is not None else len(text)]
    m = re.search(r"ATOMIC_POSITIONS\s*\(?\s*(\w+)", seg)
    if not m or m.group(1).lower() != "angstrom":
        return None
    rows = []
    for ln in seg[m.end():].splitlines():
        pr = ln.split()
        if len(pr) >= 4 and re.match(r"^[A-Z][a-z]?\d*$", pr[0]):
            try:
                rows.append((pr[0], [float(pr[1]), float(pr[2]), float(pr[3])]))
            except ValueError:
                break
        elif rows:
            break                      # 블록이 끝났다 (다음 카드로 넘어감)
    return rows or None


def verify_endpoints(work, only=None, tol=1e-4):
    """이미 만들어진 neb.in 의 끝점이 **수렴한** relax.out 좌표와 같은지 대조한다.

    왜 필요하냐 — 끝점 이완 이어달리기는 `ep_initial_r2/` 처럼 옆 디렉터리에 들어간다.
    빌더가 그걸 승계하게 고쳐진 건 2026-08-17 인데, **그 전에 만들어진 neb.in** 은
    미수렴 원본 좌표를 물고 있다. 미이완 끝점 위에서 NEB 을 돌리면 기준선이 위로
    뜬 자로 높이를 재는 셈이라, 며칠을 태워 수렴해도 그 Ea 는 인용할 수 없다.
    파일 시각(neb.in 이 더 나중)은 **증거가 아니다** — 좌표를 직접 대조한다.

    ⛔ 이 함수가 못 하는 것: 중간 이미지의 타당성, k-mesh·컷오프·의사퍼텐셜 일치,
      relax.out 이 **그 계**의 것인지(심볼 목록까지만 본다). 끝점 두 개만 본다.
    """
    import glob as _g
    # 판정 규칙은 symmetric_saddle.endpoint_dir() 하나뿐이다 — 복사하지 말고 쓴다.
    from symmetric_saddle import endpoint_dir   # noqa: E402
    rc = 0
    dirs = sorted(d for d in _g.glob(os.path.join(work, "*"))
                  if os.path.isfile(os.path.join(d, "neb.in")))
    if only:
        dirs = [d for d in dirs if os.path.basename(d) in only]
    if not dirs:
        print(f"⛔ {work} 에 neb.in 이 있는 폴더가 없다")
        return 1
    for d in dirs:
        tag = os.path.basename(d)
        nt = open(os.path.join(d, "neb.in"), errors="ignore").read()
        i1, i2 = nt.find("FIRST_IMAGE"), nt.find("LAST_IMAGE")
        i3 = nt.find("END_POSITIONS")
        if min(i1, i2, i3) < 0:
            print(f"⛔ {tag}: neb.in 에 FIRST_IMAGE/LAST_IMAGE/END_POSITIONS 가 없다")
            rc = 1
            continue
        print(f"── {tag} ──")
        for name, (s, e) in (("ep_initial", (i1, i2)), ("ep_final", (i2, i3))):
            want = _atomic_rows(nt, s, e)
            srcd = endpoint_dir(d, name)
            outp = os.path.join(srcd, "relax.out")
            if not os.path.isfile(outp):
                print(f"   ⛔ {name}: relax.out 없음 ({srcd})")
                rc = 1
                continue
            tx = open(outp, errors="ignore").read()
            if "Begin final coordinates" not in tx:
                print(f"   ⛔ {name}: **수렴본이 아니다** — 'Begin final coordinates' 없음"
                      f" ({os.path.basename(srcd)}). NEB 을 걸면 안 된다")
                rc = 1
                continue
            k = tx.rfind("Begin final coordinates")
            e2 = tx.find("End final coordinates", k)
            got = _atomic_rows(tx, k, e2 if e2 > 0 else None)
            if not want or not got:
                print(f"   ⛔ {name}: 좌표 블록을 못 읽었다 (단위가 angstrom 인지 볼 것)")
                rc = 1
                continue
            if len(want) != len(got) or [r[0] for r in want] != [r[0] for r in got]:
                print(f"   ⛔ {name}: 원자 목록이 다르다 "
                      f"(neb.in {len(want)} vs relax.out {len(got)})")
                rc = 1
                continue
            dmax = max(max(abs(a - b) for a, b in zip(p, q)) for (_, p), (_, q)
                       in zip(want, got))
            if dmax <= tol:
                print(f"   ✅ {name}: {os.path.basename(srcd)}/relax.out 수렴본과 일치 "
                      f"(최대 |Δ| {dmax:.2e} Å, {len(want)}원자)")
            else:
                print(f"   ⛔ {name}: **좌표가 다르다** — 최대 |Δ| {dmax:.4f} Å "
                      f"vs 수렴본 {os.path.basename(srcd)}/relax.out")
                print(f"      → neb.in 이 미수렴 끝점 위에 세워졌다. "
                      f"build_neb_inputs.py 로 다시 만들고 NEB 을 다시 걸 것")
                rc = 1
    return rc


def uma_scout(args):
    """**어느 홉을 DFT 로 잴지** UMA 로 먼저 고른다. 답이 아니라 정찰이다.

    왜 (1저자 지시 "li3nd·li2s 처럼 두세 번 계산 안 하면 된다"):
      li3nd 는 DFT NEB 를 **세 번** 돌았다 — v2 c–b 6.8일(안 일어나는 홉) +
      ccpath c–c 6.2일(진짜 경로) + cc333 셀수렴(진행 중). 6.8일이 통째로 낭비였고
      그 원인은 `pick_hop` docstring 에 이미 적혀 있다: **전역 최단이 전도 경로가 아니다.**
      그 판정에 필요한 것은 절대 장벽이 아니라 **끝점 비대칭**이고, UMA 로 25분이면 난다.

    무엇을 보고 고르나 (순서대로)
      ① **끝점 에너지 차** — 공공이 안정 자리에서 불안정 자리로 밀려나는 홉은 안 일어난다
         (li3nd b–c 가 +2.05 eV 였다). 이게 1순위 배제 기준이다.
      ② 장벽 — 살아남은 shell 중 최저
      ③ **셀 수렴** — supercell 을 키워 장벽이 움직이나 (cc333 이 DFT 로 묻고 있는 것)

    ⛔ 이 값은 **논문에 못 쓴다.** UMA 이고 provisional=true 로 찍는다.
       DFT 는 여기서 고른 shell·셀로 **한 번만** 돌린다.
    """
    import numpy as _np, time as _t
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "neb_diffusion"))
    from argyrodite_cage_neb import (perp_widths, build_endpoints, relax_positions,
                                     run_neb, band_health, load_calc)
    tags = args.only or ["li3nd", "li2o", "li3p", "li3po4g", "licl"]
    scs = [tuple(int(x) for x in t.split(",")) for t in args.uma_supercells.split()]
    out = {"what": "UMA-s-1p1(omat) scout: WHICH hop and WHICH cell to spend DFT on.",
           "provisional": True,
           "not_for_publication": "MLIP barriers. DFT runs once on the chosen shell/cell.",
           "decision_rule": ["1) endpoint |dE| small = vacancy stays in its sublattice",
                             "2) lowest barrier among survivors",
                             "3) barrier stable vs supercell"],
           "runs": []}
    calc = None
    for tag in tags:
        if tag not in TARGETS:
            print(f"⛔ {tag}: TARGETS 에 없는 태그 — 오타 확인"); continue
        ref_path = TARGETS[tag][0]      # 조성 검증용 참조(verified-carry). None 이면 안 된다
        roots = [args.relaxed_from] + ([DFT_WORK_ALT] if args.relaxed_from == DFT_WORK else [])
        at0 = None; whys = []
        for rt in roots:                # Nd 계는 frozen-4f 뿌리에 있다 (DFT_WORK_ALT 주석)
            at0, why = load_relaxed(tag, ref_path, rt)
            if at0 is not None:
                print(f"   이완본: {why}"); break
            whys.append(f"{rt}: {why}")
        if at0 is None:
            print(f"⛔ {tag}: 이완본 없음 — " + " · ".join(whys)); continue
        nat0 = len(at0); om = orbit_map(at0)
        # ⛔ spglib 이 없으면 orbit 이 안 나오고 shell 열거가 통째로 빈다. 그러면 이 도구가
        #   **전역 최단 하나**로 떨어지는데, 그게 정확히 li3nd 에서 6.8일을 버린 그 실수다
        #   (pick_hop docstring ★★ 참조). 조용히 그리로 가지 않는다.
        if om is None:
            print(f"⛔ {tag}: spglib 이 없어 Li orbit 을 못 낸다 → shell 열거 불가. "
                  f"`pip install spglib` 하거나 --uma_allow_no_symmetry 로 강행할 것 "
                  f"(강행하면 전역 최단 하나만 재고, 그건 li3nd 6.8일 낭비와 같은 함정이다)")
            if not args.uma_allow_no_symmetry:
                continue
        probe = pick_hop(at0.repeat((2, 2, 2)), nat0, om)
        shells = list((probe or {}).get("neighbor_shells", {}).keys())[: args.uma_shells]
        lo = li_orbits(at0)
        print(f"\n══ {tag}  n={nat0}  {lo or ''}")
        print(f"   후보 shell {shells or ['(대칭 없음 → 전역 최단 1개, 함정 주의)']}")
        for sc in scs:
            at = at0.repeat(sc)
            W = perp_widths(at.cell)
            for sh in (shells or [None]):
                try:
                    h = pick_hop(at, nat0, om, want_shell=sh)
                except SystemExit as e:
                    print(f"   {sh}: {e}"); continue
                ini0, fin0, j2, hop = build_endpoints(at, h["vac"], h["hop"])
                if calc is None:
                    calc = load_calc(args.uma_device)
                t0 = _t.time()
                try:
                    ini, c1, _ = relax_positions(ini0, calc)
                    fin, c2, _ = relax_positions(fin0, calc)
                    dE = float(fin.get_potential_energy() - ini.get_potential_energy())
                    imgs, E, info = run_neb(ini, fin, calc, args.uma_images, args.uma_steps)
                except Exception as ex:                      # OOM 등 — 죽지 말고 남긴다
                    print(f"   {sh or 'shortest'} ×{sc}: ⛔ {type(ex).__name__}: {str(ex)[:80]}")
                    out["runs"].append({"tag": tag, "shell": sh, "supercell": list(sc),
                                        "error": f"{type(ex).__name__}: {str(ex)[:160]}"})
                    continue
                probs, hh = band_health(E)
                rec = {"tag": tag, "shell": sh or "shortest", "supercell": list(sc),
                       "n_atoms": len(at),
                       # ⛔ 2026-08-20 (codex 동결감사) — scout 가 **면 높이만** 보고했다.
                       #   점결함 이미지 거리의 정본 지표는 λ₁ 이다(2026-08-16 확정). 면 높이는
                       #   보수적 하한이라 남기되, 판정에 쓰는 값이 기록에 없으면 안 된다.
                       "lambda1_A": round(shortest_translation(at.cell), 3),
                       "min_perp_width_A": round(float(W.min()), 3),
                       "_cell_metric": "lambda1 (canonical) · perp_width = conservative lower bound",
                       "hop_distance_A": round(hop, 4),
                       "endpoint_dE_eV": round(dE, 4),
                       "Ea_forward_eV": round(float(E.max() - E[0]), 4),
                       "Ea_reverse_eV": round(float(E.max() - E[-1]), 4),
                       "profile_eV_rel": [round(float(x - E[0]), 4) for x in E],
                       "band_problems": probs, **info, **hh,
                       "trustworthy": bool(info["ci_converged"] and not probs),
                       "seconds": round(_t.time() - t0, 1), "provisional": True}
                out["runs"].append(rec)
                flag = "⛔ 안 일어나는 홉" if abs(dE) > 0.5 else ("⚠" if abs(dE) > 0.2 else "✅")
                print(f"   {rec['shell']:8s} ×{sc} n={len(at):4d} d={hop:.3f}Å  "
                      f"끝점차 {1000*dE:+7.0f} meV {flag}  Ea {rec['Ea_forward_eV']:.3f}/"
                      f"{rec['Ea_reverse_eV']:.3f} eV  ({rec['seconds']:.0f}s"
                      f"{'' if rec['trustworthy'] else ', 못 믿음'})")
                for q in probs:
                    print(f"        · {q}")
        Path(args.uma_out).write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(f"\n→ {args.uma_out}  ({len(out['runs'])}건)")
    return 0


def _selftest():
    """λ₁ · protocol_hash 회귀. **음성 경로 포함** — 틀린 입력을 잡아내는지까지 본다.

    ⛔ 이 selftest 가 못 하는 것: QE 입력 생성 · pseudo 배치 · 구조 파싱은 안 본다
      (파일·네트워크가 필요하다). 여기서 고정하는 것은 **순수 기하/해시**뿐이다.
    """
    import numpy as _np
    fails, n, neg = [], 0, 0

    def ck(name, got, exp, tol=1e-6):
        nonlocal n
        n += 1
        if not (isinstance(got, float) and abs(got - exp) <= tol) and got != exp:
            fails.append(f"{name}: got {got!r} != {exp!r}")

    def ck_raises(name, fn, exc=Exception):
        nonlocal n, neg
        n += 1
        neg += 1
        try:
            fn()
        except exc:
            return
        except Exception as e:                      # noqa: BLE001
            fails.append(f"{name}: 예외 종류가 다르다 — {type(e).__name__}")
            return
        fails.append(f"{name}: **예외가 안 났다** (음성 경로 실패)")

    # ── 양성: 알려진 λ₁ ──────────────────────────────────────────────────
    ck("cubic10", shortest_translation([[10, 0, 0], [0, 10, 0], [0, 0, 10]]), 10.0)
    ck("ortho", shortest_translation([[7, 0, 0], [0, 9, 0], [0, 0, 11]]), 7.0)
    #   fcc conventional a=10 → 최단 병진은 면심 (a/√2)
    ck("fcc10", shortest_translation([[0, 5, 5], [5, 0, 5], [5, 5, 0]]), 7.0710678, 1e-5)

    # ── 음성: 유한-R 탐색이 놓치는 기운 셀 (Codex 2·3차 반례) ────────────
    #   이 둘이 통과하지 못하면 exact 가 아니다. 옛 구현(고정 R=3 / R 배증 수렴)은 여기서 죽는다.
    ck("codex2_skew", shortest_translation([[10, 0, 0], [2.49, 0.1, 0], [0, 0, 10]]), 0.401995, 1e-5)
    ck("codex3_earlystop", shortest_translation([[10, 0, 0], [0.5, 0.001, 0], [0, 0, 10]]), 0.020, 1e-6)
    #   ↑ 옛 adaptive 는 R=3 과 R=6 에서 **둘 다** 0.500001 을 내고 "수렴" 으로 종료했다.
    ck("codex3_notfacehgt",
       shortest_translation([[10, 0, 0], [0.5, 0.001, 0], [0, 0, 10]]) < 0.5, True)

    # ── 음성: 면 높이로 재판정하면 뒤집히는 실측 (2026-08-16 철회 지표) ──
    li3nd = [[0, 7.3339, 7.3339], [7.3339, 0, 7.3339], [7.3339, 7.3339, 0]]   # fcc 2x2x2 (실측)
    l1, faces = cell_metrics(li3nd)
    ck("li3nd_lambda1_ge10", l1 >= 10.0, True)
    ck("li3nd_facehgt_lt10", min(faces) < 10.0, True)   # 면높이면 오탈락 → 판정 반전 고정

    # ── 정수 계수 · unimodular 불변 ──────────────────────────────────────
    C = _np.array([[10, 0, 0], [2.49, 0.1, 0], [0, 0, 10]], float)
    l1c, ncoef, _ = shortest_translation_full(C)
    ck("coef_reconstructs", float(_np.linalg.norm(_np.asarray(ncoef, float) @ C)), l1c, 1e-9)
    ck("coef_is_integer", all(isinstance(v, int) for v in ncoef), True)
    for k, U in enumerate([[[1, 3, 0], [0, 1, 0], [0, 0, 1]],
                           [[1, 0, 0], [5, 1, 7], [0, 0, 1]],
                           [[0, 1, 0], [1, 0, 0], [-2, 4, -1]]]):
        ck(f"unimodular_invariance[{k}]",
           shortest_translation(_np.asarray(U, float) @ C), l1c, 1e-9)

    # ── 음성: unimodular 검사가 진짜 검사인가 (codex 동결감사 2026-08-20) ──
    #   옛 검사 `abs(round(det))==1` 은 det=1.4 / 0.6 을 통과시켰다. 정수성과 |det| 를
    #   따로 봐야 한다. ASE 를 못 건드리니 검사 함수를 직접 부딪친다.
    import numpy as _n2

    def _uni_check(op):
        a = _n2.asarray(op, float)
        if not _n2.allclose(a, _n2.round(a), atol=1e-9):
            raise RuntimeError("정수 아님")
        if abs(abs(float(_n2.linalg.det(a))) - 1.0) > 1e-9:
            raise RuntimeError("|det| != 1")
        return True
    ck("uni_accepts_identity", _uni_check([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), True)
    ck("uni_accepts_det_minus1", _uni_check([[0, 1, 0], [1, 0, 0], [0, 0, 1]]), True)
    ck_raises("uni_rejects_det_1p4", lambda: _uni_check([[1.4, 0, 0], [0, 1, 0], [0, 0, 1]]), RuntimeError)
    ck_raises("uni_rejects_det_0p6", lambda: _uni_check([[0.6, 0, 0], [0, 1, 0], [0, 0, 1]]), RuntimeError)
    ck_raises("uni_rejects_int_det2", lambda: _uni_check([[2, 0, 0], [0, 1, 0], [0, 0, 1]]), RuntimeError)

    # ── 음성: 병든 입력은 **경고가 아니라 즉사** ─────────────────────────
    ck_raises("degenerate_cell",
              lambda: shortest_translation([[10, 0, 0], [10, 1e-12, 0], [0, 0, 10]]), ValueError)
    ck_raises("zero_vector", lambda: shortest_translation([[0, 0, 0], [0, 9, 0], [0, 0, 11]]), ValueError)
    ck_raises("nan_cell", lambda: shortest_translation([[float("nan"), 0, 0], [0, 9, 0], [0, 0, 11]]), ValueError)
    ck_raises("wrong_shape", lambda: shortest_translation([[10, 0], [0, 9]]), ValueError)

    # ── protocol_hash: 같은 입력 = 같은 해시, 다른 입력 = 다른 해시 ──────
    #   ⚠ payload 안의 lambda1_A 는 **의도적으로 3자리 반올림**이다 (부동소수 잡음으로
    #     지문이 흔들리면 이월이 무의미해진다). "문턱 비교 전 반올림 금지" 는 게이트
    #     판정에 대한 규칙이고 해시 정규화와는 별개다 — 게이트는 원값을 쓴다.
    ns = argparse.Namespace(images=7, path_thr=0.05, min_l=10.0, min_l_basis="lambda1",
                            allow_unrelaxed_endpoints=False)
    base = dict(tag="x", a=ns, q=-1, kpts=(3, 3, 3), nat=64,
                cell=[[10, 0, 0], [0, 10, 0], [0, 0, 10]])
    h0 = protocol_hash(**base)
    ck("hash_stable", protocol_hash(**base), h0)
    ck("hash_kpts_sensitive", protocol_hash(**{**base, "kpts": (5, 5, 5)}) != h0, True)
    ck("hash_charge_sensitive", protocol_hash(**{**base, "q": 0}) != h0, True)
    ck("hash_cell_sensitive",
       protocol_hash(**{**base, "cell": [[11, 0, 0], [0, 10, 0], [0, 0, 10]]}) != h0, True)
    ns2 = argparse.Namespace(images=7, path_thr=0.05, min_l=10.0, min_l_basis="vector",
                             allow_unrelaxed_endpoints=False)
    ck("hash_basis_sensitive", protocol_hash(**{**base, "a": ns2}) != h0, True)

    # ── payload 분리 + 계보 필드 (codex 동결감사 2026-08-20) ─────────────
    pay = protocol_payload(**base)
    for k in ("hash_schema", "lambda1_method_id", "ase_version", "lambda1_A"):
        ck(f"payload_has[{k}]", k in pay, True)
    ck("payload_method_id", pay["lambda1_method_id"], LAMBDA1_METHOD_ID)
    ck("payload_ase_nonempty", bool(pay["ase_version"]), True)
    #   ⭐ 계보 필드가 지문에 **실제로 반영**되는가 — 값을 바꾸면 해시가 달라져야 한다.
    #   (문자열만 payload 에 얹고 해시는 옛 키만 보는 실수를 잡는 음성 시험)
    import hashlib as _h, json as _j
    def _hash_of(d):
        return _h.sha256(_j.dumps(d, sort_keys=True).encode()).hexdigest()[:12]
    ck("hash_covers_payload", _hash_of(pay), h0)
    ck("hash_reacts_to_ase", _hash_of({**pay, "ase_version": "0.0.0"}) != h0, True)
    ck("hash_reacts_to_method", _hash_of({**pay, "lambda1_method_id": "M-old"}) != h0, True)
    #   진단: 무엇이 바뀌었는지 말할 수 있어야 한다 (이월 거부 사유)
    d = protocol_diff(pay, {**pay, "ase_version": "0.0.0"})
    ck("diff_reports_one", len(d) == 1 and d[0].startswith("ase_version:"), True)
    ck("diff_empty_when_same", protocol_diff(pay, dict(pay)), [])

    # ── verify_endpoints: 임시 트리로 양성 1 · 음성 4 ─────────────────────────
    import tempfile as _tf
    import contextlib as _cl
    import io as _io

    def _mk(root, tag, ini, fin, relax_ini, relax_fin, conv=True, suf="_r2"):
        d = os.path.join(root, tag)
        for nm, blk in (("ep_initial", relax_ini), ("ep_final", relax_fin)):
            dd = os.path.join(d, nm + suf)
            os.makedirs(dd, exist_ok=True)
            body = "Begin final coordinates\n" if conv else ""
            body += "ATOMIC_POSITIONS (angstrom)\n" + blk
            body += "End final coordinates\n" if conv else ""
            open(os.path.join(dd, "relax.out"), "w").write(body)
        open(os.path.join(d, "neb.in"), "w").write(
            "BEGIN_POSITIONS\nFIRST_IMAGE\nATOMIC_POSITIONS angstrom\n" + ini +
            "LAST_IMAGE\nATOMIC_POSITIONS angstrom\n" + fin + "END_POSITIONS\n")
        return d

    def _run(root, tag):
        buf = _io.StringIO()
        with _cl.redirect_stdout(buf):
            r = verify_endpoints(root, [tag])
        return r, buf.getvalue()

    A = "  Li     0.0000000000     0.0000000000     0.0000000000\n" \
        "  S      1.5000000000     1.5000000000     1.5000000000\n"
    B = "  Li     2.0000000000     0.0000000000     0.0000000000\n" \
        "  S      1.5000000000     1.5000000000     1.5000000000\n"
    A_off = "  Li     0.0000000000     0.0000000000     0.4000000000\n" \
            "  S      1.5000000000     1.5000000000     1.5000000000\n"
    A_sym = "  Na     0.0000000000     0.0000000000     0.0000000000\n" \
            "  S      1.5000000000     1.5000000000     1.5000000000\n"
    with _tf.TemporaryDirectory() as _r:
        _mk(_r, "ok", A, B, A, B)                       # ① 양성
        ck("vep_pass", _run(_r, "ok")[0], 0)
        _mk(_r, "drift", A, B, A_off, B)                # ② 음성: 좌표가 다르다
        rc2, out2 = _run(_r, "drift")
        ck("vep_drift_rc", rc2, 1)
        ck("vep_drift_msg", "좌표가 다르다" in out2, True)
        neg += 1
        # ③ 음성: 수렴본이 아니다 (suf="" — endpoint_dir 이 원본으로 되돌아오는 경로)
        _mk(_r, "unconv", A, B, A, B, conv=False, suf="")
        rc3, out3 = _run(_r, "unconv")
        ck("vep_unconv_rc", rc3, 1)
        ck("vep_unconv_msg", "수렴본이 아니다" in out3, True)
        neg += 1
        # ③' 수렴본이 아예 없고 디렉터리도 없으면 '없음' 으로 잡는다 (다른 문구, 같은 ⛔)
        _mk(_r, "nodir", A, B, A, B, conv=False)
        rc3b, out3b = _run(_r, "nodir")
        ck("vep_nodir_rc", rc3b, 1)
        ck("vep_nodir_msg", "relax.out 없음" in out3b, True)
        neg += 1
        _mk(_r, "sym", A, B, A_sym, B)                  # ④ 음성: 원자 목록이 다르다
        rc4, out4 = _run(_r, "sym")
        ck("vep_symbol_rc", rc4, 1)
        ck("vep_symbol_msg", "원자 목록이 다르다" in out4, True)
        neg += 1
        # ⑤ 음성: `_r2` 수렴본을 두고 미수렴 원본을 물고 있으면 잡아야 한다
        #    (이게 cc333 을 며칠 태울 뻔한 바로 그 상황이다)
        d5 = _mk(_r, "stale", A_off, B, A, B)
        os.makedirs(os.path.join(d5, "ep_initial"), exist_ok=True)
        open(os.path.join(d5, "ep_initial", "relax.out"), "w").write(
            "The maximum number of steps has been reached.\n"
            "ATOMIC_POSITIONS (angstrom)\n" + A_off)
        rc5, out5 = _run(_r, "stale")
        ck("vep_stale_rc", rc5, 1)
        ck("vep_stale_msg", "미수렴 끝점 위에 세워졌다" in out5, True)
        neg += 1

    if fails:
        print(f"⛔ selftest 실패 {len(fails)}/{n}")
        for f in fails:
            print("   ✗", f)
        return 1
    print(f"✅ selftest {n}/{n} 통과 (λ₁ exact · 예외 요구 {neg}건 · 유한-R 반례 2건 포함)")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true",
                    help="λ₁ exact · 해시 회귀 검사 (음성 경로 포함). 파일 I/O 없음")
    ap.add_argument("--work", default=WORK)
    ap.add_argument("--pseudo_dir", default="/data/work/pseudo")
    ap.add_argument("--min_l", type=float, default=10.0,
                    help="공공-공공 주기 거리의 최소값 [Å] (기본 기준 = λ₁ 최단 격자 병진)")
    ap.add_argument("--min_l_basis", choices=("lambda1", "vector"), default="lambda1",
                    help="min_l 을 무엇으로 재나. lambda1 = 최단 격자 병진(기본, 점결함 이미지 거리) · "
                         "vector = 격자벡터 길이(옛 동작). ⛔ 면 높이(perp)는 슬랩용이라 뺐다"
                         "옳다) · vector = 격자벡터 길이(2026-08-16 이전 동작, 비직교 셀에서 "
                         "이미지 거리를 과대평가한다)")
    ap.add_argument("--images", type=int, default=7, help="NEB 이미지 수 (끝 2개 포함)")
    ap.add_argument("--nstep", type=int, default=100)
    ap.add_argument("--path_thr", type=float, default=0.05, help="경로 수렴 [eV/Å]")
    ap.add_argument("--hop_shell", default=None,
                    help="홉을 Wyckoff shell 로 지정 (예: 'c-c'). 기본은 전역 최단인데, "
                         "그게 공공을 불안정 자리로 미는 경로일 수 있다 (li3nd 실측 +2.05 eV). "
                         "먼저 --hop_shell 없이 돌려 meta.json 의 neighbor_shells 를 볼 것.")
    ap.add_argument("--kdens", type=float, default=0.04,
                    help="k 밀도 [Å⁻¹] — 슈퍼셀이라 성기게 잡는다")
    ap.add_argument("--only", nargs="*", help="일부만")
    ap.add_argument("--ci_scheme", choices=("no-CI", "auto"), default="no-CI",
                    help="QE 권고: **no-CI 로 먼저 수렴**시킨 뒤 restart + auto. "
                         "옛 기본값 auto 는 처음부터 CI 를 켠 것이라 권고와 어긋났다")
    ap.add_argument("--restart", action="store_true",
                    help="restart_mode='restart'. 용례 둘: ① 중단된 no-CI 런 이어달리기 "
                         "② no-CI 수렴본 위에 CI. **<tag>.path 가 없으면 거부한다** "
                         "(옛 판은 no-CI 면 이 플래그를 조용히 무시했다 — 리뷰 I P0-3)")
    ap.add_argument("--allow_unrelaxed_endpoints", action="store_true",
                    help="⚠ vacancy 끝점 이완 없이 강행 — Ea=0 사고의 미해결 절반. 디버그 전용")
    ap.add_argument("--vacancy_charge", choices=("minus1", "neutral"), default="minus1",
                    help="minus1 = V_Li⁻ (닫힌 껍질, tot_charge=-1, 기본) · "
                         "neutral = V_Li⁰ (정공 1개, tot_charge=0). "
                         "⚠ 옛 규약 tot_charge=+1 은 정공 2개라 틀렸다 — 폐기됨")
    ap.add_argument("--relaxed_from", default=DFT_WORK,
                    help="vc-relax 산출물 뿌리 (기본: run_sei_dft.sh 의 WORK)")
    ap.add_argument("--allow_unrelaxed", action="store_true",
                    help="⚠ 비이완 MP 구조로 강행 — li3p Ea=0 사고의 원인. 디버그 전용")
    # ⛔ 2026-08-11 자체검토 P0-1 — build() 가 이 인자를 참조하는데 정의가 없어서
    #   **게이트가 걸리는 순간 AttributeError 로 죽었다**. 절연체는 short-circuit 으로
    #   살아남고 lindo2 에서 처음 터져, 이번 분기의 주인공 두 상(lindo2·li3nd)만
    #   깔끔한 skip 대신 traceback 이었다. 재현: --plan --only lindo2
    ap.add_argument("--ignore_electronic_class", action="store_true",
                    help="⚠ electronic_class 게이트 무시 — 디버그 전용. "
                         "금속에 절연체 규약을 걸거나 4f 미해결 상을 강행하게 된다")
    ap.add_argument("--pseudo_list", action="store_true",
                    help="pseudo 전체 목록을 찍는다 (기본은 우리 계 원소만)")
    ap.add_argument("--uma_scout", action="store_true",
                    help="DFT 전에 UMA 로 **어느 홉·어느 셀**인지 정찰 (논문값 아님)")
    ap.add_argument("--uma_shells", type=int, default=4, help="시험할 shell 수")
    ap.add_argument("--uma_supercells", default="1,1,1 2,2,2")
    ap.add_argument("--uma_images", type=int, default=5)
    ap.add_argument("--uma_steps", type=int, default=800)
    ap.add_argument("--uma_device", default="cuda")
    ap.add_argument("--uma_out", default="db/properties/sei_neb_uma_scout.json")
    ap.add_argument("--uma_allow_no_symmetry", action="store_true",
                    help="spglib 없이 강행 (⚠ 전역 최단만 잰다 — li3nd 함정)")
    ap.add_argument("--plan", action="store_true",
                    help="⚠ 비용만 보고 **입력을 만들지 않는다** (돌리기 전에 이걸 먼저)")
    ap.add_argument("--verify_endpoints", action="store_true",
                    help="이미 만든 neb.in 의 끝점이 **수렴한** relax.out 좌표와 같은지 "
                         "대조만 한다 (입력을 만들지 않는다). NEB 을 며칠 태우기 전에 이걸 먼저")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()

    # ⭐ 대조만 하는 모드 — pseudo·구조 파일을 아예 안 본다. 갈래를 위로 둔다.
    if a.verify_endpoints:
        return verify_endpoints(a.work, a.only)

    # ⭐ UMA 정찰은 pseudo·QE 를 아예 안 본다 — 아래 준비 단계보다 **먼저** 갈라진다.
    if a.uma_scout:
        raise SystemExit(uma_scout(a))

    pool = find_pseudos(a.pseudo_dir)
    # ⚠ 출력은 기본이 요약이다 (CLAUDE.md). pseudo 100여 종을 매번 찍으면 정작
    #   봐야 할 ⛔ 줄이 스크롤 밖으로 밀린다 — 실제로 그랬다.
    print(f"pseudo 디렉터리 {a.pseudo_dir} — {len(pool)}종"
          + ("" if pool else "  ⚠ 비어 있다")
          + ("" if "--pseudo_list" in sys.argv else "  (목록은 --pseudo_list)"))
    _want = {"Li", "Nd", "S", "P", "O", "Cl"}          # 우리 계에 실제로 쓰는 것
    for e in sorted(_want & set(pool)):
        print(f"  {e:3s} {pool[e]}")
    if "--pseudo_list" in sys.argv:
        for e, f in sorted(pool.items()):
            if e not in _want:
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
        o = r.get("li_orbits")
        if o:
            # ⛔ 2026-08-12 — 여기서 **전역 orbit 수**로 판정하고 있었다. Codex 가 회수기에
            #   대해 지적한 P0-4 와 같은 버그인데 표시만 안 고쳐져 있었다. 구조에 Li 자리가
            #   2종이라는 사실은 "선택한 쌍이 비등가" 라는 뜻이 아니다 —
            #   c-c 홉은 자리가 2종이어도 **끝점이 대칭 동등**하다.
            pe = r.get("pair_equivalent")
            sh = r.get("hop_shell")
            verdict = ("**대칭 동등** (정=역 장벽이어야 한다)" if pe is True else
                       "**비대칭** (정≠역이 정상 — 두 자리의 에너지 차다)" if pe is False else
                       "**등가성 미상** (쌍 orbit 을 못 읽었다 — Δ끝점 게이트가 꺼진다)")
            print(f"     대칭 {o['spacegroup']} · Li 자리 {o['n_li_orbits']}종 "
                  f"{o['wyckoffs']}"
                  + (f" · 홉 shell {sh}" if sh else "") + f" → 끝점 " + verdict)
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
    print("⚠ 전하 규약은 상의 electronic_class 로 갈린다 (db/properties/sei_electronic_class.json):")
    print("   · insulator → tot_charge = −1 (V_Li⁻) + jellium. 유한 셀 근사가 남으므로")
    print("     **상 사이 비교**에 쓰고 절대값은 셀 수렴 확인 뒤 인용할 것.")
    print("   · metal     → tot_charge = 0 (중성 공공) · mv smearing. jellium 없음.")
    print("   ⛔ 2026-08-11 이전의 tot_charge=+1 입력은 정공 2개짜리라 **무효**다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
