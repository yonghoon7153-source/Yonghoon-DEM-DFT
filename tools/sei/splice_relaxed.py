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

미수렴 relax 이어달리기 (2026-08-16 추가)
  BFGS 가 nstep 을 소진하거나 trust radius 가 무너지면 QE 는 `Begin final coordinates`
  를 **안 찍는다**. 그러면 위 경로는 (옳게) 거부하지만 **재시작 기하가 없어진다** —
  cc333 끝점이 정확히 그 상태였다(힘 0.018 Ry/au 에서 정체, 최종 블록 없음).
  `--allow_unconverged` 는 마지막 `ATOMIC_POSITIONS` 스텝 블록으로 후퇴한다.
  다만 **조용히 하지 않는다**: 마지막 Total force 를 찍고, 승계한 타깃마다
  `! carried-from-unconverged` 주석을 박고, 사이드카 JSON 에 근거를 남긴다.

  python3 splice_relaxed.py --out relax.out --targets relax2.in \
      --positions_only --allow_unconverged

이 도구가 **못 하는 것**
  · 두 입력이 같은 계인지 확인하지 못한다 — 원자 수만 맞으면 덮어쓴다.
  · ATOMIC_SPECIES/전하/자기 시드는 안 건드린다 (좌표·셀만).
  · `--allow_unconverged` 로 가져온 기하가 **수렴에 가깝다고 보증하지 않는다.**
    힘이 발산 중이어도 마지막 스텝을 그대로 준다 — 힘 값을 보고 사람이 판단할 것.
  · 미수렴 vc-relax 의 **셀**은 승계하지 않는다 (스텝 중 CELL_PARAMETERS 를 매번
    찍지 않는 빌드가 있어 좌표-셀 짝이 깨질 수 있다). 그 경우 --positions_only 를 쓸 것.
"""
import argparse, json, os, re, sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

CARRY_MARK = "! carried-from-unconverged"


def last_total_force(txt):
    """마지막 `Total force = X` (Ry/au). 없으면 None."""
    m = re.findall(r"Total force\s*=\s*([-\d.Ee+]+)", txt)
    try:
        return float(m[-1]) if m else None
    except ValueError:
        return None


def final_blocks(txt, nat, need_cell=True, allow_unconverged=False):
    """최종 기하 블록 → (cell, pos, provenance). 못 읽으면 (None, None, why).

    ⚠ 고정셀 `calculation='relax'` 는 CELL_PARAMETERS 를 **안 찍는다** (셀이 안 변하니까).
      vc-relax 만 상정하면 그 경우 항상 실패한다 — need_cell=False 로 좌표만 승계한다.
      셀은 원래 입력 것을 그대로 두는 게 맞다(같은 셀이므로).

    ⚠ allow_unconverged 는 **최종 블록이 없을 때만** 스텝 블록으로 후퇴한다.
      최종 블록이 있으면 언제나 그쪽이 이긴다 (미수렴 후퇴가 정상 경로를 가리면 안 된다).
    """
    def parse(blk):
        mc = re.search(r"CELL_PARAMETERS\s*\(?(\w+)[^\n]*\n((?:[^\n]*\n){3})", blk)
        ma = re.search(r"ATOMIC_POSITIONS\s*\(?(\w+)", blk)
        if not ma:
            return None, None
        lines = blk[ma.end():].splitlines()
        pos = [l for l in lines if l.split() and re.match(r"^[A-Za-z]", l.split()[0])][:nat]
        if len(pos) != nat:
            return None, None
        return (mc.group(1), mc.group(2)) if mc else ("", ""), (ma.group(1), pos)

    i = txt.rfind("Begin final coordinates")
    if i >= 0:
        j = txt.find("End final coordinates", i)
        cell, pos = parse(txt[i:j if j > 0 else len(txt)])
        if pos is not None and not (need_cell and not cell[0]):
            return cell, pos, {"source": "final_coordinates", "converged": True}
        return None, None, {"why": "final_block_incomplete"}

    if not allow_unconverged:
        return None, None, {"why": "no_final_block"}

    # 후퇴: 마지막 ATOMIC_POSITIONS 스텝 블록. 셀은 절대 승계하지 않는다.
    if need_cell:
        return None, None, {"why": "unconverged_cell_carry_refused"}
    k = txt.rfind("ATOMIC_POSITIONS")
    if k < 0:
        return None, None, {"why": "no_step_block"}
    cell, pos = parse(txt[k:])
    if pos is None:
        return None, None, {"why": "step_block_truncated"}
    n_steps = len(re.findall(r"^ATOMIC_POSITIONS", txt, flags=re.M))
    return ("", ""), pos, {"source": "last_step_block", "converged": False,
                           "n_position_blocks": n_steps,
                           "last_total_force_Ry_au": last_total_force(txt)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--targets", nargs="+")
    ap.add_argument("--positions_only", action="store_true",
                    help="고정셀 relax — 좌표만 승계하고 CELL_PARAMETERS 는 건드리지 않는다")
    ap.add_argument("--allow_unconverged", action="store_true",
                    help="최종 블록이 없으면 **마지막 스텝** 좌표로 후퇴한다 (재시작용). "
                         "--positions_only 와 같이 써야 한다. 근거를 사이드카에 남긴다")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.out or not a.targets:
        sys.exit("⛔ --out 과 --targets 가 필요하다 (또는 --selftest)")
    if a.allow_unconverged and not a.positions_only:
        sys.exit("⛔ --allow_unconverged 는 --positions_only 와 같이 써야 한다 "
                 "— 미수렴 출력에서 셀은 승계하지 않는다 (좌표-셀 짝이 깨질 수 있다)")
    txt = open(a.out, errors="ignore").read()
    m = re.search(r"number of atoms/cell\s*=\s*(\d+)", txt)
    if not m:
        sys.exit("⛔ 원자 수를 못 읽었다")
    nat = int(m.group(1))
    cell, pos, prov = final_blocks(txt, nat, need_cell=not a.positions_only,
                                   allow_unconverged=a.allow_unconverged)
    if cell is None:
        why = prov.get("why", "")
        sys.exit("⛔ 'Begin final coordinates' 블록이 없거나 불완전하다 — "
                 "이완이 안 끝났다. 반쪽 기하를 쓰지 않고 중단한다."
                 + ("" if a.positions_only else
                    "\n   (고정셀 relax 면 CELL_PARAMETERS 가 없는 게 정상이다 "
                    "— --positions_only 를 줄 것)")
                 + ("\n   (재시작 기하만 필요하면 --positions_only --allow_unconverged)"
                    if why == "no_final_block" and a.positions_only else "")
                 + (f"\n   why={why}" if why else ""))
    if not prov.get("converged", True):
        f = prov.get("last_total_force_Ry_au")
        print(f"⚠ **미수렴 기하 승계** — 최종 블록이 없어 {prov['n_position_blocks']}번째 "
              f"스텝 좌표를 쓴다. 마지막 Total force = "
              + (f"{f:.6f} Ry/au" if f is not None else "읽지 못함")
              + " (수렴 문턱 통상 1e-3). 이 기하는 **재시작용**이고 결과가 아니다.")
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
        # 미수렴 승계는 **파일 안에** 표시를 남긴다 — 사이드카만 두면 입력만 보고는 못 안다.
        if not prov.get("converged", True) and CARRY_MARK not in s:
            f = prov.get("last_total_force_Ry_au")
            s = (f"{CARRY_MARK} from {os.path.abspath(a.out)} "
                 f"(step {prov.get('n_position_blocks')}, last Total force "
                 + (f"{f:.6f}" if f is not None else "?") + " Ry/au)\n") + s
        open(t, "w").write(s)
        print(f"  기하 승계 → {t}" + ("" if cu else " (좌표만 · 셀 유지)")
              + ("" if prov.get("converged", True) else "  ⚠ 미수렴"))
    if missing:
        print(f"  ⚠ 승계 안 한 타깃 {len(missing)}개: {', '.join(missing)}")
    if not prov.get("converged", True):
        side = os.path.splitext(a.out)[0] + "_carry.json"
        with open(side, "w", encoding="utf-8") as fh:
            json.dump({"source_out": os.path.abspath(a.out),
                       "targets": [os.path.abspath(t) for t in a.targets
                                   if t not in missing],
                       "converged": False, **prov,
                       "caveat": ("미수렴 relax 의 마지막 스텝 좌표다. 재시작 입력으로만 "
                                  "쓸 것 — 결과·인용에 쓰면 안 된다.")}, fh,
                      indent=1, ensure_ascii=False)
        print(f"  근거 → {side}")
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

    # ── --allow_unconverged (2026-08-16) — 미수렴 relax 이어달리기 ────────────
    # QE 가 nstep 을 소진하면 최종 블록 없이 스텝 블록만 남는다 (cc333 끝점의 실제 형태).
    STEP = (HEAD
            + "ATOMIC_POSITIONS (angstrom)\n"
              "  Li      0.0100000000     0.0200000000     0.0300000000\n"
              "  Nd      0.5100000000     0.5200000000     0.5300000000\n"
              "     Total force =     0.050000     Total SCF correction =     0.000010\n"
            + f"ATOMIC_POSITIONS (angstrom)\n{POS}"
              "     Total force =     0.018042     Total SCF correction =     0.000012\n"
              "     End of BFGS Geometry Optimization\n")
    r, got = run(STEP, TGT, ["--positions_only", "--allow_unconverged"])
    chk(r.returncode == 0 and "0.1000000000" in got,
        "미수렴: 마지막 스텝 좌표 승계")
    chk("0.0100000000" not in got, "미수렴: 첫 스텝이 아니라 **마지막** 스텝을 쓴다")
    chk(CARRY_MARK in got, "미수렴: 타깃 파일에 표식이 박힌다")
    chk("0.018042" in (r.stdout + got), "미수렴: 마지막 Total force 를 보고한다")
    # 음성 ⑤: 플래그 없으면 여전히 거부 (기본 경로가 느슨해지면 안 된다)
    r, got = run(STEP, TGT, ["--positions_only"])
    chk(r.returncode != 0 and "0.1000000000" not in got,
        "음성: --allow_unconverged 없으면 미수렴 출력은 거부")
    # 음성 ⑥: --positions_only 없이 --allow_unconverged → 셀 승계 위험이라 거부
    r, got = run(STEP, TGT, ["--allow_unconverged"])
    chk(r.returncode != 0 and "0.1000000000" not in got,
        "음성: --allow_unconverged 단독 사용 거부 (셀 짝 깨짐)")
    # 음성 ⑦: 최종 블록이 있으면 스텝 블록으로 후퇴하지 않는다 (정상 경로 우선)
    both = (HEAD
            + "ATOMIC_POSITIONS (angstrom)\n"
              "  Li      0.9900000000     0.9800000000     0.9700000000\n"
              "  Nd      0.9600000000     0.9500000000     0.9400000000\n"
            + f"Begin final coordinates\nATOMIC_POSITIONS (angstrom)\n{POS}"
              "End final coordinates\n")
    r, got = run(both, TGT, ["--positions_only", "--allow_unconverged"])
    chk(r.returncode == 0 and "0.1000000000" in got and "0.9900000000" not in got,
        "음성: 최종 블록이 있으면 그쪽이 이긴다")
    chk(CARRY_MARK not in got, "음성: 수렴본에 미수렴 표식을 달지 않는다")
    # 음성 ⑧: 스텝 블록이 잘려 있으면 (원자 수 부족) 거부
    trunc = HEAD + "ATOMIC_POSITIONS (angstrom)\n  Li      0.1 0.2 0.3\n"
    r, got = run(trunc, TGT, ["--positions_only", "--allow_unconverged"])
    chk(r.returncode != 0 and "0.1000000000" not in got, "음성: 잘린 스텝 블록 → 거부")
    # 음성 ⑨: ATOMIC_POSITIONS 가 아예 없으면 거부
    r, got = run(HEAD + "     Total force =     0.5\n", TGT,
                 ["--positions_only", "--allow_unconverged"])
    chk(r.returncode != 0, "음성: 스텝 블록 자체가 없으면 거부")
    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
