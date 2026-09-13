"""Arithmetic and logical countermodels for MICROSHORT_MPH_REVIEW.

No COMSOL execution and no original MPH/XML/XLSX is read. All constants below
come from REQ_MPH_MICROSHORT.md; missing original inputs remain unverified.
Run: python mph_review_checks.py
"""
import json
import math
import re
import xml.etree.ElementTree as ET


def linear(x, x0, y0, x1, y1):
    assert x0 <= x <= x1
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def main():
    dn, dp = 0.97427802, 0.97036018
    ln, lp = 0.0257219788, 0.0296398242
    xn, xp = 0.01172068149, 0.92406389
    un0 = linear(xn, .008183898, .56533, .016367829, .445258)
    un1 = linear(xn / dn, .008183898, .56533, .016367829, .445258)
    up0 = linear(xp, .916363636, 3.57093827, .924545455, 3.56548357)
    up1 = linear(xp / dp, .949090909, 3.54922689, .957272727, 3.54350457)
    bn = .63122 * 52e-6 * 31507
    bp = .58803 * 44e-6 * 50707.7
    nn = bn * (1-ln) * xn
    np_ = bp * (1-lp) * xp
    n0 = bn * xn + bp * .927
    target = nn + np_
    scaled_init_total = nn * dn + np_ * dp
    factor = .45 ** 1.5
    area, thickness, voltage = 1.53938e-4, 25e-6, 4.
    qarea = bp * (.927-.215) * 96485.33212 / 3600
    current_01c = qarea * area * .1
    leakage = []
    for sigma in [1e-20, 1.4e-6, 4.67e-6, 1.4e-5]:
        resistance = thickness / (area * factor * sigma)
        leakage.append({'sigma_S_per_m': sigma, 'R_ohm': resistance,
                        'I_at_4V_A': voltage/resistance,
                        'fraction_of_01C': voltage/resistance/current_01c})

    # The supplied regex stops a parent at the first child's closing tag.
    xml = '''<Root><PhysicsFeature op="PorousElectrode" tag="pce1" name="parent">
<PhysicsFeature op="ParticleIntercalation" tag="pin1" name="disabled child">
<entityFlags T="51">DISABLED</entityFlags><param T="33" param="csinit" value="child_init"/>
</PhysicsFeature><param T="33" param="epss" value="parent_eps"/>
</PhysicsFeature></Root>'''
    flat = []
    for m in re.finditer(r'<PhysicsFeature op="([^"]+)" tag="([^"]+)" name="([^"]*)"', xml):
        block = xml[m.start():xml.find('</PhysicsFeature>', m.start())]
        flag = re.search(r'<entityFlags T="51">([^<]*)</entityFlags>', block)
        flat.append({'tag':m.group(2), 'reported_disabled': bool(flag and 'DISABLED' in flag.group(1)),
                     'reported_params': re.findall(r'param="([^"]+)" value="([^"]*)"', block)})
    parent = ET.fromstring(xml).find('PhysicsFeature')
    actual = {'tag':parent.get('tag'), 'own_disabled':parent.find('entityFlags') is not None,
              'own_params':[(p.get('param'),p.get('value')) for p in parent.findall('param')]}

    # A no-short, finite relaxation mode persists into the proposed late window.
    relaxation = [{'t_h':t, 'voltage_excess_mV':20*math.exp(-t/10),
                   'slope_mV_per_h':-2*math.exp(-t/10)} for t in [4,6,8,12]]
    output = {
      'scope':'Analytic checks only; no COMSOL or original private data execution',
      'M1':{'soc_ne':xn/dn, 'soc_pe':xp/dp, 'ne_ocp_delta_mV':1000*(un1-un0),
            'pe_ocp_delta_mV':1000*(up1-up0), 'cell_ocp_nominal_V':up0-un0,
            'cell_ocp_rescaled_V':up1-un1, 'cell_delta_mV':1000*((up1-un1)-(up0-un0)),
            'lost_host_fraction_ne':1-(1-ln)*dn,'lost_host_fraction_pe':1-(1-lp)*dp,
            'both_occupancies_admissible':0<xn/dn<1 and 0<xp/dp<1,
            'nLi0_mol_per_m2':n0,'nLi_target_conditional_mol_per_m2':target,
            'implied_dLi_mol_per_m2':n0-target,
            'extra_Li_removed_if_only_csinit_multiplied_by_dm_mol_per_m2':target-scaled_init_total,
            'extra_Li_removed_percent_of_target':100*(target-scaled_init_total)/target,
            'xp_independently_reproduced':False,
            'xp_missing_inputs':['LLI','C_lit0_ref1','original XML parameter evaluation']},
      'M2':{'bruggeman_factor_if_b_1_5':factor,'inverse_factor':1/factor,
            'literal_epss_plus_epsl_after_recommendation':1+.45,
            'qarea_Ah_per_m2':qarea,'leakage':leakage},
      'Q5_countermodels':{'no_short_relaxation':relaxation,
          'same_conductance_slope_ratio_if_Cdiff_halves':2.,
          'same_short_repeated_cycles':'same nonzero slope with unchanged initial state and conductance',
          'tau_claim_units':'(Ah)*V/A = V*h, not h',
          'local_voltage_tau_units':'(Ah/V)*V/A = h',
          'charge_depletion_time_units':'Ah/A = h'},
      'regex_countermodel':{'reported':flat,'direct_xml_parent':actual},
      'rails_logical_countermodel':{'x_cell':.9,'a_PE_ratio':1.,'a_NE_ratio':1.,
          'c_lit_ratio':.98,'LAM_PE':.1,'LAM_NE':.1,'LLI':.02},
      'allclose_tolerance_countermodel':{'a':.1,'b':.1000009,
          'abs_error':abs(.1-.1000009),
          'numpy_default_rule_accepts':abs(.1-.1000009)<=1e-8+1e-5*abs(.1000009),
          'machine_epsilon':2.220446049250313e-16}
    }
    print(json.dumps(output,indent=2,ensure_ascii=False))


if __name__ == '__main__':
    main()
