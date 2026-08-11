#!/usr/bin/env python3
"""splice_relaxed.py — vc-relax 최종 셀·좌표를 하류 입력에 **덮어쓴다**.

왜 필요한가
  vc-relax 로 이완해 놓고 scf/nscf 를 원래 MP 기하로 돌리면 이완이 무의미해진다.
  QE 는 vc-relax 뒤 `Begin final coordinates … End final coordinates` 블록을 찍으므로
  거기서 CELL_PARAMETERS 와 ATOMIC_POSITIONS 를 떼어 목표 입력에 스플라이스한다.

⚠ 블록이 불완전하면(중단된 vc-relax) **덮어쓰지 않고 실패로 끝낸다** — 반쪽 기하를
  조용히 쓰는 것이 제일 나쁘다.

  python3 splice_relaxed.py --out 01_vcrelax.out --targets 02_scf.in 03_nscf_gap.in
"""
import argparse, os, re, sys


def final_blocks(txt, nat):
    i = txt.rfind("Begin final coordinates")
    if i < 0:
        return None, None
    j = txt.find("End final coordinates", i)
    blk = txt[i:j if j > 0 else len(txt)]
    mc = re.search(r"CELL_PARAMETERS\s*\(?(\w+)[^\n]*\n((?:[^\n]*\n){3})", blk)
    ma = re.search(r"ATOMIC_POSITIONS\s*\(?(\w+)", blk)
    if not mc or not ma:
        return None, None
    lines = blk[ma.end():].splitlines()
    pos = [l for l in lines if l.split() and re.match(r"^[A-Za-z]", l.split()[0])][:nat]
    if len(pos) != nat:
        return None, None
    return (mc.group(1), mc.group(2)), (ma.group(1), pos)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--targets", nargs="+", required=True)
    a = ap.parse_args()
    txt = open(a.out, errors="ignore").read()
    m = re.search(r"number of atoms/cell\s*=\s*(\d+)", txt)
    if not m:
        sys.exit("⛔ 원자 수를 못 읽었다")
    nat = int(m.group(1))
    cell, pos = final_blocks(txt, nat)
    if cell is None:
        sys.exit("⛔ 'Begin final coordinates' 블록이 없거나 불완전하다 — "
                 "vc-relax 가 안 끝났다. 반쪽 기하를 쓰지 않고 중단한다.")
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
        s = re.sub(r"CELL_PARAMETERS[^\n]*\n(?:[^\n]*\n){3}",
                   f"CELL_PARAMETERS {cu}\n{cb}", s, count=1)
        s = re.sub(r"ATOMIC_POSITIONS[^\n]*\n(?:\s*[A-Za-z][^\n]*\n){%d}" % nat,
                   f"ATOMIC_POSITIONS {pu}\n" + "\n".join(pl) + "\n", s, count=1)
        open(t, "w").write(s)
        print(f"  기하 승계 → {t}")
    if missing:
        print(f"  ⚠ 승계 안 한 타깃 {len(missing)}개: {', '.join(missing)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
