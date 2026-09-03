from pathlib import Path

from research_agent.sources.scholar_email import (doi_from_url, keyword_from_subject, parse_alert,
                                                   parse_alert_html, unwrap_scholar_url)

FIX = Path(__file__).parent / "fixtures" / "scholar_alert_sample.html"


def test_keyword_from_subject_variants():
    assert keyword_from_subject("새로운 결과 - dem battery") == "dem battery"
    assert keyword_from_subject("New results for dft battery") == "dft battery"
    assert keyword_from_subject("Google Scholar Alert - [ anode-less assb ]") == "anode-less assb"
    assert keyword_from_subject('"dem battery" - new results') == "dem battery"


def test_unwrap_and_doi():
    u = unwrap_scholar_url("https://scholar.google.com/scholar_url?url=https://www.nature.com/articles/s41467-026-71305-2&hl=ko&sa=X")
    assert u == "https://www.nature.com/articles/s41467-026-71305-2"
    assert doi_from_url("https://doi.org/10.1002/adma.202513090") == "10.1002/adma.202513090"
    assert doi_from_url("https://onlinelibrary.wiley.com/doi/10.1002/anie.202523225/full") == "10.1002/anie.202523225"
    assert doi_from_url("https://www.nature.com/articles/s41467-026-71305-2") is None


def test_parse_alert_html_fixture():
    hits = parse_alert_html(FIX.read_text(encoding="utf-8"))
    assert len(hits) == 4
    h0 = hits[0]
    assert h0.title.startswith("Mechanofusion-derived cathode composite")
    assert h0.url == "https://www.nature.com/articles/s41467-026-71305-2"
    assert h0.authors[0] == "M Kissel" and h0.venue == "Nature Communications" and h0.year == 2026
    assert "discrete element method" in h0.snippet
    arxiv = hits[3]
    assert "arXiv" in arxiv.venue and arxiv.year == 2026


def test_parse_alert_to_papers():
    kw, papers = parse_alert("새로운 결과 - dem battery", FIX.read_text(encoding="utf-8"), None, "<msg1@google.com>")
    assert kw == "dem battery"
    assert all(p.keywords_matched == ["dem battery"] for p in papers)
    assert papers[0].first_author == "Kissel"
    assert papers[0].id.startswith("t:")
