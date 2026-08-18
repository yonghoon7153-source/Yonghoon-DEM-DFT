#!/usr/bin/env bash
# ★★ 2026-08-18 — 심층 리뷰 2건(DR3-01~08) 뒤의 **실행 계약 순서**.  1 → 2 → 3 → 4.
#
#   왜 이 순서인가 (docs/reviews/sdcp_next_prereg_v3_20260818.md 가 정본):
#     1  CPU 수 분 · 솔브 없음 — SDCP 표현부피가 vox 0.125/0.10 에서도 ~1.0 이면
#        "기전 변수는 이미 수렴" 이 GPU 없이 서고 **4 가 불필요해질 수도 있다**
#     2  GPU ~3 h — σ_VGCF 만 이동(78.5398 → 113.097).  4 의 해석 전제다:
#        직경-보존 재척도가 vox 의 함수라 격자 스윕은 σ 스윕과 섞여 있다 (DR3-05)
#     3  GPU ~3 h — σ_VGCF = 0.  "SDCP 이득이 VGCF 채널을 통하는가" 정면 답 (항목 ② 대체)
#     4  GPU 20 h+ — 격자 스윕 vox {0.125, 0.10} × 8팔 × 2침대
#
#   ⚠ 2·3 은 **arm 0 (origin 0,0,0) 만** 돈다.  기존 8팔 sph 런의 arm 0
#     (SBE 0.07302 / DBE 0.08224, 비 1.1263) 과 **쌍대응**으로 비교하기 위해서다.
#     STEP 2a 가 그 기준점을 새 코드로 다시 찍어 **수치 불변**을 먼저 확인한다.
#
# 사용 (원격, ~/sdcp 에서):
#   . ~/dem-venv/bin/activate
#   cd ~/sdcp && git -C ~/dem-sk pull
#   setsid nohup bash ~/dem-sk/scripts/sdcp_next_1234.sh > next.log 2>&1 &
#   tail -f next.log
#
# 개별 실행:  STEPS="1" bash …   ·   STEPS="2 3" bash …   ·   STEPS="4" bash …
set -uo pipefail

SCR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STEPS="${STEPS:-1 2 3 4}"
SPH="${SPH:-0.30}"                       # SDCP 구 스탬프 직경 (게이트: d/vox ≥ 2)
SIG_BASE="${SIG_BASE:-78.5398}"          # vox 0.15 직경-보존 값 (기존 8팔 런과 동일)
SIG_125="${SIG_125:-113.097}"            # vox 0.125 의 직경-보존 값 (σ 축만 이동시킬 때)
SWEEP_VOX="${SWEEP_VOX:-0.125 0.1}"

if [ -z "${VIRTUAL_ENV:-}" ]; then
  for _v in "$HOME/dem-venv" "$SCR/../venv"; do
    [ -f "$_v/bin/activate" ] && { . "$_v/bin/activate"; break; }
  done
fi
for K in kit_SBE kit_DBE; do
  [ -d "$K" ] || { echo "ABORT — $K 없음 (~/sdcp 에서 돌릴 것)"; exit 2; }
done
grep -q 'SIGMA_VGCF_OVERRIDE' "$SCR/sdcp_gain_vox015_8arm.sh" \
  || { echo "ABORT — 러너가 옛 판이다 (git -C ~/dem-sk pull 했나?)"; exit 2; }

_has() { case " $STEPS " in *" $1 "*) return 0;; *) return 1;; esac; }
_hdr() { echo; echo "══════════════════════════════════════════════════════════════"; \
         echo "  $*"; echo "══════════════════════════════════════════════════════════════"; }
_ram() { free -g 2>/dev/null | awk '/^Mem:/{print $2" GB total, "$7" GB available"}'; }

echo "[next] 호스트 RAM: $(_ram)"
echo "[next] STEPS = $STEPS"

# ════════════════════════════════════════════════════════════════════════════
# STEP 1 — CPU 상별 부피 원장 (솔브 없음).  4 를 돌릴 가치가 있는지부터 판정한다.
# ════════════════════════════════════════════════════════════════════════════
if _has 1; then
  _hdr "STEP 1 — 상별 부피 원장 (CPU, 솔브 없음) · vox $SWEEP_VOX"
  echo "  묻는 것: SDCP 표현부피/참부피 가 vox 0.15 의 0.986 에서 유지되는가."
  echo "  유지되면 → 기전 변수는 수렴.  4 의 R 이동은 전부 σ_VGCF·VGCF 기하 교란(DR3-05/06)."
  echo "  안 유지되면 → 4 가 필요하다."
  VOXES="$SWEEP_VOX" OUTDIR="$PWD/phase_ledger" bash "$SCR/sdcp_phase_ledger.sh" \
    || { echo "[next] STEP 1 실패 — 멈춘다"; exit 1; }
  echo
  echo "[next] ★ dof 실측 (4 의 메모리 예산 = 추정이 아니라 이 숫자로)"
  python3 - <<'PY'
import glob, json, os
for p in sorted(glob.glob('phase_ledger/ledger_*.json')):
    r = json.load(open(p, encoding='utf-8'))
    c = {int(k): v for k, v in r['cells_by_sid'].items()}
    tot = sum(c.values())
    cond = sum(v for k, v in c.items() if k in (1, 2, 3, 4, 5))     # AM·VGCF·SuperP·SDCP
    print(f"  {os.path.basename(p)[7:-5]:28s} vox {r['vox_um']:<6} 격자 {str(r['grid_shape']):20s} "
          f"총 {tot:>12,} · 전도 {cond:>12,}  → VRAM ≈ {cond*140/2**30:5.1f} GB · "
          f"호스트 ≈ {cond*415/2**30:5.1f} GB")
PY
fi

# ════════════════════════════════════════════════════════════════════════════
# 공통 러너 — arm 0 만 (ARMS=1), 구 스탬프, LEAN
# ════════════════════════════════════════════════════════════════════════════
_arm0() {   # $1=σ_VGCF override("" 면 직경-보존)  $2=라벨
  local SG="$1" LBL="$2"
  echo "[next] ── $LBL"
  if [ -n "$SG" ]; then
    VOX=0.15 SDCP_SPHERE_D="$SPH" ARMS=1 LEAN=1 SIGMA_VGCF_OVERRIDE="$SG" \
      bash "$SCR/sdcp_gain_vox015_8arm.sh"
  else
    VOX=0.15 SDCP_SPHERE_D="$SPH" ARMS=1 LEAN=1 \
      bash "$SCR/sdcp_gain_vox015_8arm.sh"
  fi
}

if _has 2; then
  _hdr "STEP 2 — σ_VGCF 축만 이동 (GPU, arm 0 만)"
  echo "  2a 기준점 재현: σ_VGCF = $SIG_BASE (기존 8팔 런과 같은 값, **새 코드**로)"
  echo "     기대: SBE 0.07302 · DBE 0.08224 · 비 1.1263 재현 = 이번 수정이 수치에 무영향"
  _arm0 "" "2a 기준점 (직경-보존 $SIG_BASE)" || { echo "[next] STEP 2a 실패"; exit 1; }
  echo
  echo "  2b σ 만 이동: σ_VGCF = $SIG_125 (= vox 0.125 의 직경-보존 값, 격자는 0.15 그대로)"
  _arm0 "$SIG_125" "2b σ 이동 ($SIG_125)" || { echo "[next] STEP 2b 실패"; exit 1; }
fi

if _has 3; then
  _hdr "STEP 3 — VGCF 를 전기적으로 죽인다 (GPU, arm 0 만)"
  echo "  σ_VGCF = 0 — 셀은 남아 부피를 막고 도체만 아니게 된다 (_cond_ph 가 phase 2 를 항상 스탬프)."
  echo "  묻는 것: SDCP 이득이 **VGCF 채널을 통하는가**.  항목 ②(RVE VGCF 팔)를 대체한다."
  echo "  ⚠ SBE 가 AM 골격만으로 퍼콜하는지도 함께 나온다 (옛 base 값 ~5.7e-4 S/cm)."
  _arm0 "0" "3 VGCF-off (σ_VGCF = 0)" || { echo "[next] STEP 3 실패"; exit 1; }
fi

if _has 2 || _has 3; then
  _hdr "2·3 대조 (arm 0 쌍대응)"
  python3 - <<'PY'
import glob, json, os
rows = []
for d in sorted(glob.glob('prereg_v2_vox015_sph*')):
    for p in sorted(glob.glob(os.path.join(d, 'p2_*_a0.json'))):
        j = json.load(open(p, encoding='utf-8'))
        s = j.get('step3') or (j.get('mpm_metrics') or {}).get('step3') or {}
        m = s.get('manifest') or {}
        rows.append((d, os.path.basename(p), m.get('sigma_vgcf_S_cm'),
                     s.get('sigma_e_eff_S_cm'), s.get('sigma_ion_eff_S_cm'),
                     s.get('cg_info'), (m.get('backend_last_solve') or {}).get('backend')))
by = {}
for d, f, sg, se, si, cg, bk in rows:
    key = (d, sg)
    by.setdefault(key, {})['SBE' if '_SBE_' in f else 'DBE'] = (se, si, cg, bk)
print(f"{'디렉터리':44s} {'σ_VGCF':>10} {'σ_e SBE':>11} {'σ_e DBE':>11} {'비':>9} {'σ_ion 비':>9}")
for (d, sg), v in sorted(by.items(), key=lambda x: (x[0][1] is None, x[0][1] or 0)):
    if 'SBE' not in v or 'DBE' not in v:
        print(f'{d:44s} {str(sg):>10}  (한쪽 팔만)'); continue
    (se_s, si_s, cg_s, _), (se_d, si_d, cg_d, _) = v['SBE'], v['DBE']
    bad = '  ⚠미수렴' if (cg_s or cg_d) else ''
    r = se_d / se_s if se_s else float('nan')
    ri = si_d / si_s if si_s else float('nan')
    print(f'{d:44s} {str(sg):>10} {se_s:>11.6g} {se_d:>11.6g} {r:>9.4f} {ri:>9.4f}{bad}')
print('\n★ 읽는 법')
print('  2a 가 1.1263 (기존 arm 0) 을 재현하면 → 이번 코드 수정은 수치에 무영향.')
print('  2b−2a 의 비 변화 = **σ_VGCF 만으로 생긴 변화** ⇒ 4 의 격자 이동에서 이만큼을 빼야 한다.')
print('  3 의 비 = VGCF 가 도체가 아닐 때의 SDCP 이득.')
print('     · 3 의 이득이 크게 남으면 → SDCP 는 VGCF 와 **무관한** 경로로 기여 (AM↔AM 등)')
print('     · 3 의 이득이 사라지면   → SDCP 의 역할은 **VGCF 사이를 잇는 것** = 통제 RVE 에')
print('       VGCF 가 없던 것이 CL-31 격차의 원인 (항목 ② 가 답을 얻는다)')
PY
fi

# ════════════════════════════════════════════════════════════════════════════
# STEP 4 — 격자 스윕 (비싸다)
# ════════════════════════════════════════════════════════════════════════════
if _has 4; then
  _hdr "STEP 4 — 구 스탬프 격자 스윕 vox $SWEEP_VOX × 8팔 × 2침대 (GPU, 20 h+)"
  echo "  ⚠ 라벨: 이것은 **격자 규약 민감도**이지 격자 수렴 증명이 아니다 (DR3-05/06)."
  echo "  ⚠ vox ≤ 0.125 팔의 σ_ion·τ_pore·BV 반응면·STEP4 격자는 **인용 금지** — SE 점"
  echo "     스탬프가 미충전이다 (λ 3.0 → 1.72 → 0.88, DR3-07).  σ_e 는 무해."
  for V in $SWEEP_VOX; do
    AVAIL=$(free -g 2>/dev/null | awk '/^Mem:/{print $7}')
    echo
    echo "[next] ── vox $V  (가용 RAM ${AVAIL:-?} GB)"
    if [ -n "${AVAIL:-}" ] && [ "$AVAIL" -lt 24 ] && [ "$V" = "0.1" ]; then
      echo "[next] ⚠ vox 0.1 은 호스트 RAM ~40 GB 를 쓴다 (COO int64 조립).  가용 $AVAIL GB."
      echo "        STEP 1 의 dof 실측으로 다시 판단할 것 — 여기서는 멈춘다."
      exit 1
    fi
    VOX="$V" SDCP_SPHERE_D="$SPH" ARMS=8 LEAN=1 bash "$SCR/sdcp_gain_vox015_8arm.sh" \
      || { echo "[next] STEP 4 (vox $V) 실패 — 멈춘다 (끝난 팔은 남아 SKIP 된다)"; exit 1; }
  done
  _hdr "STEP 4 수집"
  for V in $SWEEP_VOX; do
    D="prereg_v2_vox${V/./}_sph_b048_lean"
    [ -d "$D" ] && { echo "── $D"; python3 "$SCR/sdcp_gain_verdict.py" --dir "$D" --collect-only; }
  done
fi

_hdr "끝.  결과를 붙여줄 것 — 판정은 사람이 본 뒤에."
