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
import json
import os
import pathlib
import re
import subprocess
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
    {"key": "chain2", "log": os.path.join(H, "logs", "chain2.log"),
     "done": [], "proc": (), "tmux": "chain2", "start": None},
]


def verdict(j):
    """→ (한 줄 상태, 재기동 필요?)"""
    done = bool(j["done"]) and all(os.path.exists(p) for p in j["done"])
    lm = mtime(j["log"])
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


# ═══ 헤더 ════════════════════════════════════════════════════════════════
print("=" * 70)
print(f"gabia 전체 상황  {NOW:%m-%d %H:%M}")
print("=" * 70)
up = sh("uptime -p").strip() or "?"
print(f"부팅: {BOOT:%m-%d %H:%M} ({up})" if BOOT else f"부팅 시각 조회 실패 ({up})")
if BOOT and (NOW - BOOT).total_seconds() < 3600:
    print("  ⚠ 1시간 안에 부팅됨 — tmux 세션은 재부팅으로 전부 사라진다. 아래 생존판정 확인.")
print(f"tmux 세션: {' '.join(TMUX) if TMUX else '(없음)'}")
gpu = sh("nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total "
         "--format=csv,noheader,nounits").strip() or "(조회 실패)"
print(f"GPU: {gpu}   [util%, used MiB, total MiB]")
print(f"  pw.x {alive('pw.x', exact=True)}  ·  pp.x {alive('pp.x', exact=True)}  ·  "
      f"MLIP-MD {alive('aimd_mlip|disorder_ensemble_diffusion')}")
print(BAR)

# ═══ ⓪ 생존 판정 ═════════════════════════════════════════════════════════
print("⓪ 생존 판정")
restart = []
for j in JOBS:
    msg, need = verdict(j)
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
  for r in roots:
    print(f"  [{os.path.basename(r)}]")
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
            print(f"{line}  [{n}/3]")
    if done_cfgs:
        print(f"    ✅ 3/3 완료: {', '.join(done_cfgs)}   (--full 로 값 펼침)")
    if unknown_keys:
        # 자기 진단: 값을 못 찾았으면 **어떤 키가 있었는지** 알려준다
        print(f"    ⚠ 값 미검출 — {unknown_keys[0]} 최상위 키: {unknown_keys[1]}")
  print("  ordered baseline: comp2 Ea 0.276±0.033 / comp1 0.253  (disorder가 낮추면 가설 확증)")
  print(BAR)

# ═══ ② SDCP ══════════════════════════════════════════════════════════════
# 2026-07-30: 경로가 **슬랩-우선 2단계**로 바뀌었다. 그 디렉터리가 있으면 단계별
#   사다리를 보여 주고, 없으면 예전 relax 감시로 떨어진다.
#   ⚠ 예전 섹션은 "relax.out 이 있다"만 보고 SIGKILL 로 죽은 런을 이틀 내내
#     '현재:' 로 보여줬다. 여기서도 **GPU pw.x 생존**을 같이 확인한다.
_SF = "/data/work/runs/sdcp_linio2_binding/phaseB_v7c_slabfirst"
_sf_jobs = ["slab", "mol_neutral", "mol_doped", "complex_neutral", "complex_doped"]
if want("sdcp") and os.path.isdir(_SF):
    print("② SDCP 슬랩-우선 (1단계 슬랩 → 시드 승계 → 2단계 복합체)")
    _gpu_pw0 = subprocess.run(["pgrep", "-f", r"qe-.*-gpu/bin/pw\.x"],
                              capture_output=True, text=True).stdout.strip()
    _seed = os.path.join(_SF, "slab_mag.json")
    if os.path.isfile(_seed):
        try:
            _sd = json.load(open(_seed))
            print(f"   시드 승계 ✓ Ni1 {_sd.get('Ni1'):+.3f} / Ni2 {_sd.get('Ni2'):+.3f} "
                  f"(수렴 {_sd.get('Ni1_muB','?')} μB)")
        except Exception:
            print("   ⚠ slab_mag.json 을 못 읽었다")
    else:
        print("   시드 아직 — 1단계 슬랩이 끝나야 생긴다")
    _running = False
    for j in _sf_jobs:
        o = os.path.join(_SF, j, "scf.out")
        if not os.path.isfile(o):
            if FULL:
                print(f"   ·  {j:16s} (아직)")
            continue
        txt = open(o, errors="ignore").read()
        age = (NOW - datetime.fromtimestamp(os.path.getmtime(o))).total_seconds()
        if "convergence has been achieved" in txt:
            e = [l for l in txt.splitlines() if l.startswith("!")]
            print(f"   ✓  {j:16s} {e[-1].strip()[:64] if e else '수렴'}")
            continue
        # 미수렴 — 도는 중인가 죽었는가
        it = [l.strip() for l in txt.splitlines() if "iteration #" in l][-1:]
        ac = [l.strip() for l in txt.splitlines() if "estimated scf accuracy" in l][-1:]
        dead = ("signal 9" in txt or "MPI_ABORT" in txt or "%%%%" in txt)
        if dead:
            mark = "⛔ 죽음(출력에 abort)"
        elif not _gpu_pw0:
            mark = "⛔ 죽음(GPU pw.x 없음)"
        elif age > 1800:
            mark = f"⚠ {age/60:.0f}분째 출력 없음"
        else:
            mark = "▶ 진행"; _running = True
        print(f"   {mark}  {j}")
        for l in (it + ac):
            print(f"        {l[:88]}")
    if not _running:
        print("   ⛔ 도는 게 없다 — 재기동:")
        print("      tmux new -s pbslab -d 'bash ~/Yonghoon-DEM-DFT/tools/sdcp/"
              "run_phaseB_slabfirst_gabia.sh 2>&1 | tee -a "
              "/data/work/runs/sdcp_linio2_binding/pbslabfirst.log'")
    print(BAR)
    src = None                       # 아래 예전 블록을 건너뛴다
else:
    src = ""

if src is not None:
  print("② SDCP complex_doped_v2 relax (k 2×2×1)")
  src, via = "", ""
  env_out = os.environ.get("SDCP_OUT", "")
  if env_out and os.path.isfile(env_out):
      src, via = open(env_out, errors="ignore").read(), f"파일 {env_out}"
  if not src:
      # ⚠ pw.x 의 stdout 이 파일이 아니라 **tmux 페인(/dev/pts/N)** 인 경우가 있다 — 실제로 그랬다.
      #   .out 파일이 아예 없으므로 페인 스크롤백에서 읽는다. 전 세션·전 페인을 훑는다.
      #   ⚠ 재부팅 뒤엔 페인 자체가 없다 → 여기서 못 찾는 게 정상이고, 그건 '죽음'의 증거다.
      # ⚠ 먼저 **파일**을 찾는다. 페인 스크롤백은 4000줄 밖으로 밀리면 못 읽고, 실제로
      #   sdcp_cd 페인에서 아무것도 못 건진 반면 relax.out 은 디스크에 멀쩡히 있었다.
      for g in ("/data/work/runs/sdcp*/**/relax.out", "/data/work/runs/sdcp*/**/*.out",
                os.path.join(W, "runs", "sdcp*", "**", "relax.out")):
          cands = sorted(glob.glob(os.path.expanduser(g), recursive=True),
                         key=lambda f: os.path.getmtime(f), reverse=True)
          if cands:
              src, via = open(cands[0], errors="ignore").read(), f"파일 {cands[0]} (자동탐색)"
              break
  if not src:
      sess = os.environ.get("SDCP_TMUX", "sdcp_cd")   # ⚠ want() 를 덮지 않게 이름을 분리
      panes = [p for p in sh("tmux list-panes -a -F '#{session_name}:#{window_index}.#{pane_index}'"
                             ).split() if p]
      if sess:
          panes = [p for p in panes if p.startswith(sess + ":")] + panes
      for p in panes:
          cap = sh(f"tmux capture-pane -p -t '{p}' -S -20000")
          if re.search(r"iteration #|convergence has been achieved", cap):
              src, via = cap, f"tmux {p}"
              break
  # ⚠ **파일이 있다 ≠ 돌고 있다.** relax.out 은 죽어도 그대로 남아서, 이 섹션이
  #   2026-07-29 에 SIGKILL 로 죽은 런(iteration #246, accuracy 0.51 Ry)을 이틀 내내
  #   "현재:" 로 보여줬다. GPU pw.x 생존과 파일 신선도로 죽음을 못 박는다.
  _gpu_pw = subprocess.run(["pgrep", "-f", r"qe-.*-gpu/bin/pw\.x"],
                           capture_output=True, text=True).stdout.strip()
  _sdcp_dead = None
  if src:
      if "signal 9" in src or "Killed" in src or "MPI_ABORT" in src:
          _sdcp_dead = "⛔ **죽었다 — 출력에 kill/abort 흔적**"
      elif not _gpu_pw:
          _sdcp_dead = "⛔ **죽었다 — GPU pw.x 프로세스 없음** (파일만 남은 것)"
  if src:
      print(f"  source: {via}")
      if _sdcp_dead:
          print(f"  {_sdcp_dead}")
          _tail = [l.strip() for l in src.splitlines()
                   if "signal" in l or "exit code" in l or "Error" in l][-2:]
          for l in _tail:
              print("    " + l[:110])
          print("    아래 '현재:' 는 **마지막 순간의 스냅샷**이지 진행 상황이 아니다.")

      def tail(pat, k):
          ls = [l for l in src.splitlines() if re.search(pat, l)]
          return ls[-k:] if ls else []
      for l in tail(r"number of k points", 1):
          print("  " + l.strip())
      # ⚠ scf_must_converge=.false. + maxstep 도달 = **가짜 수렴**
      print("  완료 step별 반복수 (maxstep과 같으면 **가짜 수렴**):")
      done = tail(r"convergence has been achieved in", 3)
      print("\n".join("    " + l.strip() for l in done) if done else "    (아직 없음)")
      print("  현재:")
      for l in tail(r"iteration #|estimated scf accuracy", 2):
          print("    " + l.strip())
  else:
      print("  (못 찾음 — tmux 페인이 없다. 재부팅했다면 이게 정상이고 곧 재기동해야 한다.)")
      print("   export SDCP_OUT=/경로.out  또는  export SDCP_TMUX=세션명")
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
    print(f"  단계: {stage} · pw.x {alive('pw.x', exact=True)} · pp.x {alive('pp.x', exact=True)}")
    if conv:
        print("  " + conv[-1] + "   ⚠ maxstep(200) 과 같으면 가짜 수렴")
    for l in it[-2:]:
        print("    " + l)
    err = [l.strip() for l in t.splitlines() if "Error" in l or "%%%%" in l]
    if err:
        print("  ⛔ " + err[-1][:100])
    cubes = glob.glob(os.path.join(E, "*.cube"))
    print(f"  산출 cube: {len(cubes)}개" + (" — " + ", ".join(os.path.basename(c) for c in cubes[:3])
                                          if cubes else " (아직)"))
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
live = ("chain2" in TMUX
        or (_clm is not None and (NOW - _clm).total_seconds() < 900))
if os.path.isfile(cl):
    ls = [l for l in open(cl, errors="ignore").read().splitlines() if l.strip()]
    print(f"  세션 {'살아있음' if live else '없음'} · 로그 {len(ls)}줄")
    for l in ls[-2:]:
        print("    " + l[:110])
    if not live:
        print("  ⛔ 로그는 있는데 프로세스가 없다 — 끝났거나 죽었다. 마지막 줄로 판별.")
elif live:
    print("  ▶ 세션은 있는데 ~/logs/chain2.log 가 없다 — 로그 경로가 다르다")
else:
    # ⚠ 실제 사고: `tmux new -d -s chain2 '... > ~/logs/chain2.log 2>&1'` 인데 ~/logs 가
    #   없어서 리다이렉트 실패 → 셸 즉사 → 세션도 로그도 안 남았다. "안 걸렸네"로 오해하기 쉽다.
    print("  ⛔ 미가동 (세션도 로그도 없음). ~/logs 부재로 즉사했을 가능성이 크다.")
    print("     재기동: tmux new -d -s chain2 'bash tools/ionic/chain_gpu_release.sh'")
    print("     (그 스크립트가 로그 디렉터리를 직접 만들고, CPU 빌드 QE 는 대기 조건에서 뺀다)")
print(BAR)

# ═══ 재기동 안내 ═════════════════════════════════════════════════════════
if restart:
    print("⛔ 재기동 필요 — 아래를 repo 루트에서 그대로 실행")
    for j in restart:
        print(f"  # {j['key']}")
        print(f"  {j['start']}")
else:
    print("재기동 필요 없음 (등록된 작업은 진행 중이거나 완료)")
