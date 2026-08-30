#!/usr/bin/env python3
"""watch_all.py — gabia 전체 작업 한 화면.

관례:  watch -n 30 python3 tools/ionic/watch_all.py

⚠ 왜 bash 가 아니라 python 인가
  - JSON 을 grep 으로 파면 중첩 구조에서 **다른 블록의 첫 매치**를 집어 조용히 틀린 값을 띄운다.
    실제로 겪었다: 프레임 단위 중앙값(0.3175) 대신 mace|sevennet 쌍 중앙값(0.2022)이 표시됐다.
  - bash 안에 python heredoc 을 넣으면 인용 이스케이프가 겹쳐 깨진다(실제로 `cat: webapp: Is a
    directory` 같은 워드 스플리팅 사고가 났다).

⚠ 재부팅 인지 (2026-07-28 추가)
  서버가 껐다 켜지면 tmux 세션이 통째로 사라지고 pgrep 도 전부 '-' 가 된다. 그런데 예전
  버전은 그걸 "아직 진행 중"과 구분하지 못해서, 아무것도 안 도는 상태를 정상처럼 보여줬다.
  이제 부팅 시각과 로그 mtime 을 비교해 **재부팅 전 로그 = 확실히 죽음**을 못 박고,
  살아나야 할 작업의 재기동 명령을 그대로 찍는다.

환경변수
  SDCP_OUT   pw.x 출력 파일 경로(있으면 최우선)
  SDCP_TMUX  pw.x 가 도는 tmux 세션명 (기본: 전 세션을 훑어 pw.x 출력을 가진 페인을 찾는다)
"""
import glob
import io
import json
import os
import pathlib
import re
import subprocess
import sys
from datetime import datetime

H = os.path.expanduser("~")
W = os.path.join(H, "work")
BAR = "-" * 70
NOW = datetime.now()

# ⚠ watch(1) 은 스크롤이 안 된다. 끝난 항목까지 다 찍으면 화면 밖으로 밀려서
#   **정작 봐야 할 진행 중 항목이 안 보인다**. 기본을 compact 로 두고,
#   끝난 것은 한 줄로 접는다. 전체는 --full, 한 섹션만은 --only <키>.
import argparse as _ap
_p = _ap.ArgumentParser(add_help=False)
_p.add_argument("--full", action="store_true", help="끝난 항목까지 전부 펼친다")
_p.add_argument("--only", default="",
                help="disorder|sdcp|committee|elf|bader|prereq 중 하나만")
_p.add_argument("--selftest", action="store_true",
                help="타입 계약·진리값 회귀시험 (화면을 죽인 적 있는 것만)")
ARGS, _ = _p.parse_known_args()
FULL, ONLY = ARGS.full, ARGS.only.lower()


#: gabia 판별 — 호스트명은 바뀔 수 있으니 **그 기계에만 있는 것**으로 본다.
#:   ⚠ 처음엔 `/data/work/runs` 하나만 봤는데 **너무 약했다**: 다른 컨테이너에
#:     같은 이름의 **빈 디렉터리**가 있어서 통과했다 (2026-08-30 실측).
#:     작업 루트 + 설치된 툴체인을 **둘 다** 요구한다.
#:   ⚠ 그리고 **애매하면 '아니다' 로 판정**한다 — 안내를 막는 쪽은 아무것도 안
#:     망가뜨리지만, 틀린 재기동 명령을 뿌리는 쪽은 중복 작업을 만든다.
GABIA_MARKERS = ("/data/work/runs", "/data/apps")


def is_gabia_host(markers=GABIA_MARKERS, exists=os.path.isdir):
    """마커가 **전부** 있어야 gabia 다. 하나라도 없으면 아니다 (fail-closed).

    ⛔ 못 하는 것: 진짜 gabia 인지 증명하지 않는다. '이 대시보드가 볼 것이
      여기 있나' 를 볼 뿐이다. 그게 재기동 안내를 낼 자격의 전부다.
    """
    return all(exists(m) for m in markers)


def _selftest() -> int:
    """`--selftest` — 화면을 죽인 적 있는 것만 친다 (2026-08-30).

    ⚠ 이 시험이 존재하는 이유: 08-30 에 두 번 연달아 같은 병을 맞았다.
      ① `alive()` 가 문자열 `"-"` 를 내는데 `if run:` 이 그걸 참으로 읽어
         **죽은 체인을 이틀 동안 '진행 중'** 으로 찍었다.
      ② 내가 그걸 고치며 `mtime()` 이 float 인 줄 알고 `fromtimestamp` 를 씌워
         **화면 전체가 TypeError 로 죽었다.**
      ②는 내 시험 하네스가 `mtime` 을 `lambda: os.path.getmtime` 으로 **재정의**해서
      못 잡았다 — 실물과 타입이 달랐다. 그래서 이 시험은 **모듈의 진짜 함수**를 쓴다.

    이 시험이 **못 하는 것**: 화면 내용의 정확성. 타입 계약과 진리값만 본다.
    """
    import tempfile
    ok = [0, 0]

    def chk(c, m):
        ok[0] += 1; ok[1] += bool(c)
        print(("  ✔ " if c else "  ✘ ") + m)

    chk(bool(Alive("ALIVE")) and not bool(Alive("-")) and not bool(Alive("?")),
        "alive(): 'ALIVE' 만 참 — \"-\"·\"?\" 는 거짓 (죽은 작업을 진행 중으로 못 읽는다)")
    chk(str(Alive("-")) == "-" and Alive("ALIVE") == "ALIVE",
        "alive(): 표시·비교 용법은 그대로 (호출부를 안 고쳤다)")
    chk(not (Alive("-") or Alive("-")),
        'alive(): "-" or "-" 도 거짓 (두 프로세스 OR 자리)')

    with tempfile.NamedTemporaryFile(suffix=".log") as t:
        m = mtime(t.name)
        chk(isinstance(m, datetime),
            f"mtime(): **datetime 을 낸다** (실측 {type(m).__name__}) — float 로 알고 "
            f"fromtimestamp 를 씌우면 화면이 죽는다")
        chk(isinstance((NOW - m).total_seconds(), float),
            "mtime(): NOW 와 바로 빼진다 (로그 나이 계산 경로)")
    chk(mtime("/nonexistent/zzz") is None, "mtime(): 없는 파일은 None")

    # ⑦ ORCA — **완주와 중단을 가르는 자리.** 여기가 틀리면 죽은 러너를
    #   "진행 중" 으로 보여주거나(gs0 사례), 다 끝난 것을 "죽었다" 로 오탐한다.
    chk(orca_runner_state(8, 1, False) == "dead",
        '⛔음성 ORCA: 1/8 인데 프로세스 없음 → **dead** (gs0 실측 사례)')
    chk(orca_runner_state(8, 1, True) == "running",
        'ORCA: 1/8 이고 프로세스 있음 → running')
    chk(orca_runner_state(8, 8, False) == "done",
        '⛔음성 ORCA: 8/8 이면 프로세스가 없는 게 **정상** — 완주를 죽음으로 오탐 안 함')
    chk(orca_runner_state(8, 0, False) == "dead",
        '⛔음성 ORCA: 0/8 · 프로세스 없음 → dead (한 번도 안 돈 것도 중단이다)')
    # 호스트 판별 — **틀린 기계에 재기동 명령을 뿌리지 않는 것**이 요점이다.
    chk(is_gabia_host(("/a", "/b"), lambda m: True),
        '호스트: 마커가 전부 있으면 gabia')
    chk(not is_gabia_host(("/a", "/b"), lambda m: m == "/a"),
        '⛔음성 호스트: 마커 하나만 있으면 **아니다** — 빈 /data/work/runs 가 있는 '
        '컨테이너가 gabia 로 통과했던 실측 사고')
    chk(not is_gabia_host(("/a",), lambda m: False),
        '⛔음성 호스트: 하나도 없으면 아니다')
    chk(not is_gabia_host((), lambda m: False) is False,
        '마커가 비면 all(()) 은 True — 이 함수는 마커 목록이 비지 않는다고 전제한다')
    print(f"  watch_all selftest {ok[1]}/{ok[0]}")
    return 0 if ok[0] == ok[1] else 1





def want(key):
    return (not ONLY) or ONLY == key


def sh(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True,
                              timeout=15).stdout
    except Exception:
        return ""


class Alive(str):
    """`alive()` 의 반환형 — **찍으면 'ALIVE'/'-' 이고, 조건에 쓰면 옳게 동작한다.**

    🔴 2026-08-30 실측 사고: `alive()` 가 평범한 `str` 을 냈다. 그래서
        run = alive("run_prereq_chain")     # → "-"  (프로세스 없음)
        '🔄 진행 중' if run else '⏹ 안 돌고 있다'
    가 **항상 진행 중**을 골랐다 — 파이썬에서 `"-"` 는 참이다. 이 절은
    구조적으로 "안 돌고 있다" 를 낼 수 없었고, `elif not run` 가지들(완주 판정·
    재기동 안내)은 **죽은 코드**였다. li3nd 선행검사가 08-28 02:20 에 죽었는데
    이틀 동안 화면이 "🔄 진행 중" 으로 보여줬다.

    문자열을 그대로 두고 `__bool__` 만 고친다 — 표시용 호출부(`f"pw.x {alive(...)}"`)와
    비교용 호출부(`alive(...) == "ALIVE"`)를 둘 다 안 건드리면서 조건문만 바로잡는다.
    """

    def __bool__(self):
        return str(self) == "ALIVE"


def orca_runner_state(n_seeds, n_done, runner_alive):
    """ORCA Stage A 러너의 상태 판정 — **패널의 존재 이유가 이 한 줄이다.**

    끝난 seed 가 있어도 **남은 게 있는데 프로세스가 없으면 중단**이다.
    gs0 이 정확히 그랬다: rc 0 정상종료인데 gs1 이 시작을 안 했고, 화면에
    패널이 없어서 하루를 놓쳤다.

    → "dead" · "running" · "done"
    ⛔ 못 하는 것: 왜 죽었는지는 모른다. 남은 수와 프로세스 유무만 본다.
    """
    if n_done >= n_seeds:
        return "done"                      # 완주면 러너가 없는 게 정상이다
    return "running" if runner_alive else "dead"


def alive(pat, exact=False):
    """⚠ shell=True 로 pgrep -f 를 돌리면 **자기 자신을 문다**.
    `sh -c "pgrep -f 'aimd_mlip|...'"` 의 명령줄에 패턴이 그대로 들어 있어서 pgrep 이
    그 셸을 매치한다 → MLIP-MD 가 늘 ALIVE 로 보였다(실측: shell 2 pid / argv 1 pid).
    pgrep 은 자기 pid 만 제외하므로, 셸을 아예 안 끼우는 argv 호출이 정답이다."""
    try:
        r = subprocess.run(["pgrep", "-x" if exact else "-f", pat],
                           capture_output=True, text=True, timeout=15).stdout
    except Exception:
        return Alive("?")          # 못 쟀다 — 참도 거짓도 아니게 두면 안 되므로 거짓
    return Alive("ALIVE" if r.strip() else "-")


def boot_time():
    s = sh("uptime -s").strip()
    for f in ("%Y-%m-%d %H:%M:%S",):
        try:
            return datetime.strptime(s, f)
        except ValueError:
            pass
    return None


BOOT = boot_time()
TMUX = sorted(set(l.split(":")[0] for l in sh("tmux ls").splitlines() if ":" in l))


def mtime(p):
    try:
        return datetime.fromtimestamp(os.path.getmtime(p))
    except OSError:
        return None


# ⚠ 호출은 **Alive·mtime 정의 뒤**라야 한다 — 함수 본문은 지연 평가여도
#   모듈 최상단에서 부르면 아직 없는 이름을 만난다 (두 번 NameError 로 죽었다).
if ARGS.selftest:
    sys.exit(_selftest())


def elf_stage(d):
    """ELF 단계는 **로그 문자열이 아니라 산출 파일**로 판정한다.

    ⚠ run.log 에 `[scf.in] ... -> scf.in (+scf_atomic.in)` 이라는 **입력 생성** 메시지가
      있어서, 'scf_atomic' 문자열 검색은 1단계부터 참이 된다. 실제로 그렇게 오보했다
      (본 scf 중인데 '③ scf_atomic' 으로 표시). 파일은 거짓말하지 않는다.
    """
    import os
    j = lambda f: os.path.join(d, f)
    if os.path.exists(j("lpsocl_rho_atomic.cube")):
        return "⑥ 완료 (rho_atomic 까지)"
    if os.path.exists(j("lpsocl_rho_scf.cube")):
        return "⑤ pp.x rho_atomic 중"
    if os.path.exists(j("lpsocl_elf.cube")):
        return "④ pp.x rho_scf 중"
    if os.path.exists(j("scf_atomic.out")):
        return "③ scf_atomic (본 scf 완료)"
    if os.path.exists(j("scf.out")):
        return "② scf (본 계산)"
    if os.path.isdir(j("pseudo")) and os.listdir(j("pseudo")):
        return "① pseudo 확보"
    return "· 기동 직후"


def find_scalar(o, key, depth=0):
    """json 안을 재귀로 훑어 키에 `want` 가 든 **스칼라**를 찾는다.
    ⚠ 키 이름을 하드코딩하면 파이프라인이 바뀔 때 조용히 0/3 으로 보인다 — 실제로 그랬다."""
    if depth > 6:
        return None
    if isinstance(o, dict):
        for k, v in o.items():
            if key in str(k).lower() and isinstance(v, (int, float)):
                return v
        for v in o.values():
            r = find_scalar(v, key, depth + 1)
            if r is not None:
                return r
    elif isinstance(o, list):
        for v in o[:20]:
            r = find_scalar(v, key, depth + 1)
            if r is not None:
                return r
    return None


# ═══ 작업 등록부 ═════════════════════════════════════════════════════════
# 여기 한 군데만 고치면 생존 판정·재기동 안내가 같이 따라온다 (손으로 두 곳 맞추면 어긋난다).
def _newest(*paths):
    """존재하는 파일 중 가장 최근 것. 없으면 첫 경로(=아직 시작 안 함 표시용)."""
    got = [(os.path.getmtime(q), q) for q in paths if os.path.isfile(q)]
    return max(got)[1] if got else paths[0]


JOBS = [
    {"key": "ELF",    "log": "/data/work/runs/lpsocl_elf/run.log",
     "done": ["/data/work/runs/lpsocl_elf/lpsocl_elf.cube"],
     "proc": ("pw.x", "pp.x"), "tmux": "lpsoclelf",
     "start": "tmux new -s lpsoclelf -d 'bash tools/electronic/run_lpsocl_elf_gabia.sh "
              "> /data/work/runs/lpsocl_elf/run.log 2>&1'"},
    {"key": "Bader",  "log": "/data/work/runs/lpsocl_bader/run.log",
     "done": ["/data/work/runs/lpsocl_bader/lpsocl_bader_summary.json"],
     "proc": ("pw.x", "pp.x"), "tmux": "lpsoclbader",
     "start": "mkdir -p /data/work/runs/lpsocl_bader && tmux new -s lpsoclbader -d "
              "'bash tools/electronic/run_lpsocl_bader_gabia.sh "
              "> /data/work/runs/lpsocl_bader/run.log 2>&1'"},
    # ⚠⚠ **2단계 런이라 로그가 둘이다 (2026-08-03 오탐).** 1단계는 scf_u0.out, 2단계는
    #   relax.out 을 쓴다. relax.out 만 보게 해 뒀더니 1단계가 멀쩡히 도는데 "로그 없음"으로
    #   ⛔ 재기동을 안내했고, 그 명령은 **도는 1단계를 죽이고 밀도 없이 2단계를 시작**한다.
    #   → 존재하는 것 중 **가장 최근** 로그를 본다.
    {"key": "LNOrelax", "log": _newest("/data/work/runs/sdcp_v2/slab_relax/relax.out",
                                       "/data/work/runs/sdcp_v2/slab_relax/scf_u0.out"),
     # SDCP v2 1단계 — 깨끗한 (104) 슬랩 표면 이완 (48원자 1x1, 아래 2층 고정).
     # 이게 끝나야 E_bind 의 기준점이 생긴다. 종결 = BFGS 수렴.
     # ⚠⚠ **순수 `relax` 는 "Final scf calculation" 을 안 찍는다** — vc-relax 전용 문자열이다.
     #   그것만 보게 해 뒀더니 2026-08-06 에 **JOB DONE(2d6h) 로 정상 종료한 런**이
     #   ⓪ 생존판정과 맨 아래 집계에서 ⛔ 로 잡혔고, 그 재기동 명령은 scf_u0 부터 다시 돌며
     #   **relax.out 을 덮어쓴다**. 53시간이 날아갈 뻔했다. → 표식을 여러 개 받는다.
     "done_marker": (("End of BFGS Geometry Optimization", "bfgs converged in",
                      "Final scf calculation at the relaxed structure"),
                     "표면 이완 완료 — --harvest 로 1x4 복제"),
     "done": [], "proc": ("pw.x",), "tmux": "lnorelax",
     "start": "tmux new -s lnorelax -d 'H=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/"
              "hpcx/hpcx-2.20/ompi; export PATH=$H/bin:$PATH OPAL_PREFIX=$H OMP_NUM_THREADS=1 "
              "CUDA_VISIBLE_DEVICES=0 OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1 "
              "LD_LIBRARY_PATH=$H/lib:/data/apps/nvhpc/Linux_x86_64/24.11/compilers/lib:"
              "/usr/local/cuda-12.6/lib64; cd /data/work/runs/sdcp_v2/slab_relax && "
              "$H/bin/mpirun -np 1 --oversubscribe /data/apps/qe-7.4.1-gpu/bin/pw.x -nk 1 "
              "-in scf_u0.in > scf_u0.out 2>&1 && "
              "$H/bin/mpirun -np 1 --oversubscribe /data/apps/qe-7.4.1-gpu/bin/pw.x -nk 1 "
              "-in relax.in > relax.out 2>&1'"},
    # SDCP v2 2단계 — 이완된 슬랩 위 자세 스캔(UMA). Phase-B DFT+U 로 넘길 상위 자세를 고른다.
    {"key": "phaseA", "log": os.path.join(H, "logs", "phaseA.log"),
     "done": ["/data/work/runs/sdcp_v2/phaseA/phaseA_v7c_results.csv"],
     "proc": (), "tmux": "phaseA",
     "start": "tmux new -s phaseA -d 'python3 tools/sdcp/phaseA_v7c_orient_scan.py "
              "--slab db/structures/linio2_104_sym_1x4L4_relaxed.vasp "
              "--moldir /data/work/runs/sdcp_linio2_binding/inputs/sdcp_v7c "
              "--out /data/work/runs/sdcp_v2/phaseA 2>&1 | tee -a ~/logs/phaseA.log'"},
]


def verdict(j):
    """→ (한 줄 상태, 재기동 필요?)"""
    done = bool(j["done"]) and all(os.path.exists(p) for p in j["done"])
    lm = mtime(j["log"])
    # ⚠ 산출 **파일**이 아니라 로그의 한 줄이 종결인 작업도 있다 (chain2: GPU 해방을
    #   기다렸다가 알리고 끝). done 을 파일로만 판정하면 완주한 런이 ⛔ 죽음이 된다(실측).
    dm = j.get("done_marker")
    if dm and lm and not done:
        marks = dm[0] if isinstance(dm[0], (tuple, list)) else (dm[0],)
        try:
            txt_ = open(j["log"], errors="ignore").read()
            if any(m in txt_ for m in marks):
                return f"✅ 완료 — {dm[1]}", False
        except OSError:
            pass
    running = any(alive(p, exact=True) == "ALIVE" for p in j["proc"]) or j["tmux"] in TMUX
    if done:
        return "✅ 완료", False
    if not lm:
        return "· 미가동 (로그 없음)", bool(j["start"])
    age = (NOW - lm).total_seconds() / 60
    stale_boot = BOOT is not None and lm < BOOT
    if running:
        return f"▶ 진행 중 (로그 {age:.0f}분 전 갱신)", False
    if stale_boot:
        return (f"⛔ **재부팅으로 죽음** — 로그 마지막 기록 {lm:%m-%d %H:%M} "
                f"< 부팅 {BOOT:%m-%d %H:%M}"), bool(j["start"])
    return f"⛔ 멈춤 — 프로세스·tmux 없음, 로그 {age:.0f}분 전이 마지막", bool(j["start"])


# ═══ compact 렌더러 ══════════════════════════════════════════════════════
# ⚠ watch(1) 은 스크롤이 안 된다. 끝난 섹션까지 전부 찍으면 **정작 봐야 할 진행 중
#   항목이 화면 밖으로 밀린다** (실측 2026-07-30: 완료 3섹션 + 완료 하위줄이 화면의
#   절반을 먹고, 정작 재기동이 필요한 SDCP 는 중간에 파묻혔다).
#   그래서 출력을 버퍼에 모았다가 **조치(⛔)·진행(▶) 이 없는 섹션은 접는다.**
#   --full 이면 전부 편다.
_CAP = io.StringIO()
_REAL_STDOUT = sys.stdout
if not FULL:
    sys.stdout = _CAP


_LIVE = "\x00LIVE"


def live():
    if FULL:
        return
    """이 섹션은 **지금 볼 것**이다 — compact 에서도 접지 않는다.

    ⚠ 이모지(▶/⛔)만 보고 접으면 틀린다. 실측: disorder 의 진행 중 cfg 는
      `600K✓ 800K· 1000K· [1/3]` 이라 ▶ 가 없고, chain 은 '세션 살아있음' 이라
      역시 없다 — 둘 다 조용히 접혔다. 그래서 **섹션이 스스로 선언**하게 한다.
    """
    print(_LIVE)


def render(captured: str) -> str:
    """섹션 단위로 접기. 반환값이 실제 화면."""
    parts = captured.split(BAR + "\n")
    head, secs = parts[0], parts[1:]
    keep, done, idle, n_act = [head.rstrip()], [], [], 0
    sub = {}          # 섹션 → 그 섹션에서 접힌 ✅ 항목들
    for sec in secs:
        body = sec.rstrip("\n")
        if not body.strip():
            continue
        # ⛔ 2026-08-28 — `--only <키>` 를 줬는데 그 섹션이 접혀서 화면이 비었다.
        #   그 인자는 **그 섹션을 보려고** 주는 것이다. 접지 않는다.
        is_live = (_LIVE in body) or ("⛔" in body) or bool(ONLY)
        n_act += body.count("⛔")
        body = "\n".join(l for l in body.splitlines() if _LIVE not in l)
        title = body.splitlines()[0].strip() if body.strip() else ""
        if not is_live:
            # 접히는 섹션 — 제목만 굴린다. 제목의 '— …' 뒤 부연은 버린다.
            # ⚠ **"완료" 와 "자료 없음" 을 같은 줄에 묶으면 안 된다.** 아직 시작도 안 한
            #   섹션이 ✅ 로 굴러가면 다 끝난 것처럼 보인다(로컬 테스트에서 실제로 그랬다).
            (done if "✅" in body else idle).append(
                title.split(" — ")[0].split("(")[0].strip())
            continue
        # 살아 있는 섹션 안에서도 **완료된 하위 줄**은 접는다
        lines = []
        for l in body.splitlines():
            if "✅" in l and "⛔" not in l and "▶" not in l:
                # ⚠ 섹션 제목을 안 붙이면 굴러간 조각이 정체불명이 된다
                #   (실측: "완료 — cube 3개" 만 남아 어느 작업인지 알 수 없었다).
                t = " ".join(l.replace("✅", " ").split())     # 공백 정규화
                t = t.split("(")[0].strip(" :·—")
                if t:
                    # ⚠ 항목마다 섹션 제목을 붙이면 "① …: 3/3 완료 · ① …: 3/3 완료" 처럼
                    #   같은 제목이 반복돼 줄이 길어지고 뒤가 잘린다(실측). 섹션별로 묶는다.
                    _sh = title.split(" (")[0].split(" — ")[0].strip()
                    sub.setdefault(_sh, []).append(t)
                continue
            lines.append(l)
        # 하위줄이 전부 접힌 그룹 머리(`  [comp2_disorder_relaxed]`)는 같이 지운다
        pruned = []
        for k, l in enumerate(lines):
            if re.match(r"^\s*\[.*\]\s*$", l):
                nxt = next((x for x in lines[k + 1:] if x.strip()), "")
                if not nxt or re.match(r"^\s*\[.*\]\s*$", nxt):
                    continue
            pruned.append(l)
        keep.append("\n".join(pruned).rstrip())
    out = [("\n" + BAR + "\n").join(keep)]
    # ⚠ 끝난 것·자료 없는 것은 **화면에 안 띄운다** (2026-08-03 요청).
    #   watch(1) 은 스크롤이 안 되므로 지금 볼 것만 남기는 게 목적이다.
    #   전체가 필요하면 --full. 다만 **몇 개가 접혔는지는** 한 줄로 남긴다 —
    #   "아무것도 없음"과 "다 끝남"이 화면에서 같아 보이면 안 되기 때문.
    n_fold = len(dict.fromkeys(done)) + len(dict.fromkeys(idle)) + len(sub)
    if n_fold:
        out.append(BAR)
        out.append(f"({n_fold}건 접힘 — 완료·미가동. --full 로 펼침)")
    return "\n".join(out)


# ═══ 이 화면이 **어느 기계**를 보고 있나 ══════════════════════════════════
#: 🔴 2026-08-30 실측 사고 — 헤더가 `gabia 전체 상황` 을 **박아서** 찍었다.
#:   데스크탑 WSL(DESKTOP-IK8J81H)에서 돌렸더니 화면이 "gabia" 라고 우기면서
#:   전 작업을 `미가동` 으로 찍었고(그 경로가 이 기계에 없을 뿐인데),
#:   맨 아래 `⛔ 재기동 필요` 가 ELF·Bader·LNOrelax 를 **데스크탑에서 시작하라**고
#:   시켰다. 실행했으면 실패하거나 중복 작업이 떴다.
#:   ⇒ 화면은 자기가 어디 있는지 알아야 한다. 모르면 **판정을 하지 않는다**.
HOSTNAME = (sh("hostname").strip() or "?")
IS_GABIA = is_gabia_host()


def host_banner():
    """→ (제목, 경고줄 or None). 경고가 있으면 재기동 안내를 **막는다**."""
    if IS_GABIA:
        return "gabia 전체 상황", None
    return ("⚠ 이 기계는 gabia 가 아니다 — %s" % HOSTNAME,
            "  ⛔ gabia 마커(%s)가 없다. 아래 `미가동` 은 **작업이 죽은 것이 아니라 "
            % ", ".join(m for m in GABIA_MARKERS if not os.path.isdir(m)) +
            "이 기계에 그 경로가 없다는 뜻**이다.\n"
            "     재기동 안내는 **막았다** — 여기서 실행하면 실패하거나 중복 작업이 뜬다.\n"
            "     gabia 에서 보려면: ssh root@121.78.116.27 · cd /data/work/repo")


# ═══ 헤더 ════════════════════════════════════════════════════════════════
up = sh("uptime -p").strip() or "?"
gpu = sh("nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total "
         "--format=csv,noheader,nounits").strip() or "(조회 실패)"
_TITLE, _WRONGHOST = host_banner()
if FULL:
    print("=" * 70)
    print(f"{_TITLE}  {NOW:%m-%d %H:%M}")
    print("=" * 70)
    if _WRONGHOST:
        print(_WRONGHOST)
    print(f"부팅: {BOOT:%m-%d %H:%M} ({up})" if BOOT else f"부팅 시각 조회 실패 ({up})")
    print(f"tmux 세션: {' '.join(TMUX) if TMUX else '(없음)'}")
    print(f"GPU: {gpu}   [util%, used MiB, total MiB]")
else:
    # 한 줄로 — 14주 uptime 같은 건 매 30초 볼 정보가 아니다.
    print(f"{HOSTNAME if not IS_GABIA else 'gabia'} {NOW:%m-%d %H:%M} · {up} · "
          f"tmux {' '.join(TMUX) if TMUX else '없음'} · GPU {gpu}")
    if _WRONGHOST:
        print("  ⛔ gabia 가 아니다 — 아래 판정은 이 기계 기준이다 (--full 로 사유)")
if BOOT and (NOW - BOOT).total_seconds() < 3600:
    print("  ⚠ 1시간 안에 부팅됨 — tmux 세션은 재부팅으로 전부 사라진다. 생존판정 확인.")
print(f"  pw.x {alive('pw.x', exact=True)}  ·  pp.x {alive('pp.x', exact=True)}  ·  "
      f"MLIP-MD {alive('aimd_mlip|disorder_ensemble_diffusion')}")
print(BAR)

# ═══ ⓪ 생존 판정 ═════════════════════════════════════════════════════════
print("⓪ 생존 판정")
restart = []
for j in JOBS:
    msg, need = verdict(j)
    if "완료" not in msg:
        live()
    print(f"  {j['key']:8s} {msg}")
    if need and j["start"]:
        restart.append(j)
print(BAR)

# ═══ ① comp2 disorder ════════════════════════════════════════════════════
if want("disorder"):
  print("① comp2 DISORDER ensemble")
  roots = sorted(glob.glob(os.path.join(W, "runs", "comp2_disorder*")))
  if not roots:
    print("  (comp2_disorder* 없음)")
  # ⚠⚠ **comp2_disorder(v1)는 폐기본이다.** 라벨 스왑을 이완 없이 해서 sigma_300K ~70 mS/cm
  #   아티팩트가 났고(2026-07-27), anneal+relax 하는 comp2_disorder_relaxed 로 대체됐다
  #   (run_comp2_disorder.sh 머리말). 그런데 watch 가 v1 의 미완 cfg 를 그대로 띄우는 바람에
  #   **하지 않아도 될 일이 할 일 목록에 남아** MLIP-MD 를 괜히 재기동할 뻔했다(2026-07-31).
  #   후속본이 있으면 v1 은 접는다.
  _sup = os.path.join(W, "runs", "comp2_disorder_relaxed")
  _has_v2 = os.path.isdir(_sup)
  for r in roots:
    _is_v1 = os.path.basename(r) == "comp2_disorder"
    if _is_v1 and _has_v2 and not FULL:
      print("  [comp2_disorder] ⊘ 폐기본(v1, 미이완 라벨스왑 → σ 아티팩트) — "
            "comp2_disorder_relaxed 가 대체. 미완 cfg 는 **할 일이 아니다**.")
      continue
    print(f"  [{os.path.basename(r)}]"
          + ("   ⊘ 폐기본 — 인용 금지" if _is_v1 and _has_v2 else ""))
    cfgs = sorted(glob.glob(os.path.join(r, "d*_cfg*")))
    if not cfgs:
        print("    (cfg 없음)")
    unknown_keys = None
    done_cfgs = []
    for c in cfgs:
        line, n = f"    {os.path.basename(c)} :", 0
        for T in (600, 800, 1000):
            hit, kind = None, ""
            for f in sorted(glob.glob(os.path.join(c, f"T{T}", "*.json"))):
                try:
                    d = json.load(open(f))
                except Exception:
                    continue
                # 실제 키가 `D_Li_cm2_s` 였다 — 'd_cm2' 로는 안 잡힌다. 부분 문자열을 넓게.
                # ⚠ 반복변수 이름을 want 로 두면 모듈 수준 want() 를 덮어써서
                #   뒤 섹션이 TypeError 로 죽는다 (실제로 겪음).
                for wkey, tag in (("sigma", "σ"), ("cond", "σ"),
                                  ("cm2", "D"), ("diffus", "D"), ("d_li", "D")):
                    hit = find_scalar(d, wkey)
                    if hit is not None:
                        kind = tag
                        break
                if hit is not None:
                    break
                if unknown_keys is None and isinstance(d, dict):
                    unknown_keys = (os.path.basename(f), list(d)[:8])
            if hit is not None:
                line += f" {T}K✓({kind}{hit:.2e})"
                n += 1
            else:
                run = glob.glob(os.path.join(c, f"T{T}", "traj*"))
                line += f" {T}K{'~' if run else '·'}"
        if n == 3 and not FULL:
            done_cfgs.append(os.path.basename(c))     # 완료는 접는다
        else:
            live()
            print(f"{line}  [{n}/3]")
    if done_cfgs:
        print(f"    ✅ 3/3 완료: {', '.join(done_cfgs)}   (--full 로 값 펼침)")
    if unknown_keys:
        # 자기 진단: 값을 못 찾았으면 **어떤 키가 있었는지** 알려준다
        print(f"    ⚠ 값 미검출 — {unknown_keys[0]} 최상위 키: {unknown_keys[1]}")
  if FULL:
      print("  ordered baseline: comp2 Ea 0.276±0.033 / comp1 0.253  (disorder가 낮추면 가설 확증)")
  print(BAR)

# ═══ ② SDCP v2 — 슬랩 표면 이완 ═══════════════════════════════════════════
# 2026-08-03: 옛 경로(phaseB_v7c_slabfirst)는 **깨진 슬랩** 위에서 돌았다 —
#   Li24Ni24O48 산화물인데 2.5 A 미만 원자쌍이 0개(Ni-O 3.667 A, 원자가 1/3). 전부 폐기하고
#   새 슬랩(db/structures/linio2_104_sym_1x4L4, 반전대칭 192/192, 게이트 통과)으로 다시 세웠다.
#   여기서는 **지금 도는 v2 만** 자세히 본다. 옛 경로는 한 줄로만 남긴다.
def _sdcp_maxcomp(out_path, in_path):
    """이온스텝별 **자유 원자의 max|힘 성분|** 궤적. QE BFGS 가 forc_conv_thr 에 거는 양.

    ⚠ 화면에 찍던 `Total force` 는 **자유 원자 전체의 노름**(√Σ|F|²)이라 원자 수가 많으면
      실제 판정량보다 몇 배 크게 나온다 — 그걸 1e-3 문턱과 나란히 찍는 바람에
      "아직 10배 남았다" 로 읽혔다(2026-08-05 실측: 노름 0.0102 vs 실제 판정량 0.0032).
      per-atom 출력에는 **고정 원자(if_pos 0 0 0)** 의 raw 힘도 같이 찍히므로
      relax.in 의 플래그로 걸러야 한다 (안 걸르면 0.049 짜리 고정 O 가 잡힌다).
    """
    free = {}
    try:
        on = False
        n = 0
        for line in open(in_path, errors="ignore"):
            f = line.split()
            if line.lstrip().startswith("ATOMIC_POSITIONS"):
                on, n = True, 0
                continue
            if on:
                if len(f) < 4:
                    break
                n += 1
                free[n] = not (len(f) >= 7 and f[4] == "0" and f[5] == "0" and f[6] == "0")
    except OSError:
        return []
    if not free:
        return []
    out, cur, on = [], 0.0, False
    try:
        for line in open(out_path, errors="ignore"):
            if "Forces acting on atoms" in line:
                on, cur = True, 0.0
                continue
            if on and "Total force" in line:
                out.append(cur)
                on = False
                continue
            # iverbosity 를 올리면 본 블록과 Total force 사이에 기여도 분해
            # (The non-local contrib. / The ionic contribution / The Hubbard contrib. …)가
            # 끼는데, 그것도 같은 `atom N type M force =` 형식이라 그대로 두면 물어 버린다.
            if on and line.lstrip().startswith("The "):
                on = False
                out.append(cur)
                continue
            f = line.split()
            if on and len(f) >= 9 and f[0] == "atom" and free.get(int(f[1]), False):
                for v in f[6:9]:
                    try: cur = max(cur, abs(float(v)))
                    except ValueError: pass
    except OSError:
        return []
    return out

def _sdcp_nabove(out_path, in_path, thr=1e-3):
    """이온스텝별 (문턱 위 자유원자 수, 파싱된 자유원자 수).

    ⚠⚠ **max|F| 하나로 진행을 판정하면 안 된다** (2026-08-06 실측).
      자유 원자가 24개면 어느 하나는 늘 튀어 있어서 max 가 톱니를 그리고, 그걸
      '평탄역/정체' 로 오독한다. 정작 개별 원자는 0.042 -> 0.001 로 38배 내려가 있었다.
      **문턱 위 개수**는 그 착시가 없다.
    ⚠ 계산이 도는 중이면 마지막 힘 블록이 잘린다 — 그러면 개수가 가짜로 뚝 떨어지므로
      파싱된 자유원자 수를 같이 돌려주고 부족한 스텝은 호출부에서 버린다.
    """
    free, on, n = {}, False, 0
    try:
        for line in open(in_path, errors="ignore"):
            if line.lstrip().startswith("ATOMIC_POSITIONS"):
                on, n = True, 0
                continue
            if on:
                f = line.split()
                if len(f) < 4:
                    break
                n += 1
                free[n] = not (len(f) >= 7 and f[4] == "0" and f[5] == "0" and f[6] == "0")
    except OSError:
        return []
    nfree = sum(1 for v in free.values() if v)
    if not nfree:
        return []
    out, cur, on = [], {}, False
    try:
        for line in open(out_path, errors="ignore"):
            if "Forces acting on atoms" in line:
                on, cur = True, {}
                continue
            if on and ("Total force" in line or line.lstrip().startswith("The ")):
                if cur:
                    out.append((sum(1 for v in cur.values() if v >= thr), len(cur)))
                on, cur = False, {}
                continue
            f = line.split()
            if on and len(f) >= 9 and f[0] == "atom" and free.get(int(f[1]), False):
                try:
                    cur[int(f[1])] = max(abs(float(v)) for v in f[6:9])
                except ValueError:
                    pass
    except OSError:
        return []
    return [(a, b, nfree) for a, b in out]


_V2 = "/data/work/runs/sdcp_v2"
# ⚠ U-ramp 2단계다 — 1단계 scf_u0.out(U=0, 밀도 만들기) → 2단계 relax.out(U=6.2, 이완).
#   어느 쪽을 보고 있는지 화면에 찍지 않으면 "이온스텝 0/80" 을 정체로 오해한다.
_S1 = os.path.join(_V2, "slab_relax", "scf_u0.out")
_S2 = os.path.join(_V2, "slab_relax", "relax.out")
_RLX = _S2 if os.path.isfile(_S2) else _S1
_STAGE = "2단계 U=6.2 relax" if os.path.isfile(_S2) else "1단계 U=0 scf (밀도 만들기)"
if want("sdcp"):
    print("② SDCP v2 — LiNiO2(104) 표면 이완  (E_bind 기준점)")
    if not os.path.isfile(_RLX):
        print("   · 아직 시작 안 함")
    else:
        txt = open(_RLX, errors="ignore").read()
        ls = txt.splitlines()
        gpu = subprocess.run(["pgrep", "-f", r"qe-.*-gpu/bin/pw\.x"],
                             capture_output=True, text=True).stdout.strip()
        alive_j = ("lnorelax" in TMUX) and bool(gpu)
        age = (NOW - datetime.fromtimestamp(os.path.getmtime(_RLX))).total_seconds()

        # ── BFGS 이온 스텝 궤적 ──────────────────────────────────────────
        etot = [float(m) for m in re.findall(r"^!\s+total energy\s+=\s+(-?[\d.]+)", txt, re.M)]
        forc = [float(m) for m in re.findall(r"Total force =\s+([\d.]+)", txt)]
        scfn = re.findall(r"convergence has been achieved in\s+(\d+) iterations", txt)
        # ⚠⚠ **순수 `relax` 는 "Final scf calculation" 을 안 찍는다** — 그건 vc-relax 전용이다.
        #   relax 의 완료 표식은 `bfgs converged` + `End of BFGS Geometry Optimization` + `JOB DONE.`
        #   이걸 몰라서 2026-08-06 에 **정상 종료(JOB DONE, 2d6h)한 계산을 '죽었다'** 로 찍고
        #   relax.out 을 덮어쓰는 재기동 명령을 권했다. 하마터면 53시간을 날릴 뻔했다.
        done = any(k in txt for k in ("Final scf calculation at the relaxed structure",
                                      "End of BFGS Geometry Optimization",
                                      "bfgs converged in"))
        job_done = "JOB DONE." in txt
        cpu  = re.findall(r"total cpu time spent up to now is\s+([\d.]+) secs", txt)
        RY_EV = 13.605693
        NSTEP = 80          # relax.in 의 nstep — 표시/예산 경고가 같은 값을 본다
        _need = 0           # 힘 문턱까지 필요한 이온스텝 (0=미산출, None=평탄역이라 예보 불가)

        print(f"   단계  {_STAGE}"
              + ("   (1단계엔 이온스텝이 없다 — 정상)" if "1단계" in _STAGE else ""))
        print(f"   상태  {'▶ 진행 중' if alive_j else ('✅ 완료' if done else '⛔ 프로세스 없음')}"
              f" · 로그 {age/60:.0f}분 전"
              + (f" · 이온스텝 {len(etot)}/{NSTEP}" if "2단계" in _STAGE else ""))
        if etot:
            # ⚠ 수렴 판정선을 **같이** 찍는다. 숫자만 보면 다 온 건지 알 수 없다.
            print(f"   에너지  현재 {etot[-1]:.6f} Ry"
                  + (f"  ·  직전 스텝 대비 {(etot[-1]-etot[-2])*RY_EV*1000:+.1f} meV"
                     f"  (목표 |ΔE| < {1e-4*RY_EV*1000:.1f} meV)" if len(etot) > 1 else ""))
        if forc:
            # ⚠ 판정량은 **자유 원자 max|성분|** 이다 (Total force = 노름, 문턱과 다른 양)
            mc = _sdcp_maxcomp(_RLX, os.path.join(_V2, "slab_relax", "relax.in"))
            if mc:
                print(f"   힘      max|성분| {mc[-1]:.5f} Ry/bohr  (판정량, 목표 < 1.0e-3)"
                      f"  {'✓ 도달' if mc[-1] < 1e-3 else '진행 중'}")
                print("           궤적 " + " → ".join(f"{f:.5f}" for f in mc[-6:]))
                if len(mc) >= 6 and mc[-1] >= 1e-3:
                    # 최근 구간 기하평균 감소율로 남은 스텝 추정 (톱니가 있어 6점 이상만)
                    import math
                    a, b = mc[-6], mc[-1]
                    r = (b / a) ** (1 / 5) if a > 0 and b > 0 else 1.0
                    # ⚠⚠ **톱니를 감쇠로 오독하지 않는다.** 창 안의 진폭(max/min)이 창 양끝의
                    #   감소폭보다 크면 그건 '내려가는 중' 이 아니라 **평탄역에서 흔들리는 것**이다.
                    #   기하평균 r 을 그대로 외삽하면 있지도 않은 수렴 시각을 만들어 낸다
                    #   (SDCP 에서 6점으로 6일을 예보했다가 철회한 것과 같은 함정).
                    win = mc[-6:]
                    amp = (max(win) - min(win)) / max(min(win), 1e-12)
                    drop = (a - b) / max(a, 1e-12)
                    plateau = amp > max(drop, 0.0) * 1.5
                    if plateau:
                        print(f"           ⛔ **평탄역** — 최근 6스텝이 {min(win):.5f}–{max(win):.5f} 에서"
                              f" 진동(진폭 {amp*100:.0f}%) 하고 순감소는 {drop*100:+.0f}% 뿐이다.")
                        print("              이 구간에서 감쇠율을 외삽하면 안 된다 — **수렴 시각을 예보할 수 없다**.")
                        _need = None
                    elif 0 < r < 0.999:
                        _need = math.log(b / 1e-3) / -math.log(r)
                        print(f"           감소율 {r:.3f}/스텝 → 1e-3 까지 약 {_need:.0f}스텝")
            print(f"           참고: Total force {forc[-1]:.6f} (자유원자 전체 노름 — 문턱 대상 아님)")
            # ★ max 하나보다 이게 진행을 정직하게 보여준다 (위 _sdcp_nabove 주석 참조)
            na = _sdcp_nabove(_RLX, os.path.join(_V2, "slab_relax", "relax.in"))
            na_full = [(x, tot) for x, seen, tot in na if seen >= tot]
            if len(na_full) >= 6:
                seq = [x for x, _ in na_full]
                tot = na_full[0][1]
                print(f"   문턱위  {' '.join(str(v) for v in seq[-14:])}  (자유 {tot}개 중)")
                h = len(seq) // 2
                e0, e1 = sum(seq[:h]) / h, sum(seq[h:]) / (len(seq) - h)
                verdict = ("✅ 줄고 있다 — 수렴 중" if e1 < e0 * 0.85 else
                           ("⛔ 늘고 있다 — 발산 의심" if e1 > e0 * 1.15 else
                            "⚠ 평평하다 — 여기서부터가 진짜 정체"))
                print(f"           전반 {e0:.1f} → 후반 {e1:.1f}  {verdict}")
                if len(na) > len(na_full):
                    print(f"           (쓰다 만 블록 {len(na)-len(na_full)}개 제외)")
        if scfn:
            mx = [int(x) for x in scfn]
            print(f"   SCF     스텝당 반복수 {mx[-6:]}  (300 이면 가짜 수렴 의심)")
        # ── 현재 스텝 안쪽 ──────────────────────────────────────────────
        it = [l.strip() for l in ls if "iteration #" in l][-1:]
        ac = [l.strip() for l in ls if "estimated scf accuracy" in l][-1:]
        if it or ac:
            print("   지금    " + " · ".join(x for x in (it + ac)))
        # ── 자성 건전성: AFM 이 유지되나 ────────────────────────────────
        tm = re.findall(r"total magnetization\s+=\s+(-?[\d.]+)", txt)
        am = re.findall(r"absolute magnetization\s+=\s+([\d.]+)", txt)
        if tm and am:
            ok_afm = abs(float(tm[-1])) < 0.5
            print(f"   자성    total {float(tm[-1]):+.2f} / absolute {float(am[-1]):.2f} muB"
                  f"  {'✓ AFM 유지' if ok_afm else '⛔ FM 으로 붕괴 — 시드 재설정 필요'}")
        # ── 남은 시간 어림 ─────────────────────────────────────────────
        if cpu and len(etot) >= 2:
            per = float(cpu[-1]) / max(len(etot), 1)
            # ⚠⚠ 예전엔 '20스텝 가정' 이 **하드코딩**이라, 22스텝째에 max(0,20-22)=0 →
            #   힘 추세가 "87스텝 더" 라고 찍은 바로 아래에서 "남은 0.0h" 가 나왔다(2026-08-06).
            #   기준은 **힘 문턱까지 필요한 스텝**이고, 없으면 예보하지 않는다.
            line = f"   속도    스텝당 {per/60:.0f}분 · 경과 {float(cpu[-1])/3600:.1f}h"
            if _need:
                left_h = _need * per / 3600
                line += f" · 힘 기준 남은 {_need:.0f}스텝 ≈ **{left_h:.0f}h ({left_h/24:.1f}일)**"
            elif _need is None and etot:
                line += " · 남은 시간 **예보 불가**(위 평탄역 판정)"
            print(line)
            # 자기 nstep 예산 안에 못 들어가는 것은 별도로 경고한다 — 조용히 중단되면
            # '수렴했다' 와 구별이 안 된다.
            budget = NSTEP - len(etot)
            if _need and _need > budget:
                print(f"   ⛔ **예산 초과** — nstep {NSTEP} 중 {budget}스텝 남았는데 힘 기준으로 "
                      f"{_need:.0f}스텝이 필요하다. 이대로면 **수렴 전에 멈춘다.**")
                print("      선택지: (a) nstep 상향 후 restart_mode='restart' (b) 힘 문턱 완화 "
                      "(c) 믹싱/구속 재설계. 지금 상태로 더 기다리는 것은 답이 아니다.")
        # ── 다음 단계 ──────────────────────────────────────────────────
        if done:
            print("   ✅ **이완 완료** — bfgs converged / End of BFGS"
                  + ("  ·  JOB DONE" if job_done else "  ⚠ JOB DONE 없음(마무리 중이거나 중단)"))
            print("   ⛔ **재기동하지 말 것** — relax.out 을 덮어쓰면 결과가 사라진다.")
            # ⚠ '다음' 은 **단계를 알아야** 한다. harvest 가 이미 끝났는데도 harvest 를 권하면
            #   화면이 진행을 못 따라가고, 사용자가 끝난 일을 다시 한다(2026-08-06 실측).
            _HV = "db/structures/linio2_104_sym_1x4L4_relaxed.vasp"
            if not os.path.isfile(os.path.join(REPO, _HV) if "REPO" in dir() else _HV):
                print("   다음: 이완좌표를 1x4 로 복제한다")
                print(f"      python3 tools/sdcp/make_slab_relax.py --harvest {_V2}/slab_relax")
        elif not alive_j:
            print("   ⛔ 죽었다(완료 표식 없음). ⚠ **아래를 그대로 붙이기 전에 두 가지를 먼저 한다**:")
            print(f"      1) cp {_V2}/slab_relax/relax.out{{,.bak}}   ← `> relax.out` 이 덮어쓴다")
            print("      2) 이온스텝이 이미 쌓였으면 relax.in 에 마지막 ATOMIC_POSITIONS 를")
            print("         스플라이스하고 restart_mode='restart' 로 — 처음부터 다시 돌리지 않는다")
            print("      env 는 tmux 따옴표 **안쪽**에:")
            print("      tmux new -s lnorelax -d 'H=/data/apps/nvhpc/Linux_x86_64/24.11/"
                  "comm_libs/12.6/hpcx/hpcx-2.20/ompi; export PATH=$H/bin:$PATH OPAL_PREFIX=$H \\")
            print("        OMP_NUM_THREADS=1 CUDA_VISIBLE_DEVICES=0 OMPI_ALLOW_RUN_AS_ROOT=1 \\")
            print("        OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1 LD_LIBRARY_PATH=$H/lib:/data/apps/"
                  "nvhpc/Linux_x86_64/24.11/compilers/lib:/usr/local/cuda-12.6/lib64; \\")
            print(f"        cd {_V2}/slab_relax && $H/bin/mpirun -np 1 --oversubscribe \\")
            print("        /data/apps/qe-7.4.1-gpu/bin/pw.x -nk 1 -in relax.in > relax.out 2>&1'")
        if alive_j:
            live()
    # ── Phase-A 자세 스캔 (이완 슬랩이 나온 뒤의 다음 단계) ───────────────
    # ⚠ 결과 CSV 는 **끝에 한 번** 쓰이므로 진행은 로그로 센다(도구가 flush=True 로 찍는다).
    _PA = "/data/work/runs/sdcp_v2/phaseA"
    _palog = os.path.join(H, "logs", "phaseA.log")
    if os.path.isfile(_palog):
        try:
            ll = open(_palog, errors="ignore").read().splitlines()
        except OSError:
            ll = []
        plan = sum(int(m.group(1)) for m in
                   (re.search(r"= (\d+) poses", x) for x in ll) if m)
        cases = [x for x in ll if re.search(r"E_bind = [+-]", x)]
        ncv = sum(1 for x in cases if "NOT CONVERGED" in x)
        csv_done = os.path.isfile(os.path.join(_PA, "phaseA_v7c_results.csv"))
        head = "✅ 완료" if csv_done else ("▶ 진행" if "phaseA" in TMUX else "⛔ 멈춤")
        print(f"   ── Phase-A 자세 스캔  {head} · {len(cases)}"
              + (f"/{plan}" if plan else "") + f" 케이스"
              + (f" · ⚠ 미수렴 {ncv}" if ncv else ""))
        eb = sorted((float(m.group(1)), x.split()[0]) for x in cases
                    for m in [re.search(r"E_bind = ([+-][\d.]+)", x)]
                    if m and "NOT CONVERGED" not in x)[:3]
        for v, lab in eb:
            print(f"      {v:+.3f} eV  {lab}")
        if eb:
            print("      ⚠ UMA E_bind 는 **순위용**이다 — 절대값 인용 금지. "
                  "상위 3-5 자세를 전부 Phase-B DFT+U 로 재채점한다.")
        elif not csv_done and "phaseA" in TMUX:
            print("      (아직 첫 자세 이완 중 — 슬랩/분자 기준 에너지 계산 포함)")

    # ── 슬랩 이완 허용 탐침 — 물리흡착이냐 화학흡착이냐를 가른다 (Phase-B 설계를 정함) ──
    # ⚠ freeze_frac 1.0(기본)은 좌표일치를 위해 슬랩을 통째로 얼린다. 그런데 화학흡착은
    #   표면 원자가 딸려 올라오는 현상이라 얼린 상태로는 원리적으로 못 잡는다.
    #   -> E_bind 가 깊어지면 Phase-B 에서 슬랩 상부를 풀어야 하고, 안 깊어지면
    #      진짜 물리흡착이라 기존 설계를 유지한다. DFT+U 며칠을 태우기 전에 가른다.
    _fl = os.path.join(H, "logs", "phaseA_freeslab.log")
    if os.path.isfile(_fl):
        try:
            fl = open(_fl, errors="ignore").read().splitlines()
        except OSError:
            fl = []
        got = [(float(m.group(1)), x.split()[0]) for x in fl
               for m in [re.search(r"E_bind = ([+-][\d.]+)", x)]
               if m and "NOT CONVERGED" not in x]
        # ⚠ 세션 이름이 pafree / pafree2 … 로 늘어난다 — 정확일치로 보면 놓친다.
        up = [t for t in TMUX if t.startswith("pafree")]
        st = f"▶ 진행({','.join(up)})" if up else ("✅ 완료" if got else "⛔ 멈춤")
        # 계획 케이스 수는 로그의 'N poses' 합에서 읽는다(탐침 3 → 전수 24 로 늘어남)
        pl = sum(int(m.group(1)) for m in
                 (re.search(r"= (\d+) poses", x) for x in fl) if m)
        print(f"   ── 슬랩 이완 탐침 (freeze_frac 0.6)  {st} · {len(got)}"
              + (f"/{pl}" if pl else "") + " 케이스")
        # ⚠ E_slab 이완이 수렴 안 했으면 기준 에너지가 임의값이라 E_bind 가 통째로 무효다.
        #   도구는 찍기만 하고 게이트를 안 걸므로 화면이 대신 본다.
        for x in fl:
            if x.startswith("E_slab") and "converged=" in x:
                okc = "converged=True" in x
                print(f"      {'✅' if okc else '⛔'} 맨 슬랩 이완 {x.split('(')[-1].rstrip(')')}"
                      + ("" if okc else "  ← **기준 에너지 무효. 아래 값 전부 못 씀**"))
        for v, lab in sorted(got)[:8]:
            print(f"      {v:+.3f} eV  {lab}")
        sd = [v for v, lab in got if "sulfonate" in lab]
        if sd:
            v = min(sd)
            if v > -0.40:
                print(f"      ✅ **얼린 게 문제가 아니었다** ({v:+.3f} vs 고정판 -0.258) "
                      "= 진짜 물리흡착. Phase-B 는 freeze_frac 1.0 유지.")
            else:
                print(f"      ⚠ **깊어졌다** ({v:+.3f} vs 고정판 g00 -0.244, 같은 자리)")
                print("         ⛔ 아직 '화학흡착' 이라고 부르면 안 된다 — 분자가 깨졌거나 표면에")
                print("            삽입/반응했을 수도 있다(얼렸을 땐 막혀 있던 경로다). 먼저:")
                print("            python3 tools/sdcp/check_adsorption_sanity.py --complex <xyz> \\")
                print("              --mol .../sdcp_v7c_doped.xyz --slab db/structures/"
                      "linio2_104_sym_1x4L4_relaxed.vasp")
        print("      ⚠ 이 산출물은 진단 전용 — 좌표일치가 깨져 Phase-B 입력으로 쓰지 않는다.")

    # ── Phase-B (DFT+U) — Delta 판정. 무거운 런이라 SCF 안쪽까지 본다 ──────────
    _PB = "/data/work/runs/sdcp_v2/phaseB"
    if os.path.isdir(_PB):
        RY = 13.605693
        JOBS_B = ("slab", "complex_doped", "complex_neutral", "mol_doped", "mol_neutral")
        st, mags, ens = {}, {}, {}
        for j in JOBS_B:
            o = os.path.join(_PB, j, "scf.out")
            if not os.path.isfile(o):
                st[j] = ("·", "", ""); continue
            try:
                tx = open(o, errors="ignore").read()
            except OSError:
                st[j] = ("?", "", ""); continue
            conv = "convergence has been achieved" in tx
            it = re.findall(r"iteration #\s*(\d+)", tx)
            ac = re.findall(r"estimated scf accuracy\s*<\s*([\dEe.+-]+)", tx)
            am = re.findall(r"absolute magnetization\s+=\s+([\d.]+)", tx)
            et = re.findall(r"^!\s+total energy\s+=\s+(-?[\d.]+)", tx, re.M)
            if am:
                mags[j] = float(am[-1])
            if et:
                ens[j] = float(et[-1]) * RY
            mark = "✅" if conv else ("▶" if alive("pw.x", exact=True) == "ALIVE" else "⛔")
            st[j] = (mark, f"it {it[-1]}" if it else "",
                     f"acc {float(ac[-1]):.1e}" if ac else "")
        done = sum(1 for j in JOBS_B if st[j][0] == "✅")
        print(f"   ── Phase-B (DFT+U) — Δ 판정  {done}/5 수렴")
        for j in JOBS_B:
            m, i, a = st[j]
            e = f" · E {ens[j]:.3f} eV" if j in ens else ""
            g = f" · mag {mags[j]:.2f} μB" if j in mags else ""
            print(f"      {m} {j:16s} {i:8s} {a:11s}{g}{e}")
        # ★ AFM 게이트를 화면에서도 본다 — 러너가 멈추기 전에 사람이 먼저 볼 수 있게
        if "complex_doped" in mags and "complex_neutral" in mags:
            dm = abs(mags["complex_doped"] - mags["complex_neutral"])
            ok = dm <= 2.0
            print(f"      {'✅' if ok else '⛔'} AFM 대조 — 두 복합체 자화 차 {dm:.2f} μB (허용 2.0)"
                  + ("" if ok else "  ← **Δ 오염. 러너가 멈춘다**"))
        need = ("complex_doped", "complex_neutral", "mol_doped", "mol_neutral")
        if all(k in ens for k in need):
            dlt = (ens["complex_doped"] - ens["complex_neutral"]) \
                  - (ens["mol_doped"] - ens["mol_neutral"])
            print(f"      ★ Δ = {dlt:+.4f} eV   (UMA 기준 −0.170)")
            if "slab" in ens:
                for lab, cx, mo in (("doped", "complex_doped", "mol_doped"),
                                    ("neutral", "complex_neutral", "mol_neutral")):
                    print(f"        E_ads({lab:7s}) = {ens[cx]-ens['slab']-ens[mo]:+.4f} eV")
                print("        ⚠ 개별 E_ads 는 Γ-only·전체고정이 그대로 실린다(★☆☆). 결론은 Δ 로.")
            if abs(dlt) < 0.026:
                print("      ⛔ |Δ| 가 열잡음(kT≈26 meV) 수준 — UMA 자세 선택 자체를 못 믿는다는 뜻")

    # ⚠ 옛 경로는 **한 줄만**. 재기동 안내를 찍으면 깨진 슬랩 위에서 GPU 를 태운다.
    if os.path.isdir("/data/work/runs/sdcp_linio2_binding/phaseB_v7c_slabfirst"):
        print("   ─ 옛 경로(phaseB_v7c_slabfirst)는 깨진 슬랩이라 폐기. 재기동하지 말 것.")
        print("     근거: kb/reports/sdcp_preliminary_final_2026_08_03.md §6.4")
    print(BAR)

# ═══ ③ MLIP 위원회 온도 스윕 (T1) ════════════════════════════════════════
# 판정 파일이 있으면 스윕은 **끝난 일**이다 — 한 줄로 접고 결론만 남긴다.
# ⚠ repo 경로를 $HOME 로 조립하지 않는다 — 서버마다 위치가 다르고(HOME/work/HOME) 조용히
#   "판정 없음"으로 보인다. 스크립트 자기 위치에서 올라간다.
_SWEEP = str(pathlib.Path(__file__).resolve().parents[2] / "db" / "properties"
             / "committee_temperature_sweep.json")
_sw = None
if os.path.isfile(_SWEEP):
    try:
        _sw = json.load(open(_SWEEP))
    except Exception:
        _sw = None
if _sw and not FULL and want("committee"):
    v = _sw.get("verdict", {})
    fm = _sw.get("force_model", {})
    print(f"③ MLIP 위원회 온도 스윕 — ✅ 판정 완료 ({_sw.get('date','?')})")
    print(f"   {v.get('headline','?')}")
    print(f"   온도무관 바닥 a={fm.get('linear',{}).get('intercept_eV_per_A','?')} eV/Å "
          f"({fm.get('floor_share_at_600K','?')} 몫) · 지수 n={fm.get('power',{}).get('exponent','?')}")
    print("   (--full 로 온도별 표 · db/properties/committee_temperature_sweep.json)")
    print(BAR)
elif want("committee"):
  print("③ MLIP 위원회 온도 스윕 — T1 외삽 대리지표")
  print("   기준선(600 K 교정): 프레임 중앙 0.3175 · p95 0.3669 eV/Å")
  ds = sorted(glob.glob(os.path.join(W, "committee_modelc_T*")),
              key=lambda p: int(p.rsplit("_T", 1)[1]))
  if not ds:
    print("  (아직 없음)")
  for d in ds:
    T = d.rsplit("_T", 1)[1]
    n = len(glob.glob(os.path.join(d, "pred_*.npz")))
    vf = os.path.join(d, "committee_verdict.json")
    if not os.path.exists(vf):
        lm = mtime(d)
        stale = "  ⛔ 재부팅 전 흔적" if (BOOT and lm and lm < BOOT) else ""
        print(f"  T{T}: 엔진 {n}/3 · 판정 대기{stale}")
        continue
    try:
        j = json.load(open(vf))
    except Exception:
        print(f"  T{T}: 엔진 {n}/3 · JSON 파싱 실패")
        continue
    # ⚠ 반드시 committee_frame_disagreement 에서 — 최상위 first-match 는 **쌍별** 값이다
    c = j.get("committee_frame_disagreement", {})
    mode = j.get("mode") or ""
    tag = "탐지" if mode.startswith("탐지") else ("교정" if mode.startswith("교정") else "?")
    med, ab, nf = c.get("median"), c.get("n_above_break"), j.get("n_frames")
    ms = "?" if med is None else f"{med:.4f}"
    _ = None
    # ⚠ 여기서 초과 수에 경보를 달지 않는다. 문턱은 600 K 절대값인데 조화 고체의 RMS 힘은
    #   √T 로 커지므로, 상대 정확도가 똑같아도 고온 초과는 는다. 예전엔 이 자리에
    #   '⚠⚠ 급증'을 찍었고 그건 열적 스케일링을 외삽으로 오독한 경보였다.
    #   판정은 힘 크기로 정규화하는 committee_sweep_verdict.py 가 한다.
    print(f"  T{T}: 엔진 {n}/3 · 프레임중앙 {ms} · 고정문턱초과 {ab}/{nf} · [{tag}] (정규화 전)")
  print("   ⚠ 고정문턱 초과는 **그 자체로는 판정이 아니다** (힘이 √T 로 커짐).")
  print("     판정: python3 tools/ionic/committee_sweep_verdict.py \\")
  print("             --out_json db/properties/committee_temperature_sweep.json \\")
  print("             --out_csv  db/properties/committee_temperature_sweep_origin.csv")
  print(BAR)

# ═══ ⑤ LPSOCl ELF (CPU — GPU 안 건드림) ═════════════════════════════════
print("⑤ LPSOCl ELF (CPU pw.x/pp.x — GPU 작업과 동시 실행 안전)")
E = "/data/work/runs/lpsocl_elf"
elog = os.path.join(E, "run.log")
if os.path.isfile(elog):
    t = open(elog, errors="ignore").read()
    stage = elf_stage(E)
    # ⚠ scf_must_converge 함정 — 반복수가 electron_maxstep 과 같으면 가짜 수렴
    conv = [l.strip() for l in t.splitlines() if "convergence has been achieved" in l]
    it = [l.strip() for l in t.splitlines()
          if re.search(r"iteration #|estimated scf accuracy|total energy\s+=", l)]
    # ⚠⚠ **전역 pw.x 생존으로 판정하면 안 된다.** SDCP 의 GPU pw.x 가 켜지자마자
    #   이미 끝난 ELF 가 '진행 중' 으로 되살아났다 (2026-07-30 실측: 화면에
    #   "단계: ⑥ 완료 (rho_atomic 까지) · pw.x ALIVE" 가 살아있는 섹션으로 떴다).
    #   pw.x 는 이 서버에서 여러 작업이 공유하는 이름이라 소유자를 못 가린다.
    #   **이 작업의 로그 신선도**로 본다.
    _elm = mtime(elog)
    _eage = (NOW - _elm).total_seconds() / 60 if _elm else 1e9
    _efresh = _eage < 15
    if _efresh:
        live()
    print(f"  단계: {stage} · 로그 "
          + (f"{_eage:.0f}분 전" if _elm else "없음")
          + (" (진행 중)" if _efresh else " (정지)"))
    if conv:
        print("  " + conv[-1] + "   ⚠ maxstep(200) 과 같으면 가짜 수렴")
    for l in it[-2:]:
        print("    " + l)
    err = [l.strip() for l in t.splitlines() if "Error" in l or "%%%%" in l]
    if err:
        print("  ⛔ " + err[-1][:100])
    cubes = glob.glob(os.path.join(E, "*.cube"))
    # ⚠ 이 섹션은 ✅ 를 한 번도 안 찍어서 compact 렌더러가 **끝난 ELF 를 '자료 없음'** 으로
    #   굴렸다 (2026-07-30 실측: cube 3개가 멀쩡히 있는데 그렇게 나왔다).
    #   "완료"와 "자료 없음"을 가르는 건 ✅ 유무이므로 여기서 명시적으로 찍는다.
    _need = ["lpsocl_elf.cube", "lpsocl_rho_scf.cube", "lpsocl_rho_atomic.cube"]
    _have = {os.path.basename(c) for c in cubes}
    if set(_need) <= _have:
        print(f"  ✅ 완료 — cube {len(cubes)}개 ({', '.join(sorted(_have))[:70]})")
    else:
        print(f"  산출 cube: {len(cubes)}개" +
              (" — " + ", ".join(os.path.basename(c) for c in cubes[:3]) if cubes else " (아직)")
              + f"   [남은 것: {', '.join(x for x in _need if x not in _have)}]")
else:
    print("  (미가동)")
print(BAR)

# ═══ ⑥ LPSOCl AE Bader (ELF 뒤 체인) ════════════════════════════════════
print("⑥ LPSOCl AE Bader (kjpaw + plot_num=17 — 기존 표와 비교 가능한 방법)")
B = "/data/work/runs/lpsocl_bader"
blog = os.path.join(B, "run.log")
if os.path.isfile(blog):
    t = open(blog, errors="ignore").read()
    for k, name in (("bader -p all_atom", "bader"), ("pp.x plot_num=17", "pp.x AE"),
                    ("pw.x scf_paw.in", "scf(kjpaw)"), ("[pseudo] OK", "pseudo 수집"),
                    ("ELF(pw.x/pp.x) 진행 중", "ELF 종료 대기")):
        if k in t:
            print(f"  단계: {name}")
            break
    else:
        print("  단계: ? (로그 시작 직후)")
    nit = re.findall(r"SCF 수렴 반복수 = (\S+)", t)
    if nit:
        print(f"  SCF 반복수 {nit[-1]}  ⚠ 200(=maxstep)이면 가짜 수렴")
    err = [l.strip() for l in t.splitlines() if l.strip().startswith("ERROR")]
    if err:
        print("  ⛔ " + err[-1][:100])
    s = os.path.join(B, "lpsocl_bader_summary.json")
    if not os.path.exists(s):
        live()
    if os.path.exists(s):
        try:
            d = json.load(open(s))["per_species"]
            print("  ✅ " + "  ".join(f"{k} {v['mean']:+.3f}" for k, v in d.items()))
        except Exception:
            print("  (summary 파싱 실패)")
else:
    print("  (미가동)")

# ═══ ⑦ ORCA Stage A (SDCP n=6 올리고머) ══════════════════════════════════
#   2026-08-30 신설. 왜 뒤늦게 붙나 — **이게 화면에 없어서 죽은 것을 하루 놓쳤다.**
#   gs0 이 08-30 10:29 에 정상종료(rc 0)했는데 러너가 다음 seed 로 안 넘어갔고,
#   대시보드에 패널이 없으니 11:58 까지 아무도 몰랐다. 같은 계열이 이번이 두 번째다
#   (li3nd 체인은 `alive()` 진리값 때문에 이틀).
#
# ⛔ 이 패널이 **못 하는 것**: ORCA 결과의 물리적 타당성을 판정하지 않는다.
#   수렴 표식·사이클 수·에너지를 읽어 **어디까지 갔나**만 본다. 스핀 상태가
#   옳은지, 기하가 말이 되는지는 분석기 몫이다.
print(BAR)
print("⑦ ORCA Stage A — SDCP n=6 올리고머 (CPU 전용 · GPU 안 건드림)")
_OA, _OW = "/data/work/runs/sdcp_stageA", "/data/work/runs/sdcp_stageA_run"
_oman = os.path.join(_OA, "manifest_stage_a.json")
_oseeds = []
if os.path.isfile(_oman):
    try:
        _oseeds = [(x["dir"], x["tag"])
                   for x in json.load(open(_oman)).get("geometry_seeds", [])]
    except Exception:
        print("  ⛔ manifest_stage_a.json 파싱 실패")
if not _oseeds:
    print("  (미가동 — manifest_stage_a.json 없음)")
else:
    _orun = alive("run_orca_stage_a") or alive("orca ")
    _odone, _opend, _onewest = 0, [], None
    for _d, _t in _oseeds:
        _o = os.path.join(_OW, _d, _t + ".out")
        if not os.path.isfile(_o):
            _opend.append(_d)
            continue
        _tx = open(_o, errors="ignore").read()
        _cy = _tx.count("GEOMETRY OPTIMIZATION CYCLE")
        _e = re.findall(r"FINAL SINGLE POINT ENERGY\s+(-?[\d.]+)", _tx)
        _ok = "ORCA TERMINATED NORMALLY" in _tx
        _cv = "THE OPTIMIZATION HAS CONVERGED" in _tx
        _ag = mtime(_o)
        _ag = (NOW - _ag).total_seconds() / 60 if _ag else None
        if _onewest is None or (_ag is not None and _ag < _onewest):
            _onewest = _ag
        _odone += 1 if (_ok and _cv) else 0
        print("  %-5s %s cyc=%-4s %s %s" % (
            _d,
            "✓" if (_ok and _cv) else ("⛔종료·미수렴" if _ok else "▶"),
            _cy,
            ("E=%s" % _e[-1]) if _e else "E=?",
            ("· %.0f분 전" % _ag) if _ag is not None else ""))
    _left = len(_oseeds) - _odone
    print("  진행 %d/%d · 남은 %d · 러너 %s"
          % (_odone, len(_oseeds), _left, "🔄 돈다" if _orun else "⏹ 안 돈다"))
    # ★ 이 한 줄이 이 패널의 존재 이유다 — **끝난 seed 가 있는데 러너가 없고
    #   남은 seed 가 있으면** 그건 완주가 아니라 중단이다. gs0 이 정확히 그랬다.
    _ostate = orca_runner_state(len(_oseeds), _odone, bool(_orun))
    if _ostate == "dead":
        print("  ⛔ **러너가 죽었다** — %d개 남았는데 프로세스가 없다 (%s)"
              % (_left, ", ".join(_opend[:4]) + (" …" if len(_opend) > 4 else "")))
        print("     ⚠ nohup 없이 띄우면 터미널이 닫힐 때 같이 죽는다 — gs0 뒤가 그랬다")
        print("     ORCA=/data/apps/orca-6.1.1/orca NPROCS=8 nohup bash "
              "tools/sdcp/run_orca_stage_a.sh \\")
        print("       %s %s > /data/work/runs/orca_stageA.log 2>&1 &" % (_OA, _OW))
    elif _ostate == "running":
        live()
        if _onewest is not None and _onewest > 180:
            print("  ⚠ 러너는 살아 있는데 최신 로그가 %.0f분 전이다 — 한 seed 가 "
                  "오래 걸리는 중이거나 멈춰 있다 (gs0 실측 18.5시간)" % _onewest)
    else:
        print("  ✅ 전 seed 완주")
        print("  ⛔ **이 결과로 Stage B 를 열지 않는다** (receipt 조건 6 · 회신 R4)")

# ═══ 재기동 안내 ═════════════════════════════════════════════════════════
# ⚠ 예전 판은 JOBS 목록만 보고 "재기동 필요 없음" 을 찍었다. SDCP 섹션이 바로 위에서
#   ⛔ 를 띄우고 있는데도 그랬다 — 서로 모순되는 화면이 나왔다(2026-07-30).
#   이제 **출력 전체의 ⛔ 개수**로 판정한다.
if restart and not IS_GABIA:
    # ⛔ 다른 기계에서 gabia 용 재기동 명령을 뿌리지 않는다 (2026-08-30 실측).
    print("⛔ 재기동 안내 %d건을 **막았다** — 여기는 gabia 가 아니다 (%s)"
          % (len(restart), HOSTNAME))
    print("   경로가 없어서 '미가동' 으로 보이는 것이지 작업이 죽은 것이 아니다.")
elif restart:
    print("⛔ 재기동 필요 — 아래를 repo 루트에서 그대로 실행")
    for j in restart:
        print(f"  # {j['key']}")
        print(f"  {j['start']}")


# ── li3nd 선행검사 체인 + van Hove 쓸이 (2026-08-28 신설) ─────────────────────
#   둘 다 로그 한 줄로 상태가 정해지는 작업이라 별도 watch 를 만들지 않고 여기 붙인다.
#   ⛔ 이 섹션이 못 하는 것: 결과를 **판정하지 않는다**. 어디까지 갔나만 본다.
def _tail_logs(pat, n=1):
    fs = sorted(glob.glob(pat), key=lambda f: mtime(f) or 0, reverse=True)
    return fs[:n]


if want("prereq"):
    print(BAR)
    print("■ li3nd 선행검사 체인 (리뷰 J ②~⑤)")
    # ⚠ gabia 에는 이미 `chain_gpu_release.sh` 계열의 chain* 로그가 있다 — 이름이 겹친다.
    #   선행검사 체인의 기본 로그명은 `prereq_chain_*.log` 다. 그걸 먼저 보고, 없으면 chain*.
    lg = _tail_logs("/data/work/runs/prereq_chain*.log") or _tail_logs("/data/work/runs/chain*.log")
    run = alive("run_prereq_chain")
    if not lg:
        print("  · 로그 없음 — 아직 안 걸었다")
    else:
        f = lg[0]
        txt = open(f, errors="replace").read()
        stage = [l for l in txt.splitlines() if "──" in l and ("②" in l or "③" in l
                                                              or "④" in l or "⑤" in l)]
        # ⚠ sentinel 줄은 `★ sentinel (degauss …) → **Δ +0.1 meV**` 모양이라
        #   "sentinel Δ" 로 찾으면 **안 잡힌다** (실제로 놓쳤다). 키워드로 찾는다.
        done = [l for l in txt.splitlines()
                if "sentinel" in l or "통과" in l or "장벽 범위" in l or "곡률" in l]
        # ⛔ 2026-08-28 — 첫 판은 ⛔ 로 시작하는 줄을 전부 실패로 셌다. 그런데 도구가
        #   스스로 찍는 **"못 하는 것" 안내문**도 ⛔ 로 시작한다 — 한계 설명이지 문제가 아니다.
        #   그걸 실패로 세면 오탐이고, 화면 아래 "조치 필요 N건" 카운트까지 오염된다.
        #   ⇒ **체인이 직접 찍은 줄**(ts() 가 붙이는 시각 접두)만 실패로 센다.
        # 체인이 die() 로 찍는 **명시 표지**만 실패로 센다 (2026-08-28).
        #   시각 접두만으로 세면 옛 selftest 가 남긴 ⛔ 한 줄에도 가짜 경보가 난다 — 실제로 났다.
        bad = [l for l in txt.splitlines() if "[CHAIN-FAIL]" in l]
        npt = txt.count("  ▶ ")
        if run:
            live()          # ⛔ 이걸 안 찍으면 **도는 중인데도 접힌다** (2026-08-28 실측)
        # ★ 2026-08-30 — 프로세스 생존만 보고 "진행 중" 이라 찍고 있었다. 그런데
        #   run_prereq_chain.sh 는 GPU 가 안 비면 `while …; do sleep 600; done` 으로
        #   **로그 없이 잔다**. 살아 있지만 아무 진행이 없는 상태를 정상처럼 보여준다 —
        #   이 파일 머리말이 경고한 그 오탐(재부팅 인지)과 같은 종류다.
        #   실측: 08-28 01:15 이후 58시간 무로그인데 화면은 "🔄 진행 중" 이었다.
        #   ⇒ **로그 나이와 GPU 게이트를 같이 찍는다** (ELF 절은 이미 그렇게 한다).
        # ⚠ `mtime()` 은 **datetime 을 낸다** (float 아님, 107행). 여기에
        #   `datetime.fromtimestamp()` 를 또 씌워 TypeError 로 화면이 통째로 죽었다
        #   (2026-08-30 실측). 아래 542행이 쓰는 방식과 같게 맞춘다.
        _plm = mtime(f)
        _page = (NOW - _plm).total_seconds() / 60 if _plm else 1e9
        _stall = run and _page > 90        # 정상 SCF 점 간격보다 넉넉히 크게
        print(f"  로그 {os.path.basename(f)} · SCF 시작 {npt}점 · "
              f"로그 {_page:.0f}분 전 · "
              f"{'🔄 진행 중' if run else '⏹ 안 돌고 있다'}")
        if _stall:
            def _gpu_free_mib():
                """GPU 여유 MiB. **못 재면 None** — 0 이나 큰 수로 때우지 않는다."""
                try:
                    q = subprocess.run(
                        ["nvidia-smi", "--query-gpu=memory.total,memory.used",
                         "--format=csv,noheader,nounits"],
                        capture_output=True, text=True, timeout=10)
                    t, u = (int(x) for x in q.stdout.strip().splitlines()[0].split(","))
                    return t - u
                except Exception:                                # noqa: BLE001
                    return None

            _free = _gpu_free_mib()
            print(f"  ⚠ 프로세스는 살아 있는데 로그가 {_page / 60:.1f}시간째 안 늘었다.")
            if _free is None:
                # ⛔ 못 잰 것을 "비었다" 로 말하면 안 된다 — 정지와 대기를 반대로 가른다
                print("     GPU 여유를 못 쟀다(nvidia-smi 없음/실패) — 대기인지 정지인지 "
                      "여기서는 못 가른다. pw.x 와 산출물 mtime 을 직접 볼 것.")
            elif _free < 20000:
                print(f"     GPU 여유 {_free} MiB < 20000 — **GPU 대기 루프에 잠들어 있다**"
                      f" (run_prereq_chain.sh 의 sleep 600 은 로그를 안 남긴다).")
                print("     GPU 를 쓰는 작업이 끝나야 이어진다. 지금 죽일 필요는 없다.")
            else:
                print(f"     GPU 여유 {_free} MiB ≥ 20000 인데 안 나아간다 — 대기가 아니라 "
                      f"**정지 의심**. pw.x 와 산출물 mtime 을 직접 볼 것.")
        if stage:
            print(f"  현재 단계: {stage[-1].split('──')[-1].strip()}")
        for l in done[-3:]:
            print(f"    {l.strip()[:110]}")
        if bad:
            print(f"  ⛔ {bad[-1].strip()[:110]}")
            if not run:
                print("     ⇒ 멈춰 있다. 고친 뒤 다시:  "
                      "nohup bash tools/sei/run_prereq_chain.sh --wait > /data/work/runs/chain3.log 2>&1 &")
        elif not run and "체인 끝" in txt:
            print("  ✅ 체인 완주 — ⑥(NEB 재개 판정)은 사람이 한다")
        elif not run:
            print("  ⚠ 로그에 ⛔ 도 '체인 끝' 도 없는데 프로세스가 없다 — 죽었을 수 있다")


if not FULL:
    sys.stdout = _REAL_STDOUT
    _txt = _CAP.getvalue()
    print(render(_txt))
    _n = _txt.count("⛔")
    print(BAR)
    # ⚠ ⛔ 중에는 **재기동 금지**(깨진 슬랩) 처럼 실행하면 안 되는 것도 섞인다.
    #   "전부 그대로 실행"이라고 찍으면 그걸 밟는다.
    print(f"⛔ 조치 필요 {_n}건 — 각 ⛔ 줄을 읽고 판단 (금지 표시가 있는 건 실행하지 말 것)" if _n
          else "조치 필요 없음 (등록된 작업은 진행 중이거나 완료)")
