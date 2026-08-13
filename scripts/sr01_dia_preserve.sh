#!/usr/bin/env bash
# SR-01 게이트 ⑥ — **직경-보존 재척도** 제3 arm.
#
# 왜: 선분 래스터는 섬유를 **1 복셀 굵기 관**으로 굽는다.  VGCF 는 Ø 0.15 µm 인데 복셀이
#   0.4 µm 라 단면이 부풀고 σ_e 가 과대평가된다.  단위길이당 컨덕턴스 G/L = σ·A 를 보존하면
#       σ_eff = σ_bulk · π d²/(4 vox²) = 100 · π(0.15)²/(4·0.16) = **11.04 S/cm**
#   ⇒ 추정 밴드(선분÷5~9 = 0.0204~0.0367)를 **직접 측정**으로 대체한다.
#
# ★ 스칼라로 옳은 이유 (CL-16 자기정정): `dia = √weight` 이고 VGCF 는 vol_conserve=False 라
#   weight 가 균일 → **상대 Ø ≡ 1**.  퍼지는 것은 PTFE 인데 PTFE 는 전자망에서 절연체다.
#   ⇒ 돌리기 전에 그것을 **실제 파일로 확인**한다 (아래 dia 검사).  아니면 ABORT.
#
# ⚠ 이 보정은 **단면**만이다.  계단식 경로의 여분 길이(k = 1~√3)는 미보정이고,
#   래스터 경로가 k 배 길어 저항이 k 배 크다 ⇒ 이 런의 σ_e 는 참값의 **하한**이다.
#   (2026-08-13 부호 정정 — 처음엔 상한이라고 적었다.)  참값 ≈ 측정값 × k^w
#   (w = VGCF 소산분담).  k 는 scripts/sr01_staircase_factor.py 로 실측.
#
# 사용 (V100):
#   cd ~/Yonghoon-DEM-DFT/se_curve
#   setsid nohup bash ~/dem-sk/scripts/sr01_dia_preserve.sh kit_ps_7_3 \
#     > kit_ps_7_3/sr01_dia.log 2>&1 &
#   tail -f kit_ps_7_3/sr01_dia.log
set -uo pipefail

KIT_IN="${1:-}"
[ -n "$KIT_IN" ] || { echo "사용: bash scripts/sr01_dia_preserve.sh <KIT_DIR> [RUN_DIR]"; exit 2; }
KIT="$(cd "$KIT_IN" 2>/dev/null && pwd)" || { echo "ABORT — 킷 폴더 없음: $KIT_IN"; exit 1; }

if [ -n "${2:-}" ]; then
  RUN_IN="$2"
elif [ -e "$KIT/latest_run" ]; then
  RUN_IN="$KIT/latest_run"
else
  CAND=""; NCAND=0
  for d in "$KIT"/run_*; do
    [ -f "$d/se_dump.npy" ] || continue
    CAND="$d"; NCAND=$((NCAND + 1))
  done
  [ "$NCAND" = 1 ] || { echo "ABORT — 압밀된 런이 $NCAND 개.  두 번째 인자로 지정하세요."; exit 1; }
  RUN_IN="$CAND"
fi
RUN="$(cd "$RUN_IN" && pwd)"
SCR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -z "${VIRTUAL_ENV:-}" ] && [ -z "${MPM_NO_VENV:-}" ]; then
  for _v in "$SCR/../venv" "$SCR/../.venv" "$HOME/Yonghoon-DEM-DFT/venv"; do
    [ -f "$_v/bin/activate" ] && { . "$_v/bin/activate"; echo "[dia] venv $_v"; break; }
  done
fi

for f in se_dump.npy fibre.npy; do
  [ -f "$RUN/$f" ] || { echo "ABORT — $RUN/$f 가 없습니다 (압밀이 먼저)."; exit 1; }
done
cd "$RUN"

# ── ★ 돌리기 **전에** VGCF Ø 가 정말 균일한지 실제 파일로 확인한다 ────────────────────
#    (CL-16 이 이것을 안 재고 혼합 모집단의 산포를 읽어 틀렸다.  같은 실수를 막는다.)
SIGMA=$(python3 - <<'PY'
import sys, os, math
import numpy as np
sys.path.insert(0, os.environ.get('SCRIPTS', ''))
sys.path.insert(0, os.path.expanduser('~/dem-sk/scripts'))
import step3_sigma as s3                                    # noqa: E402
VOX = float(os.environ.get('STEP3_VOX', '0.4'))
D_REF = 0.15                                                # additives.VGCF_D (Showa Denko VGCF-H)
if not (os.path.exists('fibre_dia.npy') and os.path.exists('phase.npy')):
    sys.stderr.write('ABORT — fibre_dia.npy / phase.npy 가 없다.  '
                     'mpm3d 를 --save-fibre-dia --save-phase 로 돌려야 한다.\n')
    raise SystemExit(1)
dia = np.load('fibre_dia.npy'); ph = np.load('phase.npy')
if len(dia) != len(ph):
    sys.stderr.write(f'ABORT — fibre_dia {len(dia)} != phase {len(ph)}\n'); raise SystemExit(1)
st = s3.dia_stats_by_phase(dia, ph)
for k, v in sorted(st.items()):
    sys.stderr.write(f'  [dia] phase {k}: {v}\n')
v = st.get(2)                                               # 2 = VGCF
if v is None:
    sys.stderr.write('ABORT — phase 2 (VGCF) 점이 없다.\n'); raise SystemExit(1)
if not v['uniform']:
    sys.stderr.write(f'ABORT — VGCF Ø 가 균일하지 않다 (cv {v["cv"]}, {v["min"]}~{v["max"]}).\n'
                     '        스칼라 재척도의 전제가 깨졌다 — 복셀별 σ 장(sigma_field)이 필요하다.\n'
                     '        이 런을 돌리면 평균 규약이 답을 정하게 된다 (CL-16).\n')
    raise SystemExit(1)
se, prov = s3.diameter_preserving_sigma(100.0, dia[ph == 2], D_REF, VOX, mode='harmonic')
sys.stderr.write(f'  [dia] VGCF 균일 확인 (Ø rel {v["min"]}~{v["max"]}, n={v["n"]:,})\n')
sys.stderr.write(f'  [dia] 재척도 σ_VGCF 100 → {se:.6g} S/cm  (factor {prov["factor"]})\n')
print(f'{se:.6g}')
PY
) || exit 1
[ -n "$SIGMA" ] || { echo "ABORT — 재척도 σ 를 못 구했다."; exit 1; }
echo "[dia] σ_VGCF = $SIGMA S/cm (직경-보존, 단면만 — 계단식 여분길이 미보정 ⇒ **하한**)"

OUT="mpm_payload_diapreserve.json"
if [ -s "$OUT" ]; then
  echo "[dia] 이미 있습니다: $OUT — 보존하고 종료 (지우고 다시 돌리세요)."; exit 0
fi

python3 "$SCR/sr01_stamp_compare.py" --extract-payload "$KIT/run_mpm.sh" \
        --stamp segment --extra-flags "--sigma-vgcf $SIGMA" \
        --tag diapreserve --out-name "$OUT" > _payload_dia.sh || exit 1
{ echo 'set -uo pipefail'; echo "KIT=\"$KIT\""; echo "SCR=\"$SCR\"";
  echo "PSIG=(${MPM_PERIODIC_SIGMA:+--periodic})"; cat _payload_dia.sh; } > payload_dia.sh
rm -f _payload_dia.sh

grep -q -- "--sigma-vgcf $SIGMA" payload_dia.sh || {
  echo "ABORT — --sigma-vgcf 주입 실패."; exit 1; }
grep -q -- '--step3-fibre-stamp segment' payload_dia.sh || {
  echo "ABORT — 선분 스탬프가 안 박혔다."; exit 1; }
echo "[dia] 주입 확인 OK — --sigma-vgcf $SIGMA · stamp segment · --out $OUT"

bash payload_dia.sh || { echo "[dia] FAILED — 위 트레이스"; exit 1; }

python3 - "$OUT" mpm_payload_segstamp.json mpm_payload_pointstamp.json mpm_payload_amonly.json <<'PY'
import json, os, sys


def sig(path):
    if not os.path.exists(path):
        return None
    d = json.load(open(path))
    s = d.get('step3') or (d.get('mpm_metrics') or {}).get('step3') or {}
    return s.get('sigma_e_eff_S_cm'), (s.get('manifest') or {}).get('fibre_stamp')


cur, sg, pt, fl = (sig(p) for p in sys.argv[1:5])
print()
print('── 게이트 ⑥ 직경-보존 ───────────────────────────────────')
print(f'  σ_e(직경보존)  = {cur[0]}   (stamp {cur[1]})')
for nm, v in (('선분(보정 전)', sg), ('점', pt), ('AM-only 바닥', fl)):
    if v:
        print(f'  σ_e({nm})  = {v[0]}   (stamp {v[1]})')
if sg and cur:
    print(f'\n  선분 → 직경보존 = ÷{sg[0] / cur[0]:.3g}  '
          f'(예상 ≈ ÷9.1 = 1/factor; 어긋나면 선형 가정이 깨진 것)')
if fl and cur:
    print(f'  직경보존 / 바닥 = ×{cur[0] / fl[0]:.4g}')
if pt and cur:
    print(f'  직경보존 / 점   = ×{cur[0] / pt[0]:.4g}   ← 점→참값 배수의 **하한** (계단 보정 전)')
print('\n  ⚠ 단면만 보정했다.  계단식 경로가 k 배 길어 저항이 k 배 크다 ⇒ 이 값은 **하한**이다.')
print('     참값 ≈ 측정값 × k^w  (k = 계단 인자 실측, w = VGCF 소산분담).')
PY
