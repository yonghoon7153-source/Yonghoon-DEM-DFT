#!/usr/bin/env bash
# V100 환경 셋업 — 러너들이 전제하는 레이아웃을 한 번에 재건한다.
#
# 레이아웃 (run_se_curve_batch.sh · run_wallp_multiP.sh 의 REPO/DATA 기본값):
#   /home/ubuntu/dem-stoic              ← 코드 (claude/stoic-knuth-NObVQ)
#   /home/ubuntu/Yonghoon-DEM-DFT/venv  ← numpy+taichi venv
#   /home/ubuntu/Yonghoon-DEM-DFT/se_curve/<kit>/  ← 킷 스캐폴드 (보존본에서 복원)
#   /home/ubuntu/Yonghoon-DEM-DFT/se_curve/*.json  ← 지표 보존본 68개
#   $REPO/venv → $DATA/venv 심링크 (러너 프리플라이트가 첫 순위로 찾는 경로)
#   ~/.bashrc 에 alias dem (지난 머신 규약)
#
# 사용 (fresh 머신):
#   git clone --branch claude/stoic-knuth-NObVQ \
#       https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT.git ~/dem-stoic
#   bash ~/dem-stoic/scripts/setup_v100.sh
#
# 이미 있던 볼륨이 복구된 경우에도 안전하다 — 각 단계가 멱등이라 있으면 건너뛰거나 갱신만 한다.
set -uo pipefail
REPO="${REPO:-$HOME/dem-stoic}"
DATA="${DATA:-$HOME/Yonghoon-DEM-DFT}"
BRANCH=claude/stoic-knuth-NObVQ
fail() { echo "★★ ABORT: $*" >&2; exit 1; }

echo "═══ ① GPU 확인 ═══"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader 2>/dev/null \
  || fail "nvidia-smi 실패 — GPU 드라이버부터"

echo "═══ ② 코드 ($REPO @ $BRANCH) ═══"
if [ -d "$REPO/.git" ]; then
  git -C "$REPO" fetch origin "$BRANCH" || fail "fetch 실패 (인증?)"
  git -C "$REPO" checkout "$BRANCH" 2>/dev/null || git -C "$REPO" checkout -b "$BRANCH" "origin/$BRANCH"
  git -C "$REPO" merge --ff-only "origin/$BRANCH" || fail "ff 불가 — 로컬 커밋 있음, 수동 확인"
else
  git clone --branch "$BRANCH" \
    https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT.git "$REPO" || fail "clone 실패 (인증?)"
fi
echo "  HEAD: $(git -C "$REPO" log -1 --format='%h %s' | head -c 80)"

echo "═══ ③ venv ($DATA/venv) ═══"
mkdir -p "$DATA"
if [ ! -f "$DATA/venv/bin/activate" ]; then
  python3 -m venv "$DATA/venv" 2>/dev/null || {
    echo "  python3-venv 설치 필요 → sudo apt-get 시도"
    sudo apt-get update -qq && sudo apt-get install -y -qq python3-venv python3-pip
    python3 -m venv "$DATA/venv" || fail "venv 생성 실패"
  }
fi
# shellcheck disable=SC1091
. "$DATA/venv/bin/activate"
python3 -c "import numpy, taichi" 2>/dev/null || {
  pip install -q -U pip
  pip install -q numpy taichi || fail "pip install 실패"
}
ln -sfn "$DATA/venv" "$REPO/venv"                       # 러너 프리플라이트 1순위 경로
echo "  $(python3 -c "import numpy, taichi; print('numpy', numpy.__version__, '· taichi', taichi.__version__)")"

echo "═══ ④ 킷 스캐폴드 + 지표 보존본 복원 → $DATA/se_curve ═══"
# 러너는 킷을 \$DATA/<kit> 또는 \$DATA/se_curve/<kit> 에서 찾는다 — 후자로 통일.
python3 "$REPO/scripts/unpack_kit_scaffolds.py" \
  --archive "$REPO/docs/data/kit_ps_scaffolds" \
  --metrics "$REPO/docs/data/se_curve_metrics" \
  --out "$DATA/se_curve" || fail "unpack 실패"

echo "═══ ⑤ alias dem (~/.bashrc, 멱등) ═══"
LINE="alias dem='cd $REPO && . $DATA/venv/bin/activate'"
touch ~/.bashrc
sed -i "/^alias dem=/d" ~/.bashrc 2>/dev/null
# ★ 앞에 개행을 반드시 넣는다.  ~/.bashrc 의 마지막 줄에 개행이 없으면 `echo` 가 그
#   줄 끝에 눌어붙어 (`fi` + `alias dem=...`) alias 가 통째로 무효가 된다 — 실제로
#   겪었다: 스크립트는 성공을 찍었는데 `source ~/.bashrc` 후에도 command not found.
printf '\n%s\n' "$LINE" >> ~/.bashrc
# 실제로 그 셸에서 alias 가 서는지 검증한다 (썼다는 것만으로는 증거가 안 된다)
if bash -ic 'alias dem' >/dev/null 2>&1; then
  echo "  $LINE"
else
  echo "  ⚠ alias 를 썼지만 새 셸에서 서지 않는다 — ~/.bashrc 를 직접 확인하세요:"
  echo "      tail -3 ~/.bashrc"
fi

echo "═══ ⑥ CUDA 스모크 (taichi 가 V100 을 실제로 잡는가) ═══"
python3 - <<'PY' || fail "taichi CUDA 초기화 실패"
import taichi as ti
ti.init(arch=ti.cuda, device_memory_GB=1)
print('  taichi CUDA OK')
PY

echo "═══ ⑦ 재현 스모크 (GPU 불요 — 보존본에서 d_h 적합이 비트로 서는가) ═══"
python3 "$REPO/scripts/fit_dh_collapse.py" --dir "$DATA/se_curve" --mach 0.03 --n-grid 288 \
  --kits kit_ps_0_10,kit_ps_3_7,kit_ps_5_5,kit_ps_10_0 2>&1 | tail -4

cat <<EOF

═══ 준비 끝.  다음 (docs/dem_mpm_coupling_review_request_20260811.md §7 순서) ═══
  새 셸에서:  dem      # ← alias (cd + venv)
  1) ps_7_3 192@0.03 3점:
     bash $REPO/scripts/run_se_curve_batch.sh --kits kit_ps_7_3 --phi 0.66,0.72,0.81 --n-grid 192
  2) jam 재시험 / corner 런은 Codex 리뷰(Q1/Q2) 통과 후.
EOF
