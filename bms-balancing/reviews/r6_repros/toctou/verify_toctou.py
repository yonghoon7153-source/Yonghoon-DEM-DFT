#!/usr/bin/env python3
"""R6 TOCTOU 렌즈 **독립 재현** (검증자). 사용: python3 verify_toctou.py [f01|f01b|f02|f03|f04|f05a|f05b|f06|f07|f08|real|all]
worktree: $WT (기본 ./wt/bms-balancing @1049894). 모든 fixture 는 ./work/<id>/ 에. tracked 파일은 건드리지 않는다."""
import csv, hashlib, json, os, shutil, subprocess, sys, time, pathlib, importlib.util, threading, types
S = pathlib.Path(__file__).resolve().parent
WT = pathlib.Path(os.environ.get("WT", S / "wt" / "bms-balancing"))
WORK = S / "work"; PY = sys.executable; REAL_GIT = shutil.which("git")
sys.path.insert(0, str(WT / "scripts")); import provenance                     # 실제 provenance.py
SH = (WT / "scripts" / "run_states.sh").read_text(encoding="utf-8")
VERIFY_SRC = (WT / "bms_balancing" / "verify.py").read_text(encoding="utf-8")

def sh_helpers():   # tests/_shell_helpers() 와 같은 슬라이스: write_meta … / say · check_run_id · check_artifact · run
    return SH[SH.index("write_meta ()"):SH.index('\nmkdir -p "$OUT"')] + "\n" + SH[SH.index("say ()"):SH.index("\nfail=0")]
def sh_block(kind):  # run_states.sh 의 degeneracy 블록(176-187) / matrix 블록(189-194) 원문 + 마지막 요약
    if kind == "degeneracy": a, b = SH.index('  tmp="$OUT/.degeneracy_'), SH.index('\n  run "matrix $st"')
    else: a, b = SH.index('  run "matrix $st"'), SH.index('\n  run "profile $st"')
    return SH[a:b] + "\n" + SH[SH.index("say '\\n====="):]

FAKE_VERIFY = '''# 가짜 bms_balancing.verify — 계산 대신 신호 대기; 게시 코드(publish_lock·atomic_write_csv)는 실제 verify.py 원문 슬라이스
import json, os, sys, time, tempfile
from pathlib import Path
def _wait(p):
    t = time.monotonic() + 60
    while not os.path.exists(p):
        assert time.monotonic() < t, p
        time.sleep(0.005)
{PUBLISH}
def main():
    sub, rid, role = sys.argv[1], os.environ["BMS_RUN_ID"], os.environ.get("ROLE", "?")
    if os.environ.get("STARTED_FILE"): Path(os.environ["STARTED_FILE"]).write_text(rid)
    code_seen = Path("code.py").read_text().strip() if Path("code.py").exists() else ""
    if os.environ.get("GO_FILE"): _wait(os.environ["GO_FILE"])
    argv = sys.argv
    if sub == "degeneracy":
        out = {"run_id": rid, "role": role, "n_starts": int(argv[argv.index("--starts") + 1]),
               "state": argv[argv.index("--state") + 1], "pad": "x" * int(os.environ.get("PAD", "0"))}
        for k in ("LAM_PE", "LAM_NE", "LLI"): out[f"{k}_percent"] = {"min": 1.0, "max": 2.0, "span": 1.0}
        print(json.dumps(out, ensure_ascii=False, indent=2))           # 실제 cmd_degeneracy 처럼 stdout 에 마지막 한 번
    else:
        out = argv[argv.index("--out") + 1]
        rows = [{"half_cell": "GITT", "si": "Li", "w_dqdv": "0", "role": role, "a_NE": os.environ.get("VAL", "1.0"),
                 "code_seen": code_seen, "run_id": rid}]
        atomic_write_csv(out, rows, list(rows[0]))
        print(f"wrote {out} (run_id {rid})")
main()
'''

def fixture(name):
    R = WORK / name; shutil.rmtree(R, ignore_errors=True)
    (R / "scripts").mkdir(parents=True); (R / "out").mkdir(); (R / "bms_balancing").mkdir()
    shutil.copy(WT / "scripts" / "provenance.py", R / "scripts" / "provenance.py")
    (R / "bms_balancing" / "__init__.py").write_text("")
    pub = VERIFY_SRC[VERIFY_SRC.index("class publish_lock:"):VERIFY_SRC.index("\ndef ", VERIFY_SRC.index("def atomic_write_csv"))]
    (R / "bms_balancing" / "verify.py").write_text(FAKE_VERIFY.replace("{PUBLISH}", pub), encoding="utf-8")
    (R / "code.py").write_text("value=1\n"); (R / ".gitignore").write_text("out/\n__pycache__/\n")
    git(R, "init", "-q"); git(R, "add", "."); git(R, "commit", "-qm", "base")
    return R
def git(R, *a):
    return subprocess.run([REAL_GIT, "-c", "user.name=t", "-c", "user.email=t@t", *a], cwd=R, check=True, capture_output=True, text=True).stdout
def driver(R, kind, override=""):
    p = R / f"driver_{kind}.sh"
    p.write_text('set -u\ncd "$FIXROOT" || exit 1\nSTATES="${STATES:-100}"; STARTS="${STARTS:-24}"; SI="${SI:-Li}"; OUT="${OUT:-out}"\n'
                 'LAST_RUN_ID=""; USED=""\n' + override + sh_helpers() + '\nmkdir -p "$OUT"\nfail=0; st="${ST:-100}"; SRC="${SRC:-GITT}"\n'
                 + sh_block(kind) + '\necho "WRAPPER_DONE fail=$fail"\nexit $fail\n', encoding="utf-8")
    return p
def env(R, **kw):
    e = dict(os.environ, FIXROOT=str(R), FIX=str(R), BMS_DATA_ROOT="synthetic", OUT="out", SI="Li", REAL_PY=PY, PYTHONDONTWRITEBYTECODE="1")
    e.pop("PYTHONPATH", None); e.update({k: str(v) for k, v in kw.items()}); return e
def start(R, drv, **kw):
    return subprocess.Popen(["bash", str(drv)], cwd=R, env=env(R, **kw), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
def wait(p, proc=None):
    t = time.monotonic() + 60
    while not os.path.exists(p):
        assert time.monotonic() < t, f"timeout {p}"
        if proc is not None: assert proc.poll() is None, (p, proc.communicate())
        time.sleep(0.005)
def touch(p): pathlib.Path(p).write_text("go")
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()[:12]
def csv_rows(p): return list(csv.DictReader(open(p, encoding="utf-8")))
def wrap(name, ae): return "\n".join("      " + l for l in ae.strip().splitlines()[-6:])
def load_script(n):
    spec = importlib.util.spec_from_file_location(n, WT / "scripts" / f"{n}.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
PAUSE_OVERRIDE = '''
python3 () {   # 검증자 멈춤점: A 는 --verify-unit 앞, B 는 write_meta heredoc 앞 (B_PAUSE_META 일 때), A 는 heredoc 앞 (A_PAUSE_META 일 때)
  if [ "${ROLE:-}" = "A" ] && [ "${1:-}" = "scripts/provenance.py" ] && [ "${2:-}" = "--verify-unit" ] && [ -n "${A_PAUSE_VERIFY:-}" ]; then
    : > "$FIX/A.at_verify"; while [ ! -e "$FIX/A.go" ]; do sleep 0.01; done; fi
  if [ "${ROLE:-}" = "B" ] && [ "${1:-}" = "-" ] && [ -n "${B_PAUSE_META:-}" ]; then
    : > "$FIX/B.at_meta"; while [ ! -e "$FIX/B.go" ]; do sleep 0.01; done; fi
  if [ "${ROLE:-}" = "A" ] && [ "${1:-}" = "-" ] && [ -n "${A_PAUSE_META:-}" ]; then
    : > "$FIX/A.at_meta"; while [ ! -e "$FIX/A.go" ]; do sleep 0.01; done; fi
  "$REAL_PY" "$@"
}
'''

# ── F01: degeneracy .part 고정 이름 + producer stdout fd 가 rename 을 넘어 산다 ──────────
def f01(pad_a=0, pad_b=300, tag="f01"):
    R = fixture(tag); drv = driver(R, "degeneracy"); OUT = R / "out"; pub = OUT / "degeneracy_100_Li.json"; meta = str(pub) + ".meta.json"
    B = start(R, drv, ROLE="B", STARTS="24", STARTED_FILE=R / "B.started", GO_FILE=R / "B.go", PAD=pad_b)
    wait(R / "B.started", B)                     # B 의 producer 가 .part 를 stdout 으로 연 채 계산 중
    A = start(R, drv, ROLE="A", STARTS="4", STARTED_FILE=R / "A.started", GO_FILE=R / "A.go", PAD=pad_a)
    wait(R / "A.started", A); touch(R / "A.go"); ao, ae = A.communicate(timeout=60)
    ja = json.loads(pub.read_text()); ma = json.load(open(meta))
    print(f"  A 끝남 rc={A.returncode} stderr 끝:\n{wrap('A', ae)}")
    print(f"  A 뒤 디스크: 게시 JSON run_id={ja['run_id'][:8]} role={ja['role']} n_starts={ja['n_starts']} | meta run_id={ma['run_id'][:8]} starts={ma['starts']} sha 일치={ma['sha256']==sha256_full(pub)} verify_unit={provenance.verify_unit(pub)}")
    touch(R / "B.go"); bo, be = B.communicate(timeout=60)
    print(f"  B 끝남 rc={B.returncode} stderr 끝:\n{wrap('B', be)}")
    try: j = json.loads(pub.read_text()); desc = f"run_id={j['run_id'][:8]} role={j['role']} n_starts={j['n_starts']}"
    except Exception as e: desc = f"깨진 JSON: {e}"
    m = json.load(open(meta))
    print(f"  최종 디스크: 게시 JSON {desc} ({pub.stat().st_size} B) | meta run_id={m['run_id'][:8]} starts={m['starts']} sha256 일치={m['sha256']==sha256_full(pub)}")
    print(f"  최종 verify_unit={provenance.verify_unit(pub)}  .part 잔존={ (OUT/'.degeneracy_100_Li.part').exists() }")
    cs = load_script("compare_states"); d = cs.load_degeneracy(OUT)
    print(f"  compare_states.load_degeneracy → {[(k, e['j'].get('role'), e['j'].get('n_starts'), e['meta']['starts']) for k, e in d.items()] or '[] (상태가 조용히 빠짐)'}")
    r = subprocess.run([PY, "scripts/compare_states.py", str(OUT)], cwd=WT, capture_output=True, text=True, timeout=60)
    print(f"  compare_states.py CLI rc={r.returncode} stderr={r.stderr.strip()[:160]!r} stdout 100행={[l for l in r.stdout.splitlines() if l.strip().startswith('100')][:1]}")
def sha256_full(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def f01b(): f01(pad_a=600, pad_b=0, tag="f01b")

# ── F02: ne_shape._write_csv — 비원자 CSV + 별도 meta, 잠금·id·sha 없음 ──────────
F02_WORKER = '''
import sys, pathlib, importlib.util, types
WT, role, outdir = pathlib.Path(sys.argv[1]), sys.argv[2], pathlib.Path(sys.argv[3])
sys.path.insert(0, str(WT)); sys.path.insert(0, str(WT / "scripts"))
spec = importlib.util.spec_from_file_location("ne_shape", WT / "scripts" / "ne_shape.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
a = types.SimpleNamespace(source="GITT", si_source="Li", out_dir=str(outdir))
val = 1.1 if role == "A" else 2.2
rows = [("100", val, 0.5, 0.45, 3.0, 1.0, 0.5 if role == "A" else 0.6, 0.15)]
art = m._write_csv(outdir, a, rows, {"100": 0.9}, 1.0, {}, consumed={"run_id": f"run-{role}", "matrix": {"sha256": "AAAAAAAA" if role == "A" else "BBBBBBBB"}})
print("wrote", art)
'''
def f02():
    R = fixture("f02"); (R / "bin").mkdir(); shim = R / "bin" / "git"
    shim.write_text(f'#!/usr/bin/env bash\n[ -n "${{GIT_REACHED:-}}" ] && : > "$GIT_REACHED"\nif [ -n "${{GIT_HOLD:-}}" ]; then while [ ! -e "$GIT_HOLD" ]; do sleep 0.01; done; fi\nexec {REAL_GIT} "$@"\n'); shim.chmod(0o755)
    (R / "f02_worker.py").write_text(F02_WORKER); OUT = R / "out"; csvp = OUT / "ne_shape_GITT_Li.csv"; metap = str(csvp) + ".meta.json"
    e = dict(os.environ, PATH=f"{R/'bin'}:{os.environ['PATH']}"); e.pop("PYTHONPATH", None)
    A = subprocess.Popen([PY, "f02_worker.py", str(WT), "A", str(OUT)], cwd=R, env=dict(e, GIT_HOLD=str(R / "A.go"), GIT_REACHED=str(R / "A.at_git")), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    wait(R / "A.at_git", A)
    print(f"  A 가 git 에서 멈춘 시점: CSV measured_shape_mV={csv_rows(csvp)[0]['measured_shape_mV']} meta 있음={os.path.exists(metap)}")
    B = subprocess.run([PY, "f02_worker.py", str(WT), "B", str(OUT)], cwd=R, env=e, capture_output=True, text=True, timeout=120)
    print(f"  B 완료 rc={B.returncode}: CSV measured={csv_rows(csvp)[0]['measured_shape_mV']} meta.consumed.run_id={json.load(open(metap))['consumed_inputs']['run_id']}")
    touch(R / "A.go"); ao, ae = A.communicate(timeout=120); r = csv_rows(csvp)[0]; m = json.load(open(metap))
    print(f"  A 재개 뒤 rc A={A.returncode} B={B.returncode}: CSV measured={r['measured_shape_mV']} gamma_target={r['gamma_target']} | meta consumed.run_id={m['consumed_inputs']['run_id']} matrix.sha256={m['consumed_inputs']['matrix']['sha256']}")
    print(f"  verify_unit(ne_shape csv)={provenance.verify_unit(csvp)}  (stderr A 끝: {ae.strip()[-120:]!r})")

# ── F03: fitted_pair_info 두 번 읽기 (행 파싱 ↔ sha256) ──────────
def f03():
    R = fixture("f03"); OUT = R / "out"; p = OUT / "matrix_100.csv"; m = load_script("ne_shape")
    with p.open("w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["half_cell", "si", "w_dqdv", "gamma_Si", "ref_gamma_Si", "run_id"])
        for i in range(400000): w.writerow(["OTHER", "Li", "0", "0.1", "0.1", "filler"])
        w.writerow(["GITT", "Li", "0", "0.4", "0.15", "run-old"])
    old = sha(p); new_p = OUT / "new.csv"
    with new_p.open("w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["half_cell", "si", "w_dqdv", "gamma_Si", "ref_gamma_Si", "run_id"]); w.writerow(["GITT", "Li", "0", "0.9", "0.15", "run-new"])
    new = sha(new_p); threading.Timer(0.15, lambda: os.replace(new_p, p)).start()
    t = time.perf_counter(); info = m.fitted_pair_info(OUT, "100", "GITT", "Li"); dt = time.perf_counter() - t
    print(f"  큰 CSV(400k 행, 파싱 {dt:.2f} s, 0.15 s 에 os.replace): gamma_target={info['gamma_target']} row.run_id={info['row']['run_id']} sha256={info['sha256'][:12]} (옛 {old} / 새 {new})")
    rp = WT / "out" / "matrix_300_0147.csv"; t = time.perf_counter(); n = len(list(csv.DictReader(rp.open()))); dt = time.perf_counter() - t
    print(f"  실제 out/matrix_300_0147.csv: {rp.stat().st_size} B, {n} 행, 파싱 {dt*1e3:.3f} ms → 창은 sub-ms")

# ── F04: git provenance 는 계산 뒤 write_meta 에서 한 번 ──────────
def f04():
    R = fixture("f04"); drv = driver(R, "matrix"); OUT = R / "out"; art = OUT / "matrix_100.csv"; meta = str(art) + ".meta.json"
    (R / "code.py").write_text("value=2\n")                                    # (i) 수정된 코드로 시작
    A = start(R, drv, ROLE="A", STARTS="24", STARTED_FILE=R / "A.started", GO_FILE=R / "A.go"); wait(R / "A.started", A)
    git(R, "checkout", "--", "code.py"); touch(R / "A.go"); A.communicate(timeout=60); m = json.load(open(meta))
    print(f"  (i) 계산이 본 code.py={csv_rows(art)[0]['code_seen']!r} → meta git_dirty={m['git_dirty']} git_modified_code={m['git_modified_code']} 시각 필드={[k for k in m if 'utc' in k]}")
    sha1 = git(R, "rev-parse", "HEAD").strip()[:8]
    A = start(R, drv, ROLE="A", STARTS="24", STARTED_FILE=R / "A2.started", GO_FILE=R / "A2.go"); wait(R / "A2.started", A)
    (R / "code.py").write_text("value=3\n"); git(R, "commit", "-qam", "during run"); sha2 = git(R, "rev-parse", "HEAD").strip()[:8]
    touch(R / "A2.go"); A.communicate(timeout=60); m = json.load(open(meta))
    print(f"  (ii) 계산이 본 code.py={csv_rows(art)[0]['code_seen']!r} (시작 SHA {sha1}) → meta git_commit={m['git_commit'][:8]} (실행 중 커밋 {sha2}) git_dirty={m['git_dirty']}")

# ── F05a/b: --verify-unit 은 시도 id 를 모른다 / 실패 사유 버림 + 로그는 B 의 것 ──────────
def f05(variant):
    R = fixture("f05" + variant); drv = driver(R, "matrix", PAUSE_OVERRIDE); OUT = R / "out"; art = OUT / "matrix_100.csv"; meta = str(art) + ".meta.json"; log = str(art) + ".log"
    A = start(R, drv, ROLE="A", STARTS="24", A_PAUSE_VERIFY="1"); wait(R / "A.at_verify", A)
    aid = csv_rows(art)[0]["run_id"]; print(f"  A: CSV+meta 게시 뒤 --verify-unit 앞에서 멈춤 (run_id {aid[:8]}, meta run_id {json.load(open(meta))['run_id'][:8]})")
    if variant == "a":
        B = subprocess.run(["bash", str(drv)], cwd=R, env=env(R, ROLE="B", STARTS="24"), capture_output=True, text=True, timeout=60)
        print(f"  B 완주 rc={B.returncode}: CSV run_id={csv_rows(art)[0]['run_id'][:8]} meta run_id={json.load(open(meta))['run_id'][:8]}")
    else:
        B = start(R, drv, ROLE="B", STARTS="24", B_PAUSE_META="1"); wait(R / "B.at_meta", B)
        print(f"  B: CSV 게시 뒤 write_meta 앞에서 멈춤: CSV run_id={csv_rows(art)[0]['run_id'][:8]} meta run_id={json.load(open(meta))['run_id'][:8]}")
    touch(R / "A.go"); ao, ae = A.communicate(timeout=60)
    print(f"  A 재개 rc={A.returncode} stderr 전문(진행줄 제외):\n" + "\n".join("      " + l for l in ae.splitlines() if l.strip() and not l.startswith("\x1b[1m==")))
    if variant == "b":
        print(f"  A 가 가리킨 .log 내용: {open(log).read().strip()!r}")
        touch(R / "B.go"); bo, be = B.communicate(timeout=60); print(f"  B 재개 rc={B.returncode}")
    bid = csv_rows(art)[0]["run_id"]
    print(f"  최종 디스크: CSV run_id={bid[:8]} meta run_id={json.load(open(meta))['run_id'][:8]} verify_unit={provenance.verify_unit(art)}  (A 의 id 는 {aid[:8]})")

# ── F06: .gitignore 와 잠금 파일 삭제 ──────────
def f06():
    names = ["out/matrix_100.csv.lock", "out/degeneracy_100_Li.json.lock", "out/matrix_100.csv.ab12cd.part", "out/matrix_100.csv.meta.ab12cd.part", "out/.degeneracy_100_Li.part", "out/x.log"]
    for n in names:
        r = subprocess.run([REAL_GIT, "check-ignore", "-v", n], cwd=WT, capture_output=True, text=True)
        print(f"  check-ignore {n}: rc={r.returncode} {r.stdout.strip() or '(규칙 없음)'}")
    R = fixture("f06"); lock = R / "out" / "x.csv.lock"
    holder = subprocess.Popen([PY, "-c", "import fcntl,sys,time; f=open(sys.argv[1],'a+'); fcntl.flock(f, fcntl.LOCK_EX); open(sys.argv[2],'w').close(); time.sleep(30)", str(lock), str(R / "held")]); wait(R / "held", holder)
    r1 = subprocess.run(["flock", "-n", str(lock), "true"]).returncode; os.unlink(lock)
    r2 = subprocess.run(["flock", "-n", str(lock), "true"]).returncode; holder.kill()
    print(f"  보유자 살아 있는 동안 flock -n rc={r1}; lock 파일 unlink 뒤(보유자 여전히 보유) flock -n rc={r2}")

# ── F07: reader(compare_states) 는 verify_unit 을 부르지 않는다 — 섞인 묶음이 표에 들어간다 ──────────
def f07():
    R = fixture("f07"); OUT = R / "out"
    for src, dst in [("degeneracy_300_0147_Li.json", "degeneracy_100_Li.json"), ("matrix_300_0147.csv", "matrix_100.csv")]:
        shutil.copy(WT / "out" / src, OUT / dst); shutil.copy(WT / "out" / (src + ".meta.json"), OUT / (dst + ".meta.json"))
    p = OUT / "matrix_100.csv"; rows = csv_rows(p); fields = list(rows[0]) + (["run_id"] if "run_id" not in rows[0] else [])
    def dump(rows):
        with p.open("w", newline="") as fh: w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(rows)
    for r in rows: r["run_id"] = "a" * 32
    dump(rows); mp = pathlib.Path(str(p) + ".meta.json"); m = json.load(open(mp)); m.update(run_id="a" * 32, sha256=sha256_full(p)); mp.write_text(json.dumps(m))
    print(f"  A 묶음(정상) 만듦: verify_unit={provenance.verify_unit(p)}")
    for r in rows: r["run_id"] = "b" * 32; r["LAM_PE_pct"] = str(float(r["LAM_PE_pct"]) + 40)    # CSV 만 "B" 의 bytes 로 교체 (write_meta 직전 죽은 B), meta 는 A
    dump(rows)
    print(f"  손으로 만든 섞인 쌍: verify_unit(matrix_100.csv)={provenance.verify_unit(p)}")
    r = subprocess.run([PY, "scripts/compare_states.py", str(OUT)], cwd=WT, capture_output=True, text=True, timeout=60)
    hits = [l for l in r.stdout.splitlines() if l.strip().startswith("100")]
    warn = [l for l in (r.stdout + r.stderr).splitlines() if any(k in l for k in ("run_id", "sha256", "불일치", "묶음", "verify"))]
    print(f"  compare_states.py rc={r.returncode} stderr={r.stderr.strip()[:200]!r}\n  100 행: {hits}\n  묶음 경고: {warn or '없음'}")

# ── F08: run_id 는 공개 열 — 복사한 producer X ──────────
def f08():
    R = fixture("f08"); drv = driver(R, "matrix", PAUSE_OVERRIDE); OUT = R / "out"; art = OUT / "matrix_100.csv"; meta = str(art) + ".meta.json"
    A = start(R, drv, ROLE="A", STARTS="24", A_PAUSE_META="1"); wait(R / "A.at_meta", A)
    aid = csv_rows(art)[0]["run_id"]; print(f"  A: CSV 게시(run_id {aid[:8]}, a_NE={csv_rows(art)[0]['a_NE']}) 뒤 write_meta 앞에서 멈춤")
    X = subprocess.run([PY, "-m", "bms_balancing.verify", "matrix", "--out", "out/matrix_100.csv"], cwd=R, env=env(R, ROLE="X", BMS_RUN_ID=aid, VAL="51.0"), capture_output=True, text=True)
    print(f"  X 가 디스크의 run_id 를 복사해 게시 rc={X.returncode}: {X.stdout.strip()[:60]}")
    touch(R / "A.go"); ao, ae = A.communicate(timeout=60); r = csv_rows(art)[0]; m = json.load(open(meta))
    print(f"  A 재개 rc={A.returncode} 요약줄={[l for l in ae.splitlines() if '통과' in l or '실패' in l]}")
    print(f"  최종 디스크: CSV role={r['role']} a_NE={r['a_NE']} run_id={r['run_id'][:8]} | meta run_id={m['run_id'][:8]} sha 일치={m['sha256']==sha256_full(art)} verify_unit={provenance.verify_unit(art)}")

def real():
    for n in ("degeneracy_300_0147_Li.json", "matrix_300_0147.csv", "profile_gamma_300_0147_Li.csv", "ne_shape_GITT_Li.csv"):
        print(f"  실제 out/{n}: verify_unit={provenance.verify_unit(WT / 'out' / n)}")

if __name__ == "__main__":
    ids = sys.argv[1:] or ["all"]
    if ids == ["all"]: ids = ["f01", "f01b", "f02", "f03", "f04", "f05a", "f05b", "f06", "f07", "f08", "real"]
    for i in ids:
        print(f"\n### {i}"); fn = {"f05a": lambda: f05("a"), "f05b": lambda: f05("b")}.get(i) or globals()[i]
        try: fn()
        except Exception as e: print(f"  !! 재현 스크립트 오류: {type(e).__name__}: {e}")
