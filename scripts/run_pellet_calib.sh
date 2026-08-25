#!/usr/bin/env bash
# B 트랙 (D13 이온 보정) STAGE 1 — 측정 팔 일괄 실행.
# 실행 계약: docs/reviews/sdcp_ion_calib_prereg_20260825.md (판정선은 그 문서 소관 —
# 이 러너는 측정만 한다.  보정값 동결(①~④⑥)은 STAGE 1 결과를 보고 **사람이** prereg
# 원장 순서대로 한다).
#
#   bash scripts/run_pellet_calib.sh                # kgy CPU, 수 분
#   SEEDS=6 bash scripts/run_pellet_calib.sh        # 시드 증원 (SE 요건 미달 시)
#
# 실행 규약 (런 전 선언 — prereg §8 의 구체화):
#   · binder 구 지름 = Ø0.30 µm — SDCP 는 리포 Ø0.30 규약 그대로.  PTFE 는 실측 입도가
#     없어 **같은 값을 임의 규약**으로 쓴다 (§F1: 값을 지어내는 대신 규약을 선언하고
#     d-감도를 관측량으로 기록한다 → D_SWEEP 팔).
#   · box 6 µm (= 20 지름) · vox 0.12 (d/vox 2.5 ≥ 2) · 시드 4 (prereg ≥4).
#   · 차단 노브 그리드 {0.12, 0.24, 0.36} µm — vox 양자화(스텝 ≈ vox)에 맞춘 격자.
#     0 은 스탬프-만 팔(§6-1 희석 관측)과 같다.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

PY=${PY:-python3}
SEEDS=${SEEDS:-4}
BOX=${BOX:-6}
VOX=${VOX:-0.12}
D=${D:-0.30}
OUT=${OUT:-docs/data/pellet_calib_20260825}
SIG0=${SIG0:-3.0e-3}          # 임시 매트릭스 σ_ion (S/cm) — F 는 선형이라 아무 값이나 되고,
                              # ① 동결은 F̄ 로 산술 (σ* = 3.57e-3 / F̄_neat)

mkdir -p "$OUT"
echo "── STAGE 1 측정 (${SEEDS} 시드 · box ${BOX} · vox ${VOX} · d ${D}) → $OUT"

echo "[1/4] neat (① 정규화용 F)"
$PY scripts/pellet_rve_sigma.py --binder none --box-um "$BOX" --vox "$VOX" \
    --seed 1 --seeds "$SEEDS" --sigma-ion-se "$SIG0" --out "$OUT/neat_ion.json"

echo "[2/4] +SDCP (③ — 불활성 가설 σ_ion_sdcp=0 + T2 스패닝 관측)"
$PY scripts/pellet_rve_sigma.py --binder sdcp --binder-d-um "$D" --box-um "$BOX" \
    --vox "$VOX" --seed 1 --seeds "$SEEDS" --sigma-ion-se "$SIG0" \
    --out "$OUT/sdcp_ion.json"

echo "[3/4] +PTFE (② — 차단 노브 그리드; 0 = 스탬프-만 희석 관측 §6-1)"
for B in 0 0.12 0.24 0.36; do
  $PY scripts/pellet_rve_sigma.py --binder ptfe --binder-d-um "$D" --box-um "$BOX" \
      --vox "$VOX" --seed 1 --seeds "$SEEDS" --sigma-ion-se "$SIG0" \
      --ptfe-block-um "$B" --out "$OUT/ptfe_ion_blk${B}.json"
done

echo "[4/4] 감도 — ρ_SDCP 1.1/1.7 (prereg §4 뒤집힘 검사) + d-스윕 (구 지름 규약 감도)"
for R in 1.1 1.7; do
  $PY scripts/pellet_rve_sigma.py --binder sdcp --binder-d-um "$D" --box-um "$BOX" \
      --vox "$VOX" --seed 1 --seeds "$SEEDS" --sigma-ion-se "$SIG0" \
      --rho-binder "$R" --out "$OUT/sdcp_ion_rho${R}.json"
done
for DD in 0.6 1.2; do
  $PY scripts/pellet_rve_sigma.py --binder ptfe --binder-d-um "$DD" --box-um "$BOX" \
      --vox "$VOX" --seed 1 --seeds "$SEEDS" --sigma-ion-se "$SIG0" \
      --out "$OUT/ptfe_ion_d${DD}.json"
done

cat <<'EOF'
── STAGE 1 끝.  다음 (prereg 원장 순서 — 사람이 동결):
  ① σ_ion(SE)* = 3.57e-3 / F̄(neat)                       [neat_ion.json]
  ② block_um*  = 이온 +PTFE 0.97 mS/cm 재현하는 그리드점    [ptfe_ion_blk*.json]
  ③ σ_ion(SDCP)* — 불활성(0)로 2.86 재현되는지 먼저 확인    [sdcp_ion.json]
  → 동결 후 STAGE 2 (전자축 ④⑤⑥ + T1–T3), 예:
     python3 scripts/pellet_rve_sigma.py --binder ptfe --binder-d-um 0.30 --box-um 6 \
         --vox 0.12 --seeds 4 --sigma-ion-se <①*> --ptfe-block-um <②*> \
         --sigma-e-se <④*>  --out .../ptfe_e_frozen.json     # T1: σ_e 예측 (자유도 0)
     python3 scripts/pellet_rve_sigma.py --binder sdcp --binder-d-um 0.30 --box-um 6 \
         --vox 0.12 --seeds 4 --sigma-e-se <④*> --sigma-e-sdcp <⑥ 보정> \
         --out .../sdcp_e_calib.json                          # ⑥ + T2 스패닝
EOF
