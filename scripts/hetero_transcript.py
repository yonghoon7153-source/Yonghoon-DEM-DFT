#!/usr/bin/env python3
"""이종기술 회의록 **해체 분석** — 원문 · 해독 · 주장을 세 층으로 갈라 붙든다.

    python3 scripts/hetero_transcript.py --ingest <회의록.txt> --out docs/data/hetero_transcript.json
    python3 scripts/hetero_transcript.py --verify docs/data/hetero_transcript.json --raw <회의록.txt>
    python3 scripts/hetero_transcript.py --selftest

★ **이 파일은 회의록보다 먼저 쓰인다.**  선례 = `lhs_perc_extract.py` (Codex R11 B1):
  *"추출기와 경계 fixture 를 **결과 전에** 커밋해야 이 규약이 실재한다."*  결과를 보고
  규약을 정하면 규약이 결과를 정당화한다.

═══ 왜 세 층인가 — 비준 (가) 의 내용 ═══

사용자 비준 2026-09-19: **61 발화 전수**에 `raw` · `decoded` · `claim` 을 **전부** 채운다.
기각된 쪽 (나) = *"raw 전수 + 선택 해독 ~35"*.  기각 사유는 하나다 —
**선택 해독은 "무엇을 안 골랐나" 가 기록에 남지 않는다.**  이 리포가 반복해서 데인 자리
(규율 ⑤: *"후보를 고르는 코드가 곧 사각지대"*) 와 같은 모양이다.

| 층 | 무엇 | 누가 썼나 | 바꿔도 되나 |
|---|---|---|---|
| `raw` | **회의에서 실제로 나온 말** | 사람 (녹취) | ⛔ 한 글자도 |
| `decoded` | 그 말이 **무슨 뜻인지** 푼 것 | 분석자 | ○ (근거를 남기고) |
| `claim` | 그 발화가 담은 **주장과 그 지위** | 분석자 | ○ (지위를 바꾸면 기록) |

⚠ 셋을 한 칸에 적으면 **원문이 해석에 오염된다** — 그리고 그 오염은 되돌릴 수 없다
(원문이 이미 고쳐졌으므로).  그래서 `raw` 는 재조립해 원본 파일과 **sha256 으로 대조**한다.

═══ 계약 여섯 ═══

① **원문 무손실** — `raw` 를 원문 순서로 이으면 원본 바이트가 **정확히** 나온다.
   (자르기 규칙이 무엇이든 이 검사를 통과해야 한다 ⇒ 규칙을 몰라도 안전하다.)
② **전수** — 선언한 발화 수와 실제 수가 다르면 거부.  번호는 `1..N` 빠짐없이.
③ **빈 해독 금지** — `decoded` · `claim` 이 비면 거부.
④ **복사 금지** — `decoded` 가 `raw` 와 (공백 정규화 후) 같으면 거부.
   ⚠ 이것이 ③ 의 진짜 이빨이다: 전수를 강제하면 **칸을 채우려고 원문을 복사**하게 된다.
⑤ **추정 금지** — 화자·시각은 원문에 있으면 쓰고 **없으면 `null`**.  화면은 `null` 을
   *"미상"* 으로 보인다.  지어내지 않는다.
⑥ **모르면 모른다고** — `claim_status = UNCERTAIN` 이 **허용된다**.  전수 강제의 배출구다.
   ⛔ 다만 그때 `decoded` 는 *"왜 확정 못 하는지"* 를 적어야 한다 (`why_uncertain`).
   ⚠ 이 구멍이 없으면 ③ 이 **날조를 강요**한다 — 전수 규약의 가장 큰 위험이 그것이다.

═══ `claim_status` 어휘 ═══

`FACT_STATED` 회의에서 사실로 진술됨 — ⚠ **우리가 검증했다는 뜻이 아니다** ·
`PLAN` 하기로 한 것 · `REQUEST` 요청·지시 · `QUESTION` 물음 · `OPINION` 판단·의견 ·
`NO_CLAIM` 주장 없음 (인사·추임새·중복) · `UNCERTAIN` 원문만으로 확정 불가 (계약⑥).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata

CLAIM_STATUS = ('FACT_STATED', 'PLAN', 'REQUEST', 'QUESTION', 'OPINION',
                'NO_CLAIM', 'UNCERTAIN')
#: 계약⑤ — 원문에 시각이 있으면 이 모양이다.  **없으면 null 이지 추정이 아니다.**
TS_RE = re.compile(r'^\s*\(?(\d{1,2}):(\d{2})(?::(\d{2}))?\)?\s*')
SCHEMA_VERSION = 'hetero_transcript_v1'


class TranscriptRefusal(RuntimeError):
    """해체가 조용히 반쪽이 되는 것을 막는다."""


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def _norm(s):
    """공백·유니코드 정규화 — 계약④ 의 '같은가' 판정에만 쓴다 (저장에는 안 쓴다)."""
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', s)).strip()


def split_raw(text, rule='blocks'):
    """원문을 발화로 자른다.  **자르기만 한다 — 한 글자도 안 고친다.**

    `blocks` = 빈 줄로 나뉜 덩어리 · `lines` = 빈 줄이 아닌 줄.
    반환 = `(head, [(raw, sep), ...])`.  `head` 는 첫 발화 앞의 공백, `sep` 은 그 발화
    **뒤에** 붙어 있던 구분자다.
    ⚠ **원문의 모든 바이트가 셋 중 하나에 들어간다** — 이것이 계약① 이 성립하는 이유다.
      초판은 빈 조각을 버려서 재조립이 원문과 달라졌다.  구분자를 '보기 싫은 잡음' 으로
      여기는 순간 원문 보존이 깨진다.
    ⚠ 자르기 규칙을 **잘못 골라도 조용히 틀리지 않는다** — 이어붙인 결과가 원문과 다르면
      계약① 이 거부한다.  규칙은 발화 **경계**를 정할 뿐 내용을 못 바꾼다.
    """
    if rule not in ('blocks', 'lines'):
        raise TranscriptRefusal(f'모르는 자르기 규칙: {rule!r}')
    pat = r'(\n[ \t]*\n\s*)' if rule == 'blocks' else r'(\n)'
    parts = re.split(pat, text)
    head, out = '', []
    i = 0
    while i < len(parts):
        body = parts[i]
        sep = parts[i + 1] if i + 1 < len(parts) else ''
        if body.strip():
            out.append([body, sep])
        elif out:                     # 내용 없는 조각 — 앞 발화의 꼬리에 얹는다
            out[-1][1] += body + sep
        else:                         # 아직 발화가 없다 — 머리말에 얹는다
            head += body + sep
        i += 2
    return head, [(b_, s_) for b_, s_ in out]


def probe_meta(raw):
    """계약⑤ — 시각·화자를 **원문에 있을 때만** 읽는다.  없으면 `None`."""
    ts = None
    m = TS_RE.match(raw)
    rest = raw
    if m:
        h, mi, s = m.group(1), m.group(2), m.group(3)
        ts = f'{int(h):02d}:{mi}' + (f':{s}' if s else '')
        rest = raw[m.end():]
    speaker = None
    m2 = re.match(r'\s*([^\s:：][^:：\n]{0,24})[:：]\s', rest)
    if m2:
        speaker = m2.group(1).strip()
    return ts, speaker


def ingest(path, rule='blocks', n_expect=None):
    """원문 → 골격.  `decoded`·`claim` 은 **빈 채로** 둔다 (사람이 채운다).

    ⛔ 이 도구는 해독을 **생성하지 않는다** — 빈 칸을 남겨 계약③ 이 걸리게 한다.
    """
    data = open(path, 'rb').read()
    text = data.decode('utf-8')
    head, parts = split_raw(text, rule)
    if n_expect is not None and len(parts) != n_expect:
        raise TranscriptRefusal(
            f'발화 {len(parts)} 개로 잘렸는데 {n_expect} 을 기대했다 (규칙 {rule!r}).  '
            '⇒ 자르기 규칙이 맞지 않는다.  다른 `--split` 을 쓰거나 기대값을 확인할 것 '
            '— **수를 맞추려고 원문을 고치지 말 것**.')
    utt = []
    for k, (body, sep) in enumerate(parts, 1):
        ts, sp = probe_meta(body)
        utt.append({'n': k, 'raw': body, 'sep': sep, 'ts': ts, 'speaker': sp,
                    'decoded': '', 'claim': '', 'claim_status': '',
                    'why_uncertain': ''})
    return {'schema': SCHEMA_VERSION, 'split_rule': rule,
            'head': head,
            'source': {'path': os.path.basename(path), 'sha256': sha256_bytes(data),
                       'n_bytes': len(data)},
            'n_utterances': len(utt),
            'scope': ('비준 2026-09-19 = (가) 61 발화 **전수**에 raw·decoded·claim. '
                      '기각 = (나) 선택 해독 — "무엇을 안 골랐나" 가 안 남는다.'),
            'claim_status_vocab': list(CLAIM_STATUS),
            'utterances': utt}


def reassemble(doc):
    """계약① — 발화를 원문 순서로 이어 **원본 바이트**를 만든다."""
    return (doc.get('head', '')
            + ''.join(u['raw'] + u.get('sep', '') for u in doc['utterances'])
            ).encode('utf-8')


def check(doc, raw_path=None, require_filled=True):
    """계약 여섯을 전부 잰다.  하나라도 깨지면 `TranscriptRefusal`."""
    bad = []
    utt = doc.get('utterances') or []

    # ② 전수 · 번호 연속
    if len(utt) != doc.get('n_utterances'):
        bad.append(f'② 선언 {doc.get("n_utterances")} ≠ 실제 {len(utt)}')
    ns = [u.get('n') for u in utt]
    if ns != list(range(1, len(utt) + 1)):
        miss = sorted(set(range(1, len(utt) + 1)) - set(n for n in ns if isinstance(n, int)))
        bad.append(f'② 번호가 1..{len(utt)} 연속이 아니다 (빠짐 {miss[:8]})')

    # ① 원문 무손실
    if raw_path is not None:
        want = open(raw_path, 'rb').read()
        got = reassemble(doc)
        if got != want:
            bad.append(f'① 재조립이 원문과 다르다 (원문 {len(want)}B · 재조립 {len(got)}B, '
                       f'sha {sha256_bytes(want)[:12]} ≠ {sha256_bytes(got)[:12]}) '
                       '— **원문이 고쳐졌거나 조각이 빠졌다**')
        if doc.get('source', {}).get('sha256') not in (None, sha256_bytes(want)):
            bad.append('① 기록된 source.sha256 이 지금 원문과 다르다 — 원문이 바뀌었다')

    for u in utt:
        n = u.get('n')
        st = u.get('claim_status') or ''
        if not (u.get('raw') or '').strip():
            bad.append(f'#{n}: raw 가 비었다')
        if require_filled:
            # ③ 빈 해독 금지
            if not (u.get('decoded') or '').strip():
                bad.append(f'#{n}: ③ decoded 가 비었다')
            if not (u.get('claim') or '').strip():
                bad.append(f'#{n}: ③ claim 이 비었다')
            if st not in CLAIM_STATUS:
                bad.append(f'#{n}: claim_status 가 어휘 밖이다 ({st!r})')
            # ⑥ 모르면 모른다고 — 단 사유를 적는다
            if st == 'UNCERTAIN' and not (u.get('why_uncertain') or '').strip():
                bad.append(f'#{n}: ⑥ UNCERTAIN 인데 why_uncertain 이 비었다 '
                           '— 확정 못 하는 **이유**가 기록의 내용이다')
            if st and st != 'UNCERTAIN' and (u.get('why_uncertain') or '').strip():
                bad.append(f'#{n}: why_uncertain 은 UNCERTAIN 에만 쓴다 (지금 {st})')
        # ④ 복사 금지
        if (u.get('decoded') or '').strip() and _norm(u['decoded']) == _norm(u['raw']):
            bad.append(f'#{n}: ④ decoded 가 raw 의 복사다 — 해독이 아니다')
    if bad:
        raise TranscriptRefusal(f'{len(bad)} 건 위반:\n  - ' + '\n  - '.join(bad[:20])
                                + (f'\n  … 외 {len(bad) - 20} 건' if len(bad) > 20 else ''))
    return {'n_utterances': len(utt),
            'status_tally': {s: sum(1 for u in utt if u.get('claim_status') == s)
                             for s in CLAIM_STATUS
                             if any(u.get('claim_status') == s for u in utt)},
            'n_ts': sum(1 for u in utt if u.get('ts')),
            'n_speaker': sum(1 for u in utt if u.get('speaker'))}


# ═══ 자기검사 ═══════════════════════════════════════════════════════════════════

_FAILS = []


def chk(name, ok):
    print(('  ✓ ' if ok else '  ✗ ') + name)
    if not ok:
        _FAILS.append(name)


def neg(name, fn, want=TranscriptRefusal):
    """음성대조 — **그 오류 종류로** 거부해야 통과 (아무 예외나 세지 않는다)."""
    try:
        fn()
    except want as e:
        print(f'  ✓ {name} — 거부: {str(e)[:78]}')
        return
    except Exception as e:                                        # noqa: BLE001
        chk(f'{name} (기대 {want.__name__}, 실제 {type(e).__name__}: {e})', False)
        return
    chk(f'{name} (거부하지 않았다)', False)


def _fill(doc, decoded='그 말은 X 라는 뜻이다', claim='X 를 한다', status='PLAN'):
    for u in doc['utterances']:
        u['decoded'] = f'#{u["n"]} ' + decoded
        u['claim'] = f'#{u["n"]} ' + claim
        u['claim_status'] = status
    return doc


def selftest():
    import tempfile

    print('hetero_transcript — 자기검사 (계약 6개)')
    #  ① 원문 무손실 — 여러 모양에서 재조립이 **바이트 동일**이어야 한다
    SHAPES = {
        '보통': 'ㄱ 발화 하나\n\n두 번째\n\n세 번째\n',
        '선행 공백': '\n\n  머리 공백 뒤 첫 발화\n\n둘째\n',
        '끝 개행 없음': '하나\n\n둘',
        '빈 줄 여러 개': '하나\n\n\n\n둘\n\n셋\n\n',
        '줄 안 공백': '하나   \n\n   둘\n',
        '한 발화뿐': '전부 한 덩어리다\n',
    }
    with tempfile.TemporaryDirectory() as tmp:
        for rule in ('blocks', 'lines'):
            bad = []
            for nm, txt in SHAPES.items():
                p = os.path.join(tmp, 'r.txt')
                with open(p, 'w', encoding='utf-8') as fh:
                    fh.write(txt)
                doc = ingest(p, rule=rule)
                if reassemble(doc) != txt.encode('utf-8'):
                    bad.append(nm)
            chk(f'① 계약①: 재조립이 원문과 바이트 동일 ({rule}, {len(SHAPES)} 모양)', not bad)
            if bad:
                print('       어긋난 모양:', bad)

        p = os.path.join(tmp, 'm.txt')
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write('(00:12) 김: 첫 발화다\n\n둘째 발화\n\n(1:02:03) 셋째\n')
        doc = ingest(p, rule='blocks')
        chk('② 세 발화로 잘리고 번호가 1..3', [u['n'] for u in doc['utterances']] == [1, 2, 3])
        #  ⑤ 추정 금지 — 있으면 읽고 없으면 None
        chk('⑤ 계약⑤: 시각·화자는 **있을 때만** 읽는다',
            doc['utterances'][0]['ts'] == '00:12'
            and doc['utterances'][0]['speaker'] == '김'
            and doc['utterances'][1]['ts'] is None
            and doc['utterances'][1]['speaker'] is None)
        chk('⑤ 시:분:초도 읽는다', doc['utterances'][2]['ts'] == '01:02:03')
        #  ⑦ 수확기는 **해독을 만들지 않는다**
        chk('⑦ ingest 는 decoded·claim 을 빈 채로 둔다 (사람이 채운다)',
            all(not u['decoded'] and not u['claim'] and not u['claim_status']
                for u in doc['utterances']))
        neg('⑦ 빈 골격은 계약③ 에 걸린다 (빈 채로 통과시키지 않는다)',
            lambda: check(doc, raw_path=p))
        chk('⑦ 단 require_filled=False 면 원문 계약만 잰다 (수확 직후 점검용)',
            check(json.loads(json.dumps(doc)), raw_path=p,
                  require_filled=False)['n_utterances'] == 3)

        #  ⑧ 기대 발화 수가 다르면 거부 — **수를 맞추려 원문을 고치지 말라**
        neg('⑧ 기대 발화 수 불일치 → 거부',
            lambda: ingest(p, rule='blocks', n_expect=61))

        good = _fill(json.loads(json.dumps(doc)))
        rep = check(good, raw_path=p)
        chk('⑩ 정상 문서는 통과한다 (거부 과잉이 아니다)',
            rep['n_utterances'] == 3 and rep['status_tally'] == {'PLAN': 3})
        chk('⑩ 보고에 시각·화자 실측 수가 있다', rep['n_ts'] == 2 and rep['n_speaker'] == 1)

        #  ② 번호 빠짐
        def _gap():
            d = json.loads(json.dumps(good)); d['utterances'][1]['n'] = 9
            check(d, raw_path=p)
        neg('② 계약②: 번호가 연속이 아니면 거부', _gap)

        def _short():
            d = json.loads(json.dumps(good)); d['utterances'].pop()
            check(d, raw_path=p)
        neg('② 발화가 빠지면 거부 (선언 수와 불일치)', _short)

        #  ① 원문이 **고쳐지면** 잡힌다 (이 검사의 이빨)
        def _tamper():
            d = json.loads(json.dumps(good))
            d['utterances'][0]['raw'] = d['utterances'][0]['raw'].replace('첫', '첬')
            check(d, raw_path=p)
        neg('① ★이빨: raw 를 한 글자만 고쳐도 재조립 대조가 잡는다', _tamper)

        def _drop_sep():
            d = json.loads(json.dumps(good))
            d['utterances'][0]['sep'] = ''
            check(d, raw_path=p)
        neg('① ★이빨: 구분자를 버려도 잡는다 (공백도 원문이다)', _drop_sep)

        #  ③ 빈 해독
        for fld in ('decoded', 'claim'):
            def _empty(fld=fld):
                d = json.loads(json.dumps(good)); d['utterances'][2][fld] = '  '
                check(d, raw_path=p)
            neg(f'③ 계약③: {fld} 가 비면 거부', _empty)

        def _badstatus():
            d = json.loads(json.dumps(good)); d['utterances'][0]['claim_status'] = 'MAYBE'
            check(d, raw_path=p)
        neg('③ claim_status 가 어휘 밖이면 거부', _badstatus)

        #  ④ ★ 복사 금지 — 전수 강제의 가장 흔한 빠져나가기
        def _copy():
            d = json.loads(json.dumps(good))
            d['utterances'][0]['decoded'] = '  ' + d['utterances'][0]['raw'].strip() + ' '
            check(d, raw_path=p)
        neg('④ ★계약④: decoded 가 raw 의 복사면 거부 (공백만 달라도)', _copy)

        #  ⑥ 모르면 모른다고 — 단 사유를 적는다
        def _unc_no_why():
            d = json.loads(json.dumps(good)); d['utterances'][1]['claim_status'] = 'UNCERTAIN'
            check(d, raw_path=p)
        neg('⑥ 계약⑥: UNCERTAIN 인데 why_uncertain 이 없으면 거부', _unc_no_why)

        def _why_wrong_place():
            d = json.loads(json.dumps(good)); d['utterances'][1]['why_uncertain'] = '애매'
            check(d, raw_path=p)
        neg('⑥ why_uncertain 을 UNCERTAIN 아닌 곳에 쓰면 거부', _why_wrong_place)

        d = json.loads(json.dumps(good))
        d['utterances'][1].update(claim_status='UNCERTAIN',
                                  why_uncertain='지시대명사의 선행사가 원문에 없다')
        chk('⑥ ★UNCERTAIN + 사유는 **통과한다** — 전수 강제의 배출구',
            check(d, raw_path=p)['status_tally'].get('UNCERTAIN') == 1)

        #  원문 파일 자체가 바뀌면 잡힌다
        def _src_changed():
            q = os.path.join(tmp, 'm2.txt')
            with open(q, 'w', encoding='utf-8') as fh:
                fh.write('(00:12) 김: 첫 발화다\n\n둘째 발화\n\n(1:02:03) 셋째 바뀜\n')
            check(good, raw_path=q)
        neg('① 원본 파일이 바뀌면 거부 (sha 대조)', _src_changed)

    print()
    if _FAILS:
        print(f'✗ {len(_FAILS)} 건 실패')
        for f in _FAILS:
            print('   -', f)
        return 1
    print('✓ 전부 통과   ⚠ 이 통과는 **계약이 도구에 박혔다**는 뜻이지 '
          '실제 해독이 옳다는 뜻이 아니다 — 해독의 옳음은 사람이 본다')
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        description='이종기술 회의록 해체 — 원문·해독·주장 세 층 (비준 (가) 전수)')
    ap.add_argument('--ingest', metavar='TXT', help='원문 → 골격 JSON (해독은 빈 칸)')
    ap.add_argument('--split', choices=('blocks', 'lines'), default='blocks')
    ap.add_argument('--n-expect', type=int, default=None,
                    help='기대 발화 수.  다르면 **거부** — 수를 맞추려 원문을 고치지 말 것')
    ap.add_argument('--out', help='--ingest 산출 JSON')
    ap.add_argument('--verify', metavar='JSON', help='계약 여섯을 전부 잰다')
    ap.add_argument('--raw', metavar='TXT', help='--verify 의 원문 (계약① 대조)')
    ap.add_argument('--allow-empty', action='store_true',
                    help='--verify 에서 계약③④⑥ 을 건너뛴다 (수확 직후 원문 계약만 볼 때)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.ingest:
        doc = ingest(a.ingest, rule=a.split, n_expect=a.n_expect)
        txt = json.dumps(doc, ensure_ascii=False, indent=1)
        if a.out:
            with open(a.out, 'w', encoding='utf-8') as fh:
                fh.write(txt + '\n')
            print(f'→ {a.out}   발화 {doc["n_utterances"]} 개')
        else:
            print(txt)
        r = check(doc, raw_path=a.ingest, require_filled=False)
        print(f'계약①②⑤ 통과 · 시각 {r["n_ts"]} · 화자 {r["n_speaker"]}')
        print('⬜ 남은 일: 발화마다 decoded · claim · claim_status 를 채운다 (전수).')
        return 0
    if a.verify:
        doc = json.loads(open(a.verify, encoding='utf-8').read())
        r = check(doc, raw_path=a.raw, require_filled=not a.allow_empty)
        print(f'✓ 계약 여섯 통과 — 발화 {r["n_utterances"]} · '
              f'시각 {r["n_ts"]} · 화자 {r["n_speaker"]}')
        print('  주장 지위:', ' · '.join(f'{k} {v}' for k, v in sorted(r['status_tally'].items())))
        if not a.raw:
            print('  ⚠ `--raw` 없이 쟀다 — 계약① (원문 무손실) 은 **검사되지 않았다**')
        return 0
    ap.print_help()
    return 2


if __name__ == '__main__':
    try:
        sys.exit(main())
    except TranscriptRefusal as e:
        print(f'⛔ {e}', file=sys.stderr)
        sys.exit(1)
