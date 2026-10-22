import json, re, subprocess, sys, html
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
L = s.split('\n')
j = L[80]; js = L[232]
a = j.index("{% set _svc = (_cjb['evidence'].get('solve') or {}).get('sv_counterfactual') %}")
b = j.index("{% set _cjq", a)
jsnip = j[a:b]
import jinja2
env = jinja2.Environment(autoescape=True)
t = env.from_string(jsnip)
ja = js.index("const _svc = ")
jb = js.index("const _cjq", ja)
jdef = js[ja:jb]
ea = js.index("(_svok ? `")
eb = js.index(" : '') + (_cjq.length", ea)
jexpr = js[ea:eb + len(" : '')")]
# _e from page
i0 = js.index("const _e = (s) =>"); i1 = js.index("; const _ev", i0)
edef = js[i0:i1] + ";"
_unused = "const _e = (x) => String(x).replace(/[&<>\"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',\"'\":'&#39;'}[c]));"
cases = {
 'bracket': {'sv_counterfactual_ratio': 1.0, 'ratio_limit': None, 'sv_counterfactual_ratio_hi': None, 'ratio_limit_hi': 'inf', 'n_unsplit_bridging_components': 1, 'status': 'computed', 'status_hi': 'no_through_without_sv', 'flag': None},
 'big': {'sv_counterfactual_ratio': 1e16, 'ratio_limit': None, 'sv_counterfactual_ratio_hi': 1e21, 'ratio_limit_hi': None, 'n_unsplit_bridging_components': 0, 'status': 'computed', 'status_hi': 'computed', 'flag': None},
 'bool_nu': {'sv_counterfactual_ratio': 2.5, 'ratio_limit': None, 'sv_counterfactual_ratio_hi': 2.5, 'ratio_limit_hi': None, 'n_unsplit_bridging_components': True, 'status': 'computed', 'status_hi': 'computed', 'flag': None},
 'str_ratio': {'sv_counterfactual_ratio': '2', 'ratio_limit': 'inf', 'sv_counterfactual_ratio_hi': '3', 'ratio_limit_hi': None, 'n_unsplit_bridging_components': '1', 'status': '<b>x</b>', 'status_hi': '<i>y</i>', 'flag': 'SV_DEPENDENT'},
 'nu_float': {'sv_counterfactual_ratio': 1.25, 'ratio_limit': None, 'sv_counterfactual_ratio_hi': 1.5, 'ratio_limit_hi': None, 'n_unsplit_bridging_components': 2.0, 'status': 'computed', 'status_hi': 'computed', 'flag': None},
}
def strip(x):
    return html.unescape(re.sub(r'<[^>]+>', '', x)).strip()
for nm, rec in cases.items():
    jo = strip(t.render(_cjb={'evidence': {'solve': {'sv_counterfactual': rec}}}))
    prog = f"{edef}\nconst _ev = {{solve: {{sv_counterfactual: {json.dumps(rec)}}}}};\n" + jdef.replace('const _ev', '//') + f"\nprocess.stdout.write({jexpr});"
    r = subprocess.run(['node', '-e', prog], capture_output=True, text=True)
    jso = strip(r.stdout) if r.returncode == 0 else 'NODEERR ' + r.stderr[:300]
    same = jo == jso
    print(f"{nm:10s} same={same}\n   J: {jo}\n   S: {jso}")
