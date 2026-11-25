"""DG · DH · DI · 정전 복구 · DJ · DK · DL · DM · DN 고침 변이 검사 — DM 판 (../li2s2_dm_mutation_2026_11_04/dm_mutate.py) 의 165 개를 가져오되
plan 전 판정의 이유 검사를 다시 써서 자리가 바뀐 O9_prerun_reasons_off 는 새 자리로 옮기고, DN 고침 자리 (DN1–DN9 · 판정 기록의 완료 판단
필드 타입 · 이력의 새 판정 지문 · plan 전 판정 이유의 꼴) 를 더한다. 실행 · 판정은 DL 판과 같다 (저장소 밖 복사본 3 개 · 작업자 3 개 ·
which = run / drv / both). --dry : 자리만 · --only=접두 : 그 접두의 변이만 (쉼표로 여럿)."""
import importlib.util, pathlib, sys

REPO = pathlib.Path("/home/user/Yonghoon-DEM-DFT")
_spec = importlib.util.spec_from_file_location("dm_mutate", REPO / "db/raw/li2s2_dm_mutation_2026_11_04/dm_mutate.py")
dm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dm)
dl = dm.dl
RUNR, DRVR = dl.RUNR, dl.DRVR

MOVED = {
 "O9_prerun_reasons_off": ("O9_prerun_reasons_off", DRVR, [("    if rs != {\"incomplete\": [\"plan.json 없음\"]}:\n        return False",
                                                           "    if False:\n        return False")], "drv"),
}
BAD_IF = "        if (isinstance(v, bool) and bool not in kinds) or not isinstance(v, kinds):"
NEW = [
 # ── 회신 DN P1 — 도중 끊김 후보의 완료 판단 필드: 있는데 타입이 틀리면 해석할 수 없는 기록 (보류)
 ("DN1_completion_fields_off", DRVR, [("            tp = _completion_fields_problem(r, partial, where)", "            tp = None")], "both"),
 ("DN2_type_check_off", DRVR, [(BAD_IF, "        if False:")], "both"),
 ("DN3_bool_as_int", DRVR, [(BAD_IF, "        if not isinstance(v, kinds):")], "drv"),
 ("DN4_hash_format_off", DRVR, [("        if h is not None and not (isinstance(h, str) and re.fullmatch(r\"[0-9a-f]{64}\", h)):", "        if False:")], "drv"),
 ("DN5_range_off", DRVR, [("        if v is not None and v < lo:", "        if False:")], "drv"),
 ("DN6_history_provenance_coerced", DRVR, [("                                                   \"provenance\": h.get(\"new_provenance\")}, True))",
                                            "                                                   \"provenance\": h.get(\"new_provenance\") if isinstance(h.get(\"new_provenance\"), dict) else None}, True))")], "drv"),
 ("DN7_prerun_reasons_loose", DRVR, [("    if rs != {\"incomplete\": [\"plan.json 없음\"]}:",
                                      "    if not (isinstance(rs, dict) and rs.get(\"incomplete\") == [\"plan.json 없음\"] and all(not rs.get(k) for k in rs if k != \"incomplete\")):")], "drv"),
 ("DN8_container_type_off", DRVR, [("    for key in (\"gate_check\", \"checks\"):\n        p = bad(r, key, (dict,), where)",
                                    "    for key in ():\n        p = bad(r, key, (dict,), where)")], "drv"),
 ("DN9_n_not_checked", DRVR, [("    for key, lo in ((\"n\", 0), (\"expected\", 1)):", "    for key, lo in ((\"expected\", 1),):")], "both"),
]

MUT = [MOVED.get(m[0], m) for m in dm.MUT] + NEW
dl.MUT = MUT
def make_mirror(i):
    m = dl.SP / f"mut_dn_w{i}"
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
    names = [mu[0] for mu in MUT]
    assert len(names) == len(set(names)), "변이 이름이 겹친다"
    print(f"변이 {len(MUT)} 개 (DM 판 {len(dm.MUT)} · 자리 옮김 {len(MOVED)} · DN {len(NEW)}) · 자리 모두 한 번씩", flush=True)
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
