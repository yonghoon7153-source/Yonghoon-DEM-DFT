#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""git 에 남은 케이스 표에서 **웹앱 케이스 폴더를 되살린다**.

★ 왜 (2026-08-25): 윈도우 재설치로 WSL 이 날아가 `webapp/{uploads,results}` 를 통째로 잃었다.
  옛 WSL 이미지·Windows.old·휴지통·kgy·D 드라이브를 전부 뒤졌으나 `meta.json` 이 어디에도 없었다.
  **그런데 케이스의 *숫자* 는 git 에 남아 있다** — `docs/data/case_master.csv` 가
  163 케이스 × 421 지표를 담고 있고, 그 `case` 열이 웹앱의 `<TIMESTAMP-cid>` 형식 그대로다.
  ⇒ 그 표를 되펴서 `uploads/<id>/meta.json` + `results/<id>/full_metrics.json` 을 다시 쓴다.

⚠⚠ **이것은 재실행이 아니다 — CSV 에서 되편 것이다.**  둘을 섞으면 안 되므로 **모든 산출물에
  표식을 박는다**: `meta.json` 의 `reconstructed`·`reconstructed_from`, `full_metrics.json` 의
  `_reconstructed` 블록.  표에 없던 키는 **만들어 내지 않는다** (없으면 없는 채로 둔다).

되살아나는 것 / 안 되살아나는 것:
  ✅ 케이스 목록 · 지표 표 · Group 비교 · 랭킹 · 등급(grade) — `full_metrics` 로 도는 것 전부
  ⛔ 그림(figures/*.png) · report.md · 3D 뷰어 · MPM payload · **원본 LIGGGHTS 덤프**
     → 그것들은 원자료가 있어야 하고, 원자료는 없다.

  python3 scripts/rebuild_cases_from_csv.py --check          # 무엇이 몇 개 복원되나 (쓰지 않음)
  python3 scripts/rebuild_cases_from_csv.py --write          # 실제로 쓴다
  python3 scripts/rebuild_cases_from_csv.py --write --force  # 기존 케이스가 있어도 (덮지는 않는다)
  python3 scripts/rebuild_cases_from_csv.py --selftest
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)

#: 우선순위 순 — 앞의 표가 더 풍부하면 뒤의 표는 **없는 케이스만** 채운다.
SOURCES = (
    ('docs/data/case_master.csv', 'case', 'name', ''),
    ('docs/case_summary.csv', 'case_id', None, 'fm__'),
)

#: ★ **이름(name)으로 조인해 보충**하는 표.  case_id 가 없고 `input_*` 이름만 있는 표들인데,
#:   MPM 열이 case_master(27/163)보다 훨씬 잘 차 있다 (corpus 169/291).  ⇒ 있는 것을 다 쓴다.
#:   ⚠ **덮지 않는다** — 이미 있는 키는 그대로 두고 **빈 자리만** 채운다 (case_master 가 정본).
NAME_SOURCES = (
    ('docs/data/design_performance_corpus.csv', 'name'),
    ('docs/data/case_3d_collection.csv', 'case'),
    ('docs/data/mpm_dem_porosity_reliability.csv', 'case'),
)


def _data_root():
    return os.environ.get('DEM_WEB_DATA') or os.path.join(os.path.expanduser('~'),
                                                          'Yonghoon-DEM-DFT')


def _coerce(v):
    """CSV 문자열 → 원래 타입.  **모르면 문자열 그대로 둔다** (추측해서 망가뜨리지 않는다)."""
    if v is None:
        return None
    s = v.strip()
    if s in ('', 'None', 'nan', 'NaN', 'null'):
        return None
    low = s.lower()
    if low in ('true', 'false'):
        return low == 'true'
    try:
        f = float(s)
    except ValueError:
        return s
    if s.lstrip('-').isdigit() and abs(f) < 2 ** 53:
        return int(s)
    return f


def unflatten(flat):
    """`a.b.c` 점 표기를 중첩 dict 로.  `full_metrics.json` 이 원래 그 모양이다."""
    out = {}
    for k, v in flat.items():
        if v is None:
            continue
        cur = out
        parts = k.split('.')
        for p in parts[:-1]:
            nxt = cur.get(p)
            if not isinstance(nxt, dict):
                nxt = {}
                cur[p] = nxt
            cur = nxt
        cur[parts[-1]] = v
    return out


def _created_from_id(case_id):
    """`260418_172642_6968ef` → ISO 시각.  형식이 다르면 빈 문자열 (지어내지 않는다)."""
    p = case_id.split('_')
    if len(p) >= 2 and len(p[0]) == 6 and len(p[1]) == 6 and p[0].isdigit() and p[1].isdigit():
        d, t = p[0], p[1]
        return f'20{d[:2]}-{d[2:4]}-{d[4:6]}T{t[:2]}:{t[2:4]}:{t[4:6]}'
    return ''


def collect(root=None):
    """→ {case_id: {'name', 'metrics', 'source'}}  (앞 표 우선, 뒤 표는 보충)"""
    root = root or _ROOT
    cases = {}
    for rel, id_col, name_col, prefix in SOURCES:
        p = os.path.join(root, rel)
        if not os.path.isfile(p):
            continue
        with open(p, encoding='utf-8', errors='replace') as f:
            for row in csv.DictReader(f):
                cid = (row.get(id_col) or '').strip()
                if not cid or cid in cases:
                    continue
                flat = {}
                for k, v in row.items():
                    if k in (id_col, name_col):
                        continue
                    if prefix:
                        if not k.startswith(prefix):
                            continue
                        k = k[len(prefix):]
                    c = _coerce(v)
                    if c is not None:
                        flat[k] = c
                cases[cid] = {'name': (row.get(name_col) or cid) if name_col else cid,
                              'metrics': unflatten(flat), 'source': rel,
                              'n_fields': len(flat)}
    #  ── 이름으로 조인해 **빈 자리만** 보충 ────────────────────────────────────────────
    #  ⚠⚠ 2026-08-25 실측 — `design_performance_corpus.csv` 의 `name` 열은 **섞여 있다**:
    #    MPM 이 채워진 169행은 `name` 이 **케이스 ID**(`260418_172642_6968ef`)이고 나머지는
    #    `input_*` 이름이다.  이름만으로 조인하니 MPM 열이 **169행 전부 빗나갔다**
    #    (겹침 0).  그래서 케이스당 MPM 이 27건뿐이었다.
    #    ⇒ 조인 키를 **이름 ∪ 케이스ID** 로 넓힌다.
    by_name = {}
    for cid, c in cases.items():
        by_name.setdefault(c['name'], cid)
        by_name.setdefault(cid, cid)          # ★ 케이스 ID 로도 찾을 수 있게
    for rel, name_col in NAME_SOURCES:
        p2 = os.path.join(root, rel)
        if not os.path.isfile(p2):
            continue
        with open(p2, encoding='utf-8', errors='replace') as f:
            for row in csv.DictReader(f):
                nm = (row.get(name_col) or '').strip()
                cid = by_name.get(nm)
                if not cid:
                    continue
                m = cases[cid]['metrics']
                added = 0
                for k, v in row.items():
                    if k == name_col or k in m:
                        continue          # ⚠ 있는 키는 **안 덮는다** (case_master 가 정본)
                    cv = _coerce(v)
                    if cv is not None:
                        m[k] = cv
                        added += 1
                if added:
                    cases[cid]['n_fields'] += added
                    cases[cid].setdefault('merged', []).append(f'{os.path.basename(rel)}(+{added})')
    return cases


#: 케이스가 "완전" 하려면 있어야 하는 축 — 없으면 **다시 돌려야** 하는 것.
def _mpm_porosity_keys():
    """MPM porosity 열 이름 — **정본은 `rebuild_tables_from_metrics.MPM_POROSITY_KEYS`**.

    ⚠⚠ 2026-08-25: 이 목록을 여기서 따로 적고 있다가 `mpm_porosity_pct` 를 빠뜨려
      "MPM 압밀 결손 23/169" 라는 **오보**를 냈다 (실제 결손은 6건).  같은 누락이
      `mpm_metrics()` 에도 있어 파일 17건이 안 만들어졌다.  ⇒ 베끼지 않고 **가져온다**.
      가져오기 실패 시에만 안전한 사본을 쓰고, selftest 가 둘의 일치를 강제한다.
    """
    try:
        import sys as _s
        _s.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from rebuild_tables_from_metrics import MPM_POROSITY_KEYS
        return tuple(MPM_POROSITY_KEYS)
    except Exception:
        return ('mpm.porosity_mpm_pct', 'mpm_porosity_mpm_pct', 'mpm_porosity_pct')


GAP_AXES = {
    'DEM σ 삼중항': ('sigma_ionic_full_mScm', 'electronic_sigma_full_mScm',
                     'thermal_sigma_full_mScm', 'sigma_ion', 'sigma_el'),
    #  ★ 'mpm'(중첩 dict) · compacted 는 여기 고유 후보, porosity 열은 정본에서 가져온다
    'MPM 압밀': _mpm_porosity_keys() + ('mpm', 'mpm_compacted_porosity_pct'),
    #  ⚠ **severe 등급만** 센다.  결손이라는 23건도 `frac_fragmentation_*` 는 갖고 있다 —
    #    그런데 그 둘은 **다른 양**이다 (둘 다 가진 146건에서 중앙 |Δ| 0.595 · 최대 39.13,
    #    fragmentation ≥ severe = 더 넓은 등급).  ⇒ 별칭으로 묶지 않는다.  묶으면 없는
    #    지표를 있다고 보고하게 된다 (MPM 쪽 누락을 고치면서 반대 실수를 하지 않는다).
    '취성/파괴(severe 등급)': ('fracture_severe_pct', 'frac_severe_force_pct'),
}


def gap_report(cases):
    """무엇이 없어서 **다시 돌려야** 하나 — 축별 결손 케이스 수."""
    out = {}
    for ax, keys in GAP_AXES.items():
        miss = [c['name'] for c in cases.values()
                if not any(k in c['metrics'] for k in keys)]
        out[ax] = miss
    #  뷰어/그림은 원자료가 있어야 하므로 **전부 결손**이다 (CSV 로 못 만든다)
    out['3D 뷰어 · 그림 · report'] = [c['name'] for c in cases.values()]
    return out


def write(cases, data_root=None, force=False):
    """`uploads/<id>/meta.json` + `results/<id>/full_metrics.json` 을 쓴다.

    ⚠ **기존 파일은 덮지 않는다** — 진짜 런이 있으면 그쪽이 정본이다 (복원이 실물을 지우면
      이번 사고의 되풀이다).  이미 있으면 건너뛰고 센다.
    """
    dr = data_root or _data_root()
    up = os.path.join(dr, 'webapp', 'uploads')
    rs = os.path.join(dr, 'webapp', 'results')
    made, skipped = 0, 0
    for cid, c in sorted(cases.items()):
        ud, rd = os.path.join(up, cid), os.path.join(rs, cid)
        mf, ff = os.path.join(ud, 'meta.json'), os.path.join(rd, 'full_metrics.json')
        if os.path.exists(mf) or os.path.exists(ff):
            skipped += 1
            continue
        os.makedirs(ud, exist_ok=True)
        os.makedirs(rd, exist_ok=True)
        stamp = {'reconstructed': True,
                 'reconstructed_from': c['source'],
                 'reconstructed_note': ('CSV 표에서 되편 것이다 — **재실행이 아니다**.  '
                                        '그림·report·3D·원본 덤프는 없다.'),
                 'reconstructed_fields': c['n_fields']}
        #  ★ 2026-08-25 — `mode` 를 **데이터에서 유도**한다 (옛 판은 'unknown' 을 박았다).
        #    웹앱 규약: 입자 3종(AM_P+AM_S+SE) = bimodal · 2종(AM+SE) = standard
        #    (`app.py` §detect mode).  ⇒ AM_P/AM_S 입자수가 **둘 다** 있으면 bimodal.
        #    ⚠ 판정 근거가 없으면 'unknown' 그대로 둔다 — 추측해서 채우지 않는다.
        met = c['metrics']
        _p = met.get('AM_P_n_particles') is not None
        _s = met.get('AM_S_n_particles') is not None
        mode = 'bimodal' if (_p and _s) else ('standard' if (_p or _s) else 'unknown')
        extra = {'mode': mode}
        if mode != 'unknown':
            extra['mode_source'] = 'AM_P/AM_S 입자수 유무에서 유도 (추측 아님)'
        for k_meta, k_src in (('scale', 'meta.scale'), ('ps_ratio', 'ps_ratio'),
                              ('type_map', 'meta.type_map')):
            v = met.get(k_src.split('.')[-1]) if '.' not in k_src else \
                (met.get('meta') or {}).get(k_src.split('.')[-1])
            if v is not None:
                extra[k_meta] = v
        with open(mf, 'w', encoding='utf-8') as f:
            json.dump({'name': c['name'], 'created': _created_from_id(cid),
                       'status': 'reconstructed', **extra, **stamp},
                      f, ensure_ascii=False, indent=1)
        with open(ff, 'w', encoding='utf-8') as f:
            json.dump({**c['metrics'], '_reconstructed': stamp}, f, ensure_ascii=False, indent=1)
        made += 1
    return made, skipped


def refill(cases, data_root=None):
    """이미 복원해 둔 케이스의 `full_metrics.json` 에 **빠진 키만** 채운다.

    ⚠⚠ 왜 이게 따로 필요한가 (2026-08-25 실측):  `write()` 는 파일이 하나라도 있으면
      케이스를 **통째로** 건너뛴다 — 진짜 런을 지키려면 그게 옳다.  그런데 복원 코드가
      **좋아졌을 때** (예: 조인 키를 고쳐 MPM 열이 146건 새로 들어왔을 때) 이미 복원해 둔
      케이스는 **영원히 옛 상태로 남는다**.  다시 돌려도 `건너뜀 169건` 만 찍히고
      아무 일도 안 일어나는데 **출력은 성공처럼 보인다** = 선언과 실행이 갈라진다
      (오늘 하루 반복해서 잡은 그 병).  ⇒ 갱신 경로를 **이름 있는 동작**으로 만든다.

    안전장치 셋 — 이게 `--force` 와 다른 점이다:
      · `status == 'reconstructed'` 인 케이스만 건드린다 (**진짜 런은 손대지 않는다**)
      · **있는 키는 절대 안 덮는다** — 빈 자리만 채운다 (case_master 가 정본)
      · 새 케이스를 만들지 않는다 (그건 `write()` 소관)

    반환: (건드린 케이스, 채운 키 총합, 실런이라 건너뛴 케이스, 아직 없어 건너뛴 케이스)
    """
    dr = data_root or _data_root()
    up = os.path.join(dr, 'webapp', 'uploads')
    rs = os.path.join(dr, 'webapp', 'results')
    touched = added = kept_real = absent = 0
    for cid, c in sorted(cases.items()):
        mf = os.path.join(up, cid, 'meta.json')
        ff = os.path.join(rs, cid, 'full_metrics.json')
        if not os.path.exists(ff):
            absent += 1                      # 아직 복원 안 된 케이스 → `--write` 소관
            continue
        #  ★ 실런 보호 — meta 가 없거나 reconstructed 가 아니면 **읽고 끝낸다**
        try:
            with open(mf, encoding='utf-8') as f:
                meta = json.load(f) or {}
        except Exception:
            meta = {}
        if meta.get('status') != 'reconstructed':
            kept_real += 1
            continue
        try:
            with open(ff, encoding='utf-8') as f:
                cur = json.load(f) or {}
        except Exception:
            kept_real += 1                   # 못 읽으면 **건드리지 않는다**
            continue
        new = {k: v for k, v in c['metrics'].items() if k not in cur}
        if not new:
            continue
        cur.update(new)
        st = cur.get('_reconstructed')
        if isinstance(st, dict):
            st['refilled_fields'] = int(st.get('refilled_fields') or 0) + len(new)
            st['refilled_note'] = ('복원 코드가 좋아져 **빠져 있던 키를 나중에 채웠다**.  '
                                   '기존 값은 하나도 안 덮었다.')
        with open(ff, 'w', encoding='utf-8') as f:
            json.dump(cur, f, ensure_ascii=False, indent=1)
        touched += 1
        added += len(new)
    return touched, added, kept_real, absent


def _selftest():
    import tempfile
    n = [0, 0]

    def chk(m, ok):
        n[1] += 1
        n[0] += bool(ok)
        print(f'  {"PASS" if ok else "FAIL"}  {m}')

    chk('① 점 표기를 중첩으로 되편다',
        unflatten({'a.b': 1, 'a.c': 2, 'd': 3}) == {'a': {'b': 1, 'c': 2}, 'd': 3})
    chk('② None 은 키를 아예 안 만든다 (없는 것을 만들어 내지 않는다)',
        unflatten({'a': None, 'b': 1}) == {'b': 1})
    chk('③ 타입 복원 — int/float/bool/str',
        (_coerce('3') == 3 and isinstance(_coerce('3'), int)
         and _coerce('3.5') == 3.5 and _coerce('true') is True
         and _coerce('abc') == 'abc' and _coerce('nan') is None))
    chk('④ ★ 모르는 문자열은 **문자열로 둔다** (추측해서 망가뜨리지 않는다)',
        _coerce('1e5x') == '1e5x' and _coerce('2026-01-02') == '2026-01-02')
    chk('⑤ case_id → 시각', _created_from_id('260418_172642_6968ef') == '2026-04-18T17:26:42')
    chk('⑥ 형식이 다르면 **빈 문자열** (지어내지 않는다)', _created_from_id('weird') == '')
    #  ★★ 세 곳에 흩어졌던 "MPM porosity 열 이름" 이 **한 곳에서 온다** (베낀 것이 아니라)
    try:
        import sys as _s
        _s.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from rebuild_tables_from_metrics import MPM_POROSITY_KEYS as _CANON
        chk(f'⑥a ★★ GAP_AXES 의 porosity 열이 **정본과 일치** ({len(_CANON)}개)',
            set(_CANON) <= set(GAP_AXES['MPM 압밀']))
        chk('⑥b ★ 옛 누락(`mpm_porosity_pct`)이 실제로 들어 있다 — 23건 오보의 원인',
            'mpm_porosity_pct' in GAP_AXES['MPM 압밀'])
    except ImportError:
        chk('⑥a 정본 모듈을 못 읽었다 (사본으로 동작 — 확인 필요)', False)
    real = collect()
    chk(f'⑦ ★ 실제 표에서 케이스를 읽는다 ({len(real)}건)', len(real) >= 100)
    if real:
        k = next(iter(real))
        chk(f'⑧ 케이스마다 지표가 실려 있다 (예 {real[k]["n_fields"]}개)',
            real[k]['n_fields'] >= 50)
    with tempfile.TemporaryDirectory() as d:
        sub = {'X1': {'name': 'input_a', 'metrics': {'q': 1}, 'source': 's.csv', 'n_fields': 1}}
        made, skip = write(sub, data_root=d)
        mf = os.path.join(d, 'webapp', 'uploads', 'X1', 'meta.json')
        ff = os.path.join(d, 'webapp', 'results', 'X1', 'full_metrics.json')
        chk(f'⑨ 파일을 실제로 만든다 ({made}건)',
            made == 1 and os.path.exists(mf) and os.path.exists(ff))
        m = json.load(open(mf, encoding='utf-8'))
        chk('⑩a ★ 근거가 없으면 mode 는 unknown (추측해서 안 채운다)',
            m.get('mode') == 'unknown' and 'mode_source' not in m)
        fm = json.load(open(ff, encoding='utf-8'))
        chk('⑩ ★★ **복원임을 산출물에 박는다** (재실행과 섞이지 않게)',
            m.get('reconstructed') is True and m.get('status') == 'reconstructed'
            and fm.get('_reconstructed', {}).get('reconstructed') is True)
        made2, skip2 = write(sub, data_root=d)
        chk(f'⑪ ★ 기존 파일을 **덮지 않는다** (실물이 있으면 그쪽이 정본) — 재실행 {made2}건 skip {skip2}건',
            made2 == 0 and skip2 == 1)
        before = open(ff, encoding='utf-8').read()
        write({'X1': {'name': 'DIFFERENT', 'metrics': {'q': 999}, 'source': 's', 'n_fields': 1}},
              data_root=d)
        chk('⑫ ★ 덮어쓰기 시도해도 내용이 안 바뀐다', open(ff, encoding='utf-8').read() == before)
    with tempfile.TemporaryDirectory() as d:
        two = {'B1': {'name': 'b', 'source': 's', 'n_fields': 2,
                      'metrics': {'AM_P_n_particles': 36, 'AM_S_n_particles': 421}},
               'S1': {'name': 's', 'source': 's', 'n_fields': 1,
                      'metrics': {'AM_S_n_particles': 400}}}
        write(two, data_root=d)
        mb = json.load(open(os.path.join(d, 'webapp', 'uploads', 'B1', 'meta.json'), encoding='utf-8'))
        ms = json.load(open(os.path.join(d, 'webapp', 'uploads', 'S1', 'meta.json'), encoding='utf-8'))
        chk(f'⑬ ★ AM_P+AM_S 둘 다 → bimodal ({mb["mode"]})', mb['mode'] == 'bimodal')
        chk(f'⑭ ★ 한 종류만 → standard ({ms["mode"]})', ms['mode'] == 'standard')
        chk('⑮ 유도 근거를 적는다', 'mode_source' in mb and '추측 아님' in mb['mode_source'])

    # ── ⑯ `--refill` — 옛 복원본에 빠진 키를 채운다 (오늘 실제로 겪은 결함) ──────────────
    with tempfile.TemporaryDirectory() as d:
        old = {'C1': {'name': 'c', 'source': 's', 'n_fields': 1,
                      'metrics': {'porosity': 15.0}}}
        write(old, data_root=d)
        ff = os.path.join(d, 'webapp', 'results', 'C1', 'full_metrics.json')
        #  복원 코드가 좋아져 MPM 열이 새로 생긴 상황 + 기존 값은 **다르게** 바뀐 상황
        new = {'C1': {'name': 'c', 'source': 's', 'n_fields': 3,
                      'metrics': {'porosity': 99.0, 'mpm_porosity_mpm_pct': 16.7,
                                  'mpm_thickness_mpm_um': 30.7}}}
        made2, skipped2 = write(new, data_root=d)
        chk('⑯a ★ 재실행은 **아무것도 안 한다** — 이것이 오늘의 결함이었다',
            made2 == 0 and skipped2 == 1
            and 'mpm_porosity_mpm_pct' not in json.load(open(ff, encoding='utf-8')))
        t, added, kept, absent = refill(new, data_root=d)
        cur = json.load(open(ff, encoding='utf-8'))
        chk(f'⑯b --refill 이 빠진 키를 채운다 (케이스 {t} · 키 {added})',
            t == 1 and added == 2 and cur.get('mpm_porosity_mpm_pct') == 16.7)
        chk('⑯c ★ 기존 값은 **안 덮는다** (99 로 안 바뀌고 15 그대로)',
            cur.get('porosity') == 15.0)
        chk('⑯d 보충 사실을 기록에 남긴다',
            (cur.get('_reconstructed') or {}).get('refilled_fields') == 2)
        t2, added2, _, _ = refill(new, data_root=d)
        chk('⑯e 멱등 — 두 번째는 0건 (매번 다시 쓰지 않는다)', t2 == 0 and added2 == 0)
        #  ★★ 실런 보호 — status 가 reconstructed 가 아니면 **손대지 않는다**
        mf = os.path.join(d, 'webapp', 'uploads', 'C1', 'meta.json')
        mm = json.load(open(mf, encoding='utf-8')); mm['status'] = 'done'
        json.dump(mm, open(mf, 'w', encoding='utf-8'))
        json.dump({'porosity': 15.0}, open(ff, 'w', encoding='utf-8'))
        t3, added3, kept3, _ = refill(new, data_root=d)
        chk('⑯f ★★ 진짜 런(status≠reconstructed)은 **건드리지 않는다**',
            t3 == 0 and added3 == 0 and kept3 == 1
            and 'mpm_porosity_mpm_pct' not in json.load(open(ff, encoding='utf-8')))
        #  ★ 아직 복원 안 된 케이스는 refill 이 **만들지 않는다** (write 소관)
        t4, _, _, absent4 = refill({'ZZ': {'name': 'z', 'source': 's', 'n_fields': 1,
                                           'metrics': {'porosity': 1.0}}}, data_root=d)
        chk('⑯g 없는 케이스를 refill 이 **만들어 내지 않는다**',
            t4 == 0 and absent4 == 1
            and not os.path.exists(os.path.join(d, 'webapp', 'results', 'ZZ')))

    print(f'\nrebuild_cases_from_csv selftest: {n[0]}/{n[1]} PASS')
    return 0 if n[0] == n[1] else 1


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--force', action='store_true', help='(예약 — 기존 파일은 어떤 경우에도 안 덮는다)')
    ap.add_argument('--refill', action='store_true',
                    help='이미 복원된 케이스에 **빠진 키만** 채운다 (실런·기존 값은 안 건드린다)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    cs = collect()
    if not cs:
        raise SystemExit('표를 못 읽었다 — 리포 루트에서 실행할 것')
    by = {}
    for c in cs.values():
        by[c['source']] = by.get(c['source'], 0) + 1
    print(f'복원 가능한 케이스 **{len(cs)}건**')
    for s, k in sorted(by.items(), key=lambda x: -x[1]):
        print(f'   {k:>4}건  ← {s}')
    fld = sorted(c['n_fields'] for c in cs.values())
    print(f'   케이스당 지표 중앙값 {fld[len(fld) // 2]}개 (최소 {fld[0]} · 최대 {fld[-1]})')
    print(f'   대상 데이터 루트: {_data_root()}')
    _mg = sum(1 for c in cs.values() if c.get('merged'))
    if _mg:
        print(f'   이름 조인으로 보충된 케이스 {_mg}건')
    print('\n── 결손 축 (다시 돌려야 하는 것) ──')
    for ax, miss in gap_report(cs).items():
        n = len(miss)
        mark = '⛔' if n == len(cs) else ('⚠' if n else '✅')
        ex = f'  예: {miss[0]}' if 0 < n <= len(cs) else ''
        print(f'   {mark} {ax:<22} 결손 {n:>4}/{len(cs)}{ex}')
    if a.refill:
        touched, added, kept_real, absent = refill(cs)
        print(f'\n✓ 보충한 케이스 {touched}건 · 채운 키 {added}개')
        print(f'  · 실런이라 손대지 않음 {kept_real}건 · 아직 복원 안 됨 {absent}건 (--write 소관)')
        if touched:
            print('  → 이어서:  python3 scripts/rebuild_tables_from_metrics.py --write')
        else:
            print('  (채울 것이 없었다 — 이미 최신이다)')
    elif a.write:
        made, skipped = write(cs)
        print(f'\n✓ 새로 만든 케이스 {made}건 · 이미 있어 건너뜀 {skipped}건')
        print('  ⚠ 전부 `status: reconstructed` 로 표시된다 — **재실행이 아니다**.')
        print('  ⛔ 그림·report·3D·원본 덤프는 없다 (원자료가 있어야 한다).')
        #  ★ 건너뛴 케이스는 **옛 복원 상태로 남는다** — 그 사실을 여기서 말한다.
        #    (안 말하면 "0건 새로 만듦 = 할 일 없음" 으로 읽힌다 = 오늘의 그 병)
        if skipped:
            print(f'  ⚠⚠ 건너뛴 {skipped}건은 **옛 복원 상태 그대로**다.  복원 코드가 그 뒤로')
            print('      좋아졌다면 빠진 열이 남아 있다 →  이 스크립트를 `--refill` 로 한 번 더:')
            print('        python3 scripts/rebuild_cases_from_csv.py --refill')
        print('  → `dem5002` 로 다시 띄워 목록을 확인할 것.')
    else:
        print('\n(--check 모드 — 쓰지 않았다.  실제로 쓰려면 --write)')
