"""DG · DH · DI · 정전 복구 · DJ · DK 고침 변이 검사 — 저장소 밖 복사본 (작업자마다 하나) 에서 고친 곳을 하나씩 되돌려 해당 selftest 가
빨개지는지 본다. 작업자 3 개 병렬. 끝나면 복사본은 그대로 두고 (원본 저장소는 안 건드린다) 결과를 한 줄씩 찍는다.
--dry : 변이 자리가 정확히 한 번씩 있는지만 본다 (실행 안 함)."""
import pathlib, subprocess, sys, shutil, os, concurrent.futures as cf

SP = pathlib.Path("/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad")
REPO = pathlib.Path("/home/user/Yonghoon-DEM-DFT")
RUNR, DRVR = "tools/ionic/li2s2_stage1_runner.py", "tools/ionic/melt_quench_uma.py"
N_WORKERS = 3

MUT = [
 # ── 러너 (DG)
 ("R1_terminal_stop", RUNR, [("            if code in TERMINAL_STOPS:", "            if False:")], "run"),
 ("R2_ledger_closes", RUNR, [("        if closed:\n            return stop(\"melt\"", "        if False:\n            return stop(\"melt\"")], "run"),
 ("R3_cleanup_paths", RUNR, [("            cl = stop_child(f\"러너 중단 ({why})\") or {\"group_empty\": True, \"left\": []}", "            cl = {\"group_empty\": True, \"left\": []}"),
                             ("            stop_child(\"러너가 끝난다\")", "            pass")], "run"),
 ("R4_launch_ledger", RUNR, [("            led[\"runs\"].append(ent); state[\"entry\"], state[\"t0\"] = ent, t0\n            save_ledger()", "            led[\"runs\"].append(ent); state[\"entry\"], state[\"t0\"] = ent, t0\n            pass"), ("            save_ledger()                                    # ⭐ 띄운 직후", "            pass                                             # ⭐ 띄운 직후")], "run"),
 ("R5_inrun_cap", RUNR, [("                if cum + el >= cap:                          # ⭐ 실행 중 상한", "                if False:                          # ⭐ 실행 중 상한")], "run"),
 ("R6_rejudge", RUNR, [("                now_ = mq.stage1_verdict(rd, values=vals, log=lambda *m: None, reason=\"러너 재시작 — 판정 파일을 믿지 않고 원자료로 다시 판정\")",
                        "                now_ = json.loads((rd / \"stage1_verdict.json\").read_text(encoding=\"utf-8\"))")], "run"),
 ("R7_flock", RUNR, [("            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)", "            pass")], "run"),
 ("R8_order_check", RUNR, [("        bad = check_order(order, vals)", "        bad = []")], "run"),
 ("R9_orphan_alive", RUNR, [("                if alive is not False:", "                if alive is True:")], "run"),
 ("R10_ack_match", RUNR, [("            if a.ack_stop != sp.get(\"stop_id\"):", "            if False:")], "run"),
 ("R11_cap_ack", RUNR, [("            if code == \"cap\" and not (cap_base > float(sp.get(\"cap_h\", cap_base)) + 1e-9):", "            if False:")], "run"),
 ("R12_melt_kill", RUNR, [("                    if mw[\"verdict\"] in (\"fail\", \"invalid\"):", "                    if False:")], "run"),
 ("R13_cmd_repr", RUNR, [("    return str(int(x)) if x.is_integer() and abs(x) < 1e15 else repr(x)", "    return f\"{x:g}\"")], "run"),
 ("R14_term_leader_only", RUNR, [("        if self.p.returncode is None or members() != []:\n            send(signal.SIGTERM, \"TERM\")", "        if self.p.returncode is None:\n            self.p.terminate(); sent.append(\"TERM\")")], "run"),
 # ── 러너 (DH)
 ("R15_empty_ledger_guard", RUNR, [("            if outs:                                         # ⭐ 회신 DH P0-1", "            if False:                                         # ⭐ 회신 DH P0-1")], "run"),
 ("R16_orphan_lower_bound", RUNR, [("                hi = _orphan_upper_hours(ent, recovery_clock())", "                hi = lo")], "run"),
 ("R17_kill_leader_only", RUNR, [("        if self.p.returncode is None or members() != []:\n            send(signal.SIGKILL, \"KILL\")", "        if self.p.returncode is None:\n            send(signal.SIGKILL, \"KILL\")")], "run"),
 ("R19_finish_ignores_group", RUNR, [("        if cleanup is not None and not cleanup.get(\"group_empty\"):", "        if False:")], "run"),
 ("R20_no_cleanup_after_finish", RUNR, [("            cl = stop_child(\"담금질 대표가 끝났다 — 그룹에 남은 프로세스까지 정리\")", "            cl = None; state[\"h\"] = None")], "run"),
 ("R21_invalid_as_melt", RUNR, [("                        if v.get(\"closes_system\"):                  # 과학적 종료", "                        if True:                  # 과학적 종료")], "run"),
 ("R22_summary_invalid_as_track", RUNR, [("            if sm[\"track\"] == \"invalid\":\n                return stop(\"invalid\", f\"묶음 판정 invalid", "            if sm[\"track\"] == \"invalid\":\n                return stop(\"track\", f\"묶음 판정 invalid")], "run"),
 ("R23_no_run_id", RUNR, [("+ ([\"--run_id\", run_id] if run_id else [])", "+ []")], "run"),
 # ── 드라이버 (DG)
 ("D1_plan_missing", DRVR, [("    except FileNotFoundError:\n        return done(\"incomplete\", \"plan.json 이 아직 없다", "    except KeyError:\n        return done(\"incomplete\", \"plan.json 이 아직 없다")], "drv"),
 ("D2_species", DRVR, [("    sp_why = _species_check(frames, plan, v)", "    sp_why = []")], "drv"),
 ("D3a_estimator_check", DRVR, [("    if mw.get(\"estimator\") != MELT_WINDOW_ESTIMATOR:     # 회신 DG P1-7", "    if False:     # 회신 DG P1-7")], "drv"),
 ("D3b_estimator_validate", DRVR, [("        if mw.get(\"estimator\") != MELT_WINDOW_ESTIMATOR:\n            bad.append(f\"melt_window.estimator", "        if False:\n            bad.append(f\"melt_window.estimator")], "drv"),
 ("D4_same_nan", DRVR, [("    if not (_fin(a) and _fin(b)):\n        return False\n    a, b = float(a), float(b)", "    if not (_fin(a) and _fin(b)):\n        return True\n    a, b = float(a), float(b)")], "drv"),
 ("D5_software", DRVR, [("    for k in (\"model\", \"task\"):\n        if sw.get(k) != req.get(k):", "    for k in ():\n        if sw.get(k) != req.get(k):"), ("    for k in req.get(\"versions_present\") or []:", "    for k in []:")], "drv"),
 ("D6_pressure_cols", DRVR, [("        cols_ok = len(p_cols) == 2 and all(", "        cols_ok = len(p_cols) >= 1 and all(")], "drv"),
 ("D7_final_wiring", DRVR, [("            checks[\"final_structure\"] = final_structure_check(run, plan, v, raw_last)", "            pass")], "run"),
 ("D8_all_decided", DRVR, [("                  else \"pass\" if (n_open == 0 and n_pass >= need) else \"pending\")", "                  else \"pass\" if (n_pass >= need) else \"pending\")")], "drv"),
 ("D9_unknown_status", DRVR, [("            if x not in LI2S2_STATUSES and x != \"missing\":", "            if False:")], "drv"),
 ("D10_closes_summary", DRVR, [("            if vv is not None and vv.get(\"closes_system\") is True:", "            if False:")], "drv"),
 ("D11_provenance", DRVR, [("            if pv.get(\"files_sha256\") != run_provenance(rd):", "            if False:")], "run"),
 ("D12_cost_cap", DRVR, [("    over = bool(cost is not None and not (", "    over = False and bool(cost is not None and not (")], "drv"),
 ("D13_closes_combine", DRVR, [("    closes = bool(first is not None and plan.get(\"seed\") == first and mv == \"fail\" and not reasons[\"invalid\"])", "    closes = False")], "drv"),
 ("D14_unknown_melt", DRVR, [("    elif mv != \"pass\":                                     # 회신 DG P1-7", "    elif False:  # 회신 DG P1-7")], "drv"),
 ("D15_traj_frames", DRVR, [("    tf = checks.get(\"traj_frames\")", "    tf = None")], "drv"),
 ("D16_thermo_header", DRVR, [("    if th is not None and not th.get(\"ok\"):\n        reasons[\"invalid\"].append(f\"thermo.csv 열", "    if False:\n        reasons[\"invalid\"].append(f\"thermo.csv 열")], "drv"),
 ("D17_first_seed_validate", DRVR, [("        if not isinstance(seeds, list) or not seeds or v.get(\"first_seed\") != seeds[0]:", "        if False:")], "drv"),
 ("D18_gate_target", DRVR, [("        if not _same(gate.get(\"target_density_g_cm3\"), tgt, rel=0.0, abs_=1e-6):\n            reasons[\"invalid\"].append(f\"gate_check 목표 밀도", "        if False:\n            reasons[\"invalid\"].append(f\"gate_check 목표 밀도")], "drv"),
 ("D19_composition", DRVR, [("    if want_comp is None or plan.get(\"composition\") != want_comp:\n        reasons[\"invalid\"].append(f\"조성 plan", "    if False:\n        reasons[\"invalid\"].append(f\"조성 plan")], "drv"),
 ("D20_summary_ledger", DRVR, [("    res = summarize_stage1(ver, v, cost=ledger_check(root, ver, v))", "    res = summarize_stage1(ver, v, cost={\"total_h\": 0.0, \"cap_h\": 1e9})")], "run"),
 ("D21_card_vals_sha", DRVR, [("            if pv.get(\"card_values_sha16\") != cur_vals:", "            if False:")], "run"),
 # ── 드라이버 (DH)
 ("D22_ledger_missing_run", DRVR, [("        if r is None:\n            invalid.append(f\"{s}{sd} 판정의 run_id {rid[:8]} 가 장부에 없다", "        if False:\n            invalid.append(f\"{s}{sd} 판정의 run_id {rid[:8]} 가 장부에 없다")], "run"),
 ("D23_ledger_negative", DRVR, [("        if not (_fin(w) and float(w) >= 0.0):", "        if not _fin(w):")], "run"),
 ("D24_ledger_unfinished", DRVR, [("        if r.get(\"end\") is None:\n            pending.append(", "        if False:\n            pending.append(")], "run"),
 ("D25_ledger_basis", DRVR, [("        if r.get(\"cost_basis\") not in COST_BASES:", "        if False:")], "run"),
 ("D26_identity_folder", DRVR, [("    elif (plan.get(\"system\"), plan.get(\"seed\")) != (fs, fsd):", "    elif False:")], "drv"),
 ("D27_dup_run_id", DRVR, [("                if vv.get(\"run_id\") in dup:", "                if False:")], "drv"),
 ("D28_slot_check", DRVR, [("                if vv.get(\"system\") is not None and (vv.get(\"system\"), vv.get(\"seed\")) != (s, sd):", "                if False:")], "drv"),
 ("D29_ledger_mapping", DRVR, [("        elif (r.get(\"system\"), r.get(\"seed\")) != (s, sd):", "        elif False:")], "run"),
 ("D30_history", DRVR, [("        h = _append_history(run, prev, res, reason)\n", "        h = {\"prev_status\": prev.get(\"status\"), \"changed\": {}}\n")], "run"),
 # ── DI (Codex 패치)
 ("DI3_archive_cost_join", DRVR, [("        if r is None:\n            invalid.append(f\"보존 포함 실행", "        if False:\n            invalid.append(f\"보존 포함 실행")], "run"),
 ("DI5_proc_error_swallowed", RUNR, [("                except (OSError, ValueError) as e:\n                    errors.append(f\"{d.name}: {type(e).__name__}\"); continue", "                except (OSError, ValueError) as e:\n                    continue")], "run"),
 ("DI6_cleanup_time_omitted", RUNR, [("            cl = stop_child(\"담금질 대표가 끝났다 — 그룹에 남은 프로세스까지 정리\")\n            el = (clock() - t0) / 3600.0", "            el = (clock() - t0) / 3600.0\n            cl = stop_child(\"담금질 대표가 끝났다 — 그룹에 남은 프로세스까지 정리\")")], "run"),
 ("DI7_wallclock_default", RUNR, [("deps.get(\"clock\", time.monotonic)", "deps.get(\"clock\", time.time)")], "run"),
 ("DI8_cross_boot_accepted", RUNR, [("    if any(not start.get(k) or start.get(k) != now.get(k) for k in keys):\n        return None", "    if False:\n        return None")], "run"),
 ("DI9_no_attempt_file", RUNR, [("            _write_json_atomic(rd / mq.ATTEMPT_NAME, {", "            (lambda *a_, **k_: None)(rd / mq.ATTEMPT_NAME, {")], "run"),
 ("DI10_unknown_as_dead", RUNR, [("        return None  # unknown is not dead; restart refuses it", "        return False")], "run"),
 # ── 정전 복구 (이어지는 것)
 ("O6_unknown_cost_stop", RUNR, [("        if unk:", "        if False:")], "run"),
 ("O9_consumer_rerun_after_verdict", DRVR, [("            if pk == \"scientific\":", "            if False:")], "run"),
 ("O10_consumer_retry_limit", DRVR, [("        if n_int > max_int:", "        if False:")], "run"),
 ("O11_consumer_attest_evidence", DRVR, [("            if bad:\n                invalid.append(f\"{key} 런 증언 상한 — \"", "            if False:\n                invalid.append(f\"{key} 런 증언 상한 — \"")], "run"),
 ("O12_interrupted_stop_run_id", RUNR, [("                 + \" · 그 시드 폴더는 사람이 정한다\", cleanup=cl, run_id=ent_rid)", "                 + \" · 그 시드 폴더는 사람이 정한다\", cleanup=cl)")], "run"),
 ("O13_resume_stop_run_id", RUNR, [("폴더 안 옆으로 옮기고 이 STOP 을 확인)\", sys=sysn, seed=seed, run_id=_folder_run_id(rd))", "폴더 안 옆으로 옮기고 이 STOP 을 확인)\", sys=sysn, seed=seed)")], "run"),
 # ── DJ (소비자 · 드라이버)
 ("J1_retry_of_optional", DRVR, [("            if r.get(\"retry_of\") != p_.get(\"run_id\"):", "            if r.get(\"retry_of\") is not None and r.get(\"retry_of\") != p_.get(\"run_id\"):")], "run"),
 ("J2_count_by_field", DRVR, [("            if kind == \"interrupted\":\n                n_int += 1", "            if r.get(\"retry_kind\") == \"interrupted\":\n                n_int += 1")], "run"),
 ("J3_retry_kind_unchecked", DRVR, [("            if r.get(\"retry_kind\") != kind:", "            if False:")], "run"),
 ("J4_receipt_unbound", DRVR, [("            if not (h and h.get(\"acked_at\") and h.get(\"run_id\") == p_.get(\"run_id\") and h.get(\"code\") in RETRY_BIND_CODES[kind]):",
                               "            if not (h and h.get(\"acked_at\") and h.get(\"code\") in RETRY_BIND_CODES[kind]):")], "run"),
 ("J5_consumer_no_declaration", DRVR, [("                if dp:\n                    invalid.append(f\"{tag}: 재시도 선언 — \"", "                if False:\n                    invalid.append(f\"{tag}: 재시도 선언 — \"")], "run"),
 ("J6_attempt_mismatch_ignored", DRVR, [("            elif att is not None and any(att.get(f_) != r.get(f_) for f_ in fields):", "            elif False:")], "run"),
 ("J7_attempt_file_optional", DRVR, [("            if inv_rec is not None and att is None:", "            if False:")], "run"),
 ("J8_unreadable_prev_verdict", DRVR, [("            if pk == \"unreadable\":\n                invalid.append(f\"{tag}: 앞 실행", "            if False:\n                invalid.append(f\"{tag}: 앞 실행")], "run"),
 ("J9_ledger_to_folder", DRVR, [("        if rid not in inventory:\n            invalid.append(f\"장부의", "        if False:\n            invalid.append(f\"장부의")], "run"),
 ("J10_md_complete_retry_ok", DRVR, [("            elif kind == \"interrupted\" and st_p in (\"final\", \"md_complete\"):", "            elif kind == \"interrupted\" and st_p in (\"final\",):")], "run"),
 ("J11_consumer_rejudge_off", DRVR, [("                                          rejudge_needed=(kind == \"invalid\" and st_ in (\"final\", \"md_complete\")))", "                                          rejudge_needed=False)")], "run"),
 ("J12_attest_lower_validity", DRVR, [("            if not (_fin(lo) and _fin(hb) and float(lo) >= 0 and float(hb) >= 0 and float(lo) >= float(hb) - 1e-9):", "            if False:")], "run"),
 ("J13_attest_any_status", DRVR, [("            if r.get(\"status\") != \"orphaned\":\n                bad.append(", "            if False:\n                bad.append(")], "run"),
 ("J17_cap_reason_rule", DRVR, [("    elif prev_status == \"cap\" and reason not in cap_r:", "    elif False:")], "run"),
 ("J18_reason_allowlist", DRVR, [("    if reason not in allowed:\n        why.append(", "    if False:\n        why.append(")], "run"),
 ("J20_unknown_verdict_status", DRVR, [("    return st if st in LI2S2_STATUSES else \"unreadable\"", "    return st")], "drv"),
 ("J21_cap_reasons_validate", DRVR, [("        if not (isinstance(cr, list) and cr and isinstance(rr_, dict) and set(cr) <= set(rr_.get(\"interrupted\") or [])", "        if True or not (isinstance(cr, list) and cr and isinstance(rr_, dict) and set(cr) <= set(rr_.get(\"interrupted\") or [])")], "drv"),
 ("J22_heartbeat_at_attest", DRVR, [(" and _same(at.get(\"heartbeat_at_attest\"), hb, rel=0.0, abs_=1e-9)):", "):")], "run"),
 # ── DJ (러너)
 ("K1_ledger_scientific", RUNR, [("        if v in (\"pass\", \"fail\"):\n            return {\"ok\": False, \"code\": \"invalid\", \"why\": f\"이전 실행 {tag} 에 과학적 판정", "        if False:\n            return {\"ok\": False, \"code\": \"invalid\", \"why\": f\"이전 실행 {tag} 에 과학적 판정")], "run"),
 ("K2_invalid_skips_folder", RUNR, [("        rec = inventory.get(rid) if isinstance(rid, str) else None\n", "        if v == \"invalid\":\n            kinds.append(\"invalid\"); stages.append(\"md_incomplete\"); continue\n        rec = inventory.get(rid) if isinstance(rid, str) else None\n")], "run"),
 ("K3_unreadable_as_none", RUNR, [("        if rk == \"unreadable\":", "        if False:")], "run"),
 ("K4_fire_hold_off", RUNR, [("            if st == \"md_complete\":", "            if False:")], "run"),
 ("K5_stage_unreadable_off", RUNR, [("        if st == \"unreadable\":\n            return {\"ok\": False, \"code\": \"resume\", \"why\": f\"이전 실행 {tag} 폴더의 완료 단계", "        if False:\n            return {\"ok\": False, \"code\": \"resume\", \"why\": f\"이전 실행 {tag} 폴더의 완료 단계")], "run"),
 ("K6_no_count", RUNR, [("            n_int += 1\n        kinds.append(kind); stages.append(st)", "            pass\n        kinds.append(kind); stages.append(st)")], "run"),
 ("K7_declaration_ignored", RUNR, [("    good = [h for h, pr in bound if not pr]", "    good = [h for h, pr in bound]")], "run"),
 ("K8_receipt_any_run", RUNR, [("for h in stop_history if h.get(\"acked_at\") and h.get(\"run_id\") == prev.get(\"run_id\") and h.get(\"code\") in codes]", "for h in stop_history if h.get(\"acked_at\") and h.get(\"code\") in codes]")], "run"),
 ("K9_receipt_any_code", RUNR, [("for h in stop_history if h.get(\"acked_at\") and h.get(\"run_id\") == prev.get(\"run_id\") and h.get(\"code\") in codes]", "for h in stop_history if h.get(\"acked_at\") and h.get(\"run_id\") == prev.get(\"run_id\")]")], "run"),
 ("K10_runner_rejudge_off", RUNR, [("    rejudge = kind == \"invalid\" and st in (\"final\", \"md_complete\")", "    rejudge = False")], "run"),
 ("K11_ack_unvalidated", RUNR, [("                if dprob:\n                    log(f\"⛔ 재시도 선언을 받지 않는다", "                if False:\n                    log(f\"⛔ 재시도 선언을 받지 않는다")], "run"),
 ("K12_ack_rejudge_off", RUNR, [("    return mq.declaration_problems(decl, kind, values, rejudge_needed=(kind == \"invalid\" and st in (\"final\", \"md_complete\")),", "    return mq.declaration_problems(decl, kind, values, rejudge_needed=False,")], "run"),
 ("K13_declaration_not_stored", RUNR, [("            led[\"stop_history\"].append({**sp, \"acked_at\": _now(), **({\"declaration\": decl} if decl else {})})", "            led[\"stop_history\"].append({**sp, \"acked_at\": _now()})")], "run"),
 ("K14_attest_reads_before_lock", RUNR, [("    if deps.get(\"before_lock\"):\n        deps[\"before_lock\"]()", "    _pre = json.loads(led_p.read_text(encoding=\"utf-8\"))\n    if deps.get(\"before_lock\"):\n        deps[\"before_lock\"]()"),
                                         ("        led = json.loads(led_p.read_text(encoding=\"utf-8\"))  # ⭐ 잠금 안에서 다시 읽는다", "        led = _pre  # ⭐ 잠금 안에서 다시 읽는다")], "run"),
 ("K16_attest_lower_off", RUNR, [("        if not (_finite_nonneg(lo) and _finite_nonneg(hb) and lo >= hb - 1e-9):", "        if False:")], "run"),
 ("K17_attest_zero_ok", RUNR, [("        if not (math.isfinite(h) and h > 0 and h >= float(lo)):", "        if not (math.isfinite(h) and h >= float(lo)):")], "run"),
 ("K18_attest_fields_off", RUNR, [("        if miss:\n            return 10, {\"why\": f\"근거 필드가", "        if False:\n            return 10, {\"why\": f\"근거 필드가")], "run"),
 ("K23_attempt_no_retry_fields", RUNR, [("                                                     \"retry_of\": retry_of, \"retry_stop_id\": retry_stop, \"retry_kind\": retry_kind})", "                                                     })")], "run"),
 ("K24_final_retry_ok", RUNR, [("            if st == \"final\":\n                return {\"ok\": False, \"code\": \"resume\", \"why\": f\"이전 실행 {tag} 이 끝까지 돌았다", "            if False:\n                return {\"ok\": False, \"code\": \"resume\", \"why\": f\"이전 실행 {tag} 이 끝까지 돌았다")], "run"),
 ("K25_limit_off", RUNR, [("    if n_int > lim:", "    if False:")], "run"),
 ("K26_folder_scientific", RUNR, [("        if rk == \"scientific\":", "        if False:")], "run"),
 ("K27_cost_unconfirmed_ok", RUNR, [("        if x.get(\"end\") is None or x.get(\"cost_basis\") not in mq.COST_BASES:", "        if False:")], "run"),
 # ── DJ 뒤판 (확인 단계) — 코드가 바뀐 자리
 ("K11b_ack_unvalidated", RUNR, [("                if dprob:\n                    log(f\"⛔ 재시도 선언을 받지 않는다", "                if False:\n                    log(f\"⛔ 재시도 선언을 받지 않는다")], "run"),
 ("K12b_ack_rejudge_off", RUNR, [("    return mq.declaration_problems(decl, kind, values, rejudge_needed=(kind == \"invalid\" and st in (\"final\", \"md_complete\")),", "    return mq.declaration_problems(decl, kind, values, rejudge_needed=False,")], "run"),
 ("K28_ack_kind_from_code", RUNR, [("    kind = mq.run_kind(hit[0], rec[\"path\"] if rec else None)", "    kind = next((k for k, cs in mq.RETRY_BIND_CODES.items() if code in cs), \"interrupted\")")], "run"),
 ("K29_orphan_declaration_dropped", RUNR, [("        elif declaration_from_args(a) is not None:", "        elif False:")], "run"),
 ("K30_ack_binding_off", RUNR, [("    if code not in mq.RETRY_BIND_CODES[kind]:\n        return [f\"이 멈춤 ({code}) 은 이 실행", "    if False:\n        return [f\"이 멈춤 ({code}) 은 이 실행")], "run"),
 # ── DK
 ("L1_no_md_done_write", DRVR, [("    write_md_done(out, run_id=run_id, n_steps_planned=n_m + n_q + n_h, n_steps_done=step)", "    pass")], "drv"),
 ("L2_marker_traj_sha_off", DRVR, [("              and (f / \"traj.xyz\").is_file() and rec.get(\"traj_sha256\") == _sha256_file(f / \"traj.xyz\")\n", "\n")], "run"),
 ("L3_marker_thermo_sha_off", DRVR, [("              and (f / \"thermo.csv\").is_file() and rec.get(\"thermo_sha256\") == _sha256_file(f / \"thermo.csv\"))", "              )")], "drv"),
 ("L4_marker_runid_off", DRVR, [("and isinstance(rid, str) and rid and rec.get(\"run_id\") == rid", "")], "drv"),
 ("L5_marker_steps_off", DRVR, [("              and rec[\"n_steps_planned\"] == want and rec[\"n_steps_done\"] == want\n", "\n")], "drv"),
 ("L6_missing_marker_complete", DRVR, [("    if not md.is_file():\n        return \"md_incomplete\"", "    if not md.is_file():\n        return \"md_complete\"")], "run"),
 ("L7_bad_marker_incomplete", DRVR, [("    return \"md_complete\" if ok else \"unreadable\"", "    return \"md_complete\" if ok else \"md_incomplete\"")], "run"),
 ("L8_run_kind_ledger_only", DRVR, [("    vfs = verdict_file_status(folder) if folder else None\n    if v in (\"pass\", \"fail\") or vfs in (\"pass\", \"fail\"):\n        return \"scientific\"", "    vfs = None\n    if v in (\"pass\", \"fail\") or vfs in (\"pass\", \"fail\"):\n        return \"scientific\"")], "run"),
 ("L9_attest_positive_off", DRVR, [("            if not float(w) > 0:", "            if False:")], "run"),
 ("L10_gone_keys_ok", DRVR, [("            if gone in v:", "            if False:")], "drv"),
 ("L11_ack_unreadable_ok", RUNR, [("    if kind == \"unreadable\":\n        return [\"이 실행의 판정을 못 읽는다", "    if False:\n        return [\"이 실행의 판정을 못 읽는다")], "run"),
 ("L12_ack_scientific_ok", RUNR, [("    if kind == \"scientific\":\n        return [\"이 실행에는 과학적 판정", "    if False:\n        return [\"이 실행에는 과학적 판정")], "run"),
 ("L13_runner_kind_ledger_only", RUNR, [("        rk = mq.run_kind(x, rec[\"path\"])", "        rk = mq.run_kind(x, None)")], "run"),
 ("L14_consumer_kind_ledger_only", DRVR, [("            pk = run_kind(p_, pf)", "            pk = run_kind(p_, None)")], "run"),
]


def check_anchors():
    bad = []
    for name, rel, reps, _ in MUT:
        s = (REPO / rel).read_text(encoding="utf-8")
        for old, _new in reps:
            n = s.count(old)
            if n != 1:
                bad.append(f"{name}: 자리 {n} 개 — {old[:70]!r}")
            s = s.replace(old, _new, 1) if n == 1 else s
    return bad


def make_mirror(i):
    m = SP / f"mut_dk_w{i}"
    if m.exists():
        shutil.rmtree(m)
    (m / "tools").mkdir(parents=True)
    shutil.copytree(REPO / "tools", m / "tools", dirs_exist_ok=True)
    os.symlink(REPO / "db", m / "db")
    return m


def run_one(args):
    (name, rel, reps, which), m = args
    f = m / rel
    orig = f.read_text(encoding="utf-8")
    try:
        s = orig
        for old, new in reps:
            if s.count(old) != 1:
                return f"{name:<30s} ⚠ 변이 자리 {s.count(old)} 개"
            s = s.replace(old, new, 1)
        try:
            compile(s, str(f), "exec")
        except SyntaxError as e:
            return f"{name:<30s} ⚠ 변이가 문법 오류 ({e.msg}) — 무효 변이"
        f.write_text(s, encoding="utf-8")
        tgt = m / (RUNR if which == "run" else DRVR)
        env = {**os.environ, "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"}
        r = subprocess.run([sys.executable, str(tgt), "--selftest"], capture_output=True, text=True, timeout=1800, cwd=str(m), env=env)
        out = r.stdout + r.stderr
        reds = [ln for ln in out.splitlines() if ln.startswith("  ⛔ ")]
        tail = out.strip().splitlines()[-1][:140] if out.strip() else ""
        verdict = "⭕ 빨강" if r.returncode != 0 else "⛔ 초록 (못 잡음)"
        return f"{name:<30s} {verdict} · {(reds[0][:150] if reds else tail)}"
    finally:
        f.write_text(orig, encoding="utf-8")


if __name__ == "__main__":
    bad = check_anchors()
    if bad:
        print("\n".join(bad)); sys.exit(2)
    print(f"변이 {len(MUT)} 개 · 자리 모두 한 번씩", flush=True)
    if "--dry" in sys.argv:
        sys.exit(0)
    mirrors = [make_mirror(i) for i in range(N_WORKERS)]
    import queue, threading
    q = queue.Queue()
    for mu in MUT:
        q.put(mu)
    lock = threading.Lock()
    results = []
    def worker(m):
        while True:
            try:
                mu = q.get_nowait()
            except queue.Empty:
                return
            line = run_one((mu, m))
            with lock:
                results.append(line); print(line, flush=True)
    ts = [threading.Thread(target=worker, args=(m,)) for m in mirrors]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    n_red = sum(1 for x in results if "⭕ 빨강" in x)
    print(f"끝: 빨강 {n_red} / {len(MUT)}", flush=True)
