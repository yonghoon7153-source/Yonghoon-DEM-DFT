#!/usr/bin/env python3
"""cathode_reactivity.py — cascade 코팅 후보 × 양극 계면 반응성 게이트 (open_items M6).

문헌 근거
---------
Richards/Ong 2016 (Chem. Mater. 28, 266) pseudo-binary eq 2 (**닫힌계**): 두 상을 x:(1-x)로
섞어 convex hull 로 떨어뜨렸을 때의 최악(가장 음수) 반응에너지를 x 에 대해 최소화.
Xiao/Ceder 2019 (Joule 3, 1252) F4 게이트: |dE_rxt| < 100 meV/atom 을 통과해야 코팅 후보.
litdb/papers/xiao2019_cathode_coating_screening.md 227번 줄:
  "pseudo-binary dE_rxt: 두 상을 x:(1-x)로 섞어 hull로 떨어지는 최악 반응에너지(Eq 4)
   — 계면 반응성 프록시(**닫힌계**)"

⚠ 축은 전위가 아니라 **양극 리튬화 상태**다. digest 222번 줄이
  "bare Li6PS5Cl reacts with LiCoO2 at -339 meV/atom (fully lithiated; -493 half-lithiated)"
라고 명시한다. 즉 만충/반충은 LiCoO2 / Li0.5CoO2 라는 **조성 축**이지 mu_Li 를 여는
grand-potential 전위 축이 아니다.
  (초판에서 GrandPotentialInterfacialReactivity + 전위 스캔으로 돌렸다가 -810~-1544 meV/atom
   이 나왔고, V=4.30 반응식이 "Li6PS5Cl -> 6 Li + SCl + 0.5 P2S7 + 0.5 S" 로 **양극이 아예
   빠진 자체분해**였다. Li 저장소를 열면 코팅의 탈리튬 분해가 상호반응을 압도한다.
   tools/oxidation/interface_reactivity_v2.py 의 개방계는 Li 음극 쪽 문제에 맞는 도구이고,
   양극 쪽 F4 게이트는 이 닫힌계가 맞다.)

2단 구조
--------
  1) --validate : LPSCl(우리 host) vs 양극만 먼저 계산 → Xiao 소환값과 대조.
     기대 앵커: LPSCl/LCO -339(만충)/-493(반충), LPSCl/NCM -330(만충)/-471(반충) meV/atom.
     판정: 부호(음수) · 자릿수(앵커의 0.5~2.0배) · 순서(반충이 더 발열). 소수점 일치는 요구 안 함
     (MP hull 세대 차 때문). 불일치 시 원인 후보를 출력하고 **생산 실행을 막는다**(--force 우회).
  2) (검증 통과 후) --run : 47 코팅 후보 전수 → db/properties/cathode_reactivity_cascade.csv

⚠⚠ 2026-07-28 축 추가: 초판은 **양극만** 계산했다. Kim 2026 (Nano Convergence 13, 27,
`litdb/papers/kim2026_hts_li3sc2po43_coating_midni_ncm.md`) Table S1 이 88 후보에 대해
NCM523 과 LPSCl **양쪽** dE_rxn 을 싣는데, 다수가 양극과는 0 인데 LPSCl 과는 -50~-99 meV
(Li2TiO3 0/-60 · Li3NbO4 0/-96 · Li2SO4 0/-99 · LiSrBO3 0/-96). 본문도 "many materials
exhibited stable interfaces with the NCM523, a substantial fraction fail to maintain
stability against LPSC" 라고 명시한다. **구속은 SE 쪽이 건다.**
양극만 보고 "게이트가 vacuous 하다"고 낸 우리 초판 판정은 **쉬운 쪽만 본 결과**였다.

비용 주의
--------
코팅마다 chemsys 가 달라 MP 쿼리가 코팅당 1회. LCO(=Li-Co-O + 코팅원소)는 4~5원소라 가볍고,
NCM811(Li-Ni-Co-Mn-O + 코팅)은 6~7원소라 PhaseDiagram 구성이 급격히 비싸진다. 기본은 LCO,
NCM 은 --cathodes 로 명시할 때만. 엔트리는 --cache 디렉터리에 저장되어 재실행 시 재사용된다.
같은 원소집합이면 만충/반충이 캐시를 공유하므로 쌍으로 도는 비용은 1회분이다.

실행 (gabia/kgy, MP_API_KEY 설정된 셸)
  python3 tools/cascade/cathode_reactivity.py --validate
  python3 tools/cascade/cathode_reactivity.py --run
"""
import argparse
import csv
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROP = ROOT / "db" / "properties"

# Xiao 2019 소환값 (meV/atom) — 우리 계산값과 절대 혼합 금지, 검증 대조용.
XIAO_ANCHOR = {
    ("LPSCl", "LCO"): {"full": -339, "half": -493},
    ("LPSCl", "NCM"): {"full": -330, "half": -471},
}
GATE_MEV = 100.0          # Xiao F4: |dE_rxt| < 100 meV/atom
# 기본 상대 = 양극(완전/반리튬화) + **SE(LPSCl)**.
# ⚠ SE 축은 나중에 추가됐다 — Kim 2026 (Nano Convergence 13, 27) Table S1 이
# "많은 산화물이 NCM523 과는 안정하지만 상당수가 LPSCl 에 대해 실패한다"를 보였고
# (Li2TiO3 0 vs -60 / Li3NbO4 0 vs -96 / Li2SO4 0 vs -99 meV/atom),
# 양극만 계산한 우리 초판이 **쉬운 쪽만 보고 게이트가 vacuous 하다고 오판**했다.
# 구속을 거는 쪽은 양극이 아니라 SE 다.
DEFAULT_CATHODES = ["LiCoO2:LCO:full", "Li0.5CoO2:LCO:half", "Li6PS5Cl:LPSCl:se"]
# 검증 허용대: |our| 가 |anchor| 의 이 배율 범위 안이면 "자릿수 OK"
BAND_LO, BAND_HI = 0.5, 2.0


# ── MP API 키 탐색 ─────────────────────────────────────────────
def _find_api_key():
    """env → ~/.pmgrc.yaml → ~/.config/.pmgrc.yaml 순. pymatgen이 키를 쓰는 표준 위치까지 훑는다."""
    for v in ("MP_API_KEY", "PMG_MAPI_KEY"):
        k = os.environ.get(v)
        if k and len(k.strip()) >= 15:
            print(f"[key] 환경변수 {v} 사용")
            return k.strip()
    import re as _re
    for p in (Path.home() / ".pmgrc.yaml", Path.home() / ".config" / ".pmgrc.yaml"):
        if not p.exists():
            continue
        m = _re.search(r"PMG_MAPI_KEY\s*:\s*['\"]?([A-Za-z0-9]{15,})", p.read_text())
        if m:
            print(f"[key] {p} 에서 발견")
            return m.group(1)
    sys.exit(
        "MP API 키를 못 찾음. 아래 중 하나로 지정하세요:\n"
        "  export MP_API_KEY=<32자 키>\n"
        "  또는  pmg config --add PMG_MAPI_KEY <32자 키>   (~/.pmgrc.yaml 에 저장)\n"
        "키 위치 탐색:  grep -rl 'MP_API_KEY\\|PMG_MAPI_KEY' ~/.bashrc ~/.profile ~/.pmgrc.yaml "
        "~/work ~/*.sh 2>/dev/null")


# ── MP 엔트리 (캐시) ────────────────────────────────────────────
def get_entries(elements, cache_dir):
    key = "-".join(sorted(elements))
    cp = Path(cache_dir) / f"{key}.json"
    if cp.exists():
        from monty.json import MontyDecoder
        entries = json.loads(cp.read_text(), cls=MontyDecoder)
        print(f"[cache] {len(entries):5d} entries  {key}")
        return entries
    api = _find_api_key()
    from mp_api.client import MPRester
    with MPRester(api) as mpr:
        entries = mpr.get_entries_in_chemsys(
            sorted(elements), additional_criteria={"thermo_types": ["GGA_GGA+U"]})
    cp.parent.mkdir(parents=True, exist_ok=True)
    from monty.json import MontyEncoder
    cp.write_text(json.dumps(entries, cls=MontyEncoder))
    print(f"[mp_api] {len(entries):5d} entries  {key}  → cached")
    return entries


def min_rxn_closed(c_coat, c_cath, pd):
    """Richards eq 2 (닫힌계) pseudo-binary: 혼합 분율 x 최소화.
    Xiao F4가 쓰는 바로 그 양이다 — Li 저장소를 열지 않으므로 코팅 자체분해가
    섞이지 않고 **상호 반응**만 남는다. 반환 (meV/atom, 반응식)."""
    from pymatgen.analysis.interface_reactions import InterfacialReactivity
    try:
        ir = InterfacialReactivity(c_coat, c_cath, pd, norm=True, use_hull_energy=True)
    except TypeError:                       # pymatgen 버전차 방어
        ir = InterfacialReactivity(c_coat, c_cath, pd)
    best_e, best_rxn = 1e9, None
    for k in ir.get_kinks():
        e = float(k[2])
        if e < best_e:
            best_e, best_rxn = e, str(k[3])
    if best_rxn is None:
        raise RuntimeError("get_kinks()가 비었음 — PhaseDiagram/조성 확인")
    return best_e * 1000.0, best_rxn      # eV/atom → meV/atom


_PD_MEMO = {}                 # chemsys key → PhaseDiagram


def _phase_diagram(elem_syms, cache_dir):
    """chemsys 별 PhaseDiagram 메모. 만충/반충은 원소집합이 같아 PD 를 공유한다
    (PD 구성이 이 스크립트의 지배 비용이라 47종 × 2상태에서 절반이 그냥 사라진다)."""
    key = "-".join(sorted(elem_syms))
    if key not in _PD_MEMO:
        from pymatgen.analysis.phase_diagram import PhaseDiagram
        _PD_MEMO[key] = PhaseDiagram(get_entries(sorted(elem_syms), cache_dir))
        print(f"[pd] PhaseDiagram 구성  {key}")
    return _PD_MEMO[key]


def scan(coat_str, cath_str, cache_dir):
    """한 (코팅, 양극조성) 쌍의 닫힌계 pseudo-binary 반응. 반환 (meV, rxn).
    실패 시 (None, 'ERR ...')."""
    from pymatgen.core import Composition, Element
    elems = set(Composition(coat_str).elements) | set(Composition(cath_str).elements)
    elems.add(Element("Li"))
    pd = _phase_diagram([e.symbol for e in elems], cache_dir)
    try:
        return min_rxn_closed(Composition(coat_str), Composition(cath_str), pd)
    except Exception as ex:
        return (None, f"ERR {type(ex).__name__}: {ex}")


# ── 1단계: 문헌 정답지 검증 ────────────────────────────────────
def validate(cathodes, cache_dir):
    """LPSCl 를 코팅 자리에 놓고 Xiao 소환값과 대조. 반환 True/False."""
    print("=" * 72)
    print("검증: LPSCl vs 양극 (닫힌계 pseudo-binary) — Xiao 2019 소환값과 대조")
    print("  판정 = 부호 · 자릿수(앵커의 %.1f~%.1f배) · 순서(반충 > 만충 발열). 소수점 일치 아님"
          % (BAND_LO, BAND_HI))
    print("=" * 72)
    ok = True
    got = {}                                # (label, state) -> meV
    for cstr, clab, cstate in cathodes:
        if cstate == "se":
            print(f"\n## LPSCl | {clab}/se  ({cstr})  → 자기 자신이므로 검증 생략 "
                  f"(dE_rxt = 0 자명). 생산 실행에서만 의미 있음")
            continue
        mev, rxn = scan("Li6PS5Cl", cstr, cache_dir)
        tag = f"{clab}/{cstate}" if cstate else clab
        print(f"\n## LPSCl | {tag}  ({cstr})")
        if mev is None:
            print(f"  실패: {rxn}")
            ok = False
            continue
        print(f"  {mev:9.1f} meV/atom   {rxn[:80]}")
        got[(clab, cstate)] = mev
        anchor = XIAO_ANCHOR.get(("LPSCl", clab), {}).get(cstate)
        if anchor is None:
            print("  (이 양극/상태는 소환 앵커 없음 — 참고 출력만)")
            continue
        ratio = abs(mev) / abs(anchor)
        band = (mev < 0) and (BAND_LO <= ratio <= BAND_HI)
        print(f"  [Xiao 소환값] {anchor} meV/atom  ·  우리/문헌 = {ratio:.2f}배  "
              f"{'OK' if band else '⚠ 벗어남'}")
        if not band:
            ok = False

    # 순서 검사: 같은 양극에서 반충이 만충보다 더 발열이어야 한다 (탈리튬 = 더 산화적)
    for clab in sorted({c[1] for c in cathodes}):
        f, h = got.get((clab, "full")), got.get((clab, "half"))
        if f is None or h is None:
            continue
        mono = h < f
        print(f"\n## {clab} 리튬화 순서: 만충 {f:.0f} → 반충 {h:.0f} meV/atom  "
              f"{'OK (반충이 더 발열)' if mono else '⚠ 역전'}")
        if not mono:
            ok = False

    print("\n" + "=" * 72)
    print("검증 " + ("통과 — --run 진행 가능" if ok else "실패 — 원인 확인 전 --run 금지"))
    if not ok:
        print("  원인 후보: (a) MP hull 세대 차 (Xiao 2019 당시 DB vs 현재 GGA_GGA+U)")
        print("             (b) 반충 대리조성 Li0.5CoO2 가 Xiao 의 SOC 정의와 다름")
        print("             (c) NCM 대리조성(LiNi0.8Co0.1Mn0.1O2) 차이")
        print("             (d) use_hull_energy / norm 옵션 차 (pymatgen 버전)")
        print("             (e) 개방계(GrandPotential)로 돌아가 있지 않은지 — 이 파일은 닫힌계여야 함")
    print("=" * 72)
    return ok


# ── 2단계: 47 코팅 후보 전수 ───────────────────────────────────
def load_dopants():
    p = PROP / "cascade_v23_ranked.csv"
    with open(p) as f:
        rows = list(csv.DictReader(l for l in f if not l.startswith("#")))
    return [r["dopant"] for r in rows]


def run_all(cathodes, cache_dir, out_csv):
    dopants = load_dopants()
    print(f"코팅 후보 {len(dopants)}종 × 양극 {len(cathodes)}조성 "
          f"= {len(dopants) * len(cathodes)}쌍 (닫힌계)")
    done = set()
    if Path(out_csv).exists():          # resume-safe
        with open(out_csv) as f:
            for r in csv.DictReader(l for l in f if not l.startswith("#")):
                done.add((r["coating"], r["cathode"], r["lithiation"]))
        print(f"  기존 {len(done)}행 — 완료분 skip")
    cols = ["coating", "cathode", "lithiation", "cathode_composition",
            "dE_rxt_meV_per_atom", "gate_pass_100meV", "reaction"]
    exists = Path(out_csv).exists()
    n_new = 0
    with open(out_csv, "a" if exists else "w") as f:
        if not exists:
            f.write("# cascade 코팅 후보 x 양극 계면 반응성 (open_items M6). "
                    "닫힌계 pseudo-binary InterfacialReactivity (Richards/Ong 2016 eq 2), "
                    "norm=True, use_hull_energy=True, MP GGA_GGA+U.\n")
            f.write("# 축은 전위가 아니라 양극 리튬화 상태 (full=LiCoO2 / half=Li0.5CoO2). "
                    "Xiao 2019 F4 와 동일 정의.\n")
            f.write(f"# 게이트: |dE_rxt| < {GATE_MEV:.0f} meV/atom (Xiao 2019 F4). "
                    "더 음수 = 더 반응성 = 코팅으로 부적합. "
                    "Xiao 소환값(LPSCl/LCO -339 full / -493 half)은 문헌값 — 우리 값과 혼합 금지.\n")
        w = csv.DictWriter(f, fieldnames=cols)
        if not exists:
            w.writeheader()
        for i, d in enumerate(dopants, 1):
            for cstr, clab, cstate in cathodes:
                if (d, clab, cstate) in done:
                    print(f"[{i}/{len(dopants)}] {d} | {clab}/{cstate}: skip")
                    continue
                print(f"[{i}/{len(dopants)}] {d} | {clab}/{cstate}")
                try:
                    mev, rxn = scan(d, cstr, cache_dir)
                except Exception as ex:
                    print(f"    ERR {type(ex).__name__}: {ex}")
                    continue
                w.writerow({
                    "coating": d, "cathode": clab, "lithiation": cstate,
                    "cathode_composition": cstr,
                    "dE_rxt_meV_per_atom": ("" if mev is None else f"{mev:.1f}"),
                    "gate_pass_100meV": ("" if mev is None else
                                         ("Y" if abs(mev) < GATE_MEV else "N")),
                    "reaction": (rxn or "")[:200],
                })
                f.flush()               # 중간에 죽어도 재개 가능
                n_new += 1
                if mev is None:
                    print(f"    실패: {rxn}")
                else:
                    print(f"    {mev:9.1f} meV/atom  "
                          f"{'PASS' if abs(mev) < GATE_MEV else 'fail'}")
    print(f"\n→ {out_csv}  (+{n_new}행)")


def parse_cathodes(specs):
    """'comp:label:state' 파싱. label 생략 시 comp, state 생략 시 '' (앵커 대조 없음)."""
    out = []
    for c in specs:
        parts = c.split(":")
        comp = parts[0]
        lab = parts[1] if len(parts) > 1 and parts[1] else comp
        state = parts[2] if len(parts) > 2 else ""
        if state and state not in ("full", "half", "se"):
            sys.exit(f"--cathodes 상태는 full/half/se 만 허용: {c!r}")
        out.append((comp, lab, state))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--validate", action="store_true", help="LPSCl 정답지 검증만")
    ap.add_argument("--run", action="store_true", help="47 코팅 후보 전수 (검증 통과 후)")
    ap.add_argument("--force", action="store_true", help="검증 실패해도 강행")
    ap.add_argument("--cathodes", nargs="+", default=DEFAULT_CATHODES,
                    help='comp:label:state (state=full|half|se). se = 고체전해질 쪽 계면 '
                         '(Kim 2026: 구속을 거는 쪽은 양극이 아니라 SE 다). '
                         'NCM은 원소 수가 많아 비쌈 — 예 "LiNi0.8Co0.1Mn0.1O2:NCM:full"')
    ap.add_argument("--cache", default=str(Path.home() / ".cache" / "mp_entries"))
    ap.add_argument("--out", default=str(PROP / "cathode_reactivity_cascade.csv"))
    a = ap.parse_args()

    if not (a.validate or a.run):
        ap.error("--validate 또는 --run 중 하나는 필요")
    cathodes = parse_cathodes(a.cathodes)

    ok = validate(cathodes, a.cache)
    if a.run:
        if not ok and not a.force:
            sys.exit("\n검증 실패 — --force 없이는 전수 실행하지 않습니다.")
        run_all(cathodes, a.cache, a.out)


if __name__ == "__main__":
    main()
