#!/usr/bin/env python3
import importlib.util, sys
spec = importlib.util.spec_from_file_location('tb3', sys.argv[1]); tb = importlib.util.module_from_spec(spec); spec.loader.exec_module(tb)
K=tb.KGY; c=tb.comp(K)
one_lad = 2*tb.LADDER_ARMS*c['arm_s'] + tb.ORIGINS*c['build_s']
print('one-machine ladders h', tb.h(one_lad))
print('predict stage kgy h', tb.h(tb.units_on(K,12,0)), tb.h(tb.units_on(K,12,1)))
print('first unit extra h', tb.h(3*c['build_d']))
cs=tb.comp(K, r_mode='solve')
print('solve unit kgy', tb.h(tb.unit_hit(K,0,r_mode='solve')), tb.h(tb.unit_hit(K,1,r_mode='solve')))
print('old-gen SBE iters est', 704/3054*30000, 'ratio lo', 30000/(704/3054*30000), 'hi', 60000/(704/3054*30000))
print('x2', 2*60000/(704/3054*30000), '5M margin', (5e6/277885)/(2*60000/(704/3054*30000)), '6M', (6e6/277885)/(2*60000/(704/3054*30000)), '4M x', (4e6/277885)/(60000/(704/3054*30000)))
print('2pan post ratios', 48.1/582.7, 48.1/495.9, 136.3/641.8, 136.3/555.1, '3pan', 48.0/177.7, 48.0/153.2, 136.1/208.7, 136.1/184.2)
print('a2/a3 per iter', (13245/277885)/(2914/277885), (13245/277885)/(2913/277885))
print('shares', 925/3838, 925/4932, 84485/277885)
print('a3-a4 split diff gap/post', 40-0, 459-378)
