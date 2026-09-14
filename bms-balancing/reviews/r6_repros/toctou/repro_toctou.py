#!/usr/bin/env python3
"""R6 자체 리뷰 · 렌즈 = 순서/TOCTOU. 대상 커밋 1049894, 범위 bms-balancing/.

발견마다 함수 하나. **잘못된 결과가 재현되면 assert 가 통과**한다 (수정 뒤에는 실패해야 한다).
tracked 파일은 건드리지 않는다 — 모든 산출은 이 파일 옆 `tmp/` 아래 mkdtemp 에.

    python3 repro_toctou.py            # 전부
    python3 repro_toctou.py f01 f02    # 일부

shell helper 는 tests/test_review_findings.py::_shell_helpers 와 같은 방식으로 원본
scripts/run_states.sh 에서 함수를 잘라 온다 (write_meta · say · check_run_id · check_artifact · run).
degeneracy 블록(run → flock mv → write_meta → --verify-unit)은 원본 176-187 행을 **그대로** 잘라 쓰고,
`python3 -m bms_balancing.verify` 만 PYTHONPATH 의 가짜 패키지로 바꿔 끼운다 (shell 문장은 한 글자도 안 바꾼다).
"""
from __future__ import annotations
import csv, hashlib, json, os, pathlib, shutil, subprocess, sys, tempfile, textwrap, time

HERE = pathlib.Path(__file__).resolve().parent
REPO = pathlib.Path("/home/user/Yonghoon-DEM-DFT/bms-balancing")
SH = (REPO / "scripts" / "run_states.sh").read_text(encoding="utf-8")
PY = sys.executable
TMP = HERE / "tmp"; TMP.mkdir(exist_ok=True)
sys.path.insert(0, str(REPO / "scripts")); sys.path.insert(0, str(REPO))
import provenance, compare_states                                   # noqa: E402  (원본 소비자·검증자)


# ── 공통 ────────────────────────────────────────────────────────────────────────
def shell_helpers() -> str:
    """tests/test_review_findings.py::_shell_helpers 와 동일한 슬라이스."""
    return (SH[SH.index("write_meta ()"):SH.index('\nmkdir -p "$OUT"')]
            + "\n" + SH[SH.index("say ()"):SH.index("\nfail=0")])


def degeneracy_block() -> str:
    """run_states.sh 176-187 행 그대로 (tmp= … fi)."""
    s = SH.index('  tmp="$OUT/.degeneracy_')
    e = SH.index("\n  fi\n", s) + len("\n  fi\n")
    return SH[s:e]


def matrix_block() -> str:
    """run_states.sh 189-194 행 그대로 (run "matrix $st" … || fail=$((fail+1)))."""
    s = SH.index('  run "matrix $st"')
    e = SH.index("\n\n", s)
    return SH[s:e] + "\n"


def summary_tail() -> str:
    """run_states.sh 207-213 행 (전부 통과 / 실패 N 건 — 위의 .log 를 볼 것)."""
    s = SH.index("say '\\n=====")
    e = SH.index("say \"설정:")
    return SH[s:e]


def git(root, *a):
    return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *a], cwd=root,
                          check=True, capture_output=True, text=True).stdout


def fixture_repo(root: pathlib.Path):
    """tests::_fixture_repo 와 같은 모양: scripts/provenance.py 사본 + code.py + out/ 를 커밋한 git 저장소."""
    (root / "scripts").mkdir(parents=True); (root / "out").mkdir(exist_ok=True)
    shutil.copyfile(REPO / "scripts" / "provenance.py", root / "scripts" / "provenance.py")
    (root / "code.py").write_text("value = 1\n", encoding="utf-8")
    (root / "out" / ".keep").write_text("", encoding="utf-8")
    git(root, "init", "-q"); git(root, "add", "."); git(root, "commit", "-qm", "base")
    return root


def fake_verify_pkg(where: pathlib.Path) -> pathlib.Path:
    """PYTHONPATH 에 놓을 가짜 `bms_balancing.verify`: degeneracy 는 stdout 으로 JSON, matrix 는 --out 에 CSV.
    ROLE/FIXTURE 환경으로 '시작' 신호를 내고 `<ROLE>.go` 가 생길 때까지 **계산 중**인 척 기다린다 (실제 명령의 긴
    최적화 구간). run_id 는 실제 verify.py 처럼 BMS_RUN_ID 에서."""
    pkg = where / "fakepkg" / "bms_balancing"; pkg.mkdir(parents=True)
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "verify.py").write_text(textwrap.dedent('''
        import csv, json, os, sys, time, pathlib
        a = sys.argv[1:]; sub = a[0]
        role = os.environ["ROLE"]; fx = pathlib.Path(os.environ["FIXTURE"])
        starts = int(a[a.index("--starts") + 1]); state = a[a.index("--state") + 1]
        rid = os.environ.get("BMS_RUN_ID")
        (fx / f"{role}.started").write_text("1")
        t = time.monotonic() + 120
        while not (fx / f"{role}.go").exists():
            assert time.monotonic() < t, "go timeout"; time.sleep(0.01)
        if sub == "degeneracy":
            out = {"state": state, "n_starts": starts, "run_id": rid, "role": role,
                   "best_modes_percent": {"LAM_PE": 1.0 if role == "A" else 9.0},
                   "pad": os.environ.get("PAD", "")}
            print(json.dumps(out))                       # 실제 명령처럼 stdout 으로만
        elif sub == "matrix":
            outp = pathlib.Path(a[a.index("--out") + 1])
            tmp = outp.with_name(outp.name + f".{os.getpid()}.part")
            lo = 1.0 if role == "A" else 7.0                     # role 마다 다른 숫자 (compare_states 가 폭을 계산한다)
            with tmp.open("w", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=["half_cell", "si", "w_dqdv", "run_id", "role", "LAM_PE_pct", "LAM_NE_pct",
                                                   "LLI_pct", "bounds", "ref_bounds", "gamma_Si", "ref_gamma_Si"])
                w.writeheader()
                for k in (0.0, 1.0 if role == "A" else 2.0):
                    w.writerow({"half_cell": "GITT", "si": "Li", "w_dqdv": 0, "run_id": rid, "role": role, "LAM_PE_pct": lo + k,
                                "LAM_NE_pct": lo + k, "LLI_pct": lo + k, "bounds": "-", "ref_bounds": "-", "gamma_Si": 0.4, "ref_gamma_Si": 0.3})
            import fcntl
            with open(str(outp) + ".lock", "a+") as lk:
                fcntl.flock(lk, fcntl.LOCK_EX); os.replace(tmp, outp)
            print(f"wrote {outp} (run_id {rid})")
        (fx / f"{role}.printed").write_text("1")
    '''), encoding="utf-8")
    return pkg.parent


def wait_for(path: pathlib.Path, proc=None, timeout=60.0):
    t = time.monotonic() + timeout
    while not path.exists():
        if proc is not None and proc.poll() is not None:
            o, e = proc.communicate()
            raise AssertionError(f"process exited early rc={proc.returncode}\n{o}\n{e}")
        assert time.monotonic() < t, f"timeout waiting {path}"
        time.sleep(0.01)


def sha(p) -> str:
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def banner(name, doc):
    print("\n" + "=" * 100 + f"\n{name}: {doc}\n" + "=" * 100)


# ── F01 · degeneracy 의 `.part` 는 producer 의 stdout fd — rename 뒤에도 살아서 게시된 파일에 쓴다 ────────
def f01_degeneracy_stdout_fd_survives_rename(pad_a: str = "") -> dict:
    """[F01] run_states.sh:176 `tmp="$OUT/.degeneracy_${st}_${SI}.part"` 는 시도마다 **같은 이름**이고, 그 파일이
    producer 의 stdout (`> "$redir"`, run_states.sh:131) 이다. 느린 B 가 계산 중인 동안 빠른 A 가 끝나 `.part` 를
    검사·`flock mv`·write_meta·--verify-unit 까지 전부 통과("OK")한 뒤, B 가 JSON 을 찍으면 B 의 fd 는 **rename 된
    inode = 이미 게시된 degeneracy_*.json** 을 가리킨다 → 잠금·검사 밖에서 게시 파일이 B 의 bytes 로 바뀐다.
    남는 것: JSON = B (또는 B + A 의 꼬리 = 깨진 JSON), meta = A(run_id·sha256·starts 전부 A), wrapper A 는 OK."""
    root = fixture_repo(pathlib.Path(tempfile.mkdtemp(prefix="f01_", dir=TMP)) / "repo")
    fx = root.parent; ppath = fake_verify_pkg(fx)
    body = ("st=100\nSRC=GITT\nfail=0\n" + degeneracy_block() + '\necho "FAIL_COUNT=$fail"\nexit $fail\n')
    cmd = ["bash", "-c", shell_helpers() + "\n" + body, "f01"]

    def env(role, starts, pad=""):
        return dict(os.environ, STATES="100", STARTS=starts, SI="Li", OUT=str(root / "out"), BMS_DATA_ROOT="synthetic",
                    PYTHONPATH=str(ppath), ROLE=role, FIXTURE=str(fx), PAD=pad)
    b = subprocess.Popen(cmd, cwd=root, env=env("B", "24"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    wait_for(fx / "B.started", b)                                   # B(STARTS=24, 본 실행) 가 계산 중
    a = subprocess.Popen(cmd, cwd=root, env=env("A", "4", pad_a), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    wait_for(fx / "A.started", a)
    (fx / "A.go").write_text("1")                                   # A(STARTS=4, 배관 확인) 가 먼저 끝난다
    ao, ae = a.communicate(timeout=60)
    final = root / "out" / "degeneracy_100_Li.json"; meta_p = final.with_name(final.name + ".meta.json")
    assert a.returncode == 0 and "OK" in ae and "FAIL_COUNT=0" in ao, (ao, ae)
    j_a = json.loads(final.read_text()); meta = json.loads(meta_p.read_text())
    assert j_a["role"] == "A" and meta["run_id"] == j_a["run_id"] and meta["sha256"] == sha(final)
    vu_a = provenance.verify_unit(final)
    assert vu_a == (True, "일치"), vu_a                              # A 시점: 온전한 묶음, wrapper OK
    print(f"  A 끝남: rc={a.returncode} stderr 마지막줄={ae.strip().splitlines()[-1]!r}")
    print(f"  A 시점 verify_unit={vu_a}  meta.run_id={meta['run_id'][:8]} starts={meta['starts']}")
    (fx / "B.go").write_text("1")                                   # 몇 시간 뒤 B 가 JSON 을 찍는다
    bo, be = b.communicate(timeout=60)
    raw = final.read_bytes()
    try:
        j = json.loads(raw); corrupt = False
    except json.JSONDecodeError as e:
        j, corrupt = None, True; err = str(e)
    meta2 = json.loads(meta_p.read_text())
    vu = provenance.verify_unit(final)
    print(f"  B 끝남: rc={b.returncode} stderr 마지막 3줄:\n    " + "\n    ".join(be.strip().splitlines()[-3:]))
    print(f"  게시 파일 지금: {'깨진 JSON: ' + err if corrupt else 'role=' + j['role'] + ' run_id=' + j['run_id'][:8] + ' n_starts=' + str(j['n_starts'])}")
    print(f"  meta 지금: run_id={meta2['run_id'][:8]} starts={meta2['starts']} sha256 일치={meta2['sha256'] == sha(raw and final)}")
    print(f"  verify_unit 지금: {vu}")
    print(f"  .part 남았나: {(root / 'out' / '.degeneracy_100_Li.part').exists()}  lock: {sorted(p.name for p in (root/'out').glob('*.lock'))}")
    assert b.returncode != 0 and "run id 가 산출물의 run_id 필드에 없다" in be, be   # B 는 자기 결과를 잃는다
    assert meta2 == meta, "meta 는 A 그대로"
    assert vu[0] is False, vu
    if not corrupt:
        assert j["role"] == "B" and j["run_id"] != meta2["run_id"] and meta2["starts"] == 4 and j["n_starts"] == 24
    # 소비자: compare_states 는 verify_unit 을 안 부른다 — 섞인 묶음을 그대로 읽는다
    deg = compare_states.load_degeneracy(root / "out")
    if not corrupt:
        e = deg["100"]
        print(f"  compare_states.load_degeneracy → j.role={e['j']['role']} j.n_starts={e['j']['n_starts']} meta.starts={e['meta']['starts']}"
              f"  → '⚠ starts=4 — 시험 산출이다' 를 STARTS=24 의 숫자에 붙인다")
        assert e["j"]["role"] == "B" and e["meta"]["starts"] == 4
    else:
        print(f"  compare_states.load_degeneracy → {list(deg)} (깨진 JSON 은 stderr 한 줄 뒤 조용히 빠진다)")
        assert "100" not in deg
    return {"root": str(root), "corrupt": corrupt, "verify_unit": vu, "a_rc": a.returncode, "b_rc": b.returncode}


def f01b_degeneracy_shorter_writer_leaves_garbage_tail():
    """[F01 변형] A 의 JSON 이 B 보다 길면 B 의 write 가 앞부분만 덮어 **깨진 JSON** 이 게시 경로에 남는다 (meta 는 A)."""
    return f01_degeneracy_stdout_fd_survives_rename(pad_a="x" * 300)


# ── F02 · ne_shape._write_csv: 잠금·run_id·sha256 없이 CSV 와 meta 를 따로 쓴다 ─────────────────────────
def f02_ne_shape_write_csv_mixed_bundle() -> dict:
    """[F02] scripts/ne_shape.py:126-181 `_write_csv` 는 (1) 최종 경로를 `open("w")` 로 직접 쓰고 (2) `git_provenance`
    (git 3 회) 를 부른 뒤 (3) meta 를 `write_text` 로 쓴다. 잠금도 run_id 도 sha256 도 없다. A 의 git 이 느린 동안
    (PATH 앞의 git shim — 실제 저장소에서 `git status` 는 수 초) B 가 CSV+meta 를 다 쓰고, A 가 meta 를 덮는다.
    남는 것: CSV = B, meta(consumed_inputs·git_*) = A, 둘 다 rc 0. verify_unit 은 (None, 옛 meta) — 검출 불가."""
    root = fixture_repo(pathlib.Path(tempfile.mkdtemp(prefix="f02_", dir=TMP)) / "repo")
    fx = root.parent
    worker = fx / "ne_writer.py"
    worker.write_text(textwrap.dedent(f'''
        import sys, pathlib
        from types import SimpleNamespace
        sys.path.insert(0, {str(REPO / "scripts")!r}); sys.path.insert(0, {str(REPO)!r})
        import ne_shape
        role, write_dir = sys.argv[1], pathlib.Path(sys.argv[2])
        a = SimpleNamespace(source="GITT", si_source="Li", out_dir="out")
        val = 1.1 if role == "A" else 2.2
        rows = [("100", val, val, 1.0, val, val, 0.4 if role == "A" else 0.5, 0.3, val, val)]
        consumed = {{"100": {{"matrix": {{"file": f"matrix_100_{{role}}.csv", "sha256": role * 8, "row": {{"run_id": "run-" + role}}}}}}}}
        art = ne_shape._write_csv(write_dir, a, rows, {{"100": 1.0}}, 1.0, {{}}, None, consumed)
        print("wrote", art, role)
    '''), encoding="utf-8")
    shim = fx / "shim"; shim.mkdir()
    (shim / "git").write_text(textwrap.dedent('''\
        #!/bin/sh
        # 느린 git: 첫 호출에서 신호를 내고, 놓아줄 때까지 기다린 뒤 진짜 git 을 실행한다
        : > "$FIXTURE/A.git.started"
        while [ ! -e "$FIXTURE/A.git.go" ]; do sleep 0.01; done
        exec /usr/bin/git "$@"
    '''), encoding="utf-8"); (shim / "git").chmod(0o755)
    out = root / "out"; art = out / "ne_shape_GITT_Li.csv"; meta_p = out / "ne_shape_GITT_Li.csv.meta.json"
    env_a = dict(os.environ, PATH=f"{shim}:{os.environ['PATH']}", FIXTURE=str(fx))
    a = subprocess.Popen([PY, str(worker), "A", str(out)], cwd=root, env=env_a, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    wait_for(fx / "A.git.started", a)
    csv_after_a = art.read_text(encoding="utf-8")
    b = subprocess.run([PY, str(worker), "B", str(out)], cwd=root, capture_output=True, text=True, timeout=60)
    assert b.returncode == 0, b.stderr
    csv_after_b = art.read_text(encoding="utf-8"); meta_after_b = json.loads(meta_p.read_text(encoding="utf-8"))
    (fx / "A.git.go").write_text("1")
    ao, ae = a.communicate(timeout=60)
    assert a.returncode == 0, ae
    rows = list(csv.DictReader(art.open(encoding="utf-8"))); meta = json.loads(meta_p.read_text(encoding="utf-8"))
    print(f"  A 가 git 에서 멈춘 시점 CSV 1행 measured_shape_mV={csv.DictReader(csv_after_a.splitlines()).__next__()['measured_shape_mV']}")
    print(f"  B 완료 뒤: CSV measured={csv.DictReader(csv_after_b.splitlines()).__next__()['measured_shape_mV']} meta.consumed.run_id={meta_after_b['consumed_inputs']['100']['matrix']['row']['run_id']}")
    print(f"  A 재개 뒤: CSV measured={rows[0]['measured_shape_mV']} gamma_target={rows[0]['gamma_target']}  meta.consumed.run_id={meta['consumed_inputs']['100']['matrix']['row']['run_id']}"
          f" matrix.sha256={meta['consumed_inputs']['100']['matrix']['sha256']}  rc A={a.returncode} B={b.returncode}")
    vu = provenance.verify_unit(art); print(f"  verify_unit(ne_shape csv) = {vu}")
    assert rows[0]["measured_shape_mV"] == "2.200000" and rows[0]["gamma_target"] == "0.500000"      # CSV = B
    assert meta["consumed_inputs"]["100"]["matrix"]["row"]["run_id"] == "run-A"                       # meta = A
    assert vu[0] is None                                                                               # 검출 불가
    assert "run_id" not in rows[0] and "sha256" not in meta
    return {"root": str(root), "csv_role": "B", "meta_role": "A", "verify_unit": vu}


# ── F03 · fitted_pair_info: 행은 옛 inode 에서, sha256 은 경로를 다시 열어 (새 파일) ────────────────────────
def f03_fitted_pair_info_hashes_a_file_it_did_not_consume() -> dict:
    """[F03] scripts/ne_shape.py:95-104: `csv.DictReader(f.open())` 로 행을 고른 **뒤** `f.read_bytes()` 로 sha256 을
    다시 연다. 그 사이 matrix 가 다시 게시되면(run_states.sh 의 matrix 게시는 os.replace) 행(γ·run_id)은 옛 파일,
    sha256 은 새 파일 → meta.consumed_inputs 가 소비하지 않은 파일의 identity 를 적는다.
    ⚠ 실제 matrix_*.csv 는 ~11 KB 라 창은 sub-ms 다. 여기서는 파싱이 수 초 걸리는 큰 CSV 로 창을 벌려 **기전**을 보인다."""
    fx = pathlib.Path(tempfile.mkdtemp(prefix="f03_", dir=TMP)); out = fx / "out"; out.mkdir()
    mx = out / "matrix_100.csv"
    hdr = ["half_cell", "si", "w_dqdv", "gamma_Si", "ref_gamma_Si", "run_id"]
    with mx.open("w", newline="") as fh:                            # 맞는 행은 맨 끝: 파서가 파일 전체를 읽는다
        w = csv.writer(fh); w.writerow(hdr)
        filler = ["GITT", "Li", "1", "0.4", "0.3", "run-old"]
        for _ in range(1_500_000):
            w.writerow(filler)
        w.writerow(["GITT", "Li", "0", "0.40", "0.30", "run-old"])
    sha_old = sha(mx)
    consumer = fx / "consumer.py"
    consumer.write_text(textwrap.dedent(f'''
        import sys, pathlib, json, time
        sys.path.insert(0, {str(REPO / "scripts")!r}); sys.path.insert(0, {str(REPO)!r})
        import ne_shape
        fx = pathlib.Path(sys.argv[1]); (fx / "C.started").write_text("1")
        t0 = time.monotonic()
        info = ne_shape.fitted_pair_info(fx / "out", "100", "GITT", "Li")
        print(json.dumps({{"info": info, "elapsed": time.monotonic() - t0}}))
    '''), encoding="utf-8")
    c = subprocess.Popen([PY, str(consumer), str(fx)], cwd=fx, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    wait_for(fx / "C.started", c); time.sleep(0.4)                   # 파서가 옛 inode 를 읽는 중
    new = out / "matrix_100.csv.new.part"
    with new.open("w", newline="") as fh:
        w = csv.writer(fh); w.writerow(hdr); w.writerow(["GITT", "Li", "0", "0.55", "0.30", "run-new"])
    os.replace(new, mx); t_pub = time.monotonic(); sha_new = sha(mx)          # 다른 시도의 게시 (rename)
    co, ce = c.communicate(timeout=120)
    assert c.returncode == 0, ce
    res = json.loads(co); info = res["info"]
    print(f"  파싱 {res['elapsed']:.2f}s 중 0.4s 시점에 게시 교체. 결과: gamma_target={info['gamma_target']} row.run_id={info['row']['run_id']}"
          f"  sha256={info['sha256'][:12]}  (옛 {sha_old[:12]} / 새 {sha_new[:12]})")
    assert info["gamma_target"] == 0.40 and info["row"]["run_id"] == "run-old"   # 소비한 것은 옛 파일
    assert info["sha256"] == sha_new and info["sha256"] != sha_old                # 적은 것은 새 파일
    shutil.rmtree(out, ignore_errors=True)                                        # 큰 파일 정리
    return {"consumed_run_id": "run-old", "recorded_sha": "new", "window_s": res["elapsed"]}


# ── F04 · git_provenance 는 meta 를 쓰는 순간의 트리 — 계산이 돈 코드가 아니다 ────────────────────────────
def f04_git_provenance_is_sampled_at_meta_time_not_compute_time() -> dict:
    """[F04] run_states.sh:61 `pv = git_provenance(...)` 는 write_meta 안(계산이 끝난 뒤)에서 한 번. 긴 실행 중에
    사용자가 트리를 정리하면(수정 되돌리기 / 커밋) meta 는 그 **뒤** 상태를 적는다. meta 의 시각은 created_utc
    (meta 작성 시각) 하나뿐 — 계산 시작 시각·시작 시점 트리 상태는 어디에도 없다.
    (i) 계산은 수정된 code.py(value=2) 로 돌았는데 meta: git_dirty=false, git_modified_code=[]
    (ii) 계산은 SHA1 에서 돌았는데 meta.git_commit = 실행 중 만든 SHA2."""
    root = fixture_repo(pathlib.Path(tempfile.mkdtemp(prefix="f04_", dir=TMP)) / "repo"); fx = root.parent
    art = root / "out" / "x.csv"; log = fx / "run.log"
    # 명령: 계산 시점에 본 code.py 내용을 CSV 행에 남기고, 신호 뒤 '계산 중' 대기
    prog = ("import os,sys,pathlib,time; p=pathlib.Path(sys.argv[1]); code=pathlib.Path('code.py').read_text().strip();"
            "p.write_text('a,run_id,code_seen\\n1,'+os.environ['BMS_RUN_ID']+','+code.replace(' ','')+'\\n');"
            "fx=pathlib.Path(os.environ['FIXTURE']); (fx/'P.started').write_text('1');"
            "t=time.monotonic()+60\nwhile not (fx/'P.go').exists():\n    assert time.monotonic()<t; time.sleep(0.01)")
    body = ('\nrun "x" "$1" - "$2" python3 -c "$PROG" "$1" && write_meta "$1" 100 GITT && echo "META_OK" '
            '&& python3 scripts/provenance.py --verify-unit "$1"\n')
    env = dict(os.environ, STARTS="24", SI="Li", BMS_DATA_ROOT="synthetic", OUT=str(root / "out"), FIXTURE=str(fx), PROG=prog)
    cmd = ["bash", "-c", shell_helpers() + body, "f04", str(art), str(log)]
    sha1 = git(root, "rev-parse", "HEAD").strip()
    # (i) 수정된 코드로 계산 시작 → 실행 중 되돌림
    (root / "code.py").write_text("value = 2\n", encoding="utf-8")
    p = subprocess.Popen(cmd, cwd=root, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    wait_for(fx / "P.started", p)
    git(root, "checkout", "--", "code.py")                          # 사용자가 실행 중 트리를 정리
    (fx / "P.go").write_text("1"); po, pe = p.communicate(timeout=60)
    assert p.returncode == 0 and "META_OK" in po, (po, pe)
    row = list(csv.DictReader(art.open()))[0]; meta = json.loads((root / "out" / "x.csv.meta.json").read_text())
    print(f"  (i) 계산이 본 code.py: {row['code_seen']!r}  meta: git_dirty={meta['git_dirty']} git_modified_code={meta['git_modified_code']}"
          f" git_commit={meta['git_commit'][:8]}  시각 필드={[k for k in meta if 'utc' in k or 'time' in k]}")
    assert row["code_seen"] == "value=2" and meta["git_dirty"] is False and meta["git_modified_code"] == []
    r1 = dict(row=row, meta=meta)
    # (ii) 깨끗한 SHA1 에서 계산 시작 → 실행 중 코드 수정+커밋(SHA2)
    for s in ("P.started", "P.go"):
        (fx / s).unlink()
    p = subprocess.Popen(cmd, cwd=root, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    wait_for(fx / "P.started", p)
    (root / "code.py").write_text("value = 3\n", encoding="utf-8"); git(root, "commit", "-qam", "during run")
    sha2 = git(root, "rev-parse", "HEAD").strip()
    (fx / "P.go").write_text("1"); po, pe = p.communicate(timeout=60)
    assert p.returncode == 0 and "META_OK" in po, (po, pe)
    row = list(csv.DictReader(art.open()))[0]; meta = json.loads((root / "out" / "x.csv.meta.json").read_text())
    print(f"  (ii) 계산이 본 code.py: {row['code_seen']!r} (SHA1 {sha1[:8]})  meta: git_commit={meta['git_commit'][:8]} (SHA2 {sha2[:8]}) git_dirty={meta['git_dirty']}")
    assert row["code_seen"] == "value=1" and meta["git_commit"] == sha2 and meta["git_dirty"] is False
    return {"i": r1, "ii": dict(row=row, meta=meta)}


# ── F05 · write_meta OK → --verify-unit 사이의 창: 실패는 조용하고, 가리키는 .log 는 다른 시도의 것 ───────────
def _f05_setup(tag):
    root = fixture_repo(pathlib.Path(tempfile.mkdtemp(prefix=f"f05{tag}_", dir=TMP)) / "repo"); fx = root.parent
    ppath = fake_verify_pkg(fx)
    # 멈춤점 (test_r5_04 와 같은 기법: shell 의 python3 를 함수로 덮는다):
    #   ROLE == PAUSE_VERIFY_ROLE → `python3 scripts/provenance.py --verify-unit` 직전 (<ROLE>.verify.ready / .go)
    #   ROLE == PAUSE_META_ROLE   → write_meta 의 heredoc `python3 -` 직전            (<ROLE>.meta.ready / .go)
    override = textwrap.dedent('''
        python3 () {
          if [ "$1" = "scripts/provenance.py" ] && [ "$2" = "--verify-unit" ] && [ "$ROLE" = "${PAUSE_VERIFY_ROLE:-}" ]; then
            : > "$FIXTURE/$ROLE.verify.ready"
            while [ ! -e "$FIXTURE/$ROLE.verify.go" ]; do sleep 0.01; done
          fi
          if [ "$1" = "-" ] && [ "$ROLE" = "${PAUSE_META_ROLE:-}" ]; then
            : > "$FIXTURE/$ROLE.meta.ready"
            while [ ! -e "$FIXTURE/$ROLE.meta.go" ]; do sleep 0.01; done
          fi
          "$REAL_PY" "$@"
        }
    ''')
    body = "st=100\nSRC=GITT\nfail=0\nSTATES=100\n" + matrix_block() + summary_tail() + 'echo "FAIL_COUNT=$fail"\nexit $fail\n'
    cmd = ["bash", "-c", override + shell_helpers() + "\n" + body, "f05"]

    def env(role, **extra):
        return dict(os.environ, STATES="100", STARTS="24", SI="Li", OUT=str(root / "out"), BMS_DATA_ROOT="synthetic",
                    PYTHONPATH=str(ppath), ROLE=role, FIXTURE=str(fx), REAL_PY=PY, **extra)
    return root, fx, cmd, env


def _f05_disk(root):
    art = root / "out" / "matrix_100.csv"; log = root / "out" / "matrix_100.csv.log"
    rows = list(csv.DictReader(art.open())); meta = json.loads(art.with_name(art.name + ".meta.json").read_text())
    return rows, meta, provenance.verify_unit(art), log.read_text().strip()


def f05a_verify_unit_confirms_the_other_attempts_bundle() -> dict:
    """[F05a] run_states.sh:192-194 `write_meta … && python3 scripts/provenance.py --verify-unit …`: verify_unit
    (provenance.py:118) 은 "디스크의 meta ↔ 디스크의 bytes" 만 본다 — **이 시도의 run id 는 안 받는다**. A 의
    write_meta 성공 뒤 --verify-unit 전에 B 가 CSV+meta 를 다 게시하면 A 의 verify-unit 은 B/B 를 보고 통과 →
    A 의 wrapper: "OK [run_id A]" + "전부 통과", rc 0. 디스크에 A 의 bytes 는 없다. (R5-04 의 A 는 거부됐다 —
    이번엔 A 가 **성공을 보고**한다.)"""
    root, fx, cmd, env = _f05_setup("a")
    a = subprocess.Popen(cmd, cwd=root, env=env("A", PAUSE_VERIFY_ROLE="A"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    wait_for(fx / "A.started", a); (fx / "A.go").write_text("1")
    wait_for(fx / "A.verify.ready", a)                               # A: run OK · write_meta OK · verify-unit 직전
    a_rid = json.loads((root / "out" / "matrix_100.csv.meta.json").read_text())["run_id"]
    (fx / "B.go").write_text("1")
    b = subprocess.run(cmd, cwd=root, env=env("B"), capture_output=True, text=True, timeout=60)
    assert b.returncode == 0 and "FAIL_COUNT=0" in b.stdout, (b.stdout, b.stderr)
    (fx / "A.verify.go").write_text("1")
    ao, ae = a.communicate(timeout=60)
    rows, meta, vu, log = _f05_disk(root); a_lines = ae.strip().splitlines()
    print(f"  A rc={a.returncode} stdout={[l for l in ao.splitlines() if 'FAIL_COUNT' in l]}")
    print("  A stderr:\n    " + "\n    ".join(a_lines))
    print(f"  디스크: CSV role={rows[0]['role']} run_id={rows[0]['run_id'][:8]} meta.run_id={meta['run_id'][:8]} verify_unit={vu}  (A 의 id 는 {a_rid[:8]})")
    assert a.returncode == 0 and "FAIL_COUNT=0" in ao and "전부 통과" in ae and f"[run_id {a_rid}]" in ae
    assert rows[0]["role"] == "B" and meta["run_id"] == rows[0]["run_id"] != a_rid and vu == (True, "일치")
    return {"a_rc": 0, "a_reports": "전부 통과", "disk": "B/B"}


def f05b_verify_unit_failure_is_silent_and_log_pointer_is_anothers() -> dict:
    """[F05b] 같은 창, B 가 CSV 만 게시하고 write_meta 직전에 있을 때 A 의 --verify-unit 이 돌면 실패한다(맞다).
    그러나 (1) 이유(`why`)는 `>/dev/null` 로 버려져 A 의 stderr 에 한 줄도 없다, (2) 요약 "실패 1 건 — 위의 .log 를
    볼 것" 이 가리키는 matrix_100.csv.log 는 B 가 `> "$log"` 로 덮어쓴 **B 의** 로그다 — A 의 로그는 없다.
    디스크는 B 가 마치면 B/B 로 온전하다. 결과는 안 섞이고 진단만 잃는다."""
    root, fx, cmd, env = _f05_setup("b")
    a = subprocess.Popen(cmd, cwd=root, env=env("A", PAUSE_VERIFY_ROLE="A"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    wait_for(fx / "A.started", a); (fx / "A.go").write_text("1")
    wait_for(fx / "A.verify.ready", a)                               # A: write_meta(A) 끝, verify-unit 직전
    (fx / "B.go").write_text("1")
    b = subprocess.Popen(cmd, cwd=root, env=env("B", PAUSE_META_ROLE="B"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    wait_for(fx / "B.meta.ready", b)                                 # B: CSV(B) 게시 끝, write_meta 직전
    (fx / "A.verify.go").write_text("1")
    ao, ae = a.communicate(timeout=60)
    a_lines = ae.strip().splitlines(); log_seen_by_a = (root / "out" / "matrix_100.csv.log").read_text().strip()
    (fx / "B.meta.go").write_text("1")
    bo, be = b.communicate(timeout=60)
    rows, meta, vu, log = _f05_disk(root)
    print(f"  A rc={a.returncode} stdout={[l for l in ao.splitlines() if 'FAIL_COUNT' in l]}")
    print("  A stderr:\n    " + "\n    ".join(a_lines))
    print(f"  A 가 가리킨 .log: {log_seen_by_a!r}")
    print(f"  B rc={b.returncode}; 디스크: CSV role={rows[0]['role']} meta.run_id==CSV: {meta['run_id'] == rows[0]['run_id']} verify_unit={vu}")
    assert a.returncode == 1 and "FAIL_COUNT=1" in ao and "실패 1 건" in ae
    assert not any(("verify" in l or "묶음" in l or "sha256" in l or "meta" in l) for l in a_lines)   # 이유 없음
    assert rows[0]["run_id"] in log_seen_by_a                                                          # .log 는 B 의 것
    assert b.returncode == 0 and rows[0]["role"] == "B" and vu == (True, "일치")
    return {"a_rc": 1, "reason_printed": False, "log_is": "B", "disk": "B/B"}


# ── F07 · 소비자는 verify_unit 을 부르지 않는다 — 게시와 meta 사이에서 죽은 시도의 섞인 묶음을 그대로 읽는다 ─────
def f07_readers_consume_a_mismatched_bundle_without_checking() -> dict:
    """[F07] verify_unit 은 run_states.sh 의 게시 직후 한 번만 돈다. compare_states.py:57-61 은 meta 를 `starts` 만
    보려고 읽고 run_id·sha256 은 안 본다; ne_shape.fitted_pair_info 도 안 본다. 게시(잠금 안 os.replace)와 write_meta
    사이에서 시도가 죽으면(kill -9 · 전원 · Ctrl-C 가 git status 중에) CSV = B, meta = 이전 A 가 남고, 그 뒤 어떤
    실행도 그 불일치를 다시 검사하지 않는다 — Codex R5-04 최소 조건의 reader 절("reader 도 불일치를 성공으로
    소비하지 않아야")은 구현되지 않았다."""
    root, fx, cmd, env = _f05_setup("7")
    a = subprocess.Popen(cmd, cwd=root, env=env("A"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    wait_for(fx / "A.started", a); (fx / "A.go").write_text("1"); ao, ae = a.communicate(timeout=60)
    assert a.returncode == 0, ae                                     # A/A 온전한 묶음
    (fx / "B.go").write_text("1")
    b = subprocess.Popen(cmd, cwd=root, env=env("B", PAUSE_META_ROLE="B"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    wait_for(fx / "B.meta.ready", b)                                 # B: CSV(B) 게시 끝 · write_meta 직전
    b.kill(); b.communicate(timeout=30)                              # 여기서 죽는다
    rows, meta, vu, _ = _f05_disk(root)
    mx = compare_states.load_matrix_axis(root / "out")["100"]
    cs = subprocess.run([PY, str(REPO / "scripts" / "compare_states.py"), str(root / "out")], capture_output=True, text=True)
    b_line = [l for l in cs.stdout.splitlines() if l.strip().startswith("100")]
    print(f"  디스크: CSV role={rows[0]['role']} run_id={rows[0]['run_id'][:8]}  meta.run_id={meta['run_id'][:8]}  verify_unit={vu}")
    print(f"  compare_states.load_matrix_axis['100'] → file={mx['file']} LAM_PE 폭={mx['per']['GITT']['LAM_PE']} (B 의 값 2.0; A 는 1.0)")
    print(f"  compare_states.py stdout 의 100 행: {b_line}  / 경고·불일치 언급: {[l for l in cs.stdout.splitlines() if 'run_id' in l or 'sha' in l or '불일치' in l]}")
    assert rows[0]["role"] == "B" and meta["run_id"] != rows[0]["run_id"] and vu[0] is False
    assert mx["per"]["GITT"]["LAM_PE"] == 2.0 and b_line and cs.returncode == 0
    assert not any(("run_id" in l or "sha" in l or "불일치" in l) for l in cs.stdout.splitlines())
    return {"disk": "CSV=B/meta=A", "compare_states_rc": cs.returncode, "warned": False}


# ── F08 · run id 는 산출물 안의 공개 값 — 파일에서 읽어 되쓰는 producer 는 모든 검사를 통과한다 ─────────────────
def f08_run_id_copied_from_the_published_file_passes_every_check() -> dict:
    """[F08] 소유 증거는 "파일 안에 이 시도의 id 가 있다"(check_run_id) 하나다. id 는 게시된 CSV/JSON 의 열/필드로
    누구나 읽을 수 있다. A 가 CSV(A) 를 게시하고 write_meta 전에(git status 중) 다른 producer X 가 디스크의 run_id
    를 그대로 복사해 자기 숫자로 게시하면: A 의 잠금 안 재확인 통과 → meta(A) 의 sha256 = X 의 bytes → --verify-unit
    True → "전부 통과". 묶음 'A' 의 내용은 X 다. 우연 충돌은 아니고 버그 있는/의도적인 producer 의 경우다(사소) —
    R4-06·R5-08 의 id 검사가 소유 증명이 아니라 '섞임 감지' 라는 한계를 실측으로 못 박는다."""
    root, fx, cmd, env = _f05_setup("8")
    a = subprocess.Popen(cmd, cwd=root, env=env("A", PAUSE_META_ROLE="A"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    wait_for(fx / "A.started", a); (fx / "A.go").write_text("1")
    wait_for(fx / "A.meta.ready", a)                                 # A: CSV(A) 게시·run OK · write_meta 직전
    art = root / "out" / "matrix_100.csv"
    rows_a = list(csv.DictReader(art.open())); rid = rows_a[0]["run_id"]
    x = subprocess.run([PY, "-c", textwrap.dedent(f'''
        import csv, os, sys, fcntl
        art = {str(art)!r}; rows = list(csv.DictReader(open(art)))          # 디스크의 파일에서 id 를 읽는다
        for r in rows: r.update(role="X", LAM_PE_pct=str(float(r["LAM_PE_pct"]) + 50))
        tmp = art + ".x.part"
        with open(tmp, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
        with open(art + ".lock", "a+") as lk:
            fcntl.flock(lk, fcntl.LOCK_EX); os.replace(tmp, art)
        print("X published with run_id", rows[0]["run_id"])
    ''')], capture_output=True, text=True); assert x.returncode == 0, x.stderr
    (fx / "A.meta.go").write_text("1"); ao, ae = a.communicate(timeout=60)
    rows, meta, vu, _ = _f05_disk(root)
    print(f"  A 의 id={rid[:8]}; X: {x.stdout.strip()}")
    print(f"  A rc={a.returncode} stderr 마지막줄={ae.strip().splitlines()[-1]!r}")
    print(f"  디스크: CSV role={rows[0]['role']} LAM_PE={rows[0]['LAM_PE_pct']} run_id={rows[0]['run_id'][:8]}  meta.run_id={meta['run_id'][:8]} sha256 일치={meta['sha256'] == sha(art)}  verify_unit={vu}")
    assert a.returncode == 0 and "전부 통과" in ae and rows[0]["role"] == "X" and meta["run_id"] == rid and vu == (True, "일치")
    return {"bundle_labeled": "A", "bytes_from": "X", "verify_unit": vu}


# ── F06 · 잠금 파일의 수명: untracked 로 남고, 지워지면 배타가 사라진다 ────────────────────────────────────
def f06_lock_file_is_untracked_and_deleting_it_breaks_exclusion() -> dict:
    """[F06] `<산출>.lock` 은 `.gitignore` 에 없다(`out/.*.part` 만) → 실행 뒤 `git status` 에 `??` 로 남고
    `git clean -fd`(-x 없이) 의 대상이다. 잠금은 inode 에 걸리므로 보유 중 파일이 지워지면 다음 시도는 **새 inode**
    를 잠가 즉시 성공한다 — 같은 경로, 잠금 둘. 같은 이유로 `atomic_write_csv`·write_meta 의 임시 이름
    (`matrix_100.csv.XXXX.part`, `…meta.XXXX.part`) 도 ignore 밖이라 죽은 시도의 잔해가 `??` 로 남는다."""
    root = fixture_repo(pathlib.Path(tempfile.mkdtemp(prefix="f06_", dir=TMP)) / "repo"); fx = root.parent
    art = root / "out" / "matrix_100.csv"; lock = pathlib.Path(str(art) + ".lock")
    shutil.copyfile(REPO / ".gitignore", root / ".gitignore")       # 원본 규칙 그대로
    holder = subprocess.Popen([PY, "-c", textwrap.dedent(f'''
        import sys, pathlib, time
        sys.path.insert(0, {str(REPO)!r})
        from bms_balancing.verify import publish_lock
        fx = pathlib.Path({str(fx)!r})
        with publish_lock({str(art)!r}):
            (fx / "H.locked").write_text("1")
            while not (fx / "H.go").exists(): time.sleep(0.01)
    ''')], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    wait_for(fx / "H.locked", holder)
    before = subprocess.run(["flock", "-n", str(lock), "true"]).returncode
    (root / "out" / "matrix_100.csv.ab12cd.part").write_text("half\n"); (root / "out" / "matrix_100.csv.meta.ab12cd.part").write_text("{")
    status = subprocess.run(["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True).stdout
    clean = subprocess.run(["git", "clean", "-fdn", "out"], cwd=root, capture_output=True, text=True).stdout
    ignored = subprocess.run(["git", "check-ignore", "-v", str(lock)], cwd=root, capture_output=True, text=True)
    print(f"  보유 중 flock -n rc={before} (1 = 잠겨 있다)")
    print(f"  git status --porcelain:\n    " + status.strip().replace("\n", "\n    "))
    print(f"  git clean -fdn out:\n    " + clean.strip().replace("\n", "\n    "))
    print(f"  check-ignore(lock) rc={ignored.returncode} → {'ignore 규칙 없음' if ignored.returncode else ignored.stdout.strip()}")
    lock.unlink()                                                     # git clean -fd 가 하는 일
    after = subprocess.run(["flock", "-n", str(lock), "true"]).returncode
    print(f"  lock 파일 삭제 뒤 (보유자는 아직 잠금 중) flock -n rc={after} (0 = 즉시 획득 — 배타 없음)")
    (fx / "H.go").write_text("1"); holder.communicate(timeout=30)
    assert before == 1 and after == 0 and "?? out/matrix_100.csv.lock" in status and "out/matrix_100.csv.lock" in clean
    assert ignored.returncode != 0 and "matrix_100.csv.ab12cd.part" in status and "meta.ab12cd.part" in status
    return {"flock_before": before, "flock_after_delete": after}


# ── 시도했지만 발견이 아닌 것 (N) ─────────────────────────────────────────────────────────────────────
def n01_flock_cli_and_fcntl_flock_are_the_same_lock() -> dict:
    """[N01] util-linux `flock`(run_states.sh:181) 과 Python `fcntl.flock`(verify.publish_lock · write_meta) 은 같은
    flock(2) — 두 process 로 양방향 확인. 발견 아님."""
    fx = pathlib.Path(tempfile.mkdtemp(prefix="n01_", dir=TMP)); lock = fx / "x.csv.lock"
    holder = subprocess.Popen([PY, "-c", textwrap.dedent(f'''
        import sys, pathlib, time
        sys.path.insert(0, {str(REPO)!r})
        from bms_balancing.verify import publish_lock
        fx = pathlib.Path({str(fx)!r})
        with publish_lock(str(fx / "x.csv")):
            (fx / "H.locked").write_text("1")
            while not (fx / "H.go").exists(): time.sleep(0.01)
    ''')], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    wait_for(fx / "H.locked", holder)
    rc1 = subprocess.run(["flock", "-n", str(lock), "true"]).returncode
    (fx / "H.go").write_text("1"); holder.communicate(timeout=30)
    rc2 = subprocess.run(["flock", "-n", str(lock), "true"]).returncode
    cli = subprocess.Popen(["flock", str(lock), "sh", "-c", f": > {fx}/C.locked; while [ ! -e {fx}/C.go ]; do sleep 0.01; done"])
    wait_for(fx / "C.locked", cli)
    r = subprocess.run([PY, "-c", f"import fcntl; fh=open({str(lock)!r},'a+')\n"
                        "try:\n fcntl.flock(fh, fcntl.LOCK_EX|fcntl.LOCK_NB); print('ACQUIRED')\n"
                        "except BlockingIOError: print('BLOCKED')"], capture_output=True, text=True)
    (fx / "C.go").write_text("1"); cli.wait(timeout=30)
    print(f"  python 보유 중 flock -n rc={rc1}; 해제 뒤 rc={rc2}; flock CLI 보유 중 python LOCK_NB → {r.stdout.strip()}")
    assert rc1 == 1 and rc2 == 0 and r.stdout.strip() == "BLOCKED"
    return {"cli_vs_py": "same lock"}


def n02_lock_and_part_files_do_not_pollute_consumer_globs() -> dict:
    """[N02] `.lock`·`.part`·`.meta.json` 이 compare_states(`degeneracy_*.json`, `matrix_*.csv`)·ne_shape
    (`matrix_{state}*.csv`) 의 glob 에 걸리는가 — 안 걸린다. 발견 아님."""
    import ne_shape
    fx = pathlib.Path(tempfile.mkdtemp(prefix="n02_", dir=TMP)); out = fx / "out"; out.mkdir()
    j = {"run_id": "r", "LAM_PE_percent": {"span": 1, "min": 0, "max": 1}, "LAM_NE_percent": {"span": 2, "min": 0, "max": 2},
         "LLI_percent": {"span": 0.5, "min": 0, "max": 0.5}, "best_modes_percent": {"LAM_PE": 0, "LAM_NE": 0, "LLI": 0}}
    (out / "degeneracy_100_Li.json").write_text(json.dumps(j)); (out / "degeneracy_100_Li.json.meta.json").write_text(json.dumps({"starts": 24}))
    (out / "matrix_100.csv").write_text("half_cell,si,w_dqdv,gamma_Si,ref_gamma_Si,run_id,LAM_PE_pct,LAM_NE_pct,LLI_pct,bounds,ref_bounds\nGITT,Li,0,0.4,0.3,r,1,2,3,-,-\n")
    for n in ("degeneracy_100_Li.json.lock", "matrix_100.csv.lock", "matrix_100.csv.ab12.part", "matrix_100.csv.meta.ab12.part",
              ".degeneracy_100_Li.part", "degeneracy_100_Li.json.meta.ab12.part"):
        (out / n).write_text("{" if "json" in n else "x,y\n1,2\n")
    deg = compare_states.load_degeneracy(out); mx = compare_states.load_matrix_axis(out)
    fp = ne_shape.fitted_pair_info(out, "100", "GITT", "Li")
    print(f"  load_degeneracy → {[e['file'] for e in deg.values()]}; load_matrix_axis → {[e['file'] for e in mx.values()]}; fitted_pair_info.file → {pathlib.Path(fp['file']).name}")
    assert [e["file"] for e in deg.values()] == ["degeneracy_100_Li.json"] and [e["file"] for e in mx.values()] == ["matrix_100.csv"]
    assert pathlib.Path(fp["file"]).name == "matrix_100.csv"
    return {"pollution": False}


def n03_run_helper_overrides_an_exported_BMS_RUN_ID() -> dict:
    """[N03] 사용자가 shell 에 `export BMS_RUN_ID=…` 를 남겨 둔 채 run_states.sh 를 돌려도 `run` 은 명령마다 새
    id 를 **앞에** 붙여 준다(run_states.sh:129/131) — 물려받은 id 로 게시되지 않는다. 발견 아님."""
    root = fixture_repo(pathlib.Path(tempfile.mkdtemp(prefix="n03_", dir=TMP)) / "repo"); fx = root.parent
    art = root / "out" / "x.csv"
    body = '\nrun "x" "$1" - "$2" python3 -c "import os,sys,pathlib; pathlib.Path(sys.argv[1]).write_text(\'a,run_id\\n1,\'+os.environ[\'BMS_RUN_ID\']+\'\\n\')" "$1" && echo OK_$LAST_RUN_ID\n'
    env = dict(os.environ, STARTS="24", SI="Li", BMS_DATA_ROOT="synthetic", OUT=str(root / "out"), BMS_RUN_ID="stale-exported-id")
    r = subprocess.run(["bash", "-c", shell_helpers() + body, "n03", str(art), str(fx / "l")], cwd=root, env=env, capture_output=True, text=True)
    rid = art.read_text().strip().splitlines()[-1].split(",")[-1]
    print(f"  export BMS_RUN_ID=stale-exported-id 상태에서 산출의 run_id={rid[:8]}… ({'새 id' if rid != 'stale-exported-id' else '물려받음'}) rc={r.returncode}")
    assert r.returncode == 0 and rid != "stale-exported-id" and f"OK_{rid}" in r.stdout
    return {"inherited": False}


ALL = [f01_degeneracy_stdout_fd_survives_rename, f01b_degeneracy_shorter_writer_leaves_garbage_tail,
       f02_ne_shape_write_csv_mixed_bundle, f03_fitted_pair_info_hashes_a_file_it_did_not_consume,
       f04_git_provenance_is_sampled_at_meta_time_not_compute_time, f05a_verify_unit_confirms_the_other_attempts_bundle,
       f05b_verify_unit_failure_is_silent_and_log_pointer_is_anothers, f06_lock_file_is_untracked_and_deleting_it_breaks_exclusion,
       f07_readers_consume_a_mismatched_bundle_without_checking, f08_run_id_copied_from_the_published_file_passes_every_check,
       n01_flock_cli_and_fcntl_flock_are_the_same_lock, n02_lock_and_part_files_do_not_pollute_consumer_globs,
       n03_run_helper_overrides_an_exported_BMS_RUN_ID]

if __name__ == "__main__":
    want = sys.argv[1:]
    results = {}
    for fn in ALL:
        if want and not any(fn.__name__.startswith(w) for w in want):
            continue
        banner(fn.__name__, fn.__doc__.strip().splitlines()[0])
        try:
            results[fn.__name__] = ("REPRODUCED" if fn.__name__.startswith("f") else "NO-FINDING", fn())
        except AssertionError as e:
            results[fn.__name__] = ("NOT-REPRODUCED", repr(e))
            print(f"  !! assert 실패 (재현 안 됨): {e!r}")
    print("\n" + "#" * 100)
    for k, (st, _) in results.items():
        print(f"{st:15} {k}")
    sys.exit(0 if all(st != "NOT-REPRODUCED" for st, _ in results.values()) else 1)
