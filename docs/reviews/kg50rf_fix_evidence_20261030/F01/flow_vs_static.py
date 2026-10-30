"""V8 · V14 의 -C ↔ 본 흐름 문제 줄 차이 (본 흐름에서 늘어난 문제 줄이 무엇인지) — 시험 모듈의 덱 만들기를 그대로 따라 한다.
   python3 -I flow_vs_static.py <작업 트리> <임시 폴더 위>"""
import os
import sys
import tempfile

REPO = sys.argv[1]
sys.path.insert(0, os.path.join(REPO, 'scripts'))
import test_resume_ckpt as T  # noqa: E402

script = os.path.join(REPO, 'scripts/resume_ckpt.sh')
D2D = os.path.join(REPO, 'docs/data/kg50_resume_tests_20261027/d2_main_1028_0942')
d2m = open(os.path.join(D2D, 'input_kg50_d2_b50.liggghts'), encoding='utf-8').read()
d2r = open(os.path.join(D2D, 'input_kg50_d2_b50_r4.liggghts'), encoding='utf-8').read()
D2K = ('restart_kg50_d2_b50/restart_settling_20001.bin', 20001)
RAS = 'variable r_AM_S  equal 2.0e-3'
TSD = 'timestep        ${dt}\n'
t50 = open(T.MAIN50, encoding='utf-8').read()
m14 = t50.replace(TSD, 'variable n0 equal 0\nlabel pre0\n' + TSD + 'variable dt      equal 2.0e-6\nvariable n0 equal ${n0}+1\n'
                  'if "${n0} < 2" then "jump SELF pre0"\n')
r14 = T.res_after('good', T.MAIN50, T.C50, tmpl=True)
r14 = r14.replace(TSD, TSD + 'variable dt      equal 2.0e-6\n')
CK50 = ('restart_%s/restart_after_settling.bin' % T.C50, 200001)
AS50 = dict(mode='after_settling', orig_log=T.AS_LOG)
ok_log = T.trial_log('ok')
tmp = tempfile.mkdtemp(prefix='why_', dir=sys.argv[2])
print('d2r 템플릿 줄 수 (fix pts* · pdd_mix):', sum(1 for l in d2r.splitlines() if l.split()[:1] == ['fix'] and len(l.split()) > 1
                                              and (l.split()[1].startswith('pts') or l.split()[1] == 'pdd_mix')))
print('r14 템플릿 줄 수:', sum(1 for l in r14.splitlines() if l.split()[:1] == ['fix'] and len(l.split()) > 1
                            and (l.split()[1].startswith('pts') or l.split()[1] == 'pdd_mix')))
for tag, (mt, rt), ck, kw in (('V8', (d2m.replace(RAS, RAS + '*(1+step)'), d2r.replace(RAS, RAS + '*(1+step)')), D2K, {}),
                              ('V14', (m14, r14), CK50, AS50)):
    mp, rp = os.path.join(tmp, tag + '_m.liggghts'), os.path.join(tmp, tag + '_r.liggghts')
    with open(mp, 'w', encoding='utf-8') as f:
        f.write(mt)
    with open(rp, 'w', encoding='utf-8') as f:
        f.write(rt)
    rc, out = T.deckcheck_only(script, mp, rp, ck[0], ck[1])
    cl = [l.strip() for l in out.splitlines() if l.startswith('  ✗ ')]
    r = T.run_case(script, None, None, res_text=rt, trial_text=ok_log, main_bytes=mt.encode('utf-8'), ckpt=ck[0], extra=('-T',), **kw)
    fl = [l.strip() for l in r['out'].splitlines() if l.strip().startswith('✗ ') and 'KG50R-F01' in l]
    print('== %s  -C 문제 %d · 흐름 KG50R-F01 문제 %d · 흐름 줄 중 글이 -C 에도 있는 것 %d' % (tag, len(cl), len(fl), sum(l in cl for l in fl)))
    for l in fl:
        if l not in cl:
            print('   흐름에만:', l[:300])
    dup = sorted(set(l for l in fl if fl.count(l) > 1))
    for l in dup:
        print('   흐름에 %d 번:' % fl.count(l), l[:200])
