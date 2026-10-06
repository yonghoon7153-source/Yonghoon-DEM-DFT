#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""압밀 목표압 도달 기록 (`scripts/lhs_pressure_record.py`) + 인계 생성기 관문 (`lhs_design_dataset.build_handover(pressure=…)` · CLI) — DESC-06 잔여.

  python3 scripts/test_lhs_pressure_record.py      # 종료코드 0 = PASS

반례 먼저 (옛 생성기는 압력 기록을 받는 자리 자체가 없어 아무 침대나 "300 MPa 압밀 뒤" 로 실었다 — 수확 · 배치 · 봉인 grep 0):
  [R] 기록기 — 합성 덱 (thin6 · Heckel 덱과 같은 압밀 루프 꼴) + 합성 LIGGGHTS 로그:
      마지막 판정 줄 current ≥ target = OK · < target = NOT_REACHED · 명령 echo 만 = REFUSED · NaN = REFUSED (NaN 이면 덱의 if 가 루프를 빠져나간다) ·
      Target ≠ 덱 = REFUSED · 판정 줄 있는 로그 둘 = REFUSED · 루프 꼴 없는 덱 = REFUSED · 덱 sha ≠ 수확 = REFUSED · 단위 = 덱 × 1000 MPa
  [G] 생성기 관문 — OK 기록이면 press_* 열 · NOT_REACHED · 없는 케이스 · 덱 sha · 목표 600 · 스키마 · 중복 행 · 상태와 값의 모순 → 거부 (DESC-06)
  [C] CLI — --export-handover 는 --pressure-record 또는 --pressure-unverified (명시 승인) 중 하나를 요구한다 (둘 다 없으면 거부 · 미검사를 조용히 넘기지 않는다)
"""
import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

_ok, _fail = 0, []


def chk(name, cond, extra=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f' — {str(extra)[:300]}' if extra else ''))
    return bool(cond)


DECK = """# 합성 덱 — 압밀 루프 꼴 (dem_scripts/thin6_seed.liggghts · scripts/make_heckel_inputs.py 와 같은 줄)
variable target_press equal {tp}
fix top_mesh all mesh/surface/stress file plate.stl type 1 scale 1.0 reference_point 0 0 0
print "====== PHASE 3: COMPRESSION ======"
fix move_press all move/mesh mesh top_mesh linear 0.0 0.0 -0.01
label loop_press
    run 5000
    variable current_press equal "abs(f_top_mesh[3]) / 0.0025 / 1000000"
    print "Current Pressure: ${{current_press}} MPa (Target: ${{target_press}})"
    if "${{current_press}} < ${{target_press}}" then "jump SELF loop_press"
unfix move_press
print "====== PHASE 4: RELAXATION ======"
run 50000
"""


def _log(values, target='0.3', tail=True, echo=True):
    out = ['LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, compiled 2024-01-01)', 'print "====== PHASE 3: COMPRESSION ======"']
    for v in values:
        if echo:
            out.append('    print "Current Pressure: ${current_press} MPa (Target: ${target_press})"')
        out.append(f'Current Pressure: {v} MPa (Target: {target})')
    if tail:
        out += ['print "====== PHASE 4: RELAXATION ======"', '====== PHASE 4: RELAXATION ======', 'Step Atoms KinEng', '2420000 45030 1e-9']
    return '\n'.join(out) + '\n'


def _w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(text)
    return path


def section_r(td):
    print('[R] 기록기 — 덱 루프 꼴 · 로그 마지막 판정 줄')
    import lhs_pressure_record as PR
    d = _w(os.path.join(td, 'c1', 'input_c1.liggghts'), DECK.format(tp='0.30'))
    lg = _w(os.path.join(td, 'c1', 'log.liggghts'), _log(['0.1', '0.25', '0.3021']))
    r = PR.record('c1', d, [lg], want_deck_sha=PR.sha256_of(d))
    chk('R1 마지막 판정 줄 0.3021 ≥ 목표 0.30 (덱 단위) → OK · reached True · 목표 300 MPa · 마지막 302.1 MPa · 판정 줄 3 · 뒤 줄 있음',
        r['status'] == 'OK' and r['reached'] == 'True' and abs(float(r['target_mpa']) - 300.0) < 1e-9
        and abs(float(r['last_press_mpa']) - 302.1) < 1e-6 and r['n_press_lines'] == '3' and int(r['lines_after_last']) > 0
        and len(r['log_sha256']) == 64 and r['deck_sha256'] == PR.sha256_of(d), r)
    lg2 = _w(os.path.join(td, 'c2', 'log.liggghts'), _log(['0.1', '0.29'], tail=False))
    d2 = _w(os.path.join(td, 'c2', 'input_c2.liggghts'), DECK.format(tp='0.30'))
    r2 = PR.record('c2', d2, [lg2])
    chk('R2 마지막 판정 줄 0.29 < 0.30 (루프 안에서 끝난 로그) → NOT_REACHED · reached False', r2['status'] == 'NOT_REACHED' and r2['reached'] == 'False', r2)
    lg3 = _w(os.path.join(td, 'c3', 'log.liggghts'), 'print "Current Pressure: ${current_press} MPa (Target: ${target_press})"\n' * 3)
    r3 = PR.record('c3', _w(os.path.join(td, 'c3', 'in.liggghts'), DECK.format(tp='0.30')), [lg3])
    chk('R3 명령 echo 만 있는 로그 (print 출력 없음) → REFUSED (판정 줄 없음)', r3['status'] == 'REFUSED' and '판정 줄' in r3['why'], r3)
    lg4 = _w(os.path.join(td, 'c4', 'log.liggghts'), _log(['0.1', 'nan']))
    r4 = PR.record('c4', _w(os.path.join(td, 'c4', 'in.liggghts'), DECK.format(tp='0.30')), [lg4])
    chk('R4 마지막 current NaN → REFUSED (NaN 이면 덱의 if 가 루프를 빠져나간다 — 도달로 치지 않는다)', r4['status'] == 'REFUSED' and 'NaN' in r4['why'], r4)
    lg5 = _w(os.path.join(td, 'c5', 'log.liggghts'), _log(['0.61'], target='0.6'))
    r5 = PR.record('c5', _w(os.path.join(td, 'c5', 'in.liggghts'), DECK.format(tp='0.30')), [lg5])
    chk('R5 로그 Target 0.6 ≠ 덱 target_press 0.30 → REFUSED (다른 덱의 로그)', r5['status'] == 'REFUSED' and 'Target' in r5['why'], r5)
    d6 = _w(os.path.join(td, 'c6', 'in.liggghts'), DECK.format(tp='0.30'))
    a6 = _w(os.path.join(td, 'c6', 'log.liggghts'), _log(['0.31']))
    b6 = _w(os.path.join(td, 'c6', 'log.resume.liggghts'), _log(['0.32']))
    r6 = PR.record('c6', d6, [a6, b6])
    chk('R6 판정 줄 있는 로그 둘 → REFUSED (어느 것이 끝인지 모른다)', r6['status'] == 'REFUSED' and '둘 이상' in r6['why'], r6)
    d7 = _w(os.path.join(td, 'c7', 'in.liggghts'), 'variable target_press equal 0.30\nrun 1000\n')
    r7 = PR.record('c7', d7, [_w(os.path.join(td, 'c7', 'log.liggghts'), _log(['0.31']))])
    chk('R7 압밀 루프 꼴이 없는 덱 → REFUSED (모르는 덱)', r7['status'] == 'REFUSED' and '루프 꼴' in r7['why'], r7)
    r8 = PR.record('c1', d, [lg], want_deck_sha='0' * 64)
    chk('R8 덱 sha ≠ 수확 raw.deck → REFUSED', r8['status'] == 'REFUSED' and '덱 sha' in r8['why'], r8)
    #  CLI — 코호트 TSV · 수확 폴더 (raw.deck.sha256) · 산출 TSV · rc (전부 OK 일 때만 0)
    coh = os.path.join(td, 'cohort.tsv')
    with open(coh, 'w', encoding='utf-8', newline='') as fh:
        fh.write('# 합성 코호트\ncase\tstatus\tdeck\n')
        fh.write(f'c1\tRAW_OK\t{d}\nc2\tRAW_OK\t{d2}\n')
    hd = os.path.join(td, 'harvest')
    os.makedirs(hd, exist_ok=True)
    for c, dk in (('c1', d), ('c2', d2)):
        _w(os.path.join(hd, f'{c}.json'), json.dumps({'case': c, 'raw': {'deck': {'sha256': PR.sha256_of(dk)}}}))
    out = os.path.join(td, 'rec', 'press.tsv')
    rc = PR.main(['--cohort', coh, '--harvest-dir', hd, '--out', out])
    rows = list(csv.DictReader(open(out, encoding='utf-8'), delimiter='\t'))
    chk('R9 CLI — 수확 케이스마다 한 행 (c1 OK · c2 NOT_REACHED) · 스키마 열 · rc 1 (전부 OK 가 아니다)',
        rc == 1 and [(r_['case'], r_['status']) for r_ in rows] == [('c1', 'OK'), ('c2', 'NOT_REACHED')]
        and all(r_['schema'] == PR.SCHEMA for r_ in rows), (rc, rows))
    return d, d2, out


def _harvest(case, deck_sha):
    """build_handover 가 받는 최소 수확 (bimodal · 항등식 정합 · 적격성 없음 = 옛 수확 시험 경로)."""
    return {'case': case, 'timestep': 100, 'plate_z_sim': 0.04, 'phi_se': 0.2, 'phi_am': 0.5, 'porosity_sphere_pct_RECORD_ONLY': 100.0 * (1 - 0.2 - 0.5),
            'n_types': 3, 'phase_counts': {'AM_P': 1, 'AM_S': 3, 'SE': 50},
            'coverage_AM_P_hertz_pct': 10.0, 'coverage_AM_S_hertz_pct': 20.0, 'coverage_AM_total_hertz_pct': 17.5, 'tortuosity_dijkstra_SE': None,
            'status': {'phi': 'OK', 'porosity': 'OK', 'coverage_AM_P': 'OK', 'coverage_AM_S': 'OK', 'coverage_AM_total': 'OK',
                       'tortuosity': 'NOT_PERCOLATING'},
            'tau_detail': {'n_sampled': 0, 'n_valid': 0, 'n_truncated': 0, 'tau_convention': 'harvest_v1/…'},
            'coverage_detail': {'n_capped': 0, 'n_free_surface_invalid': 0, 'counts': {'AM_P': {'n_valid': 1}, 'AM_S': {'n_valid': 3}}},
            'raw': {'atom': {'sha256': 'a' * 64}, 'contact': {'sha256': 'b' * 64}, 'mesh': {'sha256': 'e' * 64}, 'deck': {'sha256': deck_sha}}}


def section_g(td, d, d2):
    print('[G] 생성기 관문 — build_handover(pressure=…)')
    import lhs_design_dataset as L
    import lhs_pressure_record as PR
    hv = {'c1': _harvest('c1', PR.sha256_of(d)), 'c3': _harvest('c3', PR.sha256_of(d2))}
    rows = [{'case_id': 'c1', 'block': 'bimodal'}, {'case_id': 'c3', 'block': 'bimodal'}]
    lg3 = _w(os.path.join(td, 'c3b', 'log.liggghts'), _log(['0.2', '0.3']))
    recs = {'c1': PR.record('c1', d, [os.path.join(td, 'c1', 'log.liggghts')]), 'c3': PR.record('c3', d2, [lg3])}
    tsv = os.path.join(td, 'g', 'press.tsv')

    def _write(rr):
        os.makedirs(os.path.dirname(tsv), exist_ok=True)
        with open(tsv, 'w', encoding='utf-8', newline='') as fh:
            w = csv.DictWriter(fh, PR.COLS, delimiter='\t', lineterminator='\n')
            w.writeheader()
            for r_ in rr:
                w.writerow(r_)
        return tsv

    def _refused(fn, tag='DESC-06'):
        try:
            fn()
        except L.FillRefusal as e:
            return tag in str(e), str(e)[:200]
        except Exception as e:  # noqa: BLE001
            return False, f'{type(e).__name__}: {e}'
        return False, '거부하지 않았다'
    try:
        pv = L.load_pressure_record(_write([recs['c1'], recs['c3']]))
        o, c, rep = L.build_handover(rows, hv, pressure=pv)
        e0 = ''
    except Exception as e:  # noqa: BLE001
        o, c, rep, e0 = [], [], {}, f'{type(e).__name__}: {e}'
    pc = ('press_target_mpa', 'press_last_loop_mpa', 'press_reached', 'press_log_sha256')
    chk('G1 OK 기록 둘 → 통과 · press_* 네 열 (목표 300 · 마지막 판정 줄 · True · 로그 sha) · 보고 pressure_checked 2',
        not e0 and all(x in c for x in pc) and all(r_['press_reached'] == 'True' and abs(float(r_['press_target_mpa']) - 300.0) < 1e-9 for r_ in o)
        and rep.get('pressure_checked') == 2, e0 or (c[-6:], o[:1]))
    try:
        cd = {d_['column']: d_ for d_ in L.column_dictionary(c)} if c else {}
    except Exception as e:  # noqa: BLE001
        cd = {'_': {'meaning': f'{type(e).__name__}: {e}'}}
    m_last = (cd.get('press_last_loop_mpa') or {}).get('meaning', '')
    chk('G2 열 사전 — press_* 출처 pressure_log · 마지막 판정 줄은 최종 프레임 응력이 아니다 (판 고정 뒤 이완) · DESC-06',
        all((cd.get(x) or {}).get('source') == 'pressure_log' for x in pc) and '최종 프레임' in m_last and '이완' in m_last and 'DESC-06' in m_last, m_last[:200])
    nr = PR.record('c3', d2, [os.path.join(td, 'c2', 'log.liggghts')])
    for nm, rr, tag in (('NOT_REACHED 기록', [recs['c1'], nr], 'DESC-06'),
                        ('케이스 없음 (c3 기록 빠짐)', [recs['c1']], 'DESC-06'),
                        ('덱 sha ≠ 수확 raw.deck', [recs['c1'], dict(recs['c3'], deck_sha256='0' * 64)], 'DESC-06'),
                        ('목표 600 MPa (다른 덱)', [recs['c1'], dict(recs['c3'], target_mpa='600.0', target_press_deck='0.6')], 'DESC-06'),
                        ('상태 OK 인데 reached False (모순)', [recs['c1'], dict(recs['c3'], reached='False')], 'DESC-06'),
                        ('reached True 인데 마지막 < 목표 (모순)', [recs['c1'], dict(recs['c3'], last_press_mpa='299.0')], 'DESC-06'),
                        ('로그 sha 없음', [recs['c1'], dict(recs['c3'], log_sha256='')], 'DESC-06')):
        okr, why = _refused(lambda rr=rr: L.build_handover(rows, hv, pressure=L.load_pressure_record(_write(rr))))
        chk(f'G3 ★ {nm} → 거부', okr, why)
    okr, why = _refused(lambda: L.load_pressure_record(_write([recs['c1'], recs['c1'], recs['c3']])))
    chk('G4 ★ 기록 TSV 에 같은 케이스 두 행 → 읽기 거부', okr, why)
    okr, why = _refused(lambda: L.load_pressure_record(_write([dict(recs['c1'], schema='lhs_pressure_record/v0'), recs['c3']])))
    chk('G5 ★ 스키마 다른 기록 → 읽기 거부', okr, why)
    o2, c2_, _ = L.build_handover(rows, hv)
    chk('G6 pressure 없이 부르면 옛 표 그대로 (press_* 열 없음 — 함수 경로 · CLI 는 명시 승인을 요구한다 [C])', not any(x in c2_ for x in pc), c2_[-4:])
    return tsv, hv, rows, recs


def section_c(td, hv, rows, recs):
    print('[C] CLI — --pressure-record · --pressure-unverified')
    import lhs_pressure_record as PR
    cd = os.path.join(td, 'cli')
    os.makedirs(os.path.join(cd, 'harvest'), exist_ok=True)
    for q, h in hv.items():
        _w(os.path.join(cd, 'harvest', f'{q}.json'), json.dumps(h))
    with open(os.path.join(cd, 'design.csv'), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, ['case_id', 'block'], lineterminator='\n')
        w.writeheader()
        w.writerows(rows)
    tsv = os.path.join(cd, 'press.tsv')
    with open(tsv, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, PR.COLS, delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows([recs['c1'], recs['c3']])
    base = [sys.executable, os.path.join(HERE, 'lhs_design_dataset.py'), '--export-handover', os.path.join(cd, 'h.csv'),
            '--design', os.path.join(cd, 'design.csv'), '--harvest', os.path.join(cd, 'harvest'), '--union', '']
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    p0 = subprocess.run(base, capture_output=True, text=True, timeout=300, env=env)
    chk('C1 ★ 둘 다 없으면 거부 (rc ≠ 0 · 안내에 --pressure-record · --pressure-unverified) — 미검사를 조용히 넘기지 않는다',
        p0.returncode != 0 and '--pressure-record' in (p0.stdout + p0.stderr) and '--pressure-unverified' in (p0.stdout + p0.stderr)
        and not os.path.exists(os.path.join(cd, 'h.csv')), (p0.returncode, (p0.stdout + p0.stderr)[-300:]))
    p1 = subprocess.run(base + ['--pressure-unverified'], capture_output=True, text=True, timeout=300, env=env)
    h1 = next(csv.reader(open(os.path.join(cd, 'h.csv'), encoding='utf-8'))) if os.path.exists(os.path.join(cd, 'h.csv')) else []
    chk('C2 --pressure-unverified (명시 승인) → 만든다 · press_* 열 없음 · 출력에 "완료 압력 미검사 (DESC-06)" 경고',
        p1.returncode == 0 and bool(h1) and not any(x.startswith('press_') for x in h1) and '완료 압력 미검사' in p1.stdout, (p1.returncode, p1.stdout[-300:], p1.stderr[-300:]))
    p2 = subprocess.run(base + ['--pressure-record', tsv], capture_output=True, text=True, timeout=300, env=env)
    rows2 = list(csv.DictReader(open(os.path.join(cd, 'h.csv'), encoding='utf-8'))) if os.path.exists(os.path.join(cd, 'h.csv')) else []
    d2 = {r_['column']: r_ for r_ in csv.DictReader(open(os.path.join(cd, 'h_columns.tsv'), encoding='utf-8'), delimiter='\t')} \
        if os.path.exists(os.path.join(cd, 'h_columns.tsv')) else {}
    chk('C3 --pressure-record → press_* 열 · 값 · 열 사전 항목 · 출력에 확인 행 수',
        p2.returncode == 0 and bool(rows2) and all(r_.get('press_reached') == 'True' for r_ in rows2)
        and (d2.get('press_last_loop_mpa') or {}).get('source') == 'pressure_log' and 'DESC-06' in p2.stdout, (p2.returncode, p2.stdout[-300:], p2.stderr[-300:]))
    p3 = subprocess.run(base + ['--pressure-record', tsv, '--pressure-unverified'], capture_output=True, text=True, timeout=300, env=env)
    chk('C4 둘 다 주면 거부 (모순된 지시)', p3.returncode != 0, (p3.returncode, (p3.stdout + p3.stderr)[-200:]))


def main():
    td = tempfile.mkdtemp(prefix='press_rec_')
    try:
        d, d2, _ = section_r(td)
        try:
            tsv, hv, rows, recs = section_g(td, d, d2)
            section_c(td, hv, rows, recs)
        except Exception as e:  # noqa: BLE001
            import traceback
            traceback.print_exc()
            _fail.append(f'[G]/[C] 예외 {type(e).__name__}: {e}')
    finally:
        shutil.rmtree(td, ignore_errors=True)
    print(f'\n{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        for f in _fail:
            print('  -', f)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
