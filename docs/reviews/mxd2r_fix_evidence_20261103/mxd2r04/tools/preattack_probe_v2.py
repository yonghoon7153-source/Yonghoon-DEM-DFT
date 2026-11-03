"""Self pre-attack (CLAUDE.md 'Codex 요청 전 사전 공격 리뷰' ②) for the MXD2R-04 fix — the two new functions
`_d2_text_form` (character form: our parser and LIGGGHTS read the same tokens) and `_d2_generator_form` (every command =
the generator's tokens).  Attacks: NaN / inf / empty / duplicate / whitespace (ASCII · Unicode) / Unicode letters ·
digits · marks / byte forms / CRLF / normalization before the check / layout that must stay free / metadata
coordinated with the deck.  Both decks are edited (common mode), metadata hash/bytes rebound (+ the stated metadata
edit), through the three consumer APIs (readback · D2 pair · plan); byte rows go through the readback API with bytes.
'expect' = what the guarantee requires; 'reason' (FAIL rows) = a fragment that must be in the readback failure (the
right reason, not an incidental one).  Nothing is executed in LIGGGHTS.

Usage: python3 -I -X utf8 -B preattack_probe_v2.py <repo>/scripts <out.json>
"""
import copy
import hashlib
import json
import re
import sys


def main(scripts, out):
    sys.path.insert(0, scripts)
    import test_mixer_d2_consumers as t
    rb = t.rb

    def sub(pattern, repl, count=0):
        return lambda s: re.sub(pattern, repl, s, count=count, flags=re.M)

    def rep(old, new, count=1):
        return lambda s: s.replace(old, new, count)

    def tok(k, got, want):
        return f'token {k} `{got}` (generator `{want}`)'

    CTRL, ASCII, CONT, EOL = 'control character', 'printable ASCII without quotes or $', "continuation must be a command line", 'must end with a newline'
    GF = 'D2 generator form'
    fixtures = {}

    def fixture(**kw):
        key = tuple(sorted(kw.items()))
        if key not in fixtures:
            fixtures[key] = (t.fixture(**kw), t.fixture(coated=True, **kw))
        return fixtures[key]

    def set_meta(path, value):
        def edit(meta, deck):
            node = meta
            for part in path[:-1]:
                node = node[part]
            node[path[-1]] = value(meta, deck) if callable(value) else value
        return edit

    def seed_edit(new_seed):
        """deck insA seed + metadata seed, nothing else (the prime / bound rule is then the only difference)."""
        deck = lambda s: s.replace('insert/pack seed 32452843 ', f'insert/pack seed {new_seed} ', 1)
        return deck, set_meta(('seed',), new_seed)

    def steps_edit(fill_delta=0, dump_new=None, restart_new=None):
        """Change settle steps / dump / restart interval in the deck and keep every metadata time field consistent."""
        def deck(s):
            if fill_delta:
                f = int(re.search(r'(?m)^run (\d+)\nunfix', s).group(1))
                s = s.replace(f'run {f}\n', f'run {f + fill_delta}\n')
            if dump_new:
                s = re.sub(r'(?m)^(dump dmp all custom )\d+', r'\g<1>' + str(dump_new), s)
            if restart_new:
                s = re.sub(r'(?m)^restart \d+ ', f'restart {restart_new} ', s)
            return s

        def meta_edit(meta, deck_text):
            steps, phys, dt = meta['steps'], meta['physical_s'], meta['dt']['deck_s']
            steps['fill'] += fill_delta
            if dump_new:
                steps['dump_every'] = dump_new
            if restart_new:
                steps['restart_every'] = restart_new
            steps['t0_planned'] = (2 * steps['fill'] // steps['dump_every']) * steps['dump_every']
            phys.update(settle=2 * steps['fill'] * dt, dump_interval=steps['dump_every'] * dt, t0_planned=steps['t0_planned'] * dt)
        return deck, meta_edit

    def dt_edit(new_of_old):
        def deck(s):
            old = re.search(r'(?m)^timestep\s+(\S+)$', s).group(1)
            return s.replace('timestep        ' + old + '\n', 'timestep        ' + new_of_old(old) + '\n')
        return deck, set_meta(('dt', 'deck_txt'), lambda meta, d: re.search(r'(?m)^timestep\s+(\S+)$', d).group(1))

    big_prime = rb._d2_next_prime(2 ** 31)
    DPF = dict(dump_full_precision=True)
    FMT = rb.D2_DUMP_FORMAT
    dpf_line = 'dump_modify dmp format "' + FMT + '"'
    # (name, function attacked, fixture kwargs, deck transform, metadata edit or None, expect, reason fragment, semantics)
    cases = [
        # ── _d2_text_form: control characters anywhere (generator output has none) ─────────────────────────
        ('tab_in_code', '_d2_text_form', {}, rep('boundary        f f f', 'boundary\tf f f'), None, 'FAIL', CTRL,
         'TAB separates tokens for both parsers — same command, not the generator spelling'),
        ('tab_in_comment', '_d2_text_form', {}, rep('# 믹싱 드럼', '# 믹싱\t드럼'), None, 'FAIL', CTRL, 'no control character anywhere'),
        ('form_feed_in_code', '_d2_text_form', {}, rep('neigh_modify    delay 0', 'neigh_modify\fdelay 0'), None, 'FAIL', CTRL,
         'FF = whitespace for both parsers (same tokens) — not generator output'),
        ('nul_in_code', '_d2_text_form', {}, rep('boundary        f f f', 'boundary        f f f\x00'), None, 'FAIL', CTRL, 'NUL'),
        ('nul_in_comment', '_d2_text_form', {}, rep('# 믹싱 드럼', '# \x00 믹싱 드럼'), None, 'FAIL', CTRL,
         'a C-string line ends at NUL — the rest of the physical line would not reach a C reader as written'),
        ('del_in_comment', '_d2_text_form', {}, rep('# 믹싱 드럼', '# 믹싱\x7f드럼'), None, 'FAIL', CTRL, 'DEL'),
        ('nel_in_comment_middle', '_d2_text_form', {}, rep('# 믹싱 드럼', '# 믹싱\x85드럼'), None, 'FAIL', CTRL,
         'U+0085 is Python whitespace (C1 control)'),
        ('esc_in_comment', '_d2_text_form', {}, rep('# 믹싱 드럼', '# 믹싱\x1b드럼'), None, 'FAIL', CTRL, 'C0 control'),
        # ── _d2_text_form: command text = printable ASCII without quotes or $ ─────────────────────────────────
        ('nbsp_in_code', '_d2_text_form', {}, rep('boundary        f f f', 'boundary        f f f'), None, 'FAIL', ASCII,
         'Python splits on NBSP, LIGGGHTS (ASCII whitespace) would not'),
        ('ideographic_space_in_code', '_d2_text_form', {}, rep('newton          off', 'newton　off'), None, 'FAIL', ASCII, 'U+3000'),
        ('line_separator_in_code', '_d2_text_form', {}, rep('boundary        f f f', 'boundary        f f f'), None, 'FAIL', ASCII,
         'U+2028 = Python whitespace, not a line end for either parser'),
        ('zero_width_space_in_code', '_d2_text_form', {}, rep('boundary        f f f', 'boundary        f f f​'), None, 'FAIL', ASCII,
         'invisible character glued to a token'),
        ('fullwidth_letters', '_d2_text_form', {}, rep('boundary        f f f', 'ｂｏｕｎｄａｒｙ        f f f'), None, 'FAIL', 'unsupported command',
         'NFKC would map to "boundary" — no normalization before the check (an earlier check rejects the unknown command name first)'),
        ('cyrillic_homoglyph', '_d2_text_form', {}, rep('atom_style      granular', 'atom_style      granulаr'), None, 'FAIL', ASCII,
         'Cyrillic а looks like Latin a'),
        ('combining_mark', '_d2_text_form', {}, rep('newton          off', 'newton          of́f'), None, 'FAIL', ASCII, 'combining acute'),
        ('fullwidth_digit', '_d2_text_form', {}, rep('thermo 5000', 'thermo ５000'), None, 'FAIL', ASCII, 'Unicode digit'),
        ('single_quote', '_d2_text_form', {}, rep('thermo_style custom step atoms ke c_rke vol', "thermo_style custom step atoms ke c_rke 'vol'"),
         None, 'FAIL', ASCII, 'LIGGGHTS strips quotes — our parser would keep them'),
        ('double_quote_hash_on_template', '_d2_text_form', {},
         sub(r'^(fix pt1 [^\n]*radius constant \S+)$', r'\1 "#" volume_limit 1e-30'), None, 'FAIL', ASCII,
         'quoted # hides options from our parser (it cuts at the first #)'),
        ('dollar_variable', '_d2_text_form', {}, rep('thermo 5000', 'thermo ${every}'), None, 'FAIL', ASCII, 'LIGGGHTS substitutes $'),
        ('dollar_immediate', '_d2_text_form', {}, rep('thermo 5000', 'thermo $(5000)'), None, 'FAIL', ASCII, '$(...) form'),
        # ── _d2_text_form: continuation ' &' only on command lines ───────────────────────────────────────────
        ('comment_amp_nbsp_hides_command', '_d2_text_form', {},
         rep('neigh_modify    delay 0\n', 'neigh_modify    delay 0\n# note & \nneigh_modify exclude type 3 3\n'), None, 'FAIL', CONT,
         'our parser (Unicode rstrip) joins the exclude line into the comment; an ASCII-whitespace reader would not'),
        ('comment_amp_ideographic', '_d2_text_form', {},
         rep('neigh_modify    delay 0\n', 'neigh_modify    delay 0\n# note &　\nneigh_modify exclude type 3 3\n'), None, 'FAIL', CONT, 'U+3000'),
        ('comment_amp_ascii', '_d2_text_form', {},
         rep('neigh_modify    delay 0\n', 'neigh_modify    delay 0\n# note &\nneigh_modify exclude type 3 3\n'), None, 'FAIL', CONT,
         'both parsers would swallow the next line into the comment — not generator output'),
        ('command_amp_then_comment', '_d2_text_form', {},
         rep('coefficientFriction peratomtypepair 4 &', 'coefficientFriction peratomtypepair 4 & # rows'), None, 'FAIL', None,
         'no continuation for either parser (& is a token) — rejected (rows become commands)'),
        ('continuation_no_space', '_d2_text_form', {}, rep('coefficientFriction peratomtypepair 4 &', 'coefficientFriction peratomtypepair 4&'),
         None, 'FAIL', CONT, 'a C reader overwrites & with the next line (no separator)'),
        ('continuation_trailing_space', '_d2_text_form', {},
         rep('coefficientFriction peratomtypepair 4 &', 'coefficientFriction peratomtypepair 4 & '), None, 'FAIL', CONT, 'trailing space after &'),
        ('continuation_trailing_nbsp', '_d2_text_form', {},
         rep('coefficientFriction peratomtypepair 4 &', 'coefficientFriction peratomtypepair 4 & '), None, 'FAIL', ASCII,
         'joins for our parser only (the NBSP is in the command text — the ASCII rule of the same function fires first)'),
        ('continuation_double_amp', '_d2_text_form', {},
         rep('coefficientFriction peratomtypepair 4 &', 'coefficientFriction peratomtypepair 4 &&'), None, 'FAIL', '17 values',
         '&& — the left & stays a token (an earlier material check counts 17 values)'),
        ('continuation_then_blank_line', '_d2_text_form', {},
         rep('coefficientFriction peratomtypepair 4 &\n', 'coefficientFriction peratomtypepair 4 &\n\n'), None, 'FAIL', None,
         'blank line ends the command early (matrix values missing) — rejected'),
        ('amp_only_line', '_d2_text_form', {}, rep('    0.9 0.9 0.9 0.9 &\n', '    0.9 0.9 0.9 0.9 &\n &\n', 1), None, 'FAIL', CONT,
         'continuation line with no command text'),
        ('missing_final_newline', '_d2_text_form', {}, lambda s: s[:-1], None, 'FAIL', EOL, 'generator output ends with LF'),
        ('nul_after_final_newline', '_d2_text_form', {}, lambda s: s + '\x00', None, 'FAIL', 'unsupported command',
         'not ending with LF (an earlier check rejects the NUL token as a command first)'),
        # ── layout that stays free (both parsers read the same tokens · documented scope) ────────────────────
        ('blank_lines_added', 'layout', {}, rep('newton          off\n', 'newton          off\n\n\n'), None, 'PASS', None, 'blank lines'),
        ('comment_lines_added', 'layout', {}, rep('newton          off\n', 'newton          off\n# extra note\n# 추가 메모 · 설명\n'), None, 'PASS',
         None, 'comment lines (text free)'),
        ('nbsp_in_comment_middle', 'layout', {}, rep('# 믹싱 드럼', '# 믹싱 드럼'), None, 'PASS', None, 'comment text (not at an & end)'),
        ('line_separator_in_comment', 'layout', {}, rep('# 믹싱 드럼', '# 믹싱 드럼'), None, 'PASS', None,
         'U+2028 in a comment — neither parser ends the line there'),
        ('leading_spaces_on_command', 'layout', {}, rep('boundary        f f f', '   boundary        f f f'), None, 'PASS', None,
         'same tokens for both parsers'),
        ('single_space_layout', 'layout', {}, rep('atom_style      granular', 'atom_style granular'), None, 'PASS', None, 'spacing between tokens'),
        ('trailing_spaces_on_command', 'layout', {}, sub(r'^(run \d+)$', r'\1   '), None, 'PASS', None, 'trailing ASCII spaces (no &)'),
        ('trailing_comment_on_command', 'layout', {}, rep('boundary        f f f', 'boundary        f f f   # 설명 · note'), None, 'PASS', None,
         'comment after a command'),
        ('double_final_newline', 'layout', {}, lambda s: s + '\n', None, 'PASS', None, 'one more blank line'),
        # ── _d2_generator_form: the one free slot (neighbor skin value) ─────────────────────────────────────
        ('skin_nan', '_d2_generator_form', {}, sub(r'^(neighbor\s+)\S+ bin$', r'\g<1>nan bin'), None, 'FAIL', 'neighbor skin', 'nonfinite'),
        ('skin_inf', '_d2_generator_form', {}, sub(r'^(neighbor\s+)\S+ bin$', r'\g<1>inf bin'), None, 'FAIL', 'neighbor skin', 'nonfinite'),
        ('skin_empty', '_d2_generator_form', {}, sub(r'^(neighbor\s+)\S+ bin$', r'\g<1>bin'), None, 'FAIL', 'neighbor skin', 'missing value'),
        ('skin_zero', '_d2_generator_form', {}, sub(r'^(neighbor\s+)\S+ bin$', r'\g<1>0 bin'), None, 'FAIL', 'neighbor skin', 'not positive'),
        ('skin_negative', '_d2_generator_form', {}, sub(r'^(neighbor\s+)\S+ bin$', r'\g<1>-7.57e-05 bin'), None, 'FAIL', 'neighbor skin', 'negative'),
        ('skin_extra_token', '_d2_generator_form', {}, sub(r'^(neighbor\s+\S+ bin)$', r'\1 2'), None, 'FAIL', tok(3, '2', '(end)'), 'extra token'),
        ('skin_same_value_spelling', '_d2_generator_form', {}, sub(r'^(neighbor\s+)7\.57e-05 bin$', r'\g<1>0.0000757 bin'), None, 'PASS', None,
         'FREE SLOT (documented exception): the skin value is not pinned (single-deck contract outside · the pair compares tokens)'),
        ('skin_value_x1.1', '_d2_generator_form', {}, sub(r'^(neighbor\s+)7\.57e-05 bin$', r'\g<1>8.327000000000001e-05 bin'), None, 'PASS', None,
         'FREE SLOT — existing test_actual_command_scope requires single-deck PASS'),
        # ── _d2_generator_form: NaN / inf / Unicode / duplicates / order in pinned slots ─────────────────────
        ('box_nan', '_d2_generator_form', {}, rep('region          reg block -0.0144707', 'region          reg block nan'), None, 'FAIL', None, 'nonfinite'),
        ('mesh_scale_inf', '_d2_generator_form', {}, rep('scale 0.0251665', 'scale inf', -1), None, 'FAIL', None, 'nonfinite'),
        ('ced_diagonal_exponent_spelling', '_d2_generator_form', {},
         sub(r'^(fix mC [^\n]*\n    )(\d+)( )', r'\g<1>\g<2>.0\3', 1), None, 'FAIL', GF, 'same CED value, non-generator spelling (diagonal)'),
        ('material_unicode_digit', '_d2_generator_form', {}, t._friction_values('０.9'), None, 'FAIL', None, 'Unicode digit'),
        ('material_exponent_spelling', '_d2_generator_form', {}, t._friction_values('9e-1'), None, 'FAIL', tok(7, '9e-1', '0.9'),
         'same float 0.9 — generator writes 0.9'),
        ('dist_b_seed_same_as_a', '_d2_generator_form', {}, rep('particledistribution/discrete 32452883', 'particledistribution/discrete 32452867'),
         None, 'FAIL', tok(4, '32452867', '32452883'), 'duplicate RNG seed'),
        ('insert_b_seed_same_as_a', '_d2_generator_form', {}, sub(r'(fix insB all insert/pack seed )\d+', r'\g<1>32452843'), None, 'FAIL',
         tok(5, '32452843', '32452867'), 'duplicate RNG seed'),
        ('compute_duplicated', '_d2_generator_form', {}, rep('compute rke all erotate/sphere\n', 'compute rke all erotate/sphere\n' * 2), None, 'FAIL',
         tok(0, 'compute', 'thermo_style'), 'duplicate command'),
        ('thermo_modify_removed', '_d2_generator_form', {}, rep('thermo_modify lost ignore norm no\n', ''), None, 'FAIL',
         tok(0, 'shell', 'thermo_modify'), 'missing command'),
        ('command_appended_at_end', '_d2_generator_form', {}, lambda s: s + 'compute kx all ke\n', None, 'FAIL', 'command count',
         'extra command after the last run'),
        ('front_period_exp_spelling', '_d2_generator_form', {}, sub(r'(fix mvF[^\n]* period )0\.782508', r'\g<1>7.82508e-1'), None, 'FAIL',
         tok(16, '7.82508e-1', '0.782508'), 'same float as Drum — not the generator spelling (MXD2R-04 changed this row from PASS)'),
        ('origin_spelling', '_d2_generator_form', {}, rep('origin 0 0 0', 'origin 0.0 0 0', -1), None, 'FAIL', tok(8, '0.0', '0'), 'same value'),
        # ── metadata coordinated with the deck (hash rebinding alone would not change these) ───────────────
        ('seed_composite', '_d2_generator_form', {}, *seed_edit(32452845), 'FAIL', 'prime', 'composite seed in deck and metadata'),
        ('seed_prime_over_int32', '_d2_generator_form', {}, *seed_edit(big_prime), 'FAIL', 'prime', f'prime {big_prime} > 2^31−1'),
        ('dt_k1_exponent_unpadded', '_d2_generator_form', {}, *dt_edit(lambda o: o.replace('e-07', 'e-7')), 'FAIL', GF,
         'same dt, generator writes 2.373e-07 (metadata deck_txt changed too)'),
        ('dt_k1_plus_sign', '_d2_generator_form', {}, *dt_edit(lambda o: '+' + o), 'FAIL', GF, 'same dt with + sign'),
        ('dt_k2_padded', '_d2_generator_form', dict(dt_factor=.5), *dt_edit(lambda o: o.replace('e', '0e', 1)), 'FAIL', GF, 'k = 2 spelling'),
        ('dt_k3_padded', '_d2_generator_form', dict(dt_factor=1 / 3), *dt_edit(lambda o: o.replace('e', '0e', 1)), 'FAIL', GF, 'k = 3 spelling'),
        ('settle_steps_not_multiple_of_k', '_d2_generator_form', dict(dt_factor=.5), *steps_edit(fill_delta=1), 'FAIL', 'k × the generator plan',
         'settle steps +1 with every metadata time field consistent'),
        ('dump_interval_off_rule', '_d2_generator_form', {}, *steps_edit(dump_new=33000), 'FAIL', tok(4, '33000', '32976'),
         'dump interval off the generator rule (metadata consistent)'),
        ('restart_interval_off_rule', '_d2_generator_form', {}, *steps_edit(restart_new=150000), 'FAIL', tok(1, '150000', '200000'),
         'checkpoint interval off the generator rule (metadata consistent)'),
        # ── full-precision dump (--dump-full-precision · metadata dump_modify_format) ────────────────────────
        ('dpf_exact', 'dump_modify line', DPF, lambda s: s + '', None, 'PASS', None, 'generator output with the one quoted line'),
        ('dpf_double_space', 'dump_modify line', DPF, rep(dpf_line, dpf_line.replace('dmp format', 'dmp  format')), None, 'FAIL', ASCII,
         'the quoted line must match exactly'),
        ('dpf_trailing_comment', 'dump_modify line', DPF, rep(dpf_line, dpf_line + ' # x'), None, 'FAIL', ASCII, 'exact line only'),
        ('dpf_meta_format_mismatch', 'dump_modify line', DPF, lambda s: s + '', set_meta(('dump_modify_format',), FMT.replace('%.17g', '%.16g')),
         'FAIL', 'metadata dump_modify_format', 'metadata claims another format than the generator line'),
        ('dpf_meta_and_line_changed', 'dump_modify line', DPF, rep(dpf_line, dpf_line.replace('%.17g', '%.16g')),
         set_meta(('dump_modify_format',), FMT.replace('%.17g', '%.16g')), 'FAIL', 'metadata dump_modify_format', 'both changed together'),
        ('dpf_line_missing', 'dump_modify line', DPF, rep(dpf_line + '\n', ''), None, 'FAIL', tok(0, 'run', 'dump_modify'),
         'metadata declares the line, deck lacks it'),
        ('dpf_line_duplicated', 'dump_modify line', DPF, rep(dpf_line + '\n', (dpf_line + '\n') * 2), None, 'FAIL', tok(0, 'dump_modify', 'run'),
         'duplicate'),
        ('dpf_meta_removed', 'dump_modify line', DPF, lambda s: s + '', lambda meta, d: meta.pop('dump_modify_format'), 'FAIL', ASCII,
         'quoted line without the metadata declaration'),
    ]
    rows = []
    for name, func, kw, transform, meta_edit, expect, reason, why in cases:
        (a0, am0, _), (b0, bm0, _) = fixture(**kw)
        a, b = transform(a0), transform(b0)
        assert (a != a0 and b != b0) or meta_edit is not None or name == 'dpf_exact', name
        ma, mb = t.rebound(a, am0), t.rebound(b, bm0)
        if meta_edit is not None:
            meta_edit(ma, a)
            meta_edit(mb, b)
        res = {'readback': rb.read_d2(a, ma), 'pair': t.dd.diff_d2_decks(a, b, ma, mb), 'plan': t.smoke.d2_plan_check(a, ma)}
        got = {k: v['verdict'] for k, v in res.items()}
        first = (res['readback']['failures'] or [''])[0]
        right = reason is None or any(reason in f for f in res['readback']['failures'])
        rows.append(dict(case=name, attacks=func, fixture=kw and {k: str(v) for k, v in kw.items()}, expect=expect, verdicts=got,
                         reason=reason, right_reason=right, ok=all(v == expect for v in got.values()) and (expect == 'PASS' or right),
                         first_failure=first[:240], semantics=why))
    # ── byte-level inputs (read_d2 with the physical bytes) ──────────────────────────────────────────────
    (a0, am0, _), _ = fixture()
    raw = a0.encode('utf-8')

    def meta_for(data):
        m = copy.deepcopy(am0)
        m['deck_sha256'] = hashlib.sha256(data).hexdigest()
        m['deck_bytes'] = len(data)
        return m
    byte_cases = [
        ('bytes_lf', raw, 'PASS', None, 'generator bytes'),
        ('bytes_nbsp_continuation', raw.replace('neigh_modify    delay 0\n'.encode(),
                                                'neigh_modify    delay 0\n# note & \nneigh_modify exclude type 3 3\n'.encode(), 1),
         'FAIL', CONT, 'C2 A0 after & — ASCII-whitespace reader does not continue'),
        ('bytes_nul_in_comment', raw.replace('# 믹싱'.encode(), '#\x00 믹싱'.encode(), 1), 'FAIL', CTRL, 'NUL byte'),
        ('bytes_overlong_nul', raw + b'# \xc0\x80\n', 'FAIL', 'UTF-8', 'overlong NUL (invalid UTF-8 — strict decode)'),
        ('bytes_crlf', raw.replace(b'\n', b'\r\n'), 'FAIL', 'CR', 'CRLF (MXD2R-03 rule first)'),
        ('bytes_bom', b'\xef\xbb\xbf' + raw, 'FAIL', None, 'UTF-8 BOM'),
        ('bytes_tab', raw.replace(b'boundary        f f f', b'boundary\tf f f', 1), 'FAIL', CTRL, 'TAB byte'),
    ]
    for name, data, expect, reason, why in byte_cases:
        verdict = rb.read_d2(data, meta_for(data))
        right = reason is None or any(reason in f for f in verdict['failures'])
        rows.append(dict(case=name, attacks='read_d2 (bytes)', fixture=None, expect=expect, verdicts={'readback': verdict['verdict']},
                         reason=reason, right_reason=right, ok=verdict['verdict'] == expect and (expect == 'PASS' or right),
                         first_failure=(verdict['failures'] or [''])[0][:240], semantics=why))
    report = dict(tool='preattack_probe_v2.py', python=sys.version.split()[0], n=len(rows), n_ok=sum(r['ok'] for r in rows), rows=rows)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
        f.write('\n')
    for r in rows:
        print(('ok  ' if r['ok'] else 'GAP ') + r['case'].ljust(34) + ' expect ' + r['expect'] + ' got ' + str(r['verdicts'])
              + ('' if r['right_reason'] else '  WRONG REASON: ' + r['first_failure'][:120]))
    print(f"{report['n_ok']}/{report['n']} as the guarantee requires")


if __name__ == '__main__':
    main(*sys.argv[1:])
