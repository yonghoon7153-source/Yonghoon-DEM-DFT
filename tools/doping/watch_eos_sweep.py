#!/usr/bin/env python3
"""watch_eos_sweep.py — EOS 조건 스윕 한 화면 (cascade 파일럿 §4b).

    watch -n 120 python3 tools/doping/watch_eos_sweep.py
    python3 tools/doping/watch_eos_sweep.py --glob 'runs/cascade_pilot/fix_*' --log /tmp/eos_fix.log

왜 bash 가 아니라 python 인가
  `watch_all.py` 와 같은 이유다 — JSON 을 grep 으로 파면 중첩 구조에서 **다른 블록의
  첫 매치**를 집어 조용히 틀린 값을 띄운다 (실측: 프레임 중앙값 대신 쌍 중앙값).

무엇을 보나
  ① 조건별 진행 (몇/5 구조) · 지금 도는 조건과 경과
  ② 구조별 **수렴 n/m 과 최대 잔여힘** ← 회신 BQ P0-1. 이게 없으면 `maxdE` 가
     *다른 골짜기*인지 *그냥 덜 풀린 것*인지 못 가른다
  ③ 두 갈래 차이를 **모양(shape)과 높이(offset)로 분리** ← 회신 BQ Q2.
     `E_dn = E_up + C` 면 V₀·곡률이 같은데도 옛 dE/span 은 컸다
  ④ r² · B0′ · 판정 사유
  ⑤ GPU · 로그 신선도 (재부팅 전 로그는 **죽음**으로 찍는다)

⛔ 이 도구가 **못 하는 것**
  · **판정하지 않는다.** 어느 조건이 옳은지, 골짜기 이동인지 수렴 문제인지 말하지 않는다.
    숫자를 나란히 놓을 뿐이고, 읽는 것은 사람 몫이다.
  · `dE/span` 을 조건 간 비교에 쓰지 말라고 **경고만** 한다 (분모가 부피창에 딸려간다).
    그 비교를 막지는 못한다.
  · 왜 느린지 못 짚는다. 경과와 갱신 시각만 보인다.
  · 물리를 검증하지 않는다. B0′ 가 물리적인지도 게이트가 볼 뿐이다.
"""
import argparse
import glob as _glob
import json
import os
import subprocess
import sys
import time


def sh(c):
    try:
        return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=10).stdout
    except Exception:                                          # noqa: BLE001
        return ""


def boot_epoch():
    try:
        with open("/proc/uptime") as f:
            return time.time() - float(f.read().split()[0])
    except Exception:                                          # noqa: BLE001
        return 0.0


def conv_of(eos):
    """수렴 기록을 꺼낸다. 연쇄판은 hysteresis 안, 단일판은 최상위."""
    h = eos.get("hysteresis") or {}
    return h.get("convergence_up") or eos.get("convergence") or []


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--glob", default="runs/cascade_pilot/fix_*", help="조건 디렉터리 glob")
    ap.add_argument("--log", default="/tmp/eos_fix.log", help="드라이버 로그")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        ok = bad = 0
        def chk(c, m):
            nonlocal ok, bad
            if c: ok += 1
            else: bad += 1; print(f"  ⛔ {m}")
        chk(conv_of({"hysteresis": {"convergence_up": [1, 2]}}) == [1, 2], "연쇄판: hysteresis 안에서 꺼낸다")
        chk(conv_of({"convergence": [3]}) == [3], "단일판: 최상위에서 꺼낸다")
        chk(conv_of({}) == [], "⛔음성: 기록이 없으면 빈 목록 (0 으로 지어내지 않는다)")
        chk(conv_of({"hysteresis": {}}) == [], "⛔음성: 빈 hysteresis 도 빈 목록")
        # 수렴 집계가 **문자열 True 에 속지 않는가** (json default=str 사고)
        rows = [{"converged": True}, {"converged": "False"}, {"converged": False}]
        n = sum(1 for r in rows if r.get("converged") is True)
        chk(n == 1, "⛔음성: 문자열 'False' 를 참으로 세지 않는다 (is True 로 본다)")
        print(f"  selftest: ⭕ {ok} · ⛔ {bad}")
        return 0 if bad == 0 else 1

    B = boot_epoch()
    print(f"════════ EOS 조건 스윕 · {time.strftime('%m-%d %H:%M:%S')} ════════")
    g = sh("nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total "
           "--format=csv,noheader").strip()
    print(f"  GPU {g or 'n/a'}")
    alive = bool(sh("pgrep -f '[r]un_mlip_postproc'").strip())
    print(f"  드라이버 {'▶ 도는 중' if alive else '■ 멈춤'}")

    if os.path.exists(a.log):
        m = os.path.getmtime(a.log)
        age = (time.time() - m) / 60.0
        dead = m < B
        print(f"  로그 {a.log} — {'⛔ 재부팅 전 = 죽음' if dead else f'{age:.0f}분 전 갱신'}")
        heads = [l for l in open(a.log, errors="replace").read().splitlines()
                 if l.startswith("########") or l.startswith("ALLDONE")]
        if heads:
            print(f"  마지막 단계: {heads[-1][:78]}")
    else:
        print(f"  ⚠ 로그가 없다: {a.log}")

    dirs = sorted(_glob.glob(a.glob))
    if not dirs:
        print(f"\n■ {a.glob} 에 조건 디렉터리가 없다 — 아직 안 던졌거나 glob 이 다르다")
        return 0

    print(f"\n{'조건':<9}{'구조':<14}{'수렴':>7}{'잔여힘':>9}{'모양차':>9}{'높이차':>9}"
          f"{'r2':>8}{'Bp':>7}  판정")
    print("─" * 96)
    for d in dirs:
        cond = os.path.basename(d).split("_", 1)[-1] if "_" in os.path.basename(d) else os.path.basename(d)
        recs = []
        s = os.path.join(d, "postproc_summary.json")
        if os.path.exists(s):
            try:
                recs = json.load(open(s)).get("records") or []
            except Exception:                                  # noqa: BLE001
                pass
        if not recs:                       # 요약이 아직이면 개별 파일로
            for p in sorted(_glob.glob(os.path.join(d, "*", "postproc.json"))):
                try:
                    recs.append(json.load(open(p)))
                except Exception:                              # noqa: BLE001
                    pass
        if not recs:
            print(f"{cond:<9}{'(아직 출력 없음)':<14}")
            continue
        for r in recs:
            e = r.get("eos") or {}
            h = e.get("hysteresis") or {}
            cv = conv_of(e)
            # ⛔ `is True` — json default=str 이 불리언을 "False" 문자열로 만든 전력이 있다
            nok = sum(1 for x in cv if x.get("converged") is True)
            mxf = max([x.get("final_fmax_eV_A") or 0.0 for x in cv] or [0.0])
            bp = e.get("Bp")
            why = "OK" if e.get("fit_quality_ok") else (e.get("fit_quality_reason") or "—")
            print(f"{cond:<9}{(r.get('name') or '?')[:13]:<14}"
                  f"{f'{nok}/{len(cv)}' if cv else '—':>7}"
                  f"{mxf:>9.4f}"
                  f"{h.get('shape_max_abs_dE_eV', 0.0):>9.4f}"
                  f"{h.get('level_offset_eV', 0.0):>9.4f}"
                  f"{(e.get('r2') or 0.0):>8.4f}"
                  f"{(f'{bp:.2f}' if bp else '—'):>7}  {why[:34]}")

    print("\n  읽는 법")
    print("   · 수렴 7/7 인데 **모양차**가 크면 → 골짜기 이동 쪽. 수렴이 낮으면 그 줄은 아직 말이 없다")
    print("   · 잔여힘이 요청 fmax 보다 크면 그 점은 **안 풀린 것**이다")
    print("   · 높이차만 크고 모양차가 0 이면 두 갈래는 **평행이동**이다 — V₀·곡률은 같다")
    print("  ⛔ 이 표는 판정하지 않는다. 그리고 `dE/span` 은 분모가 부피창에 딸려가므로")
    print("     **조건(창)이 다른 줄끼리 같은 문턱으로 비교하지 마라** (회신 BQ Q2).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
