    #  ── 환경 꼴 (자식 프로세스 · 환경변수는 프로세스 시작 전에) — OpenBLAS 계산 경로 Haswell (AVX2 = Codex 와 비트 같은 경로 · 메인 10-21 확인) ↔
    #     기본 (이 CPU = SkylakeX AVX-512) × 스레드 1 · 4.  ⓓ 결론은 같아야 하고 (다르면 통과한 쪽이 참조값과 1e-4 안 = 보수) · ⓐ ⓑ ⓒ 의 칼날 사례 (주 반례
    #     ⓑ 불균형 9.15e-5 ↔ 1.47e-4) 는 경로마다 다르게 판정되는 것이 정상 (기록 · 단언 아님).
    ENVS = (('Haswell', '1'), ('default', '1'), ('default', '4'), ('Haswell', '4'))
    envs = {}
    for ct, nthr in ENVS:
        env = {k: v for k, v in os.environ.items() if k not in ('PYTHONPATH', 'PYTHONHOME', 'OPENBLAS_CORETYPE')}
        env.update(OPENBLAS_NUM_THREADS=nthr, OMP_NUM_THREADS=nthr, MKL_NUM_THREADS=nthr, NUMEXPR_NUM_THREADS=nthr)
        if ct != 'default':
            env['OPENBLAS_CORETYPE'] = ct
        p = subprocess.run([sys.executable, '-I', os.path.abspath(__file__), '--probe-env'], capture_output=True, text=True,
                           env=env, timeout=3600)
        line = [x for x in p.stdout.splitlines() if x.startswith('PROBE_ENV ')]
        envs[f'{ct}/{nthr}'] = (json.loads(line[-1][len('PROBE_ENV '):]) if (p.returncode == 0 and line)
                                else {'_error': (p.returncode, p.stderr[-400:])})
    refs = {which: codex_chain(which)[-1] for which in CODEX}
    for variant, sysd in sys_probe:
        Ib0, _ = CC.plate_currents(sysd['phi_direct'], sysd['Ab'], sysd['gb'], sysd['At'], sysd['gt'])
        for rt in (1e-8, 1e-12):
            refs[f'probe_{variant}_{rt:.0e}'] = Ib0
    keys = sorted(refs)
    errs = {e: v['_error'] for e, v in envs.items() if '_error' in v}
    print('    환경 꼴 표 (사례 · 환경 = ⓐⓑⓒⓓ (1 통과 · 0 거부) · ⓓ 보장 오차 상한 · ⓑ 불균형):')
    for k in keys:
        cells = []
        for e in envs:
            r = envs[e].get(k) or {}
            f = ''.join('1' if r.get(x) else '0' for x in ('pass_a', 'pass_b', 'pass_c', 'pass_d'))
            eb, im = r.get('err_bound'), r.get('imbalance')
            cells.append(f'{e} {f} {eb:.2e} {im:.2e}' if isinstance(eb, float) and isinstance(im, float) else f'{e} {f} -')
        print(f'      {k:20s} ' + ' | '.join(cells))
    same_d = all(len({(envs[e].get(k) or {}).get('pass_d') for e in envs}) == 1
                 and len({(envs[e].get(k) or {}).get('status') for e in envs}) == 1 for k in keys)
    unsound = []
    for e, out in envs.items():
        for k in keys:
            r = out.get(k) or {}
            if r.get('pass_d') is True:
                G = float.fromhex(r['sigma_hex'])
                lim = 1e-4 if k in CODEX else 1e-4 + 1e-6          # 탐침 참조 = 직접해 (자기 오차 ~1.5e-8)
                if not abs(G - refs[k]) <= lim * abs(G):
                    unsound.append((e, k, G, refs[k]))
    abc_flip = [k for k in keys if len({tuple((envs[e].get(k) or {}).get(x) for x in ('pass_a', 'pass_b', 'pass_c')) for e in envs}) > 1]
    bit_flip = [k for k in keys if len({(envs[e].get(k) or {}).get('sigma_hex') for e in envs}) > 1]
    print(f'    σ 비트가 환경마다 다른 사례 {bit_flip} · ⓐ ⓑ ⓒ 판정이 환경마다 다른 사례 (칼날 · 정상 · 기록) {abc_flip} · BLAS '
          f'{[envs[e].get("_blas") for e in envs]}')
    chk('T17c 환경 꼴 넷 (OpenBLAS Haswell ↔ 기본 SkylakeX × 스레드 1 · 4 · 자식 프로세스) — 사례 10 개 ⓓ · 상태 결론 같음',
        not errs and same_d, errs or None)
    chk('T17c2 같은 표 — 어느 환경에서든 ⓓ 통과한 해는 참조값 (Codex = 정확 직렬 G* · 탐침 = 직접해) 과 상대 1e-4 안 (보수 · 거짓 통과 0)',
        not errs and not unsound, unsound[:3])
