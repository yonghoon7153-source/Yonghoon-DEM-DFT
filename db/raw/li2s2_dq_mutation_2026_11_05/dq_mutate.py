"""회신 DP 고침 변이 검사 — DP 판 (../li2s2_dp_mutation_2026_11_04/dp_mutate.py) 의 287 개를 가져오되 DP 고침으로 자리가 바뀐 4 개는
새 자리로 옮기고, DP 고침 자리 (DQ1–) 와 회신 DP P2-2 로 '같은 결과' 설명에서 뺀 직접 진입 엄격 판독 넷 (DQ14–DQ17) 을 더한다.
실행 · 판정은 DL 판과 같다 (저장소 밖 복사본 · 작업자 · which = run / drv / both · 주석 중간 자리는 '  #' 를 붙인다 — DP 판 _keep_comment).
옵션: --dry · --only=접두 (쉼표로 여럿) · --tag=이름 · --failfast · --workers=N.
뺀 것 (같은 결과 — 시험이 못 가르는 것이 맞다 · 회신 DP 표를 따라 범위를 좁혀 적는다):
  · persist_observed 의 즉시 저장 끄기 — **같은 프로세스 안에서는** 끝 처리가 같은 장부를 저장한다. 급작스러운 종료 (kill -9 · 정전) 에서는 다르다 —
    그 경우는 이 시험 틀 (한 프로세스) 로 재현하지 않는다 (즉시 저장은 그 경우를 위한 운영 근거 · 회신 DP Q6).
  · 시드 루프의 판정 상태 엄격 판독 끄기 — 조건부: 바로 앞 ①-4 가 그 판정을 원자료로 **다시 썼을 때만** 같은 열쇠 둘이 남을 수 없다.
    다시 못 쓰면 (written False) ①-4 가 멈춘다 (DQ7 이 그 멈춤을 깬다) — 그래서 루프에 닿는 판정은 늘 새로 쓴 것이다.
  · 확인 경로의 '적기 실패 → 거부' return 끄기 — 그 실행이 과학적이라 선언 문제 목록이 늘 비어 있지 않아 바로 아래가 같은 코드로 거부한다 (회신 DP 동의).
  · 확인 구간 (확인 기록 저장 · STOP 지우기 · 확인 끝 표시) 끄기 — 그 사이 신호로 끊겨도 확인 기록은 저장되고 STOP 이 남아 다음 확인이 같은 기록을
    다시 쓰지 않는다 (같은 결과 · 구간은 기록 정리용).
  · 살아 있는 녹음 멈춤 판정의 지문 기록 (ent verdict_provenance) 끄기 — 그 판정은 일정을 못 마친 런 (담금질을 멈춤) 이라 같은 입력의 재판정이 pass · fail 로
    바뀔 수 없다 (그래서 대체가 일어나지 않는다) · 지문 기록은 일관성용이다.
  · ①-4 확인의 폴더 지문 (ledger_verdict_conflict(…, folder_provenance=…)) 끄기 — persist 가 같은 입력이면 장부 판정을 이미 바꿔 두어 그 뒤 확인에서
    지문이 결과를 가르지 않는다 (같은 입력 → 장부 = 폴더 · 다른 입력 · 기록 없음 → 지문 없이도 충돌).
  · persist 가 과학적 장부 판정과 같이 적는 지문 (DQ66 · 뺐다) — 과학적 장부 판정의 지문은 규칙이 쓰지 않는다 (pass · fail 끼리는 지문과 상관없이 충돌) ·
    대체할 때는 지문이 같은 입력이라 결과가 갈리지 않는다 · 기록용.
  · 판정 구간 안의 장부 저장 (끝 · 녹음 멈춤) 끄기 — 같은 프로세스 안에서는 끝 처리 (finally) 가 메모리 장부 (판정이 적힌) 를 저장한다 · SIGKILL · 정전은
    이 시험 틀로 재현하지 않는다 (그 경우는 장부가 빈 상태를 폴더 앞 판정으로 막는 규칙 — DQ69–DQ77 — 이 맡는다).
  (처음엔 _ledger_check 의 꼴 검사 끄기도 '뒤 원소 검사가 같은 장부를 invalid 로' 라고 뺐는데 틀렸다 — 빈 객체 stop_history ({}) 는 뒤 원소 검사가
   못 본다. 시험 (요약 · stop_history 빈 객체) 을 더하고 DQ18 (소비자) · DQ19 (러너) 로 깬다.)"""
import importlib.util, pathlib, sys

REPO = pathlib.Path("/home/user/Yonghoon-DEM-DFT")
_spec = importlib.util.spec_from_file_location("dp_mutate", REPO / "db/raw/li2s2_dp_mutation_2026_11_04/dp_mutate.py")
dp = importlib.util.module_from_spec(_spec)
_argv = sys.argv; sys.argv = [sys.argv[0]]
_spec.loader.exec_module(dp)
sys.argv = _argv
dl = dp.dl
RUNR, DRVR = dl.RUNR, dl.DRVR

MOVED = {
 # ── DQ 전 독립 리뷰 고침으로 자리가 바뀐 다섯 (뜻 그대로 · 2026-11-05)
 "D10_closes_summary": ("D10_closes_summary", DRVR, [
     ("            elif vv is not None and vv.get(\"closes_system\") is True and sd not in closed:", "            elif False:")], "drv"),
 "DO9_hist_line_consistency_off": ("DO9_hist_line_consistency_off", DRVR, [
     ("            if (\"prev_status\" in h and h.get(\"prev_status\") != pv_.get(\"status\")",
      "            if False and (\"prev_status\" in h and h.get(\"prev_status\") != pv_.get(\"status\")")], "drv"),
 "DO27_ledger_closing_off": ("DO27_ledger_closing_off", DRVR, [
     ("        elif cs is True:                                  # ⭐ DO 전 리뷰 P0", "        elif False:                                  # ⭐ DO 전 리뷰 P0")], "both"),
 "DP48_persist_verdict_off": ("DP48_persist_verdict_off", RUNR, [            # 2차: 대체 규칙 안으로 — 판정을 적지 않는다
     ('                        new_["verdict"], new_["verdict_provenance"] = obs["status"], obs.get("provenance")', '                        pass')], "run"),
 "DP29_kind_verdict_status_off": ("DP29_kind_verdict_status_off", DRVR, [                 # 2차: 관측 상태를 st_sci 로 먼저 계산
     ('        st_sci = "fail" if any(r_.get("status") == "fail" for r_ in sci) else "pass"', '        st_sci = None')], "both"),
 "DP30_kind_closes_off": ("DP30_kind_closes_off", DRVR, [
     ('                              "closes_system": any(r_.get("closes_system") is True for r_ in sci),', '                              "closes_system": False,')], "both"),
 "DP55_rejudge_disagree_off": ("DP55_rejudge_disagree_off", RUNR, [            # 같은 실행 충돌이 공통 함수로 (DQ 전 리뷰 P1-A) — ①-4 의 멈춤을 끈다
     ('            if cf_ is not None:\n                return stop("invalid", f"{sysn}{seed} 재판정',
      '            if False:\n                return stop("invalid", f"{sysn}{seed} 재판정')], "run"),
 "R4_launch_ledger": ("R4_launch_ledger", RUNR, [
     ("                led[\"runs\"].append(ent); state[\"entry\"], state[\"t0\"] = ent, t0\n                save_ledger()",
      "                led[\"runs\"].append(ent); state[\"entry\"], state[\"t0\"] = ent, t0\n                pass"),
     ("                    save_ledger()                            # ⭐ 띄운 직후", "                    pass                                     # ⭐ 띄운 직후")], "run"),
 "DP51_persist_revert_off": ("DP51_persist_revert_off", RUNR, [
     ("                        r_.clear(); r_.update(old_)          # 교체 전 실패", "                        pass  # 교체 전 실패")], "run"),
 "DP57_ledger_keys_optional": ("DP57_ledger_keys_optional", DRVR, [
     ("            out.append(f\"장부에 {k} 가 없다\")", "            led[k] = []")], "both"),
 "DP58_ledger_elems_off": ("DP58_ledger_elems_off", DRVR, [
     ("        elif not all(isinstance(x, dict) for x in led[k]):\n            out.append(f\"장부 {k} 원소가 객체가 아니다\")",
      "        elif False:\n            out.append(f\"장부 {k} 원소가 객체가 아니다\")")], "both"),
}
F = lambda name, anchor, repl, which="drv", where=DRVR: (name, where, [(anchor, repl)], which)
NC = '__import__("contextlib").nullcontext()'
NEW = [
 # ── P0-1 · P2-1: 저장 경계의 신호
 F("DQ1_persist_section_off", "                with _critical():                            # ⭐ 회신 DP P0-1 — 메모리 변경",
   f"                with {NC}:                            # ⭐ 회신 DP P0-1 — 메모리 변경", "run", RUNR),
 F("DQ2_after_replace_revert", "                    except _AfterReplace:\n                        raise                                # 디스크에 새 행이 있다",
   "                    except ZeroDivisionError:\n                        raise                                # 디스크에 새 행이 있다", "run", RUNR),
 F("DQ3_stop_section_off", "        with _critical():                                    # ⭐ 회신 DP P2-1",
   f"        with {NC}:                                    # ⭐ 회신 DP P2-1", "run", RUNR),
 F("DQ4_stop_after_replace_flag_off", "            except _AfterReplace:\n                state[\"stopped\"], state[\"stop_code\"] = True, code   # 디스크에 이 STOP 이 있다",
   "            except ZeroDivisionError:\n                state[\"stopped\"], state[\"stop_code\"] = True, code   # 디스크에 이 STOP 이 있다", "run", RUNR),
 F("DQ5_after_replace_plain", "                raise _AfterReplace(f\"교체 뒤 디렉터리 fsync 실패 ({type(e_).__name__}: {e_})\") from e_",
   "                raise", "run", RUNR),
 F("DQ6_attempt_section_off", "            with _critical():                                # ⭐ 회신 DP — 폴더 · 실행 전 기록 · 장부 행을",
   f"            with {NC}:                                # ⭐ 회신 DP — 폴더 · 실행 전 기록 · 장부 행을", "run", RUNR),
 # ── P1-1: written False · 현재 폴더 미해결 기록
 F("DQ7_rejudge_written_off", "                if now_.get(\"written\") is False:             # ⭐ 회신 DP P1-1", "                if False:", "run", RUNR),
 F("DQ8_end_written_off", "            if v.get(\"written\") is False:                    # ⭐ 회신 DP P1-1", "            if False:", "run", RUNR),
 F("DQ9_summary_unresolved_off", "            if rprob_:\n                ver[(s, sd)] = {\"status\": \"invalid\"", "            if False:\n                ver[(s, sd)] = {\"status\": \"invalid\"", "both"),
 F("DQ10_summary_none_status_off",
   "            if rprob_ is None and any(isinstance(r_, dict) and r_.get(\"status\") is None for _, r_, part_ in recs_ if not part_):",
   "            if False:", "both"),
 # ── P1-2: 요약의 장부 검사
 F("DQ11_record_tmp_off", "    invalid.extend(record_tmp_problems(out_root))", "    pass", "both"),
 F("DQ12_flip_conflict_off", "        if v_ in (\"pass\", \"fail\") and v_ != folder_status:", "        if False:", "both"),
 F("DQ13_same_run_melt_off", "        if folder_status == \"pass\" and isinstance(mc_, dict) and mc_.get(\"verdict\") == \"fail\":", "        if False:", "both"),
 # ── P2-2: 직접 진입 엄격 판독 (DP 판에서 '같은 결과' 로 뺐던 넷)
 F("DQ14_card_strict_off", "    d = loads_strict(pathlib.Path(card).read_text(encoding=\"utf-8\"))   # ⭐ 회신 DO P1 — 카드도",
   "    d = json.loads(pathlib.Path(card).read_text(encoding=\"utf-8\"))   # ⭐ 회신 DO P1 — 카드도"),
 F("DQ15_band_strict_off", "    d = loads_strict(q.read_text(encoding=\"utf-8\"))          # ⭐ 회신 DO P1 — G4 밴드 카드도",
   "    d = json.loads(q.read_text(encoding=\"utf-8\"))          # ⭐ 회신 DO P1 — G4 밴드 카드도"),
 F("DQ16_gate_plan_strict_off", "    plan = loads_strict((run / \"plan.json\").read_text(encoding=\"utf-8\"))   # ⭐ 회신 DO P1 (예외 → 판정이",
   "    plan = json.loads((run / \"plan.json\").read_text(encoding=\"utf-8\"))   # ⭐ 회신 DO P1 (예외 → 판정이"),
 F("DQ18_consumer_ledger_shape_off", "        if shp_:\n            raise ValueError(\" · \".join(shp_))\n        runs, stop_hist = led[\"runs\"], led[\"stop_history\"]",
   "        if False:\n            raise ValueError(\" · \".join(shp_))\n        runs, stop_hist = led[\"runs\"], led[\"stop_history\"]", "both"),
 F("DQ19_runner_ledger_shape_off", "                if shp_:\n                    raise ValueError(\"장부 꼴이 아니다 — \" + \" · \".join(shp_))",
   "                if False:\n                    raise ValueError(\"장부 꼴이 아니다 — \" + \" · \".join(shp_))", "run", RUNR),
 # ── DQ 전 독립 리뷰 (2026-11-05) 고침 자리
 F("DQ20_conflict_unknown_off", "    if v_ not in LEDGER_VERDICTS:\n        return f\"장부 판정", "    if False:\n        return f\"장부 판정", "both"),
 F("DQ21_conflict_recorded_off", "    if recorded and row.get(\"verdict_observed_conflict\"):", "    if False:", "both"),
 F("DQ22_rows_verdict_values_off", "        if r.get(\"verdict\") not in LEDGER_VERDICTS:          # ⭐ DQ 전 리뷰 P1-A", "        if False:", "both"),
 F("DQ23_rows_conflict_record_off", "        if vc_:\n            invalid.append(", "        if False:\n            invalid.append(", "both"),
 F("DQ24_rows_conflict_shape_off", "        if vc_ is not None and not (isinstance(vc_, list) and all(isinstance(x_, dict) for x_ in vc_)):", "        if False:", "both"),
 F("DQ25_closes_nonfirst_ledger_off", "        if cs is True and r[\"seed\"] != values.get(\"first_seed\"):   # ⭐ DQ 전 리뷰 P2-D", "        if False:", "both"),
 F("DQ26_closes_nonfirst_verdict_off", "            if vv is not None and vv.get(\"closes_system\") is True and sd != values.get(\"first_seed\"):   # ⭐ DQ 전 리뷰 P2-D",
   "            if False:", "both"),
 F("DQ27_terminal_stop_off", "    if ts_ and out[\"track\"] != \"stop_track\":", "    if False:", "both"),
 F("DQ28_stop_unreadable_off", "    if st_k == \"unreadable\":", "    if False:", "both"),
 F("DQ30_stop_open_off", "    elif st_k == \"open\":", "    elif False:", "both"),
 F("DQ31_stop_terminal_flag_off", "    if d_[\"code\"] in STOP_TERMINAL_CODES or d_.get(\"terminal\") is True:", "    if d_[\"code\"] in STOP_TERMINAL_CODES:", "both"),
 F("DQ32_stop_shape_off", "    if not (isinstance(d_, dict) and isinstance(d_.get(\"stop_id\"), str) and d_[\"stop_id\"].strip()",
   "    if False and (isinstance(d_, dict) and isinstance(d_.get(\"stop_id\"), str) and d_[\"stop_id\"].strip()", "both"),
 F("DQ33_ledger_card_fp_off", "    if led.get(\"card_values_sha16\") != values_sha16(values):", "    if False:", "both"),
 F("DQ34_ledger_driver_fp_off", "    if led.get(\"driver_sha16\") != driver_sha16():", "    if False:", "both"),
 F("DQ35_hist_prev_shape_off", "            if not isinstance(pv_, dict):                    # ⭐ DQ 전 리뷰 P2-C", "            if False:", "both"),
 F("DQ36_hist_prev_status_off", "            if pv_.get(\"status\") is not None and pv_.get(\"status\") not in LI2S2_STATUSES:", "            if False:", "both"),
 F("DQ37_hist_new_status_off", "            if h.get(\"new_status\") not in LI2S2_STATUSES:", "            if False:", "both"),
 F("DQ38_mark_summary_noop", "    q = pathlib.Path(out_root) / \"stage1_summary.json\"\n    if not os.path.lexists(q):",
   "    q = pathlib.Path(out_root) / \"stage1_summary.json\"\n    if True:", "both"),
 F("DQ39_persist_conflict_off", "                if cf_ is not None:                          # 장부를 덮지 않고 충돌 관측으로 남긴다", "                if False:", "run", RUNR),
 F("DQ41_stop_pending_init_off", "    state[\"stop_pending\"] = os.path.lexists(stop_p)          # ⭐ DQ 전 리뷰 P2-A",
   "    state[\"stop_pending\"] = False          # ⭐ DQ 전 리뷰 P2-A", "run", RUNR),
 F("DQ42_stop_code_return_off", "        elif state.get(\"stop_code\") in RC:", "        elif False:", "run", RUNR),
 F("DQ43_rejudge_verdict_not_critical", "                with _critical():                            # ⭐ DQ 전 리뷰 P2-E — 판정 파일 쓰기 (임시 → 교체)",
   "                with __import__(\"contextlib\").nullcontext():                            # ⭐ DQ 전 리뷰 P2-E — 판정 파일 쓰기 (임시 → 교체)", "run", RUNR),
 F("DQ44_cap_verdict_not_critical", "                        with _critical():                    # ⭐ DQ 전 리뷰 P2-E — 판정 파일 쓰기를",
   "                        with __import__(\"contextlib\").nullcontext():                    # ⭐ DQ 전 리뷰 P2-E — 판정 파일 쓰기를", "run", RUNR),
 F("DQ45_melt_verdict_not_critical", "                        with _critical():                    # ⭐ DQ 전 리뷰 P2-E · 3차 P1 — 판정 쓰기 · 장부 적기",
   "                        with __import__(\"contextlib\").nullcontext():                    # ⭐ DQ 전 리뷰 P2-E · 3차 P1 — 판정 쓰기 · 장부 적기", "run", RUNR),
 F("DQ46_end_verdict_not_critical", "            with _critical():                                # ⭐ DQ 전 리뷰 P2-E · 3차 P1 — 끝 판정 쓰기",
   "            with __import__(\"contextlib\").nullcontext():                                # ⭐ DQ 전 리뷰 P2-E · 3차 P1 — 끝 판정 쓰기", "run", RUNR),
 F("DQ47_closes_bad_runner_off", "        if cl_bad:                                           # ⭐ DQ 전 리뷰 P2-D", "        if False:", "run", RUNR),
 F("DQ48_mark_summary_call_off", "        mq.mark_summary_not_current(R, \"러너가 이 run_root 로 시작했다 (시작 점검 · 재판정 뒤에 새로 낸다)\")",
   "        pass", "run", RUNR),
 F("DQ49_persist_log_conflict_off", "        if conflict_:                                        # ⭐ DQ 전 리뷰 P2-B", "        if False:", "run", RUNR),
 # ── DQ 전 2차 독립 리뷰 (2026-11-05) 고침 자리
 F("DQ50_same_inputs_always", "    if not (isinstance(a, dict) and isinstance(b, dict)):\n        return False\n    for k in (\"files_sha256\"",
   "    if True:\n        return True\n    for k in (\"files_sha256\"", "both"),
 F("DQ51_same_inputs_missing_ok", "        if a.get(k) is None or b.get(k) is None or a.get(k) != b.get(k):", "        if a.get(k) != b.get(k):", "both"),
 F("DQ52_nonsci_conflict_off", "        if v_ in (\"invalid\", \"incomplete\") and not same_judge_inputs(row.get(\"verdict_provenance\"), folder_provenance):",
   "        if False:", "both"),
 F("DQ53_consumer_prov_off", "            cf_ = ledger_verdict_conflict(r, vv.get(\"status\"), recorded=False, folder_provenance=vv.get(\"provenance\"),",
   "            cf_ = ledger_verdict_conflict(r, vv.get(\"status\"), recorded=False, folder_provenance=r.get(\"verdict_provenance\"),", "both"),
 F("DQ54_runkind_prov_off", "                              \"provenance\": pv_cur, \"prior\": folder_verdict_chain(folder)}",
   "                              \"provenance\": None, \"prior\": folder_verdict_chain(folder)}", "both"),
 F("DQ55_rows_prov_shape_off", "        if vp_ is not None and not isinstance(vp_, dict):", "        if False:", "both"),
 F("DQ56_rows_superseded_shape_off", "        if vs_ is not None and not (isinstance(vs_, list) and all(isinstance(x_, dict) and x_.get(\"from\") in (\"invalid\", \"incomplete\")",
   "        if False and (isinstance(vs_, list) and all(isinstance(x_, dict) and x_.get(\"from\") in (\"invalid\", \"incomplete\")", "both"),
 F("DQ57_mark_nonpass_kept_off", "        if isinstance(old_, dict) and old_.get(\"track\") != \"stage1_pass\":\n            return False",
   "        if False:\n            return False", "both"),
 F("DQ58_conflict_closes", "                    closes_, basis_ = False, None            # ⭐ 2차 N1",
   "                    closes_, basis_ = first_ and obs.get(\"closes_system\") is True, \"x\"            # ⭐ 2차 N1", "run", RUNR),
 F("DQ59_conflict_dedupe_off", "                    if not any({k_: x_.get(k_) for k_ in ent_} == ent_ for x_ in (vc0 or [])):", "                    if True:", "run", RUNR),
 F("DQ60_supersede_off", "                    if v0 is None or v0 in (\"invalid\", \"incomplete\"):   # ⭐ 2차 N3", "                    if v0 is None:   # ⭐ 2차 N3", "run", RUNR),
 F("DQ61_supersede_record_off", "                        if v0 is not None:\n                            new_[\"verdict_superseded\"]",
   "                        if False:\n                            new_[\"verdict_superseded\"]", "run", RUNR),
 F("DQ62_end_prov_record_off", "                    ent[\"verdict_provenance\"] = v.get(\"provenance\")  # ⭐ DQ 전 2차 리뷰 N3", "                    pass  # ⭐ DQ 전 2차 리뷰 N3", "run", RUNR),
 F("DQ63_rejudge_obs_prov_off", "\"status\": now_[\"status\"], \"provenance\": now_.get(\"provenance\"),", "\"status\": now_[\"status\"],", "run", RUNR),
 F("DQ64_retry_obs_prov_off", "\"provenance\": rk_d.get(\"provenance\"), \"prior\": rk_d.get(\"prior\")},", "\"provenance\": None, \"prior\": rk_d.get(\"prior\")},", "run", RUNR),
 F("DQ65_ack_obs_prov_off", "\"provenance\": kd.get(\"provenance\"), \"prior\": kd.get(\"prior\")})", "\"provenance\": None, \"prior\": kd.get(\"prior\")})", "run", RUNR),
 # ── DQ 전 3차 독립 리뷰 (2026-11-05) 고침 자리
 ("DQ67_end_ledger_outside_section", RUNR, [                 # 3차 P1 이전 꼴 — 장부 적기 · 저장을 판정 구간 밖으로 (미룬 신호가 그 사이에서 장부를 비운다)
     ('                if v.get("written") is not False:\n                    ent["verdict"], ent["closes_system"] = v.get("status"), bool(v.get("closes_system"))',
      '                pass\n            if v.get("written") is not False:\n                    ent["verdict"], ent["closes_system"] = v.get("status"), bool(v.get("closes_system"))')], "run"),
 ("DQ68_melt_ledger_outside_section", RUNR, [
     ('                            v = mq.stage1_verdict(rd, values=vals, log=log, reason=f"첫 시드 녹음 판정 {mw[\'verdict\']} — 러너가 멈춤")\n'
      '                            ent["verdict"], ent["verdict_provenance"] = v.get("status"), v.get("provenance")',
      '                            v = mq.stage1_verdict(rd, values=vals, log=log, reason=f"첫 시드 녹음 판정 {mw[\'verdict\']} — 러너가 멈춤")\n'
      '                        if True:\n                            ent["verdict"], ent["verdict_provenance"] = v.get("status"), v.get("provenance")')], "run"),
 F("DQ69_folder_prior_off", "        if v_ is None and isinstance(folder_prior, list):", "        if False:", "both"),
 F("DQ70_prior_nonsci_changed_off", "                if st_ in (\"invalid\", \"incomplete\") and not same_judge_inputs(rec_.get(\"provenance\"), folder_provenance):",
   "                if False:", "both"),
 F("DQ71_prior_unreadable_ok", "                if st_ is None or (st_ not in LI2S2_STATUSES):", "                if False:", "both"),
 F("DQ80_prior_sci_diff_off", "                if st_ in (\"pass\", \"fail\") and st_ != folder_status:", "                if False:", "both"),
 F("DQ81_chain_prob_off", "    if prob:\n        return [{\"status\": None, \"why\": prob}]", "    if False:\n        return [{\"status\": None, \"why\": prob}]", "both"),
 F("DQ72_summary_prior_off", "                                          folder_prior=(folder_verdict_chain(pathlib.Path(out_root) / s / f\"seed{sd}\") if r.get(\"verdict\") is None else None))",
   "                                          folder_prior=None)", "both"),
 F("DQ73_rejudge_obs_prior_off", "                                       \"prior\": mq.folder_verdict_chain(R / sysn / f\"seed{seed}\"),", "                                       \"prior\": None,", "run", RUNR),
 F("DQ74_rejudge_check_prior_off", "                                              folder_prior=mq.folder_verdict_chain(R / sysn / f\"seed{seed}\"))",
   "                                              folder_prior=None)", "run", RUNR),
 F("DQ75_persist_prior_off", "folder_provenance=obs.get(\"provenance\"), folder_prior=obs.get(\"prior\"))", "folder_provenance=obs.get(\"provenance\"), folder_prior=None)", "run", RUNR),
 F("DQ76_retry_obs_prior_off", "\"provenance\": rk_d.get(\"provenance\"), \"prior\": rk_d.get(\"prior\")},", "\"provenance\": rk_d.get(\"provenance\"), \"prior\": None},", "run", RUNR),
 F("DQ77_ack_obs_prior_off", "\"provenance\": kd.get(\"provenance\"), \"prior\": kd.get(\"prior\")})", "\"provenance\": kd.get(\"provenance\"), \"prior\": None})", "run", RUNR),
 F("DQ78_runkind_prov_current_check_off", "        if not (isinstance(pv_cur, dict) and values is not None and pv_cur.get(\"files_sha256\") == run_provenance(folder)",
   "        if False and (isinstance(pv_cur, dict) and values is not None and pv_cur.get(\"files_sha256\") == run_provenance(folder)", "both"),
 F("DQ79_runkind_prior_off", "                              \"provenance\": pv_cur, \"prior\": folder_verdict_chain(folder)}",
   "                              \"provenance\": pv_cur, \"prior\": None}", "both"),
 # ── DQ 전 5차 독립 리뷰 (2026-11-05) 고침 자리 — 첫 판정도 이력에
 F("DQ82_first_line_off", "    else:\n        _append_history_first(run, res, reason)", "    else:\n        pass", "both"),
 F("DQ83_first_read_off", "            if h.get(\"first\") is True:                       # ⭐ DQ 전 5차 리뷰 P2", "            if False:", "both"),
 F("DQ84_first_shape_off", "                if \"prev\" in h or h.get(\"new_status\") not in LI2S2_STATUSES:", "                if False:", "both"),
 F("DQ17_seed_gate_plan_strict_off", "    plan = loads_strict((run / \"plan.json\").read_text(encoding=\"utf-8\")) if (run / \"plan.json\").exists() else {}",
   "    plan = json.loads((run / \"plan.json\").read_text(encoding=\"utf-8\")) if (run / \"plan.json\").exists() else {}"),
]

_dp_names = {m[0] for m in dp.MUT}
assert set(MOVED) <= _dp_names, f"옮길 변이가 DP 판에 없다: {sorted(set(MOVED) - _dp_names)}"   # 옮긴 열하나 (DP 고침 4 · DQ 전 리뷰 고침 5 · 2차 2)   # 이름이 틀리면 옮김이 조용히 빠진다
MUT = [MOVED.get(m[0], m) for m in dp.MUT] + NEW
MUT = [(m[0], m[1], dp._keep_comment(m[2]), m[3]) for m in MUT]   # 옮긴 것까지 (이미 '#' 가 있으면 그대로)
dl.MUT = MUT
TAG = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--tag=")), "dq")
dp.TAG = TAG
FAILFAST = "--failfast" in sys.argv
dp.FAILFAST = FAILFAST
WORKERS = int(next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--workers=")), dl.N_WORKERS))

if __name__ == "__main__":
    bad = dl.check_anchors()
    if bad:
        print("\n".join(bad)); sys.exit(2)
    names = [mu[0] for mu in MUT]
    assert len(names) == len(set(names)), "변이 이름이 겹친다"
    import builtins
    nbad = []
    for name, rel, reps, which in MUT:                       # 문법이 깨지는 변이가 없는지 먼저 (DP 판 무효 20 의 교훈)
        f = REPO / rel; s = f.read_text(encoding="utf-8")
        for o_, n_ in reps:
            s = s.replace(o_, n_, 1)
        try:
            compile(s, str(f), "exec")
        except SyntaxError as e:
            nbad.append(f"{name}: {e.msg}")
    if nbad:
        print("문법 오류 변이:\n" + "\n".join(nbad)); sys.exit(2)
    print(f"변이 {len(MUT)} 개 (DP 판 {len(dp.MUT)} · 자리 옮김 {len(MOVED)} · DQ {len(NEW)}) · 자리 모두 한 번씩 · 모두 컴파일됨", flush=True)
    if "--dry" in sys.argv:
        sys.exit(0)
    only = [a.split("=", 1)[1] for a in sys.argv if a.startswith("--only=")]
    todo = [mu for mu in MUT if not only or any(mu[0].startswith(p) for p in only[0].split(","))]
    mirrors = [dp.make_mirror(i) for i in range(WORKERS)]
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
                results.append(line)
                print(line, flush=True)

    ts = [threading.Thread(target=worker, args=(m,)) for m in mirrors]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    n_red = sum("⭕ 빨강" in x for x in results)
    print(f"끝: 빨강 {n_red} / {len(todo)}")
