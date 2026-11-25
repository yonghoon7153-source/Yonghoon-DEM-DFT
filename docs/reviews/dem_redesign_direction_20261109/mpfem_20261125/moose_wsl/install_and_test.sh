# MOOSE (pre-built conda package) install + rotation check on WSL - 1저자 11-25 (가-1) - development data
# run: bash ~/moose_setup/install_and_test.sh   (writes ~/moose_setup/install.log)
M=$HOME/moose_setup
mkdir -p "$M" && cd "$M" || exit 1
LOG=$M/install.log
exec > >(tee -a "$LOG") 2>&1
echo "== 0 check $(date)"
uname -sr; ldd --version | head -n 1; echo "cores $(nproc)"; free -g | sed -n '1,2p'; df -h "$HOME" | tail -n 1
FREE_GB=$(df -BG --output=avail "$HOME" | tail -n 1 | tr -dc '0-9')
if [ "${FREE_GB:-0}" -lt 8 ]; then echo "STOP: free disk ${FREE_GB} GB < 8 GB"; exit 1; fi
echo "== 1 miniforge"
if [ -x "$HOME/miniforge/bin/conda" ]; then echo "miniforge exists"; else
  curl -L -o Miniforge3-Linux-x86_64.sh https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh && bash Miniforge3-Linux-x86_64.sh -b -p "$HOME/miniforge" || { echo "STOP: miniforge install failed"; exit 1; }
fi
source "$HOME/miniforge/etc/profile.d/conda.sh" || { echo "STOP: conda.sh"; exit 1; }
echo "== 2 moose env"
conda config --add channels https://conda.software.inl.gov/public
if conda env list | grep -qE '^moose '; then echo "env moose exists"; else
  conda create -y -n moose moose || { echo "STOP: conda create failed"; exit 1; }
fi
conda activate moose || { echo "STOP: activate"; exit 1; }
echo "== 3 executable"
EXE=""
for c in moose-opt moose combined-opt; do if command -v "$c" >/dev/null 2>&1; then EXE=$(command -v "$c"); break; fi; done
ls "$CONDA_PREFIX/bin" | grep -iE 'moose|combined' | head -n 10
if [ -z "$EXE" ]; then echo "STOP: no moose executable found"; exit 1; fi
echo "EXE=$EXE"; "$EXE" --version 2>&1 | head -n 5
echo "== 4 rotation test"
mkdir -p "$M/rot" && cd "$M/rot" && cp "$M/rot_test.i" . && "$EXE" -i rot_test.i > run.log 2>&1; echo "moose rc=$?"
tail -n 5 run.log
if [ -f rot_test_out.csv ]; then python3 "$M/check_rot.py" rot_test_out.csv; else echo "STOP: no csv"; grep -iE 'error|\*\*\*' run.log | head -n 20; fi
echo "== done $(date)"
du -sh "$HOME/miniforge" 2>/dev/null
