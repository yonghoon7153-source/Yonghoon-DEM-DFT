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

★ 2026-08-16 (2) — **조성족(composition family) 표시** (미해결 항목 "clrich 섞임")
  챔피언 슬롯은 (도펀트, 농도라벨) 하나당 하나이고, 그 슬롯은 combined_score 최대값이
  가져간다. 그런데 후보 풀에는 **같은 도펀트의 두 설계 변형**이 들어 있다:
    · compound_set        (plain)  — 음이온 S17Cl4 · Li18
    · compound_set_chain  (Clrich) — 음이온 S16Cl5 · Li17  (S 하나를 Cl 로 바꾼 것)
  그래서 270 슬롯 중 17개는 **다른 조성**이 이름표만 같은 채로 앉아 있다.
  그 17개의 delta_ox_vs_host_V 는 host(Li6PS5Cl)와 비교되므로 도펀트 효과가 아니라
  **도펀트 + 음이온 치환**의 합이다. 여기서는 값을 지우지 않고 `composition_family` 로
  표시하고 `delta_ox_vs_host_V_confounded` 를 세운다. 판정은 사람이 한다.

  못 하는 것: 이 도구는 Cl 치환분과 도펀트분을 **분해하지 못한다**. 분해하려면
  도펀트 없는 Cl-rich 기준(Li_x P4 S16 Cl5)을 같은 phase set 안에서 재야 하고,
  그건 아직 어느 phase set 에도 없다 (`missing_baseline` 로 기록).
"""
import argparse, csv, json, os, math, hashlib, sys
from collections import defaultdict

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

def fnum(s):
    try: return float(s)
    except: return None

# ── 조성족 ────────────────────────────────────────────────────────────────────
# 판별자는 CSV 의 charge_compensation 이다. dopant 라벨 접미사(+Clrich)는 **거울**일 뿐이라
# 둘이 어긋나면 조용히 넘기지 않고 inconsistent 로 남긴다 (라벨만 믿다 틀린 전례가 있다).
FAMILY_BY_CHARGE_COMP = {"compound_set": "plain", "compound_set_chain": "Clrich"}
VARIANT_SUFFIX = "+Clrich"

def classify_family(dopant_label, charge_comp):
    """(family, dopant_base, consistent) — 모르는 charge_comp 는 plain 으로 넘기지 않는다."""
    base = dopant_label[:-len(VARIANT_SUFFIX)] if dopant_label.endswith(VARIANT_SUFFIX) else dopant_label
    fam = FAMILY_BY_CHARGE_COMP.get(charge_comp)
    if fam is None:
        return "unknown", base, False
    label_says_variant = dopant_label.endswith(VARIANT_SUFFIX)
    return fam, base, (label_says_variant == (fam != "plain"))

def annotate_families(results, csv_path, host_family="plain", eps=1e-9):
    """results 를 제자리에서 표시하고 감사 블록을 돌려준다.

    못 하는 것: 이름이 CSV 에 없는 결과는 **추정하지 않는다** — 그냥 실패시킨다.
    """
    by_name = {}
    with open(csv_path, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            by_name[r.get("name", "")] = r
    cand = [k for k in results if not k.startswith("__HOST__")]
    missing = [k for k in cand if k not in by_name]
    if missing:
        raise SystemExit(f"CSV 에 없는 결과 {len(missing)}건 (조성족 미상): {missing[:5]}")

    fams = defaultdict(list)
    inconsistent = []
    for k in cand:
        row = by_name[k]
        fam, base, ok = classify_family(row.get("dopant", ""), row.get("charge_compensation", ""))
        v = results[k]
        v["composition_family"] = fam
        v["dopant_base"] = base
        v["charge_compensation"] = row.get("charge_compensation", "")
        v["family_label_consistent"] = ok
        confounded = (fam != host_family)
        v["delta_ox_vs_host_V_confounded"] = confounded
        v["delta_confound"] = (
            "host 는 plain(Li6PS5Cl) 인데 이 행은 Cl-rich chain 변형(S 하나가 Cl 로 치환)이다. "
            "onset 차는 도펀트 효과와 음이온 치환 효과의 **합**이라 분해되지 않는다."
            if confounded else None)
        v["comparable_to_plain_champions"] = not confounded
        if not ok:
            inconsistent.append(k)
        fams[fam].append(k)

    def rate(keys):
        n = len(keys)
        hi = sum(1 for k in keys
                 if results[k].get("delta_ox_vs_host_V") is not None
                 and results[k]["delta_ox_vs_host_V"] > eps)
        return {"n": n, "n_raises_onset": hi, "pct": round(100.0 * hi / n, 1) if n else None}

    plain_r, var_r = rate(fams.get("plain", [])), rate(fams.get("Clrich", []))
    ratio = None
    if plain_r["pct"] and var_r["pct"] is not None:      # plain 0% 면 비율을 만들지 않는다
        ratio = round(var_r["pct"] / plain_r["pct"], 1)

    ox_by = defaultdict(lambda: defaultdict(list))
    for k in cand:
        v = results[k]
        if v.get("oxidation_limit_V") is not None:
            ox_by[v["dopant_base"]][v["composition_family"]].append(v["oxidation_limit_V"])
    only_variant, no_plain = [], []
    for base, fam in sorted(ox_by.items()):
        p, c = fam.get("plain"), fam.get("Clrich")
        if not c:
            continue
        host_ox = next((results[k].get("host_ox_V_same_phase_set") for k in cand
                        if results[k].get("dopant_base") == base
                        and results[k].get("host_ox_V_same_phase_set") is not None), None)
        if host_ox is None:
            continue
        if not p:
            no_plain.append(base)
        elif max(c) > host_ox + eps and max(p) <= host_ox + eps:
            only_variant.append(base)

    return {
        "discriminator": "cascade CSV charge_compensation (compound_set=plain · compound_set_chain=Clrich)",
        "why": ("(도펀트, 농도라벨) 슬롯을 combined_score 최대값이 가져가는데 후보 풀에 두 설계 "
                "변형이 같이 있어서, 슬롯 일부를 plain 이 아닌 Cl-rich 조성이 차지했다. "
                "이름표는 같지만 조성이 다르다."),
        "host_family": host_family,
        "counts": {f: len(v) for f, v in sorted(fams.items())},
        "family_label_inconsistent": inconsistent,
        "onset_raise_rate": {"plain": plain_r, "Clrich": var_r, "enrichment_ratio": ratio},
        "species_improving_only_as_variant": only_variant,
        "species_with_no_plain_champion": no_plain,
        "missing_baseline": ("도펀트 없는 Cl-rich 기준(Li_x P4 S16 Cl5)이 **어느 phase set 에도 없다**. "
                             "그게 없으면 Cl-rich 행의 Δ 를 (Cl 치환분)+(도펀트분) 으로 분해할 수 없다."),
        "allowed_statement": ("Cl-rich 행은 plain 챔피언과 나란히 놓지 않는다. 인용할 때는 조성식을 "
                              "같이 적고 '도펀트 효과' 라고 부르지 않는다."),
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="/data/work/repo/db/properties/cascade_v23_all.csv")
    ap.add_argument("--out", default="/data/work/repo/db/properties/oxidation_stability_cascade.json")
    ap.add_argument("--rank", default="1", help="rank_combined value to keep (champion)")
    ap.add_argument("--host", default=None,
                    help="host 조성 (예: 'Li24P4S20Cl4') — **같은 실행 안에서** 같이 재서 "
                         "candidate-host 비교를 성립시킨다. 다른 실행의 host 와 섞지 말 것")
    ap.add_argument("--annotate", metavar="JSON", default=None,
                    help="MP 없이 기존 출력에 조성족 표시만 입힌다 (제자리 갱신, 멱등)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.annotate:
        with open(a.annotate, encoding="utf-8") as fh:
            doc = json.load(fh)
        audit = annotate_families(doc["results"], a.csv)
        doc["composition_family_audit"] = audit
        with open(a.annotate, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, indent=2, ensure_ascii=False)
        print(f"-> {a.annotate}")
        print(f"   조성족 {audit['counts']}  라벨 불일치 {len(audit['family_label_inconsistent'])}건")
        r = audit["onset_raise_rate"]
        print(f"   host 초과: plain {r['plain']['n_raises_onset']}/{r['plain']['n']} = {r['plain']['pct']}%"
              f" · Clrich {r['Clrich']['n_raises_onset']}/{r['Clrich']['n']} = {r['Clrich']['pct']}%"
              f"  (x{r['enrichment_ratio']})")
        print(f"   Cl-rich 에서만 개선: {audit['species_improving_only_as_variant']}")
        print(f"   plain 챔피언 없음  : {audit['species_with_no_plain_champion']}")
        return
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
    fam_audit = annotate_families(results, a.csv)
    json.dump({"method": "grand-potential ESW (get_element_profile, MP GGA_GGA+U); per cascade champion",
               "source_csv": a.csv,
               "composition_family_audit": fam_audit,
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
               "results": results}, open(a.out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"\n-> {a.out}")
    print(f"   조성족 {fam_audit['counts']} · Cl-rich 에서만 개선 "
          f"{fam_audit['species_improving_only_as_variant']} · plain 챔피언 없음 "
          f"{fam_audit['species_with_no_plain_champion']}")
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

def selftest():
    """조성족 분류·감사 자가시험. **음성 경로 포함** — 틀린 입력을 잡아내는지 본다."""
    import tempfile, pathlib
    ok = fail = 0
    def chk(name, cond):
        nonlocal ok, fail
        if cond: ok += 1
        else:
            fail += 1
            try: print(f"  ✗ {name}")
            except Exception: print(f"  FAIL {name}")
    def raises(fn):
        try: fn(); return False
        except SystemExit: return True
        except Exception: return True

    # ── 분류기 ────────────────────────────────────────────────────────────
    chk("plain 분류",      classify_family("B2O3", "compound_set") == ("plain", "B2O3", True))
    chk("Clrich 분류",     classify_family("B2O3+Clrich", "compound_set_chain") == ("Clrich", "B2O3", True))
    chk("base 접미사 제거", classify_family("B2O3+Clrich", "compound_set_chain")[1] == "B2O3")
    # 음성 ①: 라벨과 charge_comp 가 어긋나면 consistent=False 여야 한다
    chk("음성: 라벨만 Clrich", classify_family("B2O3+Clrich", "compound_set")[2] is False)
    chk("음성: 라벨만 plain",  classify_family("B2O3", "compound_set_chain")[2] is False)
    # 음성 ②: 모르는 charge_comp 를 plain 으로 흘려보내면 안 된다
    fam, _, cons = classify_family("B2O3", "something_new")
    chk("음성: 미지 charge_comp 는 unknown", fam == "unknown" and cons is False)
    chk("음성: 미지 charge_comp 를 plain 으로 안 넘김", fam != "plain")
    chk("빈 charge_comp 도 unknown", classify_family("B2O3", "")[0] == "unknown")

    tmp = pathlib.Path(tempfile.mkdtemp())
    def write_csv(rows):
        p = tmp / "c.csv"
        with open(p, "w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["name", "dopant", "charge_compensation"])
            for r in rows: w.writerow(r)
        return str(p)

    # ── 감사 ──────────────────────────────────────────────────────────────
    csvp = write_csv([("A_x020", "X2O3", "compound_set"),
                      ("A_x050", "X2O3+Clrich", "compound_set_chain"),
                      ("B_x020", "Y2O3", "compound_set"),
                      ("B_x050", "Y2O3+Clrich", "compound_set_chain"),
                      ("C_x020", "Z2O3+Clrich", "compound_set_chain")])
    res = {
        "A_x020": {"oxidation_limit_V": 2.140, "delta_ox_vs_host_V": 0.0,   "host_ox_V_same_phase_set": 2.14},
        "A_x050": {"oxidation_limit_V": 2.354, "delta_ox_vs_host_V": 0.214, "host_ox_V_same_phase_set": 2.14},
        "B_x020": {"oxidation_limit_V": 2.282, "delta_ox_vs_host_V": 0.142, "host_ox_V_same_phase_set": 2.14},
        "B_x050": {"oxidation_limit_V": 2.282, "delta_ox_vs_host_V": 0.142, "host_ox_V_same_phase_set": 2.14},
        "C_x050": {"oxidation_limit_V": 2.317, "delta_ox_vs_host_V": 0.177, "host_ox_V_same_phase_set": 2.14},
        "__HOST__": {"oxidation_limit_V": 2.14},
    }
    # 음성 ③: CSV 에 이름이 없는 결과(C_x050 vs C_x020)는 추정하지 말고 실패해야 한다
    chk("음성: CSV 미등재 이름이면 실패", raises(lambda: annotate_families(dict(res), csvp)))

    res["C_x020"] = res.pop("C_x050")
    audit = annotate_families(res, csvp)
    chk("host 는 표시 대상 아님", "composition_family" not in res["__HOST__"])
    chk("counts plain 2 / Clrich 3", audit["counts"] == {"Clrich": 3, "plain": 2})
    chk("plain 은 confounded 아님",  res["A_x020"]["delta_ox_vs_host_V_confounded"] is False)
    # 음성 ④: 변형 행을 confounded 로 안 세우면 실패
    chk("음성: 변형 행은 confounded", res["A_x050"]["delta_ox_vs_host_V_confounded"] is True)
    chk("음성: 변형 행은 plain 과 비교 불가", res["A_x050"]["comparable_to_plain_champions"] is False)
    chk("confound 사유 문자열 존재", bool(res["A_x050"]["delta_confound"]))
    chk("plain 은 사유 없음", res["A_x020"]["delta_confound"] is None)
    chk("X2O3 는 Cl-rich 에서만 개선", audit["species_improving_only_as_variant"] == ["X2O3"])
    # 음성 ⑤: plain 도 개선하는 종을 'Cl-rich 에서만' 에 넣으면 실패
    chk("음성: Y2O3 는 목록에 없다", "Y2O3" not in audit["species_improving_only_as_variant"])
    chk("Z2O3 는 plain 챔피언 없음", audit["species_with_no_plain_champion"] == ["Z2O3"])
    # 음성 ⑥: plain 이 있는 종을 no_plain 에 넣으면 실패
    chk("음성: X2O3 는 no_plain 아님", "X2O3" not in audit["species_with_no_plain_champion"])
    r = audit["onset_raise_rate"]
    chk("plain 초과율 1/2", (r["plain"]["n_raises_onset"], r["plain"]["n"]) == (1, 2))
    chk("Clrich 초과율 3/3", (r["Clrich"]["n_raises_onset"], r["Clrich"]["n"]) == (3, 3))
    chk("enrichment 2.0x", r["enrichment_ratio"] == 2.0)
    chk("missing_baseline 명시", "Cl-rich" in audit["missing_baseline"])

    # 멱등: 두 번 돌려도 같은 감사 결과
    audit2 = annotate_families(res, csvp)
    chk("멱등", audit2["counts"] == audit["counts"]
                and audit2["onset_raise_rate"] == audit["onset_raise_rate"])

    # 음성 ⑦: plain 초과율 0% 일 때 비율을 만들어내면 안 된다 (0 나눗셈/무한대 금지)
    res0 = {"A_x020": {"oxidation_limit_V": 2.14, "delta_ox_vs_host_V": 0.0, "host_ox_V_same_phase_set": 2.14},
            "A_x050": {"oxidation_limit_V": 2.35, "delta_ox_vs_host_V": 0.21, "host_ox_V_same_phase_set": 2.14}}
    csv0 = write_csv([("A_x020", "X2O3", "compound_set"), ("A_x050", "X2O3+Clrich", "compound_set_chain")])
    a0 = annotate_families(res0, csv0)
    chk("음성: plain 0% 면 enrichment 없음", a0["onset_raise_rate"]["enrichment_ratio"] is None)

    # 음성 ⑧: 라벨 불일치가 감사에 보고돼야 한다
    csvb = write_csv([("A_x020", "X2O3+Clrich", "compound_set")])
    ab = annotate_families({"A_x020": {"oxidation_limit_V": 2.14}}, csvb)
    chk("음성: 라벨 불일치 보고", ab["family_label_inconsistent"] == ["A_x020"])

    # 음성 ⑨: delta 가 None 인 행을 '초과' 로 세면 안 된다
    csvn = write_csv([("A_x020", "X2O3", "compound_set")])
    an = annotate_families({"A_x020": {"oxidation_limit_V": None, "delta_ox_vs_host_V": None}}, csvn)
    chk("음성: delta None 은 초과 아님", an["onset_raise_rate"]["plain"]["n_raises_onset"] == 0)

    try: print(f"\nselftest: {ok} passed, {fail} failed")
    except Exception: print(f"\nselftest: {ok} passed, {fail} failed")
    return 1 if fail else 0

if __name__ == "__main__":
    raise SystemExit(main() or 0)
