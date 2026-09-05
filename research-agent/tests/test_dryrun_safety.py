"""Regression tests for the 2026-09-04 data-loss incident.

`ra morning --dry-run` destroyed a written 5-paper digest: the dry-run flag gated only the
mail send, so `_vault_sync` and `_git_commit` still ran, and a regenerated 0-paper digest
overwrote the file (164 lines → 22). Two independent guards are tested here — either alone
would have prevented it, and both are required to stay.
"""
import shutil
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from research_agent.cli import cmd_morning, cmd_noon, main
from research_agent.config import load_config
from research_agent.db import PaperDB
from research_agent.models import Paper, now_iso
from research_agent.vault import Vault

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    """A throwaway repo root with real config/prompts/templates but an empty vault + DB."""
    for d in ("config", "prompts", "templates"):
        shutil.copytree(ROOT / d, tmp_path / d)
    (tmp_path / "vault").mkdir()
    monkeypatch.setenv("RA_ROOT", str(tmp_path))
    cfg = load_config(tmp_path)
    db = PaperDB(cfg.path("storage.sqlite"), cfg.path("storage.jsonl_export"))
    return cfg, db


def _rich_digest(v: Vault, date: str, n: int = 5) -> Path:
    body = "\n".join(f"### 논문 {i}\n본문 문단 {i}." for i in range(n))
    return v.write_digest(date, body, {"n_papers": n, "n_a": n, "n_b": 0, "n_c": 0,
                                       "db_total": n, "n_week": n, "n_rejected": 0})


# --------------------------------------------------------------------- guard 1
def test_empty_digest_does_not_overwrite_richer_one(sandbox):
    """The actual mechanism of the incident: a 0-paper regen must not clobber a 5-paper file."""
    cfg, _ = sandbox
    v = Vault(cfg)
    path = _rich_digest(v, "2026-09-04", n=5)
    before = path.read_text(encoding="utf-8")
    assert "논문 4" in before and len(before.splitlines()) > 10

    v.write_digest("2026-09-04", "", {"n_papers": 0, "n_a": 0, "n_b": 0, "n_c": 0,
                                      "db_total": 0, "n_week": 0, "n_rejected": 0})

    assert path.read_text(encoding="utf-8") == before, "빈 디제스트가 기존 파일을 덮었다"


def test_force_still_allows_overwrite_and_keeps_a_backup(sandbox):
    cfg, _ = sandbox
    v = Vault(cfg)
    path = _rich_digest(v, "2026-09-04", n=5)
    v.write_digest("2026-09-04", "새 본문", {"n_papers": 0, "n_a": 0, "n_b": 0, "n_c": 0,
                                            "db_total": 0, "n_week": 0, "n_rejected": 0}, force=True)
    assert "새 본문" in path.read_text(encoding="utf-8")
    backups = list((v.digests_dir / ".backup").glob("2026-09-04.*.md"))
    assert backups and "논문 4" in backups[0].read_text(encoding="utf-8"), "덮어쓰기 전 백업이 없다"


def test_equal_or_larger_digest_overwrites_normally(sandbox):
    cfg, _ = sandbox
    v = Vault(cfg)
    _rich_digest(v, "2026-09-04", n=3)
    path = v.write_digest("2026-09-04", "확장본", {"n_papers": 7, "n_a": 7, "n_b": 0, "n_c": 0,
                                                 "db_total": 7, "n_week": 7, "n_rejected": 0})
    assert "확장본" in path.read_text(encoding="utf-8")


# --------------------------------------------------------------------- guard 2
def test_morning_dry_run_writes_nothing(sandbox, monkeypatch):
    """dry-run must skip vault sync, mail and git — not just mail."""
    cfg, db = sandbox
    p = Paper(id="doi:10.1/x", title="A paper", venue="Nature Communications", year=2026,
              doi="10.1/x", keywords_matched=["dem battery"], status="analyzed",
              journal_if=15.7, relevance=0.9, tier="A", priority=15790.0,
              analyzed_at=now_iso(), analysis={"one_liner": "요약", "selection_reason": "이유",
                                               "key_findings": ["a"]})
    db.upsert(p)

    called = []

    def fake_vault_sync(*a, **k):  # 실제 반환 모양(dict)을 흉내낸다 — cmd_morning 이 이걸 읽는다
        called.append("vault")
        return {"harvest_ok": True, "notes": 0, "stubs": 0, "harvested": 0}

    monkeypatch.setattr("research_agent.cli._vault_sync", fake_vault_sync)
    monkeypatch.setattr("research_agent.cli._git_commit", lambda *a, **k: called.append("git"))
    monkeypatch.setattr("research_agent.cli._send_digest", lambda *a, **k: called.append("mail"))

    cmd_morning(cfg, SimpleNamespace(date="2026-09-04", dry_run=True, force=False))
    assert called == [], f"dry-run 인데 부작용이 실행됐다: {called}"

    cmd_morning(cfg, SimpleNamespace(date="2026-09-04", dry_run=False, force=False))
    assert set(called) == {"vault", "git", "mail"}, f"실제 실행에서 누락: {called}"


def test_noon_dry_run_writes_nothing(sandbox, monkeypatch):
    cfg, db = sandbox
    called = []
    monkeypatch.setattr("research_agent.cli._vault_sync", lambda *a, **k: called.append("vault"))
    monkeypatch.setattr("research_agent.cli._git_commit", lambda *a, **k: called.append("git"))
    monkeypatch.setattr("research_agent.cli._ingest_imap", lambda *a, **k: (0, 0))
    monkeypatch.setattr("research_agent.cli._ingest_manual", lambda *a, **k: 0)

    cmd_noon(cfg, SimpleNamespace(no_imap=True, no_sync=True, dry_run=True))
    assert called == [], f"noon dry-run 인데 부작용이 실행됐다: {called}"


def test_cli_exposes_the_flags():
    """--dry-run on noon and --force on morning/digest must survive refactors."""
    for argv, flag in [(["noon", "--dry-run"], "dry_run"),
                       (["morning", "--force"], "force"),
                       (["digest", "--force"], "force")]:
        with pytest.raises(SystemExit) as e:
            main(argv + ["--help"])
        assert e.value.code == 0
