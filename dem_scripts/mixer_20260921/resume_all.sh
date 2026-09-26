#!/usr/bin/env bash
# 죽은 믹서 런을 체크포인트에서 **잇는다** — 2026-09-26 (WSL 이 죽었다 다시 뜨면서 L 10 런이 53–61 % 에서 끊김).
#   ⛔ run_all.sh 의 FORCE=1 은 **처음부터** 다시 돌린다 (로그·덤프 덮음, 런당 4 일 넘게 손실).  이 스크립트는 체크포인트
#      (`restart/a.bin` · `b.bin`) 에서 잇는다 — 덱은 scripts/make_mixer_resume.py 가 원 in.mixer 에서 만든다.
#   사용 (어디서나):
#     SMOKE=L0_s32452843 bash dem_scripts/mixer_20260921/resume_all.sh   # ① 임시 복사본에서 5000 스텝 시험 (원 폴더 안 건드림)
#     DRY=1 bash dem_scripts/mixer_20260921/resume_all.sh                 # ② 죽은 런마다 in.resume · 영수증만 (띄우지 않음)
#     bash dem_scripts/mixer_20260921/resume_all.sh                       # ③ 재개 발사 (동시 상한 MAXJ, 기본 nproc)
#     ONLY=<런이름> …                                                      #    한 런만
#   판정 (run_all.sh · watch.sh 와 같다): 완주 = 배너 또는 마지막 step ≥ run 합 → 건너뜀 · pid 가 살아 있음 → 건너뜀 ·
#     로그 없음 (아직 안 돈 런) → run_all.sh 소관이라 건너뜀 · 그 밖 = 죽은 런 → 잇는다.
#   ★ 로그는 `>> log.lmp` 로 **이어 붙인다** (watch.sh 그대로 쓴다) · LIGGGHTS 자체 로그는 log.resume.liggghts.
#   ★ 재개 덱이 `read_restart` 직후 `RESUME_STEP <n>` 을 찍는다 — 영수증 (resume_receipt.json) 의 checkpoint_step 과 같아야 한다.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/../.." && pwd)"
OUT="${OUT:-$HERE/runs}"
LMP="${LMP:-lmp_serial}"; MAXJ="${MAXJ:-$(nproc)}"
PRE=(); command -v stdbuf >/dev/null && PRE=(stdbuf -oL -eL)
MKR="$ROOT/scripts/make_mixer_resume.py"

tot_steps() { grep -oE '^run +[0-9]+' "$1/in.mixer" 2>/dev/null | awk '{s+=$2} END{print s+0}'; }
last_step() { grep -E '^ +[0-9]+ +[0-9]+ ' "$1/log.lmp" 2>/dev/null | tail -1 | awk '{print $1+0}'; }
done_run() {
  local d="$1" t l; [ -f "$d/log.lmp" ] || return 1
  grep -q "Total wall time" "$d/log.lmp" && return 0
  t=$(tot_steps "$d"); l=$(last_step "$d")
  [ "${t:-0}" -gt 0 ] && [ "${l:-0}" -ge "$t" ]
}
live() { local c=0; for f in "$OUT"/*_s*/pid; do [ -f "$f" ] && kill -0 "$(cat "$f")" 2>/dev/null && c=$((c+1)); done; echo $c; }

# ── ① 스모크 — 복사본에서 짧게 돌려 재개가 **이어지는지** 본다 ─────────────────────────────
if [ -n "${SMOKE:-}" ]; then
  command -v "$LMP" >/dev/null || { echo "⛔ $LMP 없음 — LMP=<실행파일>"; exit 1; }
  src="$OUT/$SMOKE"; [ -f "$src/in.mixer" ] || { echo "⛔ 런 폴더가 아니다: $src"; exit 1; }
  T="${SMOKE_DIR:-${TMPDIR:-/tmp}/mixer_smoke_$SMOKE}"; rm -rf "$T"; mkdir -p "$T/post"
  ls "$src"/*.stl >/dev/null 2>&1 || { echo "⛔ $src 에 STL 이 없다 — 덱이 Drum/Front/Back.stl 을 읽는다"; exit 1; }
  cp -a "$src/in.mixer" "$src/log.lmp" "$T/"; cp -a "$src"/*.stl "$T/"; cp -a "$src/restart" "$T/"
  [ -d "$src/data" ] && cp -a "$src/data" "$T/"
  python3 "$MKR" "$T" --smoke-steps "${SMOKE_STEPS:-5000}"
  echo "▶ 스모크 실행 — $T  (${SMOKE_STEPS:-5000} 스텝, 수 분)"
  rc=0; ( cd "$T" && timeout "${SMOKE_TIMEOUT:-5400}" "${PRE[@]}" "$LMP" -in in.smoke -log none > smoke.log 2>&1 ) || rc=$?
  python3 - "$T" "$rc" <<'PY'
import json, re, sys
T, rc = sys.argv[1], int(sys.argv[2])
r = json.load(open(f'{T}/smoke_receipt.json'))
th = re.compile(r'^ +(\d+) +\d+ ')
def lines(p):
    d = {}
    for ln in open(p, encoding='utf-8', errors='replace'):
        m = th.match(ln)
        if m: d[int(m.group(1))] = ' '.join(ln.split())
    return d
orig, new = lines(f'{T}/log.lmp'), lines(f'{T}/smoke.log')
sl = open(f'{T}/smoke.log', encoding='utf-8', errors='replace').read()
m = re.search(r'RESUME_STEP (\d+)', sl)
c, s = r['checkpoint_step'], r['smoke_steps']
ok = True
def say(tag, cond, msg):
    global ok
    print(('  ✓ ' if cond else '  ✗ ') + msg)
    if tag and not cond: ok = False
say(1, m is not None and int(m.group(1)) == c, f"RESUME_STEP {m.group(1) if m else '없음'} == 체크포인트 {c:,} ({r['checkpoint_file']})")
say(1, 'ERROR' not in sl, "LIGGGHTS ERROR 없음" + ('' if 'ERROR' not in sl else ' — ' + sl[sl.find('ERROR'):][:160].replace('\n', ' ')))
say(1, c in new and c in orig and new[c] == orig[c], f"재개 직후 thermo (step {c:,}) == 원 로그 같은 줄 — 상태 복원")
if c in new and c in orig and new[c] != orig[c]:
    print(f"      원: {orig[c]}\n      새: {new[c]}")
say(1, (c + s) in new, f"목표 step {c + s:,} 까지 돌았다 (종료코드 {rc})")
if (c + s) in new and (c + s) in orig:
    same = new[c + s] == orig[c + s]
    print(('  ✓ ' if same else '  · ') + f"step {c + s:,} 줄도 원 로그와 {'같다 — 비트 단위 재현' if same else '다르다 — 재개 뒤 궤적이 갈라짐 (정보: 판정선 · 창과 무관)'}")
    if not same:
        print(f"      원: {orig[c + s]}\n      새: {new[c + s]}")
print('\n✓ 스모크 통과 — 재개 발사 가능 (DRY=1 로 덱 확인 → 발사)' if ok else '\n✗ 스모크 실패 — 발사하지 말 것 (smoke.log 확인)')
sys.exit(0 if ok else 1)
PY
  exit $?
fi

# ── ②③ 죽은 런 재개 ─────────────────────────────────────────────────────────────────
[ "${DRY:-0}" = 1 ] || command -v "$LMP" >/dev/null || { echo "⛔ $LMP 없음 — LMP=<실행파일>"; exit 1; }
echo "[재개] ${PRE[*]} $LMP  ·  런마다 1 코어 · 동시 상한 $MAXJ  ·  DRY=${DRY:-0}"
n=0
for d in "$OUT"/*_s*/; do
  d="${d%/}"; nm=$(basename "$d")
  [ -f "$d/in.mixer" ] || continue
  case "$nm" in *_old_*) continue;; esac
  [ -n "${ONLY:-}" ] && [ "$nm" != "$ONLY" ] && continue
  if [ -f "$d/pid" ] && kill -0 "$(cat "$d/pid")" 2>/dev/null; then echo "· 실행 중 — 건너뜀: $nm"; continue; fi
  [ -f "$d/log.lmp" ] || { echo "· 로그 없음 (아직 안 돈 런 — run_all.sh 소관): $nm"; continue; }
  if done_run "$d"; then echo "· 완주 — 건너뜀: $nm"; continue; fi
  python3 "$MKR" "$d" || { echo "⛔ $nm: 재개 덱 실패 — 중단"; exit 1; }
  [ "${DRY:-0}" = 1 ] && continue
  while [ "$(live)" -ge "$MAXJ" ]; do sleep 30; done
  rm -f "$d/pid"
  ( cd "$d" || exit 1
    printf '\n# ==== RESUME %s — in.resume (resume_receipt.json) ====\n' "$(date '+%F %T')" >> log.lmp
    setsid nohup bash -c 'echo $$ > pid; exec "$@"' _ "${PRE[@]}" "$LMP" -in in.resume -log log.resume.liggghts \
        >> log.lmp 2>&1 < /dev/null &
  )
  for _ in 1 2 3 4 5; do [ -s "$d/pid" ] && break; sleep 1; done
  [ -s "$d/pid" ] || { echo "⛔ $nm: pid 파일이 안 생겼다 — 중단"; exit 1; }
  n=$((n+1)); echo "▶ 재개 $nm  pid $(cat "$d/pid")  (동시 $(live)/$MAXJ)"
  sleep 2
done
echo "재개 끝 — 띄운 런 $n 개.  진행: watch -n 60 'bash $HERE/watch.sh'  ·  확인: grep RESUME_STEP */log.lmp"
