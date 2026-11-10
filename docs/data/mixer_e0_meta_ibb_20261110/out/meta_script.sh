# mixer_e0_meta.sh — 믹서 E0 자격 pilot 한 팔 · 1 단계: ibb 읽기 전용 메타 수집 (초안 2026-11-10 · 형식 mixer_e0_meta/1)
#   붙여넣기 블록 (meta_block.txt) 이 md5 를 대조한 뒤에만 bash -c 로 돈다.  쓰는 곳 = 새 폴더 ~/mixer_e0_meta_<UTC>/ 하나뿐.
#   하지 않는 것: 제출 · 취소 · 잡 제어 · 예약 · git 쓰기 · 지우기 · 옮기기 · conda / module 바꾸기 · 계산.
#   외부 명령은 전부 timeout 안 · 없으면 MISSING 으로 적고 계속 · 전체 상한 MIX_BUDGET 초 (기본 900).
#   켜고 끄기 (붙여넣기 전에 export): MIX_BIN_HELP=0 (lmp -h 안 부름) · MIX_SLURM=0 (SLURM 조회 안 함) · MIX_REPO=<체크아웃> · LMP=<실행 파일>
#   결과: out/ (가린 사본) 을 묶은 tgz 하나 + sha256 (화면).  raw/ (가리지 않은 원문) 은 ibb 에 남긴다 (가져오지 않는다).
export LC_ALL=C GIT_OPTIONAL_LOCKS=0 GIT_TERMINAL_PROMPT=0 GIT_PAGER=cat PAGER=cat
umask 077
FORMAT='mixer_e0_meta/1'
BLOCK_ID='mixer_e0_meta_block draft 2026-11-10'
REF_LMP_0928='ee2d77261bac9e7fa4e9311c8709e74bf7583a13225a5bc35a791bef9be60a3f'
REF_E0_DECK='8b588b24117ab77bf72d93662237268b401f714df8515d62ef7b964d01c6e718'
CAP=2097152
BUDGET=${MIX_BUDGET:-900}
case "$BUDGET" in ''|*[^0-9]*) BUDGET=900;; esac
BIN_HELP=${MIX_BIN_HELP:-1}
SLURM_ON=${MIX_SLURM:-1}
SELF_TEXT=${1-}
say() { printf '%s\n' "$*"; }

# ── 가림 (awk) — 경로 · 호스트 · 계정 · IPv4 · uid/gid · 빌드 사용자.  토큰은 환경 MIX_T<k> (값) · MIX_R<k> (대체) · MIX_W<k> (1 = 낱말 경계)
AWK_RED='
function isw(c) { return (c ~ /[A-Za-z0-9_]/) }
function rlit(s, a, b,   i, o) { o = ""; while ((i = index(s, a)) > 0) { o = o substr(s, 1, i - 1) b; s = substr(s, i + length(a)) } return o s }
function rword(s, a, b,   i, o, pr, po) {
  o = ""
  while ((i = index(s, a)) > 0) {
    if (i > 1) pr = substr(s, i - 1, 1); else if (length(o) > 0) pr = substr(o, length(o), 1); else pr = ""
    po = substr(s, i + length(a), 1)
    if ((pr == "" || isw(pr) == 0) && (po == "" || isw(po) == 0)) o = o substr(s, 1, i - 1) b
    else o = o substr(s, 1, i - 1 + length(a))
    s = substr(s, i + length(a))
  }
  return o s
}
function buser(s,   i, j, r, k) {
  i = index(s, "compiled "); if (i == 0) return s
  j = index(substr(s, i), " by "); if (j == 0) return s
  j = i + j + 3; r = substr(s, j); k = match(r, /[ ,)]/)
  if (k == 0) return substr(s, 1, j - 1) "<BUILD_USER>"
  return substr(s, 1, j - 1) "<BUILD_USER>" substr(r, k)
}
BEGIN { n = 0; for (k = 1; k <= 9; k++) { v = ENVIRON["MIX_T" k]; if (length(v) > 0) { n++; T[n] = v; R[n] = ENVIRON["MIX_R" k]; W[n] = ENVIRON["MIX_W" k] } } rem = ENVIRON["MIX_REMOTE"] }
{ s = $0
  if (rem == "1") gsub(/[^ ]+:\//, "<REMOTE>:/", s)
  for (k = 1; k <= n; k++) { if (W[k] == "1") s = rword(s, T[k], R[k]); else s = rlit(s, T[k], R[k]) }
  gsub(/\/home\/[A-Za-z0-9._-]+/, "/home/<OTHER_USER>", s)
  gsub(/[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/, "<IPV4>", s)
  gsub(/uid[ =]?[0-9]+/, "uid <UID>", s); gsub(/gid[ =]?[0-9]+/, "gid <GID>", s)
  print buser(s) }'

# ── 봉인 · 시작 대조 · E0 진단 기록의 칸 몇 개만 (값 · M · 겹침은 읽지 않는다 — 그런 칸은 목록에 없다)
PY_SEAL='
import json, sys
mode = sys.argv[1]
keys = [["run"], ["stage"], ["schema"], ["time_utc"], ["backend"], ["lmp_path"], ["lmp_realpath"], ["lmp_sha256"], ["git_head"],
        ["sha256", "in.mixer"], ["sha256", "Drum.stl"], ["sha256", "Front.stl"], ["sha256", "Back.stl"],
        ["slurm", "np"], ["slurm", "mpirun_flags"], ["slurm", "qos"], ["slurm", "partition"], ["slurm", "time"],
        ["slurm", "conda_env"], ["slurm", "path_prefix"], ["slurm", "runner_sha256"], ["slurm", "start_check_sha256"],
        ["policy", "policy_id"], ["policy", "sha256"], ["ok"], ["launch_record_sha256"], ["runner_sha256_executed"],
        ["slurm_job_id"], ["slurm_ntasks"], ["start_check_sha256"]]
if mode == "diag":
    keys = [["schema"], ["verdict"]]
for p in sys.argv[2:]:
    try:
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
    except Exception as e:
        print(p + "|ERROR|" + type(e).__name__)
        continue
    if not isinstance(d, dict):
        print(p + "|NOT_OBJECT|")
        continue
    for ks in keys:
        x = d
        for k in ks:
            x = x.get(k) if isinstance(x, dict) else None
        if x is None:
            continue
        print(p + "|" + ".".join(ks) + "|" + json.dumps(x, ensure_ascii=True)[:400])
'
PY_VER='import sys, platform
print(sys.version.split()[0])
print(platform.platform())
print(sys.executable)'
PY_MODS='import importlib
for m in ("numpy", "scipy"):
    try:
        print(m, importlib.import_module(m).__version__)
    except Exception as e:
        print(m, "IMPORT_FAIL", type(e).__name__)'

# ── 시작 관문 (하나라도 안 되면 폴더도 만들지 않고 끝)
command -v timeout >/dev/null 2>&1 || { say "timeout 이 없음 — 아무것도 안 함 (폴더도 안 만듦)"; exit 3; }
TK=''
timeout -k 2 5 true </dev/null >/dev/null 2>&1 && TK='-k 5'
case "${HOME-}" in /?*) ;; *) say "HOME 이 절대경로가 아님 — 아무것도 안 함"; exit 3;; esac
[ "${#HOME}" -ge 4 ] || { say "HOME 이 너무 짧음 — 아무것도 안 함"; exit 3; }
STAMP=$(timeout 5 date -u +%Y%m%dT%H%M%SZ </dev/null 2>/dev/null)
case "$STAMP" in [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]T[0-9][0-9][0-9][0-9][0-9][0-9]Z) ;; *) say "UTC 시각을 못 읽음 — 아무것도 안 함"; exit 3;; esac
D=''; NAME=''
for sfx in '' _2 _3 _4 _5; do
  if timeout 10 mkdir -- "$HOME/mixer_e0_meta_$STAMP$sfx" </dev/null 2>/dev/null; then NAME="mixer_e0_meta_$STAMP$sfx"; D="$HOME/$NAME"; break; fi
done
[ -n "$D" ] || { say "새 폴더를 못 만듦 (이미 있음 · 권한 · 디스크) — 아무것도 안 함"; exit 3; }
timeout 10 mkdir -- "$D/raw" "$D/out" "$D/work" "$D/work/tmp" </dev/null 2>/dev/null || { say "하위 폴더를 못 만듦 — 멈춤 (만든 폴더 ~/$NAME)"; exit 3; }
export TMPDIR="$D/work/tmp"
FR="$D/raw/fields.txt"; PR="$D/raw/probes.txt"; HR="$D/raw/hashes.txt"; WR="$D/raw/walk.txt"
: > "$FR"; : > "$PR"; : > "$HR"; : > "$WR"
printf '%s' "$SELF_TEXT" > "$D/raw/meta_script.sh"
say "── 믹서 E0 메타 수집 시작 · 폴더 ~/$NAME · 최대 $BUDGET 초 · 읽기 전용 (제출 · 취소 · 지우기 없음)"

# ── 도우미
put() { local v=${2-}; v=${v//$'\n'/ }; v=${v//$'\r'/ }; printf '%s=%s\n' "$1" "$v" >> "$FR"; }
over() { [ "$SECONDS" -ge "$BUDGET" ]; }
probe() {  # probe <이름> <초> <명령...> → raw/<이름>.txt (stdout+stderr · 상한 CAP) · raw/probes.txt 한 줄 · 반환 = 명령 rc
  local name=$1 secs=$2 f t0 rc st by
  shift 2
  f="$D/raw/$name.txt"
  if over; then printf '%s|SKIPPED_BUDGET|-|0|0|%s\n' "$name" "${1##*/}" >> "$PR"; return 200; fi
  command -v -- "$1" >/dev/null 2>&1 || { printf '%s|MISSING|-|0|0|%s\n' "$name" "${1##*/}" >> "$PR"; return 127; }
  t0=$SECONDS
  timeout $TK "$secs" "$@" </dev/null 2>&1 | timeout 900 head -c "$CAP" > "$f"
  rc=${PIPESTATUS[0]}
  by=$(timeout 10 wc -c < "$f" 2>/dev/null); by=${by//[^0-9]/}
  case "$rc" in 0) st=OK;; 124|137) st=TIMEOUT;; 126|127) st=MISSING;; 141) st=TRUNC;; *) st=FAIL;; esac
  [ "$st" = OK ] && [ "${by:-0}" -ge "$CAP" ] && st=TRUNC
  printf '%s|%s|%s|%s|%s|%s\n' "$name" "$st" "$rc" "$((SECONDS - t0))" "${by:-0}" "${1##*/}" >> "$PR"
  return "$rc"
}
cls() { if [ "$1" = "$2" ]; then printf self; elif [ "$1" = 0 ]; then printf root; else printf other; fi; }
wbit() { case "$1" in 2|3|6|7) printf yes;; *) printf no;; esac; }
st_short() {  # → 종류|모드|소유|그룹|gw=..|ow=..  (소유 · 그룹 = self / root / other — 이름은 쓰지 않는다) · 없으면 ABSENT
  local s t m u g
  s=$(timeout 10 stat -c '%F|%a|%u|%g' -- "$1" </dev/null 2>/dev/null) || { printf 'ABSENT'; return 1; }
  t=${s%%|*}; s=${s#*|}; m=${s%%|*}; s=${s#*|}; u=${s%%|*}; g=${s#*|}
  printf '%s|%s|%s|%s|gw=%s|ow=%s' "$t" "$m" "$(cls "$u" "$MYUID")" "$(cls "$g" "$MYGID")" "$(wbit "${m: -2:1}")" "$(wbit "${m: -1}")"
}
st_full() {  # → 종류|모드|소유|그룹|바이트|mtime|ctime|dev|inode
  local s t m u g r
  s=$(timeout 10 stat -c '%F|%a|%u|%g|%s|%Y|%Z|%d|%i' -- "$1" </dev/null 2>/dev/null) || { printf 'ABSENT'; return 1; }
  t=${s%%|*}; s=${s#*|}; m=${s%%|*}; s=${s#*|}; u=${s%%|*}; s=${s#*|}; g=${s%%|*}; r=${s#*|}
  printf '%s|%s|%s|%s|%s' "$t" "$m" "$(cls "$u" "$MYUID")" "$(cls "$g" "$MYGID")" "$r"
}
hsh() {  # hsh <역할> <경로> [최대 바이트] → raw/hashes.txt: 역할|sha256 또는 사유|바이트|mtime|경로 · 성공이면 sha256 출력
  local role=$1 p=$2 max=${3:-52428800} s t sz mt h a
  if over; then printf '%s|SKIPPED_BUDGET|||%s\n' "$role" "$p" >> "$HR"; return 1; fi
  s=$(timeout 10 stat -c '%F|%s|%Y' -- "$p" </dev/null 2>/dev/null) || { printf '%s|ABSENT|||%s\n' "$role" "$p" >> "$HR"; return 1; }
  t=${s%%|*}; s=${s#*|}; sz=${s%%|*}; mt=${s#*|}
  case "$t" in 'regular file'|'regular empty file') ;; *) printf '%s|NOT_REGULAR:%s|%s|%s|%s\n' "$role" "$t" "$sz" "$mt" "$p" >> "$HR"; return 1;; esac
  if [ "$sz" -gt "$max" ]; then printf '%s|TOO_BIG|%s|%s|%s\n' "$role" "$sz" "$mt" "$p" >> "$HR"; return 1; fi
  h=$(timeout 300 sha256sum -- "$p" </dev/null 2>/dev/null); h=${h%% *}
  case "$h" in ''|*[^0-9a-f]*) printf '%s|HASH_FAIL|%s|%s|%s\n' "$role" "$sz" "$mt" "$p" >> "$HR"; return 1;; esac
  [ "${#h}" -eq 64 ] || { printf '%s|HASH_FAIL|%s|%s|%s\n' "$role" "$sz" "$mt" "$p" >> "$HR"; return 1; }
  a=$(timeout 10 stat -c '%F|%s|%Y' -- "$p" </dev/null 2>/dev/null)
  [ "$a" = "$t|$sz|$mt" ] || { printf '%s|CHANGED_DURING_HASH|%s|%s|%s\n' "$role" "$sz" "$mt" "$p" >> "$HR"; return 1; }
  printf '%s|%s|%s|%s|%s\n' "$role" "$h" "$sz" "$mt" "$p" >> "$HR"
  printf '%s' "$h"
}
cnt() { local c; c=$(timeout 60 find "$1" -mindepth 1 -maxdepth 1 -printf x </dev/null 2>/dev/null | timeout 60 wc -c 2>/dev/null); c=${c//[^0-9]/}; printf '%s' "${c:-ERR}"; }
walk() {  # walk <역할> <절대경로> → raw/walk.txt: 역할|접두|종류|모드|소유|그룹|gw|ow|링크 대상 (조상마다 · 읽기만)
  local role=$1 p=$2 cur='' rest comp s lt
  case "$p" in /*) ;; *) printf '%s|%s|NOT_ABSOLUTE\n' "$role" "$p" >> "$WR"; return 0;; esac
  rest=${p#/}
  printf '%s|/|%s|\n' "$role" "$(st_short /)" >> "$WR"
  while [ -n "$rest" ]; do
    comp=${rest%%/*}
    case "$rest" in */*) rest=${rest#*/};; *) rest='';; esac
    [ -n "$comp" ] || continue
    cur="$cur/$comp"
    s=$(st_short "$cur"); lt=''
    case "$s" in 'symbolic link|'*) lt=$(timeout 10 readlink -- "$cur" </dev/null 2>/dev/null);; esac
    printf '%s|%s|%s|%s\n' "$role" "$cur" "$s" "$lt" >> "$WR"
    case "$s" in ABSENT*) break;; esac
  done
}
banner_of() { timeout 10 head -c 8192 -- "$1" </dev/null 2>/dev/null | timeout 10 grep -a -m 1 -E '^(LIGGGHTS|LAMMPS) \(' 2>/dev/null; }
red_file() { MIX_REMOTE=${3:-0} timeout 60 awk "$AWK_RED" "$1" > "$2" 2>/dev/null; }
red_str() { printf '%s\n' "$1" | MIX_REMOTE=${2:-0} timeout 10 awk "$AWK_RED" 2>/dev/null; }

# ── 신원 (원문은 raw/private_identity.txt 에만 — out/ 로 복사하지 않는다) · 가림 토큰
MYUID=$(timeout 5 id -u </dev/null 2>/dev/null); MYGID=$(timeout 5 id -g </dev/null 2>/dev/null)
IDN=$(timeout 5 id -un </dev/null 2>/dev/null)
ME=${USER-}; [ -n "$ME" ] || ME=$IDN
HOST_F=$(timeout 10 hostname -f </dev/null 2>/dev/null); HOST_S=$(timeout 10 hostname -s </dev/null 2>/dev/null)
[ -n "$HOST_S" ] || HOST_S=$(timeout 5 uname -n </dev/null 2>/dev/null)
HOME_REAL=$(cd -P -- "$HOME" 2>/dev/null && pwd -P)
printf 'user=%s\nid_un=%s\nuid=%s\ngid=%s\nhost_f=%s\nhost_s=%s\nhome=%s\nhome_real=%s\n' "$ME" "$IDN" "$MYUID" "$MYGID" "$HOST_F" "$HOST_S" "$HOME" "$HOME_REAL" > "$D/raw/private_identity.txt"
TOKV=(); ti=0
addtok() { [ "${#1}" -ge 2 ] || return 0; ti=$((ti + 1)); export "MIX_T$ti=$1" "MIX_R$ti=$2" "MIX_W$ti=$3"; TOKV+=("$1"); }
if [ "${#HOME_REAL}" -gt "${#HOME}" ]; then addtok "$HOME_REAL" '<HOME_REAL>' 0; addtok "$HOME" '<HOME>' 0
else addtok "$HOME" '<HOME>' 0; [ "$HOME_REAL" = "$HOME" ] || addtok "$HOME_REAL" '<HOME_REAL>' 0; fi
[ "$HOST_F" = "$HOST_S" ] || addtok "$HOST_F" '<HOST>' 1
addtok "$HOST_S" '<HOST>' 1
addtok "$ME" '<USER>' 1
[ "$IDN" = "$ME" ] || addtok "$IDN" '<USER>' 1
if [ "$HOME_REAL" = "$HOME" ]; then REL=same
elif [ -z "$HOME_REAL" ]; then REL=unknown
elif [ "${HOME_REAL%"$HOME"}" = "$HOME_REAL" ]; then REL=different
else REL="prefix:${HOME_REAL%"$HOME"}"; fi

# ── 실행 메타 (R0 일부)
T_START=$(timeout 5 date -u +%Y-%m-%dT%H:%M:%SZ </dev/null 2>/dev/null)
put format "$FORMAT"; put block_id "$BLOCK_ID"; put target_alias ibb; put folder "~/$NAME"
put captured_start_utc "$T_START"; put home_real_relation "$REL"; put bash_version "$BASH_VERSION"
put timeout_kill_after "${TK:-unsupported}"; put budget_seconds "$BUDGET"
put switch.MIX_BIN_HELP "$BIN_HELP"; put switch.MIX_SLURM "$SLURM_ON"; put redaction_tokens "$ti"
x=$(timeout 10 md5sum -- "$D/raw/meta_script.sh" </dev/null 2>/dev/null); put script_md5 "${x%% *}"
x=$(timeout 10 sha256sum -- "$D/raw/meta_script.sh" </dev/null 2>/dev/null); put script_sha256 "${x%% *}"
put script_bytes "${#SELF_TEXT}"
for t in stat readlink find sha256sum md5sum awk grep head wc tr cut tar gzip du df file ldd git python3 findmnt getfacl quota lfs sinfo squeue sacctmgr hostname id date uname printenv; do
  command -v "$t" >/dev/null 2>&1 && put "tool.$t" present || put "tool.$t" MISSING
done
ALLOC=no; [ -n "${SLURM_JOB_ID-}" ] && ALLOC=yes; put inside_slurm_allocation "$ALLOC"
put env.mpi_slurm_var_names "$(compgen -e | timeout 5 grep -E '^(SLURM_|OMPI_|PMIX_|PRTE_|I_MPI_|MPICH|HYDRA)' | timeout 5 tr '\n' ' ')"
for v in PATH LD_LIBRARY_PATH CONDA_DEFAULT_ENV CONDA_PREFIX CONDA_EXE OMP_NUM_THREADS MKL_NUM_THREADS OPENBLAS_NUM_THREADS LOADEDMODULES MODULEPATH LMOD_VERSION MODULESHOME SHELL LMP; do
  x=$(timeout 5 printenv "$v" </dev/null 2>/dev/null) || x=UNSET
  put "env.$v" "$x"
done
if type module >/dev/null 2>&1; then probe module_list 30 bash -c 'module list 2>&1' >/dev/null
else printf 'module_list|MISSING|-|0|0|module(function)\n' >> "$PR"; fi
probe os_uname 10 uname -srm >/dev/null
probe os_release 10 cat /etc/os-release >/dev/null
probe os_glibc 10 ldd --version >/dev/null
probe tool_git 10 git --version >/dev/null
probe tool_tar 10 tar --version >/dev/null

# ── 체크아웃 (git 읽기 명령만: rev-parse · symbolic-ref · log · status --no-optional-locks · diff-index · ls-files)
REPOS=(); MIXD=()
add_repo() { local r x; r=$(timeout 10 readlink -e -- "$1" </dev/null 2>/dev/null) || return 0; for x in "${REPOS[@]}"; do [ "$x" = "$r" ] && return 0; done; REPOS+=("$r"); }
[ -n "${MIX_REPO-}" ] && add_repo "$MIX_REPO"
add_repo "$HOME/Yonghoon-DEM-DFT"
probe private_home_dirs 60 find "$HOME" -mindepth 1 -maxdepth 1 -type d -print >/dev/null
if [ -s "$D/raw/private_home_dirs.txt" ]; then
  while IFS= read -r dd; do
    case "$dd" in "$HOME"/mixer_e0_meta_*) continue;; esac
    timeout 10 stat -c %F -- "$dd/dem_scripts/mixer_20260921/launch_highbo.sh" </dev/null >/dev/null 2>&1 && add_repo "$dd"
  done < "$D/raw/private_home_dirs.txt"
fi
KEYF='dem_scripts/mixer_20260921/launch_highbo.sh dem_scripts/mixer_20260921/launch_policy.json dem_scripts/mixer_20260921/start_check.py'
KEYF="$KEYF dem_scripts/mixer_20260921/run_all.sh dem_scripts/mixer_20260921/resume_all.sh"
KEYF="$KEYF dem_scripts/mixer_20260919/Drum.stl dem_scripts/mixer_20260919/Front.stl dem_scripts/mixer_20260919/Back.stl"
KEYF="$KEYF scripts/mixer_stage_gate.py scripts/mixer_smoke_blind.py scripts/mixer_deck_diff.py scripts/mixer_deck_readback.py"
KEYF="$KEYF scripts/make_mixer_deck.py scripts/measure_mixing_index.py scripts/check_contact_validity.py"
KEYF="$KEYF scripts/mixer_precal_prepare.py scripts/mixer_precal_observe.py"
k=0
for r in "${REPOS[@]}"; do
  k=$((k + 1)); put "repo$k.path" "$r"
  ( cd -- "$r" 2>/dev/null || exit 0
    probe "repo${k}_head" 20 git rev-parse HEAD >/dev/null
    probe "repo${k}_branch" 20 git symbolic-ref -q --short HEAD >/dev/null
    probe "repo${k}_log1" 20 git log -1 --no-color '--format=%H|%ct' >/dev/null
    # status 는 색인을 새로 쓰지 않는 판 (git 2.15+ --no-optional-locks) 만 · 안 되면 plumbing 둘 (색인 안 씀) 로 대신
    probe "repo${k}_status" 120 git --no-optional-locks status --porcelain --untracked-files=normal >/dev/null && exit 0
    probe "repo${k}_diff_index" 120 git diff-index --name-status HEAD -- >/dev/null
    probe "repo${k}_untracked" 120 git ls-files -o --exclude-standard --directory >/dev/null )
  for f in $KEYF; do hsh "repo$k:$f" "$r/$f" >/dev/null; done
  MIXD+=("$r/dem_scripts/mixer_20260921/runs")
  walk "repo$k" "$r"
done
put n_repos "$k"

# ── 믹서 폴더 (DEV 런 · 확인 블록 · first8 후보) — 목록 · 크기 · 봉인 파일 sha256.  덤프 · 로그 · 숨은 금고 (.e0_diag · .smoke_blind) 는 열지 않는다 (개수만)
MIXD+=("$HOME/mixer_dev7_20260930" "$HOME/mixer_dev7_20260930_v26" "$HOME/mixer_precal_first8_20261106")
probe home_mixer_dirs 60 find "$HOME" -mindepth 1 -maxdepth 1 -name 'mixer*' -print >/dev/null
if [ -s "$D/raw/home_mixer_dirs.txt" ]; then
  while IFS= read -r dd; do case "$dd" in "$HOME"/mixer_e0_meta_*) ;; *) MIXD+=("$dd");; esac; done < "$D/raw/home_mixer_dirs.txt"
fi
SEALS=(); DIAGS=(); SEENM=()
scan_run() {  # scan_run <폴더 번호> <런 번호> <런 폴더>
  local tag="mix${1}_run${2}" r=$3 ty sz mt name
  put "$tag.path" "$r"
  probe "${tag}_ls" 60 find "$r" -mindepth 1 -maxdepth 1 -printf '%y|%s|%T@|%f\n' >/dev/null || return 0
  while IFS='|' read -r ty sz mt name; do
    case "$ty" in
      f) case "$name" in
           in.mixer|deck_meta.json|Drum.stl|Front.stl|Back.stl|jobid|*.sbatch|n_expected|r_container|release_approval.json) hsh "$tag:$name" "$r/$name" >/dev/null;;
           launch_record*.json|job_start*.json) hsh "$tag:$name" "$r/$name" >/dev/null; SEALS+=("$r/$name");;
           log.lmp|log.liggghts) put "$tag.$name.bytes" "$sz"; put "$tag.$name.banner" "$(banner_of "$r/$name")";;
         esac;;
      d) case "$name" in .*) put "$tag.hidden.$name.entries" "$(cnt "$r/$name")";; *) put "$tag.dir.$name.entries" "$(cnt "$r/$name")";; esac;;
      l) put "$tag.symlink.$name" "$(timeout 10 readlink -- "$r/$name" </dev/null 2>/dev/null)";;
    esac
  done < "$D/raw/${tag}_ls.txt"
}
scan_mixdir() {  # scan_mixdir <번호> <폴더>
  local i=$1 m=$2 ty sz mt name n=0
  probe "mix${i}_ls" 60 find "$m" -mindepth 1 -maxdepth 1 -printf '%y|%s|%T@|%f\n' >/dev/null || return 0
  while IFS='|' read -r ty sz mt name; do
    case "$ty" in
      d) case "$name" in
           .stage_gate) probe "mix${i}_stage_gate_ls" 30 find "$m/$name" -mindepth 1 -maxdepth 1 -type f -name '*.json' -printf '%f\n' >/dev/null
                        if [ -s "$D/raw/mix${i}_stage_gate_ls.txt" ]; then
                          while IFS= read -r sg; do hsh "mix$i:.stage_gate/$sg" "$m/$name/$sg" 5242880 >/dev/null; done < "$D/raw/mix${i}_stage_gate_ls.txt"
                        fi;;
           .*) put "mix$i.hidden.$name.entries" "$(cnt "$m/$name")";;
           *) n=$((n + 1)); [ "$n" -le 200 ] && scan_run "$i" "$n" "$m/$name";;
         esac;;
      f) case "$name" in
           dev_e0_diag*.json) hsh "mix$i:$name" "$m/$name" >/dev/null; DIAGS+=("$m/$name");;
           *.json|*.txt|*.sh|*.sbatch|*.liggghts|*.csv|*.tsv|SHA256SUMS*) hsh "mix$i:$name" "$m/$name" >/dev/null;;
           *) put "mix$i.other_file.$name.bytes" "$sz";;
         esac;;
      l) put "mix$i.symlink.$name" "$(timeout 10 readlink -- "$m/$name" </dev/null 2>/dev/null)";;
    esac
  done < "$D/raw/mix${i}_ls.txt"
  put "mix$i.n_subdirs" "$n"
}
i=0; na=0
for m in "${MIXD[@]}"; do
  mreal=$(timeout 10 readlink -e -- "$m" </dev/null 2>/dev/null) || { na=$((na + 1)); put "mixdir.absent$na" "$m"; continue; }
  dup=0; for x in "${SEENM[@]}"; do [ "$x" = "$mreal" ] && dup=1; done
  [ "$dup" = 1 ] && continue
  SEENM+=("$mreal"); i=$((i + 1)); put "mix$i.path" "$m"; put "mix$i.realpath" "$mreal"; put "mix$i.stat" "$(st_short "$mreal")"
  case "$(st_short "$mreal")" in directory*) scan_mixdir "$i" "$mreal";; *) hsh "mix$i:self" "$mreal" >/dev/null;; esac
  walk "mix$i" "$mreal"
done
put n_mixdirs "$i"
F8="$HOME/mixer_precal_first8_20261106"
h=$(hsh "first8:cases/PRECAL_E0/in.mixer" "$F8/cases/PRECAL_E0/in.mixer")
if [ -z "$h" ]; then put first8.e0_deck_vs_static absent
elif [ "$h" = "$REF_E0_DECK" ]; then put first8.e0_deck_vs_static same
else put first8.e0_deck_vs_static different; fi
if [ "${#SEALS[@]}" -gt 0 ]; then probe seal_extract 90 python3 -I -B -c "$PY_SEAL" seal "${SEALS[@]}" >/dev/null; fi
if [ "${#DIAGS[@]}" -gt 0 ]; then probe diag_extract 60 python3 -I -B -c "$PY_SEAL" diag "${DIAGS[@]}" >/dev/null; fi
put n_seal_files "${#SEALS[@]}"; put n_diag_files "${#DIAGS[@]}"

# ── LIGGGHTS 실행 파일 후보 (환경 LMP · PATH · 알려진 자리 · 봉인에 적힌 자리) → 실제 경로 하나마다 stat · sha256 · 배너 · ldd · -h
LMPC=(); MPIC=(); PYC=()
if [ -n "${LMP-}" ]; then x=$(command -v -- "$LMP" 2>/dev/null) && LMPC+=("$x") || LMPC+=("$LMP"); fi
x=$(command -v lmp_mpi 2>/dev/null) && LMPC+=("$x")
LMPC+=("$HOME/LIGGGHTS-PUBLIC/src/lmp_mpi" "/lustre/home/$ME/LIGGGHTS-PUBLIC/src/lmp_mpi")
if [ -s "$D/raw/seal_extract.txt" ]; then
  while IFS='|' read -r sp sk sv; do
    sv=${sv#\"}; sv=${sv%\"}
    case "$sk" in
      lmp_path|lmp_realpath) LMPC+=("$sv");;
      slurm.path_prefix) rest=$sv
        while [ -n "$rest" ]; do d1=${rest%%:*}; case "$rest" in *:*) rest=${rest#*:};; *) rest='';; esac
          [ -n "$d1" ] && { LMPC+=("$d1/lmp_mpi"); MPIC+=("$d1/mpirun"); }; done;;
    esac
  done < "$D/raw/seal_extract.txt"
fi
LMPU=(); LMPF=(); k=0
for c in "${LMPC[@]}"; do
  k=$((k + 1)); r=$(timeout 10 readlink -e -- "$c" </dev/null 2>/dev/null) || r=''
  put "lmp.candidate$k" "$c => ${r:-UNRESOLVED}"
  [ -n "$r" ] || continue
  dup=0; for x in "${LMPU[@]}"; do [ "$x" = "$r" ] && dup=1; done
  [ "$dup" = 1 ] || { LMPU+=("$r"); LMPF+=("$c"); }
done
put lmp.n_candidates "$k"; put lmp.n_unique_found "${#LMPU[@]}"
lib_hashes() {  # lib_hashes <k> — ldd 가 푼 경로마다 sha256 (읽기만 · 최대 150)
  local k=$1 n=0 l p
  while IFS= read -r l; do
    p=''
    case "$l" in
      *'=> not found'*) put "lmp$k.lib_not_found" "${l%% =>*}"; continue;;
      *'=> /'*) p=${l#*=> }; p=${p%% (*};;
      [[:space:]]/*) p=${l#"${l%%[^[:space:]]*}"}; p=${p%% (*};;
    esac
    [ -n "$p" ] || continue
    n=$((n + 1)); [ "$n" -le 150 ] || break
    hsh "lmp$k.lib" "$p" 1073741824 >/dev/null
  done < "$D/raw/lmp${k}_ldd.txt"
  put "lmp$k.n_libs_hashed" "$n"
}
LMPH=(); k=0
for b in "${LMPU[@]}"; do
  k=$((k + 1)); put "lmp$k.realpath" "$b"; put "lmp$k.first_candidate" "${LMPF[$((k - 1))]}"; put "lmp$k.stat" "$(st_full "$b")"
  h=$(hsh "lmp$k" "$b" 4294967296); LMPH+=("${h:-NONE}")
  if [ -n "$h" ]; then
    put "lmp$k.sha256" "$h"
    if [ "$h" = "$REF_LMP_0928" ]; then put "lmp$k.vs_receipt_v2_ibb_20260928" same; else put "lmp$k.vs_receipt_v2_ibb_20260928" different; fi
  fi
  probe "lmp${k}_file" 20 file -b -- "$b" >/dev/null
  probe "lmp${k}_banner_static" 60 grep -a -o -m 3 -E 'Version LIGGGHTS[ -~]{0,200}' -- "$b" >/dev/null
  probe "lmp${k}_ldd" 30 ldd -- "$b" >/dev/null && lib_hashes "$k"
  if [ "$BIN_HELP" = 0 ]; then printf 'lmp%s_help|SKIPPED_SWITCH|-|0|0|%s\n' "$k" "${b##*/}" >> "$PR"
  else ( cd "$D/work" && probe "lmp${k}_help" 30 "$b" -log none -h >/dev/null ); fi
  walk "lmp$k" "$b"
done
put work.files_after_help "$(timeout 10 find "$D/work" -mindepth 1 -printf '%P ' </dev/null 2>/dev/null)"

# ── MPI launcher 후보 (PATH · conda env · 봉인 path_prefix) → 실제 경로 하나마다 stat · sha256 · --version
x=$(command -v mpirun 2>/dev/null) && MPIC+=("$x")
x=$(command -v mpiexec 2>/dev/null) && MPIC+=("$x")
ENVS=("$HOME/.conda/envs/myenv" "$HOME/miniconda3/envs/myenv" "$HOME/anaconda3/envs/myenv")
[ -n "${CONDA_PREFIX-}" ] && ENVS+=("$CONDA_PREFIX")
for e in "${ENVS[@]}"; do MPIC+=("$e/bin/mpirun"); PYC+=("$e/bin/python3"); done
MPIU=(); MPIF=(); k=0
for c in "${MPIC[@]}"; do
  k=$((k + 1)); r=$(timeout 10 readlink -e -- "$c" </dev/null 2>/dev/null) || r=''
  put "mpi.candidate$k" "$c => ${r:-UNRESOLVED}"
  [ -n "$r" ] || continue
  dup=0; for x in "${MPIU[@]}"; do [ "$x" = "$r" ] && dup=1; done
  [ "$dup" = 1 ] || { MPIU+=("$r"); MPIF+=("$c"); }
done
put mpi.n_candidates "$k"; put mpi.n_unique_found "${#MPIU[@]}"
k=0
for b in "${MPIU[@]}"; do
  k=$((k + 1)); c=${MPIF[$((k - 1))]}
  put "mpi$k.realpath" "$b"; put "mpi$k.first_candidate" "$c"; put "mpi$k.stat" "$(st_full "$b")"
  h=$(hsh "mpi$k" "$b" 1073741824); [ -n "$h" ] && put "mpi$k.sha256" "$h"
  probe "mpi${k}_version" 20 "$c" --version >/dev/null
  walk "mpi$k" "$c"
done

# ── python3 (PATH · conda env) → 판 · numpy · scipy (-I -B: 사용자 경로 무시 · .pyc 안 씀)
x=$(command -v python3 2>/dev/null) && PYC=("$x" "${PYC[@]}")
PYU=(); PYF=(); k=0
for c in "${PYC[@]}"; do
  k=$((k + 1)); r=$(timeout 10 readlink -e -- "$c" </dev/null 2>/dev/null) || r=''
  put "py.candidate$k" "$c => ${r:-UNRESOLVED}"
  [ -n "$r" ] || continue
  dup=0; for x in "${PYU[@]}"; do [ "$x" = "$r" ] && dup=1; done
  [ "$dup" = 1 ] || { PYU+=("$r"); PYF+=("$c"); }
done
k=0
for b in "${PYU[@]}"; do
  k=$((k + 1)); c=${PYF[$((k - 1))]}
  put "py$k.realpath" "$b"; put "py$k.first_candidate" "$c"
  h=$(hsh "py$k" "$b" 1073741824); [ -n "$h" ] && put "py$k.sha256" "$h"
  probe "py${k}_version" 30 "$c" -I -B -c "$PY_VER" >/dev/null
  probe "py${k}_modules" 90 "$c" -I -B -c "$PY_MODS" >/dev/null
done
k=0; SEENE=()
for e in "${ENVS[@]}"; do
  er=$(timeout 10 readlink -e -- "$e" </dev/null 2>/dev/null) || { put conda.absent "$e"; continue; }
  dup=0; for x in "${SEENE[@]}"; do [ "$x" = "$er" ] && dup=1; done
  [ "$dup" = 1 ] && continue
  SEENE+=("$er"); k=$((k + 1)); put "conda$k.path" "$e"
  probe "conda${k}_meta" 30 find "$er/conda-meta" -mindepth 1 -maxdepth 1 -name '*.json' -printf '%f\n' >/dev/null
done

# ── SLURM (읽기 조회만: sinfo · sacctmgr show · squeue -u 나) — 실패를 빈 큐로 읽지 않는다
if [ "$SLURM_ON" = 0 ]; then printf 'slurm|SKIPPED_SWITCH|-|0|0|-\n' >> "$PR"
else
  probe slurm_sinfo_version 20 sinfo -V >/dev/null
  probe slurm_sinfo_partitions 30 sinfo -h -o '%P|%a|%l|%D|%c|%m|%t|%G' >/dev/null
  probe slurm_sinfo_summary 30 sinfo -s >/dev/null
  probe slurm_qos 30 sacctmgr -n -P show qos format=Name,Priority,MaxWall,MaxTRESPU,MaxJobsPU,MaxSubmitPU,GrpTRES,MaxTRES >/dev/null
  probe slurm_assoc_me 30 sacctmgr -n -P show assoc where "user=$ME" format=User,Partition,QOS,DefaultQOS,MaxJobs,MaxSubmit,MaxTRES,GrpTRES,MaxWall >/dev/null
  probe slurm_squeue_me 30 squeue -h -u "$ME" -o '%i|%j|%T|%C|%q|%P|%M|%l|%R|%S|%V' >/dev/null; qrc=$?
  put slurm.squeue_rc "$qrc"
  AWK_Q='$1 ~ /^[0-9]/ { n++; c[$3] += 1; u[$3] += $4; q[$5 ":" $3] += $4 }
END { printf "jobs=%d", n; for (s in c) printf " %s=%d(cpus %d)", s, c[s], u[s]; for (s in q) printf " qos:%s=cpus %d", s, q[s] }'
  if [ "$qrc" = 0 ]; then
    put slurm.my_jobs_summary "$(timeout 10 awk -F'|' "$AWK_Q" "$D/raw/slurm_squeue_me.txt")"
  else put slurm.my_jobs_summary "UNKNOWN (squeue rc $qrc — 없음 · 실패를 빈 큐로 읽지 않는다)"; fi
fi

# ── 디스크 · quota · 마운트 (가용량 = 시점 관측 · quota · 회수 예산을 대신하지 않는다)
DMNT=''; DFST=''
disk_probe() {  # disk_probe <태그> <경로>
  local mnt fst
  probe "df_${1}_bytes" 30 df -PB1 -- "$2" >/dev/null
  probe "df_${1}_inodes" 30 df -Pi -- "$2" >/dev/null
  mnt=$(timeout 10 df -P -- "$2" </dev/null 2>/dev/null | timeout 5 awk 'NR == 2 { print $NF }')
  fst=$(timeout 10 stat -f -c %T -- "$2" </dev/null 2>/dev/null)
  put "disk.$1.mount" "$mnt"; put "disk.$1.fstype" "$fst"
  DMNT=$mnt; DFST=$fst
}
disk_probe home "$HOME"
probe df_home_human 30 df -h -- "$HOME" >/dev/null
probe findmnt_home 20 findmnt -n -T "$HOME" -o TARGET,FSTYPE,OPTIONS,SOURCE >/dev/null
probe quota_s 30 quota -s >/dev/null
case "$DFST" in lustre*) probe lfs_quota_home 60 lfs quota -u "$ME" "$DMNT" >/dev/null;; *) printf 'lfs_quota_home|SKIPPED_NOT_LUSTRE|-|0|0|lfs\n' >> "$PR";; esac
k=0; for m in "${SEENM[@]}"; do k=$((k + 1)); disk_probe "mix$k" "$m"; done

# ── 권한 · 링크 (ACL 은 이름 붙은 항목 수만 · 원문은 private) · 조상 경로 walk
if command -v getfacl >/dev/null 2>&1; then
  k=0
  for p in "$HOME" "${LMPU[@]}" "${SEENM[@]}" "${REPOS[@]}"; do
    k=$((k + 1)); put "acl$k.path" "$p"
    if probe "private_acl$k" 10 getfacl -n -p --omit-header -- "$p" >/dev/null; then
      c=$(timeout 10 grep -c -E '^(default:)?(user|group):[0-9]+:' "$D/raw/private_acl$k.txt" 2>/dev/null); put "acl$k.named_entries" "${c:-ERR}"
    else put "acl$k.named_entries" UNKNOWN; fi
  done
else printf 'acl|MISSING|-|0|0|getfacl\n' >> "$PR"; fi
walk home "$HOME"

# ── 무거운 것은 맨 뒤 (예산이 남을 때만): 믹서 폴더 크기 du
k=0; for m in "${SEENM[@]}"; do k=$((k + 1)); probe "mix${k}_du" 120 du -sk -- "$m" >/dev/null; done

# ── 끝: 기록 → 가린 사본 out/ → 남은 문자열 확인 → SHA256SUMS → tgz
T_END=$(timeout 5 date -u +%Y-%m-%dT%H:%M:%SZ </dev/null 2>/dev/null)
put captured_end_utc "$T_END"; put elapsed_seconds "$SECONDS"
put probe_status_counts "$(timeout 10 awk -F'|' '{ c[$2]++ } END { for (s in c) printf "%s=%d ", s, c[s] }' "$PR")"
RED_OK=0; command -v awk >/dev/null 2>&1 && RED_OK=1
RAWL=()
for f in "$D"/raw/*; do
  b=${f##*/}
  case "$b" in private_*) continue;; esac
  RAWL+=("$b")
  [ "$b" = meta_script.sh ] && continue
  case "$b" in df_*|findmnt_*|quota_*|lfs_*) rem=1;; *) rem=0;; esac
  if [ "$RED_OK" = 1 ]; then red_file "$f" "$D/out/$b" "$rem" || printf 'redact_fail=%s\n' "$b" >> "$D/out/fields_post.txt"; fi
done
[ "$RED_OK" = 1 ] || timeout 10 cp -- "$D/raw/probes.txt" "$D/out/probes.txt"
printf '%s' "$SELF_TEXT" > "$D/out/meta_script.sh"
RES=0
for tv in "${TOKV[@]}"; do
  c=$(timeout 30 grep -r -F -c --exclude=meta_script.sh -- "$tv" "$D/out" 2>/dev/null | timeout 10 awk -F: '{ s += $NF } END { print s + 0 }')
  RES=$((RES + ${c:-0}))
done
printf 'redaction.available=%s\nredaction.residual_token_hits=%s\n' "$RED_OK" "$RES" >> "$D/out/fields_post.txt"
( cd "$D/raw" && timeout 60 sha256sum -- "${RAWL[@]}" ) > "$D/out/RAW_SHA256SUMS" 2>/dev/null
OUTL=(); for f in "$D"/out/*; do b=${f##*/}; [ "$b" = SHA256SUMS ] || OUTL+=("$b"); done
( cd "$D/out" && timeout 60 sha256sum -- "${OUTL[@]}" ) > "$D/out/SHA256SUMS" 2>/dev/null
TGZ="$D/$NAME.tgz"; TGZ_SHA=''; TGZ_BYTES=''
if timeout 120 tar --owner=0 --group=0 --numeric-owner -czf "$TGZ" -C "$D" out </dev/null 2>"$D/work/tar_err.txt"; then
  x=$(timeout 60 sha256sum -- "$TGZ" </dev/null 2>/dev/null); TGZ_SHA=${x%% *}
  TGZ_BYTES=$(timeout 10 stat -c %s -- "$TGZ" </dev/null 2>/dev/null)
  printf '%s  %s\n' "$TGZ_SHA" "$NAME.tgz" > "$D/$NAME.tgz.sha256"
fi

# ── 화면 (가린 값만 · 경로는 ~/ 로)
say "── 끝 · $SECONDS 초 · 조회 $(timeout 10 awk -F'|' '{ c[$2]++ } END { for (s in c) printf "%s %d  ", s, c[s] }' "$PR")"
if [ "${#LMPU[@]}" = 0 ]; then say "LIGGGHTS   실행 파일 후보를 못 찾음 (후보 칸 = out/fields.txt lmp.candidate*)"; fi
k=0
for b in "${LMPU[@]}"; do
  k=$((k + 1)); h=${LMPH[$((k - 1))]}
  if [ "$h" = "$REF_LMP_0928" ]; then cmp_=같음; elif [ "$h" = NONE ]; then cmp_='해시 없음'; else cmp_=다름; fi
  say "LIGGGHTS $k sha256 ${h:0:16}… · 09-28 영수증 바이너리와 $cmp_ · $(red_str "$(timeout 5 head -n 1 "$D/raw/lmp${k}_banner_static.txt" 2>/dev/null)")"
done
if [ "${#MPIU[@]}" = 0 ]; then say "mpirun     후보를 못 찾음"; else say "mpirun     $(red_str "$(timeout 5 head -n 1 "$D/raw/mpi1_version.txt" 2>/dev/null)")"; fi
if [ "${#PYU[@]}" -gt 0 ]; then say "python3    $(timeout 5 head -n 1 "$D/raw/py1_version.txt" 2>/dev/null) · $(timeout 5 tr '\n' ' ' < "$D/raw/py1_modules.txt" 2>/dev/null)"; fi
say "SLURM      $(timeout 5 grep -m 1 '^slurm.my_jobs_summary=' "$FR" 2>/dev/null | timeout 5 cut -d= -f2-)"
say "디스크     $(red_str "$(timeout 5 tail -n 1 "$D/raw/df_home_human.txt" 2>/dev/null)" 1)"
if [ "$RES" = 0 ]; then say "가림 확인  out/ 에 남은 계정 · 호스트 · 경로 문자열 0 곳"
else say "가림 확인  ⚠ out/ 에 남은 계정 · 호스트 · 경로 문자열 $RES 곳 — tgz 를 넘기기 전에 out/ 을 확인 (가림 실패면 넘기지 말 것)"; fi
if [ -n "$TGZ_SHA" ]; then
  say "가져올 파일 ~/$NAME/$NAME.tgz  ($TGZ_BYTES 바이트 · out/ 만 · 가린 사본)"
  say "sha256     $TGZ_SHA"
else say "⚠ tgz 를 못 만듦 (tar) — ~/$NAME/out/ 폴더를 그대로 가져올 것"; fi
say "raw/ (가리지 않은 원문) 은 ~/$NAME/raw/ 에 남김 — 가져오지 않는다"
