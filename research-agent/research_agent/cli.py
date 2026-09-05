"""`ra` command-line interface.

    ra status                         DB/큐/최근 실행 요약
    ra ingest [--json FILE] [--imap]  alert 메일·수동 JSON 수집 → DB(new)
    ra triage                         new → triaged/rejected (IF·관련도·tier·priority)
    ra analyze [--paper-id ID --from-file F | --direct | --queue]
    ra vault                          모든 노트/MOC/홈 재생성
    ra digest [--date D] [--send] [--dry-run]
    ra noon                           ingest → triage → analyze(direct or queue) → vault → litdb → git commit
    ra morning                        digest → send → vault → git commit
    ra sync                           [RA-HANDOFF] 메일 가져와 DB/vault/litdb 병합 (로컬 측)
    ra feedback [--show] [--dry-run]  노트 체크박스 수집 → 선별 품질 보정 보고서
    ra handoff --job noon             클라우드 측: 분석 결과를 handoff JSON으로 내보내기
    ra litdb                          litdb 재수출
    ra schedule --target crontab|hermes|launchd
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import __version__
from .analyze import analyze_direct, apply_analysis, import_analysis_file, queue_job, validate_analysis
from .config import Config, load_config
from .db import PaperDB
from .digest import digest_stats, polish_with_llm, render_body, select_for_digest, today_str
from .journals import JournalTable
from .llm import LLM
from .models import Alert, Paper, now_iso
from .triage import TriageConfig, apply_triage, rank
from .vault import Vault


# --------------------------------------------------------------------------- helpers
def _db(cfg: Config) -> PaperDB:
    return PaperDB(cfg.path("storage.sqlite"), cfg.path("storage.jsonl_export"))


def _llm(cfg: Config) -> LLM:
    return LLM(backend=cfg.get("llm.backend", "none"), model=cfg.get("llm.model", ""),
               max_tokens=int(cfg.get("llm.max_tokens", 6000)), temperature=float(cfg.get("llm.temperature", 0.2)),
               claude_cli_bin=cfg.get("llm.claude_cli_bin", "claude"))


def _triage_cfg(cfg: Config) -> TriageConfig:
    return TriageConfig(
        relevance_threshold=float(cfg.get("triage.relevance_threshold", 0.35)),
        if_unknown_default=float(cfg.get("triage.if_unknown_default", 3.0)),
        preprint_if=float(cfg.get("triage.preprint_if", 0.0)),
        tiers=cfg.get("triage.tiers"),
        keyword_weights={k["name"]: k.get("weight", 1.0) for k in cfg.keywords},
        active_keywords=cfg.active_keywords,
    )


def _log(msg: str) -> None:
    print(f"[ra {datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def _git_commit(cfg: Config, message: str) -> None:
    if not cfg.get("git.auto_commit", False):
        return
    root = cfg.root
    try:
        subprocess.run(["git", "add", "-A", "data", "vault"], cwd=root, check=False, capture_output=True)
        res = subprocess.run(["git", "commit", "-q", "-m", message], cwd=root, capture_output=True, text=True)
        if res.returncode == 0:
            _log(f"git commit: {message}")
            if cfg.get("git.push", False):
                subprocess.run(["git", "push", "-q", "origin", "HEAD"], cwd=root, check=False, capture_output=True)
        else:
            _log("git: 변경 없음 또는 repo 아님")
    except FileNotFoundError:
        _log("git 없음 — 커밋 생략")


def _vault_sync(cfg: Config, db: PaperDB, digest_date: str | None = None) -> None:
    from . import feedback as fb
    # ★ 순서가 중요하다. 노트는 매번 템플릿에서 다시 쓰이므로, 사용자가 체크한 것을 먼저 DB로
    #   걷어 오지 않으면 그대로 지워진다. harvest → write 순서를 절대 뒤집지 말 것.
    try:
        h = fb.harvest(cfg, db)
        if h.get("updated"):
            _log(f"피드백 {h['updated']}건 수집 (스캔 {h['scanned']}, 미매칭 {h['unmatched']})")
    except Exception as e:  # 피드백은 부가 기능 — 실패해도 vault 동기화는 계속된다
        _log(f"피드백 수집 실패(무시하고 계속): {e}")
    v = Vault(cfg)
    papers = db.list()
    for p in papers:
        if p.status == "rejected" and not p.analysis:
            continue  # rejected-without-analysis: keep out of vault (DB만 보관)
        v.write_paper_note(p, digest_date=digest_date)
        db.save(p)
    v.write_keyword_mocs(papers)
    digests = sorted([d.stem for d in v.digests_dir.glob("*.md")], reverse=True)
    v.write_home(papers, db.counts(), digests)
    db.export_jsonl()


# --------------------------------------------------------------------------- commands
def cmd_status(cfg: Config, args) -> int:
    db = _db(cfg)
    c = db.counts()
    pend = list(cfg.path("storage.analysis_queue").glob("*.json")) if cfg.path("storage.analysis_queue").exists() else []
    print(f"research-agent v{__version__} · root={cfg.root}")
    print(f"papers: {c}")
    print(f"analysis queue (pending): {len(pend)}")
    last = db.last_digest()
    print(f"last digest: {last['date'] if last else '-'} (sent_at={last.get('sent_at') if last else '-'})")
    for r in db.recent_runs(5):
        print(f"  run#{r['id']} {r['job']} {r['status']} {r['started_at']} → {r['finished_at']} {r['summary']}")
    top = db.list(status=["triaged", "analyzed", "digested"], limit=8)
    for p in top:
        print(f"  [{p.tier or '-'}] IF {p.journal_if} rel {p.relevance} {p.status:9s} {p.title[:70]}")
    return 0


def _ingest_imap(cfg: Config, db: PaperDB) -> tuple[int, int]:
    from .sources.imap_client import fetch_scholar_alerts
    from .sources.scholar_email import parse_alert
    s = cfg.get("sources.scholar_email", {})
    imap = s.get("imap", {})
    if not (imap.get("user") and imap.get("password")):
        _log("IMAP 자격증명 없음(EMAIL_ADDRESS/EMAIL_PASSWORD) — alert 메일 수집 건너뜀")
        return 0, 0
    mails = fetch_scholar_alerts(imap["host"], int(imap.get("port", 993)), imap["user"], imap["password"],
                                 folder=imap.get("folder", "INBOX"), sender=s.get("sender"),
                                 lookback_days=int(imap.get("lookback_days", 3)), mark_seen=bool(imap.get("mark_seen", False)))
    n_alerts = n_new = 0
    raw_dir = cfg.path("storage.raw_inbox") / "scholar"
    for m in mails:
        if db.alert_seen(m.message_id):
            continue
        keyword, papers = parse_alert(m.subject, m.html, m.text, m.message_id)
        raw = m.dump(raw_dir)
        for p in papers:
            _, is_new = db.upsert(p)
            n_new += int(is_new)
        db.record_alert(Alert(message_id=m.message_id, keyword=keyword, received_at=m.date, subject=m.subject,
                              n_items=len(papers), raw_path=str(raw)))
        n_alerts += 1
        _log(f"alert '{keyword}' ({m.date[:10]}): {len(papers)} hits")
    return n_alerts, n_new


def _ingest_manual(cfg: Config, db: PaperDB, json_file: Path | None) -> int:
    from .sources.manual import load_manual_dir, paper_from_record
    n_new = 0
    recs: list[Paper] = []
    if json_file:
        data = json.loads(Path(json_file).read_text(encoding="utf-8"))
        recs += [paper_from_record(r) for r in (data if isinstance(data, list) else [data])]
    if cfg.get("sources.manual.enabled", True):
        recs += load_manual_dir(cfg.path("sources.manual.dir"))
    for p in recs:
        _, is_new = db.upsert(p)
        n_new += int(is_new)
    return n_new


def cmd_ingest(cfg: Config, args) -> int:
    db = _db(cfg)
    n_alerts = n_new = 0
    if args.imap or (not args.json and cfg.get("sources.scholar_email.enabled", True)):
        n_alerts, n_new = _ingest_imap(cfg, db)
    n_new += _ingest_manual(cfg, db, Path(args.json) if args.json else None)
    db.export_jsonl()
    _log(f"ingest: alerts={n_alerts} new_papers={n_new}")
    return 0


def _enrich(cfg: Config, papers: list[Paper]) -> None:
    if not cfg.get("enrich.enabled", True):
        return
    from .enrich import enrich_paper
    for p in papers:
        try:
            enrich_paper(p, cfg.get("enrich.providers", []), int(cfg.get("enrich.timeout_sec", 15)), cfg.get("enrich.mailto", ""))
        except Exception as e:  # network optional
            _log(f"enrich 실패({p.id}): {e}")


def cmd_triage(cfg: Config, args) -> int:
    db = _db(cfg)
    jt = JournalTable(cfg.load_journal_table())
    tc = _triage_cfg(cfg)
    new = db.list(status="new")
    if not args.no_enrich:
        _enrich(cfg, new)
    for p in new:
        apply_triage(p, jt, tc)
        db.save(p)
    db.export_jsonl()
    c = db.counts()
    _log(f"triage: {len(new)} processed → {c}")
    for p in rank([p for p in new if p.status != 'rejected'])[:10]:
        _log(f"  [{p.tier}] IF {p.journal_if:<5} rel {p.relevance:<5} {p.title[:80]}")
    return 0


def cmd_analyze(cfg: Config, args) -> int:
    db = _db(cfg)
    if args.from_file:
        p = import_analysis_file(cfg, db, Path(args.from_file), args.paper_id)
        Vault(cfg).write_paper_note(p)
        db.save(p)
        db.export_jsonl()
        _log(f"analysis imported: [{p.tier}] {p.title[:80]}")
        return 0
    if args.import_dir:
        n = 0
        for f in sorted(Path(args.import_dir).glob("*.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                if data.get("analysis"):
                    import_analysis_file(cfg, db, f)
                    n += 1
            except Exception as e:
                _log(f"skip {f.name}: {e}")
        _vault_sync(cfg, db)
        _log(f"imported {n} analyses from {args.import_dir}")
        return 0
    llm = _llm(cfg)
    limit = args.limit or int(cfg.get("triage.max_deep_analysis_per_run", 8))
    todo = rank(db.list(status="triaged"))[:limit]
    if args.paper_id:
        todo = [db.get(args.paper_id)] if db.get(args.paper_id) else []
    mode = "direct" if (args.direct or (llm.available and not args.queue)) else "queue"
    n_done = n_q = 0
    for p in todo:
        if mode == "direct":
            a = analyze_direct(cfg, llm, p)
            ok, msg = validate_analysis(a or {})
            if not ok:
                _log(f"LLM 결과 검증 실패({msg}) → 큐로 이동: {p.title[:60]}")
                queue_job(cfg, p); n_q += 1
                continue
            apply_analysis(p, a, float(cfg.get("triage.relevance_threshold", 0.35)), cfg.get("triage.tiers"))
            db.save(p); n_done += 1
            _log(f"analyzed [{p.tier}] {p.title[:70]}")
        else:
            queue_job(cfg, p); n_q += 1
    if n_q:
        _log(f"{n_q} jobs queued → {cfg.path('storage.analysis_queue')} (Hermes/Claude Code가 채운 뒤 `ra analyze --import-dir`)")
    db.export_jsonl()
    return 0


def cmd_vault(cfg: Config, args) -> int:
    db = _db(cfg)
    _vault_sync(cfg, db)
    _log(f"vault synced → {cfg.path('vault.root')}")
    return 0


def cmd_litdb(cfg: Config, args) -> int:
    from .exporters.litdb import export
    db = _db(cfg)
    out = export(cfg, db.list(status=["triaged", "analyzed", "digested"]))
    _log(f"litdb: {json.dumps(out, ensure_ascii=False)[:300]}")
    return 0


def _build_digest(cfg: Config, db: PaperDB, date: str, llm: LLM | None,
                  force: bool = False, dry_run: bool = False) -> tuple[Path, list[Paper], dict, str]:
    from . import feedback as fb
    v = Vault(cfg)
    papers = select_for_digest(db, cfg)
    border, fstats = [], {}
    try:
        n_border = int(cfg.get("feedback.borderline_per_digest", 2))
        min_s = int(cfg.get("feedback.min_samples", 8))
        if papers and n_border:  # 빈 디제스트를 경계선 표본으로 채우지 않는다
            border = fb.borderline_sample(db, n=n_border,
                                          threshold=float(cfg.get("triage.relevance_threshold", 0.35)))
        fstats = fb.stats(db, min_s)
    except Exception as e:
        _log(f"피드백 집계 실패(무시하고 계속): {e}")
    body = render_body(papers, cfg, v, date, borderline=border, fb=fstats)
    if llm and cfg.get("digest.llm_polish", False):
        body = polish_with_llm(cfg, llm, body, date)
    stats = digest_stats(db, papers, cfg)
    stats["n_borderline"] = len(border)
    stats["n_feedback"] = fstats.get("n_feedback", 0)
    if dry_run:
        # 게이트 3 — dry-run 은 디제스트 파일도 만들지 않는다. 게이트 2(축소 덮어쓰기 거부)가
        # 피해는 막지만, "아무것도 쓰지 않는다"는 약속은 여기서 지켜야 한다.
        return v.digests_dir / f"{date}.md", papers, stats, body
    path = v.write_digest(date, body, stats, force=force)
    if border:
        fb.mark_asked(db, border)  # 같은 논문을 매일 다시 묻지 않는다
    return path, papers, stats, body


def cmd_digest(cfg: Config, args) -> int:
    db = _db(cfg)
    date = args.date or today_str(cfg)
    path, papers, stats, body = _build_digest(cfg, db, date, _llm(cfg),
                                              force=getattr(args, "force", False), dry_run=args.dry_run)
    if args.send and not args.dry_run:
        _log(f"digest written: {path} ({stats['n_papers']} papers)")
        mid = _send_digest(cfg, db, date, path, papers, stats)
        _log(f"sent: {mid}")
        _vault_sync(cfg, db, digest_date=date)
        return 0
    from .mailer import write_eml_preview
    prev = write_eml_preview(cfg.path("storage.raw_inbox") / "outgoing" / f"{date}.json",
                             _subject(cfg, date, stats), body)
    _log(f"dry-run preview: {prev} ({stats['n_papers']} papers, vault 미기록)")
    if not args.dry_run:
        _vault_sync(cfg, db, digest_date=date)
    return 0


def _subject(cfg: Config, date: str, stats: dict) -> str:
    return cfg.get("mail.subject_template", "[Research Agent] {date} digest").format(date=date, **stats)


def _send_digest(cfg: Config, db: PaperDB, date: str, path: Path, papers: list[Paper], stats: dict) -> str | None:
    from .mailer import send_email
    backend = cfg.get("mail.backend", "smtp")
    md = path.read_text(encoding="utf-8")
    mid = None
    if backend == "smtp":
        smtp = cfg.get("mail.smtp", {})
        if not (smtp.get("user") and smtp.get("password")):
            _log("SMTP 자격증명 없음 — 메일 미발송 (vault의 Digests/에는 저장됨)")
        else:
            mid = send_email(smtp, [cfg.get("owner.email")], _subject(cfg, date, stats), md,
                             attachments=[path] if cfg.get("mail.attach_markdown", True) else None,
                             html=bool(cfg.get("mail.html", True)), from_name=smtp.get("from_name", "Research Agent"))
    elif backend == "hermes":
        _log("mail.backend=hermes — Hermes cron의 --deliver email 이 본문을 전달함")
    sent_at = now_iso() if mid or backend == "hermes" else None
    for p in papers:
        p.status, p.digested_at = "digested", sent_at or now_iso()
        db.save(p)
    db.record_digest(date, str(path.relative_to(cfg.root)), [p.id for p in papers], sent_at=sent_at, mail_message_id=mid)
    db.export_jsonl()
    return mid


def cmd_noon(cfg: Config, args) -> int:
    db = _db(cfg)
    run = db.start_run("noon")
    summary: dict = {}
    try:
        if cfg.get("handoff.enabled", True) and not args.no_sync:
            try:
                from .handoff import sync_from_mail
                res = sync_from_mail(cfg, db, int(cfg.get("handoff.lookback_days", 7)))
                summary["handoff_imported"] = len(res)
            except Exception as e:
                _log(f"handoff sync 건너뜀: {e}")
        n_alerts, n_new = _ingest_imap(cfg, db) if not args.no_imap else (0, 0)
        n_new += _ingest_manual(cfg, db, None)
        summary.update(alerts=n_alerts, new=n_new)
        jt, tc = JournalTable(cfg.load_journal_table()), _triage_cfg(cfg)
        new = db.list(status="new")
        _enrich(cfg, new)
        for p in new:
            apply_triage(p, jt, tc); db.save(p)
        llm = _llm(cfg)
        todo = rank(db.list(status="triaged"))[:int(cfg.get("triage.max_deep_analysis_per_run", 8))]
        n_an = n_q = 0
        for p in todo:
            if llm.available:
                a = analyze_direct(cfg, llm, p)
                if validate_analysis(a or {})[0]:
                    apply_analysis(p, a, tc.relevance_threshold, tc.tiers); db.save(p); n_an += 1
                    continue
            queue_job(cfg, p); n_q += 1
        summary.update(analyzed=n_an, queued=n_q)
        if getattr(args, "dry_run", False):
            summary["dry_run"] = True
            db.finish_run(run, "ok", summary)
            _log(f"noon dry-run: {summary} (vault·litdb·commit 생략)")
            return 0
        _vault_sync(cfg, db)
        try:
            from .exporters.litdb import export
            summary["litdb"] = export(cfg, db.list(status=["triaged", "analyzed", "digested"]))
        except Exception as e:
            summary["litdb"] = {"error": str(e)}
        db.finish_run(run, "ok", summary)
        _git_commit(cfg, cfg.get("git.commit_message", "ra: {job} {date}").format(job="noon", date=today_str(cfg), n_new=n_new, n_analyzed=n_an))
        _log(f"noon done: {summary}")
        return 0
    except Exception as e:
        db.finish_run(run, "error", {"error": str(e), **summary})
        raise


def cmd_morning(cfg: Config, args) -> int:
    db = _db(cfg)
    run = db.start_run("morning")
    try:
        date = args.date or today_str(cfg)
        path, papers, stats, _ = _build_digest(cfg, db, date, _llm(cfg),
                                               force=getattr(args, "force", False), dry_run=args.dry_run)
        if args.dry_run:
            # dry-run 은 **아무것도 쓰지 않는다** — 메일도, vault 도, digest 파일도, git 도.
            db.finish_run(run, "ok", {"date": date, "dry_run": True, **stats})
            _log(f"morning dry-run: {date} {stats} (발송·vault·digest·commit 모두 생략)")
            return 0
        mid = _send_digest(cfg, db, date, path, papers, stats)
        _vault_sync(cfg, db, digest_date=date)
        db.finish_run(run, "ok", {"date": date, "sent": bool(mid), **stats})
        _git_commit(cfg, cfg.get("git.commit_message", "ra: {job} {date}").format(job="morning", date=date, n_new=0, n_analyzed=stats["n_papers"]))
        _log(f"morning done: {date} {stats} sent={bool(mid)}")
        return 0
    except Exception as e:
        db.finish_run(run, "error", {"error": str(e)})
        raise


def cmd_sync(cfg: Config, args) -> int:
    """Merge [RA-HANDOFF] mail, then queue anything the cloud left un-analyzed.

    The cloud analyses what it can reach (abstract-level). Papers it marked `triaged` —
    Tier C, or anything whose full text it could not fetch — are queued here so the local
    side (campus network, PDFs) can analyse them properly with `paper-analyst`.
    """
    from .handoff import sync_from_mail
    db = _db(cfg)
    res = sync_from_mail(cfg, db, int(cfg.get("handoff.lookback_days", 7)))
    n_q = 0
    for p in rank(db.list(status="triaged")):
        if not p.analysis:
            queue_job(cfg, p); n_q += 1
    if n_q:
        _log(f"{n_q}편을 분석 큐에 넣었다 → {cfg.path('storage.analysis_queue')} "
             f"(paper-analyst 로 채운 뒤 `ra analyze --import-dir`)")
    _vault_sync(cfg, db)
    try:
        from .exporters.litdb import export
        export(cfg, db.list(status=["triaged", "analyzed", "digested"]))
    except Exception as e:
        _log(f"litdb export 실패: {e}")
    _git_commit(cfg, f"ra: sync {today_str(cfg)} ({len(res)} handoff mails)")
    _log(f"sync: {len(res)} handoff mails → {json.dumps(res, ensure_ascii=False)[:400]}")
    return 0


def cmd_feedback(cfg: Config, args) -> int:
    """노트의 체크박스를 걷어 보정 보고서를 쓴다. 점수 자체는 여기서 바꾸지 않는다."""
    from . import feedback as fb
    db = _db(cfg)
    min_s = int(args.min_samples or cfg.get("feedback.min_samples", 8))
    h = fb.harvest(cfg, db)
    _log(f"피드백 수집: 스캔 {h['scanned']} · 체크됨 {h['found']} · 갱신 {h['updated']} · 미매칭 {h['unmatched']}")
    report = fb.render_report(db, cfg, min_s)
    out = Vault(cfg).moc_path.parent / "피드백 보정.md"
    if not args.dry_run:
        out.write_text(report, encoding="utf-8")
        _log(f"보고서: {out}")
    if args.show or args.dry_run:
        print(report)
    s = fb.stats(db, min_s)
    if s["n_feedback"] < min_s:
        _log(f"표본 {s['n_feedback']}/{min_s} — 아직 점수 보정은 하지 않는다.")
    else:
        adj = fb.axis_adjustments(db, min_s)
        _log(f"축 보정값: {adj or '(표본 부족)'} · 적용={'켜짐' if fb.enabled(cfg) else '꺼짐'}")
    return 0


def cmd_handoff(cfg: Config, args) -> int:
    from .handoff import build_handoff, write_handoff_file
    db = _db(cfg)
    since = args.since or (datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0).isoformat(timespec="seconds"))
    papers = [p for p in db.list() if (p.analyzed_at or p.first_seen) >= since]
    digest = None
    if args.digest:
        dpath = Vault(cfg).digests_dir / f"{args.digest}.md"
        if dpath.exists():
            digest = {"date": args.digest, "markdown": dpath.read_text(encoding="utf-8")}
    payload = build_handoff(papers, origin=args.origin, digest=digest, notes=args.notes or "")
    path = write_handoff_file(payload, cfg.path("handoff.outbox"), job=args.job)
    _log(f"handoff written: {path} ({len(papers)} papers, digest={bool(digest)})")
    print(path)
    return 0


def cmd_schedule(cfg: Config, args) -> int:
    from .scheduler import render
    print(render(cfg, args.target))
    return 0


# --------------------------------------------------------------------------- main
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="ra", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", help="repo root (default: auto-detect / $RA_ROOT)")
    ap.add_argument("--version", action="version", version=f"research-agent {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status")
    s = sub.add_parser("ingest"); s.add_argument("--json"); s.add_argument("--imap", action="store_true")
    s = sub.add_parser("triage"); s.add_argument("--no-enrich", action="store_true")
    s = sub.add_parser("analyze")
    s.add_argument("--paper-id"); s.add_argument("--from-file"); s.add_argument("--import-dir")
    s.add_argument("--direct", action="store_true"); s.add_argument("--queue", action="store_true"); s.add_argument("--limit", type=int)
    sub.add_parser("vault")
    sub.add_parser("litdb")
    s = sub.add_parser("digest"); s.add_argument("--date"); s.add_argument("--send", action="store_true")
    s.add_argument("--dry-run", action="store_true"); s.add_argument("--force", action="store_true", help="더 적은 편수로도 기존 디제스트를 덮어쓴다")
    s = sub.add_parser("noon"); s.add_argument("--no-imap", action="store_true"); s.add_argument("--no-sync", action="store_true")
    s.add_argument("--dry-run", action="store_true", help="수집·triage·분석만 하고 vault·litdb·commit 은 건너뛴다")
    s = sub.add_parser("morning"); s.add_argument("--date"); s.add_argument("--dry-run", action="store_true")
    s.add_argument("--force", action="store_true", help="더 적은 편수로도 기존 디제스트를 덮어쓴다")
    sub.add_parser("sync")
    s = sub.add_parser("feedback"); s.add_argument("--show", action="store_true", help="보고서를 화면에도 출력")
    s.add_argument("--dry-run", action="store_true", help="수집만 하고 보고서 파일은 쓰지 않는다")
    s.add_argument("--min-samples", type=int, help="이 건수 미만이면 보정값을 만들지 않는다 (기본 8)")
    s = sub.add_parser("handoff"); s.add_argument("--job", default="noon"); s.add_argument("--since"); s.add_argument("--digest")
    s.add_argument("--origin", default="local"); s.add_argument("--notes")
    s = sub.add_parser("schedule"); s.add_argument("--target", default="crontab", choices=["crontab", "hermes", "launchd", "systemd"])

    args = ap.parse_args(argv)
    cfg = load_config(Path(args.root) if args.root else None)
    fn = {"status": cmd_status, "ingest": cmd_ingest, "triage": cmd_triage, "analyze": cmd_analyze, "vault": cmd_vault,
          "litdb": cmd_litdb, "digest": cmd_digest, "noon": cmd_noon, "morning": cmd_morning, "sync": cmd_sync,
          "feedback": cmd_feedback, "handoff": cmd_handoff, "schedule": cmd_schedule}[args.cmd]
    return fn(cfg, args)


if __name__ == "__main__":
    sys.exit(main())
