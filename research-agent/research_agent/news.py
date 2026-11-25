"""주간 배터리 뉴스 아카이브 — Cowork(클라우드)가 보내는 `[RA-NEWS]` 메일의 **수신 쪽**.

층이 셋으로 갈려 있다 (`cowork/PROPOSAL_v018_news.md`):

    Notion 📰 배터리 뉴스   매일 16:00   전부              검색·정렬 (1저자 개인 워크스페이스)
    [Battery Weekly] 메일  금 17:00     골라낸 3~7건      3분 안에 읽히는 것
    여기 (아카이브)         금 17:00     그 주 **전부**    영구 보존 · 브랜치에서 조회

핵심은 **메일에서 잘린 건이 사라지면 안 된다**는 것이다. 제안서를 쓸 때 필요한 건 보통
그때 안 고른 쪽이고, Notion 은 브랜치에서 조회가 안 된다.

전송은 `[RA-HANDOFF]`(논문)와 **subject·protocol 이 분리**돼 있다. 같은 태그를 쓰면 뉴스
메일이 논문 경로로 들어가 `papers=0` 으로 조용히 소비되고 본문이 유실된다. 분리돼 있으니
수신 코드가 없는 동안 메일은 **그냥 메일함에 남는다** — 유실이 아니라 대기고, lookback 21일로
소급 수집된다.

저장 위치는 **A안**(`vault/News/<금요일>.md` + `data/news.jsonl`)으로 확정
(`cowork/REPLY_TO_COWORK_v018.md` §3). `litdb/` 에는 넣지 않는다 — litdb 는 원고가 인용하는
층이라 뉴스가 섞이면 인용층이 오염된다.

⛔ 이 모듈이 **못 하는 것**
  · 뉴스의 **사실 여부를 검증하지 않는다.** 받은 본문을 그대로 보관한다. 여기 있는 문장은
    출처가 언론이지 우리 측정이 아니다 — 원고에 인용 금지, litdb 와 섞지 말 것.
  · `scooping: true` 를 **판정하지 않는다.** 그 판단은 보내는 쪽이 했고 이쪽은 눈에 띄게
    올려 줄 뿐이다. 선점 대응 여부는 사람이 정한다.
  · 논문 DB(`papers` 테이블)를 건드리지 않는다. 뉴스는 `Paper` 가 아니다.
  · `[[wikilink]]` 를 **만들지 않는다** (v0.1.12 결정). 잘못 걸린 링크가 Obsidian 그래프를
    더럽히는 쪽이 링크가 없는 것보다 나쁘다. 본문에 원래 `[[` 가 있으면 그건 보낸 쪽 내용이라
    그대로 두되, `import_news` 가 `wikilinks_passed_through` 로 세어 돌려준다.
  · 노트를 **병합하지 않는다.** 같은 주가 다시 오면 통째로 다시 쓴다(항목이 줄면 거부).
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from .config import Config
from .db import PaperDB
from .models import Alert, now_iso

PROTOCOL = "ra-news/1"
SUBJECT_TAG = "[RA-NEWS]"
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# --------------------------------------------------------------------------- helpers
def _y(v) -> str:
    """YAML scalar. JSON 인코딩이 그대로 YAML flow scalar 라 헤드라인의 `:` · 따옴표가 안전하다."""
    return json.dumps("" if v is None else str(v), ensure_ascii=False)


def _ylist(items) -> str:
    return "[" + ", ".join(json.dumps(str(i), ensure_ascii=False) for i in (items or [])) + "]"


def news_dir(cfg: Config) -> Path:
    return cfg.path("vault.root") / str(cfg.get("vault.news_dir", "News"))


def news_jsonl(cfg: Config) -> Path:
    return cfg.path("storage.news_jsonl", "data/news.jsonl")


def week_stem(payload: dict) -> str:
    """노트 파일명(= 그 주 금요일, YYYY-MM-DD).

    ⛔ 날짜를 못 읽으면 **만들지 않는다.** `News/None.md` 나 `News/.md` 가 한 번 생기면
    다음 주 수신이 그걸 덮어쓰며 주가 뭉개진다 — 조용히 섞이느니 거부한다.
    """
    week = payload.get("week") or {}
    for cand in (week.get("end"), week.get("start"), (payload.get("created_at") or "")[:10]):
        if cand and _DATE_RE.match(str(cand).strip()):
            return str(cand).strip()
    raise ValueError(
        f"⛔ 주 날짜를 못 읽었다 (week.end/week.start/created_at 전부 YYYY-MM-DD 가 아니다): "
        f"{week!r} — 파일명을 지어내지 않고 거부한다")


def item_key(it: dict) -> str:
    """jsonl 중복 제거 키. `source` URL 이 정본이되 **없다고 항목을 버리지 않는다.**"""
    for k in ("source", "notion_url"):
        v = (it.get(k) or "").strip()
        if v:
            return v
    return f"{(it.get('headline') or '').strip()}|{(it.get('date') or '').strip()}"


def build_news(items: list[dict], week: dict, issue: int | None = None,
               weekly_markdown: str = "", notes: str = "", origin: str = "local") -> dict:
    """보내는 쪽 형식 (이쪽은 주로 시험용 — 정본 발신자는 Cowork 다)."""
    return {"protocol": PROTOCOL, "origin": origin, "created_at": now_iso(),
            "week": week, "issue": issue, "items": list(items),
            "weekly_markdown": weekly_markdown, "notes": notes}


# --------------------------------------------------------------------------- render
def render_week(payload: dict) -> str:
    stem = week_stem(payload)
    items = payload.get("items") or []
    week = payload.get("week") or {}
    scooped = [it for it in items if it.get("scooping")]
    axes = sorted({a for it in items for a in (it.get("axes") or [])})

    fm = [
        "---",
        "type: news-week",
        f"week: {_y(stem)}",
        f"week_start: {_y(week.get('start') or '')}",
        f"week_end: {_y(week.get('end') or '')}",
        f"week_label: {_y(week.get('label') or '')}",
        f"issue: {payload.get('issue') if isinstance(payload.get('issue'), int) else 'null'}",
        f"n_items: {len(items)}",
        f"n_scooping: {len(scooped)}",
        f"axes: {_ylist(axes)}",
        f"origin: {_y(payload.get('origin') or '')}",
        f"created_at: {_y(payload.get('created_at') or '')}",
        f"protocol: {_y(payload.get('protocol') or '')}",
        "---",
        "",
    ]
    b = [f"# 배터리 뉴스 — {stem} ({len(items)}건)", ""]
    b += ["> [!info] 자동 생성",
          f"> `{SUBJECT_TAG}` 메일이 만든다. 손으로 고치면 다음 수신 때 `.backup/` 으로 밀린다 — 메모는 딴 노트에.",
          "> 여기 문장은 **언론 출처**지 우리 측정이 아니다. 원고 인용 금지.", ""]
    if scooped:
        b += ["> [!warning] 선점 주의 " + f"{len(scooped)}건"]
        for it in scooped:
            why = (it.get("scooping_why") or "").strip()
            b.append(f"> - **{(it.get('headline') or '(제목 없음)').strip()}**" + (f" — {why}" if why else ""))
        b.append("")
    if (payload.get("weekly_markdown") or "").strip():
        b += ["## 주간 메일 본문", "", payload["weekly_markdown"].strip(), ""]
    b += [f"## 전체 항목 ({len(items)})", ""]
    if not items:
        b += ["- (없음)", ""]
    for i, it in enumerate(items, 1):
        head = (it.get("headline") or "(제목 없음)").strip()
        b.append(f"### {i}. {head}")
        meta = []
        if (it.get("date") or "").strip():
            meta.append((it["date"]).strip())
        if it.get("axes"):
            # ⚠ 축 이름 자체가 "축 A · DEM/MPM" 처럼 ` · ` 를 품고 있어, 구분자를 그대로 쓰면
            #   "2026-09-08 · 축 A · DEM/MPM · [출처]" 가 네 조각으로 읽힌다. 백틱으로 묶는다.
            meta.append(" ".join(f"`{a}`" for a in it["axes"]))
        if (it.get("source") or "").strip():
            meta.append(f"[출처]({it['source'].strip()})")
        if (it.get("notion_url") or "").strip():
            meta.append(f"[Notion]({it['notion_url'].strip()})")
        if it.get("scooping"):
            meta.append("**선점 주의**")
        if meta:
            b.append("- " + " · ".join(meta))
        if (it.get("summary") or "").strip():
            b += ["", f"> {it['summary'].strip()}"]
        if (it.get("body_markdown") or "").strip():
            b += ["", it["body_markdown"].strip()]
        b.append("")
    if (payload.get("notes") or "").strip():
        b += ["---", "", "## 보낸 쪽 메모", "", payload["notes"].strip(), ""]
    return "\n".join(fm + b).rstrip() + "\n"


def _existing_n_items(path: Path) -> int | None:
    try:
        m = re.search(r"^n_items:\s*(\d+)", path.read_text(encoding="utf-8")[:800], re.M)
        return int(m.group(1)) if m else None
    except Exception:
        return None


# --------------------------------------------------------------------------- import
def import_news(cfg: Config, payload: dict, force: bool = False) -> dict:
    """Write one weekly note + append to `data/news.jsonl`. Returns a summary dict.

    **축소 덮어쓰기 거부** — 같은 주가 더 적은 항목으로 다시 오면 쓰지 않는다. 재생성이
    합법적으로 비어 나올 수 있고(수집 창이 움직였다), 그걸로 덮으면 되돌릴 수 없다.
    디제스트(`Vault.write_digest`)와 같은 처방이다.
    """
    if payload.get("protocol") != PROTOCOL:
        raise ValueError(f"unknown protocol: {payload.get('protocol')} (기대: {PROTOCOL}) — "
                         "뉴스가 아닌 payload 를 뉴스로 적지 않는다")
    stem = week_stem(payload)                      # 날짜 못 읽으면 여기서 멈춘다
    items = payload.get("items") or []
    d = news_dir(cfg)
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{stem}.md"

    out: dict = {"week": stem, "note": str(path), "n_items": len(items),
                 "written": False, "why": "", "jsonl_added": 0,
                 "wikilinks_passed_through": 0, "backup": None}

    if path.exists() and not force:
        n_old = _existing_n_items(path)
        if n_old is not None and len(items) < n_old:
            out["why"] = (f"뉴스 보호: {path.name} 은 {n_old}건인데 새로 온 것은 {len(items)}건 — "
                          f"덮어쓰지 않았다 (덮어쓰려면 force=True).")
            print(f"[ra] {out['why']}", flush=True)
            return out

    text = render_week(payload)
    out["wikilinks_passed_through"] = text.count("[[")
    if path.exists() and path.read_text(encoding="utf-8").strip() != text.strip():
        bak = d / ".backup"
        bak.mkdir(exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        bpath = bak / f"{stem}.{stamp}.md"
        bpath.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
        out["backup"] = str(bpath)
    path.write_text(text, encoding="utf-8")
    out["written"] = True
    out["jsonl_added"] = _append_jsonl(cfg, payload, stem)
    return out


def _append_jsonl(cfg: Config, payload: dict, stem: str) -> int:
    """`source` URL 기준 중복 없이 적재. "이 회사가 몇 번 언급됐나" 류 질문용."""
    jp = news_jsonl(cfg)
    jp.parent.mkdir(parents=True, exist_ok=True)
    seen: set[str] = set()
    if jp.exists():
        for line in jp.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                seen.add(item_key(json.loads(line)))
            except Exception:
                continue
    added = 0
    with jp.open("a", encoding="utf-8") as fh:
        for it in payload.get("items") or []:
            k = item_key(it)
            if k in seen:
                continue
            seen.add(k)
            rec = {"week": stem, "issue": payload.get("issue"),
                   "headline": it.get("headline"), "date": it.get("date"),
                   "summary": it.get("summary"), "source": it.get("source"),
                   "notion_url": it.get("notion_url"), "axes": it.get("axes") or [],
                   "scooping": bool(it.get("scooping")), "scooping_why": it.get("scooping_why") or "",
                   "imported_at": now_iso()}
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            added += 1
    return added


# --------------------------------------------------------------------------- sync
def sync_news_from_mail(cfg: Config, db: PaperDB, lookback_days: int = 21, force: bool = False) -> list[dict]:
    """Fetch `[RA-NEWS]` self-mails and archive them (idempotent).

    lookback 이 handoff(7일)보다 긴 21일인 것은 의도다 — 수신 코드가 늦게 붙어도 그 사이
    쌓인 주를 소급해 걷는다.

    `ra sync`(논문) 와 **따로** 돈다. 뉴스 IMAP 이 실패해도 논문 동기화가 멈추면 안 된다.
    """
    from .handoff import fetch_tagged_json
    results = []
    for mid, subject, raw_path, payloads in fetch_tagged_json(cfg, db, SUBJECT_TAG, "news", lookback_days):
        summary = {"message_id": mid, "subject": subject, "imported": []}
        for pl in payloads:
            try:
                summary["imported"].append(import_news(cfg, pl, force=force))
            except Exception as e:  # keep going; a bad week must not block the rest
                summary["imported"].append({"error": str(e)})
        db.record_alert(Alert(message_id=mid, keyword="__news__", received_at=now_iso(),
                              subject=subject, n_items=len(payloads), raw_path=str(raw_path)))
        results.append(summary)
    return results
