# -*- coding: utf-8 -*-
"""P3 — 보장 5 (결과 줄 쓰기 ↔ 다시 셈 대칭 · 찾는 곳이 달라도): 정직 재실행 시도 attempt_2 (대조 같음 뒤 멈춤 · 폴더 증거 자격 True) ·
   원천 attempt_1 을 recover 전에 다른 바탕 B2 로 옮김 (판정 --attempt-dirs = "다른 곳에 둔 시도") → 실제 git 원장 · 실제 recover CLI (같은 바탕 = 원천 없음 →
   자격 False [원천]) → 판정 대조 `target_ledger_problem` (찾은 폴더 = B + B2 · 다시 셈 = 원천 있음 → True) = ATTEMPT_LEDGER_MISMATCH 인가.
   대조군 = 옮기지 않음 (같은 절차 · 통과)."""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import h  # noqa: E402

T, RR = h.T, h.RR


def build(tag, move):
    atts = T.rr4_two(tag, 'source-ceiling')                    # 정직 대조 같음 뒤 멈춤 (다음 런 L03 런 전 TIME_LIMIT)
    (f1, s1), (f2, s2) = atts
    d, _rc, _so = T.led_new(f'PA15_P3_{tag}')
    head = T.led_lines(d)[0]
    lines = T.rr4_lines(atts, head_plan=head['plan_sha256'], last_result=False)   # [머리, 항목1, 시작1, 결과1, 항목2, 시작2]
    e1, s01, _r1, e2, s02 = lines[1:]
    c1 = T.led_hand(d, e1)
    T.rr4_att_set(f1, ledger_commit=c1)
    T.led_hand(d, s01)
    T.led_hand(d, RR.attempt_result_line(1, f1, s1, 'recover'))     # 원 시도 결과 줄 (생산자 꼴)
    c2 = T.led_hand(d, e2)
    T.rr4_att_set(f2, ledger_commit=c2)
    T.led_hand(d, s02)
    b, b2 = Path(f1).parent, Path(T.TD) / 'rr4' / f'{tag}_archive'
    if move:
        b2.mkdir(parents=True)
        shutil.move(str(f1), str(b2 / 'attempt_1'))
    rc, so = T.call(['--stage', 'recover', '--out', str(f2), '--ledger', str(d)])
    r2 = T.led_result(d, 2) or {}
    raw = T.led_raw(d)
    st = RR.ledger_parse(raw)
    head_c = T.git_(d, 'rev-parse', 'HEAD')
    found = RR._attempt_folders([b, b2] if move else [b])
    try:
        ns, ad, _p = RR.target_ledger_problem(d, st, raw, head_c, 'ladder:P0', found)
        tl = ['ok', ns, ad['effective']]
    except RR.Stop as e:
        tl = ['Stop', e.code, e.cause[:400]]
    rec = RR.result_line_problem(2, f2, r2, st=st, found=found)
    return {'recover_rc': rc, 'line_resume_ok': r2.get('resume_ok'), 'commit_msg_tags': T.rr4_tag(T.git_(d, 'log', '-1', '--format=%B')),
            'recount_problem': (rec or '')[:400] or None, 'target_ledger_problem': tl}


res = {'control_not_moved': build('ctl', False), 'moved_before_recover': build('mv', True)}
h.dump(Path(__file__).resolve().parent.parent / 'out' / 'p3_moved_source.json', res)
print(json.dumps(res, ensure_ascii=False, indent=1))
