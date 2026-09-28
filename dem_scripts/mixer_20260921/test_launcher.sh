#!/usr/bin/env bash
# 런처·생성기 회귀 — 2026-09-22 사고 둘을 **재현해 놓고** 막는다 (LIGGGHTS 없이 돈다: 가짜 실행파일).
#   사고 ① 완주했는데 배너가 없는 런을 "죽음" 으로 읽고 재발사 → 로그·덤프 소실 (E0_s49979687)
#   사고 ② 실행 중인 런의 덱을 제자리 덮어쓰기 → EOF 자리에서 새 파일 바이트를 명령으로 읽음 (E0_s32452843)
#   + 2026-09-28 (Codex 3차 HBR3-08) 발사 순서 — LH 첫 시드 하나 → bin 0 스모크 증서 → 나머지 둘 (HL①–⑦)
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

echo "── gen_all.sh SET=highbo → 실행 덱 비교 (2026-09-27 고-Bo 확장 · Codex HB-03) ──"
H="$T/hb"; mkdir -p "$H"
#  짝 LC 덱 (본 캠페인과 같은 인자) 을 먼저 두고, SET=highbo 로 LH 만 만든 뒤 덱 비교 도구로 허용목록을 확인한다
for sd in 32452843 49979687 67867967; do
  python3 "$ROOT/scripts/make_mixer_deck.py" --out "$H/LC_s$sd" --n-total 100000 --cgf 151.4 --arm LC --seed "$sd" --revolutions 8 > /dev/null 2>&1
done
h1=$(OUT="$H" STL="$ROOT/dem_scripts/mixer_20260919" SET=highbo bash "$HERE/gen_all.sh" 2>&1)
chk 'H① SET=highbo 는 LH × 캠페인 시드 3 만 만든다 (L0 · E0 없음)' "[ \$(ls -d '$H'/LH_s*/ | wc -l) -eq 3 ] && ! ls -d '$H'/L0_s* '$H'/E0_s* >/dev/null 2>&1"
chk 'H①b LH 덱 옆에 n_expected · r_container (판독 계약)' "[ \"\$(cat '$H/LH_s32452843/n_expected')\" = 100000 ] && [ -s '$H/LH_s32452843/r_container' ]"
dd=$(python3 "$ROOT/scripts/mixer_deck_diff.py" --runs "$H" --allow B 2>&1); rc_dd=$?
chk 'H② ★ 실행 덱 LC_s* → LH_s* 세 시드: 허용 다섯 쌍 (AM–AM 셋 · AM–벽 둘) 만 다르다' "[ $rc_dd -eq 0 ] && grep -q '3/3 PASS' <<<\"\$dd\""
dd2=$(python3 "$ROOT/scripts/mixer_deck_diff.py" --runs "$H" --allow A 2>&1); rc_dd2=$?
chk 'H②b 같은 덱을 A (AM–AM 단독) 로 보면 거부 (AM–벽 이 허용목록 밖)' "[ $rc_dd2 -ne 0 ] && grep -q '0/3 PASS' <<<\"\$dd2\""
hx=$(OUT="$H" SET=bogus bash "$HERE/gen_all.sh" 2>&1); rc_hx=$?
chk 'H③ 모르는 SET 은 거부한다' "[ $rc_hx -ne 0 ] && grep -q 'main | highbo' <<<\"\$hx\""

echo "── resume_all.sh: 체크포인트 재개 (2026-09-26 — WSL 재시작으로 L 10 런이 53–61 % 에서 끊김) ──"
R="$T/rs"; mkdir -p "$R"
#  실물 생성기 덱 (LA) 으로 '회전 중 죽은' 런을 꾸민다: thermo 가 ckpt+5000 까지 있고 a (최신) · b 체크포인트
read -r EVERY THERMO CK < <(python3 - "$ROOT" "$R/proto.in" <<'PY'
import sys, importlib.util, re
spec = importlib.util.spec_from_file_location('m', sys.argv[1] + '/scripts/make_mixer_deck.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
dk = m.deck(m.plan(8000), rpm=75, revolutions=8, arm='LA'); open(sys.argv[2], 'w').write(dk)
runs = [int(x) for x in re.findall(r'^run (\d+)', dk, re.M)]; rot = sum(runs) - runs[-1]
every = int(re.search(r'^restart (\d+) ', dk, re.M).group(1)); th = int(re.search(r'^thermo (\d+)$', dk, re.M).group(1))
print(every, th, (rot // every + 2) * every)
PY
)
mkres() {  # mkres <이름> <마지막 thermo step> <배너 0/1>
  local d="$R/$1"; mkdir -p "$d/restart" "$d/post"; cp "$R/proto.in" "$d/in.mixer"
  for f in Drum Front Back; do echo "solid $f" > "$d/$f.stl"; done
  { echo "   Step Atoms KinEng c_rke Volume"
    for s in $((CK - THERMO)) "$CK" $((CK + THERMO)); do [ "$s" -le "$2" ] && printf '%12d %8d %s\n' "$s" 8000 "1.0e-06 1.0e-07 2.7e-05"; done
    [ "$3" = 1 ] && echo "Total wall time: 0:00:01"; } > "$d/log.lmp"
  head -c 5000 /dev/zero > "$d/restart/b.bin"; sleep 1; head -c 5000 /dev/zero > "$d/restart/a.bin"
  echo x > "$d/post/mix_$((CK + 1000)).liggghts"
}
mkres dead_s9 $((CK + THERMO)) 0
mkres banner_s9 $((CK + THERMO)) 1
mkres alive_s9 $((CK + THERMO)) 0; sleep 30 & SL2=$!; echo "$SL2" > "$R/alive_s9/pid"
mkres X_old_20260921_s9 $((CK + THERMO)) 0
mkdir -p "$R/fresh_s9"; cp "$R/proto.in" "$R/fresh_s9/in.mixer"
r1=$(OUT="$R" DRY=1 bash "$HERE/resume_all.sh" 2>&1)
chk 'R① DRY: 죽은 런만 in.resume — 체크포인트 = 최신 a · step ckpt'  "[ -f '$R/dead_s9/in.resume' ] && python3 -c \"import json,sys;r=json.load(open('$R/dead_s9/resume_receipt.json'));sys.exit(0 if r['checkpoint_file']=='restart/a.bin' and r['checkpoint_step']==$CK else 1)\""
chk 'R①b DRY: 완주(배너) · 실행 중 · 아직 안 돈 · _old_ 런은 건드리지 않는다' "! [ -f '$R/banner_s9/in.resume' ] && ! [ -f '$R/alive_s9/in.resume' ] && ! [ -f '$R/fresh_s9/in.resume' ] && ! [ -f '$R/X_old_20260921_s9/in.resume' ]"
chk 'R①c DRY: 띄우지 않는다 (pid 없음) · ckpt 뒤 덤프는 post_pre_resume_<ckpt>/ 로 (지우지 않음)' "! [ -f '$R/dead_s9/pid' ] && [ -f '$R/dead_s9/post_pre_resume_$CK/mix_$((CK + 1000)).liggghts' ]"
first=$(head -1 "$R/dead_s9/log.lmp")
FAKE_ARGS="$T/lmp_args"; printf '#!/usr/bin/env bash\necho "FAKE_ARGS $*"\nsleep 2\n' > "$FAKE_ARGS"; chmod +x "$FAKE_ARGS"
r2=$(OUT="$R" LMP="$FAKE_ARGS" MAXJ=8 ONLY=dead_s9 bash "$HERE/resume_all.sh" 2>&1)
sleep 3
chk 'R② 발사: pid = 실제 PID · -in in.resume 로 떴다'            "[ -s '$R/dead_s9/pid' ] && grep -q 'FAKE_ARGS -in in.resume' '$R/dead_s9/log.lmp'"
chk 'R②b ★ 로그는 이어 붙인다 — 옛 첫 줄 · 옛 thermo 가 그대로 · RESUME 표지' "[ \"\$(head -1 '$R/dead_s9/log.lmp')\" = \"$first\" ] && grep -qE '^ +$CK ' '$R/dead_s9/log.lmp' && grep -q '# ==== RESUME' '$R/dead_s9/log.lmp'"
chk 'R②c 사용 체크포인트를 복사 보존 (resume_from_<ckpt>.bin)'    "[ -f '$R/dead_s9/restart/resume_from_$CK.bin' ]"
kill "$SL2" 2>/dev/null
#  스모크 — 가짜 LIGGGHTS 가 RESUME_STEP 과 원 로그의 thermo 줄을 되찍으면 통과, 한 글자라도 다르면 실패
mkres smoke_s9 $((CK + THERMO)) 0
FS_OK="$T/lmp_smoke_ok"; FS_NG="$T/lmp_smoke_ng"
cat > "$FS_OK" <<'SH'
#!/usr/bin/env bash
c=$(python3 -c "import json;print(json.load(open('smoke_receipt.json'))['checkpoint_step'])")
s=$(python3 -c "import json;print(json.load(open('smoke_receipt.json'))['smoke_steps'])")
echo "RESUME_STEP $c"; grep -E "^ +$c " log.lmp | tail -1; grep -E "^ +$((c+s)) " log.lmp | tail -1
SH
sed 's/grep -E "^ +$c " log.lmp | tail -1;/printf "%12d %8d %s\\n" $c 8000 "9.9e-06 1.0e-07 2.7e-05";/' "$FS_OK" > "$FS_NG"
chmod +x "$FS_OK" "$FS_NG"
s_ok=$(OUT="$R" LMP="$FS_OK" SMOKE=smoke_s9 SMOKE_STEPS="$THERMO" SMOKE_DIR="$T/smk1" bash "$HERE/resume_all.sh" 2>&1); rc_ok=$?
s_ng=$(OUT="$R" LMP="$FS_NG" SMOKE=smoke_s9 SMOKE_STEPS="$THERMO" SMOKE_DIR="$T/smk2" bash "$HERE/resume_all.sh" 2>&1); rc_ng=$?
chk 'R③ 스모크: RESUME_STEP · 재개 직후 thermo 가 원 로그와 같으면 통과'   "[ $rc_ok -eq 0 ] && grep -q '스모크 통과' <<<\"\$s_ok\""
chk 'R③b 변이: 재개 직후 thermo 가 다르면 실패 (발사 금지)'              "[ $rc_ng -ne 0 ] && grep -q '스모크 실패' <<<\"\$s_ng\""
chk 'R③c 스모크는 원 폴더를 안 건드린다 (in.smoke · 영수증 · pid 없음)'   "! [ -f '$R/smoke_s9/in.smoke' ] && ! [ -f '$R/smoke_s9/smoke_receipt.json' ] && ! [ -f '$R/smoke_s9/pid' ]"

echo "── LH 발사 순서 — run_all.sh 관문 · launch_highbo.sh first / rest (2026-09-28, Codex 3차 HBR3-08) ──"
#  사전등록 §8 (D-4) = LH_s32452843 먼저 → bin 0 스모크 통과 → 나머지 둘.  그런데 §2-5 의 `MAXJ=3 run_all.sh` 는 미실행 _s* 를
#  전부 돌고 스모크를 안 읽으므로 LH 덱 셋을 **한꺼번에** 띄운다 (MAXJ=1 도 첫 런이 끝나면 다음을 띄울 뿐 판정을 안 기다린다).
LH1=LH_s32452843; LH2=LH_s49979687; LH3=LH_s67867967; LHL="$HERE/launch_highbo.sh"
FAKE_LH="$T/lmp_lh"; printf '#!/usr/bin/env bash\nsleep 15\n' > "$FAKE_LH"          # 오래 산다 — 상한 계산이 시각에 안 흔들리게
FAKE_LH2="$T/lmp_lh2"; printf '#!/usr/bin/env bash\n# 다른 빌드\nsleep 15\n' > "$FAKE_LH2"; chmod +x "$FAKE_LH" "$FAKE_LH2"
DD_OK="$T/dd_ok.py"; DD_NG="$T/dd_ng.py"          # 덱 비교기 대역 (DECKDIFF) — 통과 대역은 받은 인자를 $DD_ARGS 에 적는다
printf 'import os, sys\np = os.environ.get("DD_ARGS")\nif p: open(p, "a").write(" ".join(sys.argv[1:]) + "\\n")\nprint("3/3 PASS")\n' > "$DD_OK"
printf 'print("0/3 PASS  ⛔ 짝짓기 근거 없음 — 발사 금지")\nraise SystemExit(1)\n' > "$DD_NG"
mklh() {  # mklh <OUT> <이름> — 아직 안 돈 런 (덱 + STL 셋 + 판독 프레임 하나 — 내용에 전체 경로 = 폴더마다 다른 데이터)
  local d="$1/$2"; mkdir -p "$d/post"; printf 'run 1\nrun 10\n# %s\n' "$2" > "$d/in.mixer"
  for f in Drum Front Back; do echo "solid $f $2" > "$d/$f.stl"; done
  echo "frame $d" > "$d/post/mix_100.liggghts"
}
npid() { ls "$1"/*/pid 2>/dev/null | wc -l; }
mkcert() {  # mkcert <파일> <run 경로> <complete> <tech_smoke JSON> <qc_repr.pass> [cells] — measure_mixing_index.py --json 의 모양
  #  ★ HBR4-05 — 출처 블록은 **판독기의 같은 함수** (provenance_block) 로 만든다 (관문과 판독기가 형식을 따로 갖지 않게).
  #    그 폴더의 발사 봉인 · 덱 · 판독 프레임 · E0 기준을 **지금** 해시한다 — 그래서 first 뒤에 불러야 봉인 sha 가 맞는다.
  python3 - "$ROOT" "$@" <<'PY'
import json, os, sys
root, out, run, complete, tech, qc, *cells = sys.argv[1:]
sys.path.insert(0, os.path.join(root, 'scripts'))
from measure_mixing_index import provenance_block
rn = os.path.normpath(run)
ref = os.path.join(os.path.dirname(rn), 'E0_s32452843')
args = dict(cells=int(cells[0]) if cells else 16, x_cells=4, n_min=20, axis='x', r_container=0.013138)
pv = provenance_block(rn, ref, args, [(100, os.path.join(rn, 'post', 'mix_100.liggghts'))],
                      [(100, os.path.join(ref, 'post', 'mix_100.liggghts'))])
e = dict(run=run, ref=ref, provenance=pv,
         smoke=dict(bin=0, complete=json.loads(complete), tech_smoke=json.loads(tech), qc_repr={'pass': json.loads(qc)}))
json.dump([e], open(out, 'w'), ensure_ascii=False)
PY
}
cedit() {  # cedit <증서> <python 식 — e (첫 원소) 를 고친다> — 증서 JSON 한 칸 변이
  python3 - "$1" "$2" <<'PY'
import json, sys
p, code = sys.argv[1:]
d = json.load(open(p)); e = d[0]
exec(code)
json.dump(d, open(p, 'w'), ensure_ascii=False)
PY
}
#  (a) run_all.sh 는 LH 를 기본으로 건너뛴다
A="$T/hba"; for n in $LH1 $LH2 $LH3 L0_s11 E0_s12; do mklh "$A" $n; done
a1=$(OUT="$A" LMP="$FAKE" MAXJ=8 bash "$HERE/run_all.sh" 2>&1)
chk 'HL① ★ run_all.sh 기본: LH 덱 셋은 안 띄운다 (옆의 다른 런 둘은 띄운다) · 건너뜀을 찍고 새 런처를 가리킨다' \
    "! ls '$A'/LH_s*/pid >/dev/null 2>&1 && [ -s '$A/L0_s11/pid' ] && [ -s '$A/E0_s12/pid' ] && [ \$(grep -c 'LH 건너뜀' <<<\"\$a1\") -eq 3 ] && grep -q 'launch_highbo.sh first' <<<\"\$a1\""
a2=$(OUT="$A" LMP="$FAKE" MAXJ=8 ONLY="$LH1" bash "$HERE/run_all.sh" 2>&1)
a3=$(OUT="$A" LMP="$FAKE" MAXJ=8 ALLOW_LH=1 bash "$HERE/run_all.sh" 2>&1)
chk 'HL①b ONLY 만 · ALLOW_LH=1 만으로는 LH 를 안 띄운다 (둘 다 + 이름 목록 — launch_highbo.sh 만 그렇게 부른다)' \
    "! ls '$A'/LH_s*/pid >/dev/null 2>&1 && grep -q 'LH 건너뜀' <<<\"\$a2\" && [ \$(grep -c 'LH 건너뜀' <<<\"\$a3\") -eq 3 ]"
a4=$(OUT="$A" LMP="$FAKE" MAXJ=8 ALLOW_LH=1 ONLY="$LH1" bash "$HERE/run_all.sh" 2>&1); rc_a4=$?
chk 'HL①c ALLOW_LH=1 ONLY=<LH> 여도 봉인 (launch_record.json) 이 없으면 거부 — LH 는 봉인 뒤에만 뜬다' \
    "[ $rc_a4 -ne 0 ] && ! [ -e '$A/$LH1/pid' ] && grep -q '봉인 (launch_record.json) 이 없다' <<<\"\$a4\""
A2="$T/hba2"; mklh "$A2" $LH1; printf '    Step Atoms KinEng\n%12d %8d 0.0\n' 3 100 > "$A2/$LH1/log.lmp"
a5=$(OUT="$A2" LMP="$FAKE" MAXJ=8 FORCE=1 bash "$HERE/run_all.sh" 2>&1)
chk 'HL①d FORCE=1 이어도 죽은 LH 를 처음부터 다시 띄우지 않는다' "! [ -e '$A2/$LH1/pid' ] && grep -q 'LH 건너뜀' <<<\"\$a5\""
echo '{}' > "$A2/$LH1/launch_record.json"
a6=$(OUT="$A2" LMP="$FAKE" MAXJ=8 FORCE=1 ALLOW_LH=1 ONLY="$LH1" bash "$HERE/run_all.sh" 2>&1)
chk 'HL①e ALLOW_LH=1 ONLY=<LH> FORCE=1 · 봉인이 있어도 로그 있는 LH 는 처음부터 다시 안 띄운다 (재개는 resume_all.sh)' \
    "! [ -e '$A2/$LH1/pid' ] && grep -q 'LH 건너뜀 (로그 있음' <<<\"\$a6\""
#  (f) first 의 관문 — 덱 비교 · 세 시드 미발사
F="$T/hbf"; for n in $LH1 $LH2 $LH3; do mklh "$F" $n; done
f1=$(OUT="$F" LMP="$FAKE_LH" MAXJ=8 DECKDIFF="$DD_NG" bash "$LHL" first 2>&1); rc_f1=$?
chk 'HL② first: 덱 비교 관문 (mixer_deck_diff --allow B) 실패 → 거부 · 발사 0 · 봉인 0' \
    "[ $rc_f1 -ne 0 ] && [ \$(npid '$F') -eq 0 ] && ! ls '$F'/*/launch_record.json >/dev/null 2>&1 && grep -q '⛔ 덱 비교 관문 실패' <<<\"\$f1\""
echo x > "$F/$LH1/log.lmp"
f2=$(OUT="$F" LMP="$FAKE_LH" MAXJ=8 DECKDIFF="$DD_OK" bash "$LHL" first 2>&1); rc_f2=$?
chk 'HL②b first: 첫 시드에 로그가 이미 있으면 거부 (발사 0 · 봉인 0)' \
    "[ $rc_f2 -ne 0 ] && [ \$(npid '$F') -eq 0 ] && ! [ -e '$F/$LH1/launch_record.json' ] && grep -q '⛔ $LH1 에 이미' <<<\"\$f2\""
rm -f "$F/$LH1/log.lmp"; sleep 60 & SL3=$!; echo "$SL3" > "$F/$LH2/pid"
f3=$(OUT="$F" LMP="$FAKE_LH" MAXJ=8 DECKDIFF="$DD_OK" bash "$LHL" first 2>&1); rc_f3=$?
chk 'HL②c first: 나머지 시드가 이미 떠 있으면 거부 (§8 순서 위반 — 사람이 판단)' \
    "[ $rc_f3 -ne 0 ] && ! [ -e '$F/$LH1/pid' ] && ! [ -e '$F/$LH1/launch_record.json' ] && grep -q '⛔ $LH2 에 이미' <<<\"\$f3\""
kill "$SL3" 2>/dev/null
mkcert "$T/cert_f.json" "$F/$LH1" true '[]' true
f4=$(OUT="$F" LMP="$FAKE_LH" MAXJ=8 DECKDIFF="$DD_OK" bash "$LHL" rest "$T/cert_f.json" 2>&1); rc_f4=$?
chk 'HL②d rest 를 first 보다 먼저 부르면 거부 (첫 시드 봉인 · 로그 없음)' \
    "[ $rc_f4 -ne 0 ] && ! [ -e '$F/$LH3/pid' ] && ! [ -e '$F/$LH3/launch_record.json' ] && grep -q '⛔ 첫 시드' <<<\"\$f4\""
#  ★ HBR4-06 통합 (대역 없음) — 진짜 비교기 + 진짜 생성 덱.  LH 의 허용 다섯 CED 를 전부 두 배로 한 덱은 약한 호출
#    (--runs … --allow B) 을 통과하지만 (Codex launcher_target_without_expect) 런처는 거부해야 한다.  대조: 참 LH 덱은 통과.
DX="$T/hbx"; DY="$T/hby"
python3 - "$ROOT" "$DX" "$DY" <<'PY'
import os, sys
root, dx, dy = sys.argv[1:]
sys.path.insert(0, os.path.join(root, 'scripts'))
import mixer_deck_diff as dd
from make_mixer_resume import logical_commands, _tokens
import make_mixer_deck as gen


def doubled(txt):                  # Codex 4 차 프로브의 matrix_mutant 그대로 — seed · 비-CED 명령 유지, 허용 다섯 쌍만 ×2
    parsed = dd.parse_deck(txt)
    n, vals = parsed['ced']
    names = parsed['names']
    vv = list(vals)
    for i in range(n):
        for j in range(n):
            if tuple(sorted((names[i + 1], names[j + 1]))) in dd.ALLOW['B']:
                vv[i * n + j] *= 2
    out = []
    for _, blk in logical_commands(txt):
        t = _tokens(blk)
        if 'cohesionEnergyDensity' in t:
            ix = t.index('cohesionEnergyDensity')
            out.append(' '.join(t[:ix + 3] + [format(v, '.12g') for v in vv]))
        else:
            out.append('\n'.join(blk) if isinstance(blk, list) else blk)
    return '\n'.join(out) + '\n'


for base, mut in ((dx, True), (dy, False)):
    for sd in gen.CAMPAIGN_SEEDS:
        for arm in ('LC', 'LH'):
            d = os.path.join(base, f'{arm}_s{sd}')
            os.makedirs(os.path.join(d, 'post'))
            t = dd.expected_deck(arm, sd)
            open(os.path.join(d, 'in.mixer'), 'w').write(doubled(t) if (mut and arm == 'LH') else t)
            for f in ('Drum', 'Front', 'Back'):
                open(os.path.join(d, f + '.stl'), 'w').write(f'solid {f}\n')
PY
python3 "$ROOT/scripts/mixer_deck_diff.py" --runs "$DX" --allow B > /dev/null 2>&1; rc_weak=$?
x1=$(OUT="$DX" LMP="$FAKE_LH" MAXJ=8 bash "$LHL" first 2>&1); rc_x1=$?
chk 'HL②e ★ HBR4-06 재현→수정 (진짜 비교기): LH 허용 다섯 CED 를 두 배로 한 덱 — 약한 호출은 rc 0 인데 런처 first 는 거부 · 발사 0 · 봉인 0' \
    "[ $rc_weak -eq 0 ] && [ $rc_x1 -ne 0 ] && [ \$(npid '$DX') -eq 0 ] && ! ls '$DX'/*/launch_record.json >/dev/null 2>&1 && grep -q '⛔ 덱 비교 관문 실패' <<<\"\$x1\""
y1=$(OUT="$DY" LMP="$FAKE_LH" MAXJ=8 bash "$LHL" first 2>&1); rc_y1=$?
chk 'HL②f (대조 · 진짜 비교기) 참 LH 덱이면 덱 관문을 통과해 첫 시드 하나만 뜬다' \
    "[ $rc_y1 -eq 0 ] && [ \$(npid '$DY') -eq 1 ] && [ -s '$DY/$LH1/pid' ]"
#  (b) first = 정확히 하나 + 발사 전 봉인
B="$T/hbl"; for n in $LH1 $LH2 $LH3 LC_s32452843 E0_s32452843; do mklh "$B" $n; done
echo '{"stage": "first", "note": "발사 안 된 옛 봉인"}' > "$B/$LH1/launch_record.json"      # 끊긴 옛 시도가 남긴 것
b1=$(OUT="$B" LMP="$FAKE_LH" MAXJ=8 DECKDIFF="$DD_OK" DD_ARGS="$T/dd_args_b" bash "$LHL" first 2>&1); rc_b1=$?
chk 'HL③ ★ first: 정확히 하나 — LH_s32452843 만 뜬다 (나머지 LH 둘 · 같은 runs/ 의 LC · E0 는 안 뜬다)' \
    "[ $rc_b1 -eq 0 ] && [ \$(npid '$B') -eq 1 ] && [ -s '$B/$LH1/pid' ] && kill -0 \"\$(cat '$B/$LH1/pid')\""
chk 'HL③b ★ first: 덱 비교 관문을 --runs <OUT> --allow B **--expect-deck <기대 LH 덱>** 으로 불렀다 (HBR4-06)' \
    "grep -qE -- '^--runs $B --allow B --expect-deck .+/in\\.mixer\$' '$T/dd_args_b'"
sb=$(python3 - "$B/$LH1" "$FAKE_LH" "$ROOT" <<'PY' 2>&1
import hashlib, json, os, socket, subprocess, sys
d, fake, root = sys.argv[1:]
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
r = json.load(open(os.path.join(d, 'launch_record.json'), encoding='utf-8'))
g = subprocess.run(['git', '-C', root, 'rev-parse', 'HEAD'], capture_output=True, text=True)
head = g.stdout.strip() if g.returncode == 0 else 'no-git'
nproc = int(subprocess.run(['nproc'], capture_output=True, text=True).stdout)
ok = {'lmp': r.get('lmp_path') == fake and r.get('lmp_sha256') == sha(fake),
      'files': all(r.get('sha256', {}).get(f) == sha(os.path.join(d, f)) for f in ('in.mixer', 'Drum.stl', 'Front.stl', 'Back.stl')),
      'git': r.get('git_head') == head, 'host': r.get('hostname') == socket.gethostname(), 'nproc': r.get('nproc') == nproc,
      'time': bool(r.get('time_local')) and str(r.get('time_utc', '')).endswith('Z'),
      'who': r.get('run') == os.path.basename(d) and r.get('seed') == 32452843 and r.get('stage') == 'first',
      'before': os.stat(os.path.join(d, 'launch_record.json')).st_mtime_ns <= os.stat(os.path.join(d, 'pid')).st_mtime_ns}
sys.path.insert(0, os.path.join(root, 'scripts'))
import mixer_deck_diff as dd
g_ = r.get('gate_deckdiff') or {}
ok['gate'] = (g_.get('argv', [])[:5] == ['--runs', os.path.dirname(d), '--allow', 'B', '--expect-deck']
              and g_.get('expect_deck_sha256') == hashlib.sha256(dd.expected_deck('LH', 32452843).encode()).hexdigest())
print('OK' if all(ok.values()) else 'NG ' + ' '.join(k for k, v in ok.items() if not v))
PY
)
chk 'HL③c first: 발사 전 봉인 launch_record.json — 바이너리 · in.mixer · Drum/Front/Back.stl sha256 · git HEAD · 시각 (지역 · UTC) · 호스트 · nproc · LMP 경로 · '\
'덱 비교 관문의 기대 덱 sha256 (= expected_deck LH · HBR4-06)' "[ \"\$sb\" = OK ]"
chk 'HL③d first: 발사 안 된 옛 봉인은 지우지 않고 launch_record.unlaunched.*.json 으로 옆에 둔다' \
    "grep -q '발사 안 된 옛 봉인' '$B/$LH1'/launch_record.unlaunched.*.json"
#  (c) rest 의 증서 관문 — 어느 하나라도 틀리면 나머지 둘 발사 0
CE="$T/certs"; mkdir -p "$CE"
mkcert "$CE/complete.json" "$B/$LH1" false '[]' true
mkcert "$CE/tech.json"     "$B/$LH1" true '["bin 0 결손 1/26 프레임 (step [408000])"]' true
mkcert "$CE/run.json"      "$B/$LH2" true '[]' true
mkcert "$CE/qc.json"       "$B/$LH1" true '[]' false
mkcert "$CE/truthy.json"   "$B/$LH1" 1 '[]' true
echo '[{"run": ' > "$CE/garbage.json"
mkcert "$CE/old.json"      "$B/$LH1" true '[]' true; cedit "$CE/old.json" "e['provenance']['run']['launch_record_sha256'] = '0' * 64"
mkcert "$CE/grid.json"     "$B/$LH1" true '[]' true 2                                    # 2×2×1 이 아니라 2×2×4 — 등록 16×16×4 와 다른 칸
mkcert "$CE/tool.json"     "$B/$LH1" true '[]' true; cedit "$CE/tool.json" "e['provenance']['tool_sha256'] = 'f' * 64"
mkcert "$CE/noprov.json"   "$B/$LH1" true '[]' true; cedit "$CE/noprov.json" "e.pop('provenance')"
FO="$T/foreign"; mklh "$FO" $LH1; mklh "$FO" E0_s32452843; cp "$B/$LH1/launch_record.json" "$FO/$LH1/"
mkcert "$CE/foreign.json"  "$FO/$LH1" true '[]' true                                     # 다른 폴더 · 같은 이름 · 같은 봉인 사본 · 다른 데이터
rest_ng() {  # rest_ng <증서> — 거부 (rc ≠ 0) · 나머지 둘 발사 0 · 봉인 0 이면 참.  출력은 $RO
  local rc; RO=$(OUT="$B" LMP="$FAKE_LH" MAXJ=8 DECKDIFF="$DD_OK" bash "$LHL" rest "$1" 2>&1); rc=$?
  [ $rc -ne 0 ] && ! [ -e "$B/$LH2/pid" ] && ! [ -e "$B/$LH3/pid" ] && ! [ -e "$B/$LH2/launch_record.json" ] && ! [ -e "$B/$LH3/launch_record.json" ]
}
chk 'HL④ rest: 증서 파일이 없으면 거부 · 나머지 둘 발사 0'          "rest_ng '$CE/none.json' && grep -q '✗ 증서' <<<\"\$RO\""
chk 'HL④b rest: smoke.complete = false → 거부 · 발사 0'            "rest_ng '$CE/complete.json' && grep -q '✗ smoke.complete' <<<\"\$RO\""
chk 'HL④c rest: smoke.tech_smoke 가 비어 있지 않으면 거부 · 발사 0' "rest_ng '$CE/tech.json' && grep -q '✗ smoke.tech_smoke' <<<\"\$RO\""
chk 'HL④d rest: 증서의 run 이 첫 시드가 아니면 거부 · 발사 0'      "rest_ng '$CE/run.json' && grep -q '✗ run' <<<\"\$RO\""
chk 'HL④e rest: smoke.qc_repr.pass = false → 거부 · 발사 0'        "rest_ng '$CE/qc.json' && grep -q '✗ smoke.qc_repr.pass' <<<\"\$RO\""
chk 'HL④f rest: 깨진 JSON · true 가 아닌 참값 (complete: 1) 도 거부 · 발사 0' \
    "rest_ng '$CE/garbage.json' && rest_ng '$CE/truthy.json' && grep -q '✗ smoke.complete' <<<\"\$RO\""
chk 'HL④g ★ rest: 다른 (옛) 발사 봉인을 본 증서는 거부 · 발사 0 — mtime 이 아니라 봉인 sha256 으로 (HBR4-05)' \
    "rest_ng '$CE/old.json' && grep -q '✗ 증서가 본 발사 봉인' <<<\"\$RO\""
chk 'HL④h ★ HBR4-05 재현→수정: 등록과 다른 칸 규약의 증서는 거부 · 발사 0 (foreign_wrong_grid_smoke_gate 의 칸 쪽)' \
    "rest_ng '$CE/grid.json' && grep -q '✗ 판독 규약' <<<\"\$RO\""
chk 'HL④i ★ HBR4-05 재현→수정: 다른 폴더의 **실제** 판독 증서 (같은 run 이름 · 같은 봉인 사본) 는 첫 시드 프레임을 다시 해시하면 어긋나 거부 · 발사 0' \
    "rest_ng '$CE/foreign.json' && grep -q '✗ 판독 프레임' <<<\"\$RO\""
chk 'HL④j rest: 판독기 sha256 이 지금 리포의 판독기와 다르면 거부 · 발사 0' "rest_ng '$CE/tool.json' && grep -q '✗ 판독기 sha256' <<<\"\$RO\""
chk 'HL④k rest: 출처 블록이 없는 (옛 판독기) 증서는 거부 · 발사 0' "rest_ng '$CE/noprov.json' && grep -q '✗ provenance.schema' <<<\"\$RO\""
#  (d) rest = 합격 증서면 나머지 둘
mkcert "$CE/ok.json" "$B/$LH1/" true '[]' true        # 끝에 / — 판독기는 명령줄 경로를 그대로 적는다
d1=$(OUT="$B" LMP="$FAKE_LH" MAXJ=8 DECKDIFF="$DD_OK" DD_ARGS="$T/dd_args_d" bash "$LHL" rest "$CE/ok.json" 2>&1); rc_d1=$?
chk 'HL⑤ ★ rest: 증서 합격 → 나머지 둘만 정확히 뜬다 (LH 합계 3 · LC · E0 는 여전히 0)' \
    "[ $rc_d1 -eq 0 ] && [ -s '$B/$LH2/pid' ] && [ -s '$B/$LH3/pid' ] && [ \$(npid '$B') -eq 3 ]"
sd=$(python3 - "$B" "$CE/ok.json" <<'PY' 2>&1
import hashlib, json, os, sys
b, cert = sys.argv[1:]
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
ok = []
for n in ('LH_s49979687', 'LH_s67867967'):
    d = os.path.join(b, n)
    r = json.load(open(os.path.join(d, 'launch_record.json'), encoding='utf-8'))
    ok += [r.get('stage') == 'rest', r.get('run') == n, r.get('smoke_certificate', {}).get('sha256') == sha(cert),
           r.get('sha256', {}).get('in.mixer') == sha(os.path.join(d, 'in.mixer')),
           os.stat(os.path.join(d, 'launch_record.json')).st_mtime_ns <= os.stat(os.path.join(d, 'pid')).st_mtime_ns]
print('OK' if all(ok) else f'NG {ok}')
PY
)
chk 'HL⑤b rest: 둘 다 발사 전 봉인 (stage rest · 증서 sha256) · 덱 비교를 --expect-deck 과 함께 다시 불렀다' \
    "[ \"\$sd\" = OK ] && grep -qE -- '^--runs $B --allow B --expect-deck .+/in\\.mixer\$' '$T/dd_args_d'"
k2=$(cat "$B/$LH2/pid" "$B/$LH2/launch_record.json" "$B/$LH3/pid" "$B/$LH3/launch_record.json" | sha256sum)
d2=$(OUT="$B" LMP="$FAKE_LH" MAXJ=8 DECKDIFF="$DD_OK" bash "$LHL" rest "$CE/ok.json" 2>&1); rc_d2=$?
chk 'HL⑤c rest 를 다시 불러도 이미 뜬 둘은 다시 안 띄우고 봉인 · pid 를 안 덮는다 (발사 0)' \
    "[ $rc_d2 -eq 0 ] && [ \"\$(cat '$B/$LH2/pid' '$B/$LH2/launch_record.json' '$B/$LH3/pid' '$B/$LH3/launch_record.json' | sha256sum)\" = '$k2' ] && grep -q '발사 0 개' <<<\"\$d2\""
#  코호트 — 첫 발사 뒤 나머지 덱 · 바이너리가 바뀌면 거부
CO="$T/hbc"; for n in $LH1 $LH2 $LH3 E0_s32452843; do mklh "$CO" $n; done
OUT="$CO" LMP="$FAKE_LH" MAXJ=8 DECKDIFF="$DD_OK" bash "$LHL" first > /dev/null 2>&1
mkcert "$CE/ok_c.json" "$CO/$LH1" true '[]' true
cp "$CO/$LH2/in.mixer" "$T/lh2.bak"; echo '# 첫 발사 뒤에 바뀐 줄' >> "$CO/$LH2/in.mixer"
c1=$(OUT="$CO" LMP="$FAKE_LH" MAXJ=8 DECKDIFF="$DD_OK" bash "$LHL" rest "$CE/ok_c.json" 2>&1); rc_c1=$?
chk 'HL⑥ rest: 첫 발사 뒤 나머지 덱이 바뀌었으면 거부 (첫 시드 봉인의 코호트 대조) · 발사 0' \
    "[ $rc_c1 -ne 0 ] && ! [ -e '$CO/$LH2/pid' ] && ! [ -e '$CO/$LH3/pid' ] && grep -q '✗ $LH2.*코호트 불일치' <<<\"\$c1\""
cp "$T/lh2.bak" "$CO/$LH2/in.mixer"
c2=$(OUT="$CO" LMP="$FAKE_LH2" MAXJ=8 DECKDIFF="$DD_OK" bash "$LHL" rest "$CE/ok_c.json" 2>&1); rc_c2=$?
chk 'HL⑥b rest: 첫 시드와 다른 바이너리 (sha256) 면 거부 · 발사 0' \
    "[ $rc_c2 -ne 0 ] && ! [ -e '$CO/$LH2/pid' ] && ! [ -e '$CO/$LH3/pid' ] && grep -q '✗ 바이너리' <<<\"\$c2\""
#  (e) 전역 동시 상한 — LH 가 아닌 런 · 첫 시드도 함께 센다
E="$T/hbe"; for n in $LH1 $LH2 $LH3 L0_s21; do mklh "$E" $n; done
sleep 60 & SL4=$!; echo "$SL4" > "$E/L0_s21/pid"
e1=$(OUT="$E" LMP="$FAKE_LH" MAXJ=1 DECKDIFF="$DD_OK" timeout 5 bash "$LHL" first 2>&1); rc_e1=$?
chk 'HL⑦ ★ 전역 상한: 다른 런 하나가 살아 MAXJ=1 이 차 있으면 first 는 기다린다 (발사 0 · 봉인은 슬롯이 난 뒤)' \
    "[ $rc_e1 -eq 124 ] && ! [ -e '$E/$LH1/pid' ] && ! [ -e '$E/$LH1/launch_record.json' ] && grep -q '동시 상한 대기' <<<\"\$e1\""
E2="$T/hbe2"; for n in $LH1 $LH2 $LH3 L0_s22 E0_s32452843; do mklh "$E2" $n; done
OUT="$E2" LMP="$FAKE_LH" MAXJ=8 DECKDIFF="$DD_OK" bash "$LHL" first > /dev/null 2>&1
echo "$SL4" > "$E2/L0_s22/pid"; mkcert "$CE/ok_e.json" "$E2/$LH1" true '[]' true
e2=$(OUT="$E2" LMP="$FAKE_LH" MAXJ=3 DECKDIFF="$DD_OK" timeout 8 bash "$LHL" rest "$CE/ok_e.json" 2>&1); rc_e2=$?
chk 'HL⑦b ★ 전역 상한: rest 도 첫 시드 · 다른 런을 함께 센다 — MAXJ=3 에 둘이 살아 있으면 하나만 띄우고 기다린다' \
    "[ $rc_e2 -eq 124 ] && [ -s '$E2/$LH2/pid' ] && ! [ -e '$E2/$LH3/pid' ] && ! [ -e '$E2/$LH3/launch_record.json' ]"
kill "$SL4" 2>/dev/null

echo "── LH 발사 · SLURM 판 (2026-09-28 · 1저자 결정: ibb 20 코어 × 3) — 관문은 그대로 · 발사만 sbatch (HS①–⑦) ──"
#  가짜 sbatch · squeue · mpirun.  sbatch = 인자 · 제출 폴더 · 스크립트 사본을 적고 job id 를 준다 (SB_FAIL=1 이면 실패).
#  squeue = $SB_DIR/live 의 job id 를 "대기열에 있다" 로 · mpirun = 플래그와 -np N 을 건너뛰고 나머지를 그대로 실행.
SBIN="$T/sbin"; mkdir -p "$SBIN"
cat > "$SBIN/sbatch" <<'SH'
#!/usr/bin/env bash
[ "${SB_FAIL:-0}" = 1 ] && { echo "sbatch: error: Batch job submission failed" >&2; exit 1; }
n=$(( $(cat "$SB_DIR/n" 2>/dev/null || echo 900) + 1 )); echo "$n" > "$SB_DIR/n"
printf '%s\t%s\t%s\n' "$n" "$PWD" "$*" >> "$SB_DIR/calls"
cp "${@: -1}" "$SB_DIR/script_$n"
echo "$n"
SH
printf '#!/usr/bin/env bash\ncat "$SB_DIR/live" 2>/dev/null\nexit 0\n' > "$SBIN/squeue"
cat > "$SBIN/mpirun" <<'SH'
#!/usr/bin/env bash
echo "mpirun $*" >> "${MPI_LOG:-/dev/null}"
while [ $# -gt 0 ]; do case "$1" in -np) shift 2; break;; *) shift;; esac; done
exec "$@"
SH
chmod +x "$SBIN"/*
FAKE_MPI="$T/lmp_mpi_fake"; printf '#!/usr/bin/env bash\necho "LIGGGHTS (fake mpi build)"\necho "Total wall time: 0:00:00"\n' > "$FAKE_MPI"; chmod +x "$FAKE_MPI"
LMPR=$(readlink -f "$FAKE_MPI")
nsb() { [ -f "$1/calls" ] && wc -l < "$1/calls" || echo 0; }
slurm_first() {  # slurm_first <OUT> <SB_DIR> [추가 env …] — first (SLURM) 를 부르고 출력을 $SO 에
  local o="$1" sd="$2"; shift 2; mkdir -p "$sd"
  SO=$(env PATH="$SBIN:$PATH" SB_DIR="$sd" BACKEND=slurm OUT="$o" LMP="$FAKE_MPI" DECKDIFF="$DD_OK" "$@" bash "$LHL" first 2>&1); return $?
}
S="$T/hbs"; SD="$T/sbd"; for n in $LH1 $LH2 $LH3 LC_s32452843 E0_s32452843; do mklh "$S" $n; done
slurm_first "$S" "$SD"; rc_s1=$?; s1="$SO"
chk 'HS① ★ SLURM first: sbatch 정확히 한 번 — LH_s32452843 만 (그 런 폴더에서 제출 · jobid 기록 · pid 없음 · logs/ · 나머지 LH · LC · E0 제출 0)' \
    "[ $rc_s1 -eq 0 ] && [ \$(nsb '$SD') -eq 1 ] && [ \"\$(cut -f2 '$SD/calls')\" = '$S/$LH1' ] && [ \"\$(cat '$S/$LH1/jobid' 2>/dev/null)\" = 901 ] && ! ls '$S'/*/pid >/dev/null 2>&1 && ! [ -e '$S/$LH2/jobid' ] && [ -d '$S/$LH1/logs' ]"
RS="$S/$LH1/run_lh.sbatch"
chk 'HS①b 러너 = ibb 실물 형식 (docs/data/pure_se_*_20260927/run_pse_*.sh) — #SBATCH -n 20 ↔ mpirun --oversubscribe --bind-to none -np 20 짝 · qos cpu-60 · partition cpu · 5 일 · conda myenv · logs/ · 절대경로 바이너리 · 시작 대조가 mpirun 앞' \
    "grep -qx '#SBATCH --job-name=$LH1' '$RS' && grep -qxF '#SBATCH --output=logs/output_${LH1}_%j.out' '$RS' && grep -qx '#SBATCH --qos=cpu-60' '$RS' && grep -qx '#SBATCH --partition=cpu' '$RS' && grep -qx '#SBATCH -n 20' '$RS' && grep -qx '#SBATCH --time=5-00:00:00' '$RS' && grep -qx 'conda activate myenv' '$RS' && grep -qxF 'mpirun --oversubscribe --bind-to none -np 20 $LMPR -in in.mixer > log.lmp 2>&1' '$RS' && [ \"\$(grep -n 'start_check.py' '$RS' | cut -d: -f1)\" -lt \"\$(grep -n '^mpirun' '$RS' | cut -d: -f1)\" ]"
ss=$(python3 - "$S/$LH1" "$FAKE_MPI" "$HERE" <<'PY' 2>&1
import hashlib, json, os, sys
d, lmp, here = sys.argv[1:]
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
r = json.load(open(os.path.join(d, 'launch_record.json'), encoding='utf-8'))
sl = r.get('slurm') or {}
ok = {'backend': r.get('backend') == 'slurm', 'np': sl.get('np') == 20, 'flags': sl.get('mpirun_flags') == '--oversubscribe --bind-to none',
      'runner': sl.get('runner') == 'run_lh.sbatch' and sl.get('runner_sha256') == sha(os.path.join(d, 'run_lh.sbatch')),
      'check': sl.get('start_check_sha256') == sha(os.path.join(here, 'start_check.py')),
      'lmp': r.get('lmp_sha256') == sha(lmp) and r.get('lmp_realpath') == os.path.realpath(lmp),
      'files': all(r.get('sha256', {}).get(f) == sha(os.path.join(d, f)) for f in ('in.mixer', 'Drum.stl', 'Front.stl', 'Back.stl')),
      'before': os.stat(os.path.join(d, 'launch_record.json')).st_mtime_ns <= os.stat(os.path.join(d, 'jobid')).st_mtime_ns,
      'stage': r.get('stage') == 'first' and isinstance(r.get('cohort'), dict)}
print('OK' if all(ok.values()) else 'NG ' + ' '.join(k for k, v in ok.items() if not v))
PY
)
chk 'HS①c SLURM 봉인 — backend slurm · np 20 · mpirun 플래그 · 러너 · 시작 대조기 sha256 · 바이너리 · 덱 · STL · 코호트 · 제출 전 (봉인 mtime ≤ jobid)' "[ \"\$ss\" = OK ]"
slurm_first "$S" "$SD"; rc_s2=$?; s2="$SO"
chk 'HS② ★ 대기열에만 있는 첫 시드 (jobid 있음 · log.lmp 아직 없음) 는 "안 뜬 런" 이 아니다 — first 를 다시 불러도 거부 · 두 번째 sbatch 0' \
    "[ $rc_s2 -ne 0 ] && [ \$(nsb '$SD') -eq 1 ] && grep -q 'jobid' <<<\"\$s2\""
#  시작 대조 — 러너를 **실제로** 돌린다 (가짜 mpirun · 가짜 바이너리 · 없는 ~/.bashrc · 없는 conda 는 무해)
runr() {  # runr <런 폴더> [env …] — 러너 실행 → rc
  local d="$1"; shift
  ( cd "$d" && env HOME="$T/home" PATH="$SBIN:$PATH" MPI_LOG="$T/mpi.log" SLURM_JOB_ID=4242 "$@" bash run_lh.sbatch > "$T/runr.out" 2>&1 ); return $?
}
mkdir -p "$T/home"
runr "$S/$LH1" SLURM_NTASKS=20; rc_r1=$?
chk 'HS③ ★ 시작 대조 통과 → LIGGGHTS (가짜) 가 돈다 · log.lmp · job_start.json (ok · job id · ntasks 20 · 바이너리 · 러너 · 봉인 sha256)' \
    "[ $rc_r1 -eq 0 ] && grep -q 'fake mpi build' '$S/$LH1/log.lmp' && python3 -c \"import json,sys; j=json.load(open('$S/$LH1/job_start.json')); sys.exit(0 if j['ok'] is True and j['slurm_job_id']=='4242' and j['slurm_ntasks']==20 and j['schema']=='mixer_highbo_job_start/1' else 1)\""
tamper() {  # tamper <이름> <변이 명령 (그 런 폴더에서)> [runr env …] — 새로 first 한 런을 변이 → 러너 → 거부면 참
  local o="$T/hbt_$1" sd="$T/sbt_$1" mut="$2"; shift 2
  for n in $LH1 $LH2 $LH3 E0_s32452843; do mklh "$o" $n; done
  slurm_first "$o" "$sd" || return 1
  ( cd "$o/$LH1" && eval "$mut" ) || return 1
  runr "$o/$LH1" "$@"; local rc=$?
  [ "$rc" -eq 3 ] && ! [ -e "$o/$LH1/job_start.json" ] && ls "$o/$LH1"/job_start.refused.*.json >/dev/null 2>&1 && ! grep -q 'fake mpi build' "$o/$LH1/log.lmp" 2>/dev/null
}
chk 'HS③b 제출 뒤 덱이 바뀌면 시작 대조가 막는다 (exit 3 · LIGGGHTS 0 · job_start.refused.*.json)' "tamper deck 'echo \"# 제출 뒤 수정\" >> in.mixer' SLURM_NTASKS=20"
chk 'HS③c 제출 뒤 STL 이 바뀌면 막는다' "tamper stl 'echo x >> Drum.stl' SLURM_NTASKS=20"
chk 'HS③d SLURM_NTASKS ≠ 봉인 np (19 ≠ 20) 면 막는다' "tamper ntasks ':' SLURM_NTASKS=19"
chk 'HS③e SLURM 밖 (SLURM_NTASKS 없음) 에서 러너를 돌리면 막는다' "tamper noslurm ':'"
chk 'HS③f log.lmp 가 이미 있으면 (두 번째 시작) 막고 그 로그를 안 덮는다' "tamper twice 'echo 첫실행 > log.lmp' SLURM_NTASKS=20 && grep -qx 첫실행 '$T/hbt_twice/$LH1/log.lmp'"
chk 'HS③g 실행 중인 러너가 봉인한 러너와 다르면 (제출 뒤 러너 수정) 막는다' "tamper runner 'echo \"# 수정\" >> run_lh.sbatch' SLURM_NTASKS=20"
LMPC="$T/lmp_mpi_copy"; cp "$FAKE_MPI" "$LMPC"
tamper_bin() {
  local o="$T/hbt_bin" sd="$T/sbt_bin"; for n in $LH1 $LH2 $LH3 E0_s32452843; do mklh "$o" $n; done
  mkdir -p "$sd"; env PATH="$SBIN:$PATH" SB_DIR="$sd" BACKEND=slurm OUT="$o" LMP="$LMPC" DECKDIFF="$DD_OK" bash "$LHL" first > /dev/null 2>&1 || return 1
  echo '# 다시 빌드' >> "$LMPC"
  runr "$o/$LH1" SLURM_NTASKS=20; [ $? -eq 3 ] && ! grep -q 'fake mpi build' "$o/$LH1/log.lmp" 2>/dev/null
}
chk 'HS③h 제출 뒤 바이너리가 바뀌면 (sha256) 막는다' "tamper_bin"
#  rest (SLURM) — 첫 시드가 시작돼 log.lmp 가 있고 증서 합격이면 나머지 둘만 sbatch
mkcert "$CE/ok_s.json" "$S/$LH1" true '[]' true
echo 901 > "$SD/live"
s4=$(env PATH="$SBIN:$PATH" SB_DIR="$SD" BACKEND=slurm OUT="$S" LMP="$FAKE_MPI" DECKDIFF="$DD_OK" bash "$LHL" rest "$CE/ok_s.json" 2>&1); rc_s4=$?
chk 'HS④ ★ SLURM rest: 증서 합격 → 나머지 둘만 sbatch (합계 3 · 첫 시드 jobid 그대로) · 둘 다 stage rest 봉인 · 러너 · live_at_seal = 대기열의 첫 시드' \
    "[ $rc_s4 -eq 0 ] && [ \$(nsb '$SD') -eq 3 ] && [ -s '$S/$LH2/jobid' ] && [ -s '$S/$LH3/jobid' ] && [ \"\$(cat '$S/$LH1/jobid')\" = 901 ] && python3 -c \"import json,sys; r=json.load(open('$S/$LH2/launch_record.json')); sys.exit(0 if r['stage']=='rest' and r['backend']=='slurm' and r['live_at_seal']>=1 else 1)\" && [ -s '$S/$LH3/run_lh.sbatch' ]"
#  sbatch 실패 · sbatch 없음 · NP 바꾸기
SF="$T/hbsf"; for n in $LH1 $LH2 $LH3 E0_s32452843; do mklh "$SF" $n; done
slurm_first "$SF" "$T/sbf" SB_FAIL=1; rc_s5=$?
chk 'HS⑤ sbatch 실패 → 발사 0 (jobid 없음) · 봉인은 launch_record.unlaunched.*.json 으로 · 0 이 아닌 종료' \
    "[ $rc_s5 -ne 0 ] && ! [ -e '$SF/$LH1/jobid' ] && ! [ -e '$SF/$LH1/launch_record.json' ] && ls '$SF/$LH1'/launch_record.unlaunched.*.json >/dev/null 2>&1"
SN="$T/hbsn"; for n in $LH1 $LH2 $LH3; do mklh "$SN" $n; done
s6=$(env BACKEND=slurm OUT="$SN" LMP="$FAKE_MPI" DECKDIFF="$DD_OK" bash "$LHL" first 2>&1); rc_s6=$?
chk 'HS⑥ sbatch 가 없는 기계에서 BACKEND=slurm → 관문 전에 거부 (봉인 0)' \
    "[ $rc_s6 -ne 0 ] && ! [ -e '$SN/$LH1/launch_record.json' ] && grep -q 'sbatch' <<<\"\$s6\""
SP_="$T/hbsp"; for n in $LH1 $LH2 $LH3; do mklh "$SP_" $n; done
slurm_first "$SP_" "$T/sbp" NP=19; rc_s7=$?
chk 'HS⑦ NP=19 → #SBATCH -n 19 ↔ -np 19 짝 · 봉인 np 19' \
    "[ $rc_s7 -eq 0 ] && grep -qx '#SBATCH -n 19' '$SP_/$LH1/run_lh.sbatch' && grep -q -- '-np 19 ' '$SP_/$LH1/run_lh.sbatch' && python3 -c \"import json,sys; sys.exit(0 if json.load(open('$SP_/$LH1/launch_record.json'))['slurm']['np']==19 else 1)\""
s8=$(env BACKEND=slurm NP=0 OUT="$SN" LMP="$FAKE_MPI" bash "$LHL" first 2>&1); rc_s8=$?
chk 'HS⑦b NP 가 양의 정수가 아니면 거부 (봉인 0)' "[ $rc_s8 -ne 0 ] && ! [ -e '$SN/$LH1/launch_record.json' ]"

echo "test_launcher: $pass PASS / $fail FAIL"
[ "$fail" -eq 0 ]
