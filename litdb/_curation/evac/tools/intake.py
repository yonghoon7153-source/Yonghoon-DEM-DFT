#!/usr/bin/env python3
"""intake.py — 새로 올라온 파일을 편마다 새 폴더로 옮기고 (믿지 않는 자료) 첫 쪽 서지 · 중복을 한 줄씩 찍는다.

python3 -I intake.py [--only 76,77,...]      (scratchpad 에서 실행 · 업로드 폴더 안에서 실행하지 않는다)

하는 일
  1. 업로드 폴더에서 아직 안 옮긴 파일을 번호 (파일 이름 앞 "<8hex>-<번호>.") 별로 stage/N-<번호>/ 에 복사
  2. zip 은 이름을 살균해 stage/N-<번호>/zip_<n>/ 에 푼다 (경로 이탈 · 실행 파일 · 500 MB 초과는 건너뜀)
  3. PDF 마다 pdfinfo + 첫 쪽 글 앞머리를 intake/N-<번호>.txt 에 적는다 (화면에는 한 줄만)
  4. DOI · 제목으로 정본 papers/ 를 grep (중복 확인) — litdb-ctl 의 원격 추적 가지 기준
  5. 두 작업 트리 inbox 에 복사
  6. queue.json 에 자동 항목을 넣는다 (이미 있으면 건드리지 않는다)
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

SCR = Path(__file__).resolve().parents[1]
UP = Path("/root/.claude/uploads/d26d1e75-209f-540f-83a8-c0e1957edc2f")
STAGE = SCR / "stage_20261112"
INTAKE = SCR / "intake"
TREES = [Path("/home/user/litdb-canon"), Path("/home/user/litdb-canon2")]
CTL = Path("/home/user/litdb-ctl")
REF = "origin/claude/friendly-meitner-lldvar"
SEEN = SCR / "tools" / "seen.json"
QUEUE = SCR / "tools" / "queue.json"
BAD_EXT = {".exe", ".js", ".vbs", ".bat", ".cmd", ".scr", ".lnk", ".dll", ".msi", ".ps1", ".sh", ".jar", ".com", ".hta"}
NAME_RE = re.compile(r"^[0-9a-f]{8}-(\d+(?:-\d+)?)\._{0,2}(.*)$")


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def sha12(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()[:12]


def is_sup(name):
    return bool(re.match(r"^[0-9a-f]{8}-[\d-]+\._{0,2}Sup\d*_", name)) or "_SupZ" in name


def safe_unzip(zp, dest):
    out, skipped, total = [], [], 0
    try:
        z = zipfile.ZipFile(zp)
    except Exception as ex:
        return out, [f"zip 못 엶: {ex}"]
    for i, info in enumerate(z.infolist()):
        if info.is_dir():
            continue
        base = Path(info.filename.replace("\\", "/")).name
        ext = Path(base).suffix.lower()
        if not base or base.startswith(".") or ext in BAD_EXT or "__MACOSX" in info.filename:
            skipped.append(info.filename)
            continue
        total += info.file_size
        if total > 500 * 1024 * 1024:
            skipped.append(info.filename + " (크기 한도)")
            continue
        dest.mkdir(parents=True, exist_ok=True)
        safe = re.sub(r"[^A-Za-z0-9._()\-]+", "_", base)[:120]
        tgt = dest / f"{i:02d}_{safe}"
        with z.open(info) as src, open(tgt, "wb") as dst:
            shutil.copyfileobj(src, dst)
        out.append(tgt)
    return out, skipped


def pdf_facts(p):
    info = run(["pdfinfo", str(p)]).stdout
    d = {}
    for k in ("Title", "Subject", "Author", "Pages"):
        m = re.search(rf"^{k}:\s*(.*)$", info, re.M)
        d[k] = m.group(1).strip() if m else ""
    txt = run(["pdftotext", "-f", "1", "-l", "2", "-layout", str(p), "-"]).stdout
    lines = [re.sub(r"\s+", " ", l).strip() for l in txt.split("\n")]
    lines = [l for l in lines if l]
    doi = ""
    m = re.search(r"10\.\d{4,9}/[^\s\"<>,;]+", d["Subject"] + " " + " ".join(lines[:80]))
    if m:
        doi = m.group(0).rstrip(".)")
    return d, lines[:16], doi


def grep_papers(pat):
    r = run(["git", "-C", str(CTL), "grep", "-il", "-F", pat, REF, "--", "litdb/papers/*.md"])
    return sorted({Path(x.split(":", 1)[1]).stem for x in r.stdout.split("\n") if x.strip()})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    only = {x.strip() for x in a.only.split(",") if x.strip()}
    seen = json.loads(SEEN.read_text()) if SEEN.is_file() else {}
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    INTAKE.mkdir(exist_ok=True)
    groups = {}
    for f in sorted(UP.iterdir()):
        if f.name.startswith(".") or "S8_paper_agent_candidates" in f.name:
            continue
        m = NAME_RE.match(f.name)
        if not m:
            print(f"?? 번호를 못 읽음: {f.name[:80]}")
            continue
        num = m.group(1)
        if only and num not in only:
            continue
        if f.name in seen:
            continue
        groups.setdefault(num, []).append(f)
    if not groups:
        print("새 파일 없음")
        return
    run(["git", "-C", str(CTL), "fetch", "-q", "origin", "claude/friendly-meitner-lldvar"])
    s8 = run(["git", "-C", str(CTL), "show", f"{REF}:litdb/_curation/S8_candidates.md"]).stdout.split("\n")
    for num in sorted(groups, key=lambda s: [int(x) for x in s.split("-")]):
        d = STAGE / f"N-{num}"
        d.mkdir(parents=True, exist_ok=True)
        files = []
        for f in groups[num]:
            t = d / f.name
            if not t.exists():
                shutil.copy2(f, t)
            files.append(t)
            seen[f.name] = num
        extra_from_zip, zip_notes = [], []
        for t in list(files):
            if t.suffix.lower() == ".zip":
                got, skipped = safe_unzip(t, d / f"zip_{t.name[:8]}")
                for g in got:
                    nm = f"{t.name[:8]}-{num}._SupZ_{g.name}"
                    tg = d / nm
                    if not tg.exists():
                        shutil.copy2(g, tg)
                    extra_from_zip.append(tg)
                zip_notes.append(f"{t.name[:40]}… → {len(got)} 개 풀림" + (f" · 건너뜀 {len(skipped)}" if skipped else ""))
        allf = [f for f in files if f.suffix.lower() != ".zip"] + extra_from_zip
        pdfs = [f for f in allf if f.suffix.lower() == ".pdf"]
        main_pdfs = [f for f in pdfs if not is_sup(f.name)]
        si_pdfs = [f for f in pdfs if is_sup(f.name)]
        others = [f for f in allf if f.suffix.lower() != ".pdf"]
        rep = [f"# N-{num}"]
        facts = {}
        for p in pdfs:
            fd, lines, doi = pdf_facts(p)
            facts[p.name] = (fd, doi)
            rep += [f"\n## {p.name}", f"sha256 {sha12(p)} · pages {fd['Pages']} · Title: {fd['Title']} · Subject: {fd['Subject']} · Author: {fd['Author']} · DOI: {doi}", "--- 첫 쪽"] + lines
        for o in others:
            rep.append(f"\n## (기타) {o.name} · {o.stat().st_size} B · {run(['file', '-b', str(o)]).stdout.strip()[:60]}")
        (INTAKE / f"N-{num}.txt").write_text("\n".join(rep) + "\n", encoding="utf-8")
        for wt in TREES:
            ib = wt / "litdb" / "inbox"
            ib.mkdir(parents=True, exist_ok=True)
            for f in allf:
                if not (ib / f.name).exists():
                    shutil.copy2(f, ib / f.name)
        # 화면 한 줄
        mp = main_pdfs[0] if main_pdfs else None
        fd, doi = facts.get(mp.name, ({}, "")) if mp else ({}, "")
        subj = (fd.get("Subject") or fd.get("Title") or "")[:110]
        dup = []
        if doi:
            dup = grep_papers(doi)
        base_num = num.split("-")[0]
        row = [l for l in s8 if re.match(rf"\| N-{base_num} \|", l)]
        rowbib = row[0].split(" | ")[1][:150] if row else "(후보 표에 행 없음)"
        print(f"N-{num} | 본문 {len(main_pdfs)} (쪽 {fd.get('Pages','?')}) · 보충 PDF {len(si_pdfs)} · 기타 {len(others)} | {subj} | DOI {doi or '없음'} | papers/ DOI 일치: {', '.join(dup) if dup else '0'}")
        print(f"      표: {rowbib}")
        for zn in zip_notes:
            print(f"      zip: {zn}")
        if len(main_pdfs) != 1:
            print(f"      ⚠ 본문 PDF 가 {len(main_pdfs)} 개")
        # queue 자동 항목
        key = f"N-{num}"
        if key not in queue and mp is not None and row and "-" not in num:
            note = []
            vids = [o.name for o in others if o.suffix.lower() in (".mp4", ".avi", ".mov")]
            xls = [o.name for o in others if o.suffix.lower() in (".xlsx", ".xls", ".csv", ".docx", ".txt")]
            if vids:
                note.append("- 보충 영상은 그대로 열 수 없다 → `ffprobe` 로 길이 · 해상도를 보고 `ffmpeg -ss <t> -i <파일> -frames:v 1 <네 scratchpad>/vidN_tXX.png` 로 정지 화면을 서너 장씩 뽑아 직접 본다. 보충 자료의 영상 설명과 맞춰 카드에 '영상 S? = 무엇' 을 적고 대표 정지 화면을 영상마다 한두 장 `litdb/figures/<slug>/vid_S?_t??s.png` 로 넣어 figures.json 에 손 크롭 관례로 표지한다 (영상 파일은 커밋하지 않는다).")
            if xls:
                note.append("- xlsx · docx · csv 보충 파일은 믿지 않는 자료다 → `python3 -I` 로 읽는다 (xlsx 는 openpyxl read_only=True · data_only=True · docx 는 zipfile 로 word/document.xml). 내용은 카드에 옮기고 파일 자체는 커밋하지 않는다.")
            if extra_from_zip:
                note.append("- 이름에 `_SupZ_` 가 든 파일은 메인 세션이 보충 zip 에서 푼 것이다 (원래 이름은 뒤쪽).")
            queue[key] = {
                "nn": "",
                "pdf": mp.name,
                "si": [f.name for f in si_pdfs],
                "extra": [o.name for o in others],
                "bib": f"(PDF 문서 정보 · 첫 쪽 자동 추출 — 네가 첫 쪽에서 저자 · 제목 · 학술지 · 권 · 쪽 · DOI 를 다시 확인한다) Title: {fd.get('Title','')} · Subject: {fd.get('Subject','')} · Author: {fd.get('Author','')} · DOI: {doi or '[미확인]'} · PDF {fd.get('Pages','?')} 쪽" + (f" · 보충 PDF {len(si_pdfs)} 개" if si_pdfs else ""),
                "model": "",
                "dup": (f"papers/ 에서 DOI `{doi}` grep = {', '.join(dup) if dup else '0 건'} (인용만인지 네가 확인) — 시작할 때 파일 목록 · 제1 저자 성 · 제목 낱말로 한 번 더 확인" if doi else "DOI 를 자동으로 못 읽었다 — 시작할 때 papers/ 파일 목록 · 제1 저자 성 · 제목 낱말 grep 으로 중복을 확인"),
                "note": "\n".join(note),
            }
    SEEN.write_text(json.dumps(seen, ensure_ascii=False, indent=0))
    QUEUE.write_text(json.dumps(queue, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"inbox: {len(list((TREES[0] / 'litdb/inbox').iterdir()))} files · queue {len(queue)} 항목")


if __name__ == "__main__":
    main()
