#!/usr/bin/env python3
import hashlib, json, subprocess, sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
OLD=(BASE/'baseline/make_mixer_deck.py').read_text()
NEW=(BASE/'scripts/make_mixer_deck.py').read_text()

def replace_once(src, old, new):
 assert src.count(old)==1,(old[:100],src.count(old))
 return src.replace(old,new,1)

def density(src):
 old="ced_ss = ced_for_bond(a['bo_se'], d['SE'] / 2.0, nu_se, (DENS if dens is None else dens)[mat_se], E=E['SE'])"
 return replace_once(src,old,old.replace('(DENS if dens is None else dens)[mat_se]', 'DENS[mat_se]'))

def metadata_bo(src):
 return replace_once(src,"gamma_wall=a_['gamma_wall'], bo_se=a_['bo_se'],", "gamma_wall=a_['gamma_wall'], bo_se=0.21244,")

def mixed(src):
 start=src.index('def _assert_ceiling_pairwise'); end=src.index('\n\ndef ',start+1)
 part=src[start:end]
 needle='            ov = pair_overlap(M[i][j], ti, tj, d, E)'
 assert needle in part
 part=part.replace(needle,"            if ti != tj and WALL not in (ti, tj):\n                continue\n"+needle)
 return src[:start]+part+src[end:]

def wall_binding(src):
 start=src.index("    if ARMS[arm].get('rule') == 'geomean':",src.index('def _require_dens_gen'))
 end=src.index('\n\ndef ',start)
 return src[:start]+src[end:]

def rho_match(src):
 start=src.index("        if not (all(v == rho for v in ncm) or all(v == 1.0 for v in ncm)):")
 end=src.index('        arm.update(',start)
 return src[:start]+src[end:]

def stale_metadata(src):
 return replace_once(src,"        meta.update(schema='mixer_deck_meta/2', registered=None, development_contract='D2-geomean/unregistered')\n",'')

def wall_comment(src):
 return replace_once(src,"    _wall_note = ('점착 = D2 기하평균 (비코팅 NCM 벽 규칙)' if ARMS[arm].get('rule') == 'geomean'\n                  else f'점착 = 입자값 ÷ {WALL_CED_DIV:.3f}')", "    _wall_note = f'점착 = 입자값 ÷ {WALL_CED_DIV:.3f}'")

cases=[('density_gen1',density,True),('meta_constant_bo',metadata_bo,True),('skip_mixed_ceiling',mixed,True),
 ('arm_name_match',lambda s:replace_once(s,'not _ARM_NAME_RE.fullmatch(name)','not _ARM_NAME_RE.match(name)'),False),
 ('cli_gamma_float',lambda s:replace_once(s,'_g[_k] = _gm_cli_number(_v)','_g[_k] = float(_v)'),False),
 ('allow_subnormal',lambda s:replace_once(s,'math.isfinite(v) and v >= sys.float_info.min','math.isfinite(v) and v > 0.0'),False),
 ('omit_wall_binding',wall_binding,False),('omit_rho_match',rho_match,False),
 ('stale_metadata',stale_metadata,False),('stale_wall_comment',wall_comment,False)]

def drop_desc_guard(src):
 start=src.index(r"    if not isinstance(desc, str) or '\n' in desc or '\r' in desc:")
 end=src.index('    arm = dict(desc=desc',start)
 return src[:start]+src[end:]

def two_ncm_only(src):
 return replace_once(src,"if not (all(v == rho for v in ncm) or all(v == 1.0 for v in ncm)):",
                     "if (g.get('AM_P'), g.get('AM_S')) not in ((rho, rho), (1.0, 1.0)):")

cases += [
 ('gravity_d2_only', lambda s: replace_once(s,'fix             gravi all gravity 9.81 vector',
  "fix             gravi all gravity {1.0 if ARMS[arm].get('rule') == 'geomean' else 9.81} vector"),False),
 ('reader_gravity_constant', lambda s: replace_once(s,
  'weight = (4.0/3.0) * math.pi * radius**3 * density * gravity_magnitude',
  'weight = (4.0/3.0) * math.pi * radius**3 * density * 9.81'),False),
 ('active_phases_regression', two_ncm_only,False),
 ('description_guard_removed',drop_desc_guard,False),
 ('cli_wall_float',lambda s:replace_once(s,"ap.add_argument('--gm-wall-ncm', type=_gm_cli_number", "ap.add_argument('--gm-wall-ncm', type=float"),False),
 ('cli_bo_float',lambda s:replace_once(s,"ap.add_argument('--gm-bo-se', type=_gm_cli_number", "ap.add_argument('--gm-bo-se', type=float"),False),
]

expected = {
 'density_gen1':'MXD02', 'meta_constant_bo':'MXD02', 'skip_mixed_ceiling':'MXD03',
 'arm_name_match':'MXD04 terminal', 'cli_gamma_float':'MXD04 CLI', 'allow_subnormal':'MXD04 subnormal',
 'omit_wall_binding':'MXD05 production', 'omit_rho_match':'MXD05 uncoated',
 'stale_metadata':'MXD06', 'stale_wall_comment':'MXD06', 'gravity_d2_only':'MXD02',
 'reader_gravity_constant':'MXDR1', 'active_phases_regression':'MXDR2',
 'description_guard_removed':'MXDR3', 'cli_wall_float':'MXDR4', 'cli_bo_float':'MXDR4',
}
clean=subprocess.run([sys.executable,'-I',str(BASE/'scripts/make_mixer_deck.py'),'--selftest'],capture_output=True,text=True)
(BASE/'logs/mutation-v2-clean.log').write_text(clean.stdout+clean.stderr)
assert clean.returncode==0, 'Unmutated source must pass before mutation evidence is valid'
rows=[]
for name, mutate, baseline in cases:
 for version,source in ([('before',OLD)] if baseline else [])+[('after',NEW)]:
  here=BASE/'mutants'/name/version
  here.mkdir(parents=True,exist_ok=True)
  (here/'make_mixer_deck.py').write_text(mutate(source))
  link=here/'additives.py'
  if not link.exists(): link.symlink_to(BASE/'scripts/additives.py')
  proc=subprocess.run([sys.executable,'-I',str(here/'make_mixer_deck.py'),'--selftest'],capture_output=True,text=True)
  logfile=BASE/'logs'/f'mutation-{name}-{version}.log';logfile.write_text(proc.stdout+proc.stderr)
  fails=[ln.strip() for ln in proc.stdout.splitlines() if ln.startswith('  FAIL')]
  row={'mutation':name,'version':version,'rc':proc.returncode,'failures':fails,'log':str(logfile), 'source_sha256':hashlib.sha256(source.encode()).hexdigest(), 'mutant_sha256':hashlib.sha256((here/'make_mixer_deck.py').read_bytes()).hexdigest()}
  rows.append(row); print(json.dumps(row,ensure_ascii=False),flush=True)
  if version=='before': assert proc.returncode==0,(name,proc.returncode,fails)
  else: assert proc.returncode!=0 and any(expected[name] in f for f in fails),(name,proc.returncode,fails)
(BASE/'mutation-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print(f'PASS: {len(cases)} explicit mutations killed; 3 known historical weakness analogues pass old 143-check suite.')
