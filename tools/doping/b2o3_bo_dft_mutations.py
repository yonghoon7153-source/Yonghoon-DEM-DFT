#!/usr/bin/env python3
"""b2o3_bo_dft.py 의 깨기 (변이) 시험 — 검사 한 줄씩 끄고 그 도구의 selftest 가 빨개지는지 본다 (Codex EF · EG 재현용).

  python3 b2o3_bo_dft_mutations.py --selftest   # 정적 검사 (몇 초) — 변이 대상 문자열이 도구에 정확히 한 번씩 있고 · 바꾼 소스가 문법상 맞는지
                                                #   + 음성 (없는 대상 · 두 번 있는 대상 · 문법이 깨지는 변이를 잡는지)
  python3 b2o3_bo_dft_mutations.py              # 변이 전부 실행 (73 개 · 약 6 분 · CPU 1 코어) → '깨기 N/N 빨강'

변이마다 도구를 고친 사본 tools/doping/_mut_dft.py 를 만들어 '--selftest' 를 돌리고 지운다 (판독기 · host 구조를 같은 상대 경로로
찾게 같은 폴더에 둔다). 빨강 = selftest 가 'N/N' 이 아님 (crash 포함) · 줄마다 처음 ✗ 난 시험 이름을 같이 찍는다 — crash 가 그 변이의
자기 시험 때문인지 볼 수 있게.

⛔ 이 도구가 못 하는 것
  · 검사 '모든' 경로를 덮는다고 보증하지 않는다 — 목록에 있는 검사 줄만 끈다 (새 검사를 넣으면 목록에 더한다).
  · 빨강의 이유를 판정하지 않는다 — 처음 ✗ 이름을 보여 줄 뿐이다 (crash 는 ✗ 없이 끝날 수 있다).
  · 실제 QE 출력에 대한 검사가 아니다 — 도구 selftest 의 가짜 출력 · 가짜 판독기 (_FakeRD) 위에서 돈다.
"""
from __future__ import annotations

import ast
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL = HERE / "b2o3_bo_dft.py"
MUT = HERE / "_mut_dft.py"

M = [
 # ── 출력 검사 (out_problems) ──
 ("바이트 손상", 'if o["decode_error"]:', 'if False:'),
 ("실행 수", 'if o["n_runs"] != 1:', 'if False:'),
 ("JOB DONE 수", 'if o["n_job_done"] != 1 or not o["job_done"]:', 'if False:'),
 ("설정 줄 한 번", '    many = {k: c for k, c in o["once"].items() if c != 1}', '    many = {}'),
 ("JOB DONE 뒤 기록", '    if o["after_done"]:', '    if False:'),
 ("SCF '!' 한 번", '    elif stage != "relax" and o["n_scf"] != 1:', '    elif False:'),
 ("이완 '!' 수 = BFGS", '        elif o["n_scf"] != o["bfgs"]["scf_cycles"]:', '        elif False:'),
 ("SCF 수렴", 'if not o["scf_converged"]:', 'if False:'),
 ("입력 이름", 'if o["input_name"] != "scf.in":', 'if False:'),
 ("ecut", 'if o[k] is None or abs(o[k] - DFT[k]) > TOL["ecut"]:', 'if False:'),
 ("conv_thr", 'if o["conv_thr"] is None or abs(o["conv_thr"] / DFT["conv_thr"] - 1) > TOL["conv_rel"]:', 'if False:'),
 ("smearing", 'if o["smearing"] != DFT["smearing"] or o["degauss"] is None', 'if False and o["degauss"] is None'),
 ("교환상관", 'if o["xc"] is None or o["xc"][:4] != ["SLA", "PW", "PBX", "PBC"]:', 'if False:'),
 ("스핀", '    if o["spin_polarized"]:\n', '    if False:\n'),
 ("PP md5", 'if d and (d["file"] != PP[el] or d["md5"] != pl.get("md5")):', 'if False:'),
 ("Zval", 'if d and (d["zval"] is None or pl.get("z_valence") is None or abs(d["zval"] - pl["z_valence"]) > TOL["zval"]):', 'if False:'),
 ("전자 수", 'if o["nelec"] is None or abs(o["nelec"] - expect) > TOL["nelec"]:', 'if False:'),
 ("셀 축", 'if o["cell_A"] is None or np.abs(np.asarray(o["cell_A"]) - cin).max() > TOL["cell_A"]:', 'if False:'),
 ("처음 좌표", 'elif np.abs(np.asarray(ini["cart_A"]) - np.asarray(inp["frac"], float) @ cin).max() > TOL["pos_A"]:', 'elif False:'),
 ("prefix", 'if o["prefixes"] and o["prefixes"] != [inp["keys"].get("prefix")]:', 'if False:'),
 ("k shift", 'if inp.get("k_shift") != [0, 0, 0]:', 'if False:'),
 ("k 격자 호출", '    q += kmesh_problems(o, inp["k"])', '    q += []'),
 ("힘 블록", '    if (not o["forces_block"]', '    if False and (not o["forces_block"]'),
 ("이완 설정 한 번", '        many = {k: c for k, c in o["once_relax"].items() if c != 1}', '        many = {}'),
 ("BFGS 기준", '        if (c is None or abs(c[0]', '        if False and (c is None or abs(c[0]'),
 ("이완 문턱", '        if (o["etot_thr"] is None', '        if False and (o["etot_thr"] is None'),
 ("nstep", 'if o["nstep"] != R["nstep"]:', 'if False:'),
 ("힘 성분", 'if fm is not None and fm > R["forc_conv_thr"] + TOL["force_print"]:', 'if False:'),
 ("bfgs", '        if o["bfgs"] is None:', '        if False:'),
 ("최종 좌표", 'if o["final"] is None or len(o["final"]["symbols"]) != DFT["nat"]:', 'if False:'),
 ("Final energy", 'if o["final_E_Ry"] is None or o["E_Ry"] is None or abs(o["final_E_Ry"] - o["E_Ry"]) > TOL["E_final_Ry"]:', 'if False:'),
 ("응력 뒤", 'if o["P_kbar"] is None or o["E_last_at"] is None or o["P_at"] < o["E_last_at"]:', 'if False:'),
 ("부피", 'if V0 is None or o["volume_A3"] is None or abs(o["volume_A3"] - V0) > TOL["V_A3"]:', 'if False:'),
 # ── k 격자 (kmesh_problems) ──
 ("격자 밖", '        if np.abs(x - np.round(x)).max() > TOL["k_grid"]:', '        if False:'),
 ("가중치 몫", '        if abs(m - round(m)) > TOL["k_weight"] or int(round(m)) not in (1, 2):', '        if False:'),
 ("−k 둘 몫", '        if int(round(m)) == 2 and g == gm:', '        if False:'),
 ("정확히 덮음", '    if set(cover) != full or any(c != 1 for c in cover.values()) or abs(wsum - 2.0) > TOL["k_weight"] * N:', '    if False:'),
 # ── 단계 출력 (read_stage_outputs) ──
 ("누락", '    if missing:\n        raise SystemExit(f"⛔ {stage} 출력 누락', '    if False:\n        raise SystemExit(f"⛔ {stage} 출력 누락'),
 ("입력 sha", 'if not fin.is_file() or _sha(fin) != j["input_sha256"]:\n            bad.append', 'if not fin.is_file():\n            bad.append'),
 ("판 갈림", '    if len(vers) != 1:', '    if False:'),
 # ── 유사포텐셜 ──
 ("원소 머리", '        if e != el:', '        if False:'),
 ("가전자 못 읽음", '        if z is None or not math.isfinite(z) or z <= 0:', '        if False:'),
 ("유사포텐셜 다시 기록", '    if pseudo_record(plan["pseudo"]["dir"]) != plan["pseudo"]:', '    if False:'),
 # ── 8 단계 · 계획 다시 결속 ──
 ("본 판독 core", '    if RD._core(got) != RD._core(A100):\n        raise SystemExit("⛔ 본 판독 파일이', '    if False:\n        raise SystemExit("⛔ 본 판독 파일이'),
 ("보류", '    if A100.get("hold_reasons"):', '    if False:'),
 ("성공 목록 대조", 'if not S or (fa.get("min") or {}).get("name") != S[0]["name"] or fa.get("n_success") != len(S):', 'if not S:'),
 ("고르기 대조", '    if want != got:', '    if False:'),
 ("구조 다시 찾기", '        if _entry(p, base) != j["structure"]:', '        if False:'),
 ("k_main 자격 (다시 결속)", '    _k_main_check(RD, plan.get("k_main") or [], plan.get("after_kprobe"), base, plan["inputs"]["anneal_results"]["sha256"])', '    pass'),
 ("섞인 계획", '        if after_entry:\n            raise SystemExit("⛔ k_main 3×2×1 판에', '        if False:\n            raise SystemExit("⛔ k_main 3×2×1 판에'),
 ("발동 아님", '    if not kv.get("triggered"):\n        raise SystemExit("⛔ after_kprobe 판정이 발동이 아니다', '    if False:\n        raise SystemExit("⛔ after_kprobe 판정이 발동이 아니다'),
 ("다른 8 단계 결과", '    if (kv.get("stage8") or {}).get("anneal_results_sha256") != results_sha:', '    if False:'),
 ("발동 근거 다시", '    _rebind_kp(RD, kp_path, None)                # 발동', '    pass                # 발동'),
 ("도구 sha", '    if (t.get("dft_tool") or {}).get("sha256") != _tool_fp()["sha256"]:', '    if False:'),
 ("계약 같음", '    if plan.get("contract") != json.loads(json.dumps(DFT)):', '    if False:'),
 ("단일점 입력 다시", '        if _text_sha(exp[j["job"]]) != j["input_sha256"]:', '        if False:'),
 # ── 판정 사슬 ──
 ("단일점 판정 통째", '    if _norm_v(v_new) != _norm_v(v):', '    if False:'),
 ("탐침 발동 다시", '    if bool(why) != bool(kv.get("triggered")) or why != kv.get("why") or json.loads(json.dumps(pairs)) != kv.get("pairs"):', '    if False:'),
 ("탐침 판정 통째", '        if _norm_v(kv_new) != _norm_v(kv):', '        if False:'),
 ("탐침 변화", '        if abs(d2 - d1) > DFT["kprobe_shift_eV"] + 1e-12:', '        if False:'),
 ("탐침 순서", '    if o1 != o2:', '    if False:'),
 ("탐침 경계", '        if (abs(d1) >= m - 1e-12) != (abs(d2) >= m - 1e-12):', '        if False:'),
 ("발동 뒤 이완 거부", '        if prev.get("triggered"):\n            raise SystemExit("⛔ 탐침이 발동했다', '        if False:\n            raise SystemExit("⛔ 탐침이 발동했다'),
 ("host sha", '    if _sha(hp) != DFT["ref_cell"]["host_sha256"]:', '    if False:'),
 # ── 10 단계 · EOS 보류 ──
 ("고르기 규칙", '    if dec["gap_ge_margin"]:', '    if True:'),
 ("stage10 계획 폴더 기준", '        s["post_relax"] = _entry(p, base)', '        s["post_relax"] = e'),
 ("EOS 보류 대상 null", '        rv["electronic_targets"] = None', '        rv["electronic_targets"] = [{"family": F, **relaxed[F]["file"]} for F in FAM]'),
 # ── 쓰기 · 덮지 않음 · 거부 보존 ──
 ("LF 쓰기", '    path.write_bytes(text.encode("utf-8"))', '    path.write_bytes(text.replace("\\n", "\\r\\n").encode("utf-8"))'),
 ("덮지 않음 prepare", '    if (out_dir / "dft_plan.json").exists():', '    if False:'),
 ("잡 입력 덮지 않음", '            if f.read_bytes() != t.encode("utf-8"):', '            if False:'),
 ("이완 구조 덮지 않음", '    if p.exists() and p.read_bytes() != buf.getvalue().encode("utf-8"):', '    if False:'),
 ("reject 보존", '        fout.rename(dest)', '        fout.unlink()'),
 ("reject 계획 고리", '    if _bound(cur.get("plan"), p.parent, "계획") != plan_path:', '    if False:'),
]


def problems(src: str, muts) -> list:
    """정적 검사 — 대상이 정확히 한 번 · 바꾼 소스가 문법상 맞음 → [(이름, 이유)]."""
    bad = []
    for name, old, new in muts:
        n = src.count(old)
        if n != 1:
            bad.append((name, f"대상 문자열 {n} 곳"))
            continue
        try:
            ast.parse(src.replace(old, new))
        except SyntaxError as e:
            bad.append((name, f"문법 오류 {e.msg} (줄 {e.lineno})"))
    return bad


def _selftest() -> int:
    src = TOOL.read_text(encoding="utf-8")
    ok = [0, 0]

    def chk(c, m):
        ok[0] += 1
        ok[1] += bool(c)
        print(("  ✓ " if c else "  ✗ ") + m)

    chk(problems(src, M) == [], f"[양성] 변이 {len(M)} 개 — 대상이 도구에 정확히 한 번씩 · 바꾼 소스 문법 맞음")
    chk(len({n for n, _, _ in M}) == len(M), "[양성] 변이 이름이 겹치지 않는다")
    fake = [("없는 대상", "if 이런_줄은_없다:", "if False:")]
    chk(problems(src, fake) and "0 곳" in problems(src, fake)[0][1], "[음성] 도구에 없는 대상을 잡는다 (낡은 변이)")
    dup = [("두 번", "\n", "\n")]
    chk(problems(src, dup) and "곳" in problems(src, dup)[0][1], "[음성] 여러 번 있는 대상을 잡는다 (어느 줄을 끄는지 모름)")
    syn = [("문법", M[0][1], M[0][1] + " (")]
    chk(problems(src, syn) and "문법" in problems(src, syn)[0][1], "[음성] 문법이 깨지는 변이를 잡는다 (가짜 빨강)")
    print(f"selftest: {ok[1]}/{ok[0]}")
    return 0 if ok[0] == ok[1] else 1


def main() -> int:
    if "--selftest" in sys.argv[1:]:
        return _selftest()
    src = TOOL.read_text(encoding="utf-8")
    bad = problems(src, M)
    if bad:
        print("⛔ 변이 목록이 도구와 맞지 않는다 — 돌리지 않는다:", bad)
        return 2
    red = 0
    try:
        for name, old, new in M:
            MUT.write_text(src.replace(old, new), encoding="utf-8")
            r = subprocess.run([sys.executable, str(MUT), "--selftest"], capture_output=True, text=True, timeout=900)
            m = re.search(r"selftest: (\d+)/(\d+)", r.stdout)
            hit = (m is None) or (m.group(1) != m.group(2))
            red += hit
            first = next((ln.strip() for ln in r.stdout.splitlines() if ln.strip().startswith("✗")), "")
            print(f"  {'빨강' if hit else '⛔초록'} {name} ({m.group(0) if m else 'crash rc=%d' % r.returncode}) {first[:90]}",
                  flush=True)
    finally:
        MUT.unlink(missing_ok=True)
    print(f"깨기 {red}/{len(M)} 빨강")
    return 0 if red == len(M) else 1


if __name__ == "__main__":
    sys.exit(main())
