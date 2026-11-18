#!/bin/bash
#SBATCH --job-name=rtFixtureDev
#SBATCH --partition=cpu
#SBATCH --qos=cpu-60
#SBATCH --nodes=1
#SBATCH --ntasks=6
#SBATCH --cpus-per-task=1
#SBATCH --time=01:00:00
#SBATCH --no-requeue
#SBATCH --output=job_%j.out
#SBATCH --error=job_%j.err
umask 077
set -o pipefail
cd "$SLURM_SUBMIT_DIR" || exit 2
run_fixture() {
  source "$HOME/.bashrc"
  conda activate myenv || return 2
  export LMP="$HOME/LIGGGHTS-PUBLIC/src/lmp_mpi"
  export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
  bash packet/fixture.sh
}
run_fixture > fixture_screen.txt 2>&1
rc=$?
printf 'FIXTURE_RC=%s\n' "$rc" | tee worker_rc.txt
items=(worker_rc.txt fixture_screen.txt SOURCE_PIN)
if [ -s work/fixture.report.tgz ]; then items+=(work/fixture.report.tgz)
elif [ -d work ]; then items+=(work); fi
tar -czf rt_development_return.tar.gz -- "${items[@]}" &&
  sha256sum -- rt_development_return.tar.gz > SHA256SUMS.tmp &&
  mv -- SHA256SUMS.tmp SHA256SUMS || exit 3
exit "$rc"
