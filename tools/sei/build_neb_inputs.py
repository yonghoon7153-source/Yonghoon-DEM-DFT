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
import os
import sys

import numpy as np

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


def build(tag, path, disp, a, pool):
    from ase.io import read
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

    hop = pick_hop(at)
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
            f"    tot_charge      = {q:.1f}",
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
    # ★ 회수기가 대칭 게이트를 켤지 말지 여기서 판단한다 (위 li_orbits 주석 참조).
    import json as _j
    _j.dump({"tag": tag, "disp": disp, "supercell": list(rep), "nat": nat,
             "hop_distance_A": hop["d"], "nelec": nelec_vac,
             "tot_charge": q, "vacancy_charge": a.vacancy_charge,
             "charge_convention": "QE: +1=전자 부족, -1=전자 추가. V_Li- 는 -1 이다. "
                                  "2026-08-11 이전 입력은 +1(정공 2개)이라 무효.",
             "num_of_images": a.images,
             "min_cell_A": min(info["L"]), "kpts": info["kpts"],
             "li_orbits": orb,
             "endpoints_symmetry_equivalent": (orb or {}).get("n_li_orbits") == 1,
             "arrival_err_A": info["arrival_err"],
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
    ap.add_argument("--vacancy_charge", choices=("minus1", "neutral"), default="minus1",
                    help="minus1 = V_Li⁻ (닫힌 껍질, tot_charge=-1, 기본) · "
                         "neutral = V_Li⁰ (정공 1개, tot_charge=0). "
                         "⚠ 옛 규약 tot_charge=+1 은 정공 2개라 틀렸다 — 폐기됨")
    ap.add_argument("--relaxed_from", default=DFT_WORK,
                    help="vc-relax 산출물 뿌리 (기본: run_sei_dft.sh 의 WORK)")
    ap.add_argument("--allow_unrelaxed", action="store_true",
                    help="⚠ 비이완 MP 구조로 강행 — li3p Ea=0 사고의 원인. 디버그 전용")
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
    print("⚠ tot_charge=+1 (Li⁺ 공공) 이다. jellium 보정은 유한 셀 근사라 셀 크기 의존이 남는다")
    print("  — 장벽의 **상 사이 비교**에는 쓰되 절대값은 셀 수렴을 확인하고 인용할 것.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
