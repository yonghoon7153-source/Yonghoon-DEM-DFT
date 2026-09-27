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
    회전각을 틀리면 2 % 겹침이 '안 닿음' 으로 숨는다.  각은 덱에서 계산하고, 그 각의 **근거**는 (2026-09-28 Codex 3차 정정)
    ① 그 런의 `post_mesh/` 덤프 (전체 용기 · 예정각과 일치 확인) ② 재개-위상 영수증 v1 (같은 바이너리 · 같은 메시 운동 계약 ·
    판정 step 에서 실측 · 봉인) 뿐이다.  입자 배치로 각을 되읽는 fitting (`--diag-fit`) 은 **진단 전용 — 확인이 아니다**
    (참 겹침 2 % + 반 면각 어긋남을 PASS 로 승격시킨 반례, HBR2-01).  근거가 없으면 회전각-무관 상·하한 · 그 사이는 TECH.

usage
  python3 scripts/check_contact_validity.py <덤프디렉터리> [...] [--label L]          # 옛 빠른 점검 (계약 아님)
  python3 scripts/check_contact_validity.py --contract <런디렉터리> [...] --n-expected 100000 --json out.json
  python3 scripts/check_contact_validity.py --selftest
"""
import argparse
import glob
import json
import math
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from measure_bed_aspect import frames, read_dump, validate_frame          # noqa: E402

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
#: ★ 재개-위상 **등록 허용 각** (2026-09-28, Codex 3차 HBR3-03 Q3 — 생산자 0.05° · 소비자 0.5° 로 갈라져 있던 것을 **한 곳**에 둔다).
#:   영수증 생산자 (`mixer_restart_phase_test.py`) 는 실측 오차가 이 값 이하일 때만 통과를 내고, 소비자는 **실측값이 아니라 이 값**
#:   으로 벽 겹침을 [θ − ε, θ + ε] **구간 전체**에서 잰다 (실측 최대가 0 에 가깝다고 캠페인 ε 를 0 으로 두지 않는다).
PHASE_EPS_DEG = 0.05
RECEIPT_SCHEMA = 'restart_phase_v1'   # 봉인 (실행 직전 바이너리 · 덱 · STL 해시 + 실행 결과) 이 붙은 영수증.  옛 v0 는 거부.
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
    (FixMoveMesh::restart) 을 복원하므로 이 식이 재개 뒤에도 이어진다 — 이것은 소스 근거일 뿐이고, 실행 바이너리의 실측은
    재개-위상 영수증 (mixer_restart_phase_test.py) 이 맡는다.  (옛 문구 "데이터로 확인한다 (infer_drum_phase)" 는 철회 — 되읽기는 진단 전용.)
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


def motion_signature(deck_text, stl_dir):
    """덱의 **메시 운동 계약** 지문 (sha256) — 영수증 (입자 뺀 A 덱) 과 판정할 런 (LC · LH · L …) 이 같은 벽을 같은 규칙으로
    돌리는지 대조한다 (2026-09-28, Codex 3차 HBR3-02 ③④).  원 덱 전체 SHA 가 아니다 — LC 와 LH 는 CED 가 다르므로 그렇게
    대조하면 틀린다.  넣는 것: timestep · 벽 메시 (id · **STL 내용 sha256** · scale) · wall/gran 이 쓰는 메시 순서 ·
    move/mesh (id · 대상 메시 · 방식 · 원점 · 축 · 주기) 를 덱 순서대로.  빼는 것: 입자 · 재료 · CED · run 길이 · dump.
    """
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from make_mixer_resume import logical_commands, _tokens
    import hashlib
    rec = []
    for _, blk in logical_commands(deck_text):
        t = _tokens(blk)
        if not t:
            continue
        if t[0] == 'timestep':
            rec.append(['timestep', repr(float(t[1]))])
        elif t[0] == 'fix' and len(t) > 3 and t[3].startswith('mesh/surface'):
            kw = t[4:]
            f = kw[kw.index('file') + 1]
            sha = hashlib.sha256(open(os.path.join(stl_dir, f), 'rb').read()).hexdigest()
            rec.append(['mesh', t[1], sha, repr(float(kw[kw.index('scale') + 1]) if 'scale' in kw else 1.0)])
        elif t[0] == 'fix' and len(t) > 3 and t[3] == 'wall/gran' and 'meshes' in t:
            k = t.index('meshes')
            rec.append(['walls'] + t[k + 1:k + 1 + int(t[t.index('n_meshes') + 1])])
        elif t[0] == 'fix' and len(t) > 3 and t[3] == 'move/mesh':
            io, ia = t.index('origin'), t.index('axis')
            rec.append(['move', t[1], t[t.index('mesh') + 1], 'rotate' if 'rotate' in t else '?',
                        [repr(float(x)) for x in t[io + 1:io + 4]], [repr(float(x)) for x in t[ia + 1:ia + 4]],
                        repr(float(t[t.index('period') + 1])) if 'period' in t else '?'])
    return hashlib.sha256(json.dumps(rec, sort_keys=True).encode()).hexdigest()


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
      ⛔ (2026-09-28 정정) ok 가 나와도 예정 식이 **확인된 것은 아니다** — 이 되읽기는 겹침을 최소화하는 각을 찾을 뿐이라 참 벽이
      어긋나 있어도 ok 를 낸다 (HBR2-01 반례).  진단 전용 (`--diag-fit`) · 판정에 쓰지 않는다.
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


def run_banners(run_dir):
    """런 폴더의 LIGGGHTS 로그 (log.lmp · log.resume*.liggghts · log.liggghts …) → {파일: 첫 'LIGGGHTS (Version' 줄}.
    재개된 런은 로그가 여럿이다 — **전부** 영수증 배너와 같아야 같은 빌드로 돌았다고 본다 (Codex 3차 HBR3-02)."""
    out = {}
    for f in sorted(glob.glob(os.path.join(run_dir, 'log*'))):
        if not os.path.isfile(f):
            continue
        with open(f, encoding='utf-8', errors='replace') as fh:
            for k, line in enumerate(fh):
                if line.startswith('LIGGGHTS (Version'):
                    out[os.path.basename(f)] = line.strip()
                    break
                if k > 200:
                    break
    return out


def _is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def load_phase_receipt(path, spec, run_dir=None, deck_text=None, need_steps=None):
    """재개-위상 영수증 (`scripts/mixer_restart_phase_test.py` v1) → dict.  못 쓰면 ValueError (그 런은 영수증 없이 판정).

    ★ 2026-09-28 Codex 3차 HBR3-01 · 02 — 옛 소비자는 키 존재만 보고 SHA null · dt 2 배 · 축 0 · NaN 주기 · `passed="false"` 를
      받았다.  이제 **v1 스키마**만 받고 값 · 봉인 · 호환을 엄격히 본다:
        형식   passed 는 불리언 true · 주기 · dt 양의 유한 · 축 유한 단위벡터 · 각 오차 · 각 경계 0 ≤ … ≤ PHASE_EPS_DEG · SHA 64 hex
        봉인   seal.binary_sha256 (실행 **직전**에 run.sh 가 잰 값) = 영수증 SHA · A/B 실행 exit 0 · 완료
        호환   주기 · dt · 축 = 이 덱 · 운동 서명 (STL 내용 · scale · 축 · 주기 · 순서) = 이 덱 · 런 로그 배너 = 영수증 배너 (전부) ·
               창의 모든 프레임 step 이 영수증이 **실측한 step** 안에 있다 (need_steps)
      왜 이것으로 충분한가 — 드럼 회전은 **처방 운동** (move/mesh rotate) 이라 입자와 무관하다.  같은 바이너리 · 같은 메시 운동
      계약 · 같은 step 구조면 캠페인 런의 메시는 영수증 A 런의 메시와 같은 궤적을 밟고, 재개 연속성은 B 가 잰다.  그래서
      벽 각의 불확실성 ε 는 **가정값이 아니라** 그 step 에서 잰 오차 (angle_bound_deg · 출력 반올림 포함) 다.
    """
    rc = json.load(open(path, encoding='utf-8'))
    if not isinstance(rc, dict):
        raise ValueError('영수증이 JSON 객체가 아니다')
    if rc.get('schema') != RECEIPT_SCHEMA:
        raise ValueError(f'영수증 스키마 {rc.get("schema")!r} ≠ {RECEIPT_SCHEMA} — 봉인 없는 옛 (v0) 영수증은 쓰지 않는다 (HBR3-01 · 02)')
    if rc.get('test') != 'restart_phase':
        raise ValueError('영수증이 restart_phase 시험 기록이 아니다')
    if rc.get('passed') is not True:
        raise ValueError(f'영수증 passed = {rc.get("passed")!r} — 불리언 true 가 아니다')
    for k in ('period', 'dt'):
        if not (_is_num(rc.get(k)) and rc[k] > 0):
            raise ValueError(f'영수증 {k} = {rc.get(k)!r} — 양의 유한 수가 아니다')
    mv = spec['moves'].get('Drum')
    if not mv:
        raise ValueError('덱에 드럼 회전이 없다')
    if abs(float(rc['period']) - mv['period']) > 1e-9 * mv['period']:
        raise ValueError(f'영수증 주기 {rc["period"]} ≠ 덱 {mv["period"]:g}')
    if not spec.get('dt') or abs(float(rc['dt']) - spec['dt']) > 1e-9 * spec['dt']:
        raise ValueError(f'영수증 dt {rc["dt"]} ≠ 덱 {spec.get("dt")}')
    ax = rc.get('axis')
    if not (isinstance(ax, list) and len(ax) == 3 and all(_is_num(x) for x in ax)):
        raise ValueError(f'영수증 축 {ax!r} — 유한 3 성분이 아니다')
    ax = np.asarray(ax, float)
    if abs(float(np.linalg.norm(ax)) - 1.0) > 1e-9:
        raise ValueError(f'영수증 축 노름 {float(np.linalg.norm(ax)):.6g} ≠ 1')
    if float(ax @ mv['axis']) < 1 - 1e-9:
        raise ValueError('영수증 축 ≠ 덱 축')
    e = rc.get('angle_error_deg')
    b = rc.get('angle_bound_deg', e)
    if not (_is_num(e) and _is_num(b) and 0 <= e <= b <= PHASE_EPS_DEG):
        raise ValueError(f'영수증 각 오차 {e!r} · 경계 {b!r} — 0 ≤ 오차 ≤ 경계 ≤ 등록 ε {PHASE_EPS_DEG}° 인 유한 수여야 쓴다')
    sha = rc.get('binary_sha256')
    if not (isinstance(sha, str) and re.fullmatch(r'[0-9a-f]{64}', sha)):
        raise ValueError(f'영수증 바이너리 SHA {sha!r} — sha256 형식이 아니다')
    seal = rc.get('seal')
    if not isinstance(seal, dict) or seal.get('binary_sha256') != sha:
        raise ValueError('영수증 봉인 (실행 직전 바이너리 SHA) 이 없거나 영수증 SHA 와 다르다')
    rs = rc.get('run_status') if isinstance(rc.get('run_status'), dict) else {}
    for part in ('A', 'B'):
        st = rs.get(part) if isinstance(rs.get(part), dict) else {}
        if st.get('exit') != 0 or st.get('complete') is not True:
            raise ValueError(f'영수증 실행 {part} 가 정상 완료가 아니다 ({st})')
    ver = rc.get('liggghts_version')
    if not (isinstance(ver, str) and ver.startswith('LIGGGHTS')):
        raise ValueError('영수증 배너 (liggghts_version) 가 없다')
    if deck_text is not None and run_dir is not None:
        if rc.get('motion_signature') != motion_signature(deck_text, run_dir):
            raise ValueError('영수증 운동 서명 ≠ 이 런 덱의 메시 운동 계약 (STL 내용 · scale · 축 · 주기 · 순서)')
    if run_dir is not None:
        bn = run_banners(run_dir)
        if not bn:
            raise ValueError('런 폴더에 LIGGGHTS 로그 배너가 없다 — 영수증 바이너리와 연결할 수 없다')
        bad = sorted(f for f, v in bn.items() if v != ver)
        if bad:
            raise ValueError(f'런 로그 배너 ≠ 영수증 배너 ({bad}) — 다른 빌드')
    if need_steps is not None:
        have = rc.get('steps_checked_A')
        if not isinstance(have, list):
            raise ValueError('영수증에 실측 step 목록 (steps_checked_A) 이 없다')
        miss = sorted(set(int(s) for s in need_steps) - set(int(s) for s in have))
        if miss:
            raise ValueError(f'영수증이 이 창의 step {miss[:4]}{"…" if len(miss) > 4 else ""} 을 재지 않았다 — '
                             '짧은 시험을 장시간 상한으로 쓰지 않는다')
    rc['eps_wall_deg'] = float(max(b, rc.get('angle_resolution_deg', 0.0) if _is_num(rc.get('angle_resolution_deg')) else 0.0))
    if rc['eps_wall_deg'] > PHASE_EPS_DEG:
        raise ValueError(f'영수증 각 해상도 {rc.get("angle_resolution_deg")}° > 등록 ε {PHASE_EPS_DEG}°')
    return rc


def container_planes0(run_dir, spec):
    """회전 0 의 용기 평면 (N0, c0, 평면별 메시 id) + 공통 회전 (origin, axis).  볼록 · 공통 회전이 아니면 ValueError."""
    N0, C0, owner, _ = container_at(run_dir, spec, 0)
    mvs = [spec['moves'][m] for m in spec['used'] if m in spec['moves']]
    ref = spec['moves'].get('Drum')
    if ref is None:
        raise ValueError('드럼 회전이 없다')
    for mv in mvs:
        if (np.abs(mv['origin'] - ref['origin']).max() > 0 or float(mv['axis'] @ ref['axis']) < 1 - 1e-12
                or mv['period'] != ref['period'] or mv['start_step'] != ref['start_step']):
            raise ValueError('벽 메시들의 회전 (원점 · 축 · 주기 · 시작) 이 같지 않다 — 공통 회전만 지원')
    rot = np.array([m in spec['moves'] for m in owner])
    return N0, C0, owner, rot, ref['origin'], ref['axis']


def wall_interval(P, r, planes0, theta_lo, theta_hi):
    """벽 δ/r 의 **구간** 경계 — 회전각 θ ∈ [theta_lo, theta_hi] (rad) 전체에서 (2026-09-28, Codex 3차 HBR3-03).

    평면 i 까지의 부호거리는 s_i(θ) = A_i + B_i cos θ + C_i sin θ (회전축 성분 · 수직 성분 분해) 이라, 구간의 최댓값 · 최솟값은
    **양 끝과 구간 안 정지점** (θ = atan2(C, B) · 그 + π) 에서만 난다 — 옛 검사는 θ, θ ± ε 세 점만 봐서 구간 안 최악을 놓쳤다
    (참 1.0008 % → 검사값 0.9992 % → PASS).
      상한 (그 구간 어느 각에서든 날 수 있는 최대) = max_i (r − min_θ s_i) / r
      하한 (참 각이 구간 어디든 반드시 넘는 값)     = max_i (r − max_θ s_i) / r     (max_i min_θ ≤ min_θ max_i)
    반환 (upper, lower, 상한을 낸 평면 번호).  회전하지 않는 평면은 θ 와 무관하다.
    """
    N0, C0, _, rot, o, k = planes0
    q = P - o
    npar = N0 @ k
    nperp = N0 - np.outer(npar, k)
    kxn = np.cross(k, nperp)
    A = np.outer(q @ k, npar) + (N0 @ o + C0)[None, :]
    B = q @ nperp.T
    Cs = q @ kxn.T
    B = np.where(rot[None, :], B, 0.0)
    Cs = np.where(rot[None, :], Cs, 0.0)
    A = np.where(rot[None, :], A, q @ N0.T + (N0 @ o + C0)[None, :])
    sa = A + B * np.cos(theta_lo) + Cs * np.sin(theta_lo)
    sb = A + B * np.cos(theta_hi) + Cs * np.sin(theta_hi)
    amp = np.hypot(B, Cs)
    ph = np.arctan2(Cs, B)
    w = theta_hi - theta_lo

    def _inside(ang):
        return np.mod(ang - theta_lo, 2 * np.pi) <= w
    smin = np.where(_inside(ph + np.pi) & (amp > 0), A - amp, np.minimum(sa, sb))
    smax = np.where(_inside(ph) & (amp > 0), A + amp, np.maximum(sa, sb))
    up = (r[:, None] - smin) / r[:, None]
    lo = (r[:, None] - smax) / r[:, None]
    ku = np.argmax(up, axis=1)
    return up[np.arange(len(P)), ku], lo.max(axis=1), ku


def _wrap_mod(x, m):
    return (x + m / 2) % m - m / 2


def mesh_dump_container(path, run_dir, spec, step, eps_rad):
    """`dump mesh/stl` 한 장 → (N, c, 평면별 메시 id, 드럼 면 수) — **전체 용기**일 때만 (2026-09-28, Codex 3차 HBR3-04).

    옛 판은 파일이 있고 볼록이면 독립 기하로 받아, 드럼만 든 덤프 (끝판 없음) 로 끝판 2 % 를 놓쳤다.  이제:
      ① 삼각형 수 = 원 벽 메시 (wall/gran meshes) 합  ② 원 기하를 축 둘레 한 각 θ_d 로 돌린 것과 **꼭짓점 집합**이 일치
         (양방향 최근접 ≤ 허용 — 구성요소 누락 · 다른 기하는 실패)  ③ θ_d 가 예정각과 (면 대칭을 뺀 나머지) ε 안
         (다른 시각 · 다른 런의 파일은 실패)  ④ 볼록.
    """
    T = read_stl(path)
    if not np.all(np.isfinite(T)):
        raise ValueError('mesh 덤프에 비유한 꼭짓점')
    comps = {m: read_stl(os.path.join(run_dir, spec['meshes'][m][0])) * spec['meshes'][m][1] for m in spec['used']}
    n_exp = sum(len(v) for v in comps.values())
    if len(T) != n_exp:
        raise ValueError(f'mesh 덤프 삼각형 {len(T)} ≠ 원 용기 {n_exp} (' + ' + '.join(f'{m} {len(v)}' for m, v in comps.items())
                         + ') — 구성요소 (드럼 · 끝판) 누락?')
    mv = spec['moves'].get('Drum')
    o, k = (mv['origin'], mv['axis']) if mv else (np.zeros(3), np.array([1.0, 0, 0]))
    e1 = np.cross(k, [0.0, 0.0, 1.0])
    if np.linalg.norm(e1) < 1e-6:
        e1 = np.cross(k, [0.0, 1.0, 0.0])
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(k, e1)
    Nd, _ = _planes(comps['Drum'], comps['Drum'].reshape(-1, 3).mean(0))
    Nx, _ = _planes(T, T.reshape(-1, 3).mean(0))
    dr0 = np.abs(Nd @ k) < 0.99
    drx = np.abs(Nx @ k) < 0.99
    if int(dr0.sum()) != int(drx.sum()) or int(dr0.sum()) == 0:
        raise ValueError(f'mesh 덤프의 드럼 면 {int(drx.sum())} ≠ 원 {int(dr0.sum())}')
    a0 = np.arctan2(Nd[dr0] @ e2, Nd[dr0] @ e1)
    ax_ = np.arctan2(Nx[drx] @ e2, Nx[drx] @ e1)
    best = None
    for c in a0:                                       # 덤프의 첫 드럼 면을 원의 각 면에 짝지어 본다
        th = float(_wrap_mod(ax_[0] - c, 2 * np.pi))
        mis = max(float(np.min(np.abs(_wrap_mod(x - (a0 + th), 2 * np.pi)))) for x in ax_)
        if best is None or mis < best[1]:
            best = (th, mis)
    th_d = best[0]
    Rm = _rot(k, th_d)
    V0 = np.vstack([v.reshape(-1, 3) for v in comps.values()])
    Vexp = (V0 - o) @ Rm.T + o
    Vx = T.reshape(-1, 3)
    scale = float(np.abs(V0).max())
    tol = max(1e-7, 1e-5 * scale)

    def _nn(Aa, Bb):
        d = np.full(len(Aa), np.inf)
        for i0 in range(0, len(Aa), 512):
            d[i0:i0 + 512] = np.sqrt(((Aa[i0:i0 + 512, None, :] - Bb[None, :, :]) ** 2).sum(-1)).min(1)
        return float(d.max())
    hd = max(_nn(Vx, Vexp), _nn(Vexp, Vx))
    if hd > tol:
        raise ValueError(f'mesh 덤프가 원 용기 (' + ' · '.join(comps) + f') 의 강체 회전이 아니다 (꼭짓점 최대 어긋남 {hd:.3g} m > {tol:.3g})')
    if mv:
        fa = 2 * np.pi / int(dr0.sum())
        d = float(_wrap_mod(th_d - mesh_angle(spec, 'Drum', step), fa))
        if abs(d) > eps_rad + 1e-12:
            raise ValueError(f'mesh 덤프 회전각이 예정각과 {np.degrees(d):+.4f}° 다르다 (면 대칭 제외 · 허용 {np.degrees(eps_rad):.4g}°) '
                             '— 다른 시각 · 다른 런의 파일?')
    N, C = _planes(T, Vx.mean(0))
    if float((Vx @ N.T + C).min()) < -1e-5 * float(np.abs(Vx).max()):
        raise ValueError('mesh 덤프의 용기가 볼록이 아니다')
    par = np.abs(N @ k) > 0.99
    caps = {m: _planes(v, V0.mean(0)) for m, v in comps.items() if m != 'Drum'}
    owner = []
    for n_, c_, p_ in zip(N, C, par):
        if not p_:
            owner.append('Drum')
            continue
        hit = [m for m, (Nc, Cc) in caps.items() if any(float(n_ @ a_) > 1 - 1e-6 and abs(c_ - b_) < 1e-6 * scale for a_, b_ in zip(Nc, Cc))]
        owner.append(hit[0] if hit else 'Cap')
    return N, C, owner, int((~par).sum())


def container_from_stl(path, spec):
    """(옛 판 — 쓰지 않는다) 완결성 검사 없이 mesh 덤프를 용기로 읽던 함수.  ⛔ HBR3-04: 끝판 없는 덤프를 받았다.
    판정 경로는 `mesh_dump_container` 를 쓴다."""
    raise ValueError('container_from_stl 은 폐기 — mesh_dump_container (완결성 · 예정각 대조) 를 쓴다 (Codex 3차 HBR3-04)')


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
    from measure_mixing_index import deck_plan, planned_t0          # t₀ 정의는 판독기 한 곳 (규율 ①)
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
               wall_max_by_type={}, wall_lower_max=float('-inf'), wall_basis=None, phase=[], phase_status='not_run', phase_note='',
               n_frames=0, window=None)
    if not fr:
        tech.append('덤프가 없다')
        out['verdict'] = 'TECH'
        return out
    #  ★ 계획 t₀ (2026-09-28, Codex 3차 HBR3-05) — 정착 끝의 **계획 덤프 step** 이 그대로 있어야 한다.  옛 판은 "있는 것 중
    #    ≤ 2·steps_fill 인 마지막" 을 골라, 없어진 t₀ 를 앞 프레임으로 조용히 대체했다 (판독기와 같은 정의 · 같은 규칙).
    st0 = planned_t0(plan)
    if st0 not in {st for st, _ in fr}:
        tech.append(f'계획 t₀ {st0} (정착 끝 · dump 격자) 프레임이 없다 — 앞 프레임으로 대체하지 않는다 (HBR3-05)')
        out['verdict'] = 'TECH'
        return out
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
    mesh_src, receipt, eps, planes0, mesh_cache = None, None, 0.0, None, {}
    if spec is not None:
        have = [st for st, _ in win if os.path.isfile(os.path.join(mesh_dir, f'mesh_{st}.stl'))]
        if have and len(have) == len(win):
            #  ★ 완결성 (HBR3-04) — 전 프레임의 덤프가 원 용기 (드럼 + 두 끝판) 의 강체 회전이고 예정각과 맞아야 쓴다
            try:
                for st in have:
                    mesh_cache[st] = mesh_dump_container(os.path.join(mesh_dir, f'mesh_{st}.stl'), run_dir, spec, st,
                                                         float(np.radians(PHASE_EPS_DEG)))
                mesh_src = mesh_dir
            except (ValueError, OSError, KeyError, SystemExit) as e:
                mesh_cache = {}
                tech.append(f'mesh 덤프를 독립 기하로 쓸 수 없다 (step {st}: {e}) — 안 쓴다')
        elif have:
            tech.append(f'mesh 덤프가 창의 일부 프레임에만 있다 ({len(have)}/{len(win)}) — 전부 있거나 없어야 한다 (안 쓴다)')
        if phase_receipt:
            try:
                receipt = load_phase_receipt(phase_receipt, spec, run_dir=run_dir, deck_text=deck_text,
                                             need_steps=[st for st, _ in win])
                eps = float(np.radians(receipt['eps_wall_deg']))
                planes0 = container_planes0(run_dir, spec)
            except (ValueError, OSError, KeyError, TypeError) as e:
                receipt = None
                tech.append(f'재개-위상 영수증 불가 ({e}) — 영수증 없이 상·하한으로 판정')
    pick = set()
    if spec is not None and diag_fit:
        rot = [st for st, _ in win if mesh_angle(spec, 'Drum', st) > 0]
        base = rot if rot else [win[0][0]]
        pick = {base[int(round(i * (len(base) - 1) / max(PHASE_FRAMES - 1, 1)))] for i in range(min(PHASE_FRAMES, len(base)))}
    ids0 = cnt0 = attr0 = None
    for k, (st, path) in enumerate(win):
        #  ★ 매 프레임 필수 스키마 (2026-09-28, Codex 3차 HBR3-06) — 머리 (TIMESTEP = 파일명 · 원자 수 = 행 수) · 필수 열 ·
        #    id/type 유한 정수 · id 유일 · 좌표 유한 · 반경 양수.  옛 판은 t₀ 에서만 id 를 요구해 그 뒤의 id 부재 · 헤더 부재 ·
        #    소수 type (정수 절삭) 을 "변화 없음" 으로 넘겼다.  문제가 있으면 그 프레임은 **계산하지 않고** TECH.
        probs = validate_frame(path)
        if probs:
            tech.append(f'step {st}: 덤프 형식 (헤더 · 열 · 값) — {"; ".join(probs[:3])} (그 프레임은 계산에 쓰지 않는다)')
            if k == 0:
                tech.append('t₀ 프레임이 형식 검사를 못 넘어 보존 기준을 세울 수 없다')
                out['verdict'] = 'TECH'
                return out
            continue
        D = read_dump(path)
        P = np.c_[D['x'], D['y'], D['z']]
        r = D['radius']
        ty = D['type'].astype(int)
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
            #  벽 기하의 근거: mesh 덤프 (독립 · 완결 확인) > 영수증 (예정각 ± 실측 각 경계, 구간 극값) > 예정각 (미검증 — 보고만)
            if mesh_src:
                Ng, Cg, owner, _ = mesh_cache[st]
                wr, wk = wall_overlaps(P, r, Ng, Cg)
                wl = wr
            else:
                Ng, Cg, owner, _ = container_at(run_dir, spec, st)
                if receipt is not None and planes0 is not None:
                    #  ★ 구간 극값 (HBR3-03) — 예정각 ± ε (ε = 영수증이 그 step 에서 잰 각 경계) 전체에서 상한 · 하한
                    th_ = mesh_angle(spec, 'Drum', st)
                    e_ = eps if st > spec['moves']['Drum']['start_step'] else 0.0
                    wr, wl, wk = wall_interval(P, r, planes0, th_ - e_, th_ + e_)
                    owner = planes0[2]
                else:
                    wr, wk = wall_overlaps(P, r, Ng, Cg)
                    wl = wr
            own_g = mesh_cache[st][2] if mesh_src else container_at(run_dir, spec, st)[2] if receipt is not None else owner
            is_cap = np.array([o_ != 'Drum' for o_ in own_g])
            cap_rel = (r - (P @ Ng[is_cap].T + Cg[is_cap]).min(1)) / r if is_cap.any() else np.full(len(r), -np.inf)
            q_ = P - dgeo['o']
            rho = np.linalg.norm(q_ - np.outer(q_ @ dgeo['ax'], dgeo['ax']), axis=1)
            #  드럼 δ/r 의 회전각-무관 상·하한 — 면 한가운데(변심거리) 가 입자 쪽을 향할 때가 최악, 꼭짓점이면 최선
            wtouch = wr[wr > 0]
            row.update(wall_max=float(wr.max()), wall_lower=float(wl.max()), wall_n_over=int((wr > max_ovl).sum()),
                       wall_n_touch=int(len(wtouch)),
                       wall_p999=float(np.percentile(wtouch, 99.9)) if len(wtouch) else 0.0,
                       cap_max=float(cap_rel.max()),
                       drum_worst=float(((rho + r - dgeo['apo']) / r).max()),
                       drum_best=float(((rho + r - dgeo['rv']) / r).max()))
            for t_ in np.unique(ty):
                key = str(int(t_))
                out['wall_max_by_type'][key] = max(out['wall_max_by_type'].get(key, float('-inf')), float(wr[ty == t_].max()))
            j = int(np.argmax(wr))
            wmesh = owner[int(wk[j])]
            if wr[j] > out['wall_max']:
                out.update(wall_max=float(wr[j]), wall_max_step=int(st), wall_max_type=int(ty[j]), wall_max_mesh=wmesh)
            out['wall_lower_max'] = max(out['wall_lower_max'], float(wl.max()))
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
            out['wall_basis'] = (f'예정각 ± {receipt["eps_wall_deg"]:.3g}° 구간 극값 (재개-위상 영수증 {os.path.basename(phase_receipt)} 이 '
                                 f'그 step 에서 잰 각 경계 · 바이너리 {str(receipt["binary_sha256"])[:12]}…)')
            lo_ = out['wall_lower_max']
            if out['wall_max'] > max_ovl and lo_ > max_ovl:
                reject.append(f'벽 δ/r 가 위상 불확실성 구간 (± {receipt["eps_wall_deg"]:.3g}°) 의 **어느 각에서도** {lo_*100:.3f} % 이상 '
                              f'> {max_ovl*100:g} % (명백 위반 · 최대 step {out["wall_max_step"]} · 타입 {out["wall_max_type"]} · {out["wall_max_mesh"]})')
            elif out['wall_max'] > max_ovl:
                tech.append(f'위상 불확실성으로 미식별 — ± {receipt["eps_wall_deg"]:.3g}° 구간 안에서 벽 δ/r {lo_*100:.4f}–{out["wall_max"]*100:.4f} % '
                            f'가 {max_ovl*100:g} % 를 걸친다 (실제 1 % 초과 실측이 아니다 · HBR3-03)')
            over = False
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
        """옛 (v0) 영수증 모양 — 봉인 · 스키마 없음.  2026-09-28 부터 **거부**된다 (㉑b)."""
        p_ = os.path.join(td, 'receipt.json')
        _json.dump(dict(test='restart_phase', passed=ok, period=period, axis=[1.0, 0.0, 0.0], angle_error_deg=err,
                        binary_sha256='0' * 64, liggghts_version='test', date='2026-09-27'), open(p_, 'w'))
        return p_

    BANNER = 'LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, compiled 2026-08-25-18:16:51 by test, git commit 3d5c)'

    def _receipt1(td, run_, name='receipt1.json', **kw):
        """봉인된 (v1) 영수증 — 이 시험 덱과 **맞게** 만든다 (주기 · dt · 축 · 운동 서명 · 배너 · 범위).  kw 로 한 칸씩 망가뜨린다."""
        open(os.path.join(run_, 'log.lmp'), 'w').write(BANNER + '\nCreated orthogonal box\n')
        dk = open(os.path.join(run_, 'in.mixer')).read()
        sp = deck_walls(dk)
        v = dict(schema=RECEIPT_SCHEMA, test='restart_phase', passed=True, period=sp['moves']['Drum']['period'],
                 dt=sp['dt'], axis=[1.0, 0.0, 0.0], angle_error_deg=1e-5, angle_bound_deg=1e-5, binary_sha256='a' * 64,
                 liggghts_version=BANNER, motion_signature=motion_signature(dk, run_), span_rotation_steps=10 ** 7,
                 steps_checked_A=list(range(0, 14001, 500)),
                 seal=dict(binary_sha256='a' * 64), run_status=dict(A=dict(exit=0, complete=True), B=dict(exit=0, complete=True)))
        v.update(kw)
        p_ = os.path.join(td, name)
        _json.dump(v, open(p_, 'w'))
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
        rp13 = _receipt1(td, run)
        w2 = check_window(run, diag_fit=True, phase_receipt=rp13)
        chk(f'⑬b 영수증이 있으면 같은 침대가 예정각으로 판정된다 (receipt · 벽 최대 {w2["wall_max"]*100:.3f} % → PASS)',
            w2['verdict'] == 'PASS' and w2['phase_status'] == 'receipt' and 0 < w2['wall_max'] < 0.003)
        #  ⚠ 변이 — 덱의 주기를 바꾸면 영수증이 안 맞아 (주기 ≠) 영수증을 버린다 · 진단은 mismatch — 어느 쪽도 통과로 새지 않는다
        open(os.path.join(run, 'in.mixer'), 'w').write(_deck(period=0.024))
        w3 = check_window(run, diag_fit=True, phase_receipt=rp13)
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
        #  ⚠ 2026-09-28 규칙 변경 (Codex 3차 HBR3-04): 예정각과 **모순되는** mesh 덤프는 그 런 · 그 시각의 파일이라는 출처를 세우지
        #    못한다 (다른 시각 · 다른 런의 파일과 구분할 수 없다) → 독립 기하로 쓰지 않는다.  이 반례의 참 2 % 는 그래도 PASS 로 새지 않는다.
        chk(f'⑮b 예정각과 반 면각 어긋난 mesh 덤프는 쓰지 않는다 — 참 2 % 는 PASS 로 새지 않고 TECH ({w2["verdict"]} · {w2["phase_status"]})',
            w2['verdict'] == 'TECH' and w2['phase_status'] != 'mesh-dump' and any('예정각' in t for t in w2['tech'])
            and w2['wall_bound_worst'] >= 0.02 - 1e-9)
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
        w2 = check_window(run, phase_receipt=_receipt1(td, run))
        chk(f'⑯b 재개-위상 영수증이 있으면 예정각 (±오차) 으로 잰다 (receipt · 벽 최대 {w2["wall_max"]*100:.3f} %)',
            w2['verdict'] == 'PASS' and w2['phase_status'] == 'receipt' and abs(w2['wall_max'] - 0.005) < 2e-4)
        w3 = check_window(run, phase_receipt=_receipt1(td, run, name='r024.json', period=0.024))
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

    # ══ ㉑~㉕ 2026-09-28 Codex 3차 HBR3-02 · 03 · 04 · 05 · 06 — 반례를 **먼저 재현**하고 고친다 ══════════════════════════
    #   (docs/reviews/codex_mixer_highbo_rereview2_evidence_20260927/review_round3_probe.py 의 경우들을 이 12 각형 기하로)
    with tempfile.TemporaryDirectory() as td:            # ㉑ HBR3-02 — 영수증 소비자는 형식 · 봉인 · 호환을 엄격히 본다
        run = _run(td)
        for st in (2000, 2500, 3000):
            _dump(run, st, BASE + _pair(0.0025) + _ring(_th(st), 0.005))
        w = check_window(run, phase_receipt=_receipt1(td, run))
        chk(f'㉑ 봉인된 v1 영수증 (주기 · dt · 축 · 운동 서명 · 배너 · 범위 일치) 은 받는다 ({w["phase_status"]} · {w["verdict"]})',
            w['phase_status'] == 'receipt' and w['verdict'] == 'PASS')
        w = check_window(run, phase_receipt=_receipt(td))
        chk('㉑b 봉인 · 스키마 없는 옛 (v0) 영수증은 거부 → 영수증 없이 판정 (bounded · tech 에 이유)',
            w['phase_status'] != 'receipt' and any('영수증' in t for t in w['tech']))
        muts = {'binary_sha256 null': dict(binary_sha256=None), 'SHA 형식 아님': dict(binary_sha256='not-a-sha'),
                'dt 2 배': dict(dt=2e-6), '축 0 벡터': dict(axis=[0.0, 0.0, 0.0]), '주기 NaN': dict(period=float('nan')),
                'passed = "false" 문자열': dict(passed='false'), '각 오차 > 등록 ε': dict(angle_error_deg=0.2),
                '운동 서명 다름': dict(motion_signature='0' * 64), '창 step 을 안 잰 영수증 (짧은 시험)': dict(steps_checked_A=[0, 500, 2000]),
                '각 경계 < 각 오차': dict(angle_error_deg=1e-3, angle_bound_deg=1e-4),
                '봉인 SHA ≠ 영수증 SHA': dict(seal=dict(binary_sha256='b' * 64)),
                'B 실행 비정상 종료': dict(run_status=dict(A=dict(exit=0, complete=True), B=dict(exit=1, complete=False)))}
        for k_, kw_ in muts.items():
            w = check_window(run, phase_receipt=_receipt1(td, run, name=f'm_{abs(hash(k_))}.json', **kw_))
            chk(f'㉑c 변이 — {k_} → 영수증 거부', w['phase_status'] != 'receipt' and any('영수증' in t for t in w['tech']))
        rp_ = _receipt1(td, run)
        open(os.path.join(run, 'log.lmp'), 'w').write(BANNER.replace('18:16:51', '09:00:00') + '\n')
        w = check_window(run, phase_receipt=rp_)
        chk('㉑d 변이 — 런 log.lmp 배너 ≠ 영수증 배너 (다른 빌드) → 영수증 거부',
            w['phase_status'] != 'receipt' and any('배너' in t for t in w['tech']))
    with tempfile.TemporaryDirectory() as td:            # ㉒ HBR3-03 — ±ε 세 점이 아니라 **구간** 극값
        run = _run(td)
        eps_ = _m.radians(PHASE_EPS_DEG)
        rr_ = 2e-4
        Dl = APO * (1 - _m.cos(eps_ / 2)) / rr_                    # 구간 중앙 → 양 끝 (ε/2) 에서 줄어드는 δ/r
        ts = _th(2500)
        inner = 0.01 + 0.75 * Dl                                    # 참 최대 (구간 내부 θs + ε/2) > 1 % · 세 점은 1 % − 0.25·Dl
        for st in (2000, 2500, 3000):
            p7 = _on_facet(ts + eps_ / 2, 3, rr_, inner) if st == 2500 else _on_facet(_th(st), 3, rr_, -0.5)
            _dump(run, st, BASE + _pair(0.0025) + [(7, 3, *p7, rr_)])
        w = check_window(run, phase_receipt=_receipt1(td, run, angle_error_deg=PHASE_EPS_DEG, angle_bound_deg=PHASE_EPS_DEG))
        chk(f'㉒ ★ HBR3-03 재현→수정: 구간 내부 최대 {inner*100:.5f} % (세 점 {(inner - Dl)*100:.5f} %) 를 PASS 로 넘기지 않는다 '
            f'— 위상 불확실성으로 미식별 ({w["verdict"]} · 상한 {w.get("wall_max", 0)*100:.5f} %)',
            w['verdict'] == 'TECH' and w['phase_status'] == 'receipt' and w['wall_max'] > 0.01
            and any('미식별' in t for t in w['tech']))
        for st in (2000, 2500, 3000):
            p7 = _on_facet(_th(st), 3, rr_, 0.02 if st == 2500 else -0.5)
            _dump(run, st, BASE + _pair(0.0025) + [(7, 3, *p7, rr_)])
        w = check_window(run, phase_receipt=_receipt1(td, run, angle_error_deg=PHASE_EPS_DEG, angle_bound_deg=PHASE_EPS_DEG))
        chk(f'㉒b ε 구간 어디서든 1 % 를 넘으면 (하한 {w.get("wall_lower_max", 0)*100:.3f} %) REJECT — 위상과 무관한 명백 위반',
            w['verdict'] == 'REJECT' and w.get('wall_lower_max', 0) > 0.01)
    with tempfile.TemporaryDirectory() as td:            # ㉓ HBR3-04 — mesh 덤프는 **전체 용기**여야 한다
        run = _run(td)
        xh = XH_ * SC_
        for st in (2000, 2500, 3000):
            _dump(run, st, BASE + _pair(0.0025) + [(7, 3, xh - 0.98 * 2e-4, 0.0, 0.003, 2e-4)])

        def _mesh_part(st, theta, parts):
            os.makedirs(os.path.join(run, 'post_mesh'), exist_ok=True)
            Rm = _rot(np.array([1.0, 0, 0]), theta)
            tris = [tuple(map(tuple, t_ @ Rm.T)) for nm in parts for t_ in read_stl(os.path.join(run, nm)) * SC_]
            _stl(os.path.join(run, 'post_mesh', f'mesh_{st}.stl'), tris)
        for st in (2000, 2500, 3000):
            _mesh_part(st, _th(st), ('Drum.stl',))
        w = check_window(run)
        chk(f'㉓ ★ HBR3-04 재현→수정: 끝판 없는 (Drum 만) mesh 덤프로 끝판 2 % 를 놓치지 않는다 ({w["verdict"]} · {w["phase_status"]})',
            w['verdict'] != 'PASS' and w['phase_status'] != 'mesh-dump' and any('mesh' in t for t in w['tech']))
        for st in (2000, 2500, 3000):
            _mesh_part(st, _th(st), ('Drum.stl', 'Front.stl'))
        w = check_window(run)
        chk('㉓b 끝판 하나 빠진 mesh 덤프도 거부 (TECH 사유에 mesh)', w['phase_status'] != 'mesh-dump' and any('mesh' in t for t in w['tech']))
        for st in (2000, 2500, 3000):
            _mesh_part(st, _th(st) + _m.radians(5.0), ('Drum.stl', 'Front.stl', 'Back.stl'))
        w = check_window(run)
        chk('㉓c 예정각과 5° 어긋난 (다른 시각/런) 전체 mesh 덤프는 거부', w['phase_status'] != 'mesh-dump' and any('예정각' in t for t in w['tech']))
        for st in (2000, 2500, 3000):
            _mesh_part(st, _th(st), ('Drum.stl', 'Front.stl', 'Back.stl'))
        w = check_window(run)
        chk(f'㉓d 완전한 mesh 덤프면 그 벽으로 끝판 2 % 를 기각한다 ({w["phase_status"]} · {w["wall_max"]*100:.2f} % · {w["wall_max_mesh"]})',
            w['verdict'] == 'REJECT' and w['phase_status'] == 'mesh-dump' and abs(w['wall_max'] - 0.02) < 1e-6)
    with tempfile.TemporaryDirectory() as td:            # ㉔ HBR3-06 — **매 프레임** 필수 스키마
        run = _run(td)
        _dump(run, 2000, BASE + _pair(0.0025))
        H_ = 'ITEM: TIMESTEP\n{0}\nITEM: NUMBER OF ATOMS\n{1}\nITEM: BOX BOUNDS ff ff ff\n-1 1\n-1 1\n-1 1\n'
        rows_ = BASE + _pair(0.0025)
        with open(os.path.join(run, 'post', 'mix_2500.liggghts'), 'w') as fh:     # id 열 없음
            fh.write(H_.format(2500, len(rows_)) + 'ITEM: ATOMS type x y z radius\n'
                     + ''.join(f'{t_} {X} {Y} {Z} {RR}\n' for (_, t_, X, Y, Z, RR) in rows_))
        with open(os.path.join(run, 'post', 'mix_3000.liggghts'), 'w') as fh:     # 헤더 없음 + 소수 type
            fh.write('ITEM: ATOMS id type x y z radius\n'
                     + ''.join(f'{i_} {t_ + 0.5} {X} {Y} {Z} {RR}\n' for (i_, t_, X, Y, Z, RR) in rows_))
        w = check_window(run)
        chk(f'㉔ ★ HBR3-06 재현→수정: t₀ 뒤 프레임의 id 열 부재 · 헤더 부재 · 소수 type 을 통과시키지 않는다 ({w["verdict"]} · '
            f'{"; ".join(w["tech"])[:90]})',
            w['verdict'] != 'PASS' and any('2500' in t and 'id' in t for t in w['tech'])
            and any('3000' in t for t in w['tech']))
    with tempfile.TemporaryDirectory() as td:            # ㉕ HBR3-05 (검사기 쪽) — 계획 t₀ 가 없으면 앞 프레임으로 대체하지 않는다
        run = _run(td)
        for st in (1500, 2500, 3000):
            _dump(run, st, BASE + _pair(0.0025))
        w = check_window(run)
        chk(f'㉕ 계획 t₀ (2000) 프레임이 없으면 TECH — 1500 으로 대체하지 않는다 ({"; ".join(w["tech"])[:80]})',
            w['verdict'] == 'TECH' and any('계획 t₀' in t for t in w['tech']) and w.get('window') is None)
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
