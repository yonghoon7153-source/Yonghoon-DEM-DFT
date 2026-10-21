"""PRE-impl-07 fixture updates for tests outside agent B's files (main applies the patch):
  scripts/test_ca_ext_b6.py   — synthetic junction manifest fingerprints = lowercase hex 32 · good_cert carries the binding fields ·
                                 conv_cert_problem called with the manifest (new required argument)
  scripts/test_rint_r_chain.py — fake runner certificate carries the binding fields read from the same arm's manifest

usage: python3 fixture_patch_b7.py <tree root> [--write-patch OUT]
Edits the two files in <tree root>/scripts (in place) — run it on a scratch copy, then diff against the worktree.
"""
import difflib
import os
import sys

root = sys.argv[1]
out = sys.argv[sys.argv.index('--write-patch') + 1] if '--write-patch' in sys.argv else None

B6 = [
    ("CJ_REQ = dict(R_j_ohm=1.0e6, len_law='len_scaled_v0', unreg_law='cut', s_min_um=0.5, tol_ff_um=0.5, ptfe_jlaw='P0')\n",
     "CJ_REQ = dict(R_j_ohm=1.0e6, len_law='len_scaled_v0', unreg_law='cut', s_min_um=0.5, tol_ff_um=0.5, ptfe_jlaw='P0')\n"
     "#: ★ 10-21 (사전 리뷰 PRE-impl-07) — 합성 접합 매니페스트의 지문 칸 (소문자 hex 32 · 증서 결합 `run_contract.cert_binding_problem` 이\n"
     "#:   이 칸과 대조한다 — `good_cert` 가 같은 값을 싣는다)\n"
     "CJ_FP = {'registry': 'a' * 32, 'sid': 'b' * 32, 'plan_rows': 'c' * 32}\n"),
    ("    fp = {'registry': 'r' * 32, 'sid': 's' * 32, 'plan_rows': 'p' * 32}\n", "    fp = dict(CJ_FP)\n"),
    ("def good_cert(sigma, rtol=1.0e-12):\n", "def good_cert(sigma, rtol=1.0e-12, channel='electronic'):\n"),
    ("            'target_hi': 1.0, 'scale': float(sigma)}\n",
     "            'target_hi': 1.0, 'scale': float(sigma),\n"
     "            #  ★ 10-21 (PRE-impl-07) — 증서 ↔ 런 결합 칸 = `cj_manifest` 의 지문 (접합 = 주 전자 솔브만 · face_alpha 없음)\n"
     "            'bind_version': CC.BIND_VERSION, 'fp_sid': CJ_FP['sid'], 'fp_sig': 'd' * 32, 'fp_face_plan': None,\n"
     "            'fp_cjunc_registry': (CJ_FP['registry'] if channel == 'electronic' else None),\n"
     "            'fp_cjunc_rows': (CJ_FP['plan_rows'] if channel == 'electronic' else None)}\n"),
    ("    chk('R13a 증서 정상 → 문제 없음', RC.conv_cert_problem(good_cert(0.05), 0.05) is None, RC.conv_cert_problem(good_cert(0.05), 0.05))\n",
     "    chk('R13a 증서 정상 → 문제 없음', RC.conv_cert_problem(good_cert(0.05), 0.05, m) is None,\n"
     "        RC.conv_cert_problem(good_cert(0.05), 0.05, m))\n"),
    ("        chk(f'R13b 증서 거부 [{nm}]', RC.conv_cert_problem(fn(good_cert(0.05)), 0.05) is not None)\n",
     "        chk(f'R13b 증서 거부 [{nm}]', RC.conv_cert_problem(fn(good_cert(0.05)), 0.05, m) is not None)\n"),
    ("        not RC.next_gen_cert_ok(s3i)[0] and RC.next_gen_cert_ok(dict(s3i, ion_conv_cert=good_cert(0.001)))[0])\n",
     "        not RC.next_gen_cert_ok(s3i)[0] and RC.next_gen_cert_ok(dict(s3i, ion_conv_cert=good_cert(0.001, channel='ionic')))[0])\n"),
    ("            and RC.ca_ext_record_ok(mfr) == (True, None) and RC.conv_cert_problem(cert, s3_of(p_fr).get('sigma_e_eff_S_cm')) is None,\n",
     "            and RC.ca_ext_record_ok(mfr) == (True, None) and RC.conv_cert_problem(cert, s3_of(p_fr).get('sigma_e_eff_S_cm'), mfr) is None,\n"),
    ("            and RC.conv_cert_problem(cert2, s3_of(p_cr).get('sigma_e_eff_S_cm')) is None and RC.next_gen_cert_ok(s3_of(p_cr))[0],\n",
     "            and RC.conv_cert_problem(cert2, s3_of(p_cr).get('sigma_e_eff_S_cm'), mcr) is None and RC.next_gen_cert_ok(s3_of(p_cr))[0],\n"),
]

CHAIN = [
    ("def cert(si):\n", "def cert(si, man):\n"),
    ("            'target_hi': 1.0, 'scale': si}\n",
     "            'target_hi': 1.0, 'scale': si,\n"
     "            #  ★ 10-21 (사전 리뷰 PRE-impl-07) — 증서 ↔ 런 결합 칸 = 그 팔 매니페스트의 정본 지문 (접합 원장 sid · registry · plan_rows ·\n"
     "            #    face_alpha 전자 계획) · σ 표 지문 = 킷마다 (가짜)\n"
     "            **_bind(man)}\n"
     "\n"
     "\n"
     "def _bind(man):\n"
     "    ca = man.get('ca_ext') or {}\n"
     "    cjf = ((ca.get('cjunc') or {}).get('evidence') or {}).get('fp') or {}\n"
     "    faf = ((ca.get('ptfe_face') or {}).get('evidence') or {}).get('fp') or {}\n"
     "    return {'bind_version': CERT['bind_version'], 'fp_sid': cjf.get('sid', faf.get('sid_off')), 'fp_sig': hx('sig|' + kit),\n"
     "            'fp_face_plan': faf.get('plan_electronic'), 'fp_cjunc_registry': cjf.get('registry'),\n"
     "            'fp_cjunc_rows': cjf.get('plan_rows')}\n"),
    ("          'status': 'complete', 'manifest': manifest(i, si), 'conv_cert': cert(si), 'cg_iters': 321}\n",
     "          'status': 'complete', 'manifest': None, 'conv_cert': None, 'cg_iters': 321}\n"
     "    st['manifest'] = manifest(i, si)\n"
     "    st['conv_cert'] = cert(si, st['manifest'])\n"),
    ("                       'target_version': CC.TARGET_VERSION, 'target_fp': CC.TARGET_FP_RULE, 'status': CC.STATUS_POSITIVE}})\n",
     "                       'target_version': CC.TARGET_VERSION, 'target_fp': CC.TARGET_FP_RULE, 'status': CC.STATUS_POSITIVE,\n"
     "                       'bind_version': CC.BIND_VERSION}})\n"),
]

diffs = []
for rel, reps in (('scripts/test_ca_ext_b6.py', B6), ('scripts/test_rint_r_chain.py', CHAIN)):
    p = os.path.join(root, rel)
    old = open(p, encoding='utf-8').read()
    s = old
    for a, b in reps:
        n = s.count(a)
        if n != 1:
            raise SystemExit(f'{rel}: anchor found {n} times: {a[:90]!r}')
        s = s.replace(a, b)
    open(p, 'w', encoding='utf-8').write(s)
    diffs.append(''.join(difflib.unified_diff(old.splitlines(True), s.splitlines(True), f'a/{rel}', f'b/{rel}')))
if out:
    open(out, 'w', encoding='utf-8').write(''.join(diffs))
print('ok', [len(d.splitlines()) for d in diffs])
