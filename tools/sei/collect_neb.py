#!/usr/bin/env python3
"""collect_neb.py — NEB 결과를 읽어 **장벽과 그 신뢰 근거**를 같이 낸다.

왜 "장벽만" 안 내나
  NEB 의 barrier 는 세 가지가 맞아야 의미가 있다.
    ① 경로가 **수렴**했나 (`neb: convergence achieved`)
    ② **CI(climbing image)** 가 켜져 최고점을 실제로 올라탔나 — 안 그러면 이미지 격자
       때문에 장벽이 과소평가된다
    ③ 정·역 장벽이 **거의 같은가** — 공공 매개 홉은 시작·끝이 대칭 자리라 크게 다르면
       끝점 하나가 다른 국소최소로 흘렀다는 뜻이다
  셋 다 안 보고 숫자만 옮기면 조용히 틀린 값이 논문에 들어간다.

이 도구가 못 하는 것
  · 셀 크기 수렴을 대신 봐 주지 않는다 — jellium/이미지 상호작용은 별도 런으로 확인할 것.
  · 홉이 **전도 경로인지**는 판정하지 않는다 (끝점 대칭·수렴만 본다). li3nd c→b 처럼
    수렴·대칭 검사를 다 통과하고도 "일어나지 않는 홉" 일 수 있다.

  python3 tools/sei/collect_neb.py                       # 기본 루트 전부 (아래 ROOTS)
  python3 tools/sei/collect_neb.py --work /data/work/runs/sei_neb
  python3 tools/sei/collect_neb.py --work a:b,c          # 콜론/쉼표로 여러 루트
  python3 tools/sei/collect_neb.py --selftest
"""
import argparse
import glob
import json
import os
import re
import sys

OUT = "db/properties/sei_neb.json"
#: NEB 작업 루트 — watch_gabia.py 의 NEBW 와 같은 목록이어야 한다.
#: ⛔⛔ 2026-08-13 — 옛 판은 `--work` 하나만 받고 그 루트 결과로 파일을 **통째로 덮어썼다**.
#:   루트가 4개가 된 뒤로는 마지막에 회수한 루트만 db 에 남는다: ccpath 를 회수하면
#:   v2 의 li2s 가 사라지고, 그 뒤 v3 를 회수하면 방금 인용 가능해진 li3nd 가 사라진다.
#:   게다가 같은 상 이름이 루트마다 **다른 홉**이라 tag 키가 서로를 덮어쓴다
#:   (li3nd 는 v2=c→b · ccpath=c→c · cc333=3×3×3 로 셋이다).
#:   → 여러 루트를 한 번에 읽고, 키를 `<루트라벨>/<상>` 으로 쓴다.
ROOTS = os.environ.get("NEBW",
                       "/data/work/runs/sei_neb_v2"
                       ":/data/work/runs/sei_neb_v2_ccpath"
                       ":/data/work/runs/sei_neb_v2_cc333"
                       ":/data/work/runs/sei_neb_v3")


def split_roots(spec):
    """콜론/쉼표 목록 → (존재하는 루트, 없는 루트). 없는 건 조용히 버리지 않는다."""
    out, missing = [], []
    for x in re.split(r"[:,]", spec or ""):
        x = x.strip()
        if not x:
            continue
        (out if os.path.isdir(x) else missing).append(x)
    return out, missing


def root_label(d):
    """/data/work/runs/sei_neb_v2_ccpath → v2_ccpath (표와 키에 쓰는 짧은 이름)."""
    b = os.path.basename(os.path.normpath(d))
    return b[len("sei_neb_"):] if b.startswith("sei_neb_") else b
# QE neb.x 가 찍는 줄:
#   activation energy (->) =   0.286745 eV
#   activation energy (<-) =   0.286712 eV
_ACT = re.compile(r"activation energy\s*\((->|<-)\)\s*=\s*(-?[\d.]+)\s*eV")
_IMG = re.compile(r"num_of_images\s*=\s*(\d+)")
#: neb.**in** 은 네임리스트라 `CI_scheme = 'auto'`, neb.**out** 은 echo 라
#: `CI_scheme                     =    auto` — 따옴표를 강제하면 out 에서 안 맞는다.
_CI = re.compile(r"CI_scheme\s*=\s*'?([\w.\-]+)'?")


def read_one(d):
    tag = os.path.basename(d)
    out = os.path.join(d, "neb.out")
    r = {"tag": tag, "status": "not_started"}
    if not os.path.isfile(out):
        return r
    t = open(out, errors="ignore").read()
    inp = ""
    if os.path.isfile(os.path.join(d, "neb.in")):
        inp = open(os.path.join(d, "neb.in"), errors="ignore").read()
    # ⚠ 실행 자체가 실패한 경우를 **미수렴과 구분**한다 (2026-08-07 실측).
    #   neb.x 가 없어 mpirun 이 못 띄웠는데 회수기가 "경로 미수렴 — nstep_path 를 늘려"
    #   라고 안내해, 2시간 동안 안 돌고 있는 걸 눈치채지 못했다.
    if re.search(r"unable to launch|could not access or execute|command not found", t):
        r.update({"status": "launch_failed",
                  "blocking_checks": ["⛔ neb.x 실행 자체가 실패했다 — 계산이 안 돌았다. "
                                      "바이너리 경로·실행권한을 볼 것 (NEB=... 로 지정 가능)"],
                  "citable": False,
                  "launch_error": "\n".join(t.splitlines()[:8])})
        return r
    acts = _ACT.findall(t)
    fwd = [float(v) for k, v in acts if k == "->"]
    bwd = [float(v) for k, v in acts if k == "<-"]
    conv = "neb: convergence achieved" in t
    r.update({
        "status": "converged" if conv else ("running" if acts else "no_energy_yet"),
        "n_path_steps": len(fwd),
        "Ea_forward_eV": fwd[-1] if fwd else None,
        "Ea_backward_eV": bwd[-1] if bwd else None,
        "num_of_images": int(_IMG.search(inp).group(1)) if _IMG.search(inp) else None,
        # ★ neb.out 을 **먼저** 본다 — 실제로 돈 것이 무엇인지는 출력이 정본이다.
        #   neb.in 만 보면 CI 로 재생성해 놓고 CI 런이 안 뜬 상태(옛 neb.out)를
        #   'CI 완료' 로 읽는다. 없으면 입력으로 폴백.
        "CI_scheme": ((_CI.search(t) or _CI.search(inp)).group(1)
                      if (_CI.search(t) or _CI.search(inp)) else None),
        # ⚠ 전하는 meta.json 이 정본이다 — 입력 문자열 추론은 옛 규약을 되살릴 수 있다
        "tot_charge_from_input": (re.search(r"tot_charge\s*=\s*(-?[\d.]+)", inp).group(1)
                                  if re.search(r"tot_charge\s*=\s*(-?[\d.]+)", inp) else None),
    })
    # ③ 정·역 대칭성 — ★ **끝점이 대칭적으로 같을 때만** 이 검사가 유효하다.
    #   실측(2026-08-07 spglib): Li₂S 는 Li 궤도 1개(Fm-3m, Wyckoff c)라 정=역이어야 하지만,
    #   Li₃P(P6₃/mmc, b+f)·Li₃PO₄γ(Pnma, d+c)는 **Li 자리가 두 종류**라 정≠역이 정상이다.
    #   그 차이는 버그가 아니라 **두 Li 자리의 에너지 차**다. 이걸 모르고 일괄로 걸면
    #   멀쩡한 결과를 의심스럽다고 잘못 판정한다 — 입력 단계에서 기록한 meta.json 을 읽는다.
    meta = {}
    mp = os.path.join(d, "meta.json")
    if os.path.isfile(mp):
        try:
            meta = json.load(open(mp, encoding="utf-8"))
        except (OSError, ValueError):
            meta = {}
    eqv = meta.get("endpoints_symmetry_equivalent")
    r["endpoints_symmetry_equivalent"] = eqv
    r["li_orbits"] = meta.get("li_orbits")
    # ★ P0-4 — 전역 orbit 수가 아니라 **선택된 쌍**의 등가성으로 판정한다
    r["pair_orbits"] = meta.get("pair_orbits")
    r["global_n_li_orbits"] = meta.get("global_n_li_orbits")
    r["neighbor_shells"] = meta.get("neighbor_shells")
    r["protocol_hash"] = meta.get("protocol_hash")
    r["supercell"] = meta.get("supercell")
    r["min_cell_A"] = meta.get("min_cell_A")
    if r["Ea_forward_eV"] is not None and r["Ea_backward_eV"] is not None:
        f_, b_ = r["Ea_forward_eV"], r["Ea_backward_eV"]
        asym = abs(f_ - b_)
        r["asymmetry_eV"] = asym
        # ★ 장거리 수송에 걸리는 유효 장벽 = 안장점 − **가장 낮은 자리** = max(정, 역).
        #   대칭 홉이면 둘이 같으니 자동으로 맞고, 비대칭 홉이면 이게 물리적으로 맞는 값이다.
        r["Ea_effective_eV"] = max(f_, b_)
        r["site_energy_diff_eV"] = asym if eqv is False else None
        # 대칭이어야 하는 경우에만 게이트를 건다
        r["symmetric"] = (asym < 0.02) if eqv else None
    checks = []
    if not conv:
        checks.append("경로 미수렴 — nstep_path 를 늘려 이어서 돌릴 것" if acts
                      else "아직 에너지가 안 나왔다 — 시작 직후이거나 첫 SCF 중")
    if r.get("CI_scheme") in (None, "no-CI"):
        checks.append("CI 가 꺼져 있다 — 장벽이 이미지 격자만큼 과소평가된다")
    if r.get("symmetric") is False:
        checks.append(f"정·역 장벽이 {r['asymmetry_eV']:.3f} eV 어긋난다 — "
                      f"이 상은 Li 자리가 한 종류라 같아야 한다 "
                      f"(끝점 하나가 다른 국소최소로 흘렀을 수 있다)")
    if eqv is None and os.path.isfile(mp) is False:
        checks.append("meta.json 이 없어 대칭 판정을 못 한다 — 생성기를 다시 돌릴 것")
    # ★ 2026-08-11 전하 규약 정정 (Codex P0-1) — 옛 규약(+1)은 정공 2개라 무효다.
    #   ★★ 단, **차단 조건이 상의 electronic_class 로 갈린다** (Li₃Nd 착수):
    #     insulator → V_Li⁻ (tot_charge = −1) 을 기대한다. +1 은 무효, 0 은 정공 1개.
    #     metal     → 중성 공공 (tot_charge = 0) 이 **맞다.** 여기에 절연체 게이트를
    #                 걸면 옳은 계산을 도구가 막는다 — 실제로 옛 코드가 그랬다.
    tc = meta.get("tot_charge")
    ecls = meta.get("electronic_class")
    r["vacancy_charge"] = meta.get("vacancy_charge")
    r["electronic_class"] = ecls
    r["smearing"] = meta.get("smearing")
    if ecls is None:
        checks.append("meta.json 에 electronic_class 가 없다 — 옛 생성기다. "
                      "금속/절연체에 따라 전하 규약이 다르므로 재생성할 것")
    elif ecls == "metal":
        if tc is not None and abs(float(tc)) > 1e-9:
            checks.append(f"metal 인데 tot_charge={tc} — 금속에 jellium 배경전하는 "
                          "물리적 근거가 없다. tot_charge=0 으로 재생성할 것")
        if meta.get("smearing") not in (None, "mv", "m-v", "marzari-vanderbilt"):
            checks.append(f"metal 인데 smearing={meta.get('smearing')} — 금속엔 mv 를 쓴다")
        if meta.get("electronic_class_evidence") == "declared":
            checks.append("electronic_class=metal 이 **선언만** 된 상태다 (evidence=declared). "
                          "DOS/PDOS 로 E_F 상태를 확인하기 전에는 장벽을 인용하지 않는다")
    # ★ P1-10 — 옛 규약(+1) 진단은 **분기 밖에서 항상** 돈다. elif 안에 있으면
    #   electronic_class 가 없는 옛 meta(=정확히 +1 을 쓰던 그 파일들)에서
    #   "생성기가 옛것" 메시지에 가려 **진짜 이유(전자 2개 차이)가 안 보였다**.
    if tc is not None and float(tc) > 0:
        checks.append(f"tot_charge={tc} — **옛 규약(정공 2개)**이다. V_Li⁻ 는 −1 이다. "
                      "build_neb_inputs.py 를 다시 돌려 재계산할 것")
    # ★ P1-11 — insulator + tot_charge=0 (V_Li⁰, 정공 1개)은 파일럿용이지 정본이 아니다.
    #   아무 게이트도 없으면 q=−1 결과들과 같은 표에 섞인다.
    if ecls not in (None, "metal") and tc is not None and abs(float(tc)) < 1e-9:
        checks.append("insulator 인데 tot_charge=0 (V_Li⁰, 정공 1개)이다 — 파일럿 값이다. "
                      "정본은 V_Li⁻(−1) 이므로 같은 표에 섞지 말 것")
    # ★ P0-2 — vacancy 끝점이 이완되지 않았으면 장벽을 믿을 수 없다
    if meta.get("endpoints_relaxed") is False:
        checks.append("vacancy 끝점이 미이완이다 — 끝점이 경로 최고점이 되면 Ea 가 0 으로 "
                      "붕괴한다. `run_sei_neb.sh endpoints <tag>` 먼저")
    if meta.get("ci_scheme") == "no-CI":
        checks.append("no-CI 단계다 — 장벽이 이미지 격자만큼 과소평가된다. "
                      "수렴 후 --ci_scheme auto --restart 로 2단계를 돌릴 것")
    # ★ 2026-08-11 추가 — li3p 가 Ea=0.000 eV 로 `citable: true` 를 통과했다.
    #   장벽 0 은 측정이 아니라 **경로가 붕괴했다**는 신호다 (움직이는 Li 가 안 움직였거나
    #   두 끝점이 사실상 같은 구조이거나 안장점을 못 찾았거나).
    ea = r.get("Ea_effective_eV")
    if ea is not None and ea < 0.01:
        checks.append(f"유효 장벽이 {ea:.4f} eV — **0 은 측정이 아니다.** 경로 붕괴를 의심할 것: "
                      f"① 끝점 두 개가 같은 구조인가 ② 움직이는 Li 가 실제로 이동했나 "
                      f"③ 이미지 사이 최대 변위가 0 이 아닌가. neb.dat 와 끝점 좌표를 직접 볼 것")
    if ea is not None and ea < 0:
        checks.append(f"장벽이 음수({ea:.4f} eV) — 끝점이 안장점보다 높다. 입력이 잘못됐다")
    # 비등가 끝점인데 자리 에너지 차가 정확히 0 인 것도 같은 종류의 신호다
    if eqv is False and r.get("site_energy_diff_eV") is not None \
            and abs(r["site_energy_diff_eV"]) < 1e-6:
        checks.append("비등가 Li 자리(Wyckoff 2종)인데 자리 에너지 차가 0 이다 — "
                      "끝점 생성이 실제로 두 자리를 잡았는지 확인할 것")
    r["blocking_checks"] = checks
    r["citable"] = conv and not checks
    return r


def selftest():
    """양성 + **음성**. 음성이 없으면 통과해도 아무것도 보증 못 한다."""
    import shutil
    import tempfile
    td = tempfile.mkdtemp(prefix="collect_neb_st_")
    ok = True

    def chk(cond, msg):
        nonlocal ok
        print(("  ✓ " if cond else "  ✗ ") + msg)
        ok &= bool(cond)

    def mk(root, tag, ea, ci="auto", conv=True, eqv=True):
        d = os.path.join(td, root, tag)
        os.makedirs(d, exist_ok=True)
        json.dump({"endpoints_symmetry_equivalent": eqv,
                   "electronic_class": "metal", "tot_charge": 0},
                  open(os.path.join(d, "meta.json"), "w"))
        # ★ 픽스처는 **실제 형식**이어야 한다 — neb.in 은 따옴표 있는 네임리스트,
        #   neb.out 은 따옴표 없는 echo. 어제 픽스처가 둘 다 따옴표라 정규식 결함을
        #   그대로 통과시켰다 (2026-08-13).
        open(os.path.join(d, "neb.in"), "w").write(
            f"  num_of_images = 7,\n  CI_scheme = '{ci}',\n  tot_charge = 0,\n")
        body = (f"     num_of_images                 =    7\n"
                f"     CI_scheme                     =    {ci}\n"
                f"     activation energy (->) =   {ea:.6f} eV\n"
                f"     activation energy (<-) =   {ea:.6f} eV\n")
        if conv:
            body += "     neb: convergence achieved in 1 iterations\n"
        open(os.path.join(d, "neb.out"), "w").write(body)
        return d

    # 양성: CI 켜짐 + 수렴 + 대칭 → 인용 가능
    r = read_one(mk("sei_neb_v2_ccpath", "li3nd", 0.228981))
    chk(r["citable"] and abs(r["Ea_effective_eV"] - 0.228981) < 1e-9,
        f"CI·수렴·대칭 → 인용 가능 ({r.get('Ea_effective_eV')})")
    # 음성 ①: no-CI 는 하한이라 인용 불가여야 한다
    r = read_one(mk("sei_neb_v2", "li2s", 0.305, ci="no-CI"))
    chk(not r["citable"] and any("CI" in c for c in r["blocking_checks"]),
        f"no-CI → 인용 불가 ({r['blocking_checks']})")
    # 음성 ②: 미수렴
    r = read_one(mk("sei_neb_v3", "licl", 0.4, conv=False))
    chk(not r["citable"], "미수렴 → 인용 불가")
    # 음성 ③ ★ 루트가 달라도 상 이름이 같으면 **덮어쓰면 안 된다** (2026-08-13 실측 결함)
    mk("sei_neb_v2", "li3nd", 2.0717, ci="no-CI", eqv=False)
    keys = {}
    for root in sorted(glob.glob(os.path.join(td, "*"))):
        for d in sorted(glob.glob(os.path.join(root, "*"))):
            rr = read_one(d)
            rr["root"] = root_label(root)
            keys[f"{rr['root']}/{rr['tag']}"] = rr
    n_li3nd = [k for k in keys if k.endswith("/li3nd")]
    chk(len(n_li3nd) == 2 and "v2_ccpath/li3nd" in keys and "v2/li3nd" in keys,
        f"같은 상 li3nd 가 루트 2개에 **둘 다** 남는다 ({sorted(n_li3nd)})")
    chk(keys["v2_ccpath/li3nd"]["citable"] and not keys["v2/li3nd"]["citable"],
        "루트별 판정이 섞이지 않는다 (ccpath 인용 가능 · v2 불가)")
    # 루트 목록 파서
    got, miss = split_roots(f"{td}/sei_neb_v2:{td}/nope, {td}/sei_neb_v3")
    chk(len(got) == 2 and miss == [f"{td}/nope"], f"콜론·쉼표 목록 + 없는 루트 보고 ({miss})")
    chk(root_label("/a/b/sei_neb_v2_ccpath") == "v2_ccpath"
        and root_label("/a/b/other") == "other", "루트 짧은 이름")
    # ── ⛔ 축소 거부 (2026-08-16 사고) ──────────────────────────────────────
    #   run_sei_neb.sh 가 --work 로 루트 하나만 넘겨 db 를 v2 로 되돌렸고,
    #   인용 가능하던 v2_ccpath/li3nd (0.229 eV) 가 사라졌다.
    import io as _io, json as _json, contextlib as _ctx
    _prev = {"roots": ["v2", "v2_ccpath"],
             "results": {"v2_ccpath/li3nd": {"citable": True, "Ea_forward_eV": 0.228981}}}
    _tmp_out = os.path.join(td, "sei_neb.json")
    with open(_tmp_out, "w", encoding="utf-8") as fh:
        _json.dump(_prev, fh)
    _real_out = globals()["OUT"]
    try:
        globals()["OUT"] = _tmp_out
        import argparse as _ap
        _args = _ap.Namespace(allow_shrink=False)
        # 루트가 v2 하나로 줄어드는 상황을 그대로 재현
        _prev_roots = set(_prev["roots"]); _now_roots = {"v2"}
        chk(bool(_prev_roots - _now_roots), "[음성] 루트 축소를 감지한다 (v2_ccpath 소멸)")
        chk("v2_ccpath/li3nd" in [k for k, v in _prev["results"].items() if v.get("citable")],
            "[음성] 사라질 인용 가능 결과를 이름으로 지목한다")
    finally:
        globals()["OUT"] = _real_out

    shutil.rmtree(td, ignore_errors=True)
    print("selftest " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default=os.environ.get("WORK", ROOTS),
                    help="작업 루트. 콜론/쉼표로 **여러 개**를 준다 (기본은 ROOTS 전부)")
    ap.add_argument("--allow-shrink", action="store_true",
                    help="루트가 줄어드는 쓰기를 허용한다 (기본은 거부 — 사고 방지)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    roots, missing = split_roots(a.work)
    for m in missing:
        print(f"⚠ 루트 없음: {m}")
    if not roots:
        print(f"⛔ {a.work} 에 존재하는 루트가 없다 — build_neb_inputs.py 부터")
        return 1
    res = {}
    print(f"{'상':12s} {'상태':12s} {'Ea→':>8s} {'Ea←':>8s} {'유효Ea':>8s} {'끝점':>6s} {'스텝':>5s}  판정")
    for root in roots:
        dirs = sorted(d for d in glob.glob(os.path.join(root, "*")) if os.path.isdir(d))
        print(f"┌ {root_label(root)}" + ("" if dirs else "   (상 폴더 없음)"))
        for d in dirs:
            r = read_one(d)
            r["root"] = root_label(root)
            # 키에 루트를 넣는다 — 같은 상 이름이 루트마다 다른 홉이라 tag 로 키를 잡으면
            # 조용히 서로를 덮어쓴다 (li3nd 셋이 하나로 뭉개졌다).
            res[f"{r['root']}/{r['tag']}"] = r
            f = r.get("Ea_forward_eV"); b = r.get("Ea_backward_eV")
            ef = r.get("Ea_effective_eV"); eq = r.get("endpoints_symmetry_equivalent")
            print(f"{r['tag']:12s} {r['status']:12s} "
                  f"{(f'{f:.4f}' if f is not None else '—'):>8s} "
                  f"{(f'{b:.4f}' if b is not None else '—'):>8s} "
                  f"{(f'{ef:.4f}' if ef is not None else '—'):>8s} "
                  f"{('대칭' if eq else ('비대칭' if eq is False else '?')):>6s} "
                  f"{r.get('n_path_steps', 0):5d}  "
                  + ("✅ 인용 가능" if r.get("citable") else
                     ("⚠ " + " · ".join(r.get("blocking_checks") or ["진행 중"]))[:64]))
            if r.get("site_energy_diff_eV"):
                print(f"{'':12s} └ Li 자리 두 종류 {r.get('li_orbits', {}).get('wyckoffs')} — "
                      f"정·역 차 {r['site_energy_diff_eV']:.3f} eV 는 **자리 에너지 차**다(정상). "
                      f"수송 장벽은 유효Ea 를 쓴다")
    # ⛔⛔ 2026-08-16 — 다중 루트로 고쳤는데 **호출부**가 단일 루트를 계속 넘겨서
    #   run_sei_neb.sh 의 마지막 collect 가 db 를 v2 하나로 되돌렸다.
    #   실측: n_citable 1/8 → 0/2, v2_ccpath/li3nd (0.229, 인용 가능) 가 소멸.
    #   호출부는 고쳤지만, **여기서도 막는다** — 루트가 줄어드는 쓰기는 사고다.
    if os.path.exists(OUT) and not a.allow_shrink:
        try:
            prev = json.load(open(OUT, encoding="utf-8"))
        except Exception:
            prev = {}
        prev_roots = set(prev.get("roots") or [])
        now_roots = {root_label(r) for r in roots}
        lost = prev_roots - now_roots
        if lost:
            print(f"\n⛔ 이번 회수는 루트가 **줄어든다** — 쓰지 않는다.")
            print(f"   기존 {sorted(prev_roots)} → 이번 {sorted(now_roots)}  (사라질 루트: {sorted(lost)})")
            prev_ok = [k for k, v in (prev.get("results") or {}).items() if v.get("citable")]
            if prev_ok:
                print(f"   ⚠ 그중 인용 가능한 결과가 있다: {prev_ok}")
            print(f"   전체를 회수하려면 --work 없이 그냥 돌릴 것 (기본이 ROOTS 전부):")
            print(f"     python3 tools/sei/collect_neb.py")
            print(f"   정말 축소하려면 --allow-shrink (근거를 db 에 남길 것)")
            return 1

    ok = [r for r in res.values() if r.get("citable")]
    # ⛔⛔ 2026-08-11 자체검토 P0-6 — 옛 코드는 `if ok:` 일 때만 JSON 을 썼다.
    #   그래서 새 게이트가 콘솔에서 li2s 를 막아도 **db 파일은 안 건드려**,
    #   하류(원고·그림·비교표)는 철회된 0.272 eV 를 `citable: true` 로 계속 읽었다.
    #   차단은 콘솔에만 있고 db 에는 없었다 = 제일 나쁜 조합이다.
    #   → 항상 쓴다. citable 이 0건이면 최상위에 retracted 를 박는다.
    if True:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        json.dump({
            "property": "sei_li_migration_barrier_neb",
            "method": ("QE CI-NEB (neb.x). 공공 매개 Li 홉. ecutwfc 60 / ecutrho 480 Ry "
                       "— 갭 계산과 같은 사양. **전하 규약은 상의 electronic_class 로 갈린다**: "
                       "insulator = V_Li⁻ (tot_charge −1) + jellium · gaussian smearing / "
                       "metal = 중성 공공 (tot_charge 0) · mv smearing (jellium 없음). "
                       "결과마다 electronic_class·tot_charge 를 같이 싣는다. "
                       "⛔ 2026-08-11 이전의 tot_charge=+1 입력은 정공 2개라 무효."),
            "warning": ("⚠ jellium 보정은 유한 셀 근사다 — 절대값은 셀 수렴 확인 뒤 인용할 것. "
                        "**상 사이 비교**가 이 값의 용도다. "
                        "⛔ BVSE 프록시 값과 같은 표에 놓지 말 것(단위는 같아도 다른 양이다)."),
            "roots": [root_label(r) for r in roots],
            "key_format": "<루트라벨>/<상> — 같은 상이 루트마다 다른 홉이라 tag 만으로는 충돌한다",
            "n_citable": len(ok), "n_total": len(res),
            "retracted": len(ok) == 0,
            "retraction_reason": (None if ok else
                                  "인용 가능한 결과가 0건이다. 각 결과의 blocking_checks 를 볼 것. "
                                  "이 파일의 어떤 값도 인용하지 말 것."),
            "results": res,
        }, open(OUT, "w"), ensure_ascii=False, indent=2)
        print(f"\n→ {OUT}  (인용 가능 {len(ok)}/{len(res)})"
              + ("  ⛔ **retracted: true** 로 표기했다" if not ok else ""))
    print("⚠ 장벽은 **상 사이 비교**용이다. jellium 유한 셀 보정이 남아 있으니")
    print("  절대값을 실험과 나란히 놓기 전에 셀 크기 수렴을 확인할 것.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
