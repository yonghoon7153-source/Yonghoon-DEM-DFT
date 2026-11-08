#!/usr/bin/env python3
"""D2 development consumer regressions; synthetic decks only, no simulator.

MXD2R-01 · 02 · 03 (Codex 10-27 재검토 HOLD · 수정 계획 docs/reviews/mxd2r_fix_plan_20261030.md · 1저자 11-02 Q1–Q3 (가)):
반례를 고치기 **전에** 옮겼다 — 고치기 전 소비자는 아래 공통 변조 · CRLF 바이트를 세 소비자 모두 PASS / rc 0 으로 받았다.
MXD2R-04 (11-03 사전 공격 · 1저자 11-03 Q1 = 권고대로): 범위 밖 공통 변조 17 · 같은 부류 (같은 값 다른 표기 · 이름 · 순서 · 중복 ·
결손 · 배플) · 문자 꼴 (우리 파서와 LIGGGHTS 가 다른 토큰을 읽을 수 있는 꼴) 도 고치기 **전에** 옮겼다 (고치기 전 세 소비자 PASS).
"""
import copy
import hashlib
import inspect
import itertools
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_mixer_deck as gen
import mixer_deck_readback as rb
import mixer_deck_diff as dd
import mixer_smoke_blind as smoke


def fixture(phases=('AM_P', 'AM_S', 'SE'), generation='lab20261014', stiff=20., rho=.3,
            coated=False, bo=.73, n=100000, cgf=151.4, layered=True, seed=32452843, dt_factor=1.,
            dump_full_precision=False, fr=None):
    old = gen.TYPES
    try:
        gen.set_phases(phases)
        gamma = {p: 1. if coated or p == 'SE' else rho for p in phases}
        arm = gen.gm_arm(gamma, gamma_wall=gen.gm_wall_from_ncm(rho), bo_se=bo,
                         rho_uncoated_ncm=rho)
        arm['layered'] = layered
        gen.ARMS['D2CONSUMER'] = arm
        p = gen.plan(n, cgf=cgf, stiffen_se=stiff, dens_gen=generation)
        rpm = gen.resolve_rpm(p['R']) if fr is None else gen.resolve_rpm(p['R'], fr=fr)
        text = gen.deck(p, rpm, 2, seed=seed, arm='D2CONSUMER', hold_bo_pairwise=True, dt_factor=dt_factor,
                        dump_full_precision=dump_full_precision)
        meta = gen.deck_meta(p, rpm, 2, seed, 'D2CONSUMER', text, hold_bo_pairwise=True, dt_factor=dt_factor,
                             dump_full_precision=dump_full_precision)
        return text, meta, {str(i+1): int(p['n'][phase]) for i, phase in enumerate(phases)}
    finally:
        gen.ARMS.pop('D2CONSUMER', None)
        gen.set_phases(old)


def rebound(text, meta):
    meta = copy.deepcopy(meta)
    meta['deck_sha256'] = hashlib.sha256(text.encode()).hexdigest()
    meta['deck_bytes'] = len(text.encode())
    return meta


def rebound_bytes(raw, meta):
    """Metadata that states the given physical file bytes (MXD2R-03 'CRLF metadata' direction)."""
    meta = copy.deepcopy(meta)
    meta['deck_sha256'] = hashlib.sha256(raw).hexdigest()
    meta['deck_bytes'] = len(raw)
    return meta


def _block(fix_id, rows):
    """Remove `fix <id> …` and its `rows` continuation lines (Codex friction_missing form)."""
    return lambda s: re.sub(r'(?m)^fix ' + fix_id + r' [^\n]*\n(?:    [^\n]*\n){' + str(rows) + '}', '', s)


def _move_after(pattern, anchor):
    """Move the lines matched by `pattern` (multi-line allowed) to just after the line `anchor`."""
    def transform(s):
        m = re.search(pattern, s, flags=re.M)
        assert m, pattern
        s = s[:m.start()] + s[m.end():]
        a = re.search(r'(?m)^' + re.escape(anchor) + r'\n', s)
        assert a, anchor
        return s[:a.end()] + m.group(0) + s[a.end():]
    return transform


def _friction_values(new):
    def transform(s):
        m = re.search(r'(?m)^fix m4 [^\n]*\n(?:    [^\n]*\n){4}', s)
        return s[:m.start()] + m.group(0).replace('0.9', new) + s[m.end():]
    return transform


#: Codex d2/evidence/independent_probe.py 의 공통 변조 여섯 — 식 그대로 · 두 덱에 같이 · 메타 해시 · 길이 재결합.
#: 값 = (변조, 고친 뒤 거부 사유에 있어야 할 문구 — 다른 사유로 우연히 거부된 것이 아님을 확인한다)
CODEX_COMMON_MODE = {
    'run_upto': (lambda s: re.sub(r'(?m)^run (\d+)$', r'run \1 upto', s), 'run <integer>'),
    'late_timestep': (lambda s: re.sub(r'(?m)^timestep[^\n]*\n', '', s)
                      + re.search(r'(?m)^timestep[^\n]*', s).group(0) + '\n', 'timestep <dt>'),
    'insert_start_late': (lambda s: s.replace('insert_every once', 'insert_every once start 9000000'),
                          'insert/pack must be the generator form'),
    'front_period': (lambda s: re.sub(r'(fix mvF[^\n]* period )[^\s]+', r'\g<1>0.1', s), 'Drum period'),
    'exclude_SE_SE': (lambda s: s.replace('neigh_modify    delay 0', 'neigh_modify    delay 0\nneigh_modify exclude type 3 3'),
                      '`neigh_modify delay 0`'),
    'friction_missing': (lambda s: re.sub(r'(?m)^fix m4[^\n]*\n(?:    [^\n]*\n){4}', '', s), 'coefficientFriction'),
}

#: 같은 부류 (생성기 문법 밖 · 고치기 전 세 소비자 PASS) — Codex 여섯 밖의 변형으로 문법이 닫혔는지 본다 (API).
MXD2R01_SAME_CLASS = {
    'run_pre_post': (lambda s: re.sub(r'(?m)^run (\d+)$', r'run \1 pre no post no', s), 'run <integer>'),
    'run_start_stop': (lambda s: re.sub(r'(?m)^run (\d+)$', r'run \1 start 0 stop 99999999', s), 'run <integer>'),
    'timestep_after_insert_run': (_move_after(r'^timestep[^\n]*\n', 'run 1'), 'timestep <dt>'),
    'timestep_extra_token': (lambda s: re.sub(r'(?m)^(timestep\s+\S+)$', r'\1 2.373e-07', s), 'timestep <dt>'),
    'insert_repeat_every': (lambda s: s.replace('insert_every once', 'insert_every 1000'), 'insert/pack must be the generator form'),
    'insert_start_first_step': (lambda s: s.replace('insert_every once', 'insert_every once start 1'),
                                'insert/pack must be the generator form'),
    'insert_velocity': (lambda s: s.replace('vel constant 0. 0. -0.2', 'vel constant 0. 0. -2.0'),
                        'insert/pack must be the generator form'),
    'back_period': (lambda s: re.sub(r'(fix mvB[^\n]* period )[^\s]+', r'\g<1>0.1', s), 'Drum period'),
}
MXD2R02_SAME_CLASS = {
    'exclude_AM_SE': (lambda s: s.replace('neigh_modify    delay 0', 'neigh_modify    delay 0\nneigh_modify exclude type 1 3'),
                      '`neigh_modify delay 0`'),
    'exclude_same_line': (lambda s: s.replace('neigh_modify    delay 0', 'neigh_modify    delay 0 exclude type 3 3'),
                          '`neigh_modify delay 0`'),
    'neigh_every_check_no': (lambda s: s.replace('neigh_modify    delay 0', 'neigh_modify    every 10 delay 0 check no'),
                             '`neigh_modify delay 0`'),
    'neigh_missing': (lambda s: s.replace('neigh_modify    delay 0\n', ''), '`neigh_modify delay 0`'),
    'restitution_missing': (_block('m3', 4), 'coefficientRestitution'),
    'rolling_missing': (_block('m5', 4), 'coefficientRollingFriction'),
    'charvel_missing': (lambda s: re.sub(r'(?m)^fix m9 [^\n]*\n', '', s), 'characteristicVelocity'),
    'friction_duplicate': (lambda s: s.replace('fix m5 all', 'fix m4b all property/global coefficientFriction peratomtypepair 4 &\n'
                                               + '    0.1 0.1 0.1 0.1 &\n' * 3 + '    0.1 0.1 0.1 0.1\nfix m5 all', 1), 'coefficientFriction'),
    # 사전 공격 변이 M11 생존 (11-03) — 값이 다른 중복은 상수 검사가 먼저 잡아 '중복' 규칙이 시험에 묶이지 않았다 → 같은 값 중복으로 묶는다
    'friction_duplicate_same_values': (lambda s: s.replace('fix m5 all', 'fix m4b all property/global coefficientFriction peratomtypepair 4 &\n'
                                                           + '    0.9 0.9 0.9 0.9 &\n' * 3 + '    0.9 0.9 0.9 0.9\nfix m5 all', 1),
                                       'defined more than once'),
    'friction_value': (_friction_values('0.1'), 'coefficientFriction'),
    'friction_after_pair_style': (_move_after(r'^fix m4 [^\n]*\n(?:    [^\n]*\n){4}', 'pair_coeff      * *'), 'coefficientFriction'),
    'unknown_property': (lambda s: s.replace('fix m9 all', 'fix mX all property/global coefficientRestitutionWall scalar 0.5\nfix m9 all', 1),
                         'unsupported material property'),
    'pair_style_late': (_move_after(r'^pair_style[^\n]*\npair_coeff[^\n]*\n', 'write_restart restart/settled.bin'), 'pair_coeff * *'),
    'pair_coeff_partial': (lambda s: s.replace('pair_coeff      * *', 'pair_coeff      1 1'), 'pair_coeff * *'),
}


def _tok(k, got, want):
    """MXD2R-04 거부 사유 문구 — 첫 어긋난 토큰 (명령 안 위치 · 덱 토큰 · 생성기 토큰)."""
    return f'token {k} `{got}` (generator `{want}`)'


def _swap(first, second):
    """정확히 한 번씩 있는 두 줄의 자리를 바꾼다 (순서만 다른 덱)."""
    def transform(s):
        assert s.count(first) == 1 and s.count(second) == 1, (first, second)
        return s.replace(first, '\0').replace(second, first).replace('\0', second)
    return transform


def _rep(old, new, count=1):
    return lambda s: s.replace(old, new, count)


#: 문자 꼴 사유 (MXD2R-04) — 우리 파서 (_logical: 유니코드 공백 · 첫 # · 유니코드 rstrip 뒤 '&') 와 LIGGGHTS (ASCII 공백 · 따옴표 안 # ·
#:   $ 치환 · C 문자열) 가 다른 토큰을 읽을 수 있는 꼴을 토큰 대조 **전에** 거부한다.
_CTRL, _ASCII = 'control character', 'printable ASCII without quotes or $'
_CONT, _EOL = "continuation must be a command line ending exactly in ' &'", 'must end with a newline'
#: MXD2R-04 — 사전 공격 (11-03) 이 보고한 MXD2R-01–03 범위 밖 공통 변조 17 (식 = docs/reviews/mxd2r_fix_evidence_20261103/tools/
#:   preattack_outside_scope.py 그대로) · 고치기 전 세 소비자 PASS.  값 = (변조, 고친 뒤 사유 = 첫 어긋난 토큰 ↔ 생성기 토큰 · 따옴표 = 문자 꼴)
MXD2R04_OUTSIDE_17 = {
    'boundary_periodic': (_rep('boundary        f f f', 'boundary        p p p'), _tok(1, 'p', 'f')),
    'newton_on': (_rep('newton          off', 'newton          on'), _tok(1, 'on', 'off')),
    'atom_style_sphere': (_rep('atom_style      granular', 'atom_style      sphere'), _tok(1, 'sphere', 'granular')),
    'communicate_cutoff': (_rep('communicate     single vel yes', 'communicate     single cutoff 0.001 vel yes'), _tok(2, 'cutoff', 'vel')),
    'hard_particles_no': (_rep('hard_particles  yes', 'hard_particles  no'), _tok(1, 'no', 'yes')),
    'atom_modify_sort': (_rep('atom_modify     map array sort 0 0', 'atom_modify     map array sort 1000 0.0'), _tok(4, '1000', '0')),
    'thermo_lost_error': (_rep('thermo_modify lost ignore norm no', 'thermo_modify lost error norm no'), _tok(2, 'error', 'ignore')),
    'neighbor_nsq': (lambda s: re.sub(r'(?m)^(neighbor\s+\S+) bin$', r'\1 nsq', s), _tok(2, 'nsq', 'bin')),
    'template_extra_option': (lambda s: re.sub(r'(?m)^(fix pt1 [^\n]*radius constant \S+)$', r'\1 volume_limit 1e-30', s),
                              _tok(13, 'volume_limit', '(end)')),
    'template_quote_hash': (lambda s: re.sub(r'(?m)^(fix pt1 [^\n]*radius constant \S+)$', r'\1 "#" volume_limit 1e-30', s), _ASCII),
    'pdd_seed': (_rep('particledistribution/discrete 32452867', 'particledistribution/discrete 15485863'), _tok(4, '15485863', '32452867')),
    'insert_b_seed': (lambda s: re.sub(r'(fix insB all insert/pack seed )\d+', r'\g<1>15485867', s), _tok(5, '15485867', '32452867')),
    'insert_region_geometry': (lambda s: re.sub(r'(region ins_reg cylinder x 0\.0 0\.0 )(\S+)', r'\g<1>0.0100000', s),
                               _tok(6, '0.0100000', '0.0113249')),
    'mesh_scale': (lambda s: s.replace('scale 0.0251665', 'scale 0.0250000'), _tok(9, '0.0250000', '0.0251665')),
    'dump_modify_added': (_rep('\n# ① 채우고 정착', '\ndump_modify dmp sort id\n# ① 채우고 정착'), _tok(0, 'dump_modify', 'run')),
    'thermo_every': (_rep('thermo 5000', 'thermo 1000'), _tok(1, '1000', '5000')),
    'write_restart_removed': (_rep('write_restart restart/settled.bin\n', ''), _tok(0, 'fix', 'write_restart')),
}
#: MXD2R-04 같은 부류 — 같은 값 다른 표기 · 생성기 이름 (fix · region · 메시 · dump · 템플릿 id) · 순서 · 중복 · 결손 · 생성기 옵션 밖 (배플) ·
#:   출력 · 체크포인트 · 이웃 skin 토큰 꼴 (고치기 전 세 소비자 PASS — 11-03 선별 기록 docs/reviews/mxd2r_fix_evidence_20261103/)
MXD2R04_SAME_CLASS = {
    'box_spelling': (_rep('0.0144707', '0.01447070', -1), _tok(3, '-0.01447070', '-0.0144707')),
    'box_size': (_rep('0.0144707', '0.0150000', -1), _tok(3, '-0.0150000', '-0.0144707')),
    'create_box_spelling': (_rep('create_box      4 reg', 'create_box      04 reg'), _tok(1, '04', '4')),
    'young_spelling': (_rep('1.037e+09 1.037e+09', '1.037e9 1.037e9'), _tok(6, '1.037e9', '1.037e+09')),
    'nu_spelling': (_rep('poissonsRatio peratomtype 0.25 0.25 0.30 0.30', 'poissonsRatio peratomtype 0.25 0.25 0.3 0.3'), _tok(8, '0.3', '0.30')),
    'restitution_spelling': (lambda s: re.sub(r'(?m)^(fix m3 [^\n]*\n(?:    [^\n]*\n){4})', lambda m: m.group(1).replace('0.3', '0.30'), s),
                             _tok(7, '0.30', '0.3')),
    'ced_spelling': (lambda s: re.sub(r'(?m)^(fix mC [^\n]*\n(?:    [^\n]*\n){3}    [^\n]* )0$', r'\g<1>0.0', s), _tok(22, '0.0', '0')),
    'charvel_spelling': (_rep('characteristicVelocity scalar 2.0', 'characteristicVelocity scalar 2'), _tok(6, '2', '2.0')),
    'gravity_spelling': (_rep('gravity 9.81 vector', 'gravity 9.810 vector'), _tok(4, '9.810', '9.81')),
    'gravity_vector_spelling': (_rep('vector 0.0 0.0 -1.0', 'vector 0 0 -1'), _tok(6, '0', '0.0')),
    'stl_name': (_rep('file Drum.stl', 'file drum.stl'), _tok(5, 'drum.stl', 'Drum.stl')),
    'mesh_type_spelling': (_rep('type 4 scale', 'type 04 scale', -1), _tok(7, '04', '4')),
    'density_decimal': (_rep('density constant 4850 radius constant 0.0006813', 'density constant 4850.0 radius constant 0.0006813'),
                        _tok(9, '4850.0', '4850')),
    'pdd_fraction_spelling': (_rep('pt1 0.700000', 'pt1 0.7000000'), _tok(7, '0.7000000', '0.700000')),
    'ins_hi_zlo': (lambda s: re.sub(r'(?m)^(region ins_hi block (?:\S+ ){4})\S+', r'\g<1>-0.00400000', s), _tok(7, '-0.00400000', '-0.00528143')),
    'thermo_exp_spelling': (_rep('thermo 5000', 'thermo 5e3'), _tok(1, '5e3', '5000')),
    'thermo_style_extra': (_rep('thermo_style custom step atoms ke c_rke vol', 'thermo_style custom step atoms ke c_rke vol press'),
                           _tok(7, 'press', '(end)')),
    'thermo_norm_yes': (_rep('thermo_modify lost ignore norm no', 'thermo_modify lost ignore norm yes'), _tok(4, 'yes', 'no')),
    'communicate_multi': (_rep('communicate     single vel yes', 'communicate     multi vel yes'), _tok(1, 'multi', 'single')),
    'atom_modify_hash': (_rep('atom_modify     map array sort 0 0', 'atom_modify     map hash sort 0 0'), _tok(2, 'hash', 'array')),
    'restart_spelling': (lambda s: re.sub(r'(?m)^restart (\d+) ', r'restart 0\1 ', s), _tok(1, '0200000', '200000')),
    'restart_files': (_rep('restart/a.bin restart/b.bin', 'restart/a.bin restart/a.bin'), _tok(3, 'restart/a.bin', 'restart/b.bin')),
    'write_restart_path': (_rep('write_restart restart/settled.bin', 'write_restart restart/s.bin'), _tok(1, 'restart/s.bin', 'restart/settled.bin')),
    'dump_every_spelling': (lambda s: re.sub(r'(?m)^(dump dmp all custom )(\d+)', r'\g<1>0\2', s), _tok(4, '032976', '32976')),
    'dump_path': (_rep('post/mix_*.liggghts', 'post/x_*.liggghts'), _tok(5, 'post/x_*.liggghts', 'post/mix_*.liggghts')),
    'dump_columns': (_rep('fx fy fz radius', 'fx fy fz'), _tok(17, '(end)', 'radius')),
    'move_axis_spelling': (_rep('axis 1. 0. 0.', 'axis 1.0 0.0 0.0', -1), _tok(12, '1.0', '1.')),
    'origin_spelling': (_rep('origin 0 0 0', 'origin 0.0 0 0', -1), _tok(8, '0.0', '0')),
    'period_spelling': (_rep('period 0.782508', 'period 0.7825080', -1), _tok(16, '0.7825080', '0.782508')),
    'fix_id_material': (_rep('fix m9 all property/global', 'fix m6 all property/global'), _tok(1, 'm6', 'm9')),
    'fix_id_walls': (_rep('fix walls all wall/gran', 'fix wall all wall/gran'), _tok(1, 'wall', 'walls')),
    'fix_id_integrator': (_rep('fix integrS all nve/sphere', 'fix integr all nve/sphere'), _tok(1, 'integr', 'integrS')),
    'template_id': (lambda s: s.replace('fix pt1 ', 'fix ptA ').replace('pt1 0.700000', 'ptA 0.700000'), _tok(1, 'ptA', 'pt1')),
    'region_id_rename': (lambda s: s.replace('region ins_reg ', 'region ins_cyl ').replace('region ins_reg particles_in_region',
                                                                                          'region ins_cyl particles_in_region'),
                         _tok(1, 'ins_cyl', 'ins_reg')),
    'mesh_id_rename': (lambda s: s.replace('fix Front all mesh/surface', 'fix Fr all mesh/surface')
                       .replace('meshes Drum Front Back', 'meshes Drum Fr Back').replace('mesh Front rotate', 'mesh Fr rotate'),
                       _tok(1, 'Fr', 'Front')),
    'dump_id_rename': (_rep('dump dmp all custom', 'dump d1 all custom'), _tok(1, 'd1', 'dmp')),
    'pdd_entry_order': (_rep('pt1 0.700000 pt2 0.300000', 'pt2 0.300000 pt1 0.700000'), _tok(6, 'pt2', 'pt1')),
    'template_order': (_swap('fix pt1 all particletemplate/sphere 10487 atom_type 1 density constant 4850 radius constant 0.0006813',
                             'fix pt2 all particletemplate/sphere 11887 atom_type 2 density constant 4850 radius constant 0.0003028'),
                       _tok(1, 'pt2', 'pt1')),
    'global_order': (_swap('newton          off', 'communicate     single vel yes'), _tok(0, 'communicate', 'newton')),
    'global_duplicate': (_rep('boundary        f f f\n', 'boundary        f f f\nboundary        f f f\n'), _tok(0, 'boundary', 'newton')),
    'atom_modify_removed': (_rep('atom_modify     map array sort 0 0\n', ''), _tok(0, 'hard_particles', 'atom_modify')),
    'thermo_style_removed': (_rep('thermo_style custom step atoms ke c_rke vol\n', ''), _tok(0, 'thermo', 'thermo_style')),
    'compute_extra': (_rep('compute rke all erotate/sphere', 'compute rke all erotate/sphere\ncompute kx all ke'),
                      _tok(0, 'compute', 'thermo_style')),
    'shell_order': (_swap('shell mkdir post\n', 'shell mkdir restart\n'), _tok(2, 'restart', 'post')),
    'baffle_mesh': (lambda s: (s.replace('fix Back  all mesh/surface file Back.stl  type 4 scale 0.0251665',
                                         'fix Back  all mesh/surface file Back.stl  type 4 scale 0.0251665\n'
                                         'fix Baffle all mesh/surface file Baffles.stl type 4 scale 0.0251665', 1)
                               .replace('mesh n_meshes 3 meshes Drum Front Back', 'mesh n_meshes 4 meshes Drum Front Back Baffle', 1)
                               .replace('fix mvB all move/mesh mesh Back  rotate origin 0 0 0 axis 1. 0. 0. period 0.782508',
                                        'fix mvB all move/mesh mesh Back  rotate origin 0 0 0 axis 1. 0. 0. period 0.782508\n'
                                        'fix mvBf all move/mesh mesh Baffle rotate origin 0 0 0 axis 1. 0. 0. period 0.782508', 1)),
                    _tok(1, 'Baffle', 'walls')),
    # 11-03 밤 Q4 — skin 자유 칸을 없앴다: 사유가 'neighbor skin: ASCII …' (자유 칸 수 검사) → 생성기 토큰 대조로 바뀐다 (거부는 전과 같음)
    'neighbor_garbage_skin': (lambda s: re.sub(r'(?m)^(neighbor\s+)\S+ bin$', r'\g<1>7.57e-05x bin', s), _tok(1, '7.57e-05x', '7.57e-05')),
    # 사전 공격 변이 M30 생존 (11-03) — 마지막 run 뒤에 붙인 명령은 차례 대조 (zip) 가 못 본다 → 개수 대조를 시험에 묶는다
    'command_appended_at_end': (lambda s: s + 'compute kx all ke\n', 'command count'),
}
#: MXD2R-04 문자 꼴 — 우리 파서와 LIGGGHTS 가 다른 토큰을 읽을 수 있거나 (주석 끝 '&' + 유니코드 공백 · 주석 안 NUL · 따옴표 · $) 같은 토큰을
#:   다른 글자로 쓴 꼴 (탭 · NBSP · 전각 공백 · 폭 없는 공백 · 이음 꼴 · 끝 줄바꿈).  고치기 전 세 소비자 PASS.
MXD2R04_PARSER = {
    'tab_separator': (_rep('boundary        f f f', 'boundary\tf f f'), _CTRL),
    'nbsp_separator': (_rep('boundary        f f f', 'boundary        f f f'), _ASCII),
    'ideographic_space': (_rep('newton          off', 'newton　off'), _ASCII),
    'zero_width_space': (_rep('boundary        f f f', 'boundary        f f f​'), _ASCII),
    'nul_in_comment_before_rotation': (_rep('# ② 회전', '# ②\u0000 회전'), _CTRL),
    'comment_continuation_nbsp': (_rep('neigh_modify    delay 0\n', 'neigh_modify    delay 0\n# note & \nneigh_modify exclude type 3 3\n'),
                                  _CONT),
    'comment_continuation_ideographic': (_rep('neigh_modify    delay 0\n',
                                              'neigh_modify    delay 0\n# note &　\nneigh_modify exclude type 3 3\n'), _CONT),
    'comment_continuation_nel': (_rep('neigh_modify    delay 0\n', 'neigh_modify    delay 0\n# note &\u0085\nneigh_modify exclude type 3 3\n'),
                                 _CTRL),
    'continuation_no_space': (_rep('coefficientFriction peratomtypepair 4 &', 'coefficientFriction peratomtypepair 4&'), _CONT),
    'continuation_trailing_space': (_rep('coefficientFriction peratomtypepair 4 &', 'coefficientFriction peratomtypepair 4 & '), _CONT),
    'dollar_variable': (_rep('thermo 5000', 'thermo ${every}'), _ASCII),
    'missing_final_newline': (lambda s: s[:-1], _EOL),
    'dump_modify_quoted_format': (_rep('\n# ① 채우고 정착', '\ndump_modify dmp format "%d %d %g %g %g %g %g %g %g %g %g %g"\n# ① 채우고 정착'),
                                  _ASCII),
    # 사전 공격 변이 M25 생존 (11-03) — 주석 줄 끝 ' &' (두 파서 모두 다음 줄을 주석으로 삼킨다 · 생성기 꼴 밖) → 주석 줄 이음 금지를 묶는다
    'comment_continuation_ascii': (_rep('neigh_modify    delay 0\n', 'neigh_modify    delay 0\n# note &\nneigh_modify exclude type 3 3\n'), _CONT),
}


def _set_meta(path, value):
    """메타 한 칸 고치기 (value = 상수 또는 (meta, deck) → 값)."""
    def edit(meta, deck):
        node = meta
        for part in path[:-1]:
            node = node[part]
        node[path[-1]] = value(meta, deck) if callable(value) else value
    return edit


def _seed_edit(new_seed):
    """첫 삽입 시드 (덱) + 메타 seed 를 같이 — 소수 · 상한 규칙만 남는 차이."""
    return (lambda s: s.replace('insert/pack seed 32452843 ', f'insert/pack seed {new_seed} ', 1)), _set_meta(('seed',), new_seed)


def _steps_edit(fill_delta=0, dump_new=None, restart_new=None):
    """정착 step · dump · restart 간격을 덱에서 바꾸고 메타의 시간 칸 (steps · physical_s · t0) 을 전부 맞춘다."""
    def deck(s):
        if fill_delta:
            fill = int(re.search(r'(?m)^run (\d+)\nunfix', s).group(1))
            s = s.replace(f'run {fill}\n', f'run {fill + fill_delta}\n')
        if dump_new:
            s = re.sub(r'(?m)^(dump dmp all custom )\d+', r'\g<1>' + str(dump_new), s)
        if restart_new:
            s = re.sub(r'(?m)^restart \d+ ', f'restart {restart_new} ', s)
        return s

    def meta_edit(meta, deck_text):
        steps, physical, dt = meta['steps'], meta['physical_s'], meta['dt']['deck_s']
        steps['fill'] += fill_delta
        steps['dump_every'] = dump_new or steps['dump_every']
        steps['restart_every'] = restart_new or steps['restart_every']
        steps['t0_planned'] = (2 * steps['fill'] // steps['dump_every']) * steps['dump_every']
        physical.update(settle=2 * steps['fill'] * dt, dump_interval=steps['dump_every'] * dt, t0_planned=steps['t0_planned'] * dt)
    return deck, meta_edit
#: 실제 파일 바이트로도 보는 문자 꼴 (CLI 셋)
MXD2R04_PARSER_CLI = ('tab_separator', 'nul_in_comment_before_rotation', 'comment_continuation_nbsp', 'missing_final_newline')
#: MXD2R-04 범위 넓힘 (1저자 11-03 밤 Q4 = 권고대로) — neighbor skin 도 생성기 꼴 (min(지름)·0.5 의 .6g = 7.57e-05 @ CGF 151.4).
#:   두 덱에 같이 바꾼 skin (값 · 같은 값 다른 표기) — 고치기 전 (skin = 자유 칸이던 MXD2R-04 첫 판) 세 소비자 PASS = 남은 같은 부류였다.
MXD2R04_SKIN = {
    'skin_x1p1_repr': (_rep('neighbor        7.57e-05 bin', 'neighbor        8.327000000000001e-05 bin'),
                       _tok(1, '8.327000000000001e-05', '7.57e-05')),
    'skin_x1p1_g6': (_rep('neighbor        7.57e-05 bin', 'neighbor        8.327e-05 bin'), _tok(1, '8.327e-05', '7.57e-05')),
    'skin_doubled': (_rep('neighbor        7.57e-05 bin', 'neighbor        0.0001514 bin'), _tok(1, '0.0001514', '7.57e-05')),
    'skin_am_radius': (_rep('neighbor        7.57e-05 bin', 'neighbor        0.0006813 bin'), _tok(1, '0.0006813', '7.57e-05')),
    'skin_tiny': (_rep('neighbor        7.57e-05 bin', 'neighbor        1e-09 bin'), _tok(1, '1e-09', '7.57e-05')),
    'skin_same_value_decimal': (_rep('neighbor        7.57e-05 bin', 'neighbor        0.0000757 bin'), _tok(1, '0.0000757', '7.57e-05')),
    'skin_same_value_padded': (_rep('neighbor        7.57e-05 bin', 'neighbor        7.570e-05 bin'), _tok(1, '7.570e-05', '7.57e-05')),
}
MXD2R04_SKIN_CLI = ('skin_x1p1_repr', 'skin_same_value_decimal')


def _write_case(folder, old, new, old_meta, new_meta):
    """Deck files are written as exact bytes (MXD2R-03: the CLI hashes physical bytes — text-mode writes would be CRLF on Windows)."""
    folder = Path(folder)
    for name, deck in (('old.in', old), ('new.in', new)):
        (folder / name).write_bytes(deck if isinstance(deck, bytes) else deck.encode('utf-8'))
    for name, meta in (('old.json', old_meta), ('new.json', new_meta)):
        (folder / name).write_text(json.dumps(meta), encoding='utf-8')


def _run_three_cli(folder):
    """Real CLIs of the three development consumers → {consumer: (rc, stdout, stderr)}."""
    folder, scripts = Path(folder), Path(__file__).resolve().parent
    commands = {'readback': ['mixer_deck_readback.py', '--d2', str(folder / 'old.in'), str(folder / 'old.json')],
                'pair': ['mixer_deck_diff.py', str(folder / 'old.in'), str(folder / 'new.in'), '--allow', 'D2',
                         '--meta-ref', str(folder / 'old.json'), '--meta-new', str(folder / 'new.json')],
                'plan': ['mixer_smoke_blind.py', '--d2-plan', str(folder / 'old.in'), '--d2-meta', str(folder / 'old.json')]}
    out = {}
    for key, cmd in commands.items():
        proc = subprocess.run([sys.executable, '-I', '-X', 'utf8', '-B', str(scripts / cmd[0]), *cmd[1:]], capture_output=True)
        out[key] = (proc.returncode, proc.stdout.decode('utf-8', 'replace'), proc.stderr.decode('utf-8', 'replace'))
    return out


class D2Consumers(unittest.TestCase):
    def assert_pass(self, result):
        self.assertEqual(result['verdict'], 'PASS', result.get('failures'))
        self.assertFalse(result['execution_authorized'])
        self.assertIsNone(result['registered'])

    def assert_fail(self, result):
        self.assertEqual(result['verdict'], 'FAIL', result)
        self.assertTrue(result['failures'])
        self.assertFalse(result['execution_authorized'])

    def test_generation_and_supported_phase_positive(self):
        for phases, generation, stiff, rho, coated, layered in itertools.product(
                [('AM_P', 'AM_S', 'SE'), ('AM_P', 'SE')], ['gen1', 'lab20261014'],
                [1., 20.], [.03, .3, 1., 10.], [False, True], [False, True]):
            with self.subTest(phases=phases, gen=generation, stiff=stiff, rho=rho, coated=coated, layered=layered):
                text, meta, counts = fixture(phases, generation, stiff, rho, coated, layered=layered)
                result = rb.read_d2(text, meta)
                self.assert_pass(result)
                self.assertEqual(result['expected_counts'], counts)
                self.assertEqual(result['density_generation'], generation)
                self.assertLess(abs(result['Bo_SE'] / meta['adhesion_rule']['bo_se'] - 1), 2e-5)

    def test_counts_are_from_actual_inputs(self):
        observed = {}
        for n, cgf, layered, generation in itertools.product([8000, 77777, 100000, 100001],
                [75.7, 151.4, 302.8], [False, True], ['gen1', 'lab20261014']):
            text, meta, counts = fixture(n=n, cgf=cgf, layered=layered, generation=generation)
            result = smoke.d2_plan_check(text, meta)
            self.assert_pass(result)
            self.assertEqual(result['expected_counts'], counts)
            self.assertEqual(result['n_atoms_planned'], sum(counts.values()))
            if n == 100000 and cgf == 151.4: observed[generation] = counts
        self.assertEqual(observed['gen1'], {'1': 176, '2': 859, '3': 98965})
        self.assertEqual(observed['lab20261014'], {'1': 143, '2': 699, '3': 99158})
        self.assertEqual(smoke._expected_counts({'stiffen_se': 20}), {1: 176, 2: 859, 3: 98965})

    def test_d2_pairs_and_old_contracts(self):
        for phases, generation, stiff, rho in itertools.product(
                [('AM_P', 'AM_S', 'SE'), ('AM_P', 'SE')], ['gen1', 'lab20261014'], [1., 20.], [.03,.3,1.,10.]):
            a, am, _ = fixture(phases, generation, stiff, rho, False)
            b, bm, _ = fixture(phases, generation, stiff, rho, True)
            self.assert_pass(dd.diff_d2_decks(a, b, am, bm))
        a, am, _ = fixture(); b, bm, _ = fixture(coated=True)
        for allow in ['A','B','U','E','EB']:
            self.assertEqual(dd.diff_decks(a,b,allow=allow)['verdict'], 'FAIL', allow)
        self.assertEqual(set(dd.ALLOW), {'A','B'})
        self.assertNotIn('D2', dd.COHORTS)

    def test_actual_common_mode_mutations(self):
        for transform in [lambda t:t.replace('gravity 9.81', 'gravity 1.0'),
                          lambda t:t.replace('density constant 1640', 'density constant 2000'),
                          lambda t:t.replace('units           si', 'units           cgs'),
                          lambda t:t.replace('radius constant 7.57e-05', 'radius constant 7.58e-05'),
                          lambda t:t.replace('pt1 0.700000', 'pt1 0.710000'),
                          lambda t:t.replace('particles_in_region 842', 'particles_in_region 843')]:
            a,am,_=fixture(); b,bm,_=fixture(coated=True)
            aa,bb=transform(a),transform(b)
            self.assertNotEqual(aa,a)
            self.assert_fail(rb.read_d2(aa,rebound(aa,am)))
            self.assert_fail(dd.diff_d2_decks(aa,bb,rebound(aa,am),rebound(bb,bm)))

    def test_meta_binding_and_numeric_boundaries(self):
        t,m,_=fixture()
        mutations = [lambda q:q.update(dens_gen='gen1'),lambda q:q.update(dens_gen='unknown'),
            lambda q:q.update(dens_gen=' lab20261014'),lambda q:q.update(deck_sha256='0'*64),
            lambda q:q.update(deck_bytes=m['deck_bytes']+1),lambda q:q.update(n_atoms_planned=99999),
            lambda q:q.update(cgf=200.), lambda q:q.update(seed=15485863),
            lambda q:q.update(unrecognized_contract_axis=True),lambda q:q['dens_g_cm3'].update(SE=2.),
            lambda q:q['types'].update({'2':'SE','3':'AM_S'}),lambda q:q['E_Pa'].update(SE=1e7),
            lambda q:q['nu'].update(SE=.37),lambda q:q['radius_m'].update(SE=1e-4),
            lambda q:q['adhesion_rule'].update(gamma_wall=.0256),lambda q:q['adhesion_rule'].update(rho_uncoated_ncm=.2),
            lambda q:q['adhesion_rule'].update(unknown=1),lambda q:q.update(registered='new-policy-v5')]
        for f in mutations:
            q=copy.deepcopy(m);f(q);self.assert_fail(rb.read_d2(t,q))
        for v in [float('nan'),float('inf'),0,-1,True,'0.73','０.７３',1e-310,10**1000,None,[],{}]:
            q=copy.deepcopy(m);q['adhesion_rule']['bo_se']=v;self.assert_fail(rb.read_d2(t,q))
        for q in [None,[],True,{},'meta']:
            self.assert_fail(rb.read_d2(t,q))

    def test_pair_identity_and_orientation(self):
        a,am,_=fixture();b,bm,_=fixture(coated=True)
        self.assert_fail(dd.diff_d2_decks(b,a,bm,am))
        for kwargs in [dict(rho=.2),dict(generation='gen1'),dict(cgf=200.),dict(stiff=1.),dict(bo=1.5),dict(seed=15485863),dict(n=8000)]:
            t,m,_=fixture(coated=True,**kwargs);self.assert_fail(dd.diff_d2_decks(a,t,am,m))
        self.assert_fail(dd.diff_d2_decks(a,a,am,am))

    def test_ceiling_and_ced_meta_rebinding(self):
        t,m,_=fixture()
        lines=t.splitlines(); start=next(i for i,x in enumerate(lines) if 'cohesionEnergyDensity peratomtypepair' in x)
        # Matrix is continued across four rows; alter both symmetric values and rebind the content hash.
        for i in range(start+1,start+5):
            lines[i]=' '.join(str(float(x)*2) if x not in ('&',) else x for x in lines[i].split())
        changed='\n'.join(lines)+'\n'; self.assert_fail(rb.read_d2(changed,rebound(changed,m)))
        # Keep the absolute Bo declaration consistent with CED cubed so only
        # the actual static-overlap ceiling can reject this large-cohesion deck.
        lines=t.splitlines()
        for i in range(start+1,start+5):
            lines[i]=' '.join(str(float(x)*100) if x!='&' else x for x in lines[i].split())
        changed='\n'.join(lines)+'\n';meta=rebound(changed,m)
        meta['adhesion_rule']['bo_se']*=100**3
        result=rb.read_d2(changed,meta)
        self.assert_fail(result)
        self.assertTrue(any('static pair overlap' in failure for failure in result['failures']),result)

    def test_coordinated_density_and_gravity_vector(self):
        # A common density scale preserves all count ratios. Recompute the deck's
        # forces/time consistently, then falsely relabel only the declared table.
        # This must still fail the independent actual-density generation binding.
        canonical=gen.DENS_GENERATIONS['lab20261014']
        try:
            gen.DENS_GENERATIONS['lab20261014']={k:v*1.1 for k,v in canonical.items()}
            a,am,_=fixture();b,bm,_=fixture(coated=True)
        finally:
            gen.DENS_GENERATIONS['lab20261014']=canonical
        for m in (am,bm):m['dens_g_cm3']=dict(canonical)
        self.assert_fail(rb.read_d2(a,am))
        self.assert_fail(dd.diff_d2_decks(a,b,am,bm))
        a,am,_=fixture();b,bm,_=fixture(coated=True)
        aa=a.replace('vector 0.0 0.0 -1.0','vector 0.0 0.0 1.0')
        bb=b.replace('vector 0.0 0.0 -1.0','vector 0.0 0.0 1.0')
        self.assertNotEqual(aa,a)
        self.assert_fail(rb.read_d2(aa,rebound(aa,am)))
        self.assert_fail(dd.diff_d2_decks(aa,bb,rebound(aa,am),rebound(bb,bm)))

    def test_tokens_and_nested_schema(self):
        text,meta,_=fixture()
        for transform in [lambda t:t.replace('density constant 1640','density constant 1_640'),
                          lambda t:t.replace('radius constant 7.57e-05','radius constant ７.57e-05'),
                          lambda t:t.replace('pt1 0.700000','pt1 0_0.700000'),
                          lambda t:t.replace('gravity 9.81','gravity ９.81')]:
            changed=transform(text);self.assertNotEqual(changed,text)
            self.assert_fail(rb.read_d2(changed,rebound(changed,meta)))
        for field in ['dt','steps','physical_s']:
            q=copy.deepcopy(meta);q[field]['unrecognized']=1;self.assert_fail(rb.read_d2(text,q))
        for value in [True, '2', float('nan'),float('inf'),-1]:
            q=copy.deepcopy(meta);q['revolutions']=value;self.assert_fail(rb.read_d2(text,q))

    def test_actual_command_scope(self):
        text,meta,_=fixture()
        for transform in [lambda t:t.replace('gravi all gravity','gravi subset gravity'),
                          lambda t:t.replace('density constant 1640','density gaussian 1640'),
                          lambda t:t.replace('wall/gran model hertz','wall/gran model hooke'),
                          lambda t:t+'\nunfix gravi\n',lambda t:t+'\nset type 3 density 2000\n',
                          lambda t:t+'\ninclude other.in\n']:
            changed=transform(text);self.assertNotEqual(changed,text)
            self.assert_fail(rb.read_d2(changed,rebound(changed,meta)))
        other=fixture(coated=True)
        changed=other[0].replace('neighbor        ', 'neighbor        ',1)
        lines=other[0].splitlines()
        i=next(i for i,line in enumerate(lines) if line.startswith('neighbor'))
        tokens=lines[i].split();tokens[1]=str(float(tokens[1])*1.1);lines[i]=' '.join(tokens)
        changed='\n'.join(lines)+'\n'
        # ★ 기대 바꿈 (MXD2R-04 범위 넓힘 · 1저자 11-03 밤 Q4 = 권고대로 · 이유 = (가) 원리 (생성기 자신의 꼴만) · 같은 부류 예외 제거):
        #   옛 기대 = 한쪽 덱의 neighbor skin ×1.1 → 단일 덱 readback PASS (skin = 단일 덱 계약 밖 · 짝 대조만 FAIL) — 그래서 두 덱에 같이
        #   바꾼 skin 은 세 소비자 PASS 였다 (남은 같은 부류).  새 기대 = 단일 덱도 FAIL (skin = 생성기 값 min(지름)·0.5 의 .6g) · 짝도 FAIL.
        #   증거 docs/reviews/mxd2r_fix_evidence_20261103/mxd2r04/README.md §9 (옛 기대 → 새 기대 표).
        single = rb.read_d2(changed,rebound(changed,other[1]))
        self.assert_fail(single)
        self.assertTrue(any(_tok(1, tokens[1], '7.57e-05') in f for f in single['failures']), single['failures'])
        self.assert_fail(dd.diff_d2_decks(text,changed,meta,rebound(changed,other[1])))

    def test_command_lifecycle(self):
        def transform(text,case):
            lines=text.splitlines()
            if case=='early_unfix':
                lines.remove('unfix insA');lines.insert(lines.index('run 1'),'unfix insA')
            elif case=='missing_integrator':
                lines=[line for line in lines if ' all nve/sphere' not in line]
            elif case=='early_rotation':
                moves=[line for line in lines if ' all move/mesh ' in line]
                lines=[line for line in lines if line not in moves]
                index=lines.index('run 1');lines[index:index]=moves
            elif case=='late_integrator':
                line=next(line for line in lines if ' all nve/sphere' in line)
                lines.remove(line);lines.insert(lines.index('run 1')+1,line)
            elif case=='bad_region':return text.replace('region ins_reg particles_in_region','region no_such_region particles_in_region')
            elif case=='no_insert_removal':lines.remove('unfix insA')
            elif case=='missing_mesh':return text.replace('meshes Drum Front Back','meshes Missing Front Back')
            elif case=='bad_rotation_mesh':return text.replace('mesh Drum  rotate','mesh Missing  rotate')
            elif case=='duplicate_region':
                lines.insert(lines.index('run 1'),next(line for line in lines if line.startswith('region ins_reg ')))
            elif case=='unknown_create_region':return text.replace('4 reg','4 unknown',1)
            else:raise AssertionError(case)
            return '\n'.join(lines)+'\n'
        for case in ['early_unfix','missing_integrator','early_rotation','late_integrator','bad_region',
                     'no_insert_removal','missing_mesh','bad_rotation_mesh','duplicate_region','unknown_create_region']:
            with self.subTest(case=case):
                a,am,_=fixture();b,bm,_=fixture(coated=True)
                aa=transform(a,case);bb=transform(b,case)
                self.assertNotEqual(aa,a)
                self.assert_fail(rb.read_d2(aa,rebound(aa,am)))
                self.assert_fail(dd.diff_d2_decks(aa,bb,rebound(aa,am),rebound(bb,bm)))
                self.assert_fail(smoke.d2_plan_check(aa,rebound(aa,am)))

    def test_dt_half_and_legacy_cli_positive(self):
        for factor in [1.,.5,.25]:
            text,meta,counts=fixture(dt_factor=factor);self.assert_pass(rb.read_d2(text,meta))
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)
            for name,stiff in [('soft',1.),('ref',20.)]:
                text=dd.expected_deck('LC',32452843,stiffen_se=stiff,hold_bo_pairwise=True)
                (p/name).write_text(text)
            proc=subprocess.run([sys.executable,'-I','-X','utf8','-B',str(Path(dd.__file__)),str(p/'soft'),str(p/'ref'),'--allow','E'],capture_output=True,text=True,encoding='utf-8')
            self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
            self.assertNotIn('Traceback',proc.stderr)

    def test_cli_and_duplicate_json(self):
        with tempfile.TemporaryDirectory() as temp:
            b=Path(temp);a,am,_=fixture();c,cm,_=fixture(coated=True)
            for name,text,meta in [('a',a,am),('b',c,cm)]:
                # MXD2R-03: the CLI hashes physical bytes — write exact LF bytes (text-mode write = CRLF on Windows)
                (b/(name+'.in')).write_bytes(text.encode('utf-8'));(b/(name+'.json')).write_text(json.dumps(meta))
            scripts=Path(__file__).resolve().parent
            commands=[['mixer_deck_readback.py','--d2',str(b/'a.in'),str(b/'a.json')],
                      ['mixer_deck_diff.py',str(b/'a.in'),str(b/'b.in'),'--allow','D2','--meta-ref',str(b/'a.json'),'--meta-new',str(b/'b.json')],
                      ['mixer_smoke_blind.py','--d2-plan',str(b/'a.in'),'--d2-meta',str(b/'a.json')]]
            for cmd in commands:
                p=subprocess.run([sys.executable,'-I','-X','utf8','-B',str(scripts/cmd[0]),*cmd[1:]],capture_output=True,text=True,encoding='utf-8')
                self.assertEqual(p.returncode,0,p.stdout+p.stderr)
                self.assertIn('개발',p.stdout)
            raw=(b/'a.json').read_text();(b/'a.json').write_text(raw.replace('"dens_gen":', '"dens_gen":"gen1", "dens_gen":'))
            for cmd in commands:
                p=subprocess.run([sys.executable,'-I','-X','utf8','-B',str(scripts/cmd[0]),*cmd[1:]],capture_output=True,text=True,encoding='utf-8')
                self.assertNotEqual(p.returncode,0)
                self.assertNotIn('Traceback',p.stderr)

    # ── MXD2R (Codex 10-27 · 1저자 11-02 Q1–Q3 (가)) — 반례를 고치기 전에 옮겼다 ─────────────────────────────────
    def _common_mode(self, transform, reason, cli=False):
        """Same mutation in both decks, metadata hash/bytes rebound → all three consumers must reject for `reason`."""
        a, am, _ = fixture(); b, bm, _ = fixture(coated=True)
        aa, bb = transform(a), transform(b)
        self.assertNotEqual(aa, a); self.assertNotEqual(bb, b)
        ma, mb = rebound(aa, am), rebound(bb, bm)
        results = {'readback': rb.read_d2(aa, ma), 'pair': dd.diff_d2_decks(aa, bb, ma, mb), 'plan': smoke.d2_plan_check(aa, ma)}
        for key, result in results.items():
            with self.subTest(api=key):
                self.assert_fail(result)
                self.assertTrue(any(reason in failure for failure in result['failures']), (key, reason, result['failures']))
        if cli:
            with tempfile.TemporaryDirectory() as temp:
                _write_case(temp, aa, bb, ma, mb)
                for key, (rc, out, err) in _run_three_cli(temp).items():
                    with self.subTest(cli=key):
                        self.assertEqual(rc, 1, out + err)
                        self.assertIn(reason, out)
                        self.assertNotIn('Traceback', err)

    def test_mxd2r01_codex_time_insert_rotation(self):
        """MXD2R-01 — Codex 네 공통 변조 (run upto · 늦은 timestep · 삽입 start · Front 주기): API 셋 FAIL · CLI 셋 rc 1 · 사유."""
        for name in ('run_upto', 'late_timestep', 'insert_start_late', 'front_period'):
            with self.subTest(case=name):
                self._common_mode(*CODEX_COMMON_MODE[name], cli=True)

    def test_mxd2r01_same_class_generator_grammar(self):
        """MXD2R-01 같은 부류 — run 옵션 · timestep 위치/토큰 · 삽입 반복/start/속도 · Back 주기 (API 셋)."""
        for name, (transform, reason) in MXD2R01_SAME_CLASS.items():
            with self.subTest(case=name):
                self._common_mode(transform, reason)

    def test_mxd2r02_codex_contact_exclusion_and_friction(self):
        """MXD2R-02 — Codex SE–SE 접촉 제외 · 보조 탐침 마찰 행렬 삭제: API 셋 FAIL · CLI 셋 rc 1 · 사유."""
        for name in ('exclude_SE_SE', 'friction_missing'):
            with self.subTest(case=name):
                self._common_mode(*CODEX_COMMON_MODE[name], cli=True)

    def test_mxd2r02_same_class_contact_and_materials(self):
        """MXD2R-02 같은 부류 — 다른 제외 · 이웃 갱신 옵션 · 재료 fix 결손/중복/값/순서/모르는 이름 · pair 위치/계수 (API 셋)."""
        for name, (transform, reason) in MXD2R02_SAME_CLASS.items():
            with self.subTest(case=name):
                self._common_mode(transform, reason)

    def test_mxd2r02_material_copies_match_generator(self):
        """재료 fix 목록 · 상수 = 생성기 덱에서 뽑은 것과 정확히 같다 (사본이 갈리면 여기서 드러난다 · fail-closed)."""
        text, _, _ = fixture()
        names = [t[4] for t in (line.split() for line in text.splitlines())
                 if len(t) > 4 and t[0] == 'fix' and t[3] == 'property/global']
        self.assertEqual(sorted(names), sorted(rb.D2_MATERIAL))
        self.assertEqual(rb.D2_MATERIAL['coefficientRestitution'][1], gen.COR)
        self.assertEqual(rb.D2_MATERIAL['coefficientFriction'][1], gen.MU_S)
        self.assertEqual(rb.D2_MATERIAL['coefficientRollingFriction'][1], gen.MU_R)
        self.assertIn('fix m9 all property/global characteristicVelocity scalar 2.0\n', text)
        self.assertEqual(rb.D2_MATERIAL['characteristicVelocity'], ('scalar', 2.0))

    def test_mxd2r03_physical_bytes_api(self):
        """MXD2R-03 — API 가 실제 파일 바이트를 받는다: LF 바이트 PASS · CRLF+LF 메타 = SHA 사유 · CRLF+CRLF 메타 (바이트 · 텍스트) = LF-only 사유."""
        a, am, _ = fixture(); b, bm, _ = fixture(coated=True)
        ca, cb = a.replace('\n', '\r\n').encode(), b.replace('\n', '\r\n').encode()
        cam, cbm = rebound_bytes(ca, am), rebound_bytes(cb, bm)
        for key, result in {'readback': rb.read_d2(a.encode(), am), 'pair': dd.diff_d2_decks(a.encode(), b.encode(), am, bm),
                            'plan': smoke.d2_plan_check(a.encode(), am)}.items():
            with self.subTest(lf_bytes=key):
                self.assert_pass(result)
        for key, result in {'readback': rb.read_d2(ca, am), 'pair': dd.diff_d2_decks(ca, cb, am, bm),
                            'plan': smoke.d2_plan_check(ca, am)}.items():
            with self.subTest(crlf_bytes_lf_meta=key):
                self.assert_fail(result)
                self.assertTrue(any('SHA256' in f for f in result['failures']), result['failures'])
        for key, result in {'readback': rb.read_d2(ca, cam), 'pair': dd.diff_d2_decks(ca, cb, cam, cbm),
                            'plan': smoke.d2_plan_check(ca, cam), 'readback_text': rb.read_d2(ca.decode(), cam),
                            'pair_text': dd.diff_d2_decks(ca.decode(), cb.decode(), cam, cbm)}.items():
            with self.subTest(crlf_crlf_meta=key):
                self.assert_fail(result)
                self.assertTrue(any('LF-only' in f for f in result['failures']), result['failures'])

    def test_mxd2r03_physical_bytes_cli_both_directions(self):
        """MXD2R-03 — 세 CLI: LF 바이트 rc 0 · CRLF 덱 + LF 메타 rc 1 (SHA) · CRLF 덱 + CRLF 메타 rc 1 (LF-only 사유)."""
        a, am, _ = fixture(); b, bm, _ = fixture(coated=True)
        ca, cb = a.replace('\n', '\r\n').encode(), b.replace('\n', '\r\n').encode()
        cases = [('lf', (a.encode(), b.encode(), am, bm), 0, '개발'),
                 ('crlf_lf_meta', (ca, cb, am, bm), 1, 'SHA256'),
                 ('crlf_crlf_meta', (ca, cb, rebound_bytes(ca, am), rebound_bytes(cb, bm)), 1, 'LF-only')]
        with tempfile.TemporaryDirectory() as temp:
            for label, decks, rc_want, reason in cases:
                folder = Path(temp) / label
                folder.mkdir()
                _write_case(folder, *decks)
                for key, (rc, out, err) in _run_three_cli(folder).items():
                    with self.subTest(case=label, cli=key):
                        self.assertEqual(rc, rc_want, out + err)
                        self.assertIn(reason, out)
                        self.assertNotIn('Traceback', err)

    def test_mxd2r_positive_codex_independent_48(self):
        """양성 보존 (판정문 §7 (4)) — Codex 독립 정상 48 조합: 세 소비자 PASS · SE Bo · 상별 계획수 독립 산술 일치 · 증서 아님."""
        seen = 0
        for phases, generation, rho, stiff, layered in itertools.product(
                [('AM_P', 'AM_S', 'SE'), ('AM_P', 'SE')], ['gen1', 'lab20261014'], [.2, 1., 2.], [1., 20.], [True, False]):
            with self.subTest(phases=phases, gen=generation, rho=rho, stiff=stiff, layered=layered):
                kw = dict(phases=phases, generation=generation, rho=rho, stiff=stiff, layered=layered, n=90007, cgf=135, bo=1.1, seed=49979687)
                a, am, _ = fixture(**kw); b, bm, _ = fixture(coated=True, **kw)
                result = rb.read_d2(a, am)
                for r in (result, dd.diff_d2_decks(a, b, am, bm), smoke.d2_plan_check(a, am)):
                    self.assert_pass(r)
                raw = rb.read_deck(a); se = len(phases)
                rad, dens = raw['templates'][se]['radius'], raw['templates'][se]['density']
                E, nu = raw['E'][se - 1], raw['nu'][se - 1]
                es, rs, ced = E / (2 * (1 - nu * nu)), rad / 2, raw['ced'][se, se]
                bo = ((2 * math.pi * rs * ced) ** 3 / ((4 / 3) * es * math.sqrt(rs)) ** 2) / ((4 / 3) * math.pi * rad ** 3 * dens * 9.81)
                self.assertLess(abs(bo / 1.1 - 1), 2e-5)
                d0 = {'gen1': {'AM': 4800, 'SE': 2000}, 'lab20261014': {'AM': 4850, 'SE': 1640}}[generation]
                nr = [{'AM_P': 56, 'AM_S': 24, 'SE': 18}[p] / (d0['SE' if p == 'SE' else 'AM'] * ({'AM_P': 9, 'AM_S': 4, 'SE': 1}[p] ** 3))
                      for p in phases]
                self.assertEqual(list(result['expected_counts'].values()), [round(90007 * x / sum(nr)) for x in nr])
                seen += 1
        self.assertEqual(seen, 48)

    # ── MXD2R-04 (11-03 사전 공격 · 1저자 11-03 Q1 = 권고대로 — 공통 변조 17 도 생성기 꼴로) — 반례를 고치기 전에 옮겼다 ──────────────
    def test_mxd2r04_outside_scope_17_api_and_cli(self):
        """MXD2R-04 — 사전 공격이 보고한 범위 밖 공통 변조 17 (전역 설정 · 템플릿 뒤 옵션 · 따옴표 # · RNG 시드 · 기하 · 출력 · 체크포인트):
        API 셋 FAIL · CLI 셋 rc 1 · 사유 = 첫 어긋난 토큰 ↔ 생성기 토큰 (따옴표 = 문자 꼴)."""
        self.assertEqual(len(MXD2R04_OUTSIDE_17), 17)
        for name, (transform, reason) in MXD2R04_OUTSIDE_17.items():
            with self.subTest(case=name):
                self._common_mode(transform, reason, cli=True)

    def test_mxd2r04_same_class_spelling_identity_order(self):
        """MXD2R-04 같은 부류 — 같은 값 다른 표기 · 생성기 이름 · 순서 · 중복 · 결손 · 배플 · 출력 · 체크포인트 · skin 토큰 꼴 (API 셋)."""
        for name, (transform, reason) in MXD2R04_SAME_CLASS.items():
            with self.subTest(case=name):
                self._common_mode(transform, reason)

    def test_mxd2r04_parser_equivalence_characters(self):
        """MXD2R-04 문자 꼴 — 탭 · NBSP · 전각 · 폭 없는 공백 · 주석 안 NUL · 주석 끝 '&'+유니코드 공백 · 이음 꼴 · $ · 따옴표 · 끝 줄바꿈
        (API 셋 · 넷은 실제 파일 바이트로 CLI 셋)."""
        for name, (transform, reason) in MXD2R04_PARSER.items():
            with self.subTest(case=name):
                self._common_mode(transform, reason, cli=name in MXD2R04_PARSER_CLI)

    def test_mxd2r04_timestep_spelling_with_metadata(self):
        """같은 값 다른 timestep 표기를 메타 deck_txt 에도 같이 넣은 덱 (k = 1 · 2 · 3) — 메타 결합만으로는 못 잡는다 → 생성기 표기로 거부."""
        for factor in (1., .5, 1 / 3):
            with self.subTest(dt_factor=factor):
                a, am, _ = fixture(dt_factor=factor); b, bm, _ = fixture(coated=True, dt_factor=factor)
                old = re.search(r'(?m)^timestep\s+(\S+)$', a).group(1)
                mantissa, exponent = old.split('e')
                new = mantissa + ('0' if '.' in mantissa else '.0') + 'e' + exponent
                self.assertEqual(float(new), float(old)); self.assertNotEqual(new, old)
                aa, bb = (x.replace('timestep        ' + old + '\n', 'timestep        ' + new + '\n') for x in (a, b))
                self.assertNotEqual(aa, a)
                ma, mb = rebound(aa, am), rebound(bb, bm)
                for meta in (ma, mb):
                    meta['dt']['deck_txt'] = new
                for key, result in {'readback': rb.read_d2(aa, ma), 'pair': dd.diff_d2_decks(aa, bb, ma, mb),
                                    'plan': smoke.d2_plan_check(aa, ma)}.items():
                    with self.subTest(api=key):
                        self.assert_fail(result)
                        self.assertTrue(any(_tok(1, new, old) in f for f in result['failures']), result['failures'])

    def test_mxd2r04_neighbor_skin_generator_form(self):
        """MXD2R-04 범위 넓힘 (1저자 11-03 밤 Q4) — 두 덱에 같이 바꾼 neighbor skin (×1.1 · ×2 · AM 반지름 · 1e-9 · 같은 값 다른 표기):
        API 셋 FAIL · 둘은 CLI 셋 rc 1 · 사유 = 생성기 skin 토큰 (min(지름)·0.5 · .6g).  다른 CGF 의 생성기 skin 은 기존 양성 시험이 지킨다."""
        for name, (transform, reason) in MXD2R04_SKIN.items():
            with self.subTest(case=name):
                self._common_mode(transform, reason, cli=name in MXD2R04_SKIN_CLI)

    def test_mxd2r04_metadata_coordinated_rules(self):
        """MXD2R-04 — 메타까지 같이 바꾼 덱 (해시 재결합 + 메타가 덱과 같은 말 → 메타 결합으로는 못 잡는다): 합성수 시드 · 2^31−1 넘는 소수
        시드 · k 배가 아닌 정착 step · 규칙 밖 dump · restart 간격 · 전 정밀도 형식 메타 ↔ 생성기 (사전 공격 변이 M28 · M32–M35 생존 → 묶음)."""
        cases = {
            'seed_composite': ({}, *_seed_edit(32452845), 'insertion seed must be a prime'),
            'seed_prime_over_int32': ({}, *_seed_edit(gen._next_prime(2 ** 31)), 'insertion seed must be a prime'),
            'settle_not_multiple_of_k': (dict(dt_factor=.5), *_steps_edit(fill_delta=1), 'k × the generator plan'),
            'dump_interval_off_rule': ({}, *_steps_edit(dump_new=33000), _tok(4, '33000', '32976')),
            'restart_interval_off_rule': ({}, *_steps_edit(restart_new=150000), _tok(1, '150000', '200000')),
            'dump_format_meta_only': (dict(dump_full_precision=True), lambda s: s,
                                      _set_meta(('dump_modify_format',), '%d %d' + ' %.16g' * 10),
                                      'metadata dump_modify_format'),
        }
        for name, (kw, deck_edit, meta_edit, reason) in cases.items():
            with self.subTest(case=name):
                a, am, _ = fixture(**kw); b, bm, _ = fixture(coated=True, **kw)
                aa, bb = deck_edit(a), deck_edit(b)
                ma, mb = rebound(aa, am), rebound(bb, bm)
                meta_edit(ma, aa); meta_edit(mb, bb)
                self.assertNotEqual((aa, ma), (a, am))
                for key, result in {'readback': rb.read_d2(aa, ma), 'pair': dd.diff_d2_decks(aa, bb, ma, mb),
                                    'plan': smoke.d2_plan_check(aa, ma)}.items():
                    with self.subTest(api=key):
                        self.assert_fail(result)
                        self.assertTrue(any(reason in f for f in result['failures']), (key, reason, result['failures']))

    def test_mxd2r04_positive_generator_options(self):
        """양성 보존 — 생성기 꼴 엄격이 생성기 출력 (전 정밀도 덤프 · dt/3 · 다른 Froude · 다른 소수 시드 · 균일 · 층상 · 2 · 3 상) 을 받는다."""
        options = [dict(dump_full_precision=True), dict(dump_full_precision=True, layered=False, phases=('AM_P', 'SE')),
                   dict(dt_factor=1 / 3), dict(dt_factor=.25, layered=False), dict(fr=.06), dict(fr=.085, phases=('AM_P', 'SE')),
                   dict(seed=91648301), dict(seed=15485863, layered=False), dict(n=8000, cgf=302.8, generation='gen1'),
                   dict(stiff=1., rho=10., n=100001, cgf=75.7)]
        for kw in options:
            with self.subTest(**{k: str(v) for k, v in kw.items()}):
                a, am, _ = fixture(**kw); b, bm, _ = fixture(coated=True, **kw)
                for r in (rb.read_d2(a, am), dd.diff_d2_decks(a, b, am, bm), smoke.d2_plan_check(a, am),
                          rb.read_d2(a.encode('utf-8'), am)):
                    self.assert_pass(r)

    def test_mxd2r04_copies_match_generator(self):
        """MXD2R-04 사본 ↔ 생성기 — 전역 설정 줄 · 드럼 기본값 · 분포 시드 · 소수 규칙 · dump 열 · 전 정밀도 형식 · 템플릿 시드 · 시드 상한."""
        text, _, _ = fixture()
        commands = [t for _, t in rb.read_deck(text)['cmds']]
        self.assertEqual([tuple(t) for t in commands[:7]], list(rb.D2_GLOBAL_FORM))
        params = inspect.signature(gen.plan).parameters
        self.assertEqual(rb.D2_DRUM, dict(fill=params['fill'].default, pack=params['pack'].default,
                                          r_over_l=params['drum_r_over_l'].default))
        self.assertEqual(rb.D2_DIST_SEED, (32452867, gen._next_prime(32452867 + 2)))
        self.assertIn('fix pddA all particledistribution/discrete 32452867 2 &', text)
        for n in (0, 1, 2, 3, 4, 24, 32452843, 32452845, 32452869, 49979688, 2 ** 31 - 2):
            self.assertEqual(rb._d2_next_prime(n), gen._next_prime(n), n)
        old = gen.TYPES
        try:
            for phases in (('AM_P', 'AM_S', 'SE'), ('AM_P', 'SE')):
                gen.set_phases(phases)
                self.assertEqual(rb.D2_DUMP_COLUMNS, gen.dump_columns())
                self.assertEqual(rb.D2_DUMP_FORMAT, gen.dump_modify_format(gen.dump_columns()))
        finally:
            gen.set_phases(old)
        self.assertEqual({p: s for s, p in rb.REG_TPL_SEED.items()}, {p: gen.TPL_SEED[p] for p in ('AM_P', 'AM_S', 'SE')})
        self.assertEqual(rb.D2_MESHES, ('Drum', 'Front', 'Back'))
        self.assertEqual(rb.D2_SEED_MAX, 2 ** 31 - 1)


class D2InsertionSeedBounds(unittest.TestCase):
    """MXD2R-R01: actual insertion seeds, including the derived layered seed.

    Synthetic decks and real consumer CLIs only; no LIGGGHTS or scheduler.
    Added before the guard fix. Metadata hashes/lengths match every test deck.
    """
    @staticmethod
    def pair(**kw):
        a, am, _ = fixture(**kw)
        b, bm, _ = fixture(coated=True, **kw)
        return a, b, am, bm

    @classmethod
    def overflow_pair(cls, phases):
        """Keep the historical invalid deck as an explicit consumer-side mutation.

        The generator now refuses this input. Start with the accepted near-max
        boundary and reproduce the old first/derived seeds without disabling a
        generator guard or making consumer coverage depend on invalid generation.
        """
        a, b, am, bm = cls.pair(seed=2147483629, phases=phases)
        bad = []
        for text, meta in ((a, am), (b, bm)):
            text = re.sub(r'(fix insA all insert/pack seed )\d+',
                          lambda m: m[1] + '2147483647', text)
            text = re.sub(r'(fix insB all insert/pack seed )\d+',
                          lambda m: m[1] + '2147483659', text)
            meta = rebound(text, meta)
            meta['seed'] = 2147483647
            bad.append((text, meta))
        return bad[0][0], bad[1][0], bad[0][1], bad[1][1]

    @staticmethod
    def reports(a, b, am, bm):
        return {'readback': rb.read_d2(a, am), 'pair': dd.diff_d2_decks(a, b, am, bm),
                'plan': smoke.d2_plan_check(a, am)}

    def assert_refusal(self, result, reason):
        self.assertEqual(result['verdict'], 'FAIL', result)
        self.assertTrue(any(reason in f for f in result['failures']), result['failures'])
        self.assertFalse(result['execution_authorized'])

    def test_layered_max_seed_api_refuses_derived_overflow(self):
        for phases in (('AM_P', 'AM_S', 'SE'), ('AM_P', 'SE')):
            a, b, am, bm = self.overflow_pair(phases)
            self.assertIn('fix insB all insert/pack seed 2147483659 ', a)
            self.assertEqual(am['deck_sha256'], hashlib.sha256(a.encode()).hexdigest())
            self.assertEqual(bm['deck_bytes'], len(b.encode()))
            for consumer, result in self.reports(a, b, am, bm).items():
                with self.subTest(phases=phases, consumer=consumer):
                    self.assert_refusal(result, 'D2 insert/pack insB seed 2147483659: outside 1..2147483647')

    def test_layered_max_seed_three_cli_rc_one(self):
        for phases in (('AM_P', 'AM_S', 'SE'), ('AM_P', 'SE')):
            with tempfile.TemporaryDirectory() as temp:
                _write_case(temp, *self.overflow_pair(phases))
                for consumer, (rc, out, err) in _run_three_cli(temp).items():
                    with self.subTest(phases=phases, consumer=consumer):
                        self.assertEqual(rc, 1, out + err)
                        self.assertIn('D2 insert/pack insB seed 2147483659: outside 1..2147483647', out)
                        self.assertNotIn('Traceback', err)

    def test_each_actual_seed_range_and_primality(self):
        for index, fix_id in ((0, 'insA'), (1, 'insB')):
            for value, why in ((0, 'ASCII positive integer'), (-1, 'ASCII positive integer'),
                               (1, 'not prime'), (4, 'not prime'),
                               (2147483648, 'outside 1..2147483647'),
                               (2147483659, 'outside 1..2147483647')):
                decks = []
                for coated in (False, True):
                    text, meta, _ = fixture(coated=coated)
                    text, count = re.subn(r'(fix ' + fix_id + r' all insert/pack seed )\d+',
                                          lambda m: m[1] + str(value), text)
                    self.assertEqual(count, 1)
                    meta = rebound(text, meta)
                    if index == 0:
                        meta['seed'] = value
                    decks.append((text, meta))
                (a, am), (b, bm) = decks
                for consumer, result in self.reports(a, b, am, bm).items():
                    with self.subTest(fix=fix_id, value=value, consumer=consumer):
                        self.assert_refusal(result, f'D2 insert/pack {fix_id} seed {value}: {why}')

    def test_boundary_positive_api_and_cli(self):
        for phases in (('AM_P', 'AM_S', 'SE'), ('AM_P', 'SE')):
            for seed, layered in ((2147483647, False), (2147483629, True)):
                case = self.pair(seed=seed, layered=layered, phases=phases)
                if layered:
                    self.assertIn('fix insB all insert/pack seed 2147483647 ', case[0])
                for consumer, result in self.reports(*case).items():
                    with self.subTest(phases=phases, seed=seed, consumer=consumer):
                        self.assertEqual(result['verdict'], 'PASS', result)
                        self.assertFalse(result['execution_authorized'])
                with tempfile.TemporaryDirectory() as temp:
                    _write_case(temp, *case)
                    for consumer, (rc, out, err) in _run_three_cli(temp).items():
                        with self.subTest(phases=phases, seed=seed, cli=consumer):
                            self.assertEqual(rc, 0, out + err)

    def test_valid_but_wrong_second_prime_keeps_generator_binding(self):
        a, b, am, bm = self.pair(seed=2147483629)
        aa, bb = a.replace('insert/pack seed 2147483647 ', 'insert/pack seed 32452843 '), b.replace(
            'insert/pack seed 2147483647 ', 'insert/pack seed 32452843 ')
        for consumer, result in self.reports(aa, bb, rebound(aa, am), rebound(bb, bm)).items():
            with self.subTest(consumer=consumer):
                self.assert_refusal(result, '`32452843` (generator `2147483647`)')


if __name__ == '__main__':
    unittest.main(verbosity=2)
