#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""망 세대 계약 — 모드마다 허용 모델 조합 · 닫힌 열거 · 부분 결손 거부 · 옛 세대 추론 자격 (Codex 세대 2 적대 리뷰 G2R-01 · G2R-02 · 1저자 비준 10-06 밤).

  python3 scripts/test_gen2_role_contract.py

★ 시험 먼저 — 옛 코드 (7a5976602 이후 HEAD) 에서 빨갛다 (Codex `probes/publication.py` · `handover.py` · `adversarial.py` 세대 부분의 변이를
  **실 생산자 출력** 위에 그대로 옮겼다 · 우리 트리 재현 `docs/reviews/codex_gen2_network_review_evidence_20261006/_reproduction_ours_7a5976602/`):
  R  역할 — H12 레코드를 주 Hertz 자리에 (h12_as_primary) · ψ 오타 (multiply_TYPO) · 세 모드 전극 오타 (DIRICHLET_TYPO) · 세대 2 physics 에서
     area_rule · psi_placement 만 삭제 (partial_missing_g2) · 세대 2 Hertz 에 H12 없음 · 채널 표기 오타 · 명시 ψ 분모 연구 팔 (세대 2 생산자 +
     legacy_divide = 세대 1 도 2 도 아님) → 세대 계약 위반 · 레코드 있는 모드 전부 NOT_COMPUTED (invalid_input) · 옛 기본값으로 채우지 않는다
     (옛: 넷 다 OK · 세대 표기는 옛 기본값 · 주 σ +28.2 %)
  M  코호트 — 행마다 유효성 먼저 (`row_generation_problems`) — 같은 결함만 모인 코호트도 거부 · 정상 + 결함 한 행도 거부 (옛: 같은 결함 둘 = 통과)
  P  양성 대조 — 실 생산자 세 모드 = 세대 2 · 진짜 역사 레코드 (194 v1.2 배치 원천 `net194_tau_sources_20261006.tar.gz`) = inferred_legacy ·
     v1.2 인계표 τ 칸 그대로 재현 · 생산자 실패 레코드 모양 (H12 풀이 예외) 은 세대 위반이 아니라 그 모드 solver_guard
  K  세대 2 표지 키 — 실 생산자 레코드에 있고 · 역사 레코드 194 에는 하나도 없다 (옛 세대 추론 자격의 근거)
⚠ 범위 — 표기 (메타) 계약이다.  숫자만 바꿔 끼운 레코드 (표기는 그대로) 는 재계산 없이 못 잡는다 (TAU_SAME_GEN_BASIS 한계와 같은 부류).
"""
import contextlib
import copy
import io
import json
import math
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
_ok, _fail = 0, []
ARCHIVE = os.path.join(ROOT, 'docs', 'data', 'lhs_network194_11fcf91e8', 'handover_v12_20261006', 'net194_tau_sources_20261006.tar.gz')
HANDOVER_V12 = os.path.join(ROOT, 'docs', 'data', 'lhs_network194_11fcf91e8', 'handover_v12_20261006')

#  세대 2 표지 키 — 독립 오라클 (실 생산자 출력 ↔ 194 역사 레코드의 키 차 · 10-06 밤 실측 · 시험이 도우미 상수를 베끼지 않는다)
G2_ONLY = ('electrode_model', 'bulk_model', 'area_rule', 'area_rule_physics', 'hertz_constriction', 'sensitivity_mode', 'hertz_h12',
           'area_binding_counts_physics', 'n_area_physics_unavailable', 'n_clamp_zero', 'n_floor_only', 'h_film_nm', 'h_film_status',
           'solve_method_full')
G2_CHANNEL = ('electrode_model', 'bulk_model', 'area_rule', 'area_rule_physics', 'area_binding_counts_physics', 'n_clamp_zero', 'n_floor_only',
              'psi_placement')


def chk(name, cond, extra=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'   {str(extra)[:400]}' if extra else ''))


def _guard(label, fn):
    try:
        fn()
    except Exception as e:                                       # noqa: BLE001 — 옛 코드 (도우미 없음) 도 실패로 센다
        chk(f'{label} — 예외 {type(e).__name__}: {e}', False)


def quiet(fn, *a, **kw):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **kw)


def _rc(reason):
    return str(reason or '').split(':', 1)[0].strip()


#  Codex probes/publication.py 의 `change` 그대로 (dual 에 적용 — 레코드 객체마다 · 중첩 H12 포함)
def change(du, label):
    for k, r in du.items():
        if not isinstance(r, dict):
            continue
        if label == 'h12_as_primary' and k == 'hertzian':
            r.update(copy.deepcopy(r['hertz_h12']))
        elif label == 'bad_psi' and k == 'physics':
            r['psi_placement'] = 'multiply_TYPO'
        elif label == 'bad_electrode':
            r['electrode_model'] = 'DIRICHLET_TYPO'
            if 'hertz_h12' in r:
                r['hertz_h12']['electrode_model'] = 'DIRICHLET_TYPO'
        elif label == 'partial_missing_g2' and k == 'physics':
            for key in ('area_rule', 'psi_placement'):
                r.pop(key, None)


def strip_g2(du):
    """세대 2 표지를 **전부** 뺀 레코드 (값은 그대로 · 표기만) — 역사 레코드 모양 (resistance_model · contact_mode · ψ legacy_divide 만)."""
    d2 = copy.deepcopy(du)
    for m in ('hertzian', 'physics'):
        r = d2.get(m)
        if not isinstance(r, dict):
            continue
        for k in list(r):
            if k in G2_ONLY or any(k == f'{ch}_{g}' for ch in ('electronic', 'thermal') for g in G2_CHANNEL):
                r.pop(k, None)
        r['psi_placement'] = 'legacy_divide'
    return d2


def main():
    import network_conductivity as nc
    import tau_flux as tf
    contract = getattr(tf, 'network_generation_contract', None)
    row_probs = getattr(tf, 'row_generation_problems', None)
    GEN_COL = getattr(tf, 'ROW_GENERATION_COL', 'ion_net_generation')

    def con_of(du):
        return contract(du) if contract else {'generation': None, 'problems': [('?', 'NO_HELPER', '도우미 없음 (옛 코드)')]}

    def rprobs(row):
        return row_probs(row)[1] if row_probs else ['NO_HELPER']

    #  실 생산자 — SE 사슬 (21 구 · 관통) + 떨어진 AM 사슬 (전자 채널 표기도 실린다)
    A = {i: {'type': 1, 'x': 0.0, 'y': 0.0, 'z': float(z), 'radius': 1.0} for i, z in enumerate(range(21), 1)}
    A.update({100 + k: {'type': 2, 'x': 5.0, 'y': 0.0, 'z': float(z), 'radius': 1.0} for k, z in enumerate(range(21))})
    C = [{'id1': i, 'id2': i + 1, 'contact_area': 0.1, 'delta': 0.05} for i in range(1, 21)]
    C += [{'id1': 100 + k, 'id2': 101 + k, 'contact_area': 0.1, 'delta': 0.05} for k in range(20)]
    TM = {1: 'SE', 2: 'AM_P'}

    def produce(**kw):
        return json.loads(json.dumps({cm: quiet(nc._run_all_networks, A, C, [1], [2], TM, 1.0, 20.0, 10.0, 10.0, None, contact_mode=cm, **kw)
                                      for cm in ('hertzian', 'physics')}))
    base = produce()
    phi = 21 * 4.0 / 3.0 * math.pi / (10.0 * 10.0 * 20.0)
    led = {'thickness_um': 20.0, 'thickness_mass_conserving_um': 20.0, 'phi_se_mass_conserving': phi}

    def cols(du, pct=100.0):
        return tf.ion_columns(du, led, pct)

    def variant(label):
        du = copy.deepcopy(base)
        change(du, label)
        return du

    # ══ K. 세대 2 표지 키 — 실 생산자 ↔ 역사 레코드 ═════════════════════════════════════════════════════════════════════════════
    hist = {}

    def sK():
        tmp = tempfile.mkdtemp(prefix='g2rc_hist_')
        try:
            with tarfile.open(ARCHIVE) as t:
                for mem in t.getmembers():
                    if mem.isfile() and mem.name.endswith(('network_conductivity_dual.json', 'full_metrics.json', 'network_provenance.json')):
                        parts = mem.name.split('/')
                        case = parts[1]
                        d = os.path.join(tmp, case)
                        os.makedirs(d, exist_ok=True)
                        with t.extractfile(mem) as fh, open(os.path.join(d, parts[-1]), 'wb') as out:
                            out.write(fh.read())
            for case in sorted(os.listdir(tmp)):
                hist[case] = os.path.join(tmp, case)
            hk = set()
            for d in hist.values():
                du = json.load(open(os.path.join(d, 'network_conductivity_dual.json'), encoding='utf-8'))
                for m in ('hertzian', 'physics'):
                    hk |= set(du[m])
            prod = set(base['hertzian']) | set(base['physics']) | set(base['hertzian']['hertz_h12'])
            want = set(G2_ONLY) | {f'{ch}_{g}' for ch in ('electronic', 'thermal') for g in G2_CHANNEL}
            chk(f'K1 표지 키 오라클 — 실 생산자 세 레코드에 다 있다 · 역사 레코드 194 ({len(hist)} 폴더) 에는 하나도 없다',
                len(hist) == 194 and want <= prod and not (want & hk), (sorted(want - prod), sorted(want & hk)))
            mk = set(getattr(tf, 'G2_MARKER_KEYS', ()))
            chk('K2 ★ 도우미 표지 키 (tau_flux.G2_MARKER_KEYS) = 오라클 (실 생산자 ↔ 역사 차) — 하나라도 빠지면 그 키만 남긴 부분 결손을 옛 세대로 추론한다',
                mk == want, (sorted(want - mk), sorted(mk - want)))
            #  역사 레코드 = 이력 사실 (resistance_model · contact_mode · ψ legacy_divide) — 도우미 옛 세대 표가 이 모양을 받는다
            du0 = json.load(open(os.path.join(hist['lhs00_000'], 'network_conductivity_dual.json'), encoding='utf-8'))
            chk('K3 역사 레코드 모양 — hertz (maxwell · hertzian · legacy_divide) · physics (mikic · physics · legacy_divide) · H12 없음',
                (du0['hertzian'].get('resistance_model'), du0['hertzian'].get('contact_mode'), du0['hertzian'].get('psi_placement')) ==
                ('maxwell', 'hertzian', 'legacy_divide')
                and (du0['physics'].get('resistance_model'), du0['physics'].get('contact_mode'), du0['physics'].get('psi_placement')) ==
                ('mikic', 'physics', 'legacy_divide') and 'hertz_h12' not in du0['hertzian'])
        except Exception:
            shutil.rmtree(tmp, ignore_errors=True)
            raise
        hist['_tmp'] = tmp
    _guard('K', sK)

    # ══ T. 계약 표 = 생산자 상수 · 실 출력 ═══════════════════════════════════════════════════════════════════════════════════════════
    def sT():
        tab = getattr(tf, 'G2_MODE_CONTRACT', {})
        want = {'hertz': {'contact_mode': 'hertzian', 'resistance_model': 'maxwell', 'hertz_constriction': nc.HERTZ_CONSTRICTION_MAXWELL,
                          'bulk_model': nc.BULK_CYLINDER, 'electrode_model': nc.ELECTRODE_DIRICHLET, 'area_rule': nc.AREA_RULE_HERTZ,
                          'area_rule_physics': nc.AREA_RULE_G2, 'psi_placement': nc.PSI_MULTIPLY, 'sensitivity_mode': None},
                'hertz_h12': {'contact_mode': 'hertzian', 'resistance_model': 'mikic', 'hertz_constriction': nc.HERTZ_CONSTRICTION_PSI,
                              'bulk_model': nc.BULK_SPHERE_SEGMENT, 'electrode_model': nc.ELECTRODE_DIRICHLET, 'area_rule': nc.AREA_RULE_HERTZ,
                              'area_rule_physics': nc.AREA_RULE_G2, 'psi_placement': nc.PSI_MULTIPLY, 'sensitivity_mode': nc.HERTZ_H12_MODE},
                'physics': {'contact_mode': 'physics', 'resistance_model': 'mikic', 'hertz_constriction': None,
                            'bulk_model': nc.BULK_CYLINDER, 'electrode_model': nc.ELECTRODE_DIRICHLET, 'area_rule': nc.AREA_RULE_G2,
                            'area_rule_physics': nc.AREA_RULE_G2, 'psi_placement': nc.PSI_MULTIPLY, 'sensitivity_mode': None}}
        got = {m: dict(tab.get(m, ())) for m in want}
        chk('T1 ★ 세대 2 계약 표 (tau_flux.G2_MODE_CONTRACT) = 생산자 상수 — H0 = Maxwell + 원기둥 + dirichlet · H12 = ψ 곱 + 구 조각 + dirichlet · '
            'physics = ψ 곱 + physics_g2 + 원기둥 + dirichlet', got == want, got)
        recs = {'hertz': base['hertzian'], 'hertz_h12': base['hertzian']['hertz_h12'], 'physics': base['physics']}
        bad = {m: {k: recs[m].get(k) for k, v in want[m].items() if recs[m].get(k) != v} for m in want}
        chk('T2 실 생산자 세 레코드의 표기 = 계약 표 (키 없음 = None)', not any(bad.values()), bad)
    _guard('T', sT)

    # ══ P. 양성 대조 ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def sP():
        c0 = con_of(base)
        o0 = cols(base)
        chk("P1 ★ 실 생산자 세 모드 → 세대 g2 · 문제 없음 · 행 세대 칸 'g2' · 세 모드 OK · 행 계약 문제 없음",
            c0.get('generation') == 'g2' and not c0.get('problems') and o0.get(GEN_COL) == 'g2'
            and all(o0.get(f'ion_net_status_{m}') == 'OK' for m in ('hertz', 'physics', 'hertz_h12')) and not rprobs(o0),
            (c0, o0.get(GEN_COL), rprobs(o0)))
        if '_tmp' not in hist:
            chk('P2 역사 레코드 (압축 풀기 실패)', False)
            return
        import csv
        tab = {}
        for coh in ('lhs', 'lhsx'):
            with open(os.path.join(HANDOVER_V12, f'{coh}_handover_v12_20261006.csv'), encoding='utf-8', newline='') as fh:
                for r in csv.DictReader(fh):
                    tab[r['case_id']] = r
        rows, gens, bad, nprob = [], set(), [], 0
        for case, d in sorted(hist.items()):
            if case == '_tmp':
                continue
            du = json.load(open(os.path.join(d, 'network_conductivity_dual.json'), encoding='utf-8'))
            c = con_of(du)
            row = tf.case_row(d)
            rows.append(row)
            gens.add((c.get('generation'), row.get(GEN_COL)))
            nprob += bool(c.get('problems')) + bool(rprobs(row))
            want = tab.get(case) or {}
            diff = [k for k in want if k in row and tf._cell(row[k]) != want[k]]
            if diff:
                bad.append((case, diff[:3]))
        chk(f"P2 ★ 진짜 역사 레코드 194 (v1.2 배치 원천) → 세대 inferred_legacy (계약 · 행 칸) · 문제 0 · v1.2 인계표 τ 칸 그대로 재현 "
            f"(공통 칸 차이 0) {gens} · 문제 {nprob} · 어긋남 {bad[:3]}",
            gens == {('inferred_legacy', 'inferred_legacy')} and nprob == 0 and not bad and len(rows) == 194)
        o_l = rows[0] if rows else {}
        chk('P3 역사 레코드의 세대 표기 = 이력 사실로 **추론** (virtual_source_legacy · physics_g1 · cylinder_half_d · mikic_psi_divide) — 세대 칸이 추론임을 말한다',
            o_l.get('ion_net_electrode_hertz') == o_l.get('ion_net_electrode_physics') == 'virtual_source_legacy'
            and o_l.get('ion_net_area_rule_physics') == 'physics_g1' and o_l.get('ion_net_bulk_hertz') == 'cylinder_half_d'
            and o_l.get('ion_net_constriction_physics') == 'mikic_psi_divide' and o_l.get(GEN_COL) == 'inferred_legacy',
            {k: o_l.get(k) for k in (GEN_COL, 'ion_net_electrode_hertz', 'ion_net_area_rule_physics', 'ion_net_constriction_physics')})
        mixf = getattr(tf, 'generation_mixing_problem')
        chk('P4 역사 코호트 194 (lhs · lhsx) 를 한 판정에 — 세대 섞임 없음 · 행 계약 문제 없음', mixf(rows) == '', mixf(rows)[:300])
        #  생산자 실패 레코드 모양 (H12 풀이 예외 — `_hertz_h12_record` 의 except 가지) 은 세대 위반이 아니라 그 모드의 기술적 실패
        orig = nc.run_decomposition

        def _boom(*a, **k):
            if k.get('bulk_model') == nc.BULK_SPHERE_SEGMENT:
                raise RuntimeError('주입: H12 풀이 예외')
            return orig(*a, **k)
        nc.run_decomposition = _boom
        try:
            df = json.loads(json.dumps({cm: quiet(nc._run_all_networks, A, C, [1], [2], TM, 1.0, 20.0, 10.0, 10.0, None, contact_mode=cm)
                                        for cm in ('hertzian', 'physics')}))
        finally:
            nc.run_decomposition = orig
        of, cf = cols(df), con_of(df)
        #  사유 = 그 모드의 기술적 실패 그대로 (예외 가지 레코드는 관통 분율 · 띠 규칙도 없어 첫 관문 missing_input — 옛 판과 같다) · 세대 계약 사유 아님
        chk("P5 생산자 실패 레코드 (H12 풀이 예외 · 표기 일부만) → 세대 계약 위반 아님 · H12 = NOT_COMPUTED (그 모드의 기술적 실패 — invalid_input 아님) · "
            "주 두 모드 OK",
            df['hertzian']['hertz_h12'].get('sigma_full_status') == 'not_computed' and not cf.get('problems') and cf.get('generation') == 'g2'
            and of.get('ion_net_status_hertz_h12') == 'NOT_COMPUTED'
            and of.get('ion_net_status_reason_hertz_h12') in ('solver_guard', 'missing_input')
            and of.get('ion_net_status_hertz') == of.get('ion_net_status_physics') == 'OK', (cf.get('problems'), of.get('ion_net_status_reason_hertz_h12')))
    _guard('P', sP)

    # ══ R. 역할 · 닫힌 열거 · 부분 결손 (Codex 변이 + 더) ═══════════════════════════════════════════════════════════════════════
    def sR():
        o0 = cols(base)
        res = {}
        for lab in ('h12_as_primary', 'bad_psi', 'bad_electrode', 'partial_missing_g2'):
            du = variant(lab)
            c, o = con_of(du), cols(du)
            res[lab] = (c.get('generation'), bool(c.get('problems')),
                        tuple((o.get(f'ion_net_status_{m}'), _rc(o.get(f'ion_net_status_reason_{m}'))) for m in ('hertz', 'physics', 'hertz_h12')),
                        o.get(GEN_COL), bool(rprobs(o)), o.get('tau2_ion_hertz'))
        want = ('invalid', True, (('NOT_COMPUTED', 'invalid_input'),) * 3, 'invalid', True, None)
        chk(f'R1 ★ Codex 변이 넷 (h12_as_primary · bad_psi · bad_electrode · partial_missing_g2) → 세대 invalid · 세 모드 NOT_COMPUTED (invalid_input) · '
            f'값 빈칸 · 행 계약 위반 (옛: 넷 다 OK · 주 tau2 그대로 실림) { {k: v for k, v in res.items() if v != want} or ""}',
            all(v == want for v in res.values()) and len(res) == 4)
        oh = cols(variant('h12_as_primary'))
        chk('R2 ★ h12_as_primary — 주 Hertz 행 표기가 H12 를 드러낸다 (협착 mikic_psi_multiply · bulk sphere_segment) · 사유에 hertz 역할 · 옛 σ +28.2 % 가 실리지 않는다',
            oh.get('ion_net_constriction_hertz') == 'mikic_psi_multiply' and oh.get('ion_net_bulk_hertz') == 'sphere_segment'
            and 'hertz' in str(oh.get('ion_net_status_reason_hertz')) and oh.get('f_ion_hertz') is None
            and o0.get('f_ion_hertz') is not None, {k: oh.get(k) for k in ('ion_net_constriction_hertz', 'ion_net_bulk_hertz', 'ion_net_status_reason_hertz')})
        op = cols(variant('partial_missing_g2'))
        chk('R3 ★ partial_missing_g2 — 세대 2 표지가 남은 레코드의 빈 ψ · 면적을 옛 기본값 (mikic_psi_divide · physics_g1) 으로 채우지 않는다',
            op.get('ion_net_constriction_physics') != 'mikic_psi_divide' and op.get('ion_net_area_rule_physics') != 'physics_g1'
            and op.get('ion_net_psi_physics') in ('', None),
            {k: op.get(k) for k in ('ion_net_constriction_physics', 'ion_net_area_rule_physics', 'ion_net_psi_physics')})
        ob = cols(variant('bad_psi'))
        chk("R4 bad_psi — 모르는 ψ 는 'unknown:mikic/…' 로 보이고 (빈 축으로 사라지지 않는다) 세대 invalid",
            str(ob.get('ion_net_constriction_physics')).startswith('unknown:mikic/') and ob.get(GEN_COL) == 'invalid')
        #  더 — 세대 2 Hertz 에 H12 없음 · 채널 표기 오타 · 명시 ψ 분모 연구 팔 · H12 에 주 Hertz 메타 · physics 자리에 Hertz 레코드
        more = {}
        d1 = copy.deepcopy(base)
        d1['hertzian'].pop('hertz_h12')
        more['H12 없음 (세대 2 Hertz)'] = d1
        d2 = copy.deepcopy(base)
        d2['physics']['thermal_electrode_model'] = 'DIRICHLET_TYPO'
        more['열 채널 전극 오타'] = d2
        d3 = copy.deepcopy(base)
        d3['hertzian']['electronic_bulk_model'] = 'sphere_segment'
        more['전자 채널 bulk = 구 조각 (H0 자리)'] = d3
        more['명시 ψ 분모 (세대 2 생산자 + legacy_divide)'] = produce(psi_placement=nc.PSI_DIVIDE)
        d5 = copy.deepcopy(base)
        d5['hertzian']['hertz_h12'].update({k: base['hertzian'][k] for k in ('hertz_constriction', 'bulk_model', 'resistance_model')})
        more['H12 자리에 H0 메타'] = d5
        d6 = copy.deepcopy(base)
        d6['physics'] = copy.deepcopy(base['hertzian'])
        d6['physics'].pop('hertz_h12')
        more['physics 자리에 Hertz 레코드'] = d6
        d7 = copy.deepcopy(base)
        d7['physics']['area_rule'] = 'physics_g9'
        more['모르는 면적 규칙'] = d7
        d8 = copy.deepcopy(base)
        d8['hertzian']['sensitivity_mode'] = 'hertz_h12'
        more['주 Hertz 에 민감도 표지'] = d8
        got = {}
        for lab, du in more.items():
            c, o = con_of(du), cols(du)
            got[lab] = (c.get('generation'), o.get('ion_net_status_hertz'), o.get('ion_net_status_physics'))
        chk(f'R5 ★ 더 — H12 없음 · 채널 표기 오타 · 명시 ψ 분모 연구 팔 · H12 자리에 H0 메타 · physics 자리에 Hertz · 모르는 면적 · 주 Hertz 민감도 표지 → '
            f'세대 invalid · 주 두 모드 NOT_COMPUTED { {k: v for k, v in got.items() if v != ("invalid", "NOT_COMPUTED", "NOT_COMPUTED")} or ""}',
            all(v == ('invalid', 'NOT_COMPUTED', 'NOT_COMPUTED') for v in got.values()) and len(got) == len(more))
        #  옛 세대 모양 — 표지를 전부 뺀 레코드 = inferred_legacy (값 · 상태 그대로 · 표기 = 추론) · 표지 하나라도 남으면 invalid (부분 결손)
        dl = strip_g2(base)
        cl, ol = con_of(dl), cols(dl)
        chk('R6 표지를 전부 뺀 레코드 (역사 모양) → inferred_legacy · 주 두 모드 OK · H12 = NOT_COMPUTED (missing_input · 그 세대에 없는 열)',
            cl.get('generation') == 'inferred_legacy' and not cl.get('problems') and ol.get(GEN_COL) == 'inferred_legacy'
            and ol.get('ion_net_status_hertz') == ol.get('ion_net_status_physics') == 'OK'
            and ol.get('ion_net_status_reason_hertz_h12') == 'missing_input', (cl, ol.get(GEN_COL)))
        part = {}
        for k in ('electrode_model', 'n_clamp_zero', 'h_film_nm', 'thermal_area_rule', 'solve_method_full'):
            dp = strip_g2(base)
            dp['physics'][k] = base['physics'][k]
            part[k] = con_of(dp).get('generation')
        dpm = strip_g2(base)
        dpm['hertzian']['psi_placement'] = 'multiply'
        part['ψ multiply (Hertz)'] = con_of(dpm).get('generation')
        chk(f'R7 ★ 표지 하나만 남은 레코드 (전극 · 진단 키 · 채널 표기 · ψ multiply) → invalid (옛 세대로 추론하지 않는다 · 부분 결손) {part}',
            all(v == 'invalid' for v in part.values()))
        dlg = strip_g2(base)
        dlg['hertzian']['resistance_model'] = 'mikic'
        dlg2 = strip_g2(base)
        dlg2['physics']['psi_placement'] = 'TYPO'
        chk('R8 옛 세대 모양인데 역할이 틀림 (Hertz 자리 mikic · 모르는 ψ) → invalid (옛 세대 표도 닫힌 열거)',
            con_of(dlg).get('generation') == con_of(dlg2).get('generation') == 'invalid')
    _guard('R', sR)

    # ══ M. 코호트 — 행마다 유효성 먼저 ══════════════════════════════════════════════════════════════════════════════════════
    def sM():
        mixf = tf.generation_mixing_problem
        ok = dict(cols(base), case='ok')
        ok2 = dict(cols(base), case='ok2')
        rows = {lab: dict(cols(variant(lab)), case=lab) for lab in ('h12_as_primary', 'bad_psi', 'bad_electrode', 'partial_missing_g2')}
        same = {lab: mixf([dict(r, case=lab + '_a'), dict(r, case=lab + '_b')]) for lab, r in rows.items()}
        chk(f'M1 ★ 같은 결함만 모인 코호트 (둘 다 같은 변이) → 거부 (옛: 동질이라 통과) { {k: bool(v) for k, v in same.items()} }',
            all(bool(v) for v in same.values()))
        mixed = {lab: mixf([ok, r]) for lab, r in (('h12_as_primary', rows['h12_as_primary']), ('bad_psi', rows['bad_psi']))}
        chk(f'M2 ★ 정상 + 결함 한 행 ([baseline, h12_as_primary] · [baseline, bad_psi]) → 거부 (옛: 둘 다 통과) { {k: bool(v) for k, v in mixed.items()} }',
            all(bool(v) for v in mixed.values()))
        legacy = dict(cols(strip_g2(base)), case='g1')
        chk('M3 양성 — 세대 2 끼리 · 옛 세대끼리 통과 · 세대 2 + 옛 세대 = 거부 · 레코드 없는 행 (모든 표기 빈칸) 은 판정 밖',
            mixf([ok, ok2]) == '' and mixf([legacy, dict(legacy, case='g1b')]) == '' and bool(mixf([ok, legacy]))
            and mixf([ok, {'case': 'empty'}]) == '')
        ax = tf.generation_axes(ok)
        chk("M4 세대 축 = 세대 · ψ · physics 면적 · 전극 + 모드별 협착 · bulk (Codex: 주 Hertz 의 bulk · 협착이 축 밖이었다)",
            ax.get('generation') == 'g2' and ax.get('constriction_hertz') == 'maxwell_halfspace' and ax.get('bulk_hertz') == 'cylinder_half_d'
            and ax.get('constriction_hertz_h12') == 'mikic_psi_multiply' and ax.get('bulk_hertz_h12') == 'sphere_segment'
            and ax.get('constriction_physics') == 'mikic_psi_multiply' and ax.get('bulk_physics') == 'cylinder_half_d', ax)
        #  직렬화 칸 (인계 원천 cells) 도 같은 판정 — 세대 칸을 지운 새 행 (스키마는 새 행) 은 거부
        cells = {k: tf._cell(v) for k, v in ok.items()}
        nogen = {k: v for k, v in cells.items() if k != GEN_COL}
        nogen['ion_net_bulk_hertz'] = 'sphere_segment'
        chk('M5 직렬화 칸 — 정상 통과 · 세대 칸 없는 행에서 주 Hertz bulk = 구 조각이면 거부 (세대 칸 없이도 표기가 역할을 증명해야)',
            not rprobs(cells) and bool(rprobs(nogen)), (rprobs(cells), rprobs(nogen)))
    _guard('M', sM)

    # ══ C. CLI — 같은 결함 폴더 둘은 표를 내지 않는다 ═════════════════════════════════════════════════════════════════════════
    def sC():
        tmp = tempfile.mkdtemp(prefix='g2rc_cli_')
        try:
            ds = []
            for name, du in (('a', variant('bad_psi')), ('b', variant('bad_psi'))):
                d = os.path.join(tmp, name)
                os.makedirs(d)
                json.dump(du, open(os.path.join(d, 'network_conductivity_dual.json'), 'w'))
                json.dump(dict(led, percolation_pct=100.0), open(os.path.join(d, 'full_metrics.json'), 'w'))
                ds.append(d)
            out = os.path.join(tmp, 'o.tsv')
            r = subprocess.run([sys.executable, os.path.join(HERE, 'tau_flux.py'), *ds, '--tsv', out], capture_output=True, text=True, timeout=180)
            d_ok = os.path.join(tmp, 'ok')
            os.makedirs(d_ok)
            json.dump(base, open(os.path.join(d_ok, 'network_conductivity_dual.json'), 'w'))
            json.dump(dict(led, percolation_pct=100.0), open(os.path.join(d_ok, 'full_metrics.json'), 'w'))
            r2 = subprocess.run([sys.executable, os.path.join(HERE, 'tau_flux.py'), d_ok, '--tsv', out + '2'], capture_output=True, text=True,
                                timeout=180)
            chk('C1 ★ tau_flux CLI — 같은 결함 (bad_psi) 폴더 둘 → rc 2 · 표 안 씀 · 사유에 세대 계약 (옛: rc 0) · 정상 폴더 하나 → rc 0',
                r.returncode == 2 and not os.path.exists(out) and '세대' in r.stderr and r2.returncode == 0 and os.path.exists(out + '2'),
                f'rc {r.returncode} · {r.stderr[-240:]!r} · 정상 rc {r2.returncode}')
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    _guard('C', sC)

    if hist.get('_tmp'):
        shutil.rmtree(hist['_tmp'], ignore_errors=True)
    print(f'\ntest_gen2_role_contract: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
