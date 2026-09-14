#!/usr/bin/env bash
# bms-balancing MATLAB 쪽 검사 전부. Octave 가 있으면 4종, 없으면 Python 2종.
#
#   ./run_all.sh [작업디렉터리]
#
# ⚠ 여기서 "통과" 는 **MATLAB 에서 돈다** 는 뜻이 아니다. Octave 8.4 로 잰
#   것이고, MathWorks 구현과 다를 수 있다. 무엇을 증명하고 못 하는지는
#   README.md 의 「이 검사가 증명하는 것 / 못 하는 것」 절에 적혀 있다.
set -u
T="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK="${1:-$(mktemp -d -t bmsverify.XXXXXX)}"
mkdir -p "$WORK"
fail=0
have_octave=0; command -v octave-cli >/dev/null 2>&1 && have_octave=1

hdr() { printf '\n\033[1m== %s ==\033[0m\n' "$1"; }

if [ "$have_octave" -eq 1 ]; then
  hdr "1. 구문 검사 — Octave 파서가 네 파일을 읽는가"
  for f in dd_eval dd_verify fit_cycles_driver; do
    if octave-cli --no-init-file --path "$T/.." \
         --eval "nargin('$f');" >/dev/null 2>&1; then echo "  OK   $f.m"
    else echo "  FAIL $f.m"; octave-cli --no-init-file --path "$T/.." \
         --eval "nargin('$f');" 2>&1 | head -3; fail=$((fail+1)); fi
  done
  for f in sgolayfilt quantile findpeaks; do
    if octave-cli --no-init-file --path "$T/../dd_shims" \
         --eval "nargin('$f');" >/dev/null 2>&1; then echo "  OK   dd_shims/$f.m"
    else echo "  FAIL dd_shims/$f.m"; fail=$((fail+1)); fi
  done

  hdr "2. dd_shims 수치 — 우리 shim vs Octave 내장 vs Python 포팅"
  ( cd "$WORK" && python3 "$T/gen_shim_cases.py" . >/dev/null \
    && octave-cli --no-init-file --path "$T" --path "$T/.." \
         --eval "run_shims('native','res_oct_native.csv')" >/dev/null 2>&1 \
    && octave-cli --no-init-file --path "$T" --path "$T/../dd_shims" \
         --eval "run_shims('shim','res_oct_shim.csv')" >/dev/null 2>&1 \
    && python3 "$T/check_shims.py" . ) || fail=$((fail+1))

  hdr "3. dd_eval.m 배관 e2e — Octave 전사본 vs Python 전사본 (합성 데이터)"
  "$T/run_e2e.sh" "$WORK/e2e" || fail=$((fail+1))
else
  printf '\n(octave-cli 가 없다 — 1~3 건너뜀. `apt-get install octave`)\n'
fi

hdr "4. --compare 이분 판정이 갈린 단계를 짚는가"
python3 "$T/test_compare_bisect.py" "$WORK/ddc.csv" || fail=$((fail+1))

hdr "5. Python verify eval 배관 스모크 (합성 xlsx)"
python3 "$T/test_py_smoke.py" || fail=$((fail+1))

printf '\n=====================================\n'
if [ "$fail" -eq 0 ]; then echo "전부 통과   (작업디렉터리 $WORK)"; else
  echo "실패 $fail 건   (작업디렉터리 $WORK)"; fi
exit $((fail > 0))
