#!/bin/bash
#SBATCH -J li3n_drag
#SBATCH -p amd_a100nv_8
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --gres=gpu:2
#SBATCH --time=04:00:00
#SBATCH -o /scratch/x3430a02/kgy/li3n_drag_dft/logs/li3n_drag_%j.out
#SBATCH -e /scratch/x3430a02/kgy/li3n_drag_dft/logs/li3n_drag_%j.err
#SBATCH --comment qe

# ============================================================
# Li3N DFT drag (Kim&Cui reference method) — KISTI 4h chain segment.
# 9 constrained relaxes drag_p0..p8 (adatom xy pinned/z free, bottom slab
# frozen) over 2 GPUs. lpsocl 체인과 동일 설계:
#   - JOB DONE  -> skip
#   - 미완      -> 마지막 ATOMIC_POSITIONS carry (이온 진행 승계) 후 재시작
#   - 9/9 완료  -> ALL_DONE + 프로파일 자동 파싱 (drag_result.json)
# 제출: submit 4개 afterany 체인 (lpsocl 패턴 그대로)
# ============================================================

WORK_BASE=/scratch/x3430a02/kgy/li3n_drag_dft
PW=/scratch/x3430a02/kgy/apps/qe-gpu/bin/pw.x
export OMP_NUM_THREADS=8

mkdir -p $WORK_BASE/logs
cd $WORK_BASE

if [ -f ALL_DONE ]; then
    echo "ALL_DONE present — nothing to do."; exit 0
fi

echo "===== Li3N drag segment  job=$SLURM_JOB_ID  $(date) ====="

run_stream () {          # $1 = GPU id, $2.. = point tags (p0 p2 ...)
    local gpu=$1; shift
    for v in "$@"; do
        local fin=$WORK_BASE/drag_${v}.in
        local fout=$WORK_BASE/drag_${v}.out
        [ -f "$fin" ] || { echo "[$v] drag_${v}.in missing — generate first"; continue; }
        if grep -q "JOB DONE" "$fout" 2>/dev/null; then
            echo "[$v] already done — skip"; continue
        fi
        if [ -f "$fout" ]; then
            nat=$(awk '/number of atoms\/cell/{print $5; exit}' "$fout")
            ln=$(grep -n "ATOMIC_POSITIONS" "$fout" | tail -1 | cut -d: -f1)
            got=""
            if [ -n "$nat" ] && [ -n "$ln" ]; then
                sed -n "${ln},$((ln+nat))p" "$fout" > "$WORK_BASE/.carry_${v}"
                nl=$(( $(wc -l < "$WORK_BASE/.carry_${v}") - 1 ))
                if [ "$nl" -eq "$nat" ]; then
                    lin=$(grep -n "ATOMIC_POSITIONS" "$fin" | head -1 | cut -d: -f1)
                    { head -n $((lin-1)) "$fin"; cat "$WORK_BASE/.carry_${v}"; \
                      tail -n +$((lin+nat+1)) "$fin"; } > "${fin}.new" \
                        && mv "${fin}.new" "$fin" && got=1
                fi
            fi
            [ -n "$got" ] && echo "[$v] incomplete — carried last geometry (nat=$nat)" \
                          || echo "[$v] incomplete — no carry info, fresh start"
            rm -rf "$WORK_BASE/tmp_${v}" "$fout" "$WORK_BASE/.carry_${v}"
        fi
        echo "[$v] START on GPU $gpu  $(date)"
        ( cd "$WORK_BASE" && CUDA_VISIBLE_DEVICES=$gpu $PW -in "drag_${v}.in" > "$fout" 2>&1 )
        grep -q "JOB DONE" "$fout" && echo "[$v] DONE  $(date)" \
                                   || echo "[$v] NOT finished (wall/error)  $(date)"
    done
}

run_stream 0 p0 p2 p4 p6 p8 &
P0=$!
run_stream 1 p1 p3 p5 p7 &
P1=$!
wait $P0 $P1

n_done=$(grep -l "JOB DONE" $WORK_BASE/drag_p*.out 2>/dev/null | wc -l)
echo "===== segment end: $n_done/9 points complete  $(date) ====="
if [ "$n_done" -eq 9 ]; then
    touch $WORK_BASE/ALL_DONE
    echo "ALL 9 DRAG POINTS DONE — parsing profile"
    python3 - <<'PY'
import re, json
E = []
for k in range(9):
    t = open(f"drag_p{k}.out", errors="ignore").read()
    m = re.findall(r"^!.*total energy\s*=\s*(-?\d+\.\d+)\s*Ry", t, re.M)
    E.append(float(m[-1]) * 13.605693 if m else None)
if all(e is not None for e in E):
    rel = [e - E[0] for e in E]
    print(f"{'pt':>4} {'E_rel(eV)':>12}")
    for k, r in enumerate(rel):
        print(f"{k:>4} {r:>12.4f}")
    print(f"barrier(max-min) = {max(rel)-min(rel):.4f} eV")
    json.dump({"E_eV": E, "rel_eV": rel, "barrier_eV": max(rel) - min(rel),
               "mode": "relax", "n_points": 9}, open("drag_result.json", "w"), indent=2)
    print("-> drag_result.json")
else:
    print("incomplete:", [i for i, e in enumerate(E) if e is None])
PY
fi
