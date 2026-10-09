#!/usr/bin/env bash
# Li2S 2x2x2 NEB cell-convergence chain (card li2s_neb_cellconv_estimand_2026_10_09 · G1/G2 gates)
# What it does: endpoints relax (G1) -> no-CI build -> NEB no-CI (G2a) -> ci + rebuild --ci_scheme auto --restart -> NEB CI (G2b).
# Env (all required): W=worktree D=db/inputs/li2s_neb_cellconv_2026_10_09 UPY=python with ase WORK=run dir PW NEB MPIRUN.
# Exit: 0 done · 11 G1 endpoint not converged · 12 no neb.in · 13 no-CI not converged · 14 CI build failed · 15 CI stage not converged or not CI.
# Cannot: judge G3-G5 (symmetry, payload diff, MEP shape) -- done after collection in the repo. Does not stop on GPU total; watch does.
# Tested 2026-10-09 with a stub runner: pass rc 0 · G1 fail 11 · G2a fail 13 · G2b (output not CI) 15 · missing env refuses.
set -u
: "${W:?}" "${D:?}" "${UPY:?}" "${WORK:?}" "${PW:?}" "${NEB:?}" "${MPIRUN:?}"
export WORK PW NEB MPIRUN OMP_NUM_THREADS=1
cd "$W" || exit 2
L=$WORK/li2s
st(){ echo "[$(date '+%F %T')] ■ $*"; }
B(){ "$UPY" tools/sei/build_neb_inputs.py --work "$WORK" --pseudo_dir "$W/$D/pseudo" --relaxed_from "$W/$D/relaxed" --only li2s --min_l 8 "$@"; }
st "start · HEAD $(git -C "$W" rev-parse --short HEAD) · GPU $(nvidia-smi --query-gpu=memory.used --format=csv,noheader)"
st "1 endpoints relax"; bash tools/sei/run_sei_neb.sh endpoints li2s
for e in ep_initial ep_final; do
  grep -aq "Begin final coordinates" "$L/$e/relax.out" || { st "STOP G1: $e not converged"; exit 11; }; done
st "G1 ok"
st "2 build no-CI"; B > "$WORK/build_noCI.log" 2>&1; [ -f "$L/neb.in" ] || { st "STOP: no neb.in"; tail -5 "$WORK/build_noCI.log"; exit 12; }
st "3 NEB no-CI"; bash tools/sei/run_sei_neb.sh li2s
grep -aq "neb: convergence achieved" "$L/neb.out" || { st "STOP G2a: no-CI not converged"; exit 13; }
st "G2a ok"; grep -a "activation energy" "$L/neb.out" | tail -2
st "4 CI stage"; bash tools/sei/run_sei_neb.sh ci li2s
B --ci_scheme auto --restart > "$WORK/build_CI.log" 2>&1 || { st "STOP: CI build failed"; tail -5 "$WORK/build_CI.log"; exit 14; }
st "5 NEB CI"; bash tools/sei/run_sei_neb.sh li2s
{ grep -aq "neb: convergence achieved" "$L/neb.out" && grep -aqE "CI_scheme[[:space:]]*=[[:space:]]*'?auto" "$L/neb.out"; } || { st "STOP G2b: CI not converged"; exit 15; }
st "DONE G2b ok"; grep -a "activation energy" "$L/neb.out" | tail -2
