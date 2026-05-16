
#!/bin/bash

QE=/scratch/x3430a02/kgy/apps/qe-gpu/bin/pw.x

export CUDA_VISIBLE_DEVICES=0



# === 1. comp1 v2 DFT EOS (K=3x3x3) ===

echo "=== comp1 v2 DFT EOS (K=3x3x3) ==="

cd /scratch/x3430a02/kgy/manuscript_support/pipeline_v2/comp1_lpscl



# K_POINTS 수정

for f in comp1_v2_eos_v*.in; do

  sed -i 's/  2 2 2  0 0 0/  3 3 3  0 0 0/' "$f"

done



for V in 097 098 099 100 101 102 103 104 105 106 107; do

    IN="comp1_v2_eos_v${V}.in"

    echo "  v${V}..."

    

    for TRY in $(seq 0 5); do

        if [ $TRY -eq 0 ]; then

            OUT="comp1_v2_eos_v${V}.out"

            rm -rf "tmp_v${V}"

            mkdir -p "tmp_v${V}"

        else

            PREV=$(ls -t comp1_v2_eos_v${V}*.out 2>/dev/null | head -1)

            JD=$(grep -c "JOB DONE" "$PREV" 2>/dev/null)

            if [ "$JD" -gt 0 ]; then echo "    JOB DONE!"; break; fi

            

            strings "$PREV" | tac | grep -m1 -B55 "ATOMIC_POSITIONS" | tac > tmp_coords_${V}.txt

            NL=$(wc -l < tmp_coords_${V}.txt)

            if [ "$NL" -lt 50 ]; then echo "    좌표 실패"; break; fi

            

            OUT="comp1_v2_eos_v${V}_r${TRY}.out"

            NEW_IN="comp1_v2_eos_v${V}_r${TRY}.in"

            sed -n '1,/ATOMIC_POSITIONS/p' "$IN" > "$NEW_IN"

            cat tmp_coords_${V}.txt >> "$NEW_IN"

            sed -i "s/comp1_v2_v${V}/comp1_v2_v${V}_r${TRY}/" "$NEW_IN"

            sed -i "s|outdir.*|outdir = './tmp_v${V}_r${TRY}/'|" "$NEW_IN"

            mkdir -p "tmp_v${V}_r${TRY}"

            IN="$NEW_IN"

        fi

        mpirun -np 1 $QE -in "$IN" > "$OUT" 2>&1

        E=$(grep "!" "$OUT" | tail -1 | awk '{print $5}')

        F=$(grep "Total force" "$OUT" | tail -1 | awk '{print $4}')

        echo "    try$TRY: E=$E F=$F"

    done

    

    FINAL=$(ls -t comp1_v2_eos_v${V}*.out 2>/dev/null | head -1)

    E=$(grep "!" "$FINAL" | tail -1 | awk '{print $5}')

    echo "  v${V} final: $E"

done

echo "=== comp1 v2 EOS DONE ==="



# === 2. Model C Basin B EOS ===

echo ""

echo "=== Model C Basin B EOS ==="

cd /scratch/x3430a02/kgy/manuscript_support/modelC_lpsc16/eos_relax



# v103f106 좌표 추출 (Basin B ground state)

tac modelC_v103f106_final.out | grep -m1 -B65 "ATOMIC_POSITIONS" | tac > basinB_coords.txt

NL=$(wc -l < basinB_coords.txt)

echo "  Basin B coords: $NL lines"



# v096~v105 input 생성 (Basin B 좌표 + 각 volume cell)

for V in 096 097 098 099 100 101 102 103 104 105; do

    # 기존 Basin A input에서 header+cell 가져오기

    if [ -f "modelC_eos_v${V}.in" ]; then

        SRC="modelC_eos_v${V}.in"

    elif [ "$V" = "103" ]; then

        SRC="modelC_eos_v103.in"

    elif [ "$V" = "105" ]; then

        SRC="modelC_eos_v105.in"

    else

        echo "  v${V}: source not found, skip"

        continue

    fi

    

    OUT_IN="modelC_basinB_v${V}.in"

    sed -n '1,/ATOMIC_POSITIONS/p' "$SRC" > "$OUT_IN"

    cat basinB_coords.txt >> "$OUT_IN"

    sed -i "s/modelC_eos_v${V}/modelC_bB_v${V}/" "$OUT_IN"

    sed -i "s|outdir.*|outdir = './tmp_bB_v${V}/'|" "$OUT_IN"

    sed -i "s|/home/ubuntu/runyourai/bml/manuscript_support/pseudo/|/home01/x3430a02/pseudo/SSSP_1.3.0_PBE_efficiency/|" "$OUT_IN"

    mkdir -p "tmp_bB_v${V}"

done



for V in 096 097 098 099 100 101 102 103 104 105; do

    IN="modelC_basinB_v${V}.in"

    if [ ! -f "$IN" ]; then continue; fi

    echo "  v${V}..."

    

    for TRY in $(seq 0 5); do

        if [ $TRY -eq 0 ]; then

            OUT="modelC_basinB_v${V}.out"

        else

            PREV=$(ls -t modelC_basinB_v${V}*.out 2>/dev/null | head -1)

            JD=$(grep -c "JOB DONE" "$PREV" 2>/dev/null)

            if [ "$JD" -gt 0 ]; then echo "    JOB DONE!"; break; fi

            

            strings "$PREV" | tac | grep -m1 -B65 "ATOMIC_POSITIONS" | tac > tmp_bB_coords.txt

            NL=$(wc -l < tmp_bB_coords.txt)

            if [ "$NL" -lt 60 ]; then echo "    좌표 실패"; break; fi

            

            OUT="modelC_basinB_v${V}_r${TRY}.out"

            NEW_IN="modelC_basinB_v${V}_r${TRY}.in"

            sed -n '1,/ATOMIC_POSITIONS/p' "$IN" > "$NEW_IN"

            cat tmp_bB_coords.txt >> "$NEW_IN"

            sed -i "s/modelC_bB_v${V}/modelC_bB_v${V}_r${TRY}/" "$NEW_IN"

            sed -i "s|outdir.*|outdir = './tmp_bB_v${V}_r${TRY}/'|" "$NEW_IN"

            mkdir -p "tmp_bB_v${V}_r${TRY}"

            IN="$NEW_IN"

        fi

        mpirun -np 1 $QE -in "$IN" > "$OUT" 2>&1

        E=$(grep "!" "$OUT" | tail -1 | awk '{print $5}')

        F=$(grep "Total force" "$OUT" | tail -1 | awk '{print $4}')

        echo "    try$TRY: E=$E F=$F"

    done

    

    FINAL=$(ls -t modelC_basinB_v${V}*.out 2>/dev/null | head -1)

    E=$(grep "!" "$FINAL" | tail -1 | awk '{print $5}')

    echo "  v${V} final: $E"

done

echo "=== Model C Basin B EOS DONE ==="



echo ""

echo "===== ALL DONE ====="

