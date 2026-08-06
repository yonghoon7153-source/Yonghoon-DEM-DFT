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
_p.add_argument("--only", default="", help="disorder|sdcp|committee|elf|bader|chain 중 하나만")
ARGS, _ = _p.parse_known_args()
FULL, ONLY = ARGS.full, ARGS.only.lower()


def want(key):
    return (not ONLY) or ONLY == key


def sh(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True,
                              timeout=15).stdout
    except Exception:
        return ""


def alive(pat, exact=False):
    """⚠ shell=True 로 pgrep -f 를 돌리면 **자기 자신을 문다**.
    `sh -c "pgrep -f 'aimd_mlip|...'"` 의 명령줄에 패턴이 그대로 들어 있어서 pgrep 이
    그 셸을 매치한다 → MLIP-MD 가 늘 ALIVE 로 보였다(실측: shell 2 pid / argv 1 pid).
    pgrep 은 자기 pid 만 제외하므로, 셸을 아예 안 끼우는 argv 호출이 정답이다."""
    try:
        r = subprocess.run(["pgrep", "-x" if exact else "-f", pat],
                           capture_output=True, text=True, timeout=15).stdout
    except Exception:
        return "?"
    return "ALIVE" if r.strip() else "-"


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
    {"key": "chain2", "log": os.path.join(H, "logs", "chain2.log"),
     # ⚠ 이 체인은 "GPU 해방 대기 → 알림" 이 전부고 READY_FOR_QE_AND_SLAB 가 **정상 종료**다.
     #   done 을 비워 뒀더니 완주한 런이 ⛔ 죽음으로 분류됐다 (실측 08-03).
     "done_marker": ("READY_FOR_QE_AND_SLAB", "GPU 해방 대기 완료 — 후속 ①② 는 수동 착수"),
     "done": [], "proc": (), "tmux": "chain2", "start": None},
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
        is_live = (_LIVE in body) or ("⛔" in body)
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


# ═══ 헤더 ════════════════════════════════════════════════════════════════
up = sh("uptime -p").strip() or "?"
gpu = sh("nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total "
         "--format=csv,noheader,nounits").strip() or "(조회 실패)"
if FULL:
    print("=" * 70)
    print(f"gabia 전체 상황  {NOW:%m-%d %H:%M}")
    print("=" * 70)
    print(f"부팅: {BOOT:%m-%d %H:%M} ({up})" if BOOT else f"부팅 시각 조회 실패 ({up})")
    print(f"tmux 세션: {' '.join(TMUX) if TMUX else '(없음)'}")
    print(f"GPU: {gpu}   [util%, used MiB, total MiB]")
else:
    # 한 줄로 — 14주 uptime 같은 건 매 30초 볼 정보가 아니다.
    print(f"gabia {NOW:%m-%d %H:%M} · {up} · tmux {' '.join(TMUX) if TMUX else '없음'} "
          f"· GPU {gpu}")
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
print(BAR)

# ═══ ④ 체인 ══════════════════════════════════════════════════════════════
print("④ 후속 체인 (GPU 해방 대기 → QE 단일점 + Li 슬랩)")
cl = os.path.join(H, "logs", "chain2.log")
# ⚠ 여기서 pgrep -f 를 쓰지 않는다. 패턴이 호출한 셸의 명령줄에 들어 있으면 자기 자신을
#   물어 늘 '살아있음' 이 된다(실제로 개발 중 그렇게 오탐했다). tmux 세션 + 로그 신선도로 본다.
_clm = mtime(os.path.join(H, "logs", "chain2.log"))
# ⚠⚠ **로그가 새것이라는 건 살아있다는 뜻이 아니다 (2026-08-03 실측).** 중복가드에 걸려
#   즉사한 런이 방금 로그 두 줄을 남겨서, 15분 신선도 규칙이 "세션 살아있음"으로 오판했다.
#   같은 화면의 ⓪ 은 "tmux 없음 → 멈춤"이라 **한 화면 안에서 두 판정이 모순**됐다.
#   생존의 근거는 tmux 세션(또는 프로세스)뿐이고, 로그 신선도는 참고 표시로만 쓴다.
# ⚠ 지역변수 이름을 live 로 두면 모듈 함수 live() 를 가려서 TypeError 가 난다.
live_chain = "chain2" in TMUX
_fresh = _clm is not None and (NOW - _clm).total_seconds() < 900
if os.path.isfile(cl):
    ls = [l for l in open(cl, errors="ignore").read().splitlines() if l.strip()]
    if live_chain:
        live()
    _done = any("READY_FOR_QE_AND_SLAB" in l for l in ls)
    print(f"  세션 {'살아있음' if live_chain else '없음'} · 로그 {len(ls)}줄"
          + ("  (로그는 15분 내 갱신 — 그러나 세션이 없으므로 생존 근거가 아니다)"
             if _fresh and not live_chain else ""))
    for l in ls[-2:]:
        print("    " + l[:110])
    if live_chain:
        pass
    elif _done:
        print("  ✅ 완주 — GPU 해방까지가 이 체인의 일이고 그건 끝났다 (READY_FOR_QE_AND_SLAB).")
        print("     남은 ①② 는 자동 실행되지 않는다: 필요할 때 손으로 착수.")
    else:
        print("  ⛔ 로그는 있는데 세션이 없다 — 완주 표시도 없으니 죽은 것이다.")
elif live_chain:
    print("  ▶ 세션은 있는데 ~/logs/chain2.log 가 없다 — 로그 경로가 다르다")
else:
    # ⚠ 실제 사고: `tmux new -d -s chain2 '... > ~/logs/chain2.log 2>&1'` 인데 ~/logs 가
    #   없어서 리다이렉트 실패 → 셸 즉사 → 세션도 로그도 안 남았다. "안 걸렸네"로 오해하기 쉽다.
    print("  ⛔ 미가동 (세션도 로그도 없음). ~/logs 부재로 즉사했을 가능성이 크다.")
    print("     재기동: tmux new -d -s chain2 'bash tools/ionic/chain_gpu_release.sh'")
    print("     (그 스크립트가 로그 디렉터리를 직접 만들고, CPU 빌드 QE 는 대기 조건에서 뺀다)")
print(BAR)

# ═══ 재기동 안내 ═════════════════════════════════════════════════════════
# ⚠ 예전 판은 JOBS 목록만 보고 "재기동 필요 없음" 을 찍었다. SDCP 섹션이 바로 위에서
#   ⛔ 를 띄우고 있는데도 그랬다 — 서로 모순되는 화면이 나왔다(2026-07-30).
#   이제 **출력 전체의 ⛔ 개수**로 판정한다.
if restart:
    print("⛔ 재기동 필요 — 아래를 repo 루트에서 그대로 실행")
    for j in restart:
        print(f"  # {j['key']}")
        print(f"  {j['start']}")

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
