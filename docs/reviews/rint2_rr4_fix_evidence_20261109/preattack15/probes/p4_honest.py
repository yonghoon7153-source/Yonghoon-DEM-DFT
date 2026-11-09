# -*- coding: utf-8 -*-
"""P4 — 보장 4 (정직 흐름 거짓 거부 없음) — 시험에 없는 정직 꼴 (생산자 = 실제 `ResumeRunner.run` · `_copy` · 새 런 = 가짜 `_execute` · read_run 가짜):
  H1 4 시도 사슬 (1 → 2 → 3 → 4 · from = 그 시점 사슬 끝)
  H2 원천 원 시도가 L02 를 시작조차 안 함 (런 전 TIME_LIMIT · launch 없음) → 재실행 2 (L02 새로 · 남은 payload 없음 = assumed)
  H3 3 런 재실행: 시도 2 = L01 복사 · L02 재실행 (대조 같음) · L03 새 런 rc 1 (자원) → 시도 3 = L01 · L02 복사 (copied_from 2 · L02 = 시도 2 의 새 런) · L03 재실행
  H4 재실행의 재실행에서 원천 (시도 2) 의 L02 = 재실행 런 끝남 · 대조 같음 · 다음 L03 런 전 TIME_LIMIT → 시도 3 = L01 · L02 복사 · L03 새로 (원천에 L03 launch 없음)
  H5 원천 L02 끝 rc 성공 아님 (rc 1 = 자원) + 재실행 2 의 L02 도 rc 1 (재실행 런 자체 멈춤) — 시험 P5 꼴의 3 런 판
각 꼴 → 세 자리 (결과 줄 쓰기 직접 · 실제 recover CLI · 차례 · 사슬) 기대 = 자격 True · 통과."""
import contextlib
import copy
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import h  # noqa: E402

T, RR = h.T, h.RR


def first_custom(base, specs, code, run):
    """원 시도 attempt_1 — specs = [(i, text, rc)] 런 파일 (rr4_files) · 멈춤 code · run."""
    f1 = T.rr4_att(Path(base) / 'attempt_1', 1, None)
    runs = [T.rr4_files(f1, i, text, rc=rc, log=('MemoryError synthetic\n' if rc else 'synthetic fixture\n')) for i, text, rc in specs]
    return f1, T.rr4_put(f1, T.rr4_summ(code, run, runs))


def resume3(src, dst, n, src_n, plan):
    """재실행 시도 (런 1..3 차례 · 실제 ResumeRunner.run) — plan = {i: (text, rc)} 새로 도는 런의 결과 (rc ≠ 0 = RUNNER_RC 자원) · 다 돌면 다음 런 L04 없음 =
    런 셋 끝에 멈춤 없음 → 요약 = 멈춤 TIME_LIMIT L04 꼴 대신 마지막 멈춤 그대로 (끝까지 = completed 꼴 아님 · 시험 꼴과 같게 다음 이름 'L04_x' 런 전 TIME_LIMIT)."""
    dst = T.rr4_att(Path(dst), n, 1)
    rn = RR.ResumeRunner('UNUSED', src, dst, {}, None, 0, {}, parent_env={}, prefix='L', src=src, src_n=src_n, machine=h.MACH)
    rn.env_delta = lambda *_a: {}
    cur = {'i': None}

    def fake_execute(name, q, od, delta):
        i = cur['i']
        text, rc = plan[i]
        rec = T.rr4_files(dst, i, text, rc=rc, log='MemoryError synthetic\n' if rc else 'synthetic fixture\n')
        rn.records.append(rec)
        if rc:
            raise RR.Stop('RUNNER_RC', f'rc {rc} (시험)', name)
        return []

    def fake_read(outdir, req, *_a, **_k):
        return [dict(T.rr4_pub((Path(outdir) / T.RR4_FN).read_bytes()), sigma=1.0, dsigma_rel=0.0)]
    rn._execute = fake_execute
    code, run = 'TIME_LIMIT', 'L04_next'
    with T.rc_patch(read_run=fake_read), contextlib.redirect_stdout(io.StringIO()):
        try:
            for i in (1, 2, 3):
                cur['i'] = i
                role, rj = T.RR4_ROLES[i - 1]
                rn.run(T.SBE_KIT, role, 'P0', None, rj, 1)
        except RR.Stop as e:
            code, run = e.code, e.run
    return dst, T.rr4_put(dst, T.rr4_summ(code, run, copy.deepcopy(rn.records), copy.deepcopy(rn.resume)))


def H1(tag):
    base = Path(T.TD) / 'rr4' / tag
    a1 = T.rr4_first(base)
    a2 = T.rr4_resume(a1[0], base / 'attempt_2', 2, 1, 'c2', rc=1)
    a3 = T.rr4_resume(a2[0], base / 'attempt_3', 3, 2, 'c3', rc=1)
    a4 = T.rr4_resume(a3[0], base / 'attempt_4', 4, 3, 'c3')            # 원천 3 의 남은 payload 'c3' 와 같음 → 대조 같음 · 다음 L03 런 전 TIME_LIMIT
    return [a1, a2, a3, a4]


def H2(tag):
    base = Path(T.TD) / 'rr4' / tag
    a1 = first_custom(base, [(1, 'floor', 0)], 'TIME_LIMIT', h.N2)        # L02 런 전 시간 상한 (흔적 없음)
    return [a1, T.rr4_resume(a1[0], base / 'attempt_2', 2, 1, 'any-ceiling')]


def H3(tag):
    base = Path(T.TD) / 'rr4' / tag
    a1 = T.rr4_first(base)                                               # L01 끝 · L02 rc 1 (자원 · 남은 payload 'source-ceiling')
    a2 = resume3(a1[0], base / 'attempt_2', 2, 1, {2: ('source-ceiling', 0), 3: ('p3', 1)})
    a3 = resume3(a2[0], base / 'attempt_3', 3, 2, {3: ('p3', 0)})
    return [a1, a2, a3]


def H4(tag):
    base = Path(T.TD) / 'rr4' / tag
    a1 = T.rr4_first(base)
    a2 = T.rr4_resume(a1[0], base / 'attempt_2', 2, 1, 'source-ceiling')   # 대조 같음 · L03 런 전 TIME_LIMIT
    a3 = resume3(a2[0], base / 'attempt_3', 3, 2, {3: ('p3', 0)})
    return [a1, a2, a3]


def H5(tag):
    base = Path(T.TD) / 'rr4' / tag
    a1 = T.rr4_first(base)
    a2 = resume3(a1[0], base / 'attempt_2', 2, 1, {2: ('p2-again', 1)})      # 재실행 런 자체 rc 1 (대조 전 멈춤)
    a3 = resume3(a2[0], base / 'attempt_3', 3, 2, {2: ('p2-again', 0), 3: ('p3', 0)})
    return [a1, a2, a3]


res = {}
for nm, mk in (('H1_chain4', H1), ('H2_src_no_launch', H2), ('H3_three_runs', H3), ('H4_chain3_after_compare', H4), ('H5_rerun_self_stop', H5)):
    o = h.three(nm, mk)
    o['accepted_all_three'] = h.accepted(o)
    sm = mk(nm + '_shape')
    o['last_summary_shape'] = {'stop': sm[-1][1]['stop'], 'resume': sm[-1][1]['resume'],
                               'runs': [(r['name'], r.get('copied_from'), r.get('rc')) for r in sm[-1][1]['runs']]}
    res[nm] = o
h.dump(Path(__file__).resolve().parent.parent / 'out' / 'p4_honest.json', res)
print(json.dumps({k: {'acc': v['accepted_all_three'], 'w': v['writer'], 'p': v['places'], 'c': v['cli'], 'shape': v['last_summary_shape']}
                  for k, v in res.items()}, ensure_ascii=False, indent=1)[:6000])
