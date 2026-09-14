#!/usr/bin/env python3
"""R6 자체 리뷰 — sig-완전성 · archive-이식성 렌즈. 대상 1049894, 범위 bms-balancing/.

발견마다 함수 하나. **잘못된 결과가 재현되면 assert 가 통과**한다 (고치면 실패해야 정상).
tracked 파일은 건드리지 않는다 — 모든 산출은 임시 디렉터리. 실행:

    python3 repro_sig_port.py                # 전부
    python3 repro_sig_port.py f3 f5          # 일부
    OLD_VENV_PYTHON=/path/venv/bin/python python3 repro_sig_port.py f3   # scipy 교차 버전 수치까지

전제: bms-balancing 의존성(numpy·scipy·pandas·openpyxl·pytest), git, bash, util-linux flock.
"""
from __future__ import annotations
import csv, errno, json, os, pathlib, re, shutil, subprocess, sys, tempfile

REPO = pathlib.Path(__file__).resolve()
while not (REPO / ".git").exists():                      # 저장소 루트 (worktree 도 .git 파일이 있다)
    if REPO.parent == REPO:
        REPO = pathlib.Path("/home/user/Yonghoon-DEM-DFT"); break
    REPO = REPO.parent
BMS = REPO / "bms-balancing"
TARGET, PREV_GITATTR = "1049894", "274f1f8"
sys.path.insert(0, str(BMS))
PY = sys.executable
TMP = pathlib.Path(tempfile.mkdtemp(prefix="sig_port_"))


def sh(cmd, cwd=None, env=None, **kw):
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", **kw)


def synth_root(name: str) -> pathlib.Path:
    """합성 xlsx 트리 (matlab/tests/gen_synth_xlsx.py) — 공백·한글 경로 그대로."""
    root = TMP / "data" / name
    if not (root / "data" / "literature").is_dir():
        r = sh([PY, str(BMS / "matlab/tests/gen_synth_xlsx.py"), str(root)]); assert r.returncode == 0, r.stderr
    return root


def eval_audit_line(root, *extra, env=None) -> tuple[int, str, str]:
    r = sh([PY, "-m", "bms_balancing.verify", "eval", "--data-root", str(root), "--state", "pristine", *extra],
           cwd=BMS, env=env)
    line = next((l for l in r.stdout.splitlines() if l.startswith("# scale_audit,")), "")
    return r.returncode, line, r.stderr


# ── F1. 감사 줄의 root= 식별자: 공백이면 줄의 \S+ 규약이 깨지고, basename 이라 루트가 구별되지 않는다 ─────
def f1_root_label_not_an_identifier():
    space = synth_root("가형 관련/degradation mode")             # 사용자 실제 루트의 basename
    a, b = synth_root("cells/c168"), synth_root("cells_v2/c168")   # 다른 루트, 같은 basename
    head = re.compile(r"state=(\S+) source=(\S+) si=(\S+) seed=(\d+) n=(\d+)")   # test_u13 의 정규식 그대로
    rootpat = re.compile(r"root=(\S+)")                                          # 같은 줄의 다른 필드와 같은 규약
    rc, ln, _ = eval_audit_line(space); assert rc == 0 and ln, ln
    assert head.search(ln), "test_u13 head 는 여전히 잡힌다 (root 를 안 보기 때문)"
    assert rootpat.search(ln).group(1) == "degradation", ln          # 'degradation mode' 가 잘린다
    assert " root=degradation mode state=" in " " + ln[len("# scale_audit,"):], ln
    la, lb = (rootpat.search(eval_audit_line(r)[1]).group(1) for r in (a, b))
    assert la == lb == "c168", (la, lb)                               # 두 루트가 같은 식별자
    r = sh([PY, "-m", "bms_balancing.verify", "eval", "--data-root", ".", "--state", "pristine"],
           cwd=space, env={**os.environ, "PYTHONPATH": str(BMS)})
    ln_dot = next(l for l in r.stdout.splitlines() if l.startswith("# scale_audit,"))
    assert "root=. state=" in ln_dot, ln_dot                          # 상대 루트면 '.'
    # 회귀 테스트 어디에도 감사 줄의 root= 를 읽는 곳이 없다 (ns(root=…) 같은 kwargs 는 무관)
    tsrc = (BMS / "tests/test_review_findings.py").read_text(encoding="utf-8").splitlines()
    assert not [l for l in tsrc if "root=" in l and ("scale_audit" in l or "re.compile" in l or "\\S" in l)]
    return "root=degradation mode → \\S+ 로 'degradation'; c168 두 루트 동일 라벨; --data-root . → 'root=.'; 테스트는 root= 를 안 읽음"


# ── F2. U13 사본은 한 루트 4 줄을 4 번 복제하고 순서를 섞어도 test_u13 을 통과한다 ─────────────────────
def f2_u13_copy_cannot_evidence_four_roots():
    import random, importlib
    fake_root = TMP / "f2_root"; (fake_root / "out").mkdir(parents=True, exist_ok=True)
    shutil.copy(BMS / "FINDINGS.md", fake_root / "FINDINGS.md")
    lines = (BMS / "out/scale_audit_eval_u13.txt").read_text(encoding="utf-8").splitlines()
    head = [l for l in lines if not l.startswith("# scale_audit,")]
    aud = [l for l in lines if l.startswith("# scale_audit,")]
    forged = aud[0:4] * 4 + aud[16:18]                                # 루트 하나 × 4 + Kunz + step_005C
    random.Random(1).shuffle(forged)                                  # "보고 순서" 도 없앤다
    assert len(set(forged)) == 6
    (fake_root / "out/scale_audit_eval_u13.txt").write_text("\n".join(head + forged) + "\n", encoding="utf-8")
    sys.path.insert(0, str(BMS / "tests")); T = importlib.import_module("test_review_findings")
    old = T.ROOT; T.ROOT = fake_root
    try:
        T.test_u13_scale_audit_transcript_meets_the_equivalence_condition_and_covers_the_recompare_configs()
    finally:
        T.ROOT = old
    return "6 개 distinct 줄로 만든 18 줄 위조 사본이 test_u13 통과 — §1-13 '네 루트' 는 사본으로 검증 불가"


# ── F3. 서명이 라이브러리 버전을 안 잡는다 — scipy 1.11.4 ↔ 1.17.1 에서 최적점이 다르다 ─────────────────
def f3_library_versions_not_in_signature():
    req = (BMS / "requirements.txt").read_text(encoding="utf-8")
    assert all(op not in req for op in ("==", "<=", "<", "~=")), "requirements 가 상한/고정을 갖게 됐다"
    meta_src = (BMS / "scripts/run_states.sh").read_text(encoding="utf-8")
    for k in ("numpy", "scipy", "python_version", "platform"):
        assert f'"{k}' not in meta_src, k                            # write_meta 의 키에 없다
    root = synth_root("가형 관련/degradation mode")
    r = sh([PY, "-m", "bms_balancing.verify", "degeneracy", "--data-root", str(root), "--state", "100",
            "--starts", "1", "--grid", "3", "--samples", "2"], cwd=BMS)
    d = json.loads(r.stdout); assert r.returncode == 0
    assert not [k for k in d if any(s in k.lower() for s in ("numpy", "scipy", "python", "version"))], list(d)
    note = "meta/JSON 에 numpy·scipy·python 버전 없음, requirements 는 하한만"
    old = os.environ.get("OLD_VENV_PYTHON")
    if old:
        code = f"""
import sys, pathlib, numpy as np, scipy; sys.path.insert(0, {str(BMS)!r})
from bms_balancing import verify; from bms_balancing.model import LB5, UB5; from scipy.optimize import minimize
o = verify.build(pathlib.Path({str(root)!r}), "GITT", "100", "Li", w_dqdv=0.0, scale_seed=0)
r = minimize(o, LB5 + 0.5*(UB5-LB5), method="L-BFGS-B", bounds=list(zip(LB5, UB5)), options={{"maxiter": 400, "ftol": 1e-12}})
print(scipy.__version__, float(o.scales["dqdv"]).hex(), r.nit, repr(float(r.fun)), [repr(float(x)) for x in r.x])"""
        a, b = (sh([p, "-c", code]).stdout.split() for p in (PY, old))
        assert a[0] != b[0] and (a[1] != b[1] or a[2:] != b[2:]), (a, b)
        note += f"; 실측 scipy {a[0]} vs {b[0]}: dqdv scale {a[1]} vs {b[1]}, L-BFGS-B nit {a[2]} vs {b[2]}, x {a[4:]} vs {b[4:]}"
    return note


# ── F4. verify.py 가 소비한 풀셀 워크북의 identity 가 산출·meta 에 없다 — 이름순 첫 xlsx 가 조용히 바뀐다 ───
def f4_fullcell_workbook_identity_unrecorded():
    from bms_balancing import data as D, verify
    import pandas as pd
    root = synth_root("cells_v2/c168"); d = root / "data/full_cell/large_cell_033C"
    o1 = verify.build(root, "GITT", "100", "Li", scale_seed=0)
    copy = d / "fullcell_states - 복사본.xlsx"                       # Windows 탐색기 복사 이름: ' ' < '.'
    shutil.copy(d / "fullcell_states.xlsx", copy)
    try:
        assert D.full_cell_workbook(root).name == copy.name
        df = pd.read_excel(d / "fullcell_states.xlsx", header=None)
        df.iloc[2:, 3] = df.iloc[2:, 3].astype(float) * 1.01          # 다른 셀의 워크북이라 치자
        df.to_excel(copy, header=False, index=False)
        o2 = verify.build(root, "GITT", "100", "Li", scale_seed=0)
    finally:
        copy.unlink()
    assert o1.scales["pocv"] != o2.scales["pocv"], (o1.scales, o2.scales)
    ws = (BMS / "scripts/run_states.sh").read_text(encoding="utf-8")
    assert "full_cell" not in ws and "workbook" not in ws              # meta 키에 없다
    vs = (BMS / "bms_balancing/verify.py").read_text(encoding="utf-8")
    assert "full_cell_workbook" not in vs and "sha256" not in vs        # 산출 JSON/행에도 없다
    assert "full_cell" not in (BMS / "scripts/ne_shape.py").read_text(encoding="utf-8")   # R5-05 는 ne_shape 만
    return f"복사본 xlsx 가 이름순 첫 것으로 선택됨; scale pocv {float(o1.scales['pocv']).hex()} → {float(o2.scales['pocv']).hex()}; JSON·meta 에 워크북 이름/sha256 없음"


# ── F5. 인자 전체의 서명이 없다 — 같은 run_id 로 다른 목적함수(profile_scale)·다른 samples 를 돌려도 구별 불가 ──
def f5_args_not_in_artifact_signature():
    root = synth_root("가형 관련/degradation mode"); out = TMP / "f5"; out.mkdir(exist_ok=True)
    rows = {}
    for m in ("global", "per-gamma"):
        r = sh([PY, "-m", "bms_balancing.verify", "profile", "--data-root", str(root), "--state", "100", "--starts", "1",
                "--grid", "5", "--seed", "0", "--profile-scale", m, "--run-id", "RID-SAME", "--out", str(out / f"p_{m}.csv")], cwd=BMS)
        assert r.returncode == 0, r.stderr[-500:]
        assert '"profile_scale": "%s"' % m in r.stdout                  # stdout SUMMARY 에만 있다
        rows[m] = list(csv.DictReader((out / f"p_{m}.csv").open(encoding="utf-8")))
    assert list(rows["global"][0]) == list(rows["per-gamma"][0])       # 스키마 동일
    assert rows["global"][0]["run_id"] == rows["per-gamma"][0]["run_id"] == "RID-SAME"
    assert rows["global"][0]["obj"] != rows["per-gamma"][0]["obj"]      # 숫자는 다르다
    assert not {k for k in rows["global"][0] if k in ("profile_scale", "seed", "starts", "w_dqdv", "si", "half_cell")}
    js = {}
    for n in ("4", "40"):
        r = sh([PY, "-m", "bms_balancing.verify", "degeneracy", "--data-root", str(root), "--state", "100", "--starts", "1",
                "--grid", "3", "--samples", n, "--seed", "0", "--run-id", "RID-SAME"], cwd=BMS)
        assert r.returncode == 0, r.stderr[-500:]; js[n] = json.loads(r.stdout)
    cfg = ("state", "si_source", "half_cell", "w_dqdv", "tol_percent_of_best", "n_starts", "seed", "run_id")
    assert all(js["4"][k] == js["40"][k] for k in cfg)
    assert not [k for k in js["4"] if "sample" in k]                   # samples 는 어디에도 없다
    assert js["4"]["n_accepted"] != js["40"]["n_accepted"]
    # matrix 행: scale_seed·n_scale_samples 는 있지만 starts 는 없다 (in-process, Si 하나만)
    from types import SimpleNamespace
    import io, contextlib
    from bms_balancing import verify
    old_si = verify.D.SI_SOURCES; verify.D.SI_SOURCES = ["Li"]
    try:
        args = SimpleNamespace(data_root=str(root), source="GITT", state="100", si_source="Li", w_dqdv=0.0, seed=0,
                               starts=1, only_source=True, only_wdqdv=True, out=str(out / "m.csv"), run_id="RID-M")
        with contextlib.redirect_stdout(io.StringIO()):
            verify.cmd_matrix(args)
    finally:
        verify.D.SI_SOURCES = old_si
    hdr = list(csv.DictReader((out / "m.csv").open(encoding="utf-8")))[0]
    assert "scale_seed" in hdr and "n_scale_samples" in hdr and not any(k in hdr for k in ("starts", "n_starts"))
    # write_meta 의 seed 는 산출에서 읽지 않고 리터럴 0 이다
    assert '"seed": 0,' in (BMS / "scripts/run_states.sh").read_text(encoding="utf-8")
    return (f"profile global/per-gamma 같은 run_id·같은 스키마, obj {rows['global'][0]['obj'][:8]} vs {rows['per-gamma'][0]['obj'][:8]}; "
            f"degeneracy samples 4/40 설정 필드 동일, n_accepted {js['4']['n_accepted']}/{js['40']['n_accepted']}; matrix 행에 starts 없음; meta seed 리터럴")


# ── F6. eol=lf 는 소급되지 않는다 — 274f1f8 이전에 autocrlf 로 받은 사본은 run_all.sh 가 CRLF 로 남는다 ───
def f6_crlf_not_retroactive():
    c = TMP / "crlf"; shutil.rmtree(c, ignore_errors=True)
    assert sh(["git", "clone", "-q", "--no-checkout", str(REPO), str(c)]).returncode == 0
    sh(["git", "config", "core.autocrlf", "true"], cwd=c)
    assert sh(["git", "checkout", "-q", PREV_GITATTR + "^"], cwd=c).returncode == 0
    assert sh(["git", "checkout", "-q", TARGET], cwd=c).returncode == 0
    eol = sh(["git", "ls-files", "--eol", "bms-balancing/matlab/tests/run_all.sh", "bms-balancing/scripts/run_states.sh"], cwd=c).stdout
    assert "w/crlf" in eol.splitlines()[0] and "w/lf" in eol.splitlines()[1], eol
    r = sh(["bash", "matlab/tests/run_all.sh"], cwd=c / "bms-balancing", timeout=120)
    assert r.returncode != 0 and "\\r" in (r.stdout + r.stderr), (r.returncode, r.stderr[:300])
    req = (BMS / "reviews/R6_REQUEST.md").read_text(encoding="utf-8")
    assert "run_all.sh" in req and "renormalize" not in req
    return "autocrlf 사본(274f1f8^ → 1049894): run_all.sh w/crlf, run_states.sh w/lf; bash run_all.sh 는 $'\\r' 오류 rc≠0; 요청문에 renormalize 안내 없음"


# ── F7. provenance.git_provenance 의 산출/코드 분리가 cwd 에 묶여 있다 ────────────────────────────────
def f7_provenance_depends_on_cwd():
    c = TMP / "prov"; shutil.rmtree(c, ignore_errors=True)
    assert sh(["git", "clone", "-q", str(REPO), str(c)]).returncode == 0
    sh(["git", "checkout", "-q", TARGET], cwd=c)
    b = c / "bms-balancing"
    with (b / "out/matrix_300_0147.csv").open("a", encoding="utf-8") as fh:
        fh.write("\n")
    art = "out/degeneracy_300_0147_Li.json"
    res = {}
    for label, cwd, argv in (("bms-balancing", b, [str(b / "scripts/provenance.py"), art]),
                             ("repo-root", c, [str(b / "scripts/provenance.py"), "bms-balancing/" + art]),
                             ("/tmp", pathlib.Path("/tmp"), [str(b / "scripts/provenance.py"), str(b / art)])):
        res[label] = json.loads(sh([PY, *argv], cwd=cwd).stdout)
    assert res["bms-balancing"]["git_dirty"] is False and res["bms-balancing"]["git_modified_outputs"]
    assert res["repo-root"]["git_dirty"] is True and res["repo-root"]["git_modified_code"]
    assert res["/tmp"]["git_dirty"] is None
    return {k: (v["git_dirty"], v["git_modified_code"]) for k, v in res.items()}


# ── F8. flock 명령이 없으면 degeneracy 산출이 .part 로 고아가 되고, 원인이 아닌 메시지가 찍힌다 ──────────
def _shim_bin() -> pathlib.Path:
    """verify 의 세 명령만 흉내내는 python3 shim (run_id 를 필드로 박은 산출) — 나머지는 진짜 python3."""
    d = TMP / "shim"; d.mkdir(exist_ok=True)
    (d / "python3").write_text(f"""#!/usr/bin/env bash
if [ "$1" = "-m" ] && [ "$2" = "bms_balancing.verify" ]; then
  case "$3" in
    degeneracy) printf '{{"state":"100","run_id":"%s","LAM_NE_percent":{{"span":1.0}}}}\\n' "$BMS_RUN_ID"; exit 0;;
    matrix|profile) out=""; while [ $# -gt 0 ]; do [ "$1" = "--out" ] && out="$2"; shift; done
        printf 'gamma_Si,obj,run_id\\n0.1,1.0,%s\\n' "$BMS_RUN_ID" > "$out"; echo "wrote $out"; exit 0;;
  esac
fi
exec {PY} "$@"
""", encoding="utf-8"); (d / "python3").chmod(0o755)
    return d


def _path_without(name: str) -> pathlib.Path:
    d = TMP / f"path_no_{name}"; d.mkdir(exist_ok=True)
    for p in ("/usr/local/sbin", "/usr/local/bin", "/usr/sbin", "/usr/bin", "/sbin", "/bin"):
        for f in pathlib.Path(p).glob("*"):
            if f.name != name and f.is_file() and os.access(f, os.X_OK) and not (d / f.name).exists():
                (d / f.name).symlink_to(f)
    assert not (d / name).exists()
    return d


def f8_flock_binary_missing_orphans_degeneracy():
    root = synth_root("가형 관련/degradation mode"); out = TMP / "f8 out dir"; out.mkdir(exist_ok=True)
    env = {"HOME": os.environ.get("HOME", "/root"), "PATH": f"{_shim_bin()}:{_path_without('flock')}",
           "BMS_DATA_ROOT": str(root), "OUT": str(out), "STATES": "100", "STARTS": "2"}
    r = sh(["bash", "scripts/run_states.sh"], cwd=BMS, env=env)
    err = re.sub(r"\x1b\[[0-9;]*m", "", r.stderr)
    assert r.returncode == 1 and "flock: command not found" in err, err[-800:]
    assert (out / ".degeneracy_100_Li.part").exists() and not (out / "degeneracy_100_Li.json").exists()
    assert "이번 시도의 산출이 아니므로 meta 를 쓰지 않는다" in err          # 원인이 아닌 진단
    assert "flock" not in (out / "degeneracy_100_Li.json.log").read_text(encoding="utf-8")   # .log 를 보라지만 거기 없다
    assert (out / "matrix_100.csv.meta.json").exists()                     # Python fcntl 경로는 통과 — 비대칭
    return "flock 부재: .degeneracy_100_Li.part 고아, json 없음, 메시지는 'run id 가 필드에 없다', .log 에 원인 없음; matrix/profile 은 통과"


# ── F9. 비-UTF-8 기본 인코딩: check_artifact·check_run_id 가 오진하고, 한글 root 라벨은 eval 을 죽인다 ─────
def f9_non_utf8_default_encoding():
    root = synth_root("가형 관련/degradation mode")
    r = sh([PY, "-m", "bms_balancing.verify", "degeneracy", "--data-root", str(root), "--state", "100",
            "--starts", "1", "--grid", "3", "--samples", "2", "--run-id", "RID"], cwd=BMS)
    j = TMP / "f9.json"; j.write_text(r.stdout, encoding="utf-8"); assert re.search("[가-힣]", r.stdout)
    ascii_env = {**os.environ, "PYTHONUTF8": "0", "PYTHONCOERCECLOCALE": "0", "LC_ALL": "C"}
    snippet = 'import json,sys\nd = json.load(open(sys.argv[1]))\nsys.exit(0 if isinstance(d, dict) and d else 1)'  # run_states.sh 98-100
    assert sh([PY, "-c", snippet, str(j)]).returncode == 0
    assert sh([PY, "-c", snippet, str(j)], env=ascii_env).returncode == 1                       # → "JSON 이 아니다"
    rr = sh([PY, str(BMS / "scripts/provenance.py"), "--check-run-id", str(j), "RID"], env=ascii_env)
    assert rr.returncode == 1 and "UnicodeEncodeError" in rr.stderr                               # → bound=0
    kr = synth_root("kr/가형 관련")
    rc, _, err = eval_audit_line(kr, "--out", str(TMP / "f9_kr.csv"), env={**os.environ, "PYTHONIOENCODING": "cp1252"})
    assert rc == 1 and "UnicodeEncodeError" in err and not (TMP / "f9_kr.csv").exists()
    rc, _, _ = eval_audit_line(synth_root("cells/c168"), "--out", str(TMP / "f9_ok.csv"), env={**os.environ, "PYTHONIOENCODING": "cp1252"})
    assert rc == 0 and (TMP / "f9_ok.csv").exists()                                               # ASCII basename 은 통과
    return "ASCII 기본: check_artifact rc 1, check_run_id UnicodeEncodeError → 오진; cp1252 stdout + 한글 basename: eval rc 1, --out 안 써짐"


# ── F10. 잠금 호출이 ENOLCK 면 계산된 행이 통째로 버려진다 (NTFS/9p 류 마운트 가정이 문서에 없다) ─────────
def f10_enolck_discards_rows():
    import fcntl
    from bms_balancing import verify
    d = TMP / "f10"; d.mkdir(exist_ok=True); real = fcntl.flock
    fcntl.flock = lambda fh, op: (_ for _ in ()).throw(OSError(errno.ENOLCK, "No locks available"))
    try:
        try:
            verify.atomic_write_csv(d / "profile.csv", [{"gamma_Si": 0.1, "obj": 1.0, "run_id": "r"}], ["gamma_Si", "obj", "run_id"])
            raised = False
        except OSError as e:
            raised = e.errno == errno.ENOLCK
    finally:
        fcntl.flock = real
    left = sorted(p.name for p in d.iterdir())
    assert raised and left == ["profile.csv.lock"], left
    for f in ("README.md", "FINDINGS.md", "WORKING_STATE.md"):
        assert "NTFS" not in (BMS / f).read_text(encoding="utf-8")
    return f"ENOLCK → OSError, 남은 파일 {left} (행 없음); 문서에 NTFS/잠금 가정 없음"


# ── F11. 요청문의 검증 수치가 대상 커밋과 어긋난다 (86 passed vs 87) · out/*.lock 이 gitignore 밖 ──────────
def f11_request_numbers_stale():
    r = sh([PY, "-m", "pytest", "tests/", "--collect-only", "-q"], cwd=BMS)
    n = sum(1 for l in r.stdout.splitlines() if "::" in l)
    req = (BMS / "reviews/R6_REQUEST.md").read_text(encoding="utf-8")
    assert "86 passed" in req and n == 87, (n, "86 passed" in req)
    last = sh(["git", "log", "-1", "--format=%h", "--", "bms-balancing/reviews/R6_REQUEST.md"], cwd=REPO).stdout.strip()
    assert last.startswith(TARGET[:7]) or sh(["git", "rev-parse", "--short", TARGET], cwd=REPO).stdout.strip() == last
    ign = (BMS / ".gitignore").read_text(encoding="utf-8")
    assert ".lock" not in ign and "out/.*.part" in ign
    return f"collect-only {n} 항목, 요청문 '86 passed' (요청문 최종 수정 = 대상 커밋); .gitignore 에 *.lock 없음"


ALL = [f1_root_label_not_an_identifier, f2_u13_copy_cannot_evidence_four_roots, f3_library_versions_not_in_signature,
       f4_fullcell_workbook_identity_unrecorded, f5_args_not_in_artifact_signature, f6_crlf_not_retroactive,
       f7_provenance_depends_on_cwd, f8_flock_binary_missing_orphans_degeneracy, f9_non_utf8_default_encoding,
       f10_enolck_discards_rows, f11_request_numbers_stale]

if __name__ == "__main__":
    want = {a.lower() for a in sys.argv[1:]}
    fails = 0
    print(f"repo {REPO}  target {TARGET}  tmp {TMP}")
    for fn in ALL:
        tag = fn.__name__.split("_")[0]
        if want and tag not in want:
            continue
        try:
            note = fn(); print(f"[REPRODUCED] {fn.__name__}: {note}")
        except AssertionError as e:
            fails += 1; print(f"[NOT REPRODUCED — 고쳐졌나?] {fn.__name__}: {e!r}")
        except Exception as e:                        # noqa: BLE001
            fails += 1; print(f"[ERROR] {fn.__name__}: {type(e).__name__}: {e}")
    sys.exit(1 if fails else 0)
