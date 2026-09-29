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
  python3 scripts/check_contact_validity.py --contract <soft 셀> --soft-range 5.8 [--bins 0] …   # 강성 축 §6 — 상태 (TECH_FAIL · CONTRACT_MET ·
                                                                                                # CONTRACT_NOT_MET · OUT_OF_RANGE) · 원 1 % · soft 범위
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
RECEIPT_SCHEMA = 'restart_phase_v2'   # v2 (2026-09-28 Codex 4 차 HBR4-01 · 02 · 03): 봉인 · 덤프 목록 완전성 · 운동 시계 · 위치 경계.
                                      #   v1 (수정 전 생산자 — B 유한성 · 빈 목록 · 형상 잔차 누락) · v0 (봉인 없음) 은 거부.
MESH_DUMP_BASIS = False               # ★ HBR4-04 (나, 1저자 09-28) — post_mesh/ 덤프를 벽 판정 근거로 쓰지 않는다.  삼각형 수 ·
                                      #   꼭짓점 집합 보존은 "전체 용기" 의 증명이 아니다 (끝판을 [중심·테두리·중심] 으로 퇴화시키면
                                      #   평면 하나가 조용히 사라진다).  면 연결 검증 (가) 을 세우기 전까지 정지 벽 · 영수증 · 상·하한만.
STL_REF_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dem_scripts', 'mixer_20260919'))
LAUNCH_SCHEMA = 'mixer_highbo_launch_record/1'   # launch_highbo.sh 의 발사 봉인
PHASE_TOL_FRAC = 0.02            # 데이터로 되읽은 드럼 회전각 vs 덱 예정각 — 면 각도의 2 % (9.23° 면이면 0.18°)
PHASE_FRAMES = 5                 # 위상을 데이터로 확인할 프레임 수 (창 안에 고르게)
#: ★ soft 진단 범위 (2026-09-30 · 강성 축 사전등록 docs/reviews/mixer_highbo_stiffness_prereg_20260929.md v2.4 §6 · 코드 선행조건 2 단계 piece 3):
#:   "soft 진단 범위 = 5.8 % … δ_soft/δ_ref = (E_ref/E_soft)^(2/3) = 14^(2/3) = 5.81 ⇒ 등록된 ref 계약 1 % 를 그대로 환산한 값 … 관측량 = §6 의
#:   1 % 계약과 같은 양 (저장 프레임 최대 · 입자–입자 + 벽 · 상별 · 분모 r_min) · 경계 `x <= 5.8 + 1e-9` · 초과 = OUT_OF_RANGE (원 1 % 는 soft
#:   에서 어차피 NOT_MET 유지 · q 를 공식 판정에 안 씀 · 같은 조건 재시도로 지우는 TECH 사유 아님 · 팔은 완주 · 값 보존 · 보고 · 짝 블록의 다른
#:   팔 계속 …)" · "DEV E0_ref 실측 최대 × 5.81 이 5.8 % 를 넘으면 그 사실을 보고하되 **범위를 올리지 않는다**".
#:   ⛔ CLI `--soft-range` 는 이 값 외를 거부한다 (올리거나 내리지 않는다 · 결과를 보고 고르지 않는다 — Codex 9 차 Q6).
SOFT_RANGE_PCT = 5.8
SOFT_RANGE_EPS = 1e-9            # 경계 비교 규약 (부동소수 · % 단위) — 물리 허용치 아님
#: 스모크 · 관문이 구분해 내보낼 상태 (§6 — "`TECH_FAIL` / `CONTRACT_MET` / `CONTRACT_NOT_MET` / `OUT_OF_RANGE`")
CONTRACT_STATUSES = ('TECH_FAIL', 'CONTRACT_MET', 'CONTRACT_NOT_MET', 'OUT_OF_RANGE')


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


def motion_clock(deck_text):
    """메시 운동의 **시계** — 운동 fix 의 생성 · 해제 step · read_restart · run 끝 step (2026-09-28, Codex 4 차 HBR4-02).

    motion_signature 는 운동의 **모양** (축 · 주기 · 메시 · 순서) 만 담고 run 길이 · 회전 시작을 뺀다 → 회전 시작 2001 과 3001 을
    구분하지 못했다.  영수증의 각 오차는 그 **시계**에서 잰 것이라 판정할 덱과 시계가 같아야 이식된다.
    """
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from make_mixer_resume import logical_commands, _tokens
    ev, steps, movers = [], 0, set()
    for _, blk in logical_commands(deck_text):
        t = _tokens(blk)
        if not t:
            continue
        if t[0] == 'run':
            steps = int(t[1]) if 'upto' in t else steps + int(t[1])
        elif t[0] == 'fix' and len(t) > 3 and t[3] == 'move/mesh':
            movers.add(t[1])
            ev.append(['move', t[1], t[t.index('mesh') + 1] if 'mesh' in t[4:] else '?', steps])
        elif t[0] == 'unfix' and len(t) > 1 and t[1] in movers:
            movers.discard(t[1])
            ev.append(['unmove', t[1], steps])
        elif t[0] == 'read_restart':
            ev.append(['read_restart', steps])
    ev.append(['end', steps])
    return ev


def _sha_file(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def resume_marks(run_dir):
    """재개 흔적 (make_mixer_resume 산출) — in.resume · post_pre_resume_* · restart/resume_from_*."""
    out = []
    for pat in ('in.resume', 'post_pre_resume_*', os.path.join('restart', 'resume_from_*')):
        out += sorted(os.path.relpath(q, run_dir) for q in glob.glob(os.path.join(run_dir, pat)))
    return out


def launch_binding(run_dir, spec, path=None):
    """판정할 런의 **실행 직전 봉인** (launch_highbo.sh 의 launch_record.json) → dict.  못 세우면 ValueError.

    ★ HBR4-02 (Codex 4 차) — 옛 소비자는 영수증 바이너리를 영수증 **안에서만** 대조하고 런과는 배너 문자열로만 이었다 (배너가 같으면
      다른 바이너리도 수락).  이제 그 런을 실제로 띄운 바이너리의 sha256 (봉인) 과 대조하고, 봉인 때의 덱 · STL 이 지금 파일과
      같은지 본다 (검사기가 읽는 덱 · STL = 그 런이 실행한 것).  ⚠ 봉인이 없으면 **미상**이다 — 지금 파일을 해시해 과거 실행
      기록처럼 채우지 않는다 (Codex 단서).
    """
    lp = path or os.path.join(run_dir, 'launch_record.json')
    if not os.path.isfile(lp):
        raise ValueError('판정할 런의 발사 봉인 (launch_record.json) 이 없다 — 실행 당시 바이너리가 미상이라 영수증을 잇지 않는다 '
                         '(HBR4-02 · 지금 파일을 해시해 채우지 않는다)')
    lr = json.load(open(lp, encoding='utf-8'))
    if not isinstance(lr, dict) or lr.get('schema') != LAUNCH_SCHEMA:
        raise ValueError(f'발사 봉인 (launch_record.json) 스키마가 {LAUNCH_SCHEMA} 가 아니다')
    ls = lr.get('lmp_sha256')
    if not (isinstance(ls, str) and re.fullmatch(r'[0-9a-f]{64}', ls)):
        raise ValueError('발사 봉인 (launch_record.json) 의 바이너리 sha256 (lmp_sha256) 이 없거나 형식이 아니다')
    want = lr.get('sha256') if isinstance(lr.get('sha256'), dict) else {}
    files = ['in.mixer'] + [spec['meshes'][m][0] for m in spec['used']]
    bad = [f for f in files if want.get(f) is None or not os.path.isfile(os.path.join(run_dir, f))
           or _sha_file(os.path.join(run_dir, f)) != want.get(f)]
    if bad:
        raise ValueError(f'발사 봉인 (launch_record.json) 뒤 바뀌었거나 봉인에 없는 파일 {bad} — 검사기가 읽는 덱 · STL 이 그 런이 '
                         '실행한 것이 아니다')
    #  ★ SLURM 판 (2026-09-28, 1저자 결정: LH 를 ibb 에서) — 로컬 발사는 봉인 바로 뒤 exec 라 틈이 없지만, SLURM 은 제출 ↔ 시작 사이
    #    대기열 틈이 있다.  러너의 시작 대조 (dem_scripts/mixer_20260921/start_check.py) 가 남긴 **통과 기록**이 봉인과 맞아야
    #    "실행된 바이너리 = 봉인" 이 선다.  없거나 어긋나면 **미상** — 영수증을 잇지 않는다 (셀프테스트 ㉛).
    if lr.get('backend') == 'slurm':
        sl = lr.get('slurm') if isinstance(lr.get('slurm'), dict) else {}
        jp = os.path.join(os.path.dirname(lp), 'job_start.json')
        try:
            js = json.load(open(jp, encoding='utf-8'))
        except (OSError, ValueError):
            raise ValueError('SLURM 발사인데 시작 대조 기록 (job_start.json) 이 없다 — 대기열 뒤 실제로 실행된 바이너리가 봉인 것이라는 '
                             '증거가 없어 영수증을 잇지 않는다')
        want_js = {'schema': 'mixer_highbo_job_start/1', 'lmp_sha256': ls, 'runner_sha256_executed': sl.get('runner_sha256'),
                   'start_check_sha256': sl.get('start_check_sha256'), 'launch_record_sha256': _sha_file(lp),
                   'slurm_ntasks': sl.get('np')}
        off = [k for k, v in want_js.items() if not isinstance(js, dict) or v is None or js.get(k) != v]
        if not isinstance(js, dict) or js.get('ok') is not True:
            off.append('ok')
        if off:
            raise ValueError(f'SLURM 시작 대조 기록 (job_start.json) 이 봉인과 맞지 않는다 {off} — 실행된 바이너리 · 러너가 봉인 것이라는 '
                             '증거가 서지 않아 영수증을 잇지 않는다')
    return lr


def static_wall_contract(run_dir, spec, deck_text, steps, expect_deck=None, stl_ref_dir=None):
    """정지 벽 계약 (2026-09-28, Codex 4 차 HBR4-07) → (적용되나, 성립하나, 사유 목록).

    E0 (회전 0) 는 운동 fix 가 있어도 한 step 도 돌지 않는다 — 그런데 옛 검사기는 회전 캠페인용 근거 (영수증 · mesh 덤프) 만 알아
    멀쩡한 E0 를 과잉차단했다 (TECH).  **적용** = 창의 모든 step 이 모든 운동 fix 의 시작 step 이하 (θ = 0 이 식으로 정확).  **성립** =
      fresh     덱에 read_restart 없음 · 재개 흔적 없음 (make_mixer_resume 산출)
      입력      덱 = 기대 덱 (`expect_deck` — 생성기로 다시 만든 등록 덱) · 주석을 뺀 모든 명령이 토큰 단위로 같다
      기하      벽 STL = 캠페인 원본 (`stl_ref_dir`, 기본 dem_scripts/mixer_20260919) 과 내용 sha256 이 같다
    성립하면 벽 = 원 STL 그대로 (각 0 · 불확실성 0).  ⛔ 이것을 풀려고 step 포함 검사나 1 % 문턱을 느슨하게 하지 않았다.
    ⚠ 한계 (출력에 남긴다): E0 는 발사 봉인 이전 세대라 "디스크의 덱 = 실행한 덱" 은 gen_all.sh 의 덮어쓰기 가드 (로그가 있으면
      덱을 다시 쓰지 않는다) 에 기댄다 — 실행 기록을 뒤늦게 만들어 채우지 않는다.
    """
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from make_mixer_resume import logical_commands, _tokens
    last = max(steps)
    if not all(mv['start_step'] >= last for mv in spec['moves'].values()):
        return False, False, []
    why = []

    def tok(x):
        return [tt for tt in (_tokens(b) for _, b in logical_commands(x)) if tt]
    if any(tt[:1] == ['read_restart'] for tt in tok(deck_text)):
        why.append('덱에 read_restart (fresh 아님)')
    rm = resume_marks(run_dir)
    if rm:
        why.append(f'재개 흔적 {rm[:3]}')
    if not expect_deck:
        why.append('기대 덱 (--expect-deck) 없음 — 입력 동일성을 세울 수 없다')
    elif tok(open(expect_deck, encoding='utf-8', errors='replace').read()) != tok(deck_text):
        why.append('덱 ≠ 기대 덱 (주석 뺀 명령 토큰)')
    ref = stl_ref_dir or STL_REF_DIR
    for m in spec['used']:
        f = spec['meshes'][m][0]
        a_, b_ = os.path.join(run_dir, f), os.path.join(ref, f)
        if not (os.path.isfile(a_) and os.path.isfile(b_)) or _sha_file(a_) != _sha_file(b_):
            why.append(f'{f} ≠ 캠페인 원본 ({ref})')
    return True, not why, why


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


def load_phase_receipt(path, spec, run_dir=None, deck_text=None, need_steps=None, launch_record=None):
    """재개-위상 영수증 (`scripts/mixer_restart_phase_test.py` v2) → dict.  못 쓰면 ValueError (그 런은 영수증 없이 판정).

    ★★ 2026-09-28 Codex 4 차 HBR4-01 · 02 · 03 — v1 소비자는 ① 봉인 목록 · 덤프 목록이 **비어도** 받았다 ("있는 항목만" 검사)
      ② 영수증 바이너리를 **판정할 런**의 실행 기록과 대조하지 않고 배너 문자열만 봤으며, 운동 서명이 회전 시작 · run 길이를 빼서
      시작 2001 과 3001 을 구분하지 못했다 ③ 생산자가 허용한 형상 잔차 (≤ 1e-7 m) 를 버렸다.  이제 (v2):
        목록   seal.files = 두 덱 + 부분마다 벽 STL (정확히 · 빈 · 부분 거부) · run_status.A/B.dumps_n = 실측 step 수 (> 0) ·
               A↔B 차 · 잔차 · 위치 경계 유한 ≥ 0
        런     판정할 런의 launch_record.json (실행 **직전** 봉인) 의 바이너리 sha256 = 영수증 · 봉인 때 in.mixer · STL = 지금 파일
               (봉인이 없으면 미상 — 지금 파일을 해시해 채우지 않는다) · 재개 흔적이 있으면 거부 (런별 상태 확인 = 3차 Q5 는 이 영수증이 아니다)
        시계   운동 시계 (mover 생성·해제 step · read_restart · run 끝 step) = 이 덱 · 회전 시작 step = 이 덱
        경계   pos_bound_m (형상 잔차 + 출력 반올림, 좌표 최대 → 거리 √3) → check_window 가 부호거리에 더한다

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
        raise ValueError(f'영수증 스키마 {rc.get("schema")!r} ≠ {RECEIPT_SCHEMA} — v1 = 수정 전 생산자 (B 유한성 · 빈 목록 · 형상 잔차 누락, '
                         f'HBR4-01 · 03) · v0 = 봉인 없음 → 고친 도구로 analyze 를 다시 돌린다 (LIGGGHTS 재실행 불요)')
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
    #  ★ HBR4-01 — 목록 완전성 (빈 · 부분 목록이면 "있는 항목만" 검사가 통과해 버린다)
    files = seal.get('files') if isinstance(seal.get('files'), dict) else {}
    want = {'A/in.phase_a', 'B/in.phase_b'} | {f'{p_}/{spec["meshes"][m][0]}' for p_ in ('A', 'B') for m in spec['used']}
    if set(files) != want or not all(isinstance(v, str) and re.fullmatch(r'[0-9a-f]{64}', v) for v in files.values()):
        raise ValueError(f'영수증 봉인 파일 목록 ({len(files)} 개) ≠ 기대 {len(want)} 개 {sorted(want)} — 빈 · 부분 목록 거부 (HBR4-01)')
    rs = rc.get('run_status') if isinstance(rc.get('run_status'), dict) else {}
    for part, key in (('A', 'steps_checked_A'), ('B', 'steps_checked_B')):
        st = rs.get(part) if isinstance(rs.get(part), dict) else {}
        if st.get('exit') != 0 or st.get('complete') is not True:
            raise ValueError(f'영수증 실행 {part} 가 정상 완료가 아니다 ({st})')
        n_, have_ = st.get('dumps_n'), rc.get(key)
        if not (isinstance(n_, int) and not isinstance(n_, bool) and n_ > 0 and isinstance(have_, list) and len(have_) == n_):
            raise ValueError(f'영수증 {part} 덤프 목록 {n_!r} 개 ≠ 실측 step {len(have_) if isinstance(have_, list) else None} 개 — '
                             '빈 · 부분 목록 거부 (HBR4-01)')
    for k in ('ab_max_vertex_diff_m', 'residual_max_m', 'pos_bound_m'):
        if not (_is_num(rc.get(k)) and rc[k] >= 0):
            raise ValueError(f'영수증 {k} = {rc.get(k)!r} — 유한한 0 이상 수가 아니다 (HBR4-01 · 03)')
    ver = rc.get('liggghts_version')
    if not (isinstance(ver, str) and ver.startswith('LIGGGHTS')):
        raise ValueError('영수증 배너 (liggghts_version) 가 없다')
    if deck_text is not None and run_dir is not None:
        if rc.get('motion_signature') != motion_signature(deck_text, run_dir):
            raise ValueError('영수증 운동 서명 ≠ 이 런 덱의 메시 운동 계약 (STL 내용 · scale · 축 · 주기 · 순서)')
    #  ★ HBR4-02 — 운동 **시계** (서명이 뺀 회전 시작 · run 길이) 와 판정할 런의 실행 기록에 잇는다
    if deck_text is not None:
        mc = motion_clock(deck_text)
        if rc.get('motion_clock') != mc:
            raise ValueError(f'영수증 운동 시계 {rc.get("motion_clock")} ≠ 이 덱 {mc} (mover 생성·해제 · read_restart · run 끝 step) — '
                             '다른 step 구조에서 잰 각 오차는 이식하지 않는다 (HBR4-02)')
        if rc.get('rotation_start_step') != mv['start_step']:
            raise ValueError(f'영수증 회전 시작 step {rc.get("rotation_start_step")} ≠ 이 덱 {mv["start_step"]} (운동 시계 · HBR4-02)')
    if run_dir is not None:
        rm = resume_marks(run_dir)
        if rm:
            raise ValueError(f'재개된 런 ({rm[:3]}) — 이 영수증은 바이너리 + 메시 운동 계약이고 런별 상태 확인 (3차 Q5) 이 아니다')
        lr = launch_binding(run_dir, spec, launch_record)
        if lr['lmp_sha256'] != sha:
            raise ValueError(f'영수증 바이너리 {sha[:12]}… ≠ 이 런 발사 봉인의 바이너리 {lr["lmp_sha256"][:12]}… — 배너가 같아도 다른 빌드 '
                             '(HBR4-02)')
        rc['launch_record_sha256'] = _sha_file(launch_record or os.path.join(run_dir, 'launch_record.json'))
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
    rc['pos_bound_m'] = float(rc['pos_bound_m'])
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
                 phase_receipt=None, expect_counts=None, diag_fit=False, progress=False,
                 launch_record=None, expect_deck=None, stl_ref_dir=None, bins=None, soft_range_pct=None):
    """★ 등록 계약 판정 — 분석 창 **전 프레임** (정착 끝 t₀ = `measure_mixing_index` 와 같은 정의 → 마지막 덤프).

      ① 입자–입자 최대 δ/r_min ≤ max_ovl (강체 내부 쌍 제외)
      ② 벽 — 드럼 다각 원통 + 두 끝판 — 최대 δ/r ≤ max_ovl.  **드럼 회전각의 근거** (2026-09-27 Codex HBR2-01: 입자 배치로
         회전각을 되읽는 fitting 은 증거가 아니다 — 참 벽 겹침 2 % 인데 위상이 반 면각 어긋나면 PASS · 5/5 ok 를 냈고, 참
         위상 · 0.5 % 는 TECH 로 막았다.  셀프테스트 ⑮ · ⑯):
           static        정지 벽 계약 (HBR4-07) — 창 전체가 회전 전 · fresh · 덱 = 기대 덱 · STL = 캠페인 원본 → 원 STL (각 0)
           receipt       `phase_receipt` (재개-위상 영수증 v2) 가 덱 · 발사 봉인 · 운동 시계와 맞으면 예정각 ± 각 경계의 구간 극값
                         + 위치 경계 (형상 잔차 · 출력 반올림, HBR4-03)
           (mesh-dump    post_mesh/ 덤프 — ⛔ HBR4-04 (나) 로 **판정 근거에서 뺐다** (MESH_DUMP_BASIS = False) · 있으면 notes 에만 적는다)
           bounded       둘 다 없으면 회전각과 무관한 상·하한 — 상한 ≤ max_ovl 이면 PASS · 하한 > max_ovl 이면 REJECT
           unidentified  그 사이 = TECH (판정 불가.  예정각으로 잰 값은 **미검증**으로 보고만 한다)
      ③ 상별 입자 수 · id 집합 · **id 별 type · radius** = t₀ (총수 = n_expected · 상별 = expect_counts)  (HBR2-08)
      ④ 기술 조건 — 볼록 용기 · 창 프레임 ≥ 1 · **창 안 덤프 결손 없음** (HBR2-03: 미관측 구간에 통과 증서를 주지 않는다) ·
         덤프 헤더 TIMESTEP/원자 수 = 파일명/행 수 · 같은 step 중복 없음.  못 서면 **TECH** (통과로 치지 않는다)

    관측량 = **저장 프레임 최대** (snapshot-max).  덤프 사이 (이 덱 32 ms ≫ Hertz 충돌 ≈ 22 µs) 의 peak 는 관측하지 않는다 — D-1.
    verdict = PASS · REJECT (①②③ 위반) · TECH (④ 만).  둘 다면 REJECT.

    ★ 2026-09-30 (강성 축 코드 선행조건 2 단계 piece 3):
      `bins` — 창을 판독기 bin 들로 제한 (예 (0,) = 사전등록 §4 a′ "bin 0 창 전 프레임") · 그 bin 들의 계획 격자가 **전부** 있어야 한다.
      `soft_range_pct` — soft 진단 팔 (§6).  None = ref/ref2 (계약 팔).  결과 `status` = contract_status() — 원 1 % 와 soft 범위를
      **따로** 적고 (Codex 9 차 §7 "하나의 PASS/FAIL 로 두 사실을 덮지 않는다") 하나의 상태로 요약한다.  verdict (1 % 계약) 는 그대로.
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
               n_frames=0, window=None, notes=[], pos_bound_m=None, static_why=[],
               bins=sorted(int(b_) for b_ in bins) if bins is not None else None,
               reject_overlap=[], tech_wall_uncertain=[])

    def _done(v_):
        out['verdict'] = v_
        out['status'] = contract_status(out, soft_range_pct)
        return out
    if not fr:
        tech.append('덤프가 없다')
        return _done('TECH')
    #  ★ 계획 t₀ (2026-09-28, Codex 3차 HBR3-05) — 정착 끝의 **계획 덤프 step** 이 그대로 있어야 한다.  옛 판은 "있는 것 중
    #    ≤ 2·steps_fill 인 마지막" 을 골라, 없어진 t₀ 를 앞 프레임으로 조용히 대체했다 (판독기와 같은 정의 · 같은 규칙).
    st0 = planned_t0(plan)
    if st0 not in {st for st, _ in fr}:
        tech.append(f'계획 t₀ {st0} (정착 끝 · dump 격자) 프레임이 없다 — 앞 프레임으로 대체하지 않는다 (HBR3-05)')
        return _done('TECH')
    win = [(st, p) for st, p in fr if st >= st0]
    de = plan['dump_every']
    lat_bins = None
    if bins is not None:
        #  ★ 판독기 bin 창 (piece 3 · 사전등록 §4 a′) — bin = ⌊(s − t₀)/바퀴 step + 1e-9⌋ (measure_mixing_index.analyse 의 _bin 과 같은 식) ·
        #    창 = 그 bin 들 안의 저장 프레임 · 결손 = 그 bin 들의 **계획 격자 전부** 대비 (진행 중인 런의 다음 bin 은 보지 않는다)
        spr_ = plan['steps_per_rev']
        want_b = {int(b_) for b_ in bins}

        def _bin(s_):
            return int(np.floor((s_ - st0) / spr_ + 1e-9))
        lat_bins = [s_ for s_ in range(st0, plan['steps_total'] + 1, de) if _bin(s_) in want_b]
        win = [(st, p) for st, p in win if _bin(st) in want_b]
        if not lat_bins or not win:
            tech.append(f'bin {sorted(want_b)} 창이 비었다 (계획 격자 {len(lat_bins)} 장 · 있는 프레임 {len(win)} 장) — 판정 불가')
            return _done('TECH')
    out['window'] = (win[0][0], win[-1][0])
    out['n_frames'] = len(win)
    out['frames_evaluated'] = [[int(st), p] for st, p in win]       # 이 판정이 본 프레임 (증서가 다시 해시한다 — mixer_smoke_blind contact 블록)
    #  ④ 창 격자 (HBR2-03) — t₀ 부터 마지막 프레임까지 (bins 면 그 bin 들의 계획 격자 전부) dump_every 간격의 덤프가 **다** 있어야 한다
    present = [st for st, _ in win]
    pset = set(present)
    missing = [s for s in (lat_bins if lat_bins is not None else range(st0, win[-1][0] + 1, de)) if s not in pset]
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
    static_ok = False
    if spec is not None:
        have = [st for st, _ in win if os.path.isfile(os.path.join(mesh_dir, f'mesh_{st}.stl'))]
        if have and not MESH_DUMP_BASIS:
            out['notes'].append(f'post_mesh/ 덤프 {len(have)}/{len(win)} 장 — 판정 근거로 쓰지 않는다 (Codex 4 차 HBR4-04 · (나): 삼각형 수 · '
                                '꼭짓점 집합 보존은 전체 용기의 증명이 아니다 — 면 연결 검증 전까지)')
        elif have and len(have) == len(win):
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
        #  ★ 정지 벽 (HBR4-07) — 창 전체가 회전 전이면 영수증이 필요 없다 (θ = 0 이 식으로 정확).  성립 조건 = static_wall_contract
        try:
            s_app, static_ok, s_why = static_wall_contract(run_dir, spec, deck_text, [st for st, _ in win], expect_deck, stl_ref_dir)
        except (ValueError, OSError, KeyError) as e:
            s_app, static_ok, s_why = True, False, [f'정지 벽 계약 검사 불가 ({e})']
        out['static_why'] = s_why
        if s_app and not static_ok:
            out['notes'].append(f'정지 벽 계약 불성립 — {"; ".join(s_why)} (영수증 · 상·하한으로 판정)')
        if static_ok:
            if phase_receipt:
                out['notes'].append('정지 벽 계약 성립 — 창 전체가 회전 전이라 영수증을 쓰지 않는다')
        elif phase_receipt:
            try:
                receipt = load_phase_receipt(phase_receipt, spec, run_dir=run_dir, deck_text=deck_text,
                                             need_steps=[st for st, _ in win], launch_record=launch_record)
                eps = float(np.radians(receipt['eps_wall_deg']))
                planes0 = container_planes0(run_dir, spec)
                out['pos_bound_m'] = receipt['pos_bound_m']
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
                return _done('TECH')
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
                    #  ★ HBR4-03 — 생산자가 허용한 형상 잔차 + 출력 반올림 (거리 · √3 합성) 을 부호거리에 넣는다.  각 오차 0 ≠ 위치 오차 0
                    u_ = receipt['pos_bound_m']
                    wr, wl = wr + u_ / r, wl - u_ / r
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
        out['reject_overlap'].append(reject[-1])
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
        elif static_ok:
            out['phase_status'] = 'static'
            out['wall_basis'] = ('정지 벽 계약 (HBR4-07) — 창 전체가 회전 전 · fresh · 덱 = 기대 덱 · STL = 캠페인 원본 → 원 STL (각 0 · 불확실성 0).  '
                                 '⚠ 발사 봉인 이전 세대면 "디스크의 덱 = 실행한 덱" 은 gen_all.sh 덮어쓰기 가드에 기댄다')
            over = out['wall_max'] > max_ovl
        elif receipt is not None:
            out['phase_status'] = 'receipt'
            out['wall_basis'] = (f'예정각 ± {receipt["eps_wall_deg"]:.3g}° 구간 극값 (재개-위상 영수증 {os.path.basename(phase_receipt)} 이 '
                                 f'그 step 에서 잰 각 경계 · 바이너리 {str(receipt["binary_sha256"])[:12]}… = 발사 봉인 · '
                                 f'위치 경계 {receipt["pos_bound_m"]*1e9:.0f} nm)')
            lo_ = out['wall_lower_max']
            if out['wall_max'] > max_ovl and lo_ > max_ovl:
                reject.append(f'벽 δ/r 가 위상 불확실성 구간 (± {receipt["eps_wall_deg"]:.3g}°) 의 **어느 각에서도** {lo_*100:.3f} % 이상 '
                              f'> {max_ovl*100:g} % (명백 위반 · 최대 step {out["wall_max_step"]} · 타입 {out["wall_max_type"]} · {out["wall_max_mesh"]})')
                out['reject_overlap'].append(reject[-1])
            elif out['wall_max'] > max_ovl:
                tech.append(f'위상 불확실성으로 미식별 — ± {receipt["eps_wall_deg"]:.3g}° 구간 안에서 벽 δ/r {lo_*100:.4f}–{out["wall_max"]*100:.4f} % '
                            f'가 {max_ovl*100:g} % 를 걸친다 (실제 1 % 초과 실측이 아니다 · HBR3-03)')
                out['tech_wall_uncertain'].append(tech[-1])
            over = False
        elif worst <= max_ovl:
            out['phase_status'] = 'bounded'      # 근거 없어도 어느 회전각이어도 한도 안
            out['wall_basis'] = f'회전각-무관 상한 {worst*100:.3f} % ≤ {max_ovl*100:g} %'
        elif best > max_ovl:
            out['phase_status'] = 'bounded'      # 근거 없어도 어느 회전각이어도 한도 밖
            out['wall_basis'] = f'회전각-무관 하한 {best*100:.3f} % > {max_ovl*100:g} %'
            reject.append(f'벽 δ/r 가 **어느 회전각이어도** {best*100:.3f} % 이상 > {max_ovl*100:g} %')
            out['reject_overlap'].append(reject[-1])
        else:
            out['phase_status'], out['wall_basis'] = 'unidentified', '없음'
            tech.append(f'드럼 회전각의 독립 근거가 없고 (재개-위상 영수증 없음 · 정지 벽 아님 · post_mesh/ 덤프는 판정 근거가 아니다 — '
                        f'HBR4-04) 벽 δ/r 가 각에 따라 '
                        f'{best*100:.2f}–{worst*100:.2f} % — 한도 {max_ovl*100:g} % 판정 불가.  '
                        f'예정각으로 잰 {out["wall_max"]*100:.3f} % 는 미검증 (판정에 안 씀)')
            out['tech_wall_uncertain'].append(tech[-1])
        if over:
            n_over = sum(r_.get('wall_n_over', 0) for r_ in pf)
            reject.append(f'벽 최대 δ/r {out["wall_max"]*100:.3f} % > {max_ovl*100:g} % (step {out["wall_max_step"]} · '
                          f'타입 {out["wall_max_type"]} · {out["wall_max_mesh"]} · 넘은 접촉 {n_over} 건/창 · 근거 {out["phase_status"]})')
            out['reject_overlap'].append(reject[-1])
    elif walls:
        out['phase_status'] = 'no_walls'
    return _done('REJECT' if reject else ('TECH' if tech else 'PASS'))


def contract_status(w, soft_range_pct=None):
    """check_window 결과 → 상태 dict (2026-09-30 · 강성 축 사전등록 §6 · 코드 선행조건 2 단계 piece 3).

    세 축을 **따로** 적는다 (§6 표 — 기술적 관측 가능 / 원 1 % 물리 적격성 / soft 진단 범위 · Codex 9 차 §7 "하나의 PASS/FAIL 로 두 사실을 덮지 않는다"):
      technical     'OK' · 'FAIL' — 보존 · 형식 · 계획 프레임 · 창 결손 · 기하 · 출처 (tech 중 벽 위상 불확실만 뺀 것 + 겹침 아닌 기각)
      original_1pct 'MET' · 'NOT_MET' · None (벽 위상 불확실이 1 % 를 걸친다) — x_lo > 1 % 면 NOT_MET · x_hi ≤ 1 % 면 MET (check_window 와 같은 비교)
      soft_range    None (ref/ref2 = 계약 팔) · 'WITHIN' · 'OUT_OF_RANGE' · 'UNIDENTIFIED' — 경계 x ≤ 5.8 + 1e-9 (%)
    x = 저장 프레임 최대 max(입자–입자, 벽) — 벽은 근거별 구간 (static · mesh-dump = 한 값 · receipt = [하한, 상한] · bounded/unidentified =
    [회전각-무관 하한, 상한]).  status (하나로 요약): TECH_FAIL (기술 실패 · 판정 불가) > OUT_OF_RANGE > CONTRACT_NOT_MET > CONTRACT_MET.
    ⚠ soft 의 1 % 초과 (CONTRACT_NOT_MET) 는 **기술 실패가 아니다** — 값 보존 · 보고 · 관문은 막지 않는다 (§6).  ref 의 NOT_MET 은 확인 주장 HOLD.
    """
    if soft_range_pct is not None and soft_range_pct != SOFT_RANGE_PCT:
        raise ValueError(f'soft 진단 범위 {soft_range_pct!r} ≠ 등록 {SOFT_RANGE_PCT} % — 올리거나 내리지 않는다 (§6 · Codex 9 차 Q6)')
    unc = set(w.get('tech_wall_uncertain') or [])
    ovl = set(w.get('reject_overlap') or [])
    hard = [t_ for t_ in (w.get('tech') or []) if t_ not in unc] + [r_ for r_ in (w.get('reject') or []) if r_ not in ovl]
    ninf = float('-inf')

    def _f(v_):
        return float(v_) if isinstance(v_, (int, float)) and not isinstance(v_, bool) and v_ == v_ else ninf
    pp = _f(w.get('pp_max'))
    basis = w.get('phase_status')
    if basis == 'receipt':
        lo_w, hi_w = _f(w.get('wall_lower_max')), _f(w.get('wall_max'))
    elif basis in ('bounded', 'unidentified'):
        lo_w, hi_w = _f(w.get('wall_bound_best')), _f(w.get('wall_bound_worst'))
    else:                                                        # static · mesh-dump · no_walls · not_run
        lo_w = hi_w = _f(w.get('wall_max'))
    x_lo, x_hi = max(pp, lo_w), max(pp, hi_w)
    mo = float(w.get('max_ovl', CONTRACT_MAX_OVL))
    out = dict(schema='mixer_contact_status/1', max_ovl=mo, soft_range_pct=soft_range_pct, soft_range_eps=SOFT_RANGE_EPS,
               technical='FAIL' if hard else 'OK', why=hard[:6], wall_basis=basis,
               x_lo_pct=x_lo * 100.0 if x_lo != ninf else None, x_hi_pct=x_hi * 100.0 if x_hi != ninf else None,
               original_1pct=None, soft_range=None, status='TECH_FAIL')
    if hard or x_hi == ninf:
        if x_hi == ninf and not hard:
            out['why'] = ['관측값이 없다 (창 프레임 없음)']
            out['technical'] = 'FAIL'
        return out
    out['original_1pct'] = 'NOT_MET' if x_lo > mo else ('MET' if x_hi <= mo else None)
    if soft_range_pct is None:
        out['status'] = {'MET': 'CONTRACT_MET', 'NOT_MET': 'CONTRACT_NOT_MET'}.get(out['original_1pct'], 'TECH_FAIL')
        if out['original_1pct'] is None:
            out['why'] = sorted(unc)[:3] or ['1 % 판정 불가']
        return out
    thr = float(soft_range_pct) + SOFT_RANGE_EPS
    out['soft_range'] = ('OUT_OF_RANGE' if x_lo * 100.0 > thr else ('WITHIN' if x_hi * 100.0 <= thr else 'UNIDENTIFIED'))
    if out['soft_range'] == 'OUT_OF_RANGE':
        out['status'] = 'OUT_OF_RANGE'                           # 원 1 % 는 NOT_MET 그대로 (5.8 % > 1 %)
    elif out['soft_range'] == 'WITHIN' and out['original_1pct'] is not None:
        out['status'] = 'CONTRACT_MET' if out['original_1pct'] == 'MET' else 'CONTRACT_NOT_MET'
    else:
        out['why'] = sorted(unc)[:3] or ['soft 범위 · 1 % 판정 불가 (벽 위상 불확실)']
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
        for b in m.get('notes', []):
            print(f'{"":22s}   · {b}')
        st_ = m.get('status') or {}
        if st_:
            print(f'{"":22s}   ▸ 상태 {st_.get("status")} · 기술 {st_.get("technical")} · 원 1 % {st_.get("original_1pct")} · '
                  f'soft 범위 {st_.get("soft_range")} ({st_.get("soft_range_pct")}) · x {st_.get("x_lo_pct")}–{st_.get("x_hi_pct")} %')
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
        chk(f'⑩c (HBR4-04 · 나) mesh 덤프가 있어도 판정 근거로 쓰지 않는다 — 회전된 드럼 면의 참 2 % 는 PASS 로 새지 않고 TECH '
            f'(unidentified · 예정각 값 {w["wall_max"]*100:.2f} % 는 미검증) · notes 에 사유',
            w['verdict'] == 'TECH' and w['phase_status'] == 'unidentified' and abs(w['wall_max'] - 0.02) < 1e-6
            and any('HBR4-04' in n for n in w['notes']))
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

    import hashlib as _hl

    def _sha_f(p_):
        return _hl.sha256(open(p_, 'rb').read()).hexdigest()

    def _launch(run_, lmp='a' * 64, **over):
        """판정할 런의 발사 봉인 (launch_highbo.sh 의 launch_record.json 꼴) — 지금 파일의 sha256 으로."""
        rec = dict(schema='mixer_highbo_launch_record/1', run=os.path.basename(run_), stage='first', lmp_sha256=lmp,
                   sha256={f_: _sha_f(os.path.join(run_, f_)) for f_ in ('in.mixer', 'Drum.stl', 'Front.stl', 'Back.stl')})
        rec.update(over)
        _json.dump(rec, open(os.path.join(run_, 'launch_record.json'), 'w'))

    def _receipt1(td, run_, name='receipt1.json', launch=True, **kw):
        """봉인된 (v2) 영수증 — 이 시험 덱과 **맞게** 만든다 (주기 · dt · 축 · 운동 서명 · 운동 시계 · 배너 · 범위 · 목록 · 경계).
        kw 로 한 칸씩 망가뜨린다.  launch=True 면 런에 발사 봉인이 없을 때 **지금 파일로** 하나 둔다 (시험 전용)."""
        open(os.path.join(run_, 'log.lmp'), 'w').write(BANNER + '\nCreated orthogonal box\n')
        dk = open(os.path.join(run_, 'in.mixer')).read()
        sp = deck_walls(dk)
        stA, stB = list(range(0, 14001, 500)), list(range(9000, 14001, 500))
        files = {f'{p_}/{n_}': 'f' * 64 for p_ in ('A', 'B') for n_ in ('Drum.stl', 'Front.stl', 'Back.stl')}
        files.update({'A/in.phase_a': 'f' * 64, 'B/in.phase_b': 'f' * 64})
        v = dict(schema=RECEIPT_SCHEMA, test='restart_phase', passed=True, period=sp['moves']['Drum']['period'],
                 dt=sp['dt'], axis=[1.0, 0.0, 0.0], angle_error_deg=1e-5, angle_bound_deg=1e-5, binary_sha256='a' * 64,
                 liggghts_version=BANNER, motion_signature=motion_signature(dk, run_), motion_clock=motion_clock(dk),
                 rotation_start_step=sp['moves']['Drum']['start_step'], span_rotation_steps=10 ** 7,
                 steps_checked_A=stA, steps_checked_B=stB, ab_max_vertex_diff_m=0.0, residual_max_m=0.0, pos_bound_m=0.0,
                 seal=dict(binary_sha256='a' * 64, files=files),
                 run_status=dict(A=dict(exit=0, complete=True, dumps_n=len(stA)), B=dict(exit=0, complete=True, dumps_n=len(stB))))
        v.update(kw)
        if launch and not os.path.isfile(os.path.join(run_, 'launch_record.json')):
            _launch(run_)
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
        chk(f'㉓ ★ HBR3-04: 끝판 없는 (Drum 만) mesh 덤프로 끝판 2 % 를 놓치지 않는다 — 덤프는 근거가 아니고 (HBR4-04) 끝판 겹침은 회전과 '
            f'무관해 상·하한으로 REJECT ({w["verdict"]} · {w["phase_status"]})',
            w['verdict'] == 'REJECT' and w['phase_status'] == 'bounded' and any('HBR4-04' in n for n in w['notes']))
        try:
            mesh_dump_container(os.path.join(run, 'post_mesh', 'mesh_2500.stl'), run, deck_walls(open(os.path.join(run, 'in.mixer')).read()),
                                2500, float(np.radians(PHASE_EPS_DEG)))
            _rej = False
        except (ValueError, SystemExit):
            _rej = True
        chk('㉓e mesh_dump_container 자체는 끝판 없는 덤프를 여전히 거부한다 (면 연결 검증 (가) 를 세울 때의 바탕)', _rej)
        for st in (2000, 2500, 3000):
            _mesh_part(st, _th(st), ('Drum.stl', 'Front.stl'))
        w = check_window(run)
        chk('㉓b 끝판 하나 빠진 mesh 덤프도 근거가 아니다 → 끝판 2 % 는 상·하한으로 REJECT',
            w['verdict'] == 'REJECT' and w['phase_status'] == 'bounded' and any('HBR4-04' in n for n in w['notes']))
        for st in (2000, 2500, 3000):
            _mesh_part(st, _th(st) + _m.radians(5.0), ('Drum.stl', 'Front.stl', 'Back.stl'))
        w = check_window(run)
        chk('㉓c 예정각과 5° 어긋난 (다른 시각/런) 전체 mesh 덤프도 근거가 아니다 → 상·하한으로 REJECT',
            w['verdict'] == 'REJECT' and w['phase_status'] == 'bounded' and any('HBR4-04' in n for n in w['notes']))
        for st in (2000, 2500, 3000):
            _mesh_part(st, _th(st), ('Drum.stl', 'Front.stl', 'Back.stl'))
        w = check_window(run)
        chk(f'㉓d 완전한 mesh 덤프도 근거가 아니지만 (HBR4-04) 끝판 2 % 는 회전과 무관해 상·하한으로 REJECT '
            f'({w["phase_status"]} · {w["wall_max"]*100:.2f} % · {w["wall_max_mesh"]})',
            w['verdict'] == 'REJECT' and w['phase_status'] == 'bounded' and abs(w['wall_max'] - 0.02) < 1e-6)
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
    # ══ ㉖~㉚ 2026-09-28 Codex 4 차 HBR4-01 · 02 · 03 · 04 · 07 — 반례를 **먼저 재현**하고 고친다 ══════════════════════════
    #   (docs/reviews/codex_mixer_highbo_round4_evidence_20260928/review_round4_probe.py 의 경우들을 이 12 각형 기하로)
    import shutil as _sh2
    with tempfile.TemporaryDirectory() as td:            # ㉖ HBR4-01 (소비자) — 빈 봉인 목록 · 빈 덤프 목록 · 비유한 지표
        run = _run(td)
        for st in (2000, 2500, 3000):
            _dump(run, st, BASE + _pair(0.0025) + _ring(_th(st), 0.005))
        _launch(run)
        w = check_window(run, phase_receipt=_receipt1(td, run))
        chk(f'㉖ (대조) 완전한 영수증 + 발사 봉인 → 받는다 ({w["phase_status"]} · {w["verdict"]})',
            w['phase_status'] == 'receipt' and w['verdict'] == 'PASS')
        for k_, kw_ in {'봉인 파일 목록이 빈 객체 (empty_seal_lists_receipt)': dict(seal=dict(binary_sha256='a' * 64, files={})),
                        '덤프 해시 목록이 빈 (dumps_n 0)': dict(run_status=dict(A=dict(exit=0, complete=True, dumps_n=0),
                                                                              B=dict(exit=0, complete=True, dumps_n=0))),
                        'A↔B 차가 비유한 (nan_B_receipt)': dict(ab_max_vertex_diff_m=float('nan'))}.items():
            w = check_window(run, phase_receipt=_receipt1(td, run, name=f'h1_{abs(hash(k_))}.json', **kw_))
            chk(f'㉖b ★ HBR4-01 재현→수정: {k_} → 영수증 거부', w['phase_status'] != 'receipt' and any('영수증' in t for t in w['tech']))
    with tempfile.TemporaryDirectory() as td:            # ㉗ HBR4-02 — 영수증 바이너리 · 운동 시계를 **판정할 런**에 잇는다
        run = _run(td)
        for st in (2000, 2500, 3000):
            _dump(run, st, BASE + _pair(0.0025) + _ring(_th(st), 0.005))
        _launch(run, lmp='c' * 64)                        # 이 런을 실행한 바이너리 ≠ 영수증 바이너리 ('a'*64) · 배너는 같다
        w = check_window(run, phase_receipt=_receipt1(td, run))
        chk('㉗ ★ HBR4-02 재현→수정: 영수증 바이너리 ≠ 판정할 런의 발사 봉인 lmp_sha256 (배너는 같다) → 영수증 거부 (binary_mismatch_accepted)',
            w['phase_status'] != 'receipt' and any('바이너리' in t for t in w['tech']))
        os.remove(os.path.join(run, 'launch_record.json'))
        w = check_window(run, phase_receipt=_receipt1(td, run, name='nolr.json', launch=False))
        chk('㉗b 판정할 런에 발사 봉인이 없으면 (실행 당시 바이너리 미상) 영수증을 잇지 않는다 — 지금 파일을 해시해 채우지 않는다',
            w['phase_status'] != 'receipt' and any('launch_record' in t for t in w['tech']))
        _launch(run)
        rp_ = _receipt1(td, run, name='rs2001.json')          # 회전 시작 2001 덱으로 만든 영수증
        open(os.path.join(run, 'in.mixer'), 'w').write(
            _deck().replace('run 1000\nrun 1000\n', 'run 1000\nrun 1000\nrun 1000\n').replace('run 12000\n', 'run 11000\n'))
        _launch(run)                                          # 새 덱을 봉인 — 바이너리 · 덱 봉인은 정상이고 다른 것은 **시계**뿐
        w = check_window(run, phase_receipt=rp_)
        chk('㉗c ★ HBR4-02 재현→수정: 회전 시작 2001 로 잰 영수증을 시작 3001 덱에 쓰지 않는다 (운동 서명 · step 부분집합은 같다 — '
            'rotation_start_mismatch_accepted)', w['phase_status'] != 'receipt' and any('시계' in t for t in w['tech']))
        open(os.path.join(run, 'in.mixer'), 'w').write(_deck())
        _launch(run)
        open(os.path.join(run, 'in.resume'), 'w').write('# make_mixer_resume 산출 흉내\n')
        w = check_window(run, phase_receipt=_receipt1(td, run, name='resumed.json'))
        chk('㉗d 재개된 런 (in.resume) 은 이 영수증으로 잇지 않는다 — 런별 상태 확인 (3차 Q5) 은 이 영수증이 아니다',
            w['phase_status'] != 'receipt' and any('재개' in t for t in w['tech']))
    with tempfile.TemporaryDirectory() as td:            # ㉘ HBR4-03 — 생산자가 허용한 형상 잔차를 부호거리에 넣는다
        run = _run(td)
        xh = XH_ * SC_
        rr_ = 2e-4
        for st in (2000, 2500, 3000):
            _dump(run, st, BASE + _pair(0.0025) + [(7, 3, xh - (1 - 0.0095) * rr_, 0.0, 0.003, rr_)])   # 원 STL 로 끝판 δ/r 0.95 %
        _launch(run)
        pb = float(np.sqrt(3.0) * 8e-8)                      # +80 nm 평행이동 (생산자 허용 1e-7 안) — 좌표 최대 잔차 → 거리 √3 배
        w = check_window(run, phase_receipt=_receipt1(td, run, residual_max_m=8e-8, pos_bound_m=pb))
        chk(f'㉘ ★ HBR4-03 재현→수정: 원 STL 로 0.95 % 인 끝판 겹침을 위치 경계 {pb*1e9:.0f} nm 를 빼고 PASS 로 넘기지 않는다 '
            f'(translation_receipt · {w["verdict"]} · 상한 {w.get("wall_max", 0)*100:.4f} %)',
            w['verdict'] == 'TECH' and w['phase_status'] == 'receipt' and w['wall_max'] > 0.01 and w['wall_lower_max'] < 0.01)
        w = check_window(run, phase_receipt=_receipt1(td, run, name='pb0.json', residual_max_m=0.0, pos_bound_m=0.0))
        chk('㉘b (대조) 위치 경계 0 이면 같은 0.95 % 는 PASS — 경계가 판정을 무조건 막는 것이 아니다',
            w['verdict'] == 'PASS' and w['phase_status'] == 'receipt')
    with tempfile.TemporaryDirectory() as td:            # ㉙ HBR4-04 — 면 연결 없이 꼭짓점 집합만 보존한 퇴화 끝판
        run = _run(td)
        xh = XH_ * SC_
        for st in (2000, 2500, 3000):
            _dump(run, st, BASE + _pair(0.0025) + [(7, 3, xh - 0.98 * 2e-4, 0.0, 0.003, 2e-4)])        # 원 Front 에 δ/r 2 %
        os.makedirs(os.path.join(run, 'post_mesh'), exist_ok=True)
        for st in (2000, 2500, 3000):
            Rm = _rot(np.array([1.0, 0, 0]), _th(st))
            tris = []
            for nm in ('Drum.stl', 'Front.stl', 'Back.stl'):
                for t_ in read_stl(os.path.join(run, nm)) * SC_:
                    if nm == 'Front.stl':
                        t_ = np.array([t_[0], t_[1], t_[0]])          # [중심, 테두리점, 중심] — 면 수 · 꼭짓점 집합은 그대로
                    tris.append(tuple(map(tuple, t_ @ Rm.T)))
            _stl(os.path.join(run, 'post_mesh', f'mesh_{st}.stl'), tris)
        w = check_window(run)
        chk(f'㉙ ★ HBR4-04 재현→수정: Front 를 [중심·테두리·중심] 으로 퇴화시킨 mesh 덤프로 끝판 2 % 를 놓치지 않는다 '
            f'(degenerate_front_false_pass · {w["verdict"]} · {w["phase_status"]})',
            w['verdict'] == 'REJECT' and w['phase_status'] != 'mesh-dump')
    with tempfile.TemporaryDirectory() as td:            # ㉚ HBR4-07 — 정지 E0 의 정적 벽 계약 (과잉차단 → 증거 경로)
        run = _run(td)
        e0 = _deck().replace('run 12000\n', 'run 0\n')        # 회전 0 (E0) — 운동 fix 는 있으되 한 step 도 돌지 않는다
        open(os.path.join(run, 'in.mixer'), 'w').write(e0)
        half_ = APO * _m.tan(_m.pi / NP_)
        near_v = (7, 3, *_on_facet(0.0, 2, 2e-4, 0.005, u=0.9 * half_), 2e-4)   # 꼭짓점 옆 · 참 δ/r 0.5 % (각 모르면 가능 범위가 넓다)
        _dump(run, 2000, BASE + _pair(0.0025) + [near_v])
        ref = os.path.join(td, 'ref')
        os.makedirs(ref)
        for nm in ('Drum.stl', 'Front.stl', 'Back.stl'):
            _sh2.copyfile(os.path.join(run, nm), os.path.join(ref, nm))
        exp_ = os.path.join(td, 'expect_e0.mixer')
        open(exp_, 'w').write(e0)
        w = check_window(run, expect_deck=exp_, stl_ref_dir=ref)
        chk(f'㉚ ★ HBR4-07 재현→수정: 회전 0 · fresh · 원 STL · 기대 덱 = 정적 벽 (θ = 0) → 꼭짓점 옆 0.5 % 를 PASS (E0_static_contract · '
            f'{w["verdict"]} · {w["phase_status"]} · {w["wall_max"]*100:.3f} %)',
            w['verdict'] == 'PASS' and w['phase_status'] == 'static' and abs(w['wall_max'] - 0.005) < 1e-6)
        _dump(run, 2000, BASE + _pair(0.0025) + [(7, 3, *_on_facet(0.0, 3, 2e-4, 0.02), 2e-4)])
        w = check_window(run, expect_deck=exp_, stl_ref_dir=ref)
        chk(f'㉚b 정적 벽에서 2 % 는 REJECT ({w["verdict"]} · {w["phase_status"]})', w['verdict'] == 'REJECT' and w['phase_status'] == 'static')
        _dump(run, 2000, BASE + _pair(0.0025) + [near_v])
        for k_, (mut, undo) in {
                'STL 이 캠페인 원본과 다르다': (lambda: open(os.path.join(run, 'Back.stl'), 'a').write('\n'),
                                          lambda: _sh2.copyfile(os.path.join(ref, 'Back.stl'), os.path.join(run, 'Back.stl'))),
                '덱이 기대 덱과 다르다': (lambda: open(os.path.join(run, 'in.mixer'), 'w').write(e0.replace('timestep 1e-6', 'timestep 2e-6')),
                                     lambda: open(os.path.join(run, 'in.mixer'), 'w').write(e0)),
                '재개 흔적 (in.resume)': (lambda: open(os.path.join(run, 'in.resume'), 'w').write('#\n'),
                                       lambda: os.remove(os.path.join(run, 'in.resume')))}.items():
            mut()
            w = check_window(run, expect_deck=exp_, stl_ref_dir=ref)
            chk(f'㉚c 음성 대조 — {k_} → 정적 계약 불성립 (static 아님 · {w["verdict"]})', w['phase_status'] != 'static' and w['verdict'] != 'PASS')
            undo()
        w = check_window(run, stl_ref_dir=ref)
        chk('㉚d 기대 덱 (--expect-deck) 없이는 입력 동일성을 세우지 못해 정적 계약을 주지 않는다', w['phase_status'] != 'static')
    # ══ ㉛ 2026-09-28 (1저자 결정: LH 를 ibb SLURM 으로) — SLURM 봉인은 러너의 시작 대조 기록 (job_start.json) 까지 잇는다 ══════
    #   로컬 발사는 봉인 바로 뒤 exec 라 틈이 없다 (Codex Q5).  SLURM 은 제출 ↔ 시작 사이 대기열 틈이 있어, 러너의 시작 대조
    #   (dem_scripts/mixer_20260921/start_check.py) 가 남긴 통과 기록이 봉인과 맞아야 "실행된 바이너리 = 봉인" 이 선다.
    with tempfile.TemporaryDirectory() as td:
        run = _run(td)
        for st in (2000, 2500, 3000):
            _dump(run, st, BASE + _pair(0.0025) + _ring(_th(st), 0.005))
        SL_ = dict(np=20, runner='run_lh.sbatch', runner_sha256='d' * 64, start_check_sha256='e' * 64)
        _launch(run, backend='slurm', slurm=SL_)
        w = check_window(run, phase_receipt=_receipt1(td, run, name='s0.json'))
        chk('㉛ ★ SLURM 봉인인데 시작 대조 기록 (job_start.json) 이 없으면 영수증을 잇지 않는다 (대기열 틈 — 실행된 바이너리 미상)',
            w['phase_status'] != 'receipt' and any('job_start' in t for t in w['tech']))
        good_ = dict(schema='mixer_highbo_job_start/1', ok=True, lmp_sha256='a' * 64, runner_sha256_executed='d' * 64,
                     start_check_sha256='e' * 64, launch_record_sha256=_sha_f(os.path.join(run, 'launch_record.json')),
                     slurm_ntasks=20)
        _json.dump(good_, open(os.path.join(run, 'job_start.json'), 'w'))
        w = check_window(run, phase_receipt=_receipt1(td, run, name='s1.json'))
        chk(f'㉛b (대조) 시작 대조 기록이 봉인과 맞으면 받는다 ({w["phase_status"]} · {w["verdict"]})',
            w['phase_status'] == 'receipt' and w['verdict'] == 'PASS')
        for k_, (key_, val_) in {'바이너리': ('lmp_sha256', 'c' * 64), '실행된 러너': ('runner_sha256_executed', '0' * 64),
                                 '시작 대조기': ('start_check_sha256', '1' * 64), 'ntasks': ('slurm_ntasks', 19),
                                 '봉인 sha256': ('launch_record_sha256', '2' * 64), 'ok (문자열 "true")': ('ok', 'true'),
                                 '스키마': ('schema', 'x')}.items():
            bad_ = dict(good_)
            bad_[key_] = val_
            _json.dump(bad_, open(os.path.join(run, 'job_start.json'), 'w'))
            w = check_window(run, phase_receipt=_receipt1(td, run, name=f's_{key_}.json'))
            chk(f'㉛c 시작 대조 기록의 {k_} 가 봉인과 다르면 영수증을 잇지 않는다',
                w['phase_status'] != 'receipt' and any('job_start' in t for t in w['tech']))
        _json.dump(good_, open(os.path.join(run, 'job_start.json'), 'w'))
        _launch(run)                                          # 로컬 봉인 (backend 없음) — job_start.json 은 요구하지 않는다
        os.remove(os.path.join(run, 'job_start.json'))
        w = check_window(run, phase_receipt=_receipt1(td, run, name='s_local.json'))
        chk('㉛d (대조) 로컬 봉인은 시작 대조 기록 없이도 그대로 받는다 (틈이 없다)', w['phase_status'] == 'receipt' and w['verdict'] == 'PASS')
    # ══ ㉜~㉟ 2026-09-30 — 강성 축 코드 선행조건 2 단계 piece 3: bin 창 · 상태 필드 · --soft-range (사전등록 §6 · §4 a′) ══════════════
    #    ★ 반례를 먼저 옮겼다 — 옛 판: check_window 에 bins · soft_range_pct 가 없다 (TypeError) · contract_status 없음 · CLI --soft-range ·
    #      --bins 없음 ⇒ ㉜~㉟ 전부 FAIL.
    G_ = globals()

    def _okx(fn):
        try:
            return bool(fn())
        except Exception as e_:                                       # noqa: BLE001 — 옛 판의 TypeError · NameError 를 FAIL 로
            print(f'        ({type(e_).__name__}: {str(e_)[:100]})')
            return False

    def _run_rev(td_, gaps, name='rr'):
        """1000 step/바퀴 덱 (bin 0 = [2000, 3000) · bin 1 = [3000, 4000)) · 프레임 = {step: 짝 간격}."""
        run_ = os.path.join(td_, name)
        os.makedirs(os.path.join(run_, 'post'))
        _geom(run_)
        open(os.path.join(run_, 'in.mixer'), 'w').write(_deck(0.001))
        for st_, g_ in gaps.items():
            _dump(run_, st_, BASE + _pair(g_))
        return run_
    with tempfile.TemporaryDirectory() as td:
        run = _run_rev(td, {2000: 0.0025, 2500: 0.0025, 3000: 0.00198, 3500: 0.0025})
        w_all = check_window(run)
        chk(f'㉜ (대조) 창 전체는 bin 1 의 2 % 를 기각 ({w_all["verdict"]} @ {w_all["pp_max_step"]})',
            w_all['verdict'] == 'REJECT' and w_all['pp_max_step'] == 3000)
        r32 = {}

        def _t32():
            w0 = check_window(run, bins=(0,))
            w1 = check_window(run, bins=(1,))
            r32.update(w0=w0['verdict'], w1=w1['verdict'])
            os.remove(os.path.join(run, 'post', 'mix_2500.liggghts'))
            wm = check_window(run, bins=(0,))
            w5 = check_window(run, bins=(5,))
            _dump(run, 2500, BASE + _pair(0.0025))
            r32.update(miss=wm['verdict'], empty=w5['verdict'])
            return (w0['verdict'] == 'PASS' and w0['n_frames'] == 2 and tuple(w0['window']) == (2000, 2500) and w0['bins'] == [0]
                    and w1['verdict'] == 'REJECT' and w1['pp_max_step'] == 3000
                    and wm['verdict'] == 'TECH' and any('결손' in t_ for t_ in wm['tech'])
                    and w5['verdict'] == 'TECH')
        chk(f'㉜b ★ bins=(0,) = 판독기 bin 0 창만 (§4 a′) — bin 0 (2000 · 2500) PASS · bin 1 은 2 % REJECT · bin 0 격자 결손 (2500 없음) = TECH · '
            f'빈 bin (5) = TECH {r32}', _okx(_t32))

    #  ㉝ contract_status 표 — ref (계약 팔) · soft (진단 팔 · 5.8 %) × 기술 / 1 % / 범위 (§6 세 축)
    def _W(**k_):
        d_ = dict(max_ovl=0.01, tech=[], reject=[], reject_overlap=[], tech_wall_uncertain=[], phase_status='static',
                  pp_max=0.005, wall_max=0.004)
        d_.update(k_)
        return d_
    PPR = 'pp 기각'
    U_ = '위상 불확실성으로 미식별 (합성)'
    TAB = [  # (이름, 입력, soft 범위, 기대 status, 기대 original, 기대 soft)
        ('ref 0.5 %', _W(), None, 'CONTRACT_MET', 'MET', None),
        ('ref 2 %', _W(pp_max=0.02, reject=[PPR], reject_overlap=[PPR]), None, 'CONTRACT_NOT_MET', 'NOT_MET', None),
        ('soft 0.5 %', _W(), 5.8, 'CONTRACT_MET', 'MET', 'WITHIN'),
        ('soft 5 %', _W(pp_max=0.05, reject=[PPR], reject_overlap=[PPR]), 5.8, 'CONTRACT_NOT_MET', 'NOT_MET', 'WITHIN'),
        ('soft 경계 5.8 % (= 등록 · 여유 1e-9 안)', _W(pp_max=0.058, reject=[PPR], reject_overlap=[PPR]), 5.8, 'CONTRACT_NOT_MET', 'NOT_MET', 'WITHIN'),
        ('soft 5.8001 %', _W(pp_max=0.058001, reject=[PPR], reject_overlap=[PPR]), 5.8, 'OUT_OF_RANGE', 'NOT_MET', 'OUT_OF_RANGE'),
        ('soft 벽 7 % (static)', _W(wall_max=0.07, reject=['벽'], reject_overlap=['벽']), 5.8, 'OUT_OF_RANGE', 'NOT_MET', 'OUT_OF_RANGE'),
        ('ref 창 결손 (기술)', _W(tech=['창 안 덤프 결손 1 개']), None, 'TECH_FAIL', None, None),
        ('soft 창 결손 (기술)', _W(pp_max=0.05, tech=['창 안 덤프 결손 1 개'], reject=[PPR], reject_overlap=[PPR]), 5.8, 'TECH_FAIL', None, None),
        ('soft 보존 실패 (겹침 아닌 기각 = 기술)', _W(reject=['step 2500: 상별 입자 수 {1: 3} ≠ t₀ {1: 4}']), 5.8, 'TECH_FAIL', None, None),
        ('ref 벽 위상 불확실 (1 % 걸침)', _W(phase_status='receipt', pp_max=0.002, wall_lower_max=0.008, wall_max=0.012, tech=[U_],
                                        tech_wall_uncertain=[U_]), None, 'TECH_FAIL', None, None),
        ('soft 벽 위상 불확실 + 입자 5 % (1 % 는 확정 NOT_MET)', _W(phase_status='receipt', pp_max=0.05, wall_lower_max=0.008, wall_max=0.012,
                                                            tech=[U_], tech_wall_uncertain=[U_], reject=[PPR], reject_overlap=[PPR]),
         5.8, 'CONTRACT_NOT_MET', 'NOT_MET', 'WITHIN'),
        ('soft 범위 걸침 (벽 5.5–6.0 %)', _W(phase_status='receipt', pp_max=0.03, wall_lower_max=0.055, wall_max=0.060, reject=[PPR, '벽 명백'],
                                          reject_overlap=[PPR, '벽 명백']), 5.8, 'TECH_FAIL', 'NOT_MET', 'UNIDENTIFIED'),
        ('ref unidentified (상·하한 0.4–3 %)', _W(phase_status='unidentified', pp_max=0.002, wall_bound_best=0.004, wall_bound_worst=0.03,
                                                tech=[U_], tech_wall_uncertain=[U_]), None, 'TECH_FAIL', None, None),
    ]

    def _t33():
        cs = G_['contract_status']
        bad = []
        for nm_, w_, sr_, st_, og_, so_ in TAB:
            r_ = cs(w_, sr_)
            if (r_['status'], r_['original_1pct'], r_['soft_range']) != (st_, og_, so_) or r_['status'] not in G_['CONTRACT_STATUSES']:
                bad.append(f'{nm_}: {r_["status"]}/{r_["original_1pct"]}/{r_["soft_range"]}')
        try:
            cs(_W(), 6.0)
            bad.append('soft 6.0 을 받았다')
        except ValueError:
            pass
        if bad:
            print('        ' + ' | '.join(bad))
        return not bad and G_['SOFT_RANGE_PCT'] == 5.8 and abs(0.01 * 14 ** (2 / 3) * 100 - 5.81) < 0.005
    chk(f'㉝ ★ 상태 표 (§6 세 축 분리 · {len(TAB)} 행) — ref: MET · NOT_MET · 기술 실패 · 1 % 걸침 = TECH_FAIL / soft (5.8 %): 1 % 초과는 '
        'CONTRACT_NOT_MET (기술 실패 아님) · 경계 5.8 % 는 WITHIN (여유 1e-9) · 5.8001 % · 벽 7 % = OUT_OF_RANGE · 보존 실패 · 창 결손 = TECH_FAIL · '
        '벽 위상 불확실이어도 입자 5 % 면 1 % 는 확정 NOT_MET · 범위 걸침 = TECH_FAIL · 등록 밖 범위 (6.0) 거부 · 5.8 = 1 % × 14^(2/3) 반올림',
        _okx(_t33))

    #  ㉞ 실제 check_window 에 상태가 붙는다 (합성 덱)
    with tempfile.TemporaryDirectory() as td:
        def _t34():
            ok_ = []
            r2 = _run_rev(td, {2000: 0.0025, 2500: 0.00198}, 'r2')             # bin 0 에 2 %
            ok_.append(check_window(r2, bins=(0,), soft_range_pct=5.8)['status']['status'] == 'CONTRACT_NOT_MET')
            ok_.append(check_window(r2, bins=(0,))['status']['status'] == 'CONTRACT_NOT_MET')
            r7 = _run_rev(td, {2000: 0.0025, 2500: 0.00193}, 'r7')             # bin 0 에 7 %
            s7 = check_window(r7, bins=(0,), soft_range_pct=5.8)['status']
            ok_.append(s7['status'] == 'OUT_OF_RANGE' and s7['original_1pct'] == 'NOT_MET' and abs(s7['x_hi_pct'] - 7.0) < 1e-6)
            r0 = _run_rev(td, {2000: 0.0025, 2500: 0.0025}, 'r0')
            ok_.append(check_window(r0, bins=(0,), soft_range_pct=5.8)['status']['status'] == 'CONTRACT_MET')
            os.remove(os.path.join(r0, 'post', 'mix_2500.liggghts'))
            ok_.append(check_window(r0, bins=(0,), soft_range_pct=5.8)['status']['status'] == 'TECH_FAIL')
            rl = _run_rev(td, {2000: 0.0025}, 'rl')                             # 입자 하나 잃음 (보존 실패 = 기각이지만 상태는 기술 실패)
            _dump(rl, 2500, BASE[:3] + _pair(0.0025))
            wl = check_window(rl, bins=(0,), soft_range_pct=5.8)
            ok_.append(wl['verdict'] == 'REJECT' and wl['status']['status'] == 'TECH_FAIL' and wl['status']['technical'] == 'FAIL')
            print(f'        {ok_}')
            return all(ok_)
        chk('㉞ ★ check_window 결과에 상태가 붙는다 — bin 0 에 2 % (soft · ref 둘 다 CONTRACT_NOT_MET) · 7 % soft = OUT_OF_RANGE (x_hi 7 %) · '
            '0.25 % = CONTRACT_MET · bin 0 결손 = TECH_FAIL · 입자 잃음 = 판정 REJECT 이지만 상태는 TECH_FAIL (기술 실패 ≠ 계약 미달)', _okx(_t34))

    #  ㉟ CLI — --soft-range 는 등록값 5.8 만 · --bins · JSON 에 상태
    with tempfile.TemporaryDirectory() as td:
        def _t35():
            import subprocess as _spx
            r2 = _run_rev(td, {2000: 0.0025, 2500: 0.00198}, 'c2')
            js = os.path.join(td, 'o.json')
            me = os.path.abspath(__file__)
            p1 = _spx.run([sys.executable, me, '--contract', r2, '--bins', '0', '--soft-range', '5.8', '--json', js], capture_output=True, text=True)
            j1 = _json.load(open(js))[0]
            p2 = _spx.run([sys.executable, me, '--contract', r2, '--bins', '0', '--soft-range', '6'], capture_output=True, text=True)
            return (j1['status']['status'] == 'CONTRACT_NOT_MET' and j1['status']['soft_range'] == 'WITHIN' and j1['bins'] == [0]
                    and '상태 CONTRACT_NOT_MET' in p1.stdout and p2.returncode == 2 and '5.8' in p2.stderr)
        chk('㉟ CLI: --contract --bins 0 --soft-range 5.8 → JSON · 화면에 상태 (CONTRACT_NOT_MET · WITHIN) · --soft-range 6 → rc 2 (등록 5.8 만 · '
            '올리지 않는다)', _okx(_t35))
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
                         '벽 회전각 근거 = 정지 벽 (회전 전 · --expect-deck) > 영수증 v2 (+ 발사 봉인) > 상·하한 (post_mesh/ 덤프는 근거 아님 · HBR4-04)')
    ap.add_argument('--phase-receipt', default=None,
                    help='(--contract) 재개-위상 영수증 JSON (scripts/mixer_restart_phase_test.py) — 있으면 벽을 예정각 ± 오차로 잰다')
    ap.add_argument('--launch-record', default=None,
                    help='(--contract) 판정할 런의 발사 봉인 JSON (기본 <런>/launch_record.json) — 영수증 바이너리를 이것과 대조한다 (HBR4-02)')
    ap.add_argument('--expect-deck', default=None,
                    help='(--contract) 정지 벽 계약의 기대 덱 (생성기로 다시 만든 등록 덱, 예 E0) — 입력 동일성 (HBR4-07)')
    ap.add_argument('--stl-ref', default=None, help='(--contract) 정지 벽 계약의 캠페인 원본 STL 폴더 (기본 dem_scripts/mixer_20260919)')
    ap.add_argument('--expect-types', default=None, help='(--contract) t₀ 상별 입자 수, 예 "1:36,2:421,3:32832"')
    ap.add_argument('--soft-range', type=float, default=None,
                    help=f'(--contract) soft 진단 팔 (강성 축 사전등록 §6) — 등록값 {SOFT_RANGE_PCT} 만 받는다 (올리지 않는다).  결과에 상태 '
                         f'(TECH_FAIL · CONTRACT_MET · CONTRACT_NOT_MET · OUT_OF_RANGE) · 원 1 %% · soft 범위를 따로 적는다.  없으면 ref/ref2 (계약 팔)')
    ap.add_argument('--bins', default=None, help='(--contract) 판독기 bin 창만 (예 "0" = 사전등록 §4 a′ bin 0 창) — 그 bin 의 계획 격자 전부 필수')
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
        if a.soft_range is not None and a.soft_range != SOFT_RANGE_PCT:
            ap.error(f'--soft-range {a.soft_range:g} — 등록 soft 진단 범위는 {SOFT_RANGE_PCT} % 뿐이다 (§6 · 올리거나 내리지 않는다)')
        bins_ = [int(x) for x in a.bins.split(',')] if a.bins else None
        rs = [check_window(d, a.n_expected, label=labs[i] if i < len(labs) else None, phase_receipt=a.phase_receipt,
                           expect_counts=ec, diag_fit=a.diag_fit, progress=a.progress, launch_record=a.launch_record,
                           expect_deck=a.expect_deck, stl_ref_dir=a.stl_ref, bins=bins_, soft_range_pct=a.soft_range)
              for i, d in enumerate(a.dirs)]
        if a.json:
            import json
            json.dump(rs, open(a.json, 'w'), ensure_ascii=False, indent=1, default=float)
            print(f'→ {a.json}')
        raise SystemExit(report_window(rs))
    raise SystemExit(report([check(d, a.n_expected, labs[i] if i < len(labs) else None)
                             for i, d in enumerate(a.dirs)]))
