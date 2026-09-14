"""Codex R8 (2026-09-12, 대상 `a22da33`, NO-GO · P1 4 · P2 4) — 반례를 회귀로.

원문·재현 패키지는 `reviews/r8_repros/codex/` (sha256 10/10). 수정 전 우리 HEAD 에서 세 스크립트가 전부 재현됐다
(`reviews/r8_repros/replay_ours_a22da33_before/`). 여기 테스트는 그 probe 를 우리 fixture 로 다시 쓴 것이다.

R7 이 "올바르게 읽은 다음 단계" 였다면 R8 은 **그 합성** — 검증된 개별 묶음 → 완전한 모집단 → 전체 결론이 이어지는가.
"""
from __future__ import annotations
import contextlib, csv, hashlib, importlib.util, io, json, os, pathlib, subprocess, sys
from types import SimpleNamespace

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np                                                        # noqa: E402
import pytest                                                             # noqa: E402
from bms_balancing import verify                                          # noqa: E402
from test_r6_internal import _synth_root, _prov, _cs, _hook_open          # noqa: E402
from test_r7_codex import _args, _deg, _sign, _compare_states, _doc, _live  # noqa: E402
from test_review_findings import _load_script, audit_json, matrix_row      # noqa: E402


def _mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def _cli(script, *args):
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / script), *map(str, args)],
                       cwd=ROOT, capture_output=True, text=True, timeout=180)
    return r.returncode, r.stdout, r.stderr


def _verdict(stdout):
    return next((s for s in stdout.splitlines() if "항상 가장 좁은가" in s), "")


# ── R8-01 ────────────────────────────────────────────────────────────────────────────────────
def test_d8_01_aggregate_keeps_every_verified_unit_and_counts_every_requested_root(tmp_path):
    """[Codex R8-01 · P1] (a) 같은 state 의 서로 다른 Si 두 정상 묶음 — `out[state]` 에서 Li 가 Kunz 를 **덮어** 1/1·예.
    (b) `good=<정상> empty=<빈>` 또는 존재하지 않는 root 를 명시해도 1/1·예 rc 0 — 빈 root 는 후보가 되지 않아 전건성이
    합성되지 않았다.

    닫힘 조건(Codex): inventory 를 축소 전에 만들고 (root, state, source, Si) identity 를 보존, 요청한 root 마다
    expected/available/verified/excluded 를 센다. 위 입력은 두 관측 또는 명시적 부분이어야지 `1/1·예` 가 아니다."""
    base = tmp_path / "si"; base.mkdir()
    kunz = base / "degeneracy_100_Kunz.json"; li = base / "degeneracy_100_Li.json"
    wide = {"LAM_PE": 1.0, "LAM_NE": 2.0, "LLI": 9.0}; narrow = {"LAM_PE": 2.0, "LAM_NE": 3.0, "LLI": 1.0}
    verify.atomic_write_json(kunz, _deg("100", "r8-Kunz", wide) | {"si_source": "Kunz"}); _sign(kunz, "r8-Kunz", "100")
    rc, line, out, _ = _compare_states(base)
    assert rc == 0 and "아니오" in line and "1/1" in out, (rc, line)
    verify.atomic_write_json(li, _deg("100", "r8-Li", narrow)); _sign(li, "r8-Li", "100")
    assert _prov().read_unit(kunz)[0] is True and _prov().read_unit(li)[0] is True
    exc: list = []
    got = _cs().load_degeneracy(base, excluded=exc)
    assert len(got) == 2 and not exc, (sorted(got), exc)                  # 축소 전 inventory: 둘 다 남는다
    rc, line, out, _ = _compare_states(base)
    assert "2/2" in out and "Kunz" in out and "Li" in out, out[-900:]
    assert not line.rstrip().endswith("예"), line                        # Kunz 가 반례다 — 덮여서 사라지면 안 된다
    assert rc == 0 and "아니오" in line, (rc, line)

    good, empty = tmp_path / "good", tmp_path / "empty"; good.mkdir(); empty.mkdir()
    g = good / "degeneracy_100_Li.json"; verify.atomic_write_json(g, _deg("100", "r8-one", narrow)); _sign(g, "r8-one", "100")
    for extra in ("empty=" + str(empty), "absent=" + str(tmp_path / "absent")):
        r = subprocess.run([sys.executable, str(ROOT / "scripts/compare_states.py"), "good=" + str(good), extra],
                           cwd=ROOT, capture_output=True, text=True, timeout=120)
        v = _verdict(r.stdout)
        assert r.returncode != 0 and not v.rstrip().endswith("예"), (extra, r.returncode, v)
        assert "미완" in r.stdout and ("empty" in r.stdout or "absent" in r.stdout), r.stdout[-700:]
        assert "root" in r.stdout or "요청" in r.stdout, r.stdout[-700:]   # 요청한 root 별 roster 를 말한다


# ── R8-02 ────────────────────────────────────────────────────────────────────────────────────
def _full_matrix_rows(rid, lli=1.0):
    """producer 스키마(`schema.MATRIX_ROW` 39 열)를 **전부** 갖춘 matrix 행 — 진짜 receipt(역할·path·64-hex·재계산 digest)
    포함. R9-03 전의 이 fixture 는 열 이름만 맞는 부분집합이라 checker 가 내용을 안 본다는 사실을 가리고 있었다."""
    from bms_balancing import schema as S
    ci = {"half_cell": {"path": "h.xlsx", "sha256": "1" * 64}, "full_cell": {"path": "f.xlsx", "sha256": "2" * 64},
          "literature": {"gr": {"path": "g.xlsx", "sha256": "3" * 64}, "si": {"path": "s.csv", "sha256": "4" * 64}}}
    rci = {"half_cell": {"path": "p.xlsx", "sha256": "5" * 64}, "full_cell": ci["full_cell"], "literature": ci["literature"]}
    # ⚠ Codex R13 P1-1 / Q1: 전 판은 **2 행**(Li, Kunz)을 만들고 `authority=requested=2` 로 봉인했다 —
    #   2/32 짜리가 "정상 전수 대조군" 이었다. 구성원 검사가 없던 시절엔 통과했고, 그래서 승격 경로
    #   회귀 전체가 정본 모집단을 한 번도 밟지 않았다. 이제 정본 조합 집합 그대로 만든다.
    rows = []
    keys = sorted(S.canonical_combo_keys("100"))
    for i, (hc, s, w) in enumerate(keys):
        v = dict(half_cell=hc, si=s, w_dqdv=repr(w), run_id=rid, inputs_sha=S.inputs_digest(ci), ref_inputs_sha=S.inputs_digest(rci),
                 consumed_inputs=json.dumps(ci), ref_consumed_inputs=json.dumps(rci), scale_seed="0", n_scale_samples="50",
                 scale_pocv_target="1.0", scale_dvdq_target="1.0", scale_dqdv_target="1.0", scale_pocv_ref="1.0",
                 scale_dvdq_ref="1.0", scale_dqdv_ref="1.0", scale_audit_target=audit_json(), scale_audit_ref=audit_json(), obj="0.01",
                 rmse_pocv="0.002", a_PE="1.0", b_PE="0.0", a_NE="1.1", b_NE="0.0", gamma_Si="0.3", c_cell="1.0", bounds="-",
                 ref_a_PE="1.0", ref_b_PE="0.0", ref_a_NE="1.0", ref_b_NE="0.0", ref_gamma_Si="0.2", ref_obj="0.01",
                 ref_rmse_pocv="0.002", ref_c_cell="1.0", ref_bounds="-", LAM_PE_pct="1.0", LAM_NE_pct="2.0", LLI_pct=str(lli + i),
                 # 자체 리뷰 C05: matrix 도 모집단을 행에 봉인한다 — 주장이 본문(행 수)과 맞아야 한다
                 combo_roster=json.dumps({"authority": len(keys), "requested": len(keys),
                                          "succeeded": len(keys),
                                          "missing_input": [], "failed": [], "absent": []}))
        assert set(v) == set(S.MATRIX_ROW), set(v) ^ set(S.MATRIX_ROW)
        rows.append({k: v[k] for k in S.MATRIX_ROW})
    return rows


def test_d8_02_check_u14_consumes_only_the_verified_unit_and_requires_the_provenance_schema(tmp_path):
    """[Codex R8-02 · P1] `check_u14` 는 data 와 meta 를 따로 읽고 필드 존재만 봐서 (a) 정상 재실행 B 가 data 만 게시한
    중단 상태(`read_unit` False)를 "스키마 전부 갖춤 · 숫자 전부 같다 · rc 0" 으로 인증했고 (b) 필수 스키마가 R7-03/R8
    의 기준 입력 출처 열을 요구하지 않아 현행 out/ 이 "전부 갖췄다" 로 통과했다.

    닫힘 조건(Codex): 검증된 동일 data/meta snapshot 만으로 검사하고 묶음 불일치는 nonzero; producer 스키마와 checker
    의 required 스키마를 한 정본에서 대조; 현행 정본은 provenance-incomplete 로 **명시적으로** 제한한다."""
    old, new = tmp_path / "old", tmp_path / "new"; old.mkdir(); new.mkdir()
    # ⚠ 자체 리뷰 C02 뒤: 두 **독립 실행**은 run id 가 달라야 한다 (같으면 같은 시도의 사본 = alias).
    #   전 판 fixture 는 양쪽에 `r8-unit-A` 를 줘서 그 축을 구조적으로 못 쟀다.
    for d, rid in ((old, "r8-unit-A"), (new, "r8-unit-B0")):
        a = _deg("100", rid, {"LAM_PE": 1.0, "LAM_NE": 2.0, "LLI": 0.5}, schema=True)
        f = d / "degeneracy_100_Li.json"; verify.atomic_write_json(f, a); _sign(f, rid, "100", full=True)
    a = _deg("100", "r8-unit-B0", {"LAM_PE": 1.0, "LAM_NE": 2.0, "LLI": 0.5}, schema=True)
    rc, out, _ = _cli("check_u14.py", "--new", new, "--old", old)
    assert rc == 0 and "전부 같다" in out, (rc, out)
    newf = new / "degeneracy_100_Li.json"
    verify.atomic_write_json(newf, dict(a, run_id="r8-unit-B"))            # 다른 정상 시도가 data 만 게시
    assert _prov().read_unit(newf)[0] is False
    rc, out, _ = _cli("check_u14.py", "--new", new, "--old", old)
    assert rc != 0 and "전부 같다" not in out, (rc, out)
    assert "묶음" in out or "미완" in out, out
    _sign(newf, "r8-unit-B", "100", full=True)
    rc, out, _ = _cli("check_u14.py", "--new", new, "--old", old)
    assert rc == 0, (rc, out)
    # (b) producer 가 쓰는 열이 checker 의 필수 스키마에 있어야 한다 — 한 정본에서 대조
    cu = _mod("cu14_r8", ROOT / "scripts/check_u14.py")
    for c in ("ref_inputs_sha", "consumed_inputs", "ref_consumed_inputs"):
        assert c in cu.MATRIX_COLS, (c, cu.MATRIX_COLS)
        assert c in cu.PROFILE_COLS, (c, cu.PROFILE_COLS)
    m = new / "matrix_100.csv"
    rows = _full_matrix_rows("r8-m")
    verify.atomic_write_csv(m, rows, list(rows[0])); _sign(m, "r8-m", "100", full=True)
    rc, out, _ = _cli("check_u14.py", "--new", new, "--schema-only")
    assert rc == 0, (rc, out)
    stripped = [{k: v for k, v in r.items() if k != "ref_inputs_sha"} for r in rows]
    verify.atomic_write_csv(m, stripped, list(stripped[0])); _sign(m, "r8-m", "100", full=True)
    rc, out, _ = _cli("check_u14.py", "--new", new, "--schema-only")
    assert rc == 2 and "ref_inputs_sha" in out, (rc, out)
    # 옛 스키마 묶음에는 그 열이 없다 — 도구가 그것을 **말해야** 한다 (조용히 "전부 갖췄다" 가 아니라).
    # ⚠ U18b 승격(2026-09-14): 표본은 `out/` 이 아니라 `out/archive/legacy_r6_u14/` 다. 승격 뒤 정본은 rc 0 이고
    #   (그것이 승격의 뜻이다), 옛 묶음은 조건 7 대로 얼려 보존됐다 — blocked_by 40·25·6·1 이 그대로 재현된다.
    legacy = ROOT / "out" / "archive" / "legacy_r6_u14"
    rc, out, _ = _cli("check_u14.py", "--new", legacy, "--schema-only")
    assert rc == 2 and "ref_inputs_sha" in out and ("출처" in out or "provenance" in out), (rc, out[-800:])
    # 그리고 **현행 정본은 통과한다** — 이 검사가 "늘 rc 2" 를 재는 것이 아님을 같이 고정한다
    rc, out, _ = _cli("check_u14.py", "--new", ROOT / "out", "--schema-only")
    assert rc == 0, (rc, out[-800:])


# ── R8-03 ────────────────────────────────────────────────────────────────────────────────────
def _shape_harness(monkeypatch, base, offsets):
    """Codex R8 `shape` probe 의 fixture: 실제 reader·Blend·집계·publisher, 전극 로더만 결정적 합성."""
    from bms_balancing.model import Blend
    ns = _load_script("ne_shape")
    u = np.linspace(0.0, 1.0, 301)
    arrays = ((1.0 - u) ** 2, 0.1 + 0.7 * u, 1.0 - u, 0.1 + 0.7 * u)
    blend = Blend(*arrays, window=11, poly_order=3)
    class P:
        def __init__(self, state): self.state = state
        def is_file(self): return True
    class IB:
        def __init__(self, p): self.p = p
        def stream(self): return self.p
        def identity(self): return {"path": self.p.state, "sha256": hashlib.sha256(self.p.state.encode()).hexdigest()}
    class HC:
        def __init__(self, p, **kw): self.state = p.state
        def E_NE(self, x): return blend.E(x, 0.2) + offsets[self.state]
        def E_PE(self, x): return 4.2 - 0.7 * np.asarray(x)
    monkeypatch.setattr(ns.D, "STATES", list(offsets))
    monkeypatch.setattr(ns.D, "data_root", lambda *a, **k: base)
    monkeypatch.setattr(ns.D, "half_cell_path", lambda r, src, state: P(state))
    monkeypatch.setattr(ns.D, "read_input", lambda p: IB(p))
    monkeypatch.setattr(ns.D, "load_literature", lambda *a, **k: arrays)
    monkeypatch.setattr(ns, "HalfCell", HC)
    monkeypatch.setattr(ns, "raw_ne_capacity", lambda p: 1.0)
    return ns


def _pair(matrix_dir, state, **over):
    """짝 하나가 든 **온전한** matrix 묶음. ⚠ Codex R11 P1-7 뒤로 production reader 가 checker 와 같은 validator 를
    쓴다 — 열 몇 개만 맞춘 부분집합은 더 이상 과학 입력이 아니므로 fixture 도 전 열을 채운다."""
    from bms_balancing import schema as _S
    f = matrix_dir / f"matrix_{state}.csv"
    row = matrix_row(gamma_Si="0.25", ref_gamma_Si="0.2", run_id="r8-matrix-" + state, **over)
    verify.atomic_write_csv(f, [row], list(_S.MATRIX_ROW)); _sign(f, row["run_id"], state)
    assert _prov().read_unit(f)[0] is True


def test_d8_03_ne_shape_reports_measured_over_all_states_and_marks_missing_pairs_as_partial(tmp_path, monkeypatch):
    """[Codex R8-03 · P1] state100 은 10 mV 변화 + matrix 짝, state200 은 100 mV 변화인데 matrix 가 아직 없다. CSV 는
    200 행(측정 100, γ 빈칸)을 남기지만 요약은 "측정된 음극 모양 변화 최대 **10.00** mV" 로 끝나고 rc 0 이었다 —
    측정 최대까지 **γ 짝이 있는 부분집합에서** 계산했다.

    닫힘 조건(Codex): 측정 통계는 모든 측정 행에서, γ-짝 통계는 requested/available/paired 를 따로 표시하고, 요청한
    짝 분석에 누락이 있으면 partial/nonzero. 미계산과 '합법 범위를 탐색했으나 증인이 없는 상태' 를 구분한다."""
    base = tmp_path; matrix, out = base / "matrix", base / "shape"; matrix.mkdir()
    ns = _shape_harness(monkeypatch, base, {"pristine": 0.0, "100": 0.01, "200": 0.1})
    _pair(matrix, "100")

    def run(sub=""):
        buf = io.StringIO()
        monkeypatch.setattr(sys, "argv", ["ne_shape.py", "--out-dir", str(matrix), "--write", str(out)])
        with contextlib.redirect_stdout(buf):
            rc = ns.main()
        f = (out / sub / "ne_shape_GITT_Li.csv") if sub else (out / "ne_shape_GITT_Li.csv")   # R9-06: partial 은 별도 namespace
        rows = {r["state"]: r for r in csv.DictReader(io.StringIO(f.read_text(encoding="utf-8")))}
        meta = json.loads(f.with_name(f.name + ".meta.json").read_text(encoding="utf-8"))
        return rc, buf.getvalue(), rows, meta

    rc, text, rows, meta = run("partial")
    assert not (out / "ne_shape_GITT_Li.csv").exists(), "부분 실행이 canonical 자리에 게시됐다 (Codex R9-06)"
    assert float(rows["200"]["measured_shape_mV"]) == 100.0 and rows["200"]["gamma_target"] == ""
    assert "측정된 음극 모양 변화 최대 100.00 mV" in text, text[-1200:]        # 모든 측정 행에서
    assert rc != 0, "γ 짝이 빠졌는데 rc 0"
    assert "1/2" in text and ("짝" in text or "paired" in text), text[-1200:]  # requested/paired 를 말한다
    census = meta.get("pairing") or meta.get("gamma_pairs")
    assert census and census.get("requested") == ["100", "200"] and census.get("paired") == ["100"], meta.get("pairing")
    assert census.get("missing") == ["200"], census
    _pair(matrix, "200")
    rc, text, rows, meta = run()
    assert rc == 0 and "측정된 음극 모양 변화 최대 100.00 mV" in text
    assert (meta.get("pairing") or meta.get("gamma_pairs")).get("missing") == []


# ── R8-04 ────────────────────────────────────────────────────────────────────────────────────
def test_d8_04_profile_rows_carry_the_full_input_identity_not_just_the_log(tmp_path):
    """[Codex R8-04 · P1] profile 의 target/ref **전체** 입력 identity 는 stdout 의 `SUMMARY` 에만 있었고 wrapper 는 그것을
    고정 `.csv.log` 에 쓴다 — 다음 정상 재시도가 실패하면 redirect 가 먼저 log 를 잘라 이전 정상 묶음의 identity 가
    사라진다 (CSV/meta 는 `read_unit` True 인데). aggregate hash 두 개만으로는 어느 입력 역할의 어떤 bytes 였는지 복원할
    수 없다.

    닫힘 조건(Codex): 전체 identity 를 CSV 자체·검증된 meta·CSV 와 원자적으로 게시되는 typed sidecar 중 하나에 둔다.
    실행 log 를 durable receipt 로 쓰지 않는다."""
    root = _synth_root(tmp_path); art = tmp_path / "profile_gamma_200_Li.csv"
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        assert verify.cmd_profile(_args(root, art)) == 0
    summary = json.loads(next(s[8:] for s in buf.getvalue().splitlines() if s.startswith("SUMMARY ")))
    rows = list(csv.DictReader(art.open(encoding="utf-8")))
    assert rows and all(r.get("consumed_inputs") and r.get("ref_consumed_inputs") for r in rows), sorted(rows[0])
    for r in rows:
        assert json.loads(r["consumed_inputs"]) == summary["consumed_inputs"]
        assert json.loads(r["ref_consumed_inputs"]) == summary["ref_consumed_inputs"]
    ref = json.loads(rows[0]["ref_consumed_inputs"])
    assert ref["half_cell"]["path"].endswith("pristine.xlsx") and len(ref["half_cell"]["sha256"]) == 64
    assert json.loads(rows[0]["consumed_inputs"])["half_cell"]["path"].endswith("200.xlsx")
    # log 가 없어도(잘려도) 묶음 자체에서 회수된다
    (tmp_path / "profile_gamma_200_Li.csv.log").write_text("", encoding="utf-8")
    again = list(csv.DictReader(art.open(encoding="utf-8")))
    assert json.loads(again[0]["ref_consumed_inputs"]) == summary["ref_consumed_inputs"]


# ── R8-05 ────────────────────────────────────────────────────────────────────────────────────
def test_d8_05_check_u14_rejects_duplicate_row_keys_instead_of_collapsing_them(tmp_path):
    """[Codex R8-05 · P2] 같은 (half_cell, si, w_dqdv) key 의 행을 하나 더 넣되 **먼저 오는** 중복행의 LLI 를 +3 %p 바꾸면
    `compare_states` 의 폭은 움직이는데 `check_u14` 는 dict comprehension 이 마지막 원본행으로 앞 행을 지워 "전부
    같다" rc 0 이었다.

    닫힘 조건(Codex): dict 변환 전에 key 유일성·행 수·정확한 key 집합을 검사한다."""
    old, new = tmp_path / "old", tmp_path / "new"; old.mkdir(); new.mkdir()
    rows = _full_matrix_rows("r8-rows-A")
    f_old = old / "matrix_100.csv"; verify.atomic_write_csv(f_old, rows, list(rows[0])); _sign(f_old, "r8-rows-A", "100", full=True)
    changed = [dict(r) for r in rows]
    original = dict(changed[0])
    # ⚠ Codex R13 P1-1 뒤 fixture 가 2 행 → 정본 32 행이다. 최솟값 행에 +5 를 하면 폭이 오히려 **줄어**
    #   방향이 뒤집힌다 — 모집단 크기와 무관하게 폭이 커지도록 그 행을 최댓값 위로 올린다.
    changed[0]["LLI_pct"] = str(float(changed[0]["LLI_pct"]) + 50.0)
    changed.append(original)                                             # 마지막에 원본 중복행
    for r in changed:
        r["run_id"] = "r8-rows-B"
    f_new = new / "matrix_100.csv"; verify.atomic_write_csv(f_new, changed, list(changed[0])); _sign(f_new, "r8-rows-B", "100", full=True)
    rc, out, _ = _cli("check_u14.py", "--new", new, "--old", old)
    assert rc != 0 and "전부 같다" not in out, (rc, out)
    assert "중복" in out and "GITT" in out, out
    cs = _cs()
    assert cs.load_matrix_axis(new)["100"]["per"]["GITT"]["LLI"] > cs.load_matrix_axis(old)["100"]["per"]["GITT"]["LLI"] + 2


# ── R8-06 ────────────────────────────────────────────────────────────────────────────────────
def test_d8_06_mutation_audit_treats_an_empty_selection_as_an_audit_error(monkeypatch, capsys):
    """[Codex R8-06 · P2] selector 가 시험을 하나도 고르지 못하면 pytest 는 rc 5 인데 감사는 `rc != 0` 을 CAUGHT 로 세었다
    (`c6_DOES_NOT_EXIST` → "CAUGHT … 52 deselected", MISSED 0, rc 0). selector 오타·rename·수집 실패가 assertion
    검출과 구분되지 않는다.

    닫힘 조건(Codex): 선택된 시험 수 > 0 을 확인하고, rc 5·수집/실행 오류를 CAUGHT 가 아닌 감사 오류로 분류한다."""
    mod = _mod("r6_audit_r8", ROOT / "reviews/r6_repros/codex_r6_mutation_audit.py")
    calls = []
    def fake_run(k):
        calls.append(k)
        if k == "c6_0 or c6_q3":
            return 0, "7 passed, 45 deselected in 4.0s"
        return 5, "52 deselected in 1.0s"                                 # 아무 시험도 안 골라졌다
    monkeypatch.setattr(mod, "run", fake_run)
    monkeypatch.setattr(mod, "MUTATIONS", [("무해한 주석", "c6_DOES_NOT_EXIST", "scripts/provenance.py",
                                            "def read_unit(", "def read_unit(  # noqa (감사 자기시험)\n")])
    before = (ROOT / "scripts/provenance.py").read_bytes()
    rc = mod.main()
    out = capsys.readouterr().out
    assert (ROOT / "scripts/provenance.py").read_bytes() == before
    assert rc != 0 and not [l for l in out.splitlines() if l.startswith("CAUGHT")], out
    assert "오류" in out and "선택" in out, out
    # 실제 pytest 가 빈 선택에 주는 rc 5 를 분류기가 오류로 읽는다
    assert mod.classify(5, "52 deselected in 1.0s") == "오류"
    assert mod.classify(1, "1 failed, 51 deselected in 1.4s") == "CAUGHT"
    assert mod.classify(0, "1 passed, 51 deselected in 1.4s") == "MISSED"
    assert mod.classify(2, "ERROR collecting tests/test_r6_internal.py") == "오류"


# ── R8-07 ────────────────────────────────────────────────────────────────────────────────────
def test_d8_07_r7_closure_runner_records_whether_each_probe_reached_its_counterexample_assertion():
    """[Codex R8-07 · P2] 보관한 R7 probe 는 SHA 를 고정해 두어 현재 트리에서는 첫 assertion 에서 rc 1 — 그것은 옳지만,
    요청문이 주장한 "수정 뒤 각 probe 가 자기 반례 assertion 에서 실패한다" 를 **재생할 명령이 없었다**.

    닫힘 조건(Codex): 원본 pinned probe 는 보존하고 R8 용 closure runner 를 따로 둔다 — 대상 검증 뒤 실제 case 에
    도달했는지 · 반례 assertion 에서 실패했는지 · positive closure 가 성립했는지를 **별도 상태**로 기록한다."""
    runner = ROOT / "reviews/r7_repros/replay_codex_r7.py"
    assert runner.is_file(), "R7 closure runner 가 없다"
    head = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    r = subprocess.run([sys.executable, str(runner), "--target", str(ROOT), "--probes", "R7-01,R7-06",
                        "--expected-head", head, "--allow-dirty"],              # R9 P2-2: 대상 SHA 를 명시, 시험 중 트리는 dirty
                       cwd=ROOT, capture_output=True, text=True, timeout=600)
    # ⚠ 자체 리뷰 C19 뒤: 종료 코드가 `evidence_eligible` 을 반영한다 — 개발 중 트리에서는 도구 자신이
    #   HEAD 의 blob 과 달라 eligible false 가 정상이다. 계약으로 단언한다 (증거면 0, 아니면 3).
    _d = json.loads(r.stdout)
    assert r.returncode == (0 if _d["evidence_eligible"] else 3), (r.returncode, r.stderr[-800:])
    d = json.loads(r.stdout)
    assert d["target_head"] and d["pinned_sha"].startswith("521be85") and d["pin_bypassed"] is True
    for pid in ("R7-01", "R7-06"):
        p = d["probes"][pid]
        assert p["도달"] is True, (pid, p)                                  # 대상 검증을 지나 실제 case 에 닿았다
        assert p["상태"] == "반례 소멸", (pid, p)                             # 자기 반례 assertion 에서 멈췄다
        assert "assert" in p["멈춘_곳"], (pid, p)


# ── R8-08 ────────────────────────────────────────────────────────────────────────────────────
def test_d8_08_hook_counts_publications_separately_and_c6_01_asserts_them_per_schedule(tmp_path, monkeypatch):
    """[Codex R8-08 · P2] `fired["v"]` 는 callback 횟수가 아니라 **읽기** 횟수라 metadata 두 schedule 의 callback 을 꺼도
    `test_c6_01` 이 통과했다 — 다른 schedule 의 관측이 필요한 B/B·미완을 대신 채운다.

    닫힘 조건(Codex): callback 에서 별도 publication count 를 세고 각 case 가 자기 callback 을 정확히 실행했음을
    assert 한다; schedule 별 예상 publication ID 와 관측을 따로 기록한다."""
    f = tmp_path / "a.txt"; f.write_text("x", encoding="utf-8")
    with monkeypatch.context() as mp:
        c = _hook_open(mp, "a.txt", 1, lambda: None)
        f.read_text(encoding="utf-8"); f.read_text(encoding="utf-8")
    assert c["v"] == 2 and c["published"] == 1, c                          # 읽기 2 · 게시 1 — 따로 센다
    with monkeypatch.context() as mp:
        c = _hook_open(mp, "a.txt", 5, lambda: None)
        f.read_text(encoding="utf-8")
    assert c["v"] == 1 and c["published"] == 0, c
    src = (ROOT / "tests/test_r6_internal.py").read_text(encoding="utf-8")
    body = src[src.index("def test_c6_01_"):src.index("def test_c6_02_")]
    assert 'fired["published"] == 1' in body, "c6_01 이 건별 게시 횟수를 assert 하지 않는다"
    assert "schedules" in body or "schedule" in body                      # schedule 별 관측 기록
    # c6_04 의 변이는 KeyError 가 아니라 **옛 값의 소비**로 잡혀야 한다 (R7·R8 이 두 번 짚음)
    audit = _mod("r6_audit_c604", ROOT / "reviews/r6_repros/codex_r6_mutation_audit.py")
    what, k, rel, old, new = next(m for m in audit.MUTATIONS if m[1] == "c6_04")
    mutated = tmp_path / "compare_states_mut.py"
    mutated.write_text(audit.apply((ROOT / rel).read_text(encoding="utf-8"), old, new), encoding="utf-8")
    mm = _mod("cs_mut", mutated)
    d = tmp_path / "out"; d.mkdir()
    from test_r6_internal import _c6_deg
    _c6_deg(d, "rid-new", 111.0)
    (d / "degeneracy_100_Li_v2.json").write_text(json.dumps({"state": "100", "best_modes_percent": {},
        **{f"{k}_percent": {"span": 222.0} for k in ("LAM_PE", "LAM_NE", "LLI")}}), encoding="utf-8")
    with contextlib.redirect_stderr(io.StringIO()):
        got = mm.load_degeneracy(d)
    assert "100" in got and got["100"]["j"]["LLI_percent"]["span"] == 222.0, got.get("100", {}).get("file")


# ── 문서 ─────────────────────────────────────────────────────────────────────────────────────
def test_d8_09_docs_record_the_r8_closure_and_limit_the_canonical_to_provenance_incomplete():
    led = _live(_doc("reviews/R6_LEDGER.md"))
    assert "Codex R8" in led and "R8-01" in led and "R8-08" in led
    for name in ("WORKING_STATE.md", "reviews/R9_REQUEST.md"):
        live = _live(_doc(name))
        assert "provenance-incomplete" in live or "출처 미완" in live, name   # 현행 정본의 범위 제한
        assert "U18" in live, name                                        # 재실행으로 보강하는 실측 항목
    assert "값으로 잡힌다" not in led.split("Codex R8")[0].split("Codex R7")[-1] or "KeyError" in led, \
        "c6_04 '값으로 잡힌다' 주장이 정정 없이 남아 있다"
