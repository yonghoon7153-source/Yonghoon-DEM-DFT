import re, numpy as np
from pathlib import Path

STRAIN = 0.005
ref = Path("../scf.in").read_text()
m_cell = re.search(r"CELL_PARAMETERS\s*\S+\s*\n((?:[^\n]+\n){3})", ref)
cell0 = np.array([l.split() for l in m_cell.group(1).strip().split("\n")], float)
m_sp  = re.search(r"(ATOMIC_SPECIES\s*\n(?:\s*\S+\s+\S+\s+\S+\s*\n)+)", ref).group(1)
# tight regex: only lines starting with element symbol + 3 floats
m_pos_block = re.search(
    r"ATOMIC_POSITIONS\s*\(\S+\)\s*\n((?:\s*[A-Z][a-z]?\s+[-\d.eE+]+\s+[-\d.eE+]+\s+[-\d.eE+]+\s*\n)+)",
    ref)
m_pos = "ATOMIC_POSITIONS (angstrom)\n" + m_pos_block.group(1)

eps_list = [
    np.diag([1,0,0]), np.diag([0,1,0]), np.diag([0,0,1]),
    np.array([[0,0,0],[0,0,1],[0,1,0]]),
    np.array([[0,0,1],[0,0,0],[1,0,0]]),
    np.array([[0,1,0],[1,0,0],[0,0,0]]),
]

HEAD = """&CONTROL
 calculation='scf', prefix='m_e{i}_{s}', outdir='./tmp',
 pseudo_dir='/data/work/modelc_v2_elastic/pseudo',
 tprnfor=.true., tstress=.true.
/
&SYSTEM
 ibrav=0, nat=62, ntyp=4, ecutwfc=60.0, ecutrho=480.0,
 occupations='smearing', smearing='mv', degauss=0.01
/
&ELECTRONS
 conv_thr=1.0d-10, mixing_beta=0.3
/

K_POINTS automatic
6 6 3 0 0 0
"""

for sign, mag in [("p", +STRAIN), ("m", -STRAIN)]:
    for i, e0 in enumerate(eps_list, 1):
        eps = e0 * mag
        cell_s = cell0 @ (np.eye(3) + eps).T
        d = Path(f"e{i}_{sign}")
        d.mkdir(exist_ok=True)
        cb = "CELL_PARAMETERS angstrom\n"
        for r in cell_s:
            cb += f"  {r[0]:14.8f}  {r[1]:14.8f}  {r[2]:14.8f}\n"
        (d/"scf.in").write_text(HEAD.format(i=i, s=sign) + "\n" + m_sp + "\n" + m_pos + "\n" + cb)
print("OK 12 inputs (tight regex)")
