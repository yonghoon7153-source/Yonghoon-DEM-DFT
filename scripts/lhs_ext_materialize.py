#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""봉인된 확장 설계 CSV → ibb LIGGGHTS 덱, 그리고 **왕복검사** (Codex R14 조건 8·9).

    python3 scripts/lhs_ext_materialize.py \\
        --design docs/data/lhs_ext_design_v2_20260829.csv \\
        --expect-sha256 bc72b8bf… \\
        --template-3t ~/dem_test/lhs/lhs00_000/input_lhs00_000.liggghts \\
        --template-2t ~/dem_test/lhs/lhs00_110/input_lhs00_110.liggghts \\
        --outdir /tmp/lhsx_decks
    python3 scripts/lhs_ext_materialize.py --selftest

계기: R14 P1-06 — *"대상 묶음에는 CSV 를 실제 ibb 입력 덱으로 변환하는 소비자나 왕복검사가
없다.  열 이름대로 읽으면 상이 뒤집힌다."*  실제로 ibb 에도 생성기가 남아 있지 않아
(`~/dem_test` 에 `.py` 가 0개), 130 덱은 **산출물만** 있는 상태였다.

★ 템플릿은 **실물 덱 두 개**다 — 형식을 여기에 다시 적지 않는다.  실제로 돌아서 결과가
  나온 파일이 정답지이고, 손으로 옮겨 적는 순간 갈라진다.  치환은 **외과적**이고,
  기대한 자리를 정확히 한 번 못 맞히면 **거부**한다 (조용히 반쯤 바뀐 덱이 최악이다).

★★ 상(phase) 사상 — 실물 덱에서 읽은 규약 (2026-08-30):
    3-type: pts1 = AM_P (density 4800, `${r_AM_P}`)
            pts2 = AM_S (density 4800, `${r_AM_S}`)
            pts3 = SE   (density 2000, `${r_SE}`)
            가중 = `w_AM_P  w_AM_S  pdd_SE`
    2-type: pts1 = AM   (density 4800, `${r_AM}`)
            pts2 = SE   (density 2000, `${r_SE}`)
            가중 = `w_AM_P  pdd_SE`
  ⇒ **덱에는 AM_P / AM_S 구분이 없다.**  `mono_AM_P` / `mono_AM_S` 는 오직 반지름 크기가
    정하는 라벨이고, CSV 가 mono 를 `w_AM_P` · `rP_um` 열에 담는 것은 *"P 열 = 일반 AM
    자리"* 규약이 맞다.  R14 가 물은 것이 이것이고, 왕복검사가 이 규약을 못박는다.

⚠ 길이 단위: **덱 값 × 1000 = µm** (상자 0.05 = 50 µm).  `0.0055` ↔ `5.5 µm`.
⚠ `particledistribution/discrete` 는 **plain** = 질량분율이다 (`/numberbased` 아님).
   밀도 4800 / 2000 과 함께 읽어야 부피분율이 나온다.

⚠⚠ 새 배치의 ID 는 `lhsx_NNN` 이라 `lhs_ext_design.parse_headers` 의 정규식
   (`lhs\\d+_\\d+`) 에 **일부러 안 걸린다**.  그 좁음이 사고가 아니라 **보호막**이다 —
   나중에 `--scan` 을 돌려도 새 64덱이 상자 유도에 섞이지 않는다 (상자는 기존 130 이어야
   한다).  그래서 이 파일은 **자기 파서**를 갖는다.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import sys

UM_PER_DECK_UNIT = 1000.0          # 덱 값 × 1000 = µm

# ── 왕복 파서 — 덱 **본문**(주석이 아니라 실제 명령)에서 읽는다 ─────────────
_RE_VAR = re.compile(r'^\s*variable\s+(\S+)\s+equal\s+(\S+)', re.M)
_RE_PTS = re.compile(
    r'^\s*fix\s+(\S+)\s+all\s+particletemplate/sphere\s+(\d+)\s+atom_type\s+(\d+)\s+'
    r'density\s+constant\s+([\d.eE+-]+)\s+radius\s+constant\s+\$\{(\w+)\}', re.M)
_RE_PDD = re.compile(
    r'^\s*fix\s+\S+\s+all\s+particledistribution/discrete\s+(\d+)\s+(\d+)\s+(.+)$', re.M)
_RE_INS = re.compile(r'insert/pack\s+seed\s+(\d+)')
_RE_VF = re.compile(r'volumefraction_region\s+([\d.eE+-]+)')
_RE_CASE = re.compile(r'^#\s*(\S+):\s*(\S+)', re.M)


def parse_deck(text: str) -> dict:
    """덱 본문에서 설계량을 되읽는다.  **헤더 주석을 믿지 않는다.**

    헤더는 사람이 읽는 라벨이라 본문과 갈릴 수 있다 — 갈리는지 보는 것이 왕복검사의
    목적이므로, 본문에서 읽고 헤더는 따로 읽어 **대조**한다.
    """
    var = {m.group(1): m.group(2) for m in _RE_VAR.finditer(text)}
    pts = [dict(fix=m.group(1), seed=int(m.group(2)), atom_type=int(m.group(3)),
                density=float(m.group(4)), rvar=m.group(5))
           for m in _RE_PTS.finditer(text)]
    mp = _RE_PDD.search(text)
    if not mp:
        raise ValueError('particledistribution/discrete 줄을 못 읽었다')
    n_decl = int(mp.group(2))
    toks = mp.group(3).split()
    weights = {}
    for i in range(0, len(toks) - 1, 2):
        weights[toks[i]] = float(toks[i + 1])
    mi, mv = _RE_INS.search(text), _RE_VF.search(text)
    if not (mi and mv):
        raise ValueError('insert/pack seed 또는 volumefraction_region 을 못 읽었다')
    mc = _RE_CASE.search(text)

    out = dict(ntype=len(pts), n_declared=n_decl, seed=int(mi.group(1)),
               volfrac=float(mv.group(1)), weights=weights,
               header_case=mc.group(1) if mc else None,
               header_kind=mc.group(2) if mc else None)
    if len(pts) != n_decl:
        raise ValueError(f'템플릿 {len(pts)}개인데 분포는 {n_decl}개라고 적혀 있다')
    #  상별 반지름·밀도 — **본문의 density 로** AM/SE 를 가른다 (이름이 아니라)
    for p in pts:
        v = var.get(p['rvar'])
        if v is None:
            raise ValueError(f'변수 {p["rvar"]} 정의가 없다')
        p['r_um'] = float(v) * UM_PER_DECK_UNIT
        p['weight'] = weights.get(p['fix'])
        if p['weight'] is None:
            raise ValueError(f'{p["fix"]} 의 가중이 분포에 없다')
    out['pts'] = pts
    am = [p for p in pts if p['density'] > 3000]
    se = [p for p in pts if p['density'] <= 3000]
    if len(se) != 1:
        raise ValueError(f'SE 템플릿이 {len(se)}개다 (1개여야 한다)')
    out['r_SE_um'] = se[0]['r_um']
    out['pdd_SE'] = se[0]['weight']
    am.sort(key=lambda p: -p['r_um'])            # 큰 쪽이 AM_P
    out['r_AM_um'] = [p['r_um'] for p in am]
    out['w_AM'] = [p['weight'] for p in am]
    return out


def _sub1(text: str, pat: str, repl: str, what: str, count: int = 1) -> str:
    """정확히 `count` 번 치환한다.  아니면 거부 — 반쯤 바뀐 덱이 가장 나쁘다.

    **구조적인 자리**에 쓴다 (변수 정의 · 분포 줄 · insert/pack) — 거기서 개수가 어긋나면
    템플릿 형식이 바뀐 것이고, 그때는 덱을 내지 않는 것이 맞다.
    """
    new, n = re.subn(pat, repl, text, flags=re.M)
    if n != count:
        raise SystemExit(f'⛔ 치환 실패: {what} — {count}번 기대했는데 {n}번 맞았다.  '
                         '템플릿 형식이 바뀌었을 수 있다 (덱을 내지 않는다)')
    return new


def _sub_all(text: str, pat: str, repl: str, what: str) -> str:
    """같은 설계값을 담은 **모든** 자리를 바꾼다.  하나도 못 맞히면 거부.

    ★ 왜 나누는가 (2026-08-30 실사고): 실물 덱은 `seed=` 를 **두 번** 적는다 — 헤더
      주석과 `print "…(case, kind, seed=N)…"` 줄.  둘 다 같은 런 seed 이므로 **둘 다**
      바꾸는 것이 맞는데, 내 축소 픽스처에는 `print` 줄이 없어 `_sub1` 로 짰고 실물에서
      바로 거부됐다.  *"템플릿은 실물이 정답지"* 라고 적어 놓고 픽스처를 실물과 다르게
      만든 것이 원인이다 — 그래서 아래 selftest 픽스처에 그 줄을 넣었다.
    ⇒ 여기서 지키는 불변식은 "정확히 1번" 이 아니라 **"남는 자리가 없다"** 이다.
      개수는 `--verbose` 로 볼 수 있고, 0 이면 여전히 거부한다.
    """
    new, n = re.subn(pat, repl, text, flags=re.M)
    if n == 0:
        raise SystemExit(f'⛔ 치환 실패: {what} — 한 자리도 못 맞혔다.  '
                         '템플릿 형식이 바뀌었을 수 있다 (덱을 내지 않는다)')
    return new


def render(template: str, row: dict, tmpl_case: str) -> str:
    """템플릿 덱의 값만 갈아끼운다.  구조는 건드리지 않는다."""
    nt = int(row['ntype'])
    case = row['id']
    rP = float(row['rP_um']) / UM_PER_DECK_UNIT
    rSE = float(row['rSE_um']) / UM_PER_DECK_UNIT
    wP, wSE = float(row['w_AM_P']), float(row['pdd_SE'])
    t = template

    if nt == 3:
        rS = float(row['rS_um']) / UM_PER_DECK_UNIT
        wS = float(row['w_AM_S'])
        t = _sub1(t, r'^(variable\s+r_AM_P\s+equal\s+)\S+', rf'\g<1>{rP:.6g}', 'r_AM_P')
        t = _sub1(t, r'^(variable\s+r_AM_S\s+equal\s+)\S+', rf'\g<1>{rS:.6g}', 'r_AM_S')
        t = _sub1(t, r'(particledistribution/discrete\s+\d+\s+3\s+pts1\s+)[\d.]+(\s+pts2\s+)'
                     r'[\d.]+(\s+pts3\s+)[\d.]+',
                  rf'\g<1>{wP:.6f}\g<2>{wS:.6f}\g<3>{wSE:.6f}', 'pdd 가중(3)')
        t = _sub_all(t, r'rP=[\d.eE+-]+', f'rP={rP:.6g}', '헤더 rP')
        t = _sub_all(t, r'rS=[\d.eE+-]+', f'rS={rS:.6g}', '헤더 rS')
        t = _sub_all(t, r'AM_P=[\d.]+(\s+)AM_S=[\d.]+(\s+)SE=[\d.]+',
                  rf'AM_P={wP:.4f}\g<1>AM_S={wS:.4f}\g<2>SE={wSE:.4f}', '헤더 pdd(3)')
    else:
        t = _sub1(t, r'^(variable\s+r_AM\s+equal\s+)\S+', rf'\g<1>{rP:.6g}', 'r_AM')
        t = _sub1(t, r'(particledistribution/discrete\s+\d+\s+2\s+pts1\s+)[\d.]+'
                     r'(\s+pts2\s+)[\d.]+',
                  rf'\g<1>{wP:.6f}\g<2>{wSE:.6f}', 'pdd 가중(2)')
        t = _sub_all(t, r'rAM=[\d.eE+-]+', f'rAM={rP:.6g}', '헤더 rAM')
        t = _sub_all(t, r'pdd AM=[\d.]+(\s+)SE=[\d.]+',
                  rf'pdd AM={wP:.4f}\g<1>SE={wSE:.4f}', '헤더 pdd(2)')

    t = _sub1(t, r'^(variable\s+r_SE\s+equal\s+)\S+', rf'\g<1>{rSE:.6g}', 'r_SE')
    t = _sub_all(t, r'rSE=[\d.eE+-]+', f'rSE={rSE:.6g}', '헤더 rSE')
    t = _sub_all(t, r'volfrac=[\d.eE+-]+', f'volfrac={float(row["volfrac"]):.6f}', '헤더 volfrac')
    t = _sub1(t, r'volumefraction_region\s+[\d.eE+-]+',
              f'volumefraction_region {float(row["volfrac"]):.6f}', 'volumefraction_region')
    t = _sub1(t, r'insert/pack\s+seed\s+\d+', f'insert/pack seed {int(row["seed"])}',
              'insert/pack seed')
    t = _sub_all(t, r'seed=\d+', f'seed={int(row["seed"])}', '헤더 seed')
    #  라벨과 케이스명 — 남은 템플릿 케이스명은 dump/restart/post 경로까지 전부 바꾼다
    t = _sub1(t, rf'^(#\s*){re.escape(tmpl_case)}(:\s*)\S+',
              rf'\g<1>{case}\g<2>{row["kind"]}', '헤더 케이스·kind')
    t = t.replace(tmpl_case, case)
    if tmpl_case in t:                                     # pragma: no cover
        raise SystemExit('⛔ 템플릿 케이스명이 남았다')
    return t


def roundtrip(row: dict, deck_text: str) -> list[str]:
    """생성한 덱을 **다시 읽어** CSV 와 1:1 대조한다.  → 불일치 목록."""
    bad = []
    #  파싱 자체가 거부되는 것도 **불일치의 한 형태**다.  예외로 터뜨리면 덱 하나가
    #  64건 전체를 죽이고, 어느 덱이 왜 나빴는지도 안 남는다.
    try:
        d = parse_deck(deck_text)
    except Exception as e:                                 # noqa: BLE001
        return [f'{row["id"]} 덱을 되읽지 못했다 ({type(e).__name__}: {e})']
    nt = int(row['ntype'])

    def near(a, b, tol=1e-4, what=''):
        if abs(float(a) - float(b)) > tol:
            bad.append(f'{row["id"]} {what}: 덱 {a} vs CSV {b}')

    if d['ntype'] != nt:
        bad.append(f'{row["id"]} ntype: 덱 {d["ntype"]} vs CSV {nt}')
        return bad
    if d['header_case'] != row['id']:
        bad.append(f'{row["id"]} 헤더 케이스: {d["header_case"]}')
    if d['header_kind'] != row['kind']:
        bad.append(f'{row["id"]} 헤더 kind: {d["header_kind"]} vs {row["kind"]}')
    if d['seed'] != int(row['seed']):
        bad.append(f'{row["id"]} seed: 덱 {d["seed"]} vs CSV {row["seed"]}')
    near(d['volfrac'], row['volfrac'], 1e-6, 'volfrac')
    near(d['pdd_SE'], row['pdd_SE'], 1e-4, 'pdd_SE')
    near(d['r_SE_um'], row['rSE_um'], 1e-6, 'rSE_um')
    #  ★ 상 사상 — 덱은 **밀도**로 AM/SE 를 가른다.  CSV 의 열 이름이 아니라.
    near(d['r_AM_um'][0], row['rP_um'], 1e-6, 'rP_um(=큰 AM)')
    near(d['w_AM'][0], row['w_AM_P'], 1e-4, 'w_AM_P(=큰 AM 가중)')
    if nt == 3:
        near(d['r_AM_um'][1], row['rS_um'], 1e-6, 'rS_um')
        near(d['w_AM'][1], row['w_AM_S'], 1e-4, 'w_AM_S')
    else:
        if len(d['r_AM_um']) != 1:
            bad.append(f'{row["id"]}: 2-type 인데 AM 템플릿이 {len(d["r_AM_um"])}개')
        if abs(float(row['w_AM_S'])) > 1e-9:
            bad.append(f'{row["id"]}: 2-type 인데 CSV w_AM_S={row["w_AM_S"]} ≠ 0')
    #  질량분율 합 = 1 (덱 자신의 가중으로)
    s = sum(d['weights'].values())
    if abs(s - 1.0) > 1e-6:
        bad.append(f'{row["id"]} 가중 합 {s:.8f} ≠ 1')
    #  밀도 규약
    for p in d['pts']:
        if p['density'] not in (2000.0, 4800.0):
            bad.append(f'{row["id"]} {p["fix"]} density {p["density"]} 이 4800/2000 밖')
    return bad


def load_design(path: str, expect_sha: str | None):
    raw = open(path, 'rb').read()
    sha = hashlib.sha256(raw).hexdigest()
    if expect_sha and sha != expect_sha.strip().lower():
        raise SystemExit(f'⛔ 설계 CSV sha256 불일치 — 기대 {expect_sha[:12]}… '
                         f'실제 {sha[:12]}…  (봉인된 설계가 아니다)')
    import io
    return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig')))), sha


def _tmpl_case(text: str) -> str:
    m = _RE_CASE.search(text)
    if not m:
        raise SystemExit('⛔ 템플릿에서 케이스명을 못 읽었다 (첫 `# <case>: <kind>` 줄)')
    return m.group(1)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--design')
    ap.add_argument('--expect-sha256')
    ap.add_argument('--template-3t', help='bimodal 템플릿 덱 (실물)')
    ap.add_argument('--template-2t', help='mono 템플릿 덱 (실물)')
    ap.add_argument('--outdir', help='덱을 쓸 디렉터리 (없으면 dry-run: 검사만)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    for need in ('design', 'template_3t', 'template_2t'):
        if not getattr(a, need):
            ap.error(f'--{need.replace("_", "-")} 가 필요하다')

    rows, sha = load_design(a.design, a.expect_sha256)
    t3 = open(a.template_3t, encoding='utf-8').read()
    t2 = open(a.template_2t, encoding='utf-8').read()
    c3, c2 = _tmpl_case(t3), _tmpl_case(t2)
    print(f'설계 {len(rows)}행 · sha256 {sha[:12]}…')
    print(f'템플릿 3-type {c3} · 2-type {c2}')

    bad, made = [], 0
    for r in rows:
        nt = int(r['ntype'])
        text = render(t3 if nt == 3 else t2, r, c3 if nt == 3 else c2)
        bad += roundtrip(r, text)
        if a.outdir:
            d = os.path.join(a.outdir, r['id'])
            os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, f'input_{r["id"]}.liggghts'), 'w',
                      encoding='utf-8', newline='\n') as fh:
                fh.write(text)
            made += 1
    print(f'\n왕복검사 {len(rows)}건 — 불일치 {len(bad)}건')
    for b in bad[:12]:
        print('  ⛔', b)
    if a.outdir:
        print(f'{"wrote" if made else "—"} {made} decks → {a.outdir}')
    else:
        print('(dry-run — --outdir 를 주면 덱을 쓴다)')
    return 1 if bad else 0


def _selftest():
    ok, fail = 0, []

    def chk(name, cond, extra=''):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(f'{name} {extra}')

    #  실물 덱에서 읽은 형식을 그대로 축소한 픽스처 (구조가 정답지다)
    T2 = """# ============================================================
# lhs00_110: mono_AM_S (2-type) | LHS design
# rAM=0.001 rSE=0.001 | pdd AM=0.8000 SE=0.2000
# volfrac=0.250627 | E_se=0.135e7 (고정) | seed=11059
# ============================================================
variable r_AM   equal 0.001
variable r_SE    equal 0.001
fix pts1 all particletemplate/sphere 15485863 atom_type 1 density constant 4800 radius constant ${r_AM}
fix pts2 all particletemplate/sphere 32452843 atom_type 2 density constant 2000 radius constant ${r_SE}
fix pdd_mix all particledistribution/discrete 49979687 2 pts1 0.800000 pts2 0.200000
print "====== INSERTING (lhs00_110, mono_AM_S, seed=11059) ======"
fix ins_mix all insert/pack seed 11059 distributiontemplate pdd_mix &
    volumefraction_region 0.250627
shell mkdir post_lhs00_110
"""
    T3 = """# ============================================================
# lhs00_000: bimodal (3-type) | LHS design
# rP=0.0055 rS=0.0005 rSE=0.001 | pdd AM_P=0.5100 AM_S=0.3400 SE=0.1500
# volfrac=0.222984 | E_se=0.135e7 (고정) | seed=10007
# ============================================================
variable r_AM_P  equal 0.0055
variable r_AM_S  equal 0.0005
variable r_SE    equal 0.001
fix pts1 all particletemplate/sphere 15485863 atom_type 1 density constant 4800 radius constant ${r_AM_P}
fix pts2 all particletemplate/sphere 15485867 atom_type 2 density constant 4800 radius constant ${r_AM_S}
fix pts3 all particletemplate/sphere 32452843 atom_type 3 density constant 2000 radius constant ${r_SE}
fix pdd_mix all particledistribution/discrete 49979687 3 pts1 0.510000 pts2 0.340000 pts3 0.150000
print "====== INSERTING (lhs00_000, bimodal, seed=10007) ======"
fix ins_mix all insert/pack seed 10007 distributiontemplate pdd_mix &
    volumefraction_region 0.222984
shell mkdir post_lhs00_000
"""
    #  ① 템플릿 자신을 되읽는다 — 파서가 실물 형식을 실제로 이해하는가
    d2 = parse_deck(T2)
    chk('① 2-type: ntype 2', d2['ntype'] == 2, str(d2['ntype']))
    chk('① 2-type: SE 반지름 1.0 µm', abs(d2['r_SE_um'] - 1.0) < 1e-9, str(d2['r_SE_um']))
    chk('① 2-type: pdd_SE 0.2', abs(d2['pdd_SE'] - 0.2) < 1e-9)
    chk('① 2-type: AM 하나', len(d2['r_AM_um']) == 1)
    chk('① 2-type: seed 11059', d2['seed'] == 11059)
    d3 = parse_deck(T3)
    chk('① 3-type: AM 둘, 큰 쪽이 먼저',
        d3['r_AM_um'] == [5.5, 0.5], str(d3['r_AM_um']))
    chk('① 3-type: 가중 [0.51, 0.34] · SE 0.15',
        d3['w_AM'] == [0.51, 0.34] and abs(d3['pdd_SE'] - 0.15) < 1e-9)
    chk('★① 상은 **밀도**로 가른다 (이름이 아니라)',
        all(p['density'] == 4800.0 for p in d3['pts'][:2])
        and d3['pts'][2]['density'] == 2000.0)

    #  ② 렌더 → 왕복.  3-type / 2-type 각각
    r3 = dict(id='lhsx_001', kind='bimodal', ntype='3', rP_um='6.0', rS_um='0.8',
              rSE_um='0.9', w_AM_P='0.40', w_AM_S='0.20', pdd_SE='0.40',
              volfrac='0.2100', seed='20011')
    out3 = render(T3, r3, 'lhs00_000')
    chk('② 3-type 왕복 일치', roundtrip(r3, out3) == [], str(roundtrip(r3, out3)[:2]))
    chk('② 템플릿 케이스명이 안 남는다', 'lhs00_000' not in out3)
    chk('② post_ 경로도 바뀐다', 'post_lhsx_001' in out3)
    chk('★② `print INSERTING` 줄의 seed 도 갱신된다 (실물은 seed= 를 두 번 적는다)',
        'seed=20011' in out3 and 'seed=10007' not in out3,
        [l for l in out3.split(chr(10)) if 'INSERTING' in l][:1])
    r2 = dict(id='lhsx_002', kind='mono_AM_S', ntype='2', rP_um='2.3', rS_um='',
              rSE_um='0.7', w_AM_P='0.65', w_AM_S='0', pdd_SE='0.35',
              volfrac='0.2400', seed='20021')
    out2 = render(T2, r2, 'lhs00_110')
    chk('② 2-type 왕복 일치', roundtrip(r2, out2) == [], str(roundtrip(r2, out2)[:2]))
    chk('★② mono 의 AM 이 `rP_um` 열에서 온다 (P 열 = 일반 AM 자리)',
        'variable r_AM   equal 0.0023' in out2, out2.split('\n')[5])

    #  ③ 음성 대조 — 왕복검사가 **정말** 잡는가
    swapped = out3.replace('pts1 0.400000', 'pts1 0.200000').replace(
        'pts2 0.200000', 'pts2 0.400000')
    chk('★③ 가중을 뒤바꾸면 잡는다', roundtrip(r3, swapped) != [])
    wrong_r = out3.replace('variable r_AM_S  equal 0.0008',
                           'variable r_AM_S  equal 0.0009')
    chk('★③ 반지름 하나만 틀려도 잡는다', roundtrip(r3, wrong_r) != [])
    wrong_seed = out2.replace('insert/pack seed 20021', 'insert/pack seed 20023')
    chk('★③ 본문 seed 가 헤더와 갈리면 잡는다', roundtrip(r2, wrong_seed) != [])
    dens = out2.replace('density constant 2000', 'density constant 4800')
    chk('★③ SE 밀도를 AM 으로 바꾸면 잡는다 (SE 템플릿 0개)',
        roundtrip(r2, dens) != [])

    #  ④ 치환이 못 맞으면 **거부**한다 (반쯤 바뀐 덱을 내지 않는다)
    broken = T2.replace('variable r_SE    equal 0.001', '# (r_SE 정의가 사라졌다)')
    try:
        render(broken, r2, 'lhs00_110')
        chk('★④ 템플릿 형식이 바뀌면 거부', False, '거부하지 않았다')
    except SystemExit as e:
        chk('★④ 템플릿 형식이 바뀌면 거부', 'r_SE' in str(e), str(e)[:60])

    #  ⑤ 봉인 해시 강제
    import tempfile
    p = os.path.join(tempfile.mkdtemp(prefix='mat_'), 'd.csv')
    open(p, 'w', newline='').write('id\nlhsx_001\n')
    try:
        load_design(p, 'de' + 'ad' * 31)
        chk('★⑤ sha 불일치 거부', False, '거부하지 않았다')
    except SystemExit:
        chk('★⑤ sha 불일치 거부', True)

    print(f'lhs_ext_materialize selftest: {ok}/{ok + len(fail)} PASS')
    for f in fail:
        print('  ✗', f)
    return 1 if fail else 0


if __name__ == '__main__':
    raise SystemExit(main())
