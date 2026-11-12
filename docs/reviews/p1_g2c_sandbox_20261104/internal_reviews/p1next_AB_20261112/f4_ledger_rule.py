#!/usr/bin/env python3
"""P1 G2c' 초안 B 4 회차 고침 (PFA2-01) — §8 분류표 손 반례 (내부 · Codex 아님 · 11-12 밤 · 작은 산술만).

분류표 (B §8 · 결과 전 · sacct 잡마다 한 행):
  Start 없음 (Unknown/None) ∧ State CANCELLED ∧ 그 잡 장부 줄 없음     → 셈 밖 (시작 안 함)
  ExitCode 3:0 ∧ 그 잡 attempt 줄 없음 (prestop 줄 있으면 np = 잡 NP) → 셈 밖 (사전 멈춤 · 러너 전 멈춤)
  Start 있음 ∧ ExitCode ≠ 3:0 ∧ attempt 줄 하나                         → 시도 (n 40000 = 셈 · n 200 = 건식)
  그 밖 (sacct 에 없는 장부 줄 · 꼴 밖 · attempt 둘 · PENDING/RUNNING …) → 어긋남 → 그 NP 결론 없음
쓰는 법: python3 -I f4_ledger_rule.py
"""
NP_OF = {'g2cp_mpi2': 2, 'g2cp_mpi4': 4}


def classify(job, ledger):
    jid, name, start, exitc = job[:4]
    state = job[4] if len(job) > 4 else ('CANCELLED' if start is None else 'COMPLETED')
    mine = [l for l in ledger if l['slurm_job'] == jid]
    att = [l for l in mine if l['kind'] == 'attempt']
    pre = [l for l in mine if l['kind'] == 'prestop']
    bad = [l for l in mine if l['kind'] not in ('attempt', 'prestop')]
    if bad or len(att) > 1 or len(pre) > 1 or (att and pre):
        return '어긋남'
    if state in ('PENDING', 'RUNNING'):
        return '어긋남'           # 돌려받기 = 그 이름의 잡이 다 끝난 뒤
    if start is None:
        return '셈 밖 (시작 안 함)' if (not mine and state == 'CANCELLED') else '어긋남'
    if exitc == '3:0':
        if att:
            return '어긋남'
        if pre and pre[0]['np'] != NP_OF[name]:
            return '어긋남'
        return '셈 밖 (사전 멈춤)'
    if pre:
        return '어긋남'           # 손으로 만든 셈 밖 표지 꼴 (돈 잡에 prestop)
    if len(att) == 1:
        a = att[0]
        if a['np'] != NP_OF[name]:
            return '어긋남'
        return '시도' if a['n'] == 40000 else '건식'
    return '어긋남'               # attempt 줄 없이 돈 잡


def verdict(sacct, ledger, returned):
    cls = {j[0]: classify(j, ledger) for j in sacct}
    orphan = [l for l in ledger if l['slurm_job'] not in cls]   # sacct 에 없는 장부 줄
    unret = [l['slurm_job'] for l in ledger if l['kind'] == 'attempt' and l['n'] == 40000 and l['slurm_job'] not in returned]
    ok = not orphan and not unret and all(c != '어긋남' for c in cls.values())
    n_att = sum(c == '시도' for c in cls.values())
    return ('결론 설 수 있음' if ok else '결론 없음 → 1저자'), cls, n_att


def A(jid, np_, n):
    return {'slurm_job': jid, 'kind': 'attempt', 'np': np_, 'n': n}


def P(jid, np_):
    return {'slurm_job': jid, 'kind': 'prestop', 'np': np_}


S = 'start'
cases = [
    # 이름 · sacct (잡 · 이름 · Start · ExitCode) · 장부 · 돌려받은 시도 · 바라는 답
    ('정직 · 건식 사전 멈춤 rc 3 (358667 꼴) → 고쳐 건식 다시 → 샌드박스',
     [('d1', 'g2cp_mpi4', S, '3:0'), ('d2', 'g2cp_mpi4', S, '0:0'), ('s1', 'g2cp_mpi4', S, '0:0')],
     [P('d1', 4), A('d2', 4, 200), A('s1', 4, 40000)], {'s1'}, '결론 설 수 있음'),
    ('정직 · 같은 꼴 · 장부 쓰기 실패로 멈춤 (prestop 줄 없음)',
     [('d1', 'g2cp_mpi4', S, '3:0'), ('s1', 'g2cp_mpi4', S, '0:0')], [A('s1', 4, 40000)], {'s1'}, '결론 설 수 있음'),
    ('정직 · 대기 중 취소 (Start 없음)',
     [('c1', 'g2cp_mpi2', None, '0:0'), ('s1', 'g2cp_mpi2', S, '0:0')], [A('s1', 2, 40000)], {'s1'}, '결론 설 수 있음'),
    ('정직 · 잡 스크립트 러너 전 멈춤 (repo/ 없음 · exit 3)',
     [('x1', 'g2cp_mpi2', S, '3:0'), ('s1', 'g2cp_mpi2', S, '0:0')], [A('s1', 2, 40000)], {'s1'}, '결론 설 수 있음'),
    ('정직 · SLURM_NTASKS ≠ NP 사전 멈춤 (prestop)',
     [('x1', 'g2cp_mpi2', S, '3:0'), ('s1', 'g2cp_mpi2', S, '0:0')], [P('x1', 2), A('s1', 2, 40000)], {'s1'}, '결론 설 수 있음'),
    ('정직 · 시도 뒤 TIMEOUT (기술 실패) → 다시 (시도 2)',
     [('s1', 'g2cp_mpi2', S, '0:0'), ('s2', 'g2cp_mpi2', S, '0:0')], [A('s1', 2, 40000), A('s2', 2, 40000)], {'s1', 's2'}, '결론 설 수 있음'),
    ('바꿈 · 이름 바꾼 잡 (sacct 이름 목록 밖) 에서 N 40000 한 번 더',
     [('s1', 'g2cp_mpi4', S, '0:0')], [A('s1', 4, 40000), A('rn', 4, 40000)], {'s1', 'rn'}, '결론 없음 → 1저자'),
    ('바꿈 · 돈 잡 (ExitCode 0:0) 에 손으로 쓴 prestop 줄 (attempt 줄 바꿔침)',
     [('s1', 'g2cp_mpi4', S, '0:0'), ('s2', 'g2cp_mpi4', S, '0:0')], [P('s1', 4), A('s2', 4, 40000)], {'s2'}, '결론 없음 → 1저자'),
    ('바꿈 · 돈 잡의 attempt 줄만 지움',
     [('s1', 'g2cp_mpi4', S, '0:0'), ('s2', 'g2cp_mpi4', S, '0:0')], [A('s2', 4, 40000)], {'s2'}, '결론 없음 → 1저자'),
    ('바꿈 · 실행기 보장 위반 꼴 (ExitCode 3:0 인데 attempt 줄)',
     [('s1', 'g2cp_mpi4', S, '3:0')], [A('s1', 4, 40000)], {'s1'}, '결론 없음 → 1저자'),
    ('바꿈 · 잡 끝 rc 를 안 넘기는 잡 꼴 (echo 로 끝) + 사전 멈춤 (ExitCode 0:0 · prestop)',
     [('d1', 'g2cp_mpi4', S, '0:0'), ('s1', 'g2cp_mpi4', S, '0:0')], [P('d1', 4), A('s1', 4, 40000)], {'s1'}, '결론 없음 → 1저자'),
    ('바꿈 · Start 없음인데 attempt 줄',
     [('c1', 'g2cp_mpi2', None, '0:0')], [A('c1', 2, 40000)], {'c1'}, '결론 없음 → 1저자'),
    ('바꿈 · 한 잡에 attempt 둘',
     [('s1', 'g2cp_mpi2', S, '0:0')], [A('s1', 2, 40000), A('s1', 2, 40000)], {'s1'}, '결론 없음 → 1저자'),
    ('바꿈 · 장부의 N 40000 시도를 안 돌려받음',
     [('s1', 'g2cp_mpi2', S, '0:0'), ('s2', 'g2cp_mpi2', S, '0:0')], [A('s1', 2, 40000), A('s2', 2, 40000)], {'s2'}, '결론 없음 → 1저자'),
    ('바꿈 · 돌려받을 때 아직 PENDING (Start 없음) 인 잡',
     [('p1', 'g2cp_mpi2', None, '0:0', 'PENDING'), ('s1', 'g2cp_mpi2', S, '0:0')], [A('s1', 2, 40000)], {'s1'}, '결론 없음 → 1저자'),
    ('한정 (fail-closed) · 돌던 잡을 attempt 줄 전에 취소 (CANCELLED 0:15)',
     [('k1', 'g2cp_mpi2', S, '0:15'), ('s1', 'g2cp_mpi2', S, '0:0')], [A('s1', 2, 40000)], {'s1'}, '결론 없음 → 1저자'),
]
print('[L4] B §8 분류표 손 반례 (글 그대로)')
bad = 0
for lab, sacct, ledger, ret, want in cases:
    got, cls, n_att = verdict(sacct, ledger, ret)
    ok = got == want
    bad += not ok
    print(f'  {"✓" if ok else "✗"} {lab}: {got} · 분류 {cls} · N 40000 시도 {n_att} · 바라는 답 {want}')
# 한정 (막지 않음 · 사전 공격 ⑤ 꼴): 잡 스크립트를 고쳐 러너 뒤 exit 3 + attempt 줄 · OUT 지움 → 규칙상 셈 밖 = 숨음
got, cls, _ = verdict([('s1', 'g2cp_mpi4', S, '3:0'), ('s2', 'g2cp_mpi4', S, '0:0')], [A('s2', 4, 40000)], {'s2'})
print(f'  참고 · 한정 (막지 않음) · 잡 스크립트 고침 (러너 뒤 exit 3) + attempt 줄 · OUT 지움: 규칙 = {got} · 분류 {cls} (SLURM 기록으로 못 가림 · B §8 한정 줄)')
print(f'  어긋난 사례 {bad} / {len(cases)}')
