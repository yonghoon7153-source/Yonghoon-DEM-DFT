#!/usr/bin/env python3
"""splice_relaxed.py — vc-relax 최종 셀·좌표를 하류 입력에 **덮어쓴다**.

왜 필요한가
  vc-relax 로 이완해 놓고 scf/nscf 를 원래 MP 기하로 돌리면 이완이 무의미해진다.
  QE 는 vc-relax 뒤 `Begin final coordinates … End final coordinates` 블록을 찍으므로
  거기서 CELL_PARAMETERS 와 ATOMIC_POSITIONS 를 떼어 목표 입력에 스플라이스한다.

⚠ 블록이 불완전하면(중단된 vc-relax) **덮어쓰지 않고 실패로 끝낸다** — 반쪽 기하를
  조용히 쓰는 것이 제일 나쁘다.

고정셀 relax (2026-08-12 추가)
  `calculation='relax'` 는 셀이 안 변하니 CELL_PARAMETERS 를 **안 찍는다**. vc-relax 만
  상정한 옛 코드는 그 출력에서 항상 실패했다 — `--positions_only` 로 좌표만 승계한다.
  (NEB 끝점 이완 → k/degauss 사다리 scf 로 기하를 넘길 때 쓴다.)

  python3 splice_relaxed.py --out 01_vcrelax.out --targets 02_scf.in 03_nscf_gap.in
  python3 splice_relaxed.py --out relax.out --targets scf.in --positions_only
  python3 splice_relaxed.py --selftest

이 도구가 **못 하는 것**
  · 두 입력이 같은 계인지 확인하지 못한다 — 원자 수만 맞으면 덮어쓴다.
  · ATOMIC_SPECIES/전하/자기 시드는 안 건드린다 (좌표·셀만).
"""
import argparse, os, re, sys


def final_blocks(txt, nat, need_cell=True):
    """최종 기하 블록 → (cell, pos). 못 읽으면 (None, None).

    ⚠ 고정셀 `calculation='relax'` 는 CELL_PARAMETERS 를 **안 찍는다** (셀이 안 변하니까).
      vc-relax 만 상정하면 그 경우 항상 실패한다 — need_cell=False 로 좌표만 승계한다.
      셀은 원래 입력 것을 그대로 두는 게 맞다(같은 셀이므로).
    """
    i = txt.rfind("Begin final coordinates")
    if i < 0:
        return None, None
    j = txt.find("End final coordinates", i)
    blk = txt[i:j if j > 0 else len(txt)]
    mc = re.search(r"CELL_PARAMETERS\s*\(?(\w+)[^\n]*\n((?:[^\n]*\n){3})", blk)
    ma = re.search(r"ATOMIC_POSITIONS\s*\(?(\w+)", blk)
    if not ma or (need_cell and not mc):
        return None, None
    lines = blk[ma.end():].splitlines()
    pos = [l for l in lines if l.split() and re.match(r"^[A-Za-z]", l.split()[0])][:nat]
    if len(pos) != nat:
        return None, None
    return ((mc.group(1), mc.group(2)) if mc else ("", "")), (ma.group(1), pos)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--targets", nargs="+")
    ap.add_argument("--positions_only", action="store_true",
                    help="고정셀 relax — 좌표만 승계하고 CELL_PARAMETERS 는 건드리지 않는다")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.out or not a.targets:
        sys.exit("⛔ --out 과 --targets 가 필요하다 (또는 --selftest)")
    txt = open(a.out, errors="ignore").read()
    m = re.search(r"number of atoms/cell\s*=\s*(\d+)", txt)
    if not m:
        sys.exit("⛔ 원자 수를 못 읽었다")
    nat = int(m.group(1))
    cell, pos = final_blocks(txt, nat, need_cell=not a.positions_only)
    if cell is None:
        sys.exit("⛔ 'Begin final coordinates' 블록이 없거나 불완전하다 — "
                 "이완이 안 끝났다. 반쪽 기하를 쓰지 않고 중단한다."
                 + ("" if a.positions_only else
                    "\n   (고정셀 relax 면 CELL_PARAMETERS 가 없는 게 정상이다 "
                    "— --positions_only 를 줄 것)"))
    cu, cb = cell; pu, pl = pos
    missing = []
    for t in a.targets:
        # ⛔ 2026-08-11 자체검토 P0-2 — 없는 타깃에서 FileNotFoundError 로 죽으면
        #   러너의 `|| continue` 가 **그 상 전체를 01 직후 포기**한다. metal 상은
        #   03(갭) 입력을 일부러 안 만들므로(build_dft_inputs) 정확히 이 경로를 탄다.
        #   그러면 04~06(DOS/PDOS)이 안 돌고, 금속 확인 단계가 코드로 도달 불가해진다.
        #   ⚠ 더 나쁜 건 02 는 이미 승계되고 04 는 안 된 **부분 승계** 상태로 남는 것이다.
        if not os.path.isfile(t):
            missing.append(t)
            print(f"  ⏭ {t} 없음 — 건너뜀 (electronic_class=metal 이면 정상이다)")
            continue
        s = open(t).read()
        ncell = 0
        if cu:
            s, ncell = re.subn(r"CELL_PARAMETERS[^\n]*\n(?:[^\n]*\n){3}",
                               f"CELL_PARAMETERS {cu}\n{cb}", s, count=1)
        s, npos = re.subn(r"ATOMIC_POSITIONS[^\n]*\n(?:\s*[A-Za-z][^\n]*\n){%d}" % nat,
                          f"ATOMIC_POSITIONS {pu}\n" + "\n".join(pl) + "\n", s, count=1)
        # ⛔ 좌표 치환이 0건인데 "승계함" 이라고 말하면 안 된다 (조용한 무동작).
        #   셀만 바뀌고 좌표가 안 바뀌면 **원래 기하에 새 셀** 이라 더 나쁘다.
        if npos != 1:
            sys.exit(f"⛔ {t}: ATOMIC_POSITIONS {nat}줄 블록을 못 찾았다 (치환 {npos}건) "
                     f"— 원자 수/형식이 다르다. 승계했다고 보고하지 않고 중단한다."
                     + (" ⚠ 셀은 이미 바뀌었을 수 있으니 타깃을 다시 만들 것."
                        if ncell else ""))
        open(t, "w").write(s)
        print(f"  기하 승계 → {t}" + ("" if cu else " (좌표만 · 셀 유지)"))
    if missing:
        print(f"  ⚠ 승계 안 한 타깃 {len(missing)}개: {', '.join(missing)}")
    return 0


def selftest():
    """양성 2 + **음성 4**. 조용한 무동작이 제일 나쁜 실패라 그것부터 잡는다."""
    import subprocess, tempfile
    td = tempfile.mkdtemp(prefix="splice_st_")
    ok = True

    def chk(cond, msg):
        nonlocal ok
        print(("  ✓ " if cond else "  ✗ ") + msg)
        ok &= bool(cond)

    NAT = 2
    POS = "  Li      0.1000000000     0.2000000000     0.3000000000\n" \
          "  Nd      0.6000000000     0.7000000000     0.8000000000\n"
    TGT = ("&control\n/\nCELL_PARAMETERS angstrom\n  9 0 0\n  0 9 0\n  0 0 9\n"
           "ATOMIC_POSITIONS angstrom\n"
           "  Li      0.0000000000     0.0000000000     0.0000000000\n"
           "  Nd      0.5000000000     0.5000000000     0.5000000000\n")
    HEAD = f"     number of atoms/cell      =            {NAT}\n"

    def run(out_txt, tgt_txt, extra=()):
        d = tempfile.mkdtemp(dir=td)
        o, t = os.path.join(d, "r.out"), os.path.join(d, "t.in")
        open(o, "w").write(out_txt)
        open(t, "w").write(tgt_txt)
        r = subprocess.run([sys.executable, __file__, "--out", o, "--targets", t,
                            *extra], capture_output=True, text=True)
        return r, open(t).read()

    vc = HEAD + ("Begin final coordinates\nCELL_PARAMETERS (angstrom)\n"
                 "  8 0 0\n  0 8 0\n  0 0 8\n"
                 f"ATOMIC_POSITIONS (angstrom)\n{POS}End final coordinates\n")
    r, got = run(vc, TGT)
    chk(r.returncode == 0 and "8 0 0" in got and "0.1000000000" in got,
        "vc-relax: 셀+좌표 승계")
    # 고정셀 relax — CELL_PARAMETERS 가 없다 (QE 가 안 찍는다)
    fx = HEAD + ("Begin final coordinates\n"
                 f"ATOMIC_POSITIONS (angstrom)\n{POS}End final coordinates\n")
    r, got = run(fx, TGT, ["--positions_only"])
    chk(r.returncode == 0 and "0.1000000000" in got and "  9 0 0" in got,
        "고정셀 relax + --positions_only: 좌표만 승계 · 셀 유지")
    # 음성 ①: 같은 입력을 --positions_only 없이 → 거부해야 한다
    r, got = run(fx, TGT)
    chk(r.returncode != 0 and "0.1000000000" not in got,
        "고정셀인데 플래그 없음 → 거부 (타깃 무변경)")
    # 음성 ②: 블록 자체가 없다 (이완 미완)
    r, got = run(HEAD + "still running...\n", TGT)
    chk(r.returncode != 0 and "0.1000000000" not in got, "블록 없음 → 거부")
    # 음성 ③: 좌표가 원자 수보다 적다 (중단된 출력)
    half = HEAD + ("Begin final coordinates\nCELL_PARAMETERS (angstrom)\n"
                   "  8 0 0\n  0 8 0\n  0 0 8\nATOMIC_POSITIONS (angstrom)\n"
                   "  Li      0.1 0.2 0.3\n")
    r, got = run(half, TGT)
    chk(r.returncode != 0 and "  9 0 0" in got, "좌표 절단 → 거부 (셀도 안 건드림)")
    # 음성 ④: 타깃 원자 수가 달라 치환이 0건 — "승계했다" 고 말하면 안 된다
    tgt3 = TGT.replace("  Nd      0.5000000000     0.5000000000     0.5000000000\n", "")
    r, got = run(vc, tgt3)
    chk(r.returncode != 0 and "못 찾았다" in (r.stdout + r.stderr),
        "타깃 원자 수 불일치 → 조용한 무동작 대신 실패")
    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
