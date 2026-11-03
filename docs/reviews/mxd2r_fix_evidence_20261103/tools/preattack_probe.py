"""Self pre-attack (CLAUDE.md 'Codex 요청 전 사전 공격 리뷰' ②) for the MXD2R-01 · 02 · 03 fix.

For every changed function the guarantee is attacked with small inputs relevant to it —
NaN / inf / empty / duplicate / whitespace (ASCII · Unicode) / Unicode digits / byte-level forms —
applied to BOTH decks (common mode, metadata hash/bytes rebound), through the three consumer APIs
(readback · D2 pair · plan).  'expect' is what the guarantee requires; 'semantics' says why.
Nothing is executed in LIGGGHTS; the LIGGGHTS reading is a source/doc reading, stated per row.

Usage: python3 -I preattack_probe.py <repo>/scripts <out.json>
"""
import copy
import hashlib
import json
import re
import sys


def main(scripts, out):
    sys.path.insert(0, scripts)
    import test_mixer_d2_consumers as t

    def sub(pattern, repl, count=0):
        return lambda s: re.sub(pattern, repl, s, count=count, flags=re.M)

    def rep(old, new, count=-1):
        return lambda s: s.replace(old, new, count)

    # (name, function attacked, transform on the deck text, expect PASS/FAIL, semantics note)
    text_cases = [
        # ── _d2_time_grammar (run · timestep) ─────────────────────────────────────────────
        ('run_nan', '_d2_time_grammar', sub(r'^run 560606$', 'run nan', 1), 'FAIL', 'not an integer'),
        ('run_inf', '_d2_time_grammar', sub(r'^run 560606$', 'run inf', 1), 'FAIL', 'not an integer'),
        ('run_empty', '_d2_time_grammar', sub(r'^run 560606$', 'run', 1), 'FAIL', 'missing count'),
        ('run_leading_zero', '_d2_time_grammar', sub(r'^run 560606$', 'run 0560606', 1), 'FAIL',
         'same value in LIGGGHTS, but not the generator spelling'),
        ('run_plus_sign', '_d2_time_grammar', sub(r'^run 560606$', 'run +560606', 1), 'FAIL', 'non-generator spelling'),
        ('run_float', '_d2_time_grammar', sub(r'^run 560606$', 'run 560606.0', 1), 'FAIL', 'not an integer token'),
        ('run_unicode_digit', '_d2_time_grammar', sub(r'^run 560606$', 'run ５60606', 1), 'FAIL', 'Unicode digit'),
        ('run_upto_twice', '_d2_time_grammar', sub(r'^run (\d+)$', r'run \1 upto upto'), 'FAIL', 'duplicate option'),
        ('run_tab_separator', '_d2_time_grammar', sub(r'^run (\d+)$', 'run\t\\1'), 'PASS',
         'tab is a token separator for both Python and LIGGGHTS (same command)'),
        ('run_comment_upto', '_d2_time_grammar', sub(r'^run (\d+)$', r'run \1 # upto'), 'PASS',
         'comment — LIGGGHTS strips it too (same command)'),
        ('run_continuation_upto', '_d2_time_grammar', sub(r'^run (\d+)$', 'run \\1 &\n    upto'), 'FAIL',
         '`&` joins the next line — option is real'),
        ('run_nbsp_upto', '_d2_time_grammar', sub(r'^run (\d+)$', 'run \\1\u00a0upto'), 'FAIL',
         'Python str.split() splits on NBSP (3 tokens) — rejected (how LIGGGHTS tokenizes NBSP: not checked here)'),
        ('timestep_nan', '_d2_time_grammar', sub(r'^timestep(\s+)\S+$', r'timestep\1nan'), 'FAIL', 'nonfinite dt'),
        ('timestep_inf', '_d2_time_grammar', sub(r'^timestep(\s+)\S+$', r'timestep\1inf'), 'FAIL', 'nonfinite dt'),
        ('timestep_empty', '_d2_time_grammar', sub(r'^timestep(\s+)\S+$', 'timestep'), 'FAIL', 'missing dt'),
        ('timestep_duplicate_same_value', '_d2_time_grammar',
         lambda s: s.replace('run 1\n', 'run 1\n' + re.search(r'(?m)^timestep[^\n]*', s).group(0) + '\n', 1), 'FAIL',
         'second timestep after the first run (same value) — not the generator form'),
        ('timestep_unicode_digit', '_d2_time_grammar', sub(r'^timestep(\s+)2', r'timestep\g<1>２'), 'FAIL', 'Unicode digit'),
        # ── _d2_lifecycle: insert/pack generator form · common rotation ───────────────────────
        ('insert_every_nan', '_d2_lifecycle', rep('insert_every once', 'insert_every nan'), 'FAIL', 'not once'),
        ('insert_every_zero', '_d2_lifecycle', rep('insert_every once', 'insert_every 0'), 'FAIL', 'not once'),
        ('insert_once_twice', '_d2_lifecycle', rep('insert_every once', 'insert_every once insert_every once'), 'FAIL', 'duplicate option'),
        ('insert_ntry_unicode', '_d2_lifecycle', rep('ntry_mc 20000', 'ntry_mc ２0000'), 'FAIL', 'Unicode digit'),
        ('insert_vel_inf', '_d2_lifecycle', rep('vel constant 0. 0. -0.2', 'vel constant 0. 0. -inf'), 'FAIL', 'nonfinite velocity'),
        ('insert_vel_same_value_spelling', '_d2_lifecycle', rep('vel constant 0. 0. -0.2', 'vel constant 0.0 0.0 -0.20'), 'FAIL',
         'same values, non-generator spelling (exact token pin)'),
        ('front_period_nan', '_d2_lifecycle', sub(r'(fix mvF[^\n]* period )\S+', r'\g<1>nan'), 'FAIL', 'nonfinite period'),
        ('front_period_inf', '_d2_lifecycle', sub(r'(fix mvF[^\n]* period )\S+', r'\g<1>inf'), 'FAIL', 'nonfinite period'),
        ('front_period_negative', '_d2_lifecycle', sub(r'(fix mvF[^\n]* period )(\S+)', r'\g<1>-\2'), 'FAIL',
         'reverse rotation (negative period)'),
        ('front_period_zero', '_d2_lifecycle', sub(r'(fix mvF[^\n]* period )\S+', r'\g<1>0'), 'FAIL', 'zero period'),
        ('front_period_exp_spelling', '_d2_lifecycle', sub(r'(fix mvF[^\n]* period )0\.782508', r'\g<1>7.82508e-1'), 'PASS',
         'exactly the same float as Drum (same rotation)'),
        ('front_period_last_digit', '_d2_lifecycle', sub(r'(fix mvF[^\n]* period )0\.782508', r'\g<1>0.782509'), 'FAIL',
         '1e-6 s different period — not the common rotation'),
        ('front_period_unicode_digit', '_d2_lifecycle', sub(r'(fix mvF[^\n]* period )0', r'\g<1>０'), 'FAIL', 'Unicode digit'),
        ('front_rotates_twice', '_d2_lifecycle',
         lambda s: s.replace('\nrun 6595382', '\nfix mvF2 all move/mesh mesh Front rotate origin 0 0 0 axis 1. 0. 0. period 0.782508\nrun 6595382'),
         'FAIL', 'duplicate motion of one mesh'),
        # ── _d2_contact_grammar: neigh_modify · pair · material fixes ─────────────────────────
        ('neigh_delay_nan', '_d2_contact_grammar', rep('neigh_modify    delay 0', 'neigh_modify    delay nan'), 'FAIL', 'not delay 0'),
        ('neigh_delay_unicode', '_d2_contact_grammar', rep('neigh_modify    delay 0', 'neigh_modify    delay ０'), 'FAIL', 'Unicode digit'),
        ('neigh_duplicate_same', '_d2_contact_grammar', rep('neigh_modify    delay 0', 'neigh_modify    delay 0\nneigh_modify    delay 0'), 'FAIL',
         'duplicate command (generator writes one)'),
        ('neigh_tab', '_d2_contact_grammar', rep('neigh_modify    delay 0', 'neigh_modify\tdelay\t0'), 'PASS', 'tab separator (same command)'),
        ('neigh_nbsp_exclude', '_d2_contact_grammar', rep('neigh_modify    delay 0', 'neigh_modify    delay 0\u00a0exclude type 3 3'), 'FAIL',
         'NBSP-joined option'),
        ('pair_coeff_duplicate', '_d2_contact_grammar', rep('pair_coeff      * *', 'pair_coeff      * *\npair_coeff      * *'), 'FAIL',
         'duplicate command'),
        ('friction_nan', '_d2_contact_grammar', t._friction_values('nan'), 'FAIL', 'nonfinite coefficient'),
        ('friction_inf', '_d2_contact_grammar', t._friction_values('inf'), 'FAIL', 'nonfinite coefficient'),
        ('friction_unicode_digit', '_d2_contact_grammar', t._friction_values('０.9'), 'FAIL', 'Unicode digit'),
        ('friction_same_value_spellings', '_d2_contact_grammar', t._friction_values('9e-1'), 'PASS', 'same float 0.9 (same physics)'),
        ('friction_matrix_size_unicode', '_d2_contact_grammar', rep('coefficientFriction peratomtypepair 4', 'coefficientFriction peratomtypepair ４'),
         'FAIL', 'Unicode digit matrix size'),
        ('friction_matrix_empty', '_d2_contact_grammar',
         lambda s: re.sub(r'(?m)^(fix m4 [^\n]*peratomtypepair 4) &\n(?:    [^\n]*\n){4}', r'\1\n', s), 'FAIL', 'no values'),
        ('restitution_extra_value', '_d2_contact_grammar',
         lambda s: s.replace('    0.3 0.3 0.3 0.3\nfix m4', '    0.3 0.3 0.3 0.3 0.3\nfix m4', 1), 'FAIL', '17 values for 4x4'),
        ('charvel_nan', '_d2_contact_grammar', rep('characteristicVelocity scalar 2.0', 'characteristicVelocity scalar nan'), 'FAIL', 'nonfinite'),
        ('property_name_empty', '_d2_contact_grammar', rep('fix m9 all property/global characteristicVelocity scalar 2.0',
                                                            'fix m9 all property/global'), 'FAIL', 'property/global without a name'),
        ('ced_duplicate_fix', '_d2_contact_grammar',
         lambda s: s.replace('fix m9 all', re.search(r'(?m)^fix mC [^\n]*\n(?:    [^\n]*\n){4}', s).group(0).replace('fix mC', 'fix mC2') + 'fix m9 all', 1),
         'FAIL', 'second CED fix (read_deck duplicate count + material duplicate)'),
        # ── whole-deck byte/whitespace forms (read_d2) ────────────────────────────────────────
        ('bom_prefix', 'read_d2', lambda s: '\ufeff' + s, 'FAIL', 'UTF-8 BOM before the first line (not generator output)'),
        ('nul_in_comment', 'read_d2', lambda s: s.replace('# 믹싱 드럼', '# \x00 믹싱 드럼', 1), 'PASS',
         'NUL inside a comment — both Python and LIGGGHTS ignore comment text'),
        ('form_feed_in_code', 'read_d2', rep('neigh_modify    delay 0', 'neigh_modify\fdelay 0'), 'PASS',
         'form feed: Python str.split() separator (LIGGGHTS tokenizer separators: not checked here — see README limits)'),
        ('trailing_spaces', 'read_d2', sub(r'^(run \d+)$', r'\1   '), 'PASS', 'trailing spaces (same command)'),
        # ── quoted '#' (the consumer drops from the first '#'; how LIGGGHTS reads a quoted '#' is not checked) — pinned lines ──
        ('quote_hash_run', '_d2_time_grammar', sub(r'^run (\d+)$', r'run \1 "#" upto'), 'FAIL', 'leftover `"` token on a pinned line'),
        ('quote_hash_neigh', '_d2_contact_grammar', rep('neigh_modify    delay 0', 'neigh_modify    delay 0 "#" exclude type 3 3'), 'FAIL',
         'leftover `"` token on a pinned line'),
        ('quote_hash_insert', '_d2_lifecycle', rep('ntry_mc 20000   # AM', 'ntry_mc 20000 "#" start 9000000   # AM'), 'FAIL',
         'leftover `"` token on a pinned line'),
        ('quote_hash_front', '_d2_lifecycle', sub(r'(fix mvF[^\n]* period \S+)$', r'\1 "#" x'), 'FAIL', 'leftover `"` token on a pinned line'),
        ('quote_hash_mesh', 'read_d2', sub(r'^(fix Front all mesh/surface [^\n]*)$', r'\1 "#" move 0 0 1'), 'FAIL',
         'leftover `"` token on a pinned line (mesh/surface 10 tokens)'),
    ]

    a0, am0, _ = t.fixture()
    b0, bm0, _ = t.fixture(coated=True)
    rows = []
    for name, func, transform, expect, why in text_cases:
        a, b = transform(a0), transform(b0)
        assert a != a0 and b != b0, name
        ma, mb = t.rebound(a, am0), t.rebound(b, bm0)
        res = {'readback': t.rb.read_d2(a, ma), 'pair': t.dd.diff_d2_decks(a, b, ma, mb), 'plan': t.smoke.d2_plan_check(a, ma)}
        got = {k: v['verdict'] for k, v in res.items()}
        rows.append(dict(case=name, attacks=func, expect=expect, verdicts=got, ok=all(v == expect for v in got.values()),
                         first_failure=(res['readback']['failures'] or [''])[0][:220], semantics=why))

    # ── byte-level inputs (MXD2R-03 · read_d2 deck argument) ───────────────────────────────
    raw = a0.encode('utf-8')

    def meta_for(data):
        m = copy.deepcopy(am0)
        m['deck_sha256'] = hashlib.sha256(data).hexdigest()
        m['deck_bytes'] = len(data)
        return m
    byte_cases = [
        ('bytes_lf', raw, meta_for(raw), 'PASS', 'physical LF bytes'),
        ('bytes_lone_cr_in_comment', raw.replace('# 믹싱'.encode(), '#\r 믹싱'.encode(), 1), None, 'FAIL', 'any CR byte'),
        ('bytes_cr_only_line_endings', raw.replace(b'\n', b'\r'), None, 'FAIL', 'old-Mac CR line endings'),
        ('bytes_crlf', raw.replace(b'\n', b'\r\n'), None, 'FAIL', 'CRLF'),
        ('bytes_invalid_utf8', raw + b'# \xff\n', None, 'FAIL', 'invalid UTF-8 (strict decode)'),
        ('bytes_utf16', a0.encode('utf-16'), None, 'FAIL', 'UTF-16 with BOM'),
        ('bytes_utf16le_no_bom', a0.encode('utf-16-le'), None, 'FAIL', 'NUL-interleaved (valid UTF-8, unknown commands)'),
        ('bytes_empty', b'', None, 'FAIL', 'empty deck (deck_bytes must be positive)'),
        ('bytes_trailing_nul', raw + b'\x00', None, 'FAIL', 'NUL after the last newline = a command token'),
        ('bytearray_input', bytearray(raw), meta_for(raw), 'FAIL', 'only bytes or str'),
        ('memoryview_input', memoryview(raw), meta_for(raw), 'FAIL', 'only bytes or str'),
        ('none_input', None, meta_for(raw), 'FAIL', 'unreadable file in the diff CLI arrives as None'),
        ('str_surrogate', a0 + '# \udc80\n', meta_for(raw), 'FAIL', 'str that cannot be UTF-8 encoded (must fail, not crash)'),
        ('bytes_meta_len_off_by_one', raw, dict(meta_for(raw), deck_bytes=len(raw) + 1), 'FAIL', 'length mismatch'),
        ('bytes_meta_len_bool', raw, dict(meta_for(raw), deck_bytes=True), 'FAIL', 'bool is not an integer'),
        ('bytes_meta_sha_upper', raw, dict(meta_for(raw), deck_sha256=hashlib.sha256(raw).hexdigest().upper()), 'FAIL',
         'upper-case hex is not the recorded form'),
    ]
    for name, data, meta, expect, why in byte_cases:
        if meta is None:
            meta = meta_for(data)
        verdict = t.rb.read_d2(data, meta)
        rows.append(dict(case=name, attacks='read_d2 (bytes)', expect=expect, verdicts={'readback': verdict['verdict']},
                         ok=verdict['verdict'] == expect, first_failure=(verdict['failures'] or [''])[0][:220], semantics=why))
    report = dict(tool='preattack_probe.py', python=sys.version.split()[0], n=len(rows),
                  n_ok=sum(r['ok'] for r in rows), rows=rows)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
        f.write('\n')
    for r in rows:
        print(('ok  ' if r['ok'] else 'GAP ') + r['case'].ljust(36) + ' expect ' + r['expect'] + ' got ' + str(r['verdicts']))
    print(f"{report['n_ok']}/{report['n']} as the guarantee requires")


if __name__ == '__main__':
    main(*sys.argv[1:])
