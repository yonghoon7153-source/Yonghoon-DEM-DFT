"""L214R-S05 header-only Jinja tests using synthetic dictionaries.

Requires a real jinja2 runtime; dependency absence is not an accepted skip.
No Flask, app, metrics loader, ledger, browser, or research file is imported.
"""
from html.parser import HTMLParser
import math
import os
from pathlib import Path
import unittest

from jinja2 import Environment


ROOT = Path(os.environ.get('LHS_BOUNDARY_SOURCE_ROOT', Path(__file__).resolve().parents[1]))
SOURCE = ROOT / 'webapp/templates/single.html'
MISSING = object()
BAD = (MISSING, None, '12.5', 'not_numeric', True, False, math.nan, math.inf, -math.inf)


class BadgeParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.badges = []
        self.active = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'span' and 'badge' in attrs.get('class', '').split():
            self.active = {'text': '', 'title': attrs.get('title', ''), 'class': attrs.get('class', '')}

    def handle_data(self, data):
        if self.active is not None:
            self.active['text'] += data

    def handle_endtag(self, tag):
        if tag == 'span' and self.active is not None:
            self.active['text'] = ' '.join(self.active['text'].split())
            self.badges.append(self.active)
            self.active = None


def fixture():
    return dict(case=dict(name='SYNTHETIC_CASE', mode='standard', scale=2, type_map=None),
        input_params=dict(box_x=5, box_y=6),
        metrics=dict(porosity=12.5, porosity_spheresum=13.5, porosity_union=14.25,
            overlap_fraction_pct=1.25, porosity_union_exact_pct=15.25,
            porosity_union_exact_se_pct=.125, thickness_mass_conserving_um=7.25,
            thickness_um=8.25, plate_z_source='mesh', porosity_bedtop_spheresum=16.25,
            bed_top_um=9.25, headspace_um=1.5, porosity_bedtop_union_exact_pct=17.25,
            percolation_pct=81.25, ionic_active_pct=96.25, e_se_eff_gpa=2.25))


class SingleHeaderNumericBoundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = SOURCE.read_text(encoding='utf-8')
        begin = source.index('<div class="page-header">')
        start = source.index('<p>', begin) + len('<p>')
        end = source.index('</p>', start)
        # Exact source fragment, including every original attribute and guard.
        # Surrounding app/ledger/template inheritance is deliberately not loaded.
        cls.template = Environment(autoescape=True).from_string(source[start:end])

    def render(self, context):
        parser = BadgeParser()
        parser.feed(self.template.render(**context))
        return parser.badges

    def matching(self, badges, label):
        return [b for b in badges if b['text'].startswith(label)]

    def set_value(self, mapping, key, value):
        if value is MISSING:
            mapping.pop(key, None)
        else:
            mapping[key] = value

    def test_01_normal_numeric_badge_text_precision_and_units(self):
        badges = self.render(fixture())
        texts = [b['text'] for b in badges]
        for expected in ('RVE: 10×12μm', 'Porosity ε_sphere: 13.5%',
                         'ε_union 쌍 렌즈: 14.2%', 'overlap: 1.25%',
                         '두께 질량 보존: 7.25 μm', '두께 (판 간격): 8.2μm', 'Percolation: 81.2%',
                         'Ionic Active: 96.2%'):
            self.assertIn(expected, texts)
        self.assertTrue(self.matching(badges, 'E_SE:')[0]['text'].startswith('E_SE: 2.25 GPa'))
        self.assertTrue(any(t.startswith('ε_union 정확 (MC): 15.25') for t in texts))
        self.assertEqual(self.matching(badges, 'Ionic Active:')[0]['class'], 'badge badge-standard')

    def test_02_each_primary_numeric_badge_omits_unusable_value(self):
        fields = {'porosity_union': 'ε_union 쌍 렌즈:', 'overlap_fraction_pct': 'overlap:',
            'porosity_union_exact_pct': 'ε_union 정확 (MC):',
            'thickness_mass_conserving_um': '두께 질량 보존:',
            'thickness_um': '두께 (판 간격):',
            'percolation_pct': 'Percolation:', 'ionic_active_pct': 'Ionic Active:',
            'e_se_eff_gpa': 'E_SE:'}
        for field, label in fields.items():
            for value in BAD:
                with self.subTest(field=field, value=repr(value)):
                    context = fixture()
                    self.set_value(context['metrics'], field, value)
                    badges = self.render(context)
                    self.assertEqual(self.matching(badges, label), [])
                    if field != 'percolation_pct':
                        self.assertEqual(len(self.matching(badges, 'Percolation:')), 1)

    def test_03_porosity_fallback_requires_a_real_numeric_source(self):
        for value in BAD:
            with self.subTest(value=repr(value)):
                context = fixture()
                self.set_value(context['metrics'], 'porosity_spheresum', value)
                self.assertEqual(self.matching(self.render(context), 'Porosity ε_sphere:')[0]['text'],
                                 'Porosity ε_sphere: 12.5%')
                self.set_value(context['metrics'], 'porosity', value)
                self.assertEqual(self.matching(self.render(context), 'Porosity ε_sphere:'), [])
        context = fixture()
        del context['metrics']['porosity']
        selected = self.matching(self.render(context), 'Porosity ε_sphere:')
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0]['text'],
                         'Porosity ε_sphere: 13.5%')

    def test_04_rve_requires_both_dimensions_and_numeric_scale(self):
        for owner, key in (('input_params', 'box_x'), ('input_params', 'box_y'), ('case', 'scale')):
            for value in BAD:
                with self.subTest(owner=owner, key=key, value=repr(value)):
                    context = fixture()
                    self.set_value(context[owner], key, value)
                    self.assertEqual(self.matching(self.render(context), 'RVE:'), [])

    def test_05_optional_uncertainty_does_not_destroy_valid_estimate(self):
        for value in BAD:
            context = fixture()
            self.set_value(context['metrics'], 'porosity_union_exact_se_pct', value)
            with self.subTest(value=repr(value)):
                badges = self.matching(self.render(context), 'ε_union 정확 (MC):')
                self.assertEqual(len(badges), 1)
                self.assertNotIn('±', badges[0]['text'])

    def test_06_bedtop_tooltip_dependencies_are_guarded_together(self):
        for field in ('porosity_bedtop_spheresum', 'bed_top_um', 'headspace_um'):
            for value in BAD:
                with self.subTest(field=field, value=repr(value)):
                    context = fixture()
                    self.set_value(context['metrics'], field, value)
                    self.assertEqual(self.matching(self.render(context), '입자 윗면 기준 ε_sphere:'), [])

    def test_07_optional_bedtop_union_is_not_coerced(self):
        for value in BAD:
            context = fixture()
            self.set_value(context['metrics'], 'porosity_bedtop_union_exact_pct', value)
            with self.subTest(value=repr(value)):
                badges = self.matching(self.render(context), '입자 윗면 기준 ε_sphere:')
                self.assertEqual(len(badges), 1)
                self.assertNotIn('ε_union 정확:', badges[0]['text'])

    def test_08_valid_zero_is_not_missing_and_ionic_threshold_is_unchanged(self):
        context = fixture()
        for key in ('percolation_pct', 'ionic_active_pct', 'e_se_eff_gpa'):
            context['metrics'][key] = 0
        badges = self.render(context)
        self.assertEqual(self.matching(badges, 'Percolation:')[0]['text'], 'Percolation: 0.0%')
        self.assertTrue(self.matching(badges, 'E_SE:')[0]['text'].startswith('E_SE: 0.00 GPa'))
        self.assertEqual(self.matching(badges, 'Ionic Active:')[0]['class'], 'badge badge-bimodal')
        context['metrics']['ionic_active_pct'] = 95
        self.assertEqual(self.matching(self.render(context), 'Ionic Active:')[0]['class'], 'badge badge-standard')

    def test_09_empty_metrics_do_not_create_numeric_badges(self):
        for metrics in ({}, None):
            context = fixture()
            context['metrics'] = metrics
            badges = self.render(context)
            for prefix in ('RVE:', 'Porosity ε_sphere:', 'Percolation:', 'Ionic Active:', 'E_SE:'):
                self.assertEqual(self.matching(badges, prefix), [])

    def test_10_estimated_thickness_keeps_warning_only_for_numeric_value(self):
        context = fixture()
        context['metrics']['plate_z_source'] = 'estimated_center'
        badge = self.matching(self.render(context), '두께 ⚠ 추정 (판 간격):')[0]
        self.assertEqual(badge['text'], '두께 ⚠ 추정 (판 간격): 8.2μm')
        self.assertIn('badge-warning', badge['class'])
        for value in BAD:
            self.set_value(context['metrics'], 'thickness_um', value)
            with self.subTest(value=repr(value)):
                self.assertEqual(self.matching(self.render(context), '두께 ⚠ 추정 (판 간격):'), [])

    def test_11_finite_operands_with_overflowing_scale_product_are_not_formatted(self):
        for key in ('box_x', 'box_y'):
            context = fixture()
            context['input_params'][key] = 1e308
            context['case']['scale'] = 1e6
            with self.subTest(key=key):
                self.assertEqual(self.matching(self.render(context), 'RVE:'), [])
        for key in ('percolation_pct', 'thickness_um', 'e_se_eff_gpa'):
            context = fixture()
            context['metrics'][key] = 10**400
            with self.subTest(key=key):
                badges = self.render(context)
                prefix = {'percolation_pct': 'Percolation:', 'thickness_um': '두께 (판 간격):',
                          'e_se_eff_gpa': 'E_SE:'}[key]
                self.assertEqual(self.matching(badges, prefix), [])

    def test_12_large_representable_values_have_no_scientific_cutoff(self):
        for value in (1e308, -1e308):
            context = fixture()
            context['metrics']['percolation_pct'] = value
            with self.subTest(value=value):
                badge = self.matching(self.render(context), 'Percolation:')
                self.assertEqual(len(badge), 1)
                self.assertNotIn('inf', badge[0]['text'].lower())
                self.assertNotIn('nan', badge[0]['text'].lower())


if __name__ == '__main__':
    unittest.main()
