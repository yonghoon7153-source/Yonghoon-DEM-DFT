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
     VERDICT, ('㊱h', '㊳d')),
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
     "    if isinstance(plan, dict) and plan and plan_ok(plan)[0]:",
     "    if False:",
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
     STEP3, ('plate-rxn-grid', 'plate-rxn-phase-grid')),
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
    #  ── R4-CX (Codex 4차) ────────────────────────────────────────────────────────────
    ('R4 backend requested 로 폴백', 'run_contract.py',
     "        b = b.get('used')", "        b = b.get('used') or b.get('requested')",
     RC, ('D3b', 'D3c')),
    ('R4 엄격 타입 검사 제거', 'run_contract.py',
     "        if t is bool:\n            if type(v) is not bool:      # noqa: E721",
     "        if t is bool:\n            if False:",
     VERDICT, ('㊸a',)),
    #  ⚠ **faithful** — `_miss` 만 끄면 바로 아래 타입 분기가 대신 문다 (`.get` 이 없는
    #    키에 None 을 주고 `type(None) is not bool` 이므로).  두 분기는 **중복 방어**라
    #    하나만 끄는 mutant 는 무력하다.  ⇒ 검사 자체를 무력화한다.
    ('R4 계획 스키마 검사 제거', 'run_contract.py',
     "    if not isinstance(plan, dict):",
     "    if True:\n        return True, None\n    if not isinstance(plan, dict):",
     VERDICT, ('㊸b',)),
    ('R4 PTFE 기록 계약 제거', 'run_contract.py',
     "    if sv >= EVIDENCE_SINCE_SCHEMA and v is None:",
     "    if False:",
     VERDICT, ('㊸c',)),
    ('R4-CX-07 reaction sid5 제외', 'step3_sigma.py',
     "    _occ_r = sid != 0", "    _occ_r = (sid != 0) & (sid != 5)",
     STEP3, ('plate-rxn-sdcp-face',)),
    ('R4-CX-07 reaction bot signed band', 'step3_sigma.py',
     "    bot_e = _any_o & cond_e[_iir, _jjr, _kf] & (np.abs(zc[_kf] - z_b) <= band)   # 집전체 접점",
     "    bot_e = _any_o & cond_e[_iir, _jjr, _kf] & (zc[_kf] - z_b <= band)   # 집전체 접점",
     STEP3, ('plate-rxn-outside-slab',)),
    ('R4-CX-07 reaction top signed band', 'step3_sigma.py',
     "    top_i = _any_o & cond_i[_iir, _jjr, _kl] & (np.abs(z_plate - zc[_kl]) <= band)  # 분리막 접점",
     "    top_i = _any_o & cond_i[_iir, _jjr, _kl] & (z_plate - zc[_kl] <= band)  # 분리막 접점",
     STEP3, ('plate-rxn-outside-slab',)),
    #  ── A1 (2026-08-25) — CLI 회계.  ★ 두 축을 따로 문다: **포획**(실물 파서를
    #     잡는가)과 **판정**(회계 대조를 하는가).  초판은 포획이 새서 초록이었다.
    ('A1 규칙 M 을 옛 AST 훑기로 (helper 모듈 옵션 실명)', 'check_method_discipline.py',
     "    _out = _sp.run([sys.executable, '-c', _M_PROBE % _mod],",
     "    return [o for o in __import__('re').findall(r\"add_argument\\('(--[a-z0-9-]+)\",\n"
     "                                                 open(payload, encoding='utf-8').read())], None\n"
     "    _out = _sp.run([sys.executable, '-c', _M_PROBE % _mod],",
     DISC, ('M-2', 'M-3')),
    ('A1 미등재 옵션 검사 제거', 'check_method_discipline.py',
     "    _un = sorted(o for o in _opts if o != '--help' and o not in _acct)",
     "    _un = []",
     DISC, ('M-4',)),
    ('A1 고아 규약 축 검사 제거', 'check_method_discipline.py',
     "    _orphan = sorted(f for f in _PF if f not in _covered\n"
     "                     and f not in _code_const)",
     "    _orphan = []",
     #  ⚠ M-3(리포 실물 초록)은 **안 물린다** — 리포에 고아가 없으므로 검사를 지워도
     #    실물 판정은 그대로 초록이다.  음성 대조(M-8)가 유일한 파수꾼이다.
     DISC, ('M-8',)),
    ('A1 `--dilate-z` 를 규약 축에서 빼기 (침대 z 늘림이 조용해진다)', 'run_contract.py',
     "    '--dilate-z': ('protocol', ('dilate_z',)),",
     "    '--dilate-z': ('mode', None),",
     DISC, ('M-3', 'M-11')),
    #  ── A2 (2026-08-25) — 선언 밖 매니페스트 키 훑기 ─────────────────────────────
    ('A2 매니페스트 전수 훑기 제거 (선언 밖 축이 조용해진다)', 'sdcp_gain_verdict.py',
     "            _uns = manifest_unswept_keys(_ma, _mb)",
     "            _uns = []",
     VERDICT, ('㊹b',)),
    ('A2 등록 밖 raw 차이 검사 제거', 'sdcp_gain_verdict.py',
     "            _rawd = manifest_raw_diff(_ma, _mb, expect_differ)",
     "            _rawd = []",
     #  ⚠ `㊹c`(periodic_xy) 는 **안 물린다** — 그 축은 레지스트리에 있어 앞 루프가 먼저 잡는다.
     #    전수 훑기의 **고유** 사정권은 레지스트리 밖 그림자 필드다 (㊹e).  손으로 확인함.
     VERDICT, ('㊹e',)),
    ('A2 σ_VGCF 를 "런 결과" 로 면제 (전수 훑기를 우회하는 길)', 'sdcp_gain_verdict.py',
     "    'mesh_unavailable': '런 결과',",
     "    'mesh_unavailable': '런 결과', 'sigma_vgcf_S_cm': '(잘못된 면제)',",
     #  ⚠ `㉗b` 는 **안 물린다** — 레지스트리 루프가 먼저 잡기 때문이다.  면제의 유일한
     #    사정권은 **분류 안 된 키**이므로, 위험은 "계약된 축을 면제로 옮기는 것" 이고
     #    그것을 구조 불변식 ㊹f 가 막는다 (배터리가 이 사실을 알려 줬다).
     VERDICT, ('㊹f',)),
    #  ★ A3 부류 — **선언 뒤집기**.  `across_dir=False` 면 레지스트리 루프가 이 축을 건너뛴다.
    #    그때 잡는 것은 A2 의 매니페스트 전수 훑기뿐이다 (= `_rawd` 가 하는 일).
    ('A3 `periodic_xy.across_dir` 뒤집기 (선언만 바꾼다)', 'sdcp_gain_verdict.py',
     "    'periodic_xy':          dict(scope='physics', across_dir=True, required=True,",
     "    'periodic_xy':          dict(scope='physics', across_dir=False, required=True,",
     #  ⚠ 실제로 무는 것은 **구조 불변식** ㊷e ("규약 축은 전부 across_dir") 다.  거동
     #    시험 ㊹c 는 전수 훑기가 대신 잡아 여전히 통과한다 = 두 겹이 겹쳐 있다.  손으로 확인함.
     VERDICT, ('㊷e',)),
    ('A2 리더의 레지스트리 자동 채움 제거 (H5 부류 복원)', 'sdcp_gain_verdict.py',
     "    for _f in FIELD_CONTRACT:\n        if row.get(_f) is None:\n            row[_f] = man.get(_f)",
     "    for _f in ():\n        if row.get(_f) is None:\n            row[_f] = man.get(_f)",
     #  ★ `broad` — 자동 채움은 **기전**이라 14개 시험이 그것에 기댄다 (그 수 자체가 증거다).
     VERDICT, ('*broad*20', '㊹d')),
    ('A1 합성 SE 구름 게이트 제거 (proxy 침대로 σ 주장)', 'sdcp_gain_verdict.py',
     "    if _px:\n        return dict(decision='HOLD', hold_code='SE_PROXY',",
     "    if False:\n        return dict(decision='HOLD', hold_code='SE_PROXY',",
     VERDICT, ('㊹g',)),
    #  ── R5 (2026-08-25, Codex 5차) ───────────────────────────────────────────────
    ('R5-CX-01 P2_EXTRA 문자 allowlist 제거 (2단계 확장 우회 복원)', 'sdcp_gain_vox015_8arm.sh',
     "  if printf '%s' \"$P2_EXTRA\" | LC_ALL=C grep -q '[^A-Za-z0-9._=/ -]'; then",
     "  if false; then",
     DISC, ('L-13',)),
    ('R5-CX-02 세대를 자기신고로 되돌리기 (schema downgrade 우회 복원)', 'run_contract.py',
     "    _obs = observed_generation(man)\n    if _obs is not None and v < _obs:",
     "    _obs = observed_generation(man)\n    if False:",
     RC, ('F4',)),
    ('R5-CX-02 관찰 세대 판정 무력화', 'run_contract.py',
     "    if isinstance(pid, str) and pid.startswith(PROTOCOL_SCHEMA + '-') and 'unknown' not in pid:",
     "    if False:",
     RC, ('F2', 'F4')),
    ('R5-CX-04 origin 을 개수만 보기 (임의 8점 허용 복원)', 'sdcp_gain_verdict.py',
     "    _alien = sorted(_got_o - _expset)",
     "    _alien = []",
     VERDICT, ('㊺c',)),
    ('R5-CX-04 전량 런 factorial 완비 검사 제거', 'sdcp_gain_verdict.py',
     "    if require_arms is not None and int(require_arms) == len(_exp_o) and _got_o != _expset:",
     "    if False:",
     VERDICT, ('㊺e',)),
    ('R5-CX-05 PNM·collector 결과 계약 제거 (status-only 복원)', 'run_contract.py',
     "        _rspec = COMPONENT_RESULT.get(comp)",
     "        _rspec = None",
     RC, ('G3', 'G4', 'G5', 'G6')),
    ('R5-CX-05 미등록 component 조용한 통과 복원', 'run_contract.py',
     "            return False, (f'EVID|{comp}|unregistered| 이 component 의 증거 계약이 ",
     "            continue\n        if False:\n            return False, (f'EVID|{comp}|unregistered| 이 component 의 증거 계약이 ",
     RC, ('G7',)),
    #  ★ Codex R5 가 "146 PASS / FAIL 0" 으로 통과시킨 그 선언 뒤집기
    ('R5-CX-07 `backend.across_dir` 뒤집기 (선언만 바꾼다)', 'sdcp_gain_verdict.py',
     "    'backend':              dict(scope='numeric', across_dir=True, required=True,",
     "    'backend':              dict(scope='numeric', across_dir=False, required=True,",
     VERDICT, ('㊷e',)),
    ('R5-CX-07 선언↔거동 일치 검사(M_UNWRITTEN) 제거', 'check_method_discipline.py',
     "        _unwritten = sorted({f for c, flds in _acct.values()",
     "        _unwritten = [] or sorted({f for c, flds in _acct.values()",
     DISC, ('M-13',)),
    ('R5-CX-03 영수증 대조 제거 (러너 의도 미봉인 복원)', 'sr01_stamp_compare.py',
     "    if receipt:\n        _rok, _rwhy = _RC.receipt_match(receipt, (s.get('manifest') or {}),",
     "    if False:\n        _rok, _rwhy = _RC.receipt_match(receipt, (s.get('manifest') or {}),",
     RC, ('H2',)),
    ('R5-CX-03 영수증 digest 를 OUTDIR 에서 빼기 (캐시 충돌 복원)', 'sdcp_gain_vox015_8arm.sh',
     "${LEAN_TAG}${_RCPT_TAG}}"",
     "${LEAN_TAG}}"",
     DISC, ('L-14a', 'L-14b')),
    ('R4-CX-06 규칙 K 제어흐름 무시', 'check_method_discipline.py',
     "    if not _live_after(toks):\n        return False", "    if False:\n        return False",
     DISC, ('K-5',)),
    ('R4-CX-01 producer 봉인 해제', 'mpm_webapp_payload.py',
     "def _blind(a):\n    return not bool(getattr(a, 'show_results', False))",
     "def _blind(a):\n    return False",
     DISC, ('J-1',)),
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
     #  ⚠ 2026-08-25 정정: A2 의 리더 자동 채움 이후 `㊷b`(across_dir 거동)는 **안 물린다**
     #    — `across_dir` 선언은 그대로이기 때문이다.  세대 축 시험 `㊷c` 만 문다.
     VERDICT, ('㊷c',)),
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
     #  ⚠ 2026-08-25 정정: 옛 기대는 `L-11` 도 물릴 것으로 적었는데 **틀렸다** — L-11 은
     #    `P2_EXTRA` 금지 검사이고 `k_live_invocation` 과 무관하다 (배터리가 잡았다).
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
        _mut_txt = src.replace(old, new)
        #  ★ R4-CX-06 — **실행 전에** 컴파일해 본다.  문법 오류는 시험 결과가 아니라
        #    harness 사고다 (Traceback 없는 SyntaxError 의 소스 줄이 `FAIL` 처럼 보였다).
        try:
            compile(_mut_txt, fname, 'exec')
        except SyntaxError as _se:
            rows.append((label, 'HARNESS_ERROR',
                         f'mutant 가 문법 오류다 ({_se.lineno}행) — 시험이 문 것이 아니다'))
            bad.append(label)
            continue
        d = _tree(fname, _mut_txt)
        try:
            rc, out = _run(os.path.join(d, 'scripts'), cmd)
        except subprocess.TimeoutExpired:
            rows.append((label, 'HARNESS_ERROR', 'timeout')); bad.append(label); continue
        finally:
            shutil.rmtree(d, ignore_errors=True)
        #  ★★★ 2026-08-25 (R4-CX-06, Codex 4차) — **compile/import 를 먼저 본다.**
        #    옛 판은 출력 문자열만 읽어, Traceback 없는 SyntaxError 의 **소스 줄**이
        #    `㊷g: FAIL` 처럼 보이면 그것을 정상 적발로 분류했다.  ⇒ mutant 파일을
        #    실행 전에 컴파일해 보고, 실패면 harness 사고로 뺀다 (시험 결과가 아니다).
        #  ★★★ 2026-08-25 (A0) — **크래시 판별을 마지막 줄로 한다.**  옛 조건은
        #    "traceback 안에 `SystemExit` 이 없으면 크래시" 였는데, selftest 는
        #    `raise SystemExit(_selftest())` 로 끝나므로 **어떤 크래시든** traceback 에
        #    `SystemExit` 이 섞인다 ⇒ 크래시가 **한 번도** harness 사고로 분류되지 않았다.
        #    (실측: `KeyError: 'ionic'` 로 죽은 mutant 가 `★놓침★` 으로 보고됐다 —
        #     "회귀가 없다" 와 "코드가 터졌다" 는 완전히 다른 결론이다.)
        #  ⇒ traceback 의 **마지막 예외 줄**을 본다.  `SystemExit: <int>` 는 정상 종료다.
        _last = [l for l in out.strip().split('\n') if l and not l.startswith(' ')]
        _crash = ('Traceback' in out and _last
                  and not _last[-1].startswith('SystemExit')
                  and ':' in _last[-1] and 'Error' in _last[-1].split(':')[0])
        if _crash:
            _elines = [l for l in out.split('\n') if 'Error' in l]
            rows.append((label, 'HARNESS_ERROR',
                         'mutant 가 예외로 죽었다 (시험이 문 것이 아니다) — '
                         + (_elines[-1][:60] if _elines else '예외')))
            bad.append(label)
            continue
        _p, f = _parse(out)
        #  ★ R4-CX-06 — baseline 과 **집합으로** 대조한다.  같은 접두사의 여러 FAIL 이
        #    한 기대 id 로 접히던 것도, baseline 에 없던 PASS 가 사라진 것도 여기서 보인다.
        _b_rc, _b_pass, _b_fail = base[cmd]
        if rc == 0:
            rows.append((label, '★놓침★', 'mutant 인데 rc=0 (아무 시험도 안 물었다)'))
            bad.append(label)
            continue
        #  ★★★ 2026-08-25 (R5-CX-07, Codex 5차) — **baseline PASS 목록을 읽고도 비교하지
        #    않았다.**  그래서 돌연변이가 시험을 *사라지게* 만들어도(수집 실패·조기 종료)
        #    "FAIL 이 났으니 적발" 로 셌다.  ⇒ baseline 에 있던 시험이 **없어졌으면** 그것은
        #    적발이 아니라 harness 사고다 (그 시험은 물린 것이 아니라 안 돈 것이다).
        _p_now, _ = _parse(out)
        _vanished = sorted(set(_b_pass) - set(_p_now) - set(f))
        if _vanished:
            rows.append((label, 'HARNESS_ERROR',
                         f'baseline 시험 {len(_vanished)}개가 **사라졌다** '
                         f'(예: {_vanished[0][:40]}) — 물린 것이 아니라 안 돈 것이다'))
            bad.append(label)
            continue
        #  ★★ 2026-08-25 (A2 배터리) — **`broad`** 표식.  기전 자체를 들어내는 돌연변이
        #    (리더의 레지스트리 자동 채움 제거 같은 것)는 수십 개 시험이 그 기전에 기대므로
        #    "기대 밖 실패 0" 이 원리적으로 성립하지 않는다.  그것은 얽힘이 아니라
        #    **그 기전이 얼마나 많이 쓰이는가**의 측정이다.  ⇒ `broad` 는 부분집합만 본다.
        #    ⚠ 게이트 하나를 끄는 돌연변이에는 **절대 쓰지 않는다** — 거기서 기대 밖 실패는
        #      진짜 얽힘 신호다 (그것을 보려고 이 배터리를 만들었다).
        #  ★★ 2026-08-25 (R5-CX-07) — `broad` 가 **무제한 wildcard** 였다.  실제 broad row 에
        #    기대 밖 실패가 15건 있었는데 최종 문구는 여전히 `기대 밖 실패 0` 이었다
        #    (Codex 실측).  ⇒ **한도**를 요구한다: `*broad*<N>` 으로 최대 개수를 적는다.
        #    한도를 안 적으면 배터리가 거부한다 — 면죄부를 무제한으로 두지 않는다.
        _broad_cap = None
        if want and str(want[0]).startswith('*broad*'):
            _tail = str(want[0])[len('*broad*'):]
            if not _tail.isdigit():
                rows.append((label, 'HARNESS_ERROR',
                             "`*broad*` 에 한도가 없다 — `*broad*<N>` 으로 최대 기대-밖 "
                             "실패 수를 적을 것 (무제한 면제 금지, R5-CX-07)"))
                bad.append(label)
                continue
            _broad_cap = int(_tail)
            want = tuple(want[1:])
        #  ★★ `startswith` → **정확 일치**.  접두사 매칭은 `L-12` 가 `L-12(변수 참조)` 와
        #    `L-12: 봉인 실패…` 를 **같은 것으로** 세게 만든다 (이 세션에서 실제로 겪었다).
        #    시험 이름은 `id: 설명` 또는 `id(변형): 설명` 이므로 그 id 만 떼어 비교한다.
        def _tid(name):
            _h = name.split(':', 1)[0].strip()
            return _h.split('(', 1)[0].strip() if '(' in _h else _h
        _fail_ids = {_tid(x) for x in f}
        hit = sorted({w for w in want if w in _fail_ids})
        extra = sorted({x for x in f if _tid(x) not in set(want)})
        if _broad_cap is not None and len(hit) == len(want):
            if len(extra) > _broad_cap:
                rows.append((label, '과잉',
                             f'broad 한도 {_broad_cap} 를 넘었다 — 기대 밖 실패 {len(extra)}건 '
                             f'(예: {extra[0][:44]})'))
                bad.append(label)
                continue
            rows.append((label, f'적발(broad≤{_broad_cap})',
                         f'{list(want)} + 기전 의존 {len(extra)}건'))
            continue
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
