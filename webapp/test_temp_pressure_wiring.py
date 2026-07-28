#!/usr/bin/env python3
"""webapp 운전조건(온도 · 구동 스택압) 배선 selftest — docs/temp_pressure_capability.md 배선분.

  python3 webapp/test_temp_pressure_wiring.py      # 종료코드 0 = PASS

검사 항목
  [1] ★기본값 불변 — &tempc=/&eaion=/&pop= 를 안 주면(또는 빈 값으로 주면) 킷 zip 의 **모든 멤버가
      생성기 CLI 를 직접 돌린 것과 바이트 동일**하고, run_mpm.sh 어디에도 --temp-c 가 없다.
  [2] 온도 주입 — 값을 주면 run_mpm.sh 의 STEP3(payload) 호출에 --temp-c/--ea-ion-ev 가 붙고,
      mpm_input.json 에 se_material.provenance 규약(σ·T Kraft2017, T_ref 25 °C)이 남는다.
  [3] 구동압 — &pop= 이 생성기 --op-pressure-mpa 로 흘러 2단(save-state → load-state) A-1 앵커 +
      a1_pressure_provenance 가 나온다.
  [4] 입력 검증 — 비수치/범위밖/온도 없는 Eₐ 는 조용히 무시하지 않고 400.
  [5] ★파일명 미러 — 클라이언트 _addTag()(single.html, node 로 실행)와 서버 download_name 이
      **정확히** 일치한다 (VGCFPTFESDCP·_ppds 사건 재발 방지; node 없으면 SKIP).
  [6] 예측기 라우트가 sigma_e_t_model / ea_ion_ev 를 그대로 전달한다 (미지정 = 엔진 기본).
"""
import csv
import hashlib
import io
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SINGLE_HTML = os.path.join(HERE, 'templates', 'single.html')
GEN = os.path.join(ROOT, 'scripts', 'mpm_input_from_case.py')

_FAILS = []


def chk(name, cond, extra=''):
    print(f"  {'PASS' if cond else 'FAIL'}  {name}{(' — ' + extra) if extra else ''}")
    if not cond:
        _FAILS.append(name)
    return bool(cond)


# ── synthetic case (no DEM run needed) ────────────────────────────────────────
def make_case(root):
    d = os.path.join(root, 'results', 'tcase')
    os.makedirs(d, exist_ok=True)
    random.seed(7)
    rows = [('id', 'type', 'x', 'y', 'z', 'radius')]
    i = 0
    for t, r, n in ((1, 0.003, 12), (2, 0.001, 25), (3, 0.0005, 300)):
        for _ in range(n):
            i += 1
            rows.append((i, t, round(random.uniform(0.002, 0.048), 6),
                         round(random.uniform(0.002, 0.048), 6),
                         round(random.uniform(0.002, 0.030), 6), r))
    with open(os.path.join(d, 'atoms.csv'), 'w', newline='') as f:
        csv.writer(f).writerows(rows)
    json.dump({'porosity_pct': 15.6, 'thickness_um': 30.2},
              open(os.path.join(d, 'full_metrics.json'), 'w'))
    json.dump({'target_pressure_MPa': 300.0}, open(os.path.join(d, 'input_params.json'), 'w'))
    return d


def members(resp):
    """zip 컨테이너 바이트가 아니라 **멤버 내용**을 해시 (zip 헤더는 mtime 을 담아 매번 다름)."""
    z = zipfile.ZipFile(io.BytesIO(resp.data))
    return {n: hashlib.sha256(z.read(n)).hexdigest() for n in sorted(z.namelist())}


def member_text(resp, name):
    return zipfile.ZipFile(io.BytesIO(resp.data)).read(name).decode()


def fname(resp):
    m = re.search(r'filename=([^;]+)', resp.headers.get('Content-Disposition', '') or '')
    return (m.group(1).strip() if m else '')


# ── [5] 클라이언트 태그 미러: single.html 의 JS 함수를 node 로 실행 ──────────────────
def js_fn(src, name):
    """`function NAME(` 부터 중괄호 균형이 맞는 곳까지 잘라낸다 (jinja 없는 순수 JS 함수만)."""
    i = src.index(f'function {name}(')
    depth, j, started = 0, i, False
    while j < len(src):
        if src[j] == '{':
            depth += 1
            started = True
        elif src[j] == '}':
            depth -= 1
            if started and depth == 0:
                return src[i:j + 1]
        j += 1
    raise AssertionError(f'function {name} not closed')


def client_tags(cfgs):
    """node 로 _addTag() 를 실행해 각 설정의 예측 파일명 태그를 얻는다.  node 없으면 None."""
    if not shutil.which('node'):
        return None
    src = open(SINGLE_HTML, encoding='utf-8').read()
    fns = '\n'.join(js_fn(src, n) for n in ('_g', '_numOrEmpty', '_addVals', '_tpTag', '_addTag'))
    script = (
        'const CFG_LIST = ' + json.dumps(cfgs) + ';\n'
        'let CFG = {};\n'
        'const document = { getElementById: id => (CFG[id] !== undefined ? CFG[id] '
        ': { value: "", checked: false }) };\n'
        'function updateAdditiveGpuCmds() {}\n'   # _setTemp/_setPop 미사용이지만 참조 안전
        + fns +
        '\nconst out = CFG_LIST.map(c => { CFG = {}; for (const k in c) CFG[k] = c[k]; '
        'return _addTag(); });\nconsole.log(JSON.stringify(out));\n')
    with tempfile.NamedTemporaryFile('w', suffix='.mjs', delete=False) as f:
        f.write(script)
        p = f.name
    try:
        r = subprocess.run(['node', p], capture_output=True, text=True, timeout=60)
        if r.returncode != 0:
            print('    node stderr:', (r.stderr or '')[-400:])
            return None
        return json.loads(r.stdout.strip().splitlines()[-1])
    finally:
        os.unlink(p)


def dom(vg=0, sp=0, pt=0, sd=0, mix='thinky', vox='0.4', s4=(), s4chg=(), cap='', pp=False,
        tempc='', eaion='', pop=''):
    """dlAdditiveZip 이 읽는 DOM 상태 (id → {value|checked})."""
    d = {'add-vgcf': {'value': str(vg)}, 'add-superp': {'value': str(sp)},
         'add-ptfe': {'value': str(pt)}, 'add-sdcp': {'value': str(sd)},
         'add-mixing': {'value': mix}, 'add-vox': {'value': vox},
         's4-cap': {'value': cap}, 's4-pp': {'checked': pp},
         'kit-tempc': {'value': str(tempc)}, 'kit-eaion': {'value': str(eaion)},
         'kit-pop': {'value': str(pop)}}
    for rate, i in (('0.1', '01'), ('0.2', '02'), ('0.5', '05'), ('1', '1'), ('2', '2'), ('3', '3')):
        d['s4-' + i] = {'checked': rate in s4}
        d['s4g-' + i] = {'checked': rate in s4chg}
    return d


def query_of(c):
    """dlAdditiveZip 의 URL 조립 미러 (서버에 같은 조건을 그대로 보낸다)."""
    g = lambda k, dv='': (c.get(k, {}) or {}).get('value', dv)
    s4 = ','.join(r for r, i in (('0.1', '01'), ('0.2', '02'), ('0.5', '05'),
                                 ('1', '1'), ('2', '2'), ('3', '3'))
                  if (c.get('s4-' + i, {}) or {}).get('checked'))
    s4g = ','.join(r for r, i in (('0.1', '01'), ('0.2', '02'), ('0.5', '05'),
                                  ('1', '1'), ('2', '2'), ('3', '3'))
                   if (c.get('s4g-' + i, {}) or {}).get('checked'))
    q = (f"?vgcf={g('add-vgcf', '0')}&superp={g('add-superp', '0')}&ptfe={g('add-ptfe', '0')}"
         f"&sdcp={g('add-sdcp', '0')}&mixing={g('add-mixing', 'thinky')}&collector=ideal"
         f"&vox={g('add-vox', '0.4')}&step4={s4}&step4chg={s4g}")
    if s4 or s4g:
        q += '&s4vmin=3.0&s4vmax=4.5&s4icut=0.05'
    if g('s4-cap'):
        q += '&s4cap=' + g('s4-cap')
    if (c.get('s4-pp', {}) or {}).get('checked'):
        q += '&s4pp=1'
    if g('kit-tempc'):
        q += '&tempc=' + g('kit-tempc') + ('&eaion=' + g('kit-eaion') if g('kit-eaion') else '')
    if g('kit-pop'):
        q += '&pop=' + g('kit-pop')
    return q


def main():
    tmp = tempfile.mkdtemp(prefix='tp_wiring_')
    try:
        case_dir = make_case(tmp)
        for k, v in (('WEBAPP_RESULTS_FOLDER', 'results'), ('WEBAPP_UPLOAD_FOLDER', 'uploads'),
                     ('WEBAPP_ARCHIVE_FOLDER', 'archive'), ('WEBAPP_MPM_LAB_FOLDER', 'mpm_lab')):
            os.environ[k] = os.path.join(tmp, v)
        sys.path.insert(0, HERE)
        sys.path.insert(0, os.path.join(ROOT, 'scripts'))
        import app as A
        import se_material
        c = A.app.test_client()
        base = '/results/tcase/mpm-input'

        print('[1] 기본값 불변 (미지정 = 현행, 바이트 동일)')
        r0 = c.get(base)
        chk('plain 200 zip', r0.status_code == 200, str(r0.status_code))
        m0 = members(r0)
        r_empty = c.get(base + '?tempc=&eaion=&pop=')
        chk('빈 값 파라미터 = plain 과 멤버 바이트 동일', members(r_empty) == m0)
        chk('빈 값 파라미터 = plain 과 파일명 동일', fname(r_empty) == fname(r0), fname(r_empty))
        # 생성기 CLI 를 직접 돌린 것과도 동일해야 한다 (webapp 이 아무것도 덧붙이지 않음)
        raw = os.path.join(tmp, 'rawkit')
        subprocess.run([sys.executable, GEN, '--results', case_dir, '--case', 'tcase',
                        '--out', raw, '--step3-vox', '0.4'], check=True, cwd=ROOT,
                       capture_output=True, text=True)
        raw_h = {n: hashlib.sha256(open(os.path.join(raw, n), 'rb').read()).hexdigest()
                 for n in sorted(os.listdir(raw))}
        chk('킷 내용 == 생성기 CLI 직접 실행 (webapp 무개입)', raw_h == m0,
            f'{sorted(raw_h) != sorted(m0) and "member set differs" or "content differs"}'
            if raw_h != m0 else '')
        chk('기본 킷에 --temp-c 없음', '--temp-c' not in member_text(r0, 'run_mpm.sh'))
        chk('기본 킷 mpm_input.json 에 temperature_provenance 없음',
            'temperature_provenance' not in json.loads(member_text(r0, 'mpm_input.json')))

        print('[2] 온도 주입 (&tempc= / &eaion=)')
        rt = c.get(base + '?tempc=45&eaion=0.29')
        chk('200', rt.status_code == 200, str(rt.status_code))
        sh = member_text(rt, 'run_mpm.sh')
        chk('run_mpm.sh STEP3 호출에 --temp-c 45 --ea-ion-ev 0.29',
            'python3 "$SCR/mpm_webapp_payload.py" --temp-c 45 --ea-ion-ev 0.29 \\' in sh)
        chk('run_mpm.sh 에 --temp-c 는 1회만 (중복주입 없음)', sh.count('--temp-c') == 1)
        # ★ 이 단언은 유지된다 (2026-07-29 재확인) — --temp-k 는 Kinetics.T = BV 지수의 f=F/(RT)
        #   를 바꾸는데 i0 는 앵커가 없어 25 °C 그대로라, T 를 올리면 η_ct 가 **커진다**.  실제
        #   R_ct 는 30→60 °C 에 4.28× 감소한다 → 정확히 반대(§3-3①).
        _tk = re.compile(r'--temp-k\s+[0-9]')     # 설명 문구가 아니라 **값이 붙은 실제 인자**만
        chk('STEP4 --temp-k 는 굽지 않는다 (부호역전 방지, §3-3①)', not _tk.search(sh))
        # ★ 그러나 온도 그리드를 만든 킷은 STEP4 가 T1-d 가드(GRID_T_MISMATCH)에 걸려 죽었다.
        #   kinetics 는 25 °C 로 두되 그 불일치를 **명시 승인**해야 실행된다 → MIXED_TEMPERATURE.
        #   (STEP4 호출이 실제로 있는 킷으로 확인 — 위 rt 는 rate 미선택이라 STEP4 블록이 없다)
        rt_s4 = c.get(base + '?step4=0.2&s4vmin=3.0&s4vmax=4.5&s4icut=0.05&tempc=45')
        sh4 = member_text(rt_s4, 'run_mpm.sh')
        _n_call = sh4.count('python3 "$SCR/step4_dyn.py" --grid step4_grid.npz')
        chk('STEP4 에 --allow-grid-t-mismatch 주입 (T1-d 가드 통과 + 혼합상태 명시)',
            _n_call >= 1 and sh4.count('--allow-grid-t-mismatch') == _n_call,
            f'STEP4 호출 {_n_call}개 / 플래그 {sh4.count("--allow-grid-t-mismatch")}개')
        chk('STEP4 에도 --temp-k 인자는 여전히 없다 (부호역전 방지)', not _tk.search(sh4))
        chk('다만 왜 안 넣었는지는 킷에 적혀 있다 (미래의 나를 위한 근거)',
            '부호역전' in sh4 and '§3-3' in sh4)
        chk('그 사실이 로그 배너에 적힌다', 'MIXED_TEMPERATURE' in sh4)
        chk('온도 미지정 킷에는 이 플래그가 안 붙는다 (기본 불변)',
            '--allow-grid-t-mismatch' not in member_text(
                c.get(base + '?step4=0.2&s4vmin=3.0&s4vmax=4.5&s4icut=0.05'), 'run_mpm.sh'))
        tp = json.loads(member_text(rt, 'mpm_input.json'))['temperature_provenance']
        ref = se_material.provenance(45.0, 0.29)
        chk('provenance = se_material 규약 (T_C/T_ref/Ea/factor/convention)',
            all(tp[k] == ref[k] for k in ('T_C', 'T_ref_C', 'Ea_ion_eV', 'T_dependence',
                                          'sigma_ion_T_factor', 'convention')),
            f"factor={tp['sigma_ion_T_factor']:.4f}")
        chk('provenance 가 "무엇이 미반영인지" 명시', 'STEP4 kinetics' in tp['not_applied_to'])
        rt2 = c.get(base + '?tempc=45')
        chk('Eₐ 미지정 = 엔진 기본 0.41 (--ea-ion-ev 미주입)',
            '--temp-c 45 \\' in member_text(rt2, 'run_mpm.sh')
            and json.loads(member_text(rt2, 'mpm_input.json'))
                    ['temperature_provenance']['Ea_ion_eV'] == se_material.EA_ION_EV_DEFAULT)

        print('[2b] venv 자동탐지 (V100 ModuleNotFoundError 재발 방지)')
        #   실사고: run_mpm.sh 로는 되는데 같은 명령을 새 SSH 셸에서 직접 치면 numpy 가 없다.
        #   레포 안 venv 를 새 세션이 자동으로 타지 않기 때문 → 스크립트가 스스로 찾게 한다.
        rv = c.get(base + '?step4=0.2&s4vmin=3.0&s4vmax=4.5&s4icut=0.05')
        _zn = zipfile.ZipFile(io.BytesIO(rv.data)).namelist()
        for _nm in ('run_mpm.sh', 'step4_only.sh', 'run_a1_anchors.sh'):
            if _nm not in _zn:
                continue
            _t = member_text(rv, _nm)
            chk(f'{_nm}: venv 자동탐지 + numpy 확인',
                'bin/activate' in _t and 'import numpy' in _t and 'MPM_NO_VENV' in _t)
            chk(f'{_nm}: venv 탐지가 SCR 확정 뒤에 온다 (경로 의존)',
                _t.index('SCR=""') < _t.index('bin/activate'))

        print('[3] 구동 스택압 (&pop=)')
        rp = c.get(base + '?pop=90')
        chk('200', rp.status_code == 200, str(rp.status_code))
        a1 = member_text(rp, 'run_a1_anchors.sh')
        chk('A-1 앵커가 2단(save-state → load-state)', '--save-state' in a1 and '--load-state' in a1)
        chk('servo/hold 두 팔 브래킷', 'servo' in a1 and 'hold' in a1)
        pv = json.loads(member_text(rp, 'mpm_input.json'))['a1_pressure_provenance']
        chk('a1_pressure_provenance P_fab/P_operating 분리',
            pv['P_operating_MPa'] == 90.0 and pv['P_fab_MPa'] == 300.0, json.dumps(pv))
        chk('본 압밀(run_mpm.sh)은 제작압 그대로', '--target-gpa 0.3' in member_text(rp, 'run_mpm.sh'))
        # ★ 2026-07-29: zip 이름에 _op90MPa 가 붙는데 run_mpm.sh 는 제작압 형상만 낸다 →
        #   그 스코프를 실행 중 화면에 명시한다 (§3-3③ㄱ '축 혼동').
        _shp = member_text(rp, 'run_mpm.sh')
        chk('run_mpm.sh 가 구동압 스코프를 명시한다 (제작압 형상임을 화면에 적음)',
            '구동압 스코프' in _shp and 'run_a1_anchors.sh' in _shp and '§3-3' in _shp)
        chk('구동압 미지정이면 그 배너가 없다 (기본 불변)',
            '구동압 스코프' not in member_text(c.get(base), 'run_mpm.sh'))

        print('[4] 입력 검증 (침묵 무시 금지)')
        for q, why in (('?tempc=abc', '비수치 온도'), ('?tempc=900', '범위밖 온도'),
                       ('?eaion=0.29', '온도 없는 Eₐ'), ('?pop=-5', '음수 구동압'),
                       ('?pop=abc', '비수치 구동압'), ('?eaion=9&tempc=45', '범위밖 Eₐ')):
            rr = c.get(base + q)
            chk(f'400 — {why}', rr.status_code == 400, f'{rr.status_code} {rr.data[:90]}')

        print('[5] 파일명 미러 (클라이언트 _addTag ↔ 서버 download_name)')
        cfgs = [
            dom(),
            dom(vg=2, pt=1),
            dom(vg=2, pt=1, tempc=45),
            dom(vg=2, pt=1, tempc=45, eaion='0.29', pop=90),
            dom(tempc=60),
            dom(pop=90),
            dom(tempc=45.5, pop=90.5),
            dom(sd=1.5, pt=0.5, mix='handmix', vox='0.25', s4=('0.5', '1'), s4chg=('1',),
                cap='200', pp=True, tempc=60, eaion='0.46', pop=90),
            dom(sd=1.5, vox='0.25', pp=True, tempc=30),      # s4 없음 → _cap/_ppds 게이트 확인
        ]
        tags = client_tags(cfgs)
        if tags is None:
            print('  SKIP  node 미설치 — 클라이언트 태그 미러 검사를 건너뜀')
        else:
            for cfg, tag in zip(cfgs, tags):
                rr = c.get(base + query_of(cfg))
                want = f'mpm_input_tcase{tag}.zip'
                chk(f'미러 {want}', rr.status_code == 200 and fname(rr) == want,
                    f'server={fname(rr)} client={want}')

        print('[6] 예측기 라우트 pass-through')
        seen = {}
        orig = A.predictor_engine.predict
        A.predictor_engine.predict = lambda **kw: (seen.update(kw) or {'ok': True})
        try:
            c.post('/predictor/predict', json={'d_se': 1, 'd_am': 5, 'am_pct': 80})
            chk('기본 sigma_e_t_model="none" (σ_e T-무관 = 솔버 정합)',
                seen.get('sigma_e_t_model') == 'none', repr(seen.get('sigma_e_t_model')))
            chk('기본 ea_ion_ev=None (엔진 기본 0.41)', seen.get('ea_ion_ev') is None)
            seen.clear()
            c.post('/predictor/predict', json={'d_se': 1, 'ea_ion_ev': 0.46,
                                               'sigma_e_t_model': 'legacy_arrhenius'})
            chk('명시값 전달', seen.get('ea_ion_ev') == 0.46
                and seen.get('sigma_e_t_model') == 'legacy_arrhenius', json.dumps(
                    {k: seen.get(k) for k in ('ea_ion_ev', 'sigma_e_t_model')}))
        finally:
            A.predictor_engine.predict = orig

        print('[7] 업로드 결과에 온도 provenance 승계 (배지 입력)')
        payload = {'kind': 'mpm', 'particles': [], 'mpm_metrics': {'porosity_mpm_pct': 15.9},
                   'temperature_provenance': se_material.provenance(60.0, 0.46)}
        rr = c.post('/results/tcase/mpm-upload', data={
            'payload': (io.BytesIO(json.dumps(payload).encode()), 'mpm_payload.json')},
            content_type='multipart/form-data')
        chk('업로드 200 JSON', rr.status_code == 200 and rr.get_json().get('ok') is True,
            str(rr.status_code))
        side = json.load(open(os.path.join(tmp, 'results', 'tcase', 'mpm_metrics.json')))
        chk('사이드카에 temperature_provenance 승계',
            (side.get('temperature_provenance') or {}).get('T_C') == 60.0)

        print('[8] single.html 렌더 + 인라인 JS 문법')
        from jinja2 import ChainableUndefined
        _old_undef = A.app.jinja_env.undefined
        A.app.jinja_env.undefined = ChainableUndefined
        try:
            with A.app.app_context(), A.app.test_request_context('/'):
                html = A.render_template('single.html', case={'id': 'tcase', 'name': 'tcase'},
                                         figures=[], mpm_metrics={}, archive_path=None,
                                         metrics={}, active='')
        finally:
            A.app.jinja_env.undefined = _old_undef
        chk('템플릿 렌더 + 새 UI 요소 존재',
            all(t in html for t in ('kit-tempc', 'kit-eaion', 'kit-pop',
                                    'kit-op-warn', 'mpm-prov-badge')))
        if not shutil.which('node'):
            print('  SKIP  node 미설치 — 인라인 JS 문법 검사를 건너뜀')
        else:
            bad = 0
            for attrs, body in re.findall(r'<script([^>]*)>(.*?)</script>', html, re.S):
                if 'src=' in attrs or 'importmap' in attrs or 'application/json' in attrs:
                    continue                                  # JSON importmap 등은 JS 가 아님
                with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as f:
                    f.write(body)
                    p = f.name
                rc = subprocess.run(['node', '--check', p], capture_output=True, text=True)
                if rc.returncode:
                    bad += 1
                    print('    ', (rc.stderr or '')[:300])
                os.unlink(p)
            chk('인라인 JS 파싱 (node --check)', bad == 0, f'{bad} block(s) failed')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print()
    if _FAILS:
        print(f'FAIL — {len(_FAILS)}건: ' + ', '.join(_FAILS))
        return 1
    print('ALL PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
