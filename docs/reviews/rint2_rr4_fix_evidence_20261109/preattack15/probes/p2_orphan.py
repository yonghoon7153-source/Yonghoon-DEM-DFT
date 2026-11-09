# -*- coding: utf-8 -*-
"""P2 — 정직 RESUME_MISMATCH 재실행 시도 attempt_2 의 단계 요약 파일을 지움 (요약 없는 시도 = 사슬 부모 사망 꼴 · 디스크 · attempt.json 그대로) → 세 자리.
   기대 (보장 1 · 3) ↔ 실제.  + 정직 짝: 재실행 런을 다 푼 뒤 (대조 전) 사슬 부모 사망 = 같은 디스크 → 다음 재개가 L02 를 대조 없이 복사하는가."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import h  # noqa: E402

T, RR = h.T, h.RR


def mk_deleted(tag):
    atts = T.rr4_two(tag, 'changed-ceiling')
    f2 = atts[1][0]
    (Path(f2) / 'ladder_summary.json').unlink()
    return [atts[0], (f2, None)]


res = {'forged_summary_deleted': h.three('P2_orphan', mk_deleted)}
res['accepted_all_three'] = h.accepted(res['forged_summary_deleted'])
atts = mk_deleted('P2_disk')
f1, f2 = atts[0][0], atts[1][0]
od = RR.record_outdir(T.rr4_req(2))
res['orphan_cause'] = RR.orphan_cause(f2)
res['disk_rerun_payload_vs_source'] = RR.resume_recompare(Path(f1) / od, Path(f2) / od)
rn = RR.ResumeRunner('UNUSED', f2, Path(f2).parent / 'attempt_3_probe', {}, None, 0, {}, parent_env={}, prefix='L', src=f2, src_n=2, machine=h.MACH)
res['next_resume_src_done_L02'] = bool(rn._src_done(h.N2, od))
h.dump(Path(__file__).resolve().parent.parent / 'out' / 'p2_orphan.json', res)
print(json.dumps(res, ensure_ascii=False, indent=1, default=str)[:3000])
