#!/usr/bin/env bash
# Suyoung 2D registration 1 (contact mini) execution block - DEVELOPMENT_ONLY.
# Started by the PASTE TXT from the unpacked package: CHECK_ONLY | GO_SUYOUNG_CONTACT_MINI_ONCE | READBACK DIR.
# CHECK_ONLY and READBACK run no arm.  GO runs the 50 registered arms once (two physical cores, one thread
# per arm, longest first, registered limit + 30 s grace, no automatic retry) and writes the return bundle.
set -euo pipefail
umask 077
root=$(pwd -P)
mode=${1:-}
case "$mode" in
    CHECK_ONLY|GO_SUYOUNG_CONTACT_MINI_ONCE) [[ $# == 1 ]] || { echo 'Expected exactly one mode'; exit 2; } ;;
    READBACK) [[ $# == 2 ]] || { echo 'READBACK expects the return directory'; exit 2; }; received=$(realpath -e -- "$2") ;;
    *) echo 'Expected CHECK_ONLY, GO_SUYOUNG_CONTACT_MINI_ONCE or READBACK'; exit 2 ;;
esac
sha256sum --strict --status --check SOURCE_SHA256SUMS
py="$HOME/Yonghoon-DEM-DFT/venv/bin/python"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python=("$py" -I -X utf8 -B)
pin=$(cat RELEASE)
printf 'RELEASE=%s\nSOURCE_MANIFEST_SHA256=%s\n' "$pin" "$(sha256sum < SOURCE_SHA256SUMS | cut -d' ' -f1)"
"${python[@]}" reg1_queue.py env
if [[ $mode == READBACK ]]; then
    temp=$(mktemp -d)
    "${python[@]}" reg1_queue.py unpack "$root" "$received" "$temp"
    "${python[@]}" reg1_reader.py replay "$root" "$temp/run" "$received" "$temp/return_receipt.json"
    exit 0
fi
"${python[@]}" reg1_queue.py cores "$root"
"${python[@]}" docs/reviews/suyoung_next_registrations_20261125/driver/driver.py CHECK_ONLY --root "$root"
"${python[@]}" reg1_queue.py plan "$root"
"${python[@]}" reg1_reader.py selfcheck "$root"
if [[ $mode == CHECK_ONLY ]]; then echo CONTACT_MINI_CHECK_ONLY_OK; exit 0; fi
[[ $mode == GO_SUYOUNG_CONTACT_MINI_ONCE ]] || exit 2
once="$HOME/suyoung_contact_mini_1125_once"
mkdir -- "$once" || { echo "ALREADY_RESERVED $once"; exit 2; }
work=$(mktemp -d "$HOME/suyoung_contact_mini_work_XXXXXXXX")
ret=$(mktemp -d "$HOME/suyoung_contact_mini_return_XXXXXXXX")
run="$work/run"
mkdir -- "$run"
screen="$run/screen.txt"
printf 'RELEASE=%s\nWORK_DIRECTORY=%s\nRETURN_DIRECTORY=%s\n' "$pin" "$run" "$ret" | tee "$once/receipt.txt" "$screen"
cp -- RELEASE SOURCE_SHA256SUMS "$run/"
phase=QUEUE
finish() {
    rc=$?
    trap - EXIT INT TERM HUP
    set +e
    if (( rc != 0 )); then printf '{"label":"DEVELOPMENT_ONLY","phase":"%s","rc":%d,"status":"TECHNICAL_INCOMPLETE"}\n' "$phase" "$rc" > "$run/incomplete.json"; fi
    printf 'COMMAND_RC=%s\n' "$rc" | tee -a "$screen"
    (cd -- "$run" && find . -type f ! -path './SHA256SUMS' -printf '%P\0' | LC_ALL=C sort -z | xargs -0 sha256sum > SHA256SUMS && sha256sum --strict --status -c SHA256SUMS) &&
    cp -- "$screen" "$ret/screen.txt" &&
    tar -czf "$ret/suyoung_contact_mini_result.tar.gz" -C "$work" run &&
    (cd -- "$ret" && sha256sum suyoung_contact_mini_result.tar.gz screen.txt > SHA256SUMS && sha256sum --strict -c SHA256SUMS && cat SHA256SUMS) ||
    { echo "ARCHIVE_INCOMPLETE WORK_DIRECTORY=$run"; exit 3; }
    printf 'RETURN_DIRECTORY=%s\n' "$ret"
    exit "$rc"
}
trap finish EXIT
trap 'exit 130' INT
trap 'exit 143' TERM HUP
echo 'DEVELOPMENT_ONLY REG1_CONTACT_MINI ARMS=50 TWO_PHYSICAL_CORES THREADS_PER_ARM=1 AUTOMATIC_RETRIES=0 GRACE_S=30' | tee -a "$screen"
"${python[@]}" reg1_queue.py go "$root" "$run" | tee -a "$screen"
phase=SUMMARY
sha256sum --strict --status --check SOURCE_SHA256SUMS
"${python[@]}" reg1_reader.py summary "$root" "$run" | tee -a "$screen"
echo REG1_CONTACT_MINI_COMPLETE | tee -a "$screen"
