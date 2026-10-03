#!/usr/bin/env python3
"""watch_cv7probe.py — cascade v7 탐침 한 화면 (run_cascade_v7_probe.py 의 감시 짝 · 읽기만 · **D 없음**).

    python3 ~/bin/cv7_watch.py                              # 기본 out_root ~/work/runs/cascade_v7_probe_1003
    watch -n 600 -t python3 ~/bin/cv7_watch.py
    python3 tools/doping/watch_cv7probe.py --selftest

배포 — 러너가 도는 worktree(~/wt_cv7probe_1003)를 **건드리지 않고** repo 에서 이 파일만 꺼낸다.
  stdlib 만 쓰므로 어느 python3 로도 어디서든 돈다:
    git -C ~/lldvar fetch origin claude/evac-2026-10-02 && git -C ~/lldvar show FETCH_HEAD:tools/doping/watch_cv7probe.py > ~/bin/cv7_watch.py

왜 watch_eprime.py 를 안 쓰나
  그 도구는 v5/v6 용이라 끝난 런의 **D_Li 를 화면에 찍는다** — v7 탐침은 D 봉인이다 (개정 §6).
  러너의 `--status` 는 D 가 없지만 러너 worktree 안에서만 돈다 (판독기·v6 러너를 import 한다).

무엇을 보나
  ① 러너가 살아 있나 — 잠금 파일(.runner.lock)의 PID 를 `kill -0` + /proc cmdline 으로 (pgrep 안 씀 — 자기 자신을 센다) ·
     tmux 세션 이름 · 러너 로그 신선도
  ② 예산 — 누적 / 상한 · 끝난 런 단가 실측 · 그 최댓값으로 상한 안에서 더 돌 수 있는 런 수
  ③ 지금 도는 런 — md.log 시간 / (평형 + 생산) ps · 경과 · **이 런의 지금 속도로** 외삽한 남은 시간 · 예상 끝 (이 기계 시계)
  ④ 끝난 런 — 판독기 산출물의 자격 · 골격 경보 · 부창비 · 사건 (D 없음) · 생산 구간 온도 · GPU-h
  ⑤ 마지막 판독 — T* · next · 사유 ⑥ GPU 합계·사용률 ⑦ 러너 로그 끝 몇 줄

⛔ 못 하는 것 / 안 하는 것
  · D 를 읽지도 찍지도 않는다 — msd.json · ensemble_results.json · logs/<태그>.log 를 **열지 않는다** (드라이버가 D 를 쓰는 곳).
    판독기 산출물도 정해 둔 키만 옮긴다 (거기 D 가 섞여도 안 나온다).
  · 판정하지 않는다 — 자격·T* 는 cascade_v7_probe.json 을 옮겨 적을 뿐이다. 그 파일은 **런 사이에만** 갱신된다.
  · 남은 시간은 이 런의 지금까지 평균 속도 외삽이다 — 첫 1 분의 UMA 로드를 포함하고, GPU 공유(P1b pw.x)가 바뀌면 빗나간다.
    다음 런·탐침 전체의 끝은 모른다 (판독기 결과에 따라 런 수가 달라진다).
  · 러너를 멈추거나 고치지 않는다 · 잠금을 잡지 않는다 · GPU 프로세스별 사용량을 못 본다 (kgy 는 막혀 있다).
"""
from __future__ import annotations

import argparse
import calendar
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

DEFAULT_OUT = "~/work/runs/cascade_v7_probe_1003"
SESSION = "cv7probe"
RUNNER_NAME = "run_cascade_v7_probe"
SUBDIR = "d0.00_cfg0"
JUDGE_KEYS = ("T_K", "structure", "seed", "eligible", "framework_alarm", "sub_window_ratios", "events", "error")


def _json(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def runner_state(out_root) -> tuple[str, int | None]:
    """→ (상태 문장, PID). 잠금 파일의 PID 가 살아 있고 그 명령줄이 러너일 때만 '살아 있음'."""
    lk = Path(out_root) / ".runner.lock"
    try:
        pid = int(lk.read_text().split()[0])
    except (OSError, ValueError, IndexError):
        return "잠금 파일 없음 — 러너가 아직 안 떴다", None
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return f"러너 없음 (PID {pid} 끝남 — 로그 끝 줄이 이유다)", pid
    except PermissionError:
        pass
    try:
        cmd = Path(f"/proc/{pid}/cmdline").read_bytes().replace(b"\0", b" ").decode("utf-8", "ignore")
    except OSError:
        return f"PID {pid} 살아 있으나 명령줄을 못 읽음 — 러너인지 확인 못 함", pid
    if RUNNER_NAME not in cmd:
        return f"러너 없음 (PID {pid} 는 다른 프로세스 — PID 재사용)", pid
    return f"러너 살아 있음 (PID {pid})", pid


def mdlog_last(path) -> tuple[float, float] | None:
    """md.log 마지막 데이터 줄 (시간 ps, 온도 K)."""
    try:
        with open(path, "rb") as fh:
            fh.seek(0, os.SEEK_END)
            fh.seek(max(0, fh.tell() - 4096))
            lines = fh.read().decode("utf-8", "ignore").splitlines()
    except OSError:
        return None
    for line in reversed(lines):
        p = line.split()
        try:
            return float(p[0]), float(p[-1])
        except (ValueError, IndexError):
            continue
    return None


def eta(t_ps, total_ps, elapsed_s) -> float | None:
    """이 런의 지금까지 평균 속도로 남은 초. 진행이 0 이면 None (모른다 ≠ 0)."""
    if t_ps is None or t_ps <= 0 or elapsed_s <= 0:
        return None
    return max(total_ps - t_ps, 0.0) * elapsed_s / t_ps


def utc_epoch(s) -> float | None:
    try:
        return float(calendar.timegm(time.strptime(s, "%Y-%m-%dT%H:%M:%SZ")))
    except (TypeError, ValueError):
        return None


def affordable(used, cap, unit) -> int | None:
    if cap is None or unit is None or unit <= 0:
        return None
    return max(int((cap - used) // unit), 0)


def _sh(cmd) -> str | None:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return r.stdout.strip() if r.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def report(out_root, log=None, now=None, nvsmi="nvidia-smi", tmux="tmux") -> tuple[int, list[str]]:
    out_root = Path(out_root).expanduser()
    log = Path(log).expanduser() if log else Path(str(out_root) + ".log")
    now = time.time() if now is None else now
    L = [f"════ cascade v7 탐침 · {time.strftime('%F %T', time.localtime(now))} · {out_root} ════"]
    if not out_root.is_dir():
        return 2, L + ["⛔ out_root 가 없다 — 탐침이 아직 안 떴거나 경로가 다르다 (--out_root)"]
    state, _ = runner_state(out_root)
    sess = _sh([tmux, "ls", "-F", "#S"])
    L.append(f"① {state} · tmux 세션: {', '.join(sess.split()) if sess else '없음/못 읽음'}"
             + ("" if sess and SESSION in sess.split() else f" (⚠ {SESSION} 없음)"))
    try:
        age = (now - log.stat().st_mtime) / 60.0
        L.append(f"   러너 로그 {log.name} · 마지막 갱신 {age:.0f} 분 전 (러너는 30 분마다 진행 줄을 쓴다)")
    except OSError:
        L.append(f"   러너 로그 {log} 없음")
    m, b = _json(out_root / "manifest.json") or {}, _json(out_root / "budget.json")
    if b is None:
        return 2, L + ["⛔ budget.json 을 못 읽는다 — 러너가 사전점검에서 멈췄을 수 있다 (로그 끝 확인)"]
    fr = m.get("frozen") or {}
    total_ps = float(fr.get("equilib_ps", 5.0)) + float(fr.get("prod_ps", 400.0))
    steps = b.get("steps") or []
    done = [s for s in steps if s.get("ok")]
    used, cap = float(b.get("used_gpu_h") or 0.0), b.get("cap_gpu_h")
    meas = [float(s["gpu_h"]) for s in done if isinstance(s.get("gpu_h"), (int, float))]
    unit = max(meas) if meas else b.get("est_gpu_h_per_run")
    more = affordable(used, cap, unit)
    L.append(f"② 누적 {used:.2f} / 상한 {cap} GPU-h · 끝난 런 {len(done)} · 단가 실측 {[round(x, 2) for x in meas] or '없음'} · "
             f"단가 {unit} ({'실측 최댓값' if meas else '추정'}) 기준 상한 안에서 더 돌 수 있는 런 ≈ {more}")
    running = [s for s in steps if "rc" not in s and "stopped" not in s and s.get("T_K") is not None]
    for s in running:
        md = out_root / "md" / str(s.get("tag")) / SUBDIR / f"T{int(s['T_K'])}" / "md.log"
        t0 = utc_epoch(s.get("start_utc"))
        el = (now - t0) if t0 else None
        last = mdlog_last(md)
        if last is None:
            L.append(f"③ ▶ {s.get('tag')} · 경과 {el / 3600:.2f} h · md.log 아직 없음 (UMA 로드·평형 시작 전)" if el is not None
                     else f"③ ▶ {s.get('tag')} · md.log 없음")
            continue
        e = eta(last[0], total_ps, el or 0.0)
        L.append(f"③ ▶ {s.get('tag')} · md.log {last[0]:.1f} / {total_ps:g} ps ({100 * last[0] / total_ps:.0f} %) · T {last[1]:.0f} K · "
                 f"경과 {el / 3600:.2f} h" + (f" · 남은 ≈ {e / 3600:.1f} h · 예상 끝 {time.strftime('%m-%d %H:%M', time.localtime(now + e))}"
                                            " (이 런 지금 속도 외삽)" if e is not None else " · 남은 시간 모름 (진행 0)"))
    if not running:
        L.append("③ 지금 도는 런 없음")
    jd = _json(out_root / "cascade_v7_probe.json") or {}
    jr = {(r.get("T_K"), r.get("structure"), r.get("seed")): {k: r.get(k) for k in JUDGE_KEYS if k in r}
          for r in jd.get("runs") or [] if isinstance(r, dict)}
    for s in steps:
        if "rc" not in s and "stopped" not in s:
            continue
        r = jr.get((s.get("T_K"), s.get("structure"), s.get("seed")), {})
        verdict = ("자격 " + ("통과" if r.get("eligible") else "미달") + f" · 골격 {r.get('framework_alarm', '—')} · "
                   f"부창비 {[round(float(x), 2) for x in (r.get('sub_window_ratios') or []) if isinstance(x, (int, float))]} · "
                   f"사건 {r.get('events', '—')}" + (f" · ⛔ {r['error']}" if r.get("error") else "")) if r else "판독 전"
        head = "✔" if s.get("ok") else "⛔ " + str(s.get("stopped") or s.get("failed") or f"rc {s.get('rc')}")[:120]
        L.append(f"④ {head} {s.get('tag')} · {s.get('gpu_h', '—')} GPU-h · 생산 T {s.get('mdlog_T_production') or '—'} · {verdict}")
    if jd:
        L.append(f"⑤ 마지막 판독: T* {jd.get('T_star_K')} · next {jd.get('next')} · {jd.get('why')}")
    g = _sh([nvsmi, "--query-gpu=memory.used,memory.total,utilization.gpu", "--format=csv,noheader"])
    L.append(f"⑥ GPU {g or '못 읽음'} (P1b pw.x 와 공유 · 프로세스별은 못 본다)")
    try:
        tail = Path(log).read_text(encoding="utf-8", errors="ignore").splitlines()[-3:]
        L += ["⑦ 러너 로그 끝:"] + [f"   {x[:200]}" for x in tail]
    except OSError:
        pass
    return 0, L


def _selftest() -> int:
    fails = []

    def ck(name, cond):
        print(f"  {'✓' if cond else '✗'} {name}", flush=True)
        if not cond:
            fails.append(name)

    ck("남은 시간: 100/405 ps 를 2 h 에 → 6.1 h", abs(eta(100.0, 405.0, 7200.0) / 3600 - 6.1) < 1e-9)
    ck("⛔음성 진행 0 이면 남은 시간 None (0 이 아니다)", eta(0.0, 405.0, 7200.0) is None and eta(None, 405.0, 1.0) is None)
    ck("상한 안 런 수: (141 − 23.6) // 11.8 = 9", affordable(23.6, 141.0, 11.8) == 9)
    ck("⛔음성 누적 ≥ 상한 → 0 (음수 아님)", affordable(150.0, 141.0, 11.8) == 0)
    ck("⛔음성 단가 모름 → None", affordable(0.0, 141.0, None) is None)
    tmp = Path(tempfile.mkdtemp(prefix="cv7watch_st_"))
    try:
        out = tmp / "probe"
        rc, L = report(out)
        ck("⛔음성 out_root 없음 → rc 2 · 안 띄웠다고 말한다", rc == 2 and "안 떴" in L[-1])
        (out / "md" / "H0_host__T800__s2" / SUBDIR / "T800").mkdir(parents=True)
        (out / "md" / "H0_host__T800__s1" / SUBDIR / "T800").mkdir(parents=True)
        now = 1_800_000_000.0
        start = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now - 7200))
        (out / "manifest.json").write_text(json.dumps({"frozen": {"equilib_ps": 5.0, "prod_ps": 400.0}}))
        (out / "budget.json").write_text(json.dumps({"cap_gpu_h": 141.0, "est_gpu_h_per_run": 11.8, "used_gpu_h": 13.0, "steps": [
            {"tag": "H0_host__T800__s1", "T_K": 800, "structure": "H0_host", "seed": 1, "rc": 0, "ok": True, "gpu_h": 11.0,
             "mdlog_T_production": {"mean_K": 799.6}},
            {"tag": "H0_host__T800__s2", "T_K": 800, "structure": "H0_host", "seed": 2, "start_utc": start}]}))
        (out / "md" / "H0_host__T800__s2" / SUBDIR / "T800" / "md.log").write_text(
            "Time[ps]  Etot  T[K]\n0.0000 -1 800\n100.0000 -1 803\n")
        (out / "cascade_v7_probe.json").write_text(json.dumps({"T_star_K": None, "next": [800, "H0_host", 2], "why": "800 K: 남은 5",
            "runs": [{"T_K": 800, "structure": "H0_host", "seed": 1, "eligible": True, "framework_alarm": "ok",
                      "sub_window_ratios": [1.0, 0.9], "events": 120, "D_Li_cm2_s": 9.87e-6}]}))
        (out / "md" / "H0_host__T800__s1" / SUBDIR / "T800" / "msd.json").write_text('{"D_Li_cm2_s": 1.234e-06}')
        (out / "logs").mkdir()
        (out / "logs" / "H0_host__T800__s1.log").write_text("D_Li=1.234e-06 cm2/s\n")
        Path(str(out) + ".log").write_text("[x] ▶ H0_host__T800__s2\n")
        (out / ".runner.lock").write_text(f"{os.getpid()}\n")
        rc, L = report(out, now=now, nvsmi="/bin/false", tmux="/bin/false")
        txt = "\n".join(L)
        ck("양성: 도는 런 진행 100.0 / 405 ps · 남은 ≈ 6.1 h", rc == 0 and "100.0 / 405 ps" in txt and "남은 ≈ 6.1 h" in txt)
        ck("양성: 끝난 런은 판독기의 자격·사건을 옮긴다", "✔ H0_host__T800__s1" in txt and "자격 통과" in txt and "사건 120" in txt)
        ck("양성: 단가 실측 최댓값 11.0 → 상한 안 런 ≈ 11", "≈ 11" in txt)
        ck("⛔ D 봉인: 판독 산출물·msd.json·런 로그의 D 가 화면에 없다", "9.87" not in txt and "1.234" not in txt and "D_Li" not in txt)
        ck("⛔음성 잠금 PID 가 러너가 아니면(PID 재사용) '살아 있음' 이라 하지 않는다", "다른 프로세스" in txt and "살아 있음 (PID" not in txt)
        ck("⛔음성 GPU·tmux 못 읽음 → '못 읽음/없음' (비어 있음 아님)", "GPU 못 읽음" in txt and "⚠ cv7probe 없음" in txt)
        p = subprocess.Popen([sys.executable, "-c", "pass"])
        p.wait()
        (out / ".runner.lock").write_text(f"{p.pid}\n")
        _, L = report(out, now=now, nvsmi="/bin/false", tmux="/bin/false")
        ck("⛔음성 끝난 PID → '러너 없음'", "끝남" in "\n".join(L))
        fake = tmp / RUNNER_NAME
        fake.write_text("import time\ntime.sleep(30)\n")
        q = subprocess.Popen([sys.executable, str(fake)])
        try:
            time.sleep(0.2)
            (out / ".runner.lock").write_text(f"{q.pid}\n")
            _, L = report(out, now=now, nvsmi="/bin/false", tmux="/bin/false")
            ck("양성: 명령줄에 러너 이름이 있는 살아 있는 PID → '살아 있음'", "러너 살아 있음" in "\n".join(L))
        finally:
            q.kill(); q.wait()
        (out / "md" / "H0_host__T800__s2" / SUBDIR / "T800" / "md.log").unlink()
        _, L = report(out, now=now, nvsmi="/bin/false", tmux="/bin/false")
        ck("⛔음성 md.log 없음 → '아직 없음' (0 % 로 그리지 않는다)", "md.log 아직 없음" in "\n".join(L) and "(0 %)" not in "\n".join(L))
        (out / "budget.json").write_text("{")
        rc, L = report(out, now=now, nvsmi="/bin/false", tmux="/bin/false")
        ck("⛔음성 budget.json 깨짐 → rc 2", rc == 2)
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"selftest {'PASS' if not fails else 'FAIL'} ({len(fails)} 실패)")
    return 0 if not fails else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="cascade v7 탐침 감시 (읽기만 · D 없음)")
    ap.add_argument("--out_root", default=DEFAULT_OUT)
    ap.add_argument("--log", default=None, help="러너 로그 (기본 <out_root>.log)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    rc, L = report(a.out_root, a.log)
    print("\n".join(L))
    return rc


if __name__ == "__main__":
    sys.exit(main())
