#!/usr/bin/env python3
"""watch_kgy.py — kgy(RTX3090) 한 화면.

    watch -n 60 python3 tools/ionic/watch_kgy.py

⚠⚠ **kgy 는 우리 브랜치가 아니다.** `claude/stoic-knuth-NObVQ` 를 쓰고 있어서
  `git pull` 로는 우리 코드가 안 온다(2026-07-31 실측: pull 이 전혀 다른 프로젝트의
  scripts/cam_kinetics.py 를 가져왔다). 갱신은 항상:
      git fetch origin claude/friendly-meitner-lldvar
      git checkout FETCH_HEAD -- <필요한 경로>
  이 화면 맨 아래가 그걸 매번 상기시킨다.

⚠ 왜 bash 가 아니라 python 인가 — watch_all.py 와 같은 이유. JSON 을 grep 으로 파면
  중첩에서 엉뚱한 값을 조용히 집는다.

⚠ **완료 판정은 msd.json 의 D 값**이지 디렉터리 존재가 아니다. 드라이버가 resume-safe 라
  중간에 죽어도 디렉터리는 남는다.
"""
import glob
import json
import math
import os
import re
import subprocess
from datetime import datetime

H = os.path.expanduser("~")
NOW = datetime.now()
BAR = "-" * 68
kB = 8.617333262e-5
TS = (600, 800, 1000)
PROD_PS, EQ_PS = 200.0, 5.0
TOTAL_PS = EQ_PS + PROD_PS

# deck 궤적(driver 기본 seed 1234) = 1번 시드. li_transport.json headline_PAPER_GRADE 등록값.
DECK = {600: 3.09e-06, 800: 1.03e-05, 1000: 2.20e-05}
# 비교 상대 — 이게 닫으려는 충돌이다 (open_items #1)
MODELC_3SEED = "modelc 0.197±0.032 (3-seed)"


def sh(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True,
                              timeout=10).stdout
    except Exception:
        return ""


def _ancestry():
    """자기 자신 + 부모 사슬 PID 집합."""
    out, pid = set(), os.getpid()
    for _ in range(8):
        if pid <= 1:
            break
        out.add(pid)
        try:
            with open(f"/proc/{pid}/status") as f:
                pid = next(int(l.split()[1]) for l in f if l.startswith("PPid:"))
        except Exception:
            break
    return out


def alive(pat):
    """pgrep -f 를 argv 로 돌리되 **자기 조상 사슬을 뺀다**.

    ⚠⚠ shell=True 는 물론이고 argv 로 돌려도, 우리를 띄운 **부모 셸의 명령줄**에
      패턴이 들어 있으면 그 부모가 잡힌다(실측: 테스트 셸이 잡혀 늘 ALIVE).
      watch(1) 로 돌 땐 안 걸리지만, 손으로 확인할 때 조용히 거짓 ALIVE 가 된다.
    """
    pids = subprocess.run(["pgrep", "-f", pat], capture_output=True,
                          text=True).stdout.split()
    anc = _ancestry()
    return [q for q in pids if int(q) not in anc]


def arrhenius(D):
    """{T: D} → Ea (eV). 점이 2개 미만이면 None."""
    pts = [(1.0 / t, math.log(d)) for t, d in sorted(D.items()) if d and d > 0]
    if len(pts) < 2:
        return None
    n = len(pts)
    sx = sum(p[0] for p in pts); sy = sum(p[1] for p in pts)
    sxx = sum(p[0] ** 2 for p in pts); sxy = sum(p[0] * p[1] for p in pts)
    den = n * sxx - sx * sx
    if abs(den) < 1e-30:
        return None
    return -((n * sxy - sx * sy) / den) * kB


def md_progress(d):
    """md.log 마지막 Time[ps] → (ps, 퍼센트). 못 읽으면 (None, None)."""
    f = os.path.join(d, "md.log")
    if not os.path.isfile(f):
        return None, None
    try:
        with open(f, "rb") as fh:                    # 큰 파일 — 꼬리만
            fh.seek(0, 2)
            fh.seek(max(0, fh.tell() - 4096))
            tail = fh.read().decode(errors="ignore").splitlines()
    except Exception:
        return None, None
    for ln in reversed(tail):
        m = re.match(r"\s*([\d.]+)\s+-?[\d.]+", ln)
        if m:
            ps = float(m.group(1))
            return ps, 100.0 * min(1.0, ps / TOTAL_PS)
    return None, None


print("=" * 68)
gpu = sh("nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total "
         "--format=csv,noheader,nounits").strip() or "(조회 실패)"
tmux = [t.split(":")[0] for t in sh("tmux ls").splitlines() if t.strip()]
print(f"kgy {NOW:%m-%d %H:%M} · GPU {gpu} [util%, used, total MiB] · "
      f"tmux {' '.join(tmux) if tmux else '없음'}")
# ⚠ shell=True 로 pgrep -f 를 돌리면 **자기 자신을 문다** — 명령줄에 패턴이 그대로
#   들어 있어서 늘 ALIVE 가 된다(watch_all.py 에서 이미 당한 것을 여기서 또 냈다).
print(f"  MLIP-MD {'ALIVE' if alive('disorder_ensemble_diffusion') else '-'}")
print(BAR)

# ═══ ① comp1 멀티시드 (open_items #1 을 닫는 계산) ═══════════════════════
print("① comp1 멀티시드 — modelc Ea 정본 충돌을 닫는다 (open_items #1)")
ROOT = os.path.join(H, "work", "runs", "comp1_seeds")
allD = {"deck(1234)": dict(DECK)}
done_files = []
n_done = 0                     # 부분 완료(seed 하나에 T 두 개 등)도 세는 카운터
if not os.path.isdir(ROOT):
    print(f"  (아직 — {ROOT} 없음)")
else:
    for s in (2, 3):
        srow, Ds = [], {}
        live = ""
        for T in TS:
            d = os.path.join(ROOT, f"s{s}", "d0.00_cfg0", f"T{T}")
            mj = os.path.join(d, "msd.json")
            D = None
            if os.path.isfile(mj):
                try:
                    D = json.load(open(mj)).get("D_Li_cm2_s")
                except Exception:
                    D = None
            if D:
                Ds[T] = float(D)
                srow.append(f"{T}K✓({D:.2e})")
                done_files.append(mj); n_done += 1
            else:
                ps, pct = md_progress(d)
                if ps is not None:
                    srow.append(f"{T}K▶{pct:.0f}%")
                    live = f"    ▶ 지금 T{T} — {ps:.1f}/{TOTAL_PS:.0f} ps ({pct:.0f}%)"
                else:
                    srow.append(f"{T}K·")
        ea = arrhenius(Ds)
        tag = f"  s{s} : " + "  ".join(srow) + f"   [{len(Ds)}/3]"
        print(tag + (f"  Ea {ea:.4f} eV" if ea else ""))
        if live:
            print(live)
        if len(Ds) == 3:
            allD[f"s{s}"] = Ds

    # ── 3-seed 판정 (다 끝나면) ─────────────────────────────────────────
    eas = {k: arrhenius(v) for k, v in allD.items()}
    eas = {k: v for k, v in eas.items() if v}
    print(f"  기준선 deck(1234) Ea {eas.get('deck(1234)', float('nan')):.4f} eV "
          f"(li_transport.json headline)")
    if len(eas) == 3:
        vals = list(eas.values())
        mean = sum(vals) / 3
        sd = (sum((v - mean) ** 2 for v in vals) / 2) ** 0.5
        print(f"  ✅ **3-seed 완성**: comp1 Ea = {mean:.4f} ± {sd:.4f} eV "
              f"({' / '.join(f'{k} {v:.4f}' for k, v in eas.items())})")
        print(f"     → {MODELC_3SEED} 와 **같은 프로토콜**로 비교 가능. "
              "open_items #1 닫을 조건 충족.")
        print("     ⚠ 등록 전에 modelc 단일-deck 앵커(0.2235)를 SUPERSEDED 로 표시할 것.")
    else:
        left = 6 - n_done
        eta = ""
        if len(done_files) >= 2:
            ts = sorted(os.path.getmtime(f) for f in done_files)
            per = (ts[-1] - ts[0]) / (len(ts) - 1) / 3600.0
            # ⚠ per 가 0 이면(같은 mtime) ETA 를 찍지 않는다 — "0 h 남음"은 거짓말이다
            if per > 0.05:
                eta = f" · 런당 {per:.1f} h → 남은 {left}개 대략 {per * left:.0f} h"
        print(f"  진행 {n_done}/6 완료 · 남은 {left}개{eta}")

if not alive("run_comp1_seeds.sh") and "c1md" not in tmux:
    print("  ⛔ 프로세스도 tmux 도 없다 — 재기동:")
    print("     conda activate uma && PY=$(which python3) && mkdir -p ~/work && \\")
    print("     tmux new -s c1md -d \"PY=$PY bash tools/ionic/run_comp1_seeds.sh "
          "> ~/work/comp1_seeds.log 2>&1\"")
    print("     ⚠ 환경변수는 따옴표 **안쪽** — tmux 는 서버-클라이언트라 밖에 두면 안 넘어간다.")
print(BAR)

# ═══ ② VGCF NEB (완료 — 한 줄) ═══════════════════════════════════════════
NEB = os.path.join(H, "work", "vgcf_hbn", "neb")
if os.path.isdir(NEB):
    # ⚠ 하위 디렉터리를 다 세면 안 된다 — QE 의 outdir `tmp/` 가 끼어 7/8 로 보였다
    #   (2026-07-31 실측). **neb.out 이 있는 것만** 케이스다.
    cases = sorted(os.path.basename(os.path.dirname(o))
                   for o in glob.glob(os.path.join(NEB, "*", "neb.out")))
    conv = 0
    for c in cases:
        try:
            if "activation energy" in open(os.path.join(NEB, c, "neb.out"),
                                           errors="ignore").read().lower():
                conv += 1
        except Exception:
            pass
    print(f"② VGCF NEB — {conv}/{len(cases)} 수렴 · ✅ 기전 판정 완료(2026-07-30) "
          "= **CONFINEMENT**")
    print("   상세: bash tools/vgcf_hbn/watch_neb.sh · "
          "kb/results/vgcf_hbn_gallery_mechanism_2026_07_30.md")
    print("   ⚠ 남은 구멍은 3L 포화뿐 — 0.147 eV 는 '수렴값' 아닌 **2L 값**으로만 인용.")
    print("     닫으려면 Li_in_gallery_3L1L (129 atoms = 2L2L 과 같은 크기, kgy 실현 검증됨).")
    print(BAR)

# ═══ 브랜치 상기 ═════════════════════════════════════════════════════════
br = sh("git -C ~/Yonghoon-DEM-DFT branch --show-current").strip()
if br and br != "claude/friendly-meitner-lldvar":
    print(f"⚠ kgy 브랜치 = {br} (우리 브랜치 아님). git pull 로는 우리 코드가 안 온다:")
    print("   git fetch origin claude/friendly-meitner-lldvar && \\")
    print("   git checkout FETCH_HEAD -- <필요한 경로>")
