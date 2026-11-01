#!/usr/bin/env python3
"""50kg/batch 4차년도 DEM 보고 — 초안 3 (회사 보고판 · 0쪽 + 1–7쪽 + 부록 = 9 장) 생성기.

    python3 -P docs/50kg/report_y4/build_kg50_report_y4_draft3.py                 # 덱 → 검사 (렌더 없음)
    python3 -P docs/50kg/report_y4/build_kg50_report_y4_draft3.py --render        # + LibreOffice PDF · 쪽 PNG · 렌더 검사
    python3 -P docs/50kg/report_y4/build_kg50_report_y4_draft3.py --determinism   # 임시 폴더에 두 번 만들어 바이트 대조
    python3 -P docs/50kg/report_y4/build_kg50_report_y4_draft3.py --selftest      # 검사기 변이 시험 (덱을 하나씩 망가뜨려 검사가 걸리는지)
    python3 -P docs/50kg/report_y4/build_kg50_report_y4_draft3.py --measure       # 패널마다 쌓은 높이 · 넘침 표 (덱 안 씀)
    python3 -P docs/50kg/report_y4/build_kg50_report_y4_draft3.py --check-only <deck.pptx> [--pdf <deck.pdf>]

- 글 = 글 시트 `docs/50kg/report_y4/draft2/slide_text_draft3.md` (1저자 비준 쪽 계획 11-01) 를 빌드 때 읽는다 — 손으로 옮긴 글 없음.
  쪽마다: ② 머리 메시지 = 머리의 쪽 제목 자리 · ③ 보충 한 줄 = 요약 띠 · ① 탭 글 = 점선 패널 괄호 탭 · ④ 글머리 · 캡션 · 표 = 패널 안 ·
  ⑤ 회색 결론 줄 = 패널 아래 회색 줄 · ⑥ 화면 각주 = 쪽 아래 작은 글 · ⑥ 발표자 노트 + ⑦ 하지 않을 말 = 노트 (화면에 안 씀).
  시트 글에서 바꾸는 것 = 줄바꿈 · markdown 표기 (` · **) 떼기 · `x_y` 아래첨자 표기를 아래첨자 글자로 (c_cpl[22] 같은 이름은 그대로) ·
  캡션의 【 】 (양식) — 검사 V 가 화면 글을 시트 글과 한 글자씩 대조한다 (아래첨자 → `_` 로 되돌려서).
- 양식 = 초안 1 생성기 (`build_kg50_report_y4.py`) 의 상수 · 그리기 도우미 · 결정적 저장 · 검사 함수를 import 해서 그대로 쓴다
  (초안 1 생성기는 고치지 않는다).  바꾼 자리 (README §3): 요약 띠 = 한 줄 메시지용 낮은 띠 (알약 · ① ② 항목 없음 · 같은 회색 틀 + 흰 틀) ·
  패널 위 = 띠 아래 같은 간격 · 패널 바닥 · 회색 결론 줄 = 두 패널 폭 · 화면 각주 자리 · 쪽 번호 자리 = 글 (0–7 · 부록).
  글 폭 추정 = 초안 1 추정 + 괄호 둘레 자동 간격 (seq_widths3 · 이 프로세스 안에서만 바꿔 씀).
- 그림 = 전부 100 % (크기 = `draft2/figs/figs_meta.json` · 0쪽 = PNG 픽셀 ÷ 300 dpi) · 바이트 = meta sha256 — 패널에 100 % 로 안 들어가면
  줄이지 않고 그대로 두고 검사 · 넘침 보고 (overflow) 로 알린다 (1저자 결정).  글이 넘쳐도 줄이거나 빼지 않는다.
- 0쪽 식 넷 = 시트 ④-2 표의 글 그대로 (글 상자 · OMML 아님 — README §6: 시트 식 넷이 모두 OMML 로 있는 리포 파일이 없다 ·
  세미나 3장 OMML (Codex 증거) · 10-21 보고 덱 9 장 OMML 은 넷 중 일부만 시트 꼴과 같다).
"""
import argparse
import contextlib
import datetime as _dt
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_kg50_report_y4 as d1  # noqa: E402  초안 1 생성기 — 양식 상수 · 그리기 · 저장 · 검사 함수 (동작 무변경)
import kg50_y4_sources as src  # noqa: E402

I, inch = d1.I, d1.inch
SHEET = 'docs/50kg/report_y4/draft2/slide_text_draft3.md'
OUT_DIR = HERE / 'draft3'
OUT_DECK = OUT_DIR / 'kg50_report_y4_draft3.pptx'
OUT_CHECKS = OUT_DIR / 'checks_draft3.json'
RENDER_DIR = OUT_DIR / 'render'
FIG2_DIR = HERE / 'draft2' / 'figs'
FIG2_META = FIG2_DIR / 'figs_meta.json'
P0_DIR = HERE / 'figs' / 'p0_dem_method'
P0_META = P0_DIR / 'p0_figs_meta.json'
P0_DPI = 300
PAGES = ('0', '1', '2', '3', '4', '5', '6', '7', '부록')
N_PAGES = len(PAGES)
#: 쪽 번호 자리의 글 = 시트의 쪽 이름 (0–7 · 부록) — 글로 쓴다 (LibreOffice 는 firstSlideNum 을 무시해 번호 필드가 1 부터 나온다)
PAGE_LABEL = {k: k for k in PAGES}


# ───────────────────────────── 글 폭 추정 (초안 1 추정 + 괄호 둘레 자동 간격) ─────────────────────────────

BRACKETS = set('()[]')


def seq_widths3(chars):
    """초안 1 seq_widths 와 같고, 괄호 ( ) [ ] 도 영문으로 쳐서 한글 ↔ 괄호 경계에 자동 간격 0.25 em 을 더한다.
    실측 (11-01 렌더): LibreOffice 는 '(관측)' · '(면적 + 협착 규약)' 의 괄호 안팎에 아시아 자동 간격을 넣는다 → 초안 1 추정이
    3쪽 제목 상자 폭 · 6쪽 표 줄 수를 작게 잡았다 (렌더 검사 R4 · R5)."""
    out, prev = [], None
    for c, pt, b in chars:
        if d1._cjk(c):
            w, scr = pt, 'A'
        elif c in d1._AMBIG:
            w, scr = pt, None
        else:
            em = d1.SUPSUB_EM if 0x2070 <= ord(c) <= 0x209F else d1._latin_em(c)
            w = em * pt * (d1.BOLD_K if b else 1.0)
            scr = 'L' if (c.isalnum() or c in BRACKETS) else None
        if scr and prev and scr != prev:
            w += d1.AUTOSPACE * pt
        if scr:
            prev = scr
        out.append(w)
    return out


@contextlib.contextmanager
def estimator3():
    """이 생성기 프로세스 안에서만 초안 1 모듈의 seq_widths 를 seq_widths3 로 바꿔 쓴다 (빠져나오면 되돌림 · 초안 1 파일 · 실행은 그대로)."""
    old = d1.seq_widths
    d1.seq_widths = seq_widths3
    try:
        yield
    finally:
        d1.seq_widths = old


# ───────────────────────────── 초안 3 배치 (초안 1 양식 상수에서 유도 · EMU) ─────────────────────────────
BAND_X, BAND_Y, BAND_W = d1.BAND_OUT[0], d1.BAND_OUT[1], d1.BAND_OUT[2]
IN_X, IN_Y, IN_W = d1.BAND_IN[0], d1.BAND_IN[1], d1.BAND_IN[2]
IN_BOT_GAP = (d1.BAND_OUT[1] + d1.BAND_OUT[3]) - (d1.BAND_IN[1] + d1.BAND_IN[3])   # 흰 틀 아래 ↔ 회색 틀 아래 (양식)
R_OUT = d1.BAND_OUT[4] * d1.BAND_OUT[3]                  # 회색 틀 모서리 반지름 (양식 그대로 · 높이가 바뀌어도 같은 반지름)
R_IN = d1.BAND_IN[4] * d1.BAND_IN[3]
TAB_GAP = d1.PANEL_TAB_Y - (d1.BAND_OUT[1] + d1.BAND_OUT[3])   # 띠 아래 ↔ 패널 탭 위 (양식)
PANEL_DY = d1.PANEL[0][1] - d1.PANEL_TAB_Y                # 탭 위 ↔ 패널 위 (양식)
BAND3_H = 0.70                                            # 회색 띠 높이 (in) — ③ 보충 한 줄 두 줄 (11 pt) 자리 · 9 장 같은 높이
PANEL3_BOTTOM = 6.84                                      # 패널 바닥 (in · 초안 1 = 6.97 · 화면 각주 자리)
NOTE3_H = 0.22
FOOT3_Y, FOOT3_H = 7.10, 0.38
BAND_PT, TITLE_PT, HEAD_PT, BELOW_PT, CAP_PT, NOTE_PT, FOOT_PT = 11, 14, 10, 8, 7, 9, 7
TBL_PT = d1.TBL_PT
#: 아래첨자로 바꾸지 않는 이름 (코드 · 덤프 열 이름)
NO_SUB = ('c_cpl[22]',)


def band_bottom():
    return BAND_Y + I(BAND3_H)


def tab_y():
    return band_bottom() + TAB_GAP


def panel_y():
    return tab_y() + PANEL_DY


def content_top():
    return inch(tab_y() + d1.PANEL_TAB_H) + 0.03


def note_box():
    x0 = inch(d1.PANEL[0][0])
    x1 = inch(d1.PANEL[1][0] + d1.PANEL[2])
    return (x0, PANEL3_BOTTOM + 0.035, x1 - x0, NOTE3_H)


def foot_box():
    x0 = inch(d1.PANEL[0][0])
    return (x0, FOOT3_Y, inch(d1.SLDNUM[0]) - 0.05 - x0, FOOT3_H)


# ───────────────────────────── 글 시트 읽기 (빌드 때 · 구조가 다르면 멈춤) ─────────────────────────────

BLOCK_RE = re.compile(r'\*\*([①②③④⑤⑥⑦])[^*]*\*\*')


def read_sheet(rel=SHEET):
    text = src.rp(rel).read_text(encoding='utf-8')
    lines = text.split('\n')
    secs, cur = {}, None
    for no, ln in enumerate(lines, 1):
        if ln.startswith('## '):
            m = re.fullmatch(r'## (?:(\d)쪽|(부록)) — (.+)', ln)
            cur = (m.group(1) or m.group(2)) if m else None
            if cur is not None:
                src.need(cur not in secs, f'sheet: 쪽 {cur} 절이 둘')
                secs[cur] = dict(heading=m.group(3), line=no, lines=[])
            continue
        if cur is not None:
            if ln.strip() == '---':
                cur = None
            else:
                secs[cur]['lines'].append((no, ln))
    src.need(tuple(secs) == PAGES, f'sheet: 쪽 절 = {tuple(secs)} (기대 {PAGES})')
    for k, s in secs.items():
        blocks, cur = {}, None
        for no, ln in s['lines']:
            m = BLOCK_RE.fullmatch(ln.strip())
            if m:
                cur = m.group(1)
                src.need(cur not in blocks, f'sheet {k}쪽: 블록 {cur} 이 둘')
                blocks[cur] = []
                continue
            if cur is not None:
                blocks[cur].append((no, ln))
        src.need(set(blocks) == set('①②③④⑤⑥⑦'), f'sheet {k}쪽: 블록 {sorted(blocks)}')
        s['blocks'] = blocks
    return dict(text=text, sha256=hashlib.sha256(text.encode('utf-8')).hexdigest(), secs=secs)


def _find(lines, pat, start=0, what=''):
    rx = re.compile(pat)
    for i in range(start, len(lines)):
        if rx.search(lines[i][1]):
            return i
    raise src.SourceError(f'sheet: "{pat}" 를 찾지 못했다 ({what})')


def _bq(lines, start, what):
    """start 이후 첫 인용 줄 ('> ') — 한 줄이어야 한다.  → (글, 줄 번호, 다음 위치)"""
    for i in range(start, len(lines)):
        no, ln = lines[i]
        if ln.startswith('>'):
            src.need(ln.startswith('> '), f'sheet {no}: 인용 줄 꼴 ({what})')
            src.need(i + 1 >= len(lines) or not lines[i + 1][1].startswith('>'), f'sheet {no}: 인용이 여러 줄 ({what})')
            return ln[2:].strip(), no, i + 1
    raise src.SourceError(f'sheet: 인용 줄 없음 ({what})')


def _only_bq(lines, what):
    qs = [(no, ln) for no, ln in lines if ln.startswith('>')]
    src.need(len(qs) == 1, f'sheet: 인용 줄 {len(qs)} 개 ({what} · 하나여야 한다)')
    return qs[0][1][2:].strip(), qs[0][0]


def _cells(row, no):
    s = row.strip()
    src.need(s.startswith('|') and s.endswith('|'), f'sheet {no}: 표 줄 꼴')
    return [c.strip() for c in s[1:-1].split('|')]


def _table(lines, start, what):
    """start 이후 첫 표 → (머리, [(칸들, 줄 번호)], 다음 위치)."""
    i = start
    while i < len(lines) and not lines[i][1].startswith('|'):
        i += 1
    src.need(i < len(lines), f'sheet: 표 없음 ({what})')
    rows = []
    while i < len(lines) and lines[i][1].startswith('|'):
        rows.append(lines[i])
        i += 1
    src.need(len(rows) >= 3, f'sheet: 표 줄 {len(rows)} ({what})')
    hdr = _cells(rows[0][1], rows[0][0])
    src.need(re.fullmatch(r'\|(\s*:?-+:?\s*\|)+', rows[1][1].strip()) is not None, f'sheet {rows[1][0]}: 표 구분 줄 ({what})')
    data = []
    for no, ln in rows[2:]:
        c = _cells(ln, no)
        src.need(len(c) == len(hdr), f'sheet {no}: 칸 수 {len(c)} ≠ 머리 {len(hdr)} ({what})')
        data.append((c, no))
    return hdr, data, i


def _bullet(lines, label, what):
    pre = f'- {label}: '
    hits = [(no, ln) for no, ln in lines if ln.startswith(pre)]
    src.need(len(hits) == 1, f'sheet: "- {label}:" 줄 {len(hits)} 개 ({what})')
    return hits[0][1][len(pre):].strip(), hits[0][0]


def md_clean(s):
    """markdown 표기만 뗀다 (` · **) — 글자는 그대로."""
    return s.replace('`', '').replace('**', '')


def sub_markup(s):
    """시트의 `x_y` 아래첨자 표기 → 생성기 표기 `x_{y}` (아래첨자 = 영문 · 숫자 · (쉼표 + 영문 · 숫자) 이어진 것 · NO_SUB 이름 그대로)."""
    for name in NO_SUB:
        s = s.replace(name, name.replace('_', '\x00'))
    out, i, n = [], 0, len(s)
    while i < n:
        c = s[i]
        if c == '_' and i > 0 and not s[i - 1].isspace() and s[i - 1] not in '_([':
            m = re.match(r'[A-Za-z0-9]+(?:,[A-Za-z0-9]+)*', s[i + 1:])
            if m:
                out.append('_{' + m.group(0) + '}')
                i += 1 + m.end()
                continue
        out.append(c)
        i += 1
    return ''.join(out).replace('\x00', '_')


def screen_text(s, breaks=()):
    """시트 글 → 화면 글: 줄바꿈 (breaks = 그 글 바로 뒤 공백 하나를 줄바꿈으로) → markdown 떼기 → 아래첨자 표기.
    `…` 안 (코드 · 파일 · 원장 이름) 은 아래첨자로 바꾸지 않는다 (예: `p7_lit_direction`)."""
    for after in breaks:
        src.need(s.count(after) == 1 and s[s.index(after) + len(after):].startswith(' '), f'줄바꿈 자리 "{after}" (한 번 · 뒤에 공백)')
        i = s.index(after) + len(after)
        s = s[:i] + '\n' + s[i + 1:]
    t = s.replace('**', '')
    src.need('_{' not in t and '^{' not in t and '*' not in t and t.count('`') % 2 == 0, f'sheet 글에 생성기 표기와 겹치는 글자: {t[:80]}')
    parts = t.split('`')
    return ''.join(p if i % 2 else sub_markup(p) for i, p in enumerate(parts))


#: 손으로 정한 줄바꿈 (시트 글 그대로 · 공백 하나 → 줄바꿈) — 두 줄로 넘치는 자리를 '·' 뒤에서 고르게 나눈다
BREAKS = {
    ('0', 'band'): ('판 고정 이완 ·',),
    ('3', 'band'): ('21.0 µm² ·',),
    ('4', 'band'): ('×2.40) ·',),
    ('7', 'band'): ('최대 2.4배 ·',),
    ('0', 'L/head'): ('0.7–3 µm) ·',),
}


def notes_text(s):
    return md_clean(s)


def page_content(sheet, k):
    """쪽 k 의 화면 글 · 배치 · 노트 — 전부 시트에서."""
    s = sheet['secs'][k]
    B = s['blocks']
    lay_hdr, lay_rows, _ = _table(B['①'], 0, f'{k}쪽 ① 배치')
    src.need(lay_hdr == ['칸', '넣을 것', '크기 (in)', '탭 글'], f'{k}쪽 ① 머리 {lay_hdr}')
    lay = {r[0][0]: dict(what=r[0][1], size=r[0][2], tab=r[0][3], line=r[1]) for r in lay_rows}
    src.need('왼쪽' in lay and '오른쪽' in lay, f'{k}쪽 ① 왼쪽 · 오른쪽 줄')
    title, t_no = _only_bq(B['②'], f'{k}쪽 ②')
    band, b_no = _only_bq(B['③'], f'{k}쪽 ③')
    note, n_no = _only_bq(B['⑤'], f'{k}쪽 ⑤')
    b6 = B['⑥']
    foot = foot_no = None
    if any(ln.startswith('화면 각주') for _, ln in b6):
        i = _find(b6, r'^화면 각주', 0, f'{k}쪽 ⑥')
        foot, foot_no, _ = _bq(b6, i + 1, f'{k}쪽 ⑥ 화면 각주')
    i = _find(b6, r'^발표자 노트:$', 0, f'{k}쪽 ⑥')
    bullets = []
    for no, ln in b6[i + 1:]:
        if ln.startswith('- '):
            bullets.append((ln[2:].strip(), no))
        elif ln.strip() and bullets:
            break
    src.need(bullets, f'{k}쪽 발표자 노트 없음')
    d_hdr, d_rows, _ = _table(B['⑦'], 0, f'{k}쪽 ⑦')
    src.need(d_hdr == ['말', '이유'], f'{k}쪽 ⑦ 머리 {d_hdr}')
    P = dict(key=k, heading=s['heading'], title=(title, t_no), band=(band, b_no), note=(note, n_no),
             foot=(foot, foot_no) if foot else None, bullets=bullets, dont=[(r[0][0], r[0][1], r[1]) for r in d_rows],
             tabs=dict(L=(lay['왼쪽']['tab'], lay['왼쪽']['line']), R=(lay['오른쪽']['tab'], lay['오른쪽']['line'])), lay=lay)
    P['L'], P['R'] = PAGE_ITEMS[k](B['④'], lay, k)
    return P


# ── 쪽마다 패널 안 순서 (그림 이름 · 크기 = 시트 ① 과 대조) ──

def _fig(name, lay_row, k, side):
    src.need(f'`{name}`' in lay_row['what'], f'{k}쪽 {side} ① "넣을 것" 에 `{name}` 가 없다')
    return ('fig', name, lay_row['size'], lay_row['line'])


def _cap_after(b4, anchor, k):
    i = _find(b4, anchor, 0, f'{k}쪽 ④ {anchor}')
    t, no, _ = _bq(b4, i + 1, f'{k}쪽 ④ {anchor}')
    return ('cap', t, no)


def items_p0(b4, lay, k):
    i1 = _find(b4, r'^④-1 왼쪽', 0, '0쪽 ④-1')
    i2 = _find(b4, r'^④-2 오른쪽', 0, '0쪽 ④-2')
    left_lines, right_lines = b4[i1:i2], b4[i2:]
    head, h_no = _bullet(left_lines, '글머리 (그림 위 한 줄)', '0쪽 ④-1')
    below, w_no = _bullet(left_lines, '덱 값 (2 × 2 그림 아래 한 줄)', '0쪽 ④-1')
    j = _find(left_lines, r'^그림 캡션 \(작은 글\)$', 0, '0쪽 ④-1 캡션')
    lcap, lc_no, _ = _bq(left_lines, j + 1, '0쪽 ④-1 캡션')
    L = [('head', head, h_no), _fig('p0_process_grid_labeled', lay['왼쪽'], k, 'L'), ('below', below, w_no), ('cap', lcap, lc_no)]
    rh = [(no, ln) for no, ln in right_lines[1:] if ln.startswith('- ')]
    src.need(len(rh) == 1, f'0쪽 ④-2 글머리 줄 {len(rh)}')
    eh, e_rows, _ = _table(right_lines, 0, '0쪽 ④-2 식 표')
    src.need(eh[:3] == ['식 이름', '식 (2-1장 개체 · 대조용 글)', '한 줄 뜻 (붙여 넣기)'] and len(e_rows) == 4, f'0쪽 ④-2 식 표 머리 {eh}')
    j = _find(right_lines, r'^그림 캡션 \(작은 글\)$', 0, '0쪽 ④-2 캡션')
    rcap, rc_no, _ = _bq(right_lines, j + 1, '0쪽 ④-2 캡션')
    eq = [dict(name=c[0], eq=c[1], mean=c[2], line=no) for c, no in e_rows]
    # 순서 = 시트 ④-2 의 순서 (글머리 → 그림 → 식 넷 표 → 그림 캡션 (작은 글)) — 넘치면 작은 글이 먼저 밀린다
    R = [('head', rh[0][1][2:].strip(), rh[0][0]), _fig('p0_contact_model_labeled', lay['오른쪽'], k, 'R'), ('eqtable', eq), ('cap', rcap, rc_no)]
    return L, R


def items_p1(b4, lay, k):
    i = _find(b4, r'^④-1 왼쪽 조건 표', 0, '1쪽 ④-1')
    hdr, rows, _ = _table(b4, i + 1, '1쪽 조건 표')
    src.need(hdr == ['항목', '조건'], f'1쪽 조건 표 머리 {hdr}')
    L = [('table', dict(name='cond', hdr=hdr, rows=rows, col_w=(1.48, None), align=('L', 'L')))]
    R = [_fig('p1_bed_strip', lay['오른쪽'], k, 'R'), _cap_after(b4, r'^④-2 캡션 `p1_bed_strip`', k)]
    return L, R


def _two_figs(left, right):
    def f(b4, lay, k):
        L = [_fig(left, lay['왼쪽'], k, 'L'), _cap_after(b4, rf'^(④-1 )?`{left}`', k)]
        R = [_fig(right, lay['오른쪽'], k, 'R'), _cap_after(b4, rf'^(④-2 )?`{right}`', k)]
        return L, R
    return f


def _fig_table(left, col_w, align, after=None):
    def f(b4, lay, k):
        L = [_fig(left, lay['왼쪽'], k, 'L'), _cap_after(b4, rf'^④-1 `{left}`', k)]
        i = _find(b4, r'^④-2 오른쪽 표', 0, f'{k}쪽 ④-2')
        hdr, rows, _ = _table(b4, i + 1, f'{k}쪽 ④-2 표')
        R = [('table', dict(name='t', hdr=hdr, rows=rows, col_w=col_w, align=align))]
        if after:
            t, no = _bullet(b4, after, f'{k}쪽 ④-2')
            R.append(('text', t, no))
        return L, R
    return f


PAGE_ITEMS = {
    '0': items_p0,
    '1': items_p1,
    '2': _two_figs('p2_compaction', 'p6_z_structure'),
    '3': _two_figs('p3_count_vs_area', 'p3_per_am'),
    '4': _two_figs('p4_f_connect', 'p4_tortuosity'),
    '5': _fig_table('p5_breakeven_sigma', (None, 0.72, 0.80, 0.72, 0.80), ('L', 'C', 'C', 'C', 'C'), after='표 아래'),
    '6': _fig_table('p6_constriction_share', (1.05, 1.36, None), ('L', 'C', 'L')),
    '7': _fig_table('p7_summary_heat', (0.34, 1.40, 1.45, None), ('C', 'L', 'L', 'L')),
    '부록': _fig_table('diag_relax_drop_vs_N', (0.22, 0.55, 2.55, None), ('C', 'L', 'L', 'L')),
}


# ───────────────────────────── 그림 (100 % · 바이트 = meta) ─────────────────────────────

def fig_info(name):
    """그림 이름 → (PNG 경로, (폭, 높이) in, meta sha256)."""
    if name.startswith('p0_'):
        meta = json.loads(P0_META.read_text(encoding='utf-8'))
        path = P0_DIR / f'{name}.png'
        from PIL import Image
        with Image.open(path) as im:
            px = im.size
        size = (px[0] / P0_DPI, px[1] / P0_DPI)
        sha = meta['files'][f'{name}.png']
    else:
        meta = json.loads(FIG2_META.read_text(encoding='utf-8'))
        f = meta['figures'][name]
        path = FIG2_DIR / f'{name}.png'
        size = tuple(f['size_in'])
        sha = f['files'][f'{name}.png']
    src.need(hashlib.sha256(path.read_bytes()).hexdigest() == sha, f'{name}.png ≠ meta sha256')
    return path, size, sha


def sheet_size(text):
    m = re.search(r'(\d+\.\d+) × (\d+\.\d+)', text)
    return (float(m.group(1)), float(m.group(2))) if m else None


# ───────────────────────────── 그리기 ─────────────────────────────

def band3(slide, text):
    h_out = I(BAND3_H)
    d1.autoshape(slide, 'band', MSO_SHAPE.ROUNDED_RECTANGLE, (BAND_X, BAND_Y, BAND_W, h_out), fill=d1.FAINT, adj=R_OUT / h_out)
    h_in = BAND_Y + h_out - IN_BOT_GAP - IN_Y
    d1.autoshape(slide, 'band/in', MSO_SHAPE.ROUNDED_RECTANGLE, (IN_X, IN_Y, IN_W, h_in), fill='FFFFFF', line=d1.LINE_GRAY, line_w=1.0,
                 adj=R_IN / h_in)
    d1.textbox(slide, 'band/in/text', (inch(IN_X) + 0.06, inch(IN_Y) + 0.02, inch(IN_W) - 0.12, inch(h_in) - 0.04), [text], BAND_PT,
               kind='desc', align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, wrap=True, ins=(0.05, 0.02, 0.05, 0.02))


def panel3(slide, side, tab_text):
    (x, _), w, _, adj = d1.PANEL[0 if side == 'L' else 1], d1.PANEL[2], d1.PANEL[3], d1.PANEL[4]
    y = panel_y()
    h = I(PANEL3_BOTTOM) - y
    d1.autoshape(slide, side, MSO_SHAPE.ROUNDED_RECTANGLE, (x, y, w, h), fill=None, line=d1.DASH_GRAY, line_w=0.75, dash='sysDash', adj=adj)
    tw = d1.est_text_width_in(tab_text, 12) + 0.24
    tx = inch(x) + (inch(w) - tw) / 2
    d1.textbox(slide, f'{side}/tab', (tx, inch(tab_y()), tw, inch(d1.PANEL_TAB_H)), [tab_text], 12, color='000000', align=PP_ALIGN.CENTER,
               wrap=False, fill='FFFFFF', anchor=MSO_ANCHOR.MIDDLE, ins=(0.05, 0.0, 0.05, 0.0))
    return inch(x), inch(y), inch(w), inch(h)


def cell_height(txt, size, width_in, bold=False):
    """칸 글 높이 (in) — 문단 = 글 또는 [(글, 색, 굵게)] · 굵은 run 은 굵은 폭으로 (초안 1 est_box_height 와 같은 줄 높이)."""
    ins = d1.TBL_INS
    wpt = (width_in - ins[0] - ins[2]) * 72
    tot = 0.0
    for para in (txt if isinstance(txt, list) else [txt]):
        runs = [(para, None, bold)] if isinstance(para, str) else para
        segs = [(t, size, mode is not None, bold if b is None else b) for text, _, b in runs for t, mode in d1.parse_markup(text)]
        tot += d1.para_height_pt(segs, wpt, 1.0, d1.LH)[1]
    return tot / 72 + ins[1] + ins[3]


def table_heights(col_w, rows, merges=(), size=TBL_PT, row_min=0.17, head=True):
    """줄마다 높이 (in) = 칸 글의 추정 높이 최대 (합친 칸 = 높이를 줄 수로 나눔 · 머리 줄 = 굵게) — 초안 1 table 과 같은 규칙."""
    heights = []
    for r, row in enumerate(rows):
        hmax = row_min
        for c, txt in enumerate(row):
            if txt is None:
                continue
            span_w, span_h = col_w[c], 1
            for (r0, c0), (r1, c1) in merges:
                if (r0, c0) == (r, c):
                    span_w, span_h = sum(col_w[c0:c1 + 1]), r1 - r0 + 1
            hmax = max(hmax, cell_height(txt, size, span_w, bold=(head and r == 0)) / span_h)
        heights.append(round(hmax + 0.005, 3))
    return heights


def table3(slide, name, x, y, col_w, rows, *, head=True, merges=(), align=None, size=TBL_PT, row_min=0.17, shade_first_col=True):
    """rows = [[글 | 문단 목록 | None]] · 열 맞춤 L/C/R · 칸 높이 = 추정 줄 수 (초안 1 table 과 같은 꼴 · 머리 줄 + 첫 열 옅은 회색 ·
    shade_first_col=False = 첫 열도 흰 칸 (0쪽 식 2 × 2))."""
    nr, nc = len(rows), len(rows[0])
    al = {'L': PP_ALIGN.LEFT, 'C': PP_ALIGN.CENTER, 'R': PP_ALIGN.RIGHT}
    heights = table_heights(col_w, rows, merges, size, row_min, head=head)
    gf = slide.shapes.add_table(nr, nc, Emu(I(x)), Emu(I(y)), Emu(I(sum(col_w))), Emu(I(sum(heights))))
    gf.name = name
    tbl = gf.table
    tblPr = tbl._tbl.tblPr
    for k in ('firstRow', 'bandRow', 'firstCol', 'lastRow', 'lastCol', 'bandCol'):
        tblPr.set(k, '0')
    for el in tblPr.findall(qn('a:tableStyleId')):
        tblPr.remove(el)
    for j, cw in enumerate(col_w):
        tbl.columns[j].width = Emu(I(cw))
    for i, hh in enumerate(heights):
        tbl.rows[i].height = Emu(I(hh))
    for (r0, c0), (r1, c1) in merges:
        tbl.cell(r0, c0).merge(tbl.cell(r1, c1))
    for r, row in enumerate(rows):
        for c, txt in enumerate(row):
            cell = tbl.cell(r, c)
            cell.margin_left, cell.margin_top, cell.margin_right, cell.margin_bottom = (Emu(I(v)) for v in d1.TBL_INS)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            is_head = (head and r == 0) or (c == 0 and shade_first_col)
            cell.fill.solid()
            cell.fill.fore_color.rgb = d1._rgb(d1.FAINT if is_head else 'FFFFFF')
            d1._cell_border(cell)
            if txt is None or cell.is_spanned:
                continue
            tf = cell.text_frame
            tf.word_wrap = True
            a = al[(align or 'L' * nc)[c]] if not (head and r == 0) else PP_ALIGN.CENTER
            if isinstance(txt, list):
                d1.fill_paras(tf, txt, size, color=d1.DARK, kind='ko', align=a)
            else:
                d1.fill_paras(tf, [txt], size, color=d1.DARK, bold=(head and r == 0), kind='ko', align=a)
    return y + sum(heights)


def place_fig(slide, name, px, pw, y, figname):
    path, (fw, fh), _ = fig_info(figname)
    fx = px + (pw - fw) / 2
    slide.shapes.add_picture(str(path), Emu(I(fx)), Emu(I(y)), Emu(I(fw)), Emu(I(fh))).name = name
    return fx, fw, fh


PANEL_W = inch(d1.PANEL[2])
TEXT_X0 = 0.10                         # 패널 안 글 왼쪽 여백 (초안 1 과 같음)
TEXT_W = PANEL_W - 0.20
TABLE_W = TEXT_W - 0.04


def table_rows(spec):
    """시트 표 → (화면 줄들, 합칠 칸, 열 폭).  시트의 빈 첫 칸 = 위 줄 첫 칸과 합침 (1쪽 SE 영률 두 줄)."""
    rows = [[screen_text(c) for c in spec['hdr']]]
    merges = []
    for r_i, (cells, _) in enumerate(spec['rows'], 1):
        row = [screen_text(c) if c else None for c in cells]
        if row[0] is None and r_i > 1:
            merges.append(((r_i - 1, 0), (r_i, 0)))
        rows.append(row)
    fixed = sum(c for c in spec['col_w'] if c is not None)
    col_w = [c if c is not None else round(TABLE_W - fixed, 4) for c in spec['col_w']]
    src.need(abs(sum(col_w) - TABLE_W) < 0.005, f'table {spec["name"]} 열 폭 합 {sum(col_w):.3f} ≠ {TABLE_W:.3f}')
    return rows, merges, col_w


def eq_rows(eq):
    """0쪽 식 넷 → 2 × 2 칸 (칸마다 식 이름 · 식 · 한 줄 뜻 세 문단)."""
    cells = [[[(screen_text(e['name']), None, True)], [(screen_text(e['eq']), None, None)], [(screen_text(e['mean']), d1.MID, None)]]
             for e in eq]
    return [[cells[0], cells[1]], [cells[2], cells[3]]], [TABLE_W / 2, TABLE_W / 2]


def item_height(it, page='', side=''):
    """패널 안 한 항목이 차지하는 높이 (in) — render_panel 과 같은 간격."""
    kind = it[0]
    br = BREAKS.get((page, f'{side}/{kind}'), ())
    if kind == 'head':
        return d1.est_box_height([screen_text(it[1], br)], HEAD_PT, TEXT_W, 1.0) + 0.02 + 0.01
    if kind == 'fig':
        return 0.01 + fig_info(it[1])[1][1] + 0.03
    if kind in ('below', 'text'):
        return d1.est_box_height([screen_text(it[1], br)], BELOW_PT, TEXT_W, 1.2, kind='desc') + 0.02
    if kind == 'cap':
        return d1.est_box_height(['【 ' + screen_text(it[1]) + ' 】'], CAP_PT, 4.50, 1.0, kind='desc') + 0.02 + 0.04
    if kind == 'table':
        rows, merges, col_w = table_rows(it[1])
        return 0.02 + sum(table_heights(col_w, rows, merges)) + 0.06
    if kind == 'eqtable':
        rows, cw = eq_rows(it[1])
        return 0.02 + sum(table_heights(cw, rows, head=False)) + 0.06
    raise ValueError(kind)


def render_panel(slide, side, items, box, page=''):
    px, py, pw, ph = box
    x0, w0 = px + TEXT_X0, TEXT_W
    y = content_top()
    fx, fw = px + (pw - 4.50) / 2, 4.50
    for it in items:
        kind = it[0]
        br = BREAKS.get((page, f'{side}/{kind}'), ())
        if kind == 'head':
            y = d1.stack_text(slide, f'{side}/head', x0, y, w0, [screen_text(it[1], br)], HEAD_PT) + 0.01
        elif kind == 'fig':
            fx, fw, fh = place_fig(slide, f'{side}/fig', px, pw, y + 0.01, it[1])
            y += 0.01 + fh + 0.03
        elif kind == 'below':
            y = d1.stack_text(slide, f'{side}/below', x0, y, w0, [screen_text(it[1], br)], BELOW_PT, kind='desc', spacing=1.2)
        elif kind == 'cap':
            y = d1.stack_text(slide, f'{side}/cap', fx, y, fw, ['【 ' + screen_text(it[1]) + ' 】'], CAP_PT, kind='desc', color=d1.MID) + 0.04
        elif kind == 'text':
            y = d1.stack_text(slide, f'{side}/text', x0, y, w0, [screen_text(it[1])], BELOW_PT, kind='desc', spacing=1.2)
        elif kind == 'table':
            rows, merges, col_w = table_rows(it[1])
            y = table3(slide, f'{side}/table', x0 + 0.02, y + 0.02, col_w, rows, head=True, merges=merges, align=it[1]['align']) + 0.06
        elif kind == 'eqtable':
            rows, cw = eq_rows(it[1])
            y = table3(slide, f'{side}/eqtable', x0 + 0.02, y + 0.02, cw, rows, head=False, align='LL', shade_first_col=False) + 0.06
    return y


def note3(slide, text):
    d1.textbox(slide, 'note', note_box(), [text], NOTE_PT, color=d1.GRAY_TXT, kind='desc', wrap=True, anchor=MSO_ANCHOR.MIDDLE,
               ins=(0.05, 0.02, 0.05, 0.02))


def foot3(slide, text):
    d1.textbox(slide, 'foot', foot_box(), [text], FOOT_PT, color=d1.GRAY_TXT, kind='desc', wrap=True, anchor=MSO_ANCHOR.TOP,
               ins=(0.05, 0.02, 0.05, 0.02))


def page_number3(slide, label):
    """쪽 번호 자리 (초안 1 page_number 와 같은 상자 · 크기 · 색 · 글꼴) — 글 = 시트 쪽 이름 (0–7 · 부록)."""
    x, y, w, h = (inch(v) for v in d1.SLDNUM)
    d1.textbox(slide, 'pgnum', (x, y, w, h), [label], 12, color='404040', kind='desc', align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE,
               wrap=False, ins=(0.1, 0.05, 0.1, 0.05))


def notes_for(P):
    lines = [notes_text(b) for b, _ in P['bullets']]
    out = '발표자 노트\n' + '\n'.join('- ' + b for b in lines)
    out += '\n\n하지 않을 말\n' + '\n'.join(f'- {notes_text(a)} — {notes_text(b)}' for a, b, _ in P['dont'])
    return out


def build_page(prs, P):
    s = prs.slides.add_slide(prs.slide_layouts[0])
    k = P['key']
    d1.header(s, screen_text(P['title'][0]))
    band3(s, screen_text(P['band'][0], BREAKS.get((k, 'band'), ())))
    for side in ('L', 'R'):
        box = panel3(s, side, screen_text(P['tabs'][side][0]))
        render_panel(s, side, P[side], box, k)
    note3(s, screen_text(P['note'][0]))
    if P['foot']:
        foot3(s, screen_text(P['foot'][0]))
    page_number3(s, PAGE_LABEL[P['key']])
    d1.notes(s, notes_for(P))
    return s


def new_presentation3():
    prs, keep = d1.new_presentation()
    cp = prs.core_properties
    cp.title = '50kg/batch 4차년도 DEM 보고 — 초안 3 (회사 보고판)'
    cp.subject = '0쪽 (DEM 해석 방법) + 1–7쪽 + 부록 · 글 = draft2/slide_text_draft3.md'
    cp.comments = 'docs/50kg/report_y4/build_kg50_report_y4_draft3.py'
    cp.created = cp.modified = _dt.datetime(2026, 11, 1, 0, 0, 0)
    cp.last_printed = _dt.datetime(2026, 11, 1, 0, 0, 0)
    return prs, keep


def build(out=OUT_DECK):
    sheet = read_sheet()
    pages = [page_content(sheet, k) for k in PAGES]
    prs, _ = new_presentation3()
    for P in pages:
        build_page(prs, P)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    d1.save_deterministic(prs, out)
    return dict(sheet=sheet, pages=pages)


def screen_strings(P):
    """쪽의 화면 글 (시트 꼴) 전부 — 아래첨자 목록용."""
    out = [P['title'][0], P['band'][0], P['note'][0], P['tabs']['L'][0], P['tabs']['R'][0]] + ([P['foot'][0]] if P['foot'] else [])
    for side in ('L', 'R'):
        for it in P[side]:
            if it[0] in ('head', 'below', 'text', 'cap'):
                out.append(it[1])
            elif it[0] == 'table':
                out += list(it[1]['hdr']) + [c for cells, _ in it[1]['rows'] for c in cells]
            elif it[0] == 'eqtable':
                out += [x for e in it[1] for x in (e['name'], e['eq'], e['mean'])]
    return out


def subscript_inventory(pages):
    """쪽마다 아래첨자로 바꾼 자리 (기호_아래첨자) — 1저자 · 검토용 목록 (검사 V1 은 '_' 로 되돌려 시트와 대조)."""
    inv = {}
    for P in pages:
        toks = set()
        for s in screen_strings(P):
            for m in re.finditer(r'(\S?\S)_\{([^}]*)\}', screen_text(s)):
                toks.add(f'{m.group(1)}_{m.group(2)}')
        inv[P['key']] = sorted(toks)
    return inv


# ───────────────────────────── 측정 (패널마다 쌓은 높이 · 넘침) ─────────────────────────────

def measure():
    sheet = read_sheet()
    pages = [page_content(sheet, k) for k in PAGES]
    ct = content_top()
    avail = PANEL3_BOTTOM - 0.04 - ct
    print(f'band {BAND3_H} in · tab y {inch(tab_y()):.3f} · panel y {inch(panel_y()):.3f} · content top {ct:.3f} · panel bottom {PANEL3_BOTTOM} '
          f'· available {avail:.3f} in')
    pw = inch(d1.PANEL[2])
    for P in pages:
        k = P['key']
        tw = d1.est_text_width_in(screen_text(P['title'][0]), TITLE_PT, bold=True)
        print(f'— {k}쪽 title width {tw:.2f} in (room {10 - inch(d1.HDR_TITLE[0]) - 0.12:.2f})')
        bw = inch(IN_W) - 0.12
        bt = screen_text(P['band'][0], BREAKS.get((k, 'band'), ()))
        bh = d1.est_box_height([bt], BAND_PT, bw, 1.0, (0.05, 0.02, 0.05, 0.02), kind='desc')
        for seg in bt.split('\n'):
            print(f'   band line width {d1.est_text_width_in(seg, BAND_PT):.2f} in (room {bw - 0.10:.2f})')
        print(f'   band text height {bh:.3f} (inner {inch(BAND_Y + I(BAND3_H) - IN_BOT_GAP - IN_Y) - 0.04:.3f})')
        nw = note_box()[2]
        nh = d1.est_box_height([screen_text(P['note'][0])], NOTE_PT, nw, 1.0, (0.05, 0.02, 0.05, 0.02), kind='desc')
        print(f'   note height {nh:.3f} (box {NOTE3_H})')
        if P['foot']:
            fh = d1.est_box_height([screen_text(P['foot'][0])], FOOT_PT, foot_box()[2], 1.0, (0.05, 0.02, 0.05, 0.02), kind='desc')
            print(f'   foot height {fh:.3f} (box {FOOT3_H})')
        for side in ('L', 'R'):
            tabw = d1.est_text_width_in(screen_text(P['tabs'][side][0]), 12) + 0.24
            y = ct
            parts = []
            for it in P[side]:
                h = item_height(it, k, side)
                parts.append(f'{it[0]} {h:.2f}')
                y += h
            print(f'   {side} tab {tabw:.2f}/{pw:.2f} · ' + ' + '.join(parts) + f' → bottom {y:.3f} (limit {PANEL3_BOTTOM - 0.04:.3f})')


# ───────────────────────────── 검사 (저장된 덱을 다시 읽는다) ─────────────────────────────

def marked_text(el):
    """도형 · 표 칸 XML → 시트 꼴 글 (아래첨자 run = '_' + 글 · 줄바꿈 = 공백 · 문단 = '\n')."""
    txBody = el.find('.//' + qn('p:txBody'))
    if txBody is None:
        txBody = el.find('.//' + qn('a:txBody'))
    if txBody is None:
        return ''
    paras = []
    for p in txBody.findall(qn('a:p')):
        out = []
        for r in p.iterchildren(qn('a:r'), qn('a:fld'), qn('a:br')):
            if r.tag == qn('a:br'):
                out.append(' ')
                continue
            rpr = r.find(qn('a:rPr'))
            t = r.find(qn('a:t')).text or ''
            base = rpr.get('baseline') if rpr is not None else None
            if base == '-25000':
                out.append('_' + t)
            elif base == '30000':
                out.append('^' + t)
            else:
                out.append(t)
        paras.append(''.join(out))
    return '\n'.join(paras)


def _n(s):
    return re.sub(r'\s+', ' ', s).strip()


def expected_texts(P):
    """화면 도형 이름 → 시트 글 (md 뗀 꼴) — 검사 V 의 기준."""
    E = {'hdr/title': P['title'][0], 'band/in/text': P['band'][0], 'note': P['note'][0], 'L/tab': P['tabs']['L'][0], 'R/tab': P['tabs']['R'][0]}
    if P['foot']:
        E['foot'] = P['foot'][0]
    for side in ('L', 'R'):
        for it in P[side]:
            if it[0] in ('head', 'below', 'text'):
                E[f'{side}/{it[0]}'] = it[1]
            elif it[0] == 'cap':
                E[f'{side}/cap'] = '【 ' + it[1] + ' 】'
    return {k: md_clean(v) for k, v in E.items()}


def expected_cells(P):
    out = {}
    for side in ('L', 'R'):
        for it in P[side]:
            if it[0] == 'table':
                spec = it[1]
                rows = [list(spec['hdr'])] + [list(c) for c, _ in spec['rows']]
                out[f'{side}/table'] = [[md_clean(c) for c in r] for r in rows]
            elif it[0] == 'eqtable':
                e = it[1]
                cell = [md_clean(x['name']) + '\n' + md_clean(x['eq']) + '\n' + md_clean(x['mean']) for x in e]
                out[f'{side}/eqtable'] = [[cell[0], cell[1]], [cell[2], cell[3]]]
    return out


FORBIDDEN = d1.FORBIDDEN
STAGE_E_OK = 'Stage-E σ_ion 안 씀'
NEG = ('아님', '안 함', '안 씀', '금지')


def check_deck(path, info=None):
    C = d1.Checks()
    prs = Presentation(str(path))
    slides = list(prs.slides)
    sheet = read_sheet()
    pages = [page_content(sheet, k) for k in PAGES]
    C.add('C1 slide count = 9 (0쪽 · 1–7쪽 · 부록)', len(slides) == N_PAGES, len(slides))
    C.add('C1 slide size = template (10 × 7.5 in)', (prs.slide_width, prs.slide_height) == (d1.SLIDE_W, d1.SLIDE_H), (prs.slide_width, prs.slide_height))
    # V — 화면 글 = 시트 글 (도형 · 표 칸)
    v_bad, v_missing, v_extra = [], [], []
    for P, s in zip(pages, slides):
        E = expected_texts(P)
        shapes = {sp.name: sp for sp in s.shapes}
        for nm, want in E.items():
            if nm not in shapes:
                v_missing.append((P['key'], nm))
                continue
            got = marked_text(shapes[nm]._element)
            if _n(got) != _n(want):
                v_bad.append((P['key'], nm, _n(got)[:90], _n(want)[:90]))
        for nm, want_rows in expected_cells(P).items():
            if nm not in shapes or not shapes[nm].has_table:
                v_missing.append((P['key'], nm))
                continue
            tbl = shapes[nm].table
            for r, row in enumerate(want_rows):
                for c, want in enumerate(row):
                    cell = tbl.cell(r, c)
                    if cell.is_spanned:
                        if want.strip():
                            v_bad.append((P['key'], nm, (r, c), 'spanned cell has sheet text', want[:60]))
                        continue
                    got = marked_text(cell._tc)
                    if _n(got) != _n(want):
                        v_bad.append((P['key'], nm, (r, c), _n(got)[:80], _n(want)[:80]))
        allowed = set(E) | set(expected_cells(P)) | {'hdr/sq/num', 'hdr/proj', 'pgnum'}
        for sp in s.shapes:
            has_t = (sp.has_text_frame and sp.text_frame.text.strip()) or (getattr(sp, 'has_table', False) and sp.has_table)
            if has_t and sp.name not in allowed:
                v_extra.append((P['key'], sp.name, (sp.text_frame.text if sp.has_text_frame else '')[:60]))
    C.add('V1 every screen text = the sheet text for that slot (verbatim · subscript runs read back as "_" · 【 】 = caption frame)', not v_bad, v_bad[:12])
    C.add('V2 every sheet slot present on its slide', not v_missing, v_missing)
    C.add('V3 no screen text outside the sheet slots (except chapter number · project · page number)', not v_extra, v_extra)
    # V4 — 노트 = 시트 발표자 노트 + 하지 않을 말
    n_bad = []
    for P, s in zip(pages, slides):
        got = s.notes_slide.notes_text_frame.text if s.has_notes_slide else ''
        if got != notes_for(P):
            n_bad.append(P['key'])
    C.add('V4 notes = sheet 발표자 노트 bullets + ⑦ 하지 않을 말 (markdown removed)', not n_bad, n_bad)
    # C4 금지 낱말 · Stage-E · 인용 금지
    texts = [d1.all_text(s) for s in slides]
    notes_t = [s.notes_slide.notes_text_frame.text if s.has_notes_slide else '' for s in slides]
    hits = [(PAGES[i], f) for i, t in enumerate(texts) for f in FORBIDDEN if f in t]
    C.add('C4 forbidden wording absent on screen (plan §1 · principles §5)', not hits, hits)
    nh = []
    for i, t in enumerate(notes_t):
        body, _, dont = t.partition('\n\n하지 않을 말\n')
        for f in FORBIDDEN:
            for m in re.finditer(re.escape(f), body):
                tail = body[m.end():m.end() + 25]
                if not any(ng in tail for ng in NEG):
                    nh.append((PAGES[i], f, body[max(0, m.start() - 15):m.end() + 25]))
    C.add('C4 forbidden wording in notes only negated (… 아님 · 안 함 · 안 씀) or under "하지 않을 말"', not nh, nh)
    bad_stage = []
    for i, t in enumerate(texts + notes_t):
        for m in re.finditer('Stage-E', t):
            seg = t[m.start():m.start() + 20]
            if not (seg.startswith('Stage-E σ_ion 안 씀') or seg.startswith('Stage-E σion 안 씀') or seg.startswith('Stage-E σ_ion 은')):
                bad_stage.append((PAGES[i % N_PAGES], seg))
    C.add(f'C4 "Stage-E" only in "{STAGE_E_OK}" (KG50B-07)', not bad_stage, bad_stage)
    ban = json.loads(src.rp('docs/reviews/claims.json').read_text(encoding='utf-8')).get('quotation_ban', [])
    pats = [q.get('pattern') if isinstance(q, dict) else q for q in ban]
    allt = '\n'.join(texts + notes_t)
    C.add('C4 quotation_ban patterns absent (claims.json · screen + notes)', not [p for p in pats if p and p in allt],
          [p for p in pats if p and p in allt])
    # C5 글 상자 맞춤 · 한 줄 상자 · 줄바꿈 없는 상자 폭
    fit_bad, one_bad, wide_bad = [], [], []
    for i, s in enumerate(slides):
        for sp in s.shapes:
            if not sp.has_text_frame or not sp.text_frame.text.strip():
                continue
            lines, need_h, inner_h, too_wide = d1.text_fit(sp)
            if need_h > inner_h * d1.FIT_SLACK + 1e-6:
                fit_bad.append((PAGES[i], sp.name, round(need_h, 3), round(inner_h, 3)))
            if any(k in sp.name for k in d1.ONE_LINE) and (max(lines) > 1 + sum(sp.text_frame.text.count(c) for c in ('\n', '\v'))):
                one_bad.append((PAGES[i], sp.name, lines))
            if too_wide:
                wide_bad.append((PAGES[i], sp.name))
    C.add('C5 every text box: estimated text height ≤ box (conservative widths: Hangul 1 em · Latin DejaVu)', not fit_bad, fit_bad)
    C.add('C5 one-line boxes (header · tabs · page number · grey note) stay one line', not one_bad, one_bad)
    C.add('C5 no-wrap boxes: text width ≤ box', not wide_bad, wide_bad)
    # C6 겹침 · 포함 · 머리 띠
    ov_bad, in_bad, hdr_bad = [], [], []
    hdr_bottom = d1.HDR_BAND[1] + d1.HDR_BAND[3]
    for i, s in enumerate(slides):
        boxes = d1.slide_boxes(s)
        names = list(boxes)
        for nm, b in boxes.items():
            par = d1._parent(nm, boxes)
            if not nm.startswith('hdr/') and b[1] < hdr_bottom:
                hdr_bad.append((PAGES[i], nm, round(inch(b[1]), 3)))
            if par is None:
                if not d1._inside(b, (0, 0, d1.SLIDE_W, d1.SLIDE_H)):
                    in_bad.append((PAGES[i], nm, 'outside slide'))
                continue
            pb = boxes[par]
            if nm.endswith('/tab'):
                cy = b[1] + b[3] / 2
                ok = abs(cy - pb[1]) <= I(0.09) and b[0] >= pb[0] and b[0] + b[2] <= pb[0] + pb[2]
                if not ok:
                    in_bad.append((PAGES[i], nm, f'tab not centred on {par} top edge'))
            elif not d1._inside(b, pb):
                in_bad.append((PAGES[i], nm, f'not inside {par}', round(inch(b[1] + b[3] - pb[1] - pb[3]), 3)))
        for a_i in range(len(names)):
            for b_i in range(a_i + 1, len(names)):
                a, b = names[a_i], names[b_i]
                if a.startswith(b + '/') or b.startswith(a + '/'):
                    continue
                if d1._overlap(boxes[a], boxes[b]):
                    ov_bad.append((PAGES[i], a, b))
    C.add('C6 no overlapping shapes except parent ⊃ child (names = hierarchy)', not ov_bad, ov_bad)
    C.add('C6 children inside their parent · tabs straddle the parent top edge · roots inside the slide', not in_bad, in_bad)
    C.add('C6 nothing (but header text) inside the template header band (y < 0.911 in)', not hdr_bad, hdr_bad)
    # C9 그림 100 % · 바이트 = meta · 시트 크기
    pic_bad, byte_bad, size_bad = [], [], []
    for P, s in zip(pages, slides):
        for side in ('L', 'R'):
            for it in P[side]:
                if it[0] != 'fig':
                    continue
                path, (fw, fh), sha = fig_info(it[1])
                sps = [sp for sp in s.shapes if sp.name == f'{side}/fig']
                if len(sps) != 1:
                    pic_bad.append((P['key'], side, it[1], 'missing'))
                    continue
                sp = sps[0]
                sx, sy = inch(sp.width) / fw, inch(sp.height) / fh
                if not (abs(sx - 1) < 0.005 and abs(sy - 1) < 0.005):
                    pic_bad.append((P['key'], side, it[1], round(sx, 4), round(sy, 4)))
                if sp.image.blob != path.read_bytes() or hashlib.sha256(sp.image.blob).hexdigest() != sha:
                    byte_bad.append((P['key'], side, it[1]))
                want = sheet_size(it[2])
                if want is None or abs(want[0] - fw) > 0.005 or abs(want[1] - fh) > 0.005:
                    size_bad.append((P['key'], side, it[1], it[2], (fw, fh)))
    C.add('C9 every figure placed at 100 % of its figure size (no rescale)', not pic_bad, pic_bad)
    C.add('C9 figure bytes = PNG = meta sha256', not byte_bad, byte_bad)
    C.add('C9 figure size = sheet ① 크기 (in)', not size_bad, size_bad)
    # C12 글꼴 · 크기
    f_bad = []
    allowed_f = {d1.EN, d1.KO, d1.DESC}
    for i, s in enumerate(slides):
        for el in s._element.iter(qn('a:rPr')):
            faces = {el.find(qn('a:' + t)).get('typeface') if el.find(qn('a:' + t)) is not None else None for t in ('latin', 'ea')}
            if not faces <= allowed_f or el.get('sz') is None or int(el.get('sz')) < 700:
                f_bad.append((PAGES[i], faces, el.get('sz')))
    C.add('C12 every run: explicit fonts from {Aptos, KoPubWorld돋움체 Medium, 맑은 고딕} · size ≥ 7 pt', not f_bad, f_bad[:10])
    # C8 화면 숫자 ⊆ 그 쪽 시트 절의 숫자
    num_bad = []
    for P, s in zip(pages, slides):
        sec = '\n'.join(ln for _, ln in sheet['secs'][P['key']]['lines'])
        sec_toks = set(re.findall(r'\d+(?:\.\d+)?', sec))
        t = '\n'.join(sp.text_frame.text for sp in s.shapes if sp.has_text_frame and sp.name not in ('pgnum', 'hdr/sq/num', 'hdr/proj'))
        t += '\n' + '\n'.join(c.text for sp in s.shapes if getattr(sp, 'has_table', False) and sp.has_table for r in sp.table.rows for c in r.cells)
        unk = sorted({tk for tk in re.findall(r'\d+(?:\.\d+)?', t) if tk not in sec_toks})
        if unk:
            num_bad.append((P['key'], unk))
    C.add('C8 every number on a slide occurs in that page\'s sheet section', not num_bad, num_bad)
    return C


# ───────────────────────────── 넘침 보고 (저장된 덱 · 패널 바닥 기준) ─────────────────────────────

def line_char_counts(segs, width_pt):
    """d1.wrap_lines 와 같은 규칙으로 나눈 줄마다 글자 수 (공백 포함)."""
    chars = [(c, pt * (0.65 if sub else 1.0), b) for t, pt, sub, b in segs for c in t]
    if not chars:
        return [0]
    ws = d1.seq_widths(chars)
    words, cur = [], []
    for (c, _, _), w in zip(chars, ws):
        if c == ' ':
            words.append(cur)
            cur = []
            words.append([(c, w)])
        elif c == '\n':
            words.append(cur)
            cur = []
            words.append(None)
        else:
            cur.append((c, w))
    words.append(cur)
    counts, x = [0], 0.0

    def long_word(wd, x0):
        nonlocal x
        acc = x0
        for _, w in wd:
            if acc + w > width_pt + 1e-6 and acc > 0:
                counts.append(0)
                acc = 0.0
            acc += w
            counts[-1] += 1
        x = acc

    for wd in words:
        if wd is None:
            counts.append(0)
            x = 0.0
            continue
        if not wd:
            continue
        ww = sum(w for _, w in wd)
        if wd[0][0] == ' ':
            x += ww
            counts[-1] += 1
            continue
        if x + ww <= width_pt + 1e-6:
            x += ww
            counts[-1] += len(wd)
        elif x == 0.0:
            long_word(wd, 0.0)
        else:
            counts.append(0)
            x = 0.0
            if ww > width_pt:
                long_word(wd, 0.0)
            else:
                x = ww
                counts[-1] += len(wd)
    return counts


def shape_lines(sp):
    """글 상자 → [(줄 위 in, 줄 아래 in, 글자 수)] (저장된 상자 · 초안 1 text_fit 과 같은 추정)."""
    d, _ = d1._insets(sp)
    w_pt = (sp.width - d['lIns'] - d['rIns']) / d1.EMU * 72
    y = inch(sp.top + d['tIns'])
    out = []
    for segs, spc, lh in d1._shape_paras(sp):
        size = max((sg[1] for sg in segs), default=10)
        step = size * lh * spc / 72
        for n in line_char_counts(segs, w_pt):
            out.append((y, y + step, n))
            y += step
    return out


def overflow_report(path):
    """패널 (L · R) 의 자식이 패널 바닥 아래로 내려간 자리 — 넘친 in · 넘친 글자 수 (줄 단위 추정 · 표 = 넘친 줄의 글자)."""
    prs = Presentation(str(path))
    rep = []
    for k, s in zip(PAGES, prs.slides):
        boxes = d1.slide_boxes(s)
        for side in ('L', 'R'):
            if side not in boxes:
                continue
            pb = inch(boxes[side][1] + boxes[side][3])
            for sp in s.shapes:
                if not sp.name.startswith(side + '/') or sp.name.endswith('/tab'):
                    continue
                x, y, w, h = boxes[sp.name]
                bottom = inch(y + h)
                if bottom <= pb + 0.01:
                    continue
                ent = dict(page=k, side=side, element=sp.name, over_in=round(bottom - pb, 3), top_in=round(inch(y), 3),
                           bottom_in=round(bottom, 3), panel_bottom_in=round(pb, 3), slide_bottom_over_in=round(max(0.0, bottom - 7.5), 3))
                if sp.shape_type == 13:
                    ent['kind'] = 'picture'
                elif getattr(sp, 'has_table', False) and sp.has_table:
                    ent['kind'] = 'table'
                    tbl = sp.table
                    yy, over_chars, tot, rows_over = inch(y), 0, 0, []
                    est_h = d1.table_est_height(sp)
                    scale = est_h / sum(r.height for r in tbl.rows)       # 추정 높이 (넘친 칸) 를 줄 높이에 비례로 나눔
                    for r_i, row in enumerate(tbl.rows):
                        rh = inch(row.height) * scale
                        n = sum(len(c.text) for c in row.cells if not c.is_spanned)
                        tot += n
                        if yy + rh > pb + 0.01:
                            over_chars += n
                            rows_over.append(r_i)
                        yy += rh
                    ent.update(chars_over=over_chars, chars_total=tot, rows_over=rows_over)
                else:
                    ent['kind'] = 'text'
                    ls = shape_lines(sp)
                    ent.update(chars_over=sum(n for a, b, n in ls if b > pb + 0.01), chars_total=sum(n for _, _, n in ls),
                               lines_over=sum(1 for a, b, n in ls if b > pb + 0.01), lines_total=len(ls))
                rep.append(ent)
    return rep


# ───────────────────────────── 렌더 검사 (초안 1 R1–R6 을 9 장에 맞춤) ─────────────────────────────

def render_checks(pdf, deck):
    from html import unescape
    C = d1.Checks()
    with tempfile.TemporaryDirectory() as td:
        html = Path(td) / 'bbox.html'
        import subprocess
        subprocess.run(['pdftotext', '-bbox', str(pdf), str(html)], check=True)
        srcx = html.read_text(encoding='utf-8')
    pages = []
    for pm in re.finditer(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', srcx, flags=re.S):
        w, h, body = float(pm.group(1)), float(pm.group(2)), pm.group(3)
        words = [dict(x0=float(a), y0=float(b), x1=float(c), y1=float(e), t=unescape(t))
                 for a, b, c, e, t in re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', body)]
        pages.append(dict(w=w, h=h, words=words))
    C.add('R1 rendered pages = 9', len(pages) == N_PAGES, len(pages))
    over, outside = [], []
    for i, pg in enumerate(pages):
        ws = pg['words']
        for a in ws:
            if a['x0'] < -0.5 or a['y0'] < -0.5 or a['x1'] > pg['w'] + 0.5 or a['y1'] > pg['h'] + 0.5:
                outside.append((PAGES[i], a['t']))
        for k in range(len(ws)):
            for b in ws[k + 1:]:
                dx = min(ws[k]['x1'], b['x1']) - max(ws[k]['x0'], b['x0'])
                dy = min(ws[k]['y1'], b['y1']) - max(ws[k]['y0'], b['y0'])
                if dx > 1.0 and dy > 1.0:
                    over.append((PAGES[i], ws[k]['t'], b['t'], round(dx, 1), round(dy, 1)))
    C.add('R2 no two rendered words overlap by > 1 pt in both directions', not over, over[:20])
    C.add('R3 every rendered word inside the page', not outside, outside[:20])
    prs = Presentation(str(deck))
    miss, outbox, on_fig = [], [], []
    for i, (s, pg) in enumerate(zip(prs.slides, pages)):
        sx, sy = pg['w'] / inch(d1.SLIDE_W), pg['h'] / inch(d1.SLIDE_H)      # pt per in
        shape_tokens = {}
        for sp in s.shapes:
            txt = sp.text_frame.text if sp.has_text_frame else ''
            if getattr(sp, 'has_table', False) and sp.has_table:
                txt = ' '.join(c.text for r in sp.table.rows for c in r.cells)
            shape_tokens[sp.name] = [t for t in re.split(r'\s+', txt) if len(t) >= 2]
        counts = {}
        for toks in shape_tokens.values():
            for t in set(toks):
                counts[t] = counts.get(t, 0) + 1
        rendered = {}
        for wd in pg['words']:
            rendered.setdefault(wd['t'], []).append(wd)
        boxes = d1.slide_boxes(s)
        for nm, toks in shape_tokens.items():
            x, y, w, h = boxes[nm]
            bx0, by0, bx1, by1 = inch(x) * sx - 2, inch(y) * sy - 2, inch(x + w) * sx + 2, inch(y + h) * sy + 2
            for t in set(toks):
                if counts[t] != 1 or len(rendered.get(t, [])) != 1:
                    continue
                wd = rendered[t][0]
                if not (wd['x0'] >= bx0 and wd['x1'] <= bx1 and wd['y0'] >= by0 and wd['y1'] <= by1):
                    outbox.append((PAGES[i], nm, t, round(wd['x0']), round(wd['y0'])))
        for sp in s.shapes:
            if sp.name == 'hdr/title' and re.sub(r'\s+', '', sp.text_frame.text) not in d1._region_text(pg, boxes[sp.name], sx, sy):
                miss.append((PAGES[i], sp.text_frame.text))
            if sp.shape_type != 13:
                continue
            x, y, w, h = boxes[sp.name]
            for wd in pg['words']:
                cx, cy = (wd['x0'] + wd['x1']) / 2 / sx * d1.EMU, (wd['y0'] + wd['y1']) / 2 / sy * d1.EMU
                if x <= cx <= x + w and y <= cy <= y + h:
                    on_fig.append((PAGES[i], sp.name, wd['t']))
    C.add('R4 unique words of each text box render inside that box (± 2 pt)', not outbox, outbox[:20])
    C.add('R5 page titles rendered in the title box (whitespace-insensitive)', not miss, miss)
    C.add('R6 no slide text rendered over a figure', not on_fig, on_fig[:20])
    return C


# ───────────────────────────── 변이 시험 ─────────────────────────────

def _shape(slide, name):
    hits = [sp for sp in slide.shapes if sp.name == name]
    assert len(hits) == 1, (name, len(hits))
    return hits[0]


def _set_first_run(sp, text):
    runs = [r for p in sp.text_frame.paragraphs for r in p.runs]
    runs[0].text = text
    for r in runs[1:]:
        r.text = ''


def _ban_pattern():
    ban = json.loads(src.rp('docs/reviews/claims.json').read_text(encoding='utf-8')).get('quotation_ban', [])
    pats = [q.get('pattern') if isinstance(q, dict) else q for q in ban]
    return next(p for p in pats if p and len(p) >= 4)


def _mut_font(prs):
    rpr = next(prs.slides[2]._element.iter(qn('a:rPr')))
    rpr.find(qn('a:ea')).set('typeface', 'Arial')


def _mut_cell(prs):
    gf = _shape(prs.slides[5], 'R/table')
    r = gf.table.cell(1, 2).text_frame.paragraphs[0].runs[0]
    r.text = r.text + '9'


MUTATIONS = [
    ('shape overlap (2쪽 L/cap moved onto L/fig)', lambda p: setattr(_shape(p.slides[2], 'L/cap'), 'top', _shape(p.slides[2], 'L/fig').top + I(0.5)),
     'C6 no overlapping'),
    ('text overflow (3쪽 band text made long)', lambda p: _set_first_run(_shape(p.slides[3], 'band/in/text'), '가' * 300), 'C5 every text box'),
    ('forbidden wording on screen (7쪽 note "최적 입도")', lambda p: _set_first_run(_shape(p.slides[7], 'note'), '최적 입도 = 1 µm'), 'C4 forbidden wording absent'),
    ('retracted value (1쪽 note = quotation_ban pattern)', lambda p: _set_first_run(_shape(p.slides[1], 'note'), _ban_pattern()), 'C4 quotation_ban'),
    ('Stage-E outside the limit phrase (4쪽 L/cap)', lambda p: _set_first_run(_shape(p.slides[4], 'L/cap'), 'Stage-E σ 로 비교'), 'C4 "Stage-E"'),
    ('figure not at 100 % (1쪽 R/fig width + 2 %)', lambda p: setattr(_shape(p.slides[1], 'R/fig'), 'width', int(_shape(p.slides[1], 'R/fig').width * 1.02)),
     'C9 every figure placed'),
    ('title ≠ sheet ② (3쪽)', lambda p: _set_first_run(_shape(p.slides[3], 'hdr/title'), '접촉 수는 10배'), 'V1 every screen text'),
    ('table cell ≠ sheet (5쪽 R/table 2.13 → 2.139)', _mut_cell, 'V1 every screen text'),
    ('font outside the set (2쪽 first run ea = Arial)', _mut_font, 'C12 every run'),
    ('shape inside the header band (4쪽 L/cap at y 0.5 in)', lambda p: setattr(_shape(p.slides[4], 'L/cap'), 'top', I(0.5)), 'C6 nothing'),
    ('root shape off the slide (6쪽 note at x 9.5 in)', lambda p: setattr(_shape(p.slides[6], 'note'), 'left', I(9.5)), 'C6 children inside'),
    ('number not in the sheet section (2쪽 note)', lambda p: _set_first_run(_shape(p.slides[2], 'note'), '같은 가압 규약에서 7.77 %p'), 'C8 every number'),
    ('notes ≠ sheet (6쪽 notes)', lambda p: setattr(p.slides[6].notes_slide.notes_text_frame, 'text', '노트 없음'), 'V4 notes'),
]


def selftest(deck):
    """만든 덱을 하나씩 망가뜨려 그 검사가 (새로) 걸리는지 — 만든 덱이 이미 실패한 검사는 실패 내용이 바뀌어야 걸린 것으로 센다."""
    out = []
    base = check_deck(deck)
    base_detail = {c['check']: c['detail'] for c in base.items}
    out.append(dict(mutation='(none — the built deck)', expect='-', ok=True, failed=[c['check'] for c in base.failed]))
    for name, fn, expect in MUTATIONS:
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'm.pptx'
            prs = Presentation(str(deck))
            fn(prs)
            prs.save(str(p))
            C = check_deck(p)
            hit = [c for c in C.failed if c['check'].startswith(expect)]
            caught = any(base_detail.get(c['check']) != c['detail'] for c in hit)
            out.append(dict(mutation=name, expect=expect, ok=caught, failed=[c['check'] for c in C.failed if base_detail.get(c['check']) != c['detail']]))
    bad = [o for o in out[1:] if not o['ok']]
    print(f'selftest (checker mutations): {len(out) - 1} mutations · not caught {len(bad)}')
    for o in bad:
        print('  ✗', o['mutation'], '— expected', o['expect'], '· got', o['failed'])
    return out, len(bad)


# ───────────────────────────── 실행 ─────────────────────────────

def main():
    with estimator3():
        return _main()


def _main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(OUT_DECK))
    ap.add_argument('--render', action='store_true', help='LibreOffice → PDF · 쪽 PNG (draft3/render/) · 렌더 검사')
    ap.add_argument('--check-only', help='기존 덱 검사만')
    ap.add_argument('--pdf', help='--check-only 와 같이: 그 덱의 PDF 렌더 검사')
    ap.add_argument('--determinism', action='store_true', help='임시 폴더에 두 번 만들어 바이트 대조')
    ap.add_argument('--selftest', action='store_true', help='검사기 변이 시험')
    ap.add_argument('--measure', action='store_true', help='패널마다 쌓은 높이 · 넘침 (덱 안 씀)')
    ap.add_argument('--json', default=str(OUT_CHECKS))
    a = ap.parse_args()
    if a.measure:
        measure()
        return 0
    if a.determinism:
        with tempfile.TemporaryDirectory() as td:
            p1, p2 = Path(td) / 'a.pptx', Path(td) / 'b.pptx'
            build(p1)
            build(p2)
            h1, h2 = (hashlib.sha256(p.read_bytes()).hexdigest() for p in (p1, p2))
            print('determinism:', 'same bytes' if h1 == h2 else 'DIFFERENT', h1[:16], h2[:16])
            return 0 if h1 == h2 else 1
    if a.check_only:
        C = check_deck(Path(a.check_only))
        nf = d1.report(C, 'deck checks')
        if a.pdf:
            nf += d1.report(render_checks(Path(a.pdf), Path(a.check_only)), 'render checks')
        return 1 if nf else 0
    out = Path(a.out)
    info = build(out)
    C = check_deck(out, info)
    nf = d1.report(C, 'deck checks')
    ov = overflow_report(out)
    print(f'overflow (panel children below the panel bottom): {len(ov)}')
    for e in ov:
        extra = (f" · chars over {e['chars_over']}/{e['chars_total']}" if 'chars_over' in e else '') + \
                (f" · lines over {e['lines_over']}/{e['lines_total']}" if 'lines_over' in e else '') + \
                (f" · rows over {e['rows_over']}" if 'rows_over' in e else '')
        print(f"  {e['page']}쪽 {e['element']} ({e['kind']}) bottom {e['bottom_in']} > panel {e['panel_bottom_in']} = +{e['over_in']} in"
              f"{' · past slide bottom +' + str(e['slide_bottom_over_in']) if e['slide_bottom_over_in'] else ''}{extra}")
    rec = dict(deck=out.name, deck_sha256=hashlib.sha256(out.read_bytes()).hexdigest(), sheet=SHEET, sheet_sha256=info['sheet']['sha256'],
               checks=C.items, overflow=ov, subscripts=subscript_inventory(info['pages']),
               figures={f'{P["key"]}/{side}': it[1] for P in info['pages'] for side in ('L', 'R') for it in P[side] if it[0] == 'fig'})
    if a.selftest:
        st, nbad = selftest(out)
        rec['selftest'] = st
        nf += nbad
    if a.render:
        pdf, pngs = d1.render(out, outdir=RENDER_DIR, pdf_out=out.with_suffix('.pdf'))
        R = render_checks(pdf, out)
        nf += d1.report(R, 'render checks')
        rec['render'] = dict(pdf=pdf.name, pngs=[p.name for p in pngs], checks=R.items)
    rec['failed'] = nf
    Path(a.json).write_text(json.dumps(rec, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print('written', out, '·', a.json)
    return 1 if nf else 0


if __name__ == '__main__':
    sys.exit(main())
