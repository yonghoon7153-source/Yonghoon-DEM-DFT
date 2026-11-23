#!/usr/bin/env bash
set -euo pipefail
umask 077
if [[ $# -ne 4 ]]; then
    echo 'Expected CHECK_ONLY or GO_SUYOUNG_DEPTH_PREFIX_ONCE, half-speed result, material-lid result, and wall-balance result.' >&2
    exit 2
fi
case "$1" in CHECK_ONLY|GO_SUYOUNG_DEPTH_PREFIX_ONCE) mode=$1 ;; *) exit 2 ;; esac
pkg=$(pwd -P)
prior=$(realpath -e -- "$2")
material=$(realpath -e -- "$3")
baseline=$(realpath -e -- "$4")
previous_pin=ba0e2bb980a4f098aee6ee526d069ed2d2446151
material_pin=35099db02148c1a5dc2581f880e0adbf28c0368d
balance_pin=0c4eb97d447f9afa984303425e1c5ab221ae9cec
prior_hash=ddcf2fd738430c40246d177d1e1dea73de24883c07218e4f07c0dcf6de90f863
material_hash=cdd3ff1dcdbe02dcb6493a4112a0136076883f2179c33f322e2287c0ffdfb14e
baseline_hash=1f680f4f255910bb2c93ce7e2edea004c89b4177fb3a4b8af93bd59edeab209e
verify_inputs() {
    sha256sum --strict --check --status "$pkg/SOURCE_SHA256SUMS" &&
    [[ $(cat "$pkg/history/RELEASE") == "$previous_pin" ]] &&
    [[ $(cat "$pkg/history/history/RELEASE") == "$material_pin" ]] &&
    [[ $(cat "$pkg/history/history/history/RELEASE") == "$balance_pin" ]] &&
    [[ $(sha256sum < "$prior") == "$prior_hash  -" ]] &&
    [[ $(sha256sum < "$material") == "$material_hash  -" ]] &&
    [[ $(sha256sum < "$baseline") == "$baseline_hash  -" ]]
}
verify_inputs || { echo 'Source package or reference result digest mismatch.' >&2; exit 2; }
pin=$(cat RELEASE)
[[ "$pin" =~ ^[0-9a-f]{40}$ ]]
py="$HOME/Yonghoon-DEM-DFT/venv/bin/python"
[[ -x "$py" ]] || { echo 'Expected WSL project venv.' >&2; exit 2; }
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
cpu=$("$py" -I -B -c 'import os; print(min(os.sched_getaffinity(0)))')
pyrun=(taskset -c "$cpu" "$py" -I -B)
"${pyrun[@]}" -c 'import os,sys,numpy; assert sys.version_info[:3]==(3,12,3) and numpy.__version__=="2.5.2" and len(os.sched_getaffinity(0))==1, "reference WSL runtime mismatch"'
app=("${pyrun[@]}" "$pkg/docs/reviews/suyoung_half_speed_readback_20261123/depth_prefix.py")
inputs=(--root "$pkg" --prior "$prior" --material "$material" --baseline "$baseline")
"${app[@]}" check "${inputs[@]}"
if [[ "$mode" == CHECK_ONLY ]]; then printf 'CHECK_OK\nRELEASE=%s\n' "$pin"; exit 0; fi

once="$HOME/suyoung_depth_prefix_once_${pin:0:12}"
mkdir -- "$once" || { echo "Attempt already reserved. See $once/receipt.txt" >&2; exit 2; }
work=$(mktemp -d "$HOME/suyoung_depth_prefix_work_XXXXXXXX")
ret=$(mktemp -d "$HOME/suyoung_depth_prefix_return_XXXXXXXX")
run="$work/run"
mkdir -- "$run"
printf 'RELEASE=%s\nWORK_DIRECTORY=%s\nRETURN_DIRECTORY=%s\n' "$pin" "$work" "$ret" | tee "$once/receipt.txt"
screen="$run/screen.txt"
phase=INITIALIZE
finish() {
    local rc=$?
    trap - EXIT INT HUP TERM
    set +e
    if (( rc != 0 )); then
        printf '{"status":"INCOMPLETE","phase":"%s","rc":%d,"u6_qualified":false,"stage3_go":false,"three_dimensional_go":false}\n' \
            "$phase" "$rc" > "$run/incomplete.json"
    fi
    printf 'COMMAND_RC=%d\n' "$rc" | tee -a "$screen"
    cp -- "$screen" "$ret/screen.txt" &&
    tar -czf "$ret/suyoung_depth_prefix_result.tar.gz" -C "$work" run &&
    (cd -- "$ret" && sha256sum suyoung_depth_prefix_result.tar.gz screen.txt > SHA256SUMS &&
     sha256sum --check --strict SHA256SUMS && cat SHA256SUMS) ||
    { printf 'ARCHIVE_INCOMPLETE WORK_DIRECTORY=%s\n' "$work"; exit 3; }
    printf 'RETURN_DIRECTORY=%s\n' "$ret"
    exit "$rc"
}
trap finish EXIT
trap 'exit 130' INT
trap 'exit 143' TERM HUP
printf 'DEVELOPMENT_ONLY\nRELEASE=%s\nPRIOR_HALF_SPEED_SHA256=%s\nPRIOR_MATERIAL_LID_SHA256=%s\nPRIOR_BALANCE_SHA256=%s\nCPU=%s\nSPEED_RATIO=0.5\nF12_STEPS=555\nF24_STEPS=1110\nF12_BUDGET_SECONDS=600\nF24_BUDGET_SECONDS=1200\nWATCHDOG_GRACE_SECONDS=30\nRETRIES=0\n' \
    "$pin" "$prior_hash" "$material_hash" "$baseline_hash" "$cpu" | tee "$screen"
cp -- RELEASE SOURCE_SHA256SUMS "$run/"
inputs+=(--run "$run")
for cells in 12 24; do
    phase="F$cells"
    case "$cells" in 12) watchdog=630 ;; 24) watchdog=1230 ;; esac
    printf '%s_BEGIN=%s\n' "$phase" "$(date -u +%FT%TZ)" | tee -a "$screen"
    rc=0
    timeout --signal=KILL "${watchdog}s" "${app[@]}" arm "${inputs[@]}" --cells "$cells" > "$run/$phase.log" 2>&1 || rc=$?
    printf '%s_RC=%d\n' "$phase" "$rc" | tee -a "$screen"
    if (( rc != 0 )); then tail -n 4 -- "$run/$phase.log"; exit "$rc"; fi
done
phase=READBACK
verify_inputs
"${app[@]}" summary "${inputs[@]}" | tee "$run/readback.log"
[[ -s "$run/summary.json" ]] || { echo 'MISSING_SUMMARY' >&2; exit 3; }
printf 'DEPTH_PREFIX_READBACK_COMPLETE\n' | tee -a "$screen"
