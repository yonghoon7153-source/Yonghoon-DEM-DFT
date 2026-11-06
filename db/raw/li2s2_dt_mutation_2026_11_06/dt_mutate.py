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

_SHORTCUT = ("    if pv_.get(\"md_progress\") == \"in_progress\" and isinstance(fa_, dict) and all(f in fa_ and fa_[f] is None for f in LATE_FILES):")
_GUARD = "        if k_ not in (None, \"file\"):\n            msg = (f\"판정 기록 자리"

#: DS 판 변이 중 DS 회신 고침으로 자리가 바뀐 것 (뜻 그대로 · 새 자리) — --dry 의 '자리 0 개' 목록에서 채웠다 (2026-11-06)
MOVED_DT = {
 # '진행 중' 지름길이 md_done · md_complete_seen 대신 md_progress (진행 중 확인) + 뒤 산출물 없음으로 (회신 DS P1-1)
 "DS10_md_done_ignored": F("DS10_md_done_ignored", _SHORTCUT, "    if True:"),
 "DS21_md_seen_ignored": F("DS21_md_seen_ignored", _SHORTCUT,
                           "    if isinstance(fa_, dict) and all(f in fa_ and fa_[f] is None for f in LATE_FILES):"),
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
   "            and 0 <= tf_[\"n\"] < tf_[\"expected\"]):",
   "            ):"),
 F("DT5_progress_record_inprog", "                         \"md_progress\": md_progress(run, plan, gate, checks),",
   "                         \"md_progress\": \"in_progress\","),
 F("DT6_progress_record_unknown", "                         \"md_progress\": md_progress(run, plan, gate, checks),",
   "                         \"md_progress\": \"unknown\","),
 F("DT7_after_trace_result_dropped",
   "MD_AFTER_TRACES = (MD_DONE_NAME, MD_DONE_TMP, \"final_relax.log\", \"final.xyz\", \"result.json\", \"md_init_raw.xyz\")",
   "MD_AFTER_TRACES = (MD_DONE_NAME, MD_DONE_TMP, \"final_relax.log\", \"final.xyz\", \"md_init_raw.xyz\")"),
 F("DT8_after_trace_tmp_dropped",
   "MD_AFTER_TRACES = (MD_DONE_NAME, MD_DONE_TMP, \"final_relax.log\", \"final.xyz\", \"result.json\", \"md_init_raw.xyz\")",
   "MD_AFTER_TRACES = (MD_DONE_NAME, \"final_relax.log\", \"final.xyz\", \"result.json\", \"md_init_raw.xyz\")"),
 F("DT9_after_trace_fire_log_dropped",
   "MD_AFTER_TRACES = (MD_DONE_NAME, MD_DONE_TMP, \"final_relax.log\", \"final.xyz\", \"result.json\", \"md_init_raw.xyz\")",
   "MD_AFTER_TRACES = (MD_DONE_NAME, MD_DONE_TMP, \"final.xyz\", \"result.json\", \"md_init_raw.xyz\")"),
 # ── 회신 DS P1-1: 기준 앞 '진행 중' 지름길
 F("DT10_shortcut_late_ignored", _SHORTCUT, "    if pv_.get(\"md_progress\") == \"in_progress\":"),
 F("DT11_shortcut_old_rule", _SHORTCUT,
   "    if \"md_done\" in pv_ and pv_[\"md_done\"] is None and pv_.get(\"md_complete_seen\") is False:"),
 # ── 회신 DS P1-1: 기록 꼴
 F("DT12_prerun_keys_no_progress", "                                     \"md_complete_seen\", \"md_progress\"})",
   "                                     \"md_complete_seen\"})"),
 F("DT13_progress_vocab_off",
   "    if pv.get(\"md_progress\") is not None and pv.get(\"md_progress\") not in MD_PROGRESS_STATES:", "    if False:"),
 # ── 회신 DS P2-1: 직접 판정도 비정상 판정 · 이력 자리를 거부
 F("DT14_p2_guard_off", _GUARD, "        if False:\n            msg = (f\"판정 기록 자리"),
 F("DT15_p2_guard_verdict_only", "    for nm_ in (\"stage1_verdict.json\", VERDICT_HISTORY):", "    for nm_ in (\"stage1_verdict.json\",):"),
 F("DT16_p2_guard_history_only", "    for nm_ in (\"stage1_verdict.json\", VERDICT_HISTORY):", "    for nm_ in (VERDICT_HISTORY,):"),
 F("DT17_p2_guard_links_ok", _GUARD, "        if k_ not in (None, \"file\", \"link\"):\n            msg = (f\"판정 기록 자리"),
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
