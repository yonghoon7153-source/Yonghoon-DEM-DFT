#!/bin/bash
# PAI probe — the static checker heredoc runs `python3 - "$@"` (not -I); in the main flow its cwd = the case root (-r · cd $L),
#   so a stray difflib.py / fnmatch.py / shutil.py … there is imported instead of the stdlib module.  runnerck runs `python3 -I -`.
#   Here: -C run from a directory holding a harmless difflib.py that only prints a marker and re-exports the real module.
#   usage: bash shadow_import.sh <scratch with d07/>
WT=$(cd "$(dirname "$0")/../../../../.." && pwd)
SP=${1:?scratch}
B=$SP/shadow; rm -rf "$B"; mkdir -p "$B/root" "$B/W"
cat > "$B/root/difflib.py" <<'EOF'
import sys
print('SHADOW: local difflib.py imported by the static checker (cwd module)', file=sys.stderr)
sys.path = [p for p in sys.path if p not in ('', '.')]
del sys.modules['difflib']
import difflib as _real
sys.modules['difflib'] = _real
EOF
cd "$B/root" || exit 9
bash "$WT/scripts/resume_ckpt.sh" -C "$WT/docs/data/kg50_decks_20261027_v3_b50/kg50_d07_b50/input_kg50_d07_b50.liggghts" \
  "$SP/d07/d07_tool_r56.liggghts" restart_kg50_d07_b50/restart_settling_20001.bin 20001 "$B/W" 2>&1 | grep -E "SHADOW|정적 대조:"
echo "--- same with python3 -I (what runnerck uses):"
python3 -I - <<'EOF'
import difflib, sys
print('difflib from', difflib.__file__)
EOF
