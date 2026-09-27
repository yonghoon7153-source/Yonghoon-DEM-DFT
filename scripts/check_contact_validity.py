#!/usr/bin/env python3
"""접촉 유효성 검사 — **점착을 올리면 접촉모델이 먼저 죽는다**.

왜 이 검사가 필요한가 (실측 근거, 2026-09-19)
  믹서 팔 `E4`(CED 3e7 J/m³)를 정착시켰더니 지표는 멀쩡한 숫자를 냈는데
  (`H/R 2.023`) 그 밑에서 접촉모델이 무너져 있었다:
      겹침 δ/r_min  중앙 3.25 % · 90 % 3.92 % · **최대 197 %**
      드럼 벽 밖 입자 79 개 · 이미 삭제된 원자 2,296 개 (8,002 → 5,703)
  δ/r = 1.97 은 한 구의 중심이 상대 구의 **반대편 바깥**에 있다는 뜻이다
  = 겹침이 아니라 **통과**.  그 상태의 H/R 은 물리가 아니라 붕괴의 그림자다.

⚠ SJKR 은 겹침에 **선형**이고(`F = CED·2π·R*·δ`) Hertz 반발은 `δ^1.5` 다.
  ⇒ 평형은 언제나 존재하지만 CED 가 크면 **터무니없는 δ** 에서 잡힌다.
  ⇒ 연화된 영률(계산비용용 1e7 Pa)이 **점착 스윕의 천장을 정한다**.
     천장을 올리려면 E 를 올려야 하고 dt ∝ 1/√G 라 비용이 √E 로 는다.

⛔ 이 검사를 통과하지 못한 팔의 지표는 **인용하지 않는다**.

★★ 2026-09-27 (Codex HB-05) — **등록 계약은 `--contract` 다.**  사전등록 (`mixer_layered_prereg_20260921.md` §1) 의
  *"최대 겹침 실측 ≤ 1 %"* 를 옛 기본 모드 (마지막 프레임 하나 · 기각선 50 % · 벽 없음) 는 강제하지 못했다
  (Codex 반례: δ/r 2 % 통과 — 셀프테스트 ⑧).  `--contract` 는 정착 끝 t₀ 부터 마지막 덤프까지 **전 프레임**에서
  입자–입자 · 벽 (39 각형 드럼 + 끝판, **회전각 반영**) 최대 δ/r ≤ 1 % 와 상별 입자 수 · id 보존을 본다.
  ⚠ 드럼은 원통이 아니라 **39 각형**이다 — 면 한가운데가 꼭짓점 원보다 0.0426 mm (SE 반경의 56 %) 안쪽이라
    회전각을 틀리면 2 % 겹침이 '안 닿음' 으로 숨는다.  각은 덱에서 계산하고 (LIGGGHTS 는 매 스텝 ω·dt 누적 ·
    재개 때 메시 꼭짓점·경과시간 복원) **데이터로 되읽어 확인**한다 — 어긋나면 벽 값 무효 = TECH.

usage
  python3 scripts/check_contact_validity.py <덤프디렉터리> [...] [--label L]          # 옛 빠른 점검 (계약 아님)
  python3 scripts/check_contact_validity.py --contract <런디렉터리> [...] --n-expected 100000 --json out.json
  python3 scripts/check_contact_validity.py --selftest
"""
import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from measure_bed_aspect import frames, read_dump          # noqa: E402

#  판정선 — DEM 연질구 관례.  ⚠ 문턱이지 물리 상수가 아니다.
OVL_MEDIAN_WARN = 0.01      # 중앙 겹침 1 % 넘으면 경고
OVL_MAX_FAIL = 0.50         # 최대 겹침 50 % 넘으면 **기각** (통과 직전)
LOST_FAIL_PCT = 1.0         # 원자 1 % 넘게 잃으면 기각


def _pair_candidates(P, r, types=None):
    """겹칠 수 있는 쌍 후보 (n, 2).

    ★ `types` 가 있으면 **타입쌍별** 검색 (cutoff = 두 타입 최대 반경의 합).  2026-09-27: 캠페인 침대는
      AM_P(0.68 mm) 176 개 · SE(0.076 mm) 약 9.9 만 개라 `2·r_max` 한 번 검색이면 SE 한 알마다 반경 1.36 mm
      안의 이웃을 다 세어 **수천만 쌍**이 된다 (메모리 GB 급).  타입쌍별이면 SE–SE 는 0.15 mm 안만 본다.
      결과 집합은 전수 검색과 같다 (셀프테스트 ⑭).
    """
    from scipy.spatial import cKDTree
    if types is None:
        return cKDTree(P).query_pairs(2 * r.max(), output_type='ndarray')
    types = np.asarray(types).astype(int)
    idx = {t: np.flatnonzero(types == t) for t in np.unique(types)}
    tree = {t: cKDTree(P[ix]) for t, ix in idx.items()}
    rmax = {t: float(r[ix].max()) for t, ix in idx.items()}
    ts = sorted(idx)
    out = []
    for ia, a in enumerate(ts):
        for b in ts[ia:]:
            cut = rmax[a] + rmax[b]
            if a == b:
                pp = tree[a].query_pairs(cut, output_type='ndarray')
                if len(pp):
                    out.append(np.c_[idx[a][pp[:, 0]], idx[a][pp[:, 1]]])
            else:
                sm = tree[a].sparse_distance_matrix(tree[b], cut, output_type='ndarray')
                if len(sm):
                    out.append(np.c_[idx[a][sm['i']], idx[b][sm['j']]])
    return np.vstack(out) if out else np.zeros((0, 2), dtype=int)


def contacts(P, r, mol=None, types=None):
    """겹친 쌍의 (쌍, δ/r_min, 강체내부쌍수).  `types` 를 주면 타입쌍별 검색 (같은 결과, 훨씬 가볍다).

    ⚠⚠ **강체(multisphere) 내부 쌍을 빼야 한다** — 2026-09-19 실측으로 잡은 결함.
      섬유는 구를 `0.8·d` 간격으로 꿴 사슬이라 **설계상** `δ/r = 0.4` 로 겹쳐 있다.
      그것을 접촉으로 세면 다섯 팔 전부가 *"최대 겹침 40.0 %"* 를 내놓고, 그 값은
      점착과 아무 상관이 없다 (점착 0 인 `E0` 도 똑같이 40.0 %).
      ★ 그래서 나쁜 이유는 **보기 싫어서가 아니라 검사가 눈이 머는 것**이다:
        기각 문턱이 50 % 인데 섬유가 40 % 에 상주하면 **40~50 % 구간의 진짜 통과를
        못 본다**.  반대로 문턱을 조금만 내리면 모든 팔이 거짓 기각된다.
      ⇒ `mol` 이 같고 **양수**인 쌍만 제외한다.  LIGGGHTS 는 평범한 구에 `mol = -1`
        을 주므로 `> 0` 조건이 없으면 **평범한 구 쌍을 전부 지워** 버린다
        (실측: type 1·2·3 은 mol 고유값 1개 = −1).
      ★ 제외한 개수는 **보고한다** — 조용히 버리지 않는다.
    """
    try:
        pr = _pair_candidates(P, r, types)
    except ImportError:                                     # scipy 없으면 전수 (작은 입력 전용)
        if types is not None:
            raise SystemExit('⛔ scipy 가 없다 — 계약 판정(대용량)은 scipy 필수')
        n = len(r)
        pr = np.array([(i, j) for i in range(n) for j in range(i + 1, n)])
    if len(pr) == 0:
        return pr, np.zeros(0), 0
    i, j = pr[:, 0], pr[:, 1]
    d = np.linalg.norm(P[i] - P[j], axis=1)
    ov = (r[i] + r[j]) - d
    m = ov > 0
    if mol is not None:
        same = (mol[i] == mol[j]) & (mol[i] > 0)            # ★ > 0 이 필수
        n_intra = int((m & same).sum())
        m = m & ~same
    else:
        n_intra = 0
    return pr[m], ov[m] / np.minimum(r[i], r[j])[m], n_intra


def check(d, n_expected=None, label=None):
    step, path = frames(d)[-1]
    D = read_dump(path)
    P = np.c_[D['x'], D['y'], D['z']]
    r = D['radius']
    pr, rel, n_intra = contacts(P, r, D.get('mol'))
    lost = (100.0 * (n_expected - len(r)) / n_expected) if n_expected else 0.0
    bad = []
    if len(rel) and float(np.max(rel)) > OVL_MAX_FAIL:
        bad.append(f'최대 겹침 {np.max(rel)*100:.0f} % > {OVL_MAX_FAIL*100:.0f} %')
    if lost > LOST_FAIL_PCT:
        bad.append(f'원자 손실 {lost:.1f} % > {LOST_FAIL_PCT} %')
    return dict(label=label or d, step=step, n=len(r), n_contact=len(pr),
                n_intra=n_intra,
                cn=(2.0 * len(pr) / len(r) if len(r) else float('nan')),
                ovl_med=(float(np.median(rel)) if len(rel) else 0.0),
                ovl_p90=(float(np.percentile(rel, 90)) if len(rel) else 0.0),
                ovl_max=(float(np.max(rel)) if len(rel) else 0.0),
                lost_pct=lost, reject=bad)


# ════════════════════════ 계약 판정 (2026-09-27, Codex HB-05) ════════════════════════
#  사전등록 `mixer_layered_prereg_20260921.md` §1 은 *"최대 겹침 실측 ≤ 1 %"* 를 계약으로 적었는데 위 check() 는
#  ⓐ 마지막 프레임 하나만 ⓑ 기각선 50 % ⓒ 벽 없음 ⓓ 상별 보존 없음이었다 (Codex 반례: δ/r 2 % 가 통과).
#  아래 check_window() 가 등록 문구를 **실제로** 판정한다.  허용치는 결과를 보고 바꾸지 않는다.
CONTRACT_MAX_OVL = 0.01          # prereg §1 "최대 겹침 실측 ≤ 1 %" — 입자–입자 (δ/r_min) · 벽 (δ/r) 둘 다
PHASE_TOL_FRAC = 0.02            # 데이터로 되읽은 드럼 회전각 vs 덱 예정각 — 면 각도의 2 % (9.23° 면이면 0.18°)
PHASE_FRAMES = 5                 # 위상을 데이터로 확인할 프레임 수 (창 안에 고르게)


def read_stl(path):
    """STL (ASCII · 바이너리) → (n, 3, 3) 삼각형 배열 (STL 좌표 — scale 전)."""
    raw = open(path, 'rb').read()
    if raw[:5].lower() == b'solid' and b'facet' in raw[:4096]:
        V = np.array([[float(x) for x in l.split()[1:4]]
                      for l in raw.decode('utf-8', 'replace').splitlines() if l.strip().startswith('vertex')])
    else:
        import struct
        n = struct.unpack('<I', raw[80:84])[0]
        rec = np.dtype([('n', '<f4', (3,)), ('v', '<f4', (3, 3)), ('a', '<u2')])
        V = np.frombuffer(raw, dtype=rec, count=n, offset=84)['v'].astype(float).reshape(-1, 3)
    if len(V) == 0 or len(V) % 3:
        raise SystemExit(f'⛔ {path}: 꼭짓점 {len(V)} 개 — 삼각형으로 읽을 수 없다')
    return V.reshape(-1, 3, 3)


def deck_walls(deck_text):
    """덱 → 벽 명세 dict(meshes={id: (파일, scale)}, used=[벽 메시 id], moves={메시 id: 회전}, dt).

    회전 = dict(origin, axis(단위), period, start_step).  start_step = 그 `fix … move/mesh` 줄 **앞** run 합
    — LIGGGHTS 회전은 매 스텝 ω·dt 씩 **누적**하므로 (MeshMoverRotate::initial_integrate) 스텝 s 의 덤프에서
    각 = 2π·(s − start)·dt/period.  재개 (read_restart) 는 메시 꼭짓점 (FixMesh::restart) 과 경과시간
    (FixMoveMesh::restart) 을 복원하므로 이 식이 재개 뒤에도 이어진다 — 그래도 데이터로 확인한다 (infer_drum_phase).
    """
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from make_mixer_resume import logical_commands, _tokens      # 덱 논리 명령 파서 — 한 벌만 둔다
    meshes, used, moves, dt, steps = {}, [], {}, None, 0
    for _, blk in logical_commands(deck_text):
        t = _tokens(blk)
        if not t:
            continue
        if t[0] == 'timestep':
            dt = float(t[1])
        elif t[0] == 'run':
            steps = int(t[1]) if 'upto' in t else steps + int(t[1])
        elif t[0] == 'fix' and len(t) > 3 and t[3].startswith('mesh/surface'):
            kw = t[4:]
            for bad in ('move', 'rotate'):
                if bad in kw:
                    raise ValueError(f'메시 {t[1]} 에 자체 변환 `{bad}` — 지원하지 않는다')
            meshes[t[1]] = (kw[kw.index('file') + 1], float(kw[kw.index('scale') + 1]) if 'scale' in kw else 1.0)
        elif t[0] == 'fix' and len(t) > 3 and t[3] == 'wall/gran' and 'meshes' in t:
            k = t.index('meshes')
            used = t[k + 1:k + 1 + int(t[t.index('n_meshes') + 1])]
        elif t[0] == 'fix' and len(t) > 3 and t[3] == 'move/mesh':
            m = t[t.index('mesh') + 1]
            if 'rotate' not in t:
                raise ValueError(f'메시 {m} 의 이동이 rotate 가 아니다 — 지원하지 않는다')
            io, ia = t.index('origin'), t.index('axis')
            ax = np.array([float(x) for x in t[ia + 1:ia + 4]])
            moves[m] = dict(origin=np.array([float(x) for x in t[io + 1:io + 4]]), axis=ax / np.linalg.norm(ax),
                            period=float(t[t.index('period') + 1]), start_step=steps)
    return dict(meshes=meshes, used=used, moves=moves, dt=dt)


def _rot(axis, th):
    k = np.asarray(axis, float)
    K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) * np.cos(th) + np.sin(th) * K + (1 - np.cos(th)) * np.outer(k, k)


def mesh_angle(spec, mesh_id, step):
    mv = spec['moves'].get(mesh_id)
    if not mv or step <= mv['start_step']:
        return 0.0
    return 2 * np.pi * (step - mv['start_step']) * spec['dt'] / mv['period']


def _planes(tris, ref):
    """삼각형 → 안쪽-법선 평면 (N (k,3), c (k,)) — 안쪽 점 p 는 N·p + c ≥ 0.  같은 평면(쿼드의 두 삼각형)은 하나로."""
    a, b, c3 = tris[:, 0], tris[:, 1], tris[:, 2]
    nv = np.cross(b - a, c3 - a)
    L = np.linalg.norm(nv, axis=1)
    keep = L > 1e-12 * max(1.0, float(np.abs(tris).max()) ** 2)
    nv, a = nv[keep] / L[keep, None], a[keep]
    c = -(nv * a).sum(1)
    flip = (nv @ ref + c) < 0
    nv[flip] *= -1
    c[flip] *= -1
    scale = float(np.abs(tris).max())
    N, C = [], []
    for ni, ci in zip(nv, c):                          # 탐욕 병합 — 법선 1e-6 · 오프셋 1e-6·크기 안이면 같은 평면
        if not any(float(ni @ nj) > 1 - 1e-6 and abs(ci - cj) < 1e-6 * scale for nj, cj in zip(N, C)):
            N.append(ni)
            C.append(ci)
    return np.array(N), np.array(C)


def container_at(run_dir, spec, step, dtheta=0.0):
    """스텝 `step` 의 용기 평면 → (N, c, 평면별 메시 id, 드럼 면 수).  볼록이 아니면 ValueError.
    dtheta = 회전각에 더할 오프셋 (rad) — 영수증의 각 오차 전파용."""
    if not spec['used']:
        raise ValueError('덱에 wall/gran meshes 가 없다')
    unsupported = [m for m in spec['used'] if m not in ('Drum', 'Front', 'Back')]
    if unsupported:
        raise ValueError(f'벽 메시 {unsupported} — 볼록 용기(드럼+끝판) 밖의 메시(배플 등)는 지원하지 않는다')
    tri = {}
    for m in spec['used']:
        f, sc = spec['meshes'][m]
        T = read_stl(os.path.join(run_dir, f)) * sc
        mv = spec['moves'].get(m)
        if mv:
            R = _rot(mv['axis'], mesh_angle(spec, m, step) + dtheta)
            T = (T - mv['origin']) @ R.T + mv['origin']
        tri[m] = T
    ref = np.vstack([T.reshape(-1, 3) for T in tri.values()]).mean(0)
    N, C, owner = [], [], []
    n_drum = 0
    for m, T in tri.items():
        n_, c_ = _planes(T, ref)
        N.append(n_)
        C.append(c_)
        owner += [m] * len(c_)
        if m == 'Drum':
            n_drum = len(c_)
    N, C = np.vstack(N), np.concatenate(C)
    V = np.vstack([T.reshape(-1, 3) for T in tri.values()])
    if float((V @ N.T + C).min()) < -1e-5 * float(np.abs(V).max()):
        raise ValueError('용기가 볼록이 아니다 — 평면 최소거리 = 벽 거리 가 성립하지 않는다')
    return N, C, owner, n_drum


def wall_overlaps(P, r, N, C):
    """볼록 용기 안의 입자 → (δ/r, 가장 가까운 평면 번호).  δ = r − min_k(N_k·p + c_k)  (음수 = 안 닿음)."""
    s = P @ N.T + C
    k = np.argmin(s, axis=1)
    return (r - s[np.arange(len(P)), k]) / r, k


def infer_drum_phase(P, r, run_dir, spec, step, max_ovl=CONTRACT_MAX_OVL, tol_frac=PHASE_TOL_FRAC,
                     coarse=240, fine=240):
    """드럼 면 배치를 **데이터로** 되읽는다 — 드럼 평면을 축 둘레로 θ 만큼 더 돌려 가며 벽 근처 입자의 최대 δ/r 이
    가장 작은 θ 를 찾는다 (0 ≤ θ < 면 각).  반환 dict(status, theta_data, theta_sched, dtheta, facet, n_cand, …).

    status: ok (되읽은 각 = 예정 각, 허용 면각×tol_frac) · mismatch · few (벽 근처 입자 < 20 — 되읽지 않는다).
      한 프레임이라도 ok 이고 mismatch 가 없으면 **예정 식 자체가 확인된 것**이다 (식은 스텝의 결정론적 함수).
      하나도 ok 가 없으면 check_window 가 회전각과 무관한 해석적 상·하한으로 판정한다 (drum_worst · drum_best).
    ⚠ 왜 — 드럼은 **39 각형**이다 (Drum.stl 78 삼각형).  면 한가운데는 꼭짓점 원보다 반경 × (1 − cos(π/39))
      = 0.0426 mm 안쪽이고 그것은 SE 반경의 56 % 다.  회전각을 틀리면 2 % 겹침이 '안 닿음' 으로 숨는다 (⑩b).
    """
    mv = spec['moves'].get('Drum')
    f, sc = spec['meshes']['Drum']
    T0 = read_stl(os.path.join(run_dir, f)) * sc
    origin = mv['origin'] if mv else np.zeros(3)
    axis = mv['axis'] if mv else np.array([1.0, 0, 0])
    N0, C0 = _planes(T0, T0.reshape(-1, 3).mean(0))
    nf = len(C0)
    facet = 2 * np.pi / nf
    apo = float(C0.min())
    sag = apo / np.cos(facet / 2) - apo
    q = P - origin
    rho = np.linalg.norm(q - np.outer(q @ axis, axis), axis=1)
    cand = rho + r >= apo - sag
    out = dict(step=int(step), n_cand=int(cand.sum()), facet=facet,
               theta_sched=mesh_angle(spec, 'Drum', step) % facet,
               theta_data=float('nan'), dtheta=float('nan'), ovl_min=float('nan'))
    Pc, rc = q[cand], r[cand]

    def score(th):
        Nt = N0 @ _rot(axis, th).T
        return float(((rc - (Pc @ Nt.T + C0).min(1)) / rc).max())
    grid = np.arange(coarse) * facet / coarse
    if out['n_cand'] < 20:                 # 되읽기엔 적다 — 판정은 check_window 의 해석적 상·하한이 맡는다
        out['status'] = 'few'
        return out
    sc_ = np.array([score(t) for t in grid])
    j = int(np.argmin(sc_))
    g2 = grid[j] + (np.arange(fine) - fine / 2) * (2 * facet / coarse) / fine
    s2 = np.array([score(t) for t in g2])
    th = float(g2[int(np.argmin(s2))] % facet)
    d = (th - out['theta_sched'] + facet / 2) % facet - facet / 2
    out.update(theta_data=th, dtheta=float(d), ovl_min=float(s2.min()),
               status='ok' if abs(d) <= tol_frac * facet else 'mismatch')
    return out


def load_phase_receipt(path, spec):
    """재개-위상 영수증 (`scripts/mixer_restart_phase_test.py` 가 쓴다 — **이 바이너리**가 재개 뒤에도 덱 스케줄대로 메시를
    돌린다는 실측: 체크포인트 앞뒤의 `dump mesh/stl` 각 = 2π·(s − start)·dt/period) → dict.
    덱의 드럼 회전 (주기 · 축) 과 맞지 않거나 실패한 영수증이면 ValueError — 그 런은 영수증 없이 (상·하한) 판정한다.
    ⚠ 영수증은 코드 근거 (FixMoveMesh::restart 가 time_ 을 복원) 를 **실행 바이너리에서 실측**한 것이지 그 런의 벽 좌표가 아니다.
    """
    rc = json.load(open(path, encoding='utf-8'))
    miss = [k for k in ('test', 'passed', 'period', 'axis', 'angle_error_deg', 'binary_sha256') if k not in rc]
    if miss:
        raise ValueError(f'영수증에 {miss} 가 없다')
    if rc['test'] != 'restart_phase' or not rc['passed']:
        raise ValueError('영수증이 restart_phase 통과 기록이 아니다')
    mv = spec['moves'].get('Drum')
    if not mv:
        raise ValueError('덱에 드럼 회전이 없다')
    if abs(float(rc['period']) - mv['period']) > 1e-9 * mv['period']:
        raise ValueError(f'영수증 주기 {rc["period"]} ≠ 덱 {mv["period"]:g}')
    ax = np.asarray(rc['axis'], float)
    ax = ax / np.linalg.norm(ax)
    if float(ax @ mv['axis']) < 1 - 1e-9:
        raise ValueError('영수증 축 ≠ 덱 축')
    if not (0 <= float(rc['angle_error_deg']) <= 0.5):
        raise ValueError(f'영수증 각 오차 {rc["angle_error_deg"]}° — 0.5° 안이어야 쓴다')
    return rc


def container_from_stl(path, spec):
    """LIGGGHTS `dump mesh/stl` 파일 (시뮬레이션 단위 · **그 step 의 실제 벽**) → (N, c, 평면별 표지, 드럼 면 수).
    독립 기하 — 회전각을 계산하지 않고 덤프된 삼각형을 그대로 쓴다.  끝판 = 법선이 드럼 축과 나란한 평면 ('Cap')."""
    T = read_stl(path)
    N, C = _planes(T, T.reshape(-1, 3).mean(0))
    mv = spec['moves'].get('Drum') or dict(axis=np.array([1.0, 0, 0]))
    par = np.abs(N @ mv['axis']) > 0.99
    V = T.reshape(-1, 3)
    if float((V @ N.T + C).min()) < -1e-5 * float(np.abs(V).max()):
        raise ValueError('mesh 덤프의 용기가 볼록이 아니다')
    return N, C, ['Cap' if p_ else 'Drum' for p_ in par], int((~par).sum())


def check_window(run_dir, n_expected=None, max_ovl=CONTRACT_MAX_OVL, label=None, walls=True,
                 phase_receipt=None, expect_counts=None, diag_fit=False, progress=False):
    """★ 등록 계약 판정 — 분석 창 **전 프레임** (정착 끝 t₀ = `measure_mixing_index` 와 같은 정의 → 마지막 덤프).

      ① 입자–입자 최대 δ/r_min ≤ max_ovl (강체 내부 쌍 제외)
      ② 벽 — 드럼 다각 원통 + 두 끝판 — 최대 δ/r ≤ max_ovl.  **드럼 회전각의 근거** (2026-09-27 Codex HBR2-01: 입자 배치로
         회전각을 되읽는 fitting 은 증거가 아니다 — 참 벽 겹침 2 % 인데 위상이 반 면각 어긋나면 PASS · 5/5 ok 를 냈고, 참
         위상 · 0.5 % 는 TECH 로 막았다.  셀프테스트 ⑮ · ⑯):
           mesh-dump     post_mesh/mesh_<step>.stl (LIGGGHTS `dump mesh/stl`) 이 창 **전 프레임**에 있으면 그 삼각형 = 독립 기하
           receipt       `phase_receipt` (재개-위상 영수증) 가 덱과 맞으면 예정각 ± 영수증 각 오차 (최댓값)
           bounded       둘 다 없으면 회전각과 무관한 상·하한 — 상한 ≤ max_ovl 이면 PASS · 하한 > max_ovl 이면 REJECT
           unidentified  그 사이 = TECH (판정 불가.  예정각으로 잰 값은 **미검증**으로 보고만 한다)
      ③ 상별 입자 수 · id 집합 · **id 별 type · radius** = t₀ (총수 = n_expected · 상별 = expect_counts)  (HBR2-08)
      ④ 기술 조건 — 볼록 용기 · 창 프레임 ≥ 1 · **창 안 덤프 결손 없음** (HBR2-03: 미관측 구간에 통과 증서를 주지 않는다) ·
         덤프 헤더 TIMESTEP/원자 수 = 파일명/행 수 · 같은 step 중복 없음.  못 서면 **TECH** (통과로 치지 않는다)

    관측량 = **저장 프레임 최대** (snapshot-max).  덤프 사이 (이 덱 32 ms ≫ Hertz 충돌 ≈ 22 µs) 의 peak 는 관측하지 않는다 — D-1.
    verdict = PASS · REJECT (①②③ 위반) · TECH (④ 만).  둘 다면 REJECT.
    """
    from measure_mixing_index import deck_plan, _t0_frame, dump_header
    deck_path = os.path.join(run_dir, 'in.mixer')
    deck_text = open(deck_path, encoding='utf-8', errors='replace').read()
    plan = deck_plan(deck_path)
    fr = frames(os.path.join(run_dir, 'post'))
    reject, tech = [], []
    out = dict(label=label or run_dir, max_ovl=max_ovl, reject=reject, tech=tech, per_frame=[],
               observable='snapshot-max: 창의 저장 프레임에서 잰 최대 — 덤프 사이 peak 는 관측하지 않는다 (D-1)',
               dump_every=plan['dump_every'], dump_interval_s=plan['dump_every'] * plan['dt'],
               pp_max=float('-inf'), pp_max_step=None, pp_max_types=None, pp_max_by_pair={},
               wall_max=float('-inf'), wall_max_step=None, wall_max_type=None, wall_max_mesh=None,
               wall_max_by_type={}, wall_basis=None, phase=[], phase_status='not_run', phase_note='',
               n_frames=0, window=None)
    if not fr:
        tech.append('덤프가 없다')
        out['verdict'] = 'TECH'
        return out
    st0, _ = _t0_frame(fr, plan['steps_fill'])
    win = [(st, p) for st, p in fr if st >= st0]
    out['window'] = (win[0][0], win[-1][0])
    out['n_frames'] = len(win)
    #  ④ 창 격자 (HBR2-03) — t₀ 부터 마지막 프레임까지 dump_every 간격의 덤프가 **다** 있어야 한다
    de = plan['dump_every']
    present = [st for st, _ in win]
    pset = set(present)
    missing = [s for s in range(st0, win[-1][0] + 1, de) if s not in pset]
    if missing:
        tech.append(f'창 안 덤프 결손 {len(missing)} 개 (step {missing[:6]}{"…" if len(missing) > 6 else ""}) — '
                    '미관측 구간에 통과 증서를 줄 수 없다')
    off = [s for s in present if (s - st0) % de]
    if off:
        tech.append(f'덤프 격자 밖 step {off[:6]} — 덱의 dump_every {de} 와 맞지 않는다')
    if len(pset) != len(present):
        tech.append('같은 step 의 덤프가 둘 이상이다')
    spec = None
    if walls:
        try:
            spec = deck_walls(deck_text)
            container_at(run_dir, spec, st0)                     # 기하 검사 (볼록 · 파일) 를 창 앞에서 한 번
            #  회전각과 무관한 드럼 상·하한용: 축 · 변심거리(면 한가운데) · 꼭짓점 반경
            _mv = spec['moves'].get('Drum') or dict(origin=np.zeros(3), axis=np.array([1.0, 0, 0]))
            _f, _sc = spec['meshes']['Drum']
            _T = read_stl(os.path.join(run_dir, _f)) * _sc
            _q = _T.reshape(-1, 3) - _mv['origin']
            _ax = _mv['axis']
            _N0, _C0 = _planes(_T, _T.reshape(-1, 3).mean(0))
            dgeo = dict(o=_mv['origin'], ax=_ax, apo=float((_N0 @ _mv['origin'] + _C0).min()),
                        rv=float(np.linalg.norm(_q - np.outer(_q @ _ax, _ax), axis=1).max()))
        except (ValueError, OSError, KeyError, SystemExit) as e:
            tech.append(f'벽 기하 불가: {e}')
            spec = None
    #  ② 회전각의 근거 — mesh 덤프 (전 프레임) > 영수증 > 상·하한
    mesh_dir = os.path.join(run_dir, 'post_mesh')
    mesh_src, receipt, eps = None, None, 0.0
    if spec is not None:
        have = [st for st, _ in win if os.path.isfile(os.path.join(mesh_dir, f'mesh_{st}.stl'))]
        if have and len(have) == len(win):
            mesh_src = mesh_dir
        elif have:
            tech.append(f'mesh 덤프가 창의 일부 프레임에만 있다 ({len(have)}/{len(win)}) — 전부 있거나 없어야 한다 (안 쓴다)')
        if phase_receipt:
            try:
                receipt = load_phase_receipt(phase_receipt, spec)
                eps = float(np.radians(float(receipt['angle_error_deg'])))
            except (ValueError, OSError, KeyError, TypeError) as e:
                tech.append(f'재개-위상 영수증 불가 ({e}) — 영수증 없이 상·하한으로 판정')
    pick = set()
    if spec is not None and diag_fit:
        rot = [st for st, _ in win if mesh_angle(spec, 'Drum', st) > 0]
        base = rot if rot else [win[0][0]]
        pick = {base[int(round(i * (len(base) - 1) / max(PHASE_FRAMES - 1, 1)))] for i in range(min(PHASE_FRAMES, len(base)))}
    ids0 = cnt0 = attr0 = None
    for k, (st, path) in enumerate(win):
        hs, hn = dump_header(path)
        D = read_dump(path)
        P = np.c_[D['x'], D['y'], D['z']]
        r = D['radius']
        ty = D['type'].astype(int)
        if hs is not None and hs != st:
            tech.append(f'step {st}: 덤프 헤더 TIMESTEP {hs} ≠ 파일명 (복제 · 오명명 의심)')
        if hn is not None and hn != len(r):
            tech.append(f'step {st}: 헤더 원자 수 {hn} ≠ 행 수 {len(r)}')
        cnt = {int(t): int(c) for t, c in zip(*np.unique(ty, return_counts=True))}
        ids = attr = None
        if 'id' in D:
            raw = D['id']
            if not np.all(np.isfinite(raw)) or np.any(raw != np.round(raw)):
                tech.append(f'step {st}: id 가 정수가 아니다')
            order = np.argsort(raw, kind='stable')
            ids = raw[order].astype(np.int64)
            if len(np.unique(ids)) != len(ids):
                reject.append(f'step {st}: id 중복 {len(ids) - len(np.unique(ids))} 개')
            attr = (ty[order], r[order])
        if k == 0:
            ids0, cnt0, attr0 = ids, cnt, attr
            out['counts_t0'] = cnt0
            if n_expected is not None and len(r) != n_expected:
                reject.append(f't₀ 입자 {len(r)} ≠ 계획 {n_expected}')
            if expect_counts is not None and {int(a): int(b) for a, b in expect_counts.items()} != cnt0:
                reject.append(f't₀ 상별 입자 수 {cnt0} ≠ 계획 {expect_counts}')
            if ids is None:
                tech.append('덤프에 id 열이 없다 — id 보존을 확인할 수 없다')
        else:
            if cnt != cnt0:
                reject.append(f'step {st}: 상별 입자 수 {cnt} ≠ t₀ {cnt0}')
            elif ids is not None and ids0 is not None and not np.array_equal(ids, ids0):
                reject.append(f'step {st}: id 집합이 t₀ 와 다르다 (수 {len(ids)} vs {len(ids0)})')
            elif attr is not None and attr0 is not None:
                nt, nr = int((attr[0] != attr0[0]).sum()), int((attr[1] != attr0[1]).sum())
                if nt or nr:
                    reject.append(f'step {st}: id 별 type/radius 가 t₀ 와 다르다 (type {nt} 개 · radius {nr} 개) — '
                                  '상별 수와 id 집합이 같아도 입자 속성은 보존되지 않았다')
        pr, rel, n_intra = contacts(P, r, D.get('mol'), types=ty)
        #  판정은 등록 문구대로 **최대**다.  분위수 · 넘은 비율은 기술 보고 (한도 해석은 런 결과를 보기 전에만 정한다)
        row = dict(step=int(st), n=int(len(r)), n_contact=int(len(pr)), n_intra=n_intra,
                   pp_max=float(rel.max()) if len(rel) else 0.0, pp_n_over=int((rel > max_ovl).sum()),
                   pp_p99=float(np.percentile(rel, 99)) if len(rel) else 0.0,
                   pp_p999=float(np.percentile(rel, 99.9)) if len(rel) else 0.0,
                   pp_median=float(np.median(rel)) if len(rel) else 0.0)
        if len(rel):
            ti, tj = ty[pr[:, 0]], ty[pr[:, 1]]
            lo, hi = np.minimum(ti, tj), np.maximum(ti, tj)
            for a_, b_ in set(zip(lo.tolist(), hi.tolist())):
                m_ = (lo == a_) & (hi == b_)
                key = f'{a_}-{b_}'
                out['pp_max_by_pair'][key] = max(out['pp_max_by_pair'].get(key, float('-inf')), float(rel[m_].max()))
            j = int(np.argmax(rel))
            if rel[j] > out['pp_max']:
                out.update(pp_max=float(rel[j]), pp_max_step=int(st), pp_max_types=f'{lo[j]}-{hi[j]}')
        elif out['pp_max'] < 0:
            out['pp_max'] = 0.0
        if spec is not None:
            if mesh_src:
                N, C, owner, _ = container_from_stl(os.path.join(mesh_src, f'mesh_{st}.stl'), spec)
            else:
                N, C, owner, _ = container_at(run_dir, spec, st)
            wr, wk = wall_overlaps(P, r, N, C)
            if receipt is not None and eps > 0 and not mesh_src:      # 영수증의 각 오차를 전파 — ±ε 에서도 재서 최댓값
                for sg in (-1.0, 1.0):
                    N2, C2, _, _ = container_at(run_dir, spec, st, dtheta=sg * eps)
                    wr2, wk2 = wall_overlaps(P, r, N2, C2)
                    m_ = wr2 > wr
                    wr, wk = np.where(m_, wr2, wr), np.where(m_, wk2, wk)
            is_cap = np.array([o_ != 'Drum' for o_ in owner])
            cap_rel = (r - (P @ N[is_cap].T + C[is_cap]).min(1)) / r if is_cap.any() else np.full(len(r), -np.inf)
            q_ = P - dgeo['o']
            rho = np.linalg.norm(q_ - np.outer(q_ @ dgeo['ax'], dgeo['ax']), axis=1)
            #  드럼 δ/r 의 회전각-무관 상·하한 — 면 한가운데(변심거리) 가 입자 쪽을 향할 때가 최악, 꼭짓점이면 최선
            wtouch = wr[wr > 0]
            row.update(wall_max=float(wr.max()), wall_n_over=int((wr > max_ovl).sum()),
                       wall_n_touch=int(len(wtouch)),
                       wall_p999=float(np.percentile(wtouch, 99.9)) if len(wtouch) else 0.0,
                       cap_max=float(cap_rel.max()),
                       drum_worst=float(((rho + r - dgeo['apo']) / r).max()),
                       drum_best=float(((rho + r - dgeo['rv']) / r).max()))
            for t_ in np.unique(ty):
                key = str(int(t_))
                out['wall_max_by_type'][key] = max(out['wall_max_by_type'].get(key, float('-inf')), float(wr[ty == t_].max()))
            j = int(np.argmax(wr))
            if wr[j] > out['wall_max']:
                out.update(wall_max=float(wr[j]), wall_max_step=int(st), wall_max_type=int(ty[j]),
                           wall_max_mesh=owner[int(wk[j])])
            if st in pick:
                out['phase'].append(infer_drum_phase(P, r, run_dir, spec, st, max_ovl))
        out['per_frame'].append(row)
        if progress:
            print(f'   … {os.path.basename(run_dir.rstrip("/"))} step {st}  pp {row["pp_max"]*100:6.3f} %'
                  + (f'  벽 {row["wall_max"]*100:6.3f} %' if 'wall_max' in row else ''), flush=True)
    if out['pp_max'] > max_ovl:
        n_over = sum(r_['pp_n_over'] for r_ in out['per_frame'])
        reject.append(f'입자–입자 최대 δ/r_min {out["pp_max"]*100:.3f} % > {max_ovl*100:g} % '
                      f'(step {out["pp_max_step"]} · 타입 {out["pp_max_types"]} · 넘은 접촉 {n_over} 건/창)')
    if spec is not None:
        pf = out['per_frame']
        cap = max(r_['cap_max'] for r_ in pf)
        worst = max(max(r_['drum_worst'] for r_ in pf), cap)
        best = max(max(r_['drum_best'] for r_ in pf), cap)
        out.update(wall_bound_worst=worst, wall_bound_best=best)
        if out['phase']:
            out['phase_note'] = '진단 — 입자 배치로 되읽은 회전각 (증거 아님 · 판정에 안 씀 · HBR2-01)'
        over = None
        if mesh_src is not None:
            out['phase_status'], out['wall_basis'] = 'mesh-dump', 'post_mesh/ 덤프 = 독립 기하 (창 전 프레임)'
            over = out['wall_max'] > max_ovl
        elif receipt is not None:
            out['phase_status'] = 'receipt'
            out['wall_basis'] = (f'예정각 ± {receipt["angle_error_deg"]}° (재개-위상 영수증 {os.path.basename(phase_receipt)} · '
                                 f'바이너리 {str(receipt["binary_sha256"])[:12]}…)')
            over = out['wall_max'] > max_ovl
        elif worst <= max_ovl:
            out['phase_status'] = 'bounded'      # 근거 없어도 어느 회전각이어도 한도 안
            out['wall_basis'] = f'회전각-무관 상한 {worst*100:.3f} % ≤ {max_ovl*100:g} %'
        elif best > max_ovl:
            out['phase_status'] = 'bounded'      # 근거 없어도 어느 회전각이어도 한도 밖
            out['wall_basis'] = f'회전각-무관 하한 {best*100:.3f} % > {max_ovl*100:g} %'
            reject.append(f'벽 δ/r 가 **어느 회전각이어도** {best*100:.3f} % 이상 > {max_ovl*100:g} %')
        else:
            out['phase_status'], out['wall_basis'] = 'unidentified', '없음'
            tech.append(f'드럼 회전각의 독립 근거가 없고 (post_mesh/ 덤프 · 재개-위상 영수증 없음) 벽 δ/r 가 각에 따라 '
                        f'{best*100:.2f}–{worst*100:.2f} % — 한도 {max_ovl*100:g} % 판정 불가.  '
                        f'예정각으로 잰 {out["wall_max"]*100:.3f} % 는 미검증 (판정에 안 씀)')
        if over:
            n_over = sum(r_.get('wall_n_over', 0) for r_ in pf)
            reject.append(f'벽 최대 δ/r {out["wall_max"]*100:.3f} % > {max_ovl*100:g} % (step {out["wall_max_step"]} · '
                          f'타입 {out["wall_max_type"]} · {out["wall_max_mesh"]} · 넘은 접촉 {n_over} 건/창 · 근거 {out["phase_status"]})')
    elif walls:
        out['phase_status'] = 'no_walls'
    out['verdict'] = 'REJECT' if reject else ('TECH' if tech else 'PASS')
    return out


def report_window(rs):
    print(f'{"런":22s} {"창 (step)":>21s} {"프레임":>6s}  {"입자–입자 최대":>14s}  {"벽 최대":>9s}  {"회전각":>9s}  판정')
    for m in rs:
        w = m['window'] or ('-', '-')
        pp = f'{m["pp_max"]*100:.3f} %' if np.isfinite(m['pp_max']) else '—'
        wl = f'{m["wall_max"]*100:.3f} %' if np.isfinite(m['wall_max']) else '—'
        print(f'{os.path.basename(str(m["label"]).rstrip("/")):22s} {w[0]:>10} – {w[1]:<9} {m["n_frames"]:6d}  '
              f'{pp:>14s}  {wl:>9s}  {m["phase_status"]:>9s}  {m["verdict"]}')
        for b in m['reject']:
            print(f'{"":22s}   ⛔ {b}')
        for b in m['tech']:
            print(f'{"":22s}   ⚠ TECH {b}')
    n_bad = sum(m['verdict'] != 'PASS' for m in rs)
    if n_bad:
        print(f'\n⛔ {n_bad} 런이 계약 (최대 겹침 ≤ {CONTRACT_MAX_OVL*100:g} % · 벽 포함 · 상별 보존) 을 통과하지 못했다 — '
              f'판정에 쓰지 않는다.  TECH 는 검사 자체가 서지 않은 것 (통과 아님).')
    return 1 if n_bad else 0


def report(rs):
    print(f'{"팔":14s} {"n":>6s} {"CN":>5s}  겹침 δ/r_min  중앙/90 %/최대      손실   강체내부   판정')
    for m in rs:
        v = '⛔ 기각' if m['reject'] else ('⚠ 경고' if m['ovl_med'] > OVL_MEDIAN_WARN else '✓')
        print(f'{m["label"]:14s} {m["n"]:6d} {m["cn"]:5.2f}  '
              f'{m["ovl_med"]*100:6.2f} / {m["ovl_p90"]*100:6.2f} / {m["ovl_max"]*100:7.1f} %'
              f'  {m["lost_pct"]:5.1f} %  {m.get("n_intra", 0):7d}   {v}')
        for b in m['reject']:
            print(f'{"":14s}   ⛔ {b}')
    if any(m['reject'] for m in rs):
        print('\n⛔ 기각된 팔이 있다 — 그 팔의 H/R 은 접촉모델이 푼 값이 아니다.  인용 금지.')
    return 1 if any(m['reject'] for m in rs) else 0


def _selftest():
    import tempfile
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)
        print(('  PASS  ' if cond else '  FAIL  ') + name)

    def write(td, pts, name='t_100.liggghts'):
        with open(os.path.join(td, name), 'w') as fh:
            fh.write(f'ITEM: TIMESTEP\n100\nITEM: NUMBER OF ATOMS\n{len(pts)}\n')
            fh.write('ITEM: BOX BOUNDS mm mm mm\n-1 1\n-1 1\n-1 1\n')
            fh.write('ITEM: ATOMS id type x y z radius\n')
            for i, (X, Y, Z, R) in enumerate(pts):
                fh.write(f'{i+1} 1 {X} {Y} {Z} {R}\n')

    R = 0.001
    with tempfile.TemporaryDirectory() as td:               # 겹침 정확히 10 %
        write(td, [(0, 0, 0, R), (0.0019, 0, 0, R)])
        m = check(td)
        chk('① 겹침 δ/r 을 정확히 낸다 (설계 10 %)', abs(m['ovl_max'] - 0.10) < 1e-9)
        chk('② 10 % 는 기각이 아니다 (경고 영역)', not m['reject'])
    with tempfile.TemporaryDirectory() as td:               # 통과 — 중심이 반대편
        write(td, [(0, 0, 0, R), (0.0002, 0, 0, R)])
        m = check(td)
        chk(f'③ 통과(δ/r {m["ovl_max"]*100:.0f} %)를 **기각**한다', bool(m['reject']))
    with tempfile.TemporaryDirectory() as td:               # 닿지 않음
        write(td, [(0, 0, 0, R), (0.01, 0, 0, R)])
        m = check(td)
        chk('④ 안 닿으면 접촉 0 · 기각 없음',
            m['n_contact'] == 0 and not m['reject'] and m['ovl_max'] == 0.0)
    with tempfile.TemporaryDirectory() as td:               # 원자 손실
        write(td, [(0, 0, 0, R), (0.01, 0, 0, R)])
        m = check(td, n_expected=100)
        chk(f'⑤ 원자 손실을 기각한다 ({m["lost_pct"]:.0f} % 잃음)', bool(m['reject']))
    with tempfile.TemporaryDirectory() as td:               # ★ 변이 — 다분산에서 작은 쪽 기준
        write(td, [(0, 0, 0, 0.01), (0.0105, 0, 0, 0.001)])
        m = check(td)
        #  δ = 0.011 − 0.0105 = 0.0005 ;  r_min = 0.001 → 50 %  (큰 쪽 기준이면 5 %)
        chk(f'⑥ 변이: 겹침을 **작은 쪽 반경**으로 잰다 (50 %, 큰 쪽이면 5 %)',
            abs(m['ovl_max'] - 0.50) < 1e-9)
    #  ★★ ⑦ 강체 내부 쌍 — **실제로 검사를 멀게 했던 결함** (2026-09-19)
    #     섬유 사슬은 설계상 δ/r = 0.4 로 겹쳐 있다.  그것을 접촉으로 세면 다섯 팔
    #     전부가 "최대 40.0 %" 를 내놓고 40~50 % 구간의 진짜 통과를 못 본다.
    def write_mol(td, rows):
        with open(os.path.join(td, 'm_100.liggghts'), 'w') as fh:
            fh.write(f'ITEM: TIMESTEP\n100\nITEM: NUMBER OF ATOMS\n{len(rows)}\n')
            fh.write('ITEM: BOX BOUNDS mm mm mm\n-1 1\n-1 1\n-1 1\n')
            fh.write('ITEM: ATOMS id type mol x y z radius\n')
            for i, (ty, mo, X, Y, Z, RR) in enumerate(rows):
                fh.write(f'{i+1} {ty} {mo} {X} {Y} {Z} {RR}\n')
    with tempfile.TemporaryDirectory() as td:
        #  강체 2구는 40 % 겹침(mol 7) · 평범한 구 2개는 mol −1 로 5 % 겹침
        #  강체쌍: 중심거리 0.0016 → δ = 0.0004 → δ/r = 40 % (섬유 사슬과 같은 값)
        #  평구쌍: 중심거리 0.00195 → δ = 0.00005 → δ/r = 5 %
        write_mol(td, [(4, 7, 0.0, 0, 0, R), (4, 7, 0.0016, 0, 0, R),
                       (1, -1, 0.01, 0, 0, R), (1, -1, 0.01195, 0, 0, R)])
        m = check(td)
        chk(f'⑦ 강체 내부 쌍(40 %)을 빼고 잰다 (남은 최대 {m["ovl_max"]*100:.0f} %)',
            abs(m['ovl_max'] - 0.05) < 1e-9 and m['n_intra'] == 1 and m['n_contact'] == 1)
        #  ★ 변이 — mol>0 조건이 없으면 평범한 구 쌍(mol −1 끼리)도 지워진다
        import numpy as _np
        P = _np.array([[0., 0, 0], [0.01, 0, 0], [0.01195, 0, 0]])
        rr = _np.array([R, R, R])
        mol_all = _np.array([-1., -1., -1.])
        _, rel_ok, _ = contacts(P, rr, mol_all)
        chk('⑦b 변이: mol = −1 끼리는 **같은 강체가 아니다** (평범한 구를 지우지 않는다)',
            len(rel_ok) == 1)

    # ══ ⑧~⑭ 2026-09-27 Codex HB-05 — 등록 계약 *"최대 겹침 실측 ≤ 1 %"* (prereg mixer_layered §1) 를 **실제로** 강제하나 ══
    #   옛 check() = 마지막 프레임 하나 · 기각선 50 % · 벽 없음 · 상별 보존 없음.  아래는 그 넷이 새는 자리를 **재현**한다.
    import math as _m
    rng = np.random.default_rng(11)

    def _stl(path, tris):
        with open(path, 'w') as fh:
            fh.write('solid t\n')
            for a_, b_, c_ in tris:
                nv = np.cross(np.subtract(b_, a_), np.subtract(c_, a_))
                nv = nv / (np.linalg.norm(nv) or 1.0)
                fh.write(f' facet normal {nv[0]:.6e} {nv[1]:.6e} {nv[2]:.6e}\n  outer loop\n')
                for v in (a_, b_, c_):
                    fh.write(f'   vertex {v[0]:.9e} {v[1]:.9e} {v[2]:.9e}\n')
                fh.write('  endloop\n endfacet\n')
            fh.write('endsolid t\n')

    NP_, RV_, XH_, SC_ = 12, 0.5, 0.2, 0.02           # STL 단위 (튜토리얼 Mixer 꼴) · scale → 반경 0.01 m · 반길이 0.004 m
    APO = RV_ * SC_ * _m.cos(_m.pi / NP_)              # 변심거리 (면 한가운데까지의 거리)

    def _geom(td):
        ang = [2 * _m.pi * k / NP_ + _m.pi / NP_ for k in range(NP_)]     # 꼭짓점 15°, 45°, … ⇒ 면 법선 0°, 30°, …
        vs = [(RV_ * _m.cos(a_), RV_ * _m.sin(a_)) for a_ in ang]
        drum = []
        for k in range(NP_):
            (y0, z0), (y1, z1) = vs[k], vs[(k + 1) % NP_]
            drum += [((-XH_, y0, z0), (XH_, y0, z0), (XH_, y1, z1)),
                     ((-XH_, y0, z0), (XH_, y1, z1), (-XH_, y1, z1))]
        _stl(os.path.join(td, 'Drum.stl'), drum)
        for nm, xc in (('Front.stl', XH_), ('Back.stl', -XH_)):
            _stl(os.path.join(td, nm), [((xc, 0, 0), (xc, *vs[k]), (xc, *vs[(k + 1) % NP_])) for k in range(NP_)])

    def _deck(period=0.012):
        return ('timestep 1e-6\n'
                f'fix Drum  all mesh/surface file Drum.stl  type 4 scale {SC_}\n'
                f'fix Front all mesh/surface file Front.stl type 4 scale {SC_}\n'
                f'fix Back  all mesh/surface file Back.stl  type 4 scale {SC_}\n'
                'fix walls all wall/gran model hertz tangential history cohesion sjkr rolling_friction cdt &\n'
                '    mesh n_meshes 3 meshes Drum Front Back\n'
                'run 1\n'
                'dump dmp all custom 500 post/mix_*.liggghts id type x y z radius\n'
                'run 1000\nrun 1000\n'
                f'fix mvD all move/mesh mesh Drum  rotate origin 0 0 0 axis 1. 0. 0. period {period}\n'
                f'fix mvF all move/mesh mesh Front rotate origin 0 0 0 axis 1. 0. 0. period {period}\n'
                f'fix mvB all move/mesh mesh Back  rotate origin 0 0 0 axis 1. 0. 0. period {period}\n'
                'run 12000\n')

    def _dump(run_, step, rows):
        with open(os.path.join(run_, 'post', f'mix_{step}.liggghts'), 'w') as fh:
            fh.write(f'ITEM: TIMESTEP\n{step}\nITEM: NUMBER OF ATOMS\n{len(rows)}\n'
                     'ITEM: BOX BOUNDS ff ff ff\n-1 1\n-1 1\n-1 1\nITEM: ATOMS id type x y z radius\n')
            for (i_, t_, X, Y, Z, RR) in rows:
                fh.write(f'{i_} {t_} {X:.12g} {Y:.12g} {Z:.12g} {RR:.12g}\n')

    def _run(td, period=0.012):
        run_ = os.path.join(td, 'run')
        os.makedirs(os.path.join(run_, 'post'))
        _geom(run_)
        open(os.path.join(run_, 'in.mixer'), 'w').write(_deck(period))
        return run_

    def _mesh_dump(run_, step, theta):
        """LIGGGHTS `dump mesh/stl` 흉내 — 참 회전각 theta 로 돌린 드럼·끝판 삼각형 (시뮬레이션 단위) 을 post_mesh/mesh_<step>.stl 에."""
        os.makedirs(os.path.join(run_, 'post_mesh'), exist_ok=True)
        Rm = _rot(np.array([1.0, 0, 0]), theta)
        tris = []
        for nm in ('Drum.stl', 'Front.stl', 'Back.stl'):
            for t_ in read_stl(os.path.join(run_, nm)) * SC_:
                tris.append(tuple(map(tuple, t_ @ Rm.T)))
        _stl(os.path.join(run_, 'post_mesh', f'mesh_{step}.stl'), tris)

    #  바탕 입자 넷 (서로 · 벽과 안 닿는다) + 짝 둘 (id 5·6) — 프레임마다 짝 간격만 바꾼다
    BASE = [(1, 1, 0.0, 0.0, 0.0, 1e-3), (2, 2, 0.0, 0.004, 0.0, 5e-4),
            (3, 3, 0.0, -0.004, 0.002, 2e-4), (4, 3, 0.001, -0.004, -0.002, 2e-4)]

    def _pair(gap_y):
        return [(5, 1, 0.0, 0.0, -0.005, 1e-3), (6, 1, 0.0, gap_y, -0.005, 1e-3)]

    TH2500 = 2 * _m.pi * (2500 - 2001) / 12000        # 회전 시작 = run 1 + 1000 + 1000 = 2001 스텝

    with tempfile.TemporaryDirectory() as td:
        run = _run(td)
        #  ★ Codex 반례 그대로: 반경 1 mm 두 구 · 중심 간격 1.98 mm ⇒ δ/r 2 % — **가운데 프레임에만**
        _dump(run, 2000, BASE + _pair(0.0025))
        _dump(run, 2500, BASE + _pair(0.00198))
        _dump(run, 3000, BASE + _pair(0.0025))
        old = check(os.path.join(run, 'post'))
        chk('⑧ 재현: 옛 check() 는 가운데 프레임의 2 % 겹침을 **못 본다** (마지막 프레임만 · 기각선 50 %)',
            not old['reject'] and old['ovl_max'] == 0.0)
        w = check_window(run)
        chk(f'⑧b ★ 계약 판정은 분석 창 전 프레임을 보고 2 % 를 기각한다 '
            f'(최대 {w["pp_max"]*100:.2f} % @ step {w["pp_max_step"]})',
            w['verdict'] == 'REJECT' and abs(w['pp_max'] - 0.02) < 1e-6 and w['pp_max_step'] == 2500
            and w['window'] == (2000, 3000) and w['n_frames'] == 3)
    with tempfile.TemporaryDirectory() as td:
        run = _run(td)
        for st in (2000, 2500, 3000):
            _dump(run, st, BASE + _pair(0.0025))
        w = check_window(run)
        chk(f'⑨ 겹침 없는 창은 통과한다 (판정 {w["verdict"]} · 위상 확인 {w["phase_status"]})',
            w['verdict'] == 'PASS' and w['pp_max'] <= 0.0 and w['wall_max'] < 0)
    #  ⑩ 벽 — 드럼은 **다각형**이고 돈다.  회전된 면에 2 % 박힌 입자를 둔다
    def _on_facet(theta, k, r_, ovl, u=0.0, x=0.0):
        """회전각 theta 인 드럼의 면 k 에 δ/r = ovl 로 닿은 입자 중심 (u = 면 방향 오프셋, m)."""
        ph = 2 * _m.pi * k / NP_ + theta
        nrm = np.array([_m.cos(ph), _m.sin(ph)]); tng = np.array([-_m.sin(ph), _m.cos(ph)])
        yz = (APO - r_ + ovl * r_) * nrm + u * tng
        return (x, float(yz[0]), float(yz[1]))
    def _th(st):
        return 0.0 if st <= 2001 else 2 * _m.pi * (st - 2001) / 12000

    def _bed(theta):
        """면마다 6 알씩 δ/r 0.1 % 로 얹힌 침대 — 회전각을 데이터로 되읽을 수 있게 (실제 런은 침대가 벽에 늘 닿아 있다)."""
        rows, i_ = [], 100
        half = APO * _m.tan(_m.pi / NP_)
        for k in range(NP_):
            for u in np.linspace(-0.8, 0.8, 6) * half:
                rows.append((i_, 3, *_on_facet(theta, k, 2e-4, 0.001, u=u, x=float(rng.uniform(-0.003, 0.003))), 2e-4))
                i_ += 1
        return rows
    with tempfile.TemporaryDirectory() as td:
        run = _run(td)
        for st in (2000, 2500, 3000):
            ov7 = 0.02 if st == 2500 else -0.5
            _dump(run, st, BASE + _pair(0.0025) + _bed(_th(st)) + [(7, 3, *_on_facet(_th(st), 3, 2e-4, ov7), 2e-4)])
        w = check_window(run)
        chk(f'⑩ ★ 독립 기하 없이는 회전된 면의 2 % 도 기각 못 한다 — 상·하한 [{w["wall_bound_best"]*100:.0f}, {w["wall_bound_worst"]*100:.0f}] % '
            f'가 1 % 를 양쪽에서 걸친다 ⇒ TECH (예정각 값 {w["wall_max"]*100:.2f} % 는 미검증 · 판정에 안 씀)',
            w['verdict'] == 'TECH' and w['phase_status'] == 'unidentified' and abs(w['wall_max'] - 0.02) < 1e-6)
        for st in (2000, 2500, 3000):
            _mesh_dump(run, st, _th(st))
        w = check_window(run)
        chk(f'⑩c ★ mesh 덤프 (독립 기하) 가 있으면 회전된 드럼 면에 2 % 박힌 입자를 기각한다 (벽 최대 {w["wall_max"]*100:.2f} % @ {w["wall_max_step"]} · '
            f'{w["wall_max_mesh"]} · 근거 {w["phase_status"]})',
            w['verdict'] == 'REJECT' and abs(w['wall_max'] - 0.02) < 1e-6 and w['wall_max_step'] == 2500
            and w['wall_max_mesh'] == 'Drum' and w['phase_status'] == 'mesh-dump')
        #  ⚠ 위상을 틀리게(0) 두면 **같은 입자가 안 닿은 것으로** 보인다 — 위상이 판정을 좌우한다
        spec = deck_walls(open(os.path.join(run, 'in.mixer')).read())
        P7 = np.array([_on_facet(TH2500, 3, 2e-4, 0.02)])
        ov_right, _ = wall_overlaps(P7, np.array([2e-4]), *container_at(run, spec, 2500)[:2])
        ov_wrong, _ = wall_overlaps(P7, np.array([2e-4]), *container_at(run, spec, 2001)[:2])
        chk(f'⑩b 변이: 위상 0 으로 두면 같은 2 % 가 {ov_wrong[0]*100:.1f} % 로 보인다 (위상을 스텝에서 계산해야 하는 이유)',
            abs(ov_right[0] - 0.02) < 1e-6 and ov_wrong[0] < 0.0)
    with tempfile.TemporaryDirectory() as td:                   # ⑪ 끝판 (x = ±반길이) 겹침
        run = _run(td)
        xh = XH_ * SC_
        for st in (2000, 2500, 3000):
            _dump(run, st, BASE + _pair(0.0025) + [(7, 3, xh - 0.98 * 2e-4, 0.0, 0.003, 2e-4)])
        w = check_window(run)
        chk(f'⑪ 끝판에 2 % 박힌 입자를 기각한다 (벽 최대 {w["wall_max"]*100:.2f} % · {w["wall_max_mesh"]})',
            w['verdict'] == 'REJECT' and abs(w['wall_max'] - 0.02) < 1e-6 and w['wall_max_mesh'] == 'Front')
    with tempfile.TemporaryDirectory() as td:                   # ⑫ 상별 보존 — 잃음 · 타입 바뀜
        run = _run(td)
        _dump(run, 2000, BASE + _pair(0.0025))
        _dump(run, 2500, BASE[:3] + _pair(0.0025))                                    # id 4 소실
        _dump(run, 3000, BASE[:3] + [(4, 2, 0.001, -0.004, -0.002, 2e-4)] + _pair(0.0025))   # 돌아왔는데 타입이 2
        w = check_window(run, n_expected=6)
        chk(f'⑫ ★ 창 안에서 입자를 잃거나 상이 바뀌면 기각한다 ({"; ".join(w["reject"])[:90]})',
            w['verdict'] == 'REJECT' and any('2500' in b for b in w['reject'])
            and any('3000' in b for b in w['reject']))
    #  ⑬ 되읽기 (입자 배치에서 회전각 fitting) 는 **진단일 뿐 증거가 아니다** (Codex HBR2-01 — ⑮ 가 그 반례) — 판정에 안 쓴다.
    #     면을 따라 넓게 깔린 침대 (실제 런) 는 꼭짓점 쪽 알의 최악 겹침이 크므로 근거 없이는 늘 unidentified 다 — 그래서
    #     실제 런의 벽 판정은 영수증 (또는 mesh 덤프) 이 있어야 나온다.
    import json as _json

    def _receipt(td, period=0.012, ok=True, err=0.01):
        p_ = os.path.join(td, 'receipt.json')
        _json.dump(dict(test='restart_phase', passed=ok, period=period, axis=[1.0, 0.0, 0.0], angle_error_deg=err,
                        binary_sha256='0' * 64, liggghts_version='test', date='2026-09-27'), open(p_, 'w'))
        return p_
    with tempfile.TemporaryDirectory() as td:
        run = _run(td)
        for st in (2000, 2500, 3000):
            _dump(run, st, BASE + _pair(0.0025) + _bed(_th(st)))
        w = check_window(run, diag_fit=True)
        ph = [p_ for p_ in w['phase'] if p_['step'] == 2500][0]
        chk(f'⑬ 면을 따라 깔린 침대 (0.1 %) 는 근거 없이는 unidentified (상·하한 {w["wall_bound_best"]*100:.0f}–{w["wall_bound_worst"]*100:.0f} %) '
            f'— 되읽기 진단은 각을 맞히지만 (차 {_m.degrees(ph["dtheta"]):.4f}°) 판정에 쓰지 않는다',
            w['verdict'] == 'TECH' and w['phase_status'] == 'unidentified' and abs(ph['dtheta']) < _m.radians(0.05)
            and w['phase_note'].startswith('진단'))
        w2 = check_window(run, diag_fit=True, phase_receipt=_receipt(td))
        chk(f'⑬b 영수증이 있으면 같은 침대가 예정각으로 판정된다 (receipt · 벽 최대 {w2["wall_max"]*100:.3f} % → PASS)',
            w2['verdict'] == 'PASS' and w2['phase_status'] == 'receipt' and 0 < w2['wall_max'] < 0.003)
        #  ⚠ 변이 — 덱의 주기를 바꾸면 영수증이 안 맞아 (주기 ≠) 영수증을 버린다 · 진단은 mismatch — 어느 쪽도 통과로 새지 않는다
        open(os.path.join(run, 'in.mixer'), 'w').write(_deck(period=0.024))
        w3 = check_window(run, diag_fit=True, phase_receipt=_receipt(td))
        chk('⑬c 변이: 덱 주기 ≠ 영수증 주기 → 영수증 기각 (TECH) · 진단은 mismatch 를 적는다 — fitting 으로 구제하지 않는다',
            w3['verdict'] == 'TECH' and w3['phase_status'] == 'unidentified' and any('영수증' in t for t in w3['tech'])
            and any(p_['status'] == 'mismatch' for p_ in w3['phase']))
        w4 = check_window(run)
        chk('⑬d 기본 (--diag-fit 없음) 은 되읽기를 아예 안 돌린다 (phase = [])', w4['phase'] == [] and w4['verdict'] == 'TECH')
    with tempfile.TemporaryDirectory() as td:                   # ⑬c 벽 근처 입자가 한 알 (꼭짓점 옆) → 되읽기 불가
        run = _run(td)
        half_ = APO * _m.tan(_m.pi / NP_)
        for st in (2000, 2500, 3000):
            _dump(run, st, BASE + _pair(0.0025) + [(7, 3, *_on_facet(_th(st), 2, 2e-4, 0.005, u=0.9 * half_), 2e-4)])
        w = check_window(run)
        chk(f'⑬c 회전각 미확인 · 각에 따라 δ/r {w["wall_bound_best"]*100:.0f}–{w["wall_bound_worst"]*100:.0f} % '
            f'(참 0.5 %) ⇒ TECH (통과로 새지 않는다)',
            w['verdict'] == 'TECH' and w['phase_status'] == 'unidentified')
    #  ⑭ 타입쌍별 격자 검색 = 전수 검색 (다분산에서 2·r_max 전수는 10 만 입자에 수천만 쌍이다)
    Pr = rng.uniform(0, 0.01, (400, 3)); tr = rng.integers(1, 4, 400)
    rr = np.choose(tr - 1, [8e-4, 3e-4, 1e-4])
    a1, r1, _ = contacts(Pr, rr)
    a2, r2, _ = contacts(Pr, rr, types=tr)
    s1 = sorted(zip(map(tuple, np.sort(a1, axis=1)), np.round(r1, 12)))
    s2 = sorted(zip(map(tuple, np.sort(a2, axis=1)), np.round(r2, 12)))
    chk(f'⑭ 타입쌍별 격자 검색이 전수 검색과 같은 접촉 집합을 낸다 ({len(s1)} 쌍)', s1 == s2 and len(s1) > 10)

    # ══ ⑮~⑲ 2026-09-27 저녁 Codex 재리뷰 HBR2-01 · 03 · 08 — 합성 반례를 **먼저 재현**하고 고쳤다 ══════════════════
    #   (docs/reviews/codex_mixer_highbo_rereview_evidence_20260927/review_probe.py 의 경우들을 이 12 각형 시험 기하로 옮김)
    HALF = _m.pi / NP_                                   # 반 면각 — 참 벽이 예정보다 이만큼 어긋난 반례

    def _ring(theta, ovl, r_=2e-4):
        """면마다 한 알 — 참 회전각 theta 인 드럼의 면 한가운데에 δ/r = ovl 로 (알끼리는 안 닿는다)."""
        return [(200 + k, 3, *_on_facet(theta, k, r_, ovl), r_) for k in range(NP_)]
    with tempfile.TemporaryDirectory() as td:            # ⑮ HBR2-01 반례 1 — 참 벽 겹침 2 % · 위상이 예정보다 반 면각 어긋남 · 증거 없음
        run = _run(td)
        for st in (2000, 2500, 3000):
            _dump(run, st, BASE + _pair(0.0025) + _ring(_th(st) + HALF, 0.02))
        w = check_window(run)
        chk(f'⑮ ★ HBR2-01 재현→수정: 참 벽 겹침 2 % 가 예정각에서는 {w["wall_max"]*100:.0f} % (안 닿음) 로 보인다 — 증거 없이는 PASS 를 주지 않는다 '
            f'({w["verdict"]} · {w["phase_status"]} · 상한 {w["wall_bound_worst"]*100:.1f} %)',
            w['verdict'] == 'TECH' and w['phase_status'] == 'unidentified' and w['wall_max'] < 0
            and abs(w['wall_bound_worst'] - 0.02) < 1e-6 and not w['phase'])
        for st in (2000, 2500, 3000):
            _mesh_dump(run, st, _th(st) + HALF)
        w2 = check_window(run)
        chk(f'⑮b 독립 기하 (post_mesh/ 덤프) 를 주면 그 벽으로 재서 2 % 를 기각한다 ({w2["phase_status"]} · {w2["wall_max"]*100:.2f} %)',
            w2['verdict'] == 'REJECT' and w2['phase_status'] == 'mesh-dump' and abs(w2['wall_max'] - 0.02) < 1e-6)
        os.remove(os.path.join(run, 'post_mesh', 'mesh_2500.stl'))
        w3 = check_window(run)
        chk('⑮c mesh 덤프가 창의 일부 프레임에만 있으면 쓰지 않는다 (TECH)',
            w3['verdict'] == 'TECH' and w3['phase_status'] == 'unidentified' and any('mesh' in t for t in w3['tech']))
    with tempfile.TemporaryDirectory() as td:            # ⑯ 반례 2 — 참 = 예정 · 0.5 % : 옛 되읽기는 이것을 TECH (5/5 mismatch) 로 막았다
        run = _run(td)
        for st in (2000, 2500, 3000):
            _dump(run, st, BASE + _pair(0.0025) + _ring(_th(st), 0.005))
        w = check_window(run)
        chk(f'⑯ 참 위상 = 예정 · 0.5 %: 어느 회전각이어도 ≤ 1 % 라 PASS (bounded · 상한 {w["wall_bound_worst"]*100:.2f} %)',
            w['verdict'] == 'PASS' and w['phase_status'] == 'bounded')
        w2 = check_window(run, phase_receipt=_receipt(td))
        chk(f'⑯b 재개-위상 영수증이 있으면 예정각 (±오차) 으로 잰다 (receipt · 벽 최대 {w2["wall_max"]*100:.3f} %)',
            w2['verdict'] == 'PASS' and w2['phase_status'] == 'receipt' and abs(w2['wall_max'] - 0.005) < 2e-4)
        w3 = check_window(run, phase_receipt=_receipt(td, period=0.024))
        chk('⑯c 영수증의 주기가 덱과 다르면 영수증을 쓰지 않는다 (TECH — 상·하한 값은 남긴다)',
            w3['verdict'] == 'TECH' and w3['phase_status'] == 'bounded' and any('영수증' in t for t in w3['tech']))
    with tempfile.TemporaryDirectory() as td:            # ⑰ HBR2-08 — 같은 id 둘의 type 교환 + 한 알 반경 절반 (상별 수 · id 집합은 그대로)
        run = _run(td)
        _dump(run, 2000, BASE + _pair(0.0025))
        mut = [(1, 2) + BASE[0][2:], (2, 1) + BASE[1][2:], BASE[2][:5] + (BASE[2][5] * 0.5,), BASE[3]] + _pair(0.0025)
        _dump(run, 2500, mut)
        _dump(run, 3000, mut)
        w = check_window(run)
        chk(f'⑰ ★ HBR2-08: id 별 type/radius 가 t₀ 와 다르면 기각한다 ({"; ".join(w["reject"])[:80]})',
            w['verdict'] == 'REJECT' and any('type' in b and 'radius' in b for b in w['reject']))
    with tempfile.TemporaryDirectory() as td:            # ⑱ HBR2-03 — 창 안 덤프 결손 (2500 없음): 미관측 구간에 통과 증서를 주지 않는다
        run = _run(td)
        for st in (2000, 3000):
            _dump(run, st, BASE + _pair(0.0025))
        w = check_window(run)
        chk(f'⑱ ★ HBR2-03: 창 안 덤프가 빠지면 TECH ({"; ".join(w["tech"])[:70]})',
            w['verdict'] == 'TECH' and any('결손' in t for t in w['tech']))
        chk('⑱b 관측량 표지 = 저장 프레임 최대 (덤프 사이 peak 미관측, D-1)',
            str(w.get('observable', '')).startswith('snapshot-max'))
    with tempfile.TemporaryDirectory() as td:            # ⑲ 덤프 헤더 step ≠ 파일명 (복제 파일로 수를 채운 경우) → TECH
        run = _run(td)
        for st in (2000, 2500, 3000):
            _dump(run, st, BASE + _pair(0.0025))
        import shutil as _sh
        _sh.copyfile(os.path.join(run, 'post', 'mix_2000.liggghts'), os.path.join(run, 'post', 'mix_2500.liggghts'))
        w = check_window(run)
        chk('⑲ 헤더 step 이 파일명과 다른 덤프 (복제) 는 TECH', w['verdict'] == 'TECH' and any('헤더' in t for t in w['tech']))
    print(f'\ncheck_contact_validity selftest: {ok}/{ok+len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('dirs', nargs='*')
    ap.add_argument('--label', action='append', default=None)
    ap.add_argument('--n-expected', type=int, default=None,
                    help='삽입 계획 원자 수 — 손실 판정에 쓴다')
    ap.add_argument('--contract', action='store_true',
                    help='★ 등록 계약 판정 (런 디렉터리 = in.mixer · post/ · STL): 분석 창 전 프레임 (저장 프레임 최대) · '
                         f'입자–입자와 벽 최대 겹침 ≤ {CONTRACT_MAX_OVL*100:g} %% · 상별 · id 별 속성 보존 · 창 결손 없음 · '
                         '벽 회전각 근거 = post_mesh/ 덤프 > 영수증 > 상·하한')
    ap.add_argument('--phase-receipt', default=None,
                    help='(--contract) 재개-위상 영수증 JSON (scripts/mixer_restart_phase_test.py) — 있으면 벽을 예정각 ± 오차로 잰다')
    ap.add_argument('--expect-types', default=None, help='(--contract) t₀ 상별 입자 수, 예 "1:36,2:421,3:32832"')
    ap.add_argument('--diag-fit', action='store_true',
                    help='(--contract) 입자 배치로 회전각을 되읽는 진단을 같이 낸다 (증거 아님 · 판정에 안 씀)')
    ap.add_argument('--json', default=None, help='(--contract) 결과 JSON 경로')
    ap.add_argument('--progress', action='store_true', help='(--contract) 프레임마다 한 줄')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    if not a.dirs:
        ap.error('디렉터리를 하나 이상 주세요')
    labs = a.label or [None] * len(a.dirs)
    if a.contract:
        ec = None
        if a.expect_types:
            ec = {int(k): int(v) for k, v in (x.split(':') for x in a.expect_types.split(','))}
        rs = [check_window(d, a.n_expected, label=labs[i] if i < len(labs) else None, phase_receipt=a.phase_receipt,
                           expect_counts=ec, diag_fit=a.diag_fit, progress=a.progress)
              for i, d in enumerate(a.dirs)]
        if a.json:
            import json
            json.dump(rs, open(a.json, 'w'), ensure_ascii=False, indent=1, default=float)
            print(f'→ {a.json}')
        raise SystemExit(report_window(rs))
    raise SystemExit(report([check(d, a.n_expected, labs[i] if i < len(labs) else None)
                             for i, d in enumerate(a.dirs)]))
