#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사전 리뷰 탐침 — ibb 문법 fixture 실행 2 반입 (§7) 의 숫자 · 재판독 · 사전 점검 모의 (리포에 쓰지 않는다 · 묶음 안 아무것도 실행하지 않는다).

python3 -I -B probe_run2.py <리포 작업 트리> <키트 폴더 (판독기 · ul_reader 가 있는 곳)> <출력 폴더>
① 받은 묶음 sha256 = README · SHA256SUMS.received  ② tar 멤버 (절대 경로 · .. · 링크 · 장치 = 0)  ③ 풀어서 run_manifest · 판정 JSON · 단계 rc · 덱 사본 sha256 ·
   kit SHA256SUMS (= sums_sha256 · 판독기 · 표 줄)  ④ 우리 판독기로 옮긴 사본 재판독 (기대 = GA_args · GB_args 만 거짓)
⑤ 절대 경로 접두를 이 폴더로 바꾼 '원래 자리' 모의 (ckpt.txt · vars.txt · run_manifest kit= · 판정 run_dir — 바꾼 것 목록 기록) + kit 사본 = 리포 history_test 바이트
   + 묶음의 kit SHA256SUMS → 재판독 · ul_reader.grammar_prereq (사전 점검 전체)."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile

WT, KIT, OUT = (os.path.abspath(x) for x in sys.argv[1:4])
RAW = os.path.join(WT, 'docs', 'reviews', 'dem_unloading_grammar_fixture_runs_20261015', 'raw')
HT = os.path.join(KIT, 'history_test')
sys.path.insert(0, KIT)
import ul_reader as U  # noqa: E402

LMP = 'ee2d77261bac9e7fa4e9311c8709e74bf7583a13225a5bc35a791bef9be60a3f'
PREFIX = '/home/yonghoon/ps45_unload_hist_20261013'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


res = {'raw': {}, 'runs': {}}
recv = {}
for ln in open(os.path.join(RAW, 'SHA256SUMS.received'), encoding='utf-8').read().splitlines():
    w = ln.split()
    if len(w) == 2:
        recv[w[1].lstrip('*')] = w[0]
for nm in sorted(os.listdir(RAW)):
    if nm == 'SHA256SUMS.received':
        continue
    res['raw'][nm] = {'sha256': sha(os.path.join(RAW, nm)), 'bytes': os.path.getsize(os.path.join(RAW, nm)), 'received_list': recv.get(nm)}
if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
for nm in sorted(os.listdir(RAW)):
    if not nm.endswith('.report.tgz'):
        continue
    stamp = nm[:-len('.report.tgz')]
    r = res['runs'][stamp] = {}
    with tarfile.open(os.path.join(RAW, nm), 'r:gz') as t:
        mem = t.getmembers()
        bad = [m.name for m in mem if m.name.startswith('/') or '..' in m.name.split('/') or not (m.isfile() or m.isdir())]
        r['n_members'], r['bad_members'] = len(mem), bad
        dest = os.path.join(OUT, 'x_' + stamp)
        os.makedirs(dest)
        if not bad:
            t.extractall(dest, filter='data')
    rd = os.path.join(dest, stamp)
    kv = U.ul_lib.read_kv(os.path.join(rd, 'run_manifest.txt'))
    v = json.load(open(os.path.join(rd, 'grammar_verdict.json'), encoding='utf-8'))
    kd = [x for x in os.listdir(dest) if x.startswith('kit_')]
    ks = os.path.join(dest, kd[0], 'SHA256SUMS') if kd else None
    listed = {}
    if ks:
        for ln in open(ks, encoding='utf-8').read().splitlines():
            w = ln.split()
            if len(w) == 2:
                listed[w[1]] = w[0]
    r.update(repo_head=kv.get('repo_head'), repo_dirty=kv.get('repo_dirty_here'), kit=kv.get('kit'), mode=kv.get('mode'), end=('end' in kv),
             lmp_sha256=kv.get('lmp_sha256'), sums_sha256=kv.get('sums_sha256'), kit_sums_file_sha256=sha(ks) if ks else None,
             kit_reader=listed.get('read_history.py'), kit_params=listed.get('history_params.json'),
             verdict_status=v.get('status'), verdict_exit=v.get('exit_code'), verdict_run_dir=v.get('run_dir'),
             verdict_checks_true=sum(1 for x in (v.get('checks') or {}).values() if x is True), verdict_checks_n=len(v.get('checks') or {}),
             stage_rc={s: (open(os.path.join(rd, s, 'rc')).read().strip() if os.path.exists(os.path.join(rd, s, 'rc')) else None) for s in ('P', 'GA', 'GB')},
             deck_copies={f'{s}/{n}': (sha(os.path.join(rd, s, n)) == U.GRAMMAR_INPUTS.get(n)) if os.path.exists(os.path.join(rd, s, n)) else None
                          for s, d in U.GRAMMAR_STAGES for n in (d, 'plate_hist.stl')})
    # ④ 옮긴 사본 재판독 (우리 판독기)
    op = os.path.join(OUT, f'reread_relocated_{stamp}.json')
    p = subprocess.run([sys.executable, '-I', os.path.join(HT, 'read_history.py'), rd, '--grammar', '--params', os.path.join(HT, 'history_params.json'),
                        '--out', op], capture_output=True, text=True, timeout=600)
    rv = json.load(open(op, encoding='utf-8')) if os.path.exists(op) else {}
    r['relocated'] = {'rc': p.returncode, 'status': rv.get('status'), 'false_checks': sorted(k for k, x in (rv.get('checks') or {}).items() if x is not True)}
    # ⑤ '원래 자리' 모의 — 절대 경로 접두를 이 폴더로 (바꾼 파일 목록)
    if v.get('status') == 'PASS':
        sim_root = os.path.join(OUT, 'sim_' + stamp)
        shutil.copytree(dest, sim_root)
        old = os.path.dirname(v['run_dir'])
        changed = []
        for dp, _dn, fn in os.walk(sim_root):
            for f in fn:
                if f in ('ckpt.txt', 'vars.txt', 'run_manifest.txt', 'grammar_verdict.json'):
                    pth = os.path.join(dp, f)
                    txt = open(pth, encoding='utf-8').read()
                    if old in txt:
                        open(pth, 'w', encoding='utf-8', newline='\n').write(txt.replace(old, sim_root))
                        changed.append(os.path.relpath(pth, sim_root))
        kitc = os.path.join(sim_root, kd[0])
        for f in os.listdir(HT):   # kit 사본 = 리포 history_test 바이트 (러너가 복사하는 15 파일 · SHA256SUMS 는 묶음 것 그대로)
            if f != 'SHA256SUMS' and os.path.isfile(os.path.join(HT, f)):
                shutil.copyfile(os.path.join(HT, f), os.path.join(kitc, f))
        srd = os.path.join(sim_root, stamp)
        op2 = os.path.join(OUT, f'reread_sim_inplace_{stamp}.json')
        p2 = subprocess.run([sys.executable, '-I', os.path.join(kitc, 'read_history.py'), srd, '--grammar', '--params', os.path.join(kitc, 'history_params.json'),
                             '--out', op2], capture_output=True, text=True, timeout=600)
        rv2 = json.load(open(op2, encoding='utf-8')) if os.path.exists(op2) else {}
        ok, pr, rec = U.grammar_prereq(os.path.join(srd, 'grammar_verdict.json'), LMP)
        r['sim_inplace'] = {'rewritten_files': sorted(changed), 'reread_rc': p2.returncode, 'reread_status': rv2.get('status'),
                            'reread_false_checks': sorted(k for k, x in (rv2.get('checks') or {}).items() if x is not True),
                            'checks_equal_json': (rv2.get('checks') == v.get('checks')),
                            'prereq_ok': ok, 'prereq_problems': pr[:6], 'prereq_reread': rec.get('reread')}
json.dump(res, open(os.path.join(OUT, 'probe_run2.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for k, r in res['runs'].items():
    print(k, {x: r.get(x) for x in ('repo_head', 'lmp_sha256', 'sums_sha256', 'kit_reader', 'verdict_status', 'verdict_checks_true', 'stage_rc')})
    print('   relocated', r['relocated'])
    print('   sim_inplace', {x: (r.get('sim_inplace') or {}).get(x) for x in ('rewritten_files', 'reread_status', 'checks_equal_json', 'prereq_ok', 'prereq_problems')})
for k, x in res['raw'].items():
    print(k, x)
