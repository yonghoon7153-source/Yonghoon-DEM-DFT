#!/usr/bin/env python3
"""li2s2_stage1_runner.py — li2s-2 카드 1 단계 (고정 밀도 담금질 10 개 · kgy 한 기계 · 한 번에 하나) 실행기.

카드 : db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json (§1b · §4 S1 · 기계_판독_값)
결정 : D-2026-11-03-li2s2-dense-window — **active 가 아니면 시작하지 않는다**
회신 DF: P1-2 (판정은 --stage1_verdict 의 필드 · 종료코드를 합치지 않는다) · P1-3 (한쪽 계가 닫히면 트랙 전체 멈춤)
         Q-DF-3 (첫 시드의 100 ps 녹음 판정이 그 담금질과 뒤 시드를 **실제로** 멈춘다)

하는 일 (순서 A11 → B11 → A12 → B12 → … → B15 · 계를 번갈아):
  ① 시작 전: 결정 active · 드라이버 sha16 = 고정값 · 카드 값 · 잠금 (같은 run_root 에 살아 있는 러너가 있으면 거부)
  ② 시드마다: 판정 파일이 있으면 건너뜀 · 판정 없이 런 폴더만 있으면 **멈춤** (끊긴 런을 덮어쓰지 않는다 — 사람이 정한다)
  ③ 상한: 누적 벽시계 + 한 시드 최악 (관측 최댓값 · 없으면 --seed_worst_h) > --cap_h 면 새 시드를 띄우지 않고 '상한 · 미완결' 로 멈춤
     (회신 DF P1-6: 상한 비교는 런 벽시계를 온전히 합산 · 그때까지 끝난 시드만 골라 판정하지 않는다)
  ④ GPU 가 빌 때까지 기다린다 (memory.used ≤ --start_max_mib 두 번 연속 — cascade 가 끝나면 열린다)
  ⑤ 담금질을 띄운다 (카드 일정 · 고정 밀도 · turbo) — 계의 **첫 시드**면 --poll_s 마다 melt_window_check:
     미충족 · 무효 → 그 담금질을 죽이고 판정 파일 (fail · invalid) · STOP.json 을 쓰고 멈춘다 · 미완 → 계속 본다 · 통과 → 끝까지 둔다
  ⑥ 담금질 rc 0 → stage1_verdict → stage1_summary → stop_track · invalid 면 멈춤 · rc ≠ 0 → 멈춤 (비정상 종료 · 사용자 결정)
  ⑦ 장부 stage1_ledger.json (시드마다 시작 · 끝 · 벽시계 · rc · 판정) · 로그 stage1.log · 끝나면 stage1_summary.json

종료코드: 0 1 단계 통과 (2 단계 시드는 stage1_summary.json) · 10 거부 (결정 · sha · 잠금 · 카드) · 20 트랙 멈춤 (묶음 판정)
         21 첫 시드 녹음 미충족 · 무효 · 22 상한 · 미완결 · 23 담금질 비정상 종료 · 24 끊긴 런 폴더 · 25 끝났는데 묶음이 대기

⛔ 이 도구가 못 하는 것
  · GPU 를 다른 잡과 나눠 쓰는지 프로세스별로 못 본다 (kgy 는 프로세스 정보가 막혀 있다) — 총 사용량으로만 기다린다
  · 끊긴 시드를 이어 돌리지 않는다 · 2 단계를 띄우지 않는다 (묶음 판정과 2 단계 시드만 적는다)
  · 판정 자체는 하지 않는다 — melt_quench_uma.py 의 melt_window_check · stage1_verdict · stage1_summary 를 부른다 (같은 worktree · sha 고정)

  python3 tools/ionic/li2s2_stage1_runner.py --worktree ~/wt_li2s2 --run_root ~/work/runs/li2s2_dense_1103 \\
          --python /home/kgy/apps/miniforge3/envs/uma/bin/python
  python3 tools/ionic/li2s2_stage1_runner.py --selftest
"""
from __future__ import annotations
import argparse, datetime, hashlib, importlib.util, json, os, pathlib, signal, subprocess, sys, tempfile, time

EXPECTED_DRIVER_SHA16 = "f5063afca93dbf31"     # tools/ionic/melt_quench_uma.py — 바뀌면 이 줄도 같이 바꾸고 다시 리뷰한다
DECISION = "D-2026-11-03-li2s2-dense-window"
CARD_REL = "db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json"
DRIVER_REL = "tools/ionic/melt_quench_uma.py"
N_FU = {"A": 12, "B": 15}
DEFAULT_ORDER = "A:11,B:11,A:12,B:12,A:13,B:13,A:14,B:14,A:15,B:15"
RC = {"pass": 0, "refused": 10, "track": 20, "melt": 21, "cap": 22, "abnormal": 23, "resume": 24, "pending": 25}


def _now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def sha16(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()[:16]


def decision_state(worktree, did=DECISION):
    D = json.loads((pathlib.Path(worktree) / "db/governance/decisions.json").read_text(encoding="utf-8"))
    hit = [d for d in D["decisions"] if d.get("id") == did]
    return hit[0].get("decision_state") if len(hit) == 1 else None


def load_mq(worktree):
    """같은 worktree 의 melt_quench_uma.py 를 모듈로 (sha 를 본 그 파일)."""
    spec = importlib.util.spec_from_file_location("melt_quench_uma_li2s2", str(pathlib.Path(worktree) / DRIVER_REL))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def parse_order(s):
    out = []
    for tok in s.split(","):
        sysn, seed = tok.strip().split(":")
        if sysn not in N_FU:
            raise SystemExit(f"⛔ 순서에 모르는 계 {sysn}")
        out.append((sysn, int(seed)))
    return out


class _Proc:
    """subprocess.Popen 감싸개 — 시험에서 같은 모양의 가짜로 바꾼다."""
    def __init__(self, cmd, log_path):
        self.fh = open(log_path, "a")
        self.p = subprocess.Popen(cmd, stdout=self.fh, stderr=subprocess.STDOUT, start_new_session=True)
    def poll(self):
        return self.p.poll()
    def stop(self, grace_s=60):
        """그 담금질만 (자기 프로세스 그룹) 죽인다 — 이름으로 잡지 않는다 (CLAUDE.md pkill 금지)."""
        try:
            os.killpg(self.p.pid, signal.SIGTERM)
        except ProcessLookupError:
            return self.p.poll()
        t0 = time.time()
        while self.p.poll() is None and time.time() - t0 < grace_s:
            time.sleep(1)
        if self.p.poll() is None:
            os.killpg(self.p.pid, signal.SIGKILL); self.p.wait()
        self.fh.close()
        return self.p.returncode
    @property
    def returncode(self):
        return self.p.returncode


def _gpu_used_mib():
    out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                         capture_output=True, text=True, check=True).stdout
    return int(out.split()[0])


def run(a, deps=None):
    deps = deps or {}
    W, R = pathlib.Path(a.worktree), pathlib.Path(a.run_root)
    R.mkdir(parents=True, exist_ok=True)
    sleep, clock = deps.get("sleep", time.sleep), deps.get("clock", time.time)
    gpu_used, launch = deps.get("gpu_used", _gpu_used_mib), deps.get("launch", _Proc)
    logf = open(R / "stage1.log", "a")
    def log(*m):
        line = f"[{_now()}] " + " ".join(str(x) for x in m)
        print(line, flush=True); logf.write(line + "\n"); logf.flush()
    def stop(code, reason, **detail):
        (R / "STOP.json").write_text(json.dumps({"at": _now(), "code": code, "reason": reason, **detail},
                                                ensure_ascii=False, indent=1), encoding="utf-8")
        log(f"⛔ 멈춤 ({code}) — {reason}")
        return RC[code]
    # ① 시작 전 점검
    st = decision_state(W)
    if st != "active":
        log(f"⛔ 결정 {DECISION} 이 active 가 아니다 ({st}) — 시작하지 않는다"); return RC["refused"]
    s16 = sha16(W / DRIVER_REL)
    if s16 != a.expect_sha:
        log(f"⛔ 드라이버 sha16 {s16} ≠ 고정값 {a.expect_sha} — 시작하지 않는다"); return RC["refused"]
    mq = deps.get("mq") or load_mq(W)
    try:
        vals = mq.read_li2s2_values(W / CARD_REL)
    except Exception as e:
        log(f"⛔ 카드 값을 못 읽었다 ({type(e).__name__}: {e})"); return RC["refused"]
    lock = R / "stage1.lock"
    if lock.exists():
        try:
            pid = int(lock.read_text().strip()); os.kill(pid, 0); alive = True
        except Exception:
            alive = False
        if alive and pid != os.getpid():
            log(f"⛔ 같은 run_root 로 러너가 살아 있다 (pid {pid}) — 시작하지 않는다"); return RC["refused"]
    lock.write_text(str(os.getpid()))
    try:
        sched, rho = vals["schedule"], vals["fix_density_g_cm3"]
        led_p = R / "stage1_ledger.json"
        ledger = json.loads(led_p.read_text(encoding="utf-8")) if led_p.is_file() else {"runs": []}
        ledger.update({"decision": DECISION, "driver_sha16": s16, "card": CARD_REL, "cap_h": a.cap_h})
        def save_ledger():
            led_p.write_text(json.dumps(ledger, ensure_ascii=False, indent=1), encoding="utf-8")
        order = parse_order(a.order)
        first = {}
        for sysn, seed in order:
            first.setdefault(sysn, seed)
        log(f"▶ 시작 · sha16 {s16} · 결정 {DECISION} active · 순서 {a.order} · 상한 {a.cap_h} h")
        for sysn, seed in order:
            rd = R / sysn / f"seed{seed}"
            vf = rd / "stage1_verdict.json"
            if vf.is_file():
                log(f"  {sysn}{seed}: 판정 있음 ({json.loads(vf.read_text(encoding='utf-8')).get('status')}) — 건너뜀"); continue
            if rd.exists():
                return stop("resume", f"{sysn}{seed} 런 폴더가 판정 없이 있다 — 끊긴 런을 덮어쓰지 않는다 (사람이 정한다)", sys=sysn, seed=seed)
            walls = [r["wall_h"] for r in ledger["runs"] if r.get("wall_h") is not None]
            cum, worst = sum(walls), max(walls + [a.seed_worst_h])
            if cum + worst > a.cap_h:
                save_ledger()
                return stop("cap", f"누적 {cum:.1f} h + 한 시드 최악 {worst:.1f} h > 상한 {a.cap_h} h — 미완결로 멈춤 (끝난 시드만 골라 판정하지 않는다)",
                            cum_h=cum, worst_h=worst)
            ok_n, t_wait = 0, clock()
            while ok_n < 2:
                u = gpu_used()
                ok_n = ok_n + 1 if u <= a.start_max_mib else 0
                if ok_n < 2:
                    if u > a.start_max_mib and (clock() - t_wait) % 1800 < a.gpu_poll_s:
                        log(f"  GPU {u} MiB > {a.start_max_mib} — 비기를 기다린다")
                    sleep(a.gpu_poll_s)
            cmd = [a.python, str(W / DRIVER_REL), "--system", sysn, "--n_fu", str(N_FU[sysn]), "--seed", str(seed),
                   "--T_melt", f"{sched['T_melt_K']:g}", "--T_final", f"{sched['T_final_K']:g}", "--melt_ps", f"{sched['melt_ps']:g}",
                   "--quench_rate", f"{sched['quench_rate_K_s']:g}", "--hold_ps", f"{sched['hold_ps']:g}", "--dt_fs", f"{sched['dt_fs']:g}",
                   "--save_ps", f"{sched['save_ps']:g}", "--turbo", "--fix_density", f"{rho[sysn]:g}",
                   "--compress_ps", f"{sched['compress_ps']:g}", "--out_root", str(R)]
            t0 = clock(); start = _now()
            log(f"▶ {sysn}{seed} 담금질 — ρ {rho[sysn]:g} · " + " ".join(cmd[2:]))
            h = launch(cmd, R / f"quench_{sysn}{seed}.log")
            need_melt = (seed == first[sysn])
            while h.poll() is None:
                sleep(a.poll_s)
                if need_melt:
                    mw = mq.melt_window_check(rd, values=vals, log=lambda *m: None)
                    if mw["verdict"] in ("fail", "invalid"):
                        h.stop()
                        rec = {"status": mw["verdict"], "system": sysn, "seed": seed, "melt_window_check": mw,
                               "reasons": {mw["verdict"]: [mw.get("message")]}, "by": "li2s2_stage1_runner — 첫 시드 녹음 판정 · 담금질을 멈춤"}
                        rd.mkdir(parents=True, exist_ok=True)
                        vf.write_text(json.dumps(rec, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
                        ledger["runs"].append({"system": sysn, "seed": seed, "start": start, "end": _now(),
                                               "wall_h": (clock() - t0) / 3600.0, "rc": "killed_melt", "status": mw["verdict"]})
                        save_ledger()
                        return stop("melt", f"{sysn}{seed} (계의 첫 시드) 녹음 판정 {mw['verdict']} — {mw.get('message')} · 그 계가 닫혀 트랙 전체 멈춤",
                                    sys=sysn, seed=seed)
                    if mw["verdict"] == "pass":
                        need_melt = False
                        log(f"  {sysn}{seed}: 녹음 판정 통과 (D_P {mw.get('D_framework_cm2_s')}) — 담금질 계속")
            rc = h.returncode
            ledger["runs"].append({"system": sysn, "seed": seed, "start": start, "end": _now(),
                                   "wall_h": (clock() - t0) / 3600.0, "rc": rc})
            save_ledger()
            if rc != 0:
                return stop("abnormal", f"{sysn}{seed} 담금질 rc {rc} — 비정상 종료 (사용자 결정 · 그 계를 어떻게 할지)", sys=sysn, seed=seed, rc=rc)
            v = mq.stage1_verdict(rd, values=vals, log=log)
            ledger["runs"][-1]["status"] = v.get("status"); save_ledger()
            sm = mq.stage1_summary(R, values=vals, log=log)
            if sm["track"] in ("stop_track", "invalid"):
                return stop("track", f"묶음 판정 {sm['track']} — {sm.get('why')}", summary=sm)
        sm = mq.stage1_summary(R, values=vals, log=log)
        if sm["track"] == "stage1_pass":
            log(f"✅ 1 단계 통과 — 2 단계 시드 {sm['stage2']['seeds']} · 기계 {sm['stage2']['machines']}")
            return RC["pass"]
        if sm["track"] in ("stop_track", "invalid"):
            return stop("track", f"묶음 판정 {sm['track']} — {sm.get('why')}", summary=sm)
        return stop("pending", f"순서를 다 돌았는데 묶음 판정이 {sm['track']} — 판정 파일을 확인한다", summary=sm)
    finally:
        try:
            if lock.read_text().strip() == str(os.getpid()):
                lock.unlink()
        except Exception:
            pass
        logf.close()


# ───────────────────────── selftest ─────────────────────────
def _selftest():
    ok = bad = 0
    def chk(c, m):
        nonlocal ok, bad
        print(("  ⭕ " if c else "  ⛔ ") + m); ok += bool(c); bad += (not c)
    repo = pathlib.Path(__file__).resolve().parents[2]
    real = load_mq(repo)
    VAL = real.read_li2s2_values(repo / CARD_REL)

    class FakeMQ:
        """판정 함수 가짜 — 시나리오대로 · 묶음 판정은 **진짜** summarize_stage1 (카드 값) 을 쓴다."""
        def __init__(self, melt=None, verdict=None):
            self.melt, self.verdict, self.calls = melt or {}, verdict or {}, {}
        def read_li2s2_values(self, card):
            return real.read_li2s2_values(card)
        def melt_window_check(self, rd, values=None, log=None):
            key = (rd.parent.name, int(rd.name.replace("seed", "")))
            seq = self.melt.get(key, ["incomplete", "pass"])
            i = self.calls.get(key, 0); self.calls[key] = i + 1
            v = seq[min(i, len(seq) - 1)]
            return {"verdict": v, "message": f"fake {v}", "D_framework_cm2_s": 1e-5 if v == "pass" else 1e-8}
        def stage1_verdict(self, rd, values=None, log=None):
            key = (rd.parent.name, int(rd.name.replace("seed", "")))
            res = {"status": self.verdict.get(key, "pass"), "software": {"inference": "turbo", "fairchem-core": "2.21.0"},
                   "system": key[0], "seed": key[1], "reasons": {}}
            (rd / "stage1_verdict.json").write_text(json.dumps(res), encoding="utf-8")
            return res
        def stage1_summary(self, root, values=None, log=None):
            ver = {}
            for s in ("A", "B"):
                for sd in values["seeds"]:
                    p = pathlib.Path(root) / s / f"seed{sd}" / "stage1_verdict.json"
                    ver[(s, sd)] = json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None
            res = real.summarize_stage1(ver, values)
            (pathlib.Path(root) / "stage1_summary.json").write_text(json.dumps(res, ensure_ascii=False), encoding="utf-8")
            return res

    class FakeProc:
        def __init__(self, cmd, log_path, polls=3, rc=0, launched=None):
            self.cmd, self.left, self._rc, self.stopped = cmd, polls, rc, False
            out = pathlib.Path(cmd[cmd.index("--out_root") + 1]) / cmd[cmd.index("--system") + 1] / f"seed{cmd[cmd.index('--seed') + 1]}"
            out.mkdir(parents=True, exist_ok=True)
            if launched is not None:
                launched.append(self)
        def poll(self):
            if self.stopped:
                return -15
            if self.left > 0:
                self.left -= 1; return None
            return self._rc
        def stop(self, grace_s=60):
            self.stopped = True; return -15
        @property
        def returncode(self):
            return -15 if self.stopped else self._rc

    def mk_wt(state="active", driver_txt="# fake driver\n"):
        td = pathlib.Path(tempfile.mkdtemp())
        (td / "db/governance").mkdir(parents=True); (td / "db/properties").mkdir(parents=True); (td / "tools/ionic").mkdir(parents=True)
        (td / "db/governance/decisions.json").write_text(json.dumps({"decisions": [{"id": DECISION, "decision_state": state}]}), encoding="utf-8")
        (td / CARD_REL).write_text((repo / CARD_REL).read_text(encoding="utf-8"), encoding="utf-8")
        (td / DRIVER_REL).write_text(driver_txt, encoding="utf-8")
        return td

    def go(wt, mq, polls=None, rcs=None, gpu=None, cap_h=230.0, order=DEFAULT_ORDER, expect=None):
        launched, clock = [], [0.0]
        def launch(cmd, lp):
            key = (cmd[cmd.index("--system") + 1], int(cmd[cmd.index("--seed") + 1]))
            return FakeProc(cmd, lp, polls=(polls or {}).get(key, 3), rc=(rcs or {}).get(key, 0), launched=launched)
        gq = list(gpu or [])
        def gpu_used():
            return gq.pop(0) if gq else 100
        def sleep(s):
            clock[0] += s
        rr = pathlib.Path(tempfile.mkdtemp())
        a = argparse.Namespace(worktree=str(wt), run_root=str(rr), python="python3", cap_h=cap_h, seed_worst_h=21.0,
                               poll_s=3600.0, gpu_poll_s=60.0, start_max_mib=2000, order=order,
                               expect_sha=expect or sha16(pathlib.Path(wt) / DRIVER_REL))
        rc = run(a, {"mq": mq, "launch": launch, "gpu_used": gpu_used, "sleep": sleep, "clock": lambda: clock[0]})
        return rc, launched, rr

    wt = mk_wt()
    rc, L, rr = go(wt, FakeMQ())
    sm = json.loads((rr / "stage1_summary.json").read_text(encoding="utf-8"))
    chk(rc == 0 and len(L) == 10 and [(p.cmd[p.cmd.index("--system") + 1], p.cmd[p.cmd.index("--seed") + 1]) for p in L][:3]
        == [("A", "11"), ("B", "11"), ("A", "12")] and sm["stage2"]["seeds"] == [11, 12],
        f"모두 통과: 10 담금질 · A/B 번갈아 · 1 단계 통과 · 2 단계 시드 {sm['stage2']['seeds']} (rc {rc})")
    c0 = L[0].cmd
    chk(c0[c0.index("--fix_density") + 1] == "1.91347" and L[1].cmd[L[1].cmd.index("--fix_density") + 1] == "1.88"
        and c0[c0.index("--compress_ps") + 1] == "20" and "--turbo" in c0 and c0[c0.index("--n_fu") + 1] == "12",
        "담금질 명령: 카드 값 (A 1.91347 · B 1.88 · 압축 20 ps · turbo · n_fu 12/15) 그대로")
    mq2 = FakeMQ(melt={("A", 11): ["incomplete", "fail"]})
    rc, L, rr = go(wt, mq2, polls={("A", 11): 5})
    st = json.loads((rr / "STOP.json").read_text(encoding="utf-8"))
    chk(rc == RC["melt"] and len(L) == 1 and L[0].stopped and st["code"] == "melt"
        and json.loads((rr / "A/seed11/stage1_verdict.json").read_text(encoding="utf-8"))["status"] == "fail",
        "⛔음성 DF Q-DF-3: A11 녹음 미충족 → 그 담금질을 실제로 멈추고 뒤 시드를 안 띄운다 (트랙 멈춤 21)")
    rc, L, rr = go(wt, FakeMQ(melt={("B", 11): ["invalid"]}), polls={("B", 11): 5})
    chk(rc == RC["melt"] and len(L) == 2 and L[1].stopped and not L[0].stopped, "⛔음성: B11 녹음 무효 → B11 을 멈추고 트랙 멈춤 (A11 은 끝까지)")
    rc, L, rr = go(wt, FakeMQ(melt={("A", 12): ["fail"]}), polls={("A", 12): 5})
    chk(rc == 0 and len(L) == 10 and not any(p.stopped for p in L), "첫 시드가 아닌 A12 는 담금질 중 녹음 판정으로 멈추지 않는다 (판정은 끝난 뒤 stage1_verdict)")
    rc, L, rr = go(wt, FakeMQ(verdict={("A", 12): "fail", ("A", 13): "fail"}))
    chk(rc == RC["track"] and len(L) == 5 and json.loads((rr / "STOP.json").read_text(encoding="utf-8"))["summary"]["track"] == "stop_track",
        "⛔음성 DF P1-3: A 탈락이 둘이 되는 순간 (A13 뒤) 트랙 멈춤 — B 가 통과 중이어도")
    rc, L, rr = go(wt, FakeMQ(verdict={("A", 11): "fail"}))
    sm = json.loads((rr / "stage1_summary.json").read_text(encoding="utf-8"))
    chk(rc == 0 and sm["stage2"]["seeds"] == [12, 13], f"A11 만 탈락 → 4/5 로 통과 · 2 단계 시드 = 공통 통과 중 작은 둘 {sm['stage2']['seeds']}")
    rc, L, rr = go(wt, FakeMQ(), rcs={("B", 12): 137})
    chk(rc == RC["abnormal"] and len(L) == 4, "⛔음성: B12 담금질 rc 137 (비정상) → 멈춤 (뒤 시드 안 띄움)")
    rc, L, rr = go(wt, FakeMQ(), polls={k: 10 for k in [("A", 11), ("B", 11)]}, cap_h=40.0)
    chk(rc == RC["cap"] and len(L) == 2 and json.loads((rr / "STOP.json").read_text(encoding="utf-8"))["code"] == "cap",
        "⛔음성 DF P1-6: 누적 벽시계 + 최악 > 상한이면 새 시드를 안 띄우고 '미완결' 로 멈춤")
    rc, L, rr = go(mk_wt(state="proposed"), FakeMQ())
    chk(rc == RC["refused"] and not L, "⛔음성: 결정이 proposed 면 시작하지 않는다")
    rc, L, rr = go(wt, FakeMQ(), expect="0000000000000000")
    chk(rc == RC["refused"] and not L, "⛔음성: 드라이버 sha16 이 고정값과 다르면 시작하지 않는다")
    rr0 = pathlib.Path(tempfile.mkdtemp()); (rr0 / "A/seed11").mkdir(parents=True)
    a = argparse.Namespace(worktree=str(wt), run_root=str(rr0), python="python3", cap_h=230.0, seed_worst_h=21.0, poll_s=1.0,
                           gpu_poll_s=1.0, start_max_mib=2000, order=DEFAULT_ORDER, expect_sha=sha16(wt / DRIVER_REL))
    launched = []
    rc = run(a, {"mq": FakeMQ(), "launch": lambda c, lp: FakeProc(c, lp, launched=launched), "gpu_used": lambda: 100,
                 "sleep": lambda s: None, "clock": time.time})
    chk(rc == RC["resume"] and not launched, "⛔음성: 판정 없이 런 폴더만 있으면 (끊긴 런) 덮어쓰지 않고 멈춘다")
    (rr0 / "A/seed11/stage1_verdict.json").write_text(json.dumps({"status": "pass", "software": {"inference": "turbo", "fairchem-core": "2.21.0"}}))
    launched = []
    rc = run(a, {"mq": FakeMQ(), "launch": lambda c, lp: FakeProc(c, lp, polls=1, launched=launched), "gpu_used": lambda: 100,
                 "sleep": lambda s: None, "clock": time.time})
    chk(rc == 0 and len(launched) == 9, "판정 파일이 있는 시드는 건너뛰고 이어 간다 (9 담금질)")
    (rr0 / "stage1.lock").write_text(str(os.getppid()))
    rc = run(a, {"mq": FakeMQ(), "launch": lambda c, lp: FakeProc(c, lp), "gpu_used": lambda: 100, "sleep": lambda s: None, "clock": time.time})
    chk(rc == RC["refused"], "⛔음성: 같은 run_root 에 살아 있는 러너 (잠금) 가 있으면 시작하지 않는다")
    (rr0 / "stage1.lock").unlink()
    rc, L, rr = go(wt, FakeMQ(), gpu=[9000, 9000, 1500, 9000, 1500, 1500])
    log_txt = (rr / "stage1.log").read_text(encoding="utf-8")
    chk(rc == 0 and len(L) == 10 and "비기를 기다린다" in log_txt, "GPU 가 찰 때는 두 번 연속 빌 때까지 기다린 뒤 띄운다")
    print(f"li2s2_stage1_runner selftest: ⭕ {ok} · ⛔ {bad}")
    return 0 if bad == 0 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--worktree", help="이 카드를 담은 커밋의 git worktree (도구 · 카드 · 결정 원장을 여기서 읽는다)")
    ap.add_argument("--run_root", help="담금질 출력 루트 → <run_root>/<A|B>/seed<S>/")
    ap.add_argument("--python", default=sys.executable, help="담금질을 돌릴 python (uma env 절대경로)")
    ap.add_argument("--order", default=DEFAULT_ORDER)
    ap.add_argument("--cap_h", type=float, default=230.0, help="1 단계 상한 (GPU 벽시계 h · 카드 §4c)")
    ap.add_argument("--seed_worst_h", type=float, default=21.0, help="관측이 없을 때 한 시드 최악 (카드 견적 상단)")
    ap.add_argument("--poll_s", type=float, default=300.0, help="첫 시드 녹음 판정을 볼 간격")
    ap.add_argument("--gpu_poll_s", type=float, default=60.0)
    ap.add_argument("--start_max_mib", type=int, default=2000, help="이 이하가 두 번 연속이면 띄운다")
    ap.add_argument("--expect_sha", default=EXPECTED_DRIVER_SHA16)
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if not (a.worktree and a.run_root):
        ap.error("--worktree · --run_root 가 필요하다")
    return run(a)


if __name__ == "__main__":
    sys.exit(main())
