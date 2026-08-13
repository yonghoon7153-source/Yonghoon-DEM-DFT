#!/usr/bin/env python3
"""build_cascade_audit_manifest.py — cascade 감사 원장의 **단독 소유자**.

왜 이 도구가 생겼나 (2026-08-14, Codex Round-3 P0-1)
  `plot_cascade_audit_2026_08.py` 와 `rebuild_pool_inputs.py` 가 **같은**
  `db/properties/cascade_audit_manifest.json` 을 서로 다른 깊이로 통째로 덮어썼다.
  나중에 돈 쪽이 이겨서, 그 커밋의 manifest 에는 플로터의 핵심 계약 블록
  (`datasets`·`metric_contract`·`source_hashes`·`recovered_artifacts`)이 통째로 없었다.
  `--validate-only` 는 schema/source/headline 과 figure·support 해시만 보므로 **그 결손을
  못 잡는다**. 두 생산자가 한 파일을 쓰는 구조 자체가 결함이었다.

  → 지금 규약: **생산자는 sidecar 만 쓴다. 최종 manifest 는 이 도구만 쓴다.**

      rebuild_pool_inputs.py  → cascade_pool_audit_v2.json          (sidecar)
                              → cascade_audit_artifacts_sidecar.json (sidecar)
      plot_cascade_audit.py   → cascade_audit_*.csv / *.png          (sidecar)
                              ↓
              **이 도구** → cascade_audit_manifest.json  (유일한 writer)

artifact 별 provenance (Codex Round-3 P0-2)
  최상위 `source_commit` 하나로 전부를 덮으면 거짓말이 된다 — Na₂S 정정으로
  `ranked_v2` 만 뒤 커밋 산출물이 됐는데 원장은 `9abe5105` 이라고 적고 있었다.
  이제 artifact 마다 `source_commit` · `derived_from` · `override_reason` 을 싣는다.

  python3 tools/cascade/build_cascade_audit_manifest.py
  python3 tools/cascade/build_cascade_audit_manifest.py --check     # 쓰지 않고 검증만
  python3 tools/cascade/build_cascade_audit_manifest.py --selftest

이 도구가 못 하는 것
  · 값을 검증하지 않는다. 파일의 해시·바이트·행수와 **선언된 지위**만 굳힌다.
  · 그림을 만들지 않는다 (plot_cascade_audit_2026_08.py 담당).
  · status 를 추론하지 않는다 — ARTIFACTS 표에 사람이 적은 값을 쓴다.
  · G3 의 phase-set 정체성을 복구하지 못한다. 그건 재계산이 필요하다.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROP = ROOT / "db" / "properties"
FIGD = ROOT / "docs" / "figures" / "cascade"
OUT = PROP / "cascade_audit_manifest.json"

#: 고정 소스 — 감사 패널이 만들어진 커밋.
PINNED_SOURCE_COMMIT = "9abe5105cacafa22ab3e185f09e2a4c37118b9a9"
#: Na₂S 정정 커밋. `ranked_v2` 만 이쪽 산출물이다.
NA2S_FIX_COMMIT = "922332c0"

#: ── status 어휘 통일 (Codex Round-3 P1) ──────────────────────────────────
#  전에는 세 축이 뒤섞여 있었다: manifest 5종 · 최상위 `audit_current__…` ·
#  figure 의 `audit-current`. **릴리스 지위**와 **artifact 승인 지위**를 나눈다.
RELEASE_STATUS = "audit_current__leaderboard_unavailable"   # 릴리스 전체의 지위 (1개)
#: artifact 승인 지위 (artifact 마다 1개) — loader 가 이 어휘 밖 값을 만나면 fail-closed
APPROVAL_STATUS = ("historical", "recovered_unvalidated", "approved",
                   "superseded", "invalid", "audit_current")
#: 사용 범위 — 승인 지위와 **직교**한다 (Codex: "approved/unvalidated 와 use-scope 를 나눠라")
USE_SCOPE = ("default_visible",      # 기본 화면 노출 가능
             "archive_only",         # ?archive=1 필요
             "diagnostic_only",      # ?view=diagnostic 필요 (acquisition 용)
             "blocked")              # 어떤 경로로도 표시 금지

#: (파일, 승인지위, use_scope, 설명, 한계, source_commit, derived_from, override_reason)
ARTIFACTS = [
    ("cascade_v23_all.csv", "recovered_unvalidated", "diagnostic_only",
     "완주 원자료 (unified_dataset_273.csv 회수분)",
     ["UMA 상대값", "일부 열은 재계산 세대가 섞여 있을 수 있음"],
     PINNED_SOURCE_COMMIT, None, None),
    ("cascade_v23_champions_v2.csv", "recovered_unvalidated", "diagnostic_only",
     "champion 270행 (rank_combined==1)",
     ["champion 재선정 안 함",
      "Na2S_x100 은 B_hill 음수 — 탄성 계산 실패 행 (소비자가 걸러야 한다)"],
     PINNED_SOURCE_COMMIT, None, None),
    ("cascade_v23_litransport_v2.csv", "recovered_unvalidated", "diagnostic_only",
     "G4 정적 프록시 270행",
     ["legacy Adams-2003 BVS — 정본 softBV 아님",
      "blocking 은 4 Å foreign-center count", "min–max 정규화라 풀 상대값"],
     PINNED_SOURCE_COMMIT, None, None),
    ("oxidation_stability_cascade_v2.csv", "recovered_unvalidated", "diagnostic_only",
     "grand-potential ESW 90종 — **record-complete 90 / method-comparable 0**",
     ["phase_set_id·mp-ID·MP 스냅샷 미기록 — 재현 불가",
      "host onset 2.140 V 는 phase set 의존 (LiS4 제외 시 2.256 V)",
      "270 회수 반응 중 124건에 LiS4 가 들어 있다"],
     PINNED_SOURCE_COMMIT, None, None),
    ("cascade_v23_ranked_v2.csv", "recovered_unvalidated", "diagnostic_only",
     "합성점수 랭킹 89종 (AlI3 제외) — acquisition 전용",
     ["G4 순환 (blocking 이 BVS 를 덮어씀)", "G5 median 컷은 로스터 상대",
      "가중치 수작업", "min-max 정규화라 풀이 바뀌면 값이 바뀜"],
     NA2S_FIX_COMMIT, PINNED_SOURCE_COMMIT,
     "Na2S ductility retraction — Na2S_x100 has B_hill = -36.27 GPa (failed elastic "
     "calculation) and was averaged in, producing a false B/G = 2.50. "
     "plot_cascade_insights.py now drops non-positive Hill moduli; Na2S is B/G 1.22. "
     "Only unphysical row in 270. No audit panel reads this file."),
    ("cascade_v23_all_20260629_47species.csv", "historical", "archive_only",
     "2026-06-29 취합 경계판 (47종)", ["캠페인 커버리지 기준으로 superseded"],
     PINNED_SOURCE_COMMIT, None, None),
    ("cascade_v23_ranked.csv", "superseded", "archive_only",
     "47종 랭킹 — 역사 스냅샷", ["결과로 인용 금지", "90종 회수 이전 판"],
     PINNED_SOURCE_COMMIT, None, None),
    ("cascade_screening_funnel.json", "historical", "archive_only",
     "47종 게이트 감사", ["G3 phase set 미기록", "G4 순환", "G5 로스터 상대"],
     PINNED_SOURCE_COMMIT, None, None),
    ("cascade_screening_funnel_v2.json", "recovered_unvalidated", "diagnostic_only",
     "89종 게이트 감사", ["위와 동일 + 풀 상대 정규화 재계산됨"],
     PINNED_SOURCE_COMMIT, None, None),
    ("cascade_pool_audit_v2.json", "recovered_unvalidated", "default_visible",
     "gate 입력 ingestion 감사 (행 존재만 본다)",
     ["값의 물리성은 안 본다 — validity-aware 판정은 gate_completeness 표를 볼 것"],
     PINNED_SOURCE_COMMIT, None, None),
]

#: 5개 감사 패널 — 계약상 기본 공개가 허용된 유일한 그림
#: 2026-08-14 Codex Round-3 P1 로 **내용을 고친** 감사 CSV. 고정 커밋 산출물이 아니므로
#:  artifact 별 provenance 를 따로 싣는다 (top-level source_commit 하나로 덮으면 거짓말).
AMENDED_CSV = {
    "cascade_audit_g3_phase_set.csv":
        ("recovered 행의 synthetic phase_set_id 를 비우고 phase_set_assumption 으로 분리했다. "
         "합성 ID 를 남기면 method-complete=0 판정과 정면으로 충돌한다 — 반응식에 LiS4 가 "
         "들어 있다는 사실은 method identity 가 아니다. 그림은 host onset 두 값과 LiS4 "
         "수만 표시하므로 영향 없음."),
    "cascade_audit_g4_rescore.csv":
        ("pool_id · normalization_n · BVS pool min/max · actual_x · concentration_label 추가. "
         "min–max 점수를 고정 물성처럼 읽지 못하게 하는 메타다 — B2O3 는 historical 47 풀에서 "
         "0.1000, recovered 88 풀에서 0.1998 (둘 다 fail). 기존 값 열은 안 건드렸다."),
    "cascade_audit_gate_completeness.csv":
        ("completeness_basis 열과 G5 validity-aware 열 추가. presence 로 세면 88/1/1 이지만 "
         "비물리 탄성(B_hill·G_hill ≤ 0)을 거르면 86 / AlBr3·MgI2·Na2S / AlI3 / usable 89 다. "
         "기존 presence 수치는 그대로 두고 옆에 병기했다."),
}

FIGURES = [("campaign_status", "캠페인 현황"),
           ("g3_phase_set", "G3 phase-set 민감도"),
           ("g4_rescore", "G4 분해 — blocking 제거 재점수"),
           ("interface_axes", "계면 축 (47종 post-hoc)"),
           ("ml_validation", "ML 검증 · acquisition")]
SUPPORTING = ["cascade_audit_gate_completeness.csv"]

#: 플로터가 쓰던 계약 블록 — 이제 여기가 원본이다 (전엔 두 도구가 각자 썼다).
METRIC_CONTRACT = {
    "G3": {
        "display_name": "MP phase-set onset",
        "historical_host_onset_V": 2.140,
        "alternate_host_onset_V": 2.256,
        "rule": "compare candidate and host within the same phase_set_id",
        "record_vs_comparable": ("record-complete 90 / method-comparable 0 — 파생표가 "
                                 "phase_set_id 를 떨어뜨렸고 plain/Cl-rich 지지가 섞여 있다. "
                                 "'기록이 있다' 는 '비교 가능하다' 가 아니다."),
        "lis4_exposure": {"onset_reactions_containing_LiS4": 124, "of_records": 270},
    },
    "G4": {
        "display_name": "legacy BVS + 4A foreign-center composite",
        "blocking_definition": "fraction of Li within 4 A of atoms outside {Li,P,S,Cl}",
        "historical_rule": "blocking<0.60 ? 0.10+0.90*minmax(BVS) : 0.05",
        "circularity": ("blocking 컷 탈락자는 BVS 값이 버려지고 norm 이 0.05 로 강제된다. "
                        "컷 0.30 보다 낮으므로 blocking 탈락 = G4 탈락이 결정론적으로 따라온다. "
                        "두 독립 신호의 AND 로 읽으면 안 된다."),
        "pool_relative": ("min-max 정규화라 같은 종의 점수가 로스터에 따라 움직인다 — "
                          "B2O3 blocking-free 는 historical 47 풀에서 0.1000, "
                          "recovered 88 풀에서 0.1998 이다 (둘 다 fail)."),
        "not_equivalent_to": ["canonical BVSE", "migration barrier", "diffusivity", "conductivity"],
    },
    "G5": {
        "display_name": "UMA relaxed-ion elastic screen",
        "presence_vs_validity": ("field presence 로 세면 88/1/1 이지만, 비물리 탄성"
                                 "(B_hill·G_hill ≤ 0) 을 거르면 all-label-valid 86 · "
                                 "partial AlBr3|MgI2|Na2S · dropped AlI3 · usable 89 다."),
        "reciprocal_metric_warning": ("열 이름은 pugh 지만 값은 G/B 다. B/G 는 행별로 뒤집은 뒤 "
                                      "통계를 내야 한다 — 1/mean(G/B) ≠ mean(B/G)."),
    },
}
DATASETS = {
    "historical_47": {
        "approval_status": "historical", "use_scope": "archive_only",
        "species_count": 47, "slot_count": 141, "actual_x": 0.25,
        "pool_id": "cascade-v23-o37-f10-2026-06",
        "phase_set_id": None,
        "phase_set_assumption": "mp-gga-gga-u__lis4-included (가정 — 행 단위 기록 없음)",
        "limitations": ["historical campaign snapshot", "pool-relative ranks",
                        "not current campaign coverage"],
    },
    "recovered_90_gp": {
        "approval_status": "recovered_unvalidated", "use_scope": "diagnostic_only",
        "species_count": 90, "actual_x": 0.25,
        "pool_id": "cascade-v23-completed-90-2026-07",
        "phase_set_id": None,
        "phase_set_assumption": "mp-gga-gga-u__lis4-included (가정 — 행 단위 기록 없음)",
        "overlap_with_historical": 141, "overlap_oxidation_drift_count": 0,
        "limitations": ["not fully re-ranked or re-gated", "G3 phase-set identity absent",
                        "G4 must be rebuilt with canonical softBV"],
    },
    "current_approved_leaderboard": {
        "approval_status": "approved", "use_scope": "blocked",
        "species_count": 0,
        "limitations": ["존재하지 않는다 — 승인된 current ranking 은 0종이다"],
    },
}


def _meta(path: Path, csv_rows=False) -> dict:
    """sha256 · bytes (· 주석 제외 데이터 행수).

    ⚠ CRLF 이식성 (Codex Round-3 P1): 깨끗한 Windows checkout 에서 CSV 가 CRLF 로
    변환되면 바이트 해시가 달라진다. `.gitattributes` 로 `db/properties/*.csv|json` 을
    `eol=lf` 로 고정했고, 여기서는 **정규화 해시**도 같이 실어 둘 다로 검증할 수 있게 한다.
    """
    b = path.read_bytes()
    it = {"sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b),
          "sha256_lf": hashlib.sha256(b.replace(b"\r\n", b"\n")).hexdigest()}
    if csv_rows:
        lines = [x for x in b.decode("utf-8-sig").splitlines()
                 if x and not x.startswith("#")]
        it["rows"] = max(0, len(lines) - 1)
    return it


def build(audit: dict) -> dict:
    arts = []
    for fn, appr, scope, desc, lims, src, derived, why in ARTIFACTS:
        p = PROP / fn
        if not p.is_file():
            continue
        assert appr in APPROVAL_STATUS, f"알 수 없는 approval_status: {appr}"
        assert scope in USE_SCOPE, f"알 수 없는 use_scope: {scope}"
        a = {"artifact_id": f"cascade-v23-{p.stem}",
             "source_path": f"db/properties/{fn}",
             "approval_status": appr, "use_scope": scope, "description": desc,
             "actual_x": 0.25, "campaign_labels": ["x002", "x005", "x010"],
             "source_commit": src, "limitations": lims, **_meta(p, csv_rows=fn.endswith(".csv"))}
        if derived:
            a["derived_from"] = derived
            a["override_reason"] = why
        arts.append(a)

    figs = []
    for name, title in FIGURES:
        img, tab = FIGD / f"cascade_audit_{name}.png", PROP / f"cascade_audit_{name}.csv"
        if not (img.is_file() and tab.is_file()):
            continue
        im, tb = _meta(img), _meta(tab, csv_rows=True)
        fig = {"panel": name, "title": title,
               "image": f"docs/figures/cascade/{img.name}",
               "csv": f"db/properties/{tab.name}",
               "approval_status": "audit_current", "use_scope": "default_visible",
               "source_commit": PINNED_SOURCE_COMMIT}
        if tab.name in AMENDED_CSV:
            fig["csv_source_commit"] = "working tree (2026-08-14 amendment)"
            fig["csv_derived_from"] = PINNED_SOURCE_COMMIT
            fig["csv_override_reason"] = AMENDED_CSV[tab.name]
        figs.append({**fig,
                     "image_sha256": im["sha256"], "image_bytes": im["bytes"],
                     "csv_sha256": tb["sha256"], "csv_bytes": tb["bytes"], "csv_rows": tb["rows"]})

    sup = []
    for fn in SUPPORTING:
        p = PROP / fn
        if p.is_file():
            it = {"path": f"db/properties/{fn}",
                  "approval_status": "audit_current", "use_scope": "default_visible",
                  "source_commit": PINNED_SOURCE_COMMIT, **_meta(p, csv_rows=True)}
            if fn in AMENDED_CSV:
                it["source_commit"] = "working tree (2026-08-14 amendment)"
                it["derived_from"] = PINNED_SOURCE_COMMIT
                it["override_reason"] = AMENDED_CSV[fn]
            sup.append(it)

    return {
        "property": "cascade_audit_manifest",
        "schema_version": 2,
        "artifact_id": "cascade-audit-2026-08-14",
        "owner": "tools/cascade/build_cascade_audit_manifest.py",
        "owner_note": ("이 파일의 writer 는 위 도구 **하나뿐**이다. plot_cascade_audit_2026_08.py 와 "
                       "rebuild_pool_inputs.py 는 sidecar 만 쓴다 (Codex Round-3 P0-1)."),
        "status": RELEASE_STATUS,
        "source_commit": PINNED_SOURCE_COMMIT,
        "source_commit_note": ("패널 고정 커밋. **artifact 마다 자기 source_commit 이 있고 "
                               "그쪽이 우선한다** — ranked_v2 는 Na₂S 정정 이후 산출물이다."),
        "source_of_truth": "docs/reviews/cascade_dftweb_source_of_truth_2026_08_14.md",
        "approval_status_vocabulary": list(APPROVAL_STATUS),
        "use_scope_vocabulary": list(USE_SCOPE),
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
        "datasets": DATASETS,
        "metric_contract": METRIC_CONTRACT,
        "artifacts": arts,
        "figures": figs,
        "supporting_tables": sup,
    }


def check(man: dict) -> list:
    """원장이 실제 파일과 맞는지. 반환값이 비어 있어야 통과."""
    bad = []
    for a in man.get("artifacts", []) + man.get("supporting_tables", []):
        rel = a.get("source_path") or a.get("path")
        p = ROOT / rel
        if not p.is_file():
            bad.append(f"{rel}: 파일 없음"); continue
        m = _meta(p)
        if m["sha256"] != a.get("sha256") and m["sha256_lf"] != a.get("sha256_lf"):
            bad.append(f"{rel}: 해시 불일치 (원문·LF정규화 둘 다)")
        if a.get("approval_status") not in APPROVAL_STATUS:
            bad.append(f"{rel}: 알 수 없는 approval_status {a.get('approval_status')!r}")
        if a.get("use_scope") not in USE_SCOPE:
            bad.append(f"{rel}: 알 수 없는 use_scope {a.get('use_scope')!r}")
    for f in man.get("figures", []):
        for key, hk in (("image", "image_sha256"), ("csv", "csv_sha256")):
            p = ROOT / f[key]
            if not p.is_file():
                bad.append(f"{f[key]}: 파일 없음"); continue
            if _meta(p)["sha256"] != f[hk]:
                bad.append(f"{f[key]}: 해시 불일치")
    if len(man.get("figures", [])) != 5:
        bad.append(f"감사 패널이 {len(man.get('figures', []))}개다 — 정확히 5개여야 한다")
    return bad


def selftest() -> int:
    ok = True

    def chk(name, cond):
        nonlocal ok
        ok &= bool(cond)
        print(f"  {'✓' if cond else '✗'} {name}")

    # 양성
    audit = json.loads((PROP / "cascade_pool_audit_v2.json").read_text(encoding="utf-8"))
    man = build(audit)
    chk("빌드가 5개 패널을 싣는다", len(man["figures"]) == 5)
    chk("플로터 계약 블록이 전부 있다",
        all(k in man for k in ("datasets", "metric_contract", "artifacts",
                               "figures", "supporting_tables")))
    chk("headline 키가 플로터가 대조하는 6개다",
        set(man["headline"]) == {"planned_slots", "completed_slots", "completed_species",
                                 "historical_snapshot_species",
                                 "approved_current_leaderboard_species",
                                 "explicit_pair_property_labels"})
    rk = [a for a in man["artifacts"] if a["source_path"].endswith("ranked_v2.csv")][0]
    chk("ranked_v2 에 자기 source_commit 이 있다", rk["source_commit"] == NA2S_FIX_COMMIT)
    chk("ranked_v2 에 derived_from·override_reason 이 있다",
        rk.get("derived_from") == PINNED_SOURCE_COMMIT and rk.get("override_reason"))
    chk("승인된 current ranking 은 0", man["headline"]["approved_current_leaderboard_species"] == 0)
    chk("정상 원장은 check 를 통과한다", check(man) == [])

    # ── 음성 (틀린 입력을 잡아내는지) ──
    bad = json.loads(json.dumps(man))
    bad["artifacts"][0]["sha256"] = "0" * 64
    bad["artifacts"][0]["sha256_lf"] = "0" * 64
    chk("[음성] 해시 위조를 잡는다", any("해시" in x for x in check(bad)))

    bad2 = json.loads(json.dumps(man))
    bad2["artifacts"][0]["approval_status"] = "approved_by_nobody"
    chk("[음성] 어휘 밖 approval_status 를 잡는다",
        any("approval_status" in x for x in check(bad2)))

    bad3 = json.loads(json.dumps(man))
    bad3["artifacts"][0]["use_scope"] = "everyone_can_see_it"
    chk("[음성] 어휘 밖 use_scope 를 잡는다", any("use_scope" in x for x in check(bad3)))

    bad4 = json.loads(json.dumps(man))
    bad4["figures"] = bad4["figures"][:3]
    chk("[음성] 패널이 5개가 아니면 잡는다", any("패널" in x for x in check(bad4)))

    bad5 = json.loads(json.dumps(man))
    bad5["figures"][0]["image_sha256"] = "0" * 64
    chk("[음성] 그림 해시 위조를 잡는다", any("해시" in x for x in check(bad5)))

    # CRLF 이식성: LF 정규화 해시로도 통과해야 한다
    crlf = json.loads(json.dumps(man))
    p = ROOT / crlf["artifacts"][0]["source_path"]
    if p.suffix == ".csv":
        crlf["artifacts"][0]["sha256"] = hashlib.sha256(
            p.read_bytes().replace(b"\n", b"\r\n")).hexdigest()
        chk("[CRLF] 원문 해시가 달라도 LF 정규화로 통과한다", check(crlf) == [])

    print("selftest", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="쓰지 않고 기존 원장만 검증")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.check:
        if not OUT.is_file():
            print(f"⛔ 원장이 없다: {OUT}"); return 1
        bad = check(json.loads(OUT.read_text(encoding="utf-8")))
        print("\n".join(f"  ⛔ {b}" for b in bad) if bad else "  ✓ 원장이 파일과 일치한다")
        return 1 if bad else 0

    audit_p = PROP / "cascade_pool_audit_v2.json"
    if not audit_p.is_file():
        print("⛔ cascade_pool_audit_v2.json 이 없다 — rebuild_pool_inputs.py 를 먼저 돌릴 것")
        return 1
    man = build(json.loads(audit_p.read_text(encoding="utf-8")))
    bad = check(man)
    if bad:
        print("⛔ 빌드 직후 검증 실패 (쓰지 않는다):")
        print("\n".join(f"   {b}" for b in bad))
        return 1
    OUT.write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[manifest] {OUT}")
    print(f"           artifact {len(man['artifacts'])} · 패널 {len(man['figures'])} · "
          f"supporting {len(man['supporting_tables'])} · 승인 ranking "
          f"{man['headline']['approved_current_leaderboard_species']}종")
    return 0


if __name__ == "__main__":
    sys.exit(main())
