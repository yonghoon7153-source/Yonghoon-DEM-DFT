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
  Y  ★ G2RR-02 (Codex 세대 2 재검증 §3 · §7-2 · 10-06 밤) — 증서 ↔ 가지 · 채널 · 역할 · 전극 · ΔV · 기하 (G→q) · 발행값 결합: CF → FULL · H12 → H0 ·
     채널 바꿔치기 · 기하 인자 · 위장 CF (재구성은 맞춘 것) · 숫자만 · 실린 CF · 협착-only 진단 숫자의 증서 결손 · 보존 실패 · 결합 키 없는 증서 → invalid ·
     양성 = 정상 · GEN2-01 협착-only 미계산 · 진짜 비관통 · CF 모형 과전도 (표지는 증서 면제가 아니다)
⚠ 범위 — 표기 계약 + 증서 결합.  숫자만 바꾼 레코드는 이제 증서 재구성이 잡는다 (Y) · 증서 · 숫자 · 기하를 한 실행의 모든 증서에 걸쳐 일관되게
  바꾼 전면 위조는 재계산 없이 못 잡는다 (TAU_SAME_GEN_BASIS 한계와 같은 부류).
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
G2_ONLY = ('solve_certificate_full', 'solve_certificate_bulk_net', 'solve_certificate_constr_net', 'electrode_model', 'bulk_model', 'area_rule', 'area_rule_physics', 'hertz_constriction', 'sensitivity_mode', 'hertz_h12',
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
    #  ★ 10-06 밤 통합 (G2R-03 증서 → 계약) — 세대 2 레코드의 계산된 FULL σ 는 수치 증서 (solve_certificate_full) 가 있고 통과해야 한다.
    #    게시 관문 ⑨ · 인계 재독이 같은 계약을 부르므로 여기서 거부되면 둘 다 막힌다 (반례 먼저 — 옛 계약은 증서를 안 봤다).
    def _cert_case(fn):
        d2 = copy.deepcopy(base)
        fn(d2)
        return con_of(d2)

    def _probs_text(c):
        return ' | '.join(f'{m}:{k}:{s}' for m, k, s in c.get('problems', []))
    _okb = con_of(base)
    _hcert = (base.get('hertzian') or {}).get('solve_certificate_full')
    chk('X1 실 생산자 세 모드 레코드에 FULL 증서가 있고 (증서 문제 없음) 계약 g2 · 문제 없음',
        isinstance(_hcert, dict) and nc.certificate_problem(_hcert) is None and _okb.get('generation') == 'g2' and not _okb.get('problems'),
        (_hcert if not isinstance(_hcert, dict) else nc.certificate_problem(_hcert), _okb))
    _c2 = _cert_case(lambda d: d['hertzian'].pop('solve_certificate_full', None))
    chk('X2 ★ 주 Hertz FULL 증서 삭제 → 세대 invalid (부분 결손 — 증서도 세대 2 필수 필드)',
        _c2.get('generation') == 'invalid' and 'solve_certificate_full' in _probs_text(_c2), _c2)

    def _break(d):
        c = d['physics']['solve_certificate_full']
        c['I_top'] = -0.5 * float(c['I_bottom'])
        c['conservation_rel'] = abs(float(c['I_bottom']) + float(c['I_top'])) / max(abs(float(c['I_bottom'])), abs(float(c['I_top'])))
    _c3 = _cert_case(_break)
    chk('X3 ★ physics 증서의 전류 보존 실패 (기록값은 자기일관) → invalid · 사유에 보존',
        _c3.get('generation') == 'invalid' and '보존' in _probs_text(_c3), _c3)
    _c4 = _cert_case(lambda d: d['hertzian']['hertz_h12'].pop('solve_certificate_full', None))
    chk('X4 ★ H12 레코드 증서 삭제 → invalid', _c4.get('generation') == 'invalid' and 'hertz_h12' in _probs_text(_c4), _c4)
    _c5 = _cert_case(lambda d: d['hertzian']['solve_certificate_full'].update(method='cg+ilu'))
    chk('X5 ★ 지운 방법 (cg+ilu · SPD 아닌 전처리 CG) 의 증서 → invalid', _c5.get('generation') == 'invalid', _c5)
    _c6 = con_of(strip_g2(base))
    chk('X6 표지 · 증서를 다 뺀 역사 모양 → inferred_legacy (증서 키도 세대 2 표지)', _c6.get('generation') == 'inferred_legacy', _c6)

    #  ══ Y. ★ G2RR-02 — 증서 ↔ 가지 · 역할 · 발행값 결합 (Codex 세대 2 재검증 §3 · §7-2 · probes/acceptance.py 변이를 실 생산자 레코드 위에 · 1저자 비준) ══
    #     옛 계약 (G2R-03 통합) 은 `solve_certificate_full` **자리**의 증서 내부 일관성 (보존 · 잔차 · 방법) 만 봤다 → 같은 실행의 CF 증서 · H12 FULL 증서 ·
    #     전자 채널 증서를 주 Hertz FULL 자리에 복사해도 g2 · τ OK (우리 트리 재현 db74ea98).  기하 인자만 바꾼 증서 · 숫자만 바꾼 레코드 (두 표현
    #     항등식은 맞춤) · 실린 CF 숫자의 증서 삭제 · 보존 실패도 통과했다.  이제 증서의 가지 · 채널 · 역할 · 전극 · ΔV · 기하 (G→q) 를 자리 · 부모와
    #     대조하고 q = I_bottom/ΔV × T/A 를 저장 σ_ratio · σ_dim 의 반올림 반폭 안으로 재구성해야 한다.  양성: 정상 · GEN2-01 협착-only 미계산 ·
    #     진짜 비관통 · CF 모형 과전도 (표지는 증서 면제가 아니다).  옛 기록 정책: 결합 키 없는 세대 2 증서 = 거부 · 역사 194 (표지 없음) = inferred_legacy 그대로.
    MODES3 = ('hertz', 'physics', 'hertz_h12')
    CERTK = ('solve_certificate_full', 'solve_certificate_bulk_net', 'solve_certificate_constr_net')
    BIND = ('branch', 'channel', 'role', 'contact_mode', 'delta_V', 'geometry', 'g_to_q', 'sigma_bulk_S_cm')   # 독립 오라클 (생산자 상수를 베끼지 않는다)

    def _all_certs(du):
        for dk in ('hertzian', 'physics'):
            r = du.get(dk) or {}
            for rr in (r, r.get('hertz_h12')):
                if not isinstance(rr, dict):
                    continue
                for k in list(rr):
                    if k.endswith(CERTK) and isinstance(rr[k], dict):
                        yield rr[k]

    def _bed_produce(A_, C_, tm, am, box=10.0):
        return json.loads(json.dumps({cm: quiet(nc._run_all_networks, A_, C_, [1], am, tm, 1.0, 20.0, box, box, None, contact_mode=cm)
                                      for cm in ('hertzian', 'physics')}))

    def _geo(c):
        """증서의 기하 — 없으면 (고치기 전 생산자) 이 침대의 기하를 넣고 돌려준다 (변이가 옛 코드에서도 적용돼 실패로 보이게)."""
        return c.setdefault('geometry', {'plate_z': 20.0, 'box_x': 10.0, 'box_y': 10.0, 'scale': 1.0})

    def _g2q_x2(c):
        c['g_to_q'] = (c.get('g_to_q') or 0.2) * 2

    def _plate_x2(c):
        _geo(c)['plate_z'] *= 2

    def _y_cf_disguised(d):
        """CF 증서를 가지 표기 'full' 로 바꾸고 기하 (판 높이) 를 발행 q 에 맞춰 재척도 — 증서 하나 안은 자기일관 (g_to_q = T/A · 재구성 = 발행 q) ·
        같은 실행의 다른 증서들과 기하가 다르다 (봉인된 기하 대조만 잡는다)."""
        r = d['hertzian']
        c = copy.deepcopy(r['solve_certificate_bulk_net'])
        g = _geo(c)
        a_ = g['box_x'] * g['box_y'] * g['scale'] ** 2
        g['plate_z'] = r['sigma_full'] / c['I_bottom'] * a_ / g['scale']
        c['g_to_q'] = (g['plate_z'] * g['scale']) / a_
        c['branch'] = 'full'
        r['solve_certificate_full'] = c

    def _y_all_geom(d):
        for c in _all_certs(d):
            _plate_x2(c)
            _g2q_x2(c)

    def _y_numbers(d):
        for dk in ('hertzian', 'physics'):
            r = d[dk]
            r['sigma_full'] = round(r['sigma_full'] * 1.25, 8)
            r['sigma_full_mScm'] = round(r['sigma_full'] * r['sigma_grain_S_cm'] * 1000, 6)      # 두 표현 항등식은 맞춘다 (공용 기술 검사 통과)

    def _y_cf_numbers(d):
        r = d['hertzian']
        r['sigma_bulk_net'] = round(r['sigma_bulk_net'] * 2, 8)
        r['sigma_bulk_net_mScm'] = round(r['sigma_bulk_net'] * r['sigma_grain_S_cm'] * 1000, 6)

    def _y_unbound(d):
        for c in _all_certs(d):
            for k in BIND:
                c.pop(k, None)

    def _hz(d):
        return d['hertzian']
    YMUT = {
        'CF → FULL (Codex full_cert_from_cf)': lambda d: _hz(d).update(solve_certificate_full=copy.deepcopy(_hz(d)['solve_certificate_bulk_net'])),
        'H12 → H0 (Codex full_cert_from_h12)': lambda d: _hz(d).update(solve_certificate_full=copy.deepcopy(_hz(d)['hertz_h12']['solve_certificate_full'])),
        'H0 → H12 자리': lambda d: _hz(d)['hertz_h12'].update(solve_certificate_full=copy.deepcopy(_hz(d)['solve_certificate_full'])),
        'H0 → physics 자리': lambda d: d['physics'].update(solve_certificate_full=copy.deepcopy(_hz(d)['solve_certificate_full'])),
        '전자 채널 FULL → 이온 FULL 자리': lambda d: _hz(d).update(solve_certificate_full=copy.deepcopy(_hz(d)['electronic_solve_certificate_full'])),
        '기하 인자 g_to_q ×2': lambda d: _g2q_x2(_hz(d)['solve_certificate_full']),
        '기하 판 높이 ×2 (g_to_q 그대로)': lambda d: _plate_x2(_hz(d)['solve_certificate_full']),
        '기하 판 높이 · g_to_q 함께 ×2 (증서 안 자기일관)': lambda d: (_plate_x2(_hz(d)['solve_certificate_full']),
                                                         _g2q_x2(_hz(d)['solve_certificate_full'])),
        'CF 증서 위장 (가지 full · 기하 재척도 — 재구성 맞음)': _y_cf_disguised,
        '모든 증서 기하 ×2 (한 실행 안 일관)': _y_all_geom,
        'ΔV 2': lambda d: _hz(d)['solve_certificate_full'].update(delta_V=2.0),
        '숫자만 ×1.25 (σ_ratio · σ_dim 항등식 맞춤 · 두 모드)': _y_numbers,
        'CF 숫자만 ×2 (σ_ratio · σ_dim 맞춤)': _y_cf_numbers,
        'CF 증서 보존 실패 (Codex cf_bad_conservation)': lambda d: _hz(d)['solve_certificate_bulk_net'].update(I_top=0.0, conservation_rel=1.0),
        'CF 증서 삭제 (Codex missing_cf_cert)': lambda d: _hz(d).pop('solve_certificate_bulk_net'),
        '협착-only 증서 삭제 (숫자 실림 · Codex missing_constr_cert)': lambda d: _hz(d).pop('solve_certificate_constr_net'),
        'CF 숫자 실림 ↔ 상태 not_computed': lambda d: _hz(d).update(sigma_bulk_net_status='not_computed'),
        '결합 키 없는 증서 (G2RR-02 이전 세대 2 증서 모양)': _y_unbound,
    }

    def sY():
        c0, o0 = con_of(base), cols(base)
        hc = base['hertzian'].get('solve_certificate_full') or {}
        chk('Y0 양성 — 실 생산자 레코드 (세 모드 · 이온 · 전자 · 열) = g2 · 문제 없음 · 세 모드 OK · 주 FULL 증서에 결합 키 (가지 · 채널 · 역할 · 전극 · ΔV · '
            '기하 · G→q · σ₀) 가 있다',
            c0.get('generation') == 'g2' and not c0.get('problems') and all(o0.get(f'ion_net_status_{m}') == 'OK' for m in MODES3)
            and all(k in hc for k in BIND), (c0.get('problems'), sorted(set(BIND) - set(hc))))
        got = {}
        for lab, fn in YMUT.items():
            d2 = copy.deepcopy(base)
            fn(d2)
            c, o = con_of(d2), cols(d2)
            got[lab] = (c.get('generation'), tuple((o.get(f'ion_net_status_{m}'), _rc(o.get(f'ion_net_status_reason_{m}'))) for m in MODES3),
                        o.get('tau2_ion_hertz'), _probs_text(c))
        want = ('invalid', (('NOT_COMPUTED', 'invalid_input'),) * 3, None)
        bad = {k: (v[0], v[1], v[2], v[3][:160]) for k, v in got.items() if v[:3] != want}
        chk(f'Y1 ★ 증서 결합 변이 {len(YMUT)} 종 (CF → FULL · H12 → H0 · 채널 · 기하 인자 · ΔV · 숫자만 · CF 진단 증서 · 결합 키 없음) → 세대 invalid · 세 모드 '
            f'NOT_COMPUTED (invalid_input) · 주 tau2 빈칸 (옛: CF → FULL · H12 → H0 · 기하 · 숫자만 · CF 진단 넷 = g2 · OK) {bad or ""}',
            not bad and len(got) == len(YMUT))
        why = {k: v[3] for k, v in got.items()}
        chk('Y2 ★ 사유가 무엇을 어겼는지 말한다 — CF → FULL = 가지 · H12 → H0 = 역할 · 전자 → 이온 = 채널 · 위장 CF = 기하 · 숫자만 = 재구성 · '
            '결합 키 없음 = G2RR-02 이전 증서',
            '가지' in why['CF → FULL (Codex full_cert_from_cf)'] and '역할' in why['H12 → H0 (Codex full_cert_from_h12)']
            and '채널' in why['전자 채널 FULL → 이온 FULL 자리'] and '기하' in why['CF 증서 위장 (가지 full · 기하 재척도 — 재구성 맞음)']
            and '재구성' in why['숫자만 ×1.25 (σ_ratio · σ_dim 항등식 맞춤 · 두 모드)']
            and 'G2RR-02 이전' in why['결합 키 없는 증서 (G2RR-02 이전 세대 2 증서 모양)'],
            {k: v[:200] for k, v in why.items()})
        #  양성 대조 셋 — 해 없는 가지는 증서를 요구하지 않는다 (숫자 없음 ↔ 상태 일치만) · 모형 과전도 표지는 증서 면제가 아니다
        Acl = {i: {'type': 1, 'x': 0.0, 'y': 0.0, 'z': float(z), 'radius': 1.0} for i, z in enumerate(range(21), 1)}
        Ccl = [{'id1': i, 'id2': i + 1, 'contact_area': (math.pi * 1.02 ** 2 if i == 10 else 0.1), 'delta': 0.05} for i in range(1, 21)]
        dcl = _bed_produce(Acl, Ccl, {1: 'SE'}, [])
        ccl, ocl = con_of(dcl), cols(dcl)
        pcl = dcl['physics']
        chk('Y3 ★ 양성 GEN2-01 — 협착-only R_c = 0 (physics · H12) = NOT_COMPUTED zero_resistance_requires_contraction · 그 증서는 해를 주장하지 않는다 · '
            '세대 g2 · 문제 없음 · 세 모드 OK (FULL 유지 — 없는 수렴 증서를 요구하지 않는다)',
            ccl.get('generation') == 'g2' and not ccl.get('problems') and all(ocl.get(f'ion_net_status_{m}') == 'OK' for m in MODES3)
            and pcl.get('sigma_constr_net') is None and pcl.get('sigma_constr_net_reason') == 'zero_resistance_requires_contraction'
            and (pcl.get('solve_certificate_constr_net') or {}).get('status') == 'not_computed'
            and (pcl.get('solve_certificate_constr_net') or {}).get('I_bottom') is None,
            (ccl.get('problems'), {m: ocl.get(f'ion_net_status_{m}') for m in MODES3}))
        dfake = copy.deepcopy(dcl)
        _fc = copy.deepcopy(dfake['physics']['solve_certificate_full'])
        _fc['branch'] = 'constriction_only'
        dfake['physics']['solve_certificate_constr_net'] = _fc
        cfk = con_of(dfake)
        chk('Y4 ★ 해 없는 협착-only 자리에 수렴 증서 (FULL 증서를 가지만 바꿔) → invalid (거짓 수렴으로 채우지 않는다)',
            cfk.get('generation') == 'invalid' and 'solve_certificate_constr_net' in _probs_text(cfk), _probs_text(cfk)[:300])
        Ant = {i: {'type': 1, 'x': 3.0 * i, 'y': 0.0, 'z': z, 'radius': 1.0} for i, z in ((1, 0.0), (2, 1.0), (3, 2.0))}
        Ant.update({10 + k: {'type': 1, 'x': 0.0, 'y': 5.0, 'z': float(z), 'radius': 1.0} for k, z in enumerate(range(10, 21))})
        Cnt = [{'id1': 10 + k, 'id2': 11 + k, 'contact_area': 0.1, 'delta': 0.05} for k in range(10)]
        dnt = _bed_produce(Ant, Cnt, {1: 'SE'}, [])
        phi_nt = sum(4.0 / 3.0 * math.pi * a['radius'] ** 3 for a in Ant.values()) / (10.0 * 10.0 * 20.0)
        ont = tf.ion_columns(dnt, {'thickness_um': 20.0, 'thickness_mass_conserving_um': 20.0, 'phi_se_mass_conserving': phi_nt}, 0.0)
        cnt = con_of(dnt)
        chk('Y5 ★ 양성 진짜 비관통 — 세 가지 모두 숫자 없음 · valid_zero (no_through_path) · 증서는 해를 주장하지 않는다 → g2 · 문제 없음 · 세 모드 NOT_PERCOLATING',
            cnt.get('generation') == 'g2' and not cnt.get('problems') and all(ont.get(f'ion_net_status_{m}') == 'NOT_PERCOLATING' for m in MODES3)
            and all((dnt['hertzian'].get(k) or {}).get('I_bottom') is None for k in CERTK),
            (cnt.get('problems'), {m: ont.get(f'ion_net_status_{m}') for m in MODES3}))
        dmo = _bed_produce(Acl, [dict(c, contact_area=0.1) for c in Ccl], {1: 'SE'}, [], box=1.0)
        cmo = con_of(dmo)
        hmo = dmo['hertzian']
        dmo_b = copy.deepcopy(dmo)
        dmo_b['hertzian']['solve_certificate_bulk_net'].update(I_top=0.0, conservation_rel=1.0)
        cmo_b = con_of(dmo_b)
        chk('Y6 ★ CF 모형 과전도 (상자 1 × 1 · q > 1.5 · model_over_conduction) — 그 CF 숫자도 결합 증서 검사를 통과해야 한다: 정상 = g2 · 문제 없음 · '
            '같은 증서의 보존을 깨면 invalid (표지는 증서 면제가 아니다)',
            hmo.get('sigma_bulk_net_status') == 'model_over_conduction' and cmo.get('generation') == 'g2' and not cmo.get('problems')
            and cmo_b.get('generation') == 'invalid' and 'solve_certificate_bulk_net' in _probs_text(cmo_b),
            (hmo.get('sigma_bulk_net_status'), cmo.get('problems'), _probs_text(cmo_b)[:200]))
        chk('Y7 옛 기록 정책 — 표지 · 증서를 다 뺀 역사 모양은 inferred_legacy 그대로 (결합 검사 대상 아님 · 역사 194 = P2) · 결합 키만 없는 세대 2 증서는 '
            'invalid (Y1) — 결합 키를 지워 옛 증서로 위장할 수 없다',
            con_of(strip_g2(base)).get('generation') == 'inferred_legacy' and got['결합 키 없는 증서 (G2RR-02 이전 세대 2 증서 모양)'][0] == 'invalid')
    _guard('Y', sY)

    #  ══ Z. ★ 10-07 G2RR2-04 · 05 (Codex 세대 2 재검증 2 §5 · §6) — σ₀ 결합 · 진단 가지 기록 결손을 실 생산자 레코드 위에 (공용 계약 단위) ══════════════
    #     옛 계약: CF · 협착-only 차원값을 그 증서 자신의 σ₀ 로 재구성 (증서 ↔ 부모 σ₀ 미대조) · 부모 σ₀ ↔ 온도 규약 미대조 · 상태 키가 없는 가지 = 통과.
    #     e2e (게시 · 인계 · 다시 읽기) 는 webapp/test_gen2_publication_handover ⑥ · ⑦ · ⑧.
    def _z_cf_s0(d, k='solve_certificate_bulk_net', qk='sigma_bulk_net', dk='sigma_bulk_net_mScm', mode='hertzian'):
        r = d[mode]
        r[k]['sigma_bulk_S_cm'] = r[k]['sigma_bulk_S_cm'] * 2
        if qk and r.get(qk) is not None:
            r[dk] = round(r[qk] * r[k]['sigma_bulk_S_cm'] * 1000, 6)

    def _z_parent_s0(d):
        for r in (d['hertzian'], d['hertzian']['hertz_h12'], d['physics']):
            r['sigma_grain_S_cm'] *= 2
            r['sigma_full_mScm'] = round(1000 * r['sigma_grain_S_cm'] * r['sigma_full'], 6)

    def _z_tc(d):
        for r in (d['hertzian'], d['hertzian']['hertz_h12'], d['physics']):
            r['temperature_provenance']['T_C'] = 60.0

    def _z_absent(d):
        for k in ('sigma_bulk_net', 'sigma_bulk_net_mScm', 'sigma_bulk_net_status', 'sigma_bulk_net_reason', 'solve_certificate_bulk_net'):
            d['hertzian'].pop(k, None)

    def _z_honest(d, reason='solve_failed'):
        """정직한 실패 모양 (생산자 `_net_sigma_status` · `solve_certificate` 가 첫 단 예외에 내는 것) — 값 없음 · not_computed · 사유 · 해를 주장하지 않는 증서."""
        r = d['hertzian']
        c = r['solve_certificate_bulk_net']
        c.update(status='solve_failed', reason='solve_failed', I_bottom=None, I_top=None, conservation_rel=None, residual_rel=None)
        r.update(sigma_bulk_net=None, sigma_bulk_net_mScm=None, sigma_bulk_net_status='not_computed', sigma_bulk_net_reason=reason)
        r.pop('R_brug_over_full', None)

    ZMUT = {
        'CF 증서 σ₀ ×2 + CF 차원값 그 σ₀ 로 재계산 (Codex cf_sigma0_x2)': _z_cf_s0,
        'FULL 증서 σ₀ ×2 (Codex full_cert_sigma0_x2 — FULL 숫자 그대로)': lambda d: _z_cf_s0(d, 'solve_certificate_full', None),
        '협착-only 증서 σ₀ ×2 + 그 차원값 재계산': lambda d: _z_cf_s0(d, 'solve_certificate_constr_net', 'sigma_constr_net', 'sigma_constr_net_mScm'),
        'physics CF 증서 σ₀ ×2 + 차원값 재계산': lambda d: _z_cf_s0(d, mode='physics'),
        'H12 FULL 증서 σ₀ ×2': lambda d: d['hertzian']['hertz_h12']['solve_certificate_full'].update(
            sigma_bulk_S_cm=d['hertzian']['hertz_h12']['solve_certificate_full']['sigma_bulk_S_cm'] * 2),
        '부모 σ₀ 만 ×2 (모드 셋 · FULL 차원값 재계산 — 두 표현 항등식 맞춤 · 증서 그대로)': _z_parent_s0,
        '부모 온도 규약 T_C 만 60 °C (모드 셋 · σ₀ · 배수 그대로)': _z_tc,
        '전자 채널 FULL 증서 σ_bulk = 이온 σ₀ (채널 기준 전도도가 아니다)': lambda d: d['hertzian']['electronic_solve_certificate_full'].update(
            sigma_bulk_S_cm=d['hertzian']['sigma_grain_S_cm']),
        '열 채널 증서 채널 이름 electronic': lambda d: d['physics']['thermal_solve_certificate_full'].update(channel='electronic'),
        'CF 다섯 키 삭제 (Codex diagnostic_fields_absent)': _z_absent,
        'CF 사유 없는 not_computed (값 · 증서 없음)': lambda d: (_z_honest(d), d['hertzian'].update(sigma_bulk_net_reason=None)),
        'CF 모르는 상태 failed (값 없음)': lambda d: (_z_honest(d), d['hertzian'].update(sigma_bulk_net_status='failed')),
    }

    def sZ():
        got = {}
        for lab, fn in ZMUT.items():
            d2 = copy.deepcopy(base)
            fn(d2)
            c, o = con_of(d2), cols(d2)
            got[lab] = (c.get('generation'), tuple((o.get(f'ion_net_status_{m}'), _rc(o.get(f'ion_net_status_reason_{m}'))) for m in MODES3),
                        o.get('tau2_ion_hertz'), _probs_text(c))
        want = ('invalid', (('NOT_COMPUTED', 'invalid_input'),) * 3, None)
        bad = {k: (v[0], v[1], v[2], v[3][:160]) for k, v in got.items() if v[:3] != want}
        chk(f'Z1 ★ G2RR2-04 · 05 변이 {len(ZMUT)} 종 (증서 σ₀ 넷 · 부모 σ₀ · 온도 규약 · 전자 · 열 채널 기준 · 가지 기록 결손 · 사유 없음 · 모르는 상태) → 세대 '
            f'invalid · 세 모드 NOT_COMPUTED (invalid_input) · 주 tau2 빈칸 (옛: σ₀ 변이 · 채널 · 결손 = g2 · OK) {bad or ""}',
            not bad and len(got) == len(ZMUT))
        why = {k: v[3] for k, v in got.items()}
        chk('Z2 ★ 사유 — σ₀ 변이 = G2RR2-04 · 결손 · 사유 없음 · 모르는 상태 = G2RR2-05',
            all('G2RR2-04' in why[k] for k in list(ZMUT)[:9]) and all('G2RR2-05' in why[k] for k in list(ZMUT)[9:]),
            {k: v[:160] for k, v in why.items()})
        dh = copy.deepcopy(base)
        _z_honest(dh)
        ch, oh = con_of(dh), cols(dh)
        dh2 = copy.deepcopy(base)
        _z_honest(dh2, 'current_conservation_failed')
        dh2['hertzian']['solve_certificate_bulk_net'].update(status='not_computed', reason='current_conservation_failed')
        ch2 = con_of(dh2)
        chk('Z3 ★ 양성 — 정직한 CF 실패 (값 없음 · not_computed · 사유 solve_failed / current_conservation_failed · 해를 주장하지 않는 증서) = g2 · 문제 없음 · '
            '세 모드 OK (FULL 유지) · 다시 읽기 K7 이 쓰는 공용 가지 표도 [] · 전자 증서 σ_bulk (채널 기준 0.05) ≠ 이온 σ₀ 인 정상 레코드 = 문제 없음',
            ch.get('generation') == 'g2' and not ch.get('problems') and all(oh.get(f'ion_net_status_{m}') == 'OK' for m in MODES3)
            and ch2.get('generation') == 'g2' and not ch2.get('problems') and tf.branch_table_problems('hertz', dh['hertzian']) == []
            and base['hertzian']['electronic_solve_certificate_full'].get('sigma_bulk_S_cm') != base['hertzian']['sigma_grain_S_cm']
            and not con_of(base).get('problems'),
            (ch.get('problems'), ch2.get('problems')))
        Ah = {i: {'type': 1, 'x': 0.0, 'y': 0.0, 'z': float(z), 'radius': 1.0} for i, z in enumerate(range(21), 1)}
        Ch = [{'id1': i, 'id2': i + 1, 'contact_area': 0.1, 'delta': 0.05} for i in range(1, 21)]
        dT = json.loads(json.dumps({cm: quiet(nc._run_all_networks, Ah, Ch, [1], [], {1: 'SE'}, 1.0, 20.0, 10.0, 10.0, None, contact_mode=cm,
                                              temp_c=60.0) for cm in ('hertzian', 'physics')}))
        cT = con_of(dT)
        s60 = dT['hertzian']['sigma_grain_S_cm']
        chk(f'Z4 양성 — 정상 온도 적용 (생산자 temp_c 60) = g2 · 문제 없음 · 부모 σ₀ = 증서 σ₀ = 60 °C 규약값 {s60} · 온도 규약 대조 없음',
            cT.get('generation') == 'g2' and not cT.get('problems') and s60 != 0.003
            and tf.sigma0_convention_problem(dT['hertzian']) is None
            and {c_.get('sigma_bulk_S_cm') for c_ in _all_certs(dT) if c_.get('channel') == 'ionic'} == {s60}, cT.get('problems'))
    _guard('Z', sZ)

    #  ★ 10-06 밤 G2R-04 — [H0, H12] 는 두 규약의 쌍대응 시나리오 (오차막대 · 상하한 · 신뢰구간 아님) · ±5 % 는 시험한 기하 한정
    import lhs_design_dataset as _ldd
    _v = getattr(_ldd, 'TAU_NET_VERDICT_H12', '')
    _dr = open(os.path.join(ROOT, 'docs', 'reviews', 'gen2_network_design_20261006.md'), encoding='utf-8').read()
    chk('W1 ★ 열 사전 H12 판정 = 쌍대응 시나리오 · 구간 아님 (괄호로 읽는다 문구 없음) · 부록 전용 유지',
        '쌍대응 시나리오' in _v and '신뢰구간이 아니다' in _v and '괄호로 읽는다' not in _v and '부록 전용' in _v, _v[:200])
    chk('W2 ★ 설계 기록 ±5 % = 시험한 기하 한정 + 구 사슬 반례 (G2R-04)', '시험한 기하' in _dr and '구 사슬 z = 2' in _dr)

    print(f'\ntest_gen2_role_contract: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
