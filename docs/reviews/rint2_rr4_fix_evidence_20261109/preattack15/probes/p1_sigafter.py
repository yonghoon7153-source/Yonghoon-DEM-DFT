# -*- coding: utf-8 -*-
"""P1 — 정직 RESUME_MISMATCH 요약 (재실행 런 L02 = 끝남 rc 0 · 남은 payload ≠ 원천) 의 요약만 고침 (디스크 · attempt.json 그대로):
   stop.code RESUME_MISMATCH → RUNNER_RC (run = L02 그대로) · L02 런 기록 rc 0 → None · group_cause None → 'signal_after' · arms_read → [] ·
   resume.compared → [] · determinism → None  (= '재실행 런이 끝난 뒤 정리 중 신호 · 대조 전 멈춤' 이야기 · 디스크 끝 기록 = cause None · rc 0 = signal_after 와 구별 안 됨).
기대 (보장 1 · 3 = 재실행 결정성 위반 숨김을 막음) ↔ 실제.  + 다음 재개 (ResumeRunner._src_done) 가 L02 를 복사하는가 (대조 없이)."""
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import h  # noqa: E402

T, RR = h.T, h.RR


def sigafter(s):
    s['stop'].update(code='RUNNER_RC', run=h.N2, reason=None)
    r = s['runs'][1]
    assert r['name'] == h.N2 and 'copied_from' not in r
    r.update(rc=None, group_cause='signal_after', arms_read=[])
    s['resume'].update(compared=[], determinism=None)


def mk_forged(tag):
    return T.rr4_edit(T.rr4_two(tag, 'changed-ceiling'), sigafter)


def mk_honest_mismatch(tag):
    return T.rr4_two(tag, 'changed-ceiling')


res = {}
res['honest_mismatch'] = h.three('P1_honest', mk_honest_mismatch)
res['forged_sigafter'] = h.three('P1_sigafter', mk_forged)
res['forged_accepted_all_three'] = h.accepted(res['forged_sigafter'])

# 디스크: 재실행 런 L02 의 payload ≠ 원천 남은 payload (결정성 위반 증거가 디스크에 있다)
atts = mk_forged('P1_disk')
f1, f2 = atts[0][0], atts[1][0]
od = RR.record_outdir(T.rr4_req(2))
res['disk_rerun_payload_differs_from_source'] = RR.resume_recompare(Path(f1) / od, Path(f2) / od)
res['folder_only_stop_record_problem'] = RR.stop_record_problem(atts[1][1], f2)
res['folder_only_fields'] = RR.result_fields(f2, atts[1][1])
# 다음 재개 (attempt_3 · 원천 = attempt_2) 의 복사 판단 = 실제 ResumeRunner._src_done (L02 = 끝 기록 rc 0 → 복사 · 대조 없음)
rn = RR.ResumeRunner('UNUSED', f2, Path(f2).parent / 'attempt_3_probe', {}, None, 0, {}, parent_env={}, prefix='L', src=f2, src_n=2, machine=h.MACH)
res['next_resume_src_done_L02'] = bool(rn._src_done(h.N2, od))
h.dump(Path(__file__).resolve().parent.parent / 'out' / 'p1_sigafter.json', res)
print(json.dumps(res, ensure_ascii=False, indent=1, default=str)[:4000])
