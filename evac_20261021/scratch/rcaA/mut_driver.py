#!/usr/bin/env python3
"""Source-line mutation driver (one mutant at a time, restore byte-exact, verify sha256).

  python3 -I mut_driver.py <worktree> <results.jsonl> M1 M2 ...

Per mutant: the file must contain `old` exactly once -> write mutated file -> run the test (nice 19 · 1 thread via nrun.py) ->
restore the original bytes (finally) -> assert sha256 == original -> append one JSON line (id, pass, total, failing check names)."""
import hashlib
import json
import os
import re
import subprocess
import sys
import time

WT = sys.argv[1]
OUT = sys.argv[2]
IDS = sys.argv[3:]
NRUN = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nrun.py')
CJ = 'scripts/carbon_junction.py'
S3 = 'scripts/step3_sigma.py'
CW = 'scripts/ca_ext_cjunc.py'
S0 = 'scripts/ca_s0_census.py'
TCJ = ['scripts/test_carbon_junction.py', '--quick']
TS0 = ['scripts/test_ca_s0_census.py']

MUTS = {
    'M1': (CJ, "        rep = np.arange(self.n_total)\n",
           "        rep = np.arange(self.n_total); [rep.__setitem__(self.pos_dof[_q], self.pos_dof[_p]) for _p, _q in "
           "np.asarray(reg.get('self_revisit_pairs', np.zeros((0, 2))), np.int64).reshape(-1, 2)]\n",
           TCJ, 'RCA-03 재방문 셀 안 합침 (옛 동작)'),
    'M2': (CJ, "    o = np.lexsort((ijk[:, 2], ijk[:, 1], ijk[:, 0]))\n",
           "    o = np.lexsort((-ijk[:, 2], -ijk[:, 1], -ijk[:, 0]))\n", TCJ, 'RCA-04 포트 동률 = 사전식 최대'),
    'M3': (CJ, "    bnd = cand[d2 <= m + CJUNC_EPS_D2_UM2]\n", "    bnd = cand[d2 <= m]\n", TCJ, 'RCA-04 포트 ε 띠 없앰 (정확 최소만)'),
    'M4': (CJ, "    keyed.sort(key=lambda t: t[0])\n", "    keyed.sort(key=lambda t: t[1])\n", TCJ, 'RCA-04 경로 순서 = fid'),
    'M5': (CJ, "    return max(2, int(math.ceil(r - CJUNC_LPAR_RTOL)))\n", "    return 1\n", TCJ, 'RCA-05 k = 1 (분산 끔)'),
    'M6': (CJ, "            g[e] = float(junction_g_code(r)) * float(mult[q]) / float(kk[q])",
           "            g[e] = float(junction_g_code(r)) * float(mult[q])", TCJ, 'RCA-05 간선 G 를 k 로 안 나눔 (계획만)'),
    'M7': (CJ, "            d2, _, _ = pt_seg_d2(np.repeat(scp[e][None], len(psegs['P0']), 0), psegs['P0'], psegs['P1'])\n",
           "            d2, _, _ = pt_seg_d2(np.repeat(cp[sub['inst'][e]][None], len(psegs['P0']), 0), psegs['P0'], psegs['P1'])\n",
           TCJ, 'RCA-05 PTFE 덮임 = instance 대표점 (간선마다 아님)'),
    'M8': (CJ, "            ds, _ = tree.query(scp)\n", "            ds, _ = tree.query(cp[sub['inst']])\n", TCJ,
           'RCA-05 SDCP 근접 = instance 대표점'),
    'M9': (CJ, "        if thr is not None and r_ is not None and r_ >= thr:\n",
           "        if r_ is not None and (thr is None or r_ >= thr):\n", TCJ, 'RCA-06 문턱 없이도 SV_DEPENDENT'),
    'M10': (CJ, "drop_cat=_CAT['sv_face'])\n", "drop_cat=None)\n", TCJ, 'RCA-06 반사실이 SV 면을 안 끊음'),
    'M11': (S3, "                    LAST_BACKEND.clear(); LAST_BACKEND.update(_bk0)\n", "                    pass\n", TCJ,
            'RCA-06 위생 ① 전역 출처 되돌림 없음'),
    'M12': (CJ, "            if certify is not None:\n", "            if False:\n", TCJ, 'RCA-06 위생 ② 반사실 증서 무시'),
    'M13': (CJ, "                rec.update(status='nonpositive_cut_current')",
            "                rec.update(status='no_through_without_sv', sv_counterfactual_ratio=math.inf)", TCJ,
            'RCA-06 위생 ③ 푼 I_cut ≤ 0 → inf (옛)'),
    'M14': (CJ, "        if not (math.isfinite(float(I_full)) and float(I_full) > 0.0):\n", "        if False:\n", TCJ,
            'RCA-06 위생 ④ 분자 ≤ 0 지킴 없음'),
    'M15': (CJ, "    rv_items = [x for x, it in enumerate(self_items) if it[4] == 0]\n",
            "    rv_items = [x for x, it in enumerate(self_items) if True]\n", TCJ, 'Q11 census 재방문 = 면 후보까지 셈'),
    'M16': (CJ, "        b = bnd[np.lexsort((j[bnd], i[bnd], mid[:, 2], mid[:, 1], mid[:, 0]))[0]]\n",
            "        b = mem[np.argmin(d[mem])]\n", TCJ, 'RCA-04/05 접점 = argmin 첫 쌍 (옛)'),
    'M17': (CW, "    elif (_lm == 1.0) != (n_sub == cnt['n_instances']):\n", "    elif False:\n", TCJ,
            '검증기 간선 수 ↔ 배율 결합 없음'),
    'M18': (CJ, "        keyed.append(((seq[0], seq[-1], seq), int(f), r, kp))\n", "        keyed.append((seq, int(f), r, kp))\n", TCJ,
            'RCA-04 경로 순서 키 끝점 뺌 (점열만)'),
    'M19': (CJ, "    if dup:\n        rej.append({'code': 'duplicate_path_reversed'",
            "    if False:\n        rej.append({'code': 'duplicate_path_reversed'", TCJ, 'RCA-04 역순 중복 거부 없음'),
    'M20': (S0, "'n_instances_ptfe_partial': cen.get('n_instances_ptfe_partial')", "'n_instances_ptfe_partial': 0", TS0,
            'S0 census 부분 덮임 instance 0 으로'),
    'M21': (CJ, "            if np.isfinite(xa).all() and np.isfinite(xb).all():\n", "            if False:\n", TCJ,
            'RCA-03 자기 접합 포트 = 옛 대표 항목 (기하 접점 아님)'),
    'M22': (CJ, "    if len(same) > 1:                                          # ③", "    if False:                                          # ③", TCJ,
            'RCA-04 같은 셀 여러 가지 = 중심선 거리 없이 (조각, 번호)'),
    'M23': (CJ, "        side = 1 if rJ[3] > rI[3] * (1.0 + CJUNC_LPAR_RTOL) else 0\n", "        side = 0\n", TCJ,
            'RCA-05 정의 쪽 = 늘 i'),
    'M24': (CJ, "        t = (j + 0.5) * L / k\n", "        t = j * L / k\n", TCJ, 'RCA-05 등분 칸 가운데 → 칸 시작'),
    'M25': (CJ, "    return Cb[np.lexsort((Cb[:, 2], Cb[:, 1], Cb[:, 0]))[0]]\n", "    return Cb[0]\n", TCJ,
            'RCA-05 맞은편 최근접점 띠 → 첫 점'),
    'M26': (CW, "    n_sub = cnt.get('n_subedges', cnt['n_instances'])\n", "    n_sub = cnt['n_instances']\n", TCJ,
            '검증기 n_subedges 무시'),
    'M27': (S3, "            if unconv:                                     #   주 해가 미수렴",
            "            if False:                                     #   주 해가 미수렴", TCJ, 'RCA-06 주 해 미수렴이어도 반사실'),
    'M28': (CJ, "    if not (r > 1.0 + CJUNC_LPAR_RTOL):\n", "    if not (r > 1.0):\n", TCJ,
            'RCA-05 k 문턱에서 1e-9 띠 뺌 (깊은 직교 교차 몇 ulp → k 2)'),
    'M29': (CJ, "    return len(Q) > 1 and _seq_less(np.asarray(Q)[::-1], Q)\n",
            "    return len(Q) > 1 and _seq_less(Q, np.asarray(Q)[::-1])\n", TCJ, 'RCA-04 정준 방향 판정 뒤집음'),
    'M30': (CJ, "    if not (math.isfinite(tf) and tf >= 1.0):\n", "    if not (math.isfinite(tf) and tf >= 0.0):\n", TCJ,
            'RCA-06 문턱 < 1 허용'),
    'M31': (CJ, "    if plan.get('sv_counterfactual') is not None:           # ★ 10-21 RCA-06",
            "    if False:           # ★ 10-21 RCA-06", TCJ, 'RCA-06 노브를 계획 지문에서 뺌'),
    'M32': (CJ, "'n_port_ties': int(np.sum(sub['tie_i']) + np.sum(sub['tie_j']))",
            "'n_port_ties': int(np.sum(sub['tie_j']))", TCJ, 'Q11 census 포트 동률 = j 쪽만'),
    'M34': (CJ, "            np.add.at(acc, qi, G[self._jidx] * dphi[self._jidx])\n",
            "            acc[qi] = G[self._jidx] * dphi[self._jidx]\n", TCJ, 'RCA-05 instance 접합 전류 = 마지막 간선만 (합 아님)'),
    'M36': (CJ, "    return max(2, int(math.ceil(r - CJUNC_LPAR_RTOL)))\n", "    return max(2, int(r))\n", TCJ,
            'RCA-05 k = floor (ceil 아님)'),
}


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def main():
    env = dict(os.environ)
    for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        env[k] = '1'
    for mid in IDS:
        f, old, new, test, desc = MUTS[mid]
        path = os.path.join(WT, f)
        orig = open(path, 'rb').read()
        h0 = hashlib.sha256(orig).hexdigest()
        txt = orig.decode('utf-8')
        n = txt.count(old)
        rec = {'id': mid, 'file': f, 'desc': desc, 'occurrences': n}
        if n != 1:
            rec['error'] = f'old string occurs {n} times'
            print(json.dumps(rec, ensure_ascii=False), flush=True)
            with open(OUT, 'a', encoding='utf-8') as fo:
                fo.write(json.dumps(rec, ensure_ascii=False) + '\n')
            continue
        t0 = time.time()
        try:
            open(path, 'wb').write(txt.replace(old, new).encode('utf-8'))
            p = subprocess.run([sys.executable, NRUN] + test, cwd=WT, env=env, capture_output=True, text=True, timeout=300)
            outp = p.stdout + p.stderr
        finally:
            open(path, 'wb').write(orig)
        assert sha(path) == h0, f'{mid}: restore failed'
        m = re.search(r'== test_carbon_junction: (\d+)/(\d+) PASS', outp) or re.search(r'(\d+) PASS · (\d+) FAIL', outp)
        if m and '==' in m.group(0):
            ok, tot = int(m.group(1)), int(m.group(2))
        elif m:
            ok, tot = int(m.group(1)), int(m.group(1)) + int(m.group(2))
        else:
            ok, tot = None, None
        fails = [ln.strip()[6:].split('  (')[0][:110] for ln in outp.splitlines() if ln.startswith('  FAIL')]
        exc = [ln.strip()[:160] for ln in outp.splitlines() if 'Error' in ln and ('Traceback' not in ln)][:3]
        rec.update(pass_=ok, total=tot, n_fail=(None if ok is None else tot - ok), fails=fails[:12], n_fails_listed=len(fails),
                   exceptions=exc, wall_s=round(time.time() - t0, 1), restored_sha_ok=True)
        print(json.dumps(rec, ensure_ascii=False), flush=True)
        with open(OUT, 'a', encoding='utf-8') as fo:
            fo.write(json.dumps(rec, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
