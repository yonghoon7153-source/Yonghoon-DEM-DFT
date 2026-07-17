#!/usr/bin/env bash
# =============================================================================
# run_b2o3_elastic_kgy.sh — b2o3 elastic RETRY on kgy (RTX3090), 2026-07-17.
#
# 왜 재도전: KISTI 07-03 relaxed-ion (h=0.005)에서 shear가 ±비틀기 국소최소 분기로
# 오염 (C66 붕괴, 고유값 -2.87, E_VRH -107.7 폐기; kb/results/b2o3_elastic_analysis).
# 처방 그대로: strain 0.01 (신호 2배) + forc_conv 1e-4 강화, 12종 전부 0.01 통일.
#
# 준비물 ($HOME/work/b2o3_elastic 에):
#   relax_v0.in / relax_v0.out / pseudo/   <- KISTI b2o3_eos 에서 tar-pipe 전송
# 발사 (MD 종료 감지 후 자동 — 별도 waiter tmux가 이 스크립트를 부름):
#   bash ~/Yonghoon-DEM-DFT/tools/elastic/run_b2o3_elastic_kgy.sh
#
# VRAM 프로브: 첫 스트레인(strain_11_p)이 OOM/실패하면 즉시 중단하고 gabia 폴백을
# 안내한다 (128원자 @ 24 GB는 간당간당 — 실패해도 아무것도 잃지 않는 설계).
# =============================================================================
set -u; set +H
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
W=$HOME/work/b2o3_elastic
STRAIN=0.01
cd "$W" || { echo "ERROR: $W 없음 (KISTI 전송 먼저)"; exit 1; }
for f in relax_v0.in relax_v0.out; do
    [ -s "$f" ] || { echo "ERROR: $W/$f 없음"; exit 1; }
done
[ -d pseudo ] || { echo "ERROR: $W/pseudo 없음"; exit 1; }

# ---- QE 자동 탐지 (kgy: pw.x는 RPATH로 lib 절대경로 참조 → env 불요) ----
PW=${PW:-$(find "$HOME/apps" "$HOME" -maxdepth 4 -name pw.x -path "*qe*gpu*bin*" 2>/dev/null | head -1)}
[ -n "$PW" ] || PW=$(find "$HOME/apps" -maxdepth 4 -name pw.x -path "*bin*" 2>/dev/null | head -1)
[ -n "$PW" ] || { echo "ERROR: pw.x 못 찾음 — PW=/path/to/pw.x 로 지정"; exit 1; }
# mpirun: PATH → openmpi-4.1.6(DOS 때 사용) → hpcx. 없으면 단일랭크 직접 실행.
MPIRUN=${MPIRUN:-$(command -v mpirun 2>/dev/null)}
[ -n "$MPIRUN" ] || MPIRUN=$(find "$HOME/apps" -maxdepth 5 -name mpirun -path "*openmpi*bin*" 2>/dev/null | head -1)
[ -n "$MPIRUN" ] || MPIRUN=$(find "$HOME/apps" -maxdepth 6 -name mpirun -path "*hpcx*bin*" 2>/dev/null | head -1)
echo "pw.x   = $PW"
echo "mpirun = ${MPIRUN:-<none, 단일랭크 직접실행>}"
RUN() { if [ -n "$MPIRUN" ]; then "$MPIRUN" -np 1 "$PW" -npool 1 -in "$1"; else "$PW" -npool 1 -in "$1"; fi; }

wait_gpu() {   # MD 뒤끝/타 프로세스 대비
    while :; do
        free=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits -i 0 2>/dev/null | head -1)
        [ "${free:-0}" -ge 20000 ] && break
        echo "[$(date +%H:%M:%S)] GPU free ${free} MiB < 20000 — wait"; sleep 120
    done
}

# ---- 1) 12개 strain 입력 생성 (h=0.01) ----
if [ ! -f strains/strain_11_p.in ]; then
    python3 "$REPO/tools/comp1_v3/build_elastic_strain_inputs.py" \
        --relaxed_ion --src_in "$W/relax_v0.in" --src_out "$W/relax_v0.out" \
        --strain "$STRAIN" --workdir "$W/strains" --prefix_base strain
fi
cd "$W/strains"
TAGS="strain_11_p strain_11_m strain_22_p strain_22_m strain_33_p strain_33_m \
      strain_23_p strain_23_m strain_13_p strain_13_m strain_12_p strain_12_m"
for t in $TAGS; do
    sed -i "s|outdir *=.*|outdir='./tmp_$t'|; s|prefix *=.*|prefix='$t'|; s|pseudo_dir *=.*|pseudo_dir='$W/pseudo'|" "$t.in"
    # 처방 ②: forc_conv 강화 (shear 오염 억제)
    if grep -q "forc_conv_thr" "$t.in"; then
        sed -i "s|forc_conv_thr *=.*|forc_conv_thr = 1.0d-4|" "$t.in"
    else
        sed -i "/calculation/a\    forc_conv_thr = 1.0d-4" "$t.in"
    fi
done

# ---- 2) VRAM 프로브 = 첫 스트레인 ----
t=strain_11_p
if ! grep -q "JOB DONE" "$t.out" 2>/dev/null; then
    wait_gpu
    echo "[$(date +%H:%M:%S)] VRAM probe: $t (128 at @ 24 GB — 실패하면 gabia 폴백)"
    RUN "$t.in" > "$t.out" 2>&1
    if ! grep -q "JOB DONE" "$t.out"; then
        echo "!!!!! PROBE FAIL — tail:"; tail -15 "$t.out"
        echo "!!!!! 3090 VRAM 부족 추정 → b2o3 elastic은 gabia 큐(phaseb 뒤)로 폴백하세요."
        exit 1
    fi
    echo "PROBE OK — 나머지 11개 진행"
fi

# ---- 3) 나머지 11개 ----
for t in $TAGS; do
    grep -q "JOB DONE" "$t.out" 2>/dev/null && { echo "[$t] done — skip"; continue; }
    wait_gpu
    echo "[$(date +%H:%M:%S)] pw.x $t"
    RUN "$t.in" > "$t.out" 2>&1
    grep -q "JOB DONE" "$t.out" && echo "[$t] OK" || { echo "[$t] FAIL — tail:"; tail -10 "$t.out"; }
done

# ---- 4) fit ----
echo "[$(date +%H:%M:%S)] fit Cij (h=$STRAIN):"
python3 "$REPO/tools/modelc_v3/fit_elastic_cij_stress.py" --workdir "$W/strains" --strain "$STRAIN" \
    | tee "$W/elastic_fit_b2o3_h01.txt" || echo "fit FAIL (미완 strain 확인)"
echo "done. 결과: $W/elastic_fit_b2o3_h01.txt — 고유값 검진은 붙여넣으면 처리"
