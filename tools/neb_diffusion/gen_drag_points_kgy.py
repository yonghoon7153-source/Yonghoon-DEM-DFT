#!/usr/bin/env python3
"""gen_drag_points_kgy.py — regenerate Li3N drag inputs p5..p8 on kgy from a
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
"""
import argparse
import os
import re

Y_FIX = 1.58054864
Z0 = 13.48712429
X_P0 = 8.2125
DX = 0.684375
TARGETS = {5: X_P0 - 5 * DX, 6: X_P0 - 6 * DX, 7: X_P0 - 7 * DX, 8: X_P0 - 8 * DX}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", required=True, help="p0_min4.in (136-atom drag input)")
    ap.add_argument("--pseudo_src", required=True, help="dir with li_pbe_v1.4.uspp.F.UPF + N.pbe-n-radius_5.UPF")
    ap.add_argument("--outdir", required=True)
    a = ap.parse_args()

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
    # locate ATOMIC_POSITIONS block
    ip = next(i for i, l in enumerate(lines) if l.strip().upper().startswith("ATOMIC_POSITIONS"))
    # adatom = the atom line whose trailing 3 flags are 0 0 1 (xy pinned, z free)
    adatom_i = None
    for i in range(ip + 1, len(lines)):
        s = lines[i].split()
        if len(s) >= 7 and s[-3:] == ["0", "0", "1"] and re.match(r"^[A-Za-z]", s[0]):
            adatom_i = i
            break
    if adatom_i is None:
        # fallback: atom nearest (X_P0, Y_FIX)
        best = None
        for i in range(ip + 1, len(lines)):
            s = lines[i].split()
            if len(s) >= 4 and re.match(r"^[A-Za-z]", s[0]):
                try:
                    d = (float(s[1]) - X_P0) ** 2 + (float(s[2]) - Y_FIX) ** 2
                except ValueError:
                    continue
                if best is None or d < best[0]:
                    best = (d, i)
        adatom_i = best[1]
        print(f"[warn] no '0 0 1' flag found; adatom by proximity -> line: {lines[adatom_i].strip()}")
    sp = lines[adatom_i].split()
    print(f"adatom detected: {sp[0]} at ({sp[1]},{sp[2]},{sp[3]}) flags={sp[-3:] if len(sp)>=7 else 'none'}")

    for p, xt in TARGETS.items():
        out = list(lines)
        # keep species + if_pos flags; rewrite x,y,z
        tail = " 0 0 1" if len(sp) >= 7 else ""
        out[adatom_i] = f"  {sp[0]:3s} {xt:.8f} {Y_FIX:.8f} {Z0:.8f}{tail}"
        txt = "\n".join(out) + "\n"
        txt = re.sub(r"pseudo_dir\s*=\s*'?[^'\n,]+'?", f"pseudo_dir = '{pdir}'", txt)
        dst = os.path.join(a.outdir, f"drag_p{p}.in")
        open(dst, "w").write(txt)
        print(f"-> {dst}  (adatom x={xt:.6f})")
    print("done. run: bash ~/Yonghoon-DEM-DFT/tools/neb_diffusion/run_li3n_drag_kgy.sh")


if __name__ == "__main__":
    main()
