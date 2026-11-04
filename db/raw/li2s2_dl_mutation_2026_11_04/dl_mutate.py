"""DG · DH · DI · 정전 복구 · DJ · DK · DL 고침 변이 검사 — 저장소 밖 복사본 (작업자마다 하나) 에서 고친 곳을 하나씩 되돌려 해당 selftest 가
빨개지는지 본다. DK 판 (db/raw/li2s2_dk_mutation_2026_11_04/dk_mutate.py) 의 125 개를 그대로 가져오되, DL 고침으로 자리가 없어진
L6 · L7 (folder_stage 다시 씀) 은 새 자리 (N22 · N23) 로 옮기고, DL 고침 자리 변이 (N 계열) 를 더한다.
which: "run" = 러너 selftest · "drv" = 드라이버 selftest · "both" = 드라이버 → (초록이면) 러너.
--dry : 변이 자리가 정확히 한 번씩 있는지만 본다 (실행 안 함)."""
import importlib.util, os, pathlib, shutil, subprocess, sys

SP = pathlib.Path("/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad")
REPO = pathlib.Path("/home/user/Yonghoon-DEM-DFT")
RUNR, DRVR = "tools/ionic/li2s2_stage1_runner.py", "tools/ionic/melt_quench_uma.py"
N_WORKERS = 3

_spec = importlib.util.spec_from_file_location("dk_mutate", REPO / "db/raw/li2s2_dk_mutation_2026_11_04/dk_mutate.py")
_dk = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_dk)
GONE = ("L6_missing_marker_complete", "L7_bad_marker_incomplete")

NEW = [
 # ── 회신 DL P0 · Q2 — 완료 단계 판독 (folder_stage_detail)
 ("N1_tmp_ignored", DRVR, [("    if os.path.lexists(f / MD_DONE_TMP):\n        return \"unreadable\", \"MD 완료 기록 임시 파일이 남았다",
                            "    if False:\n        return \"unreadable\", \"MD 완료 기록 임시 파일이 남았다")], "both"),
 ("N2_noplan_extras_ignored", DRVR, [("        if extra:\n            return \"unreadable\", f\"plan.json 없이",
                                      "        if False:\n            return \"unreadable\", f\"plan.json 없이")], "both"),
 ("N3_end_boundary_off", DRVR, [("    if last >= end:\n        return \"unreadable\", (f\"완료 기록이 없는데",
                                 "    if False:\n        return \"unreadable\", (f\"완료 기록이 없는데")], "both"),
 ("N4_end_is_planned", DRVR, [("    end = (want // save_int) * save_int", "    end = want")], "drv"),
 ("N5_fire_log_rule_off", DRVR, [("    if os.path.lexists(f / \"final_relax.log\"):\n        return \"unreadable\", \"FIRE 로그가",
                                  "    if False:\n        return \"unreadable\", \"FIRE 로그가")], "drv"),
 ("N6_thermo_tail_not_counted", DRVR, [("        if j == len(idx) - 2:                          # 마지막 비어 있지 않은 줄 = 덜 써진 꼬리 → 시작된 기록\n            n += 1\n            break",
                                        "        if j == len(idx) - 2:                          # 마지막 비어 있지 않은 줄 = 덜 써진 꼬리 → 시작된 기록\n            break")], "drv"),
 ("N7_traj_tail_not_counted", DRVR, [("        if i + nat + 1 > last:                           # 덜 써진 마지막 프레임\n            n += 1\n            break",
                                      "        if i + nat + 1 > last:                           # 덜 써진 마지막 프레임\n            break")], "drv"),
 ("N8_thermo_mid_garbage_ok", DRVR, [("        return None, f\"thermo.csv {i + 1} 번째 줄이 깨졌다 (꼬리가 아니다) — 진행량을 못 읽는다\"", "        break")], "drv"),
 ("N9_cadence_off", DRVR, [("                  and abs(t - n * save_int * dt / 1000.0) <= 1.5e-3)", "                  )")], "drv"),
 ("N10_traj_mid_garbage_ok", DRVR, [("            return None, f\"traj.xyz {i + 1} 번째 줄에서 프레임 머리가 깨졌다 (꼬리가 아니다) — 진행량을 못 읽는다\"", "            break")], "drv"),
 ("N11_progress_thermo_only", DRVR, [("    for nm, fn in ((\"thermo.csv\", _thermo_last_step), (\"traj.xyz\", _traj_last_step)):",
                                      "    for nm, fn in ((\"thermo.csv\", _thermo_last_step),):")], "drv"),
 ("N12_progress_traj_only", DRVR, [("    for nm, fn in ((\"thermo.csv\", _thermo_last_step), (\"traj.xyz\", _traj_last_step)):",
                                    "    for nm, fn in ((\"traj.xyz\", _traj_last_step),):")], "drv"),
 ("N18_header_check_off", DRVR, [("    if idx[0] != 0 or lines[0].split(\",\")[0].strip() != \"t_ps\":\n        return None, \"thermo.csv 첫 줄이",
                                  "    if False:\n        return None, \"thermo.csv 첫 줄이")], "drv"),
 ("N19_nonmd_verdict_missing", DRVR, [("NON_MD_FILES = frozenset({ATTEMPT_NAME, ATTEMPT_NAME + \".tmp\", \"stage1_verdict.json\", \"stage1_verdict.json.tmp\", VERDICT_HISTORY})",
                                       "NON_MD_FILES = frozenset({ATTEMPT_NAME, ATTEMPT_NAME + \".tmp\"})")], "drv"),
 ("N21_consumer_unreadable_ok", DRVR, [("            if st_p == \"unreadable\":\n                invalid.append(f\"{tag}: 앞 실행 {str(p_.get('run_id'))[:8]} 폴더의 완료 단계를 못 읽는데",
                                        "            if False:\n                invalid.append(f\"{tag}: 앞 실행 {str(p_.get('run_id'))[:8]} 폴더의 완료 단계를 못 읽는데")], "run"),
 ("N22_mid_cut_as_complete", DRVR, [("    return \"md_incomplete\", f\"명확한 도중 끊김", "    return \"md_complete\", f\"명확한 도중 끊김")], "run"),
 ("N23_bad_marker_incomplete", DRVR, [("               (\"unreadable\", \"MD 완료 기록이 plan · 궤적 · thermo 와 안 맞는다", "               (\"md_incomplete\", \"MD 완료 기록이 plan · 궤적 · thermo 와 안 맞는다")], "run"),
 ("N24_tmp_as_complete", DRVR, [("        return \"unreadable\", \"MD 완료 기록 임시 파일이 남았다 — 기록 도중 끊김 (완료로 승인하지 않고 보류)\"",
                                 "        return \"md_complete\", \"MD 완료 기록 임시 파일이 남았다 — 기록 도중 끊김 (완료로 승인하지 않고 보류)\"")], "drv"),
 # ── 회신 DL P1-1 — 완료 기록 저장 순서 · 동기화
 ("N13_no_data_fsync", DRVR, [("    for nm in (\"traj.xyz\", \"thermo.csv\"):\n        if (out / nm).is_file():\n            _fsync_file(out / nm)",
                               "    for nm in ():\n        if (out / nm).is_file():\n            _fsync_file(out / nm)")], "drv"),
 ("N14_no_tmp_fsync", DRVR, [("        _fsync_handle(fh)\n    os.replace(tmp, out / MD_DONE_NAME)", "        pass\n    os.replace(tmp, out / MD_DONE_NAME)")], "drv"),
 ("N15_no_dir_fsync", DRVR, [("    os.replace(tmp, out / MD_DONE_NAME)\n    _fsync_dir(out)\n    return rec", "    os.replace(tmp, out / MD_DONE_NAME)\n    return rec")], "drv"),
 ("N16_dir_fsync_before_replace", DRVR, [("    os.replace(tmp, out / MD_DONE_NAME)\n    _fsync_dir(out)\n    return rec", "    _fsync_dir(out)\n    os.replace(tmp, out / MD_DONE_NAME)\n    return rec")], "drv"),
 # ── 회신 DL P1-2 — FIRE 전에 기록 (순서를 지키는 회귀시험)
 ("N17_md_done_after_fire", DRVR, [("    write_md_done(out, run_id=run_id, n_steps_planned=n_m + n_q + n_h, n_steps_done=step)   # ⭐ 회신 DK — MD 완료의 증거 (FIRE 전)\n"
                                    "    FIRE(atoms, logfile=str(out / \"final_relax.log\")).run(fmax=0.05, steps=2000)",
                                    "    FIRE(atoms, logfile=str(out / \"final_relax.log\")).run(fmax=0.05, steps=2000)\n"
                                    "    write_md_done(out, run_id=run_id, n_steps_planned=n_m + n_q + n_h, n_steps_done=step)   # ⭐ 회신 DK — MD 완료의 증거 (FIRE 전)")], "drv"),
 # ── 러너 쪽 (회신 DL P0 — 러너가 같은 판독을 쓴다)
 ("N25_runner_stage_plain", RUNR, [("        st, st_why = mq.folder_stage_detail(rec[\"path\"])", "        st, st_why = (\"md_incomplete\", \"\")")], "run"),
]

MUT = [m for m in _dk.MUT if m[0] not in GONE] + NEW


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
    m = SP / f"mut_dl_w{i}"
    if m.exists():
        shutil.rmtree(m)
    (m / "tools").mkdir(parents=True)
    shutil.copytree(REPO / "tools", m / "tools", dirs_exist_ok=True)
    os.symlink(REPO / "db", m / "db")
    return m


def _selftest(m, rel):
    env = {**os.environ, "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"}
    r = subprocess.run([sys.executable, str(m / rel), "--selftest"], capture_output=True, text=True, timeout=1800, cwd=str(m), env=env)
    out = r.stdout + r.stderr
    reds = [ln for ln in out.splitlines() if ln.startswith("  ⛔ ")]
    tail = out.strip().splitlines()[-1][:140] if out.strip() else ""
    return r.returncode, (reds[0][:150] if reds else tail)


def run_one(args):
    (name, rel, reps, which), m = args
    f = m / rel
    orig = f.read_text(encoding="utf-8")
    try:
        s = orig
        for old, new in reps:
            if s.count(old) != 1:
                return f"{name:<32s} ⚠ 변이 자리 {s.count(old)} 개"
            s = s.replace(old, new, 1)
        try:
            compile(s, str(f), "exec")
        except SyntaxError as e:
            return f"{name:<32s} ⚠ 변이가 문법 오류 ({e.msg}) — 무효 변이"
        f.write_text(s, encoding="utf-8")
        order = {"run": [RUNR], "drv": [DRVR], "both": [DRVR, RUNR]}[which]
        for tgt in order:
            rc, msg = _selftest(m, tgt)
            if rc != 0:
                return f"{name:<32s} ⭕ 빨강 [{pathlib.Path(tgt).stem}] · {msg}"
        return f"{name:<32s} ⛔ 초록 (못 잡음) · {msg}"
    finally:
        f.write_text(orig, encoding="utf-8")


if __name__ == "__main__":
    bad = check_anchors()
    if bad:
        print("\n".join(bad)); sys.exit(2)
    print(f"변이 {len(MUT)} 개 (DK 판 {len(_dk.MUT)} − 자리 없어진 {len(GONE)} + DL {len(NEW)}) · 자리 모두 한 번씩", flush=True)
    if "--dry" in sys.argv:
        sys.exit(0)
    only = [a.split("=", 1)[1] for a in sys.argv if a.startswith("--only=")]
    todo = [mu for mu in MUT if not only or any(mu[0].startswith(p) for p in only[0].split(","))]
    mirrors = [make_mirror(i) for i in range(N_WORKERS)]
    import queue, threading
    q = queue.Queue()
    for mu in todo:
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
    print(f"끝: 빨강 {n_red} / {len(todo)}", flush=True)
