"""회신 DR 고침 변이 검사 — DR 판 (../li2s2_dr_mutation_2026_11_05/dr_mutate.py) 의 448 개를 가져오되 DR 회신 고침으로 자리가 바뀐 것은 새 자리로
옮기고 (MOVED_DS · 뜻 그대로), DR 회신 고침 자리 (DS1–) 를 더한다. 실행 · 판정은 DR 판과 같다 (저장소 밖 복사본 · 작업자 · which = run / drv / both ·
주석 중간 자리는 '  #' — DP 판 _keep_comment). 옵션: --dry · --only=접두 (쉼표로 여럿) · --tag=이름 · --failfast · --workers=N.

뺀 것: 없음 (DR 판 머리글의 제외 설명은 그대로 — 회신 DR Q7 이 그 범위에 동의했다 · 전체 실행은 우리 쪽 실행이지 독립 재실행이 아니다)."""
import importlib.util, pathlib, sys

REPO = pathlib.Path("/home/user/Yonghoon-DEM-DFT")
_spec = importlib.util.spec_from_file_location("dr_mutate", REPO / "db/raw/li2s2_dr_mutation_2026_11_05/dr_mutate.py")
dr = importlib.util.module_from_spec(_spec)
_argv = sys.argv; sys.argv = [sys.argv[0]]
_spec.loader.exec_module(dr)
sys.argv = _argv
dq, dp, dl = dr.dq, dr.dp, dr.dl
RUNR, DRVR = dl.RUNR, dl.DRVR
F = lambda name, anchor, repl, which="both", where=DRVR: (name, where, [(anchor, repl)], which)
F2 = lambda name, pairs, which="both", where=DRVR: (name, where, pairs, which)

_LOOP_OLD_NEW = ("                if st_ in (\"invalid\", \"incomplete\") and (k_ is None or i_ > k_ or (i_ < k_ and not pre_anchor_exempt(rec_, "
                 "folder_provenance))):")
_DERIVED_NEW = "        if f in JUDGE_DERIVED_FILES and fa[f] is None and isinstance(fb[f], str) and _SHA256_RE.fullmatch(fb[f]):"

#: DR 판 변이 중 DR 회신 고침으로 자리가 바뀐 것 (뜻 그대로 · 새 자리) — --dry 의 '자리 없음' 목록에서 채웠다 (2026-11-06)
MOVED_DS = {
 # 판정 기록의 완료 필드 검사가 경로 상태 함수 (path_state_problem) 로
 "DN4_hash_format_off": F("DN4_hash_format_off", "        ph_ = path_state_problem(fs.get(x))", "        ph_ = None", "drv"),
 # 장부 기준 앞 기록 규칙이 붙음 (회신 DR P1-1) — 그 줄의 뒤 기록 · 대체 규칙 끄기는 뜻 그대로
 "DQ70_prior_nonsci_changed_off": F("DQ70_prior_nonsci_changed_off", _LOOP_OLD_NEW, "                if False:"),
 "DR62_after_anchor_ignored": F("DR62_after_anchor_ignored", _LOOP_OLD_NEW,
                                "                if st_ in (\"invalid\", \"incomplete\") and (k_ is None or (i_ < k_ and not pre_anchor_exempt(rec_, "
                                "folder_provenance))):"),
 # 파생 파일 생성 예외가 '진짜 부재 → 정상 파일' 로 (회신 DR P1-2)
 "DR3_derived_any_change": F("DR3_derived_any_change", _DERIVED_NEW,
                             "        if f in JUDGE_DERIVED_FILES and isinstance(fb[f], str) and _SHA256_RE.fullmatch(fb[f]):"),
 "DR4_derived_exception_off": F("DR4_derived_exception_off", _DERIVED_NEW + "\n            continue", "        if False:\n            continue"),
 # DS 전 1차 리뷰 — 입력 불일치 문구가 '정상 파일 아님' 갈래를 품음 · 파생 파일 임시 쓰기가 O_EXCL · O_NOFOLLOW 로 (뜻 그대로)
 "DR10_mismatch_as_error": F("DR10_mismatch_as_error", "                input_mismatch.append((f\"{SEED_GATE_RAW} 자리가 정상 파일이 아니다",
                             "                judge_err.append((f\"{SEED_GATE_RAW} 자리가 정상 파일이 아니다"),
 "DR19_derived_write_direct": F2("DR19_derived_write_direct", [
     ("            with os.fdopen(fd_, \"w\", encoding=\"utf-8\") as fh_:\n                write(fh_, clean, format=\"extxyz\")",
      "            with open(out, \"w\", encoding=\"utf-8\") as fh_:\n                write(fh_, clean, format=\"extxyz\")"),
     ("            os.replace(tmp_, out)", "            pass")]),
}

NEW = [
 # ── 회신 DR P1-1: 장부 기준 앞의 기록 — 진행 중 incomplete (입력 불일치 없음) 만 면제
 F("DS1_exempt_ignores_mismatch", "    if not (jn_ is None or (isinstance(jn_, dict) and jn_.get(\"input_mismatch\") == [])):\n        return False",
   "    if False:\n        return False"),
 F("DS2_exempt_any_status", "    if not (isinstance(rec, dict) and rec.get(\"status\") == \"incomplete\"):", "    if not isinstance(rec, dict):"),
 F("DS3_pre_anchor_rule_off", "(k_ is None or i_ > k_ or (i_ < k_ and not pre_anchor_exempt(rec_, folder_provenance))):", "(k_ is None or i_ > k_):"),
 # ── 회신 DR P1-2: 경로 상태 (없음 · 정상 파일 · 링크 · 그 밖) · 생성 예외는 부재 → 정상 파일만
 F("DS4_dir_as_absent", "        return \"nonfile:dir\" if p.is_dir() else \"nonfile:other\"", "        return None"),
 F("DS5_symlink_as_file", "        return \"link\" if p.is_file() else \"nonfile:symlink\"", "        return \"file\" if p.is_file() else None"),
 F("DS6_derived_any_nonnull", "fa[f] is None and isinstance(fb[f], str) and _SHA256_RE.fullmatch(fb[f]):", "fa[f] is None and fb[f] is not None:"),
 F("DS7_state_problem_lax", "    if h is None or h in NONFILE_STATES:\n        return None", "    if True:\n        return None"),
 F("DS8_link_prefix_off", "    if isinstance(h, str) and (_SHA256_RE.fullmatch(h) or (h.startswith(\"link:\") and _SHA256_RE.fullmatch(h[5:]))):",
   "    if isinstance(h, str) and _SHA256_RE.fullmatch(h):"),
 F("DS9_provenance_is_file_only", "    return {f: path_state(run / f) for f in names}",
   "    return {f: (_sha256_file(run / f) if (run / f).is_file() else None) for f in names}"),
 # ── DS 전 리뷰 1 차 (MD 가 끝난 뒤 들여다본 incomplete · seed_gate 경로 상태 · 안전한 임시 파일 · plan 경로 · 완료 단계 FIFO · 기록 경로 링크 · md_done 꼴)
 #    ⚠ FIFO 를 여는 변이 (막기를 통째로 끔) 는 넣지 않았다 — 시험이 멈추면 하네스의 시간 제한 예외가 작업자를 죽인다 · 대신 '막되 재시도 단계로' 를 깬다
 F("DS10_md_done_ignored", "    if \"md_done\" in pv_ and pv_[\"md_done\"] is None:\n        return True", "    if True:\n        return True"),
 F("DS11_md_outputs_not_compared", "    return (all(fa_.get(f) == fb_.get(f) for f in same_md)", "    return (True"),
 F("DS12_late_files_lax", "            and all(fa_.get(f) is None or fa_.get(f) == fb_.get(f) for f in LATE_FILES))", "            and True)"),
 F("DS13_md_done_marker_none", "                         \"md_done\": path_state(run / MD_DONE_NAME),", "                         \"md_done\": None,"),
 F("DS14_seed_gate_broken_link_read", "        if st_out is not None and not (isinstance(st_out, str) and _SHA256_RE.fullmatch(st_out)):",
   "        if st_out is not None and not (isinstance(st_out, str) and (_SHA256_RE.fullmatch(st_out) or st_out == \"nonfile:symlink\")):"),
 F2("DS15_tmp_follows_link", [("                os.unlink(tmp_)", "                pass"),
                              ("            fd_ = os.open(tmp_, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, \"O_NOFOLLOW\", 0), 0o644)",
                               "            fd_ = os.open(tmp_, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)")]),
 F("DS16_plan_oserror_incomplete", "        res = {\"status\": \"invalid\", \"reasons\": {\"invalid\": [msg_pl]}, \"run\": str(run)}",
   "        res = {\"status\": \"incomplete\", \"reasons\": {\"incomplete\": [msg_pl]}, \"run\": str(run)}"),
 F("DS17_stage_guard_retryable", "            return \"unreadable\", f\"{x} 자리에 정상 파일이 아닌 것 ({k_}) 이 있다 — 보류 (열지 않는다)\"",
   "            return \"md_incomplete\", f\"{x} 자리에 정상 파일이 아닌 것 ({k_}) 이 있다 — 보류 (열지 않는다)\""),
 F("DS18_record_link_read", "        if k_ is not None and k_ != \"file\":\n            return [], f\"판정 기록 경로",
   "        if k_ is not None and k_ not in (\"file\", \"link\"):\n            return [], f\"판정 기록 경로"),
 F("DS19_history_append_follows", "    if k_ not in (None, \"file\"):\n        raise OSError(f\"판정 이력 경로", "    if False:\n        raise OSError(f\"판정 이력 경로"),
 F("DS20_md_done_shape_off", "    if path_state_problem(pv.get(\"md_done\")):", "    if False:"),
]

_dr_names = {m[0] for m in dr.MUT}
assert set(MOVED_DS) <= _dr_names, f"옮길 변이가 DR 판에 없다: {sorted(set(MOVED_DS) - _dr_names)}"
MUT = [MOVED_DS.get(m[0], m) for m in dr.MUT] + NEW
MUT = [(m[0], m[1], dp._keep_comment(m[2]), m[3]) for m in MUT]
dl.MUT = MUT
TAG = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--tag=")), "ds")
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
    print(f"변이 {len(MUT)} 개 (DR 판 {len(dr.MUT)} · 자리 옮김 {len(MOVED_DS)} · DS {len(NEW)}) · 자리 모두 한 번씩 · 모두 컴파일됨", flush=True)
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
