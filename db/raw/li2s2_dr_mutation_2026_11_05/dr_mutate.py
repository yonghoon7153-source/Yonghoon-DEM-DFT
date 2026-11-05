"""회신 DQ 고침 변이 검사 — DQ 판 (../li2s2_dq_mutation_2026_11_05/dq_mutate.py) 의 368 개를 가져오되 DQ 고침으로 자리가 바뀐 것은 새 자리로
옮기고 (MOVED_DR · 뜻 그대로), DQ 고침 자리 (DR1–) 를 더한다. 실행 · 판정은 DQ 판과 같다 (저장소 밖 복사본 · 작업자 · which = run / drv / both ·
주석 중간 자리는 '  #' — DP 판 _keep_comment). 옵션: --dry · --only=접두 (쉼표로 여럿) · --tag=이름 · --failfast · --workers=N.

뺀 것 (DQ 판의 '같은 결과' 설명을 회신 DQ Q9 대로 좁힌다 — 상태가 같다는 뜻이 아니라 **같은 차단 결과** 라는 뜻이다):
  · 확인 구간 (확인 기록 저장 · STOP 지우기 · 확인 끝 표시) 끄기 — 지운 직후 신호면 STOP 은 없고 확인 기록만 남을 수 있다 (상태는 다르다).
    그래도 다음 시작은 추가 실행 0 이다 (Codex 재현) — 그 차단 결과가 같아서 시험이 못 가르는 것이 맞다.
  · persist_observed 의 즉시 저장 끄기 — **정상적인 끝 저장이 성공하는 범위에서만** 같다 (같은 프로세스 안에서 끝 처리가 같은 장부를 저장할 때).
    끝 저장이 실패하거나 kill -9 · 정전이면 다르다 — 그 경우는 이 시험 틀 (한 프로세스) 로 재현하지 않는다 (즉시 저장은 그 경우를 위한 운영 근거).
  (나머지 DQ 판 제외 — 시드 루프의 판정 상태 엄격 판독 · 확인 경로 '적기 실패 → 거부' return · 살아 있는 녹음 멈춤 판정의 지문 기록 · ①-4 확인의
   폴더 지문 · DQ66 · 판정 구간 안의 장부 저장 — 의 설명과 조건은 DQ 판 머리글 그대로다.)
DR 자리에서 뺀 것: 없음 (아래 DR 은 모두 시험이 가르는 것으로 넣었다 — 살아남으면 시험을 보강하거나 같은 결과면 이유를 적고 뺀다)."""
import importlib.util, pathlib, sys

REPO = pathlib.Path("/home/user/Yonghoon-DEM-DFT")
_spec = importlib.util.spec_from_file_location("dq_mutate", REPO / "db/raw/li2s2_dq_mutation_2026_11_05/dq_mutate.py")
dq = importlib.util.module_from_spec(_spec)
_argv = sys.argv; sys.argv = [sys.argv[0]]
_spec.loader.exec_module(dq)
sys.argv = _argv
dp, dl = dq.dp, dq.dl
RUNR, DRVR = dl.RUNR, dl.DRVR
F = lambda name, anchor, repl, which="both", where=DRVR: (name, where, [(anchor, repl)], which)
F2 = lambda name, pairs, which="both", where=DRVR: (name, where, pairs, which)

#: DQ 판 변이 중 DQ 고침으로 자리가 바뀐 것 (뜻 그대로 · 새 자리) — --dry 의 '자리 없음' 목록에서 채웠다 (2026-11-05)
MOVED_DR = {
 # 요약의 지문 대조가 공통 함수 provenance_current_problems 로 (요약 · _run_kind 가 같이 쓴다)
 "D11_provenance": F("D11_provenance", "    if pv.get(\"files_sha256\") != run_provenance(folder):", "    if False:"),
 "D21_card_vals_sha": F("D21_card_vals_sha", "    if pv.get(\"card_values_sha16\") != cur_vals:", "    if False:"),
 "DQ78_runkind_prov_current_check_off": F("DQ78_runkind_prov_current_check_off", "        if not (isinstance(pv_cur, dict) and values is not None",
                                          "        if False and (isinstance(pv_cur, dict) and values is not None"),
 # 러너의 STOP 확인이 소비자와 같은 함수 (stop_record → stop_shape_problem) 로
 "DO39_stop_id_not_required": F("DO39_stop_id_not_required",
                                "    if not (isinstance(d_.get(\"stop_id\"), str) and d_[\"stop_id\"].strip() and isinstance(d_.get(\"code\"), str)",
                                "    if not (isinstance(d_.get(\"code\"), str)"),
 "DO40_stop_unreadable_overwritten": F2("DO40_stop_unreadable_overwritten", [
     ("                log(f\"⛔ STOP.json 을 받을 수 없다 ({str(sp)[:160]}) — 원본을 덮어쓰거나 확인으로 지우지 않고 시작하지 않는다 (사람이 본다)\")\n"
      "                return RC[\"refused\"]", "                raise RuntimeError(str(sp))")], "run", RUNR),
 "DQ32_stop_shape_off": F("DQ32_stop_shape_off", "    if not (isinstance(d_.get(\"stop_id\"), str) and d_[\"stop_id\"].strip()",
                          "    if False and (isinstance(d_.get(\"stop_id\"), str) and d_[\"stop_id\"].strip()"),
 # 같은 실행 충돌 규칙이 same_judge_inputs → supersede_block 으로
 "DQ50_same_inputs_always": F("DQ50_same_inputs_always",
                              "    if not (isinstance(a, dict) and isinstance(b, dict)):\n        return False\n    fa, fb = a.get(\"files_sha256\"), b.get(\"files_sha256\")",
                              "    if True:\n        return True\n    fa, fb = a.get(\"files_sha256\"), b.get(\"files_sha256\")"),
 "DQ52_nonsci_conflict_off": F("DQ52_nonsci_conflict_off", "        if v_ in (\"invalid\", \"incomplete\"):\n            sb_ = supersede_block(row.get(",
                               "        if False:\n            sb_ = supersede_block(row.get("),
 # DR 전 2차 리뷰 P1 — 폴더 기록 규칙이 장부 판정 None · invalid · incomplete 로 넓어짐 (그 줄 · 요약의 인자 줄이 바뀜)
 "DQ69_folder_prior_off": F("DQ69_folder_prior_off",
                            "        if (v_ is None or v_ in (\"invalid\", \"incomplete\")) and isinstance(folder_prior, list):", "        if False:"),
 "DQ72_summary_prior_off": F2("DQ72_summary_prior_off", [
     ("                                          folder_prior=(folder_verdict_chain(pathlib.Path(out_root) / s / f\"seed{sd}\")\n"
      "                                                        if r.get(\"verdict\") in (None, \"invalid\", \"incomplete\") else None))",
      "                                          folder_prior=None)")]),
 "DQ70_prior_nonsci_changed_off": F("DQ70_prior_nonsci_changed_off",            # DR 전 3 · 4차: 대체 규칙을 받는 기록 줄로
                                    "                if st_ in (\"invalid\", \"incomplete\") and (k_ is None or i_ > k_):",
                                    "                if False:"),
 # DR 전 3차 리뷰 P2 — 이력의 새 판정 줄에 closes_system 이 붙음 (DN 판 변이 — 그 줄의 지문을 객체로만 받기)
 "DN6_history_provenance_coerced": F("DN6_history_provenance_coerced",
     "                                                   \"provenance\": h.get(\"new_provenance\"), \"closes_system\": h.get(\"new_closes_system\")}, True))",
     "                                                   \"provenance\": h.get(\"new_provenance\") if isinstance(h.get(\"new_provenance\"), dict) else None, "
     "\"closes_system\": h.get(\"new_closes_system\")}, True))", "drv"),
}
#: DQ 판 변이 중 DQ 고침으로 뜻이 없어진 것 — 이유를 적고 뺀다
DROPPED_DR = {
 "DQ31_stop_terminal_flag_off": "그 자리 (terminal 표시만으로 닫힘 · 코드와 모순이어도) 가 DQ P2-1 고침으로 없어졌다 — 모순된 기록은 이제 판독 불가다. "
                                "terminal 표시와 코드의 관계는 DR37 (일치 검사 끄기) · DR38 (참거짓 검사 끄기) 이 깬다.",
}

NEW = [
 # ── P1-1: 판정이 읽은 입력 전부 같음 (same_judge_inputs)
 F("DR1_same_inputs_keyset_off",
   "    if not (isinstance(fa, dict) and isinstance(fb, dict) and set(fa) == set(fb) and set(JUDGE_FILES) <= set(fa)):",
   "    if not (isinstance(fa, dict) and isinstance(fb, dict)):"),
 F("DR2_same_inputs_keys_off", "    for k in JUDGE_INPUT_KEYS:", "    for k in ():"),
 F("DR3_derived_any_change", "        if f in JUDGE_DERIVED_FILES and fa[f] is None and fb[f] is not None:",
   "        if f in JUDGE_DERIVED_FILES and fb[f] is not None:"),
 # DR4 (DR 전 리뷰 1 차 P2-A 로 바뀜) — '이 판정이 만들었을 때만' 조건은 없앴다 (중간 판정 · 사람의 --seed_gate 뒤 회복이 영구 보류로 굳었다) ·
 #      대신 '없던 파생 파일이 생긴 것' 예외 자체를 끈다
 F("DR4_derived_exception_off", "        if f in JUDGE_DERIVED_FILES and fa[f] is None and fb[f] is not None:\n            continue",
   "        if False:\n            continue"),
 # ── P1-1 · Q5: 앞 판정의 성격 (supersede_block)
 F("DR5_mismatch_check_off", "    if jn[\"input_mismatch\"]:", "    if False:"),
 F("DR6_errors_check_off", "    if not jn[\"errors\"]:", "    if False:"),
 F("DR7_nature_missing_ok", "        return \"앞 판정에 판정 성격 기록 (judge_nature) 이 없다 — 판정 도중 오류였는지 모른다\"", "        return None"),
 F("DR8_row_rule_same_inputs", "            sb_ = supersede_block(row.get(\"verdict_provenance\"), folder_provenance)",
   "            sb_ = None if same_judge_inputs(row.get(\"verdict_provenance\"), folder_provenance) else \"x\""),
 F("DR9_chain_rule_same_inputs", "                    sb_ = supersede_block(rec_.get(\"provenance\"), folder_provenance)",
   "                    sb_ = None if same_judge_inputs(rec_.get(\"provenance\"), folder_provenance) else \"x\""),
 # ── P1-1: 판정이 성격 · 처음 만듦을 적는다 (stage1_verdict)
 F("DR10_mismatch_as_error", "                input_mismatch.append(f\"{SEED_GATE_RAW} 가 이미 있고", "                judge_err.append(f\"{SEED_GATE_RAW} 가 이미 있고"),
 F("DR11_derived_written_off", "            if not raw_before and (run / SEED_GATE_RAW).is_file():", "            if False:"),
 F("DR12_derived_from_status", "            if not raw_before and (run / SEED_GATE_RAW).is_file():",
   "            if isinstance(seedg, dict) and (seedg.get(\"md_init_raw\") or {}).get(\"status\") == \"썼다\":"),
 F("DR13_bind_raw_off", "JUDGE_FILES = PROVENANCE_FILES + JUDGE_DERIVED_FILES", "JUDGE_FILES = PROVENANCE_FILES"),
 F("DR14_bind_attempt_off", "    names = JUDGE_FILES + ((ATTEMPT_NAME,) if _judge_reads_attempt(run) else ())", "    names = JUDGE_FILES"),
 F("DR15_current_band_off", "    if cur_band is None or pv.get(\"band_sha16\") != cur_band:", "    if False:"),
 F("DR16_band_sha_const", "        return _sha256_file(_band_card_path(card))[:16]", "        return \"0\" * 16"),
 F("DR17_runtime_python_off", "    out = {\"python\": sys.version.split()[0], \"numpy\": getattr(np, \"__version__\", None)}", "    out = {}"),
 F("DR18_band_in_provenance_off", "                         \"band_sha16\": band_card_sha16() if band_read else BAND_NOT_READ,",
   "                         \"band_sha16\": None,"),
 # ── DR 전 리뷰 1 차 (P3-B 밴드는 읽었을 때만 · P3-A 폴더 이름 · P2-B 보존 폴더 · DQ50 꼴 검사)
 F("DR42_band_always_read", "                         \"band_sha16\": band_card_sha16() if band_read else BAND_NOT_READ,",
   "                         \"band_sha16\": band_card_sha16(),"),
 F("DR43_band_never_read", "            if isinstance(gate, dict) and \"band_center\" in gate:", "            if False:"),
 F("DR44_band_notread_compared", "    if pv.get(\"band_sha16\") != BAND_NOT_READ:", "    if True:"),
 F("DR45_folder_key_off", "JUDGE_INPUT_KEYS = (\"driver_sha16\", \"band_sha16\", \"runtime\", \"folder\")",
   "JUDGE_INPUT_KEYS = (\"driver_sha16\", \"band_sha16\", \"runtime\")"),
 F("DR46_folder_current_off", "    if pv.get(\"folder\") != [fo_.parent.name, fo_.name]:", "    if False:"),
 F("DR47_folder_record_off", "                         \"folder\": [run.parent.name, run.name], \"derived_written\"",
   "                         \"folder\": None, \"derived_written\""),
 F("DR48_preserved_runner_off", "                                                   for s_, d_, nm_, why_ in mq.preserved_unresolved(R, vals[\"seeds\"])]",
   "                                                   for s_, d_, nm_, why_ in []]", "run", RUNR),
 F("DR49_preserved_summary_off", "                   for s_, _, nm_, why_ in preserved_unresolved(out_root, values.get(\"seeds\")))",
   "                   for s_, _, nm_, why_ in [])"),
 # DR50 (2차로 바뀜) — 보존 폴더 판독 기준이 folder_record_problem 으로 (판정 기록 문제 · 모르는 상태까지)
 F("DR50_preserved_records_off", "    recs_, prob_ = _verdict_records(folder)\n    if prob_:\n        return prob_",
   "    recs_, prob_ = _verdict_records(folder)\n    if False:\n        return prob_"),
 # ── DR 전 리뷰 2 차 (P1 장부 판정이 비과학적이어도 폴더 기록 전체 · P2-B 이름 꼴과 무관 · P3 멈추기 전에 장부에)
 F("DR51_chain_nonsci_ledger_off", "        if (v_ is None or v_ in (\"invalid\", \"incomplete\")) and isinstance(folder_prior, list):",
   "        if v_ is None and isinstance(folder_prior, list):"),
 F("DR52_summary_chain_nonsci_off", "                                                        if r.get(\"verdict\") in (None, \"invalid\", \"incomplete\") else None))",
   "                                                        if r.get(\"verdict\") is None else None))"),
 F("DR53_preserved_name_pattern", "            if (p_.name in cur_) if cur_ is not None else re.fullmatch(r\"seed\\d+\", p_.name):",
   "            if not re.fullmatch(r\"seed\\d+\\..+\", p_.name):"),
 F("DR54_record_status_check_off", "    if any(x_ is None or x_ not in LI2S2_STATUSES for x_ in sts_):", "    if False:"),
 F("DR55_preserved_seeds_off", "    out, cur_ = [], ({f\"seed{x_}\" for x_ in seeds} if seeds is not None else None)",
   "    out, cur_ = [], set()"),
 # ── DR 전 리뷰 3 차 (P2 이력 줄의 닫힘 · P3 비과학적 장부 판정의 폴더 기록은 입력 불일치만 · P3 시드는 장부 행에서)
 F("DR57_hist_first_closes_off", "           \"new_closes_system\": res.get(\"closes_system\") is True}   # ⭐ DR 전 3차 리뷰 P2 — 첫 시드 닫힘도",
   "           \"new_closes_system\": False}   # ⭐ DR 전 3차 리뷰 P2 — 첫 시드 닫힘도", "drv"),
 F("DR58_hist_line_closes_off", "           \"new_closes_system\": res.get(\"closes_system\") is True}   # ⭐ DR 전 3차 리뷰 P2\n",
   "           \"new_closes_system\": False}   # ⭐ DR 전 3차 리뷰 P2\n"),
 F("DR59_first_line_closes_unread", "                                                         \"closes_system\": h.get(\"new_closes_system\")}, True))",
   "                                                         \"closes_system\": None}, True))"),
 F("DR60_closes_type_check_off", "            if \"new_closes_system\" in h and type(h.get(\"new_closes_system\")) is not bool:", "            if False:"),
 # DR61–DR63 (DR 전 4차로 바뀜) — 비과학적 장부 판정의 폴더 기록 규칙이 '입력 불일치만' 에서 '장부 판정 자신의 기록 뒤는 엄격' 으로
 F("DR61_anchor_off", "            k_ = (min((i_ for i_, r_ in enumerate(folder_prior) if isinstance(r_, dict) and r_.get(\"status\") == v_ and r_.get(\"provenance\") == vp_),",
   "            k_ = None and (min((i_ for i_, r_ in enumerate(folder_prior) if isinstance(r_, dict) and r_.get(\"status\") == v_ and r_.get(\"provenance\") == vp_),"),
 F("DR62_after_anchor_ignored", "                if st_ in (\"invalid\", \"incomplete\") and (k_ is None or i_ > k_):",
   "                if st_ in (\"invalid\", \"incomplete\") and k_ is None:"),
 F("DR63_anchor_last_not_first", "            k_ = (min((i_ for i_, r_ in enumerate(folder_prior) if isinstance(r_, dict) and r_.get(\"status\") == v_ and r_.get(\"provenance\") == vp_),",
   "            k_ = (max((i_ for i_, r_ in enumerate(folder_prior) if isinstance(r_, dict) and r_.get(\"status\") == v_ and r_.get(\"provenance\") == vp_),"),
 F("DR64_stop_seed_from_name", "            if len(row0_) == 1:                              # ⭐ DR 전 3차 리뷰 P3", "            if False:                              # ⭐ DR 전 3차 리뷰 P3",
   "run", RUNR),
 # ── DR 전 리뷰 4 차 (쓴 순서의 판정 기록 · 다른 카드 판정 기록 · 즉시 melt)
 F("DR65_chain_dup_prev", "            if not writes or writes[-1] != x_:               # 앞 줄의 새 판정과 같으면 겹침",
   "            if True:               # 앞 줄의 새 판정과 같으면 겹침"),
 F("DR66_chain_oob_prev_dropped", "            if not writes or writes[-1] != x_:               # 앞 줄의 새 판정과 같으면 겹침",
   "            if not writes:               # 앞 줄의 새 판정과 같으면 겹침"),
 F("DR67_chain_current_off", "    if cur is not None and (not writes or writes[-1] != cur):", "    if False:"),
 F("DR68_alien_card_off", "    if sci and values is not None:                           # ⭐ DR 전 4 · 5차 리뷰 P2", "    if False:                           # ⭐ DR 전 4 · 5차 리뷰 P2"),
 # ── DR 전 리뷰 5 차 (판정 규칙 지문 · 지금 규칙 기록 우선 · 첫 기준)
 F("DR70_judge_values_full_card", "            return pv_r.get(\"judge_values_sha16\") == jv_ if \"judge_values_sha16\" in pv_r else pv_r.get(\"card_values_sha16\") == cv_",
   "            return pv_r.get(\"card_values_sha16\") == cv_"),
 F("DR71_alien_poisons", "            sci = sci_now                                    # 지금 규칙의 기록이 있으면", "            sci = sci if len(sci_now) == len(sci) else []  # 지금 규칙의 기록이 있으면"),
 F("DR72_judge_keys_include_cap", "                    \"thermo_required_columns\", \"uma_inference_mode\")",
   "                    \"thermo_required_columns\", \"uma_inference_mode\", \"stage1_cap_gpu_h\")"),
 F("DR73_judge_keys_drop_melt", "JUDGE_VALUE_KEYS = (\"composition\", \"first_seed\", \"fix_density_g_cm3\", \"gate_check\", \"melt_window\", \"schedule\",",
   "JUDGE_VALUE_KEYS = (\"composition\", \"first_seed\", \"fix_density_g_cm3\", \"gate_check\", \"schedule\","),
 F("DR69_immediate_melt_off", "            if closed_:                                      # ⭐ DR 전 4차 리뷰 P3", "            if False:                                      # ⭐ DR 전 4차 리뷰 P3",
   "run", RUNR),
 # ── DR 전 리뷰 6 차 (자동 대체도 판정 규칙 지문 · 지금 규칙의 비과학적 판정이 있으면 다른 규칙 기록 무시)
 F("DR74_supersede_full_card", "    if a.get(\"judge_values_sha16\") is not None and b.get(\"judge_values_sha16\") is not None:   # ⭐ DR 전 6차 리뷰 P2",
   "    if False:   # ⭐ DR 전 6차 리뷰 P2"),
 F("DR75_supersede_rules_ignored", "        if a[\"judge_values_sha16\"] != b[\"judge_values_sha16\"]:",
   "        if False:"),
 F("DR76_now_nonsci_ignored", "        if not sci_now and any_now:", "        if False:"),
 F("DR56_persist_before_stop_off", "                if rk_ != \"scientific\" or rkd_.get(\"source\") not in (\"folder_verdict\", \"folder_melt_window\"):",
   "                if True:", "run", RUNR),
 F2("DR19_derived_write_direct", [
     ("            with open(tmp_, \"w\", encoding=\"utf-8\") as fh_:\n                write(fh_, clean, format=\"extxyz\")",
      "            with open(out, \"w\", encoding=\"utf-8\") as fh_:\n                write(fh_, clean, format=\"extxyz\")"),
     ("            os.replace(tmp_, out)", "            pass")]),
 F("DR20_err_gate_off", "                judge_err.append(f\"gate_check {type(e).__name__}: {str(e)[:80]}\")", "                pass"),
 F("DR21_err_melt_off", "                    judge_err.append(f\"melt_window_check {k_}: {str(melt[k_])[:80]}\")", "                    pass"),
 F("DR22_err_seedgate_off", "                judge_err.append(f\"seed_gate {type(e).__name__}: {str(e)[:80]}\")", "                pass"),
 F("DR23_err_identity_off", "        judge_err += list(checks[\"identity\"].get(\"judge_errors\") or [])", "        pass"),
 F("DR24_err_lastframe_off", "                    judge_err.append(f\"traj 마지막 프레임 읽기 {type(e).__name__}: {str(e)[:80]}\")", "                    pass"),
 F("DR25_err_final_off", "            judge_err += list(checks[\"final_structure\"].get(\"judge_errors\") or [])", "            pass"),
 F("DR26_final_judge_errors_off", "        res[\"judge_errors\"] = [f\"final.xyz 읽기 {type(e).__name__}: {str(e)[:80]}\"]", "        pass"),
 F("DR27_identity_read_err_off", "                read_err = f\"{ATTEMPT_NAME} 읽기 {type(e_).__name__}: {str(e_)[:80]}\"", "                pass"),
 F("DR28_melt_io_error_off", "            out[\"io_error\"] = f\"traj 프레임 세기 {io_err}\"", "            pass"),
 # ── P1-2: 정본 없이 이력 · 임시 파일만 남은 폴더
 F("DR29_unresolved_off", "    left = [n for n in (vf.name + \".tmp\", VERDICT_HISTORY) if os.path.lexists(f / n)]", "    left = []"),
 F("DR30_unresolved_history_off", "    left = [n for n in (vf.name + \".tmp\", VERDICT_HISTORY) if os.path.lexists(f / n)]",
   "    left = [n for n in (vf.name + \".tmp\",) if os.path.lexists(f / n)]"),
 F("DR31_unresolved_tmp_off", "    left = [n for n in (vf.name + \".tmp\", VERDICT_HISTORY) if os.path.lexists(f / n)]",
   "    left = [n for n in (VERDICT_HISTORY,) if os.path.lexists(f / n)]"),
 F("DR32_unresolved_nonfile_off", "    if os.path.lexists(vf):\n        return \"정본 판정 자리", "    if False:\n        return \"정본 판정 자리"),
 F("DR33_summary_unresolved_off", "                ur_ = unresolved_first_write(rd)", "                ur_ = None"),
 F("DR34_runner_start_check_off", "        if ur_all:", "        if False:", "run", RUNR),
 F("DR35_hist_marker_off", "        if n_:\n            rec[\"history_lines_before\"] = n_", "        if False:\n            rec[\"history_lines_before\"] = n_", "drv"),
 # ── P2-1: STOP 기록 공통 검사
 F("DR36_stop_vocab_off", "    if code_ not in STOP_CODES:", "    if False:"),
 F("DR37_stop_term_consistency_off", "    if term_ != (code_ in STOP_TERMINAL_CODES):", "    if False:"),
 F("DR38_stop_term_type_off", "    if type(term_) is not bool:", "    if False:"),
 F("DR39_ack_terminal_code_ok", "        if code_ in STOP_TERMINAL_CODES:\n            return f\"닫는 코드", "        if False:\n            return f\"닫는 코드"),
 F("DR40_ledger_stop_history_off", "        elif k == \"stop_history\":", "        elif False:"),
 F("DR41_runner_ack_shared_off", "                st_sp, sp = mq.stop_record(R)", "                st_sp, sp = \"open\", mq.loads_strict(stop_p.read_text(encoding=\"utf-8\"))",
   "run", RUNR),
]

_dq_names = {m[0] for m in dq.MUT}
assert set(MOVED_DR) <= _dq_names, f"옮길 변이가 DQ 판에 없다: {sorted(set(MOVED_DR) - _dq_names)}"
assert set(DROPPED_DR) <= _dq_names and not set(DROPPED_DR) & set(MOVED_DR), "뺄 변이가 DQ 판에 없거나 옮길 목록과 겹친다"
MUT = [MOVED_DR.get(m[0], m) for m in dq.MUT if m[0] not in DROPPED_DR] + NEW
MUT = [(m[0], m[1], dp._keep_comment(m[2]), m[3]) for m in MUT]
dl.MUT = MUT
TAG = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--tag=")), "dr")
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
    print(f"변이 {len(MUT)} 개 (DQ 판 {len(dq.MUT)} − 뺌 {len(DROPPED_DR)} · 자리 옮김 {len(MOVED_DR)} · DR {len(NEW)}) · 자리 모두 한 번씩 · "
          "모두 컴파일됨", flush=True)
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
