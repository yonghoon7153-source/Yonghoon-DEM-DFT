#!/usr/bin/env bash
# SR-01 게이트 ⑤ — {점, 직경-보존 선분} × {SBE, DBE} 2×2.
#
# 질문: SDCP 의 +51 % 이득이 **래스터가 만든 것**인가?
#   원고 기전 = SDCP 가 VGCF 접합부의 좁은 목을 잇는다.
#   그런데 **점 스탬프 자체가 VGCF 를 조각낸다** (실침대 68.5~86.4 % 가 2.6~3.4 조각).
#   ⇒ SDCP 가 잇는 것이 물리적 목인가, 래스터가 만든 가짜 단절인가?
#   섬유를 제대로 이어 놓고(직경-보존 선분) 다시 재면 갈린다.
#
# 사전등록: docs/reviews/sr01_gate5_prereg_20260813.md  (h0 ratio_seg=1.51 · h1 =1.15 · 분해능 0.03)
#
# ★ 네 팔을 **같은 세션·같은 코드**로 돈다 — 기존 점 팔(2026-08-12)을 재활용하지 않는다.
#   교호작용은 **비의 차**라 절대값 드리프트가 그 안에 남기 때문이다 (CL-10 이 드리프트
#   +3.5~4.1 % 를 실측했다).
#
# 사용 (V100):
#   cd ~/sdcp
#   setsid nohup bash ~/dem-sk/scripts/sr01_gate5_2x2.sh kit_SBE kit_DBE \
#     > gate5.log 2>&1 &
#   tail -f gate5.log
set -uo pipefail

KIT_SBE_IN="${1:-}"; KIT_DBE_IN="${2:-}"
[ -n "$KIT_SBE_IN" ] && [ -n "$KIT_DBE_IN" ] || {
  echo "사용: bash scripts/sr01_gate5_2x2.sh <KIT_SBE> <KIT_DBE>"; exit 2; }
SCR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -z "${VIRTUAL_ENV:-}" ] && [ -z "${MPM_NO_VENV:-}" ]; then
  for _v in "$SCR/../venv" "$SCR/../.venv" "$HOME/Yonghoon-DEM-DFT/venv"; do
    [ -f "$_v/bin/activate" ] && { . "$_v/bin/activate"; echo "[g5] venv $_v"; break; }
  done
fi

resolve_run() {                                   # $1 = kit dir → 절대 런 경로
  local kit; kit="$(cd "$1" && pwd)"
  if [ -e "$kit/latest_run" ]; then (cd "$kit/latest_run" && pwd); return; fi
  local cand="" n=0
  for d in "$kit"/run_*; do [ -f "$d/se_dump.npy" ] || continue; cand="$d"; n=$((n+1)); done
  [ "$n" = 1 ] || { echo "ABORT — $kit 에 압밀된 런이 $n 개" >&2; return 1; }
  (cd "$cand" && pwd)
}

KIT_SBE="$(cd "$KIT_SBE_IN" && pwd)"; KIT_DBE="$(cd "$KIT_DBE_IN" && pwd)"
RUN_SBE="$(resolve_run "$KIT_SBE")" || exit 1
RUN_DBE="$(resolve_run "$KIT_DBE")" || exit 1
echo "[g5] SBE run: $RUN_SBE"
echo "[g5] DBE run: $RUN_DBE"

# ── VGCF Ø 균일성을 **두 침대 모두** 실측 확인.  아니면 ABORT (스칼라 전제, CL-16) ────
dia_sigma() {                                     # $1 = run dir → σ_VGCF (재척도)
  ( cd "$1" && python3 - <<'PY'
import os, sys
import numpy as np
sys.path.insert(0, os.path.expanduser('~/dem-sk/scripts'))
import step3_sigma as s3                                        # noqa: E402
VOX, D_REF = float(os.environ.get('STEP3_VOX', '0.4')), 0.15
for f in ('fibre_dia.npy', 'phase.npy'):
    if not os.path.exists(f):
        sys.stderr.write(f'ABORT — {os.getcwd()}/{f} 없음 (--save-fibre-dia --save-phase 필요)\n')
        raise SystemExit(1)
dia, ph = np.load('fibre_dia.npy'), np.load('phase.npy')
if len(dia) != len(ph):
    sys.stderr.write(f'ABORT — fibre_dia {len(dia)} != phase {len(ph)}\n'); raise SystemExit(1)
st = s3.dia_stats_by_phase(dia, ph)
sys.stderr.write(f'  [g5]   {os.path.basename(os.getcwd())}: ' +
                 ' · '.join(f'ph{k}={v["min"]}~{v["max"]}(cv {v["cv"]})'
                            for k, v in sorted(st.items()) if v) + '\n')
v = st.get(2)
if v is None:
    sys.stderr.write('ABORT — phase 2 (VGCF) 점이 없다\n'); raise SystemExit(1)
if not v['uniform']:
    sys.stderr.write(f'ABORT — VGCF Ø 비균일 (cv {v["cv"]}) → 스칼라 전제 붕괴 (CL-16).\n'
                     '        복셀별 σ 장이 필요하다.  이 런은 평균 규약이 답을 정하게 된다.\n')
    raise SystemExit(1)
print(f'{s3.diameter_preserving_sigma(100.0, dia[ph == 2], D_REF, VOX)[0]:.6g}')
PY
  )
}
SIG_SBE="$(dia_sigma "$RUN_SBE")" || exit 1
SIG_DBE="$(dia_sigma "$RUN_DBE")" || exit 1
echo "[g5] 재척도 σ_VGCF — SBE $SIG_SBE · DBE $SIG_DBE S/cm"
[ "$SIG_SBE" = "$SIG_DBE" ] || echo "[g5] ⚠ 두 침대의 재척도 σ 가 다르다 — Ø 분포가 다르다는 뜻이니 §5 무효조건 확인"

run_arm() {                                       # $1 run  $2 kit  $3 stamp  $4 extra  $5 out  $6 tag
  local run="$1" kit="$2" stamp="$3" extra="$4" out="$5" tag="$6"
  cd "$run"
  if [ -s "$out" ]; then
    if python3 "$SCR/sr01_stamp_compare.py" --check-arm "$out" --stamp "$stamp" >/dev/null 2>&1; then
      echo "[g5] SKIP (완전) $(basename "$run")/$out"; return 0
    fi
    mv -f "$out" "${out%.json}.superseded.json"
    echo "[g5] 불완전 → 다시 돈다: $out"
  fi
  python3 "$SCR/sr01_stamp_compare.py" --extract-payload "$kit/run_mpm.sh" \
          --stamp "$stamp" --extra-flags "$extra" --tag "$tag" --out-name "$out" \
          > "_g5_$tag.sh" || return 1
  { echo 'set -uo pipefail'; echo "KIT=\"$kit\""; echo "SCR=\"$SCR\"";
    echo "PSIG=(${MPM_PERIODIC_SIGMA:+--periodic})"; cat "_g5_$tag.sh"; } > "g5_$tag.sh"
  rm -f "_g5_$tag.sh"
  grep -q -- "--step3-fibre-stamp $stamp" "g5_$tag.sh" || { echo "ABORT — 스탬프 미주입"; return 1; }
  [ -z "$extra" ] || grep -q -- "$extra" "g5_$tag.sh" || { echo "ABORT — extra 미주입"; return 1; }
  echo "[g5] ── $(basename "$run")  stamp=$stamp  extra='${extra:-（없음）}'  → $out"
  bash "g5_$tag.sh" || { echo "[g5] FAILED"; return 1; }
}

run_arm "$RUN_SBE" "$KIT_SBE" point   ""                        mpm_payload_g5_sbe_pt.json  g5sbept  || exit 1
run_arm "$RUN_DBE" "$KIT_DBE" point   ""                        mpm_payload_g5_dbe_pt.json  g5dbept  || exit 1
run_arm "$RUN_SBE" "$KIT_SBE" segment "--sigma-vgcf $SIG_SBE"   mpm_payload_g5_sbe_sg.json  g5sbesg  || exit 1
run_arm "$RUN_DBE" "$KIT_DBE" segment "--sigma-vgcf $SIG_DBE"   mpm_payload_g5_dbe_sg.json  g5dbesg  || exit 1

python3 - "$RUN_SBE" "$RUN_DBE" <<'PY'
import json, math, os, sys

RS, RD = sys.argv[1], sys.argv[2]


def read(run, name):
    p = os.path.join(run, name)
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    s = d.get('step3') or (d.get('mpm_metrics') or {}).get('step3') or {}
    mf = s.get('manifest') or {}
    return {'sig': s.get('sigma_e_eff_S_cm'), 'ion': s.get('sigma_ion_eff_S_cm'),
            'stamp': mf.get('fibre_stamp'), 'req': mf.get('fibre_stamp_requested'),
            'dof': s.get('n_dof')}


arms = {'SBE·점': read(RS, 'mpm_payload_g5_sbe_pt.json'),
        'DBE·점': read(RD, 'mpm_payload_g5_dbe_pt.json'),
        'SBE·선분': read(RS, 'mpm_payload_g5_sbe_sg.json'),
        'DBE·선분': read(RD, 'mpm_payload_g5_dbe_sg.json')}
print()
print('── 게이트 ⑤ 2×2 ────────────────────────────────────────')
bad = []
for k, v in arms.items():
    if v is None:
        print(f'  {k:10s}  (없음)'); bad.append(k); continue
    want = 'segment' if '선분' in k else 'point'
    flag = '' if v['stamp'] == want else f'  ⚠ 도장 {v["stamp"]} ≠ {want}'
    if v['req'] is not None and v['req'] != v['stamp']:
        flag += f'  ⚠⚠ 요청 {v["req"]} ≠ 적용 {v["stamp"]} = 강등 런'
        bad.append(k)
    print(f'  {k:10s}  σ_e {v["sig"]:<12} σ_ion {v["ion"]:<12} dof {v["dof"]}{flag}')
if bad:
    print(f'\n  ⚠⚠ 사용 불가 팔: {bad} — §5 무효조건.  교호작용 계산 안 함.')
    raise SystemExit(1)

r_pt = arms['DBE·점']['sig'] / arms['SBE·점']['sig']
r_sg = arms['DBE·선분']['sig'] / arms['SBE·선분']['sig']
I = math.log(r_sg) - math.log(r_pt)
print()
print(f'  ratio_pt  = {r_pt:.4f}  (+{(r_pt - 1) * 100:.2f} %)   ← 현행 생산 규약')
print(f'  ratio_seg = {r_sg:.4f}  (+{(r_sg - 1) * 100:.2f} %)   ← 직경-보존 선분')
print(f'  I = ln(ratio_seg) − ln(ratio_pt) = {I:+.4f}')
if r_pt > 1:
    print(f'  f_artifact = 1 − ln(r_seg)/ln(r_pt) = {1 - math.log(r_sg) / math.log(r_pt):+.3f}'
          '   (이득 중 래스터가 만든 몫)')
print()
print('  사전등록 (docs/reviews/sr01_gate5_prereg_20260813.md, 분해능 0.03):')
print(f'    h0 물리 기전   ratio_seg = 1.51   |Δ| = {abs(r_sg - 1.51):.4f}')
print(f'    h1 래스터 인공물 ratio_seg = 1.15   |Δ| = {abs(r_sg - 1.15):.4f}')
if I > 0.03:
    print('    ⇒ **둘 다 기각** — 선분에서 SDCP 가 더 효과적이다.  새 기전이 필요하다 (창 이동 금지).')
elif abs(r_sg - 1.51) < abs(r_sg - 1.15):
    print('    ⇒ h0 쪽 (물리 기전 생존)')
else:
    print('    ⇒ h1 쪽 (래스터 인공물)')
print()
print('  이온 축 (CL-18 대조): σ_ion 은 규약에 8 % 안이어야 한다')
for a, b in (('SBE·점', 'SBE·선분'), ('DBE·점', 'DBE·선분')):
    x, y = arms[a]['ion'], arms[b]['ion']
    if x and y:
        print(f'    {a.split("·")[0]}: {x} → {y} = {(y / x - 1) * 100:+.2f} %')
PY
