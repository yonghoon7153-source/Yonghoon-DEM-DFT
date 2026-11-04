"""회신 DO 고침 변이 검사 — DO 판 (../li2s2_do_mutation_2026_11_04/do_mutate.py) 의 222 개를 가져오되 DO 고침으로 자리가 바뀐 5 개는 새 자리로
옮기고, DO 고침 자리 (DP1–) 를 더한다. 실행 · 판정은 DL 판과 같다 (저장소 밖 복사본 · 작업자 · which = run / drv / both).
옵션: --dry (자리만) · --only=접두 (쉼표로 여럿) · --tag=이름 (복사본 폴더) · --failfast (러너 selftest 첫 빨강에서 멈춤 — 판정 같음) · --workers=N.
⭐ DP 전 리뷰 (독립 리뷰 둘 · 2026-11-04) 고침 자리 DP29–DP65 (DP45 · DP52 는 뺐다) 와 그 고침으로 자리가 바뀐 DO23 · DO47 · DP3 · DP4 · DP7 · DP8 을 더했다.
뺀 것 (같은 결과를 내는 변이 — 시험이 못 가르는 것이 맞다):
  · persist_observed 의 save_ledger 끄기 — run() 의 끝 처리가 어차피 장부를 저장한다
  · (DP52) 확인 경로의 '적기 실패 → 거부' return 끄기 — 그 실행이 과학적이라 선언 문제 목록이 늘 비어 있지 않아 바로 아래 '선언을 받지 않는다' 가 같은 코드로 거부한다
  · (DP45) DO7 (판독 예외 보류의 바깥 except) — 따로 만들지 않았다: 시험 (MD 완료 기록의 깊은 JSON) 을 더해 DO 판 변이 DO7 이 그대로 잡는다
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
 # DP 전 리뷰 고침으로 자리가 바뀐 셋 (DO23 · DO47 · R4)
 "DO23_kind_records_scientific_off": ("DO23_kind_records_scientific_off", DRVR, [
     ('    if sci:                                                  # ⭐ DP 전 리뷰 F1 · F2', '    if False:')], "both"),
 "DO47_fsync_off": ("DO47_fsync_off", RUNR, [
     ('                os.fsync(fh.fileno())\n            os.replace(tmp, path)', '                pass\n            os.replace(tmp, path)')], "run"),
 "R4_launch_ledger": ("R4_launch_ledger", RUNR, [
     ("            led[\"runs\"].append(ent); state[\"entry\"], state[\"t0\"] = ent, t0\n            save_ledger()",
      "            led[\"runs\"].append(ent); state[\"entry\"], state[\"t0\"] = ent, t0\n            pass"),
     ("                    save_ledger()                            # ⭐ 띄운 직후", "                    pass                                     # ⭐ 띄운 직후")], "run"),
}
F = lambda name, anchor, repl, which="drv", where=DRVR: (name, where, [(anchor, repl)], which)
NEW = [
 # ── P0: 복구 · 확인 경로가 본 녹음 fail 을 거부 전에 장부에
 F("DP1_retry_observed_off", '            if rk_d.get("source") == "folder_melt_window":     # ⭐ 회신 DO P0', '            if False:', "run", RUNR),
 F("DP2_ack_observed_off", '        if kd.get("source") == "folder_melt_window" and observed is not None:', '        if False:', "run", RUNR),
 F("DP3_persist_melt_off", '                if not (isinstance(mc0, dict) and mc0.get("verdict") == "fail"):', '                if False:', "run", RUNR),
 F("DP4_persist_no_close", '            if closes_ and cs0 is not True:', '            if False:', "run", RUNR),
 F("DP6_ack_persist_call_off", '                for o_ in obs_:                              # ⭐ 회신 DO P0', '                for o_ in []:', "run", RUNR),
 F("DP7_loop_persist_call_off", '                    if el_.get("observed"):                      # ⭐ 회신 DO P0 · DP 전 리뷰 F1 · F2', '                    if False:', "run", RUNR),
 F("DP8_loop_melt_stop_off", '                        if r_ is not None and r_.get("closes_system") is True:\n                            src_ = (',
   '                        if False:\n                            src_ = (', "run", RUNR),
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
 # ══ DP 전 리뷰 (독립 리뷰 둘) 고침 — 첫째 F1–F5 · 둘째 F1–F6 · 잔 항목
 # ── 드라이버: 실행 종류 (판정 기록의 근거 · 못 읽은 이전 판정 · 끊긴 런 녹음 invalid · 보관 목록)
 F("DP29_kind_verdict_status_off", '        return "scientific", {"source": "folder_verdict", "status": "fail" if any(r_.get("status") == "fail" for r_ in sci) else "pass",',
   '        return "scientific", {"source": "folder_verdict", "status": None,', "both"),
 F("DP30_kind_closes_off", '                              "closes_system": any(r_.get("closes_system") is True for r_ in sci)}',
   '                              "closes_system": False}', "both"),
 ("DP31_kind_none_status_regress", DRVR, [
     ('    if any(x is None for x in sts):                          # ⭐ DP 전 리뷰 F1', '    if False:                          # ⭐ DP 전 리뷰 F1'),
     ('    if any(x not in LI2S2_STATUSES for x in sts):\n        return "unreadable", {"source": "unreadable"}\n    st_ = row.get',
      '    if any(x not in LI2S2_STATUSES and x is not None for x in sts):\n        return "unreadable", {"source": "unreadable"}\n    st_ = row.get')], "both"),
 F("DP32_kind_cut_melt_invalid", '        if mw.get("verdict") == "invalid" and st_ in RUN_STATUSES_ENDED:   # ⭐ DP 전 리뷰 F3',
   '        if mw.get("verdict") == "invalid":', "both"),
 F("DP33_kind_history_type_off", '    if row.get("melt_check_history") is not None and not isinstance(row.get("melt_check_history"), list):   # ⭐ DP 전 리뷰 F4',
   '    if False:', "both"),
 F("DP34_ledger_history_type_off", '        if mh is not None and not (isinstance(mh, list) and all(isinstance(x_, dict) for x_ in mh)):', '        if False:'),
 # ── 드라이버: 판정 쓰기 · 원문 · 이력 · CLI · 요약 · 앞 프레임 · 소비자
 F("DP35_verdict_tmp_overwrite", '    if os.path.lexists(run / "stage1_verdict.json.tmp"):     # ⭐ DP 전 리뷰 (둘째) F2', '    if False:', "both"),
 F("DP36_raw_lossy", '                    "raw_b64": base64.b64encode(raw_).decode("ascii"),',
   '                    "raw_b64": base64.b64encode(raw_.decode("utf-8", errors="replace").encode("utf-8")).decode("ascii"),', "both"),
 F("DP37_history_splitlines", '            hl = hp.read_text(encoding="utf-8").split("\\n")    # ⭐ DP 전 리뷰 (둘째)',
   '            hl = hp.read_text(encoding="utf-8").splitlines()'),
 F("DP38_cli_writes_folder", '        print(json.dumps({k: res.get(k) for k in ("verdict", "message", "D_framework_cm2_s", "window_used_ps", "n_frames_read")},',
   '        (pathlib.Path(a.melt_window_check) / "melt_window_check.json").write_text("{}", encoding="utf-8")\n'
   '        print(json.dumps({k: res.get(k) for k in ("verdict", "message", "D_framework_cm2_s", "window_used_ps", "n_frames_read")},'),
 F("DP39_summary_base_off", '    except BaseException as e:                               # ⭐ DP 전 리뷰 (둘째) F3', '    except ZeroDivisionError as e:'),
 F("DP40_summary_drop_off", '        try:\n            os.unlink(q)\n        except OSError:\n            pass\n        raise',
   '        try:\n            pass\n        except OSError:\n            pass\n        raise'),
 F("DP41_early_frame_off", '    if why is not None and len(frames) < n_need:            # ⭐ DP 전 리뷰 (둘째) F5', '    if False:', "both"),
 F("DP42_early_frame_header_off", '        if io_err is None and (n_whole is None or n_whole > len(frames)):',
   '        if io_err is None and n_whole is not None and n_whole > len(frames):'),
 F("DP43_consumer_melt_replace_off", '        if not isinstance(r, dict) or not (r.get("verdict") == "fail"\n'
                                     '                                           or (isinstance(r.get("melt_check"), dict) and r["melt_check"].get("verdict") == "fail")):',
   '        if not isinstance(r, dict) or not (r.get("verdict") == "fail"):', "both"),
 F("DP44_consumer_stopid_dup_off", '            if h["stop_id"] in hist:\n                invalid.append(', '            if False:\n                invalid.append(', "both"),
 # ── 러너: 폴더 판정 기록으로 본 결과 · 재판정 · 적기 실패
 F("DP46_retry_verdict_observed_off", '            if rk_d.get("source") == "folder_verdict":         # ⭐ DP 전 리뷰 F1 · F2', '            if False:', "run", RUNR),
 F("DP47_ack_verdict_observed_off", '        elif kd.get("source") == "folder_verdict" and observed is not None:     # ⭐ DP 전 리뷰 F1', '        elif False:', "run", RUNR),
 F("DP48_persist_verdict_off", '                if v0 is None:\n                    new_["verdict"] = obs["status"]', '                if False:\n                    new_["verdict"] = obs["status"]', "run", RUNR),
 F("DP49_persist_verdict_closes_off", '                closes_, basis_ = first_ and obs.get("closes_system") is True, f"first_seed 판정',
   '                closes_, basis_ = False, f"first_seed 판정', "run", RUNR),
 F("DP50_persist_shape_off", '            if mh0 is not None and not isinstance(mh0, list):\n                raise ValueError(',
   '            if False:\n                raise ValueError(', "run", RUNR),
 F("DP51_persist_revert_off", '                    r_.clear(); r_.update(old_)              # 저장 못 했으면 메모리도 되돌린다', '                    pass', "run", RUNR),
 F("DP53_loop_persist_fail_stop_off", '                        except _PersistFailed as e_:\n                            return stop("invalid", f"{sysn}{seed}: 앞 실행에서 본',
   '                        except ZeroDivisionError as e_:\n                            return stop("invalid", f"{sysn}{seed}: 앞 실행에서 본', "run", RUNR),
 F("DP54_rejudge_persist_off", '        for sysn, seed, now_ in rejudged:                    # ⭐ DP 전 리뷰 F2', '        for sysn, seed, now_ in []:', "run", RUNR),
 F("DP55_rejudge_disagree_off", '            if r_ is not None and r_.get("verdict") != now_["status"]:', '            if False:', "run", RUNR),
 F("DP56_first_seed_undecided_off", '            if need_melt and v.get("closes_system") is not True and mw_end != "pass":   # ⭐ DP 전 리뷰 (둘째) F5',
   '            if False:', "run", RUNR),
 # ── 러너: 장부 꼴 · 남은 임시 파일 · 원자 쓰기 · 증언 · 확인 중 예외 · 끝 저장 · 신호 마스크
 F("DP57_ledger_keys_optional", '                if not (isinstance(led0_, dict) and isinstance(led0_.get("runs"), list) and isinstance(led0_.get("stop_history"), list)',
   '                if not (isinstance(led0_, dict) and isinstance(led0_.setdefault("runs", []), list) and isinstance(led0_.setdefault("stop_history", []), list)',
   "run", RUNR),
 F("DP58_ledger_elems_off", '                        and all(isinstance(x_, dict) for x_ in led0_["runs"])', '                        and True', "run", RUNR),
 F("DP59_tmp_start_check_off", '        if left_:                                            # ⭐ DP 전 리뷰 (둘째) F2 — 남은 임시 파일을 무시', '        if False:', "run", RUNR),
 F("DP60_write_excl_off", '    fd = os.open(str(tmp), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)',
   '    fd = os.open(str(tmp), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)', "run", RUNR),
 F("DP61_attest_tmp_off", '        if left_:                                            # ⭐ DP 전 리뷰 (둘째) F2\n            return 10, {"why": f"앞 쓰기가 끊겨',
   '        if False:\n            return 10, {"why": f"앞 쓰기가 끊겨', "run", RUNR),
 F("DP62_stop_pending_off", '        if state.get("stop_pending"):                        # ⭐ DP 전 리뷰 F4', '        if False:', "run", RUNR),
 ("DP63_held_outer_off", RUNR, [
     ('    _PRE_HOLD_MASK = old if outer is None else outer', '    _PRE_HOLD_MASK = old'),
     ('        _PRE_HOLD_MASK = outer\n        if hold:', '        _PRE_HOLD_MASK = None\n        if hold:')], "run"),
 F("DP64_child_unblock_off", '    signal.pthread_sigmask(signal.SIG_UNBLOCK, _held_signal_set())   # ⭐ DP 전 리뷰 (둘째) F4', '    pass', "run", RUNR),
 F("DP66_signal_defer_off", '            if _CRIT[0] > 0:                                 # ⭐ 쓰기 · 띄우기 구간 안', '            if False:', "run", RUNR),
 F("DP67_write_not_critical", '    with _critical():                                        # ⭐ 신호가 임시 파일을 만든 직후에',
   '    with __import__("contextlib").nullcontext():                                        # ⭐ 신호가 임시 파일을 만든 직후에', "run", RUNR),
 F("DP68_launch_not_critical", '                with _critical():                            # ⭐ DP 전 리뷰 (둘째) F4 — 다른 스레드가',
   '                with __import__("contextlib").nullcontext():                            # ⭐ DP 전 리뷰 (둘째) F4 — 다른 스레드가', "run", RUNR),
 F("DP65_final_save_raises", '            except Exception as e_:                          # ⭐ DP 전 리뷰 F4 — 끝 저장 실패로',
   '            except ZeroDivisionError as e_:                          # ⭐ DP 전 리뷰 F4 — 끝 저장 실패로', "run", RUNR),
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
