"""LLM backend abstraction.

backends
  anthropic  : direct Messages API (needs ANTHROPIC_API_KEY, `pip install anthropic`)
  claude-cli : `claude -p` headless (uses the Claude Code login/subscription on the machine)
  hermes     : no direct call — the script writes a job file to data/analysis/pending/ and the
               Hermes Agent (running the paper-agent skill) fills it in. `ra analyze --from-file`
               then ingests the result. Same protocol works for Claude Code slash commands.
  none       : return None; caller marks analysis as pending.

All backends expose `complete(system, user) -> str | None` and `complete_json(...) -> dict | None`.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass


def _extract_json(text: str) -> dict | None:
    if not text:
        return None
    text = text.strip()
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    cand = m.group(1) if m else None
    if cand is None:
        start, end = text.find("{"), text.rfind("}")
        cand = text[start:end + 1] if start != -1 and end > start else None
    if cand is None:
        return None
    try:
        return json.loads(cand)
    except json.JSONDecodeError:
        # tolerate trailing commas
        try:
            return json.loads(re.sub(r",(\s*[}\]])", r"\1", cand))
        except Exception:
            return None


@dataclass
class LLM:
    backend: str = "none"
    model: str = "claude-sonnet-4-5"
    max_tokens: int = 6000
    temperature: float = 0.2
    claude_cli_bin: str = "claude"

    @property
    def available(self) -> bool:
        if self.backend == "anthropic":
            return bool(os.environ.get("ANTHROPIC_API_KEY"))
        if self.backend == "claude-cli":
            return shutil.which(self.claude_cli_bin) is not None
        return False  # hermes / none → queue protocol

    def complete(self, system: str, user: str) -> str | None:
        if self.backend == "anthropic":
            return self._anthropic(system, user)
        if self.backend == "claude-cli":
            return self._claude_cli(system, user)
        return None

    def complete_json(self, system: str, user: str) -> dict | None:
        out = self.complete(system, user + "\n\n반드시 하나의 JSON 객체만 출력하세요 (코드펜스 허용).")
        return _extract_json(out or "")

    # ------------------------------------------------------------------ impls
    def _anthropic(self, system: str, user: str) -> str | None:
        try:
            import anthropic  # type: ignore
        except ImportError as e:
            raise RuntimeError("pip install anthropic 필요") from e
        client = anthropic.Anthropic()
        msg = client.messages.create(
            model=self.model, max_tokens=self.max_tokens, temperature=self.temperature,
            system=system, messages=[{"role": "user", "content": user}],
        )
        return "".join(getattr(b, "text", "") for b in msg.content)

    def _claude_cli(self, system: str, user: str) -> str | None:
        cmd = [self.claude_cli_bin, "-p", "--output-format", "text", "--append-system-prompt", system]
        if self.model:
            cmd += ["--model", self.model]
        res = subprocess.run(cmd, input=user, text=True, capture_output=True, timeout=900)
        if res.returncode != 0:
            raise RuntimeError(f"claude -p 실패: {res.stderr[:500]}")
        return res.stdout
