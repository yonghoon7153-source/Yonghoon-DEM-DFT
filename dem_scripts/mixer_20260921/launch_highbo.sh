#!/usr/bin/env bash
# 고-Bo 확장 `LH` 발사 — **첫 시드 하나 → bin 0 스모크 증서 → 나머지 둘** (2026-09-28, Codex 3차 HBR3-08 · Q5)
#
# 왜: 사전등록 docs/reviews/mixer_highbo_prereg_20260927.md §8 (D-4) 는 `LH_s32452843` 를 먼저 띄우고 첫 완전 바퀴 (bin 0)
#   기술 스모크가 통과한 뒤에만 `LH_s49979687` · `LH_s67867967` 을 띄우기로 했다.  그런데 옛 §2-5 의 `MAXJ=3 run_all.sh` 는
#   미실행 `_s*` 를 전부 돌고 스모크를 읽지 않으므로 LH 덱 셋을 **한꺼번에** 띄운다 (`MAXJ=1` 도 첫 런이 끝나면 다음을 띄울 뿐
#   판정을 기다리지 않는다).  ⇒ run_all.sh 는 이제 LH 를 기본으로 건너뛰고, 이 스크립트만 `ALLOW_LH=1 ONLY=<런>` 으로 **한 개씩**
#   부른다 (pid · 동시 상한 · 완주 판정 · 죽은 런 비재발사는 run_all.sh 그대로).
#
# 사용 (리포 루트에서):
#   ① bash dem_scripts/mixer_20260921/launch_highbo.sh first
#        관문: 덱 비교 (`python3 scripts/mixer_deck_diff.py --runs <OUT> --allow B` 가 0 으로 끝남) · LH 세 시드 모두 log.lmp · pid 없음
#        → 슬롯 (전 런 합산 live < MAXJ) → 봉인 <OUT>/LH_s32452843/launch_record.json → LH_s32452843 **하나만** 발사하고 끝난다
#   ② bin 0 (첫 완전 바퀴) 이 끝나면 스모크 증서:
#        python3 scripts/measure_mixing_index.py <OUT>/LH_s32452843 --ref <OUT>/E0_s32452843 --r-container 0.013138 --axis x … --json <smoke.json>
#        (칸 · 규약은 사전등록 §2-3 · §8 그대로 — 이 스크립트는 칸을 정하지 않는다)
#   ③ bash dem_scripts/mixer_20260921/launch_highbo.sh rest <smoke.json>
#        관문: 첫 시드가 ① 로 봉인 · 발사됨 · 증서 (JSON 목록의 첫 원소) `run` = LH_s32452843 · `smoke.complete` = true ·
#        `smoke.tech_smoke` = [] · `smoke.qc_repr.pass` = true (JSON true 만 — 1 · "true" 는 거부) · 증서가 첫 봉인보다 나중 ·
#        코호트 (나머지 둘의 in.mixer · STL · 바이너리 sha256 = 첫 봉인 때) · 덱 비교 재통과
#        → 하나라도 틀리면 **발사 0** · 0 이 아닌 종료.  통과하면 런마다 슬롯 → 봉인 → 발사 (LH_s49979687 · LH_s67867967)
#   환경변수: OUT (기본 dem_scripts/mixer_20260921/runs) · LMP (기본 lmp_serial) · MAXJ (기본 nproc — **전 런** 합산 상한)
#            DECKDIFF (덱 비교기 경로 — 기본 scripts/mixer_deck_diff.py, python3 로 부른다 · 시험은 대역을 꽂는다)
#
# ★ 봉인 (Codex Q5 — 실행 **직전**): 바이너리 (`command -v $LMP`) · in.mixer · Drum/Front/Back.stl sha256 · 리포 git HEAD (없으면
#   no-git) · 지역 · UTC 시각 · 호스트 · nproc · LMP 경로 · 런 · 시드.  슬롯이 난 **뒤**, 발사 **앞**에 쓴다 (대기 중에는 봉인도 없다).
#   first 봉인에는 세 시드의 덱 · STL 해시 (코호트) 도 적는다 — rest 는 첫 시드가 스모크를 받은 그 코호트인지 대조한다.
# ⛔ 로그 · pid 가 있는 LH 는 다시 띄우지 않고 그 봉인도 덮지 않는다 (재개는 resume_all.sh).  정지는 PID 로만 (pkill -f 금지).
# ⚠ rest 가 기계로 읽는 것은 판독기 증서 (§8 ③ 의 smoke 필드) 뿐이다 — §8 ① 보존 · ② 접촉 계약 · ③ 의 8×8×2 바닥 비 · ④ step/s 는
#   사람이 확인한다 (그 중 하나라도 실패면 rest 를 부르지 않는다 = 전체 확장 HOLD).
#   회귀: test_launcher.sh HL①–⑦ (가짜 실행파일 · 덱 비교기 대역).
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/../.." && pwd)"
OUT="${OUT:-$HERE/runs}"
LMP="${LMP:-lmp_serial}"; MAXJ="${MAXJ:-$(nproc)}"
DECKDIFF="${DECKDIFF:-$ROOT/scripts/mixer_deck_diff.py}"
FIRST=LH_s32452843; REST=(LH_s49979687 LH_s67867967)     # §8 (D-4) 순서 = 생성기 CAMPAIGN_HIGHBO 순서 (첫 시드 = 캠페인 첫 시드)

usage() {
  cat <<EOF
사용 (리포 루트에서) — 사전등록 §8 (D-4) 순서:
  bash dem_scripts/mixer_20260921/launch_highbo.sh first               # 관문 → 봉인 → $FIRST 하나만
  bash dem_scripts/mixer_20260921/launch_highbo.sh rest <smoke.json>   # bin 0 스모크 증서 · 코호트 · 덱 비교 → 봉인 → ${REST[*]}
  증서 = python3 scripts/measure_mixing_index.py <OUT>/$FIRST --ref <OUT>/E0_s32452843 … --json <smoke.json>
  환경변수: OUT · LMP (기본 lmp_serial) · MAXJ (기본 nproc, 전 런 합산) · DECKDIFF (기본 scripts/mixer_deck_diff.py)
EOF
}

#  run_all.sh 와 같은 정의 — pid 파일 + kill -0 로 **살아 있는 런만**, LH 가 아닌 런까지 전부 센다
live() { local c=0; for f in "$OUT"/*_s*/pid; do [ -f "$f" ] && kill -0 "$(cat "$f")" 2>/dev/null && c=$((c+1)); done; echo $c; }
fresh() { [ ! -e "$OUT/$1/log.lmp" ] && [ ! -e "$OUT/$1/pid" ]; }       # 한 번도 안 뜬 런
stamp() { date -u +%Y%m%dT%H%M%S.%NZ; }                                 # 옆으로 옮긴 봉인 이름 — 같은 초에 둘이어도 안 덮게

wait_slot() {  # 전 런 합산 live < MAXJ 가 될 때까지 (run_all.sh 와 같은 30 초 주기) — 봉인은 그 **뒤**
  local said=0
  while [ "$(live)" -ge "$MAXJ" ]; do
    [ "$said" = 1 ] || { echo "… 동시 상한 대기 — 살아 있는 런 $(live)/$MAXJ (30 초마다 다시 본다 · 봉인은 슬롯이 난 뒤)"; said=1; }
    sleep 30
  done
}

deckdiff() {  # 관문 — 실행 덱 LC_s* → LH_s* 허용 diff B (사전등록 §2-2 · Codex HB-03)
  echo "── 관문: 덱 비교 — python3 $DECKDIFF --runs $OUT --allow B"
  python3 "$DECKDIFF" --runs "$OUT" --allow B; local rc=$?
  [ "$rc" -eq 0 ] || { echo "⛔ 덱 비교 관문 실패 (종료 코드 $rc) — 발사 0"; return 1; }
}

seal() {  # seal <런> <first|rest> [증서] — 발사 직전 봉인 <OUT>/<런>/launch_record.json (임시 파일 → rename)
  local nm="$1" stage="$2" cert="${3:-}" d="$OUT/$1" lp head
  lp=$(command -v "$LMP") || { echo "⛔ $LMP 없음 — LMP=<실행파일>"; return 1; }
  head=$(git -C "$ROOT" rev-parse HEAD 2>/dev/null) || head=no-git
  #  fresh 인데 봉인이 있다 = 발사되지 않은 옛 봉인 — 지우지 않고 옆으로
  if [ -e "$d/launch_record.json" ]; then mv "$d/launch_record.json" "$d/launch_record.unlaunched.$(stamp).json" || return 1; fi
  python3 - "$d" "$stage" "$LMP" "$lp" "$head" "$(nproc)" "$MAXJ" "$(live)" "$DECKDIFF" "$OUT" "$cert" "$FIRST" "${REST[@]}" <<'PY'
import hashlib, json, os, platform, socket, sys, time
from datetime import datetime, timezone
d, stage, lmp, lmp_path, head, nproc, maxj, live, dd, out, cert, first, *rest = sys.argv[1:]
FILES = ('in.mixer', 'Drum.stl', 'Front.stl', 'Back.stl')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


nm, now = os.path.basename(d), time.time()
rec = {
    'schema': 'mixer_highbo_launch_record/1',
    'run': nm, 'seed': int(nm.rsplit('_s', 1)[1]), 'stage': stage,
    'time_local': datetime.fromtimestamp(now).astimezone().isoformat(timespec='seconds'),
    'time_utc': datetime.fromtimestamp(now, timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'hostname': socket.gethostname(), 'platform': platform.platform(),
    'nproc': int(nproc), 'maxj': int(maxj), 'live_at_seal': int(live),
    'lmp': lmp, 'lmp_path': lmp_path, 'lmp_realpath': os.path.realpath(lmp_path), 'lmp_sha256': sha(lmp_path),
    'sha256': {f: sha(os.path.join(d, f)) for f in FILES},
    'git_head': head,
    'gate_deckdiff': {'script': os.path.realpath(dd), 'script_sha256': sha(dd), 'argv': ['--runs', out, '--allow', 'B'], 'rc': 0},
}
if stage == 'first':      # 코호트 — rest 가 '첫 시드가 스모크를 받은 그 덱 · STL' 인지 대조한다 (바이너리는 lmp_sha256)
    rec['cohort'] = {n: {f: sha(os.path.join(out, n, f)) for f in FILES} for n in [first] + rest}
else:
    rec['smoke_certificate'] = {'path': os.path.realpath(cert), 'sha256': sha(cert)}
tmp = os.path.join(d, '.launch_record.json.tmp')
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(rec, f, ensure_ascii=False, indent=1)
    f.write('\n')
os.replace(tmp, os.path.join(d, 'launch_record.json'))
print(f"🔒 봉인 {nm}/launch_record.json — {rec['time_local']} · lmp {rec['lmp_sha256'][:12]}… · "
      f"in.mixer {rec['sha256']['in.mixer'][:12]}… · git {head[:12]}")
PY
}

launch_one() {  # launch_one <런> <first|rest> [증서] — 슬롯 → 봉인 → run_all.sh (ALLOW_LH=1 ONLY=<런>) → pid 확인
  local nm="$1" d="$OUT/$1"
  wait_slot
  seal "$@" || { echo "⛔ $nm: 봉인 실패 — 발사 0"; return 1; }
  OUT="$OUT" LMP="$LMP" MAXJ="$MAXJ" FORCE=0 ALLOW_LH=1 ONLY="$nm" bash "$HERE/run_all.sh"
  if [ -s "$d/pid" ]; then echo "▶ $nm 발사 확인 — pid $(cat "$d/pid") · 봉인 $d/launch_record.json"; return 0; fi
  mv "$d/launch_record.json" "$d/launch_record.unlaunched.$(stamp).json" 2>/dev/null
  echo "⛔ $nm: 발사되지 않았다 (위 run_all.sh 출력 확인) — 봉인은 launch_record.unlaunched.*.json 으로 옮겼다"; return 1
}

cmd_first() {
  [ $# -eq 0 ] || { usage; return 2; }
  echo "[LH first] OUT=$OUT · LMP=$LMP · MAXJ=$MAXJ (전 런 합산) — 사전등록 §8 (D-4): $FIRST 하나만"
  local nm bad=0
  command -v "$LMP" >/dev/null || { echo "⛔ $LMP 없음 — LMP=<실행파일>.  발사 0"; return 1; }
  for nm in "$FIRST" "${REST[@]}"; do
    [ -f "$OUT/$nm/in.mixer" ] || { echo "⛔ $OUT/$nm/in.mixer 없음 — 먼저 SET=highbo gen_all.sh"; bad=1; }
  done
  [ "$bad" = 0 ] || { echo "⛔ 발사 0"; return 1; }
  deckdiff || return 1                                               #  관문 1
  for nm in "$FIRST" "${REST[@]}"; do                                #  관문 2 — 세 시드 모두 아직 안 떴다
    fresh "$nm" || { echo "⛔ $nm 에 이미 log.lmp / pid 가 있다 — first 는 LH 세 시드가 모두 아직 안 떴을 때만 (§8 순서 · 재개는 resume_all.sh).  사람이 판단"; bad=1; }
  done
  [ "$bad" = 0 ] || { echo "⛔ 발사 0"; return 1; }
  launch_one "$FIRST" first || return 1
  echo "다음: bin 0 (첫 완전 바퀴) 이 끝나면 스모크 증서 (measure_mixing_index.py … --json <smoke.json>) → bash $HERE/launch_highbo.sh rest <smoke.json>"
}

cmd_rest() {
  [ $# -eq 1 ] && [ -n "$1" ] || { usage; return 2; }
  local cert="$1" nm lp k=0 todo=()
  echo "[LH rest] OUT=$OUT · LMP=$LMP · MAXJ=$MAXJ (전 런 합산) · 증서 $cert — 사전등록 §8 (D-4): ${REST[*]}"
  #  관문 0 — 첫 시드가 first 로 봉인 · 발사됐다 (순서)
  if [ ! -s "$OUT/$FIRST/launch_record.json" ] || [ ! -e "$OUT/$FIRST/log.lmp" ]; then
    echo "⛔ 첫 시드 $FIRST 가 'launch_highbo.sh first' 로 봉인 · 발사된 기록 (launch_record.json · log.lmp) 이 없다 — first 먼저.  발사 0"
    return 1
  fi
  lp=$(command -v "$LMP") || { echo "⛔ $LMP 없음 — LMP=<실행파일>.  발사 0"; return 1; }
  #  관문 1 — 스모크 증서 · 관문 2 — 코호트 (표준 라이브러리 python3 만)
  python3 - "$cert" "$OUT" "$FIRST" "$lp" "${REST[@]}" <<'PY' || { echo "⛔ 증서 · 코호트 관문 불합격 — 나머지 둘 발사 0"; return 1; }
import hashlib, json, os, sys
cert, out, first, lmp_path, *rest = sys.argv[1:]
FILES = ('in.mixer', 'Drum.stl', 'Front.stl', 'Back.stl')
bad = 0


def say(ok, msg):
    global bad
    print(('  ✓ ' if ok else '  ✗ ') + msg)
    bad += not ok


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def show(x):
    return json.dumps(x, ensure_ascii=False)


print(f'── 관문: 스모크 증서 (bin 0 · 사전등록 §8 ③ · D-4) — {cert}')
try:
    with open(cert, encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    say(False, f'증서 파일 없음: {cert}')
    sys.exit(1)
except (OSError, UnicodeDecodeError, ValueError) as e:
    say(False, f'증서를 읽을 수 없다 ({type(e).__name__}: {e})')
    sys.exit(1)
e = data[0] if isinstance(data, list) and data else None
if not isinstance(e, dict):
    say(False, '증서 모양 — measure_mixing_index.py --json 의 목록 [{run, smoke, …}] 이 아니다')
    sys.exit(1)
run = e.get('run')
rb = os.path.basename(os.path.normpath(run)) if isinstance(run, str) and run else None
say(rb == first, f'run = {rb} (목록의 첫 원소 · 기대 {first})')
sm = e.get('smoke')
if not isinstance(sm, dict):
    say(False, 'smoke 없음 — 스모크 창 (HBR2-02) 이 없는 판독기 판의 증서')
    sm = {}
c = sm.get('complete')
say(c is True, f'smoke.complete = {show(c)} (true 여야 — bin 0 계획 프레임 전부)')
t = sm.get('tech_smoke')
say(isinstance(t, list) and t == [], f'smoke.tech_smoke = {show(t)} ([] 여야)')
q = sm.get('qc_repr')
qp = q.get('pass') if isinstance(q, dict) else None
say(qp is True, f'smoke.qc_repr.pass = {show(qp)} (true 여야 — bin 0 부피 누락 QC)')
fs = os.path.join(out, first, 'launch_record.json')
try:
    with open(fs, encoding='utf-8') as f:
        fr = json.load(f)
except (OSError, ValueError) as e_:
    say(False, f'첫 시드 봉인을 읽을 수 없다 ({e_})')
    sys.exit(1)
say(fr.get('stage') == 'first' and fr.get('run') == first, f'첫 시드 봉인 = {first} · first 단계')
say(os.stat(cert).st_mtime_ns >= os.stat(fs).st_mtime_ns,
    '증서 시각 — 첫 시드 봉인 뒤에 만들어졌다 (다른 발사 · 옛 시험의 증서가 아니다)')
print('── 관문: 코호트 — 첫 시드 봉인 (first) 때의 덱 · STL · 바이너리 그대로인가')
co = fr.get('cohort') if isinstance(fr.get('cohort'), dict) else {}
for n in rest:
    want = co.get(n)
    if not isinstance(want, dict):
        say(False, f'{n}: 첫 봉인에 코호트 기록이 없다 (코호트 불일치)')
        continue
    changed = []
    for f_ in FILES:
        try:
            got = sha(os.path.join(out, n, f_))
        except OSError:
            got = None
        if got is None or got != want.get(f_):
            changed.append(f_)
    say(not changed, f'{n}: ' + ('in.mixer · Drum/Front/Back.stl sha256 = 첫 봉인 때' if not changed
                                 else f'첫 봉인 뒤에 바뀜 · 없음 — {", ".join(changed)} (코호트 불일치)'))
try:
    ls = sha(lmp_path)
except OSError as e_:
    ls = None
    print(f'     ({lmp_path}: {e_})')
say(ls is not None and ls == fr.get('lmp_sha256'),
    f'바이너리 sha256 {str(ls)[:12]}… {"=" if ls == fr.get("lmp_sha256") else "≠"} 첫 시드 {str(fr.get("lmp_sha256"))[:12]}…')
sys.exit(1 if bad else 0)
PY
  deckdiff || return 1                                               #  관문 3 — 덱 비교 (발사 직전 다시)
  for nm in "${REST[@]}"; do
    if fresh "$nm"; then todo+=("$nm")
    else echo "· $nm: 이미 log.lmp / pid 가 있다 — 건너뜀 (다시 띄우지 않고 봉인도 덮지 않는다 · 재개는 resume_all.sh)"; fi
  done
  for nm in "${todo[@]}"; do launch_one "$nm" rest "$cert" || return 1; k=$((k+1)); done
  echo "rest 끝 — 발사 $k 개 · 건너뜀 $(( ${#REST[@]} - ${#todo[@]} )) 개.  진행: bash $HERE/watch.sh"
}

case "${1:-}" in
  first) shift; cmd_first "$@"; exit $?;;
  rest)  shift; cmd_rest "$@"; exit $?;;
  *)     usage; exit 2;;
esac
