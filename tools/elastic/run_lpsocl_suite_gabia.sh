#!/usr/bin/env bash
# =============================================================================
# run_lpsocl_suite_gabia.sh — LPSOCl(V0, 62 at) full DFT suite on gabia (A6000)
#   + Phase-B VERDICT relax check, one sequential tmux chain (single GPU).
#
# Stages (arg = all|scf|pp|bader|lobster|elastic|phaseb; default all):
#   scf      02_scf.in rerun on gabia (save needed for pp/LOBSTER; conv 1e-8)
#   pp       ELF cube (plot_num=8) + valence-density cube (plot_num=0)
#   bader    bader -p all_atom on the density cube (USPP valence = 근사, 상대비교)
#   lobster  all-PAW scf+nscf (extended basis, nbnd 500) -> LOBSTER 5.1.1 ICOHP
#            (LOBSTER는 USPP 거부 "Wrong potential!" — b2o3 icohp_paw 경로 그대로)
#   elastic  12 relaxed-ion strain relaxes (±0.005, 6 Voigt) -> full Cij -> E_VRH
#            (recipe cloned from 01_relax_v0.in: ecut 60/480, mv 0.01, k 2 2 1)
#   phaseb   VERDICT robustness: complex_{doped,neutral} molecule-only BFGS relax
#            (make_phaseB_relax_check.py; slab frozen -> E_bind refs unchanged)
#
# Prereqs (already done 2026-07-17): kgy -> /data/work/runs/lpsocl_dft/
#   {01_relax_v0.in,01_relax_v0.out,02_scf.in,03_nscf_dos.in,lpsocl_v0_kit.tgz}
#
# Launch:
#   cd ~/work/Yonghoon-DEM-DFT && git pull
#   tmux new -s lpsocl_suite -d 'bash ~/work/Yonghoon-DEM-DFT/tools/elastic/run_lpsocl_suite_gabia.sh \
#       > /data/work/runs/lpsocl_dft/suite.log 2>&1'
#   tail -f /data/work/runs/lpsocl_dft/suite.log
# Resume-safe: every stage skips on its done-marker; rerun continues the chain.
# pw.x와 UMA 동시 실행 금지 규율: wait_gpu가 각 단계 전에 VRAM을 확인한다.
# =============================================================================
set -u; set +H
REPO=${REPO:-$HOME/work/Yonghoon-DEM-DFT}
WORK=/data/work/runs/lpsocl_dft
PB=/data/work/runs/sdcp_linio2_binding/phaseB_v7c
STAGE=${1:-all}

# ---- gabia QE-GPU env (run_phaseB_gabia.sh와 동일) ----
HPCX=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi
export PATH=$HPCX/bin:$PATH
export LD_LIBRARY_PATH=$HPCX/lib:/data/apps/nvhpc/Linux_x86_64/24.11/compilers/lib:/usr/local/cuda-12.6/lib64:${LD_LIBRARY_PATH:-}
export OPAL_PREFIX=$HPCX
export OMP_NUM_THREADS=1 CUDA_VISIBLE_DEVICES=0
export OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
QE=/data/apps/qe-7.4.1-gpu/bin
MPIRUN=$HPCX/bin/mpirun
LOBSTER=/data/apps/lobster-5.1.1/lobster
BADER=/data/apps/bader/bader

ts() { date +%H:%M:%S; }
wait_gpu() {   # $1 = required free MiB
    local need=$1 free
    while :; do
        free=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits -i 0 2>/dev/null | head -1)
        [ -z "$free" ] && free=0
        [ "$free" -ge "$need" ] && { echo "[$(ts)] GPU free ${free} MiB >= ${need} — go"; return; }
        echo "[$(ts)] GPU free ${free} MiB < ${need} — wait"; sleep 60
    done
}
run_pw() {     # $1=input $2=output $3=needMiB   (skip if JOB DONE)
    if grep -q "JOB DONE" "$2" 2>/dev/null; then echo "[$(ts)] $2 already DONE — skip"; return 0; fi
    wait_gpu "$3"
    echo "[$(ts)] pw.x $1"
    "$MPIRUN" -np 1 "$QE/pw.x" -npool 1 -in "$1" > "$2" 2>&1
    grep -q "JOB DONE" "$2" && echo "[$(ts)] $1 OK" || { echo "[$(ts)] $1 FAIL — tail:"; tail -12 "$2"; return 1; }
}

cd "$WORK" || { echo "ERROR: $WORK 없음 (kgy 전송 확인)"; exit 1; }

# ---- Stage 0: kit unpack + pseudo_dir 경로 통일 (항상 실행, 멱등) ----
if [ ! -e .kit_ready ]; then
    mkdir -p kit_unpack && tar xzf lpsocl_v0_kit.tgz -C kit_unpack
    UPF1=$(find kit_unpack -name "*.UPF" | head -1)
    [ -n "$UPF1" ] || { echo "ERROR: kit에 UPF 없음"; exit 1; }
    ln -sfn "$(dirname "$UPF1")" pseudo_kit
    touch .kit_ready
fi
PSE=$WORK/pseudo_kit
echo "[$(ts)] pseudo_kit -> $(readlink -f pseudo_kit) ($(ls pseudo_kit/*.UPF 2>/dev/null | wc -l) UPFs)"
for f in 02_scf.in 03_nscf_dos.in; do
    sed -i "s|pseudo_dir *=.*|pseudo_dir = '$PSE'|" "$f"
done

# ---- [scf] ----
if [ "$STAGE" = all ] || [ "$STAGE" = scf ]; then
    echo "===== [scf] $(ts) ====="
    run_pw 02_scf.in 02_scf.out 6000 || exit 1
fi

# ---- [pp] ELF + rho cubes ----
if [ "$STAGE" = all ] || [ "$STAGE" = pp ]; then
    echo "===== [pp] $(ts) ====="
    test -d tmp/lpsocl_v0.save || { echo "ERROR: tmp/lpsocl_v0.save 없음 (scf 먼저)"; exit 1; }
    if [ ! -s lpsocl_elf.cube ]; then
        cat > pp_elf.in <<'EOF'
&INPUTPP
  prefix='lpsocl_v0', outdir='./tmp', plot_num=8, filplot='lpsocl_elf_pl'
/
&PLOT
  iflag=3, output_format=6, fileout='lpsocl_elf.cube'
/
EOF
        wait_gpu 4000
        "$MPIRUN" -np 1 "$QE/pp.x" -in pp_elf.in > pp_elf.out 2>&1
        echo "[$(ts)] ELF: $(ls -la lpsocl_elf.cube 2>/dev/null || echo FAIL)"
    fi
    if [ ! -s lpsocl_rho.cube ]; then
        cat > pp_rho.in <<'EOF'
&INPUTPP
  prefix='lpsocl_v0', outdir='./tmp', plot_num=0, filplot='lpsocl_rho_pl'
/
&PLOT
  iflag=3, output_format=6, fileout='lpsocl_rho.cube'
/
EOF
        wait_gpu 4000
        "$MPIRUN" -np 1 "$QE/pp.x" -in pp_rho.in > pp_rho.out 2>&1
        echo "[$(ts)] rho: $(ls -la lpsocl_rho.cube 2>/dev/null || echo FAIL)"
    fi
fi

# ---- [bader] ----
if [ "$STAGE" = all ] || [ "$STAGE" = bader ]; then
    echo "===== [bader] $(ts) ====="
    if [ -s ACF.dat ]; then echo "ACF.dat 있음 — skip"
    elif [ -s lpsocl_rho.cube ]; then
        "$BADER" -p all_atom lpsocl_rho.cube > bader_run.out 2>&1
        echo "[$(ts)] bader done; ACF.dat head:"; head -12 ACF.dat 2>/dev/null || tail -8 bader_run.out
    else echo "rho cube 없음 — skip"; fi
fi

# ---- [lobster] all-PAW scf+nscf -> LOBSTER (USPP는 LOBSTER가 거부 — b2o3 교훈) ----
if [ "$STAGE" = all ] || [ "$STAGE" = lobster ]; then
    echo "===== [lobster] $(ts) ====="
    # PAW(kjpaw) 6종 확보: O는 gabia에 이미 있고 나머지는 QE 사이트에서
    mkdir -p "$WORK/pseudo"
    cp -n /data/work/pseudo/O.pbe-n-kjpaw_psl.0.1.UPF "$WORK/pseudo/" 2>/dev/null || true
    bash "$REPO/tools/electronic/fetch_paw_pseudos.sh" "$WORK"
    NEED="Li.pbe-sl-kjpaw_psl.1.0.0.UPF P.pbe-n-kjpaw_psl.1.0.0.UPF S.pbe-nl-kjpaw_psl.1.0.0.UPF Cl.pbe-nl-kjpaw_psl.1.0.0.UPF O.pbe-n-kjpaw_psl.0.1.UPF"
    for f in $NEED; do
        [ -s "$WORK/pseudo/$f" ] || { echo "ERROR: PAW $f 없음 (인터넷/프록시 확인)"; exit 1; }
    done
    # extended-basis 입력 생성 (nbnd 500 >= basis 445 = Li27x5 + [P,S,Cl]34x9 + O1x4)
    if [ ! -f lobster_ext/lobster_scf.in ]; then
        python3 "$REPO/tools/comp1_v3/build_lobster_paw_inputs.py" \
            --src_in "$WORK/01_relax_v0.in" --src_out "$WORK/01_relax_v0.out" \
            --workdir "$WORK/lobster_ext" --pseudo_dir "$WORK/pseudo" --nbnd 500
    fi
    cd "$WORK/lobster_ext"
    run_pw lobster_scf.in lobster_scf.out 8000 || { cd "$WORK"; exit 1; }
    run_pw lobster_nscf.in lobster_nscf.out 10000 || { cd "$WORK"; exit 1; }
    ln -sfn tmp_V0_lobster_scf/V0_lobster_scf.save ./V0_lobster_scf.save
    # LOBSTER는 *scf.in을 QE 입력으로 읽음 -> nscf 내용(nbnd/wf_collect)으로 잠시 교체 (KISTI 흐름)
    [ -f lobster_scf.in.orig ] || cp lobster_scf.in lobster_scf.in.orig
    cp lobster_nscf.in lobster_scf.in
    if [ -s ICOHPLIST.lobster ]; then echo "ICOHPLIST 있음 — skip"
    else
        export OMP_NUM_THREADS=8
        echo "[$(ts)] LOBSTER start (OMP=8)"
        "$LOBSTER" > lobster_run.out 2>&1
        export OMP_NUM_THREADS=1
        echo "==== charge spilling (b2o3는 1.19%였음; <5%면 OK) ===="
        grep -iE "charge spilling" lobster_run.out | head -4
        echo "==== ICOHPLIST head ===="
        head -20 ICOHPLIST.lobster 2>/dev/null || tail -15 lobster_run.out
    fi
    cp lobster_scf.in.orig lobster_scf.in   # 원복
    cd "$WORK"
fi

# ---- [elastic] 12 relaxed-ion strains -> Cij -> E_VRH ----
if [ "$STAGE" = all ] || [ "$STAGE" = elastic ]; then
    echo "===== [elastic] $(ts) ====="
    if [ ! -f elastic/strain_11_p.in ]; then
        python3 "$REPO/tools/comp1_v3/build_elastic_strain_inputs.py" \
            --relaxed_ion --src_in "$WORK/01_relax_v0.in" --src_out "$WORK/01_relax_v0.out" \
            --strain 0.005 --workdir "$WORK/elastic" --prefix_base strain
    fi
    cd "$WORK/elastic"
    TAGS="strain_11_p strain_11_m strain_22_p strain_22_m strain_33_p strain_33_m \
          strain_23_p strain_23_m strain_13_p strain_13_m strain_12_p strain_12_m"
    for t in $TAGS; do
        sed -i "s|outdir *=.*|outdir='./tmp_$t'|; s|prefix *=.*|prefix='$t'|; s|pseudo_dir *=.*|pseudo_dir='$PSE'|" "$t.in"
    done
    for t in $TAGS; do
        run_pw "$t.in" "$t.out" 6000 || echo "  ($t FAIL — 나머지 계속, fit 전에 재실행 필요)"
    done
    echo "[$(ts)] fit Cij -> moduli:"
    python3 "$REPO/tools/modelc_v3/fit_elastic_cij_stress.py" --workdir "$WORK/elastic" --strain 0.005 \
        | tee "$WORK/elastic_fit.txt" || echo "fit FAIL (미완 strain 확인)"
    cd "$WORK"
fi

# ---- [phaseb] VERDICT relax check (doped 먼저 = 의심 자세) ----
if [ "$STAGE" = all ] || [ "$STAGE" = phaseb ]; then
    echo "===== [phaseb relax check] $(ts) ====="
    PHASEB_BASE=$PB python3 "$REPO/tools/sdcp/make_phaseB_relax_check.py"
    for t in complex_doped complex_neutral; do
        cd "$PB/$t"
        run_pw relax.in relax.out 30000 || { echo "$t relax FAIL"; cd "$WORK"; continue; }
        cd "$WORK"
    done
    echo "==== relaxed E_bind (Ry->eV; refs: slab -10563.22819091, mol_d -518.39271245, mol_n -519.68310300) ===="
    python3 - <<'PY'
import re, os
Ry = 13.605693
refs = {"complex_doped": -518.39271245, "complex_neutral": -519.68310300}
slab = -10563.22819091
base = "/data/work/runs/sdcp_linio2_binding/phaseB_v7c"
eb = {}
for t, mol in refs.items():
    p = os.path.join(base, t, "relax.out")
    if not os.path.exists(p):
        print(t, "relax.out 없음"); continue
    es = re.findall(r"^!\s+total energy\s+=\s+(-\d+\.\d+)", open(p, errors="ignore").read(), re.M)
    if not es:
        print(t, "수렴 에너지 아직 없음"); continue
    e = float(es[-1])
    eb[t] = (e - slab - mol) * Ry
    print(f"{t}: E={e:.8f} Ry ({len(es)} ionic steps) -> E_bind={eb[t]:+.4f} eV")
if len(eb) == 2:
    print(f"RELAXED VERDICT Delta(d-n) = {eb['complex_doped']-eb['complex_neutral']:+.4f} eV  (single-point was +0.689)")
PY
fi
echo "===== suite done $(ts) ====="
