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
import argparse, collections, csv, json, os, math, hashlib, sys
from collections import defaultdict

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "cascade"))
from cascade_ids import base_species          # noqa: E402  — 그룹핑 정본

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
    base = base_species(dopant_label)          # 그룹핑은 tools/cascade/cascade_ids.py 정본
    fam = FAMILY_BY_CHARGE_COMP.get(charge_comp)
    if fam is None:
        return "unknown", base, False
    label_says_variant = dopant_label.endswith(VARIANT_SUFFIX)
    return fam, base, (label_says_variant == (fam != "plain"))

#: chain 변형이 plain 대비 만족해야 하는 **정확한** 조성 변환. 하나라도 어긋나면
#: 그건 S→Cl 치환이 아니라 다른 recipe 다 (Codex P0-1, 2026-08-16: 17행 중 7행).
CHAIN_TRANSFORM = {"Li": -1.0, "S": -1.0, "Cl": +1.0}


def _comp(row):
    return {k[len("composition_"):]: float(row[k] or 0)
            for k in row if k.startswith("composition_")}


def classify_transform(chain_row, plain_rows, tol=1e-9):
    """chain 후보가 plain 형제와 **정확히** ΔLi=-1·ΔS=-1·ΔCl=+1 인가.

    → ("exact", 짝 이름) | ("multi_transform", 가장 가까운 plain) | ("no_plain_candidate", None)

    ⛔ 이 판정은 조성 벡터 전체를 본다. 라벨(`+Clrich`)이나 charge_compensation 만으로는
       "S 하나가 Cl 로 바뀐 것" 이라고 말할 수 없다 — B2O3·MoO3·WO3 는 치환 자리(P_4b vs
       Li_24g)와 Li/P 화학량론까지 함께 다르다.
    """
    if not plain_rows:
        return "no_plain_candidate", None
    c = _comp(chain_row)
    els = set(c) | {e for p in plain_rows for e in _comp(p)}
    for p in plain_rows:
        pc = _comp(p)
        if all(abs((c.get(e, 0.0) - pc.get(e, 0.0)) - CHAIN_TRANSFORM.get(e, 0.0)) < tol
               for e in els):
            return "exact", p.get("name")
    return "multi_transform", plain_rows[0].get("name")


def annotate_families(results, csv_path, host_family="plain", eps=1e-9):
    """results 를 제자리에서 표시하고 감사 블록을 돌려준다.

    못 하는 것
      · 이름이 CSV 에 없는 결과는 **추정하지 않는다** — 그냥 실패시킨다.
      · 조성족은 provenance(어느 generator 가 만들었나)이지 **원인 변수가 아니다.**
        여기서 세는 비율은 전부 사후 기술통계다 — 인과 효과 크기로 인용하면 안 된다.
      · chain 후보가 없는 슬롯까지 분모에 넣은 비(9.6배)와, chain 후보가 실제 있던
        슬롯만 본 비(2.59배)는 다른 양이다. 둘 다 싣되 둘 다 non-causal 이다.
    """
    by_name, all_rows = {}, []
    with open(csv_path, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            by_name[r.get("name", "")] = r
            all_rows.append(r)
    cand = [k for k in results if not k.startswith("__HOST__")]
    missing = [k for k in cand if k not in by_name]
    if missing:
        raise SystemExit(f"CSV 에 없는 결과 {len(missing)}건 (조성족 미상): {missing[:5]}")

    fams = defaultdict(list)
    inconsistent = []
    plain_by_base = defaultdict(list)
    for r in all_rows:
        if r.get("charge_compensation") == "compound_set":
            plain_by_base[classify_family(r.get("dopant", ""), "compound_set")[1]].append(r)

    for k in cand:
        row = by_name[k]
        fam, base, ok = classify_family(row.get("dopant", ""), row.get("charge_compensation", ""))
        v = results[k]
        v["composition_family"] = fam
        v["dopant_base"] = base
        v["generator_variant"] = row.get("charge_compensation", "")
        v["charge_compensation"] = row.get("charge_compensation", "")
        v["substitution_site"] = row.get("cation_site", "")
        v["anion_site"] = row.get("anion_site", "")
        v["family_label_consistent"] = ok
        confounded = (fam != host_family)
        v["delta_ox_vs_host_V_confounded"] = confounded
        v["comparable_to_plain_champions"] = not confounded
        # ── 변환 판정 (Codex P0-1) ────────────────────────────────────────────
        # chain 이라고 다 "S 하나가 Cl 로" 가 아니다. 조성 벡터를 전수 대조한다.
        if fam == "Clrich":
            st, pair = classify_transform(row, plain_by_base.get(base, []))
            v["matched_transform_status"] = st
            v["matched_plain_candidate"] = pair
            v["matched_plain_site"] = (
                next((r.get("cation_site") for r in plain_by_base.get(base, [])
                      if r.get("name") == pair), None))
            v["contrast_scope"] = "multi_intervention_recipe_vs_host"
            v["delta_confound"] = (
                "host 는 plain 이고 이 행은 compound_set_chain generator 산물이다. "
                + ("plain 형제와 정확히 ΔLi=-1·ΔS=-1·ΔCl=+1 이라 조성 대비는 짝지어지지만, "
                   "그래도 onset 차는 (도펀트 + 추가 치환)의 합이라 분해되지 않는다."
                   if st == "exact" else
                   "plain 형제와 **치환 자리·Li/P 화학량론까지 다르다** — 단순 S→Cl 대비가 "
                   "아니다. 여러 개입이 동시에 들어간 recipe 대비다."
                   if st == "multi_transform" else
                   "plain 형제 자체가 없어 짝지을 대비가 없다."))
        else:
            v["matched_transform_status"] = None
            v["matched_plain_candidate"] = None
            v["contrast_scope"] = "primary_recipe_vs_host"
            # ⛔ plain 도 host 대비 O/S 치환·자리 선택·Li 전하보상이 함께 바뀐다.
            #   "unconfounded" 가 의미하는 범위는 **추가 chain 개입이 없다** 까지다.
            v["delta_confound"] = None
        v["isolated_dopant_effect"] = False
        if not ok:
            inconsistent.append(k)
        fams[fam].append(k)

    def rate(keys):
        n = len(keys)
        hi = sum(1 for k in keys
                 if results[k].get("delta_ox_vs_host_V") is not None
                 and results[k]["delta_ox_vs_host_V"] > eps)
        # ⛔ pct 는 표시용이다. 비율은 **원계수에서 한 번만** 반올림한다 —
        #   6.7 과 64.7 을 먼저 반올림하고 나누면 9.6 이 9.7 이 된다 (Codex P1-1).
        return {"n": n, "n_raises_onset": hi, "pct": round(100.0 * hi / n, 1) if n else None}

    def ratio_of(a, b):
        if not a["n"] or not b["n"] or not b["n_raises_onset"]:
            return None
        return round((a["n_raises_onset"] / a["n"]) / (b["n_raises_onset"] / b["n"]), 2)

    plain_r, var_r = rate(fams.get("plain", [])), rate(fams.get("Clrich", []))
    ratio = ratio_of(var_r, plain_r)

    # ── eligible-slot 대비 (Codex P1-2) ──────────────────────────────────────
    # 위 비의 분모에는 chain 후보가 **존재하지도 않았던** 슬롯이 들어 있다.
    # chain 후보가 실제 있던 (base, 농도라벨) 슬롯만 남기면 대비가 훨씬 작아진다.
    def slot(r):
        return (classify_family(r.get("dopant", ""), r.get("charge_compensation", ""))[1],
                r.get("concentration_label", ""))
    eligible = {slot(r) for r in all_rows if r.get("charge_compensation") == "compound_set_chain"}
    e_keys = [k for k in cand if slot(by_name[k]) in eligible]
    e_plain = rate([k for k in e_keys if results[k]["composition_family"] == "plain"])
    e_chain = rate([k for k in e_keys if results[k]["composition_family"] == "Clrich"])

    tr = collections.Counter(results[k].get("matched_transform_status")
                             for k in cand if results[k]["composition_family"] == "Clrich")
    unmatched = sorted(k for k in cand
                       if results[k].get("matched_transform_status") == "multi_transform")

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
        "discriminator": ("cascade CSV charge_compensation "
                          "(compound_set=plain · compound_set_chain=Clrich). "
                          "**provenance label 이지 원인 변수가 아니다.**"),
        "why": ("(도펀트, 농도라벨) 슬롯을 combined_score 최대값이 가져가는데 후보 풀에 두 설계 "
                "변형이 같이 있어서, 슬롯 일부를 plain 이 아닌 chain generator 조성이 차지했다. "
                "이름표는 같지만 조성이 다르다."),
        "host_family": host_family,
        "counts": {f: len(v) for f, v in sorted(fams.items())},
        "family_label_inconsistent": inconsistent,
        "matched_transform": {
            "definition": "chain 후보가 같은 base 의 plain 후보와 정확히 ΔLi=-1·ΔS=-1·ΔCl=+1 인가",
            "counts": {k: v for k, v in sorted(tr.items(), key=lambda x: str(x[0]))},
            "multi_transform_rows": unmatched,
            "note": ("⛔ 'chain = S 하나가 Cl 로 치환' 은 **전체 family 설명으로 거짓**이다 "
                     "(Codex P0-1). multi_transform 행은 치환 자리(P_4b vs Li_24g)와 "
                     "Li/P 화학량론까지 함께 다르다 — 여러 개입이 동시에 들어갔다."),
        },
        "onset_raise_rate": {
            "plain": plain_r, "Clrich": var_r, "enrichment_ratio": ratio,
            "eligible_slots_only": {
                "definition": ("chain 후보가 실제로 존재한 (base, 농도라벨) 슬롯의 챔피언만. "
                               "위 전체 비의 분모에는 chain 후보가 없던 슬롯이 들어 있다."),
                "n_slots": len(eligible),
                "plain": e_plain, "Clrich": e_chain,
                "ratio": ratio_of(e_chain, e_plain),
            },
            "caveat": ("⛔ 두 비 모두 **사후 기술통계**다. 챔피언은 combined_score 최대값으로 "
                       "사후 선택됐고 농도 라벨은 독립 반복이 아니다(실측 x 는 셋 다 0.25). "
                       "어느 쪽도 Cl 의 물리 효과 크기로 인용하지 않는다."),
        },
        "species_improving_only_as_variant": only_variant,
        "species_with_no_plain_champion": no_plain,
        "missing_baseline": (
            "도펀트 없는 Cl-only host 기준이 **캐스케이드 phase set 안에 없다**. "
            "4 f.u. host 는 Li24P4S20Cl4 이고, S²⁻ 하나를 Cl⁻ 로 바꾸며 중성을 유지하면 "
            "Li23P4S19Cl5 다. 최소 설계는 H_plain·H_Cl·D_plain·D_Cl 네 칸을 같은 "
            "phase_set_id 에서 재는 것이고, 그래야 main effect 와 interaction 이 분리된다. "
            "(constrained_esw_cl_scan.json 의 Cl 스캔은 LiS4 제외 phase set 이라 "
            "절대값 이식 불가 — 참고용이다.)"),
        "allowed_statement": ("chain 행은 plain 챔피언과 나란히 놓지 않는다. 인용할 때는 조성식과 "
                              "치환 자리를 같이 적고 '도펀트 효과' 라고 부르지 않는다. "
                              "plain 도 host 대비 여러 원자가 함께 바뀌므로 "
                              "'recipe-level host contrast' 라고 쓴다."),
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
    def raises(fn, want="", exc=SystemExit):
        """⛔ 앞 판은 `except Exception: return True` 였다 — **오타로 죽어도 통과**했다
        (Codex F). 기대하는 예외 type 과 메시지 조각을 둘 다 확인한다."""
        try:
            fn()
        except exc as e:
            return (want in str(e)) if want else True
        except Exception as e:
            print(f"    (예상 밖 예외 {type(e).__name__}: {str(e)[:60]})")
            return False
        return False

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
    _seq = [0]
    def write_csv(rows):
        # ⚠ 파일명을 고정하면 뒤 테스트가 앞 테스트의 CSV 를 덮어써서 서로를 망친다
        #   (실제로 당했다 — 멱등 검사가 엉뚱한 CSV 를 읽고 SystemExit).
        _seq[0] += 1
        p = tmp / f"c{_seq[0]}.csv"
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
    chk("음성: CSV 미등재 이름이면 실패",
        raises(lambda: annotate_families(dict(res), csvp), want="CSV 에 없는"))
    # 음성 ⑩: raises() 자체가 fail-open 이면 안 된다 — 아무 예외나 통과시키면 실패
    chk("음성: raises() 는 엉뚱한 예외를 통과시키지 않는다",
        raises(lambda: (_ for _ in ()).throw(ValueError("boom"))) is False)
    chk("음성: raises() 는 메시지가 다르면 통과시키지 않는다",
        raises(lambda: annotate_families(dict(res), csvp), want="전혀 다른 문구") is False)

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
    chk("missing_baseline 에 Cl-only host 조성", "Li23P4S19Cl5" in audit["missing_baseline"])
    # ── 반올림 순서 (Codex P1-1) ──────────────────────────────────────────
    # 실제 캐스케이드 수: plain 17/253, chain 11/17. pct 를 먼저 반올림하면 9.7 이 된다.
    csvr = write_csv([(f"P{i}", "R2O3", "compound_set") for i in range(253)]
                     + [(f"C{i}", "R2O3+Clrich", "compound_set_chain") for i in range(17)])
    resr = {}
    for i in range(253):
        resr[f"P{i}"] = {"oxidation_limit_V": 2.2, "host_ox_V_same_phase_set": 2.14,
                         "delta_ox_vs_host_V": 0.06 if i < 17 else 0.0}
    for i in range(17):
        resr[f"C{i}"] = {"oxidation_limit_V": 2.3, "host_ox_V_same_phase_set": 2.14,
                         "delta_ox_vs_host_V": 0.16 if i < 11 else 0.0}
    ar = annotate_families(resr, csvr)["onset_raise_rate"]
    chk("반올림: 원계수에서 한 번만 → 9.63", abs(ar["enrichment_ratio"] - 9.63) < 1e-9)
    chk("음성: pct 를 먼저 반올림한 9.7 이 아니다", ar["enrichment_ratio"] != 9.7)

    # ── 변환 판정 (Codex P0-1) ────────────────────────────────────────────
    def wcsv_comp(rows):
        _seq[0] += 1
        q = tmp / f"t{_seq[0]}.csv"
        with open(q, "w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["name", "dopant", "charge_compensation", "cation_site",
                        "concentration_label", "composition_Li", "composition_S",
                        "composition_Cl", "composition_P"])
            for r in rows: w.writerow(r)
        return str(q)
    # exact: ΔLi=-1 ΔS=-1 ΔCl=+1, 나머지 동일
    csvt = wcsv_comp([
        ("Ap", "X2O3", "compound_set", "Li_24g", "x002", 18, 17, 4, 4),
        ("Ac", "X2O3+Clrich", "compound_set_chain", "Li_24g", "x002", 17, 16, 5, 4),
        ("Bp", "Y2O3", "compound_set", "P_4b", "x002", 28, 17, 4, 2),
        ("Bc", "Y2O3+Clrich", "compound_set_chain", "Li_24g", "x002", 17, 16, 5, 4),
    ])
    rt = {n: {"oxidation_limit_V": 2.3, "host_ox_V_same_phase_set": 2.14,
              "delta_ox_vs_host_V": 0.16} for n in ("Ap", "Ac", "Bp", "Bc")}
    at = annotate_families(rt, csvt)
    chk("exact 변환 판정", rt["Ac"]["matched_transform_status"] == "exact")
    chk("exact 는 짝 이름을 남긴다", rt["Ac"]["matched_plain_candidate"] == "Ap")
    # 음성 ⑪: 자리·화학량론이 다르면 exact 라고 하면 안 된다 (B2O3·MoO3·WO3 실제 케이스)
    chk("음성: 자리/Li/P 가 다르면 multi_transform",
        rt["Bc"]["matched_transform_status"] == "multi_transform")
    chk("음성: multi_transform 을 S→Cl 로 설명하지 않는다",
        "S→Cl 대비가 아니다" in (rt["Bc"]["delta_confound"] or ""))
    chk("변환 집계", at["matched_transform"]["counts"].get("exact") == 1
        and at["matched_transform"]["counts"].get("multi_transform") == 1)
    chk("multi_transform 행 목록", at["matched_transform"]["multi_transform_rows"] == ["Bc"])
    chk("plain 은 contrast_scope=primary_recipe_vs_host",
        rt["Ap"]["contrast_scope"] == "primary_recipe_vs_host")
    chk("음성: plain 도 isolated_dopant_effect 가 아니다",
        rt["Ap"]["isolated_dopant_effect"] is False)
    # eligible-slot 대비 (Codex P1-2)
    el = at["onset_raise_rate"]["eligible_slots_only"]
    chk("eligible 슬롯 수", el["n_slots"] == 2)

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
