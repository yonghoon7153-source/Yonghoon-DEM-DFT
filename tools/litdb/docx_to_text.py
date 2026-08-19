#!/usr/bin/env python3
"""docx_to_text.py — SI 가 .docx / .xlsx 로 오는 논문의 본문·표·Source Data 를
**stdlib 만으로** 텍스트화.

왜 필요한가
  litdb 로 들어오는 Supporting Information 의 상당수가 PDF 가 아니라 Word(.docx)다
  (Wiley/Angew 계열이 특히 `anieXXXX-sup-0001-SuppMat.docx` 를 그대로 올린다).
  이 컨테이너에는 pandoc 도 python-docx 도 없다 → zipfile + XML 파싱(stdlib)으로 직접 푼다.
  표(계산 파라미터·Rietveld·EIS)가 SI 표에 몰려 있어서 **표를 살려서** 뽑는 게 핵심이다.
  2026-08-19 추가: Nature 계열의 **Source Data (.xlsx)** — 그림의 원수치가 들어 있어
  digest 의 `figure-read ≈` 를 **exact** 로 승격시킬 수 있다. openpyxl 이 없어서
  같은 수법(zip+XML)으로 읽는다. `--xlsx` 플래그.

이 도구가 **못 하는 것** (한계를 먼저 적는다)
  - 수식(OMML)은 텍스트 근사만 한다 — 아래첨자/위첨자/분수 구조가 평문으로 뭉개진다.
    (`Li6PS5Cl` 의 6/5 가 아래첨자였는지 여기선 알 수 없다. 화학식은 본문 PDF 로 교차확인.)
  - 그림은 뽑지 않는다. SI 그림은 `word/media/*` 에 원본이 들어 있고 캡션과의 짝은
    보장되지 않는다 → `--media <dir>` 로 파일만 덤프하고 번호 매칭은 사람이 한다.
  - 변경이력(track changes)·주석은 무시한다(삭제된 텍스트도 같이 나올 수 있다).
  - .doc(구형 바이너리)은 못 읽는다. .docx(OOXML)만 된다.
  - **xlsx**: 셀 서식을 안 본다 → **날짜 serial 을 날짜로 못 바꾸고**(45000 같은 숫자로 나온다),
    반올림 표시(0.12 로 보이지만 저장값 0.1234)도 **저장값**을 준다. 수식은 캐시된 값만
    읽고 수식 자체는 버린다(캐시가 없으면 빈칸). 차트·피벗·매크로는 무시한다.
    셀 병합은 첫 칸에만 값이 있고 나머지는 빈칸으로 나온다.
  - .xls(구형 바이너리)는 못 읽는다.

usage
  python3 tools/litdb/docx_to_text.py <file.docx>                  # stdout
  python3 tools/litdb/docx_to_text.py <file.docx> -o out.md        # 파일로
  python3 tools/litdb/docx_to_text.py <file.docx> --media dir/     # 임베디드 이미지도 덤프
  python3 tools/litdb/docx_to_text.py --xlsx <file.xlsx>           # Source Data → TSV
  python3 tools/litdb/docx_to_text.py --xlsx <f.xlsx> --sheet "Fig 3d" --max-rows 40
  python3 tools/litdb/docx_to_text.py --xlsx <f.xlsx> --list       # 시트 목록·크기만
  python3 tools/litdb/docx_to_text.py --selftest
"""
import argparse
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


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


# ─────────────────────────── xlsx (Source Data) ───────────────────────────
# xlsx 도 zip+XML 이다. 네임스페이스가 판본마다 달라서 **local-name 으로만** 본다.
def _ln(tag):
    return tag.rsplit("}", 1)[-1]


_CELLREF = re.compile(r"^([A-Z]+)(\d+)$")


def _col_idx(ref):
    """'A1'→0, 'B7'→1, 'AA3'→26. 형식이 이상하면 None."""
    m = _CELLREF.match(ref or "")
    if not m:
        return None
    n = 0
    for ch in m.group(1):
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def _shared_strings(z):
    """sharedStrings.xml → 문자열 풀. 없으면 빈 리스트(정상 — 숫자만 있는 시트)."""
    name = next((n for n in z.namelist() if n.lower().endswith("sharedstrings.xml")), None)
    if not name:
        return []
    out = []
    for si in ET.fromstring(z.read(name)):
        if _ln(si.tag) != "si":
            continue
        out.append("".join(t.text or "" for t in si.iter() if _ln(t.tag) == "t"))
    return out


def _sheet_list(z):
    """[(시트이름, zip 내 경로)] — workbook.xml + rels 로 순서를 지킨다."""
    wb = next((n for n in z.namelist() if n.lower().endswith("xl/workbook.xml")), None)
    if not wb:
        raise ValueError("xl/workbook.xml 이 없다 — .xlsx(OOXML) 가 아니다")
    rels = {}
    rp = wb.rsplit("/", 1)[0] + "/_rels/workbook.xml.rels"
    if rp in z.namelist():
        for rel in ET.fromstring(z.read(rp)):
            rels[rel.get("Id")] = rel.get("Target", "").lstrip("/")
    out = []
    for el in ET.fromstring(z.read(wb)).iter():
        if _ln(el.tag) != "sheet":
            continue
        nm = el.get("name") or f"sheet{len(out)+1}"
        tgt = rels.get(el.get(R_NS + "id"), "")
        if tgt.startswith("xl/"):
            path = tgt
        elif tgt:
            path = "xl/" + tgt
        else:  # rels 가 없거나 깨졌으면 순번으로 추정
            path = f"xl/worksheets/sheet{len(out)+1}.xml"
        out.append((nm, path))
    return out


def _sheet_rows(z, path, shared):
    """워크시트 → [[셀문자열,…],…]. 빈 칸은 ''로 채워 열을 맞춘다."""
    if path not in z.namelist():
        raise ValueError(f"{path}: 워크북이 가리키는 시트가 zip 안에 없다 — 손상된 xlsx")
    rows = []
    for row in ET.fromstring(z.read(path)).iter():
        if _ln(row.tag) != "row":
            continue
        cells = {}
        for c in row:
            if _ln(c.tag) != "c":
                continue
            i = _col_idx(c.get("r"))
            if i is None:
                i = len(cells)
            t = c.get("t")
            val = ""
            if t == "inlineStr":
                val = "".join(x.text or "" for x in c.iter() if _ln(x.tag) == "t")
            else:
                v = next((x for x in c if _ln(x.tag) == "v"), None)
                raw = (v.text or "") if v is not None else ""
                if t == "s":  # sharedStrings 인덱스
                    try:
                        val = shared[int(raw)]
                    except (ValueError, IndexError):
                        # sharedStrings 가 없거나 인덱스가 범위 밖 → 조작하지 말고 표시
                        val = f"<?s{raw}?>"
                else:
                    val = raw
            cells[i] = val.replace("\t", " ").replace("\n", " ").strip()
        if cells:
            n = max(cells) + 1
            rows.append([cells.get(i, "") for i in range(n)])
        else:
            rows.append([])
    return rows


def xlsx_to_text(path, sheet=None, max_rows=0, list_only=False):
    """xlsx → TSV 텍스트. sheet 는 이름 부분일치. max_rows>0 이면 시트마다 잘라낸다."""
    with zipfile.ZipFile(path) as z:
        sheets = _sheet_list(z)
        if not sheets:
            raise ValueError(f"{path}: 시트가 하나도 없다")
        shared = _shared_strings(z)
        out = []
        for nm, sp in sheets:
            if sheet and sheet.lower() not in nm.lower():
                continue
            rows = _sheet_rows(z, sp, shared)
            ncol = max((len(r) for r in rows), default=0)
            out.append(f"## sheet: {nm}\t[{len(rows)} rows x {ncol} cols]")
            if list_only:
                continue
            keep = rows[:max_rows] if max_rows else rows
            for r in keep:
                out.append("\t".join(r))
            if max_rows and len(rows) > max_rows:
                out.append(f"… (+{len(rows)-max_rows} rows 생략)")
            out.append("")
        if len(out) == 0:
            raise ValueError(f"{path}: '{sheet}' 에 맞는 시트가 없다 "
                             f"(있는 것: {', '.join(n for n, _ in sheets)})")
    return "\n".join(out)


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

        # ══════════════════ xlsx ══════════════════
        S = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
        RL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

        def _mk(p, sheets, shared=True, drop_sheet=False):
            """작은 xlsx 를 만든다. sheets = [(name, [[cell,…],…])], 문자열은 shared 로."""
            pool, idx = [], {}
            for _, rows in sheets:
                for r in rows:
                    for v in r:
                        if isinstance(v, str) and v not in idx:
                            idx[v] = len(pool); pool.append(v)
            with zipfile.ZipFile(p, "w") as z:
                z.writestr("xl/workbook.xml",
                           f'<workbook xmlns="{S}" xmlns:r="{RL}"><sheets>' + "".join(
                               f'<sheet name="{n}" sheetId="{i+1}" r:id="rId{i+1}"/>'
                               for i, (n, _) in enumerate(sheets)) + "</sheets></workbook>")
                z.writestr("xl/_rels/workbook.xml.rels",
                           f'<Relationships xmlns="{RL}">' + "".join(
                               f'<Relationship Id="rId{i+1}" Target="worksheets/sheet{i+1}.xml"/>'
                               for i in range(len(sheets))) + "</Relationships>")
                if shared:
                    z.writestr("xl/sharedStrings.xml",
                               f'<sst xmlns="{S}">' + "".join(
                                   f"<si><t>{v}</t></si>" for v in pool) + "</sst>")
                for i, (_, rows) in enumerate(sheets):
                    if drop_sheet:
                        continue
                    body = []
                    for ri, r in enumerate(rows, 1):
                        cs = []
                        for ci, v in enumerate(r):
                            ref = chr(65 + ci) + str(ri)
                            if isinstance(v, str):
                                cs.append(f'<c r="{ref}" t="s"><v>{idx[v]}</v></c>')
                            else:
                                cs.append(f'<c r="{ref}"><v>{v}</v></c>')
                        body.append(f'<row r="{ri}">' + "".join(cs) + "</row>")
                    z.writestr(f"xl/worksheets/sheet{i+1}.xml",
                               f'<worksheet xmlns="{S}"><sheetData>'
                               + "".join(body) + "</sheetData></worksheet>")

        # --- 양성: 시트 2개, 문자열+숫자, 시트 선택
        good = Path(d) / "src.xlsx"
        _mk(good, [("Fig 3d", [["Radius", "g_ij"], [60, 11.8], [72, 11.2]]),
                   ("Fig 6f", [["TM", "ppm"], ["Ni", 0.4]])])
        got = xlsx_to_text(good)
        for need in ("## sheet: Fig 3d", "Radius\tg_ij", "60\t11.8", "## sheet: Fig 6f", "Ni\t0.4"):
            if need not in got:
                print(f"  ✗ xlsx 양성 실패: '{need}' 없음"); ok = False
        one = xlsx_to_text(good, sheet="6f")
        if "Fig 3d" in one or "Ni\t0.4" not in one:
            print("  ✗ xlsx 양성 실패: --sheet 필터가 안 먹는다"); ok = False
        cut = xlsx_to_text(good, sheet="3d", max_rows=2)
        if "72\t11.2" in cut or "+1 rows 생략" not in cut:
            print("  ✗ xlsx 양성 실패: --max-rows 가 안 먹는다"); ok = False
        if ok:
            print("  ✓ xlsx 양성: 시트·문자열풀·숫자·필터·행제한")

        # --- 음성 ④: workbook.xml 없는 zip → ValueError
        b4 = Path(d) / "nowb.xlsx"
        with zipfile.ZipFile(b4, "w") as z:
            z.writestr("hello.txt", "nope")
        try:
            xlsx_to_text(b4)
            print("  ✗ 음성④ 실패: workbook.xml 없는 zip 을 통과시켰다"); ok = False
        except ValueError:
            print("  ✓ 음성④: workbook.xml 없는 zip 을 거부")

        # --- 음성 ⑤: zip 이 아님(.xls 흉내) → BadZipFile
        b5 = Path(d) / "old.xls"
        b5.write_bytes(b"\xd0\xcf\x11\xe0binary junk")
        try:
            xlsx_to_text(b5)
            print("  ✗ 음성⑤ 실패: 비-zip(.xls) 을 통과시켰다"); ok = False
        except (zipfile.BadZipFile, ValueError):
            print("  ✓ 음성⑤: 비-zip(.xls) 을 거부")

        # --- 음성 ⑥: sharedStrings 가 없는데 t="s" → **조용히 숫자만 내지 말고** 표시해야 한다
        b6 = Path(d) / "noss.xlsx"
        _mk(b6, [("S", [["label"], [3.14]])], shared=False)
        got6 = xlsx_to_text(b6)
        if "<?s0?>" not in got6 or "3.14" not in got6:
            print("  ✗ 음성⑥ 실패: sharedStrings 없을 때 문자열 손실을 안 알린다"); ok = False
        else:
            print("  ✓ 음성⑥: sharedStrings 없는 xlsx — 숫자는 살리고 문자열 손실을 표시")

        # --- 음성 ⑦: 워크북이 가리키는 시트 파일이 없음 → ValueError
        b7 = Path(d) / "ghost.xlsx"
        _mk(b7, [("Ghost", [["a", 1]])], drop_sheet=True)
        try:
            xlsx_to_text(b7)
            print("  ✗ 음성⑦ 실패: 시트 파일 없는 xlsx 를 통과시켰다"); ok = False
        except ValueError:
            print("  ✓ 음성⑦: 워크북이 가리키는 시트가 없으면 거부")

        # --- 음성 ⑧: 없는 시트 이름 → ValueError (조용히 빈 출력 금지)
        try:
            xlsx_to_text(good, sheet="Fig 99z")
            print("  ✗ 음성⑧ 실패: 없는 시트 이름에 빈 출력을 냈다"); ok = False
        except ValueError:
            print("  ✓ 음성⑧: 없는 시트 이름을 거부")
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("docx", nargs="?", help=".docx 경로 (--xlsx 면 .xlsx 경로)")
    ap.add_argument("-o", "--out", help="출력 파일 (없으면 stdout)")
    ap.add_argument("--media", help="임베디드 이미지 덤프 디렉터리")
    ap.add_argument("--xlsx", action="store_true",
                    help=".xlsx(Source Data)로 읽는다 → 시트별 TSV")
    ap.add_argument("--sheet", help="--xlsx: 이 문자열이 든 시트만 (부분일치)")
    ap.add_argument("--max-rows", type=int, default=0,
                    help="--xlsx: 시트마다 앞 N 행만")
    ap.add_argument("--list", action="store_true",
                    help="--xlsx: 시트 이름·크기만 (값은 안 찍는다)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if not a.docx:
        ap.error("파일 경로가 필요하다 (또는 --selftest)")
    if a.xlsx:
        txt = xlsx_to_text(a.docx, sheet=a.sheet, max_rows=a.max_rows, list_only=a.list)
        if a.out:
            Path(a.out).write_text(txt, encoding="utf-8")
            print(f"[ok] {len(txt)} chars → {a.out}", file=sys.stderr)
        else:
            sys.stdout.write(txt)
        return 0
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
