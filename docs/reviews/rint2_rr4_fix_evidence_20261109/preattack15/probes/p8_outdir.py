# -*- coding: utf-8 -*-
"""P8 — 정직 RESUME_MISMATCH 요약만 고침 (디스크 · attempt.json 그대로): 재실행 런 L02 기록의 요청 칸 · 출력 폴더를 다른 이름으로 (arms 1 → 2 · outdir
   L02_ceiling_arm1 → L02_ceiling_arm2 · arms_read 를 그 요청 팔 수에 맞춘 판독 완료 꼴 두 개) + 멈춤 = 다음 런 L03 런 전 TIME_LIMIT + resume.compared [] ·
   determinism 'assumed'.  디스크: L02_ceiling_arm2 폴더는 원천에도 이 시도에도 없다 (실제 재실행 출력 = L02_ceiling_arm1 · 원천 남은 payload 와 다름).
   기대 (보장 1 ⓒ · ⓓ "실제 첫 새 런 payload 다시 대조") ↔ 실제."""
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import h  # noqa: E402

T, RR = h.T, h.RR


def relabel(s):
    T.rr4_tl(s)                                               # 멈춤 = TIME_LIMIT · L03_point (런 기록 없음)
    r = s['runs'][1]
    assert r['name'] == h.N2 and 'copied_from' not in r and r['arms'] == 1
    a0 = r['arms_read'][0]
    a1 = dict(a0, index=1, file=a0['file'].replace('_a0.json', '_a1.json'), sha256='e' * 64)
    r.update(arms=2, outdir=h.N2 + '_arm2', arms_read=[a0, a1])
    s['resume'].update(compared=[], determinism='assumed')


def mk(tag):
    return T.rr4_edit(T.rr4_two(tag, 'changed-ceiling'), relabel)


res = {'forged_outdir_relabel': h.three('P8_outdir', mk)}
res['accepted_all_three'] = h.accepted(res['forged_outdir_relabel'])
atts = mk('P8_disk')
f1, f2 = Path(atts[0][0]), Path(atts[1][0])
res['disk'] = {'attempt2_has_L02_arm2': (f2 / (h.N2 + '_arm2')).exists(), 'attempt2_has_L02_arm1': (f2 / (h.N2 + '_arm1')).is_dir(),
               'true_rerun_vs_source': RR.resume_recompare(f1 / (h.N2 + '_arm1'), f2 / (h.N2 + '_arm1'))}
rn = RR.ResumeRunner('UNUSED', f2, f2.parent / 'attempt_3_probe', {}, None, 0, {}, parent_env={}, prefix='L', src=f2, src_n=2, machine=h.MACH)
res['next_resume_src_done_L02_true_outdir'] = bool(rn._src_done(h.N2, h.N2 + '_arm1'))
h.dump(Path(__file__).resolve().parent.parent / 'out' / 'p8_outdir.json', res)
o = res['forged_outdir_relabel']
print('accepted_all_three', res['accepted_all_three'], '| writer', o['writer'], '| places', o['places'], '| cli', o['cli'])
print(json.dumps(res['disk'], ensure_ascii=False), 'next_src_done', res['next_resume_src_done_L02_true_outdir'])
