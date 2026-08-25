"""**단일 되돌림 돌연변이 배터리** — 각 수정 하나만 옛 코드로 되돌려 회귀가 무는지 본다.

    python3 scripts/mutation_sweep_20260825.py

★★★ 2026-08-25 (R3-CX-08, Codex 3차) — **초판 harness 는 주장 대부분을 보증하지 않았다.**
  Codex 지적 그대로:
    · baseline(수정 전 상태에서 PASS)을 **먼저 고정하지 않았다**
    · **어떤 nonzero 든** "적발" 로 셌다 (import 오류·문법 오류·timeout 도 적발이 됐다)
    · **의도한 그 시험**이 실패했는지 확인하지 않았다 (다른 시험이 대신 물어도 초록)
    · needle 이 안 맞으면 조용히 넘어갔다 (`NEEDLE?` 만 찍고 계속)
  ⇒ mutant 마다 **기대 시험 id** 를 선언하고 넷을 다 본다:
      ⓐ baseline 이 정말 PASS 인가 (아니면 `HARNESS_ERROR`)
      ⓑ 기대한 시험이 **실제로** FAIL 했는가
      ⓒ **기대 밖 실패가 0** 인가 (과잉 커버리지 = 시험이 서로 얽혔다는 신호)
      ⓓ 실패가 코드 결함인가, harness 사고인가 (import/문법/timeout 은 따로 분류)

⚠ 느리다 (~15 분) — 규칙 J 스모크가 팔마다 payload 를 실제로 돌린다.  그래서
  `check_all.sh` 에 넣지 않는다.  수정을 추가할 때 손으로 돌리고 결과를 원장에 적는다.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

VERDICT = ('sdcp_gain_verdict.py', '--selftest')
DISC = ('check_method_discipline.py', '--selftest')
STEP3 = ('step3_sigma.py', '--selftest')
SR01 = ('sr01_stamp_compare.py', '--selftest')
RC = ('run_contract.py', '--selftest')

#: (라벨, 대상파일, 옛코드, 새코드, 시험 명령, **기대 시험 id 접두사들**)
#  ⚠ 기대 id 는 **정확히** 그 시험이 물어야 한다는 선언이다.  다른 시험이 대신 물면
#    그것은 통과가 아니라 "시험이 얽혀 있다" 는 보고다 (과잉 커버리지).
MUTANTS = [
    ('CX-01 payload 자리를 옛 `metrics` 오타로', 'run_contract.py',
     "STEP3_PATHS = (('mpm_metrics', 'step3'), ('step3',))",
     "STEP3_PATHS = (('metrics', 'step3'), ('step3',))",
     DISC, ('J-1',)),
    ('CX-03 규약 재계산 대조 제거', 'run_contract.py',
     "    if stored != recomputed:", "    if False:",
     VERDICT, ('㊱h',)),
    ('CX-03 키 부재 ↔ 명시 OFF 합침', 'run_contract.py',
     "        if k not in man:\n            _miss.append(k)                       # ★ 키 부재 = 모름 (OFF 가 아니다)\n            continue",
     "        if k not in man:\n            _v[k] = '__OFF__'\n            continue",
     VERDICT, ('㊱i', '㉒', '㊱b', '㊱g')),
    ('CX-05 cg_info 타입 검사를 옛 isinstance 로', 'run_contract.py',
     "    if type(cg_info) is not int:                       # noqa: E721 — bool/float 를 막는 것이 목적",
     "    if isinstance(cg_info, bool) or not isinstance(cg_info, (int, float)):",
     RC, ('B2', 'C2')),
    #  ⚠ **faithful** 이어야 한다: 옛 결함은 component 자신의 backend 가 **없을 때**
    #    다른 component 로 내려간 것이다.  `c.get(comp) or …` 로 쓰면 component dict 가
    #    존재하기만 하면 폴백이 안 일어나 mutant 가 무력하다 (초판이 그랬다).
    ('CX-05 backend 폴백 부활', 'run_contract.py',
     "    b = v.get('backend')",
     "    b = v.get('backend') or (c.get('ionic') or {}).get('backend') \\\n"
     "        or ((step3 or {}).get('manifest') or {}).get('backend_last_solve')",
     RC, ('D2',)),
    ('CX-05 수치 증거 검사 제거', 'run_contract.py',
     "    ok, why = conv_ok(s.get('cg_info'), s.get('unconverged'), s.get('cg_resid'))\n    if not ok:",
     "    ok, why = conv_ok(s.get('cg_info'), s.get('unconverged'), s.get('cg_resid'))\n    if False:",
     RC, ('C2',)),
    ('CX-04 required 를 계획에서 파생하지 않음', 'run_contract.py',
     "    if isinstance(plan, dict) and plan:\n        return tuple(_MAP[k] for k in _MAP if plan.get(k))",
     "    if False:\n        return ()",
     RC, ('E3',)),
    ('CX-06 파생 필드 자동 허용 제거', 'sdcp_gain_verdict.py',
     "                if FIELD_CONTRACT.get(fld, {}).get('derived_from') and not same:",
     "                if False:",
     VERDICT, ('㊶a', '㉗a', '㉗d')),
    ('CX-07① 반응 ionic-top 을 옛 규약으로 (faithful)', 'step3_sigma.py',
     "    top_i = _any_o & cond_i[_iir, _jjr, _kl] & (np.abs(z_plate - zc[_kl]) <= band)  # 분리막 접점",
     "    _kli = nz - 1 - np.argmax(cond_i[:, :, ::-1], axis=2)\n"
     "    _kl = np.where(cond_i.any(2), _kli, _kl)\n"
     "    top_i = cond_i.any(2) & (np.abs(z_plate - zc[_kl]) <= band)",
     STEP3, ('plate-rxn-grid',)),
    ('CX-07② occupied surface 에서 sid 5 제외', 'step3_sigma.py',
     "    occ = sid != 0\n    any_c = occ.any(2)",
     "    occ = (sid != 0) & (sid != 5)\n    any_c = occ.any(2)",
     STEP3, ('plate-uniform-column',)),
    ('CX-07③ 부분 원장 허용', 'step3_sigma.py',
     "    for _side in ('bot', 'top'):\n        _e = _pe.get(_side)",
     "    for _side in ():\n        _e = _pe.get(_side)",
     STEP3, ('plate-ledger-complete',)),
    ('CX-07④ signed band (top)', 'step3_sigma.py',
     "    top_m = any_c & _surf_top_cond & (np.abs(z_plate - zc[k_last]) <= band)",
     "    top_m = any_c & _surf_top_cond & (z_plate - zc[k_last] <= band)",
     STEP3, ('plate-top-above-plane',)),
    ('CX-07④ signed band (bot)', 'step3_sigma.py',
     "    bot_m = any_c & _surf_bot_cond & (np.abs(zc[k_first] - z_b) <= band_bot)",
     "    bot_m = any_c & _surf_bot_cond & (zc[k_first] - z_b <= band_bot)",
     STEP3, ('plate-bot-below-plane',)),
    ('CX-07 plate 소산에서 vox 인자 제거', 'step3_sigma.py',
     "    _use_plate = True\n    _u = float(_vox)",
     "    _use_plate = True\n    _u = 1.0",
     STEP3, ('plate-share-identity-vox',)),
    #  ── R3-CX-06: **선언을 뒤집는** mutant.  ㊷ 가 레지스트리에서 거동을 생성하므로
    #     선언을 뒤집으면 그 필드가 시험에서 빠져 조용히 초록이 되던 부류다 (Codex 실측).
    ('CX-06 physics_protocol_id.required 뒤집기', 'sdcp_gain_verdict.py',
     "'physics_protocol_id':  dict(scope='physics', across_dir=True, required=True,",
     "'physics_protocol_id':  dict(scope='physics', across_dir=True, required=False,",
     VERDICT, ('㊷g',)),
    ('CX-06 temp_c.across_dir 뒤집기', 'sdcp_gain_verdict.py',
     "    'temp_c':               dict(scope='physics', across_dir=True, generation=True),",
     "    'temp_c':               dict(scope='physics', across_dir=False, generation=True),",
     VERDICT, ('㊷e',)),
    ('CX-06 temp_c.generation 제거', 'sdcp_gain_verdict.py',
     "    'temp_c':               dict(scope='physics', across_dir=True, generation=True),",
     "    'temp_c':               dict(scope='physics', across_dir=True),",
     VERDICT, ('㊷b', '㊷c')),
    ('CX-06 vox.required 뒤집기', 'sdcp_gain_verdict.py',
     "    'vox':                  dict(scope='physics', across_dir=True, required=True,",
     "    'vox':                  dict(scope='physics', across_dir=True, required=False,",
     VERDICT, ('㉞e',)),
    ('조건5 compare_dirs 계약 제거', 'sdcp_gain_verdict.py',
     "    for _tag, _ar in (('A', arms_a), ('B', arms_b)):\n"
     "        _h, _ = validate_contract(_ar, where=f'디렉터리 {_tag}')\n"
     "        if _h:\n            return dict(out, **_h)\n", '',
     VERDICT, ('㊳a', '㊳b', '㊳c', '㊳d', '㊳f')),
    ('조건7 규칙 K 를 옛 부분문자열로', 'check_method_discipline.py',
     "            _hit = any(k_live_invocation(ln, _base, _flag) for ln in _txt.splitlines())",
     "            _hit = any(_base in ln and _flag in ln for ln in _txt.splitlines())",
     DISC, ('K-7',)),
    ('조건2 게시-전-검증 되돌림', 'mpm_webapp_payload.py',
     "    _fail_reason = _payload_reject_reason(a, step3)\n"
     "    if _fail_reason:\n        _bad = a.out + '.failed'\n"
     "        _os_w2.replace(_part, _bad)",
     "    _os_w2.replace(_part, a.out)\n"
     "    _fail_reason = _payload_reject_reason(a, step3)\n"
     "    if _fail_reason:\n        _bad = a.out + '.failed'",
     DISC, ('J-1',)),
    ('CX-02 producer stdout 봉인 해제', 'mpm_webapp_payload.py',
     "def _blind(a):\n    return not bool(getattr(a, 'show_results', False))",
     "def _blind(a):\n    return False",
     DISC, ('J-1',)),
]


def _parse(out):
    """selftest 출력 → (PASS 목록, FAIL 목록).

    ⚠⚠ 2026-08-25 — 초판은 step3 표기를 `t.endswith('FAIL')` 로 읽었는데, 그 스크립트는
      실패 시 진단을 **뒤에 붙인다** (`plate-rxn-grid: … FAIL ['이온망 위판: …']`).
      그래서 **실패를 못 읽고 "회귀가 없다" 로 보고**했다 — harness 자신의 false-negative.
      (배터리를 엄격하게 만든 첫 실행에서 바로 이것이 드러났다.)
    ⇒ `\bFAIL\b` 를 찾고, 라벨은 **첫 콜론 앞**으로 잡는다.
    """
    import re as _re
    passed, failed = [], []
    for ln in out.split('\n'):
        t = ln.strip()
        if not t or t.startswith('SELFTEST'):
            continue
        if t.startswith('FAIL  '):
            failed.append(t[6:].strip())
        elif t.startswith('PASS  '):
            passed.append(t[6:].strip())
        elif _re.search(r'\bFAIL\b', t) and ':' in t:      # step3 표기 (진단이 뒤에 붙는다)
            failed.append(t.split(':', 1)[0].strip())
        elif _re.search(r'\bOK\b', t) and ':' in t:
            passed.append(t.split(':', 1)[0].strip())
    return passed, failed


def _run(script_dir, cmd):
    r = subprocess.run([sys.executable, os.path.join(script_dir, cmd[0]), *cmd[1:]],
                       capture_output=True, text=True, timeout=2400, cwd=os.path.dirname(script_dir))
    return r.returncode, r.stdout + r.stderr


def _tree(mutate_file=None, content=None):
    """리포 사본(심볼릭) + 필요하면 파일 하나만 실체로 교체."""
    d = tempfile.mkdtemp()
    os.mkdir(os.path.join(d, 'scripts'))
    for f in os.listdir(os.path.join(REPO, 'scripts')):
        if f == mutate_file:
            continue
        os.symlink(os.path.join(REPO, 'scripts', f), os.path.join(d, 'scripts', f))
    if mutate_file:
        with open(os.path.join(d, 'scripts', mutate_file), 'w', encoding='utf-8') as fh:
            fh.write(content)
    for top in ('docs', '.github', 'wiki', 'CLAUDE.md'):
        if os.path.exists(os.path.join(REPO, top)):
            os.symlink(os.path.join(REPO, top), os.path.join(d, top))
    return d


def main():
    #  ── ⓐ baseline — 각 시험 명령이 **지금** PASS 인가 ────────────────────────────────
    print('── baseline (수정 전 상태에서 정말 통과하는가) ──')
    base = {}
    for cmd in {m[4] for m in MUTANTS}:
        d = _tree()
        try:
            rc, out = _run(os.path.join(d, 'scripts'), cmd)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        p, f = _parse(out)
        base[cmd] = (rc, set(p), set(f))
        mark = 'OK ' if rc == 0 and not f else '✗✗ '
        print(f'  {mark}{cmd[0]:<28} rc={rc} PASS {len(p)} FAIL {len(f)}')
        if rc != 0 or f:
            print(f'      HARNESS_ERROR — baseline 이 초록이 아니다.  돌연변이 결과는 뜻이 없다.')
            return 2

    rows, bad = [], []
    print('\n── 돌연변이 (하나만 되돌린다) ──')
    for label, fname, old, new, cmd, want in MUTANTS:
        src = open(os.path.join(REPO, 'scripts', fname), encoding='utf-8').read()
        if src.count(old) != 1:
            rows.append((label, 'HARNESS_ERROR', f'needle {src.count(old)}회 — 배터리가 낡았다'))
            bad.append(label)
            continue
        d = _tree(fname, src.replace(old, new))
        try:
            rc, out = _run(os.path.join(d, 'scripts'), cmd)
        except subprocess.TimeoutExpired:
            rows.append((label, 'HARNESS_ERROR', 'timeout')); bad.append(label); continue
        finally:
            shutil.rmtree(d, ignore_errors=True)
        if 'Traceback' in out and 'SystemExit' not in out.split('Traceback')[-1][:400]:
            rows.append((label, 'HARNESS_ERROR',
                         'mutant 가 예외로 죽었다 (시험이 문 것이 아니다) — '
                         + [l for l in out.split('\n') if 'Error' in l][-1:][0][:60]
                         if any('Error' in l for l in out.split('\n')) else '예외'))
            bad.append(label)
            continue
        _, f = _parse(out)
        hit = sorted({w for w in want if any(x.startswith(w) for x in f)})
        extra = sorted({x for x in f if not any(x.startswith(w) for w in want)})
        if len(hit) != len(want):
            rows.append((label, '★놓침★',
                         f'기대 {list(want)} 중 {hit} 만 물었다 (FAIL {len(f)}건)'))
            bad.append(label)
        elif extra:
            rows.append((label, '과잉',
                         f'기대 밖 실패 {len(extra)}건: {extra[0][:52]}'))
            bad.append(label)
        else:
            rows.append((label, '적발', f'{list(want)} (기대 밖 실패 0)'))

    print(f'\n{"돌연변이":<44} {"결과":<14} 근거')
    print('-' * 120)
    for a, b, c in rows:
        print(f'{a:<44} {b:<14} {c}')
    print()
    if bad:
        print(f'✗ 계약을 만족하지 않은 항목 {len(bad)}개: {bad}')
        print('  (★놓침 = 회귀가 없다 · 과잉 = 시험이 얽혔다 · HARNESS_ERROR = 배터리 결함)')
        return 1
    print(f'✓ {len(MUTANTS)} 돌연변이 전부 **기대한 시험만** 물었다 '
          f'(baseline PASS · 기대 밖 실패 0 · harness 사고 0)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
