#!/usr/bin/env python3
"""Build PAW SCF + NSCF + lobsterin (extended basis) for LOBSTER post-processing.

Takes a V0_relax.in/out pair (which may use USPP pseudos) and writes:
  - lobster_scf.in   : PAW SCF (kjpaw pseudos) at the V0 cell
  - lobster_nscf.in  : NSCF with wf_collect, nosym, nbnd ≥ required for the
                       extended LCAO basis (Li 1s 2s 2p, P/S/Cl 3s 3p 3d)
  - lobsterin        : extended-basis lobster config (cohpGenerator presets)
  - run_lobster.sh   : sequencer (SCF → NSCF → lobster)

PAW pseudo filenames are hard-coded to the kjpaw_psl 1.0.0 set:
  Li.pbe-sl-kjpaw_psl.1.0.0.UPF
  P.pbe-n-kjpaw_psl.1.0.0.UPF
  S.pbe-nl-kjpaw_psl.1.0.0.UPF
  Cl.pbe-nl-kjpaw_psl.1.0.0.UPF

Usage:
    python3 build_lobster_paw_inputs.py \\
        --src_in  V0_relax.in \\
        --src_out V0_relax.out \\
        --workdir lobster_ext \\
        --pseudo_dir /home/ubuntu/pseudo/ \\
        --nbnd 450
"""
import argparse, re
from pathlib import Path
import numpy as np


PAW_PSEUDOS = {
    "Li": "Li.pbe-sl-kjpaw_psl.1.0.0.UPF",
    "P":  "P.pbe-n-kjpaw_psl.1.0.0.UPF",
    "S":  "S.pbe-nl-kjpaw_psl.1.0.0.UPF",
    "Cl": "Cl.pbe-nl-kjpaw_psl.1.0.0.UPF",
    "Br": "Br.pbe-n-kjpaw_psl.1.0.0.UPF",  # comp2 (Li6PS5Cl0.5Br0.5) 2026-07-22
    "O":  "O.pbe-n-kjpaw_psl.0.1.UPF",     # lpsocl (2026-07-17); b2o3 KISTI run had it bash-side
    # Nd (2026-09-10, ndo_lpscl16 대조군). gabia/kgy 둘 다 이 파일만 있다.
    # ⚠ 라벨 'spdn' 은 s·p·d semicore + nlcc 를 뜻하고 **f 가 없다** = 4f-in-core 로 보이지만,
    #   **파일명으로 정하지 않는다** (Po/P 사고). 실제 basis 는 UPF 의 valence_configuration
    #   에서 읽는다 — upf_valence_labels() 참조.
    "Nd": "Nd.pbe-spdn-kjpaw_psl.1.0.0.UPF",
    "B":  "B.pbe-n-kjpaw_psl.1.0.0.UPF",   # b2o3 (2026-09-10) — repo 다른 도구와 같은 이름
}
SPECIES_MASS = {"Li": 6.941, "P": 30.974, "S": 32.065, "Cl": 35.453, "Br": 79.904,
                "O": 15.999, "Nd": 144.242, "B": 10.811}
BASIS_FUNCS = {"Li": "1s 2s 2p", "P": "3s 3p 3d", "S": "3s 3p 3d",
               "Cl": "3s 3p 3d", "Br": "4s 4p", "O": "2s 2p",
               # Nd 는 UPF 에서 읽어 덮어쓴다 (아래). 이 값은 못 읽었을 때의 대비다.
               "Nd": "5s 5p 5d 6s", "B": "2s 2p"}


def upf_valence_labels(upf_path):
    """UPF 의 valence_configuration 에서 nl 라벨을 읽는다 ('5S','4F' -> '5s 4f').

    ⛔ **유사포텐셜의 valence 를 파일명으로 추측하지 않는다.** 2026-08-20 에
      파일명만 보고 Po 를 P 자리에 꽂을 뻔한 사고가 있었다. LOBSTER basis 가
      pseudo 의 valence 와 어긋나면 charge spilling 이 치솟는데, 그건 조용히
      나쁜 결과로 나오지 에러로 안 나온다.

    이 함수가 못 하는 것: 읽은 라벨이 LOBSTER 가 아는 basis 인지 검증하지 않는다.
      (LOBSTER 가 거부하면 그때 알 수 있고, 통과하면 charge spilling 을 봐야 한다)
    """
    import re as _re
    try:
        txt = open(upf_path, errors="ignore").read(200000)
    except OSError:
        return None
    # ⛔ pslibrary UPF 는 `Valence configuration:` (공백·대문자) 로 쓴다.
    #   `valence_configuration` 만 찾다가 **여섯 원소 전부 못 읽었다** (gabia 실측
    #   2026-09-10). 다행히 못 읽은 걸 화면에 찍게 해둬서 바로 보였다.
    m = _re.search(r"[Vv]alence[ _]configuration\s*:?(.*?)"
                   r"(?:</PP_INFO|Generation\s+configuration|Generation|wavefunctions)",
                   txt, _re.S)
    if not m:
        return None
    labs = []
    for line in m.group(1).splitlines():
        t = line.split()
        if t and _re.fullmatch(r"[1-7][SPDFspdf]", t[0]) and t[0].lower() not in labs:
            labs.append(t[0].lower())
    return " ".join(labs) if labs else None


def parse_namelists_and_cards(in_text):
    nls, cards = {}, {}
    cur, buf = None, []
    for line in in_text.splitlines():
        s = line.strip()
        if s.startswith("&"):
            cur = ("nl", s[1:].split()[0].upper()); buf = [line]
        elif s == "/" and cur and cur[0] == "nl":
            buf.append(line); nls[cur[1]] = "\n".join(buf); cur, buf = None, []
        elif s and s.split()[0] in {
                "ATOMIC_SPECIES", "K_POINTS", "CELL_PARAMETERS",
                "ATOMIC_POSITIONS", "OCCUPATIONS", "HUBBARD"}:
            if cur and cur[0] == "card":
                cards[cur[1]] = "\n".join(buf)
            cur = ("card", s.split()[0]); buf = [line]
        elif cur:
            buf.append(line)
    if cur and cur[0] == "card":
        cards[cur[1]] = "\n".join(buf)
    return nls, cards


def parse_cell_from_in(text):
    m = re.search(
        r"CELL_PARAMETERS\s*(?:\(?\s*(angstrom|bohr|alat)\s*\)?)?\s*\n"
        r"((?:[-+\d.eE\s]+\n){3})", text, re.IGNORECASE)
    if not m:
        return None, None
    unit = (m.group(1) or "alat").lower()
    rows = [[float(x) for x in line.split()[:3]]
            for line in m.group(2).strip().splitlines()[:3]]
    return np.array(rows), unit


def parse_final_cell(out_text):
    """vc-relax 출력의 **최종** CELL_PARAMETERS. 없으면 (None, None).

    ⛔⛔ 2026-09-18 — 이 함수가 없어서 빌더가 셀을 **입력**에서 읽고 좌표는 **출력**에서
      읽었다. `relax`(셀 고정)면 둘이 같으니 맞지만, **`vc-relax` 면 셀이 바뀐다** —
      옛 셀 + 새 좌표 = **다른 구조**이고 **오류가 안 난다**. 실측: SEI 파이프라인이
      만든 vc-relax 출력을 먹였더니 단위 검사(`Need crystal-coord`)에만 걸렸다.
      그 검사만 풀었으면 조용히 틀린 구조로 LOBSTER 를 돌렸을 것이다.

    QE 는 vc-relax 가 힘·응력 기준을 만족했을 때만 `Begin final coordinates` 블록을
    찍고, 그 안에 CELL_PARAMETERS 와 ATOMIC_POSITIONS 가 **짝으로** 들어 있다.
    그 짝을 쓴다 — 둘을 다른 데서 가져오지 않는다.

    ⛔ 못 하는 것: 블록이 없으면 None 을 준다. 중간 BFGS 스텝의 셀을 대신 쓰지 않는다
      (그건 수렴하지 않은 기하다).
    """
    i = out_text.rfind("Begin final coordinates")
    if i < 0:
        return None, None
    tail = out_text[i:]
    j = tail.find("End final coordinates")
    if j > 0:
        tail = tail[:j]
    m = re.search(r"CELL_PARAMETERS\s*\(?\s*(angstrom|bohr|alat)\s*\)?\s*\n"
                  r"((?:[-+\d.eE\s]+\n){3})", tail, re.IGNORECASE)
    if not m:
        return None, None
    rows = [[float(x) for x in line.split()[:3]]
            for line in m.group(2).strip().splitlines()[:3]]
    return np.array(rows), m.group(1).lower()


def parse_final_positions(out_text):
    matches = list(re.finditer(
        r"ATOMIC_POSITIONS\s*\(([^)]+)\)\n((?:[A-Za-z]\w*\s+[-+\d.eE\s]+\n)+)",
        out_text))
    if not matches:
        return None, None
    m = matches[-1]
    return m.group(1).strip(), m.group(2)


def species_in_block(pos_block):
    """Return unique element symbols (preserving first-seen order)."""
    seen, order = set(), []
    for line in pos_block.strip().splitlines():
        parts = line.split()
        if not parts:
            continue
        sp = parts[0]
        if sp not in seen:
            seen.add(sp); order.append(sp)
    return order


def atomic_species_block(species, pseudo_dir):
    lines = ["ATOMIC_SPECIES"]
    for s in species:
        if s not in PAW_PSEUDOS:
            raise SystemExit(f"No PAW pseudo configured for {s}")
        lines.append(f"  {s:4s} {SPECIES_MASS[s]:8.3f}  {PAW_PSEUDOS[s]}")
    return "\n".join(lines) + "\n"


def control_block(prefix, outdir, calculation, extra=""):
    return f"""&CONTROL
  calculation='{calculation}'
  prefix='{prefix}'
  pseudo_dir='{outdir["pseudo_dir"]}'
  outdir='{outdir["outdir"]}'
  tprnfor=.true.
  tstress=.true.
  verbosity='high'
{extra}/
"""


def _selftest():
    """⛔ 음성 중심. 이 도구의 제일 비싼 결함은 **조용히 다른 구조**를 만드는 것이다.

    2026-09-18 실측: 셀을 `src_in` 에서, 좌표를 `src_out` 에서 읽고 있었다.
    `relax`(셀 고정)면 맞지만 **`vc-relax` 면 옛 셀 + 새 좌표 = 다른 구조**이고
    **오류가 안 난다**. 그 자리를 여기서 잡는다.
    """
    import subprocess
    import sys as _sys
    import tempfile
    n = [0, 0]

    def chk(c, m):
        n[0] += 1; n[1] += bool(c)
        print(("  ✓ " if c else "  ✗ ") + m)

    IN_CELL = "  10.0000 0 0\n  0 10.0000 0\n  0 0 10.0000\n"
    OUT_CELL = "  11.0000 0 0\n  0 11.0000 0\n  0 0 11.0000\n"
    MID_CELL = "  10.5000 0 0\n  0 10.5000 0\n  0 0 10.5000\n"
    POS = "Li  0.0 0.0 0.0\nS   1.0 1.0 1.0\n"

    def mk_out(final=True, mid=True, unit="angstrom"):
        t = ""
        if mid:                                   # 중간 BFGS 스텝 (수렴 전)
            t += f"CELL_PARAMETERS (angstrom)\n{MID_CELL}ATOMIC_POSITIONS ({unit})\n{POS}\n"
        if final:
            t += ("Begin final coordinates\n     new unit-cell volume = 1331.0\n"
                  f"CELL_PARAMETERS (angstrom)\n{OUT_CELL}"
                  f"ATOMIC_POSITIONS ({unit})\n{POS}End final coordinates\n")
        t += "JOB DONE.\n"
        return t

    # ── parse_final_cell: 최종 블록만 본다 ────────────────────────────────
    c, u = parse_final_cell(mk_out())
    chk(c is not None and abs(c[0][0] - 11.0) < 1e-9 and u == "angstrom",
        f"[양성] 최종 블록의 셀을 읽는다 (a={c[0][0] if c is not None else None})")
    # ⛔음성 — 중간 BFGS 스텝의 셀을 집으면 10.5 가 나온다. 그러면 안 된다.
    chk(c is not None and abs(c[0][0] - 10.5) > 1e-9,
        "⛔음성: **중간 스텝의 셀**(10.5)을 집지 않는다 — 수렴 안 한 기하다")
    chk(parse_final_cell(mk_out(final=False)) == (None, None),
        "⛔음성: 최종 블록이 없으면 **None** (중간 셀로 대신하지 않는다)")

    # ── main 의 셀 선택 (subprocess — 실제 실행 경로) ─────────────────────
    def run(calc, final, unit="angstrom"):
        d = tempfile.mkdtemp()
        src_in = (f"&CONTROL\n  calculation='{calc}'\n/\n&SYSTEM\n  ibrav=0\n  nat=2\n  ntyp=2\n/\n"
                  f"ATOMIC_SPECIES\n Li 6.94 x.UPF\n S 32.06 y.UPF\n"
                  f"CELL_PARAMETERS angstrom\n{IN_CELL}"
                  f"ATOMIC_POSITIONS (angstrom)\n{POS}")
        Path(d, "s.in").write_text(src_in)
        Path(d, "s.out").write_text(mk_out(final=final, unit=unit))
        r = subprocess.run([_sys.executable, __file__, "--src_in", f"{d}/s.in",
                            "--src_out", f"{d}/s.out", "--workdir", f"{d}/w",
                            "--pseudo_dir", d, "--nbnd", "8",
                            "--kpoints", "3 3 1 0 0 0"],
                           capture_output=True, text=True, timeout=60)
        return r

    r = run("vc-relax", final=True)
    chk("src_out" in r.stdout, f"[양성] vc-relax → 셀을 **src_out** 에서 (찍힌 말: "
        f"{[l for l in r.stdout.splitlines() if l.startswith('Cell')] or '없음'})")
    chk("+33.10 %" in r.stdout or "33.1" in r.stdout,
        "부피 변화를 **찍는다** (10³ → 11³ = +33.1 %) — 사람이 셀이 바뀐 걸 본다")
    # ⛔음성 — vc-relax 인데 최종 블록이 없으면 **죽어야** 한다 (입력 셀로 안 떨어진다)
    r2 = run("vc-relax", final=False)
    chk(r2.returncode != 0 and "Begin final coordinates" in (r2.stdout + r2.stderr),
        f"⛔음성: vc-relax + 최종블록 없음 → **죽는다** (rc={r2.returncode})")
    chk("src_in" not in r2.stdout,
        "⛔음성: 그때 입력 셀로 **조용히 떨어지지 않는다**")
    # 양성 — relax(셀 고정)면 입력 셀 폴백이 정상
    r3 = run("relax", final=False)
    chk("src_in" in r3.stdout,
        f"[양성] relax + 최종블록 없음 → 입력 셀 폴백 (rc={r3.returncode})")
    # ⛔음성 — 모르는 단위는 거부
    r4 = run("vc-relax", final=True, unit="bohr")
    chk(r4.returncode != 0 and "단위를 모른다" in (r4.stdout + r4.stderr),
        "⛔음성: 모르는 좌표 단위(bohr)를 거부한다")

    # ── k-메시: 조용한 기본값이 카드를 이기면 안 된다 (2026-09-18 실측) ──────
    #   Nd PP-swap 카드 §4 는 `6 6 1` 을 못박았는데 default="2 2 1 0 0 0" 이
    #   아무 말 없이 나갔다. 요약에도 안 찍혀 diff 를 따로 안 쳤으면 그대로 돌 뻔했다.
    d5 = tempfile.mkdtemp()
    Path(d5, "s.in").write_text(
        f"&CONTROL\n  calculation='relax'\n/\n&SYSTEM\n  ibrav=0\n  nat=2\n  ntyp=2\n/\n"
        f"ATOMIC_SPECIES\n Li 6.94 x.UPF\n S 32.06 y.UPF\n"
        f"CELL_PARAMETERS angstrom\n{IN_CELL}ATOMIC_POSITIONS (angstrom)\n{POS}")
    Path(d5, "s.out").write_text(mk_out())
    base5 = [_sys.executable, __file__, "--src_in", f"{d5}/s.in", "--src_out", f"{d5}/s.out",
             "--pseudo_dir", d5, "--nbnd", "8"]
    r5 = subprocess.run(base5 + ["--workdir", f"{d5}/w5"], capture_output=True, text=True, timeout=60)
    chk(r5.returncode != 0 and "kpoints" in (r5.stdout + r5.stderr).lower(),
        f"⛔음성: --kpoints 를 안 주면 **시작하지 않는다** (rc={r5.returncode}) — 조용한 기본값 없음")
    chk(not Path(d5, "w5", "lobster_scf.in").exists(),
        "⛔음성: 그때 입력 파일을 **만들지도 않는다** (반쯤 만든 폴더를 남기지 않는다)")
    r6 = subprocess.run(base5 + ["--workdir", f"{d5}/w6", "--kpoints", "6 6 1 0 0 0"],
                        capture_output=True, text=True, timeout=60)
    scf6 = Path(d5, "w6", "lobster_scf.in").read_text() if r6.returncode == 0 else ""
    nscf6 = Path(d5, "w6", "lobster_nscf.in").read_text() if r6.returncode == 0 else ""
    chk("6 6 1 0 0 0" in scf6 and "6 6 1 0 0 0" in nscf6,
        "[양성] 준 k-메시가 **scf·nscf 둘 다**에 들어간다 (한쪽만 바뀌면 두 계산이 갈린다)")
    chk("2 2 1" not in scf6 and "2 2 1" not in nscf6,
        "⛔음성: 옛 기본값 `2 2 1` 이 어디에도 **남아 있지 않다**")
    chk("6 6 1 0 0 0" in r6.stdout,
        "⛔음성: k-메시가 **요약에 찍힌다** — 안 찍히면 사람이 diff 를 따로 쳐야 잡는다")

    print(f"selftest {'PASS' if n[1] == n[0] else 'FAIL'} — {n[1]}/{n[0]}")
    return 0 if n[1] == n[0] else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src_in", default=None,
                    help="V0_relax.in (셀·종 정보). --from_xyz 를 주면 불필요")
    ap.add_argument("--src_out", default=None,
                    help="V0_relax.out (최종 좌표). --from_xyz 를 주면 불필요")
    ap.add_argument("--from_xyz", default=None,
                    help="extxyz 하나로 셀+좌표를 모두 받는다 (relax out 이 없는 기계용)")
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--pseudo_dir", default="/home/ubuntu/pseudo/")
    ap.add_argument("--nbnd", type=int, default=450,
                    help="nbnd for NSCF (≥ extended-basis LCAO function count)")
    # ⛔ 기본값 없음 (2026-09-18). k-메시는 **셀마다 다르고** 카드가 핀으로 박는 양이다.
    #   전에는 default="2 2 1 0 0 0" 이었고, Nd PP-swap 은 카드 §4 가 `6 6 1` 을 못박았는데
    #   아무도 --kpoints 를 안 줘서 **조용히 2 2 1** 이 나갔다. 요약에도 안 찍혀서 안 보였다.
    #   그래서 fail-closed: 안 주면 시작하지 않는다.
    ap.add_argument("--kpoints", required=True,
                    help="K_POINTS automatic 한 줄 (예: \"6 6 1 0 0 0\"). "
                         "기본값을 두지 않는다 — 셀·카드마다 다르다")
    ap.add_argument("--prefix_base", default="V0_lobster")
    ap.add_argument("--ecutwfc", type=float, default=70.0,
                    help="raised from 52 for PAW (kjpaw needs higher cutoff)")
    ap.add_argument("--ecutrho", type=float, default=560.0)
    args = ap.parse_args()

    wd = Path(args.workdir); wd.mkdir(parents=True, exist_ok=True)

    if args.from_xyz:
        # extxyz -> 셀 + 결정좌표. relax out 이 없는 기계(gabia)를 위한 경로다.
        import re as _re
        L = Path(args.from_xyz).read_text().splitlines()
        nat_x = int(L[0])
        mm = _re.search(r'Lattice="([^"]+)"', L[1])
        if not mm:
            raise SystemExit(f"{args.from_xyz}: Lattice=\"...\" 가 없다 (extxyz 가 아니다)")
        cell = np.array([float(x) for x in mm.group(1).split()]).reshape(3, 3)
        inv = np.linalg.inv(cell)
        rows = []
        for line in L[2:2 + nat_x]:
            t = line.split()
            f = np.array([float(x) for x in t[1:4]]) @ inv
            rows.append(f"  {t[0]:<3s} {f[0]:14.10f} {f[1]:14.10f} {f[2]:14.10f}")
        pos_block = "\n".join(rows)
        pos_unit = "crystal"
        print(f"from_xyz: {args.from_xyz} — {nat_x} atoms, cell from Lattice=")
    else:
        if not (args.src_in and args.src_out):
            raise SystemExit("--from_xyz 를 안 쓰면 --src_in 과 --src_out 이 둘 다 필요하다")
        in_text = Path(args.src_in).read_text()
        out_text = Path(args.src_out).read_text()
        nls, cards = parse_namelists_and_cards(in_text)
        #: ⭐ 2026-09-18 — 셀은 **출력의 최종 블록**을 먼저 본다 (vc-relax 대응).
        #   입력 셀로 떨어지는 것은 relax(셀 고정)일 때뿐이고, 어느 쪽을 썼는지 **찍는다**.
        cell, cell_unit = parse_final_cell(out_text)
        cell_src = "src_out (Begin final coordinates)"
        if cell is None:
            cell, cell_unit = parse_cell_from_in(in_text)
            cell_src = "src_in (출력에 최종 블록이 없다 — relax 로 본다)"
        if cell is None:
            raise SystemExit("CELL_PARAMETERS 를 src_out 에서도 src_in 에서도 못 읽었다")
        if cell_unit != "angstrom":
            raise SystemExit(f"CELL_PARAMETERS 단위가 angstrom 이 아니다: {cell_unit}")
        #: ⛔ vc-relax 인데 입력 셀로 떨어지면 **다른 구조**가 된다 — 조용히 넘어가지 않는다.
        if "vc-relax" in in_text and cell_src.startswith("src_in"):
            raise SystemExit("⛔ 입력이 vc-relax 인데 출력에 `Begin final coordinates` 가 없다. "
                             "이완이 안 끝났거나 수렴하지 않았다 — 입력 셀을 대신 쓰지 않는다.")
        pos_unit, pos_block = parse_final_positions(out_text)
        if pos_block is None:
            raise SystemExit("Could not parse final ATOMIC_POSITIONS from src_out")
        #: ⭐ angstrom 도 받는다. QE 가 `ATOMIC_POSITIONS (angstrom)` 를 그대로 먹고,
        #   아래에서 단위를 **그대로 넘긴다**. 종전엔 crystal 만 받아 SEI 파이프라인
        #   출력을 거부했다 — 그 거부 자체는 옳았다(위 셀 문제를 막았다).
        if not pos_unit.lower().startswith(("crystal", "angstrom")):
            raise SystemExit(f"좌표 단위를 모른다: {pos_unit} (crystal · angstrom 만 받는다)")
        print(f"Cell   : {cell_src} · {cell_unit}")
        print(f"Coords : {pos_unit} (그대로 전달)")
        _cin, _ = parse_cell_from_in(in_text)
        if _cin is not None and cell is not None:
            _dv = abs(np.linalg.det(cell)) / abs(np.linalg.det(_cin)) - 1.0
            print(f"         입력 셀 대비 부피 {100*_dv:+.2f} %"
                  + ("  ← vc-relax 로 셀이 바뀌었다" if abs(_dv) > 1e-6 else ""))

    V = abs(np.linalg.det(cell))
    species = species_in_block(pos_block)
    print(f"Source: V={V:.4f} Å³, species={species}")
    print(f"Target: PAW kjpaw, extended basis (Li 1s2s2p, X 3s3p3d)")
    print(f"        nbnd={args.nbnd}, ecutwfc={args.ecutwfc}/ecutrho={args.ecutrho}")
    print(f"        K_POINTS automatic  {args.kpoints}   ← 카드가 박은 값과 대조할 것")

    # Build new SYSTEM with bumped ecut (PAW kjpaw needs higher cutoffs)
    nat = sum(1 for line in pos_block.strip().splitlines() if line.split())
    ntyp = len(species)
    system_lines = ["&SYSTEM",
                    "  ibrav=0",
                    f"  nat={nat}",
                    f"  ntyp={ntyp}",
                    f"  ecutwfc={args.ecutwfc}",
                    f"  ecutrho={args.ecutrho}",
                    "  occupations='smearing'",
                    "  smearing='mv'",
                    "  degauss=0.01",
                    "  nosym=.true.",
                    "/"]
    system_paw = "\n".join(system_lines)

    cell_lines = ["CELL_PARAMETERS angstrom"]
    for row in cell:
        cell_lines.append("  " + "  ".join(f"{x:14.10f}" for x in row))
    cell_card = "\n".join(cell_lines) + "\n"

    species_card = atomic_species_block(species, args.pseudo_dir)
    kpts = f"K_POINTS automatic\n  {args.kpoints}\n"
    pos_card = f"ATOMIC_POSITIONS ({pos_unit})\n{pos_block}"

    # === SCF ===
    scf_control = f"""&CONTROL
  calculation='scf'
  prefix='{args.prefix_base}_scf'
  pseudo_dir='{args.pseudo_dir}'
  outdir='./tmp_{args.prefix_base}_scf/'
  tprnfor=.true.
  tstress=.true.
  verbosity='high'
  wf_collect=.true.
/
"""
    electrons = "&ELECTRONS\n  conv_thr=1.0d-9\n  mixing_beta=0.3\n/\n"
    scf_in = (scf_control + "\n" + system_paw + "\n" + electrons + "\n"
              + species_card + "\n" + kpts + "\n" + cell_card + "\n"
              + pos_card + "\n")
    (wd / "lobster_scf.in").write_text(scf_in)

    # === NSCF (use SCF outdir, nbnd high, wf_collect, nosym) ===
    nscf_control = f"""&CONTROL
  calculation='nscf'
  prefix='{args.prefix_base}_scf'
  pseudo_dir='{args.pseudo_dir}'
  outdir='./tmp_{args.prefix_base}_scf/'
  tprnfor=.true.
  tstress=.true.
  verbosity='high'
  wf_collect=.true.
/
"""
    nscf_system = system_paw.replace("/", f"  nbnd={args.nbnd}\n/", 1)
    nscf_in = (nscf_control + "\n" + nscf_system + "\n" + electrons + "\n"
               + species_card + "\n" + kpts + "\n" + cell_card + "\n"
               + pos_card + "\n")
    (wd / "lobster_nscf.in").write_text(nscf_in)

    # === lobsterin (extended basis; species-aware since 2026-07-17 for O systems) ===
    # basis 는 **UPF 에서 읽어** 쓴다. 표에 박아둔 값은 못 읽었을 때만.
    #   basis 가 pseudo 의 valence 와 어긋나면 LOBSTER 가 에러를 내지 않고
    #   **charge spilling 만 올라간다** — 조용히 나쁜 결과가 된다.
    # ⛔⛔ **LOBSTER 기저는 QE 의 valence 와 다른 것이다.** 2026-09-10 에 한 번 섞었다:
    #   UPF 에서 읽은 valence 를 그대로 기저로 썼더니 P/S/Cl 이 `3s 3p` 가 되면서
    #   표의 `3s 3p 3d` (extended basis) 를 덮어버렸다. 그 3d 는 오타가 아니라
    #   **의도한 설계**다 — LOBSTER 는 평면파를 자기 국소 기저에 투영하므로 pseudo 에
    #   3d 채널이 없어도 빈 3d 기저를 넣을 수 있고, 그래야 분극 꼬리를 잡아
    #   charge spilling 이 내려간다.
    #   ⇒ 기저는 **표(curated extended)** 가 정본이다. UPF 읽기는 valence 를 **보고**
    #     하는 용도다 — 특히 Nd 의 4f 가 core 인지 valence 인지가 그 값으로 갈린다.
    #     표에 없는 원소(Nd)만 UPF 값을 기저로 쓴다.
    _CURATED = set(BASIS_FUNCS)
    basis_used, upf_seen = {}, {}
    for sp in species:
        lab = upf_valence_labels(Path(args.pseudo_dir) / PAW_PSEUDOS[sp])
        upf_seen[sp] = lab
        if sp in _CURATED and sp != "Nd":
            basis_used[sp] = (BASIS_FUNCS[sp], "표(extended)")
        elif lab:
            basis_used[sp] = (lab, "UPF")
        else:
            basis_used[sp] = (BASIS_FUNCS[sp], "표(대비값)")
    print("  LOBSTER basis (기저) · UPF valence (참고):")
    for sp in species:
        lab, src = basis_used[sp]
        u = upf_seen[sp] or "⚠ 못 읽음"
        mark = ""
        if sp == "Nd":
            mark = "  ← 4f **in valence**" if (upf_seen[sp] and "4f" in upf_seen[sp]) \
                   else "  ← 4f in core (frozen-4f 계산과 짝)"
        print(f"    {sp:3s} {lab:<20s} ({src})   valence={u}{mark}")
    basis_lines = "\n".join(f"basisfunctions  {sp:3s} {basis_used[sp][0]}" for sp in species)
    gens = ["cohpGenerator from 0.5 to 4.0 type Li type S",
            "cohpGenerator from 0.5 to 4.0 type Li type Cl",
            "cohpGenerator from 0.5 to 4.0 type P  type S",
            "cohpGenerator from 0.5 to 4.0 type S  type S"]
    if "Br" in species:
        gens += ["cohpGenerator from 0.5 to 4.0 type Li type Br"]
    if "O" in species:
        gens += ["cohpGenerator from 0.5 to 4.0 type P  type O",
                 "cohpGenerator from 0.5 to 4.0 type Li type O"]
    if "B" in species:
        # b2o3 의 핵심은 B-O 골격이다. B-S 도 넣는다 — 황화물 안에서 B 가 S 와
        # 결합하는지가 골격 creep 논의의 대상이었다 (md_run_ledger ★_VERDICT).
        gens += ["cohpGenerator from 0.5 to 3.0 type B  type O",
                 "cohpGenerator from 0.5 to 3.5 type B  type S",
                 "cohpGenerator from 0.5 to 4.0 type Li type B"]
    if "Nd" in species:
        # Nd 는 이완 후 6배위(S 5 + Cl 1, 2.68-2.98 Å)라 상한을 4.0 그대로 두면 충분하다.
        # P-Nd 도 넣는다 — 장부상 Nd 가 P 자리라 **정말 P 와 결합이 없는지**가 확인 대상이다.
        gens += ["cohpGenerator from 0.5 to 4.0 type Nd type S",
                 "cohpGenerator from 0.5 to 4.0 type Nd type Cl",
                 "cohpGenerator from 0.5 to 4.0 type Nd type O",
                 "cohpGenerator from 0.5 to 4.0 type Nd type P"]
    cobi_gens = [g.replace("cohpGenerator", "cobiGenerator") for g in gens]  # bond order (ICOBI)
    lobsterin = f"""COHPstartEnergy  -15
COHPendEnergy      8
COBIstartEnergy  -15
COBIendEnergy      8
basisSet         pbeVaspFit2015
gaussianSmearingWidth 0.02
skipDOS
skipPopulationAnalysis  False
skipMadelungEnergy
skipGrossPopulation

! Extended basis (target spilling < 5%)
{basis_lines}

! pCOHP (bond strength) + pCOBI (bond order)
""" + "\n".join(gens) + "\n" + "\n".join(cobi_gens) + "\n"
    (wd / "lobsterin").write_text(lobsterin)

    # === Runner ===
    runner = wd / "run_lobster.sh"
    runner.write_text(f"""#!/bin/bash
# Sequential SCF → NSCF → LOBSTER for {args.prefix_base}
set -e
cd $(dirname $(realpath $0))
export OMP_NUM_THREADS=8

# 1. SCF (PAW)
if [ -f lobster_scf.out ] && grep -q "JOB DONE" lobster_scf.out; then
    echo "[$(date +%H:%M:%S)] SCF: already done"
else
    echo "[$(date +%H:%M:%S)] SCF: START"
    T0=$(date +%s)
    mpirun --bind-to none -np 1 pw.x -inp lobster_scf.in > lobster_scf.out 2>&1
    DT=$(( $(date +%s) - T0 ))
    grep -q "JOB DONE" lobster_scf.out && echo "  ✓ SCF DONE in ${{DT}}s" \\
        || {{ echo "  ✗ SCF FAILED"; tail -10 lobster_scf.out; exit 1; }}
fi

# 2. NSCF (extended bands, wf_collect)
if [ -f lobster_nscf.out ] && grep -q "JOB DONE" lobster_nscf.out; then
    echo "[$(date +%H:%M:%S)] NSCF: already done"
else
    echo "[$(date +%H:%M:%S)] NSCF: START"
    T0=$(date +%s)
    mpirun --bind-to none -np 1 pw.x -inp lobster_nscf.in > lobster_nscf.out 2>&1
    DT=$(( $(date +%s) - T0 ))
    grep -q "JOB DONE" lobster_nscf.out && echo "  ✓ NSCF DONE in ${{DT}}s" \\
        || {{ echo "  ✗ NSCF FAILED"; tail -10 lobster_nscf.out; exit 1; }}
fi

# 3. LOBSTER (CPU)
if [ -f lobsterout ] && grep -q "finished in" lobsterout; then
    echo "[$(date +%H:%M:%S)] LOBSTER: already done"
else
    export PATH=/home/ubuntu/opt/lobster-5.1.1:$PATH
    which lobster >/dev/null || ln -sf /home/ubuntu/opt/lobster-5.1.1/lobster-5.1.1 \\
        /home/ubuntu/opt/lobster-5.1.1/lobster
    echo "[$(date +%H:%M:%S)] LOBSTER: START"
    T0=$(date +%s)
    lobster 2>&1 | tee lobster.log
    DT=$(( $(date +%s) - T0 ))
    echo "[$(date +%H:%M:%S)] LOBSTER DONE in ${{DT}}s"
    grep -E "spilling|recovered" lobsterout | head -4
fi

echo ""
echo "=== ALL DONE. Plot:"
echo "python3 /home/ubuntu/work/Yonghoon-DEM-DFT/tools/modelc_v3/plot_lobster_4panel.py \\\\"
echo "    --lobster_dir . --out_png V0_COHP_4panel_ext.png"
""")
    runner.chmod(0o755)

    print(f"\n→ {wd}/lobster_scf.in")
    print(f"→ {wd}/lobster_nscf.in")
    print(f"→ {wd}/lobsterin")
    print(f"→ {wd}/run_lobster.sh")
    print(f"\nRun: bash {wd}/run_lobster.sh")


if __name__ == "__main__":
    import sys as _s0
    if "--selftest" in _s0.argv:
        raise SystemExit(_selftest())
    main()
