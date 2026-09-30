#!/usr/bin/env bash
# 런처·생성기 회귀 — 2026-09-22 사고 둘을 **재현해 놓고** 막는다 (LIGGGHTS 없이 돈다: 가짜 실행파일).
#   사고 ① 완주했는데 배너가 없는 런을 "죽음" 으로 읽고 재발사 → 로그·덤프 소실 (E0_s49979687)
#   사고 ② 실행 중인 런의 덱을 제자리 덮어쓰기 → EOF 자리에서 새 파일 바이트를 명령으로 읽음 (E0_s32452843)
#   + 2026-09-28 (Codex 3차 HBR3-08) 발사 순서 — LH 첫 시드 하나 → bin 0 스모크 증서 → 나머지 둘 (HL①–⑦)
#   + 2026-09-30 강성 축 새 단계 (DV · CF · CR — dev-e0 · dev-rot · confirm-first · confirm-rest · 시작 직전 관문 · 디스크 · run_all/resume 가드)
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
#  t0_step · plan = 판독기 JSON 의 같은 키 (HBR5-02 관문이 bin 0 창을 여기서 정한다) — 픽스처: t₀ 100 · 한 바퀴 100 step · 간격 100
#  ⇒ bin 0 = [100, 200) 의 격자 {100} = mklh 의 프레임 한 장
e = dict(run=run, ref=ref, provenance=pv, t0_step=100, plan=dict(steps_per_rev=100.0, dump_every=100, steps_total=900),
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
#  ★ HBR5-02 (Codex 5 차, 2026-09-28) — 옛 관문은 증서 목록 **안** 파일만 다시 해시했다 ⇒ 증서 뒤 bin 0 에 같은 step 의 복제를 넣어도
#    rc 0 인데 같은 폴더를 판독기로 재판독하면 24/25 · smoke.complete=false (재현 키 smoke_after_duplicate).  판독기와 **같은 파일 규칙**
#    (measure_bed_aspect.STEP_RE) 으로 지금 폴더의 bin 0 창과 E0 t₀ 를 다시 열거해 중복 · 격자 밖 · 결손 · 다른 파일을 막는다.
mkcert "$CE/ok5.json" "$B/$LH1" true '[]' true
cp "$B/$LH1/post/mix_100.liggghts" "$B/$LH1/post/copy_100.liggghts"
chk 'HL④l ★ HBR5-02 재현→수정: 증서 뒤 bin 0 에 같은 step 의 복제 (copy_100 · 바이트 동일) 를 넣으면 거부 · 발사 0' \
    "rest_ng '$CE/ok5.json' && grep -q '✗ bin 0 에 같은 step' <<<\"\$RO\""
rm -f "$B/$LH1/post/copy_100.liggghts"
echo "frame off-grid" > "$B/$LH1/post/mix_150.liggghts"
chk 'HL④m ★ HBR5-02: 증서 뒤 bin 0 창 안에 격자 밖 프레임 (step 150) 이 생기면 거부 · 발사 0' \
    "rest_ng '$CE/ok5.json' && grep -q '✗ bin 0 격자 밖' <<<\"\$RO\""
rm -f "$B/$LH1/post/mix_150.liggghts"
cp "$B/E0_s32452843/post/mix_100.liggghts" "$B/E0_s32452843/post/dup_100.liggghts"
chk 'HL④n ★ HBR5-02: E0 기준 t₀ step 의 덤프가 둘이면 거부 · 발사 0' \
    "rest_ng '$CE/ok5.json' && grep -q '✗ E0 기준 t₀' <<<\"\$RO\""
rm -f "$B/E0_s32452843/post/dup_100.liggghts"
rx=$(python3 - "$ROOT" "$LHL" <<'PY' 2>&1
import os, re, sys
root, lhl = sys.argv[1:]
sys.path.insert(0, os.path.join(root, 'scripts'))
import measure_bed_aspect as m
g = re.search(r"^STEP_RE = re\.compile\(r'([^']*)'\)", open(lhl, encoding='utf-8').read(), re.M)
print('OK' if g and g.group(1) == m.STEP_RE.pattern else f'NG {g and g.group(1)!r} vs {m.STEP_RE.pattern!r}')
PY
)
chk 'HL④o HBR5-02: rest 관문의 파일 규칙 = 판독기의 규칙 (measure_bed_aspect.STEP_RE — 한쪽만 바뀌면 여기서 걸린다)' "[ \"\$rx\" = OK ]"
#  (d) rest = 합격 증서면 나머지 둘
mkcert "$CE/ok.json" "$B/$LH1/" true '[]' true        # 끝에 / — 판독기는 명령줄 경로를 그대로 적는다
echo "frame bin1" > "$B/$LH1/post/mix_200.liggghts"   # ★ HBR5-02 대조 — 증서 뒤 **bin 1** 의 정상 프레임 추가는 막지 않는다
d1=$(OUT="$B" LMP="$FAKE_LH" MAXJ=8 DECKDIFF="$DD_OK" DD_ARGS="$T/dd_args_d" bash "$LHL" rest "$CE/ok.json" 2>&1); rc_d1=$?
chk 'HL⑤ ★ rest: 증서 합격 → 나머지 둘만 정확히 뜬다 (LH 합계 3 · LC · E0 는 여전히 0) · 증서 뒤 bin 1 프레임 추가는 통과 (HBR5-02 대조)' \
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
#  ★ HBR5-01 (Codex 5 차, 2026-09-28) — 문법적으로 정상인 **빈 / 비객체 봉인** ({} · null · [] · "invalid") 을 옛 시작 대조기는
#    rc 0 · ok=true 로 통과시켰다 (비객체 → 빈 dict · 주요 검사가 전부 `if lr and …`).  네 입력 모두 rc 3 · mpirun 호출 0 ·
#    job_start.json 없음 · 거부 영수증만 (재현 키 start_empty_dict / start_null / start_list / start_string).  정상 봉인 = HS③ 그대로 통과.
seal_as() {  # seal_as <empty|null|list|str> — 지금 폴더의 launch_record.json 을 문법상 정상인 빈 객체 / 비객체로 덮는다
  python3 - "$1" <<'PY'
import json, sys
json.dump({'empty': {}, 'null': None, 'list': [], 'str': 'invalid'}[sys.argv[1]], open('launch_record.json', 'w'))
PY
}
chk 'HS③i ★ HBR5-01 봉인이 빈 객체 {} 면 막는다 (rc 3 · mpirun 0 · 거부 영수증만)' \
    "tamper seal_empty 'seal_as empty' SLURM_NTASKS=20 MPI_LOG='$T/mpi_seal_empty.log' && ! [ -s '$T/mpi_seal_empty.log' ]"
chk 'HS③j ★ HBR5-01 봉인이 null 이면 막는다' \
    "tamper seal_null 'seal_as null' SLURM_NTASKS=20 MPI_LOG='$T/mpi_seal_null.log' && ! [ -s '$T/mpi_seal_null.log' ]"
chk 'HS③k ★ HBR5-01 봉인이 빈 목록 [] 이면 막는다' \
    "tamper seal_list 'seal_as list' SLURM_NTASKS=20 MPI_LOG='$T/mpi_seal_list.log' && ! [ -s '$T/mpi_seal_list.log' ]"
chk 'HS③l ★ HBR5-01 봉인이 문자열 "invalid" 면 막는다' \
    "tamper seal_str 'seal_as str' SLURM_NTASKS=20 MPI_LOG='$T/mpi_seal_str.log' && ! [ -s '$T/mpi_seal_str.log' ]"
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

echo "── LH all · 저자 편차 (09-28 밤: 세 시드 × 20 코어 동시 · bin 0 스모크 관문 생략 — §8 D-4 이탈) (HA①–⑦) ──"
#  all = first 의 관문 (덱 비교 · 세 시드 모두 안 뜸) 그대로 + DEVIATION 문구 필수 + SLURM 판 전용 → 세 시드를 순서대로 봉인 · 제출.
#  봉인 stage = 'all' · deviation = {author_decision: DEVIATION, skipped_gate …} · 코호트 · 증서 없음.  all 뒤의 rest 는 발사 0.
DEV='1저자 결정 2026-09-28 밤 — 세 시드 동시 (bin 0 스모크 관문 생략)'
#  ★ 발사 정책 (09-29): 리포 기본 정책은 first · rest 만 — all 시험은 all 을 허용하는 시험용 정책 파일을 꽂는다 (HA⑧ 은 기본 정책으로 거부를 본다)
PALL="$T/policy_all.json"
python3 - "$PALL" <<'PY'
import json, sys
json.dump({"schema": "mixer_highbo_launch_policy/1", "policy_id": "TEST-all-allowed", "allowed_stages": ["first", "rest", "all"]}, open(sys.argv[1], "w"), ensure_ascii=False)
PY
slurm_all() {  # slurm_all <OUT> <SB_DIR> [추가 env …] — all (SLURM · all 허용 시험 정책) → 출력 $SO
  local o="$1" sd="$2"; shift 2; mkdir -p "$sd"
  SO=$(env PATH="$SBIN:$PATH" SB_DIR="$sd" BACKEND=slurm OUT="$o" LMP="$FAKE_MPI" DECKDIFF="$DD_OK" POLICY_FILE="$PALL" "$@" bash "$LHL" all 2>&1); return $?
}
A0="$T/hba0"; for n in $LH1 $LH2 $LH3 E0_s32452843; do mklh "$A0" $n; done
slurm_all "$A0" "$T/sba0"; rc_a0=$?
chk 'HA① DEVIATION 없이 all → 거부 · sbatch 0 · 봉인 0' \
    "[ $rc_a0 -ne 0 ] && [ \$(nsb '$T/sba0') -eq 0 ] && ! ls '$A0'/*/launch_record.json >/dev/null 2>&1 && grep -q 'DEVIATION' <<<\"\$SO\""
A1="$T/hba1"; SA="$T/sba1"; for n in $LH1 $LH2 $LH3 LC_s32452843 E0_s32452843; do mklh "$A1" $n; done
slurm_all "$A1" "$SA" DEVIATION="$DEV"; rc_a1=$?; a1="$SO"
chk 'HA② ★ all (DEVIATION): sbatch 정확히 세 번 — LH 세 시드만, 순서대로 (각 런 폴더에서 · jobid 901 · 902 · 903 · LC · E0 제출 0)' \
    "[ $rc_a1 -eq 0 ] && [ \$(nsb '$SA') -eq 3 ] && [ \"\$(cut -f2 '$SA/calls' | tr '\n' ' ')\" = '$A1/$LH1 $A1/$LH2 $A1/$LH3 ' ] && [ \"\$(cat '$A1/$LH1/jobid' '$A1/$LH2/jobid' '$A1/$LH3/jobid' | tr '\n' ' ')\" = '901 902 903 ' ] && ! [ -e '$A1/LC_s32452843/jobid' ] && ! [ -e '$A1/E0_s32452843/jobid' ]"
sa=$(PALL="$PALL" python3 - "$A1" "$DEV" "$LH1" "$LH2" "$LH3" <<'PY' 2>&1
import hashlib, json, os, sys
out, dev, *runs = sys.argv[1:]
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
bad = []
for n in runs:
    d = os.path.join(out, n)
    r = json.load(open(os.path.join(d, 'launch_record.json'), encoding='utf-8'))
    dv = r.get('deviation') or {}
    ok = {'stage': r.get('stage') == 'all', 'dev': dv.get('author_decision') == dev,
          'skip': 'bin 0' in str(dv.get('skipped_gate', '')) and 'D-4' in str(dv.get('registered_order', '')),
          'cohort': sorted((r.get('cohort') or {}).keys()) == sorted(runs),
          'nocert': 'smoke_certificate' not in r,
          'slurm': (r.get('slurm') or {}).get('np') == 20 and (r.get('slurm') or {}).get('runner_sha256') == sha(os.path.join(d, 'run_lh.sbatch')),
          'files': all(r.get('sha256', {}).get(f) == sha(os.path.join(d, f)) for f in ('in.mixer', 'Drum.stl', 'Front.stl', 'Back.stl')),
          'policy': (r.get('policy') or {}).get('policy_id') == 'TEST-all-allowed' and (r.get('policy') or {}).get('sha256') == sha(os.environ['PALL'])
                    and 'all' in ((r.get('policy') or {}).get('allowed_stages') or [])}
    bad += [f'{n}:{k}' for k, v in ok.items() if not v]
print('OK' if not bad else 'NG ' + ' '.join(bad))
PY
)
chk 'HA③ 세 봉인 모두 stage all · deviation (저자 결정 문구 · 생략한 관문 bin 0 · 등록 순서 §8 D-4) · 코호트 세 시드 · 증서 없음 · np 20 · 러너 · 덱/STL sha256 · ★ 정책 (id · sha256 · all 허용)' "[ \"\$sa\" = OK ]"
A8="$T/hba8"; for n in $LH1 $LH2 $LH3 E0_s32452843; do mklh "$A8" $n; done
a8=$(env PATH="$SBIN:$PATH" SB_DIR="$T/sba8" BACKEND=slurm OUT="$A8" LMP="$FAKE_MPI" DECKDIFF="$DD_OK" DEVIATION="$DEV" bash "$LHL" all 2>&1); rc_a8=$?
chk 'HA⑧ ★ 기본 정책 (리포 launch_policy.json = first · rest) 에서는 DEVIATION 이 있어도 all 거부 · sbatch 0 · 봉인 0 (Codex 6 차 §7-2 — 옛 DEVIATION 만으로 안 열린다)' \
    "[ $rc_a8 -ne 0 ] && [ \$(nsb '$T/sba8') -eq 0 ] && ! ls '$A8'/*/launch_record.json >/dev/null 2>&1 && grep -q '발사 정책' <<<\"\$a8\" && grep -q \"'all'\" <<<\"\$a8\""
PBAD="$T/policy_bad.json"; echo '{"schema": "x"}' > "$PBAD"
a8b=$(env PATH="$SBIN:$PATH" SB_DIR="$T/sba8b" BACKEND=slurm OUT="$A8" LMP="$FAKE_MPI" DECKDIFF="$DD_OK" DEVIATION="$DEV" POLICY_FILE="$PBAD" bash "$LHL" all 2>&1); rc_a8b=$?
a8c=$(env PATH="$SBIN:$PATH" SB_DIR="$T/sba8c" BACKEND=slurm OUT="$A8" LMP="$FAKE_MPI" DECKDIFF="$DD_OK" POLICY_FILE="$T/no_such_policy.json" bash "$LHL" first 2>&1); rc_a8c=$?
chk 'HA⑧b 정책 파일 모양 아님 → all 거부 / 정책 파일 없음 → first 도 거부 (fail-closed · sbatch 0)' \
    "[ $rc_a8b -ne 0 ] && [ $rc_a8c -ne 0 ] && [ \$(nsb '$T/sba8b') -eq 0 ] && [ \$(nsb '$T/sba8c') -eq 0 ] && grep -q '모양' <<<\"\$a8b\" && grep -q '읽을 수 없다' <<<\"\$a8c\""
runr "$A1/$LH2" SLURM_NTASKS=20; rc_a4=$?
chk 'HA④ all 로 봉인한 런의 러너도 시작 대조를 통과 → LIGGGHTS (가짜) · job_start.json ok' \
    "[ $rc_a4 -eq 0 ] && grep -q 'fake mpi build' '$A1/$LH2/log.lmp' && python3 -c \"import json,sys; sys.exit(0 if json.load(open('$A1/$LH2/job_start.json'))['ok'] is True else 1)\""
mkcert "$CE/ok_a.json" "$A1/$LH1" true '[]' true
runr "$A1/$LH1" SLURM_NTASKS=20 >/dev/null 2>&1
a5=$(env PATH="$SBIN:$PATH" SB_DIR="$SA" BACKEND=slurm OUT="$A1" LMP="$FAKE_MPI" DECKDIFF="$DD_OK" bash "$LHL" rest "$CE/ok_a.json" 2>&1); rc_a5=$?
chk 'HA⑤ all 뒤의 rest → 발사 0 (첫 봉인 stage 가 first 가 아니다 · sbatch 합계 3 그대로)' "[ $rc_a5 -ne 0 ] && [ \$(nsb '$SA') -eq 3 ]"
A6="$T/hba6"; for n in $LH1 $LH2 $LH3; do mklh "$A6" $n; done; echo 777 > "$A6/$LH3/jobid"
slurm_all "$A6" "$T/sba6" DEVIATION="$DEV"; rc_a6=$?
chk 'HA⑥ 한 시드라도 이미 떴으면 (jobid) all 거부 · sbatch 0 · 봉인 0' \
    "[ $rc_a6 -ne 0 ] && [ \$(nsb '$T/sba6') -eq 0 ] && ! ls '$A6'/*/launch_record.json >/dev/null 2>&1"
A7="$T/hba7"; for n in $LH1 $LH2 $LH3; do mklh "$A7" $n; done
slurm_all "$A7" "$T/sba7" DEVIATION="$DEV" DECKDIFF="$DD_NG"; rc_a7=$?
a7l=$(env OUT="$A7" LMP="$FAKE_MPI" DECKDIFF="$DD_OK" DEVIATION="$DEV" bash "$LHL" all 2>&1); rc_a7l=$?
chk 'HA⑦ 덱 비교 관문 실패 → sbatch 0 · 봉인 0 / BACKEND=local 의 all → 거부 (SLURM 판 전용)' \
    "[ $rc_a7 -ne 0 ] && [ \$(nsb '$T/sba7') -eq 0 ] && ! ls '$A7'/*/launch_record.json >/dev/null 2>&1 && [ $rc_a7l -ne 0 ] && ! ls '$A7'/*/launch_record.json >/dev/null 2>&1"

echo "── watch.sh · SLURM 런 (pid 없음 · jobid) — 09-28 밤 (HW①–②) ──"
W="$T/wat"; mkdir -p "$T/sbw"; for n in $LH1 $LH2; do mklh "$W" $n; printf 'run 1\nrun 100000\n' > "$W/$n/in.mixer"; printf '      1000   100000 0.1 0.2\n' > "$W/$n/log.lmp"; done   # 1000 < 100001 = 진행 중
echo 555 > "$W/$LH1/jobid"; echo 556 > "$W/$LH2/jobid"; echo 555 > "$T/sbw/live"
wo=$(env PATH="$SBIN:$PATH" SB_DIR="$T/sbw" OUT="$W" bash "$HERE/watch.sh" 2>&1)
chk 'HW① SLURM 런 — jobid 가 대기열 (squeue) 에 있으면 실행 (pid 가 없다고 ⛔죽음 으로 찍지 않는다)' "grep -E '^$LH1 +실행' <<<\"\$wo\" >/dev/null"
chk 'HW② jobid 가 대기열에 없고 완주도 아니면 ⛔죽음 (SLURM 판도 죽은 런은 죽었다고 찍는다)' "grep -E '^$LH2 +⛔죽음' <<<\"\$wo\" >/dev/null"
echo "── 강성 축 새 단계 (2026-09-30 · 사전등록 mixer_highbo_stiffness_prereg_20260929 §8-2 · 코드 2 단계 piece 1 · 5) — DV · CF · CR ──"
#  ★ 반례를 먼저 옮겼다 — 옛 런처에는 dev-e0 · dev-rot · confirm-first · confirm-rest 가 없다 (usage rc 2) · 정책 v2 를 '모양 아님' 으로 거부 ·
#    run_all.sh 가 강성 축 셀을 로컬로 띄운다 (LH_* 만 막았다).  가짜 sbatch (--hold 기록) · squeue (-j 상태 조회) · scontrol · df · mpirun.
SB2="$T/sbin2"; mkdir -p "$SB2"
cat > "$SB2/sbatch" <<'SH'
#!/usr/bin/env bash
n=$(( $(cat "$SB_DIR/n" 2>/dev/null || echo 900) + 1 ))
if [ -n "${SB_FAIL_AT:-}" ] && [ "$n" -ge "$SB_FAIL_AT" ]; then echo "sbatch: error: fake failure" >&2; exit 1; fi
echo "$n" > "$SB_DIR/n"
printf '%s\t%s\t%s\n' "$n" "$PWD" "$*" >> "$SB_DIR/calls"
cp "${@: -1}" "$SB_DIR/script_$n"
case " $* " in *" --hold "*) echo "$n|PENDING|JobHeldUser" >> "$SB_DIR/state";; *) echo "$n|PENDING|None" >> "$SB_DIR/state";; esac
echo "$n"
SH
cat > "$SB2/squeue" <<'SH'
#!/usr/bin/env bash
ids=""
while [ $# -gt 0 ]; do case "$1" in -j) ids="$2"; shift 2;; *) shift;; esac; done
if [ -n "$ids" ]; then
  IFS=, read -ra A <<< "$ids"
  for i in "${A[@]}"; do l=$(grep "^$i|" "$SB_DIR/state" 2>/dev/null | tail -1); [ -n "$l" ] && echo "$l"; done
else
  cut -d'|' -f1 "$SB_DIR/state" 2>/dev/null | sort -u
fi
exit 0
SH
cat > "$SB2/scontrol" <<'SH'
#!/usr/bin/env bash
echo "scontrol $*" >> "$SB_DIR/scontrol_calls"
[ "${SC_FAIL:-0}" = 1 ] && { echo "scontrol: error: fake failure" >&2; exit 1; }
[ "$1" = release ] || exit 0
IFS=, read -ra A <<< "$2"
for i in "${A[@]}"; do echo "$i|PENDING|None" >> "$SB_DIR/state"; done
exit 0
SH
cat > "$SB2/df" <<'SH'
#!/usr/bin/env bash
echo "Filesystem 1-blocks Used Available Capacity Mounted on"
echo "fakefs 999999999999999999 0 ${DF_AVAIL:-1000000000000000} 0% /"
SH
cp "$SBIN/mpirun" "$SB2/mpirun"; chmod +x "$SB2"/*
nsb2() { [ -f "$1/calls" ] && wc -l < "$1/calls" || echo 0; }
nsc() { [ -f "$1/scontrol_calls" ] && wc -l < "$1/scontrol_calls" || echo 0; }
stg() {  # stg <OUT> <SB_DIR> <단계> [인자] [-- env …] — 새 단계 (SLURM · 가짜 기계) → 출력 $SO
  local o="$1" sd="$2" st="$3"; shift 3; local args=() envs=()
  while [ $# -gt 0 ]; do if [ "$1" = -- ]; then shift; envs=("$@"); break; fi; args+=("$1"); shift; done
  mkdir -p "$sd"
  SO=$(env PATH="$SB2:$PATH" SB_DIR="$sd" BACKEND=slurm OUT="$o" LMP="$FAKE_MPI" "${envs[@]}" bash "$LHL" "$st" "${args[@]}" 2>&1); return $?
}
runr2() {  # runr2 <런 폴더> [env …] — 러너 (시작 대조 → 가짜 mpirun → 가짜 lmp) → rc
  local d="$1"; shift
  ( cd "$d" && env HOME="$T/home" PATH="$SB2:$PATH" MPI_LOG="$T/mpi2.log" SLURM_JOB_ID=5151 "$@" bash run_lh.sbatch > "$T/runr2.out" 2>&1 ); return $?
}
fx() {  # fx <python 본문> [인자 …] — scripts/mixer_stage_gate.py 의 합성 고정물 (_fx_*) 을 부른다
  local code="$1"; shift
  python3 - "$ROOT" "$@" <<PY
import sys, os, json
sys.path.insert(0, os.path.join(sys.argv[1], 'scripts'))
import mixer_stage_gate as sg
import mixer_deck_diff as dd
A = sys.argv[2:]
$code
PY
}
PCF="$T/policy_cf.json"                                                    # 확인 두 단계를 허용하는 시험용 정책 (리포 정책 = dev 까지만)
python3 - "$HERE/launch_policy.json" "$PCF" <<'PY'
import json, sys
p = json.load(open(sys.argv[1], encoding='utf-8'))
p['allowed_stages'] = p['allowed_stages'] + ['confirm-first', 'confirm-rest']
p['policy_id'] = 'TEST-confirm-allowed'
json.dump(p, open(sys.argv[2], 'w'), ensure_ascii=False)
PY

#  (DV) dev-e0 — 리포 정책 (dev 허용) · 진짜 덱 비교기 · 진짜 관문
DV="$T/dv"; fx 'for n in list(dd.DEV_E0) + list(dd.DEV_ROT): sg._fx_cell(A[0], n)' "$DV"
stg "$DV" "$T/sdv" dev-e0; rc_dv1=$?; dv1="$SO"
chk 'DV① ★ dev-e0: sbatch 정확히 8 — NP 프로브 셋 (npprobe5/10/20 · 같은 덱 · -n 5/10/20 · 1 h) 먼저 + E0 다섯 (-n 20 · 정책 시간) · --hold 없음 · 회전 2 런 · 확인 셀 제출 0' \
    "[ $rc_dv1 -eq 0 ] && [ \$(nsb2 '$T/sdv') -eq 8 ] && ! grep -q -- '--hold' '$T/sdv/calls' && grep -qx '#SBATCH -n 5' '$DV/npprobe5_E0_ref_s32452843/run_lh.sbatch' && grep -qx '#SBATCH --time=01:00:00' '$DV/npprobe20_E0_ref_s32452843/run_lh.sbatch' && grep -qx '#SBATCH -n 20' '$DV/E0_ref2_s32452843/run_lh.sbatch' && ! [ -e '$DV/LC_ref_r2_s32452843/jobid' ] && cmp -s '$DV/npprobe10_E0_ref_s32452843/in.mixer' '$DV/E0_ref_s32452843/in.mixer'"
sdv=$(python3 - "$DV" "$ROOT" <<'PY' 2>&1
import hashlib, json, os, sys
out, root = sys.argv[1:]
sys.path.insert(0, os.path.join(root, 'scripts'))
import mixer_deck_diff as dd
bad = []
for n, blk in [(n, 'dev') for n in dd.DEV_E0] + [(n, 'probe') for n in dd.DEV_PROBES]:
    r = json.load(open(os.path.join(out, n, 'launch_record.json'), encoding='utf-8'))
    g = r.get('gate_deckdiff') or {}
    ok = {'stage': r.get('stage') == 'dev-e0', 'block': r.get('block') == blk, 'cell': (r.get('cell') or {}).get('name') == dd.parse_run(n)['name'],
          'gate': g.get('argv') == ['--runs', os.path.realpath(out), '--cohort', 'dev-e0']
                  and g.get('expect_deck_sha256') == hashlib.sha256(dd.cell_expected_deck(n).encode()).hexdigest(),
          'pre': (r.get('stage_gate') or {}).get('preflight', {}).get('sha256') is not None,
          'policy': (r.get('policy') or {}).get('policy_id', '').startswith('STIFF-'), 'np': (r.get('slurm') or {}).get('np') == (20 if blk == 'dev' else int(n[7:n.index('_')])),
          'disk': (r.get('disk_estimate') or {}).get('frames') == {'E0_ref_s32452843': 1037, 'E0_ref2_s32452843': 1467}.get(n, (r.get('disk_estimate') or {}).get('frames')),
          'probe': (('probe' in r) == (blk == 'probe')), 'no_legacy': 'cohort' not in r and 'deviation' not in r}
    bad += [f'{n}:{k}' for k, v in ok.items() if not v]
print('OK' if not bad else 'NG ' + ' '.join(bad))
PY
)
chk 'DV①b dev-e0 봉인 — stage dev-e0 · block (dev / probe) · cell · 덱 관문 = --cohort dev-e0 · 기대 덱 sha256 (이름에서 재생성) · preflight sha · 새 정책 id · np (프로브 = 5/10/20) · 디스크 추정 (E0_ref 867 · ×28 1,227 프레임) · probe 표지' "[ \"\$sdv\" = OK ]"
DV2="$T/dv2"; fx 'for n in dd.DEV_E0: sg._fx_cell(A[0], n)
open(os.path.join(A[0], "E0_ref_s49979687", "in.mixer"), "w").write(dd.cell_expected_deck("E0_ref_s15485863"))' "$DV2"
stg "$DV2" "$T/sdv2" dev-e0; rc_dv2=$?
chk 'DV② ★ DEV 폴더에 holdout seed 덱 (E0_ref_s49979687 ← E0_ref_s15485863 덱) → 덱 코호트 관문 거부 · sbatch 0 · 봉인 0' \
    "[ $rc_dv2 -ne 0 ] && [ \$(nsb2 '$T/sdv2') -eq 0 ] && ! ls '$DV2'/*/launch_record.json >/dev/null 2>&1 && grep -q '덱 코호트 관문 실패' <<<\"\$SO\""
PDV="$T/policy_dv_bad.json"
python3 - "$HERE/launch_policy.json" "$PDV" <<'PY'
import json, sys
p = json.load(open(sys.argv[1], encoding='utf-8'))
p['stages']['dev-e0']['runs'] = p['stages']['dev-e0']['runs'] + ['E0_ref_s15485863']
json.dump(p, open(sys.argv[2], 'w'), ensure_ascii=False)
PY
DV3="$T/dv3"; fx 'for n in dd.DEV_E0: sg._fx_cell(A[0], n)' "$DV3"
stg "$DV3" "$T/sdv3" dev-e0 -- POLICY_FILE="$PDV"; rc_dv3=$?; dv3="$SO"
stg "$DV3" "$T/sdv3" dev-e0 -- DF_AVAIL=5000000000; rc_dv4=$?; dv4="$SO"
stg "$DV3" "$T/sdv3" dev-e0 -- SB_TIME=5-00:00:00; rc_dv5=$?; dv5="$SO"
dv5b=$(env OUT="$DV3" LMP="$FAKE_MPI" bash "$LHL" dev-e0 2>&1); rc_dv5b=$?
chk 'DV③ ★ 정책의 dev-e0 목록에 holdout seed 셀 → 거부 (정책 인자 불합격) · 디스크 5 GB (필요 ≈ 100 GB × 1.10) → 거부 · SB_TIME 을 주면 거부 · BACKEND=local → 거부 — 넷 다 sbatch 0' \
    "[ $rc_dv3 -ne 0 ] && grep -q '정책 stages.dev-e0 인자 불합격' <<<\"\$dv3\" && [ $rc_dv4 -ne 0 ] && grep -q '디스크' <<<\"\$dv4\" && [ $rc_dv5 -ne 0 ] && grep -q 'SB_TIME' <<<\"\$dv5\" && [ $rc_dv5b -ne 0 ] && grep -q 'SLURM 판 전용' <<<\"\$dv5b\" && [ \$(nsb2 '$T/sdv3') -eq 0 ]"
stg "$DV" "$T/sdv" dev-rot; rc_dr0=$?
stg "$DV" "$T/sdv" dev-rot "$DV/none.json"; rc_dr1=$?; dr1="$SO"
chk 'DV④ dev-rot: E0 진단 기록 인자 없음 → usage · 없는 기록 → preflight 거부 — sbatch 합계 8 그대로 (회전 0)' \
    "[ $rc_dr0 -eq 2 ] && [ $rc_dr1 -ne 0 ] && grep -q 'E0 진단 기록' <<<\"\$dr1\" && [ \$(nsb2 '$T/sdv') -eq 8 ]"
#  E0 다섯을 '돌린다' — 러너 (시작 대조 → 가짜 lmp) 뒤 완주 로그 · t₀ 덤프 (고정물) → 진짜 생산자로 E0 진단 기록 (검사기 · S_R² 대역)
for n in E0_ref_s32452843 E0_ref_s49979687 E0_ref_s67867967 E0_ref2_s32452843 E0_ref_dthalf_s32452843; do runr2 "$DV/$n" SLURM_NTASKS=20; done
fx 'for n in dd.DEV_E0: sg._fx_e0_done(A[0], n)
rc, rec = sg._fx_e0_record(A[0], os.path.join(A[0], "dev_e0_diag.json"))
print("E0DIAG", rc, rec["verdict"])' "$DV" > "$T/e0diag.out" 2>&1
stg "$DV" "$T/sdv" dev-rot "$DV/dev_e0_diag.json" -- NP=10; rc_dr2=$?; dr2="$SO"
chk 'DV⑤ ★ E0 진단 PASS (진짜 생산자) 여도 NP 가 다르면 (10 ≠ 기록 20) dev-rot 거부 — 블록 NP 통일 · sbatch 합계 8' \
    "grep -q 'E0DIAG 0 PASS' '$T/e0diag.out' && [ $rc_dr2 -ne 0 ] && grep -q 'NP' <<<\"\$dr2\" && [ \$(nsb2 '$T/sdv') -eq 8 ]"
stg "$DV" "$T/sdv" dev-rot "$DV/dev_e0_diag.json"; rc_dr3=$?; dr3="$SO"
sdr=$(python3 - "$DV" <<'PY' 2>&1
import hashlib, json, os, sys
out = sys.argv[1]
rec = os.path.join(out, 'dev_e0_diag.json')
h = hashlib.sha256(open(rec, 'rb').read()).hexdigest()
bad = []
for n in ('LC_ref_r2_s32452843', 'LH_ref_r2_s32452843'):
    r = json.load(open(os.path.join(out, n, 'launch_record.json'), encoding='utf-8'))
    rq = r.get('requires') or [{}]
    if not (r.get('stage') == 'dev-rot' and rq[0].get('path') == os.path.realpath(rec) and rq[0].get('sha256') == h and rq[0].get('kind') == 'dev_e0_diag'):
        bad.append(n)
print('OK' if not bad else 'NG ' + ' '.join(bad))
PY
)
chk 'DV⑥ ★ dev-rot (기록 PASS · 같은 NP) → 회전 두 런만 제출 (합계 10) · 봉인 requires = E0 진단 기록 (절대경로 · sha256)' \
    "[ $rc_dr3 -eq 0 ] && [ \$(nsb2 '$T/sdv') -eq 10 ] && [ \"\$sdr\" = OK ]"
runr2 "$DV/LC_ref_r2_s32452843" SLURM_NTASKS=20; rc_r1=$?
echo ' ' >> "$DV/dev_e0_diag.json"                                                              # 봉인 뒤 기록이 바뀐다
runr2 "$DV/LH_ref_r2_s32452843" SLURM_NTASKS=20; rc_r2=$?
chk 'DV⑦ ★ 시작 직전 관문 — 기록 그대로면 회전 런 시작 (LIGGGHTS 가짜) · 봉인 뒤 기록이 바뀌면 시작 대조가 막는다 (exit 3 · LIGGGHTS 0 · 거부 영수증)' \
    "[ $rc_r1 -eq 0 ] && grep -q 'fake mpi build' '$DV/LC_ref_r2_s32452843/log.lmp' && [ $rc_r2 -eq 3 ] && ! [ -e '$DV/LH_ref_r2_s32452843/log.lmp' ] && ls '$DV/LH_ref_r2_s32452843'/job_start.refused.*.json >/dev/null 2>&1"
ra=$(OUT="$DV2" LMP="$FAKE" MAXJ=8 bash "$HERE/run_all.sh" 2>&1)
chk 'DV⑧ ★ run_all.sh 는 강성 축 셀을 띄우지 않는다 (SLURM 새 단계로만 · 봉인 · 관문) — 옛 판: LH_* 만 막아 E0_ref_s* 를 로컬로 띄웠다' \
    "! ls '$DV2'/*/pid >/dev/null 2>&1 && [ \$(grep -c '강성 축 셀 건너뜀' <<<\"\$ra\") -eq \$(ls -d '$DV2'/*_s*/ | wc -l) ] && [ \$(ls -d '$DV2'/*_s*/ | wc -l) -ge 5 ]"

#  (CF · CR) 확인 — 시험용 정책 (confirm 두 단계 허용)
mkcf() { fx 'for n in dd.COHORTS["confirm"]: sg._fx_cell(A[0], n)' "$1"; }
CF="$T/cf"; mkcf "$CF"
stg "$CF" "$T/scf0" confirm-first; rc_cf0=$?; cf0="$SO"
chk 'CF① 리포 정책 (확인 단계 미허용 — Codex GO 전) → confirm-first 거부 · sbatch 0' \
    "[ $rc_cf0 -ne 0 ] && [ \$(nsb2 '$T/scf0') -eq 0 ] && grep -q \"'confirm-first'\" <<<\"\$cf0\""
PNULL="$T/policy_cf_null.json"
python3 - "$PCF" "$PNULL" <<'PY'
import json, sys
p = json.load(open(sys.argv[1], encoding='utf-8'))
p['stages']['confirm-first']['soft_range_pct'] = None
json.dump(p, open(sys.argv[2], 'w'), ensure_ascii=False)
PY
stg "$CF" "$T/scf0" confirm-first -- POLICY_FILE="$PNULL"; rc_cfn=$?; cfn="$SO"
chk 'CF② ★ soft 진단 범위 null → 확인 soft 발사 거부 (§6) · sbatch 0' "[ $rc_cfn -ne 0 ] && [ \$(nsb2 '$T/scf0') -eq 0 ]"
CFD="$T/cfd"; mkcf "$CFD"; cp "$DV/LC_ref_r2_s32452843/in.mixer" "$CFD/LC_ref_r8_s15485863/in.mixer"
stg "$CFD" "$T/scfd" confirm-first -- POLICY_FILE="$PCF"; rc_cfd=$?
chk 'CF③ ★ 확인 셀 폴더에 DEV 덱 (LC_ref_r2_s32452843) → 덱 코호트 관문 거부 · sbatch 0' "[ $rc_cfd -ne 0 ] && [ \$(nsb2 '$T/scfd') -eq 0 ]"
stg "$CF" "$T/scf" confirm-first -- POLICY_FILE="$PCF"; rc_cf=$?; cf1="$SO"
scf=$(python3 - "$CF" "$T/scf" "$ROOT" <<'PY' 2>&1
import json, os, sys
out, sd, root = sys.argv[1:]
sys.path.insert(0, os.path.join(root, 'scripts'))
import mixer_deck_diff as dd
calls = [l.rstrip('\n').split('\t') for l in open(os.path.join(sd, 'calls'), encoding='utf-8')]
first = [os.path.basename(c[1]) for c in calls if '--hold' not in c[2]]
held = [os.path.basename(c[1]) for c in calls if '--hold' in c[2]]
m = json.load(open(os.path.join(out, 'confirm_manifest.json'), encoding='utf-8'))
bad = []
if first != list(dd.CONFIRM_FIRST) or held != list(dd.CONFIRM_REST):
    bad.append('order')
if not (m['complete'] is True and m['held_query']['held_ok'] is True and len(m['cells']) == 18 and all(c['jobid'] for c in m['cells'])):
    bad.append('manifest')
for n in dd.COHORTS['confirm']:
    r = json.load(open(os.path.join(out, n, 'launch_record.json'), encoding='utf-8'))
    want_ap = n in dd.CONFIRM_REST
    if ('approval' in r) != want_ap or r.get('soft_range_pct') != 7.37 or r.get('stage') != 'confirm-first':
        bad.append(n)
print('OK' if not bad else 'NG ' + ' '.join(bad))
PY
)
chk 'CF④ ★ confirm-first (§8-2 ④ first-seed-block 6 → rest 12): sbatch 18 = 첫 seed 6 즉시 + 나머지 12 처음부터 --hold (순서 = 등록) · manifest 18 칸 (job ID · 봉인 · held 조회 ok) · held 봉인만 approval 요구 · soft 범위 5.8 봉인' \
    "[ $rc_cf -eq 0 ] && [ \$(nsb2 '$T/scf') -eq 18 ] && [ \"\$scf\" = OK ]"
#  첫 seed 6 런을 '돌린다' (시작 대조 → 가짜 lmp) → bin 0 · E0 고정물 → 진짜 생산자로 증서 6
for n in LC_soft_r8_s15485863 LH_soft_r8_s15485863 LC_ref_r8_s15485863 LH_ref_r8_s15485863 E0_soft_s15485863 E0_ref_s15485863; do runr2 "$CF/$n" SLURM_NTASKS=20; done
fx 'for n in dd.CONFIRM_FIRST:
    (sg._fx_e0_done if n.startswith("E0_") else sg._fx_rot_frames)(A[0], n)
sg._fx_certs(A[0], A[1])' "$CF" "$T/certs_cf"
HX=LC_soft_r8_s86028121
runr2 "$CF/$HX" SLURM_NTASKS=20; rc_hx=$?
chk 'CR① ★ 관문 전에 held 런이 풀려 시작하면 (사람의 scontrol release — 수동 편차) 시작 대조가 막는다 (승인 증서 없음 · exit 3 · LIGGGHTS 0)' \
    "[ $rc_hx -eq 3 ] && ! [ -e '$CF/$HX/log.lmp' ] && grep -q '승인 증서' '$CF/$HX'/job_start.refused.*.json"
stg "$CF" "$T/scf" confirm-rest "$T/certs_cf" -- POLICY_FILE="$PCF"; rc_cr1=$?; cr1="$SO"
chk 'CR①b 그 뒤 confirm-rest 는 거부 (승인 없이 시작된 held 런 = 수동 편차 · 사람이 판단) · scontrol 0' \
    "[ $rc_cr1 -ne 0 ] && [ \$(nsc '$T/scf') -eq 0 ] && grep -q '승인 없이 이미 시작' <<<\"\$cr1\""
CG="$T/cg"; mkcf "$CG"
stg "$CG" "$T/scg" confirm-first -- POLICY_FILE="$PCF"; rc_cg=$?
for n in LC_soft_r8_s15485863 LH_soft_r8_s15485863 LC_ref_r8_s15485863 LH_ref_r8_s15485863 E0_soft_s15485863 E0_ref_s15485863; do runr2 "$CG/$n" SLURM_NTASKS=20; done
fx 'for n in dd.CONFIRM_FIRST:
    (sg._fx_e0_done if n.startswith("E0_") else sg._fx_rot_frames)(A[0], n)
sg._fx_certs(A[0], A[1])
sg._fx_certs(A[0], A[2], status={"LH_soft_r8_s15485863": "TECH_FAIL"})' "$CG" "$T/certs_cg" "$T/certs_cg_tech"
stg "$CG" "$T/scg" confirm-rest "$T/certs_cg_tech" -- POLICY_FILE="$PCF"; rc_cg1=$?; cg1="$SO"
chk 'CR② ★ soft TECH_FAIL 증서 → 관문표가 거부 (release 0 · 승인 0 · 전체 HOLD)' \
    "[ $rc_cg ] && [ $rc_cg1 -ne 0 ] && [ \$(nsc '$T/scg') -eq 0 ] && ! ls '$CG'/*/release_approval.json >/dev/null 2>&1 && grep -q 'TECH_FAIL' <<<\"\$cg1\""
stg "$CG" "$T/scg" confirm-rest "$T/certs_cg" -- POLICY_FILE="$PCF" SC_FAIL=1; rc_cg2=$?; cg2="$SO"
chk 'CR③ ★ release 재시도 ① — 관문 통과 (승인 12) 인데 scontrol 실패 → rc≠0 · 기록 (confirm_release.jsonl · still_held 12)' \
    "[ $rc_cg2 -ne 0 ] && [ \$(ls '$CG'/*/release_approval.json | wc -l) -eq 12 ] && [ \$(nsc '$T/scg') -eq 1 ] && grep -q '\"still_held\": \[\"' '$CG/confirm_release.jsonl'"
stg "$CG" "$T/scg" confirm-rest "$T/certs_cg" -- POLICY_FILE="$PCF"; rc_cg3=$?
HY=LH_ref_r8_s104395301
runr2 "$CG/$HY" SLURM_NTASKS=20; rc_hy=$?
chk 'CR④ ★ release 재시도 ② — 같은 증서로 다시 → 승인 그대로 · scontrol release 12 (합계 2 호출) · 풀린 held 런은 시작 직전 승인 대조를 통과해 돈다' \
    "[ $rc_cg3 -eq 0 ] && [ \$(nsc '$T/scg') -eq 2 ] && [ \$(tail -1 '$T/scg/scontrol_calls' | tr ',' ' ' | wc -w) -eq 14 ] && [ $rc_hy -eq 0 ] && grep -q 'fake mpi build' '$CG/$HY/log.lmp' && python3 -c \"import json,sys; j=json.load(open('$CG/$HY/job_start.json')); sys.exit(0 if j['ok'] is True and j.get('approval_sha256') else 1)\""
CH="$T/ch"; mkcf "$CH"
stg "$CH" "$T/sch" confirm-first -- POLICY_FILE="$PCF" SB_FAIL_AT=908; rc_ch=$?
stg "$CH" "$T/sch" confirm-rest "$T/certs_cg" -- POLICY_FILE="$PCF"; rc_ch2=$?; ch2="$SO"
chk 'CR⑤ ★ 제출 일부 실패 (8 번째 sbatch) → confirm-first rc≠0 · 7 제출 · manifest 불완전 (failed_at) → confirm-rest 거부 · scontrol 0' \
    "[ $rc_ch -ne 0 ] && [ \$(nsb2 '$T/sch') -eq 7 ] && python3 -c \"import json,sys; m=json.load(open('$CH/confirm_manifest.json')); sys.exit(0 if m['complete'] is False and m['failed_at'] else 1)\" && [ $rc_ch2 -ne 0 ] && [ \$(nsc '$T/sch') -eq 0 ]"
mkres LC_ref_r2_s32452843 $((CK + THERMO)) 0
rsm=$(OUT="$R" DRY=1 ONLY=LC_ref_r2_s32452843 bash "$HERE/resume_all.sh" 2>&1)
chk 'DV⑨ resume_all.sh 는 강성 축 셀을 잇지 않는다 (fresh 전용 · §8-1 — 실패는 §8-4 새 폴더 재실행) · in.resume 없음' \
    "! [ -f '$R/LC_ref_r2_s32452843/in.resume' ] && grep -q '재개 없음' <<<\"\$rsm\""
echo "test_launcher: $pass PASS / $fail FAIL"
[ "$fail" -eq 0 ]
