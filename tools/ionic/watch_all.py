#!/usr/bin/env python3
"""watch_all.py — gabia 전체 작업 한 화면.

관례:  watch -n 30 python3 tools/ionic/watch_all.py

⚠ 왜 bash 가 아니라 python 인가
  - JSON 을 grep 으로 파면 중첩 구조에서 **다른 블록의 첫 매치**를 집어 조용히 틀린 값을 띄운다.
    실제로 겪었다: 프레임 단위 중앙값(0.3175) 대신 mace|sevennet 쌍 중앙값(0.2022)이 표시됐다.
  - bash 안에 python heredoc 을 넣으면 인용 이스케이프가 겹쳐 깨진다(실제로 `cat: webapp: Is a
    directory` 같은 워드 스플리팅 사고가 났다).

환경변수
  SDCP_OUT   pw.x 출력 파일 경로(있으면 최우선)
  SDCP_TMUX  pw.x 가 도는 tmux 세션명 (기본: 전 세션을 훑어 pw.x 출력을 가진 페인을 찾는다)
"""
import glob
import json
import os
import re
import subprocess
import sys
from datetime import datetime

H = os.path.expanduser("~")
W = os.path.join(H, "work")
BAR = "-" * 70


def sh(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True,
                              timeout=15).stdout
    except Exception:
        return ""


def alive(pat, exact=False):
    r = sh(f"pgrep {'-x' if exact else '-f'} '{pat}'").strip()
    return "ALIVE" if r else "-"


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


# ═══ 헤더 ════════════════════════════════════════════════════════════════
print("=" * 70)
print(f"gabia 전체 상황  {datetime.now():%m-%d %H:%M}")
print("=" * 70)
gpu = sh("nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total "
         "--format=csv,noheader,nounits").strip() or "(조회 실패)"
print(f"GPU: {gpu}   [util%, used MiB, total MiB]")
print(f"  pw.x {alive('pw.x', exact=True)}  ·  "
      f"MLIP-MD {alive('aimd_mlip|disorder_ensemble_diffusion')}")
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
                for want, tag in (("sigma", "σ"), ("cond", "σ"),
                                  ("d_cm2", "D"), ("diffus", "D"), ("slope", "s")):
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
    want = os.environ.get("SDCP_TMUX", "")
    panes = [p for p in sh("tmux list-panes -a -F '#{session_name}:#{window_index}.#{pane_index}'"
                           ).split() if p]
    if want:
        panes = [p for p in panes if p.startswith(want + ":")] + panes
    for p in panes:
        cap = sh(f"tmux capture-pane -p -t '{p}' -S -4000")
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
    print("  (못 찾음. export SDCP_OUT=/경로.out  또는  export SDCP_TMUX=세션명)")
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
        print(f"  T{T}: 엔진 {n}/3 · 판정 대기")
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
    mark = ""
    if tag == "탐지" and isinstance(ab, int) and isinstance(nf, int) and nf:
        r = ab / nf
        mark = "  ⚠⚠ 급증" if r > 0.25 else ("  ⚠ 증가" if r > 0.10 else "  ok")
    ms = "?" if med is None else f"{med:.4f}"
    print(f"  T{T}: 엔진 {n}/3 · 프레임중앙 {ms} · break초과 {ab}/{nf} · [{tag}]{mark}")
print("   ⚠ '교정'의 초과는 정의상 5% — **'탐지' 값만 정보다.**")
print("     1000 K 급증이면 Arrhenius 상단(600/800/1000 K)이 신뢰 밖 → open_items #1 이 시드로 안 풀림")
print(BAR)

# ═══ ④ 체인 ══════════════════════════════════════════════════════════════
print("④ 후속 체인 (GPU 해방 대기 → QE 단일점 + Li 슬랩)")
cl = os.path.join(H, "logs", "chain2.log")
if os.path.isfile(cl):
    ls = [l for l in open(cl, errors="ignore").read().splitlines() if l.strip()]
    print("  " + (ls[-1] if ls else "(빈 로그)"))
else:
    print("  (chain2 미가동)")
print(BAR)
print("tmux: " + " ".join(sorted(set(
    l.split(":")[0] for l in sh("tmux ls").splitlines() if ":" in l))))
