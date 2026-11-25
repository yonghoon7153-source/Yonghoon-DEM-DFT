"""IMAP fetcher for Google Scholar alert mails (works with Gmail app passwords — same creds Hermes uses)."""
from __future__ import annotations

import email
import imaplib
import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.header import decode_header, make_header
from email.message import Message
from pathlib import Path


@dataclass
class RawMail:
    message_id: str
    subject: str
    date: str
    html: str | None
    text: str | None
    uid: str

    def dump(self, folder: Path) -> Path:
        folder.mkdir(parents=True, exist_ok=True)
        safe = "".join(c if c.isalnum() else "_" for c in self.message_id)[:80]
        p = folder / f"{self.date[:10]}_{safe}.json"
        p.write_text(json.dumps(self.__dict__, ensure_ascii=False, indent=1), encoding="utf-8")
        return p


def _decode(s: str | None) -> str:
    if not s:
        return ""
    try:
        return str(make_header(decode_header(s)))
    except Exception:
        return s


def _bodies(msg: Message) -> tuple[str | None, str | None]:
    html, text = None, None
    for part in msg.walk():
        ctype = part.get_content_type()
        if part.get_content_disposition() == "attachment":
            continue
        try:
            payload = part.get_payload(decode=True)
        except Exception:
            continue
        if payload is None:
            continue
        charset = part.get_content_charset() or "utf-8"
        body = payload.decode(charset, errors="replace")
        if ctype == "text/html" and html is None:
            html = body
        elif ctype == "text/plain" and text is None:
            text = body
    return html, text


def fetch_scholar_alerts(host: str, port: int, user: str, password: str, folder: str = "INBOX",
                         sender: str = "scholaralerts-noreply@google.com", lookback_days: int = 3,
                         mark_seen: bool = False, only_unseen: bool = False) -> list[RawMail]:
    since = (datetime.now(timezone.utc) - timedelta(days=lookback_days)).strftime("%d-%b-%Y")
    criteria = ["FROM", f'"{sender}"', "SINCE", since]
    if only_unseen:
        criteria.insert(0, "UNSEEN")
    out: list[RawMail] = []
    with imaplib.IMAP4_SSL(host, port) as M:
        M.login(user, password)
        M.select(folder, readonly=not mark_seen)
        typ, data = M.uid("search", None, *criteria)
        if typ != "OK":
            return out
        for uid in data[0].split():
            typ, msg_data = M.uid("fetch", uid, "(BODY.PEEK[])" if not mark_seen else "(RFC822)")
            if typ != "OK" or not msg_data or msg_data[0] is None:
                continue
            raw = msg_data[0][1]
            msg = email.message_from_bytes(raw)
            html, text = _bodies(msg)
            out.append(RawMail(
                message_id=(msg.get("Message-ID") or f"uid:{uid.decode()}").strip(),
                subject=_decode(msg.get("Subject")),
                date=_parse_date(msg.get("Date")),
                html=html, text=text, uid=uid.decode(),
            ))
    return out


def _parse_date(d: str | None) -> str:
    if not d:
        return datetime.now(timezone.utc).isoformat(timespec="seconds")
    try:
        dt = email.utils.parsedate_to_datetime(d)
        return dt.astimezone(timezone.utc).isoformat(timespec="seconds")
    except Exception:
        return datetime.now(timezone.utc).isoformat(timespec="seconds")
