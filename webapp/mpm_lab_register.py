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
    # 또는 Render 원격 webapp 로 직접 push
    python webapp/mpm_lab_register.py --payload out/mpm_payload.json \
        --name "DBE_2C_N10"  --url https://dem-analyzer.onrender.com/mpm-lab/upload
"""
from __future__ import annotations

import argparse
import json
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

    def _add(key, label, present, unconv, resid=None, detail=''):
        if not present:
            return
        badges.append({'key': key, 'label': label,
                       'status': 'warn' if unconv else 'ok',
                       'resid': resid, 'detail': detail})

    # electronic·ionic 은 step3 최상위(sigma_*_eff_S_cm), thermal/pore/rxn 은 중첩
    _add('sigma_e', 'σ_e (전자)',
         present=('sigma_e_eff_S_cm' in s3),
         unconv=_has_unconverged(s3.get('trust')),
         resid=s3.get('cg_resid'))
    _add('sigma_ion', 'σ_ion (이온)',
         present=('sigma_ion_eff_S_cm' in s3),
         unconv=_has_unconverged(s3.get('ion_trust')),   # 문자열 없으면 resid 만 보고 (아래)
         resid=s3.get('ion_resid'))
    _th = s3.get('thermal') or {}
    _add('thermal', 'κ (열전도)',
         present=bool(_th) and ('kappa_eff_mW_cmK' in _th or 'cg_resid' in _th),
         unconv=_has_unconverged(_th.get('trust')),
         resid=_th.get('cg_resid'))
    _po = s3.get('pore') or {}
    _add('pore', 'τ (기공확산)',
         present=bool(_po) and ('tau' in _po or 'resid' in _po),
         unconv=_has_unconverged(_po.get('trust')),
         resid=_po.get('resid'))
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
    if not conv_badges:
        overall = 'na'          # STEP3 미실행 → 수렴 판정 대상 없음(구조 배지만)
    elif n_warn:
        overall = 'warn'
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
    _vox_um = (mm.get('step3') or {}).get('vox_um')
    if size_mb is None:
        size_mb = round(len(json.dumps(data)) / 1e6, 1)
    return {
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
    for attempt in range(retries):
        try:
            with open(payload_path, 'rb') as fh:
                r = requests.post(url, files={'payload': fh},
                                  data={'name': name}, timeout=timeout)
            if r.status_code == 200:
                return r.json()
            # 4xx(잘못된 payload 등)는 재시도 무의미 → 즉시 실패
            if 400 <= r.status_code < 500:
                raise RuntimeError(f"HTTP {r.status_code}: {r.text[:200]}")
            last = f"HTTP {r.status_code}: {r.text[:200]}"
        except Exception as e:   # 네트워크류만 재시도
            last = str(e)
            if '400' in last or '415' in last:
                break
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
    # porosity 0 = sentinel → warn
    assert compute_trust({'porosity_mpm_pct': 0})['n_warn'] >= 1
    assert compute_trust({'porosity_mpm_pct': 65})['n_warn'] >= 1
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
