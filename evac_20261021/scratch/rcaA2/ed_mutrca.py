p = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee/scripts/test_carbon_junction.py'
s = open(p, encoding='utf-8').read()


def rep(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:80])
    s = s.replace(old, new)


rep('''    def cf_nodrop(self, solve_, I_full, request):           # 변이 — 반사실이 SV 면을 끊지 않는다
        orig = self._assemble
        self._assemble = lambda *a, **k: orig(*a, **dict(k, drop_cat=None))
        try:
            return real_cf(self, solve_, I_full, request)
        finally:
            del self._assemble''',
    '''    def cf_nodrop(self, solve_, I_full, request, certify=None):   # 변이 — 반사실이 SV 면을 끊지 않는다 (★ 10-21 PRE-impl-09 — 생산 호출
        orig = self._assemble                                       #  서명 그대로 (certify=) · 옛 변이는 TypeError 로만 '잡혔다')
        self._assemble = lambda *a, **k: orig(*a, **dict(k, counterfactual=False))
        try:
            return real_cf(self, solve_, I_full, request, certify=certify)
        finally:
            del self._assemble''')
rep('''    for nm, ctx, check in cases:
        b = bool(check())
        try:
            with ctx:
                c = not bool(check())
        except AttributeError as e:                         # 훅 없음 (고치기 전 판) = 변이를 못 끼움 = 실패로 센다
            c = None
            print(f'    MUT-RCA {nm}: {e}')
        chk(f'MUT-RCA {nm} (변이 전 통과 · 변이 실패)', b and c is True, f'base {b} caught {c}')''',
    '''    for nm, ctx, check in cases:
        #  ★ 10-21 (PRE-impl-09) — 변이 안에서 난 예외 (`_try` 가 삼킨 것 포함) = 하네스 실패 (잡힘 아님 · T18 '기준선 통과 단언만' 과 같게) ·
        #    기준선 검사도 예외 없이 통과해야 한다
        _TRY_EXC[0] = 0
        b = bool(check())
        e0 = _TRY_EXC[0]
        c, why = None, ''
        try:
            with ctx:
                _TRY_EXC[0] = 0
                c = not bool(check())
                if _TRY_EXC[0]:
                    c, why = None, f'변이 안 예외 {_TRY_EXC[0]} 건 = 하네스 실패 (옳은 이유 아님)'
        except Exception as e:                              # noqa: BLE001 — 훅 없음 (고치기 전 판) · 변이 예외 = 하네스 실패
            c, why = None, f'{type(e).__name__}: {e}'
        if why:
            print(f'    MUT-RCA {nm}: {why}')
        chk(f'MUT-RCA {nm} (변이 전 통과 · 변이 실패 · 예외 없음)', b and e0 == 0 and c is True, f'base {b} (예외 {e0}) caught {c} {why}')''')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
