#!/usr/bin/env bash
set -euo pipefail
umask 077
if [[ $# -ne 2 ]]; then echo 'CHECK_ONLY or GO_SUYOUNG_MATCHED_PREFIX_ONCE, then cross-return archive' >&2; exit 2; fi
mode=$1
case "$mode" in CHECK_ONLY|GO_SUYOUNG_MATCHED_PREFIX_ONCE) ;; *) exit 2 ;; esac
prior=$(realpath -e -- "$2")
pkg=$(pwd -P)
[[ -f "$prior" && -f "$pkg/RELEASE" ]]
pin=$(cat "$pkg/RELEASE")
[[ "$pin" =~ ^[0-9a-f]{40}$ ]]
sha256sum --strict -c --status SOURCE_SHA256SUMS
py="$HOME/Yonghoon-DEM-DFT/venv/bin/python"
[[ -x "$py" ]] || { echo 'Expected project WSL venv is missing' >&2; exit 2; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
cpu=$("$py" -I -B -c 'import os; print(min(os.sched_getaffinity(0)))')
runner=(taskset -c "$cpu" "$py" -I -B)
"${runner[@]}" -c 'import sys,numpy; print(sys.version.split()[0],numpy.__version__); sys.exit(0 if sys.version_info[:3]==(3,12,3) and numpy.__version__=="2.5.2" else "Reference WSL environment mismatch")'
driver="$pkg/docs/reviews/suyoung_wall_layers_20261123/matched_controls.py"
"${runner[@]}" "$driver" check --repo "$pkg" --prior "$prior"
printf 'DEVELOPMENT_ONLY\nRELEASE=%s\nCPU=%s\n' "$pin" "$cpu"
if [[ "$mode" == CHECK_ONLY ]]; then echo CHECK_OK; exit 0; fi
once="$HOME/suyoung_matched_once_${pin:0:12}"
mkdir -- "$once" || { echo "Existing attempt: $once" >&2; exit 2; }
work=$(mktemp -d "$HOME/suyoung_matched_work_XXXXXXXX")
ret=$(mktemp -d "$HOME/suyoung_matched_return_XXXXXXXX")
run="$work/run"
mkdir -- "$run"
screen="$run/screen.txt"
printf 'DEVELOPMENT_ONLY\nRELEASE=%s\nWORK=%s\nRETURN_DIRECTORY=%s\n' "$pin" "$work" "$ret" | tee "$screen" "$once/receipt.txt"
finish() {
    local rc=$?
    trap - EXIT INT HUP TERM
    set +e
    printf 'COMMAND_RC=%d\n' "$rc" | tee -a "$screen"
    cp -- "$screen" "$ret/screen.txt" &&
    tar -czf "$ret/suyoung_matched_result.tar.gz" -C "$work" run &&
    (cd -- "$ret" && sha256sum suyoung_matched_result.tar.gz screen.txt > SHA256SUMS && sha256sum -c SHA256SUMS && cat SHA256SUMS) ||
    { printf 'ARCHIVE_INCOMPLETE WORK=%s\n' "$work"; exit 3; }
    printf 'RETURN_DIRECTORY=%s\n' "$ret"
    exit "$rc"
}
trap finish EXIT
trap 'exit 130' INT
trap 'exit 143' TERM HUP
cp -- SOURCE_SHA256SUMS RELEASE "$run/"
sha256sum -- "$prior" | cut -d ' ' -f1 > "$run/prior_sha256.txt"
for seed in 8 16; do
    rc=0
    printf 'F8_SEED%s_BEGIN=%s\n' "$seed" "$(date -u +%FT%TZ)" | tee -a "$screen"
    timeout --kill-after=5s 610s "${runner[@]}" "$driver" arm --repo "$pkg" --prior "$prior" --seed-cells "$seed" --out "$run/seed$seed" > "$run/seed$seed.log" 2>&1 || rc=$?
    printf 'F8_SEED%s_RC=%d\n' "$seed" "$rc" | tee -a "$screen"
    if (( rc != 0 )); then tail -n 3 "$run/seed$seed.log" | tee -a "$screen"; exit "$rc"; fi
done
"${runner[@]}" "$driver" read --repo "$pkg" --prior "$prior" --run "$run" --out "$run/summary.json" > "$run/summary.log" 2>&1
sha256sum --strict -c --status SOURCE_SHA256SUMS
echo READBACK_REQUIRED | tee -a "$screen"
