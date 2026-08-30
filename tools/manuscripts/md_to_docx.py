#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""markdown → .docx (WordprocessingML), 표준 라이브러리만.

공저자 회람용 교체안 문서(docs/manuscripts/*.md)를 Word 로 내보낸다.
.docx 는 XML 몇 개를 담은 zip 이라 npm `docx` 없이 stdlib 로 만든다 —
클라우드 컨테이너가 죽어도 재설치가 필요 없다.

지원하는 마크다운 (우리 하우스 문서가 실제로 쓰는 것만):
  #/##/###          제목 (outlineLvl 부여 → Word 탐색창에 뜬다)
  본문 문단          빈 줄로 구분
  > ...             인용 블록 = **원고에 붙여넣는 영문 블록** (좌측 파란 굵은 선 + 들여쓰기)
                    인용 안에서 4칸 이상 들여쓴 줄은 등폭(수식/코드)으로 뽑는다
  - / * 항목         글머리표 (문자 • + 들여쓰기)
  | a | b |         표 (둘째 줄이 |---| 구분선이어야 한다)
  ---               가로줄
  **굵게** *기울임* `코드`

⛔ 이 도구가 못 하는 것 (숨기지 않는다):
  - 번호목록·중첩목록·각주·머리말/꼬리말·목차 필드·페이지 번호
  - 이미지·하이퍼링크·상호참조·추적변경·댓글
  - 표 병합(colspan/rowspan)·표 안의 표·표 안의 글머리표
  - 글머리표는 진짜 numbering.xml 이 아니라 **문자 •** 다 (Word 에서 목록으로 인식 안 됨)
  - 페이지 나누기 제어(§ 분절 방지)를 하지 않는다 — 조판은 사람이 Word 에서 마무리한다
  - 마크다운 전반을 파싱하지 않는다. 위 목록 밖 문법은 **글자 그대로** 나간다
"""
import argparse
import html
import os
import re
import sys
import zipfile

INK = "1F2937"
MUT = "6B7280"
BLU = "1D4ED8"
GRD = "D1D5DB"
HDR = "EEF2FF"
TOTAL_W = 9000                      # A4 - 여백 (dxa)
FONTS = '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Malgun Gothic"/>'
MONO = '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:eastAsia="Malgun Gothic"/>'


class MdError(Exception):
    """입력이 우리 규약을 벗어났을 때. 조용히 넘어가지 않는다."""


# ─────────────────────────────────────────────────────────── 인라인
def _runs(text, size=20, color=INK, bold=False, mono=False):
    """**굵게** *기울임* `코드` 를 w:r 열로. 닫히지 않은 표식은 글자 그대로 둔다."""
    out = []
    pat = re.compile(r"\*\*(.+?)\*\*|`(.+?)`|(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)")
    pos = 0
    for m in pat.finditer(text):
        if m.start() > pos:
            out.append((text[pos:m.start()], bold, False, mono))
        if m.group(1) is not None:
            out.append((m.group(1), True, False, mono))
        elif m.group(2) is not None:
            out.append((m.group(2), bold, False, True))
        else:
            out.append((m.group(3), bold, True, mono))
        pos = m.end()
    if pos < len(text):
        out.append((text[pos:], bold, False, mono))
    if not out:
        out = [("", bold, False, mono)]
    xml = []
    for t, b, i, mo in out:
        rpr = [MONO if mo else FONTS, '<w:sz w:val="%d"/>' % size,
               '<w:color w:val="%s"/>' % color]
        if b:
            rpr.append("<w:b/>")
        if i:
            rpr.append("<w:i/>")
        xml.append('<w:r><w:rPr>%s</w:rPr><w:t xml:space="preserve">%s</w:t></w:r>'
                   % ("".join(rpr), html.escape(t)))
    return "".join(xml)


def _p(text, size=20, color=INK, bold=False, after=120, indent=0,
       left_bar=None, bottom_rule=False, outline=None, mono=False, keep=False,
       style=None):
    ppr = []
    if style:
        ppr.append('<w:pStyle w:val="%s"/>' % style)
    ppr.append('<w:spacing w:after="%d" w:line="276" w:lineRule="auto"/>' % after)
    if indent:
        ppr.append('<w:ind w:left="%d"/>' % indent)
    if left_bar:
        ppr.append('<w:pBdr><w:left w:val="single" w:sz="18" w:space="8" w:color="%s"/></w:pBdr>'
                   % left_bar)
    if bottom_rule:
        ppr.append('<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="4" w:color="%s"/></w:pBdr>'
                   % GRD)
    if outline is not None:
        ppr.append('<w:outlineLvl w:val="%d"/>' % outline)
        ppr.append('<w:keepNext/>')
    if keep:
        ppr.append("<w:keepNext/>")
    return ('<w:p><w:pPr>%s</w:pPr>%s</w:p>'
            % ("".join(ppr), _runs(text, size, color, bold, mono)))


# ─────────────────────────────────────────────────────────── 표
def _split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def _is_sep(cells):
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c) for c in cells)


def _widths(rows, ncol):
    span = [max((len(r[j]) for r in rows if j < len(r)), default=1) for j in range(ncol)]
    span = [max(6, s) for s in span]
    tot = sum(span)
    w = [max(700, int(TOTAL_W * s / tot)) for s in span]
    k = TOTAL_W / sum(w)
    return [int(x * k) for x in w]


def _table(rows):
    ncol = len(rows[0])
    for i, r in enumerate(rows):
        if len(r) != ncol:
            raise MdError("표의 열 수가 어긋난다 — 머리행 %d열인데 %d번째 행이 %d열: %r"
                          % (ncol, i + 1, len(r), r))
    w = _widths(rows, ncol)
    borders = ("<w:tblBorders>" + "".join(
        '<w:%s w:val="single" w:sz="4" w:space="0" w:color="%s"/>' % (e, GRD)
        for e in ("top", "left", "bottom", "right", "insideH", "insideV")) + "</w:tblBorders>")
    out = ['<w:tbl><w:tblPr><w:tblW w:w="%d" w:type="dxa"/>%s</w:tblPr><w:tblGrid>%s</w:tblGrid>'
           % (TOTAL_W, borders, "".join('<w:gridCol w:w="%d"/>' % x for x in w))]
    for i, r in enumerate(rows):
        cells = []
        for j, c in enumerate(r):
            shd = ('<w:shd w:val="clear" w:color="auto" w:fill="%s"/>' % HDR) if i == 0 else ""
            body = ('<w:p><w:pPr><w:spacing w:after="0" w:line="260" w:lineRule="auto"/></w:pPr>%s</w:p>'
                    % _runs(c, size=18, bold=(i == 0)))
            cells.append('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s'
                         '<w:tcMar><w:top w:w="60" w:type="dxa"/><w:bottom w:w="60" w:type="dxa"/>'
                         '<w:left w:w="100" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tcMar>'
                         '</w:tcPr>%s</w:tc>' % (w[j], shd, body))
        # 행이 페이지 경계에서 쪼개지면 읽는 사람이 값을 잃는다 (회신 AF 조판)
        hdr = ('<w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>' if i == 0
               else '<w:trPr><w:cantSplit/></w:trPr>')
        out.append("<w:tr>%s%s</w:tr>" % (hdr, "".join(cells)))
    out.append("</w:tbl>")
    out.append(_p("", after=60))          # Word 는 표 뒤에 문단을 요구한다
    return "".join(out)


# ─────────────────────────────────────────────────────────── 본체
def md_to_body(md):
    if not md.strip():
        raise MdError("입력이 비어 있다")
    lines = md.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out, i, n = [], 0, len(lines)
    while i < n:
        ln = lines[i]
        s = ln.strip()

        if not s:
            i += 1
            continue

        if re.fullmatch(r"-{3,}|_{3,}|\*{3,}", s):
            out.append(_p("", after=100, bottom_rule=True))
            i += 1
            continue

        m = re.match(r"^(#{1,4})\s+(.*)$", s)
        if m:
            lvl = len(m.group(1))
            size = {1: 34, 2: 27, 3: 23, 4: 21}[lvl]
            out.append(_p(m.group(2), size=size, bold=True, after=140,
                          outline=lvl - 1, style="Heading%d" % lvl))
            i += 1
            continue

        # 표: 이 줄이 |...| 이고 다음 줄이 구분선
        if s.startswith("|") and i + 1 < n and _is_sep(_split_row(lines[i + 1])):
            head = _split_row(s)
            if len(_split_row(lines[i + 1])) != len(head):
                raise MdError("표 구분선의 열 수가 머리행과 다르다 (행 %d)" % (i + 2))
            rows = [head]
            i += 2
            while i < n and lines[i].strip().startswith("|"):
                rows.append(_split_row(lines[i].strip()))
                i += 1
            out.append(_table(rows))
            continue

        # 인용 = 영문 붙여넣기 블록
        if s.startswith(">"):
            buf, block = [], []
            while i < n and lines[i].strip().startswith(">"):
                raw = re.sub(r"^\s*>\s?", "", lines[i])
                if not raw.strip():
                    if buf:
                        block.append((" ".join(buf), False))
                        buf = []
                elif raw.startswith("    "):
                    if buf:
                        block.append((" ".join(buf), False))
                        buf = []
                    block.append((raw.strip(), True))
                else:
                    buf.append(raw.strip())
                i += 1
            if buf:
                block.append((" ".join(buf), False))
            for j, (txt, mono) in enumerate(block):
                out.append(_p(txt, indent=340, left_bar=BLU, mono=mono,
                              after=(140 if j == len(block) - 1 else 80)))
            continue

        m = re.match(r"^[-*]\s+(.*)$", s)
        if m:
            while i < n and re.match(r"^\s*[-*]\s+", lines[i]):
                item = re.sub(r"^\s*[-*]\s+", "", lines[i]).strip()
                j = i + 1
                while j < n and lines[j].strip() and not re.match(
                        r"^\s*([-*]\s+|\||#|>)", lines[j]) and lines[j].startswith("  "):
                    item += " " + lines[j].strip()
                    j += 1
                out.append(_p("• " + item, indent=280, after=70))
                i = j
            continue

        # 일반 문단 — 다음 빈 줄/블록 시작까지 합친다
        buf = [s]
        i += 1
        while i < n and lines[i].strip() and not re.match(
                r"^\s*(#{1,4}\s|\||>|[-*]\s|-{3,}$)", lines[i]):
            buf.append(lines[i].strip())
            i += 1
        out.append(_p(" ".join(buf)))
    return "".join(out)


STYLES = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
          '<w:docDefaults><w:rPrDefault><w:rPr>' + FONTS +
          '<w:sz w:val="20"/></w:rPr></w:rPrDefault></w:docDefaults>'
          '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
          '<w:name w:val="Normal"/></w:style>' +
          "".join(
              '<w:style w:type="paragraph" w:styleId="Heading%d">'
              '<w:name w:val="heading %d"/><w:basedOn w:val="Normal"/>'
              '<w:qFormat/><w:pPr><w:keepNext/><w:outlineLvl w:val="%d"/>'
              '<w:spacing w:before="%d" w:after="140"/></w:pPr>'
              '<w:rPr><w:b/><w:sz w:val="%d"/><w:color w:val="%s"/></w:rPr></w:style>'
              % (i, i, i - 1, 320 - 40 * i, sz, INK)
              for i, sz in ((1, 34), (2, 27), (3, 23), (4, 21))) +
          '</w:styles>')

DOC_TPL = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
           '<w:body>%s'
           '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
           '<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134"'
           ' w:header="708" w:footer="708" w:gutter="0"/></w:sectPr>'
           '</w:body></w:document>')

CT = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
      '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
      '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
      '<Default Extension="xml" ContentType="application/xml"/>'
      '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-'
      'officedocument.wordprocessingml.document.main+xml"/>'
      '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-'
      'officedocument.wordprocessingml.styles+xml"/></Types>')

RELS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
        'relationships/officeDocument" Target="word/document.xml"/></Relationships>')

DOC_RELS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/'
            '2006/relationships/styles" Target="styles.xml"/></Relationships>')


def build(md, out_path):
    body = md_to_body(md)
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CT)
        z.writestr("_rels/.rels", RELS)
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/document.xml", DOC_TPL % body)
    return out_path


# ─────────────────────────────────────────────────────────── selftest
def selftest():
    ok = fail = 0

    def chk(name, cond):
        nonlocal ok, fail
        if cond:
            ok += 1
        else:
            fail += 1
            print("  ✗ %s" % name)

    def neg(name, fn, frag=""):
        nonlocal ok, fail
        try:
            fn()
        except MdError as e:
            if frag and frag not in str(e):
                fail += 1
                print("  ✗ %s — 메시지에 %r 없음: %s" % (name, frag, e))
            else:
                ok += 1
            return
        except Exception as e:                       # noqa: BLE001
            fail += 1
            print("  ✗ %s — MdError 가 아니라 %s" % (name, type(e).__name__))
            return
        fail += 1
        print("  ✗ %s — 통과해 버렸다 (막았어야 한다)" % name)

    # ── 양성
    b = md_to_body("# 제목\n\n본문 하나.\n")
    chk("H1 이 Heading1 스타일을 쓴다 (탐색창·목차)", '<w:pStyle w:val="Heading1"/>' in b)
    chk("H2 는 Heading2", '<w:pStyle w:val="Heading2"/>' in md_to_body("## 둘\n"))
    chk("H1 이 굵고 크게", '<w:sz w:val="34"/>' in b and "<w:b/>" in b)
    chk("H1 이 탐색창에 뜬다", '<w:outlineLvl w:val="0"/>' in b)
    chk("본문 텍스트", "본문 하나." in b)

    b = md_to_body("| a | b |\n|---|---|\n| 1 | 2 |\n")
    chk("표 생성", "<w:tbl>" in b and b.count("<w:tr>") == 2)
    chk("머리행 음영", HDR in b)
    chk("머리행 반복", "<w:tblHeader/>" in b)
    chk("행이 페이지 사이에서 안 쪼개진다", b.count("<w:cantSplit/>") == 2)
    chk("[음성] 본문 행에는 tblHeader 가 안 붙는다", b.count("<w:tblHeader/>") == 1)
    chk("표 뒤 문단", b.rstrip().endswith("</w:p>"))

    b = md_to_body("> English block here.\n> second line.\n")
    chk("인용이 한 문단으로 합쳐진다", "English block here. second line." in b)
    chk("인용 좌측 선", 'w:left w:val="single"' in b and BLU in b)

    b = md_to_body("> lead\n>\n>     E = a - b\n")
    chk("인용 안 들여쓴 줄은 등폭", "Consolas" in b)

    b = md_to_body("**굵게** 와 `코드` 와 *기울임*")
    chk("굵게", "<w:b/>" in b)
    chk("코드 등폭", "Consolas" in b)
    chk("기울임", "<w:i/>" in b)

    b = md_to_body("- 하나\n- 둘\n")
    chk("글머리표 문자", b.count("•") == 2)

    b = md_to_body("---\n")
    chk("가로줄", "w:bottom w:val=\"single\"" in b)

    b = md_to_body("a < b & c > d")
    chk("XML 특수문자 이스케이프", "&lt;" in b and "&amp;" in b and "&gt;" in b)
    chk("날 것의 & 가 남지 않는다", "b & c" not in b)

    b = md_to_body("값은 **[___]** eV 다")
    chk("자리표시자 보존", "[___]" in b)

    # 실제 zip 이 열리는가
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "t.docx")
        build("# T\n\n| a |\n|---|\n| 1 |\n", p)
        with zipfile.ZipFile(p) as z:
            names = set(z.namelist())
            chk("docx 5부 구성", names == {"[Content_Types].xml", "_rels/.rels",
                                           "word/_rels/document.xml.rels",
                                           "word/styles.xml", "word/document.xml"})
            chk("styles.xml 이 XML 로 파싱된다", _parses(z.read("word/styles.xml").decode()))
            chk("zip 무결성", z.testzip() is None)
            doc = z.read("word/document.xml").decode()
            chk("document.xml 이 XML 로 파싱된다", _parses(doc))
            chk("sectPr 존재", "<w:sectPr>" in doc)

    # ── 음성 (틀린 입력을 실제로 잡는가)
    neg("빈 입력", lambda: md_to_body("   \n\n"), "비어")
    neg("본문 행이 머리행보다 열이 많다",
        lambda: md_to_body("| a | b |\n|---|---|\n| 1 | 2 | 3 |\n"), "열 수")
    neg("본문 행이 머리행보다 열이 적다",
        lambda: md_to_body("| a | b | c |\n|---|---|---|\n| 1 | 2 |\n"), "열 수")
    neg("구분선 열 수 불일치",
        lambda: md_to_body("| a | b |\n|---|\n| 1 | 2 |\n"), "구분선")

    # 닫히지 않은 표식은 글자 그대로 — 문서 끝까지 굵어지면 안 된다
    b = md_to_body("**열린 굵게 와 나머지 본문")
    chk("[음성] 닫히지 않은 ** 는 굵게 처리 안 함", "<w:b/>" not in b)
    chk("[음성] 닫히지 않은 ** 는 글자로 남는다", "**열린 굵게" in b)

    # 구분선이 없으면 표가 아니다 — 조용히 표로 만들면 안 된다
    b = md_to_body("| a | b |\n| 1 | 2 |\n")
    chk("[음성] 구분선 없는 파이프 줄은 표가 아니다", "<w:tbl>" not in b)

    # 표 안의 특수문자가 이스케이프되는가 (안 하면 Word 가 파일을 못 연다)
    b = md_to_body("| x |\n|---|\n| a & b |\n")
    chk("[음성] 표 셀도 이스케이프", "&amp;" in b and _parses(DOC_TPL % b))

    print("selftest: %d/%d" % (ok, ok + fail))
    return 0 if fail == 0 else 1


def _parses(xml):
    import xml.etree.ElementTree as ET
    try:
        ET.fromstring(xml)
        return True
    except ET.ParseError:
        return False


def main():
    ap = argparse.ArgumentParser(description="markdown → .docx (stdlib only)")
    ap.add_argument("src", nargs="?", help="입력 .md")
    ap.add_argument("dst", nargs="?", help="출력 .docx")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.src or not a.dst:
        ap.error("src 와 dst 가 필요하다 (또는 --selftest)")
    if not os.path.exists(a.src):
        print("⛔ 입력이 없다: %s" % a.src, file=sys.stderr)
        return 2
    try:
        build(open(a.src, encoding="utf-8").read(), a.dst)
    except MdError as e:
        print("⛔ 마크다운 규약 위반: %s" % e, file=sys.stderr)
        return 3
    print("✓ %s → %s (%.1f KB)" % (a.src, a.dst, os.path.getsize(a.dst) / 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
