#!/usr/bin/env bash
# One-shot setup for a fresh compute server (gabia g-cloud etc.) — MPM/DEM ready.
#
#   curl -fsSL https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/claude/stoic-knuth-NObVQ/scripts/setup_gabia.sh | bash
#
# Idempotent: safe to re-run.  Does, in order:
#   1. system deps (git, python3, pip — apt or yum)
#   2. clone the repo to ~/work/Yonghoon-DEM-DFT (or pull if it exists)
#   3. checkout the working branch claude/stoic-knuth-NObVQ
#   4. pip deps for MPM/DEM (taichi, numpy, matplotlib) [+ webapp extras with --with-webapp]
#   5. GPU probe (nvidia-smi) → tells you whether --arch cuda is available
#   6. smoke test: dem3d_plastic --unit-test (CPU, seconds)
#
# NOTE: clone is read-only (repo is public).  Pushing from this server needs a
# GitHub token — keep the uma workflow: compute here, results go back via scp /
# pasted output, commits happen from the Claude session.
set -euo pipefail

REPO_URL="https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT.git"
BRANCH="claude/stoic-knuth-NObVQ"
WORK="$HOME/work"
DIR="$WORK/Yonghoon-DEM-DFT"
WITH_WEBAPP=0
[ "${1:-}" = "--with-webapp" ] && WITH_WEBAPP=1

echo "== [1/6] system deps =="
if command -v apt-get >/dev/null 2>&1; then
    apt-get update -qq || true
    DEBIAN_FRONTEND=noninteractive apt-get install -y -qq git python3 python3-pip python3-venv curl >/dev/null
elif command -v dnf >/dev/null 2>&1; then
    dnf install -y -q git python3 python3-pip curl
elif command -v yum >/dev/null 2>&1; then
    yum install -y -q git python3 python3-pip curl
else
    echo "  no apt/dnf/yum — install git+python3+pip manually"; exit 1
fi
python3 --version

echo "== [2/6] repo =="
mkdir -p "$WORK"
if [ -d "$DIR/.git" ]; then
    echo "  exists — fetching"
    git -C "$DIR" fetch origin "$BRANCH"
else
    git clone --filter=blob:none "$REPO_URL" "$DIR"
fi

echo "== [3/6] branch $BRANCH =="
cd "$DIR"
git checkout -B "$BRANCH" "origin/$BRANCH"
git log --oneline -1

echo "== [4/6] python deps (MPM/DEM) =="
PIP="python3 -m pip"
$PIP install --upgrade pip -q
# taichi 1.7.4 = the version validated on uma + the cloud session (needs py3.8–3.12)
$PIP install -q "taichi==1.7.4" numpy matplotlib scipy || {
    echo "  ⚠ taichi 1.7.4 wheel failed — likely python>=3.13.  Install python3.11 and retry:"
    echo "    apt-get install -y python3.11 python3.11-venv && python3.11 -m pip install taichi==1.7.4 numpy matplotlib scipy"
    exit 1
}
if [ "$WITH_WEBAPP" = "1" ]; then
    echo "  + webapp extras (flask etc.)"
    $PIP install -q -r webapp/requirements.txt
    echo "  ⚠ webapp case DATA (webapp/results, archive) is NOT in git — rsync it from"
    echo "    your WSL machine if you want the dashboard populated here.  And NEVER run"
    echo "    app.py bound to 0.0.0.0 on this public IP (debug=True ⇒ RCE) — use:"
    echo "    ssh -L 5000:localhost:5000 root@<this-server>  then PORT=5000 python3 app.py"
fi

echo "== [5/6] GPU probe =="
if command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi >/dev/null 2>&1; then
    nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv,noheader
    echo "  → GPU available: use --arch cuda (add --gpu-mem 2.0 if the card is shared)"
else
    echo "  no NVIDIA GPU — MPM/DEM run with --arch cpu (calibration N≤2500 is fine on CPU)"
fi

echo "== [6/6] smoke test: Thornton contact law (CPU, ~5 s) =="
python3 scripts/dem3d_plastic.py --unit-test 2>&1 | grep -E "UNIT TEST|PASS|FAIL" || {
    echo "  ✗ unit test did not run — check the taichi install above"; exit 1
}

cat <<'EOF'

✓ setup complete.  Next steps (pure-SE Minnmann calibration):

  cd ~/work/Yonghoon-DEM-DFT

  # plastic w/ incompressibility lock (CPU; add --arch cuda if GPU free)
  python3 scripts/dem3d_plastic.py --material SE --n-target 800 --plastic --arch cpu

  # rigid baseline (cap OFF)
  python3 scripts/dem3d_plastic.py --material SE --n-target 800 --rigid --arch cpu

  # beta-lock sweep → find the b that gives porosity ≈ 10% @ 0.3 GPa
  for b in 0.02 0.04 0.06 0.10 0.16; do
    echo "=== beta=$b ==="
    python3 scripts/dem3d_plastic.py --material SE --n-target 800 --plastic \
        --beta-lock $b --arch cpu --quiet | tail -2
  done
EOF
