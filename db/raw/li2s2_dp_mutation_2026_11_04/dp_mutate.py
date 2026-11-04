"""회신 DO 고침 변이 검사 — DO 판 (../li2s2_do_mutation_2026_11_04/do_mutate.py) 의 222 개를 가져오되 DO 고침으로 자리가 바뀐 5 개는 새 자리로
옮기고, DO 고침 자리 (DP1–) 를 더한다. 실행 · 판정은 DL 판과 같다 (저장소 밖 복사본 · 작업자 · which = run / drv / both).
옵션: --dry (자리만) · --only=접두 (쉼표로 여럿) · --tag=이름 (복사본 폴더) · --failfast (러너 selftest 첫 빨강에서 멈춤 — 판정 같음) · --workers=N.
뺀 것 (같은 결과를 내는 변이 — 시험이 못 가르는 것이 맞다):
  · persist_observed_melt 의 save_ledger 끄기 — run() 의 끝 처리가 어차피 장부를 저장한다
  · run() 시드 루프의 판정 상태 엄격 판독 끄기 — 바로 앞 ①-4 가 그 판정을 원자료로 다시 써서 같은 열쇠 둘이 남을 수 없다
  · 카드 · G4 밴드 카드 · gate_check · seed_gate 의 plan 엄격 판독 끄기 — 카드는 값 지문으로 고정되고 · plan 은 stage1_verdict 가 먼저 엄격히
    읽어 못 읽으면 gate · seed_gate 까지 안 간다 (깊은 방어)."""
import importlib.util, pathlib, sys

REPO = pathlib.Path("/home/user/Yonghoon-DEM-DFT")
_spec = importlib.util.spec_from_file_location("do_mutate", REPO / "db/raw/li2s2_do_mutation_2026_11_04/do_mutate.py")
do = importlib.util.module_from_spec(_spec)
_argv = sys.argv; sys.argv = [sys.argv[0]]                   # do_mutate 의 --tag · --failfast 해석을 여기서 다시 한다
_spec.loader.exec_module(do)
sys.argv = _argv
dl = do.dl
RUNR, DRVR = dl.RUNR, dl.DRVR

MOVED = {
 "K14_attest_reads_before_lock": ("K14_attest_reads_before_lock", RUNR, [
     ('    if deps.get("before_lock"):\n        deps["before_lock"]()',
      '    _pre = _loads_strict(led_p.read_text(encoding="utf-8"))\n    if deps.get("before_lock"):\n        deps["before_lock"]()'),
     ('        try:                                                 # ⭐ 잠금 안에서 다시 읽는다 · 회신 DO P1 — 엄격히 (못 읽으면 증언을 받지 않고 원본 그대로)\n'
      '            led = _loads_strict(led_p.read_text(encoding="utf-8"))',
      '        try:                                                 # ⭐ 잠금 안에서 다시 읽는다 · 회신 DO P1 — 엄격히 (못 읽으면 증언을 받지 않고 원본 그대로)\n'
      '            led = _pre')], "run"),
 "K28_ack_kind_from_code": ("K28_ack_kind_from_code", RUNR, [
     ('    kind, kd = mq.run_kind_detail(hit[0], rec["path"] if rec else None, values)',
      '    kind, kd = next((k for k, cs in mq.RETRY_BIND_CODES.items() if code in cs), "interrupted"), {}')], "run"),
 "L12_ack_scientific_ok": ("L12_ack_scientific_ok", RUNR, [
     ('    if kind == "scientific":\n        if kd.get("source") == "folder_melt_window" and observed is not None:',
      '    if False:\n        if kd.get("source") == "folder_melt_window" and observed is not None:')], "run"),
 "L13_runner_kind_ledger_only": ("L13_runner_kind_ledger_only", RUNR, [
     ('        rk, rk_d = mq.run_kind_detail(x, rec["path"], values)', '        rk, rk_d = mq.run_kind_detail(x, None, values)')], "run"),
 "DO43_signal_unmasked": ("DO43_signal_unmasked", RUNR, [
     ('    hold = hasattr(signal, "pthread_sigmask") and threading.current_thread() is threading.main_thread()', '    hold = False')], "run"),
}
F = lambda name, anchor, repl, which="drv", where=DRVR: (name, where, [(anchor, repl)], which)
NEW = [
 # ── P0: 복구 · 확인 경로가 본 녹음 fail 을 거부 전에 장부에
 F("DP1_retry_observed_off", '            if rk_d.get("source") == "folder_melt_window":     # ⭐ 회신 DO P0', '            if False:', "run", RUNR),
 F("DP2_ack_observed_off", '        if kd.get("source") == "folder_melt_window" and observed is not None:', '        if False:', "run", RUNR),
 F("DP3_persist_melt_off", '        if not (isinstance(r_.get("melt_check"), dict) and r_["melt_check"].get("verdict") == "fail"):', '        if False:', "run", RUNR),
 F("DP4_persist_no_close", '        if first_ and r_.get("closes_system") is not True:', '        if False:', "run", RUNR),
 F("DP6_ack_persist_call_off", '                for o_ in obs_:                              # ⭐ 회신 DO P0', '                for o_ in []:', "run", RUNR),
 F("DP7_loop_persist_call_off", '                    if el_.get("observed_melt"):                 # ⭐ 회신 DO P0', '                    if False:', "run", RUNR),
 F("DP8_loop_melt_stop_off", '                        if r_ is not None and r_.get("closes_system") is True:\n                            return stop("melt",',
   '                        if False:\n                            return stop("melt",', "run", RUNR),
 F("DP9_kind_detail_no_melt", '            return "scientific", {"source": "folder_melt_window", "melt": {k: mw.get(k) for k in MELT_OBSERVED_KEYS}}',
   '            return "scientific", {"source": "ledger"}', "run"),
 # ── P1: 같은 열쇠 둘 — 엄격 판독 · 원문 보존 · 못 읽은 장부를 다시 쓰지 않음
 F("DP10_verdict_records_loose", '            v = loads_strict(vf.read_text(encoding="utf-8"))', '            v = json.loads(vf.read_text(encoding="utf-8"))', "both"),
 F("DP11_history_loose", '                h = loads_strict(ln)                             # ⭐ 회신 DO P1', '                h = json.loads(ln)', "both"),
 F("DP12_prev_loose", '            prev = loads_strict(vf.read_text(encoding="utf-8"))', '            prev = json.loads(vf.read_text(encoding="utf-8"))', "both"),
 F("DP13_plan_stage_loose", '        plan = loads_strict((f / "plan.json").read_text(encoding="utf-8"))   # ⭐ 회신 DO P1',
   '        plan = json.loads((f / "plan.json").read_text(encoding="utf-8"))'),
 F("DP14_md_done_loose", '            rec = loads_strict(md.read_text(encoding="utf-8"))\n            rid = plan.get("run_id")',
   '            rec = json.loads(md.read_text(encoding="utf-8"))\n            rid = plan.get("run_id")'),
 F("DP15_identity_attempt_loose", '                att_ = loads_strict((rd_ / ATTEMPT_NAME).read_text(encoding="utf-8"))',
   '                att_ = json.loads((rd_ / ATTEMPT_NAME).read_text(encoding="utf-8"))'),
 F("DP16_verdict_status_loose", '        st = loads_strict(vf.read_text(encoding="utf-8")).get("status")', '        st = json.loads(vf.read_text(encoding="utf-8")).get("status")'),
 F("DP17_inventory_loose", '                    rec = loads_strict(p.read_text(encoding="utf-8"))   # ⭐ 회신 DO P1',
   '                    rec = json.loads(p.read_text(encoding="utf-8"))'),
 F("DP18_stage1_plan_loose", '        plan = loads_strict((run / "plan.json").read_text(encoding="utf-8"))   # ⭐ 회신 DO P1 — 같은 열쇠 둘은 마지막 값으로 읽지 않는다',
   '        plan = json.loads((run / "plan.json").read_text(encoding="utf-8"))', "both"),
 F("DP19_driver_strict_hook_off", '    return json.loads(text, object_pairs_hook=_no_dup_pairs)', '    return json.loads(text)', "both"),
 F("DP20_ledger_run_loose", '                led0_ = _loads_strict(led_p.read_text(encoding="utf-8"))', '                led0_ = json.loads(led_p.read_text(encoding="utf-8"))',
   "run", RUNR),
 F("DP21_attest_view_loose", '        try:                                                 # ⭐ 회신 DO P1 — 읽기만 하는 조회도 엄격히 (같은 열쇠 둘 = 못 읽음)\n'
                             '            led = _loads_strict(led_p.read_text(encoding="utf-8"))',
   '        try:                                                 # ⭐ 회신 DO P1 — 읽기만 하는 조회도 엄격히 (같은 열쇠 둘 = 못 읽음)\n'
   '            led = json.loads(led_p.read_text(encoding="utf-8"))', "run", RUNR),
 F("DP22_attest_lock_loose", '        try:                                                 # ⭐ 잠금 안에서 다시 읽는다 · 회신 DO P1 — 엄격히 (못 읽으면 증언을 받지 않고 원본 그대로)\n'
                             '            led = _loads_strict(led_p.read_text(encoding="utf-8"))',
   '        try:                                                 # ⭐ 잠금 안에서 다시 읽는다 · 회신 DO P1 — 엄격히 (못 읽으면 증언을 받지 않고 원본 그대로)\n'
   '            led = json.loads(led_p.read_text(encoding="utf-8"))', "run", RUNR),
 F("DP23_runner_strict_hook_off", '    return json.loads(text, object_pairs_hook=_no_dup_pairs)\n\n\ndef decision_state',
   '    return json.loads(text)\n\n\ndef decision_state', "run", RUNR),
 F("DP24_decision_loose", '        D = _loads_strict((pathlib.Path(worktree) / "db/governance/decisions.json").read_text(encoding="utf-8"))',
   '        D = json.loads((pathlib.Path(worktree) / "db/governance/decisions.json").read_text(encoding="utf-8"))', "run", RUNR),
 # ── P2: 요약 fail-closed · 자식 신호 마스크
 F("DP25_summary_shape_off", '            shp = _verdict_shape_problem(vv)                  # ⭐ 회신 DO P2', '            shp = None'),
 F("DP26_summary_failclosed_off", '    except Exception as e:\n        res = _summary_failed(', '    except ZeroDivisionError as e:\n        res = _summary_failed('),
 F("DP27_child_mask_off", '        kw = {"preexec_fn": _child_restore_mask} if (os.name == "posix" and hasattr(signal, "pthread_sigmask")) else {}',
   '        kw = {}', "run", RUNR),
 F("DP28_child_restore_noop", '    m = _PRE_HOLD_MASK\n    if m is not None:', '    return\n    m = _PRE_HOLD_MASK\n    if m is not None:', "run", RUNR),
]

MUT = [MOVED.get(m[0], m) for m in do.MUT] + NEW
dl.MUT = MUT
TAG = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--tag=")), "dp")
FAILFAST = "--failfast" in sys.argv
WORKERS = int(next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--workers=")), dl.N_WORKERS))


def make_mirror(i):
    m = dl.SP / f"mut_{TAG}_w{i}"
    if m.exists():
        dl.shutil.rmtree(m)
    (m / "tools").mkdir(parents=True)
    dl.shutil.copytree(REPO / "tools", m / "tools", dirs_exist_ok=True)
    dl.os.symlink(REPO / "db", m / "db")
    return m


def _selftest(m, rel):
    env = {**dl.os.environ, "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1",
           **({"LI2S2_SELFTEST_FAILFAST": "1"} if FAILFAST else {})}
    r = dl.subprocess.run([sys.executable, str(m / rel), "--selftest"], capture_output=True, text=True, timeout=1800, cwd=str(m), env=env)
    out = r.stdout + r.stderr
    reds = [ln for ln in out.splitlines() if ln.startswith("  ⛔ ")]
    tail = out.strip().splitlines()[-1][:140] if out.strip() else ""
    return r.returncode, (reds[0][:150] if reds else tail)


dl.make_mirror = make_mirror
dl._selftest = _selftest

if __name__ == "__main__":
    bad = dl.check_anchors()
    if bad:
        print("\n".join(bad)); sys.exit(2)
    names = [mu[0] for mu in MUT]
    assert len(names) == len(set(names)), "변이 이름이 겹친다"
    print(f"변이 {len(MUT)} 개 (DO 판 {len(do.MUT)} · 자리 옮김 {len(MOVED)} · DP {len(NEW)}) · 자리 모두 한 번씩", flush=True)
    if "--dry" in sys.argv:
        sys.exit(0)
    only = [a.split("=", 1)[1] for a in sys.argv if a.startswith("--only=")]
    todo = [mu for mu in MUT if not only or any(mu[0].startswith(p) for p in only[0].split(","))]
    mirrors = [make_mirror(i) for i in range(WORKERS)]
    print(f"작업자 {WORKERS} · 러너 첫 빨강 멈춤 {'켬' if FAILFAST else '끔'} · 복사본 mut_{TAG}_w*", flush=True)
    import queue, threading
    q = queue.Queue()
    for mu in todo:
        q.put(mu)
    lock, results = threading.Lock(), []

    def worker(m):
        while True:
            try:
                mu = q.get_nowait()
            except queue.Empty:
                return
            line = dl.run_one((mu, m))
            with lock:
                results.append(line); print(line, flush=True)
    ts = [threading.Thread(target=worker, args=(m,)) for m in mirrors]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    print(f"끝: 빨강 {sum(1 for x in results if '⭕ 빨강' in x)} / {len(todo)}", flush=True)
