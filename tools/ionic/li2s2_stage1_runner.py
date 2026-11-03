#!/usr/bin/env python3
"""li2s2_stage1_runner.py — li2s-2 카드 1 단계 (고정 밀도 담금질 10 개 · kgy 한 기계 · 한 번에 하나) 실행기.

카드 : db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json (§1b · §4 S1 · 기계_판독_값)
결정 : D-2026-11-03-li2s2-dense-window — **active 가 아니면 시작하지 않는다**
회신 DF: P1-2 (판정은 --stage1_verdict 의 필드 · 종료코드를 합치지 않는다) · P1-3 (한쪽 계가 닫히면 트랙 전체 멈춤)
         Q-DF-3 (첫 시드의 100 ps 녹음 판정이 그 담금질과 뒤 시드를 **실제로** 멈춘다)
회신 DG (2026-11-03 NO-GO → 고침):
  P0-1 트랙을 닫는 사건은 **재시작에도 남는다** — 세 겹: STOP.json (닫는 사건은 --ack_stop 으로도 못 넘긴다) · 장부의
       closes_system · 판정 파일의 closes_system (묶음 판정이 그 계를 닫는다 — STOP · 장부를 지워도)
  P0-2 어떤 탈출 경로 (예외 · Ctrl-C · SIGTERM · SIGHUP) 에서도 살아 있는 자기 담금질 (자기 프로세스 그룹) 을 멈추고 기다린 뒤
       장부 (경과 비용) · STOP (사유) 을 쓰고 **그 다음에** 잠금을 푼다 · 시작 직후 파일이 없으면 '미완' 으로 기다린다 ·
       담금질을 띄운 **직후** 장부에 적고 poll 마다 heartbeat (러너가 SIGKILL 로 죽어도 시작 사실 · 경과가 남는다)
  P0-3 상한 = 카드 `stage1_cap_gpu_h` (CLI 로 못 바꾼다) · **실행 중에도** (누적 + 이 런 경과) ≥ 상한이면 그 담금질을 멈추고 미완결 ·
       끝난 뒤 넘었으면 통과로 올리지 않는다 · 묶음 판정도 장부로 상한을 다시 잰다 · 관측 최댓값은 착수 판단용 예상치일 뿐
  P1-4 재시작 때 판정 파일을 믿지 않고 **원자료로 다시 판정** (stage1_verdict) · 묶음 판정은 지문 (원자료 · 카드 값 · 도구) 을 다시 잰다
  P1-6 잠금 = flock (한 번의 시스템 호출 · 러너 수명 동안 보유 · 러너가 죽으면 커널이 푼다)

하는 일 (순서 A11 → B11 → A12 → B12 → … → B15 · 계를 번갈아):
  ① 시작 전: 결정 active · 드라이버 sha16 = 고정값 · 카드 값 (드라이버 검사 통과) · 순서 = 카드 시드 전부 · 첫 시드 = 카드 first_seed ·
     잠금 · STOP.json (닫는 사건이면 거부 · 아니면 --ack_stop <stop_id> 가 있어야 이어감) · 장부의 도는 중 런 (프로세스 그룹이
     살아 있으면 거부 · 죽었으면 고아 런으로 비용 어림 마감) · 장부의 closes_system · 판정 파일 다시 판정 → 묶음 판정 (멈춤이면 거부)
  ② 시드마다: 판정이 pass · fail 이면 건너뜀 · 판정이 미완 · 무효거나 판정 없이 런 폴더만 있으면 **멈춤** (끊긴 런을 덮어쓰지 않는다)
  ③ 상한: 누적 + 한 시드 최악 (관측 최댓값 · 없으면 --seed_worst_h) > 상한이면 새 시드를 안 띄우고 미완결로 멈춤 ·
     실행 중 poll 마다 누적 + 경과 ≥ 상한이면 그 담금질을 멈추고 미완결
  ④ GPU 가 빌 때까지 기다린다 (memory.used ≤ --start_max_mib 두 번 연속 — cascade 가 끝나면 열린다)
  ⑤ 담금질을 띄운다 (카드 기계값에서 만든 명령 · --print_cmd 로 미리 볼 수 있다) — 계의 **첫 시드**면 --poll_s 마다
     melt_window_check: 미충족 · 무효 → 그 담금질을 멈추고 stage1_verdict (그 계를 닫는 사건) · STOP (닫는 사건) · 미완 → 계속 본다
  ⑥ 담금질 rc 0 → stage1_verdict → stage1_summary → 멈춤이면 멈춤 · rc ≠ 0 → 멈춤 (비정상 종료 · 사용자 결정)
  ⑦ 장부 stage1_ledger.json (시드마다 시작 · heartbeat · 끝 · 벽시계 · rc · 판정 · closes_system · STOP 이력) · 로그 stage1.log

종료코드: 0 1 단계 통과 (2 단계 시드는 stage1_summary.json) · 10 거부 (결정 · sha · 잠금 · 카드 · 순서 · 살아 있는 이전 담금질 · ack)
         20 트랙 멈춤 (묶음 판정) · 21 첫 시드 녹음 미충족 · 무효 (그 계를 닫음) · 22 상한 · 미완결 · 23 담금질 비정상 종료 ·
         24 끊긴 런 폴더 · 25 끝났는데 묶음이 대기 · 26 러너 중단 (예외 · Ctrl-C · 신호 — 담금질은 멈췄다)

⛔ 이 도구가 못 하는 것
  · GPU 를 다른 잡과 나눠 쓰는지 프로세스별로 못 본다 (kgy 는 프로세스 정보가 막혀 있다) — 총 사용량으로만 기다린다
  · 끊긴 시드를 이어 돌리지 않는다 · 2 단계를 띄우지 않는다 (묶음 판정과 2 단계 시드만 적는다)
  · 러너를 다시 띄우면 돌던 담금질을 넘겨받지 않는다 — 러너가 끝날 때 자기 담금질을 멈춘다 (그 시드는 사람이 정한다)
  · 러너가 SIGKILL 로 죽으면 담금질 (자기 세션) 은 산다 — 재시작이 그 프로세스 그룹이 살아 있는 동안 거부하고, 죽은 뒤엔
    마지막 heartbeat 와 폴더 파일 시각으로 비용을 **어림**한다 (정확한 벽시계가 아니다)
  · 판정 자체는 하지 않는다 — melt_quench_uma.py 의 melt_window_check · stage1_verdict · stage1_summary 를 부른다 (같은 worktree · sha 고정)
  · flock 은 같은 기계의 로컬 파일시스템에서만 믿는다 (NFS 너머 두 기계의 동시 실행은 못 막는다)

  python3 tools/ionic/li2s2_stage1_runner.py --worktree ~/wt_li2s2 --run_root ~/work/runs/li2s2_dense_1103 \\
          --python /home/kgy/apps/miniforge3/envs/uma/bin/python
  python3 tools/ionic/li2s2_stage1_runner.py --worktree ~/wt_li2s2 --run_root … --print_cmd A:11   # 손 실행 명령 (기계값에서)
  python3 tools/ionic/li2s2_stage1_runner.py --selftest
"""
from __future__ import annotations
import argparse, datetime, hashlib, importlib.util, json, os, pathlib, shlex, shutil, signal, subprocess, sys, tempfile, threading, time, traceback

EXPECTED_DRIVER_SHA16 = "615445c9e0f54710"     # tools/ionic/melt_quench_uma.py — 바뀌면 이 줄도 같이 바꾸고 다시 리뷰한다
DECISION = "D-2026-11-03-li2s2-dense-window"
CARD_REL = "db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json"
DRIVER_REL = "tools/ionic/melt_quench_uma.py"
SYSTEMS = ("A", "B")
DEFAULT_ORDER = "A:11,B:11,A:12,B:12,A:13,B:13,A:14,B:14,A:15,B:15"
RC = {"pass": 0, "refused": 10, "track": 20, "melt": 21, "cap": 22, "abnormal": 23, "resume": 24, "pending": 25, "interrupted": 26}
TERMINAL_STOPS = ("melt", "track")       # --ack_stop 으로 못 넘긴다 — 그 계 · 트랙은 카드 규칙으로 닫혔다 (새 카드 · 새 run_root)


class _RunnerSignal(BaseException):
    """SIGTERM · SIGHUP 을 예외로 — except Exception 에 안 먹히고 정리 경로 (자식 멈춤 · 장부 · STOP · 잠금) 를 탄다."""


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
        if sysn not in SYSTEMS:
            raise ValueError(f"순서에 모르는 계 {sysn}")
        out.append((sysn, int(seed)))
    return out


def check_order(order, vals):
    """순서 = 카드 시드 × 두 계 **전부 · 한 번씩** · 계마다 첫 시드 = 카드 first_seed (첫 시드 녹음 판정의 '첫' 을 카드가 정한다)."""
    why = []
    want = {(s, sd) for s in SYSTEMS for sd in vals["seeds"]}
    if len(order) != len(set(order)):
        why.append("순서에 같은 (계, 시드) 가 두 번 있다")
    if set(order) != want:
        why.append(f"순서가 카드 시드 전부가 아니다 (빠짐 {sorted(want - set(order))} · 남음 {sorted(set(order) - want)})")
    for s in SYSTEMS:
        firsts = [sd for (x, sd) in order if x == s][:1]
        if firsts != [vals["first_seed"]]:
            why.append(f"{s} 의 첫 시드 {firsts} ≠ 카드 first_seed {vals['first_seed']}")
    return why


def _num(x):
    """명령줄 숫자 — 반올림 없이 (repr) · 정수값은 정수로. %g 는 여섯 자리에서 잘라 카드 값과 어긋날 수 있다 (회신 DG P2)."""
    x = float(x)
    return str(int(x)) if x.is_integer() and abs(x) < 1e15 else repr(x)


def build_cmd(python, worktree, run_root, sysn, seed, vals, mq):
    """담금질 명령 — **카드 기계값에서만** 만든다 (손 실행도 --print_cmd 로 같은 명령을 쓴다 · 회신 DG P2)."""
    sched, comp = vals["schedule"], vals["composition"][sysn]
    form, _ = mq.SYSTEMS[sysn]
    n_fu = comp.get("P")
    if not n_fu or {e: n * n_fu for e, n in form.items() if n} != comp:
        raise ValueError(f"카드 조성 {comp} 가 드라이버 식단위 {form} × n_fu 와 안 맞는다")
    return [python, str(pathlib.Path(worktree) / DRIVER_REL), "--system", sysn, "--n_fu", str(n_fu), "--seed", str(int(seed)),
            "--T_melt", _num(sched["T_melt_K"]), "--T_final", _num(sched["T_final_K"]), "--melt_ps", _num(sched["melt_ps"]),
            "--quench_rate", _num(sched["quench_rate_K_s"]), "--hold_ps", _num(sched["hold_ps"]), "--dt_fs", _num(sched["dt_fs"]),
            "--save_ps", _num(sched["save_ps"]), "--turbo", "--fix_density", _num(vals["fix_density_g_cm3"][sysn]),
            "--compress_ps", _num(sched["compress_ps"]), "--out_root", str(run_root)]


class _Proc:
    """subprocess.Popen 감싸개 — 시험에서 같은 모양의 가짜로 바꾼다. 자기 세션 (start_new_session) = 자기 프로세스 그룹."""
    def __init__(self, cmd, log_path):
        self.fh = open(log_path, "a")
        self.p = subprocess.Popen(cmd, stdout=self.fh, stderr=subprocess.STDOUT, start_new_session=True)
    @property
    def pid(self):
        return self.p.pid
    def poll(self):
        rc = self.p.poll()
        if rc is not None and not self.fh.closed:
            self.fh.close()
        return rc
    def stop(self, grace_s=60):
        """그 담금질만 (자기 프로세스 그룹) 멈추고 **기다린다** — 이름으로 잡지 않는다 (CLAUDE.md pkill 금지)."""
        try:
            os.killpg(self.p.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        t0 = time.time()
        while self.p.poll() is None and time.time() - t0 < grace_s:
            time.sleep(1)
        if self.p.poll() is None:
            try:
                os.killpg(self.p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            self.p.wait()
        if not self.fh.closed:
            self.fh.close()
        return self.p.returncode
    @property
    def returncode(self):
        return self.p.returncode


def _pg_alive(pgid):
    try:
        os.killpg(int(pgid), 0); return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except Exception:
        return False


def _gpu_used_mib():
    out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                         capture_output=True, text=True, check=True).stdout
    return int(out.split()[0])


class _Lock:
    """한 run_root 에 러너 하나 — flock (원자적 · 수명 동안 보유 · 프로세스가 죽으면 커널이 푼다 · 회신 DG P1-6).
    fcntl 이 없는 OS 는 O_CREAT|O_EXCL 로 (그때는 낡은 잠금 파일을 사람이 지운다)."""
    def __init__(self, path):
        self.path, self.fd, self.kind = pathlib.Path(path), None, None
    def acquire(self):
        try:
            import fcntl
        except ImportError:
            try:
                self.fd = os.open(str(self.path) + ".excl", os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
            except FileExistsError:
                return False
            os.write(self.fd, f"{os.getpid()}\n".encode()); self.kind = "excl"
            return True
        fd = os.open(str(self.path), os.O_RDWR | os.O_CREAT, 0o644)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            os.close(fd)
            return False
        os.ftruncate(fd, 0); os.write(fd, f"{os.getpid()}\n".encode())
        self.fd, self.kind = fd, "flock"
        return True
    def release(self):
        if self.fd is None:
            return
        if self.kind == "flock":
            import fcntl
            fcntl.flock(self.fd, fcntl.LOCK_UN); os.close(self.fd)
        else:
            os.close(self.fd)
            try:
                os.unlink(str(self.path) + ".excl")
            except FileNotFoundError:
                pass
        self.fd = None


def _write_json_atomic(path, obj):
    path = pathlib.Path(path)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    os.replace(tmp, path)


def run(a, deps=None):
    deps = deps or {}
    W, R = pathlib.Path(a.worktree), pathlib.Path(a.run_root)
    R.mkdir(parents=True, exist_ok=True)
    sleep, clock, wall = deps.get("sleep", time.sleep), deps.get("clock", time.time), deps.get("wall", time.time)
    gpu_used, launch, pg_alive = deps.get("gpu_used", _gpu_used_mib), deps.get("launch", _Proc), deps.get("pg_alive", _pg_alive)
    logf = open(R / "stage1.log", "a")
    def log(*m):
        line = f"[{_now()}] " + " ".join(str(x) for x in m)
        print(line, flush=True); logf.write(line + "\n"); logf.flush()
    led_p, stop_p = R / "stage1_ledger.json", R / "STOP.json"
    state = {"h": None, "entry": None, "t0": None, "ledger": None, "stopped": False}
    def save_ledger():
        if state["ledger"] is not None:
            _write_json_atomic(led_p, state["ledger"])
    def stop(code, reason, **detail):
        rec = {"at": _now(), "code": code, "reason": reason, "terminal": code in TERMINAL_STOPS, **detail}
        rec["stop_id"] = hashlib.sha256(json.dumps(rec, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()[:16]
        _write_json_atomic(stop_p, rec)
        state["stopped"] = True
        log(f"⛔ 멈춤 ({code}) — {reason} · stop_id {rec['stop_id']}")
        return RC[code]
    def finish(ent, rc, status, wall_h):
        ent.update(end=_now(), wall_h=wall_h, rc=rc, status=status)
        state["entry"] = None
        save_ledger()
    def cost_so_far():
        return sum(float(r["wall_h"] if r.get("wall_h") is not None else (r.get("wall_h_so_far") or 0.0))
                   for r in state["ledger"]["runs"])
    def stop_child(why):
        """살아 있는 자기 담금질을 멈추고 기다린다 — 어떤 탈출 경로에서도 (회신 DG P0-2)."""
        h = state["h"]
        if h is None:
            return None
        try:
            alive = h.poll() is None
        except BaseException:
            alive = True
        rc_ = None
        if alive:
            log(f"  ⚠ {why} — 돌던 담금질 (프로세스 그룹 {getattr(h, 'pid', '?')}) 을 멈추고 기다린다")
            rc_ = h.stop()
        state["h"] = None
        return rc_

    # ① 시작 전 점검 (부작용 없음)
    st = decision_state(W)
    if st != "active":
        log(f"⛔ 결정 {DECISION} 이 active 가 아니다 ({st}) — 시작하지 않는다"); logf.close(); return RC["refused"]
    s16 = sha16(W / DRIVER_REL)
    if s16 != a.expect_sha:
        log(f"⛔ 드라이버 sha16 {s16} ≠ 고정값 {a.expect_sha} — 시작하지 않는다"); logf.close(); return RC["refused"]
    mq = deps.get("mq") or load_mq(W)
    try:
        vals = mq.read_li2s2_values(W / CARD_REL)
        order = parse_order(a.order)
        bad = check_order(order, vals)
        if bad:
            raise ValueError(" · ".join(bad))
        for s in SYSTEMS:
            build_cmd(a.python, W, R, s, vals["first_seed"], vals, mq)
    except Exception as e:
        log(f"⛔ 카드 값 · 순서를 못 받았다 ({type(e).__name__}: {e}) — 시작하지 않는다"); logf.close(); return RC["refused"]
    cap = float(vals["stage1_cap_gpu_h"])
    lock = _Lock(R / "stage1.lock")
    if not lock.acquire():
        log("⛔ 같은 run_root 로 러너가 이미 잠금을 잡고 있다 — 시작하지 않는다"); logf.close(); return RC["refused"]
    old = {}
    if threading.current_thread() is threading.main_thread():
        def _raise_sig(signum, frame):
            raise _RunnerSignal(f"신호 {signal.Signals(signum).name}")
        for sg in (signal.SIGTERM, signal.SIGHUP):
            old[sg] = signal.signal(sg, _raise_sig)
    try:
        state["ledger"] = (json.loads(led_p.read_text(encoding="utf-8")) if led_p.is_file() else {"runs": []})
        led = state["ledger"]
        led.setdefault("runs", []); led.setdefault("stop_history", [])
        led.update({"decision": DECISION, "driver_sha16": s16, "card": CARD_REL, "cap_h": cap,
                    "card_values_sha16": mq.values_sha16(vals)})
        # ①-1 STOP.json — 닫는 사건은 넘기지 않는다 · 나머지는 사람이 stop_id 로 확인해야 이어간다 (회신 DG P0-1)
        if stop_p.is_file():
            sp = json.loads(stop_p.read_text(encoding="utf-8"))
            code = sp.get("code")
            if code in TERMINAL_STOPS:
                log(f"⛔ 이 run_root 는 닫혔다 ({code} · {sp.get('reason')}) — 재시작으로 다시 열지 않는다 (새 카드 · 새 run_root)")
                return RC.get(code, RC["refused"])
            if a.ack_stop != sp.get("stop_id"):
                log(f"⛔ 앞선 멈춤이 남아 있다 ({code} · {sp.get('reason')}) — 확인했으면 --ack_stop {sp.get('stop_id')}")
                return RC.get(code, RC["refused"])
            if code == "cap" and not (cap > float(sp.get("cap_h", cap)) + 1e-9):
                log(f"⛔ 상한 멈춤은 카드 상한이 올라갔을 때만 넘긴다 (멈춤 {sp.get('cap_h')} · 지금 {cap} — 바꾸려면 결정 · 카드 개정)")
                return RC["cap"]
            led["stop_history"].append({**sp, "acked_at": _now()})
            stop_p.unlink()
            save_ledger()
            log(f"  앞선 멈춤 {code} (stop_id {sp.get('stop_id')}) 확인 — 장부 stop_history 로 옮기고 이어간다")
        # ①-2 장부의 도는 중 런 — 살아 있으면 거부 · 죽었으면 고아 런으로 마감 (비용 어림)
        for ent in led["runs"]:
            if ent.get("end") is None:
                pg = ent.get("pgid")
                if pg is not None and pg_alive(pg):
                    log(f"⛔ 장부의 {ent['system']}{ent['seed']} 담금질 (프로세스 그룹 {pg}) 이 아직 살아 있다 — 시작하지 않는다")
                    return RC["refused"]
                rd = R / ent["system"] / f"seed{ent['seed']}"
                mt = max((f.stat().st_mtime for f in rd.iterdir() if f.is_file()), default=None) if rd.is_dir() else None
                est = float(ent.get("wall_h_so_far") or 0.0)
                if mt is not None and ent.get("start_epoch") is not None:
                    est = max(est, (mt - float(ent["start_epoch"])) / 3600.0)
                ent.update(end=_now(), wall_h=est, rc="unknown_runner_died", status="orphaned",
                           wall_h_basis="어림 = max(마지막 heartbeat 경과, 폴더 파일 마지막 시각 − 시작)")
                save_ledger()
                log(f"  ⚠ 장부의 {ent['system']}{ent['seed']} 는 러너가 죽어 끝이 안 적혔다 — 고아 런 · 비용 어림 {est:.2f} h")
        # ①-3 장부에 그 계를 닫은 사건이 있으면 거부 (STOP 을 지워도)
        closed = [f"{r['system']}{r['seed']}" for r in led["runs"] if r.get("closes_system")]
        if closed:
            return stop("melt", f"장부에 계를 닫은 사건이 있다 ({closed} · 첫 시드 녹음 미충족) — 재시작으로 다시 열지 않는다")
        # ①-4 판정 파일을 믿지 않는다 — 원자료로 다시 판정 → 묶음 판정 (회신 DG P1-4)
        for sysn, seed in order:
            rd = R / sysn / f"seed{seed}"
            if (rd / "stage1_verdict.json").is_file():
                was = json.loads((rd / "stage1_verdict.json").read_text(encoding="utf-8")).get("status")
                now_ = mq.stage1_verdict(rd, values=vals, log=lambda *m: None)
                log(f"  {sysn}{seed}: 판정 다시 냄 {was} → {now_.get('status')}" + (" ⚠ 바뀜" if was != now_.get("status") else ""))
        sm = mq.stage1_summary(R, values=vals, log=log)
        if sm["track"] in ("stop_track", "invalid"):
            return stop("track", f"시작 전 묶음 판정 {sm['track']} — {sm.get('why')}", summary=sm)
        if sm["track"] == "cap_incomplete":
            return stop("cap", f"시작 전 묶음 판정 상한 · 미완결 — {sm.get('why')}", cap_h=cap, summary=sm)
        if sm["track"] == "stage1_pass":
            log(f"✅ 이미 1 단계 통과 — 2 단계 시드 {sm['stage2']['seeds']} · 기계 {sm['stage2']['machines']}")
            return RC["pass"]
        log(f"▶ 시작 · sha16 {s16} · 결정 {DECISION} active · 순서 {a.order} · 상한 {cap:g} h (카드) · 누적 {cost_so_far():.2f} h")
        for sysn, seed in order:
            rd = R / sysn / f"seed{seed}"
            vf = rd / "stage1_verdict.json"
            if vf.is_file():
                sv = json.loads(vf.read_text(encoding="utf-8")).get("status")
                if sv in ("pass", "fail"):
                    log(f"  {sysn}{seed}: 판정 {sv} — 건너뜀"); continue
                return stop("resume", f"{sysn}{seed} 판정이 {sv} — 끝나지 않은 런 폴더 (덮어쓰지 않는다 · 사람이 정한다)", sys=sysn, seed=seed)
            if rd.exists():
                return stop("resume", f"{sysn}{seed} 런 폴더가 판정 없이 있다 — 끊긴 런을 덮어쓰지 않는다 (사람이 정한다)", sys=sysn, seed=seed)
            walls = [float(r["wall_h"]) for r in led["runs"] if r.get("wall_h") is not None and r.get("status") == "ended"]
            cum, worst = cost_so_far(), max(walls + [a.seed_worst_h])
            if cum + worst > cap:
                return stop("cap", f"누적 {cum:.1f} h + 한 시드 최악 {worst:.1f} h > 상한 {cap:g} h — 미완결로 멈춤 (끝난 시드만 골라 판정하지 않는다)",
                            cum_h=cum, worst_h=worst, cap_h=cap)
            ok_n, t_wait = 0, clock()
            while ok_n < 2:
                u = gpu_used()
                ok_n = ok_n + 1 if u <= a.start_max_mib else 0
                if ok_n < 2:
                    if u > a.start_max_mib and (clock() - t_wait) % 1800 < a.gpu_poll_s:
                        log(f"  GPU {u} MiB > {a.start_max_mib} — 비기를 기다린다")
                    sleep(a.gpu_poll_s)
            cmd = build_cmd(a.python, W, R, sysn, seed, vals, mq)
            t0 = clock()
            log(f"▶ {sysn}{seed} 담금질 — " + " ".join(cmd[2:]))
            h = launch(cmd, R / f"quench_{sysn}{seed}.log")
            state["h"], state["t0"] = h, t0
            ent = {"system": sysn, "seed": seed, "start": _now(), "start_epoch": wall(), "pgid": getattr(h, "pid", None),
                   "status": "running", "end": None, "wall_h": None, "wall_h_so_far": 0.0, "cum_before_h": cum}
            led["runs"].append(ent); state["entry"] = ent
            save_ledger()                                    # ⭐ 띄운 직후 — 러너가 죽어도 시작 사실이 남는다 (회신 DG P0-2)
            need_melt = (seed == vals["first_seed"])
            while h.poll() is None:
                sleep(a.poll_s)
                el = (clock() - t0) / 3600.0
                ent["wall_h_so_far"], ent["last_seen"] = el, _now()
                save_ledger()
                if cum + el >= cap:                          # ⭐ 실행 중 상한 (회신 DG P0-3)
                    stop_child(f"상한 도달 (누적 {cum:.1f} + 경과 {el:.1f} ≥ {cap:g} h)")
                    finish(ent, "killed_cap", "cap", el)
                    try:
                        mq.stage1_verdict(rd, values=vals, log=log)      # 기록용 (판정은 미완 — 통과로 오르지 않는다)
                    except Exception as e:
                        log(f"  (기록용 판정 실패 {type(e).__name__}: {e})")
                    return stop("cap", f"{sysn}{seed} 실행 중 누적 {cum + el:.1f} h ≥ 상한 {cap:g} h — 그 담금질을 멈추고 미완결",
                                sys=sysn, seed=seed, cum_h=cum + el, cap_h=cap)
                if need_melt:
                    try:
                        mw = mq.melt_window_check(rd, values=vals, log=lambda *m: None)
                    except Exception as e:                   # 판독 예외로 러너가 죽지 않는다 — 기록하고 다음 poll 에 다시
                        ent.setdefault("melt_check_errors", []).append(f"{_now()} {type(e).__name__}: {e}")
                        save_ledger()
                        log(f"  ⚠ {sysn}{seed}: 녹음 판정 예외 ({type(e).__name__}: {e}) — 다음 poll 에 다시 (끝난 뒤 판정에서도 본다)")
                        continue
                    if mw["verdict"] in ("fail", "invalid"):
                        stop_child(f"{sysn}{seed} 첫 시드 녹음 판정 {mw['verdict']}")
                        finish(ent, "killed_melt", mw["verdict"], (clock() - t0) / 3600.0)
                        v = mq.stage1_verdict(rd, values=vals, log=log)  # 판정은 드라이버 한 곳 — 그 계를 닫는 사건 (closes_system)
                        ent["verdict"], ent["closes_system"] = v.get("status"), bool(v.get("closes_system"))
                        save_ledger()
                        return stop("melt", f"{sysn}{seed} (계의 첫 시드) 녹음 판정 {mw['verdict']} — {mw.get('message')} · "
                                            "그 계가 닫혀 트랙 전체 멈춤", sys=sysn, seed=seed, verdict=v.get("status"))
                    if mw["verdict"] == "pass":
                        need_melt = False
                        log(f"  {sysn}{seed}: 녹음 판정 통과 (D_P {mw.get('D_framework_cm2_s')}) — 담금질 계속")
            rc = h.returncode
            state["h"] = None
            el = (clock() - t0) / 3600.0
            finish(ent, rc, "ended", el)
            if rc != 0:
                return stop("abnormal", f"{sysn}{seed} 담금질 rc {rc} — 비정상 종료 (사용자 결정 · 그 계를 어떻게 할지)", sys=sysn, seed=seed, rc=rc)
            v = mq.stage1_verdict(rd, values=vals, log=log)
            ent["verdict"], ent["closes_system"] = v.get("status"), bool(v.get("closes_system"))
            save_ledger()
            if cum + el > cap:                               # 끝난 뒤에도 넘었으면 통과로 올리지 않는다 (회신 DG P0-3)
                return stop("cap", f"{sysn}{seed} 가 끝났을 때 누적 {cum + el:.1f} h > 상한 {cap:g} h — 미완결 (통과로 올리지 않는다)",
                            sys=sysn, seed=seed, cum_h=cum + el, cap_h=cap)
            sm = mq.stage1_summary(R, values=vals, log=log)
            if sm["track"] in ("stop_track", "invalid"):
                return stop("track", f"묶음 판정 {sm['track']} — {sm.get('why')}", summary=sm)
            if sm["track"] == "cap_incomplete":
                return stop("cap", f"묶음 판정 상한 · 미완결 — {sm.get('why')}", cap_h=cap, summary=sm)
        sm = mq.stage1_summary(R, values=vals, log=log)
        if sm["track"] == "stage1_pass":
            log(f"✅ 1 단계 통과 — 2 단계 시드 {sm['stage2']['seeds']} · 기계 {sm['stage2']['machines']}")
            return RC["pass"]
        if sm["track"] in ("stop_track", "invalid"):
            return stop("track", f"묶음 판정 {sm['track']} — {sm.get('why')}", summary=sm)
        if sm["track"] == "cap_incomplete":
            return stop("cap", f"묶음 판정 상한 · 미완결 — {sm.get('why')}", cap_h=cap, summary=sm)
        return stop("pending", f"순서를 다 돌았는데 묶음 판정이 {sm['track']} — 판정 파일을 확인한다", summary=sm)
    except BaseException as e:                               # 예외 · Ctrl-C · SIGTERM · SIGHUP (회신 DG P0-2)
        why = f"{type(e).__name__}: {e}"
        try:
            stop_child(f"러너 중단 ({why})")
        except BaseException as e2:
            log(f"  ⛔ 담금질 멈춤도 실패 ({type(e2).__name__}: {e2}) — 프로세스 그룹 {getattr(state['h'], 'pid', '?')} 를 손으로 본다")
        ent = state["entry"]
        if ent is not None and ent.get("end") is None:
            finish(ent, "killed_runner_exit", "interrupted", (clock() - state["t0"]) / 3600.0)
        log("  " + traceback.format_exc().strip().replace("\n", "\n  "))
        if not state["stopped"]:
            stop("interrupted", f"러너 중단 — {why} (돌던 담금질은 멈췄다 · 그 시드 폴더는 사람이 정한다)")
        return RC["interrupted"]
    finally:
        try:
            stop_child("러너가 끝난다")
        finally:
            try:
                save_ledger()
            finally:
                for sg, hd in old.items():
                    signal.signal(sg, hd)
                lock.release()
                logf.close()


# ───────────────────────── selftest ─────────────────────────
def _selftest():
    """가짜 담금질 (진짜 드라이버가 쓰는 파일을 poll 마다 조금씩 쓴다) + **진짜** 판독 함수 (melt_window_check · stage1_verdict ·
    stage1_summary · 카드 검사) — 회신 DG ④: 판독기를 가짜로 바꾸면 판독 예외 · 산출물 검증 누락을 못 본다."""
    import numpy as np
    ok = bad = 0
    def chk(c, m):
        nonlocal ok, bad
        print(("  ⭕ " if c else "  ⛔ ") + m); ok += bool(c); bad += (not c)
    repo = pathlib.Path(__file__).resolve().parents[2]
    real = load_mq(repo)
    tmp_root = pathlib.Path(tempfile.mkdtemp(prefix="li2s2_runner_st_"))
    # 시험 카드 = 진짜 카드에서 일정만 줄이고 (담금질 9 ps · 유지 20 ps) 밀도를 무작위 PS₄ 셀의 밀도로 — 그 외 값은 진짜 그대로
    card0 = json.loads((repo / CARD_REL).read_text(encoding="utf-8"))
    BASE, rho = {}, {}
    for s in SYSTEMS:
        n_fu = card0["기계_판독_값"]["composition"][s]["P"]
        sym, pos, cell = real.build_random_cell(s, seed=3, density_g_cm3=1.2, n_fu=n_fu)
        from ase import Atoms
        at = Atoms(symbols=sym, positions=pos, cell=cell, pbc=True)
        BASE[s] = (list(sym), np.asarray(pos, float), np.asarray(cell, float))
        rho[s] = real.density_g_cm3(at)
        gv = real._gate_view(at)
        chk(gv["PS4_fraction"] == 1.0 and gv["min_pair_excl_PS_A"] > 2.0, f"시험 바탕 구조 {s}: 시드 게이트 통과 ({gv['min_pair_excl_PS_A']:.3f} Å)")
    def mk_card(**over):
        c = json.loads(json.dumps(card0))
        mv = c["기계_판독_값"]
        mv["schedule"].update({"quench_rate_K_s": 1e14, "hold_ps": 20.0})
        mv["fix_density_g_cm3"] = dict(rho)
        for k, x in over.items():
            mv[k] = x
        return c
    SW = {"model": "uma-s-1p1", "task": "omat", "inference": "turbo", "fairchem-core": "2.21.0", "torch": "2.8.0", "ase": "3.26.0"}

    def _xyz(path, sym, frames, cell, mode="a"):
        lat = " ".join(f"{x:.10f}" for x in np.asarray(cell).ravel())
        with open(path, mode) as f:
            for P in frames:
                f.write(f"{len(sym)}\nLattice=\"{lat}\" Properties=species:S:1:pos:R:3 pbc=\"T T T\"\n")
                f.writelines(f"{e} {x:.8f} {y:.8f} {z:.8f}\n" for e, (x, y, z) in zip(sym, P))

    class FakeQuench:
        """진짜 드라이버가 쓰는 파일 (plan.json · thermo.csv · traj.xyz · final.xyz · result.json) 을 poll 마다 조금씩 쓴다.
        poll 1: 폴더만 (plan 없음) · 2: plan + 70 ps · 3: 100 ps (녹음 창 확보) · n_polls: 끝까지 + final · 그 다음 poll 이 rc."""
        def __init__(self, cmd, log_path, scen=None, launched=None):
            g = lambda k: cmd[cmd.index(k) + 1]
            self.cmd, self.sys, self.seed = cmd, g("--system"), int(g("--seed"))
            self.rd = pathlib.Path(g("--out_root")) / self.sys / f"seed{self.seed}"
            self.rd.mkdir(parents=True, exist_ok=True)
            self.f = {k: float(g("--" + k)) for k in ("fix_density", "compress_ps", "melt_ps", "hold_ps", "quench_rate",
                                                       "T_melt", "T_final", "save_ps", "dt_fs")}
            sc = (scen or {}).get((self.sys, self.seed), {})
            self.melt, self.final, self._rc = sc.get("melt", "pass"), sc.get("final", "ok"), sc.get("rc", 0)
            self.n_polls, self.raise_on = max(4, sc.get("polls", 5)), sc.get("raise_on_poll")
            self.k, self.stopped, self.pid, self.t_written = 0, False, 990000 + len(launched or []), -1
            self.sym, self.base, self.cell = BASE[self.sys]
            rng = np.random.default_rng(1000 * self.seed + ord(self.sys))
            step = 0.5 if self.melt == "pass" else 0.0005
            self.walk = np.cumsum(rng.normal(0, step, (51, len(self.sym), 3)), axis=0)
            self.walk -= self.walk[0]
            self.isP = np.array([e == "P" for e in self.sym])
            if launched is not None:
                launched.append(self)
        @property
        def quench_ps(self):
            return (self.f["T_melt"] - self.f["T_final"]) / self.f["quench_rate"] * 1e12
        def _pos(self, t):
            if 50 <= t <= 100:
                P = self.base.copy(); P[self.isP] += self.walk[int(round(t - 50))][self.isP]; return P
            return self.base + (0.002 if t > 100 else 0.0)
        def _write(self, t_end, final=False):
            if self.t_written < 0:
                plan = real.build_plan(self.sys, self.seed, self.sym, 1.0, self.f["T_melt"], self.f["T_final"], self.f["melt_ps"],
                                       self.f["quench_rate"], self.quench_ps, self.f["hold_ps"], self.f["dt_fs"], self.f["save_ps"],
                                       fix_density=self.f["fix_density"], compress_ps=self.f["compress_ps"])
                plan["uma_inference_mode"] = "turbo"; plan["software"] = dict(SW)
                (self.rd / "plan.json").write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
                (self.rd / "thermo.csv").write_text("t_ps,T_K,T_set_K,density_g_cm3,volume_A3,E_pot_eV,P_GPa,P_virial_GPa\n", encoding="utf-8")
            ts = [t for t in range(int(self.t_written) + 1, int(round(t_end)) + 1)]
            _xyz(self.rd / "traj.xyz", self.sym, [self._pos(t) for t in ts], self.cell)
            M, Q = self.f["melt_ps"], self.quench_ps
            with open(self.rd / "thermo.csv", "a") as fh:
                for t in ts:
                    Ts = self.f["T_melt"] if t <= M else (self.f["T_final"] if t >= M + Q else
                                                         self.f["T_melt"] - (self.f["T_melt"] - self.f["T_final"]) * (t - M) / Q)
                    d = self.f["fix_density"] if t >= self.f["compress_ps"] else 1.0 + (self.f["fix_density"] - 1.0) * t / self.f["compress_ps"]
                    fh.write(f"{t:.3f},{Ts + 3:.1f},{Ts:.1f},{d:.4f},{1000.0:.2f},{-500.0:.4f},{3.6:.4f},{3.5:.4f}\n")
            self.t_written = ts[-1] if ts else self.t_written
            if final:
                fc = self.cell.copy(); fp = self.base.copy(); fs = list(self.sym)
                if self.final == "five":
                    iP = fs.index("P"); D = np.linalg.norm(self.base - self.base[iP], axis=1)
                    idx = [iP] + [i for i in np.argsort(D) if fs[i] == "S"][:4]
                    fp, fs = self.base[idx], [fs[i] for i in idx]
                elif self.final == "dense":
                    fc = self.cell * 0.98; fp = self.base * 0.98
                elif self.final == "ps4_broken":
                    iP = fs.index("P"); D = np.linalg.norm(self.base - self.base[iP], axis=1)
                    iS = [i for i in np.argsort(D) if fs[i] == "S"][0]
                    u = (self.base[iS] - self.base[iP]); fp = self.base.copy(); fp[iS] = self.base[iP] + u / np.linalg.norm(u) * 2.95
                _xyz(self.rd / "final.xyz", fs, [fp], fc, mode="w")
                (self.rd / "result.json").write_text(json.dumps({"files": ["traj.xyz", "thermo.csv", "final.xyz"]}), encoding="utf-8")
        def poll(self):
            if self.stopped:
                return -15
            self.k += 1
            if self.k == 1:                                   # 띄운 직후 — 장부에 시작이 이미 디스크에 있나 (회신 DG P0-2)
                lp = self.rd.parent.parent / "stage1_ledger.json"
                led_ = json.loads(lp.read_text(encoding="utf-8")) if lp.is_file() else {"runs": []}
                self.ledger_at_first_poll = any(r.get("system") == self.sys and r.get("seed") == self.seed and r.get("end") is None
                                                for r in led_.get("runs", []))
            if self.raise_on == self.k:
                raise KeyboardInterrupt("시험: poll 중 Ctrl-C")
            if self.k == 2:
                self._write(70.0)
            elif self.k == 3:
                self._write(100.0)
            elif self.k == self.n_polls:
                self._write(self.f["melt_ps"] + self.quench_ps + self.f["hold_ps"], final=True)
            return None if self.k <= self.n_polls else self._rc
        def stop(self, grace_s=60):
            self.stopped = True; return -15
        @property
        def returncode(self):
            return -15 if self.stopped else self._rc

    def mk_wt(state="active", card=None, driver_txt="# fake driver\n"):
        td = pathlib.Path(tempfile.mkdtemp(dir=tmp_root))
        (td / "db/governance").mkdir(parents=True); (td / "db/properties").mkdir(parents=True); (td / "tools/ionic").mkdir(parents=True)
        (td / "db/governance/decisions.json").write_text(json.dumps({"decisions": [{"id": DECISION, "decision_state": state}]}), encoding="utf-8")
        (td / CARD_REL).write_text(json.dumps(card or mk_card(), ensure_ascii=False), encoding="utf-8")
        (td / DRIVER_REL).write_text(driver_txt, encoding="utf-8")
        return td

    def go(wt, scen=None, poll_s=3600.0, order=DEFAULT_ORDER, expect=None, rr=None, ack=None, mq=None,
           gpu=None, sleep_hook=None, pg_alive=None, seed_worst_h=21.0):
        launched, clock = [], [0.0]
        def launch(cmd, lp):
            return FakeQuench(cmd, lp, scen=scen, launched=launched)
        gq = list(gpu or [])
        def gpu_used():
            x = gq.pop(0) if gq else 100
            if isinstance(x, BaseException):
                raise x
            return x
        def sleep(s):
            clock[0] += s
            if sleep_hook:
                sleep_hook(clock[0])
        rr = rr or pathlib.Path(tempfile.mkdtemp(dir=tmp_root))
        a = argparse.Namespace(worktree=str(wt), run_root=str(rr), python="python3", seed_worst_h=seed_worst_h,
                               poll_s=poll_s, gpu_poll_s=60.0, start_max_mib=2000, order=order, ack_stop=ack,
                               expect_sha=expect or sha16(pathlib.Path(wt) / DRIVER_REL))
        rc = run(a, {"mq": mq or real, "launch": launch, "gpu_used": gpu_used, "sleep": sleep, "clock": lambda: clock[0],
                     "pg_alive": pg_alive or (lambda pg: False)})
        return rc, launched, rr
    J = lambda p: json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
    tag = lambda L: [(p.sys, p.seed) for p in L]

    wt = mk_wt()
    # 1) 모두 통과 — 진짜 판독 함수로
    rc, L, rr = go(wt)
    sm = J(rr / "stage1_summary.json"); led = J(rr / "stage1_ledger.json")
    v11 = J(rr / "A/seed11/stage1_verdict.json")
    chk(rc == 0 and len(L) == 10 and tag(L)[:3] == [("A", 11), ("B", 11), ("A", 12)] and sm["track"] == "stage1_pass"
        and sm["stage2"]["seeds"] == [11, 12] and len(led["runs"]) == 10 and all(r["status"] == "ended" for r in led["runs"])
        and v11["status"] == "pass" and v11["provenance"]["files_sha256"]["traj.xyz"] and not v11["closes_system"]
        and all(getattr(p_, "ledger_at_first_poll", False) for p_ in L),
        f"진짜 판독 함수: 10 담금질 · A/B 번갈아 · 띄운 직후 장부에 시작 (첫 poll 전) · 판정에 원자료 지문 · 1 단계 통과 · 2 단계 시드 {sm['stage2'] and sm['stage2']['seeds']} (rc {rc})")
    c0 = L[0].cmd
    chk(c0[c0.index("--fix_density") + 1] == repr(float(rho["A"])) and c0[c0.index("--compress_ps") + 1] == "20"
        and "--turbo" in c0 and c0[c0.index("--n_fu") + 1] == "12" and L[1].cmd[L[1].cmd.index("--n_fu") + 1] == "15",
        "담금질 명령: 카드 기계값 그대로 (밀도 repr · 압축 20 · turbo · n_fu 12/15 = 카드 조성의 P 수)")
    real_vals = real.read_li2s2_values(repo / CARD_REL)
    cmdA = build_cmd("py", repo, "/r", "A", 11, real_vals, real)
    chk(cmdA[cmdA.index("--fix_density") + 1] == "1.91347" and cmdA[cmdA.index("--quench_rate") + 1] == "1000000000000",
        "DG P2: 진짜 카드의 손 실행 명령은 기계값 1.91347 그대로 (본문 1.9135 반올림 아님) · --print_cmd 와 같은 함수")
    # 2) DG P0-1 — A11 녹음 미충족 → 닫음 → 재시작 · STOP 지움 · 장부 지움 어느 쪽으로도 다시 안 열린다
    wt_m = mk_wt()
    rc, L, rr = go(wt_m, scen={("A", 11): {"melt": "fail", "polls": 8}})
    v = J(rr / "A/seed11/stage1_verdict.json"); sp = J(rr / "STOP.json")
    chk(rc == RC["melt"] and len(L) == 1 and L[0].stopped and v["status"] == "fail" and v["closes_system"] and sp["terminal"],
        "⛔음성 DF Q-DF-3 · DG P0-1: A11 녹음 미충족 → 그 담금질을 실제로 멈추고 · 판정 fail + closes_system · STOP (닫는 사건)")
    rc2, L2, _ = go(wt_m, rr=rr)
    rc3, L3, _ = go(wt_m, rr=rr, ack=sp["stop_id"])
    stop_id3, hist3 = J(rr / "STOP.json")["stop_id"], J(rr / "stage1_ledger.json").get("stop_history")   # rc3 직후에 잰다
    (rr / "STOP.json").unlink()
    rc4, L4, _ = go(wt_m, rr=rr)
    (rr / "STOP.json").unlink(); (rr / "stage1_ledger.json").unlink()
    rc5, L5, _ = go(wt_m, rr=rr)
    chk(rc2 == RC["melt"] and rc3 == RC["melt"] and not L2 and not L3 and not hist3 and stop_id3 == sp["stop_id"],
        f"⛔음성 DG P0-1: 같은 run_root 로 재시작해도 · --ack_stop 을 줘도 닫는 사건은 다시 안 열린다 (담금질 0 · rc {rc2} · {rc3} · "
        f"STOP 그대로 · 이력 {len(hist3 or [])})")
    chk(rc4 == RC["melt"] and not L4 and rc5 == RC["track"] and not L5 and J(rr / "stage1_summary.json")["track"] == "stop_track",
        f"⛔음성 DG P0-1: STOP 을 지워도 장부가 · 장부까지 지워도 판정 파일 (다시 판정 · closes_system) 이 막는다 (rc {rc4} · {rc5})")
    rc, L, rr = go(wt, scen={("B", 11): {"melt": "fail", "polls": 8}})
    chk(rc == RC["melt"] and len(L) == 2 and L[1].stopped and not L[0].stopped, "⛔음성: B11 녹음 미충족 → B11 을 멈추고 트랙 멈춤 (A11 은 끝까지)")
    rc, L, rr = go(wt, scen={("A", 12): {"melt": "fail"}})
    sm = J(rr / "stage1_summary.json"); v12 = J(rr / "A/seed12/stage1_verdict.json")
    chk(rc == 0 and len(L) == 10 and not any(p.stopped for p in L) and v12["status"] == "fail" and not v12["closes_system"]
        and sm["stage2"]["seeds"] == [11, 13],
        f"첫 시드가 아닌 A12 녹음 미충족은 일반 탈락 (담금질 중 안 멈춤 · 계를 안 닫음) → A 4/5 · 2 단계 시드 {sm['stage2'] and sm['stage2']['seeds']}")
    rc, L, rr = go(wt, scen={("A", 12): {"final": "ps4_broken"}, ("A", 13): {"final": "ps4_broken"}})
    chk(rc == RC["track"] and len(L) == 5 and J(rr / "STOP.json")["summary"]["track"] == "stop_track",
        "⛔음성 DF P1-3: A 탈락 (PS₄ 깨짐) 이 둘이 되는 순간 (A13 뒤) 트랙 멈춤 — B 가 통과 중이어도")
    # 3) DG P1-4 — final.xyz 오복사 (5 원자 · 밀도 다름) 는 진짜 stage1_verdict 가 무효로
    rc, L, rr = go(wt, scen={("A", 12): {"final": "five"}})
    v = J(rr / "A/seed12/stage1_verdict.json")
    chk(rc == RC["track"] and len(L) == 3 and v["status"] == "invalid" and J(rr / "stage1_summary.json")["track"] == "invalid",
        "⛔음성 DG P1-4: final.xyz 에 5 원자 PS₄ 를 넣으면 진짜 stage1_verdict 가 무효 → 트랙 멈춤 (통과 아님)")
    rc, L, rr = go(wt, scen={("B", 11): {"final": "dense"}})
    chk(rc == RC["track"] and J(rr / "B/seed11/stage1_verdict.json")["status"] == "invalid",
        "⛔음성 DG P1-4: final.xyz 의 셀 · 밀도가 계획과 다르면 무효")
    rr_full = go(wt)[2]
    rr_v = pathlib.Path(tempfile.mkdtemp(dir=tmp_root))
    for s in SYSTEMS:
        for sd in (11, 12, 13, 14, 15):
            (rr_v / s / f"seed{sd}").mkdir(parents=True)
            shutil.copy(rr_full / s / f"seed{sd}" / "stage1_verdict.json", rr_v / s / f"seed{sd}" / "stage1_verdict.json")
    smv = real.stage1_summary(rr_v, values=real.read_li2s2_values(wt / CARD_REL), log=lambda *m: None)
    rc, L, _ = go(wt, rr=rr_v)
    chk(smv["track"] == "invalid" and len(smv["stale_verdicts"]) == 10 and rc in (RC["resume"], RC["track"]) and not L
        and J(rr_v / "stage1_summary.json")["track"] != "stage1_pass"
        and J(rr_v / "A/seed11/stage1_verdict.json")["status"] == "incomplete",
        f"⛔음성 DG P1-4: 원자료 없이 통과 판정 파일만 있는 폴더 — 묶음은 지문 불일치로 무효 · 러너는 다시 판정해 안 띄우고 멈춤 (rc {rc})")
    shutil.copy(rr_full / "A/seed11/final.xyz", rr_full / "A/seed11/final.xyz.bak")
    (rr_full / "A/seed11/final.xyz").write_text((rr_full / "A/seed11/final.xyz").read_text().replace("Cl ", "Cl ", 1) + "\n", encoding="utf-8")
    sm_t = real.stage1_summary(rr_full, values=real.read_li2s2_values(wt / CARD_REL), log=lambda *m: None)
    chk(sm_t["track"] == "invalid" and sm_t["stale_verdicts"] == ["A11"],
        "⛔음성 DG P1-4: 판정 뒤 원자료 (final.xyz) 가 한 바이트라도 바뀌면 그 시드 판정은 무효 (다시 판정하라)")
    shutil.move(rr_full / "A/seed11/final.xyz.bak", rr_full / "A/seed11/final.xyz")
    vals_other = json.loads(json.dumps(real.read_li2s2_values(wt / CARD_REL)))
    vals_other["melt_window"]["threshold_source"] = "시험: 카드 값 글자 하나만 다름"
    sm_card = real.stage1_summary(rr_full, values=vals_other, log=lambda *m: None)
    sm_same = real.stage1_summary(rr_full, values=real.read_li2s2_values(wt / CARD_REL), log=lambda *m: None)
    chk(sm_card["track"] == "invalid" and len(sm_card["stale_verdicts"]) == 10 and sm_same["track"] == "stage1_pass",
        "⛔음성 DG P1-4: 다른 카드 값으로 낸 판정은 묶음에서 무효 (카드 값 지문 · 같은 카드면 그대로 통과)")
    # 4) DG P0-2 — Ctrl-C · 예외 · 판독 예외
    hook = {"armed": True}
    def ctrl_c(t):
        if hook["armed"] and t >= 3600.0 * 7 + 1:     # A11 (5 h) 끝난 뒤 B11 의 둘째 poll 전후
            hook["armed"] = False; raise KeyboardInterrupt("시험: 사용자 Ctrl-C")
    wt_i = mk_wt()
    rc, L, rr = go(wt_i, sleep_hook=ctrl_c)
    led = J(rr / "stage1_ledger.json"); sp = J(rr / "STOP.json")
    lk = _Lock(rr / "stage1.lock"); got_lock = lk.acquire(); lk.release()
    chk(rc == RC["interrupted"] and L[-1].stopped and led["runs"][-1]["status"] == "interrupted" and led["runs"][-1]["end"]
        and led["runs"][-1]["wall_h"] is not None and sp["code"] == "interrupted" and not sp["terminal"] and got_lock,
        "⛔음성 DG P0-2: 담금질 중 Ctrl-C → 그 담금질을 멈추고 · 장부에 끝 · 경과 · STOP 을 쓴 뒤 잠금을 푼다")
    rc_a, La, _ = go(wt_i, rr=rr)
    rc_b, Lb, _ = go(wt_i, rr=rr, ack="0000000000000000")
    rc_c, Lc, _ = go(wt_i, rr=rr, ack=sp["stop_id"])
    chk(rc_a == RC["interrupted"] and rc_b == RC["interrupted"] and not La and not Lb and rc_c == RC["resume"] and not Lc
        and J(rr / "stage1_ledger.json")["stop_history"][-1]["stop_id"] == sp["stop_id"],
        "⛔음성 DG P0-2: 중단 뒤 재시작은 --ack_stop <stop_id> 가 맞아야 이어가고 · 끊긴 시드 폴더에서 멈춘다 (덮어쓰지 않는다)")
    rc, L, rr = go(wt, scen={("A", 11): {"raise_on_poll": 3, "polls": 6}})
    lk = _Lock(rr / "stage1.lock"); got_lock = lk.acquire(); lk.release()
    chk(rc == RC["interrupted"] and L[0].stopped and J(rr / "stage1_ledger.json")["runs"][0]["status"] == "interrupted" and got_lock,
        "⛔음성 DG P0-2: poll 이 예외를 던져도 (자식 상태 확인 실패) 담금질을 멈추고 장부 · 잠금 정리")
    rc, L, rr = go(wt, gpu=[100, 100, 100, 100, RuntimeError("nvidia-smi 실패")])
    sp = J(rr / "STOP.json")
    chk(rc == RC["interrupted"] and len(L) == 2 and not any(p.stopped for p in L) and sp["code"] == "interrupted",
        "⛔음성 DG P0-2: 담금질 사이의 예외 (nvidia-smi) → 돌던 담금질 없음 · STOP · 잠금 정리")
    class FlakyMQ:
        def __init__(self):
            self.n = 0
        def __getattr__(self, k):
            return getattr(real, k)
        def melt_window_check(self, rd, values=None, log=None):
            self.n += 1
            if self.n == 2:
                raise RuntimeError("시험: 판독 예외")
            return real.melt_window_check(rd, values=values, log=log)
    rc, L, rr = go(wt, mq=FlakyMQ())
    led = J(rr / "stage1_ledger.json")
    chk(rc == 0 and len(led["runs"][0].get("melt_check_errors", [])) == 1,
        "DG P0-2: 녹음 판정이 한 번 예외를 던져도 러너는 죽지 않고 기록 뒤 다음 poll 에 다시 본다 (진짜 판독기 · plan 없음 → 미완)")
    # 5) DG P0-3 — 실행 중 상한 (아홉 런 20 h · 마지막 60 h · 상한 230)
    scen = {(s, sd): {"polls": 20} for s in SYSTEMS for sd in (11, 12, 13, 14, 15)}
    scen[("B", 15)] = {"polls": 60}
    rc, L, rr = go(wt, scen=scen)
    led = J(rr / "stage1_ledger.json"); sm = real.stage1_summary(rr, values=real.read_li2s2_values(wt / CARD_REL), log=lambda *m: None)
    chk(rc == RC["cap"] and len(L) == 10 and L[-1].stopped and abs(led["runs"][-1]["wall_h"] - 50.0) < 1e-9
        and led["runs"][-1]["status"] == "cap" and sm["track"] != "stage1_pass",
        f"⛔음성 DG P0-3: 마지막 런이 60 h 여도 누적 230 h 에서 그 담금질을 멈추고 미완결 (wall {led['runs'][-1]['wall_h']:.1f} h · 묶음 {sm['track']})")
    rc, L, rr = go(mk_wt(card=mk_card(stage1_cap_gpu_h=40.0)), scen={k: {"polls": 10} for k in scen})
    chk(rc == RC["cap"] and len(L) == 2 and J(rr / "STOP.json")["code"] == "cap",
        "⛔음성 DF P1-6: 누적 + 한 시드 최악 > 상한 (카드 40 h) 이면 새 시드를 안 띄우고 미완결")
    sid_cap = J(rr / "STOP.json")["stop_id"]
    rc_c2, Lc2, _ = go(mk_wt(card=mk_card(stage1_cap_gpu_h=40.0)), rr=rr, ack=sid_cap)
    chk(rc_c2 == RC["cap"] and not Lc2 and J(rr / "STOP.json")["stop_id"] == sid_cap and not J(rr / "stage1_ledger.json").get("stop_history"),
        "⛔음성 DG P0-3: 상한 멈춤은 --ack_stop 만으로 안 넘어간다 (STOP 그대로 · 이력에 안 옮김 — 카드 상한이 올라가야)")
    # 소비자 쪽 상한 (회신 DG P0-3) — 다 통과한 폴더라도 장부 합이 상한을 넘거나 장부가 없으면 1 단계 통과가 아니다
    vals_t = real.read_li2s2_values(wt / CARD_REL)
    led_full = J(rr_full / "stage1_ledger.json")
    sm_ok = real.stage1_summary(rr_full, values=vals_t, log=lambda *m: None)
    _write_json_atomic(rr_full / "stage1_ledger.json", {**led_full, "runs": led_full["runs"] + [{"system": "A", "seed": 11, "wall_h": 300.0}]})
    sm_over = real.stage1_summary(rr_full, values=vals_t, log=lambda *m: None)
    (rr_full / "stage1_ledger.json").unlink()
    sm_none = real.stage1_summary(rr_full, values=vals_t, log=lambda *m: None)
    chk(sm_ok["track"] == "stage1_pass" and sm_over["track"] == "cap_incomplete" and sm_none["track"] == "pending",
        f"⛔음성 DG P0-3 (소비자): 다 통과해도 장부 합 > 상한이면 미완결 · 장부가 없으면 대기 ({sm_ok['track']} · {sm_over['track']} · {sm_none['track']})")
    # 6) 시작 전 검사 · 끊긴 런 · 잠금 · 고아 런 · 순서
    rc, L, rr = go(mk_wt(state="proposed"))
    chk(rc == RC["refused"] and not L, "⛔음성: 결정이 proposed 면 시작하지 않는다")
    rc, L, rr = go(wt, expect="0000000000000000")
    chk(rc == RC["refused"] and not L, "⛔음성: 드라이버 sha16 이 고정값과 다르면 시작하지 않는다")
    bad_card = mk_card(); bad_card["기계_판독_값"]["melt_window"]["estimator"] = "window_mto_v2"
    rc, L, rr = go(mk_wt(card=bad_card))
    chk(rc == RC["refused"] and not L, "⛔음성 DG P1-7: 카드 estimator 가 구현과 다르면 시작하지 않는다")
    rc, L, rr = go(wt, order="A:11,B:11,A:12,B:12,A:13,B:13,A:14,B:14,A:15")
    rc2, L2, _ = go(wt, order="A:12,B:11,A:11,B:12,A:13,B:13,A:14,B:14,A:15,B:15")
    chk(rc == RC["refused"] and rc2 == RC["refused"] and not L and not L2, "⛔음성: 순서가 카드 시드 전부가 아니거나 첫 시드 ≠ 카드 first_seed 면 거부")
    rr0 = pathlib.Path(tempfile.mkdtemp(dir=tmp_root)); (rr0 / "A/seed11").mkdir(parents=True)
    rc, L, _ = go(wt, rr=rr0)
    chk(rc == RC["resume"] and not L, "⛔음성: 판정 없이 런 폴더만 있으면 (끊긴 런) 덮어쓰지 않고 멈춘다")
    rr1 = pathlib.Path(tempfile.mkdtemp(dir=tmp_root))
    held = _Lock(rr1 / "stage1.lock"); assert held.acquire()
    rc, L, _ = go(wt, rr=rr1)
    held.release()
    second = _Lock(rr1 / "stage1.lock"); a1 = second.acquire(); third = _Lock(rr1 / "stage1.lock"); a2 = third.acquire(); second.release()
    chk(rc == RC["refused"] and not L and a1 and not a2,
        "⛔음성 DG P1-6: 잠금을 잡은 러너가 있으면 거부 · 잠금은 한 번의 flock (둘째 획득 실패) · 놓으면 다시 잡힌다")
    (rr1 / "stage1.lock").write_text("999999\n")          # 죽은 러너가 남긴 잠금 파일 — flock 이 아니라 파일만
    rc, L, _ = go(wt, rr=rr1)
    chk(rc == 0 and len(L) == 10, "낡은 잠금 파일 (프로세스 없음) 은 막지 않는다 — flock 은 커널이 풀었다")
    rr2 = pathlib.Path(tempfile.mkdtemp(dir=tmp_root)); (rr2 / "A/seed11").mkdir(parents=True)
    (rr2 / "A/seed11/thermo.csv").write_text("x\n")
    _write_json_atomic(rr2 / "stage1_ledger.json", {"runs": [{"system": "A", "seed": 11, "start": "t", "start_epoch": time.time() - 7200,
                                                               "pgid": 4242, "status": "running", "end": None, "wall_h": None,
                                                               "wall_h_so_far": 1.5}]})
    rc_al, L_al, _ = go(wt, rr=rr2, pg_alive=lambda pg: pg == 4242)
    rc_or, L_or, _ = go(wt, rr=rr2)
    led = J(rr2 / "stage1_ledger.json")
    chk(rc_al == RC["refused"] and not L_al and rc_or == RC["resume"] and not L_or and led["runs"][0]["status"] == "orphaned"
        and led["runs"][0]["wall_h"] >= 1.5,
        f"⛔음성 DG P0-2: 장부의 도는 중 런 — 프로세스 그룹이 살아 있으면 거부 · 죽었으면 고아 런으로 비용 어림 ({led['runs'][0]['wall_h']:.2f} h) 뒤 끊긴 폴더에서 멈춤")
    rc, L, rr = go(wt, scen={("B", 12): {"rc": 137}})
    chk(rc == RC["abnormal"] and len(L) == 4, "⛔음성: B12 담금질 rc 137 (비정상) → 멈춤 (뒤 시드 안 띄움)")
    rc, L, rr = go(wt, gpu=[9000, 9000, 1500, 9000, 1500, 1500])
    chk(rc == 0 and len(L) == 10 and "비기를 기다린다" in (rr / "stage1.log").read_text(encoding="utf-8"),
        "GPU 가 찰 때는 두 번 연속 빌 때까지 기다린 뒤 띄운다")
    # 7) 진짜 프로세스 그룹 (POSIX) — _Proc.stop 이 자기 그룹 (자식 · 손자) 만 멈추고 기다린다 · 옆 프로세스는 안 건드린다
    #    (회신 DG: '실제 Linux 프로세스 그룹 종료는 하지 않았다' — 가짜 담금질 시험이 못 보는 자리)
    if os.name == "posix":
        def _pid_alive(pid):
            try:
                return pathlib.Path(f"/proc/{pid}/stat").read_text().split()[2] != "Z"     # 거둬지지 않은 좀비는 죽은 것
            except FileNotFoundError:
                return False
            except OSError:
                try:
                    os.kill(pid, 0); return True
                except ProcessLookupError:
                    return False
        tdp = pathlib.Path(tempfile.mkdtemp(dir=tmp_root))
        code = ("import subprocess, sys, time; "
                "c = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(600)']); "
                "open(sys.argv[1], 'w').write(str(c.pid)); time.sleep(600)")
        bystander = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(600)"])
        pr = _Proc([sys.executable, "-c", code, str(tdp / "grandchild.pid")], tdp / "p.log")
        for _ in range(200):
            if (tdp / "grandchild.pid").is_file() and (tdp / "grandchild.pid").read_text().strip():
                break
            time.sleep(0.05)
        gpid = int((tdp / "grandchild.pid").read_text())
        before = pr.poll() is None and _pid_alive(gpid) and os.getpgid(gpid) == pr.pid
        t0 = time.time(); rc_ = pr.stop(grace_s=5); dt = time.time() - t0
        time.sleep(0.2)
        gone = (pr.poll() is not None) and not _pid_alive(gpid)
        by_ok = bystander.poll() is None
        bystander.kill(); bystander.wait()
        chk(before and gone and by_ok and rc_ is not None and dt < 10,
            f"진짜 프로세스 그룹: _Proc.stop 이 그 담금질과 손자까지 멈추고 기다린다 · 옆 프로세스는 산다 (rc {rc_} · {dt:.1f} s)")
    shutil.rmtree(tmp_root, ignore_errors=True)
    print(f"li2s2_stage1_runner selftest: ⭕ {ok} · ⛔ {bad}")
    return 0 if bad == 0 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--worktree", help="이 카드를 담은 커밋의 git worktree (도구 · 카드 · 결정 원장을 여기서 읽는다)")
    ap.add_argument("--run_root", help="담금질 출력 루트 → <run_root>/<A|B>/seed<S>/")
    ap.add_argument("--python", default=sys.executable, help="담금질을 돌릴 python (uma env 절대경로)")
    ap.add_argument("--order", default=DEFAULT_ORDER)
    ap.add_argument("--seed_worst_h", type=float, default=21.0, help="관측이 없을 때 한 시드 최악 (카드 견적 상단 · 착수 판단용 예상치)")
    ap.add_argument("--poll_s", type=float, default=300.0, help="첫 시드 녹음 판정 · 상한 · heartbeat 를 볼 간격")
    ap.add_argument("--gpu_poll_s", type=float, default=60.0)
    ap.add_argument("--start_max_mib", type=int, default=2000, help="이 이하가 두 번 연속이면 띄운다")
    ap.add_argument("--ack_stop", default=None, help="STOP.json 의 stop_id — 앞선 (닫는 사건이 아닌) 멈춤을 확인했다는 표시")
    ap.add_argument("--print_cmd", default=None, metavar="SYS:SEED", help="그 시드의 담금질 명령을 카드 기계값에서 만들어 찍고 끝난다")
    ap.add_argument("--expect_sha", default=EXPECTED_DRIVER_SHA16)
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if not (a.worktree and a.run_root):
        ap.error("--worktree · --run_root 가 필요하다")
    if a.print_cmd:
        W = pathlib.Path(a.worktree); mq = load_mq(W)
        vals = mq.read_li2s2_values(W / CARD_REL)
        sysn, seed = parse_order(a.print_cmd)[0]
        print(shlex.join(build_cmd(a.python, W, a.run_root, sysn, seed, vals, mq)))
        return 0
    return run(a)


if __name__ == "__main__":
    sys.exit(main())
