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
#  ★★★ 2026-08-25 (R3-CX-09, Codex 3차) — **진단 런이 생산 이름공간을 못 쓴다.**
#    옛 판은 ⓐ ARMS > 8 을 허용했고(실제 shift 는 8개뿐이라 조용히 8 로 잘린다)
#    ⓑ 명시 `OUTDIR` 이 조립된 `_armN` 태그를 **통째로 덮어** `ARMS=2 OUTDIR=<생산경로>`
#    로 진단 파일을 생산 이름에 쓸 수 있었다.
#    ⇒ 상한을 강제하고, ARMS≠8 이면 사용자 OUTDIR 에도 접미사를 **붙인다**.
if ! [ "$ARMS" -ge 1 ] 2>/dev/null || [ "$ARMS" -gt 8 ]; then
  echo "ABORT — ARMS=$ARMS 는 1..8 이어야 한다 (SHIFTS 가 8개다; 초과는 조용히 잘린다)"
  exit 2
fi
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
#  ★ 2026-08-25 — `bash -s`(stdin) 로 설정부만 돌리면 `BASH_SOURCE` 가 없다 (규칙 L 이 그렇게 돈다).
#    `P2_SCR` 를 먼저 보고, 없으면 `$0` 로 떨어진다 — 리포에 이미 있는 규약이다.
SCR="${P2_SCR:-$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)}"

#  ★★★ 2026-09-02 — **읽지 않는 축 env 는 조용히 무시되면 안 된다** (실측 사고).
#    사고: closure 스윕 중심점을 `SIGMA_AM_S_OVERRIDE=0.01 SIGMA_SDCP_OVERRIDE=250` 으로
#    띄웠는데 kgy 의 `~/dem-mt` 가 **배선 이전 커밋**이었다.  두 변수는 그냥 안 읽히는
#    환경변수가 됐고, 그 값들이 마침 프리셋 기본값과 같아서 런은 **정확히 옳은 σ_e 를
#    내며 통과**했다 — 아무것도 시험하지 않은 채로.  디렉터리 태그를 눈으로 확인하지
#    않았다면 그대로 25 격자점 스윕에 들어갔다.
#  ⚠ 이 부류의 위험은 "틀린 답" 이 아니라 **"맞는 답인데 근거가 없는 것"** 이다.
#    사전등록 축이 적용되지 않은 팔은 대조로도 판정으로도 쓸 수 없다.
#  ⇒ **목록을 손으로 유지하지 않는다** (이 리포가 그 방식으로 세 번 졌다 —
#    `SBRG_FLAG`·`RQG_FLAG`·`AS_FLAG`).  러너가 **자기 소스를 읽어** 실제로 역참조하는
#    이름만 인정하고, 축 이름꼴(`SIGMA_*`·`SDCP_*`·`PTFE_*`)인데 안 읽는 것이 설정돼
#    있으면 **죽는다**.  주석에 이름이 적힌 것만으로는 통과하지 않는다 (`$VAR` 역참조를 본다).
_SELF="${P2_SELF:-${BASH_SOURCE[0]:-$0}}"
if [ -r "$_SELF" ]; then
  _p2_unread=""
  for _v in $(env | sed -n 's/^\(SIGMA_[A-Z0-9_]*\|SDCP_[A-Z0-9_]*\|PTFE_[A-Z0-9_]*\)=.*/\1/p'); do
    grep -qE '\$\{?'"$_v"'\b' "$_SELF" || _p2_unread="$_p2_unread $_v"
  done
  if [ -n "$_p2_unread" ]; then
    echo "[p2] ABORT — 이 러너가 **읽지 않는** 축 env 를 받았다:$_p2_unread"
    echo "     그대로 돌면 그 축이 조용히 무시된 채 런이 통과한다 — 값이 우연히 기본값과"
    echo "     같으면 **옳은 숫자를 내면서 아무것도 시험하지 않는다** (2026-09-02 실측)."
    echo "     원인 대개: 러너 코드가 배선 이전 커밋이다.  고치는 법:"
    echo "       git -C \"\$(dirname \"$SCR\")\" fetch origin claude/stoic-knuth-NObVQ"
    echo "       git -C \"\$(dirname \"$SCR\")\" merge --ff-only origin/claude/stoic-knuth-NObVQ"
    echo "     오타라면 이름을 고칠 것.  러너: $_SELF"
    exit 2
  fi
elif env | grep -qE '^(SIGMA_|SDCP_|PTFE_)[A-Z0-9_]*='; then
  #  자기 소스를 못 읽는 경로(`bash -s` 등)에서 축 env 가 실려 오면 **판정 불가**다.
  #  fail-open 하면 위 사고가 그대로 재발하므로 여기서도 죽는다.
  echo "[p2] ABORT — 축 env 가 설정됐는데 러너가 자기 소스($_SELF)를 못 읽어 배선을 확인할 수 없다."
  echo "     `P2_SELF=<러너 경로>` 를 주거나 파일로 직접 실행할 것."
  exit 2
fi
#  ★ 위 게이트만 돌려 보고 나가는 문 (규율 검사기가 GPU 없이 거동을 시험한다).
[ -n "${P2_ENV_GUARD_ONLY:-}" ] && { echo "[p2] env 게이트 통과"; exit 0; }

SD_FLAG=""; SD_TAG=""
if [ -n "$SDCP_SPHERE_D" ]; then
  SD_FLAG=" --step3-sdcp-sphere-d $SDCP_SPHERE_D"; SD_TAG="_sph"
  echo "[p2] ★ SDCP **부피-보존 구 스탬프** Ø$SDCP_SPHERE_D µm (점 스탬프가 아니다)"
fi

#  ★ 판별 축 (2026-08-25, sdcp_bridge_prereg_20260825) — SDCP 접촉 브리지.
#    P2_EXTRA 허용 목록이 물리 플래그를 막는 것이 **옳으므로**, 사전등록 §7 의
#    `P2_EXTRA="--step3-sdcp-bridge …"` 표기는 이 축으로 대체된다 (판정선 불변).
#    ⚠ 기존 `BRIDGE_UM` 은 **AM–AM 접촉 브리지**로 다른 축이다 — 이름을 갈랐다.
SBRG_FLAG=""; SBRG_TAG=""
if [ -n "${SDCP_BRIDGE:-}" ]; then
  case "$SDCP_BRIDGE" in
    *[!0-9.]*|"") echo "[p2] ABORT — SDCP_BRIDGE 는 µm 숫자여야 한다 (받은 값: $SDCP_BRIDGE)"; exit 2;;
  esac
  #  ⚠⚠ **fail-closed (2026-08-27)** — 브리지는 구 반지름 r = d/2 에서 정의된다.
  #     `SDCP_SPHERE_D` 없이 브리지만 주면 점 스탬프가 되고 브리지는 **조용히 사라진다**.
  #     2026-08-27 A 트랙 4팔이 정확히 그렇게 무효화됐다 (처리팔이 대조팔과 바이트 동일,
  #     `INVALID_TREATMENT_NOT_APPLIED`).  step3 안에도 같은 가드가 있지만 그쪽은 격자를
  #     찍는 시점 = 이미 DEM·MPM 을 몇 시간 돌린 뒤다.  여기서 **초 단위로** 죽인다.
  if [ -z "${SDCP_SPHERE_D:-}" ]; then
    echo "[p2] ABORT — SDCP_BRIDGE=$SDCP_BRIDGE 인데 SDCP_SPHERE_D 가 비었다."
    echo "      브리지 기하는 구 반지름 r=d/2 에서 정의된다 → 점 스탬프에서는 **no-op** 이고"
    echo "      처리팔이 대조팔과 바이트 동일해진다 (2026-08-27 A 트랙 무효화 원인)."
    echo "      고치는 법:  SDCP_SPHERE_D=0.30 SDCP_BRIDGE=$SDCP_BRIDGE ... 로 **둘 다** 줄 것."
    exit 2
  fi
  SBRG_FLAG=" --step3-sdcp-bridge $SDCP_BRIDGE"; SBRG_TAG="_sbrg${SDCP_BRIDGE//./}"
  echo "[p2] ★ **판별 팔** — SDCP 접촉 브리지 tol=$SDCP_BRIDGE µm.  생산 규약 아님"        "(sdcp_bridge_prereg_20260825 — 진단 전용, 기본 off)"
fi

# ★★ 2026-08-18 (심층 리뷰 ① H4) — OUTDIR 이 vox·(구/점) 만 구분해서, 같은 vox 를 **다른
#   브리지·다른 σ** 로 다시 돌리면 `[ -s "$OUT" ] && SKIP` 이 옛 팔을 전부 재사용하고
#   새 라벨로 보고했다.  판정기의 고정-인자 게이트는 팔들이 **같이 낡았으면** 통과한다.
#   ⇒ 설정을 디렉터리 이름에 넣는다 (`sr01_grid_converge_e.sh:34` 가 이미 쓰는 규약).
BR_TAG="_b${BRIDGE_UM/./}"
#  σ_VGCF 를 명시로 고정한 런은 **다른 실험**이다 — 디렉터리를 갈라 SKIP 이 섞이지 않게.
SG_TAG=""; [ -n "${SIGMA_VGCF_OVERRIDE:-}" ] && SG_TAG="_sg${SIGMA_VGCF_OVERRIDE//./}"
#  ★★ 2026-09-02 (사전등록 `sigma_closure_sweep_prereg_20260902.md`) — **두 대비를 축으로.**
#    R20-05: 비의 불확실성은 공통 스케일이 아니라 `σ_AM_S/σ_VGCF` · `σ_SDCP/σ_VGCF` **두
#    독립 대비**에 있고 그것은 상쇄되지 않는다.  그 스윕을 하려면 두 σ 도 러너 축이어야
#    한다 (payload CLI 에는 `--sigma-am-s`·`--sigma-sdcp` 가 이미 있었고 러너만 안 넘겼다).
#  ⚠ 값을 고정한 런은 **다른 실험**이므로 디렉터리를 가른다 (SG_TAG 와 같은 규칙).
AS_TAG=""; AS_FLAG=""
if [ -n "${SIGMA_AM_S_OVERRIDE:-}" ]; then
  case "$SIGMA_AM_S_OVERRIDE" in ''|*[!0-9.eE+-]*)
    echo "ABORT — SIGMA_AM_S_OVERRIDE 는 수치여야 한다 (받은 값: $SIGMA_AM_S_OVERRIDE)"; exit 2;; esac
  #  ⚠⚠ 점을 **지우면 안 된다** — `${V//./}` 는 `2.5` 와 `25` 를 똑같이 `25` 로 만든다.
  #    사전등록 격자의 σ_SDCP 가 정확히 `2.5, 25, 250, 2500, 25000` 이라 두 점이 **같은
  #    디렉터리**로 떨어진다 ⇒ 러너가 기존 영수증을 맞다고 보고 팔을 재사용한다.
  #    ⇒ `.` → `p` 로 **무손실** 치환.  (기존 축의 규칙은 안 건드린다 — 이미 돈 팔의
  #    디렉터리 이름이 바뀌면 완주한 산출물을 못 찾는다.)
  AS_TAG="_as${SIGMA_AM_S_OVERRIDE//./p}"; AS_FLAG=" --sigma-am-s $SIGMA_AM_S_OVERRIDE"
fi
SD_SIG_TAG=""; SD_SIG_FLAG=""
if [ -n "${SIGMA_SDCP_OVERRIDE:-}" ]; then
  case "$SIGMA_SDCP_OVERRIDE" in ''|*[!0-9.eE+-]*)
    echo "ABORT — SIGMA_SDCP_OVERRIDE 는 수치여야 한다 (받은 값: $SIGMA_SDCP_OVERRIDE)"; exit 2;; esac
  SD_SIG_TAG="_sd${SIGMA_SDCP_OVERRIDE//./p}"; SD_SIG_FLAG=" --sigma-sdcp $SIGMA_SDCP_OVERRIDE"
fi

#  ★★★ 2026-08-30 (Codex R13 C-7 ⓒ) — **두 이온 σ 를 정식 축으로 올린다.**
#    여태 배선이 없었다: `P2_EXTRA="--sigma-ion-sdcp 0.00062"` 는 허용목록(수치 전용)에서
#    **exit 2** 였다.  그래서 D13 펠릿 보정이 낸 값을 전극에서 시험할 **수단 자체가 없었다.**
#  ⚠ **둘을 함께** 노브로 둔다 (C-7 ⓑ).  SDCP 만 바꾸면 상대비가 안 옮겨간다 —
#    동결값은 `0.62/3.57 = 0.1737` 인데 SE 를 생산 `0.003` 에 두고 SDCP 만 `0.00062` 로
#    하면 `0.2067` 이다.  어느 쪽을 의도했는지 **런이 스스로 선언**해야 한다.
#  ⚠ 기본은 빈 값 = 기존 거동 그대로 (payload 기본값 SE 0.003 · SDCP 0.001).
SION_FLAG=""; SION_TAG=""
if [ -n "${SIGMA_ION_SDCP:-}" ]; then
  case "$SIGMA_ION_SDCP" in ''|*[!0-9.eE+-]*) echo "ABORT — SIGMA_ION_SDCP 는 수치여야 한다 (받은 값: $SIGMA_ION_SDCP)"; exit 2;; esac
  SION_FLAG="$SION_FLAG --sigma-ion-sdcp $SIGMA_ION_SDCP"; SION_TAG="${SION_TAG}_isd${SIGMA_ION_SDCP//./}"
fi
if [ -n "${SIGMA_ION_SE:-}" ]; then
  case "$SIGMA_ION_SE" in ''|*[!0-9.eE+-]*) echo "ABORT — SIGMA_ION_SE 는 수치여야 한다 (받은 값: $SIGMA_ION_SE)"; exit 2;; esac
  SION_FLAG="$SION_FLAG --sigma-ion-se $SIGMA_ION_SE"; SION_TAG="${SION_TAG}_ise${SIGMA_ION_SE//./}"
fi
#  ★★★ 2026-08-31 (Codex R16 P1-5) — **PTFE 이온 차단을 정식 축으로 배선한다.**
#    `run_contract.py` 는 `--step3-ptfe-block-um` 을 이미 규약 축으로 알고 있는데
#    **러너에 env·tag·receipt 배선이 없었다.**  `P2_EXTRA` 로 주면 허용목록(수치 전용)이
#    거부하고, 억지로 우회하면 OUTDIR 이름이 안 갈려 **SKIP 캐시가 옛 팔을 재활용**한다.
#    ⇒ SION 과 같은 모양으로 축을 만든다.  기본 빈 값 = 기존 거동 그대로.
#  ⚠ `PTFE_BLOCK_SCOPE` 는 `se`(기본, 옛 거동 비트 동일) 또는 `ion`(SDCP 도 차단).
#    ⚠⚠ `ion` 은 **전자 no-op 이 아니다** (SDCP σ_e 250 → 차단 셀 0) — 그 팔의 σ_e 를
#    centerline 팔과 나란히 놓지 말 것.  왜 두 규약이 필요한가: `se` 만 쓰면 SBE(PTFE 1.0/
#    SDCP 0) 가 DBE(0.5/0.5) 보다 더 깎이는 방향이 **연산자에 내장**된다 (Codex R16 Q6 반례 2).
PB_FLAG=""; PB_TAG=""
if [ -n "${PTFE_BLOCK_UM:-}" ]; then
  case "$PTFE_BLOCK_UM" in ''|*[!0-9.eE+-]*) echo "ABORT — PTFE_BLOCK_UM 는 수치여야 한다 (받은 값: $PTFE_BLOCK_UM)"; exit 2;; esac
  PB_FLAG="$PB_FLAG --step3-ptfe-block-um $PTFE_BLOCK_UM"; PB_TAG="${PB_TAG}_pb${PTFE_BLOCK_UM//./}"
fi
if [ -n "${PTFE_BLOCK_SCOPE:-}" ]; then
  case "$PTFE_BLOCK_SCOPE" in
    se|ion) ;;
    *) echo "ABORT — PTFE_BLOCK_SCOPE 는 se 또는 ion 이어야 한다 (받은 값: $PTFE_BLOCK_SCOPE)"; exit 2;;
  esac
  #  ⚠ scope 만 주고 두께를 안 주면 **아무 일도 안 일어난다** — 조용한 no-op 을 막는다.
  if [ -z "${PTFE_BLOCK_UM:-}" ]; then
    echo "ABORT — PTFE_BLOCK_SCOPE 를 주려면 PTFE_BLOCK_UM 도 줘야 한다 (두께 0 이면 scope 는 무의미)."
    exit 2
  fi
  PB_FLAG="$PB_FLAG --step3-ptfe-block-scope $PTFE_BLOCK_SCOPE"; PB_TAG="${PB_TAG}_${PTFE_BLOCK_SCOPE}"
fi
#  ⚠ 차단은 **이온 축**이다 — 이온을 안 푸는 LEAN 과 함께 주면 모순이다 (아래 게이트가 잡는다).

#  ⚠ 이온 축을 건드리면서 이온을 안 푸는 것은 **모순**이다 — 조용히 넘기지 않는다.
#  ★ σ-치환 진단 팔 (2026-08-18, CL-43/44 · prereg v3 §4b) — SDCP 가 VGCF 셀에 양보한다.
#    **생산 규약이 아니다.**  디렉터리·태그를 갈라 SKIP 캐시가 생산 팔과 섞이지 않게 한다
#    (판정기 게이트가 잡긴 하지만, 애초에 안 섞이는 것이 낫다 — H4 와 같은 이유).
YV_FLAG=""; YV_TAG=""
if [ "${SDCP_YIELD_VGCF:-0}" = "1" ]; then
  YV_FLAG=" --step3-sdcp-yield-to-vgcf"; YV_TAG="_yvgcf"
  echo "[p2] ★ **진단 팔** — SDCP 가 VGCF 셀에 양보 (σ-치환 채널 OFF).  생산 규약 아님"
fi
# ── ★ GPU 폴백 fail-closed (2026-08-26, kgy 실측 사고) ────────────────────────────
#   `EXPECT_BACKEND=gpu` (기본) 로 봉인하는 런에서 GPU OOM 이 나면 STEP3 는 **조용히
#   CPU 로 내려가** 수 시간을 풀고, 그 결과는 `sr01_stamp_compare --expect-backend` 가
#   **반드시 거부**한다 = 계산을 다 하고 버린다.  실측: vox 0.15 arm 15 에서 1 시간 낭비
#   (다른 프로세스가 GPU 를 물고 있었고, 그것이 끝난 뒤에도 폴백은 되돌릴 수 없다 —
#   backend 는 솔브 진입 시 한 번 정해진다).  ⇒ 기대가 gpu 면 폴백을 **막는다**.
#   ⚠ `EXPECT_BACKEND=cpu` 로 돌리는 런은 영향 없음 (폴백이 정상 경로다).
RQG_FLAG=""
[ "${EXPECT_BACKEND:-gpu}" = "gpu" ] && RQG_FLAG=" --step3-require-gpu"
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
#    예: `P2_EXTRA="--step3-maxiter 200000"`.
#  ★★★ 2026-08-25 (R3-CX-04, Codex 3차) — **주의 문구로는 못 막는다.**  옛 판은
#    "규약을 바꾸는 플래그는 여기로 주지 말 것" 이라고 **적어만** 뒀고, `P2_EXTRA` 가
#    조립 문자열의 **맨 뒤**에 붙어 앞의 선언을 전부 덮을 수 있었다
#    (`--periodic` · `--no-ion` · `--sigma-vgcf` …).  주의는 게이트가 아니다.
#    ⇒ 금지 목록을 **거부**한다 (fail-closed).  진짜로 필요하면 러너에 축을 만든다.
#  ★★★ 2026-08-25 (R4-CX-03, Codex 4차) — **금지 목록(deny) → 허용 목록(allow).**
#    정확 문자열 금지는 argparse **축약**으로 뚫린다 (`--period` 가 `--periodic` 으로
#    받아졌다, Codex 실측).  그리고 목록에 없던 축이 계속 나왔다 —
#    `--show-results` · `--sigma-ion-se` · `--sigma-superp` · `--swcnt-ion-block` ·
#    `--step3-amg` 전부 통과했다.  **없는 것을 다 적는 방식은 원리적으로 진다.**
#    ⇒ 진단용으로 안전하다고 **명시한 것만** 통과시킨다 (solver 물리를 안 바꾸는 축).
#      새 축이 필요하면 여기 적으면서 "왜 물리를 안 바꾸는가" 를 같이 적는다.
_P2_ALLOWED='--step3-maxiter --step3-rtol --gpu-mem --n-vox --void-max'
if [ -n "${P2_EXTRA:-}" ]; then
  for _tok in $P2_EXTRA; do
    case "$_tok" in
      -*)
        _k="${_tok%%=*}"
        case " $_P2_ALLOWED " in
          *" $_k "*) ;;
          *)
            echo "ABORT — P2_EXTRA 의 \`$_k\` 는 허용 목록에 없다."
            echo "  P2_EXTRA 는 조립 문자열 **맨 뒤**라 러너의 \`--expect-physics\` 선언을 덮는다."
            echo "  허용(진단·수치 전용): $_P2_ALLOWED"
            echo "  물리를 바꾸려면 러너에 축을 만들 것 (VOX·SIGMA_PTFE·PTFE_STAMP·LEAN …)."
            exit 2;;
        esac;;
    esac
  done
  #  ★★★ 2026-08-25 (R5-CX-01, Codex 5차) — **위 검사만으로는 뚫린다.**
  #    `for _tok in $P2_EXTRA` 는 한 번만 확장하므로 `--step3-maxiter=$MPM_ATTACK` 이
  #    **리터럴**로 보여 통과한다.  그 문자열은 뒤에서 생성 스크립트에 박히고 그것이
  #    실행될 때 **두 번째로 확장**돼 `--step3-maxiter=1 --show-results` 두 토큰이 된다
  #    (Codex 실측: 금지된 결과-공개 플래그가 실제 payload argv 에 도달했다).
  #  ⇒ **문자 allowlist** 로 막는다.  "나쁜 것을 다 적는" 부정 목록은 원리적으로 진다는
  #    것이 바로 위 주석의 교훈이므로, 여기서도 **허용 문자만** 통과시킨다.
  #    ⚠ `$`·백틱·`;`·`|`·`&`·괄호·따옴표·개행이 전부 여기서 걸린다.
  if printf '%s' "$P2_EXTRA" | LC_ALL=C grep -q '[^A-Za-z0-9._=/ -]'; then
    echo "ABORT — P2_EXTRA 에 허용 밖 문자가 있다 (허용: 영숫자 . _ = / - 공백)."
    echo "  이유: 이 문자열은 생성 스크립트에 박혀 **한 번 더 확장**된다.  \$VAR·명령치환·"
    echo "        구분자를 넣으면 검사를 통과한 뒤 다른 인자가 만들어진다 (R5-CX-01)."
    exit 2
  fi
  if [ "$(printf '%s' "$P2_EXTRA" | wc -l)" -ne 0 ]; then
    echo "ABORT — P2_EXTRA 에 개행이 있다 (토큰 검사를 우회한다)."; exit 2
  fi
fi
#  ★★ R4-CX-03 — `${MPM_PERIODIC_SIGMA:+--periodic}` 은 **값이 `0` 이어도** 켠다
#    (`:+` 는 nonempty 를 본다).  킷 생성기는 `= "1"` 로 비교하므로 두 곳이 갈린다.
#    ⇒ 여기서도 `= 1` 만 켠다.  그리고 `periodic_xy` 를 선언 목록에 넣는다 (아래 XP).
if [ -n "${MPM_PERIODIC_SIGMA:-}" ] && [ "${MPM_PERIODIC_SIGMA}" != "1" ] \
   && [ "${MPM_PERIODIC_SIGMA}" != "0" ]; then
  echo "ABORT — MPM_PERIODIC_SIGMA=${MPM_PERIODIC_SIGMA} 는 0 또는 1 이어야 한다"
  exit 2
fi
PERIODIC_ON=0; [ "${MPM_PERIODIC_SIGMA:-0}" = "1" ] && PERIODIC_ON=1
#  ★★★ 2026-08-30 — **LEAN 값 검증**.  여태 없었다: `LEAN=9` 를 주면 `LEAN_FLAGS` 도
#    `LEAN_TAG` 도 빈 값이라 **LEAN 미지정과 같은 OUTDIR** 을 쓰면서 전체 파이프라인을 돈다
#    = 요청한 것과 도는 것이 다른데 이름이 같다 (FIBRE_STAMP 가 이미 막은 것과 같은 부류).
case "${LEAN:-0}" in
  0|1|2|3|4) ;;
  *) echo "ABORT — LEAN 은 0(미지정)·1·2·3·4 중 하나여야 한다 (받은 값: ${LEAN})"; exit 2;;
esac
LEAN_FLAGS=""
[ "${LEAN:-0}" = "1" ] && LEAN_FLAGS=" --no-step4 --no-thermal --no-trackb --no-field"
#     ★ 2026-08-18 2차: `--no-collector` 도 넣는다.  1차 LEAN=2 시도가 **집전체 기하 솔브**
#       에서 또 죽었다 (p2_DBE_sph_a3: 전자 솔브 0.06071 수렴 후 사망).  그 2회 솔브는
#       shift 팔에서 `_bot_mask` 가 origin 을 안 더해 **어차피 무효**다 (위 주석 참조).
[ "${LEAN:-0}" = "2" ] && { LEAN_FLAGS=" --no-step4 --no-thermal --no-trackb --no-field --no-ion --no-pore --no-collector"; \
  echo "[p2] ★ LEAN=2 (σ_e 전용) — 이온·pore-τ·집전체기하 를 전부 끈다 (팔당 솔브 3회 → 1회)"; }
#  ★★ LEAN=3 (2026-08-29) — **σ_e + σ_ion**.  LEAN=2 에서 `--no-ion` 하나만 뺀다.
#    왜 축을 새로 만드나: `P2_EXTRA="--step3-ion"` 은 허용목록(수치 전용)에 없어 거부된다
#    (`:174` 게이트).  물리를 바꾸는 것은 **러너 노브여야** 매니페스트·OUTDIR·영수증에
#    같이 기록된다 — 그 게이트가 없었으면 "요청한 것 ≠ 쓰인 것" 이 또 났다.
#    ⚠ pore-τ·집전체는 계속 끈다 (DR3-07/08 로 이 침대에서 pore-τ 가 무의미하고, 집전체
#      기하는 shift 팔에서 `_bot_mask` 가 origin 을 안 더해 어차피 무효다).
#    비용: 팔당 솔브 1 → 2회.
[ "${LEAN:-0}" = "3" ] && { LEAN_FLAGS=" --no-step4 --no-thermal --no-trackb --no-field --no-pore --no-collector"; \
  echo "[p2] ★ LEAN=3 (σ_e + σ_ion) — pore-τ·집전체기하만 끈다 (팔당 솔브 2회)"; }
#  ★★ LEAN=4 (2026-08-30) — **σ_e + σ_ion + 필드**.  LEAN=3 에서 `--no-field` 만 뺀다.
#    왜 필요한가: 3D 뷰어 그림(Figure 4a)은 **필드 점군**으로 그리는데, LEAN 1·2·3 이
#    **전부** `--no-field` 를 붙인다 ⇒ 필드를 남기는 레벨이 하나도 없었다.  그렇다고
#    `LEAN` 을 안 주면 **pore-τ 가 required** 가 되고(`run_contract.required_components()`),
#    이 침대는 pore-τ 가 `None` 을 내서 `STEP3_EVIDENCE` 로 **payload 전체가 게시 거부**된다
#    (2026-08-27 kit_SBE 실측: `EVID|pore|result| tau=None` → `mpm_payload.json.failed`).
#    DR3-07/08 이 그 이유를 이미 적었다 — 격자를 조일수록 `closed-from-top` 28.5 → 99.2 %.
#    ⇒ "필드는 남기고 pore 는 끄는" 조합이 **원리적으로 없었다**.  이것이 그 조합이다.
#    ⚠ `P2_EXTRA="--no-pore"` 로는 못 한다 — 허용목록(`_P2_ALLOWED`)이 수치 전용이라 거부된다.
#      물리를 바꾸는 축은 러너 노브여야 매니페스트·OUTDIR·영수증에 같이 기록된다.
#    ⚠ `--no-step4` 는 켠 채로 둔다 (STEP4 가 이 침대의 OOM 원인, prereg v3 STEP 4).
#      뷰어가 step4 격자를 요구하면 그때 LEAN=5 로 따로 만든다 — 지금 짐작으로 켜지 않는다.
[ "${LEAN:-0}" = "4" ] && { LEAN_FLAGS=" --no-step4 --no-thermal --no-trackb --no-pore --no-collector"; \
  echo "[p2] ★ LEAN=4 (σ_e + σ_ion + 필드) — pore-τ·집전체·STEP4 만 끈다 (뷰어 그림용)"; }
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
#  ⚠ 새 접미사 — LEAN=2 산출물과 **섞이면 안 된다** (이온 유무가 다른 런이다)
[ "${LEAN:-0}" = "3" ] && LEAN_TAG="_lean3"
[ "${LEAN:-0}" = "4" ] && LEAN_TAG="_lean4"   # ⚠ 필드 유무가 달라 lean3 과 섞이면 안 된다

#  ⚠⚠ **이 가드는 `LEAN_FLAGS` 가 조립된 *뒤*에 있어야 한다** (R14 D-1 수정 중 실사고):
#    초판을 파일 앞쪽(SION 파싱 직후)에 뒀는데 거기서는 `LEAN_FLAGS` 가 아직 빈 문자열이라
#    **조용히 아무것도 안 막았다** — 과잉차단보다 나쁘다 (있는 줄 알고 믿게 된다).
#    레벨 번호를 다시 적지 않고 **조립된 flags** 를 보는 이유도 같다: 레벨이 늘면 갈라진다.
if [ -n "$SION_FLAG$PB_FLAG" ] && case "$LEAN_FLAGS" in *--no-ion*) true;; *) false;; esac; then
  echo "ABORT — 이온 축(SIGMA_ION_* 또는 PTFE_BLOCK_*)을 줬는데 LEAN=${LEAN:-0} 의 조립 flags 에 --no-ion 이 있다."
  echo "  이온 σ 를 바꾸면서 이온을 안 푸는 런은 아무것도 재지 않는다.  LEAN=3 또는 4 로."
  echo "  (조립 결과: ${LEAN_FLAGS})"
  exit 2
fi
#  ★★★ 2026-08-25 (R5-CX-03, Codex 5차) — **런 영수증**.  러너가 무엇으로 돌라고 했는지
#    한 곳에 적고, cache/fresh/final 이 전부 이 값을 요구한다.
#    ⚠ 왜: Codex 실측에서 HEAD·vox·구경·code SHA·input digest 가 전부 달라도 캐시된 팔이
#      SKIP 으로 통과하고 final 이 `h0` 였다.  `check_arm` 은 stamp/backend 만 받았고
#      final 은 digest 의 **존재와 팔 사이 일관성**만 봤다 — 팔들이 **같이 낡았으면**
#      그 검사는 통과한다 (H4 와 같은 부류).  **일치는 옳음이 아니다.**
#  ⚠ `SIGMA` 는 여기 없다 — 그것은 **팔마다** 계산된다 (직경-보존 재척도 또는 override).
#    러너가 **정한 것만** 선언한다.  σ_VGCF 축은 `--expect-physics` 가 팔 단위로 봉인하고
#    payload 가 불일치면 exit 4 를 낸다 (다른 겹).  선언하지 않은 축은 `receipt_match` 가
#    요구하지 않는다 — 모르는 것을 아는 척하지 않는다.
_RCPT_JSON="$(python3 - "$SCR" "$VOX" "$BRIDGE_UM" "$FIBRE_STAMP" "${SDCP_SPHERE_D:-}" \
                  "${SDCP_YIELD_VGCF:-0}" "${PTFE_STAMP:-off}" "${SIGMA_PTFE:-}" \
                  "${SIGMA_VGCF_OVERRIDE:-}" \
                  "$PERIODIC_ON" "$ARMS" "${EXPECT_BACKEND:-gpu}" "${SDCP_BRIDGE:-}" \
                  "${LEAN:-0}" "${SIGMA_ION_SDCP:-}" "${SIGMA_ION_SE:-}" \
                  "${PTFE_BLOCK_UM:-}" "${PTFE_BLOCK_SCOPE:-}" \
                  "${SIGMA_AM_S_OVERRIDE:-}" "${SIGMA_SDCP_OVERRIDE:-}" <<'PYRCPT'
import json, os, sys
sys.path.insert(0, sys.argv[1])
import run_contract as RC
_scr, _vox, _br, _fs, _sd, _yv, _ps, _pt, _sg, _per, _arms, _bk = sys.argv[1:13]
_sbrg = sys.argv[13] if len(sys.argv) > 13 else ''
_lean = sys.argv[14] if len(sys.argv) > 14 else '0'
_isd  = sys.argv[15] if len(sys.argv) > 15 else ''
_ise  = sys.argv[16] if len(sys.argv) > 16 else ''
_pbu  = sys.argv[17] if len(sys.argv) > 17 else ''
_pbs  = sys.argv[18] if len(sys.argv) > 18 else ''
_ams  = sys.argv[19] if len(sys.argv) > 19 else ''
_sdsg = sys.argv[20] if len(sys.argv) > 20 else ''
vox = float(_vox)
rec = {'vox_um': vox, 'bridge_um': float(_br), 'fibre_stamp': _fs,
       'sdcp_stamp': ('sphere' if _sd else 'point'),
       'sdcp_sphere_d_um': (float(_sd) if _sd else 0.0),
       'sdcp_yield_to_vgcf': (_yv == '1'), 'ptfe_stamp': _ps,
       'periodic_xy': (_per == '1'),
       'arms': int(_arms), 'expect_backend': _bk,
       'origins': [list(o) for o in RC.expected_origins_for(vox)]}
if _sbrg:
    rec['sdcp_bridge_um'] = float(_sbrg)   # 판별 축 — 러너가 정한 것만 선언
#  ★ 두 이온 σ — **러너가 정했을 때만** 선언한다 (RECEIPT_AXES 규약).  기본값으로 돌면
#    선언하지 않아 기존 팔이 그대로 산다.
if _isd:
    rec['sigma_ion_sdcp_S_cm'] = float(_isd)
if _ise:
    #  ★★★ 2026-08-30 (Codex R14 D-1 온도 계약) — **기준값을 적용값 키에 쓰지 않는다.**
    #    payload 는 `--sigma-ion-se` 를 **T_ref 선언값**으로 받아 Arrhenius 로 보정한 뒤
    #    매니페스트에 `sigma_ion_se_S_cm`(적용 후) 와 `sigma_ion_se_ref_S_cm`(기준) 을
    #    **나눠** 적는다 (mpm_webapp_payload.py:2625-2626).  러너가 준 것은 **기준값**이다.
    #    옛 판은 그것을 적용값 키에 써서, 25 °C 가 아니면 대조가 거짓 불일치를 냈다
    #    (60 °C: 0.003 → 0.0143553 ⇒ SDCP/SE 비 0.1737 → 0.04319).
    rec['sigma_ion_se_ref_S_cm'] = float(_ise)
#  ★ 2026-08-31 (Codex R16 P1-5) — PTFE 차단 축을 영수증에 싣는다.
#    `ptfe_block_um` 은 규약 축이고 `ptfe_block_scope` 는 `record` 축이다 (p2 보존 —
#    `run_contract.CLI_ACCOUNTING` 의 주석 참조).  둘 다 `RECEIPT_AXES` 에 있어
#    코호트 안에서 값이 갈리면 거부된다.
if _pbu:
    rec['ptfe_block_um'] = float(_pbu)
if _pbs:
    rec['ptfe_block_scope'] = str(_pbs)
#  ★★★ 2026-08-30 (코드리뷰 지적 1) — **LEAN=4 일 때만** 필드 유무를 선언한다.
#    `field_requested` 는 `RECEIPT_AXES_NODIGEST` 라 **digest 를 안 바꾼다** (기존 팔 전부 보존).
#    ⚠ 왜 LEAN=4 에만: 이 레벨은 오늘 만든 것이라 **혼동될 기존 팔이 없다** ⇒ 거짓 경보 0.
#      LEAN 미지정(전체 파이프라인)도 필드를 쓰지만, 거기서 선언하면 이 키를 모르는
#      **오늘 이전 팔이 전부 `missing` = HOLD** 가 된다 (돌고 있는 진단 런 포함).
#    ⚠ 남는 구멍: LEAN 미지정 팔은 여전히 매니페스트로 필드 유무를 증명하지 못한다.
#      그 팔을 쓰려면 JSON 안의 필드 배열을 직접 확인해야 한다 (자동 검사 밖).
if _lean == '4':
    rec['field_requested'] = True
if _pt:
    rec['sigma_ptfe_S_cm'] = float(_pt)
if _sg:
    rec['sigma_vgcf_S_cm'] = float(_sg)      # 명시 override 일 때만 (러너가 정한 것)
#  ★★ 2026-09-02 — closure 스윕의 두 대비 축.  **러너가 정했을 때만** 선언한다
#    (RECEIPT_AXES 규약: 기본값으로 돈 기존 팔은 그대로 산다).
#  ⚠ 둘은 `RECEIPT_AXES_NODIGEST` 다 — digest 에 넣으면 `rec.get(k)=None` 이 해시 본문에
#    들어가 **기존 digest 가 전부 바뀌고** 커밋된 코호트 디렉터리 이름까지 어긋난다.
#    디렉터리를 가르는 일은 위의 무손실 태그(`_as`·`_sd`)가 하고, 여기서는 **팔마다
#    매니페스트와 대조**해 '러너가 의도한 σ 로 돌았는가' 를 증명한다.
if _ams:
    rec['sigma_am_s_S_cm'] = float(_ams)
if _sdsg:
    rec['sigma_sdcp_S_cm'] = float(_sdsg)
#  ★ code SHA 는 payload 와 **같은 함수**로 (사본을 두면 갈라진다)
try:
    import mpm_webapp_payload as _P
    rec['code_sha'] = _P._code_sha(_scr)
except Exception:
    pass
rec['receipt_digest'] = RC.receipt_digest(rec)
print(json.dumps(rec, ensure_ascii=False, sort_keys=True))
PYRCPT
)" || { echo "[p2] ABORT — 런 영수증을 못 만들었다"; exit 2; }
_RCPT_TAG="_r$(printf '%s' "$_RCPT_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["receipt_digest"])')"
OUTDIR="${OUTDIR:-$PWD/prereg_v2_vox${VOX/./}${SD_TAG}${BR_TAG}${SG_TAG}${AS_TAG}${SD_SIG_TAG}${YV_TAG}${PT_TAG}${PS_TAG}${SBRG_TAG}${FS_TAG}${SION_TAG}${PB_TAG}${AR_TAG}${LEAN_TAG}${_RCPT_TAG}}"
#  ★★★ R3-CX-09 — 진단 런(ARMS≠8)은 **사용자가 준 OUTDIR 에도** 접미사를 강제한다.
#    안 그러면 `ARMS=2 OUTDIR=<생산경로>` 로 2팔 산출물이 8팔 디렉터리에 섞인다.
#  ★ 2026-09-01 — 검사를 **끝자리**에서 **포함**으로 바꾼다.  기본 OUTDIR 은 이미
#    `${AR_TAG}` 로 팔 수를 담는데 그 뒤에 `${LEAN_TAG}${_RCPT_TAG}` 가 붙으므로 끝자리
#    검사가 "없다" 로 읽고 **또** 붙였다 (실측: `…_arm1_lean2_r5ef6da47ca4e_arm1`).
#    디렉터리 이름은 이 리포에서 규약의 일부라(판정기가 태그로 팔을 짝짓는다) 중복은
#    조용한 오독의 씨앗이다.
#  ⚠ **"사용자가 준 경우만" 으로 좁히지 말 것** — 처음에 그렇게 고쳤다가 L-5a 가 잡았다.
#    그 시험이 지키는 것은 **이중 방어**다: 조립에서 `${AR_TAG}` 가 지워져도 이 줄이
#    여전히 진단 산출물을 격리해야 한다.  포함 검사는 두 요구를 동시에 만족한다.
if [ "$ARMS" -ne 8 ] && [ "${OUTDIR#*_arm$ARMS}" = "$OUTDIR" ]; then
  OUTDIR="${OUTDIR}_arm${ARMS}"
  echo "[p2] ⚠ 진단 런($ARMS 팔) — OUTDIR 에 강제 접미사: $OUTDIR"
fi
#  ★★★ 2026-08-25 (R4-CX-08, Codex 4차) — **접미사는 문자열이다.**  `user_arm2` 를
#    production 디렉터리로 가리키는 junction/symlink 를 만들면 문자열 검사는 통과하고
#    **resolved path 는 production** 이 된다 (Codex 실측).  ⇒ 실경로로 충돌을 본다.
if [ "$ARMS" -ne 8 ]; then
  _PROD="$PWD/prereg_v2_vox${VOX/./}${SD_TAG}${BR_TAG}${SG_TAG}${AS_TAG}${SD_SIG_TAG}${YV_TAG}${PT_TAG}${PS_TAG}${SBRG_TAG}${FS_TAG}${SION_TAG}${PB_TAG}${LEAN_TAG}"
  mkdir -p "$OUTDIR" 2>/dev/null || true
  _R_OUT="$(cd "$OUTDIR" 2>/dev/null && pwd -P || echo "$OUTDIR")"
  _R_PROD="$([ -d "$_PROD" ] && cd "$_PROD" && pwd -P || echo "$_PROD")"
  if [ "$_R_OUT" = "$_R_PROD" ]; then
    echo "ABORT — 진단 런($ARMS 팔)의 실경로가 **생산 디렉터리와 같다**."
    echo "  OUTDIR   = $OUTDIR"
    echo "  실경로   = $_R_OUT"
    echo "  생산경로 = $_R_PROD"
    echo "  (junction/symlink 로 이름만 다르게 한 경우다 — 접미사는 문자열이지 격리가 아니다)"
    exit 2
  fi
fi
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
#  ★★★ R5-CX-03 — 영수증을 **런 디렉터리에 남긴다**.  cache/fresh 검사가 이 파일을 읽어
#    팔의 매니페스트와 축별로 대조한다.  ⚠ 이미 있고 **다르면** 중단 — 같은 디렉터리에
#    다른 설정의 팔이 섞이는 것이 바로 H4·R5-CX-03 이 잡은 그 사고다.
if [ -s "$OUTDIR/run_receipt.json" ]; then
  if ! printf '%s' "$_RCPT_JSON" | diff -q - "$OUTDIR/run_receipt.json" >/dev/null 2>&1; then
    echo "[p2] ABORT — 이 디렉터리의 영수증이 지금 설정과 다르다: $OUTDIR/run_receipt.json"
    echo "     같은 디렉터리에 다른 설정의 팔을 섞을 수 없다.  OUTDIR 을 갈라 쓸 것."
    diff <(printf '%s' "$_RCPT_JSON") "$OUTDIR/run_receipt.json" | sed 's/^/     /' | head -12
    exit 2
  fi
else
  printf '%s' "$_RCPT_JSON" > "$OUTDIR/run_receipt.json"
  echo "[p2] 런 영수증 → $OUTDIR/run_receipt.json"
fi


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
         --receipt "$OUTDIR/run_receipt.json" \
         --expect-backend "${EXPECT_BACKEND:-gpu}" >/dev/null 2>&1; then
      echo "[p2] SKIP (완전) $TAG"; return 0
    fi
    echo "[p2] ⚠ 기존 $TAG 이 불완전 — 다시 돈다:"
    python3 "$SCR/sr01_stamp_compare.py" --check-arm "$OUT" --stamp "$FIBRE_STAMP" \
      --receipt "$OUTDIR/run_receipt.json" \
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
  #  ★★★ 2026-08-25 (Codex 재리뷰 조건 4) — **기대값을 러너 자신의 설정에서 만든다.**
  #    `EXPECT_PROTOCOL` 의 표준 용법("첫 팔이 찍은 id 를 나머지에 넘긴다")은 **첫 팔을
  #    진리로 삼는다** — 첫 팔이 조용히 잘못된 규약으로 돌면 나머지 일곱이 그것에
  #    일치해 전부 통과한다.  팔간 일치는 옳음이 아니다.
  #    ⇒ 러너가 자기가 설정한 축을 **선언**하고 payload 가 적용값과 필드별로 대조한다.
  #      다르면 exit 4.  해시가 아니라 필드라서 **어느 축이 갈렸는지**까지 말해 준다.
  #    ⚠ 여기 적는 것은 러너가 **실제로 인자로 넘긴 축**뿐이다 (킷이 정하는 σ_AM·온도 등은
  #      러너가 모르므로 선언하지 않는다 — 모르는 것을 선언하면 그것이 새 거짓 보증이다).
  local XP="vox_um=$VOX,bridge_um=$BRIDGE_UM,sigma_vgcf_S_cm=$SIGMA"
  XP="$XP,fibre_stamp=$FIBRE_STAMP"
  XP="$XP,sdcp_stamp=$([ -n "$SD_FLAG" ] && echo sphere || echo point)"
  XP="$XP,sdcp_yield_to_vgcf=$([ -n "$YV_FLAG" ] && echo True || echo False)"
  #  ★ R4-CX-03 — `periodic_xy` 가 선언 목록에 **없었다** (규약 축인데).
  XP="$XP,periodic_xy=$([ "$PERIODIC_ON" = 1 ] && echo True || echo False)"
  [ -n "$PS_FLAG" ] && XP="$XP,ptfe_stamp=$PTFE_STAMP"
  [ -n "$PT_FLAG" ] && XP="$XP,sigma_ptfe_S_cm=$SIGMA_PTFE"
  local XP_FLAG=" --expect-physics $XP"
  local SHF="$RUN/${TAG}.$$.sh"
  ( cd "$RUN" && P2_SCR="$SCR" python3 "$SCR/sr01_stamp_compare.py" \
      --extract-payload "$KIT/run_mpm.sh" --stamp "$FIBRE_STAMP" \
      --extra-flags "--sigma-vgcf $SIGMA${AS_FLAG}${SD_SIG_FLAG} --step3-vox $VOX --step3-bridge-um $BRIDGE_UM --step3-origin-shift $SH$SD_FLAG$YV_FLAG$PT_FLAG$PS_FLAG$SBRG_FLAG$RQG_FLAG$EP_FLAG$XP_FLAG$FS_FLAG$SION_FLAG$PB_FLAG$LEAN_FLAGS${P2_EXTRA:+ $P2_EXTRA}" \
      --tag "$TAG" --out-name "$(basename "$OUT")" > "$SHF.body" ) || return 1
  { echo 'set -uo pipefail'; echo "KIT=\"$KIT\""; echo "SCR=\"$SCR\"";
    #  ★ R4-CX-03 — `:+` 는 값 `0` 도 nonempty 라 켰다.  `= 1` 만 켠다.
    echo "PSIG=($([ "$PERIODIC_ON" = 1 ] && echo --periodic))"; cat "$SHF.body"; } > "$SHF.part" \
    && mv -f "$SHF.part" "$SHF"
  rm -f "$SHF.body"
  # ★★ 2026-08-19 fail-closed — **생성된 스크립트 자체가 온전한가**.
  #   실사고: `--out p2_SBE_sph_a0.json` 토큰이 줄바꿈으로 **한가운데서 잘렸다**
  #   (line 8 이 `--out p` 로 끝나고 line 9 가 `2_SBE_sph_a0.json`).  bash 문법으로는
  #   유효해서(두 개의 명령) `bash -n` 도 통과하고, payload 는 **정상 완주한 뒤** 다음 줄에서
  #   `command not found` 로 죽는다 = 40 분을 버리고 팔이 실패한다.
  #   ⇒ 돌기 **전에** --out 토큰이 한 줄에 붙어 있는지 본다.  잘린 파일은 지우지 않고 남긴다.
  #  ★★★ 2026-08-25 (R5-CX-01, 2겹) — **생성된 실물에 확장되지 않은 변수가 남아 있나.**
  #    위 문자 검사는 `P2_EXTRA` 경로를 막지만, 다른 경로로 `$` 가 들어오면 실행 시점에
  #    새 인자가 만들어진다.  ⇒ **만들어진 명령 자체**를 보고, 러너가 스스로 넣은 셋
  #    (`$KIT` · `$SCR` · `${PSIG[@]}`) 밖의 변수 참조가 있으면 돌기 전에 선다.
  #    (검사 대상은 "무엇을 줬나" 가 아니라 "무엇이 실행되나" 다 — 이 리포의 반복 교훈.)
  _STRAY="$(grep -o -- '\$[A-Za-z_{][A-Za-z0-9_]*' "$SHF" \
            | grep -vE '^\$(KIT|SCR|\{PSIG)' | sort -u || true)"
  if [ -n "$_STRAY" ]; then
    echo "[p2] ABORT — 생성된 $TAG.sh 에 확장 안 된 변수 참조가 남아 있다:"
    printf '     %s\n' $_STRAY
    echo "     실행 시점에 확장되면 검사를 지난 뒤 **다른 인자**가 만들어진다 (R5-CX-01)."
    echo "     파일을 남겨 둔다: $SHF"
    return 1
  fi
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
       --receipt "$OUTDIR/run_receipt.json" \
       --expect-backend "${EXPECT_BACKEND:-gpu}" >/dev/null 2>&1; then
    echo "[p2] ABORT — 갓 만든 $TAG 이 불완전하다.  **옮기지 않는다** (캐시 오염 방지):"
    python3 "$SCR/sr01_stamp_compare.py" --check-arm "$FRESH" --stamp "$FIBRE_STAMP" \
      --receipt "$OUTDIR/run_receipt.json" \
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
#  ★★ 2026-08-24 (CDXR2-5) — `--collect-only` 는 **항상 exit 0** 이라 팔이 모자라도·
#    미수렴이어도·고정인자가 어긋나도 러너가 초록으로 끝났다.  그렇다고 러너가 판정을
#    돌리면 이 파일 헤더의 규약("결과를 보고 창을 옮길 수 없게")이 깨진다.
#    ⇒ **봉인과 판정을 가른다**: 봉인 = 데이터가 쓸 만한가, 판정 = 그것이 뭐라고 말하는가.
#      `--seal-only` 는 h0/h1 과 비를 **출력하지 않으므로** 사전등록이 안 깨진다.
#  ⚠ 상수 8 로 건다 ($ARMS 가 아니다 — 그것이 CDXR3-7 의 자기참조였다).
#  ★★★ 2026-08-25 (Codex 재리뷰 조건 1) — **봉인이 먼저다.**  옛 판은 바로 위에서
#    `--collect-only` 를 돌려 **16 팔의 σ_e 원값 표**를 찍은 **뒤에** 봉인을 걸었다.
#    그러면 운영자가 결과를 다 보고 나서 봉인을 통과시킬지 결정할 수 있다 = 봉인이
#    눈먼 것이 아니다 (사전등록의 요점이 정확히 그것이다).
#    ⇒ 봉인을 **먼저** 돌리고, 원값 덤프는
#       · 봉인 통과 → 찍지 않는다 (필요하면 운영자가 명령을 직접 친다)
#       · 봉인 실패 → 찍는다 (데이터는 이미 기각됐으므로 창을 옮길 여지가 없고,
#                             진단에는 원값이 필요하다)
if [ "$ARMS" -eq "$PREREG_ARMS" ]; then
  echo "[p2] 계약 봉인 — 데이터가 쓸 만한가 (판정 아님, 원값은 아직 안 본다)"
  #  ★★ 2026-08-25 (R3-CX-04) — 생산 봉인은 **입력 digest·code SHA** 를 요구한다.
  #    옛 판은 안 넘겨서, 같은 침대라는 증거도 재현 가능한 코드라는 증거도 없이 통과했다.
  #  ⚠ `--require-ionic` 은 **넘기지 않는다** — LEAN=2 는 σ_e 전용이고 이온을 안 푼다.
  #    이온축이 결론인 트랙은 LEAN 을 끄고 그 옵션을 켠 채로 따로 봉인한다.
  #  ★ LEAN=3 (2026-08-29) 은 이온을 **푼다**.  그래도 여기서 `--require-ionic` 을 자동으로
  #    켜지 않는다 — 이 봉인은 σ_e 축의 계약이고, 이온이 결론인 트랙은 여전히 그 옵션을
  #    **명시적으로** 붙여 따로 봉인해야 한다 (자동으로 켜면 어느 축이 결론인지가 흐려진다).
  #  ★★★ 2026-08-30 (Codex R13 C-2) — **LEAN=3/4 는 이온 증거를 요구한다.**
  #    위 문단은 "어느 축이 결론인지 흐려진다" 며 자동 부착을 거부했는데, 그 논리는
  #    LEAN=2(σ_e 전용)에서만 맞다.  LEAN=3/4 는 **이온을 풀려고 켠 모드**이고, 지금
  #    영수증은 이온 계획을 선언하지 않는다 ⇒ producer 가 `component_plan.ionic=False`
  #    로 자기신고하면 `required_components()` 가 그것을 정본으로 받아 이온을 요구하지
  #    않는다 (Codex 실측: `--no-ion` 이 최종 argv 에 남아도 `check_arm = None`).
  #    ⇒ 그 모드에서는 봉인이 **양의 σ_ion 존재**를 직접 요구한다.
  _RQI=""; case "${LEAN:-0}" in 3|4) _RQI="--require-ionic"; \
    echo "[p2] ★ LEAN=${LEAN} — 봉인에 --require-ionic 부착 (이온이 이 모드의 존재 이유다)";; esac
  if ! python3 "$SCR/sdcp_gain_verdict.py" --dir "$OUTDIR" --seal-only \
       --require-arms "$PREREG_ARMS" --require-digest $_RQI; then
    echo "[p2] ✗ 계약 봉인이 깨졌다 — 위 근거를 고치고 다시 돌 것"
    #  ★★★ 2026-08-25 (R3-CX-02, Codex 3차) — **실패해도 원값을 자동으로 찍지 않는다.**
    #    옛 판은 여기서 `--collect-only` 를 돌렸다.  "이미 기각됐으니 안전" 이라고 봤지만
    #    Codex 가 반례를 냈다 — **metadata 를 일부러 깨뜨려 봉인을 실패시키고 raw table 을
    #    보는 경로**가 열린다.  그리고 그 디렉터리는 고쳐서 다시 봉인할 수 있으므로,
    #    "기각됐다" 가 "다시 못 쓴다" 를 뜻하지 않는다.
    #    ⇒ 변경 불가능한 **기각 영수증**을 남기고, 원값을 보려면 사람이 명시로 친다.
    _RCPT="$OUTDIR/.rejected_$(date -u +%Y%m%dT%H%M%SZ)"
    { echo "rejected_utc=$(date -u +%FT%TZ)"; echo "arms=$ARMS"; echo "outdir=$OUTDIR";
      echo "code_sha=$(git -C "$SCR/.." rev-parse --short=8 HEAD 2>/dev/null || echo unknown)";
      echo "reason=seal_broken"; } > "$_RCPT"
    chmod 444 "$_RCPT" 2>/dev/null || true
    echo "[p2] 기각 영수증: $_RCPT  (이 디렉터리는 '한 번 기각됨' 으로 기록됐다)"
    echo "     원값이 필요하면 **명시로** 칠 것 — 자동으로 찍지 않는다:"
    echo "       python3 $SCR/sdcp_gain_verdict.py --dir \"$OUTDIR\" --collect-only"
    exit 1
  fi
  echo "[p2] ✓ 계약 봉인 통과 ($PREREG_ARMS 팔).  판정은 prereg §5 순서로 **따로** 돌 것"
  echo "     원값을 보려면:  python3 $SCR/sdcp_gain_verdict.py --dir \"$OUTDIR\" --collect-only"
else
  #  진단 런은 애초에 "판정하지 말 것" 이므로 원값을 봐도 사전등록이 안 깨진다.
  python3 "$SCR/sdcp_gain_verdict.py" --dir "$OUTDIR" --collect-only || true
  echo "[p2] ⚠ **진단 런 ($ARMS 팔) — 생산 봉인 아님.**  이 산출물로 판정하지 말 것."
  echo "     사전등록은 $PREREG_ARMS 팔이다 (prereg §4).  OUTDIR: $OUTDIR"
fi
