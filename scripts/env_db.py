#!/usr/bin/env python3
"""환경 DB 조회 + 머신 진단 (config/env_db.json 이 정본).

임시 GPU 인스턴스를 껐다 켤 때마다 "뭐가 빠졌나"를 사람이 기억하지 않게 — DB 가 요구하는
패키지·앵커·env 를 실제로 import/검사해서 **빠진 것과 그 고침 명령**을 그대로 뱉는다.

  python3 scripts/env_db.py --doctor            # 현재 머신 진단 (핵심) — 종료코드 0=정상, 1=결함
  python3 scripts/env_db.py --machine v100      # 그 머신의 셋업/실행/회수 명령
  python3 scripts/env_db.py --pitfalls          # 증상→원인→고침 표
  python3 scripts/env_db.py --env               # STEP4 솔버 노브 (기본값·의미·현재값)
  python3 scripts/env_db.py --json              # DB 원본
  python3 scripts/env_db.py --selftest          # DB 스키마 자기검증
"""
from __future__ import annotations
import argparse
import importlib
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, 'config', 'env_db.json')
OK, NO, WARN = '✓', '✗', '⚠'


def load_db(path=DB_PATH):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def _pip_name(entry):
    return entry['pip']


def _check_import(mod):
    """import 성공 여부 + 실패 사유 (버전은 있으면)."""
    if not mod:
        return None, ''                                   # import 대상 없음(라이브러리 파일만 제공)
    try:
        m = importlib.import_module(mod)
        return True, str(getattr(m, '__version__', '') or '')
    except Exception as e:
        return False, f'{type(e).__name__}: {e}'


def doctor(db, want_gpu=True):
    """현재 인터프리터/머신을 DB 요구사항에 대조.  (결함 리스트, 고침 명령 리스트) 반환."""
    bad, fixes = [], []
    print(f'== env doctor ==  python {sys.version.split()[0]} @ {sys.executable}')
    pv = sys.version_info[:2]
    if pv >= (3, 13):
        print(f'  {WARN} python {pv[0]}.{pv[1]} — taichi wheel 없음(1.7.4≤3.12 / 1.6.0≤3.11).'
              ' 구 glibc 서버면 conda python=3.11 필요')

    groups = ['core', 'mpm', 'step4'] + (['gpu'] if want_gpu else [])
    for g in groups:
        print(f'\n-- {g} --')
        miss = []
        for e in db['packages'][g]:
            mod = e.get('import')
            got, info = _check_import(mod)
            if got is None:                                # import 없는 라이브러리 패키지 → pip 목록으로만 확인
                print(f'  ·  {_pip_name(e):28s} (import 대상 없음 — {e["why"][:40]})')
                continue
            if got:
                print(f'  {OK}  {_pip_name(e):28s} {info}')
            else:
                print(f'  {NO}  {_pip_name(e):28s} {info[:90]}')
                miss.append(e)
                fb = e.get('fallback')
                if fb:
                    print(f'      ↳ fallback 후보: {fb}  ({e.get("note", "")[:70]})')
        if miss:
            bad += [f'{g}:{_pip_name(e)}' for e in miss]
            # gpu 그룹은 라이브러리 패키지도 함께 깔아야 import 가 뚫린다
            names = [_pip_name(e) for e in miss]
            if g == 'gpu':
                names = [_pip_name(e) for e in db['packages']['gpu']]
            fixes.append('python -m pip install ' + ' '.join(f'"{n}"' for n in names))

    print('\n-- 선택(있으면 좋음) --')
    for e in db['packages']['optional']:
        got, info = _check_import(e.get('import'))
        print(f'  {OK if got else WARN}  {_pip_name(e):28s} '
              f'{info[:60] if got else "미설치 — " + e["why"][:50]}')

    print('\n-- GPU --')
    try:
        import taichi as ti                                # noqa: F401
        try:
            ti.init(arch=ti.cuda, log_level='error')
            print(f'  {OK}  taichi CUDA (MPM GPU)')
        except Exception as e:
            print(f'  {WARN}  taichi 있으나 CUDA init 실패 ({type(e).__name__}) → --arch cpu 만 가능')
    except Exception as e:
        print(f'  {NO}  taichi import 실패 — {type(e).__name__}: {str(e)[:80]}')
    if want_gpu:
        try:                                               # 실제 코드 경로(sparse CG)로 검증 — import 만으론 부족
            import cupy as cp
            import cupyx.scipy.sparse as sp
            from cupyx.scipy.sparse.linalg import cg
            n = 512
            A = sp.csr_matrix(sp.diags([cp.full(n, 2.0), cp.full(n - 1, -1.0), cp.full(n - 1, -1.0)],
                                       [0, 1, -1]))
            b = cp.ones(n)
            try:
                x, _i = cg(A, b, rtol=1e-8, maxiter=2000)
            except TypeError:
                x, _i = cg(A, b, tol=1e-8, maxiter=2000)
            r = float(cp.linalg.norm(A @ x - b))
            print(f'  {OK}  cupy GPU sparse CG (STEP3/4 경로) resid {r:.1e}')
        except Exception as e:
            print(f'  {NO}  cupy GPU sparse CG 실패 — {type(e).__name__}: {str(e)[:80]}')
            bad.append('gpu:sparse_cg')
            fixes.append('python -m pip install "cupy-cuda12x[ctk]" '
                         + ' '.join(f'"{_pip_name(e)}"' for e in db['packages']['gpu'][1:]))

    print('\n-- 앵커 (없으면 STEP4 통째 SKIP) --')
    for rel, meta in db['anchors'].items():
        p = os.path.join(ROOT, rel)
        if os.path.isfile(p):
            print(f'  {OK}  {rel}')
        else:
            print(f'  {NO}  {rel} — {meta["why"][:60]}')
            bad.append(f'anchor:{rel}')
            if meta.get('generate', '').startswith('python3'):
                fixes.append(meta['generate'])

    print('\n-- repo --')
    try:
        br = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=ROOT,
                            capture_output=True, text=True, timeout=10).stdout.strip()
        want = db['_meta']['branch']
        print(f'  {OK if br == want else WARN}  branch {br or "?"}' + ('' if br == want else f'  (정본 {want})'))
        if br != want:
            fixes.append(f'git fetch origin {want} && git checkout -B {want} origin/{want}')
    except Exception as e:
        print(f'  {WARN}  git 확인 불가 ({type(e).__name__})')

    print('\n-- STEP4 솔버 env (현재 셸) --')
    for k, v in db['solver_env'].items():
        if k.startswith('_'):
            continue
        cur = os.environ.get(k)
        d = v.get('default', '')
        mark = ' ←설정됨' if cur is not None else ''
        print(f'  {k:24s} = {cur if cur is not None else d}{mark}   {v["meaning"][:52]}')
        if k == 'MPM_S4_CONTRAST_CAP' and cur not in (None, '', '0'):
            print(f'      {WARN} cap 런 = σ-메트릭 보고 금지 ({v.get("cost", "")})')

    print('\n' + '=' * 62)
    if bad:
        print(f'{NO} 결함 {len(bad)}건: ' + ', '.join(bad))
        print('\n고침 (순서대로):')
        seen = set()
        for f in fixes:
            if f not in seen:
                seen.add(f)
                print('  ' + f)
        print(f'\n또는 한 방에: {db["recipes"]["setup"]}')
    else:
        print(f'{OK} 전부 정상 — 바로 실행 가능:  {db["recipes"]["run_full"]}')
    return bad


def show_machine(db, name):
    m = db['machines'].get(name)
    if not m:
        raise SystemExit(f'모르는 머신: {name} (있는 것: {", ".join(db["machines"])})')
    print(f'== {name} == {m["role"]}')
    for k in ('ssh_alias', 'workdir', 'python', 'venv', 'gpu', 'downloads'):
        if m.get(k):
            print(f'  {k:10s} {m[k]}')
    print('  주의:')
    for q in m.get('quirks', []):
        print(f'    - {q}')
    print('\n  명령:')
    for k in ('setup', 'activate', 'doctor', 'run_full', 'run_step4_only', 'run_step4_capped',
              'fetch', 'fetch_step4', 'kill_stuck'):
        if db['recipes'].get(k):
            print(f'    {k:18s} {db["recipes"][k]}')


def show_pitfalls(db):
    print('== 증상 → 원인 → 고침 ==')
    for p in db['pitfalls']:
        print(f'\n  ▸ {p["symptom"]}')
        print(f'     원인: {p["cause"]}')
        print(f'     고침: {p["fix"]}')


def show_env(db):
    print('== STEP4 솔버 노브 ==')
    print('  ' + db['solver_env']['_doc'])
    for k, v in db['solver_env'].items():
        if k.startswith('_'):
            continue
        cur = os.environ.get(k)
        print(f'\n  {k}  (기본 {v.get("default", "")}{"" if cur is None else f" · 현재 {cur}"})')
        print(f'     {v["meaning"]}')
        if v.get('solution_invariant') is True:
            print('     해-불변 (수렴 속도만 바꿈)')
        if v.get('cost'):
            print(f'     대가: {v["cost"]}')
        for kk in ('on_when', 'off_when'):
            if v.get(kk):
                print(f'     {kk}: {v[kk]}')


def _selftest(db):
    """DB 스키마 자기검증 — 필드 누락/오타를 CI 없이 잡는다."""
    ok = True
    for g, items in db['packages'].items():
        for e in items:
            if 'pip' not in e or 'why' not in e or 'import' not in e:
                print(f'  {NO} packages.{g}: pip/import/why 필수 — {e}'); ok = False
    for name, m in db['machines'].items():
        if 'role' not in m or 'workdir' not in m:
            print(f'  {NO} machines.{name}: role/workdir 필수'); ok = False
    for k, v in db['solver_env'].items():
        if k.startswith('_'):
            continue
        if 'meaning' not in v:
            print(f'  {NO} solver_env.{k}: meaning 필수'); ok = False
    for p in db['pitfalls']:
        if not {'symptom', 'cause', 'fix'} <= set(p):
            print(f'  {NO} pitfalls: symptom/cause/fix 필수 — {p}'); ok = False
    need_recipes = {'setup', 'activate', 'doctor', 'run_full', 'kill_stuck'}
    miss = need_recipes - set(db['recipes'])
    if miss:
        print(f'  {NO} recipes 누락: {miss}'); ok = False
    # 코드↔DB 정합: solver_env 키가 step4_dyn 에 실제로 존재하는지
    s4 = os.path.join(ROOT, 'scripts', 'step4_dyn.py')
    if os.path.isfile(s4):
        src = open(s4, encoding='utf-8').read()
        for k in db['solver_env']:
            if k.startswith('_') or k in ('MPM_S4_RINT', 'MPM_S4_DS', 'MPM_NO_PULL'):
                continue                                   # 킷/러너 쪽 env — step4_dyn 소스엔 없음
            if k not in src:
                print(f'  {NO} solver_env.{k} 가 step4_dyn.py 에 없음 (DB 낡음)'); ok = False
    # 앵커 생성 명령이 실제 스크립트를 가리키는지
    for rel, meta in db['anchors'].items():
        g = meta.get('generate', '')
        if g.startswith('python3 '):
            tgt = g.split()[1]
            if not os.path.isfile(os.path.join(ROOT, tgt)):
                print(f'  {NO} anchors.{rel}: {tgt} 없음'); ok = False
    print(f'{OK} env_db selftest PASS' if ok else f'{NO} env_db selftest FAIL')
    return ok


def main():
    ap = argparse.ArgumentParser(description='환경 DB 조회 + 머신 진단 (config/env_db.json 정본)')
    ap.add_argument('--doctor', action='store_true', help='현재 머신 진단 + 고침 명령')
    ap.add_argument('--no-gpu', action='store_true', help='doctor 에서 GPU 항목 생략 (CPU 전용 머신)')
    ap.add_argument('--machine', metavar='NAME', help='머신 프로필 + 명령 (v100/kgy/wsl)')
    ap.add_argument('--pitfalls', action='store_true', help='증상→원인→고침')
    ap.add_argument('--env', action='store_true', help='STEP4 솔버 노브')
    ap.add_argument('--json', action='store_true', help='DB 원본 출력')
    ap.add_argument('--selftest', action='store_true', help='DB 스키마 자기검증')
    a = ap.parse_args()
    db = load_db()
    if a.json:
        print(json.dumps(db, ensure_ascii=False, indent=1)); return
    if a.selftest:
        sys.exit(0 if _selftest(db) else 1)
    if a.machine:
        show_machine(db, a.machine); return
    if a.pitfalls:
        show_pitfalls(db); return
    if a.env:
        show_env(db); return
    if a.doctor:
        sys.exit(1 if doctor(db, want_gpu=not a.no_gpu) else 0)
    ap.print_help()


if __name__ == '__main__':
    main()
