#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""리뷰 finding 원장 검사 — "응답 문서는 있었는데 다음 작업 목록에서 사라짐" 을 막는다.

★ 왜 필요한가 (실제로 일어난 일): Codex 5회차 리뷰(2026-08-07)가 **4일간 처리되지
  않았다**.  응답 문서도 쓰고 회귀도 붙였는데, 다음 세션에서 그 문서가 큐에 없었다.
  사용자가 "이것도 반영이 된 건가?" 라고 묻기 전까지 아무도 몰랐다.  산문으로 상태를
  적으면 다시 새어나간다 — **기계가 읽는 단일 원장**이 필요하다 (Codex Q8).

원장: `docs/reviews/findings.json`
  {"findings": [ {id, severity, status, owner, opened_in, claimed_fixed_sha,
                  verified_sha, evidence_tests, supersedes, decision_note}, … ]}

이 검사가 강제하는 것:
  ① ID 중복 없음 · 형식(RC6-01 류) 준수
  ② `claimed_fixed` 는 fix SHA **와** 회귀 근거(evidence_tests)를 **둘 다** 가진다
  ③ `verified` 는 **구현자와 다른** 검증자(verified_by)가 있어야 한다
     — 자기가 고치고 자기가 검증했다고 닫는 것을 막는다 (이번 라운드의 교훈:
       "구현자의 회귀 PASS 와 결함 종료는 같은 뜻이 아니다")
  ④ 열린 항목(open/claimed_fixed)을 **항상 화면에 뽑는다** — 다음 리뷰 요청 문서가
     그 목록을 그대로 실을 수 있게

⚠ 이 검사는 원장의 **자기일관성**만 본다.  "정말 고쳐졌는가" 는 회귀와 독립 검증자의
  몫이다 — 원장이 그것을 대신한다고 착각하면 안 된다.

⚠ **아직 못 하는 것** (RC7-04 잔여, Codex 지적):
  · evidence 는 **파일 실재**만 본다 — `file.py::RC6-02` 의 **selector 가 실제로 선택
    가능한지**는 검사하지 않는다.  우리 테스트가 pytest 가 아니라 자체 `main()` 형식이라
    그 문자열은 실행 대상이 아니다.  최종형은 evidence 를 자유문자열이 아니라
    `{command, target_sha, expected_exit, selector}` 로 두고 **CI 가 실제 실행**하는 것.
  · identity 를 코드로 좁혔을 뿐, 구현자가 `verified_by: codex` 라고 **쓰는 것 자체**는
    막지 못한다.  그것은 branch protection / CODEOWNERS 의 몫이다.

  python3 scripts/check_review_findings.py            # 검사 + 열린 항목 출력
  python3 scripts/check_review_findings.py --open     # 열린 항목만 (리뷰 요청서용)
  python3 scripts/check_review_findings.py --selftest
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

# ★ RC7-04 (Codex): `--open` 이 Windows 기본 CP949 에서 세 번째 항목을 찍다 죽었다
#   (UnicodeEncodeError, exit 1).  "열린 항목을 **항상** 화면에 뽑는다" 가 이 도구의
#   존재 이유인데 기본 Windows 실행에서 그 계약이 성립하지 않았다.
#   → stdout/stderr 를 UTF-8 로 재구성하고, 그것이 불가능한 환경에서는 대체문자로 떨어뜨린다
#     (죽는 것보다 읽히는 것이 낫다).
for _stream in ('stdout', 'stderr'):
    _s = getattr(sys, _stream, None)
    if _s is not None and hasattr(_s, 'reconfigure'):
        try:
            _s.reconfigure(encoding='utf-8', errors='replace')
        except Exception:                                   # noqa: BLE001
            pass

LEDGER_DEFAULT = os.path.join('docs', 'reviews', 'findings.json')

#: 실제로 쓰는 ID 형태를 전부 받는다 — RC6-01 · RR3-04 · F-18 · RC6-04b · RC6-Q7 · PD-02.
#: (첫 정의가 너무 좁아 우리 자신의 ID 를 거부했다 — 원장이 규약을 따라야지 반대가 아니다.)
ID_RE = re.compile(r'^[A-Z][A-Z0-9]{0,4}-[A-Za-z0-9]{1,4}$')
STATUSES = ('open', 'claimed_fixed', 'verified', 'wontfix')
SEVERITIES = ('P1', 'P2', 'P3')

#: ★ RC7-04: identity 를 자유문자열로 두면 **case 변형으로 자기검증 금지를 우회**한다
#:   (Codex 실측: owner='claude' · verified_by='Claude' 가 통과했다).  정본 목록으로 좁힌다.
ACTORS = ('claude', 'codex', 'user')

#: git SHA 형식 (짧은 것도 허용하되 hex 여야 한다).
SHA_RE = re.compile(r'^[0-9a-f]{7,40}$')

#: 상태별로 **반드시** 있어야 하는 필드.  없으면 그 상태를 주장할 수 없다.
REQUIRED_BY_STATUS = {
    'claimed_fixed': ('claimed_fixed_sha', 'evidence_tests'),
    'verified': ('claimed_fixed_sha', 'evidence_tests', 'verified_sha', 'verified_by'),
    'wontfix': ('decision_note',),
}


#: ── 철회-문자열 스윕 (2026-08-20) ────────────────────────────────────────────────
#:   왜: 원장은 SR-01 축에서 실질 정본으로 작동하는데 **정본성이 바깥으로 강제되지 않는다**.
#:   실증 — 2026-08-12 에 반증된 `~9.4 %` 가 **08-19 신규 문서에서 재주장**됐고, 독립 리뷰가
#:   그것을 (역시 낡은) 정본에 대조해 "일치"로 **통과**시켰다.  ⇒ 대조 검증조차 정본 신선도에
#:   종속된다.  발견: `docs/reviews/fable_audit_docs_20260820.md` (a)-1.
#:   등록부는 `docs/reviews/claims.json` 의 `quotation_ban` (CLAUDE.md ★★ 인용 금지 목록의
#:   기계 판).  ⚠ 이 파일 목록이 비면 규칙이 조용히 사라지므로 selftest 가 비었는지도 본다.
CLAIMS_DEFAULT = os.path.join('docs', 'reviews', 'claims.json')

#: ⚠⚠ 2026-08-20 (Codex CDX-IJ-04) — 초판 범위는 **md/html/js 뿐**이라 두 곳이 새고 있었다:
#:   · `docs/seminar/seminar_deck.json` — 웹앱 `/api/seminar/slides`(`webapp/app.py`)가 **직접
#:     서빙**하는 활성 산출물인데 `+52%`·`+5.6%` 를 현행 결론으로 말한다.
#:   · `scripts/sr01_gate5_2x2.sh` — 철회된 `f_artifact` 를 여전히 출력한다.
#:   그런데 스윕은 "누수 0" 을 냈다 = false-green.  ⇒ **사용자에게 노출되는 산출물**을 전부 넣는다
#:   (JSON 덱·러너 셸·덱 생성기).  scripts/*.py 는 넣지 않는다 — 그쪽 등장은 대부분 철회를
#:   설명하는 주석이고, 필요하면 줄-근처 표지 규칙으로 개별 통과한다.
#: ⚠⚠ 2026-08-20 (CDXIJ-9 **잔여**) — zip 안은 스윕이 못 봤다.  `docs/seminar/*.pptx` 두 덱이
#:   슬라이드에 `+52.0 %`·`+5.6 %`·`48.2` 를 표지 없이 달고 있는데 스윕은 "누수 0" 을 냈다 =
#:   CDXIJ-4 와 **같은 false-green, 매체만 다르다**.  웹앱 UI 와 덱 생성기를 fail-closed 로
#:   막아도 **체크인된 바이너리 자체**는 열면 그대로 보인다 — 그리고 발표에 쓰이는 것은 그쪽이다.
#:   ⇒ 리더 층(`_ban_read_lines`)을 둬서 Office zip 을 문단당 한 줄로 펼친다.
BAN_SCAN_GLOBS = ('CLAUDE.md', 'docs/**/*.md', 'wiki/**/*.md',
                  'webapp/templates/*.html', 'webapp/static/js/*.js',
                  'scripts/seminar_deck/*.js',
                  'docs/**/*.json', 'webapp/**/*.json', 'scripts/*.sh',
                  'docs/**/*.pptx',
                  # ⚠ 2026-08-23 — 리더(`BAN_ZIP_EXT`)는 처음부터 .docx 를 읽을 수 있었는데
                  #   글롭이 .pptx 만 걸어 **원고·SI 가 스윕 밖에 있었다** (CDXIJ-9 와 같은
                  #   구조의 매체 구멍 — 철회값이 가장 크게 새는 자리가 정작 안 읽혔다).
                  'docs/**/*.docx',
                  # ⚠⚠ 2026-08-25 (A-track 자체점검) — **출력은 읽고 생성기는 안 읽었다.**
                  #   `docs/manuscript_draft/build.js` 가 Table S3 셀에 hold 값
                  #   (CL-33 비)을 그대로 들고 있는데 스윕은 "누수 0" 을 냈다.  원고 .docx
                  #   자신은 머리 배너(claims.json 지목)로 **파일 전체가 면제**라 안 걸리고,
                  #   생성기는 글롭 밖이라 안 읽혔다 ⇒ `build.js` 를 다시 돌리면 철회값이
                  #   표에 **되살아난다** (docx 만 고친 커밋이 내구적이지 않았다).
                  #   덱 생성기(`scripts/seminar_deck/*.js`)를 넣은 것과 같은 이유인데
                  #   원고 쪽만 빠져 있었다 = CDXIJ-4/9 와 같은 매체 구멍.
                  #   ★ 생성기에는 **파일 전체 면제를 주지 않는다** — 출력이 배너로 면제되는
                  #     이상, 표 셀을 실제로 지키는 자리는 여기뿐이다 (설명 문단은 줄-근처
                  #     표지로 개별 통과시킨다).
                  'docs/**/*.js')

#: 이 경로들은 **박제된 원문**이라 철회값이 들어 있는 것이 정상이다 (원장 자신 · 감사 원문 ·
#: 사전등록 계약 · 외부 리뷰 요청서 = 리뷰 시점의 상태를 보존해야 하는 문서).
BAN_ALLOW_ALWAYS = ('docs/reviews/claims.json',
                    # finding 원장도 "무엇을 철회했나" 를 적는 등록부다 (claims.json 과 같은 층).
                    'docs/reviews/findings.json',
                    'docs/reviews/fable_audit_docs_20260820.md',
                    'docs/reviews/fable_audit_code_20260820.md',
                    # ⚠ 외부 리뷰 **원문 박제** — 리뷰어가 인용한 철회값이 그대로 있어야 한다
                    #   (고치면 그 리뷰가 무엇을 보고 판정했는지 알 수 없게 된다).
                    'docs/reviews/codex_crosscheck_IJ_20260820.md')

#: 파일 머리 이 줄 수 안에 배너가 있으면 그 파일 전체를 이력 문서로 본다.
BAN_BANNER_HEAD_LINES = 12
#: 줄-근처 표지로 인정하는 표시 (그 줄만 면제).
BAN_BANNER_MARKS = ('HISTORICAL', '⛔', '인용 금지', '철회', '반증', 'retired', 'RETIRED',
                    '~~', '폐기', '무효')
#: ⚠⚠ 2026-08-20 (Codex 재검증 IJ-04) — **파일 전체 면제는 더 좁게.**
#:   옛 규칙은 위 목록 중 아무 단어나 머리에 있으면 파일을 통째로 면제했다.  Codex 실측:
#:   *무관한* "HISTORICAL" 한 단어 + 현행 "+52.0%" → 0건.  자기승인(self-authorizing)이다.
#:   ⇒ 파일 전체 면제는 **원장을 가리킬 때만** 인정한다 (배너가 등록부/클레임을 지목해야 한다).
#:   줄-근처 면제는 그대로 둔다 (그 줄 하나만 풀어 주므로 남용 여지가 작다).
BAN_BANNER_ANCHORS = ('claims.json', 'CL-', 'CLAUDE.md', '인용 금지')
#: 해당 줄 위아래 이 범위에 표지가 있으면 "철회를 밝히고 인용" 으로 본다.
BAN_NEAR_LINES = 2
#: ⚠⚠ 2026-08-20 (Codex 재검증 IJ-04, 2차) — 줄-근처 면제도 **철회 전용 어휘**만 인정한다.
#:   실측: 근처에 *무관한* "HISTORICAL"/"retired" 한 단어만 있어도 면제됐다.  그 둘은 문서
#:   머리 **배너** 어휘이지 "이 값은 철회됐다" 는 진술이 아니다.  ⇒ 근처 면제에서 뺀다
#:   (⛔ 도 뺀다 — 그 기호 하나로는 무엇이 철회됐는지 말하지 않는다).
BAN_NEAR_MARKS = ('인용 금지', '철회', '반증', '폐기', '무효', '~~', 'CL-')

#: 표기 변형 정규화 — NBSP·얇은 공백·JSON `\u0025`(%)·꼬리 0.
#: Codex 실측 미검출: "+52.00%", NBSP, JSON 이스케이프.
_BAN_WS = {'\u00a0': ' ', '\u2009': ' ', '\u202f': ' ', '\u2007': ' '}


def _ban_norm(text):
    """스윕 비교용 정규화 — 표기 변형이 검사를 우회하지 못하게."""
    import re as _re
    for a, b in _BAN_WS.items():
        text = text.replace(a, b)
    text = text.replace('\\u0025', '%').replace('\\u002B', '+')
    #  숫자의 **꼬리 0** 을 깎는다: +52.00 % → +52 % · +52.0% → +52%
    text = _re.sub(r'(\d)\.0+(?=\D|$)', r'\1', text)
    text = _re.sub(r'(\.\d*?)0+(?=\D|$)', r'\1', text)
    #  숫자와 % 사이 공백 제거 (한쪽 표기로 접는다)
    text = _re.sub(r'\s+%', '%', text)
    return text


def load_bans(claims_path):
    """→ (bans, why).  등록부가 없거나 비면 빈 리스트."""
    if not os.path.exists(claims_path):
        return [], f'등록부 없음: {claims_path}'
    with open(claims_path, encoding='utf-8') as f:
        d = json.load(f)
    return list(d.get('quotation_ban') or []), ''


def _ban_files(repo_root):
    import glob as _glob
    out = []
    for pat in BAN_SCAN_GLOBS:
        out += _glob.glob(os.path.join(repo_root, pat), recursive=True)
    #: 남의 코드는 우리 주장이 아니다 — `docs/**/*.js` 가 없으면 원고 디렉터리의
    #: `node_modules` 145 개가 끌려온다 (검사 시간만 늘고 판정에는 기여 0).
    out = [f for f in out if 'node_modules' not in f.replace(os.sep, '/').split('/')]
    return sorted(set(out))


#: Office zip 으로 취급할 확장자 (내용이 XML 파트라 평문 읽기로는 안 보인다).
BAN_ZIP_EXT = ('.pptx', '.docx')
#: zip 안에서 사용자에게 **보이는** 파트만 읽는다 (테마·마스터는 안 읽는다 — 화면에 안 뜬다).
BAN_ZIP_PARTS = ('ppt/slides/slide', 'ppt/notesSlides/notesSlide', 'word/document')


def _office_paragraphs(xml):
    """Office XML 한 파트 → 문단 문자열 리스트.

    ⚠ **run 은 붙여서 잇는다** (`''.join`).  pptx 는 한 낱말을 여러 `<a:t>` run 으로 쪼개는
      것이 기본 동작이라 (맞춤법 검사·서식 흔적) 공백으로 이으면 `+52.` / `0 %` 같은 분할이
      검사를 그냥 통과한다.  문단 경계(`</a:p>` · `</w:p>`)만 줄로 가른다.
    """
    import re as _re
    import html as _html
    out = []
    for para in _re.split(r'</a:p>|</w:p>', xml):
        runs = _re.findall(r'<(?:a|w):t[^>]*>(.*?)</(?:a|w):t>', para, _re.S)
        if runs:
            out.append(_html.unescape(''.join(runs)))
    return out


def _ban_read_lines(path):
    """검사용 텍스트 줄 → list, 또는 못 읽으면 None.

    평문은 그대로.  Office zip 은 **보이는 파트만** 풀어 `slide3| …` 처럼 출처를 붙인
    문단 줄로 펼친다 (그래야 보고가 몇 번째 슬라이드인지 말한다).  파트 순서를 지키므로
    슬라이드 1 이 배너면 `_has_banner` 의 머리 줄 규칙이 자연히 적용된다.
    """
    if os.path.splitext(path)[1].lower() not in BAN_ZIP_EXT:
        try:
            with open(path, encoding='utf-8', errors='replace') as f:
                return f.read().split('\n')
        except OSError:
            return None
    import zipfile as _zf
    import re as _re
    try:
        z = _zf.ZipFile(path)
    except Exception:                                              # noqa: BLE001
        return None
    names = set(z.namelist())

    def _txt(member, tag, out):
        if member not in names:
            return
        try:
            xml = z.read(member).decode('utf-8', 'replace')
        except Exception:                                          # noqa: BLE001
            return
        for para in _office_paragraphs(xml):
            out.append(f'{tag}| {para}')

    #  ⚠⚠ **정규식으로 읽지 않는다.**  실사고 (2026-08-20): `r:id` 를 문자열로 찾았더니, 접두사가
    #    다르게 직렬화된 슬라이드 하나를 **조용히 빠뜨렸다** — 그리고 하필 그것이 배너였다.
    #    빠진 장은 스윕에도 안 걸리므로 **덱이 검사를 숨길 수 있는 구멍**이다 (fail-open).
    #    ⇒ 네임스페이스 정규명으로 파싱하고, 그래도 안 잡힌 슬라이드 파트는 `orphan:` 으로
    #      **끌어와 검사**한다 (fail-closed).
    _R_NS = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'

    def _rels(part):
        """part 의 rels → {rId: 대상 멤버 경로}."""
        import xml.etree.ElementTree as _ET
        d, base = part.rsplit('/', 1)
        m = f'{d}/_rels/{base}.rels'
        if m not in names:
            return {}
        try:
            root = _ET.fromstring(z.read(m))
        except Exception:                                          # noqa: BLE001
            return {}
        out = {}
        for el in root:
            rid, tgt = el.get('Id'), el.get('Target')
            if rid and tgt and el.get('TargetMode') != 'External':
                out[rid] = _os_norm(d, tgt)
        return out

    lines = []
    #  ⚠⚠ **발표 순서 ≠ zip 멤버 이름 순서.**  실사고 (2026-08-20): 배너 슬라이드를 맨 앞에
    #    끼웠더니 python-pptx 가 `slide21.xml` 로 저장했고, 이름순으로 읽던 옛 판은 그것을
    #    **맨 뒤**로 놓아 배너를 못 봤다.  게다가 보고가 `#slide12` 라고 말하는데 그 번호는
    #    파일 이름이지 **화면에서 12번째** 라는 뜻이 아니었다 — 사람이 열어 보면 다른 장이다.
    #    ⇒ `presentation.xml` 의 `sldIdLst` 로 **진짜 순서**를 푼다.  노트도 그 슬라이드에 붙인다.
    if 'ppt/presentation.xml' in names:
        import xml.etree.ElementTree as _ET
        rel = _rels('ppt/presentation.xml')
        order = []
        try:
            root = _ET.fromstring(z.read('ppt/presentation.xml'))
            for lst_el in root.iter():
                if lst_el.tag.endswith('}sldIdLst'):
                    order = [rel.get(el.get(_R_NS)) for el in lst_el]
                    break
        except Exception:                                          # noqa: BLE001
            pass
        seen_parts = set()
        for pos, member in enumerate([m for m in order if m], 1):
            seen_parts.add(member)
            _txt(member, f'slide{pos}', lines)
            for tgt in _rels(member).values():
                if 'notesSlide' in tgt:
                    _txt(tgt, f'slide{pos}-notes', lines)
        #  순서에서 못 찾은 슬라이드 파트도 반드시 읽는다 — 안 그러면 검사를 숨길 수 있다.
        for n in sorted(x for x in names
                        if x.startswith('ppt/slides/slide') and x.endswith('.xml')
                        and x not in seen_parts):
            _txt(n, f'orphan-{n.rsplit("/", 1)[-1][:-4]}', lines)
    else:
        for n in sorted(n for n in names
                        if n.endswith('.xml') and any(n.startswith(p) for p in BAN_ZIP_PARTS)):
            _txt(n, n.rsplit('/', 1)[-1][:-4], lines)
    return lines


def _os_norm(base_dir, target):
    """rels 의 상대 대상(`../notesSlides/x.xml`)을 zip 멤버 경로로."""
    return os.path.normpath(os.path.join(base_dir, target)).replace(os.sep, '/')


def _has_banner(lines):
    """파일 전체 면제 여부.  **표지 + 원장 지목**을 둘 다 요구한다 (IJ-04)."""
    head = '\n'.join(lines[:BAN_BANNER_HEAD_LINES])
    return (any(m in head for m in BAN_BANNER_MARKS)
            and any(a in head for a in BAN_BANNER_ANCHORS))


def ban_sweep(repo_root, claims_path=None, files=None):
    """→ (문제 목록, 검사한 파일 수, 등록부 크기).

    한 출현이 **허용**되려면 셋 중 하나: ⓐ 파일이 allowed_in / 상시허용 목록 ⓑ 파일 머리
    배너가 있음(이력 문서) ⓒ 그 줄 ±2 줄에 철회 표지가 있음(철회를 밝히고 인용).
    """
    import fnmatch as _fn
    import re as _re_mod
    claims_path = claims_path or os.path.join(repo_root, CLAIMS_DEFAULT)
    bans, err = load_bans(claims_path)
    probs = []
    if err:
        return [err], 0, 0
    files = files if files is not None else _ban_files(repo_root)
    for path in files:
        rel = os.path.relpath(path, repo_root).replace(os.sep, '/')
        if rel in BAN_ALLOW_ALWAYS:
            continue
        lines = _ban_read_lines(path)
        if lines is None:
            continue
        banner = _has_banner(lines)
        for b in bans:
            pat = b.get('pattern')
            if not pat:
                continue
            if any(_fn.fnmatch(rel, g) for g in (b.get('allowed_in') or [])):
                continue
            _npat = _ban_norm(pat)
            for i, ln in enumerate(lines):
                if pat not in ln and _npat not in _ban_norm(ln):
                    continue
                if banner:
                    continue
                lo = max(0, i - BAN_NEAR_LINES)
                near = '\n'.join(lines[lo:i + BAN_NEAR_LINES + 1])
                if any(m in near for m in BAN_NEAR_MARKS):
                    continue
                #  Office zip 은 줄번호가 뜻이 없다 — 리더가 붙인 파트 태그(`slide7`)를 쓴다.
                _m = _re_mod.match(r'([A-Za-z0-9-]+)\| ', ln)
                _at = f'{rel}#{_m.group(1)}' if _m else f'{rel}:{i + 1}'
                probs.append(f'BAN| {_at} — 철회값 "{pat}" 이 표지 없이 살아 있다 '
                             f'({b.get("claim", "?")}: {b.get("why", "")[:70]})')
    return probs, len(files), len(bans)


def load(path):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    return data.get('findings', []) if isinstance(data, dict) else list(data)


def check(findings, repo_root=None):
    """→ 문제 목록 (빈 리스트면 원장이 자기일관적).

    `repo_root` 를 주면 `opened_in` 이 **실재하는 파일**인지도 본다 — 원장이 유령
    문서를 가리키면 추적이 거기서 끊긴다 (실제로 RC6 원문이 붙여넣기라 리포에
    없었다 → 원문을 보존해 해소).
    """
    problems, seen = [], {}
    for i, f in enumerate(findings):
        where = f.get('id') or f'#{i}'
        fid = f.get('id')
        if not fid:
            problems.append(f'{where}: id 없음')
            continue
        if not ID_RE.match(fid):
            problems.append(f'{fid}: id 형식 (예: RC6-01)')
        if fid in seen:
            problems.append(f'{fid}: id 중복 (앞선 항목 #{seen[fid]})')
        seen[fid] = i

        st = f.get('status')
        if st not in STATUSES:
            problems.append(f'{fid}: status={st!r} (허용: {"/".join(STATUSES)})')
            continue
        if f.get('severity') not in SEVERITIES:
            problems.append(f'{fid}: severity={f.get("severity")!r}')
        if not f.get('opened_in'):
            problems.append(f'{fid}: opened_in 없음 (어느 리뷰에서 나왔는지)')
        elif repo_root and not os.path.exists(os.path.join(repo_root, f['opened_in'])):
            problems.append(f'{fid}: opened_in 이 실재하지 않는다 ({f["opened_in"]}) — '
                            '리뷰 원문을 리포에 보존할 것')

        for key in REQUIRED_BY_STATUS.get(st, ()):
            v = f.get(key)
            if not v:
                problems.append(f'{fid}: status={st} 인데 {key} 없음')
        # ★ identity 는 정본 목록으로만 (RC7-04: case 변형 우회 차단)
        for key in ('owner', 'verified_by'):
            v = f.get(key)
            if v is not None and v not in ACTORS:
                problems.append(f'{fid}: {key}={v!r} 는 정본 actor 가 아니다 '
                                f'(허용: {"/".join(ACTORS)}) — 대소문자 변형 우회 차단')
        # ★ 자기검증 금지 — 구현자와 검증자가 같으면 verified 로 닫을 수 없다.
        #   ⚠ 정규화해서 비교한다 (Codex 실측: 'claude' vs 'Claude' 가 통과했다).
        _own = (f.get('owner') or '').strip().casefold()
        _ver = (f.get('verified_by') or '').strip().casefold()
        if st == 'verified' and _ver and _own and _ver == _own:
            problems.append(f'{fid}: verified_by == owner ({f["owner"]}) — '
                            '구현자 자신은 검증자가 될 수 없다')
        # ★ SHA 는 형식 + (repo 가 있으면) **실재하는 커밋**이어야 한다 (RC7-04)
        for key in ('claimed_fixed_sha', 'verified_sha'):
            sha = f.get(key)
            if not sha:
                continue
            if not SHA_RE.match(str(sha)):
                problems.append(f'{fid}: {key}={sha!r} 가 SHA 형식이 아니다')
            elif repo_root and not _commit_exists(repo_root, sha):
                #  ★ 2026-08-20 — 외부 검증자(Codex)는 **자기 worktree** 에서 커밋한다.
                #    그 SHA 는 우리 리포에 없다.  두 극단이 다 틀렸다: 거부하면 독립 검증을
                #    원장에 못 적고, 조용히 통과시키면 **기계로 확인 못 한 것을 확인한 척**한다.
                #    ⇒ `verified_repo` 를 **명시**하면 허용하되, 그 사실이 원장에 남는다
                #    (기계 확인 불가임을 사람이 읽을 수 있게).  없으면 종전대로 거부.
                if key == 'verified_sha' and f.get('verified_repo'):
                    pass
                else:
                    problems.append(f'{fid}: {key}={sha} 가 **HEAD 에서 안 닿는** 커밋이다 '
                                    f'— 리베이스로 SHA 가 바뀌었거나 다른 브랜치의 커밋이다.  '
                                    f'같은 변경의 현재 SHA 로 고칠 것 '
                                    f'(외부 검증이면 `verified_repo` 를 적을 것)')
        # ★ evidence 가 가리키는 **파일이 실재**해야 한다 (RC7-04: 유령 evidence 통과)
        for ev in (f.get('evidence_tests') or []):
            path = str(ev).split('::', 1)[0].split()[0] if ev else ''
            if repo_root and path and not os.path.exists(os.path.join(repo_root, path)):
                problems.append(f'{fid}: evidence 가 실재하지 않는다 ({ev})')
        # supersedes 가 가리키는 id 는 실재해야 한다
        for sup in (f.get('supersedes') or []):
            if sup not in {x.get('id') for x in findings}:
                problems.append(f'{fid}: supersedes 대상 {sup} 이 원장에 없다')
    return problems


def _commit_exists(repo_root, sha):
    """그 SHA 가 **HEAD 에서 닿는** 커밋인가 (RC7-04 + 2026-08-25 강화).

    ★★ 옛 판은 `cat-file -e` 로 **객체 존재**만 봤다.  그러면 리베이스로 버려진 커밋도
      로컬 저장소에 객체가 남아 있어 **통과한다** — 그리고 그 브랜치를 번들로 떼어내면
      그 객체가 없어서 받는 쪽에서 원장 검사가 깨진다.
    ⚠ 실측으로 잡혔다 (2026-08-25): R4CX-01~08 이 `c0ac0ad8` 을 가리키는데 그것은 이
      세션 초반 rebase **이전** SHA 였다.  같은 변경이 이 브랜치엔 `8bcfbeff` 로 들어가
      있었고(patch-id 동일), 로컬에서는 8건 전부 초록이었다.  `make_review_bundle.sh` 가
      번들 안에서 이 검사를 **실제로 돌려서야** 드러났다.
    ⇒ 이제 **조상 여부**를 본다.  "이 브랜치가 그 수정을 담고 있는가" 가 원장이 주장하는
      바이고, 객체가 어딘가 떠다니는 것은 그 주장이 아니다.
    ⚠ git 이 없거나 HEAD 가 없는 환경에서는 **거짓 실패를 만들지 않는다** (검사 생략).
    """
    try:
        if subprocess.run(['git', '-C', repo_root, 'rev-parse', '--verify', 'HEAD'],
                          capture_output=True, timeout=10).returncode != 0:
            return True                                     # HEAD 가 없다 = 판단 불가
        r = subprocess.run(['git', '-C', repo_root, 'merge-base', '--is-ancestor', sha, 'HEAD'],
                           capture_output=True, timeout=10)
        return r.returncode == 0
    except Exception:                                       # noqa: BLE001
        return True            # git 을 못 쓰는 환경에서 **거짓 실패**를 만들지 않는다


def open_items(findings):
    """아직 닫히지 않은 것 (open · claimed_fixed).  다음 리뷰 요청서에 그대로 싣는다."""
    return [f for f in findings if f.get('status') in ('open', 'claimed_fixed')]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument('--ledger', default=os.path.join(here, LEDGER_DEFAULT))
    ap.add_argument('--open', action='store_true', help='열린 항목만 출력')
    ap.add_argument('--claims', default=os.path.join(here, CLAIMS_DEFAULT))
    ap.add_argument('--ban-sweep', action='store_true',
                    help='철회-문자열 스윕만 실행 (claims.json quotation_ban 등록부)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    if a.ban_sweep:
        bprobs, nfile, nban = ban_sweep(here, a.claims)
        print(f'── 철회-문자열 스윕 — 등록 {nban} 개 × 파일 {nfile} 개 ──')
        for p in bprobs:
            print('   ' + p)
        if not nban:
            print('   ⚠ 등록부가 비었다 — 이 규칙은 지금 아무것도 강제하지 않는다')
            return 1
        print(('\n★★ 철회값 누수 %d 건 ★★' % len(bprobs)) if bprobs
              else '\n철회값 누수 없음 ✓')
        return 1 if bprobs else 0
    if not os.path.exists(a.ledger):
        sys.exit(f'원장 없음: {a.ledger}')
    findings = load(a.ledger)
    probs = check(findings, repo_root=here)

    if not a.open:
        by = {}
        for f in findings:
            by.setdefault(f.get('status', '?'), []).append(f)
        print(f'══ finding 원장 — {len(findings)} 건 ══')
        for st in STATUSES:
            if by.get(st):
                print(f'   {st:<14} {len(by[st])}')
        print()

    ops = open_items(findings)
    print(f'── 열린 항목 {len(ops)} 건 (open · claimed_fixed) ──')
    for f in ops:
        ev = ', '.join(f.get('evidence_tests') or []) or '—'
        print(f"  [{f.get('severity')}] {f['id']:<8} {f.get('status'):<13} "
              f"{(f.get('title') or '')[:52]}")
        print(f"        회귀: {ev}   opened_in: {f.get('opened_in')}")

    if probs:
        print(f'\n★★ 원장 불일치 {len(probs)} 건 ★★')
        for p in probs:
            print('   ' + p)
        return 1
    print('\n원장 자기일관 ✓  (⚠ "정말 고쳐졌는가" 는 회귀와 독립 검증자의 몫이다)')
    return 0


def _selftest():
    n = [0, 0]

    def ok(name, cond):
        n[1] += 1
        n[0] += bool(cond)
        print(f'  {"PASS" if cond else "FAIL"}  {name}')

    base = {'id': 'RC6-01', 'severity': 'P1', 'status': 'open',
            'owner': 'claude', 'opened_in': 'docs/reviews/x.md'}
    ok('1) 최소 항목은 통과', check([base]) == [])
    ok('2) id 중복을 잡는다', any('중복' in p for p in check([base, dict(base)])))
    ok('3) id 형식을 잡는다', any('형식' in p for p in check([dict(base, id='bad')])))
    ok('3b) ★ 우리가 실제로 쓰는 ID 형태를 전부 받는다',
       all(ID_RE.match(x) for x in ('RC6-01', 'RR3-04', 'F-18', 'RC6-04b', 'RC6-Q7', 'PD-02')))
    ok('4) 모르는 status 를 잡는다', any('status=' in p for p in check([dict(base, status='done')])))
    ok('5) ★ claimed_fixed 는 SHA + 회귀를 둘 다 요구한다',
       len([p for p in check([dict(base, status='claimed_fixed')])]) == 2)
    # ★ SHA 형식 검사가 생긴 뒤로는 fixture 도 진짜 형태여야 한다 (fixture-drift 교정).
    #   repo_root 를 안 주므로 **실재 검사는 생략**되고 형식만 본다.
    ok('6) 둘 다 있으면 통과',
       check([dict(base, status='claimed_fixed', claimed_fixed_sha='0123abc',
                   evidence_tests=['t1'])]) == [])
    ok('7) ★ verified 는 검증자까지 요구한다',
       any('verified_by' in p for p in check([dict(base, status='verified',
                                                   claimed_fixed_sha='0123abc',
                                                   evidence_tests=['t'],
                                                   verified_sha='abc0123')])))
    ok('8) ★ 자기검증(verified_by == owner)을 거부한다',
       any('검증자가 될 수 없다' in p for p in check([
           dict(base, status='verified', claimed_fixed_sha='0123abc', evidence_tests=['t'],
                verified_sha='abc0123', verified_by='claude')])))
    ok('9) 다른 검증자면 통과',
       check([dict(base, status='verified', claimed_fixed_sha='0123abc',
                   evidence_tests=['t'], verified_sha='abc0123', verified_by='codex')]) == [])
    ok('10) wontfix 는 사유를 요구한다',
       any('decision_note' in p for p in check([dict(base, status='wontfix')])))
    ok('11) opened_in 이 없으면 잡는다',
       any('opened_in' in p for p in check([{k: v for k, v in base.items()
                                             if k != 'opened_in'}])))
    ok('12) supersedes 대상이 없으면 잡는다',
       any('supersedes' in p for p in check([dict(base, supersedes=['RC5-99'])])))
    ok('13) 열린 항목만 골라낸다',
       [f['id'] for f in open_items([
           base, dict(base, id='RC6-02', status='verified'),
           dict(base, id='RC6-03', status='claimed_fixed')])] == ['RC6-01', 'RC6-03'])

    # ══ RC7-04 (Codex 6→7회차): 검사기 자신이 통과시키던 손상 원장 ══
    _corrupt = {'id': 'RC6-01', 'severity': 'P1', 'status': 'verified', 'owner': 'claude',
                'opened_in': 'docs/reviews/x.md', 'verified_by': 'Claude',
                'claimed_fixed_sha': 'not-a-sha', 'verified_sha': 'also-not-a-sha',
                'evidence_tests': ['missing.py::ghost']}
    _probs = check([_corrupt])
    ok('16) ★ case 변형 자기검증 우회를 잡는다 (claude vs Claude)',
       any('정본 actor' in p for p in _probs) and any('검증자가 될 수 없다' in p for p in _probs))
    ok('17) ★ SHA 형식 위반을 잡는다 (not-a-sha)',
       len([p for p in _probs if 'SHA 형식' in p]) == 2)
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ok('18) ★ 유령 evidence 를 잡는다',
       any('evidence 가 실재하지' in p for p in check([_corrupt], repo_root=here)))
    ok('19) ★ 형식은 맞지만 리포에 없는 커밋을 잡는다',
       any('안 닿는' in p for p in check(
           [dict(_corrupt, verified_by='codex', claimed_fixed_sha='deadbeef',
                 verified_sha='cafebabe',
                 evidence_tests=['webapp/test_pipeline_provenance.py'])], repo_root=here)))
    #  ★★ 2026-08-25 — **존재하지만 HEAD 에서 안 닿는** 커밋도 잡아야 한다.  이것이
    #    리베이스 잔재의 모양이고, 옛 판(`cat-file -e`)은 여기서 **통과**했다.
    #    실측: R4CX-01~08 이 rebase 이전 SHA 를 가리키는데 로컬 8건 전부 초록이었고,
    #    `make_review_bundle.sh` 가 번들 안에서 이 검사를 실제로 돌려서야 드러났다.
    #  ⇒ 매달린(dangling) 커밋을 하나 만들어 그 상태를 재현한다 — 객체는 실재하지만
    #    어느 ref 에서도 안 닿는다.
    _dang = None
    try:
        _t = subprocess.run(['git', '-C', here, 'rev-parse', 'HEAD^{tree}'],
                            capture_output=True, text=True, timeout=10)
        if _t.returncode == 0:
            _c = subprocess.run(['git', '-C', here, 'commit-tree', _t.stdout.strip(), '-m',
                                 'dangling probe (selftest)'],
                                capture_output=True, text=True, timeout=10)
            if _c.returncode == 0:
                #  ⚠ 간헐 실패 (2026-08-29 실측): 단순히 `[:8]` 로 자르면 그 접두사가
                #    **모호**할 수 있고 (다른 객체와 충돌) 그때 검사가 거짓 실패한다.
                #    `--short=8` 은 모호하면 git 이 자동으로 길이를 늘린다.
                #    ⇒ 검사기가 가끔 빨간불을 내면 언젠가 이유 없이 GPU 런을 막는다.
                _sr = subprocess.run(['git', '-C', here, 'rev-parse', '--short=8',
                                      _c.stdout.strip()], capture_output=True, text=True,
                                     timeout=10)
                _dang = (_sr.stdout.strip() if _sr.returncode == 0
                         else _c.stdout.strip()[:8])
    except Exception:                                       # noqa: BLE001
        _dang = None
    if _dang:
        _pd = check([dict(_corrupt, verified_by='codex', claimed_fixed_sha=_dang,
                          verified_sha=_dang,
                          evidence_tests=['webapp/test_pipeline_provenance.py'])],
                    repo_root=here)
        ok(f'19b) ★★ **존재하지만 HEAD 에서 안 닿는** 커밋을 잡는다 (리베이스 잔재, {_dang})',
           any('안 닿는' in p for p in _pd))
    else:
        ok('19b) (git 을 못 써 건너뜀 — 거짓 실패를 만들지 않는다)', True)
    ok('20) 정본 actor 세 개는 통과', set(ACTORS) == {'claude', 'codex', 'user'})

    led = os.path.join(here, LEDGER_DEFAULT)
    if os.path.exists(led):
        ok('14) ★ 실제 원장이 자기일관적이다', check(load(led), repo_root=here) == [])
        ok('15) ★ opened_in 이 유령 문서면 잡는다 (추적이 거기서 끊긴다)',
           any('실재하지' in p for p in check(
               [dict(base, opened_in='docs/reviews/nope.md')], repo_root=here)))
    else:
        print('  SKIP 14) 원장 파일 없음')

    # ── 철회-문자열 스윕 (2026-08-20) ────────────────────────────────────────────
    #   ★ 음성 대조가 핵심이다 — 규칙 D 의 교훈("한 번도 발동한 적이 없는 검사")대로,
    #     "지금 리포가 깨끗하다" 만으로는 검사기가 **정말 잡는지** 증명되지 않는다.
    import tempfile as _tf
    _claims = os.path.join(here, CLAIMS_DEFAULT)
    _bans, _err = load_bans(_claims)
    ok('16) 등록부가 비어 있지 않다 (비면 이 규칙이 조용히 사라진다)',
       not _err and len(_bans) >= 5)
    if _bans:
        _pat = _bans[0]['pattern']
        with _tf.TemporaryDirectory() as _d:
            _bad = os.path.join(_d, 'bad.md')
            with open(_bad, 'w', encoding='utf-8') as _f:
                _f.write(f'# 제목\n\n본문에서 {_pat} 를 현행 사실로 쓴다\n')
            _p1, _, _ = ban_sweep(_d, _claims, files=[_bad])
            #  ⚠ 2026-08-20: 표기 정규화 후에는 한 줄이 여러 등록 패턴에 걸릴 수 있다
            #    (`+52.0 %` · `+52 %` · `+52%` 가 전부 `+52%` 로 접힌다).  개수가 아니라
            #    **그 패턴이 지목됐는지**를 본다.
            ok('17) ★ 음성 대조 — 표지 없는 철회값을 **정말** 잡는다',
               any(_pat in x for x in _p1))

            _good = os.path.join(_d, 'good.md')
            with open(_good, 'w', encoding='utf-8') as _f:
                #  ⚠ 2026-08-20: 배너는 **원장을 지목**해야 파일 전체를 면제한다 (IJ-04).
                _f.write(f'# 제목\n\n> ⛔ HISTORICAL — 아래는 이력이다\n'
                         f'> 정본: docs/reviews/claims.json (CL-24)\n\n{_pat} 는 옛 값\n')
            _p2, _, _ = ban_sweep(_d, _claims, files=[_good])
            ok('18) 파일 머리 배너가 있으면 통과 (이력 문서를 죽이지 않는다)', _p2 == [])

            _near = os.path.join(_d, 'near.md')
            with open(_near, 'w', encoding='utf-8') as _f:
                _f.write(f'# 제목\n\n옛 헤드라인 {_pat} 는 **철회**됐다 (CL-24)\n')
            _p3, _, _ = ban_sweep(_d, _claims, files=[_near])
            ok('19) 같은 줄에 철회 표지가 있으면 통과 (철회를 밝히고 인용)', _p3 == [])
            #  ── 2026-08-20 (Codex 재검증 IJ-04) — **우회 두 가지를 상주 음성 대조로** ──
            _self = os.path.join(_d, 'selfauth.md')
            with open(_self, 'w', encoding='utf-8') as _f:
                #  머리에 *무관한* HISTORICAL 한 단어만 — 원장을 지목하지 않는다
                _f.write(f'# 제목\n\nHISTORICAL context of the field\n'
                         f'\nretired equipment note\n\n{_pat} 는 현행 결론\n')
            _p4, _, _ = ban_sweep(_d, _claims, files=[_self])
            ok('20a) ★ 자기승인 배너(원장 미지목)로는 파일 면제가 안 된다',
               any(_pat in x for x in _p4))

            _var = os.path.join(_d, 'variant.md')
            with open(_var, 'w', encoding='utf-8') as _f:
                _f.write('# 제목\n\n결과는 +52.00% 이고 이온은 +5.60% 다\n')
            _p5, _, _ = ban_sweep(_d, _claims, files=[_var])
            ok('20b) ★ 표기 변형(+52.00% · +5.60%)도 잡는다', _p5 != [])

            #  ── 2026-08-20 (CDXIJ-9 잔여) — **zip 안**을 정말 보는가.  세 가지 음성 대조:
            #     ⓐ 표지 없는 슬라이드를 잡고 **몇 번 슬라이드인지 말한다**
            #     ⓑ 슬라이드 1 배너면 면제 (이력 덱을 죽이지 않는다)
            #     ⓒ ★ run 이 쪼개져도 잡는다 — pptx 가 한 낱말을 여러 `<a:t>` 로 가르는 것이
            #        기본 동작이라, 이 대조가 없으면 스윕이 조용히 통과한다.
            import zipfile as _zft

            def _mkppt(dst, slides):
                with _zft.ZipFile(dst, 'w') as _z:
                    for _i, _runs in enumerate(slides, 1):
                        _t = ''.join(f'<a:t>{r}</a:t>' for r in _runs)
                        _z.writestr(f'ppt/slides/slide{_i}.xml',
                                    f'<p:sld xmlns:a="x"><a:p>{_t}</a:p></p:sld>')

            _d1 = os.path.join(_d, 'deck_bad.pptx')
            _mkppt(_d1, [['제목 슬라이드'], [f'헤드라인 {_pat} 달성']])
            _p6, _, _ = ban_sweep(_d, _claims, files=[_d1])
            ok('22a) ★ 음성 대조 — pptx 슬라이드 안의 철회값을 잡고 슬라이드를 지목한다',
               any(_pat in x and 'slide2' in x for x in _p6))

            _d2 = os.path.join(_d, 'deck_ok.pptx')
            _mkppt(_d2, [['⛔ HISTORICAL — 이 덱은 이력이다.  정본: docs/reviews/claims.json (CL-24)'],
                         [f'헤드라인 {_pat} 달성']])
            _p7, _, _ = ban_sweep(_d, _claims, files=[_d2])
            ok('22b) 슬라이드 1 이 원장을 지목하는 배너면 덱 전체 면제', _p7 == [])

            #  `+52.0 %` 를 pptx 가 실제로 쪼개는 방식대로 run 3개로 가른다
            _d3 = os.path.join(_d, 'deck_split.pptx')
            _sp = [_pat[:len(_pat) // 2], _pat[len(_pat) // 2:]]
            _mkppt(_d3, [['제목'], ['헤드라인 '] + _sp + [' 달성']])
            _p8, _, _ = ban_sweep(_d, _claims, files=[_d3])
            ok('22c) ★ run 이 쪼개져 있어도 잡는다 (문단 안에서 run 을 붙여 읽는다)',
               any(_pat in x for x in _p8))

            #  ⓓ ★ **순서에 없는 슬라이드도 읽는다.**  실사고: 배너를 끼웠더니 접두사가 다르게
            #     직렬화돼 순서 해석에서 빠졌고, 빠진 장은 스윕에도 안 걸렸다 = 덱이 검사를
            #     숨길 수 있었다.  여기서는 `sldIdLst` 를 아예 비워 그 상황을 만든다.
            _d4 = os.path.join(_d, 'deck_orphan.pptx')
            with _zft.ZipFile(_d4, 'w') as _z:
                _z.writestr('ppt/presentation.xml',
                            '<p:presentation xmlns:p="y"><p:sldIdLst/></p:presentation>')
                _z.writestr('ppt/slides/slide1.xml',
                            f'<p:sld xmlns:a="x"><a:p><a:t>헤드라인 {_pat}</a:t></a:p></p:sld>')
            _p9, _, _ = ban_sweep(_d, _claims, files=[_d4])
            ok('22d) ★ 발표 순서에 없는(고아) 슬라이드도 검사한다 — 덱이 검사를 숨길 수 없다',
               any(_pat in x and 'orphan' in x for x in _p9))

            #  ⓔ ★ **원고·SI 는 .docx 다.**  리더(`BAN_ZIP_EXT`)는 처음부터 word/document 를
            #     읽을 수 있었는데 **글롭이 .pptx 만 걸어** 원고가 스윕 밖에 있었다 (2026-08-23).
            #     그래서 여기서는 `files=` 를 주지 않는다 — 글롭 발견 경로 자체를 검사한다.
            _dr = os.path.join(_d, 'reporoot')
            os.makedirs(os.path.join(_dr, 'docs', 'reviews'), exist_ok=True)
            import shutil as _sh
            _sh.copy(_claims, os.path.join(_dr, 'docs', 'reviews', 'claims.json'))
            _d5 = os.path.join(_dr, 'docs', 'manuscript.docx')
            with _zft.ZipFile(_d5, 'w') as _z:
                _z.writestr('word/document.xml',
                            '<w:document xmlns:w="z"><w:body><w:p>'
                            f'<w:r><w:t>headline {_pat} achieved</w:t></w:r>'
                            '</w:p></w:body></w:document>')
            _p10, _nf10, _ = ban_sweep(_dr)
            ok('22e) ★ 글롭이 .docx 를 발견한다 — 원고·SI 가 스윕 안에 있다',
               _nf10 >= 1 and any(_pat in x and 'manuscript.docx' in x for x in _p10))

            #  ⓕ ★★ **출력만 읽고 생성기를 안 읽으면 고침이 내구적이지 않다** (2026-08-25).
            #     원고 .docx 는 머리 배너(원장 지목)로 **파일 전체가 면제**라, 표 셀을 실제로
            #     지키는 자리는 생성기뿐이다.  그런데 `docs/**/*.js` 가 글롭에 없어
            #     `build.js` 가 Table S3 셀에 hold 값을 들고도 스윕은 "누수 0" 을 냈다
            #     = 덱을 다시 돌리면 철회값이 표에 **되살아난다**.
            _d6 = os.path.join(_dr, 'docs', 'draft')
            os.makedirs(os.path.join(_d6, 'node_modules', 'dep'), exist_ok=True)
            with open(os.path.join(_d6, 'build.js'), 'w', encoding='utf-8') as _f6:
                _f6.write("rows.push(['ratio','%s']);\n" % _pat)
            #     남의 코드가 같은 문자열을 가져도 우리 주장이 아니다.
            with open(os.path.join(_d6, 'node_modules', 'dep', 'x.js'), 'w',
                      encoding='utf-8') as _f7:
                _f7.write("var v = '%s';\n" % _pat)
            _p11, _, _ = ban_sweep(_dr)
            ok('22f) ★★ 글롭이 **생성기**(docs/**/*.js) 도 발견한다 — docx 만 고치면 내구적이 아니다',
               any('build.js' in x and _pat in x for x in _p11))
            ok('22g) 그러나 node_modules 는 안 읽는다 (남의 코드는 우리 주장이 아니다)',
               not any('node_modules' in x for x in _p11))

    ok('21) ★ 리포 전체가 지금 깨끗하다 (누수 0)',
       ban_sweep(here, _claims)[0] == [])

    print(f'\ncheck_review_findings selftest: {n[0]}/{n[1]} PASS')
    return 0 if n[0] == n[1] else 1


if __name__ == '__main__':
    raise SystemExit(main())
