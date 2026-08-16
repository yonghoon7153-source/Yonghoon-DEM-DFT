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
import sys
from datetime import datetime

H = os.path.expanduser("~")
NOW = datetime.now()
BAR = "-" * 68
#: watch_all.py 의 --only 관례를 따른다 (단독 화면)
ONLY = ""
for _i, _a in enumerate(sys.argv):
    if _a == "--only" and _i + 1 < len(sys.argv):
        ONLY = sys.argv[_i + 1]
    elif _a.startswith("--only="):
        ONLY = _a.split("=", 1)[1]
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


# ═══ ⑥ lpsocl 600 K × 800 ps — (B) vs (C) 판정 런 ═══════════════════════════
#   2026-08-12. 홉 통계가 (C) 느린 전이/통계 부족 쪽으로 기울였고, 그 예측을 검정한다.
#   실측 홉 7.3/이온(200 ps) → ~29/이온(800 ps) 로 문턱 10 을 넘는다.
#   ★ 정지 규칙을 **미리** 박아 둔다 — 결과를 보고 기준을 고치지 않기 위해서다
#     (kb/methodology/beta_gate_seed_policy.md: '통과할 때까지 다시' 금지).
LONG = os.environ.get("LONGDIR") or os.path.join(H, "work", "runs", "lpsocl_600_long")
def _newest_long_log():
    """가장 최근 ~/logs/lpsocl*.log — 시드 추가 런이 새 로그를 쓰기 때문 (2026-08-14).
    옛 로그를 계속 읽으면 '141분 전 갱신' 같은 죽은 정보가 화면에 남는다."""
    c = sorted(glob.glob(os.path.join(H, "logs", "lpsocl*.log")),
               key=lambda f: os.path.getmtime(f), reverse=True)
    return c[0] if c else os.path.join(H, "logs", "lpsocl800.log")
LONG_LOG = os.environ.get("LONGLOG") or _newest_long_log()
LONG_TARGET_PS = 800.0
LONG_HOURS_PER_200PS = 3.42          # 실측 (arrhenius_6pt 21런)
BETA_PASS, BETA_FAIL = 0.80, 0.75    # 사이면 경계 → 시드 추가


def long_verdict(b):
    """선언한 정지 규칙. 이 함수가 판정의 유일한 출처다."""
    if b is None:
        return "—", "아직 msd.json 없음"
    if b >= BETA_PASS:
        return "✅ (C) 확정", ("통계 부족이었다 — lpsocl 600 K 를 아레니우스에 **복귀**시킨다. "
                             "처방은 창/시간 연장이 맞았다.")
    if b < BETA_FAIL:
        return "⛔ (B) 확정", ("홉이 4배로 늘어도 안 살아났다 — 진짜 멱함수다. "
                             "이 점은 D 인용 금지, 아레니우스에서 뺀다.")
    # ⚠ 2026-08-14 — 처방이 시드 수에 따라 갈린다. 3시드 전이면 시드 추가,
    #   3시드를 채우고도 경계면 **더 넣지 않고 판정 불가로 종결**한다
    #   (6시드로도 표준오차 0.06→0.04 라 0.75/0.80 을 못 가른다).
    #   선언: kb/methodology/beta_gate_seed_policy.md
    return "△ 경계", (f"{BETA_FAIL}–{BETA_PASS} 사이 — 3시드 전이면 시드 추가(s3·s4), "
                     f"3시드를 채우고도 경계면 **판정 불가로 종결**하고 그 점을 "
                     f"아레니우스에서 뺀 채 '미해결' 로 보고한다. 시드를 더 넣지 않는다.")


def section_long():
    print("⑥ lpsocl 600 K × 800 ps — (B) 진짜 멱함수 vs (C) 느린 전이 판정")
    # ⚠ 2026-08-14 — 세션 이름을 "lpsocl800" 으로 고정하면 시드 추가 런(lpsocl_s34)을
    #   못 본다. 실제로 s3 가 도는데 "완료·tmux 없음" 으로 찍혔다. 접두사로 찾는다.
    up = any(ln.split(":")[0].startswith("lpsocl") for ln in sh("tmux ls").splitlines() if ln.strip())
    # ⚠ 러너 쉘이 살아 있는 건 **python 이 돈다는 증거가 아니다**. 드라이버를 직접 본다.
    nproc = len([x for x in sh("pgrep -f '[r]un_arrhenius_6pt.sh'").split() if x])
    ndrv = len([x for x in sh("pgrep -f '[d]isorder_ensemble_diffusion.py'").split() if x])
    gpu = sh("nvidia-smi --query-gpu=utilization.gpu,memory.used "
             "--format=csv,noheader,nounits").strip().splitlines()
    gpu = gpu[0] if gpu else "?"
    # ⚠ 2026-08-14 — 단일 시드(s2)만 보던 것을 **전 시드**로 넓힌다. β 0.799 가 문턱
    #   0.80 바로 아래라 한 시드로 판정하면 뒤집힌다 (2026-07-09 1.33× 철회의 재발 방지).
    seed_mj = {}
    for d in sorted(glob.glob(os.path.join(LONG, "lpsocl", "T600_s*"))):
        sd = os.path.basename(d).split("_s")[-1]
        f = next(iter(sorted(glob.glob(os.path.join(d, "**", "msd.json"), recursive=True))), None)
        if f:
            seed_mj[sd] = f
    mj = seed_mj.get("2") or (next(iter(seed_mj.values()), None))
    if not os.path.isdir(LONG) and not up:
        print("   · 미착수. 걸려면:")
        # ⚠ ONLY 는 **위치인자**로 준다 — 환경변수만 주면 옛 판에서 all 로 돌았다 (2026-08-14).
        print("     tmux new -s lpsocl800 -d \""
              "OUTROOT=$HOME/work/runs/lpsocl_600_long \\")
        print("       SEEDS=2 TEMP_PROD='' LPSOCL_EXTRA='600:800' \\")
        # ⚠ 계 이름은 **위치인자** — 환경변수 ONLY 만 주면 옛 판에서 all 로 돌았다 (2026-08-14)
        print("       bash tools/ionic/run_arrhenius_6pt.sh lpsocl 2>&1 | tee -a ~/logs/lpsocl800.log\"")
        return
    # 시작 시각 = 러너의 ▶ 줄
    t0, tail = None, []
    if os.path.isfile(LONG_LOG):
        try:
            lines = open(LONG_LOG, errors="ignore").read().splitlines()
        except OSError:
            lines = []
        tail = lines[-3:]
        # ▶ 줄을 먼저 찾고, 없으면 **로그의 첫 타임스탬프**로 후퇴한다.
        #   (러너 출력이 버퍼링되면 ▶ 가 늦게 나타난다 — 그때 "시작 ?" 로 비면
        #    경과·잔여를 못 보여 준다. 근사라도 있는 게 낫고, 어느 쪽인지 표시한다.)
        for ln in lines:
            if "prod=800" in ln and "▶" in ln:
                m = re.search(r"\[([\d-]+\s+)?(\d{2}:\d{2}:\d{2})\]", ln)
                if m:
                    t0 = m.group(2)
        if t0 is None:
            for ln in lines:
                m = re.search(r"\[([\d-]+\s+)?(\d{2}:\d{2}:\d{2})\]", ln)
                if m:
                    t0 = m.group(2) + "~"      # ~ = 로그 시작 시각(근사)
                    break
        if t0 is None and os.path.isfile(LONG_LOG):
            t0 = datetime.fromtimestamp(
                os.path.getmtime(LONG_LOG)).strftime("%H:%M:%S") + "?"
    el = os.path.getmtime(LONG_LOG) if os.path.isfile(LONG_LOG) else None
    age = (datetime.now().timestamp() - el) / 60.0 if el else None
    st = "✅ 완료" if mj else ("▶ 진행" if (up or nproc) else "⛔ 죽음/미착수")
    print(f"   상태 {st} · tmux {'있음' if up else '없음'} · 러너 {nproc} · "
          f"**드라이버 {ndrv}** · GPU {gpu} · 시작 {t0 or '?'} · "
          f"예상 {LONG_TARGET_PS / 200 * LONG_HOURS_PER_200PS:.1f} h")
    if t0 and not mj:
        try:
            hh, mm, ss = (int(x) for x in t0.rstrip("~?").split(":"))
            now = datetime.now()
            el_h = ((now.hour - hh) * 3600 + (now.minute - mm) * 60
                    + (now.second - ss)) / 3600.0
            if el_h < 0:
                el_h += 24
            tgt = LONG_TARGET_PS / 200 * LONG_HOURS_PER_200PS
            print(f"   경과 {el_h:.1f} h / {tgt:.1f} h  ({100 * el_h / tgt:.0f}%) · "
                  f"남은 {max(0.0, tgt - el_h):.1f} h")
        except ValueError:
            pass
    if not mj and ndrv == 0:
        print("   ⛔ 드라이버 python 이 없다 — 쉘만 살아 있고 계산은 안 돈다")
    # MD 는 진행 로그를 거의 안 찍는다 — 출력 폴더가 크는지가 더 나은 생존 신호다
    tot = 0
    for r2, _d, fs2 in os.walk(os.path.join(LONG, "lpsocl", "T600_s2")):
        for f2 in fs2:
            try:
                tot += os.path.getsize(os.path.join(r2, f2))
            except OSError:
                pass
    print(f"   출력 {tot / 1e6:.1f} MB (traj 는 종료 시 한 번에 쓰인다 — 0 이어도 정상)")
    if age is not None:
        # ⚠ 이 MD 드라이버는 진행 로그를 거의 안 찍는다 — 로그 침묵만으로 경고하면
        #   늑대소년이 된다(실측 228분 침묵인데 GPU 94%로 정상 실행 중이었다).
        #   드라이버·GPU 가 살아 있으면 침묵은 정상이라고 말한다.
        try:
            gutil = int(str(gpu).split(",")[0].strip())
        except (ValueError, IndexError):
            gutil = None
        alive = ndrv > 0 and (gutil is None or gutil > 10)
        note = ("   (드라이버·GPU 살아 있음 — 이 드라이버는 원래 진행 로그를 안 찍는다)"
                if alive else
                "   ⚠ 30분 넘게 조용한데 드라이버/GPU 도 놀고 있다 — 죽었는지 확인")
        print(f"   로그 마지막 갱신 {age:.0f}분 전"
              + (note if age > 30 and not mj else ""))
    b = None
    if mj:
        try:
            j = json.load(open(mj))
            b = _beta_series(j.get("times_ps_mto") or j.get("times_ps"),
                             j.get("msd_Li_A2_mto") or j.get("msd_Li_A2"))
        except (OSError, ValueError, KeyError):
            print("   ⛔ msd.json 손상")
    # 시드별 β 를 전부 읽어 중앙값으로 판정한다 (단일 시드 판정 금지)
    betas = {}
    for sd, f in sorted(seed_mj.items()):
        try:
            jj = json.load(open(f))
            bb = _beta_series(jj.get("times_ps_mto") or jj.get("times_ps"),
                              jj.get("msd_Li_A2_mto") or jj.get("msd_Li_A2"))
            if bb is not None:
                betas[sd] = bb
        except (OSError, ValueError, KeyError):
            print(f"   ⛔ s{sd} msd.json 손상")
    if betas:
        print("   β(창 2–50) 시드별: "
              + " · ".join(f"s{k} {v:.3f}" for k, v in sorted(betas.items())))
    # ⚠⚠ 여기 숫자는 **진단**이다. 판정량은 시드별 β 가 아니라
    #   **시드 앙상블 평균곡선(MTO)에서 잰 β̄** 다 (규약: requests §4-2).
    #   순서를 바꾸면 값이 달라진다(Jensen) — watch 는 msd.json 을 개별로만 읽으므로
    #   판정을 낼 수 없다. 선언 문서: kb/methodology/beta_gate_seed_policy.md
    n = len(betas)
    print(f"   ⚠ 위는 **시드별 진단값**이다 — 판정량 아님 (규약 = 시드 평균곡선의 β̄).")
    if n < 3:
        print(f"   판정: **△ 시드 부족 ({n}/3)** — s3·s4 가 끝날 때까지 (B)/(C) 를 말하지 않는다.")
    else:
        print(f"   판정: 시드 {n}개 모임 → **아래 스캔을 돌려 β̄ 로 판정할 것** (watch 가 대신 못 한다).")
    print(f"   선언한 규칙 (2026-08-14, 결과 보기 전 선언):")
    print(f"     β̄ ≥ {BETA_PASS} → (C) 느린 전이 · 600 K 아레니우스 복귀")
    print(f"     β̄ < {BETA_FAIL} → (B) 진짜 멱함수 · 그 점 제거")
    print(f"     {BETA_FAIL}–{BETA_PASS} → **판정 불가로 종결. 시드 더 넣지 않는다** (6시드로도 SE 0.04 라 부족)")
    stray = [os.path.basename(d) for d in
             sorted(glob.glob(os.path.join(LONG, "*")))
             if os.path.isdir(d) and os.path.basename(d) != "lpsocl"]
    if stray:
        # ⚠ 500/700/900 은 **1저자 요청 #1(6점 아레니우스)** 의 정당한 축이다 — 쓰레기가 아니다.
        #   다만 이 폴더의 것은 2026-08-12 런이 ONLY/TEMP_PROD 버그로 **딸려 돌린 중복**이고,
        #   700/900 은 2026-08-11 에 이미 21런 돌아 결과가 나와 있다 (8/21 게이트 탈락).
        #   그리고 500 K 는 §9-6 이 "예상 실패에 30시간" 이라며 **명시적으로 보류**한 온도다.
        print(f"   ⚠ 이 폴더에 lpsocl 외 산출물: {' '.join(stray)}")
        print("     500/700/900 은 요청 #1(6점 아레니우스)의 축이지만, 700/900 은 2026-08-11"
              " 21런으로 이미 있고(8/21 탈락)")
        print("     500 K 는 kb/reports/paper_first_author_requests_2026_08.md §9-6 이"
              " **보류 결정**한 온도다 — 여기 것은 버그로 딸려온 중복.")
    if True:
        print("   ★ 판정은 이 명령으로만 (watch 숫자로 판정 금지):")
        print(f"     python3 tools/ionic/msd_diffusive_check.py --scan --average --mto \\")
        # ⚠ `*/T*_s*` 는 modelc·b2o3 까지 빨아들인다 — 판정 대상은 lpsocl 600 K 뿐이다
        print(f"       --glob '{LONG}/lpsocl/T600_s*/**/msd.json'")
    for ln in tail:
        print(f"   │ {ln[:96]}")


def selftest_long():
    """선언한 정지 규칙의 시험. 여기 버그는 **과학적 판정을 조용히 바꾼다**."""
    ok = True

    def chk(c, m):
        nonlocal ok
        print(("  ✓ " if c else "  ✗ ") + m)
        ok &= bool(c)

    cases = [(0.90, "(C)"), (0.80, "(C)"), (0.799, "경계"), (0.76, "경계"),
             (0.75, "경계"), (0.749, "(B)"), (0.61, "(B)")]
    for b, want in cases:
        v, _ = long_verdict(b)
        chk(want in v, f"β={b} → {v}  (기대 {want})")
    chk(long_verdict(None)[0] == "—", "msd.json 없음 → 판정 보류")
    # 음성: 경계 구간이 비면 안 된다 (둘 다 안 걸리는 β 가 없어야 한다)
    holes = [round(x / 1000, 3) for x in range(600, 1000)
             if long_verdict(x / 1000)[0] == "—"]
    chk(not holes, f"0.60~1.00 에 판정 구멍 없음 (구멍 {holes[:3]})")
    # 음성: PASS 와 FAIL 이 뒤집혀 있으면 안 된다
    chk(BETA_FAIL < BETA_PASS, f"문턱 순서 {BETA_FAIL} < {BETA_PASS}")
    # ★ 2026-08-14 추가 — **시드 수 규칙**. 3시드 미만이면 (B)/(C) 를 말하면 안 된다.
    #   화면 로직과 같은 판정을 여기서 재현한다 (0.799 가 문턱 바로 아래라 실전 위험).
    import statistics as _st
    def _decide(bs):
        """시드별 β dict → (판정, 사용한 β). 화면 로직의 축약."""
        if len(bs) >= 3:
            return long_verdict(_st.median(bs.values()))[0], _st.median(bs.values())
        return "△ 시드 부족", (next(iter(bs.values())) if bs else None)
    chk(_decide({"2": 0.799})[0] == "△ 시드 부족", "단일 시드 → 판정 보류")
    chk(_decide({"2": 0.799, "3": 0.81})[0] == "△ 시드 부족", "2시드도 보류")
    # 중앙값이라 한 시드가 튀어도 안 뒤집힌다
    # ★ 문턱 자체의 시험 (판정량이 무엇이든 이 매핑은 같아야 한다)
    chk(long_verdict(0.80)[0].startswith("✅"), "β̄ 0.80 → (C) (경계 포함)")
    chk(long_verdict(0.799)[0].startswith("△"), "β̄ 0.799 → 경계")
    chk(long_verdict(0.75)[0].startswith("△"), "β̄ 0.75 → 경계 (하한 포함)")
    chk(long_verdict(0.749)[0].startswith("⛔"), "β̄ 0.749 → (B)")
    # ★ 경계면 **시드를 더 넣지 않는다** — 선언 문서의 규칙이 처방에 반영됐는지
    chk("시드 추가" in long_verdict(0.78)[1],
        f"경계 처방에 시드 추가가 적혀 있다 ({long_verdict(0.78)[1][:30]})")
    # ★ 2026-08-14 — 화면이 옛 런을 보던 3건의 회귀 시험
    import tempfile as _tf
    _td = _tf.mkdtemp(prefix="watch_long_st_")
    _lg = os.path.join(_td, "logs"); os.makedirs(_lg)
    for nm, mt in (("lpsocl800.log", 1000), ("lpsocl_s34.log", 2000)):
        f = os.path.join(_lg, nm); open(f, "w").write("x\n"); os.utime(f, (mt, mt))
    _newest = sorted(glob.glob(os.path.join(_lg, "lpsocl*.log")),
                     key=lambda f: os.path.getmtime(f), reverse=True)[0]
    chk(os.path.basename(_newest) == "lpsocl_s34.log",
        f"가장 최근 lpsocl*.log 를 고른다 ({os.path.basename(_newest)})")
    _sessions = "lpsocl_s34: 1 windows\nqegpu: 1 windows"
    chk(any(l.split(":")[0].startswith("lpsocl") for l in _sessions.splitlines()),
        "세션 이름이 lpsocl800 이 아니어도 잡는다")
    chk(not any(l.split(":")[0].startswith("lpsocl") for l in "qegpu: 1 windows".splitlines()),
        "lpsocl 세션이 없으면 없다고 한다 (오탐 없음)")
    import shutil as _sh; _sh.rmtree(_td, ignore_errors=True)
    chk("복귀" in long_verdict(0.9)[1] and "뺀다" in long_verdict(0.7)[1],
        "처방이 판정과 반대로 붙지 않았다")
    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1

# ═══ ⑦ lpsocl 3×3×1 셀 확대 — β 실패가 상자 탓인지 시험 ═══════════════════════
#  근거 (2026-08-16 실측): 원본 셀의 **최소 수직 폭**이 5.672 Å 이라
#  무상관 한계 (d/2)² = 8.04 Å² 인데, 창끝 MSD 가 25.8 Å² 로 **3.21배 초과**다.
#  이온이 짧은 방향에서 상자를 세 번 가로질렀다는 뜻이고, 그러면 변위가 자기
#  주기이미지와 상관돼 늦은 시간 MSD 증가가 눌린다. 관측 3증상이 한꺼번에 설명된다:
#    · β 가 1 로 안 가고 0.87 에서 포화 (창 100–200)
#    · 절편 c 가 창 따라 2.17 → 21.15 Å² (10배)
#    · 시드를 늘려도 안 고쳐짐 — 모든 시드가 같은 상자
#  ⚠ 한계는 |a|(6.95 Å)가 아니라 **수직 폭**이다. 삼방정계라 1.2배 차이 난다.
CELL = os.environ.get("CELLDIR") or os.path.join(H, "work", "runs", "arrhenius_6pt", "lpsocl_3x3x1")
CELL_LOG = os.environ.get("CELLLOG") or os.path.join(H, "logs", "lpsocl_3x3x1.log")


def section_cell():
    print("⑦ lpsocl 3×3×1 셀 확대 — β 실패가 상자 탓인지 시험 (558원자 · 3시드 · 200 ps)")
    up = any(ln.split(":")[0] == "lp331" for ln in sh("tmux ls").splitlines() if ln.strip())
    ndrv = len([x for x in sh("pgrep -f '[d]isorder_ensemble_diffusion.py'").split() if x])
    gpu = sh("nvidia-smi --query-gpu=utilization.gpu,memory.used "
             "--format=csv,noheader,nounits").strip().splitlines()
    print(f"   유한크기: 원본 최소 수직폭 5.67 Å → (d/2)² 8.04 Å² · MSD 25.8 → **3.21× 초과**")
    print(f"             3×3×1  최소 수직폭 17.02 Å → (d/2)² 72.4 Å² · MSD 25.8 → **0.36× 여유**")
    seeds = {}
    for d in sorted(glob.glob(os.path.join(CELL, "T600_s*"))):
        sd = os.path.basename(d).split("_s")[-1]
        f = next(iter(sorted(glob.glob(os.path.join(d, "**", "msd.json"), recursive=True))), None)
        if f:
            seeds[sd] = f
    if not os.path.isdir(CELL) and not up:
        print("   · 미착수. 걸려면:")
        print("     tmux new -d -s lp331 \"cd ~/Yonghoon-DEM-DFT && ONLY=lpsocl_3x3x1 \\")
        print("       EXTRA_SYS='lpsocl_3x3x1|db/structures/lpsocl_relaxV0_3x3x1.xyz' \\")
        print("       TEMP_PROD='600:200' LPSOCL_EXTRA='' SEEDS='2 3 4' \\")
        print("       bash tools/ionic/run_arrhenius_6pt.sh 2>&1 | tee -a ~/logs/lpsocl_3x3x1.log\"")
        return
    st = "▶ 진행 중" if (up or ndrv) else ("✅ 완료" if seeds else "⚠ 시작 안 됨")
    print(f"   상태 {st} · tmux lp331 {'있음' if up else '없음'} · 드라이버 {ndrv} · GPU {gpu[0] if gpu else '?'}")
    if os.path.isfile(CELL_LOG):
        age = (NOW - datetime.fromtimestamp(os.path.getmtime(CELL_LOG))).total_seconds() / 60
        print(f"   로그 마지막 갱신 {age:.0f}분 전  ({CELL_LOG})")
        try:
            for ln in open(CELL_LOG, errors="ignore").read().splitlines()[-2:]:
                print(f"   │ {ln[:100]}")
        except OSError:
            pass
    if seeds:
        bs = []
        for sd in sorted(seeds):
            b = beta(seeds[sd])
            bs.append((sd, b))
        print("   β(창 2–50) 시드별: " + " · ".join(
            f"s{sd} {('%.3f' % b) if b is not None else '—'}" for sd, b in bs))
        print("   ⚠ 위는 **시드별 진단값**이다 — 판정량은 시드 평균곡선의 β̄ (규약).")
    print(f"   ★ 판정 (시드 3개 모인 뒤):")
    print(f"     python3 tools/ionic/msd_diffusive_check.py --scan --average --mto \\")
    print(f"       --glob '{CELL}/T600_s*/**/msd.json'")
    print("   해석: 작은 셀 β̄ = 0.77 (3시드 평균, 2026-08-16 확정)")
    print("     · β̄ ≥ 0.80  → **상자가 원인 확정**. 600 K 복귀 + modelc·b2o3 도 같은 셀로 재계산해야 비교 성립")
    print("     · β̄ 여전 0.77 급 → 상자가 아니다. 진짜 sub-diffusion — 그 점 제거하고 재적합")
    print("   ⚠ modelc(β600 0.868)·b2o3(0.806)도 **같은 5.67 Å 상자**다. D 가 작아 덜 걸렸을 뿐일 수 있어")
    print("     lpsocl 만 큰 셀로 재면 '+90 meV' 가 화학 차이인지 셀 차이인지 못 가른다.")


if "--selftest" in sys.argv:
    sys.exit(selftest_long())

if ONLY == "long":
    section_long()
    sys.exit(0)

if ONLY == "cell":
    section_cell()
    sys.exit(0)


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
    # ★★ 2026-08-11 판정 — 여기서 500 K 를 안내하던 문구를 **철회**한다.
    #   ① 21런 전수 게이트: 8/21 탈락 (lpsocl 9런 중 5런). 700/900 이 이미 뚫렸다.
    #   ② 그 탈락이 잡음이 아님을 귀무분포로 확인 (beta_null_test.py):
    #      이상 브라운 운동은 창 2-50 에서 β 1.006, 0.8 미만이 1.0% 뿐.
    #   ③ 500 K@400 ps 는 홉 수(∝D·t) 로 600 K@200 ps 의 0.66배 — 그 600 K 가 이미 탈락한 계다.
    #   ④ --mto 재적합은 **돌아가지 않는다**: 21런이 옛 드라이버로 돌아 MTO 가 없고
    #      프레임(--save_traj)도 없어 소급 계산이 불가하다.
    print("   ⛔ **500 K 를 걸지 않는다 (2026-08-11 판정).** 700/900 에서 이미 8/21 탈락이다:")
    print("      · lpsocl 5/9 · modelc 2/6 · b2o3 1/6  (창 2-50, β<0.80)")
    print("      · 잡음 아님을 확인: python3 tools/ionic/beta_null_test.py --n_li 27 "
          "--n_frames 2001 --dt_ps 0.1")
    print("        → 이상 브라운 운동도 창 2-50 에서 β 1.006, 0.8 미만은 1.0% 뿐")
    print("      · 500 K@400 ps 는 홉 수로 600 K@200 ps 의 0.66배 — 더 어렵다")
    print("      ⚠ --mto 재적합도 못 한다: 21런이 옛 드라이버(MTO 이전 판)로 돌았고")
    print("        --save_traj 도 없어 프레임이 없다. 소급 계산 불가.")
    print("   ▶ 대신 ④ 셀 확대 사다리를 본다 — 시간이 아니라 이온 수가 남은 축이다.")
    print("      게이트 전수 재확인:  python3 tools/ionic/msd_diffusive_check.py --scan \\")
    print(f"        --glob '{ARR}/*/T*_s*/**/msd.json'")
elif not arr_up and not n_done:
    print("   · 미착수:")
    print("      tmux new -s arr6 -d 'TEMP_PROD=\"700:200 900:200\" \\")
    print("        bash tools/ionic/run_arrhenius_6pt.sh 2>&1 | tee -a ~/logs/arr6.log'")
print(BAR)

# ═══ ⑤ MTO 파일럿 — β 게이트 자체를 검정한다 ═══════════════════════════════
# 왜: 2026-08-11 창 추세 판정에서 **게이트가 실제 진단과 어긋나는 사례**가 나왔다.
#   modelc/700 β̄0.76 (탈락) → 실제 케이지 절편(D 인용 가능) · b2o3/700 β̄0.85 (통과)
#   → 실제 sub-diffusion(D 금지). 7 온도점 중 3개는 꼬리 잡음으로 **판별 불가**다.
#   그 3개를 가르려면 다중 시간원점(MTO)이 필요한데 21런엔 프레임이 없어 소급 불가 →
#   3계 × 700 K × 1시드만 다시 돈다. 이번엔 MTO + --save_traj 가 들어간다.
MTO = os.path.join(H, "work", "runs", "mto_pilot")
MTO_PLAN = [(lab, 700, 2) for lab in SYSL]
mto_up = "mtopilot" in tmux
print("⑤ MTO 파일럿 — **β 게이트 자체를 검정한다** (3계 × 700 K × 1시드)")
print("   판별 불가 3점(b2o3/900 · lpsocl/700 · lpsocl/900) 해소 + MTO 산포 실측 + 프레임 확보")
if not os.path.isdir(MTO) and not mto_up:
    print("   · 미착수:  tmux new -s mtopilot -d \"OUTROOT=$HOME/work/runs/mto_pilot "
          "SEEDS=2 TEMP_PROD='700:200' bash tools/ionic/run_arrhenius_6pt.sh "
          "2>&1 | tee -a ~/logs/mtopilot.log\"")
else:
    n_ok = 0
    print(f"   {'계':10s} {'상태':>22s} {'β(STO)':>8s} {'β(MTO)':>8s} {'traj':>6s}")
    for lab, T, sd in MTO_PLAN:
        d = os.path.join(MTO, lab, f"T{T}_s{sd}")
        mj = _under(d, "msd.json")
        b_sto = b_mto = None
        traj = "—"
        if mj:
            try:
                j = json.load(open(mj))
            except Exception:
                j = {}
            b_sto = beta(mj)
            if "msd_Li_A2_mto" in j:
                b_mto = _beta_series(j.get("times_ps_mto") or j.get("times_ps"),
                                     j["msd_Li_A2_mto"])
            tj = _under(d, "traj.xyz")
            traj = "✔" if tj else "⛔"
            st = "✅ 완료" + ("" if b_mto is not None else "  ⛔ MTO 없음!")
            n_ok += 1
        else:
            lg = _under(d, "md.log")
            ps, _ = md_progress(os.path.dirname(lg)) if lg else (None, None)
            st = (f"▶ {ps:.0f}/205 ps ({100 * min(1, ps / 205):.0f}%)" if ps is not None
                  else ("▶ 착수" if os.path.isdir(d) else "· 대기"))
        print(f"   {lab:10s} {st:>22s} "
              f"{(f'{b_sto:.3f}' if b_sto is not None else '—'):>8s} "
              f"{(f'{b_mto:.3f}' if b_mto is not None else '—'):>8s} {traj:>6s}")
    if n_ok >= len(MTO_PLAN):
        print("   ▶ 다 끝났다. 추세 판정을 MTO 곡선으로 다시:")
        print(f"      python3 tools/ionic/msd_diffusive_check.py --scan --average \\")
        print(f"        --glob '{MTO}/*/T*_s*/**/msd.json'")
        print("      · β(MTO) 가 β(STO) 와 **거의 같으면** → 게이트 탈락은 잡음이 아니었다")
        print("      · 크게 다르면 → 단일원점 추정이 문제였다. 21런 전체를 재판정해야 한다")
        print("      · 어느 쪽이든 traj 가 남았으니 홉 통계로 기구를 분해할 수 있다:")
        # ⚠ hops_per_ion.py 는 **해석적 예측기**(n_hop=6Dt/d²)라 궤적을 안 읽는다.
        #   궤적에서 기구를 보는 건 aimd_jump_stats.py 다 (van Hove + 케이지간 홉).
        print(f"        T=$(ls -d {MTO}/lpsocl/T600_s2 2>/dev/null); "
              f"f=$(find $T -name traj.xyz | head -1)")
        print(f"        python3 tools/ionic/aimd_jump_stats.py --traj $f \\")
        print(f"            --label lpsocl_T600_s2 --out_dir {MTO}/_jumpstats")
        print(f"        # 통계 부족 여부는 궤적 없이도 예측된다:")
        print(f"        python3 tools/ionic/hops_per_ion.py --prod_ps 200")
    print("   ⚠ traj 열이 ⛔ 면 --save_traj 가 안 걸린 것 — 러너를 다시 받을 것")
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

print("④ comp1 셀 확대 사다리 — ⚠ **⑤ 뒤로 보류** (2026-08-11)")
print("   이유: 케이지 절편 c 는 이온 수를 늘려도 안 줄어든다(진동 진폭이 정한다).")
print("   사다리가 줄이는 건 β 의 **산포**뿐인데, 지금 문제는 산포가 아니라 β 라는 지표 자체다.")
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
    # ★★ 2026-08-11 판정 규칙 **전면 교체** (자체검토 P1-4 + Codex 재리뷰).
    #   옛 규칙(칸별 +0.03 허용 단조성)은 실제로 돌려 보니 이렇게 틀렸다:
    #     0.64 → 0.90 → 0.88 → 0.86 (계속 감소)  → "가설 성립" ⛔ 거짓
    #     0.64 → 0.70 → 0.75 → 0.79 (교과서 단조) → "가설 기각" ⛔ 거짓
    #   더 근본적으로 **β 의 중심은 이온 수에 안 움직인다** — 어떤 생성모형에서도.
    #   N 은 분산만 줄인다 (실측: sd 0.090 → 0.032, 정확히 1/√8).
    #   ⇒ 판정량을 "β 가 올라갔나" 에서 **"산포가 줄었나 · 중앙값이 어디에 머무나"** 로 바꾼다.
    if betas:
        import statistics as _st
        by_sc = {}
        for nli, b in betas:
            by_sc.setdefault(nli, []).append(b)
        print(f"   {'Li':>4s} {'n시드':>5s} {'β 중앙값':>9s} {'β sd':>7s}  해석")
        for nli in sorted(by_sc):
            v = by_sc[nli]
            sd = _st.stdev(v) if len(v) > 1 else float("nan")
            print(f"   {nli:4d} {len(v):5d} {_st.median(v):9.3f} "
                  + (f"{sd:7.3f}" if len(v) > 1 else "      —")
                  + ("  (시드 1개 — 산포를 못 잰다)" if len(v) < 2 else ""))
        ks = sorted(by_sc)
        if len(ks) >= 2 and all(len(by_sc[k]) >= 3 for k in (ks[0], ks[-1])):
            m0, m1 = _st.median(by_sc[ks[0]]), _st.median(by_sc[ks[-1]])
            s0, s1 = _st.stdev(by_sc[ks[0]]), _st.stdev(by_sc[ks[-1]])
            sem = (s0 ** 2 / len(by_sc[ks[0]]) + s1 ** 2 / len(by_sc[ks[-1]])) ** 0.5
            print(f"   Δ중앙값 {m1 - m0:+.3f} ± {sem:.3f} (양 끝 Li {ks[0]} → {ks[-1]}) · "
                  f"sd {s0:.3f} → {s1:.3f}")
            shrink = s1 / s0 if s0 > 0 else float("nan")
            print(f"   sd 축소 {shrink:.2f}배 (이상적 독립 Li 면 √({ks[0]}/{ks[-1]}) = "
                  f"{(ks[0] / ks[-1]) ** 0.5:.2f}배)")
            if m1 >= 0.80 and abs(m1 - m0) > 2 * sem:
                print("   ✅ 큰 셀에서 β 가 게이트를 넘고 이동이 유의하다 → "
                      "finite-size/sampling 효과 지지. comp1 Ea 재산출로.")
            elif m1 < 0.80 and shrink < 1.0:
                print("   ⚠ **중앙값은 0.80 아래에 머물고 산포만 줄었다.**")
                print("      ⛔ 이건 '셀 확대 실패' 가 아니라 **non-Fickian 을 더 정밀하게 잰 것**이다.")
                print("      → 다음은 MSD 가 아니라 기구 분해:  --scan 의 c 행 · hops_per_ion.py")
            elif abs(m1 - m0) > 2 * sem:
                print("   ⚠ 중앙값이 불확실도를 넘어 이동했다 → 진짜 유한크기/형상 물리이거나 추정기 편향.")
            else:
                print("   · 아직 갈리지 않았다 (Δ가 표준오차 안) — 시드를 늘리거나 양 끝을 채울 것.")
        else:
            print("   · 판정하려면 **양 끝 칸에 각각 3시드 이상** 필요하다 "
                  "(시드 sd ≈ 0.107 · 기대 신호 0.16 — 같은 크기다).")
        print("   ⛔ **β 단조성으로 판정하지 않는다** — 어떤 모형도 그걸 예측하지 않는다.")
    print(BAR)

# ═══ 브랜치 상기 ═════════════════════════════════════════════════════════
br = sh("git -C ~/Yonghoon-DEM-DFT branch --show-current").strip()
if br and br != "claude/friendly-meitner-lldvar":
    print(f"⚠ kgy 브랜치 = {br} (우리 브랜치 아님). git pull 로는 우리 코드가 안 온다:")
    print("   git fetch origin claude/friendly-meitner-lldvar && \\")
    print("   git checkout FETCH_HEAD -- <필요한 경로>")

if ONLY == "":
    print(BAR)
    section_long()
    print(BAR)
    section_cell()
