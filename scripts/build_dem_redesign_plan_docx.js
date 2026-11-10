#!/usr/bin/env node
'use strict';
/*
 * DEM 재설계 계획서 (처음 보는 분을 위한 설명) docx 빌더.
 *
 *   node scripts/build_dem_redesign_plan_docx.js --out <쓸 파일.docx> [--json <모델.json>] [--root <리포 루트>]
 *
 * 읽는 것 = docs/reviews/dem_redesign_direction_20261109/plan_newcomer_docx_model.json
 *   (python3 scripts/build_dem_redesign_plan.py --write 가 원고 plan_newcomer_ko.md 에서 만든다 · 손으로 고치지 않는다).
 * 내는 꼴 = 1저자가 2026-11-10 에 올려 받아들인 docx (정본 · 같은 폴더의 DEM_redesign_plan_for_newcomers_20261110.docx):
 *   A4 · 맑은 고딕 + Calibri 10.5 pt · 제목 블록 네 줄 · "지위" 문단 · "한 줄로" 상자 · Heading 1 · 글머리 / 번호 목록 ·
 *   머리 행 음영 표 (열 너비 · 쪽 붙임은 JSON 이 싣는다) · 표 뒤 빈 문단 · 바닥글 쪽 번호.
 *
 * 수식 · 그림 (1저자 11-10 "docx에 MPM에 대한 설명, 지배방정식등을 이런식으로 그림으로도 표현해서 넣어줘"):
 *   - 수식은 Word 수식 (OMML) 으로 들어간다.  LaTeX → OMML 변환은 생성기가 pandoc 으로 해서 JSON 에 실어 둔다
 *     (런의 {math: "<m:oMath>…"} · 블록 {t: "eq", omml: "<m:oMathPara>…"}).  이 빌더는 pandoc 을 부르지 않는다:
 *     docx 모듈로 문서를 만들 때 수식 자리에 표지 글 한 런을 두고, 다 만든 뒤 word/document.xml 에서 그 런을 OMML 로 바꾼다
 *     (OMML 은 pandoc 이 낸 바이트 그대로 · 문서 뿌리에 m: 네임스페이스가 이미 있다).
 *   - 그림 ({t: "fig", path, sha256, width, height, alt, caption}) 은 본문 가운데에 놓고 캡션을 그 아래 가운데에 둔다.
 *     크기 (px) 는 생성기가 정한다: 폭을 적지 않은 그림은 본문 폭 (601 px) · {width=NN%} 는 그 몫 · 키는 한 쪽에 들어가게.
 *     파일은 --root (기본 = 리포 루트) 아래 path 에서 읽고, sha256 이 JSON 과 다르면 멈춘다.
 *   - 글 안 수식이 든 문단에는 줄 간격 규칙 "auto" 를 적는다 (뜻은 적지 않을 때와 같다 · LibreOffice 가 키 큰 수식에 줄을 늘리게).
 *   수식 · 그림이 없는 원고에서는 이 길을 타지 않아 출력이 정본과 같다.
 *   알아 둘 것 (2026-11-10 · LibreOffice 24.2 로 PDF 를 떠서 본 것): 식 번호 \tag{1} 은 식 끝의 글자 "(1)" 로 들어가는데
 *   LibreOffice 는 그것을 "\(1\)" 로 그리고, 굵은 벡터 (\mathbf) 를 보통 굵기로 그린다.  pandoc 이 직접 만든 docx 도 똑같이
 *   보이므로 LibreOffice 의 OMML 읽개 탓으로 본다.  Word 에서의 모습은 이 리포의 기계에서 확인하지 못했다.
 *
 * 정본은 올린 파일 그대로 리포에 있다 (시험이 sha256 을 고정한다).  이 빌더의 출력은 커밋하지 않는다: 만든 시각이
 * 들어가 바이트가 매번 다르다.  대신 시험 webapp/test_dem_redesign_plan_page.py 가 (node 와 docx 모듈이 있을 때) 이 빌더를
 * 돌려 문단 글 · 순서를 정본과 견주고, docx 모듈이 정본을 만든 판 (9.7.1) 이면 본문 · 스타일 · 번호 · 바닥글 · 설정 XML 이
 * 요소 · 속성까지 같은지 본다 (2026-11-10 확인: 그 판에서 이 다섯 XML 은 정본과 바이트까지 같았다 · 다른 것은 만든 시각과
 * ZIP 의 폴더 항목뿐).
 *
 * 원고가 바뀌면 (정본을 바꾸는 절차):
 *   1. python3 scripts/build_dem_redesign_plan.py --write           JSON 과 웹 페이지 둘을 다시 만든다
 *                                                                   (새 수식이 있으면 pandoc 이 있는 기계에서)
 *   2. node scripts/build_dem_redesign_plan_docx.js --out <임시>.docx
 *   3. <임시>.docx 를 PDF 로 바꿔 쪽 넘김 · 표 · 수식 · 그림을 눈으로 본다 (표가 쪽 끝에서 갈리면 JSON 의 keep 규칙 =
 *      생성기의 NEWCOMER_TABLES 를 고친다)
 *   4. <임시>.docx 를 정본 자리에 복사하고 시험의 DOCX_SHA256 을 새 sha256 으로, SHAPE 묶음 (절 · 표 · 용어 · 참고문헌 ·
 *      정본 문단 수) 을 새 원고의 수로 바꾼다 (제목 블록 · 첫 문장을 못 박은 검사도 글이 바뀌었으면 같이)

 *   5. python3 webapp/test_dem_redesign_plan_page.py 통과를 보고 1저자에게 새 정본을 알린다
 *
 * --out 없이는 아무것도 쓰지 않는다 (rc 2): 정본을 실수로 덮지 않기 위해서다.
 * 출력 ZIP 에서는 폴더 항목을 뺀다 (Word 가 클라우드 공동 편집에서 그런 파일을 거부한 적이 있다).
 */
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const REPO_ROOT = path.join(__dirname, '..');
const DEFAULT_JSON = path.join(REPO_ROOT, 'docs', 'reviews', 'dem_redesign_direction_20261109',
  'plan_newcomer_docx_model.json');
const SCHEMA = 'dem_redesign_plan_docx/1';
// 수식 자리 표지 (다 만든 뒤 OMML 로 바뀐다).  원고 글에 이 글자열이 있으면 멈춘다.
const OMML_MARK = '@@DEMPLAN_OMML_';
const ommlToken = (n) => OMML_MARK + n + '@@';

// 형식 기준 docx 의 값 (색 = 16 진 · 크기 = 반 포인트 · 길이 = DXA)
const INK = '1F2933';
const ACC = '1F4E79';
const MUT = '5B6770';
const LINE = 'B8C4CE';
const TH_FILL = 'E6EDF3';
const BOX_FILL = 'EAF2FA';
const FONT = { ascii: 'Calibri', cs: 'Calibri', eastAsia: 'Malgun Gothic', hAnsi: 'Calibri' };
const MONO = { ascii: 'Consolas', cs: 'Consolas', eastAsia: 'Malgun Gothic', hAnsi: 'Consolas' };
const PAGE = { width: 11906, height: 16838, top: 1440, right: 1440, bottom: 1300, left: 1440 };

function die(msg) {
  process.stderr.write('✗ ' + msg + '\n');
  process.stderr.write('  사용법: node scripts/build_dem_redesign_plan_docx.js --out <쓸 파일.docx> [--json <모델.json>]'
    + ' [--root <리포 루트>]\n');
  process.exit(2);
}

function parseArgs(argv) {
  const out = { json: DEFAULT_JSON, out: null, root: REPO_ROOT };
  for (let i = 0; i < argv.length; i += 1) {
    const a = argv[i];
    if ((a === '--out' || a === '--json' || a === '--root') && i + 1 < argv.length) {
      out[a.slice(2)] = argv[i + 1];
      i += 1;
    } else {
      die('모르는 인자: ' + a);
    }
  }
  if (!out.out) {
    die('--out 이 없다 (정본을 실수로 덮지 않게, 쓸 자리를 늘 적는다)');
  }
  return out;
}

// 그림 파일을 읽는다 (리포 루트 아래 상대 경로만 · sha256 이 모델과 같아야 한다)
function readFigure(root, b) {
  const parts = String(b.path).split('/');
  if (!b.path || path.isAbsolute(b.path) || parts.includes('..') || parts.includes('')) {
    throw new Error('그림 경로를 받을 수 없다: ' + b.path);
  }
  const data = fs.readFileSync(path.join(root, ...parts));
  const sha = crypto.createHash('sha256').update(data).digest('hex');
  if (sha !== b.sha256) {
    throw new Error('그림 파일이 모델과 다르다 (sha256): ' + b.path + ' → 생성기 --write 를 다시 돌릴 것');
  }
  return data;
}

function build(model, docx, root) {
  const {
    AlignmentType, BorderStyle, Document, Footer, HeadingLevel, ImageRun, LevelFormat, LineRuleType, PageNumber,
    Paragraph, ShadingType, Table, TableCell, TableLayoutType, TableRow, TextRun, WidthType,
  } = docx;
  const ommls = [];     // 수식 자리 n 번에 들어갈 OMML

  function mathRun(omml) {
    if (typeof omml !== 'string' || !/^<m:oMath(Para)?>/.test(omml)) {
      throw new Error('수식 (OMML) 의 꼴이 다르다');
    }
    ommls.push(omml);
    return new TextRun({ text: ommlToken(ommls.length - 1), font: FONT });
  }

  // 런: JSON 의 {text, b, i, code} 또는 {math} + 그 자리의 글자 속성 (색 · 크기 · 굵기)
  function runs(list, props) {
    return list.map((r) => {
      if (r.math !== undefined) {
        return mathRun(r.math);
      }
      if (String(r.text).includes(OMML_MARK)) {
        throw new Error('원고 글에 수식 자리 표지와 같은 글자열이 있다: ' + OMML_MARK);
      }
      const o = Object.assign({ text: r.text, font: r.code ? MONO : FONT }, props || {});
      if (r.b) {
        o.bold = true;
      }
      if (r.i) {
        o.italics = true;
      }
      return new TextRun(o);
    });
  }
  const one = (text, props) => [new TextRun(Object.assign({ text, font: FONT }, props))];
  // 글 안 수식이 든 문단은 줄 간격 규칙 "auto" 를 적어 둔다.  뜻은 적지 않을 때와 같다 (배수 간격) · 적지 않으면 LibreOffice 가
  // 키 큰 수식 (분수 · 합 기호) 에 맞춰 줄을 늘리지 않아 윗줄과 겹친다 (2026-11-10 그림으로 확인).  수식이 없는 문단에는
  // 적지 않는다 = 정본과 같은 XML.
  const hasMath = (list) => list.some((r) => r.math !== undefined);
  const spacingFor = (sp, list) => (hasMath(list) ? Object.assign({}, sp, { lineRule: LineRuleType.AUTO }) : sp);

  const children = [];

  // ── 제목 블록 네 줄 ──
  children.push(new Paragraph({
    spacing: { after: 60, before: 0 },
    children: one(model.title, { bold: true, color: ACC, size: 44 }),
  }));
  children.push(new Paragraph({
    spacing: { after: 60, before: 0 },
    children: one(model.subtitle, { color: INK, size: 26 }),
  }));
  children.push(new Paragraph({
    spacing: { after: 60, before: 0 },
    children: one(model.audience, { color: MUT, size: 20 }),
  }));
  children.push(new Paragraph({
    border: { bottom: { color: ACC, space: 6, style: BorderStyle.SINGLE, size: 12 } },
    spacing: { after: 200, before: 0 },
    children: one(model.status_line, { color: MUT, size: 18 }),
  }));

  // ── "지위" 문단 · "한 줄로" 상자 ──
  model.lead.forEach((lead) => {
    if (lead.kind === 'status') {
      children.push(new Paragraph({
        spacing: spacingFor({ after: 160, before: 0, line: 290 }, lead.runs),
        children: runs(lead.runs, { color: MUT, size: 18 }),
      }));
    } else if (lead.kind === 'oneline') {
      children.push(new Paragraph({
        border: { left: { color: ACC, space: 8, style: BorderStyle.SINGLE, size: 24 } },
        shading: { fill: BOX_FILL, type: ShadingType.CLEAR, color: 'auto' },
        spacing: spacingFor({ after: 160, before: 120, line: 320 }, lead.runs),
        indent: { left: 160, right: 160 },
        children: runs(lead.runs, { color: INK, size: 22 }),
      }));
    } else {
      throw new Error('모르는 lead.kind: ' + lead.kind);
    }
  });

  // ── 본문 ──
  const cellBorder = { style: BorderStyle.SINGLE, size: 4, color: LINE };
  function table(b) {
    const nrow = b.rows.length;
    if (b.widths.reduce((s, w) => s + w, 0) !== model.text_width) {
      throw new Error('표의 열 너비 합이 본문 너비 ' + model.text_width + ' 가 아니다');
    }
    return new Table({
      width: { size: model.text_width, type: WidthType.DXA },
      layout: TableLayoutType.FIXED,
      columnWidths: b.widths,
      rows: b.rows.map((row, ri) => {
        if (row.length !== b.widths.length) {
          throw new Error('표 줄의 칸 수가 열 너비 수와 다르다');
        }
        const head = ri === 0;
        return new TableRow({
          cantSplit: true,
          tableHeader: head,
          children: row.map((cell, ci) => {
            const para = { spacing: spacingFor({ after: 0, before: 0, line: 276 }, cell) };
            if (b.keep && ri < nrow - 1) {
              para.keepNext = true;     // 표를 한 쪽에 붙여 둔다 (끝 줄만 빼고 다음 줄과 붙임)
            }
            const props = { color: INK, size: 18 };
            if (head) {
              props.bold = true;
            }
            para.children = runs(cell, props);
            const tc = {
              width: { size: b.widths[ci], type: WidthType.DXA },
              borders: { top: cellBorder, left: cellBorder, bottom: cellBorder, right: cellBorder },
              margins: { top: 70, left: 100, bottom: 70, right: 100 },
              children: [new Paragraph(para)],
            };
            if (head) {
              tc.shading = { fill: TH_FILL, type: ShadingType.CLEAR, color: 'auto' };
            }
            return new TableCell(tc);
          }),
        });
      }),
    });
  }

  model.blocks.forEach((b) => {
    if (b.t === 'h1') {
      const p = { heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: b.text, font: FONT })] };
      if (b.pageBreakBefore) {
        p.pageBreakBefore = true;
      }
      children.push(new Paragraph(p));
    } else if (b.t === 'p') {
      const p = { spacing: spacingFor({ after: 130, before: 0, line: 312 }, b.runs), children: runs(b.runs, { color: INK }) };
      if (b.keepNext) {
        p.keepNext = true;
      }
      children.push(new Paragraph(p));
    } else if (b.t === 'li') {
      children.push(new Paragraph({
        numbering: { reference: 'bullets', level: b.level },
        spacing: spacingFor({ after: 70, before: 0, line: 312 }, b.runs),
        children: runs(b.runs, { color: INK }),
      }));
    } else if (b.t === 'ol') {
      children.push(new Paragraph({
        numbering: { reference: 'numbers', level: 0 },
        spacing: spacingFor({ after: 90, before: 0, line: 312 }, b.runs),
        children: runs(b.runs, { color: INK }),
      }));
    } else if (b.t === 'table') {
      children.push(table(b));
      children.push(new Paragraph({ spacing: { after: 120, before: 0 } }));
    } else if (b.t === 'eq') {
      // 줄 수식: 문단 하나에 OMML (m:oMathPara · 가운데 맞춤은 OMML 이 싣는다)
      children.push(new Paragraph({ spacing: { after: 130, before: 60 }, children: [mathRun(b.omml)] }));
    } else if (b.t === 'fig') {
      const cap = b.caption && b.caption.length > 0;
      const alt = b.alt || path.basename(b.path);     // 대체 글 = 캡션 글 (수식은 LaTeX 글 그대로 · 생성기가 싣는다)
      children.push(new Paragraph({
        alignment: AlignmentType.CENTER,
        keepNext: cap ? true : undefined,
        spacing: { after: cap ? 60 : 160, before: 120 },
        children: [new ImageRun({
          type: 'png',
          data: readFigure(root, b),
          transformation: { width: b.width, height: b.height },
          altText: { title: alt, description: alt, name: path.basename(b.path) },
        })],
      }));
      if (cap) {
        children.push(new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: spacingFor({ after: 160, before: 0, line: 290 }, b.caption),
          children: runs(b.caption, { color: MUT, size: 18 }),
        }));
      }
    } else {
      throw new Error('모르는 블록: ' + b.t);
    }
  });

  const footer = new Footer({
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({
        font: FONT,
        color: MUT,
        size: 16,
        children: [model.footer + '  ·  ', PageNumber.CURRENT, ' / ', PageNumber.TOTAL_PAGES],
      })],
    })],
  });

  const doc = new Document({
    title: model.title,
    creator: model.creator,
    description: model.audience,
    styles: {
      default: {
        document: { run: { font: FONT, color: INK, size: 21 } },
        heading1: {
          run: { font: FONT, bold: true, color: ACC, size: 28 },
          paragraph: { keepNext: true, spacing: { after: 140, before: 360 } },
        },
        heading2: {
          run: { font: FONT, bold: true, color: INK, size: 24 },
          paragraph: { keepNext: true, spacing: { after: 100, before: 240 } },
        },
      },
    },
    numbering: {
      config: [
        {
          reference: 'bullets',
          levels: [
            {
              level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
              style: { paragraph: { indent: { left: 420, hanging: 240 } } },
            },
            {
              level: 1, format: LevelFormat.BULLET, text: '–', alignment: AlignmentType.LEFT,
              style: { paragraph: { indent: { left: 840, hanging: 240 } } },
            },
          ],
        },
        {
          reference: 'numbers',
          levels: [
            {
              level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT,
              style: { paragraph: { indent: { left: 420, hanging: 320 } } },
            },
          ],
        },
      ],
    },
    sections: [{
      properties: {
        page: {
          size: { width: PAGE.width, height: PAGE.height },
          margin: { top: PAGE.top, right: PAGE.right, bottom: PAGE.bottom, left: PAGE.left },
        },
      },
      footers: { default: footer },
      children,
    }],
  });
  return { doc, ommls };
}

// word/document.xml 의 수식 자리 (표지 글 한 런) 를 OMML 로 바꾼다.  자리마다 정확히 한 번 있어야 한다.
function spliceOmml(xml, ommls) {
  let out = xml;
  ommls.forEach((omml, n) => {
    const tok = ommlToken(n);
    const at = out.indexOf(tok);
    if (at < 0 || out.indexOf(tok, at + tok.length) >= 0) {
      throw new Error('수식 자리 ' + n + ' 를 문서에서 찾을 수 없다 (또는 둘 이상이다)');
    }
    const start = out.lastIndexOf('<w:r>', at);
    const end = out.indexOf('</w:r>', at);
    if (start < 0 || end < 0 || out.slice(start, at).includes('</w:r>')) {
      throw new Error('수식 자리 ' + n + ' 를 감싼 런을 찾을 수 없다');
    }
    out = out.slice(0, start) + omml + out.slice(end + '</w:r>'.length);
  });
  if (out.includes(OMML_MARK)) {
    throw new Error('수식 자리 표지가 문서에 남았다');
  }
  return out;
}

// ZIP 을 다시 싼다: 폴더 항목 ("word/" 등) 을 빼고, 수식 자리를 OMML 로 바꾼다.  docx 모듈이 쓰는 jszip 을 빌려 쓴다.
async function repack(buf, ommls) {
  let JSZip;
  try {
    JSZip = require(require.resolve('jszip', { paths: [path.dirname(require.resolve('docx'))] }));
  } catch (e) {
    if (ommls.length) {
      throw new Error('jszip 을 찾지 못해 수식을 넣을 수 없다');
    }
    process.stderr.write('  (jszip 을 찾지 못해 ZIP 의 폴더 항목을 그대로 둔다)\n');
    return buf;
  }
  const zin = await JSZip.loadAsync(buf);
  const zout = new JSZip();
  for (const name of Object.keys(zin.files)) {
    const f = zin.files[name];
    if (f.dir) {
      continue;
    }
    if (name === 'word/document.xml' && ommls.length) {
      zout.file(name, spliceOmml(await f.async('string'), ommls), { createFolders: false, date: f.date });
    } else {
      zout.file(name, await f.async('nodebuffer'), { createFolders: false, date: f.date });
    }
  }
  return zout.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE' });
}

// 설치된 docx 모듈의 판 (package.json 은 exports 에 막혀 require 로 못 읽어 파일로 읽는다).  못 읽으면 "?".
function docxVersion() {
  try {
    const pkg = path.join(path.dirname(require.resolve('docx')), '..', 'package.json');
    return JSON.parse(fs.readFileSync(pkg, 'utf8')).version;
  } catch (e) {
    return '?';
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  let docx;
  try {
    docx = require('docx');
  } catch (e) {
    die('docx 모듈 (npm) 을 찾을 수 없다');
  }
  let model;
  try {
    model = JSON.parse(fs.readFileSync(args.json, 'utf8'));
  } catch (e) {
    die('모델 JSON 을 읽을 수 없다: ' + e.message);
  }
  if (model.schema !== SCHEMA) {
    die('모델 JSON 의 schema 가 ' + SCHEMA + ' 가 아니다');
  }
  const built = build(model, docx, args.root);
  const buf = await repack(await docx.Packer.toBuffer(built.doc), built.ommls);
  fs.writeFileSync(args.out, buf);
  process.stdout.write('  쓴 파일 ' + args.out + ' (' + buf.length + ' B) · 원고 ' + model.source + ' sha256 '
    + String(model.source_sha256).slice(0, 16) + ' · 수식 ' + built.ommls.length + ' · docx 모듈 ' + docxVersion() + '\n');
}

main().catch((e) => {
  process.stderr.write('✗ ' + (e && e.message ? e.message : String(e)) + '\n');
  process.exit(1);
});
