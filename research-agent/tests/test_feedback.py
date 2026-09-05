"""피드백 루프 테스트.

제일 중요한 것은 `test_feedback_survives_note_regeneration` 이다. 노트는 매번 템플릿에서
다시 쓰이므로, harvest 를 write 보다 먼저 부르지 않으면 사용자가 체크한 것이 조용히 사라진다.
2026-09-04 디제스트 사고와 같은 계열(덮어쓰기로 인한 조용한 데이터 손실)이라 회귀로 고정한다.
"""
import shutil
from types import SimpleNamespace

import pytest

from research_agent import feedback as fb
from research_agent.cli import _vault_sync, cmd_feedback
from research_agent.config import load_config
from research_agent.db import PaperDB
from research_agent.models import Paper, now_iso
from research_agent.vault import Vault
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    for d in ("config", "prompts", "templates"):
        shutil.copytree(ROOT / d, tmp_path / d)
    (tmp_path / "vault").mkdir()
    monkeypatch.setenv("RA_ROOT", str(tmp_path))
    cfg = load_config(tmp_path)
    db = PaperDB(cfg.path("storage.sqlite"), cfg.path("storage.jsonl_export"))
    return cfg, db


def _paper(i: int = 1, **kw) -> Paper:
    d = dict(id=f"doi:10.1/x{i}", title=f"Discrete element modeling of sulfide composite cathode {i}",
             venue="Nature Communications", year=2026, doi=f"10.1/x{i}",
             keywords_matched=["dem battery"], status="analyzed", journal_if=15.7,
             relevance=0.8, tier="A", priority=15780.0, analyzed_at=now_iso(),
             analysis={"one_liner": "요약", "selection_reason": "이유", "key_findings": ["a"]})
    d.update(kw)
    return Paper(**d)


def _check(path: Path, label: str, why: str = "") -> None:
    """사용자가 Obsidian 에서 체크한 상황을 재현한다."""
    text = path.read_text(encoding="utf-8").replace(f"- [ ] {label}", f"- [x] {label}", 1)
    if why:
        text = text.replace("왜: ", f"왜: {why}")
    path.write_text(text, encoding="utf-8")


# ------------------------------------------------------------------ 렌더 & 파싱
def test_note_carries_an_unchecked_feedback_section(sandbox):
    cfg, db = sandbox
    p = _paper()
    db.upsert(p)
    path = Vault(cfg).write_paper_note(p)
    text = path.read_text(encoding="utf-8")
    assert "## 피드백" in text
    for label in ("유용함", "무관", "읽음", "안 봄"):
        assert f"- [ ] {label}" in text
    assert "feedback: none" in text


@pytest.mark.parametrize("label,expected", [("유용함", "useful"), ("무관", "irrelevant"),
                                            ("읽음", "read"), ("안 봄", "skipped")])
def test_parse_each_verdict(label, expected):
    body = "\n".join(f"- [{'x' if l == label else ' '}] {l}" for l in ("유용함", "무관", "읽음", "안 봄"))
    assert fb.parse_note(body)["verdict"] == expected


def test_parse_returns_none_when_nothing_checked():
    assert fb.parse_note("- [ ] 유용함\n- [ ] 무관\n왜: \n") is None


def test_multiple_checks_take_the_strongest_signal():
    body = "- [x] 유용함\n- [ ] 무관\n- [x] 읽음\n- [ ] 안 봄"
    assert fb.parse_note(body)["verdict"] == "useful"


def test_why_line_is_captured():
    body = "- [x] 유용함\n- [ ] 무관\n왜: Bruggeman 지수 비교값이 있다"
    assert fb.parse_note(body)["note"] == "Bruggeman 지수 비교값이 있다"


# ------------------------------------------------------------------ 손실 방지 ★
def test_feedback_survives_note_regeneration(sandbox):
    """체크 → vault 재동기화 → 체크가 남아 있어야 한다. harvest 가 write 보다 먼저 돌지 않으면 깨진다."""
    cfg, db = sandbox
    p = _paper()
    db.upsert(p)
    path = Vault(cfg).write_paper_note(p)
    db.save(p)

    _check(path, "유용함", "Bruggeman 비교값")

    _vault_sync(cfg, db)  # 노트를 통째로 다시 쓴다

    after = path.read_text(encoding="utf-8")
    assert "- [x] 유용함" in after, "노트를 다시 쓰면서 체크가 사라졌다"
    assert "Bruggeman 비교값" in after, "왜: 메모가 사라졌다"
    assert "feedback: useful" in after, "frontmatter 에 반영되지 않았다"
    assert fb.verdict_of(db.get(p.id)) == "useful", "DB 에 저장되지 않았다"


def test_harvest_matches_by_ra_id_not_filename(sandbox):
    """제목·연도가 나중에 보정돼 파일명이 바뀌어도 피드백이 끊기면 안 된다."""
    cfg, db = sandbox
    p = _paper()
    db.upsert(p)
    path = Vault(cfg).write_paper_note(p)
    _check(path, "무관")
    renamed = path.with_name("완전히 다른 이름.md")
    path.rename(renamed)

    fb.harvest(cfg, db)
    assert fb.verdict_of(db.get(p.id)) == "irrelevant"


def test_harvest_ignores_unknown_ra_id(sandbox):
    cfg, db = sandbox
    papers_dir = cfg.path("vault.root") / "Papers"
    papers_dir.mkdir(parents=True, exist_ok=True)
    (papers_dir / "orphan.md").write_text('---\nra_id: "doi:10.9/ghost"\n---\n- [x] 유용함\n', encoding="utf-8")
    h = fb.harvest(cfg, db)
    assert h["found"] == 1 and h["unmatched"] == 1 and h["updated"] == 0


# ------------------------------------------------------------------ 집계·보정
def test_no_adjustment_below_min_samples(sandbox):
    """표본이 적을 때 학습하지 않는다 — n=4 로 만든 가중치는 없느니만 못하다."""
    cfg, db = sandbox
    for i in range(4):
        p = _paper(i)
        p.extra = {"feedback": {"verdict": "useful", "note": "", "at": now_iso()}}
        db.upsert(p)
    assert fb.stats(db, min_samples=8)["enough"] is False
    assert fb.axis_adjustments(db, min_samples=8) == {}
    assert "아직 판단할 표본이 아니다" in fb.render_report(db, cfg, 8)


def test_adjustment_appears_with_enough_samples_and_is_capped(sandbox):
    cfg, db = sandbox
    for i in range(12):
        p = _paper(i)
        p.extra = {"feedback": {"verdict": "useful", "note": "", "at": now_iso()}}
        db.upsert(p)
    for i in range(12, 22):  # 다른 축을 무관으로
        p = _paper(i, title=f"DFT study of adsorption energy on NCM {i}", keywords_matched=["dft battery"])
        p.extra = {"feedback": {"verdict": "irrelevant", "note": "", "at": now_iso()}}
        db.upsert(p)
    adj = fb.axis_adjustments(db, min_samples=8, cap=0.10)
    assert adj, "표본이 충분한데 보정값이 없다"
    assert all(abs(v) <= 0.10 + 1e-9 for v in adj.values()), f"상한을 넘었다: {adj}"
    assert adj.get("축 A · DEM/MPM", 0) > 0 > adj.get("축 B · DFT/MLIP", 0)


def test_adjustment_is_off_by_default(sandbox):
    """`feedback.apply_to_scoring` 를 명시적으로 켜지 않으면 점수는 안 바뀐다."""
    cfg, _ = sandbox
    assert fb.enabled(cfg) is False


def test_adjust_relevance_leaves_paper_untouched(sandbox):
    p = _paper()
    new, reason = fb.adjust_relevance(p, {"축 A · DEM/MPM": 0.05})
    assert new == 0.85 and "축 A" in reason
    assert p.relevance == 0.8, "원본 논문의 점수를 건드렸다"


# ------------------------------------------------------------------ 경계선 표본
def test_borderline_sample_picks_just_below_threshold(sandbox):
    cfg, db = sandbox
    db.upsert(_paper(1, status="rejected", relevance=0.30, tier=""))   # 경계선
    db.upsert(_paper(2, status="rejected", relevance=0.05, tier=""))   # 한참 아래 — 뽑히면 안 됨
    db.upsert(_paper(3, status="analyzed", relevance=0.80))            # 통과한 것 — 뽑히면 안 됨
    got = fb.borderline_sample(db, n=2, band=0.10, threshold=0.35)
    assert [p.id for p in got] == ["doi:10.1/x1"]


def test_borderline_skips_already_answered_and_recently_asked(sandbox):
    cfg, db = sandbox
    answered = _paper(1, status="rejected", relevance=0.32, tier="")
    answered.extra = {"feedback": {"verdict": "irrelevant", "note": "", "at": now_iso()}}
    asked = _paper(2, status="rejected", relevance=0.31, tier="")
    asked.extra = {"borderline_asked_at": now_iso()}
    db.upsert(answered); db.upsert(asked)
    assert fb.borderline_sample(db, n=2, threshold=0.35) == []


def test_borderline_not_added_to_an_empty_digest(sandbox):
    """0편인 날 경계선 표본으로 디제스트를 억지로 채우지 않는다."""
    from research_agent.cli import _build_digest
    cfg, db = sandbox
    db.upsert(_paper(1, status="rejected", relevance=0.30, tier=""))
    _, papers, stats, body = _build_digest(cfg, db, "2026-09-05", None, dry_run=True)
    assert papers == [] and stats["n_borderline"] == 0
    assert "경계선 확인" not in body


def test_borderline_block_renders_when_there_are_papers(sandbox):
    from research_agent.cli import _build_digest
    cfg, db = sandbox
    db.upsert(_paper(1))                                                # 디제스트에 뽑힐 논문
    db.upsert(_paper(2, status="rejected", relevance=0.30, tier=""))    # 경계선
    _, papers, stats, body = _build_digest(cfg, db, "2026-09-05", None, dry_run=True)
    assert papers and stats["n_borderline"] == 1
    assert "경계선 확인" in body and "뺀 이유" in body


# ------------------------------------------------------------------ CLI
def test_cmd_feedback_writes_a_report(sandbox):
    cfg, db = sandbox
    db.upsert(_paper())
    rc = cmd_feedback(cfg, SimpleNamespace(show=False, dry_run=False, min_samples=None))
    out = Vault(cfg).moc_path.parent / "피드백 보정.md"
    assert rc == 0 and out.exists() and "피드백 보정" in out.read_text(encoding="utf-8")


def test_cmd_feedback_dry_run_writes_nothing(sandbox, capsys):
    cfg, db = sandbox
    db.upsert(_paper())
    cmd_feedback(cfg, SimpleNamespace(show=False, dry_run=True, min_samples=None))
    assert not (Vault(cfg).moc_path.parent / "피드백 보정.md").exists()


def test_digest_dry_run_does_not_write_the_digest_file(sandbox):
    """게이트 3 — dry-run 은 디제스트 파일도 만들지 않는다."""
    from research_agent.cli import _build_digest
    cfg, db = sandbox
    db.upsert(_paper())
    path, _, _, _ = _build_digest(cfg, db, "2026-09-05", None, dry_run=True)
    assert not path.exists(), "dry-run 인데 디제스트 파일이 생겼다"


# ------------------------------------------------------------------ 백로그 상한 (Claude Code §②)
def test_backlog_is_capped_so_a_mail_outage_cannot_flood_one_digest(sandbox):
    """발송이 며칠 실패해 analyzed 가 쌓여도 한 디제스트가 무한정 커지지 않는다."""
    from research_agent.digest import select_for_digest
    cfg, db = sandbox
    for i in range(40):
        p = _paper(i)
        p.analyzed_at = "2020-01-01T00:00:00+00:00"   # 창 밖 — 두 번째 루프로만 들어온다
        p.priority = float(i)
        db.upsert(p)
    sel = select_for_digest(db, cfg)
    assert len(sel) == 30, f"상한이 걸리지 않았다: {len(sel)}편"
    assert sel[0].priority == 39.0, "상한을 걸 때 우선순위 높은 쪽을 남겨야 한다"


def test_feedback_footer_handles_empty_stats():
    """fb 가 비었을 때 n 을 먼저 읽지 않고 바로 빠져나온다 (Claude Code §①)."""
    from research_agent.digest import _feedback_footer
    assert _feedback_footer({}) == []
    assert _feedback_footer({"n_feedback": 2, "min_samples": 8, "counts": {}})


# ============================================================ P0 회귀 (Claude Code 회신 ④)
# 두 건 다 "정상 경로만 보는 시험" 이 놓친 것이다. 예외 경로와 배관 연결을 직접 고정한다.

def test_harvest_failure_does_not_regenerate_notes(sandbox, monkeypatch):
    """★ P0 ①-b — harvest 가 예외로 죽으면 노트를 다시 쓰면 안 된다 (fail-closed).

    이전 판은 예외를 삼키고 재생성을 계속했다. sqlite 락 한 번에 사용자 체크가 전손되고,
    지워진 걸 모르니 다시 체크하지도 않는다.
    """
    from research_agent import feedback as fbmod
    cfg, db = sandbox
    p = _paper()
    db.upsert(p)
    path = Vault(cfg).write_paper_note(p)
    db.save(p)
    _check(path, "유용함", "이건 살아남아야 한다")
    before = path.read_text(encoding="utf-8")

    def boom(*a, **k):
        raise RuntimeError("sqlite is locked")
    monkeypatch.setattr(fbmod, "harvest", boom)

    out = _vault_sync(cfg, db)

    assert out["harvest_ok"] is False, "실패를 기록하지 않았다"
    assert out["notes"] == 0, "harvest 실패인데 노트를 다시 썼다"
    assert path.read_text(encoding="utf-8") == before, "★ 조용한 전손 — 체크가 지워졌다"


def test_note_with_unharvested_check_is_never_overwritten(sandbox):
    """두 번째 겹 — DB 가 모르는 판정이 노트에 있으면 파일 단계에서 거부한다.

    harvest 실패 경로는 예외뿐이 아니다(ra_id 파싱 실패, 경로 누락…). 게이트 하나로는 모자란다.
    """
    cfg, db = sandbox
    p = _paper()
    db.upsert(p)
    v = Vault(cfg)
    path = v.write_paper_note(p)
    _check(path, "무관", "잘못 골랐다")
    before = path.read_text(encoding="utf-8")

    v.write_paper_note(p)  # DB 는 아직 판정을 모른다 → 거부해야 한다

    assert path.read_text(encoding="utf-8") == before
    assert v.unharvested_feedback(path, p)["verdict"] == "irrelevant"


def test_borderline_paper_gets_a_note_to_answer_in(sandbox):
    """★ P0 ③ — 물어봤으면 답할 자리가 있어야 한다.

    걸러진 논문은 분석이 없어 노트가 안 만들어지는데 디제스트는 "노트에 체크하라"고 안내했다.
    사용자는 Obsidian 을 열고 그 논문을 못 찾는다 → 오탈락 측정치가 구조적으로 영원히 0.
    """
    cfg, db = sandbox
    p = _paper(1, status="rejected", relevance=0.30, tier="",
               relevance_reason="규칙 기반: 매칭 용어 약함")
    p.extra = {"borderline_asked_at": now_iso()}
    db.upsert(p)

    out = _vault_sync(cfg, db)

    stub = Vault(cfg).borderline_path(p)
    assert out["stubs"] == 1 and stub.exists(), "물어본 논문의 노트가 없다"
    text = stub.read_text(encoding="utf-8")
    assert f'ra_id: "{p.id}"' in text, "ra_id 가 없어 harvest 가 매칭할 수 없다"
    assert "## 피드백" in text and "- [ ] 무관" in text
    assert "매칭 용어 약함" in text, "왜 뺐는지가 없으면 판단할 수 없다"
    assert not (Vault(cfg).papers_dir / f"{Vault(cfg).note_name(p)}.md").exists(), \
        "Papers 위계를 어지럽히면 안 된다"


def test_feedback_on_a_borderline_stub_is_harvested(sandbox):
    """stub 에 체크한 판정이 실제로 DB 까지 와야 배관이 이어진 것이다."""
    cfg, db = sandbox
    p = _paper(1, status="rejected", relevance=0.31, tier="")
    p.extra = {"borderline_asked_at": now_iso()}
    db.upsert(p)
    stub = Vault(cfg).write_borderline_stub(p)

    _check(stub, "유용함", "이건 봤어야 했다")
    fb.harvest(cfg, db)

    assert fb.verdict_of(db.get(p.id)) == "useful", "경계선 판정이 DB 에 안 들어왔다"
    assert fb.stats(db)["n_feedback"] == 1


def test_digest_links_the_borderline_note(sandbox):
    """디제스트가 노트를 위키링크로 가리켜야 한다 — 이름만 적으면 못 찾는다."""
    from research_agent.cli import _build_digest
    cfg, db = sandbox
    db.upsert(_paper(1))
    b = _paper(2, status="rejected", relevance=0.30, tier="")
    db.upsert(b)
    _, _, _, body = _build_digest(cfg, db, "2026-09-05", None, dry_run=True)
    assert f"[[{Vault(cfg).note_name(b)}]]" in body
    assert "vault/Borderline/" in body


# ============================================================ P1 회귀 (Claude Code 회신 ⑤)
def test_answer_slot_exists_before_asking_is_committed(sandbox):
    """★ P1 — 발송 단계에서 멈춰도 '물어봤는데 답할 데가 없는' 상태가 남으면 안 된다.

    문제는 발송 실패 자체가 아니라 **그때 남는 상태**다. 그래서 실패를 흉내내지 않고,
    `_build_digest` 까지만 돌린 뒤(= _send_digest 직전에 멈춘 상태) 남은 것을 본다.
    """
    from research_agent.cli import _build_digest
    cfg, db = sandbox
    db.upsert(_paper(1))                                             # 디제스트에 실릴 논문
    b = _paper(2, status="rejected", relevance=0.30, tier="")
    db.upsert(b)

    _build_digest(cfg, db, "2026-09-05", None)                       # 여기서 예외로 멈췄다고 치자

    stub = Vault(cfg).borderline_path(b)
    assert stub.exists(), "★ 물어보기 전에 답할 자리가 없다 — 발송이 깨지면 한 달간 묻히는 논문이 된다"
    assert "## 피드백" in stub.read_text(encoding="utf-8")


def test_asked_without_a_slot_ignores_the_cooldown(sandbox):
    """두 번째 겹 — 순서 보장이 어디선가 뚫려도 논문이 영영 묻히지 않는다."""
    cfg, db = sandbox
    p = _paper(1, status="rejected", relevance=0.31, tier="")
    p.extra = {"borderline_asked_at": now_iso()}                     # 물어봤다고만 찍힌 상태
    db.upsert(p)
    v = Vault(cfg)

    assert fb.borderline_sample(db, n=2, threshold=0.35) == [], "노트 유무를 안 보면 쿨다운에 걸린다"
    got = fb.borderline_sample(db, n=2, threshold=0.35,
                               has_answer_slot=lambda x: v.borderline_path(x).exists())
    assert [x.id for x in got] == [p.id], "★ 답할 자리가 없는데 쿨다운이 적용됐다"

    v.write_borderline_stub(p)                                       # 자리가 생기면 다시 조용해진다
    assert fb.borderline_sample(db, n=2, threshold=0.35,
                                has_answer_slot=lambda x: v.borderline_path(x).exists()) == []


def test_asked_at_is_consistent_between_stub_and_db(sandbox):
    """stub 에 찍힌 asked_at 과 DB 값이 어긋나면 나중에 둘을 대조할 수 없다."""
    from research_agent.cli import _build_digest
    cfg, db = sandbox
    db.upsert(_paper(1))
    b = _paper(2, status="rejected", relevance=0.30, tier="")
    db.upsert(b)
    _build_digest(cfg, db, "2026-09-05", None)
    stamp = (db.get(b.id).extra or {}).get("borderline_asked_at")
    assert stamp and stamp[:10] in Vault(cfg).borderline_path(b).read_text(encoding="utf-8")


def test_dry_run_creates_no_borderline_stub(sandbox):
    """dry-run 은 여전히 아무것도 쓰지 않는다 — stub 도 예외가 아니다."""
    from research_agent.cli import _build_digest
    cfg, db = sandbox
    db.upsert(_paper(1))
    b = _paper(2, status="rejected", relevance=0.30, tier="")
    db.upsert(b)
    _build_digest(cfg, db, "2026-09-05", None, dry_run=True)
    assert not Vault(cfg).borderline_path(b).exists()
    assert (db.get(b.id).extra or {}).get("borderline_asked_at") is None
