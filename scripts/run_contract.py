"""**실행 계약의 단일 출처** — producer · `check_arm` · 판정기가 **같은 함수**를 쓴다.

★★★ 왜 (2026-08-25, Codex 3차 R3-CX-01/05/06): 같은 계약이 세 곳에 따로 적혀 있었고
  세 곳 다 조금씩 달랐다.  실제로 난 사고:

  · **payload 자리**가 두 목록에 따로 있었고 한쪽이 `metrics` **오타**였다 →
    `check_arm` 이 **모든 실제 팔을 거부**했다 (생산 전면 차단).  selftest 75/75 는
    초록이었다 — 픽스처가 같은 오타를 쓰고 있었기 때문이다.
  · **수렴 계약**이 `cg_info == 0` 만 봐서 `cg_info = 0.5` 가 통과했다 (`int(ci)` 절삭).
  · **backend** 가 component 를 못 찾으면 다른 component → last-solve 로 내려앉아,
    전자 backend 가 **없는데** ionic 의 gpu 도장으로 통과했다.
  · **수치 증거**를 producer validator 가 안 봐서 `sigma_e=None` · `cg_resid=NaN` ·
    `cg_info=99` 인 payload 가 전부 게시됐다.

⚠ 규칙: 이 파일 밖에서 이 계약을 **다시 적지 않는다**.  새 소비자가 생기면 여기서 import 한다.
  (그 중복이 위 네 사고의 공통 뿌리다.)
"""
from __future__ import annotations

import math

#: payload 안에서 STEP3 결과가 사는 자리.  producer 는 `mpm_metrics['step3']` 에 쓴다
#  (`mpm_webapp_payload.py`, `mpm_metrics['step3'] = step3`).
#  ⚠ `metrics` 는 **의도적으로 없다** — 그 자리에 쓰는 producer 가 없고, 관대하게 받아
#    주면 "자리를 못 찾아 조용히 통과" 와 구분되지 않는다 (R3-CX-01 이 그 상태였다).
STEP3_PATHS = (('mpm_metrics', 'step3'), ('step3',))

#: CG 수렴 문턱.  `step3_sigma.py` 의 `unconv = bool(info) or resid > 1e-6` 과 **같은 값**.
CG_RESID_MAX = 1e-6

#: 항상 필요한 component.  나머지는 run mode 가 정한다 (`required_components`).
ALWAYS_REQUIRED = ('electronic',)


def dig(obj, path):
    for k in path:
        if not isinstance(obj, dict) or k not in obj:
            return None
        obj = obj[k]
    return obj


def step3_of(payload):
    """payload dict → step3 dict.  자리를 못 찾으면 None (조용히 0 을 만들지 않는다)."""
    for p in STEP3_PATHS:
        got = dig(payload, p)
        if isinstance(got, dict):
            return got
    return None


#: 물리 규약 스키마 판.  ★ 축 집합이 바뀌면 **이 접두사도 올린다** — 안 올리면 옛 팔과
#  새 팔의 id 가 같은 이름공간에 살아 "다른 축 집합인데 문자열만 같다" 를 구분할 수 없다
#  (R3-CX-03: 축을 17 → 19 로 늘렸는데 접두사는 `p1-` 그대로였다).
PROTOCOL_SCHEMA = 'p2'

#: 규약을 정하는 축.  ⚠ **producer 도 소비자도 이 목록 하나만 쓴다** (사본 금지).
PROTOCOL_FIELDS = ('vox_um', 'bridge_um', 'fibre_stamp', 'sdcp_stamp', 'sdcp_sphere_d_um',
                   'sdcp_yield_to_vgcf', 'ptfe_stamp', 'ptfe_zero_dof',
                   'sigma_vgcf_S_cm', 'sigma_sdcp_S_cm', 'sigma_ptfe_S_cm',
                   'sigma_ion_se_S_cm', 'sigma_ion_sdcp_S_cm',
                   'sigma_am_s_S_cm', 'sigma_am_p_S_cm', 'cam', 'temp_c',
                   'periodic_xy', 'plate_rule')

#: `None` 이 **명시적 OFF** 인 축 (값 부재가 아니다).
PROTOCOL_OFF_OK = ('temp_c',)


def physics_protocol_id(man):
    """적용된 규약 dict → 안정 해시.  **선언이 아니라 결과**다.

    ★★★ 2026-08-25 (R3-CX-03, Codex 3차) — 두 가지를 고쳤다.

    ⓐ **키 부재와 명시적 OFF 를 구분한다.**  옛 판은 `man.get(k)` 라 둘 다 `None` 이었고,
       `temp_c=None (키 있음)` 과 `temp_c 키 없음` 이 **같은 해시**를 냈다 (Codex 실측).
       키가 아예 없으면 그 팔은 그 축을 기록하지 않은 옛 세대이고, 그것은 OFF 가 아니라
       **모름**이다.  ⇒ `in` 으로 존재를 먼저 본다.
    ⓑ **스키마 접두사를 올린다** (`p1-` → `p2-`).  축을 17 → 19 로 늘렸는데 접두사가
       그대로면 옛 id 와 새 id 가 같은 이름공간에 산다.

    ⚠ 값이 하나라도 없으면 `unknown:<빠진 필드>` 를 낸다 (임의 기본값으로 채우지 않는다).
    """
    import hashlib as _hl
    import json as _json
    _v, _miss = {}, []
    for k in PROTOCOL_FIELDS:
        if k not in man:
            _miss.append(k)                       # ★ 키 부재 = 모름 (OFF 가 아니다)
            continue
        val = man[k]
        if val is None:
            if k in PROTOCOL_OFF_OK:
                _v[k] = '__OFF__'                 # 명시적 OFF 는 유효값
            else:
                _miss.append(k)
        else:
            _v[k] = val
    if _miss:
        return 'unknown:' + ','.join(sorted(set(_miss)))
    _canon = _json.dumps(_v, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    return f'{PROTOCOL_SCHEMA}-' + _hl.sha256(_canon.encode('utf-8')).hexdigest()[:16]


def protocol_ok(man):
    """매니페스트 → `(ok, reason|None)`.  **저장된 id 를 믿지 않고 다시 계산한다.**

    ★★★ R3-CX-03: 소비자가 `manifest['physics_protocol_id']` 를 **읽기만** 했다.
      그래서 Codex 가 통과시켰다 —
        · 16 팔 전부 `periodic_xy`/`plate_rule` 키가 **없는데** stored id 는 `p1-…`
        · 팔마다 `periodic_xy` 를 True/False 로 바꿔 놓고 stored id 만 같게
        · 모든 팔에 `physics_protocol_id = "garbage"`
      셋 다 "서로 같으니 통과" 였다.  **문자열 일치는 규약 일치가 아니다.**
    ⇒ raw manifest 로 재계산해 저장값과 대조한다.  다르면 그 기록은 신뢰할 수 없다.
    """
    stored = (man or {}).get('physics_protocol_id')
    recomputed = physics_protocol_id(man or {})
    if not isinstance(stored, str) or not stored:
        return False, f'PROTOCOL_ID_MISSING| 저장된 id 가 없다 (재계산 = {recomputed})'
    if recomputed.startswith('unknown:'):
        return False, (f'PROTOCOL_UNKNOWN| 규약을 확정할 수 없다 — {recomputed} '
                       f'(저장값 {stored!r} 은 그 사실을 숨긴다)')
    if stored != recomputed:
        return False, (f'PROTOCOL_ID_STALE| 저장된 id {stored!r} 가 raw manifest 재계산 '
                       f'{recomputed!r} 와 다르다 — 옛 세대이거나 손으로 쓴 값이다.  '
                       f'문자열 일치는 규약 일치가 아니다 (R3-CX-03)')
    return True, None


def conv_ok(cg_info, unconverged, resid):
    """수렴 계약 → `(ok, why)`.  모르는 것·모순·타입 오류는 전부 실패다 (fail-closed).

    ⚠ `type(cg_info) is int` 를 요구한다 — `bool` 은 `int` 의 하위형이라 `isinstance` 로는
      `True` 가 통과하고, `float` 는 `int(0.5) == 0` 으로 **절삭**돼 통과한다.
      Codex 실측: `conv_ok(0.5, False, 1e-9)` 이 옛 판에서 `(True, '')` 였다.
    ⚠ residual 은 **필수**다.  없으면 수렴했는지 모르는 것이고, 모르는 것은 통과가 아니다.
    """
    if cg_info is None or unconverged is None or resid is None:
        return False, 'blind'
    if type(cg_info) is not int:                       # noqa: E721 — bool/float 를 막는 것이 목적
        return False, 'type'
    if type(unconverged) is not bool:                  # noqa: E721
        return False, 'type'
    if isinstance(resid, bool) or not isinstance(resid, (int, float)):
        return False, 'type'
    if unconverged or cg_info != 0:
        return False, 'unconv'
    if not math.isfinite(resid) or resid < 0 or resid > CG_RESID_MAX:
        return False, 'resid'
    return True, ''


def required_components(no_ion=False, no_thermal=False, no_pore=False,
                        no_collector=False, plan=None):
    """run mode → **완료돼야 하는** component 이름들.

    ★ `plan` (매니페스트의 `component_plan`) 이 있으면 **그것이 정본**이다 —
      소비자는 실행 인자를 모르고 매니페스트만 보기 때문이다 (R3-CX-04).
    ⚠ 계획 키 `collector` ↔ component 이름 `collector_geom` 의 불일치를 여기서 흡수한다.
    """
    _MAP = {'electronic': 'electronic', 'ionic': 'ionic', 'thermal': 'thermal',
            'pore': 'pore', 'collector': 'collector_geom'}
    if isinstance(plan, dict) and plan:
        return tuple(_MAP[k] for k in _MAP if plan.get(k))
    req = list(ALWAYS_REQUIRED)
    if not no_ion:
        req.append('ionic')
    if not no_thermal:
        req.append('thermal')
    if not no_pore:
        req.append('pore')
    if not no_collector:
        req.append('collector_geom')
    return tuple(req)


def component_backend(step3, comp):
    """`comp` 자신의 backend.  **폴백하지 않는다** — 없으면 None.

    ⚠ 옛 판은 component 를 못 찾으면 다른 component → last-solve 로 내려갔다.  그래서
      전자 backend 가 **없는데** ionic 의 `gpu` 도장으로 `expect_backend='gpu'` 를
      통과했고, 전자 cpu + ionic gpu 도 통과했다 (Codex 실측 3건).
      다른 component 의 backend 는 이 component 에 대한 증거가 아니다.
    """
    c = ((step3 or {}).get('manifest') or {}).get('components') or {}
    v = c.get(comp)
    if not isinstance(v, dict):
        return None
    b = v.get('backend')
    if isinstance(b, dict):
        b = b.get('used') or b.get('requested')
    return b if isinstance(b, str) and b else None


def numeric_ok(step3):
    """**계산이 실제로 일어났다는 수치 증거** → `(ok, reason|None)`.

    status 문자열만 보면 계산 없는 자가보고가 통과한다.  Codex 실측: `sigma_e=None` ·
    `cg_resid=NaN` · `cg_info=99` 인 payload 가 전부 `reject_reason = None` 이었다.

    ⚠ 사유는 **안정된 진단 코드**로 시작한다 (`SIGMA_E|` `N_DOF|` `CONV|`).  회귀가
      느슨한 부분문자열이 아니라 코드로 짝지어야 "정확히 그 검사가 물었다" 를 말할 수
      있다 (Codex R3-CX-08).
    """
    s = step3 or {}
    sig, dof = s.get('sigma_e_eff_S_cm'), s.get('n_dof')
    if isinstance(sig, bool) or not isinstance(sig, (int, float)) \
            or not math.isfinite(sig) or sig <= 0:
        return False, f'SIGMA_E| sigma_e_eff_S_cm={sig!r} (유한한 양수여야 한다)'
    if type(dof) is not int or dof <= 0:               # noqa: E721
        return False, f'N_DOF| n_dof={dof!r} (양의 정수여야 한다)'
    ok, why = conv_ok(s.get('cg_info'), s.get('unconverged'), s.get('cg_resid'))
    if not ok:
        return False, (f'CONV|{why}| 전자 수렴 미확인 cg_info={s.get("cg_info")!r} '
                       f'unconverged={s.get("unconverged")!r} cg_resid={s.get("cg_resid")!r}')
    return True, None


def _selftest():
    ok = fail = 0

    def chk(c, m):
        nonlocal ok, fail
        ok, fail = (ok + 1, fail) if c else (ok, fail + 1)
        print(('  PASS  ' if c else '  FAIL  ') + m)

    #  ── 자리 ────────────────────────────────────────────────────────────────────
    chk(step3_of({'mpm_metrics': {'step3': {'a': 1}}}) == {'a': 1},
        'A1 producer 자리(`mpm_metrics.step3`)를 읽는다')
    chk(step3_of({'step3': {'a': 1}}) == {'a': 1}, 'A2 평평한 자리도 읽는다')
    chk(step3_of({'metrics': {'step3': {'a': 1}}}) is None,
        'A3 ★★ 옛 오타 자리(`metrics.step3`)는 **읽지 않는다** — 관대하면 R3-CX-01 이 '
        '숨는다')
    chk(step3_of({'mpm_metrics': {}}) is None, 'A4 없으면 None (0 을 만들지 않는다)')

    #  ── 수렴 ────────────────────────────────────────────────────────────────────
    chk(conv_ok(0, False, 1e-9) == (True, ''), 'B1 정상 증인')
    #  ⚠ **코드까지** 본다 (Codex R3-CX-08).  `[0] is False` 만 보면, 타입 검사를 옛
    #    `isinstance` 로 되돌려도 `0.5 != 0` 이 `unconv` 로 대신 물어 **초록**이다 —
    #    그러면 이 시험은 타입 검사를 인증하지 못한다 (실측으로 그랬다).
    for _v, _code, _lbl in ((0.5, 'type', 'float 0.5 (옛 판은 int() 절삭으로 통과시켰다)'),
                            (True, 'type', 'bool True (bool 은 int 의 하위형)'),
                            (None, 'blind', 'None')):
        _o, _w = conv_ok(_v, False, 1e-9)
        chk(_o is False and _w == _code,
            f'B2 cg_info={_lbl} → `{_code}` 로 거부 (받은 것: {_w!r})')
    chk(conv_ok(0, 0, 1e-9)[0] is False, 'B3 unconverged 가 bool 이 아니면 거부')
    for _r, _lbl in ((None, 'None'), (float('nan'), 'NaN'), (float('inf'), 'inf'),
                     (-1e-9, '음수'), (2e-6, '문턱 초과')):
        chk(conv_ok(0, False, _r)[0] is False, f'B4 resid={_lbl} → 거부')
    chk(conv_ok(0, False, CG_RESID_MAX) == (True, ''), 'B5 문턱 **경계값**은 통과')
    chk(conv_ok(30000, False, 1e-9)[1] == 'unconv',
        'B6 ★ cg_info≠0 인데 unconverged=False (모순) → unconv')

    #  ── 수치 증거 ────────────────────────────────────────────────────────────────
    _good = {'sigma_e_eff_S_cm': 0.01, 'n_dof': 5000, 'cg_info': 0,
             'cg_resid': 1e-9, 'unconverged': False}
    chk(numeric_ok(_good) == (True, None), 'C1 정상 증인')
    #  ⚠ **정확한 진단 코드**로 짝짓는다 (Codex R3-CX-08) — 느슨한 부분문자열이면
    #    "다른 검사가 대신 물어서" 통과해도 초록이라 그 검사가 인증되지 않는다.
    for _k, _v, _code, _lbl in (
            ('sigma_e_eff_S_cm', None, 'SIGMA_E|', 'σ_e=None'),
            ('sigma_e_eff_S_cm', float('nan'), 'SIGMA_E|', 'σ_e=NaN'),
            ('sigma_e_eff_S_cm', float('inf'), 'SIGMA_E|', 'σ_e=inf'),
            ('sigma_e_eff_S_cm', 0.0, 'SIGMA_E|', 'σ_e=0'),
            ('sigma_e_eff_S_cm', -1.0, 'SIGMA_E|', 'σ_e<0'),
            ('n_dof', 0, 'N_DOF|', 'dof=0'), ('n_dof', None, 'N_DOF|', 'dof=None'),
            ('n_dof', 5000.0, 'N_DOF|', 'dof 가 float'),
            ('cg_resid', None, 'CONV|blind|', 'resid=None'),
            ('cg_resid', float('nan'), 'CONV|resid|', 'resid=NaN (비유한)'),
            ('cg_resid', 2e-6, 'CONV|resid|', 'resid 문턱 초과'),
            ('cg_info', 99, 'CONV|unconv|', 'cg_info=99'),
            ('cg_info', 0.5, 'CONV|type|', 'cg_info=0.5 (float 절삭)'),
            ('unconverged', True, 'CONV|unconv|', 'unconverged=True')):
        _o, _w = numeric_ok(dict(_good, **{_k: _v}))
        chk(_o is False and str(_w).startswith(_code),
            f'C2 {_lbl} → `{_code}` 로 거부 (옛 producer validator 는 전부 통과시켰다)')

    #  ── backend (폴백 금지) ───────────────────────────────────────────────────────
    def _p(**comps):
        return {'manifest': {'components': comps}}
    chk(component_backend(_p(electronic={'status': 'complete', 'backend': 'gpu'}),
                          'electronic') == 'gpu', 'D1 자기 backend 를 읽는다')
    chk(component_backend(_p(electronic={'status': 'complete'},
                             ionic={'status': 'complete', 'backend': 'gpu'}),
                          'electronic') is None,
        'D2 ★★ 전자 backend 가 없으면 **ionic 의 gpu 를 빌려오지 않는다**')
    chk(component_backend(_p(electronic={'status': 'complete',
                                         'backend': {'used': 'cpu', 'requested': 'gpu'}}),
                          'electronic') == 'cpu',
        'D3 dict backend 는 **실제로 쓴 것**(used)을 읽는다')
    chk(component_backend({}, 'electronic') is None, 'D4 매니페스트가 없으면 None')

    #  ── required (계획이 정본) ────────────────────────────────────────────────────
    chk(required_components(no_ion=True, no_thermal=True, no_pore=True,
                            no_collector=True) == ('electronic',),
        'E1 LEAN=2 는 전자만 필수')
    chk(set(required_components()) == {'electronic', 'ionic', 'thermal', 'pore',
                                       'collector_geom'}, 'E2 기본은 다섯 전부')
    chk(set(required_components(plan={'electronic': True, 'ionic': False, 'thermal': True,
                                      'pore': False, 'collector': True}))
        == {'electronic', 'thermal', 'collector_geom'},
        'E3 ★ `component_plan` 이 있으면 그것이 정본 (소비자는 실행 인자를 모른다)')
    chk('collector_geom' in required_components(plan={'collector': True}),
        'E4 ★ 계획 키 `collector` ↔ component 이름 `collector_geom` 불일치를 흡수한다')

    print(f'\nrun_contract selftest: {ok}/{ok + fail} PASS'
          + ('' if not fail else '   ✗ 실패 있음'))
    return 0 if not fail else 1


if __name__ == '__main__':
    import sys
    sys.exit(_selftest() if '--selftest' in sys.argv else
             print('사용: python3 scripts/run_contract.py --selftest') or 0)
