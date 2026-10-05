"""Small independent network probes; no source or production output writes."""
import ast
import contextlib
import importlib.util
import io
import json
import math
from pathlib import Path
import sys
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'source' / 'scripts'))
import network_conductivity as nc
import test_constriction_power_share as fixtures


def quiet(fn, *args, **kwargs):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args, **kwargs)


def not_percolating():
    atoms, contacts = fixtures.chain(range(21), 1.0)
    contacts = [c for c in contacts if c['id1'] != 10]
    result = quiet(nc.run_decomposition, atoms, contacts, [1], 1.0,
                   20.0, 10.0, 10.0, type_map={1: 'SE'},
                   contact_mode='hertzian', mode='ionic')
    keys = ('sigma_full', 'sigma_full_mScm', 'sigma_full_status',
            'percolating_fraction', 'boundary_rule',
            'constriction_power_share_ion_hertz',
            'constriction_power_share_ion_hertz_status')
    assert result['percolating_fraction'] == 0.0
    assert result['sigma_full_status'] == 'not_computed'
    return {k: result.get(k) for k in keys}


def independent_power():
    # Distinct bottom nodes: finite electrode resistances can change the path
    # current ratio even when electrode heat is excluded from the fraction.
    nodes = {i: {} for i in range(4)}
    edges = [fixtures.edge(0, 2, 1., 9.), fixtures.edge(1, 3, 1., 0.)]
    net = dict(nodes=nodes, edges=edges, bottom={0, 1}, top={2, 3},
               scale=1., plate_z=1., box_x=10., box_y=10.)
    G, sr, field = quiet(nc.solve_network, net, mode='full', return_field=True)
    actual, status = nc.constriction_power_share(field)
    # The exact producer electrode formula for these two edges.
    gb = max(100 * 1.1 / 4, 10 * 1., 1e-6)
    ra, rb = 10. + 2 / gb, 1. + 2 / gb
    ia, ib = (1 / ra) / (1 / ra + 1 / rb), (1 / rb) / (1 / ra + 1 / rb)
    expected = ia**2 * 9 / (ia**2 * 10 + ib**2)
    physical_heat = ia**2 * 10 + ib**2
    electrodes_heat = 2 / gb * (ia**2 + ib**2)
    assert math.isclose(actual, expected, rel_tol=1e-12)
    assert math.isclose(1 / G, physical_heat + electrodes_heat, rel_tol=1e-12)
    return dict(status=status, power_share_actual=actual, power_share_independent=expected,
                ideal_electrode_share=9/110,
                relative_to_ideal_percent=100*(actual/(9/110)-1),
                physical_edge_power=physical_heat, virtual_electrode_power=electrodes_heat,
                source_power_at_unit_current=1/G,
                electrode_fraction_of_total=electrodes_heat/(physical_heat+electrodes_heat))


def old_new():
    path = HERE / 'reference_network_eedada5d3.py'
    spec = importlib.util.spec_from_file_location('old_network_reference', path)
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    # Function AST identity substantiates the raw solve before field assembly.
    def fn_ast(path, name):
        t = ast.parse(path.read_text(encoding='utf-8'))
        f = next(x for x in t.body if isinstance(x, ast.FunctionDef) and x.name == name)
        return ast.dump(f, include_attributes=False)
    solve_identical = fn_ast(path, 'solve_network') == fn_ast(ROOT/'source/scripts/network_conductivity.py', 'solve_network')
    checks = []
    inputs = [('L0', range(21), 1., 20.), ('L1', np.arange(81)*.5, .4, 40.),
              ('L2', range(21), 1., 100.)]
    for label, zs, r, plate in inputs:
        atoms, contacts = fixtures.chain(zs, r)
        for cm in ('hertzian', 'physics'):
            if cm == 'physics' and (nc._film_area is None or old._film_area is None):
                checks.append(dict(fixture=label, mode=cm, status='SKIPPED_MISSING_PLASTIC_DEPENDENCY'))
                continue
            args = (atoms, contacts, [1], 1., plate, 10., 10., 2.)
            kw = dict(type_map={1:'SE'}, contact_mode=cm, mode='ionic')
            n0 = quiet(old.build_network, *args, **kw)
            n1 = quiet(nc.build_network, *args, **kw)
            for mode in ('full', 'bulk_only', 'constriction_only'):
                z0 = quiet(old.solve_network, n0, mode=mode)
                z1 = quiet(nc.solve_network, n1, mode=mode, return_field=True)[:2]
                identical = all((x == y and (x is None or float(x).hex() == float(y).hex())) for x,y in zip(z0,z1))
                assert identical
                checks.append(dict(fixture=label, contact_mode=cm, solve_mode=mode,
                                   boundaries_identical=n0['bottom']==n1['bottom'] and n0['top']==n1['top'],
                                   raw_output_hex_identical=identical,
                                   output_hex=[float(x).hex() if x is not None else None for x in z1]))
    return dict(solve_function_ast_identical=solve_identical, checks=checks)


if __name__ == '__main__':
    print(json.dumps(dict(not_percolating=not_percolating(), independent_power=independent_power(),
                          old_new=old_new()), indent=2))
