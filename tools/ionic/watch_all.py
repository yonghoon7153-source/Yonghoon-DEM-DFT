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
import re
import subprocess
from datetime import datetime

H = os.path.expanduser("~")
W = os.path.join(H, "work")
BAR = "-" * 70
NOW = datetime.now()


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


def find_scalar(o, want, depth=0):
    """json 안을 재귀로 훑어 키에 `want` 가 든 **스칼라**를 찾는다.
    ⚠ 키 이름을 하드코딩하면 파이프라인이 바뀔 때 조용히 0/3 으로 보인다 — 실제로 그랬다."""
    if depth > 6:
        return None
    if isinstance(o, dict):
        for k, v in o.items():
            if want in str(k).lower() and isinstance(v, (int, float)):
                return v
        for v in o.values():
            r = find_scalar(v, want, depth + 1)
            if r is not None:
                return r
    elif isinstance(o, list):
        for v in o[:20]:
            r = find_scalar(v, want, depth + 1)
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
                for want, tag in (("sigma", "σ"), ("cond", "σ"),
                                  ("cm2", "D"), ("diffus", "D"), ("d_li", "D")):
                    hit = find_scalar(d, want)
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
        print(f"{line}  [{n}/3]")
    if unknown_keys:
        # 자기 진단: 값을 못 찾았으면 **어떤 키가 있었는지** 알려준다
        print(f"    ⚠ 값 미검출 — {unknown_keys[0]} 최상위 키: {unknown_keys[1]}")
print("  ordered baseline: comp2 Ea 0.276±0.033 / comp1 0.253  (disorder가 낮추면 가설 확증)")
print(BAR)

# ═══ ② SDCP relax ════════════════════════════════════════════════════════
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
    want = os.environ.get("SDCP_TMUX", "sdcp_cd")
    panes = [p for p in sh("tmux list-panes -a -F '#{session_name}:#{window_index}.#{pane_index}'"
                           ).split() if p]
    if want:
        panes = [p for p in panes if p.startswith(want + ":")] + panes
    for p in panes:
        cap = sh(f"tmux capture-pane -p -t '{p}' -S -20000")
        if re.search(r"iteration #|convergence has been achieved", cap):
            src, via = cap, f"tmux {p}"
            break
if src:
    print(f"  source: {via}")

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
print("③ MLIP 위원회 온도 스윕 — T1 외삽 대리지표")
print("   기준선(600 K 교정): 프레임 중앙 0.3175 · p95 0.3669 eV/Å")
ds = sorted(glob.glob(os.path.join(W, "committee_modelc_T*")),
            key=lambda p: int(p.rsplit("_T", 1)[1]))
if not ds:
    print("  (아직 없음)")
for d in ds:
    T = d.rsplit("_T", 1)[1]
    n = len(glob.glob(os.path.join(d, "pred_*.npz")))
    v = os.path.join(d, "committee_verdict.json")
    if not os.path.exists(v):
        lm = mtime(d)
        stale = "  ⛔ 재부팅 전 흔적" if (BOOT and lm and lm < BOOT) else ""
        print(f"  T{T}: 엔진 {n}/3 · 판정 대기{stale}")
        continue
    try:
        j = json.load(open(v))
    except Exception:
        print(f"  T{T}: 엔진 {n}/3 · JSON 파싱 실패")
        continue
    # ⚠ 반드시 committee_frame_disagreement 에서 — 최상위 first-match 는 **쌍별** 값이다
    c = j.get("committee_frame_disagreement", {})
    mode = j.get("mode") or ""
    tag = "탐지" if mode.startswith("탐지") else ("교정" if mode.startswith("교정") else "?")
    med, ab, nf = c.get("median"), c.get("n_above_break"), j.get("n_frames")
    ms = "?" if med is None else f"{med:.4f}"
    # ⚠ 여기서 초과 수에 경보를 달지 않는다. 문턱은 600 K 절대값인데 조화 고체의 RMS 힘은
    #   √T 로 커지므로, 상대 정확도가 똑같아도 고온 초과는 는다. 예전엔 이 자리에
    #   '⚠⚠ 급증'을 찍었고 그건 열적 스케일링을 외삽으로 오독한 경보였다.
    #   판정은 힘 크기로 정규화하는 committee_sweep_verdict.py 가 한다.
    print(f"  T{T}: 엔진 {n}/3 · 프레임중앙 {ms} · 고정문턱초과 {ab}/{nf} · [{tag}] (정규화 전)")
print("   ⚠ '교정'의 초과는 정의상 5% — 기준선 표본의 초과 수는 결과가 아니다.")
print("   ⚠ 고온의 고정문턱 초과도 **그 자체로는 판정이 아니다** (힘이 √T 로 커짐).")
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
    stage = "?"
    for k, name in (("pp_rho_at.in", "pp.x rho_atomic"), ("pp_rho.in", "pp.x rho_scf"),
                    ("pp.x elf", "pp.x ELF"), ("scf_atomic", "atomic ρ scf"),
                    ("pw.x scf.in", "scf"), ("[pseudo] OK", "pseudo 수집")):
        if k in t:
            stage = name
            break
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
