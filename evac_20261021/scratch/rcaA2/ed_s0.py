p = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee/scripts/test_ca_s0_census.py'
s = open(p, encoding='utf-8').read()


def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)


rep('''      정준 바이트 · sha256 · 손댄 계획 거부 · 개정 커밋 대조 (임시 git 저장소: 통과 · 없음 · 조상 아님 · 해시 없음 ·
      계획 없음 · 전각 sha)''',
    '''      정준 바이트 · sha256 · 손댄 계획 거부 · 개정 커밋 대조 (임시 git 저장소: 통과 · 없음 · 조상 아님 · 해시 없음 ·
      계획 없음 · 전각 sha) · ★ 10-21 (사전 리뷰 PRE-design-04) 단계 2 관문 = 같은 커밋의 두 줄 (`| S0 계획 해시 |` 끝 칸 = S0 계획 ·
      `| 계획 해시 |` 끝 칸 = R 런 사슬 계획 · ⬜ = 거부) · R 런 계획 파일 (`--r-plan-path`) sha256 = 그 줄 · 꼴 (`rint_r_chain.load_plan`) ·
      tol_ff_um = S0 values_um.tol_ff · len_law = 이 코드의 법칙 · s_min 등록 (숫자)''')

rep('''def make_plan_repo(d, plan_bytes, plan_sha, *, put_hash=True, put_plan=True):
    """임시 git 저장소 — R 문서 (계획 해시 줄) + 계획 파일을 한 커밋에.  → (repo, sha, plan_rel, r_doc_rel)."""
    repo = os.path.join(d, 'repo')
    os.makedirs(os.path.join(repo, 'docs', 'reviews'))
    os.makedirs(os.path.join(repo, 'docs', 'data', 's0'))
    _git(repo, 'init', '-q')
    r_rel = 'docs/reviews/R.md'; p_rel = 'docs/data/s0/cjunc_plan.json'
    with open(os.path.join(repo, 'README'), 'w') as f:
        f.write('base\\n')
    _git(repo, 'add', '-A'); _git(repo, 'commit', '-qm', 'base')
    with open(os.path.join(repo, r_rel), 'w', encoding='utf-8') as f:
        f.write('# R §2-1 개정\\n' + (f'| 계획 해시 | `CJUNC_PLAN` sha256 | {plan_sha} |\\n' if put_hash else '(해시 없음)\\n'))
    if put_plan:
        with open(os.path.join(repo, p_rel), 'wb') as f:
            f.write(plan_bytes)
    _git(repo, 'add', '-A'); _git(repo, 'commit', '-qm', 'R 2-1 revision')
    return repo, _git(repo, 'rev-parse', 'HEAD'), p_rel, r_rel''',
    '''R_PLAN_REL = 'docs/data/s0/rint_r_plan.json'     # ★ 10-21 (PRE-design-04) — R 런 사슬 계획 (rint-r-plan-v1) 파일 (같은 개정 커밋)


def r_plan_bytes(tol_ff, **over):
    """R 런 사슬 계획 (`rint_r_chain.load_plan` 꼴 · 칸 일곱) 바이트 — tol_ff_um = S0 계획 values_um.tol_ff (등록 R §2-1 두 계획 대조)."""
    import carbon_junction as _cj
    obj = {'schema': 'rint-r-plan-v1', 'len_law': _cj.CJUNC_LEN_LAW, 'unreg_law': 'cut', 's_min_um': 0.6,
           'tol_ff_um': float(tol_ff), 'step3_rtol': 1e-12, 'p2_extra': ''}
    obj.update(over)
    return (json.dumps(obj, sort_keys=True) + '\\n').encode('utf-8')


def make_plan_repo(d, plan_bytes, plan_sha, *, put_hash=True, put_plan=True, r_plan=None, r_row='auto', s0_row='auto',
                   extra_doc=''):
    """임시 git 저장소 — R 문서 (계획 해시 줄 둘) + 계획 파일 둘을 한 커밋에.  → (repo, sha, plan_rel, r_doc_rel).
    ★ 10-21 (PRE-design-04) — 등록 R §2-1 의 두 줄: `| 계획 해시 |` (R 런 사슬 계획 · 끝 칸) · `| S0 계획 해시 |` (S0 단계 1 계획 · 끝 칸).
    put_hash False = S0 줄 없음 · r_row None = R 줄 없음 · 'auto' = 파일의 sha256 · 문자열 = 그 값 (⬜ 포함) · r_plan = R 런 계획 바이트
    (None = 기본 꼴 · tol_ff = S0 계획 값 · False = 파일 없음) · extra_doc = 문서 끝에 덧붙일 줄 (S0 해시를 줄 밖에 두는 반례)."""
    repo = os.path.join(d, 'repo')
    os.makedirs(os.path.join(repo, 'docs', 'reviews'))
    os.makedirs(os.path.join(repo, 'docs', 'data', 's0'))
    _git(repo, 'init', '-q')
    r_rel = 'docs/reviews/R.md'; p_rel = 'docs/data/s0/cjunc_plan.json'
    with open(os.path.join(repo, 'README'), 'w') as f:
        f.write('base\\n')
    _git(repo, 'add', '-A'); _git(repo, 'commit', '-qm', 'base')
    if r_plan is None:
        try:
            tol = json.loads(plan_bytes.decode('ascii'))['values_um']['tol_ff']
        except Exception:                                    # noqa: BLE001 — 깨진 S0 계획 반례 = 아무 숫자
            tol = 0.075
        r_plan = r_plan_bytes(tol)
    r_sha = hashlib.sha256(r_plan).hexdigest() if r_plan else '⬜'
    doc = '# R §2-1 개정\\n'
    if r_row is not None:
        doc += f'| 계획 해시 | R 런 사슬 계획 (rint-r-plan-v1) sha256 | {r_sha if r_row == "auto" else r_row} |\\n'
    if put_hash:
        doc += f'| S0 계획 해시 | S0 단계 1 계획 (ca-cjunc-plan-v1) sha256 | {plan_sha if s0_row == "auto" else s0_row} |\\n'
    else:
        doc += '(해시 없음)\\n'
    doc += extra_doc
    with open(os.path.join(repo, r_rel), 'w', encoding='utf-8') as f:
        f.write(doc)
    if put_plan:
        with open(os.path.join(repo, p_rel), 'wb') as f:
            f.write(plan_bytes)
    if r_plan:
        with open(os.path.join(repo, R_PLAN_REL), 'wb') as f:
            f.write(r_plan)
    _git(repo, 'add', '-A'); _git(repo, 'commit', '-qm', 'R 2-1 revision')
    return repo, _git(repo, 'rev-parse', 'HEAD'), p_rel, r_rel


def _has_kw(fn, name):
    import inspect
    try:
        return name in inspect.signature(fn).parameters
    except (TypeError, ValueError):
        return False


def _vpc(repo, sha, prel, rrel, rp=R_PLAN_REL):
    """단계 2 관문 — ★ 10-21 (PRE-design-04) R 런 계획 경로를 넘긴다 (고치기 전 판 = 인자 없음 → 그 키만 빼고 부른다: 반례가
    그 판에서 **통과** 하는 것 = 옳은 이유의 실패)."""
    if _has_kw(S0.verify_plan_commit, 'r_plan_path'):
        return S0.verify_plan_commit(repo, sha, prel, r_doc=rrel, r_plan_path=rp)
    return S0.verify_plan_commit(repo, sha, prel, r_doc=rrel)


def _s2kw(rp=R_PLAN_REL):
    return {'r_plan_path': rp} if _has_kw(S0.run_stage, 'r_plan_path') else {}''')

rep('''def t_plan_commit():
    p, b, h = S0.make_plan(0.15, R_F, 2.0, _src())
    with tempfile.TemporaryDirectory() as d:
        repo, sha, prel, rrel = make_plan_repo(d, b, h)
        ok = S0.verify_plan_commit(repo, sha, prel, r_doc=rrel)
        chk('L3a 개정 커밋 · 계획 · 해시 일치 → 통과 (계획 · sha256 · 전체 sha)',
            ok[1] == h and ok[0]['values_um'] == p['values_um'] and ok[2] == sha)
        chk('L3b 없는 커밋 거부', raises(lambda: S0.verify_plan_commit(repo, 'deadbeef' * 5, prel, r_doc=rrel),
                                          S0.S0Error))
        chk('L3c 전각 · 비 ASCII sha 거부', raises(lambda: S0.verify_plan_commit(repo, '０' * 40, prel, r_doc=rrel),
                                                  S0.S0Error))
        chk('L3d 계획 경로 없음 거부', raises(lambda: S0.verify_plan_commit(repo, sha, 'docs/none.json', r_doc=rrel),
                                            S0.S0Error))''',
    '''def t_plan_commit():
    p, b, h = S0.make_plan(0.15, R_F, 2.0, _src())
    with tempfile.TemporaryDirectory() as d:
        repo, sha, prel, rrel = make_plan_repo(d, b, h)
        ok = _vpc(repo, sha, prel, rrel)
        chk('L3a 개정 커밋 · 계획 · 해시 일치 → 통과 (계획 · sha256 · 전체 sha)',
            ok[1] == h and ok[0]['values_um'] == p['values_um'] and ok[2] == sha)
        rb = r_plan_bytes(p['values_um']['tol_ff'])
        ri = ok[3] if len(ok) > 3 else None
        chk('L3a2 ★ R 런 계획 결합 기록 — 경로 · sha256 (= 같은 커밋의 `| 계획 해시 |` 끝 칸) · s_min · tol_ff (= S0 tol_ff) · 법칙',
            isinstance(ri, dict) and ri.get('path') == R_PLAN_REL and ri.get('sha256') == hashlib.sha256(rb).hexdigest()
            and ri.get('s_min_um') == 0.6 and ri.get('tol_ff_um') == p['values_um']['tol_ff']
            and ri.get('len_law') == 'len_scaled_v0', str(ri))
        chk('L3b 없는 커밋 거부', raises(lambda: _vpc(repo, 'deadbeef' * 5, prel, rrel), S0.S0Error))
        chk('L3c 전각 · 비 ASCII sha 거부', raises(lambda: _vpc(repo, '０' * 40, prel, rrel), S0.S0Error))
        chk('L3d 계획 경로 없음 거부', raises(lambda: _vpc(repo, sha, 'docs/none.json', rrel), S0.S0Error))''')

rep('''        chk('L3e HEAD 의 조상 아닌 커밋 거부 (가지 밖)',
            raises(lambda: S0.verify_plan_commit(repo, sha, prel, r_doc=rrel), S0.S0Error))
    with tempfile.TemporaryDirectory() as d:
        repo, sha, prel, rrel = make_plan_repo(d, b, h, put_hash=False)
        chk('L3f R 문서에 계획 해시 없음 거부', raises(lambda: S0.verify_plan_commit(repo, sha, prel, r_doc=rrel),
                                                    S0.S0Error))
    with tempfile.TemporaryDirectory() as d:
        bb = b.replace(b'"gap_tol":2.0', b'"gap_tol":2.5')
        repo, sha, prel, rrel = make_plan_repo(d, bb, hashlib.sha256(bb).hexdigest())
        chk('L3g 커밋 안 계획이 식 어긋남 (손댐) → 거부', raises(lambda: S0.verify_plan_commit(repo, sha, prel, r_doc=rrel),
                                                         S0.S0Error))''',
    '''        chk('L3e HEAD 의 조상 아닌 커밋 거부 (가지 밖)', raises(lambda: _vpc(repo, sha, prel, rrel), S0.S0Error))
    with tempfile.TemporaryDirectory() as d:
        repo, sha, prel, rrel = make_plan_repo(d, b, h, put_hash=False)
        chk('L3f R 문서에 계획 해시 없음 거부', raises(lambda: _vpc(repo, sha, prel, rrel), S0.S0Error))
    with tempfile.TemporaryDirectory() as d:
        bb = b.replace(b'"gap_tol":2.0', b'"gap_tol":2.5')
        repo, sha, prel, rrel = make_plan_repo(d, bb, hashlib.sha256(bb).hexdigest())
        chk('L3g 커밋 안 계획이 식 어긋남 (손댐) → 거부', raises(lambda: _vpc(repo, sha, prel, rrel), S0.S0Error))
    #  ★ 10-21 (사전 리뷰 PRE-design-04 · 등록 R §2-1 · §2-1b · §11 ④) — 단계 2 관문 = 같은 개정 커밋의 두 계획 · 두 줄.  반례 (버림 저장소 ·
    #    탐침 probe_stage2_gate 꼴): 옛 관문은 S0 해시가 문서 **어디에든** 있으면 통과 (`h in 문서`) · R 런 계획 줄 · s_min 을 안 봤다.
    tol = p['values_um']['tol_ff']
    neg = (
        ('L3h S0 해시가 `| S0 계획 해시 |` 줄 밖 (산문 줄) · 그 줄 = ⬜ → 거부', dict(s0_row='⬜', extra_doc=f'(참고: {h})\\n')),
        ('L3i R 런 계획 줄 (`| 계획 해시 |`) = ⬜ (s_min 미등록 · 탐침 꼴) → 거부', dict(r_row='⬜')),
        ('L3j R 런 계획 줄 없음 → 거부', dict(r_row=None)),
        ('L3k R 런 계획 줄 = 64 hex 인데 파일 sha256 와 다름 → 거부', dict(r_row='0' * 64)),
        ('L3l R 런 계획 파일 없음 (줄만) → 거부', dict(r_plan=False, r_row='1' * 64)),
        ('L3m R 런 계획 tol_ff_um ≠ S0 values_um.tol_ff (두 계획 대조) → 거부', dict(r_plan=r_plan_bytes(tol * 0.5))),
        ('L3n R 런 계획 s_min_um = null (미등록 숫자) → 거부', dict(r_plan=r_plan_bytes(tol, s_min_um=None))),
        ('L3o R 런 계획 len_law ≠ 이 코드의 길이 법칙 → 거부', dict(r_plan=r_plan_bytes(tol, len_law='len_scaled_v9'))),
        ('L3p R 런 계획 꼴 틀림 (칸 하나 더) → 거부', dict(r_plan=r_plan_bytes(tol, extra_key=1))),
        ('L3q `| 계획 해시 |` 줄 둘 → 거부', dict(extra_doc='| 계획 해시 | 다른 줄 | ' + 'a' * 64 + ' |\\n')),
        ('L3r `| S0 계획 해시 |` 줄 둘 → 거부', dict(extra_doc=f'| S0 계획 해시 | 다른 줄 | {h} |\\n')),
    )
    for nm, kw in neg:
        with tempfile.TemporaryDirectory() as d:
            repo, sha, prel, rrel = make_plan_repo(d, b, h, **kw)
            chk(nm, raises(lambda: _vpc(repo, sha, prel, rrel), S0.S0Error))
    with tempfile.TemporaryDirectory() as d:
        repo, sha, prel, rrel = make_plan_repo(d, b, h)
        chk('L3s R 런 계획 경로 = 리포 상대 ASCII (절대 · .. · 공백 = 거부)',
            all(raises(lambda q=q: _vpc(repo, sha, prel, rrel, rp=q), S0.S0Error)
                for q in ('/abs/plan.json', '../plan.json', 'docs/a b.json')))
        out = os.path.join(d, 'out_s2')
        try:
            S0.run_stage(2, [os.path.join(d, 'no_kit')], out, threshold_commit=sha, plan_path=prel, repo=repo, r_doc=rrel)
            why = 'no error'
        except S0.S0Error as e:
            why = str(e)
        except Exception as e:                                # noqa: BLE001
            why = f'{type(e).__name__}: {e}'
        chk('L3t 단계 2 · --r-plan-path 없음 → 관문에서 거부 (킷을 보기 전 · 사유에 r-plan-path)', 'r-plan-path' in why, why)
        import contextlib
        import io
        er = io.StringIO()
        try:
            with contextlib.redirect_stderr(er), contextlib.redirect_stdout(io.StringIO()):
                rc = S0.main(['--stage', '2', '--kit', os.path.join(d, 'no_kit'), '--out', os.path.join(d, 'out_cli'),
                              '--threshold-commit', sha, '--plan-path', prel, '--r-plan-path', R_PLAN_REL, '--r-doc', rrel,
                              '--repo', repo])
        except SystemExit as e:
            rc = f'SystemExit {e.code}'
        chk('L3u CLI --r-plan-path 받음 — 관문 통과 뒤 킷 없음으로 rc 2 (인자 오류 아님)',
            rc == 2 and 'r-plan-path' not in er.getvalue() and 'unrecognized' not in er.getvalue(), f'{rc} {er.getvalue()[-200:]}')''')

rep('''    repo, sha, prel, rrel = make_plan_repo(os.path.join(tmp, 'g'), planA, h)
    out = os.path.join(tmp, 'outB2')
    _stage(2, [STATE['kitB']], out, threshold_commit=sha, plan_path=prel, repo=repo, r_doc=rrel)
    rep = _load(os.path.join(out, 's0_stage2_kit_B.json'))
    STATE['repB'] = rep
    chk('E7a 단계 2 — 계획 = 커밋에서 (sha · 해시)', rep['plan']['source'] == f'commit:{sha}' and rep['plan']['sha256'] == h)''',
    '''    repo, sha, prel, rrel = make_plan_repo(os.path.join(tmp, 'g'), planA, h)
    out = os.path.join(tmp, 'outB2')
    _stage(2, [STATE['kitB']], out, threshold_commit=sha, plan_path=prel, repo=repo, r_doc=rrel, **_s2kw())
    rep = _load(os.path.join(out, 's0_stage2_kit_B.json'))
    STATE['repB'] = rep
    chk('E7a 단계 2 — 계획 = 커밋에서 (sha · 해시)', rep['plan']['source'] == f'commit:{sha}' and rep['plan']['sha256'] == h)
    rpb = r_plan_bytes(json.loads(planA.decode('ascii'))['values_um']['tol_ff'])
    rpr = (rep.get('plan') or {}).get('r_plan') or {}
    chk('E7a2 ★ 단계 2 보고 — R 런 계획 결합 (경로 · sha256 = 커밋의 `| 계획 해시 |` · s_min 봉인 · tol_ff = S0 tol_ff)',
        rpr.get('path') == R_PLAN_REL and rpr.get('sha256') == hashlib.sha256(rpb).hexdigest() and rpr.get('s_min_um') == 0.6
        and rpr.get('tol_ff_um') == json.loads(planA.decode('ascii'))['values_um']['tol_ff'], str(rpr))''')

rep('''    out = os.path.join(tmp, 'outBP')
    _stage(2, [kitP], out, threshold_commit=sha, plan_path=prel, repo=repo, r_doc=rrel)''',
    '''    out = os.path.join(tmp, 'outBP')
    _stage(2, [kitP], out, threshold_commit=sha, plan_path=prel, repo=repo, r_doc=rrel, **_s2kw())''')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
