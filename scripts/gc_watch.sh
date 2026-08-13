#!/usr/bin/env bash
# 격자 수렴 런 3종 감시 — 진행·충돌·결과를 한 화면에.
#
# ⚠ 왜 충돌을 먼저 보나: `setsid ... &` 는 즉시 분리되므로 `wait` 이 바로 반환한다.
#   위 셸에서 세 줄을 연달아 치면 **세 런이 동시에 GPU 를 잡는다** (전에 "one GPU = one run"
#   에 걸렸다).  동시 실행이면 OOM 이나 상호 지연이 나고 결과가 오염된다.
#
# 사용:  watch -n 20 'bash ~/dem-sk/scripts/gc_watch.sh'
#   또는 한 번만:  bash ~/dem-sk/scripts/gc_watch.sh
set -uo pipefail
cd "${SDCP_DIR:-$HOME/sdcp}" 2>/dev/null || { echo "ABORT — ~/sdcp 없음"; exit 1; }

echo "══ 프로세스 ═══════════════════════════════════════════════"
N=$(pgrep -f mpm_webapp_payload 2>/dev/null | wc -l | tr -d " ")
[ -n "$N" ] || N=0
if [ "$N" -gt 1 ]; then
  echo "  ⚠⚠ payload 프로세스 $N 개 — **동시 실행 중이다**.  GPU 를 나눠 쓰면"
  echo "     느려지거나 OOM 이고, 어느 런이 실패했는지 로그가 섞인다."
  echo "     ⇒ 하나만 남기고 죽이려면:  pgrep -f mpm_webapp_payload   후 kill <PID>"
  pgrep -af mpm_webapp_payload | sed 's/^/     /' | cut -c1-150
elif [ "$N" = 1 ]; then
  pgrep -af mpm_webapp_payload | sed 's/^/  실행중  /' | cut -c1-140
else
  echo "  실행중인 payload 없음"
fi
command -v nvidia-smi >/dev/null && nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu \
  --format=csv,noheader | sed 's/^/  GPU  /'

echo
echo "══ 로그 (마지막 줄) ═══════════════════════════════════════"
for f in gc_dbe.log gc_025.log gc_bridge.log; do
  [ -f "$f" ] || { printf '  %-14s (없음)\n' "$f"; continue; }
  last=$(grep -v '^\s*$' "$f" | tail -1 | cut -c1-118)
  age=$(( $(date +%s) - $(stat -c %Y "$f") ))
  printf '  %-14s [%4ds 전] %s\n' "$f" "$age" "$last"
  grep -E 'ABORT|FAILED|OOM|Traceback|out of memory' "$f" | tail -2 | sed 's/^/                  ⚠ /' | cut -c1-140
done

echo
echo "══ 산출물 ═════════════════════════════════════════════════"
python3 - <<'PY'
import glob, json, os
rows = []
for f in sorted(glob.glob('kit_*/**/mpm_payload_gc*.json', recursive=True)):
    try:
        d = json.load(open(f))
        s = d.get('step3') or (d.get('mpm_metrics') or {}).get('step3') or {}
        kit = f.split('/')[0]
        rows.append((kit, os.path.basename(f), s.get('sigma_e_eff_S_cm'),
                     s.get('sigma_ion_eff_S_cm'), s.get('n_dof')))
    except Exception as e:
        rows.append((f.split('/')[0], os.path.basename(f), f'X {type(e).__name__}', '', ''))
if not rows:
    print('  아직 없음')
for kit, b, se, si, nd in rows:
    print(f'  {kit:9s} {b:26s} σ_e {str(se):<11} σ_ion {str(si):<11} dof {nd}')

# ★ 비가 격자에 강건한가 — 이게 논문이 걸린 지점
def sig(kit, tag):
    g = glob.glob(f'{kit}/**/mpm_payload_{tag}.json', recursive=True)
    if not g:
        return None
    d = json.load(open(g[0]))
    s = d.get('step3') or (d.get('mpm_metrics') or {}).get('step3') or {}
    return s.get('sigma_e_eff_S_cm')

import math
print()
print('══ ★ 비가 격자에 강건한가 (논문이 걸린 지점) ═══════════════')
for tag, lab in (('gc04', 'vox 0.4'), ('gc03', 'vox 0.3'), ('gc025', 'vox 0.25')):
    a, b = sig('kit_SBE', tag), sig('kit_DBE', tag)
    if a and b:
        print(f'  {lab:9s} SBE {a:<9.4g} DBE {b:<9.4g} → 비 {b/a:.4f} (+{(b/a-1)*100:.2f} %)')
    else:
        miss = [n for n, v in (('SBE', a), ('DBE', b)) if not v]
        print(f'  {lab:9s} 미완 ({", ".join(miss)} 없음)')
r4 = [sig('kit_SBE', 'gc04'), sig('kit_DBE', 'gc04')]
r3 = [sig('kit_SBE', 'gc03'), sig('kit_DBE', 'gc03')]
if all(r4) and all(r3):
    a, b = r4[1] / r4[0], r3[1] / r3[0]
    print()
    print(f'  ratio 0.4 → 0.3 : {a:.4f} → {b:.4f}  = {(b/a-1)*100:+.2f} %'
          f'   I = {math.log(b)-math.log(a):+.4f}')
    print('  ⇒ |Δ| < 3 % 면 **비는 격자에 강건** = 헤드라인 생존.')
    print('     ★ 2026-08-13 실측: Δ = −18.25 % (판정선의 6.1배) ⇒ **강건하지 않다** (CL-22).')
PY
