#!/usr/bin/env python3
"""PAI probe — reproduce '실제 kg50 본 덱 12 × (settling · after_settling) 24 쌍 = rc 0 24' (65c5d6d37 commit message) with the
repo's own generators (no script/log for that claim is committed at 65c5d6d37):
  settling  = harness res_good() (MAIN patched) + with_tmpl()  ·  also the D2-learned dem_restart.py form (make_d07_resume.T) when
              the deck has the 257-line v3 layout
  after_settling = harness res_after(main, case, tmpl=True)
usage: python3 pairs24.py <scratch>
"""
import glob, importlib.util, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '../../../../..'))
spec = importlib.util.spec_from_file_location('trc', os.path.join(REPO, 'scripts/test_resume_ckpt.py'))
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
spec2 = importlib.util.spec_from_file_location('mk', os.path.join(HERE, 'make_d07_resume.py'))
mk = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(mk)


def cflag(main, res, ck, s0, W):
    p = subprocess.run(['bash', t.SCRIPT, '-C', main, res, ck, str(s0), W], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.stdout.decode('utf-8', 'replace')
    last = [l.strip() for l in out.splitlines() if '재개 덱 정적 대조:' in l]
    first = [l.strip()[:140] for l in out.splitlines() if l.strip().startswith('✗')][:1]
    return p.returncode, (last or ['?'])[0], (first or [''])[0]


def main():
    sp = sys.argv[1]
    W = os.path.join(sp, 'w_pairs')
    os.makedirs(W, exist_ok=True)
    mains = sorted(p for p in glob.glob(os.path.join(REPO, 'docs/data/kg50_decks_*/kg50_*/input_kg50_*.liggghts'))
                   if not p.endswith('_insert.liggghts') and '20261026/' not in p.replace('20261026_v2', ''))
    mains = [p for p in mains if '/kg50_decks_20261026_v2/' in p or '/kg50_decks_20261027_v3_b50/' in p]
    rows, n0 = [], 0
    for mp in mains:
        case = os.path.basename(os.path.dirname(mp))
        t.MAIN, t.C = mp, case
        t.CKPT = 'restart_%s/restart_settling_20001.bin' % case
        res = []
        try:
            res.append(('settling (harness res_good + 템플릿)', t.with_tmpl(t.res_good()), t.CKPT, 20001))
        except Exception as e:
            rows.append((case, 'settling (harness)', 'GEN-FAIL %s' % e, '', ''))
        L = open(mp, encoding='utf-8', newline='').read().splitlines(keepends=True)
        if len(L) == 257:
            try:
                raw = mk.T(L, case, 'r56', t.CKPT, 20001, 179999)
                res.append(('settling (dem_restart.py 꼴 재구성 · fix-run 뒤)', ''.join(mk.tool_edits(raw, L)), t.CKPT, 20001))
            except AssertionError as e:
                rows.append((case, 'settling (dem_restart.py 꼴)', 'layout differs %s' % str(e)[:60], '', ''))
        try:
            res.append(('after_settling (harness res_after tmpl)', t.res_after('good', main=mp, case=case, tmpl=True),
                        'restart_%s/restart_after_settling.bin' % case, 200001))
        except Exception as e:
            rows.append((case, 'after_settling (harness)', 'GEN-FAIL %s' % e, '', ''))
        for tag, text, ck, s0 in res:
            rp = os.path.join(sp, 'pair_res.liggghts')
            open(rp, 'w', encoding='utf-8').write(text)
            rc, last, first = cflag(mp, rp, ck, s0, W)
            n0 += rc == 0
            rows.append((case, tag, rc, last, first))
    print('| 본 덱 | 재개 덱 꼴 | -C rc | 판정 | 첫 문제 |\n|---|---|---|---|---|')
    for r in rows:
        print('| %s | %s | %s | %s | %s |' % r)
    print('\n본 덱 %d 개 · 쌍 %d · rc 0 = %d' % (len(mains), len([r for r in rows if isinstance(r[2], int)]), n0))


if __name__ == '__main__':
    main()
