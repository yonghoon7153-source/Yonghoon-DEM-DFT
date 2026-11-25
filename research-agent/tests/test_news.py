"""`[RA-NEWS]` 주간 뉴스 아카이브 수신 (v0.1.12).

메일은 9/11 17:00 KST 부터 온다. 그때 처음 돌아 보는 코드라 **음성 경로가 대부분**이다 —
"잘 되면 이렇게 된다"는 실물이 오면 알게 되지만, 조용히 망가지는 쪽은 지금 잠가야 한다.

    python -m pytest tests/test_news.py -q

⛔ 이 파일이 보증하지 못하는 것
  · IMAP 경로 전체. `sync_news_from_mail` 의 메일 걷기는 안 탄다 — 여기서 보는 것은
    **payload 하나가 들어왔을 때** 무슨 일이 나는가다. 메일 파싱은
    `test_payloads_from_message_*` 가 순수 함수로 따로 본다.
  · Cowork 가 보내는 payload 가 실제로 이 스키마인지. 그건 첫 메일이 와야 안다.
  · 뉴스 내용의 사실 여부 (검증 대상이 아니다 — 보관 대상이다).
"""
import email
import json
import shutil
from pathlib import Path

import pytest

from research_agent import news as nw
from research_agent.config import load_config
from research_agent.db import PaperDB
from research_agent.handoff import payloads_from_message

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    for d in ("config", "prompts", "templates"):
        shutil.copytree(ROOT / d, tmp_path / d)
    (tmp_path / "vault").mkdir()
    monkeypatch.setenv("RA_ROOT", str(tmp_path))
    return load_config(tmp_path)


def _item(i=1, **kw):
    d = dict(headline=f"LG엔솔, 전고체 파일럿 라인 {i}", date="2026-09-08",
             summary=f"요약 {i}", source=f"https://example.com/news/{i}",
             body_markdown=f"본문 {i}\n\n- 항목", notion_url=f"https://notion.so/{i}",
             axes=["축 A · DEM/MPM"], scooping=False, scooping_why="")
    d.update(kw)
    return d


def _payload(n=3, **kw):
    d = dict(protocol=nw.PROTOCOL, origin="cowork-cloud", created_at="2026-09-11T08:00:00+00:00",
             week={"start": "2026-09-05", "end": "2026-09-11", "label": "9월 2주"},
             issue=2, items=[_item(i) for i in range(1, n + 1)],
             weekly_markdown="## 이번 주\n- 골라낸 3건", notes="")
    d.update(kw)
    return d


# --------------------------------------------------------------------- 프로토콜 분리
def test_a_handoff_payload_is_refused(cfg):
    """⛔음성: 논문 payload 가 뉴스로 들어가면 안 된다.

    이게 이 모듈의 존재 이유다. subject·protocol 을 나눈 것은 뉴스 메일이 논문 경로로
    새어 `papers=0` 으로 **조용히 소비**되는 걸 막기 위해서인데, 반대 방향도 같이 막아야
    대칭이 성립한다. 던지지 않고 받아 적으면 `News/` 에 논문 payload 가 노트로 남는다.
    """
    with pytest.raises(ValueError):
        nw.import_news(cfg, {"protocol": "ra-handoff/1", "papers": [], "week": {"end": "2026-09-11"}})
    assert not (nw.news_dir(cfg)).exists() or not list(nw.news_dir(cfg).glob("*.md")), \
        "거부했는데 노트가 남았다"


def test_a_week_without_a_readable_date_is_refused(cfg):
    """⛔음성: 날짜를 못 읽으면 `News/None.md` 를 만들지 않는다.

    한 번 생기면 그 다음 주 수신이 같은 파일을 덮어쓰며 **여러 주가 한 파일에 뭉개진다.**
    조용히 섞이느니 그 주만 거부하고 메일은 다시 걷을 수 있게 둔다.
    """
    for bad in ({"end": "지난주"}, {}, {"end": "2026/09/11"}):
        with pytest.raises(ValueError):
            nw.import_news(cfg, _payload(week=bad, created_at="언젠가"))
    assert not list(nw.news_dir(cfg).glob("*.md")) if nw.news_dir(cfg).exists() else True


def test_one_bad_week_does_not_block_the_others(cfg):
    """날짜가 깨진 주 하나가 그 메일의 나머지 payload 를 막으면 안 된다."""
    good, bad = _payload(2), _payload(2, week={"end": "언젠가"}, created_at="x")
    with pytest.raises(ValueError):
        nw.import_news(cfg, bad)
    res = nw.import_news(cfg, good)
    assert res["written"], "앞 payload 가 죽었다고 뒤 payload 를 못 쓰면 그 주가 통째로 유실된다"


# --------------------------------------------------------------------- 축소 덮어쓰기
def test_a_smaller_week_does_not_overwrite(cfg):
    """⛔음성: 같은 주가 **더 적은 항목**으로 다시 오면 덮어쓰지 않는다.

    재생성이 합법적으로 줄어들 수 있고(수집 창이 움직였다 · Notion 행이 지워졌다),
    그걸로 덮으면 되돌릴 수 없다. 09-04 사고와 같은 계열이라 같은 처방을 쓴다.
    """
    nw.import_news(cfg, _payload(7))
    note = nw.news_dir(cfg) / "2026-09-11.md"
    assert "n_items: 7" in note.read_text(encoding="utf-8")

    res = nw.import_news(cfg, _payload(3))
    assert res["written"] is False
    assert "7건" in res["why"] and "3건" in res["why"], f"이유가 숫자를 안 말한다: {res['why']}"
    assert "n_items: 7" in note.read_text(encoding="utf-8"), "7건짜리가 3건으로 덮였다"
    assert not (nw.news_dir(cfg) / ".backup").exists(), \
        "안 썼는데 백업이 생겼다 — 안 쓴 게 아니라 쓰고 되돌린 것이다"


def test_force_overwrites_but_keeps_a_backup(cfg):
    nw.import_news(cfg, _payload(7))
    res = nw.import_news(cfg, _payload(3), force=True)
    assert res["written"] and res["backup"]
    assert "n_items: 7" in Path(res["backup"]).read_text(encoding="utf-8"), "백업이 옛 내용이 아니다"


def test_a_bigger_week_replaces_it(cfg):
    """줄면 막지만 늘면 받는다 — 막기만 하면 갱신이 영영 안 된다."""
    nw.import_news(cfg, _payload(3))
    res = nw.import_news(cfg, _payload(9))
    assert res["written"] and res["backup"]
    assert "n_items: 9" in (nw.news_dir(cfg) / "2026-09-11.md").read_text(encoding="utf-8")


def test_reimporting_the_same_week_is_idempotent(cfg):
    a = nw.import_news(cfg, _payload(4))
    b = nw.import_news(cfg, _payload(4))
    assert b["written"] and b["backup"] is None, "내용이 같은데 백업이 쌓인다"
    assert b["jsonl_added"] == 0, f"같은 항목이 jsonl 에 또 들어갔다 (+{b['jsonl_added']})"
    assert a["jsonl_added"] == 4


# --------------------------------------------------------------------- jsonl
def test_jsonl_dedups_by_source_url(cfg):
    nw.import_news(cfg, _payload(3))
    nw.import_news(cfg, _payload(5, week={"start": "2026-09-12", "end": "2026-09-18"}))
    rows = [json.loads(l) for l in nw.news_jsonl(cfg).read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(rows) == 5, f"3 + (5 중 새 2) = 5 여야 하는데 {len(rows)}"
    assert len({r["source"] for r in rows}) == 5


def test_items_without_a_source_are_not_dropped(cfg):
    """⛔음성: 중복 키가 없다고 항목을 버리면 안 된다.

    `source` 는 있을 법하지만 없을 수도 있다(Notion 행에 URL 을 안 적은 경우).
    그때 조용히 사라지면 **메일에서 잘린 걸 보관한다**는 이 층의 목적 자체가 무너진다.
    """
    items = [_item(1, source="", notion_url=""), _item(2, source="", notion_url=""),
             _item(3, source="", notion_url="", headline="LG엔솔, 전고체 파일럿 라인 1")]
    res = nw.import_news(cfg, _payload(items=items))
    rows = [json.loads(l) for l in nw.news_jsonl(cfg).read_text(encoding="utf-8").splitlines() if l.strip()]
    assert res["n_items"] == 3
    assert len(rows) == 2, "headline|date 로 떨어지므로 1·3 은 같은 것으로 본다 — 그래도 2건은 남아야 한다"
    body = (nw.news_dir(cfg) / "2026-09-11.md").read_text(encoding="utf-8")
    assert body.count("### ") == 3, "노트에는 세 건 다 있어야 한다 (jsonl 중복 제거와 별개다)"


def test_a_corrupt_jsonl_line_does_not_stop_the_load(cfg):
    jp = nw.news_jsonl(cfg)
    jp.parent.mkdir(parents=True, exist_ok=True)
    jp.write_text("{망가진 줄\n", encoding="utf-8")
    res = nw.import_news(cfg, _payload(2))
    assert res["jsonl_added"] == 2


# --------------------------------------------------------------------- 렌더
def test_scooping_items_are_surfaced(cfg):
    """선점 경보가 본문에 안 보이면 이 아카이브의 실용 가치가 절반 사라진다."""
    items = [_item(1), _item(2, scooping=True, scooping_why="우리 축 A 와 같은 계"), _item(3)]
    nw.import_news(cfg, _payload(items=items))
    body = (nw.news_dir(cfg) / "2026-09-11.md").read_text(encoding="utf-8")
    assert "n_scooping: 1" in body
    assert "선점 주의" in body and "우리 축 A 와 같은 계" in body


def test_we_do_not_create_wikilinks(cfg):
    """⛔음성: 우리 골격이 `[[ ]]` 를 만들지 않는다 (v0.1.12 결정).

    잘못 걸린 링크가 Obsidian 그래프를 더럽히는 쪽이 링크가 없는 것보다 나쁘다.
    보낸 쪽 본문에 원래 `[[` 가 있으면 그건 **내용**이라 그대로 두되 세어서 알려준다 —
    내용을 말없이 고치지 않는다.
    """
    res = nw.import_news(cfg, _payload(3))
    assert res["wikilinks_passed_through"] == 0
    body = (nw.news_dir(cfg) / "2026-09-11.md").read_text(encoding="utf-8")
    assert "[[" not in body

    res2 = nw.import_news(cfg, _payload(3, week={"end": "2026-09-18"},
                                        items=[_item(1, body_markdown="원문에 [[Some Note]] 가 있다")]))
    assert res2["wikilinks_passed_through"] == 1, "보낸 쪽 링크를 세지 않으면 오염을 못 본다"
    assert "[[Some Note]]" in (nw.news_dir(cfg) / "2026-09-18.md").read_text(encoding="utf-8"), \
        "내용을 말없이 고쳤다"


def test_headline_with_yaml_metacharacters_stays_parseable(cfg):
    """⛔음성: 헤드라인의 `:` · 따옴표가 frontmatter 를 깨면 안 된다."""
    nw.import_news(cfg, _payload(items=[_item(1, headline='삼성SDI: "전고체" 2027년 — 왜?', axes=['축 "A"'])]))
    body = (nw.news_dir(cfg) / "2026-09-11.md").read_text(encoding="utf-8")
    fm = body.split("---")[1]
    assert "n_items: 1" in fm
    assert '삼성SDI: "전고체"' in body
    import re
    for line in fm.strip().splitlines():
        assert re.match(r"^[a-z_]+: ", line), f"frontmatter 줄이 깨졌다: {line!r}"


def test_an_empty_week_still_writes_a_note(cfg):
    """0건인 주도 기록한다 — "그 주엔 아무것도 없었다"와 "안 걷었다"는 다르다."""
    res = nw.import_news(cfg, _payload(0))
    assert res["written"]
    assert "n_items: 0" in (nw.news_dir(cfg) / "2026-09-11.md").read_text(encoding="utf-8")


# --------------------------------------------------------------------- 논문 DB 격리
def test_news_never_touches_the_paper_db(cfg):
    """⛔음성: 뉴스는 `Paper` 가 아니다. papers 테이블에 한 줄도 들어가면 안 된다."""
    db = PaperDB(cfg.path("storage.sqlite"), cfg.path("storage.jsonl_export"))
    nw.import_news(cfg, _payload(5))
    assert db.list() == [], "뉴스가 논문 DB 로 샜다"


# --------------------------------------------------------------------- 메일 파싱 (순수)
def _mail(body: str, attach: str | None = None, fn: str = "ra-news-20260911.json"):
    """실물과 같은 모양으로 만든다 — **bytes 로 직렬화한 뒤 다시 파싱**한다.

    ⚠ 처음엔 `message_from_string` 으로 짰다가 한글 첨부가 통째로 안 읽혔다. str 로 만든
      메시지는 `get_payload(decode=True)` 가 raw-unicode-escape 로 인코딩해 UTF-8 이
      깨지기 때문인데, **실물 경로는 `message_from_bytes` + base64** 라 그런 일이 없다.
      즉 그건 픽스처의 결함이었다. 픽스처가 실물보다 험하면 없는 버그를 쫓게 된다.
    """
    msg = email.message.EmailMessage()
    msg["Subject"] = "[RA-NEWS] 2026-09-11 weekly 7 items"
    msg["Message-ID"] = "<n1@x>"
    msg.set_content(body)
    if attach is not None:
        msg.add_attachment(attach.encode("utf-8"), maintype="application", subtype="json", filename=fn)
    return email.message_from_bytes(msg.as_bytes())


def test_payloads_from_message_prefers_the_attachment(cfg):
    p = json.dumps(_payload(2), ensure_ascii=False)
    got = payloads_from_message(_mail("본문 인사말 {아무 것도 아님}", attach=p))
    assert len(got) == 1 and got[0]["protocol"] == nw.PROTOCOL and len(got[0]["items"]) == 2


def test_payloads_from_message_falls_back_to_the_body(cfg):
    got = payloads_from_message(_mail("앞말\n" + json.dumps(_payload(1), ensure_ascii=False) + "\n뒷말"))
    assert len(got) == 1 and len(got[0]["items"]) == 1


def test_payloads_from_message_returns_nothing_rather_than_guessing(cfg):
    """⛔음성: JSON 이 없으면 **빈 목록**이다. 반쯤 읽은 걸 지어내지 않는다."""
    assert payloads_from_message(_mail("이번 주 뉴스입니다. 첨부 없음.")) == []
    assert payloads_from_message(_mail("깨진 것: {\"a\": ", attach="{망가진 JSON")) == []


def test_both_mail_paths_share_one_fetcher():
    """⛔음성: handoff 와 news 가 IMAP 걷기를 **두 벌** 갖고 있으면 안 된다.

    한쪽만 고쳐지는 순간(dedupe·lookback·인코딩) 나머지가 조용히 뒤처진다.
    """
    import inspect
    from research_agent import handoff as hf
    assert "fetch_tagged_json" in inspect.getsource(hf.sync_from_mail)
    assert "fetch_tagged_json" in inspect.getsource(nw.sync_news_from_mail)
    assert "imaplib" not in inspect.getsource(nw), "news 가 IMAP 을 따로 연다"


def test_the_two_tags_are_actually_different():
    """같은 태그를 쓰면 뉴스가 논문 경로로 들어가 papers=0 으로 조용히 소비된다."""
    from research_agent import handoff as hf
    assert nw.SUBJECT_TAG != hf.SUBJECT_TAG
    assert nw.PROTOCOL != hf.PROTOCOL
