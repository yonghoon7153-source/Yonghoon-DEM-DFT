#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""망 세대 도장 ↔ 레코드 대조 — Codex 세대 2 재검증 G2RR-01 (P2 · 판정문 §2 · §7-1 · 1저자 비준 10-06 밤 *"권고대로"*).

  python3 webapp/test_gen2_stamp_record.py

★ 시험 먼저 — 옛 코드 (70a6d91a4) 에서 빨갛다.  Codex `probes/acceptance.py` 의 도장 변이를 **실 생산자 → 게시 → 인계** 사슬 그대로 상주시킨다
  (우리 트리 재현 `docs/reviews/codex_gen2_network_reverify_evidence_20261006/_reproduction_ours/` §5 — control g2 · all_unknown g2 · all_null g2 ·
  one_null_legacy_shape inferred_legacy · g2_declares_legacy g2 · stamp_absent_keys 거부):
  A  게시자 = 유도 — 실 CLI 가 게시한 활성 도장의 네 세대 값 = 그 폴더 레코드에서 유도한 값 (`pipeline_service.generation_stamp_values` — 게시와
     인계 대조가 같은 함수) = 세대 2 값 (오라클 = 생산자 상수 · 타입까지) · 도장 파일 모양 (키 · 순서) 그대로 · 상수 짝 (세대 2 도장 값 ·
     세대 이름 = tau_flux · 인계 생성기)
  S  g2 인계 (`lhs_design_dataset.load_tau_results`) — 게시된 정상 g2 폴더 사본에서 **도장 네 세대 필드만** 바꾼 변이 (입력 · 숫자 · 레코드 ·
     실행 ID 그대로): Codex 셋 (all_unknown · all_null · g2_declares_legacy) · 키 하나씩 결손 · null · unknown · legacy 값 · 타입 (hertz_h12 = 1 ·
     'True') → 전부 τ P4 거부 (G2RR-01) · 네 키 삭제 (기존 거부 · 회귀) · 정상 g2 도장 = 통과 (칸 = 같은 폴더의 tau_flux.case_row)
  H  역사 경로 = 확인된 역사 도장 스키마만 (194 v1.2 배치 실측 194/194 = 8 키 · solver · units_contract · argv contact_mode both · 세대 키 없음):
     정확한 역사 모양 = inferred_legacy 통과 · Codex one_null_legacy_shape (electrode_model=null) · 옛 세대 값 넷을 적은 도장 · 모르는 키 ·
     키 결손 (argv) · argv contact_mode ≠ both · units_contract 다름 → 거부 · 진짜 역사 194 (v1.2 배치 원천 도장 + dual) = 같은 함수 194/194 통과 ·
     같은 진짜 레코드에 Codex 변이 · 세대 2 값 도장 = 거부
  M  배치 manifest 기대 세대 (`load_tau_results(expected_generation=)` · `tau_manifest_expected_generation` — manifest 의 expected_network_generation):
     같으면 통과 (기대 세대가 결과에 남는다) · g2 폴더에 inferred_legacy · 역사 폴더에 g2 = 거부 · 모르는 값 · 선언 없는 manifest (194 v1.2 런처
     manifest 포함) · 없는 파일 = 거부
  W  웹앱 (J20-l) — 케이스 페이지 "망 세대" 행에 같은 대조 (`app._ion_handover_stamp` = 인계와 같은 함수): 어긋나면 "⚠ 도장 ↔ 레코드 불일치 —
     인계 거부 (G2RR-01)" · 정상 g2 · 정확한 역사 모양은 화면 그대로 · 라우트 배선 · 툴팁에 새 규칙 (옛 "도장이 세대 2 게시를 말하면" 문구 없음)
⚠ 범위 — 도장 · 레코드 · 모든 사본을 함께 일관되게 바꾼 편집은 못 잡는다 (TAU_SAME_GEN_BASIS · 게시 시점 해시 없음 — 요청서 §5 의 한계와 같다).
"""
import json
import os
import re
import shutil
import sys
import tarfile
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCRIPTS = ROOT / 'scripts'
for _p in (str(HERE), str(SCRIPTS)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import pipeline_service as ps                   # noqa: E402
import test_gen2_publication_handover as PH     # noqa: E402  (실 생산자 게시 · 강제 폴더 — 같은 도구)

ARCHIVE = ROOT / 'docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/net194_tau_sources_20261006.tar.gz'
MANIFEST_194 = ROOT / 'docs/data/lhs_network194_11fcf91e8/manifest.json'
#  오라클 — 게시자 (`stamp_network_provenance`) 가 쓰는 네 세대 키 · 194 v1.2 도장 실측 키 (도우미 상수를 베끼지 않는다)
KEYS = ('psi_placement_physics', 'electrode_model', 'area_rule_physics', 'hertz_h12')
HIST_KEYS = ('argv', 'code_sha', 'input_digests', 'network_run_id', 'solver', 'solver_status', 'stamped_at', 'units_contract')
LEGACY_VALUES = {'psi_placement_physics': 'legacy_divide', 'electrode_model': 'virtual_source_legacy', 'area_rule_physics': 'physics_g1',
                 'hertz_h12': False}
GEN = '망 세대 (세대 계약 · G2R-01 · 02)'
PASS = FAIL = 0


def chk(label, ok, detail=''):
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f'  PASS {label}')
    else:
        FAIL += 1
        print(f'  FAIL {label}' + (f' — {str(detail)[:400]}' if detail else ''))


def _canon(v):
    return json.dumps(v, sort_keys=True, default=str)


def _refused(e, *tags):
    return e.startswith('FillRefusal') and all(t in e for t in tags)


def main():
    import app
    import network_conductivity as nc
    import tau_flux as tf
    import lhs_webapp_batch as LWB
    import lhs_design_dataset as LDD
    gsv = getattr(ps, 'generation_stamp_values', None)
    gpp = getattr(ps, 'provenance_generation_problem', None)
    oracle = {'psi_placement_physics': nc.PSI_MULTIPLY, 'electrode_model': nc.ELECTRODE_DIRICHLET, 'area_rule_physics': nc.AREA_RULE_G2,
              'hertz_h12': True}
    tmp = Path(tempfile.mkdtemp(prefix='g2sr_'))
    made = []
    try:
        print('A 게시자 = 유도 — 실 CLI 가 게시한 활성 도장 (network_provenance.json)')
        b_d, b_st, b_f, b_rid = PH._publish(app, 'baseline')
        made.append(b_d)
        prov0 = json.loads((Path(b_d) / ps.PROVENANCE_FILE).read_text(encoding='utf-8'))
        dual0 = json.loads((Path(b_d) / 'network_conductivity_dual.json').read_text(encoding='utf-8'))
        stamp0 = {k: prov0.get(k, 'ABSENT') for k in KEYS}
        chk(f'A1 양성 — 실 생산자 게시 = done · 활성 도장의 네 세대 값 = 세대 2 값 (생산자 상수 · hertz_h12 는 bool True) {stamp0}',
            b_st == 'done' and _canon(stamp0) == _canon(oracle) and prov0.get('hertz_h12') is True, PH._why(b_f))
        derived = gsv(dual0) if callable(gsv) else None
        chk('A2 ★ 레코드에서 유도한 기대값 (pipeline_service.generation_stamp_values — 게시 · 인계 대조가 같은 함수) = 게시된 도장 네 값 (타입까지)',
            derived is not None and _canon(derived) == _canon(stamp0), derived if derived is not None else '도우미 없음 (옛 코드)')
        chk('A3 도장 파일 모양 그대로 — 12 키 · 순서 (유도를 한 함수로 옮겨도 게시 출력은 같다)',
            list(prov0) == ['network_run_id', 'code_sha', 'stamped_at', 'solver_status', 'solver', 'argv', 'units_contract', 'input_digests',
                            *KEYS], list(prov0))
        chk('A4 상수 짝 — pipeline_service.NETWORK_GENERATION2_STAMP = 생산자 상수 오라클 · NETWORK_GEN_G2 · LEGACY = tau_flux.NET_GEN_G2 · NET_GEN_LEGACY = '
            'lhs_design_dataset.TAU_EXPECTED_GENERATIONS (사본끼리 어긋나면 대조가 다른 세대 이름을 본다)',
            _canon(dict(getattr(ps, 'NETWORK_GENERATION2_STAMP', ()))) == _canon(oracle)
            and (getattr(ps, 'NETWORK_GEN_G2', None), getattr(ps, 'NETWORK_GEN_LEGACY', None)) == (tf.NET_GEN_G2, tf.NET_GEN_LEGACY)
            == tuple(getattr(LDD, 'TAU_EXPECTED_GENERATIONS', ())))

        print('S g2 인계 — 게시된 정상 g2 폴더 사본에서 도장 네 세대 필드만 바꾼다 → load_tau_results (출처 관문 P0–P4)')
        st0 = json.loads((ROOT / 'docs/data/lhs_webapp_contact_d1ec42fba' / 'status.json').read_text(encoding='utf-8'))

        def _load(tag, cases, **kw):
            root = tmp / ('tau_' + re.sub(r'[^0-9A-Za-z_]', '_', tag))
            res_ = root / 'results'
            res_.mkdir(parents=True)
            stx = json.loads(json.dumps(st0))
            stx.update(stop_after='network', cases={})
            rowsx = {}
            for c, d_ in cases.items():
                shutil.copytree(d_, res_ / c)
                fm_ = json.loads((res_ / c / 'full_metrics.json').read_text(encoding='utf-8'))
                stx['cases'][c] = dict(case=c, stop_after='network', status='done', failed_stages=[], network_run_id=fm_['network_run_id'])
                rowsx[c] = dict({k: v for k, v in fm_.items() if not isinstance(v, (dict, list))}, case=c)
            LWB.write_outputs(root / 'batch', stx, rowsx)
            try:
                return LDD.load_tau_results(res_, LDD.load_webapp(root / 'batch'), **kw), ''
            except Exception as e:                                       # noqa: BLE001 — 옛 코드 (인자 · 도우미 없음) 도 실패로 센다
                return None, f'{type(e).__name__}: {e}'

        def _stamped(tag, base, edit, via_reader=False):
            """base 폴더 사본에서 도장만 바꾼다 — via_reader = Codex 처럼 read_network_provenance 로 읽어 (provenance_state 포함) 다시 쓴다."""
            dst = tmp / ('stamp_' + re.sub(r'[^0-9A-Za-z_]', '_', tag))
            shutil.copytree(base, dst)
            pp = dst / ps.PROVENANCE_FILE
            p = ps.read_network_provenance(str(dst)) if via_reader else json.loads(pp.read_text(encoding='utf-8'))
            if edit is not None:
                edit(p)
            pp.write_text(json.dumps(p), encoding='utf-8')
            return dst

        def _cells(tv):
            return ((tv or {}).get('cases') or {}).get('lhs00_000', {}).get('cells') or {}

        f_ctrl = _stamped('control', b_d, None, via_reader=True)
        tv_c, e_c = _load('control', {'lhs00_000': f_ctrl})
        want_c = {c: tf._cell(v) for c, v in tf.case_row(str(f_ctrl)).items() if c in tf.column_names()}
        chk("S0 양성 — 정상 g2 도장 (Codex control · 읽은 그대로 다시 씀) → 통과 · 세대 칸 'g2' · 칸 = 같은 폴더의 tau_flux.case_row",
            not e_c and _cells(tv_c).get('ion_net_generation') == 'g2' and _cells(tv_c) == want_c, e_c[:300])
        codex3 = {'all_unknown': lambda p: p.update({k: 'unrecognized' for k in KEYS}),
                  'all_null': lambda p: p.update({k: None for k in KEYS}),
                  'g2_declares_legacy': lambda p: p.update(LEGACY_VALUES)}
        stop = {}
        for lab, ed in codex3.items():
            stop[lab] = _load(lab, {'lhs00_000': _stamped(lab, b_d, ed, via_reader=True)})[1]
        bad = {k: (v[:120] or '통과 (g2 로 인계)') for k, v in stop.items() if not _refused(v, 'τ P4', 'G2RR-01')}
        chk(f'S1 ★ Codex 모순 변이 셋 (네 값 전부 unrecognized · 전부 null · virtual_source_legacy/physics_g1/legacy_divide/hertz_h12=False) → '
            f'τ P4 거부 (G2RR-01 · 옛: 셋 다 g2 로 인계) {bad or ""}', not bad and len(stop) == 3)
        _e_abs = _load('stamp_absent_keys', {'lhs00_000': _stamped('stamp_absent_keys', b_d, lambda p: [p.pop(k, None) for k in KEYS],
                                                                   via_reader=True)})[1]
        stop['stamp_absent_keys'] = _e_abs
        chk('S2 회귀 — 네 키 자체를 삭제한 도장 (세대 2 이전 도장 모양) → τ P4 거부 (기존 G2R-02 거울 · 그대로)',
            _refused(_e_abs, 'τ P4', '세대'), _e_abs[:300] or '통과')
        per = {}
        for k in KEYS:
            per[f'drop:{k}'] = lambda p, k=k: p.pop(k, None)
            per[f'null:{k}'] = lambda p, k=k: p.update({k: None})
            per[f'unknown:{k}'] = lambda p, k=k: p.update({k: 'unrecognized'})
            per[f'legacy:{k}'] = lambda p, k=k: p.update({k: LEGACY_VALUES[k]})
        for lab, ed in per.items():
            stop[lab] = _load(lab, {'lhs00_000': _stamped(lab, b_d, ed)})[1]
        bad = {k: (stop[k][:100] or '통과') for k in per if not _refused(stop[k], 'τ P4', 'G2RR-01')}
        chk(f'S3 ★ 키 하나만 — 결손 (부분 결손) · null · unknown · legacy 값 (네 키 × 넷 = 16) → 전부 τ P4 거부 (G2RR-01 · 옛: 결손 · 값 변이 다 통과) '
            f'{bad or ""}', not bad and len(per) == 16)
        typ = {'type:hertz_h12=1': lambda p: p.update(hertz_h12=1), "type:hertz_h12='True'": lambda p: p.update(hertz_h12='True')}
        for lab, ed in typ.items():
            stop[lab] = _load(lab, {'lhs00_000': _stamped(lab, b_d, ed)})[1]
        bad = {k: (stop[k][:100] or '통과') for k in typ if not _refused(stop[k], 'τ P4', 'G2RR-01')}
        chk(f"S4 ★ 타입 모순 — hertz_h12 = 1 (1 == True 인 느슨한 대조) · 'True' (문자열) → τ P4 거부 (JSON 정규형으로 엄격 대조) {bad or ''}",
            not bad)

        print('H 역사 경로 — 확인된 역사 도장 스키마만 (표지 없는 레코드 + 도장)')
        f_hist = PH._force(app, b_d, b_rid, 'legacy_shape', tmp / 'forced_hist', stamp='historical')
        tv_h, e_h = _load('hist_exact', {'lhs00_000': f_hist})
        ch = _cells(tv_h)
        chk("H1 양성 — 표지 없는 레코드 + 정확한 역사 도장 모양 (세대 2 이전 게시자 · 8 키) → 통과 · 세대 칸 'inferred_legacy' · 주 두 모드 OK",
            not e_h and ch.get('ion_net_generation') == 'inferred_legacy' and ch.get('ion_net_status_hertz') == ch.get('ion_net_status_physics') == 'OK',
            e_h[:300])
        hist_mut = {'one_null_legacy_shape': (lambda p: p.update(electrode_model=None), True),     # Codex 보조 탐침 (읽은 그대로 + null 한 키)
                    'hist_declares_g1': (lambda p: p.update(LEGACY_VALUES), False),
                    'hist_extra_key': (lambda p: p.update(generation='g1'), False),
                    'hist_missing_argv': (lambda p: p.pop('argv', None), False),
                    'hist_argv_hertzian': (lambda p: p['argv'].update(contact_mode='hertzian'), False),
                    'hist_units_other': (lambda p: p.update(units_contract='sim_to_real_v0'), False)}
        for lab, (ed, vr) in hist_mut.items():
            stop[lab] = _load(lab, {'lhs00_000': _stamped(lab, f_hist, ed, via_reader=vr)})[1]
        e_one = stop['one_null_legacy_shape']
        chk('H2 ★ Codex one_null_legacy_shape — 역사 모양 레코드 + electrode_model=null 한 키만 남긴 도장 → τ P4 거부 (G2RR-01 · 옛: inferred_legacy 로 통과 · '
            '"세대 2 를 말하지 않음" 은 역사성 증명이 아니다)', _refused(e_one, 'τ P4', 'G2RR-01'), e_one[:300] or '통과')
        bad = {k: (stop[k][:100] or '통과') for k in hist_mut if k != 'one_null_legacy_shape' and not _refused(stop[k], 'τ P4', 'G2RR-01')}
        chk(f'H3 ★ 확인된 역사 도장 스키마 밖 — 옛 세대 값 넷을 적은 도장 · 모르는 키 · argv 결손 · argv contact_mode hertzian · units_contract 다름 → '
            f'τ P4 거부 (G2RR-01) {bad or ""}', not bad and len(hist_mut) == 6)

        hist194 = tmp / 'hist194'
        with tarfile.open(ARCHIVE) as t:
            for mem in t.getmembers():
                if mem.isfile() and mem.name.endswith(('network_conductivity_dual.json', ps.PROVENANCE_FILE)):
                    d_ = hist194 / mem.name.split('/')[1]
                    d_.mkdir(parents=True, exist_ok=True)
                    with t.extractfile(mem) as fh:
                        (d_ / mem.name.split('/')[-1]).write_bytes(fh.read())
        r194, schemas = {}, set()
        for d_ in sorted(hist194.iterdir()):
            pv = ps.read_network_provenance(str(d_))
            du = json.loads((d_ / 'network_conductivity_dual.json').read_text(encoding='utf-8'))
            g_ = tf.network_generation_contract(du).get('generation')
            r194[d_.name] = (g_, gpp(pv, du, g_) if callable(gpp) else ['도우미 없음 (옛 코드)'])
            schemas.add(tuple(sorted(k for k in pv if k != 'provenance_state')))
        n_ok = sum(1 for g_, pr in r194.values() if g_ == 'inferred_legacy' and not pr)
        chk(f'H4 ★ 진짜 역사 194 (v1.2 배치 원천 도장 + dual · 인계 P4 와 같은 함수) → inferred_legacy · 도장 = 확인된 역사 도장 스키마 {n_ok}/{len(r194)}',
            len(r194) == 194 and n_ok == 194, next((v for v in r194.values() if v[1]), ''))
        chk(f'H5 역사 도장 스키마 오라클 — 194 도장의 키 집합은 하나 (8 키 · 세대 키 없음) = 도우미 상수 NETWORK_HISTORICAL_STAMP_KEYS {sorted(schemas)}',
            schemas == {HIST_KEYS} and set(getattr(ps, 'NETWORK_HISTORICAL_STAMP_KEYS', ())) == set(HIST_KEYS))
        d0 = hist194 / 'lhs00_000'
        pv0 = ps.read_network_provenance(str(d0))
        du0 = json.loads((d0 / 'network_conductivity_dual.json').read_text(encoding='utf-8'))
        rb = {lab: (gpp(dict(pv0, **ed), du0, 'inferred_legacy') if callable(gpp) else [])
              for lab, ed in (('electrode_model=null', {'electrode_model': None}), ('옛 세대 값 넷', LEGACY_VALUES), ('세대 2 값 넷', oracle))}
        chk(f'H6 ★ 같은 진짜 역사 레코드 (lhs00_000) + 도장에 세대 키 (null 한 키 · 옛 세대 값 넷 · 세대 2 값 넷) → 문제 (역사 스키마 아님) '
            f'{ {k: bool(v) for k, v in rb.items()} }', all(bool(v) for v in rb.values()))

        print('M 배치 manifest 기대 세대 — load_tau_results(expected_generation=…) · manifest 읽기')
        mres = {('g2', 'g2'): _load('m_g2_g2', {'lhs00_000': f_ctrl}, expected_generation='g2'),
                ('g2', 'inferred_legacy'): _load('m_g2_leg', {'lhs00_000': f_ctrl}, expected_generation='inferred_legacy'),
                ('hist', 'g2'): _load('m_hist_g2', {'lhs00_000': f_hist}, expected_generation='g2'),
                ('hist', 'inferred_legacy'): _load('m_hist_leg', {'lhs00_000': f_hist}, expected_generation='inferred_legacy'),
                ('g2', 'g3'): _load('m_bad', {'lhs00_000': f_ctrl}, expected_generation='g3')}
        okm = (not mres[('g2', 'g2')][1] and (mres[('g2', 'g2')][0] or {}).get('expected_generation') == 'g2'
               and _cells(mres[('g2', 'g2')][0]) == _cells(tv_c)
               and not mres[('hist', 'inferred_legacy')][1] and (mres[('hist', 'inferred_legacy')][0] or {}).get('expected_generation') == 'inferred_legacy')
        chk('M1 양성 — 기대 세대 = 레코드 세대 (g2 폴더 · g2 / 역사 폴더 · inferred_legacy) → 통과 · 결과에 expected_generation · 칸 = 대조 없는 판과 같다',
            okm, {k: v[1][:120] for k, v in mres.items()})
        badm = {f'{k[0]}·{k[1]}': (v[1][:100] or '통과') for k, v in mres.items()
                if k in (('g2', 'inferred_legacy'), ('hist', 'g2')) and not _refused(v[1], 'τ P4', '기대 세대')}
        chk(f'M2 ★ 기대 세대 ≠ 레코드 세대 (g2 폴더에 inferred_legacy · 역사 폴더에 g2) → τ P4 거부 (배치 manifest 교차 대조) {badm or ""}', not badm)
        chk('M3 모르는 기대 세대 (g3) → 거부 (닫힌 열거 · 대조를 약속했는데 못 하면 통과로 치지 않는다)',
            _refused(mres[('g2', 'g3')][1], '기대 세대'), mres[('g2', 'g3')][1][:200] or '통과')
        rd = getattr(LDD, 'tau_manifest_expected_generation', None)

        def _rd(x):
            try:
                return rd(x), ''
            except Exception as e:                                       # noqa: BLE001
                return None, f'{type(e).__name__}: {e}'
        mp = tmp / 'manifest_leg.json'
        mp.write_text(json.dumps({'schema': 'network_parallel_launcher/v1', 'expected_network_generation': 'inferred_legacy'}), encoding='utf-8')
        got = {'dict g2': _rd({'expected_network_generation': 'g2'}), 'file inferred_legacy': _rd(str(mp)),
               '선언 없음': _rd({'schema': 'network_parallel_launcher/v1'}), '모르는 값': _rd({'expected_network_generation': 'g9'}),
               '194 v1.2 런처 manifest (선언 없음)': _rd(str(MANIFEST_194)), '없는 파일': _rd(str(tmp / 'nope.json'))}
        chk(f'M4 ★ manifest 읽기 (tau_manifest_expected_generation) — 선언 = 값 · 선언 없음 · 모르는 값 · 194 v1.2 런처 manifest · 없는 파일 = 거부 '
            f'{ {k: (v[0] if not v[1] else v[1][:60]) for k, v in got.items()} }',
            callable(rd) and got['dict g2'] == ('g2', '') and got['file inferred_legacy'] == ('inferred_legacy', '')
            and all(_refused(got[k][1], '기대 세대') for k in ('선언 없음', '모르는 값', '194 v1.2 런처 manifest (선언 없음)', '없는 파일')))

        print('W 웹앱 (J20-l) — 케이스 페이지 망 세대 행 · 툴팁')
        stamp_fn = getattr(app, '_ion_handover_stamp', None)

        def _gen_cell(d_):
            fm_ = json.loads((Path(d_) / 'full_metrics.json').read_text(encoding='utf-8'))
            ih = app._ion_handover(str(d_), dict(fm_))
            m_ = dict(fm_, _ion_handover=ih)
            if callable(stamp_fn):
                m_['_ion_handover_stamp'] = stamp_fn(str(d_), ih)
            tables = {'network_summary': {'columns': ['지표', '값'], 'data': [['Porosity(%)', 15.0]]}}
            app.transform_network_summary_4col(tables, m_, {})
            r_ = next((r for r in tables['network_summary']['data'] if isinstance(r, list) and r and str(r[0]).strip() == GEN), None)
            return (r_[1], r_[2]) if r_ else (None, None)
        f_nostamp = tmp / 'stamp_none'
        shutil.copytree(f_ctrl, f_nostamp)
        (f_nostamp / ps.PROVENANCE_FILE).unlink()
        wc = {lab: _gen_cell(d_) for lab, d_ in (('control', f_ctrl), ('all_null', tmp / 'stamp_all_null'), ('hist_exact', f_hist),
                                                 ('one_null_legacy_shape', tmp / 'stamp_one_null_legacy_shape'), ('no_stamp', f_nostamp))}
        g2_txt, leg_txt = app.ION_HANDOVER_GEN_TEXT['g2'], app.ION_HANDOVER_GEN_TEXT['inferred_legacy']
        chk('W1 정상 g2 · 정확한 역사 모양 → 망 세대 행 그대로 (H · P = 세대 문구 · 덧붙임 없음 — 보통 화면 불변) · 도장 없는 폴더도 덧붙임 없음 '
            '(인계 τ P0 이 답한다 — 도장 이전 옛 케이스 화면에 표지를 뿌리지 않는다)',
            wc['control'] == (g2_txt, g2_txt) and wc['hist_exact'] == (leg_txt, leg_txt) and wc['no_stamp'] == (g2_txt, g2_txt), wc)
        _bad_w = [lab for lab in ('all_null', 'one_null_legacy_shape')
                  if not (wc[lab][0] and wc[lab][0] == wc[lab][1] and '도장 ↔ 레코드 불일치' in wc[lab][0] and 'G2RR-01' in wc[lab][0])]
        chk(f'W2 ★ 도장 모순 (all_null · one_null_legacy_shape) → 망 세대 행 끝에 "⚠ 도장 ↔ 레코드 불일치 — 인계 거부 (G2RR-01): …" (H · P 같은 값 · '
            f'인계와 같은 함수) {_bad_w or ""}', callable(stamp_fn) and not _bad_w
            and str(wc['all_null'][0]).startswith(g2_txt) and str(wc['one_null_legacy_shape'][0]).startswith(leg_txt), wc)
        src = (HERE / 'app.py').read_text(encoding='utf-8')
        i_ih = src.find("metrics['_ion_handover'] = _ion_handover(results_dir, metrics)")
        i_st = src.find("metrics['_ion_handover_stamp'] = _ion_handover_stamp(results_dir, metrics['_ion_handover'])")
        i_tr = src.find('    transform_network_summary_4col(tables, metrics, meta)')
        chk('W3 케이스 라우트 배선 — _ion_handover 뒤 · 표 변환 전에 _ion_handover_stamp 를 붙인다', 0 <= i_ih < i_st < i_tr, (i_ih, i_st, i_tr))
        html = (HERE / 'templates' / 'single.html').read_text(encoding='utf-8')
        i_t = html.find(f"'{GEN}': {{")
        tip = html[i_t:html.find('\n  },', i_t)] if i_t >= 0 else ''
        chk('W4 ★ 툴팁 — 새 규칙 (G2RR-01 · 네 세대 값 = 레코드에서 유도한 기대값 · 확인된 역사 도장 스키마 · 불일치 표지) · 옛 문구 '
            '"도장이 세대 2 게시를 말하면 추론하지 않는다" 없음',
            all(w in tip for w in ('G2RR-01', '네 세대 값', '레코드에서 유도', '역사 도장 스키마', '도장 ↔ 레코드 불일치'))
            and '도장이 세대 2 게시를 말하면' not in tip, tip[:300])
        #  ★ 10-07 — 인계 열 사전 (`_TAU_SHARED['ion_net_generation']`) 도 같은 규칙 (G2RR-02 에이전트가 찾은 낡은 문장 · 웹앱 툴팁 W4 와 짝)
        gdoc = getattr(LDD, '_TAU_SHARED', {}).get('ion_net_generation', '')
        chk('W5 ★ 인계 열 사전 ion_net_generation — 새 규칙 (G2RR-01 · 확인된 역사 도장 스키마 · 레코드에서 유도한 기대값) · 옛 문구 '
            '"도장이 세대 2 게시를 말하면 추론하지 않는다" 없음',
            all(w in gdoc for w in ('G2RR-01', '역사 도장 스키마', '레코드에서 유도')) and '도장이 세대 2 게시를 말하면' not in gdoc,
            gdoc[:300])

        print('  (변이마다 멈춘 곳 — 관문 · 첫 사유)')
        for lab, e_ in stop.items():
            gate = e_.split(' — ')[0].split(': ', 2)[-1] if ' — ' in e_ else ''
            why = e_[e_.find('레코드 세대'):] if '레코드 세대' in e_ else e_
            print(f'    {lab:32s} → {gate or "통과"} · {why[:150]}')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        for d in made:
            shutil.rmtree(d, ignore_errors=True)

    print(f'\ntest_gen2_stamp_record: {PASS}/{PASS + FAIL} PASS')
    return 0 if FAIL == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
