"""조건 8 (Codex 재리뷰 2026-08-25) — **단일 되돌림** 돌연변이 배터리.

각 수정에 대해 **그 하나만** 옛 코드로 되돌린 사본을 만들고, 대응 selftest 가
빨간불을 내는지 본다.  통과하는 회귀는 인증되지 않은 회귀다 (규칙 D 의 교훈).

    python3 scripts/mutation_sweep_20260825.py

⚠ 느리다 (~10 분) — 규칙 J 스모크가 팔마다 payload 를 실제로 돌린다.  그래서
  `check_all.sh` 에 넣지 않는다.  **수정을 추가할 때 손으로 돌리고 결과를 원장에 적는다.**
⚠ needle 이 안 맞으면 (`NEEDLE?`) 그것 자체가 실패다 — 코드가 움직였는데 이 배터리가
  낡은 것이므로, 돌연변이를 갱신하기 전에는 "적발" 을 주장할 수 없다.
"""
import subprocess, sys, tempfile, os, shutil, json
REPO = os.path.abspath('.')

# (라벨, 대상파일, 옛코드, 새코드, 이 돌연변이를 잡아야 하는 selftest 명령)
VERDICT = [sys.executable, 'scripts/sdcp_gain_verdict.py', '--selftest']
DISC    = [sys.executable, 'scripts/check_method_discipline.py', '--selftest']
STEP3   = [sys.executable, 'scripts/step3_sigma.py', '--selftest']

M = [
 ('조건5 compare_dirs 계약 제거', 'sdcp_gain_verdict.py',
  """    for _tag, _ar in (('A', arms_a), ('B', arms_b)):
        _h, _ = validate_contract(_ar, where=f'디렉터리 {_tag}')
        if _h:
            return dict(out, **_h)
""", '', VERDICT),
 ('조건5 where 접두사 제거', 'sdcp_gain_verdict.py',
  """    if _h and where and _h.get('reason'):
        _h = dict(_h, reason=f'[{where}] ' + _h['reason'])
""", '', VERDICT),
 ('조건3 전자 수렴 게이트 제거', 'sdcp_gain_verdict.py',
  "    if _eb:\n        return dict(decision='HOLD', hold_code='ELECTRONIC_CONV',",
  "    if False:\n        return dict(decision='HOLD', hold_code='ELECTRONIC_CONV',", VERDICT),
 ('조건3 resid 문턱 제거', 'sdcp_gain_verdict.py',
  "    if rs != rs or rs in (float('inf'), float('-inf')) or rs < 0 or rs > CG_RESID_MAX:",
  "    if False:", VERDICT),
 ('조건4 periodic_xy 규약축 제거', 'mpm_webapp_payload.py',
  "                   'periodic_xy', 'plate_rule')", "                   'plate_rule')", VERDICT),
 ('조건6 아래판 occupied-first 되돌림', 'step3_sigma.py',
  "    bot_m = any_c & _surf_bot_cond & (zc[k_first] - z_b <= band_bot)",
  "    _kfc = np.argmax(cond, axis=2)\n    bot_m = any_c & cond.any(2) & (zc[_kfc] - z_b <= band_bot)\n    k_first = np.where(cond.any(2), _kfc, k_first)", STEP3),
 ('조건6 반응솔버 되돌림', 'step3_sigma.py',
  "    bot_e = _any_o & cond_e[_iir, _jjr, _kf] & (zc[_kf] - z_b <= band)",
  "    _kfe = np.argmax(cond_e, axis=2)\n    bot_e = cond_e.any(2) & (zc[_kfe] - z_b <= band)\n    _kf = np.where(cond_e.any(2), _kfe, _kf)", STEP3),
 ('조건6 plate 소산 vox 인자 제거', 'step3_sigma.py',
  "    _use_plate = True\n    _u = float(_vox)", "    _use_plate = True\n    _u = 1.0", STEP3),
 ('조건6 원장 fail-open 되돌림', 'step3_sigma.py',
  """    if _pe is None or _vox is None:
        raise ValueError('phase_current_share: 플레이트 원장이 없다 (plate_edges/vox_um) — '
                         'solve_sigma_z 의 새 res 를 쓸 것.  없이 계산하면 소산 분담이 '
                         '내부 면만 세어 항등식 w_a = ∂ln σ_eff/∂ln σ_a 를 깬다 (CDXR2-1).  '
                         '조용히 옛 값으로 돌아가지 않는다 (fail-closed)')
    _use_plate = True
    _u = float(_vox)""",
  """    _use_plate = _pe is not None and _vox is not None
    _u = float(_vox) if _use_plate else 1.0""", STEP3),
 ('조건7 규칙K 옛 부분문자열', 'check_method_discipline.py',
  "            _hit = any(k_live_invocation(ln, _base, _flag) for ln in _txt.splitlines())",
  "            _hit = any(_base in ln and _flag in ln for ln in _txt.splitlines())", DISC),
 ('SELF-01 vox_um 매니페스트 제거', 'mpm_webapp_payload.py',
  "            'vox_um': float(a.step3_vox),\n            #  ★★ 2026-08-25 (Codex 재리뷰 조건 4)",
  "            #  ★★ 2026-08-25 (Codex 재리뷰 조건 4)", DISC),
 ('조건2 게시-전-검증 되돌림', 'mpm_webapp_payload.py',
  """    _fail_reason = _payload_reject_reason(a, step3)
    if _fail_reason:
        _bad = a.out + '.failed'
        _os_w2.replace(_part, _bad)""",
  """    _os_w2.replace(_part, a.out)
    _fail_reason = _payload_reject_reason(a, step3)
    if _fail_reason:
        _bad = a.out + '.failed'""", DISC),
]

rows = []
for label, fname, old, new, cmd in M:
    src = open(os.path.join(REPO, 'scripts', fname)).read()
    if src.count(old) != 1:
        rows.append((label, 'NEEDLE?', f'{src.count(old)}회'))
        continue
    d = tempfile.mkdtemp(); os.mkdir(os.path.join(d, 'scripts'))
    for f in os.listdir(os.path.join(REPO, 'scripts')):
        if f == fname: continue
        os.symlink(os.path.join(REPO, 'scripts', f), os.path.join(d, 'scripts', f))
    open(os.path.join(d, 'scripts', fname), 'w').write(src.replace(old, new))
    for top in ('docs', '.github', 'wiki', 'CLAUDE.md'):
        if os.path.exists(os.path.join(REPO, top)):
            os.symlink(os.path.join(REPO, top), os.path.join(d, top))
    r = subprocess.run([cmd[0], os.path.join(d, cmd[1]), *cmd[2:]],
                       capture_output=True, text=True, timeout=2400, cwd=d)
    out = r.stdout + r.stderr
    fails = [l.strip() for l in out.split('\n')
             if ('FAIL' in l and not l.strip().startswith('SELFTEST'))]
    rows.append((label, '적발' if (r.returncode != 0) else '★놓침★',
                 f'{len(fails)}건' + (f' — {fails[0][:64]}' if fails else ' (exit만)')))
    shutil.rmtree(d, ignore_errors=True)

print(f'{"돌연변이":<34} {"결과":<8} 적발 회귀')
print('-' * 108)
for a, b, c in rows:
    print(f'{a:<34} {b:<8} {c}')
missed = [a for a, b, _ in rows if b != '적발']
print()
print('놓친 돌연변이:', missed or '없음')
