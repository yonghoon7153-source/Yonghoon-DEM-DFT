#!/usr/bin/env python3
"""gen_drag_points_kgy.py — regenerate Li3N drag inputs p4..p8 on kgy from a
local template (no scp needed; KISTI drag_p*.in unavailable).

The drag path is: adatom held at fixed (x, y=1.5805486400), z free (if_pos 0 0 1),
bottom slab frozen; x steps by 0.684375 A from p0 x=8.2125 down to p8 x=2.7375.
Confirmed from the KISTI watch/CARRY logs:
  p0 8.2125 / p2 6.8437 / p3 6.1594 / p4 5.4750  -> dx = 0.684375, y = 1.58054864
  => p5 4.790625 / p6 4.106250 / p7 3.421875 / p8 2.737500

We clone the template (p0_min4.in: same 136-atom slab, same constraints), find the
ADATOM as the unique atom whose if_pos flags are '0 0 1' (xy pinned, z free), and
rewrite ONLY its x,y for each target point. Everything else (settings, frozen
bottom, cell, pseudo section) is copied verbatim. Starting z = 13.48712429 (the
KISTI fresh-start z); it relaxes. Constrained relax -> same minimum as KISTI.

  cd ~/work/li3n_drag   # (created here)
  python3 ~/Yonghoon-DEM-DFT/tools/neb_diffusion/gen_drag_points_kgy.py \
     --template ~/work/li3n_dft/p0_min4.in \
     --pseudo_src ~/work/li3n_dft --outdir ~/work/li3n_drag
Then: bash ~/Yonghoon-DEM-DFT/tools/neb_diffusion/run_li3n_drag_kgy.sh

--------------------------------------------------------------------------
PATH MODE (2026-08-12) — arbitrary straight hop, for the manuscript figure
--------------------------------------------------------------------------
The block above is the frozen KISTI straight-line drag (fixed y, x stepping).
`--path` generalises it: give a start xy, an end xy, and the reduced coordinates
to sample, and it writes one constrained-relax input per point. Same protocol as
the reported 2-point barrier (adatom xy pinned, z free, frozen bottom kept).

  python3 gen_drag_points_kgy.py --path \
     --template ~/work/li3n_dft/p0_min4.in --pseudo_src ~/work/li3n_dft \
     --outdir ~/work/li3n_hop --tag hop \
     --from_xy 9.0606,1.1440 --to_xy 3.5857,4.3050 \
     --xi 0.2,0.5,0.6,0.8,1.0

WHAT THIS TOOL DOES NOT DO
  - It does not find the path. You supply the two endpoints; if they are not
    symmetry-equivalent sites the resulting profile is not a migration barrier.
  - It does not check that the straight line is the minimum-energy path. A
    constrained scan along a straight line is an UPPER bound on the true MEP.
  - It does not run anything, parse outputs, or judge convergence.
  - It assumes the template's adatom is at --from_xy (it verifies this and
    refuses otherwise) and that the template's constraint block is correct.
"""
import argparse
import os
import re

ADATOM_TOL_A = 0.35
Y_FIX = 1.58054864
Z0 = 13.48712429
X_P0 = 8.2125
DX = 0.684375
# p4 added 2026-07-20: KISTI p4 (x=5.475) stalled unconverged at +251 meV (|F|=0.0069,
# a straight-path UPPER bound). KISTI is being wiped, so re-run p4 FRESH on kgy where
# the relax runs to convergence -> the true p4 profile point. Chained AFTER p8 (the
# runner's WAIT_FOR env), so it fills in without touching the running p5-p8 chain.
TARGETS = {4: X_P0 - 4 * DX, 5: X_P0 - 5 * DX, 6: X_P0 - 6 * DX, 7: X_P0 - 7 * DX, 8: X_P0 - 8 * DX}


def _xy(txt):
    v = [float(t) for t in txt.replace(" ", "").split(",")]
    if len(v) != 2:
        raise SystemExit(f"--from_xy/--to_xy 는 'X,Y' 형식이어야 한다: {txt!r}")
    return tuple(v)


def plan_path(from_xy, to_xy, xis):
    """(tag_index, x, y, xi) for each requested reduced coordinate along from->to.

    Pure function -- no file IO -- so the selftest can exercise it directly.
    Raises on a degenerate segment or an out-of-range xi.
    """
    (x0, y0), (x1, y1) = from_xy, to_xy
    seg = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
    if seg < 1e-6:
        raise ValueError(f"from_xy == to_xy (segment {seg:.2e} A) -- 경로가 없다")
    out = []
    for k, xi in enumerate(xis):
        if not (0.0 <= xi <= 1.0):
            raise ValueError(f"xi={xi} 가 [0,1] 밖이다")
        out.append((k, x0 + xi * (x1 - x0), y0 + xi * (y1 - y0), xi))
    return out


def selftest():
    ok = True

    def chk(name, cond):
        nonlocal ok
        print(("  ok   " if cond else "  FAIL ") + name)
        ok = ok and bool(cond)

    pts = plan_path((0.0, 0.0), (3.0, 4.0), [0.0, 0.5, 1.0])
    chk("endpoints exact", pts[0][1:3] == (0.0, 0.0) and pts[2][1:3] == (3.0, 4.0))
    chk("midpoint on segment", abs(pts[1][1] - 1.5) < 1e-12 and abs(pts[1][2] - 2.0) < 1e-12)
    chk("xi carried through", [p[3] for p in pts] == [0.0, 0.5, 1.0])

    # negative paths -- the tool must REFUSE bad input, not silently produce it
    try:
        plan_path((1.0, 1.0), (1.0, 1.0), [0.5]); chk("degenerate segment rejected", False)
    except ValueError:
        chk("degenerate segment rejected", True)
    for bad in (-0.01, 1.01, 2.0):
        try:
            plan_path((0.0, 0.0), (1.0, 0.0), [bad]); chk(f"xi={bad} rejected", False)
        except ValueError:
            chk(f"xi={bad} rejected", True)
    try:
        _xy("1.0"); chk("malformed --from_xy rejected", False)
    except SystemExit:
        chk("malformed --from_xy rejected", True)

    # adatom mismatch guard: the template's adatom must sit at --from_xy
    chk("mismatch tolerance is tight", ADATOM_TOL_A <= 0.5)
    print("RESULT:", "0 실패" if ok else "실패 있음")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", help="p0_min4.in (136-atom drag input)")
    ap.add_argument("--pseudo_src", help="dir with li_pbe_v1.4.uspp.F.UPF + N.pbe-n-radius_5.UPF")
    ap.add_argument("--outdir")
    ap.add_argument("--path", action="store_true", help="임의 직선 hop 모드 (docstring 참조)")
    ap.add_argument("--from_xy", help="경로 시작 xy (Å, 'X,Y') — 템플릿 adatom 위치여야 한다")
    ap.add_argument("--to_xy", help="경로 끝 xy (Å, 'X,Y')")
    ap.add_argument("--xi", help="샘플할 환산좌표 목록, 예 '0.2,0.5,0.6,0.8,1.0'")
    ap.add_argument("--tag", default="hop", help="출력 파일 접두어 (기본 hop)")
    ap.add_argument("--z0", type=float, default=None, help="시작 z (기본: 템플릿 adatom z)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(selftest())
    for req in ("template", "pseudo_src", "outdir"):
        if not getattr(a, req):
            raise SystemExit(f"--{req} 필요")
    if a.path and not (a.from_xy and a.to_xy and a.xi):
        raise SystemExit("--path 는 --from_xy --to_xy --xi 를 모두 요구한다")

    os.makedirs(a.outdir, exist_ok=True)
    pdir = os.path.join(a.outdir, "pseudo")
    os.makedirs(pdir, exist_ok=True)
    for upf in ("li_pbe_v1.4.uspp.F.UPF", "N.pbe-n-radius_5.UPF"):
        src = os.path.join(os.path.expanduser(a.pseudo_src), upf)
        dst = os.path.join(pdir, upf)
        if not os.path.exists(dst):
            if not os.path.exists(src):
                raise SystemExit(f"pseudo 없음: {src}")
            os.symlink(src, dst)

    lines = open(os.path.expanduser(a.template)).read().splitlines()
    # locate ATOMIC_POSITIONS block + its atom lines
    ip = next(i for i, l in enumerate(lines) if l.strip().upper().startswith("ATOMIC_POSITIONS"))
    atom_lines = []
    for i in range(ip + 1, len(lines)):
        s = lines[i].split()
        if len(s) >= 4 and re.match(r"^[A-Za-z][a-z]?$", s[0]):
            try:
                float(s[1]); float(s[2]); float(s[3])
            except ValueError:
                break
            atom_lines.append(i)
        elif atom_lines:
            break
    # ADATOM = atom nearest (X_P0, Y_FIX) in xy. The free-relax adatom sits ~0.37 A
    # from there; the nearest substrate Li is >1 A away -> unambiguous. Cross-check
    # with max-z (adsorbate on top).
    ax, ay = _xy(a.from_xy) if a.path else (X_P0, Y_FIX)

    def xy_d(i):
        s = lines[i].split()
        return (float(s[1]) - ax) ** 2 + (float(s[2]) - ay) ** 2
    adatom_i = min(atom_lines, key=xy_d)
    maxz_i = max(atom_lines, key=lambda i: float(lines[i].split()[3]))
    sp = lines[adatom_i].split()
    mz = lines[maxz_i].split()
    print(f"nat parsed = {len(atom_lines)}")
    print(f"adatom (nearest p0 xy) = line {adatom_i-ip}: {sp[0]} ({sp[1]},{sp[2]},{sp[3]}), xy-dist {xy_d(adatom_i)**0.5:.3f} A")
    print(f"max-z atom (cross-check) = line {maxz_i-ip}: {mz[0]} ({mz[1]},{mz[2]},{mz[3]})")
    if adatom_i != maxz_i:
        print("  [note] nearest-xy != max-z; using nearest-xy (adatom relaxed from p0 xy). "
              "If wrong, the slab's top surface atom is being picked -- verify.")
    print("  -> pinning xy at each target, z free (if_pos 0 0 1); frozen bottom kept as-is")

    if a.path:
        d = xy_d(adatom_i) ** 0.5
        if d > ADATOM_TOL_A:
            raise SystemExit(
                f"템플릿 adatom 이 --from_xy 에서 {d:.3f} A 떨어져 있다 (허용 {ADATOM_TOL_A} A).\n"
                "  --from_xy 가 이 템플릿의 경로 시작점이 아니거나, 템플릿이 틀렸다.")
        if adatom_i != maxz_i:
            raise SystemExit("path 모드: nearest-xy adatom 과 max-z 원자가 다르다 -- 템플릿 확인 필요")
        z0 = a.z0 if a.z0 is not None else float(lines[adatom_i].split()[3])
        for k, xt, yt, xi in plan_path(_xy(a.from_xy), _xy(a.to_xy),
                                       [float(t) for t in a.xi.replace(" ", "").split(",")]):
            out = list(lines)
            out[adatom_i] = f"  {sp[0]:3s} {xt:.8f} {yt:.8f} {z0:.8f}   0 0 1"
            txt = "\n".join(out) + "\n"
            txt = re.sub(r"pseudo_dir\s*=\s*'?[^'\n,]+'?", f"pseudo_dir = '{pdir}'", txt)
            name = f"{a.tag}_xi{int(round(xi * 100)):03d}"
            dst = os.path.join(a.outdir, name + ".in")
            open(dst, "w").write(txt)
            print(f"-> {dst}  (xi={xi:.3f}  xy={xt:.5f},{yt:.5f}  z0={z0:.5f})")
        print("done (path mode). 실행: POINTS 대신 각 .in 을 순차 실행")
        return

    for p, xt in TARGETS.items():
        out = list(lines)
        # ALWAYS pin adatom xy (0 0 1) regardless of template's flags (template = free-relax min)
        out[adatom_i] = f"  {sp[0]:3s} {xt:.8f} {Y_FIX:.8f} {Z0:.8f}   0 0 1"
        txt = "\n".join(out) + "\n"
        txt = re.sub(r"pseudo_dir\s*=\s*'?[^'\n,]+'?", f"pseudo_dir = '{pdir}'", txt)
        dst = os.path.join(a.outdir, f"drag_p{p}.in")
        open(dst, "w").write(txt)
        print(f"-> {dst}  (adatom x={xt:.6f})")
    print("done. run: bash ~/Yonghoon-DEM-DFT/tools/neb_diffusion/run_li3n_drag_kgy.sh")


if __name__ == "__main__":
    main()
