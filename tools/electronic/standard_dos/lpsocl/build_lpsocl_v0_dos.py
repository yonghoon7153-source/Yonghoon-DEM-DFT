#!/usr/bin/env python3
"""build_lpsocl_v0_dos.py — LPSOCl V0-relax → scf → nscf(DOS/gap) → dos/projwfc 원버튼 패키지 (kgy).

b2o3 트랙과 동일한 후처리를 LPSOCl에 이식:
  EOS(완료, B0=24.71) → ★이 패키지: V0 relax → 표준 DOS 레시피(standard_dos README)
  - V0 = 8128.4 bohr^3 (ASE BM3), v100 = 8105.2 → 격자 스케일 s = (V0/V100)^(1/3) = 1.000953
  - nscf: occupations='tetrahedra_opt', k 8 8 2, conv 1e-9 (modelc 규약)
  - 갭: occupations='fixed' nscf의 VBM/CBM 고유값 (smearing 금지)
  - nbnd: 원소가수(Li3 P5 S6 Cl7 O6)로 자동 계산 후 1.4배 반올림 (modelc 294e -> 210)
  - 산출 csv는 b2o3_dos_smooth / b2o3_pdos_element_* 포맷 미러

사용 (kgy):
  python3 build_lpsocl_v0_dos.py --kit lpsocl_v0_kit --out lpsocl_v0 --pseudo $PWD/lpsocl_v0_kit
  nohup bash lpsocl_v0/run_lpsocl_v0.sh "$MPIRUN" "$QEGPU" > lpsocl_v0/chain.log 2>&1 &
kit 디렉토리에는 KISTI 백업의 v100 relax.in / relax.out + UPF 5종이 있어야 함.
러너는 GPU가 빌 때까지(다른 pw.x 없음 + mem<2GB) 대기 후 자동 발사 — min4와 충돌 없음.
"""
import argparse
import math
import os
import re
import shutil

VAL = {"Li": 3, "P": 5, "S": 6, "Cl": 7, "O": 6}
V0_BOHR3, V100_BOHR3 = 8128.4, 8105.2
NSCF_K = "8 8 2 0 0 0"


def read_blocks(path):
    txt = open(path).read()
    lines = txt.splitlines()
    # CELL_PARAMETERS
    ci = next(i for i, l in enumerate(lines) if l.strip().upper().startswith("CELL_PARAMETERS"))
    cell_unit = lines[ci].split()[1] if len(lines[ci].split()) > 1 else "angstrom"
    cell = [[float(x) for x in lines[ci+k+1].split()[:3]] for k in range(3)]
    # ATOMIC_SPECIES
    si = next(i for i, l in enumerate(lines) if l.strip().upper().startswith("ATOMIC_SPECIES"))
    species = []
    k = si + 1
    while k < len(lines) and len(lines[k].split()) >= 3:
        species.append(lines[k].split())
        k += 1
    # nat
    m = re.search(r"(?mi)^\s*nat\s*=\s*(\d+)", txt)
    nat = int(m.group(1))
    # ATOMIC_POSITIONS (입력의 것 — 단위 확인용)
    pi = next(i for i, l in enumerate(lines) if l.strip().upper().startswith("ATOMIC_POSITIONS"))
    pos_unit = re.sub(r"[(){}]", "", lines[pi].split()[1]).lower() if len(lines[pi].split()) > 1 else "alat"
    # K_POINTS (relax/scf용 원본)
    ki = next(i for i, l in enumerate(lines) if l.strip().upper().startswith("K_POINTS"))
    kmesh = lines[ki+1].strip()
    # namelist 원문 (&CONTROL~/ 구간들)
    return dict(txt=txt, lines=lines, cell_unit=cell_unit, cell=cell, species=species,
                nat=nat, pos_unit=pos_unit, kmesh=kmesh)


def last_positions(out_path, nat):
    out = open(out_path, errors="ignore").read().splitlines()
    idx = [i for i, l in enumerate(out) if l.strip().startswith("ATOMIC_POSITIONS")]
    assert idx, "relax.out에 ATOMIC_POSITIONS 없음"
    blk = out[idx[-1]: idx[-1] + nat + 1]
    unit = re.sub(r"[(){}]", "", blk[0].split()[1]).lower() if len(blk[0].split()) > 1 else "alat"
    atoms = [l.split() for l in blk[1:]]
    assert len(atoms) == nat and all(len(a) >= 4 for a in atoms), "잘린 블록"
    return unit, [(a[0], float(a[1]), float(a[2]), float(a[3])) for a in atoms]


def namelist(name, pairs):
    body = "\n".join(f"    {k} = {v}" for k, v in pairs)
    return f"&{name}\n{body}\n/\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kit", required=True, help="relax.in/relax.out/UPF들이 있는 디렉토리")
    ap.add_argument("--out", required=True)
    ap.add_argument("--pseudo", required=True, help="pseudo_dir 절대경로")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    B = read_blocks(os.path.join(a.kit, "relax.in"))
    s = (V0_BOHR3 / V100_BOHR3) ** (1.0 / 3.0)
    cellV0 = [[x * s for x in v] for v in B["cell"]]
    unit, atoms = last_positions(os.path.join(a.kit, "relax.out"), B["nat"])
    if unit.startswith("angstrom"):
        atoms = [(e, x * s, y * s, z * s) for e, x, y, z in atoms]     # 등방 스케일
    elif unit.startswith("crystal"):
        pass                                                           # 분율은 불변
    else:
        raise SystemExit(f"지원 안 하는 좌표 단위: {unit}")

    counts = {}
    for e, *_ in atoms:
        counts[e] = counts.get(e, 0) + 1
    nelec = sum(VAL[e] * n for e, n in counts.items())
    nocc = nelec // 2
    nbnd = int(math.ceil(nocc * 1.4 / 10.0) * 10)
    ntyp = len(B["species"])
    print(f"조성 {counts} | 전자 {nelec} -> N_occ {nocc}, nbnd {nbnd} | 스케일 s={s:.6f}")

    # 원본에서 ecut 추출
    ec = re.search(r"(?mi)^\s*ecutwfc\s*=\s*([\d.]+)", B["txt"]).group(1)
    er_m = re.search(r"(?mi)^\s*ecutrho\s*=\s*([\d.]+)", B["txt"])
    er = er_m.group(1) if er_m else str(float(ec) * 8)
    occ_m = re.search(r"(?mi)^\s*occupations\s*=\s*'([^']+)'", B["txt"])
    occ0 = occ_m.group(1) if occ_m else "smearing"
    dg_m = re.search(r"(?mi)^\s*degauss\s*=\s*([\d.dDeE+-]+)", B["txt"])
    sm_m = re.search(r"(?mi)^\s*smearing\s*=\s*'([^']+)'", B["txt"])

    def species_block():
        return "ATOMIC_SPECIES\n" + "\n".join(f"  {s0:<4s} {s1:>8s}  {s2}" for s0, s1, s2 in B["species"]) + "\n"

    def cell_block():
        rows = "\n".join(f"  {v[0]:18.12f} {v[1]:18.12f} {v[2]:18.12f}" for v in cellV0)
        return f"CELL_PARAMETERS {B['cell_unit']}\n{rows}\n"

    def pos_block(ats):
        rows = "\n".join(f"  {e:<4s} {x:18.12f} {y:18.12f} {z:18.12f}" for e, x, y, z in ats)
        return f"ATOMIC_POSITIONS {unit}\n{rows}\n"

    def sys_pairs(extra):
        base = [("ibrav", "0"), ("nat", str(B["nat"])), ("ntyp", str(ntyp)),
                ("ecutwfc", ec), ("ecutrho", er)]
        return base + extra

    def occ_pairs():
        p = [("occupations", f"'{occ0}'")]
        if occ0 == "smearing":
            p.append(("smearing", f"'{sm_m.group(1) if sm_m else 'mv'}'"))
            p.append(("degauss", dg_m.group(1) if dg_m else "0.01"))
        return p

    def kblock(mesh):
        return f"K_POINTS automatic\n{mesh}\n"

    O = lambda f: os.path.join(a.out, f)
    # 01: V0 fixed-cell relax (v100 최종기하 스케일 탑재)
    with open(O("01_relax_v0.in"), "w") as f:
        f.write(namelist("CONTROL", [("calculation", "'relax'"), ("prefix", "'lpsocl_v0'"),
                                     ("outdir", "'./tmp'"), ("pseudo_dir", f"'{a.pseudo}'"),
                                     ("forc_conv_thr", "1.0d-3"), ("etot_conv_thr", "1.0d-5"),
                                     ("nstep", "200"), ("verbosity", "'high'")]))
        f.write(namelist("SYSTEM", sys_pairs(occ_pairs())))
        f.write(namelist("ELECTRONS", [("conv_thr", "1.0d-8"), ("mixing_beta", "0.3"),
                                       ("electron_maxstep", "200")]))
        f.write(namelist("IONS", [("ion_dynamics", "'bfgs'")]))
        f.write(species_block()); f.write(cell_block()); f.write(pos_block(atoms))
        f.write(kblock(B["kmesh"]))
    # 02 scf / 03 nscf(dos) / 03b nscf(gap) 골격 — 좌표는 러너가 01 결과로 채움 (@POS@)
    def write_stage(fname, calc, occ_extra, kmesh, elec_conv):
        with open(O(fname), "w") as f:
            f.write(namelist("CONTROL", [("calculation", f"'{calc}'"), ("prefix", "'lpsocl_v0'"),
                                         ("outdir", "'./tmp'"), ("pseudo_dir", f"'{a.pseudo}'"),
                                         ("verbosity", "'high'")]))
            f.write(namelist("SYSTEM", sys_pairs(occ_extra)))
            f.write(namelist("ELECTRONS", [("conv_thr", elec_conv), ("mixing_beta", "0.3"),
                                           ("electron_maxstep", "300")]))
            f.write(species_block()); f.write(cell_block()); f.write("@POS@\n")
            f.write(kblock(kmesh))
    write_stage("02_scf.in", "scf", occ_pairs(), B["kmesh"], "1.0d-8")
    write_stage("03_nscf_dos.in", "nscf", [("occupations", "'tetrahedra_opt'"), ("nbnd", str(nbnd))],
                NSCF_K, "1.0d-9")
    write_stage("03b_nscf_gap.in", "nscf", [("occupations", "'fixed'"), ("nbnd", str(nbnd))],
                NSCF_K, "1.0d-9")
    with open(O("04_dos.in"), "w") as f:
        f.write("&DOS\n    prefix='lpsocl_v0'\n    outdir='./tmp'\n    fildos='lpsocl_v0.dos'\n    DeltaE=0.01\n/\n")
    with open(O("05_projwfc.in"), "w") as f:
        f.write("&PROJWFC\n    prefix='lpsocl_v0'\n    outdir='./tmp'\n    filpdos='lpsocl_v0'\n    DeltaE=0.01\n/\n")

    counts_str = repr(counts)
    with open(O("post_lpsocl_dos.py"), "w") as f:
        f.write('''#!/usr/bin/env python3
"""04/05 산출물 -> b2o3 포맷 csv 3종 + 갭 요약 (stdlib only)."""
import glob, math, re
COUNTS = ''' + counts_str + '''
NTOT = sum(COUNTS.values())
vbm = cbm = None
try:
    t = open("03b_nscf_gap.out", errors="ignore").read()
    m = re.search(r"highest occupied, lowest unoccupied level \\(ev\\):\\s*([-\\d.]+)\\s+([-\\d.]+)", t)
    if m: vbm, cbm = float(m.group(1)), float(m.group(2))
except FileNotFoundError:
    pass
if vbm is None:
    t = open("03_nscf_dos.out", errors="ignore").read()
    m = re.search(r"highest occupied, lowest unoccupied level \\(ev\\):\\s*([-\\d.]+)\\s+([-\\d.]+)", t)
    if m: vbm, cbm = float(m.group(1)), float(m.group(2))
assert vbm is not None, "VBM/CBM 라인 못 찾음 (fixed nscf 실패? 03b out 확인)"
gap = cbm - vbm
print(f"VBM {vbm:.4f} eV | CBM {cbm:.4f} eV | gap {gap:.3f} eV")
open("lpsocl_v0_gap.txt", "w").write(f"VBM_eV {vbm:.4f}\\nCBM_eV {cbm:.4f}\\ngap_eV {gap:.4f}\\nmethod standard_dos(tetrahedra_opt DOS + fixed-occ eigenvalues, k882, nbnd auto)\\n")

def smooth_resample(E, Y, sigma=0.05, e0=-8.0, e1=8.0, de=0.02):
    out = []
    j0 = 0
    for k in range(int(round((e1 - e0) / de)) + 1):
        e = e0 + k * de
        num = den = 0.0
        for i in range(len(E)):
            d = E[i] - e
            if d < -4 * sigma:
                continue
            if d > 4 * sigma:
                break
            w = math.exp(-0.5 * (d / sigma) ** 2)
            num += w * Y[i]; den += w
        out.append((e, num / den if den else 0.0))
    return out

# 총 DOS
E, D = [], []
for l in open("lpsocl_v0.dos"):
    if l.strip().startswith("#") or not l.split():
        continue
    p = l.split(); E.append(float(p[0]) - vbm); D.append(float(p[1]))
with open("lpsocl_dos_smooth.csv", "w") as f:
    f.write("E_minus_VBM,total_DOS\\n")
    for e, y in smooth_resample(E, D):
        f.write(f"{e:.4f},{y:.4f}\\n")

# 원소별 PDOS 합
el_sum = {}
for fn in glob.glob("lpsocl_v0.pdos_atm#*"):
    m = re.search(r"atm#\\d+\\(([A-Za-z]+)\\)", fn)
    el = m.group(1)
    rows = []
    for l in open(fn):
        if l.strip().startswith("#") or not l.split():
            continue
        p = l.split(); rows.append((float(p[0]), float(p[1])))
    if el not in el_sum:
        el_sum[el] = dict(rows)
    else:
        for e, y in rows:
            el_sum[el][e] = el_sum[el].get(e, 0.0) + y
els = [e for e in ("Li", "P", "S", "Cl", "O") if e in el_sum]
grid = sorted(next(iter(el_sum.values())).keys())
sm = {el: smooth_resample([e - vbm for e in grid], [el_sum[el][e] for e in grid]) for el in els}
with open("lpsocl_pdos_element_smooth.csv", "w") as f:
    f.write("E_minus_VBM," + ",".join(els) + "\\n")
    for i in range(len(sm[els[0]])):
        f.write(f"{sm[els[0]][i][0]:.4f}," + ",".join(f"{sm[el][i][1]:.4f}" for el in els) + "\\n")
with open("lpsocl_pdos_element_PERATOM.csv", "w") as f:
    f.write(f'"# lpsocl element PDOS normalized. _perTOT = /total atoms ({NTOT}); _perEL = /count {COUNTS}"\\n')
    f.write("E_minus_VBM," + ",".join(f"{el}_perTOT" for el in els) + "," + ",".join(f"{el}_perEL" for el in els) + "\\n")
    for i in range(len(sm[els[0]])):
        e = sm[els[0]][i][0]
        pt = [sm[el][i][1] / NTOT for el in els]
        pe = [sm[el][i][1] / COUNTS[el] for el in els]
        f.write(f"{e:.4f}," + ",".join(f"{v:.5f}" for v in pt) + "," + ",".join(f"{v:.5f}" for v in pe) + "\\n")
print("csv 3종 + lpsocl_v0_gap.txt 완료")
''')

    with open(O("run_lpsocl_v0.sh"), "w") as f:
        f.write("""#!/bin/bash
# usage: run_lpsocl_v0.sh <MPIRUN> <QEGPU_BIN>   (qegpu 셸에서)
M=$1; Q=$2
cd "$(dirname "$0")"
[ -z "$M" ] || [ -z "$Q" ] && { echo "MPIRUN/QEGPU 인자 필요"; exit 1; }

echo "[wait] GPU 비기를 대기 (다른 pw.x 없음 + mem<2GB)"
while true; do
    pgrep -x pw.x >/dev/null 2>&1 || {
        mem=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | head -1 | tr -d ' ')
        [ "${mem:-99999}" -lt 2000 ] && break
    }
    sleep 120
done
echo "[go] $(date)"

run_pw () {  # $1=in $2=out
    grep -aq "JOB DONE" "$2" 2>/dev/null && { echo "[$1] done — skip"; return 0; }
    echo "[$1] START $(date)"
    $M -np 1 "$Q/pw.x" -npool 1 -in "$1" > "$2" 2>&1
    grep -aq "JOB DONE" "$2" && echo "[$1] DONE $(date)" || { echo "[$1] FAILED $(date)"; return 1; }
}

run_pw 01_relax_v0.in 01_relax_v0.out || exit 1
grep -aq "bfgs converged" 01_relax_v0.out && echo "[01] bfgs 수렴" || echo "[01] MAXSTEP 주의"

python3 - <<'PY'    # 01 최종기하 -> @POS@ 치환
import re
out = open("01_relax_v0.out", errors="ignore").read().splitlines()
nat = int(next(re.search(r"=\\s*(\\d+)", l).group(1) for l in out if "number of atoms/cell" in l))
idx = [i for i, l in enumerate(out) if l.strip().startswith("ATOMIC_POSITIONS")]
blk = "\\n".join(out[idx[-1]: idx[-1] + nat + 1])
for f in ("02_scf.in", "03_nscf_dos.in", "03b_nscf_gap.in"):
    t = open(f).read()
    if "@POS@" in t:
        open(f, "w").write(t.replace("@POS@", blk))
        print(f"[carry] {f} <- V0 최종기하 {nat}원자")
PY

run_pw 02_scf.in 02_scf.out || exit 1
run_pw 03_nscf_dos.in 03_nscf_dos.out || exit 1
run_pw 03b_nscf_gap.in 03b_nscf_gap.out || echo "[03b] fixed 실패(결함밴드?) — 갭은 03 폴백"
echo "[04] dos.x"; $M -np 1 "$Q/dos.x" < 04_dos.in > 04_dos.out 2>&1
echo "[05] projwfc.x"; $M -np 1 "$Q/projwfc.x" < 05_projwfc.in > 05_projwfc.out 2>&1
python3 post_lpsocl_dos.py
echo "[ALL DONE] $(date) — 산출: lpsocl_v0_gap.txt + csv 3종 + 01_relax_v0.out(V0 구조)"
""")

    with open(O("watch_lpsocl_v0.sh"), "w") as f:
        f.write("""#!/bin/bash
# watch -n 60 bash lpsocl_v0/watch_lpsocl_v0.sh
cd "$(dirname "$0")"
echo "══════ kgy LPSOCl V0→DOS 체인  $(date '+%m-%d %H:%M:%S') ══════"
for st in 01_relax_v0 02_scf 03_nscf_dos 03b_nscf_gap 04_dos 05_projwfc; do
    o=$st.out
    if [ ! -f "$o" ]; then echo " $st: ⬚ 대기"; continue; fi
    if grep -aq "JOB DONE" "$o"; then
        e=$(grep -a '^!' "$o" 2>/dev/null | tail -1 | awk '{print $5}')
        echo " $st: ✅ DONE ${e:+E=$e Ry}"
    else
        ion=$(grep -ac '^!' "$o" 2>/dev/null)
        it=$(grep -a "iteration #" "$o" 2>/dev/null | tail -1 | sed 's/.*#[ ]*\\([0-9]*\\).*/\\1/')
        fo=$(grep -a "Total force" "$o" 2>/dev/null | tail -1 | awk '{print $4}')
        age=$(( $(date +%s) - $(stat -c %Y "$o") ))
        echo " $st: ⏳ ion=$ion iter=${it:--} |F|=${fo:--} (${age}s前)"
    fi
done
[ -f lpsocl_v0_gap.txt ] && { echo "── 갭 ──"; sed 's/^/  /' lpsocl_v0_gap.txt; }
tail -3 chain.log 2>/dev/null | sed 's/^/ · /'
nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader 2>/dev/null | sed 's/^/ GPU: /'
""")
    print(f"패키지 완성: {a.out}/ (01→05 + post + run + watch)")


if __name__ == "__main__":
    main()
