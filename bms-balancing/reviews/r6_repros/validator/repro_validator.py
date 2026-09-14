#!/usr/bin/env python3
"""R6 내부 적대적 리뷰 — 렌즈: validator 우회 (형식은 맞는데 의미가 틀린 산출물이 통과하는 경로).

대상: bms-balancing @ 1049894. 발견마다 함수 하나 — **잘못된 결과가 재현되면 assert 가 통과**한다
(수정 뒤에는 assert 가 실패해야 정상). 실행: python3 repro_validator.py [--case NAME]
tracked 파일은 건드리지 않는다 — 모든 산출은 mktemp 안.
"""
import sys, io, json, os, shutil, pathlib, subprocess, tempfile, textwrap, contextlib, argparse
ROOT = "/home/user/Yonghoon-DEM-DFT/bms-balancing"
sys.path.insert(0, ROOT); sys.path.insert(0, ROOT + "/scripts")
from bms_balancing import verify
from bms_balancing.verify import ANCHOR_STAGE, DD_EVAL_P
import provenance as pv

TMP = pathlib.Path(tempfile.mkdtemp(prefix="r6_validator_"))
COLS = ["rmse_pocv", "rmse_dvdq", "rmse_dqdv", "rmse_dqdv_w"]
P = [list(p) for p in DD_EVAL_P]
ANCHORS = {k: 1.0 for k, _ in ANCHOR_STAGE}; ANCHORS["dv_n"] = 350.0
# Python 값은 [0.0116, 0.0122], MATLAB 값은 +0.0002 — 둘 다 %.2g 로 '0.012' 지만 상대차 최대 1.7 % (MODEL_REL 의 1.7e7 배)
PY = {c: [0.0116 + 0.00002 * i + 0.0001 * j for i in range(len(P))] for j, c in enumerate(COLS)}
ML = {c: [x + 0.0002 for x in PY[c]] for c in COLS}
GAP = max(abs(ML[c][i] - PY[c][i]) / PY[c][i] for c in COLS for i in range(8))
assert GAP > 1e-2 and all(format(PY[c][i], ".2g") == format(ML[c][i], ".2g") for c in COLS for i in range(8))


def make_csv(name, head=("# printed_format,%.17g",), header="top", fmt=".17g", n_cols=4, anchors=True, extra_row=None):
    """dd_eval.m 모양 CSV. header: 'top' | 'bottom' | None. n_cols: rmse 열 수. extra_row: 헤더 앞에 끼울 원문 행."""
    lines = list(head) + ([f"# {k},{v:.17g}" for k, v in ANCHORS.items()] if anchors else [])
    hdr = "a_PE,b_PE,a_NE,b_NE,gamma_Si" + ("," + ",".join(COLS[:n_cols]) if n_cols else "")
    body = [",".join([format(x, ".6f") for x in p] + [format(ML[c][i], fmt) for c in COLS[:n_cols]]) for i, p in enumerate(P)]
    if extra_row:
        body.insert(0, extra_row)
    if header == "top":
        lines += [hdr] + body
    elif header == "bottom":
        lines += body + [hdr]
    else:
        lines += body
    p = TMP / name; p.write_text("\n".join(lines) + "\n", encoding="utf-8"); return p


def compare(path, **kw):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        res = verify._compare_dd_eval(dict(ANCHORS), P, PY, path, **kw)
    return res, buf.getvalue()


_DRIVER = TMP / "driver.py"
_DRIVER.write_text(textwrap.dedent(f"""
    import sys, json
    sys.path.insert(0, {ROOT!r})
    from unittest.mock import patch
    from bms_balancing import verify
    an = json.loads(sys.argv[1]); py = json.loads(sys.argv[2]); P = {P!r}
    class Obj:
        def _at(self, p, col): return py[col][P.index([float(x) for x in p])]
        def rmse_pocv(self, p): return self._at(p, "rmse_pocv")
        def rmse_dvdq(self, p): return self._at(p, "rmse_dvdq")
        def rmse_dqdv(self, p, weighted=False): return self._at(p, "rmse_dqdv_w" if weighted else "rmse_dqdv")
    with patch.object(verify.D, "data_root", return_value=None), \\
         patch.object(verify, "build", return_value=Obj()), \\
         patch.object(verify, "dd_eval_anchors", return_value=list(an.items())):
        sys.exit(verify.main(["eval", "--compare", sys.argv[3]] + sys.argv[4:]))
"""), encoding="utf-8")


def cli(path, *extra):
    """`python3 -m bms_balancing.verify eval --compare <csv> …` 와 같은 경로 (test_r3_07 방식의 mock)."""
    r = subprocess.run([sys.executable, str(_DRIVER), json.dumps(ANCHORS), json.dumps(PY), str(path), *extra],
                       capture_output=True, text=True, encoding="utf-8", cwd=ROOT)
    return r.returncode, r.stdout + r.stderr


def verdict_lines(out):
    return [l for l in out.splitlines() if l.startswith(("판정", "종료 코드", "!")) or "Error" in l][-2:]


# ═══════════════════════════════════════════════════════════════════════════════════════════════
def v01_header_after_rows_skips_token_audit():
    """V6-01 · 헤더가 데이터 행 **뒤**에 있으면 audit 의 행별 검사(선언 형식 재출력 · 열 수)가 전부 건너뛰어진다.
    같은 내용으로 헤더가 위면 invalid(2), 아래면 complete(0) — 선언 %.2g 아래 17 자리 토큰, 상대차 1.7 %."""
    top = make_csv("v01_top.csv", head=("# printed_format,%.2g",), header="top")
    bottom = make_csv("v01_bottom.csv", head=("# printed_format,%.2g",), header="bottom")
    rc_top, out_top = cli(top); rc_bot, out_bot = cli(bottom)
    print(f"  header top    -> rc={rc_top} {verdict_lines(out_top)}")
    print(f"  header bottom -> rc={rc_bot} {verdict_lines(out_bot)}")
    print(f"  audit(top)={verify.dd_eval_csv_audit(top, spec=('sig', 2))[:1]}\n  audit(bottom)={verify.dd_eval_csv_audit(bottom, spec=('sig', 2))}")
    # 열 수 검사도 같이 빠진다: 헤더 앞의 10 칸 행(헤더는 9 열)이 문제로 잡히지 않는다
    wide = make_csv("v01_wide.csv", head=("# printed_format,%.17g",), header="bottom",
                    extra_row=",".join([format(x, ".6f") for x in P[0]] + [format(ML[c][0], ".17g") for c in COLS] + ["9.9"]))
    print(f"  audit(10-field row before header)={verify.dd_eval_csv_audit(wide, spec=('exact', 17))}")
    assert rc_top == 2 and rc_bot == 0 and "complete" in out_bot and GAP > 1e-2
    assert verify.dd_eval_csv_audit(wide, spec=("exact", 17)) == []


def v02_precision_option_is_never_audited_against_tokens():
    """V6-02 · `--precision` 옵션은 토큰과 대조되지 않는다. 선언이 없거나(B1) 해석 불가(B2)·숫자(B3)면
    17 자리 토큰을 `sig:2` 구간으로 판정해 complete(0). 선언이 `%.17g` 면 같은 옵션이 partial(3) — 대조군."""
    undecl = make_csv("v02_undecl.csv", head=())
    bad = make_csv("v02_e17.csv", head=("# printed_format,%.17e",), fmt=".17e")
    num = make_csv("v02_num.csv", head=("# printed_format,17",))
    good = make_csv("v02_g17.csv", head=("# printed_format,%.17g",))
    rcs = {}
    for label, path, opt in [("no declaration", undecl, "sig:2"), ("declaration %.17e (unparseable)", bad, "sig:2"),
                             ("declaration '17' (numeric)", num, "sig:2"), ("no declaration, fixed:0", undecl, "fixed:0"),
                             ("CONTROL declaration %.17g", good, "sig:2")]:
        rc, out = cli(path, "--precision", opt); rcs[label] = rc
        print(f"  {label:<36} --precision {opt:<7} -> rc={rc} {verdict_lines(out)}")
    assert rcs["no declaration"] == 0 and rcs["declaration %.17e (unparseable)"] == 0 and rcs["declaration '17' (numeric)"] == 0
    assert rcs["no declaration, fixed:0"] == 0 and rcs["CONTROL declaration %.17g"] == 3


def v03_headerless_file_skips_audit_and_allow_partial_passes():
    """V6-03 · 헤더 없는 파일: 토큰 audit·파라미터 열 검사가 없고 앞 두 열을 위치로 rmse 로 본다.
    선언 %.2g + 17 자리 토큰(헤더가 있으면 invalid) → partial(3) → `--allow-partial` 로 0."""
    p = make_csv("v03_nohdr.csv", head=("# printed_format,%.2g",), header=None)
    rc3, out3 = cli(p); rc0, out0 = cli(p, "--allow-partial")
    print(f"  no header              -> rc={rc3} {verdict_lines(out3)}")
    print(f"  no header + allow-part -> rc={rc0} {verdict_lines(out0)}")
    print(f"  audit={verify.dd_eval_csv_audit(p, spec=('sig', 2))}")
    assert rc3 == 3 and rc0 == 0 and "rmse 16개" in out0


def v04_zero_shared_columns_and_zero_anchors_pass_with_allow_partial():
    """V6-04 · rmse 열이 **하나도** 없는 파일(헤더 = 파라미터 다섯뿐)도 '옛 스키마' 로 partial → `--allow-partial` 로 0.
    앵커까지 없으면 '앵커 0개와 rmse 0개가 전부 일치' 로 0 — 아무것도 비교하지 않은 파일이 성공이다."""
    only_params = make_csv("v04_params.csv", n_cols=0)
    bare = make_csv("v04_bare.csv", n_cols=0, anchors=False)
    rc_a, out_a = cli(only_params, "--allow-partial"); rc_b, out_b = cli(bare, "--allow-partial")
    res_b, _ = compare(bare)
    print(f"  params+anchors, 0 rmse cols   -> rc={rc_a} {verdict_lines(out_a)}")
    print(f"  params only (no anchors)      -> rc={rc_b} {verdict_lines(out_b)}")
    print(f"  compared={res_b['compared']}/{res_b['expected']} anchors={res_b['anchors_compared']}/{res_b['anchors_expected']} status={res_b['status']}")
    assert rc_a == 0 and rc_b == 0 and "rmse 0개" in out_a and "앵커 0개와 rmse 0개" in out_b
    assert res_b["compared"] == 0 and res_b["anchors_compared"] == 0


def v05_verify_unit_does_not_bind_meta_to_filename():
    """V6-05 · `verify_unit` 은 meta 의 run_id·sha256 만 본다. 산출물+meta 를 **다른 상태의 이름**으로 복사하면
    meta 는 artifact=matrix_100.csv·state=100 이라 말하는데 `--verify-unit matrix_200.csv` 가 0 (일치)."""
    rid = "a" * 32
    a = TMP / "matrix_100.csv"
    a.write_text("half_cell,si,w_dqdv,run_id,LLI_pct\n" + "\n".join([f"GITT,Li,0.0,{rid},3.1"] * 3) + "\n", encoding="utf-8")
    (TMP / "matrix_100.csv.meta.json").write_text(json.dumps({"artifact": "matrix_100.csv", "state": "100", "run_id": rid, "sha256": pv.sha256_file(a)}))
    b = TMP / "matrix_200.csv"; shutil.copy(a, b); shutil.copy(str(a) + ".meta.json", str(b) + ".meta.json")
    r = subprocess.run([sys.executable, ROOT + "/scripts/provenance.py", "--verify-unit", str(b)], capture_output=True, text=True)
    print(f"  --verify-unit matrix_200.csv -> rc={r.returncode} {r.stdout.strip()!r}; meta says {json.loads((TMP / 'matrix_200.csv.meta.json').read_text())['artifact']!r}")
    assert r.returncode == 0 and pv.verify_unit(b) == (True, "일치")


def v06_numeric_declaration_is_treated_as_absent_not_invalid():
    """V6-06 · `# printed_format,17` — audit 는 선언으로 세지만(n_decl) meta 리더는 숫자라 버린다 → '선언 없음' 으로
    추정(partial) 이 되고, `--precision` 을 주면 선언이 있었다는 말 없이 옵션이 대체된다. 정책은 '해석 못 하는 선언 = invalid'."""
    p = make_csv("v06_num.csv", head=("# printed_format,17",))
    pol = verify.resolve_precision(p); rc, out = cli(p)
    print(f"  resolve_precision: source={pol['source']!r} declared_raw={pol['declared_raw']!r}; declared_precision()={verify.declared_precision(p)!r}")
    print(f"  auto -> rc={rc} {verdict_lines(out)}")
    assert pol["source"] == "inferred" and pol["declared_raw"] is None and rc != 2


def v07_unreadable_compare_path_exits_1_like_a_mismatch():
    """V6-07 · `--compare` 경로가 없거나 디렉터리면 OSError 가 잡히지 않아 traceback 으로 종료 1 — README 의 '1 = 갈림'."""
    rc1, out1 = cli(TMP / "does_not_exist.csv"); rc2, out2 = cli(TMP)
    print(f"  missing file -> rc={rc1} {verdict_lines(out1)}\n  directory    -> rc={rc2} {verdict_lines(out2)}")
    assert rc1 == 1 and rc2 == 1 and "FileNotFoundError" in out1 and "종료 코드" not in out1


def v08_check_run_id_duplicate_run_id_columns_last_wins():
    """V6-08 (사소) · CSV 에 `run_id` 열이 둘이면 DictReader 는 마지막 열만 본다 — 첫 열이 다른 시도의 id 여도 통과."""
    rid = "a" * 32
    p = TMP / "dup_run_id.csv"; p.write_text("run_id,half_cell,run_id\n" + "\n".join([f"{'b' * 32},GITT,{rid}"] * 2) + "\n")
    ok = pv.check_run_id(p, rid); print(f"  check_run_id -> {ok}; first column = {'b' * 8}…")
    assert ok == (True, "전 행 일치")


def v09_signed_zero_token_is_a_false_model_mismatch():
    """V6-09 (사소·fail-closed) · 토큰 '0.000000' 와 Python -1e-20 (또는 '-0.000000' 와 +1e-20) 은 같은 문자열로 안 찍혀
    excess=1e-20, eff = excess/|pv| = 1 → '모델 차이'. 부호 있는 0 의 구간 경계가 값 0 에서 상대 정규화와 만난다."""
    ex = verify.token_excess(("fixed", 6), 0.0, -1e-20); eff = ex / max(1e-20, 1e-30)
    print(f"  token '0.000000' vs pv=-1e-20: excess={ex:.3g} eff={eff:.3g} (MODEL_REL={verify.MODEL_REL:.0e})")
    assert eff > verify.MODEL_REL


def controls_fail_closed():
    """시도했지만 fail-closed 였던 것 — 발견 아님 (보고서 '시도한 것')."""
    rows = []
    inv = make_csv("ctl_invalid.csv", head=("# printed_format,%.2g",)); rc, _ = cli(inv, "--allow-partial"); rows.append(("--allow-partial + invalid", rc))
    mm = dict(ANCHORS); mm["c_cell"] = 2.0
    with contextlib.redirect_stdout(io.StringIO()):
        res = verify._compare_dd_eval(mm, P, PY, inv)
    rows.append(("anchor mismatch + malformed", res["status"]))
    old = make_csv("ctl_old.csv", n_cols=2); res, _ = compare(old); rows.append(("partial(schema) + model gap 1.7 %", res["status"]))
    e = make_csv("ctl_e.csv", head=("# printed_format,%.17e",), fmt=".17e"); res, _ = compare(e); rows.append(("declaration %e, auto", res["status"]))
    expf = TMP / "ctl_expf.csv"; expf.write_text("\n".join(["# printed_format,%.10f"] + [f"# {k},1" for k, _ in ANCHOR_STAGE] + ["a_PE,b_PE,a_NE,b_NE,gamma_Si,rmse_pocv", "1,2,3,4,5,1e-05"]) + "\n")
    rows.append(("exponent token under %.10f", "invalid" if verify.dd_eval_csv_audit(expf, spec=("fixed", 10)) else "passes"))
    rid = "a" * 32
    for label, text, suffix in [("run_id 열 값이 빈 문자열", "half_cell,run_id\nGITT,\nGITT,\n", ".csv"), ("run_id 열만 있고 행 0", "half_cell,run_id\n", ".csv"),
                                ("JSON 이 list", json.dumps([{"run_id": rid}]), ".json"), (".json.log 확장자", f"run_id {rid}\n", ".json.log")]:
        q = TMP / ("ctl_" + label.replace(" ", "_") + suffix); q.write_text(text); rows.append((label, pv.check_run_id(q, rid)[0]))
    j = TMP / "ctl_unit.json"; j.write_text(json.dumps({"run_id": rid, "k": 1})); o = TMP / "ctl_other.json"; o.write_text(json.dumps({"run_id": rid, "k": 2}))
    (TMP / "ctl_unit.json.meta.json").write_text(json.dumps({"run_id": rid, "sha256": pv.sha256_file(o)})); rows.append(("meta sha256 가 다른 파일의 것", pv.verify_unit(j)[0]))
    ln = TMP / "ctl_link.json"; os.symlink(j, ln); rows.append(("symlink (meta 는 링크 옆에 없음)", pv.verify_unit(ln)[0]))
    import random, struct, math; random.seed(0)
    bad = sum(1 for _ in range(100000) for x in [struct.unpack("<d", struct.pack("<Q", random.getrandbits(64)))[0]] if math.isfinite(x) and float(format(x, ".17g")) != x)
    rows.append(("%.17g 왕복 실패 / 100k 무작위 double", bad))
    for label, val in rows:
        print(f"  {label:<40} -> {val}")


CASES = {f.__name__.split("_")[0]: f for f in (v01_header_after_rows_skips_token_audit, v02_precision_option_is_never_audited_against_tokens,
                                                 v03_headerless_file_skips_audit_and_allow_partial_passes, v04_zero_shared_columns_and_zero_anchors_pass_with_allow_partial,
                                                 v05_verify_unit_does_not_bind_meta_to_filename, v06_numeric_declaration_is_treated_as_absent_not_invalid,
                                                 v07_unreadable_compare_path_exits_1_like_a_mismatch, v08_check_run_id_duplicate_run_id_columns_last_wins,
                                                 v09_signed_zero_token_is_a_false_model_mismatch)}
CASES["controls"] = controls_fail_closed

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--case", choices=list(CASES)); args = ap.parse_args()
    print(f"target {ROOT}  HEAD {subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT, capture_output=True, text=True).stdout.strip()}  tmp {TMP}  gap {GAP:.3%}")
    failed = 0
    for name, fn in ([(args.case, CASES[args.case])] if args.case else CASES.items()):
        print(f"\n== {name}: {fn.__doc__.splitlines()[0]}")
        try:
            fn(); print(f"   -> {'재현됨 (잘못된 결과가 아직 있다)' if name != 'controls' else '기록'}")
        except AssertionError as e:
            failed += 1; print(f"   -> 재현 안 됨 (수정된 뒤라면 정상): {e!r}")
    sys.exit(1 if failed else 0)
