#!/usr/bin/env python3
"""audit_label_scatter.py — 세 농도 라벨이 실제로 무엇이었는지, 그 평균이 얼마나 오염됐는지.

배경
  v23 는 91 화합물 × 3 라벨(x002/x005/x010) = 273 슬롯을 돌렸다. 그런데 셀이 1×1×1 4 f.u.
  라 P 가 4개뿐이고, 정수 치환이라 **세 라벨이 전부 실측 x = 0.25** 로 반올림됐다.
  그래서 세 점은 농도 3점이 아니다.

  그럼 세 점은 뭔가? 각 라벨이 자기 구조 열거·이완을 따로 돌아 **자기 챔피언**을 골랐다.
  즉 "같은 조성을 도펀트 위치만 바꿔 세 번" 에 가깝다 — 다만 **통제된 반복은 아니다**
  (같은 후보 목록에서 combined_score 최대값을 뽑은 것이라 서로 독립이 아니다).

  그리고 `de`·`E_GPa`·`pugh` 는 이 세 점의 **산술평균**으로 게이트에 들어간다.

이 도구가 재는 것
  ① 세 챔피언의 조성이 같은가, 다르면 무엇이 얼마나 움직였나
  ② 조성 동일 여부가 **치환 자리 종류**로 설명되는가 (교차표)
  ③ **종내 흩어짐 vs 종간 흩어짐** — 이게 핵심이다.
     종내(같은 종 3점의 범위) 중앙값을 종간(종별 평균들의 표준편차)으로 나눈 비가
     1 에 가까우면, 세 번 돌린 흩어짐이 종끼리의 차이만큼 크다는 뜻이고
     **그 축의 순위는 신호가 아니라 배치 잡음**이다.
  ④ 3점 평균 대신 그중 하나만 써도 순위가 얼마나 뒤집히나

이 도구가 **못 하는 것**
  · 어느 챔피언이 "맞는" 구조인지 말하지 못한다. 흩어짐의 크기만 잰다.
  · 흩어짐이 물리(진짜 자리 의존성)인지 최적화 실패(국소최소 갇힘)인지 구별하지 못한다.
    둘 다 같은 숫자로 나온다 — 구별하려면 같은 자리를 여러 시드로 다시 돌려야 한다.
  · 게이트 통과/탈락이 실제로 뒤집히는지는 여기서 판정하지 않는다 (순위 이동만 본다).
  · 평균이 아닌 다른 집계(중앙값·최소)가 옳다고 주장하지 않는다.

    python3 tools/cascade/audit_label_scatter.py
    python3 tools/cascade/audit_label_scatter.py --out db/properties/cascade_label_scatter_audit.json
    python3 tools/cascade/audit_label_scatter.py --selftest
"""
import argparse, collections, csv, json, os, statistics as st, sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cascade_ids import base_species          # noqa: E402  — 그룹핑 정본

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV = os.path.join(ROOT, "db", "properties", "cascade_v23_all.csv")

#: (열, 짧은 이름, 게이트에서의 쓰임)
#:
#: ⛔ 2026-08-16 (Codex 재감사 P0-2·P0-3) — 앞 판은 두 가지를 틀렸다:
#:   · G1 이 쓰는 열은 `screen_de_per_atom`(어닐 **전**)이 아니라
#:     `rerank_de_post_anneal`(어닐 **후**) 이다. build_screening_funnel.py:93.
#:     비가 0.083 이 아니라 **0.205** 다.
#:   · G4 는 3점 **평균이 아니다.** litransport 의 **x005 한 점**만 쓴다
#:     (build_screening_funnel.py:107,121). 그래서 여기 bvs 비는 "평균이 망쳤다" 가
#:     아니라 **"의미 없는 세 라벨 중 하나를 임의 대표로 골랐다"** 의 근거다.
#:   · `eos_B0_GPa` 는 **게이트 입력이 아니다** (funnel 에 0회 등장). 참고용.
AXES = [("rerank_de_post_anneal", "de_post", "G1 (3점 평균)"),
        ("elastic_E_young_GPa", "E_GPa", "G5 (3점 평균)"),
        ("elastic_pugh_GoverB", "pugh", "G5 (3점 평균)"),
        ("bvs_li_proxy_score", "bvs", "G4 (x005 단일 선택)"),
        ("screen_de_per_atom", "de_screen", "게이트 아님 (어닐 전)"),
        ("eos_B0_GPa", "B0", "게이트 아님")]

#: 이 비를 넘으면 "그 축의 순위는 배치 잡음에 잠겼다" 고 부른다.
NOISE_RATIO = 1.0


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def composition(row, els):
    return {e: float(row["composition_" + e]) for e in els
            if (row.get("composition_" + e) or "") not in ("", "0", "0.0")}


def site_kind(row):
    """치환 '자리 종류' — 세부 Wyckoff 가 아니라 어느 부격자를 건드렸나."""
    return (str(row.get("cation_site", "")).split("_")[0],
            str(row.get("anion_site", "")).split("_")[0])


def group_champions(rows, rank="1", by_base=True):
    """{종: {농도라벨: 행}} — rank_combined==rank 인 챔피언만, 세 라벨이 다 있는 것만.

    ⛔⛔ 2026-08-16 (Codex 재감사 P0-1) — 앞 판은 `dopant` 를 **그대로** 키로 썼다.
      그래서 `WO3` 와 `WO3+Clrich` 가 다른 종이 됐고, 라벨 사이에서 generator 변형이
      바뀐 9종(Al2O3·MgO·MoO3·Nd2O3·Sc2O3·Sm2O3·WO3·Y2O3·ZnO)은 어느 이름으로도
      3점이 안 돼 **통째로 빠졌다.** 81종은 전수가 아니었다 — 정정하면 90종이다.
      (B2O3 는 3슬롯이 전부 +Clrich 라 빠지진 않았지만 `B2O3+Clrich` 라는 **다른 이름**
       으로 세어졌다. 같은 결함의 다른 얼굴이다.)
    """
    key = base_species if by_base else (lambda x: x or "")
    by = collections.defaultdict(dict)
    for r in rows:
        if r.get("rank_combined") != rank:
            continue
        by[key(r.get("dopant", ""))][r.get("concentration_label", "")] = r
    return {k: v for k, v in by.items() if len(v) >= 3}


def composition_audit(by, els):
    """①② 조성 동일 여부와 자리 종류의 교차표 + 다른 종의 상세."""
    cross = collections.Counter()
    differing = []
    for dop, d in sorted(by.items()):
        ks = sorted(d)
        cs = [composition(d[k], els) for k in ks]
        keys = set().union(*[set(c) for c in cs])
        same_comp = all(cs[0].get(e) == c.get(e) for c in cs for e in keys)
        same_kind = len({site_kind(d[k]) for k in ks}) == 1
        cross[(same_comp, same_kind)] += 1
        if not same_comp:
            moved = {e: round(max(c.get(e, 0) for c in cs) - min(c.get(e, 0) for c in cs), 4)
                     for e in keys}
            differing.append({
                "dopant": dop,
                "moved_atoms": {e: v for e, v in sorted(moved.items()) if v},
                "anion_sites": sorted({d[k].get("anion_site", "") for k in ks}),
                "cation_sites": sorted({d[k].get("cation_site", "") for k in ks}),
                "names": [d[k].get("name", "") for k in ks],
            })
    return {
        "n_species": len(by),
        "cross_table": {
            "same_composition_same_site_kind": cross[(True, True)],
            "same_composition_diff_site_kind": cross[(True, False)],
            "diff_composition_same_site_kind": cross[(False, True)],
            "diff_composition_diff_site_kind": cross[(False, False)],
        },
        "interpretation": (
            "⛔ 2026-08-16 정정 — base 종으로 묶으면 '다른 조성 / 같은 자리 종류' 칸이 "
            "**7종** 나온다(앞 판은 raw dopant 로 묶어 0 이었다). 따라서 "
            "'조성 동일 여부가 자리 종류 하나로 완전히 결정된다' 는 **성립하지 않는다.** "
            "같은 부격자에 앉고도 전하 보상 Li 수가 달라 조성이 갈리는 경우가 있다. "
            "다만 '세 라벨의 조성이 같은 것은 설계된 통제가 아니다' 는 그대로다 — "
            "그건 교차표와 무관하게, 라벨이 조성을 지정하지 않기 때문이다."),
        "differing_species": differing,
    }


def scatter_audit(by, axes=AXES, noise_ratio=NOISE_RATIO):
    """③ 종내 vs 종간 흩어짐."""
    out = {}
    for col, name, gate in axes:
        within, means = [], []
        for dop, d in by.items():
            v = [fnum(d[k].get(col)) for k in sorted(d)]
            v = [x for x in v if x is not None]
            if len(v) < 2:
                continue
            within.append(max(v) - min(v))
            means.append(st.mean(v))
        if len(means) < 5:
            out[name] = {"gate": gate, "n": len(means), "verdict": "표본 부족"}
            continue
        w = st.median(within)
        sd = st.pstdev(means)
        ratio = (w / sd) if sd else None
        out[name] = {
            "gate": gate, "n_species": len(means),
            "within_species_range_median": round(w, 4),
            "between_species_sd": round(sd, 4),
            "between_species_range": round(max(means) - min(means), 4),
            "ratio_within_over_between": (round(ratio, 3) if ratio is not None else None),
            "verdict": ("배치 잡음에 잠김" if ratio is not None and ratio >= noise_ratio
                        else "신호가 잡음보다 큼" if ratio is not None else "판정 불가"),
        }
    return out


def rank_stability(by, col="elastic_E_young_GPa", jump=5):   # G5 축 (3점 평균이 맞다)
    """④ 3점 평균 대신 하나만 써도 순위가 얼마나 움직이나."""
    base = {}
    for dop, d in by.items():
        v = [fnum(d[k].get(col)) for k in sorted(d)]
        if len(v) == 3 and all(x is not None for x in v):
            base[dop] = v
    if len(base) < 5:
        return {"column": col, "n": len(base), "moved_ge_jump": None}
    order = [k for k, _ in sorted(base.items(), key=lambda x: st.mean(x[1]))]
    moved = []
    for pick in range(3):
        o = [k for k, _ in sorted(base.items(), key=lambda x: x[1][pick])]
        moved.append(sum(1 for i, k in enumerate(order) if abs(o.index(k) - i) >= jump))
    return {"column": col, "n_species": len(base), "jump_threshold": jump,
            "moved_ge_jump_per_pick": moved,
            "note": ("3점 평균 순위 대비 몇 종이 jump 계단 이상 움직이는가. "
                     "크면 '평균' 이라는 집계 선택 자체가 순위를 만든다는 뜻이다.")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=CSV)
    ap.add_argument("--out", default=None)
    ap.add_argument("--rank", default="1")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    with open(a.csv, encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    els = [k[len("composition_"):] for k in rows[0] if k.startswith("composition_")]
    by = group_champions(rows, a.rank)

    comp = composition_audit(by, els)
    sca = scatter_audit(by)
    rk = rank_stability(by)

    ct = comp["cross_table"]
    print(f"세 라벨이 다 있는 종: {comp['n_species']}")
    print(f"  조성 같음 / 자리종류 같음  {ct['same_composition_same_site_kind']:3d}")
    print(f"  조성 같음 / 자리종류 다름  {ct['same_composition_diff_site_kind']:3d}")
    print(f"  조성 다름 / 자리종류 같음  {ct['diff_composition_same_site_kind']:3d}")
    print(f"  조성 다름 / 자리종류 다름  {ct['diff_composition_diff_site_kind']:3d}")
    off = ct["same_composition_diff_site_kind"] + ct["diff_composition_same_site_kind"]
    print(f"  → 교차 칸 {off}종: "
          + ("자리 종류만으로 결정된다" if not off else
             "**자리 종류만으로는 설명 안 된다** (전하 보상 Li 수도 갈린다)"))
    print(f"  조성이 다른 종 {len(comp['differing_species'])}개: "
          f"{', '.join(x['dopant'] for x in comp['differing_species'][:8])}"
          f"{' …' if len(comp['differing_species']) > 8 else ''}")

    print(f"\n{'축':11s}{'게이트에서의 쓰임':20s}{'종내(중앙)':>11s}{'종간SD':>9s}{'비':>7s}  판정")
    for name, v in sca.items():
        if "ratio_within_over_between" not in v:
            continue
        print(f"{name:11s}{v['gate']:20s}{v['within_species_range_median']:11.3f}"
              f"{v['between_species_sd']:9.3f}{(v['ratio_within_over_between'] or 0):7.2f}  {v['verdict']}")
    print(f"\n{rk['column']}: 평균 대신 한 점만 쓰면 {rk['jump_threshold']}계단 이상 이동 "
          f"{rk['moved_ge_jump_per_pick']} / {rk['n_species']}종")

    doc = {
        "what": ("v23 세 농도 라벨(x002/x005/x010)의 실체와, 그 3점 평균이 게이트 축에 "
                 "얼마나 잡음을 넣는지"),
        "why_labels_are_not_concentrations": (
            "1×1×1 · 4 f.u. 셀은 P 가 4개뿐이고 치환이 정수라 최소 치환이 1/4 = x 0.25 다. "
            "세 라벨이 전부 그 값으로 반올림됐다."),
        "cannot_do": [
            "어느 챔피언이 '맞는' 구조인지 말하지 못한다 — 흩어짐 크기만 잰다",
            "흩어짐이 물리(자리 의존성)인지 최적화 실패(국소최소)인지 구별하지 못한다",
            "게이트 통과/탈락이 실제로 뒤집히는지는 판정하지 않는다 (순위 이동만)",
            "평균이 아닌 다른 집계가 옳다고 주장하지 않는다",
        ],
        "noise_ratio_threshold": NOISE_RATIO,
        "composition_audit": comp,
        "scatter_audit": sca,
        "rank_stability": rk,
    }
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, indent=2, ensure_ascii=False)
        print(f"\n-> {a.out}")
    return 0


def selftest():
    """합성 데이터로 판정 로직을 검사한다. **음성 경로 포함.**"""
    ok = fail = 0

    def chk(name, cond):
        nonlocal ok, fail
        if cond:
            ok += 1
        else:
            fail += 1
            try: print(f"  ✗ {name}")
            except Exception: print(f"  FAIL {name}")

    def mk(dop, label, cat, an, comp, **cols):
        r = {"dopant": dop, "concentration_label": label, "rank_combined": "1",
             "name": f"{dop}_{label}_{cat}{an}", "cation_site": cat, "anion_site": an}
        r.update({"composition_" + e: str(v) for e, v in comp.items()})
        r.update({k: str(v) for k, v in cols.items()})
        return r

    els = ["Li", "S", "Cl"]
    # 같은 자리·같은 조성 3점
    same = [mk("A", f"x{i:03d}", "Li_24g", "S_4a", {"Li": 24, "S": 20, "Cl": 4},
               rerank_de_post_anneal=-0.5 - i * 0.001) for i in (2, 5, 10)]
    # 다른 자리 → 다른 조성
    diff = [mk("B", "x002", "Li_24g", "Cl_4d", {"Li": 24, "S": 23, "Cl": 1}),
            mk("B", "x005", "Li_24g", "Cl_4d", {"Li": 24, "S": 23, "Cl": 1}),
            mk("B", "x010", "Li_24g", "S_4a", {"Li": 24, "S": 20, "Cl": 4})]
    by = group_champions(same + diff)
    chk("세 라벨 다 있는 종만 남는다", set(by) == {"A", "B"})
    # ── base 그룹핑 (2026-08-16 Codex P0-1) ────────────────────────────────
    chk("base_species 접미사 제거", base_species("WO3+Clrich") == "WO3")
    chk("접미사 없으면 그대로", base_species("WO3") == "WO3")
    chk("빈 값도 죽지 않는다", base_species(None) == "" and base_species("") == "")
    # 라벨마다 generator 변형이 바뀐 종: raw 로 묶으면 사라지고 base 로 묶으면 살아난다
    split = [mk("W", "x002", "Li_24g", "S_4a", {"Li": 17, "S": 16, "Cl": 5}),
             mk("W", "x005", "Li_24g", "S_4a", {"Li": 17, "S": 16, "Cl": 5}),
             mk("W", "x010", "P_4b", "S_4a", {"Li": 23, "S": 17, "Cl": 4})]
    split[0]["dopant"] = split[1]["dopant"] = "W+Clrich"
    chk("음성: raw 로 묶으면 사라진다",
        "W" not in group_champions(split, by_base=False)
        and "W+Clrich" not in group_champions(split, by_base=False))
    chk("base 로 묶으면 살아난다", "W" in group_champions(split))
    chk("기본값이 base 그룹핑", set(group_champions(split)) == {"W"})
    ca = composition_audit(by, els)
    ct = ca["cross_table"]
    chk("A: 조성 같음·자리 같음", ct["same_composition_same_site_kind"] == 1)
    chk("B: 조성 다름·자리 다름", ct["diff_composition_diff_site_kind"] == 1)
    chk("교차 칸 0", ct["same_composition_diff_site_kind"] == 0
        and ct["diff_composition_same_site_kind"] == 0)
    chk("다른 종만 상세에 실린다", [x["dopant"] for x in ca["differing_species"]] == ["B"])
    chk("움직인 원자 S3 Cl3", ca["differing_species"][0]["moved_atoms"] == {"S": 3.0, "Cl": 3.0})
    # 음성 ⑩: 같은 자리인데 조성이 다른 경우(전하 보상 차이)를 교차 칸에 제대로 넣는가
    #   — 앞 판은 이 칸이 0 이라고 보고했고 그걸 근거로 "자리로 완전히 결정" 이라고 썼다
    chg = [mk("D", "x002", "Li_24g", "S_4a", {"Li": 18, "S": 17, "Cl": 4}),
           mk("D", "x005", "Li_24g", "S_4a", {"Li": 18, "S": 17, "Cl": 4}),
           mk("D", "x010", "Li_24g", "S_4a", {"Li": 23, "S": 17, "Cl": 4})]
    cc = composition_audit(group_champions(chg), els)["cross_table"]
    chk("음성: 같은 자리·다른 조성이 교차 칸에 들어간다",
        cc["diff_composition_same_site_kind"] == 1)
    chk("음성: 그걸 '같은 조성' 으로 세지 않는다",
        cc["same_composition_same_site_kind"] == 0)
    # 음성 ①: 3점이 안 되면 아예 제외 (2점을 3점처럼 세면 안 된다)
    chk("음성: 2점짜리는 제외", "C" not in group_champions(
        [mk("C", "x002", "Li_24g", "S_4a", {"Li": 1}),
         mk("C", "x005", "Li_24g", "S_4a", {"Li": 1})]))
    # 음성 ②: 자리 종류는 Wyckoff 세부가 아니라 부격자다
    chk("음성: S_4a 와 S_16e 는 같은 종류", site_kind({"cation_site": "Li_24g", "anion_site": "S_4a"})
        == site_kind({"cation_site": "Li_24g", "anion_site": "S_16e"}))
    chk("Cl_4d 는 다른 종류", site_kind({"cation_site": "Li_24g", "anion_site": "Cl_4d"})
        != site_kind({"cation_site": "Li_24g", "anion_site": "S_4a"}))

    # ── 흩어짐 판정 ─────────────────────────────────────────────────────────
    # 종내가 좁고 종간이 넓은 축 → 신호
    sig = []
    for j, dop in enumerate("PQRSTUVWXY"):
        for i in (2, 5, 10):
            sig.append(mk(dop, f"x{i:03d}", "Li_24g", "S_4a", {"Li": 24},
                          rerank_de_post_anneal=-1.0 + 0.2 * j + 0.001 * i))
    s = scatter_audit(group_champions(sig), axes=[("rerank_de_post_anneal", "de_post", "G1")])
    chk("좁은 종내 → 신호", s["de_post"]["verdict"] == "신호가 잡음보다 큼")
    chk("비가 1 미만", s["de_post"]["ratio_within_over_between"] < 1.0)
    # 음성 ③: 종내가 종간만큼 넓으면 **잡음** 이라고 말해야 한다
    # ⚠ 잡음은 **종마다 다른 방향**이어야 한다. 모든 종에 같은 오프셋을 주면
    #   한 점만 뽑아도 순위가 그대로라 rank_stability 가 0 이 나온다 (내 첫 픽스처의 오류).
    noi = []
    for j, dop in enumerate("PQRSTUVWXY"):
        offs = [0.0, 0.6, 1.2] if j % 2 == 0 else [1.2, 0.0, 0.6]
        for n, i in enumerate((2, 5, 10)):
            noi.append(mk(dop, f"x{i:03d}", "Li_24g", "S_4a", {"Li": 24},
                          rerank_de_post_anneal=-1.0 + 0.2 * j + offs[n]))
    s2 = scatter_audit(group_champions(noi), axes=[("rerank_de_post_anneal", "de_post", "G1")])
    chk("음성: 넓은 종내 → 배치 잡음", s2["de_post"]["verdict"] == "배치 잡음에 잠김")
    chk("음성: 비가 1 이상", s2["de_post"]["ratio_within_over_between"] >= 1.0)
    # 음성 ④: 표본이 적으면 판정하지 않는다 (억지로 비를 만들지 않는다)
    few = [mk("Z", f"x{i:03d}", "Li_24g", "S_4a", {"Li": 1}, rerank_de_post_anneal=-1.0)
           for i in (2, 5, 10)]
    s3 = scatter_audit(group_champions(few), axes=[("rerank_de_post_anneal", "de_post", "G1")])
    chk("음성: 표본 부족이면 판정 안 함", s3["de_post"]["verdict"] == "표본 부족")
    # 음성 ⑤: 값이 없는 열은 세지 않는다
    s4 = scatter_audit(group_champions(sig), axes=[("nonexistent_col", "nope", "—")])
    chk("음성: 없는 열은 판정 불가", s4["nope"]["verdict"] == "표본 부족")

    # ── 순위 안정성 ─────────────────────────────────────────────────────────
    rk = rank_stability(group_champions(sig), col="rerank_de_post_anneal", jump=2)
    chk("안정한 축은 이동 0", rk["moved_ge_jump_per_pick"] == [0, 0, 0])
    rk2 = rank_stability(group_champions(noi), col="rerank_de_post_anneal", jump=2)
    chk("음성: 불안정한 축은 이동 > 0", max(rk2["moved_ge_jump_per_pick"]) > 0)

    try: print(f"\nselftest: {ok} passed, {fail} failed")
    except Exception: print(f"\nselftest: {ok} passed, {fail} failed")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main() or 0)
