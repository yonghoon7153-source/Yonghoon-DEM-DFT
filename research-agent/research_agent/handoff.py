"""Cloud ↔ local relay ("handoff") — lets Cowork (cloud, has Gmail) and Hermes/Claude Code (local, has the
repo, litdb, campus full-text access) cooperate without the user in the loop.

Transport = the owner's own mailbox. The cloud side mails itself a JSON attachment with subject
`[RA-HANDOFF] ...`; the local side runs `ra sync` (Hermes cron / Claude Code) which imports it into the
SQLite DB, Obsidian vault and litdb, then git-commits. Mails queue up if the computer is off.

Payload (protocol ra-handoff/1)
{
  "protocol": "ra-handoff/1", "origin": "cowork-cloud" | "local", "created_at": iso,
  "papers": [Paper.to_dict()...],            # may include filled `analysis`
  "digest": {"date": "YYYY-MM-DD", "markdown": "..."} | null,
  "notes": "free text for the receiving agent"
}
"""
from __future__ import annotations

import email
import imaplib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .config import Config
from .db import PaperDB
from .models import Alert, Paper, now_iso

PROTOCOL = "ra-handoff/1"
SUBJECT_TAG = "[RA-HANDOFF]"


def build_handoff(papers: list[Paper], origin: str, digest: dict | None = None, notes: str = "") -> dict:
    return {"protocol": PROTOCOL, "origin": origin, "created_at": now_iso(),
            "papers": [p.to_dict() for p in papers], "digest": digest, "notes": notes}


def write_handoff_file(payload: dict, folder: Path, job: str = "noon") -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    path = folder / f"ra-handoff-{stamp}-{job}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    return path


def import_handoff(cfg: Config, db: PaperDB, payload: dict, apply_triage_fn=None) -> dict:
    """Merge a handoff payload into the local DB. Returns summary counts."""
    if payload.get("protocol") != PROTOCOL:
        raise ValueError(f"unknown protocol: {payload.get('protocol')}")
    n_new = n_upd = n_an = 0
    thr = float(cfg.get("triage.relevance_threshold", 0.35))
    for rec in payload.get("papers", []):
        incoming = Paper.from_dict(rec)
        stored, is_new = db.upsert(incoming)
        n_new += int(is_new)
        n_upd += int(not is_new)
        # triage fields: take incoming if local has none
        for f in ("journal_canonical", "journal_if", "is_preprint", "relevance", "relevance_reason", "tier", "priority"):
            if getattr(stored, f) in (None, "", 0) and getattr(incoming, f) not in (None, ""):
                setattr(stored, f, getattr(incoming, f))
        if incoming.analysis and not stored.analysis:
            stored.analysis = incoming.analysis
            stored.analyzed_at = incoming.analyzed_at or now_iso()
            stored.status = "analyzed" if (stored.relevance or 0) >= thr else "rejected"
            n_an += 1
        elif is_new and apply_triage_fn:
            apply_triage_fn(stored)
        if incoming.status == "digested" and stored.status == "analyzed":
            stored.status, stored.digested_at = "digested", incoming.digested_at or now_iso()
        db.save(stored)
    digest = payload.get("digest")
    if digest and digest.get("date") and digest.get("markdown"):
        from .vault import Vault
        v = Vault(cfg)
        path = v.digests_dir / f"{digest['date']}.md"
        if not path.exists():
            path.write_text(digest["markdown"], encoding="utf-8")
            db.record_digest(digest["date"], str(path.relative_to(cfg.root)),
                             [r.get("id") for r in payload.get("papers", []) if r.get("id")],
                             sent_at=digest.get("sent_at"), mail_message_id=digest.get("mail_message_id"))
    return {"new": n_new, "updated": n_upd, "analyses": n_an, "digest": bool(digest)}


def sync_from_mail(cfg: Config, db: PaperDB, lookback_days: int = 7) -> list[dict]:
    """Fetch [RA-HANDOFF] self-mails via IMAP and import their JSON attachments (idempotent)."""
    imap = cfg.get("sources.scholar_email.imap", {})
    host, port, user, pw = imap.get("host"), int(imap.get("port", 993)), imap.get("user"), imap.get("password")
    if not (host and user and pw):
        raise RuntimeError("IMAP 설정(EMAIL_ADDRESS/EMAIL_PASSWORD)이 없어 handoff 동기화를 건너뜀")
    since = (datetime.now(timezone.utc) - timedelta(days=lookback_days)).strftime("%d-%b-%Y")
    results = []
    raw_dir = cfg.path("storage.raw_inbox") / "handoff"
    raw_dir.mkdir(parents=True, exist_ok=True)
    with imaplib.IMAP4_SSL(host, port) as M:
        M.login(user, pw)
        M.select(imap.get("folder", "INBOX"), readonly=True)
        typ, data = M.uid("search", None, "SUBJECT", f'"{SUBJECT_TAG}"', "SINCE", since)
        if typ != "OK":
            return results
        for uid in data[0].split():
            typ, md = M.uid("fetch", uid, "(BODY.PEEK[])")
            if typ != "OK" or not md or md[0] is None:
                continue
            msg = email.message_from_bytes(md[0][1])
            mid = (msg.get("Message-ID") or f"uid:{uid.decode()}").strip()
            if db.alert_seen(mid):
                continue
            payloads = []
            for part in msg.walk():
                fn = part.get_filename() or ""
                if fn.endswith(".json"):
                    try:
                        payloads.append(json.loads(part.get_payload(decode=True).decode("utf-8")))
                    except Exception:
                        continue
            if not payloads:
                # body-inline JSON fallback
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        try:
                            txt = part.get_payload(decode=True).decode("utf-8", "replace")
                            s, e = txt.find("{"), txt.rfind("}")
                            if s != -1 and e > s:
                                payloads.append(json.loads(txt[s:e + 1]))
                        except Exception:
                            pass
            summary = {"message_id": mid, "subject": msg.get("Subject", ""), "imported": []}
            for pl in payloads:
                (raw_dir / f"{uid.decode()}.json").write_text(json.dumps(pl, ensure_ascii=False, indent=1), encoding="utf-8")
                try:
                    summary["imported"].append(import_handoff(cfg, db, pl))
                except Exception as e:  # keep going; record error
                    summary["imported"].append({"error": str(e)})
            db.record_alert(Alert(message_id=mid, keyword="__handoff__", received_at=now_iso(),
                                  subject=msg.get("Subject", ""), n_items=len(payloads),
                                  raw_path=str(raw_dir / f"{uid.decode()}.json")))
            results.append(summary)
    return results
