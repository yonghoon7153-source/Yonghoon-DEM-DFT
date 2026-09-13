#!/usr/bin/env python3
"""S0 — **협착 항이 삭제된 간선이 몇 개인가** (면적 계약 §4, 계산 불변).

정본 계약 = `docs/area_contract_20260913.md`.  원장 = `SELF-28` · `AREA-01`~`AREA-04`.
적대 검토 = `docs/reviews/codex_verdict_area_contract_20260913.md`.

⛔⛔ **초판(커밋 9392860a8)은 HOLD 였다** — Codex 가 네 P1 을 냈다.  초판은 helper 를
**다시 구현**해 세었고 그래서 생산 솔버와 모집단·입력 경로가 갈렸다:
  · `AREA-01` δ 부재/0 을 건너뛰었다.  솔버는 **native contact_area** 를 쓴다
    ⇒ 합성 반례에서 S0 **0 %** ↔ 솔버 **100 %**.
  · `AREA-02` S0 는 **raw 행**, 솔버는 정렬 ID쌍 key 의 **마지막 채택 행**만 센다
    ⇒ **90 %** ↔ **0 %** (반대 방향도 재현).
  · Hertz 대조가 생산 Hertz 가 아니었다 (생산 Hertz 가지엔 ψ 삭제가 **없다**)
    ⇒ S0 100 % ↔ 실제 `Rc = 5.206583187 > 0`.
  · helper 예외가 **비삭제**로 집계됐고 오류 카운터가 없었다.
  · `_pair_kind` 가 *"AM 이 아니면 SE"* 였다 (미등록 type9 가 AM_SE 로).
  · ★ selftest 가 **판별력 0** 이었다 — 소스 문자열 존재만 봐서, `R_constriction = 0`
    대입을 `R_Maxwell` 로 바꿔 실제 Rc 가 **0 → 0.20771261697** 이 돼도 **13/13 PASS**.
    (`SELF-25`·`L4-03` 과 같은 부류이고 이번엔 **내가 만든 계측기**에서 났다.)

★★ **2판의 설계 = 다시 구현하지 않는다.  솔버를 부른다.**
`network_conductivity.build_network(..., contact_mode=...)` 를 **그대로 호출**하고 돌려받은
간선에서 `R_constriction == 0` 을 센다.  그러면
  · δ 부재/0 의 native 면적 fallback  (AREA-01)
  · 정렬 ID쌍 dedup 과 마지막-채택  (AREA-02)
  · 채널별 상 필터 (ionic=SE–SE · electronic=AM–AM · thermal=전부)
  · Hertz-명명 가지에 ψ 삭제가 없다는 사실
이 **전부 솔버의 것**이 된다 — 우리가 흉내 낼 여지가 없다.
⇒ selftest 도 구조적으로 판별력을 갖는다: 솔버의 `Rc = 0` 분기를 바꾸면 이 수가 **반드시**
움직인다 (회귀 ⑥ 이 그것을 강제한다).

★ 문턱 자체는 기록으로만 남긴다 (판정용 아님):
    Rc = 0 분기  <=>  psi <= 1e-4  <=>  a/r_min >= 0.99784556531
                <=>  A >= 0.9956957722087699 * pi * r_min^2
⚠ **문서의 옛 등가식은 틀렸다** (Codex [P2]) — `psi` **정확히 0** 은 `A/(pi r^2) >= 1` 이고
  `Rc = 0` 분기는 그보다 **낮은** 0.99570 에서 이미 켜진다.  둘은 다른 문턱이다.

⚠ **계산을 바꾸지 않는다** — 읽기 전용이다.  솔버도 코퍼스도 건드리지 않는다.
⚠ `Rc = 0` 은 **협착 항** 삭제다.  보통 `R_bulk` 는 남는다 — 간선 삭제나 총저항 0 과
  섞지 말 것 (그것은 `L2-10` 의 다른 양이다).
⚠ box_x/box_y 는 `d_ij` → `R_bulk` 에만 들어가고 `R_constriction` 에는 안 들어간다
  ⇒ 삭제 집계는 상자 크기에 **불변**이다 (그래서 넉넉히 준다).
⚠ 이 컨테이너에는 원 접촉 자료가 없다 — **코퍼스가 있는 머신에서** 돌린다.

사용:
  python3 scripts/audit_constriction_deleted.py --webapp ~/Yonghoon-DEM-DFT/webapp
  python3 scripts/audit_constriction_deleted.py --webapp <경로> --limit 5
  python3 scripts/audit_constriction_deleted.py --webapp <경로> --out-csv docs/data/s0.csv
  python3 scripts/audit_constriction_deleted.py --selftest
"""
from __future__ import annotations
import argparse
import csv
import importlib.util
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / 'scripts'


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


#  규율 (1): 케이스 탐색·로딩은 **이 리포에 이미 있다** — 다시 짜지 않는다.
#  `extract_se_network_diagnostics` 의 로더는 2026-09-13 에 L4-06(내용 지문 중복제거)·
#  L4-07(메타 병합)로 고쳐졌으므로 그 수정을 그대로 물려받는다.
_SED = _load('_sed_loader', SCRIPTS / 'extract_se_network_diagnostics.py')
#  ★★ 2판의 핵심 — 면적 helper 를 다시 구현하지 않고 **솔버를 부른다** (AREA-01/02).
_NC = _load('_nc_solver', SCRIPTS / 'network_conductivity.py')

#  기록용 문턱 (판정에 쓰지 않는다 — 판정은 솔버의 `R_constriction` 이 한다)
PSI_FLOOR = 1e-4
S_STAR = 1.0 - PSI_FLOOR ** (2.0 / 3.0)          # 0.99784556531
AREA_FRAC = S_STAR ** 2                           # 0.9956957722087699

#: 채널 → (build_network mode, target_types 선택자).
#  ⚠ 채널 필터는 `mode` 가 아니라 **`target_types`** 로 걸린다 (`network_conductivity.py:251`).
#    생산 `main` 이 그렇게 만든다:
#      ionic      target_types = [k for k,v in type_map.items() if v == 'SE']
#      electronic am_types     = [k for k,v in type_map.items() if 'AM' in v]
#      thermal    전부 (thermal 가지는 `:246` 에서 필터를 건너뛴다)
#    처음에 셋 다 전체 type 을 넘겼더니 ionic·electronic 이 AM–SE 를 **받아 버렸다**
#    (selftest ⑤a·⑤b 가 빨간불).  그 반례를 그대로 검사로 남긴다.
CHANNELS = {
    'ionic':      ('ionic',      lambda tm: {k for k, v in tm.items() if v == 'SE'}),
    'electronic': ('electronic', lambda tm: {k for k, v in tm.items() if 'AM' in str(v)}),
    'thermal':    ('thermal',    lambda tm: set(tm)),
}

#: 허용 상 이름 — 미등록 type 을 조용히 SE 로 만들지 않는다 (Codex [P2])
_AM = frozenset({'AM_P', 'AM_S', 'AM'})
_SE = frozenset({'SE'})


def _pair_kind(t1, t2):
    """상 쌍 분류.  **모르는 상은 `UNKNOWN`** 이다 (옛 판은 "AM 이 아니면 SE" 였다)."""
    def k(t):
        if t in _AM:
            return 'AM'
        if t in _SE:
            return 'SE'
        return '?'
    a, b = k(t1), k(t2)
    if '?' in (a, b):
        return 'UNKNOWN'
    return {('AM', 'AM'): 'AM_AM', ('SE', 'SE'): 'SE_SE'}.get((a, b), 'AM_SE')


def type_map_from_deck(deck_path):
    """LIGGGHTS 덱에서 **type → 상** 지도를 유도한다.  두 신호를 교차확인한다.

    ★ 왜 필요한가 (실측): LHS 코퍼스는 **케이스마다 type 구성이 다르다**.
      `lhs00_000` 은 헤더가 `bimodal (3-type)` 인데 `lhs00_100` 의 원자 분포는
      `{1: 796, 2: 30315}` 로 **type 3 이 0개**다.  하나를 박아 두면 채널 분류가 통째로
      틀린다 — `AREA-02`(모집단이 조용히 달라진다)를 재생산하는 자리다.

    신호 ①  `fix pts<N> ... particletemplate/sphere ... atom_type <T> ... radius constant ${VAR}`
             → VAR 이름(`r_AM_P` · `r_AM_S` · `r_SE`)이 상을 말한다.
    신호 ②  `fix m1 ... youngsModulus peratomtype E1 E2 ...`
             → **연화된 값**(<1e7 sim)이 SE 다 (AM 은 1.4e8).

    ⛔ 둘이 어긋나거나 어느 하나라도 못 읽으면 **거부**한다 (추측하지 않는다).
    """
    txt = Path(deck_path).read_text(errors='replace')
    tm, src = {}, {}
    for raw in txt.split('\n'):
        line = raw.split('#', 1)[0].strip()
        if 'particletemplate/sphere' not in line:
            continue
        toks = line.split()
        t = var = None
        for i, w in enumerate(toks):
            if w == 'atom_type' and i + 1 < len(toks):
                try:
                    t = int(toks[i + 1])
                except ValueError:
                    pass
            if w == 'radius' and i + 2 < len(toks) and toks[i + 1] == 'constant':
                var = toks[i + 2]
        if t is None or not var:
            continue
        u = var.upper().strip('${}')
        #  ⚠ 순서가 중요하다 — mono 케이스는 `${r_AM}` 로 **접미사가 없다**
        #    (`lhs00_100: mono_AM_S (2-type)` 의 덱이 그렇다).  AM_P/AM_S 를 먼저 보고
        #    그 다음 SE, 마지막에 맨 AM.
        ph = ('AM_P' if 'AM_P' in u else
              'AM_S' if 'AM_S' in u else
              'SE'   if 'SE'   in u else
              'AM'   if 'AM'   in u else None)
        if ph is None:
            raise ValueError(f'{deck_path}: atom_type {t} 의 반경 변수 {var!r} 에서 '
                             f'상을 못 읽는다 (AM_P·AM_S·AM·SE 중 하나여야 한다)')
        if t in tm and tm[t] != ph:
            raise ValueError(f'{deck_path}: atom_type {t} 가 {tm[t]} 와 {ph} 로 중복 정의')
        tm[t] = ph
        src[t] = var
    if not tm:
        raise ValueError(f'{deck_path}: particletemplate/sphere 를 못 찾았다')

    #  ── 신호 ② 로 **교차확인** ────────────────────────────────────────────
    es = []
    for raw in txt.split('\n'):
        line = raw.split('#', 1)[0].strip()
        if 'youngsModulus' in line and 'peratomtype' in line:
            for p in line.split('peratomtype')[-1].split():
                try:
                    es.append(float(p))
                except ValueError:
                    break
            break
    if es:
        soft = {i + 1 for i, e in enumerate(es) if e < 1e7}
        declared_se = {t for t, v in tm.items() if v == 'SE'}
        if soft and declared_se and soft != declared_se:
            raise ValueError(
                f'{deck_path}: 두 신호가 어긋난다 — 템플릿이 말하는 SE={sorted(declared_se)} '
                f'인데 youngsModulus 의 연화 type={sorted(soft)} (E={es}).  추측하지 않는다.')
    return tm, src


def audit_case(case_dir, contact_mode='physics', channels=('ionic', 'electronic', 'thermal'),
               deck_dir=None):
    """한 케이스 — **솔버가 만든 간선**에서 `R_constriction == 0` 을 센다.

    ⚠ 예외를 **비삭제로 만들지 않는다** — 실패는 `error` 로 올리고 `None` 을 돌려준다
    (옛 판은 helper 예외를 삼켜 분모에는 남기고 삭제는 0 으로 셌다).
    """
    atoms, type_map, scale, _meta = _SED.load_case(case_dir)
    #  ★ 덱이 있으면 **그것이 정본**이다 — meta.json 의 손으로 적은 지도보다 우선한다
    #    (케이스마다 type 구성이 다르다는 것을 실측으로 확인했다).
    deck_used = ''
    if deck_dir:
        cands = [Path(deck_dir) / case_dir.name / f'input_{case_dir.name}.liggghts',
                 Path(deck_dir) / f'input_{case_dir.name}.liggghts']
        dk = next((p for p in cands if p.is_file()), None)
        if dk is None:
            raise ValueError(f'덱을 못 찾았다: {[str(p) for p in cands]}')
        type_map, _src = type_map_from_deck(dk)
        deck_used = str(dk)
    contacts = _SED.load_contacts(case_dir)
    if not contacts:
        raise ValueError('접촉 행이 0개')
    plate_z = _SED.estimate_plate_z(atoms)
    #  box: 최소영상이 절대 안 걸리게 넉넉히 (삭제 집계는 상자에 불변 — 헤더 참조)
    span = max((max(a['x'] for a in atoms.values()) - min(a['x'] for a in atoms.values()),
                max(a['y'] for a in atoms.values()) - min(a['y'] for a in atoms.values()),
                1e-9))
    box = span * 1000.0

    from collections import Counter as _C
    type_hist = _C(a['type'] for a in atoms.values())
    all_types = sorted(type_hist)
    row = {'case': case_dir.name, 'contact_mode': contact_mode,
           'n_contact_rows': len(contacts),
           'type_hist': ';'.join(f'{t}:{type_hist[t]}' for t in all_types),
           'type_map': ';'.join(f'{k}={v}' for k, v in sorted(type_map.items())),
           'deck': deck_used}
    for ch in channels:
        mode, pick = CHANNELS[ch]
        tt = pick(type_map)
        #  ⚠ 빈 선택을 **전체로 대체하지 않는다** — 그러면 채널 필터가 조용히 사라진다.
        if not tt:
            raise ValueError(
                f'채널 {ch}: type_map 에서 고른 target_types 가 비었다.  '
                f'type_map={dict(sorted(type_map.items()))} · '
                f'원자 type 분포={dict(type_hist)}')
        net = _NC.build_network(atoms, contacts, tt, scale,
                                plate_z, box_x=box, box_y=box,
                                mode=mode, type_map=type_map,
                                contact_mode=contact_mode)
        #  `build_network:196` 은 `target_ids` 가 비면 **None** 을 돌려준다.
        if net is None:
            n_hit = sum(type_hist[t] for t in tt if t in type_hist)
            raise ValueError(
                f'채널 {ch}: build_network 가 None (해당 상의 입자가 없다).  '
                f'target_types={sorted(tt)} · 그 type 의 원자 {n_hit}개 · '
                f'원자 type 분포={dict(type_hist)} · '
                f'type_map={dict(sorted(type_map.items()))}')
        edges = net['edges'] if isinstance(net, dict) else net[1]
        n = d = 0
        by_kind = {}
        for e in edges:
            kd = _pair_kind(type_map.get(e['type1'], '?'), type_map.get(e['type2'], '?'))
            n += 1
            dele = (e['R_constriction'] == 0.0)
            d += 1 if dele else 0
            s_ = by_kind.setdefault(kd, [0, 0])
            s_[0] += 1
            s_[1] += 1 if dele else 0
        row[f'{ch}_n_edges'] = n
        row[f'{ch}_n_deleted'] = d
        row[f'{ch}_deleted_pct'] = round(100.0 * d / n, 4) if n else 0.0
        for kd in ('AM_AM', 'AM_SE', 'SE_SE', 'UNKNOWN'):
            nn, dd = by_kind.get(kd, (0, 0))
            row[f'{ch}_{kd}_n'] = nn
            row[f'{ch}_{kd}_deleted'] = dd
    return row


def main() -> int:
    ap = argparse.ArgumentParser(
        description='협착 항이 삭제된 **간선** 비율 (면적 계약 S0, 2판 — 솔버 호출)')
    ap.add_argument('--contact-mode', default='physics',
                    choices=['physics', 'hertzian'],
                    help='솔버의 contact_mode.  생산 Physics 가지가 기본. '
                         'hertzian 은 ψ 삭제 가지를 **타지 않는다** (대조용).')
    ap.add_argument('--channels', default='ionic,electronic,thermal',
                    help='채널 — ionic=SE–SE · electronic=AM–AM · thermal=전부')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--out-csv', default='')
    #  ⚠ CLAUDE.md 가 경고한 자리 — **코드 폴더 ≠ 데이터 폴더**.
    ap.add_argument('--webapp', default='',
                    help='results/ · archive/ 가 있는 폴더.  env AUDIT_WEBAPP 도 가능.')
    ap.add_argument('--deck-dir', default='',
                    help='LIGGGHTS 덱이 있는 폴더 — `<deck-dir>/<case>/input_<case>.liggghts`.  '
                         '주면 **덱에서 type_map 을 유도**한다 (meta.json 보다 우선).')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return _selftest()

    import os as _os
    wp = a.webapp or _os.environ.get('AUDIT_WEBAPP', '')
    if wp:
        _SED.WEBAPP = Path(wp).expanduser().resolve()
    print(f'webapp = {_SED.WEBAPP}')
    if not _SED.WEBAPP.is_dir():
        print(f'\n⛔ 그런 폴더가 없다: {_SED.WEBAPP}')
        return 2
    subs = [d for d in ('results', 'archive') if (_SED.WEBAPP / d).is_dir()]
    if not subs:
        print(f'\n⛔ {_SED.WEBAPP} 안에 results/ 도 archive/ 도 없다')
        return 2
    print(f'  하위: {", ".join(subs)}')

    chans = tuple(c.strip() for c in a.channels.split(',') if c.strip())
    bad = [c for c in chans if c not in CHANNELS]
    if bad:
        print(f'⛔ 모르는 채널: {bad}')
        return 2

    cases = _SED.discover_cases()
    if a.limit:
        cases = cases[:a.limit]
    print(f'케이스 {len(cases)}개 · contact_mode={a.contact_mode} · 채널 {",".join(chans)}')
    print(f'기록용 문턱: A >= {AREA_FRAC:.16f} · π · r_min²   '
          f'(판정은 솔버의 R_constriction 이 한다)')
    if not cases:
        print('\n⛔ 접촉 자료를 못 찾았다 — atoms.csv + contacts.csv + (input_params|meta).json')
        return 1

    rows, errs = [], []
    for i, d in enumerate(cases):
        try:
            r = audit_case(d, contact_mode=a.contact_mode, channels=chans,
                           deck_dir=(a.deck_dir or None))
        except Exception as e:                      # ⚠ 실패를 **비삭제로 만들지 않는다**
            errs.append((d.name, f'{type(e).__name__}: {e}'))
            print(f'  [{i+1:>3}/{len(cases)}] {d.name[:34]:34s}  ⛔ {type(e).__name__}')
            continue
        rows.append(r)
        pc = r.get(f'{chans[0]}_deleted_pct', 0.0)
        print(f'  [{i+1:>3}/{len(cases)}] {r["case"][:34]:34s} '
              f'{chans[0]} {r.get(chans[0]+"_n_edges",0):>8,d} edge  삭제 {pc:>6.2f} %')

    if errs:
        print(f'\n⛔ 실패 {len(errs)}건 — **집계를 발행하지 않는다** (부분 census 금지):')
        for nm, msg in errs[:10]:
            print(f'    {nm}: {msg}')
        return 3
    if not rows:
        print('집계할 행이 없다.')
        return 1

    print('\n═══ 간선 가중 집계 ═══')
    print(f'  케이스 {len(rows)} (실패 0)')
    for ch in chans:
        n = sum(r[f'{ch}_n_edges'] for r in rows)
        d = sum(r[f'{ch}_n_deleted'] for r in rows)
        print(f'  {ch:11s} 삭제 {d:>10,d} / {n:>10,d} = '
              f'{(100.0*d/n if n else 0.0):7.3f} %')
        for kd in ('AM_AM', 'AM_SE', 'SE_SE', 'UNKNOWN'):
            nn = sum(r[f'{ch}_{kd}_n'] for r in rows)
            dd = sum(r[f'{ch}_{kd}_deleted'] for r in rows)
            if nn:
                print(f'      {kd:8s} {dd:>10,d} / {nn:>10,d} = {100.0*dd/nn:7.3f} %')
    print('\n⚠ 이것은 **협착 항** 삭제다 (R_bulk 는 보통 남는다).  간선 삭제·총저항 0 과 다르다.')
    print('⚠ 채널별로 따로 읽을 것 — AM–SE 비율을 이온망 하한으로 쓰지 않는다 (AREA-02).')

    if a.out_csv:
        p = Path(a.out_csv)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)
        print(f'\n→ {p}')
    return 0


def _selftest() -> int:
    """★ **판별력**이 핵심이다 — 초판은 소스 문자열 존재만 봐서 Rc=0 분기를 바꿔도 13/13 PASS 였다.

    2판은 실제 `build_network` 를 돌려 그 출력을 세므로, ⑥ 이 *"솔버 분기를 바꾸면 이 수가
    움직인다"* 를 **직접** 확인한다.
    """
    ok = True

    def chk(name, cond, extra=''):
        nonlocal ok
        print(('  ✓ ' if cond else '  ✗ ') + name + (f'   {extra}' if extra else ''))
        ok = ok and bool(cond)

    print('협착 삭제 census (S0 2판 — 솔버 호출)')

    R = 1.0                                    # sim 반경
    scale = 1.0

    def net(rows, mode='thermal', cm='physics'):
        atoms = {1: {'type': 1, 'radius': R, 'x': 0.0, 'y': 0.0, 'z': 0.0},
                 2: {'type': 3, 'radius': R, 'x': 2 * R, 'y': 0.0, 'z': 0.0}}
        tm = {1: 'AM_P', 3: 'SE'}
        #  ⚠ 생산과 같은 방식 — 채널 필터는 target_types 가 건다
        tt = CHANNELS[{'ionic': 'ionic', 'electronic': 'electronic'}.get(mode, 'thermal')][1](tm)
        n = _NC.build_network(atoms, rows, tt, scale, 10.0,
                              box_x=1e4, box_y=1e4, mode=mode, type_map=tm,
                              contact_mode=cm)
        e = n['edges'] if isinstance(n, dict) else n[1]
        return e

    deep = {'id1': 1, 'id2': 2, 'contact_area': 0.998 * math.pi * R * R, 'delta': 0.0}
    shallow = {'id1': 1, 'id2': 2, 'contact_area': 1e-6, 'delta': 1e-6}

    # ── ① AREA-01: δ=0 인데 native 면적이 크면 **솔버는 삭제**한다 ──────────
    e = net([deep])
    chk('①a AREA-01: δ=0 · native 면적 0.998πr² → 간선 1개', len(e) == 1)
    chk('①b AREA-01: 그 간선의 R_constriction 이 **0** (옛 S0 는 이걸 0 %로 셌다)',
        len(e) == 1 and e[0]['R_constriction'] == 0.0,
        f"Rc={e[0]['R_constriction'] if e else '—'}")

    # ── ② 대조: 얕은 접촉은 삭제되지 않는다 (게이트가 "항상 삭제" 가 아니다) ─
    e = net([shallow])
    chk('② 대조: 얕은 접촉은 Rc > 0',
        len(e) == 1 and e[0]['R_constriction'] > 0.0,
        f"Rc={e[0]['R_constriction'] if e else '—'}")

    # ── ③ AREA-02: 같은 ID쌍 여러 행 → **간선 1개**, 마지막 행이 이긴다 ─────
    e = net([deep] * 9 + [shallow])
    chk('③a AREA-02: raw 10행 → 간선 **1개** (옛 S0 는 10행을 셌다)', len(e) == 1)
    chk('③b AREA-02: 마지막이 shallow 이면 **삭제 아님** (옛 S0 는 90 % 삭제)',
        len(e) == 1 and e[0]['R_constriction'] > 0.0)
    e = net([shallow] * 9 + [deep])
    chk('③c AREA-02: 마지막이 deep 이면 **삭제** (옛 S0 는 10 %)',
        len(e) == 1 and e[0]['R_constriction'] == 0.0)

    # ── ④ Hertz-명명 가지에는 ψ 삭제가 없다 ────────────────────────────────
    e = net([deep], cm='hertzian')
    chk('④ 생산 Hertz 가지는 같은 접촉에서 Rc > 0 (옛 S0 는 100 % 삭제로 셌다)',
        len(e) == 1 and e[0]['R_constriction'] > 0.0,
        f"Rc={e[0]['R_constriction'] if e else '—'}")

    # ── ⑤ 채널 필터가 솔버의 것이다 ────────────────────────────────────────
    chk('⑤a ionic 은 AM–SE 를 안 받는다', len(net([deep], mode='ionic')) == 0)
    chk('⑤b electronic 도 AM–SE 를 안 받는다', len(net([deep], mode='electronic')) == 0)
    chk('⑤c thermal 은 받는다', len(net([deep], mode='thermal')) == 1)
    chk('⑤d 상 분류가 "AM 이 아니면 SE" 가 아니다 — 미등록은 UNKNOWN',
        _pair_kind('AM_P', 'type9') == 'UNKNOWN' and _pair_kind('?', '?') == 'UNKNOWN'
        and _pair_kind('AM_P', 'SE') == 'AM_SE')

    # ── ⑥ ★★ 판별력: 솔버의 Rc=0 분기를 바꾸면 이 census 가 **반드시** 움직인다 ─
    src = (SCRIPTS / 'network_conductivity.py').read_text(encoding='utf-8')
    mutated = src.replace('                R_constriction = 0.0\n',
                          '                R_constriction = R_Maxwell\n', 1)
    chk('⑥a 변이 지점이 실재한다 (소스가 바뀌었다)', mutated != src)
    import types as _t
    m = _t.ModuleType('_nc_mut')
    m.__file__ = str(SCRIPTS / 'network_conductivity.py')
    sys.path.insert(0, str(SCRIPTS))
    exec(compile(mutated, m.__file__, 'exec'), m.__dict__)
    atoms = {1: {'type': 1, 'radius': R, 'x': 0.0, 'y': 0.0, 'z': 0.0},
             2: {'type': 3, 'radius': R, 'x': 2 * R, 'y': 0.0, 'z': 0.0}}
    em = m.build_network(atoms, [deep], {1, 3}, scale, 10.0, box_x=1e4, box_y=1e4,
                         mode='thermal', type_map={1: 'AM_P', 3: 'SE'},
                         contact_mode='physics')
    em = em['edges'] if isinstance(em, dict) else em[1]
    chk('⑥b ★ 변이판에서는 같은 접촉이 **삭제되지 않는다** — 이 검사에 판별력이 있다 '
        '(초판은 이 변이에도 13/13 PASS 였다)',
        len(em) == 1 and em[0]['R_constriction'] != 0.0,
        f"변이 Rc={em[0]['R_constriction'] if em else '—'}")

    # ── ⑦ 문턱 기록값 (판정용 아님) ────────────────────────────────────────
    chk('⑦ 기록 문턱 A/(πr²) = 0.9956957722087699 (ψ 정확 0 인 1 과 **다르다**)',
        abs(AREA_FRAC - 0.9956957722087699) < 1e-15, f'{AREA_FRAC!r}')

    # ── ⑨ 덱에서 type_map 유도 — **케이스마다 다르다** (실측 두 종류) ──────
    import tempfile as _tf
    tdir = Path(_tf.mkdtemp())
    bi = tdir / 'input_bi.liggghts'
    bi.write_text(
        '# lhs00_000: bimodal (3-type) | LHS design\n'
        'fix m1 all property/global youngsModulus peratomtype 1.4e8 1.4e8 0.135e7\n'
        'fix pts1 all particletemplate/sphere 15485863 atom_type 1 density constant 4800 '
        'radius constant ${r_AM_P}\n'
        'fix pts2 all particletemplate/sphere 15485867 atom_type 2 density constant 4800 '
        'radius constant ${r_AM_S}\n'
        'fix pts3 all particletemplate/sphere 32452843 atom_type 3 density constant 2000 '
        'radius constant ${r_SE}\n')
    mo = tdir / 'input_mono.liggghts'
    mo.write_text(
        '# lhs00_100: mono_AM_S (2-type) | LHS design\n'
        'fix m1 all property/global youngsModulus peratomtype 1.4e8 0.135e7\n'
        'fix pts1 all particletemplate/sphere 15485863 atom_type 1 density constant 4800 '
        'radius constant ${r_AM}\n'
        'fix pts2 all particletemplate/sphere 32452843 atom_type 2 density constant 2000 '
        'radius constant ${r_SE}\n')
    chk('⑨a 3-type 덱 → {1:AM_P, 2:AM_S, 3:SE}',
        type_map_from_deck(bi)[0] == {1: 'AM_P', 2: 'AM_S', 3: 'SE'},
        str(type_map_from_deck(bi)[0]))
    chk('⑨b ★ 2-type mono 덱 → {1:AM, 2:SE} (접미사 없는 `${r_AM}` — 실측 반례)',
        type_map_from_deck(mo)[0] == {1: 'AM', 2: 'SE'},
        str(type_map_from_deck(mo)[0]))
    chk('⑨c 그 둘이 **다르다** — 하나를 박아 두면 채널 분류가 틀린다',
        type_map_from_deck(bi)[0] != type_map_from_deck(mo)[0])
    bad = tdir / 'input_bad.liggghts'
    bad.write_text(
        'fix m1 all property/global youngsModulus peratomtype 0.135e7 1.4e8\n'
        'fix pts1 all particletemplate/sphere 1 atom_type 1 density constant 4800 '
        'radius constant ${r_AM}\n'
        'fix pts2 all particletemplate/sphere 2 atom_type 2 density constant 2000 '
        'radius constant ${r_SE}\n')
    try:
        type_map_from_deck(bad); raised = False
    except ValueError:
        raised = True
    chk('⑨d 대조: 두 신호(템플릿 이름 ↔ 연화 영률)가 어긋나면 **거부**한다', raised)

    # ── ⑧ 계약·판정문이 실재하고 서로를 가리키는가 ─────────────────────────
    doc = ROOT / 'docs' / 'area_contract_20260913.md'
    ver = ROOT / 'docs' / 'reviews' / 'codex_verdict_area_contract_20260913.md'
    chk('⑧ 계약·판정문 둘 다 있다', doc.exists() and ver.exists())

    print('협착 삭제 census SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
