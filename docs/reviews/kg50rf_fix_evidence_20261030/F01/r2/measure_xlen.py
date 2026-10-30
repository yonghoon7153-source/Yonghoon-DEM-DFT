# R7 상한 (XCAP) 근거: 실제 kg50 24 쌍 (real24.py 와 같은 재개 덱) 의 -C 대조에서 펼친 글 (var_env 정의 본문 · expand · sub_text · xline) 의 최대 길이
#   도구 heredoc 을 읽어 함수만 감싸 잰다 (도구 파일은 안 바꿈) · usage: python3 -I measure_xlen.py <worktree> <tool>
import os, sys
WT, TOOL = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
s = open(TOOL, encoding='utf-8').read()
a = s.index("deckcheck(){ python3 - \"$@\" <<'PY'\n") + len("deckcheck(){ python3 - \"$@\" <<'PY'\n")
src = s[a:s.index("\nif len(sys.argv) == 3 and sys.argv[1] == '--strip-comments':", a)]
ns = {'__name__': 'deck'}
exec(compile(src, '<deck>', 'exec'), ns)
MAX = {'var_env': 0, 'expand': 0, 'sub_text': 0, 'xline': 0}
o_exp, o_sub, o_xl, o_ve = ns['expand'], ns['sub_text'], ns['xline'], ns['var_env']


def expand(*a, **k):
    t, w = o_exp(*a, **k)
    if t is not None:
        MAX['expand'] = max(MAX['expand'], len(t))
    return t, w


def sub_text(*a, **k):
    t, w = o_sub(*a, **k)
    if t is not None:
        MAX['sub_text'] = max(MAX['sub_text'], len(t))
    return t, w


def xline(*a, **k):
    t = o_xl(*a, **k)
    MAX['xline'] = max(MAX['xline'], len(t))
    return t


def var_env(*a, **k):
    out = o_ve(*a, **k)
    for env, _ in out:
        for st, b in env.values():
            if st != 'bad':
                MAX['var_env'] = max(MAX['var_env'], len(b))
    return out


ns.update(expand=expand, sub_text=sub_text, xline=xline, var_env=var_env)
import glob, tempfile, shutil  # noqa: E402
sys.argv = ['real24']
r24 = {}
exec(compile(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'real24.py'), encoding='utf-8').read().split('\nos.makedirs(TMP')[0]
             .replace("WT = os.path.abspath(sys.argv[1])", "WT = %r" % WT).replace("TOOLS = [os.path.abspath(x) for x in sys.argv[2:]]", "TOOLS = []"),
             'real24', 'exec'), r24)
mains = [m for m in sorted(glob.glob(os.path.join(WT, 'docs/data/kg50_decks_2026102[67]_*/kg50_*/input_kg50_*.liggghts'))) if not m.endswith('_insert.liggghts')]
n = bad = 0
d = tempfile.mkdtemp(prefix='xlen_', dir=r24['TMP'])
try:
    for m in mains:
        case = os.path.basename(m)[len('input_'):-len('.liggghts')]
        for rt, ck, s0 in ((r24['settle_resume'](m, case), 'restart_%s/restart_settling_20001.bin' % case, 20001),
                           (r24['T'].res_after('good', m, case, tmpl=True), 'restart_%s/restart_after_settling.bin' % case, 200001)):
            rp = os.path.join(d, 'r.liggghts')
            with open(rp, 'w', encoding='utf-8') as f:
                f.write(rt)
            probs, _ = ns['check'](m, rp, ck, s0, d)
            n += 1
            bad += bool(probs)
finally:
    shutil.rmtree(d, ignore_errors=True)
print('쌍 %d · 문제 있는 쌍 %d · XCAP %d · 펼친 글 최대 길이 %s' % (n, bad, ns['XCAP'], MAX))
