"""Cowork 피드백 루프 — 이쪽이 독립으로 잡은 결함들의 회귀.

v0.1.6 에서 P0 두 건을 프로브로 잡았고(`cowork/REPLY_TO_COWORK_v016.md`),
v0.1.7 에서 **둘 다 고쳐졌다.** 그래서 아래 둘은 이제 `xfail` 이 아니라 **정상 회귀**다 —
남겨 두는 이유는 다시 깨지면 알아야 하기 때문이다. 고친 사람의 시험만 믿지 않는다.

v0.1.7 을 읽다 **③ 을 고친 자리 바로 옆에서 새 구멍**이 하나 보였다 (아래 P1).
그건 아직 `xfail` 이다.

    python -m pytest tests/test_cowork_v016_known_defects.py -q -rxX

⛔ 이 파일이 보증하지 못하는 것
  · 피드백 **점수 보정** 로직의 타당성 (지금 `apply_to_scoring: false` 로 꺼져 있다).
  · harvest 의 파싱 정확도 — 여기서 보는 건 "언제 도느냐"지 "잘 읽느냐"가 아니다.
  · 메일 발송 경로 전체. 아래 P1 은 **발송이 실패했을 때의 상태**만 본다.
"""
import shutil
from pathlib import Path

import pytest

from research_agent import feedback as fb
from research_agent.cli import _build_digest, _vault_sync
from research_agent.config import load_config
from research_agent.db import PaperDB
from research_agent.models import Paper, now_iso

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    for d in ("config", "prompts", "templates"):
        shutil.copytree(ROOT / d, tmp_path / d)
    (tmp_path / "vault").mkdir()
    monkeypatch.setenv("RA_ROOT", str(tmp_path))
    cfg = load_config(tmp_path)
    return cfg, PaperDB(cfg.path("storage.sqlite"), cfg.path("storage.jsonl_export"))


def _paper(i=1, **kw):
    d = dict(id=f"doi:10.1/x{i}", title=f"Discrete element modeling of sulfide composite cathode {i}",
             venue="Nature Communications", year=2026, doi=f"10.1/x{i}",
             keywords_matched=["dem battery"], status="analyzed", journal_if=15.7,
             relevance=0.8, tier="A", priority=15780.0, analyzed_at=now_iso(),
             analysis={"one_liner": "요약", "selection_reason": "이유", "key_findings": ["a"]})
    d.update(kw)
    return Paper(**d)


def _borderline(**kw):
    d = dict(i=9, status="rejected", relevance=0.30, analysis=None,
             relevance_reason="축 B 약함", title="Borderline probe paper")
    d.update(kw)
    return _paper(**d)


def test_harvest_failure_does_not_destroy_checkmarks(sandbox, monkeypatch):
    """⛔음성: harvest 가 **실패**하면 노트를 다시 쓰면 안 된다. (v0.1.6 P0 ①-b · v0.1.7 수정)

    `_vault_sync` 는 harvest 를 write 보다 먼저 부르도록 잘 설계돼 있었는데, 그 호출이
    `try/except: 무시하고 계속` 으로 감싸져 있어 **예외 경로에서는 순서 보장이 없어졌다.**
    실측으로 체크가 노트에서도 DB 에서도 사라졌다.

    "부가 기능이니 실패해도 계속" 이라는 판단이 여기서만 거꾸로다 — harvest 실패는
    *"아직 안 걷었다"* 는 뜻이고, 그 상태의 재생성이 파괴 경로다.
    """
    cfg, db = sandbox
    p = _paper(1)
    db.save(p)
    _vault_sync(cfg, db)
    note = next((cfg.path("vault.root") / "Papers").rglob("*.md"))
    note.write_text(note.read_text(encoding="utf-8")
                    .replace("- [ ] 유용함", "- [x] 유용함", 1), encoding="utf-8")

    def boom(*a, **k):                       # 동시 실행 중 락 — 현실적인 실패다
        raise RuntimeError("sqlite is locked")
    monkeypatch.setattr(fb, "harvest", boom)
    out = _vault_sync(cfg, db)

    assert out.get("harvest_ok") is False, "실패를 반환값으로 알려야 한다 (로그만으론 아무도 모른다)"
    assert "- [x] 유용함" in note.read_text(encoding="utf-8"), \
        "harvest 가 실패했는데 노트를 덮어써 체크가 사라졌다"


def test_borderline_papers_have_somewhere_to_answer(sandbox):
    """⛔음성: 디제스트가 판정을 **물어본** 논문에는 답할 자리가 있어야 한다.
    (v0.1.6 P0 ③ · v0.1.7 에서 A안 = stub 노트로 수정)

    ⚠ 이 시험의 v1 은 `borderline_sample()` 직후 바로 `_vault_sync` 를 불렀는데, 그건
      실제 흐름이 아니다 — stub 은 `mark_asked` 가 `extra.borderline_asked_at` 를 남긴
      논문에만 생긴다. 실제 순서(뽑기 → 표시 → 동기화)를 그대로 따라간다.
    """
    cfg, db = sandbox
    db.save(_borderline())
    picked = fb.borderline_sample(db, n=2, threshold=0.35)
    assert picked, "전제: 경계선 표본으로 실제로 뽑힌다"
    fb.mark_asked(db, picked)
    _vault_sync(cfg, db)
    notes = [p.name for p in cfg.path("vault.root").rglob("*.md")]
    assert any("Borderline" in n for n in notes), \
        f"물어보는데 체크할 노트가 없다 — 사용자가 답할 방법이 없다. 노트: {notes}"


def test_borderline_verdict_reaches_the_db(sandbox):
    """⛔음성: stub 에 체크한 판정이 **DB 까지** 와야 한다 — 배관 전체.

    stub 이 만들어지는 것만으로는 부족하다. `harvest()` 가 `Borderline/` 를 안 훑으면
    사용자는 체크했는데 측정치는 영원히 0이고, 그 0이 "다들 무관한 게 맞았다" 로 읽힌다.
    """
    cfg, db = sandbox
    b = _borderline()
    db.save(b)
    fb.mark_asked(db, fb.borderline_sample(db, n=2, threshold=0.35))
    _vault_sync(cfg, db)
    stub = next(p for p in cfg.path("vault.root").rglob("*.md") if "Borderline" in p.name)
    stub.write_text(stub.read_text(encoding="utf-8")
                    .replace("- [ ] 무관", "- [x] 무관", 1), encoding="utf-8")
    _vault_sync(cfg, db)
    assert fb.verdict_of(db.get(b.id)), "stub 판정이 DB 로 안 온다 — 측정이 성립하지 않는다"


@pytest.mark.xfail(reason="v0.1.7 P1 — mark_asked 가 발송 전에 커밋되고 stub 은 발송 후에 생긴다",
                   strict=False)
def test_asking_is_not_committed_before_the_answer_slot_exists(sandbox):
    """⛔음성 **신규 P1**: 물어봤다는 기록이 답할 자리보다 **먼저** 확정되면 안 된다.

    `cmd_morning` 의 순서가 이렇다:

        _build_digest(...)   →  write_digest 후 `fb.mark_asked(db, border)`   ← 여기서 확정
        _send_digest(...)    →  메일 (IMAP/SMTP — 이 파이프라인에서 제일 잘 깨지는 단계)
        _vault_sync(...)     →  `write_borderline_stub`                       ← 여기서 자리 생성

    발송이 예외로 죽으면 `_vault_sync` 가 안 돈다. 그러면 그 논문은
    **`borderline_asked_at` 이 찍힌 채 stub 이 없는 상태**로 남고,
    `borderline_sample` 의 30일 쿨다운이 다시 묻는 것을 막는다.
    ⇒ 한 달 동안 조용히, 물어보지도 답하지도 못하는 논문이 된다.

    ⚠ 이 시험은 `_send_digest` 를 부르지 않고 그 사이 상태를 재현한다 — 발송 실패가
      아니라 **"발송 단계에서 멈췄을 때 남는 상태"** 가 문제이기 때문이다.

    고치는 방향(택일):
      ⓐ stub 생성을 `mark_asked` 와 **같은 자리**로 옮긴다 (물어보기 전에 자리부터 만든다)
      ⓑ `mark_asked` 를 `_vault_sync` 성공 뒤로 미룬다
      ⓒ `borderline_sample` 이 "asked 인데 stub 없음" 을 쿨다운에서 제외한다
    """
    cfg, db = sandbox
    b = _borderline()
    db.save(b)
    picked = fb.borderline_sample(db, n=2, threshold=0.35)
    fb.mark_asked(db, picked)                       # ← 디제스트가 여기까지 하고
    # ← 발송이 죽어 `_vault_sync` 가 안 돈다 (그래서 여기서 부르지 않는다)
    again = fb.borderline_sample(db, n=2, threshold=0.35)
    stubs = [p for p in cfg.path("vault.root").rglob("*.md") if "Borderline" in p.name]
    assert stubs or again, (
        "물어봤다고 표시됐는데 stub 도 없고 쿨다운에 걸려 다시 묻지도 않는다 — "
        "30일 동안 답할 방법이 없는 논문이 된다")


def test_the_defect_paths_are_still_reachable(sandbox):
    """⛔음성: 위 시험들이 **전제 자체가 사라져서** 초록이 되는 것을 막는다.

    `borderline_sample` 이 없어지거나 `_vault_sync` 가 harvest 를 안 부르게 되면
    위 시험들은 "고쳐진 것" 처럼 보인다. 그건 고친 게 아니라 기능이 없어진 것이다.
    """
    import inspect
    assert callable(getattr(fb, "harvest", None)), "harvest 가 사라졌다"
    assert callable(getattr(fb, "borderline_sample", None)), "borderline_sample 이 사라졌다"
    assert callable(getattr(fb, "mark_asked", None)), "mark_asked 가 사라졌다"
    assert "harvest" in inspect.getsource(_vault_sync), "_vault_sync 가 harvest 를 안 부른다"
    assert "mark_asked" in inspect.getsource(_build_digest), "_build_digest 가 ask 를 표시하지 않는다"
