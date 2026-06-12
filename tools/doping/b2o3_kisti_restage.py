#!/usr/bin/env python3
"""Build the B2O3 DFT-EOS resume package for KISTI as PASTE payloads (no sftp/scp).

V100 died mid-EOS (runs/b2o3_dft3_run): v0.98 relax at BFGS block 61, v1.00 at 19,
v1.02 SCF diverged on the UMA warm-start coords, and NO volume reached JOB DONE.
Binary outdirs (.save/.bfgs) cannot move over a paste-only channel and are not
needed: the standard recovery is a from_scratch restart on the LAST printed
coordinates. This rebuilds a clean 6-point grid (0.96..1.06 — same as modelC
v{096..106}, keeps dB0 vs 21.7 apples-to-apples) as plain-text inputs:

  0.98 / 1.00    original .in + LAST complete ATOMIC_POSITIONS block of its .out
  1.02           own cell kept, coords = v1.00 last block x (1.02)^(1/3),
                 mixing_beta 0.3 -> 0.15 (SCF diverged with the UMA coords)
  0.96/1.04/1.06 built from the v1.00 input (cell & coords x cbrt(tag))

Every staged input gets pseudo_dir='./pseudo/' (UPFs are too big to paste — on
KISTI reuse the Nd-run pseudo dir + wget the rest by exact filename; the needed
names are printed). Each staged file is also wrapped as paste_payloads/
payload_NN_<name>.txt = a self-contained `cat > <name> <<'PAYLOAD_EOF'` block to
paste into the KISTI shell, plus payload_ALL.txt for a single big paste.
md5 manifest is printed so a mangled paste is caught by `md5sum` on KISTI.

Usage (WSL):
  python3 tools/doping/b2o3_kisti_restage.py
  -> /mnt/d/v100백업/b2o3_kisti_stage/paste_payloads/
"""
import argparse
import hashlib
import re
from pathlib import Path

POS_LINE = r"[ \t]*[A-Za-z][A-Za-z]?\d*(?:[ \t]+-?\d+\.\d+){3}[^\n]*\n"
CELL_ROW = r"\s*(?:-?\d+\.\d+\s+){2}-?\d+\.\d+\s*\n"


def nat_of(out_txt):
    return int(re.search(r"number of atoms/cell\s*=\s*(\d+)", out_txt).group(1))


def pos_blocks(out_txt, nat):
    """All complete (unit, block) position blocks in a pw.x output, in order."""
    pat = re.compile(r"ATOMIC_POSITIONS\s*\(?([A-Za-z]+)\)?[^\n]*\n((?:%s){%d})"
                     % (POS_LINE, nat))
    return pat.findall(out_txt)


def replace_positions(in_txt, unit, block):
    pat = re.compile(r"ATOMIC_POSITIONS[^\n]*\n(?:%s)+" % POS_LINE)
    if not pat.search(in_txt):
        raise SystemExit("no ATOMIC_POSITIONS card found in input")
    return pat.sub(lambda m: "ATOMIC_POSITIONS %s\n%s" % (unit, block), in_txt, count=1)


def scale_block(block, s):
    out = []
    for ln in block.strip("\n").splitlines():
        m = re.match(r"\s*([A-Za-z][A-Za-z]?\d*)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)", ln)
        sym = m.group(1)
        x, y, z = (float(m.group(i)) * s for i in (2, 3, 4))
        out.append(f"  {sym:3s} {x:.8f} {y:.8f} {z:.8f}")
    return "\n".join(out) + "\n"


def get_cell(in_txt):
    m = re.search(r"CELL_PARAMETERS\s+(\S+)\s*\n((?:%s){3})" % CELL_ROW, in_txt)
    return m.group(1), m.group(2)


def scale_cell(cell_block, s):
    rows = []
    for ln in cell_block.strip().splitlines():
        rows.append("  " + " ".join(f"{float(v) * s:.10f}" for v in ln.split()))
    return "\n".join(rows) + "\n"


RESUME_SPLICE = '''#!/usr/bin/env python3
"""Transplant the last complete ATOMIC_POSITIONS block of OUT into IN (no-op if none)."""
import re, sys
inp, out = sys.argv[1], sys.argv[2]
t = open(inp).read()
try:
    o = open(out).read()
except FileNotFoundError:
    sys.exit(0)
m = re.search(r"number of atoms/cell\\s*=\\s*(\\d+)", o)
if not m:
    sys.exit(0)
nat = int(m.group(1))
POS = r"[ \\t]*[A-Za-z][A-Za-z]?\\d*(?:[ \\t]+-?\\d+\\.\\d+){3}[^\\n]*\\n"
blks = re.findall(r"ATOMIC_POSITIONS\\s*\\(?([A-Za-z]+)\\)?[^\\n]*\\n((?:%s){%d})" % (POS, nat), o)
if not blks:
    sys.exit(0)
unit, blk = blks[-1]
new = re.sub(r"ATOMIC_POSITIONS[^\\n]*\\n(?:%s)+" % POS,
             lambda mm: "ATOMIC_POSITIONS %s\\n%s" % (unit, blk), t, count=1)
if new != t:
    open(inp, "w").write(new)
    print(f"[resume] {inp} <- last coords of {out} ({len(blks)} blocks)")
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run_dir", default="/mnt/d/v100백업/runs/b2o3_dft3_run")
    ap.add_argument("--out", default="/mnt/d/v100백업/b2o3_kisti_stage")
    ap.add_argument("--new_tags", nargs="*", default=["0.96", "1.04", "1.06"])
    A = ap.parse_args()
    run = Path(A.run_dir)
    stage = Path(A.out)
    stage.mkdir(parents=True, exist_ok=True)

    in098 = (run / "eos_v0.98.in").read_text()
    out098 = (run / "eos_v0.98.out").read_text()
    in100 = (run / "eos_v1.00.in").read_text()
    out100 = (run / "eos_v1.00.out").read_text()
    in102 = (run / "eos_v1.02.in").read_text()

    nat = nat_of(out100)
    assert nat == nat_of(out098), "nat mismatch between 0.98 and 1.00 outputs"
    b098 = pos_blocks(out098, nat)
    b100 = pos_blocks(out100, nat)
    assert b098 and b100, "no complete ATOMIC_POSITIONS block found"
    u98, blk98 = b098[-1]
    u100, blk100 = b100[-1]
    crystal = u100.lower().startswith("crystal")
    print(f"nat={nat}  blocks: v0.98={len(b098)}  v1.00={len(b100)}  unit={u100}")

    # sanity: the 0.98 cell must be the 1.00 cell x 0.98^(1/3)
    _, c098 = get_cell(in098)
    _, c100 = get_cell(in100)
    a98 = max(abs(float(v)) for v in c098.split())
    a100 = max(abs(float(v)) for v in c100.split())
    ratio, expect = a98 / a100, 0.98 ** (1 / 3)
    print(f"cell-ratio check 0.98/1.00: {ratio:.6f} (expect {expect:.6f})")
    assert abs(ratio - expect) < 1e-3, "cells are not a cbrt(0.98) scaling — grid assumption broken"

    # 1) in-flight volumes: restart from their own last coords
    (stage / "eos_v0.98.in").write_text(replace_positions(in098, u98, blk98))
    (stage / "eos_v1.00.in").write_text(replace_positions(in100, u100, blk100))

    # 2) diverged 1.02: keep its cell, transplant scaled v1.00 coords, gentler mixing
    s = 1.02 ** (1 / 3)
    t102 = replace_positions(in102, u100, blk100 if crystal else scale_block(blk100, s))
    t102, nsub = re.subn(r"mixing_beta\s*=\s*[\d.]+", "mixing_beta=0.15", t102)
    assert nsub == 1, "mixing_beta line not found in eos_v1.02.in"
    (stage / "eos_v1.02.in").write_text(t102)

    # 3) new volumes from the v1.00 template
    for tag in A.new_tags:
        s = float(tag) ** (1 / 3)
        t = re.sub(r"(CELL_PARAMETERS[^\n]*\n)(?:%s){3}" % CELL_ROW,
                   lambda m: m.group(1) + scale_cell(c100, s), in100, count=1)
        t = replace_positions(t, u100, blk100 if crystal else scale_block(blk100, s))
        t = t.replace("b2o3eos_1.00", f"b2o3eos_{tag}").replace("tmp_1.00", f"tmp_{tag}")
        (stage / f"eos_v{tag}.in").write_text(t)

    # 4) UPFs can't be pasted -> inputs point at ./pseudo/, names printed for
    #    KISTI-side reuse (Nd-run dir) or wget by exact filename
    sp = re.search(r"ATOMIC_SPECIES\s*\n((?:\s*\S+\s+[\d.]+\s+\S+\s*\n)+)", in100).group(1)
    upfs = [ln.split()[2] for ln in sp.strip().splitlines()]
    for f in stage.glob("eos_v*.in"):
        f.write_text(re.sub(r"pseudo_dir\s*=\s*'[^']*'", "pseudo_dir='./pseudo/'",
                            f.read_text()))
    (stage / "resume_splice.py").write_text(RESUME_SPLICE)

    # 5) paste payloads: one self-contained heredoc per file + ALL-in-one
    pay = stage / "paste_payloads"
    pay.mkdir(exist_ok=True)
    for old in pay.glob("payload_*.txt"):
        old.unlink()
    files = sorted(stage.glob("eos_v*.in")) + [stage / "resume_splice.py"]
    manifest, blobs = [], []
    for i, f in enumerate(files, 1):
        content = f.read_text()
        if not content.endswith("\n"):
            content += "\n"
        blob = f"cat > {f.name} <<'PAYLOAD_EOF'\n{content}PAYLOAD_EOF\n"
        (pay / f"payload_{i:02d}_{f.name}.txt").write_text(blob)
        blobs.append(blob)
        manifest.append((f.name, hashlib.md5(content.encode()).hexdigest(),
                         content.count("\n")))
    (pay / "payload_ALL.txt").write_text("\n".join(blobs))

    print(f"\nstaged -> {stage}")
    print(f"payloads -> {pay}  (개별 7개 + payload_ALL.txt)")
    print("\nKISTI 붙여넣기 후 `md5sum eos_v*.in resume_splice.py` 와 대조:")
    for name, md5, nl in manifest:
        print(f"  {md5}  {name}  ({nl} lines)")
    print("\n./pseudo/ 에 필요한 UPF (paste 불가 — Nd-run dir 복사 or wget):")
    for u in upfs:
        print(f"  {u}")


if __name__ == "__main__":
    main()
