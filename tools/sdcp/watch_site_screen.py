#!/usr/bin/env python3
"""watch_site_screen.py — 자리 선호 스크리닝 진행 감시.

숫자만 세지 않는다. **판정이 성립할 수 있는 상태인지**를 같이 본다:
  · 단계별 진척(아틀라스 → rigid → relax@freeze) + ETA
  · 게이트 탈락 누적 (사유별·양이온별) — 검열이 한쪽으로 쏠리면 그 자리에서 보인다
  · **Li/Ni 대조쌍 완성 수** — 이게 0이면 아무리 오래 돌려도 자리 판정이 안 나온다
  · 로그 꼬리 · GPU

  python3 tools/sdcp/watch_site_screen.py                    # 1회
  python3 tools/sdcp/watch_site_screen.py --loop 60          # 60초마다
  python3 tools/sdcp/watch_site_screen.py --run <RUN> --loop 30
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_screen import PRIMARY, shortlist_with_matched_pairs  # noqa: E402

DEF_RUN = "/data/work/runs/sdcp_v4_sitescreen"


def load_dir(d: Path):
    out = []
    if not d.is_dir():
        return out
    for p in sorted(d.glob("*.json")):
        if p.name.startswith("_"):
            continue
        try:
            out.append((json.loads(p.read_text()), p.stat().st_mtime))
        except json.JSONDecodeError:      # 쓰는 중인 파일
            pass
    return out


def fmt_dt(sec: float) -> str:
    if sec < 0 or sec != sec:
        return "—"
    h, m = divmod(int(sec) // 60, 60)
    return f"{h}h{m:02d}m" if h else f"{m}m"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default=DEF_RUN)
    ap.add_argument("--loop", type=float, default=0, help="초 단위 반복 (0=1회)")
    # (--freeze 제거 — '1.0' vs '1.00' 문자열 함정. relax_f* 디렉터리를 직접 발견한다. 자체 리뷰 #9)
    a = ap.parse_args()
    run = Path(a.run)

    while True:
        if a.loop:
            os.system("clear")
        print(f"═══ site_screen  {run}   {time.strftime('%H:%M:%S')} ═══")
        if not run.is_dir():
            print(f"⛔ {run} 이 없다"); return 2
        shortfall = 0        # 목표치에 못 미친 단계 수 — '완료'와 '정지'를 구분하려고 센다
        relax_missing = 0    # rigid 는 됐는데 relax 디렉터리가 하나도 없는 조각 수

        for frag in PRIMARY:
            fdir = run / frag
            if not fdir.is_dir():
                # ★ 자체 리뷰 #2 — 없는 조각을 조용히 건너뛰면 '아무것도 없음'이 완료로 찍힌다
                print(f"  {frag:14s} (없음 — 미시작)"); shortfall += 1; continue
            atlas = len(list(fdir.glob("*.xyz")))
            rigid = load_dir(fdir / "rigid")

            # rigid 목표치 = atlas 통과 자세 수 (atlas_rows.json 이 정본)
            rigid_target = None
            try:
                rigid_target = sum(1 for r in json.loads((fdir / "atlas_rows.json").read_text())
                                   if r.get("ranking_eligible"))
            except (OSError, json.JSONDecodeError):
                pass
            if rigid_target is None or len(rigid) < rigid_target:
                shortfall += 1           # 목표를 모르는 것도 '완료 증명 불가'다
            rt = f"/{rigid_target}" if rigid_target is not None else "/?"
            line = f"  {frag:14s} atlas {atlas:4d} · rigid {len(rigid):4d}{rt}"

            # relax 디렉터리는 실제로 존재하는 것을 발견한다 (이름 규약 하드코딩 금지)
            relax_dirs = sorted(d for d in fdir.glob("relax_f*") if d.is_dir())
            if not relax_dirs and rigid:
                relax_missing += 1
            for rd in relax_dirs:
                rows = load_dir(rd)
                n = len(rows)
                # relax 목표치 = score 가 남긴 이완 명단 (없으면 기본 파라미터로 추정하고 표시)
                target, est = None, ""
                try:
                    target = len(json.loads((rd / "_shortlist.json").read_text()))
                except (OSError, json.JSONDecodeError):
                    if rigid:
                        try:
                            target = len(shortlist_with_matched_pairs([r for r, _ in rigid], 2, 5))
                            est = "≈"
                        except Exception:
                            target = None
                tgt = f"/{est}{target}" if target else "/?"
                eta = ""
                if target is None or n < target:
                    shortfall += 1
                    if len(rows) >= 2 and target:
                        ts = sorted(t for _, t in rows)
                        rate = (ts[-1] - ts[0]) / max(len(ts) - 1, 1)
                        eta = f" ETA {fmt_dt(rate * (target - n))}"
                line += f" · {rd.name.replace('relax_', '')} {n:3d}{tgt}{eta}"
            print(line)

            # 게이트 탈락 + 대조쌍 — relax 결과가 있을 때만 의미 있다
            for rd in relax_dirs:
                ff = rd.name.replace("relax_f", "")
                rows = [r for r, _ in load_dir(rd)]
                if not rows:
                    continue
                bad = [r for r in rows if not r.get("ranking_eligible")]
                cat = Counter(r.get("nearest_cation") for r in rows if r.get("ranking_eligible"))
                why = Counter((r.get("gate_reasons") or ["?"])[0].split("(")[0] for r in bad)
                # 대조쌍: 같은 down_dir·roll 로 Li_top 과 Ni_top 이 **둘 다** 살아 있는가
                idx = {(r.get("site"), r.get("down_dir"), r.get("roll_deg")): r
                       for r in rows if r.get("ranking_eligible")}
                pairs = sum(1 for (s, d, ro) in idx
                            if s == "Li_top" and ("Ni_top", d, ro) in idx)
                half = sum(1 for (s, d, ro) in idx
                           if s in ("Li_top", "Ni_top")
                           and (("Ni_top" if s == "Li_top" else "Li_top"), d, ro) not in idx)
                mark = "✔" if pairs else "⛔"
                print(f"      f{ff}: 통과 {len(rows)-len(bad)}/{len(rows)} · 접촉 {dict(cat)} · "
                      f"탈락 {dict(why) or '없음'}")
                print(f"      {mark} 완성된 Li/Ni 대조쌍 **{pairs}쌍** · 한쪽만 살아남은 자세 {half}개"
                      + ("   ← 이게 0이면 자리 판정이 안 나온다" if not pairs else ""))
                if bad:
                    kc = Counter(r.get("nearest_cation") for r in bad)
                    if len(kc) == 1 and sum(kc.values()) >= 3:
                        print(f"      ⚠ 탈락이 **{list(kc)[0]} 접촉 쪽으로만 쏠렸다** ({sum(kc.values())}건) "
                              "— 검열 편향 경로. verdict 의 검열 검사를 반드시 볼 것")

        # 프로세스 · 로그 · GPU
        print()
        running = ""
        try:
            running = subprocess.run(["pgrep", "-fa", r"python.*site_screen\.py score"],
                                     capture_output=True, text=True).stdout.strip()
        except FileNotFoundError:
            pass
        if running:
            print(running)
        elif shortfall == 0 and relax_missing == 0:
            print("  ✔ **완료** — 모든 단계가 목표치에 도달했고 실행 중인 job 이 없다")
        elif shortfall == 0:
            print(f"  ⚠ rigid 까지 완료 — relax 미시작 조각 {relax_missing}개 (완료 아님)")
        else:
            print(f"  ⛔ score 가 안 돌고 있는데 목표에 못 미친 단계가 {shortfall}개 있다 — 중단/미시작")
        logs = sorted((run / "logs").glob("relax_*.log")) + sorted((run / "logs").glob("rigid_*.log"))
        if logs:
            newest = max(logs, key=lambda p: p.stat().st_mtime)
            age = time.time() - newest.stat().st_mtime
            tail = newest.read_text(errors="ignore").strip().splitlines()[-3:]
            print(f"  ── {newest.name} (마지막 갱신 {fmt_dt(age)} 전) ──")
            for t in tail:
                print("   " + t[:150])
            # 로그 정체는 **실행 중일 때만** 이상 신호다. 끝난 job 의 로그는 당연히 안 는다.
            if age > 900 and running:
                print("  ⚠ 15분 넘게 로그가 안 늘었다 — 멈췄는지 확인할 것")
        try:
            g = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,memory.total",
                                "--format=csv,noheader"], capture_output=True, text=True).stdout.strip()
            print(f"  GPU {g}")
        except FileNotFoundError:
            pass

        if not a.loop:
            return 0
        time.sleep(a.loop)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:          # Ctrl+C 는 정상 종료다 — traceback 을 뱉지 않는다
        print("\n(감시 종료)")
        sys.exit(0)
