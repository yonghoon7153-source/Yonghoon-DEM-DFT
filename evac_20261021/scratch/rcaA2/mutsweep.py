"""One-line source mutants of the A2 implementation — each must make a named test fail (for the right reason).
Runs the worktree tests through drv.py with a temp impl dir (one file mutated).  Writes a JSON table."""
import json
import os
import shutil
import subprocess
import sys
import tempfile

D = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2/'
IMPL = sys.argv[1] if len(sys.argv) > 1 else D + 'impl'
OUT = sys.argv[2] if len(sys.argv) > 2 else D + 'logs/mutsweep.json'
CJ, CW, S0, S3 = 'carbon_junction.py', 'ca_ext_cjunc.py', 'ca_s0_census.py', 'step3_sigma.py'
MUTS = [
    ('M01 조각 = fid 규칙 (서로 다른 섬유 = fid 다름만)', CJ, "return segs['piece'][i] != segs['piece'][j]",
     "return segs['fid'][i] != segs['fid'][j]", 'cj', 'GAP'),
    ('M02 바닥 = s > D 만', CJ, 'return (s > float(D)) & (s > 0.5 * math.pi * d)', 'return (s > float(D))', 'cj', 'FLOOR,KINK'),
    ('M03 고리 이음매 별칭 끔', CJ, 'return bool(is_ring and len(cu) >= 2 and np.array_equal(cu[0], cu[-1]))', 'return False', 'cj', 'RING'),
    ('M04 포트 후보 = 살아있는 위치만 (옛 옮김)', CJ, '    a0, a1 = piece_pos[piece]\n    return np.arange(a0, a1)\n',
     "    a0, a1 = piece_pos[piece]\n    c_ = np.arange(a0, a1)\n    return c_[pos['live'][c_]]\n", 'cj', 'QC'),
    ('M05 SV 반사실 = 성분 SV 면 전부 끊음', CJ, 'cut |= m & ~pas', 'cut |= m', 'cj', 'QD'),
    ('M06 닫힌 경로 이음매 잇기 끔', CJ, 'joined = bool(closed and len(ixs) >= 2)', 'joined = False', 'cj', 'RING'),
    ('M07 덮인 포트 = 그대로 실현 (미실현 안 함)', CJ, "    if not pos['live'][p]:\n        lin = int(pos['lin'][p])",
     "    if False:\n        lin = int(pos['lin'][p])", 'cj', 'QC'),
    ('M08 같은 조각 면 연속 판정 끔 (늘 접촉)', CJ, "            if bool(np.asarray(_continuity(s_f, d_f, D, thr['s_min_um']))):",
     '            if False:', 'cj', 'KINK,KINK-R'),
    ('M09 SV 무리 \'지남\' = 사이 위치 살아있음 (뒤집음)', CJ, "if len(btw) and np.all(~pos['live'][btw])",
     "if len(btw) and np.all(pos['live'][btw])", 'cj', 'QD'),
    ('M10 자기 L_c = 두 쪽 선분 전부 짝 (접합 쌍 제한 끔)', CJ, '        si = np.searchsorted(su, S); qi = np.searchsorted(qu, Q)\n',
     '        si = np.repeat(np.arange(len(su)), len(qu)); qi = np.tile(np.arange(len(qu)), len(su))\n', 'cj',
     'KINK,RCA03,SELFD,REC,CEN'),
    ('M11 고리 s 둘레 짧은 쪽 끔', CJ, '    s = np.where(L > 0.0, np.minimum(s, L - s), s)\n    fl = np.asarray(_self_floor(s, d, D), bool)',
     '    fl = np.asarray(_self_floor(s, d, D), bool)', 'cj', 'RING'),
    ('M12 쌍 무리 고리 둘레 잇기 끔', CJ, '                if rg:\n                    a_, b_ = a_ % n_, b_ % n_',
     '                if False:\n                    a_, b_ = a_ % n_, b_ % n_', 'cj', 'RING'),
    ('M13 조립기 이음매 별칭 dof 끔', CJ, '        self.pos_dof[al] = self.pos_dof[alias[al]]\n', '', 'cj', 'RING'),
    ('M14 SV 다리 표지 0 (끊을 것 없음)', CJ, '    cut[rows[mask]] = True\n', '', 'cj', 'QD'),
    ('M15 계획 centerline 거부 끔', CJ, "    if ptfe_stamp == 'centerline':\n        raise ValueError('cjunc_plan: 접합 + ptfe_stamp centerline",
     "    if False:\n        raise ValueError('cjunc_plan: 접합 + ptfe_stamp centerline", 'cj', 'QC'),
    ('M16 솔브 입구 centerline 거부 끔', CJ, "    if plan.get('ptfe_stamp') not in ('off', 'face_alpha') or",
     "    if False and plan.get('ptfe_stamp') not in ('off', 'face_alpha') or", 'cj', 'QC'),
    ('M17 protocol centerline 받음', CW, "    if ptfe_stamp not in ('off', 'face_alpha'):",
     "    if ptfe_stamp not in ('off', 'centerline', 'face_alpha'):", 'cj', 'QC'),
    ('M18 자기 포트 후보 = 조각 전부 (쪽 제한 끔)', CJ,
     "            ci = _side_cand(allinst['seg_i'][k], int(allinst['piece_i'][k]), pos, piece_pos)\n"
     "            cj = _side_cand(allinst['seg_j'][k], int(allinst['piece_j'][k]), pos, piece_pos)\n",
     "            ci = _piece_cand(int(allinst['piece_i'][k]), pos, piece_pos)\n"
     "            cj = _piece_cand(int(allinst['piece_j'][k]), pos, piece_pos)\n", 'cj', 'RCA03,CEN,KINK-R,SELFD,KINK'),
    ('M19 자기 분산판 맞은편 = 짝 제한 끔', CJ, '                    m_ = pb[pa == Xs[j]]\n', '                    m_ = pb\n', 'cj',
     'SELFD,RCA03,KINK,RING,CEN'),
    ('M20 미수렴 반사실 종류 = 옛 문자열', S3, "{'kind': _cjm.CJUNC_SV_CF_KIND, 'rule'", "{'kind': 'counterfactual_cut_sv_faces', 'rule'",
     'cj', 'RCA06'),
    ('M21 S0 해시 = 문서 어디에든 (옛)', S0, "    if _row_value(doc, 'S0 계획 해시') != h:", '    if h not in doc:', 's0', 't_plan_commit'),
    ('M22 두 계획 tol_ff 대조 끔', S0, "    if robj['tol_ff_um'] != plan['values_um']['tol_ff']:", '    if False:', 's0', 't_plan_commit'),
    ('M23 두 계획 len_law 대조 끔', S0, "    if robj['len_law'] != cj.CJUNC_LEN_LAW:", '    if False:', 's0', 't_plan_commit'),
    ('M24 R 런 계획 파일 sha 대조 끔', S0, '        if hashlib.sha256(rpb).hexdigest() != r_hash:', '        if False:', 's0', 't_plan_commit'),
    ('M25 단계 2 --r-plan-path 필수 끔', S0, '        if not threshold_commit or not plan_path or not r_plan_path:',
     '        if not threshold_commit or not plan_path:', 's0', 't_plan_commit'),
    ('M26 같은 셀 재방문 = 별칭 짝도 셈', CJ,
     "                if pos['piece'][p] != pos['piece'][q] or int(pos['alias'][p]) == q or int(pos['alias'][q]) == p:",
     "                if pos['piece'][p] != pos['piece'][q]:", 'cj', 'RING'),
    ('M27 경로로만 = 경로 끊김 검사 끔', CJ, "        if np.all(pos['live'][a0_:a1_ + 1]):", '        if True:', 'cj', 'CEN,KINK-R,RCA03,QD,QC'),
]


def run(tmpd, kind, tags):
    if kind == 'cj':
        cmd = [sys.executable, D + 'drv.py', '--impl', tmpd, '--', '--only', tags]
    else:
        cmd = [sys.executable, D + 'run_s0_groups.py', '--impl', tmpd] + tags.split(',')
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1')
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=900, env=env,
                       cwd='/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee')
    out = p.stdout + p.stderr
    fails = [ln.strip() for ln in out.splitlines() if ln.strip().startswith('FAIL ') or ln.strip().startswith('FAIL:')]
    summ = [ln for ln in out.splitlines() if 'PASS' in ln and ('test_carbon_junction:' in ln or ' FAIL' in ln)]
    return p.returncode, fails, (summ[-1] if summ else out[-300:])


rows = []
base = {}
for kind, tags in sorted({(m[4], m[5]) for m in MUTS}):
    base[(kind, tags)] = run(IMPL, kind, tags)
for nm, fn, old, new, kind, tags in MUTS:
    tmpd = tempfile.mkdtemp(prefix='a2mut_')
    try:
        for f in os.listdir(IMPL):
            if f.endswith('.py'):
                shutil.copy(os.path.join(IMPL, f), tmpd)
        src = open(os.path.join(tmpd, fn), encoding='utf-8').read()
        c = src.count(old)
        if c != 1:
            rows.append({'mutant': nm, 'file': fn, 'error': f'snippet count {c}'})
            print(nm, 'SNIPPET', c, flush=True)
            continue
        open(os.path.join(tmpd, fn), 'w', encoding='utf-8').write(src.replace(old, new))
        rc, fails, summ = run(tmpd, kind, tags)
        b = base[(kind, tags)]
        rows.append({'mutant': nm, 'file': fn, 'tests': tags, 'base_rc': b[0], 'base_summary': b[2], 'rc': rc, 'summary': summ,
                     'caught': rc != 0 and b[0] == 0, 'fails': fails[:6]})
        print(nm, '→', 'CAUGHT' if (rc != 0 and b[0] == 0) else 'NOT CAUGHT', '|', summ, flush=True)
    finally:
        shutil.rmtree(tmpd, ignore_errors=True)
json.dump({'impl': IMPL, 'base': {f'{k[0]}:{k[1]}': v[2] for k, v in base.items()}, 'rows': rows}, open(OUT, 'w'),
          ensure_ascii=False, indent=1)
print('wrote', OUT)
