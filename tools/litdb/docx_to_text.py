#!/usr/bin/env python3
"""docx_to_text.py — SI 가 .docx 로 오는 논문의 본문/표를 **stdlib 만으로** 텍스트화.

왜 필요한가
  litdb 로 들어오는 Supporting Information 의 상당수가 PDF 가 아니라 Word(.docx)다
  (Wiley/Angew 계열이 특히 `anieXXXX-sup-0001-SuppMat.docx` 를 그대로 올린다).
  이 컨테이너에는 pandoc 도 python-docx 도 없다 → zipfile + XML 파싱(stdlib)으로 직접 푼다.
  표(계산 파라미터·Rietveld·EIS)가 SI 표에 몰려 있어서 **표를 살려서** 뽑는 게 핵심이다.

이 도구가 **못 하는 것** (한계를 먼저 적는다)
  - 수식(OMML)은 텍스트 근사만 한다 — 아래첨자/위첨자/분수 구조가 평문으로 뭉개진다.
    (`Li6PS5Cl` 의 6/5 가 아래첨자였는지 여기선 알 수 없다. 화학식은 본문 PDF 로 교차확인.)
  - 그림은 뽑지 않는다. SI 그림은 `word/media/*` 에 원본이 들어 있고 캡션과의 짝은
    보장되지 않는다 → `--media <dir>` 로 파일만 덤프하고 번호 매칭은 사람이 한다.
  - 변경이력(track changes)·주석은 무시한다(삭제된 텍스트도 같이 나올 수 있다).
  - .doc(구형 바이너리)은 못 읽는다. .docx(OOXML)만 된다.

usage
  python3 tools/litdb/docx_to_text.py <file.docx>                  # stdout
  python3 tools/litdb/docx_to_text.py <file.docx> -o out.md        # 파일로
  python3 tools/litdb/docx_to_text.py <file.docx> --media dir/     # 임베디드 이미지도 덤프
  python3 tools/litdb/docx_to_text.py --selftest
"""
import argparse
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def _text_of_run(r):
    """run 하나의 표시 텍스트. w:t / w:tab / w:br / 삭제 아닌 것만."""
    out = []
    for node in r.iter():
        tag = node.tag
        if tag == W + "t":
            out.append(node.text or "")
        elif tag == W + "tab":
            out.append("\t")
        elif tag in (W + "br", W + "cr"):
            out.append("\n")
    return "".join(out)


def _para_text(p):
    """문단 하나 → 텍스트. 아래/위첨자는 마커로 살린다(화학식 복원용)."""
    chunks = []
    for r in p.findall(f"./{W}r"):
        t = _text_of_run(r)
        if not t:
            continue
        rpr = r.find(f"./{W}rPr")
        va = None
        if rpr is not None:
            v = rpr.find(f"./{W}vertAlign")
            if v is not None:
                va = v.get(W + "val")
        if va == "subscript":
            t = "_" + t.strip() if len(t.strip()) else t
        elif va == "superscript":
            t = "^" + t.strip() if len(t.strip()) else t
        chunks.append(t)
    # 수식(OMML)은 run 밖에 있다 — m:t 를 긁어 붙인다(구조는 잃는다).
    for mt in p.iter():
        if mt.tag.endswith("}t") and "math" in mt.tag:
            chunks.append(mt.text or "")
    return "".join(chunks).strip()


def _cell_text(tc):
    return " ".join(x for x in (_para_text(p) for p in tc.findall(f"./{W}p")) if x).strip()


def _table_md(tbl):
    rows = []
    for tr in tbl.findall(f"./{W}tr"):
        rows.append([_cell_text(tc) for tc in tr.findall(f"./{W}tc")])
    if not rows:
        return ""
    ncol = max(len(r) for r in rows)
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    esc = lambda s: s.replace("|", "\\|").replace("\n", " ")
    out = ["| " + " | ".join(esc(c) for c in rows[0]) + " |",
           "|" + "|".join(["---"] * ncol) + "|"]
    for r in rows[1:]:
        out.append("| " + " | ".join(esc(c) for c in r) + " |")
    return "\n".join(out)


def docx_to_text(path):
    """docx → markdown-ish 텍스트 (문단 + 표)."""
    with zipfile.ZipFile(path) as z:
        if "word/document.xml" not in z.namelist():
            raise ValueError(f"{path}: word/document.xml 이 없다 — .docx(OOXML) 가 아니다")
        xml = z.read("word/document.xml")
    root = ET.fromstring(xml)
    body = root.find(f"./{W}body")
    if body is None:
        raise ValueError(f"{path}: w:body 없음 — 손상된 docx")
    out = []
    for child in body:
        if child.tag == W + "p":
            t = _para_text(child)
            if t:
                out.append(t)
        elif child.tag == W + "tbl":
            md = _table_md(child)
            if md:
                out.append(md)
    txt = "\n\n".join(out)
    return re.sub(r"\n{4,}", "\n\n\n", txt)


def dump_media(path, outdir):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    n = 0
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            if name.startswith("word/media/") and not name.endswith("/"):
                (outdir / Path(name).name).write_bytes(z.read(name))
                n += 1
    return n


def _selftest():
    """양성(정상 docx 를 만들어 왕복) + 음성(깨진 입력을 잡는지) 둘 다."""
    import io
    import tempfile
    ok = True
    # --- 양성: 문단 + 아래첨자 + 표
    doc = (
        '<?xml version="1.0"?>'
        f'<w:document xmlns:w="{W[1:-1]}"><w:body>'
        '<w:p><w:r><w:t>Table S2. DFT parameters</w:t></w:r></w:p>'
        '<w:p><w:r><w:t>Li</w:t></w:r>'
        '<w:r><w:rPr><w:vertAlign w:val="subscript"/></w:rPr><w:t>6</w:t></w:r>'
        '<w:r><w:t>PS</w:t></w:r>'
        '<w:r><w:rPr><w:vertAlign w:val="subscript"/></w:rPr><w:t>5</w:t></w:r>'
        '<w:r><w:t>Cl</w:t></w:r></w:p>'
        '<w:tbl><w:tr><w:tc><w:p><w:r><w:t>cutoff</w:t></w:r></w:p></w:tc>'
        '<w:tc><w:p><w:r><w:t>520 eV</w:t></w:r></w:p></w:tc></w:tr>'
        '<w:tr><w:tc><w:p><w:r><w:t>k-mesh</w:t></w:r></w:p></w:tc>'
        '<w:tc><w:p><w:r><w:t>1x1x1</w:t></w:r></w:p></w:tc></w:tr></w:tbl>'
        '</w:body></w:document>')
    with tempfile.TemporaryDirectory() as d:
        good = Path(d) / "good.docx"
        with zipfile.ZipFile(good, "w") as z:
            z.writestr("word/document.xml", doc)
        got = docx_to_text(good)
        for need in ("Table S2", "Li_6PS_5Cl", "| cutoff | 520 eV |", "| k-mesh | 1x1x1 |"):
            if need not in got:
                print(f"  ✗ 양성 실패: '{need}' 가 결과에 없다"); ok = False
        if ok:
            print("  ✓ 양성: 문단·아래첨자·표 모두 복원")

        # --- 음성 ①: docx 가 아닌 zip (document.xml 없음) → ValueError 여야 한다
        bad1 = Path(d) / "notdocx.docx"
        with zipfile.ZipFile(bad1, "w") as z:
            z.writestr("hello.txt", "nope")
        try:
            docx_to_text(bad1)
            print("  ✗ 음성① 실패: document.xml 없는 zip 을 통과시켰다"); ok = False
        except ValueError:
            print("  ✓ 음성①: document.xml 없는 zip 을 거부")

        # --- 음성 ②: zip 이 아예 아님 (구형 .doc 흉내) → BadZipFile
        bad2 = Path(d) / "old.doc"
        bad2.write_bytes(b"\xd0\xcf\x11\xe0binary junk")
        try:
            docx_to_text(bad2)
            print("  ✗ 음성② 실패: 비-zip 바이너리를 통과시켰다"); ok = False
        except (zipfile.BadZipFile, ValueError):
            print("  ✓ 음성②: 비-zip(.doc) 을 거부")

        # --- 음성 ③: body 없는 손상 docx → ValueError
        bad3 = Path(d) / "nobody.docx"
        with zipfile.ZipFile(bad3, "w") as z:
            z.writestr("word/document.xml",
                       f'<w:document xmlns:w="{W[1:-1]}"></w:document>')
        try:
            docx_to_text(bad3)
            print("  ✗ 음성③ 실패: body 없는 docx 를 통과시켰다"); ok = False
        except ValueError:
            print("  ✓ 음성③: body 없는 docx 를 거부")
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("docx", nargs="?", help=".docx 경로")
    ap.add_argument("-o", "--out", help="출력 파일 (없으면 stdout)")
    ap.add_argument("--media", help="임베디드 이미지 덤프 디렉터리")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if not a.docx:
        ap.error("docx 경로가 필요하다 (또는 --selftest)")
    txt = docx_to_text(a.docx)
    if a.media:
        n = dump_media(a.docx, a.media)
        print(f"[media] {n} files → {a.media}", file=sys.stderr)
    if a.out:
        Path(a.out).write_text(txt, encoding="utf-8")
        print(f"[ok] {len(txt)} chars → {a.out}", file=sys.stderr)
    else:
        sys.stdout.write(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
