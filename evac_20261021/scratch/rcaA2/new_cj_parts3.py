# Part 3 — plan · entry gate · assembler (A round 2 · 10-21).  flake8: noqa


def cjunc_plan(reg, R_j_ohm, *, unreg_law, ptfe_stamp, ptfe_jlaw='P0', sdcp_mod=None, quantitative=True,
               allow_rj_limits=False, rj_reference=RJ_REFERENCE_PLANE, lead_subtraction=None, sv_counterfactual=None):
    """분산 간선 (원장 'subedges') 마다 간선 (g = 1e4·m/(k·R_j′) · m = 길이 법칙 v0 배율 · k = 그 instance 의 간선 수) · 축약 (R_j′ = 0) ·
    절단 (P1 · 간선마다 덮임) · 미실현.  S3 = sdcp_mod {'c': c} (간선마다 근접 · S2 원장 없이 = 거부).  정량 (quantitative=True): R_j 유한
    > 0 (극한 0 · ∞ = allow_rj_limits 사다리 진단 전용) · c ∈ {0, 1} · 원장 거부 사유 (s_min 미등록 포함) = 거부.  긴 접촉은 거부하지
    않는다 (옛 J8 · 길이 법칙 + 분산판 v0 이 맡는다 · 수는 기록).  sv_counterfactual = 반사실 대조 노브 (`_sv_cf_request` · 기본 끔).
    ★ 10-21 (사전 리뷰 PRE-impl-03 · 1저자 Q-C) — ptfe_stamp centerline = 거부 (시험 모드 포함 · 접합은 off · face_alpha 에서만)."""
    if not isinstance(reg, dict) or reg.get('kind') != 'cjunc_registry':
        raise TypeError('cjunc_plan: 원장은 cjunc_registry 의 결과여야 한다 (S3 = S2 원장 없이 거부 · 설계 §5-2)')
    if registry_fp(reg) != reg.get('fp', {}).get('registry'):
        raise ValueError('cjunc_plan: 원장이 만든 뒤 바뀌었다 (지문 불일치 · E5)')
    if rj_reference != RJ_REFERENCE_PLANE:
        raise ValueError(f'cjunc_plan: R_j 기준면 {rj_reference!r} — v0 는 모형 내부값 ({RJ_REFERENCE_PLANE}) 만 받는다 (T1-5′ · J4)')
    if lead_subtraction is not None:
        raise ValueError('cjunc_plan: 리드 빼기 (단자 기준 R_j) = v0 미지원 · 거부 (T1-5′ — 실측 순접촉값 주장 없음)')
    if isinstance(R_j_ohm, bool) or not isinstance(R_j_ohm, (int, float, np.floating, np.integer)):
        raise TypeError(f'cjunc_plan: R_j = 실수 (Ω): {R_j_ohm!r}')
    R0 = float(R_j_ohm)
    if math.isnan(R0) or R0 < 0.0:
        raise ValueError(f'cjunc_plan: R_j 는 NaN · 음수일 수 없다: {R_j_ohm!r}')
    if (R0 == 0.0 or math.isinf(R0)) and not allow_rj_limits:
        raise ValueError('cjunc_plan: R_j 극한 (0 = 사다리 천장 축약 · ∞ = 바닥) 은 allow_rj_limits 표지 (사다리 진단) 와만 — 정량 거부')
    if unreg_law not in UNREG_LAWS:
        raise ValueError(f'cjunc_plan: 미등록 VV 면 법칙 {unreg_law!r} — 선언 필수 {UNREG_LAWS} (자동 fallback 없음 · v2 §3-6)')
    if ptfe_stamp not in PTFE_STAMPS:
        raise ValueError(f'cjunc_plan: ptfe_stamp 선언 필수 {PTFE_STAMPS}: {ptfe_stamp!r}')
    if ptfe_stamp == 'centerline':
        raise ValueError('cjunc_plan: 접합 + ptfe_stamp centerline = 거부 (10-21 사전 리뷰 PRE-impl-03 · 1저자 Q-C — centerline 은 VGCF 셀을 '
                         'sid 7 로 덮는다: 옛 판은 덮인 접점의 포트를 옆 셀로 옮겨 절연체를 더해 σ 가 올랐다 (Rayleigh 위반) · '
                         '접합은 off · face_alpha 에서만)')
    if ptfe_jlaw not in PTFE_JLAWS:
        raise ValueError(f'cjunc_plan: PTFE–접합 법칙 {ptfe_jlaw!r} ∉ {PTFE_JLAWS}')
    if ptfe_jlaw == 'P1' and ptfe_stamp != 'face_alpha':
        raise ValueError(f'cjunc_plan: P1 은 face_alpha 에서만 ({ptfe_stamp} — off 는 PTFE 표현이 없다 · 설계 §4-1)')
    svc = _sv_cf_request(sv_counterfactual)
    c = None
    if sdcp_mod is not None:
        if not isinstance(sdcp_mod, dict) or set(sdcp_mod) - {'c'} or 'c' not in sdcp_mod:
            raise TypeError(f"cjunc_plan: sdcp_mod = {{'c': c}} 만: {sdcp_mod!r}")
        cv = sdcp_mod['c']
        if isinstance(cv, bool) or not isinstance(cv, (int, float, np.floating, np.integer)):
            raise TypeError(f'cjunc_plan: c = 실수: {cv!r}')
        c = float(cv)
        if not (math.isfinite(c) and 0.0 <= c <= 1.0):
            raise ValueError(f'cjunc_plan: c ∈ [0, 1] 유한: {cv!r}')
        if quantitative and c not in (0.0, 1.0):
            raise ValueError(f'cjunc_plan: 정량 R 런의 c 는 {{0, 1}} 만 (시험 격자는 quantitative=False): {c}')
    inst = reg['instances']
    sub = reg['subedges']
    nI = len(inst['fi'])
    nS = len(sub['inst'])
    mult = np.asarray(inst['mult'], np.float64).copy()       # 길이 법칙 v0 (원장에서 한 번 · 계획은 읽기만)
    if not (np.isfinite(mult).all() and (mult >= 1.0).all()):
        raise ValueError('cjunc_plan: 길이 법칙 배율은 유한 · ≥ 1 이어야 한다 (max(1, L_c/L_par)) — 원장 이상')
    kk = np.asarray(inst['nsub'], np.int64)
    io = np.asarray(sub['inst'], np.int64)
    if len(kk) != nI or (nI and (kk < 1).any()) or int(kk.sum()) != nS or (nS and not np.array_equal(np.bincount(io, minlength=nI), kk)):
        raise ValueError('cjunc_plan: 분산 간선 표 ↔ instance 간선 수 (k) 가 맞지 않는다 — 원장 이상')
    mode = np.zeros(nS, np.int64)
    g = np.zeros(nS, np.float64)
    rje = np.full(nS, np.nan)
    a = np.asarray(sub['a_sdcp'], bool).astype(np.float64)
    for e in range(nS):
        q = int(io[e])
        if not sub['realized'][e]:
            mode[e] = MODE_UNREALIZED
            continue
        if ptfe_jlaw == 'P1' and sub['ptfe_cov'][e]:
            mode[e] = MODE_CUT_P1                            # N18 — 덮인 간선은 c 와 무관하게 먼저 절단 (간선마다 · RCA-05)
            continue
        if c is not None and math.isinf(R0) and c * a[e] == 1.0:
            r = 0.0                                          # Z3 — 바닥 (R_j,0 = ∞) 의 c = 1 근접 = 축약 (∞·0 = NaN 금지 · 유한 R_j,0 은 아래 식 그대로)
        else:
            r = R0 if c is None else float(sdcp_rj_eff(R0, c, a[e]))
        rje[e] = r
        if r == 0.0:
            mode[e] = MODE_CONTRACT
        elif math.isinf(r):
            mode[e] = MODE_NONE_INF
        else:
            mode[e] = MODE_EDGE
            g[e] = float(junction_g_code(r)) * float(mult[q]) / float(kk[q])   # 간선 G = (max(1, L_c/L_par) / R_j′)/k (분산판 v0)
    long = np.asarray(inst['long'], bool)
    rej = [dict(x) for x in reg['rejections']]               # 긴 접촉 = 거부 아님 (길이 법칙 v0 · 1저자 10-20 Q17)
    if not quantitative:
        rej = []
    near = int(np.sum(np.asarray(sub['a_sdcp'], bool) & np.asarray(sub['realized'], bool)))
    share = (mult[io] / kk[io]) if nS else np.zeros(0)       # 간선마다 배율 몫 (m/k) — k 1 = 옛 instance 배율 그대로
    counts = {'n_instances': nI, 'n_subedges': nS, 'n_edge': int(np.sum(mode == MODE_EDGE)),
              'n_contract': int(np.sum(mode == MODE_CONTRACT)),
              'n_cut_p1': int(np.sum(mode == MODE_CUT_P1)), 'n_unrealized': int(np.sum(mode == MODE_UNREALIZED)),
              'n_none_inf': int(np.sum(mode == MODE_NONE_INF)), 'n_long': int(np.sum(long)), 'n_sdcp_near': near,
              'n_contracted_by_c': int(np.sum((mode == MODE_CONTRACT) & (R0 > 0.0))),
              'n_ptfe_cov': int(np.sum(np.asarray(sub['ptfe_cov'], bool))),
              'len_mult_sum_edge': float(np.sum(share[mode == MODE_EDGE])),
              'len_mult_max': (float(np.max(mult)) if nI else None)}
    record = {'model': CJUNC_MODEL_VERSION, 'schema': CJUNC_SCHEMA, 'status': CJUNC_STATUS,
              'qualifiers': list(CJUNC_QUALIFIERS), 'R_j_ohm': (R0 if math.isfinite(R0) else 'inf'),
              'len_law': CJUNC_LEN_LAW, 'dist_rule': CJUNC_DIST_RULE, 's_min_um': reg['thresholds']['s_min_um'],
              'rj_reference_plane': RJ_REFERENCE_PLANE, 'half_cell_in_edge': False, 'unreg_law': unreg_law,
              'ptfe_jlaw': ptfe_jlaw, 'ptfe_stamp': ptfe_stamp,
              'sdcp_mod': (None if c is None else {'c': c, 'tol_sj_um': reg['thresholds']['tol_sj_um'],
                                                   'r_sdcp_um': reg['thresholds']['r_sdcp_um']}),
              's3_discriminating': (None if c is None else bool(near > 0)),
              'sv_counterfactual_request': (None if svc is None else dict(svc)),
              'quantitative': bool(quantitative), 'allow_rj_limits': bool(allow_rj_limits),
              'thresholds': dict(reg['thresholds']), 'rules': dict(reg['rules']), 'census': dict(reg['census']),
              'counts': counts, 'fp_registry': reg['fp']['registry'], 'fp_sid': reg['fp']['sid']}
    plan = {'kind': 'cjunc_plan', 'version': CJUNC_MODEL_VERSION, 'registry': reg, 'mode': mode, 'g_code': g, 'rj_eff': rje,
            'mult': mult, 'unreg_law': unreg_law, 'ptfe_jlaw': ptfe_jlaw, 'ptfe_stamp': ptfe_stamp,
            'sdcp_mod': (None if c is None else {'c': c}), 'quantitative': bool(quantitative), 'rejections': rej,
            'sv_counterfactual': svc, 'record': record}
    plan['fp_rows'] = plan_rows_fp(plan)
    return plan


def cjunc_require_quantitative(plan, sid, vox, sigma_of_sid=None, rint=None, iface=None, periodic_xy=False,
                               return_field=False):
    """솔브 입구 관문 (조립 전 · CG 0) — 계획 모양 · 지문 · 불변량 · 거부 사유 · 동시 사용 · 격자 결합 · 채널 · ★ 10-21 PTFE 규약
    (centerline = 거부 · Q-C)."""
    if not isinstance(plan, dict) or plan.get('kind') != 'cjunc_plan':
        raise TypeError('cjunc 는 cjunc_plan 의 결과여야 한다 (S3 sdcp_mod 단독 = 거부)')
    if plan.get('version') != CJUNC_MODEL_VERSION or plan.get('record', {}).get('schema') != CJUNC_SCHEMA:
        raise ValueError(f"cjunc: 다른 판본 계획 ({plan.get('version')!r}) — 거부")
    reg = plan['registry']
    if registry_fp(reg) != reg['fp']['registry']:
        raise ValueError('cjunc: 원장이 계획 뒤 바뀌었다 (지문 · E5)')
    if plan_rows_fp(plan) != plan.get('fp_rows'):
        raise ValueError('cjunc: 계획 행이 만든 뒤 바뀌었다 (지문 · E5)')
    if plan.get('ptfe_stamp') not in ('off', 'face_alpha') or plan.get('record', {}).get('ptfe_stamp') != plan.get('ptfe_stamp'):
        raise ValueError(f"cjunc: ptfe_stamp {plan.get('ptfe_stamp')!r} (기록 {plan.get('record', {}).get('ptfe_stamp')!r}) — 접합은 off · "
                         f'face_alpha 에서만 (centerline = 거부 · 10-21 사전 리뷰 PRE-impl-03 · Q-C · 조립 전)')
    if reg.get('rules', {}).get('len_law') != CJUNC_LEN_LAW or plan.get('record', {}).get('len_law') != CJUNC_LEN_LAW:
        raise ValueError(f"cjunc: 다른 접합 길이 법칙의 원장 · 계획 ({reg.get('rules', {}).get('len_law')!r}) — "
                         f'{CJUNC_LEN_LAW} 만 (옛 점 접합 · J8 거부 판 섞임 거부)')
    g = np.asarray(plan['g_code'], np.float64)
    mode = np.asarray(plan['mode'], np.int64)
    sub = reg.get('subedges') if isinstance(reg.get('subedges'), dict) else None
    if sub is None or g.shape != mode.shape or len(g) != len(sub['inst']):
        raise ValueError('cjunc: 계획 행 ↔ 원장 분산 간선 표 모양 불일치 (간선마다 한 행 · cjunc-v2) — 조립 전 거부')
    e = mode == MODE_EDGE
    if not (np.isfinite(g).all() and (g >= 0.0).all() and (g[e] > 0.0).all()):
        raise ValueError('cjunc: 계획 간선 g 는 유한 · 0 이상 (간선 행 > 0) — NaN · 음수 · inf = 조립 전 거부 (Q7 와 같은 꼴 · 지문을 다시 만든 변이도)')
    m = np.asarray(plan.get('mult'), np.float64)
    nI = len(reg['instances']['fi'])
    if m.shape != (nI,) or not (np.isfinite(m).all() and (m >= 1.0).all()):
        raise ValueError('cjunc: 계획 배율 (길이 법칙 v0) 은 instance 마다 유한 · ≥ 1 — 조립 전 거부')
    io = np.asarray(sub['inst'], np.int64)
    kk = np.asarray(reg['instances']['nsub'], np.float64)
    if e.any() and not np.array_equal(g[e], junction_g_code(np.asarray(plan['rj_eff'], np.float64)[e]) * m[io[e]] / kk[io[e]]):
        raise ValueError('cjunc: 계획 간선 g ≠ 1e4·m/(k·R_j′) — 배율 · 간선 수 기록과 쓰는 값이 묶이지 않았다 (지문을 다시 만든 변이 · '
                         '조립 전 거부)')
    if plan.get('sv_counterfactual') is not None and _sv_cf_request(plan['sv_counterfactual']) != plan['sv_counterfactual']:
        raise ValueError('cjunc: 반사실 대조 노브 모양 이상 — 조립 전 거부')
    if plan['rejections']:
        raise ValueError('cjunc 정량 모드 거부 — ' + ' · '.join(f"{x['code']}(n={x.get('n')})" for x in plan['rejections']))
    if rint:
        raise ValueError('cjunc: r1 탐침 표 (--step3-rint-e/-i) 와 동시 사용 거부 (설계 §4-3)')
    if iface is not None:
        raise ValueError('cjunc: ①′ AM–AM 막 (iface) 과 동시 사용 거부 (생산 HOLD · 설계 §4-3)')
    if periodic_xy:
        raise ValueError('cjunc: 주기 경계 정량 거부 (raster 가 주기 영상을 안 만든다 · J10)')
    if return_field:
        raise ValueError('cjunc v0 = σ_e 전용 — 장 · je · 분담 · Joule 진단은 원장을 읽기 전이라 거부 (return_field · 설계 §3-3 · §7 LEAN 4)')
    if tuple(np.asarray(sid).shape) != tuple(reg['shape']) or _grid_fp(sid) != reg['fp']['sid']:
        raise ValueError('cjunc: 다른 격자 (sid 지문 · 모양) — 원장을 그 sid 에서 다시 만들 것 (E5)')
    v = float(vox)
    if not (math.isfinite(v) and v == float(reg['vox'])):
        raise ValueError(f"cjunc: 솔버 vox {vox!r} ≠ 원장 vox {reg['vox']!r} (RIMP-05 와 같은 부류)")
    if sigma_of_sid is not None:
        a = np.asarray(sigma_of_sid, np.float64)
        s = np.asarray(sid)
        bad = (not (a.shape[0] > 3 and a[3] > 0.0)) if a.ndim == 1 else (not (a[s == 3] > 0.0).all())
        if bad and len(reg['positions']['lin']):
            raise ValueError('cjunc: 이 채널에서 VGCF 절연 (σ_VGCF = 0 · 이온 표) — 접합 요청은 전자 채널뿐 (조용한 무효 금지)')
    return plan
