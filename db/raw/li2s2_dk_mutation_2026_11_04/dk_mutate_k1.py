"""DG · DH · DI · 정전 복구 · DJ · DK 고침 변이 검사 — 저장소 밖 복사본 (작업자마다 하나) 에서 고친 곳을 하나씩 되돌려 해당 selftest 가
빨개지는지 본다. 작업자 3 개 병렬. 끝나면 복사본은 그대로 두고 (원본 저장소는 안 건드린다) 결과를 한 줄씩 찍는다.
--dry : 변이 자리가 정확히 한 번씩 있는지만 본다 (실행 안 함)."""
import pathlib, subprocess, sys, shutil, os, concurrent.futures as cf

SP = pathlib.Path("/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad")
REPO = pathlib.Path("/home/user/Yonghoon-DEM-DFT")
RUNR, DRVR = "tools/ionic/li2s2_stage1_runner.py", "tools/ionic/melt_quench_uma.py"
N_WORKERS = 1

MUT = [
 ("K1_ledger_scientific", RUNR, [("        if v in (\"pass\", \"fail\"):\n            return {\"ok\": False, \"code\": \"invalid\", \"why\": f\"이전 실행 {tag} 에 과학적 판정", "        if False:\n            return {\"ok\": False, \"code\": \"invalid\", \"why\": f\"이전 실행 {tag} 에 과학적 판정")], "run"),
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
    m = SP / f"mut_dkf_w{i}"
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
