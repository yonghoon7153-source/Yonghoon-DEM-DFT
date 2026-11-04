"""DG · DH · DI · 정전 복구 · DJ · DK · DL · DM 고침 변이 검사 — DL 판 (../li2s2_dl_mutation_2026_11_04/dl_mutate.py) 의 147 개를 가져오되
thermo 판독을 다시 써서 자리가 바뀐 N6 · N8 · N9 는 새 자리로 옮기고, DM 고침 자리 (O 계열) 를 더한다. 실행 · 판정은 DL 판과 같다
(저장소 밖 복사본 3 개 · 작업자 3 개 · which = run / drv / both). --dry : 자리만 · --only=접두 : 그 접두의 변이만."""
import importlib.util, pathlib, sys

REPO = pathlib.Path("/home/user/Yonghoon-DEM-DFT")
_spec = importlib.util.spec_from_file_location("dl_mutate", REPO / "db/raw/li2s2_dl_mutation_2026_11_04/dl_mutate.py")
dl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dl)
RUNR, DRVR = dl.RUNR, dl.DRVR

MOVED = {
 "N3_end_boundary_off": ("N3_end_boundary_off", DRVR, [("    if last is not None and last >= end:\n        return \"unreadable\", (f\"완료 기록이 없는데",
                                                         "    if False:\n        return \"unreadable\", (f\"완료 기록이 없는데")], "both"),
 "N6_thermo_tail_not_counted": ("N6_thermo_tail_not_counted", DRVR, [("        n += 1                                         # 다음 기록이 시작됐다 (덜 써진 행 · 첫 칸이 맞다)",
                                                                       "        pass                                           # 다음 기록이 시작됐다 (덜 써진 행 · 첫 칸이 맞다)")], "drv"),
 "N8_thermo_mid_garbage_ok": ("N8_thermo_mid_garbage_ok", DRVR, [("            return None, f\"thermo.csv {i + 1} 번째 줄이 깨졌다 (꼬리가 아니다) — 진행량을 못 읽는다\"", "            break")], "drv"),
 "N9_cadence_off": ("N9_cadence_off", DRVR, [("            ok = (\"\\x00\" not in ln and math.isfinite(t) and i == prev + 1 and abs(t - t_of(n)) <= 1.5e-3)",
                                               "            ok = (\"\\x00\" not in ln and math.isfinite(t) and i == prev + 1)")], "drv"),
}
NEW = [
 # ── 회신 DM P0-1 — thermo 마지막 줄 (꼬리)
 ("O1_tail_time_mismatch_ok", DRVR, [("            if not (math.isfinite(tt) and abs(tt - t_of(n)) <= 1.5e-3):\n                return None, (f\"thermo.csv 마지막 줄 시각",
                                      "            if False:\n                return None, (f\"thermo.csv 마지막 줄 시각")], "both"),
 ("O2_tail_prefix_off", DRVR, [("        elif not (head and want.startswith(head)):", "        elif False:")], "drv"),
 ("O3_tail_gap_ok", DRVR, [("        if i != prev + 1:                              # ── 꼬리 (마지막 비어 있지 않은 줄)", "        if False:                              # ── 꼬리 (마지막 비어 있지 않은 줄)")], "drv"),
 ("O4_tail_nul_text_ok", DRVR, [("        if rest.strip(\"\\x00 \\t\\r\"):", "        if False:")], "drv"),
 # ── 회신 DM P0-2 — 판정 기록을 내용으로
 ("O5_noplan_verdict_check_off", DRVR, [("        ev = _verdict_evidence(f, pre_run_only=True)          # ⭐ 회신 DM P0-2", "        ev = None          # ⭐ 회신 DM P0-2")], "both"),
 ("O6_mid_verdict_check_off", DRVR, [("    ev = _verdict_evidence(f, pre_run_only=False)            # ⭐ 회신 DM P0-2", "    ev = None            # ⭐ 회신 DM P0-2")], "both"),
 ("O7_verdict_tmp_ignored", DRVR, [("    if os.path.lexists(vf.with_name(vf.name + \".tmp\")):\n        return [], \"판정 임시 파일", "    if False:\n        return [], \"판정 임시 파일")], "both"),
 ("O8_history_ignored", DRVR, [("    if os.path.lexists(hp):", "    if False:")], "both"),
 ("O9_prerun_reasons_off", DRVR, [("    if not (isinstance(rs, dict) and rs.get(\"incomplete\") == [\"plan.json 없음\"] and all(not rs.get(k) for k in rs if k != \"incomplete\")):\n        return False",
                                   "    if False:\n        return False")], "drv"),
 ("O10_prerun_provenance_off", DRVR, [("    return isinstance(fs, dict) and set(PROVENANCE_FILES) <= set(fs) and all(fs.get(x) is None for x in PROVENANCE_FILES)", "    return True")], "drv"),
 ("O11_mid_final_hash_off", DRVR, [("            if isinstance(fs, dict) and any(fs.get(x) for x in (\"final.xyz\", \"result.json\")):", "            if False:")], "drv"),
 ("O12_mid_pass_fail_off", DRVR, [("            if st in (\"pass\", \"fail\"):\n                return f\"{where} 에 과학적 판정", "            if False:\n                return f\"{where} 에 과학적 판정")], "drv"),
 ("O13_history_new_part_off", DRVR, [("            ok = (st == \"incomplete\" and isinstance(fs, dict) and set(PROVENANCE_FILES) <= set(fs)\n                  and all(fs.get(x) is None for x in PROVENANCE_FILES)) if partial else _verdict_is_pre_run(r)",
                                      "            ok = True if partial else _verdict_is_pre_run(r)")], "drv"),
]

MUT = [MOVED.get(m[0], m) for m in dl.MUT] + NEW
dl.MUT = MUT                     # DL 판의 실행 함수들이 이 목록을 쓰게 한다
dl.SP = dl.SP                    # 같은 scratchpad
_orig_make_mirror = dl.make_mirror
def make_mirror(i):
    m = dl.SP / f"mut_dm_w{i}"
    if m.exists():
        dl.shutil.rmtree(m)
    (m / "tools").mkdir(parents=True)
    dl.shutil.copytree(REPO / "tools", m / "tools", dirs_exist_ok=True)
    dl.os.symlink(REPO / "db", m / "db")
    return m
dl.make_mirror = make_mirror

if __name__ == "__main__":
    bad = dl.check_anchors()
    if bad:
        print("\n".join(bad)); sys.exit(2)
    print(f"변이 {len(MUT)} 개 (DL 판 {len(dl._dk.MUT) - len(dl.GONE) + len(dl.NEW)} · 자리 옮김 {len(MOVED)} · DM {len(NEW)}) · 자리 모두 한 번씩", flush=True)
    if "--dry" in sys.argv:
        sys.exit(0)
    only = [a.split("=", 1)[1] for a in sys.argv if a.startswith("--only=")]
    todo = [mu for mu in MUT if not only or any(mu[0].startswith(p) for p in only[0].split(","))]
    mirrors = [make_mirror(i) for i in range(dl.N_WORKERS)]
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
