"""회신 DS 고침 변이 검사 — DS 판 (../li2s2_ds_mutation_2026_11_06/ds_mutate.py) 의 472 개를 가져오되 DS 회신 고침으로 자리가 바뀐 것은 새 자리로
옮기고 (MOVED_DT · 뜻 그대로), DS 회신 고침 자리 (DT1–) 를 더한다. 실행 · 판정은 DS 판과 같다 (저장소 밖 복사본 · 작업자 · which = run / drv / both ·
주석 중간 자리는 '  #' — DP 판 _keep_comment · selftest 시간 제한은 ⚠ 로 남긴다). 옵션: --dry · --only=접두 (쉼표로 여럿) · --tag=이름 · --failfast · --workers=N.

뺀 것: 없음 (DR 판 머리글의 제외 설명은 그대로 — 회신 DR Q7 이 그 범위에 동의했다 · 전체 실행은 우리 쪽 실행이지 독립 재실행이 아니다).
넣지 않은 것 (같은 뜻 · 시험이 가를 수 없는 변이): md_progress 의 plan 객체 조건 끄기 (plan 을 못 읽으면 gate_check 가 안 돌아 gate 조건이 같이 막는다) ·
n 하한 (0 ≤ n) 끄기 (프레임 수는 음수가 아니다) · n ≥ 기대 갈래 (md_complete_seen 이 먼저 complete 로 보낸다)."""
import importlib.util, pathlib, subprocess, sys

REPO = pathlib.Path("/home/user/Yonghoon-DEM-DFT")
_spec = importlib.util.spec_from_file_location("ds_mutate", REPO / "db/raw/li2s2_ds_mutation_2026_11_06/ds_mutate.py")
ds = importlib.util.module_from_spec(_spec)
_argv = sys.argv; sys.argv = [sys.argv[0]]
_spec.loader.exec_module(ds)
sys.argv = _argv
dr, dq, dp, dl = ds.dr, ds.dq, ds.dp, ds.dl
RUNR, DRVR = dl.RUNR, dl.DRVR
F = lambda name, anchor, repl, which="both", where=DRVR: (name, where, [(anchor, repl)], which)

_SHORTCUT = ("    if (pv_.get(\"md_progress\") == \"in_progress\" and isinstance(fa_, dict) and all(f in fa_ and fa_[f] is None for f in LATE_FILES)")
_SHORTCUT_FULL = (_SHORTCUT + "\n            and isinstance(fb_, dict) and fa_.get(\"plan.json\") is not None and fa_.get(\"plan.json\") == fb_.get(\"plan.json\")"
                  "\n            and fa_.get(ATTEMPT_NAME) == fb_.get(ATTEMPT_NAME)"
                  "\n            and _utc_before(pv_.get(\"judged_at_utc\"), current_provenance.get(\"md_done_at_utc\"))):")
_TRACES1 = "MD_AFTER_TRACES = (MD_DONE_NAME, MD_DONE_TMP, \"final_relax.log\", \"final.xyz\", \"final.vasp\", \"result.json\", \"gr_partials.csv\","
_GUARD = "        if k_ not in (None, \"file\"):\n            msg = (f\"판정 기록 자리"

#: DS 판 변이 중 DS 회신 고침으로 자리가 바뀐 것 (뜻 그대로 · 새 자리) — --dry 의 '자리 0 개' 목록에서 채웠다 (2026-11-06)
MOVED_DT = {
 # '진행 중' 지름길이 md_done · md_complete_seen 대신 md_progress (진행 중 확인) + 뒤 산출물 없음으로 (회신 DS P1-1)
 "DS10_md_done_ignored": F("DS10_md_done_ignored", _SHORTCUT_FULL, "    if True:"),
 "DS21_md_seen_ignored": F("DS21_md_seen_ignored", _SHORTCUT,
                           "    if (isinstance(fa_, dict) and all(f in fa_ and fa_[f] is None for f in LATE_FILES)"),
 # DT 전 1차 — 첫 시드 녹음 판정 자리에 '못 씀' 확인이 붙음 (DQ68 = 장부 쓰기를 임계 구간 밖으로 · 뜻 그대로)
 "DQ68_melt_ledger_outside_section": ("DQ68_melt_ledger_outside_section", RUNR, [
     ('                            v = mq.stage1_verdict(rd, values=vals, log=log, reason=f"첫 시드 녹음 판정 {mw[\'verdict\']} — 러너가 멈춤")\n'
      '                            if v.get("written") is not False:',
      '                            v = mq.stage1_verdict(rd, values=vals, log=log, reason=f"첫 시드 녹음 판정 {mw[\'verdict\']} — 러너가 멈춤")\n'
      '                        if True:\n                            if v.get("written") is not False:')], "run"),
}

NEW = [
 # ── 회신 DS P1-1: md_progress (완료 · 진행 중 확인 · 확인 불가)
 F("DT1_progress_no_after_traces",
   "    if md_complete_seen(run, gate, checks) or any(path_kind(run / x) is not None for x in MD_AFTER_TRACES):",
   "    if md_complete_seen(run, gate, checks):"),
 F("DT2_progress_gate_unchecked",
   "    if (isinstance(plan, dict) and isinstance(gate, dict) and \"error\" not in gate and gate.get(\"schedule_complete\") is False",
   "    if (isinstance(plan, dict)"),
 F("DT3_progress_schedule_unchecked",
   "    if (isinstance(plan, dict) and isinstance(gate, dict) and \"error\" not in gate and gate.get(\"schedule_complete\") is False",
   "    if (isinstance(plan, dict) and isinstance(gate, dict) and \"error\" not in gate"),
 F("DT4_progress_frames_unchecked",
   "            and isinstance(tf_, dict) and type(tf_.get(\"n\")) is int and type(tf_.get(\"expected\")) is int\n"
   "            and 0 <= tf_[\"n\"] < tf_[\"expected\"] and not extra_):",
   "            and not extra_):"),
 F("DT5_progress_record_inprog", "                         \"md_progress\": md_progress(run, plan, gate, checks),",
   "                         \"md_progress\": \"in_progress\","),
 F("DT6_progress_record_unknown", "                         \"md_progress\": md_progress(run, plan, gate, checks),",
   "                         \"md_progress\": \"unknown\","),
 F("DT7_after_trace_result_dropped", _TRACES1, _TRACES1.replace("\"result.json\", ", "")),
 F("DT8_after_trace_tmp_dropped", _TRACES1, _TRACES1.replace("MD_DONE_TMP, ", "")),
 F("DT9_after_trace_fire_log_dropped", _TRACES1, _TRACES1.replace("\"final_relax.log\", ", "")),
 # ── 회신 DS P1-1: 기준 앞 '진행 중' 지름길
 F("DT10_shortcut_late_ignored", _SHORTCUT, "    if (pv_.get(\"md_progress\") == \"in_progress\" and isinstance(fa_, dict)"),
 F("DT11_shortcut_old_rule", _SHORTCUT_FULL,
   "    if \"md_done\" in pv_ and pv_[\"md_done\"] is None and pv_.get(\"md_complete_seen\") is False:"),
 # ── 회신 DS P1-1: 기록 꼴
 F("DT12_prerun_keys_no_progress", "                                     \"md_complete_seen\", \"md_progress\", \"judged_at_utc\", \"md_done_at_utc\"})",
   "                                     \"md_complete_seen\", \"judged_at_utc\", \"md_done_at_utc\"})"),
 F("DT27_prerun_keys_no_times", "                                     \"md_complete_seen\", \"md_progress\", \"judged_at_utc\", \"md_done_at_utc\"})",
   "                                     \"md_complete_seen\", \"md_progress\"})"),
 F("DT13_progress_vocab_off",
   "    if pv.get(\"md_progress\") is not None and pv.get(\"md_progress\") not in MD_PROGRESS_STATES:", "    if False:"),
 # ── 회신 DS P2-1: 직접 판정도 비정상 판정 · 이력 자리를 거부
 F("DT14_p2_guard_off", _GUARD, "        if False:\n            msg = (f\"판정 기록 자리"),
 F("DT15_p2_guard_verdict_only", "    for nm_ in (\"stage1_verdict.json\", VERDICT_HISTORY):", "    for nm_ in (\"stage1_verdict.json\",):"),
 F("DT16_p2_guard_history_only", "    for nm_ in (\"stage1_verdict.json\", VERDICT_HISTORY):", "    for nm_ in (VERDICT_HISTORY,):"),
 F("DT17_p2_guard_links_ok", _GUARD, "        if k_ not in (None, \"file\", \"link\"):\n            msg = (f\"판정 기록 자리"),
 # ── DT 전 1차 리뷰 (quench_ps 대조 · 같은 plan · 완료 전 시각 · 실행 전 기록 · 모르는 파일 · 첫 시드 녹음 판정의 '못 씀')
 F("DT18_quench_check_off", "    if q_want is None or not _same(plan.get(\"quench_ps\"), q_want):", "    if False:"),
 F("DT19_shortcut_plan_unchecked",
   "            and isinstance(fb_, dict) and fa_.get(\"plan.json\") is not None and fa_.get(\"plan.json\") == fb_.get(\"plan.json\")",
   "            and isinstance(fb_, dict)"),
 F("DT20_shortcut_time_unchecked",
   "            and _utc_before(pv_.get(\"judged_at_utc\"), current_provenance.get(\"md_done_at_utc\"))):",
   "            ):"),
 F("DT21_shortcut_attempt_unchecked", "            and fa_.get(ATTEMPT_NAME) == fb_.get(ATTEMPT_NAME)\n", ""),
 F("DT22_progress_extra_files_ok", "            and 0 <= tf_[\"n\"] < tf_[\"expected\"] and not extra_):", "            and 0 <= tf_[\"n\"] < tf_[\"expected\"]):"),
 F("DT23_md_done_time_unread", "    q = pathlib.Path(run) / MD_DONE_NAME\n    if path_kind(q) != \"file\":\n        return None",
   "    q = pathlib.Path(run) / MD_DONE_NAME\n    if True:\n        return None"),
 F("DT24_judged_time_fixed",
   "                         \"judged_at_utc\": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec=\"microseconds\"),",
   "                         \"judged_at_utc\": \"2000-01-01T00:00:00+00:00\","),
 F("DT25_after_trace_vasp_dropped", _TRACES1, _TRACES1.replace("\"final.vasp\", ", "")),
 # ── DT 전 2차 리뷰 P3 (완료 기록의 시각은 run_id · traj · thermo 해시가 맞을 때만)
 F("DT28_md_done_hash_unchecked",
   "    if not (isinstance(files, dict) and rec.get(\"traj_sha256\") is not None and rec.get(\"traj_sha256\") == files.get(\"traj.xyz\")\n"
   "            and rec.get(\"thermo_sha256\") is not None and rec.get(\"thermo_sha256\") == files.get(\"thermo.csv\")):\n        return None",
   "    if False:\n        return None"),
 F("DT29_md_done_run_id_unchecked",
   "    if not (isinstance(plan, dict) and isinstance(plan.get(\"run_id\"), str) and rec.get(\"run_id\") == plan.get(\"run_id\")):\n        return None",
   "    if False:\n        return None"),
 F("DT26_runner_melt_written_ignored",
   "                            if v.get(\"written\") is not False:   # ⭐ DT 전 1차 리뷰 P3 — 판정을 쓰지 못했으면",
   "                            if True:   # ⭐ DT 전 1차 리뷰 P3 — 판정을 쓰지 못했으면", "run", RUNR),
]

_ds_names = {m[0] for m in ds.MUT}
assert set(MOVED_DT) <= _ds_names, f"옮길 변이가 DS 판에 없다: {sorted(set(MOVED_DT) - _ds_names)}"
MUT = [MOVED_DT.get(m[0], m) for m in ds.MUT] + NEW
MUT = [(m[0], m[1], dp._keep_comment(m[2]), m[3]) for m in MUT]
dl.MUT = MUT
TAG = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--tag=")), "dt")
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
    print(f"변이 {len(MUT)} 개 (DS 판 {len(ds.MUT)} · 자리 옮김 {len(MOVED_DT)} · DT {len(NEW)}) · 자리 모두 한 번씩 · 모두 컴파일됨", flush=True)
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
            try:
                line = dl.run_one((mu, m))
            except subprocess.TimeoutExpired:                # selftest 가 시간 안에 안 끝남 — 판정 없이 ⚠ (작업자가 죽지 않게)
                line = f"{mu[0]:<32s} ⚠ 시간 제한 — selftest 가 끝나지 않았다 (멈춤 · 빨강도 초록도 아님 · 사람이 본다)"
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
