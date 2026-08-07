#!/usr/bin/env bash
set -uo pipefail
# STEP4만 (재개/단독) — 사용법: bash step4_only.sh [런폴더]   (기본: latest_run)
KIT="$(cd "$(dirname "$0")" && pwd)"
SCR=""; for c in "$KIT/scripts" "$KIT/../scripts"; do [ -d "$c" ] && SCR="$(cd "$c" && pwd)" && break; done
[ -z "$SCR" ] && { echo "scripts/ 못 찾음 — 레포 루트에 킷을 푸세요"; exit 1; }
# scripts 자동 최신화 (버전 스큐 방지; 끄기 MPM_NO_PULL=1)
if [ -z "${MPM_NO_PULL:-}" ] && [ -d "$SCR/../.git" ]; then ( cd "$SCR/.." && git pull --ff-only ) || echo "  ⚠ git pull 스킵 — 기존 스크립트로 진행"; fi
RUN="${1:-$KIT/latest_run}"
[ -f "$RUN/step4_grid.npz" ] || { echo "step4_grid.npz 없음: $RUN — run_mpm.sh 먼저 (payload가 그리드 export)"; exit 1; }
if [ -z "${S4_DETACHED:-}" ]; then
  export S4_DETACHED=1
  log="$RUN/step4_run_$(date +%Y%m%d_%H%M%S).log"
  echo "→ detached — log: $log"
  setsid nohup bash "$0" "$@" >"$log" 2>&1 </dev/null &
  echo "   PID $!     follow: tail -f $log"
  exit 0
fi
cd "$RUN"
# 3) STEP4-v2 — ★Zive 스케줄 9스텝 (Loop 전개 → 총 12런) 순차 (charge-first, per-step 컷오프).
#    각 런은 독립 초기상태 (방전 = x0 충전상태에서, 충전 = x100 방전상태에서 시작).  그리드는 STEP 2가 export.
# ★STEP4 솔버 노브 (2026-07-27 near-null 대수술; docs/step4_bottleneck_analysis_20260727.md)
#   기본값 = 권장값.  런타임 env 로 override 가능 (예: MPM_S4_CONTRAST_CAP=200 bash step4_only.sh).
#   prune_float: 집전체·AM 무접촉 부유 e-클러스터 제거 = 정확특이 블록 소거(해-불변, GPU-CG 회생)
#   ew        : Eisenstat-Walker inexact Newton (기본 OFF — 측정 2건서 일량 증가, 이득 미입증)
#   gpu_amg   : AMG apply 를 GPU V-cycle 미러로 (빌드는 CPU 1회; cupy 없으면 자동 CPU 폴백)
#   contrast_cap: e-망 σ대비 상한 (0=OFF).  200 → CG iter ×5.2 실측이나 σ_eff −7.8% →
#                 ★수렴 정체 시에만, 그리고 σ-메트릭 보고는 uncapped 런으로 (npz meta 에 태그됨)
export MPM_S4_PRUNE_FLOAT="${MPM_S4_PRUNE_FLOAT:-1}"
export MPM_S4_EW="${MPM_S4_EW:-0}"
export MPM_S4_GPU_AMG="${MPM_S4_GPU_AMG:-1}"
export MPM_S4_CONTRAST_CAP="${MPM_S4_CONTRAST_CAP:-200}"
echo "[run_mpm] STEP4 솔버: prune=$MPM_S4_PRUNE_FLOAT ew=$MPM_S4_EW gpu_amg=$MPM_S4_GPU_AMG cap=$MPM_S4_CONTRAST_CAP"
AP=""
for d in "$KIT/anchor_params" "$KIT/../anchor_params"; do [ -f "$d/ocp_nmc811_chen2020.csv" ] && AP="$d" && break; done
if [ -z "$AP" ]; then
  echo "[run_mpm] STEP4 SKIP — OCP 앵커 없음 (anchor_params/ocp_nmc811_chen2020.csv)."
  echo "          1회 생성: python3 $SCR/step4_pybamm_anchor.py --export-params   (pybamm 필요)"
  echo "          그 뒤 재개: bash step4_only.sh"
else
  echo "[run_mpm] STEP4 스케줄[0] 충전 0.2C (CV@4.3V I<0.1C cyc1 · ★풀셀 축: R_int=${MPM_S4_RINT:-50} Ωcm² 직렬 · ★SC 단결정 단일 D_s=3e-15 m²/s (mono, σ_e AM_S=10 mS/cm)) $(date)"
  python3 "$SCR/step4_dyn.py" --grid step4_grid.npz \
    --ocp-csv "$AP/ocp_nmc811_chen2020.csv" --params-json "$AP/params_nmc811_chen2020.json" \
    --c-rate 0.2 --charge --cv-hold --v-min 3 --v-max 4.3 --x100 0.9084 --i-cut-frac 0.1 --r-int-ohm-cm2 "${MPM_S4_RINT:-50}" --d-s "${MPM_S4_DS:-3e-15}" --gpu \
    --out "step4_sched00n1_chg_c0.2_rint${MPM_S4_RINT:-50}_ds${MPM_S4_DS:-3e-15}.npz" --viz-out "step4_sched00n1_viz_chg_c0.2_rint${MPM_S4_RINT:-50}_ds${MPM_S4_DS:-3e-15}.json" \
    || echo "[run_mpm] 스케줄[0]cyc1 충전 0.2C FAILED — 다음 스텝 계속"
  echo "[run_mpm] STEP4 스케줄[1]cyc1 Rest 1min — v1 독립런: 모델 무동작(프로토콜 표시; 완화 모델은 v2 chaining)"
  echo "[run_mpm] STEP4 스케줄[2] 방전 0.2C (>=2.5V cyc1 · ★풀셀 축: R_int=${MPM_S4_RINT:-50} Ωcm² 직렬 · ★SC 단결정 단일 D_s=3e-15 m²/s (mono, σ_e AM_S=10 mS/cm)) $(date)"
  python3 "$SCR/step4_dyn.py" --grid step4_grid.npz \
    --ocp-csv "$AP/ocp_nmc811_chen2020.csv" --params-json "$AP/params_nmc811_chen2020.json" \
    --c-rate 0.2 --v-min 2.5 --v-max 4.5 --x100 0.9084 --r-int-ohm-cm2 "${MPM_S4_RINT:-50}" --d-s "${MPM_S4_DS:-3e-15}" --gpu \
    --out "step4_sched02n1_c0.2_rint${MPM_S4_RINT:-50}_ds${MPM_S4_DS:-3e-15}.npz" --viz-out "step4_sched02n1_viz_c0.2_rint${MPM_S4_RINT:-50}_ds${MPM_S4_DS:-3e-15}.json" \
    || echo "[run_mpm] 스케줄[2]cyc1 방전 0.2C FAILED — 다음 스텝 계속"
  echo "[run_mpm] STEP4 스케줄[3]cyc1 Rest 1min — v1 독립런: 모델 무동작(프로토콜 표시; 완화 모델은 v2 chaining)"
  echo "[run_mpm] STEP4 스케줄[4] 충전 2C (CV@4.3V I<1C cyc1 · ★풀셀 축: R_int=${MPM_S4_RINT:-50} Ωcm² 직렬 · ★SC 단결정 단일 D_s=3e-15 m²/s (mono, σ_e AM_S=10 mS/cm)) $(date)"
  python3 "$SCR/step4_dyn.py" --grid step4_grid.npz \
    --ocp-csv "$AP/ocp_nmc811_chen2020.csv" --params-json "$AP/params_nmc811_chen2020.json" \
    --c-rate 2 --charge --cv-hold --v-min 3 --v-max 4.3 --x100 0.9084 --i-cut-frac 1 --r-int-ohm-cm2 "${MPM_S4_RINT:-50}" --d-s "${MPM_S4_DS:-3e-15}" --gpu \
    --out "step4_sched04n1_chg_c2_rint${MPM_S4_RINT:-50}_ds${MPM_S4_DS:-3e-15}.npz" --viz-out "step4_sched04n1_viz_chg_c2_rint${MPM_S4_RINT:-50}_ds${MPM_S4_DS:-3e-15}.json" \
    || echo "[run_mpm] 스케줄[4]cyc1 충전 2C FAILED — 다음 스텝 계속"
  echo "[run_mpm] STEP4 스케줄[5]cyc1 Rest 1min — v1 독립런: 모델 무동작(프로토콜 표시; 완화 모델은 v2 chaining)"
  echo "[run_mpm] STEP4 스케줄[6] 방전 2C (>=2.5V cyc1 · ★풀셀 축: R_int=${MPM_S4_RINT:-50} Ωcm² 직렬 · ★SC 단결정 단일 D_s=3e-15 m²/s (mono, σ_e AM_S=10 mS/cm)) $(date)"
  python3 "$SCR/step4_dyn.py" --grid step4_grid.npz \
    --ocp-csv "$AP/ocp_nmc811_chen2020.csv" --params-json "$AP/params_nmc811_chen2020.json" \
    --c-rate 2 --v-min 2.5 --v-max 4.5 --x100 0.9084 --r-int-ohm-cm2 "${MPM_S4_RINT:-50}" --d-s "${MPM_S4_DS:-3e-15}" --gpu \
    --out "step4_sched06n1_c2_rint${MPM_S4_RINT:-50}_ds${MPM_S4_DS:-3e-15}.npz" --viz-out "step4_sched06n1_viz_c2_rint${MPM_S4_RINT:-50}_ds${MPM_S4_DS:-3e-15}.json" \
    || echo "[run_mpm] 스케줄[6]cyc1 방전 2C FAILED — 다음 스텝 계속"
  echo "[run_mpm] STEP4 스케줄[7]cyc1 Rest 1min — v1 독립런: 모델 무동작(프로토콜 표시; 완화 모델은 v2 chaining)"
  echo "[run_mpm] STEP4 스케줄[4] 충전 2C (CV@4.3V I<1C cyc2 · ★풀셀 축: R_int=${MPM_S4_RINT:-50} Ωcm² 직렬 · ★SC 단결정 단일 D_s=3e-15 m²/s (mono, σ_e AM_S=10 mS/cm)) $(date)"
  python3 "$SCR/step4_dyn.py" --grid step4_grid.npz \
    --ocp-csv "$AP/ocp_nmc811_chen2020.csv" --params-json "$AP/params_nmc811_chen2020.json" \
    --c-rate 2 --charge --cv-hold --v-min 3 --v-max 4.3 --x100 0.9084 --i-cut-frac 1 --r-int-ohm-cm2 "${MPM_S4_RINT:-50}" --d-s "${MPM_S4_DS:-3e-15}" --gpu \
    --out "step4_sched04n2_chg_c2_rint${MPM_S4_RINT:-50}_ds${MPM_S4_DS:-3e-15}.npz" --viz-out "step4_sched04n2_viz_chg_c2_rint${MPM_S4_RINT:-50}_ds${MPM_S4_DS:-3e-15}.json" \
    || echo "[run_mpm] 스케줄[4]cyc2 충전 2C FAILED — 다음 스텝 계속"
  echo "[run_mpm] STEP4 스케줄[5]cyc2 Rest 1min — v1 독립런: 모델 무동작(프로토콜 표시; 완화 모델은 v2 chaining)"
  echo "[run_mpm] STEP4 스케줄[6] 방전 2C (>=2.5V cyc2 · ★풀셀 축: R_int=${MPM_S4_RINT:-50} Ωcm² 직렬 · ★SC 단결정 단일 D_s=3e-15 m²/s (mono, σ_e AM_S=10 mS/cm)) $(date)"
  python3 "$SCR/step4_dyn.py" --grid step4_grid.npz \
    --ocp-csv "$AP/ocp_nmc811_chen2020.csv" --params-json "$AP/params_nmc811_chen2020.json" \
    --c-rate 2 --v-min 2.5 --v-max 4.5 --x100 0.9084 --r-int-ohm-cm2 "${MPM_S4_RINT:-50}" --d-s "${MPM_S4_DS:-3e-15}" --gpu \
    --out "step4_sched06n2_c2_rint${MPM_S4_RINT:-50}_ds${MPM_S4_DS:-3e-15}.npz" --viz-out "step4_sched06n2_viz_c2_rint${MPM_S4_RINT:-50}_ds${MPM_S4_DS:-3e-15}.json" \
    || echo "[run_mpm] 스케줄[6]cyc2 방전 2C FAILED — 다음 스텝 계속"
  echo "[run_mpm] STEP4 스케줄[7]cyc2 Rest 1min — v1 독립런: 모델 무동작(프로토콜 표시; 완화 모델은 v2 chaining)"
fi
