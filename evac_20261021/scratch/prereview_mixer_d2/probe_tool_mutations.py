#!/usr/bin/env python3
"""recheck 10-21 — mutation tests on the FIXED checking tools (readback · deck diff · contact reader · smoke) at 9412f384a.

Each mutant = a folder mutt/<name>/ holding symlinks to every file of <W>/scripts except the mutated tool (a real, edited copy).
The mutated tool's selftest is run from that folder (its _HERE = mutant folder → imports resolve to the symlinks).
Diff mutants also re-run the readback selftest? no — each tool's own selftest only (that is the claim being tested).
KILLED = rc != 0 or a FAIL/✗ line.  Control per tool = unmutated copy.
usage: python3 -I -B probe_tool_mutations.py <W> [tools...]   (tools: rb df cr sm; default rb df cr)
"""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W = sys.argv[1]
TOOLS = sys.argv[2:] or ['rb', 'df', 'cr']
SCRIPTS = os.path.join(W, 'scripts')
FILES = {'rb': 'mixer_deck_readback.py', 'df': 'mixer_deck_diff.py', 'cr': 'mixer_contact_reader.py', 'sm': 'mixer_smoke_blind.py'}
MUT = {
    'rb': [
        ('R01_bo_check_off', "        if not _near(R['bo_read'], dc['bo_se'], TOL['gm_bo_rel']):", '        if False:'),
        ('R02_law_check_off', "        elif not _near(ratio, expect, TOL['gm_law_rel']):", '        elif False:'),
        ('R03_q2_gw_rho_off', "        if not _near(dc['gamma_wall'], GM_WALL * dc['rho'], q):", '        if False:'),
        ('R04_q2_ncm_off', "        off = {t: tk[t] for t in D2_NCM if not (_near(g[t], 1.0, q) or _near(g[t], dc['rho'], q))}", '        off = {}'),
        ('R05_overlap_off', "        if not ov <= OVL_CEILING * (1.0 + TOL['gm_ovl_rel']):", '        if False:'),
        ('R06_hdr_ratio_col_off', "                                   ('ratio', ratio, TOL['gm_hdr_rel'])):", '                                   ):'),
        ('R07_meta_binding_off', "    m = D.get('meta')\n    if m is None:\n        return []", "    m = None\n    if m is None:\n        return []"),
        ('R08_meta_bo_binding_off', "    for key, t_, what in (('gamma_wall', 'gw', 'γ_W/γ_SE'), ('bo_se', 'bo', 'SE–SE Bo_code (절대 수준)')):",
         "    for key, t_, what in (('gamma_wall', 'gw', 'γ_W/γ_SE'),):"),
        ('R09_lab_generation_dropped', "REG_DENSITY_GEN = {'gen1': {'AM': 4800.0, 'SE': 2000.0}, 'lab20261014': {'AM': 4850.0, 'SE': 1640.0}}",
         "REG_DENSITY_GEN = {'gen1': {'AM': 4800.0, 'SE': 2000.0}}"),
        ('R10_dens_tag_check_off', '    elif dd and dd[0] != gen:', '    elif False:'),
        ('R11_gm_same_world_off', "            check('같은 ρ 세계 — 밀도 세대 · 벽 규칙 · ρ_비코팅 · γ_W · SE γ · Bo_SE · 삽입이 같다 (NCM 표면만 바뀐다)', not dif,",
         "            check('같은 ρ 세계 — 밀도 세대 · 벽 규칙 · ρ_비코팅 · γ_W · SE γ · Bo_SE · 삽입이 같다 (NCM 표면만 바뀐다)', True,"),
        ('R12_gm_surface_change_off', """                  a_['surface'] != b_['surface'], f"{a_['surface']} → {b_['surface']}")""",
         """                  True, f"{a_['surface']} → {b_['surface']}")"""),
        ('R13_gm_mult_tol_wide', "abs((n_ / o_) / e_ - 1.0) <= TOL['gm_mult_rel'])", "abs((n_ / o_) / e_ - 1.0) <= 0.5)"),
        ('R14_gm_unchanged_token_off', "                        r_['ok'] = A['ced_tok'][key] == B['ced_tok'][key]\n                        r_['reason'] = '' if r_['ok'] else (f'규칙이 안 바꾸는",
         "                        r_['ok'] = True\n                        r_['reason'] = '' if r_['ok'] else (f'규칙이 안 바꾸는"),
        ('R15_E_same_arm_off', "                  RA_['is_d2'] and RB_['is_d2'] and ka is not None and ka == kb, f'{ka} ⇄ {kb}')",
         "                  True, f'{ka} ⇄ {kb}')"),
        ('R16_is_d2_by_meta_off', "    R['is_d2'] = heads > 0 or (isinstance(meta, dict) and 'adhesion_rule' in meta)", "    R['is_d2'] = heads > 0"),
        ('R17_insertion_line_off', "    if dc['layered'] != (n_ins == 2):", '    if False:'),
        ('R18_surface_vs_gamma_off', "        if dc['surface'][t] not in allowed[t]:", '        if False:'),
        ('R19_explicit_coated_only_off', '        off = {t: tk[t] for t in D2_NCM if not _near(g[t], 1.0, q)}', '        off = {}'),
        ('R20_dec_any_float', '    if not isinstance(tok, str) or not _RE_DEC.fullmatch(tok):', '    if not isinstance(tok, str):'),
        ('R21_two_heads_ok', '    if heads > 1:', '    if False:'),
        ('R22_bo_uses_reg_g', "        R['bo_read'] = fss / ((4.0 / 3.0) * math.pi * r_se ** 3 * rho_se * grav)",
         "        R['bo_read'] = fss / ((4.0 / 3.0) * math.pi * r_se ** 3 * rho_se * REG_G)"),
        ('R23_load_meta_never', "    mp = os.path.join(os.path.dirname(os.path.abspath(path)), 'deck_meta.json')\n    if not os.path.exists(mp):\n        return None",
         "    mp = os.path.join(os.path.dirname(os.path.abspath(path)), 'deck_meta.json')\n    if True:\n        return None"),
        ('R24_meta_schema_off', "    if m.get('schema') != D2_META_SCHEMA:", '    if False:'),
        ('R25_meta_sha_off', "    if m.get('deck_sha256') != D['sha256']:", '    if False:'),
    ],
    'df': [
        ('D01_d2_attach_off', '    return _d2_attach(out, allow, RA, RB)', '    return out'),
        ('D02_d2_read_none', "    if not isinstance(text, str) or _rb.D2_HEAD not in text:", '    if True:'),
        ('D03_E_pairing_off', '        if (RA is None) != (RB is None):', '        if False:'),
        ('D04_E_same_decl_off', "        elif RA is not None and RA.get('decl') and RB.get('decl') and _d2_key(RA['decl']) != _d2_key(RB['decl']):",
         '        elif False:'),
        ('D05_gm_same_world_off', '    if dif:\n        dr.append(f"GM 은 같은 ρ 세계 비교다', '    if False:\n        dr.append(f"GM 은 같은 ρ 세계 비교다'),
        ('D06_gm_same_surface_ok', "    if A_['surface'] == B_['surface']:", '    if False:'),
        ('D07_gm_mult_tol_wide', 'abs((y / x) / e_ - 1.0) <= GM_MULT_REL):', 'abs((y / x) / e_ - 1.0) <= 0.5):'),
        ('D08_gm_outside_ignored', "    out['outside'] = sorted(changed - expected)", "    out['outside'] = []"),
        ('D09_d2_cell_meta_not_required', " or is_d2      # ★ D2 셀", "      # ★ D2 셀"),
        ('D10_d2_cell_meta_fields_off', "            if is_d2:\n                #  ★ 2026-10-21 (MXD2-01 · 02) — D2 셀: 세대",
         "            if False:\n                #  ★ 2026-10-21 (MXD2-01 · 02) — D2 셀: 세대"),
        ('D11_d2_cell_readback_off', '            if is_d2 and isinstance(mj, dict):', '            if False:'),
        ('D12_grammar_rho1_any_state', "    if rho == 1.0 and (sp, ss) != ('c', 'c'):", '    if False:'),
        ('D13_grammar_noncanonical', "_D2_DEC = r'(?:0|[1-9][0-9]*)(?:p[0-9]*[1-9])?'", "_D2_DEC = r'[0-9]+(?:p[0-9]+)?'"),
        ('D14_cli_args_no_densgen', "            '--seed', str(c_['seed']), '--dens-gen', c_['dens_gen'],", "            '--seed', str(c_['seed']),"),
    ],
    'cr': [
        ('C01_schema_v2_rejected', "DECK_META_SCHEMAS = (DECK_META_SCHEMA, 'mixer_deck_meta/2')", 'DECK_META_SCHEMAS = (DECK_META_SCHEMA,)'),
        ('C02_any_schema', "    if not isinstance(meta, dict) or meta.get('schema') not in DECK_META_SCHEMAS:", '    if not isinstance(meta, dict):'),
    ],
    'sm': [
        ('S01_counts_gen1', "stiffen_se=c['stiffen_se'], dens_gen=c.get('dens_gen'))", "stiffen_se=c['stiffen_se'])"),
    ],
}


def mk(name, tool, text):
    d = os.path.join(HERE, 'mutt', name)
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    for f in os.listdir(SCRIPTS):
        src = os.path.join(SCRIPTS, f)
        if f == FILES[tool] or f == '__pycache__':
            continue
        os.symlink(src, os.path.join(d, f))
    open(os.path.join(d, FILES[tool]), 'w', encoding='utf-8').write(text)
    return d


def run(d, tool):
    p = subprocess.run([sys.executable, '-I', '-B', os.path.join(d, FILES[tool]), '--selftest'], capture_output=True, text=True,
                       env=dict(os.environ, OPENBLAS_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1'), timeout=1200)
    out = p.stdout + p.stderr
    fails = [l.strip()[:120] for l in out.splitlines() if l.lstrip().startswith(('FAIL', '✗')) or ' FAIL ' in l[:12]]
    tail = [l for l in out.splitlines() if 'selftest' in l and ('PASS' in l or 'FAIL' in l)]
    return dict(rc=p.returncode, n_fail=len(fails), fails=fails[:6], summary=(tail[-1] if tail else out.strip().splitlines()[-1:] or [''])[:200]
                if isinstance(tail, list) else '')


res = []
for tool in TOOLS:
    src = open(os.path.join(SCRIPTS, FILES[tool]), encoding='utf-8').read()
    d = mk('CTL_' + tool, tool, src)
    r = run(d, tool)
    r.update(tool=tool, mutation='CONTROL', status='CLEAN' if (r['rc'] == 0 and not r['n_fail']) else 'DIRTY')
    res.append(r)
    print(f"[{tool}] CONTROL rc={r['rc']} nfail={r['n_fail']} {str(r['summary'])[:80]}")
    shutil.rmtree(d)
    for name, old, new in MUT[tool]:
        n = src.count(old)
        rec = dict(tool=tool, mutation=name, occurrences=n)
        if n != 1:
            rec['status'] = 'NOT_APPLIED'
            res.append(rec)
            print(f'[{tool}] {name}: NOT APPLIED (occurrences {n})')
            continue
        d = mk(name, tool, src.replace(old, new))
        rec.update(run(d, tool))
        rec['status'] = 'KILLED' if (rec['rc'] != 0 or rec['n_fail']) else 'SURVIVED'
        res.append(rec)
        shutil.rmtree(d)
        print(f"[{tool}] {name:34s} {rec['status']:9s} rc={rec['rc']} nfail={rec['n_fail']} | {'; '.join(x[:50] for x in rec['fails'][:3])}")
json.dump(res, open(os.path.join(HERE, 'probe_tool_mutations_' + '_'.join(TOOLS) + '.json'), 'w'), ensure_ascii=False, indent=1)
summ = {}
for r in res:
    summ[r['status']] = summ.get(r['status'], 0) + 1
print('SUMMARY', summ)
