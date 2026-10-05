#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MPM payload → mpm_lab 등록 훅  (결과회수 자동화 = 파이프라인 ③).

원격(V100 등) 계산 완료 → 이 모듈이 ``mpm_payload.json`` 을 webapp 의 mpm_lab
데이터 폴더에 **등록** → Flask 동적 로딩(`_mpm_lab_list`)이 다음 새로고침에 자동
반영(재시작 불필요).  즉 "db 등록 = 사이트 반영" 자동 동기화의 서버-측 조각.

핵심: meta.json 을 만드는 로직(`build_meta`)을 **여기 한 곳**에 두고 webapp
`/mpm-lab/upload` 라우트와 CLI 훅이 **같이 import** → 두 경로의 meta 가 절대
어긋나지 않음(single source of truth).  등록 시 `trust`(수렴/미수렴 배지)도
payload 가 이미 기록한 실제 잔차/UNCONVERGED 마커에서 계산해 임베드 → "각 값의
수렴을 db 에서 읽어 자동 배지"(파이프라인 ④)의 데이터-측을 등록 훅이 함께 채움.

등록 경로 3종 (토폴로지에 맞게 택1):
  --dest DIR          로컬/공유 파일시스템에 폴더 기록 (WSL·공유디스크·NFS 마운트)
  --url  URL          실행중 webapp 의 /mpm-lab/upload 로 HTTP push (Render 등 원격 호스트)
  --rsync HOST:DIR    폴더를 로컬 생성 후 rsync(ssh) — V100 → webapp 호스트

Flask 의존성 없음(순수 stdlib + 선택적 requests).  webapp/app.py 와 같은 폴더에
두어 `import mpm_lab_register` 가 경로설정 없이 되도록 함.

    # V100 계산 스크립트 끝에 붙이는 훅 예시
    python webapp/mpm_lab_register.py --payload out/mpm_payload.json \
        --name "DBE_2C_N10"  --dest /shared/dem/webapp/mpm_lab
    # 또는 실행중인 webapp 으로 HTTP push (파일시스템 접근이 없을 때)
    python webapp/mpm_lab_register.py --payload out/mpm_payload.json \
        --name "DBE_2C_N10"  --url http://localhost:5002/mpm-lab/upload
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import time
import uuid
from datetime import datetime


# ── slug: webapp/app.py `_mpm_lab_slug` 과 동일 규칙(연속점 붕괴 = path traversal 차단) ──
def slugify(s) -> str:
    return (re.sub(r'\.{2,}', '_', re.sub(r'[^A-Za-z0-9_.-]+', '_', str(s or '')))
            .strip('_') or 'payload')


def _has_unconverged(*vals) -> bool:
    """payload 가 trust/note 문자열에 심어둔 '⚠UNCONVERGED' 마커 감지."""
    for v in vals:
        if isinstance(v, str) and 'UNCONVERGED' in v:
            return True
    return False


def compute_trust(mm: dict) -> dict:
    """payload 의 mpm_metrics 에서 STEP3/4 수렴 배지를 계산.

    fabricate 하지 않음 — payload 가 실제로 기록한 잔차(cg_resid/ion_resid/resid/
    kcl_err)와 UNCONVERGED 마커만 읽는다.  step3 가 없으면(--no-step3) overall='na'.
    반환: {overall: 'ok'|'warn'|'na', converged: bool, n_warn, badges:[{key,label,status,resid,detail}]}
    """
    mm = mm or {}
    s3 = mm.get('step3') or {}
    badges: list[dict] = []

    #  ★★ 2026-09-07 — `component_plan` 을 읽는다.  payload 는 *"무엇을 돌리기로 했는가"* 를
    #    적고 있는데(매니페스트 주석: "이것이 없으면 `disabled` 가 의도적으로 껐다인지 조용히
    #    죽었다인지 구분할 근거가 없다", M-R3-03) 이 함수는 **`present` 만 봤다** — 그래서
    #    계획해 놓고 결과가 없는 채널이 **침묵으로 통과**했다.  present-only 는 false-green 이다.
    #  ⚠ 옛 payload 에는 `component_plan` 이 없다 → 그때는 **기존 동작 그대로** (매니페스트가
    #    "옛 payload 에 새 필드를 소급 요구하면 과잉차단" 이라고 세대별 적용을 명시).
    _plan = ((s3.get('manifest') or {}).get('component_plan') or None)

    def _add(key, label, present, unconv, resid=None, detail='', plan_key=None):
        if not present:
            if _plan is None or plan_key is None or plan_key not in _plan:
                return                                   # 옛 payload = 판단 근거 없음 → 침묵
            if _plan.get(plan_key):
                badges.append({'key': key, 'label': label, 'status': 'warn', 'resid': None,
                               'detail': '계획됐는데 결과가 없다 (조용한 실패 의심)'})
            else:
                badges.append({'key': key, 'label': label, 'status': 'skip', 'resid': None,
                               'detail': '계획에서 제외됨 (LEAN)'})
            return
        # ★F1(리뷰): resid 문턱(solver 규약 1e-6)도 unconv 로 판정 — payload 가 trust 문자열을 안 넣는
        #   채널(σ_ion 은 ion_resid 만 방출, trust 문자열 없음)이 항상 'ok' 로 새는 false-green 방어.
        if not unconv and resid is not None:
            try:
                unconv = float(resid) > 1e-6
            except (TypeError, ValueError):
                pass
        badges.append({'key': key, 'label': label,
                       'status': 'warn' if unconv else 'ok',
                       'resid': resid, 'detail': detail})

    # electronic·ionic 은 step3 최상위(sigma_*_eff_S_cm), thermal/pore/rxn 은 중첩
    _add('sigma_e', 'σ_e (전자)',
         present=('sigma_e_eff_S_cm' in s3),
         unconv=_has_unconverged(s3.get('trust')),
         resid=s3.get('cg_resid'), plan_key='electronic')
    _add('sigma_ion', 'σ_ion (이온)',
         present=('sigma_ion_eff_S_cm' in s3),
         unconv=_has_unconverged(s3.get('ion_trust')),   # payload 미방출 → _add 의 resid 문턱(1e-6)이 판정
         resid=s3.get('ion_resid'), plan_key='ionic')
    _th = s3.get('thermal') or {}
    _add('thermal', 'κ (열전도)',
         present=bool(_th) and ('kappa_eff_mW_cmK' in _th or 'cg_resid' in _th),
         unconv=_has_unconverged(_th.get('trust')),
         resid=_th.get('cg_resid'), plan_key='thermal')
    _po = s3.get('pore') or {}
    _add('pore', 'τ (기공확산)',
         present=bool(_po) and ('tau' in _po or 'resid' in _po),
         unconv=_has_unconverged(_po.get('trust')),
         resid=_po.get('resid'), plan_key='pore')
    #  ★ RGL-01 (Codex 10-05) — 집전체 기하 (component `collector_geom`) = 보조 σ_e 솔브 둘 (wetted · bare) 의 차.  둘 다
    #    수렴해야 R_geom · jb 가 결과다 (producer · check_arm · 판정기 공용 계약).  배지는 producer 와 **같은 이름**의 상태 ·
    #    수렴 3필드를 읽는다.  3필드가 없는 옛 payload = 판단 근거 없음 → skip (warn 으로 소급하지 않는다).
    _cg = s3.get('collector_geometric')
    _cgs = (((s3.get('manifest') or {}).get('components') or {}).get('collector_geom') or {}).get('status')
    if isinstance(_cg, dict) or _cgs in ('unconverged', 'failed'):
        _cg = _cg if isinstance(_cg, dict) else {}
        _cvk = ('wetted_cg_info', 'wetted_unconverged', 'wetted_cg_resid',
                'bare_cg_info', 'bare_unconverged', 'bare_cg_resid')
        _res = [_cg.get(k) for k in ('wetted_cg_resid', 'bare_cg_resid')]
        if _cgs in ('unconverged', 'failed'):
            _st, _dt = 'warn', f'collector_geom {_cgs} — R_geom · jb 미게시'
        elif not all(k in _cg for k in _cvk):
            _st, _dt = 'skip', '보조 솔브 수렴 3필드 없음 (RGL-01 이전 payload — 판단 근거 없음)'
        else:
            _bad = (any(_cg.get(k) is not False for k in ('wetted_unconverged', 'bare_unconverged'))
                    or any(_cg.get(k) != 0 for k in ('wetted_cg_info', 'bare_cg_info'))
                    or not all(isinstance(r, (int, float)) and not isinstance(r, bool)
                               and math.isfinite(r) and 0 <= r <= 1e-6 for r in _res))
            _st, _dt = ('warn' if _bad else 'ok'), 'wetted · bare 수렴 3필드'
        badges.append({'key': 'collector_geom', 'label': '집전체 기하 R_geom (wetted·bare)', 'status': _st,
                       'resid': max((r for r in _res if isinstance(r, (int, float))), default=None), 'detail': _dt})
    else:
        _add('collector_geom', '집전체 기하 R_geom (wetted·bare)', present=False, unconv=False,
             plan_key='collector')
    _rx = s3.get('rxn') or {}
    _add('rxn', 'STEP4 반응분포',
         present=bool(_rx) and ('resid' in _rx or 'kcl_err' in _rx),
         unconv=_has_unconverged(_rx.get('trust')),
         resid=_rx.get('resid'), detail=(f"KCL {_rx.get('kcl_err')}" if _rx.get('kcl_err') is not None else ''))

    # 구조 sanity: porosity 0/None/≥60% = 비물리(과압축 sentinel 또는 broken) — 항상 확인
    por = mm.get('porosity_mpm_pct')
    por_bad = (por is None) or (por <= 0) or (por >= 60)
    badges.append({'key': 'porosity', 'label': '공극률 물리범위',
                   'status': 'warn' if por_bad else 'ok',
                   'resid': None,
                   'detail': (f'{por}% (0<ε<60 벗어남)' if por_bad else f'{por}%')})

    conv_badges = [b for b in badges if b['key'] != 'porosity']
    n_warn = sum(1 for b in badges if b['status'] == 'warn')
    if n_warn:                  # ★F3(리뷰): 어떤 배지든 warn(porosity=과압축 sentinel 포함) → warn (na 로 숨기지 않음)
        overall = 'warn'
    elif not conv_badges:       # STEP3 미실행 + 구조 정상 → na (수렴 판정 대상 없음)
        overall = 'na'
    else:
        overall = 'ok'
    return {'overall': overall, 'converged': (overall == 'ok'),
            'n_warn': n_warn, 'badges': badges}


def build_meta(data: dict, name: str, *, uploaded_at: str | None = None,
               size_mb: float | None = None) -> dict:
    """webapp/app.py `mpm_lab_upload` 과 **동일한** meta dict (+ trust).

    라우트와 CLI 훅이 이 함수를 공유 → meta 스키마 drift 방지.  size_mb 는
    payload.json 기록 후 파일크기로 채우는 게 정확(모르면 dumps 길이 근사)."""
    mm = data.get('mpm_metrics', {}) or {}
    ac = mm.get('additive_counts') or {}
    _sel = ((mm.get('step3') or {}).get('collector') or {}).get('selected') or {}
    collector = (f"{_sel.get('name')} (R_int {_sel.get('R_int_ohm_cm2'):g}Ωcm²)"
                 if _sel.get('name') else '')
    _man = ((mm.get('step3') or {}).get('manifest') or {})
    _vox_um = (mm.get('step3') or {}).get('vox_um')
    if _vox_um is None:
        _vox_um = _man.get('vox_um')
    #  ★★ 2026-09-07 — **규약을 meta 로 끌어올린다.**  payload 는 스탬프·σ 표·origin 위상을
    #    `step3.manifest` 에 이미 적는데 meta 가 안 읽어서, 목록에서 규약이 다른 런이 구분 없이
    #    나란히 보였다.  같은 침대라도 PTFE 규약 하나로 σ_e 비가 1.12↔1.31 로 갈린다(CL-49)
    #    ⇒ 표시 문제가 아니라 **비교 가능성**의 문제다.  값은 만들지 않고 있는 것만 옮긴다.
    convention = {k: _man[k] for k in (
        'ptfe_stamp', 'sdcp_stamp', 'fibre_stamp', 'vox_um', 'periodic_xy',
        'origin_shift_um', 'plate_rule', 'schema_version', 'sdcp_sphere_d_um',
        'sdcp_yield_to_vgcf', 'ptfe_zero_dof',
        'sigma_vgcf_S_cm', 'sigma_sdcp_S_cm', 'sigma_ptfe_S_cm',
    ) if k in _man}
    #  ⚠ 요청 ≠ 실제 = **도장만 찍히고 규약이 안 걸린** 회귀의 유일한 증인 (CDXR2-6).
    #    `legacy-unversioned` 는 옛 런이라 불일치가 아니다.
    mismatch = [f'{lbl}: 요청 {_man[req]} ≠ 실제 {_man[act]}'
                for act, req, lbl in (('ptfe_stamp', 'ptfe_stamp_requested', 'ptfe'),
                                      ('fibre_stamp', 'fibre_stamp_requested', 'fibre'))
                if act in _man and req in _man
                and _man[req] not in (None, 'legacy-unversioned')
                and _man[act] != _man[req]]
    #  표시 문자열도 **여기서** 만든다 — Jinja 와 JS 가 각자 조립하면 그것이 이 모듈이
    #  경고하는 바로 그 drift 다 (렌더러 둘, 규약 하나).
    _cl = []
    if convention.get('ptfe_stamp') and convention['ptfe_stamp'] != 'off':
        _cl.append(f"PTFE {convention['ptfe_stamp']}")
    if convention.get('sdcp_stamp') == 'sphere':
        _cl.append(f"SDCP 구 Ø{convention.get('sdcp_sphere_d_um')}")
    for _k, _lab in (('sigma_vgcf_S_cm', 'σ_VGCF'), ('sigma_sdcp_S_cm', 'σ_SDCP'),
                     ('sigma_ptfe_S_cm', 'σ_PTFE')):
        if convention.get(_k):
            _cl.append(f'{_lab} {convention[_k]:g}')
    _osh = convention.get('origin_shift_um') or []
    if any(_osh):
        _cl.append('origin ' + ','.join(f'{float(x):g}' for x in _osh))
    if convention.get('periodic_xy'):
        _cl.append('periodic-xy')
    if convention.get('sdcp_yield_to_vgcf'):
        _cl.append('⚠ SDCP→VGCF 양보(진단팔)')
    if size_mb is None:
        size_mb = round(len(json.dumps(data)) / 1e6, 1)
    return {
        'convention': convention,
        'convention_mismatch': mismatch,
        'convention_label': ' · '.join(_cl),
        'name': name,
        'source_case': data.get('case', ''),
        'porosity': mm.get('porosity_mpm_pct'),
        'thickness': mm.get('thickness_mpm_um'),
        'se_fraction': mm.get('se_fraction_pct'),
        'n_am': mm.get('n_am') or len(data.get('particles', [])),
        'additive_counts': ac,
        'recipe': ' · '.join(f'{k} {int(v):,}' for k, v in ac.items()) if ac else '',
        'collector': collector,
        'vox_um': _vox_um,
        'has_additives': bool(ac),
        'uploaded_at': uploaded_at or datetime.now().strftime('%Y-%m-%d %H:%M'),
        'size_mb': size_mb,
        'mpm_metrics': mm,
        'trust': compute_trust(mm),          # ← 등록 훅이 채우는 수렴 배지 (④ 데이터-측)
    }


def register_local(data: dict, name: str, dest: str, *,
                   uploaded_at: str | None = None) -> tuple[str, str, dict]:
    """dest(mpm_lab 폴더)에 `<name-slug>_<uuid6>/{payload.json,meta.json}` 기록.

    라우트와 동일 레이아웃/네이밍 → Flask 동적 로딩이 그대로 인식.  (pid, dir, meta) 반환."""
    if data.get('kind') != 'mpm' or 'particles' not in data:
        raise ValueError('MPM payload 아님 (kind=mpm + particles 필요). '
                         'mpm_payload.json 을 넣으세요(metrics 파일 아님).')
    pid = f"{slugify(name)[:52]}_{uuid.uuid4().hex[:6]}"   # NAME 부분만 cap → uuid 보존
    d = os.path.join(dest, pid)
    os.makedirs(d, exist_ok=True)
    pj = os.path.join(d, 'payload.json')
    with open(pj, 'w') as out:
        json.dump(data, out)
    meta = build_meta(data, name, uploaded_at=uploaded_at,
                      size_mb=round(os.path.getsize(pj) / 1e6, 1))
    with open(os.path.join(d, 'meta.json'), 'w') as mf:
        json.dump(meta, mf)
    return pid, d, meta


def push_http(payload_path: str, url: str, name: str, *,
              retries: int = 4, timeout: int = 600) -> dict:
    """실행중 webapp 의 /mpm-lab/upload 로 HTTP push (Render 등 원격).

    서버가 자기 쪽 build_meta 로 등록 → 이 리팩터 후엔 서버 meta 도 trust 포함.
    네트워크 오류만 지수 백오프 재시도(2,4,8,16s)."""
    try:
        import requests
    except ImportError:
        raise RuntimeError("--url 모드는 requests 필요 (pip install requests)")
    last = None
    last = None
    for attempt in range(retries):
        try:
            with open(payload_path, 'rb') as fh:
                r = requests.post(url, files={'payload': fh},
                                  data={'name': name}, timeout=timeout)
            if r.status_code == 200:
                return r.json()
            # ★F2(리뷰): 4xx(클라이언트 오류: 400/404/413/415/422…)는 재시도 무의미 → 상태코드로 즉시 실패
            #   (기존 body 문자열 '400'/'415' 검사는 404/413 등을 놓쳐 대용량 payload를 4회 재-POST했음).
            if 400 <= r.status_code < 500:
                raise RuntimeError(f"HTTP {r.status_code} (4xx, 재시도 안 함): {r.text[:200]}")
            last = f"HTTP {r.status_code}: {r.text[:200]}"          # 5xx = 서버 일시오류 → 재시도
        except RuntimeError:                                        # 4xx fast-fail (위 raise) — 재시도 금지
            raise
        except Exception as e:                                      # 네트워크/타임아웃류만 재시도
            last = str(e)
        if attempt < retries - 1:
            wait = 2 ** (attempt + 1)
            print(f"  push 실패({last}) — {wait}s 후 재시도 [{attempt + 1}/{retries}]", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError(f"HTTP push 실패 ({retries}회): {last}")


def push_rsync(local_dir: str, remote: str, *, dry_run: bool = False) -> int:
    """로컬 등록 폴더를 원격 mpm_lab 로 rsync(ssh).  remote = 'host:/path/to/mpm_lab'.

    ssh 자격/키는 사용자 환경(원격 실행 컨테이너엔 ssh 없음)."""
    import subprocess
    dst = remote.rstrip('/') + '/' + os.path.basename(local_dir.rstrip('/'))
    cmd = ['rsync', '-az', local_dir.rstrip('/') + '/', dst + '/']
    print('  ' + ' '.join(cmd))
    if dry_run:
        return 0
    return subprocess.call(cmd)


def _default_dest() -> str:
    return (os.environ.get('WEBAPP_MPM_LAB_FOLDER')
            or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mpm_lab'))


def main(argv=None):
    ap = argparse.ArgumentParser(description='MPM payload → mpm_lab 등록 훅 (결과회수 자동화)')
    ap.add_argument('--payload', required=True, help='mpm_payload.json 경로')
    ap.add_argument('--name', default='', help='표시 이름 (기본: payload.case)')
    g = ap.add_mutually_exclusive_group()
    g.add_argument('--dest', default='', help=f'로컬/공유 mpm_lab 폴더 (기본 {_default_dest()})')
    g.add_argument('--url', default='', help='실행중 webapp /mpm-lab/upload URL (HTTP push)')
    ap.add_argument('--rsync', default='', help='로컬 등록 후 rsync 할 원격 host:mpm_lab (dest 와 함께)')
    ap.add_argument('--dry-run', action='store_true', help='rsync 명령만 출력')
    a = ap.parse_args(argv)

    with open(a.payload) as fh:
        data = json.load(fh)
    name = (a.name or data.get('case') or 'payload').strip()

    if a.url:                                    # ── HTTP push (원격 webapp) ──
        res = push_http(a.payload, a.url, name)
        item = res.get('item', {}) if isinstance(res, dict) else {}
        tr = (item.get('trust') or {})
        print(f"✓ 등록(HTTP): {item.get('id', '?')}  "
              f"porosity {item.get('porosity')}%  trust={tr.get('overall', '?')}")
        return 0

    dest = a.dest or _default_dest()             # ── 로컬 파일시스템 등록 ──
    os.makedirs(dest, exist_ok=True)
    pid, d, meta = register_local(data, name, dest)
    tr = meta['trust']
    warn = [b['label'] for b in tr['badges'] if b['status'] == 'warn']
    print(f"✓ 등록(로컬): {pid}")
    print(f"  → {d}")
    print(f"  porosity {meta['porosity']}%  두께 {meta['thickness']}µm  SE {meta['se_fraction']}%"
          + (f"  · {meta['recipe']}" if meta['recipe'] else ''))
    print(f"  trust: {tr['overall'].upper()}"
          + (f"  ⚠ {', '.join(warn)}" if warn else '  (모든 배지 통과)'))

    if a.rsync:                                  # ── 로컬 등록 → 원격 rsync ──
        rc = push_rsync(d, a.rsync, dry_run=a.dry_run)
        print(f"  rsync → {a.rsync}: {'OK' if rc == 0 else f'FAIL(rc={rc})'}")
        return rc
    return 0


# ─────────────────────────── self-test ───────────────────────────
def _selftest() -> int:
    fails = []
    # slug: 연속점 붕괴(traversal 차단) + uuid 보존 자리
    assert slugify('a..b') == 'a_b', slugify('a..b')
    assert slugify('VGCF2.97') == 'VGCF2.97'
    assert slugify('  ///  ') == 'payload'
    # trust: --no-step3 → na, 구조배지만
    t0 = compute_trust({'porosity_mpm_pct': 12.7})
    assert t0['overall'] == 'na' and t0['converged'] is False, t0
    assert any(b['key'] == 'porosity' and b['status'] == 'ok' for b in t0['badges'])
    # porosity 0 = sentinel → warn (★F3: step3 없어도 overall='warn', 'na' 로 숨기지 않음)
    _p0 = compute_trust({'porosity_mpm_pct': 0})
    assert _p0['n_warn'] >= 1 and _p0['overall'] == 'warn', _p0
    assert compute_trust({'porosity_mpm_pct': 65})['overall'] == 'warn'
    # ★F1: σ_ion 은 payload 가 trust 문자열 없이 ion_resid 만 방출 — resid>1e-6 → warn (false-green 방어)
    _ion = compute_trust({'porosity_mpm_pct': 15, 'step3': {
        'sigma_ion_eff_S_cm': 1.0, 'ion_resid': 1e-2}})
    assert _ion['overall'] == 'warn' and any(
        b['key'] == 'sigma_ion' and b['status'] == 'warn' for b in _ion['badges']), _ion
    # 반대로 낮은 ion_resid → ok
    assert compute_trust({'porosity_mpm_pct': 15, 'step3': {
        'sigma_ion_eff_S_cm': 1.0, 'ion_resid': 1e-9}})['overall'] == 'ok'
    # step3 수렴 = ok
    ok = compute_trust({'porosity_mpm_pct': 15, 'step3': {
        'sigma_e_eff_S_cm': 3.0, 'cg_resid': 1e-9, 'trust': 'σ_e OK',
        'thermal': {'kappa_eff_mW_cmK': 2.0, 'cg_resid': 1e-8, 'trust': 'κ OK'}}})
    assert ok['overall'] == 'ok' and ok['converged'], ok
    # UNCONVERGED 마커 감지 → warn
    bad = compute_trust({'porosity_mpm_pct': 15, 'step3': {
        'sigma_e_eff_S_cm': 3.0, 'cg_resid': 1e-2,
        'trust': 'σ_e ⚠UNCONVERGED (resid 1e-2)'}})
    assert bad['overall'] == 'warn' and bad['n_warn'] >= 1, bad
    # build_meta: 라우트 필드 존재 + trust 포함
    data = {'kind': 'mpm', 'case': 'demo', 'particles': [[0, 0, 0, 1]],
            'mpm_metrics': {'porosity_mpm_pct': 15, 'thickness_mpm_um': 30,
                            'se_fraction_pct': 27, 'n_am': 1,
                            'additive_counts': {'VGCF': 100}}}
    m = build_meta(data, 'demo')
    for k in ('name', 'porosity', 'thickness', 'se_fraction', 'recipe',
              'uploaded_at', 'size_mb', 'mpm_metrics', 'trust'):
        assert k in m, f'meta missing {k}'
    assert m['recipe'] == 'VGCF 100' and m['has_additives'], m

    # ★★ 2026-09-07 — **규약을 meta 로 올린다.**  payload 는 `step3.manifest` 에 스탬프·σ 표·
    #   origin 위상을 이미 적고 있는데 meta 가 그것을 **안 읽어서**, mpm_lab 목록에서 규약이
    #   다른 런이 구분 없이 나란히 보였다.  같은 침대라도 PTFE 규약 하나로 σ_e 비가 1.12↔1.31
    #   로 갈리므로(CL-49) 이것은 표시 문제가 아니라 **비교 가능성**의 문제다.
    def _mk(man, **mm_extra):
        return {'kind': 'mpm', 'case': 'c', 'particles': [[0, 0, 0, 1]],
                'mpm_metrics': dict({'porosity_mpm_pct': 15, 'step3': dict(
                    {'sigma_e_eff_S_cm': 0.054, 'cg_resid': 1e-9,
                     'manifest': man}, **mm_extra)})}
    _man = {'ptfe_stamp': 'centerline', 'ptfe_stamp_requested': 'centerline',
            'sdcp_stamp': 'point', 'sdcp_sphere_d_um': 0.0,
            'fibre_stamp': 'segment', 'fibre_stamp_requested': 'segment',
            'vox_um': 0.15, 'periodic_xy': False,
            'origin_shift_um': [0.075, 0.0, 0.0],
            'sigma_vgcf_S_cm': 78.5398, 'sigma_sdcp_S_cm': 0.0, 'sigma_ptfe_S_cm': 0.0,
            'component_plan': {'electronic': True, 'ionic': False,
                               'thermal': False, 'pore': False, 'collector': False}}
    mc = build_meta(_mk(_man), 'conv')
    cv = mc.get('convention') or {}
    for k in ('ptfe_stamp', 'sdcp_stamp', 'fibre_stamp', 'vox_um',
              'periodic_xy', 'origin_shift_um', 'sigma_vgcf_S_cm'):
        assert k in cv, f'convention missing {k}: {cv}'
    assert cv['ptfe_stamp'] == 'centerline' and cv['sigma_vgcf_S_cm'] == 78.5398, cv
    assert not mc.get('convention_mismatch'), mc.get('convention_mismatch')
    # 표시 문자열은 build_meta 가 만든다 (렌더러 둘이 각자 조립하면 drift)
    lab = mc.get('convention_label') or ''
    assert 'PTFE centerline' in lab and 'σ_VGCF 78.5398' in lab and 'origin 0.075' in lab, lab
    assert 'σ_SDCP' not in lab, lab            # 0 인 항은 싣지 않는다 (빈 값 노이즈 방지)

    # ★ 요청 ≠ 실제 → **경고**.  이 쌍이 payload 에 있는 이유가 그것이다 (CDXR2-6):
    #   스탬프가 조용히 안 걸려도 매니페스트는 요청값을 적어 도장을 달던 회귀가 있었다.
    _bad = dict(_man, ptfe_stamp='off', ptfe_stamp_requested='centerline')
    mb = build_meta(_mk(_bad), 'conv-bad')
    assert mb.get('convention_mismatch'), mb.get('convention')
    assert any('ptfe' in s for s in mb['convention_mismatch']), mb['convention_mismatch']

    # ★ LEAN=2 (--no-ion) — 계획에 없으니 σ_ion 부재는 **정상**.  warn 내지 않는다.
    tl = compute_trust(_mk(_man)['mpm_metrics'])
    assert tl['overall'] == 'ok', tl
    assert any(b['key'] == 'sigma_ion' and b['status'] == 'skip' for b in tl['badges']), tl

    # ★★ 반대로 **계획했는데 결과가 없으면** = 조용히 죽은 것 → warn.
    #   현행은 `present` 만 보므로 이 경우를 **침묵으로 통과**시킨다 (M-R3-03 과 같은 혼동).
    _plan_ion = dict(_man, component_plan=dict(_man['component_plan'], ionic=True))
    tm = compute_trust(_mk(_plan_ion)['mpm_metrics'])
    assert tm['overall'] == 'warn', tm
    assert any(b['key'] == 'sigma_ion' and b['status'] == 'warn' for b in tm['badges']), tm

    # ★ 소급 금지 — `component_plan` 없는 옛 payload 는 기존 동작 그대로 (과잉차단 안 함).
    _old = {k: v for k, v in _man.items() if k != 'component_plan'}
    to = compute_trust(_mk(_old)['mpm_metrics'])
    assert to['overall'] == 'ok', to
    assert not any(b['key'] == 'sigma_ion' for b in to['badges']), to

    # ★ RGL-01 (Codex 10-05) — 집전체 기하 배지 = 보조 솔브 (wetted · bare) 수렴 3필드 · collector_geom 상태 (producer 와 같은 이름)
    _cgok = {'wetted_sigma_S_cm': 0.08, 'bare_sigma_S_cm': 0.05, 'R_geom_ohm_cm2': 1.2e-4,
             'wetted_cg_info': 0, 'wetted_unconverged': False, 'wetted_cg_resid': 1e-9,
             'bare_cg_info': 0, 'bare_unconverged': False, 'bare_cg_resid': 1e-9}
    _man_c = dict(_man, component_plan=dict(_man['component_plan'], collector=True),
                  components={'collector_geom': {'status': 'complete'}})

    def _cgb(t):
        return next((b for b in t['badges'] if b['key'] == 'collector_geom'), None)
    tc = compute_trust(_mk(_man_c, collector_geometric=_cgok)['mpm_metrics'])
    assert tc['overall'] == 'ok' and (_cgb(tc) or {}).get('status') == 'ok', tc
    _man_u = dict(_man_c, components={'collector_geom': {'status': 'unconverged', 'reason': '보조 솔브 미수렴'}})
    tu = compute_trust(_mk(_man_u, collector_geometric=dict(_cgok, R_geom_ohm_cm2=None, bare_cg_info=1,
                                                             bare_unconverged=True, bare_cg_resid=0.35))['mpm_metrics'])
    assert tu['overall'] == 'warn' and (_cgb(tu) or {}).get('status') == 'warn', tu      # allow-partial 게시본
    tt = compute_trust(_mk(_man_c, collector_geometric=dict(_cgok, wetted_unconverged=True))['mpm_metrics'])
    assert (_cgb(tt) or {}).get('status') == 'warn', tt                                     # 상태는 complete 인데 3필드 미수렴
    tn = compute_trust(_mk(_man_c, collector_geometric=dict(_cgok, wetted_cg_resid=None))['mpm_metrics'])
    assert (_cgb(tn) or {}).get('status') == 'warn', tn                                     # 키는 있는데 잔차 null (NaN 벨트) = 수렴 미확인
    _cg_old = {k: v for k, v in _cgok.items() if 'cg_' not in k and 'unconverged' not in k}
    tq = compute_trust(_mk(_man_c, collector_geometric=_cg_old)['mpm_metrics'])
    assert (_cgb(tq) or {}).get('status') == 'skip' and tq['overall'] == 'ok', tq        # 옛 payload = 판단 근거 없음
    assert (_cgb(tl) or {}).get('status') == 'skip', tl                                     # LEAN (--no-collector) = 계획 제외

    # register_local roundtrip (임시폴더)
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        pid, d, meta = register_local(data, 'demo case', td)
        assert os.path.isfile(os.path.join(d, 'payload.json'))
        assert os.path.isfile(os.path.join(d, 'meta.json'))
        assert pid.startswith('demo_case_') and len(pid.split('_')[-1]) == 6, pid
        rt = json.load(open(os.path.join(d, 'meta.json')))
        assert rt['trust']['overall'] == 'na', rt['trust']   # no step3
    # non-mpm 거부
    try:
        register_local({'kind': 'dem'}, 'x', '/tmp')
        fails.append('non-mpm 미거부')
    except ValueError:
        pass
    print('selftest OK' if not fails else 'selftest FAIL: ' + '; '.join(fails))
    return 1 if fails else 0


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--selftest':
        raise SystemExit(_selftest())
    raise SystemExit(main())
