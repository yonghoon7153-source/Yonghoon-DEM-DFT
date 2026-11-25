"""DG · DH · DI · 정전 복구 · DJ · DK · DL · DM · DN · DO 전 리뷰 고침 변이 검사 — DN 판 (../li2s2_dn_mutation_2026_11_04/dn_mutate.py) 의 174 개를
가져오되 DO 전 리뷰 고침으로 자리가 바뀐 10 개는 새 자리로 옮기고, DO 전 리뷰 고침 자리 (DO1–) 를 더한다. 실행 · 판정은 DL 판과 같다 (저장소 밖
복사본 3 개 · 작업자 3 개 · which = run / drv / both). --dry : 자리만 · --only=접두 : 그 접두의 변이만 (쉼표로 여럿) · --tag=이름 : 복사본 폴더 이름 (기본 do — 돌고 있는 실행과 겹치지 않게 재실행 때 바꾼다) ·
--failfast : 러너 selftest 를 첫 빨강에서 멈춘다 (빨강 · 초록 판정은 같다 — 초록은 끝까지 돈다 · 첫 빨강 줄도 같다) · --workers=N."""
import importlib.util, pathlib, sys

REPO = pathlib.Path("/home/user/Yonghoon-DEM-DFT")
_spec = importlib.util.spec_from_file_location("dn_mutate", REPO / "db/raw/li2s2_dn_mutation_2026_11_04/dn_mutate.py")
dn = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dn)
dl = dn.dl
RUNR, DRVR = dl.RUNR, dl.DRVR

MOVED = {
 "R4_launch_ledger": ("R4_launch_ledger", RUNR, [
     ("            led[\"runs\"].append(ent); state[\"entry\"], state[\"t0\"] = ent, t0\n            save_ledger()",
      "            led[\"runs\"].append(ent); state[\"entry\"], state[\"t0\"] = ent, t0\n            pass"),
     ("                save_ledger()                                # ⭐ 띄운 직후", "                pass                                         # ⭐ 띄운 직후")], "run"),
 "R11_cap_ack": ("R11_cap_ack", RUNR, [("            if code == \"cap\" and not (_is_num(sp.get(\"cap_h\")) and cap_base > float(sp[\"cap_h\"]) + 1e-9):",
                                         "            if False:")], "run"),
 "R21_invalid_as_melt": ("R21_invalid_as_melt", RUNR, [("                        if mw[\"verdict\"] == \"fail\":                  # 과학적 종료",
                                                         "                        if True:                  # 과학적 종료")], "run"),
 "D10_closes_summary": ("D10_closes_summary", DRVR, [("            if vv is not None and vv.get(\"closes_system\") is True and sd not in closed:",
                                                       "            if False:")], "drv"),
 "K13_declaration_not_stored": ("K13_declaration_not_stored", RUNR, [("                                            **({\"declaration\": decl} if decl else {})})",
                                                                       "                                            })")], "run"),
 "K28_ack_kind_from_code": ("K28_ack_kind_from_code", RUNR, [("    kind = mq.run_kind(hit[0], rec[\"path\"] if rec else None, values)",
                                                               "    kind = next((k for k, cs in mq.RETRY_BIND_CODES.items() if code in cs), \"interrupted\")")], "run"),
 "L8_run_kind_ledger_only": ("L8_run_kind_ledger_only", DRVR, [("    recs, prob = _verdict_records(folder) if folder else ([], None)",
                                                                 "    recs, prob = [], None")], "run"),
 "L13_runner_kind_ledger_only": ("L13_runner_kind_ledger_only", RUNR, [("        rk = mq.run_kind(x, rec[\"path\"], values)",
                                                                         "        rk = mq.run_kind(x, None, values)")], "run"),
 "L14_consumer_kind_ledger_only": ("L14_consumer_kind_ledger_only", DRVR, [("            pk = run_kind(p_, pf, values)",
                                                                             "            pk = run_kind(p_, None, values)")], "run"),
 "DN8_container_type_off": ("DN8_container_type_off", DRVR, [("    for key in (\"gate_check\", \"checks\", \"history\"):\n        p = bad(r, key, (dict,), where)",
                                                               "    for key in ():\n        p = bad(r, key, (dict,), where)")], "drv"),
}
F = lambda name, anchor, repl, which="drv", where=DRVR: (name, where, [(anchor, repl)], which)
NEW = [
 # ── 드라이버: 수 · plan 일정 · 진행 파일 · 폴더 파일 목록 · 예외
 F("DO1_fin_accepts_str", "    if isinstance(x, bool) or not isinstance(x, numbers.Real):", "    if isinstance(x, bool):", "both"),
 F("DO2_plan_num_coerce", "    if not _fin(x) or not (float(x) > 0 if positive else float(x) >= 0) or float(x) > PLAN_NUM_MAX:", "    if False:"),
 F("DO3_thermo_all_nul_ok", "        if raw:                                        # ⭐ DO 전 리뷰 F7", "        if False:                                        # ⭐ DO 전 리뷰 F7"),
 F("DO4_traj_all_nul_ok", "    if last < 0 and raw:", "    if False:"),
 F("DO5_mid_allowlist_off", "    if extra:                                                # ⭐ DO 전 리뷰 F1", "    if False:                                                # ⭐ DO 전 리뷰 F1", "both"),
 F("DO6_final_lexists_off", "    if any(os.path.lexists(f / x) for x in (\"result.json\", \"final.xyz\")):", "    if False:"),
 F("DO7_stage_exception_crash", "    except Exception as e:                                   # ⭐ DO 전 리뷰 F6", "    except ZeroDivisionError as e:                                   # ⭐ DO 전 리뷰 F6"),
 # ── 드라이버: 판정 기록
 F("DO8_prerun_keys_loose", "    if not isinstance(v, dict) or v.get(\"status\") != \"incomplete\" or not set(v) <= PRE_RUN_VERDICT_KEYS:",
   "    if not isinstance(v, dict) or v.get(\"status\") != \"incomplete\":"),
 F("DO9_hist_line_consistency_off", "            if isinstance(pv_, dict) and (\"prev_status\" in h and h.get(\"prev_status\") != pv_.get(\"status\")",
   "            if False and (\"prev_status\" in h and h.get(\"prev_status\") != pv_.get(\"status\")"),
 F("DO10_gate_error_ok", "    if (r.get(\"gate_check\") or {}).get(\"error\"):", "    if False:"),
 F("DO11_final_traces_off", "                for k_, why_ in ((\"final_structure\", \"최종 구조 판정\"), (\"seed_gate_error\", \"시드 게이트 오류\")):",
   "                for k_, why_ in ():"),
 F("DO12_plan_frames_off", "                if type(n_) is int and ex_ is None and plan_frames and n_ >= plan_frames:", "                if False:"),
 F("DO13_history_summary_off", "                if (r.get(\"history\") or {}).get(\"prev_status\") in (\"pass\", \"fail\"):", "                if False:"),
 F("DO14_history_status_type_off", "    p = bad(r.get(\"history\") or {}, \"prev_status\", (str,), f\"{where} 의 history\")", "    p = None"),
 # ── 드라이버: 판정 함수 (프레임 · thermo · 보존 폴더 · 녹음 규칙)
 ("DO15_xyz_frames_strict", DRVR, [("            if nat0 is not None and last - i + 1 < nat0 + 2:   # 꼬리에서 머리째 덜 써짐 — 세지 않는다\n                return n",
                                    "            if nat0 is not None and last - i + 1 < nat0 + 2:   # 꼬리에서 머리째 덜 써짐 — 세지 않는다\n                return None"),
                                   ("        if i + nat + 1 > last:                               # 덜 써진 마지막 프레임 — 세지 않는다\n            return n",
                                    "        if i + nat + 1 > last:                               # 덜 써진 마지막 프레임 — 세지 않는다\n            return None")], "both"),
 F("DO16_read_thermo_junk_kept", "    lines = [ln for ln in pathlib.Path(path).read_bytes().decode(\"utf-8\", errors=\"replace\").split(\"\\n\") if not _junk(ln)]",
   "    lines = [ln for ln in pathlib.Path(path).read_bytes().decode(\"utf-8\", errors=\"replace\").split(\"\\n\") if ln.strip()]", "both"),
 F("DO17_identity_preserved_off", "        if (m_ and isinstance(att_, dict) and att_.get(\"system\") == rd_.parent.name and type(att_.get(\"seed\")) is int",
   "        if (False and m_ and isinstance(att_, dict) and att_.get(\"system\") == rd_.parent.name and type(att_.get(\"seed\")) is int", "both"),
 F("DO18_rule_m_off", "    elif closes or mv == \"fail\":                         # ⭐ DO 전 리뷰", "    elif closes:                         # ⭐ DO 전 리뷰", "both"),
 F("DO19_gate_error_as_false", "                gate = {\"schedule_complete\": None, \"error\": f\"{type(e).__name__}: {e}\"}",
   "                gate = {\"schedule_complete\": False}", "both"),
 # ── 드라이버: 실행 종류
 F("DO20_kind_invalid_any_status", "    if (v == \"invalid\" or \"invalid\" in sts) and st_ in RUN_STATUSES_ENDED:", "    if (v == \"invalid\" or \"invalid\" in sts):", "both"),
 F("DO21_kind_melt_check_off", "    if v in (\"pass\", \"fail\") or cs is True or (mc or {}).get(\"verdict\") == \"fail\":", "    if v in (\"pass\", \"fail\"):", "both"),
 F("DO22_kind_folder_melt_off", "    if values is not None and folder and os.path.lexists(pathlib.Path(folder) / \"traj.xyz\"):", "    if False:", "both"),
 F("DO23_kind_records_scientific_off", "    if any(x in (\"pass\", \"fail\") for x in sts):\n        return \"scientific\"", "    if False:\n        return \"scientific\"", "both"),
 F("DO24_kind_melt_check_type_off", "    if mc is not None and not (isinstance(mc, dict) and mc.get(\"verdict\") in (\"fail\", \"invalid\")):\n        return \"unreadable\"",
   "    if False:\n        return \"unreadable\""),
 F("DO25_kind_closes_type_off", "    if cs is not None and not isinstance(cs, bool):\n        return \"unreadable\"", "    if False:\n        return \"unreadable\""),
 F("DO26_kind_orphan_status_off", "    st_ = row.get(\"status_before_orphan\") or row.get(\"status\")", "    st_ = row.get(\"status\")"),
 # ── 드라이버: 소비자 장부
 F("DO27_ledger_closing_off", "        if cs is True:                                    # ⭐ DO 전 리뷰 P0", "        if False:                                    # ⭐ DO 전 리뷰 P0", "both"),
 F("DO28_ledger_row_types_off", "        if r.get(\"system\") not in (\"A\", \"B\") or type(r.get(\"seed\")) is not int:", "        if False:", "both"),
 F("DO29_ledger_end_type_off", "        if not (isinstance(r.get(\"end\"), str) and r[\"end\"].strip()):", "        if False:", "both"),
 F("DO30_ledger_bounds_off", "            if any(x is not None and float(w) < float(x) - 1e-9 for x in (hb_, lo_)):", "            if False:", "both"),
 F("DO31_ledger_bound_types_off", "            if any(x is not None and not (_fin(x) and float(x) >= 0) for x in (hb_, lo_)):", "            if False:", "both"),
 F("DO32_ledger_closes_type_off", "        if cs is not None and not isinstance(cs, bool):\n            invalid.append(f\"{key} 런의 closes_system",
   "        if False:\n            invalid.append(f\"{key} 런의 closes_system", "both"),
 F("DO33_ledger_melt_check_type_off", "        if mc is not None and not (isinstance(mc, dict) and mc.get(\"verdict\") in (\"fail\", \"invalid\")):\n            invalid.append(f\"{key} 런의 melt_check",
   "        if False:\n            invalid.append(f\"{key} 런의 melt_check", "both"),
 F("DO34_dup_keys_ok", "    return json.loads(text, object_pairs_hook=_no_dup_pairs)", "    return json.loads(text)", "both"),
 F("DO35_consumer_verdict_crash", "            except (ValueError, UnicodeDecodeError, RecursionError) as e:     # ⭐ DO 전 리뷰 — 잘린 판정에 죽지 않는다",
   "            except ZeroDivisionError as e:     # ⭐ DO 전 리뷰 — 잘린 판정에 죽지 않는다", "both"),
 # ── 러너
 ("DO36_melt_check_not_first", RUNR, [("                        ent[\"melt_check\"] = {\"verdict\": mw[\"verdict\"], \"message\": str(mw.get(\"message\"))[:300], \"at\": _now()}",
                                       "                        pass"),
                                      ("                            ent[\"closes_system\"] = True", "                            pass")], "run"),
 F("DO37_melt_fail_stuck_abnormal", "                            if mw[\"verdict\"] == \"fail\":\n                                return stop(\"melt\"",
   "                            if False:\n                                return stop(\"melt\"", "run", RUNR),
 F("DO38_orphan_status_lost", "                ent.setdefault(\"status_before_orphan\", ent.get(\"status\"))", "                pass", "run", RUNR),
 F("DO39_stop_id_not_required", "                if not (isinstance(sp, dict) and isinstance(sp.get(\"stop_id\"), str) and sp[\"stop_id\"].strip()",
   "                if False and not (isinstance(sp, dict) and isinstance(sp.get(\"stop_id\"), str) and sp[\"stop_id\"].strip()", "run", RUNR),
 F("DO40_stop_unreadable_overwritten", "                log(f\"⛔ STOP.json 을 못 읽는다 ({type(e).__name__}: {str(e)[:80]}) — 원본을 덮어쓰지 않고 시작하지 않는다 (사람이 본다)\")\n                return RC[\"refused\"]",
   "                raise", "run", RUNR),
 F("DO41_stop_keys_all", "                led[\"stop_history\"].append({**{k_: sp[k_] for k_ in STOP_KEYS if k_ in sp}, \"acked_at\": _now(),",
   "                led[\"stop_history\"].append({**sp, \"acked_at\": _now(),", "run", RUNR),
 F("DO42_reboot_alive_ignored", "                alive = False if rebooted else (pg_alive(pg) if pg is not None else None)",
   "                alive = pg_alive(pg) if pg is not None else None", "run", RUNR),
 F("DO43_signal_unmasked", "            hold_sig = hasattr(signal, \"pthread_sigmask\") and threading.current_thread() is threading.main_thread()",
   "            hold_sig = False", "run", RUNR),
 F("DO44_cap_sleep_full", "                sleep(max(1.0, min(a.poll_s, left_s)))", "                sleep(a.poll_s)", "run", RUNR),
 F("DO45_values_pin_off", "    if want_v is not None and mq.values_sha16(vals) != want_v:", "    if False:", "run", RUNR),
 F("DO46_python_check_off", "    if not deps.get(\"python_ok\", lambda x_: shutil.which(x_) is not None)(a.python):", "    if False:", "run", RUNR),
 F("DO47_fsync_off", "        os.fsync(fh.fileno())\n    os.replace(tmp, path)", "        pass\n    os.replace(tmp, path)", "run", RUNR),
 F("DO48_orphan_numbers_loose", "    if not (_is_num(now.get(\"seconds\")) and _is_num(start.get(\"seconds\")) and _is_num(lo_)):", "    if False:", "run", RUNR),
]

MUT = [MOVED.get(m[0], m) for m in dn.MUT] + NEW
dl.MUT = MUT
TAG = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--tag=")), "do")   # 복사본 이름 — 다른 실행과 겹치지 않게 (재실행 때)
def make_mirror(i):
    m = dl.SP / f"mut_{TAG}_w{i}"
    if m.exists():
        dl.shutil.rmtree(m)
    (m / "tools").mkdir(parents=True)
    dl.shutil.copytree(REPO / "tools", m / "tools", dirs_exist_ok=True)
    dl.os.symlink(REPO / "db", m / "db")
    return m
dl.make_mirror = make_mirror
FAILFAST = "--failfast" in sys.argv                          # 러너 selftest 를 첫 빨강에서 멈춘다 (LI2S2_SELFTEST_FAILFAST=1) — 판정 같음 · 시간만
WORKERS = int(next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--workers=")), dl.N_WORKERS))
def _selftest(m, rel):
    env = {**dl.os.environ, "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1",
           **({"LI2S2_SELFTEST_FAILFAST": "1"} if FAILFAST else {})}
    r = dl.subprocess.run([sys.executable, str(m / rel), "--selftest"], capture_output=True, text=True, timeout=1800, cwd=str(m), env=env)
    out = r.stdout + r.stderr
    reds = [ln for ln in out.splitlines() if ln.startswith("  ⛔ ")]
    tail = out.strip().splitlines()[-1][:140] if out.strip() else ""
    return r.returncode, (reds[0][:150] if reds else tail)
dl._selftest = _selftest

if __name__ == "__main__":
    bad = dl.check_anchors()
    if bad:
        print("\n".join(bad)); sys.exit(2)
    names = [mu[0] for mu in MUT]
    assert len(names) == len(set(names)), "변이 이름이 겹친다"
    print(f"변이 {len(MUT)} 개 (DN 판 {len(dn.MUT)} · 자리 옮김 {len(MOVED)} · DO {len(NEW)}) · 자리 모두 한 번씩", flush=True)
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
