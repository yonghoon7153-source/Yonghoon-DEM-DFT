# test_kg50_watch.sh — kg50_watch.sh 납품 전 시험 (샌드박스 전용 · LIGGGHTS 없음 · Slurm 흉내 = docs/dem1/dem1_kit/test/slurm.py · pkill 안 씀)
#   bash docs/dem1/kg50_watch/test_kg50_watch.sh        장면 8 + 덱 · 재개 도구 대조 + 형식 + 붙여넣기 → ✅/❌ 집계 (❌ 0 이어야 납품)
#   TOOL=다른/kg50_watch.sh · WORK=작업 폴더 (기본 mktemp -d) · AWKBIN=/usr/bin/gawk (ibb 꼴) · LC_ALL=C.UTF-8 로 바꿔 시험
#   장면: ① 본런 P3 (압력 기울기 ETA · mesh kstep/h) + .ins1 만  ② 보류 대기 + 시험 끝  ③ 시험 돌고있음 + ERROR + 로그 없음
#         ④ P4 이완 ETA + 끝  ⑤ squeue 실패  ⑥ 삽입 중 (원 폴더) + 삽입 끝 · 옮기기 전  ⑦ QoS 대기 + 같은 케이스 RUNNING 둘  ⑧ 삽입 FATAL + 폴더 없음
#   장면마다: 읽기 전용 (홈 파일 목록 · 크기 · mtime · 흉내 큐 잡 목록 그대로) · stdin 을 막아도 안 멈춤 · resume 열 화면 폭 맞춤
set -u
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../../.." && pwd); KIT=$REPO/docs/dem1/dem1_kit
TOOL=${TOOL:-$HERE/kg50_watch.sh}; TOOL=$(cd "$(dirname "$TOOL")" && pwd)/$(basename "$TOOL")
DECKS=$REPO/docs/data/kg50_decks_20261027_v3_b50; REPS=$REPO/docs/data/kg50_resume_tests_20261027
WORK=${WORK:-$(mktemp -d "${TMPDIR:-/tmp}/kg50w.XXXXXX")}; B=$WORK/bin; D2=kg50_d2_b50; D07=kg50_d07_b50
PASS=0; FAIL=0; FAILS=
ok(){ echo "  ✅ $*"; PASS=$((PASS+1)); }
ng(){ echo "  ❌ $*"; FAIL=$((FAIL+1)); FAILS="$FAILS
   - $*"; }
chk(){ local d=$1; shift; if "$@" > /dev/null 2>&1; then ok "$d"; else ng "$d"; fi; }
hdr(){ echo; echo "################ $*"; }
rm -rf "$B"; mkdir -p "$B"; cp "$KIT/test/slurm.py" "$B/slurm.py"; chmod +x "$B/slurm.py"
for c in squeue sbatch scancel scontrol sacct; do ln -sf slurm.py "$B/$c"; done
[ -n "${AWKBIN:-}" ] && ln -sf "$AWKBIN" "$B/awk"   # AWKBIN=/usr/bin/gawk = ibb 와 같은 gawk 로 (기본 = 이 기계 awk)
export PATH=$B:$PATH USER=yonghoon MOCK_QOS_CAP=60; unset MOCK_TLIMIT MOCK_SBATCH_FAIL_IN_JOB MOCK_REQUIRE_CONF
rm -f "$WORK/fifo"; mkfifo "$WORK/fifo"; exec 7<>"$WORK/fifo"   # 열린 채 아무도 안 쓰는 stdin — 빈 파일 이름으로 stdin 을 읽으면 멈춤 → timeout 이 잡는다

# ── 가짜 LIGGGHTS 로그 (thermo 규칙 = LAMMPS: run 시작 줄 (CPU 0) · 1000 의 배수 · 끝 step / 덱 print 표식 그대로)
cat > "$WORK/genlog.py" <<'PY'
import sys
kind, natoms, grid, upto = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4])
err = 'err' in sys.argv[5:]
out = []; P = out.append
class Stop(Exception): pass
TAG = {'kg50_d2_b50': 'KG50_D2_B50: mono AM D6, AM:SE=85:15 wt%, SE D50 2um, 6.5mAh/cm2, 50x50um',
       'kg50_d07_b50': 'KG50_D07_B50: mono AM D6, AM:SE=85:15 wt%, SE D50 0.7um, 6.5mAh/cm2, 50x50um'}[sys.argv[6] if len(sys.argv) > 6 else 'kg50_d2_b50']
NPROC = 1
for x in grid.split('x'): NPROC *= int(x)
def boot(restart):
    P('LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, compiled 2025-08-25-10:00:00 by mock)')
    if restart: P('Reading restart file ...'); P('  orthogonal box = (0 0 -0.01) to (0.05 0.05 1)')
    else: P('Created orthogonal box = (0 0 -0.01) to (0.05 0.05 1)')
    P('  %s by %s by %s MPI processor grid' % tuple(grid.split('x')))
    if restart: P('  %d atoms' % natoms)
def run(s0, s1, press=None, every=1000, zmax=False):
    # ibb LIGGGHTS 꼴 그대로 (docs/data/mixer_highbo_devu_prelim_20261006/exact_runs/*/log.exact): 머리 '%8s %8s %14s …' · 줄 '%8d %8d %14.8g …'
    P('Setting up run at Wed Oct 28 09:45:12 2026'); P('Memory usage per processor = 12.3 Mbytes')
    h = ['Step', 'Atoms'] + (['zmax'] if zmax else (['KinEng', 'CPU', 'pressMPa'] if press else ['KinEng', 'CPU']))
    P('%8s %8s' % tuple(h[:2]) + ''.join(' %14s' % x for x in h[2:]) + ' ')
    st = [s0] + list(range((s0 // every + 1) * every, s1 + 1, every))
    if st[-1] != s1: st.append(s1)
    for s in st:
        if s > upto: raise Stop
        cpu = 0 if s == s0 else (s - s0) * 0.05; ke = 1e-3 + 1e-9 * s
        v = [0.174] if zmax else ([ke, cpu, press(s)] if press else [ke, cpu])
        P('%8d %8d' % (s, natoms) + ''.join(' %14.8g' % x for x in v) + ' ')
    P('Loop time of %g on %d procs for %d steps with %d atoms, finish time Wed Oct 28 10:00:00 2026' % ((s1 - s0) * 0.05, NPROC, s1 - s0, natoms)); P('')
    P('Pair  time (%) = 1.0 (50.0)'); P('Neigh time (%) = 0.5 (25.0)'); P('Comm  time (%) = 0.5 (25.0)')
    P('Nlocal:    %g ave %d max %d min' % (natoms / NPROC, natoms, 0)); P('Histogram: 1 0 0 0 0 0 0 0 0 1'); P('Dangerous builds = 0'); P('')
def p3(s): return max(0.005, 0.10 + (s - 540000) * 1e-6)
try:
    if kind == 'insert':
        boot(False); P('====== INSERTING PARTICLES (%s) =====' % TAG)
        P('%8s %8s %14s %14s ' % ('Step', 'Atoms', 'KinEng', 'CPU')); P('%8d %8d %14.8g %14.8g ' % (0, 0, 0, 0))
        P('INFO: Particle insertion ins_mix: inserted %d particle templates (mass 1.234e-05) at step 1' % natoms)
        P('%8d %8d %14.8g %14.8g ' % (1, natoms, 0.5, 0.01)); P('Loop time of 0.01 on 1 procs for 1 steps with %d atoms' % natoms)
        P('====== INSERTED %d / %d (floor %d = 99%%) ======' % (natoms, natoms, natoms * 99 // 100))
        if 'fatal' in sys.argv[5:]: P("FATAL: partial insertion - bed composition differs (PS-01). aborting."); raise Stop
        P('====== AM 1481 / 1481 (gate 1474-1488) ======'); P('====== SE %d / %d (gate 0-0) ======' % (natoms - 1481, natoms - 1481))
        P('====== PHASE 1: SETTLING ======'); run(1, 20001); run(20001, 23001)
    elif kind == 'trial':
        boot(True); P('====== PHASE 1: SETTLING ======'); run(20001, 22001)
        if err: P('ERROR: Lost atoms: original %d current %d (../thermo.cpp:404)' % (natoms, natoms - 11))
    elif kind == 'main':
        boot(True); P('====== PHASE 1: SETTLING ======'); run(20001, 200001)
        P('====== RESTART SAVED ======'); run(200001, 200002, every=1, zmax=True)
        P('====== SETTLING COMPLETE ======'); P('====== Z_MAX (center): 0.174 ======'); P('====== PLATE HEIGHT: 0.18 ======')
        P('====== PHASE 2: STABILIZE ======'); run(200002, 400002, press=lambda s: 0.002)
        P('====== PHASE 3: COMPRESSION (Speed 0.01) ======'); s = 400002
        while True:
            run(s, s + 5000, press=p3); s += 5000
            P('Current Pressure: %.8g MPa (Target: 0.30)' % p3(s))
            if p3(s) >= 0.30: break
        P('====== PHASE 4: RELAXATION ======'); s4 = s
        run(s4, s4 + 100000, press=lambda x: 0.25 - (x - s4) * 1e-7); run(s4 + 100000, s4 + 100000, press=lambda x: 0.24)
        P('====== Simulation Finished' + chr(33) + ' (%s) ======' % TAG)
except Stop:
    pass
print('\n'.join(out))
PY
gl(){ python3 "$WORK/genlog.py" "$@"; }   # 종류 원자수 grid upto [err|-] [케이스]

newhome(){ T=$WORK/$1; H=$T/home; rm -rf "$T"; mkdir -p "$T/state" "$T/fix" "$T/run" "$H/dem_test/logs"; export HOME=$H MOCK_SLURM_STATE=$T/state; cp "$TOOL" "$H/kg50_watch.sh"; NOW=$(date +%s); }
at(){ echo $(( NOW - $1 )); }
tch(){ touch -d "@$2" "$1"; }
mkbin(){ mkdir -p "$(dirname "$1")"; head -c 4096 /dev/urandom > "$1"; tch "$1" "$2"; }
mkcase(){ mkdir -p "$1"; cp "$DECKS/$2"/input_$2*.liggghts "$DECKS/$2"/run_$2*.sh "$1/"; }   # 리포 v3 덱 · 러너 그대로
mkins1(){ local C=$1 N=$2; mkcase "$H/dem_test/$C.ins1" $C; mkbin "$H/dem_test/$C.ins1/restart_$C/restart_settling_20001.bin" $(at 70000)
  gl insert $N 1x1x1 99999999 - $C > "$H/dem_test/$C.ins1/log.liggghts"; tch "$H/dem_test/$C.ins1/log.liggghts" $(at 70000)
  cp -p "$H/dem_test/$C.ins1/log.liggghts" "$H/dem_test/logs/output_${C}_ins_300100.out"; }
mkwork(){ local C=$1 NP=$2 W=$H/dem_test/$1; cp -a "$H/dem_test/$C.ins1" "$W"; mv "$W/log.liggghts" "$W/log.liggghts.ins1"
  cp "$W/input_$C.liggghts" "$W/input_${C}_r$NP.liggghts"
  sed -e "s|^#SBATCH --job-name=.*|#SBATCH --job-name=${C}_r$NP|" -e "s|^#SBATCH --output=.*|#SBATCH --output=logs/output_${C}_r${NP}_%j.out|" -e "s|^#SBATCH -n .*|#SBATCH -n $NP|" "$W/run_$C.sh" > "$W/run_${C}_r$NP.sh"
  sed -e "s/${C}_r$NP/${C}_r${NP}t/g" "$W/run_${C}_r$NP.sh" > "$W/run_${C}_r${NP}t.sh"; }
mkmesh(){ mkdir -p "$1/post_$2"; printf 'solid LIGGGHTS_STL_EXPORT\n  facet normal 0.000000 0.000000 -1.000000\n    outer loop\n      vertex 0.000000 0.000000 %s\n      vertex 0.050000 0.050000 %s\n      vertex 0.050000 0.000000 %s\n    endloop\n  endfacet\nendsolid LIGGGHTS_STL_EXPORT\n' $4 $4 $4 > "$1/post_$2/mesh_$3.stl"; tch "$1/post_$2/mesh_$3.stl" $5; }
pz(){ awk -v s=$1 'BEGIN{z=0.18; if(s>400002) z=0.18-(s-400002)*1e-8; printf "%f", z}'; }   # 판 z (덱 판 속도 0.01 x dt 1e-6 = 1e-8 / step · P3 시작 400002)
mkjob(){ # 이름 코어 로그내용 잠 [sbatch 옵션…] → 잡 번호 (흉내 잡: 로그 내용을 출력 파일에 쓰고 잠)
  local n=$1 np=$2 fx=$3 sl=$4 r=$T/run/$1_$RANDOM.sh; shift 4
  { echo "#SBATCH --job-name=$n"; echo "#SBATCH --output=logs/output_${n}_%j.out"; echo "#SBATCH -n $np"; echo "#SBATCH --time=5-00:00:00"
    [ -n "$fx" ] && echo "cat '$fx'"; [ "$sl" -gt 0 ] && echo "exec sleep $sl"; } > "$r"
  ( cd "$H/dem_test" && sbatch --parsable "$@" "$r" ); }
waitlog(){ local i; for i in $(seq 1 100); do [ -f "$1" ] && [ "$(stat -c %s "$1")" = "$(stat -c %s "$2")" ] && return 0; sleep 0.1; done; return 1; }
waitgone(){ local i; for i in $(seq 1 100); do [ -z "$(squeue -h -j $1 -o %i)" ] && return 0; sleep 0.2; done; return 1; }
setstart(){ python3 - "$1" "$2" <<'PY'
import json, os, sys, time, fcntl
st = os.environ['MOCK_SLURM_STATE']; lk = open(os.path.join(st, 'lock'), 'w'); fcntl.flock(lk, fcntl.LOCK_EX)
p = os.path.join(st, 'jobs.json'); d = json.load(open(p))
for j in d['jobs']:
    if j['id'] == int(sys.argv[1]): j['start'] = time.time() - float(sys.argv[2])
json.dump(d, open(p + '.tmp', 'w'), indent=1); os.replace(p + '.tmp', p)
PY
}
report(){ # 보고 이름 mtime케이스 판정줄 (resume_ckpt.sh 보고 꼴: 머리 두 줄 + '## C' 절 + 끝 줄)
  local f=$H/dem_test/$1 m=$2 c=$3; shift 3
  { echo "# LIGGGHTS 체크포인트 재개 기록 — 시험 · 2026-10-28 09:42"; echo "명령: bash resume_ckpt.sh (흉내)"; echo; echo "## $c"; echo "- 멈춘 폴더: $c.ins1 (손대지 않음)"
    echo "- G0 시험 정상 종료: 통과"; echo "$*"; } > "$f"; tch "$f" $m; }
snap(){ ( cd "$H" && find . -printf '%p %s %T@ %m\n' | LC_ALL=C sort | md5sum | cut -c1-32 )
  python3 -c 'import json,os; p=os.path.join(os.environ["MOCK_SLURM_STATE"],"jobs.json"); d=json.load(open(p)) if os.path.exists(p) else {"jobs":[]}; print(sorted((j["id"],j["name"],j["state"],j["held"],j["cores"],tuple(j["deps"])) for j in d["jobs"]))' | md5sum | cut -c1-32; }
runw(){ ( cd "$H" && timeout 60 bash ~/kg50_watch.sh watch <&7 ) > "$1" 2>&1; echo $? > "$1.rc"; }
fld(){ awk -v c="$2" -v k="$3" '$1==c {print $k}' "$1"; }
colchk(){ python3 - "$@" <<'PY'
import sys, unicodedata
def w(s): return sum(0 if unicodedata.combining(ch) else (2 if unicodedata.east_asian_width(ch) in 'WF' else 1) for ch in s)
L = open(sys.argv[1], encoding='utf-8').read().splitlines()
h = [l for l in L if l.startswith('case ')][0]; ref = w(h[:h.rindex(' resume')])
bad = 0
for a in sys.argv[2:]:
    c, v = a.split('=', 1); r = [l for l in L if l.split(' ')[0] == c][0]
    if not r.endswith(' ' + v): print('끝 열이 다름', c, repr(r[-30:])); bad = 1; continue
    x = w(r[:len(r) - len(v) - 1])
    if x != ref: print('폭 다름', c, x, ref); bad = 1
sys.exit(bad)
PY
}
expect(){ # 출력 케이스 열번호 기대값 이름
  local v; v=$(fld "$1" "$2" "$3"); if [ "$v" = "$4" ]; then ok "$5 = $4"; else ng "$5: 기대 [$4] · 실제 [$v]"; fi; }
has(){ local d=$1 f=$2; shift 2; if grep -qF -- "$*" "$f"; then ok "$d"; else ng "$d (없음: $*)"; fi; }
hasnot(){ local d=$1 f=$2; shift 2; if grep -qF -- "$*" "$f"; then ng "$d (있음: $*)"; else ok "$d"; fi; }
ro(){ local a; a=$(snap); if [ "$a" = "$1" ]; then ok "읽기 전용 (홈 파일 목록·크기·mtime · 큐 잡 목록 그대로)"; else ng "읽기 전용 깨짐"; fi; }
rcok(){ [ "$(cat "$1.rc")" = 0 ] && ok "끝까지 돎 (rc 0 · stdin 막혀도 안 멈춤)" || ng "rc $(cat "$1.rc") (124 = stdin 을 읽다 멈춤)"; }
endq(){ local j; for j in $(squeue -h -o %i 2>/dev/null); do scancel $j; done; }   # 흉내 잡만 (흉내 scancel = 그 잡의 프로세스 그룹)

s1(){ hdr "① 본런 P3 (압력 기울기 → ETA · mesh mtime → kstep/h) · kg50_d07_b50 = .ins1 만 · 남의 잡 · 보고 셋 (머리만 · 🧪 · ✅)"
  local J O=$WORK/s1.out S
  newhome s1; mkins1 $D2 22353; mkins1 $D07 488291; mkwork $D2 4
  local W=$H/dem_test/$D2 s
  for s in 50000 100000 150000 200000 250000 300000 350000 400000; do mkbin "$W/restart_$D2/restart_settling_$s.bin" $(at $(( 10500 - s / 100 ))); done
  mkbin "$W/restart_$D2/restart_after_settling.bin" $(at 8400); mkbin "$W/restart_$D2/restart_compress_600000.bin" $(at 2700)
  mkmesh "$W" $D2 300000 $(pz 300000) $(at 7000); mkmesh "$W" $D2 400000 $(pz 400000) $(at 5000)
  for s in 600000 605000 610000 615000 620000 625000 630000 635000 640000; do mkmesh "$W" $D2 $s $(pz $s) $(at $(( (640000 - s) * 300 / 5000 ))); done
  gl main 22353 2x2x1 640002 - $D2 > "$T/fix/main.log"
  mkmesh "$W" $D2 700000 0.111111 $(at 20000)   # 잡 시작 (3시간 전) 보다 옛 mesh — step 은 더 커도 이번 잡 것으로 안 셈
  J=$(mkjob ${D2}_r4 4 "$T/fix/main.log" 900); waitlog "$H/dem_test/logs/output_${D2}_r4_$J.out" "$T/fix/main.log"; setstart $J 10800
  cp "$T/fix/main.log" "$W/log.liggghts"
  mkjob th3_85 3 "" 900 > /dev/null; mkjob th9_80 28 "" 900 --hold > /dev/null; mkjob kg50_d2_b40_r4 2 "" 900 > /dev/null   # 이름이 비슷한 남의 잡 (40x40 옛 셋)
  cp -p "$REPS/resume_r4_1027_2110.md" "$REPS/resume_r4_1027_2230.md" "$H/dem_test/"; tch "$H/dem_test/resume_r4_1027_2230.md" $(at 50000); tch "$H/dem_test/resume_r4_1027_2110.md" $(at 60)
  report resume_r4_1028_0942.md $(at 11000) $D2 "- ✅ 본 제출 job $J (run_${D2}_r4.sh, 제출 폴더 /home/yonghoon/dem_test)"
  report resume_r4_1028_1000.md $(at 30) kg50_d2_b40 "- ⛔ 본 제출 안 함 — 위 G0/G1/G2/G3 확인 후 사람이 판단"   # 다른 케이스 절만 있는 더 새 보고
  S=$(snap); runw $O; cat $O; rcok $O; ro "$S"
  has "머리: 내 코어 R 9 / 60 (대기 28) — 남의 잡도 셈" $O "내 코어 R 9 / 60 (대기 28)"
  hasnot "비슷한 이름 kg50_d2_b40_r4 를 이 케이스 잡으로 안 셈" $O "⚠R"
  expect $O $D2 2 $J "d2 job"; expect $O $D2 5 4 "d2 np"; expect $O $D2 6 2x2x1 "d2 grid"; expect $O $D2 7 P3-comp "d2 phase"
  expect $O $D2 8 640002 "d2 step (로그 640002 ≥ mesh 640000)"; expect $O $D2 9 22353 "d2 atoms"; expect $O $D2 10 0.2000 "d2 P_MPa"
  expect $O $D2 11 0.177600 "d2 plate_z (mesh_640000)"; expect $O $D2 12 1.74 "d2 z/hs (0.1776 / 0.10198)"
  expect $O $D2 13 60 "d2 kstep/h (최근 1시간 mesh 9 장 · 옛 mesh 둘 뺌)"; expect $O $D2 14 2h "d2 ETA (P 0.200 · 1시간 전 0.140 · 목표 0.30 → 1.67 h)"
  expect $O $D2 15 compress_600000 "d2 ckpt"; expect $O $D2 16 - "d2 next"
  chk "d2 elapsed 3:00:xx (흉내 잡 시작 = 3시간 전)" grep -qE "^$D2 +$J +3:00:" $O
  has "d2 상태 = 돌고있음 r4" $O "돌고있음 r4"
  chk "d2 resume = ✅본제출 $J (가장 최근 머리만 보고는 건너뜀)" grep -qE "^$D2 .* ✅본제출 $J\$" $O
  expect $O $D07 2 - "d07 job"; expect $O $D07 7 P1-settle "d07 phase (삽입 로그)"; expect $O $D07 8 23001 "d07 step"; expect $O $D07 9 488291 "d07 atoms"
  expect $O $D07 6 1x1x1 "d07 grid"; expect $O $D07 15 settling_20001 "d07 ckpt (.ins1)"; expect $O $D07 11 - "d07 plate_z"
  chk "d07 상태 = 삽입 끝 · 재개 전 · resume -" grep -qE "^$D07 .*삽입 끝 · 재개 전 +-\$" $O
  has "덱에서 단위: 1 µm = 0.001 덱 길이 (r_* 줄 3개) → 고체 두께 0.10198" $O "1 µm = 0.001 덱 길이 (r_* 줄 3개) → 고체 두께 0.10198"
  has "덱에서 목표 0.30 · 이완 run 100000" $O "목표 0.30 · 이완 run 100000"
  has "resume 출처 = resume_r4_1028_0942.md" $O "resume ← resume_r4_1028_0942.md"
  chk "resume 열 화면 폭 맞춤 (한글 · 이모지)" colchk $O "$D2=✅본제출 $J" "$D07=-"
  endq; }

s2(){ hdr "② kg50_d2_b50 = 보류 대기 · kg50_d07_b50 = 시험 끝 (흉내 잡 COMPLETED · 큐에 없음) · 🧪"
  local J P O=$WORK/s2.out S
  newhome s2; mkins1 $D2 22353; mkins1 $D07 488291; mkwork $D2 4; mkwork $D07 56
  gl trial 488291 7x8x1 99999999 - $D07 > "$T/fix/t07.log"; gl trial 22353 2x2x1 99999999 - $D2 > "$T/fix/t2.log"
  J=$(mkjob ${D07}_r56t 56 "$T/fix/t07.log" 0); waitgone $J; cp "$T/fix/t2.log" "$H/dem_test/logs/output_${D2}_r4t_327010.out"
  P=$(mkjob ${D2}_r4 4 "" 900 --hold)
  cp -p "$REPS/resume_r4_1027_2230.md" "$H/dem_test/"; report resume_r56_1028_1300.md $(at 100) $D07 "- 🧪 시험만 (-T) — G0–G3 통과 · 본 제출 안 함"
  S=$(snap); runw $O; cat $O; rcok $O; ro "$S"
  has "머리: R 0 / 60 (대기 4)" $O "내 코어 R 0 / 60 (대기 4)"
  expect $O $D2 2 - "d2 job"; expect $O $D2 16 $P "d2 next = 보류 잡"; expect $O $D2 5 4 "d2 np (대기 잡 코어)"
  chk "d2 상태 = 대기 JobHeldUser · resume 🧪시험만" grep -qE "^$D2 .*대기 JobHeldUser +🧪시험만\$" $O
  expect $O $D07 2 - "d07 job (끝난 시험은 큐에 없음)"; expect $O $D07 8 22001 "d07 step (시험 끝 22001)"; expect $O $D07 6 7x8x1 "d07 grid"
  expect $O $D07 5 56 "d07 np (러너 run_${D07}_r56.sh)"; expect $O $D07 7 P1-settle "d07 phase"
  chk "d07 상태 = 시험 끝 · 본 제출 전 · resume 🧪시험만" grep -qE "^$D07 .*시험 끝 · 본 제출 전 +🧪시험만\$" $O
  chk "resume 열 화면 폭 맞춤" colchk $O "$D2=🧪시험만" "$D07=🧪시험만"
  endq; }

s3(){ hdr "③ 시험 돌고있음 (job 뒤 t) + ERROR 줄 · 본런 로그 없음 (지워짐 · mesh 로만 step · 판 z · kstep/h) · ⛔ 보고"
  local J K O=$WORK/s3.out S s
  newhome s3; mkins1 $D2 22353; mkins1 $D07 488291; mkwork $D2 4; mkwork $D07 56
  gl trial 488291 7x8x1 99999999 err $D07 > "$T/fix/t07.log"
  J=$(mkjob ${D07}_r56t 56 "$T/fix/t07.log" 900); waitlog "$H/dem_test/logs/output_${D07}_r56t_$J.out" "$T/fix/t07.log"; setstart $J 600
  K=$(mkjob ${D2}_r4 4 "" 900); setstart $K 7200; sleep 0.3; rm -f "$H/dem_test/logs/output_${D2}_r4_$K.out"
  for s in 300000 305000 310000 315000 320000 325000 330000; do mkmesh "$H/dem_test/$D2" $D2 $s $(pz $s) $(at $(( (330000 - s) * 300 / 5000 ))); done
  report resume_r56_1028_1300.md $(at 3000) $D07 "- ⛔ 본 제출 안 함 — 위 G0/G1/G2/G3 확인 후 사람이 판단"
  report resume_r4_1028_0942.md $(at 8000) $D2 "- ✅ 본 제출 job $K (run_${D2}_r4.sh, 제출 폴더 /home/yonghoon/dem_test)"
  S=$(snap); runw $O; cat $O; rcok $O; ro "$S"
  has "머리: R 60 / 60 (대기 0)" $O "내 코어 R 60 / 60 (대기 0)"
  expect $O $D07 2 ${J}t "d07 job = 시험 표시 t"; expect $O $D07 5 56 "d07 np"; expect $O $D07 8 22001 "d07 step"
  expect $O $D07 13 - "d07 kstep/h (시험 2000 step · CPU 50 s < 60 s → 안 냄)"
  chk "d07 상태 = 시험 중 r56t ERR1 · resume ⛔" grep -qE "^$D07 .*시험 중 r56t ERR1 +⛔\$" $O
  expect $O $D2 2 $K "d2 job"; expect $O $D2 7 - "d2 phase (로그 없음)"; expect $O $D2 6 - "d2 grid (로그 없음)"; expect $O $D2 9 - "d2 atoms (로그 없음)"
  expect $O $D2 8 330000 "d2 step (mesh)"; expect $O $D2 11 0.180000 "d2 plate_z (mesh)"; expect $O $D2 12 1.77 "d2 z/hs"; expect $O $D2 13 60 "d2 kstep/h (mesh 7 장 · 30 분)"
  chk "d2 상태 = 돌고있음 r4 ⚠로그없음 (옛 로그를 지금 것처럼 안 씀)" grep -qE "^$D2 .*돌고있음 r4 ⚠로그없음 +✅본제출 $K\$" $O
  chk "resume 열 화면 폭 맞춤" colchk $O "$D2=✅본제출 $K" "$D07=⛔"
  endq; }

s4(){ hdr "④ 본런 P4 이완 (ETA = 덱 이완 run 100000 − 진행) · kg50_d07_b50 = 끝 (✅끝 · ckpt end)"
  local J O=$WORK/s4.out S s
  newhome s4; mkins1 $D2 22353; mkins1 $D07 488291; mkwork $D2 4; mkwork $D07 56
  local W=$H/dem_test/$D2 V=$H/dem_test/$D07
  mkbin "$W/restart_$D2/restart_compress_600000.bin" $(at 3000)
  for s in 760000 765000 770000 775000 780000 785000 790000; do mkmesh "$W" $D2 $s $(pz 740002) $(at $(( (790000 - s) * 300 / 5000 ))); done
  gl main 22353 2x2x1 790000 - $D2 > "$T/fix/main.log"
  J=$(mkjob ${D2}_r4 4 "$T/fix/main.log" 900); waitlog "$H/dem_test/logs/output_${D2}_r4_$J.out" "$T/fix/main.log"; setstart $J 20000
  gl main 488291 7x8x1 99999999 - $D07 > "$H/dem_test/logs/output_${D07}_r56_329001.out"; tch "$H/dem_test/logs/output_${D07}_r56_329001.out" $(at 600)
  mkbin "$V/restart_$D07/restart_compress_600000.bin" $(at 5000); mkbin "$V/restart_$D07/restart_end.bin" $(at 600); mkmesh "$V" $D07 840000 $(pz 740002) $(at 600)
  report resume_r4_1028_0942.md $(at 30000) $D2 "- ✅ 본 제출 job $J (run_${D2}_r4.sh, 제출 폴더 /home/yonghoon/dem_test)"
  report resume_r56_1028_1300.md $(at 20000) $D07 "- ✅ 본 제출 job 329001 (run_${D07}_r56.sh, 제출 폴더 /home/yonghoon/dem_test)"
  S=$(snap); runw $O; cat $O; rcok $O; ro "$S"
  expect $O $D2 7 P4-relax "d2 phase"; expect $O $D2 8 790000 "d2 step"; expect $O $D2 13 60 "d2 kstep/h"; expect $O $D2 10 0.2450 "d2 P_MPa"
  expect $O $D2 14 0.8h "d2 ETA ((740002 + 100000 − 790000) / 60 kstep/h)"; expect $O $D2 11 0.176600 "d2 plate_z"; expect $O $D2 12 1.73 "d2 z/hs"
  expect $O $D07 7 done "d07 phase"; expect $O $D07 15 end "d07 ckpt (restart_end)"; expect $O $D07 10 0.2400 "d07 P_MPa (마지막 정규 줄)"; expect $O $D07 12 1.73 "d07 z/hs (마지막 mesh)"
  chk "d07 상태 = ✅끝 · resume ✅본제출 329001" grep -qE "^$D07 .*✅끝 +✅본제출 329001\$" $O
  chk "resume 열 화면 폭 맞춤" colchk $O "$D2=✅본제출 $J" "$D07=✅본제출 329001"
  S4H=$H; S4T=$T; }   # ⑤ 가 이 나무를 그대로 씀 (잡은 ⑤ 끝에 취소)

s5(){ hdr "⑤ squeue 실패 (흉내 상태 없음) → 4번 묻고 '큐 상태 모름' — 멈춤·끝으로 읽지 않음"
  local O=$WORK/s5.out S
  export HOME=$S4H; H=$S4H; T=$S4T; S=$(snap)
  ( unset MOCK_SLURM_STATE; cd "$H" && timeout 60 bash ~/kg50_watch.sh watch <&7 ) > $O 2>&1; echo $? > $O.rc; cat $O; rcok $O
  export MOCK_SLURM_STATE=$T/state; ro "$S"
  has "머리: squeue 4번 실패" $O "⚠ squeue 4번 실패 — 큐 상태 모름"
  expect $O $D2 2 "?" "d2 job = ?"; expect $O $D2 16 "?" "d2 next = ?"; has "상태 = ?큐조회실패" $O "?큐조회실패"
  hasnot "끝·멈춤으로 안 읽음" $O "✅끝"
  endq; }

s6(){ hdr "⑥ kg50_d07_b50 삽입 중 (원 폴더 · .ins1 없음) · kg50_d2_b50 삽입 끝 · 옮기기 전 (마지막 step = 삽입 덱 run 합 23001)"
  local J O=$WORK/s6.out S
  newhome s6; mkcase "$H/dem_test/$D07" $D07; mkcase "$H/dem_test/$D2" $D2
  gl insert 488291 1x1x1 10000 - $D07 > "$T/fix/ins07.log"
  J=$(mkjob ${D07}_ins 1 "$T/fix/ins07.log" 900); waitlog "$H/dem_test/logs/output_${D07}_ins_$J.out" "$T/fix/ins07.log"; setstart $J 3000
  gl insert 22353 1x1x1 99999999 - $D2 > "$H/dem_test/logs/output_${D2}_ins_300200.out"; tch "$H/dem_test/logs/output_${D2}_ins_300200.out" $(at 4000)
  mkbin "$H/dem_test/$D2/restart_$D2/restart_settling_20001.bin" $(at 4100)
  S=$(snap); runw $O; cat $O; rcok $O; ro "$S"
  expect $O $D07 2 $J "d07 job"; expect $O $D07 5 1 "d07 np"; expect $O $D07 8 10000 "d07 step"; expect $O $D07 7 P1-settle "d07 phase"
  expect $O $D07 13 72 "d07 kstep/h (로그 CPU 열)"
  chk "d07 상태 = 삽입 중" grep -qE "^$D07 .*삽입 중 +-\$" $O
  chk "d2 상태 = 삽입 끝 · 재개 전 (원 폴더)" grep -qE "^$D2 .*삽입 끝 · 재개 전 +-\$" $O
  expect $O $D2 8 23001 "d2 step"; expect $O $D2 15 settling_20001 "d2 ckpt"
  endq; }

s7(){ hdr "⑦ QoS 대기: 남의 28 코어 + kg50_d2_b50 4 코어 (+ 실수로 겹친 시험 4 코어) 돌고 · kg50_d07_b50 시험 56 코어 대기 (QOSMaxCpuPerUserLimit)"
  local J P O=$WORK/s7.out S
  newhome s7; mkins1 $D2 22353; mkins1 $D07 488291; mkwork $D2 4; mkwork $D07 56
  gl main 22353 2x2x1 100000 - $D2 > "$T/fix/main.log"
  mkjob th9_80 28 "" 900 > /dev/null
  J=$(mkjob ${D2}_r4 4 "$T/fix/main.log" 900); waitlog "$H/dem_test/logs/output_${D2}_r4_$J.out" "$T/fix/main.log"; setstart $J 900
  mkjob ${D2}_r4t 4 "" 900 > /dev/null
  P=$(mkjob ${D07}_r56t 56 "" 900)
  S=$(snap); runw $O; cat $O; rcok $O; ro "$S"
  has "머리: R 36 / 60 (대기 56)" $O "내 코어 R 36 / 60 (대기 56)"
  expect $O $D07 16 ${P}t "d07 next = 대기 시험 잡 (t)"; expect $O $D07 5 56 "d07 np (대기 잡 코어)"
  chk "d07 상태 = 대기 QOSMaxCpuPerUserLimit" grep -qE "^$D07 .*대기 QOSMaxCpuPerUserLimit +-\$" $O
  expect $O $D2 2 $J "d2 job = 먼저 돈 (번호 작은) 잡"; expect $O $D2 7 P1-settle "d2 phase"; expect $O $D2 8 100000 "d2 step"
  chk "d2 상태 = 돌고있음 r4 ⚠R2 (같은 케이스 RUNNING 둘)" grep -qE "^$D2 .*돌고있음 r4 ⚠R2 +-\$" $O
  expect $O $D2 13 72 "d2 kstep/h (덤프 없음 → 로그 CPU 열: 79000 step / 3950 s)"
  chk "resume 열 화면 폭 맞춤 (상태 26 칸 꽉 참)" colchk $O "$D2=-" "$D07=-"
  endq; }

s8(){ hdr "⑧ 삽입 실패 (덱 FATAL 문 · 큐에 없음 · 원 폴더) · 다른 케이스 = 폴더 없음"
  local O=$WORK/s8.out S
  newhome s8; mkcase "$H/dem_test/$D07" $D07
  gl insert 488291 1x1x1 99999999 fatal $D07 > "$H/dem_test/logs/output_${D07}_ins_300300.out"; tch "$H/dem_test/logs/output_${D07}_ins_300300.out" $(at 500)
  S=$(snap); runw $O; cat $O; rcok $O; ro "$S"
  chk "d07 상태 = 멈춤 (큐 없음) FATAL (삽입 끝으로 안 읽음)" grep -qE "^$D07 .*멈춤 \(큐 없음\) FATAL +-\$" $O
  expect $O $D07 7 insert "d07 phase (INSERTED 뒤 멈춤)"
  chk "d2 상태 = 폴더 없음 · 덱 없음" grep -qE "^$D2 .*폴더 없음 +-\$" $O
  has "덱 없으면 값 ? · 덱 없음" $O "($D2 덱 값: 목표 ? · 이완 run ? · 1 µm = ? 덱 길이 (r_* 줄 0개) → 고체 두께 ? · 덱 없음 · resume ← 없음)"
  endq; }

t_deck(){ hdr "대조: 도구가 기대는 이름 · 줄이 리포 v3 덱 · 러너 · scripts/resume_ckpt.sh 에 그대로 있다 (바뀌면 여기서 실패)"
  local C F G R=$REPO/scripts/resume_ckpt.sh
  for C in $D07 $D2; do F=$DECKS/$C/input_$C.liggghts; G=$DECKS/$C/input_${C}_insert.liggghts
    chk "$C: mesh 덤프 = post_$C/mesh_*.stl" grep -qE "^dump +dmp_mesh +all +mesh/stl +[0-9]+ +post_$C/mesh_\*\.stl +top_mesh" $F
    chk "$C: restart = restart_$C/restart_settling_* · restart_compress_*" grep -qE "^restart +[0-9]+ +restart_$C/restart_compress_\*\.bin" $F
    chk "$C: settling restart 줄" grep -qE "^restart +[0-9]+ +restart_$C/restart_settling_\*\.bin" $F
    chk "$C: write_restart after_settling · end" [ "$(grep -cE "^write_restart +restart_$C/restart_(after_settling|end)\.bin" $F)" = 2 ]
    chk "$C: thermo = step atoms ke cpu v_pressMPa (압력 = 끝 열 · CPU 열)" grep -qE '^thermo_style +custom step atoms ke cpu v_pressMPa *$' $F
    chk "$C: 목표 = variable target_press equal 0.30" grep -qE '^variable target_press equal 0\.30( |$)' $F
    chk "$C: 표식 PHASE 1–4 · INSERTED · Simulation Finished" [ "$(grep -cE '^print "====== (PHASE [1-4]|INSERTED |Simulation Finished)' $F)" = 6 ]
    chk "$C: P4 표식 글자 그대로 (ETA 시작 step 을 이 줄로 찾음)" grep -qxF 'print "====== PHASE 4: RELAXATION ======"' $F
    chk "$C: r_* 줄 3개 · 값 ÷ 주석 µm 이 같음" [ "$(awk '$1=="variable" && $2~/^r_/ {h=index($0,"#"); c=substr($0,h); if(match(c,/r=[0-9.]+/)) printf "%.6g\n", $4/substr(c,RSTART+2,RLENGTH-2)}' $F | sort -u | tr '\n' ' ')" = "0.001 " ]
    chk "$C: 삽입 덱 run 합 23001 · write_restart restart_settling_20001" [ "$(awk '$1=="run" && $2~/^[0-9]+$/ {s+=$2} END{print s}' $G)" = 23001 ]
    chk "$C: 삽입 덱 체크포인트" grep -qE "^write_restart +restart_$C/restart_settling_20001\.bin" $G
    chk "$C: 러너 출력 = logs/output_<잡 이름>_%j.out (C · C_ins)" [ "$(grep -cE "^#SBATCH --output=logs/output_${C}(_ins)?_%j\.out" $DECKS/$C/run_$C.sh $DECKS/$C/run_${C}_insert.sh | awk -F: '{s+=$2} END{print s}')" = 2 ]
  done
  chk "resume_ckpt.sh: 보고 = \$L/resume_\${SFX}_\$STAMP.md" grep -qF 'REP=$L/resume_${SFX}_$STAMP.md' $R
  chk "resume_ckpt.sh: 케이스 절 머리 '## \$C'" grep -qF 'echo; echo "## $C"' $R
  chk "resume_ckpt.sh: 판정 줄 넷 (✅ 본 제출 job · 🧪 시험만 · ⛔ 본 제출 안 함 · ⛔ 본 제출 실패)" [ "$(grep -oE -- '"- (✅ 본 제출 job \$JM|🧪 시험만 \(-T\)|⛔ 본 제출 실패|⛔ 본 제출 안 함)' $R | sort -u | wc -l)" = 4 ]
  chk "resume_ckpt.sh: 시험 잡 · 로그 = \${C}_\${SFX}t · logs/output_\${C}_\${SFX}t_\$J.out" grep -qF 'logs/output_${C}_${SFX}t_$J.out' $R
  chk "resume_ckpt.sh: 작업 사본 = \$L/\$C · 멈춘 폴더 = \$L/\$C.\$SUF" grep -qF 'S=$L/$C.$SUF; W=$L/$C;' $R; }

t_fmt(){ hdr "형식 (DEM1): 느낌표 · 탭 · CR 0 · 첫 6줄 사용법 · main · 큐 · 파일을 바꾸는 명령 없음"
  local O=$WORK/fmt.out
  chk "bash -n" bash -n "$TOOL"
  chk "느낌표 0" [ "$(tr -cd '\041' < "$TOOL" | wc -c)" = 0 ]
  chk "탭 0" [ "$(tr -cd '\t' < "$TOOL" | wc -c)" = 0 ]
  chk "CR 0" [ "$(tr -cd '\r' < "$TOOL" | wc -c)" = 0 ]
  chk "첫 6줄 = 주석" [ "$(head -6 "$TOOL" | grep -c '^#')" = 6 ]
  ( cd "$WORK" && bash "$TOOL" ) > $O 2>&1; chk "인자 없음 → 첫 6줄 그대로" cmp -s $O <(head -6 "$TOOL")
  ( cd "$WORK" && bash "$TOOL" xyz ) > $O 2>&1; chk "모르는 인자 → 사용법" cmp -s $O <(head -6 "$TOOL")
  chk "끝 줄 = main \"\$@\"; exit \$?" [ "$(tail -1 "$TOOL")" = 'main "$@"; exit $?' ]
  chk "main(){ case \"\$1\" in" grep -qF 'main(){ case "$1" in' "$TOOL"
  chk "sbatch · scancel · scontrol 없음" [ "$(grep -cwE 'sbatch|scancel|scontrol' "$TOOL")" = 0 ]
  chk "rm · mv · cp · mkdir · touch · tee · ln 명령 없음" [ "$(grep -cE '(^|[;&|({] *)(rm|mv|cp|mkdir|touch|tee|ln|chmod) ' "$TOOL")" = 0 ]
  chk "squeue 재시도 (4번)" grep -qF 'for i in 1 2 3 4; do o=$(squeue' "$TOOL"; }

t_paste(){ hdr "붙여넣기 블록: make_block (검사 + md5) · 대화형 붙여넣기 왕복 · 1글자 깨짐 · CRLF"
  local BL=$WORK/kg50_watch_block.txt O
  cp "$TOOL" "$WORK/kg50_watch.sh"; bash "$KIT/tool/make_block.sh" "$WORK/kg50_watch.sh" "bash ~/kg50_watch.sh watch" > $WORK/mb.out 2>&1
  chk "make_block 통과" grep -q '^✅' $WORK/mb.out
  [ "$TOOL" = "$HERE/kg50_watch.sh" ] && [ -s "$HERE/kg50_watch_block.txt" ] && chk "만든 블록 = 리포의 kg50_watch_block.txt" cmp -s $BL "$HERE/kg50_watch_block.txt"
  chk "블록 마지막 줄 = md5 게이트 → watch 한 번" grep -qE '^if \[ "\$\(md5sum < ~/kg50_watch.sh \| cut -c1-32\)" = [0-9a-f]{32} \]; then bash ~/kg50_watch.sh watch; else' <(tail -1 $BL)
  newhome p1; O=$WORK/p1.out; rm -f "$H/kg50_watch.sh"
  ( cd "$H" && timeout 60 bash --norc -i < $BL ) > $O 2>&1
  chk "붙여넣기 왕복 = 원본" cmp -s "$H/kg50_watch.sh" "$TOOL"
  chk "게이트 뒤 watch 한 번 돎" grep -q '^══ 50kg SE 입도 2케이스' $O   # 대화형 bash 는 heredoc 줄을 '> ' 뒤에 되찍는다 → 줄 머리로만 센다
  newhome p2; O=$WORK/p2.out; rm -f "$H/kg50_watch.sh"; sed '0,/^mt(){/s//mt (){/' $BL > $T/bad.txt
  ( cd "$H" && timeout 60 bash --norc -i < $T/bad.txt ) > $O 2>&1
  chk "1글자 깨진 붙여넣기 → md5 게이트가 막음" grep -qF '붙여넣기가 깨짐 (md5 다름) — 아무것도 안 함' $O
  chk "깨졌을 땐 watch 안 돎" [ "$(grep -c '^══ 50kg' $O)" = 0 ]
  newhome p3; O=$WORK/p3.out; rm -f "$H/kg50_watch.sh"; sed 's/$/\r/' $BL > "$H/kg50_watch_block.txt"
  ( cd "$H" && sed -i 's/\r$//' ~/kg50_watch_block.txt && bash ~/kg50_watch_block.txt ) > $O 2>&1
  chk "CRLF 파일도 sed 로 복구 → 원본과 같음 · watch 돎" cmp -s "$H/kg50_watch.sh" "$TOOL"
  chk "CRLF 복구 뒤 watch 출력" grep -q '^══ 50kg SE 입도 2케이스' $O; }

echo "도구 $TOOL (md5 $(md5sum < "$TOOL" | cut -c1-32)) · 작업 $WORK · awk $(readlink -f "$(command -v awk)") · LC_ALL=${LC_ALL:-} LANG=${LANG:-}"
s1; s2; s3; s4; s5; s6; s7; s8; t_deck; t_fmt; t_paste
exec 7>&-
echo; echo "════ 결과: ✅ $PASS · ❌ $FAIL ════"; [ $FAIL = 0 ] || { echo "실패:$FAILS"; exit 1; }
