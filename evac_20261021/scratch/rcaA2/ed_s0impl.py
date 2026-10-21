p = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2/impl/ca_s0_census.py'
s = open(p, encoding='utf-8').read()


def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)


rep('''  단계 2 = DBE 침대들 — `--threshold-commit <개정 커밋>` · `--plan-path <리포 안 계획 경로>` 필수.  도구가 확인: 커밋이
           이 작업 트리 HEAD 의 조상 · 그 커밋의 계획 파일 sha256 이 그 커밋의 등록 R 문서에 있음 · 계획 식 재유도 · 정준 바이트.''',
    '''  단계 2 = DBE 침대들 — `--threshold-commit <개정 커밋>` · `--plan-path <리포 안 계획 경로>` · `--r-plan-path <같은 커밋의 R 런 사슬
           계획>` 필수.  도구가 확인: 커밋이 이 작업 트리 HEAD 의 조상 · 그 커밋 등록 R 문서의 `| S0 계획 해시 |` 줄 (하나) 끝 칸 = 계획
           파일 sha256 · 계획 식 재유도 · 정준 바이트 · ★ 10-21 (사전 리뷰 PRE-design-04 · 등록 R §2-1 · §2-1b · §11 ④) 같은 문서의
           `| 계획 해시 |` 줄 (하나 · 사슬 `rint_r_chain.registration_plan_hash` 그대로 · ⬜ = 거부) = R 런 계획 파일 sha256 · 그 꼴
           (`rint_r_chain.load_plan` — s_min 숫자 등록) · 두 계획 대조 (tol_ff_um = S0 values_um.tol_ff · len_law = 원장의 길이 법칙).''')

rep('''  python3 scripts/ca_s0_census.py --stage 2 --threshold-commit <sha> --plan-path docs/data/<…>/cjunc_plan.json \\\\
          --kit ~/sdcp/kit_DBE_sdcp1um_vgcf100 --kit ~/sdcp/kit_DBE --out ~/sdcp/ca1_s0_dbe''',
    '''  python3 scripts/ca_s0_census.py --stage 2 --threshold-commit <sha> --plan-path docs/data/<…>/cjunc_plan.json \\\\
          --r-plan-path docs/data/<…>/<R 런 계획>.json --kit ~/sdcp/kit_DBE_sdcp1um_vgcf100 --kit ~/sdcp/kit_DBE --out ~/sdcp/ca1_s0_dbe''')

rep('''    '자기 (같은 가닥) 후보의 경로 호 길이 s = 원장 규칙 (두 쪽 셀 조각 최근접점 쌍 · ε 띠 · 띠 안 = 작은 s) — s_min 을 정하는 근거 · '
    's_min 숫자는 등록 R §2-1 개정 (이 도구는 고르지 않는다)',''',
    '''    '자기 (같은 가닥) 후보 = 원장 규칙 (★ 10-21 Q-B: 같은 조각 중심선 쌍 d ≤ D · 바닥 s > D 그리고 s > (π/2)·d · 후보 무리마다 접점 쌍의 '
    '경로 호 길이 s — s_min None 이라 바닥 쌍 전부 · 그 L_c = 바닥 쌍의 닿음 (s_min 이 줄일 수 있다)) — s_min 을 정하는 근거 · s_min 숫자는 '
    '등록 R §2-1 개정 (이 도구는 고르지 않는다) · 같은 fid 의 끊긴 조각 = 서로 다른 섬유 규칙 (자기 후보 아님)',''')

rep('''def verify_plan_commit(repo, sha, plan_path, r_doc=R_DOC_DEFAULT):
    """단계 2 관문 — 개정 커밋이 HEAD 의 조상 · 그 커밋의 계획 파일 sha256 이 그 커밋의 등록 R 문서에 있음 · 식 재유도 · 정준.
    → (계획, sha256, 전체 sha).  커밋 순서만으로는 시점 증명이 안 된다 (v3 판정) → 해시로 묶는다."""
    if not isinstance(sha, str) or not _SHA_RE.match(sha):
        raise S0Error('--threshold-commit 은 ASCII 16진 7–40 자 (전각 · 공백 · 다른 문자 거부)')
    for p in (plan_path, r_doc):
        if (not isinstance(p, str) or not p or os.path.isabs(p) or '..' in p.split('/') or not p.isascii()
                or re.search(r'\\s', p)):
            raise S0Error(f'리포 상대 ASCII 경로여야 한다: {p!r}')''',
    '''def _row_value(text, label):
    """등록 문서의 `| <label> |` 줄 (정확히 하나) 의 끝 칸 (백틱 · 공백 뺌) — 없거나 둘 이상 = S0Error."""
    rows = [ln for ln in text.splitlines() if ln.startswith(f'| {label} |')]
    if len(rows) != 1:
        raise S0Error(f'등록 R 문서의 "| {label} |" 줄이 {len(rows)} 개 (1 이어야)')
    cells = [c.strip() for c in rows[0].strip().strip('|').split('|')]
    return cells[-1].strip('` ')


def verify_plan_commit(repo, sha, plan_path, r_doc=R_DOC_DEFAULT, *, r_plan_path=None):
    """단계 2 관문 — 개정 커밋이 HEAD 의 조상 · 그 커밋 등록 R 문서의 `| S0 계획 해시 |` 줄 끝 칸 = 계획 파일 sha256 · 식 재유도 · 정준.
    ★ 10-21 (사전 리뷰 PRE-design-04 · 등록 R §2-1 · §2-1b · §11 ④) — 같은 커밋의 `| 계획 해시 |` 줄 (R 런 사슬 계획 · 사슬과 같은 함수
    `rint_r_chain.registration_plan_hash` · ⬜ = s_min 미등록 = 거부) = r_plan_path 파일 sha256 · 그 꼴 (`rint_r_chain.load_plan`) · 두 계획
    대조 (tol_ff_um = S0 values_um.tol_ff · len_law = 원장의 길이 법칙).  옛 관문 = S0 해시가 문서 어디에든 있으면 통과 · R 런 계획 · s_min 은
    보지 않았다 (DBE 를 s_min 봉인 전에 열 수 있었다).
    → (계획, sha256, 전체 sha, R 런 계획 결합 기록).  커밋 순서만으로는 시점 증명이 안 된다 (v3 판정) → 해시로 묶는다."""
    if not isinstance(sha, str) or not _SHA_RE.match(sha):
        raise S0Error('--threshold-commit 은 ASCII 16진 7–40 자 (전각 · 공백 · 다른 문자 거부)')
    if r_plan_path is None:
        raise S0Error('단계 2 관문 — --r-plan-path (같은 개정 커밋의 R 런 사슬 계획 · s_min 봉인) 가 없다 (★ 10-21 PRE-design-04)')
    for p in (plan_path, r_doc, r_plan_path):
        if (not isinstance(p, str) or not p or os.path.isabs(p) or '..' in p.split('/') or not p.isascii()
                or re.search(r'\\s', p)):
            raise S0Error(f'리포 상대 ASCII 경로여야 한다: {p!r}')''')

rep('''    r = _git(repo, 'show', f'{full}:{r_doc}')
    if r.returncode != 0:
        raise S0Error(f'커밋 {full[:12]} 에 등록 R 문서 {r_doc} 가 없다')
    if h not in r.stdout:
        raise S0Error(f'등록 R 문서 ({r_doc} @ {full[:12]}) 에 계획 sha256 {h[:16]}… 이 없다 — §2-1 개정 커밋이 아니다')
    try:
        plan = json.loads(pb.decode('ascii'))
    except Exception as e:                                  # noqa: BLE001
        raise S0Error(f'계획 파일이 ASCII JSON 이 아니다 ({type(e).__name__})')
    check_plan(plan)
    if plan_bytes_of(plan) != pb:
        raise S0Error('계획 파일이 정준 바이트가 아니다 (손으로 고친 형식) — 단계 1 산출물 그대로 커밋할 것')
    return plan, h, full''',
    '''    r = _git(repo, 'show', f'{full}:{r_doc}', text=False)
    if r.returncode != 0:
        raise S0Error(f'커밋 {full[:12]} 에 등록 R 문서 {r_doc} 가 없다')
    doc_raw = r.stdout
    try:
        doc = doc_raw.decode('utf-8')
    except UnicodeDecodeError:
        raise S0Error(f'등록 R 문서 ({r_doc} @ {full[:12]}) 가 UTF-8 이 아니다') from None
    if _row_value(doc, 'S0 계획 해시') != h:
        raise S0Error(f'등록 R 문서 ({r_doc} @ {full[:12]}) 의 "| S0 계획 해시 |" 끝 칸 ≠ 계획 sha256 {h[:16]}… — §2-1 개정 커밋이 아니다 '
                      f'(★ 10-21 — 줄 밖 · 다른 칸에 적힌 해시는 세지 않는다)')
    try:
        plan = json.loads(pb.decode('ascii'))
    except Exception as e:                                  # noqa: BLE001
        raise S0Error(f'계획 파일이 ASCII JSON 이 아니다 ({type(e).__name__})')
    check_plan(plan)
    if plan_bytes_of(plan) != pb:
        raise S0Error('계획 파일이 정준 바이트가 아니다 (손으로 고친 형식) — 단계 1 산출물 그대로 커밋할 것')
    #  ★ 10-21 (PRE-design-04) — R 런 사슬 계획 (같은 커밋 · s_min 봉인) — 사슬과 같은 함수 (사본 없음)
    import rint_r_chain as _rrc
    with tempfile.TemporaryDirectory(prefix='s0_r_') as td:
        dp = os.path.join(td, 'R.md')
        with open(dp, 'wb') as f:
            f.write(doc_raw)
        try:
            r_hash, _doc_sha = _rrc.registration_plan_hash(dp)
        except _rrc.Stop as e:
            raise S0Error(f'등록 R 문서 ({r_doc} @ {full[:12]}) 의 R 런 계획 줄 — {e.code}: {e.cause} (s_min 봉인 전 DBE 단계 2 금지)') from None
        r = _git(repo, 'show', f'{full}:{r_plan_path}', text=False)
        if r.returncode != 0:
            raise S0Error(f'커밋 {full[:12]} 에 R 런 계획 파일 {r_plan_path} 이 없다')
        rpb = r.stdout
        if hashlib.sha256(rpb).hexdigest() != r_hash:
            raise S0Error(f'R 런 계획 파일 {r_plan_path} sha256 {hashlib.sha256(rpb).hexdigest()[:16]}… ≠ 등록 "| 계획 해시 |" '
                          f'{r_hash[:16]}… (같은 커밋)')
        rp = os.path.join(td, 'r_plan.json')
        with open(rp, 'wb') as f:
            f.write(rpb)
        try:
            robj, _rsha = _rrc.load_plan(rp)
        except _rrc.Stop as e:
            raise S0Error(f'R 런 계획 파일 {r_plan_path} — {e.code}: {e.cause}') from None
    if robj['tol_ff_um'] != plan['values_um']['tol_ff']:
        raise S0Error(f"두 계획 대조 — R 런 계획 tol_ff_um {robj['tol_ff_um']!r} ≠ S0 계획 values_um.tol_ff {plan['values_um']['tol_ff']!r} "
                      f'(같은 float · 등록 R §2-1)')
    if robj['len_law'] != cj.CJUNC_LEN_LAW:
        raise S0Error(f"두 계획 대조 — R 런 계획 len_law {robj['len_law']!r} ≠ 원장의 길이 법칙 {cj.CJUNC_LEN_LAW!r}")
    rinfo = {'path': r_plan_path, 'sha256': r_hash, 's_min_um': float(robj['s_min_um']), 'tol_ff_um': float(robj['tol_ff_um']),
             'len_law': robj['len_law'], 'unreg_law': robj['unreg_law'], 'step3_rtol': float(robj['step3_rtol']),
             'checked': 'S0 row exact · R row (registration_plan_hash) · R plan sha256 · load_plan · tol_ff = S0 tol_ff · len_law'}
    return plan, h, full, rinfo''')

rep('''def census_kit(kit, out_dir, *, stage, plan=None, plan_sha=None, plan_source=None, vox=0.15, bridge_um=0.48,
               sdcp_sphere_d=0.30, scripts_dir=SCRIPTS):''',
    '''def census_kit(kit, out_dir, *, stage, plan=None, plan_sha=None, plan_source=None, vox=0.15, bridge_um=0.48,
               sdcp_sphere_d=0.30, scripts_dir=SCRIPTS, plan_extra=None):''')

rep('''        'plan': {'sha256': plan_sha, 'source': plan_source},''',
    '''        'plan': dict({'sha256': plan_sha, 'source': plan_source}, **(plan_extra or {})),''')

rep('''def run_stage(stage, kits, out_dir, *, threshold_commit=None, plan_path=None, repo=None, r_doc=R_DOC_DEFAULT,
              vox=0.15, bridge_um=0.48, sdcp_sphere_d=0.30, scripts_dir=SCRIPTS):''',
    '''def run_stage(stage, kits, out_dir, *, threshold_commit=None, plan_path=None, repo=None, r_doc=R_DOC_DEFAULT,
              vox=0.15, bridge_um=0.48, sdcp_sphere_d=0.30, scripts_dir=SCRIPTS, r_plan_path=None):''')

rep('''    plan = plan_sha = plan_source = None
    if stage == 1:
        if len(kits) != 1:
            raise S0Error('단계 1 = SBE 침대 하나 (계획은 한 침대의 기하에서만 나온다)')
        if threshold_commit or plan_path:
            raise S0Error('단계 1 에는 --threshold-commit · --plan-path 를 주지 않는다')
    else:
        if not threshold_commit or not plan_path:
            raise S0Error('단계 2 는 --threshold-commit <§2-1 개정 커밋> · --plan-path <리포 안 계획> 가 있어야 돈다 (N17)')
        plan, plan_sha, full = verify_plan_commit(repo or ROOT, threshold_commit, plan_path, r_doc=r_doc)
        plan_source = f'commit:{full}\'''',
    '''    plan = plan_sha = plan_source = plan_extra = None
    if stage == 1:
        if len(kits) != 1:
            raise S0Error('단계 1 = SBE 침대 하나 (계획은 한 침대의 기하에서만 나온다)')
        if threshold_commit or plan_path or r_plan_path:
            raise S0Error('단계 1 에는 --threshold-commit · --plan-path · --r-plan-path 를 주지 않는다')
    else:
        if not threshold_commit or not plan_path or not r_plan_path:
            raise S0Error('단계 2 는 --threshold-commit <§2-1 개정 커밋> · --plan-path <리포 안 계획> · --r-plan-path <같은 커밋의 R 런 '
                          '사슬 계획 · s_min 봉인> 가 있어야 돈다 (N17 · ★ 10-21 PRE-design-04)')
        plan, plan_sha, full, rinfo = verify_plan_commit(repo or ROOT, threshold_commit, plan_path, r_doc=r_doc,
                                                         r_plan_path=r_plan_path)
        plan_source = f'commit:{full}'
        plan_extra = {'r_plan': rinfo}''')

rep('''        rep, arrays, pout, jarrays = census_kit(kit, out_dir, stage=stage, plan=plan, plan_sha=plan_sha,
                                                plan_source=plan_source, vox=vox, bridge_um=bridge_um,
                                                sdcp_sphere_d=sdcp_sphere_d, scripts_dir=scripts_dir)''',
    '''        rep, arrays, pout, jarrays = census_kit(kit, out_dir, stage=stage, plan=plan, plan_sha=plan_sha,
                                                plan_source=plan_source, vox=vox, bridge_um=bridge_um,
                                                sdcp_sphere_d=sdcp_sphere_d, scripts_dir=scripts_dir, plan_extra=plan_extra)''')

rep('''    ap.add_argument('--r-doc', default=R_DOC_DEFAULT, help='계획 sha256 이 적힌 등록 R 문서 (리포 상대)')''',
    '''    ap.add_argument('--r-plan-path', default=None, help='단계 2 — 같은 개정 커밋 안 R 런 사슬 계획 (rint-r-plan-v1 · s_min 봉인) 의 리포 '
                                                         '상대 경로 (sha256 = 등록 R "| 계획 해시 |" 줄)')
    ap.add_argument('--r-doc', default=R_DOC_DEFAULT, help='계획 sha256 이 적힌 등록 R 문서 (리포 상대)')''')

rep('''        res = run_stage(a.stage, a.kit, a.out, threshold_commit=a.threshold_commit, plan_path=a.plan_path, repo=a.repo,
                        r_doc=a.r_doc, vox=a.vox, bridge_um=a.bridge_um, sdcp_sphere_d=a.sdcp_sphere_d)''',
    '''        res = run_stage(a.stage, a.kit, a.out, threshold_commit=a.threshold_commit, plan_path=a.plan_path, repo=a.repo,
                        r_doc=a.r_doc, vox=a.vox, bridge_um=a.bridge_um, sdcp_sphere_d=a.sdcp_sphere_d,
                        r_plan_path=a.r_plan_path)''')

rep(''''rule': reg['rules'].get('branch'), 'meaning': '같은 fid 가 같은 셀을 비연속으로 다시 지난 가지 쌍 (가지마다 따로 · 합치지 않음 · '
                                                           'RCA-03) — s = 그 쌍이 든 자기 후보의 경로 호 길이'}''',
    ''''rule': reg['rules'].get('branch'), 'meaning': '같은 조각이 같은 셀을 비연속으로 다시 지난 가지 쌍 (가지마다 따로 · 합치지 않음 · '
                                                           'RCA-03 · 고리 이음매 별칭 제외) — s = 그 쌍의 경로 호 간격 (쌍마다 · ★ 10-21)'}''')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
