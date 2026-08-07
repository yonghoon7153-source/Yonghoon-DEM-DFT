#!/usr/bin/env python3
"""build_dft_inputs.py — SEI 상들의 **갭 + DOS/PDOS** QE 입력 일괄 생성.

체인 (조성마다)
  ① vc-relax  — MP 구조는 VASP/PAW 로 이완된 것이라 우리 QE/USPP 평형부피와 다르다.
                 부피가 다르면 갭이 움직이므로 먼저 우리 조건으로 이완한다. (셀이 작아 싸다)
  ② scf       — 이완된 기하에서
  ③ **nscf (occupations='fixed', 조밀 k)** — ★ 갭은 **여기서 VBM/CBM 고유값으로만** 낸다
  ④ nscf + dos.x     — 전체 DOS (그림용)
  ⑤ projwfc.x        — PDOS (원소·궤도 분해)

⚠⚠ **갭을 DOS 문턱으로 읽지 말 것** (CLAUDE.md 규율). DOS 는 Gaussian 퍼짐 때문에
  ~0.3 eV 과소평가된다. 갭의 정본은 ③의 고유값이고, DOS/PDOS 는 **그림과 성분 분해용**이다.

⚠ PBE 갭은 이 계열(넓은 갭 절연체)에서 계통적으로 30–50% 과소평가된다.
  실험값과 나란히 놓지 말고 **6종 사이의 상대 비교**와 같은 방법의 문헌값 대조로 쓴다.

⚠ Nd 계열(LiNdO₂·Nd₂O₃·Nd₂S₃): 우리 pseudo 는 z_valence=14 로 **4f 가 valence** 다.
  PBE 만으로는 4f 가 E_F 에 걸려 갭이 무의미해진다. 우리 repo 노트가 이미
  "PBE+U 는 Nd 4f 를 잘못 배치하고, **갭 가장자리가 4f 면 실패한다**" 고 적어 놓았고
  이 세 상이 정확히 그 경우다. → `--nd_u` 로 U 를 걸 수는 있지만 **기본은 진단용**이며,
  최종 수치는 MP 의 frozen-4f 값을 출처 명시해 인용하는 편이 정직하다.

  python3 tools/sei/build_dft_inputs.py                 # 입력 생성 + pseudo 점검
  python3 tools/sei/build_dft_inputs.py --nd_u 6.0      # Nd 4f 에 U (진단용)
"""
import argparse
import glob
import json
import os
import sys

ECUTWFC, ECUTRHO = 60.0, 480.0        # Ry — USPP/PAW 기준 (pseudo 요구 최대 47/326 위)
KDENS_SCF, KDENS_NSCF = 0.30, 0.15    # Å⁻¹ 간격 — 갭용 nscf 를 2배 조밀하게
# ⚠ DOS/PDOS 용 nscf 는 **대칭을 끄고**(projwfc 의 d_matrix 회피) 돌아야 하는데,
#   그러면 k 점이 전부 명시적으로 풀려 폭증한다. 갭만큼 조밀할 필요도 없으므로 성기게.
KDENS_DOS = 0.28
DEGAUSS = 0.01                        # Ry — scf 만 (nscf 는 fixed)
WORK = "/data/work/runs/sei_dft"
PROV = "db/properties/sei_structures_provenance.json"


def zval(path):
    """UPF 헤더에서 z_valence. nbnd 를 정하려면 전자 수를 알아야 한다."""
    import re
    try:
        head = open(path, errors="ignore").read(6000)
    except OSError:
        return None
    m = re.search(r'z_valence\s*=\s*"?\s*([\d.]+)', head, re.I)
    if m:
        return float(m.group(1))
    m = re.search(r"([\d.]+)\s+Z valence", head, re.I)      # UPF v1 텍스트 헤더
    return float(m.group(1)) if m else None


def find_pseudos(pdir):
    """pseudo 디렉터리에서 원소 → 파일명. ⚠ 없는 원소는 그대로 보고한다."""
    out = {}
    for f in sorted(os.listdir(pdir)):
        if not f.lower().endswith((".upf",)):
            continue
        el = f.split(".")[0].split("_")[0]
        el = el[0].upper() + el[1:].lower() if len(el) > 1 else el.upper()
        out.setdefault(el, f)
    return out


def kmesh(cell, dens):
    import numpy as np
    b = 2 * np.pi * np.linalg.inv(cell).T
    # ⚠ round 를 쓰면 비 1.35 가 1 로 내려가 그 축이 Γ-only 가 된다(실측: Nd2S3 [5,3,1]).
    #   장축이라도 k=2 는 싸므로 ceil 로 올림해 안전하게 간다.
    return [max(1, int(np.ceil(np.linalg.norm(v) / dens))) for v in b]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pattern", default="db/structures/sei_*.vasp")
    ap.add_argument("--pseudo_dir", default="/data/work/pseudo")
    ap.add_argument("--work", default=WORK)
    # ⚠⚠ 2026-08-07 진단으로 밝혀진 것: Nd 3종의 갭이 −0.02 eV 로 닫힌 건
    #   "PBE 가 4f 에 약해서"가 **아니라 스핀분극을 안 켠 탓**이 크다.
    #   Nd³⁺ = 4f³ 인데 nspin=1 이면 전자 3개가 7겹 f 다중항에 **분수 점유**로 퍼진다
    #   → 부분점유 밴드 = 정의상 금속. 게다가 occupations='fixed' 는 nocc=nelec/2 번째
    #   밴드까지 채우므로 VBM·CBM 이 **같은 평평한 f 다중항 안**에서 잡혀 갭이 0 이 된다.
    #   실측 증거: 화학이 전혀 다른 세 상이 −0.021/−0.022/−0.028 로 7 meV 안에서 일치했고,
    #   E_F ±0.5 eV DOS 의 95~96% 가 Nd_f 였다(peak 49/106/243 states/eV = 평평한 밴드).
    #   ★ 우리 Nd₂O₃@LPSCl1.6 계산은 nspin=2 + starting_magnetization + Hubbard U 를
    #     썼고(tools/nd/build_lobster_nd.py), 거기선 빈 4f 가 +1.77 eV 에 구경꾼으로 앉아
    #     갭 1.632 eV 가 살아남았다. 같은 처방을 여기에도 준다.
    ap.add_argument("--nd_spin", action="store_true", default=True,
                    help="Nd 계에 nspin=2 + starting_magnetization (기본 켬)")
    ap.add_argument("--no_nd_spin", dest="nd_spin", action="store_false")
    ap.add_argument("--nd_mag", type=float, default=0.3,
                    help="Nd starting_magnetization (4f³ 국소모멘트 씨앗)")
    ap.add_argument("--nd_u", type=float, default=6.0,
                    help="Nd 4f 에 U [eV] (0 = 안 걺). 기본 6.0 — 란타나이드 4f 통상값")
    a = ap.parse_args()

    from ase.io import read

    pool = find_pseudos(a.pseudo_dir)
    files = sorted(glob.glob(a.pattern))
    if not files:
        sys.exit(f"⛔ {a.pattern} 에 구조가 없다")
    os.makedirs(a.work, exist_ok=True)
    prov = json.load(open(PROV)) if os.path.isfile(PROV) else {}

    # ── pseudo 점검을 먼저 전부 한다 — 중간에 죽는 것보다 낫다 ──────────────
    need, missing = set(), set()
    for f in files:
        need |= set(read(f).get_chemical_symbols())
    for el in sorted(need):
        if el not in pool:
            missing.add(el)
    print(f"pseudo 디렉터리 {a.pseudo_dir}")
    for el in sorted(need):
        print(f"  {el:3s} {pool.get(el, '⛔ 없음')}")
    if missing:
        print(f"\n⛔ pseudo 없음: {', '.join(sorted(missing))}")
        print("   → pslibrary/SSSP 에서 받아 넣은 뒤 다시 실행할 것. 해당 조성은 건너뛴다.")

    made, skipped = [], []
    for f in files:
        tag = os.path.basename(f)[len("sei_"):-len(".vasp")]
        at = read(f)
        els = sorted(set(at.get_chemical_symbols()))
        if any(e in missing for e in els):
            print(f"\n⏭  {tag} — pseudo 없음({','.join(e for e in els if e in missing)})")
            skipped.append(tag); continue

        d = os.path.join(a.work, tag)
        os.makedirs(d, exist_ok=True)
        cell = at.cell.array
        k_scf, k_nscf = kmesh(cell, KDENS_SCF), kmesh(cell, KDENS_NSCF)
        has_nd = "Nd" in els
        nat, ntyp = len(at), len(els)

        # ⚠⚠ occupations='fixed' 인 nscf 는 QE 가 **nbnd = nelec/2 로 딱 맞춘다** —
        #   전도대가 없어 CBM 을 못 본다. nbnd 를 명시해야 갭이 나온다 (2026-08-06).
        zs = {e: zval(os.path.join(a.pseudo_dir, pool[e])) for e in els}
        if any(v is None for v in zs.values()):
            bad = [e for e, v in zs.items() if v is None]
            print(f"\n⏭  {tag} — UPF 에서 z_valence 를 못 읽었다: {','.join(bad)}")
            skipped.append(tag); continue
        nelec = sum(zs[e] for e in at.get_chemical_symbols())
        # Nd 계는 스핀분극 + U 로 간다 (아래 --nd_spin 주석). n_nd 는 tot_magnetization 용.
        n_nd = at.get_chemical_symbols().count("Nd")
        spinpol = bool(has_nd and a.nd_spin and n_nd)
        # ⚠ nspin=2 + tot_magnetization 이면 다수스핀 점유가 (nelec+M)/2 로 늘어난다.
        #   여유를 그만큼 더 준다 — 안 그러면 CBM 을 못 본다.
        pad = (3 * n_nd) // 2 if spinpol else 0
        nbnd = int(nelec / 2 * 1.35) + 8 + pad      # 점유 + 넉넉한 빈 상태 (CBM 용)
        nbnd_dos = int(nelec / 2 * 1.60) + 12 + pad  # DOS 용은 더 여유 (&ELECTRONS 주석)

        def block(calc, kpts, fixed, extra="", nosym=False, verbose=False, dos=False):
            occ = ("    occupations     = 'fixed'\n" if fixed else
                   f"    occupations     = 'smearing'\n    smearing        = 'mv'\n"
                   f"    degauss         = {DEGAUSS}\n")
            hub = ""
            if has_nd and a.nd_u > 0:
                hub = f"\nHUBBARD (ortho-atomic)\n  U Nd-4f {a.nd_u}\n"
            L = [f"&CONTROL", f"    calculation     = '{calc}'",
                 f"    prefix          = '{tag}'", "    outdir          = './tmp'",
                 f"    pseudo_dir      = '{a.pseudo_dir}'", "    tprnfor         = .true.",
                 # ⚠ projwfc.x 는 **파동함수 파일**이 있어야 돈다. nscf 의 disk_io 기본값이
                 #   낮으면 끝나고 지워져 projwfc 가 MPI_ABORT 로 죽는다(실측 2026-08-06:
                 #   dos.x 는 됐는데 projwfc.x 만 실패). nscf 에서만 남긴다.
                 ("    disk_io         = 'medium'" if calc == "nscf" else ""),
                 # ⚠⚠ verbosity 는 **&CONTROL 소속**이다. &SYSTEM 에 넣어 9/9 가
                 #   read_namelists 에서 즉사했다 (2026-08-07). real_space 를 &ELECTRONS 대신
                 #   &SYSTEM 에 넣어 같은 사고를 낸 게 하루 전이다 — 네임리스트 소속을
                 #   추측하지 말고 확인할 것.
                 #   k 점이 100개를 넘으면 QE 는 verbosity='low' 에서 밴드를 아예 안 찍는다
                 #   (실측: li2o k 1098개 → 'bands (ev)' 0개 → 갭 추출 전멸).
                 ("    verbosity       = 'high'" if verbose else ""),
                 "    tstress         = .true." if calc == "vc-relax" else "", "/",
                 "&SYSTEM", "    ibrav           = 0", f"    nat             = {nat}",
                 f"    ntyp            = {ntyp}", f"    ecutwfc         = {ECUTWFC}",
                 f"    ecutrho         = {ECUTRHO}",
                 # ⚠ DOS 용 nscf 는 밴드를 더 준다. 제일 위 몇 밴드는 Davidson 이 항상
                 #   제일 늦게 수렴하는데, 여유 밴드가 그 실패를 흡수한다(어차피 안 쓴다).
                 (f"    nbnd            = {nbnd_dos if dos else nbnd}"
                  if calc == "nscf" else ""),
                 # ⚠ projwfc.x 가 'Error in routine d_matrix (2)' 로 죽는다 — 대칭연산을
                 #   구면조화함수에 적용하는 회전행렬을 못 만든다. 표준 우회는 대칭 끄기.
                 ("    nosym           = .true." if nosym else ""),
                 # ★ Nd 4f³ 는 스핀분극 없이는 분수 점유가 되어 갭이 정의되지 않는다
                 #   (위 --nd_spin 주석 참조). 씨앗 모멘트를 Nd 종에만 준다.
                 ("    nspin           = 2" if spinpol else ""),
                 (f"    starting_magnetization({els.index('Nd') + 1}) = {a.nd_mag}"
                  if spinpol else ""),
                 # ⚠ QE 는 `occupations='fixed'` + `nspin=2` 조합에서 tot_magnetization 을
                 #   **요구한다**(없으면 read_namelists 에서 즉사). Nd³⁺ = 4f³ 이므로
                 #   홀전자 3개 × Nd 개수. 이 값이 곧 ↑/↓ 점유 밴드 수를 가른다.
                 (f"    tot_magnetization = {3 * n_nd}" if (spinpol and fixed) else ""),
                 ("    noinv           = .true." if nosym else ""),
                 occ.rstrip(), "/",
                 # ⚠⚠ DOS 용 nscf 만 문턱을 푼다 (2026-08-07 licl 04 단독 실패).
                 #   증상: `c_bands (1): too many bands are not converged` → MPI_ABORT.
                 #   원인: LiCl 은 갭 6.26 eV 짜리 이온결정이라 빈 전도대가 거의
                 #   자유전자꼴이고, nosym 으로 k 점이 전 BZ 로 늘어난 상태에서
                 #   conv_thr 1e-8(→ ethr ~1e-9)을 제일 위 밴드까지 요구하면 안 닫힌다.
                 #   ★ 여기서 문턱을 푸는 게 **정당한 이유**: 이 단계 산출은 DOS **모양**뿐이고
                 #     갭은 03 단계 고유값이 정본이다. DOS 의 degauss 0.007 Ry(≈0.095 eV)가
                 #     이미 1e-6 Ry 보다 다섯 자리 굵다 — 정밀도가 남아돈다.
                 #   ⛔ 03(갭) 단계는 **절대 안 푼다.** 그 값이 논문에 실린다.
                 "&ELECTRONS",
                 ("    conv_thr        = 1.0d-6" if dos else "    conv_thr        = 1.0d-8"),
                 # Davidson 부분공간을 키우면 잘 안 닫히는 밴드가 닫힌다(기본 2 → 4).
                 ("    diago_david_ndim = 4" if dos else ""),
                 "    mixing_beta     = 0.3", "    electron_maxstep = 200", "/"]
            if calc in ("relax", "vc-relax"):
                L += ["&IONS", "/"]
            if calc == "vc-relax":
                L += ["&CELL", "    cell_dofree     = 'all'", "/"]
            L = [x for x in L if x != ""]
            body = "\n".join(L) + "\n\nATOMIC_SPECIES\n"
            from ase.data import atomic_masses, atomic_numbers
            for e in els:
                body += f"  {e:3s} {atomic_masses[atomic_numbers[e]]:8.3f}  {pool[e]}\n"
            body += "\nCELL_PARAMETERS angstrom\n"
            for v in cell:
                body += "  %16.10f %16.10f %16.10f\n" % tuple(v)
            body += "\nATOMIC_POSITIONS angstrom\n"
            for s_, p in zip(at.get_chemical_symbols(), at.positions):
                body += f"  {s_:3s} %16.10f %16.10f %16.10f\n" % tuple(p)
            body += hub
            body += f"\nK_POINTS automatic\n  {kpts[0]} {kpts[1]} {kpts[2]} 0 0 0\n"
            return body + extra

        open(os.path.join(d, "01_vcrelax.in"), "w").write(block("vc-relax", k_scf, False))
        open(os.path.join(d, "02_scf.in"), "w").write(block("scf", k_scf, False))
        # ★ 갭의 정본 — fixed occupations + 조밀 k. nbnd 를 넉넉히 줘 CBM 을 잡는다
        open(os.path.join(d, "03_nscf_gap.in"), "w").write(
            block("nscf", k_nscf, True, verbose=True))
        k_dos = kmesh(cell, KDENS_DOS)
        open(os.path.join(d, "04_nscf_dos.in"), "w").write(
            block("nscf", k_dos, False, nosym=True, dos=True))
        open(os.path.join(d, "05_dos.in"), "w").write(
            f"&DOS\n  prefix = '{tag}'\n  outdir = './tmp'\n"
            f"  fildos = '{tag}.dos'\n  degauss = 0.007\n/\n")
        open(os.path.join(d, "06_projwfc.in"), "w").write(
            f"&PROJWFC\n  prefix = '{tag}'\n  outdir = './tmp'\n"
            f"  filpdos = '{tag}'\n  degauss = 0.007\n  ngauss = 0\n/\n")
        note = ""
        if has_nd:
            note = "  ⚠ Nd 4f 가 valence 다 — "
            if spinpol and a.nd_u > 0:
                note += (f"nspin=2 · M_tot={3 * n_nd} μB · U(Nd 4f)={a.nd_u} eV. "
                         "2026-08-07 이전 실행(스핀 없음·U 없음)의 −0.02 eV 는 "
                         "**분수 점유 인공물**이었다 — 이 설정이 그걸 고친다.")
            elif spinpol:
                note += f"nspin=2 · M_tot={3 * n_nd} μB, U 없음 → 갭 과소 가능."
            else:
                note += ("**스핀분극 없음** → 4f³ 가 분수 점유가 되어 갭이 정의되지 않는다. "
                         "이 설정의 갭은 인용 금지(진단용).")
        print(f"\n✓ {tag:26s} {nat:3d}원자 {'+'.join(els):14s} "
              f"k scf {k_scf} / gap {k_nscf} / dos {kmesh(cell, KDENS_DOS)} (nosym) · "
              f"전자 {nelec:.0f} → nbnd {nbnd} "
              + (f"(점유 ↑{int((nelec + 3*n_nd)/2)}/↓{int((nelec - 3*n_nd)/2)}, M={3*n_nd} μB)"
                 if spinpol else
                 f"(점유 {int(nelec/2)} + 빈 {nbnd - int(nelec/2)})"))
        if note:
            print(note)
        made.append(tag)

    print(f"\n생성 {len(made)}개 · 건너뜀 {len(skipped)}개 → {a.work}")
    print("\n실행:  bash tools/sei/run_sei_dft.sh")
    print("⚠ 갭은 03_nscf_gap 의 고유값으로만 낸다 — DOS 문턱 판독 금지.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
