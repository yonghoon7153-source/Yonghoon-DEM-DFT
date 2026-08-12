#!/usr/bin/env bash
# SR-01 #9 — **AM-only 바닥** 1런.  같은 압밀 베드에서 탄소를 전기적으로 꺼서
# "탄소가 아무것도 안 했다면 σ_e 가 얼마인가" 를 잰다 = 진짜 하한.
#
# 왜 필요한가 (docs/reviews/sr01_raster_review_verdict_20260812.md §6):
#   점 스탬프는 참값의 하한이 **아니다** — 살아남은 조각의 단면이 ~6배 부풀어 있다.
#     σ_e(AM-only) ≤ σ_e(참) ≤ σ_e(선분)/~6
#     σ_e(점) ≤ σ_e(선분)                   ← Rayleigh 단조성으로 증명됨
#     σ_e(점) vs σ_e(참)                     ← **순서 미정**
#   왼쪽 끝(AM-only)이 리포에 없어서 ×35.79 를 브래킷할 수 없다.  이 런이 그것을 채운다.
#
# 방법: `--sigma-vgcf 1e-9` — 탄소 복셀을 **그래프에 남긴 채** 전기적으로만 끈다.
#   σ=0 으로 두면 전도 마스크에서 빠져 dof·플레이트 접촉·성분 구조가 함께 바뀌어
#   "재료 기여" 와 "그래프 변화" 가 섞인다.  1e-9 는 조화평균 컨덕턴스를 ~2e-9 로
#   눌러 사실상 절연이면서 **격자·dof 를 그대로 둔다** = 교란변수 최소.
#   ⇒ 결과 σ_e 는 AM-AM 접촉망만으로 나온 값이다.
#
# 스탬프는 **선분**(생산 규약)으로 고정한다 — 바닥은 헤드라인과 같은 래스터에서 재야
# 같은 축의 하한이 된다.
#
# 사용 (V100):
#   cd ~/Yonghoon-DEM-DFT/se_curve
#   setsid nohup bash ~/dem-sk/scripts/sr01_floor_amonly.sh kit_ps_7_3 \
#     > kit_ps_7_3/sr01_floor.log 2>&1 &
#   tail -f kit_ps_7_3/sr01_floor.log
set -uo pipefail

KIT_IN="${1:-}"
[ -n "$KIT_IN" ] || { echo "사용: bash scripts/sr01_floor_amonly.sh <KIT_DIR> [RUN_DIR]"; exit 2; }
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
[ -e "$RUN_IN" ] || { echo "ABORT — 런 폴더가 없습니다: $RUN_IN"; exit 1; }
RUN="$(cd "$RUN_IN" && pwd)"
SCR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -z "${VIRTUAL_ENV:-}" ] && [ -z "${MPM_NO_VENV:-}" ]; then
  for _v in "$SCR/../venv" "$SCR/../.venv" "$HOME/Yonghoon-DEM-DFT/venv"; do
    [ -f "$_v/bin/activate" ] && { . "$_v/bin/activate"; echo "[floor] venv $_v"; break; }
  done
fi

for f in se_dump.npy fibre.npy; do
  [ -f "$RUN/$f" ] || { echo "ABORT — $RUN/$f 가 없습니다 (압밀이 먼저)."; exit 1; }
done

cd "$RUN"
OUT="mpm_payload_amonly.json"
if [ -s "$OUT" ]; then
  echo "[floor] 이미 있습니다: $OUT — 보존하고 종료합니다 (지우고 다시 돌리세요)."
  exit 0
fi

python3 "$SCR/sr01_stamp_compare.py" --extract-payload "$KIT/run_mpm.sh" \
        --stamp segment --extra-flags '--sigma-vgcf 1e-9' \
        --tag amonly --out-name "$OUT" > _payload_amonly.sh || exit 1
{ echo 'set -uo pipefail'; echo "KIT=\"$KIT\""; echo "SCR=\"$SCR\"";
  echo "PSIG=(${MPM_PERIODIC_SIGMA:+--periodic})"; cat _payload_amonly.sh; } > payload_amonly.sh
rm -f _payload_amonly.sh

# ★ 주입이 실제로 들어갔는지 **돌리기 전에** 확인한다 (조용히 기본값 100 으로 도는 것 차단)
grep -q -- '--sigma-vgcf 1e-9' payload_amonly.sh || {
  echo "ABORT — payload_amonly.sh 에 --sigma-vgcf 가 안 들어갔습니다.  주입 실패."; exit 1; }
grep -q -- "--out $OUT" payload_amonly.sh || {
  echo "ABORT — --out 이 $OUT 로 안 바뀌었습니다."; exit 1; }
echo "[floor] 주입 확인 OK — --sigma-vgcf 1e-9 · --out $OUT · stamp segment"

bash payload_amonly.sh || { echo "[floor] FAILED — 위 트레이스"; exit 1; }

python3 - "$OUT" mpm_payload_segstamp.json <<'PY'
import json, os, sys


def s3_of(path):
    d = json.load(open(path))
    return d.get('step3') or (d.get('mpm_metrics') or {}).get('step3') or {}


s3 = s3_of(sys.argv[1])
print()
print('── AM-only 바닥 ──────────────────────────────────────────')
print('  sigma_e_eff_S_cm :', s3.get('sigma_e_eff_S_cm'))
print('  sigma_ion_eff    :', s3.get('sigma_ion_eff_S_cm'))
# ⚠ 2026-08-12: 첫 판은 `s3['electronic']['n_dof']` 를 봤는데 **그런 키가 없어** 양쪽 None 이
#   됐고, 검사가 "불일치" 라고 **거짓 경보**를 냈다.  실제 자리를 찾아 쓴다.
def n_dof_of(d):
    for path in (('electronic', 'n_dof'), ('sigma_e', 'n_dof'), ('n_dof_e',), ('n_dof',)):
        v = d
        for k in path:
            v = v.get(k) if isinstance(v, dict) else None
            if v is None:
                break
        if isinstance(v, int):
            return v
    return None


nd = n_dof_of(s3)
print('  n_dof(e)         :', nd)

# ★ 코드 드리프트 검사 — 이 런은 기존 두 팔보다 나중 코드로 돈다.
#   σ 값만 바꿨으므로 **전도 마스크는 같아야 한다** (--sigma-vgcf 1e-9 는 여전히 >0).
#   n_dof 가 선분 팔과 다르면 σ 아닌 무언가가 바뀐 것 = 브래킷이 오염됐다.
ref = sys.argv[2]
if os.path.exists(ref):
    r3 = s3_of(ref)
    rnd = n_dof_of(r3)
    print()
    if nd is not None and rnd is not None and nd == rnd:
        print(f'  ✓ n_dof 일치 (선분 팔 {rnd:,}) — 격자·마스크 불변, σ 만 달랐다.')
        print(f'    선분 팔 σ_e = {r3.get("sigma_e_eff_S_cm")}  ⇒ 바닥 대비 배수 = '
              f'{(r3.get("sigma_e_eff_S_cm") or 0) / (s3.get("sigma_e_eff_S_cm") or 1):.4g}×')
    elif nd is None or rnd is None:
        print(f'  ⚠ n_dof 를 못 읽었다 (바닥 {nd} · 선분 팔 {rnd}) — 검사 **미실시**.')
        print('     이것은 불일치가 아니다.  step3 의 n_dof 키 자리를 확인할 것.')
        print(f'    선분 팔 σ_e = {r3.get("sigma_e_eff_S_cm")}  ⇒ 배수 = '
              f'{(r3.get("sigma_e_eff_S_cm") or 0) / (s3.get("sigma_e_eff_S_cm") or 1):.4g}×')
    else:
        print(f'  ⚠⚠ n_dof 불일치: 바닥 {nd:,} vs 선분 팔 {rnd:,}')
        print('     σ 만 바꿨는데 전도 마스크가 달라졌다 = 그 사이 코드가 솔브 경로를 바꿨다.')
        print('     **브래킷에 쓰지 말 것** — 선분 팔을 같은 코드로 다시 돌려야 한다.')
else:
    print()
    print(f'  ⚠ 대조군 {ref} 이 없어 코드-드리프트 검사를 못 했다 (n_dof 비교 불가).')
print()
print('  ⇒ 이 값이 σ_e(참) 의 **하한**이다.  점/선분 팔과 나란히 놓아 ×35.79 를 브래킷할 것.')
PY
