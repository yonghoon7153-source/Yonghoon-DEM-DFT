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
#  ★★★ 2026-08-30 (Codex R15 F, P1) — **한 배치 안에서 σ_SE 를 섞지 않는다.**
#    원래 주석대로 F(형성인자)는 σ_SE 에 선형이라 "아무 값이나" 수학적으로는 맞다.
#    그런데 JSON 은 F 를 안 적고 `sigma_ion_eff_mS_cm_mean` 만 적는다 ⇒ 원자료를 읽는
#    사람은 σ 를 직접 비교하게 되고, 배치 안에서 σ_SE 가 다르면 **b 효과와 σ_SE 효과가
#    갈리지 않는다.**  2026-08-25 원자료가 실제로 그랬다 (b 0/0.12/0.24/0.36 은 0.003,
#    0.17/0.21 은 0.00357 — 19 % 차).  정규화로 복구는 되지만, 정규화가 필요하다는 것
#    자체가 등록 밖 축이 배치에 있었다는 뜻이다.
#  ⇒ 기본을 **Fig 2f neat 값 3.57e-3** 으로 두어 σ 를 그대로 읽어도 안전하게 만든다.
#    (F 기반 동결은 그대로다 — 아래 [F] 행이 F 를 명시적으로 찍는다.)
SIG0=${SIG0:-3.57e-3}         # 매트릭스 σ_ion (S/cm) = Fig 2f neat.  배치 전체 단일값.

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
#  ★ 격자 = 사전등록 v2 §2-1 (원자료가 증언한 실제 격자).  0.17·0.21 이 빠져 있었고
#    그 둘이 바로 표적 0.97 을 둘러싸는 구간이다 (R15 F, P1).
for B in 0 0.12 0.17 0.21 0.24 0.36; do
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

#  ★★★ 2026-08-30 (R15 F) — **F(형성인자)를 명시적으로 찍는다.**
#    JSON 은 sigma_ion_eff 만 적어서, 읽는 사람이 σ 를 직접 비교하다 σ_SE 축을 놓친다.
#    F = σ_eff / σ_SE 가 이 계의 불변량이므로 그것을 배치 끝에서 표로 낸다.
echo
echo "── [F] 형성인자 (σ_eff / σ_SE) — 이것이 σ_SE 에 불변인 양이다 ──"
$PY - "$OUT" <<'PYF'
import json, glob, os, sys
out = sys.argv[1]
print(f"  {'파일':26s} {'σ_SE':>9s} {'σ_ion mS/cm':>12s} {'F':>10s} {'시드SE(log10)':>13s}")
for f in sorted(glob.glob(os.path.join(out, '*.json'))):
    d = json.load(open(f)); a = d.get('arm') or {}; g = d.get('agg') or {}
    se = a.get('sigma_ion_se'); s_ = g.get('sigma_ion_eff_mS_cm_mean')
    F = (s_ / 1000.0 / se) if (se and s_ is not None) else None
    print(f"  {os.path.basename(f)[:-5]:26s} {str(se):>9s} "
          f"{('%.6f' % s_) if s_ is not None else '—':>12s} "
          f"{('%.6f' % F) if F is not None else '—':>10s} "
          f"{('%.2e' % g['log10_ion_se']) if g.get('log10_ion_se') is not None else '—':>13s}")
_se = {a for a in (json.load(open(f)).get('arm', {}).get('sigma_ion_se')
                   for f in glob.glob(os.path.join(out, '*.json'))) if a is not None}
print(f"  ⇒ 이 배치의 σ_SE 집합: {sorted(_se)}"
      + ("" if len(_se) == 1 else "   ⚠⚠ 하나가 아니다 — σ 를 직접 비교하지 말 것 (R15 F)"))
PYF

cat <<'EOF'
── STAGE 1 끝.  다음 (prereg 원장 순서 — 사람이 동결):
  ① σ_ion(SE)* = 3.57e-3 / F̄(neat)                       [neat_ion.json]
  ② block_um*  — ⚠⚠ **가까운 그리드점을 고르지 않는다** (사전등록 v2 §2-1·§6, R15 F).
       표적 0.97 mS/cm 이 인접 두 격자점 **사이**에 있으면 판정은 `UNREACHABLE` 이고
       **브래킷 두 값을 보고**한다.  2026-08-25 배치가 정확히 그랬다 —
       단일 σ_SE 로 정규화하면 b=0.12 → 1.5175 · b=0.17 → 0.7170 이고 표적이 그 사이라,
       선택됐던 0.17 은 표적 대비 **−26.1 %** 였다.  그것을 "보정 성공" 으로 적으면 안 된다.
       ★ EDT 가 복셀 껍질로 양자화된다 (vox 0.12 → 다음 껍질 0.12·√2 = 0.169706)
         ⇒ **연속 최적화가 원리적으로 불가능**하다.  더 촘촘한 b 를 넣어도 같은 껍질이면
         같은 값이 나온다.  브래킷을 좁히려면 **vox 를 바꿔야** 하고 그것은 다른 규약이다.
       [ptfe_ion_blk*.json]
  ③ σ_ion(SDCP)* — 불활성(0)로 2.86 재현되는지 먼저 확인    [sdcp_ion.json]
  → 동결 후 STAGE 2 (전자축 ④⑤⑥ + T1–T3), 예:
     python3 scripts/pellet_rve_sigma.py --binder ptfe --binder-d-um 0.30 --box-um 6 \
         --vox 0.12 --seeds 4 --sigma-ion-se <①*> --ptfe-block-um <②*> \
         --sigma-e-se <④*>  --out .../ptfe_e_frozen.json     # T1: σ_e 예측 (자유도 0)
     python3 scripts/pellet_rve_sigma.py --binder sdcp --binder-d-um 0.30 --box-um 6 \
         --vox 0.12 --seeds 4 --sigma-e-se <④*> --sigma-e-sdcp <⑥ 보정> \
         --out .../sdcp_e_calib.json                          # ⑥ + T2 스패닝
EOF
