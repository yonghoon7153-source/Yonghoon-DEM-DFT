#!/usr/bin/env python
"""generate_dft_inputs.py — generate QE pw.in files for Top-N MLIP winners.

UMA-s-1p1 is a general MLIP that has known bias for sulfide systems
(Wang 2025 npj Comp Mater reports PES softening / Li diffusivity over-
estimation). For paper-grade B0 / band gap / Bader / PDOS we need DFT
spot-checks on the top MLIP candidates.

This tool reads the final FINAL_RANKING.json (from combine_rankings.py)
and generates QE input files for the top N structures, using the same
template as our Nd-EOS pipeline (52-atom cell, ecutwfc=52 Ry, K=2×2×1).

Each top winner gets its own directory with:
  relax.in        — QE relax input (cell+positions, BFGS)
  pseudo_list.txt — required pseudopotentials for this structure

Then user scp's the directory to KISTI and runs sbatch.

Usage:
  python3 tools/doping/generate_dft_inputs.py \\
      --ranking runs/tier_.../FINAL_RANKING.json \\
      --top 10 \\
      --out runs/tier_.../dft_inputs/
"""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

from ase.io import read

sys.path.insert(0, str(Path(__file__).parent))
from _provenance import get_provenance


PSEUDO_DIR_KISTI = '/scratch/x3430a02/kgy/manuscript_support/pseudo'

# Element → mass + pseudopotential filename (matches Nd-EOS prepare script)
PSEUDOS = {
    'Li': ('6.9410',   'li_pbe_v1_4_uspp_F.UPF'),
    'P':  ('30.9740',  'P_pbe-n-rrkjus_psl_1_0_0.UPF'),
    'S':  ('32.0650',  's_pbe_v1_4_uspp_F.UPF'),
    'Cl': ('35.4530',  'cl_pbe_v1_4_uspp_F.UPF'),
    'Br': ('79.9040',  'br_pbe_v1.4.uspp.F.UPF'),
    'I':  ('126.9045', 'I.pbe-n-rrkjus_psl.0.2.UPF'),
    'F':  ('18.9984',  'F.pbe-n-kjpaw_psl.0.1.UPF'),
    'O':  ('15.9994',  'O.pbe-n-kjpaw_psl.0.1.UPF'),
    'N':  ('14.0067',  'N.pbe-n-rrkjus_psl.0.1.UPF'),
    # Cations
    'Nd': ('144.242',  'Nd.paw.z_14.atompaw.wentzcovitch.v1.2.upf'),
    'La': ('138.9055', 'La.paw.z_11.atompaw.wentzcovitch.v1.2.upf'),
    'Sm': ('150.36',   'Sm.paw.z_14.atompaw.wentzcovitch.v1.2.upf'),
    'Y':  ('88.9059',  'Y.pbe-spn-kjpaw_psl.1.0.0.UPF'),
    'Sc': ('44.9559',  'Sc.pbe-spn-kjpaw_psl.0.2.3.UPF'),
    'Al': ('26.9815',  'Al.pbe-n-kjpaw_psl.1.0.0.UPF'),
    'Mg': ('24.3050',  'Mg.pbe-n-kjpaw_psl.0.3.0.UPF'),
    'Zn': ('65.38',    'Zn.pbe-dnl-kjpaw_psl.1.0.0.UPF'),
    'Ca': ('40.0780',  'Ca.pbe-spn-kjpaw_psl.1.0.0.UPF'),
    'Sr': ('87.62',    'Sr.pbe-spn-kjpaw_psl.1.0.0.UPF'),
    'Ba': ('137.327',  'Ba.pbe-spn-kjpaw_psl.1.0.0.UPF'),
    'Cu': ('63.546',   'Cu.pbe-dn-kjpaw_psl.1.0.0.UPF'),
    'Ag': ('107.868',  'Ag.pbe-n-kjpaw_psl.1.0.0.UPF'),
    'Ti': ('47.867',   'Ti.pbe-spn-kjpaw_psl.1.0.0.UPF'),
    'Zr': ('91.224',   'Zr.pbe-spn-kjpaw_psl.1.0.0.UPF'),
    'Hf': ('178.49',   'Hf.pbe-spn-kjpaw_psl.1.0.0.UPF'),
    'Si': ('28.0855',  'Si.pbe-n-kjpaw_psl.1.0.0.UPF'),
    'Ge': ('72.63',    'Ge.pbe-dn-kjpaw_psl.1.0.0.UPF'),
    'Sn': ('118.710',  'Sn.pbe-dn-kjpaw_psl.1.0.0.UPF'),
    'Sb': ('121.76',   'Sb.pbe-n-kjpaw_psl.1.0.0.UPF'),
    'Bi': ('208.98',   'Bi.pbe-dn-kjpaw_psl.1.0.0.UPF'),
    'B':  ('10.811',   'B.pbe-n-kjpaw_psl.1.0.0.UPF'),
    'V':  ('50.9415',  'V.pbe-spnl-kjpaw_psl.1.0.0.UPF'),
    'Nb': ('92.9064',  'Nb.pbe-spn-kjpaw_psl.1.0.0.UPF'),
    'Ta': ('180.9479', 'Ta.pbe-spn-kjpaw_psl.1.0.0.UPF'),
    'W':  ('183.84',   'W.pbe-spn-kjpaw_psl.1.0.0.UPF'),
    'Mo': ('95.95',    'Mo.pbe-spn-kjpaw_psl.1.0.0.UPF'),
    'Cr': ('51.9961',  'Cr.pbe-spn-kjpaw_psl.1.0.0.UPF'),
    'Mn': ('54.9380',  'Mn.pbe-spn-kjpaw_psl.0.3.1.UPF'),
    'Fe': ('55.845',   'Fe.pbe-spn-kjpaw_psl.0.2.1.UPF'),
    'Co': ('58.9332',  'Co.pbe-spn-kjpaw_psl.0.3.1.UPF'),
    'Ni': ('58.6934',  'Ni.pbe-spn-kjpaw_psl.1.0.0.UPF'),
}


def generate_pwin(atoms, prefix: str, ecutwfc=52, ecutrho=520,
                 kpoints='2 2 1', pseudo_dir=None, pp_names=None,
                 calculation='relax', nosym=True, occupations='smearing',
                 conv_thr='1.0d-8', nspin=1, start_mag=None, hubbard=None,
                 tot_magnetization=None, mixing_mode='plain', mixing_beta=0.2,
                 electron_maxstep=100, mixing_ndim=8, smearing='mv',
                 degauss=0.01) -> str:
    """⚠ 2026-09-08 — `occupations`/gamma k-점을 열었다 (힘 대조 카드 §4).
    금속용 smearing 을 절연체 단일점에 그대로 쓰면 힘에 smearing 항이 섞인다.
    `kpoints='gamma'` 를 주면 `K_POINTS gamma` 를 쓴다 (automatic 1 1 1 과 다르다 —
    gamma 전용 코드경로가 절반의 비용으로 같은 답을 낸다)."""
    # ⛔ pseudo_dir 를 KISTI 로 박아두면 다른 머신에서 pw.x 가 조용히 죽는다
    #   (gabia 는 /data/work/pseudo). 호출부가 줄 수 있게 열어둔다.
    species = sorted(set(atoms.get_chemical_symbols()))
    ntyp = len(species)
    nat = len(atoms)
    cell = atoms.cell.array
    frac = atoms.get_scaled_positions()
    syms = atoms.get_chemical_symbols()

    missing = [s for s in species if s not in PSEUDOS]
    if missing:
        raise ValueError(f"Missing pseudopotentials for {missing}; add to PSEUDOS")

    lines = []
    lines.append("&CONTROL")
    lines.append(f"    calculation = '{calculation}'")
    lines.append(f"    prefix      = '{prefix}'")
    lines.append("    outdir      = './tmp'")
    lines.append(f"    pseudo_dir  = '{pseudo_dir or PSEUDO_DIR_KISTI}'")
    lines.append("    tprnfor     = .true.")
    lines.append("    tstress     = .true.")
    lines.append("    etot_conv_thr = 1.0d-6")
    lines.append("    forc_conv_thr = 1.0d-4")
    lines.append("    nstep        = 200")
    lines.append("/")
    lines.append("&SYSTEM")
    lines.append("    ibrav       = 0")
    lines.append(f"    nat         = {nat}")
    lines.append(f"    ntyp        = {ntyp}")
    lines.append(f"    ecutwfc     = {ecutwfc}")
    lines.append(f"    ecutrho     = {ecutrho}")
    lines.append(f"    occupations = '{occupations}'")
    if occupations == 'smearing':
        lines.append(f"    smearing    = '{smearing}'")
        lines.append(f"    degauss     = {degauss}")
    lines.append(f"    nosym       = .{str(bool(nosym)).lower()}.")
    # ── 스핀·U (2026-09-08 · Nd O-모티프 순위 재채점) ─────────────────────────
    #   ⚠ Nd³⁺ = 4f³ 이다. z≈14 PP(4f 원자가)를 쓰면서 nspin=1 로 두면 전자 3개가
    #     7겹 f 다중항에 **분수 점유**로 퍼져 계가 인공적으로 금속이 된다 (2026-08-07 실측:
    #     화학이 다른 세 상의 갭이 −0.021/−0.022/−0.028 eV 로 7 meV 안에 몰렸다).
    #   ⛔ 그리고 **씨앗 자화를 계마다 다르게 주면 총에너지 차가 무의미해진다** —
    #     비교하는 두 구조가 다른 f 점유로 수렴할 수 있다 (SDCP wave1 교훈).
    #     그래서 이 함수는 값을 정하지 않고 호출부가 준 것을 그대로 찍는다.
    if int(nspin) == 2:
        lines.append("    nspin       = 2")
        for el, m in sorted((start_mag or {}).items()):
            i = species.index(el) + 1              # ATOMIC_SPECIES 순서 = 아래 정렬과 같다
            lines.append(f"    starting_magnetization({i}) = {float(m)}")
        if tot_magnetization is not None:
            lines.append(f"    tot_magnetization = {float(tot_magnetization)}")
    lines.append("/")
    lines.append("&ELECTRONS")
    lines.append(f"    conv_thr     = {conv_thr}")
    # ⛔ 2026-09-08 실측 — 힘 대조 첫 점(b2o3 128원자, 700 K 스냅샷)이 **100회 만에 잘렸다**.
    #   정확도가 줄다 멈춘 게 아니라 **진동**했다 (0.0274 → 0.0305 → 0.0487 → 0.0431 Ry) —
    #   큰 무질서 셀의 전형적인 charge sloshing 이다. plain Broyden 은 이 계에서 안 잡힌다.
    #   ⛔⛔ 그런데 `local-TF` 로 바꿨더니 **더 나빠졌다** — 1회부터 48,000 Ry,
    #     `negative rho 5.9E+02`(정상은 1e-4~1e-2). 시작 밀도가 4.4% 모자란 상태에서
    #     국소 TF 스크리닝이 비물리적 밀도를 만들었다. **이 계에는 쓰지 않는다.**
    #     진동의 처방은 `mixing_beta` 를 낮추고 `mixing_ndim`(Broyden 이력)을 늘리는 것,
    #     그리고 여유 밴드가 없는 `occupations='fixed'` 를 smearing 으로 푸는 것이다.
    #   ⚠ 이 설정은 **비교하는 전 점이 같아야** 한다 — 점마다 다르면 계 간 비교가 아니라
    #     설정 간 비교가 된다. 그래서 값을 여기서 정하지 않고 호출부가 준 것을 찍는다.
    lines.append(f"    electron_maxstep = {int(electron_maxstep)}")
    lines.append(f"    mixing_mode  = '{mixing_mode}'")
    lines.append(f"    mixing_beta  = {mixing_beta}")
    lines.append(f"    mixing_ndim  = {int(mixing_ndim)}")
    lines.append("    diagonalization = 'david'")
    lines.append("/")
    if calculation != 'scf':
        lines.append("&IONS")
        lines.append("    ion_dynamics = 'bfgs'")
        lines.append("/")
        lines.append("&CELL")
        lines.append("    cell_dynamics = 'bfgs'")
        lines.append("    press_conv_thr = 0.5")
        lines.append("/")
    lines.append("ATOMIC_SPECIES")
    for s in species:
        mass, ppf = PSEUDOS[s]
        # pp_names 로 실제 머신의 파일명을 덮어쓴다 (같은 pseudo 라도 구두점이 다르다)
        ppf = (pp_names or {}).get(s, ppf)
        lines.append(f"  {s}  {mass}  {ppf}")
    lines.append("CELL_PARAMETERS angstrom")
    for row in cell:
        lines.append(f"  {row[0]:14.10f}  {row[1]:14.10f}  {row[2]:14.10f}")
    lines.append("ATOMIC_POSITIONS crystal")
    for sym, fr in zip(syms, frac):
        lines.append(f"  {sym}  {fr[0]:14.10f}  {fr[1]:14.10f}  {fr[2]:14.10f}")
    if str(kpoints).strip().lower() == 'gamma':
        lines.append("K_POINTS gamma")
    else:
        lines.append("K_POINTS automatic")
        lines.append(f"  {kpoints} 0 0 0")
    # ⛔ 원자가에 없는 껍질에 U 를 걸면 QE 가 죽거나 **조용히 무시**한다 (2026-08-29 실측:
    #   frozen-4f PP 인데 `HUBBARD U Nd-4f 6.0` 을 찍고 있었다). 여기서는 호출부가 준
    #   목록을 그대로 찍되, 판별은 호출부 몫이다 — 이 함수는 PP 의 z_valence 를 모른다.
    #   형식은 tools/sei/build_dft_inputs.py 와 **같아야 한다** (갈라지면 두 트랙이 어긋난다).
    if hubbard:
        lines.append("HUBBARD (ortho-atomic)")
        for man in hubbard:
            lines.append(f"  U {man}")
    return "\n".join(lines) + "\n"


# ══════════════════════════════════════════════════════════════════════════
# 궤적 스냅샷 → DFT 단일점 (2026-09-08 · b2o3 UMA-vs-DFT 힘 대조 카드 §4)
#   카드: db/properties/b2o3_uma_vs_dft_force_prereg_2026_09_08.json (ratified 2판)
#
#   왜 여기에 붙였나 — `generate_pwin()` 이 이미 52/520 USPP 레시피와 `pp_names`
#   머신별 덮어쓰기를 갖고 있다. 새 파일을 만들면 그 레시피가 두 곳으로 갈라진다.
#
#   ⛔ 이 경로가 **못 하는 것**
#     · 표본을 고르지 않는다 — 프레임 번호는 카드의 결정적 규칙(시각→index)이 정한다.
#     · UMA 힘을 계산하지 않는다. 같은 `frame.xyz` 를 쓰라고 내보낼 뿐이다.
#     · pw.x 를 돌리지 않는다. 입력과 대조용 해시만 만든다.
#     · 유사포텐셜이 **물리적으로 맞는지**는 모른다 — 존재와 해시만 본다.
#: 카드 §4 가 못박은 파일명 (kgy /home/kgy/work/pseudo 실물 기준 · 구두점이 PSEUDOS 와 다르다)
PP_USPP_52_520 = {
    'Li': 'li_pbe_v1.4.uspp.F.UPF',
    'P':  'P.pbe-n-rrkjus_psl.1.0.0.UPF',
    'S':  's_pbe_v1.4.uspp.F.UPF',
    'Cl': 'cl_pbe_v1.4.uspp.F.UPF',
    'O':  'O.pbe-n-kjpaw_psl.0.1.UPF',
    'B':  'B.pbe-n-kjpaw_psl.1.0.0.UPF',
}


def frame_index_for_time(t_ps, save_fs):
    """카드의 결정적 규칙: index = round(t[ps] * 1000 / save_fs), 0-기준.

    ⚠ **half-up 반올림을 명시한다.** 파이썬 내장 `round` 는 은행가 반올림이라
      `round(0.5) == 0` 이다 — 표본 index 가 이런 규칙에 걸리면 재현 시 사람이
      다른 답을 낸다. 카드의 시각(10·20·30·40·50 ps)은 정확히 떨어져 이 분기를
      타지 않지만, 규칙은 문서와 코드가 같아야 하므로 여기서 고정한다.
    ⛔ 사람이 프레임을 고르는 경로를 두지 않는다 (§8 무효 조건)."""
    import math as _m
    if save_fs <= 0:
        raise ValueError("save_fs 는 양수여야 한다")
    return int(_m.floor(float(t_ps) * 1000.0 / float(save_fs) + 0.5))


def coord_digest(atoms):
    """좌표·격자의 sha256 — QE 입력과 UMA 입력이 **같은 배치**인지 기계로 대조한다.

    소수 10자리로 고정한다. 그 **아래**(1e-11 이하)는 xyz 왕복에서 살아남지 않으므로
    비교 기준이 못 된다. 1e-10 은 10자리에 그대로 보이므로 다른 배치로 센다."""
    import hashlib as _h
    parts = []
    for row in atoms.cell.array:
        parts.append(" ".join(f"{v:.10f}" for v in row))
    for sym, pos in zip(atoms.get_chemical_symbols(), atoms.get_positions()):
        parts.append(f"{sym} " + " ".join(f"{v:.10f}" for v in pos))
    return _h.sha256("\n".join(parts).encode()).hexdigest()


def preflight_pseudos(species, pseudo_dir, pp_names=None):
    """유사포텐셜 존재·해시. 하나라도 없으면 **거부**한다 (조용히 빠지면 pw.x 가 나중에 죽는다)."""
    import hashlib as _h
    pp = dict(PP_USPP_52_520)
    pp.update(pp_names or {})
    out, missing = {}, []
    for el in sorted(set(species)):
        name = pp.get(el)
        if not name:
            missing.append(f"{el}(파일명 미정)")
            continue
        f = Path(pseudo_dir) / name
        if not f.is_file():
            missing.append(f"{el}:{name}")
            continue
        out[el] = {"file": name,
                   "sha256": _h.sha256(f.read_bytes()).hexdigest()}
    if missing:
        raise FileNotFoundError("유사포텐셜 없음 — " + " · ".join(missing)
                                + f"  (pseudo_dir={pseudo_dir})")
    return out


def snapshots_from_traj(traj, times_ps, save_fs, out_dir, label, seed,
                        pseudo_dir, ecutwfc=52, ecutrho=520, pp_names=None,
                        mixing_mode='plain', mixing_beta=0.2, electron_maxstep=100,
                        mixing_ndim=8, occupations=None, smearing='gaussian', degauss=0.01):
    """궤적에서 카드 규칙대로 프레임을 뽑아 frame.xyz + scf.in + 대조 해시를 쓴다.

    ⛔ 2026-09-14 — 기본 smearing 이 **`mv`(cold)였다.** 형제 함수 `scf_from_xyz` 는
      2026-09-11 에 `gaussian` 으로 고쳤는데 이쪽은 안 고쳐서, CLI(`--smearing gaussian`)로
      부르면 안전하고 **함수를 직접 부르면 위험한** 상태였다. 뜨거운 황화물 MD 스냅샷에서
      `mv` 는 음의 점유를 허용해 SCF 를 무너뜨린다 (실측 118,698 Ry 발산, `runs/fc_pilot`).
      두 경로의 기본값을 맞춘다. 자체시험이 CLI 기본값과 함수 기본값의 일치를 강제한다.

    ⚠ `occupations=None` → **`fixed`** 다. 절연체로 **선언된** 구조에만 맞다. 융체·고온
      스냅샷처럼 갭이 닫힐 수 있는 프레임에는 호출부가 `occupations='smearing'` 을 줘야 한다
      — 이 함수는 온도를 모르므로 대신 판단하지 않는다."""
    from ase.io import read as _read, write as _write
    out_dir = Path(out_dir)
    idxs = [frame_index_for_time(t, save_fs) for t in times_ps]
    frames = _read(str(traj), index=':')
    n = len(frames)
    bad = [(t, i) for t, i in zip(times_ps, idxs) if i >= n or i < 0]
    if bad:
        raise IndexError(f"궤적 프레임 {n}개인데 필요한 index {bad} 가 범위 밖이다 "
                         "— 창 밖 표본을 조용히 대체하지 않는다 (카드 §8)")
    pseudos = preflight_pseudos(frames[0].get_chemical_symbols(), pseudo_dir, pp_names)
    pp = dict(PP_USPP_52_520); pp.update(pp_names or {})
    recs = []
    for t, i in zip(times_ps, idxs):
        a = frames[i]
        tag = f"{label}_{seed}_t{int(round(float(t)))}ps"
        w = out_dir / tag
        w.mkdir(parents=True, exist_ok=True)
        _write(str(w / "frame.xyz"), a, format="extxyz")
        (w / "scf.in").write_text(generate_pwin(
            a, tag, ecutwfc, ecutrho, kpoints='gamma', pseudo_dir=pseudo_dir,
            pp_names=pp, calculation='scf', nosym=True,
            occupations=(occupations or 'fixed'),
            mixing_mode=mixing_mode, mixing_beta=mixing_beta,
            electron_maxstep=electron_maxstep, mixing_ndim=mixing_ndim,
            smearing=smearing, degauss=degauss))
        recs.append({"tag": tag, "time_ps": float(t), "frame_index": i,
                     "n_atoms": len(a), "coord_sha256": coord_digest(a),
                     "cell": [[float(x) for x in r] for r in a.cell.array],
                     "path": str(w)})
    man = {"card": "db/properties/b2o3_uma_vs_dft_force_prereg_2026_09_08.json",
           "scf_settings": {"mixing_mode": mixing_mode, "mixing_beta": mixing_beta,
                            "electron_maxstep": electron_maxstep,
                            "occupations": (occupations or "fixed"), "mixing_ndim": mixing_ndim,
                            "smearing": smearing, "degauss": degauss, "kpoints": "gamma",
                            "⚠": "전 점이 같아야 한다 — 다르면 계 간 비교가 아니라 설정 간 비교다"},
           "label": label, "seed": seed, "traj": str(traj),
           "n_frames_in_traj": n, "save_fs": float(save_fs),
           "규칙": "index = round(t_ps*1000/save_fs), 0-기준 — 사람이 고르지 않는다",
           "dft": {"code": "QE 7.4.1", "calculation": "scf", "kpoints": "gamma",
                   "occupations": "fixed", "ecutwfc": ecutwfc, "ecutrho": ecutrho,
                   "conv_thr": "1.0d-8", "tprnfor": True, "nosym": True},
           "pseudos": pseudos, "snapshots": recs,
           "⛔_이_파일이_보증하지_않는_것": "pw.x 수렴 · UMA 힘 계산 · 유사포텐셜의 물리적 적합성"}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"SNAPSHOTS_{label}_{seed}.json").write_text(
        json.dumps(man, ensure_ascii=False, indent=1))
    return man


# ── 회수: pw.x 출력 → DFT 라벨 붙은 extxyz (2026-09-08) ────────────────────
#   왜 여기인가 — 이 폴더 구조(<label>_<seed>_t<NN>ps/{frame.xyz,scf.in,scf.out})와
#   SNAPSHOTS json 을 만든 것이 이 도구다. 구조를 아는 쪽이 회수도 해야 갈라지지 않는다.
#   힘 **대조** 는 여기서 하지 않는다 — mlip_committee.py bench 가 그 일을 한다.
RY_TO_EV = 13.605693122994
RY_AU_TO_EV_A = RY_TO_EV / 0.529177210903        # Ry/bohr → eV/Å


def parse_pw_out(text):
    """pw.x scf 출력에서 (energy_eV, forces_eV_per_A, flags). 실패는 예외로 낸다.

    ⛔ 못 하는 것: 수렴의 **물리적** 타당성을 보지 않는다. 문자열이 있는지만 본다.
    ⚠ 자체 파서를 쓰는 이유 — ase 의 espresso-out 리더는 버전마다 요구 블록이 달라
      합성 시험을 만들기 어렵다. 우리가 읽는 세 블록은 QE 출력 형식에서 안정적이다.
    """
    import re as _re
    conv = "convergence has been achieved" in text
    done = "JOB DONE" in text
    # ⛔⛔ 2026-09-11 (회신 BJ2 P0-3b) — 옛 판은 에너지를 `findall[-1]`(**마지막**), 힘을
    #   `search`(**첫 번째**) 로 잡았다. 완결 SCF 두 개가 한 파일에 이어 붙으면
    #   **B 의 에너지와 A 의 힘이 한 레코드로** 나오고 converged·job_done 은 둘 다 True 였다.
    #   (BJ2 재현: A −100 Ry/F 0.01 + B −200 Ry/F 0.09 → E=B, F=A, 플래그 전부 참.)
    #   회수물이 실제로 오염됐다는 증거는 없다 — 결함은 **탐지 장치가 없다**는 것이다.
    #   ⇒ 실행 경계를 세어 **둘 이상이면 멈춘다.** 조용히 섞지 않는다.
    _starts = len(_re.findall(r"Program PWSCF .*? starts on", text)) or \
              len(_re.findall(r"^\s*Program PWSCF", text, _re.M))
    _dones = text.count("JOB DONE")
    if _starts > 1 or _dones > 1:
        raise ValueError(
            f"한 파일에 pw.x 실행이 여러 번 들어 있다 (시작 {_starts}회 · JOB DONE {_dones}회) — "
            "에너지와 힘이 서로 다른 실행에서 올 수 있어 **읽지 않는다**. "
            "이어붙인 출력을 실행별로 가르거나 다시 돌려라 (회신 BJ2 P0-3b)")
    m = _re.findall(r"^!\s+total energy\s+=\s+([-\d.]+)\s+Ry", text, _re.M)
    if not m:
        raise ValueError("총에너지 줄(`!    total energy`)이 없다 — scf 가 안 끝났다")
    energy = float(m[-1]) * RY_TO_EV
    _fbs = _re.findall(r"Forces acting on atoms.*?\n(.*?)\n\s*\n", text, _re.S)
    if len(_fbs) > 1:
        raise ValueError(
            f"힘 블록이 {len(_fbs)}개다 — 한 SCF 의 출력이 아니다. 에너지(마지막)와 힘(첫째)이 "
            "다른 곳에서 올 수 있어 읽지 않는다 (회신 BJ2 P0-3b)")
    fb = _re.search(r"Forces acting on atoms.*?\n(.*?)\n\s*\n", text, _re.S)
    if not fb:
        raise ValueError("힘 블록(`Forces acting on atoms`)이 없다 — tprnfor 를 확인하라")
    F = []
    for ln in fb.group(1).splitlines():
        g = _re.match(r"\s*atom\s+(\d+)\s+type\s+\d+\s+force\s*=\s*"
                      r"([-\d.Ee+]+)\s+([-\d.Ee+]+)\s+([-\d.Ee+]+)", ln)
        if g:
            F.append([float(g.group(2)) * RY_AU_TO_EV_A,
                      float(g.group(3)) * RY_AU_TO_EV_A,
                      float(g.group(4)) * RY_AU_TO_EV_A])
    if not F:
        raise ValueError("힘 블록은 있는데 `atom N type M force =` 줄을 하나도 못 읽었다")
    return energy, F, {"converged": conv, "job_done": done}


def parse_pw_stress(text):
    """pw.x 출력의 **전체 응력텐서** (3×3, GPa, QE 부호: 압축 +). `tstress=.true.` 가 없으면 예외.

    QE 형식:  `     total   stress  (Ry/bohr**3)                   (kbar)     P=  -12.34`
              이어서 3줄 × 6열 (앞 3 = Ry/bohr³, 뒤 3 = kbar). kbar 열을 읽어 /10 → GPa.
    ⛔ 못 하는 것: 응력의 물리적 타당성은 보지 않는다. 한 파일에 응력 블록이 둘 이상이면
      (실행이 이어 붙음) **읽지 않는다** — parse_pw_out 과 같은 규율(회신 BJ2 P0-3b).
    """
    import re as _re
    blocks = list(_re.finditer(r"total\s+stress\s+\(Ry/bohr\*\*3\)\s+\(kbar\)\s+P=\s*([-\d.Ee+]+)\s*\n"
                                r"((?:.*\n){3})", text))
    if not blocks:
        raise ValueError("응력 블록(`total   stress`)이 없다 — tstress=.true. 를 확인하라")
    if len(blocks) > 1:
        raise ValueError(f"응력 블록이 {len(blocks)}개다 — 한 SCF 의 출력이 아니다. 읽지 않는다")
    P_kbar = float(blocks[0].group(1))
    rows = []
    for ln in blocks[0].group(2).splitlines():
        nums = [float(x) for x in _re.findall(r"[-\d.]+(?:[Ee][-+]?\d+)?", ln)]
        if len(nums) < 6:
            raise ValueError(f"응력 행을 못 읽었다: {ln!r}")
        rows.append([v / 10.0 for v in nums[3:6]])     # kbar → GPa
    return {"sigma_GPa": rows, "P_GPa": P_kbar / 10.0}


# comp1 정본 DFT 설정 (tools/electronic/standard_dos/comp1/comp1_scf.in · eos.json k444) —
# 정적대조는 **이 설정으로만** 돈다. 생성기 기본값(52/520/2×2×1)을 쓰면 '같은 설정' 이 아니다.
COMP1_DFT = {"ecutwfc": 60, "ecutrho": 480, "kpoints": "4 4 4", "occupations": "smearing",
             "smearing": "mv", "degauss": 0.01, "conv_thr": "1.0d-9", "mixing_beta": 0.3,
             "mixing_mode": "plain", "nosym": True, "calculation": "scf",
             "pp_names": {"Li": "li_pbe_v1_4_uspp_F.UPF", "P": "P_pbe-n-rrkjus_psl_1_0_0.UPF",
                          "S": "s_pbe_v1_4_uspp_F.UPF", "Cl": "cl_pbe_v1_4_uspp_F.UPF"}}

STATIC_PAIR_ALARM = {"force_rmse_eV_A_per_atom_vector": 0.05, "stress_component_GPa": 0.3,
                     "⚠": "진단 **경보선**이지 Ea/B 정확도 보증이 아니다 (회신 BO Q2). "
                          "basin 판정 없음 — 에너지 높낮이로 최소점을 확정하지 않는다"}


def static_pair(a_path, b_path, out_dir, pseudo_dir, settings=None, alarm=None):
    """정적대조 (카드 v3 §5): 같은 조성의 두 **고정 기하** (a)(b) 에 **같은 DFT 설정**으로
    scf 입력을 만든다. `<out>/a/scf.in` · `<out>/b/scf.in` · `manifest.json`(기하 sha256·설정·경보선).

    ⛔ 못 하는 것: 돌리지 않는다. UMA 쪽은 gabia 블록이 따로 낸다(uma_ab.json).
    ⛔ 거부: 두 기하의 조성이 다르면 '같은 조성의 상수 오프셋 제거'(δΔE)가 성립 안 해 만들지 않는다.
    """
    import hashlib as _h
    from ase.io import read as _read
    from collections import Counter as _C
    st = dict(COMP1_DFT); st.update(settings or {})
    al = dict(STATIC_PAIR_ALARM); al.update(alarm or {})
    A, B = _read(str(a_path)), _read(str(b_path))
    ca, cb = _C(A.get_chemical_symbols()), _C(B.get_chemical_symbols())
    if ca != cb:
        raise ValueError(f"⛔ (a)(b) 조성이 다르다 {dict(ca)} vs {dict(cb)} — δΔE 가 정의되지 않는다")
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    man = {"provenance": get_provenance(), "created": _dt_now(), "kind": "static_pair",
           "settings": {k: v for k, v in st.items() if k != "pp_names"}, "pp_names": st["pp_names"],
           "alarm": al, "cells": []}
    for tag, pth, at in (("a", a_path, A), ("b", b_path, B)):
        d = out / tag; d.mkdir(exist_ok=True)
        txt = generate_pwin(at, f"sp_{tag}", ecutwfc=st["ecutwfc"], ecutrho=st["ecutrho"],
                            kpoints=st["kpoints"], pseudo_dir=pseudo_dir, pp_names=st["pp_names"],
                            calculation="scf", nosym=st["nosym"], occupations=st["occupations"],
                            conv_thr=st["conv_thr"], mixing_mode=st["mixing_mode"],
                            mixing_beta=st["mixing_beta"], smearing=st["smearing"], degauss=st["degauss"])
        assert "tstress     = .true." in txt and "tprnfor     = .true." in txt
        (d / "scf.in").write_text(txt)
        man["cells"].append({"tag": tag, "source": str(pth),
                             "source_sha256": _h.sha256(Path(pth).read_bytes()).hexdigest(),
                             "scf_in_sha256": _h.sha256(txt.encode()).hexdigest(),
                             "n_atoms": len(at), "composition": dict(ca),
                             "V_per_atom": float(at.get_volume() / len(at))})
    (out / "manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=1))
    return man


def compare_static_pair(out_dir, uma_json):
    """(a)(b) 의 DFT scf.out 과 UMA 단일점(uma_ab.json) 을 대조해 카드 v3 §5 보고 항목을 낸다.

      δΔE   = [E_U(b) − E_U(a)] − [E_D(b) − E_D(a)]   (meV/atom)
      힘     RMSE **원자별 벡터** 기준(성분 기준과 √3 차 명시) · 원소별 · 최대 원자
      응력   성분별 |Δσ| · (b) 의 DFT 응력 크기
    ⛔ 하지 않는 판정: basin 확정 · 최소점 존재 · UMA 일반 편향. 숫자만 낸다.
    """
    import numpy as _np
    from ase.io import read as _read
    out = Path(out_dir); U = json.loads(Path(uma_json).read_text())["uma_singlepoint"]
    rep = {"alarm": STATIC_PAIR_ALARM, "cells": {}}
    ED = {}
    for tag in ("a", "b"):
        txt = (out / tag / "scf.out").read_text(errors="replace")
        E, F, fl = parse_pw_out(txt)
        try:
            S = parse_pw_stress(txt); stress_ok = True
        except ValueError as e:
            S = {"sigma_GPa": None, "P_GPa": None, "error": str(e)}; stress_ok = False
        Fd = _np.asarray(F); Fu = _np.asarray(U[tag]["F_eV_A"])
        _, syms, _ = parse_pw_in_positions((out / tag / "scf.in").read_text())
        dF = Fu - Fd
        per_atom = _np.linalg.norm(dF, axis=1)
        rmse_vec = float(_np.sqrt((per_atom ** 2).mean()))
        rmse_comp = float(_np.sqrt((dF ** 2).mean()))
        by_el = {el: float(_np.sqrt((per_atom[[i for i, s in enumerate(syms) if s == el]] ** 2).mean()))
                 for el in sorted(set(syms))}
        imax = int(per_atom.argmax())

        # ⭐ 회신 BO / 카드 §5 — 차이(dF)만으로는 카드가 묻는 것을 못 답한다.
        #   카드 §5 판정문: *"(b) 의 **DFT** 힘·응력이 크면 '이 구성은 DFT 정상점 아님',
        #   작으면 '정상점 후보' 까지"*. 그러려면 **각 방법이 자기 기하에서 느끼는 힘**이
        #   있어야 하는데 종전 출력에는 없었다 (2026-09-13 실측: dF 만 보고 F_DFT≈0 을
        #   **추론**해야 했다 — 추론이 맞았더라도 도구가 답한 것은 아니다).
        #   ⛔ 여기에 합격/불합격 문턱을 만들지 않는다. 카드가 수치 문턱을 안 줬으므로
        #     비교 기준척도(=이 계를 만든 relax 의 forc_conv_thr)만 같이 적고 판정은 사람이 한다.
        def _fstats(arr):
            m = _np.linalg.norm(_np.asarray(arr), axis=1)
            j = int(m.argmax())
            return {"rmse_eV_A": float(_np.sqrt((m ** 2).mean())),
                    "max_atom": {"index": j, "element": syms[j], "F_eV_A": float(m[j])},
                    "by_element": {el: float(_np.sqrt((m[[i for i, s in enumerate(syms) if s == el]] ** 2).mean()))
                                   for el in sorted(set(syms))}}
        force_self = {"DFT": _fstats(Fd), "UMA": _fstats(Fu),
                      "기준척도_eV_A": {"forc_conv_thr_1e-3_Ry_bohr": 0.02571,
                                        "⚠": "comp1 계열 relax 의 수렴문턱을 Å 단위로 옮긴 값. **합격선이 아니다** — 카드 §5 는 수치 문턱을 주지 않았고, '크다/작다' 판정은 1저자가 한다"},
                      "⛔": "자기 힘이 작다 == 그 방법의 최소점이다 라고 읽지 않는다. 정상점 **후보**까지다 (카드 §5)"}

        n = len(F); ED[tag] = E / n
        cell = {"n_atoms": n, "E_DFT_eV_per_atom": E / n, "E_UMA_eV_per_atom": U[tag]["E_per_atom_eV"],
                "converged": fl["converged"], "job_done": fl["job_done"], "stress_ok": stress_ok,
                "force": {"rmse_per_atom_vector_eV_A": rmse_vec, "rmse_per_component_eV_A": rmse_comp,
                          "note": "벡터 RMSE ≈ √3 × 성분 RMSE", "by_element": by_el,
                          "max_atom": {"index": imax, "element": syms[imax], "dF_eV_A": float(per_atom[imax])},
                          "alarm_exceeded": rmse_vec > STATIC_PAIR_ALARM["force_rmse_eV_A_per_atom_vector"]},
                "force_self": force_self,
                "stress": None}
        if stress_ok:
            sd = _np.asarray(S["sigma_GPa"]); su = _np.asarray(U[tag]["stress_voigt_GPa"])
            su3 = _np.array([[su[0], su[5], su[4]], [su[5], su[1], su[3]], [su[4], su[3], su[2]]])
            dS = _np.abs(su3 - sd)
            cell["stress"] = {"DFT_GPa": sd.tolist(), "UMA_GPa": su3.tolist(), "P_DFT_GPa": S["P_GPa"],
                              "max_component_diff_GPa": float(dS.max()),
                              "DFT_max_abs_component_GPa": float(_np.abs(sd).max()),
                              "alarm_exceeded": float(dS.max()) > STATIC_PAIR_ALARM["stress_component_GPa"]}
        rep["cells"][tag] = cell
    if "a" in ED and "b" in ED:
        dU = U["b"]["E_per_atom_eV"] - U["a"]["E_per_atom_eV"]; dD = ED["b"] - ED["a"]
        rep["delta"] = {"dE_UMA_b_minus_a_meV_atom": 1e3 * dU, "dE_DFT_b_minus_a_meV_atom": 1e3 * dD,
                        "delta_delta_E_meV_atom": 1e3 * (dU - dD),
                        "⛔": "부호·10–30 meV 구간 전부 보고. basin 판정에 쓰지 않는다"}
    (out / "compare.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1))
    return rep


def parse_pw_in_positions(text):
    """scf.in 의 CELL_PARAMETERS(angstrom) + ATOMIC_POSITIONS(crystal) → (cell, symbols, cart)."""
    import re as _re
    cm = _re.search(r"CELL_PARAMETERS angstrom\n((?:\s*[-\d.Ee+]+\s+[-\d.Ee+]+\s+[-\d.Ee+]+\n){3})", text)
    pm = _re.search(r"ATOMIC_POSITIONS crystal\n((?:.*\n)+?)(?=K_POINTS|\Z)", text)
    if not (cm and pm):
        raise ValueError("scf.in 에서 CELL_PARAMETERS/ATOMIC_POSITIONS 를 못 읽었다")
    cell = [[float(x) for x in ln.split()] for ln in cm.group(1).strip().splitlines()]
    syms, frac = [], []
    for ln in pm.group(1).splitlines():
        t = ln.split()
        if len(t) == 4:
            syms.append(t[0]); frac.append([float(x) for x in t[1:]])
    cart = [[sum(frac[i][k] * cell[k][j] for k in range(3)) for j in range(3)]
            for i in range(len(frac))]
    return cell, syms, cart


def collect_results(out_dir, label, seed, max_dev_A=1e-6):
    """<out_dir> 의 이 (label, seed) 점들을 회수해 DFT 라벨 extxyz + RESULTS json 을 쓴다.

    ⛔ 실패한 점을 **빼고 진행하지 않는다** — 카드 §8 (19점으로 판정하지 않는다).
      실패가 있으면 기록하고 예외를 낸다.
    ⚠ 좌표 대조는 `frame.xyz` ↔ `scf.in` 이다. scf 는 원자를 움직이지 않으므로 이 둘이
      맞으면 두 계산이 같은 배치를 본 것이다. 완전한 비트 동일은 xyz↔분수좌표 왕복에서
      성립하지 않으므로 **문턱(기본 1e-6 Å)** 으로 판정하고 그 값을 기록한다.
    """
    from ase.io import read as _read, write as _write
    import numpy as _np
    out_dir = Path(out_dir)
    man_p = out_dir / f"SNAPSHOTS_{label}_{seed}.json"
    if not man_p.is_file():
        raise FileNotFoundError(f"스냅샷 원장이 없다: {man_p}")
    man = json.loads(man_p.read_text(encoding="utf-8"))
    frames, rows, bad = [], [], []
    for rec in man["snapshots"]:
        w = Path(rec["path"])
        at = _read(str(w / "frame.xyz"))
        try:
            if coord_digest(at) != rec["coord_sha256"]:
                raise ValueError("frame.xyz 가 원장 기록과 다르다 (파일이 바뀌었다)")
            _c, _s, cart = parse_pw_in_positions((w / "scf.in").read_text())
            if _s != at.get_chemical_symbols():
                raise ValueError("scf.in 과 frame.xyz 의 원소 순서가 다르다")
            # ⛔⛔ 주기경계를 봐야 한다. 첫 판은 데카르트 좌표를 그냥 뺐는데,
            #   frame.xyz 와 scf.in 이 원자를 **서로 다른 주기 이미지**에 적으면
            #   (wrapping 관례 차이) 편차가 통째로 격자벡터 크기로 나온다.
            #   2026-09-10 실측: 20점 **전부** 실패했고 편차가 57.58 Å(b2o3 c_z)·
            #   35.04 Å 처럼 **격자벡터 값 몇 종류로만 반복**됐다 — 좌표가 틀렸으면
            #   제각각 나왔을 값이다.
            #   ⚠ 문턱을 느슨하게 푸는 게 아니다. **격자 병진 정수배만** 용서하고,
            #     그 나머지(잔차)는 원래 문턱으로 그대로 잰다. 원자가 실제로
            #     움직였으면 잔차가 남아 여전히 실패한다.
            _cellA = _np.asarray(_c, dtype=float)
            _d = _np.asarray(cart) - at.get_positions()
            _fr = _d @ _np.linalg.inv(_cellA)          # 격자 단위 편차
            _n = _np.round(_fr)                         # 정수 병진분
            dev = float(_np.abs((_fr - _n) @ _cellA).max())   # 이미지 접은 뒤 잔차
            n_img = int(_np.abs(_n).max())              # 몇 칸이나 옮겨 적혔나
            if dev > max_dev_A:
                raise ValueError(f"좌표가 어긋난다: 이미지 접은 뒤 최대 {dev:.3e} Å "
                                 f"> {max_dev_A:.0e} (병진 {n_img}칸)")
            e, F, fl = parse_pw_out((w / "scf.out").read_text(errors="ignore"))
            if len(F) != len(at):
                raise ValueError(f"힘 {len(F)}개 · 원자 {len(at)}개")
            if not (fl["converged"] and fl["job_done"]):
                raise ValueError(f"미수렴/미완료 {fl}")
        except Exception as exc:
            bad.append({"tag": rec["tag"], "why": str(exc)}); continue
        at.calc = None
        from ase.calculators.singlepoint import SinglePointCalculator as _SPC
        at.calc = _SPC(at, energy=e, forces=_np.asarray(F))
        frames.append(at)
        rows.append({"tag": rec["tag"], "time_ps": rec["time_ps"],
                     "E_eV": e, "F_max_eVA": float(_np.abs(_np.asarray(F)).max()),
                     "coord_max_dev_A": dev, "coord_image_shift_cells": n_img,
                     "coord_sha256": rec["coord_sha256"]})
    res = {"card": man["card"], "label": label, "seed": seed,
           "n_ok": len(rows), "n_expected": len(man["snapshots"]),
           "coord_check": {"기준": "frame.xyz ↔ scf.in — **주기 이미지를 접은 뒤** 최대편차",
                           "문턱_A": max_dev_A,
                           "⚠": "비트 동일이 아니라 문턱 판정이다 — 분수좌표 왕복 때문.",
                           "⚠_이미지": "coord_image_shift_cells 는 두 파일이 원자를 몇 칸 "
                                      "다른 주기 이미지에 적었는지다. 0 이 아니어도 물리적으로 "
                                      "같은 배치이고, 격자 병진 정수배만 용서한다 — 그 나머지 "
                                      "잔차는 문턱으로 그대로 잰다 (2026-09-10 수정)."},
           "pseudos": man["pseudos"], "points": rows, "failed": bad}
    (out_dir / f"RESULTS_{label}_{seed}.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=1))
    if bad:
        raise RuntimeError(f"{label}/{seed}: {len(bad)}점 실패 — " +
                           " · ".join(f"{b['tag']}({b['why']})" for b in bad) +
                           "  ⛔ 카드 §8: 빠뜨린 채 판정하지 않는다")
    _write(str(out_dir / f"labeled_{label}_{seed}.xyz"), frames, format="extxyz")
    return res


def _cli_defaults():
    """argparse 기본값을 **파서에서** 읽는다 (문서에 적힌 값이 아니라 실제 값)."""
    return [(a.dest, a.default) for a in _build_parser()._actions]


def _selftest():
    import tempfile, hashlib as _h
    from ase import Atoms
    from ase.io import write as _write
    ok = fail = 0

    def chk(c, m):
        nonlocal ok, fail
        print(("  \u2b55 " if c else "  \u26d4 ") + m)
        ok, fail = ok + bool(c), fail + (not c)

    chk(frame_index_for_time(10, 100) == 100, "t=10 ps · save_fs 100 fs → index 100")
    chk(frame_index_for_time(50, 100) == 500, "t=50 ps → index 500")
    chk(frame_index_for_time(0.05, 100) == 1,
        "half-up 반올림 (0.05 ps → index 1 · 파이썬 기본 round 면 0 이 된다)")
    try:
        frame_index_for_time(10, 0); chk(False, "\u26d4음성: save_fs=0 을 받으면 안 된다")
    except ValueError:
        chk(True, "\u26d4음성: save_fs=0 거부")

    a1 = Atoms("Li2", positions=[[0, 0, 0], [1, 1, 1]], cell=[5, 5, 5], pbc=True)
    a2 = Atoms("Li2", positions=[[0, 0, 0], [1, 1, 1.000000000001]], cell=[5, 5, 5], pbc=True)
    a3 = Atoms("Li2", positions=[[0, 0, 0], [1, 1, 1.001]], cell=[5, 5, 5], pbc=True)
    chk(coord_digest(a1) == coord_digest(a2), "10자리 **아래**(1e-12) 차이는 같은 배치")
    a2b = Atoms("Li2", positions=[[0, 0, 0], [1, 1, 1.0000000001]], cell=[5, 5, 5], pbc=True)
    chk(coord_digest(a1) != coord_digest(a2b), "⛔음성: 1e-10 은 10자리에 보이므로 다른 배치")
    chk(coord_digest(a1) != coord_digest(a3), "\u26d4음성: 0.001 Å 다르면 다른 배치")

    txt = generate_pwin(a1, "t", calculation='scf', kpoints='gamma',
                        occupations='fixed', pseudo_dir='/x',
                        pp_names={'Li': 'li_pbe_v1.4.uspp.F.UPF'})
    chk("K_POINTS gamma" in txt and "automatic" not in txt, "gamma k-점 경로")
    chk("occupations = 'fixed'" in txt and "degauss" not in txt,
        "\u26d4음성: fixed 인데 degauss 가 남으면 안 된다")
    chk("tprnfor     = .true." in txt and "&IONS" not in txt, "scf + 힘 출력 · 이완 절 없음")

    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "pp").mkdir()
        (d / "pp" / "li_pbe_v1.4.uspp.F.UPF").write_bytes(b"x")
        got = preflight_pseudos(["Li"], d / "pp")
        chk(got["Li"]["sha256"] == _h.sha256(b"x").hexdigest(), "유사포텐셜 해시 기록")
        try:
            preflight_pseudos(["Li", "S"], d / "pp")
            chk(False, "\u26d4음성: 없는 유사포텐셜을 통과시키면 안 된다")
        except FileNotFoundError as e:
            chk("S:" in str(e), "\u26d4음성: 빠진 원소를 이름으로 지목")

        tr = d / "traj.xyz"
        _write(str(tr), [a1] * 6, format="extxyz")
        m = snapshots_from_traj(tr, [0.1, 0.2], 100, d / "out", "lbl", "s2", d / "pp")
        chk(len(m["snapshots"]) == 2 and m["snapshots"][1]["frame_index"] == 2,
            "스냅샷 2개 · index 규칙 적용")
        chk((d / "out" / "lbl_s2_t0ps" / "scf.in").is_file(), "scf.in 생성")
        chk(m["snapshots"][0]["coord_sha256"] == coord_digest(a1), "좌표 해시가 frame 과 일치")
        # ⑪ 2026-09-14 — 형제 함수·CLI 와 기본 smearing 이 갈리면 **함수 직접 호출 경로만** 위험해진다
        import inspect as _ins
        _fd = _ins.signature(snapshots_from_traj).parameters["smearing"].default
        _sd = _ins.signature(scf_from_xyz).parameters["smearing"].default
        _cd = [a for a in _cli_defaults() if a[0] == "smearing"]
        chk(_fd == _sd == "gaussian" and _cd and _cd[0][1] == "gaussian",
            f"뜨거운 스냅샷 기본 smearing 이 세 경로에서 같다 (함수 {_fd} · 형제 {_sd} · CLI {_cd[0][1] if _cd else '?'})")
        try:
            snapshots_from_traj(tr, [10.0], 100, d / "out2", "lbl", "s2", d / "pp")
            chk(False, "\u26d4음성: 범위 밖 프레임을 조용히 대체하면 안 된다")
        except IndexError as e:
            chk("범위 밖" in str(e), "\u26d4음성: 창 밖 표본 거부")

        # ── 회수 경로 ──────────────────────────────────────────────────
        e, F, fl = parse_pw_out(
            "!    total energy              =     -10.00000000 Ry\n"
            "     convergence has been achieved in  9 iterations\n"
            "     Forces acting on atoms (cartesian axes, Ry/au):\n\n"
            "     atom    1 type  1   force =     0.10000000    0.00000000    0.00000000\n"
            "     atom    2 type  1   force =    -0.10000000    0.00000000    0.00000000\n"
            "\n     JOB DONE.\n")
        chk(abs(e - (-10.0 * RY_TO_EV)) < 1e-9 and fl["converged"] and fl["job_done"],
            "pw.x 에너지·수렴·완료 파싱")
        chk(len(F) == 2 and abs(F[0][0] - 0.1 * RY_AU_TO_EV_A) < 1e-9,
            "힘 단위 변환 Ry/au → eV/Å")
        try:
            parse_pw_out("아무것도 없음"); chk(False, "\u26d4음성: 빈 출력을 통과시키면 안 된다")
        except ValueError:
            chk(True, "\u26d4음성: 총에너지 없는 출력 거부")
        try:
            parse_pw_out("!    total energy              =     -1.0 Ry\n")
            chk(False, "\u26d4음성: 힘 없는 출력을 통과시키면 안 된다")
        except ValueError as _x:
            chk("힘 블록" in str(_x), "\u26d4음성: 힘 블록 없는 출력 거부 (tprnfor 안내)")

        # ── ⛔음성: 이어붙인 두 실행 (회신 BJ2 P0-3b 재현 fixture) ──────────
        #   A: −100 Ry · F 0.01   B: −200 Ry · F 0.09
        #   옛 파서는 **E=B · F=A** 를 한 레코드로 내고 플래그가 둘 다 True 였다.
        def _run(e_ry, f_ry):
            return ("     Program PWSCF v.7.4.1 starts on 1Jan2026 at 0: 0: 0\n"
                    f"!    total energy              =   {e_ry:.8f} Ry\n"
                    "     convergence has been achieved in  9 iterations\n"
                    "     Forces acting on atoms (cartesian axes, Ry/au):\n\n"
                    f"     atom    1 type  1   force =     {f_ry:.8f}    0.00000000    0.00000000\n"
                    f"     atom    2 type  1   force =    -{f_ry:.8f}    0.00000000    0.00000000\n"
                    "\n     JOB DONE.\n")
        _A, _B = _run(-100.0, 0.01), _run(-200.0, 0.09)
        _eA, _FA, _ = parse_pw_out(_A); _eB, _FB, _ = parse_pw_out(_B)
        chk(abs(_eA - (-100.0 * RY_TO_EV)) < 1e-9 and abs(_eB - (-200.0 * RY_TO_EV)) < 1e-9,
            "단독 실행 둘은 각자 제 에너지를 준다 (fixture 가 유효하다)")
        try:
            parse_pw_out(_A + _B)
            chk(False, "\u26d4음성: 이어붙인 두 실행을 한 레코드로 내면 안 된다 (E=B·F=A 혼합)")
        except ValueError as _x:
            chk("여러 번" in str(_x) or "힘 블록이" in str(_x),
                "\u26d4음성: 실행이 둘이면 거부 — BJ2 P0-3b (탐지 장치 신설)")
        try:
            # JOB DONE 이 없는 앞 실행 + 완결 실행 → 힘 블록 2개로도 잡힌다
            parse_pw_out(_A.replace("JOB DONE.", "") + _B)
            chk(False, "\u26d4음성: 앞 실행이 미완이어도 섞으면 안 된다")
        except ValueError as _x:
            chk(True, "\u26d4음성: 앞 실행이 미완(JOB DONE 없음)이어도 거부")
        _pin = (d / "out" / "lbl_s2_t0ps" / "scf.in").read_text()
        _c, _s2, _cart = parse_pw_in_positions(_pin)
        import numpy as _np2
        chk(_s2 == ["Li", "Li"] and
            float(_np2.abs(_np2.asarray(_cart) - a1.get_positions()).max()) < 1e-9,
            "scf.in 분수좌표 → 카티전이 frame 과 일치")

    # \u2500\u2500 \uc2a4\ud540\u00b7U \ubc29\ucd9c (2026-09-08 \u00b7 Nd O-\ubaa8\ud2f0\ud504 \uc7ac\ucc44\uc810) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
    from ase import Atoms as _At
    _nd = _At('NdOLi', positions=[[0, 0, 0], [2, 0, 0], [0, 2, 0]], cell=[8, 8, 8], pbc=True)
    _pp = {'Nd': 'Nd.paw.z_14.atompaw.wentzcovitch.v1.2.upf'}
    _plain = generate_pwin(_nd, 'x', calculation='scf', pp_names=_pp, pseudo_dir='/p')
    # \u26d4\uc74c\uc131: \uc548 \uc2dc\ud0a4\uba74 \uc548 \ub098\uc628\ub2e4 (\uae30\ubcf8\uc774 \uc870\uc6a9\ud788 \uc2a4\ud540\u00b7U \ub97c \ucf1c\uba74 \uc61b \uacc4\uc0b0\uacfc \ubabb \ube44\uad50\ud55c\ub2e4)
    chk('nspin' not in _plain and 'HUBBARD' not in _plain,
        "\u26d4\uc74c\uc131: nspin/HUBBARD \ub294 **\uc548 \uc8fc\uba74 \uc548 \ucc0d\ud78c\ub2e4**")
    _spin = generate_pwin(_nd, 'x', calculation='scf', pp_names=_pp, pseudo_dir='/p',
                          nspin=2, start_mag={'Nd': 0.3}, hubbard=['Nd-4f 6.0'],
                          tot_magnetization=6)
    _sp = sorted(set(_nd.get_chemical_symbols()))          # ATOMIC_SPECIES \uc21c\uc11c
    chk(f'starting_magnetization({_sp.index("Nd") + 1}) = 0.3' in _spin,
        "starting_magnetization \uc774 **Nd \uc758 \uc885 \ubc88\ud638**\uc5d0 \ubd99\ub294\ub2e4")
    chk('nspin       = 2' in _spin and 'tot_magnetization = 6' in _spin, "nspin\u00b7\ucd1d\uc790\ud654 \ubc29\ucd9c")
    chk('HUBBARD (ortho-atomic)' in _spin and '  U Nd-4f 6.0' in _spin,
        "HUBBARD \uce74\ub4dc \ud615\uc2dd\uc774 tools/sei/build_dft_inputs.py \uc640 \uac19\ub2e4")
    # \u26d4\uc74c\uc131: \uc885 \ubc88\ud638\ub97c 1\ub85c \ubc15\uc544 \ub450\uba74 \uc6d0\uc18c \uc21c\uc11c\uac00 \ubc14\ub014 \ub54c **\uc5c9\ub6b1\ud55c \uc6d0\uc18c\uc5d0 \uc790\ud654\uac00 \uac78\ub9b0\ub2e4**
    _nd2 = _At('LiNdO', positions=[[0, 0, 0], [2, 0, 0], [0, 2, 0]], cell=[8, 8, 8], pbc=True)
    _s2x = generate_pwin(_nd2, 'x', calculation='scf', pp_names=_pp, pseudo_dir='/p',
                         nspin=2, start_mag={'Nd': 0.3})
    chk(f'starting_magnetization({sorted(set(_nd2.get_chemical_symbols())).index("Nd") + 1}) = 0.3'
        in _s2x, "\u26d4\uc74c\uc131: \uc6d0\uc18c \uad6c\uc131\uc774 \ub2ec\ub77c\ub3c4 Nd \uc758 \ubc88\ud638\ub97c \ub2e4\uc2dc \uc13c\ub2e4")

    # \u2500\u2500 \uad6c\uc870\ud30c\uc77c \u2192 scf (--from_xyz) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
    with tempfile.TemporaryDirectory() as _td:
        _d = Path(_td)
        (_d / "ps").mkdir()
        for _f in ('li_pbe_v1.4.uspp.F.UPF', 'O.pbe-n-kjpaw_psl.0.1.UPF', 'ND.upf'):
            (_d / "ps" / _f).write_text("x")
        _a = _At('LiLiO', positions=[[0, 0, 0], [2, 0, 0], [0, 2, 0]], cell=[8, 8, 8], pbc=True)
        _p1 = _d / "one_post_relax.xyz"; _a.write(str(_p1))
        _m = scf_from_xyz([_p1], _d / "o", str(_d / "ps"), nspin=2,
                          start_mag={'Li': 0.1}, tot_mag_per={'Li': 2})
        chk((_d / "o" / "one" / "scf.in").is_file(), "--from_xyz: <out>/<name>/scf.in \ubc30\uce58")
        chk(_m['cells'][0]['tot_magnetization'] == 4.0,
            "tot_magnetization \uc744 **\uc140\ubcc4 \uc6d0\uc790 \uc218**\ub85c \uacc4\uc0b0\ud55c\ub2e4 (Li 2\uac1c \u00d7 2)")
        chk((_d / "o" / "one" / "struct.xyz").is_file(), "\uc6d0\ubcf8 \uad6c\uc870\ub97c \uc606\uc5d0 \ub0a8\uae34\ub2e4 (\uc7ac\ud604)")
        chk(bool(json.loads((_d / "o" / "MANIFEST.json").read_text()).get("gate")),
            "MANIFEST \uc5d0 gate(\ube44\uad50 \ub2e8\uc704\u00b7\ubb34\ud6a8 \uc870\uac74)\uac00 \uc2e4\ub9b0\ub2e4")
        # \u26d4\uc74c\uc131: frozen-4f PP \uc5d0 U \ub97c \uac78\uba74 **\uac70\ubd80**\ud55c\ub2e4 (\uc6d0\uc790\uac00\uc5d0 \uc5c6\ub294 \uaecd\uc9c8\uc5d0 U)
        (_d / "ps" / "Nd.frozen.UPF").write_text('z_valence="11.0"\n')
        _an = _At('NdO', positions=[[0, 0, 0], [2, 0, 0]], cell=[8, 8, 8], pbc=True)
        _p2 = _d / "nd_post_relax.xyz"; _an.write(str(_p2))
        try:
            scf_from_xyz([_p2], _d / "o3", str(_d / "ps"), nspin=2,
                         start_mag={'Nd': 0.3}, hubbard=['Nd-4f 6.0'],
                         pp_names={'Nd': 'Nd.frozen.UPF'})
            chk(False, "\u26d4\uc74c\uc131: frozen-4f \uc5d0 U \ub97c \uac78\uba74 \uac70\ubd80\ud574\uc57c \ud55c\ub2e4")
        except ValueError as _e:
            chk('frozen-4f' in str(_e), "\u26d4\uc74c\uc131: frozen-4f + U \uac70\ubd80 (z_valence \ub85c \ud310\ubcc4)")
        # \u2b55\uc591\uc131 \uacbd\uacc4: \uac19\uc740 PP \ub77c\ub3c4 U \ub97c \uc548 \uac78\uba74 \ud1b5\uacfc\ud574\uc57c \ud55c\ub2e4 (\uac00\ub4dc\uac00 \uacfc\uc789\uc774\uba74 \uc548 \ub41c\ub2e4)
        _m3 = scf_from_xyz([_p2], _d / "o4", str(_d / "ps"),
                           pp_names={'Nd': 'Nd.frozen.UPF'})
        chk(len(_m3['cells']) == 1, "\u2b55\uc591\uc131: frozen-4f \ub77c\ub3c4 U \uc5c6\uc774\ub294 \ud1b5\uacfc")
        # \u26d4\uc74c\uc131: \uc720\uc0ac\ud3ec\ud150\uc15c\uc774 \uc5c6\uc73c\uba74 **\uc785\ub825\uc744 \ub9cc\ub4e4\uc9c0 \uc54a\ub294\ub2e4** (\ub098\uc911\uc5d0 pw.x \uac00 \uc8fd\ub294\ub2e4)
        try:
            scf_from_xyz([_p1], _d / "o2", str(_d / "nope"))
            chk(False, "\u26d4\uc74c\uc131: \uc5c6\ub294 pseudo_dir \ub85c\ub3c4 \uc785\ub825\uc744 \ub9cc\ub4e4\uba74 \uc548 \ub41c\ub2e4")
        except Exception:
            chk(True, "\u26d4\uc74c\uc131: pseudo \uc5c6\uc73c\uba74 \uc785\ub825 \uc0dd\uc131 \uac70\ubd80")

    # ── ⭐ 정적대조 (회신 BO 조건 1) ──────────────────────────────────────────────
    _stress_blk = ("     total   stress  (Ry/bohr**3)                   (kbar)     P=      -1.23\n"
                   "  -0.00001000   0.00000000   0.00000000          -1.47        0.00        0.00\n"
                   "   0.00000000  -0.00000800   0.00000000           0.00       -1.18        0.00\n"
                   "   0.00000000   0.00000000  -0.00000700           0.00        0.00       -1.03\n")
    _sp = parse_pw_stress("x\n" + _stress_blk + "y\n")
    chk(abs(_sp["P_GPa"] + 0.123) < 1e-9 and abs(_sp["sigma_GPa"][0][0] + 0.147) < 1e-9
        and abs(_sp["sigma_GPa"][2][2] + 0.103) < 1e-9, "parse_pw_stress: kbar → GPa, 대각·P 정확")
    try:
        parse_pw_stress(_stress_blk + _stress_blk); chk(False, "⛔음성: 응력 블록 2개 → 거부")
    except ValueError:
        chk(True, "⛔음성: 응력 블록 2개(이어붙인 실행) → 거부")
    try:
        parse_pw_stress("JOB DONE\n"); chk(False, "⛔음성: 응력 블록 없음 → 거부")
    except ValueError:
        chk(True, "⛔음성: 응력 블록 없음(tstress 꺼짐) → 거부")
    with tempfile.TemporaryDirectory() as _td:
        _d = Path(_td)
        _A = _At('LiLiSS', positions=[[0, 0, 0], [2.5, 0, 0], [0, 2.5, 0], [2.5, 2.5, 0]], cell=[5, 5, 5], pbc=True)
        _B = _A.copy(); _B.set_cell([5.4, 5.4, 5.4], scale_atoms=True)
        _A.write(str(_d / "a.vasp"), format="vasp"); _B.write(str(_d / "b.vasp"), format="vasp")
        _man = static_pair(_d / "a.vasp", _d / "b.vasp", _d / "sp", "/nope")
        _ta = (_d / "sp" / "a" / "scf.in").read_text(); _tb = (_d / "sp" / "b" / "scf.in").read_text()
        chk((_d / "sp" / "manifest.json").exists() and len(_man["cells"]) == 2
            and all(len(c["source_sha256"]) == 64 for c in _man["cells"]), "static_pair: a/b scf.in + manifest(sha256)")
        chk("tstress     = .true." in _ta and "tprnfor     = .true." in _tb, "static_pair: 두 입력 다 tstress/tprnfor")
        def _has(txt, key, val):
            return re.search(rf"^\s*{key}\s*=\s*{re.escape(val)}\s*$", txt, re.M) is not None
        chk(_has(_ta, "ecutwfc", "60") and _has(_ta, "ecutrho", "480") and "  4 4 4 0 0 0" in _ta
            and _has(_ta, "conv_thr", "1.0d-9") and _has(_ta, "mixing_beta", "0.3") and _has(_ta, "smearing", "'mv'")
            and _has(_ta, "degauss", "0.01"),
            "static_pair: 설정 = comp1 정본(60/480/k444/mv 0.01/1e-9/β0.3), 생성기 기본값 아님")
        _sa = re.search(r"&SYSTEM(.*?)/", _ta, re.S).group(1); _sb = re.search(r"&SYSTEM(.*?)/", _tb, re.S).group(1)
        chk(_sa == _sb, "static_pair: (a)(b) &SYSTEM 동일")
        _C = _At('LiLiSP', positions=_A.positions, cell=[5, 5, 5], pbc=True); _C.write(str(_d / "c.vasp"), format="vasp")
        try:
            static_pair(_d / "a.vasp", _d / "c.vasp", _d / "sp2", "/nope"); chk(False, "⛔음성: 조성 다르면 거부")
        except ValueError:
            chk(True, "⛔음성: (a)(b) 조성 다르면 거부 (δΔE 미정의)")
        def _out(E_ry, F, with_stress):
            t = ("     Program PWSCF v.7.4.1 starts on 12Sep2026\n     convergence has been achieved in 9 iterations\n"
                 f"!    total energy              =  {E_ry:.8f} Ry\n\n     Forces acting on atoms (cartesian axes, Ry/au):\n\n")
            for i, f in enumerate(F, 1):
                t += f"     atom {i} type 1   force =  {f[0]:12.8f} {f[1]:12.8f} {f[2]:12.8f}\n"
            t += "\n     Total force =   0.001\n\n"
            if with_stress:
                t += _stress_blk
            return t + "\n     JOB DONE.\n"
        _F = [[0.001, 0, 0], [0, 0.001, 0], [0, 0, 0.001], [0.001, 0.001, 0]]
        (_d / "sp" / "a" / "scf.out").write_text(_out(-40.0, _F, True))
        (_d / "sp" / "b" / "scf.out").write_text(_out(-39.9, _F, False))
        _FU = [[x * RY_AU_TO_EV_A for x in f] for f in _F]
        _uma = {"uma_singlepoint": {"a": {"E_per_atom_eV": -10.0 * RY_TO_EV, "F_eV_A": _FU,
                                           "stress_voigt_GPa": [-0.147, -0.118, -0.103, 0, 0, 0]},
                                    "b": {"E_per_atom_eV": -9.975 * RY_TO_EV, "F_eV_A": _FU,
                                           "stress_voigt_GPa": [0, 0, 0, 0, 0, 0]}}}
        (_d / "uma.json").write_text(json.dumps(_uma))
        _r = compare_static_pair(_d / "sp", _d / "uma.json")
        chk(_r["cells"]["a"]["stress_ok"] and _r["cells"]["a"]["stress"]["max_component_diff_GPa"] < 1e-6
            and _r["cells"]["a"]["force"]["rmse_per_atom_vector_eV_A"] < 1e-9,
            "compare: (a) UMA=DFT 이면 힘·응력 차 0")
        chk((not _r["cells"]["b"]["stress_ok"]) and _r["cells"]["b"]["stress"] is None,
            "⛔음성: (b) 응력 블록 없음 → stress_ok False · **미검증**(추정하지 않음)")
        chk("delta" in _r and abs(_r["delta"]["delta_delta_E_meV_atom"]) < 1e-6
            and abs(_r["cells"]["a"]["force"]["rmse_per_component_eV_A"] * (3 ** 0.5)
                    - _r["cells"]["a"]["force"]["rmse_per_atom_vector_eV_A"]) < 1e-12,
            "compare: δΔE 산술 + 벡터 RMSE = √3 × 성분 RMSE")

        # ── force_self: 각 방법이 자기 기하에서 느끼는 힘 (카드 §5 판정에 필요) ──
        _fa = _r["cells"]["a"]["force_self"]
        _expect = ((3 * (0.001 * RY_AU_TO_EV_A) ** 2 + (0.001 * 2 ** 0.5 * RY_AU_TO_EV_A) ** 2) / 4) ** 0.5
        chk(abs(_fa["DFT"]["rmse_eV_A"] - _expect) < 1e-9 and abs(_fa["UMA"]["rmse_eV_A"] - _expect) < 1e-9,
            "compare/force_self: DFT·UMA 각자의 |F| RMSE 를 낸다 (dF 가 0 이어도)")
        chk(_fa["DFT"]["max_atom"]["index"] == 3
            and abs(_fa["DFT"]["max_atom"]["F_eV_A"] - 0.001 * 2 ** 0.5 * RY_AU_TO_EV_A) < 1e-9
            and set(_fa["DFT"]["by_element"]) == {"Li", "S"},
            "compare/force_self: 최대 원자 + 원소별 분해")
        # ⛔ 음성 경로 — **차이는 크지만 한쪽은 정상점**인 경우를 가르는가.
        #   이게 실측 (b) 의 모습이다: UMA 는 자기 최소점이라 |F|≈0, DFT 는 거기서 힘을 본다.
        #   dF 만 보던 종전 출력으로는 "둘이 다르다" 까지밖에 못 갔다.
        (_d / "sp3" / "a").mkdir(parents=True); (_d / "sp3" / "b").mkdir(parents=True)
        for _t in ("a", "b"):
            shutil.copy(_d / "sp" / _t / "scf.in", _d / "sp3" / _t / "scf.in")
            (_d / "sp3" / _t / "scf.out").write_text(_out(-40.0 if _t == "a" else -39.9, _F, True))
        _uma0 = {"uma_singlepoint": {t: {"E_per_atom_eV": -10.0 * RY_TO_EV, "F_eV_A": [[0, 0, 0]] * 4,
                                        "stress_voigt_GPa": [0, 0, 0, 0, 0, 0]} for t in ("a", "b")}}
        (_d / "uma0.json").write_text(json.dumps(_uma0))
        _r3 = compare_static_pair(_d / "sp3", _d / "uma0.json")
        _f3 = _r3["cells"]["b"]["force_self"]
        chk(_f3["UMA"]["rmse_eV_A"] == 0.0 and abs(_f3["DFT"]["rmse_eV_A"] - _expect) < 1e-9
            and abs(_r3["cells"]["b"]["force"]["rmse_per_atom_vector_eV_A"] - _expect) < 1e-9,
            "⛔음성: UMA 정상점 · DFT 아님 을 가른다 (UMA |F|=0 · DFT |F|>0 · dF=DFT)")
        chk(_f3["기준척도_eV_A"]["forc_conv_thr_1e-3_Ry_bohr"] > 0 and "합격선이 아니다" in _f3["기준척도_eV_A"]["⚠"],
            "compare/force_self: 기준척도는 있되 **합격선이 아니라고 적혀 있다**")

    print(f"  selftest: \u2b55 {ok} \u00b7 \u26d4 {fail}")
    return 0 if fail == 0 else 1


# ══════════════════════════════════════════════════════════════════════════
# 완화된 구조 파일 → scf 단일점 (2026-09-08 · Nd O-모티프 UMA 순위 DFT 재채점)
#
#   왜 여기냐 — `generate_pwin()` 의 52/520 레시피와 `pp_names` 머신별 덮어쓰기를
#   그대로 쓴다. 산출 배치(`<out>/<name>/scf.in`)도 `--from_traj` 와 같게 두어
#   **같은 러너**(run_force_check_scf.sh)가 순차 실행한다.
#
#   ⛔ 이 경로가 **못 하는 것**
#     · 순위를 판정하지 않는다 — 총에너지를 낼 뿐이다. 비교 규칙은 아래 gate 가 적는다.
#     · **다른 조성끼리 비교할 수 있는지 모른다.** n=4(54원자)와 n=5(66원자)는 조성이
#       달라 총에너지도 원자당 에너지도 가로질러 비교하면 안 된다. manifest 에 적어만 둔다.
#     · 스핀 상태가 **의도한 상태로 수렴했는지** 모른다. 그건 회수 단계가 본다.
#     · PP 가 물리적으로 맞는지 모른다 (존재·해시만).
#: 이 비교가 **무엇을 판정하고 무엇을 판정하지 않는가** — 산출물에 항상 실린다.
SCF_COMPARE_GATE = {
    "비교_단위": "같은 조성(같은 n) 안에서만. n=4(54원자)와 n=5(66원자)는 조성이 "
         "달라 총에너지도 원자당 에너지도 가로질러 비교하지 않는다.",
    "상태_선택_정책": ("네 셀 전부 같은 씨앗 자화·같은 U·같은 cutoff/k점. "
               "값을 통일하는 것이 아니라 **정책**을 통일한다."),
    "스핀_구속_선언": ("tot_magnetization 을 Nd 개수×3(4f³, FM 정렬)로 **고정**한다. "
               "이건 자유 바닥상태가 아니라 **선언된 구속**이다 — 두 셀이 서로 "
               "다른 f 점유로 수렴하는 것을 막으려는 것이고, 쌍의 조성이 같으므로 "
               "같은 구속이 걸린다(SDCP wave1 의 '제약된 기준 − 자유로운 복합체' "
               "사고를 피한다). ⚠ 따라서 이 에너지는 **절대값으로 인용 금지**이고 "
               "같은 구속끼리의 차이로만 읽는다. AFM 이 진짜 바닥이어도 Nd 는 이 "
               "비교에서 구경꾼이라 O 모티프 순위는 거의 안 움직인다는 가정 위에 "
               "있다 — 그 가정을 확인하려면 AFM 대조를 따로 돌려야 한다."),
    "무효_조건": ("쌍 안에서 수렴 총자화가 다르면 그 쌍의 ΔE 는 무효다 — "
          "다른 f 점유끼리 뺀 값이 된다 (SDCP wave1 교훈)."),
    "판정하는_것": "같은 n 안의 O 모티프 순위가 UMA 와 같은 부호인가.",
    "판정하지_않는_것": "절대 에너지 · 조성 간 비교 · 형성에너지.",
}


def scf_from_xyz(paths, out_dir, pseudo_dir, ecutwfc=52, ecutrho=520,
                 kpoints='2 2 1', pp_names=None, nspin=1, start_mag=None,
                 hubbard=None, tot_mag_per=None, gate=None,
                 smearing='gaussian', degauss=0.01):
    """구조 파일 여러 개 → `<out>/<name>/scf.in` + manifest.

    ⛔ 2026-09-11 — smearing 종류가 **하드코딩 `mv` 였다.** 뜨거운 황화물 MD 스냅샷에서
      `mv`(cold)는 음의 점유를 허용해 SCF 를 무너뜨린다: 실측 `runs/fc_pilot` 에서
      **118,698 Ry 발산**, 같은 스냅샷·같은 mixing 에서 `gaussian` 은 **49 회 수렴**
      (`runs/fc_gapchk`). 인자로 열고 기본을 `gaussian` 으로 바꾼다.
      manifest 에도 실제 값을 적는다 — 종전엔 문자열 "smearing(mv,0.01)" 이 박혀 있어
      호출부가 뭘 줬든 manifest 가 `mv` 라고 **거짓말**했다.

    `tot_mag_per` = {원소: 원자당 모멘트} — 셀마다 그 원소 개수 × 값으로 tot_magnetization
    을 계산한다 (셀마다 원자 수가 다르므로 상수로 박으면 틀린다).
    """
    from ase.io import read as _read
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    # ⛔ gate 는 **함수가 항상 싣는다.** CLI 에만 두었더니 함수를 직접 부른 경로에서
    #   조용히 사라졌다 (자체시험이 잡았다) — 선언이 빠진 산출물은 나중에 근거가 없다.
    _g = dict(SCF_COMPARE_GATE); _g.update(gate or {})
    man = {"provenance": get_provenance(), "created": _dt_now(),
           "settings": {"ecutwfc": ecutwfc, "ecutrho": ecutrho, "kpoints": kpoints,
                        "nspin": nspin, "starting_magnetization": start_mag or {},
                        "hubbard": hubbard or [], "tot_mag_per_atom": tot_mag_per or {},
                        "occupations": f"smearing({smearing},{degauss})", "calculation": "scf"},
           "gate": _g, "cells": []}
    species_all = set()
    for pth in paths:
        a = _read(str(pth))
        species_all |= set(a.get_chemical_symbols())
    pp = preflight_pseudos(sorted(species_all), pseudo_dir, pp_names)
    # ⛔⛔ **원자가에 없는 껍질에 U 를 걸지 못하게 막는다.** tools/sei/build_dft_inputs.py
    #   가 2026-08-29 에 실측으로 잡은 사고를 이 경로에도 건다: frozen-4f PP(z≈11, 4f 가
    #   core)에 `HUBBARD U Nd-4f` 를 찍으면 QE 가 죽거나 **조용히 무시**한다.
    #   판별 기준도 그쪽과 같다 — z ≈ 14 = 4f 원자가 · z ≈ 11 = frozen.
    for man_s in (hubbard or []):
        el = str(man_s).split('-')[0].strip()
        f = Path(pseudo_dir) / pp.get(el, {}).get("file", "")
        if not f.is_file():
            continue
        head = f.read_text(errors="ignore")[:8000]
        m = re.search(r'z_valence\s*=\s*"?\s*([\d.eEdD+-]+)', head, re.I) or \
            re.search(r"([\d.eEdD+-]+)\s+Z valence", head, re.I)
        if not m:
            continue
        z = float(m.group(1).replace("D", "E").replace("d", "e"))
        if "-4f" in str(man_s) and z < 12.0:
            raise ValueError(
                f"⛔ {el} PP 가 frozen-4f 다 (z_valence {z:.1f} < 12, {pp[el]['file']}) — "
                f"4f 가 core 에 있어 `HUBBARD U {man_s}` 는 걸 대상이 없다.\n"
                "   frozen-4f 로 갈 거면 --hubbard 와 --nspin 2 를 빼라. 4f 를 원자가에 둘 거면 "
                "z≈14 PP(예: Nd.paw.z_14.atompaw…)를 pseudo_dir 에 넣어라.\n"
                "   ⚠ 어느 쪽이든 **비교 대상과 같은 선택**이어야 한다.")
    man["pseudos"] = pp
    for pth in paths:
        pth = Path(pth)
        a = _read(str(pth))
        name = pth.stem.replace("_post_relax", "")
        d = out / name; d.mkdir(parents=True, exist_ok=True)
        syms = a.get_chemical_symbols()
        tm = None
        if int(nspin) == 2 and tot_mag_per:
            tm = sum(syms.count(el) * float(m) for el, m in tot_mag_per.items())
        txt = generate_pwin(a, name, ecutwfc=ecutwfc, ecutrho=ecutrho,
                            kpoints=kpoints, pseudo_dir=pseudo_dir,
                            pp_names={el: v["file"] for el, v in pp.items()},
                            calculation='scf', occupations='smearing',
                            smearing=smearing, degauss=degauss,
                            nspin=nspin, start_mag=start_mag, hubbard=hubbard,
                            tot_magnetization=tm)
        (d / "scf.in").write_text(txt)
        (d / "struct.xyz").write_text(Path(pth).read_text())
        man["cells"].append({"name": name, "source": str(pth), "n_atoms": len(a),
                             "formula": a.get_chemical_formula(),
                             "tot_magnetization": tm,
                             "coord_sha256": coord_digest(a)})
    (out / "MANIFEST.json").write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n")
    return man


def _dt_now():
    import datetime as _d
    return _d.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _build_parser():
    """CLI 파서를 만든다. ⭐ 따로 뺀 이유: 자체시험이 **문서가 아니라 파서에서** 기본값을 읽는다."""
    p = argparse.ArgumentParser(description=__doc__,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--ranking',
                  help='FINAL_RANKING.json from combine_rankings.py')
    p.add_argument('--from_traj', help='궤적에서 스냅샷을 뽑아 scf 입력을 만든다 (힘 대조 카드 §4)')
    p.add_argument('--label'); p.add_argument('--seed')
    p.add_argument('--times_ps', nargs='+', type=float, default=[10, 20, 30, 40, 50])
    p.add_argument('--save_fs', type=float, default=100.0)
    p.add_argument('--pseudo_dir', default='/home/kgy/work/pseudo')
    p.add_argument('--selftest', action='store_true')
    p.add_argument('--collect', action='store_true',
                  help='pw.x 출력을 회수해 DFT 라벨 extxyz + RESULTS json (--out --label --seed)')
    p.add_argument('--top', type=int, default=10)
    p.add_argument('--out')          # --selftest 는 out 이 필요 없다
    p.add_argument('--ecutwfc', type=float, default=52)
    p.add_argument('--ecutrho', type=float, default=520)
    p.add_argument('--kpoints', default='2 2 1')
    p.add_argument('--mixing_mode', default='plain',
                  choices=('plain', 'TF', 'local-TF'),
                  help="기본 plain. ⛔ 황화물 MD 스냅샷에 local-TF 를 쓰지 마라 — "
                       "2026-09-08 실측에서 1회부터 48,000 Ry 발산 + negative rho 5.9E+02 "
                       "(철회됨). sloshing 처방은 --mixing_ndim 12~16 + --occupations smearing")
    p.add_argument('--mixing_beta', type=float, default=0.2)
    p.add_argument('--electron_maxstep', type=int, default=100)
    p.add_argument('--mixing_ndim', type=int, default=8,
                  help='Broyden 이력. 진동하면 12~16 (2026-09-08 실측)')
    p.add_argument('--occupations', default=None,
                  choices=('fixed', 'smearing'),
                  help="기본은 경로별 값. 뜨거운 MD 스냅샷은 fixed 로 수렴이 안 될 수 있다")
    p.add_argument('--smearing', default='gaussian',
                  help="⛔ 기본을 2026-09-11 에 mv → gaussian 으로 바꿨다. 뜨거운 황화물 "
                       "MD 스냅샷에서 mv(cold)는 음의 점유를 허용해 SCF 를 무너뜨린다 — "
                       "같은 스냅샷에서 mv 118,698 Ry 발산(runs/fc_pilot) vs gaussian 49회 "
                       "수렴(runs/fc_gapchk). 금속에는 mv 가 표준이지만 이 계에는 아니다.")
    p.add_argument('--degauss', type=float, default=0.01)
    # ── 구조 파일 → scf 단일점 (Nd O-모티프 재채점) ─────────────────────────
    p.add_argument('--from_xyz', nargs='+',
                  help='완화된 구조 파일들 → <out>/<name>/scf.in (같은 러너로 순차 실행)')
    p.add_argument('--static_pair', nargs=2, metavar=('A', 'B'),
                  help='⭐ 정적대조(카드 v3 §5): 같은 조성의 고정 기하 두 개 → <out>/{a,b}/scf.in + manifest. '
                       'DFT 설정은 comp1 정본(60/480/k444/mv 0.01/1e-9/β0.3)으로 고정 — 기본값 아님')
    p.add_argument('--compare_static_pair', nargs=2, metavar=('OUT', 'UMA_JSON'),
                  help='정적대조 회수: <OUT>/{a,b}/scf.out + gabia uma_ab.json → <OUT>/compare.json (δΔE·힘·응력)')
    p.add_argument('--nspin', type=int, default=1, choices=(1, 2))
    p.add_argument('--start_mag', nargs='*', default=[],
                  help='원소=씨앗자화 (예: Nd=0.3). ⚠ 비교하는 셀 전부 **같은 값**이어야 한다')
    p.add_argument('--tot_mag_per', nargs='*', default=[],
                  help='원소=원자당 모멘트 (예: Nd=3) → 셀별 개수×값으로 tot_magnetization')
    p.add_argument('--hubbard', nargs='*', default=[],
                  help='HUBBARD 항목 (예: "Nd-4f 6.0"). ⛔ 원자가에 없는 껍질에 걸지 말 것')
    p.add_argument('--pp', nargs='*', default=[],
                  help='유사포텐셜 파일명 덮어쓰기 (예: Nd=Nd.paw.z_14.atompaw...upf)')
    return p


def main():
    p = _build_parser()
    args = p.parse_args()

    def _kv(items):
        d = {}
        for s in items:
            if '=' not in s:
                p.error(f'--- 형식은 원소=값 이다: {s!r}')
            k, v = s.split('=', 1)
            d[k] = v
        return d

    if args.selftest:
        sys.exit(_selftest())
    if args.collect:
        if not (args.out and args.label and args.seed):
            p.error('--collect 는 --out --label --seed 가 필요하다')
        r = collect_results(args.out, args.label, args.seed)
        print(f"✓ {args.label}/{args.seed}: {r['n_ok']}/{r['n_expected']}점 회수 "
              f"· 좌표 최대편차 {max(x['coord_max_dev_A'] for x in r['points']):.2e} Å")
        return
    if args.static_pair:
        if not args.out:
            p.error('--static_pair 는 --out 이 필요하다')
        _m = static_pair(args.static_pair[0], args.static_pair[1], args.out, args.pseudo_dir)
        for c in _m["cells"]:
            print(f"  {c['tag']}: {c['n_atoms']}원자 · V/atom {c['V_per_atom']:.3f} · src sha256 {c['source_sha256'][:12]}…")
        print(f"✓ static_pair → {args.out}/{{a,b}}/scf.in · manifest.json (설정 = comp1 정본, tstress/tprnfor 켜짐)")
        return
    if args.compare_static_pair:
        _r = compare_static_pair(args.compare_static_pair[0], args.compare_static_pair[1])
        for t, c in _r["cells"].items():
            f = c["force"]; st = c["stress"]
            print(f"  {t}: 힘 RMSE(벡터) {f['rmse_per_atom_vector_eV_A']:.4f} eV/Å"
                  f"{' ⚠경보' if f['alarm_exceeded'] else ''} · 최대원자 {f['max_atom']['element']}#{f['max_atom']['index']} "
                  f"{f['max_atom']['dF_eV_A']:.3f} · 응력 " +
                  (f"최대성분차 {st['max_component_diff_GPa']:.3f} GPa{' ⚠경보' if st['alarm_exceeded'] else ''}" if st else "**미검증(응력 블록 없음)**"))
            fs = c.get("force_self")
            if fs:
                print(f"      자기힘 |F| RMSE  DFT {fs['DFT']['rmse_eV_A']:.4f} (max {fs['DFT']['max_atom']['element']}"
                      f"#{fs['DFT']['max_atom']['index']} {fs['DFT']['max_atom']['F_eV_A']:.3f})"
                      f"  ·  UMA {fs['UMA']['rmse_eV_A']:.4f} (max {fs['UMA']['max_atom']['element']}"
                      f"#{fs['UMA']['max_atom']['index']} {fs['UMA']['max_atom']['F_eV_A']:.3f})"
                      f"   [relax 수렴문턱 {fs['기준척도_eV_A']['forc_conv_thr_1e-3_Ry_bohr']:.4f} — 합격선 아님]")
        if "delta" in _r:
            d = _r["delta"]
            print(f"  ΔE(b−a): UMA {d['dE_UMA_b_minus_a_meV_atom']:+.1f} · DFT {d['dE_DFT_b_minus_a_meV_atom']:+.1f} "
                  f"· δΔE {d['delta_delta_E_meV_atom']:+.1f} meV/atom   (basin 판정 없음)")
        print(f"✓ compare → {args.compare_static_pair[0]}/compare.json")
        return
    if args.from_xyz:
        if not args.out:
            p.error('--from_xyz 는 --out 이 필요하다')
        _sm = {k: float(v) for k, v in _kv(args.start_mag).items()}
        _tm = {k: float(v) for k, v in _kv(args.tot_mag_per).items()}
        if args.nspin == 2 and not _sm:
            p.error('--nspin 2 인데 --start_mag 이 없다 — 씨앗을 안 주면 셀마다 다른 '
                    '상태로 수렴할 수 있고 그러면 총에너지 차가 무의미해진다')
        man = scf_from_xyz(args.from_xyz, args.out, args.pseudo_dir,
                           args.ecutwfc, args.ecutrho, args.kpoints,
                           pp_names=_kv(args.pp), nspin=args.nspin,
                           start_mag=_sm, hubbard=args.hubbard,
                           tot_mag_per=_tm,
                           smearing=args.smearing, degauss=args.degauss)
        print(f"✓ {len(man['cells'])}셀 → {args.out}  (nspin={args.nspin}"
              f"{' · U=' + ','.join(args.hubbard) if args.hubbard else ''})")
        for c in man['cells']:
            print(f"    {c['name']:36s} {c['formula']:26s} n={c['n_atoms']:3d} "
                  f"tot_mag={c['tot_magnetization']}  {c['coord_sha256'][:12]}")
        print("  ⚠ 비교는 같은 n 안에서만. MANIFEST.json 의 gate 를 읽어라.")
        return
    if args.from_traj:
        if not args.out:
            p.error('--from_traj 는 --out 이 필요하다')
        if not (args.label and args.seed):
            p.error('--from_traj 는 --label 과 --seed 가 필요하다 (산출물 이름·계보)')
        man = snapshots_from_traj(args.from_traj, args.times_ps, args.save_fs,
                                  args.out, args.label, args.seed, args.pseudo_dir,
                                  args.ecutwfc, args.ecutrho,
                                  mixing_mode=args.mixing_mode,
                                  mixing_beta=args.mixing_beta,
                                  electron_maxstep=args.electron_maxstep,
                                  mixing_ndim=args.mixing_ndim,
                                  occupations=args.occupations,
                                  smearing=args.smearing, degauss=args.degauss)
        print(f"✓ {args.label}/{args.seed}: 스냅샷 {len(man['snapshots'])}개 → {args.out}")
        for r in man['snapshots']:
            print(f"    {r['tag']}  frame {r['frame_index']}  n={r['n_atoms']}  {r['coord_sha256'][:12]}")
        return
    if not (args.ranking and args.out):
        p.error('--ranking(+--out) 또는 --from_traj 또는 --selftest')

    data = json.loads(Path(args.ranking).read_text())
    rows = data.get('rows', [])[:args.top]
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    # Resume: skip if relax.in already exists
    summary = {'provenance': get_provenance(), 'generated': [], 'skipped': [],
               'failed': []}
    for i, row in enumerate(rows, 1):
        name = row.get('name', f'top{i}')
        work = out / f'rank{i:02d}_{name}'
        relax_in = work / 'relax.in'
        if relax_in.exists():
            summary['skipped'].append(name)
            print(f"  [skip] {name} (relax.in exists)")
            continue
        # We need the xyz to read coordinates — look up from screening
        xyz_candidates = [
            row.get('xyz_input'), row.get('xyz_file'),
            row.get('_anneal', {}).get('post_relax_xyz'),
        ]
        xyz_path = next((Path(x) for x in xyz_candidates
                        if x and Path(x).exists()), None)
        if xyz_path is None:
            summary['failed'].append({'name': name, 'reason': 'no xyz found'})
            print(f"  ⚠ {name}: no xyz available")
            continue
        try:
            atoms = read(str(xyz_path))
            work.mkdir(parents=True, exist_ok=True)
            relax_in.write_text(generate_pwin(atoms, name,
                                              args.ecutwfc, args.ecutrho,
                                              args.kpoints))
            # Copy xyz for traceability
            shutil.copy(str(xyz_path), str(work / 'init.xyz'))
            # List required pseudos
            species = sorted(set(atoms.get_chemical_symbols()))
            (work / 'pseudo_list.txt').write_text(
                '\n'.join(PSEUDOS[s][1] for s in species) + '\n')
            summary['generated'].append({
                'name': name, 'path': str(work),
                'rank': i,
                'composite_score': row.get('score_combined'),
                'B0_GPa_MLIP': row.get('B0_GPa'),
                'E_young_GPa_MLIP': row.get('E_young_GPa'),
            })
            print(f"  ✓ rank{i:02d}_{name} → {work}")
        except Exception as e:
            summary['failed'].append({'name': name, 'reason': str(e)})
            print(f"  ✗ {name}: {e}")

    (out / 'dft_input_summary.json').write_text(
        json.dumps(summary, indent=2, default=str))
    print(f"\n✓ Generated {len(summary['generated'])} DFT inputs "
          f"({len(summary['skipped'])} skipped, "
          f"{len(summary['failed'])} failed)")
    print(f"\nNext: scp -r {out} <KISTI>:/path/  then sbatch <run script>")


if __name__ == '__main__':
    main()
