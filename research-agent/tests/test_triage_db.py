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
