def _muted(fns, run):
    """시험 함수들을 조용히 돌려 (단언 이름, 결과) 목록을 모은다 — 함수가 예외로 죽으면 그것도 실패 단언 하나."""
    _MUTE.append([])
    err = None
    try:
        for f in run:
            try:
                quiet(fns[f])
            except Exception as e:                          # noqa: BLE001 — 변이가 시험을 죽여도 적발이다
                err = f'{type(e).__name__}: {e}'
                _MUTE[-1].append((f'{f}: 예외', False))
    finally:
        res = _MUTE.pop()
    return res, err


@case('T18 변이 시험 — 증서 · 계약 구현 한 줄을 틀리게 하면 시험이 옳은 이유로 실패한다 (변이 표 · 원 모듈로 되돌림 · 기준선 통과 단언만 센다)')
def t18():
    global CC, RC
    fns = {'t1': t1, 't3': t3, 't6': t6, 't7': t7, 't13': t13, 't16': t16}
    #  기준선 — 변이 없이 같은 시험.  변이에서 실패한 단언 중 **기준선에서 통과한** 것만 적발 근거로 센다 (원래 실패하는 단언으로 적발을
    #  꾸미지 않는다 · 같은 이름이 여럿이면 전부 통과해야 통과로 친다).
    base_res, base_err = _muted(fns, sorted({f for m in MUTANTS for f in m[4]}))
    base_pass = {}
    for n, c in base_res:
        base_pass[n] = base_pass.get(n, True) and c
    base_fail = [n for n, v in base_pass.items() if not v]
    chk(f'T18 기준선 — 변이 없이 돌린 단언 {len(base_res)} 개 전부 통과 (예외 없음)', not base_fail and base_err is None,
        (base_fail[:4], base_err))
    table = []
    for nm, mod, old, new, run, want in MUTANTS:
        orig_cc, orig_rc = CC, RC
        saved = sys.modules.get(mod)
        try:
            m = _mutant(mod, old, new)
        except Exception as e:                              # noqa: BLE001
            chk(f'T18 [{nm}] 변이 만들기', False, f'{type(e).__name__}: {e}')
            continue
        sys.modules[mod] = m
        if mod == 'step3_conv_cert':
            CC = m
        else:
            RC = m
        try:
            res, err = _muted(fns, run)
        finally:
            CC, RC = orig_cc, orig_rc
            if saved is None:
                sys.modules.pop(mod, None)
            else:
                sys.modules[mod] = saved
        failed = [n for n, c in res if not c]
        right = [n for n in failed if base_pass.get(n) is True and any(n.startswith(w) for w in want)]
        table.append((nm, len(res), len(failed), len(right), right[:2]))
        chk(f'T18 [{nm}] 적발 — 실패 {len(failed)}/{len(res)} · 옳은 이유 (기준선에서 통과한 기대 시험 {want} 가 실패) {len(right)} · {right[:2]}',
            bool(right), (failed[:4], err))
    print('    변이 표 (이름 · 돌린 단언 · 실패 · 옳은 이유 (기준선 통과 → 변이 실패) 수 · 예):')
    for row in table:
        print(f'      {row[0]:40s} {row[1]:4d} {row[2]:4d} {row[3]:4d}  {row[4]}')
    chk('T18 되돌림 — 변이 뒤 시험 모듈이 원 모듈 (sys.modules · 전역 CC · RC)', CC is sys.modules.get('step3_conv_cert')
        and RC is sys.modules.get('run_contract') and not hasattr(CC, '__mutant__'), (CC, RC))
