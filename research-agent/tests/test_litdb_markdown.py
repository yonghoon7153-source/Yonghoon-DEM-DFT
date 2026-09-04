"""litdb markdown 어댑터 — 양성 + **음성** 경로.

음성이 핵심이다: 이 어댑터는 사용자의 실물 서랍(`litdb/papers/`)에 쓰기 때문에
① 기존 카드를 덮어쓰면 안 되고 ② INDEX 를 자동으로 건드리면 안 되고
③ 실물 없이 채운 칸을 `✅` 로 찍으면 안 된다.
"""
from __future__ import annotations

import json

from research_agent.config import Config
from research_agent.exporters.litdb import _slug, export_markdown
from research_agent.models import Paper


def _cfg(tmp_path):
    return Config(tmp_path, {"litdb": {"enabled": True, "mode": "markdown",
                                       "markdown_dir": "litdb/papers"}})


def _paper(**kw):
    d = dict(id="x1", title="Resistor network models for solid-state composites",
             authors=["Lukas Ketter", "Wolfgang G. Zeier"], year=2025,
             doi="10.1038/s41467-025-56514-5", venue="Nature Communications",
             status="digested", tier="A", relevance=0.95, journal_if=15.7)
    d.update(kw)
    return Paper(**{k: v for k, v in d.items() if k in Paper.__dataclass_fields__})


def test_slug_follows_existing_convention():
    p = _paper()
    assert _slug(p) == "ketter2025_resistor_network_models_solid_state_composites"
    # 저자 없음 · 연도 없음 도 죽지 않는다
    assert _slug(_paper(authors=[], year=None)).startswith("unknown")


def test_writes_skeleton_not_a_finished_digest(tmp_path):
    cfg = _cfg(tmp_path)
    res = export_markdown(cfg, [_paper()])
    assert res["written"] == ["ketter2025_resistor_network_models_solid_state_composites"]
    md = (tmp_path / "litdb" / "papers" / (res["written"][0] + ".md")).read_text(encoding="utf-8")
    # ⛔음성: 실물을 안 읽었는데 완료 표시를 하면 안 된다
    assert "status `✅`" not in md
    assert "🌱 skeleton" in md
    # 실물이 필요한 칸이 **명시**돼야 한다
    for section in ("## 3. 핵심 물성", "## 4. 방법", "## 5. Figure set", "## 7. 우리 대비"):
        assert section in md
    assert md.count("⏳ 문서 대기") >= 4
    # 우리 규율이 비판 포인트로 박혀 있어야 한다
    assert "frame[4]" in md and "DOS-threshold" in md


def test_never_overwrites_existing_card(tmp_path):
    cfg = _cfg(tmp_path)
    d = tmp_path / "litdb" / "papers"
    d.mkdir(parents=True)
    slug = "ketter2025_resistor_network_models_solid_state_composites"
    (d / f"{slug}.md").write_text("사람이 쓴 원본 — 건드리면 안 된다", encoding="utf-8")
    res = export_markdown(cfg, [_paper()])
    assert res["written"] == []
    assert res["skipped"] and res["skipped"][0]["why"] == "slug 중복"
    assert (d / f"{slug}.md").read_text(encoding="utf-8") == "사람이 쓴 원본 — 건드리면 안 된다"


def test_dedupe_by_doi_even_when_slug_differs(tmp_path):
    """제목이 달라 slug 가 달라져도 **DOI 가 같으면** 새로 만들지 않는다.

    실측 사고 대응: 같은 논문을 두 세션이 각자 digest 한 전례가 있다 (ECER-D-26-00097).
    """
    cfg = _cfg(tmp_path)
    d = tmp_path / "litdb" / "papers"
    d.mkdir(parents=True)
    (d / "zeier2025_totally_different_title.md").write_text(
        "> slug `zeier2025_totally_different_title` · DOI `10.1038/s41467-025-56514-5`",
        encoding="utf-8")
    res = export_markdown(cfg, [_paper()])
    assert res["written"] == []
    assert res["skipped"][0]["why"] == "DOI 중복"
    assert res["skipped"][0]["existing"] == "zeier2025_totally_different_title"


def test_index_is_not_touched_only_proposed(tmp_path):
    """⛔음성: INDEX.md 는 손으로 쓴 분석 산문이다 — 자동으로 건드리지 않는다."""
    cfg = _cfg(tmp_path)
    d = tmp_path / "litdb" / "papers"
    d.mkdir(parents=True)
    idx = tmp_path / "litdb" / "INDEX.md"
    idx.write_text("# 원본 INDEX\n", encoding="utf-8")
    res = export_markdown(cfg, [_paper()])
    assert idx.read_text(encoding="utf-8") == "# 원본 INDEX\n"      # 그대로
    assert res["index_proposals"] == 1
    prop = (tmp_path / "litdb" / "_INDEX_proposals.md").read_text(encoding="utf-8")
    assert "사람이 한다" in prop and "ketter2025" in prop


def test_rejected_papers_are_not_written(tmp_path):
    cfg = _cfg(tmp_path)
    res = export_markdown(cfg, [_paper(status="rejected")])
    assert res["written"] == []
