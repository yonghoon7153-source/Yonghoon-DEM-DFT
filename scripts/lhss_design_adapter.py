#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lhss 보충 20 설계 CSV → 130 인계 스키마의 설계행 (1저자 10-12 Q4 = (가) lhss 별도 데이터셋 · v1.3 = 194 + 보충 20 준비).

    mkdir <빈 임시 폴더> && tar -xzf docs/data/lhs_supp_runs_20261006/lhss_harvest_20261011_r2.tgz -C <그 폴더>
    python3 -I scripts/lhss_design_adapter.py --design docs/data/lhs_supp_design_20261006.csv \\
        --union <그 폴더>/lhss_out_20261011/lhss20_union_r2.tsv --out docs/data/lhss_design_adapted_20261012.csv
    python3 scripts/lhss_design_adapter.py --selftest

왜 필요한가: lhsx 64 와 같다 (`scripts/lhsx_design_adapter.py` 머리말) — `lhs_design_dataset.build_handover` 는 설계행의 열을 그대로 싣는데
보충 설계 (`lhs_supp_design` · `id · pdd_SE · w_AM_P …`) 는 130 설계 (`case_id · am_pct · d_am_p_um …`) 와 이름 · 규약이 다르다.

★ 변환 = `lhsx_design_adapter.adapt_row` 를 **import 해 그대로 부른다** (사본 없음 — 질량분율 → am_pct · ps_frac · mono "P 열 = AM 자리" ·
  입자 수 왕복 · 템플릿 값 전부 그 함수의 정의).  보충 CSV 는 adapt_row 가 읽는 18 열 (`LHSX_FIELDS`) 을 **같은 이름 · 같은 뜻**으로 갖는다
  (`lhs_supp_design.generate` 가 `lhs_ext_design` 규약 — 질량분율 셋 · mono 의 P 열 · 4 자리 반지름 — 을 따른다) → 그 18 열만 골라 넘기고
  (보충 CSV 의 `block` = 배치 구분 supp · thick 은 넘기지 않는다 · adapt_row 가 block = kind 로 쓴다), 나온 `lhsx_*` 12 열은 **이름만** `lhss_*` 로 바꾼다.
★ 전제 = 삽입 높이 ×1 (`ins_scale` 1.0): adapt_row 의 입자 수 왕복은 `lhs_ext_design.n_spheres` 기본 삽입 부피 `V_INS` 로 세고, 생성기
  `lhs_supp_design.counts` 는 `V_INS × ins_scale` 로 센다 → 보충 침대에서만 같은 식이다 (selftest ③ — 20/20 상대차 < 1e-12 · CSV 정수와 |Δ| ≤ 0.5
  = 정수 반올림뿐: 생성기가 반지름을 4 자리로 반올림한 **뒤** 세므로 lhsx 의 반지름 반올림 폭이 쓰이지 않는다).  `ins_scale` ≠ 1 은 adapt_row 앞에서 거부.
  후막 짝 `lhst_*` 8 (ins_scale 3 · 4) = LHS 밖 (1저자 10-11 · 등록 §5 ④ 별도 보고) → 선택 = `block = supp` 이고 **정확히** lhss_001…lhss_020 이 아니면 거부.
★ 설계 CSV 는 sha256 고정 (`DESIGN_SHA256`) — 같은 바이트를 `check_all.sh` 가 `lhs_supp_design --verify --expect-sha256` 으로 재검증한다.  다르면 거부.
  · 압력 300 MPa · E_SE 1.35 GPa · 상자 50 µm = lhsx 와 같은 템플릿 상속 (`lhs_ext_materialize.render` 는 반지름 · 가중 · volfrac · seed · 이름만 치환 ·
    보충 침대의 `apply_ins_scale(…, 1.0)` = 바이트 그대로).  상자 50 은 union `lx_um` 로 20/20 확인한다.
  ⚠ 산출물 `docs/data/lhss_design_adapted_20261012.csv` 의 상자 확인에 쓴 union = **r2** (`docs/data/lhs_supp_runs_20261006/lhss_harvest_20261011_r2.tgz`
    안 `lhss_out_20261011/lhss20_union_r2.tsv`) — 정식 r3 union (`docs/data/lhss_union_1e09f661d/lhss20_union.tsv` · 194 와 같은 수확기 판 1e09f661d ·
    1저자 10-12 Q5) 은 아직 반입 전.  상자 크기는 수확기 판과 무관 (덱의 상자 · 덤프 머리) 이고 이 어댑터는 union 값을 **싣지 않는다** (확인만)
    → 산출물 바이트는 union 판과 무관하다.
  · 하중 규칙이 반반이다: `2mAh_fixed` 10 (AM-rich · 130 의 2 mAh 규칙 · 하중 2.0 = 설계 입력) · `volfrac_free` 10 (SE-rich · 64 확장처럼 volfrac 가
    설계 축 · 하중 = volfrac 에서 거꾸로 계산한 값).  ★ 본 열 `loading_mAh_cm2` (1저자 10-12 Q6 = (가) — 배포 lhss = lhs 와 같은 132 열):
    `2mAh_fixed` = 2.0 (설계 입력 · 값 = 생성기 `lhs_supp_design.volfrac_for_loading` 의 기본 하중) · `volfrac_free` = **빈칸** (하중은 설계 입력이
    아니다 — 역산값은 싣지 않는다 · lhsx 64 는 이 열이 없다).  130 설계 (AM 70–95 wt% · 전부 2.0) 와 같은 자리 (`rve_um` 바로 뒤).
    규칙 ↔ SE 비율은 생성기 경계 그대로 대조한다 (`2mAh_fixed` ⟺ `pdd_SE ≤ SE_SPLIT` (0.30) ⟺ am_pct ≥ `LOADING_AM_MIN_PCT` (70)) — 어긋나면 거부.
    역산값 · 규칙은 출처 열 `lhss_loading_rule` · `lhss_loading_mAh_cm2` 에 그대로 남는다 (인계표 · 배포 아님).
  · 130 전용 추정 열 9 (`OMITTED` — lhsx 의 10 중 하중을 뺀 것) 은 lhsx 와 같이 만들지 않는다 — 실측 열 (수확 · union) 이 그 자리를 대신한다.
  · 보충 전용 출처 열: `lhss_loading_rule` · `lhss_loading_mAh_cm2` · `lhss_ins_scale` (20/20 = 1.0) · `lhss_cap_adjust` (`volfrac` = 입자 수 상한 때문에
    volfrac 를 낮춘 행 · 2 건) · `lhss_gap_dist` (선택 순간의 최근접 거리 — 기존 194 점 + 먼저 고른 보충 점 · 정규화 3 축 · `lhs_supp_design.maximin`).
  ⚠ 이름은 lhsx 와 같아도 뜻이 다른 출처 열: `lhss_stratum` · `lhss_lhs_cell` = 빈칸 (보충 침대는 층화 LHS 가 아니라 maximin 선택) ·
    `lhss_rSE_lo_um` 0.5 = SE 지름 ≥ 1.0 µm 시뮬 가능 하한 (lhsx 의 "입자 수 상한 때문에 올린 하한" 이 아니다) · `lhss_rSE_truncated` 20/20 = 0.
  ⚠ `ps_label` 은 adapt_row 의 거친 표지 (10·ps 를 파이썬 round) — 보충 ps 는 0.05 격자라 bimodal 14 중 6 (ps 0.25 · 0.35 · 0.45 · 0.55 ×2 · 0.75)
    이 .5 경계에 놓여 표지가 겹친다 (0.35 · 0.45 → 4:6 · 0.55 · 0.6 → 6:4 · 0.75 · 0.8 → 8:2 · 0.25 → 2:8).  정확한 값은 `ps_frac`.
  · 셀 규약 = lhsx `write` (float = repr · NaN = 빈칸) — selftest ⑨ 가 공통 열 · 이름만 바뀐 열의 글자를 lhsx `write` 출력과 대조한다.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import inspect
import io
import os
import sys
import tarfile
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import lhsx_design_adapter as LX                              # noqa: E402  — adapt_row · COLS · OMITTED · TEMPLATE_FIXED · _f · write (정본)
import lhs_supp_design as SD                                  # noqa: E402  — counts (selftest ③ 대조 · 생성기 정본)

DESIGN = os.path.join(ROOT, 'docs', 'data', 'lhs_supp_design_20261006.csv')
DESIGN_SHA256 = '73d9a47f76f49989ddbd2c1237007c8499601d63bd5baf0e1ad11c527f21beb0'     # = check_all.sh 의 lhs_supp_design --verify --expect-sha256
OUT_COMMITTED = os.path.join(ROOT, 'docs', 'data', 'lhss_design_adapted_20261012.csv')
R2_TGZ = os.path.join(ROOT, 'docs', 'data', 'lhs_supp_runs_20261006', 'lhss_harvest_20261011_r2.tgz')
R2_MEMBER = 'lhss_out_20261011/lhss20_union_r2.tsv'
SUPP_IDS = tuple(f'lhss_{i:03d}' for i in range(1, 21))

AdapterRefusal = LX.AdapterRefusal                            # 거부는 한 종류 — adapt_row 의 거부도 같은 예외로 올라온다

#: adapt_row 가 읽는 열 — 보충 CSV 에 같은 이름 · 같은 뜻으로 있다.  그 밖의 열은 넘기지 않는다 (block · partner · 하중 · 코어 …).
LHSX_FIELDS = ('id', 'stratum', 'ntype', 'kind', 'pdd_SE', 'w_AM_P', 'w_AM_S', 'rP_um', 'rS_um', 'rSE_um',
               'rSE_lo_um', 'rSE_truncated', 'volfrac', 'phi_AM', 'n_AM_est', 'n_SE_est', 'lhs_cell', 'seed')
#: 보충 전용 출처 열의 원천 (보충 CSV 열 → lhss_ 열)
SUPP_FIELDS = ('loading_rule', 'loading_mAh_cm2', 'ins_scale', 'cap_adjust', 'gap_dist')
SUPP_ONLY = tuple('lhss_' + k for k in SUPP_FIELDS)

BASE_COLS = [c for c in LX.COLS if not c.startswith('lhsx_')]                       # 130 인계 스키마 22 열 — lhsx 와 같은 이름 · 순서
RENAME = {c: 'lhss_' + c[len('lhsx_'):] for c in LX.COLS if c.startswith('lhsx_')}  # 출처 12 열 — 이름만 바꾼다
#: ★ 본 하중 열 (1저자 10-12 Q6 = (가)) — 130 설계와 같은 자리 (rve_um 바로 뒤) · 2mAh_fixed = 2.0 · volfrac_free = 빈칸 (NaN → 빈 셀)
MAIN_LOADING = 'loading_mAh_cm2'
_I_RVE = BASE_COLS.index('rve_um') + 1
COLS = BASE_COLS[:_I_RVE] + [MAIN_LOADING] + BASE_COLS[_I_RVE:] + list(RENAME.values()) + list(SUPP_ONLY)
#: 2mAh_fixed 하중 = 생성기 정본 (`lhs_supp_design.volfrac_for_loading` 의 기본 하중 — 130 설계 상수 2.0 과 같다 · 사본 금지)
LOADING_FIXED = float(inspect.signature(SD.volfrac_for_loading).parameters['loading'].default)
#: 하중 규칙 경계 = 생성기 `SE_SPLIT` (pdd_SE > SE_SPLIT = volfrac_free) — am_pct (= 100·(1 − pdd_SE)) 로 70 · 배포 빈칸 규칙이 같은 경계를 쓴다
LOADING_AM_MIN_PCT = 100.0 * (1.0 - SD.SE_SPLIT)
LOADING_RULES = ('2mAh_fixed', 'volfrac_free')

OMITTED = {k: v for k, v in LX.OMITTED.items() if k != MAIN_LOADING}                 # 아홉 = lhsx 와 같은 사유 (130 추정 규약 열 · 만들지 않는다)


def _num(r: dict, key: str) -> float:
    try:
        return LX._f(r[key])
    except (TypeError, ValueError):
        raise AdapterRefusal(f'{r.get("id")}: {key} = {r.get(key)!r} 숫자 아님') from None


def read_design(path: str) -> list[dict]:
    """봉인된 보충 설계만 받는다 — 바이트 sha256 이 `DESIGN_SHA256` 과 다르면 거부 (우회 인자 없음)."""
    with open(path, 'rb') as fh:
        raw = fh.read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != DESIGN_SHA256:
        raise AdapterRefusal(f'설계 sha256 {sha[:12]}… ≠ 고정 {DESIGN_SHA256[:12]}… — 봉인된 보충 설계 (lhs_supp_design --verify) 가 아니다')
    return list(csv.DictReader(io.StringIO(raw.decode('utf-8'), newline='')))


def adapt_rows(rows: list[dict]) -> list[dict]:
    """설계 행 (보충 20 + 후막 8) → 보충 20 의 인계 설계행.  선택 = block 'supp' · 정확히 lhss_001…lhss_020."""
    ids = [r.get('id', '') for r in rows]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        raise AdapterRefusal(f'id 중복 {dup[:5]}')
    sel = [r for r in rows if r.get('block') == 'supp']
    thick = [r.get('id') for r in sel if str(r.get('id', '')).startswith('lhst_')]
    if thick:
        raise AdapterRefusal(f'선택 (block = supp) 에 후막 행 {thick[:5]} — 후막 짝 8 은 LHS 밖 (1저자 10-11 · 등록 §5 ④ 별도 보고)')
    stray = [(r.get('id'), r.get('block')) for r in rows
             if r.get('block') != 'supp' and not (r.get('block') == 'thick' and str(r.get('id', '')).startswith('lhst_'))]
    if stray:
        raise AdapterRefusal(f'보충도 후막도 아닌 행 (id ↔ block) {stray[:5]}')
    got = [str(r.get('id', '')) for r in sel]
    if sorted(got) != list(SUPP_IDS):
        raise AdapterRefusal(f'선택 집합 ≠ lhss_001…lhss_020 — 빠짐 {[i for i in SUPP_IDS if i not in got]} · '
                             f'밖 {[i for i in got if i not in SUPP_IDS]}')
    out = []
    for r in sel:
        miss = [k for k in LHSX_FIELDS + SUPP_FIELDS if k not in r]
        if miss:
            raise AdapterRefusal(f'{r["id"]}: 열 없음 {miss}')
        sc = _num(r, 'ins_scale')
        if not abs(sc - 1.0) <= 1e-12:
            raise AdapterRefusal(f'{r["id"]}: ins_scale {r["ins_scale"]!r} ≠ 1 — adapt_row 의 입자 수 왕복은 기본 삽입 부피 V_INS (높이 ×1) 로 센다')
        try:
            o = LX.adapt_row({k: r[k] for k in LHSX_FIELDS})
        except KeyError as e:
            raise AdapterRefusal(f'{r["id"]}: adapt_row 가 읽는 열 {e} 가 LHSX_FIELDS 에 없다 — lhsx 어댑터가 바뀌었다') from None
        if list(o) != LX.COLS:
            raise AdapterRefusal(f'{r["id"]}: adapt_row 출력 열 ≠ lhsx COLS — lhsx 어댑터가 바뀌었다')
        rule, load, pdd = r['loading_rule'], _num(r, 'loading_mAh_cm2'), _num(r, 'pdd_SE')
        if rule not in LOADING_RULES:
            raise AdapterRefusal(f'{r["id"]}: 하중 규칙 {rule!r} 을 모른다 (아는 것: {LOADING_RULES})')
        fixed = pdd <= SD.SE_SPLIT + 1e-9                                         # 생성기 lhs_supp_design 의 규칙 대조와 같은 식
        if (rule == '2mAh_fixed') != fixed or (o['am_pct'] >= LOADING_AM_MIN_PCT) != fixed:
            raise AdapterRefusal(f'{r["id"]}: 하중 규칙 {rule} ↔ pdd_SE {pdd} · am_pct {o["am_pct"]:.4g} 어긋남 — 생성기 경계 SE_SPLIT {SD.SE_SPLIT} '
                                 f'(2mAh_fixed ⟺ pdd_SE ≤ SE_SPLIT ⟺ am_pct ≥ {LOADING_AM_MIN_PCT:g})')
        if fixed and load != LOADING_FIXED:
            raise AdapterRefusal(f'{r["id"]}: 2mAh_fixed 인데 하중 {r["loading_mAh_cm2"]!r} ≠ {LOADING_FIXED} (130 의 2 mAh 규칙 · 생성기 기본 하중)')
        vals = {k: o[k] for k in BASE_COLS}
        vals.update({RENAME[k]: o[k] for k in RENAME})
        vals[MAIN_LOADING] = LOADING_FIXED if fixed else float('nan')            # Q6 (가) — volfrac_free = 빈칸 (역산값은 출처 열에만)
        vals.update(lhss_loading_rule=rule, lhss_loading_mAh_cm2=load, lhss_ins_scale=sc,
                    lhss_cap_adjust=r['cap_adjust'], lhss_gap_dist=_num(r, 'gap_dist'))
        out.append({k: vals[k] for k in COLS})
    return out


def union_from_text(text: str) -> dict:
    rows = list(csv.DictReader(io.StringIO(text, newline=''), delimiter='\t'))
    cases = [r.get('case', '') for r in rows]
    dup = sorted({c for c in cases if cases.count(c) > 1})
    if dup:
        raise AdapterRefusal(f'union case 중복 {dup[:5]}')
    return {r['case']: r for r in rows}


def read_union(path: str) -> dict:
    with open(path, encoding='utf-8', newline='') as fh:
        return union_from_text(fh.read())


def check_union(out_rows: list[dict], u: dict) -> None:
    """lhsx adapt 와 같은 확인 — 설계행마다 union 행이 있고 상자 (lx_um) = 템플릿 50 µm."""
    miss = [o['case_id'] for o in out_rows if o['case_id'] not in u]
    if miss:
        raise AdapterRefusal(f'union 에 없는 설계행 {miss[:5]}')
    bad = []
    for o in out_rows:
        try:
            lx = float(u[o['case_id']].get('lx_um'))
        except (TypeError, ValueError):
            lx = float('nan')
        if not abs(lx - LX.TEMPLATE_FIXED['rve_um']) <= 1e-9:
            bad.append((o['case_id'], u[o['case_id']].get('lx_um')))
    if bad:
        raise AdapterRefusal(f'상자 ≠ 50 µm: {bad[:5]} — 템플릿 상속 가정이 깨졌다')


def adapt(design_path: str, union_path: str | None = None) -> list[dict]:
    out = adapt_rows(read_design(design_path))
    if union_path:
        check_union(out, read_union(union_path))
    return out


def _cell(v):
    if isinstance(v, float):
        return '' if v != v else repr(v)                      # lhsx write 와 같은 셀 규약 (selftest ⑨ 가 대조)
    return v


def write(out_rows: list[dict], path: str) -> None:
    with open(path, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, COLS, lineterminator='\n')
        w.writeheader()
        for o in out_rows:
            w.writerow({k: _cell(v) for k, v in o.items()})


def _r2_union() -> dict:
    """커밋된 r2 수확 묶음에서 union 한 파일만 **메모리로** 읽는다 (디스크에 풀지 않는다 · 일반 파일만)."""
    with tarfile.open(R2_TGZ, 'r:gz') as tf:
        m = tf.getmember(R2_MEMBER)
        if not m.isfile():
            raise AdapterRefusal(f'{R2_MEMBER}: 일반 파일이 아니다')
        return union_from_text(tf.extractfile(m).read().decode('utf-8'))


def selftest() -> int:
    fails, n = [], [0]

    def chk(name, fn):
        n[0] += 1
        try:
            res = fn()
        except Exception as e:                                # noqa: BLE001 — 검사 하나의 예외 = 그 검사 실패 (나머지는 계속 돈다)
            res = (False, f'{type(e).__name__}: {e}')
        ok, extra = res if isinstance(res, tuple) else (res, '')
        print(f"  {'✓' if ok else '✗'} {name}" + (f'  ({extra})' if extra else ''))
        if not ok:
            fails.append(name)

    def refuses_with(fn, *keys):
        try:
            fn()
        except AdapterRefusal as e:
            m = str(e)
            return all(k in m for k in keys), m[:150]
        return False, '거부하지 않았다'

    try:
        base = read_design(DESIGN)
    except Exception as e:                                    # noqa: BLE001 — 스텁 · 해시 실패도 아래 검사들이 ✗ 로 보고한다
        print(f'  · 실물 설계 읽기 실패 ({type(e).__name__}: {e}) — 아래 실물 검사는 ✗')
        base = list(csv.DictReader(open(DESIGN, encoding='utf-8', newline='')))
    sel = [r for r in base if r.get('block') == 'supp']
    try:
        out = adapt_rows([dict(r) for r in base])
    except Exception as e:                                    # noqa: BLE001
        print(f'  · adapt_rows 실패 ({type(e).__name__}: {e})')
        out = []
    by_id = {o['case_id']: o for o in out}

    def mut(fn):
        rr = [dict(r) for r in base]
        fn(rr)
        return rr

    def _row(rr, rid):
        return next(r for r in rr if r['id'] == rid)

    #  ── 실물 (커밋된 보충 설계 · sha256 고정) ──
    chk('① 설계 sha256 = 고정값 · 28 행 (보충 20 + 후막 8) — read_design 통과',
        lambda: (len(read_design(DESIGN)) == 28, f'sha256 {DESIGN_SHA256[:12]}…'))
    chk('② 20 행 · id = lhss_001…lhss_020 (순서 그대로) · 후막 lhst_* 0',
        lambda: (tuple(o['case_id'] for o in out) == SUPP_IDS, f'{len(out)} 행'))

    def _rt():
        if len(out) != 20:
            return False, f'{len(out)} 행'
        worst = max(max(abs(by_id[r['id']]['n_am_p_est'] + by_id[r['id']]['n_am_s_est'] - int(r['n_AM_est'])),
                        abs(by_id[r['id']]['n_se_est'] - int(r['n_SE_est']))) for r in sel)
        return worst <= 0.5 + 1e-6, f'adapt_row 왕복 거부 0 · CSV 정수와 최대 |Δ| {worst:.3f}'
    chk('③a 입자 수 왕복 20/20 (adapt_row 의 허용 규칙) · |Δ| ≤ 0.5 = 정수 반올림뿐', _rt)

    def _gen():
        if len(out) != 20:
            return False, f'{len(out)} 행'
        worst = 0.0
        for r in sel:
            n_am, n_se, _phi = SD.counts(float(r['pdd_SE']), float(r['w_AM_P']), float(r['w_AM_S'] or 0), float(r['rP_um']),
                                         float(r['rS_um'] or 0), float(r['rSE_um']), int(r['ntype']), float(r['volfrac']),
                                         float(r['ins_scale']))
            o = by_id[r['id']]
            worst = max(worst, abs(n_am - (o['n_am_p_est'] + o['n_am_s_est'])) / n_am, abs(n_se - o['n_se_est']) / n_se)
        return worst < 1e-12, f'최대 상대차 {worst:.1e}'
    chk('③b 입자 수 = 생성기 lhs_supp_design.counts (V_INS × ins_scale 1) — adapt_row 를 쓸 전제', _gen)
    chk('④ 하중 규칙 2mAh_fixed 10 · volfrac_free 10 · 2mAh_fixed 의 lhss_loading_mAh_cm2 = 2.0 (설계 입력)',
        lambda: (sum(o['lhss_loading_rule'] == '2mAh_fixed' for o in out) == 10 and sum(o['lhss_loading_rule'] == 'volfrac_free' for o in out) == 10
                 and all(o['lhss_loading_mAh_cm2'] == 2.0 for o in out if o['lhss_loading_rule'] == '2mAh_fixed')))

    def _main_loading():
        if len(out) != 20:
            return False, f'{len(out)} 행'
        fixed = [o for o in out if o['lhss_loading_rule'] == '2mAh_fixed']
        free = [o for o in out if o['lhss_loading_rule'] == 'volfrac_free']
        ok = (len(fixed) == len(free) == 10 and all(o.get('loading_mAh_cm2') == 2.0 for o in fixed)
              and all(isinstance(o.get('loading_mAh_cm2'), float) and o['loading_mAh_cm2'] != o['loading_mAh_cm2'] for o in free)
              and all(o['am_pct'] >= LOADING_AM_MIN_PCT for o in fixed) and all(o['am_pct'] < LOADING_AM_MIN_PCT for o in free))
        return ok, (f'2.0 = {sorted(o["case_id"] for o in fixed)[:3]}… · 빈칸 (NaN) = {len(free)} · 경계 am_pct {LOADING_AM_MIN_PCT} '
                    f'(= 100·(1 − lhs_supp_design.SE_SPLIT))')
    chk('④b ★ Q6 (가) 본 열 loading_mAh_cm2 — 2mAh_fixed 10 = 2.0 (설계 입력) · volfrac_free 10 = 빈칸 (NaN · 하중은 설계 입력이 아님) · '
        '규칙 ↔ am_pct 경계 (생성기 SE_SPLIT) 그대로', _main_loading)
    chk('⑤ lhss_ins_scale 20/20 = 1.0', lambda: (len(out) == 20 and all(o['lhss_ins_scale'] == 1.0 for o in out)))
    chk('⑥ block bimodal 14 · mono_AM_S 4 · mono_AM_P 2 (block = kind)',
        lambda: ({b: sum(o['block'] == b for o in out) for b in ('bimodal', 'mono_AM_S', 'mono_AM_P')} == {'bimodal': 14, 'mono_AM_S': 4, 'mono_AM_P': 2}
                 and all(o['block'] == o['lhss_kind'] for o in out)))
    chk('⑥b lhss_cap_adjust = volfrac 2 건 (lhss_002 · lhss_004) · 나머지 빈칸',
        lambda: sorted(o['case_id'] for o in out if o['lhss_cap_adjust'] == 'volfrac') == ['lhss_002', 'lhss_004']
        and all(o['lhss_cap_adjust'] in ('', 'volfrac') for o in out))
    want12 = ['lhss_stratum', 'lhss_ntype', 'lhss_kind', 'lhss_pdd_SE', 'lhss_w_AM_P', 'lhss_w_AM_S', 'lhss_rSE_lo_um', 'lhss_rSE_truncated',
              'lhss_volfrac', 'lhss_phi_AM_solid', 'lhss_lhs_cell', 'lhss_seed']
    chk('⑦ 열 = lhsx 130 스키마 22 (case_id … rve_over_d_am_max) + 본 열 loading_mAh_cm2 (rve_um 바로 뒤 — 130 설계와 같은 자리 · Q6 (가)) + '
        'lhss_ 12 (이름만) + 보충 전용 5 = 40 · lhsx_ 0 · 행 열 = COLS · 넣지 않은 130 추정 열 = lhsx 의 열 중 loading 뺀 9',
        lambda: (len(BASE_COLS) == 22 and BASE_COLS[0] == 'case_id' and BASE_COLS[-1] == 'rve_over_d_am_max' and list(RENAME.values()) == want12
                 and list(SUPP_ONLY) == ['lhss_loading_rule', 'lhss_loading_mAh_cm2', 'lhss_ins_scale', 'lhss_cap_adjust', 'lhss_gap_dist']
                 and len(COLS) == 40 and not any(c.startswith('lhsx_') for c in COLS)
                 and COLS[COLS.index('rve_um') + 1] == 'loading_mAh_cm2' and COLS.count('loading_mAh_cm2') == 1
                 and [c for c in COLS if c != 'loading_mAh_cm2'] == BASE_COLS + want12 + list(SUPP_ONLY)
                 and 'loading_mAh_cm2' not in OMITTED and sorted(OMITTED) == sorted(k for k in LX.OMITTED if k != 'loading_mAh_cm2')
                 and len(out) == 20 and all(list(o) == COLS for o in out), f'{len(COLS)} 열'))

    def _same():
        if len(out) != 20:
            return False, f'{len(out)} 행'
        for r in sel:
            o, ref = by_id[r['id']], LX.adapt_row({k: r[k] for k in LHSX_FIELDS})
            same = lambda a, b: (a == b) or (isinstance(a, float) and isinstance(b, float) and a != a and b != b)   # noqa: E731
            if not (all(same(o[k], ref[k]) for k in BASE_COLS) and all(same(o[RENAME[k]], ref[k]) for k in RENAME)):
                return False, r['id']
        return True
    chk('⑧ 값 = adapt_row 그대로 (공통 22 · 이름만 바뀐 12)', _same)

    def _parity():
        if len(out) != 20:
            return False, f'{len(out)} 행'
        with tempfile.TemporaryDirectory() as td:
            pa, pb = os.path.join(td, 'lhss.csv'), os.path.join(td, 'lhsx.csv')
            write(out, pa)
            LX.write([LX.adapt_row({k: r[k] for k in LHSX_FIELDS}) for r in sel], pb)
            a = list(csv.DictReader(open(pa, encoding='utf-8', newline='')))
            b = list(csv.DictReader(open(pb, encoding='utf-8', newline='')))
        ok = len(a) == len(b) == 20 and all(x[k] == y[k] for x, y in zip(a, b) for k in BASE_COLS) \
            and all(x[RENAME[k]] == y[k] for x, y in zip(a, b) for k in RENAME)
        blanks = sum(x['d_am_p_um'] == '' for x in a) + sum(x['d_am_s_um'] == '' for x in a)
        return ok and blanks == 6, f'mono 빈칸 {blanks} (d_am_p 4 + d_am_s 2)'
    chk('⑨ 셀 규약 = lhsx write (공통 · 이름만 바뀐 열 글자 같음 · NaN = 빈칸)', _parity)

    def _union_ok():
        u = _r2_union()
        check_union(out, u)
        return (len(out) == 20 and all(float(u[o['case_id']]['lx_um']) == 50.0 for o in out)), f'r2 union {len(u)} 행'
    chk('⑩ 커밋된 r2 union (tgz · 메모리에서 읽음) 상자 50 µm 20/20 — check_union 통과', _union_ok)

    def _repro():
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, 'a.csv')
            write(adapt(DESIGN), p)
            mine = open(p, 'rb').read()
        theirs = open(OUT_COMMITTED, 'rb').read()
        hdr = theirs.decode('utf-8').split('\n', 1)[0].split(',')
        return mine == theirs and hdr == COLS and theirs.count(b'\n') == 21, f'sha256 {hashlib.sha256(theirs).hexdigest()[:12]}…'
    chk('⑪ 커밋된 산출물 = 재생성 바이트 그대로 (머리 = COLS · 20 행)', _repro)

    #  ── 거부 (반례) ──
    def _bad_sha():
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, 'd.csv')
            raw = open(DESIGN, 'rb').read()
            open(p, 'wb').write(raw.replace(b'lhss_001,supp', b'lhss_001,supp ', 1))
            return refuses_with(lambda: read_design(p), 'sha256')
    chk('★⑫ 설계 sha256 다름 거부 (한 바이트 바꾼 사본)', _bad_sha)
    chk('★⑬ 후막 lhst_* 가 선택에 (block = supp 로 바꿈) 거부',
        lambda: refuses_with(lambda: adapt_rows(mut(lambda rr: _row(rr, 'lhst_045_6m').update(block='supp'))), 'lhst_045_6m', '후막'))
    chk('★⑭ lhss 행 하나 빠짐 (19) 거부',
        lambda: refuses_with(lambda: adapt_rows(mut(lambda rr: rr.remove(_row(rr, 'lhss_007')))), 'lhss_007', '빠짐'))
    chk('★⑮ id 중복 거부',
        lambda: refuses_with(lambda: adapt_rows(mut(lambda rr: rr.append(dict(_row(rr, 'lhss_005'))))), 'lhss_005', '중복'))
    chk('★⑯ lhss 행 ins_scale ≠ 1 거부 (adapt_row 앞 관문)',
        lambda: refuses_with(lambda: adapt_rows(mut(lambda rr: _row(rr, 'lhss_003').update(ins_scale='3.0'))), 'lhss_003', 'ins_scale'))
    chk('★⑰ 질량분율 합 ≠ 1 거부 (adapt_row 상속)',
        lambda: refuses_with(lambda: adapt_rows(mut(lambda rr: _row(rr, 'lhss_004').update(w_AM_S='0.2'))), 'lhss_004', '질량분율'))
    chk('★⑱ 입자 수 +1 % 거부 (adapt_row 왕복 · 실제 보충 행 lhss_006)',
        lambda: refuses_with(lambda: adapt_rows(mut(lambda rr: _row(rr, 'lhss_006').update(n_AM_est=str(round(int(_row(rr, 'lhss_006')['n_AM_est']) * 1.01))))),
                             'lhss_006', '입자 수'))
    chk('★⑲ adapt_row 가 읽는 열이 없으면 거부 (phi_AM 뺌)',
        lambda: refuses_with(lambda: adapt_rows(mut(lambda rr: _row(rr, 'lhss_001').pop('phi_AM'))), 'lhss_001', 'phi_AM'))

    def _union_bad():
        if len(out) != 20:
            return False, f'{len(out)} 행'
        head = 'case\tlx_um\n'
        t49 = head + ''.join(f'{o["case_id"]}\t{"49.0" if i == 3 else "50.0"}\n' for i, o in enumerate(out))
        t19 = head + ''.join(f'{o["case_id"]}\t50.0\n' for o in out[1:])
        tdu = head + ''.join(f'{o["case_id"]}\t50.0\n' for o in out) + f'{out[0]["case_id"]}\t50.0\n'
        a = refuses_with(lambda: check_union(out, union_from_text(t49)), '상자', out[3]['case_id'])
        b = refuses_with(lambda: check_union(out, union_from_text(t19)), 'union 에 없는', out[0]['case_id'])
        c = refuses_with(lambda: union_from_text(tdu), '중복')
        return a[0] and b[0] and c[0], ' · '.join(x[1][:50] for x in (a, b, c))
    chk('★⑳ union 상자 ≠ 50 µm 거부 · union 에 없는 행 거부 · union case 중복 거부', _union_bad)

    def _drift():
        global LHSX_FIELDS
        saved_fields, saved_adapt = LHSX_FIELDS, LX.adapt_row
        try:
            LHSX_FIELDS = tuple(k for k in saved_fields if k != 'seed')       # adapt_row 는 seed 를 읽는다 → KeyError
            a = refuses_with(lambda: adapt_rows([dict(r) for r in base]), 'LHSX_FIELDS', 'seed')
        finally:
            LHSX_FIELDS = saved_fields
        try:
            LX.adapt_row = lambda r: dict(saved_adapt(r), lhsx_extra=1)      # 출력 열이 늘어난 lhsx 어댑터
            b = refuses_with(lambda: adapt_rows([dict(r) for r in base]), 'lhsx COLS')
        finally:
            LX.adapt_row = saved_adapt
        return a[0] and b[0], a[1][:70] + ' · ' + b[1][:70]
    chk('★㉑ lhsx 어댑터 표류 거부 — adapt_row 가 넘기지 않은 열을 읽음 (KeyError) · 출력 열 ≠ lhsx COLS', _drift)
    chk('★㉒ 하중 규칙 ↔ SE 비율 어긋남 거부 — volfrac_free 행 (lhss_001 · pdd_SE 0.7) 을 2mAh_fixed 로 바꿈',
        lambda: refuses_with(lambda: adapt_rows(mut(lambda rr: _row(rr, 'lhss_001').update(loading_rule='2mAh_fixed', loading_mAh_cm2='2.0'))),
                             'lhss_001', 'SE_SPLIT'))
    chk('★㉓ 하중 규칙 ↔ SE 비율 어긋남 거부 — 2mAh_fixed 행 (lhss_005 · AM 92.5) 을 volfrac_free 로 바꿈',
        lambda: refuses_with(lambda: adapt_rows(mut(lambda rr: _row(rr, 'lhss_005').update(loading_rule='volfrac_free'))), 'lhss_005', 'SE_SPLIT'))
    chk('★㉔ 2mAh_fixed 행의 하중 ≠ 2.0 거부 (lhss_006 → 2.5) · 모르는 하중 규칙 거부 (lhss_007 → fixed)',
        lambda: tuple(x and y for x, y in zip(
            refuses_with(lambda: adapt_rows(mut(lambda rr: _row(rr, 'lhss_006').update(loading_mAh_cm2='2.5'))), 'lhss_006', '2.0'),
            refuses_with(lambda: adapt_rows(mut(lambda rr: _row(rr, 'lhss_007').update(loading_rule='fixed'))), 'lhss_007', '하중 규칙'))))

    print(f'lhss_design_adapter selftest: {n[0] - len(fails)}/{n[0]}' + (' 전부 통과' if not fails else f'  ✗ {len(fails)} 건'))
    return 0 if not fails else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--design', default=DESIGN, help='보충 설계 CSV (sha256 고정 — 다르면 거부)')
    ap.add_argument('--union', default='', help='상자 50 µm 확인용 union TSV (case · lx_um) · 빈 값이면 생략 · '
                                               '정식 r3 = docs/data/lhss_union_1e09f661d/lhss20_union.tsv (아직 없음)')
    ap.add_argument('--out', default='', help='산출 CSV (빈 값이면 검사만)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    try:
        rows = adapt(a.design, a.union or None)
    except AdapterRefusal as e:
        print(f'⛔ {e}')
        return 1
    print(f'상자 확인: {a.union} → 50 µm {len(rows)}/{len(rows)}' if a.union else '상자 확인 생략 (--union 없음)')
    if a.out:
        write(rows, a.out)
        print(f'→ {a.out}  {len(rows)} 행 × {len(COLS)} 열  (넣지 않은 130 추정 열 {len(OMITTED)}: {", ".join(OMITTED)})')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
