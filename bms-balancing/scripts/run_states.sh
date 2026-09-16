#!/usr/bin/env bash
# 다른 상태 일반화 — `300_0009` 에서 한 것을 100 · 200 · 300_0147 에도 그대로.
#
# 왜 스크립트로 두나: 아홉 번의 실행이 **같은 설정**이어야 비교가 성립한다.
# 손으로 아홉 줄을 치면 한 줄에서 `--starts` 를 흘리는 순간 그 행만 다른
# 조건이 되고, 나중에 그것을 알아챌 방법이 없다. 여기 적힌 플래그가
# 산출의 provenance 다.
#
#   export BMS_DATA_ROOT='/mnt/d/…/degradation mode'
#   ./scripts/run_states.sh                    # 세 상태 전부
#   STATES=100 ./scripts/run_states.sh         # 하나만
#   STARTS=6 STATES=100 ./scripts/run_states.sh   # 배관 확인용 (수치는 못 씀)
#
# 산출은 전부 `out/` 에. 원자료는 하나도 안 들어간다 — 파라미터와 요약뿐이다.

set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$HERE" || exit 1
: "${BMS_DATA_ROOT:?BMS_DATA_ROOT 를 먼저 export 하라}"

STATES="${STATES:-100 200 300_0147}"
STARTS="${STARTS:-24}"
SI="${SI:-Li}"
# SRC 를 주면 그 소스로 **고정**한다 (없으면 그 상태는 건너뛴다).
# 안 주면 상태마다 GITT -> step_005C 순으로 있는 것을 고른다 (pick_src).
FORCE_SRC="${SRC:-}"
USED=""            # 상태별로 실제 무엇을 썼는지 — 마지막에 찍는다
OUT="${OUT:-out}"  # 산출 디렉터리. 시험 실행은 여기를 바꿔서 out/ 을 안 더럽힌다

# ══ DEFS BEGIN ══ 아래부터 `fail=0` 전까지가 **함수 정의**다. 회귀(`tests/test_r10_codex.py`)가 정확히 이 구간을
#    source 해서 production 함수(`run`·`write_meta`·`shape_step`)를 그대로 부른다 — 그래야 그 줄을 위조하는 변이가
#    시험에 잡힌다 (Codex R10 P2-3: 전 판 회귀는 `run()` 을 안 부르고 `LAST_ARGV` 를 직접 주입했다).

# ⚠ 산출마다 **설정을 옆에 적는다** (`.meta.json`). 2026-09-10 실측: 합성
#   데이터로 STARTS=4 짜리 시험을 돌렸더니 `out/matrix_300_0147.csv` 가
#   생겼는데, **파일 이름만으로는 진짜 산출과 구별이 안 됐다.** 정본이
#   artifact 인 저장소에서 그건 치명적이다. 무엇으로 만든 값인지가 파일에
#   붙어 있어야 한다.
# ⚠ Codex R4-06: meta 는 **이번 시도**의 산출에만 붙는다. `run` 이 만든 run id(`LAST_RUN_ID`)가 파일
#   안에 있어야 하고, 없으면 meta 를 쓰지 않는다 — 시각이 아니라 id 가 계산과 게시 bytes 를 잇는다.
# ⚠ Codex R4-07: git_dirty 는 **코드**(산출 디렉터리 밖 추적 파일)만 본다. 산출 디렉터리 안에서 수정된
#   다른 추적 파일은 `git_modified_outputs` 로 따로 적는다 (입력으로 쓰는 artifact 의 변경을 숨기지 않게).
# ⚠ Codex R5-04: 산출 게시와 meta 게시가 한 시도의 **한 묶음**이어야 한다. run id 검사 뒤 meta 를 쓰기 전에 다른
#   시도가 산출을 바꾸면 "CSV 는 B, meta 는 A" 가 남았다. 이제 meta 작성자는 `<산출>.lock`(verify.py 의
#   게시가 잡는 것과 같은 flock) 안에서 id 를 **필드로 다시** 확인하고, 그 순간의 bytes 해시를 meta 에 적는다.
#   실패하면 meta 를 쓰지 않는다 — 마지막 실행의 온전한 묶음만 남는다.
# ⚠ Codex R5-08: id 검사는 grep(파일 어디든 문자열)이 아니라 CSV 의 `run_id` 열 전 행 / JSON 의 `run_id` 필드다.
LAST_RUN_ID=""
write_meta () {  # write_meta <산출파일> <state> <src>   (LAST_RUN_ID 는 직전 run 이 준다)
  local art="$1" st="$2" src="$3" rid="${LAST_RUN_ID:-}"
  if [ -z "$rid" ] || ! check_run_id "$art" "$rid"; then
    say '   %s: run id (%s) 가 산출물의 필드에 없다 — 이번 시도의 산출이 아니므로 meta 를 쓰지 않는다\n' "$art" "${rid:-없음}"
    return 1
  fi
  # ⚠ 자체 리뷰 C09: `python3 -` 는 `sys.path[0]` 이 `''`(cwd) 라 저장소 루트의 untracked `hashlib.py` 가
  #   `from provenance import …` 보다 **먼저** 실행됐다 (실측: 그것이 provenance 를 선주입하면 meta 에
  #   `git_dirty: false` 가 찍힌다 — R11 P1-9 반례 재개방). `-I`(격리) `-P`(cwd 를 path 에 안 넣음)로 부른다.
  if ! python3 -I -P - "$art" "$st" "$src" "$STARTS" "$SI" "${BMS_DATA_ROOT}" "$rid" "${OUT:-out}" \
        "${LAST_PRE_PV:-{\}}" "${LAST_STARTED_UTC:-}" "${LAST_ARGV_JSON:-[]}" <<'PYMETA'
import csv, fcntl, hashlib, io, json, os, sys, datetime, pathlib, tempfile
art, st, src, starts, si, root, rid, out_dir, pre_json, started = sys.argv[1:11]
try:                                                 # Codex R10 P2-3: argv 는 문자열이 아니라 **vector** 다
    argv = json.loads(sys.argv[11]) if len(sys.argv) > 11 else []
    if not isinstance(argv, list):
        argv = []
except json.JSONDecodeError:
    argv = []


try:
    pre = json.loads(pre_json) if pre_json else {}
except json.JSONDecodeError:
    pre = {}
sys.path.insert(0, "scripts")
from provenance import git_provenance, check_run_id_bytes, env_signature   # R4-07 · R5-08 · R5-04 · R6 F3
# ⚠ Codex R11: 명부 유도는 **한 자리**(`bms_balancing.schema.body_roster`) — 전 판은 같은 로직이 여기와 checker 에
#   따로 있었고 둘이 갈리면 사이드카가 본문과 다른 명부를 봉인했다. provenance 모듈이 있는 곳의 부모가 저장소다.
sys.path.insert(0, str(pathlib.Path(git_provenance.__globals__["__file__"]).resolve().parents[1]))
# ⚠ R16 (조건 8 축 ②): **모집단 선언**의 식별자를 사이드카에 적는다 — 어느 dataset manifest 로 roster 를
#   정했는가. 여기서 `bms_balancing.data` 를 import 하지 **않는다**: 이 기록기는 `-I -P` 로 격리 실행되고
#   그 모듈은 pandas 를 끌고 온다 (2026-09-16 실측: `dateutil` 없음으로 meta 가 통째로 안 쓰였다).
#   형식 검사는 producer 가 이미 했다 — 여기서는 **읽어서 식별자만** 만든다 (stdlib).
#   ⚠ 계산이 두 자리에 있으므로 `test_r16_37` 이 둘이 같은 값을 내는지 댄다 (규칙이 두 벌이면 갈린다).
def _dataset_manifest_identity():
    import hashlib
    try:
        raw = pathlib.Path("datasets/half_cell.manifest.json").read_bytes()
        doc = json.loads(raw.decode("utf-8"))
        return {"version": doc["manifest_version"], "dataset_id": doc["dataset_id"],
                "sha256": hashlib.sha256(raw).hexdigest()}
    except Exception:                                 # noqa: BLE001 — 지어내지 않고 null 로 적는다
        return None

roster_err = None
try:
    from bms_balancing.schema import body_roster as roster_of
except ModuleNotFoundError as e:                     # 패키지가 없는 트리(합성 fixture) — 명부를 **지어내지 않는다**
    roster_of, roster_err = None, f"bms_balancing 를 못 찾았다: {e}"

    print(f"   경고: 명부를 유도할 수 없다 ({roster_err}) — meta 에 roster: null 로 적는다 (승격 gate 가 막는다)",
          file=sys.stderr)

with open(art + ".lock", "a+") as lock:
    fcntl.flock(lock, fcntl.LOCK_EX)                                  # verify.py 의 게시와 같은 잠금
    with open(art, "rb") as fh:
        data = fh.read()                                              # 잠금 안 **한 번** 읽은 bytes — id 재확인·sha256·roster 전부
    ok, why = check_run_id_bytes(os.path.basename(art), data, rid)
    if not ok:
        print(f"run id 재확인 실패: {why}", file=sys.stderr); sys.exit(1)
    pv = git_provenance(artifact=art, output_roots=(out_dir, "out"))
    roster = None
    if roster_of:
        try:
            roster = roster_of(pathlib.Path(art).name, data)
        except ValueError as e:      # Codex R13 §Q6: 등록되지 않은 산출 이름 — 명부를 지어내지 않고 meta 도 쓰지 않는다 (fail-closed)
            print(f"산출 이름이 등록된 종류가 아니다 ({e}) — meta 를 쓰지 않는다", file=sys.stderr); sys.exit(1)
    meta = {
        "artifact": pathlib.Path(art).name, "state": st, "half_cell_source": src,
        "si_source": si, "starts": int(starts), "seed": 0, "w_dqdv_note": "명령별",
        "data_root": root, "run_id": rid, "sha256": hashlib.sha256(data).hexdigest(),
        # Codex R9 P2-4: 실제 argv 와 본문에서 유도한 exact 명부 — `si_source`(SI 환경값)·`starts` 는 명부가 아니다
        "argv": argv, "roster": roster,
        **({"roster_error": roster_err} if roster_err else {}),
        "si_source_note": "wrapper 의 SI 환경값 — 본문의 exact 명부는 roster (matrix 는 Si 전부를 돈다)",
        "git_commit": pv["git_commit"], "git_dirty": pv["git_dirty"],
        "git_modified_outputs": pv["git_modified_outputs"], "git_modified_code": pv["git_modified_code"],
        # R6 내부 F04: 계산 **전** 상태도 적고 둘이 다르면 표시한다 — 뒤에서 한 번 샘플한 값은 "돌린 코드가
        #   commit 과 같았나" 에 거짓 답을 줄 수 있다 (실행 중 checkout/커밋).
        "git_commit_at_start": pre.get("git_commit"), "git_dirty_at_start": pre.get("git_dirty"),
        "git_modified_code_at_start": pre.get("git_modified_code"),
        "git_state_changed_during_run": bool(pre) and (
            pre.get("git_commit") != pv["git_commit"] or pre.get("git_dirty") != pv["git_dirty"]
            or pre.get("git_modified_code") != pv["git_modified_code"]),
        "started_utc": started or None,
        "env": env_signature(),                                       # R6 내부 F3: 인터프리터·라이브러리·플랫폼
        # ⚠ R16 (조건 8 축 ②): **모집단 선언**의 식별자. 어느 dataset manifest 로 roster 를 정했는지가
        #   산출에 남아야 한다 — 파일로 옮기기만 하고 안 적으면 나중에 그 파일이 바뀌었을 때 말할 수 없다.
        "dataset_manifest": _dataset_manifest_identity(),   # 못 읽으면 null — 승격 gate 가 막는다
        "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(os.path.abspath(art)), prefix=os.path.basename(art) + ".meta.", suffix=".part")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(meta, ensure_ascii=False, indent=2) + "\n")
    os.replace(tmp, art + ".meta.json")
PYMETA
  then
    say '   %s: 잠금 안 재확인에서 이번 시도의 산출이 아니었다 (다른 시도가 게시함) — meta 를 쓰지 않는다\n' "$art"
    return 1
  fi
}
# R6 내부 F05a·F05b: 게시 뒤 묶음 검사는 **이 시도의 id** 로 하고, 실패 이유는 버리지 않고 말한다
verify_unit_or_say () {  # verify_unit_or_say <산출파일> <run id>
  local why
  if why="$(python3 scripts/provenance.py --verify-unit "$1" "$2" 2>&1)"; then return 0; fi
  say '   %s: 묶음 검사 실패 — %s\n' "$1" "$why"
  return 1
}
mkdir -p "$OUT"

# ⚠ 진행 표시는 **전부 stderr 로**. degeneracy 는 전 판에 JSON 을 stdout 으로 냈고
#   stdout 에 한 줄이라도 찍으면 그 줄이 **JSON 안에 섞였다** (2026-09-10 실측:
#   첫 판이 그랬고, exit code 가 0 이라 스크립트는 "전부 통과" 라고 말했다).
#   R6 내부 F01 부터 degeneracy 도 `--out` 으로 잠금 안 원자적 게시 — stdout 은 로그다.
say () { printf "$@" >&2; }

# R5-08: run id 는 산출물의 **필드**로 확인한다 (CSV 의 run_id 열 전 행 / JSON 의 run_id) — grep 은 다른 칸의 문자열도 통과시켰다
check_run_id () {  # check_run_id <산출파일> <run id>
  python3 scripts/provenance.py --check-run-id "$1" "$2" >/dev/null 2>&1
}

# 종료 코드는 산출이 쓸 만한지 말해 주지 않는다. 실제로 열어서 읽는다.
check_artifact () {
  local f="$1"
  [ -s "$f" ] || { say '   %s: 파일이 비었다\n' "$f"; return 1; }
  case "$f" in
    *.json|*.part)
      python3 -c 'import json,sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
sys.exit(0 if isinstance(d, dict) and d else 1)' "$f" 2>/dev/null \
        || { say '   %s: JSON 이 아니다 (stdout 오염?)\n' "$f"; return 1; } ;;
    *.csv)
      python3 -c 'import csv,sys
r = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
sys.exit(0 if r and r[0] else 1)' "$f" 2>/dev/null \
        || { say '   %s: CSV 에 행이 없다\n' "$f"; return 1; } ;;
  esac
  return 0
}

# run <라벨> <검사할 산출> <stdout 받을 파일 | -> <로그> <명령...>
#   리다이렉트를 **호출부가 아니라 여기서** 건다. 호출부에서 걸면 say 의
#   stderr 까지 로그로 빨려 들어가 화면에 진행이 안 보인다.
#
# ⚠ 2026-09-11 Codex R3-08: 전 판은 rc 0 + '비어 있지 않은 파일' 만 봤다. profile 이 전부
#   실패해 아무것도 안 쓰면 **이전 실행의 CSV** 가 그 검사를 통과해 "OK" 가 찍히고
#   `write_meta` 가 옛 파일에 새 provenance 를 붙였다.
# ⚠ Codex R4-06 · Q4: 그 다음 판의 시각 도장(`find -newer`)은 옛 파일을 `touch` 만 해도 통과시켰다 —
#   시각은 시도와 계산 bytes 를 잇는 증거가 아니다. 이제 `run` 이 시도마다 run id 를 만들어 명령에
#   `BMS_RUN_ID` 로 주고(verify.py 의 세 명령이 산출물 안에 박는다), 게시된 파일이 **그 id 를 담고
#   있어야** OK 다. 옛 파일은 지우지 않는다 — 보존은 하되 새 결과로 세지 않는다.
run () {
  local label="$1" art="$2" redir="$3" log="$4"; shift 4
  # ⚠ Codex R9 P2-4 → R10 P2-3: sidecar 가 이 시도의 **실제 argv** 를 봉인한다. 전 판의 `"$*"` 는 공백으로 이어 붙인
  #   문자열이라 `['cmd','a b','c']` 와 `['cmd','a','b c']` 가 같은 줄로 기록됐다 (다른 실행인데 같은 증거).
  #   `"$@"` 경계를 JSON array 로 직렬화한다 — 이 한 줄이 production 결속이고 회귀(`test_d10_11`)가 여기를 통과한다.
  LAST_ARGV_JSON="$(python3 -c 'import json,sys; print(json.dumps(sys.argv[1:], ensure_ascii=False))' "$@")"
  say '\n\033[1m== %s\033[0m\n' "$label"
  local t0=$SECONDS rc=0
  local rid; rid="$(python3 -c 'import uuid; print(uuid.uuid4().hex)')"
  LAST_RUN_ID="$rid"                                # write_meta 가 같은 id 를 확인·기록한다
  # R6 내부 F04: 명령 **전** 의 git 상태·시작 시각 — write_meta 가 계산 뒤 상태와 비교한다
  # ⚠ U18-02: `$OUT` 을 같이 넘긴다 — 안 넘기면 CLI 기본값 `out` 만 산출 root 라서 `OUT=out_u18` 의 untracked
  #   디렉터리가 '코드 변경' 이 되고, 끝 상태(write_meta 는 out_dir 을 안다)와 달라져 모든 산출이 '실행 중 변경' 이 된다.
  # ⚠ Codex R14 §7-4: 시작·끝은 **같은 명시 설정**을 공유한다. `$OUT` 은 위에서 이미 확정됐으므로(28 줄)
  #   여기서 `${OUT:-out}` 로 다시 기본값을 만들면 두 자리에 기본값이 생겨 어긋날 수 있다 — 그 어긋남이
  #   U18-02 였다. 확정된 값 하나만 넘긴다 (CLI 쪽도 이제 생략을 오류로 돌려준다).
  LAST_PRE_PV="$(python3 scripts/provenance.py "$art" "$OUT" 2>/dev/null || echo '{}')"
  LAST_STARTED_UTC="$(python3 -c 'import datetime; print(datetime.datetime.now(datetime.timezone.utc).isoformat())')"
  if [ "$redir" = "-" ]; then
    BMS_RUN_ID="$rid" "$@" > "$log" 2>&1 || rc=1
  else
    BMS_RUN_ID="$rid" "$@" > "$redir" 2> "$log" || rc=1
  fi
  local bound=0
  [ -e "$art" ] && check_run_id "$art" "$rid" && bound=1     # R5-08: 필드로 확인 (grep 아님)
  if [ "$rc" -eq 0 ] && [ "$bound" -eq 1 ] && check_artifact "$art"; then
    say '   OK   (%d 초)  → %s  [run_id %s]\n' "$((SECONDS - t0))" "$art" "$rid"
    return 0
  fi
  if [ "$rc" -eq 0 ] && [ "$bound" -eq 0 ]; then
    say '   %s: 이번 시도의 run id 가 산출물의 run_id 필드에 없다 (이전 산출이 남아 있거나 touch 만 됐다) — 새 결과로 세지 않는다\n' "$art"
  fi
  say '   \033[31mFAIL\033[0m (%d 초) — 로그: %s\n' "$((SECONDS - t0))" "$log"
  return 1
}

# ── ne_shape 는 typed status 를 낸다 — wrapper 가 그것을 **읽는다** (Codex R9 P2-5 · R10 P1-2 · P2-7) ──────────
#   0 complete : canonical 에 게시됐다        1 none : γ 짝이 하나도 없다 (부분이 아니라 없음)
#   3 partial/subset : canonical 은 그대로고 산출은 `<write>/partial/` 에 있다 — 승격 대상이 아니다
#   전 판은 이 계약을 코드와 문서에만 적어 두고 **소비하는 production path 가 0 개**였다 (Codex R10 P2-7).
shape_step () {    # shape_step <write-dir> <명령...>
  local write="$1"; shift
  local rc=0 out
  # ⚠ Codex R11 P2-2: 전 판은 namespace 를 `ls | head -1` 로 훑어 옆에 있던 **stale canonical** 의 status 를 읽었고,
  #   rc 3 도 바깥에서 성공으로 세탁됐다. 이제 producer 가 `SHAPE_RESULT {…}` 로 **자기가 쓴 경로·run_id·status** 를
  #   말하고, wrapper 는 rc ↔ status ↔ namespace ↔ run_id 를 대조한다. 못 대조하면 실패다 (모르는 채 넘기지 않는다).
  # ⚠ 자체 리뷰 C15: 네 production 단계 중 여기만 `BMS_RUN_ID` 를 안 주고 묶음 검사(`verify_unit_or_say`)도 안
  #   불렀다 — `read_unit` 이 False 인 섞인 묶음에 `STEP_RC=0 complete` 가 나왔다 (R8-02 가 닫은 "data B / meta A"
  #   축이 거기만 열려 있었다). `run` 과 같이 이번 시도의 id 를 만들어 넘기고, 대조 뒤 묶음 검사를 부른다.
  local rid; rid="$(python3 -c 'import uuid;print(uuid.uuid4().hex)')"
  LAST_RUN_ID="$rid"
  local log; log="$(mktemp "${TMPDIR:-/tmp}/shape_step.XXXXXX")"
  out="$(BMS_RUN_ID="$rid" "$@" 2>&1)" || rc=$?
  printf '%s\n' "$out" >&2
  printf '%s\n' "$out" > "$log"     # ⚠ heredoc 이 stdin 을 쓰므로 producer 출력은 **파일로** 넘긴다
  python3 -I -P - "$rc" "$write" "$log" <<'PYSHAPE'
import json, pathlib, sys
rc, write = int(sys.argv[1]), pathlib.Path(sys.argv[2])
captured = pathlib.Path(sys.argv[3]).read_text(encoding="utf-8", errors="replace")
line = next((l for l in captured.splitlines() if l.startswith("SHAPE_RESULT ")), None)
EXPECT = {0: {"complete"}, 3: {"partial", "subset"}, 1: {"none"}}
if rc not in EXPECT:
    print(f"   ne_shape: 실행 실패 rc {rc}", file=sys.stderr); sys.exit(rc)
if line is None:
    print("   ne_shape: producer 가 SHAPE_RESULT 를 내지 않았다 — 무엇을 읽어야 하는지 모르는 채로 넘기지 않는다 "
          "(Codex R11 P2-2)", file=sys.stderr); sys.exit(1)
r = json.loads(line[len("SHAPE_RESULT "):])
art = pathlib.Path(r["artifact"]) if r.get("artifact") else None
want_ns = write if rc == 0 else write / "partial"
problems = []
if r.get("status") not in EXPECT[rc]:
    problems.append(f"rc {rc} 는 {sorted(EXPECT[rc])} 를 뜻하는데 status 는 {r.get('status')!r}")
if art is None or art.parent.resolve() != want_ns.resolve():
    problems.append(f"산출이 {want_ns} 에 있어야 하는데 {art} 다")
elif not art.is_file():
    problems.append(f"{art} 가 없다")
else:
    m = art.with_name(art.name + ".meta.json")
    meta = json.loads(m.read_text(encoding="utf-8")) if m.is_file() else {}
    if meta.get("status") != r.get("status"):
        problems.append(f"meta status {meta.get('status')!r} ≠ 보고한 {r.get('status')!r}")
    if r.get("run_id") and meta.get("run_id") != r.get("run_id"):
        problems.append(f"meta run_id {meta.get('run_id')!r} ≠ 보고한 {r.get('run_id')!r}")
if problems:
    print("   ne_shape: **모순** — " + " · ".join(problems) + " (Codex R11 P2-2)", file=sys.stderr)
    sys.exit(1)
label = {0: "complete", 3: "부분", 1: "없음"}[rc]
print(f"   ne_shape: **{label}({r['status']})** → {art}"
      + ("" if rc == 0 else "  (canonical 은 건드리지 않았다; 승격 대상 아님)"), file=sys.stderr)
sys.exit(rc)
PYSHAPE
  local prc=$?
  rm -f "$log"
  # ⚠ 자체 리뷰 C15: 대조를 통과했어도 **묶음 검사**는 따로다 (data 와 meta 가 이번 시도의 한 묶음인가).
  #   producer 가 게시한 산출의 경로는 위 python 이 확인했으므로, 그 자리에서 다른 세 단계와 같은 검사를 건다.
  if [ "$prc" -eq 0 ] || [ "$prc" -eq 3 ]; then
    local art
    art="$(printf '%s\n' "$out" | sed -n 's/^SHAPE_RESULT .*"artifact": "\([^"]*\)".*/\1/p' | head -1)"
    if [ -n "$art" ] && ! verify_unit_or_say "$art" "$rid"; then
      say '   ne_shape: 묶음 검사 실패 — data 와 meta 가 이번 시도의 한 묶음이 아니다 (자체 리뷰 C15)\n'
      return 1
    fi
  fi
  return $prc
}

fail=0
# 상태마다 반쪽전지 소스를 고른다. `GITT` 에 그 상태 파일이 없으면
# `step_005C` 로 넘어간다 — 2026-09-10 실측: `300_0147` 이 GITT 에만 없어서
# degeneracy 가 죽었다 (`dd_verify('check')` 의 "상태 파일 4/5" 가 이것이다).
# ⚠ 소스가 섞이면 **행끼리 비교하면 안 된다.** 그래서 무엇을 썼는지 찍는다.
pick_src () {
  local st="$1"
  if [ -n "$FORCE_SRC" ]; then
    case "$FORCE_SRC" in
      GITT)      [ -f "$BMS_DATA_ROOT/data/half_cell/GITT/${st}.xlsx" ] && echo GITT ;;
      step_005C) [ -f "$BMS_DATA_ROOT/data/half_cell/step_005C/${st}_005C.xlsx" ] \
                   && echo step_005C ;;
    esac
    return
  fi
  if [ -f "$BMS_DATA_ROOT/data/half_cell/GITT/${st}.xlsx" ]; then echo GITT
  elif [ -f "$BMS_DATA_ROOT/data/half_cell/step_005C/${st}_005C.xlsx" ]; then echo step_005C
  else echo ""; fi
}

for st in $STATES; do
  SRC="$(pick_src "$st")"
  if [ -z "$SRC" ]; then
    say '\n\033[31m== %s 건너뜀\033[0m — 어느 소스에도 반쪽전지가 없다\n' "$st"
    fail=$((fail+1)); continue
  fi
  USED="$USED $st=$SRC"
  say '\n\033[1m-- %s : 반쪽전지 소스 %s --\033[0m\n' "$st" "$SRC"
  # R6 내부 F01: 전 판은 stdout 을 고정 이름 `.part` 로 받아 shell 이 `flock mv` 했다 — producer 의 stdout fd 가
  #   rename 을 넘어 살아남아, 빠른 다른 시도가 게시·meta·검사를 끝낸 뒤 느린 시도가 게시된 inode 에 잠금 밖에서
  #   썼다 (JSON=B, meta=A, 두 wrapper 는 "통과"). 이제 matrix·profile 과 같이 `--out` 으로 잠금 안 원자적 게시.
  run "degeneracy $st" "$OUT/degeneracy_${st}_${SI}.json" - "$OUT/degeneracy_${st}_${SI}.json.log" \
    env PYTHONUNBUFFERED=1 python3 -m bms_balancing.verify degeneracy \
      --state "$st" --si-source "$SI" --source "$SRC" --w-dqdv 0 \
      --tol 0.01 --starts "$STARTS" --seed 0 --grid 21 --samples 400 \
      --out "$OUT/degeneracy_${st}_${SI}.json" \
      && write_meta "$OUT/degeneracy_${st}_${SI}.json" "$st" "$SRC" \
      && verify_unit_or_say "$OUT/degeneracy_${st}_${SI}.json" "$LAST_RUN_ID" \
      || fail=$((fail+1))

  run "matrix $st" "$OUT/matrix_${st}.csv" - "$OUT/matrix_${st}.csv.log" \
    env PYTHONUNBUFFERED=1 python3 -m bms_balancing.verify matrix \
      --state "$st" --starts "$STARTS" --seed 0 \
      --out "$OUT/matrix_${st}.csv" && write_meta "$OUT/matrix_${st}.csv" "$st" "$SRC" \
      && verify_unit_or_say "$OUT/matrix_${st}.csv" "$LAST_RUN_ID" \
      || fail=$((fail+1))

  run "profile $st" "$OUT/profile_gamma_${st}_${SI}.csv" - \
      "$OUT/profile_gamma_${st}_${SI}.csv.log" \
    env PYTHONUNBUFFERED=1 python3 -m bms_balancing.verify profile \
      --state "$st" --si-source "$SI" --source "$SRC" --w-dqdv 0 \
      --starts "$STARTS" --seed 0 --grid 21 \
      --out "$OUT/profile_gamma_${st}_${SI}.csv" \
      && write_meta "$OUT/profile_gamma_${st}_${SI}.csv" "$st" "$SRC" \
      && verify_unit_or_say "$OUT/profile_gamma_${st}_${SI}.csv" "$LAST_RUN_ID" \
      || fail=$((fail+1))
done

# ⚠ U18-01 (2026-09-13 실측): 전 판은 `--source "${SHAPE_SRC:-${SRC:-GITT}}"` 였다 — `SRC` 는 위 loop 의 **상태별** 변수라
#   마지막 상태의 소스가 새어 들어갔고, STATES 끝이 `300_0147`(step_005C 전용)이면 shape 가 `ne_shape_step_005C_Li.csv`
#   로 게시됐다 (정본은 `ne_shape_GITT_Li.csv`). shape 소스는 loop 와 무관하다: SHAPE_SRC 아니면 GITT (회귀 `test_g27`).
SHAPE_SRC="${SHAPE_SRC:-GITT}"
shape_rc=0
shape_step "$OUT" env PYTHONUNBUFFERED=1 python3 scripts/ne_shape.py \
  --out-dir "$OUT" --write "$OUT" --source "$SHAPE_SRC" --si-source "$SI" \
  > "$OUT/ne_shape.log" 2>&1 || shape_rc=$?
partial=0
case "$shape_rc" in
  0) ;;                                            # complete — 정본 갱신
  3) partial=$((partial+1))                        # ⚠ Codex R11 P2-2: 부분은 성공이 **아니다** (아래 종료 코드에)
     say '   (ne_shape 부분 — 위 로그와 %s/partial/ 을 볼 것; 승격 대상 아님)\n' "$OUT" ;;
  *) fail=$((fail+1)) ;;                           # none·실행 실패·모순은 실패로 센다
esac

say '\n=====================================\n'
if [ "$fail" -eq 0 ] && [ "${partial:-0}" -eq 0 ]; then
  say '전부 통과 — 산출 %d개, 전부 열어서 읽히는 것을 확인했다\n' \
      "$((3 * $(echo $STATES | wc -w)))"
elif [ "$fail" -eq 0 ]; then
  say '**부분** %d 건 — 실패는 없지만 완전하지 않다 (승격 대상 아님). partial/ 을 볼 것\n' "$partial"
else
  say '실패 %d 건 — 위의 .log 를 볼 것\n' "$fail"
fi
say "설정: STATES='%s' STARTS=%s SI=%s SHAPE_SRC=%s\n" "$STATES" "$STARTS" "$SI" "$SHAPE_SRC"
say "반쪽전지 소스:%s\n" "$USED"
say "⚠ 소스가 섞였으면 그 상태끼리는 직접 비교하지 말 것 (축이 다르다)\n"
exit $(( fail > 0 ? 1 : (${partial:-0} > 0 ? 3 : 0) ))   # 부분은 성공으로 세탁하지 않는다 (Codex R11 P2-2)
