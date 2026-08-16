#!/usr/bin/env python3
"""esw_cascade_batch.py — grand-potential ESW (oxidation/reduction window) for
EVERY doped-argyrodite champion in the cascade. Fast: needs only composition +
MP hull (no DFT). Same method as tools/oxidation/esw_grand_potential.py
(Mo/Ong/Ceder get_element_profile), looped over the cascade champions.

Run on gabia/kserver116 (MP_API_KEY set, mp_api + pymatgen in env):
    python3 esw_cascade_batch.py \
        --csv /data/work/repo/db/properties/cascade_v23_all.csv \
        --out /data/work/repo/db/properties/oxidation_stability_cascade.json

Reads rank_combined==1 rows, builds Composition from composition_* columns,
runs the grand-potential Li-evolution profile, and records per champion:
  reduction_limit_V, oxidation_limit_V, ocv_self_decomposition_V + onset rxns.
Caches the MP hull per chemsys so dopants sharing a chemsys pull once.

★ 2026-08-16 — **phase_set_id 기록** (Codex Round-3 P0: G3 method-comparable 0)
  옛 판은 값만 저장하고 **어떤 경쟁상 집합으로 쟀는지**를 안 남겼다. 규칙 자체는
  균일했다(chemsys 전체 · GGA_GGA+U · 제외 없음). 문제는 그 규칙이 **해석된 결과**
  (실제 entry ID 목록, MP 스냅샷 버전)가 사라진 것이다. 그래서 90종에 onset 기록이
  다 있는데도 candidate–host 비교가 0종이었다: 같은 집합을 썼다는 증거가 없다.

  이제 chemsys 마다 다음을 싣는다:
    · entry_ids      정렬된 MP entry ID 전체
    · phase_set_id   sha256(정렬된 entry_ids)[:16]  ← 같으면 같은 집합
    · n_entries      개수 (빠른 대조용)
    · db_version     MP 데이터베이스 버전
  그리고 --host 를 주면 **같은 실행 안에서** host onset 도 재서 후보와 나란히 싣는다.
  다른 실행·다른 스냅샷의 host 값과 섞으면 안 되기 때문이다.

  ⚠ chemsys 가 다르면 entry 집합이 **필연적으로** 다르다(원소가 다르니까). 그건 결함이
  아니라 방법의 성질이다. phase_set_id 는 "같은 chemsys 를 같은 스냅샷으로 봤나" 를
  보증하지, 서로 다른 chemsys 를 같게 만들어 주지 않는다.
"""
import argparse, csv, json, os, math, hashlib
from collections import defaultdict

def fnum(s):
    try: return float(s)
    except: return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="/data/work/repo/db/properties/cascade_v23_all.csv")
    ap.add_argument("--out", default="/data/work/repo/db/properties/oxidation_stability_cascade.json")
    ap.add_argument("--rank", default="1", help="rank_combined value to keep (champion)")
    ap.add_argument("--host", default=None,
                    help="host 조성 (예: 'Li24P4S20Cl4') — **같은 실행 안에서** 같이 재서 "
                         "candidate-host 비교를 성립시킨다. 다른 실행의 host 와 섞지 말 것")
    a = ap.parse_args()
    key = os.environ.get("MP_API_KEY") or os.environ.get("PMG_MAPI_KEY")
    if not key: raise SystemExit("Set MP_API_KEY (run on gabia).")
    from pymatgen.core import Composition, Element
    from pymatgen.analysis.phase_diagram import PhaseDiagram
    from mp_api.client import MPRester
    Li = Element("Li")

    # ---- gather champion compositions ----
    champs = []
    for r in csv.DictReader(open(a.csv)):
        if r.get("rank_combined") != a.rank: continue
        comp = {}
        for k, v in r.items():
            if k.startswith("composition_") and v not in ("", None):
                n = fnum(v)
                if n and n > 0: comp[k.split("composition_")[1]] = n
        if not comp: continue
        champs.append((r.get("_dir", r.get("name", "?")), r.get("dopant", "?"), comp))
    print(f"{len(champs)} champions with composition")

    # ---- group by chemsys, pull each hull once ----
    # ★ 2026-08-16 — chemsys 를 **후보 ∪ host** 로 잡는다.
    #   x=0.25 에서 셀의 Cl 이 4개뿐이라, Cl 자리를 치환하는 도펀트(TiF4·ZrBr4·ZrF4)는
    #   **Cl 을 전부 없앤다**: 실측 조성 Li25 P3 S20 F4 Ti1 — Cl 0개.
    #   그러면 host(Li24P4S20Cl4)가 그 chemsys 의 부분집합이 아니라 같은 phase set 에
    #   못 들어가고, 후보-host 비교가 성립하지 않는다 (9/270 이 그 경우였다).
    #   합집합으로 잡으면 host 가 항상 들어가고, 두 값이 같은 hull 에서 나온다.
    #   ⚠ 대부분의 후보는 이미 host 원소를 포함하므로 합집합 = 자기 chemsys (변화 없음).
    #     바뀌는 건 Cl 을 전부 치환한 그 9건뿐이고, 그쪽은 Cl 상이 hull 에 추가되므로
    #     **후보 자신의 onset 도 달라질 수 있다** — 그게 같은 집합 안의 값이라 옳다.
    host_els_for_group = set()
    if a.host:
        from pymatgen.core import Composition as _C0
        host_els_for_group = {str(e) for e in _C0(a.host).elements}
    by_sys = defaultdict(list)
    n_union = 0
    for name, dop, comp in champs:
        els = set(comp)
        if host_els_for_group and not host_els_for_group <= els:
            els = els | host_els_for_group
            n_union += 1
        by_sys[tuple(sorted(els))].append((name, dop, comp))
    if n_union:
        print(f"  ⚠ {n_union}건은 host 원소가 조성에 없어 **합집합 chemsys** 로 묶었다 "
              f"(도펀트가 Cl 을 전부 치환한 경우)")

    results = {}
    phase_sets = {}
    # ★ host 를 후보와 **같은 실행**에 넣는다 — 그래야 같은 스냅샷·같은 chemsys 규칙이 된다.
    if a.host:
        from pymatgen.core import Composition as _C
        hc = _C(a.host)
        host_comp = {str(e): float(hc[e]) for e in hc.elements}
        host_els = set(host_comp)
        # ★ 2026-08-16 — host 를 **모든 chemsys 안에서** 잰다.
        #   후보는 host 원소 + 도펀트 원소라 chemsys 가 더 크다. host 를 자기 chemsys
        #   에서만 재면 "후보 2.356 vs host 2.140" 이 **서로 다른 phase set 끼리 뺀 값**이
        #   된다 — G3 의 method-comparable 0 이 정확히 그 상태였다.
        #   같은 hull 안에서 host 도 재면 그 차가 처음으로 같은 집합 안의 차가 된다.
        #   hull 은 chemsys 당 한 번만 당기므로 추가 비용은 profile 계산 하나뿐이다.
        n_added = 0
        for sys_els in list(by_sys):
            if host_els <= set(sys_els):
                by_sys[sys_els].append((f"__HOST__@{'-'.join(sorted(sys_els))}",
                                        a.host, dict(host_comp)))
                n_added += 1
        if tuple(sorted(host_els)) not in by_sys:
            by_sys[tuple(sorted(host_els))].append(("__HOST__", a.host, dict(host_comp)))
            n_added += 1
        print(f"host {a.host} 를 chemsys {n_added}개 안에서 함께 잰다 "
              f"(같은 phase set 안의 후보-host 차를 만들기 위해)")

    for sys_els, items in by_sys.items():
        els = list(sys_els)
        try:
            with MPRester(key) as mpr:
                entries = mpr.get_entries_in_chemsys(els,
                    additional_criteria={"thermo_types": ["GGA_GGA+U"]})
                try:
                    db_version = mpr.get_database_version()
                except Exception:
                    db_version = None
            pd = PhaseDiagram(entries)
            muref = pd.el_refs[Li].energy_per_atom
            # ★ 이 hull 을 만든 **실제 entry 목록**을 지문으로 굳힌다 (2026-08-16).
            eids = sorted(str(getattr(e, "entry_id", "") or
                              getattr(getattr(e, "data", {}), "get", lambda *_: "")("material_id") or "")
                          for e in entries)
            psid = hashlib.sha256("|".join(eids).encode()).hexdigest()[:16]
            phase_sets[psid] = {"chemsys": "-".join(sorted(els)), "n_entries": len(entries),
                                "entry_ids": eids, "db_version": db_version,
                                "thermo_types": ["GGA_GGA+U"], "exclusions": []}
        except Exception as e:
            for name, dop, comp in items:
                results[name] = {"dopant": dop, "error": f"hull: {str(e)[:120]}"}
            print(f"  [{'-'.join(els)}] hull FAIL: {str(e)[:80]}")
            continue
        print(f"  [{'-'.join(els)}] {len(entries)} entries -> {len(items)} champ")
        for name, dop, comp in items:
            try:
                c = Composition(comp)
                prof = pd.get_element_profile(Li, c)
                steps = [{"V": round(muref - float(p["chempot"]), 3),
                          "evo": round(float(p["evolution"]), 4),
                          "rxn": str(p["reaction"])} for p in prof]
                pos = [s for s in steps if s["evo"] > 1e-6]
                neg = [s for s in steps if s["evo"] < -1e-6]
                neu = [s for s in steps if abs(s["evo"]) <= 1e-6]
                red = max((s["V"] for s in pos), default=None)
                ox = min((s["V"] for s in neg), default=None)
                ocv = min((s["V"] for s in neu), default=None)
                def rxn_at(v): return min(steps, key=lambda s: abs(s["V"]-v))["rxn"] if v is not None else None
                # ⚠ els 는 **합집합** chemsys 다. 원래 조성 원소를 따로 남겨야
                #   "합집합으로 쟀다" 를 사후에 판별할 수 있다 (2026-08-16 실측: 안 남겨서
                #   chemsys_note 가 0건이 나왔다 — 조건이 항상 참이 됐다).
                results[name] = {"dopant": dop, "elements": els,
                    "composition_elements": sorted(comp),
                    "chemsys_is_union_with_host": sorted(comp) != sorted(els),
                    "phase_set_id": psid, "n_entries": len(entries), "db_version": db_version,
                    "reduction_limit_V": red, "oxidation_limit_V": ox,
                    "ocv_self_decomposition_V": ocv,
                    "oxidation_onset_rxn": rxn_at(ox), "ocv_rxn": rxn_at(ocv),
                    "window_V": (round(ox-red,3) if (ox is not None and red is not None) else None),
                    "n_breakpoints": len(steps)}
            except Exception as e:
                results[name] = {"dopant": dop, "phase_set_id": psid, "error": str(e)[:120]}

    # ── 같은 phase set 안의 host 값을 각 후보에 붙인다 ────────────────────────
    host_by_psid = {}
    for k, v in results.items():
        if k.startswith("__HOST__") and "oxidation_limit_V" in v:
            host_by_psid[v.get("phase_set_id")] = v
    n_comparable = 0
    for k, v in results.items():
        if k.startswith("__HOST__") or "error" in v:
            continue
        h = host_by_psid.get(v.get("phase_set_id"))
        if h and h.get("oxidation_limit_V") is not None and v.get("oxidation_limit_V") is not None:
            v["host_ox_V_same_phase_set"] = h["oxidation_limit_V"]
            if v.get("chemsys_is_union_with_host"):
                v["chemsys_note"] = ("후보 조성에 host 원소가 없어 합집합 chemsys 로 쟀다 "
                                     "— x=0.25 에서 도펀트가 그 원소를 전부 치환한 경우")
            v["delta_ox_vs_host_V"] = round(v["oxidation_limit_V"] - h["oxidation_limit_V"], 4)
            v["method_comparable"] = True
            n_comparable += 1
        else:
            v["host_ox_V_same_phase_set"] = None
            v["delta_ox_vs_host_V"] = None
            v["method_comparable"] = False
    host = results.get("__HOST__")
    json.dump({"method": "grand-potential ESW (get_element_profile, MP GGA_GGA+U); per cascade champion",
               "source_csv": a.csv,
               "phase_set_contract": (
                   "phase_set_id = sha256(sorted MP entry_ids)[:16]. 같은 id 면 같은 경쟁상 집합이다. "
                   "candidate-host 비교는 **같은 phase_set_id** 안에서만 성립한다. "
                   "규칙: chemsys 전체 · thermo_types=GGA_GGA+U · 제외 없음."),
               "phase_sets": phase_sets,
               "host": host, "host_composition": a.host,
               "hosts_by_phase_set": host_by_psid,
               "n_method_comparable": n_comparable,
               "method_comparable_definition": (
                   "후보와 host 를 **같은 phase_set_id**(같은 chemsys · 같은 MP 스냅샷 · "
                   "같은 entry 목록) 안에서 재서 delta_ox_vs_host_V 를 만든 건수. "
                   "이 값이 아니면 onset 차를 '후보 고유 효과' 로 읽을 수 없다."),
               "results": results}, open(a.out, "w"), indent=2)
    print(f"\n-> {a.out}")
    print(f"   phase_set {len(phase_sets)}개 · "
          f"entry 총 {sum(v['n_entries'] for v in phase_sets.values())} · "
          f"MP db {sorted({str(v['db_version']) for v in phase_sets.values()})}")
    print(f"   ★ method-comparable {n_comparable}/{sum(1 for k in results if not k.startswith('__HOST__'))}"
          f"  (같은 phase set 안에서 host 와 뺀 건수)")
    if host and "oxidation_limit_V" in host:
        print(f"   host {a.host}: ox {host['oxidation_limit_V']} V "
              f"(phase_set {host.get('phase_set_id')})")
        print("   ⚠ 후보와 host 의 phase_set_id 가 다르면 (chemsys 가 다르므로 보통 다르다) "
              "onset 차를 '후보 고유 효과' 로 읽지 말 것 — 같은 집합 안에서만 비교된다.")
    # compact summary (paste-friendly)
    print(f"\n{'champion':18s} {'ox_V':>6s} {'red_V':>6s} {'ocv_V':>6s} {'win_V':>6s}")
    for name in sorted(results):
        d = results[name]
        if "error" in d: print(f"{name:18s} ERROR {d['error'][:50]}"); continue
        print(f"{name:18s} {str(d['oxidation_limit_V']):>6s} {str(d['reduction_limit_V']):>6s} "
              f"{str(d['ocv_self_decomposition_V']):>6s} {str(d['window_V']):>6s}")

if __name__ == "__main__":
    main()
