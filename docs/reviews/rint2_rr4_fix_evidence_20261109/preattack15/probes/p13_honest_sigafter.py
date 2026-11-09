# -*- coding: utf-8 -*-
"""P13 — P1 의 정직 짝: 실제 `ResumeRunner.run` 에서 재실행 런 L02 의 가짜 `_execute` 가 `Runner._execute` 의 signal_after 가지 그대로 (러너 끝 rc 0 · 디스크 끝
   기록 cause None · rc 0 · 확인 True · 런 기록 rc None · group_cause signal_after · arms_read [] · Stop RUNNER_RC) → 요약 = P1 위조 요약과 같은가 (seconds 칸 뺌)
   · 세 자리 · 남은 payload 다른데 (비결정) 자격 True 인가 · 다음 재개 `_src_done(L02)` = 복사 (대조 없이)."""
import contextlib
import copy
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import h  # noqa: E402

T, RR = h.T, h.RR


def honest_sigafter(tag, ceiling='changed-ceiling'):
    base = Path(T.TD) / 'rr4' / tag
    a1 = T.rr4_first(base)
    dst = T.rr4_att(base / 'attempt_2', 2, 1)
    rn = RR.ResumeRunner('UNUSED', a1[0], dst, {}, None, 0, {}, parent_env={}, prefix='L', src=a1[0], src_n=1, machine=h.MACH)
    rn.env_delta = lambda *_a: {}

    def fake_execute(name, q, od, delta):                      # `Runner._execute` signal_after 가지 (run_in_group = 원인 signal_after · 디스크 끝 = None · rc 0)
        rec = T.rr4_files(dst, 2, ceiling, rc=0)
        rec.update(rc=None, group_cause='signal_after', arms_read=[])
        rn.records.append(rec)
        raise RR.Stop('RUNNER_RC', f'{name}: 사슬이 신호 SIGTERM 를 받았다 (러너가 끝난 뒤 정리 중 · 시험)', name)

    def fake_read(outdir, req, *_a, **_k):
        return [dict(T.rr4_pub((Path(outdir) / T.RR4_FN).read_bytes()), sigma=1.0, dsigma_rel=0.0)]
    rn._execute = fake_execute
    code, run = None, None
    with T.rc_patch(read_run=fake_read), contextlib.redirect_stdout(io.StringIO()):
        try:
            for i in (1, 2):
                role, rj = T.RR4_ROLES[i - 1]
                rn.run(T.SBE_KIT, role, 'P0', None, rj, 1)
        except RR.Stop as e:
            code, run = e.code, e.run
    return [a1, (dst, T.rr4_put(dst, T.rr4_summ(code, run, copy.deepcopy(rn.records), copy.deepcopy(rn.resume))))]


def strip(s):
    s = copy.deepcopy(s)
    for r in s['runs']:
        r.pop('seconds', None)
    return s


hon = honest_sigafter('P13_cmp')
import p1_sigafter as P1  # noqa: E402  (P1 모듈 실행부가 같이 돈다 · 결과 파일은 같은 내용으로 다시 씀)
forged = T.rr4_edit(T.rr4_two('P13_forged', 'changed-ceiling'), P1.sigafter)
res = {'honest_summary_equals_forged_except_seconds': strip(hon[1][1]) == strip(forged[1][1])}
o = h.three('P13_honest_sigafter', honest_sigafter)
res['honest_sigafter_three'] = {'writer': o['writer'], 'places': o['places'], 'cli': o['cli'], 'accepted': h.accepted(o)}
f1, f2 = Path(hon[0][0]), Path(hon[1][0])
od = RR.record_outdir(T.rr4_req(2))
res['rerun_payload_vs_source'] = RR.resume_recompare(f1 / od, f2 / od)
rn = RR.ResumeRunner('UNUSED', f2, f2.parent / 'attempt_3_probe', {}, None, 0, {}, parent_env={}, prefix='L', src=f2, src_n=2, machine=h.MACH)
res['next_resume_src_done_L02'] = bool(rn._src_done(h.N2, od))
h.dump(Path(__file__).resolve().parent.parent / 'out' / 'p13_honest_sigafter.json', res)
print(json.dumps(res, ensure_ascii=False, default=str))
