#!/usr/bin/env bash
# 런처·생성기 회귀 — 2026-09-22 사고 둘을 **재현해 놓고** 막는다 (LIGGGHTS 없이 돈다: 가짜 실행파일).
#   사고 ① 완주했는데 배너가 없는 런을 "죽음" 으로 읽고 재발사 → 로그·덤프 소실 (E0_s49979687)
#   사고 ② 실행 중인 런의 덱을 제자리 덮어쓰기 → EOF 자리에서 새 파일 바이트를 명령으로 읽음 (E0_s32452843)
#   사용: bash dem_scripts/mixer_20260921/test_launcher.sh      (check_all.sh 에 배선)
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/../.." && pwd)"
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
pass=0; fail=0
chk() { if eval "$2"; then echo "  ✓ $1"; pass=$((pass+1)); else echo "  ✗ $1"; fail=$((fail+1)); fi; }
mk() {  # mk <이름> <두번째 run 스텝> <마지막 thermo step | -> <배너 0/1>   (tot = 1 + $2)
  local d="$T/runs/$1"; mkdir -p "$d/post"
  printf 'run 1\nrun %s\n' "$2" > "$d/in.mixer"
  if [ "$3" != "-" ]; then
    { echo "    Step Atoms KinEng"; printf '%12d %8d %s\n' "$3" 100 0.0; echo "Dangerous builds = 0"
      [ "$4" = 1 ] && echo "Total wall time: 0:00:01"; } > "$d/log.lmp"
  fi
}
FAKE="$T/lmp_fake"; printf '#!/usr/bin/env bash\nsleep 2\n' > "$FAKE"; chmod +x "$FAKE"

echo "── run_all.sh: 완주 판정 · 죽은 런 비재발사 ──"
mk done_s1 10 11 1        # 배너 있는 완주
mk nobanner_s1 10 11 0    # ★ 배너 없이 마지막 step 도달 = 새 덱의 종료 결함 (09-22 E0 3/3)
mk dead_s1 10 3 0         # 죽은 미완주
mk fresh_s1 10 - 0        # 아직 안 돈 것
out=$(OUT="$T/runs" LMP="$FAKE" MAXJ=4 bash "$HERE/run_all.sh" 2>&1)
chk '① 배너 있는 완주 런은 안 띄운다'                          "! [ -f '$T/runs/done_s1/pid' ]"
chk '② ★ 배너 없는 완주 런도 안 띄운다 (옛 판은 재발사했다)'    "! [ -f '$T/runs/nobanner_s1/pid' ] && grep -q '완료됨 (배너 없음' <<<\"\$out\""
chk '③ ★ 죽은 미완주 런은 FORCE 없이 안 띄운다 — 목록만'        "! [ -f '$T/runs/dead_s1/pid' ] && grep -q '자동 재발사 안 함' <<<\"\$out\""
chk '④ 아직 안 돈 런은 띄운다 (pid 파일 = 실제 PID)'             "[ -s '$T/runs/fresh_s1/pid' ] && kill -0 \"\$(cat '$T/runs/fresh_s1/pid')\""
chk '⑤ 미완주 목록을 끝에 찍는다'                               "grep -q '미완주(죽은) 런 1 개' <<<\"\$out\""
sleep 3
out2=$(OUT="$T/runs" LMP="$FAKE" MAXJ=4 FORCE=1 bash "$HERE/run_all.sh" 2>&1)
chk '⑥ FORCE=1 이면 죽은 런을 띄운다'                            "[ -s '$T/runs/dead_s1/pid' ]"
chk '⑦ FORCE=1 이어도 완주 런(배너 유무 무관)은 안 띄운다'        "! [ -f '$T/runs/nobanner_s1/pid' ] && ! [ -f '$T/runs/done_s1/pid' ]"
sleep 3

echo "── watch.sh: 같은 판정 ──"
w=$(OUT="$T/runs" bash "$HERE/watch.sh" 2>&1)
chk '⑧ watch: 배너 없는 완주는 완료* (옛 판은 ⛔죽음 100%)'      "grep -E '^nobanner_s1 ' <<<\"\$w\" | grep -q '완료\*'"
chk '⑧b watch: 배너 있는 완주는 완료'                           "grep -E '^done_s1 ' <<<\"\$w\" | grep -qE '완료 '"
chk '⑧c watch: 죽은 런은 ⛔죽음'                               "grep -E '^dead_s1 ' <<<\"\$w\" | grep -q '죽음' || grep -E '^dead_s1 ' <<<\"\$w\" | grep -q '실행'"

echo "── gen_all.sh: 살아 있는 런 건너뜀 · 로그 있는 런 건너뜀 · rename 교체 ──"
G="$T/gen"; mkdir -p "$G"
#  캠페인 13 디렉터리 이름을 생성기에서 받아 12 개는 '살아 있는' 런, 1 개는 '죽은(로그 있는)' 런으로 꾸민다
mapfile -t ARMS < <(python3 - "$ROOT" <<'PY'
import sys, importlib.util
spec = importlib.util.spec_from_file_location('m', sys.argv[1] + '/scripts/make_mixer_deck.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for a, s in m.CAMPAIGN: print(f'{a}_s{s}')
for a, s, r in m.REFERENCE: print(f'{a}_s{s}')
PY
)
chk '⑨ 캠페인 목록 13 개' "[ ${#ARMS[@]} -eq 13 ]"
sleep 30 & SL=$!
for a in "${ARMS[@]}"; do mkdir -p "$G/$a"; echo OLD > "$G/$a/in.mixer"; echo "$SL" > "$G/$a/pid"; done
victim="${ARMS[12]}"; rm -f "$G/$victim/pid"; echo "log" > "$G/$victim/log.lmp"    # 죽은 런 하나 (E0 기준 런)
g1=$(OUT="$G" STL="$ROOT/dem_scripts/mixer_20260919" bash "$HERE/gen_all.sh" 2>&1)
chk '⑩ 살아 있는 런 12 개는 전부 건너뛴다'      "[ \$(grep -c '실행 중 — 건너뜀' <<<\"\$g1\") -eq 12 ]"
chk '⑩b 로그 있는 죽은 런은 FORCE 없이 건너뛴다' "grep -q '로그 있음' <<<\"\$g1\" && [ \"\$(cat '$G/$victim/in.mixer')\" = OLD ]"
chk '⑩c 살아 있는 런의 덱은 한 바이트도 안 바뀐다' "[ \"\$(cat \"$G/${ARMS[0]}/in.mixer\")\" = OLD ]"
#  rename 교체 — 열어 둔 fd 는 옛 내용을 끝까지 읽는다 (제자리 덮어쓰기면 새 바이트를 읽는다)
rd=$(python3 - "$G/$victim/in.mixer" "$HERE/gen_all.sh" "$G" "$ROOT/dem_scripts/mixer_20260919" <<'PY'
import sys, subprocess, os
path, gen, out, stl = sys.argv[1:5]
f = open(path, 'rb')                      # 실행 중인 LIGGGHTS 처럼 먼저 열어 둔다
env = dict(os.environ, OUT=out, STL=stl, FORCE='1')
p = subprocess.run(['bash', gen], env=env, capture_output=True, text=True)
tail = f.read()                           # 옛 inode 를 읽는다 — rename 이면 b'OLD\n'
print('OK' if tail == b'OLD\n' and 'restart' in open(path).read() else f'NG tail={tail!r} rc={p.returncode}')
PY
)
chk '⑪ ★ FORCE=1 재생성은 rename 교체 — 열린 fd 는 옛 내용(OLD)을 읽고 새 파일은 새 덱이다' "[ \"$rd\" = OK ]"
chk '⑪b 새 덱 옆에 n_expected · r_container 가 생긴다' "[ -s '$G/$victim/n_expected' ] && [ -s '$G/$victim/r_container' ]"
chk '⑪c 임시 디렉터리 .new 가 남지 않는다' "! [ -d '$G/$victim.new' ]"
kill "$SL" 2>/dev/null

echo "test_launcher: $pass PASS / $fail FAIL"
[ "$fail" -eq 0 ]
