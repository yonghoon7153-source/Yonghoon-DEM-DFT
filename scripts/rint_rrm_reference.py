#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""①′ RRM — resolved reference model: **시험 전용** 해상 기준 (2026-10-13).

계약 = v2 + v3 (§2-1 CNC ↔ RRM 표 · §2-3 N9 · §8-2 D17) + v3.1 (§5 · §6) — 겹치면 뒤가 이긴다
(docs/reviews/contact_resistance_pipeline_draft_v3_20261006.md · …_v3_1_20261007.md).  판정 = docs/reviews/codex_review_rint_g2_v3_20261007.md
§5 · §7-3 (RRM 은 시험 전용 해상 기준 · 생산 경로에 넣지 않는다 · T2 개발 결과로 고른 RRM 도 그 자체 오차 확인 전에는 독립 기준이 아니다).

⛔ **생산 경로가 아니다.**  step3_sigma (생산 · ①′ 정량 코드) · mpm_webapp_payload · run_contract 는 이 모듈을 import 하지 않는다
   (scripts/test_rint_g2_rrm.py RRM-5 가 AST 로 지킨다).  PROTOCOL_FIELDS 밖 · payload CLI 없음 · 웹앱 화면 없음 — 기구 · 시험 전용.
   이 모듈은 step3_sigma 를 **읽기만** 한다 (속성 대입 · 몽키패치 없음 — 같은 시험의 AST 검사).

무엇 (v3 §2-1 RRM 열):
  support    참 원판 (근축면 위 · 반경 a) 과 겹친 S_c^surv 면만.  면 가중 w_e = 그 면이 대표하는 참 원판 면적 = (면 투영 ∩ 원판).
  면 막      r_face,e = r_type · h² / w_e  ⇒  면 막 G_e = 1e−8·w_e/r [S] · 접점 ΣG = 1e−8·Σw/r (원판을 owner 면이 다 덮으면 Σw = A_true).
  원판 밖    **절단** — g = 0 · 원장에 tombstone 행 (E6).  D17 (절단 ↔ 재구성) = **권고 기본값 절단 · 1저자 확인 전** (재구성 = 등록
             대안 · 미구현).  ⛔ 막 OFF (행 없음 = 조화평균) 로 두기 금지 = bulk 우회 → N9 `rrm_check` 가 거부한다.
  축 정렬만  축 정렬 접점은 그 축의 면만 원판에 투영 면적을 가진다 (L1 · 축별 가중이 같다 — 손 유도) · 다른 축 면 = 투영 면적 0 = 절단.
             기울기 접점의 가중 규칙 = D11 (T2-1 결과 전) → `rrm_unsupported_tilt` 거부 (조용히 CNC 로 돌아가지 않는다).
  해상 조건  a ≥ k·h — k = **호출자 인자** (기본값 없음 · D12-V 숫자는 1저자 · 시험은 픽스처 값) · 미달 = `rrm_unresolved_subgrid` 거부.
  r → 0      OFF 아님 — 원판 밖 절단이 남는다 (v3 §2-1).
  탄소       RRM 은 탄소 가림 법칙 (CNC 의 remove_area · renormalize) 을 쓰지 않는다 — 덮이고 남은 S_c^surv 면에 기하 가중만.

⚠ 이 모듈의 PASS 는 **기구의 증거**다 — RRM 자체 오차 (T3-D) · CNC 편향 (T2-4 · T3-B) 의 검증이 아니다 (D12-V 수치 봉인 전 ·
  개발 판만 · 개발 결과를 나중에 독립 검증으로 재분류하지 않는다 — 판정문 §4 · §8 · v3.1 §6-2).

★ RIMP-04 (Codex 10-14 판정문 §5 · 1저자 Q3 (가)) — N9 `rrm_check` 는 계획 기록 (resolve_k · r 표 · 예외 법칙) 을 **믿지 않는다**:
  ① 기록 (recipe) 모양 · 값 검사 (없음 · 비유한 k · 파싱 안 되는 r 표 · 모르는 법칙 = 위반)
  ② 행 값 — rface 유한 · ≥ 0 · 절단 행 = tombstone (rface 0 · ck 0) · 막 행 rface 0 은 그 접점의 등록 r = 0 일 때만 (RRM-4 경로)
  ③ 기대 접점 · 적격성 재계산 — 원장에서 막 후보 (부류 · N_c^surv · 면적) 를 r 표 **없이** 정하고, 빠진 접점 (r 없음 · 기울기 · 미해상) 은 계획 거부
     사유 수로 덮여야 한다 (메타데이터로 검사 집합을 비울 수 없다) · 남은 접점 = owner 면 전수 대조 (NaN 은 불일치)
  ④ 재현 결합 — 기록된 recipe 로 `rrm_plan` 을 다시 만들어 행 · 거부 사유가 비트 같아야 한다 (복합 변이 = 재현 불가)
★ RIMP-06 (판정문 §7) — RRM 계획 · 풀이 기록의 표준 `iface_contact_ledger` = **실제 RRM 행**에서 다시 셈 (`summary_source`) · CNC 값
  (원장 요약 · 탄소 법칙 · 균일 rface_c) = 별도 이름공간 `iface_cnc_comparison` (기록) · `cnc_comparison` (계획) · `iface_carbon_cover` = None.
"""
import math
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import step3_sigma as S3          # noqa: E402  읽기만 (생산 함수를 부르기만 한다)

#: import 시점의 step3_sigma 함수 객체 — 시험 RRM-5 가 "이 모듈이 바꾸지 않았다" 를 본다.
_S3_FN_IDS = {'solve_sigma_z': S3.solve_sigma_z, 'am_iface_plan': S3.am_iface_plan,
              'iface_require_quantitative': S3.iface_require_quantitative}

RRM_REFERENCE = 'resolved_true_disc_v1'
RRM_AREA_LAW = 'resolved_true_disc_v1 (RRM · 시험 전용 — 생산 법칙 아님 · 면 가중 = 면 ∩ 참 원판)'
RRM_OUTSIDE_LAW = 'cut'
RRM_OUTSIDE_LAW_STATUS = '권고 기본값 · 1저자 확인 전 (D17 — 재구성 (목을 원판으로 다시 raster) = 등록 대안 · 미구현)'
RRM_RESOLVE_K_STATUS = '호출자 인자 (픽스처 값) — D12-V 의 해상 조건 k 숫자가 아니다 (그 숫자는 1저자 · 실행 전)'
RRM_STATUS = ('시험 전용 RRM (resolved reference model) — 생산 경로 아님 · ①′ 정량 채택 HOLD · 검증 PASS 아님 '
              '(D12-V 수치 봉인 전 · 개발 판만 · v3.1 §6-2)')
#: 축 정렬 판정 — 중심선 단위벡터의 다른 두 성분 ≤ 이것.  합성 픽스처용 (실침대 접점은 거의 늘 기울기 → D11 전에는 RRM 밖).
RRM_AXIS_TOL = 1e-12


# ═════════════════════════ 기하 ═════════════════════════
def _circ_int(a, X):
    """∫_0^X √(a² − u²) du (|X| ≤ a 로 자른다) = (X·√(a² − X²) + a²·asin(X/a)) / 2."""
    X = max(-a, min(a, X))
    return 0.5 * (X * math.sqrt(max(a * a - X * X, 0.0)) + a * a * math.asin(X / a))


def disc_rect_area(cx, cy, a, x0, x1, y0, y1):
    """원판 (중심 (cx, cy) · 반경 a) ∩ 축 정렬 직사각형 [x0, x1] × [y0, y1] 의 **정확** 면적.

    X 를 원판 중심 기준으로 옮기고 ∫ [min(y1, s(X)) − max(y0, −s(X))]⁺ dX (s = √(a² − X²)) 를 구간별 닫힌 식으로 적분한다 —
    구간 경계 = 직사각형 끝 · s(X) = |y0| · |y1| 인 X.  각 구간에서 위 · 아래 경계가 직선인지 원호인지가 일정하다."""
    a = float(a)
    if not a > 0.0:
        return 0.0
    X0, X1, Y0, Y1 = float(x0) - cx, float(x1) - cx, float(y0) - cy, float(y1) - cy
    lo, hi = max(X0, -a), min(X1, a)
    if not hi > lo or Y1 <= -a or Y0 >= a or not Y1 > Y0:
        return 0.0
    pts = {lo, hi}
    for Y in (Y0, Y1):
        if abs(Y) < a:
            xb = math.sqrt(a * a - Y * Y)
            for v in (-xb, xb):
                if lo < v < hi:
                    pts.add(v)
    pts = sorted(pts)
    total = 0.0
    for u, v in zip(pts[:-1], pts[1:]):
        m = 0.5 * (u + v)
        s = math.sqrt(max(a * a - m * m, 0.0))
        top_c, bot_c = s < Y1, -s > Y0                     # 위 = 원호인가 · 아래 = 원호인가 (구간 안에서 일정)
        if min(Y1, s) <= max(Y0, -s):
            continue                                       # 이 구간에서 빈 집합
        I_s = _circ_int(a, v) - _circ_int(a, u)            # ∫ s dX
        top = I_s if top_c else Y1 * (v - u)
        bot = -I_s if bot_c else Y0 * (v - u)
        total += top - bot
    return max(total, 0.0)


def contact_disc(ca, ra, cb, rb):
    """두 구의 **참 접촉 원판** (근축면 위) — `lens_geometry.intersection_disc_area` 와 같은 원판 (π a² 같음).

    d = |c_b − c_a| · n = (c_b − c_a)/d · x = (d² + r_a² − r_b²)/(2d) (c_a 에서 근축면까지) · a² = r_a² − x².
    → {'p0' (원판 중심), 'n', 'a', 'x', 'd', 'axis' (축 정렬이면 0 · 1 · 2 · 아니면 None)} · 부분 겹침이 아니면 (안 닿음 · 포함) None."""
    ca = np.asarray(ca, np.float64); cb = np.asarray(cb, np.float64)
    ra, rb = float(ra), float(rb)
    v = cb - ca
    d = float(math.sqrt(float((v * v).sum())))
    if not d > 0.0 or not (ra + rb - d) > 0.0:
        return None
    x = (d * d + ra * ra - rb * rb) / (2.0 * d)
    a2 = ra * ra - x * x
    if not a2 > 0.0:
        return None
    n = v / d
    k = int(np.argmax(np.abs(n)))
    off = max(abs(float(n[j])) for j in range(3) if j != k)
    return {'p0': ca + x * n, 'n': n, 'a': math.sqrt(a2), 'x': x, 'd': d, 'axis': (k if off <= RRM_AXIS_TOL else None)}


def rrm_face_weights(ledger, q):
    """접점 q 의 S_c^surv 면 (원장 `faces` 의 cid == q ∧ surv) 과 RRM 면 가중 w (면 투영 ∩ 참 원판 · µm²).

    → {'axis', 'lin', 'o_lo', 'w', 'inside' (면 정사각형이 원판 안에 다 듦), 'disc', 'eligible' (축 정렬 원판), 'plane_dist_max' (면 평면 ↔ 원판
    평면 최대 거리 µm · 기록)}.  축 정렬이 아니거나 원판이 없으면 w 는 전부 0 · eligible False (가중 규칙 = D11 전)."""
    F, C, Pp = ledger['faces'], ledger['contacts'], ledger.get('particles')
    if Pp is None:
        raise TypeError('rrm_face_weights: 원장에 canonical 입자 (particles) 가 없다 — am_iface_ledger 의 결과를 그대로 줄 것')
    m = (F['cid'] == q) & F['surv']
    ax = F['axis'][m].astype(np.int64); lin = F['lin'][m].astype(np.int64); olo = F['o_lo'][m].astype(np.int64)
    ia, ib = int(C['a'][q]), int(C['b'][q])
    D = contact_disc(Pp['c'][ia], Pp['r'][ia], Pp['c'][ib], Pp['r'][ib])
    w = np.zeros(len(lin)); inside = np.zeros(len(lin), bool)
    out = {'axis': ax, 'lin': lin, 'o_lo': olo, 'w': w, 'inside': inside, 'disc': D, 'eligible': False, 'plane_dist_max': None}
    if D is None or D['axis'] is None:
        return out
    shape, h, lo = tuple(ledger['shape']), float(ledger['vox']), np.asarray(ledger['box_lo'], np.float64)
    k = D['axis']; u, v = [j for j in range(3) if j != k]
    ijk = np.stack(np.unravel_index(lin, shape), axis=1) if len(lin) else np.zeros((0, 3), np.int64)
    pu, pv, a = float(D['p0'][u]), float(D['p0'][v]), float(D['a'])
    pd = []
    for e in range(len(lin)):
        if ax[e] != k:
            continue                                       # 다른 축 면 = 원판 평면으로의 투영 면적 0 → 절단
        x0 = float(lo[u] + ijk[e, u] * h); y0 = float(lo[v] + ijk[e, v] * h)
        w[e] = disc_rect_area(pu, pv, a, x0, x0 + h, y0, y0 + h)
        far = math.hypot(max(abs(x0 - pu), abs(x0 + h - pu)), max(abs(y0 - pv), abs(y0 + h - pv)))
        inside[e] = far <= a
        pd.append(abs(float(lo[k] + (ijk[e, k] + 1) * h) - float(D['p0'][k])))
    out.update(eligible=True, plane_dist_max=(max(pd) if pd else None))
    return out


# ═════════════════════════ 계획 ═════════════════════════
def _film_contacts(ledger, rt, ambiguous_arm):
    """막을 질 접점 (am_iface_plan 의 realized 와 같은 규칙 — 원장 · 표 · 팔에서 독립 재계산)."""
    C = ledger['contacts']
    cls = C['cls']
    film = (cls == 0) | ((cls == 1) & (ambiguous_arm == 'a_hi'))
    A_f = np.where(cls == 0, C['A_true'], np.where(cls == 1, C['A_hi'], 0.0))
    has_r = np.array([str(k_) in rt for k_ in C['type_key']], bool) if len(cls) else np.zeros(0, bool)
    return film & (C['nsurv'] > 0) & (A_f > 0.0) & has_r


def rrm_plan(ledger, r_type, *, resolve_k, gap_law=None, unreg_law=None, ambiguous_arm=None):
    """RRM 계획 — `solve_sigma_z(iface=…)` 이 받는 행 모양 (kind `am_iface_plan`) · 기록에 `iface_reference = resolved_true_disc_v1`.

    막을 질 접점마다 S_c^surv 면 전부를 행으로: w > 0 → 막 r_face = r·h²/w · w = 0 (원판 밖 · 다른 축 면) → 절단 tombstone.
    예외 부류 (모호 · 간극 · 미등록) 의 법칙 · 거부 · 절단 행은 같은 원장의 CNC 계획 (`am_iface_plan`) 과 같다 (그 부분은 RRM 이 아니다).
    resolve_k  해상 조건 a ≥ k·h 의 k — **필수 · 기본값 없음** (D12-V 숫자를 지어내지 않는다 · 시험 = 픽스처 값)."""
    k = float(resolve_k)
    if not (math.isfinite(k) and k > 0.0):
        raise ValueError(f'rrm_plan: resolve_k 는 유한한 양수 — {resolve_k!r}')
    base = S3.am_iface_plan(ledger, r_type, gap_law=gap_law, unreg_law=unreg_law, ambiguous_arm=ambiguous_arm)
    rej = [dict(x) for x in base['rejections']]
    h = float(ledger['vox'])
    rt = S3.parse_iface_r_type(r_type)
    rows = [{'lin': [], 'rface': [], 'cut': [], 'ck': [], 'cid': [], 'olo': []} for _ in range(3)]
    info, n_tilt, n_unres = [], 0, 0
    if ledger.get('owner') is not None:
        C = ledger['contacts']
        film = _film_contacts(ledger, rt, ambiguous_arm)
        for q in np.flatnonzero(film).tolist():
            W = rrm_face_weights(ledger, q)
            D = W['disc']
            tkey = str(C['type_key'][q])
            rec_c = {'cid': int(q), 'type_key': tkey, 'a_um': (None if D is None else float(D['a'])),
                     'A_true_um2': float(C['A_true'][q]), 'n_faces': int(len(W['lin']))}
            if D is None or not W['eligible']:
                n_tilt += 1
                info.append(dict(rec_c, status='unsupported_tilt'))
                continue
            if D['a'] < k * h:
                n_unres += 1
                info.append(dict(rec_c, status='unresolved_subgrid', a_over_h=float(D['a'] / h)))
                continue
            r_q = float(rt[tkey]); ck = int(S3.SID_IFACE_AM[tkey])
            w = W['w']
            for e in range(len(W['lin'])):
                R = rows[int(W['axis'][e])]
                R['lin'].append(int(W['lin'][e])); R['cid'].append(int(q)); R['olo'].append(int(W['o_lo'][e]))
                if w[e] > 0.0:
                    R['rface'].append(float(S3.iface_rface_ohm_cm2(r_q, 1, h, float(w[e])))); R['cut'].append(False); R['ck'].append(ck)
                else:
                    R['rface'].append(0.0); R['cut'].append(True); R['ck'].append(0)
            sw = float(w.sum())
            info.append(dict(rec_c, status='reference', a_over_h=float(D['a'] / h), sum_w_um2=sw,
                             coverage=(sw / float(C['A_true'][q]) if C['A_true'][q] > 0 else None),
                             n_faces_inside=int(W['inside'].sum()), n_faces_partial=int(((w > 0.0) & ~W['inside']).sum()),
                             n_faces_outside=int((w == 0.0).sum()),
                             n_faces_offaxis=int((W['axis'] != D['axis']).sum()),
                             plane_dist_max_um=W['plane_dist_max'], film_G_S=1e-8 * sw / r_q if r_q > 0 else None))
    if n_tilt:
        rej.append({'code': 'rrm_unsupported_tilt', 'test': 'RRM', 'n': n_tilt,
                    'why': '축 정렬이 아닌 접점 — 기울기 접점의 RRM 가중 규칙 = D11 (T2-1 결과 전) · 기준 주장에서 뺀다 (CNC 로 조용히 돌아가지 않는다)'})
    if n_unres:
        rej.append({'code': 'rrm_unresolved_subgrid', 'test': 'RRM', 'n': n_unres,
                    'why': f'a < k·h (k = {k:g} · 호출자 인자) — 해상 support 0 · 기준 주장에서 뺀다 (검증된 subgrid/포트 모형 등록 전)'})
    axes = []
    for ax in range(3):
        b = base['axes'][ax]
        keep = b['cut']                                    # 예외 부류의 절단 행 (모호 cut 팔 · 간극 cut · 미등록 cut) 만 그대로
        lin = np.concatenate([b['lin'][keep], np.asarray(rows[ax]['lin'], np.int64)])
        cols = {'lin': lin,
                'rface': np.concatenate([b['rface'][keep], np.asarray(rows[ax]['rface'], np.float64)]),
                'cut': np.concatenate([b['cut'][keep], np.asarray(rows[ax]['cut'], bool)]),
                'ck': np.concatenate([b['ck'][keep], np.asarray(rows[ax]['ck'], np.int64)]),
                'cid': np.concatenate([b['cid'][keep], np.asarray(rows[ax]['cid'], np.int64)]),
                'olo': np.concatenate([b['olo'][keep], np.asarray(rows[ax]['olo'], np.int64)])}
        o = np.argsort(cols['lin'], kind='stable')
        cols = {kk: vv[o] for kk, vv in cols.items()}
        if len(lin) and np.any(np.diff(cols['lin']) == 0):
            raise ValueError(f'rrm_plan: 축 {ax} 에 같은 면 두 행 — 면은 한 접점에만 속해야 한다 (원장 결함)')
        axes.append(cols)
    plan = dict(base)
    plan['axes'] = tuple(axes)
    plan['fp_rows'] = S3._iface_rows_fp(plan['axes'])
    plan['n_film_rows'] = int(sum(int((~a_['cut']).sum()) for a_ in axes))
    plan['n_cut_rows'] = int(sum(int(a_['cut'].sum()) for a_ in axes))
    plan['rejections'] = rej
    #  ★ RIMP-06 — CNC 계획의 접점별 균일 r_face · 탄소 법칙 · realized 는 이 계획의 행이 아니다 → 비교 이름공간으로.  realized = RRM 기준 접점
    nC = len(base['realized'])
    ref_mask = np.zeros(nC, bool)
    for x in info:
        if x['status'] == 'reference':
            ref_mask[int(x['cid'])] = True
    plan['cnc_comparison'] = {'meaning': 'CNC 비교값 — 같은 원장 · 같은 r 표의 CNC 계획 (이 RRM 계획의 행이 아니다 · RIMP-06)',
                              'carbon_cover': base['carbon_cover'], 'realized': base['realized'], 'rface_c': base['rface_c'],
                              'rface_remove': base.get('rface_remove'), 'rface_renorm': base.get('rface_renorm'),
                              'n_film_rows': base['n_film_rows'], 'n_cut_rows': base['n_cut_rows']}
    for kk in ('rface_remove', 'rface_renorm'):
        plan.pop(kk, None)
    plan.update(rface_c=None, carbon_cover=None, realized=ref_mask)
    rec = dict(base['record'])
    rec.update({
        'iface_reference': RRM_REFERENCE, 'iface_area_law': RRM_AREA_LAW, 'iface_status': RRM_STATUS,
        'iface_rejections': [{k_: v_ for k_, v_ in x.items() if k_ != 'detail'} for x in rej],
        'iface_carbon_cover': None,
        'iface_carbon_cover_status': 'RRM — 탄소 가림 법칙 (CNC remove_area · renormalize) 미사용 · CNC 판 = iface_cnc_comparison (RIMP-06)',
        'iface_contact_ledger': _rrm_summary(base['record']['iface_contact_ledger'], plan, info, ledger),
        'iface_cnc_comparison': {'meaning': 'CNC 비교값 — 같은 원장 · 같은 r 표의 CNC 계획 요약 (이 RRM 계획의 행 · 풀이가 아니다 · RIMP-06)',
                                 'iface_area_law': base['record']['iface_area_law'],
                                 'iface_carbon_cover': base['record']['iface_carbon_cover'],
                                 'iface_contact_ledger': base['record']['iface_contact_ledger'],
                                 'n_film_rows': base['n_film_rows'], 'n_cut_rows': base['n_cut_rows']},
        'iface_rrm': {'outside_law': RRM_OUTSIDE_LAW, 'outside_law_status': RRM_OUTSIDE_LAW_STATUS,
                      'resolve_k': k, 'resolve_k_status': RRM_RESOLVE_K_STATUS,
                      'axis_rule': '축 정렬 접점만 (다른 축 면 = 투영 면적 0 = 절단) · 기울기 = D11 전 거부',
                      'carbon': '탄소 가림 법칙 미사용 — 덮이고 남은 S_c^surv 면에 기하 가중만',
                      'n_reference': int(sum(1 for x in info if x['status'] == 'reference')),
                      'n_unsupported_tilt': n_tilt, 'n_unresolved_subgrid': n_unres, 'contacts': info}})
    plan['record'] = rec
    return plan


#: RRM 표준 요약에 그대로 두는 CNC 요약 키 — 원장 기하 (법칙 · 행과 무관) 만.
_GEOM_SUMMARY_KEYS = ('vox_um', 'bridge_um', 'tol_am_um', 'delta_bound_um', 'n_particles', 'carbon_path_current_share',
                      'carbon_path_current_share_status', 'n_contacts', 'n_film_contacts', 'unrealized', 'unregistered',
                      'n_cells_multi_claim', 'n_faces_triple', 'Nsurv_over_N0', 'Nsurv_over_N0_meaning', 'carbon_cover_frac')


def _rrm_summary(cnc_summary, plan, info, ledger):
    """RIMP-06 — RRM 계획의 표준 `iface_contact_ledger` = 원장 기하 키 (CNC 요약 그대로) + **실제 RRM 행**에서 다시 센 행 · 막 몫."""
    s = {k_: cnc_summary[k_] for k_ in _GEOM_SUMMARY_KEYS if k_ in cnc_summary}
    rf = np.concatenate([np.asarray(a_['rface'], np.float64)[~np.asarray(a_['cut'], bool)] for a_ in plan['axes']])
    ref = [x for x in info if x['status'] == 'reference']
    C = ledger.get('contacts')
    a_lt = 0
    if C is not None:
        a_lt = int(sum(1 for x in ref if bool(C['a_lt_h'][int(x['cid'])])))
    fp = (cnc_summary.get('film_faces') or {})
    G = float(S3.iface_plan_film_G_S(plan).sum()) if len(plan['realized']) else 0.0
    s.update({
        'summary_source': 'rrm_rows — 실제 RRM 행 · 면 가중에서 다시 셈 (CNC 비교값 = iface_cnc_comparison · RIMP-06)',
        'n_realized': len(ref),
        'a_lt_h': {'n': a_lt, 'film_current_share': None,
                   'meaning': 'a < h — RRM 기준 접점 중 (해상 조건 a ≥ k·h 를 통과한 것) · 풀이 뒤 막 전류 몫'},
        'A_film_sum_um2': float(sum(float(x['sum_w_um2']) for x in ref)),
        'film_faces': {'pre': fp.get('pre'), 'surv': fp.get('surv'), 'active': int((rf > 0.0).sum()), 'zero_r': int((rf == 0.0).sum())},
        'cut_faces': int(sum(int(np.asarray(a_['cut'], bool).sum()) for a_ in plan['axes'])),
        'rface_ohm_cm2': {'rrm': S3._iface_quant(rf[rf > 0.0])},
        'film_G_S_total': {'rrm': G},
    })
    return s


# ═════════════════════════ N9 원장 검사 ═════════════════════════
_N9_WHY = {
    'film_off_outside': '원판 밖 owner 쌍 면이 행 없음 = 막 OFF (조화평균) — bulk 우회 (N9 · v3 §2-1 "막 OFF 로 두기 금지")',
    'film_off_inside': '원판과 겹친 owner 쌍 면이 행 없음 = 막 OFF (조화평균) — 막 없이 우회',
    'outside_not_cut': '원판 밖 면이 절단 tombstone 이 아니다 (막 행) — RRM 은 원판 밖을 절단한다 (D17 권고 기본값)',
    'inside_cut': '원판과 겹친 면이 절단됐다 — RRM 막 면이어야 한다',
    'rface_mismatch': '막 면 r_face ≠ r·h²/w (면 가중 재계산과 다르다)',
    'cid_mismatch': '행의 접점 번호가 그 면의 접점과 다르다',
    'row_not_owner_face': '기준 접점의 행인데 그 접점의 S_c^surv 면이 아니다',
    'duplicate_row': '같은 면에 행 둘',
    'recipe_missing': '계획 기록에 RRM recipe (iface_rrm · r 표 · 예외 법칙) 가 없다 — 검사 집합을 정할 수 없다 (RIMP-04)',
    'recipe_invalid': 'RRM recipe 값이 틀렸다 (resolve_k 비유한 · ≤ 0 · r 표 파싱 실패 · 모르는 예외 법칙) (RIMP-04)',
    'rface_nonfinite': '행 rface 가 유한하지 않다 (NaN 비교는 어떤 허용폭도 실패시키지 않는다 · 솔버는 NaN 면을 bulk 로 둔다 · RIMP-04)',
    'rface_negative': '행 rface < 0',
    'cut_not_tombstone': '절단 행이 tombstone 이 아니다 (rface ≠ 0 또는 ck ≠ 0)',
    'film_rface_zero': '막 행 rface 0 인데 그 접점의 등록 r 가 0 이 아니다 (등록된 r = 0 경로만 허용)',
    'row_cid_invalid': '막 행의 접점 번호가 원장 접점 범위 밖',
    'excluded_without_rejection': '기준에서 빠진 접점 (r 없음 · 기울기 · 미해상) 이 계획 거부 사유로 덮이지 않았다 — 메타데이터로 검사 집합을 비웠다 (RIMP-04)',
    'row_for_excluded_contact': '기준에서 빠진 접점의 막 행이 있다',
    'plan_not_reproducible': '기록된 recipe 로 rrm_plan 을 다시 만들면 행 · 거부 사유가 다르다 (복합 변이 · RIMP-04)',
}


def _recipe(rec):
    """계획 기록 → (resolve_k, r 표 (정규화), 예외 법칙 dict) 또는 (None, 사유) — RIMP-04 ① (기록 모양 · 값)."""
    rr = rec.get('iface_rrm')
    if not isinstance(rr, dict) or 'resolve_k' not in rr or 'iface_r_type_ohm_cm2' not in rec or 'iface_exception_law' not in rec:
        return None, 'recipe_missing'
    try:
        k = float(rr['resolve_k'])
    except (TypeError, ValueError):
        return None, 'recipe_invalid'
    if isinstance(rr['resolve_k'], (bool, np.bool_)) or not (math.isfinite(k) and k > 0.0):
        return None, 'recipe_invalid'
    try:
        rt = S3.parse_iface_r_type(rec['iface_r_type_ohm_cm2'])
    except (TypeError, ValueError):
        return None, 'recipe_invalid'
    law = rec['iface_exception_law']
    if not isinstance(law, dict) or set(law) != {'gap', 'unregistered', 'ambiguous_arm'}:
        return None, 'recipe_invalid'
    if (law['gap'] not in (None,) + S3.IFACE_EXCEPTION_LAWS or law['unregistered'] not in (None,) + S3.IFACE_EXCEPTION_LAWS
            or law['ambiguous_arm'] not in (None,) + S3.IFACE_AMBIGUOUS_ARMS):
        return None, 'recipe_invalid'
    return (k, rt, dict(law)), None


def rrm_check(plan, ledger):
    """N9 `reject_film_off_outside` — RRM 원장 검사 (v3 §2-3): 기준 접점마다 owner 쌍 면 (S_c^surv) = 막 행 (w > 0 · r_face = r·h²/w)
    또는 절단 tombstone (w = 0) · **그 밖은 없다**.  면 가중은 원장에서 다시 계산한다 (계획의 기록을 믿지 않는다).
    ★ RIMP-04 — 기록 (recipe) 검사 · 행 값 (유한 · ≥ 0 · tombstone · r = 0 경로) · 기대 접점 · 적격성 재계산 (빠진 접점은 거부 사유로 덮여야
      한다 · 메타데이터로 검사 집합을 비울 수 없다) · recipe 로 다시 만든 계획과 행 · 거부 사유 비트 같음 (재현 결합).
    → 위반 목록 [{code, n, detail, why}] (빈 목록 = 통과).  계획 행 지문 (E5) · 원장 격자 지문도 본다."""
    V = []

    def add(code, item):
        for x in V:
            if x['code'] == code:
                x['n'] += 1
                if len(x['detail']) < 8:
                    x['detail'].append(item)
                return
        V.append({'code': code, 'n': 1, 'detail': [item], 'why': _N9_WHY.get(code, code)})

    rec = plan.get('record') or {}
    if rec.get('iface_reference') != RRM_REFERENCE:
        return [{'code': 'not_rrm_plan', 'n': 1, 'detail': [], 'why': 'RRM 계획이 아니다 (iface_reference 없음)'}]
    if S3._iface_rows_fp(plan['axes']) != plan.get('fp_rows'):
        V.append({'code': 'fp_rows', 'n': 1, 'detail': [], 'why': '계획 행이 만든 뒤 바뀌었다 (지문 불일치 · E5)'})
    if plan.get('fp_sid') != ledger.get('fp_sid'):
        V.append({'code': 'ledger_mismatch', 'n': 1, 'detail': [], 'why': '계획이 다른 원장 (격자) 에서 만들어졌다'})
    got, why = _recipe(rec)
    if got is None:                                        # ① recipe 없이는 검사 집합을 정할 수 없다 → 위반 (통과 아님)
        V.append({'code': why, 'n': 1, 'detail': [], 'why': _N9_WHY[why]})
        return V
    k, rt, law = got
    arm = law['ambiguous_arm']
    h = float(ledger['vox'])
    C = ledger.get('contacts')
    nC = 0 if C is None else len(C['cls'])
    #  ② 행 값 (모든 행)
    rows = {}
    for ax, A in enumerate(plan['axes']):
        rf_ = np.asarray(A['rface'], np.float64); cut_ = np.asarray(A['cut'], bool)
        ck_ = np.asarray(A['ck'], np.int64); cid_ = np.asarray(A['cid'], np.int64)
        for e in range(len(A['lin'])):
            key = (ax, int(A['lin'][e]))
            if key in rows:
                add('duplicate_row', key)
            rows[key] = (bool(cut_[e]), float(rf_[e]), int(cid_[e]))
            if not math.isfinite(float(rf_[e])):
                add('rface_nonfinite', key)
            elif rf_[e] < 0.0:
                add('rface_negative', key)
            if cut_[e]:
                if not (rf_[e] == 0.0 and ck_[e] == 0):
                    add('cut_not_tombstone', key)
            else:
                if not (0 <= cid_[e] < nC):
                    add('row_cid_invalid', key)
                elif rf_[e] == 0.0 and rt.get(str(C['type_key'][cid_[e]])) != 0.0:
                    add('film_rface_zero', key)
    if ledger.get('owner') is not None:
        #  ③ 기대 접점 — 막 후보 = 부류 (팔) · N_c^surv > 0 · 면적 > 0 (r 표 없이) · 빠진 것은 계획 거부 사유로 덮여야 한다
        cls = C['cls']
        film = (cls == 0) | ((cls == 1) & (arm == 'a_hi'))
        A_f = np.where(cls == 0, C['A_true'], np.where(cls == 1, C['A_hi'], 0.0))
        cand = film & (C['nsurv'] > 0) & (A_f > 0.0)
        need = {'r_type_missing': 0, 'rrm_unsupported_tilt': 0, 'rrm_unresolved_subgrid': 0}
        excluded = set()
        for q in np.flatnonzero(cand).tolist():
            tkey = str(C['type_key'][q])
            if tkey not in rt:
                need['r_type_missing'] += 1; excluded.add(q)
                continue
            W = rrm_face_weights(ledger, q)
            if not W['eligible']:
                need['rrm_unsupported_tilt'] += 1; excluded.add(q)
                continue
            if not (W['disc']['a'] >= k * h):
                need['rrm_unresolved_subgrid'] += 1; excluded.add(q)
                continue
            r_q = float(rt[tkey])
            mine = set()
            for e in range(len(W['lin'])):
                key = (int(W['axis'][e]), int(W['lin'][e])); w = float(W['w'][e])
                mine.add(key)
                if key not in rows:
                    add('film_off_outside' if w == 0.0 else 'film_off_inside', key)
                    continue
                cut, rface, cid = rows[key]
                if cid != q:
                    add('cid_mismatch', key)
                if w == 0.0 and not cut:
                    add('outside_not_cut', key)
                elif w > 0.0 and cut:
                    add('inside_cut', key)
                elif w > 0.0:
                    want = float(S3.iface_rface_ohm_cm2(r_q, 1, h, w))
                    if not (math.isfinite(rface) and abs(rface - want) <= 1e-12 * max(abs(want), 1e-300)):
                        add('rface_mismatch', key)
            for key, (cut, rface, cid) in rows.items():
                if cid == q and key not in mine:
                    add('row_not_owner_face', key)
        have = {}
        for x in plan.get('rejections') or ():
            have[x.get('code')] = have.get(x.get('code'), 0) + int(x.get('n') or 0)
        for code_, n_ in need.items():
            if n_ and have.get(code_, 0) < n_:
                add('excluded_without_rejection', (code_, n_, have.get(code_, 0)))
        for key, (cut, rface, cid) in rows.items():
            if not cut and cid in excluded:
                add('row_for_excluded_contact', key)
    #  ④ 재현 결합 — 기록된 recipe 로 다시 만든 계획과 행 · 거부 사유 · 행 수가 비트 같아야 한다
    try:
        E = rrm_plan(ledger, rt, resolve_k=k, gap_law=law['gap'], unreg_law=law['unregistered'], ambiguous_arm=arm)
    except (TypeError, ValueError) as ex:
        add('plan_not_reproducible', f'rrm_plan 재생성 실패 — {type(ex).__name__}: {ex}')
        return V
    if sorted((x['code'], int(x.get('n') or 0)) for x in plan.get('rejections') or ()) != \
            sorted((x['code'], int(x.get('n') or 0)) for x in E['rejections']):
        add('plan_not_reproducible', 'rejections')
    for ax in range(3):
        for kk in ('lin', 'rface', 'cut', 'ck', 'cid', 'olo'):
            a_, b_ = np.asarray(plan['axes'][ax][kk]), np.asarray(E['axes'][ax][kk])
            if not (a_.dtype == b_.dtype and a_.shape == b_.shape and a_.tobytes() == b_.tobytes()):
                add('plan_not_reproducible', f'axes[{ax}].{kk}')
    for kk in ('n_film_rows', 'n_cut_rows'):
        if plan.get(kk) != E[kk]:
            add('plan_not_reproducible', kk)
    return V


def rrm_require(plan, ledger):
    """N9 관문 — 위반이 있으면 ValueError (RRM 시험 harness 가 솔브 **앞**에서 부른다)."""
    V = rrm_check(plan, ledger)
    if V:
        raise ValueError('RRM 원장 검사 (N9) 거부 — ' + ' · '.join(f"{x['code']}(n={x['n']})" for x in V))
    return plan


def rrm_solve(sid, sigma_of_sid, vox, plan, ledger, **solve_kw):
    """RRM 계획으로 생산 솔버를 부른다 — 원장 검사 (N9) 를 **먼저**.  솔버 자신은 RRM 을 모른다 (생산 경로 그대로)."""
    rrm_require(plan, ledger)
    return S3.solve_sigma_z(sid, sigma_of_sid, vox, iface=plan, **solve_kw)
