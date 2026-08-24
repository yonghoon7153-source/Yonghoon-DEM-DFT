#!/usr/bin/env bash
# ★ 사전등록 v2 판별 런 — `docs/reviews/sdcp_gain_prereg_v2_20260816.md`
#
#   SBE / DBE 를 **vox 0.15 µm** 에서 **origin 8 팔 factorial** 로 푼다.
#   h0 (이득은 물리)        → σ_e 비 ≥ 1.05
#   h1 (SDCP 부피 인공물)  → σ_e 비 = 1.015
#   분해능 0.02 · 8 팔 표준오차 4.3σ (prereg §4)
#
# ⚠ 이 스크립트는 **판정을 하지 않는다** — 16 개 값을 전부 뽑아 JSON 으로 남긴다.
#   판정은 prereg §5 순서대로 `--verdict` 로 따로 돈다 (결과를 보고 창을 옮길 수 없게).
#
# ⚠ 고정해야 하는 것 (prereg §5): 브리지 반경을 **명시**한다.  기본 1.2·vox 는 격자마다
#   달라져 CL-22 의 결함을 반복한다.  vox 0.15 기본이면 0.18 µm — 여기서는 세 격자 비교에
#   쓴 값과 같은 **물리 단위**로 못 박는다.
#
# 사용 (원격 GPU 호스트):
#   . ~/dem-venv/bin/activate
#   cd ~/sdcp
#   setsid nohup bash ~/dem-sk/scripts/sdcp_gain_vox015_8arm.sh > p2.log 2>&1 &
#   tail -f p2.log
#   # 팔 하나만 시험:  ARMS=1 bash ~/dem-sk/scripts/sdcp_gain_vox015_8arm.sh
set -uo pipefail

VOX="${VOX:-0.15}"
BRIDGE_UM="${BRIDGE_UM:-0.48}"          # prereg §5 — 격자와 무관하게 고정
ARMS="${ARMS:-8}"
#  ★★ 2026-08-24 (CDXR3-7) — `ARMS` 는 **사전등록 계약이 아니다**.  옛 판은 마지막 봉인에
#    `--require-arms "$ARMS"` 를 줘서 **자기가 설정한 값을 자기한테 요구**했다 — ARMS=2 도
#    2팔을 요구하고 초록이 됐다 (실측).  prereg §4 가 고정한 것은 **8** 이다.
#    ⇒ 생산 봉인은 상수 8 로 건다.  8 이 아니면 **진단 런**이고, OUTDIR 을 갈라
#      생산 산출물과 같은 이름을 쓰지 못하게 한다 (재사용 오염 차단).
case "$ARMS" in
  ''|*[!0-9]*) echo "[p2] ABORT — ARMS 는 양의 정수 (받은 값: $ARMS)"; exit 2;;
esac
[ "$ARMS" -ge 1 ] || { echo "[p2] ABORT — ARMS >= 1 이어야 한다 (받은 값: $ARMS)"; exit 2; }
PREREG_ARMS=8
AR_TAG=""
if [ "$ARMS" -ne "$PREREG_ARMS" ]; then
  AR_TAG="_arm$ARMS"
  echo "[p2] ⚠ ARMS=$ARMS ≠ 사전등록 $PREREG_ARMS — **진단 런**이다."
  echo "     OUTDIR 에 $AR_TAG 를 붙여 생산 산출물과 갈라 놓는다.  생산 봉인은 걸지 않는다."
fi
#  ★ SDCP **부피-보존 구 스탬프** (2026-08-16, prereg v2 판정 h1 의 대응).
#    빈 값이면 현행 점 스탬프 = 사전등록 v2 판별 런과 같은 규약.
#    `SDCP_SPHERE_D=0.30` 을 주면 참 직경 구로 굽는다 — 태그와 OUTDIR 이 갈려 섞이지 않는다.
SDCP_SPHERE_D="${SDCP_SPHERE_D:-}"
SCR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SD_FLAG=""; SD_TAG=""
if [ -n "$SDCP_SPHERE_D" ]; then
  SD_FLAG=" --step3-sdcp-sphere-d $SDCP_SPHERE_D"; SD_TAG="_sph"
  echo "[p2] ★ SDCP **부피-보존 구 스탬프** Ø$SDCP_SPHERE_D µm (점 스탬프가 아니다)"
fi
# ★★ 2026-08-18 (심층 리뷰 ① H4) — OUTDIR 이 vox·(구/점) 만 구분해서, 같은 vox 를 **다른
#   브리지·다른 σ** 로 다시 돌리면 `[ -s "$OUT" ] && SKIP` 이 옛 팔을 전부 재사용하고
#   새 라벨로 보고했다.  판정기의 고정-인자 게이트는 팔들이 **같이 낡았으면** 통과한다.
#   ⇒ 설정을 디렉터리 이름에 넣는다 (`sr01_grid_converge_e.sh:34` 가 이미 쓰는 규약).
BR_TAG="_b${BRIDGE_UM/./}"
#  σ_VGCF 를 명시로 고정한 런은 **다른 실험**이다 — 디렉터리를 갈라 SKIP 이 섞이지 않게.
SG_TAG=""; [ -n "${SIGMA_VGCF_OVERRIDE:-}" ] && SG_TAG="_sg${SIGMA_VGCF_OVERRIDE//./}"
#  ★ σ-치환 진단 팔 (2026-08-18, CL-43/44 · prereg v3 §4b) — SDCP 가 VGCF 셀에 양보한다.
#    **생산 규약이 아니다.**  디렉터리·태그를 갈라 SKIP 캐시가 생산 팔과 섞이지 않게 한다
#    (판정기 게이트가 잡긴 하지만, 애초에 안 섞이는 것이 낫다 — H4 와 같은 이유).
YV_FLAG=""; YV_TAG=""
if [ "${SDCP_YIELD_VGCF:-0}" = "1" ]; then
  YV_FLAG=" --step3-sdcp-yield-to-vgcf"; YV_TAG="_yvgcf"
  echo "[p2] ★ **진단 팔** — SDCP 가 VGCF 셀에 양보 (σ-치환 채널 OFF).  생산 규약 아님"
fi
#  ★ PTFE 스탬프 감도 팔 (2026-08-18, CL-49 · CL-46 편차 검증) — **생산 규약이 아니다.**
#    `SIGMA_PTFE=1e-16` 이면 payload 가 phase-4 점을 격자에 찍는다 (`_cond_ph` 게이트).
#    PTFE 는 상 루프에서 VGCF·SDCP **뒤**라 그 셀을 덮는다 = 탄소망을 실제로 끊는다.
#    1e-16 = 실질 절연이되 `> 0` 게이트를 여는 최소값 (문헌 벌크 PTFE σ ~1e-16 S/cm).
PT_FLAG=""; PT_TAG=""
if [ -n "${SIGMA_PTFE:-}" ]; then
  PT_FLAG=" --sigma-ptfe $SIGMA_PTFE"; PT_TAG="_ptfe${SIGMA_PTFE//./}"
  echo "[p2] ★ **진단 팔** — PTFE 를 격자에 스탬프 (σ_PTFE=$SIGMA_PTFE).  생산 규약 아님 (CL-49)"
fi
#  ★★ 2026-08-24 (CDXR2-6) — PTFE **스탬프 규약**을 σ 와 따로 준다.
#    `PTFE_STAMP=centerline` + σ 미지정 = **exact-zero DOF** (sid 7 을 찍되 σ=0 이라
#    솔버의 `cond = sig > 0` 이 dof 에서 뺀다).  1e-16 우회로와 달리 조건수를 안 건드린다.
#    ⚠ 반드시 **태그와 OUTDIR 을 가른다** — P2_EXTRA 로 주면 이름이 안 갈려 옛 팔과
#      섞이고 SKIP 캐시가 오염된다 (H4 와 같은 실수).  그래서 전용 변수를 둔다.
PS_FLAG=""; PS_TAG=""
if [ -n "${PTFE_STAMP:-}" ]; then
  case "$PTFE_STAMP" in
    off|centerline) ;;
    capsule) echo "[p2] ABORT — PTFE_STAMP=capsule 은 **예약값이고 미구현**이다 (payload 가 " \
                  "unsupported_protocol 로 중단한다).  D-1 census 뒤에 구현한다"; exit 2;;
    *) echo "[p2] ABORT — PTFE_STAMP 는 off 또는 centerline (받은 값: $PTFE_STAMP)"; exit 2;;
  esac
  PS_FLAG=" --ptfe-stamp $PTFE_STAMP"; PS_TAG="_pts${PTFE_STAMP}"
  if [ -z "${SIGMA_PTFE:-}" ] && [ "$PTFE_STAMP" != "off" ]; then
    echo "[p2] ★ **진단 팔** — PTFE 스탬프 $PTFE_STAMP · σ_PTFE 미지정 = **exact-zero DOF**." \
         " 생산 규약 아님 (CDXR2-6)"
  else
    echo "[p2] ★ PTFE 스탬프 규약 = $PTFE_STAMP (명시)"
  fi
fi
# ★ 스윕 팔에서 끌 것 (리뷰 ① H7): 팔당 σ_e 솔브 1회가 아니라 **7~8회**가 돈다.
#   `--no-step4`(2×dof 연성계) · `--no-thermal` · `--no-trackb`(기하 τ) · `--no-field`.
#   ⚠ `_res3w`/`_res3b`(collector wetted/bare)는 끄는 플래그가 **없어** 2회는 남는다 —
#     그리고 그 둘은 shift 팔에서 `_bot_mask` 가 origin 을 안 더해 어차피 틀린 값이다.
#   기본은 빈 값 = 기존 거동 유지.  스윕은 `LEAN=1` 로 켠다.
#   ★★ 2026-08-18 — `LEAN=2` (**σ_e 전용**) 신설.  vox 0.125 스윕이 이온계 조립 중
#     `Killed` 로 죽었다 (전자 45.1 M dof 위에 이온 36.7 M dof).  그리고 DR3-07 대로
#     vox ≤ 0.125 의 σ_ion·pore-τ 는 **어차피 인용 금지**다 — 실측으로 pore-τ 가
#     1,415 → 4.97e9 로 터졌다.  ⇒ 스윕에서는 둘 다 끈다.
#     ⚠ `LEAN=1` 의 뜻은 **바꾸지 않는다** — 이미 그 값으로 돈 팔(STEP 2/3/5)의 규약을
#       소급해 흔들지 않기 위해서다.  스윕만 2 를 쓴다.
#  ★ 2026-08-20 — 진단 팔이 코드 수정 없이 payload 플래그를 더할 수 있게.
#    예: `P2_EXTRA="--step3-maxiter 200000"`.  ⚠ 태그·OUTDIR 에는 안 들어가므로
#    **규약을 바꾸는 플래그는 여기로 주지 말 것** (섞이면 판정기가 못 잡는다).
LEAN_FLAGS=""
[ "${LEAN:-0}" = "1" ] && LEAN_FLAGS=" --no-step4 --no-thermal --no-trackb --no-field"
#     ★ 2026-08-18 2차: `--no-collector` 도 넣는다.  1차 LEAN=2 시도가 **집전체 기하 솔브**
#       에서 또 죽었다 (p2_DBE_sph_a3: 전자 솔브 0.06071 수렴 후 사망).  그 2회 솔브는
#       shift 팔에서 `_bot_mask` 가 origin 을 안 더해 **어차피 무효**다 (위 주석 참조).
[ "${LEAN:-0}" = "2" ] && { LEAN_FLAGS=" --no-step4 --no-thermal --no-trackb --no-field --no-ion --no-pore --no-collector"; \
  echo "[p2] ★ LEAN=2 (σ_e 전용) — 이온·pore-τ·집전체기하 를 전부 끈다 (팔당 솔브 3회 → 1회)"; }
#  ⚠ LEAN=1 은 **옛 접미사 `_lean` 그대로** 둔다 — 이미 끝난 팔(STEP 2/3/5)이 살아 있는
#    디렉터리라 이름을 바꾸면 전부 다시 돈다.  LEAN=2 만 새 접미사를 받는다.
#  ★★ 2026-08-20 (게이트 ⑤ factorial) — **섬유 스탬프 축**.  CL-19 가 retired 된 이유가
#    점 팔과 선분 팔에 **서로 다른 σ_VGCF** 를 줘서 두 축을 동시에 움직인 것이었다.
#    가르려면 `{점,선분} × {σ 두 값}` 4조합이 필요한데, 여태 이 러너는 `segment` 를
#    **세 군데에 하드코딩**하고 있었다 (SKIP 검사 · 그 진단 · payload 주입).
#    ⚠ 그래서 `P2_EXTRA="--step3-fibre-stamp point"` 같은 우회는 **조용히 무력**하다:
#      OUTDIR 태그가 안 갈려 기존 선분 팔과 같은 폴더를 보고, SKIP 검사가 `--stamp segment`
#      로 그 팔들을 "완전" 이라 판정해 **아무것도 안 돌고 끝난다**.
#    ⇒ 축을 정식 노브로 올린다.  기본은 segment (기존 동작 그대로).
FIBRE_STAMP="${FIBRE_STAMP:-segment}"
case "$FIBRE_STAMP" in
  point|segment) ;;
  *) echo "ABORT — FIBRE_STAMP 는 point 또는 segment (받은 값: $FIBRE_STAMP)"; exit 2;;
esac
FS_TAG=""; [ "$FIBRE_STAMP" = "point" ] && FS_TAG="_fspt"
FS_FLAG=""; [ "$FIBRE_STAMP" = "point" ] && FS_FLAG=" --step3-fibre-stamp point"
LEAN_TAG=""; [ "${LEAN:-0}" = "1" ] && LEAN_TAG="_lean"; [ "${LEAN:-0}" = "2" ] && LEAN_TAG="_lean2"
OUTDIR="${OUTDIR:-$PWD/prereg_v2_vox${VOX/./}${SD_TAG}${BR_TAG}${SG_TAG}${YV_TAG}${PT_TAG}${PS_TAG}${FS_TAG}${AR_TAG}${LEAN_TAG}}"
#  ★★★ RUNNER_CONFIG_END — 여기까지가 **순수 변수 조립**이다 (부작용 없음).
#    규칙 L 이 이 지점까지를 서브셸에서 **실제로 실행해** 조립 결과를 검사한다.
#    그 아래는 mkdir·venv·게이트라 실행하면 안 된다.  ⚠ 이 표지를 옮기면 규칙 L 이
#    다른 것을 재게 되므로, 옮길 때는 규칙 L 의 기대값도 같이 본다.
#  ⚠ 이름 규약이 바뀌었다 — 2026-08-16/17 판별 런은 `prereg_v2_vox015[_sph]` 에 있다.
#    그 팔들을 다시 돌리고 싶지 않으면 `OUTDIR=` 로 옛 경로를 명시할 것.
_LEGACY="$PWD/prereg_v2_vox${VOX/./}${SD_TAG}"
if [ -d "$_LEGACY" ] && [ ! -d "$OUTDIR" ]; then
  echo "[p2] ⚠ 옛 출력 디렉터리가 있다: $_LEGACY"
  echo "     새 규약은 $OUTDIR — 그대로 두면 **처음부터 다시 돈다**."
  echo "     옛 팔을 이어 쓰려면:  OUTDIR=\"$_LEGACY\" bash \$0 …"
fi
mkdir -p "$OUTDIR"

if [ -z "${VIRTUAL_ENV:-}" ] && [ -z "${MPM_NO_VENV:-}" ]; then
  for _v in "$HOME/dem-venv" "$SCR/../venv" "$SCR/../.venv"; do
    [ -f "$_v/bin/activate" ] && { . "$_v/bin/activate"; echo "[p2] venv $_v"; break; }
  done
fi

# ── 게이트: prereg 와 코드가 실제로 준비됐는지 (fail-closed) ─────────────────────────
PREREG="$SCR/../docs/reviews/sdcp_gain_prereg_v2_20260816.md"
[ -f "$PREREG" ] || { echo "ABORT — 사전등록 파일이 없다: $PREREG"; exit 2; }
python3 -c "
import sys; sys.path.insert(0,'$SCR')
import argparse, importlib.util as iu
spec = iu.spec_from_file_location('m','$SCR/mpm_webapp_payload.py')
src = open('$SCR/mpm_webapp_payload.py', encoding='utf-8').read()
assert '--step3-origin-shift' in src, 'origin 이동 CLI 가 없다 — 8 팔을 돌릴 수 없다'
print('  [p2] origin 이동 CLI 확인')
" || exit 2
#  ⚠ 2026-08-20 — 실패 **이유를 버리지 않는다**.  옛 코드는 `>/dev/null 2>&1` 이라
#    "먼저 통과시킬 것" 만 찍고 무엇이 걸렸는지 알 수 없었다 (kgy 실사고).
_DISC_LOG="$(mktemp)"
if ! PYTHONUTF8=1 python3 "$SCR/check_method_discipline.py" >"$_DISC_LOG" 2>&1; then
  echo "ABORT — 방법론 규율 검사 실패.  먼저 통과시킬 것"
  echo "──── 실패한 항목 ────"
  grep -E '^(ERR|✗|  ✗|[A-Z]_[A-Z]+\|)' "$_DISC_LOG" | head -20
  tail -5 "$_DISC_LOG"
  echo "──── 전체 로그: $_DISC_LOG ────"
  exit 2
fi
rm -f "$_DISC_LOG"
echo "[p2] 규율 검사 통과"
#  ★ 미정의 이름 게이트 (실사고 2026-08-16): 판별 런이 SE 점 6,792 만 개를 읽은 **뒤**
#    `NameError: _zt3` 로 죽었다.  런이 실제로 쓰는 파일만 정적으로 먼저 본다.
PYTHONUTF8=1 python3 "$SCR/check_undefined_names.py" \
  "$SCR/mpm_webapp_payload.py" "$SCR/step3_sigma.py" "$SCR/viz_mpm_continuum.py" \
  "$SCR/additives.py" "$SCR/sr01_stamp_compare.py" >/dev/null 2>&1 \
  || { echo "ABORT — 미정의 이름 발견.  다음으로 확인:"; \
       PYTHONUTF8=1 python3 "$SCR/check_undefined_names.py" \
         "$SCR/mpm_webapp_payload.py" "$SCR/step3_sigma.py" "$SCR/viz_mpm_continuum.py" \
         "$SCR/additives.py" "$SCR/sr01_stamp_compare.py"; exit 2; }
echo "[p2] 미정의 이름 없음 (런 경로 5 파일)"

# ── 8 팔 = {0, vox/2}³ ─────────────────────────────────────────────────────────────
H=$(python3 -c "print(f'{$VOX/2:.6f}')")
SHIFTS=()
for X in 0 "$H"; do for Y in 0 "$H"; do for Z in 0 "$H"; do
  SHIFTS+=("$X $Y $Z")
done; done; done

run_arm() {   # $1=kit dir  $2="sx sy sz"  $3=tag
  local KIT="$1" SH="$2" TAG="$3"
  local RUN OUT
  if [ -e "$KIT/latest_run" ]; then RUN="$(cd "$KIT/latest_run" && pwd)"
  else
    RUN=""; for d in "$KIT"/run_*; do [ -f "$d/se_dump.npy" ] && RUN="$(cd "$d" && pwd)"; done
  fi
  [ -n "$RUN" ] || { echo "[p2] ABORT — $KIT 압밀 런 없음"; return 1; }
  OUT="$OUTDIR/${TAG}.json"
  #  ★★ 2026-08-18 (심층 리뷰 ① B2) — `[ -s "$OUT" ]` 는 **파일이 있기만 하면** SKIP 했다.
  #    구 스탬프 게이트가 fail-open 이던 시절 그 조합은 치명적이었다: 쓰레기 JSON 이
  #    영구 캐시된다.  게이트는 이제 fail-closed(SystemExit)지만, 재개 판정 자체를
  #    **쓸 수 있는 결과인가**로 올린다 — 그 검사기는 이미 있었고 이 러너만 안 썼다.
  if [ -s "$OUT" ]; then
    if python3 "$SCR/sr01_stamp_compare.py" --check-arm "$OUT" --stamp "$FIBRE_STAMP" \
         --expect-backend "${EXPECT_BACKEND:-gpu}" >/dev/null 2>&1; then
      echo "[p2] SKIP (완전) $TAG"; return 0
    fi
    echo "[p2] ⚠ 기존 $TAG 이 불완전 — 다시 돈다:"
    python3 "$SCR/sr01_stamp_compare.py" --check-arm "$OUT" --stamp "$FIBRE_STAMP" \
      --expect-backend "${EXPECT_BACKEND:-gpu}" 2>&1 | sed 's/^/     /'
    rm -f "$OUT"
  fi

  # 이 vox 의 직경-보존 σ_VGCF 를 다시 뽑는다 (격자마다 다르다 — 기존 러너와 같은 규약)
  local SIGMA
  #  ★★ 2026-08-18 (심층 리뷰 ① H1 / DR3-05) — σ_VGCF 를 **명시로 못 박는 통로**.
  #    직경-보존 재척도는 `σ = 100·πd²/(4·vox²)` 라 vox 의 함수다 (0.15 → 78.540 ·
  #    0.125 → 113.097 · 0.10 → 176.715).  그런데 σ_SDCP 는 250 고정이므로 격자 스윕이
  #    **탄소 백본 대비 SDCP 의 상대 전도도를 2.25배 같이 바꾼다** = 격자 축과 재료 축이
  #    섞인다 (CL-19 가 retired 된 것과 같은 구조).  이 override 로 두 축을 가른다:
  #      · `SIGMA_VGCF_OVERRIDE=113.097` + VOX=0.15  → σ 만 이동 (dR/dlnσ_VGCF 측정)
  #      · `SIGMA_VGCF_OVERRIDE=0`                   → VGCF 를 전기적으로 죽인다
  #        (셀은 남아 부피를 막는다 — `_cond_ph` 가 phase 2 를 항상 스탬프한다)
  if [ -n "${SIGMA_VGCF_OVERRIDE:-}" ]; then
    SIGMA="$SIGMA_VGCF_OVERRIDE"
    echo "[p2] ★ σ_VGCF **명시 고정** $SIGMA S/cm (직경-보존 재척도 우회)"
  else
  #  ⚠ 2026-08-16 실사고: `P2_SCR` 를 이 heredoc 에 안 넘겨 KeyError 로 전 팔이 실패했다.
  #    (fail-closed 는 작동했다 — 쓰레기 대신 0 팔을 냈다.)  두 변수를 **여기서** 넘긴다.
  SIGMA=$(cd "$RUN" && P2_SCR="$SCR" STEP3_VOX="$VOX" python3 - <<'PY'
import os, sys
import numpy as np
sys.path.insert(0, os.environ['P2_SCR'])
import step3_sigma as s3
VOX, D_REF = float(os.environ['STEP3_VOX']), 0.15
dia, ph = np.load('fibre_dia.npy'), np.load('phase.npy')
st = s3.dia_stats_by_phase(dia, ph)
v = st.get(2)
if v is None or not v['uniform']:
    sys.stderr.write(f'ABORT — VGCF Ø 비균일/부재: {v}\n'); raise SystemExit(1)
se, pv = s3.diameter_preserving_sigma(100.0, dia[ph == 2], D_REF, VOX)
sys.stderr.write(f'  [p2] vox {VOX}: σ_VGCF 100 → {se:.6g}\n')
print(f'{se:.6g}')
PY
  ) || return 1
  fi

  #  ★★ 2026-08-19 — 팔 스크립트를 **프로세스별 이름 + 원자적 쓰기**로.
  #    실사고: STEP 4 런에서 `--out p2_SBE_sph_a0.json` 이 토큰 한가운데서 잘려
  #    (`line 9: 2_SBE_sph_a0.json: command not found`) payload 가 **정상 완주한 뒤** 죽었다.
  #    옛 판은 두 런이 같은 `$RUN/$TAG.sh` 를 공유했다 — 한쪽이 쓰는 도중 다른 쪽이 읽으면
  #    **반쯤 쓰인 파일**을 실행한다.  `$$` 로 갈라 놓으면 그 경합이 원리적으로 사라지고,
  #    `mv` 로 원자화하면 부분 파일을 볼 수 없다.  (⚠ 근본 원인 미확정이지만 이 수정은
  #    원인이 무엇이든 이 실패 형태를 없앤다.)
  #  ★★ 2026-08-25 (CDXR3-3) — 러너가 **기대 규약 id** 를 넘긴다.  빈 값이면 payload 가
  #    적용값에서 파생만 하고 대조는 안 한다 (옛 거동).  `EXPECT_PROTOCOL=p1-...` 을 주면
  #    payload 가 적용값과 대조해 다르면 **exit 4** 로 죽는다 = 요청↔적용 end-to-end 봉인.
  #    ⚠ 첫 팔의 payload 가 찍은 id 를 읽어 나머지 팔에 넘기는 것이 표준 용법이다
  #      (규약이 도중에 조용히 바뀌는 것을 그때 잡는다).
  local EP_FLAG=""
  [ -n "${EXPECT_PROTOCOL:-}" ] && EP_FLAG=" --expect-protocol $EXPECT_PROTOCOL"
  local SHF="$RUN/${TAG}.$$.sh"
  ( cd "$RUN" && P2_SCR="$SCR" python3 "$SCR/sr01_stamp_compare.py" \
      --extract-payload "$KIT/run_mpm.sh" --stamp "$FIBRE_STAMP" \
      --extra-flags "--sigma-vgcf $SIGMA --step3-vox $VOX --step3-bridge-um $BRIDGE_UM --step3-origin-shift $SH$SD_FLAG$YV_FLAG$PT_FLAG$PS_FLAG$EP_FLAG$FS_FLAG$LEAN_FLAGS${P2_EXTRA:+ $P2_EXTRA}" \
      --tag "$TAG" --out-name "$(basename "$OUT")" > "$SHF.body" ) || return 1
  { echo 'set -uo pipefail'; echo "KIT=\"$KIT\""; echo "SCR=\"$SCR\"";
    echo "PSIG=(${MPM_PERIODIC_SIGMA:+--periodic})"; cat "$SHF.body"; } > "$SHF.part" \
    && mv -f "$SHF.part" "$SHF"
  rm -f "$SHF.body"
  # ★★ 2026-08-19 fail-closed — **생성된 스크립트 자체가 온전한가**.
  #   실사고: `--out p2_SBE_sph_a0.json` 토큰이 줄바꿈으로 **한가운데서 잘렸다**
  #   (line 8 이 `--out p` 로 끝나고 line 9 가 `2_SBE_sph_a0.json`).  bash 문법으로는
  #   유효해서(두 개의 명령) `bash -n` 도 통과하고, payload 는 **정상 완주한 뒤** 다음 줄에서
  #   `command not found` 로 죽는다 = 40 분을 버리고 팔이 실패한다.
  #   ⇒ 돌기 **전에** --out 토큰이 한 줄에 붙어 있는지 본다.  잘린 파일은 지우지 않고 남긴다.
  _ON="$(basename "$OUT")"
  if ! grep -q -- "--out $_ON" "$SHF"; then
    echo "[p2] ABORT — 생성된 $TAG.sh 에서 \`--out $_ON\` 토큰이 온전하지 않다 (줄바꿈에 잘렸나?)."
    echo "     파일을 남겨 둔다: $SHF"
    echo "     ── 문제 줄 ──"; grep -n -- '--out' "$SHF" | sed 's/^/     /'
    echo "     ── 줄 길이 ──"; awk '{printf "     %d: %d chars\n", NR, length($0)}' "$SHF"
    return 1
  fi
  bash -n "$SHF" || { echo "[p2] ABORT — 생성된 $TAG.sh 가 bash 문법 오류"; return 1; }
  # ★ fail-closed — 세 인자가 **실제로** 주입됐는지 확인 (조용히 빠지면 팔이 오염된다)
  for NEEDLE in "--step3-vox $VOX" "--step3-origin-shift $SH" "--step3-bridge-um $BRIDGE_UM" \
                ${SDCP_SPHERE_D:+"--step3-sdcp-sphere-d $SDCP_SPHERE_D"}; do
    grep -q -- "$NEEDLE" "$SHF" || { echo "[p2] ABORT — 미주입: $NEEDLE"; return 1; }
  done
  echo "[p2] ── $TAG  shift=($SH)  σ_VGCF=$SIGMA"
  #  ★★ 2026-08-19 — **피크 호스트 RAM 을 실측**한다.  vox 0.10 이 가용 57 GB 에서
  #    조립 중 OOM 으로 죽었는데(로그가 `STEP3 solve:` 전에 아무 에러 없이 끊김 =
  #    OOM killer 의 SIGKILL), 러너의 RAM 문턱(0.1 → 40 GB)은 **dof 투영에서 나온 추정**이라
  #    실제 피크를 몰랐다.  ⇒ 추정을 실측으로 바꾼다.  `/usr/bin/time -v` 가 있으면
  #    "Maximum resident set size" 를 찍고, 없으면 조용히 그냥 돈다 (기능은 안 막는다).
  #    ⚠ 이 값은 **한 팔의 피크**다.  팔은 순차 실행이므로 동시 합산이 아니다.
  local TIMEV="" RSSLOG="$RUN/.peak_rss_${TAG}.txt"
  [ -x /usr/bin/time ] && TIMEV="/usr/bin/time -v -o $RSSLOG"
  ( cd "$RUN" && $TIMEV bash "$(basename "$SHF")" ) || { echo "[p2] $TAG FAILED"; return 1; }
  if [ -s "$RSSLOG" ]; then
    local PK
    PK=$(awk -F': *' '/Maximum resident set size/{print $2}' "$RSSLOG")
    [ -n "$PK" ] && echo "[p2] ▸ $TAG 피크 호스트 RSS = $(awk -v k="$PK" 'BEGIN{printf "%.1f", k/1048576}') GB"
  fi
  #  ★★ 2026-08-24 (CDXR2-5) — **fresh 팔도 검사한다.**  옛 판은 **캐시된** 팔만
  #    `--check-arm` 을 돌리고 갓 만든 팔은 그대로 옮겼다.  payload 는 STEP3 예외를
  #    `status: failed` 로 적고 **exit 0** 으로 끝낼 수 있으므로
  #    (`mpm_webapp_payload.py` 의 `except Exception` 경로), 쓰레기 JSON 이 검사 없이
  #    $OUTDIR 로 들어가고 다음 실행에서 "SKIP (완전)" 로 **영구 캐시**된다.
  #    ⇒ 옮기기 **전에** 같은 검사기를 건다.  실패하면 옮기지 않고 $RUN 에 남겨 둔다
  #      (증거 보존 — 지우면 왜 죽었는지 못 본다).
  local FRESH="$RUN/$(basename "$OUT")"
  [ -s "$FRESH" ] || { echo "[p2] ABORT — $TAG 이 산출물을 안 남겼다 ($FRESH)"; return 1; }
  if ! python3 "$SCR/sr01_stamp_compare.py" --check-arm "$FRESH" --stamp "$FIBRE_STAMP" \
       --expect-backend "${EXPECT_BACKEND:-gpu}" >/dev/null 2>&1; then
    echo "[p2] ABORT — 갓 만든 $TAG 이 불완전하다.  **옮기지 않는다** (캐시 오염 방지):"
    python3 "$SCR/sr01_stamp_compare.py" --check-arm "$FRESH" --stamp "$FIBRE_STAMP" \
      --expect-backend "${EXPECT_BACKEND:-gpu}" 2>&1 | sed 's/^/     /'
    echo "     원본을 남겨 둔다: $FRESH"
    return 1
  fi
  mv "$FRESH" "$OUT"
}

echo "[p2] vox $VOX · 브리지 $BRIDGE_UM µm 고정 · 섬유 $FIBRE_STAMP · $ARMS 팔 · out $OUTDIR"
i=0
for SH in "${SHIFTS[@]}"; do
  [ "$i" -ge "$ARMS" ] && break
  for K in kit_SBE kit_DBE; do
    [ -d "$K" ] || { echo "[p2] ABORT — $K 없음 (~/sdcp 에서 돌릴 것)"; exit 2; }
    #  ★ fail-fast — 한 팔이 실패하면 **전체를 멈춘다**.  실패한 팔을 빼고 계속하면
    #    팔 수가 달라져 앙상블이 오염된다 (판정기가 HOLD 를 내겠지만 GPU 시간을 버린다).
    if ! run_arm "$(cd "$K" && pwd)" "$SH" "p2_${K#kit_}${SD_TAG}_a${i}"; then
      echo "[p2] ABORT — 팔 p2_${K#kit_}${SD_TAG}_a${i} 실패.  원인을 고치고 다시 돌릴 것"
      echo "     (이미 끝난 팔은 $OUTDIR 에 남아 있어 다음 실행에서 SKIP 된다)"
      exit 1
    fi
  done
  i=$((i+1))
done

echo
echo "[p2] 수집 — 판정은 하지 않는다 (prereg §5 순서로 따로)"
python3 "$SCR/sdcp_gain_verdict.py" --dir "$OUTDIR" --collect-only

#  ★★ 2026-08-24 (CDXR2-5) — `--collect-only` 는 **항상 exit 0** 이라 팔이 모자라도·
#    미수렴이어도·고정인자가 어긋나도 러너가 초록으로 끝났다.  그렇다고 러너가 판정을
#    돌리면 이 파일 헤더의 규약("결과를 보고 창을 옮길 수 없게")이 깨진다.
#    ⇒ **봉인과 판정을 가른다**: 봉인 = 데이터가 쓸 만한가, 판정 = 그것이 뭐라고 말하는가.
#      `--seal-only` 는 h0/h1 과 비를 **출력하지 않으므로** 사전등록이 안 깨진다.
#  ⚠ 상수 8 로 건다 ($ARMS 가 아니다 — 그것이 CDXR3-7 의 자기참조였다).
if [ "$ARMS" -eq "$PREREG_ARMS" ]; then
  if ! python3 "$SCR/sdcp_gain_verdict.py" --dir "$OUTDIR" --seal-only \
       --require-arms "$PREREG_ARMS"; then
    echo "[p2] ✗ 계약 봉인이 깨졌다 — 위 근거를 고치고 다시 돌 것"
    exit 1
  fi
  echo "[p2] ✓ 계약 봉인 통과 ($PREREG_ARMS 팔).  판정은 prereg §5 순서로 **따로** 돌 것"
else
  echo "[p2] ⚠ **진단 런 ($ARMS 팔) — 생산 봉인 아님.**  이 산출물로 판정하지 말 것."
  echo "     사전등록은 $PREREG_ARMS 팔이다 (prereg §4).  OUTDIR: $OUTDIR"
fi
