#!/usr/bin/env python3
"""oncv_regen_check.py — ONCVPSP 로 다시 뽑은 pseudo 가 배포본 psp8 과 같은 pseudo 인지 숫자로 대조한다.

왜 있나 (2026-10-19 · Nd Q3 ELF · 결정 D-2026-10-19-nd-q23-ppswap-structure · 사용자 '권고대로 해')
  ELF 규약은 NC pseudo 다 (run_lpsocl_elf_gabia.sh · 호스트 modelc ELF 표와 같은 규약). 4f 를 core 에 둔 NC Nd 는
  PseudoDojo (ONCVPSP-PBE-PDv0.4/Nd/Nd3+_f-in-core · ONCVPSP 3.2.3.1 · 가전자 5s²5p⁶5d¹6s² = 11) 에 psp8 로만 있다.
  QE 는 UPF 를 읽는다 → 같은 입력 (.in) 으로 ONCVPSP 를 다시 돌려 psfile 'both' 로 psp8 · UPF 를 **한 번에** 뽑고,
  그 psp8 이 배포본 psp8 과 숫자로 같으면 같은 실행에서 나온 UPF 도 같은 pseudo 라고 본다 (UPF 를 손으로 변환하지 않는다).

  python3 tools/electronic/oncv_regen_check.py --set_psfile Nd3+_f-in-core.in both --dest Nd3+_both.dat
  python3 tools/electronic/oncv_regen_check.py --extract Nd3+_both.out --kind upf  --dest Nd3+_f-in-core.oncvpsp.upf
  python3 tools/electronic/oncv_regen_check.py --compare Nd3+_f-in-core.psp8 regen.psp8 --tol 1e-3 --json cmp.json

⛔ 이 도구가 못 하는 것
  · pseudo 의 물리적 품질 (전이성 · 고스트) 을 판정하지 않는다 — PseudoDojo 검증 기록 (djrepo) 과 ONCVPSP 출력의 진단을 사람이 본다.
  · UPF 자체를 배포본과 대조하지 못한다 (배포본 UPF 가 없다) — psp8 이 같다는 것을 근거로 같은 실행의 UPF 를 믿는다.
  · ONCVPSP 판이 다르면 (3.2.3.1 대 4.x) 최적화 루틴이 바뀌어 숫자가 조금 다를 수 있다 (release_notes 3.3.0) — 그 차이를
    재서 보고할 뿐 '허용' 여부는 --tol 로 정한다 (기본 1e-3 상대 · 넘으면 종료 1).
  · psp8 의 헤더 pspd (생성 날짜 코드) 와 첫 줄 제목은 비교하지 않는다 — 다시 뽑으면 당연히 다르다.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

_NUM = re.compile(r"^[-+]?(\d+\.?\d*|\.\d+)([eEdD][-+]?\d+)?$")


def _f(tok):
    return float(tok.replace("D", "E").replace("d", "e"))


def _nums(line):
    out = []
    for t in line.split():
        if _NUM.match(t):
            out.append(_f(t))
        else:
            break
    return out


def read_psp8(path):
    """psp8 → dict(header=..., blocks={name: list of rows}, ekb={l: [...]})."""
    L = Path(path).read_text().splitlines()
    h1, h2, h3 = _nums(L[1]), _nums(L[2]), _nums(L[3])
    pspcod, pspxc, lmax, lloc, mmax = (int(x) for x in h2[:5])
    if pspcod != 8:
        raise SystemExit(f"{path}: pspcod {pspcod} — psp8 이 아니다")
    nproj = [int(x) for x in _nums(L[4])[:lmax + 1]]
    ext = [int(x) for x in _nums(L[5])]
    hdr = {"zatom": h1[0], "zion": h1[1], "pspcod": pspcod, "pspxc": pspxc, "lmax": lmax, "lloc": lloc, "mmax": mmax,
           "r2well": h2[5] if len(h2) > 5 else None, "rchrg": h3[0], "fchrg": h3[1], "qchrg": h3[2], "nproj": nproj, "ext": ext}
    i, blocks, ekb = 6, {}, {}

    def take(n, name):
        nonlocal i
        rows = [_nums(L[i + k]) for k in range(n)]
        if any(not r for r in rows) or len({len(r) for r in rows}) != 1:
            raise SystemExit(f"{path}: {name} 블록 모양이 이상하다 (줄 {i + 1}–{i + n})")
        i += n
        return rows

    for l in range(lmax + 1):
        if nproj[l] == 0:
            continue
        h = _nums(L[i])
        if int(h[0]) != l:
            raise SystemExit(f"{path}: 투영자 머리 l={int(h[0])} (기대 {l}) — 줄 {i + 1}")
        ekb[l] = h[1:1 + nproj[l]]
        i += 1
        blocks[f"proj_l{l}"] = take(mmax, f"proj_l{l}")
    if lloc > lmax:
        h = _nums(L[i])
        if int(h[0]) != lloc:
            raise SystemExit(f"{path}: 국소 퍼텐셜 머리 {int(h[0])} (기대 lloc {lloc}) — 줄 {i + 1}")
        i += 1
        blocks["vloc"] = take(mmax, "vloc")
    if hdr["fchrg"] > 0:
        blocks["core"] = take(mmax, "core")
    tail = []
    while i < len(L) and _nums(L[i]) and not L[i].lstrip().startswith("#"):
        tail.append(_nums(L[i])); i += 1
    if tail:
        blocks["tail"] = tail
    return {"header": hdr, "blocks": blocks, "ekb": ekb}


def compare(a, b, tol=1e-3):
    """두 psp8 (read_psp8) → (ok, report). 헤더 (pspd · 제목 제외) 는 같아야 하고 블록은 상대 오차 ≤ tol."""
    rep, ok = {"tol_rel": tol, "header_mismatch": [], "blocks": {}, "ekb": {}}, True
    for k in ("zatom", "zion", "pspcod", "pspxc", "lmax", "lloc", "mmax", "r2well", "rchrg", "fchrg", "qchrg", "nproj", "ext"):
        if a["header"][k] != b["header"][k]:
            rep["header_mismatch"].append(f"{k}: {a['header'][k]} ≠ {b['header'][k]}")
    if rep["header_mismatch"]:
        return False, rep
    if set(a["blocks"]) != set(b["blocks"]):
        rep["header_mismatch"].append(f"블록 집합 {sorted(a['blocks'])} ≠ {sorted(b['blocks'])}")
        return False, rep
    for name in a["blocks"]:
        A, B = a["blocks"][name], b["blocks"][name]
        if len(A) != len(B) or any(len(x) != len(y) for x, y in zip(A, B)):
            rep["blocks"][name] = {"shape": "다름"}; ok = False; continue
        # 첫 열 (격자 번호) 은 정수 · 둘째 열 r 은 격자 — 둘 다 같아야 한다 · 나머지 열을 값으로 본다.
        # ⚠ 상대 오차는 **열마다** 잰다 — core · 가전자 블록은 값 옆에 도함수 열 (r=0 근처 10⁶) 이 있어서
        #   블록 전체 최대로 나누면 값 열의 차가 묻힌다 (2026-10-19 실물 psp8 에서 확인).
        grid = max(abs(x[0] - y[0]) + abs(x[1] - y[1]) for x, y in zip(A, B)) if len(A[0]) > 1 else 0.0
        cols = []
        for c in range(2, len(A[0])):
            scale = max(abs(x[c]) for x in A) or 1.0
            dmax = max(abs(x[c] - y[c]) for x, y in zip(A, B))
            cols.append({"col": c, "max_abs_diff": dmax, "max_abs_value": scale, "rel": dmax / scale})
        worst = max(cols, key=lambda r: r["rel"]) if cols else {"max_abs_diff": 0.0, "max_abs_value": 0.0, "rel": 0.0, "col": None}
        good = grid < 1e-12 and worst["rel"] <= tol
        rep["blocks"][name] = {"max_abs_diff": worst["max_abs_diff"], "max_abs_value": worst["max_abs_value"], "rel": worst["rel"],
                               "worst_col": worst["col"], "per_col": cols, "grid_diff": grid, "ok": good}
        ok &= good
    for l in a["ekb"]:
        ea, eb = a["ekb"][l], b["ekb"].get(l, [])
        rel = max((abs(x - y) / max(abs(x), 1e-30) for x, y in zip(ea, eb)), default=9.9) if len(ea) == len(eb) else 9.9
        good = rel <= tol
        rep["ekb"][str(l)] = {"a": ea, "b": eb, "rel": rel, "ok": good}
        ok &= good
    return ok, rep


def extract(out_path, kind):
    """ONCVPSP .out → psp8 · upf 본문 (scripts/extract.sh 와 같은 표지: PSPCODE8 · PSP_UPF ~ END_PSP)."""
    mark = {"psp8": "PSPCODE8", "upf": "PSP_UPF"}[kind]
    rows, on = [], False
    for line in Path(out_path).read_text().splitlines(True):
        if "END_PSP" in line:
            on = False
        if on:
            rows.append(line)
        if mark in line:
            on = True
    if not rows:
        raise SystemExit(f"{out_path}: {mark} 블록이 없다 — ONCVPSP 가 {kind} 를 안 썼다 (psfile 확인 · ERROR 줄 확인)")
    return "".join(rows)


def set_psfile(in_path, value):
    """ONCVPSP 입력의 첫 자료 줄 (atsym z nc nv iexc psfile) 의 psfile 만 바꾼다."""
    L = Path(in_path).read_text().splitlines(True)
    for k, line in enumerate(L):
        if line.lstrip().startswith("#") or not line.strip():
            continue
        t = line.split()
        if len(t) != 6 or t[5] not in ("psp8", "upf", "both"):
            raise SystemExit(f"{in_path}: 첫 자료 줄이 'atsym z nc nv iexc psfile' 꼴이 아니다 — {line.strip()}")
        L[k] = line.replace(t[5], value, 1) if line.rstrip().endswith(t[5]) else line
        if L[k].split()[5] != value:
            raise SystemExit(f"{in_path}: psfile 을 못 바꿨다")
        return "".join(L)
    raise SystemExit(f"{in_path}: 자료 줄이 없다")


def md5(path):
    return hashlib.md5(Path(path).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--compare", nargs=2, metavar=("REF_PSP8", "NEW_PSP8"))
    ap.add_argument("--tol", type=float, default=1e-3)
    ap.add_argument("--json")
    ap.add_argument("--extract", metavar="OUT")
    ap.add_argument("--kind", choices=["psp8", "upf"])
    ap.add_argument("--set_psfile", nargs=2, metavar=("IN", "VALUE"))
    ap.add_argument("--dest")
    ap.add_argument("--md5", nargs=2, metavar=("FILE", "EXPECTED"))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.md5:
        got = md5(a.md5[0])
        print(f"md5 {got} {'= ' if got == a.md5[1] else '≠ '}{a.md5[1]}")
        return 0 if got == a.md5[1] else 1
    if a.set_psfile:
        Path(a.dest).write_text(set_psfile(*a.set_psfile)); print(f"→ {a.dest}"); return 0
    if a.extract:
        Path(a.dest).write_text(extract(a.extract, a.kind)); print(f"→ {a.dest}"); return 0
    if a.compare:
        ok, rep = compare(read_psp8(a.compare[0]), read_psp8(a.compare[1]), a.tol)
        rep.update({"ref": a.compare[0], "new": a.compare[1], "ok": ok})
        for m in rep["header_mismatch"]:
            print(f"  ✗ 헤더 {m}")
        for n, r in rep["blocks"].items():
            print(f"  {'✓' if r.get('ok') else '✗'} {n:8s} " + (f"상대 {r['rel']:.2e} (최대 |Δ| {r['max_abs_diff']:.2e} / {r['max_abs_value']:.2e})" if "rel" in r else "모양 다름"))
        for l, r in rep["ekb"].items():
            print(f"  {'✓' if r['ok'] else '✗'} ekb l={l} 상대 {r['rel']:.2e}")
        print(f"{'✅ 같은 pseudo (상대 ≤ ' + str(a.tol) + ')' if ok else '⛔ 다르다'}")
        if a.json:
            Path(a.json).write_text(json.dumps(rep, ensure_ascii=False, indent=1) + "\n")
        return 0 if ok else 1
    ap.error("할 일을 하나 고른다 (--compare · --extract · --set_psfile · --md5 · --selftest)")


def selftest():
    import tempfile
    n = [0, 0]

    def ck(name, cond, info=""):
        n[0 if cond else 1] += 1
        print(f"  {'✓' if cond else '✗'} {name}" + ("" if cond else f"  {info}"))

    def raises(fn):
        try:
            fn()
        except SystemExit:
            return True
        return False

    T = Path(tempfile.mkdtemp(prefix="oncv_st_"))
    mm = 6
    def psp8(scale=1.0, pspd="170524", ws="  ", vloc_bump=0.0, mmax=mm, nproj="2 1"):
        r = [0.01 * k for k in range(mmax)]
        s = ["Nd    ONCVPSP-x  r_core=  2.1", f"{ws}60.0000  11.0000  {pspd}  zatom,zion,pspd",
             f"{ws}8  11  1  4  {mmax}  0  pspcod,pspxc,lmax,lloc,mmax,r2well", f"{ws}5.99  5.40  0.0  rchrg fchrg qchrg",
             f"{ws}{nproj}  nproj", f"{ws}1 1  extension_switch",
             f"{ws}0  6.6415844384433D+00  7.3386355293075D-01"]
        s += [f"{ws}{k + 1}  {r[k]:.13E}  {scale * 0.1 * k:.13E}  {-0.05 * k:.13E}" for k in range(mmax)]
        s += [f"{ws}1  -1.2D+00"] + [f"{ws}{k + 1}  {r[k]:.13E}  {0.2 * k:.13E}" for k in range(mmax)]
        s += [f"{ws}4"] + [f"{ws}{k + 1}  {r[k]:.13E}  {-3.0 + 0.1 * k + (vloc_bump if k == 3 else 0):.13E}" for k in range(mmax)]
        s += [f"{ws}{k + 1}  {r[k]:.13E}  {1.0 / (k + 1):.13E}  0.0  0.0  0.0" for k in range(mmax)]
        s += [f"{ws}{k + 1}  {r[k]:.13E}  {0.5 / (k + 1):.13E}" for k in range(mmax)]
        s += ["# ATOM AND REFERENCE CONFIGURATION", "# echo"]
        return "\n".join(s) + "\n"
    (T / "a.psp8").write_text(psp8())
    (T / "b.psp8").write_text(psp8(pspd="261019", ws=""))
    ok, rep = compare(read_psp8(T / "a.psp8"), read_psp8(T / "b.psp8"))
    ck("공백 · pspd 만 다른 psp8 = 같은 pseudo (상대 0)", ok and all(r["rel"] == 0 for r in rep["blocks"].values()), json.dumps(rep)[:300])
    ck("블록 = proj_l0 · proj_l1 · vloc · core · tail (모양대로 읽음)", sorted(rep["blocks"]) == ["core", "proj_l0", "proj_l1", "tail", "vloc"])
    (T / "c.psp8").write_text(psp8(scale=1.01))
    ck("⛔음성: 투영자 1 % 다르면 (tol 1e-3) 다르다", not compare(read_psp8(T / "a.psp8"), read_psp8(T / "c.psp8"))[0])
    (T / "d.psp8").write_text(psp8(vloc_bump=1e-6))
    ok_d, rep_d = compare(read_psp8(T / "a.psp8"), read_psp8(T / "d.psp8"))
    ck("작은 차 (1e-6) 는 tol 안 · 상대값을 보고한다", ok_d and 0 < rep_d["blocks"]["vloc"]["rel"] < 1e-5, str(rep_d["blocks"].get("vloc")))
    # 열마다 상대 오차 — core 블록의 값 열 (1/(k+1) · 최대 1) 을 1 % 바꾸면, 옆 열이 아무리 커도 잡혀야 한다
    big = psp8().splitlines()
    k0 = next(i for i, s in enumerate(big) if s.strip().startswith("1") and len(s.split()) == 6)
    big = [s if not (k0 <= i < k0 + mm) else (lambda t: "  ".join(t[:3] + [f"{1e6 * (i - k0 + 1):.6E}"] + t[4:]))(s.split())
           for i, s in enumerate(big)]
    (T / "h.psp8").write_text("\n".join(big) + "\n")
    big2 = [s if not (k0 <= i < k0 + mm) else (lambda t: "  ".join(t[:2] + [f"{1.01 * _f(t[2]):.13E}"] + t[3:]))(s.split())
            for i, s in enumerate(big)]
    (T / "i.psp8").write_text("\n".join(big2) + "\n")
    ok_h, rep_h = compare(read_psp8(T / "h.psp8"), read_psp8(T / "i.psp8"))
    ck("⛔음성: 큰 도함수 열 옆의 값 열 1 % 차도 잡는다 (열마다 상대)", not ok_h and rep_h["blocks"]["core"]["worst_col"] == 2,
       str({k: v.get("rel") for k, v in rep_h["blocks"].items()}))
    (T / "e.psp8").write_text(psp8(mmax=7))
    ck("⛔음성: mmax 다르면 (헤더) 다르다", not compare(read_psp8(T / "a.psp8"), read_psp8(T / "e.psp8"))[0])
    (T / "f.psp8").write_text(psp8(nproj="2 2"))
    ck("⛔음성: 투영자 수 다르면 읽기부터 멈추거나 다르다",
       raises(lambda: read_psp8(T / "f.psp8")) or not compare(read_psp8(T / "a.psp8"), read_psp8(T / "f.psp8"))[0])
    (T / "g.psp8").write_text(psp8().replace("  6.6415844384433D+00", "  6.7415844384433D+00"))
    ck("⛔음성: ekb 가 다르면 다르다", not compare(read_psp8(T / "a.psp8"), read_psp8(T / "g.psp8"))[0])
    # extract
    out = T / "x.out"
    out.write_text("head\nBegin PSPCODE8\n" + psp8() + "END_PSP\nmid\nBegin PSP_UPF\n<UPF version=\"2.0.1\">\n</UPF>\nEND_PSP\n")
    ck("extract psp8 = 원문 · upf 본문", extract(out, "psp8") == psp8() and extract(out, "upf").startswith("<UPF"))
    out2 = T / "y.out"; out2.write_text("Begin PSPCODE8\n" + psp8() + "END_PSP\n")
    ck("⛔음성: UPF 블록이 없으면 멈춘다 (psfile psp8 로 돈 경우)", raises(lambda: extract(out2, "upf")))
    # set_psfile
    inp = T / "z.in"
    inp.write_text("# ATOM AND REFERENCE CONFIGURATION\n# atsym  z   nc   nv     iexc    psfile\n  Nd 60.00   10    4       4       psp8\n#\n    1    0    2.00    -1.59D+03\n")
    s = set_psfile(inp, "both")
    ck("psfile psp8 → both (그 줄만 · 나머지 그대로)", s.splitlines()[2].split() == ["Nd", "60.00", "10", "4", "4", "both"]
       and s.splitlines()[4] == inp.read_text().splitlines()[4])
    inp2 = T / "w.in"; inp2.write_text("# x\n  Nd 60.00 10 4 4\n")
    ck("⛔음성: psfile 칸이 없으면 멈춘다", raises(lambda: set_psfile(inp2, "both")))
    print(f"{'✅' if n[1] == 0 else '⛔'} oncv_regen_check selftest {n[0]}/{n[0] + n[1]} 통과")
    return 0 if n[1] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
