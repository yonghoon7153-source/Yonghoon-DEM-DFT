"""Codex R7 (2026-09-12, 대상 `521be85`, NO-GO · P1 3 · P2 3) — 반례를 회귀로.

원문·재현 패키지는 `reviews/r7_repros/codex/` (sha256 대조 10/10). 여기 테스트는 **패키지의 probe 를 우리 fixture 로
다시 쓴 것**이고, 원본 probe 자체의 재생 기록은 `reviews/r7_repros/replay_ours_*.json` 이다.

R6 는 "독자가 검증한 묶음만 소비하는가" 였고 R7 은 **그 다음 단계** — 올바르게 읽은 뒤 (a) 일부가 빠졌는데 전체
결론을 내리는가 (b) 적합과 잡음이 같은 입력을 쓰는가 (c) 행이 기준 입력의 출처를 남기는가.
"""
from __future__ import annotations
import contextlib, csv, io, json, os, pathlib, subprocess, sys
from types import SimpleNamespace

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pytest                                                             # noqa: E402
from bms_balancing import verify                                          # noqa: E402
from bms_balancing import schema as _S                                    # noqa: E402
from test_r6_internal import _synth_root, _bump_xlsx, _prov, _cs          # noqa: E402
from test_review_findings import _load_script, _section, NOT_A_CLAIM      # noqa: E402

CODEX = ROOT / "reviews" / "r7_repros" / "codex"


def _doc(name): return (ROOT / name).read_text(encoding="utf-8")
def _live(txt): return NOT_A_CLAIM.sub("", txt)


def _args(root, out=None, state="200", **kw):
    a = SimpleNamespace(data_root=str(root), source="GITT", state=state, si_source="Li", w_dqdv=0.0,
                        starts=2, seed=0, only_source=True, only_wdqdv=True, out=str(out) if out else None,
                        # ⚠ Codex R11 P1-3: 정본 γ 격자(21)가 아니면 그 실행은 subset 이고 canonical 이 아니다 —
                        #   격자가 시험 주제가 아닌 곳은 정본 격자로 돈다 (좁히는 시험은 kw 로 grid 를 준다)
                        run_id="r7-test", grid=_S.CANONICAL_GAMMA_GRID_N, tol=0.01, profile_scale="global",
                        samples=50, repeats=2)
    for k, v in kw.items():
        setattr(a, k, v)
    return a


def _noisy_reexport(path, sheet_col, sigma=0.020, seed=731):
    """같은 이름으로 **정상 재-export** — 전압에 잡음을 더한다 (오프셋은 σ 를 안 움직인다).
    풀셀은 2행 헤더(1행 상태·2행 단위)에 (capacity, voltage) 쌍 열이다."""
    import numpy as np, pandas as pd
    rng = np.random.default_rng(seed)
    df = pd.read_excel(path, header=None)
    col = 2 * verify.D.FULL_COL[sheet_col] + 1
    v = pd.to_numeric(df.iloc[2:, col], errors="coerce")
    df.iloc[2:, col] = v + rng.normal(0.0, sigma, size=v.shape)
    df.to_excel(path, header=False, index=False)


def _deg(state, rid, spans, schema=False):
    obj = {"run_id": rid, "state": state, "si_source": "Li", "half_cell": "GITT", "n_starts": 24,
           "best_modes_percent": {k: 1.0 for k in spans},
           **{f"{k}_percent": {"min": 0.0, "max": v, "span": v, "is_lower_bound": True} for k, v in spans.items()}}
    if schema:      # check_u14 가 숫자 대조까지 가려면 producer 스키마(`schema.DEGENERACY_KEYS`)와 **진짜 receipt** 가 다 있어야 한다 (R9-03)
        from bms_balancing import schema as S
        ci = {"half_cell": {"path": "h.xlsx", "sha256": "1" * 64}, "full_cell": {"path": "f.xlsx", "sha256": "2" * 64},
              "literature": {"gr": {"path": "g.xlsx", "sha256": "3" * 64}, "si": {"path": "s.csv", "sha256": "4" * 64}}}
        rci = {"half_cell": {"path": "p.xlsx", "sha256": "5" * 64}, "full_cell": ci["full_cell"], "literature": ci["literature"]}
        obj |= {"w_dqdv": 0.0, "tol_percent_of_best": 1.0, "seed": 0, "n_grid": 21, "n_samples": 400, "env": {"python": "3.11.0", "numpy": "2.0", "scipy": "1.11.0", "pandas": "2.0.0", "platform": "linux-x"},
                "consumed_inputs": ci, "ref_consumed_inputs": rci, "inputs_sha": S.inputs_digest(ci),
                "n_accepted": 5, "best_obj": 1.5, "best_p": [1.0, 0.0, 1.0, 0.0, 0.2], "ref_p": [1.0, 0.0, 1.0, 0.0, 0.2]}
    return obj


def _sign(art, rid, state, full=False):
    prov = _prov()
    meta = {"artifact": art.name, "state": state, "run_id": rid, "sha256": prov.sha256_file(art), "starts": 24}
    if full:        # check_u14 의 META_KEYS + 실행 조건 + argv·roster (Codex R11 P1-6: 실제 `write_meta` 가 쓰는 전부)
        from bms_balancing import schema as _S
        meta |= {"env": {"python": "3.12.3", "numpy": "2.5.3", "scipy": "1.18.1", "pandas": "2.2.0", "platform": "test-fixture"},
                 "started_utc": "2026-09-12T00:00:00Z", "half_cell_source": "GITT", "si_source": "Li", "seed": 0,
                 "git_commit_at_start": "0" * 40, "git_state_changed_during_run": False, "git_dirty": False,
                 "git_modified_code": [], "argv": ["python3", "-m", "bms_balancing.verify", "fixture"],
                 "roster": _S.body_roster(art.name, art.read_bytes())}
    (art.parent / (art.name + ".meta.json")).write_text(json.dumps(meta), encoding="utf-8")


def _compare_states(path):
    r = subprocess.run([sys.executable, str(ROOT / "scripts/compare_states.py"), "case=" + str(path)],
                       cwd=ROOT, capture_output=True, text=True, timeout=120)
    line = next((s for s in r.stdout.splitlines() if "항상 가장 좁은가" in s), "")
    return r.returncode, line, r.stdout, r.stderr


def test_d7_01_aggregate_says_incomplete_instead_of_certifying_the_states_that_survived(tmp_path):
    """[Codex R7-01 · P1] 반례인 상태가 **미완으로 제외되면** 전체 판정이 "아니오" 에서 "예" 로 뒤집혔다 (rc 0).
    `read_unit` 은 그 미완을 정확히 거부하는데(R6-01·02), 상위 집계가 남은 부분집합을 전체처럼 인증했다. 빈
    디렉터리도 "예" 였다.

    닫힘 조건(Codex): 후보·검증·제외를 구분해 세고, 제외가 있거나 관측이 0 이면 전체 "항상 예" 판정을 내지 않으며
    종료 상태가 그 미완을 표현한다. 일정은 **아니오 → 미완 → 아니오** 여야 한다."""
    out = tmp_path / "out"; out.mkdir()
    narrow = out / "degeneracy_100_Li.json"; wide = out / "degeneracy_200_Li.json"
    verify.atomic_write_json(narrow, _deg("100", "A100", {"LAM_PE": 2.0, "LAM_NE": 3.0, "LLI": 1.0}))
    verify.atomic_write_json(wide, _deg("200", "A200", {"LAM_PE": 1.0, "LAM_NE": 2.0, "LLI": 9.0}))
    _sign(narrow, "A100", "100"); _sign(wide, "A200", "200")
    rc, line, _, _ = _compare_states(out)
    assert rc == 0 and "아니오" in line, (rc, line)                        # 둘 다 온전 → 반례가 보인다

    verify.atomic_write_json(wide, _deg("200", "B200", {"LAM_PE": 1.0, "LAM_NE": 2.0, "LLI": 9.0}))  # data 만 게시
    assert _prov().verify_unit(wide)[0] is False
    rc, line, out_txt, err = _compare_states(out)
    assert "표에서 뺀다" in err, err
    assert not line.rstrip().endswith("예"), f"제외된 반례를 빼고 '예' 로 인증했다: {line}"
    assert "미완" in out_txt and rc != 0, (rc, out_txt[-600:])
    assert "1/2" in out_txt or "제외 1" in out_txt, out_txt[-600:]         # 몇 개 중 몇 개를 봤는지 말한다

    _sign(wide, "B200", "200")
    rc, line, _, _ = _compare_states(out)
    assert rc == 0 and "아니오" in line, (rc, line)                        # 되돌아온다 — 아니오 → 미완 → 아니오

    empty = tmp_path / "empty"; empty.mkdir()
    rc, line, out_txt, _ = _compare_states(empty)
    assert not line.rstrip().endswith("예") and rc != 0, (rc, line, out_txt[-400:])


def test_d7_02_noise_measures_sigma_on_the_snapshot_it_fitted(tmp_path):
    """[Codex R7-02 · P1] `cmd_noise` 는 `build(A)` 뒤 같은 경로를 **다시 열어** 잡음을 쟀다. 그 사이 정상 재-export B 가
    있으면 분자는 A 의 부적합, 분모는 B 의 σ 다 — 어느 실행의 값도 아니고, 진단 문장이 "거짓으로 좁은 구간" 에서
    "likelihood 를 논의할 여지" 로 바뀐다 (misfit/σ 2163 → 1.59).

    닫힘 조건(Codex): 적합용 배열과 **잡음용 원시 capacity/voltage** 를 같은 snapshot 에서 공급하고 그 identity 를
    기록한다. 원시 배열을 평활·재표본 배열로 바꿔 정의를 바꾸지 않는다."""
    root = _synth_root(tmp_path)
    wb = verify.D.full_cell_workbook(root)

    def run():
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            verify.cmd_noise(_args(root))
        return json.loads(buf.getvalue())

    A = run()
    real_build, seen = verify.build, []

    def build_then_reexport(*a, **k):
        obj = real_build(*a, **k)
        seen.append(dict(obj.consumed_inputs["full_cell"]))
        _noisy_reexport(wb, "200")                                        # 정상 재-export B (같은 이름, σ 가 움직인다)
        return obj

    verify.build = build_then_reexport
    try:
        mixed = run()
    finally:
        verify.build = real_build
    B = run()
    # A 의 분자에 B 의 분모가 붙으면 안 된다 — 섞인 실행은 A/A 여야 한다
    assert mixed["misfit_rmse_pocv_V"] == A["misfit_rmse_pocv_V"], (mixed["misfit_rmse_pocv_V"], A["misfit_rmse_pocv_V"])
    assert mixed["sigma_at_k1_V"] == A["sigma_at_k1_V"], (mixed["sigma_at_k1_V"], A["sigma_at_k1_V"], B["sigma_at_k1_V"])
    assert B["sigma_at_k1_V"] != A["sigma_at_k1_V"], "fixture 가 σ 를 안 움직였다"
    assert mixed["verdict"] == A["verdict"] != B["verdict"]
    # 소비한 입력 identity 가 산출에 남는다 (섞임을 나중에 짚을 수 있게)
    assert mixed["consumed_inputs"]["full_cell"]["sha256"] == seen[0]["sha256"], mixed["consumed_inputs"]
    assert mixed["inputs_sha"] and mixed["inputs_sha"] != B["inputs_sha"]


def _matrix_rows(path, root, state="200", **kw):
    """`--out` 은 **파일**이다 (디렉터리가 아니다).

    ⚠ Codex R11 P1-2: `--only-source`·`--only-wdqdv` 로 **좁힌** 실행은 권위 명부를 다 돌지 않았으므로 subset 이고,
    canonical 이 아니라 `partial/` 에 게시된다. producer 의 rc 가 말하는 자리에서 읽는다.
    """
    with contextlib.redirect_stdout(io.StringIO()):
        rc = verify.cmd_matrix(_args(root, path, state=state, **kw))
    return list(csv.DictReader(verify.publish_target(path, "complete" if rc == 0 else "subset")
                               .open(encoding="utf-8-sig")))


def test_d7_03_matrix_and_profile_rows_carry_the_reference_input_signature(tmp_path):
    """[Codex R7-03 · P1] matrix 행은 **기준 적합**도 소비하는데 `inputs_sha` 는 대상 것만 적었다. 기준 전용 입력
    (pristine 반쪽전지)만 바꾸면 LAM_NE 2.85 → 3.85 %p 로 움직이는데 행의 서명은 **같다** — 대상 digest 가 틀린 게
    아니라 다른 계산 입력의 출처가 빠진 것이다. profile 행도 같다. degeneracy JSON 은 `ref_consumed_inputs` 를
    이미 남긴다 (양성 경로).

    닫힘 조건(Codex): target/ref 각각의 실제 소비 snapshot identity 를 행에 남긴다."""
    root = _synth_root(tmp_path); out = tmp_path / "out"; out.mkdir()
    a = _matrix_rows(out / "A.csv", root)[0]
    assert a.get("ref_inputs_sha"), f"기준 입력 서명 열이 없다: {sorted(a)}"
    assert a.get("ref_consumed_inputs"), sorted(a)
    _bump_xlsx(root / "data/half_cell/GITT/pristine.xlsx", delta=0.02, header=0)   # 기준 전용 입력만 바꾼다
    b = _matrix_rows(out / "B.csv", root)[0]
    assert a["inputs_sha"] == b["inputs_sha"], "대상 입력은 그대로여야 한다 (fixture)"
    assert a["ref_inputs_sha"] != b["ref_inputs_sha"], (a["ref_inputs_sha"], b["ref_inputs_sha"])
    assert float(a["LAM_NE_pct"]) != float(b["LAM_NE_pct"]), "fixture 가 숫자를 안 움직였다"
    ra, rb = json.loads(a["ref_consumed_inputs"]), json.loads(b["ref_consumed_inputs"])
    assert ra["half_cell"]["sha256"] != rb["half_cell"]["sha256"], (ra, rb)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        verify.cmd_profile(_args(root, out / "profile.csv"))
    prof = [json.loads(l) for l in buf.getvalue().splitlines() if l.startswith("{") and '"gamma_Si"' in l]
    assert prof and all(r.get("ref_inputs_sha") for r in prof), prof[:1]


def _u14(new, old, *extra):
    return subprocess.run([sys.executable, str(ROOT / "scripts/check_u14.py"), "--new", str(new), "--old", str(old),
                           *extra], cwd=ROOT, capture_output=True, text=True, timeout=120)


def test_d7_04_check_u14_does_not_prefer_a_versioned_sibling_in_a_current_directory(tmp_path):
    """[Codex R7-04 · P2] `--old` 가 **현행 디렉터리**여도 역사 규칙(가장 높은 `_vN`)이 적용됐다. 현행 독자는 `_v2` 를
    경고·제외하고 A 를 쓰는데 `check_u14` 는 `_v2`(B) 를 골라 "정본과 전부 같다" rc 0 을 냈다 — `_v2` 를 지우면 같은
    대조가 차이 2 건 rc 1 이다. 두 규칙이 docstring 으로만 갈라져 있었다.

    닫힘 조건(Codex): 현행 `--old` 에는 unversioned 규칙(또는 sibling 거부), 명시한 역사 리비전 모드에서만 최고판.
    어느 정책으로 골랐는지 출력한다."""
    cur, rerun = tmp_path / "current", tmp_path / "rerun"
    for d in (cur, rerun):
        d.mkdir()
    A = _deg("100", "A", {"LAM_PE": 1.0, "LAM_NE": 2.0, "LLI": 0.5736895850554351}, schema=True)
    B = _deg("100", "B", {"LAM_PE": 1.0, "LAM_NE": 2.0, "LLI": 1.5736895850554351}, schema=True)
    for d, obj, rid in ((cur, A, "A"), (rerun, B, "B")):
        f = d / "degeneracy_100_Li.json"; verify.atomic_write_json(f, obj); _sign(f, rid, "100", full=True)
    # ⚠ 자체 리뷰 C02 뒤: 역사 리비전의 정본(`_v2`)과 재실행은 **독립 실행**이다 — 숫자는 같아도 run id 는 다르다
    #   (같으면 같은 시도의 사본이라 alias 로 막힌다). 전 판 fixture 는 둘 다 `"B"` 였다.
    B_hist = _deg("100", "B-hist", {"LAM_PE": 1.0, "LAM_NE": 2.0, "LLI": 1.5736895850554351}, schema=True)
    stale = cur / "degeneracy_100_Li_v2.json"
    verify.atomic_write_json(stale, B_hist); _sign(stale, "B-hist", "100", full=True)
    r = _u14(rerun, cur)
    assert "정책" in r.stdout and "current" in r.stdout, r.stdout          # 어느 규칙으로 골랐는지 말한다
    assert "쓰지 않았다" in r.stdout and "degeneracy_100_Li_v2.json" in r.stdout, r.stdout
    assert r.returncode == 1 and "다른 숫자" in r.stdout, (r.returncode, r.stdout)
    # 역사 리비전 모드는 그대로 최고판을 쓴다 (U14-02 가 필요로 한 규칙) — 명시했을 때만
    h = _u14(rerun, cur, "--baseline-policy", "historical")
    assert "historical" in h.stdout and h.returncode == 0 and "전부 같다" in h.stdout, (h.returncode, h.stdout)
    stale.unlink(); (cur / "degeneracy_100_Li_v2.json.meta.json").unlink()
    r2 = _u14(rerun, cur)
    assert r2.returncode == 1 and r2.stdout.count("다른 숫자") == r.stdout.count("다른 숫자"), (r2.returncode, r2.stdout)


def test_d7_05_adapted_replay_does_not_treat_a_missing_baseline_as_the_current_directory():
    """[Codex R7-05 · P2] `R6_OLD_OUT` 이 없으면 `Path("")` 가 `.` 이 되고 존재하는 디렉터리라 **현재 트리를 과거
    baseline 으로** 삼아 full 재생을 부른다 — 요청문에 적은 기본 호출이 5/6·rc 1 이었다. 없는 환경값은 경로로
    바꾸기 **전에** 걸러내고, baseline 없는 재생은 full 과 구분해 부분으로 표시한다."""
    m = _load_script("replay_codex_r6_adapted", CODEX.parent.parent / "r6_repros/codex/replay_codex_r6_adapted.py") \
        if False else None                                                # (경로는 아래에서 직접 연다)
    import importlib.util
    p = ROOT / "reviews/r6_repros/codex/replay_codex_r6_adapted.py"
    spec = importlib.util.spec_from_file_location("r6_adapted", p)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    for value in (None, "", "   "):
        env = dict(os.environ)
        env.pop("R6_OLD_OUT", None)
        if value is not None:
            env["R6_OLD_OUT"] = value
        assert mod.baseline_from_env(env) is None, value                  # `.` 로 떨어지지 않는다
    env = dict(os.environ, R6_OLD_OUT=str(ROOT / "out"))
    assert mod.baseline_from_env(env) == (ROOT / "out").resolve()
    assert "R6_OLD_OUT" in p.read_text(encoding="utf-8")                   # 어떻게 주는지 파일이 말한다


def test_d7_06_mutation_audit_exits_nonzero_when_a_mutation_is_missed(monkeypatch):
    """[Codex R7-06 · P2] 변이 감사가 `MISSED: 1` 을 찍고도 rc 0 이었다 — 자동화가 그 실패를 못 본다. 놓친 변이가
    있거나 복구 뒤 회귀가 실패하면 비영 종료여야 한다 (실제 8 건은 전부 CAUGHT 였다 — 그 관측은 그대로다)."""
    import importlib.util
    p = ROOT / "reviews/r6_repros/codex_r6_mutation_audit.py"
    spec = importlib.util.spec_from_file_location("r6_audit", p)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    calls = []
    monkeypatch.setattr(mod, "run", lambda k: (calls.append(k), (0, "1 passed"))[1])   # 아무 변이도 안 잡힌다
    monkeypatch.setattr(mod, "MUTATIONS", [("무해한 주석 변이", "c6_01", "scripts/provenance.py",
                                            "def read_unit(", "def read_unit(  # noqa: E501 (감사 자기시험)\n")])
    before = (ROOT / "scripts/provenance.py").read_bytes()
    rc = mod.main()
    assert (ROOT / "scripts/provenance.py").read_bytes() == before, "트리를 되돌리지 않았다"
    assert rc != 0, "놓친 변이가 있는데 0 을 냈다"
    assert calls, calls


def test_d7_07_docs_state_the_profile_budget_without_settling_the_cause():
    """[Codex R7 §5] "γ당 25 회" 는 사실이지만 그것만으로 "시작 예산이 충분했다"·"차이는 ULP 때문" 이 되지 않는다.
    또 Codex Q2 가 짚은 전제 오류: `run_states.sh` 에는 **실행 직전 `inputs_sha` 가 없다** (그 문자열 0 회; 실행 전에는
    `LAST_PRE_PV` 의 git 상태·시각만 모은다). 서명은 각 `build()` 가 소비 snapshot 으로 만든다."""
    sh = (ROOT / "scripts/run_states.sh").read_text(encoding="utf-8")
    assert "inputs_sha" not in sh, "run_states.sh 가 inputs_sha 를 만든다면 이 문장을 다시 써야 한다"
    for name in ("reviews/R6_LEDGER.md", "WORKING_STATE.md"):
        live = _live(_doc(name))
        assert "적은 시작" not in live, name
    led = _live(_doc("reviews/R6_LEDGER.md"))
    assert "γ당 25" in led
    assert "U16" in led and ("원인은 U16" in led or "원인 분리" in led or "미확정" in led), led[-800:]
    req = _live(_doc("reviews/R8_REQUEST.md"))
    assert "실행 직전" not in req or "없다" in req, "Q2 전제(실행 직전 inputs_sha)를 그대로 들고 있다"
