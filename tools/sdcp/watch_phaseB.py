#!/usr/bin/env python3
"""watch_phaseB.py — SDCP Phase-B (DFT+U) 전용 화면.

    watch -n 120 python3 tools/sdcp/watch_phaseB.py

왜 따로 만드나 — watch_all 의 ② 절은 이미 끝난 슬랩 이완과 Phase-A 로 가득 차 있어서
정작 지금 도는 Phase-B 가 맨 아래 다섯 줄로 밀린다. 며칠짜리 런은 자기 화면이 있어야 한다.

무엇을 보나
  0) **살아 있나** — 산출물이 하나도 없는데 프로세스도 없으면 착수 자체가 실패한 것이다.
     그 경우 로그 꼬리를 바로 찍어 준다(가장 흔한 실패가 '입력 생성 단계에서 죽음' 이다).
  1) 존재하는 job 의 SCF 안쪽 — iteration · accuracy 궤적 · 자화 · 총에너지
     (job 목록은 고정이 아니다 — v2 5개 / v3 6개 / 탐침 1개를 자동 감지한다)
  2) ★ **AFM 대조** — 복합체들이 다른 스핀 배열로 수렴하면 Δ 도 ΔE_extract 도 오염된다.
     특히 doped 의 두 기하(물리흡착·추출)가 갈리면 ΔE_extract 는 추출이 아니라
     **스핀 전이**를 재는 값이 된다. 러너도 막지만 사람이 더 일찍 보는 게 낫다.
  3) 흡착에너지(E_ads·Δ)와 반응에너지(ΔE_rxn·ΔE_extract) — 둘은 다른 물리량이다
"""
import glob
import os
import re
import subprocess
import sys
from datetime import datetime

RY = 13.605693
# v3 가 있으면 그쪽을 본다 (v3 = 흡착에너지 + 반응에너지, job 6개)
_DEF = ("/data/work/runs/sdcp_v2/phaseB_v3"
        if os.path.isdir("/data/work/runs/sdcp_v2/phaseB_v3")
        else "/data/work/runs/sdcp_v2/phaseB")
PB = os.environ.get("PB", _DEF)
LOG = os.path.expanduser(os.environ.get("LOG", "~/logs/phaseB_v3.log"
                                        if PB.endswith("_v3") else "~/logs/phaseB.log"))
# ⚠ 고정 목록이 아니다 — v2(5개)와 v3(6개)의 job 구성이 다르고, 탐침은 1개만 만든다.
ALL_JOBS = ("slab", "complex_doped", "complex_doped_extr",
            "complex_neutral", "complex_neutral_extr", "mol_doped", "mol_neutral")
JOBS = tuple(j for j in ALL_JOBS
             if os.path.isdir(os.path.join(PB, j))) or ALL_JOBS[:5]
MAGTOL = float(os.environ.get("MAGTOL", "2.0"))
BAR = "─" * 74


def sh(c):
    try:
        return subprocess.run(c, shell=True, capture_output=True, text=True,
                              timeout=10).stdout
    except Exception:
        return ""


def alive(pat):
    """⚠ pgrep 을 shell 로 돌리면 자기 자신을 문다 — argv 로 돌리고 조상 사슬을 뺀다."""
    out = subprocess.run(["pgrep", "-f", pat], capture_output=True, text=True).stdout.split()
    anc, pid = set(), os.getpid()
    for _ in range(8):
        if pid <= 1:
            break
        anc.add(pid)
        try:
            with open(f"/proc/{pid}/status") as f:
                pid = next(int(l.split()[1]) for l in f if l.startswith("PPid:"))
        except Exception:
            break
    return [q for q in out if int(q) not in anc]


def scan(j):
    o = os.path.join(PB, j, "scf.out")
    if not os.path.isfile(o):
        return None
    try:
        tx = open(o, errors="ignore").read()
    except OSError:
        return None
    et = re.findall(r"^!\s+total energy\s+=\s+(-?[\d.]+)", tx, re.M)
    return {
        "conv": "convergence has been achieved" in tx,
        "it": re.findall(r"iteration #\s*(\d+)", tx),
        "acc": re.findall(r"estimated scf accuracy\s*<\s*([\dEe.+-]+)", tx),
        "am": re.findall(r"absolute magnetization\s+=\s+([\d.]+)", tx),
        "tm": re.findall(r"total magnetization\s+=\s+(-?[\d.]+)", tx),
        "E": float(et[-1]) * RY if et else None,
        "cpu": re.findall(r"total cpu time spent up to now is\s+([\d.]+) secs", tx),
        "mtime": os.path.getmtime(o),
    }


print("=" * 74)
gpu = sh("nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader,nounits").strip()
tmux = [t.split(":")[0] for t in sh("tmux ls").splitlines() if t.strip()]
pw = alive("pw.x")
print(f"SDCP Phase-B (DFT+U) · {datetime.now():%m-%d %H:%M} · GPU {gpu or '?'} · "
      f"pw.x {'ALIVE ×' + str(len(pw)) if pw else '-'} · tmux {' '.join(tmux) or '없음'}")
print(f"경로 {PB}")
print(BAR)

data = {j: scan(j) for j in JOBS}
any_out = any(v for v in data.values())

# ── 0) 착수 실패 진단 — 이게 제일 흔한 실패다 ────────────────────────────────
if not any_out:
    print("⛔ **산출물이 하나도 없다.**")
    inputs = glob.glob(os.path.join(PB, "*", "scf.in"))
    if len(inputs) >= len(JOBS):
        print(f"   · scf.in {len(inputs)}개 다 있음 → **입력은 다 만들었고 pw.x 실행에서 죽었다**")
    elif inputs:
        # ⚠ 생성기는 job 순서대로 쓰다가 게이트에 걸리면 거기서 죽는다 —
        #   '몇 개까지 썼나'가 곧 '어느 job 에서 걸렸나'다.
        got = sorted(os.path.basename(os.path.dirname(p)) for p in inputs)
        nxt = next((j for j in JOBS if j not in got), "?")
        print(f"   · scf.in 이 {len(inputs)}/{len(JOBS)}개뿐 ({', '.join(got)}) → "
              f"**입력 생성이 `{nxt}` 에서 멈췄다** (실행 전 단계)")
    else:
        print("   · scf.in 도 없다 → **입력 생성 단계에서 죽었다**"
              " (phaseB_v7c_dft_binding.py 인자·경로·pseudo 확인)")
    # 셀 파일 이름이 판마다 다르다 — v2 는 slab_cshrink, v3 는 slab_ref_c<c>.vasp
    cs = glob.glob(os.path.join(PB, "slab_cshrink.vasp")) + \
        glob.glob(os.path.join(PB, "slab_ref_c*.vasp"))
    print(f"   · 셀 파일 {os.path.basename(cs[0]) + ' 있음' if cs else '**없음** ← 셀 준비 단계에서 죽었을 수도'}")
    if not any(t.startswith("pb") or "phaseB" in t for t in tmux):
        print("   · Phase-B tmux 세션이 없다 — 프로세스가 끝났거나 시작을 못 했다")
    print(f"\n   로그 꼬리 ({LOG}):")
    if os.path.isfile(LOG):
        for ln in sh(f"tail -25 {LOG}").splitlines():
            print("     " + ln)
    else:
        print("     (로그 파일이 없다 — tee 경로를 확인할 것)")
    print(BAR)
    sys.exit(0)

# ── 1) job 별 SCF 안쪽 ───────────────────────────────────────────────────────
now = datetime.now().timestamp()
for j in JOBS:
    d = data[j]
    if not d:
        print(f"  ·  {j:16s} (아직 없음)")
        continue
    age = (now - d["mtime"]) / 60.0
    live = age < 20 and not d["conv"]
    mark = "✅" if d["conv"] else ("▶" if live else "⛔")
    it = d["it"][-1] if d["it"] else "-"
    acc = f"{float(d['acc'][-1]):.1e}" if d["acc"] else "-"
    mg = f"{float(d['am'][-1]):.2f}" if d["am"] else "-"
    tmg = f"{float(d['tm'][-1]):+.2f}" if d["tm"] else "-"
    hrs = f"{float(d['cpu'][-1])/3600:.1f}h" if d["cpu"] else "-"
    print(f"  {mark} {j:16s} it {it:>3s} · acc {acc:>9s} · mag {tmg:>6s}/{mg:>6s} μB · "
          f"cpu {hrs:>6s} · 로그 {age:.0f}분 전")
    if d["acc"] and len(d["acc"]) >= 4 and not d["conv"]:
        tail = [f"{float(x):.0e}" for x in d["acc"][-5:]]
        print(f"       accuracy 궤적 {' → '.join(tail)}")
        # ⚠ 평탄하면 수렴이 아니라 정체다. 300 반복까지 태우기 전에 본다.
        try:
            a0, a1 = float(d["acc"][-5]), float(d["acc"][-1])
            if a1 > a0 * 0.3:
                print("       ⚠ 5반복 동안 3배도 못 줄었다 — 정체 의심"
                      " (mixing_beta·ndim 또는 U-ramp 재검토)")
        except (ValueError, IndexError):
            pass
    if d["E"] is not None:
        print(f"       E = {d['E']:.4f} eV")

print(BAR)

# ── 2) ★ AFM 대조 — 복합체 **전부**를 본다 ──────────────────────────────────
#   ΔE_extract 는 같은 종의 두 기하 차이라, doped 물리흡착과 doped 추출이 다른 스핀
#   상태로 수렴하면 그 차이는 추출이 아니라 **스핀 전이**가 된다. Δ 보다 더 민감하다.
cx = [(j, float(data[j]["am"][-1])) for j in JOBS
      if j.startswith("complex") and data[j] and data[j]["am"]]
if len(cx) >= 2:
    lo, hi = min(v for _, v in cx), max(v for _, v in cx)
    print(f"★ AFM 대조 — 폭 {hi-lo:.2f} μB (허용 {MAGTOL})")
    for j, v in cx:
        print(f"    {j:22s} {v:6.2f} μB")
    print("   " + ("✅ 같은 자기 상태로 가고 있다 — Δ·ΔE_extract 가 성립한다"
                   if hi - lo <= MAGTOL else
                   "⛔⛔ **다른 자기 상태다.** 특히 doped 의 두 기하가 갈리면 ΔE_extract 는 "
                   "추출이 아니라 스핀 전이를 재는 값이 된다"))
elif cx:
    print(f"★ AFM 대조 — 아직 복합체 1개만 나왔다 ({cx[0][0]} {cx[0][1]:.2f} μB)")
else:
    print("★ AFM 대조 — 아직 복합체 자화가 안 나왔다 (이게 최대 리스크다)")

# ── 3) 흡착에너지 · 반응에너지 ──────────────────────────────────────────────
E = {j: data[j]["E"] for j in JOBS if data[j] and data[j]["E"] is not None}


def ads(cx_, mol_):
    if all(k in E for k in ("slab", cx_, mol_)):
        return E[cx_] - E["slab"] - E[mol_]
    return None


ad = ads("complex_doped", "mol_doped")
an = ads("complex_neutral", "mol_neutral")
rx = ads("complex_doped_extr", "mol_doped")
dx = (E["complex_doped_extr"] - E["complex_doped"]
      if {"complex_doped_extr", "complex_doped"} <= set(E) else None)

print()
if ad is not None:
    print(f"  E_ads(doped, 물리흡착)   = {ad:+.4f} eV   ← 흡착에너지")
if an is not None:
    print(f"  E_ads(neutral, 물리흡착) = {an:+.4f} eV   ← 흡착에너지")
if None not in (ad, an):
    print(f"  Δ = E_ads(d) − E_ads(n)  = {ad - an:+.4f} eV   (UMA −0.073)")
    print("     ⚠ Δ 는 프로토콜 의존적이다 (얼린 −0.170 vs top1free −0.073) — 결론을 여기 걸지 말 것")
if rx is not None:
    print(f"\n  ΔE_rxn(doped)            = {rx:+.4f} eV   ← **반응**에너지 (흡착에너지 아님)")
if dx is not None:
    print(f"  ★ ΔE_extract(doped)      = {dx:+.4f} eV   (UMA −0.942)")
    print("     기준항이 전부 상쇄되는 값이라 이 캠페인에서 제일 믿을 만하다.")
    print("     " + ("→ DFT+U 에서도 추출이 유리 = **Li 스캐빈징 열화 기구 실재**" if dx < 0 else
                     "→ DFT+U 에서는 추출이 불리 = UMA 가 Ni³⁺→Ni⁴⁺ 산화 대가를 안 문 것"))
    print("     ⚠ 열역학이지 속도론이 아니다 — 장벽은 NEB 이 있어야 말한다")
if ad is None and dx is None:
    left = [j for j in JOBS if j not in E]
    print(f"· 아직 계산 대기 — 남은 job: {', '.join(left) or '없음'}")
print(BAR)
