#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lacey 혼합지수 `M(t)` — §24 층상 시작 런의 **믹싱** 지표 (2026-09-20).

    python3 scripts/measure_mixing_index.py <런 디렉터리> --ref <균일 삽입 런 디렉터리>
    python3 scripts/measure_mixing_index.py --selftest

━━ 정의 (사전등록 §24-3 — 결과 보고 바꾸지 않는다) ━━━━━━━━━━━━━━━━━━━━━━━━━━━
  셀      (y, z) `cells`×`cells` × x `x_cells`  (드럼 축 x, 통 반경 R 기준).  입자 ≥ n_min 인 칸만.
  p_i     칸 i 의 AM **부피분율** (type 1·2 부피 / 칸 안 고체 부피)
          ⚠ 개수분율이면 SE(개수 73 %)가 지배해 AM 의 분포를 못 본다.
  S²(t)   p_i 의 칸 간 분산
  S₀²     같은 런의 t=0 (정착 끝) 프레임         ← 층상 = 완전 분리 기준
  S_R²    균일 삽입 런(--ref, 같은 시드·같은 칸)의 정착 끝 프레임   ← 무작위 기준 (실측)
          (둘 다 **그 덱의 계획 t₀ step 정확히** — 없으면 거부, 앞 프레임으로 대신하지 않는다 · 2026-09-28 HBR3-05)
  M(t)  = (S₀² − S²(t)) / (S₀² − S_R²)

  ⚠ S_R² 를 이항식으로 두지 않는 이유: 다분산·부피가중 분율에 이항 공식이 안 맞는다.
    균일 삽입 침대가 이미 있으니(§13 E0) **같은 코드로 재서** 기준을 삼는다.

━━ 2026-09-27 보조 진단 (Codex HB-05) — M 의 정의는 그대로, 판정에 안 쓰는 값만 더 적는다 ━━━━━━━━━━━━━
  ① `planned` = 덱의 계획 바퀴 수의 **마지막 완전 bin** (8 바퀴면 bin 7, 25 프레임) 과 평탄 조건.
     ⚠ 옛 `M_final` 은 **마지막 bin** 이라 중간 판독에서는 부분 bin (2–12 프레임) 이다 — 최종값으로 쓰지 말 것.
  ② 칸 선택 진단 — `n_min` 미만 칸을 버리면 한 상이 버린 칸에 몰렸을 때 분리가 숨는다 (셀프테스트 ⑫).
     프레임마다 상별 유지 부피·입자 비 (`am_vol_kept` · `se_vol_kept` …) · 버린 칸 · 칸당 입자 중앙값 ·
     빈 칸만 뺀 **전 칸 M (`M_all`, 민감도)**.
  ③ `tech` — 미완주 · 최종 bin 비유한값 · 최종·직전 bin 덤프 결손 · 계산에서 뺀 프레임 (아래 ④).  있으면 등록 최종값을 쓰지 않는다.

━━ 2026-09-28 (Codex 3차 HBR3-05 · 06) — t₀ 는 계획 step 정확히 · 계산에 들어가는 프레임의 자격 ━━━━━━━━━━━━━━━━━━━
  ④ t₀ = `planned_t0(덱)` = ⌊2·steps_fill / dump_every⌋·dump_every — 평가 런 · E0 기준 **둘 다** 그 step 의 덤프가 정확히 한 장
     있고 스키마 검사 (measure_bed_aspect.validate_frame) 를 넘어야 한다.  아니면 거부 (옛 판은 앞 정착 프레임으로 조용히 대신했다).
  ⑤ 행 (M · SD · 평탄 · QC 에 들어가는 프레임) = 계획 덤프 격자 (t₀ + k·dump_every ≤ 덱 끝) 위 · step 당 한 장 · 검사 통과.
     격자 밖 · 같은 step 둘 이상 · 머리 없음 · 머리 step ≠ 파일명 · 소수 type · id 없음 … 은 빼고 tech (bin 0 이면 tech_smoke 도) 에 적는다.
     `dump_gaps` 는 옛 판 그대로 있는 파일 전부의 간격이다.

━━ t=0 · 바퀴 경계는 덱(`in.mixer`)에서 읽는다 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  `run N` 두 번 = 정착 (`2·steps_fill`) · `timestep` · `fix mvD … period P` ⇒ 바퀴 = P/dt 스텝.
  t₀ = 정착 끝 직전의 덤프 격자점 (④ · planned_t0).
  덱이 실행 기록이므로 별도 메타파일을 두지 않는다 (두 벌이면 갈린다).
  ⚠ 프레임은 **숫자순** (`ls | tail` 함정 — measure_bed_aspect.frames 를 재사용).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

import numpy as np

_SCR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCR)
from measure_bed_aspect import frames, read_dump, validate_frame  # noqa: E402

AM_TYPES = (1, 2)
#  D-2 (2026-09-27 저녁 등록 — 겹침 미열람 · M 열람 뒤 = 진단-맹검 개정): 등록 bin 의 부피 누락 QC.  ⚠ 대표성 보증이 아니다 —
#  유지 0.98 이어도 S²_keep 0 · S²_all 0.2 인 반례 (Codex HBR2-06 · 셀프테스트 ⑱).  미달이면 M 을 지우지 않고
#  "선택-셀 M · 대표성 QC 미달 — 전체-bed 결론 제한" 으로 보고한다 (K3).  평균만 보면 25 프레임 중 2 프레임 유지 0 도 0.92 로
#  통과하므로 프레임별 · 상별 최솟값을 같이 건다.
QC_MEAN_MIN, QC_FRAME_MIN = 0.90, 0.80


def dump_header(path):
    """덤프 머리 → (TIMESTEP, NUMBER OF ATOMS).  없으면 (None, None).  파일명 step · 행 수와 대조하는 데 쓴다 (HBR2-04 · 08).

    ⚠ 2026-09-28 (Codex 3차 HBR3-06) — None 은 "머리 없음" 이다, 통과가 아니다.  판독기 (analyse) 는 이 함수 대신
      measure_bed_aspect.validate_frame 으로 매 프레임을 검사한다 (check_contact_validity 가 import 해서 남겨 둔다).
    """
    with open(path, encoding='utf-8', errors='replace') as fh:
        L = [next(fh, '') for _ in range(4)]
    st = int(L[1]) if L[0].startswith('ITEM: TIMESTEP') and L[1].strip().lstrip('-').isdigit() else None
    n = int(L[3]) if L[2].startswith('ITEM: NUMBER OF ATOMS') and L[3].strip().isdigit() else None
    return st, n


def qc_representativeness(rows):
    """등록 bin 의 프레임 행 (am_vol_kept · se_vol_kept · vol_kept_by_type) → dict(pass, am_mean, se_mean, min_by_type, rule)."""
    am = float(np.mean([r_['am_vol_kept'] for r_ in rows]))
    se = float(np.mean([r_['se_vol_kept'] for r_ in rows]))
    types = sorted({t_ for r_ in rows for t_ in r_['vol_kept_by_type']})
    mn = {t_: float(min(r_['vol_kept_by_type'].get(t_, float('nan')) for r_ in rows)) for t_ in types}
    ok = bool(am >= QC_MEAN_MIN and se >= QC_MEAN_MIN and all(v >= QC_FRAME_MIN for v in mn.values()))
    return {'pass': ok, 'am_mean': am, 'se_mean': se, 'min_by_type': mn,
            'rule': f'mean(AM, SE) ≥ {QC_MEAN_MIN} ∧ 프레임별 · 상별 최솟값 ≥ {QC_FRAME_MIN} (부피 누락 QC — 대표성 보증 아님)'}


def deck_plan(deck_path):
    """`in.mixer` → dict(steps_fill, dump_every, dt, steps_per_rev, steps_run).  없으면 ValueError."""
    t = open(deck_path, encoding='utf-8', errors='replace').read()
    runs = [int(x) for x in re.findall(r'^run\s+(\d+)\s*$', t, re.M)]
    #  실제 덱은 `run 1`(삽입) · `run F` · `run F`(정착 두 번) · `run N`(회전) = 넷이다.
    #  ⇒ **회전 직전의 같은 값 두 줄**을 정착으로 잡는다 (앞에 뭐가 있든).
    if len(runs) < 3:
        raise ValueError(f'run 줄이 {len(runs)}개 — 정착 2 + 회전 1 이어야 한다')
    if runs[-3] != runs[-2]:
        raise ValueError(f'회전 직전의 두 run 이 다르다: {runs[-3]} vs {runs[-2]} (정착이 아니다)')
    dt = float(re.search(r'^timestep\s+([0-9.eE+-]+)', t, re.M).group(1))
    per = float(re.search(r'fix\s+mvD\s+.*?period\s+([0-9.eE+-]+)', t).group(1))
    de = int(re.search(r'^dump\s+dmp\s+all\s+custom\s+(\d+)', t, re.M).group(1))
    return dict(steps_fill=runs[-2], dump_every=de, dt=dt,
                steps_per_rev=per / dt, steps_run=runs[-1], n_run_lines=len(runs), steps_total=sum(runs))


def cell_variance(D, r_container, cells=8, x_cells=2, n_min=20, axis='x'):
    """한 프레임 → (S², 쓴 칸 수, 버린 칸 수, 칸별 p_i).  (계산은 cell_stats — 이 함수는 옛 반환형 그대로)"""
    st = cell_stats(D, r_container, cells, x_cells, n_min, axis)
    return st['s2'], st['used'], st['dropped'], st['p']


def cell_stats(D, r_container, cells=8, x_cells=2, n_min=20, axis='x'):
    """한 프레임 → dict: s2 · used · dropped · p (= cell_variance) + **보조 진단** (2026-09-27, Codex HB-05).

    ⚠ 왜 — `n_min` 미만 칸을 버리므로 **한 상이 통째로 버린 칸에 몰리면 분리가 '분산 0' 으로 숨는다**
      (셀프테스트 ⑫: AM 칸 둘 + SE 19 알 칸 하나 → S² = 0).  M 의 정의는 바꾸지 않고, 버린 몫을 **보이게** 한다:
      am_vol_kept · se_vol_kept = 쓴 칸 안의 상별 부피 / 그 상 전체 · am_n_kept · se_n_kept (입자 수) ·
      nonempty (빈 칸 아닌 칸) · cell_n_median (쓴 칸의 입자 수 중앙값 — prereg §2 가 보고를 요구) ·
      s2_all = **빈 칸만 뺀 모든 칸**의 분산 (민감도 — 판정에 쓰지 않는다).
      'se' = AM 이 아닌 상 전부 (3 상 캠페인에서는 SE).
    """
    x, y, z = D['x'], D['y'], D['z']
    r = D['radius']; t = D['type'].astype(int)
    vol = (4.0 / 3.0) * np.pi * r ** 3
    am = np.isin(t, AM_TYPES).astype(float)
    if axis == 'x':                                    # 자유 단면 (y, z), 축 x
        a, b, c = y, z, x
    elif axis == 'y':
        a, b, c = x, z, y
    else:
        a, b, c = x, y, z
    R = float(r_container)
    ia = np.clip(((a + R) / (2 * R) * cells).astype(int), 0, cells - 1)
    ib = np.clip(((b + R) / (2 * R) * cells).astype(int), 0, cells - 1)
    lo, hi = c.min(), c.max()
    ic = np.clip(((c - lo) / max(hi - lo, 1e-12) * x_cells).astype(int), 0, x_cells - 1)
    key = (ia * cells + ib) * x_cells + ic
    ncell = cells * cells * x_cells
    cnt = np.bincount(key, minlength=ncell)
    cam = np.bincount(key, weights=am, minlength=ncell)
    vtot = np.bincount(key, weights=vol, minlength=ncell)
    vam = np.bincount(key, weights=vol * am, minlength=ncell)
    use = cnt >= n_min
    ne = cnt > 0
    p = vam[use] / np.maximum(vtot[use], 1e-30)
    s2 = float(p.var(ddof=0)) if p.size > 1 else float('nan')
    p_all = vam[ne] / np.maximum(vtot[ne], 1e-30)
    vse, cse = vtot - vam, cnt - cam

    def _frac(a_, tot):
        return float(a_[use].sum() / tot) if tot > 0 else float('nan')
    vk = {}                                             # 상별 (type 별) 유지 부피 — AM_P · AM_S 를 합치면 작은 AM_S 의 누락이 숨는다 (K3)
    for t_ in np.unique(t):
        m_ = (t == t_).astype(float)
        vk[int(t_)] = _frac(np.bincount(key, weights=vol * m_, minlength=ncell), float((vol * m_).sum()))
    return dict(s2=s2, used=int(use.sum()), dropped=int(ne.sum() - use.sum()), p=p, n=int(len(x)), vol_kept_by_type=vk,
                nonempty=int(ne.sum()), s2_all=float(p_all.var(ddof=0)) if p_all.size > 1 else float('nan'),
                am_vol_kept=_frac(vam, vam.sum()), se_vol_kept=_frac(vse, vse.sum()),
                am_n_kept=_frac(cam, cam.sum()), se_n_kept=_frac(cse, cse.sum()),
                cell_n_median=float(np.median(cnt[use])) if use.any() else float('nan'))


#  ⚠ 2026-09-28 (Codex 3차 HBR3-05) — 판독기 (analyse) 는 이 함수를 더 쓰지 않는다: 계획 t₀ 가 없으면 앞 정착 프레임으로 조용히
#    대신했다.  scripts/check_contact_validity.py 가 아직 import 하므로 그대로 둔다.  판독기는 planned_t0 · _t0_exact 를 쓴다.
def _t0_frame(fr, steps_fill):
    """정착 끝 = 스텝 ≤ 2·steps_fill 인 마지막 프레임."""
    cand = [(st, p) for st, p in fr if st <= 2 * steps_fill]
    if not cand:
        raise SystemExit('⛔ 정착 구간 프레임이 없다 — 덤프 간격이 정착보다 길다')
    return cand[-1]


def planned_t0(plan):
    """계획 t₀ = 정착 끝 (회전 직전) 의 **계획 덤프 step** = ⌊2·steps_fill / dump_every⌋·dump_every.

    2026-09-28, Codex 3차 HBR3-05 — 판독기는 이 step 의 프레임을 **정확히** 요구한다 (옛 `_t0_frame` 처럼 "≤ 2F 인 마지막
    프레임" 을 고르면 계획 t₀ 가 없을 때 앞의 정착 프레임이 조용히 들어온다).
    덱 = `run 1` (삽입) · `run F` · `run F` (정착 두 번) · `run N` (회전) 이고 `dump … every` 가 `run 1` **뒤**에 정의되므로
    덤프는 every 의 배수 step 에만 떨어진다 ⇒ 정착 끝 (step 1 + 2F) 직전의 마지막 격자점.
    실측 (make_mixer_deck · 100,000 알 · cgf 151.4 · 시드 32452843): LC 8 바퀴 = F 192,668 · 간격 45,333 ⇒ t₀ 362,664
    (회전 시작 385,337 = 1 + 2F) · E0 (`--revolutions 0` → `run 0`) = 간격 1,000 ⇒ t₀ 385,000.  정상 입력에서 옛 규칙과 같은 프레임.
    ⚠ 1 + 2F 가 간격의 배수이면 그 step 의 덤프도 정착 끝이지만 옛 규칙 (≤ 2F) 과 같게 쓰지 않는다 (두 실제 덱은 해당 없음).
    """
    return (2 * plan['steps_fill'] // plan['dump_every']) * plan['dump_every']


def _t0_exact(fr, plan, run_dir, who):
    """계획 t₀ 프레임 → (step, path).  그 step 의 덤프가 **정확히 한 장** 있고 스키마 검사를 넘어야 한다 — 아니면 거부.

    2026-09-28, Codex 3차 HBR3-05 (t₀ 대체 — 평가 런 · E0 기준 둘 다) · HBR3-06 (머리 · 스키마 불량이 조용히 통과).
    ⛔ 앞의 정착 프레임으로 대신하지 않는다 — E0 기준 t₀ 가 빠진 프로브에서 옛 판은 S_R² 0.0069 → 0.0434 · M_final 0.45 → 0.529 를
      내고도 complete · flat · tech [] 였다.
    """
    t0 = planned_t0(plan)
    pre = plan['steps_total'] - plan['steps_run'] - 2 * plan['steps_fill']        # 정착 앞 step 수 (삽입 `run 1`)
    if t0 <= pre:
        raise SystemExit(f'⛔ {who} {run_dir}: 계획 t₀ step {t0} 가 정착 앞 (≤ {pre}) 이다 — 덤프 간격 {plan["dump_every"]} 이 '
                         f'정착 2·{plan["steps_fill"]} 보다 길다')
    hit = [p_ for st, p_ in fr if st == t0]
    if not hit:
        near = [st for st, _ in fr if st < t0][-3:]
        raise SystemExit(f'⛔ {who} {run_dir}: 계획 t₀ (정착 끝) step {t0} 의 덤프가 없다 — 앞 프레임 {near} 으로 대신하지 않는다 '
                         f'(Codex 3차 HBR3-05)')
    if len(hit) > 1:
        raise SystemExit(f'⛔ {who} {run_dir}: 계획 t₀ step {t0} 의 덤프가 {len(hit)} 장 — 어느 것이 참인지 모른다')
    probs = validate_frame(hit[0])
    if probs:
        raise SystemExit(f'⛔ {who} {run_dir}: 계획 t₀ step {t0} 프레임이 검사 (헤더 · 스키마) 를 못 넘는다 {probs[:3]} '
                         f'— 없는 것과 같게 거부한다 (Codex 3차 HBR3-06)')
    return t0, hit[0]


PROVENANCE_SCHEMA = 'mixing_provenance/1'


def _sha_file(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def frame_digest(files):
    """[[step, 파일명, sha256], …] → 묶음 sha256 (step 순 · 'step:파일명:sha' 줄).  launch_highbo.sh rest 관문이 같은 식으로 다시 계산한다."""
    import hashlib
    return hashlib.sha256(''.join(f'{int(a)}:{b}:{c}\n' for a, b, c in sorted(files, key=lambda t: int(t[0]))).encode()).hexdigest()


def frame_bundle(pairs):
    """[(step, 경로)] → dict(files=[[step, 파일명, sha256]…], sha256=묶음)."""
    files = [[int(s_), os.path.basename(p_), _sha_file(p_)] for s_, p_ in sorted(pairs, key=lambda t: int(t[0]))]
    return dict(files=files, sha256=frame_digest(files))


def verify_frames(post_dir, bundle):
    """증서의 프레임 묶음을 **이 폴더**의 파일로 다시 해시 → 어긋난 목록 (빈 목록 = 같다)."""
    bad = []
    for s_, name, h in (bundle or {}).get('files') or []:
        p_ = os.path.join(post_dir, os.path.basename(str(name)))
        if not os.path.isfile(p_) or _sha_file(p_) != h:
            bad.append((s_, name))
    if not bad and frame_digest((bundle or {}).get('files') or []) != (bundle or {}).get('sha256'):
        bad.append(('digest', None))
    return bad


def provenance_block(run_dir, ref_dir, args, used, ref_used):
    """★ 증서의 출처 (2026-09-28, Codex 4 차 HBR4-05) — 옛 증서는 run 경로 문자열 · smoke 불리언뿐이라 **다른 폴더 · 다른 칸
    규약 (2×2×1)** 의 실제 판독 결과가 16×16×4 첫 시드 증서로 rest 관문을 통과했다 (basename 만 비교 · mtime 으로 "다른 발사가
    아니다" 판정 — 복사 · 재판독이면 mtime 은 새로워진다).  이제 관문이 **불변 식별자**로 잇는다: 판독기 sha256 · 모든 규약 인자 ·
    평가 런 / E0 기준의 덱 sha256 · 판독한 프레임 (step · 파일명 · sha256) · 평가 런의 발사 봉인 sha256."""
    lr = os.path.join(run_dir, 'launch_record.json')
    return dict(schema=PROVENANCE_SCHEMA, tool_sha256=_sha_file(os.path.abspath(__file__)), args=dict(args),
                run=dict(name=os.path.basename(os.path.normpath(run_dir)), deck_sha256=_sha_file(os.path.join(run_dir, 'in.mixer')),
                         launch_record_sha256=_sha_file(lr) if os.path.isfile(lr) else None, frames=frame_bundle(used)),
                ref=dict(name=os.path.basename(os.path.normpath(ref_dir)), deck_sha256=_sha_file(os.path.join(ref_dir, 'in.mixer')),
                         frames=frame_bundle(ref_used)))


def bin_of(step, t0, steps_per_rev):
    """판독기의 bin 식 (analyse 의 _bin 과 같다) — ⌊(s − t₀)/바퀴 step + 1e-9⌋."""
    return int(np.floor((step - t0) / steps_per_rev + 1e-9))


def bin_window_files(post_dir, t0, steps_per_rev, dump_every, steps_total, bins):
    """그 bin 들의 **계획 덤프 격자** 와 지금 폴더의 파일 (판독기 파일 규칙 = measure_bed_aspect.frames) 을 맞춘다 (2026-09-30 · piece 3 · 4).
    → dict(lattice={step}, cur={step: [경로…]} (창 안 파일), dup=[step], off=[step] (창 안 격자 밖), miss=[step] (격자에 없음)).
    관문 (scripts/mixer_stage_gate.py rest-gate · mixer_smoke_blind 중간 판정의 사전조건) 이 **판독기와 같은 식** 으로 입력 집합을 다시 연다
    (Codex 5 차 HBR5-02 — 증서 목록 안 파일만 다시 해시하면 같은 step 복제 · 격자 밖 추가를 못 본다)."""
    want = {int(b_) for b_ in bins}
    lat = {s_ for s_ in range(int(t0), int(steps_total) + 1, int(dump_every)) if bin_of(s_, t0, steps_per_rev) in want}
    cur = {}
    for st, p_ in frames(post_dir) if os.path.isdir(post_dir) else []:
        if st >= t0 and bin_of(st, t0, steps_per_rev) in want:
            cur.setdefault(st, []).append(p_)
    return dict(lattice=lat, cur=cur, dup=sorted(s_ for s_, ps in cur.items() if len(ps) > 1),
                off=sorted(set(cur) - lat), miss=sorted(lat - set(cur)))


def e0_t0_stats(ref_dir, r_container, cells=8, x_cells=2, n_min=20, axis='x'):
    """E0 기준의 **계획 t₀** 프레임 통계 → (t₀ step, 경로, cell_stats) — analyse 가 S_R² 를 재는 바로 그 경로 (계획 t₀ 정확히 · 대체 금지).
    E0 진단 (강성 축 §4-c "S_R² 변화 ≤ 1 % (상대)") 이 판독기와 **같은 식** 으로 S_R² 를 잰다 (2026-09-30 · piece 1)."""
    rplan = deck_plan(os.path.join(ref_dir, 'in.mixer'))
    rst0, rp = _t0_exact(frames(os.path.join(ref_dir, 'post')), rplan, ref_dir, 'E0 기준')
    return rst0, rp, cell_stats(read_dump(rp), r_container, cells, x_cells, n_min, axis)


#: 프레임 행의 보조 진단 키 (analyse 와 bin_window_stats 가 같은 목록을 쓴다)
ROW_DIAG = ('am_vol_kept', 'se_vol_kept', 'am_n_kept', 'se_n_kept', 'nonempty', 'cell_n_median', 's2_all', 'vol_kept_by_type')

# ══ 중간 판정 한 번 (2026-09-30 · 강성 축 코드 선행조건 2 단계 piece 4) ═══════════════════════════════════════════════
#  사전등록 docs/reviews/mixer_highbo_stiffness_prereg_20260929.md §5-a (v2.5 · 결과 전 등록 — 값을 바꾸지 않는다):
#    "보는 시점 = 한 번: 확인 회전 12 런이 모두 4 바퀴 (판독기 계획 bin 3 창) 를 지난 때 … 두 번째 중간 판정은 없다"
#    "중간 문턱 (최종보다 엄격): E_ref 에서 bin 3 의 d_s = M(LC_ref,s) − M(LH_ref,s) 세 seed 가 모두 양수 ∧ Δ3 − u_mean ≥ 0.10 ∧
#     Δ3 − u_mean ≥ 3·(SE3 + u_SE) (… u 항은 §5 와 같은 식).  경계 비교는 §5 의 수치 규약 (여유 1e−12)."
#    "열람 범위: … 세 d_s 의 부호 · Δ3 · SE3 · 충족 여부 + d_soft(bin 3) · q(bin 3) 의 값 보고용 요약뿐 · M(t) 곡선 전체와 다른 bin 은 최종까지 봉인"
#  이 모듈은 **계산만** 한다 (bin 3 창 · 판정선 · 요약).  열람 · 한 번 규칙 · 봉인 · 허용목록 투영은 scripts/mixer_smoke_blind.py --interim.
INTERIM_BIN = 3            # "4 바퀴 (판독기 계획 bin 3 창)"
INTERIM_MID = 0.10         # "Δ3 − u_mean ≥ 0.10"
INTERIM_K_SE = 3.0         # "Δ3 − u_mean ≥ 3·(SE3 + u_SE)" — 최종 판정선의 2·SE 대신 3·SE
INTERIM_TOL = 1e-12        # "경계 비교는 §5 의 수치 규약 (여유 1e−12)" — 부동소수 비교 규약 (물리 허용치 아님)
#  바닥 검사 = 본 캠페인 결정 (b) (mixer_layered_prereg_20260921.md §4-1 · 모체 mixer_highbo_prereg_20260927.md §5-5): 거친 칸 8×8×2 · 문턱 5
FLOOR_CELLS, FLOOR_X_CELLS, FLOOR_MIN = 8, 2, 5.0


def bin_window_stats(run_dir, ref_dir, r_container, bin_, cells=8, x_cells=2, n_min=20, axis='x'):
    """한 bin 의 **계획 덤프 격자만** 으로 M → dict (2026-09-30 · piece 4 · §5-a 중간 판정의 판독).

    읽는 파일 = 평가 런의 계획 t₀ (S₀²) · 그 bin 의 계획 격자 프레임 · E0 기준의 계획 t₀ (S_R²) — **이것뿐**이다.  다른 bin 의 프레임은
    열지 않는다 (§5-a "다른 bin 은 최종까지 봉인" — 계산하지 않은 값은 새지 않는다 · 셀프테스트 ㉚ 이 연 파일 집합을 고정한다).
    M 의 식 · t₀ · S_R² 경로 · 칸 규약 · bin 식은 analyse 와 같다 (그 bin 이 완전하면 값 = analyse 의 by_rev[bin].M_mean · ㉚).

    fail-closed (값 없음 = M_bin None · tech 에 사유):
      ① 그 bin 의 계획 격자가 비었다 (계획 바퀴 수 밖)
      ② 창 입력 집합이 판독기 규칙에 안 맞는다 — 결손 (= 아직 그 bin 을 지나지 않음) · 같은 step 중복 · 격자 밖 (bin_window_files — 관문과 같은 식)
         ⇒ **bin 프레임 · E0 를 열지 않고** 돌아간다 (M 미계산)
      ③ 창 프레임 형식 검사 실패 (validate_frame) — 이때도 M 을 계산하지 않는다
      ④ 비유한 M
    S₀² ≤ S_R² 면 analyse 와 같이 SystemExit (M 정의 불가 — §24-4).
    반환 키: run · ref · bin · t0_step · plan · expected · n · complete · M_bin · M_sd · n_nonfinite · S0 · SR · rows · qc_repr · tech · provenance ·
    args.  ⚠ M_bin · rows · S0 · SR 은 **결과**다 — 화면 · 증서에 내는 것은 호출자 (mixer_smoke_blind --interim) 의 허용목록 투영뿐이다."""
    plan = deck_plan(os.path.join(run_dir, 'in.mixer'))
    post = os.path.join(run_dir, 'post')
    st0, p0 = _t0_exact(frames(post), plan, run_dir, '평가 런')
    spr, de = plan['steps_per_rev'], plan['dump_every']
    b_ = int(bin_)
    w = bin_window_files(post, st0, spr, de, plan['steps_total'], (b_,))
    lat = sorted(w['lattice'])
    args = dict(cells=int(cells), x_cells=int(x_cells), n_min=int(n_min), axis=str(axis), r_container=float(r_container))
    out = dict(run=run_dir, ref=ref_dir, bin=b_, t0_step=st0, plan=plan, expected=len(lat), n=0, complete=False, M_bin=None, M_sd=None,
               n_nonfinite=None, S0=None, SR=None, rows=[], qc_repr=None, tech=[], provenance=None, args=args)
    tech = out['tech']
    if not lat:
        n_revs = int(round(plan['steps_run'] / spr))
        tech.append(f'bin {b_} 의 계획 덤프 격자가 비었다 (덱의 계획 {n_revs} 바퀴 = bin 0–{n_revs - 1}) — 값 없음')
        return out
    if w['miss'] or w['dup'] or w['off']:
        if w['miss']:
            tech.append(f'bin {b_} 결손 {len(w["miss"])}/{len(lat)} 프레임 (step {w["miss"][:4]}{"…" if len(w["miss"]) > 4 else ""}) — '
                        '아직 그 bin 을 지나지 않았거나 덤프가 빠졌다')
        if w['dup']:
            tech.append(f'bin {b_} 에 같은 step 의 덤프가 둘 이상 (step {w["dup"][:4]}) — 어느 것이 참인지 모른다')
        if w['off']:
            tech.append(f'bin {b_} 에 계획 덤프 격자 밖 step {w["off"][:4]} (t₀ {st0} + k·{de})')
        return out                                                  # ★ M 미계산 — bin 프레임 · E0 를 열지 않는다
    bad = {}
    for s_ in lat:
        pr_ = validate_frame(w['cur'][s_][0])
        if pr_:
            bad[s_] = pr_
    if bad:
        tech += [f'step {s_}: 프레임 검사 (헤더 · 스키마) 실패 {pr_[:3]} — 값 없음' for s_, pr_ in sorted(bad.items())]
        return out
    kw = dict(cells=cells, x_cells=x_cells, n_min=n_min, axis=axis)
    c0 = cell_stats(read_dump(p0), r_container, **kw)
    rst0, rp, cR = e0_t0_stats(ref_dir, r_container, **kw)
    s0, sR = c0['s2'], cR['s2']
    if not (s0 > sR):
        raise SystemExit(f'⛔ S₀² ({s0:.4g}) ≤ S_R² ({sR:.4g}) — 층상 시작이 아니거나 기준이 틀렸다.  '
                         f'M 을 정의할 수 없다 (§24-4 바닥 검사 실패)')
    rows = []
    for s_ in lat:
        cs = cell_stats(read_dump(w['cur'][s_][0]), r_container, **kw)
        row = dict(step=s_, rev=(s_ - st0) / spr, s2=cs['s2'], M=(s0 - cs['s2']) / (s0 - sR), cells_used=cs['used'],
                   cells_dropped=cs['dropped'], n=cs['n'])
        row.update({k: cs[k] for k in ROW_DIAG})
        rows.append(row)
    v = [r_['M'] for r_ in rows]
    nonfin = sum(1 for x in v if not np.isfinite(x))
    out.update(S0=s0, SR=sR, rows=rows, n=len(rows), n_nonfinite=nonfin, qc_repr=qc_representativeness(rows),
               provenance=provenance_block(run_dir, ref_dir, args, [(st0, p0)] + [(s_, w['cur'][s_][0]) for s_ in lat], [(rst0, rp)]))
    if nonfin:
        tech.append(f'bin {b_} 에 비유한 M {nonfin} 프레임 — 값 없음')
        return out
    out.update(complete=True, M_bin=float(np.mean(v)), M_sd=float(np.std(v, ddof=1)) if len(v) > 1 else 0.0)
    return out


def t0_floor(run_dir, ref_dir, r_container, cells=FLOOR_CELLS, x_cells=FLOOR_X_CELLS, n_min=20, axis='x', thr=FLOOR_MIN):
    """바닥 검사 (본 캠페인 결정 (b) — 8×8×2 에서 S₀²/S_R² ≥ 5) → dict(ratio, pass, s0, sR, cells, x_cells, min, t0_step, ref_t0_step).
    읽는 파일 = 평가 런의 계획 t₀ · E0 기준의 계획 t₀ **두 장** (M(t) 와 무관 — 회전 뒤 프레임을 열지 않는다).  S_R² = 0 이고 S₀² > 0 이면 비 = ∞ (통과) ·
    비유한 · 0/0 은 불합격 (fail-closed)."""
    plan = deck_plan(os.path.join(run_dir, 'in.mixer'))
    st0, p0 = _t0_exact(frames(os.path.join(run_dir, 'post')), plan, run_dir, '평가 런')
    kw = dict(cells=cells, x_cells=x_cells, n_min=n_min, axis=axis)
    s0 = cell_stats(read_dump(p0), r_container, **kw)['s2']
    rst0, _rp, cR = e0_t0_stats(ref_dir, r_container, **kw)
    sR = cR['s2']
    if np.isfinite(s0) and np.isfinite(sR) and sR > 0:
        ratio = float(s0 / sR)
    elif np.isfinite(s0) and s0 > 0 and sR == 0:
        ratio = float('inf')
    else:
        ratio = float('nan')
    return {'ratio': ratio, 'pass': bool(ratio == ratio and ratio >= thr), 's0': float(s0), 'sR': float(sR), 'cells': int(cells),
            'x_cells': int(x_cells), 'min': float(thr), 't0_step': st0, 'ref_t0_step': rst0}


def _seed_map(m, S, what, nonneg=False):
    """{seed: 값} (키 = int 또는 십진 문자열) → 등록 seed 순서의 float 목록.  seed 집합이 다르거나 · 값이 유한 실수가 아니거나 (불리언 거부) ·
    (nonneg) 음수면 ValueError — fail-closed (빠진 seed 를 0 으로 채우지 않는다)."""
    import numbers
    if not isinstance(m, dict):
        raise ValueError(f'{what} 이 {{seed: 값}} 이 아니다 ({type(m).__name__})')
    nm = {}
    for k, v in m.items():
        try:
            ik = int(k)
        except (TypeError, ValueError):
            raise ValueError(f'{what} 의 seed 키 {k!r} 가 정수가 아니다')
        if ik in nm:
            raise ValueError(f'{what} 에 seed {ik} 가 두 번 있다')
        nm[ik] = v
    if sorted(nm) != sorted(S):
        raise ValueError(f'{what} 의 seed {sorted(nm)} ≠ 등록 {sorted(S)}')
    out = []
    for s_ in S:
        v = nm[s_]
        if isinstance(v, (bool, np.bool_)) or not isinstance(v, numbers.Real) or not np.isfinite(float(v)):
            raise ValueError(f'{what}[{s_}] = {v!r} — 유한 실수가 아니다')
        if nonneg and float(v) < 0:
            raise ValueError(f'{what}[{s_}] = {v!r} < 0')
        out.append(float(v))
    return out


def _seeds3(seeds):
    S = tuple(int(s_) for s_ in seeds)
    if len(S) != 3 or len(set(S)) != 3:
        raise ValueError(f'seed 는 등록 셋 (n = 3 · 서로 다름) 이어야 한다: {seeds!r}')
    return S


def interim_rule(d_ref, eps, seeds):
    """§5-a 중간 판정선 → dict (seed 별 **값은 담지 않는다** — 부호 · Δ3 · SE3 · u 항 · 조건 · 충족만).

      d_ref  {seed: d_s} — d_s = M_bin3(LC_ref, s) − M_bin3(LH_ref, s) (같은 강성 · 같은 seed 의 E0 로 정규화)
      eps    {seed: ε_s} — 결과 전 등록된 seed 별 확정 수치 오차 상한 (bin 3 용 · §5 "판독기 반올림 · 등록된 결정론적 항만")
      seeds  등록 holdout 세 seed (순서 = 보고 순서)
    Δ3 = mean(d) · SE3 = sd(d, ddof 1)/√n · u_mean = mean(ε) · u_SE = √(Σε²)/√(n(n−1)) (§5 식 그대로) ·
    충족 = 모두 양수 (**엄격** d > 0 — 0 은 양수가 아니다 · 여유를 주지 않는다) ∧ Δ3 − u_mean ≥ 0.10 − 1e−12 ∧ Δ3 − u_mean ≥ 3·(SE3 + u_SE) − 1e−12.
    입력이 등록 seed 셋과 다르거나 비유한 · ε 음수/불리언이면 ValueError (fail-closed)."""
    import math
    S = _seeds3(seeds)
    d = _seed_map(d_ref, S, 'd_ref')
    e = _seed_map(eps, S, 'ε', nonneg=True)
    n = len(S)
    delta = math.fsum(d) / n
    se = math.sqrt(math.fsum((x - delta) ** 2 for x in d) / (n - 1)) / math.sqrt(n)
    u_mean = math.fsum(e) / n
    u_se = math.sqrt(math.fsum(x * x for x in e)) / math.sqrt(n * (n - 1))
    lhs = delta - u_mean
    rhs_se = INTERIM_K_SE * (se + u_se)
    cond = dict(all_positive=bool(all(x > 0 for x in d)), mid=bool(lhs >= INTERIM_MID - INTERIM_TOL),
                se=bool(lhs >= rhs_se - INTERIM_TOL))
    return dict(schema='mixer_interim_rule/1', bin=INTERIM_BIN, seeds=[str(s_) for s_ in S], n=n,
                signs={str(s_): ('+' if x > 0 else ('−' if x < 0 else '0')) for s_, x in zip(S, d)},
                delta3=delta, se3=se, u_mean=u_mean, u_se=u_se, lhs=lhs, mid=INTERIM_MID, k_se=INTERIM_K_SE, rhs_se=rhs_se, tol=INTERIM_TOL,
                cond=cond, met=bool(all(cond.values())),
                rule='세 seed d_s > 0 ∧ Δ3 − u_mean ≥ 0.10 ∧ Δ3 − u_mean ≥ 3·(SE3 + u_SE) (경계 여유 1e−12 · §5-a)')


def value_summary(vals, seeds):
    """seed 별 값 → dict(mean, se, n) — **세 seed 가 다 있고 유한할 때만** (아니면 None · 부분 요약을 만들지 않는다).
    §5-a 의 d_soft(bin 3) · q(bin 3) '값 보고용 요약' 에 쓴다 (판정 아님)."""
    import math
    try:
        S = _seeds3(seeds)
        v = _seed_map(vals, S, 'value')
    except ValueError:
        return None
    n = len(v)
    mean = math.fsum(v) / n
    return dict(mean=mean, se=math.sqrt(math.fsum((x - mean) ** 2 for x in v) / (n - 1)) / math.sqrt(n), n=n)


def analyse(run_dir, ref_dir, r_container, cells=8, x_cells=2, n_min=20, axis='x'):
    deck = os.path.join(run_dir, 'in.mixer')
    plan = deck_plan(deck)
    fr = frames(os.path.join(run_dir, 'post'))
    if not fr:
        raise SystemExit(f'⛔ {run_dir}: 덤프가 없다')
    kw = dict(cells=cells, x_cells=x_cells, n_min=n_min, axis=axis)
    #  ★ t₀ = **계획** 정착 끝 덤프 step 그 자체 (2026-09-28, Codex 3차 HBR3-05) — 없거나 · 둘이거나 · 검사 실패면 거부.
    #    옛 `_t0_frame` ("≤ 2F 인 마지막 프레임") 은 계획 t₀ 가 빠지면 앞의 정착 프레임으로 조용히 대신했다.
    st0, p0 = _t0_exact(fr, plan, run_dir, '평가 런')
    c0 = cell_stats(read_dump(p0), r_container, **kw)
    s0, n0 = c0['s2'], c0['used']
    #  무작위 기준 — 균일 삽입 런의 **같은 위치**(그 덱의 계획 정착 끝) 프레임 · 같은 규칙 (e0_t0_stats — E0 진단과 같은 경로)
    rst0, rp, cR = e0_t0_stats(ref_dir, r_container, **kw)
    sR, nR = cR['s2'], cR['used']
    if not (s0 > sR):
        raise SystemExit(f'⛔ S₀² ({s0:.4g}) ≤ S_R² ({sR:.4g}) — 층상 시작이 아니거나 기준이 틀렸다.  '
                         f'M 을 정의할 수 없다 (§24-4 바닥 검사 실패)')
    #  민감도 (판정에 안 씀): 빈 칸만 뺀 모든 칸의 M — 버린 칸이 분리를 숨기는지 보이게
    s0a, sRa = c0['s2_all'], cR['s2_all']
    DIAG = ROW_DIAG                                          # bin_window_stats 와 같은 목록
    #  ★ 행 (= M · SD · 평탄 · QC 에 들어가는 프레임) = **계획 덤프 격자** (t₀ + k·dump_every ≤ 덱 끝) 위 · step 당 한 장 ·
    #    스키마 검사 (measure_bed_aspect.validate_frame) 통과 (2026-09-28, Codex 3차 HBR3-05 · 06).  나머지 — 격자 밖 · 같은 step
    #    둘 이상 · 머리 없음 · 머리 step ≠ 파일명 · 소수 type · id 없음 … — 는 계산에 **넣지 않고** tech (bin 0 이면 tech_smoke 도) 에
    #    남긴다.  옛 판은 격자 밖 7301 을 bin 7 에 넣어 26/25 프레임 · complete · tech [] · M_final 0.45 → 0.4327 을 냈고,
    #    머리가 없는 프레임은 dump_header 가 (None, None) 을 돌려 검사 없이 지나갔다 (소수 type 은 정수로 깎였다).
    de, spr = plan['dump_every'], plan['steps_per_rev']
    lat = set(range(st0, plan['steps_total'] + 1, de))

    def _bin(s_):
        return bin_of(s_, st0, spr)                      # 같은 식 (bin_of — 관문 · 중간 판정이 같은 함수를 쓴다)
    by_step = {}
    for st, pth in fr:
        if st >= st0:
            by_step.setdefault(st, []).append(pth)
    dups = sorted(s_ for s_, ps_ in by_step.items() if len(ps_) > 1)
    rows, excl = [], {}                                  # excl: step → 계산에서 뺀 사유 (같은 step 중복은 dups 로 따로)
    for st, ps_ in sorted(by_step.items()):
        if st not in lat:
            excl[st] = f'계획 덤프 격자 밖 (t₀ {st0} + k·{de} ≤ 덱 끝 {plan["steps_total"]})'
            continue
        if len(ps_) > 1:
            continue                                     # 어느 쪽이 참인지 모른다 — 아래 dups 표지
        if st == st0:
            cs = c0                                      # t₀ 는 _t0_exact 가 이미 검사했다
        else:
            probs = validate_frame(ps_[0])
            if probs:
                excl[st] = f'프레임 검사 (헤더 · 스키마) 실패 {probs[:3]}'
                continue
            cs = cell_stats(read_dump(ps_[0]), r_container, **kw)
        s2 = cs['s2']
        rev = (st - st0) / spr
        row = dict(step=st, rev=rev, s2=s2, M=(s0 - s2) / (s0 - sR), cells_used=cs['used'], cells_dropped=cs['dropped'], n=cs['n'])
        row.update({k: cs[k] for k in DIAG})
        row['M_all'] = (s0a - cs['s2_all']) / (s0a - sRa) if s0a > sRa else float('nan')
        rows.append(row)
    #  바퀴별 요약
    by_rev = {}
    for r_ in rows:
        k = int(np.floor(r_['rev'] + 1e-9))
        by_rev.setdefault(k, []).append(r_)
    revs = {}
    for k, rr in sorted(by_rev.items()):
        v = [r_['M'] for r_ in rr]
        fin = [x for x in v if np.isfinite(x)]
        types_ = sorted({t_ for r_ in rr for t_ in r_['vol_kept_by_type']})
        revs[k] = dict(M_mean=float(np.mean(v)), M_sd=float(np.std(v, ddof=1)) if len(v) > 1 else 0.0, n=len(v),
                       n_nonfinite=len(v) - len(fin),
                       M_all_mean=float(np.mean([r_['M_all'] for r_ in rr])),
                       s2_mean=float(np.mean([r_['s2'] for r_ in rr])),
                       am_vol_kept_mean=float(np.mean([r_['am_vol_kept'] for r_ in rr])),
                       se_vol_kept_mean=float(np.mean([r_['se_vol_kept'] for r_ in rr])),
                       vol_kept_min=float(min(min(r_['am_vol_kept'], r_['se_vol_kept']) for r_ in rr)),
                       vol_kept_min_by_type={t_: float(min(r_['vol_kept_by_type'][t_] for r_ in rr)) for t_ in types_},
                       vol_kept_mean_by_type={t_: float(np.mean([r_['vol_kept_by_type'][t_] for r_ in rr])) for t_ in types_},
                       qc=qc_representativeness(rr),
                       cells_dropped_frac=float(np.mean([r_['cells_dropped'] / max(r_['nonempty'], 1) for r_ in rr])))
    last_k = max(revs)
    #  ★ 등록 최종값 (2026-09-27, Codex HB-05) — 덱의 계획 바퀴 수의 **마지막 완전 바퀴**.  옛 `M_final` 은 마지막 bin 이라
    #    **부분 bin** (2–12 프레임, 중간 판독) 일 수 있어 최종값으로 쓰면 안 된다 (셀프테스트 ⑭ · 계획 끝을 넘은 덤프는 ⑬b).
    #  ★ 완전 = **계획 덤프 격자** (t₀ 부터 덱 끝까지 dump_every 간격) 의 그 bin step 이 **다** 있다 (2026-09-27 저녁,
    #    Codex HBR2-04 — 옛 "뒤 bin 이 있으면 완전" 은 직전 bin 이 2/25 프레임이어도 flat=true 를 냈다 · 셀프테스트 ⑰).
    fpr = plan['steps_per_rev'] / plan['dump_every']
    last_rev = rows[-1]['rev']
    n_revs = int(round(plan['steps_run'] / plan['steps_per_rev']))
    present = {r_['step'] for r_ in rows}
    exp_bin = {}
    for s_ in range(st0, plan['steps_total'] + 1, plan['dump_every']):
        exp_bin.setdefault(int(np.floor((s_ - st0) / plan['steps_per_rev'] + 1e-9)), set()).add(s_)

    def _missing(k):
        return sorted(exp_bin.get(k, set()) - present)

    def _complete(k):
        return k in exp_bin and not _missing(k)
    #  dump_gaps 는 옛 판 그대로 t₀ 이후 **있는 파일 전부** (계산에서 뺀 프레임 포함) 의 간격이다 — 계산에 쓴 행이 아니다
    steps = [st for st, _ in fr if st >= st0]
    gaps = [(a_, b_) for a_, b_ in zip(steps, steps[1:]) if b_ - a_ != plan['dump_every']]
    tech = []
    planned = None
    if n_revs >= 1:
        fb = n_revs - 1
        ok_ = _complete(fb)
        planned = dict(n_revs=n_revs, final_bin=fb, frames_per_rev=fpr, complete=ok_,
                       n=revs[fb]['n'] if fb in revs else 0, expected=len(exp_bin.get(fb, ())), missing=_missing(fb)[:8],
                       M_final=revs[fb]['M_mean'] if ok_ else None, M_final_sd=revs[fb]['M_sd'] if ok_ else None,
                       prev_bin=fb - 1, prev_complete=_complete(fb - 1) if fb >= 1 else None, flat=None,
                       qc_repr=revs[fb]['qc'] if fb in revs else None)
        if ok_ and fb >= 1 and _complete(fb - 1):
            planned['flat'] = bool(abs(revs[fb]['M_mean'] - revs[fb - 1]['M_mean']) <= revs[fb]['M_sd'])
        if not ok_:
            tech.append(f'미완주 — 계획 {n_revs} 바퀴의 마지막 bin {fb} 이 완전하지 않다 (있음 {planned["n"]}/{planned["expected"]} · '
                        f'마지막 프레임 rev {last_rev:.3f} · 결손 step {_missing(fb)[:4]}{"…" if len(_missing(fb)) > 4 else ""})')
        elif fb >= 1 and not _complete(fb - 1):
            tech.append(f'평탄 비교 불가 — 직전 bin {fb - 1} 결손 {len(_missing(fb - 1))}/{len(exp_bin.get(fb - 1, ()))} 프레임 '
                        f'(step {_missing(fb - 1)[:4]}…) — 최종값은 보고하되 평탄 증서 (flat) 는 발행하지 않는다')
        if ok_ and revs[fb]['n_nonfinite']:
            tech.append(f'최종 bin {fb} 에 비유한 M {revs[fb]["n_nonfinite"]} 프레임')
    ex_msg = {s_: f'step {s_}: {w_} — 계산 (M · SD · 평탄 · QC) 에서 뺐다' for s_, w_ in sorted(excl.items())}
    tech += list(ex_msg.values())
    if dups:
        tech.append(f'같은 step 의 덤프가 둘 이상 ({dups[:4]}) — 그 step 은 계산에서 뺐다')
    #  ★ 스모크 창 (2026-09-27 저녁, Codex HBR2-02) — 고-Bo 사전등록 §8 은 **첫 완전 bin 0** 만 본다.  전체 미완주는
    #    스모크에서 예상되는 상태라 `tech` (최종 창) 에만 두고, bin 0 안의 결손 · 비유한 · 뺀 프레임 (격자 밖 · 헤더 · 스키마 —
    #    2026-09-28 HBR3-05 · 06) 만 `tech_smoke` 에 넣는다.
    b0 = exp_bin.get(0, set())
    smoke = dict(bin=0, expected=len(b0), present=len(b0 & present), complete=_complete(0) if b0 else False,
                 n=revs[0]['n'] if 0 in revs else 0, M_mean=revs[0]['M_mean'] if 0 in revs else None,
                 qc_repr=revs[0]['qc'] if 0 in revs else None, tech_smoke=[])
    if b0 and not _complete(0):
        smoke['tech_smoke'].append(f'bin 0 결손 {len(_missing(0))}/{len(b0)} 프레임 (step {_missing(0)[:4]}{"…" if len(_missing(0)) > 4 else ""})')
    if 0 in revs and revs[0]['n_nonfinite']:
        smoke['tech_smoke'].append(f'bin 0 에 비유한 M {revs[0]["n_nonfinite"]} 프레임')
    smoke['tech_smoke'] += [m_ for s_, m_ in ex_msg.items() if _bin(s_) == 0]
    if any(d_ in b0 for d_ in dups):
        smoke['tech_smoke'].append('bin 0 에 같은 step 의 덤프가 둘 이상')
    prov = provenance_block(run_dir, ref_dir, dict(cells=int(cells), x_cells=int(x_cells), n_min=int(n_min), axis=str(axis),
                                                   r_container=float(r_container)),
                            [(r_['step'], by_step[r_['step']][0]) for r_ in rows], [(rst0, rp)])
    return dict(run=run_dir, ref=ref_dir, provenance=prov, plan=plan, t0_step=st0, S0=s0, SR=sR,
                cells_t0=n0, cells_ref=nR, rows=rows, by_rev=revs,
                M_final=revs[last_k]['M_mean'], M_final_sd=revs[last_k]['M_sd'], final_rev=last_k,
                M_t0=rows[0]['M'], planned=planned, smoke=smoke, tech=tech, dump_gaps=gaps,
                lattice=dict(dump_every=plan['dump_every'], t0=st0, end=plan['steps_total'],
                             expected_by_bin={k: len(v) for k, v in sorted(exp_bin.items())},
                             present_by_bin={k: len(v & present) for k, v in sorted(exp_bin.items())},
                             excluded=dict(sorted(excl.items())), duplicates=dups),
                S0_all=s0a, SR_all=sRa,
                diag_t0={k: c0[k] for k in DIAG + ('used', 'dropped')},
                diag_ref={k: cR[k] for k in DIAG + ('used', 'dropped')})


def report(res):
    print(f"{res['run']}")
    print(f"   t0 step {res['t0_step']} · S₀² {res['S0']:.5f} ({res['cells_t0']} 칸) · S_R² {res['SR']:.5f} "
          f"({res['cells_ref']} 칸, ref {os.path.basename(res['ref'].rstrip('/'))}) · M(t0) {res['M_t0']:+.3f}")
    d0 = res['diag_t0']
    print(f"   t0 보조: 유지 부피 AM {d0['am_vol_kept']:.3f} · SE {d0['se_vol_kept']:.3f} · 버린 칸 {d0['dropped']}/{d0['nonempty']} "
          f"· 칸당 입자 중앙 {d0['cell_n_median']:.0f} · 전 칸 S₀² {res['S0_all']:.5f} / S_R² {res['SR_all']:.5f}")
    for k, v in res['by_rev'].items():
        print(f"   바퀴 {k:2d}  M {v['M_mean']:6.3f} ± {v['M_sd']:.3f}  (프레임 {v['n']})"
              f"   [유지 부피 AM {v['am_vol_kept_mean']:.3f} · SE {v['se_vol_kept_mean']:.3f} · 버린 칸 "
              f"{v['cells_dropped_frac']*100:.1f} % · 전 칸 M {v['M_all_mean']:.3f}]")
    print(f"   (옛 키) M_final = 마지막 bin {res['final_rev']} ({res['by_rev'][res['final_rev']]['n']} 프레임 — 부분일 수 있다) "
          f"= {res['M_final']:.3f} ± {res['M_final_sd']:.3f}")
    pl = res.get('planned')
    if pl:
        if pl['complete']:
            print(f"   ★ 등록 최종값 (계획 {pl['n_revs']} 바퀴 · bin {pl['final_bin']} · {pl['n']} 프레임) = "
                  f"{pl['M_final']:.3f} ± {pl['M_final_sd']:.3f}   평탄 {pl['flat']}")
        else:
            print(f"   ★ 등록 최종값 — 없음 (bin {pl['final_bin']} 미완 · {pl['n']} 프레임)")
    pl = res.get('planned')
    if pl and pl.get('qc_repr'):
        q = pl['qc_repr']
        print(f"   D-2 부피 누락 QC (등록 bin): {'통과' if q['pass'] else '⚠ 미달 — 선택-셀 M · 전체-bed 결론 제한'} "
              f"(평균 AM {q['am_mean']:.3f} · SE {q['se_mean']:.3f} · 프레임별 최솟값 {q['min_by_type']})")
    sm = res.get('smoke')
    if sm:
        print(f"   스모크 창 (bin 0): {sm['present']}/{sm['expected']} 프레임 · M {sm['M_mean'] if sm['M_mean'] is None else round(sm['M_mean'], 3)}"
              + (''.join(f'  ⚠ {t}' for t in sm['tech_smoke']) if sm['tech_smoke'] else '  ✓'))
    for t in res.get('tech', []):
        print(f"   ⚠ {t}")


# ───────────────────────────── selftest ─────────────────────────────
def _selftest():                                              # noqa: C901
    import tempfile
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)
        print(('  PASS  ' if cond else '  FAIL  ') + name)

    rng = np.random.default_rng(7)
    R = 0.02

    def cloud(n, layered, seg_frac=1.0, r_am=0.0012, r_se=0.0003):
        """반지름 R 안에 n 개 — layered=True 면 AM 은 z<0, SE 는 z>0 (seg_frac 만큼)."""
        th = rng.uniform(0, 2 * np.pi, n); rr = R * 0.9 * np.sqrt(rng.uniform(0, 1, n))
        y, z = rr * np.cos(th), rr * np.sin(th)
        x = rng.uniform(-0.007, 0.007, n)
        t = np.where(rng.uniform(0, 1, n) < 0.3, 1, 3)
        if layered:
            flip = rng.uniform(0, 1, n) < seg_frac
            z = np.where(flip, -np.abs(z) * (t == 1) + np.abs(z) * (t == 3), z)
        r = np.where(t == 1, r_am, r_se)
        return dict(id=np.arange(n) + 1., type=t.astype(float), mol=-np.ones(n),
                    x=x, y=y, z=z, radius=r)

    def write_dump(path, D):
        n = len(D['x'])
        st_ = int(re.search(r'_(\d+)\.', os.path.basename(path)).group(1))     # 헤더 step = 파일명 step (실제 LIGGGHTS 와 같이)
        with open(path, 'w') as f:
            f.write(f'ITEM: TIMESTEP\n{st_}\nITEM: NUMBER OF ATOMS\n{n}\nITEM: BOX BOUNDS pp pp pp\n'
                    '-1 1\n-1 1\n-1 1\nITEM: ATOMS id type mol x y z radius\n')
            for i in range(n):
                f.write(f"{int(D['id'][i])} {int(D['type'][i])} {int(D['mol'][i])} "
                        f"{D['x'][i]:.6g} {D['y'][i]:.6g} {D['z'][i]:.6g} {D['radius'][i]:.6g}\n")

    #  ⚠ 2026-09-28 (Codex 3차 HBR3-05) — 판독기는 **계획 덤프 격자** (t₀ + k·간격 ≤ 덱 끝) 위의 프레임만 쓴다.  옛 고정구
    #    (간격 500 · 덱 끝 6001) 에서는 9600 · 249600 이 격자 밖이었다 ⇒ 간격 100 · 회전 248000 으로 격자 위에 둔다 (프레임 · 값 · 목적 그대로).
    DECK = ('timestep 1e-6\nrun 1\nrun 1000\nrun 1000\n'
            'dump dmp all custom 100 post/mix_*.liggghts id type mol x y z radius\n'
            'fix mvD all move/mesh mesh Drum rotate origin 0 0 0 axis 1. 0. 0. period 1.0\n'
            'run 248000\n')

    seg = cloud(6000, True); mix = cloud(6000, False)
    s_seg, nu_seg, _, _ = cell_variance(seg, R)
    s_mix, nu_mix, _, _ = cell_variance(mix, R)
    chk('① 완전 분리 침대의 S² 가 무작위 침대보다 훨씬 크다', s_seg > 5 * s_mix and nu_seg > 20)
    half = cloud(6000, True, seg_frac=0.5)
    s_half, _, _, _ = cell_variance(half, R)
    chk('② 반만 분리하면 S² 가 그 사이에 온다', s_mix < s_half < s_seg)

    #  부피가중 vs 개수가중이 실제로 다른 경우 (AM 이 크고 적다)
    p_num = None
    D = seg
    t = D['type'].astype(int); am = np.isin(t, AM_TYPES)
    chk('③ AM 개수분율 ≪ 부피분율 (개수로 재면 SE 가 지배한다)',
        am.mean() < 0.35 and ((4/3*np.pi*D['radius']**3)[am].sum() /
                              (4/3*np.pi*D['radius']**3).sum()) > 0.8)

    with tempfile.TemporaryDirectory() as td:
        run = os.path.join(td, 'run'); ref = os.path.join(td, 'ref')
        for d in (run, ref):
            os.makedirs(os.path.join(d, 'post'))
            open(os.path.join(d, 'in.mixer'), 'w').write(DECK)
        #  run: t0(step 2000) 층상 → 점점 섞임 (프레임 9600 이 249600 뒤에 오게 이름을 둔다: 숫자순 검사)
        seq = [(2000, 1.0), (2500, 0.75), (3000, 0.5), (4000, 0.25), (9600, 0.1)]
        for st, f in seq:
            write_dump(os.path.join(run, 'post', f'mix_{st}.liggghts'), cloud(6000, True, seg_frac=f))
        #  마지막 프레임 = 기준 구름과 **동일** ⇒ 공식상 M_final 이 정확히 1 이어야 한다
        _refc = cloud(6000, False)
        write_dump(os.path.join(run, 'post', 'mix_249600.liggghts'), _refc)
        write_dump(os.path.join(ref, 'post', 'mix_2000.liggghts'), _refc)
        res = analyse(run, ref, R)
        chk('④ t0 = 정착 끝(step 2000) 프레임이고 M(t0) ≈ 0', res['t0_step'] == 2000 and abs(res['M_t0']) < 1e-9)
        Ms = [r_['M'] for r_ in res['rows']]
        #  단조성은 프레임마다 새 추첨이라 잡음 허용(−0.05); 마지막은 기준과 같은 구름이라 정확히 1
        chk('⑤ M 이 시간에 따라 (잡음 안에서) 증가하고, 기준과 같은 구름이면 정확히 1',
            all(np.diff(Ms) > -0.05) and Ms[-1] > Ms[0] + 0.5 and abs(Ms[-1] - 1.0) < 1e-9)
        chk('⑥ 프레임을 숫자순으로 읽는다 (249600 이 9600 뒤)', res['rows'][-1]['step'] == 249600)
        chk('⑦ 바퀴 경계 = period/dt (1e6 스텝) 로 계산돼 전부 0 바퀴째다', res['final_rev'] == 0
            and res['plan']['steps_per_rev'] == 1e6)
        #  빈 칸 보고
        _, nu, nd, _ = cell_variance(cloud(300, False), R, n_min=20)
        chk('⑧ 입자가 적으면 칸을 버리고 **개수를 보고**한다 (조용히 안 넘긴다)', nd > 0 and nu < 128)
        #  바닥 검사: 층상이 아닌 런을 주면 거부
        run2 = os.path.join(td, 'run2'); os.makedirs(os.path.join(run2, 'post'))
        open(os.path.join(run2, 'in.mixer'), 'w').write(DECK)
        write_dump(os.path.join(run2, 'post', 'mix_2000.liggghts'), cloud(6000, False))
        try:
            analyse(run2, ref, R); bad = False
        except SystemExit as e:
            bad = '바닥 검사' in str(e)
        chk('⑨ S₀² ≤ S_R² 면 M 을 정의하지 않고 거부한다 (§24-4 바닥 검사)', bad)
        #  덱 파싱 거부
        open(os.path.join(run2, 'in.mixer'), 'w').write('timestep 1e-6\nrun 5\n')
        try:
            deck_plan(os.path.join(run2, 'in.mixer')); bad2 = False
        except ValueError:
            bad2 = True
        chk('⑩ 덱에 run 줄이 셋 미만이면 거부한다', bad2)

    # ══ ⑫~⑮ 2026-09-27 Codex HB-05 — 버린 칸이 분리를 숨기는가 · 부분 바퀴를 최종값으로 쓰는가 ══════════════
    #  ⑫ Codex 반례 그대로: AM 만 25 알 든 칸 둘 + SE 만 19 알 든 칸 하나 (n_min 20) → S² = 0 · 쓴 칸 2 · 버린 칸 1.
    #     두 상은 완전히 갈라져 있는데 SE 칸이 통째로 빠져 '분산 0' 이 된다.
    def _blob(cy, cz, n, typ, rad):
        return dict(y=np.full(n, cy) + rng.uniform(-1e-4, 1e-4, n), z=np.full(n, cz) + rng.uniform(-1e-4, 1e-4, n),
                    x=rng.uniform(-0.006, -0.004, n), type=np.full(n, float(typ)), radius=np.full(n, rad))
    parts = [_blob(-0.015, -0.015, 25, 1, 5e-4), _blob(0.015, -0.015, 25, 1, 5e-4), _blob(0.005, 0.015, 19, 3, 2e-4)]
    Dsep = {k: np.concatenate([p_[k] for p_ in parts]) for k in parts[0]}
    s2_, nu_, nd_, _ = cell_variance(Dsep, R, cells=4, x_cells=1, n_min=20)
    chk(f'⑫ 재현: 버린 칸이 분리를 숨긴다 — S² {s2_:.3g} · 쓴 칸 {nu_} · 버린 칸 {nd_} (Codex 반례)',
        s2_ == 0.0 and nu_ == 2 and nd_ == 1)
    cs = cell_stats(Dsep, R, cells=4, x_cells=1, n_min=20)
    chk(f'⑫b ★ 보조 진단이 그것을 드러낸다 — SE 유지 부피 {cs["se_vol_kept"]:.2f} · AM {cs["am_vol_kept"]:.2f} · '
        f'전 칸 S² {cs["s2_all"]:.3f}',
        cs['se_vol_kept'] == 0.0 and cs['am_vol_kept'] == 1.0 and cs['s2_all'] > 0.2 and cs['nonempty'] == 3)
    #  ⑬ 등록 최종값 = 덱의 계획 바퀴 수의 **마지막 완전 바퀴**.  옛 `M_final` 은 마지막 bin (부분일 수 있다).
    #  ⚠ 2026-09-28 (HBR3-05) — 정착을 10 ×2 → 125 ×2 로: 옛 고정구의 t₀ 20 은 간격 250 격자 밖 (계획 t₀ = 0) 이라 판독기가
    #    거부한다.  t₀ 250 · 프레임 250 + 250k 로 **간격 · bin 구조 · 값은 옛 고정구 그대로** (모든 step 이 +230 평행이동).
    DECK2 = ('timestep 1e-3\nrun 1\nrun 125\nrun 125\n'
             'dump dmp all custom 250 post/mix_*.liggghts id type mol x y z radius\n'
             'fix mvD all move/mesh mesh Drum rotate origin 0 0 0 axis 1. 0. 0. period 1.001\n'
             'run 2000\n')
    with tempfile.TemporaryDirectory() as td:
        run = os.path.join(td, 'run'); ref = os.path.join(td, 'ref')
        for d in (run, ref):
            os.makedirs(os.path.join(d, 'post'))
            open(os.path.join(d, 'in.mixer'), 'w').write(DECK2)
        write_dump(os.path.join(ref, 'post', 'mix_250.liggghts'), cloud(6000, False))
        write_dump(os.path.join(run, 'post', 'mix_250.liggghts'), cloud(6000, True))
        #  t0 = 250 · 바퀴 = 1001 스텝 · 덤프 250 ⇒ 실제 캠페인 (바퀴 = 덤프 25.0004 개) 처럼 마지막 덤프가 계획 끝
        #  **바로 앞** (rev 1.998) 이고 덤프 간격에 결손이 없다
        for k_ in range(1, 9):
            write_dump(os.path.join(run, 'post', f'mix_{250 + 250 * k_}.liggghts'), cloud(6000, True, seg_frac=0.3))
        res = analyse(run, ref, R)
        pl_ = res['planned']
        chk(f'⑬ 계획 바퀴 수 {pl_["n_revs"]} · 최종 bin {pl_["final_bin"]} 완전 ({pl_["n"]} 프레임) · 값 = 그 bin 평균',
            pl_['n_revs'] == 2 and pl_['final_bin'] == 1 and pl_['complete'] and pl_['n'] == 4
            and abs(pl_['M_final'] - res['by_rev'][1]['M_mean']) < 1e-12 and not res['tech'])
        #  덤프가 계획 끝을 한 프레임 넘으면 (계획 격자 밖) — 옛 판은 그 한 장을 '1 프레임짜리 bin 2' 로 옛 `M_final` 에 넣었다.
        #  2026-09-28 (HBR3-05) 부터 **행에서 빠지고** tech 로 남는다.  등록 값은 그때도 지금도 안 움직인다.
        write_dump(os.path.join(run, 'post', f'mix_{250 + 250 * 9}.liggghts'), cloud(6000, False))
        res2 = analyse(run, ref, R)
        chk(f'⑬b 계획 끝을 넘은 덤프 (step 2500) 는 행 · 옛 M_final 에서 빠지고 tech 로 남는다 — 등록 값은 안 움직인다 '
            f'(옛 M_final bin {res2["final_rev"]})',
            res2['final_rev'] == 1 and 2 not in res2['by_rev'] and all(r_['step'] != 2500 for r_ in res2['rows'])
            and abs(res2['planned']['M_final'] - res['planned']['M_final']) < 1e-12
            and any('step 2500' in t and '격자 밖' in t for t in res2['tech']))
        #  미완주 — 마지막 두 프레임을 치우면 최종 bin 이 불완전 ⇒ 값 없음 + 기술 표지.  옛 `M_final` 은 이때 부분 bin (2 프레임) 이다
        for k_ in (7, 8, 9):
            os.remove(os.path.join(run, 'post', f'mix_{250 + 250 * k_}.liggghts'))
        res3 = analyse(run, ref, R)
        chk(f'⑭ 미완주면 등록 최종값 = 없음 · 기술 표지 · 옛 M_final 은 부분 bin ({"; ".join(res3["tech"])[:60]})',
            res3['planned']['M_final'] is None and not res3['planned']['complete'] and res3['tech']
            and res3['final_rev'] == 1 and res3['by_rev'][1]['n'] == 2)
        #  ⑮ 평탄 조건 (prereg §2: |M̄₈ − M̄₇| ≤ M_sd(8)) 을 등록 bin 으로 계산해 둔다
        pf_ = res['planned']
        chk('⑮ 평탄 조건 = |M̄(최종) − M̄(직전)| ≤ sd(최종) 를 등록 bin 으로 계산한다',
            pf_['flat'] == (abs(res['by_rev'][1]['M_mean'] - res['by_rev'][0]['M_mean']) <= res['by_rev'][1]['M_sd']))

    # ══ ⑯~⑱ 2026-09-27 저녁 Codex 재리뷰 HBR2-02 · 04 · 06 — 합성 반례 (evidence/review_probe.py) 를 **먼저 재현**하고 고쳤다 ══
    DECK3 = ('timestep 0.001\nrun 1\nrun 100\nrun 100\n'
             'dump dmp all custom 40 post/mix_*.liggghts id type x y z radius\n'
             'fix mvD all move/mesh mesh Drum rotate origin 0 0 0 axis 1 0 0 period 1.00001\nrun 8000\n')

    def _cloud(kind):
        """작은 결정론적 구름 (기계 상태 아님) — 4 무리 × 24 알.  seg = 층상 · ref = 무작위 기준 · mid = 중간.
        ref_p · ref_alt = Codex 3차 프로브 (review_round3_probe.py) 의 기준 · 대체 기준 (앞 · 뒤 두 무리의 AM 알 10·14 / 7·17)."""
        n_am = {'ref': (6, 18), 'mid': (3, 21), 'ref_p': (10, 14), 'ref_alt': (7, 17)}
        xs, ys, zs, ts = [], [], [], []
        for j, (y, z) in enumerate([(-.01, -.01), (-.01, .01), (.01, -.01), (.01, .01)]):
            for k in range(24):
                ys.append(y); zs.append(z); xs.append((k - 12) * 1e-5)
                if kind == 'seg':
                    ts.append(1 if j < 2 else 3)
                else:
                    ts.append(1 if k < n_am[kind][0 if j < 2 else 1] else 3)
        return dict(id=np.arange(1, 97, dtype=float), type=np.array(ts, float), mol=-np.ones(96),
                    x=np.array(xs), y=np.array(ys), z=np.array(zs), radius=np.full(96, 1e-5))

    def _case(td, name, idx):
        run_ = os.path.join(td, name); os.makedirs(os.path.join(run_, 'post'))
        open(os.path.join(run_, 'in.mixer'), 'w').write(DECK3)
        for i in idx:
            write_dump(os.path.join(run_, 'post', f'mix_{200 + 40 * i}.liggghts'), _cloud('seg' if i == 0 else 'mid'))
        return run_
    with tempfile.TemporaryDirectory() as td:
        ref = _case(td, 'ref', []); write_dump(os.path.join(ref, 'post', 'mix_200.liggghts'), _cloud('ref'))
        run = _case(td, 'smoke', range(26))                       # 정상 bin 0 (t₀ + 25 = 26 프레임) · 그 뒤는 아직 안 돔
        res = analyse(run, ref, .02, cells=2, x_cells=1)
        sm = res['smoke']
        chk(f'⑯ ★ HBR2-02: 정상 bin 0 스모크 — smoke 창은 통과 (tech_smoke {sm["tech_smoke"]}) · 최종 창의 미완주 표지와 분리',
            sm['complete'] and not sm['tech_smoke'] and sm['n'] == 26 and not res['planned']['complete']
            and any('미완주' in t for t in res['tech']))
        pv = res['provenance']
        chk('㉖ ★ HBR4-05 — 증서의 출처: 판독기 sha256 · 칸 규약 (실제 인자 전부) · 평가/기준 덱 sha256 · 판독 프레임 (step · 파일 · sha256) = '
            '계산에 쓴 행 · 발사 봉인 없음은 None (지어내지 않는다)',
            pv['schema'] == PROVENANCE_SCHEMA and pv['tool_sha256'] == _sha_file(os.path.abspath(__file__))
            and pv['args'] == dict(cells=2, x_cells=1, n_min=20, axis='x', r_container=0.02)
            and [f_[0] for f_ in pv['run']['frames']['files']] == [r_['step'] for r_ in res['rows']]
            and pv['run']['frames']['sha256'] == frame_digest(pv['run']['frames']['files'])
            and [f_[0] for f_ in pv['ref']['frames']['files']] == [200] and pv['run']['launch_record_sha256'] is None
            and not verify_frames(os.path.join(run, 'post'), pv['run']['frames']))
        foreign = _case(td, 'foreign', [0])                        # 다른 폴더 · 같은 계획 · 다른 데이터 (Codex foreign_wrong_grid_smoke_gate)
        for i in range(1, 26):
            write_dump(os.path.join(foreign, 'post', f'mix_{200 + 40 * i}.liggghts'), _cloud('ref_alt'))
        pvf = analyse(foreign, ref, .02, cells=2, x_cells=1)['provenance']
        chk('㉖b 다른 폴더의 **실제** 판독 증서 (같은 이름 규칙 · 같은 계획 · 다른 데이터) 는 이 런의 프레임으로 다시 해시하면 어긋난다 — '
            '칸 규약 불일치는 인자로 드러나 런처 관문이 거부한다 (test_launcher HL④h)',
            bool(verify_frames(os.path.join(run, 'post'), pvf['run']['frames'])))
        os.remove(os.path.join(run, 'post', 'mix_600.liggghts'))
        res = analyse(run, ref, .02, cells=2, x_cells=1)
        chk('⑯b bin 0 안의 덤프 결손은 스모크 실패 (tech_smoke)',
            not res['smoke']['complete'] and any('결손' in t for t in res['smoke']['tech_smoke']))
        run2 = _case(td, 'prev', [0, *range(174, 201)])            # bin 6 이 2/25 · bin 7 은 25/25 (Codex 반례 그대로)
        res2 = analyse(run2, ref, .02, cells=2, x_cells=1)
        pl = res2['planned']
        chk(f'⑰ ★ HBR2-04: 직전 bin 이 2/25 프레임이면 최종값은 보고하되 평탄 = None · 기술 표지 (flat {pl["flat"]})',
            pl['complete'] and pl['M_final'] is not None and pl['flat'] is None
            and any('직전' in t for t in res2['tech']) and res2['by_rev'][6]['n'] == 2)
        run3 = _case(td, 'last', range(200))                        # 마지막 계획 덤프 (8200) 하나 없음
        chk('⑰b 최종 bin 의 마지막 계획 덤프가 없으면 미완주',
            not analyse(run3, ref, .02, cells=2, x_cells=1)['planned']['complete'])
        run4 = _case(td, 'dup', range(26))
        import shutil as _sh
        _sh.copyfile(os.path.join(run4, 'post', 'mix_200.liggghts'), os.path.join(run4, 'post', 'mix_600.liggghts'))
        res4 = analyse(run4, ref, .02, cells=2, x_cells=1)
        chk('⑰c 헤더 step 이 파일명과 다른 덤프 (복제로 수 채움) 는 스모크 · 최종 둘 다 기술 표지',
            any('헤더' in t for t in res4['smoke']['tech_smoke']) and any('헤더' in t for t in res4['tech']))
    #  ⑱ HBR2-06 — 부피 유지 0.98 이어도 선택-칸 분산과 전 칸 분산은 다르다 · 상별 · 프레임별 QC (D-2)
    xs, ys, zs, ts, rs = [], [], [], [], []
    for y, z in [(-.75, -.75), (-.25, -.75)]:
        for k in range(200):
            ys.append(y); zs.append(z); xs.append(k * 1e-5); ts.append(1 if k < 100 else 3); rs.append(1e-6)
    for j, (y, z) in enumerate([(.25, -.75), (.75, -.75), (-.75, -.25), (-.25, -.25), (.25, -.25), (.75, -.25), (-.75, .25), (-.25, .25)]):
        ys.append(y); zs.append(z); xs.append(0); ts.append(1 if j < 4 else 3); rs.append(1e-6)
    Dq = dict(id=np.arange(1, len(xs) + 1, dtype=float), type=np.array(ts, float), x=np.array(xs), y=np.array(ys),
              z=np.array(zs), radius=np.array(rs))
    st_ = cell_stats(Dq, 1, cells=4, x_cells=1, n_min=20)
    chk(f'⑱ 재현 (HBR2-06): 유지 부피 AM {st_["am_vol_kept"]:.4f} · SE {st_["se_vol_kept"]:.4f} 인데 S²_keep {st_["s2"]:.3f} vs '
        f'S²_all {st_["s2_all"]:.3f} — 유지율은 대표성 보증이 아니다 (상별 유지 {st_.get("vol_kept_by_type")})',
        st_['am_vol_kept'] > .9 and st_['se_vol_kept'] > .9 and st_['s2'] == 0 and st_['s2_all'] > .19
        and set(st_.get('vol_kept_by_type', {})) == {1, 3})
    rows_ = [dict(am_vol_kept=1.0, se_vol_kept=(0.0 if i < 2 else 1.0),
                  vol_kept_by_type={1: 1.0, 3: (0.0 if i < 2 else 1.0)}) for i in range(25)]
    q = qc_representativeness(rows_)
    chk(f'⑱b D-2 QC: 25 프레임 중 2 프레임 유지 0 → 평균 {q["se_mean"]:.2f} ≥ 0.90 인데 프레임별 최솟값 '
        f'{q["min_by_type"][3]:.0f} < 0.80 ⇒ 미달 (평균으로 상쇄하지 않는다)',
        q['se_mean'] >= .9 and not q['pass'])

    # ══ ⑲~㉔ 2026-09-28 Codex 3차 HBR3-05 · 06 — 합성 반례 (evidence/review_round3_probe.py `reader_*`) 를 **먼저 재현**하고 고쳤다 ══
    #  덱 = DECK3 (정착 100 ×2 · 간격 40 ⇒ 계획 t₀ 200) · 기준 = 프로브의 ref (AM 10·14) ⇒ 정상 등록 최종값 0.45.
    def _refuses(fn, *need):
        """fn() 이 SystemExit 로 거부하고 메시지에 need 가 다 있으면 True (통과하거나 다른 사유로 거부하면 False)."""
        try:
            fn()
        except SystemExit as e:
            return all(w in str(e) for w in need)
        return False

    def _dump_raw(path, D, header=True):
        """열 순서 · 값 그대로 쓰는 덤프 (write_dump 는 id · type 을 정수로 깎는다) — 머리 · 스키마 결함 고정구용."""
        keys = list(D)
        n = len(D[keys[0]])
        st_ = int(re.search(r'_(\d+)\.', os.path.basename(path)).group(1))
        with open(path, 'w') as f:
            if header:
                f.write(f'ITEM: TIMESTEP\n{st_}\nITEM: NUMBER OF ATOMS\n{n}\nITEM: BOX BOUNDS ff ff ff\n-1 1\n-1 1\n-1 1\n')
            f.write('ITEM: ATOMS ' + ' '.join(keys) + '\n')
            for i in range(n):
                f.write(' '.join(format(float(D[k][i]), '.17g') for k in keys) + '\n')
    _an = dict(r_container=.02, cells=2, x_cells=1)
    with tempfile.TemporaryDirectory() as td:
        ref = _case(td, 'ref_p', []); write_dump(os.path.join(ref, 'post', 'mix_200.liggghts'), _cloud('ref_p'))
        run_nom = _case(td, 'nom', range(201))                      # t₀ 200 ~ 8200 · 201 프레임 (계획 격자 전부)
        nom = analyse(run_nom, ref, **_an)
        M_nom = nom['planned']['M_final']
        #  (a) 평가 런의 계획 t₀ (200) 가 없고 앞의 정착 프레임 (160) 만 있다 — 옛 판: t0_step 160 으로 조용히 대신했다
        run = _case(td, 'miss_t0', range(1, 201)); write_dump(os.path.join(run, 'post', 'mix_160.liggghts'), _cloud('seg'))
        chk('⑲ ★ HBR3-05: 평가 런의 계획 t₀ (step 200) 가 없으면 앞 정착 프레임 (160) 으로 대신하지 않고 거부한다',
            _refuses(lambda: analyse(run, ref, **_an), 't₀', 'step 200'))
        #  (b) E0 기준의 계획 t₀ (200) 가 없고 앞의 정착 프레임 (160, 다른 구름) 만 있다 — 옛 판: S_R² 0.0434 · M_final 0.529 로 통과
        ref_m = _case(td, 'ref_miss', []); write_dump(os.path.join(ref_m, 'post', 'mix_160.liggghts'), _cloud('ref_alt'))
        chk('⑳ ★ HBR3-05: E0 기준의 계획 t₀ (step 200) 가 없으면 앞 정착 프레임 (160) 으로 대신하지 않고 거부한다',
            _refuses(lambda: analyse(run_nom, ref_m, **_an), 't₀', 'step 200', 'E0'))
        #  (c) 계획 격자 25 프레임 + 격자 밖 1 장 (7301) — 옛 판: n 26/25 · complete · tech [] · M_final 0.45 → 0.4327
        run = _case(td, 'offgrid', range(201)); write_dump(os.path.join(run, 'post', 'mix_7301.liggghts'), _cloud('seg'))
        r_ = analyse(run, ref, **_an)
        pl = r_['planned']
        chk(f'㉑ ★ HBR3-05: 격자 밖 덤프 (7301) 는 행 · M · SD · 평탄에서 빠지고 tech 로 남는다 — M_final {pl["M_final"]} '
            f'(정상 {M_nom}) · n {pl["n"]}/{pl["expected"]}',
            M_nom is not None and abs(M_nom - 0.45) < 1e-12 and pl['M_final'] is not None and abs(pl['M_final'] - M_nom) < 1e-12
            and pl['M_final_sd'] == nom['planned']['M_final_sd'] and pl['flat'] == nom['planned']['flat']
            and pl['n'] == pl['expected'] == 25 and all(x_['step'] != 7301 for x_ in r_['rows'])
            and any('step 7301' in t and '격자 밖' in t for t in r_['tech']) and not r_['smoke']['tech_smoke'])
        #  bin 0 안의 격자 밖 덤프 (230) — 스모크 창에서도 빠지고 tech_smoke 에 남는다
        run = _case(td, 'offgrid0', range(201)); write_dump(os.path.join(run, 'post', 'mix_230.liggghts'), _cloud('seg'))
        r_ = analyse(run, ref, **_an)
        chk('㉑b bin 0 안의 격자 밖 덤프 (230) 는 스모크 창에서도 빠지고 (M · n 정상과 같다) tech_smoke · tech 에 남는다',
            r_['smoke']['n'] == nom['smoke']['n'] == 26 and abs(r_['smoke']['M_mean'] - nom['smoke']['M_mean']) < 1e-12
            and any('step 230' in t for t in r_['smoke']['tech_smoke']) and any('step 230' in t for t in r_['tech']))
        #  같은 step (7600, 최종 bin) 의 덤프가 둘 — 어느 쪽이 참인지 모르므로 둘 다 쓰지 않는다 (옛 판: 둘 다 평균에 넣었다)
        run = _case(td, 'dup2', range(201)); write_dump(os.path.join(run, 'post', 'dup_7600.liggghts'), _cloud('seg'))
        r_ = analyse(run, ref, **_an)
        chk('㉑c 같은 step 의 덤프가 둘이면 어느 것도 계산에 쓰지 않는다 — 최종 bin 결손 · 등록 최종값 없음 · tech',
            7600 not in {x_['step'] for x_ in r_['rows']} and r_['planned']['M_final'] is None
            and any('같은 step' in t for t in r_['tech']))
        #  (d) 머리 (TIMESTEP · NUMBER OF ATOMS) 없는 행 프레임 — bin 0 의 1000 · 최종 bin 의 8000
        run = _case(td, 'nohdr', [i for i in range(201) if i not in (20, 195)])
        for i in (20, 195):
            _dump_raw(os.path.join(run, 'post', f'mix_{200 + 40 * i}.liggghts'), _cloud('mid'), header=False)
        r_ = analyse(run, ref, **_an)
        chk('㉒ ★ HBR3-06: 머리 없는 프레임 (1000 · 8000) 은 계산에서 빠지고 tech · (bin 0 이면) tech_smoke 에 남는다 '
            '— 최종 bin 결손이라 등록 최종값 없음',
            not ({1000, 8000} & {x_['step'] for x_ in r_['rows']})
            and any('step 1000' in t for t in r_['tech']) and any('step 8000' in t for t in r_['tech'])
            and any('step 1000' in t for t in r_['smoke']['tech_smoke'])
            and not any('step 8000' in t for t in r_['smoke']['tech_smoke'])
            and r_['planned']['M_final'] is None and not r_['smoke']['complete'])
        #  (e) 뒤 프레임의 소수 type (1.5 · 3.5 — 정수로 깎으면 1 · 3 이라 '변화 없음' 으로 보인다) · id 열 없음
        run = _case(td, 'schema', [i for i in range(201) if i not in (190, 191)])
        Df = _cloud('mid'); Df['type'] = Df['type'] + 0.5
        _dump_raw(os.path.join(run, 'post', 'mix_7800.liggghts'), Df)
        Dn = _cloud('mid'); Dn.pop('id')
        _dump_raw(os.path.join(run, 'post', 'mix_7840.liggghts'), Dn)
        r_ = analyse(run, ref, **_an)
        chk('㉓ ★ HBR3-06: 소수 type · id 열 없는 뒤 프레임 (7800 · 7840) 은 계산에서 빠지고 tech 에 남는다 (옛 판: 깎아서 그대로 썼다)',
            not ({7800, 7840} & {x_['step'] for x_ in r_['rows']}) and r_['planned']['M_final'] is None
            and any('step 7800' in t and 'type' in t for t in r_['tech'])
            and any('step 7840' in t and 'id' in t for t in r_['tech']))
        #  (f) t₀ 프레임 자체가 검사를 못 넘는다 — 평가 런 t₀ 머리 없음 · E0 t₀ 소수 type ⇒ 없는 것처럼 거부
        run = _case(td, 't0_bad', range(1, 201))
        _dump_raw(os.path.join(run, 'post', 'mix_200.liggghts'), _cloud('seg'), header=False)
        ref_b = _case(td, 'ref_bad', []); Dr = _cloud('ref_p'); Dr['type'] = Dr['type'] + 0.5
        _dump_raw(os.path.join(ref_b, 'post', 'mix_200.liggghts'), Dr)
        chk('㉔ ★ HBR3-05 · 06: t₀ 프레임이 검사를 못 넘으면 (평가 런 머리 없음 · E0 소수 type) 없는 것처럼 거부한다',
            _refuses(lambda: analyse(run, ref, **_an), 't₀', 'step 200')
            and _refuses(lambda: analyse(run_nom, ref_b, **_an), 't₀', 'step 200', 'E0'))

    # ══ ㉘ ㉙ 2026-09-30 — 강성 축 코드 선행조건 2 단계 piece 1: bin 창 파일 열거 (관문 공용) · E0 t₀ 통계 (E0 진단) ═══════════
    #    ★ 반례를 먼저 옮겼다 — 옛 판: bin_window_files · e0_t0_stats 없음 (NameError) ⇒ 전부 FAIL.
    def _okm(fn):
        try:
            return bool(fn())
        except Exception as e_:                                       # noqa: BLE001
            print(f'        ({type(e_).__name__}: {str(e_)[:100]})')
            return False
    with tempfile.TemporaryDirectory() as td:
        ref = _case(td, 'ref_i', []); write_dump(os.path.join(ref, 'post', 'mix_200.liggghts'), _cloud('ref_p'))
        #  DECK3: 정착 끝 t₀ 200 · 간격 40 · 바퀴 1000.01 step ⇒ bin 3 = step 3240 … 4200 (25 프레임)
        run4 = _case(td, 'r4', range(101))                         # 200 … 4200 = bin 0–3 완전 · bin 4 이후 아직 안 돔
        def _t28():
            post = os.path.join(run4, 'post')
            w3 = bin_window_files(post, 200, 1000.01, 40, 8201, (3,))
            w0 = bin_window_files(post, 200, 1000.01, 40, 8201, (0,))
            a_ = analyse(run4, ref, **_an)
            ok0 = (w3['lattice'] == {s_ for s_ in range(200, 8201, 40) if bin_of(s_, 200, 1000.01) == 3} and not (w3['dup'] or w3['off'] or w3['miss'])
                   and len(w0['lattice']) == a_['lattice']['expected_by_bin'][0] and len(w3['lattice']) == a_['lattice']['expected_by_bin'][3])
            __import__('shutil').copyfile(os.path.join(post, 'mix_3600.liggghts'), os.path.join(post, 'copy_3600.liggghts'))
            write_dump(os.path.join(post, 'mix_3610.liggghts'), _cloud('mid'))
            os.remove(os.path.join(post, 'mix_4000.liggghts'))
            w3b = bin_window_files(post, 200, 1000.01, 40, 8201, (3,))
            return ok0 and w3b['dup'] == [3600] and w3b['off'] == [3610] and w3b['miss'] == [4000]
        chk('㉘ bin_window_files = 판독기 계획 격자 (bin 0 · 3 의 수가 analyse 의 expected_by_bin 과 같다) · 중복 (copy_3600) · 격자 밖 (3610) · 결손 (4000) 을 '
            '그대로 낸다 (관문 · 중간 판정 사전조건이 판독기와 같은 식을 쓴다)', _okm(_t28))

        run2 = _case(td, 'r2', range(76))                          # bin 2 까지만 (3200)

        def _t29():
            st_, p_, cs_ = e0_t0_stats(ref, **_an)
            a_ = analyse(run2, ref, **_an)
            return st_ == 200 and os.path.basename(p_) == 'mix_200.liggghts' and cs_['s2'] == a_['SR'] and bin_of(3240, 200, 1000.01) == 3
        chk('㉙ e0_t0_stats = analyse 가 S_R² 를 재는 바로 그 경로 (계획 t₀ 200 · 같은 S_R²) — E0 진단 (§4-c) 이 판독기와 같은 식으로 잰다', _okm(_t29))

    # ══ ㉚~㉞ 2026-09-30 — 강성 축 코드 선행조건 2 단계 piece 4: 중간 판정 한 번 (사전등록 §5-a · bin 3 = 4 바퀴) ════════════════
    #    ★ 반례를 먼저 옮겼다 — 옛 판: bin_window_stats · t0_floor · interim_rule · value_summary 없음 (NameError) ⇒ ㉚~㉞ 전부 FAIL.
    #    §5-a "M(t) 곡선 전체와 다른 bin 은 최종까지 봉인" ⇒ 판독기는 bin 3 의 **계획 격자** + 정규화에 필요한 계획 t₀ · E0 계획 t₀ 만 연다.
    G_ = globals()

    def _logged(fn):
        """fn() 을 돌리며 read_dump · validate_frame 이 연 경로를 모은다 → (결과, 연 경로 집합 (realpath))."""
        seen = []
        rd_, vf_ = G_['read_dump'], G_['validate_frame']

        def rd2(p, *a, **k):
            seen.append(os.path.realpath(p))
            return rd_(p, *a, **k)

        def vf2(p, *a, **k):
            seen.append(os.path.realpath(p))
            return vf_(p, *a, **k)
        G_['read_dump'], G_['validate_frame'] = rd2, vf2
        try:
            return fn(), set(seen)
        finally:
            G_['read_dump'], G_['validate_frame'] = rd_, vf_

    def _rp(d_, s_):
        return os.path.realpath(os.path.join(d_, 'post', f'mix_{s_}.liggghts'))
    with tempfile.TemporaryDirectory() as td:
        ref = _case(td, 'ref_i3', []); write_dump(os.path.join(ref, 'post', 'mix_200.liggghts'), _cloud('ref_p'))
        #  DECK3: t₀ 200 · 간격 40 · 바퀴 1000.01 step ⇒ bin 3 = 3240 … 4200 (25 장) · 계획 bin 0–7
        b3 = [s_ for s_ in range(200, 8201, 40) if bin_of(s_, 200, 1000.01) == 3]

        def _t30():
            run_ = _case(td, 'r_all', range(201))                          # bin 0–7 완전
            full = analyse(run_, ref, **_an)
            w, seen = _logged(lambda: bin_window_stats(run_, ref, bin_=3, **_an))
            allowed = {_rp(run_, s_) for s_ in [200] + b3} | {_rp(ref, 200)}
            ok0 = (w['complete'] and not w['tech'] and w['n'] == w['expected'] == full['lattice']['expected_by_bin'][3] == 25
                   and abs(w['M_bin'] - full['by_rev'][3]['M_mean']) < 1e-12 and w['qc_repr']['pass'] == full['by_rev'][3]['qc']['pass']
                   and seen == allowed and [f_[0] for f_ in w['provenance']['run']['frames']['files']] == [200] + b3
                   and [f_[0] for f_ in w['provenance']['ref']['frames']['files']] == [200])
            for s_ in range(240, 8201, 40):                                   # bin 3 밖 (t₀ 제외) 을 전부 쓰레기로 — 열면 값이 바뀌거나 거부된다
                if s_ not in b3:
                    open(os.path.join(run_, 'post', f'mix_{s_}.liggghts'), 'w').write('쓰레기 — 중간 판정은 이 파일을 열면 안 된다\n')
            w2 = bin_window_stats(run_, ref, bin_=3, **_an)
            return (ok0 and w2['complete'] and w2['M_bin'] == w['M_bin'] and w2['provenance']['run']['frames'] == w['provenance']['run']['frames']
                    and len(analyse(run_, ref, **_an)['tech']) > 0)            # (대조) 전체 판독기는 쓰레기를 보고 tech 를 낸다
        chk('㉚ ★ §5-a bin 3 창 판독 = 계획 격자 25 장 · 값 = analyse 의 bin 3 평균 (같은 식 · 1e-12) · 연 파일 = 계획 t₀ + bin 3 격자 + E0 계획 t₀ '
            '**정확히** · 다른 bin 을 전부 쓰레기로 바꿔도 같은 값 · 같은 출처 (열지 않는다)', _okm(_t30))

        def _t31():
            run_ = _case(td, 'r_inc', range(101))                          # bin 0–3 까지만 (4200)
            p_ = os.path.join(run_, 'post')
            res = {}
            w0 = bin_window_stats(run_, ref, bin_=3, **_an)
            res['ok'] = w0['complete'] and w0['M_bin'] is not None
            os.remove(os.path.join(p_, 'mix_4200.liggghts'))               # bin 3 마지막 계획 덤프 결손 = 아직 4 바퀴 전
            w1, seen1 = _logged(lambda: bin_window_stats(run_, ref, bin_=3, **_an))
            res['miss'] = (not w1['complete'] and w1['M_bin'] is None and any('결손' in t_ for t_ in w1['tech'])
                           and seen1 <= {_rp(run_, 200)})                    # M 을 계산하지 않았다 (bin 3 · E0 를 열지 않음)
            write_dump(os.path.join(p_, 'mix_4200.liggghts'), _cloud('mid'))
            __import__('shutil').copyfile(os.path.join(p_, 'mix_3600.liggghts'), os.path.join(p_, 'copy_3600.liggghts'))
            w2 = bin_window_stats(run_, ref, bin_=3, **_an)
            res['dup'] = not w2['complete'] and w2['M_bin'] is None and any('3600' in t_ for t_ in w2['tech'])
            os.remove(os.path.join(p_, 'copy_3600.liggghts'))
            write_dump(os.path.join(p_, 'mix_3610.liggghts'), _cloud('mid'))
            w3 = bin_window_stats(run_, ref, bin_=3, **_an)
            res['off'] = not w3['complete'] and w3['M_bin'] is None and any('3610' in t_ for t_ in w3['tech'])
            os.remove(os.path.join(p_, 'mix_3610.liggghts'))
            _dump_raw(os.path.join(p_, 'mix_3640.liggghts'), _cloud('mid'), header=False)
            w4 = bin_window_stats(run_, ref, bin_=3, **_an)
            res['format'] = not w4['complete'] and w4['M_bin'] is None and any('3640' in t_ for t_ in w4['tech'])
            write_dump(os.path.join(p_, 'mix_3640.liggghts'), _cloud('mid'))
            w5 = bin_window_stats(run_, ref, bin_=8, **_an)                # 계획 8 바퀴 = bin 0–7 · bin 8 은 계획에 없다
            res['beyond'] = not w5['complete'] and w5['M_bin'] is None and w5['expected'] == 0
            run6 = _case(td, 'r_flat', range(1, 101)); write_dump(os.path.join(run6, 'post', 'mix_200.liggghts'), _cloud('ref_p'))
            res['floor16'] = _refuses(lambda: bin_window_stats(run6, ref, bin_=3, **_an), '바닥 검사')     # S₀² ≤ S_R² (analyse ⑨ 와 같은 거부)
            print('        ' + ' · '.join(f'{k_}:{"✓" if v_ else "✗"}' for k_, v_ in res.items()))
            return all(res.values())
        chk('㉛ ★ bin 3 창이 불완전 (결손 = 4 바퀴 전 · 중복 · 격자 밖 · 형식 실패 · 계획 밖 bin) 이면 값 없음 · tech — 결손이면 bin 3 · E0 프레임을 '
            '열지도 않는다 (M 미계산) · S₀² ≤ S_R² 는 analyse 와 같이 거부', _okm(_t31))

    def _flat_cloud(n_a, n_b):
        """x 가 모두 같은 4 모서리 × 24 알 (8×8×2 에서도 칸당 24 ≥ n_min) — 앞 두 모서리 AM n_a 알 · 뒤 두 모서리 n_b 알."""
        ys, zs, ts = [], [], []
        for j, (y, z) in enumerate([(-.01, -.01), (-.01, .01), (.01, -.01), (.01, .01)]):
            for k in range(24):
                ys.append(y); zs.append(z); ts.append(1 if k < (n_a if j < 2 else n_b) else 3)
        n = len(ys)
        return dict(id=np.arange(1, n + 1, dtype=float), type=np.array(ts, float), mol=-np.ones(n), x=np.zeros(n),
                    y=np.array(ys), z=np.array(zs), radius=np.full(n, 1e-5))
    with tempfile.TemporaryDirectory() as td:
        def _t32():
            ref_ = _case(td, 'ref_f', []); write_dump(os.path.join(ref_, 'post', 'mix_200.liggghts'), _flat_cloud(10, 14))
            res = {}
            for lab, (na, nb), want_pass in (('seg', (24, 0), True), ('weak', (9, 15), False)):
                run_ = _case(td, f'fl_{lab}', range(1, 30)); write_dump(os.path.join(run_, 'post', 'mix_200.liggghts'), _flat_cloud(na, nb))
                fl, seen = _logged(lambda: t0_floor(run_, ref_, r_container=.02))
                want = (cell_stats(_flat_cloud(na, nb), .02, 8, 2)['s2'] / cell_stats(_flat_cloud(10, 14), .02, 8, 2)['s2'])
                res[lab] = (abs(fl['ratio'] - want) < 1e-12 and fl['pass'] is want_pass and (fl['cells'], fl['x_cells'], fl['min']) == (8, 2, 5.0)
                            and seen == {_rp(run_, 200), _rp(ref_, 200)})
            print('        ' + ' · '.join(f'{k_}:{"✓" if v_ else "✗"}' for k_, v_ in res.items()))
            return all(res.values())
        chk('㉜ 바닥 검사 t0_floor = 8×8×2 에서 S₀²/S_R² ≥ 5 (본 캠페인 결정 (b) 의 칸 · 문턱) — 계획 t₀ · E0 계획 t₀ 두 장만 연다 · 층상 36 통과 · 약한 층상 '
            '2.25 불합격', _okm(_t32))

    def _t33():
        S = (15485863, 86028121, 104395301)
        res = {}

        def rule(d, e):
            return interim_rule(dict(zip(S, d)), dict(zip(S, e)), S)
        r = rule((0.30, 0.25, 0.35), (0.0, 0.0, 0.0))
        se = 0.05 / 3 ** 0.5
        res['met'] = (r['met'] is True and abs(r['delta3'] - 0.30) < 1e-12 and abs(r['se3'] - se) < 1e-12 and r['u_mean'] == 0 and r['u_se'] == 0
                      and r['signs'] == {str(s_): '+' for s_ in S} and (r['mid'], r['k_se'], r['tol'], r['bin']) == (0.10, 3.0, 1e-12, 3))
        r = rule((0.30, 0.25, 0.35), (0.01, 0.02, 0.02))
        res['u'] = (abs(r['u_mean'] - 0.05 / 3) < 1e-15 and abs(r['u_se'] - 0.03 / 6 ** 0.5) < 1e-15 and abs(r['lhs'] - (0.30 - 0.05 / 3)) < 1e-12
                    and abs(r['rhs_se'] - 3 * (se + 0.03 / 6 ** 0.5)) < 1e-12 and r['met'] is True)
        #  Codex (7 차 HBR7-04) 의 d = .04/.14/.24 — 최종 판정선 (2·SE) 은 통과하지만 중간 (3·SE) 은 못 넘는다 = 중간이 더 엄격하다
        r = rule((0.04, 0.14, 0.24), (0.0, 0.0, 0.0))
        res['3se'] = (r['met'] is False and r['cond'] == dict(all_positive=True, mid=True, se=False)
                      and r['delta3'] >= 2 * r['se3'] and r['delta3'] < 3 * r['se3'])
        r = rule((0.60, -0.01, 0.60), (0.0, 0.0, 0.0))
        res['neg'] = r['met'] is False and r['cond']['all_positive'] is False and r['signs'][str(S[1])] == '−' and r['cond']['mid'] is True
        r = rule((0.0, 0.5, 0.5), (0.0, 0.0, 0.0))
        res['zero'] = r['met'] is False and r['signs'][str(S[0])] == '0' and r['cond']['all_positive'] is False
        r = rule((0.1, 0.2, 0.3), (0.3, 0.0, 0.0))                     # Δ − u_mean = 0.09999999999999999 (부동소수) — 등록 여유 1e−12 로 경계 안
        res['tol'] = r['lhs'] < 0.10 and r['cond']['mid'] is True
        bad = []
        for d_, e_, s_ in (((0.3, 0.3, 0.3), (0.0, 0.0, 0.0), S[:2]), ((0.3, float('nan'), 0.3), (0.0, 0.0, 0.0), S),
                           ((0.3, 0.3, 0.3), (0.0, -0.01, 0.0), S), ((0.3, 0.3, 0.3), (0.0, True, 0.0), S)):
            try:
                interim_rule(dict(zip(s_, d_)), dict(zip(s_, e_)), s_)
                bad.append(False)
            except ValueError:
                bad.append(True)
        try:
            interim_rule(dict(zip(S, (0.3, 0.3, 0.3))), {S[0]: 0.0, S[1]: 0.0}, S)
            bad.append(False)
        except ValueError:
            bad.append(True)
        res['fail_closed'] = all(bad) and len(bad) == 5
        r = rule((0.371, 0.2468, 0.3913), (0.0, 0.0, 0.0))
        flo = [v_ for v_ in _keys_vals(r) if isinstance(v_, float)]
        res['no_seed_values'] = not any(abs(v_ - x_) < 1e-12 for v_ in flo for x_ in (0.371, 0.2468, 0.3913))
        sm = value_summary(dict(zip(S, (0.1, 0.2, 0.3))), S)
        res['summary'] = (abs(sm['mean'] - 0.2) < 1e-12 and abs(sm['se'] - 0.1 / 3 ** 0.5) < 1e-12 and sm['n'] == 3
                          and value_summary({S[0]: 0.1, S[1]: 0.2}, S) is None and value_summary(dict(zip(S, (0.1, float('inf'), 0.3))), S) is None)
        print('        ' + ' · '.join(f'{k_}:{"✓" if v_ else "✗"}' for k_, v_ in res.items()))
        return all(res.values())

    def _keys_vals(v):
        if isinstance(v, dict):
            for x_ in v.values():
                yield from _keys_vals(x_)
        elif isinstance(v, (list, tuple)):
            for x_ in v:
                yield from _keys_vals(x_)
        else:
            yield v
    chk('㉝ ★ §5-a 중간 판정선 — 세 seed 모두 양수 (엄격 · 0 은 양수 아님) ∧ Δ3 − u_mean ≥ 0.10 ∧ Δ3 − u_mean ≥ 3·(SE3 + u_SE) (u = §5 식 · 경계 여유 1e−12) · '
        'Codex d .04/.14/.24 는 2·SE 는 넘고 3·SE 는 못 넘는다 · 입력 fail-closed (seed 누락 · NaN · 음수/불리언 ε) · 출력에 seed 별 d 값 없음 · 요약 = 세 seed 다 유한할 때만',
        _okm(_t33))

    #  ㉕ planned_t0 — 실제 캠페인 덱 생성기 (make_mixer_deck) 로 만든 LC 8 바퀴 · E0 (`--revolutions 0`) 덱 (2026-09-28 실측값 고정).
    #     생성기를 못 불러오면 이름으로 보고하고 건너뛴다 (⑪ 과 같은 규약).
    try:
        import contextlib
        import io
        import make_mixer_deck as _gen
        with contextlib.redirect_stdout(io.StringIO()):
            _p = _gen.plan(100000, cgf=151.4)
            _rpm = _gen.resolve_rpm(_p['R'])
            _dk = {a_: _gen.deck(_p, _rpm, rv_, seed=32452843, arm=a_) for a_, rv_ in (('LC', 8), ('E0', 0))}
    except Exception as e:                                        # noqa: BLE001 — 생성기 부재 · 변경 중이면 SKIP
        print(f'  SKIP  ㉕ 덱 생성기를 못 불러 건너뜀 ({type(e).__name__}: {e})')
    else:
        with tempfile.TemporaryDirectory() as td:
            _pl = {}
            for a_, t_ in _dk.items():
                open(os.path.join(td, a_), 'w').write(t_)
                _pl[a_] = deck_plan(os.path.join(td, a_))
        lc_, e0_ = _pl['LC'], _pl['E0']
        chk(f'㉕ 계획 t₀ — 실제 덱 LC {planned_t0(lc_)} (정착 {lc_["steps_fill"]} ×2 · 간격 {lc_["dump_every"]} · 회전 시작 '
            f'{lc_["steps_total"] - lc_["steps_run"]}) · E0 {planned_t0(e0_)} (간격 {e0_["dump_every"]} · 회전 run {e0_["steps_run"]})',
            planned_t0(lc_) == 362664 and lc_['steps_total'] - lc_['steps_run'] == 385337 == 1 + 2 * lc_['steps_fill']
            and planned_t0(e0_) == 385000 and e0_['steps_run'] == 0 and e0_['n_run_lines'] == 4
            and e0_['steps_fill'] == lc_['steps_fill'])

    #  실제 덱으로 파서 검증 (스크래치패드에 있을 때만 — 없으면 이름으로 보고)
    _real = os.environ.get('MIX_REAL_DECK', '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/'
                           'd26d1e75-209f-540f-83a8-c0e1957edc2f/scratchpad/arms3/E1/in.mixer')
    if os.path.exists(_real):
        pl = deck_plan(_real)
        chk('⑪ 실제 덱: run 줄 4 개 중 정착 36308 ×2 · 회전 427062 · 바퀴 ≈ 213,538 스텝',
            pl['n_run_lines'] == 4 and pl['steps_fill'] == 36308 and pl['steps_run'] == 427062
            and abs(pl['steps_per_rev'] - 213538) < 2)
    else:
        print('  SKIP  ⑪ 실제 덱이 없어 건너뜀 (MIX_REAL_DECK 로 지정 가능)')

    print(f'\nmeasure_mixing_index selftest: {ok}/{ok + len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


def main():
    ap = argparse.ArgumentParser(description='Lacey 혼합지수 (§24)')
    ap.add_argument('runs', nargs='*', help='런 디렉터리 (in.mixer + post/)')
    ap.add_argument('--ref', help='균일 삽입 런 디렉터리 (S_R² 기준)')
    ap.add_argument('--r-container', type=float, default=0.02056)
    ap.add_argument('--cells', type=int, default=8)
    ap.add_argument('--x-cells', type=int, default=2)
    ap.add_argument('--n-min', type=int, default=20)
    ap.add_argument('--axis', default='x', choices=('x', 'y', 'z'))
    ap.add_argument('--json', help='결과 JSON 을 쓸 경로')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    if not (a.runs and a.ref):
        ap.error('런 디렉터리와 --ref 가 필요하다')
    out = []
    for d in a.runs:
        res = analyse(d, a.ref, a.r_container, a.cells, a.x_cells, a.n_min, a.axis)
        report(res)
        out.append(res)
    if a.json:
        json.dump(out, open(a.json, 'w'), ensure_ascii=False, indent=1, default=float)
        print(f'→ {a.json}')


if __name__ == '__main__':
    main()
