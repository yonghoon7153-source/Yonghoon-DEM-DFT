# -*- coding: utf-8 -*-
"""P5 — 판정문 반례 부류의 변형 (요약 · attempt.json · 디스크 한 곳) 을 세 자리 (결과 줄 쓰기 직접 · 실제 recover CLI · 차례 · 사슬) 에 → 상태.
   accepted = 세 자리 모두 자격 True · 통과 (거짓 통과) · rejected = 하나라도 거부 (어디서 어떤 표지)."""
import json
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import h  # noqa: E402

T, RR = h.T, h.RR
N1, N2, N3 = h.N1, h.N2, h.N3


def ed(base_fn, *fns, att=None, disk=None):
    def mk(tag):
        atts = base_fn(tag)
        atts = T.rr4_edit(atts, *fns, att=att) if (fns or att) else atts
        if disk:
            disk(atts)
        return atts
    return mk


mism = lambda t: T.rr4_two(t, 'changed-ceiling')                      # noqa: E731 정직 RESUME_MISMATCH
okc = lambda t: T.rr4_two(t, 'source-ceiling')                        # noqa: E731 정직 대조 같음 뒤 멈춤 (자격 True)
three = lambda t: T.rr4_three(t, 'newer-different-ceiling')           # noqa: E731 정직 3 시도 (자격 True)


def r1_bool(s):
    T.rr4_r1(s)
    s['runs'][1]['copied_from'] = True


def r1_det_assumed(s):
    """R1 의 다른 꼴 — L02 = 새 런 그대로 · 멈춤 L03 · compared [] · assumed (원천에 남은 payload 없다는 주장)."""
    T.rr4_tl(s)
    s['resume'].update(compared=[], determinism='assumed')


def r2_swap(s):
    """R2 + 복사 기록 순서: L01 copied_from 지움 · 런 기록 L02 를 앞으로."""
    T.rr4_r2(s)
    s['runs'] = [s['runs'][1], s['runs'][0]]
    s['resume']['rerun'] = N2


def dup_copy(s):
    """같은 이름 런 둘 — 정직 대조 같음 요약에 L01 복사 기록 하나 더."""
    s['runs'].insert(1, dict(s['runs'][0]))
    s['resume']['copied'] = [N1, N1]


def from_str(s):
    s['resume']['from'] = '1'


def from_float(s):
    s['resume']['from'] = 1.0


def copied_from_other(s):
    """3 시도 사슬 끝 (원천 2) 의 L01 copied_from 2 → 1 만."""
    s['runs'][0]['copied_from'] = 1


def extra_new_copied_from(s):
    """새 런 L02 에 copied_from 칸 하나 더 (값 = from)."""
    T.rr4_tl(s)
    s['runs'][1]['copied_from'] = 1
    s['resume']['copied'] = [N1, N2]
    s['resume']['rerun'] = N3
    s['resume']['compared'], s['resume']['determinism'] = [], None


def disk_end_byte(atts):
    """디스크 — 복사 런 L01 의 groups/L01.end.json 한 칸 바꿈 (launch 같고 end 만 다름 · 요약 정직)."""
    p = Path(atts[-1][0]) / 'groups' / f'{N1}.end.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    d['killed'] = 0
    p.write_bytes(RR.canon_bytes(d))


def disk_copy_payload(atts):
    """디스크 — 복사 런 L01 의 payload 바이트 바꿈 (이름만 같음)."""
    od = RR.record_outdir(T.rr4_req(1))
    p = Path(atts[-1][0]) / od / T.RR4_FN
    p.write_bytes(RR.canon_bytes({'synthetic': 'tampered-floor'}))


def disk_src_symlink(atts):
    """원천 attempt_1 폴더 → 링크 (실물 = 옆 사본) — 원천 폴더 링크."""
    f1 = Path(atts[0][0])
    real = f1.parent / 'attempt_1_real'
    shutil.move(str(f1), str(real))
    os.symlink(str(real), str(f1))


rows = [
    ('V01_R1_codex', ed(mism, T.rr4_r1)),
    ('V02_R1_copied_from_True', ed(mism, r1_bool)),
    ('V03_R1_det_assumed', ed(mism, r1_det_assumed)),
    ('V04_R2_codex', ed(mism, T.rr4_r2)),
    ('V05_R2_order_swap', ed(mism, r2_swap)),
    ('V06_new_run_extra_copied_from', ed(mism, extra_new_copied_from)),
    ('V07_dup_copy_record', ed(okc, dup_copy)),
    ('V08_attempt_resume_of_True', ed(okc, att={'resume_of': True})),
    ('V09_attempt_machine_other', ed(okc, att={'machine': 'gabia'})),
    ('V10_from_str', ed(okc, from_str)),
    ('V11_from_float', ed(okc, from_float)),
    ('V12_chain3_copied_from_1', ed(three, copied_from_other)),
    ('V13_chain3_rebind_codex', ed(lambda t: T.rr4_three(t, 'source-ceiling'), T.rr4_rebind)),
    ('V14_disk_end_only_differs', ed(okc, disk=disk_end_byte)),
    ('V15_disk_copy_payload', ed(okc, disk=disk_copy_payload)),
    ('V16_src_symlink', ed(okc, disk=disk_src_symlink)),
    ('V17_attempt_null_codex', ed(mism, T.rr4_null, att={'resume_of': None})),
    ('V18_attempt_only_null', ed(okc, att={'resume_of': None})),
]
res = {}
for nm, mk in rows:
    o = h.three(nm, mk)
    o['accepted_all_three'] = h.accepted(o)
    res[nm] = o
h.dump(Path(__file__).resolve().parent.parent / 'out' / 'p5_variants.json', res)
for k, v in res.items():
    w, p, c = v['writer'], v['places'], v['cli']
    print(k, 'ACCEPTED' if v['accepted_all_three'] else 'rejected', '| w', (w[0], w[1][0]) if isinstance(w, list) else w,
          '| order', p[1] if isinstance(p, list) else p, '| chain', p[2] if isinstance(p, list) else '', '| cli', c[:3] if isinstance(c, list) else c)
