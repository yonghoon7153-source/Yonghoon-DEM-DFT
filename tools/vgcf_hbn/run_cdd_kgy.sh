#!/usr/bin/env bash
# =============================================================================
# run_cdd_kgy.sh — Li 결합 CDD (charge density difference) on kgy.
#   CDD = rho(Li+host) - rho(host) - rho(Li)   [같은 셀·같은 grid 3-SCF 차분]
# Liu2022(AMI 9,2200011) 그림 (f)(g) 대응 비교그림용. relaxed 구조에서 single-point.
#   대상 3종: Li_on_graphene(↔Li-Cu) / Li_on_hbn(↔Li-hBN) / Li_in_gallery_2L2L(↔샌드위치)
#
# 노랑=전자 축적(받개), 청록=결핍(Li+). VGCF가 전자받개(Cu역할) vs h-BN 수동캡 시각화.
#
# ⚠ GPU 필요 (pw.x). NEB 돌면 대기 내장 — 근데 CDD 빨리 원하면 NEB 잠깐 멈추고(resume-safe)
#   이거 먼저(~2h) 돌린 뒤 NEB 재개 권장. relaxed 좌표는 ~/work/vgcf_hbn/*.out에서.
#   cd ~/Yonghoon-DEM-DFT && git pull   # (or checkout tools/vgcf_hbn/)
#   tmux new -s vgcfcdd -d 'bash tools/vgcf_hbn/run_cdd_kgy.sh >> ~/work/vgcf_hbn/cdd_run.log 2>&1'
# =============================================================================
set -u; set +H
REPO=${REPO:-$HOME/Yonghoon-DEM-DFT}; [ -d "$REPO" ] || REPO=$HOME/work/Yonghoon-DEM-DFT
WORK=${WORK:-$HOME/work/vgcf_hbn}; CDD=$WORK/cdd; mkdir -p "$CDD"
CASES=${CASES:-"Li_on_graphene Li_on_hbn Li_in_gallery_2L2L"}
[ "$(pgrep -fc run_cdd_kgy.sh)" -le 3 ] || { echo "이미 실행중"; exit 1; }

# GPU 대기 (NEB/relax 뒤)
while pgrep -f 'pw\.x|neb\.x' >/dev/null 2>&1; do
  echo "[$(date +%H:%M:%S)] GPU 사용중(NEB?) — 5분 뒤 재확인 (빨리 원하면 NEB 멈추고 재시작)"; sleep 300
done
echo "[$(date +%H:%M:%S)] GPU free — CDD 시작"

# ---- qegpu env + pp.x ----
PW=${PW:-$(find "$HOME/apps" -maxdepth 4 -name pw.x -path "*qe*gpu*bin*" 2>/dev/null | head -1)}
PPX="$(dirname "$PW")/pp.x"; [ -x "$PPX" ] || { echo "ERROR: pp.x 없음"; exit 1; }
NV="$HOME/apps/nvhpc/Linux_x86_64/24.11"
HPCX="$(ls -d "$NV"/comm_libs/*/hpcx/hpcx-*/ompi 2>/dev/null | sort | tail -1)"
export OPAL_PREFIX="$HPCX" OMP_NUM_THREADS=1
export LD_LIBRARY_PATH="$NV/compilers/lib:$NV/cuda/12.6/lib64:$NV/math_libs/lib64:$HPCX/lib:${LD_LIBRARY_PATH:-}"
export PATH="$(dirname "$PW"):$HPCX/bin:$PATH"
MPIRUN="$HPCX/bin/mpirun"; PSE=$WORK/pseudo
echo "pw.x=$PW  pp.x=$PPX"

gen_scf() {  # $1=case  -> complex/host/li 3개 scf.in (relaxed 좌표, same cell/grid)
  python3 - "$WORK" "$CDD" "$1" "$PSE" <<'PY'
import re, sys, os
W, out, nm, pse = sys.argv[1:5]
t = open(f"{W}/{nm}.out", errors="ignore").read()
assert "JOB DONE" in t and "Begin final coordinates" in t, f"{nm}: relaxed .out 없음"
blk = t.split("Begin final coordinates")[-1].split("End final coordinates")[0]
at = [(l.split()[0], *[float(x) for x in l.split()[1:4]])
      for l in blk.splitlines() if re.match(r"\s*[A-Z][a-z]?\s+-?\d", l)]
tin = open(f"{W}/{nm}.in").read()
head = tin.split("CELL_PARAMETERS")[0]
head = head.replace("calculation     = 'relax'", "calculation     = 'scf'")
head = re.sub(r"&IONS.*?/\n", "", head, flags=re.S)
head = re.sub(r"\n\s*nstep\s*=.*", "", head); head = re.sub(r"forc_conv_thr.*\n", "", head)
cell = re.search(r"CELL_PARAMETERS angstrom\n(( *-?\d[^\n]*\n){3})", tin).group(0)
spec = re.search(r"ATOMIC_SPECIES\n(( +[A-Za-z][^\n]*\n)+)", tin).group(0)
kpts = re.search(r"K_POINTS automatic\n[^\n]*\n?", tin).group(0)
def block(atoms, tag, nsp):
    order = []
    for e, *_ in atoms:
        if e not in order: order.append(e)
    if "Li" in order: order = [e for e in order if e != "Li"] + ["Li"]
    # ntyp/nspin 조정
    h = re.sub(r"ntyp\s*=\s*\d+", f"ntyp            = {len(order)}", head)
    h = re.sub(r"prefix\s*=\s*'[^']*'", f"prefix          = '{tag}'", h)
    h = re.sub(r"outdir\s*=\s*'[^']*'", f"outdir          = './tmp_{tag}'", h)
    if nsp == 1:
        h = re.sub(r"\n\s*nspin\s*=.*", "", h); h = re.sub(r"\n\s*starting_magnetization.*", "", h)
    sp = "\n".join(l for l in spec.splitlines() if l.strip().startswith("ATOMIC_SPECIES")
                   or any(l.strip().startswith(e) for e in order))
    pos = "ATOMIC_POSITIONS angstrom\n" + "\n".join(
        f"  {e:2s} {x:14.8f} {y:14.8f} {z:14.8f}" for e, x, y, z in atoms)
    return h + cell + "\n" + sp + "\n\n" + pos + "\n\n" + kpts
os.makedirs(f"{out}/{nm}", exist_ok=True)
li = [a for a in at if a[0] == "Li"]; host = [a for a in at if a[0] != "Li"]
open(f"{out}/{nm}/complex.in", "w").write(block(at,   f"c_{nm[:8]}", 2))
open(f"{out}/{nm}/host.in",    "w").write(block(host, f"h_{nm[:8]}", 1))
open(f"{out}/{nm}/li.in",      "w").write(block(li,   f"l_{nm[:8]}", 2))
print(f"[{nm}] 3-SCF 입력 생성 (complex {len(at)} / host {len(host)} / li {len(li)})")
PY
}

run_scf() { # $1=dir $2=tag ($tag.in -> $tag.out + density cube)
  local d=$1 g=$2
  if ! grep -aq "JOB DONE" "$d/$g.out" 2>/dev/null; then
    sed "s|\$PSEUDO_DIR|$PSE|g" "$d/$g.in" > "$d/$g.run.in"
    echo "[$(date +%H:%M:%S)] pw.x $(basename $d)/$g"
    "$MPIRUN" -np 1 "$PW" -in "$d/$g.run.in" > "$d/$g.out" 2>&1
    grep -aq "JOB DONE" "$d/$g.out" || { echo "[$g] FAIL:"; tail -8 "$d/$g.out"; return 1; }
  fi
  if [ ! -s "$d/${g}_rho.cube" ]; then
    cat > "$d/pp_$g.in" <<EOF
&INPUTPP prefix='$(grep -aoP "prefix\s*=\s*'\K[^']+" "$d/$g.in" | head -1)', outdir='$d/tmp_$(grep -aoP "prefix\s*=\s*'\K[^']+" "$d/$g.in" | head -1)', plot_num=0, filplot='$d/${g}_fp' /
&PLOT iflag=3, output_format=6, fileout='$d/${g}_rho.cube' /
EOF
    "$MPIRUN" -np 1 "$PPX" -in "$d/pp_$g.in" > "$d/pp_$g.out" 2>&1
  fi
}

for c in $CASES; do
  d=$CDD/$c
  gen_scf "$c" || { echo "[$c] 입력생성 실패 skip"; continue; }
  run_scf "$d" complex && run_scf "$d" host && run_scf "$d" li || { echo "[$c] SCF 실패"; continue; }
  echo "[$(date +%H:%M:%S)] CDD 차분 $c"
  python3 "$REPO/tools/electronic/cube_diff.py" --mode cdd \
    --ab "$d/complex_rho.cube" --a "$d/host_rho.cube" --b "$d/li_rho.cube" \
    --out "$d/${c}_cdd.cube" && echo "[$c] -> $d/${c}_cdd.cube"
done

echo ""; echo "===== CDD cube (VESTA로 iso ~0.002~0.005 e/Bohr^3, 노랑+ 청록-) ====="
ls -la $CDD/*/*_cdd.cube 2>/dev/null
echo ">> cube 3개 가져오면 .vesta 페어 + 그림(노랑축적/청록결핍) 만들어줄게 (Liu f/g 대응)."
