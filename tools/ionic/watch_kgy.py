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


def beta(mj, lo=2.0, hi=50.0):
    """msd.json → 창 [lo,hi] 의 log-log 기울기. 확산이면 ~1.

    ⚠ 이 화면이 예전에 '3-seed 완성 → open_items #1 닫을 조건 충족' 이라고 찍었는데,
      정작 6/6 이 케이지(β 0.17–0.79)라 **그 Ea 를 쓰면 안 되는** 상태였다(2026-08-01).
      Ea 를 보여줄 거면 게이트도 같은 화면에서 보여줘야 한다.
    """
    try:
        d = json.load(open(mj))
        return _beta_series(d.get("times_ps"), d.get("msd_Li_A2"), lo, hi)
    except Exception:
        return None


def _beta_series(t, y, lo=2.0, hi=50.0):
    """시계열 자체에서 log-log 기울기. MTO 계열(msd_Li_A2_mto)에도 같은 게이트를 건다."""
    if not t or not y:
        return None
    pts = [(math.log(a), math.log(b)) for a, b in zip(t, y)
           if lo <= a <= hi and a > 0 and b > 0]
    if len(pts) < 3:
        return None
    n = len(pts)
    sx = sum(q[0] for q in pts); sy = sum(q[1] for q in pts)
    sxx = sum(q[0] ** 2 for q in pts); sxy = sum(q[0] * q[1] for q in pts)
    den = n * sxx - sx * sx
    return (n * sxy - sx * sy) / den if abs(den) > 1e-30 else None


def _ens_beta(mjs, lo=2.0, hi=50.0):
    """여러 시드의 msd.json → **MSD 를 평균한 뒤** 그 곡선의 β.

    ⚠ mean(β_i) 와 다른 양이다(β 는 로그 기울기라 비선형). 우리 규율은 앙상블 평균 쪽이다.
    ⚠ 시드마다 times_ps 격자가 다르면 평균이 성립하지 않으므로 **길이가 같은 것만** 쓴다.
    """
    ts, ys = None, []
    for mj in mjs:
        if not mj:
            continue
        try:
            d = json.load(open(mj))
            t, y = d.get("times_ps"), d.get("msd_Li_A2")
        except Exception:
            continue
        if not t or not y or len(t) != len(y):
            continue
        if ts is None:
            ts = t
        if len(t) != len(ts):
            continue
        ys.append(y)
    if not ts or not ys:
        return None
    mean = [sum(col) / len(col) for col in zip(*ys)]
    return _beta_series(ts, mean, lo, hi)


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

# ═══ ① comp1 멀티시드 — **판정 종료**. 기본은 3줄 요약 ═══════════════════
# ⚠ 이 항목은 2026-08-06 에 닫혔다(결론: 시간으로는 못 닫는다, 셀 확대 필요).
#   화면은 '지금 무엇을 봐야 하나' 를 위한 것이지 기록 보관소가 아니다 —
#   닫힌 판정을 60 초마다 6 줄씩 다시 읽을 이유가 없다. 원장은 open_items #1.
#   원본 표가 필요하면 `V=1 python3 tools/ionic/watch_kgy.py`.
VERBOSE = os.environ.get("V", "") not in ("", "0")

ROOT = os.path.join(H, "work", "runs", "comp1_seeds")
LONG = os.path.join(H, "work", "runs", "comp1_seeds_p1600")


def scan_seeds(root, seeds, ts=TS):
    """{seed: {T: (D, beta)}} — msd.json 의 D 가 있는 것만."""
    out = {}
    for s in seeds:
        row = {}
        for T in ts:
            for d in (os.path.join(root, f"s{s}", "d0.00_cfg0", f"T{T}"),
                      os.path.join(root, f"s{s}", f"T{T}")):
                mj = os.path.join(d, "msd.json")
                if not os.path.isfile(mj):
                    continue
                try:
                    D = json.load(open(mj)).get("D_Li_cm2_s")
                except Exception:
                    D = None
                if D:
                    row[T] = (float(D), beta(mj))
                break
        if row:
            out[s] = row
    return out


s200 = scan_seeds(ROOT, (2, 3))
s1600 = scan_seeds(LONG, (1, 2, 3, 4))
n200 = sum(len(v) for v in s200.values())
n1600 = sum(len(v) for v in s1600.values())


def _gate_counts(sc):
    ok = bad = 0
    for row in sc.values():
        for _, b in row.values():
            if b is None:
                continue
            ok, bad = (ok + 1, bad) if 0.8 <= b <= 1.2 else (ok, bad + 1)
    return ok, bad


ok2, bad2 = _gate_counts(s200)
ok16, bad16 = _gate_counts(s1600)

print("① comp1 — ✅ **판정 종료 (2026-08-06)**: 시간으로는 못 닫는다")
if n200 or n1600:
    print(f"   200 ps 게이트 {ok2}/{ok2 + bad2} 통과 · "
          f"1600 ps(8배) {ok16}/{ok16 + bad16} 통과(1000 K 만) · "
          f"같은 시드 Ea +0.133 eV 이동 = 3시드 산포의 2.3배")
    print("   창 재적합도 구제 아님(600 K 는 어떤 창에서도 확산영역 없음) · MTO 도 불가 "
          "→ **남은 수는 셀 확대**")
    print("   ⛔ 현재 comp1 에 **인용 가능한 Ea 없음**. 원장: kb/open_items.md #1 · "
          "db/properties/msd_window_scan_comp1_p1600.csv")
else:
    print(f"   (런 없음 — {ROOT})")

if VERBOSE and (n200 or n1600):
    print("   ── V=1 상세 ──────────────────────────────────────────────")
    for tag, sc in (("200 ps ", s200), ("1600ps ", s1600)):
        for s, row in sorted(sc.items()):
            cells = "  ".join(
                f"{T}K({D:.2e})" + ("" if b is None else
                                    ("✅" if 0.8 <= b <= 1.2 else "⛔") + f"β{b:.2f}")
                for T, (D, b) in sorted(row.items()))
            ea = arrhenius({T: D for T, (D, _) in row.items()})
            print(f"   {tag}s{s} : {cells}" + (f"   Ea {ea:.4f} eV" if ea else ""))
    print(f"   deck(1234) Ea {arrhenius(DECK):.4f} eV (li_transport.json headline)")

# 아직 안 끝난 1600 ps 런이 있으면 그것만 살려 둔다 (진행 중인 것은 화면에 필요하다)
for d in sorted(glob.glob(os.path.join(LONG, "s*", "*", "T*"))
                + glob.glob(os.path.join(LONG, "s*", "T*"))):
    if os.path.isfile(os.path.join(d, "msd.json")):
        continue
    ps, _ = md_progress(d)
    if ps is not None:
        print(f"   ▶ 진행 중 {os.path.relpath(d, LONG)} — {ps:.0f}/1605 ps "
              f"({100 * ps / 1605:.0f}%)")
print(BAR)

# ═══ ② VGCF NEB — 완료. 한 줄 + 남은 구멍 한 줄 ═══════════════════════════
NEB = os.path.join(H, "work", "neb")
if os.path.isdir(NEB):
    cases = [c for c in sorted(os.listdir(NEB)) if os.path.isdir(os.path.join(NEB, c))]
    conv = 0
    for c in cases:
        try:
            if "activation energy" in open(os.path.join(NEB, c, "neb.out"),
                                           errors="ignore").read().lower():
                conv += 1
        except Exception:
            pass
    print(f"② VGCF NEB — {conv}/{len(cases)} 수렴 · ✅ 기전 = **CONFINEMENT**(2026-07-30) · "
          "상세 `bash tools/vgcf_hbn/watch_neb.sh`")
    print("   ⚠ 0.147 eV 는 **2L 값**(수렴값 아님). 닫으려면 Li_in_gallery_3L1L (129 atoms).")
    print(BAR)

# ═══ ③ 6점 아레니우스 — 지금 도는 것. 화면의 주인공 ══════════════════════
# 왜 500 K 를 뺐나: comp1 이 **600 K / 1600 ps 로도** 게이트 실패(β0.37)했고 창 재적합도
#   구제가 아니었다(어떤 창에서도 확산영역 없음). 500 K 는 100 K 더 낮은데 계획 prod 는
#   1/4(400 ps)이라 거의 확실히 탈락한다. → 700/900 을 먼저 돌려 **MTO 의 실측 효과**와
#   500 K 필요량을 정하고 나서 500 K 를 건다. 6점을 포기한 게 아니라 **순서를 바꾼 것**.
ARR = os.path.join(H, "work", "runs", "arrhenius_6pt")
SYSL = ("modelc", "lpsocl", "b2o3")
SEEDL = (2, 3, 4)
# 계획: 신규 700/900 x 3계 x 3시드 = 18 · lpsocl 600 재실행 3 = 21
PLAN = [(lab, T, s) for lab in SYSL for T in (700, 900) for s in SEEDL] \
       + [("lpsocl", 600, s) for s in SEEDL]
ARR_TOTAL_PS = EQ_PS + 200.0
arr_up = [s for s in ("arr6", "arrchain") if s in tmux]

print("③ 6점 아레니우스 — **700/900 선행** (500 K 는 이 β 를 보고 정한다)")
print("   ⚠ 500 K 400 ps 를 지금 안 태우는 이유: comp1 이 600 K/1600 ps 로도 탈락했다. "
       "500 K 는 100 K 더 낮고 prod 는 1/4.")

cell, live, done_mt = {}, [], []
# ⚠⚠ 드라이버(disorder_ensemble_diffusion.py)는 --out_root **아래에 또**
#   `d{disorder}_cfg{n}/T{T}/` 를 만든다. 즉 산출물은
#     arrhenius_6pt/<계>/T700_s2/d0.00_cfg0/T700/{msd.json,md.log}
#   이지 T700_s2/ 바로 밑이 아니다. 직접 경로로 찾으면 **돌고 있는데 0/21 로 보인다**
#   (2026-08-06 실측: GPU 93 % 인데 화면은 진행 표시 0). 항상 재귀로 찾는다.
def _under(d, name):
    hits = glob.glob(os.path.join(d, "**", name), recursive=True)
    return hits[0] if hits else None


for lab, T, s in PLAN:
    d = os.path.join(ARR, lab, f"T{T}_s{s}")
    mj = _under(d, "msd.json")
    if mj:
        try:
            j = json.load(open(mj))
            D = j.get("D_Li_cm2_s")
        except Exception:
            j, D = {}, None
        if D:
            b = beta(mj)
            # ★ 신규 런은 다중 시간원점(MTO)을 갖는다 — 있으면 그 β 도 같이 본다.
            #   MTO 의 실측 효과를 보는 것이 이번 판의 목적 중 하나다.
            bm = beta(mj) if "msd_Li_A2_mto" not in j else _beta_series(
                j.get("times_ps_mto") or j.get("times_ps"), j["msd_Li_A2_mto"])
            cell[(lab, T, s)] = (float(D), b, bm, "msd_Li_A2_mto" in j)
            done_mt.append(os.path.getmtime(mj))
            continue
    lg = _under(d, "md.log")
    ps, pct = md_progress(os.path.dirname(lg)) if lg else (None, None)
    if ps is not None:
        cell[(lab, T, s)] = None
        live.append((lab, T, s, ps, 100.0 * min(1.0, ps / ARR_TOTAL_PS)))
    elif os.path.isdir(d):
        # 디렉터리는 생겼는데 md.log 가 아직 없다 = 방금 착수(구조 준비/UMA 로드)
        live.append((lab, T, s, None, None))

n_done = sum(1 for v in cell.values() if v)
print(f"   진행 **{n_done}/{len(PLAN)}**"
      f"{'  ▶ ' + ','.join(arr_up) if arr_up else '  ⛔ 세션 없음 — 죽었는지 확인'}", end="")
if len(done_mt) >= 2:
    ts_ = sorted(done_mt)
    per = (ts_[-1] - ts_[0]) / (len(ts_) - 1) / 3600.0
    if per > 0.02:
        print(f" · 런당 {per:.2f} h → 남은 {len(PLAN) - n_done}개 ≈ {per * (len(PLAN) - n_done):.0f} h",
              end="")
print()

# ── 계 x 온도 격자 (시드별 게이트를 그대로 보여준다) ────────────────────────
# ⚠ 한글은 터미널에서 2칸을 먹는다 — 헤더에 쓰면 열이 어긋난다. 라벨은 ASCII 로.
W = 27
print("     " + "system".ljust(9) + "".join(f"{T} K".ljust(W) for T in (600, 700, 900)))
mto_seen = False
for lab in SYSL:
    cells = []
    for T in (600, 700, 900):
        if (lab, T, SEEDL[0]) not in [(l, t, s) for l, t, s in PLAN]:
            cells.append("-".ljust(W))
            continue
        marks = []
        for s in SEEDL:
            v = cell.get((lab, T, s))
            if v is None and (lab, T, s) in cell:
                marks.append(f"s{s}▶")
            elif v:
                D, b, bm, has = v
                mto_seen |= has
                g = "·" if b is None else ("✓" if 0.8 <= b <= 1.2 else "✗")
                marks.append(f"s{s}{g}")
            else:
                marks.append(f"s{s}·")
        Ds = [cell[(lab, T, s)][0] for s in SEEDL if cell.get((lab, T, s))]
        # ★★ 게이트는 **시드 MSD 를 평균한 곡선의 β** 로 건다 — 시드별 β 의 평균이 아니다.
        #   β 는 log-log 기울기라 비선형이라서 β(mean MSD) ≠ mean(β_i) 다. 그리고
        #   앙상블 평균은 통계를 늘려 β 를 1 쪽으로 올린다 — 그게 우리가 쓰는 판정량이다
        #   (open_items #1: "modelc·b2o3 **3시드 평균** 검사 0.87/0.93/0.92 통과",
        #    LPSOCl 600 K 는 "4시드 **앙상블 평균**에서 β 0.61 탈락").
        #   ⚠ 시드별로 게이트를 걸어 통과한 것만 평균하면 **선택 편향**이 생긴다 —
        #     D 가 큰 시드가 β 도 좋을 확률이 높아 D 를 위로 밀어 올린다.
        bens = _ens_beta([_under(os.path.join(ARR, lab, f"T{T}_s{s}"), "msd.json")
                          for s in SEEDL if cell.get((lab, T, s))])
        # ⚠ 시드가 다 안 모인 β̄ 는 **판정량이 아니다** — 화면에 n 을 붙여 잠정임을 못박는다.
        #   (2026-08-07: 1시드 β̄ 를 확정값으로 읽을 뻔했다. 규율은
        #    kb/methodology/beta_gate_seed_policy.md)
        # bens 가 쓴 것과 **같은 판정**으로 센다 (msd.json 존재가 아니라 cell 등재 여부) —
        # 두 곳이 다른 기준을 쓰면 n 과 β̄ 가 어긋난다.
        _nb = len([s for s in SEEDL if cell.get((lab, T, s))])
        _bt = (f"β̄{bens:.2f}" + ("" if _nb >= 3 else f"(n={_nb}!)")) if bens is not None else "β—"
        tag = (f"{sum(Ds) / len(Ds):.2e} " + _bt
               if Ds else "")
        cells.append(f"{' '.join(marks)} {tag}".ljust(W))
    print(f"     {lab:9s}" + "".join(cells))
print("     (s#✓/✗ = **시드별** 참고용, 판정에 안 쓴다 · β̄ = **시드 MSD 평균 곡선**의 β = 판정량)")
print("     ⚠ β̄(n=k!) 는 시드 k개뿐인 **잠정값** — 3시드 미만은 판정에 쓰지 않는다")
print("     ⚠ 시드 추가 규칙: kb/methodology/beta_gate_seed_policy.md — 정지 규칙을 먼저")
print("        선언하고, 추가한 시드는 **전부** 평균에 넣는다. '통과할 때까지 다시' 는 금지.")

for lab, T, s, ps, pct in live:
    if ps is None:
        print(f"     ▶ 지금 {lab} T{T} s{s} — 착수 직후(md.log 아직 없음)")
    else:
        print(f"     ▶ 지금 {lab} T{T} s{s} — {ps:.1f}/{ARR_TOTAL_PS:.0f} ps ({pct:.0f}%)")

# ── 게이트 요약 — comp1 에서 배운 것: 개수만 보면 못 쓸 숫자를 모으게 된다 ──
# ⚠ 실패 집계도 **온도점 단위(앙상블 β)** 로 한다 — 아레니우스에 들어가는 것이 온도점이지
#   개별 시드가 아니기 때문이다. 시드별 ✓/✗ 마크는 어느 시드가 튀는지 보라는 참고일 뿐.
bad = []
for lab in SYSL:
    for T in (600, 700, 900):
        got = [s for s in SEEDL if cell.get((lab, T, s))]
        if len(got) < len(SEEDL):
            continue                      # 시드가 다 모여야 앙상블 판정을 한다
        be = _ens_beta([_under(os.path.join(ARR, lab, f"T{T}_s{s}"), "msd.json") for s in got])
        if be is not None and not (0.8 <= be <= 1.2):
            bad.append(f"{lab}/T{T}(β̄{be:.2f}, {len(got)}시드)")
if n_done:
    if bad:
        print(f"   ⛔ 온도점 게이트 실패 {len(bad)}건: {', '.join(bad[:6])}"
              + (" …" if len(bad) > 6 else ""))
        print("      → 이 점들은 아레니우스에서 **뺀다**. 창을 옮겨 구제하지 않는다"
              "(comp1 1600 ps 에서 확인).")
    else:
        print("   ✅ 시드가 다 모인 온도점은 전부 앙상블 게이트 통과 "
              "(시드 미완 온도점은 아직 판정 안 함)")
    if mto_seen:
        print("   ★ MTO(다중 시간원점) 감지 — 단일원점 대비 β 산포가 줄어드는지가 이번 판의 관전 포인트")

if n_done >= len(PLAN):
    print("   ▶ 다 끝났다. 500 K 필요 prod 를 이 β 로 정하고 나서 걸 것:")
    print("      python3 tools/ionic/msd_refit_window.py --mto \\")
    print(f"        --glob '{ARR}/*/T*_s*/**/msd.json'")
    print("      tmux new -s arr500 -d 'TEMP_PROD=\"500:<정한값>\" LPSOCL_EXTRA=\"\" \\")
    print("        bash tools/ionic/run_arrhenius_6pt.sh 2>&1 | tee -a ~/logs/arr500.log'")
elif not arr_up and not n_done:
    print("   · 미착수:")
    print("      tmux new -s arr6 -d 'TEMP_PROD=\"700:200 900:200\" \\")
    print("        bash tools/ionic/run_arrhenius_6pt.sh 2>&1 | tee -a ~/logs/arr6.log'")
print(BAR)

# ═══ ④ comp1 셀 확대 사다리 ═══════════════════════════════════════════════
# 왜 이게 ①의 후속인가: ① 이 "시간으로는 못 닫는다"로 끝났고(1600 ps 로 600 K β 0.64→0.37),
#   남은 가설이 **62원자 셀에 Li 24개라 표본이 없다** 하나다. 사다리로 그 가설을 검정한다.
# ⚠ 한 점(2×2×2)만 보면 '올랐다/안 올랐다' 밖에 못 말한다. **단조 증가인지**가 판정이다.
SC = os.path.join(H, "work", "runs", "comp1_supercell")
LADDER = [("2x1x1", 104, 48), ("2x2x1", 208, 96), ("2x2x2", 416, 192)]
SC_SEED = 2
SC_TOTAL_PS = EQ_PS + 200.0
sc_up = "c1sc" in tmux

print("④ comp1 셀 확대 사다리 — ① 의 '남은 수' (시간이 아니라 **이온 수**)")
print("   기준선: 1×1×1 (52원자 · Li 24) 600 K β **0.64** · 1600 ps 로 늘리면 0.37 로 악화")
if not os.path.isdir(SC) and not sc_up:
    print("   · 미착수:  conda activate uma && PY=$(which python3) && mkdir -p ~/logs")
    print("     tmux new -s c1sc -d \"PY=$PY bash ~/Yonghoon-DEM-DFT/tools/ionic/"
          "run_comp1_supercell.sh 2>&1 | tee -a ~/logs/c1sc.log\"")
else:
    print(f"   {'셀':8s} {'원자':>5s} {'Li':>4s} {'상태':>22s} {'β(2-50)':>9s} {'D':>10s}")
    betas = []
    for sc, nat, nli in LADDER:
        d = os.path.join(SC, f"sc{sc}_s{SC_SEED}")
        mj = _under(d, "msd.json")
        b = D = None
        if mj:
            try:
                j = json.load(open(mj)); D = j.get("D_Li_cm2_s")
            except Exception:
                j = {}
            b = beta(mj)
            st = "✅ 완료"
        else:
            lg = _under(d, "md.log")
            ps, _ = md_progress(os.path.dirname(lg)) if lg else (None, None)
            if ps is not None:
                st = f"▶ {ps:.0f}/{SC_TOTAL_PS:.0f} ps ({100*min(1,ps/SC_TOTAL_PS):.0f}%)"
            elif os.path.isdir(d):
                st = "▶ 착수 (UMA 로드)"
            else:
                st = "· 대기"
        if b is not None:
            betas.append((nli, b))
        print(f"   {sc:8s} {nat:5d} {nli:4d} {st:>22s} "
              f"{(f'{b:.2f}' if b is not None else '—'):>9s} "
              f"{(f'{D:.3e}' if D else '—'):>10s}")
    # ── 판정: 기준선(Li 24, β 0.64)을 포함해 단조 증가인가 ──────────────────
    pts = [(24, 0.64)] + sorted(betas)
    if len(betas) >= 2:
        mono = all(pts[i][1] <= pts[i + 1][1] + 0.03 for i in range(len(pts) - 1))
        top = pts[-1]
        print(f"   사다리 β: " + " → ".join(f"Li{n}:{b:.2f}" for n, b in pts))
        if top[1] >= 0.80 and mono:
            print("   ✅ **가설 성립** — 이온 수를 늘리니 β 가 올라 게이트를 넘었다. "
                  "원인은 통계였다. → 800/1000 K 확장 후 comp1 Ea 재산출:")
            print("      TEMPS='600 800 1000' LADDER='2x2x2' "
                  "bash tools/ionic/run_comp1_supercell.sh")
        elif not mono:
            print("   ⚠ 단조가 아니다 — 표본 잡음일 수 있다. 마지막 칸까지 보고 말할 것.")
        else:
            print(f"   ⛔ **가설 기각 쪽** — Li {top[0]}개에서도 β {top[1]:.2f} 로 0.80 미달. "
                  "셀 확대도 답이 아니다.")
            print("      → MSD 경로를 접고 **홉 통계**로 간다 (Fickian MSD 가 필요 없다):")
            print(f"         python3 tools/ionic/hops_per_ion.py --glob '{SC}/*/**/traj.xyz'")
            print("      → open_items #1 에 그렇게 적고 comp1 Ea 는 인용 보류 유지.")
    elif betas:
        print("   · 아직 한 칸 — 사다리는 **두 칸 이상**이라야 경향을 말할 수 있다.")
print(BAR)

# ═══ 브랜치 상기 ═════════════════════════════════════════════════════════
br = sh("git -C ~/Yonghoon-DEM-DFT branch --show-current").strip()
if br and br != "claude/friendly-meitner-lldvar":
    print(f"⚠ kgy 브랜치 = {br} (우리 브랜치 아님). git pull 로는 우리 코드가 안 온다:")
    print("   git fetch origin claude/friendly-meitner-lldvar && \\")
    print("   git checkout FETCH_HEAD -- <필요한 경로>")
