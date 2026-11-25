"""Configuration loading with ${ENV:-default} substitution and repo-relative paths."""
from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

_ENV_RE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?::-([^}]*))?\}")


def _expand(value: Any) -> Any:
    if isinstance(value, str):
        def repl(m: re.Match) -> str:
            name, default = m.group(1), m.group(2)
            return os.environ.get(name, default if default is not None else "")
        return _ENV_RE.sub(repl, value)
    if isinstance(value, list):
        return [_expand(v) for v in value]
    if isinstance(value, dict):
        return {k: _expand(v) for k, v in value.items()}
    return value


def find_repo_root(start: Path | None = None) -> Path:
    """Walk up until a directory containing config/agent.yaml is found."""
    env_root = os.environ.get("RA_ROOT")
    if env_root:
        return Path(env_root).resolve()
    p = (start or Path.cwd()).resolve()
    for cand in [p, *p.parents]:
        if (cand / "config" / "agent.yaml").exists():
            return cand
    # fallback: package parent
    here = Path(__file__).resolve().parent.parent
    if (here / "config" / "agent.yaml").exists():
        return here
    raise FileNotFoundError("config/agent.yaml을 찾을 수 없습니다. RA_ROOT 환경변수를 설정하거나 repo 안에서 실행하세요.")


@dataclass
class Config:
    root: Path
    raw: dict

    # ---- convenience accessors -------------------------------------------------
    def get(self, dotted: str, default: Any = None) -> Any:
        cur: Any = self.raw
        for part in dotted.split("."):
            if not isinstance(cur, dict) or part not in cur:
                return default
            cur = cur[part]
        return cur

    def path(self, dotted: str, default: str | None = None) -> Path:
        val = self.get(dotted, default)
        if val is None:
            raise KeyError(dotted)
        p = Path(str(val)).expanduser()
        return p if p.is_absolute() else (self.root / p)

    @property
    def keywords(self) -> list[dict]:
        return list(self.get("keywords", []))

    @property
    def active_keywords(self) -> list[str]:
        return [k["name"] for k in self.keywords if k.get("active", True)]

    @property
    def timezone(self) -> str:
        return self.get("owner.timezone", "Asia/Seoul")

    def load_journal_table(self) -> dict:
        with open(self.root / "config" / "journal_if.yaml", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def load_research_profile(self) -> str:
        return (self.root / "config" / "research_profile.md").read_text(encoding="utf-8")

    def load_prompt(self, name: str) -> str:
        return (self.root / "prompts" / f"{name}.md").read_text(encoding="utf-8")

    def load_template(self, name: str) -> str:
        return (self.root / "templates" / f"{name}.md").read_text(encoding="utf-8")


def load_config(root: Path | None = None) -> Config:
    root = root or find_repo_root()
    # .env (optional) — same file Hermes uses (~/.hermes/.env) can be pointed to via RA_ENV_FILE
    for env_file in [root / ".env", Path(os.environ.get("RA_ENV_FILE", "")).expanduser()]:
        if env_file and env_file.is_file():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    with open(root / "config" / "agent.yaml", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return Config(root=root, raw=_expand(raw))
