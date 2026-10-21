"""Self-attack probe of run_contract.cert_binding_problem (pure dicts · no solve · seconds).

HOLD classes from CLAUDE.md pre-attack rule ②: NaN · inf · overflow · empty · duplicate · normalisation before check · unicode digits ·
whitespace · cert <-> result binding · other-version certificate.  Each forged value must be refused; the legit pairs accepted.
usage: python3 -I probe_bind.py <scripts dir>"""
import sys

sys.path.insert(0, sys.argv[1])
import run_contract as RC          # noqa: E402
import step3_conv_cert as CC       # noqa: E402

H = lambda c: c * 32               # noqa: E731
CJ = {'registry': H('a'), 'sid': H('b'), 'plan_rows': H('c')}
FA = {'caps': H('e'), 'plan_electronic': H('f'), 'plan_ionic': H('9'), 'sid_off': H('b')}


def man(cj=True, fa=True, cjfp=None, fafp=None):
    ca = {'schema': 'x'}
    if cj:
        ca['cjunc'] = {'protocol': {}, 'evidence': {'fp': dict(CJ if cjfp is None else cjfp)}}
    if fa:
        ca['ptfe_face'] = {'protocol': {}, 'evidence': {'fp': dict(FA if fafp is None else fafp)}}
    return {'ca_ext': ca}


def cert(channel='electronic', cj=True, fa=True, **over):
    c = CC.bind_record(fp_sid=H('b'), fp_sig=H('d'),
                       fp_face_plan=(FA['plan_' + channel] if fa else None),
                       fp_cjunc_registry=(CJ['registry'] if cj and channel == 'electronic' else None),
                       fp_cjunc_rows=(CJ['plan_rows'] if cj and channel == 'electronic' else None))
    c.update(over)
    return c


n_ok = n_bad = 0


def expect(name, got_problem, want_reject):
    global n_ok, n_bad
    ok = (got_problem is not None) == want_reject
    n_ok += ok
    n_bad += (not ok)
    print(('  ok  ' if ok else '  BAD ') + name + ('' if ok else f'  -> {got_problem!r}'))


# legit pairs
for cj in (True, False):
    for fa in (True, False):
        if not (cj or fa):
            continue
        for ch in ('electronic', 'ionic'):
            expect(f'legit cj={cj} fa={fa} {ch}', RC.cert_binding_problem(cert(ch, cj, fa), man(cj, fa), ch), False)

FORGE = {'NaN': float('nan'), 'inf': float('inf'), '-inf': float('-inf'), 'big int': 10 ** 400, 'int': 123, 'True': True,
         'empty': '', 'bytes': H('b').encode(), 'list': [H('b')], 'upper': H('B'), 'lead space': ' ' + H('b')[1:],
         'trail newline': H('b')[:-1] + '\n', 'nbsp': ' ' + H('b')[1:], 'fullwidth a': 'ａ' + H('b')[1:],
         'arabic-indic 3': '٣' + H('b')[1:], 'zero-width space': H('b')[:16] + '​' + H('b')[16:31], '33 chars': H('b') + 'b',
         '31 chars': H('b')[:31], 'hex 0x': '0x' + H('b')[:30], 'other hex': H('7')}
for k in ('fp_sid', 'fp_sig', 'fp_face_plan', 'fp_cjunc_registry', 'fp_cjunc_rows'):
    for nm, v in FORGE.items():
        if k == 'fp_sig' and nm == 'other hex':
            #  σ 표 지문은 형식만 본다 (한정어) — 다른 hex 는 받는다 (기록 → 보고)
            expect(f'cert {k} = {nm} (format-only field: accepted by design)', RC.cert_binding_problem(cert(**{k: v}), man(), 'electronic'), False)
            continue
        expect(f'cert {k} = {nm}', RC.cert_binding_problem(cert(**{k: v}), man(), 'electronic'), True)
for fk in ('sid', 'registry', 'plan_rows'):
    for nm, v in FORGE.items():
        mm = man(cjfp=dict(CJ, **{fk: v}))
        expect(f'manifest cjunc.{fk} = {nm}', RC.cert_binding_problem(cert(), mm, 'electronic'), True)
for fk in ('plan_electronic',):
    for nm, v in FORGE.items():
        mm = man(fafp=dict(FA, **{fk: v}))
        expect(f'manifest ptfe_face.{fk} = {nm}', RC.cert_binding_problem(cert(), mm, 'electronic'), True)
for nm, v in FORGE.items():
    mm = man(cj=False, fafp=dict(FA, sid_off=v))
    expect(f'manifest ptfe_face.sid_off (face_alpha only) = {nm}', RC.cert_binding_problem(cert(cj=False), mm, 'electronic'), True)
# versions / keys
expect('bind_version other', RC.cert_binding_problem(cert(bind_version='cert-bind-v0'), man(), 'electronic'), True)
expect('bind_version missing', RC.cert_binding_problem({k: v for k, v in cert().items() if k != 'bind_version'}, man(), 'electronic'), True)
for k in CC.BIND_KEYS:
    expect(f'cert key {k} missing', RC.cert_binding_problem({kk: v for kk, v in cert().items() if kk != k}, man(), 'electronic'), True)
for ch in ('Electronic', 'electronic ', 'thermal', '', None, 0):
    expect(f'channel {ch!r}', RC.cert_binding_problem(cert(), man(), ch), True)
# manifest shapes
for nm, mm in (('None', None), ('list', []), ('ca_ext list', {'ca_ext': []}), ('cjunc list', {'ca_ext': {'cjunc': []}}),
               ('evidence list', {'ca_ext': {'cjunc': {'evidence': []}}}), ('fp list', {'ca_ext': {'cjunc': {'evidence': {'fp': []}}}}),
               ('only sdcp_mod', {'ca_ext': {'sdcp_mod': {'evidence': {'fp': dict(CJ)}}}})):
    expect(f'manifest {nm}', RC.cert_binding_problem(cert(), mm, 'electronic'), True)
# channel swaps in a combo run
expect('ionic cert in electronic slot', RC.cert_binding_problem(cert('ionic'), man(), 'electronic'), True)
expect('electronic cert in ionic slot', RC.cert_binding_problem(cert('electronic'), man(), 'ionic'), True)
# conv_cert_problem order: inner check first, binding after
print(f'== probe_bind: {n_ok} ok · {n_bad} BAD')
sys.exit(1 if n_bad else 0)
