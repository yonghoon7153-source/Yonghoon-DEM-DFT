"""Mutation check for webapp/test_ca_ext_labels.py W12-W14: patch the template text in memory, run the test main, report which checks fail."""
import builtins
import io
import os
import sys

WT = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-afe53be7bdb176c82'
TPL = os.path.join(WT, 'webapp', 'templates', 'mpm_lab.html')
sys.path.insert(0, os.path.join(WT, 'webapp'))
sys.path.insert(0, os.path.join(WT, 'scripts'))
src = open(TPL, encoding='utf-8').read()

MUTS = {
    'm1 Jinja ratio_limit inf branch dropped': ("('∞' if _svc.get('ratio_limit') == 'inf' else '—')", "'—'"),
    'm2 JS qualifier escape dropped': ("`<div>· ${_e(q)}</div>`", "`<div>· ${q}</div>`"),
    'm3 Jinja zero state word misspelt': ("{% if _cst == 'VALID_ZERO_TOPOLOGY' %}", "{% if _cst == 'VALID_ZERO' %}"),
    'm4 JS ion certificate key dropped': ("[['conv_cert', 'σ_e'], ['ion_conv_cert', 'σ_ion']]", "[['conv_cert', 'σ_e']]"),
    'm5 JS producer flag dropped': ("${_svc.flag ? ` · ${_e(_svc.flag)}` : ''}", ""),
    'm6 Jinja qualifiers not rendered': ("{% for _q in _cjq %}<div>· {{ _q }}</div>{% endfor %}", ""),
    'm7 JS short state shows finite': ("σ = +∞ (J11 단락 · 유한 σ 로 게시하지 않음)</span>` : (_cst === 'NOT_CERTIFIABLE')",
                                       "σ 유한</span>` : (_cst === 'NOT_CERTIFIABLE')"),
}
real_open = builtins.open
for name, (old, new) in MUTS.items():
    assert src.count(old) == 1, (name, src.count(old))
    mut = src.replace(old, new)

    def fake_open(p, *a, _mut=mut, **k):
        if os.path.abspath(str(p)) == TPL:
            return io.StringIO(_mut)
        return real_open(p, *a, **k)
    builtins.open = fake_open
    import importlib
    import test_ca_ext_labels as T
    importlib.reload(T)
    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    try:
        T.main()
        code = 0
    except SystemExit as e:
        code = e.code
    finally:
        sys.stdout = old_stdout
        builtins.open = real_open
    fails = [ln.strip() for ln in buf.getvalue().splitlines() if ln.startswith('  FAIL')]
    print(f'{name}: exit {code} · FAIL {len(fails)} · first: {fails[0][:150] if fails else "-"}')
