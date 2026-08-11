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
import sys

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
}
DFT_WORK = "/data/work/runs/sei_dft"      # run_sei_dft.sh 의 vc-relax 산출물 (이완본 출처)


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


def pick_hop(at, nat0=None, omap=None):
    """공공 자리 A 와 그리로 뛸 Li B 를 고른다.

    최근접 Li–Li 쌍을 쓴다 = **기본 홉**. 더 긴 경로는 이것들의 조합이므로 먼저 이걸 잰다.
    ⚠ 끝점은 감싼 좌표가 아니라 `pos[B] + 최소이미지 벡터` 로 만든다(위 함정 ①).

    ★ 2026-08-11 (Codex 검토 P0-4) — **선택한 쌍의 등가성**을 기록한다.
      구조 전체에 Li orbit 이 2종이라는 사실은 "선택된 A/B 가 비등가"라는 뜻이 **아니다**.
      Li₃P 의 최단 2.512 Å 쌍은 실제로 f–f **동등자리**이고 b–f 는 2.741 Å 다.
      옛 코드는 전역 orbit 수만 보고 비등가로 판정해 `site_energy_diff==0` 차단을
      false positive 로 걸었다. 이제 쌍 자체의 orbit 을 본다.
      (ASE repeat 는 블록 타일링이라 supercell index % nat0 = 원본 index.)
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
    vec = at.get_distance(B, A, mic=True, vector=True)
    out = {"d": float(d), "vac": A, "hop": B, "vec": np.asarray(vec, float),
           "pair_orbits": None, "pair_equivalent": None}
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


def protocol_hash(tag, a, q, kpts, nat, cell, smear=None, degauss=None,
                  ecls=None, pps=None) -> str:
    """입력 규약 지문 — 프로토콜이 바뀌면 옛 neb.out/tmp/prefix.path 를 재사용하면 안 된다.

    ★ 2026-08-11 (Codex 검토 P0-3) — 같은 WORK 에 새 입력을 쓰면 runner 가 옛 neb.out 의
      'convergence achieved' 만 보고 건너뛴다. 그러면 **새 meta.json 과 옛 에너지가 결합**된다.
      기존 li2s 는 min_cell 8.02 인데 새 기본은 --min_l 10 이라 실제로 일어날 수 있었다.
    """
    import hashlib
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
               "nat": nat, "min_l": a.min_l,
               "cell": [round(float(x), 6) for v in cell for x in v],
               "smearing": smear, "degauss": degauss,
               "electronic_class": (ecls or {}).get("class"),
               "pseudos": dict(sorted((pps or {}).items())),
               "endpoints_relaxed": not a.allow_unrelaxed_endpoints}
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
    L = at0.cell.lengths()
    rep = tuple(max(1, int(np.ceil(a.min_l / x))) for x in L)
    at = at0.repeat(rep)
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
    hop = pick_hop(at, nat0=len(at0), omap=omap)
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
        outp = os.path.join(epd, "relax.out")
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
            (f"  restart_mode    = 'restart'" if a.ci_scheme != "no-CI" and a.restart
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
    open(os.path.join(d, "neb.in"), "w").write("\n".join(body))
    # ★ 회수기가 대칭 게이트를 켤지 말지 여기서 판단한다 (위 li_orbits 주석 참조).
    _j = json
    _j.dump({"tag": tag, "disp": disp, "supercell": list(rep), "nat": nat,
             "hop_distance_A": hop["d"], "nelec": nelec_vac,
             "protocol_hash": protocol_hash(tag, a, q, info["kpts"], nat, at.cell.array,
                                            smear=smear, degauss=degauss, ecls=ecls,
                                            pps={e: pool[e] for e in els}),
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
    ap.add_argument("--ci_scheme", choices=("no-CI", "auto"), default="no-CI",
                    help="QE 권고: **no-CI 로 먼저 수렴**시킨 뒤 restart + auto. "
                         "옛 기본값 auto 는 처음부터 CI 를 켠 것이라 권고와 어긋났다")
    ap.add_argument("--restart", action="store_true",
                    help="restart_mode='restart' (2단계 CI 에서 쓴다)")
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
        o = r.get("li_orbits")
        if o:
            eqv = o["n_li_orbits"] == 1
            print(f"     대칭 {o['spacegroup']} · Li 자리 {o['n_li_orbits']}종 "
                  f"{o['wyckoffs']} → 끝점 "
                  + ("**대칭 동등** (정=역 장벽이어야 한다)" if eqv else
                     "**비대칭** (정≠역이 정상 — 두 자리의 에너지 차다)"))
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
