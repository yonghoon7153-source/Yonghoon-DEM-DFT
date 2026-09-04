import json
from pathlib import Path

import pytest

from research_agent.config import load_config
from research_agent.db import PaperDB
from research_agent.journals import JournalTable
from research_agent.models import Paper, paper_id_from
from research_agent.sources.scholar_email import parse_alert
from research_agent.triage import TriageConfig, apply_triage, rank, rule_relevance

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "tests" / "fixtures" / "scholar_alert_sample.html"


@pytest.fixture
def cfg():
    return load_config(ROOT)


def test_journal_lookup(cfg):
    jt = JournalTable(cfg.load_journal_table())
    assert jt.lookup("Nature Communications").impact_factor > 10
    assert jt.lookup("Nat. Commun.").canonical == "Nature Communications"
    assert jt.lookup("… Energy Storage Materials").canonical == "Energy Storage Materials"
    assert jt.lookup("arXiv preprint arXiv:2609.01234").is_preprint
    assert jt.lookup("Some Unknown Journal").matched_by == "default"


def test_rule_relevance_orders_dem_over_supercap():
    dem = Paper(id="a", title="DEM simulation of Li6PS5Cl composite cathode compaction", snippet="discrete element method porosity percolation")
    sc = Paper(id="b", title="Porosity in energy storage materials", snippet="porous carbons for supercapacitor electrodes battery")
    assert rule_relevance(dem)[0] > 0.6
    assert rule_relevance(sc)[0] < 0.35


def test_triage_if_first_ordering(cfg):
    jt = JournalTable(cfg.load_journal_table())
    tc = TriageConfig(tiers=cfg.get("triage.tiers"))
    _, papers = parse_alert("새로운 결과 - dem battery", FIX.read_text(encoding="utf-8"), None, "m1")
    for p in papers:
        apply_triage(p, jt, tc)
    ranked = rank([p for p in papers if p.status != "rejected"])
    # Nature Communications (IF~15.7) must come before Advanced Powder Technology (IF~4.2) before arXiv (IF 0)
    assert ranked[0].journal_canonical == "Nature Communications" and ranked[0].tier == "A"
    assert ranked[1].journal_canonical == "Advanced Powder Technology"
    assert ranked[-1].is_preprint
    rejected = [p for p in papers if p.status == "rejected"]
    assert len(rejected) == 1 and "Porosity in electrochemical" in rejected[0].title


def test_db_upsert_idempotent(tmp_path, cfg):
    db = PaperDB(tmp_path / "t.sqlite", tmp_path / "t.jsonl")
    p = Paper(id=paper_id_from("A Title"), title="A Title", keywords_matched=["dem battery"], venue="Nature")
    _, new1 = db.upsert(p)
    q = Paper(id=paper_id_from("a title"), title="a title", keywords_matched=["dft battery"], doi="10.1/x")
    stored, new2 = db.upsert(q)
    assert new1 and not new2
    assert set(stored.keywords_matched) == {"dem battery", "dft battery"}
    assert stored.doi == "10.1/x" and stored.venue == "Nature"
    assert db.counts()["total"] == 1
    db.export_jsonl()
    assert len((tmp_path / "t.jsonl").read_text().splitlines()) == 1


# ---------------------------------------------------------------------------
# 캠페인 용어 (2026-09-04) — `db/`·`kb/` 전수조사로 드러난 축 B 캠페인 ④⑤⑧⑨⑪ 이
# `_TERMS` 에 한 낱말도 없었다. 양성 + **음성** 을 같이 박아 둔다.
# ---------------------------------------------------------------------------

def test_campaign_papers_are_no_longer_missed():
    """④⑤⑧⑨ — 이 넷은 예전 표에서 배터리 일반(0.05)까지만 긁혔다."""
    cases = {
        "④cascade": Paper(
            id="c4", title="Grand-potential electrochemical stability window of argyrodite solid electrolytes",
            snippet="decomposition reaction and oxidation limit from Materials Project convex hull"),
        "⑤doping": Paper(
            id="c5", title="High-throughput screening of dopants for sulfide solid electrolytes",
            snippet="descriptor-based screening funnel, formation energy and band gap gates"),
        "⑧Li3N": Paper(
            id="c8", title="Li adatom surface diffusion on Li3N(001) from first-principles NEB",
            snippet="migration barrier of lithium nitride anode interphase"),
        "⑨hBN": Paper(
            id="c9", title="Li intercalation in h-BN galleries on carbon fiber",
            snippet="nudged elastic band interlayer binding energy VGCF"),
    }
    for name, p in cases.items():
        assert rule_relevance(p)[0] >= 0.45, (name, rule_relevance(p))


def test_zn_rescue_is_narrow_not_a_blanket_pardon():
    """⑪ — Cu–Zn **상동정**만 살린다. 일반 zinc-ion 은 감점 그대로여야 한다."""
    cu_zn = Paper(id="z1", title="Rietveld phase identification of Cu-Zn intermetallics",
                  snippet="XRD pattern overlap of brass phases, convex hull from DFT")
    zn_generic = Paper(id="z2", title="A high-rate zinc-ion battery cathode",
                       snippet="aqueous zinc-ion electrolyte and electrode cycling")
    assert rule_relevance(cu_zn)[0] >= 0.35
    # ⛔음성: 일반 zinc-ion 은 상쇄 없이 여전히 탈락
    assert rule_relevance(zn_generic)[0] < 0.35


def test_campaign_terms_alone_do_not_pass_threshold():
    """⛔음성: campaign 줄은 **보조**다. 방법도 재료계도 없이 통과시키면 안 된다."""
    weak = Paper(id="w1", title="Band gap and formation energy of a hypothetical oxide",
                 snippet="convex hull and Arrhenius fit of an unrelated semiconductor")
    assert rule_relevance(weak)[0] < 0.35


def test_zinc_ion_paper_mentioning_rietveld_still_fails():
    """⛔음성: 감점 상쇄가 **말 한 마디로** 뚫리면 안 된다."""
    p = Paper(id="z3", title="Rietveld analysis of a zinc-ion battery cathode",
              snippet="aqueous zinc-ion electrode cycling and capacity retention")
    assert rule_relevance(p)[0] < 0.35
