#!/usr/bin/env python3
"""oncv_regen_check.py — PseudoDojo psp8 을 QE 용 UPF 로 옮기고, 그 변환이 맞는지 숫자로 대조한다 (+ ONCVPSP 재생성 대조).

왜 있나 (2026-10-19 · Nd Q3 ELF · 결정 D-2026-10-19-nd-q23-ppswap-structure · 사용자 '권고대로 해')
  ELF 규약은 NC pseudo 다 (run_lpsocl_elf_gabia.sh · 호스트 modelc ELF 표와 같은 규약). 4f 를 core 에 둔 NC Nd 는
  PseudoDojo (ONCVPSP-PBE-PDv0.4/Nd/Nd3+_f-in-core · ONCVPSP 3.2.3.1 · 가전자 5s²5p⁶5d¹6s² = 11) 에 psp8 로만 있다.
  ① 첫 계획 — 같은 입력으로 ONCVPSP 를 다시 돌려 UPF 를 같이 뽑는다 → **실패**: 손에 넣을 수 있는 판은 4.0.1 뿐이고
     (3.3.0 최적화 · 4.0.1 modcore 변경) 4.0.1 은 **다른 pseudo** 를 낸다 (r_core 2.109→2.112 · ekb 최대 83 % · l=0 GHOST(+) 경고 —
     3.2.3.1 출력에는 없다). 그 UPF 는 PseudoDojo 가 검증한 pseudo 가 아니다.
  ② 지금 경로 — 배포본 psp8 을 그대로 UPF 로 옮긴다 (--to_upf · ONCVPSP 4.0.1 upfout.f90 의 단위·격자 규약 · 보간 없음).
     변환이 맞는지는 **같은 4.0.1 실행이 쓴 psp8 · UPF 짝** 으로 잰다 (--compare_upf): psp8 격자 안 1e-10 일치 ·
     다른 것은 둘뿐이고 보고서에 따로 적는다 — 투영자 꼬리 (4.0.1 psp8 이 rc+2·drl 뒤를 '0.' 으로 쓴 1–3 점 · ≤1e-4) ·
     psp8 격자 (rchrg) 밖 (원본 UPF 는 17.55 bohr 까지 · 국소 퍼텐셜은 쿨롱과 ≤8.8e-5 Ry · 시작 밀도 0.27 e).

  python3 tools/electronic/oncv_regen_check.py --to_upf Nd3+_f-in-core.psp8 --dest Nd3+_f-in-core.dojo_psp8_conv.upf
  python3 tools/electronic/oncv_regen_check.py --compare_upf oncv401.upf conv401.upf --json cmp.json     # 같은 실행 짝 대조
  python3 tools/electronic/oncv_regen_check.py --compare Nd3+_f-in-core.psp8 regen.psp8 --tol 1e-3      # 재생성 psp8 대 배포본

⛔ 이 도구가 못 하는 것
  · pseudo 의 물리적 품질 (전이성 · 고스트) 을 판정하지 않는다 — PseudoDojo 검증 기록 (djrepo) 과 ONCVPSP 출력의 진단을 사람이 본다.
  · psp8 에 없는 것은 못 만든다 — PP_PSWFC (원자 파동함수 · QE 시작 파동함수가 무작위로 채워진다) · rchrg 밖의 국소 퍼텐셜
    (쿨롱으로 본다 = ABINIT 가 psp8 을 읽는 방식) · rchrg 밖의 시작 밀도. 그래서 **같은 pseudo 의 ONCVPSP UPF 와 절대 에너지가
    조금 다르다** — 2026-10-19 fcc Nd 실측 4.6 mRy · 1.5 kbar, 거의 전부 6–10 bohr 국소 퍼텐셜 꼬리 (G=0 상수항) 다
    (원본 UPF 의 그 꼬리만 쿨롱으로 바꾸면 0.05 mRy 안으로 맞는다). 밀도 · ELF 차는 최대 2e-5 · 1.7e-4.
    ⇒ 이 UPF 는 **밀도에서 나오는 양 (ELF · 밀도 그림)** 에 쓴다. 다른 pseudo 판과 절대 에너지를 섞지 않는다.
  · ONCVPSP 판이 다르면 재생성 psp8 은 배포본과 다를 수 있다 — --compare 는 그 차이를 재서 보고할 뿐이다 (기본 1e-3 · 넘으면 종료 1).
  · psp8 의 헤더 pspd (생성 날짜 코드) 와 첫 줄 제목은 --compare 가 보지 않는다 — 다시 뽑으면 당연히 다르다.
  · 지원: lloc = 4 · 스칼라 상대론 · 가전자 밀도가 든 psp8 (extension_switch 1) · PBE/PZ 만 (밖이면 멈춘다).
"""
import argparse
import hashlib
import json
import math
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
    # 제목 줄 (원소 · 판 · r_core) — compare() 는 안 본다 (다시 뽑으면 판 이름이 다르다) · psp8_to_upf 가 쓴다
    m = re.search(r"r_core=\s*(.*)$", L[0])
    hdr.update({"title": L[0].rstrip(), "atsym": (L[0].split() or [""])[0], "rc": _nums(m.group(1)) if m else []})
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
    return {"header": hdr, "blocks": blocks, "ekb": ekb, "echo": [s.rstrip() for s in L[i:]]}


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


_XC_UPF = {11: "PBE", -101130: "PBE", 2: "PZ", -1009: "PZ"}   # psp8 pspxc (ABINIT ixc · libxc 음수) → UPF functional


def _e20(vals, per=4):
    return ["".join(f"{v:20.10E}" for v in vals[k:k + per]) for k in range(0, len(vals), per)]


def psp8_to_upf(p, source=""):
    """psp8 (read_psp8) → UPF v2.0.1 본문 — ONCVPSP 4.0.1 src/upfout.f90 의 규약을 그대로 옮긴다.

    upfout 과 linout (psp8) 은 같은 로그 격자 배열을 **같은 선형 격자 rl = (i−1)·drl 에 같은 보간 (dpnint)** 으로 옮겨 쓴다.
    그래서 psp8 의 값에 단위만 곱하면 UPF 의 값이다 (r ≤ psp8 의 rchrg 구간):
      PP_LOCAL = 2·vloc (Ha → Ry) · PP_BETA = 투영자 그대로 (cutoff_radius_index = max_l(4 + int(rc_l/drl)) → 짝수 → 4 의 배수)
      PP_DIJ = 대각 2·ekb · PP_NLCC = core 첫 열 / 4π · PP_RHOATOM = r² × 가전자 첫 열
    ⛔ 못 하는 것: PP_PSWFC (psp8 에 원자 파동함수가 없다 → number_of_wfc 0 · QE 시작 파동함수는 무작위로 채워진다) ·
      psp8 격자 (rchrg) 밖의 값 — 원본 UPF 는 파동함수 꼬리까지 격자를 늘리지만 (upfout 'Updating nrl') psp8 에는 그 구간이 없다.
      그 구간의 PP_LOCAL 은 −2·Zion/r 이고 (QE 는 erf 로 뺀 나머지만 적분한다) PP_RHOATOM 은 시작 밀도뿐이다 —
      둘이 결과에 안 들어간다는 것은 같은 실행의 psp8·UPF 짝 대조 (compare_upf 의 'beyond') 와 QE 대조로 확인한다.
      lloc ≠ 4 · 스핀궤도 (extension_switch ≥ 2) · 가전자 밀도 없는 psp8 은 안 한다 (멈춘다)."""
    h, B = p["header"], p["blocks"]
    lmax, lloc, n = h["lmax"], h["lloc"], h["mmax"]
    if h["pspcod"] != 8:
        raise SystemExit(f"pspcod {h['pspcod']} — psp8 이 아니다")
    if lloc != 4:
        raise SystemExit(f"lloc {lloc} — 국소 퍼텐셜이 l 채널인 psp8 은 안 한다 (lloc = 4 만)")
    if not h["ext"] or h["ext"][0] != 1 or any(e >= 2 for e in h["ext"]) or "tail" not in B:
        raise SystemExit(f"extension_switch {h['ext']} — 가전자 밀도가 없거나 스핀궤도 psp8 (PP_RHOATOM 을 못 만든다)")
    if len(h.get("rc", [])) != lmax + 1:
        raise SystemExit(f"제목 줄 r_core 개수 {len(h.get('rc', []))} ≠ lmax+1 ({lmax + 1}) — cutoff_radius_index 를 못 정한다")
    xc = _XC_UPF.get(h["pspxc"])
    if xc is None:
        raise SystemExit(f"pspxc {h['pspxc']} — UPF functional 이름을 모른다 (PBE · PZ 만)")
    r = [row[1] for row in B["vloc"]]
    if len(r) != n or n < 8:
        raise SystemExit(f"국소 퍼텐셜 줄 수 {len(r)} ≠ mmax {n}")
    drl = r[1] - r[0]
    if r[0] != 0.0 or drl <= 0 or max(abs(r[k] - k * drl) for k in range(n)) > 1e-9:
        raise SystemExit("psp8 격자가 r = (i−1)·drl 선형 격자가 아니다")
    for name, rows in B.items():
        if len(rows) != n or max(abs(row[1] - r[k]) for k, row in enumerate(rows)) > 1e-6:
            raise SystemExit(f"{name} 블록의 격자가 국소 퍼텐셜 격자와 다르다")
    # cutoff_radius_index — upfout 규칙 (max_l 4 + int(rc_l/drl)) 과 '마지막 0 아닌 점' 중 큰 쪽 → 짝수 → 4 의 배수.
    #   4.0.1 psp8 (linout) 은 rc_l + 2·drl 뒤를 f4.0 '0.' 으로 자르지만 3.2.3.1 psp8 은 보간 잔물결 (rc 뒤 ~0.1 bohr ·
    #   PseudoDojo Nd3+ l=3 에서 최대의 1.7e-3) 을 끝까지 쓴다 — ABINIT 가 검증에 쓴 그 값을 버리지 않는다.
    cols = [(l, jj, [row[2 + jj] for row in B[f"proj_l{l}"]]) for l in range(lmax + 1) for jj in range(h["nproj"][l])]
    last_nz = max((max((k + 1 for k, v in enumerate(c) if v != 0.0), default=0) for _, _, c in cols), default=0)
    nrlproj = max(max(4 + int(rc / drl + 1e-6) for rc in h["rc"]), last_nz)
    nrlproj += nrlproj % 2
    if nrlproj % 4:
        nrlproj += 2
    if nrlproj > n:
        raise SystemExit(f"cutoff_radius_index {nrlproj} > 격자 {n}")
    betas = [(l, c[:nrlproj]) for l, _, c in cols]
    dij = [2.0 * p["ekb"][l][jj] for l, jj, _ in cols]
    nb = len(betas)
    core = h["fchrg"] > 0
    ln = []
    ln += ['<UPF version="2.0.1">', "  <PP_INFO>",
           " Converted from psp8 by tools/electronic/oncv_regen_check.py --to_upf",
           " (unit and grid conventions of ONCVPSP 4.0.1 src/upfout.f90; no interpolation).",
           f" Source psp8: {source}" if source else " Source psp8: (not given)",
           f" psp8 title: {h['title']}",
           " No pseudo-atomic wavefunctions in psp8: number_of_wfc = 0.",
           "    <PP_INPUTFILE>"]
    ln += [s for s in p.get("echo", []) if s.strip() and not s.strip().startswith(("<", "END_PSP"))
           and "<" not in s and "&" not in s]
    ln += ["    </PP_INPUTFILE>", "  </PP_INFO>", "  <!--                               -->",
           "  <!-- END OF HUMAN READABLE SECTION -->", "  <!--                               -->", "    <PP_HEADER"]
    hv = [("generated", "Generated using ONCVPSP code by D. R. Hamann (converted from psp8)"), ("author", "anonymous"),
          ("date", ""), ("comment", ""), ("element", f"{h['atsym']:2s}"), ("pseudo_type", "NC"), ("relativistic", "scalar"),
          ("is_ultrasoft", "F"), ("is_paw", "F"), ("is_coulomb", "F"), ("has_so", "F"), ("has_wfc", "F"), ("has_gipaw", "F"),
          ("core_correction", "T" if core else "F"), ("functional", xc), ("z_valence", f"{h['zion']:8.2f}"),
          ("rho_cutoff", f"{r[-1]:20.11E}"), ("l_max", f"{lmax}"), ("l_local", "-1"), ("mesh_size", f"{n:6d}"),
          ("number_of_wfc", "0"), ("number_of_proj", f"{nb}")]
    ln += [f'       {k}="{v}"' for k, v in hv]
    ln[-1] += "/>"
    ln += [" <PP_MESH>", f'   <PP_R type="real"  size="{n:4d}" columns="8">']
    ln += ["".join(f"{v:10.4f}" for v in r[k:k + 8]) for k in range(0, n, 8)]
    ln += ["   </PP_R>", f'   <PP_RAB type="real"  size="{n:4d}" columns="8">']
    ln += ["".join(f"{drl:10.4f}" for _ in range(min(8, n - k))) for k in range(0, n, 8)]
    ln += ["   </PP_RAB>", " </PP_MESH>", f'  <PP_LOCAL type="real"  size="{n:4d}" columns="4">']
    ln += _e20([2.0 * row[2] for row in B["vloc"]])
    ln += ["  </PP_LOCAL>", " <PP_NONLOCAL>"]
    for i, (l, v) in enumerate(betas, 1):
        ln += [f"   <PP_BETA.{i}", '       type="real"', f'       size="{n:4d}"', '       columns="4"', f'       index="{i}"',
               f'       angular_momentum="{l}"', f'       cutoff_radius_index="{nrlproj:4d}"',
               f'       cutoff_radius="{(nrlproj - 1) * drl:20.10E}" >']
        ln += _e20(v)
        z = n - nrlproj
        ln += [" 0." * min(4, z - k) for k in range(0, z, 4)]
        ln += [f"   </PP_BETA.{i}>"]
    ln += [f'   <PP_DIJ type="real"  size="{nb * nb:4d}" columns="4">']
    ln += _e20([dij[i] if i == j else 0.0 for j in range(nb) for i in range(nb)])
    ln += ["   </PP_DIJ>", " </PP_NONLOCAL>", " <PP_PSWFC>", " </PP_PSWFC>"]
    if core:
        ln += [f' <PP_NLCC type="real"  size="{n:4d}" columns="4">']
        ln += _e20([row[2] / (4.0 * math.pi) for row in B["core"]])
        ln += [" </PP_NLCC>"]
    ln += [f' <PP_RHOATOM type="real"  size="{n:4d}" columns="4">']
    ln += _e20([r[k] ** 2 * row[2] for k, row in enumerate(B["tail"])])
    ln += [" </PP_RHOATOM>", "</UPF>"]
    return "\n".join(ln) + "\n"


def read_upf(path):
    """UPF v2 → {header, PP_R, PP_RAB, PP_LOCAL, PP_DIJ, PP_NLCC, PP_RHOATOM, betas[{l, cut, v}], chi[]} (정규식 · stdlib)."""
    s = Path(path).read_text()
    m = re.search(r"<PP_HEADER\b(.*?)/>", s, re.S)
    if not m:
        raise SystemExit(f"{path}: PP_HEADER 가 없다 (UPF v2 가 아니다)")
    attr = lambda t: {k: v.strip() for k, v in re.findall(r'(\w+)\s*=\s*"([^"]*)"', t)}

    def arr(tag):
        mm = re.search(rf"<{re.escape(tag)}\b([^>]*)>(.*?)</{re.escape(tag)}>", s, re.S)
        if not mm:
            return None, {}
        return [_f(t) for t in mm.group(2).split()], attr(mm.group(1))
    out = {"header": attr(m.group(1))}
    for tag in ("PP_R", "PP_RAB", "PP_LOCAL", "PP_DIJ", "PP_NLCC", "PP_RHOATOM"):
        out[tag] = arr(tag)[0]
    out["betas"] = []
    for i in range(1, int(out["header"].get("number_of_proj", "0")) + 1):
        v, at = arr(f"PP_BETA.{i}")
        if v is None:
            raise SystemExit(f"{path}: PP_BETA.{i} 가 없다")
        out["betas"].append({"l": int(at.get("angular_momentum", "-1")), "cut": int(at.get("cutoff_radius_index", "0") or 0), "v": v})
    out["chi"] = [arr(f"PP_CHI.{i}")[0] for i in range(1, int(out["header"].get("number_of_wfc", "0")) + 1)]
    return out


def _trapz(y, dx):
    return dx * (sum(y) - 0.5 * (y[0] + y[-1])) if len(y) > 1 else 0.0


TAIL_PTS = 4   # psp8 꼬리 창 (점) — 실물 4.0.1 짝에서 잔물결은 rc_l + 2·drl 뒤 1–3 점


def compare_upf(a, b, tol=1e-8, tail_tol=1e-3):
    """두 UPF (read_upf) → (ok, report). 헤더 (물리 항목) 는 같아야 하고 배열은 **짧은 쪽 격자까지** 상대 ≤ tol.
    긴 쪽에만 있는 구간은 'beyond' 에 따로 적는다 (ok 에 안 넣는다): PP_LOCAL 이 −2·Zion/r 에서 벗어난 최대 · 그 구간의 PP_RHOATOM 전하."""
    rep, ok = {"tol_rel": tol, "header_mismatch": [], "arrays": {}, "beyond": {}}, True
    for k in ("element", "pseudo_type", "relativistic", "is_ultrasoft", "is_paw", "has_so", "core_correction", "functional",
              "l_max", "l_local", "number_of_proj"):
        if a["header"].get(k) != b["header"].get(k):
            rep["header_mismatch"].append(f"{k}: {a['header'].get(k)} ≠ {b['header'].get(k)}")
    za, zb = float(a["header"].get("z_valence", "nan")), float(b["header"].get("z_valence", "nan"))
    if not abs(za - zb) < 1e-9:
        rep["header_mismatch"].append(f"z_valence: {za} ≠ {zb}")
    if rep["header_mismatch"] or len(a["betas"]) != len(b["betas"]):
        rep["header_mismatch"] += [] if len(a["betas"]) == len(b["betas"]) else [f"투영자 수 {len(a['betas'])} ≠ {len(b['betas'])}"]
        return False, rep
    n = min(len(a["PP_R"]), len(b["PP_R"]))

    def cmp(name, x, y, nn=n):
        nonlocal ok
        if x is None and y is None:
            return
        if x is None or y is None or len(x) < nn or len(y) < nn:
            rep["arrays"][name] = {"ok": False, "why": "한쪽에 없거나 짧다"}; ok = False; return
        scale = max(abs(v) for v in x[:nn]) or 1.0
        d = max(abs(p_ - q) for p_, q in zip(x[:nn], y[:nn]))
        good = d / scale <= tol
        rep["arrays"][name] = {"n": nn, "max_abs_diff": d, "max_abs_value": scale, "rel": d / scale, "ok": good}
        ok &= good
    for name in ("PP_R", "PP_RAB", "PP_LOCAL", "PP_NLCC", "PP_RHOATOM"):
        cmp(name, a[name], b[name])
    for i, (x, y) in enumerate(zip(a["betas"], b["betas"]), 1):
        if x["l"] != y["l"]:
            rep["arrays"][f"PP_BETA.{i}"] = {"ok": False, "why": f"l {x['l']} ≠ {y['l']}"}; ok = False; continue
        # psp8 꼬리: linout 은 r > rc_l + 2·drl 의 투영자를 f4.0 ('0.') 으로 쓴다 — upfout 은 보간 잔물결 (몇 점 · ≲1e-4) 을 그대로 쓴다.
        #   new 가 그 지점부터 끝까지 정확히 0 이면, 0 이 시작한 뒤 TAIL_PTS 점 안의 차는 '꼬리' 로 따로 적고 (상대 ≤ tail_tol)
        #   그 밖의 차만 tol 로 본다. 0 이 일찍 시작하면 (변환기가 투영자를 자른 것) 꼬리 창 밖 차가 남아 잡힌다.
        yv, xv = y["v"], x["v"]
        z0 = len(yv)
        while z0 > 0 and yv[z0 - 1] == 0.0:
            z0 -= 1
        tail = range(z0, min(z0 + TAIL_PTS, n))
        xs = [0.0 if k in tail else v for k, v in enumerate(xv)]
        cmp(f"PP_BETA.{i}", xs, yv)
        tmax = max((abs(xv[k]) for k in tail), default=0.0)
        scale = max(abs(v) for v in xv[:n]) or 1.0
        rb = rep["arrays"][f"PP_BETA.{i}"]
        rb.update({"cutoff_radius_index": [x["cut"], y["cut"]], "zero_tail_from_index": z0 + 1,
                   "tail_max_abs": tmax, "tail_rel": tmax / scale, "tail_ok": tmax / scale <= tail_tol})
        if not rb["tail_ok"]:
            rb["ok"] = False; ok = False
    cmp("PP_DIJ", a["PP_DIJ"], b["PP_DIJ"], len(a["PP_DIJ"] or []))
    L = a if len(a["PP_R"]) > len(b["PP_R"]) else b
    if len(L["PP_R"]) > n:
        rr, zv = L["PP_R"], za
        dev = max(abs(L["PP_LOCAL"][k] + 2.0 * zv / rr[k]) for k in range(n, len(rr)))
        dr = rr[1] - rr[0]
        rho = L["PP_RHOATOM"]
        rep["beyond"] = {"longer": "ref" if L is a else "new", "r_from": rr[n], "r_to": rr[-1],
                         "max_abs_local_minus_coulomb_Ry": dev, "rhoatom_charge_beyond": _trapz(rho[n - 1:], dr),
                         "rhoatom_charge_total_longer": _trapz(rho, dr)}
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
    ap.add_argument("--tol", type=float, default=None, help="--compare 1e-3 · --compare_upf 1e-8 (기본)")
    ap.add_argument("--to_upf", metavar="PSP8", help="psp8 → UPF v2 (--dest) · upfout.f90 규약")
    ap.add_argument("--compare_upf", nargs=2, metavar=("REF_UPF", "NEW_UPF"))
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
        tol = 1e-3 if a.tol is None else a.tol
        ok, rep = compare(read_psp8(a.compare[0]), read_psp8(a.compare[1]), tol)
        rep.update({"ref": a.compare[0], "new": a.compare[1], "ok": ok})
        for m in rep["header_mismatch"]:
            print(f"  ✗ 헤더 {m}")
        for n, r in rep["blocks"].items():
            print(f"  {'✓' if r.get('ok') else '✗'} {n:8s} " + (f"상대 {r['rel']:.2e} (최대 |Δ| {r['max_abs_diff']:.2e} / {r['max_abs_value']:.2e})" if "rel" in r else "모양 다름"))
        for l, r in rep["ekb"].items():
            print(f"  {'✓' if r['ok'] else '✗'} ekb l={l} 상대 {r['rel']:.2e}")
        print(f"{'✅ 같은 pseudo (상대 ≤ ' + str(tol) + ')' if ok else '⛔ 다르다'}")
        if a.json:
            Path(a.json).write_text(json.dumps(rep, ensure_ascii=False, indent=1) + "\n")
        return 0 if ok else 1
    if a.to_upf:
        src = f"{Path(a.to_upf).name} sha256 {hashlib.sha256(Path(a.to_upf).read_bytes()).hexdigest()} md5 {md5(a.to_upf)}"
        Path(a.dest).write_text(psp8_to_upf(read_psp8(a.to_upf), src))
        u = read_upf(a.dest)
        print(f"→ {a.dest} · 격자 {len(u['PP_R'])} (r ≤ {u['PP_R'][-1]:.2f}) · 투영자 {len(u['betas'])} "
              f"(cutoff_radius_index {u['betas'][0]['cut'] if u['betas'] else '—'}) · z_valence {u['header']['z_valence']} · wfc 0")
        return 0
    if a.compare_upf:
        tol = 1e-8 if a.tol is None else a.tol
        ok, rep = compare_upf(read_upf(a.compare_upf[0]), read_upf(a.compare_upf[1]), tol)
        rep.update({"ref": a.compare_upf[0], "new": a.compare_upf[1], "ok": ok})
        for m in rep["header_mismatch"]:
            print(f"  ✗ 헤더 {m}")
        for nme, r in rep["arrays"].items():
            print(f"  {'✓' if r.get('ok') else '✗'} {nme:11s} " + (f"상대 {r['rel']:.2e} (|Δ| {r['max_abs_diff']:.2e} / {r['max_abs_value']:.2e} · {r['n']} 점)"
                  + (f" · cut {r['cutoff_radius_index']} · psp8 꼬리 (점 {r['zero_tail_from_index']}~) 상대 {r['tail_rel']:.1e}"
                     if 'cutoff_radius_index' in r else "") if "rel" in r else r.get("why", "")))
        if rep["beyond"]:
            b = rep["beyond"]
            print(f"  · 긴 쪽 ({b['longer']}) 에만 있는 r {b['r_from']:.2f}–{b['r_to']:.2f}: PP_LOCAL − (−2Zv/r) 최대 {b['max_abs_local_minus_coulomb_Ry']:.2e} Ry"
                  f" · PP_RHOATOM 전하 {b['rhoatom_charge_beyond']:.4f} / 전체 {b['rhoatom_charge_total_longer']:.4f}")
        print(f"{'✅ 같은 값 (상대 ≤ ' + str(tol) + ' · 짧은 격자까지)' if ok else '⛔ 다르다'}")
        if a.json:
            Path(a.json).write_text(json.dumps(rep, ensure_ascii=False, indent=1) + "\n")
        return 0 if ok else 1
    ap.error("할 일을 하나 고른다 (--compare · --compare_upf · --to_upf · --extract · --set_psfile · --md5 · --selftest)")


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
    # ── psp8 → UPF 변환 · UPF 대조 ───────────────────────────────────────────────────────────
    def p8(mmax=40, lloc=4, pspxc=11, rc="0.10000   0.12000", dr=0.01, bump=None, ext="1 1", far=None, tailpts=True):
        r = [dr * k for k in range(mmax)]
        if bump is not None:
            r[bump] += 0.003
        rcs = [float(x) for x in rc.split()]
        def pv(l, j, k):   # rc_l + 2·drl 안쪽만 값 · 밖은 0 (4.0.1 꼴) · far=(l, k) 면 그 점에 잔물결 하나
            if far and far == (l, k):
                return 3e-3
            rl_ = rcs[min(l, len(rcs) - 1)]   # 'r_core 개수' 음성 시험은 rc 하나만 준다
            return (j + 1) * (1.0 + 0.1 * k) * (1 - r[k] / (rl_ + 0.0201)) if r[k] <= rl_ + 0.0201 else 0.0
        s_ = ["Nd    ONCVPSP-x  r_core=   " + rc, "60.0000  11.0000  170524  zatom,zion,pspd",
              f"8  {pspxc}  1  {lloc}  {mmax}  0  pspcod,pspxc,lmax,lloc,mmax,r2well", f"{r[-1]:.8f}  5.40  0.0  rchrg fchrg qchrg",
              "2  1  0  0  0  nproj", f"{ext}  extension_switch", "0  6.25D+00  6.6D-01"]
        s_ += [f"{k + 1}  {r[k]:.13E}  {pv(0, 0, k):.13E}  {pv(0, 1, k):.13E}" for k in range(mmax)]
        s_ += ["1  -1.5D+00"] + [f"{k + 1}  {r[k]:.13E}  {pv(1, 0, k):.13E}" for k in range(mmax)]
        s_ += ["4"] + [f"{k + 1}  {r[k]:.13E}  {-11.0 / max(r[k], 0.5):.13E}" for k in range(mmax)]
        s_ += [f"{k + 1}  {r[k]:.13E}  {2.0 / (1 + k):.13E}  0.0  0.0  0.0  0.0" for k in range(mmax)]
        if tailpts:
            s_ += [f"{k + 1}  {r[k]:.13E}  {0.3 / (1 + k):.13E}  0.0  0.0" for k in range(mmax)]
        s_ += ["<INPUT>", "# ATOM AND REFERENCE CONFIGURATION", "  Nd 60.00 10 4 4 psp8", "# a & b", "</INPUT>"]
        return "\n".join(s_) + "\n"
    (T / "u.psp8").write_text(p8())
    pu = read_psp8(T / "u.psp8")
    (T / "u.upf").write_text(psp8_to_upf(pu, "u.psp8"))
    U = read_upf(T / "u.upf")
    r_ = [0.01 * k for k in range(40)]
    ck("to_upf: PP_LOCAL = 2·vloc · NLCC = core/4π · RHOATOM = r²·가전자 · DIJ = 대각 2·ekb",
       max(abs(U["PP_LOCAL"][k] - 2 * (-11.0 / max(r_[k], 0.5))) for k in range(40)) < 1e-8
       and max(abs(U["PP_NLCC"][k] - 2.0 / (1 + k) / (4 * math.pi)) for k in range(40)) < 1e-10
       and max(abs(U["PP_RHOATOM"][k] - r_[k] ** 2 * 0.3 / (1 + k)) for k in range(40)) < 1e-10
       and [U["PP_DIJ"][0], U["PP_DIJ"][4], U["PP_DIJ"][8]] == [12.5, 1.32, -3.0] and sum(abs(x) for x in U["PP_DIJ"]) == 12.5 + 1.32 + 3.0,
       str(U["PP_DIJ"]))
    ck("to_upf: 헤더 (z 11 · PBE · l_max 1 · 투영자 3 · wfc 0 · NLCC T) · cutoff 16 (= 4+int(0.12/0.01) → 4 의 배수)",
       U["header"]["z_valence"] == "11.00" and U["header"]["functional"] == "PBE" and U["header"]["l_max"] == "1"
       and len(U["betas"]) == 3 and U["header"]["number_of_wfc"] == "0" and U["header"]["core_correction"] == "T"
       and [b_["cut"] for b_ in U["betas"]] == [16, 16, 16] and [b_["l"] for b_ in U["betas"]] == [0, 0, 1], str(U["header"]))
    ck("to_upf: PP_INFO 에 '<' '&' 줄을 안 옮긴다 (QE xml 이 깨진다)",
       "a & b" not in (T / "u.upf").read_text() and "<INPUT>" not in (T / "u.upf").read_text())
    ok_s, rep_s = compare_upf(U, U)
    ck("compare_upf: 자기 자신 = 같다 (상대 0)", ok_s and all(r.get("rel", 0) == 0 for r in rep_s["arrays"].values()))
    (T / "far.psp8").write_text(p8(far=(1, 30)))
    (T / "far.upf").write_text(psp8_to_upf(read_psp8(T / "far.psp8")))
    Uf = read_upf(T / "far.upf")
    ck("to_upf: rc 밖 잔물결 (3.2.3.1 꼴) 이 있으면 cutoff 를 늘려 버리지 않는다 (점 31 → 32)",
       Uf["betas"][2]["cut"] == 32 and Uf["betas"][2]["v"][30] == 3e-3, str([b_["cut"] for b_ in Uf["betas"]]))
    def mut(text, tag, k, fac):   # UPF 의 tag 배열 k 번째 값만 fac 배
        i0 = text.index(">", text.index("<" + tag)) + 1; i1 = text.index("</" + tag)
        v = [_f(t) for t in text[i0:i1].split()]; v[k] *= fac
        return text[:i0] + "\n" + "\n".join("".join(f"{x:20.10E}" for x in v[j:j + 4]) for j in range(0, len(v), 4)) + "\n" + text[i1:]
    base = (T / "u.upf").read_text()
    (T / "m1.upf").write_text(mut(base, "PP_BETA.1", 5, 1 + 1e-6))
    ck("⛔음성: 투영자 안쪽 값 1e-6 차를 잡는다 (tol 1e-8)", not compare_upf(U, read_upf(T / "m1.upf"))[0])
    (T / "m2.upf").write_text(mut(base, "PP_DIJ", 4, 1.001))
    ck("⛔음성: DIJ 0.1 % 차를 잡는다", not compare_upf(U, read_upf(T / "m2.upf"))[0])
    (T / "m3.upf").write_text(base.replace('z_valence="   11.00"', 'z_valence="   12.00"'))
    ck("⛔음성: z_valence 가 다르면 다르다", not compare_upf(U, read_upf(T / "m3.upf"))[0])
    # 변환기가 투영자를 일찍 자르는 버그 — new 의 0 꼬리가 안쪽에서 시작하면 꼬리 창 (4 점) 밖 차가 남아 잡혀야 한다
    i0 = base.index(">", base.index("<PP_BETA.1")) + 1; i1 = base.index("</PP_BETA.1")
    v = [_f(t) for t in base[i0:i1].split()]; v = v[:5] + [0.0] * (len(v) - 5)
    (T / "m4.upf").write_text(base[:i0] + "\n" + "\n".join("".join(f"{x:20.10E}" for x in v[j:j + 4]) for j in range(0, len(v), 4)) + "\n" + base[i1:])
    ck("⛔음성: 투영자를 안쪽 (점 6) 부터 0 으로 자르면 잡는다 (꼬리 창으로 덮이지 않는다)", not compare_upf(U, read_upf(T / "m4.upf"))[0])
    # 꼬리 창 안 (마지막 0 아닌 점 1 개를 0 으로) — 꼬리로 따로 적고 ok (상대 ≤ tail_tol)
    last = max(k for k, x in enumerate(U["betas"][0]["v"]) if x != 0.0)
    v5 = list(U["betas"][0]["v"]); small = v5[last]; v5[last] = 0.0
    i0 = base.index(">", base.index("<PP_BETA.1")) + 1; i1 = base.index("</PP_BETA.1")
    (T / "m5.upf").write_text(base[:i0] + "\n" + "\n".join("".join(f"{x:20.10E}" for x in v5[j:j + 4]) for j in range(0, len(v5), 4)) + "\n" + base[i1:])
    ok5, rep5 = compare_upf(U, read_upf(T / "m5.upf"), tail_tol=1.0)
    ck("꼬리 창 안의 차 (psp8 '0.' 절단) 는 따로 적고 ok", ok5 and rep5["arrays"]["PP_BETA.1"]["tail_max_abs"] == abs(small), str(rep5["arrays"]["PP_BETA.1"]))
    ck("⛔음성: 꼬리 차가 tail_tol 을 넘으면 다르다", not compare_upf(U, read_upf(T / "m5.upf"), tail_tol=1e-9)[0])
    # 창 크기 자체를 재는 시험: 기준 쪽에 작은 잔물결 (상대 1e-5 · tail_tol 아래) 이 8 점 · new 는 그걸 다 0 으로 —
    #   앞 TAIL_PTS 점만 꼬리로 봐주고 나머지는 잡혀야 한다 (창이 넓으면 tail_tol 도 못 잡는다)
    v6 = list(U["betas"][0]["v"]); mx6 = max(abs(x) for x in v6)
    for k in range(last + 1, last + 9):
        v6[k] = 1e-5 * mx6
    (T / "m6.upf").write_text(base[:i0] + "\n" + "\n".join("".join(f"{x:20.10E}" for x in v6[j:j + 4]) for j in range(0, len(v6), 4)) + "\n" + base[i1:])
    ck("⛔음성: 꼬리 창 (4 점) 밖의 작은 잔물결 (tail_tol 아래) 을 0 으로 버리면 잡는다", not compare_upf(read_upf(T / "m6.upf"), U)[0])
    (T / "long.psp8").write_text(p8(mmax=60))
    ok_l, rep_l = compare_upf(read_upf(T / "u.upf"), (lambda f: (f.write_text(psp8_to_upf(read_psp8(T / "long.psp8"))), read_upf(f))[1])(T / "long.upf"))
    ck("긴 격자 쪽 구간은 'beyond' 로 따로 적는다 (쿨롱 편차 · 전하) · 공통 구간은 같다",
       ok_l and rep_l["beyond"].get("longer") == "new" and rep_l["beyond"]["rhoatom_charge_beyond"] > 0, str(rep_l["beyond"]))
    for name, kw, why in (("lloc", {"lloc": 1}, "lloc ≠ 4"), ("xc", {"pspxc": 7}, "pspxc 모름"), ("rc", {"rc": "0.10000"}, "r_core 개수"),
                          ("grid", {"bump": 7}, "격자 비선형"), ("ext", {"ext": "0 0", "tailpts": False}, "가전자 밀도 없음")):
        f = T / f"bad_{name}.psp8"; f.write_text(p8(**kw))
        ck(f"⛔음성: to_upf 가 멈춘다 — {why}", raises(lambda: psp8_to_upf(read_psp8(f))))
    print(f"{'✅' if n[1] == 0 else '⛔'} oncv_regen_check selftest {n[0]}/{n[0] + n[1]} 통과")
    return 0 if n[1] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
