"""Cowork v0.1.6 피드백 루프의 **알려진 결함 2건** — 회신 `cowork/REPLY_TO_COWORK_v016.md`.

둘 다 `xfail` 이다. 지금은 실패하는 게 정상이고, Cowork 가 고치면 **XPASS 로 뒤집혀**
아무도 안 물어봐도 화면에 뜬다. 그때 이 파일을 지우지 말고 `xfail` 표시만 떼면
그대로 정상 회귀가 된다.

    python -m pytest tests/test_cowork_v016_known_defects.py -q -rxX

⛔ 이 파일이 보증하지 못하는 것
  · 피드백 **점수 보정** 로직의 타당성 (지금 `apply_to_scoring: false` 로 꺼져 있다).
  · harvest 의 파싱 정확도 — 여기서 보는 건 "언제 도느냐"지 "잘 읽느냐"가 아니다.
  · Cowork 가 어느 안(A/B/C)으로 고칠지. 배관이 이어졌는지만 본다.
"""
import shutil
from pathlib import Path

import pytest

from research_agent import feedback as fb
from research_agent.cli import _vault_sync
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


@pytest.mark.xfail(reason="Cowork v0.1.6 P0 ①-b — harvest 예외를 삼키고 노트를 재생성한다",
                   strict=False)
def test_harvest_failure_must_not_destroy_checkmarks(sandbox, monkeypatch):
    """⛔음성: harvest 가 **실패**하면 노트를 다시 쓰면 안 된다.

    `_vault_sync` 는 harvest 를 write 보다 먼저 부르도록 잘 설계돼 있고, 그 순서는
    `test_feedback_survives_note_regeneration` 이 지킨다. 그런데 그 호출이
    `try/except Exception: 무시하고 계속` 으로 감싸져 있어서 **예외 경로에서는
    순서 보장이 통째로 없어진다** — 안 걷은 채로 노트를 덮어쓴다.

    "부가 기능이니 실패해도 계속" 이라는 판단이 여기서만 거꾸로다. harvest 실패는
    *"아직 안 걷었다"* 는 뜻이고, 그 상태의 재생성이 바로 파괴 경로다. 사용자는
    지워진 걸 모르므로 **다시 체크하지도 않는다.**
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
    _vault_sync(cfg, db)

    survived = "- [x] 유용함" in note.read_text(encoding="utf-8")
    assert survived or fb.verdict_of(db.get(p.id)), (
        "harvest 가 실패하자 체크가 노트에서도 DB 에서도 사라졌다 — 조용한 전손")


@pytest.mark.xfail(reason="Cowork v0.1.6 P0 ③ — 경계선 논문에는 체크할 노트가 없다",
                   strict=False)
def test_borderline_papers_have_somewhere_to_answer(sandbox):
    """⛔음성: 디제스트가 판정을 **물어보는** 논문에는 답할 자리가 있어야 한다.

    `borderline_sample()` 은 `status="rejected"` 에서 뽑고, threshold 아래 논문은
    분석을 안 거쳐 `analysis` 가 없다. 그런데 `_vault_sync` 에는
    `if p.status == "rejected" and not p.analysis: continue` 가 있어 **노트가 안 만들어진다.**
    디제스트 본문은 "노트 맨 아래 `## 피드백`에 남기면 됩니다" 라고 안내한다.

    ⇒ 오탈락 측정치는 구조적으로 영원히 0건이고, 그 0이 "다들 무관한 게 맞았다" 로
      읽힌다. 그쪽이 경고한 *"좁아진다는 사실 자체가 안 보인다"* 가 그대로 재현된다.
    """
    cfg, db = sandbox
    db.save(_paper(9, status="rejected", relevance=0.30, analysis=None,
                   relevance_reason="축 B 약함", title="Borderline probe paper"))
    picked = fb.borderline_sample(db, n=2, threshold=0.35)
    assert picked, "전제: 경계선 표본으로 실제로 뽑힌다"
    _vault_sync(cfg, db)
    notes = [p.name for p in cfg.path("vault.root").rglob("*.md")]
    assert any("Borderline" in n for n in notes), (
        f"물어보는데 체크할 노트가 없다 — 사용자가 답할 방법이 없다. 노트: {notes}")


def test_the_two_defects_are_still_reachable(sandbox):
    """⛔음성: 위 두 xfail 이 **전제 자체가 사라져서** 초록이 되는 것을 막는다.

    `borderline_sample` 이 없어지거나 `_vault_sync` 가 harvest 를 아예 안 부르게 되면
    위 시험들은 "고쳐진 것" 처럼 보인다. 그건 고친 게 아니라 기능이 없어진 것이다.
    """
    cfg, db = sandbox
    assert callable(getattr(fb, "harvest", None)), "harvest 가 사라졌다"
    assert callable(getattr(fb, "borderline_sample", None)), "borderline_sample 이 사라졌다"
    import inspect
    src = inspect.getsource(_vault_sync)
    assert "harvest" in src, "_vault_sync 가 더 이상 harvest 를 부르지 않는다"
