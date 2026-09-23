"""The paper records the audit cites (ADR 0042).

A citation that does not resolve is worse than none: it looks checked.  So
every id the code mentions must be in the files, every quote must be short
and belong to a record the code actually cites (the repository is public),
and the numbers the code uses must be the numbers the record holds.
"""

import pathlib
import re

import pytest

from wrdkit.eis import knowledge
from wrdkit.eis.audit import REFERENCES
from wrdkit.eis.capacitance import PROCESSES, process

SOURCE_TREE = pathlib.Path(knowledge.__file__).resolve().parents[1]
ID = re.compile(r"\b([A-Z][A-Z0-9_]*\d{4}(?:_[A-Z]+)?\.[a-z0-9][a-z0-9-]*[a-z0-9])\b")
KINDS = {"definition", "formula", "criterion", "range", "model", "procedure",
         "caveat", "example"}


def cited_in_source() -> set[str]:
    found: set[str] = set()
    for path in SOURCE_TREE.rglob("*.py"):
        found.update(ID.findall(path.read_text(encoding="utf-8")))
    return found


def test_every_paper_and_record_loads():
    sources = knowledge.sources()
    assert set(sources) == {"ISW1990", "HIRSCHORN2010", "SCHOENLEBER2014",
                            "VADHVA2021", "LASIA1999", "ECSIF2019_BIOLOGIC",
                            "GUPTA2019"}
    records = knowledge.records()
    assert len(records) >= 190
    for one in records.values():
        assert one.source in sources, one.id
        assert one.id.startswith(one.source + "."), one.id
        assert one.kind in KINDS, one.id
        assert one.claim_ko and one.claim, one.id
        assert one.page, one.id


def test_every_finding_cites_records_that_exist():
    for code, ids in REFERENCES.items():
        assert ids, code
        for record_id in ids:
            knowledge.record(record_id)              # KeyError 면 실패


def test_every_id_written_in_the_code_exists():
    """docstring 에 적은 id 에 오타가 있으면 그 인용은 아무것도 가리키지 않는다."""
    known_sources = set(knowledge.sources())
    for record_id in cited_in_source():
        if record_id.split(".")[0] in known_sources:
            knowledge.record(record_id)


def test_quotes_are_short_and_only_where_the_code_cites():
    """저장소는 공개다 — 원문은 코드가 인용하는 기록에만, 25 단어까지."""
    cited = cited_in_source()
    for one in knowledge.records().values():
        if one.quote:
            assert len(one.quote.split()) <= 25, one.id
            assert one.id in cited, f"{one.id} 는 인용되지 않는데 원문을 싣고 있다"
    for record_id in cited:
        if record_id.split(".")[0] in knowledge.sources():
            assert knowledge.record(record_id).quote, f"{record_id} 에 원문이 없다"


def test_a_citation_names_the_paper_page_and_place():
    assert knowledge.cite("ISW1990.bulk-arc-off-scale") == (
        "Irvine–Sinclair–West 1990, p. 135 (Sect. 2.2; Fig. 4b,c)")
    with pytest.raises(KeyError):
        knowledge.cite("ISW1990.no-such-record")


def test_the_capacitance_table_is_the_papers_table():
    """`capacitance.PROCESSES` 의 경계가 Irvine–Sinclair–West 표 1 의 수다.
    표의 겹치는 범위는 다음 행이 시작하는 곳에서 자른다 (벌크 10⁻¹² 는 입계가
    시작하는 10⁻¹¹ 까지)."""
    rows = {row["label"]: row for row in
            knowledge.record("ISW1990.table1-capacitance-interpretation").values}
    assert rows["bulk"]["value"] == 1e-12 < process("bulk").high
    assert (rows["grain boundary"]["low"], rows["grain boundary"]["high"]) == (
        process("grain_boundary").low, process("grain_boundary").high)
    assert (rows["surface layer"]["low"], rows["surface layer"]["high"]) == (
        process("surface_layer").low, process("surface_layer").high)
    assert (rows["sample-electrode interface"]["low"],
            rows["sample-electrode interface"]["high"]) == (
        process("interface").low, process("interface").high)
    assert process("reaction").low <= rows["electrochemical reactions"]["value"]
    # 우리 표에 없는 두 행 — 그 이유는 ADR 0042 에 있다.
    assert {"minor, second phase", "bulk ferroelectric"} <= set(rows)
    assert len(PROCESSES) == 5


def test_search_by_topic_and_text():
    kk = knowledge.search(topic="kramers-kronig")
    assert {one.source for one in kk} >= {"SCHOENLEBER2014", "LASIA1999", "VADHVA2021"}
    assert knowledge.search(text="R_SE,bulk", source="VADHVA2021")
    assert knowledge.search(topic="kramers-kronig", source="ISW1990") == []
