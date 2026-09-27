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

    # 순수 SE 판정 시험 (docs/reviews/pure_se_union_prereg_20260927.md) — 15 코어 러너까지
    python3 scripts/lhs_ext_materialize.py \\
        --pure-se pse_r050_a:0.5:0.22:20011 --pure-se pse_r075_a:0.75:0.22:20021 \\
        --pure-se pse_r100_a:1.0:0.22:20023 --pure-se pse_r100_b:1.0:0.22:20029 \\
        --template-2t ~/lhs_local/lhs00_110/input_lhs00_110.liggghts \\
        --template-run ~/lhs_local/lhs00_110/run_lhs00_110.sh --ntasks 15 --outdir <빈 폴더>
    ★ 순수 SE 덱은 AM 템플릿을 **분포에 가중 0 으로 남긴다** (지우거나 분포에서 빼면 LIGGGHTS 가
      "Atom types must start from 1" 로 죽는다 — render_pure_se 주석 ①, 2026-09-27 ibb 실패 ③).

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
_RE_PROC = re.compile(r'^[ \t]*processors[ \t]+([^\n]*?)[ \t]*$', re.M)
_RE_CBOX = re.compile(r'^[ \t]*create_box\s', re.M)


def _strip_comments(text: str) -> str:
    """주석(`#` 로 시작하는 줄)을 지운 **명령만** 남긴다.

    ⚠⚠ R15 §5: 옛 파서는 `re.search` 를 원문에 걸어서, 헤더 주석에 올바른 seed 를 적고
      실제 `fix insert/pack` 에는 옛 seed 를 둬도 **주석을 먼저 읽어** 왕복검사가 통과했다.
      왕복검사의 목적은 *"헤더가 본문과 갈리는가"* 이므로, 본문 파싱이 주석을 보면
      검사가 자기 목적을 배반한다.  헤더는 `_RE_CASE` 로 **따로** 읽어 대조한다.
    """
    return '\n'.join('' if ln.lstrip().startswith('#') else ln
                      for ln in text.split('\n'))


def parse_deck(text: str) -> dict:
    """덱 본문에서 설계량을 되읽는다.  **헤더 주석을 믿지 않는다.**

    헤더는 사람이 읽는 라벨이라 본문과 갈릴 수 있다 — 갈리는지 보는 것이 왕복검사의
    목적이므로, 본문에서 읽고 헤더는 따로 읽어 **대조**한다.
    """
    body = _strip_comments(text)          # ★ 본문 파싱은 **주석 없는** 사본에서
    var = {m.group(1): m.group(2) for m in _RE_VAR.finditer(body)}
    pts = [dict(fix=m.group(1), seed=int(m.group(2)), atom_type=int(m.group(3)),
                density=float(m.group(4)), rvar=m.group(5))
           for m in _RE_PTS.finditer(body)]
    mp = _RE_PDD.search(body)
    if not mp:
        raise ValueError('particledistribution/discrete 줄을 못 읽었다')
    n_decl = int(mp.group(2))
    toks = mp.group(3).split()
    weights = {}
    for i in range(0, len(toks) - 1, 2):
        weights[toks[i]] = float(toks[i + 1])
    mi, mv = _RE_INS.search(body), _RE_VF.search(body)
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
    #  ★ 분포에 든 템플릿의 최소 atom_type.  LIGGGHTS 는 입자 타입이 1 부터가 아니면 첫 run 에서
    #    `ERROR: Atom types must start from 1 for granular simulations (properties.cpp:120)` 로 죽는다.
    #    (여기서 pts 는 전부 분포에 든 템플릿이다 — 분포에 없는 템플릿은 위에서 이미 거부된다)
    out['min_type'] = min(p['atom_type'] for p in pts) if pts else None
    #  processors 줄 (영역 분할) — 있으면 create_box 앞이어야 한다
    procs = [(m.start(), ' '.join(m.group(1).split())) for m in _RE_PROC.finditer(body)]
    cbox = _RE_CBOX.search(body)
    out['processors'] = (procs[0][1] if len(procs) == 1 else ('MULTIPLE' if procs else None))
    out['processors_before_box'] = bool(procs) and bool(cbox) and procs[-1][0] < cbox.start()
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


def deck_weights(row: dict) -> tuple[float, ...]:
    """덱에 적을 질량분율.  **소수 6자리에서 합이 정확히 1** 이 되게 만든다.

    ★ 왜 (2026-08-30 실측): CSV 의 가중은 이미 6자리로 반올림돼 있어 그대로 적으면
      합이 `0.999999` / `1.000001` 로 나온다 — 64건 중 **6건**이 그랬다.  기존 130 덱은
      `0.510000 0.340000 0.150000` 처럼 **정확히 1** 이고, LIGGGHTS 가 합이 어긋난
      분포를 어떻게 받는지는 확인된 바 없다.  08-18 에 비소수 seed 로 25건이 즉시
      abort 한 전례가 있는 이상 "아마 괜찮다" 로 넘기지 않는다.
    ⚠ 검사 허용치를 늘리는 것은 **오답**이다 — 그러면 검사만 조용해지고 덱은 여전히
      0.999999 다.  고칠 자리는 덱이다.
    ⇒ 마이크로 단위 정수로 배분하고 **SE 에 잔차를 몰아준다**.  잔차가 반올림 규모를
      넘으면 (설계가 애초에 합 1이 아니라는 뜻) 거부한다.
    """
    nt = int(row['ntype'])
    WP = round(float(row['w_AM_P']) * 1e6)
    WS = round(float(row['w_AM_S']) * 1e6) if nt == 3 else 0
    WSE = 1_000_000 - WP - WS
    drift = abs(WSE / 1e6 - float(row['pdd_SE']))
    if drift > 2e-6:            # 6자리 셋의 반올림 한계(1.5e-6)를 넘으면 설계 문제다
        raise SystemExit(f'⛔ {row["id"]}: 가중 합이 1에서 {drift:.2e} 벗어난다 — '
                         '반올림으로 설명되지 않는다 (덱을 내지 않는다)')
    return ((WP / 1e6, WS / 1e6, WSE / 1e6) if nt == 3 else (WP / 1e6, WSE / 1e6))


def render(template: str, row: dict, tmpl_case: str) -> str:
    """템플릿 덱의 값만 갈아끼운다.  구조는 건드리지 않는다."""
    nt = int(row['ntype'])
    case = row['id']
    rP = float(row['rP_um']) / UM_PER_DECK_UNIT
    rSE = float(row['rSE_um']) / UM_PER_DECK_UNIT
    _w = deck_weights(row)
    wP, wSE = _w[0], _w[-1]
    t = template

    if nt == 3:
        rS = float(row['rS_um']) / UM_PER_DECK_UNIT
        wS = _w[1]
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


def _is_prime(n: int) -> bool:
    if n < 2 or n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


PURE_SE_PROCS = '* * 1'      # 순수 SE 덱의 기본 영역 분할 — 아래 render_pure_se ② 참조


def render_pure_se(template: str, case: str, r_se_um: float, volfrac: float, seed: int,
                   tmpl_case: str, procs: str | None = PURE_SE_PROCS) -> str:
    """2-type 실물 덱 → **AM 없는 순수 SE 덱** (판정 시험 `docs/reviews/pure_se_union_prereg_20260927.md`).

    바꾸는 것: 분포 가중 (AM 0 · SE 1) · r_SE · volfrac · insert seed · 케이스명 · (선택) processors 줄.
    **나머지 (벽 재질 · 플래튼 메시 · 목표 압력 · 재질 행렬 · 덤프 · 입자 템플릿 정의) 는 한 글자도 안
    바꾼다** — LHS 코호트와 같은 프로토콜이어야 비교가 선다.

    ① ★★ AM 템플릿은 **지우지도, 분포에서 빼지도 않는다.  분포에 가중 0 으로 남긴다.**
       (2026-09-27 ibb 실패 ③ · LIGGGHTS-PUBLIC 3.8 소스와 실제 실행으로 확인)
       - LIGGGHTS 는 run 초기화 때 `Properties::max_type()` 로 입자 타입 범위를 모으고, 최소가 1 이
         아니면 `ERROR: Atom types must start from 1 for granular simulations (properties.cpp:120)`.
       - 그 범위에 들어가는 것은 **존재하는 원자 · 분포 (distribution) 에 든 템플릿 · 벽 (primitive
         type) · 메시** 뿐이다.  `fix particletemplate/sphere` 자체는 min_type() 을 보고하지 않는다.
       - 삽입 · 침강 동안은 플래튼 메시 (type 1) 가 아직 없고 바닥 벽은 type 2 (SE) 다.
         ⇒ AM 템플릿 줄을 지우면 (옛 판) **최소 타입 = 2 → 즉시 abort** (실패 ③ 그대로 재현됨).
         ⇒ AM 템플릿을 정의만 남기고 분포에서 빼도 (실패 요약의 처방) **똑같이 abort** — 재현됨.
       - `particledistribution/discrete` 는 음수 가중만 거부하고 0 은 받는다.  개수는
         `int(N·w + U(0,1))` 이라 w = 0 이면 항상 0 개 (U < 1).  분포의 최소 타입은 **분포에 든 모든
         템플릿**으로 정하므로 type 1 이 남는다 → 검사 통과.
       - 실제 실행 (LIGGGHTS-PUBLIC 3.8, 축소 LHS 2-type 덱): `pts1 number% 0` · 삽입된 입자 **전부 type 2** ·
         침강 → 플래튼 → 안정화 → 압축 루프까지 오류 없음.
       - 부수 효과: 분포의 최대 반지름에 r_AM 이 남아 이웃 목록 bin 이 AM 기준 크기다 — 원래 LHS mono
         덱과 **같은** 조건이다 (물리는 불변, 속도만 영향).
    ② processors (기본 `* * 1`): 원래 LHS 러너는 1 코어라 분할이 없었다.  여러 코어로 돌리면 LIGGGHTS 는
       키 큰 상자를 z 로만 자른다 (ibb 실패 ③ 로그: `1 by 1 by 15`) → 침강 후 침대 (~27 µm) 가 한두 조각에
       몰려 나머지 코어는 논다.  `* * 1` 은 x·y 로 자른다 (15 → 5×3).  **물리는 그대로**, 코어 수를 바꿀 때와
       마찬가지로 비트 동일하지는 않다.  `create_box` 앞 (`region reg_box` 앞) 에 넣어 재시작 덱 (head 블록)
       에도 따라간다.  `procs=None` 이면 넣지 않는다.
    """
    d = parse_deck(template)
    if d['ntype'] != 2:
        raise SystemExit(f'⛔ 순수 SE 덱은 2-type (mono) 실물 템플릿에서만 만든다 — 받은 템플릿은 {d["ntype"]}-type')
    if not (seed > 10000 and _is_prime(seed)):
        raise SystemExit(f'⛔ insert seed {seed} — 10000 보다 큰 소수여야 한다 (08-18 비소수 seed 25 건 abort 사고)')
    if not (0.0 < volfrac < 0.6) or not (0.0 < r_se_um < 10.0):
        raise SystemExit(f'⛔ 범위 밖 — volfrac {volfrac} · r_SE {r_se_um} µm')
    am = [p for p in d['pts'] if p['density'] > 3000]
    se = [p for p in d['pts'] if p['density'] <= 3000]
    if len(am) != 1 or len(se) != 1:                       # pragma: no cover (parse_deck 가 먼저 막는다)
        raise SystemExit(f'⛔ AM {len(am)} · SE {len(se)} 템플릿 — 각각 1 개여야 한다')
    if am[0]['atom_type'] != 1 or d['min_type'] != 1:
        raise SystemExit(f'⛔ 템플릿의 AM atom_type {am[0]["atom_type"]} · 최소 타입 {d["min_type"]} — '
                         'AM 이 type 1 인 실물 2-type 덱이어야 한다 (LIGGGHTS 타입 1 규칙)')
    rSE = r_se_um / UM_PER_DECK_UNIT
    af, sf = re.escape(am[0]['fix']), re.escape(se[0]['fix'])
    t = template
    #  ① 분포: 템플릿 둘 다 남기고 가중만 AM 0 · SE 1 (순서는 실물대로 AM 먼저 — 다르면 거부)
    t = _sub1(t, rf'(particledistribution/discrete\s+\d+\s+2\s+){af}\s+[\d.]+(\s+){sf}\s+[\d.]+',
              rf'\g<1>{am[0]["fix"]} 0.000000\g<2>{se[0]["fix"]} 1.000000', '분포 → AM 0 · SE 1')
    t = _sub_all(t, r'pdd AM=[\d.]+(\s+)SE=[\d.]+', r'pdd AM=0.0000\g<1>SE=1.0000', '헤더 pdd(2)')
    #  ② 영역 분할
    if procs:
        if _RE_PROC.search(_strip_comments(t)):
            t = _sub1(t, r'^[ \t]*processors[ \t]+[^\n]*$', f'processors      {procs}', 'processors 줄 교체')
        else:
            t = _sub1(t, r'^(region\s+reg_box\s)', rf'processors      {procs}\n\g<1>',
                      'processors 줄 삽입 (region reg_box 앞)')
    t = _sub1(t, r'^(variable\s+r_SE\s+equal\s+)\S+', rf'\g<1>{rSE:.6g}', 'r_SE')
    t = _sub_all(t, r'rSE=[\d.eE+-]+', f'rSE={rSE:.6g}', '헤더 rSE')
    t = _sub_all(t, r'volfrac=[\d.eE+-]+', f'volfrac={volfrac:.6f}', '헤더 volfrac')
    t = _sub1(t, r'volumefraction_region\s+[\d.eE+-]+', f'volumefraction_region {volfrac:.6f}',
              'volumefraction_region')
    t = _sub1(t, r'insert/pack\s+seed\s+\d+', f'insert/pack seed {seed}', 'insert/pack seed')
    t = _sub_all(t, r'seed=\d+', f'seed={seed}', '헤더 seed')
    t = _sub1(t, rf'^(#\s*){re.escape(tmpl_case)}(:\s*)\S+', r'\g<1>' + case + r'\g<2>pure_SE',
              '헤더 케이스·kind')
    t = re.sub(r'(INSERTING\s*\(\s*' + re.escape(tmpl_case) + r',\s*)mono_AM_[PS]', r'\g<1>pure_SE', t)   # 표시용 (없어도 됨)
    t = t.replace(tmpl_case, case)
    if tmpl_case in t:                                     # pragma: no cover
        raise SystemExit('⛔ 템플릿 케이스명이 남았다')
    return t


def roundtrip_pure_se(case: str, r_se_um: float, volfrac: float, seed: int, text: str,
                      procs: str | None = PURE_SE_PROCS) -> list[str]:
    """생성한 순수 SE 덱을 **본문에서** 되읽어 대조한다 (헤더는 따로).  → 불일치 목록.

    ★ 순수 SE 의 정답 형태 (render_pure_se ① 참조): 템플릿 2 개 **둘 다 분포에** · AM (type 1) 가중 0 ·
      SE 가중 1 · 분포 최소 타입 1.  옛 판 (AM 줄 삭제) 과 실패 요약의 처방 (정의만 유지) 은 둘 다 여기서 걸린다.
    """
    bad = []
    try:
        d = parse_deck(text)
    except ValueError as e:
        return [f'{case}: 되읽기 실패 — {e}']
    if d['ntype'] != 2 or d['n_declared'] != 2:
        bad.append(f'{case}: 분포 템플릿 {d["ntype"]} · 선언 {d["n_declared"]} (2 · 2 이어야 — '
                   'AM 은 가중 0 으로 분포에 남아야 LIGGGHTS 타입 검사를 통과한다)')
    am = [p for p in d['pts'] if p['density'] > 3000]
    if len(am) != 1 or am[0]['weight'] != 0.0 or am[0]['atom_type'] != 1:
        bad.append(f'{case}: AM 템플릿 {[(p["fix"], p["atom_type"], p["weight"]) for p in am]} '
                   '(type 1 · 가중 0 하나여야)')
    if abs((d['pdd_SE'] or 0.0) - 1.0) > 1e-9:
        bad.append(f'{case}: SE 가중 {d["pdd_SE"]} (1 이어야)')
    if d['min_type'] != 1:
        bad.append(f'{case}: 분포 최소 atom_type {d["min_type"]} — LIGGGHTS 가 첫 run 에서 '
                   '"Atom types must start from 1" 로 죽는다')
    if procs and (d['processors'] != ' '.join(procs.split()) or not d['processors_before_box']):
        bad.append(f'{case}: processors {d["processors"]} (create_box 앞 {d["processors_before_box"]}) '
                   f'vs 요청 "{procs}"')
    if abs(d['r_SE_um'] - r_se_um) > 1e-6:
        bad.append(f'{case}: r_SE {d["r_SE_um"]} µm vs 요청 {r_se_um}')
    if abs(d['volfrac'] - volfrac) > 1e-6:
        bad.append(f'{case}: volfrac {d["volfrac"]} vs 요청 {volfrac}')
    if d['seed'] != seed:
        bad.append(f'{case}: seed {d["seed"]} vs 요청 {seed}')
    if d['header_case'] != case or d['header_kind'] != 'pure_SE':
        bad.append(f'{case}: 헤더 {d["header_case"]}:{d["header_kind"]}')
    return bad


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
    if d['min_type'] != 1:
        bad.append(f'{row["id"]} 분포 최소 atom_type {d["min_type"]} — LIGGGHTS 는 1 부터여야 한다')
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


_RE_RUN_JOB = re.compile(r'^#SBATCH\s+--job-name=(\S+)', re.M)
_RE_RUN_OUT = re.compile(r'^#SBATCH\s+--output=(\S+)', re.M)
_RE_RUN_TIME = re.compile(r'^#SBATCH\s+--time=(\S+)', re.M)
_RE_RUN_IN = re.compile(r'-in\s+(\S+\.liggghts)')
_RE_RUN_CD = re.compile(r'^\s*cd\s+(\S+)', re.M)
_RE_RUN_NT = re.compile(r'^#SBATCH\s+(?:-n\s+|--ntasks[= ])(\d+)', re.M)
_RE_RUN_NP = re.compile(r'\bmpirun\b[^\n]*?-np\s+(\d+)')
MPIRUN_FLAGS = '--oversubscribe --bind-to none'   # ibb: 이 둘이 없으면 여러 코어에서 바인딩 오류 (실패 ①②)


def _runner_case(text: str) -> str:
    m = _RE_RUN_JOB.search(text)
    if not m:
        raise SystemExit('⛔ 러너 템플릿에 `#SBATCH --job-name=` 이 없다')
    return m.group(1)


def render_runner(template: str, case: str, tmpl_case: str, ntasks: int | None = None) -> str:
    """러너의 케이스명을 갈아끼운다.  `ntasks` 를 주면 코어 수 두 자리도 바꾼다 — 그 밖의 구조는 그대로.

    ★ 러너에서 케이스명이 나오는 자리는 넷이다 — job-name · output 로그 · `cd` 경로 ·
      `-in` 덱 파일.  하나라도 옛 이름이 남으면 **다른 케이스의 덱을 돌리거나 로그를
      덮어쓴다**.  그래서 치환 후 옛 이름이 남았는지 확인하고, 넷을 각각 되읽어 대조한다.
    ★ `ntasks` (2026-09-27 실패 ①②): 사람이 sed 로 `-n 15` 만 바꿨다가 OpenMPI 바인딩 오류로 두 번 죽었다.
      ibb 에서 여러 코어는 `#SBATCH -n N` 과 `mpirun --oversubscribe --bind-to none -np N` 이 **짝**이어야
      한다.  두 자리를 정확히 한 번씩 바꾸고, 못 맞히면 거부한다 (반쯤 바뀐 러너를 내지 않는다).
    """
    if tmpl_case not in template:
        raise SystemExit(f'⛔ 러너 템플릿에서 케이스명 {tmpl_case} 을 못 찾았다')
    t = template.replace(tmpl_case, case)
    if tmpl_case in t:                                    # pragma: no cover
        raise SystemExit('⛔ 러너에 템플릿 케이스명이 남았다')
    if ntasks is not None:
        if not (1 <= int(ntasks) <= 60):
            raise SystemExit(f'⛔ ntasks {ntasks} — 1..60 (qos cpu-60)')
        t = _sub1(t, r'^(#SBATCH\s+(?:-n\s+|--ntasks[= ]))\d+', rf'\g<1>{int(ntasks)}', '#SBATCH -n')
        t = _sub1(t, r'\bmpirun\b(?:\s+--oversubscribe|\s+--bind-to\s+\S+)*\s+-np\s+\d+',
                  f'mpirun {MPIRUN_FLAGS} -np {int(ntasks)}', 'mpirun -np')
    return t


def roundtrip_runner(case: str, text: str, ntasks: int | None = None) -> list[str]:
    """생성한 러너를 되읽어 케이스명 네 자리 (와 `ntasks` 면 코어 두 자리) 를 확인한다.  → 불일치 목록."""
    bad = []
    if ntasks is not None:
        body0 = _strip_comments_keep_sbatch(text)
        nt = [int(x) for x in _RE_RUN_NT.findall(body0)]
        npv = [int(x) for x in _RE_RUN_NP.findall(body0)]
        if nt != [int(ntasks)]:
            bad.append(f'{case} 러너: #SBATCH -n {nt} vs 요청 {ntasks}')
        if npv != [int(ntasks)] or f'mpirun {MPIRUN_FLAGS} -np {int(ntasks)}' not in body0:
            bad.append(f'{case} 러너: mpirun -np {npv} / "{MPIRUN_FLAGS}" 필요 (요청 {ntasks})')
    body = _strip_comments_keep_sbatch(text)
    for what, rx, want in (('job-name', _RE_RUN_JOB, case),
                           ('output', _RE_RUN_OUT, case),
                           ('-in 덱', _RE_RUN_IN, f'input_{case}.liggghts'),
                           ('cd 경로', _RE_RUN_CD, case)):
        m = rx.search(text if rx is not _RE_RUN_IN else body)
        if not m:
            bad.append(f'{case} 러너: `{what}` 을 못 읽었다')
        elif want not in m.group(1):
            bad.append(f'{case} 러너 {what}: {m.group(1)} 에 {want} 가 없다')
    mt = _RE_RUN_TIME.search(text)
    if not mt:
        bad.append(f'{case} 러너: `--time` 이 없다 — 벽시간 없이 제출하지 않는다')
    return bad


def _strip_comments_keep_sbatch(text: str) -> str:
    """`#SBATCH` 는 지시자이므로 남기고, 나머지 주석만 지운다."""
    out = []
    for ln in text.split('\n'):
        st = ln.lstrip()
        out.append(ln if (not st.startswith('#') or st.startswith('#SBATCH')
                          or st.startswith('#!')) else '')
    return '\n'.join(out)


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
    ap.add_argument('--expect-sha256', help='봉인 해시 — **필수**')
    ap.add_argument('--box', help='봉인 상자 JSON — **필수** (템플릿 해시·설계 재검증)')
    ap.add_argument('--template-3t', help='bimodal 템플릿 덱 (실물)')
    ap.add_argument('--template-2t', help='mono 템플릿 덱 (실물)')
    ap.add_argument('--template-run', help='러너 템플릿 (실물 run_*.sh) — **필수**')
    ap.add_argument('--outdir', help='덱을 쓸 디렉터리 (없으면 dry-run: 검사만)')
    ap.add_argument('--pure-se', action='append', default=[], metavar='CASE:R_SE_UM:VOLFRAC:SEED',
                    help='순수 SE 판정 시험 덱 (docs/reviews/pure_se_union_prereg_20260927.md) — '
                         '--template-2t 필수 · --template-run 은 있으면 러너도 만든다 · 설계 CSV 흐름과 따로 돈다')
    ap.add_argument('--ntasks', type=int, default=None,
                    help='러너 코어 수 — `#SBATCH -n N` 과 `mpirun --oversubscribe --bind-to none -np N` 를 짝으로 '
                         '바꾼다 (안 주면 러너 자원은 템플릿 그대로)')
    ap.add_argument('--procs', default=PURE_SE_PROCS,
                    help=f'순수 SE 덱의 processors 줄 (기본 "{PURE_SE_PROCS}" — x·y 분할).  "none" 이면 넣지 않는다')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    if a.pure_se:
        return _main_pure_se(a)
    #  ★★ 전부 **필수**다 (R15 §4).  옛 판은 `--expect-sha256` 이 없으면 64 ID·소수
    #     seed·절대 칸을 아예 검사하지 않았고, 첫 seed 를 합성수 `4` 로 바꿔도
    #     "불일치 0건 · rc=0" 을 냈다 — 08-18 의 25건 abort 를 그대로 재현할 수 있었다.
    for need in ('design', 'expect_sha256', 'box', 'template_3t', 'template_2t',
                 'template_run'):
        if not getattr(a, need):
            ap.error(f'--{need.replace("_", "-")} 가 필요하다 (봉인 없이 덱을 만들지 않는다)')

    rows, sha = load_design(a.design, a.expect_sha256)
    t3 = open(a.template_3t, encoding='utf-8').read()
    t2 = open(a.template_2t, encoding='utf-8').read()
    c3, c2 = _tmpl_case(t3), _tmpl_case(t2)
    print(f'설계 {len(rows)}행 · sha256 {sha[:12]}…')
    print(f'템플릿 3-type {c3} · 2-type {c2}')

    #  ── 봉인 재검증: 설계 자체를 verifier 로 다시 돌린다 (조건 1·6 우회 차단) ──
    import subprocess as _sp
    _vf = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lhs_ext_design.py')
    _vr = _sp.run([sys.executable, _vf, '--verify', a.design,
                   '--box', a.box, '--expect-sha256', a.expect_sha256],
                  capture_output=True, text=True, stdin=_sp.DEVNULL)
    if _vr.returncode != 0:
        print(_vr.stdout[-2000:])
        raise SystemExit('⛔ 봉인 설계가 verifier 를 통과하지 못했다 — 덱을 만들지 않는다')
    print('봉인 재검증 ✓ (ID·소수 seed·절대 칸·해시)')

    #  ── 템플릿 해시를 상자 원장과 대조 ──────────────────────────────────
    import json as _json
    _bx = _json.load(open(a.box, encoding='utf-8'))
    _files = {os.path.basename(f['file']): f['sha256']
              for f in ((_bx.get('source') or {}).get('files') or [])}
    for _lbl, _path in (('3-type', a.template_3t), ('2-type', a.template_2t)):
        _bn = os.path.basename(_path)
        _h = hashlib.sha256(open(_path, 'rb').read()).hexdigest()
        _want = _files.get(_bn)
        if _want is None:
            raise SystemExit(f'⛔ 템플릿 {_bn} 이 상자 원장에 없다 — 어떤 파일로 만들었는지 '
                             '증명할 수 없으면 덱을 내지 않는다')
        if _h != _want:
            raise SystemExit(f'⛔ 템플릿 {_bn} 해시 불일치 — 원장 {_want[:12]}… '
                             f'실제 {_h[:12]}…  (템플릿이 변조됐다)')
        print(f'템플릿 {_lbl} {_bn} sha256 ✓ {_h[:12]}…')

    #  ── 전수 렌더 → 전수 검증 → **그 뒤에만** 공개 (R15 §5) ────────────────
    #  ⚠⚠ 옛 판은 한 건씩 검사하고 **곧바로 썼다**.  강제 실패 재현에서 "불일치 64건 ·
    #     wrote 64 decks · rc=1" 이 나왔고, 이전 세대 파일도 살아남았다.
    #     ⇒ 메모리에 다 만들고, 전부 통과했을 때만, **빈 디렉터리**에 쓴다.
    trun = open(a.template_run, encoding='utf-8').read()
    crun = _runner_case(trun)
    print(f'러너 템플릿 {crun}')
    made, runs = {}, {}
    bad = []
    for r in rows:
        nt = int(r['ntype'])
        text = render(t3 if nt == 3 else t2, r, c3 if nt == 3 else c2)
        bad += roundtrip(r, text)
        made[r['id']] = text
        rtext = render_runner(trun, r['id'], crun, a.ntasks)
        bad += roundtrip_runner(r['id'], rtext, a.ntasks)
        runs[r['id']] = rtext
    print(f'\n왕복검사 {len(rows)}건 — 불일치 {len(bad)}건')
    for b in bad[:12]:
        print('  ⛔', b)
    if bad:
        print('⛔ 불일치가 있어 **한 건도 쓰지 않는다**')
        return 1
    if not a.outdir:
        print('(dry-run — --outdir 를 주면 덱을 쓴다)')
        return 0
    if os.path.exists(a.outdir) and os.listdir(a.outdir):
        raise SystemExit(f'⛔ {a.outdir} 이 비어 있지 않다 — 세대가 섞인다.  '
                         '새 디렉터리를 주거나 비우고 다시 실행할 것')
    os.makedirs(a.outdir, exist_ok=True)
    man = []
    for cid, text in made.items():
        d = os.path.join(a.outdir, cid)
        os.makedirs(d, exist_ok=True)
        fp = os.path.join(d, f'input_{cid}.liggghts')
        with open(fp, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(text)
        rp = os.path.join(d, f'run_{cid}.sh')
        with open(rp, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(runs[cid])
        os.chmod(rp, 0o755)
        man.append(dict(id=cid, file=os.path.relpath(fp, a.outdir),
                        sha256=hashlib.sha256(text.encode('utf-8')).hexdigest(),
                        runner=os.path.relpath(rp, a.outdir),
                        runner_sha256=hashlib.sha256(
                            runs[cid].encode('utf-8')).hexdigest()))
    mp = os.path.join(a.outdir, 'deck_manifest.json')
    with open(mp, 'w', encoding='utf-8') as fh:
        _json.dump(dict(design_sha256=sha, n=len(man),
                        template_3t=dict(file=os.path.basename(a.template_3t),
                                         sha256=_files[os.path.basename(a.template_3t)]),
                        template_2t=dict(file=os.path.basename(a.template_2t),
                                         sha256=_files[os.path.basename(a.template_2t)]),
                        ids=sorted(made), decks=man),
                   fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write('\n')
    print(f'wrote {len(man)} decks → {a.outdir}')
    print(f'wrote {mp}  (ID census + 파일별 sha256)')
    return 0


def am_references(text: str) -> list[str]:
    """순수 SE 덱 **본문**에서 AM 에 기대는 줄 — AM 템플릿 정의 · 분포 줄 · r_AM 변수 정의는 뺀다.

    순수 SE 덱에 AM 이 0 개여도 LHS 프로토콜의 일부 (플래튼 높이 = zmax + r_AM + 여유 · 플래튼 메시 재질
    type 1) 는 **일부러 그대로 둔다** — lhsx mono 덱과 같은 조건이어야 비교가 서기 때문이다.  여기서 그
    줄들을 보여줘서, 사람이 "의도대로 남긴 것" 인지 확인하게 한다 (막지는 않는다).
    """
    d = parse_deck(text)
    am = [p for p in d['pts'] if p['density'] > 3000]
    if not am:
        return []
    rv, fx = re.escape(am[0]['rvar']), re.escape(am[0]['fix'])
    out = []
    for i, ln in enumerate(_strip_comments(text).split('\n'), 1):
        s = ' '.join(ln.split())
        if (not s or re.match(rf'variable {rv} equal', s) or re.match(rf'fix {fx} all particletemplate', s)
                or 'particledistribution/discrete' in s):
            continue
        if re.search(rf'\$\{{{rv}\}}|\bv_{rv}\b|\b{fx}\b|\btype 1\b', s):
            out.append(f'{i}: {s}')
    return out


def _main_pure_se(a) -> int:
    """`--pure-se` 흐름 — 2-type 실물 템플릿에서 순수 SE 덱 (과 러너) 을 만들고 되읽어 대조한 뒤에만 쓴다."""
    import json as _json
    if not a.template_2t:
        raise SystemExit('⛔ --pure-se 는 --template-2t (2-type 실물 덱) 가 필요하다')
    procs = None if str(a.procs).strip().lower() in ('none', '') else ' '.join(str(a.procs).split())
    t2 = open(a.template_2t, encoding='utf-8').read()
    c2 = _tmpl_case(t2)
    #  ★ 템플릿은 **봉인 상자에 기록된 그 실물 덱**이어야 한다 — lhsx mono 덱과 같은 프로토콜이어야 비교가 선다
    _t2sha = hashlib.sha256(open(a.template_2t, 'rb').read()).hexdigest()
    _boxp = a.box or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs', 'data',
                                  'lhs_ext_box_v2_20260829.json')
    _want = {f.get('file'): f.get('sha256')
             for f in ((_json.load(open(_boxp, encoding='utf-8')).get('source') or {}).get('files') or [])}
    _key = f'{c2}/input_{c2}.liggghts'
    if _want.get(_key) != _t2sha:
        raise SystemExit(f'⛔ 템플릿 {os.path.basename(a.template_2t)} sha256 {_t2sha[:12]}… 가 봉인 상자 ({os.path.basename(_boxp)}) '
                         f'의 {_key} = {str(_want.get(_key))[:12]}… 와 다르다 — 봉인된 실물 템플릿만 쓴다')
    print(f'템플릿 sha256 ✓ {_t2sha[:12]}… = 봉인 상자 {_key}')
    specs, made, runs, bad = [], {}, {}, []
    for s in a.pure_se:
        p = s.split(':')
        if len(p) != 4:
            raise SystemExit(f'⛔ --pure-se 형식은 CASE:R_SE_UM:VOLFRAC:SEED — 받은 값 {s}')
        case, r_se, vf, seed = p[0], float(p[1]), float(p[2]), int(p[3])
        if not re.fullmatch(r'[A-Za-z0-9_]+', case) or case in made:
            raise SystemExit(f'⛔ 케이스명 {case} — 영숫자·밑줄만, 중복 금지')
        text = render_pure_se(t2, case, r_se, vf, seed, c2, procs)
        bad += roundtrip_pure_se(case, r_se, vf, seed, text, procs)
        made[case] = text
        specs.append(dict(id=case, r_SE_um=r_se, volfrac=vf, seed=seed))
    trun = crun = None
    if a.template_run:
        trun = open(a.template_run, encoding='utf-8').read()
        crun = _runner_case(trun)
        for case in made:
            runs[case] = render_runner(trun, case, crun, a.ntasks)
            bad += roundtrip_runner(case, runs[case], a.ntasks)
    elif a.ntasks is not None:
        raise SystemExit('⛔ --ntasks 는 --template-run 이 있어야 쓴다 (러너를 만들 때만 의미가 있다)')
    print(f'템플릿 2-type {c2} · 순수 SE {len(made)} 건 · 러너 {"있음 (" + crun + ")" if trun else "없음"}'
          f' · 코어 {a.ntasks if a.ntasks is not None else "템플릿 그대로"} · processors {procs or "없음"}')
    for sp in specs:
        print(f"  {sp['id']}: r_SE {sp['r_SE_um']} µm · volfrac {sp['volfrac']} · seed {sp['seed']}")
    _first = next(iter(made.values()))
    _dd = parse_deck(_first)
    print('  분포: ' + ' · '.join(f"{p['fix']}(type {p['atom_type']}) {p['weight']:g}" for p in _dd['pts'])
          + f"  → 최소 atom_type {_dd['min_type']} (LIGGGHTS 는 1 이어야 돈다)")
    _refs = am_references(_first)
    if _refs:
        print('  ℹ AM 에 기대는 줄 (LHS 프로토콜 그대로 — 의도대로 남김, 확인만):')
        for _r in _refs:
            print('     ' + _r)
    print(f'왕복검사 — 불일치 {len(bad)} 건')
    for b in bad:
        print('  ⛔', b)
    if bad:
        print('⛔ 불일치가 있어 **한 건도 쓰지 않는다**')
        return 1
    if not a.outdir:
        print('(dry-run — --outdir 를 주면 덱을 쓴다)')
        return 0
    if os.path.exists(a.outdir) and os.listdir(a.outdir):
        raise SystemExit(f'⛔ {a.outdir} 이 비어 있지 않다 — 새 디렉터리를 줄 것')
    os.makedirs(a.outdir, exist_ok=True)
    man = []
    for case, text in made.items():
        d = os.path.join(a.outdir, case)
        os.makedirs(d, exist_ok=True)
        fp = os.path.join(d, f'input_{case}.liggghts')
        with open(fp, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(text)
        ent = dict(id=case, file=os.path.relpath(fp, a.outdir),
                   sha256=hashlib.sha256(text.encode('utf-8')).hexdigest())
        if case in runs:
            rp = os.path.join(d, f'run_{case}.sh')
            with open(rp, 'w', encoding='utf-8', newline='\n') as fh:
                fh.write(runs[case])
            os.chmod(rp, 0o755)
            ent.update(runner=os.path.relpath(rp, a.outdir),
                       runner_sha256=hashlib.sha256(runs[case].encode('utf-8')).hexdigest())
        man.append(ent)
    mp = os.path.join(a.outdir, 'deck_manifest.json')
    with open(mp, 'w', encoding='utf-8') as fh:
        _json.dump(dict(purpose='pure_se_union_prereg_20260927', n=len(man), specs=specs,
                        am_template='분포에 가중 0 으로 유지 (LIGGGHTS 타입 1 규칙 · 실패 ③)',
                        processors=procs, ntasks=a.ntasks,
                        mpirun=(f'mpirun {MPIRUN_FLAGS} -np {a.ntasks}' if a.ntasks is not None else None),
                        template_2t=dict(file=os.path.basename(a.template_2t), case=c2,
                                         sha256=hashlib.sha256(t2.encode('utf-8')).hexdigest()),
                        template_run=(dict(file=os.path.basename(a.template_run), case=crun) if trun else None),
                        decks=man), fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write('\n')
    print(f'wrote {len(man)} decks → {a.outdir}  ·  {mp}')
    return 0


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
region reg_box block 0.0 0.05 0.0 0.05 -0.01 1.0 units box
create_box      2 reg_box
fix zwall_bot all wall/gran model hooke/hysteresis tangential history rolling_friction cdt primitive type 2 zplane 0.0
fix pts1 all particletemplate/sphere 15485863 atom_type 1 density constant 4800 radius constant ${r_AM}
fix pts2 all particletemplate/sphere 32452843 atom_type 2 density constant 2000 radius constant ${r_SE}
fix pdd_mix all particledistribution/discrete 49979687 2 pts1 0.800000 pts2 0.200000
print "====== INSERTING (lhs00_110, mono_AM_S, seed=11059) ======"
fix ins_mix all insert/pack seed 11059 distributiontemplate pdd_mix &
    volumefraction_region 0.250627
shell mkdir post_lhs00_110
variable plate_z equal ${z_max}+${r_AM}+${plate_margin}
fix top_mesh all mesh/surface/stress file plate_lhs00_110.stl type 1 scale 1.0 reference_point 0 0 0
"""
    T3 = """# ============================================================
# lhs00_000: bimodal (3-type) | LHS design
# rP=0.0055 rS=0.0005 rSE=0.001 | pdd AM_P=0.5100 AM_S=0.3400 SE=0.1500
# volfrac=0.222984 | E_se=0.135e7 (고정) | seed=10007
# ============================================================
variable r_AM_P  equal 0.0055
variable r_AM_S  equal 0.0005
variable r_SE    equal 0.001
region reg_box block 0.0 0.05 0.0 0.05 -0.01 1.0 units box
create_box      3 reg_box
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

    #  ②-b 가중 합이 **덱 문자열에서** 정확히 1 인가 (2026-08-30 실사고)
    #     CSV 값을 그대로 적으면 6자리 반올림으로 0.999999 가 나온다 — 64건 중 6건.
    r3b = dict(r3, w_AM_P='0.409999', w_AM_S='0.200000', pdd_SE='0.390000')
    o3b = render(T3, r3b, 'lhs00_000')
    import re as _re
    _m = _re.search(r'discrete\s+\d+\s+3\s+pts1\s+([\d.]+)\s+pts2\s+([\d.]+)'
                    r'\s+pts3\s+([\d.]+)', o3b)
    chk('★②-b 덱 가중 문자열의 합이 정확히 1',
        _m is not None and sum(map(float, _m.groups())) == 1.0,
        _m.groups() if _m else 'no match')
    chk('★②-b 잔차는 SE 로 간다 (AM 은 설계값 그대로)',
        _m is not None and _m.group(1) == '0.409999' and _m.group(2) == '0.200000',
        _m.groups() if _m else '')
    chk('②-b 그래도 왕복은 통과한다', roundtrip(r3b, o3b) == [],
        str(roundtrip(r3b, o3b)[:2]))

    #  ②-c 주석은 본문이 아니다 (R15 §5) — 헤더에 옳은 seed, 본문에 옛 seed
    spoof = out2.replace('insert/pack seed 20021', 'insert/pack seed 19991')
    chk('★②-c 주석의 올바른 seed 로 본문을 가릴 수 없다',
        roundtrip(r2, spoof) != [], str(roundtrip(r2, spoof)[:1]))
    chk('★②-c 파서가 본문 seed 를 읽는다 (주석 아님)',
        parse_deck(spoof)['seed'] == 19991, str(parse_deck(spoof)['seed']))
    #  주석에 가짜 변수 정의를 심어도 본문 값이 이긴다
    spoof2 = out2.replace('# rAM=0.0023', '# rAM=0.0023\n# variable r_SE    equal 0.999')
    chk('★②-c 주석 속 변수 정의를 무시한다',
        abs(parse_deck(spoof2)['r_SE_um'] - 0.7) < 1e-9,
        str(parse_deck(spoof2)['r_SE_um']))

    #  ②-d 러너 (실물 형식 축소, R15 §6) ──────────────────────────────────
    TRUN = """#!/bin/bash
#SBATCH --job-name=lhs00_000
#SBATCH --output=logs/output_lhs00_000_%j.out
#SBATCH --qos=cpu-60
#SBATCH --partition=cpu
#SBATCH -n 1
#SBATCH --time=5-00:00:00

source ~/.bashrc
conda activate myenv
cd ~/dem_test/lhs/lhs00_000
mpirun -np 1 lmp_mpi -in input_lhs00_000.liggghts
"""
    chk('②-d 러너 템플릿 케이스명', _runner_case(TRUN) == 'lhs00_000')
    rr = render_runner(TRUN, 'lhsx_007', 'lhs00_000')
    chk('②-d 러너 왕복 일치', roundtrip_runner('lhsx_007', rr) == [],
        str(roundtrip_runner('lhsx_007', rr)[:2]))
    chk('★②-d 네 자리가 다 바뀐다 (job·log·cd·-in)',
        'job-name=lhsx_007' in rr and 'output_lhsx_007_' in rr
        and 'lhs/lhsx_007' in rr and '-in input_lhsx_007.liggghts' in rr)
    chk('★②-d 옛 케이스명이 한 자도 안 남는다', 'lhs00_000' not in rr)
    chk('②-d 자원 요청은 안 건드린다',
        '--time=5-00:00:00' in rr and '--qos=cpu-60' in rr and '-n 1' in rr)
    #  ★ 덱 이름만 옛것으로 남으면 **다른 케이스를 돌린다** — 잡아야 한다
    wrong_in = rr.replace('-in input_lhsx_007.liggghts', '-in input_lhsx_006.liggghts')
    chk('★②-d 러너가 다른 덱을 가리키면 잡는다',
        roundtrip_runner('lhsx_007', wrong_in) != [])
    no_time = '\n'.join(l for l in rr.split('\n') if '--time' not in l)
    chk('★②-d 벽시간이 없으면 잡는다', roundtrip_runner('lhsx_007', no_time) != [])

    #  ②-e 러너 코어 수 (2026-09-27 실패 ①② — 사람이 sed 로 -n 만 바꿔 OpenMPI 바인딩 오류) ──
    r15 = render_runner(TRUN, 'pse_r050_a', 'lhs00_000', 15)
    chk('★②-e ntasks 15: `#SBATCH -n 15` · `mpirun --oversubscribe --bind-to none -np 15` 짝',
        '#SBATCH -n 15' in r15 and 'mpirun --oversubscribe --bind-to none -np 15 lmp_mpi' in r15
        and '-np 1 ' not in r15, [l for l in r15.split('\n') if 'mpirun' in l or '-n ' in l])
    chk('②-e ntasks 러너 왕복 일치', roundtrip_runner('pse_r050_a', r15, 15) == [],
        str(roundtrip_runner('pse_r050_a', r15, 15)))
    _r2x = render_runner(r15, 'pse_r075_a', 'pse_r050_a', 15)
    chk('②-e 이미 --oversubscribe 가 있는 러너도 한 번만 바뀐다 (플래그 중복 없음)',
        _r2x.count('--oversubscribe') == 1 and _r2x.count('--bind-to') == 1
        and roundtrip_runner('pse_r075_a', _r2x, 15) == [], [l for l in _r2x.split('\n') if 'mpirun' in l])
    half = r15.replace('-np 15 lmp_mpi', '-np 1 lmp_mpi')
    chk('★②-e -n 과 -np 가 갈리면 잡는다 (반쯤 고친 러너)', roundtrip_runner('pse_r050_a', half, 15) != [])
    noflag = r15.replace(f'mpirun {MPIRUN_FLAGS} -np 15', 'mpirun -np 15')
    chk('★②-e --oversubscribe --bind-to none 이 빠지면 잡는다', roundtrip_runner('pse_r050_a', noflag, 15) != [])
    for _bad_t, _why in ((TRUN.replace('#SBATCH -n 1', '#SBATCH --cpus-per-task=1'), '-n 줄 없는 러너'),
                         (TRUN, 'ntasks 61')):
        try:
            render_runner(_bad_t, 'pse_x', 'lhs00_000', 61 if 'ntasks' in _why else 15)
            chk(f'★②-e {_why} 거부', False, '거부하지 않았다')
        except SystemExit:
            chk(f'★②-e {_why} 거부', True)

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

    #  ③-b 분포 최소 atom_type 이 1 이 아니면 (LIGGGHTS properties.cpp:120) 설계 흐름도 잡는다
    shifted = out2.replace('atom_type 2 density', 'atom_type 3 density').replace(
        'atom_type 1 density', 'atom_type 2 density')
    chk('★③-b 분포 타입이 2 부터면 잡는다', roundtrip(r2, shifted) != [], str(roundtrip(r2, shifted)[:1]))

    #  ⑥ 순수 SE 판정 시험 (docs/reviews/pure_se_union_prereg_20260927.md) — 2-type 실물 덱에서
    #    **AM 템플릿은 정의·분포에 그대로 두고 가중만 0**, SE 가중 1.  (실패 ③ · render_pure_se ① 참조)
    #    나머지 규약 (벽 · 플래튼 · 압력 · 재질 · 템플릿 정의) 은 한 글자도 안 바꾼다.
    try:
        ps = render_pure_se(T2, 'pse_r050_a', 0.5, 0.22, 20011, 'lhs00_110')
        dps = parse_deck(ps)
        chk('⑥ 순수 SE: 템플릿 2 개가 **둘 다 분포에** (선언 2)', dps['ntype'] == 2 and dps['n_declared'] == 2,
            str((dps['ntype'], dps['n_declared'])))
        _am = [p for p in dps['pts'] if p['density'] > 3000]
        chk('★⑥ 순수 SE: AM(type 1) 가중 정확히 0 · SE 가중 정확히 1',
            len(_am) == 1 and _am[0]['atom_type'] == 1 and _am[0]['weight'] == 0.0 and dps['pdd_SE'] == 1.0,
            str([(p['fix'], p['atom_type'], p['weight']) for p in dps['pts']]))
        chk('★⑥ 순수 SE: 분포 최소 atom_type 1 (LIGGGHTS 타입 규칙)', dps['min_type'] == 1, str(dps['min_type']))
        chk('⑥ 순수 SE: AM 템플릿 정의 줄은 템플릿과 한 글자도 같다',
            [l for l in T2.split('\n') if l.startswith('fix pts1 ')][0] in ps.split('\n'))
        chk('⑥ 순수 SE: r_SE 0.5 µm · volfrac 0.22 · seed 20011',
            abs(dps['r_SE_um'] - 0.5) < 1e-9 and abs(dps['volfrac'] - 0.22) < 1e-9 and dps['seed'] == 20011,
            str((dps['r_SE_um'], dps['volfrac'], dps['seed'])))
        chk('⑥ 순수 SE: 케이스명 · kind 헤더 · 템플릿명 잔존 0',
            dps['header_case'] == 'pse_r050_a' and dps['header_kind'] == 'pure_SE' and 'lhs00_110' not in ps,
            str((dps['header_case'], dps['header_kind'])))
        chk('★⑥ 순수 SE: processors "* * 1" 이 create_box 앞에 한 번',
            dps['processors'] == '* * 1' and dps['processors_before_box']
            and ps.count('\nprocessors ') == 1, str((dps['processors'], dps['processors_before_box'])))
        chk('⑥ 순수 SE: 왕복검사 불일치 0', roundtrip_pure_se('pse_r050_a', 0.5, 0.22, 20011, ps) == [],
            str(roundtrip_pure_se('pse_r050_a', 0.5, 0.22, 20011, ps)))
        chk('⑥ 순수 SE: 왕복검사가 틀린 seed 를 잡는다', roundtrip_pure_se('pse_r050_a', 0.5, 0.22, 20021, ps) != [])
        #  ★ 실패 ③ 의 두 형태 — 둘 다 LIGGGHTS 에서 "Atom types must start from 1" 로 죽는 덱이다
        _pts1 = [l for l in ps.split('\n') if l.startswith('fix pts1 ')][0] + '\n'
        old_gen = ps.replace(_pts1, '').replace('2 pts1 0.000000 pts2 1.000000', '1 pts2 1.000000')
        chk('★⑥ 옛 판 (AM 템플릿 줄 삭제 · 분포 SE 단독) 을 잡는다',
            roundtrip_pure_se('pse_r050_a', 0.5, 0.22, 20011, old_gen) != [])
        def_only = ps.replace('2 pts1 0.000000 pts2 1.000000', '1 pts2 1.000000')
        chk('★⑥ 실패 요약의 처방 (AM 정의만 유지 · 분포에서 뺌) 을 잡는다',
            roundtrip_pure_se('pse_r050_a', 0.5, 0.22, 20011, def_only) != [])
        some_am = ps.replace('pts1 0.000000', 'pts1 0.000001').replace('pts2 1.000000', 'pts2 0.999999')
        chk('★⑥ AM 가중이 0 이 아니면 잡는다', roundtrip_pure_se('pse_r050_a', 0.5, 0.22, 20011, some_am) != [])
        no_proc = ps.replace('processors      * * 1\n', '')
        chk('★⑥ processors 줄이 빠지면 잡는다', roundtrip_pure_se('pse_r050_a', 0.5, 0.22, 20011, no_proc) != [])
        ps0 = render_pure_se(T2, 'pse_r050_a', 0.5, 0.22, 20011, 'lhs00_110', None)
        chk('⑥ procs=None 이면 processors 줄을 넣지 않고 왕복도 통과',
            'processors' not in ps0 and roundtrip_pure_se('pse_r050_a', 0.5, 0.22, 20011, ps0, None) == [])
        tp = T2.replace('region reg_box', 'processors      * * *\nregion reg_box')
        psr = render_pure_se(tp, 'pse_r050_a', 0.5, 0.22, 20011, 'lhs00_110')
        chk('⑥ 템플릿에 processors 가 있으면 그 줄을 바꾼다 (중복 없음)',
            psr.count('\nprocessors ') == 1 and 'processors      * * 1' in psr)
        _refs = am_references(ps)
        chk('⑥ AM 참조 보고: 플래튼 높이 (r_AM) · 플래튼 메시 재질 (type 1) 을 보여준다',
            any('plate_z' in r for r in _refs) and any('top_mesh' in r for r in _refs), str(_refs))
    except (NameError, SystemExit, ValueError, IndexError) as e:
        chk('⑥ 순수 SE 덱 생성', False, f'{type(e).__name__}: {e}'[:80])
    for _args, _why in (((T3, 'x', 0.5, 0.22, 20011, 'lhs00_000'), '3-type 템플릿'),
                        ((T2, 'x', 0.5, 0.22, 20013, 'lhs00_110'), '비소수 seed'),
                        ((T2, 'x', 0.5, 0.22, 9973, 'lhs00_110'), 'seed ≤ 10000'),
                        ((T2.replace('2 pts1 0.800000 pts2 0.200000', '2 pts2 0.200000 pts1 0.800000'),
                          'x', 0.5, 0.22, 20011, 'lhs00_110'), '분포 순서가 실물과 다른 템플릿')):
        try:
            render_pure_se(*_args)
            chk(f'★⑥ {_why} 거부', False, '거부하지 않았다')
        except SystemExit:
            chk(f'★⑥ {_why} 거부', True)
        except NameError as e:
            chk(f'★⑥ {_why} 거부', False, str(e)[:60])

    print(f'lhs_ext_materialize selftest: {ok}/{ok + len(fail)} PASS')
    for f in fail:
        print('  ✗', f)
    return 1 if fail else 0


if __name__ == '__main__':
    raise SystemExit(main())
