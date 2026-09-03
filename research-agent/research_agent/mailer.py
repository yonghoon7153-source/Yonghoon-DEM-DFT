"""Digest e-mail sender (SMTP with Gmail app password) + Markdown→HTML conversion.

Also provides `send_handoff` used by the cloud↔local relay (see handoff.py).
"""
from __future__ import annotations

import json
import smtplib
from email.message import EmailMessage
from email.utils import formataddr, make_msgid
from pathlib import Path

try:
    import markdown as _md
except ImportError:  # pragma: no cover
    _md = None

_CSS = """
body{font-family:-apple-system,'Apple SD Gothic Neo','Noto Sans KR',Segoe UI,Roboto,sans-serif;line-height:1.55;color:#1f2328;max-width:820px;margin:0 auto;padding:16px}
h1{font-size:1.5em;border-bottom:2px solid #d0d7de;padding-bottom:.3em}h2{font-size:1.2em;margin-top:1.6em;border-bottom:1px solid #d0d7de}
h3{font-size:1.05em;margin-top:1.3em}blockquote{border-left:4px solid #8250df;background:#f6f8fa;margin:.6em 0;padding:.4em .9em}
code{background:#f6f8fa;padding:1px 4px;border-radius:3px}table{border-collapse:collapse}td,th{border:1px solid #d0d7de;padding:4px 8px}
a{color:#0969da}hr{border:0;border-top:1px solid #d0d7de}
"""


def strip_frontmatter(md: str) -> str:
    if md.startswith("---"):
        end = md.find("\n---", 3)
        if end != -1:
            return md[end + 4:].lstrip("\n")
    return md


def wikilinks_to_text(md: str) -> str:
    """[[Note Name]] → *Note Name* (mail clients can't resolve vault links)."""
    import re
    return re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", lambda m: f"*{m.group(2) or m.group(1)}*", md)


def callouts_to_quotes(md: str) -> str:
    import re
    return re.sub(r"^> \[!(\w+)\]\s*(.*)$", lambda m: f"> **{m.group(1).upper()}** {m.group(2)}", md, flags=re.M)


def md_to_html(md: str) -> str:
    text = callouts_to_quotes(wikilinks_to_text(strip_frontmatter(md)))
    if _md is None:
        return f"<html><body><pre>{text}</pre></body></html>"
    html = _md.markdown(text, extensions=["tables", "fenced_code", "sane_lists", "nl2br"])
    return f"<html><head><meta charset='utf-8'><style>{_CSS}</style></head><body>{html}</body></html>"


def send_email(smtp: dict, to: list[str], subject: str, markdown_body: str, attachments: list[Path] | None = None,
               html: bool = True, from_name: str = "Research Agent") -> str:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr((from_name, smtp["user"]))
    msg["To"] = ", ".join(to)
    msg["Message-ID"] = make_msgid(domain="research-agent.local")
    plain = wikilinks_to_text(strip_frontmatter(markdown_body))
    msg.set_content(plain)
    if html:
        msg.add_alternative(md_to_html(markdown_body), subtype="html")
    for att in attachments or []:
        att = Path(att)
        data = att.read_bytes()
        if att.suffix == ".md":
            msg.add_attachment(data, maintype="text", subtype="markdown", filename=att.name)
        elif att.suffix == ".json":
            msg.add_attachment(data, maintype="application", subtype="json", filename=att.name)
        else:
            msg.add_attachment(data, maintype="application", subtype="octet-stream", filename=att.name)
    with smtplib.SMTP(smtp["host"], int(smtp.get("port", 587)), timeout=60) as s:
        s.ehlo()
        s.starttls()
        s.login(smtp["user"], smtp["password"])
        s.send_message(msg)
    return msg["Message-ID"]


def write_eml_preview(path: Path, subject: str, markdown_body: str) -> Path:
    """For dry runs / sandboxes without SMTP: dump what would be sent."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"subject": subject, "markdown": markdown_body, "html": md_to_html(markdown_body)},
                               ensure_ascii=False, indent=1), encoding="utf-8")
    return path
