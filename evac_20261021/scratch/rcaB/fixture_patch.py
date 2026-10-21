"""Apply the v2-certificate / exempt-marker fixture updates to a scratch copy of two test files (NOT the repo).

usage: python3 fixture_patch.py <scripts dir of a scratch tree>
Each replacement must match exactly once (else abort) — the same rule as the repo's mutation helper.
"""
import sys
from pathlib import Path

S = Path(sys.argv[1])
EDITS = {
    'test_ca_ext_b6.py': [(
        "            'dsigma_rel': 1e-12, 'resolve_info': 0, 'resolve_I_bot': 1.0, 'resolve_I_top': 1.0,\n"
        "            'pass_a': True, 'pass_b': True, 'pass_c': True, 'ok': True}\n",
        "            'dsigma_rel': 1e-12, 'resolve_info': 0, 'resolve_I_bot': 1.0, 'resolve_I_top': 1.0,\n"
        "            'pass_a': True, 'pass_b': True, 'pass_c': True, 'ok': True,\n"
        "            #  ★ 10-21 증서 v2 (Codex RCA-07 · RCA-13) — 상태 · ⓓ 목표량 증서 (구간 [1, 1] ∋ 게시 판 전류 1 · scale = σ)\n"
        "            'status': CC.STATUS_POSITIVE, 'pass_d': True, 'target_tol': CC.CERT_TARGET_TOL, 'target_version': CC.TARGET_VERSION,\n"
        "            'target_fp': CC.TARGET_FP_RULE, 'target_ledger_ok': True, 'target_topology': 'through', 'target_lo': 1.0,\n"
        "            'target_hi': 1.0, 'scale': float(sigma)}\n",
    )],
    'test_rint_r_chain.py': [
        ("              'cert': {'version': CC.CERT_VERSION, 'rtol_max': CC.CERT_RTOL_MAX, 'eps_I': CC.CERT_EPS_I,\n"
         "                       'resolve_tol': CC.CERT_RESOLVE_TOL}})\n",
         "              'cert': {'version': CC.CERT_VERSION, 'rtol_max': CC.CERT_RTOL_MAX, 'eps_I': CC.CERT_EPS_I,\n"
         "                       'resolve_tol': CC.CERT_RESOLVE_TOL, 'target_tol': CC.CERT_TARGET_TOL,\n"
         "                       'target_version': CC.TARGET_VERSION, 'target_fp': CC.TARGET_FP_RULE, 'status': CC.STATUS_POSITIVE}})\n"),
        ("            'sigma_resolve': si, 'dsigma_rel': 1e-9, 'resolve_info': 0, 'pass_a': True, 'pass_b': ok, 'pass_c': True, 'ok': ok,\n"
         "            'iters': 321, 'resolve_iters': 17}\n",
         "            'sigma_resolve': si, 'dsigma_rel': 1e-9, 'resolve_info': 0, 'pass_a': True, 'pass_b': ok, 'pass_c': True, 'ok': ok,\n"
         "            'iters': 321, 'resolve_iters': 17,\n"
         "            #  ★ 10-21 증서 v2 — 상태 · ⓓ (구간 [1, 1] ∋ 게시 판 전류 1 · scale = σ)\n"
         "            'status': CERT['status'], 'pass_d': True, 'target_tol': CERT['target_tol'], 'target_version': CERT['target_version'],\n"
         "            'target_fp': CERT['target_fp'], 'target_ledger_ok': True, 'target_topology': 'through', 'target_lo': 1.0,\n"
         "            'target_hi': 1.0, 'scale': si}\n"),
        ("                                     'diagnostics': cp_(T['fa_diag']), 'label': T['fa_label']}},\n",
         "                                     'diagnostics': cp_(T['fa_diag']), 'label': T['fa_label'],\n"
         "                                     'exempt_assumptions': cp_(T['fa_exempt'])}},\n"),
        ("                     'fa_volume': FA.volume_record(0.05, 0.06), 'vgcf_rule': S3.VGCF_SIGMA_RULE}\n",
         "                     'fa_volume': FA.volume_record(0.05, 0.06), 'vgcf_rule': S3.VGCF_SIGMA_RULE,\n"
         "                     'fa_exempt': dict(FA.EXEMPT_ASSUMPTIONS)}\n"),
    ],
}
for name, pairs in EDITS.items():
    p = S / name
    src = p.read_text(encoding='utf-8')
    for old, new in pairs:
        n = src.count(old)
        if n != 1:
            sys.exit(f'{name}: {n} matches for {old[:60]!r}')
        src = src.replace(old, new)
    p.write_text(src, encoding='utf-8')
    print(f'patched {name} ({len(pairs)} edits)')
