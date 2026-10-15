#!/usr/bin/env python3
"""연구세미나 덱 생성기 v3.3 (2026-10-15 · Codex v3.2 재확인 HOLD 반영 — SEM32-01–04 · SELF-117 · 1저자 10-15 비준 Q1 (가) · Q2 · 세미나 10-16).

v3.3 = v3.2 덱 (`build_seminar_v32.py` 를 **그대로** 불러 만든다) 위의 차분이다.  바뀌는 장은 3 · 5 · 7 · 11 · 13 · 15 뿐이고
나머지 12 장 (1 · 2 · 4 · 6 · 8 · 9 · 10 · 12 · 14 · 16 · 17 · 18) 은 v3.2 와 글 run · notes · 그림 바이트가 같다 (검사 B3):
  · 3  = 출처 줄 (Codex 문안 · 두 줄 · `This work —` 머리) · notes (대표식 · ② 작은 겹침 근사 · 구현 지렛대 Rᵢ − δᵢⱼ/2 · CDT ω_r = 0 → 토크 0)
         — 식 OMML · 대체 그림 · 그림 = 바이트 그대로 (A8)
  · 5  = notes (큰 입자 LPSCl 펠릿 = 1저자 10-14 승인)
  · 7  = 본문 첫 "300 MPa" 에 (nominal stopping pressure; see Problem 4)
  · 11 = 본문 2 (Codex 문안) · 그림 F_p4_v33 (띠 이름 = registered prediction band) · 해석 줄 (b) · notes
  · 13 = notes 의 Kissel 2026 문장 (Codex 문안)
  · 15 = 흐름도 순서 (… relaxation → unloading → platen removal) · "Heckel analysis to be redone" · notes (같은 순서 · provisional target 문장)

    python3 build_seminar_v33.py --template <10-13 덱.pptx> --eq-deck <10-09 지배방정식.pptx> --repo <리포> --figs figs_v3 --lit <크롭 폴더> --out <out.pptx> \
        [--v32 <비교 v3.2 덱>] [--json <검사 기록>] [--sources-out slide_sources_v33.json]
    python3 build_seminar_v33.py --selftest-only <deck.pptx> --repo <리포> --figs figs_v3 --v32 <v3.2 덱> --v31 <v3.1 덱> --eq-deck <…> [--json <기록>]
    python3 build_seminar_v33.py --dump <deck.pptx> --out <slide_text_v33.md>
"""
import argparse
import hashlib
import importlib
import json
import posixpath
import re
import sys
import zipfile
from pathlib import Path

from lxml import etree
from pptx import Presentation

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_seminar_v32 as v32  # noqa: E402  (v3.2 생성기 · 검사 245 · v3.1 생성기를 그대로 부른다)
import build_seminar_v3 as v3  # noqa: E402

NS = dict(v32.NS)
A, P_, R_, M_ = NS['a'], NS['p'], NS['r'], NS['m']
EMU = 914400
N_SLIDES = 18
#: 바뀌는 장 (Codex v3.2 재확인 · 수정 계획 Q2 = 이 여섯 장의 권고 전부) · 나머지 = v3.2 그대로
CHANGED = (3, 5, 7, 11, 13, 15)
UNCHANGED = tuple(i for i in range(1, N_SLIDES + 1) if i not in CHANGED)
V32_P4_FIG = 'F_p4'
P4_FIG = 'F_p4_v33'

# ───────────────────────────── Codex 문안 (판정문 그대로 · 영어) ─────────────────────────────
#: SEM32-01 (Codex SEMV32-01) — 3 장 출처 줄.  `This work —` 머리 (출처 줄 관례) · 한 줄에 안 들어가 두 줄 (각 줄 ≤ 110 자)
SRC3_LINES = ('This work — representative equations based on LIGGGHTS-PUBLIC 3.8.0 [2]; linear hysteretic law [1].',
              'Equation ② uses the small-overlap approximation ℓᵢⱼ ≈ Rᵢnᵢⱼ.')
SRC3 = ' '.join(SRC3_LINES)
SRC3_OLD = 'This work — implemented equations of LIGGGHTS-PUBLIC 3.8.0 [2]; linear hysteretic law [1]'
SRC_PT = 10
#: 순서 질문 3 — 7 장 본문 첫 "300 MPa"
P7_QUAL = ' (nominal stopping pressure; see Problem 4)'
#: SEM32-02 (Codex SEMV32-02) — 11 장 본문 2 (v3.2 문장 → Codex 교체문) · 빨강 = 두 낱말 묶음 (v3.2 와 같은 다섯 run 꼴)
B11_OLD = ('At fixed platen the same bed relaxes to 165 MPa; a servo branch holding the target force (damping 1e-5) instead compacts it '
           'further (111.05 → 105.84 µm) — model-internal until the open checks pass.')
B11_CODEX = ('At fixed platen, the original run relaxes to 165 MPa. A combined follow-up protocol—plate-contact history reset, lower damping '
             'and force hold—reduces thickness from 111.05 to 105.84 µm. This remains a model-internal diagnostic; static-equilibrium and '
             'conservation checks are pending.')
#: 덱 글 = Codex 문안 + 숫자–단위 사이 줄바꿈 금지 공백 하나 (U+00A0 · v3.2 렌더에서 "105.84 / µm" 이 줄에서 갈렸다) — 글자는 그대로
B11_RUNS = ('At fixed platen, the original run relaxes to 165 MPa. A ', 'combined follow-up protocol',
            '—plate-contact history reset, lower damping and force hold—reduces thickness from 111.05 to 105.84 µm. This remains a ',
            'model-internal diagnostic', '; static-equilibrium and conservation checks are pending.')
B11 = ''.join(B11_RUNS)
assert B11.replace(' ', ' ') == B11_CODEX
#: §5 — 그림 · 해석 줄의 띠 이름
BAND = 'registered prediction band'
CAP11_EDIT = ('shaded = band registered before the run', 'shaded = registered prediction band')
#: SEM32-04 (Codex SEMV32-04) — 13 장 notes 의 Kissel 2026 요약
KISSEL_OLD = 'coating coverage followed the stress intensity rather than the number of stress events'
KISSEL_NEW = ('Coating coverage depended on stress intensity as well as stress number; increasing stress number alone did not collapse '
              'results across rotor speeds.')
#: SEM32-03 (Codex SEMV32-03) — 15 장 흐름도 (1저자 10-14 Q1 비준 = 이완 → 언로딩 → 판 분리)
GEN2_STEPS = ('insertion', 'stabilization', 'compression', 'servo', 'relaxation', 'unloading', 'platen removal')
GEN2_NAVY = ('servo', 'unloading', 'platen removal')
HECKEL_OLD, HECKEL_NEW = 'Heckel analysis redone', 'Heckel analysis to be redone'
#: 순서 질문 4 — 15 장 ε_union 10–13 % 목표 (notes · 작은 글은 단어 한도 120 을 넘어 notes 에만)
PROVISIONAL = 'Provisional geometric calibration target; experimental definition and load state still to be matched.'

#: 바뀌는 도형 글 (v3.2 글 → v3.3 글 · 각 old 는 v3.2 글에 정확히 한 번 · 나머지 도형 글은 그대로 = 검사 B4)
SHAPE_EDITS = {
    3: {'TextBox 69': [(SRC3_OLD, '\n'.join(SRC3_LINES))]},
    7: {'Rectangle 4': [('pressed to 300 MPa; ', 'pressed to 300 MPa' + P7_QUAL + '; ')]},
    11: {'Rectangle 4': [(B11_OLD, B11)], 'Caption': [CAP11_EDIT]},
    15: {'Gen2 box 6': [('platen removal', 'unloading')], 'Gen2 box 7': [('unloading', 'platen removal')],
         'Gen2 note': [(HECKEL_OLD, HECKEL_NEW)]},
}
#: notes 고침 (v3.2 notes → v3.3 notes · 같은 규칙)
NOTE_EDITS = {
    3: [('Qualifiers: these are the implemented equations of the LIGGGHTS-PUBLIC 3.8.0 hooke/hysteresis model [2], read from the source code, '
         'not re-derived by a run;',
         'Qualifiers: these are representative equations based on the LIGGGHTS-PUBLIC 3.8.0 hooke/hysteresis model [2], read from the source '
         'code, not re-derived by a run; equation ② uses the small-overlap approximation ℓᵢⱼ ≈ Rᵢnᵢⱼ — on the spherical-particle path the '
         'implemented lever arm has magnitude Rᵢ − δᵢⱼ/2 (contact radius cri = radi − 0.5·deltan; LIGGGHTS-PUBLIC commit 3d5c00f, '
         'surface_model_default.h lines 173–188 and tangential_model_history.h lines 254–261; '
         'docs/dem_governing_equations_background_20261011.md §3.1);'),
        ('the rolling torque uses k_n δ, not the hysteretic normal force;',
         'the rolling torque uses k_n δ, not the hysteretic normal force; the CDT rolling torque is zero when the relative angular velocity '
         'is zero (the direction ω_r/‖ω_r‖ is used only for ‖ω_r‖ > 0; rolling_model_cdt.h lines 94 and 138; torsion torque off);')],
    5: [('(listed by the author on 10-14 for this deck; the progress log of 10-14 evening still records it as a recommendation awaiting an '
         'answer)',
         '(one large-particle LPSCl pellet added to the EIS plan, approved by the author on 10-14; docs/session_20260923_progress.md, '
         '10-14 night 9 entry)')],
    11: [('B2 (104.9 µm, band 103–107 µm; ε_sphere 10.0 %, band 8.3–11.7 %) contains the result.',
          'B2 (104.9 µm, band 103–107 µm; ε_sphere 10.0 %, band 8.3–11.7 %) contains the result; the shaded band in (b) is this registered '
          'prediction band — a model prediction registered before the run, not an experimental range or a statistical confidence interval.'),
         ('Figure F_p4 is redrawn from these recorded values only (docs/seminar_20261013/figs_v3/make_seminar_figs_v32.py).',
          'Figure F_p4_v33 is redrawn from these recorded values only (docs/seminar_20261013/figs_v3/make_seminar_figs_v33.py: the drawing '
          'code of make_seminar_figs_v32.py with the band label added).'),
         ('the comparison is limited to this bed and loading history.',
          'the comparison is limited to this bed and loading history. Passing these internal checks would qualify the numerical state of '
          'this bed; it would not validate the model against experiment.')],
    13: [('single-crystal NCM: coating coverage followed the stress intensity rather than the number of stress events.',
          'single-crystal NCM. ' + KISSEL_NEW)],
    15: [('→ relaxation → platen removal → unloading, so the unloading logic is a prerequisite;',
          '→ relaxation → unloading → platen removal (order ratified on 10-14: docs/reviews/dem_protocol_gen2_plan_draft_20261014.md Q1; '
          'docs/session_20260923_progress.md, 10-14 night 7 entry), so the unloading logic is a prerequisite;'),
         ('MV-03); Heckel analysis redone, because', 'MV-03); Heckel analysis to be redone, because'),
         ('apparent coefficient of the old protocol (same review, Q2).',
          'apparent coefficient of the old protocol (same review, Q2). ε_union 10–13 %: ' + PROVISIONAL + ' It is a planned geometric '
          'target for the new protocol, not the existing 10 % calibration target on the MPM-inputs slide.')],
}
#: 장별 필수 · 금지 (대소문자 무시 · notes 는 notes 글 · 장 글 = 장 XML 의 모든 a:t)
REQ_NOTES = {
    3: ['representative equations based on the liggghts-public 3.8.0', 'small-overlap approximation ℓᵢⱼ ≈ rᵢnᵢⱼ', 'rᵢ − δᵢⱼ/2',
        'surface_model_default.h lines 173–188', 'tangential_model_history.h lines 254–261', 'commit 3d5c00f',
        'docs/dem_governing_equations_background_20261011.md §3.1', 'zero when the relative angular velocity is zero'],
    5: ['large-particle lpscl pellet added to the eis plan, approved by the author on 10-14', '10-14 night 9 entry'],
    11: ['resets the normal plastic contact history', 'combined protocol (history reset + damping drop + force hold)', '13 se lost',
         'the 13 lost particles are se', 'registered prediction band', 'not an experimental range or a statistical confidence interval',
         'would not validate the model against experiment', 'make_seminar_figs_v33.py'],
    13: ['kissel 2026 [6]', KISSEL_NEW.lower()],
    15: ['relaxation → unloading → platen removal', 'heckel analysis to be redone', PROVISIONAL.lower(),
         'dem_protocol_gen2_plan_draft_20261014.md q1'],
}
FORBID_ALL = ['implemented equations', 'until the open checks pass', KISSEL_OLD]   # 장 글 + notes 어디에도 (대소문자 무시)
FORBID_RE = [r'(?i)heckel analysis redone']                                       # "to be" 없는 옛 문구
FORBID_NOTES = {5: ['awaiting an answer', 'still records it as a recommendation'], 15: ['relaxation → platen removal']}
#: 단어 한도 (v3.2 규칙: 100 / 넓은 장 120) 를 넘는 장 = Codex 필수 문안이 늘린 만큼만 허용 (늘어난 단어 = 위 SHAPE_EDITS 의 차)
MANDATED_GROWTH_SLIDES = (7, 11, 15)
#: 3 장 출처 줄 — 두 줄 글 바닥 추정 상한 (in) · 제목 글자 윗선 ≈ 1.35 in (v3.2 렌더) 보다 0.08 in 위
SRC3_BOTTOM_MAX = 1.27


# ───────────────────────────── 읽기 (python-pptx 와 독립 · Codex inspect 와 같은 규칙) ─────────────────────────────

def _xml_texts(el):
    return el.xpath('.//a:t/text() | .//m:t/text()', namespaces=NS)


def deck_fp(path):
    """장마다 글 run (a:t · m:t 문서 순서) · notes run · 그림 sha256 (정렬) · 식 (m:oMathPara C14N).  Codex 판정 증거 `inspect_deck.py` 의 extract 와 같은 규칙."""
    out = []
    with zipfile.ZipFile(path) as z:
        def rels(part):
            d, f = posixpath.split(part)
            rp = f'{d}/_rels/{f}.rels'
            if rp not in z.namelist():
                return []
            return [(n.get('Target'), n.get('Type'), n.get('TargetMode') == 'External') for n in etree.fromstring(z.read(rp))]
        pres = etree.fromstring(z.read('ppt/presentation.xml'))
        prel = {n.get('Id'): n.get('Target') for n in etree.fromstring(z.read('ppt/_rels/presentation.xml.rels'))}
        for sid in pres.findall('p:sldIdLst/p:sldId', NS):
            part = posixpath.normpath('ppt/' + prel[sid.get('{%s}id' % R_)])
            root = etree.fromstring(z.read(part))
            notes, media = [], []
            for tgt, typ, ext in rels(part):
                if ext:
                    continue
                loc = posixpath.normpath(posixpath.dirname(part) + '/' + tgt)
                if typ.endswith('/notesSlide'):
                    notes = _xml_texts(etree.fromstring(z.read(loc)))
                if typ.endswith('/image'):
                    media.append(hashlib.sha256(z.read(loc)).hexdigest())
            eqs = [etree.tostring(e, method='c14n').decode() for e in root.xpath('.//m:oMathPara', namespaces=NS)]
            out.append(dict(texts=_xml_texts(root), notes=notes, media=sorted(media), equations=eqs))
    return out


def _norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def shape_texts(slide):
    """(도형 이름, 글) — 무리 안 · 표 포함 · python-pptx 순서."""
    out = []
    for sh in v32.iter_shapes(slide.shapes):
        if sh.has_text_frame:
            out.append((sh.name, sh.text_frame.text))
        if getattr(sh, 'has_table', False) and sh.has_table:
            out.append((sh.name, '\n'.join(' | '.join(c.text for c in r.cells) for r in sh.table.rows)))
    return out


def apply_edits(text, edits, where=''):
    """(old, new) 를 차례로 — old 는 정확히 한 번 있어야 한다 (아니면 AssertionError · 조용히 넘어가지 않는다)."""
    for old, new in edits:
        k = text.count(old)
        assert k == 1, (where, k, old[:80])
        text = text.replace(old, new)
    return text


def _words(t):
    return len(t.split())


# ───────────────────────────── 검사 (v3.2 검사 245 유지 + v3.3 · 시험 먼저 = v3.2 덱에서 실패 확인) ─────────────────────────────

def _a9_v33(slides, figs):
    """(v3.2 A9 'slide 11 carries F_p4.png' 의 v3.3 판) 띠 이름을 바꾼 새 그림 파일 F_p4_v33.png."""
    name = 'A9 slide 11 carries F_p4_v33.png byte-identical (v3.3: band renamed — figure file F_p4 → F_p4_v33)'
    if not figs or len(slides) < 11:
        return name, False, 'no figs dir or < 11 slides'
    png = Path(figs) / f'{P4_FIG}.png'
    pics = [sh for sh in slides[10].shapes if sh.shape_type == 13]
    return name, png.exists() and any(sh.image.blob == png.read_bytes() for sh in pics), f'{png.name} exists={png.exists()}'


def _src_lines_v33(slides):
    """(v3.2 A10 'source lines ≤ 110 characters' 의 v3.3 판) 줄마다 ≤ 110 자 · 한 줄 · 3 장만 두 줄 (Codex SEM32-01 문장 162 자)."""
    name = 'A10 source lines ≤ 110 characters per line; one line, slide 3 two lines (v3.3: SEM32-01 sentence = 162 characters)'
    bad = []
    for i, s in enumerate(slides, 1):
        for sh in s.shapes:
            if sh.name != 'TextBox 69':
                continue
            paras = [p.text for p in sh.text_frame.paragraphs if p.text.strip()]
            if len(paras) != (2 if i == 3 else 1) or '\v' in sh.text_frame.text:
                bad.append((i, 'lines', len(paras)))
            w = sh.width / EMU - (sh.text_frame.margin_left + sh.text_frame.margin_right) / EMU
            for t in paras:
                if len(t) > 110 or v3.est_lines(t, SRC_PT, w) != 1:
                    bad.append((i, len(t), v3.est_lines(t, SRC_PT, w)))
    return name, not bad, str(bad)


def _words_v33(prs, ref_prs):
    """(v3.2 A10 'words ≤ 100 / 120' 의 v3.3 판) 한도는 그대로 · 7 · 11 · 15 장만 Codex 필수 문안이 늘린 만큼 넘을 수 있다 (그보다 더는 안 된다)."""
    name = ('A10 words ≤ 100 / 120 (small print, tables, groups excluded; v3.3: slides 7 · 11 · 15 may exceed only by the words the '
            'Codex-mandated wording adds)')
    st = v32.slide_stats_v32(prs)
    st0 = v32.slide_stats_v32(ref_prs) if ref_prs is not None else None
    bad = []
    for i, (w, _, _) in enumerate(st, 1):
        if not 2 <= i <= 16:
            continue
        cap = 120 if i in v32.WIDE else 100
        if w <= cap:
            continue
        if i in MANDATED_GROWTH_SLIDES and st0 is not None:
            grow = sum(_words(new) - _words(old) for eds in SHAPE_EDITS.get(i, {}).values() for old, new in eds)
            if w - st0[i - 1][0] <= grow:
                continue
            bad.append((i, w, cap, f'v3.2 {st0[i - 1][0]} + mandated {grow}'))
        else:
            bad.append((i, w, cap))
    return name, not bad, str(bad)


ADAPTED = {'A9 slide 11 carries F_p4.png byte-identical': 'a9',
           'A10 source lines ≤ 110 characters': 'src',
           'A10 words ≤ 100 / 120 (small print, tables, groups excluded)': 'words'}


def selftest_v33(deck, repo, figs=None, v32_ref=None, v31=None, eq_deck=None):
    """v3.2 검사 (245 · 옛 문구 · 옛 파일을 강제하던 셋은 v3.3 판으로 바꿈) + v3.3 검사 B1–B6.  모든 실패를 모은다."""
    repo = Path(repo)
    base = v32.selftest_v32(deck, repo, figs, v31, eq_deck)
    prs = Presentation(str(deck))
    slides = list(prs.slides)
    n = len(slides)
    ref = Presentation(str(v32_ref)) if v32_ref else None
    C = v32.Checks()
    done = set()
    for nm, ok, det in base.items:
        kind = ADAPTED.get(nm)
        if kind == 'a9':
            C.add(*_a9_v33(slides, figs))
        elif kind == 'src':
            C.add(*_src_lines_v33(slides))
        elif kind == 'words':
            C.add(*_words_v33(prs, ref))
        else:
            C.items.append((nm, ok, det))
        if kind:
            done.add(nm)
    for nm in ADAPTED:
        if nm not in done and not (nm.startswith('A9') and not figs):
            C.add(f'v3.2 check present to adapt: {nm}', False, 'not in the v3.2 check run')

    texts = [v32.xml_text(s) for s in slides]
    notes = [s.notes_slide.notes_text_frame.text if s.has_notes_slide else '' for s in slides]
    low, lown = [t.lower() for t in texts], [t.lower() for t in notes]
    C.add('B0 slide count = 18 (v3.3)', n == N_SLIDES, str(n))
    if n < N_SLIDES:
        return C

    # B1 금지 문구 — 장 글 + notes (대소문자 무시)
    for f in FORBID_ALL:
        hits = [(i, w) for i in range(1, n + 1) for w, body in (('slide', low[i - 1]), ('notes', lown[i - 1])) if f.lower() in body]
        C.add(f'B1 forbidden "{f[:48]}" absent (slides + notes)', not hits, str(hits))
    for pat in FORBID_RE:
        hits = [(i, w) for i in range(1, n + 1) for w, body in (('slide', texts[i - 1]), ('notes', notes[i - 1])) if re.search(pat, body)]
        C.add(f'B1 forbidden pattern {pat} absent (slides + notes)', not hits, str(hits))
    for i, fs in FORBID_NOTES.items():
        bad = [f for f in fs if f.lower() in lown[i - 1]]
        C.add(f'B1 forbidden notes wording slide {i}', not bad, str(bad))
    boxes = {}
    for sh in slides[14].shapes:
        mo = re.fullmatch(r'Gen2 box (\d)', sh.name)
        if mo and sh.has_text_frame:
            boxes[int(mo.group(1))] = _norm(sh.text_frame.text)
    order = [boxes.get(k, '') for k in range(1, 8)]
    pairs = list(zip(order, order[1:]))
    C.add('B1 slide 15 flow: relaxation is not followed directly by platen removal', ('relaxation', 'platen removal') not in pairs, str(order))

    # B2 필수 문안
    src = [sh for sh in slides[2].shapes if sh.name == 'TextBox 69']
    sp = [p.text for p in src[0].text_frame.paragraphs if p.text.strip()] if src else []
    C.add('B2 slide 3 source line = Codex SEMV32-01 wording with the "This work —" head (two lines)',
          tuple(sp) == SRC3_LINES and _norm(' '.join(sp)) == SRC3, str(sp)[:200])
    for i, rs in REQ_NOTES.items():
        miss = [r for r in rs if r.lower() not in lown[i - 1]]
        C.add(f'B2 required notes slide {i}', not miss, str(miss))
    C.add('B2 slide 13 notes: Kissel sentence = Codex SEMV32-04 wording (exact)', KISSEL_NEW in notes[12])
    body7 = [sh.text_frame.text for sh in slides[6].shapes if sh.name == 'Rectangle 4']
    b7 = body7[0] if body7 else ''
    m300 = [mo.start() for mo in re.finditer(r'300\s?MPa', b7)]
    first_ok = bool(m300) and b7[m300[0]:].startswith('300 MPa' + P7_QUAL)
    #  "첫 언급" = 본문이 이 장에서 300 MPa 를 말하는 유일한 글 상자여야 한다 (해석 줄 · 꼬리표 · 출처 줄은 말하지 않는다)
    others = [sh.name for sh in slides[6].shapes if sh.name != 'Rectangle 4' and sh.has_text_frame and re.search(r'300\s?MPa', sh.text_frame.text)]
    C.add('B2 slide 7: first "300 MPa" carries "(nominal stopping pressure; see Problem 4)"', first_ok and not others, f'{b7[:140]} · {others}')
    body11 = [sh for sh in slides[10].shapes if sh.name == 'Rectangle 4']
    paras11 = [p.text for p in body11[0].text_frame.paragraphs if p.text.strip()] if body11 else []
    C.add('B2 slide 11 body 2 = Codex SEMV32-02 wording (exact; one no-break space between 105.84 and µm)',
          len(paras11) == 3 and paras11[2] == B11 and paras11[2].replace(' ', ' ') == B11_CODEX, str(paras11[2:])[:200])
    red11 = []
    if body11 and len(body11[0].text_frame.paragraphs) > 2:
        for r in body11[0].text_frame.paragraphs[2].runs:
            sf = r._r.find('{%s}rPr/{%s}solidFill/{%s}srgbClr' % (A, A, A))
            if sf is not None and sf.get('val') == v32.RED:
                red11.append(r.text)
    C.add('B2 slide 11 body 2 highlights = "combined follow-up protocol" · "model-internal diagnostic"',
          red11 == [B11_RUNS[1], B11_RUNS[3]], str(red11))
    tab11 = ' '.join(c.text for sh in slides[10].shapes if getattr(sh, 'has_table', False) and sh.has_table
                     for r in sh.table.rows for c in r.cells).lower()
    C.add('B2 slide 11 table keeps the history-reset and 13-SE-lost rows', 'contact history reset' in tab11 and '13 se particles lost' in tab11, tab11[:160])
    cap11 = ' '.join(sh.text_frame.text for sh in slides[10].shapes if sh.name == 'Caption')
    C.add('B2 slide 11 caption names the registered prediction band', CAP11_EDIT[1] in cap11, cap11[-160:])
    C.add('B2 slide 15 flow boxes = insertion → … → relaxation → unloading → platen removal', tuple(order) == GEN2_STEPS, str(order))
    sty = []
    for sh in slides[14].shapes:
        mo = re.fullmatch(r'Gen2 box (\d)', sh.name)
        if mo:
            r0 = sh.text_frame.paragraphs[0].runs[0]
            want_navy = _norm(sh.text_frame.text) in GEN2_NAVY
            col = sh.line.color.rgb if sh.line.color and sh.line.color.type is not None else None
            if bool(r0.font.bold) != want_navy or str(col) != (v32.NAVY if want_navy else v32.GRAY):
                sty.append((sh.name, sh.text_frame.text, r0.font.bold, str(col)))
    C.add('B2 slide 15 flow box style: servo · unloading · platen removal navy bold, others gray', not sty, str(sty))
    note15 = ' '.join(sh.text_frame.text for sh in slides[14].shapes if sh.name == 'Gen2 note')
    C.add('B2 slide 15 note line: "Heckel analysis to be redone"', HECKEL_NEW in note15, note15[-80:])

    # B3 바뀌지 않은 12 장 = v3.2 (글 run · notes · 그림 바이트 · 식) · 바뀐 장의 식 · 그림
    if v32_ref:
        a, b = deck_fp(deck), deck_fp(v32_ref)
        for i in UNCHANGED:
            for k in ('texts', 'notes', 'media', 'equations'):
                C.add(f'B3 unchanged slide {i} = v3.2 ({k})', a[i - 1][k] == b[i - 1][k], 'differs')
        for i in CHANGED:
            C.add(f'B3 changed slide {i}: equations = v3.2', a[i - 1]['equations'] == b[i - 1]['equations'], 'differs')
            if i == 11:
                old_png = Path(figs) / f'{V32_P4_FIG}.png' if figs else None
                new_png = Path(figs) / f'{P4_FIG}.png' if figs else None
                ok = bool(figs) and new_png.exists()
                if ok:
                    want = sorted(set(b[10]['media']) - {hashlib.sha256(old_png.read_bytes()).hexdigest()}
                                  | {hashlib.sha256(new_png.read_bytes()).hexdigest()})
                    ok = a[10]['media'] == want and len(b[10]['media']) == len(a[10]['media'])
                C.add('B3 slide 11 pictures = v3.2 with F_p4.png replaced by F_p4_v33.png', ok, str(a[10]['media'])[:120])
            else:
                C.add(f'B3 changed slide {i}: pictures = v3.2 (bytes)', a[i - 1]['media'] == b[i - 1]['media'], 'differs')
    else:
        C.add('B3 identity check needs --v32', False, 'no v3.2 deck given')

    # B4 바뀐 장 = v3.2 + 등록한 고침만 (도형 글 · notes) — 다른 글은 한 글자도 그대로
    if ref is not None:
        rs = list(ref.slides)
        for i in CHANGED:
            new_t, old_t = shape_texts(slides[i - 1]), shape_texts(rs[i - 1])
            C.add(f'B4 slide {i}: same text shapes as v3.2', [x for x, _ in new_t] == [x for x, _ in old_t],
                  str(sorted(set(x for x, _ in new_t) ^ set(x for x, _ in old_t))))
            if [x for x, _ in new_t] != [x for x, _ in old_t]:
                continue
            bad = []
            for (nm, t1), (_, t0) in zip(new_t, old_t):
                eds = SHAPE_EDITS.get(i, {}).get(nm)
                try:
                    want = apply_edits(t0, eds, f'{i} {nm}') if eds else t0
                except AssertionError as e:
                    bad.append((nm, 'edit not applicable to v3.2 text', str(e)[:80]))
                    continue
                if t1 != want:
                    bad.append((nm, t1[:60]))
            C.add(f'B4 slide {i}: shape texts = v3.2 + registered edits only', not bad, str(bad)[:240])
            n0 = rs[i - 1].notes_slide.notes_text_frame.text
            try:
                want = apply_edits(n0, NOTE_EDITS.get(i, []), f'{i} notes')
                C.add(f'B4 slide {i}: notes = v3.2 + registered edits only', notes[i - 1] == want, 'differs')
            except AssertionError as e:
                C.add(f'B4 slide {i}: notes = v3.2 + registered edits only', False, f'edit not applicable: {e}'[:160])
    else:
        C.add('B4 edit check needs --v32', False, 'no v3.2 deck given')

    # B5 자리 — 3 장 출처 줄 두 줄이 제목 위에서 끝난다 · 11 장 그림 · 표 · 해석 줄
    if src:
        sh = src[0]
        tf = sh.text_frame
        lines = len([p for p in tf.paragraphs if p.text.strip()])
        spc = tf.paragraphs[0].line_spacing if tf.paragraphs and isinstance(tf.paragraphs[0].line_spacing, float) else 1.0
        bottom = sh.top / EMU + (tf.margin_top or 0) / EMU + lines * SRC_PT * 1.2 * spc / 72
        C.add(f'B5 slide 3 source text ends above the title (estimate ≤ {SRC3_BOTTOM_MAX} in)', bottom <= SRC3_BOTTOM_MAX, f'{bottom:.3f}')
    pic11 = [sh for sh in slides[10].shapes if sh.name == 'Fig plate reaction']
    tbl11 = [sh for sh in slides[10].shapes if sh.name == 'Table checks']
    if pic11 and body11:
        est = v3.est_body_bottom(paras11[0], paras11[1:]) if len(paras11) > 1 else 0
        C.add('B5 slide 11 figure and table below the body text (estimate)', pic11[0].top / EMU >= est + 0.02
              and bool(tbl11) and tbl11[0].top / EMU >= est + 0.02, f'body {est:.2f} fig {pic11[0].top / EMU:.2f}')
    else:
        C.add('B5 slide 11 figure and table below the body text (estimate)', False, 'missing shapes')

    # B6 그림 F_p4_v33 — 값 · 빗금 = F_p4 (v3.2) · 띠 이름 = registered prediction band
    if figs:
        figs = Path(figs)
        have = all((figs / f'{P4_FIG}.{e}').exists() for e in ('png', 'svg', 'csv'))
        C.add('B6 F_p4_v33 files exist (png · svg · csv)', have)
        if have:
            sys.path.insert(0, str(figs))
            fm = importlib.import_module('make_seminar_figs_v33')
            fails = fm.check_fig_files(figs / f'{P4_FIG}.svg', figs / f'{P4_FIG}.csv', figs / f'{V32_P4_FIG}.svg', figs / f'{V32_P4_FIG}.csv')
            C.add('B6 F_p4_v33 = F_p4 values · hatch · bars, band named "registered prediction band"', not fails, str(fails)[:240])
    return C


# ───────────────────────────── 생성 (v3.2 덱 위 차분) ─────────────────────────────

def _replace_in_run(shape, old, new):
    """old → new 를 run 하나 안에서 (run 서식 그대로) — old 는 그 도형에 정확히 한 번 · 한 run 안에 있어야 한다."""
    hits = [r for p in shape.text_frame.paragraphs for r in p.runs if old in r.text]
    assert len(hits) == 1 and hits[0].text.count(old) == 1, (shape.name, old, len(hits))
    hits[0].text = hits[0].text.replace(old, new)


def _source_two_lines(sp, top=0.93):
    """3 장 출처 줄: 한 문단 → 두 문단 (같은 run 서식 · 오른쪽 맞춤) · 위아래 여백 0 · 높이 = 두 줄.  각 줄 ≤ 110 자 (검사 A10′)."""
    body = sp.text_frame._txBody
    p0 = body.find('{%s}p' % A)
    pars = []
    for line in SRC3_LINES:
        p = etree.fromstring(etree.tostring(p0))
        for e in p.findall('{%s}endParaRPr' % A):
            p.remove(e)
        runs = p.findall('{%s}r' % A)
        assert len(runs) == 1, len(runs)
        runs[0].find('{%s}t' % A).text = line
        pars.append(p)
    idx = list(body).index(p0)
    body.remove(p0)
    for k, p in enumerate(pars):
        body.insert(idx + k, p)
    bp = body.find('{%s}bodyPr' % A)
    bp.set('tIns', '0')
    bp.set('bIns', '0')
    h = round(len(SRC3_LINES) * SRC_PT * 1.2 / 72 + 0.01, 3)
    v3.place(sp, (sp.left / EMU, top, sp.width / EMU, h))


def _edit_notes(slide, i):
    v3.notes(slide, apply_edits(slide.notes_slide.notes_text_frame.text, NOTE_EDITS[i], f'{i} notes'))


def build_v33(template, repo, figs, lit, eq_deck, out, v32_out=None, v31_out=None):
    """v3.2 를 그대로 만든 뒤 (build_seminar_v32.build_v32) 3 · 5 · 7 · 11 · 13 · 15 장만 고친다.  → (출처 dict, v3.2 기반 덱, v3.1 기반 덱)."""
    repo, figs, out = Path(repo), Path(figs), Path(out)
    v32_path = Path(v32_out) if v32_out else out.with_name(out.stem + '_base_v32.pptx')
    S32, v31 = v32.build_v32(template, repo, figs, lit, eq_deck, str(v32_path), v31_out)
    prs = Presentation(str(v32_path))
    sl = list(prs.slides)
    assert len(sl) == N_SLIDES, len(sl)

    # ── 3 — 출처 줄 (SEM32-01 · Codex 문안 · 두 줄) · notes.  식 · 그림 · 판 = 손대지 않음 ──
    _source_two_lines(v3.shape(sl[2], 'TextBox 69'))
    _edit_notes(sl[2], 3)
    # ── 5 — notes (큰 입자 LPSCl 펠릿 = 1저자 10-14 승인) ──
    _edit_notes(sl[4], 5)
    # ── 7 — 본문 첫 "300 MPa" (순서 질문 3) ──
    _replace_in_run(v3.shape(sl[6], 'Rectangle 4'), 'pressed to 300 MPa; ', 'pressed to 300 MPa' + P7_QUAL + '; ')
    # ── 11 — 본문 2 (SEM32-02 · 같은 다섯 run 꼴: 보통 · 빨강 · 보통 · 빨강 · 보통) · 그림 F_p4_v33 · 해석 줄 (b) · notes ──
    s = sl[10]
    bx = v3.shape(s, 'Rectangle 4')
    paras = bx.text_frame.paragraphs
    assert paras[2].text == B11_OLD and len(paras[2].runs) == len(B11_RUNS), paras[2].text
    for r, t in zip(paras[2].runs, B11_RUNS):
        r.text = t
    head, b1 = paras[0].text, paras[1].text
    pic = v3.shape(s, 'Fig plate reaction')
    ft_old = round(pic.top / EMU, 2)
    fh = round(v3.FZ_BOTTOM - ft_old - 0.50, 2)                    # v3.2 그림 띠 높이 그대로 (그림 크기 · 글씨 크기 같음)
    ft = max(v3.FT_MIN, round(v3.est_body_bottom(head, [b1, B11]) + v3.FT_MARGIN, 2))
    tree = pic._element.getparent()
    z = list(tree).index(pic._element)                            # v3.2 그림의 쌓임 순서 자리 (새 그림을 같은 자리에)
    tree.remove(pic._element)
    new_pic = v3.place_pic(s, figs / f'{P4_FIG}.png', (0.45, ft, 5.45, fh), name='Fig plate reaction')
    tree.remove(new_pic._element)
    tree.insert(z, new_pic._element)
    tbl = v3.shape(s, 'Table checks')
    v3.place(tbl, (tbl.left / EMU, round(ft + 0.15, 2), tbl.width / EMU, tbl.height / EMU))
    cap = v3.shape(s, 'Caption')
    v3.place(cap, (cap.left / EMU, round(ft + fh + 0.04, 2), cap.width / EMU, cap.height / EMU))
    _replace_in_run(cap, *CAP11_EDIT)
    v3.place(bx, (0.61, v3.BODY_TOP, 8.84, round(ft - v3.BODY_TOP - 0.05, 2)))
    v32._prune_image_rels(s)
    v32._unique_ids(s)
    _edit_notes(s, 11)
    print(f'slide 11 layout: figure band top {ft_old} → {ft} in (height {fh} in kept) · caption bottom {round(ft + fh + 0.04 + cap.height / EMU, 2)} in')
    # ── 13 — notes 의 Kissel 2026 문장 (SEM32-04) ──
    _edit_notes(sl[12], 13)
    # ── 15 — 흐름도 순서 (SEM32-03 · 두 상자 글만 바꿈 · 둘 다 남색 굵게 = 서식 같음) · 작은 글 · notes ──
    s = sl[14]
    _replace_in_run(v3.shape(s, 'Gen2 box 6'), 'platen removal', 'unloading')
    _replace_in_run(v3.shape(s, 'Gen2 box 7'), 'unloading', 'platen removal')
    _replace_in_run(v3.shape(s, 'Gen2 note'), HECKEL_OLD, HECKEL_NEW)
    _edit_notes(s, 15)

    prs.save(str(out))
    S = dict(S32)
    S['3'] += ('; v3.3 (Codex v3.2 re-check SEMV32-01 = ledger SEM32-01): source line = Codex wording (representative equations; equation ② '
               'small-overlap approximation ℓᵢⱼ ≈ Rᵢnᵢⱼ); notes = implemented lever arm Rᵢ − δᵢⱼ/2 (LIGGGHTS-PUBLIC 3d5c00f '
               'surface_model_default.h 173–188 · tangential_model_history.h 254–261 · docs/dem_governing_equations_background_20261011.md §3.1) '
               'and CDT torque zero at ω_r = 0 (rolling_model_cdt.h 94 · 138); equation objects, fallback images and pictures unchanged (A8)')
    S['5'] += ('; v3.3: large-particle LPSCl pellet approved by the author on 10-14 (docs/session_20260923_progress.md, 10-14 night 9 entry; '
               'Codex v3.2 re-check Q5)')
    S['7'] += '; v3.3: first "300 MPa" = nominal stopping pressure, see Problem 4 (Codex v3.2 re-check, order question 3)'
    S['11'] += ('; v3.3 (SEMV32-02 = SEM32-02): body 2 = Codex wording (combined follow-up protocol; model-internal diagnostic; '
                'static-equilibrium and conservation checks pending); figure F_p4_v33 = F_p4 values with the band named "registered prediction '
                'band" (Codex §5; figs_v3/make_seminar_figs_v33.py)')
    S['13'] += '; v3.3 (SEMV32-04 = SEM32-04): Kissel 2026 sentence = Codex wording (stress intensity as well as stress number)'
    S['15'] += ('; v3.3 (SEMV32-03 = SEM32-03): flow relaxation → unloading → platen removal = author 10-14 Q1 '
                '(docs/reviews/dem_protocol_gen2_plan_draft_20261014.md · progress log 10-14 night 7 entry); "Heckel analysis to be redone"; '
                'notes = provisional geometric calibration target (Codex v3.2 re-check, order question 4)')
    Path(str(out) + '.sources.json').write_text(json.dumps(S, ensure_ascii=False, indent=1), encoding='utf-8')
    return S, v32_path, v31


def dump_text_v33(deck, out):
    v32.dump_text_v32(deck, out)
    lines = Path(out).read_text(encoding='utf-8').split('\n')
    lines[0] = ('# 연구세미나 덱 v3.3 (18 장 · Codex v3.2 재확인 반영 · 1저자 10-15 비준) — 장별 글 전문 (생성기 출력에서 추출 · 표 · 출처 줄 · '
                '무리 안 라벨 · 식 이름 · 다리 줄 · notes 포함)')
    Path(out).write_text('\n'.join(lines), encoding='utf-8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--template')
    ap.add_argument('--eq-deck', help='1저자 10-09 DEM 지배방정식 슬라이드 (식 OMML · 그림 원본 · A8)')
    ap.add_argument('--repo')
    ap.add_argument('--figs')
    ap.add_argument('--lit')
    ap.add_argument('--out')
    ap.add_argument('--v32', help='비교 v3.2 덱 (B3 · B4 · 단어 차) — 생성 때 없으면 같은 빌드의 v3.2 기반 덱')
    ap.add_argument('--v31', help='v3.1 덱 (v3.2 검사 A5) — 생성 때는 자동')
    ap.add_argument('--json', help='검사 결과 기록 (JSON)')
    ap.add_argument('--sources-out', help='장별 출처 JSON 사본 (리포의 slide_sources_v33.json)')
    ap.add_argument('--selftest-only', help='기존 덱 검사만')
    ap.add_argument('--dump', help='덱의 장별 글 전문을 --out (md) 로')
    a = ap.parse_args()
    if a.dump:
        dump_text_v33(a.dump, a.out)
        return 0
    if a.selftest_only:
        C = selftest_v33(a.selftest_only, a.repo, a.figs, a.v32, a.v31, a.eq_deck)
        return 1 if v32.report_checks(C, a.json, label=Path(a.selftest_only).name) else 0
    S, v32_base, v31 = build_v33(a.template, a.repo, a.figs, a.lit, a.eq_deck, a.out)
    if a.sources_out:
        Path(a.sources_out).write_text(json.dumps(S, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    C = selftest_v33(a.out, a.repo, a.figs, a.v32 or v32_base, a.v31 or v31, a.eq_deck)
    nf = v32.report_checks(C, a.json, label=Path(a.out).name)
    print('written', a.out)
    return 1 if nf else 0


if __name__ == '__main__':
    sys.exit(main())
