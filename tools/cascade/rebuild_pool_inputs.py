#!/usr/bin/env python3
"""rebuild_pool_inputs.py — 풀 입력 2종을 **자동으로** 만든다 (champions.csv · ESW csv).

왜 이 도구가 있나 (2026-08-13)
  이 두 파일은 여태 **손으로** 만들어졌다. 그래서 2026-06-29 에 사람이 멈추자 파이프라인이
  같이 멈췄고, 7/11 에 끝난 계산 43종이 정본에 못 들어왔다
  (kb/methodology/cascade_pipeline_anatomy_2026_08_13.md). 손 단계를 없애는 것이 목적이다.

체인에서의 위치
    cascade_v23_all.csv (= unified_dataset_273.csv)
    oxidation_stability_cascade_v2.json (esw_cascade_batch.py 산출)
            ↓  **이 도구**
    cascade_v23_champions.csv  ·  oxidation_stability_cascade.csv
            ↓  tools/figures/plot_cascade_insights.py
    cascade_v23_ranked.csv
            ↓  tools/cascade/build_screening_funnel.py
    cascade_screening_funnel.json

ESW csv 의 plain/Cl-rich 분리
  옛 판이 `ox_V`(plain champion) 와 `clrich_ox_V`(+Clrich chain 변형) 를 **다른 열**로 실었다.
  그 규약을 그대로 재현한다 — 섞으면 "6종이 2.14 를 넘었다" 같은 집계가 조용히 달라진다.

  python3 tools/cascade/rebuild_pool_inputs.py --selftest
  python3 tools/cascade/rebuild_pool_inputs.py            # db/properties 에 _v2 접미사로 출력
  python3 tools/cascade/rebuild_pool_inputs.py --inplace  # 기존 파일을 덮어쓴다 (백업 먼저)

이 도구가 못 하는 것
  · 값을 검증하지 않는다. 입력 CSV/JSON 을 그대로 재배열할 뿐이다.
  · champion 을 다시 고르지 않는다 (`rank_combined == 1` 을 그대로 믿는다).
  · ranked.csv 와 funnel 은 만들지 않는다 — 위 체인의 다음 두 도구가 한다.
"""
import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROP = ROOT / "db" / "properties"

#: 음이온별 형식 원자가. plot_cascade_insights.py 의 ANION_VAL 과 같아야 한다.
ANION_VAL = {"O": 2, "S": 2, "N": 3, "F": 1, "Cl": 1, "Br": 1, "I": 1}
LANTH = {"La", "Nd", "Sm", "Gd"}
ALKALI = {"Li", "Na"}
AE = {"Mg", "Ca", "Sr", "Ba"}
MAIN = {"B", "Al", "Ga", "In", "Si", "Ge", "Sn", "Sb"}

#: champions.csv 가 실어야 하는 열 (plot_cascade_insights.py 가 읽는 것 + 계보용)
CHAMP_COLS = ["_dir", "dopant", "concentration", "rerank_de_post_anneal",
              "anneal_dV_pct", "eos_B0_GPa", "eos_fit_quality_ok",
              "elastic_E_young_GPa", "elastic_B_hill_GPa", "elastic_G_hill_GPa",
              "elastic_poisson_nu", "elastic_pugh_GoverB",
              "sigma_300K_S_cm_NE", "sigma_md_Ea_eV", "wad_J_m2_mean",
              "anneal_converged", "combined_score", "rank_combined"]


def parse_dopant(d):
    """`Al2O3+Clrich` → ('Al', 'O', 3, 'main-group'). 미지 음이온이면 예외."""
    d = d.split("+")[0]
    toks = [(e, int(n) if n else 1)
            for e, n in re.findall(r"([A-Z][a-z]?)(\d*)", d) if e]
    an = [e for e, _ in toks if e in ANION_VAL]
    if not an:
        raise ValueError(f"음이온을 못 찾았다: {d} — ANION_VAL 에 추가할 것")
    anion = an[-1]
    cats = [(e, n) for e, n in toks if e != anion]
    if not cats:
        raise ValueError(f"양이온을 못 찾았다: {d}")
    cat = cats[0]
    bn = [n for e, n in toks if e == anion][0]
    val = round(ANION_VAL[anion] * bn / cat[1])
    grp = ("lanthanide" if cat[0] in LANTH else "alkali" if cat[0] in ALKALI
           else "alk.earth" if cat[0] in AE else "main-group" if cat[0] in MAIN
           else "TM")
    return cat[0], anion, val, grp


def build_champions(all_csv):
    """cascade_v23_all.csv → champion 행만 (rank_combined == 1)."""
    rows = list(csv.DictReader(open(all_csv, encoding="utf-8")))
    if not rows:
        raise ValueError(f"빈 입력: {all_csv}")
    champs = [r for r in rows if str(r.get("rank_combined", "")).strip() == "1"]
    out = []
    for r in champs:
        o = {}
        for c in CHAMP_COLS:
            if c == "_dir":
                o[c] = r.get("_dir") or r.get("name", "")
            else:
                o[c] = r.get(c, "")
        out.append(o)
    return out, len(rows)


def build_esw_csv(esw_json):
    """ESW json → 도펀트당 1행. plain 과 +Clrich 를 **다른 열**로 나눈다."""
    j = json.load(open(esw_json, encoding="utf-8"))
    recs = j.get("results", j)
    plain, clr = {}, {}
    for k, v in recs.items():
        ox = v.get("oxidation_limit_V")
        if ox is None:
            continue
        sp = str(v.get("dopant", "")).split("+")[0]
        if not sp:
            continue
        tgt = clr if "chain_Cl" in k else plain
        # 같은 도펀트의 여러 농도 중 **가장 높은 onset** 을 대표로 (옛 판 규약)
        if sp not in tgt or ox > tgt[sp]["oxidation_limit_V"]:
            tgt[sp] = v
    rows = []
    for sp in sorted(set(plain) | set(clr)):
        base = plain.get(sp) or clr[sp]
        cat, anion, val, grp = parse_dopant(sp)
        note = []
        win = base.get("window_V")
        if win is not None and win < 0.05:
            note.append("collapse=window<0.05V")
        if sp in clr and sp in plain:
            d = clr[sp]["oxidation_limit_V"] - plain[sp]["oxidation_limit_V"]
            if abs(d) > 0.01:
                note.append(f"Cl-rich:ox->{clr[sp]['oxidation_limit_V']:.3f}")
        if sp not in plain:
            note.append("plain champion 없음 — Cl-rich 값으로 대체")
        rows.append({
            "dopant": sp, "anion": anion, "valence": val, "group": grp,
            "ox_V": base.get("oxidation_limit_V"),
            "red_V": base.get("reduction_limit_V"),
            "ocv_V": base.get("ocv_self_decomposition_V"),
            "window_V": win,
            "clrich_ox_V": (clr[sp]["oxidation_limit_V"] if sp in clr and sp in plain
                            else ""),
            "note": " ; ".join(note),
        })
    return rows


#: litransport 가 싣는 열 (build_screening_funnel.load_pool 이 `_dir` 로 조인한다)
LITRANS_COLS = ["_dir", "bvs_li_proxy_score", "migration_volume_fraction",
                "tier2_dopant_blocking_fraction", "tier2_li_li_disorder_std",
                "cation_site", "anion_site"]


def build_litransport(all_csv):
    """champion 행만 뽑아 G4 축 입력을 만든다. `_dir` 은 `<dopant>_x0NN` 형식이어야
    한다 — funnel 이 `rpartition('_x')` 로 도펀트와 농도를 가른다."""
    import re
    rows = list(csv.DictReader(open(all_csv, encoding="utf-8")))
    out = []
    for r in rows:
        if str(r.get("rank_combined", "")).strip() != "1":
            continue
        name = r.get("_dir") or r.get("name", "")
        # Ag2O_x020_cLi24ga... → Ag2O_x005 (funnel 은 x002/x005/x010 을 기대한다)
        m = re.match(r"(.+?)_x(\d+)", name)
        if not m:
            continue
        pct = {"002": "002", "005": "005", "010": "010",
               "020": "002", "050": "005", "100": "010"}.get(m.group(2))
        if not pct:
            continue
        o = {c: r.get(c, "") for c in LITRANS_COLS}
        o["_dir"] = f"{m.group(1)}_x{pct}"
        out.append(o)
    return out


def write_esw_csv(rows, path, src):
    # ⚠ 주석줄은 **csv.writer 로 쓰지 않는다**. 줄 안에 쉼표가 있으면 writer 가
    #   따옴표로 감싸 `"#...` 가 되고, 소비자의 `line.startswith("#")` 주석 필터를
    #   빠져나가 헤더 파싱이 깨진다 (2026-08-14 build_screening_funnel 에서 실측).
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write(f"# grand-potential ESW per cascade dopant (UMA champion composition; "
                f"MP GGA_GGA+U hull). Source: {os.path.basename(src)} via "
                f"tools/cascade/rebuild_pool_inputs.py\n")
        f.write("# ox_V = PLAIN champion; clrich_ox_V = +Clrich chain variant "
                "(blank = no variant or no plain). Do not merge the two.\n")
        w = csv.writer(f)
        w.writerow(list(rows[0]))
        for r in rows:
            w.writerow([r[k] for k in rows[0]])


#: gate 입력으로 **실제로** 쓰이는 열. 하나라도 비면 그 (종, 라벨) 은 평가에 못 들어간다.
#
#  ⛔ 2026-08-14 정정 (Codex 리뷰 P0-3). 처음 판은 `eos_B0_GPa` 를 넣고
#  `elastic_pugh_GoverB` 를 뺐는데 **둘 다 거꾸로**였다. build_screening_funnel.py 의
#  load_pool() 이 게이트에 쓰는 값은 de · ox_V/window_V · bvs · blocking · E_GPa ·
#  **pugh(GoverB, G5 연성축)** 이고, `eos_B0_GPa` 는 **어느 게이트도 쓰지 않는다**
#  (화면 표시용). 그래서 옛 71/18/1 은 gate completeness 가 아니었다.
GATE_INPUT_COLS = {
    "champions":   ["rerank_de_post_anneal",      # → ranked.de   (G1 안정성)
                    "elastic_E_young_GPa",        # → ranked.E_GPa (G5 기계)
                    "elastic_pugh_GoverB"],       # → ranked.pugh  (G5 연성)
    "litransport": ["bvs_li_proxy_score",         # → G4 transport_norm
                    "tier2_dopant_blocking_fraction"],  # → G4 blocking 게이트
}
#: 게이트가 **안 쓰는데** champions csv 에 있는 열 — 완결성 판정에 넣지 않는다.
NON_GATE_COLS = ["eos_B0_GPa", "eos_fit_quality_ok", "anneal_dV_pct",
                 "elastic_B_hill_GPa", "elastic_G_hill_GPa", "elastic_poisson_nu"]


def audit_completeness(champ_rows, lit_rows, esw_rows):
    """⛔ 2026-08-14 (Codex 감사) — "90종 funnel" 은 틀린 표현이다.

    ESW 는 90종이지만 gate 입력(형성에너지·탄성·BVS)이 비면 그 종은 랭킹·깔때기에서
    **조용히 빠진다**. AlI₃ 가 정확히 그 경우였고(champion 3개·litransport 3개 전부 결측),
    MgI₂ 는 x050 이 통째로 비었는데 나머지 두 라벨 평균으로 살아남았다.
    → 종을 dropped / partial / complete 로 갈라 기록한다. 화면은 이 판정을 그대로 쓴다.
    """
    def base(x):
        import re
        return re.sub(r"_x\d+.*$", "", x).split("+")[0]

    def blank(v):
        return str(v).strip() in ("", "nan", "None", "NA")

    per = {}
    for r in champ_rows:
        sp = base(r.get("_dir") or r.get("dopant", ""))
        d = per.setdefault(sp, {"champ_ok": 0, "champ_n": 0, "lit_ok": 0, "lit_n": 0})
        d["champ_n"] += 1
        if not any(blank(r.get(c, "")) for c in GATE_INPUT_COLS["champions"]):
            d["champ_ok"] += 1
    for r in lit_rows:
        sp = base(r.get("_dir", ""))
        d = per.setdefault(sp, {"champ_ok": 0, "champ_n": 0, "lit_ok": 0, "lit_n": 0})
        d["lit_n"] += 1
        if not any(blank(r.get(c, "")) for c in GATE_INPUT_COLS["litransport"]):
            d["lit_ok"] += 1

    esw_sp = {r["dopant"] for r in esw_rows}
    dropped, partial, complete = {}, {}, []
    for sp in sorted(esw_sp):
        d = per.get(sp, {"champ_ok": 0, "champ_n": 0, "lit_ok": 0, "lit_n": 0})
        if d["champ_ok"] == 0 or d["lit_ok"] == 0:
            dropped[sp] = (f"gate 입력 전면 결측 — champion {d['champ_ok']}/{d['champ_n']} · "
                           f"litransport {d['lit_ok']}/{d['lit_n']}. ESW 만 있고 평가 불가")
        elif d["champ_ok"] < d["champ_n"] or d["lit_ok"] < d["lit_n"]:
            partial[sp] = (f"부분 결측 — champion {d['champ_ok']}/{d['champ_n']} · "
                           f"litransport {d['lit_ok']}/{d['lit_n']}. 남은 라벨 평균으로 평가됨")
        else:
            complete.append(sp)
    return {
        "audited": "2026-08-14",
        "audited_by": "tools/cascade/rebuild_pool_inputs.py --audit (Codex 감사 반영)",
        "headline": (f"ESW {len(esw_sp)}종 회수 → gate 평가 {len(esw_sp) - len(dropped)}종 "
                     f"(전면 결측 {len(dropped)} · 부분 결측 {len(partial)})"),
        "⛔_do_not_say": "\"90종 funnel\" — 정확히는 \"90종 회수 → 89종 부분평가\"다.",
        "n_esw": len(esw_sp), "n_evaluable": len(esw_sp) - len(dropped),
        "n_complete": len(complete), "dropped": dropped, "partial": partial,
        "gate_input_cols": GATE_INPUT_COLS,
        "non_gate_cols": NON_GATE_COLS,
        "gate_input_basis": (
            "build_screening_funnel.py load_pool() 이 게이트에 실제로 넣는 값만 센다: "
            "de(G1) · E_GPa·pugh(G5) · bvs·blocking(G4). "
            "⛔ eos_B0_GPa 는 어느 게이트도 쓰지 않는다 — 2026-08-14 이전 판은 그것을 세고 "
            "pugh 를 빼서 gate completeness 가 아니었다 (Codex 리뷰 P0-3)."),
    }


#: ── artifact manifest ────────────────────────────────────────────────────
#  왜: 화면 최상단 숫자가 data.py 하드코드였다. "이게 정본" 이라고 부를 수 없다
#  (2026-08-14 Codex 리뷰 P1). 파일의 sha256·바이트·주석 제외 행수를 같이 굳혀서
#  **파일이 바뀌면 화면이 조용히 옛말을 하지 않고 fail-closed** 되게 한다.
#
#  status 어휘 (5개, 이 밖의 값은 loader 가 거부한다):
#    historical            — 재현 가능하지만 캠페인 커버리지 기준으로는 대체됨
#    recovered_unvalidated — 회수됐고 검증 전. 다운로드는 되지만 결과로 인용 금지
#    approved              — 승인된 정본 (현재 cascade 에는 **하나도 없다**)
#    superseded            — 더 나은 세대가 있음
#    invalid               — 생성기 결함이 확인됨. 화면에서 차단
MANIFEST_STATUS = ("historical", "recovered_unvalidated", "approved", "superseded", "invalid")

#: (파일, status, 한 줄 설명, 한계)
MANIFEST_ARTIFACTS = [
    ("cascade_v23_all.csv", "recovered_unvalidated",
     "완주 원자료 (unified_dataset_273.csv 회수분)",
     ["UMA 상대값", "일부 열은 재계산 세대가 섞여 있을 수 있음"]),
    ("cascade_v23_champions_v2.csv", "recovered_unvalidated",
     "champion 270행 (rank_combined==1)",
     ["champion 재선정 안 함", "Na2S_x100 은 B_hill 음수 — 탄성 계산 실패 행"]),
    ("cascade_v23_litransport_v2.csv", "recovered_unvalidated",
     "G4 정적 프록시 270행",
     ["legacy Adams-2003 BVS — 정본 softBV 아님", "blocking 은 4 Å foreign-center count"]),
    ("oxidation_stability_cascade_v2.csv", "recovered_unvalidated",
     "grand-potential ESW 90종",
     ["phase_set_id·mp-ID·MP 스냅샷 미기록 — 재현 불가",
      "host onset 2.140 V 는 phase set 의존 (LiS4 제외 시 2.256 V)"]),
    ("cascade_v23_ranked_v2.csv", "recovered_unvalidated",
     "합성점수 랭킹 89종 (AlI3 제외)",
     ["G4 순환 (blocking 이 BVS 를 덮어씀)", "G5 median 컷은 로스터 상대",
      "가중치 수작업", "min-max 정규화라 풀이 바뀌면 값이 바뀜"]),
    ("cascade_v23_all_20260629_47species.csv", "historical",
     "2026-06-29 취합 경계판 (47종)", ["캠페인 커버리지 기준으로 superseded"]),
    ("cascade_v23_ranked.csv", "superseded",
     "47종 랭킹 — 역사 스냅샷", ["결과로 인용 금지", "90종 회수 이전 판"]),
    ("cascade_screening_funnel.json", "historical",
     "47종 게이트 감사", ["G3 phase set 미기록", "G4 순환", "G5 로스터 상대"]),
    ("cascade_screening_funnel_v2.json", "recovered_unvalidated",
     "89종 게이트 감사", ["위와 동일 + 풀 상대 정규화 재계산됨"]),
    ("cascade_pool_audit_v2.json", "recovered_unvalidated",
     "gate 입력 완결성 감사", ["행 존재만 본다 — 값의 물리성은 안 본다"]),
]


def _sha_rows(path):
    """sha256 · 바이트 · **주석(#) 제외** 데이터 행수. csv 는 헤더도 뺀다."""
    import hashlib
    b = path.read_bytes()
    n = None
    if path.suffix == ".csv":
        lines = [l for l in b.decode("utf-8", "replace").splitlines()
                 if l.strip() and not l.startswith("#")]
        n = max(0, len(lines) - 1)          # 헤더 1줄
    return hashlib.sha256(b).hexdigest(), len(b), n


#: Codex 감사 산출물 (2026-08-14 인계). 5개 패널 + 게이트별 완결성 표.
#:  ⚠ PNG 는 `9abe5105` 에서 만든 것을 그대로 쓴다 — 이 컨테이너엔 플로터가 쓰는
#:  TrueType 폰트가 없어 재생성하면 바이트가 달라져 무결성이 깨진다.
AUDIT_FIGURES = ["campaign_status", "g3_phase_set", "g4_rescore",
                 "interface_axes", "ml_validation"]
AUDIT_SUPPORTING = ["cascade_audit_gate_completeness.csv"]
PINNED_SOURCE_COMMIT = "9abe5105cacafa22ab3e185f09e2a4c37118b9a9"


def _meta(path, csv_rows=False):
    """sha256 · bytes (· 주석 제외 데이터 행수). plot_cascade_audit 의 _file_meta 와 같은 규약."""
    import hashlib
    b = path.read_bytes()
    it = {"sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
    if csv_rows:
        lines = [x for x in b.decode("utf-8-sig").splitlines() if x and not x.startswith("#")]
        it["rows"] = max(0, len(lines) - 1)
    return it


def build_manifest(audit):
    """artifact manifest — 화면 최상단 숫자의 **유일한 기계 계약**.

    스키마는 Codex 의 `tools/figures/plot_cascade_audit_2026_08.py` 가 검증하는
    schema_version 2 를 따르고, 거기에 우리 webapp 이 쓰는 `artifacts` 블록을 얹는다.
    두 도구가 같은 파일을 보므로 스키마가 갈라지면 안 된다.
    """
    arts = []
    for fn, status, desc, lims in MANIFEST_ARTIFACTS:
        p = PROP / fn
        if not p.exists():
            continue
        assert status in MANIFEST_STATUS, f"알 수 없는 status: {status}"
        sha, nbytes, nrows = _sha_rows(p)
        arts.append({
            "artifact_id": f"cascade-v23-{p.stem}",
            "source_path": f"db/properties/{fn}",
            "status": status, "description": desc,
            "sha256": sha, "bytes": nbytes, "rows": nrows,
            "actual_x": 0.25, "campaign_labels": ["x002", "x005", "x010"],
            "limitations": lims,
        })
    # ── Codex schema_version 2 가 요구하는 블록 ────────────────────────────
    figs = []
    for name in AUDIT_FIGURES:
        img = ROOT / "docs" / "figures" / "cascade" / f"cascade_audit_{name}.png"
        tab = PROP / f"cascade_audit_{name}.csv"
        if not (img.is_file() and tab.is_file()):
            continue
        im, tb = _meta(img), _meta(tab, csv_rows=True)
        figs.append({"image": f"docs/figures/cascade/{img.name}",
                     "csv": f"db/properties/{tab.name}", "status": "audit-current",
                     "image_sha256": im["sha256"], "image_bytes": im["bytes"],
                     "csv_sha256": tb["sha256"], "csv_bytes": tb["bytes"], "csv_rows": tb["rows"]})
    sup = []
    for fn in AUDIT_SUPPORTING:
        p = PROP / fn
        if p.is_file():
            it = _meta(p, csv_rows=True)
            sup.append({"path": f"db/properties/{fn}", "status": "audit-current", **it})

    return {
        "property": "cascade_audit_manifest",
        # Codex 플로터 계약 — 이 세 값이 바뀌면 --validate-only 가 막는다
        "schema_version": 2,
        "artifact_id": "cascade-audit-2026-08-14",
        "status": "audit_current__leaderboard_unavailable",
        "source_commit": PINNED_SOURCE_COMMIT,
        "source_of_truth": "docs/reviews/cascade_dftweb_source_of_truth_2026_08_14.md",
        "figures": figs,
        "supporting_tables": sup,
        "generated_by": "tools/cascade/rebuild_pool_inputs.py (schema는 plot_cascade_audit_2026_08.py 와 공유)",
        "contract": ("화면 최상단 숫자와 artifact 지위의 유일한 출처. loader 는 여기 없는 "
                     "artifact 나 MANIFEST_STATUS 밖의 status 를 만나면 표시하지 않고 "
                     "fail-closed 한다. sha256/rows 가 어긋나면 stale 로 막는다."),
        "status_vocabulary": list(MANIFEST_STATUS),
        # ⚠ 이 네 수는 화면 타일의 출처다. audit 에서 파생하고 손으로 안 적는다.
        # ⚠ 키 이름은 Codex 플로터가 **정확히 대조**한다 — 바꾸면 validate 가 막는다.
        "headline": {
            "planned_slots": 273, "completed_slots": 270,
            "completed_species": audit["n_esw"],
            "historical_snapshot_species": 47,
            "approved_current_leaderboard_species": 0,
            "explicit_pair_property_labels": 0,
        },
        "headline_basis": ("273 = master_batch_273.sh 의 91 화합물 × 3 라벨. "
                           "270 = 완주 슬롯(As₂S₃ 3건 seed 실패). "
                           "completed_species 는 ESW 회수분에서 센다. "
                           "approved = 0 은 판정이다 — 결측이 아니라 점수·게이트 타당성이 미해결."),
        "actual_x": 0.25,
        "actual_x_note": ("라벨 x002/x005/x010 은 1×1×1 · 4 f.u. 셀의 정수 치환 때문에 "
                          "셋 다 실측 x=0.25 다. 농도 스윕도 반복실험도 아니다."),
        "host": {"formula_hint": "Li₆PS₅Cl 계열 (Cl:P = 1.0)",
                 "evidence": "ESW 반응식 좌변 Li22P4(S5Cl)4 계열",
                 "not": "Model C (Li₅.₄PS₄.₄Cl₁.₆) 가 아니다"},
        "artifacts": arts,
    }


def selftest():
    """양성 + **음성**. 옛 판이 틀리던 입력과 plain/Clrich 분리를 확인한다."""
    import tempfile
    ok = True

    def chk(c, m):
        nonlocal ok
        print(("  ✓ " if c else "  ✗ ") + m)
        ok &= bool(c)

    chk(parse_dopant("Al2O3+Clrich")[:3] == ("Al", "O", 3), "변형 접미사를 떼고 파싱")
    chk(parse_dopant("ZrCl4")[:3] == ("Zr", "Cl", 4), "염화물 (옛 판은 F/1 로 오인)")
    chk(parse_dopant("Li3N")[:3] == ("Li", "N", 1), "질화물")
    try:
        parse_dopant("Xx9"); chk(False, "미지 음이온을 통과시켰다")
    except ValueError:
        chk(True, "미지 음이온 → 예외 (조용한 오분류 금지)")

    td = Path(tempfile.mkdtemp(prefix="rebuild_pool_st_"))
    # champions: rank_combined 가 1 인 행만 골라야 한다
    ac = td / "all.csv"
    with open(ac, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["name", "dopant", "rank_combined",
                                          "rerank_de_post_anneal", "elastic_E_young_GPa"])
        w.writeheader()
        w.writerow({"name": "A_x020_s0", "dopant": "Al2O3", "rank_combined": "1",
                    "rerank_de_post_anneal": "-0.8", "elastic_E_young_GPa": "40"})
        w.writerow({"name": "A_x020_s1", "dopant": "Al2O3", "rank_combined": "2",
                    "rerank_de_post_anneal": "-0.7", "elastic_E_young_GPa": "41"})
    ch, ntot = build_champions(ac)
    chk(len(ch) == 1 and ntot == 2, f"champion 1행만 (전체 {ntot} 중 {len(ch)})")
    chk(ch[0]["_dir"] == "A_x020_s0", "_dir 없으면 name 으로 채운다")

    # ESW: plain 과 chain_Cl 이 **다른 열**로 가야 한다
    ej = td / "esw.json"
    json.dump({"results": {
        "Al2O3_x050_cLi_s0":               {"dopant": "Al2O3", "oxidation_limit_V": 2.140,
                                            "reduction_limit_V": 1.37, "window_V": 0.77},
        "Al2O3_x020_chain_Cl_x200_cLi_s0": {"dopant": "Al2O3+Clrich", "oxidation_limit_V": 2.354,
                                            "reduction_limit_V": 1.72, "window_V": 0.64},
        "FeCl3_x020_cLi_s0":               {"dopant": "FeCl3", "oxidation_limit_V": 1.808,
                                            "reduction_limit_V": 1.804, "window_V": 0.004},
    }}, open(ej, "w"))
    rows = build_esw_csv(ej)
    al = next(r for r in rows if r["dopant"] == "Al2O3")
    chk(al["ox_V"] == 2.140 and al["clrich_ox_V"] == 2.354,
        f"plain 2.140 / clrich 2.354 분리 (ox={al['ox_V']} clr={al['clrich_ox_V']})")
    # ★ 음성: 섞어서 max 를 쓰면 안 된다
    chk(al["ox_V"] != 2.354, "ox_V 에 Cl-rich 값이 새어들지 않는다")
    fe = next(r for r in rows if r["dopant"] == "FeCl3")
    chk("collapse" in fe["note"], f"window<0.05 → collapse 플래그 ({fe['note']})")
    chk(fe["anion"] == "Cl" and fe["valence"] == 3, "회수 계열도 정상 분류")

    # ★ 음성: 주석줄이 따옴표로 감싸이면 소비자의 `#` 필터를 빠져나가 헤더가 깨진다
    ep = td / "esw.csv"
    write_esw_csv(rows, ep, "x.json")
    lines = open(ep, encoding="utf-8").read().splitlines()
    chk(all(l.startswith("#") for l in lines[:2]),
        f"주석줄이 따옴표 없이 '#' 로 시작 ({lines[0][:12]!r})")
    parsed = list(csv.DictReader(l for l in open(ep, encoding="utf-8")
                                 if not l.startswith("#")))
    chk(parsed and "dopant" in parsed[0],
        f"'#' 필터만으로 헤더가 잡힌다 ({list(parsed[0])[:3] if parsed else '실패'})")

    import shutil
    shutil.rmtree(td, ignore_errors=True)
    print("selftest " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all_csv", default=str(PROP / "cascade_v23_all.csv"))
    ap.add_argument("--esw_json", default=str(PROP / "oxidation_stability_cascade_v2.json"))
    ap.add_argument("--inplace", action="store_true",
                    help="기존 champions.csv / oxidation_stability_cascade.csv 를 덮는다")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    suf = "" if a.inplace else "_v2"
    ch, ntot = build_champions(a.all_csv)
    p1 = PROP / f"cascade_v23_champions{suf}.csv"
    with open(p1, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CHAMP_COLS)
        w.writeheader()
        w.writerows(ch)
    print(f"[champions] {p1}  {len(ch)}행 (전체 {ntot}행 중 rank_combined==1)")

    lit = build_litransport(a.all_csv)
    p3 = PROP / f"cascade_v23_litransport{suf}.csv"
    with open(p3, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=LITRANS_COLS)
        w.writeheader()
        w.writerows(lit)
    print(f"[litransport] {p3}  {len(lit)}행")

    rows = build_esw_csv(a.esw_json)
    p2 = PROP / f"oxidation_stability_cascade{suf}.csv"
    write_esw_csv(rows, p2, a.esw_json)
    n_clr = sum(1 for r in rows if r["clrich_ox_V"] != "")
    print(f"[esw]       {p2}  {len(rows)}종 · Cl-rich 비교 가능 {n_clr}종")

    audit = audit_completeness(ch, lit, rows)
    p4 = PROP / f"cascade_pool_audit{suf}.json"
    json.dump(audit, open(p4, "w"), ensure_ascii=False, indent=1)
    open(p4, "a").write("\n")
    print(f"[audit]     {p4}  {audit['headline']}")
    if audit["dropped"]:
        print(f"            ⛔ 전면 결측: {' '.join(sorted(audit['dropped']))}")
    if audit["partial"]:
        print(f"            ⚠ 부분 결측: {' '.join(sorted(audit['partial']))}")

    # ⛔ 2026-08-14 (Codex Round-3 P0-1) — 이 도구는 manifest 를 **쓰지 않는다.**
    #   두 생산자가 같은 원장을 통째로 덮어써서 늦게 돈 쪽이 상대의 계약 블록을 지웠다.
    #   지금은 sidecar 만 쓰고, 원장은 build_cascade_audit_manifest.py 가 단독 소유한다.
    print("다음: python3 tools/cascade/build_cascade_audit_manifest.py  (원장 갱신)")
    print("다음: python3 tools/figures/plot_cascade_insights.py "
          "→ cascade_v23_ranked.csv → tools/cascade/build_screening_funnel.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
