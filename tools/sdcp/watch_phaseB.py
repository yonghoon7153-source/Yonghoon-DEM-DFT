#!/usr/bin/env python3
"""watch_phaseB.py — SDCP Phase-B (DFT+U) 전용 화면.

    watch -n 120 python3 tools/sdcp/watch_phaseB.py

왜 따로 만드나 — watch_all 의 ② 절은 이미 끝난 슬랩 이완과 Phase-A 로 가득 차 있어서
정작 지금 도는 Phase-B 가 맨 아래 다섯 줄로 밀린다. 며칠짜리 런은 자기 화면이 있어야 한다.

무엇을 보나
  0) **살아 있나** — 산출물이 하나도 없는데 프로세스도 없으면 착수 자체가 실패한 것이다.
     그 경우 로그 꼬리를 바로 찍어 준다(가장 흔한 실패가 '입력 생성 단계에서 죽음' 이다).
  1) job 5개의 SCF 안쪽 — iteration · accuracy 궤적 · 자화 · 총에너지
  2) ★ **AFM 대조** — 두 복합체가 다른 스핀 배열로 수렴하면 Δ 가 통째로 오염된다.
     러너도 게이트를 걸지만, 사람이 **더 일찍** 보는 게 낫다.
  3) Δ 와 개별 E_ads — ⚠ 신뢰도가 다르다(Δ ★★★ / 개별 ★☆☆)
"""
import glob
import os
import re
import subprocess
import sys
from datetime import datetime

RY = 13.605693
PB = os.environ.get("PB", "/data/work/runs/sdcp_v2/phaseB")
LOG = os.path.expanduser("~/logs/phaseB.log")
JOBS = ("slab", "complex_doped", "complex_neutral", "mol_doped", "mol_neutral")
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
    if inputs:
        print(f"   · scf.in 은 {len(inputs)}개 생성됨 → **입력은 만들었고 실행에서 죽었다**")
    else:
        print("   · scf.in 도 없다 → **입력 생성 단계에서 죽었다**"
              " (phaseB_v7c_dft_binding.py 인자·경로·pseudo 확인)")
    cs = os.path.join(PB, "slab_cshrink.vasp")
    print(f"   · slab_cshrink.vasp {'있음' if os.path.isfile(cs) else '**없음** ← c-shrink 에서 죽었을 수도'}")
    if "phaseB" not in tmux:
        print("   · tmux 세션 phaseB 도 없다 — 프로세스가 끝났거나 시작을 못 했다")
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

# ── 2) ★ AFM 대조 — Δ 를 지키는 장치 ────────────────────────────────────────
md, mn = data["complex_doped"], data["complex_neutral"]
if md and mn and md["am"] and mn["am"]:
    a, b = float(md["am"][-1]), float(mn["am"][-1])
    dm = abs(a - b)
    ok = dm <= MAGTOL
    print(f"★ AFM 대조 — doped {a:.2f} vs neutral {b:.2f} μB · 차 {dm:.2f} (허용 {MAGTOL})")
    print("   " + ("✅ 같은 자기 상태로 가고 있다 — Δ 가 성립한다"
                   if ok else
                   "⛔⛔ **다른 자기 상태다. Δ 가 오염된다.** 러너가 멈출 것이고, "
                   "이 상태의 Δ 는 쓰면 안 된다"))
else:
    print("★ AFM 대조 — 아직 두 복합체 자화가 다 안 나왔다 (이게 최대 리스크다)")

# ── 3) Δ 와 개별 E_ads ──────────────────────────────────────────────────────
E = {j: data[j]["E"] for j in JOBS if data[j] and data[j]["E"] is not None}
need = ("complex_doped", "complex_neutral", "mol_doped", "mol_neutral")
if all(k in E for k in need):
    dlt = (E["complex_doped"] - E["complex_neutral"]) - (E["mol_doped"] - E["mol_neutral"])
    print(f"\n★ Δ = E_ads(doped) − E_ads(neutral) = {dlt:+.4f} eV      (UMA 기준 −0.170)")
    if "slab" in E:
        for lab, cx, mo in (("doped", "complex_doped", "mol_doped"),
                            ("neutral", "complex_neutral", "mol_neutral")):
            print(f"    E_ads({lab:7s}) = {E[cx] - E['slab'] - E[mo]:+.4f} eV")
    print("    ⚠ Δ 는 E_slab·k-오차가 상쇄돼 ★★★ · 개별 E_ads 는 Γ-only 와 전체고정이"
          " 그대로 실려 ★☆☆ — 논문엔 조건 병기, 결론은 Δ 로")
    if abs(dlt) < 0.026:
        print("    ⛔ |Δ| 가 열잡음(kT≈26 meV) 수준 — UMA 자세 선택 자체를 못 믿는다는 뜻")
    elif dlt > 0:
        print("    ⛔ **부호가 UMA 와 반대다** — 'doped 가 더 잘 붙는다' 가설이 뒤집힌다")
else:
    left = [k for k in need if k not in E]
    print(f"\n· Δ 계산 대기 — 남은 job: {', '.join(left)}")
print(BAR)
