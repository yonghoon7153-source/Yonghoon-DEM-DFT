#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""원장(`docs/reviews/claims.json` · `findings.json`)을 **웹앱이 읽는** 창구.

왜 이것이 생겼나 — 2026-09-09 전수 감사의 실측:

  · 웹앱 8 영역 전부에서 **기계는 최신인데 라벨이 3~15 개월 뒤처져** 있었다.
  · 철회 배너 **두 개가 같은 문장에서 다른 금지 세트**를 현행 결론으로 적고 있었다
    (`app.py:4035` · `seminar_deck.json`).
  · 원인은 하나다 — 상태를 말하는 문장이 전부 **템플릿·라우트에 손으로 적힌 산문**이고,
    원장이 바뀌어도 **아무것도 그것을 따라가게 만들지 않는다.**
    실제로 `webapp/` 어디에서도 `claims.json` 을 **읽은 적이 없었다** (문자열로 언급만).

⇒ 처방: 산문을 **원장에서 렌더**한다.  철회가 등재되면 다음 요청에 화면이 바뀐다.

설계 원칙 세 가지
  ① **원장이 없으면 조용히 비운다** — 배포 호스트에 `docs/` 가 없을 수 있다.  없는데
     있는 척하는 것이 최악이므로 `available() == False` 를 명시적으로 노출한다.
  ② **파싱을 새로 안 짠다** — 금지 등록부는 `scripts/check_review_findings.py` 의
     `load_bans()` 를 그대로 쓴다 (규율 ① 사다리: "이 리포에 이미 있나").
  ③ **읽기 전용** — 이 모듈은 원장을 쓰지 않는다.  등재는 사람과 CLI 의 몫이다.
"""
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(_HERE, '..'))
CLAIMS_PATH = os.path.join(REPO_ROOT, 'docs', 'reviews', 'claims.json')
FINDINGS_PATH = os.path.join(REPO_ROOT, 'docs', 'reviews', 'findings.json')

#: 화면에 띄우는 상태 어휘 → (한 낱말 라벨, CSS 클래스).  원장 `_status_vocab` 과 같은 축.
STATUS_UI = {
    'live': ('유효', 'ok'),
    'hold': ('보류', 'warn'),
    'rejected': ('기각', 'bad'),
    'retired': ('철회', 'bad'),
}

_cache = {'stamp': None, 'data': None}


def _stamp():
    """두 원장 파일의 (mtime, size) — 바뀌면 캐시를 버린다."""
    out = []
    for p in (CLAIMS_PATH, FINDINGS_PATH):
        try:
            st = os.stat(p)
            out.append((p, st.st_mtime_ns, st.st_size))
        except OSError:
            out.append((p, None, None))
    return tuple(out)


def _load():
    stamp = _stamp()
    if _cache['stamp'] == stamp and _cache['data'] is not None:
        return _cache['data']
    claims, bans, findings, err = [], [], [], None
    try:
        with open(CLAIMS_PATH, encoding='utf-8') as f:
            doc = json.load(f)
        claims = doc.get('claims') or []
        bans = doc.get('quotation_ban') or []
    except Exception as e:                                     # noqa: BLE001
        err = f'{type(e).__name__}: {e}'
    f_err = None
    try:
        with open(FINDINGS_PATH, encoding='utf-8') as f:
            findings = (json.load(f) or {}).get('findings') or []
    except Exception as e:                                     # noqa: BLE001
        #  ⛔ **정정 2026-09-09 (Codex Q3-3)** — 옛 판은 이 예외를 삼켜
        #    `available=True · open_findings=[]` 를 돌려줬다 = **읽기 실패를 "열린 결함
        #    없음" 처럼** 보이게 했다.  없는 것과 못 읽은 것은 다르다.
        f_err = f'{type(e).__name__}: {e}'
    data = {'claims': claims, 'bans': bans, 'findings': findings,
            'error': err, 'findings_error': f_err}
    _cache['stamp'], _cache['data'] = stamp, data
    return data


def available():
    """원장을 실제로 읽었는가.  False 면 화면은 **상태를 주장하지 않는다.**"""
    return bool(_load()['claims'])


def error():
    return _load()['error']


def findings_error():
    """결함 원장을 **못 읽었는가** — `[]` 와 구별해야 한다 (Codex Q3-3)."""
    return _load().get('findings_error')


#: 금지값이 화면에 닿기 전에 지우는 자리.  ⚠⚠ 이것이 **없으면 안 되는 이유**:
#:   원장 본문과 등록부의 `why` 는 *"무엇이 왜 철회됐나"* 를 설명하느라 **그 값을 인용한다.**
#:   그래서 원장을 그대로 렌더하면 **금지값을 보여 주는 페이지가 곧 누수**가 된다.
#:   이것이 가설이 아니라 실측이다 — `webapp/test_ledger_view.py` 15) 가 초판 구현에서
#:   `/ledger` 11 건 · `/` 2 건을 잡았고, 감사가 `app.py:4035` 에서 찾은 것과 **같은 양식**이다
#:   (철회를 알리는 문장이 같은 자리에서 금지값을 현행처럼 적는다).
_REDACT_CACHE = {'stamp': None, 'rx': None}


def _pattern_regex(pat):
    """등록부 패턴 하나 → `_ban_norm` 이 접는 표기 변형까지 잡는 정규식 조각.

    스윕과 **같은 관용**을 가져야 한다 — 스윕이 잡는 것을 화면이 흘리면 안 되고,
    반대로 화면이 과하게 지우면 설명이 사라진다.
    """
    out, i = [], 0
    while i < len(pat):
        ch = pat[i]
        if ch == '%':
            out.append('%')
        elif ch == ' ':
            #  숫자와 % 사이 공백은 스윕이 접는다 (NBSP·얇은공백 포함, 없어도 매치)
            out.append('[\\s\\u00a0\\u2009\\u202f\\u2007]*')
        elif ch.isdigit():
            j = i
            while j < len(pat) and (pat[j].isdigit() or pat[j] == '.'):
                j += 1
            num = pat[i:j]
            out.append(re.escape(num))
            #  꼬리 0 관용 — 같은 값이 소수점 0 을 달고도 쓰이므로 스윕과 같은 폭으로 접는다.
            #  (⚠ 여기에 실례를 적지 않는다: 이 파일도 스윕 대상이라 예시가 곧 누수다.)
            out.append('(?:\\.0+)?' if '.' not in num else '0*')
            i = j
            continue
        else:
            out.append(re.escape(ch))
        i += 1
    return ''.join(out)


def _redactor():
    stamp = _stamp()
    if _REDACT_CACHE['stamp'] == stamp and _REDACT_CACHE['rx'] is not None:
        return _REDACT_CACHE['rx']
    rules = []
    for b in _load()['bans']:
        pat = b.get('pattern')
        if not pat:
            continue
        try:
            rules.append((re.compile(_pattern_regex(pat)), b.get('claim') or '?'))
        except re.error:
            rules.append((re.compile(re.escape(pat)), b.get('claim') or '?'))
    #  긴 패턴을 먼저 지운다 — 짧은 패턴이 긴 패턴의 앞부분을 먼저 먹으면 잔여가 남는다.
    rules.sort(key=lambda r: -len(r[0].pattern))
    _REDACT_CACHE['stamp'], _REDACT_CACHE['rx'] = stamp, rules
    return rules


def redact(text):
    """화면으로 나가는 모든 원장 산문은 여기를 통과한다.

    금지값을 **지우는 것이 아니라 자리를 남긴다** — 독자가 *"여기 값이 있었고 지금은
    인용할 수 없다"* 를 알아야 하기 때문이다.  값이 필요하면 원장 파일 안에서만 본다.
    """
    if not text:
        return text
    s = str(text)
    for rx, cl in _redactor():
        s = rx.sub(f'⟨인용금지·{cl}⟩', s)
    return s


def _num(cl_id):
    """`CL-89` → 89.  정렬용 (문자열 정렬은 CL-9 를 CL-89 뒤에 둔다)."""
    try:
        return int(str(cl_id).split('-')[-1])
    except (ValueError, TypeError):
        return -1


#: 화면으로 나가는 레코드에서 **산문 필드만** 남긴다.  측정치(`measured`)·판정(`verdict`)은
#: 통째로 뺀다 — 거기에 금지값이 가장 많고, 그것을 보려면 원장 파일을 여는 것이 맞다.
_VIEW_FIELDS = ('id', 'date', 'status', 'kind')


def _view(c):
    out = {k: c.get(k) for k in _VIEW_FIELDS}
    out['claim'] = redact(c.get('claim'))
    return out


def claims(status=None, limit=None, raw=False):
    """원장 클레임 — **최신이 먼저** (날짜 내림차순, 같은 날은 id 번호 내림차순).

    기본은 **화면용 view** 다 (금지값 지움 · 산문 필드만).  `raw=True` 는 내부 계산용.
    """
    rows = _load()['claims']
    if status:
        want = {status} if isinstance(status, str) else set(status)
        rows = [c for c in rows if c.get('status') in want]
    rows = sorted(rows, key=lambda c: (c.get('date') or '', _num(c.get('id'))),
                  reverse=True)
    rows = rows[:limit] if limit else rows
    return rows if raw else [_view(c) for c in rows]


def by_id(cl_id):
    for c in _load()['claims']:
        if c.get('id') == cl_id:
            return c
    return None


def counts():
    out = {}
    for c in _load()['claims']:
        s = c.get('status') or 'unknown'
        out[s] = out.get(s, 0) + 1
    out['total'] = len(_load()['claims'])
    return out


def newest_date():
    """가장 최근 **클레임** 등재 날짜."""
    ds = [c.get('date') for c in _load()['claims'] if c.get('date')]
    return max(ds) if ds else None


#: `opened_in` 문서명에 박힌 8자리에서 날짜를 캔다 (예 `…_20260913.md`).
_FDATE = re.compile(r'(20\d{2})(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])')


def finding_date(f):
    """finding 의 등재 날짜.

    ⚠ `findings.json` 레코드에는 **`date` 필드가 없다** — `opened_in` 문서명의 8자리에서
    캔다.  못 캐면 `None` 이고, 그때는 **날짜 비교에서 뺀다** (모르는 것을 오늘로 치지 않는다).
    """
    m = _FDATE.search(str(f.get('opened_in') or ''))
    return f'{m.group(1)}-{m.group(2)}-{m.group(3)}' if m else None


def newest_finding_date():
    """아직 안 닫힌 결함 중 가장 최근 등재 날짜."""
    ds = [finding_date(f) for f in _load()['findings']
          if f.get('status') in ('open', 'claimed_fixed')]
    ds = [d for d in ds if d]
    return max(ds) if ds else None


def newest_ledger_date():
    """★★ 신선도 기준선 — **클레임과 결함 둘 다** 본다.

    ⛔ **정정 2026-09-14 (webapp 감사 D-2)** — 옛 판은 `newest_date()`(클레임 전용)만 썼다.
    그래서 `/single` 이 `updated=2026-09-09` 로 **초록 '검토됐다'** 를 띄우는 동안, 정작 그
    화면을 구동하는 코드에 대해 **2026-09-13 에 열린 결함이 6건**(`L3-01`·`L3-02`·`L4-01`·
    `L4-02` = P1) 이었다.  원장이 claims 축으로만 화면에 배선돼 있었던 것이다.
    ⇒ 규율 ⑤ 의 false-green 이 **매체가 아니라 축**에서 재현됐다.  결함도 원장이다.
    """
    ds = [d for d in (newest_date(), newest_finding_date()) if d]
    return max(ds) if ds else None


def finding_by_id(fid):
    for f in _load()['findings']:
        if f.get('id') == fid:
            return f
    return None


def finding_chip(fid):
    """한 결함의 화면용 요약 — 없는 id 면 **모른다고 말한다**."""
    f = finding_by_id(fid)
    if not f:
        return {'id': fid, 'known': False, 'label': '미등재', 'cls': 'na',
                'date': None, 'title': ''}
    st = f.get('status')
    label, cls = {'open': ('열림', 'hold'),
                  'claimed_fixed': ('고쳤다고 주장', 'na'),
                  'verified': ('검증됨', 'live'),
                  'wontfix': ('안 고침', 'na')}.get(st, (st or '?', 'na'))
    sev = f.get('severity') or ''
    return {'id': fid, 'known': True, 'label': f'{sev} {label}'.strip(), 'cls': cls,
            'status': st, 'severity': sev, 'date': finding_date(f),
            'title': redact(f.get('title') or '')[:190]}


def banned():
    """인용 금지 등록부.  ⚠ 이 목록 자체를 화면에 **값으로** 뿌리지 않는다 —
    패턴 문자열이 곧 금지값이라, 그것을 렌더하면 이 페이지가 누수가 된다.
    `banned_summary()` 로 **개수와 클레임 id 만** 보여 준다."""
    return _load()['bans']


def banned_summary():
    """→ [{'claim': 'CL-24', 'n': 6, 'why': '…'}] — 값 없이 '무엇이 금지인가' 만."""
    by = {}
    for b in _load()['bans']:
        cl = b.get('claim') or '?'
        row = by.setdefault(cl, {'claim': cl, 'n': 0, 'why': ''})
        row['n'] += 1
        if not row['why']:
            #  ⚠ `why` 는 *왜 철회됐나* 를 설명하느라 **그 값을 인용한다** — 반드시 지운다.
            row['why'] = redact(b.get('why') or '')[:190]
    return sorted(by.values(), key=lambda r: -_num(r['claim']))


def open_findings(limit=None):
    """열린 결함 — P0/P1 이 먼저, 그 안에서 id 역순."""
    rank = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3}
    rows = [f for f in _load()['findings']
            if f.get('status') in ('open', 'claimed_fixed')]
    rows.sort(key=lambda f: (rank.get(f.get('severity'), 9),
                             f.get('status') != 'open',
                             -_num(f.get('id'))))
    rows = rows[:limit] if limit else rows
    return [{'id': f.get('id'), 'severity': f.get('severity'),
             'status': f.get('status'), 'title': redact(f.get('title'))}
            for f in rows]


def chip(cl_id):
    """한 클레임의 화면용 요약 — 없는 id 면 **모른다고 말한다** (지어내지 않는다)."""
    c = by_id(cl_id)
    if not c:
        return {'id': cl_id, 'known': False, 'label': '미등재',
                'cls': 'na', 'date': None, 'title': ''}
    label, cls = STATUS_UI.get(c.get('status'), (c.get('status') or '?', 'na'))
    #  claim 본문의 첫 문장만 — 원장 서술은 길고 화면은 좁다.
    text = redact((c.get('claim') or '')).replace('**', '').replace('*', '')
    for cut in ('.  ', '. ', '\n'):
        if cut in text:
            text = text.split(cut)[0]
            break
    return {'id': cl_id, 'known': True, 'label': label, 'cls': cls,
            'date': c.get('date'), 'status': c.get('status'),
            'title': text[:190]}


def freshness(page_updated, ledger_ids=(), finding_ids=()):
    """페이지가 원장보다 뒤처졌는가 — **감사를 기다리지 않고 스스로 말하게 한다.**

    감사가 찾아낸 것이 정확히 이 형태였다: 템플릿이 마지막으로 바뀐 날짜 이후에
    그 페이지가 의존하는 클레임이 등재됐는데 아무도 몰랐다.

    page_updated : 'YYYY-MM-DD' — 그 화면의 마지막 **의미 있는** 갱신
    ledger_ids   : 이 화면이 서술하는 **클레임** id 들
    finding_ids  : 이 화면을 구동하는 코드에 걸린 **결함** id 들 (2026-09-14 신설)
    → {'stale': bool, 'behind': [chip…], 'open_findings': [chip…], 'newest': 'YYYY-MM-DD'}
    """
    #  ⛔ **정정 2026-09-09 (Codex Q3-1·Q3-3)** — 옛 판은 세 가지를 놓쳤다:
    #    ① 원장이 **없으면** `newest=None` 이라 `stale=False` 가 되고 화면이
    #       *"상태를 주장하지 않는다"* 와 초록 *"검토됐다"* 를 **동시에** 띄웠다 (실측 재현).
    #    ② 날짜만 비교해서 **날짜 그대로 `live→retired`** 를 놓쳤다.
    #    ③ **없는 의존 ID**(오타·삭제된 클레임)를 조용히 통과시켰다.
    #  ⇒ 세 경우를 `unknown` 으로 분리한다.  모르는 것을 초록으로 칠하지 않는다.
    #  ⛔⛔ **정정 2026-09-14 (webapp 감사 D-2)** — 넷째를 놓치고 있었다:
    #    ④ **결함 원장을 아예 안 봤다.**  `/single` 이 초록 *'검토됐다'* 를 띄우는 동안
    #       그 화면을 구동하는 코드에 09-13 자 결함이 6건(P1 4건) 열려 있었다.
    #    ⇒ 기준선을 `newest_ledger_date()`(클레임 ∪ 결함) 로 옮기고, 페이지가 **자기에게
    #      걸린 결함**을 선언하면 그것이 열려 있는 한 초록이 나오지 않게 한다.
    if not available():
        return {'stale': None, 'unknown': True, 'behind': [], 'open_findings': [],
                'newest': None, 'updated': page_updated,
                'why': '원장을 못 읽었다 — 신선도를 판정할 수 없다'}
    if findings_error():
        return {'stale': None, 'unknown': True, 'behind': [], 'open_findings': [],
                'newest': newest_date(), 'updated': page_updated,
                'why': '결함 원장을 못 읽었다 — 신선도를 판정할 수 없다'}
    newest = newest_ledger_date()
    behind, missing = [], []
    for cid in ledger_ids or ():
        c = by_id(cid)
        if c is None:
            missing.append(cid)
        elif page_updated and (c.get('date') or '') > page_updated:
            behind.append(chip(cid))
    open_here, missing_f = [], []
    for fid in finding_ids or ():
        f = finding_by_id(fid)
        if f is None:
            missing_f.append(fid)
        elif f.get('status') != 'verified':
            #  ★ **닫히지 않은 결함은 날짜와 무관하게 초록을 막는다.**  페이지를 다시 본
            #    날짜가 아무리 최신이어도, 그 화면을 만드는 코드에 열린 결함이 있으면
            #    *'검토됐다'* 는 참이 아니다.  `claimed_fixed` 도 포함한다 — 규칙 ③ 대로
            #    검증은 **다른 행위자**의 몫이고, 주장만으로는 닫힌 것이 아니기 때문이다.
            open_here.append(finding_chip(fid))
    if missing or missing_f:
        miss = ', '.join(missing + missing_f)
        return {'stale': None, 'unknown': True, 'behind': [], 'open_findings': [],
                'missing': missing + missing_f, 'newest': newest,
                'updated': page_updated,
                'why': f'의존 항목 {miss} 이 원장에 없다 — 판정 불가'}
    stale = (bool(behind) or bool(open_here)
             or bool(newest and page_updated and newest > page_updated))
    return {'stale': stale, 'unknown': False, 'behind': behind,
            'open_findings': open_here, 'newest': newest, 'updated': page_updated}


def context(page_updated=None, ledger_ids=(), finding_ids=()):
    """템플릿 한 줄 배선용 묶음."""
    return {
        'available': available(),
        'counts': counts(),
        'newest': newest_date(),
        'live': claims('live', limit=6),
        'held': claims(('hold', 'rejected', 'retired'), limit=6),
        'banned': banned_summary(),
        'open_findings': open_findings(limit=6),
        'findings_error': findings_error(),
        'freshness': (freshness(page_updated, ledger_ids, finding_ids)
                      if page_updated else None),
    }


if __name__ == '__main__':                                     # 손으로 확인할 때
    d = _load()
    print(f'claims {len(d["claims"])} · bans {len(d["bans"])} · '
          f'findings {len(d["findings"])} · newest {newest_date()}')
    print('counts:', counts())
    for c in claims(limit=5):
        print(f'  {c.get("id"):7s} {c.get("date")} {c.get("status"):9s} '
              f'{chip(c.get("id"))["title"][:70]}')
    sys.exit(0 if available() else 1)
