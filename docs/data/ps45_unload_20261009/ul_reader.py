#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEM 언로딩 키트 K4 — 읽는 쪽 (상태 기계 판독 · 선택 · 다음 제출 관문).  표준 라이브러리만 · 런 폴더를 읽기만 한다 (판정 JSON 만 쓴다).

    python3 ul_reader.py --selftest
    python3 ul_reader.py inputs  <root> <bed>            # in/ 원 파일 sha256 = 표 (rc 0 · 2)
    python3 ul_reader.py restore <root> <bed> [--hist <history_verdict.json>] [--job RJ|RJ2]
    python3 ul_reader.py kebase  <root> <bed>            # KE 기준 파일 <bed>/ul_base.in (S2 문턱 = 10 × (병진 + 회전))
    python3 ul_reader.py s0p     <root>                  # 10:0 이완 연장 S0′ / S0″ 결정 → ps_10_0_r45/s0_decision.json
    python3 ul_reader.py arm     <root> <bed> <job>      # 팔 판독 → <job>/arm_verdict.json
    python3 ul_reader.py select  <root>                  # 7:3 결정표 (§12-4 · §13-1) → ps_7_3_r45/selection.json
    python3 ul_reader.py gate    <root> <bed> <job>      # 그 잡을 지금 낼 수 있나 (rc 0 허용 · 2 거부 — 러너가 부른다)
    python3 ul_reader.py report  <root>                  # 다섯 침대 · 10 쌍 괄호 표 → report.json
    python3 ul_reader.py copycmd <bed>                   # 원 파일 복사 명령 여섯 (표에서 · ~ 경로)
    python3 ul_reader.py parentsums <UT 런 폴더>          # UTc 의 부모 관측 sha256 목록 (러너가 UTc 시작 때 parent_UT.sha256 으로 쓴다 · 개정 3 §14-3)
    python3 ul_reader.py grammar <gram_<시각>/grammar_verdict.json> --lmp-sha <sha256>   # 문법 fixture PASS 사전 조건 (Q5 · 러너가 RJ · RJ2 · EXT 의 LIGGGHTS 전에 · rc 0 · 2)

폴더 (정본 이름 = README §0):  <root>/<침대>/in/ (원 파일) · RJ/ (Ut0 · R · UN · UK) · RJ2/ (10:0 S0′ 에서) · EXT/ · EXT2/ (10:0) ·
  <팔>/ (UB · UT · UC · UVa · UVb · UT3 · UTc · G_<팔>) · ul_base.in · s0_decision.json · selection.json.
판정 규칙 (등록 §12 · §13 · 권고 기본값 = docs/reviews/dem_unloading_kit_section13_appendix_draft_20261013.md):
  창 접촉 상태  CONTACT (벽 local 접촉 ≥ 1 · 창 평균 P > 0) · TENSION (≥ 1 · P ≤ 0) · ZERO (0) · OBS_MISSING (덤프 없음 · 깨짐 — 0 으로 세지 않는다)
  분리 선언    연속 두 ZERO 창의 둘째 창 끝 · 재접촉이면 계수 · 분리 뒤 창 · 표면 관측 초기화 (§13-3)
  상쇄 표지    교차 끝점 마지막 창의 인장 합 ≥ 0.5 · P_meas · A — 처분 = 진단값 (순위 · 10 쌍 표에서 미식별 · §13-3 Q2 (가))
  끝점 유효    덱 정상 (S1 ∧ S2 두 창) · S3 PASS · 유한 · (k* 는) NOISE_FLOOR 아님 · 접촉 (CONTACT · TENSION)
  교차         P̄ − P_meas 부호 바뀜 (> ↔ ≤) · 첫 교차 = 점 추정 (P 두 점 선형 보간) + 실제 괄호 · 비단조 = 모든 교차 괄호의 합집합 (§13-5 ①)
  상태 두 축   primary_status (주 측정 · 첫 교차 + 확인 두 단) ↔ trajectory_status (분리 · 표면 · 종료) — §13-2 TIMEOUT 세 경우
  선택         유효한 δ 두 개면 결정표 한 행 · 아니면 SELECTION_UNRESOLVED (NaN 은 ≤ 도 > 도 아니다 · §13-1)
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ul_gates  # noqa: E402
import ul_lib  # noqa: E402
import ul_observers  # noqa: E402
import ul_s3  # noqa: E402

BEDS = ('ps_0_10_r45', 'ps_3_7_r45', 'ps_5_5_r45', 'ps_7_3_r45', 'ps_10_0_r45')
B73, B100 = 'ps_7_3_r45', 'ps_10_0_r45'
ARM_JOBS = ('UB', 'UT', 'UC', 'UVa', 'UVb', 'UT3', 'UTc', 'G_UB', 'G_UVa', 'G_UVb', 'G_UT3')
TUPLE_ARM = {'t1': 'UB', 't2': 'UVa', 't3': 'UT3', 't4': 'UVb'}
EPS_PP = 1e-9          # δ 경계 비교 — 부동소수 반올림 허용 (%p · choice C13)
WALL_U = ('mesh', 'tri', 'id', 'fnx', 'fny', 'fnz')                                         # compute wall/gran/local id force_normal
WALL_R = ('mesh', 'tri', 'id', 'fnx', 'fny', 'fnz', 'deltaMax', 'shearx', 'sheary', 'shearz')  # id history force_normal → 열 순서 = id · fn · history
ATOM_COLS = ['id', 'type', 'x', 'y', 'z', 'radius', 'mass', 'vx', 'vy', 'vz', 'omegax', 'omegay', 'omegaz', 'fx', 'fy', 'fz']   # U · G 덱 창 끝 원자 덤프 열
CPL_COLS = [f'c_cpl[{c}]' for c in range(1, 27)]                                            # r8 머리 cpl (pair/gran/local 26 열)

#: Q5 (1저자 10-14 — 강제) · 개정 3 §14-9: 본 R (RJ · RJ2) · 10:0 연장 (EXT) 의 LIGGGHTS 전 문법 fixture PASS — read_history.py --grammar 판정의 꼴 ·
#: 단계 폴더 (run_history.sh --grammar-only 가 덱 사본을 둔다) · 그 입력 (덱 둘 + 판 STL) 의 봉인 sha256 = 039abb141 판 (실행 2 대상 — 덱은 그 판 뒤
#: 바뀌지 않았다 · selftest R32 가 history_test 의 실제 파일과 대조 · 덱이 바뀌면 같은 묶음에서 고친다).  러너 파일 sha256 은 대조하지 않는다 (덱 아님) ·
#: 판독기 (read_history.py · history_params.json) = 아래 GRAMMAR_READER 봉인 값일 때만 그 런 원자료를 다시 읽는다 (Q3 · 1저자 10-15).
GRAMMAR_SCHEMA = 'ps45_unload_grammar_verdict_v1'
GRAMMAR_CHECKS = ('P_tech', 'GA_exists', 'GB_exists', 'GA_args', 'GB_args') + tuple(
    f'{s}_{c}' for s in ('GA', 'GB') for c in ('tech', 'markers', 'atom_dump_steps', 'wall_dump_steps', 'mesh_z', 'restart_state', 'contact_geo'))
GRAMMAR_STAGES = (('P', 'in.hist_producer.liggghts'), ('GA', 'in.hist_grammar.liggghts'), ('GB', 'in.hist_grammar.liggghts'))
GRAMMAR_INPUTS = {'in.hist_producer.liggghts': 'bc42a3ad71d5e02f6f21181bed09109dccfa60ad67a5d4a6b3d47f9c472fd70d',
                  'in.hist_grammar.liggghts': 'a1f0ee432b977d12a415b876ab3aa47225fec8f83c21cdd92948ff3abce8e6ed',
                  'plate_hist.stl': '5bc74ec7726723ec8e2bbc3dc10fafd639e6175f83a0e0047ca35a44ee7aa65d'}
#: Q3 (1저자 10-15 · Codex 수정 재확인 Q4) — 승인된 문법 판독기 = history_test 봉인 (history_test/SHA256SUMS) 의 read_history.py · history_params.json
#: (selftest R36 이 실제 파일 · 그 봉인 줄과 대조 · 판독기 · 표가 바뀌면 같은 묶음에서 고친다).  사전 점검은 그 런 kit 사본 (run_history.sh 가 복사) 의 두 파일이
#: 이 값일 때만 그 판독기로 원자료를 다시 읽는다 (`read_history.py --grammar` — 검사 19 = 판정 JSON 이어야 통과 · 아니면 실행하지 않고 거부).
GRAMMAR_READER = {'read_history.py': '70f741a9b8308fe33683de0f22872e2c44ce674dd6223cfce8c00e1a725b696c',
                  'history_params.json': '7a5279f0119cbbc37a9c212593e256a03e417dc9a6af4f18a4f01bdc72404ff4'}


# ── 구현 (아래 selftest 를 먼저 썼다) ─────────────────────────────────────────

_f = ul_lib.fnum


def _i(x):
    v = _f(x)
    return int(round(v)) if v is not None else None


def _csv(path, cols):
    """→ (행 dict 목록 · 문제 목록) — 머리 = 표 · 열 수 다른 줄은 버리지 않고 문제로 적는다."""
    if not os.path.exists(path):
        return None, [f'{os.path.basename(path)} 없음']
    lines = [ln for ln in open(path, encoding='utf-8', errors='replace').read().splitlines() if ln.strip()]
    pr = []
    if not lines or lines[0].split(',') != list(cols):
        pr.append(f'{os.path.basename(path)} 머리 ≠ 표')
        return [], pr
    out = []
    for n, ln in enumerate(lines[1:], 2):
        v = ln.split(',')
        if len(v) != len(cols):
            pr.append(f'{os.path.basename(path)}:{n} 열 수 {len(v)} ≠ {len(cols)}')
            continue
        out.append(dict(zip(cols, v)))
    return out, pr


def _state_vars(path):
    """덱 상태 파일 (`variable 이름 equal 값` 줄 · make_unload_decks._state) → {이름: 정확한 정수 | None (정수 아님)} · 파일 없음 = {}."""
    out = {}
    if not os.path.isfile(path):
        return out
    for ln in open(path, encoding='utf-8', errors='replace').read().splitlines():
        w = ln.split()
        if len(w) == 4 and w[0] == 'variable' and w[2] == 'equal':
            v = _f(w[3])
            out[w[1]] = int(v) if v is not None and v.is_integer() else None
    return out


def _resume_auth(d, events):
    """승인된 이어 돌림 경계 (ULKRR-02 · ULKRF-01 · 개정 3 §14-4 · 등록 §14-11) → ([(k, step)] 고유 경계 — 경계 하나에 승인 한 번, 문제 목록).
    승인 = 러너 시도 기록 (run_manifest.txt 의 `resume_from=step` · 러너가 이어 돌린 restart_unload_<step> 의 step) 의 step 마다 RESUME 사건이 **정확히 한 줄** ·
    덱 상태 파일 (restart/state_unload_<step>.in 의 ul_rstep = step · ul_k = 사건 k) 과 맞음.  같은 경계 (step) 의 RESUME 둘 이상 (같은 k = 중복 · 다른 k = 상충) ·
    사건 k ↔ 상태 파일 불일치 · 러너 resume_from 밖 step 의 RESUME · k · step 숫자 아님 = 승인 없음 + 사유 (ULKRF-01 — 중복 사건이 승인 하나를 둘로 늘리지 않는다).
    러너 resume_from 이 없는 폴더 (예 UTc = 부모 R_M 경계 · 다른 규칙 · _read_run_cont) 는 승인 · 문제 모두 없음."""
    man = os.path.join(d, 'run_manifest.txt')
    rf = set()
    if os.path.isfile(man):
        for ln in open(man, encoding='utf-8', errors='replace').read().splitlines():
            m = re.fullmatch(r'resume_from=(\d+)', ln.strip())
            if m:
                rf.add(int(m.group(1)))
    out, pr = [], []
    if not rf:
        return out, pr
    by = {}
    for e in events:
        if e['event'] != 'RESUME':
            continue
        if e['k'] is None or e['step'] is None:
            pr.append(f'ul_events.csv: RESUME 사건 k · step 숫자 아님 ({e["k"]} · {e["step"]}) — 승인 없음 (ULKRF-01)')
        elif e['step'] not in rf:
            pr.append(f'ul_events.csv: RESUME (k {e["k"]} · step {e["step"]}) 의 step ∉ 러너 resume_from {sorted(rf)} — 상충 · 승인 없음 (ULKRF-01)')
        else:
            by.setdefault(e['step'], []).append(e['k'])
    for s in sorted(by):
        ks = by[s]
        if len(ks) > 1:
            pr.append(f'ul_events.csv: 같은 경계 step {s} 의 RESUME 사건 {len(ks)} 줄 (k {ks}) — {"중복" if len(set(ks)) == 1 else "상충"} · '
                      '경계 하나에 승인 한 번 (중복 사건으로 늘리지 않는다) · 승인 없음 (ULKRF-01)')
            continue
        st = _state_vars(os.path.join(d, 'restart', f'state_unload_{s}.in'))
        if st.get('ul_rstep') == s and st.get('ul_k') == ks[0]:
            out.append((ks[0], s))
        else:
            pr.append(f'RESUME (k {ks[0]} · step {s}) ≠ 상태 파일 state_unload_{s}.in (ul_k {st.get("ul_k")} · ul_rstep {st.get("ul_rstep")}) — '
                      '상충 · 승인 없음 (ULKRF-01)')
    return out, pr


def _supersede(rows, auth, name, steps_csv=False):
    """이어 돌림 경계 (ULKRR-02 · ULKRF-01 · 02): 실패한 시도가 남긴 줄을 버리는 것 = 승인된 경계 (k_r, s_r) (_resume_auth · 고유) 에서만, 경계마다 한 번 —
    새 시도 시작 = 승인 경계 뒤 **먼저 오는 쪽**: step 역행 (step ≤ 앞 줄 · 창 CSV · 단 CSV) 또는 (단 CSV · steps_csv) k 가 되돌아옴 (k ≤ 앞 줄 k — 한 단 한 줄이라
    새 시도가 옛 시도보다 늦게 끝나도 (유지 창 수가 늘어도) 보인다 · ULKRF-02) · 그 줄 = 그 경계 새 시도의 첫 줄 (k = k_r + 1 · step > s_r) · 버릴 줄 = 끝의 step > s_r
    줄 전부 (k > k_r) · 버린 뒤 앞 줄 = 정확히 (k_r, s_r).  그 밖 중복 · 역행 · 되돌아옴 = 버리지 않고 문제 (→ 주 값 미식별) →
    (줄 · 버린 수 · 문제 · {경계: 그 경계에서 버린 옛 시도 줄} — 새 시도 시작이 식별된 경계만 · ULPR-01 _resume_tails 가 읽는다)."""
    kept, dropped, pr, used, by = [], 0, [], set(), {}
    for n, r in enumerate(rows, 1):
        s, k = r.get('step'), r.get('k')
        prev = kept[-1] if kept else None
        back = prev is not None and s is not None and prev.get('step') is not None and prev['step'] >= s
        kback = steps_csv and prev is not None and k is not None and prev.get('k') is not None and prev['k'] >= k
        if back or kback:
            ok = False
            for kr, sr in auth:
                if (kr, sr) in used or k != kr + 1 or s is None or not s > sr:
                    continue
                j = len(kept)
                while j > 0 and kept[j - 1].get('step') is not None and kept[j - 1]['step'] > sr:
                    j -= 1
                stale = kept[j:]
                if stale and j > 0 and all(x.get('k') is not None and x['k'] > kr for x in stale) \
                        and (kept[j - 1].get('k'), kept[j - 1].get('step')) == (kr, sr):
                    by[(kr, sr)] = list(stale)
                    del kept[j:]
                    dropped += len(stale)
                    used.add((kr, sr))
                    ok = True
                    break
            if not ok:
                what = (f'≤ 앞 줄 (k {prev.get("k")} · step {prev.get("step")})' if back else
                        f'k 가 앞 줄 k {prev.get("k")} 에서 되돌아옴 (step {prev.get("step")} → {s})')
                pr.append(f'{name} {n} 째 줄 (k {k} · step {s}) {what} — 승인된 이어 돌림 경계 (RESUME 사건 + 러너 resume_from + 상태 파일 k · 경계마다 한 번) '
                          '가 아닌 중복 · 역행 (ULKRR-02 · ULKRF-02)')
        kept.append(r)
    return kept, dropped, pr, by


#: 단 끝 사건 (ULPR-01) — 덱이 단 줄 바로 뒤 · 같은 hold 끝에 같은 (k, step) 으로 쓰는 사건 (in.UT · in.U_* · in.G_* 의 ul_hold_end → ul_end_hold0 · ul_end_search ·
#: ul_end_confirm · ul_rm · ul_rmstop · ul_tech · ul_nobracket · ul_next 의 LIFT_CAP).  창 사건 (SEPARATED · RECONTACT · POST_DONE · SEP_INCOMPLETE · GUARD) 은 그 창 끝
#: step 이라 넣지 않는다 (단 줄과 같은 step 이어도 그 단 줄을 쓴 시도의 증거가 아니다).
HOLD_END_EVENTS = frozenset({'HOLD0_DONE', 'MODE_B', 'CROSS', 'RM', 'RM_STOP', 'CONFIRMED', 'GRAVITY_HOLD_DONE', 'NO_BRACKET', 'TECH', 'LIFT_CAP'})


def _windows_match(line, wins):
    """단 줄 ↔ 그 단 창 기록 (덱 ul_hold_end — n_windows = 그 단 창 수 ul_w · step = 마지막 창 step · 단 줄 뒤 그 k 의 창 없음): 창 w = 1 … n_windows 정확히 ·
    마지막 창 step = 단 step (정수 대조 · 허용폭 없음)."""
    n = line.get('n_windows')
    return (bool(wins) and isinstance(n, int) and n >= 1 and [x.get('w') for x in wins] == list(range(1, n + 1))
            and wins[-1].get('step') is not None and wins[-1]['step'] == line.get('step'))


def _state_steps_after(d, sr):
    """restart/state_unload_<s>.in (s > s_r · ul_rstep = s) 의 s 집합 — 단 끝 restart · 상태 파일은 그 단을 끝낸 (ul_step_done 까지 간) 시도만 쓴다 ·
    러너는 마지막 restart_unload 에서 이어 돌리므로 s > s_r 의 상태 파일 = 이어 돌린 새 시도 (run_unload.sh RESUME · ULPR-01)."""
    rd = os.path.join(d, 'restart')
    out = set()
    for nm in sorted(os.listdir(rd)) if os.path.isdir(rd) else []:
        m = re.fullmatch(r'state_unload_([1-9][0-9]*)\.in', nm)   # 덱이 쓰는 꼴 그대로 (ASCII 숫자 · 앞 0 없음 — 다른 이름은 증거로 세지 않는다)
        if m and int(m.group(1)) > sr and _state_vars(os.path.join(rd, nm)).get('ul_rstep') == int(m.group(1)):
            out.add(int(m.group(1)))
    return out


def _resume_tails(d, auth, events, ev_old, windows, steps, w_old, s_old):
    """ULPR-01 (사전 공격 리뷰 10-21 PRE-UL-01 · 등록 §14-12): 승인된 경계 (k_r, s_r) 뒤 기록 줄은 **어느 시도가 썼는지 기록으로 증명될 때만** 정상 관측으로 쓴다
    (등록 §14-10 · §14-11 ① "끊긴 시도가 남긴 줄 = 승인 경계에서 버림 · 버린 행을 정상 관측으로 쓰지 않는다" — 행 교체 (_supersede) 는 새 시도가 그 CSV 에 줄을 다시
    써야만 옛 줄을 알아본다).  덱 쓰는 순서 (창 줄 → 단 줄 → 단 끝 사건 → 단 끝 restart_unload + 상태 파일) · 러너 = 마지막 restart_unload 에서 이어 돌림 ⇒
    옛 시도의 경계 뒤 줄 = 단 k_r + 1 줄뿐 · 새 시도 첫 창 step = 옛 시도 첫 창 step (같은 덱 · 같은 상태).
      새 시도 증거 = 창 · 단 기록 역행 (그 경계 행 교체) · 경계 뒤 k ≥ k_r + 2 줄 · RESUME 줄 뒤 사건 (step > s_r) · 요약 · 경계 뒤 단 끝 상태 파일 (state_unload_<s> · s > s_r).
      ② 새 시도 증거 없음 → 경계 뒤 줄 (k_r + 1 만) = 옛 시도 (경계 뒤 옛 사건을 버렸으면) 또는 시도 미확정 → 쓰지 않는다 (버린 줄 · 기록).
      ① 새 시도 증거 있음 · 단 기록 역행 없음 · k ≥ k_r + 2 없음 → 경계 뒤 단 줄 (k_r + 1) 은 새 시도 것으로 증명될 때만 쓴다 — 새 시도 증명 = 그 단 끝 상태 파일 ·
         RESUME 뒤 단 끝 사건 (같은 k · step) · (사건 증거가 없으면) 남은 창 (w 1 … n · 마지막 step) 과 맞고 버린 옛 창과는 다름 · 옛 시도 증명 = 버린 옛 단 끝 사건 ·
         버린 옛 창과만 맞음 → 버림 · 둘 다와 맞음 = 시도 미확정 → 버림 (보수) · 둘 다 증명 = 모순 → 문제.
      모순 = 경계 뒤 옛 사건이 있는데 창 기록 역행 (옛 시도 창) 이 없고 새 시도 증거는 있다 → 문제 (버리지 · 고르지 않는다) · 경계 뒤 k ≠ k_r + 1 줄을 증거 없이 → 문제.
      ③ 남은 경계 뒤 단 줄마다 = 그 단 창 기록과 맞아야 (_windows_match) — 아니면 문제 (시도 섞임 · 결손).
    → (창, 단, 버린 수, 문제, 경계마다 기록)."""
    pr, recs, ndrop = [], [], 0
    summ = os.path.exists(os.path.join(d, 'ul_summary.txt'))

    def drop(rows, gone):
        ids = {id(x) for x in gone}
        return [x for x in rows if id(x) not in ids]
    for kr, sr in sorted(auth, key=lambda b: b[1]):
        b, k1 = (kr, sr), kr + 1
        ri = next((i for i, e in enumerate(events) if e['event'] == 'RESUME' and (e['k'], e['step']) == b), None)
        new_ev = [e for e in (events[ri + 1:] if ri is not None else []) if e['step'] is not None and e['step'] > sr]
        old_ev = ev_old.get(b, [])
        tw = [x for x in windows if x.get('step') is not None and x['step'] > sr]
        ts = [x for x in steps if x.get('step') is not None and x['step'] > sr]
        states = _state_steps_after(d, sr)
        later = any(x.get('k') is not None and x['k'] > k1 for x in tw + ts)
        ev = {'windows_rollback': bool(w_old.get(b)), 'steps_rollback': bool(s_old.get(b)), 'later_stage': later, 'events_after_resume': bool(new_ev),
              'summary': summ, 'stage_state_files': bool(states)}
        rec = {'boundary': [kr, sr], 'new_attempt_evidence': sorted(k for k, v in ev.items() if v), 'old_events': [(e['event'], e['k'], e['step']) for e in old_ev],
               'dropped_windows': 0, 'dropped_steps': 0, 'why': []}
        tag = f'승인 경계 (k {kr} · step {sr}) 뒤'
        if not any(ev.values()):
            other = [(x.get('k'), x.get('step')) for x in tw + ts if x.get('k') != k1]
            if other:
                pr.append(f'{tag} 줄 {other[:3]} 이 단 k {k1} 가 아닌데 새 시도 증거가 없다 — 기록 결손 · 모순 · 버리지 않는다 (ULPR-01)')
            elif tw or ts:
                windows, steps = drop(windows, tw), drop(steps, ts)
                rec.update(dropped_windows=len(tw), dropped_steps=len(ts))
                rec['why'].append(('옛 시도 줄 (경계 뒤 옛 사건을 버렸다)' if old_ev else '시도 미확정 (옛 · 새 어느 시도 줄인지 기록으로 가를 수 없다)')
                                  + ' · 새 시도 증거 없음 → 정상 관측으로 쓰지 않는다 (ULPR-01 ②)')
        else:
            if old_ev and not w_old.get(b):
                pr.append(f'{tag} 옛 사건 {rec["old_events"][:3]} 이 있는데 창 기록 역행 (옛 시도 창 ↔ 새 시도 첫 창) 이 없다 · 새 시도 증거 {rec["new_attempt_evidence"]} '
                          '— 모순 · 버리지 · 고르지 않는다 (ULPR-01)')
            if not s_old.get(b) and not later and ts:
                L = ts[0]
                key = (L.get('k'), L.get('step'))
                if len(ts) == 1 and L.get('k') == k1:
                    new_pf = L.get('step') in states or any(e['event'] in HOLD_END_EVENTS and (e['k'], e['step']) == key for e in new_ev)
                    old_pf = any(e['event'] in HOLD_END_EVENTS and (e['k'], e['step']) == key for e in old_ev)
                    m_new = _windows_match(L, [x for x in windows if x.get('k') == k1])
                    m_old = _windows_match(L, [x for x in w_old.get(b, []) if x.get('k') == k1])
                    why = None
                    if new_pf and old_pf:
                        pr.append(f'{tag} 단 줄 (k {key[0]} · step {key[1]}) 을 옛 시도 (버린 단 끝 사건) 와 새 시도 (단 끝 사건 · 상태 파일) 가 둘 다 썼다 — 모순 (ULPR-01)')
                    elif not new_pf and old_pf:
                        why = '옛 시도 단 줄 (버린 옛 단 끝 사건과 같은 k · step)'
                    elif not new_pf and m_old and not m_new:
                        why = '옛 시도 단 줄 (버린 옛 창과만 맞는다)'
                    elif not new_pf and m_old and m_new:
                        why = '시도 미확정 단 줄 (옛 · 새 창 둘 다와 맞는다 · 사건 · 상태 파일 증거 없음)'
                    if why:
                        steps = drop(steps, [L])
                        rec['dropped_steps'] += 1
                        rec['why'].append(f'{why} (k {key[0]} · step {key[1]}) → 정상 관측으로 쓰지 않는다 (ULPR-01 ①)')
        ndrop += rec['dropped_windows'] + rec['dropped_steps']
        recs.append(rec)
    seen = set()
    for kr, sr in sorted(auth, key=lambda b: b[1]):
        for L in [x for x in steps if x.get('step') is not None and x['step'] > sr]:
            if id(L) in seen:
                continue
            seen.add(id(L))
            wins = [x for x in windows if x.get('k') == L.get('k')]
            if not _windows_match(L, wins):
                pr.append(f'ul_steps.csv: 승인 경계 (k {kr} · step {sr}) 뒤 단 줄 (k {L.get("k")} · step {L.get("step")} · n_windows {L.get("n_windows")}) ≠ '
                          f'그 단 창 기록 (w {[x.get("w") for x in wins][:14]} · 마지막 step {wins[-1].get("step") if wins else None}) — 시도 섞임 · 결손 · '
                          '정상 관측으로 쓰지 않는다 (ULPR-01 ③)')
    return windows, steps, ndrop, pr, recs


def _order_problems(rows, name, windows):
    """남은 기록 줄의 순서 (ULKRR-02): k · step (창이면 w) 숫자 · k 가 줄지 않음 · (창) 같은 k 안 w 증가 · (k, w) 고유 — 아니면 문제."""
    pr = []
    need = ('k', 'w', 'step') if windows else ('k', 'step')
    nonnum = [n for n, r in enumerate(rows, 1) if any(r.get(x) is None for x in need)]
    if nonnum:
        pr.append(f'{name} {nonnum[:3]} 째 줄 {"/".join(need)} 숫자 아님 (기록 결손 · ULKRR-02)')
        return pr
    for n, (a, b) in enumerate(zip(rows, rows[1:]), 2):
        if b['k'] < a['k']:
            pr.append(f'{name} {n} 째 줄 k {b["k"]} < 앞 줄 k {a["k"]} (역행 · ULKRR-02)')
            break
        if windows and b['k'] == a['k'] and b['w'] <= a['w']:
            pr.append(f'{name} {n} 째 줄 (k {b["k"]} · w {b["w"]}) ≤ 앞 줄 w {a["w"]} (중복 · 역행 · ULKRR-02)')
            break
    return pr


def read_run(d, P=None):
    P = P or ul_lib.load_params()
    R = P['records']
    out = {'dir': d, 'windows': [], 'steps': [], 'events': [], 'summary': None, 'problems': [], 'n_superseded_rows': 0, 'resume_steps': [],
           'resume_auth': [], 'resume_tails': []}
    ev, pr = _csv(os.path.join(d, 'ul_events.csv'), R['events_cols'])
    out['problems'] += pr
    events = [{'event': r['event'], 'k': _i(r['k']), 'step': _i(r['step']), 'plate_z': _f(r['plate_z']), 'lift': _f(r['lift']),
               'detail': r['detail']} for r in (ev or [])]
    out['resume_steps'] = [e['step'] for e in events if e['event'] == 'RESUME']
    auth, apr = _resume_auth(d, events)
    out['resume_auth'] = auth
    out['problems'] += apr
    kept, used, ev_old = [], set(), {}
    for e in events:   # 승인된 RESUME 앞에 실패한 시도가 남긴 그 step 뒤 사건 (k > k_r) 만 버린다 · 경계마다 한 번 (ULKRR-02 · ULKRF-01 — 아니면 버리지 않고 문제)
        if e['event'] == 'RESUME' and e['step'] is not None:
            stale = [x for x in kept if x['step'] is not None and x['step'] > e['step']]
            b = (e['k'], e['step'])
            if stale and b in auth and b not in used and all(x['k'] is not None and x['k'] > e['k'] for x in stale):
                kept = [x for x in kept if x['step'] is None or x['step'] <= e['step']]
                used.add(b)
                ev_old[b] = stale   # ULPR-01 — 그 경계에서 버린 옛 시도 사건 (옛 시도가 경계 뒤에 썼다는 증거 · 옛 단 끝 사건 = 옛 단 줄)
            elif stale:
                out['problems'].append(f'ul_events.csv: RESUME (k {e["k"]} · step {e["step"]}) 앞 사건 {len(stale)} 개가 그 step 뒤 — 승인된 이어 돌림 경계 '
                                       '(러너 resume_from + 상태 파일 k · 경계마다 한 번 · 버릴 사건 k > k_r) 가 아니어서 버리지 않는다 (ULKRR-02 · ULKRF-01)')
        kept.append(e)
    out['events'] = kept
    csv_pr, sup_pr, sup_by = {}, {}, {}
    for name, key, cols in (('ul_windows.csv', 'windows', R['windows_cols']), ('ul_steps.csv', 'steps', R['steps_cols'])):
        rows, csv_pr[key] = _csv(os.path.join(d, name), cols)
        conv = []
        for r in rows or []:
            c = {}
            for k, v in r.items():
                c[k] = v if k in ('arm', 'bed', 'kind') else _f(v)
            for k in ('k', 'w', 'phase', 'step', 'n_windows', 'n_move', 'steady', 'modeB', 'n_contact_geo', 'n_contact_last', 'atoms', 'leak'):
                if k in c and c[k] is not None:
                    c[k] = int(round(c[k]))
            conv.append(c)
        conv, dropped, sup_pr[key], sup_by[key] = _supersede(conv, auth, name, steps_csv=(key == 'steps'))
        out[key] = conv
        out['n_superseded_rows'] += dropped
    tpr = []
    if auth:   # ULPR-01 — 승인 경계 뒤 줄 = 어느 시도가 썼는지 기록으로 증명될 때만 (새 시도가 그 CSV 를 다시 쓰기 전에 끝난 경우 · 시도 미확정)
        out['windows'], out['steps'], nd, tpr, out['resume_tails'] = _resume_tails(d, auth, kept, ev_old, out['windows'], out['steps'], sup_by['windows'],
                                                                                   sup_by['steps'])
        out['n_superseded_rows'] += nd
    for name, key in (('ul_windows.csv', 'windows'), ('ul_steps.csv', 'steps')):   # 문제 순서 = 옛 판 그대로 (CSV 마다 파서 → 행 교체 · 순서) · 그 뒤 경계 뒤 줄 (ULPR-01)
        out['problems'] += csv_pr[key] + sup_pr[key] + ([] if sup_pr[key] else _order_problems(out[key], name, key == 'windows'))
    out['problems'] += tpr
    sp = os.path.join(d, 'ul_summary.txt')
    out['summary'] = ul_lib.read_kv(sp) if os.path.exists(sp) else None
    return out


def parent_sums(src):
    """UTc 의 부모 (UT) 관측 파일 sha256 목록 (sha256sum 꼴 · 상대 경로 · 정렬) — 러너가 UTc 시작 때 한 번 쓴다 (개정 3 §14-3 · ULKR-03).
    대상 = 기록 CSV · 요약 · 화면 · 로그 · 덱 사본 · 단계 · 잡 기록 · dump/ 전부 · restart/state_*.in · restart_RM_*.bin.
    뺀다 = 단 끝 restart_unload_*.bin 등 다른 .bin (판독기가 읽지 않는다 · 크다) · arm_verdict.json (판독기 산출물 — 다시 읽으면 바뀐다)."""
    lines = []
    for dp, dn, fn in os.walk(src):
        dn.sort()
        for name in sorted(fn):
            p = os.path.join(dp, name)
            rel = os.path.relpath(p, src).replace(os.sep, '/')
            if not os.path.isfile(p) or os.path.islink(p) or rel == 'arm_verdict.json':
                continue
            if rel.endswith('.bin') and not re.fullmatch(r'restart/restart_RM_\d+\.bin', rel):
                continue
            lines.append(f'{ul_lib.sha256_file(p)}  {rel}')
    return '\n'.join(lines) + ('\n' if lines else '')


def _continuation(d):
    """UTc → 부모 UT (run_manifest 의 continues · parent_dir · rm_step · parent_sums · parent_sums_sha256) — 목록 · 작은 기록 파일 sha256 대조
    (큰 덤프는 처음 쓸 때 _cont_path 가 대조) → {'status': OK | FAIL, 'dir', 'rm_step', 'sums', 'checked', 'problems'}."""
    out = {'status': 'FAIL', 'dir': None, 'rm_step': None, 'sums': {}, 'checked': {}, 'problems': []}
    kv = ul_lib.read_kv(os.path.join(d, 'run_manifest.txt'))
    pdir, rm = kv.get('parent_dir'), _i(kv.get('rm_step'))
    sp = os.path.join(d, kv.get('parent_sums') or 'parent_UT.sha256')
    if kv.get('continues') != 'UT' or not pdir or rm is None:
        out['problems'].append('run_manifest 에 continues=UT · parent_dir · rm_step 없음 (개정 3 §14-3 러너가 쓴다)')
        return out
    if not os.path.isdir(pdir) or not os.path.exists(sp):
        out['problems'].append(f'부모 폴더 · sha256 목록 없음 ({pdir} · {os.path.basename(sp)})')
        return out
    if kv.get('parent_sums_sha256') != ul_lib.sha256_file(sp):
        out['problems'].append('부모 sha256 목록 파일 자체의 sha256 ≠ run_manifest 기록')
        return out
    for ln in open(sp, encoding='utf-8').read().splitlines():
        if not ln.strip():
            continue
        h, rel = ln.split(None, 1)
        rel = rel.strip().lstrip('*')
        if rel in out['sums'] or rel.startswith('/') or '..' in rel.split('/'):
            out['problems'].append(f'부모 sha256 목록의 경로 이상 · 중복: {rel}')
            return out
        out['sums'][rel] = h
    out.update(dir=pdir, rm_step=rm)
    for rel in ('ul_windows.csv', 'ul_steps.csv', 'ul_events.csv', f'restart/state_RM_{rm}.in'):
        if _cont_path(out, rel) is None:
            out['problems'].append(f'부모 필수 파일 {rel} 목록 밖 · sha256 다름')
    for rel in sorted(out['sums']):
        if re.fullmatch(r'screen(_a\d+)?\.txt', rel):
            _cont_path(out, rel)
    out['status'] = 'OK' if not out['problems'] else 'FAIL'
    return out


def _cont_path(cont, rel):
    """부모 파일 경로 — 목록에 있고 sha256 이 같을 때만 (처음 쓸 때 대조 · 다르면 관측 결손 + 이어 돌림 무효 · 목록 밖 = 관측 결손)."""
    if rel not in cont['sums']:
        return None
    if rel not in cont['checked']:
        p = os.path.join(cont['dir'], rel)
        ok = os.path.isfile(p) and ul_lib.sha256_file(p) == cont['sums'][rel]
        cont['checked'][rel] = ok
        if not ok:
            cont['problems'].append(f'부모 파일 sha256 다름 · 없음: {rel}')
            cont['status'] = 'FAIL'
    return os.path.join(cont['dir'], rel) if cont['checked'][rel] else None


def _read_run_cont(d, cont, P):
    """UTc 기록 = 부모 UT 기록 (≤ R_M · 해시 대조된 CSV) + UTc 자기 기록 (> R_M) — 경계 중복 · 누락 검사 (개정 3 §14-3)."""
    par, own = read_run(cont['dir'], P), read_run(d, P)
    rm, pr = cont['rm_step'], []
    rm_ev = [e for e in par['events'] if e['event'] == 'RM']
    k_rm = rm_ev[0]['k'] if len(rm_ev) == 1 else None
    if len(rm_ev) != 1 or rm_ev[0]['step'] != rm:
        pr.append(f'부모 RM 사건 {[(e["k"], e["step"]) for e in rm_ev]} ≠ rm_step {rm}')
    if not par['steps'] or par['steps'][-1]['step'] != rm or par['steps'][-1]['k'] != k_rm:
        pr.append('부모 단 기록의 끝 ≠ R_M 단 (부모 기록 끝 · 누락)')
    if any(w.get('step') is None or w['step'] > rm for w in par['windows']):
        pr.append('부모 창 기록이 R_M 뒤에도 있다')
    if any(r.get('step') is None or r['step'] <= rm for r in own['windows'] + own['steps']):
        pr.append('UTc 기록 중 R_M step 이하 (경계 중복 — 부모 기록을 복사하지 않는다)')
    if k_rm is not None and own['windows'] and (own['windows'][0].get('k'), own['windows'][0].get('w')) != (k_rm + 1, 1):
        pr.append(f'UTc 첫 창 (k {own["windows"][0].get("k")} · w {own["windows"][0].get("w")}) ≠ (k_RM + 1 · w 1) (경계 누락)')
    if k_rm is not None and own['steps'] and own['steps'][0].get('k') != k_rm + 1:
        pr.append(f'UTc 첫 단 k {own["steps"][0].get("k")} ≠ k_RM + 1 (경계 누락)')
    rs = [e for e in own['events'] if e['event'] == 'RESUME']
    if not rs or rs[0]['step'] != rm or rs[0]['k'] != k_rm:
        pr.append('UTc 의 RESUME 사건 ≠ (k_RM · R_M step)')
    if pr:
        cont['problems'] += pr
        cont['status'] = 'FAIL'
    return {'dir': d, 'windows': par['windows'] + own['windows'], 'steps': par['steps'] + own['steps'], 'events': par['events'] + own['events'],
            'summary': own['summary'], 'problems': [f'부모 {x}' for x in par['problems']] + own['problems'],
            'n_superseded_rows': par['n_superseded_rows'] + own['n_superseded_rows'], 'resume_steps': own['resume_steps'],
            'resume_tails': [dict(x, part='parent_UT') for x in par.get('resume_tails', [])] + own.get('resume_tails', [])}


def window_states(windows, wall_by_step, P=None):
    """창마다 판 접촉 상태 — 벽 local 덤프 (창 끝) 의 접촉 수 · 창 평균 압력 (덱 → 보고 MPa) · 인장 합 (N · 판이 입자를 끌어올리는 쪽)."""
    P = P or ul_lib.load_params()
    sign = P['plate_fn_compressive_sign']
    scale = P['units']['report_MPa_per_Ps']
    out = []
    for w in windows:
        step = w.get('step')
        Pd = _f(w.get('Ps_avg'))
        Pr = Pd * scale if Pd is not None else None
        rows = wall_by_step.get(step)
        rec = {'step': step, 'P_MPa': Pr, 'n': None, 'tension_N': None, 'compress_N': None, 'n_geo': w.get('n_contact_geo')}
        if rows is None:
            rec['state'] = 'OBS_MISSING'
        else:
            fz = [_f(r.get('fnz')) for r in rows]
            if any(x is None for x in fz):
                rec['state'] = 'OBS_MISSING'
                out.append(rec)
                continue
            rec['n'] = len(rows)
            rec['tension_N'] = sum(abs(x) for x in fz if x * sign < 0)
            rec['compress_N'] = sum(abs(x) for x in fz if x * sign > 0)
            if not rows:
                rec['state'] = 'ZERO'
            elif Pr is None:
                rec['state'] = 'OBS_MISSING'
            else:
                rec['state'] = 'CONTACT' if Pr > 0 else 'TENSION'
        out.append(rec)
    return out


def _contiguous(a, b, w_steps):
    """같은 k 의 앞 창 a → 이 창 b 가 이어지는가 (Q4 가 · 판정문 §6-1): w = 앞 w + 1 · (w_steps 가 있으면) 창 끝 step 간격 = 그 팔 창 W."""
    if a.get('w') is None or b.get('w') is None or b['w'] != a['w'] + 1:
        return False
    if w_steps is None:
        return True
    return a.get('step') is not None and b.get('step') is not None and b['step'] - a['step'] == w_steps


def _arm_wsteps(d, job, P):
    """그 팔의 창 W (step) — 런 폴더의 덱 사본 (deck.liggghts · 덱이 증거 · ULR1-04) · 없으면 표 (W0 ÷ 그 팔 dt_factor · 중력 팔 = 부모 · UTc = UT3)."""
    p = os.path.join(d, 'deck.liggghts')
    if os.path.isfile(p):
        w = deck_windows(open(p, encoding='utf-8', errors='replace').read())['W']
        if w:
            return w
    arm = job[2:] if job.startswith('G_') else ('UT3' if job == 'UTc' else job)
    a = P['arms'].get(arm) or {}
    return int(round(P['windows']['W0'] / a['dt_factor'])) if a.get('dt_factor') else None


def separation(states, sepreq=2, w_steps=None):
    """§13-3: 연속 sepreq 개 ZERO 창의 마지막 창 끝 = 분리 선언 · 그 창부터 분리 뒤 창 · 재접촉 (CONTACT · TENSION) 이면 계수 · 분리 뒤 창 초기화 ·
    OBS_MISSING 은 0 이 아니다 (연속을 끊는다 · 분리 뒤면 그 분리의 표면 관측도 끊긴다).
    덱과 같은 규칙 (개정 3 §14-7 · ULKR-07) — 창에 k · 단계가 있으면: 판 이동 (k 바뀜) = 연속 계수 초기화 (덱 ul_hold_start 의 ul_sepn 0 ·
    표 separation.reset_on_move) · 분리 뒤 이동이면 그 분리는 끝 · 선언은 SEPARATE 단계 (2) 창에서만 (덱 ul_win_sep).
    Q4 (가 · 판정문 §6-1): 창에 w 가 있으면 같은 k 안 앞 창 → 이 창이 고유 · 연속 w (앞 + 1) 이고 · w_steps (그 팔 창 W) 가 있으면 창 끝 step 간격 = W —
    아니면 빈 구간 (gap_index) = OBS_MISSING 처럼 연속을 끊는다 (CSV 줄 인접 ≠ 물리 창 연속 · 예산 끝 선언 → 분리 뒤 4 창은 그대로)."""
    out = {'declared_index': None, 'declared_step': None, 'recontact_index': [], 'missing_index': [], 'moved_index': [], 'gap_index': [],
           'separated_final': False, 'post_windows': []}
    run, sep, prev_k, prev = 0, False, None, None
    for i, s in enumerate(states):
        st = s['state']
        k = s.get('k')
        if k is not None:
            if prev_k is not None and k != prev_k:
                run = 0
                if sep:
                    out['moved_index'].append(i)
                    sep = False
                    out['post_windows'] = []
            elif prev is not None and prev_k is not None and 'w' in s and 'w' in prev and not _contiguous(prev, s, w_steps):
                out['gap_index'].append(i)
                run = 0
                if sep:
                    sep = False
                    out['post_windows'] = []
            prev_k = k
        prev = s
        if st == 'ZERO':
            run += 1
            if sep:
                out['post_windows'].append(i)
            elif run >= sepreq and s.get('phase') in (None, 2):
                sep = True
                out['declared_index'], out['declared_step'] = i, s['step']
                out['post_windows'] = [i]
            continue
        run = 0
        if st == 'OBS_MISSING':
            out['missing_index'].append(i)
        else:
            if sep:
                out['recontact_index'].append(i)
        if sep:
            sep = False
            out['post_windows'] = []
    out['separated_final'] = sep
    return out


def crossings(steps, Pm):
    """연속 두 단 (둘 다 유한 P) 의 P − P_meas 부호 바뀜 (> ↔ ≤) → [(i, j)]."""
    out = []
    for i in range(len(steps) - 1):
        a, b = steps[i]['P'], steps[i + 1]['P']
        if a is None or b is None:
            continue
        if (a > Pm) != (b > Pm):
            out.append((i, i + 1))
    return out


def interp_rho(a, b, Pm, h0_um):
    """두 단 (lift_um · P) 사이 P_meas 의 선형 보간 → (ρ %, 괄호 µm, 괄호 %) · 분모 0 · 비유한 = (None, …)."""
    la, lb, pa, pb = a['lift_um'], b['lift_um'], a['P'], b['P']
    br = [min(la, lb), max(la, lb)] if la is not None and lb is not None else None
    brp = [100.0 * x / h0_um for x in br] if br else None
    if None in (la, lb, pa, pb) or pa == pb:
        return None, br, brp
    hc = la + (pa - Pm) / (pa - pb) * (lb - la)
    return 100.0 * hc / h0_um, br, brp


def _wall_rows(path, step=None, cols=WALL_U):
    """창 끝 벽 local 덤프 → 접촉 목록 · 없음 · 깨짐 (머리 · 열 · 행 수 · 비유한) · 머리 step ≠ 요청 창 끝 = None (OBS_MISSING — 0 으로 세지 않는다 · ULKR-04)."""
    if not path or not os.path.exists(path):
        return None
    d = ul_lib.read_dump(path, 'local', [f'c_ul_wh[{c}]' for c in range(1, len(cols) + 1)])
    if not d['ok'] or (step is not None and d['step'] != step):
        return None
    return [{n: r[f'c_ul_wh[{c}]'] for c, n in enumerate(cols, 1)} for r in d['rows']]


def _s0_dump(root, bed, P):
    """S0 원자 덤프 (in/atom_<S0>.liggghts — 10:0 은 s0_decision 의 S0′ 프레임) → (덤프 | None, S0) — 전부 읽힘 · 머리 step = S0 · 고유 ID 일 때만 (ULKR-04)."""
    s0 = _bed_s0(root, bed, P)
    if s0 is None:
        return None, None
    cand = [os.path.join(root, bed, 'in', f'atom_{s0}.liggghts'), os.path.join(root, bed, 'EXT', 'post', f'atom_{s0}.liggghts'),
            os.path.join(root, bed, 'EXT2', 'post', f'atom_{s0}.liggghts')]
    for p in cand:
        if os.path.exists(p):
            d = ul_lib.read_dump(p, 'custom')
            ids = ul_lib.ids_of(d['rows'])[0] if d['ok'] else None   # 파서 · 필수 열 문제 먼저 · ID = 정확한 양의 정수 (ULKRR-04)
            if ids is not None and d['rows'] and d['step'] == s0 and len(set(ids)) == len(ids):
                return d, s0
            return None, s0
    return None, s0


def _s0_frame(root, bed, P):
    """S0 원자 → (id 집합, 원자 목록, step) — _s0_dump 와 같은 자격 (ULKR-04)."""
    d, s0 = _s0_dump(root, bed, P)
    if d is None:
        return None, None, s0
    return {int(r['id']) for r in d['rows']}, d['rows'], s0


A_PS = 0.0025   # 덱 Ps 식의 면적 글자 (덱 m² — f_top_mesh[3] / 0.0025 / 1e6) · W_proxy 의 힘 = P̄ · A_PS (압력과 같은 면적)


def _aux_eps_w(v, steps, cross, s0d, fp, s0_ids, h0, P):
    """ε_sphere · W_proxy (§12-9 · 개정 3 §14-8 · Q7 · ULKR-12) — 보조 관측 (주 ρ 무영향) → (eps, w_proxy_J, w_proxy).
    ε: C_all = 검증한 S0 프레임 (전부 읽힘 · 머리 step · 고유 ID · 유한 양의 반경) 에서 봉인한 Σ V ÷ A (A = S0 상자 x · y) — 프레임마다 다시 계산하지 않는다 ·
       자리 = S0 (판 h0) · 첫 교차 끝점 둘 (단 끝 프레임 — S0 ID 전부 · 같은 반경 아니면 그 자리 NOT_COMPUTED) · M (보간 높이 · ε_all 만 · 주 값 OK 일 때).
    W_proxy: 주 값 OK · 단 k 0 … k* − 1 연속 · 전부 정상 (S1 ∧ S2) · 유한 → 정착 단 사다리꼴 + 끝 조각 k* − 1 → M (P_meas) · A_PS × 1e-6 = 보고 J
       (판이 받은 일 아님) · 아니면 None (0 J 아님)."""
    scale = P['units']['report_MPa_per_Ps']
    Pm = P['P_meas_report_MPa']
    ok_cross = isinstance(cross, tuple) and len(cross) == 2 and all(isinstance(x, int) for x in cross)
    okM = v['primary_status'] == 'OK' and v['rho_pct'] is not None and ok_cross
    hM = h0 * (1.0 + v['rho_pct'] / 100.0) if okM else None
    eps = {'status': 'NOT_COMPUTED', 'C_all_m': None, 'area_m2': None, 'n_s0': None, 'S0': None, 'endpoints': [], 'M': None, 'why': []}
    vol = ul_observers.s0_volumes(s0d['rows']) if s0d else None
    box = (s0d or {}).get('box')
    area = (box[0][1] - box[0][0]) * (box[1][1] - box[1][0]) if box and len(box) >= 2 else None
    if vol is None or area is None or not area > 0:
        eps['why'].append('S0 프레임 봉인 없음 (결손 · 중복 · 비유한 반경 · 상자 없음) — ε 미계산')
    else:
        s0e = ul_observers.eps_sphere(s0d['rows'], vol, area, h0)
        eps.update(status='OK', C_all_m=s0e['C_all'], area_m2=area, n_s0=len(vol),
                   S0=dict({k: s0e[k] for k in ('status', 'eps_all', 'eps_inside', 'n_inside')}, h_m=h0))
        if ok_cross:
            for x in cross:
                s = steps[x]
                rec = {'k': s['k'], 'step': s['step'], 'h_m': s['plate_z'], 'status': 'NOT_COMPUTED', 'eps_all': None, 'eps_inside': None,
                       'n_inside': None, 'why': []}
                A, pr = _atom_frame(fp(f'dump/atom_{s["step"]}.dump', s['step']), s['step'], s0_ids)
                if A is None or s['plate_z'] is None:
                    rec['why'] = pr or ['판 높이 비유한']
                else:
                    e = ul_observers.eps_sphere(A['rows'], vol, area, s['plate_z'])
                    rec.update({k: e[k] for k in ('status', 'eps_all', 'eps_inside', 'n_inside')}, why=e['why'])
                eps['endpoints'].append(rec)
        if okM:
            e = ul_observers.eps_sphere(None, vol, area, hM)
            eps['M'] = {'h_m': hM, 'status': e['status'], 'eps_all': e['eps_all'], 'eps_inside': None}
    w = {'status': 'NOT_COMPUTED', 'n_points': 0, 'why': []}
    wJ = None
    if not okM:
        w['why'].append('주 값 OK 아님 — M (보간 높이) 없음')
    else:
        rng = steps[:cross[0] + 1]
        bad = [s['k'] for s in rng if not s['steady'] or s.get('P_deck') is None or s['plate_z'] is None]
        if [s['k'] for s in rng] != list(range(len(rng))):
            w['why'].append(f'단 k 0 … k* − 1 불연속 ({[s["k"] for s in rng][:8]})')
        if bad:
            w['why'].append(f'구간 (k 0 → M) 비정상 · 비유한 단 k {bad[:5]}')
        if not w['why']:
            pts = [(s['plate_z'], s['P_deck']) for s in rng] + [(hM, Pm / scale)]
            wJ = ul_observers.w_proxy(pts, A_PS)
            w.update(status='OK' if wJ is not None else 'NOT_COMPUTED', n_points=len(pts))
    return eps, wJ, w


def _atom_frame(path, step, s0_ids=None):
    """창 · 단 끝 원자 덤프 (덱 꼴 열) — 전부 읽힘 · 머리 step = 요청 · 고유 ID · (주면) S0 에 없는 ID 없음 → (덤프 | None, 문제).
    합법적 공간 제외 (S0 ID ∩ 프레임 ∩ [0, 판]) 는 쓰는 쪽 몫이고 깨진 프레임은 여기서 거부한다 (ULKR-04)."""
    if not path or not os.path.exists(path):
        return None, [f'원자 덤프 없음 ({os.path.basename(path or "")})']
    A = ul_lib.read_dump(path, 'custom', ATOM_COLS)
    pr = list(A['problems'][:2])
    if A['step'] != step:
        pr.append(f'원자 덤프 머리 step {A["step"]} ≠ 요청 {step}')
    if not A['ok']:   # 파서 · 필수 열 문제를 먼저 돌려준다 (ULKRR-04 — 열 결손이면 id 를 읽지 않는다 · 예외 없음)
        return None, pr or ['원자 덤프 읽기 실패']
    ids, ipr = ul_lib.ids_of(A['rows'])
    if ids is None:   # 소수 · 0 이하 ID = 정수로 자르지 않는다 (ULKRR-04)
        return None, pr + [f'원자 덤프 {x}' for x in ipr]
    if len(set(ids)) != len(ids):
        pr.append('원자 ID 중복')
    if s0_ids is not None and set(ids) - s0_ids:
        pr.append(f'S0 에 없는 원자 ID {len(set(ids) - s0_ids)}')
    return (A if not pr else None), pr


def _bed_s0(root, bed, P):
    B = P['beds'][bed]
    if B['s0'] is not None:
        return B['s0']
    dec = _readjson(os.path.join(root, B100, 's0_decision.json')) if root else None
    return dec.get('s0') if dec and dec.get('status') == 'PASS' else None


def _readjson(p):
    try:
        return json.load(open(p, encoding='utf-8'))
    except (OSError, ValueError):
        return None


def _arm_g(job, P):
    """S3 무게 항의 g = 그 팔의 실제 중력 (개정 3 §14-6 · Q5 · ULKR-10 B) — 중력 팔 G_* = 표 g_aux (덱이 R_M 뒤 바꾼 중력) · 그 밖 = 표 S3 g."""
    return P['g_aux'] if job.startswith('G_') else P['s3']['g']


def _hold_wmax(job, P):
    """B 단 유지 예산 (창 수 상한) = 표 budget_max × 그 팔의 hold_factor (중력 팔 = 부모 팔 · UTc = UT 덱) — 분리 선언은 이 안이어야 한다 (개정 3 §14-7)."""
    arm = job[2:] if job.startswith('G_') else ('UT' if job == 'UTc' else job)
    return P['windows']['budget_max'] * P['arms'][arm]['hold_factor']


def _s3_at(d, step, plate_z, s0_ids, g=ul_s3.G, ap=None, cp=None):
    """단 끝 S3 — 원자 · 쌍 덤프 전부 읽힘 · 두 머리 step = 요청 step (서로 같은 것만으로는 아니다) · 고유 ID · S0 에 없는 ID 없음 (ULKR-04) ·
    무게 항 g = 그 팔의 실제 중력 (Q5 · ULKR-10 B)."""
    ap = ap or (os.path.join(d, 'dump', f'atom_{step}.dump') if d else None)
    cp = cp or (os.path.join(d, 'dump', f'contact_{step}.dump') if d else None)
    if s0_ids is None or not (ap and cp and os.path.exists(ap) and os.path.exists(cp)):
        return {'status': 'NOT_COMPUTED', 'why': ['S3 입력 덤프 · S0 집합 없음']}
    A, pr = _atom_frame(ap, step, s0_ids)
    C = ul_lib.read_dump(cp, 'local', CPL_COLS)
    pr += C['problems'][:2]
    if C['step'] != step:
        pr.append(f'쌍 덤프 머리 step {C["step"]} ≠ 요청 {step}')
    if A is None or pr:
        return {'status': 'NOT_COMPUTED', 'why': pr}
    con = []
    for r in C['rows']:
        i1, i2 = ul_lib.exact_id(r['c_cpl[7]']), ul_lib.exact_id(r['c_cpl[8]'])
        if i1 is None or i2 is None:   # 쌍 참조도 정확한 양의 정수 (ULKRR-04 — 잘라서 다른 원자에 붙이지 않는다)
            return {'status': 'NOT_COMPUTED', 'why': [f'쌍 덤프 참조 ID ({r["c_cpl[7]"]!r} · {r["c_cpl[8]"]!r}) 가 유한 · 양의 정확한 정수가 아니다']}
        con.append({'id1': i1, 'id2': i2, 'fx': r['c_cpl[10]'], 'fy': r['c_cpl[11]'], 'fz': r['c_cpl[12]']})
    return ul_s3.s3_residual(A['rows'], con, s0_ids, plate_z, atom_step=A['step'], contact_step=C['step'], g=g)


def _thermo(d):
    txt = ''
    for name in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        if re.fullmatch(r'screen(_a\d+)?\.txt', name):
            txt += open(os.path.join(d, name), encoding='utf-8', errors='replace').read() + '\n'
    return ul_lib.parse_thermo(txt)


def deck_windows(deck_text):
    """생성된 덱 → 창 W (step) · dt (마지막 숫자 정의) · T_W = W · dt (ULR1-04 — 덱이 증거)."""
    var = {}
    for ln in ul_lib.logical_lines(deck_text):
        w = ln.split()
        if w[:1] == ['variable'] and len(w) >= 4 and w[2] in ('equal', 'index') and re.fullmatch(r'[-+0-9.eE]+', w[3]):
            var[w[1]] = float(w[3])
    W, dt = var.get('ul_W'), var.get('dt')
    return {'W': int(W) if W else None, 'dt': dt, 'T_W': W * dt if W and dt else None}


def arm_verdict(d, bed, job, P=None, root=None):
    """팔 런 폴더 → 판정 (§12-3 · §13-1 · §13-2 · §13-3 · §13-5) — 덱의 단 기록 + 창 끝 덤프 (벽 · 원자 · 쌍) + thermo."""
    P = P or ul_lib.load_params()
    root = root or os.path.dirname(os.path.dirname(d))
    cont = _continuation(d) if job == 'UTc' else None          # 개정 3 §14-3 — UT 부모 관측 (경로 + sha256 · 복사 없음)
    run = _read_run_cont(d, cont, P) if (cont and cont['dir']) else read_run(d, P)
    Pm = P['P_meas_report_MPa']
    scale = P['units']['report_MPa_per_Ps']
    um = P['units']['um_per_deck_m']
    conf = P['protocol']['confirm_steps']
    h0_um = P['beds'][bed]['h0'] * um
    N_per_MPa = A_PS * 1e6 / scale   # 1 보고 MPa = 0.001 덱 MPa → 0.001 × 0.0025 m² × 1e6 = 2.5 N (덱 Ps 식의 A · 1e6)
    s0d, _s0 = _s0_dump(root, bed, P)
    s0_ids, s0_atoms = ({int(r['id']) for r in s0d['rows']}, s0d['rows']) if s0d else (None, None)
    v = {'job': job, 'bed': bed, 'dir': d, 'problems': list(run['problems']), 'n_superseded_rows': run['n_superseded_rows'],
         'resume_tails': run.get('resume_tails', []), 'primary_status': None, 'rho_pct': None, 'bracket_um': None, 'bracket_pct': None, 'union_bracket_um': None, 'union_bracket_pct': None,
         'lower_bound_pct': None, 'nonmonotone': False, 'cancellation': None, 'disposition': None, 'rank_eligible': False,
         'endpoint_states': [], 'sigma_P': None, 'trajectory_status': None, 'separation': None, 's4_status': 'NOT_COMPUTED', 'why': []}
    gravity = job.startswith('G_')
    g_arm = _arm_g(job, P)

    def fp(rel, step):
        """관측 파일 — UTc 의 R_M step 이하 = 부모 UT (목록 · sha256 대조) · 그 밖 = 이 런 폴더."""
        if cont is not None and cont['dir'] and step is not None and step <= cont['rm_step']:
            return _cont_path(cont, rel)
        return os.path.join(d, rel)

    def thermo_regular():
        if cont is None or not cont['dir']:
            return _thermo(d)['regular']
        rm = cont['rm_step']
        txt = ''
        for rel in sorted(cont['sums']):
            if re.fullmatch(r'screen(_a\d+)?\.txt', rel) and _cont_path(cont, rel):
                txt += open(_cont_path(cont, rel), encoding='utf-8', errors='replace').read() + '\n'
        reg = {k: r for k, r in ul_lib.parse_thermo(txt)['regular'].items() if k <= rm}
        own = _thermo(d)['regular']
        if any(k <= rm for k in own):
            cont['problems'].append('UTc thermo 정규 줄 중 R_M step 이하 (경계 중복)')
            cont['status'] = 'FAIL'
        reg.update({k: r for k, r in own.items() if k > rm})
        return reg
    summ = run['summary']
    res = (summ or {}).get('result')
    v['trajectory_status'] = {'DONE': 'DONE', 'LIFT_CAP': 'LIFT_CAP', 'GUARD': 'GUARD', 'TECH': 'TECH', 'RM_STOP': 'RM_STOP',
                              'SEP_INCOMPLETE': 'SEP_INCOMPLETE'}.get(res, 'TIMEOUT')
    wins = run['windows']
    walls = {w['step']: _wall_rows(fp(f'dump/wall_{w["step"]}.dump', w['step']), w['step']) for w in wins if w.get('step') is not None}
    states = window_states(wins, walls, P)
    for st, w in zip(states, wins):
        st['k'], st['w'], st['phase'] = w.get('k'), w.get('w'), w.get('phase')
    steps = []
    for s in run['steps']:
        Pb = s.get('Pbar')
        steps.append({'k': s.get('k'), 'kind': s.get('kind'), 'step': s.get('step'), 'lift_um': (s['lift'] * um) if s.get('lift') is not None else None,
                      'plate_z': s.get('plate_z'), 'P': Pb * scale if Pb is not None else None, 'P_deck': Pb, 'steady': s.get('steady') == 1,
                      'phase': s.get('phase')})
    last_state = {}
    for st in states:
        last_state[st['k']] = st
    # 기록 자체의 결손 (ULKR-04 · 개정 3 §14-10) — CSV 가 버린 줄 · 머리 ≠ 표 · 단 k 불연속 (누락 · 중복 · 순서) 이면 주 값을 내지 않는다
    rec_why = []
    if run['problems']:
        rec_why.append(f'CSV 기록 결손 · 무결성 ({" · ".join(run["problems"][:3])}) — 버린 줄 · 승인 안 된 중복 · 역행 줄을 정상 기록으로 쓰지 않는다')
    ks = [s['k'] for s in steps]
    if ks and ks != list(range(len(ks))):
        rec_why.append(f'단 기록 k 불연속 ({ks[:12]}) — 누락 · 중복 · 순서')

    def endpoint(i, contact=True):
        s = steps[i]
        why = []
        if s['P'] is None or s['lift_um'] is None:
            why.append(f'단 {s["k"]} P̄ · 높이 비유한')
        if not s['steady']:
            why.append(f'단 {s["k"]} UNSTEADY (S1 ∧ S2 두 창 없음)')
        s3 = _s3_at(None, s['step'], s['plate_z'], s0_ids, g_arm, ap=fp(f'dump/atom_{s["step"]}.dump', s['step']),
                    cp=fp(f'dump/contact_{s["step"]}.dump', s['step']))
        s['s3'] = s3['status']
        if s3['status'] != 'PASS':
            why.append(f'단 {s["k"]} S3 {s3["status"]}' + (f' ({s3["why"][0]})' if s3.get('why') else ''))
        st = last_state.get(s['k'], {}).get('state')
        s['state'] = st
        if contact and st not in ('CONTACT', 'TENSION'):
            why.append(f'단 {s["k"]} 판 접촉 {st}')
        return why

    def confirmations(j):
        """ULKR-01 · Q1 — 실제로 이어지는 B 확인 두 단 (k* + 1 · k* + 2 · 단계 CONFIRM) 의 등록 정상 완료 (덱 정상 · S3 · 유한 · 순서 · 누락 없음 · 판 접촉은 요구하지 않음)."""
        why = []
        for c in range(1, conf + 1):
            x = j + c
            if x >= len(steps):
                why.append(f'확인 단 {c} 없음 (주 측정 미완료 · 하한 · 점 추정 자동 발행 없음)')
                continue
            s = steps[x]
            if s['k'] != steps[j]['k'] + c:
                why.append(f'확인 단 {c} k {s["k"]} ≠ {steps[j]["k"] + c} (단 기록 불연속 — 누락 · 순서)')
                continue
            if s.get('kind') != 'B':
                why.append(f'확인 단 {c} (k {s["k"]}) 이 B 단 아님 ({s.get("kind")})')
            if s.get('phase') != 1:
                why.append(f'확인 단 {c} (k {s["k"]}) 단계 {s.get("phase")} ≠ CONFIRM 1')
            why += [f'확인 단 {c}: {w}' for w in endpoint(x, contact=False)]
        return why

    # 첫 교차 (k ≥ 1 의 사다리 · 비유한 단을 사이에 둔 교차 = 끝점 무효)
    first, gap = None, False
    for j in range(1, len(steps)):
        pj = steps[j]['P']
        if pj is None:
            gap = True
            continue
        if pj <= Pm:
            pi = steps[j - 1]['P']
            first = ('gap', j) if (gap or pi is None) else ((j - 1, j) if pi > Pm else ('below', j))
            break
        gap = False
    nb = [e for e in run['events'] if e['event'] == 'NO_BRACKET']
    if gravity and nb:
        v['primary_status'] = 'NO_BRACKET'
        v['why'].append(f'중력 팔 재평형 뒤 P̄ ≤ P_meas · 분리 · 비정상 ({nb[0]["detail"]}) — 압력 · 높이 · 표면만 (§12-7)')
        first = None
    elif first and first[0] == 'gap':
        v['primary_status'] = 'UNIDENTIFIED'
        v['why'].append(f'교차 끝점 비유한 (단 {steps[first[1] - 1]["k"]} — NaN 은 ≤ 도 > 도 아니다)')
    elif first and first[0] == 'below':
        v['primary_status'] = 'UNIDENTIFIED'
        v['why'].append('출발 (k = 0 · 중력 팔 첫 유지) 부터 P̄ ≤ P_meas — 교차 없음')
    elif first:
        i, j = first
        why = rec_why + endpoint(i) + endpoint(j) + confirmations(j)
        v['endpoint_states'] = [steps[i].get('state'), steps[j].get('state')]
        rho, br, brp = interp_rho(steps[i], steps[j], Pm, h0_um)
        v['rho_pct'], v['bracket_um'], v['bracket_pct'] = rho, br, brp
        # k* 의 σ_P — 그 단 마지막 두 창의 thermo 정규 줄 (창 범위 = 창 기록의 step)
        ws = sorted(w['step'] for w in wins if w.get('k') == steps[j]['k'] and w.get('step') is not None)
        if len(ws) >= 2:
            lo = ws[-2] - (ws[-1] - ws[-2])
            sg = ul_observers.sigma_P(thermo_regular(), [(lo, ws[-1])], ddof=P['noise_floor']['ddof'], min_n=P['noise_floor']['min_n'],
                                      col=P['records']['thermo_cols'][4], scale=scale)
            v['sigma_P'] = sg['sigma']
            nf = ul_observers.noise_floor(sg['sigma'], Pm, P['noise_floor']['factor'])
        else:
            nf = 'OBS_MISSING'
        if rho is None:
            why.append('보간 불가 (분모 0 · 비유한)')
        if why:
            v['primary_status'] = 'UNIDENTIFIED'
            v['why'] += why
            v['rho_pct'] = None
        elif nf == 'NOISE_FLOOR':
            v['primary_status'] = 'NOISE_FLOOR'
            v['why'].append(f'P_meas < {P["noise_floor"]["factor"]} σ_P ({v["sigma_P"]})')
        elif nf != 'OK':
            v['primary_status'] = 'UNIDENTIFIED'
            v['why'].append(f'σ_P {nf}')
            v['rho_pct'] = None
        else:
            v['primary_status'] = 'OK'
        # 비단조 — k = 0 부터 모든 교차 괄호의 외곽 구간 [최소, 최대] (§13-5 ① · 개정 3 §14-2 · b 판정 없음 · ULKR-02)
        cr = crossings(steps, Pm)
        v['nonmonotone'] = len(cr) > 1
        bad = [s['k'] for s in steps if s['P'] is None or s['lift_um'] is None]
        if bad:
            v['why'].append(f'합집합 미계산 — 기록된 단 P̄ · 높이 비유한 (k {bad[:5]}) · 10 쌍 표 미식별')
        elif cr:
            lifts = [steps[x]['lift_um'] for pair in cr for x in pair]
            v['union_bracket_um'] = [min(lifts), max(lifts)]
            v['union_bracket_pct'] = [100.0 * x / h0_um for x in v['union_bracket_um']]
            if br and not (v['union_bracket_um'][0] <= br[0] and br[1] <= v['union_bracket_um'][1]):
                v['why'].append('합집합 ⊉ 첫 교차 괄호 (불변식 위반) — 합집합 미계산')
                v['union_bracket_um'] = v['union_bracket_pct'] = None
        # 상쇄 — 교차 끝점 마지막 창의 인장 합 ≥ 0.5 · P_meas · A (힘)
        tens = [last_state.get(steps[x]['k'], {}).get('tension_N') for x in (i, j)]
        thr = 0.5 * Pm * N_per_MPa
        v['cancellation'] = any(t is not None and t >= thr for t in tens)
        v['cancellation_detail'] = {'tension_N': tens, 'threshold_N': thr}
    elif v['primary_status'] is None:
        # 교차 없음 — §13-2 ② · ③
        if v['trajectory_status'] in ('DONE', 'SEP_INCOMPLETE'):
            v['primary_status'] = 'NO_CROSSING'
            v['why'].append('끝났는데 교차 없음')
        else:
            why = list(rec_why)
            ks = list(range(1, len(steps)))
            for x in ks:
                why += endpoint(x)
            mono = all(steps[x]['P'] is not None and steps[x - 1]['P'] is not None and steps[x]['P'] <= steps[x - 1]['P'] for x in ks)
            if not ks:
                why.append('정상 단 없음')
            if not mono:
                why.append('비단조 (교차 전) — 하한 전제 불충족')
            if why:
                v['primary_status'] = 'UNIDENTIFIED'
                v['why'] += why
            else:
                v['primary_status'] = 'LOWER_BOUND'
                v['lower_bound_pct'] = 100.0 * steps[ks[-1]]['lift_um'] / h0_um
    if steps and steps[0]['k'] == 0 and not steps[0]['steady'] and not gravity:
        v['primary_status'] = 'TECH'
        v['why'].append('k = 0 출발 비정상 (§7-1 TECH)')
    if res == 'TECH':
        v['primary_status'] = 'TECH'
    v['disposition'] = 'DIAGNOSTIC' if v['cancellation'] else ('VALUE' if v['primary_status'] == 'OK' else 'NONE')
    v['rank_eligible'] = v['primary_status'] == 'OK' and not v['cancellation']
    # 분리 · 분리 뒤 표면 (§13-3) · S4 (창 = 덱 물리 창 — 창 끝 프레임 사이) · 창 기록 = 같은 k 안 고유 · 연속 w + 그 팔 창 간격 (Q4 가)
    sep = separation(states, P['windows']['sep_declare'], w_steps=_arm_wsteps(d, job, P))
    v['separation'] = {k: sep[k] for k in ('declared_step', 'separated_final', 'recontact_index', 'missing_index', 'moved_index', 'gap_index')}
    v['separation']['n_post'] = len(sep['post_windows'])
    v['separation']['declared_w'] = states[sep['declared_index']]['w'] if sep['declared_index'] is not None else None
    if sep['separated_final'] and sep['post_windows']:
        excl = ul_observers.s0_exclusion(s0_atoms, P['beds'][bed]['h0']) if s0_atoms else set()
        hs = []
        for idx in sep['post_windows'][:P['windows']['post_sep']]:
            stp = states[idx]['step']
            ad, _pr = _atom_frame(fp(f'dump/atom_{stp}.dump', stp), stp, s0_ids)   # 전부 읽힘 · 머리 step · 고유 ID (ULKR-04)
            box = ((0.0, 0.05), (0.0, 0.05)) if not (ad and ad['box']) else (ad['box'][0], ad['box'][1])
            si = ul_observers.surface_index(ad['rows'], excl, box, grid=P['surface']['grid'], q=P['surface']['quantile'],
                                            method=P['surface']['quantile_method'], um=um) if ad and ad['rows'] else {'status': 'NOT_COMPUTED', 'mean_um': None}
            hs.append(si['mean_um'])
        v['surface_um'] = hs
        s4 = [ul_observers.s4_check(a, b, P['steady']['S4_um_per_window']) for a, b in zip(hs, hs[1:])]
        v['s4_status'] = 'FAIL' if 'FAIL' in s4 else ('PASS' if s4 and all(x == 'PASS' for x in s4) else 'NOT_COMPUTED')
    # 분리 완료 (개정 3 §14-7 · Q6 · ULKR-07) — 덱 DONE 은 판독기가 같은 분리를 볼 때만 DONE: 판독기 최종 분리 + 분리 뒤 4 창 · 선언 창 ≤ 유지 예산 ·
    # 덱 마지막 SEPARATED 사건 step = 판독기 선언 창 · POST_DONE = 판독기 넷째 분리 뒤 창.  아니면 보조 미완료 SEP_INCOMPLETE — 주 ρ 무영향.
    if res in ('DONE', 'SEP_INCOMPLETE'):
        sw = []
        postn = P['windows']['post_sep']
        if res == 'SEP_INCOMPLETE':
            sw.append('덱 SEP_INCOMPLETE (재접촉 뒤 같은 높이 유지 예산 끝 — 분리 뒤 4 창 미완료)')
        elif not (sep['separated_final'] and len(sep['post_windows']) >= postn):
            sw.append(f'덱 DONE 인데 판독기 최종 분리 · 분리 뒤 창 {len(sep["post_windows"])} < {postn} (재접촉 창 {sep["recontact_index"][:3]} · '
                      f'벽 덤프 결손 창 {sep["missing_index"][:3]} · 이동 {sep["moved_index"][:3]} · 창 기록 끊김 (w · 간격) {sep["gap_index"][:3]})')
        else:
            wmax = _hold_wmax(job, P)
            dw = v['separation']['declared_w']
            if dw is None or dw > wmax:
                sw.append(f'판독기 분리 선언 창 w {dw} > 유지 예산 {wmax} (선언은 예산 안 · 분리 뒤 4 창만 예산 밖)')
            ev_sep = [e['step'] for e in run['events'] if e['event'] == 'SEPARATED']
            ev_post = [e['step'] for e in run['events'] if e['event'] == 'POST_DONE']
            if not ev_sep or ev_sep[-1] != sep['declared_step']:
                sw.append(f'덱 마지막 SEPARATED 사건 step {ev_sep[-1] if ev_sep else None} ≠ 판독기 선언 창 step {sep["declared_step"]}')
            pw = states[sep['post_windows'][postn - 1]]['step']
            if not ev_post or ev_post[-1] != pw:
                sw.append(f'덱 POST_DONE 사건 step {ev_post[-1] if ev_post else None} ≠ 판독기 분리 뒤 {postn} 째 창 step {pw}')
        if sw:
            v['trajectory_status'] = 'SEP_INCOMPLETE'
            v['why'] += ['보조 미완료 (분리 · 표면 — 주 ρ 무영향): ' + w for w in sw]
    if cont is not None:
        v['continuation'] = {'status': cont['status'], 'parent_dir': cont['dir'], 'rm_step': cont['rm_step'], 'problems': cont['problems'][:8],
                             'n_parent_listed': len(cont['sums']), 'n_parent_checked': len(cont['checked'])}
        if cont['status'] != 'OK':
            v['primary_status'] = 'UNIDENTIFIED'
            v['rho_pct'] = None
            v['rank_eligible'] = False
            v['disposition'] = 'NONE'
            v['why'].append(f'UTc 이어 돌림 (UT 부모 관측) 무효 — {" · ".join(cont["problems"][:3])} (개정 3 §14-3)')
    if gravity:
        g = _g_restore(d, run, root, bed, job)
        v['g_restore'] = g
        if g['status'] != 'PASS':
            v['primary_status'] = 'TECH'
            v['rank_eligible'] = False
            v['why'].append(f'중력 팔 R_M 복원 {g["status"]} (G1 {g.get("G1")} · G2 {g.get("G2")} · G2c {g.get("G2c")}) — choice C12')
    # ε_sphere · W_proxy (개정 3 §14-8 · Q7 · ULKR-12) — 보조 관측 (주 값 판정이 끝난 뒤 · 주 ρ 무영향)
    v['eps'], v['w_proxy_J'], v['w_proxy'] = _aux_eps_w(v, steps, first, s0d, fp, s0_ids, P['beds'][bed]['h0'], P)
    return v


def _g_restore(d, run, root, bed, job):
    """중력 팔 복원 (choice C12): R_M 의 run 0 setup — G1 (출처 팔 로그의 R_M 정규 줄) · G2 (원자) · G2c (쌍) = 출처 팔의 R_M 창 끝 덤프 · G3 해당 없음."""
    out = {'status': 'NOT_COMPUTED', 'why': []}
    st = [e for e in run['events'] if e['event'] == 'START']
    if not st or st[0]['step'] is None:
        out['why'].append('START 사건 없음')
        return out
    rm = st[0]['step']
    man = os.path.join(d, 'run_manifest.txt')
    m = re.search(r'source=(\S+)', open(man, encoding='utf-8').read()) if os.path.exists(man) else None
    src = m.group(1) if m else os.path.join(root, bed, 'UT' if (bed == B73 and job == 'G_UT3') else job[2:])
    row = _thermo(src)['regular'].get(rm)
    scrp = os.path.join(d, 'screen.txt')
    if row is None or not os.path.exists(scrp):
        out['why'].append(f'출처 팔 R_M 정규 줄 · 중력 팔 화면 없음 ({src})')
        return out
    ref = f'{rm} {int(row["Atoms"])} {row["KinEng"]!r} 0 0'
    g1 = ul_gates.g1_check(open(scrp, encoding='utf-8', errors='replace').read(), ref, rm)
    g2 = ul_gates.g2_compare(os.path.join(d, 'dump', f'atom_{rm}.dump'), os.path.join(src, 'dump', f'atom_{rm}.dump'), step=rm)   # 관측 결손 · 값 차이 = PASS 아님 → TECH (C12)
    g2c = ul_gates.g2c_compare(os.path.join(d, 'dump', f'contact_{rm}.dump'), os.path.join(src, 'dump', f'contact_{rm}.dump'), step=rm)
    out.update(rm_step=rm, source=src, G1=g1['status'], G2=g2['status'], G2c=g2c['status'], G3='해당 없음 (중력 교체)')
    out['status'] = 'PASS' if (g1['status'], g2['status'], g2c['status']) == ('PASS', 'PASS', 'PASS') else 'FAIL'
    return out


def _valid_rho(vd):
    return vd is not None and vd.get('primary_status') == 'OK' and isinstance(vd.get('rho_pct'), float) and math.isfinite(vd['rho_pct'])


def _le(a, b):
    return a <= b + EPS_PP


def selection(v_ub, v_ut, v_uv=None, P=None):
    """§12-4 결정표 · §13-1 끝점 유효성 — 유효한 δ 둘이면 행 하나 · 아니면 SELECTION_UNRESOLVED (다음 팔 · 본 런 없음)."""
    P = P or ul_lib.load_params()
    lim = P['selection']['delta_max_pp']
    out = {'stage': None, 'delta_dt': None, 'delta_v': None, 'dt_star': None, 'tuple': None, 'arm': None, 'next': [], 'why': []}
    if v_ub is None or v_ut is None:
        out.update(stage='need_UB_UT', why=['UB · UT 판독 전'])
        return out
    if not (_valid_rho(v_ub) and _valid_rho(v_ut)):
        out['stage'] = 'SELECTION_UNRESOLVED'
        out['why'].append(f'끝점 무효 — UB {v_ub.get("primary_status")} · UT {v_ut.get("primary_status")} (δ_dt 없음)')
        return out
    d_dt = abs(v_ut['rho_pct'] - v_ub['rho_pct'])
    out['delta_dt'] = d_dt
    if not math.isfinite(d_dt):
        out.update(stage='SELECTION_UNRESOLVED', why=['δ_dt 비유한'])
        return out
    half = not _le(d_dt, lim)
    out['dt_star'] = 'dt0/2' if half else 'dt0'
    uvjob = 'UVb' if half else 'UVa'
    if v_uv is None:
        out.update(stage='need_UV', next=[uvjob])
        return out
    if v_uv.get('job') not in (None, uvjob):
        out.update(stage='SELECTION_UNRESOLVED', why=[f'UV 팔 {v_uv.get("job")} ≠ dt* 의 팔 {uvjob}'])
        return out
    ref = v_ut if half else v_ub
    if not _valid_rho(v_uv):
        out['stage'] = 'SELECTION_UNRESOLVED'
        out['why'].append(f'끝점 무효 — {uvjob} {v_uv.get("primary_status")} (δ_v 없음)')
        return out
    d_v = abs(v_uv['rho_pct'] - ref['rho_pct'])
    out['delta_v'] = d_v
    if not math.isfinite(d_v):
        out.update(stage='SELECTION_UNRESOLVED', why=['δ_v 비유한'])
        return out
    slow = not _le(d_v, lim)
    tup = {(False, False): 't1', (False, True): 't2', (True, False): 't3', (True, True): 't4'}[(half, slow)]
    out.update(stage='resolved', tuple=tup, arm=TUPLE_ARM[tup])
    return out


def _arm_v(root, bed, job, P):
    d = os.path.join(root, bed, job)
    if not os.path.isdir(d):
        return None
    try:
        return arm_verdict(d, bed, job, P, root=root)
    except Exception as e:  # noqa: BLE001 — 판독 실패 = 무효 끝점 (조용히 넘기지 않는다)
        return {'job': job, 'primary_status': 'UNIDENTIFIED', 'why': [f'판독 실패 {type(e).__name__}: {e}']}


def selection_state(root, P=None):
    P = P or ul_lib.load_params()
    ub, ut = _arm_v(root, B73, 'UB', P), _arm_v(root, B73, 'UT', P)
    s = selection(ub, ut, None, P)
    if s['stage'] == 'need_UV':
        uv = _arm_v(root, B73, s['next'][0], P)
        if uv is not None:
            s = selection(ub, ut, uv, P)
    return s


def _job_receipt(root, bed, job):
    """잡 완료 영수증 (ULKRR-03 · 개정 3 §14-10): 러너 run_manifest.txt 의 끝 줄 `end=… fails=N reader_rc=M` — fails · reader_rc 가 둘 다 한 번씩 있고 ·
    정수 · 0 일 때만 참.  판독기가 결과 파일 (증서 · 기준 파일) 을 쓴 뒤 실패한 잡 = reader_rc ≠ 0 — 그 산출물을 다음 제출 승인으로 다시 쓰지 않는다
    (판독 오류를 rc 0 으로 삼키지 않는다 · 정상 미식별은 판독기 rc 0 · JSON) → (참?, 이유, 기록 글자).
    범위 (Q2 (가) · 1저자 10-15 · Codex 수정 재확인 Q2): 복원 / EXT 증서는 성공 완료 영수증이 필수이며, 일반 팔의 주 관측은 원 폴더에서 재판독한다
    (이 영수증을 읽지 않는다 — arm_verdict).  재판독 가능성이 잡의 기술 성공을 뜻하지는 않는다."""
    man = os.path.join(root, bed, job, 'run_manifest.txt')
    text = open(man, encoding='utf-8', errors='replace').read() if os.path.isfile(man) else ''
    ends = [ln for ln in text.splitlines() if ln.startswith('end=')]
    if not ends:
        return False, f'{job} 잡 기록 (run_manifest.txt) 에 끝 줄 없음 — 러너가 끝내지 못했다', text
    kv = {}
    for tok in ends[-1].split()[1:]:
        k, _sep, val = tok.partition('=')
        kv.setdefault(k, []).append(val)
    bad = [k for k in ('fails', 'reader_rc') if len(kv.get(k, [])) != 1 or not re.fullmatch(r'\d+', kv[k][0]) or int(kv[k][0]) != 0]
    if bad:
        return (False, f'{job} 잡 기록 끝 줄 ({ends[-1].strip()}) — {" · ".join(bad)} ≠ 0 · 결손 · 정수 아님 (기술 실패 · 판독기 오류 — fails=0 · reader_rc=0 '
                f'둘 다 필수 · 산출물을 다시 쓰지 않는다 · 새 시도 · ULKRR-03)', text)
    return True, f'{job} 잡 끝 fails=0 · reader_rc=0', text


def _job_restored(root, bed, job):
    """복원 증서 RESTORED + 그 RJ · RJ2 잡 완료 영수증 (fails=0 · reader_rc=0 · ULKRR-03) + 문법 fixture 사전 점검 PASS 기록 (grammar_prereq=PASS ·
    Q5 — 그 잡의 R 이 문법 PASS 뒤에 돌았다) — 같은 실행 끝의 기술 실패 · 판독기 오류가 있으면 증서를 믿지 않는다 (ULKR-05)."""
    r = _readjson(os.path.join(root, bed, job, 'restore_verdict.json'))
    if not (r and r.get('status') == 'RESTORED'):
        return False, f'{job} 복원 판정 RESTORED 아님 ({(r or {}).get("status")})'
    ok, why, text = _job_receipt(root, bed, job)
    if not ok:
        return False, why
    if not re.search(r'^grammar_prereq=PASS$', text, re.M):
        return False, (f'{job} 잡 기록에 문법 fixture 사전 점검 PASS 줄 (grammar_prereq=PASS) 없음 — 본 R 전 문법 fixture PASS 필수 '
                       '(개정 3 §14-9 · Q5) · 새 시도')
    return True, f'{job} RESTORED · 잡 끝 fails=0 · reader_rc=0 · 문법 fixture 사전 점검 PASS'


def _restored(root, bed, P):
    job = 'RJ2' if bed == B100 else 'RJ'
    ok, why = _job_restored(root, bed, job)
    return ok, job, why


def _has_event(root, bed, job, name):
    run = read_run(os.path.join(root, bed, job))
    return any(e['event'] == name for e in run['events'])


def gate(root, bed, job, P=None):
    """다음 제출 관문 (§13-1 · §13-5 ② ③) → (허용?, 이유)."""
    P = P or ul_lib.load_params()
    if bed not in BEDS:
        return False, f'모르는 침대 {bed}'
    if job == 'RJ':
        return True, '복원 시험 (원 체크포인트 · 결과 0 건)'
    if job == 'EXT':
        if bed != B100:
            return False, 'EXT = 10:0 전용'
        ok, why = _job_restored(root, bed, 'RJ')
        return ok, f'10:0 이완 연장 = 3,600,000 복원 관문 통과 뒤 (§12-11) — {why}'
    if job == 'RJ2':
        if bed != B100:
            return False, 'RJ2 = 10:0 전용 (S0′ 복원 · UK)'
        dec = _readjson(os.path.join(root, bed, 's0_decision.json'))
        if not (dec and dec.get('status') == 'PASS'):
            return False, 'S0′ 결정 PASS 뒤 (§12-11 · F3 이면 없음)'
        ok, why, _text = _job_receipt(root, bed, 'EXT')   # ULKRR-03 — 그 결정을 낸 EXT 잡의 완료 영수증도
        return ok, f'S0′ 결정 PASS + EXT 잡 완료 영수증 — {why}'
    ok, rj, why = _restored(root, bed, P)
    if not ok:
        return False, f'{rj} 복원 관문 미통과 — {why} (§12-1 ⑤ · 개정 3 §14-10 — 미확인 · 실패면 U 없음)'
    if not os.path.exists(os.path.join(root, bed, 'ul_base.in')):
        return False, 'KE 기준 파일 ul_base.in 없음 (kebase · UK 뒤)'
    if job == 'UC':
        return True, '무이동 대조 (dt₀ · 서로 독립)'
    if bed == B73:
        if job in ('UB', 'UT'):
            return True, '7:3 개발 팔 (UB · UT · UC 먼저 · 서로 독립 · §13-5 ②)'
        s = selection_state(root, P)
        if job in ('UVa', 'UVb'):
            if s['stage'] == 'need_UV' and s['next'] == [job]:
                return True, f'δ_dt {s["delta_dt"]} → dt* {s["dt_star"]} → {job}'
            return False, f'선택 단계 {s["stage"]} · 다음 {s["next"]} ({" · ".join(s["why"])}) — UV 는 UB · UT 끝점 판독 뒤 dt* 의 팔 하나만'
        if s['stage'] != 'resolved':
            return False, f'최종 튜플 없음 ({s["stage"]} · {" · ".join(s["why"])})'
        if job == 'UTc':
            ok = s['tuple'] == 't3' and _has_event(root, bed, 'UT', 'RM')
            return ok, f'튜플 {s["tuple"]} — UTc 는 결정표 3 행 (UT 채택) 일 때 UT 의 R_M 에서만 (§13-5 ③)'
        if job == 'UT3':
            return False, '7:3 의 t3 본 값 = UT + UTc (S0 에서 새 UT3 를 돌리지 않는다)'
        if job.startswith('G_'):
            src = 'UT' if s['tuple'] == 't3' else s['arm']
            ok = job == f'G_{s["arm"]}' and _has_event(root, bed, src, 'RM')
            return ok, f'중력 팔 = 최종 팔 {s["arm"]} 의 R_M (출처 {src}) 에서'
        return False, f'7:3 {job} — 개발 팔 순서 밖'
    s = selection_state(root, P)
    if s['stage'] != 'resolved':
        return False, f'7:3 최종 튜플 없음 ({s["stage"]}) — 나머지 넷 U 없음 (§13-1)'
    if job == s['arm']:
        return True, f'본 런 = 최종 튜플 {s["tuple"]} 의 팔 {job}'
    if job == f'G_{s["arm"]}':
        ok = _has_event(root, bed, s['arm'], 'RM')
        return ok, f'중력 팔 = {s["arm"]} 의 R_M 에서'
    return False, f'{bed} 는 최종 튜플 {s["tuple"]} 의 팔 {s["arm"]} 만 (민감도 미측정 · §12-5)'


def pair_table(verdicts):
    """10 쌍 — 유효 · 순위 자격 (상쇄 진단값 아님) 둘 다일 때만 괄호 (합집합) 비교 · 겹침 = 미구분 (동률 아님) · 아니면 UNIDENTIFIED."""
    out = []
    for i, a in enumerate(BEDS):
        for b in BEDS[i + 1:]:
            va, vb = verdicts.get(a) or {}, verdicts.get(b) or {}
            ok = all(x.get('primary_status') == 'OK' and x.get('rank_eligible') and x.get('union_bracket_pct') for x in (va, vb))
            if not ok:
                rel = 'UNIDENTIFIED'
            else:
                (a0, a1), (b0, b1) = sorted(va['union_bracket_pct']), sorted(vb['union_bracket_pct'])
                rel = 'OVERLAP' if (a0 <= b1 and b0 <= a1) else 'SEPARATED'
            out.append({'a': a, 'b': b, 'relation': rel})
    return out


def _screen_info(path):
    info = {'banner': False, 'git': False, 'errors': [], 'loops': [], 'resets': set(), 'markers': []}
    if not os.path.exists(path):
        info['errors'].append('화면 없음')
        return info
    for ln in open(path, encoding='utf-8', errors='replace').read().splitlines():
        if 'LIGGGHTS-PUBLIC 3.8.0' in ln:
            info['banner'] = True
            info['git'] = info['git'] or '3d5c00f' in ln
        if ln.startswith('ERROR') or 'Segmentation fault' in ln or 'MPI_ABORT' in ln:
            info['errors'].append(ln.strip())
        m = re.search(r'Loop time of [0-9.eE+-]+ on (\d+) procs', ln)
        if m:
            info['loops'].append(int(m.group(1)))
        m = re.match(r'Resetting (global|per-atom) state of Fix (\S+) Style (\S+) from restart file info', ln.strip())
        if m:
            info['resets'].add((m.group(2), m.group(3), m.group(1)))
        if ln.startswith('UL_'):
            info['markers'].append(ln.strip())
    return info


EXPECTED_RESETS = (('history_zwall_bot', 'property/atom', ('global', 'per-atom')), ('top_mesh', 'mesh/surface/stress', ('global',)),
                   ('n_neighs_mesh_top_mesh', 'property/atom', ('global', 'per-atom')),
                   ('tracker_top_mesh', 'contacthistory/mesh', ('global', 'per-atom')), ('contacthistory', 'contacthistory', ('global', 'per-atom')))


#: R · UNread 덱의 바닥 이력 관측 열 (make_unload_decks._hist_dump_cols 와 같음 — selftest R19 가 대조)
HIST_PRE_COLS = ('id', 'type', 'x', 'y', 'z', 'radius', 'mass', 'vx', 'vy', 'vz', 'omegax', 'omegay', 'omegaz',
                 'f_history_zwall_bot[1]', 'f_history_zwall_bot[2]', 'f_history_zwall_bot[3]', 'f_history_zwall_bot[4]')
HIST_POST_COLS = HIST_PRE_COLS[:13] + ('fx', 'fy', 'fz') + HIST_PRE_COLS[13:]
STAGE_NP = 6           # 러너 NP (README §3 · #SBATCH -n 6 ↔ -np 6)


def _stage_tech(sdir, kind, marker=None, np_=STAGE_NP):
    """러너가 쓴 단계 기록 (run_check.txt — 줄마다 '<덱 종류> <화면> PASS rc=0 procs=N' · 아니면 FAIL · missing_ckpt) + 그 화면 —
    PASS 줄 하나 이상 · 다른 줄 없음 · 배너 · ERROR 없음 · Loop time procs = NP · 표지 (ULKR-05 · ULKR-11)."""
    pr = []
    rc = os.path.join(sdir, 'run_check.txt')
    lines = [ln.split() for ln in open(rc, encoding='utf-8', errors='replace').read().splitlines() if ln.strip()] if os.path.exists(rc) else None
    if lines is None:
        pr.append('단계 기록 run_check.txt 없음')
    else:
        if not any(len(t) >= 4 and t[0] == kind and t[2] == 'PASS' and t[3] == 'rc=0' for t in lines):
            pr.append(f'{kind} PASS 줄 없음')
        bad = [' '.join(t) for t in lines if not (len(t) >= 4 and t[0] == kind and t[2] == 'PASS' and t[3] == 'rc=0')]
        if bad:
            pr.append(f'단계 기록 실패 줄: {bad[:2]}')
    si = _screen_info(os.path.join(sdir, 'screen.txt'))
    if not (si['banner'] and si['git']):
        pr.append('배너 LIGGGHTS-PUBLIC 3.8.0 · 3d5c00f 없음')
    if si['errors']:
        pr.append(f'화면 ERROR: {si["errors"][:2]}')
    if not si['loops'] or any(n != np_ for n in si['loops']):
        pr.append(f'Loop time procs {si["loops"]} ≠ {np_}')
    if marker and not any(m.startswith(marker) for m in si['markers']):
        pr.append(f'{marker} 표지 없음')
    return {'ok': not pr, 'problems': pr, 'loops': si['loops'], 'errors': si['errors'][:3]}


def _obs_frame(path, cols, step, ids):
    """관측 덤프 한 장 — 전부 읽힘 (머리 · 열 이름 · 행 수 · 유한 — 파서가 버린 행이 있으면 실패) · 머리 step = 기대 · ID 고유 ·
    ID 집합 = 기대 (S0) → (행 목록 | None, 문제).  버린 행을 정상 부분 관측으로 쓰지 않는다 (ULKR-04 · 05)."""
    d = ul_lib.read_dump(path, 'custom', list(cols))
    pr = [f'{os.path.basename(path or "")}: {p}' for p in d['problems']]
    if step is None or d['step'] != step:
        pr.append(f'{os.path.basename(path or "")}: 머리 step {d["step"]} ≠ 기대 {step}')
    if not d['ok']:   # 파서 · 필수 열 문제를 먼저 (ULKRR-04 — 열 결손이면 id 를 읽지 않는다)
        return None, pr
    got, ipr = ul_lib.ids_of(d['rows'])
    if got is None:   # 소수 · 0 이하 ID = 정수로 자르지 않는다 (ULKRR-04 · Codex fractional_un_id)
        return None, pr + [f'{os.path.basename(path or "")}: {x}' for x in ipr]
    if len(set(got)) != len(got):
        pr.append(f'{os.path.basename(path or "")}: ID 중복')
    if ids is None:
        pr.append('기대 ID 집합 (S0) 없음')
    elif set(got) != ids:
        pr.append(f'{os.path.basename(path or "")}: ID 집합 ≠ S0 (빠짐 {len(ids - set(got))} · 더 있음 {len(set(got) - ids)})')
    return (d['rows'] if not pr else None), pr


def _hist_qualifies(h, P):
    """이력 시험 자격 (ULKR-08 · §14-10): schema · rc 0 · H0–H5 PASS · SYN PASS · 측정 부호 = 표 · 총힘 출력 시점 PASS — SYN 없음 = 자격 없음."""
    if h is None:
        return None, ['이력 시험 판정 없음']
    why = []
    if h.get('schema') != 'ps45_unload_history_verdict_v1':
        why.append(f'판정 schema {h.get("schema")!r} (이력 시험 판정 파일이 아니다)')
    if h.get('exit_code') != 0:
        why.append(f'이력 시험 rc {h.get("exit_code")}')
    rows = h.get('rows') or {}
    bad = [f'H{i}' for i in range(6) if (rows.get(f'H{i}') or {}).get('status') != 'PASS']
    if bad:
        why.append(f'{" · ".join(bad)} PASS 아님')
    info = h.get('info') or {}
    syn = info.get('syn') or {}
    if syn.get('status') != 'PASS':
        why.append(f'SYN {syn.get("status")} (SYN PASS 필수 — 없으면 자격 없음)')
    if syn.get('plate_fn_sign') != P['plate_fn_compressive_sign']:
        why.append(f'SYN 판 법선력 부호 {syn.get("plate_fn_sign")} ≠ 표 {P["plate_fn_compressive_sign"]} (측정된 같은 부호 필수)')
    if info.get('force_timing') != 'PASS':
        why.append(f'총힘 출력 시점 {info.get("force_timing")} (C1 선행조건)')
    return (not why), why


def _readtext(path):
    try:
        return open(path, encoding='utf-8', errors='replace').read().strip()
    except OSError:
        return None


def _grammar_reread(rd, kit, listed, json_checks, readers=None):
    """Q3 (1저자 10-15 · Codex 수정 재확인 Q4 — 캐시 신뢰 경계): 문법 런 폴더 rd 의 원자료를 **승인된 판독기** 로 다시 읽어 판정 JSON 과 대조 → (문제 목록, 기록).
    승인된 판독기 = 그 런 kit 사본 (run_manifest kit=) 의 read_history.py · history_params.json — 두 파일 sha256 = readers (GRAMMAR_READER · history_test 봉인) 이고
    그 런 kit SHA256SUMS (listed — sha256 = run_manifest sums_sha256 로 확인된 것) 에도 같은 값일 때만 실행한다 (`python3 -I read_history.py <rd> --grammar --params …
    --out <임시>` · 런 폴더에 쓰지 않는다).  통과 = 재판독 status PASS · exit_code 정수 0 · rc 0 · 검사 19 (GRAMMAR_CHECKS) = 판정 JSON 의 값 (둘 다 참)."""
    import subprocess
    import tempfile
    readers = GRAMMAR_READER if readers is None else readers
    rec = {'reader': None, 'reader_sha256': None, 'status': None, 'exit_code': None, 'rc': None, 'diff': None, 'problems': None}
    if not kit or not os.path.isdir(kit):
        return [f'원자료 재판독: 그 런 kit 사본 폴더 없음 ({kit}) — 승인된 판독기를 찾을 수 없다 (Q3)'], rec
    pr = []
    for n, h in sorted(readers.items()):
        p = os.path.join(kit, n)
        got = ul_lib.sha256_file(p) if os.path.isfile(p) else None
        if got != h:
            pr.append(f'원자료 재판독: kit 사본 {n} sha256 {got} ≠ 승인된 판독기 봉인 값 {h} — 승인 밖 판독기 · 실행하지 않는다 (Q3)')
        elif listed is None or listed.get(n) != h:
            pr.append(f'원자료 재판독: 그 런 kit SHA256SUMS 의 {n} ({None if listed is None else listed.get(n)}) ≠ 승인된 판독기 봉인 값 {h} (Q3)')
    if pr:
        return pr, rec
    reader = os.path.join(kit, 'read_history.py')
    rec.update(reader=reader, reader_sha256=readers['read_history.py'])
    with tempfile.TemporaryDirectory(prefix='ul_gram_reread_') as td:
        op = os.path.join(td, 'reread.json')
        try:
            p = subprocess.run([sys.executable, '-I', reader, rd, '--grammar', '--params', os.path.join(kit, 'history_params.json'), '--out', op],
                               capture_output=True, text=True, timeout=600)
        except (OSError, subprocess.SubprocessError) as ex:
            return [f'원자료 재판독 실행 실패: {type(ex).__name__}: {ex} (Q3)'], rec
        rec['rc'] = p.returncode
        rv = _readjson(op)
    if not isinstance(rv, dict):
        return [f'원자료 재판독: 판독기 결과 JSON 없음 · 깨짐 (rc {p.returncode} · {p.stderr.strip()[-160:]}) (Q3)'], rec
    rch = rv.get('checks') if isinstance(rv.get('checks'), dict) else {}
    diff = {k: [json_checks.get(k), rch.get(k)] for k in GRAMMAR_CHECKS if not (json_checks.get(k) is True and rch.get(k) is True)}
    rec.update(status=rv.get('status'), exit_code=rv.get('exit_code'), diff=diff or None, problems=(rv.get('problems') or [])[:4])
    if rv.get('schema') != GRAMMAR_SCHEMA:
        pr.append(f'원자료 재판독 schema {rv.get("schema")!r} ≠ {GRAMMAR_SCHEMA} (Q3)')
    ec = rv.get('exit_code')
    if rv.get('status') != 'PASS' or type(ec) is not int or ec != 0 or p.returncode != 0:
        pr.append(f'원자료 재판독 = status {rv.get("status")!r} · exit_code {ec!r} · rc {p.returncode} ≠ PASS · 0 — 그 런 폴더 원자료가 판정 JSON 과 다르다 '
                  f'({" · ".join((rv.get("problems") or [])[:2])}) (Q3)')
    if diff:
        pr.append(f'원자료 재판독 검사 ≠ 판정 JSON (JSON · 재판독) {dict(list(diff.items())[:4])} (Q3)')
    return pr, rec


def grammar_prereq(verdict_path, lmp_sha, inputs=None):
    """문법 fixture PASS 사전 조건 (Q5 — 1저자 10-14 강제 · 개정 3 §14-9) — 러너가 본 R (RJ · RJ2) · 10:0 연장 (EXT) 의 LIGGGHTS **전에** 부른다 →
    (허용?, 문제 목록, 기록).  ① 판정 JSON: schema · status PASS · exit_code 정수 0 · 검사 열아홉 (GRAMMAR_CHECKS) 전부 참 ② 그 판정의 런 폴더 = 판정 파일이
    놓인 폴더 (run_dir 대조) · run_manifest mode=gram · end 있음 · lmp_sha256 = 지금 돌릴 바이너리 (lmp_sha) ③ 덱 출처 — 단계 P · GA · GB 의 rc 0 · deck.txt ·
    덱 사본 · 판 STL 사본 sha256 = 봉인 값 (inputs = GRAMMAR_INPUTS) · 그 런의 kit SHA256SUMS (sha256 = run_manifest sums_sha256) 가 같은 값을 적었다
    ④ (Q3 · 1저자 10-15) 그 런 폴더 원자료를 승인된 판독기 (그 런 kit 사본의 read_history.py · history_params.json = GRAMMAR_READER 봉인 값) 로 다시 읽어
    검사 19 = 판정 JSON (_grammar_reread — JSON 만으로 원자료 PASS 를 인증하지 않는다 · 기록 rec['reread']).
    러너 스크립트 (run_history.sh) sha256 은 대조하지 않는다 (덱 · 판독기가 아니다 — 러너 수정이 그 판정을 무효로 만들지 않는다)."""
    inputs = GRAMMAR_INPUTS if inputs is None else inputs
    rec = {'verdict': verdict_path, 'verdict_sha256': None, 'run_dir': None, 'lmp_sha256': lmp_sha,
           'grammar_deck_sha256': inputs.get('in.hist_grammar.liggghts'), 'producer_deck_sha256': inputs.get('in.hist_producer.liggghts'), 'reread': None}
    if not verdict_path or not os.path.isfile(verdict_path):
        return False, [f'문법 fixture 판정 파일 없음 ({verdict_path or "GRAMMAR_VERDICT 비어 있음"})'], rec
    rec['verdict_sha256'] = ul_lib.sha256_file(verdict_path)
    v = _readjson(verdict_path)
    if not isinstance(v, dict):
        return False, ['문법 fixture 판정이 JSON 객체가 아니다'], rec
    pr = []
    if v.get('schema') != GRAMMAR_SCHEMA:
        pr.append(f'판정 schema {v.get("schema")!r} ≠ {GRAMMAR_SCHEMA}')
    if v.get('status') != 'PASS':
        pr.append(f'판정 status {v.get("status")!r} ≠ PASS')
    ec = v.get('exit_code')
    if type(ec) is not int or ec != 0:
        pr.append(f'판정 exit_code {ec!r} ≠ 정수 0')
    ch = v.get('checks')
    if not isinstance(ch, dict):
        pr.append('판정 checks 없음')
    else:
        miss = [k for k in GRAMMAR_CHECKS if k not in ch]
        notok = sorted(k for k, x in ch.items() if x is not True)
        if miss:
            pr.append(f'판정 검사 없음 {miss[:4]}')
        if notok:
            pr.append(f'판정 검사 참 아님 {notok[:4]}')
    rd = os.path.dirname(os.path.realpath(verdict_path))
    rec['run_dir'] = rd
    vr = v.get('run_dir')
    if not (isinstance(vr, str) and os.path.realpath(vr) == rd):
        pr.append(f'판정 run_dir {vr!r} ≠ 판정 파일 폴더 {rd} (다른 런의 판정)')
    kv = ul_lib.read_kv(os.path.join(rd, 'run_manifest.txt'))
    if kv.get('mode') != 'gram':
        pr.append(f'문법 런 run_manifest mode {kv.get("mode")!r} ≠ gram')
    if 'end' not in kv:
        pr.append('문법 런 run_manifest end 없음 (끝나지 않은 런)')
    if not lmp_sha or kv.get('lmp_sha256') != lmp_sha:
        pr.append(f'문법 런 LMP sha256 {kv.get("lmp_sha256")} ≠ 지금 돌릴 바이너리 {lmp_sha} (같은 바이너리의 문법 PASS 만)')
    kit = kv.get('kit')
    sp = os.path.join(kit, 'SHA256SUMS') if kit else None
    listed = None
    if not (sp and os.path.isfile(sp)):
        pr.append(f'문법 런 kit SHA256SUMS 없음 ({sp})')
    elif ul_lib.sha256_file(sp) != kv.get('sums_sha256'):
        pr.append('문법 런 kit SHA256SUMS 의 sha256 ≠ run_manifest sums_sha256')
    else:
        listed = {}
        for ln in open(sp, encoding='utf-8', errors='replace').read().splitlines():
            w = ln.split()
            if len(w) == 2:
                listed[w[1].lstrip('*')] = w[0]
        bad = sorted(n for n, h in inputs.items() if listed.get(n) != h)
        if bad:
            pr.append(f'문법 런 kit SHA256SUMS 의 {bad} sha256 ≠ 봉인 값')
    for st, deck in GRAMMAR_STAGES:
        sd = os.path.join(rd, st)
        rcv = _readtext(os.path.join(sd, 'rc'))
        if rcv != '0':
            pr.append(f'문법 런 {st} rc {rcv!r} ≠ 0')
        dt = _readtext(os.path.join(sd, 'deck.txt'))
        if dt != deck:
            pr.append(f'문법 런 {st} deck.txt {dt!r} ≠ {deck}')
        for n in (deck, 'plate_hist.stl'):
            p = os.path.join(sd, n)
            h = ul_lib.sha256_file(p) if os.path.isfile(p) else None
            if h != inputs.get(n):
                pr.append(f'문법 런 {st}/{n} sha256 {h} ≠ 봉인 값 {inputs.get(n)}')
    rpr, rec['reread'] = _grammar_reread(rd, kit, listed, ch if isinstance(ch, dict) else {})
    pr += rpr
    return (not pr), pr, rec


def restore_verdict(root, bed, job='RJ', hist=None, P=None):
    """§12-1 복원 판정 · 개정 3 §14-10 — 단계 기술 성공 (Ut0 · R · UN) · G0 (러너가 실행 전 원 덱으로 남긴 g0.json) · reset 로그 · G1 · G2 · G2c ·
    판 mesh md5 · G3 · PRE = POST (바닥 이력 · 전부 읽힘 · S0 ID 전부) · 보조 소거 진단 (R_END ↔ UN · 같은 대상) · 이력 시험 (H0–H5 + SYN + 총힘 시점) →
    RESTORED · UNCONFIRMED (관측 결손 · 미확인) · SYNTAX_FAIL (문법 · 기술 실패) · VALUE_MISMATCH (수치 불일치)."""
    P = P or ul_lib.load_params()
    B = P['beds'][bed]
    J = os.path.join(root, bed, job)
    R, UN = os.path.join(J, 'R'), os.path.join(J, 'UN')
    s0 = B['s0'] if bed != B100 else (P['ext_10_0']['start_step'] if job == 'RJ' else _bed_s0(root, bed, P))
    s_end = s0 + P['windows']['R_steps'] if s0 is not None else None
    out = {'bed': bed, 'job': job, 's0': s0, 'checks': {}, 'status': None}
    stages = {'R': _stage_tech(R, 'R', 'UL_R_DONE'), 'UN': _stage_tech(UN, 'UNread', 'UL_UN_DONE')}
    if bed == B73 and job == 'RJ':
        stages['Ut0'] = _stage_tech(os.path.join(J, 'Ut0'), 'Ut0')
    syntax = all(s['ok'] for s in stages.values())
    si = _screen_info(os.path.join(R, 'screen.txt'))
    out['checks']['syntax'] = {'ok': syntax, 'stages': {k: v['problems'] for k, v in stages.items()}, 'loops': si['loops'], 'errors': si['errors'][:3]}
    miss = [(f, s, k) for f, s, ks in EXPECTED_RESETS for k in ks if (f, s, k) not in si['resets']]
    out['checks']['reset_log'] = {'ok': not miss, 'missing': miss}
    g0 = _readjson(os.path.join(J, 'g0.json'))
    out['checks']['g0'] = {'ok': bool(g0 and g0.get('status') == 'PASS'), 'violations': (g0 or {}).get('violations')}
    scr = open(os.path.join(R, 'screen.txt'), encoding='utf-8', errors='replace').read() if os.path.exists(os.path.join(R, 'screen.txt')) else ''
    ref_g1 = B['g1'] if (bed != B100 or job == 'RJ') else None
    if ref_g1 is None and bed == B100:
        T = ul_lib.parse_thermo(_ext_log_text(root))
        row = T['regular'].get(s0)
        ref_g1 = f'{s0} {int(row["Atoms"])} {row["KinEng"]} 0 0' if row else None
    out['checks']['G1'] = ul_gates.g1_check(scr, ref_g1, s0) if ref_g1 else {'status': 'NOT_COMPUTED'}
    orig_atom = _orig_frame(root, bed, job, s0, 'atom', P)
    orig_con = _orig_frame(root, bed, job, s0, 'contact', P)
    orig_mesh = _orig_frame(root, bed, job, s0, 'mesh', P)
    g2a = os.path.join(R, 'g2', f'atom_{s0}.liggghts')
    g2c = os.path.join(R, 'g2', f'contact_{s0}.liggghts')
    g2m = os.path.join(R, 'g2', f'mesh_{s0}.stl')
    # G2 · G2c — 관측 (전부 읽힘 · 머리 step = S0 · ID 고유) 결손 = NOT_COMPUTED → 아래 prepost None → UNCONFIRMED · 값 차이 = FAIL → VALUE_MISMATCH (ULPR-03 · 04 · §14-10)
    out['checks']['G2'] = ul_gates.g2_compare(g2a, orig_atom, step=s0) if orig_atom and os.path.exists(g2a) else {'status': 'NOT_COMPUTED'}
    out['checks']['G2c'] = ul_gates.g2c_compare(g2c, orig_con, step=s0) if orig_con and os.path.exists(g2c) else {'status': 'NOT_COMPUTED'}
    out['checks']['mesh_md5'] = {'status': ('NOT_COMPUTED' if not (orig_mesh and os.path.exists(g2m))
                                            else ('PASS' if ul_gates.mesh_md5_equal(g2m, orig_mesh) else 'FAIL'))}
    log = _orig_log_text(root, bed, job, P)
    out['checks']['G3'] = ul_gates.g3_check(scr, log, s0) if log else {'status': 'NOT_COMPUTED'}
    # 관측 대상 = S0 원자 전부 (원 atom_S0 · 전부 읽힘 · 고유 ID)
    s0d = ul_lib.read_dump(orig_atom, 'custom') if orig_atom else None
    s0_ids = None
    if s0d and s0d['ok'] and s0d['step'] == s0:
        ids = ul_lib.ids_of(s0d['rows'])[0]   # 필수 열 · ID = 정확한 양의 정수 (ULKRR-04 — 열 결손 = 관측 결손 · 예외 없음)
        if ids is not None and len(set(ids)) == len(ids):
            s0_ids = set(ids)
    obs = os.path.join(R, 'obs')
    pre, pre_pr = _obs_frame(os.path.join(obs, 'pre_bot.dump'), HIST_PRE_COLS, s0, s0_ids)
    posts = sorted(x for x in os.listdir(obs) if x.startswith('post_atom_')) if os.path.isdir(obs) else []
    post, post_pr = _obs_frame(os.path.join(obs, f'post_atom_{s0}.dump'), HIST_POST_COLS, s0, s0_ids)
    if posts != [f'post_atom_{s0}.dump']:
        post, post_pr = None, post_pr + [f'POST 덤프 목록 {posts[:3]} ≠ [post_atom_{s0}.dump]']
    equal = None if (pre is None or post is None) else _hist_equal(pre, post)
    out['checks']['pre_post'] = {'ok': equal is True, 'equal': equal, 'problems': (pre_pr + post_pr)[:6]}
    end, end_pr = _obs_frame(os.path.join(obs, 'end_pre_bot.dump'), HIST_PRE_COLS, s_end, s0_ids)
    un, un_pr = _obs_frame(os.path.join(UN, 'obs', 'un_pre_bot.dump'), HIST_PRE_COLS, s_end, s0_ids)
    seen = None if (end is None or un is None) else _erasure_seen(end, un)
    out['checks']['un_erasure'] = {'seen': seen, 'problems': (end_pr + un_pr)[:6]}
    h = _readjson(hist) if hist else None
    hpass, hwhy = _hist_qualifies(h, P)
    sign = (((h or {}).get('info') or {}).get('syn') or {}).get('plate_fn_sign')
    out['checks']['history_test'] = {'pass': hpass, 'why': hwhy, 'source': hist, 'source_sha256': ul_lib.sha256_file(hist) if h is not None else None,
                                     'plate_fn_sign': sign, 'table_sign': P['plate_fn_compressive_sign']}
    gs = [out['checks'][k].get('status') for k in ('G1', 'G2', 'G2c', 'mesh_md5', 'G3')]
    if 'FAIL' in gs or equal is False:
        prepost = False
    elif all(s == 'PASS' for s in gs) and equal is True:
        prepost = True
    else:
        prepost = None
    out['status'] = ul_gates.restoration_verdict(out['checks']['reset_log']['ok'], out['checks']['g0']['ok'], syntax, prepost, hpass, seen)
    return out


def _orig_frame(root, bed, job, s0, kind, P):
    name = {'atom': f'atom_{s0}.liggghts', 'contact': f'contact_{s0}.liggghts', 'mesh': f'mesh_{s0}.stl'}[kind]
    for p in (os.path.join(root, bed, 'in', name), os.path.join(root, bed, 'EXT', 'post', name), os.path.join(root, bed, 'EXT2', 'post', name)):
        if os.path.exists(p):
            return p
    return None


def _orig_log_text(root, bed, job, P):
    if bed == B100 and job == 'RJ2':
        return _ext_log_text(root)
    p = os.path.join(root, bed, 'in', P['beds'][bed]['orig_log'])
    if os.path.exists(p):
        return open(p, encoding='utf-8', errors='replace').read()
    if bed == B73:
        return ul_lib.tgz_member(P['head_source']['r8_log_suffix'], None, P).decode('utf-8', 'replace')
    return None


def _ext_log_text(root):
    txt = ''
    for j in ('EXT', 'EXT2'):
        p = os.path.join(root, B100, j, 'screen.txt')
        if os.path.exists(p):
            txt += open(p, encoding='utf-8', errors='replace').read() + '\n'
    return txt


def _hist_cols(rows):
    return {int(r['id']): tuple(r.get(f'f_history_zwall_bot[{c}]') for c in range(1, 5)) for r in rows}


def _hist_equal(pre, post, rel=1e-12, floor=1e-18):
    """바닥 primitive 이력 PRE_SETUP = POST_SETUP (이력 시험과 같은 허용 — 상대 1e-12 · 절대 1e-18 덱 m)."""
    if not pre or not post:
        return False
    a, b = _hist_cols(pre), _hist_cols(post)
    if set(a) != set(b):
        return False
    for i in a:
        for x, y in zip(a[i], b[i]):
            if x is None or y is None or abs(x - y) > max(rel * abs(x), floor):
                return False
    return True


def _erasure_seen(end_rows, un_rows):
    """보조 소거 진단 — 같은 관측 대상 (ID 집합 같음) 에서 R_END 의 바닥 이력에 0 아닌 값이 있고 UN (소거 뒤 새 프로세스) 에서는 전부 0 이면 참.
    ID 집합이 다르면 비교 미계산 (None — ULKR-05)."""
    if not end_rows or not un_rows:
        return None
    a, b = _hist_cols(end_rows), _hist_cols(un_rows)
    if set(a) != set(b) or len(a) != len(end_rows) or len(b) != len(un_rows):
        return None
    nz_end = any(any(x not in (None, 0.0) for x in v) for v in a.values())
    zero_un = all(all(x == 0.0 for x in v) for v in b.values())
    return bool(nz_end and zero_un)


def _uk_check(root, bed, job, P):
    """UK 회전 KE 출처 (choice C4 · 개정 3 §14-10 · ULKR-09) — 정확히 S0 무이동 완전 세 창만 기준이 된다:
    단계 기술 성공 (run_check UK PASS rc=0 · 배너 · ERROR 없음 · Loop procs = NP · UL_SUMMARY) · 덱 요약 result = DONE · 사건 START = S0 ·
    창 기록 = 머리 = 표 · 버린 줄 없음 · 정확히 uk_windows 줄 · arm UK · bed · k 0 · 단계 4 · w = 1 … n (연속 · 고유) · step = S0 + w · W0 (T_W 간격) ·
    판 높이 = h0 · 들어 올림 0 · 회전 KE 유한 ≥ 0 → (창 평균 목록 | None, 문제)."""
    d = os.path.join(root, bed, job, 'UK')
    B, Wn = P['beds'][bed], P['windows']
    n, W0 = Wn['uk_windows'], Wn['W0']
    s0 = _bed_s0(root, bed, P)
    pr = []
    tech = _stage_tech(d, 'UK', 'UL_SUMMARY')
    pr += [f'UK 단계 {x}' for x in tech['problems']]
    summ = ul_lib.read_kv(os.path.join(d, 'ul_summary.txt')) if os.path.exists(os.path.join(d, 'ul_summary.txt')) else {}
    if summ.get('result') != 'DONE':
        pr.append(f'UK 덱 요약 result {summ.get("result")} ≠ DONE')
    ev, epr = _csv(os.path.join(d, 'ul_events.csv'), P['records']['events_cols'])
    pr += epr
    st = [e for e in ev or [] if e['event'] == 'START']
    if s0 is None or len(st) != 1 or _i(st[0]['step']) != s0 or _i(st[0]['k']) != 0:
        pr.append(f'UK 사건 START ≠ S0 {s0} (k 0) — {[(e["k"], e["step"]) for e in st]}')
    rows, wpr = _csv(os.path.join(d, 'ul_windows.csv'), P['records']['windows_cols'])
    pr += wpr
    rows = rows or []
    if len(rows) != n:
        pr.append(f'UK 창 기록 {len(rows)} 줄 ≠ {n}')
    rot = []
    for idx, r in enumerate(rows, 1):
        w, k, ph, stp, rk = _i(r['w']), _i(r['k']), _i(r['phase']), _i(r['step']), _f(r['ke_rot_avg'])
        pz, lift = _f(r['plate_z']), _f(r['lift'])
        bad = []
        if r['arm'] != 'UK' or r['bed'] != bed:
            bad.append(f'arm · bed {r["arm"]} · {r["bed"]}')
        if w != idx or k != 0 or ph != 4:
            bad.append(f'w {w} (기대 {idx}) · k {k} · 단계 {ph} (기대 4)')
        if s0 is None or stp != s0 + idx * W0:
            bad.append(f'step {stp} ≠ S0 + {idx} · W0')
        if pz is None or abs(pz - B['h0']) > 1e-12 or lift != 0.0:
            bad.append(f'판 {pz} · 들어 올림 {lift} (무이동 아님)')
        if rk is None or rk < 0.0:
            bad.append(f'회전 KE {r["ke_rot_avg"]}')
        if bad:
            pr.append(f'UK 창 {idx}: {" · ".join(bad)}')
        rot.append(rk)
    return (rot if not pr else None), pr


def kebase(root, bed, P=None, write=True):
    """KE 기준 (choice C4): 병진 = 표 (원 로그 이완 끝 · 10:0 = EXT 로그 S0′) · 회전 = UK 창 평균의 중앙값 → S2 문턱 = 10 × 합 · 기준 파일.
    UK 가 정확히 S0 무이동 완전 세 창이 아니면 (_uk_check) 기준 파일을 쓰지 않는다 (ULKR-09 · 문턱 계수 10 은 그대로)."""
    P = P or ul_lib.load_params()
    B = P['beds'][bed]
    job = 'RJ2' if bed == B100 else 'RJ'
    trans = B['ke_base_trans']
    if bed == B100:
        dec = _readjson(os.path.join(root, B100, 's0_decision.json'))
        trans = dec.get('ke_trans') if dec else None
    rot, pr = _uk_check(root, bed, job, P)
    k = ul_observers.ke_base(trans, rot or [], P['steady']['S2_factor'])
    k['problems'] = pr
    if k['s2_limit'] is None:
        k['text'] = None
        return k
    k['text'] = (f'# KE 기준 (ul_reader.py kebase) — {bed} · 병진 {trans!r} J ({"EXT 로그 S0′" if bed == B100 else "표 · 원 로그 이완 끝"}) · '
                 f'회전 {k["rot"]!r} J (UK 창 평균 {len(rot)} 의 중앙값) · S2 문턱 = {P["steady"]["S2_factor"]} × 합\n'
                 f'variable ul_KEbase equal {k["base"]!r}\nvariable ul_S2max equal {k["s2_limit"]!r}\n')
    if write:
        with open(os.path.join(root, bed, 'ul_base.in'), 'w', encoding='utf-8') as f:
            f.write(k['text'])
    return k


def s0p_decision(root, P=None, write=True):
    """10:0 이완 연장 (REG §10 Q11 (가) · §12-11): S0′ = 3,650,000 조건 (EXT 로그) → 미달이면 S0″ = 3,700,000 (EXT2) → 그래도 미달 = F3."""
    P = P or ul_lib.load_params()
    x = P['ext_10_0']
    out = {'status': 'NOT_COMPUTED', 's0': None, 'tried': [], 'ke_trans': None}
    for job, s, end in (('EXT', x['s0p'], x['end1']), ('EXT2', x['s0pp'], x['end2'])):
        p = os.path.join(root, B100, job, 'screen.txt')
        if not os.path.exists(p):
            break
        c = ul_gates.s0p_condition(open(p, encoding='utf-8', errors='replace').read(), s, window=x['cond_window'], frac=x['cond_frac'],
                                   tail=x['tail_lines'])
        ck = os.path.exists(os.path.join(root, B100, job, 'restart', f'restart_ext_{s}.bin'))
        endck = os.path.exists(os.path.join(root, B100, job, 'restart', f'restart_ext_{end}.bin'))
        out['tried'].append({'job': job, 's0': s, 'condition': c['status'], 'max_rel': c.get('max_rel'), 'ckpt': ck, 'end_ckpt': endck})
        if c['status'] == 'PASS' and ck:
            out.update(status='PASS', s0=s, ke_trans=c['ke_base'])
            break
        out['status'] = 'FAIL'
    if out['status'] == 'FAIL' and len(out['tried']) == 2:
        out['status'] = 'F3'
    if write:
        with open(os.path.join(root, B100, 's0_decision.json'), 'w', encoding='utf-8') as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
    return out


def inputs_check(root, bed, P=None):
    """in/ 원 파일 (체크포인트 · atom · contact · mesh) sha256 = 표 · 원 로그 · 원 마지막 조각 덱 있음."""
    P = P or ul_lib.load_params()
    B = P['beds'][bed]
    out = {'ok': True, 'files': {}}
    for key, rec in B['in_files'].items():
        p = os.path.join(root, bed, 'in', rec['file'])
        if not os.path.exists(p):
            out['files'][key] = 'missing'
            out['ok'] = False
            continue
        sh = ul_lib.sha256_file(p)
        out['files'][key] = 'ok' if sh == rec['sha256'] else f'sha256 {sh} ≠ 표'
        out['ok'] = out['ok'] and sh == rec['sha256']
    for key in ('orig_log', 'last_deck'):
        p = os.path.join(root, bed, 'in', B[key])
        out['files'][key] = 'ok (sha256 기록)' if os.path.exists(p) else 'missing'
        out['ok'] = out['ok'] and os.path.exists(p)
    return out


def copy_commands(bed, P=None):
    """원 파일 복사 명령 (침대마다 · 표에서 · 읽기만 · 있으면 덮지 않는다 · REG §8-2 꼴 · 주소 · 사용자 이름 없이 ~ 경로)."""
    P = P or ul_lib.load_params()
    B = P['beds'][bed]
    c, f = B['case'], B['in_files']
    dst = f'~/ps45_unload_20261009/{bed}/in/'
    src = f'~/dem_test/ps45/{c}'
    return [f'# {bed} — 원 파일 여섯 (sha256 = 표 · 러너 사전 점검이 대조)', f'mkdir -p {dst}',
            f'cp -n {src}/restart_{c}/{f["ckpt"]["file"]} {dst}', f'cp -n {src}/post_{c}/{f["atom"]["file"]} {dst}',
            f'cp -n {src}/post_{c}/{f["contact"]["file"]} {dst}', f'cp -n {src}/post_{c}/{f["mesh"]["file"]} {dst}',
            f'cp -n ~/dem_test/ps45/logs/{B["orig_log"]} {dst}', f'cp -n {src}/{B["last_deck"]} {dst}']


AUX_KEYS = ('trajectory_status', 'separation', 's4_status', 'surface_um', 'union_bracket_um', 'union_bracket_pct', 'nonmonotone')


def _t3_entry(root, P):
    """7:3 최종 t3 = UT 주 값 (UT 폴더 판독) + UTc 보조 관측 (분리 · 표면 · 합집합 — 같은 궤적 · 해시로 묶인 부모) (개정 3 §14-3 · ULKR-03).
    UTc 가 없거나 이어 돌림 무효 · UTc 가 다시 읽은 주 값 ≠ UT 주 값 이면 주 값은 그대로 · 보조 = SEP_INCOMPLETE."""
    ut, utc = _arm_v(root, B73, 'UT', P), _arm_v(root, B73, 'UTc', P)
    if ut is None:
        return None
    e = dict(ut, job='UT+UTc', primary_source='UT', aux_source=None)
    why = []
    if utc is None:
        why.append('UTc 없음 — 보조 관측 (분리 · 표면) 미완료')
    elif (utc.get('continuation') or {}).get('status') != 'OK':
        why.append(f'UTc 이어 돌림 무효 ({" · ".join((utc.get("continuation") or {}).get("problems", [])[:2])}) — 보조 관측 미완료')
    elif utc.get('primary_status') != ut.get('primary_status') or not (
            (ut.get('rho_pct') is None and utc.get('rho_pct') is None)
            or (ut.get('rho_pct') is not None and utc.get('rho_pct') is not None and abs(ut['rho_pct'] - utc['rho_pct']) <= 1e-12)):
        why.append(f'UTc 가 다시 읽은 주 값 ({utc.get("primary_status")} · {utc.get("rho_pct")}) ≠ UT 주 값 — 보조 관측 미완료')
    if why:
        e['trajectory_status'] = 'SEP_INCOMPLETE'
        e['why'] = list(ut.get('why') or []) + why
    else:
        for k in AUX_KEYS:
            e[k] = utc.get(k)
        e['aux_source'] = 'UTc'
        e['why'] = list(ut.get('why') or []) + [w for w in (utc.get('why') or []) if w not in (ut.get('why') or [])]
    e['utc'] = None if utc is None else {'primary_status': utc.get('primary_status'), 'rho_pct': utc.get('rho_pct'), 'continuation': utc.get('continuation')}
    return e


def report(root, P=None):
    P = P or ul_lib.load_params()
    s = selection_state(root, P)
    vs = {}
    for bed in BEDS:
        if bed == B73 and s.get('tuple') == 't3':
            vs[bed] = _t3_entry(root, P)
            continue
        job = s.get('arm')
        if job:
            vs[bed] = _arm_v(root, bed, job, P)
    return {'selection': s, 'beds': vs, 'pairs': pair_table({b: v for b, v in vs.items() if v})}


# ── 합성 런 폴더 (덱이 쓰는 꼴 그대로 · 시험 전용) ─────────────────────────────

def _w(path, text):
    """합성 시험 파일 쓰기 — 줄바꿈 LF 고정 (Q4 · Codex 수정 재확인 10-15 §6: Windows 글자 모드가 CRLF 로 써서 LF 글자의 sha256 과 어긋나던 R32 fixture ·
    운영 검사를 늦추지 않는다 — 시험 쪽 이식성)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


def _chain_atoms(ids, plate_z, bad=False, m=1e-6, g=9.81):
    """S3 합성 — 총힘 0 인 원자 (bad = 무게의 10 % 알짜힘)."""
    rows = []
    for k, i in enumerate(ids):
        rows.append({'id': i, 'type': 3, 'x': 0.001 + 0.0005 * k, 'y': 0.002, 'z': min(plate_z * 0.5, 0.01) + 0.001 * k, 'radius': 0.0005,
                     'mass': m, 'vx': 0.0, 'vy': 0.0, 'vz': 0.0, 'omegax': 0.0, 'omegay': 0.0, 'omegaz': 0.0, 'fx': 0.0, 'fy': 0.0,
                     'fz': (0.1 * m * g if bad else 0.0)})
    return rows


def _surf_atoms():
    """합성 S0 의 표면 원자 100 (id 1000–1099 · z 0.05 · 반경 0.0005) — 단 끝 프레임 완전 (full_frames) 용 · 총힘 0 · 접촉 없음."""
    return [{'id': 1000 + i, 'type': 3, 'x': 0.0025, 'y': 0.0025, 'z': 0.05, 'radius': 0.0005, 'mass': 1e-6, 'vx': 0.0, 'vy': 0.0, 'vz': 0.0,
             'omegax': 0.0, 'omegay': 0.0, 'omegaz': 0.0, 'fx': 0.0, 'fy': 0.0, 'fz': 0.0} for i in range(100)]


def _chain_contacts(ids, m=1e-6, g=9.81):
    out = []
    for k in range(len(ids) - 1):
        f = m * g * (len(ids) - 1 - k)
        v = [0.0] * 26
        v[6], v[7] = float(ids[k]), float(ids[k + 1])
        v[9], v[10], v[11] = 0.0, 0.0, -f
        out.append({f'c_cpl[{c + 1}]': v[c] for c in range(26)})
    return out




def _mk_arm(root, bed, job, spec, P):
    """spec = {'W', 'dt', 'steps': [{'lift_um', 'P', 'steady', 'nw', 'kind', 'phase', 'modeB', 'wall' (창마다 [fn_z N …] 또는 None) ,
    's3': 'ok' | 'bad', 'sigma': 보고 MPa}], 'summary': 결과 | None, 'events': [(이름, 단 번호, 설명)], 'post_surface': [(h_um …)] | None}."""
    d = os.path.join(root, bed, job)
    R = P['records']
    B = P['beds'][bed]
    h0 = B['h0']
    W, dt = spec['W'], spec['dt']
    s0 = spec.get('s0', B['s0'] or B.get('s0_candidates', [0])[0])
    th = spec.get('thermo', round(5e-4 / dt))
    step = s0
    wl, sl, el = [','.join(R['windows_cols'])], [','.join(R['steps_cols'])], [','.join(R['events_cols'])]
    head = '    Step    Atoms         KinEng        ul_erot          ul_Ps       pressMPa            CPU '
    thermo = []
    os.makedirs(os.path.join(d, 'dump'), exist_ok=True)
    el.append(f'START,0,{s0},{h0},0,s0')
    ids = [1, 2, 3, 4, 5]
    surf_i = 0

    def run_block(step0, n, Pd, sig):
        """LIGGGHTS run 하나의 화면 — 머리 · setup 줄 (step0) · thermo 주기 정규 줄 · Loop time."""
        thermo.append(head)
        thermo.append(f' {step0} 160417 1e-07 1e-08 {Pd:.12g} {abs(Pd):.12g} 0')
        for t in range(1, n // th + 1):
            noise = (sig / 1000.0) * (1 if t % 2 else -1)
            thermo.append(f' {step0 + t * th} 160417 1e-07 1e-08 {Pd + noise:.12g} {abs(Pd + noise):.12g} 0')
        thermo.append(f'Loop time of 1.0 on 6 procs for {n} steps with 160417 atoms')

    for k, st in enumerate(spec['steps']):
        lift = st['lift_um'] / 1000.0
        pz = h0 + lift
        n_move = st.get('n_move', 0 if k == 0 else (round(spec.get('dzA', 2e-4) / (spec.get('v', 0.01) * dt)) if st.get('kind') == 'A'
                                                       else round(spec.get('dzB', 5e-5) / (spec.get('v', 0.01) * dt))))
        Pd = st['P'] / 1000.0
        sig = st.get('sigma', 0.001)
        if n_move:
            run_block(step, n_move, Pd, 0.0)
        step += n_move
        wsteps = []
        for w in range(1, st['nw'] + 1):
            step0, step = step, step + W
            wsteps.append(step)
            run_block(step0, W, Pd, sig)
            okw = 1 if (st['steady'] and w >= st['nw'] - 1) else 0
            walls = st.get('wall')
            wv = walls[w - 1] if isinstance(walls, list) and w - 1 < len(walls) else ('default' if walls is None else walls)
            if wv == 'missing':
                pass
            else:
                fns = [-(st['P'] * 2.5)] if wv == 'default' else wv
                rows = [{f'c_ul_wh[{c}]': v for c, v in zip(range(1, 7), (0.0, float(j % 2), float(100 + j), 0.0, 0.0, fz))} for j, fz in enumerate(fns)]
                ul_lib.write_local(os.path.join(d, 'dump', f'wall_{step}.dump'), step, [f'c_ul_wh[{c}]' for c in range(1, 7)], rows)
            nc = 0 if wv == 'missing' else (1 if wv == 'default' else len(wv))
            wl.append(f'U,{bed},{k},{w},{st.get("phase", 0)},{step},{pz},{lift},{Pd},1e-07,1e-08,1.1e-07,{okw},{okw},{okw},{nc},160417,11,1e-07')
            if st.get('surface') is not None:
                hs = st['surface'][surf_i] if isinstance(st['surface'], list) else st['surface']
                surf_i += 1
                atoms = []
                for ix in range(10):
                    for iy in range(10):
                        atoms.append({'id': 1000 + ix * 10 + iy, 'type': 3, 'x': 0.0025 + 0.005 * ix, 'y': 0.0025 + 0.005 * iy,
                                      'z': hs / 1000.0 - 0.0005, 'radius': 0.0005, 'mass': 1e-6, 'vx': 0.0, 'vy': 0.0, 'vz': 0.0, 'omegax': 0.0,
                                      'omegay': 0.0, 'omegaz': 0.0, 'fx': 0.0, 'fy': 0.0, 'fz': 0.0})
                ul_lib.write_custom(os.path.join(d, 'dump', f'atom_{step}.dump'), step, ATOM_COLS, atoms)
        steady = 1 if st['steady'] else 0
        Pbar = Pd if st.get('Pbar') is None else st['Pbar']
        sl.append(f'U,{bed},{k},{st.get("kind", "0")},{lift},{n_move},{step},{pz},{lift},{Pbar},{st["nw"]},{steady},{st.get("phase", 0)},'
                  f'{st.get("modeB", 0)},1' + (',x' if st.get('mut') == 'csv_bad' else ''))
        ap, cp = os.path.join(d, 'dump', f'atom_{step}.dump'), os.path.join(d, 'dump', f'contact_{step}.dump')
        if st.get('surface') is None:   # full_frames = 단 끝 프레임에 S0 원자 전부 (사슬 5 + 표면 100 · 같은 반경 — ε 비교 프레임 완전)
            ul_lib.write_custom(ap, step, ATOM_COLS, _chain_atoms(ids, pz, bad=(st.get('s3') == 'bad')) + (_surf_atoms() if spec.get('full_frames') else []))
        ul_lib.write_local(cp, step, [f'c_cpl[{c}]' for c in range(1, 27)], _chain_contacts(ids))
        mut = st.get('mut')
        if mut == 'atom_nan':          # 한 원자의 fz = nan (파서가 그 행을 버린다 — ULKR-04 · Codex nonfinite_atom_salvaged)
            L = open(ap).read().splitlines()
            L[-1] = L[-1].rsplit(' ', 1)[0] + ' nan'
            open(ap, 'w').write('\n'.join(L) + '\n')
        if mut == 'atom_unbalanced':   # 같은 원자 fz = 1e-3 N (불평형 — S3 FAIL 대조)
            L = open(ap).read().splitlines()
            L[-1] = L[-1].rsplit(' ', 1)[0] + ' 0.001'
            open(ap, 'w').write('\n'.join(L) + '\n')
        if mut == 'free_fall_aux':     # 무접촉 저압 끝점 — 쌍 접촉 0 · 원자마다 총힘 = −m g_aux (중력 팔에서 자유 낙하 = 평형 아님 · ULKR-10 B)
            ul_lib.write_custom(ap, step, ATOM_COLS, [dict(a, fz=-a['mass'] * P['g_aux']) for a in _chain_atoms(ids, pz)])
            ul_lib.write_local(cp, step, CPL_COLS, [])
        if mut == 'drop_s0_atom':      # 단 끝 프레임에서 S0 원자 한 행이 빠짐 (선언 수도 맞춤 — 파서 결손 아님 · ε 비교 프레임 불완전 · Codex fixed_volume)
            ul_lib.write_custom(ap, step, ATOM_COLS, (_chain_atoms(ids, pz) + (_surf_atoms() if spec.get('full_frames') else []))[:-1])
        if mut == 'dumps_past':        # 원자 · 쌍 덤프 머리 step 둘 다 100,000 과거 (서로는 같다 — 요청 끝점 시점이 아니다)
            for p in (ap, cp):
                _restep(p, step - 100000)
        if mut == 'wall_past' and os.path.exists(os.path.join(d, 'dump', f'wall_{step}.dump')):
            _restep(os.path.join(d, 'dump', f'wall_{step}.dump'), step - 100000)
        for name, kk, det in spec.get('events', []):
            if kk == k:
                mw = re.fullmatch(r'w(\d+)', det) if name in ('SEPARATED', 'POST_DONE', 'SEP_INCOMPLETE') else None
                est = wsteps[int(mw.group(1)) - 1] if mw and 0 < int(mw.group(1)) <= len(wsteps) else step   # 덱 꼴 — 창 사건은 그 창 끝 step
                el.append(f'{name},{k},{est},{pz},{lift},{det}')
                if name == 'RM':   # 덱 ul_rm 꼴 — R_M restart + 이어 돌릴 상태 파일 (단계 2 · 그 단)
                    _w(os.path.join(d, 'restart', f'restart_RM_{step}.bin'), 'x')
                    _w(os.path.join(d, 'restart', f'state_RM_{step}.in'), f'variable ul_rstep equal {step}\nvariable ul_k equal {k}\nvariable ul_phase equal 2\n'
                       f'variable ul_modeB equal 1\nvariable ul_pz equal {pz}\nvariable ul_lift equal {lift}\nvariable ul_ncross equal 2\n')
    _w(os.path.join(d, 'ul_windows.csv'), '\n'.join(wl) + '\n')
    _w(os.path.join(d, 'ul_steps.csv'), '\n'.join(sl) + '\n')
    _w(os.path.join(d, 'ul_events.csv'), '\n'.join(el) + '\n')
    _w(os.path.join(d, 'screen.txt'), 'LIGGGHTS-PUBLIC 3.8.0 (git 3d5c00f)\n' + '\n'.join(thermo) + '\n')
    if spec.get('summary'):
        _w(os.path.join(d, 'ul_summary.txt'), f'result={spec["summary"]}\narm={job}\nbed={bed}\n')
    if spec.get('deck'):
        _w(os.path.join(d, 'deck.liggghts'), spec['deck'])
    os.makedirs(os.path.join(root, bed, 'in'), exist_ok=True)
    s0f = os.path.join(root, bed, 'in', f'atom_{s0}.liggghts')
    if not os.path.exists(s0f):
        surf = [{'id': 1000 + i, 'type': 3, 'x': 0.0025, 'y': 0.0025, 'z': 0.05, 'radius': 0.0005, 'vx': 0.0, 'vy': 0.0, 'vz': 0.0} for i in range(100)]
        ul_lib.write_custom(s0f, s0, ['id', 'type', 'x', 'y', 'z', 'radius', 'vx', 'vy', 'vz'],
                            [{k2: a[k2] for k2 in ('id', 'type', 'x', 'y', 'z', 'radius', 'vx', 'vy', 'vz')} for a in _chain_atoms(ids, h0)] + surf)
    return d


def _ladder(lifts, Ps, steady=True, nw=4, Pm=1.0, **kw):
    """사다리 단 (k = 0 은 출발 P̄ 160) + 주어진 단들 (B 단) — 단계는 덱 꼴 그대로: 첫 P ≤ P_meas 단 (교차 · 그 유지는 SEARCH 0) → 다음 두 단 CONFIRM 1 → 그 뒤 SEPARATE 2."""
    steps = [{'lift_um': 0.0, 'P': 160.0, 'steady': True, 'nw': 3, 'kind': '0', 'phase': 4}]
    cross = next((i for i, p in enumerate(Ps) if isinstance(p, (int, float)) and p <= Pm), None)
    for i, (lift, p) in enumerate(zip(lifts, Ps)):
        ph = 0 if cross is None or i <= cross else (1 if i <= cross + 2 else 2)
        steps.append(dict({'lift_um': lift, 'P': p, 'steady': steady, 'nw': nw, 'kind': 'B', 'phase': ph, 'modeB': 1, 'n_move': 0}, **kw))
    return steps


_HIST_PRE = list(HIST_PRE_COLS)
_HIST_POST = list(HIST_POST_COLS)


def _mk_utc(root, bed, ut_spec, cont_steps, P, summary='DONE', events=(), layout='hash'):
    """합성 UTc (러너 개정 3 §14-3 꼴) — UT (R_M 에서 멈춘 폴더) 가 이미 있을 때.  같은 사다리 + 이어 돌림 단을 임시 폴더에 한 번에 만들어
    R_M step 뒤 부분만 UTc 로 옮긴다 (경계 step · k 가 정확히 이어진다) · run_manifest (부모 경로 · rm_step · sha256 목록) · 머리만 있는 CSV + 이어 돌림 줄.
    layout = 'hash' (개정 3) · 'copy' (옛 러너 — UT 기록 CSV 를 복사한 꼴) · 'gap' (첫 이어 돌림 단 k 를 하나 건너뜀)."""
    import tempfile as _tf
    ut = os.path.join(root, bed, 'UT')
    ev = [ln.split(',') for ln in open(os.path.join(ut, 'ul_events.csv')).read().splitlines()[1:]]
    rm = [e for e in ev if e[0] == 'RM'][0]
    k_rm, rm_step = int(rm[1]), int(rm[2])
    d = os.path.join(root, bed, 'UTc')
    os.makedirs(os.path.join(d, 'dump'), exist_ok=True)
    R = P['records']
    with _tf.TemporaryDirectory() as tmp:
        full = _mk_arm(tmp, bed, 'FULL', dict(ut_spec, steps=list(ut_spec['steps']) + list(cont_steps), summary=summary,
                                                events=list(ut_spec.get('events', [])) + list(events)), P)
        for name, cols in (('ul_windows.csv', R['windows_cols']), ('ul_steps.csv', R['steps_cols'])):
            rows = [ln for ln in open(os.path.join(full, name)).read().splitlines()[1:] if int(ln.split(',')[5 if name == 'ul_windows.csv' else 6]) > rm_step]
            if layout == 'gap':
                rows = [ln.replace(f',{k_rm + 1},', f',{k_rm + 2},', 1) for ln in rows]
            head = open(os.path.join(ut, name)).read().splitlines() if layout == 'copy' else [','.join(cols)]
            _w(os.path.join(d, name), '\n'.join(head + rows) + '\n')
        erow = [ln for ln in open(os.path.join(full, 'ul_events.csv')).read().splitlines()[1:] if int(ln.split(',')[2]) > rm_step]
        head = open(os.path.join(ut, 'ul_events.csv')).read().splitlines() if layout == 'copy' else [','.join(R['events_cols'])]
        _w(os.path.join(d, 'ul_events.csv'), '\n'.join(head + [f'RESUME,{k_rm},{rm_step},0,0,state'] + erow) + '\n')
        for nm in os.listdir(os.path.join(full, 'dump')):
            if int(re.search(r'_(\d+)\.', nm).group(1)) > rm_step:
                shutil.copy(os.path.join(full, 'dump', nm), os.path.join(d, 'dump', nm))
        blocks, cur = [], []
        for ln in open(os.path.join(full, 'screen.txt')).read().splitlines()[1:]:
            if ln.strip().startswith('Step') and cur:
                blocks.append(cur)
                cur = []
            cur.append(ln)
        blocks.append(cur)
        keep = [b for b in blocks if len(b) > 1 and b[0].strip().startswith('Step') and int(b[1].split()[0]) >= rm_step]
        _w(os.path.join(d, 'screen.txt'), 'LIGGGHTS-PUBLIC 3.8.0 (git 3d5c00f)\n' + '\n'.join(ln for b in keep for ln in b) + '\n')
        if os.path.exists(os.path.join(full, 'ul_summary.txt')):
            _w(os.path.join(d, 'ul_summary.txt'), open(os.path.join(full, 'ul_summary.txt')).read().replace('arm=FULL', 'arm=UTc'))
    _w(os.path.join(d, 'parent_UT.sha256'), parent_sums(ut))
    _w(os.path.join(d, 'run_manifest.txt'), f'bed={bed}\njob=UTc\nresume=0\ngate=ALLOW\ncontinues=UT\nparent_dir={ut}\nrm_step={rm_step}\n'
       f'parent_sums=parent_UT.sha256\nparent_sums_sha256={ul_lib.sha256_file(os.path.join(d, "parent_UT.sha256"))}\n')
    return d


def _restep(path, step):
    """합성 반례 — 덤프 머리의 TIMESTEP 줄만 바꾼다 (파일 이름은 그대로)."""
    L = open(path).read().splitlines()
    k = L.index('ITEM: TIMESTEP')
    L[k + 1] = str(step)
    open(path, 'w').write('\n'.join(L) + '\n')


def _patch_count(path, n):
    """합성 반례 — 덤프 머리의 개수 줄만 바꾼다 (선언 ≠ 실제 행)."""
    L = open(path).read().splitlines()
    k = next(i for i, x in enumerate(L) if x.startswith('ITEM: NUMBER OF'))
    L[k + 1] = str(n)
    open(path, 'w').write('\n'.join(L) + '\n')


def _mk_rj(root, bed, P, mut=None):
    """합성 RJ 폴더 (러너 · R · UNread 덱이 쓰는 꼴 그대로 · 7:3) — Ut0 · R · UN 단계 기록 (run_check) · 화면 · G0 · G2 · G2c · mesh ·
    PRE · POST · R_END · UN 관측 · RJ 잡 기록 (end= fails=0).  mut = 반례 하나 (ULKR-05 시험 전용)."""
    B = P['beds'][bed]
    s0 = B['s0']
    s_end = s0 + P['windows']['R_steps']
    J = os.path.join(root, bed, 'RJ')
    R_, UN = os.path.join(J, 'R'), os.path.join(J, 'UN')
    g1, g3 = B['g1'].split(), B['g3'].split()
    resets = ''.join(f'Resetting {k} state of Fix {f} Style {s} from restart file info\n' for f, s, ks in EXPECTED_RESETS for k in ks)
    head = '    Step    Atoms         KinEng        ul_erot          ul_Ps       pressMPa            CPU \n'
    scr = ('LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, git commit 3d5c00f)\n' + resets + head + f' {g1[0]} {g1[1]} {g1[2]} 1e-08 {g1[4]} {g1[4]} 0\n'
           'Loop time of 0 on 6 procs for 0 steps with 160417 atoms\n' + head + f' {g1[0]} {g1[1]} {g1[2]} 1e-08 {g1[4]} {g1[4]} 0\n'
           f' {g3[0]} {g3[1]} {g3[2]} 1e-08 {g3[4]} {g3[4]} 1\nLoop time of 1 on 6 procs for 2000 steps with 160417 atoms\nUL_R_DONE\n')
    _w(os.path.join(R_, 'screen.txt'), scr)
    if mut != 'r_runcheck_missing':
        _w(os.path.join(R_, 'run_check.txt'), 'R screen.txt PASS rc=0 procs=6\n')
    _w(os.path.join(J, 'Ut0', 'run_check.txt'), 'Ut0 screen.txt ' + ('FAIL rc=1\n' if mut == 'ut0_fail' else 'PASS rc=0 procs=6\n'))
    _w(os.path.join(J, 'Ut0', 'screen.txt'), 'LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, git commit 3d5c00f)\nLoop time of 1 on 6 procs for 100 steps with 160417 atoms\n'
       'UL_SUMMARY arm=Ut0 bed=x result=DONE\n' + ('ERROR: synthetic Ut0 failure\n' if mut == 'ut0_fail' else ''))
    _w(os.path.join(J, 'g0.json'), json.dumps({'status': 'PASS', 'violations': []}))
    cols = ['id', 'type', 'x', 'y', 'z', 'radius', 'vx', 'vy', 'vz', 'c_strs[1]', 'c_strs[2]', 'c_strs[3]', 'c_ke']
    rows = [{'id': i, 'type': 3, 'x': 0.001 * i, 'y': 0.002, 'z': 0.003, 'radius': 0.0005, 'vx': 1e-6, 'vy': 0.0, 'vz': 0.0, 'c_strs[1]': 0.0,
             'c_strs[2]': 0.0, 'c_strs[3]': 0.0, 'c_ke': 0.0} for i in range(1, 4)]
    for p in (os.path.join(root, bed, 'in', f'atom_{s0}.liggghts'), os.path.join(R_, 'g2', f'atom_{s0}.liggghts')):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        dup = mut == 'g2_dup_id' and p.startswith(R_)   # ULPR-03 — R/g2 원자 덤프에 같은 ID 두 줄 (첫 줄 x 다름 · 선언 수 = 행 수)
        ul_lib.write_custom(p, s0, cols, ([dict(rows[0], x=0.9)] if dup else []) + rows, fmt=lambda x: f'{x:g}')
    ccols = [f'c_cpl[{c}]' for c in range(1, 27)]
    crow = dict(zip(ccols, [0.001, 0.01, 0.01, 0.0015, 0.01, 0.01, 1, 2, 0, -0.5, 0, 0, -0.5, 0, 0, 0, 0.01, 0, 0, 0, 0, 1e-8, 1e-5, 0.00125, 0.01, 0.01]))
    for p in (os.path.join(root, bed, 'in', f'contact_{s0}.liggghts'), os.path.join(R_, 'g2', f'contact_{s0}.liggghts')):
        val = mut == 'g2c_value' and p.startswith(R_)   # ULPR-04 대조 — R/g2 쌍 덤프 법선 힘 −0.5 → −0.6 (수치 불일치 · 관측은 완전)
        ul_lib.write_local(p, s0, ccols, [dict(crow, **{'c_cpl[10]': -0.6}) if val else crow])
    m3 = re.fullmatch(r'g2c_(test|orig)_no_c([78])', mut or '')
    if m3:   # ULKRF-03 (Codex g2c_c_cpl7_missing · g2c_c_cpl8_missing) — G2c 쌍 덤프 머리의 필수 열 하나만 이름 바꿈 (숫자 행 · 다른 파일 그대로)
        col = f'c_cpl[{m3.group(2)}]'
        _dump_field(os.path.join(R_, 'g2', f'contact_{s0}.liggghts') if m3.group(1) == 'test' else os.path.join(root, bed, 'in', f'contact_{s0}.liggghts'),
                    col, rename=f'not_{col}')
    stl = 'solid LIGGGHTS_STL_EXPORT\n facet normal 0 0 -1\n  outer loop\n   vertex 0 0 0.111052\n   vertex 0.05 0.05 0.111052\n   vertex 0.05 0 0.111052\n'
    for p in (os.path.join(root, bed, 'in', f'mesh_{s0}.stl'), os.path.join(R_, 'g2', f'mesh_{s0}.stl')):
        _w(p, stl)

    def atom(i, h):
        a = {'id': i, 'type': 1 if i == 1 else 3, 'x': 0.001 * i, 'y': 0.002, 'z': 0.003, 'radius': 0.0005, 'mass': 1e-6, 'vx': 1e-6, 'vy': 0.0,
             'vz': 0.0, 'omegax': 0.0, 'omegay': 0.0, 'omegaz': 0.0, 'fx': 0.0, 'fy': 0.0, 'fz': 0.0}
        a.update({f'f_history_zwall_bot[{c}]': v for c, v in zip(range(1, 5), h)})
        return a
    hist = [atom(1, (2e-5, 1e-6, 0.0, 0.0)), atom(2, (0.0,) * 4), atom(3, (0.0,) * 4)]
    zero = [atom(i, (0.0,) * 4) for i in (1, 2, 3)]
    obs = os.path.join(R_, 'obs')
    pre, post = os.path.join(obs, 'pre_bot.dump'), os.path.join(obs, f'post_atom_{s0}.dump')
    end, unp = os.path.join(obs, 'end_pre_bot.dump'), os.path.join(UN, 'obs', 'un_pre_bot.dump')
    os.makedirs(obs, exist_ok=True)
    os.makedirs(os.path.dirname(unp), exist_ok=True)
    ul_lib.write_custom(pre, s0, _HIST_PRE, hist[:1] if mut == 'trunc_prepost' else hist)
    ul_lib.write_custom(post, s0, _HIST_POST, (hist[:1] if mut == 'trunc_prepost' else hist) + (hist[:1] if mut == 'post_dup_id' else []))
    if mut == 'trunc_prepost':
        _patch_count(pre, 3)
        _patch_count(post, 3)
    if mut == 'pre_nan':
        L = open(pre).read().splitlines()
        L[-2] = L[-2].rsplit(' ', 1)[0] + ' nan'
        open(pre, 'w').write('\n'.join(L) + '\n')
    ul_lib.write_custom(end, s_end - 1000 if mut == 'end_wrong_step' else s_end, _HIST_PRE, hist)
    ul_lib.write_custom(unp, s_end, _HIST_PRE, [dict(zero[0], id=999)] if mut == 'un_other_ids' else zero)
    if mut == 'un_frac_id':        # Codex fractional_un_id — UN 첫 ID 1 → 1.5 (나머지 그대로 · 정수 1 로 잘리면 같은 대상으로 보인다)
        _dump_field(unp, 'id', 0, '1.5')
    if mut == 'pre_frac_id':       # PRE 둘째 ID 2 → 2.5
        _dump_field(pre, 'id', 1, '2.5')
    if mut == 's0_no_id':          # 원 atom_S0 머리 id → not_id (필수 열 결손 — 예외가 아니라 관측 결손)
        _dump_field(os.path.join(root, bed, 'in', f'atom_{s0}.liggghts'), 'id', rename='not_id')
    _w(os.path.join(UN, 'screen.txt'), 'LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, git commit 3d5c00f)\nUL_UN_START\n'
       'Loop time of 0 on 6 procs for 0 steps with 160417 atoms\nUL_UN_DONE\n' + ('ERROR: synthetic failure after a partial dump\n' if mut == 'un_tech_fail' else ''))
    _w(os.path.join(UN, 'run_check.txt'), 'UNread screen.txt ' + ('FAIL rc=1\n' if mut == 'un_tech_fail' else 'PASS rc=0 procs=6\n'))
    end_line = {'manifest_no_end': '', 'manifest_fail': 'end=x fails=1 reader_rc=0\n', 'manifest_reader_rc': 'end=x fails=0 reader_rc=120\n',
                'manifest_reader_rc_missing': 'end=x fails=0\n', 'manifest_reader_rc_text': 'end=x fails=0 reader_rc=x\n'}.get(mut, 'end=x fails=0 reader_rc=0\n')
    _w(os.path.join(J, 'run_manifest.txt'), f'bed={bed}\njob=RJ\nresume=0\n' + ('' if mut == 'manifest_no_grammar' else 'grammar_prereq=PASS\n')
       + 'start=x\n' + end_line)
    return J


_HIST_TGZ = ('docs/reviews/dem_unloading_history_test_20261014/hist_20261014_094731.report.tgz',
             'be0acbd7841d0922604eee8aa31524fcddbe179a8240f937b317432dbebb0ca0')


def _repo_history_verdict():
    """반입된 실제 이력 시험 판정 (10-14 · job 283122) — 리포 보고 묶음 (sha256 대조) 안 history_verdict.json 을 자료로만 읽는다 (시험 전용)."""
    import tarfile
    p = os.path.join(ul_lib.REPO, _HIST_TGZ[0])
    if not os.path.exists(p) or ul_lib.sha256_file(p) != _HIST_TGZ[1]:
        return None
    with tarfile.open(p, 'r:gz') as t:
        ms = [m for m in t.getmembers() if m.isfile() and m.name.endswith('/history_verdict.json')]
        return json.load(t.extractfile(ms[0])) if len(ms) == 1 else None


def _fake_restored(root, bed, job='RJ'):
    """관문 순서 시험 전용 — RESTORED 증서 + 그 RJ 잡 기록 (러너 꼴: 문법 fixture 사전 점검 PASS 줄 · 끝 줄 end= fails=0 reader_rc=0)."""
    _w(os.path.join(root, bed, job, 'restore_verdict.json'), json.dumps({'status': 'RESTORED'}))
    _w(os.path.join(root, bed, job, 'run_manifest.txt'), f'bed={bed}\njob={job}\nresume=0\ngrammar_prereq=PASS\nend=x fails=0 reader_rc=0\n')


def _edit_rows(path, mutate):
    """합성 반례 — 기록 CSV (머리 = 표) 의 줄 목록을 열 이름으로 바꾼다 (mutate(rows: list[dict]))."""
    L = open(path).read().splitlines()
    cols = L[0].split(',')
    rows = [dict(zip(cols, ln.split(','))) for ln in L[1:] if ln.strip()]
    mutate(rows)
    _w(path, '\n'.join([L[0]] + [','.join(r[c] for c in cols) for r in rows]) + '\n')


def _dump_field(path, col, row=None, value=None, rename=None):
    """합성 반례 — 덤프 한 장의 한 칸 (열 이름 · 데이터 행 번호) 을 글자 그대로 바꾸거나 · 머리의 열 이름 하나를 바꾼다 (rename)."""
    L = open(path).read().splitlines()
    k = next(i for i, x in enumerate(L) if x.startswith(('ITEM: ATOMS', 'ITEM: ENTRIES')))
    head = L[k].split()
    if rename is not None:
        L[k] = ' '.join(head[:2] + [rename if c == col else c for c in head[2:]])
    else:
        f = L[k + 1 + row].split()
        f[head[2:].index(col)] = value
        L[k + 1 + row] = ' '.join(f)
    _w(path, '\n'.join(L) + '\n')


def _resume_layout(d, P, kr=1, manifest=True, ev_k=None, state_k=None, state_file=True, job='UT', repeat=1, resumes=None, dup_event=False,
                   conflict_k=None):
    """합성 이어 돌림 (러너 · 덱이 쓰는 꼴 — ULKRR-02 양성 대조 · 반례): 첫 시도가 단 kr 끝 (restart_unload_<s_r> + state_unload_<s_r>) 뒤 단 kr + 1 의
    창 둘 · 단 줄 하나 · 사건 하나를 남기고 끊김 (P 9.999 — 그대로 쓰면 주 값이 바뀐다) → 두 번째 시도 = RESUME (k kr · step s_r) + 나머지 기록.
    manifest = 러너 시도 기록 (run_manifest resume_from=s_r) · ev_k / state_k = RESUME 사건 · 상태 파일의 k (반례) · state_file = 상태 파일 유무 → s_r.
    ULKRF-01 반례 (Codex 수정 재확인 10-15): repeat = 끊긴 시도 묶음 수 (묶음마다 위 창 둘 · 단 줄 · 사건) · resumes = RESUME 사건 줄 수 (기본 = repeat ·
    앞 묶음부터 하나씩 뒤에 — 러너 resume_from · 상태 파일은 그대로 하나) · dup_event = 마지막 RESUME 바로 뒤 같은 줄 하나 더 (같은 경계 중복) ·
    conflict_k = 마지막 RESUME 바로 뒤 같은 step · 다른 k 의 RESUME 하나 (상충)."""
    R = P['records']
    wc, sc, ec = R['windows_cols'], R['steps_cols'], R['events_cols']
    paths = [os.path.join(d, f) for f in ('ul_windows.csv', 'ul_steps.csv', 'ul_events.csv')]
    W, S, E = ([ln.split(',') for ln in open(p).read().splitlines()[1:] if ln.strip()] for p in paths)
    wk, ws, wP = wc.index('k'), wc.index('step'), wc.index('Ps_avg')
    sk, ss, sP = sc.index('k'), sc.index('step'), sc.index('Pbar')
    es = ec.index('step')
    rowk = next(r for r in S if int(r[sk]) == kr)
    sr = int(rowk[ss])
    stale_w = [r[:wP] + ['9.999'] + r[wP + 1:] for r in W if int(r[wk]) == kr + 1][:2]
    stale_s = [r[:sP] + ['9.999'] + r[sP + 1:] for r in S if int(r[sk]) == kr + 1][:1]
    stale_e = [r for r in E if int(r[es]) > sr][:1]
    res = ['RESUME', str(kr if ev_k is None else ev_k), str(sr), rowk[sc.index('plate_z')], rowk[sc.index('lift')], 'state']
    nres = repeat if resumes is None else resumes
    seg_w, seg_s, seg_e = [], [], []
    for i in range(repeat):   # 끊긴 시도 묶음 (기본 하나 = 옛 꼴 그대로)
        seg_w += [list(r) for r in stale_w]
        seg_s += [list(r) for r in stale_s]
        seg_e += [list(r) for r in stale_e] + ([list(res)] if i < nres else [])
    if dup_event:
        seg_e.append(list(res))
    if conflict_k is not None:
        seg_e.append([res[0], str(conflict_k)] + res[2:])

    def cat(head, rows):
        return '\n'.join([','.join(head)] + [','.join(r) for r in rows]) + '\n'
    _w(paths[0], cat(wc, [r for r in W if int(r[ws]) <= sr] + seg_w + [r for r in W if int(r[ws]) > sr]))
    _w(paths[1], cat(sc, [r for r in S if int(r[ss]) <= sr] + seg_s + [r for r in S if int(r[ss]) > sr]))
    _w(paths[2], cat(ec, [r for r in E if int(r[es]) <= sr] + seg_e + [r for r in E if int(r[es]) > sr]))
    _w(os.path.join(d, 'restart', f'restart_unload_{sr}.bin'), 'x')
    if state_file:
        _w(os.path.join(d, 'restart', f'state_unload_{sr}.in'), f'variable ul_rstep equal {sr}\nvariable ul_k equal {kr if state_k is None else state_k}\n'
           'variable ul_phase equal 0\nvariable ul_modeB equal 1\n')
    bed = os.path.basename(os.path.dirname(d))
    _w(os.path.join(d, 'run_manifest.txt'), f'bed={bed}\njob={job}\nresume=0\ngate=ALLOW\nstart=a1\nstage={job} screen=screen.txt rc=1 check= rc=1\n'
       f'reader_arm_rc=0\nend=a1 fails=1 reader_rc=0\nbed={bed}\njob={job}\nresume=1\ngate=RESUME\nstart=a2\n'
       + (f'resume_from={sr}\n' if manifest else '') + f'stage={job} screen=screen_a2.txt rc=0 check=PASS\nreader_arm_rc=0\nend=a2 fails=0 reader_rc=0\n')
    return sr


def _ut_trace(P, nw2, bed=B73):
    """생성된 UT 덱의 제어 흐름 (make_unload_decks.deck_sim · 입자 계산 없음) → 덱이 쓰는 기록 줄 (ULKRF-02 시험 전용).
    창 압력 (덱 MPa) = k 0 0.16 · k 1 0.0012 · k 2 0.0008 (앞 창 + (nw2 − 2 − w) × 1e-4) · k 3 0.0006 · k 4 0.0004 → 단 k 2 유지 = nw2 창
    (nw2 5 = 0.0010 · 0.0009 · 0.0008 · 0.0008 · 0.0008 → S1 [0, 0, 0, 1, 1]) · 교차 k 2 · 확인 k 3 · 4 · R_M 멈춤."""
    import make_unload_decks as mk

    def obs(k, w, phase, step):
        pd = {None: 0.16, 0: 0.16, 1: 0.0012, 2: 0.0008, 3: 0.0006, 4: 0.0004}.get(k, 0.0002)
        if k == 2 and w <= nw2 - 3:
            pd += (nw2 - 2 - w) * 0.0001
        return {'P': pd, 'Kt': 1e-7, 'Kr': 1e-8, 'Kti': 1e-7, 'nc': 1, 'na': 160417, 'lk': 11}
    return mk.deck_sim(mk.render(bed, 'UT', P), obs, P['beds'][bed]['s0'], cli={'ul_resume': '0'})


def _ut_trace_arm(root, P, nw2, bed=B73):
    """UT 런 폴더 (ULKRF-02 시험 전용) — 덤프 · thermo · 덱 사본 = _mk_arm (같은 사다리 · 첫 이동 A · 그 뒤 B · 이동 길이 = 덱 셈 · 단 k 2 유지 nw2 창) ·
    기록 CSV = 생성 UT 덱 제어 흐름 (_ut_trace) 그대로 → (폴더, 흐름)."""
    import make_unload_decks as mk
    steps = _ladder([0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4])
    for i, r in enumerate(steps[1:], 1):
        r['kind'] = 'A' if i == 1 else 'B'
        r.pop('n_move', None)
    steps[2]['nw'] = nw2
    shutil.rmtree(os.path.join(root, bed, 'UT'), ignore_errors=True)
    d = _mk_arm(root, bed, 'UT', {'W': 10000, 'dt': 5e-7, 'steps': steps, 'summary': 'RM_STOP', 'events': [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')],
                                  'full_frames': True, 'deck': mk.render(bed, 'UT', P)}, P)
    tr = _ut_trace(P, nw2, bed)
    R = P['records']
    for n in ('windows', 'steps', 'events'):
        _w(os.path.join(d, f'ul_{n}.csv'), '\n'.join([','.join(R[f'{n}_cols'])] + [','.join(r) for r in tr[n]]) + '\n')
    return d, tr


def _hold_resume(d, P, old_nw, auth=True, kr=1):
    """ULKRF-02 반례 꼴 (Codex resume_completed_hold_*) — 첫 시도가 단 kr + 1 을 old_nw 창 유지로 끝내고 단 줄 · 그 단 사건 (CROSS) 까지 쓴 뒤 그 단 끝
    restart · 상태 파일 전에 끊김 (덱 순서 = 단 줄 → 사건 → restart · 상태 파일 · in.UT 의 ul_hold_end → ul_step_done) → 러너가 단 kr 끝 (s_r) restart +
    상태 파일에서 이어 돌림 (auth · RESUME (kr · s_r) · resume_from=s_r) — 지금 폴더 기록 (새 시도) 앞에 옛 시도의 그 단 줄 (P 9.999) · 옛 덤프 (새 시도가 안 덮은 것) 를
    둔다.  auth 거짓 = RESUME 사건 · resume_from · 상태 파일 없이 같은 줄 (승인 없는 되돌아옴) → s_r."""
    import tempfile as _tf
    R = P['records']
    wc, sc, ec = R['windows_cols'], R['steps_cols'], R['events_cols']
    old = _ut_trace(P, old_nw)
    rd = {n: [ln.split(',') for ln in open(os.path.join(d, f'ul_{n}.csv')).read().splitlines()[1:] if ln.strip()] for n in ('windows', 'steps', 'events')}
    rowk = next(r for r in rd['steps'] if int(r[sc.index('k')]) == kr)
    sr = int(rowk[sc.index('step')])
    k1 = str(kr + 1)
    ow = [r[:wc.index('Ps_avg')] + ['9.999'] + r[wc.index('Ps_avg') + 1:] for r in old['windows'] if r[wc.index('k')] == k1]
    osr = [r[:sc.index('Pbar')] + ['9.999'] + r[sc.index('Pbar') + 1:] for r in old['steps'] if r[sc.index('k')] == k1]
    oe = [list(r) for r in old['events'] if r[ec.index('k')] == k1]
    res = [['RESUME', str(kr), str(sr), rowk[sc.index('plate_z')], rowk[sc.index('lift')], 'state']] if auth else []

    def cat(head, rows):
        return '\n'.join([','.join(head)] + [','.join(r) for r in rows]) + '\n'
    for n, head, idx, stale in (('windows', wc, wc.index('step'), ow), ('steps', sc, sc.index('step'), osr), ('events', ec, ec.index('step'), oe)):
        rows = rd[n]
        _w(os.path.join(d, f'ul_{n}.csv'), cat(head, [r for r in rows if int(r[idx]) <= sr] + stale + (res if n == 'events' else [])
                                              + [r for r in rows if int(r[idx]) > sr]))
    s_old = max(int(r[wc.index('step')]) for r in ow)
    with _tf.TemporaryDirectory() as tmp:   # 옛 시도 덤프 (끊긴 그 단 끝까지 · 새 시도가 같은 이름으로 덮지 않은 것은 디스크에 남는다)
        od, _otr = _ut_trace_arm(tmp, P, old_nw)
        for nm in os.listdir(os.path.join(od, 'dump')):
            if int(re.search(r'_(\d+)\.', nm).group(1)) <= s_old and not os.path.exists(os.path.join(d, 'dump', nm)):
                shutil.copyfile(os.path.join(od, 'dump', nm), os.path.join(d, 'dump', nm))
    bed = os.path.basename(os.path.dirname(d))
    if auth:
        _w(os.path.join(d, 'restart', f'restart_unload_{sr}.bin'), 'x')
        _w(os.path.join(d, 'restart', f'state_unload_{sr}.in'), f'variable ul_rstep equal {sr}\nvariable ul_k equal {kr}\nvariable ul_phase equal 0\n'
           'variable ul_modeB equal 1\n')
        _w(os.path.join(d, 'run_manifest.txt'), f'bed={bed}\njob=UT\nresume=0\ngate=ALLOW\nstart=a1\nstage=UT screen=screen.txt rc=1 check= rc=1\n'
           f'reader_arm_rc=0\nend=a1 fails=1 reader_rc=0\nbed={bed}\njob=UT\nresume=1\ngate=RESUME\nstart=a2\nresume_from={sr}\n'
           'stage=UT screen=screen_a2.txt rc=0 check=PASS\nreader_arm_rc=0\nend=a2 fails=0 reader_rc=0\n')
    else:
        _w(os.path.join(d, 'run_manifest.txt'), f'bed={bed}\njob=UT\nresume=0\ngate=ALLOW\nstart=a1\nstage=UT screen=screen.txt rc=0 check=PASS\n'
           'reader_arm_rc=0\nend=a1 fails=0 reader_rc=0\n')
    return sr


def _resume_mix(d, P, kr, old_nw=0, old_line=False, old_ev=False, old_events=(), new_nw=0, new_line=False, new_ev=False, new_state=False,
                rest=False, end='TIMEOUT', resumed=True, next_nw=0):
    """ULPR-01 시험 꼴 (사전 리뷰 10-21 PRE-UL-01 · 탐침 probe_resume_unfinished 의 일반화) — d = 한 시도가 처음부터 끝까지 쓴 팔 폴더 (_mk_arm = 기준 궤적).
    덱이 쓰는 순서 (in.UT · in.U_* 의 ul_win → ul_hold_end → 단 끝 사건 → ul_step_done): 창 줄 → 단 줄 → 단 끝 사건 (CROSS · MODE_B · RM …) →
    단 끝 restart_unload + 상태 파일 (UT 의 R_M 단은 restart_RM · 상태만 · 멈춤).  단 kr 끝 (s_r) 까지 = 기준 그대로 · 단 kr + 1 = 옛 시도 (창 old_nw 개 ·
    old_line = 그 단 줄 · old_ev = 기준의 그 단 사건 · old_events = [(사건 이름, 창 번호)] 합성 창 사건) → (resumed) RESUME (kr · s_r) · 러너 resume_from=s_r ·
    restart_unload_<s_r> + 상태 파일 → 새 시도 (창 new_nw 개 · new_line · new_ev · new_state = 그 단 끝 restart_unload + 상태 파일 · rest = 단 kr + 2 부터
    기준 끝까지 + 기준 요약 · next_nw = rest 없이 단 kr + 2 의 창만 그 개수) · end = TIMEOUT (요약 없음) · GUARD (새 시도 마지막 창에 GUARD 사건 + 요약 GUARD).
    resumed 거짓 = 새 시도 줄만 (같은 꼴 fresh — 옛 줄 · RESUME · resume_from 없음).  덤프 = 기준 그대로 (판독기는 남은 기록 step 의 덤프만 읽는다) → s_r."""
    R = P['records']
    wc, sc, ec = R['windows_cols'], R['steps_cols'], R['events_cols']
    rd = {n: [ln.split(',') for ln in open(os.path.join(d, f'ul_{n}.csv')).read().splitlines()[1:] if ln.strip()] for n in ('windows', 'steps', 'events')}
    wk, ws, sk, ss, ek, es = wc.index('k'), wc.index('step'), sc.index('k'), sc.index('step'), ec.index('k'), ec.index('step')
    rowk = next(r for r in rd['steps'] if int(r[sk]) == kr)
    sr, k1 = int(rowk[ss]), kr + 1
    W1 = [r for r in rd['windows'] if int(r[wk]) == k1]
    S1 = [r for r in rd['steps'] if int(r[sk]) == k1]
    E1 = [r for r in rd['events'] if int(r[es]) > sr and int(r[ek]) == k1]
    Wr, Sr = [r for r in rd['windows'] if int(r[wk]) > k1], [r for r in rd['steps'] if int(r[sk]) > k1]
    Er = [r for r in rd['events'] if int(r[es]) > sr and int(r[ek]) > k1]
    pz, lf = wc.index('plate_z'), wc.index('lift')
    old_w = [list(r) for r in W1[:old_nw]]
    old_s = [list(r) for r in S1] if old_line else []
    old_e = ([list(r) for r in E1] if old_ev else []) + [[n, str(k1), W1[w - 1][ws], W1[w - 1][pz], W1[w - 1][lf], f'w{w}'] for n, w in old_events]
    new_w = [list(r) for r in W1[:new_nw]] + ([list(r) for r in Wr] if rest else [list(r) for r in Wr if int(r[wk]) == k1 + 1][:next_nw])
    new_s = ([list(r) for r in S1] if new_line else []) + ([list(r) for r in Sr] if rest else [])
    new_e = ([list(r) for r in E1] if new_ev else []) + ([list(r) for r in Er] if rest else [])
    if end == 'GUARD':
        new_e.append(['GUARD', str(k1), W1[new_nw - 1][ws], W1[new_nw - 1][pz], W1[new_nw - 1][lf], 'ke_trans_inst'])
    res = [['RESUME', str(kr), str(sr), rowk[sc.index('plate_z')], rowk[sc.index('lift')], 'state']]

    def cat(head, rows):
        return '\n'.join([','.join(head)] + [','.join(r) for r in rows]) + '\n'
    keep = {n: [r for r in rd[n] if int(r[(ws, ss, es)[i]]) <= sr] for i, n in enumerate(('windows', 'steps', 'events'))}
    if resumed:
        _w(os.path.join(d, 'ul_windows.csv'), cat(wc, keep['windows'] + old_w + new_w))
        _w(os.path.join(d, 'ul_steps.csv'), cat(sc, keep['steps'] + old_s + new_s))
        _w(os.path.join(d, 'ul_events.csv'), cat(ec, keep['events'] + old_e + res + new_e))
        _w(os.path.join(d, 'restart', f'restart_unload_{sr}.bin'), 'x')
        _w(os.path.join(d, 'restart', f'state_unload_{sr}.in'), f'variable ul_rstep equal {sr}\nvariable ul_k equal {kr}\nvariable ul_phase equal 0\n'
           'variable ul_modeB equal 1\n')
    else:
        _w(os.path.join(d, 'ul_windows.csv'), cat(wc, keep['windows'] + new_w))
        _w(os.path.join(d, 'ul_steps.csv'), cat(sc, keep['steps'] + new_s))
        _w(os.path.join(d, 'ul_events.csv'), cat(ec, keep['events'] + new_e))
    if new_state and S1:
        s1 = int(S1[0][ss])
        _w(os.path.join(d, 'restart', f'restart_unload_{s1}.bin'), 'x')
        _w(os.path.join(d, 'restart', f'state_unload_{s1}.in'), f'variable ul_rstep equal {s1}\nvariable ul_k equal {k1}\nvariable ul_phase equal 0\n'
           'variable ul_modeB equal 1\n')
    smp = os.path.join(d, 'ul_summary.txt')
    summ = open(smp).read() if os.path.exists(smp) else None
    if os.path.exists(smp):
        os.remove(smp)
    job, bed = os.path.basename(d), os.path.basename(os.path.dirname(d))
    if end == 'GUARD':
        _w(smp, f'result=GUARD\narm={job}\nbed={bed}\n')
    elif rest and summ:
        _w(smp, summ)
    done = os.path.exists(smp)
    a1 = f'bed={bed}\njob={job}\nresume=0\ngate=ALLOW\nstart=a1\n'
    if resumed:
        man = (a1 + f'stage={job} screen=screen.txt rc=1 check= rc=1\nreader_arm_rc=0\nend=a1 fails=1 reader_rc=0\n'
               f'bed={bed}\njob={job}\nresume=1\ngate=RESUME\nstart=a2\nresume_from={sr}\n'
               + (f'stage={job} screen=screen_a2.txt rc=0 check=PASS\nreader_arm_rc=0\nend=a2 fails=0 reader_rc=0\n' if done else ''))
    else:
        man = a1 + (f'stage={job} screen=screen.txt rc=0 check=PASS\nreader_arm_rc=0\nend=a1 fails=0 reader_rc=0\n' if done else '')
    _w(os.path.join(d, 'run_manifest.txt'), man)
    return sr


def _mk_uk(root, P, mut=None, bed=B73, job='RJ'):
    """합성 UK 단계 (덱 in.UK 꼴 그대로 — 창 기록 · 사건 · 요약 · 화면 · 단계 기록) · mut = 반례 하나 (ULKR-09 · Codex one_uk_row 꼴)."""
    uk = os.path.join(root, bed, job, 'UK')
    shutil.rmtree(uk, ignore_errors=True)
    B = P['beds'][bed]
    s0, h0, W0 = B['s0'], B['h0'], P['windows']['W0']
    rows = [{'arm': 'UK', 'k': 0, 'w': w, 'ph': 4, 'step': s0 + W0 * w, 'pz': h0, 'lift': 0, 'rot': r} for w, r in ((1, 3e-8), (2, 1e-8), (3, 2e-8))]
    if mut == 'one_row':        # Codex one_uk_row — step 1 · w 1 · 회전 0.001 J 한 줄
        rows = [dict(rows[0], step=1, rot=0.001)]
    elif mut == 'dup_w':        # 같은 창 두 번 (w 1 · 2 · 2)
        rows[2] = dict(rows[1])
    elif mut == 'spacing':      # 셋째 창 끝 step 이 T_W 간격 밖
        rows[2]['step'] += 1000
    elif mut == 'motion':       # 둘째 창에서 판이 움직임 (무이동 아님)
        rows[1].update(pz=h0 + 1e-5, lift=1e-5)
    elif mut == 'k1':           # k = 1 (S0 k = 0 아님)
        for r in rows:
            r['k'] = 1
    elif mut == 'phase0':       # 단계 0 (HOLD0 4 아님)
        rows[0]['ph'] = 0
    elif mut == 'four':         # 넷째 창 (정확히 셋 아님)
        rows.append(dict(rows[2], w=4, step=s0 + 4 * W0))
    elif mut == 'other_arm':    # 다른 팔의 창 기록
        for r in rows:
            r['arm'] = 'UB'
    body = [f'{r["arm"]},{bed},{r["k"]},{r["w"]},{r["ph"]},{r["step"]},{r["pz"]},{r["lift"]},0.16,2e-07,{r["rot"]},0,-1,-1,-1,400,160417,11,2e-07'
            for r in rows]
    if mut == 'csv_bad':        # 열 수 다른 줄 (파서가 버린다 — 남은 두 줄로 기준을 만들면 안 된다)
        body[1] += ',x'
    _w(os.path.join(uk, 'ul_windows.csv'), ','.join(P['records']['windows_cols']) + '\n' + '\n'.join(body) + '\n')
    _w(os.path.join(uk, 'ul_events.csv'), ','.join(P['records']['events_cols']) + f'\nSTART,0,{s0},{h0},0,s0\nNOMOVE_DONE,0,{s0 + 3 * W0},{h0},0,w3\n')
    _w(os.path.join(uk, 'ul_summary.txt'), f'result={"GUARD" if mut == "guard" else "DONE"}\narm=UK\nbed={bed}\n')
    _w(os.path.join(uk, 'screen.txt'), 'LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, git commit 3d5c00f)\n'
       'Loop time of 1 on 6 procs for 15000 steps with 160417 atoms\n'
       f'UL_SUMMARY arm=UK bed={bed} result={"GUARD" if mut == "guard" else "DONE"} step={s0 + 3 * W0} k=0\n'
       + ('ERROR: synthetic UK failure\n' if mut == 'tech' else ''))
    _w(os.path.join(uk, 'run_check.txt'), 'UK screen.txt ' + ('FAIL ERROR rc=1\n' if mut == 'tech' else 'PASS rc=0 procs=6\n'))
    return uk


#: 문법 fixture 판정 (read_history.py --grammar) 의 검사 열아홉 — 시험이 따로 적는다 (구현 상수를 베끼지 않는다 · Q5 시험 전용).
_GRAM_TEST_CHECKS = (['P_tech', 'GA_exists', 'GB_exists', 'GA_args', 'GB_args']
                     + [f'{s}_{c}' for s in ('GA', 'GB') for c in ('tech', 'markers', 'atom_dump_steps', 'wall_dump_steps', 'mesh_z', 'restart_state',
                                                                  'contact_geo')])
#: Q3 — 승인된 문법 판독기 파일 (이력 시험 kit 사본에 있는 이름) — 시험이 따로 적는다 (구현 상수를 베끼지 않는다).
_GRAM_TEST_READER_FILES = ('read_history.py', 'history_params.json')


def _hist_reader():
    """이력 시험 읽는 쪽 (history_test/read_history.py) 모듈 — 합성 문법 런을 그 자신의 합성기 (synth_gram_run) 로 만든다 (시험 전용 · Q3)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location('ul_test_read_history', os.path.join(HERE, 'history_test', 'read_history.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _mk_gram(base, lmp_sha, files, mut=None):
    """합성 문법 fixture 런 (run_history.sh --grammar-only 가 쓰는 꼴: <WORK_ROOT>/gram_<시각>/ (P · GA · GB 단계 폴더 — rc · deck.txt · 덱 사본 ·
    판 STL 사본 · run_manifest.txt · grammar_verdict.json) + <WORK_ROOT>/kit_<시각>/SHA256SUMS) — Q5 시험 전용.
    files = {덱 둘 · 판 STL 이름: 글자} · mut = 반례 하나 → 판정 JSON 경로.
    Q3 (1저자 10-15 · Codex 수정 재확인 Q4): 단계 원자료 = 승인된 판독기 (history_test/read_history.py) 자신의 합성기 synth_gram_run (그 판독기가 PASS 로
    읽는 꼴) · kit 사본 = 그 판독기 · 표 (read_history.py · history_params.json) 바이트 그대로 + kit SHA256SUMS 에 그 sha256 · 판정 JSON 의 검사 19 = 손으로 (전부 참).
    원자료 반례 (판정 JSON 그대로 — Codex raw_*_cached_pass): raw_ga_error (GA 화면 ERROR 덧붙임) · raw_gb_mesh (GB 첫 판 mesh z 99) · raw_gb_screen (GB 화면 지움) ·
    raw_gb_state (GB 마지막 상태 파일 값) · 판독기 반례: kit_reader (kit 사본 판독기 고침 + kit SHA256SUMS · run_manifest sums_sha256 를 맞춤 — Codex
    different_reader_runner_seal) · kit_params (표 고침 · 같이 맞춤) · kit_reader_missing (kit 사본 판독기 없음) · kit_sums_reader (kit 사본 판독기 = 봉인 바이트
    그대로 · 그 런 kit SHA256SUMS 의 판독기 줄만 다른 값 · sums_sha256 맞춤 — ULPR-02)."""
    work = os.path.join(base, 'work')
    run, kit = os.path.join(work, 'gram_20261014_000000'), os.path.join(work, 'kit_20261014_000000')
    os.makedirs(run, exist_ok=True)
    os.makedirs(kit, exist_ok=True)
    rh = _hist_reader()
    Ph = rh.load_params()
    rh.synth_gram_run(run, Ph)   # 단계 P · GA · GB 원자료 (rc · np.txt · screen.out · 덤프 · 판 mesh · restart · 상태 파일 · ckpt.txt · vars.txt)
    for n in _GRAM_TEST_READER_FILES:   # kit 사본 = 판독기 · 표 바이트 그대로 (run_history.sh 의 kit 복사 꼴)
        shutil.copyfile(os.path.join(HERE, 'history_test', n), os.path.join(kit, n))
    if mut == 'kit_reader':
        with open(os.path.join(kit, 'read_history.py'), 'a', encoding='utf-8', newline='\n') as f:
            f.write('\n# 승인 밖 판독기 (봉인 값과 다른 바이트)\n')
    if mut == 'kit_params':
        with open(os.path.join(kit, 'history_params.json'), 'a', encoding='utf-8', newline='\n') as f:
            f.write('\n')
    sums = {n: ul_lib.sha256_bytes(t.encode()) for n, t in files.items()}
    if mut == 'kit_deck':
        sums['in.hist_grammar.liggghts'] = '0' * 64
    sums.update({n: ul_lib.sha256_file(os.path.join(kit, n)) for n in _GRAM_TEST_READER_FILES})
    if mut == 'kit_sums_reader':   # ULPR-02 — kit 사본 판독기 = 봉인 바이트 그대로 · 그 런 kit SHA256SUMS 의 판독기 줄만 다른 값 (sums_sha256 은 아래에서 맞춘다)
        sums['read_history.py'] = 'f' * 64
    if mut == 'kit_reader_missing':
        os.remove(os.path.join(kit, 'read_history.py'))
    _w(os.path.join(kit, 'SHA256SUMS'), ''.join(f'{h}  {n}\n' for n, h in sums.items()) + f'{"1" * 64}  run_history.sh\n')
    E = rh.grammar_expect(Ph)
    if mut == 'raw_ga_error':
        with open(os.path.join(run, 'GA', 'screen.out'), 'a', encoding='utf-8', newline='\n') as f:
            f.write('ERROR: injected raw error after the PASS verdict\n')
    if mut == 'raw_gb_mesh':
        _w(os.path.join(run, 'GB', 'probe', f'mesh_{E["GB"]["start"]}.stl'), 'solid changed\n vertex 0 0 99\nendsolid\n')
    if mut == 'raw_gb_screen':
        os.remove(os.path.join(run, 'GB', 'screen.out'))
    if mut == 'raw_gb_state':
        _w(os.path.join(run, 'GB', 'restart', f'state_g_{E["GB"]["ends"][-1]}.in'), 'variable gr_rstep equal 0\nvariable gr_k equal 0\nvariable gr_pz equal 0\n')
    for st, deck in (('P', 'in.hist_producer.liggghts'), ('GA', 'in.hist_grammar.liggghts'), ('GB', 'in.hist_grammar.liggghts')):
        sd = os.path.join(run, st)
        _w(os.path.join(sd, 'rc'), '1\n' if (mut == 'stage_rc' and st == 'GA') else '0\n')
        _w(os.path.join(sd, 'deck.txt'), ('in.hist_producer.liggghts' if (mut == 'deck_txt' and st == 'GA') else deck) + '\n')
        _w(os.path.join(sd, deck), files[deck] + ('# 고침\n' if (mut == 'deck_copy' and st == 'GB') else ''))
        _w(os.path.join(sd, 'plate_hist.stl'), files['plate_hist.stl'] + ('x\n' if (mut == 'stl_copy' and st == 'P') else ''))
    man = (f'kit={kit}\nrepo_head=x\nrepo_dirty_here=0\nsums_sha256={ul_lib.sha256_file(os.path.join(kit, "SHA256SUMS"))}\nlmp=/x/lmp_mpi\n'
           f'lmp_sha256={lmp_sha}\nnp=6\nnp_alt=4\nmpirun=mpirun --oversubscribe --bind-to none\nslurm_job=1 slurm_ntasks=6 slurm_nodes=n\n'
           f'mode={"hist" if mut == "mode" else "gram"}\nallow_other_lmp=0\nstart=x\n' + ('' if mut == 'no_end' else 'end=y\n'))
    _w(os.path.join(run, 'run_manifest.txt'), man)
    if mut == 'sums_sha':
        _w(os.path.join(kit, 'SHA256SUMS'), open(os.path.join(kit, 'SHA256SUMS')).read() + f'{"2" * 64}  extra.txt\n')
    if mut == 'no_kit':
        shutil.rmtree(kit)
    if mut == 'no_stage':
        shutil.rmtree(os.path.join(run, 'GB'))
    checks = {k: True for k in _GRAM_TEST_CHECKS}
    if mut == 'check_false':
        checks['GB_tech'] = False
    if mut == 'check_missing':
        del checks['GB_args']
    v = {'schema': 'ps45_unload_history_verdict_v1' if mut == 'schema' else 'ps45_unload_grammar_verdict_v1',
         'run_dir': os.path.join(base, 'elsewhere') if mut == 'run_dir' else run, 'status': 'FAIL' if mut == 'status_fail' else 'PASS',
         'checks': checks, 'problems': [], 'exit_code': {'status_fail': 2, 'rc_str': '0', 'rc_bool': False}.get(mut, 0)}
    vp = os.path.join(run, 'grammar_verdict.json')
    if mut == 'bad_json':
        _w(vp, '{ 이것은 JSON 이 아니다')
    elif mut != 'absent':
        _w(vp, json.dumps(v, ensure_ascii=False))
    return vp


def selftest() -> int:
    import tempfile
    fails = []

    def chk(name, cond, detail=''):
        try:
            ok = bool(cond() if callable(cond) else cond)
        except Exception as e:  # noqa: BLE001 — 빈 구현 · 예외도 실패
            ok, detail = False, f'{type(e).__name__}: {e}'
        print(('  ✓ ' if ok else '  ✗ ') + name + ('' if ok else f'  — {detail}'))
        if not ok:
            fails.append(name)

    P = ul_lib.load_params()
    import make_unload_decks as mk  # noqa: E402 — 생성된 덱에서 물리 창을 다시 읽는다 (ULR1-04)
    decks = {k: mk.render(B73, k, P) for k in ('U_UB', 'UT', 'U_UVa', 'U_UVb', 'U_UT3')}
    h0um = P['beds'][B73]['h0'] * 1000.0
    with tempfile.TemporaryDirectory() as root:
        # ── ULR1-02 측정 뒤 TIMEOUT (Codex state.json post_measurement_timeout) ──
        sp = {'W': 5000, 'dt': 1e-6, 'deck': decks['U_UB'],
              'steps': _ladder([0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4]),
              'events': [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')], 'summary': None}
        _mk_arm(root, B73, 'UB', sp, P)
        v = None
        try:
            v = arm_verdict(os.path.join(root, B73, 'UB'), B73, 'UB', P, root=root)
        except Exception:  # noqa: BLE001
            v = None
        chk('R1 ULR1-02 측정 뒤 TIMEOUT — 사다리 0.2 · 0.25 · 0.3 · 0.35 µm / 1.2 · 0.8 · 0.6 · 0.4 MPa · +2 확인 끝 · 분리 전 시간 끝 → '
            'primary OK · ρ = 0.2026077873428664 % · 실제 괄호 [0.2, 0.25] µm · trajectory TIMEOUT (옛 "ρ > 0.315 %" 하한 아님)',
            lambda: v['primary_status'] == 'OK' and abs(v['rho_pct'] - 0.2026077873428664) < 1e-12
            and abs(v['bracket_um'][0] - 0.2) < 1e-12 and abs(v['bracket_um'][1] - 0.25) < 1e-12 and v['trajectory_status'] == 'TIMEOUT')
        sp2 = dict(sp, steps=_ladder([0.2, 0.25, 0.3], [1.9, 1.6, 1.3]), events=[])
        _mk_arm(root, B73, 'UT', sp2, P)
        chk('R1 ULR1-02 교차 전 TIMEOUT · 마지막 정상 단까지 정상 · 접촉 · 단조 → LOWER_BOUND (ρ > ρ(0.3 µm)) · 점 추정 없음',
            lambda: (lambda u: u['primary_status'] == 'LOWER_BOUND' and u['rho_pct'] is None
                     and abs(u['lower_bound_pct'] - 100 * 0.3 / h0um) < 1e-12)(arm_verdict(os.path.join(root, B73, 'UT'), B73, 'UT', P, root=root)))
        sp3 = dict(sp, steps=_ladder([0.2, 0.25, 0.3], [1.9, 2.1, 1.3]), events=[])
        _mk_arm(root, B73, 'UVa', sp3, P)
        chk('R1 ULR1-02 교차 전 TIMEOUT 인데 비단조 (1.9 → 2.1) → 하한 자동 발행 안 함 = UNIDENTIFIED (사유 기록)',
            lambda: (lambda u: u['primary_status'] == 'UNIDENTIFIED' and u['lower_bound_pct'] is None and u['why'])(
                arm_verdict(os.path.join(root, B73, 'UVa'), B73, 'UVa', P, root=root)))
    with tempfile.TemporaryDirectory() as root:
        # ── ULR1-01 끝점 유효성 → 선택 → 다음 제출 (종단) ──
        def arm(job, lifts, Ps, **kw):
            sp = {'W': 5000 if job in ('UB', 'UVa') else 10000, 'dt': 1e-6 if job in ('UB', 'UVa') else 5e-7,
                  'steps': _ladder(lifts, Ps), 'events': [('CROSS', 1, 'first'), ('RM', 3, 'ncross2')], 'summary': 'DONE'}
            sp.update(kw)
            return _mk_arm(root, B73, job, sp, P)

        def rho_lifts(r):   # 교차를 원하는 ρ 로 놓는 사다리 (P 1.2 → 0.8 · 보간 = 두 단 가운데)
            mid = r / 100.0 * h0um
            return [mid - 0.025, mid + 0.025, mid + 0.075, mid + 0.125]

        Ps4 = [1.2, 0.8, 0.6, 0.4]
        cases = [('t1', 1.0, 1.04, 1.03, 'UB'), ('t2', 1.0, 1.04, 1.2, 'UVa'), ('t3', 1.0, 1.2, 1.22, 'UT3'), ('t4', 1.0, 1.2, 1.4, 'UVb')]
        for tup, rub, rut, ruv, want in cases:
            for j in ('UB', 'UT', 'UVa', 'UVb'):
                shutil.rmtree(os.path.join(root, B73, j), ignore_errors=True)
            arm('UB', rho_lifts(rub), Ps4)
            arm('UT', rho_lifts(rut), Ps4)
            s1 = None
            try:
                s1 = selection(arm_verdict(os.path.join(root, B73, 'UB'), B73, 'UB', P, root=root),
                               arm_verdict(os.path.join(root, B73, 'UT'), B73, 'UT', P, root=root), None, P)
            except Exception:  # noqa: BLE001
                s1 = None
            uvjob = 'UVa' if abs(rut - rub) <= 0.1 else 'UVb'
            base = rub if uvjob == 'UVa' else rut
            arm(uvjob, rho_lifts(ruv), Ps4, W=5000 if uvjob == 'UVa' else 10000, dt=1e-6 if uvjob == 'UVa' else 5e-7)
            s2 = None
            try:
                s2 = selection(arm_verdict(os.path.join(root, B73, 'UB'), B73, 'UB', P, root=root),
                               arm_verdict(os.path.join(root, B73, 'UT'), B73, 'UT', P, root=root),
                               arm_verdict(os.path.join(root, B73, uvjob), B73, uvjob, P, root=root), P)
            except Exception:  # noqa: BLE001
                s2 = None
            chk(f'R2 ULR1-01 결정표 {tup}: ρ_UB {rub} · ρ_UT {rut} → δ_dt {abs(rut - rub):.2f} → 다음 = {uvjob} (UB · UT 끝 뒤에만) · '
                f'ρ_UV {ruv} (기준 {base}) → 튜플 {tup} · 7:3 최종 팔 {want}',
                lambda s1=s1, s2=s2, uvjob=uvjob, tup=tup: s1['stage'] == 'need_UV' and s1['next'] == [uvjob]
                and s2['stage'] == 'resolved' and s2['tuple'] == tup)
        for j in ('UB', 'UT', 'UVa', 'UVb'):
            shutil.rmtree(os.path.join(root, B73, j), ignore_errors=True)
        arm('UB', rho_lifts(1.0), Ps4)
        arm('UT', rho_lifts(1.1), Ps4)
        arm('UVa', rho_lifts(1.1), Ps4)
        chk('R2 ULR1-01 경계 δ = 0.10 정확히 (ρ 1.0 ↔ 1.1 · 부동소수 0.10000000000000009) = ≤ 쪽 → dt* = dt₀ · δ_v 0.10 → t1 (UB)',
            lambda: selection(arm_verdict(os.path.join(root, B73, 'UB'), B73, 'UB', P, root=root),
                              arm_verdict(os.path.join(root, B73, 'UT'), B73, 'UT', P, root=root),
                              arm_verdict(os.path.join(root, B73, 'UVa'), B73, 'UVa', P, root=root), P)['tuple'] == 't1')
        # 무효 끝점 셋 — UT UNSTEADY · UT NaN · UV 무교차
        shutil.rmtree(os.path.join(root, B73, 'UT'), ignore_errors=True)
        arm('UT', rho_lifts(1.04), Ps4, steps=_ladder(rho_lifts(1.04), Ps4, steady=False))
        chk('R3 ULR1-01 UT 끝점 UNSTEADY → δ_dt 없음 → SELECTION_UNRESOLVED · 다음 제출 없음 (UV 안 냄)',
            lambda: (lambda s: s['stage'] == 'SELECTION_UNRESOLVED' and s['next'] == [] and s['tuple'] is None)(
                selection(arm_verdict(os.path.join(root, B73, 'UB'), B73, 'UB', P, root=root),
                          arm_verdict(os.path.join(root, B73, 'UT'), B73, 'UT', P, root=root), None, P)))
        shutil.rmtree(os.path.join(root, B73, 'UT'), ignore_errors=True)
        nan_steps = _ladder(rho_lifts(1.04), Ps4)
        nan_steps[2]['Pbar'] = 'nan'
        arm('UT', rho_lifts(1.04), Ps4, steps=nan_steps)
        chk('R3 ULR1-01 UT 끝점 P̄ = NaN (CSV "nan") → else 로 흘리지 않는다 → SELECTION_UNRESOLVED',
            lambda: selection(arm_verdict(os.path.join(root, B73, 'UB'), B73, 'UB', P, root=root),
                              arm_verdict(os.path.join(root, B73, 'UT'), B73, 'UT', P, root=root), None, P)['stage'] == 'SELECTION_UNRESOLVED')
        shutil.rmtree(os.path.join(root, B73, 'UT'), ignore_errors=True)
        arm('UT', rho_lifts(1.04), Ps4)
        shutil.rmtree(os.path.join(root, B73, 'UVa'), ignore_errors=True)
        arm('UVa', [0.2, 0.25, 0.3, 0.35], [1.9, 1.8, 1.7, 1.6], events=[], summary='LIFT_CAP')
        chk('R3 ULR1-01 UV 무교차 (상한) → δ_v 없음 → SELECTION_UNRESOLVED (최종 튜플 없음 · 나머지 네 침대 U 없음)',
            lambda: (lambda s: s['stage'] == 'SELECTION_UNRESOLVED' and s['tuple'] is None)(
                selection(arm_verdict(os.path.join(root, B73, 'UB'), B73, 'UB', P, root=root),
                          arm_verdict(os.path.join(root, B73, 'UT'), B73, 'UT', P, root=root),
                          arm_verdict(os.path.join(root, B73, 'UVa'), B73, 'UVa', P, root=root), P)))
        chk('R3 NO_BRACKET 이름은 개발 팔 판정에 쓰지 않는다 (§13-1 — 중력 팔 전용)',
            lambda: 'NO_BRACKET' not in json.dumps(arm_verdict(os.path.join(root, B73, 'UVa'), B73, 'UVa', P, root=root)))
        # ── S3 · NOISE_FLOOR 가 끝점을 무효로 ──
        shutil.rmtree(os.path.join(root, B73, 'UT'), ignore_errors=True)
        st = _ladder(rho_lifts(1.04), Ps4)
        st[2]['s3'] = 'bad'
        arm('UT', rho_lifts(1.04), Ps4, steps=st)
        chk('R4 교차 끝점 S3 FAIL (총힘 잔차 > 1e-3) → 끝점 무효 → primary UNIDENTIFIED (S3 사유) · 선택 UNRESOLVED',
            lambda: (lambda u: u['primary_status'] == 'UNIDENTIFIED' and 'S3' in ' '.join(u['why']))(
                arm_verdict(os.path.join(root, B73, 'UT'), B73, 'UT', P, root=root)))
        shutil.rmtree(os.path.join(root, B73, 'UT'), ignore_errors=True)
        st = _ladder(rho_lifts(1.04), Ps4)
        st[2]['sigma'] = 0.5
        arm('UT', rho_lifts(1.04), Ps4, steps=st)
        chk('R4 k* 의 마지막 두 창 thermo σ_P 0.5 MPa (> P_meas / 3) → NOISE_FLOOR (주 값 아님 · 선택 UNRESOLVED)',
            lambda: (lambda u: u['primary_status'] == 'NOISE_FLOOR' and u['sigma_P'] > 0.4)(
                arm_verdict(os.path.join(root, B73, 'UT'), B73, 'UT', P, root=root)))
        # ── ULR1-05 결정표 3 행 → UTc 후속 산출물 · 다음 제출 관문 ──
        for j in ('UB', 'UT', 'UVa', 'UVb'):
            shutil.rmtree(os.path.join(root, B73, j), ignore_errors=True)
        _fake_restored(root, B73)
        _w(os.path.join(root, B73, 'ul_base.in'), 'variable ul_S2max equal 1e-05\n')
        arm('UB', rho_lifts(1.0), Ps4)
        chk('R5 관문: UB · UT 판독 전 UVa · UVb 거부 (동시 UV 제출 없음 · §13-5 ②)', lambda: not gate(root, B73, 'UVa', P)[0] and not gate(root, B73, 'UVb', P)[0])
        arm('UT', rho_lifts(1.2), Ps4)
        chk('R5 관문: δ_dt 0.2 → dt* = dt₀/2 → UVb 만 허용 · UVa 거부', lambda: gate(root, B73, 'UVb', P)[0] and not gate(root, B73, 'UVa', P)[0])
        arm('UVb', rho_lifts(1.22), Ps4, W=10000, dt=5e-7)
        chk('R5 ULR1-05 결정표 3 행 (UT 채택) → UTc (UT 의 R_M 에서 이어 돌림) 허용 · UT3 를 S0 에서 새로 (7:3) 거부 · G_UT3 허용 (R_M = UT)',
            lambda: gate(root, B73, 'UTc', P)[0] and not gate(root, B73, 'UT3', P)[0] and gate(root, B73, 'G_UT3', P)[0])
        chk('R5 다른 침대: 복원 전 거부 · 복원 뒤에는 최종 튜플의 팔 (UT3) 만 허용 · UB · UVa 거부',
            lambda: (not gate(root, 'ps_3_7_r45', 'UT3', P)[0]) and (_fake_restored(root, 'ps_3_7_r45') or True)
            and (_w(os.path.join(root, 'ps_3_7_r45', 'ul_base.in'), 'x\n') or True)
            and gate(root, 'ps_3_7_r45', 'UT3', P)[0] and not gate(root, 'ps_3_7_r45', 'UB', P)[0] and not gate(root, 'ps_3_7_r45', 'UVa', P)[0])
        chk('R5 10:0: 이완 연장 결정 (S0′) 전 RJ2 · U 거부', lambda: not gate(root, B100, 'RJ2', P)[0] and not gate(root, B100, 'UT3', P)[0])
    with tempfile.TemporaryDirectory() as root:
        # ── ULKR-01 확인 두 단 = 실제로 이어지는 B 확인 단의 등록 정상 완료 (Q1 — 판 접촉은 요구하지 않음 · Codex reader_adversarial confirmation_*) ──
        _fake_restored(root, B73)
        _w(os.path.join(root, B73, 'ul_base.in'), 'variable ul_S2max equal 1e-05\n')
        base_l, base_p = [0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4]

        def put(job, steps, W=5000, dt=1e-6, events=(('CROSS', 2, 'first'), ('RM', 4, 'ncross2')), summary=None, bed=B73):
            shutil.rmtree(os.path.join(root, bed, job), ignore_errors=True)
            return _mk_arm(root, bed, job, {'W': W, 'dt': dt, 'steps': steps, 'events': list(events), 'summary': summary}, P)

        def av(job, bed=B73):
            return arm_verdict(os.path.join(root, bed, job), bed, job, P, root=root)

        def conf(fn, lifts=base_l, Ps=base_p, which=(3, 4)):
            st = _ladder(lifts, Ps)
            for x in which:
                fn(st[x])
            return st

        def near(a, b):
            return a is not None and len(a) == len(b) and all(abs(x - y) < 1e-12 for x, y in zip(a, b))

        def ut_invalid(why_part):
            u = av('UT')
            return (u['primary_status'] == 'UNIDENTIFIED' and u['rho_pct'] is None and any(why_part in w for w in u['why'])
                    and selection_state(root, P)['stage'] == 'SELECTION_UNRESOLVED' and not gate(root, B73, 'UVa', P)[0]
                    and not gate(root, B73, 'UVb', P)[0])
        put('UB', _ladder(base_l, base_p), summary='DONE')
        put('UT', _ladder(base_l, base_p), W=10000, dt=5e-7, summary='RM_STOP')
        chk('R20 대조: UB · UT 정상 (교차 k 2 · 확인 k 3 · 4 정상) → UT OK · δ_dt 0 → UVa 허용', lambda: av('UT')['primary_status'] == 'OK' and gate(root, B73, 'UVa', P)[0])
        put('UT', conf(lambda s: s.update(steady=False, nw=12, s3='bad')), W=10000, dt=5e-7, summary='RM_STOP')
        chk('R20 ULKR-01 확인 두 단 UNSTEADY (12 창 소진 · steady 0) · S3 FAIL (Codex confirmation_invalid) → UT UNIDENTIFIED · SELECTION_UNRESOLVED · UVa · UVb 거부',
            lambda: ut_invalid('확인 단'))
        put('UT', conf(lambda s: s.update(Pbar='nan')), W=10000, dt=5e-7, summary='RM_STOP')
        chk('R20 ULKR-01 확인 두 단 P̄ = NaN 만 (교차 양 끝은 유효 · Codex confirmation_nan) → UNIDENTIFIED · 제출 거부', lambda: ut_invalid('확인 단'))
        put('UT', conf(lambda s: s.update(steady=False, nw=12), which=(4,)), W=10000, dt=5e-7, summary='RM_STOP')
        chk('R20 ULKR-01 둘째 확인 단만 UNSTEADY → UNIDENTIFIED · 제출 거부', lambda: ut_invalid('UNSTEADY'))
        put('UT', conf(lambda s: s.update(s3='bad'), which=(3,)), W=10000, dt=5e-7, summary='RM_STOP')
        chk('R20 ULKR-01 첫 확인 단 S3 FAIL 만 (정상 · 유한) → UNIDENTIFIED · 제출 거부', lambda: ut_invalid('S3'))
        put('UT', conf(lambda s: s.update(kind='A'), which=(3,)), W=10000, dt=5e-7, summary='RM_STOP')
        chk('R20 ULKR-01 확인 단이 B 단이 아님 (A) → UNIDENTIFIED (등록 확인 = B 두 단)', lambda: ut_invalid('B 단'))
        d_ut = put('UT', _ladder(base_l, base_p), W=10000, dt=5e-7, summary='RM_STOP')
        sp = os.path.join(d_ut, 'ul_steps.csv')
        _w(sp, '\n'.join(ln for ln in open(sp).read().splitlines() if ln.split(',')[2] != '3') + '\n')
        chk('R20 ULKR-01 첫 확인 단 기록 (k 3) 누락 — 남은 단이 k 2 → 4 로 건너뜀 → UNIDENTIFIED (누락 · 순서) · 제출 거부', lambda: ut_invalid('불연속'))
        put('UT', conf(lambda s: s.update(P=0.0, wall=[[]] * 4), Ps=[1.2, 0.8, 0.0, 0.0]), W=10000, dt=5e-7, summary='RM_STOP')
        chk('R20 Q1 확인 두 단에서 판이 떨어짐 (벽 접촉 0 · 정상 · S3 PASS · 유한) → 주 값 OK 그대로 (판 접촉은 확인 단 조건이 아니다)',
            lambda: (lambda u: u['primary_status'] == 'OK' and abs(u['rho_pct'] - 0.2026077873428664) < 1e-12)(av('UT')))
        # ── ULKR-02 k = 0 → 1 교차를 합집합에 넣는다 (Codex first_step_cross · first_step_rebound) ──
        put('UB', _ladder([0.2, 0.25, 0.3], [0.8, 0.6, 0.4]), summary='DONE')
        stA = _ladder([0.2, 0.25, 0.3], [0.8, 0.6, 0.4])
        stA[1]['kind'] = 'A'
        put('UB', stA, summary='DONE')
        chk('R21 ULKR-02 첫 A 단 (k 0 → 1) 교차 · 반등 없음 → ρ 0.1798695599526285 · 괄호 [0, 0.2] µm · 합집합 = 그 괄호 (옛 코드 = null)',
            lambda: (lambda u: u['primary_status'] == 'OK' and abs(u['rho_pct'] - 0.1798695599526285) < 1e-12 and near(u['bracket_um'], [0.0, 0.2])
                     and near(u['union_bracket_um'], [0.0, 0.2]))(av('UB')))
        stR = _ladder([0.2, 0.25, 0.3, 0.35, 0.4], [0.8, 0.6, 0.4, 1.2, 0.7])
        stR[1]['kind'] = 'A'
        put('UB', stR, summary='DONE')
        put('UB', _ladder([0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4]), summary='DONE', bed='ps_0_10_r45')
        chk('R21 ULKR-02 첫 A 단 교차 + 뒤 반등 (1.2 → 0.7) → 합집합 외곽 [0, 0.4] µm (옛 [0.3, 0.4]) · 0:10 괄호 [0.2, 0.25] µm 와 10 쌍 = OVERLAP (옛 SEPARATED)',
            lambda: (lambda u, o: near(u['union_bracket_um'], [0.0, 0.4]) and u['nonmonotone'] is True and near(o['union_bracket_um'], [0.2, 0.25])
                     and {(r['a'], r['b']): r['relation'] for r in pair_table({'ps_0_10_r45': o, 'ps_7_3_r45': u})}[('ps_0_10_r45', 'ps_7_3_r45')] == 'OVERLAP')(
                av('UB'), av('UB', 'ps_0_10_r45')))
        stN = _ladder([0.2, 0.25, 0.3, 0.35, 0.4], [1.2, 0.8, 0.6, 0.4, 0.3])
        stN[5]['Pbar'] = 'nan'
        put('UB', stN, summary='DONE')
        chk('R21 ULKR-02 확인 뒤 단 하나 P̄ 비유한 → 주 값 OK 그대로 · 합집합 미계산 (null · 사유 — 10 쌍 표 미식별)',
            lambda: (lambda u: u['primary_status'] == 'OK' and u['union_bracket_um'] is None and any('합집합' in w for w in u['why']))(av('UB')))
        put('UB', _ladder(base_l, base_p), summary='DONE')
        chk('R21 ULKR-02 불변식: 보고 합집합 ⊇ 첫 교차 괄호 (B 단 교차 · 반등 없음 = 같음)',
            lambda: (lambda u: u['union_bracket_um'][0] <= u['bracket_um'][0] and u['bracket_um'][1] <= u['union_bracket_um'][1])(av('UB')))
        # ── ULKR-04 파서가 버린 행 · 다른 시점 프레임을 정상 관측으로 쓰지 않는다 (Codex observer_adversarial) ──
        for mut, what, why_part in (('atom_nan', '교차 끝점 원자 덤프 한 행 fz = nan (파서가 그 행을 버림 — 옛 코드는 남은 4 원자로 S3 PASS)', 'S3'),
                                    ('wall_past', '교차 끝점 마지막 창 벽 덤프 머리 step = 요청 − 100,000', '판 접촉'),
                                    ('dumps_past', '교차 끝점 원자 · 쌍 덤프 머리 둘 다 100,000 과거 (서로는 같음)', 'S3'),
                                    ('csv_bad', 'k 1 단 기록 줄 열 수 틀림 (CSV 가 그 줄을 버림 — 옛 코드는 k 0 → 2 를 교차로 씀)', 'CSV')):
            st = _ladder(base_l, base_p)
            st[2 if mut != 'csv_bad' else 1]['mut'] = mut
            put('UB', st, summary='DONE')
            chk(f'R22 ULKR-04 {what} → UB UNIDENTIFIED (사유) · 선택 UNRESOLVED',
                lambda why_part=why_part: (lambda u: u['primary_status'] == 'UNIDENTIFIED' and u['rho_pct'] is None and any(why_part in w for w in u['why']))(av('UB'))
                and selection_state(root, P)['stage'] == 'SELECTION_UNRESOLVED')
        st = _ladder(base_l, base_p)
        st[2]['mut'] = 'atom_unbalanced'
        put('UB', st, summary='DONE')
        chk('R22 대조: 같은 원자 fz = 1e-3 N (유한 · 불평형) → S3 FAIL → UNIDENTIFIED (nan 행을 버리면 이 실패가 PASS 로 바뀌던 것)',
            lambda: (lambda u: u['primary_status'] == 'UNIDENTIFIED' and any('S3 FAIL' in w for w in u['why']))(av('UB')))
    with tempfile.TemporaryDirectory() as root:
        # ── ULKR-03 UT → UTc 이어 돌림 — UTc 가 해시로 묶인 UT 부모 관측을 읽는다 · 최종 report = UT 주 값 + UTc 보조 관측 (Codex reader_continuation) ──
        _fake_restored(root, B73)
        _w(os.path.join(root, B73, 'ul_base.in'), 'variable ul_S2max equal 1e-05\n')
        Ps4 = [1.2, 0.8, 0.6, 0.4]
        ev = [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')]
        _mk_arm(root, B73, 'UB', {'W': 5000, 'dt': 1e-6, 'steps': _ladder([0.2, 0.25, 0.3, 0.35], Ps4), 'events': ev, 'summary': 'DONE'}, P)
        ut_spec = {'W': 10000, 'dt': 5e-7, 'steps': _ladder([0.4, 0.45, 0.5, 0.55], Ps4), 'events': ev + [('RM_STOP', 4, 'UT')], 'summary': 'RM_STOP'}
        _mk_arm(root, B73, 'UT', ut_spec, P)
        _mk_arm(root, B73, 'UVb', dict(ut_spec, events=ev, summary='DONE'), P)
        cont = [{'lift_um': 0.6, 'P': 0.0, 'steady': True, 'nw': 5, 'kind': 'B', 'phase': 2, 'modeB': 1, 'n_move': 0, 'wall': [[]] * 5, 'surface': [120.0] * 5}]
        cev = [('SEPARATED', 5, 'w2'), ('POST_DONE', 5, 'w5')]
        rho_ut = 0.3827035983143033

        def utc(layout='hash', edit=None):
            try:
                shutil.rmtree(os.path.join(root, B73, 'UTc'), ignore_errors=True)
                _mk_utc(root, B73, ut_spec, cont, P, events=cev, layout=layout)
                if edit:
                    edit()
                return report(root, P)['beds'][B73] or {}, _arm_v(root, B73, 'UTc', P) or {}
            except Exception as ex:  # noqa: BLE001 — 빈 구현 (시험 먼저) · 예외도 실패
                return {'error': repr(ex)}, {'error': repr(ex)}
        chk('R23 대조: UB ρ 0.2026 · UT ρ 0.3827 (R_M 에서 멈춤 · RM_STOP) · UVb = UT → 선택 t3 (UT3 = UT + UTc)',
            lambda: (lambda s: s['stage'] == 'resolved' and s['tuple'] == 't3')(selection_state(root, P)))
        e, u = utc()
        chk('R23 ULKR-03 UTc = 해시로 묶인 UT 부모 관측 (복사 없음) + 이어 돌림 → UTc 판독 주 값 = UT 주 값 (OK · ρ 0.3827035983143033) · 이어 돌림 OK',
            lambda: u['primary_status'] == 'OK' and abs(u['rho_pct'] - rho_ut) < 1e-12 and (u.get('continuation') or {}).get('status') == 'OK')
        chk('R23 ULKR-03 최종 report (t3) = UT 주 값 (OK · ρ 0.3827) + UTc 보조 관측 (분리 · 분리 뒤 4 창 · trajectory DONE · 출처 UTc)',
            lambda: e['primary_status'] == 'OK' and abs(e['rho_pct'] - rho_ut) < 1e-12 and e.get('job') == 'UT+UTc' and e.get('aux_source') == 'UTc'
            and e['trajectory_status'] == 'DONE' and e['separation']['separated_final'] is True and e['separation']['n_post'] == 4)
        e, u = utc(edit=lambda: open(os.path.join(root, B73, 'UT', 'screen.txt'), 'a').write('# UTc 시작 뒤 부모 파일이 바뀜\n'))
        chk('R23 ULKR-03 UTc 시작 뒤 UT 부모 파일 (screen.txt) 이 바뀜 (sha256 ≠ 목록) → UTc 이어 돌림 무효 · UTc 주 값 UNIDENTIFIED · report = UT 주 값 그대로 · 보조 SEP_INCOMPLETE',
            lambda: (u.get('continuation') or {}).get('status') == 'FAIL' and u['primary_status'] == 'UNIDENTIFIED'
            and e['primary_status'] == 'OK' and abs(e['rho_pct'] - rho_ut) < 1e-12 and e['trajectory_status'] == 'SEP_INCOMPLETE' and e.get('aux_source') is None)
        shutil.rmtree(os.path.join(root, B73, 'UT'))
        _mk_arm(root, B73, 'UT', ut_spec, P)
        e, u = utc('copy')
        chk('R23 ULKR-03 옛 러너 꼴 (UT 기록 CSV 를 UTc 에 복사) → 경계 중복 (R_M step 이하 UTc 기록) → 이어 돌림 무효 · report = UT 주 값 + 보조 SEP_INCOMPLETE',
            lambda: (u.get('continuation') or {}).get('status') == 'FAIL' and any('중복' in p for p in u['continuation']['problems'])
            and e['primary_status'] == 'OK' and e['trajectory_status'] == 'SEP_INCOMPLETE')
        e, u = utc('gap')
        chk('R23 ULKR-03 경계 누락 (UTc 첫 단 k = k_RM + 2) → 이어 돌림 무효 · report = UT 주 값 + 보조 SEP_INCOMPLETE',
            lambda: (u.get('continuation') or {}).get('status') == 'FAIL' and any('누락' in p for p in u['continuation']['problems'])
            and e['primary_status'] == 'OK' and e['trajectory_status'] == 'SEP_INCOMPLETE')
        mp = os.path.join(root, B73, 'UTc', 'run_manifest.txt')
        e, u = utc(edit=lambda: _w(mp, open(mp).read().replace('rm_step=', 'rm_step=1')))
        chk('R23 ULKR-03 run_manifest 의 rm_step ≠ 부모 RM 사건 step → 이어 돌림 무효 (부모 기록 끝 ≠ R_M)',
            lambda: (u.get('continuation') or {}).get('status') == 'FAIL' and e['primary_status'] == 'OK' and e['trajectory_status'] == 'SEP_INCOMPLETE')
        shutil.rmtree(os.path.join(root, B73, 'UTc'), ignore_errors=True)
        e = report(root, P)['beds'][B73] or {}
        chk('R23 ULKR-03 UTc 아직 없음 → report = UT 주 값 (OK) · 보조 SEP_INCOMPLETE (UTc 없음)',
            lambda: e['primary_status'] == 'OK' and abs(e['rho_pct'] - rho_ut) < 1e-12 and e['trajectory_status'] == 'SEP_INCOMPLETE')
        chk('R23 ULKR-03 parentsums = 부모 UT 의 판독 대상 파일 sha256 (기록 · 화면 · 덤프 · 상태 · R_M restart) — 단 끝 restart_unload · arm_verdict.json 은 뺀다',
            lambda: (lambda t: 'ul_windows.csv' in t and 'screen.txt' in t and 'dump/' in t and 'arm_verdict.json' not in t)(parent_sums(os.path.join(root, B73, 'UT'))))
    with tempfile.TemporaryDirectory() as root:
        # ── ULKR-07 (Q6 · 개정 3 §14-7) — 판독기가 덱의 분리 · 분리 뒤 창 · 예산과 맞지 않으면 DONE 이 아니다 (주 ρ 무영향 · Codex done_recontact · done_missing) ──
        def sep_arm(walls, nw, summary='DONE', sev=(('SEPARATED', 'w2'), ('POST_DONE', 'w5')), last4=None):
            """분리 단 (k 5 · 단계 2) — walls = 창마다 벽 접촉 · sev = 덱이 쓴 창 사건 (그 창 끝 step) · last4 = k 4 (CONFIRM) 창마다 벽."""
            st = _ladder([0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4])
            if last4 is not None:
                st[4]['wall'] = last4
            st.append({'lift_um': 0.4, 'P': 0.0, 'steady': True, 'nw': nw, 'kind': 'B', 'phase': 2, 'modeB': 1, 'n_move': 0, 'wall': walls})
            shutil.rmtree(os.path.join(root, B73, 'UB'), ignore_errors=True)
            _mk_arm(root, B73, 'UB', {'W': 5000, 'dt': 1e-6, 'steps': st, 'summary': summary,
                                      'events': [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')] + [(n, 5, w) for n, w in sev]}, P)
            return arm_verdict(os.path.join(root, B73, 'UB'), B73, 'UB', P, root=root)

        def ok_primary(u):
            return u['primary_status'] == 'OK' and abs(u['rho_pct'] - 0.2026077873428664) < 1e-12

        def k5_step(w):
            return [int(ln.split(',')[5]) for ln in open(os.path.join(root, B73, 'UB', 'ul_windows.csv')).read().splitlines()[1:]
                    if ln.split(',')[2] == '5' and ln.split(',')[3] == str(w)][0]
        chk('R24 대조: 분리 단 벽 접촉 [0, 0, 0, 0, 0] · 덱 DONE (SEPARATED w2 · POST_DONE w5) → 판독기 분리 (w 2) · 분리 뒤 4 창 → trajectory DONE · 주 값 OK',
            lambda: (lambda u: ok_primary(u) and u['trajectory_status'] == 'DONE' and u['separation']['n_post'] == 4)(sep_arm([[]] * 5, 5)))
        chk('R24 ULKR-07 덱 DONE 인데 판독기 벽 덤프 [0, 0, 0, 0, 1] (마지막 창 재접촉 · Codex done_recontact) → trajectory SEP_INCOMPLETE (DONE 아님) · 주 값 OK 그대로',
            lambda: (lambda u: ok_primary(u) and u['trajectory_status'] == 'SEP_INCOMPLETE')(sep_arm([[], [], [], [], [-1.0]], 5)))
        chk('R24 ULKR-07 덱 DONE 인데 마지막 창 벽 덤프 결손 (Codex done_missing) → SEP_INCOMPLETE · 주 값 OK',
            lambda: (lambda u: ok_primary(u) and u['trajectory_status'] == 'SEP_INCOMPLETE')(sep_arm([[], [], [], [], 'missing'], 5)))
        chk('R24 ULKR-07 판독기 분리 선언 창이 유지 예산 밖 (w 13 > 12 — 11 창 접촉 뒤 0 다섯) · 덱 DONE → SEP_INCOMPLETE · 주 값 OK',
            lambda: (lambda u: ok_primary(u) and u['trajectory_status'] == 'SEP_INCOMPLETE')(
                sep_arm([[-1.0]] * 11 + [[]] * 5, 16, sev=(('SEPARATED', 'w13'), ('POST_DONE', 'w16')))))
        chk('R24 Q6 덱 요약 SEP_INCOMPLETE (재접촉 뒤 예산 끝) → trajectory SEP_INCOMPLETE · 주 값 OK',
            lambda: (lambda u: ok_primary(u) and u['trajectory_status'] == 'SEP_INCOMPLETE')(
                sep_arm([[], [], [-1.0]] + [[-1.0]] * 9, 12, summary='SEP_INCOMPLETE', sev=(('SEPARATED', 'w2'), ('SEP_INCOMPLETE', 'w12')))))
        chk('R24 ULKR-07 덱 SEPARATED 사건 (w 3) ≠ 판독기 선언 창 (w 2) → SEP_INCOMPLETE (덱 ↔ 판독기 불일치 = 보조 미완료) · 주 값 OK',
            lambda: (lambda u: ok_primary(u) and u['trajectory_status'] == 'SEP_INCOMPLETE')(sep_arm([[]] * 5, 5, sev=(('SEPARATED', 'w3'), ('POST_DONE', 'w5')))))
        chk('R24 ULKR-07 덱 DONE 인데 SEPARATED · POST_DONE 사건 없음 → SEP_INCOMPLETE · 주 값 OK',
            lambda: (lambda u: ok_primary(u) and u['trajectory_status'] == 'SEP_INCOMPLETE')(sep_arm([[]] * 5, 5, sev=())))
        chk('R24 ULKR-07 이동 = 연속 초기화 (덱 ul_sepn 0): k 4 마지막 창 0 + k 5 첫 창 0 → 선언은 k 5 w 2 (덱과 같다 · 옛 판독 k 5 w 1) · DONE · 분리 뒤 창 = w 2–5',
            lambda: (lambda u: ok_primary(u) and u['trajectory_status'] == 'DONE' and u['separation']['declared_step'] == k5_step(2)
                     and u['separation']['n_post'] == 4)(sep_arm([[]] * 5, 5, last4=['default', 'default', 'default', []])))
        chk('R24 ULKR-07 separation(): CONFIRM (단계 1) 창의 연속 0 은 선언 아님 (덱 = SEPARATE 단계 2 에서만) · 단계 2 로 넘어가면 그때 선언',
            lambda: separation([{'state': 'ZERO', 'step': s, 'k': 3, 'phase': 1} for s in (1, 2, 3)])['declared_index'] is None
            and separation([{'state': 'ZERO', 'step': s, 'k': 3, 'phase': 1} for s in (1, 2)]
                           + [{'state': 'ZERO', 'step': s, 'k': 4, 'phase': 2} for s in (3, 4)])['declared_step'] == 4)
    with tempfile.TemporaryDirectory() as root:
        # ── ULKR-10 B (Q5 · 개정 3 §14-6) — S3 무게 항 g = 그 팔의 실제 중력 (Codex gravity_floor: m 1e-6 kg · 총힘 9.81e-12 N) ──
        def ff_arm(job):
            st = _ladder([0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4])
            st[2]['mut'] = 'free_fall_aux'
            shutil.rmtree(os.path.join(root, B73, job), ignore_errors=True)
            _mk_arm(root, B73, job, {'W': 5000, 'dt': 1e-6, 'steps': st, 'events': [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')], 'summary': 'DONE'}, P)
            return arm_verdict(os.path.join(root, B73, job), B73, job, P, root=root)
        chk('R26 대조: 일반 팔 (UB · g 9.81) 교차 끝점 무접촉 원자 총힘 = −m g_aux (무게의 1e-6) → S3 PASS · 주 값 OK (ρ 0.2026…)',
            lambda: (lambda u: u['primary_status'] == 'OK' and abs(u['rho_pct'] - 0.2026077873428664) < 1e-12)(ff_arm('UB')))
        chk('R26 ULKR-10 B 중력 팔 (G_UB · g_aux 9.81e-6) 같은 끝점 = 자유 낙하 → S3 FAIL (R = 1 · 기본 g 9.81 이면 R 1e-6 PASS)',
            lambda: any('단 2 S3 FAIL' in w for w in ff_arm('G_UB')['why']))
        chk('R26 ULKR-10 B _arm_g: 일반 팔 · UTc = 표 S3 g 9.81 · 중력 팔 G_UB · G_UVa · G_UVb · G_UT3 = g_aux 9.81e-6',
            lambda: _arm_g('UB', P) == 9.81 and _arm_g('UTc', P) == 9.81 and all(_arm_g(j, P) == P['g_aux'] for j in ('G_UB', 'G_UVa', 'G_UVb', 'G_UT3')))
    with tempfile.TemporaryDirectory() as root:
        # ── ULKR-12 · Q7 (개정 3 §14-8) — ε_sphere (S0 봉인 C_all) · W_proxy (k 0 → M) 를 파일 → 팔 판정 → 최종 보고까지 (Codex observer_production_calls) ──
        _fake_restored(root, B73)
        _w(os.path.join(root, B73, 'ul_base.in'), 'variable ul_S2max equal 1e-05\n')
        lifts, Ps4 = [0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4]
        ev = [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')]

        def put(job, steps, W=5000, dt=1e-6):
            shutil.rmtree(os.path.join(root, B73, job), ignore_errors=True)
            _mk_arm(root, B73, job, {'W': W, 'dt': dt, 'steps': steps, 'full_frames': True, 'events': ev + ([('RM_STOP', 4, 'UT')] if job == 'UT' else []),
                                     'summary': 'RM_STOP' if job == 'UT' else 'DONE'}, P)
            return arm_verdict(os.path.join(root, B73, job), B73, job, P, root=root)
        u = put('UB', _ladder(lifts, Ps4))
        put('UT', _ladder(lifts, Ps4), 10000, 5e-7)
        put('UVa', _ladder(lifts, Ps4))
        h0 = P['beds'][B73]['h0']
        C = 105 * 4.0 / 3.0 * math.pi * 0.0005 ** 3 / 0.0025          # 합성 S0 = 사슬 5 + 표면 100 · 반경 0.0005 · 상자 0.05 × 0.05
        hM = h0 + 0.225 / 1000.0                                       # M = 보간 들어 올림 0.225 µm
        pts = [(h0, 0.16), (h0 + 0.0002, 0.0012), (hM, 0.001)]          # k 0 (P̄ 160) · k* − 1 (1.2) · M (P_meas 1) — 덱 MPa
        W_exp = sum(0.5 * (p0 + p1) * 1e6 * 0.0025 * (h1 - h0_) for (h0_, p0), (h1, p1) in zip(pts, pts[1:])) * 1e-6

        def close(a, b, rel=1e-12):
            return a is not None and b is not None and abs(a - b) <= rel * max(abs(b), 1e-300)
        chk('R27 ULKR-12 팔 판정 ε: C_all = S0 봉인 (Σ V ÷ A) · S0 · 교차 끝점 둘 (k 1 · 2 · 완전 프레임) · M (보간 높이 · ε_all 만) = 1 − C_all / h',
            lambda: u['eps']['status'] == 'OK' and close(u['eps']['C_all_m'], C) and close(u['eps']['S0']['eps_all'], 1 - C / h0)
            and [e['k'] for e in u['eps']['endpoints']] == [1, 2] and all(e['status'] == 'OK' for e in u['eps']['endpoints'])
            and close(u['eps']['endpoints'][0]['eps_all'], 1 - C / (h0 + 0.0002)) and close(u['eps']['endpoints'][1]['eps_all'], 1 - C / (h0 + 0.00025))
            and close(u['eps']['M']['eps_all'], 1 - C / hM) and u['eps']['M']['eps_inside'] is None)
        chk('R27 ULKR-12 팔 판정 W_proxy = k 0 → M 정착 단 사다리꼴 (끝 조각 k* − 1 → M 은 P_meas) × 1e-6 = 4.036875e-8 J 보고 (판이 받은 일 아님)',
            lambda: close(u['w_proxy_J'], W_exp) and close(W_exp, 4.036875e-8, 1e-9) and u['w_proxy']['status'] == 'OK')
        rep = report(root, P)
        e = (rep['beds'] or {}).get(B73) or {}
        chk('R27 ULKR-12 최종 보고 (t1 = UB) 에 같은 ε · W_proxy (파일 → 팔 판정 → report)',
            lambda: rep['selection']['tuple'] == 't1' and e.get('eps') == u['eps'] and e.get('w_proxy_J') == u['w_proxy_J'])
        st = _ladder(lifts, Ps4)
        st[2]['mut'] = 'drop_s0_atom'
        ud = put('UB', st)
        chk('R27 ULKR-12 Codex fixed_volume (판독기) — 교차 끝점 k 2 프레임에서 S0 원자 한 행이 빠짐 → 그 끝점 ε NOT_COMPUTED (C_all 다시 계산해 줄이지 않는다) · '
            'S0 · k 1 · M 그대로 · 주 값 OK',
            lambda: ud['primary_status'] == 'OK' and ud['eps']['endpoints'][1]['status'] == 'NOT_COMPUTED' and ud['eps']['endpoints'][1]['eps_all'] is None
            and close(ud['eps']['C_all_m'], C) and ud['eps']['endpoints'][0]['status'] == 'OK' and close(ud['eps']['M']['eps_all'], 1 - C / hM))
        st = _ladder([0.1] + lifts, [3.0] + Ps4)
        st[1]['steady'] = False
        uw = put('UB', st)
        chk('R27 ULKR-12 W_proxy 구간 (k 0 → M) 에 비정상 (UNSTEADY) 단 하나 = 미계산 (None · 0 J 아님) · 주 값 OK 그대로 (끝점 · 확인 단 정상)',
            lambda: uw['primary_status'] == 'OK' and uw['w_proxy_J'] is None and uw['w_proxy']['status'] == 'NOT_COMPUTED')
    with tempfile.TemporaryDirectory() as root:
        # ── ULR1-03 접촉 상태 · 상쇄 · 분리 · 창 결손 ──
        def wins(counts, pressures):
            return [{'step': 100 + i, 'Ps_avg': p / 1000.0, 'n_contact_geo': c} for i, (c, p) in enumerate(zip(counts, pressures))]

        def walls(counts):
            return {100 + i: (None if c == 'M' else [{'fnz': -1.0}] * c) for i, c in enumerate(counts)}

        s = None
        try:
            st = window_states(wins([2, 0, 0], [0.4, 0, 0]), walls([2, 0, 0]), P)
            s = separation(st, 2)
        except Exception:  # noqa: BLE001
            s = None
        chk('R6 ULR1-03 [2, 0, 0] (P 0.4 · 0 · 0) → CONTACT → (첫 0 창 = 대기) → 둘째 0 창 끝에 SEPARATED · TENSION 을 거치지 않는다',
            lambda: [x['state'] for x in st] == ['CONTACT', 'ZERO', 'ZERO'] and s['declared_index'] == 2 and s['declared_step'] == 102)
        chk('R6 ULR1-03 [0, 0, 1, 1] (P 0 · 0 · 0.2 · 0.2) → 둘째 창에 분리 → 셋째 창 재접촉 → 분리 계수 · 분리 뒤 창 · 표면 관측 초기화 (분리 미완료)',
            lambda: (lambda s2: s2['declared_index'] == 1 and s2['recontact_index'] == [2] and s2['separated_final'] is False
                     and s2['post_windows'] == [])(separation(window_states(wins([0, 0, 1, 1], [0, 0, 0.2, 0.2]), walls([0, 0, 1, 1]), P), 2)))
        chk('R6 ULR1-03 [0, 결손, 0] → OBS_MISSING 은 0 이 아니다 → 분리 선언 없음',
            lambda: (lambda st3: [x['state'] for x in st3] == ['ZERO', 'OBS_MISSING', 'ZERO'] and separation(st3, 2)['declared_index'] is None)(
                window_states(wins([0, 0, 0], [0, 0, 0]), walls([0, 'M', 0]), P)))
        chk('R6 ULR1-03 P ≤ 0 만으로 분리 아님 — 접촉 2 (+0.25 · −0.25 순힘 0) · P 0 → TENSION (분리 아님)',
            lambda: window_states(wins([2], [0.0]), {100: [{'fnz': -0.625}, {'fnz': 0.625}]}, P)[0]['state'] == 'TENSION')
        # 상쇄 +1.6 / −0.6 (Codex state.json pressure_positive_cancellation) — 종단: 런 폴더 → 판독
        Ps4 = [1.2, 1.0, 0.6, 0.4]
        canc = [-1.6 * 2.5, 0.6 * 2.5]
        st = _ladder([0.2, 0.25, 0.3, 0.35], Ps4)
        st[2]['wall'] = [canc] * 4
        st[2]['P'] = 1.0
        _mk_arm(root, B73, 'UB', {'W': 5000, 'dt': 1e-6, 'steps': st, 'events': [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')], 'summary': 'DONE'}, P)
        chk('R7 ULR1-03 상쇄: 교차 끝점 압축 1.6 · 인장 0.6 MPa (순 1.0) → 접촉 상태 CONTACT · 상쇄 표지 참 (0.6 ≥ 0.5 · P_meas) · '
            '처분 = 진단값 (순위 밖) · 주 측정 자격은 따로 (세 칸)',
            lambda: (lambda u: u['endpoint_states'][-1] == 'CONTACT' and u['cancellation'] is True and u['rank_eligible'] is False
                     and u['disposition'] == 'DIAGNOSTIC')(arm_verdict(os.path.join(root, B73, 'UB'), B73, 'UB', P, root=root)))
        # 비단조 (Codex live_nonmonotone_b_reference) — 첫 교차 점 추정 + 합집합 괄호 · b 없음
        _mk_arm(root, B73, 'UC', {'W': 5000, 'dt': 1e-6, 'steps': _ladder([1.0, 1.05, 1.1, 1.15], [1.2, 0.8, 1.3, 0.7]),
                                  'events': [('CROSS', 2, 'first')], 'summary': 'DONE'}, P)
        chk('R8 ULR1-05 ① 비단조 1.2 · 0.8 · 1.3 · 0.7 MPa → 첫 교차 ρ 0.9229910312286136 % · 비단조 표지 · 보고 괄호 = 교차 괄호 합집합 [1.0, 1.15] µm · b 판정 없음',
            lambda: (lambda u: abs(u['rho_pct'] - 0.9229910312286136) < 1e-12 and u['nonmonotone'] is True
                     and abs(u['union_bracket_um'][0] - 1.0) < 1e-12 and abs(u['union_bracket_um'][1] - 1.15) < 1e-12
                     and 'band_b' not in u and 'b_pp' not in u)(arm_verdict(os.path.join(root, B73, 'UC'), B73, 'UC', P, root=root)))
        # A 단 교차 = A 괄호 그대로 (되돌려 B 로 대체하지 않는다)
        stA = [{'lift_um': 0.0, 'P': 160.0, 'steady': True, 'nw': 3, 'kind': '0', 'phase': 4},
               {'lift_um': 0.2, 'P': 1.4, 'steady': True, 'nw': 4, 'kind': 'A', 'phase': 0, 'n_move': 0},
               {'lift_um': 0.4, 'P': 0.6, 'steady': True, 'nw': 4, 'kind': 'A', 'phase': 0, 'n_move': 0}]
        _mk_arm(root, B73, 'UVb', {'W': 10000, 'dt': 5e-7, 'steps': stA, 'events': [], 'summary': None}, P)
        chk('R8 A 단 교차 → 실제 괄호 = A 괄호 [0.2, 0.4] µm 그대로 (예정 Δz_B 아님 · §12-3)',
            lambda: (lambda u: abs(u['bracket_um'][0] - 0.2) < 1e-12 and abs(u['bracket_um'][1] - 0.4) < 1e-12)(
                arm_verdict(os.path.join(root, B73, 'UVb'), B73, 'UVb', P, root=root)))
    with tempfile.TemporaryDirectory() as root:
        # ── ULR1-04 물리 창 — 생성된 덱에서 다시 계산 · S4 반례 (표면 0.6 µm / 덱 s) ──
        dw = {}
        try:
            dw = {k: deck_windows(t) for k, t in decks.items()}
        except Exception:  # noqa: BLE001
            dw = {}
        chk('R9 ULR1-04 생성된 덱에서 창 물리 시간 다시 계산: UB 5,000 × 1e-6 · UT · U_UT3 · U_UVb 10,000 × 5e-7 = 0.005 덱 s (모두 같다)',
            lambda: all(abs(dw[k]['T_W'] - 0.005) < 1e-15 for k in decks) and dw['UT']['W'] == 10000 and dw['U_UVb']['W'] == 10000 and dw['U_UB']['W'] == 5000)

        def s4_case(deck_text, job):
            ww = deck_windows(deck_text)
            u = 0.6   # µm / 덱 s
            hs = [120.0 + u * ww['T_W'] * i for i in range(5)]   # 창 끝마다 · 창 시간 = 그 덱의 W × dt
            st = _ladder([0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4])
            st.append({'lift_um': 0.4, 'P': 0.0, 'steady': True, 'nw': 5, 'kind': 'B', 'phase': 2, 'modeB': 1, 'n_move': 0,
                       'wall': [[]] * 5, 'surface': hs})   # 둘째 0 창에 분리 선언 → 분리 뒤 4 창 (선언 창 포함)
            _mk_arm(root, B73, job, {'W': ww['W'], 'dt': ww['dt'], 'steps': st, 'deck': deck_text,
                                     'events': [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')], 'summary': 'DONE'}, P)
            return arm_verdict(os.path.join(root, B73, job), B73, job, P, root=root)

        chk('R9 ULR1-04 S4 반례 — 생성된 U_UT3 덱 (창 10,000 step = 0.005 s) 에서 표면 0.6 µm/s = 0.003 µm/창 → S4 FAIL',
            lambda: s4_case(decks['U_UT3'], 'UT3')['s4_status'] == 'FAIL')
        bad_deck = decks['U_UT3'].replace('variable ul_W equal 10000', 'variable ul_W equal 5000')
        chk('R9 ULR1-04 판별력 — 옛 규약 (dt₀/2 에서도 5,000 step = 0.0025 s) 덱이면 0.0015 µm/창 → PASS 로 바뀐다 (그래서 덱에서 다시 계산한다)',
            lambda: s4_case(bad_deck, 'UVb')['s4_status'] == 'PASS')
    with tempfile.TemporaryDirectory() as root:
        # ── 이어 돌림 · 10 쌍 표 · KE 기준 · S0′ ──
        sp = {'W': 5000, 'dt': 1e-6, 'steps': _ladder([0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4]),
              'events': [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')], 'summary': 'DONE'}
        d = _mk_arm(root, B73, 'UB', sp, P)
        wpath = os.path.join(d, 'ul_windows.csv')
        L = open(wpath).read().splitlines()
        stale = [ln.split(',') for ln in L[1:] if ln.split(',')[2] == '2']
        resume_step = int([ln.split(',') for ln in L[1:] if ln.split(',')[2] == '1'][-1][5])
        extra = [','.join(r[:5] + [str(int(r[5]))] + r[6:8] + ['9.999'] + r[9:]) for r in stale[:2]]
        _w(wpath, '\n'.join(L[:1] + [ln for ln in L[1:] if int(ln.split(',')[5]) <= resume_step] + extra + L[1:][len([1 for ln in L[1:] if int(ln.split(',')[5]) <= resume_step]):]) + '\n')
        open(os.path.join(d, 'ul_events.csv'), 'a').write(f'RESUME,1,{resume_step},0.111252,0.0002,state\n')
        # 러너 · 덱이 쓰는 이어 돌림 기록 (ULKRR-02 — 승인 경계 = RESUME 사건 + 러너 시도 기록 resume_from + 덱 상태 파일 k)
        _w(os.path.join(d, 'run_manifest.txt'), f'bed={B73}\njob=UB\nresume=0\ngate=ALLOW\nend=a1 fails=1 reader_rc=0\nbed={B73}\njob=UB\nresume=1\ngate=RESUME\n'
           f'resume_from={resume_step}\nend=a2 fails=0 reader_rc=0\n')
        _w(os.path.join(d, 'restart', f'state_unload_{resume_step}.in'), f'variable ul_rstep equal {resume_step}\nvariable ul_k equal 1\n')
        chk('R10 이어 돌림: 실패한 시도가 남긴 이어 돌림 step 뒤 창 줄 (P 9.999) 은 버리고 새 시도 줄만 쓴다 — 판독 같음 (ρ 0.2026…)',
            lambda: (lambda u: abs(u['rho_pct'] - 0.2026077873428664) < 1e-12 and u['n_superseded_rows'] == 2)(
                arm_verdict(d, B73, 'UB', P, root=root)))
        vs = {'ps_0_10_r45': {'primary_status': 'OK', 'union_bracket_pct': [1.0, 1.2], 'rank_eligible': True},
              'ps_3_7_r45': {'primary_status': 'OK', 'union_bracket_pct': [1.1, 1.3], 'rank_eligible': True},
              'ps_5_5_r45': {'primary_status': 'OK', 'union_bracket_pct': [1.4, 1.5], 'rank_eligible': True},
              'ps_7_3_r45': {'primary_status': 'OK', 'union_bracket_pct': [0.5, 0.6], 'rank_eligible': False},
              'ps_10_0_r45': {'primary_status': 'NOISE_FLOOR', 'union_bracket_pct': None, 'rank_eligible': False}}
        chk('R11 10 쌍 표: 괄호 겹침 = 미구분 (0:10 ↔ 3:7) · 분리 = 구분 (3:7 ↔ 5:5) · 상쇄 진단값 · 무효 침대 = 미식별 · 10 쌍 전부',
            lambda: (lambda t: len(t) == 10 and {(r['a'], r['b']): r['relation'] for r in t}[('ps_0_10_r45', 'ps_3_7_r45')] == 'OVERLAP'
                     and {(r['a'], r['b']): r['relation'] for r in t}[('ps_3_7_r45', 'ps_5_5_r45')] == 'SEPARATED'
                     and {(r['a'], r['b']): r['relation'] for r in t}[('ps_3_7_r45', 'ps_7_3_r45')] == 'UNIDENTIFIED'
                     and {(r['a'], r['b']): r['relation'] for r in t}[('ps_0_10_r45', 'ps_10_0_r45')] == 'UNIDENTIFIED')(pair_table(vs)))
        def mk_uk(mut=None):
            """합성 UK 단계 — 모듈 _mk_uk (ULKRR-03 실제 CLI 시험과 같은 꼴) 를 이 root 에."""
            return _mk_uk(root, P, mut)
        mk_uk()
        chk('R12 KE 기준: 병진 = 표 (7:3 2.04e-07) · 회전 = UK 창 평균 셋의 중앙값 (2e-08) · S2 문턱 = 10 × 합 = 2.24e-06 · 기준 파일',
            lambda: (lambda k: abs(k['rot'] - 2e-8) < 1e-20 and abs(k['s2_limit'] - 2.24e-6) < 1e-18 and 'ul_S2max' in k['text'])(kebase(root, B73, P, write=False)))

        def no_base(mut):
            base = os.path.join(root, B73, 'ul_base.in')
            if os.path.exists(base):
                os.remove(base)
            mk_uk(mut)
            k = kebase(root, B73, P)
            return k['s2_limit'] is None and k['text'] is None and not os.path.exists(base)
        for mut, what in (('one_row', 'Codex one_uk_row (step 1 · w 1 · 회전 0.001 J 한 줄 — 옛 판독 S2max 0.01000204 J)'),
                          ('dup_w', '같은 창 두 번 (w 1 · 2 · 2)'), ('spacing', '창 간격 ≠ T_W (셋째 창 +1,000 step)'),
                          ('motion', '판 이동 (둘째 창 plate_z ≠ h0 · lift ≠ 0)'), ('k1', 'k = 1 (S0 k = 0 아님)'), ('phase0', '단계 0 (HOLD0 4 아님)'),
                          ('four', '창 넷 (정확히 셋 아님)'), ('other_arm', '다른 팔 (UB) 의 창 기록'), ('csv_bad', '열 수 다른 줄 (파서가 버린 줄)'),
                          ('guard', '덱 요약 GUARD (DONE 아님)'), ('tech', '단계 기술 실패 (run_check FAIL · 화면 ERROR)')):
            chk(f'R25 ULKR-09 UK {what} → KE 기준 미발행 (s2_limit 없음 · ul_base.in 안 씀)', lambda m=mut: no_base(m))
        mk_uk()
        ext = os.path.join(root, B100, 'EXT')
        lines = ['    Step    Atoms         KinEng        ul_erot          ul_Ps       pressMPa            CPU ', ' 3600000 159152 3.5e-06 1e-07 0.3 0.3 0']
        lines += [f' {3600000 + 1000 * k} 159152 {1e-7 * (1 + (k % 5))} 1e-08 0.174 0.174 {k}' for k in range(1, 61)]
        lines.append('Loop time of 1 on 6 procs for 60000 steps with 159152 atoms')
        _w(os.path.join(ext, 'screen.txt'), '\n'.join(lines) + '\n')
        _w(os.path.join(ext, 'restart', 'restart_ext_3650000.bin'), 'x')
        _w(os.path.join(ext, 'restart', 'restart_ext_3660000.bin'), 'x')
        chk('R13 10:0 S0′: EXT 로그 ± 5,000 · 마지막 25 줄 1 % 안 → S0′ = 3,650,000 · KE 병진 기준 = 5 줄 창 평균 다섯의 중앙값 · 체크포인트 실재',
            lambda: (lambda s: s['status'] == 'PASS' and s['s0'] == 3650000 and abs(s['ke_trans'] - 3e-7) < 1e-18)(s0p_decision(root, P, write=False)))
    with tempfile.TemporaryDirectory() as root:
        # ── 복원 판정 조립 (§12-1 ⑤ · 개정 3 §14-10) — 합성 RJ 폴더 (단계 기록 · 화면 · G2 · G2c · mesh · PRE · POST · R_END · UN) ──
        hv = os.path.join(root, 'hist_verdict.json')
        good = {'schema': 'ps45_unload_history_verdict_v1', 'exit_code': 0, 'rows': {f'H{i}': {'status': 'PASS'} for i in range(6)},
                'info': {'syn': {'status': 'PASS', 'plate_fn_sign': -1}, 'force_timing': 'PASS'}}

        def rv(h, mut=None, full=False):
            shutil.rmtree(os.path.join(root, B73), ignore_errors=True)
            J = _mk_rj(root, B73, P, mut)
            if mut == 'reset_missing':
                sp = os.path.join(J, 'R', 'screen.txt')
                _w(sp, open(sp).read().replace('Resetting per-atom state of Fix history_zwall_bot', 'x'))
            if h is not None:
                _w(hv, json.dumps(h))
            r = restore_verdict(root, B73, 'RJ', hv if h is not None else None, P)
            return r if full else r['status']

        def rv_gate(h, mut=None):
            """복원 판정을 러너처럼 증서로 쓴 뒤 다음 제출 관문 (UB) — (판정, 관문 허용?)."""
            r = rv(h, mut, full=True)
            _w(os.path.join(root, B73, 'RJ', 'restore_verdict.json'), json.dumps(r, default=lambda o: sorted(o) if isinstance(o, set) else str(o)))
            _w(os.path.join(root, B73, 'ul_base.in'), 'variable ul_S2max equal 1e-05\n')
            return r['status'], gate(root, B73, 'UB', P)[0]
        chk('R14 복원 판정 조립: reset 로그 다섯 · G0 · G1 · G2 · G2c · mesh md5 · G3 · PRE = POST · UN 소거 보임 · 이력 시험 rc 0 (H0–H5 PASS) → RESTORED',
            lambda: rv(good) == 'RESTORED')
        chk('R14 이력 시험 없음 · rc 2 → UNCONFIRMED (표지만 달아 U 로 넘기지 않는다)',
            lambda: rv(None) == 'UNCONFIRMED' and rv(dict(good, exit_code=2)) == 'UNCONFIRMED')
        chk('R14 이력 시험 SYN 의 판 접촉 법선력 부호 (+1) ≠ 표 plate_fn_compressive_sign (−1) → UNCONFIRMED (표를 결과 0 건에서 고친 뒤)',
            lambda: rv(dict(good, info={'syn': {'status': 'PASS', 'plate_fn_sign': 1}, 'force_timing': 'PASS'})) == 'UNCONFIRMED')
        chk('R14 바닥 primitive per-atom reset 로그 빠짐 → VALUE_MISMATCH', lambda: rv(good, 'reset_missing') == 'VALUE_MISMATCH')
        # ── ULKR-05 반례 (Codex history_restore — 판정문 §3) · 각 변이에서 복원 + 다음 제출 (UB) 함께 거부 ──
        chk('R14 정상 RJ 폴더 + 증서 → 다음 제출 (UB) 허용 (반례의 대조)', lambda: rv_gate(good) == ('RESTORED', True))
        for mut, want, what in (('trunc_prepost', 'UNCONFIRMED', 'PRE · POST 가 3 원자를 선언하고 1 행만 (둘 다 파서 ok=false)'),
                                ('post_dup_id', 'UNCONFIRMED', 'POST 에 같은 ID 둘 (선언 = 행 수)'),
                                ('pre_nan', 'UNCONFIRMED', 'PRE 한 행 NaN (파서가 버림 — 관측 결손 · 수치 불일치가 아니다)'),
                                ('end_wrong_step', 'UNCONFIRMED', 'R_END 머리 step = S0 + 1,000 (기대 S0 + 2,000)'),
                                ('un_other_ids', 'UNCONFIRMED', 'UN = ID 999 하나의 0 (R_END = ID 1 · 2 · 3 · ID 1 이력 비영)'),
                                ('un_tech_fail', 'SYNTAX_FAIL', 'UN 화면 ERROR · 단계 기록 FAIL rc=1 (부분 덤프는 남음)'),
                                ('r_runcheck_missing', 'SYNTAX_FAIL', 'R 단계 기록 (run_check.txt) 없음'),
                                ('ut0_fail', 'SYNTAX_FAIL', '7:3 Ut0 단계 기록 FAIL rc=1 (R 의 선행 단계)')):
            chk(f'R17 ULKR-05 {what} → {want} · 다음 제출 (UB) 거부', lambda mut=mut, want=want: rv_gate(good, mut) == (want, False))
        chk('R17 ULKR-05 RESTORED 증서인데 RJ 잡 기록 끝 줄 fails=1 (러너가 같은 실행 끝에 기술 실패) → 다음 제출 (UB) 거부',
            lambda: rv_gate(good, 'manifest_fail') == ('RESTORED', False))
        chk('R17 ULKR-05 RESTORED 증서인데 RJ 잡 기록에 끝 줄 없음 (러너가 끝내지 못함) → 다음 제출 거부',
            lambda: rv_gate(good, 'manifest_no_end') == ('RESTORED', False))
        # ── ULKR-08 — SYN PASS + 측정 부호 = 표 · 총힘 시점 PASS 필수 (SYN 없음 = 자격 없음) ──
        for name, h in (('SYN 없음 (NOT_RUN · 부호 null — Codex actual_bundle_without_SYN)', dict(good, info={'syn': {'status': 'NOT_RUN', 'plate_fn_sign': None},
                                                                                                                'force_timing': 'PASS'})),
                        ('SYN FAIL (부호는 표와 같음)', dict(good, info={'syn': {'status': 'FAIL', 'plate_fn_sign': -1}, 'force_timing': 'PASS'})),
                        ('총힘 출력 시점 FAIL (C1 선행조건)', dict(good, info={'syn': {'status': 'PASS', 'plate_fn_sign': -1}, 'force_timing': 'FAIL'})),
                        ('판정 schema 다름 (다른 판정 파일)', dict(good, schema='x'))):
            chk(f'R18 ULKR-08 이력 시험 H0–H5 PASS · rc 0 인데 {name} → UNCONFIRMED · 다음 제출 거부',
                lambda h=h: rv_gate(h) == ('UNCONFIRMED', False))
        chk('R19 판독기의 바닥 이력 관측 열 = 생성기가 R · UNread 덱에 쓰는 열 (PRE write_dump · POST 덤프 — 따로 적은 사본이 어긋나면 관측 전부 결손)',
            lambda: list(HIST_PRE_COLS) == mk._hist_dump_cols(forces=False).split() and list(HIST_POST_COLS) == mk._hist_dump_cols().split()
            and f'write_dump all custom ${{out}}/obs/pre_bot.dump {" ".join(HIST_PRE_COLS)}' in mk.render(B73, 'R', P)
            and f'write_dump all custom ${{out}}/obs/un_pre_bot.dump {" ".join(HIST_PRE_COLS)}' in mk.render(B73, 'UNread', P)
            and all(f'dump ul_da all custom ${{ul_W}} ${{out}}/dump/atom_*.dump {" ".join(ATOM_COLS)}' in mk.render(B73, k, P) for k in ('U_UB', 'UT', 'G_UVb'))
            and all(f'dump ul_dc all local ${{ul_W}} ${{out}}/dump/contact_*.dump {" ".join(CPL_COLS)}' in mk.render(B73, k, P) for k in ('U_UB', 'UT', 'G_UVb')))
        real = _repo_history_verdict()
        chk('R18 ULKR-08 실제 반입 이력 판정 (10-14 job 283122 · SYN PASS −1 · 총힘 PASS) → RESTORED · 같은 판정에서 SYN 만 뺌 → UNCONFIRMED',
            lambda: real is not None and rv(real) == 'RESTORED'
            and rv(dict(real, info=dict(real['info'], syn={'status': 'NOT_RUN', 'checks': {}, 'plate_fn_sign': None}))) == 'UNCONFIRMED')
        # ── ULKRR-03 — 다음 관문이 읽는 잡 완료 영수증 = fails=0 · reader_rc=0 둘 다 (있고 · 정수 · 0) · 문법 fixture 사전 점검 PASS 줄 (Q5) ──
        for mut, what in (('manifest_reader_rc', '끝 줄 fails=0 · reader_rc=120 (판독기가 증서를 쓴 뒤 실패 — Codex runner_recheck manifest_reader_rc1 꼴)'),
                          ('manifest_reader_rc_missing', '끝 줄에 reader_rc 없음'), ('manifest_reader_rc_text', '끝 줄 reader_rc=x (정수 아님)'),
                          ('manifest_no_grammar', '잡 기록에 문법 fixture 사전 점검 PASS 줄 (grammar_prereq=PASS) 없음 (Q5 — R 전 강제의 기록)')):
            chk(f'R29 ULKRR-03 RESTORED 증서인데 RJ {what} → 다음 제출 (UB) 거부', lambda mut=mut: rv_gate(good, mut) == ('RESTORED', False))
        # ── ULKRR-04 — 복원 관측 · S0 의 ID = 유한 · 양 · 정확한 정수 · 필수 열 결손 = 관측 결손 (예외 없음) ──
        for mut, what in (('un_frac_id', 'UN 첫 ID 1 → 1.5 (Codex fractional_un_id — 정수 1 로 잘려 RESTORED · UB 허용이던 것)'),
                          ('pre_frac_id', 'PRE 둘째 ID 2 → 2.5'), ('s0_no_id', '원 atom_S0 머리 id → not_id (예외 없이 판정)')):
            chk(f'R30 ULKRR-04 복원 {what} → RESTORED 아님 · 다음 제출 (UB) 거부', lambda mut=mut: (lambda r: r[0] != 'RESTORED' and r[1] is False)(rv_gate(good, mut)))
        # ── ULKRR-03 실제 판독기 CLI — stdout 이 닫힌 채 (Codex actual_restore_cli_closed_stdout): 결과 파일을 쓴 뒤 출력 flush 에서 rc 120 ──
        import subprocess

        def closed_cli(args):
            p = subprocess.Popen([sys.executable, '-I', os.path.abspath(__file__)] + args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            p.stdout.close()
            return p.wait(timeout=600)
        cli = {}
        try:
            shutil.rmtree(os.path.join(root, B73), ignore_errors=True)
            J = _mk_rj(root, B73, P)
            _mk_uk(root, P)
            _w(hv, json.dumps(good))
            cli['rc_r'] = closed_cli(['restore', root, B73, '--hist', hv])
            cli['rc_k'] = closed_cli(['kebase', root, B73])
            cli['status'] = json.load(open(os.path.join(J, 'restore_verdict.json'))).get('status')
            cli['base'] = os.path.exists(os.path.join(root, B73, 'ul_base.in'))
            man = os.path.join(J, 'run_manifest.txt')     # 러너 기록 꼴 (run_unload.sh reader() · kebase 실패 = RRC 2)
            _w(man, open(man).read().replace('end=x fails=0 reader_rc=0\n', f'reader_restore_rc={cli["rc_r"]}\nreader_kebase_rc={cli["rc_k"]}\n'
                                             f'end=x fails=0 reader_rc={2 if cli["rc_k"] else cli["rc_r"]}\n'))
            cli['gate'] = gate(root, B73, 'UB', P)[0]
        except Exception as ex:  # noqa: BLE001 — 시험 먼저 · 예외도 실패
            cli['error'] = repr(ex)
        chk('R29 ULKRR-03 실제 판독기 CLI (stdout 닫힘) — restore 가 RESTORED 증서 · kebase 가 기준 파일을 쓴 뒤 둘 다 rc 120 → 러너 기록 끝 줄 reader_rc 2 '
            '(fails=0) → 다음 제출 (UB) 거부 (판독 오류를 rc 0 으로 삼키지 않는다)',
            lambda: cli.get('rc_r') == 120 and cli.get('rc_k') == 120 and cli.get('status') == 'RESTORED' and cli.get('base') is True and cli.get('gate') is False,
            str(cli))
        # ── ULKRF-03 (Codex 수정 재확인 10-15 · g2c_c_cpl7_missing · g2c_c_cpl8_missing · g2c_missing_column_actual_cli) — G2c 쌍 덤프 필수 열 결손 (양쪽 비교 파일) =
        #    예외 없이 사유 → RESTORED 아님 · 다음 제출 거부 · 실제 restore CLI = rc 2 (Traceback rc 1 아님) · 증서 미발행 · 숫자 채우기 · 행 삭제 없음 ·
        #    ULPR-04 (사전 리뷰 10-21 · 1저자 Q2 권고대로) — 그 결손 = 관측 결손 → G2c NOT_COMPUTED → 복원 UNCONFIRMED (등록 §14-10 · 옛 판 = FAIL → VALUE_MISMATCH) ──
        def g2c_fail(r):
            g = r['checks']['G2c']
            return r['status'] == 'UNCONFIRMED' and g.get('status') == 'NOT_COMPUTED' and any('열 이름' in w for w in g.get('why', []))
        for mut, what in (('g2c_test_no_c7', 'R/g2 쌍 덤프 머리 c_cpl[7] → not_c_cpl[7] (Codex g2c_c_cpl7_missing)'),
                          ('g2c_test_no_c8', 'R/g2 쌍 덤프 머리 c_cpl[8] → not_c_cpl[8] (Codex g2c_c_cpl8_missing)'),
                          ('g2c_orig_no_c7', '원 in/ 쌍 덤프 머리 c_cpl[7] → not_c_cpl[7]'), ('g2c_orig_no_c8', '원 in/ 쌍 덤프 머리 c_cpl[8] → not_c_cpl[8]')):
            chk(f'R35 ULKRF-03 · ULPR-04 복원 {what} → 예외 없이 G2c 관측 결손 NOT_COMPUTED + 사유 (열 이름) · 복원 UNCONFIRMED (VALUE_MISMATCH 아님 · 등록 §14-10) · '
                'RESTORED 아님 · 다음 제출 (UB) 거부',
                lambda mut=mut: g2c_fail(rv(good, mut, full=True)) and rv_gate(good, mut)[1] is False)
        chk('R35 ULPR-04 대조: R/g2 쌍 덤프 법선 힘 −0.5 → −0.6 (수치 불일치) → G2c FAIL → VALUE_MISMATCH 그대로 (관측 결손 UNCONFIRMED 와 따로) · 다음 제출 거부',
            lambda: (lambda r: r['status'] == 'VALUE_MISMATCH' and r['checks']['G2c'].get('status') == 'FAIL')(rv(good, 'g2c_value', full=True))
            and rv_gate(good, 'g2c_value') == ('VALUE_MISMATCH', False))
        chk('R35 ULPR-03 복원: R/g2 원자 덤프에 같은 ID 두 줄 (첫 줄 x 다름 · 선언 수 = 행 수 — 옛 판 = 뒤 줄이 덮어 G2 PASS · RESTORED) → G2 관측 결손 NOT_COMPUTED '
            '(ID 중복) → UNCONFIRMED · 다음 제출 거부',
            lambda: (lambda r: r['status'] == 'UNCONFIRMED' and r['checks']['G2'].get('status') == 'NOT_COMPUTED'
                     and any('ID 중복' in w for w in r['checks']['G2'].get('why', [])))(rv(good, 'g2_dup_id', full=True))
            and rv_gate(good, 'g2_dup_id') == ('UNCONFIRMED', False))
        clg = {}
        try:
            shutil.rmtree(os.path.join(root, B73), ignore_errors=True)
            J = _mk_rj(root, B73, P, 'g2c_test_no_c7')
            _w(hv, json.dumps(good))
            g2p = os.path.join(J, 'R', 'g2', f'contact_{P["beds"][B73]["s0"]}.liggghts')
            before = ul_lib.sha256_file(g2p)
            pr_ = subprocess.run([sys.executable, '-I', os.path.abspath(__file__), 'restore', root, B73, '--hist', hv], capture_output=True, text=True, timeout=600)
            clg['rc'] = pr_.returncode
            clg['traceback'] = 'Traceback' in pr_.stderr
            rj = _readjson(os.path.join(J, 'restore_verdict.json')) or {}
            clg['status'] = rj.get('status')
            clg['g2c'] = (rj.get('checks') or {}).get('G2c') or {}
            clg['dump_same'] = ul_lib.sha256_file(g2p) == before
            clg['gate'] = gate(root, B73, 'UB', P)[0]
        except Exception as ex:  # noqa: BLE001 — 시험 먼저 · 예외도 실패
            clg['error'] = repr(ex)
        chk('R35 ULKRF-03 · ULPR-04 실제 restore CLI — R/g2 쌍 덤프 머리 c_cpl[7] 결손 → rc 2 (Traceback · rc 1 아님 · 다른 UNCONFIRMED 와 같은 rc) · '
            'restore_verdict.json = UNCONFIRMED (RESTORED 아님 · 증서 미발행) · G2c 관측 결손 NOT_COMPUTED + 사유 (열 이름) · 덤프 그대로 (채우기 · 지우기 없음) · '
            '다음 제출 (UB) 거부',
            lambda: clg.get('rc') == 2 and clg.get('traceback') is False and clg.get('status') == 'UNCONFIRMED' and clg['g2c'].get('status') == 'NOT_COMPUTED'
            and any('열 이름' in w for w in clg['g2c'].get('why', [])) and clg.get('dump_same') is True and clg.get('gate') is False, str(clg)[:600])
    with tempfile.TemporaryDirectory() as root:
        # ── ULKRR-03 RJ2 관문 = S0′ 결정 PASS + 그 EXT 잡 완료 영수증 (fails=0 · reader_rc=0) ──
        _w(os.path.join(root, B100, 's0_decision.json'), json.dumps({'status': 'PASS', 's0': 3650000}))

        def ext_man(end):
            _w(os.path.join(root, B100, 'EXT', 'run_manifest.txt'), f'bed={B100}\njob=EXT\nresume=0\ngrammar_prereq=PASS\n' + end)
            return gate(root, B100, 'RJ2', P)[0]
        chk('R29 ULKRR-03 RJ2 관문: S0′ 결정 PASS + EXT 끝 줄 fails=0 · reader_rc=0 = 허용 · fails=1 · reader_rc=1 · reader_rc 없음 · 끝 줄 없음 = 거부',
            lambda: ext_man('end=x fails=0 reader_rc=0\n') and not ext_man('end=x fails=1 reader_rc=0\n') and not ext_man('end=x fails=0 reader_rc=1\n')
            and not ext_man('end=x fails=0\n') and not ext_man(''))
    with tempfile.TemporaryDirectory() as root:
        # ── ULKRR-02 이어 돌림 경계 — 행 교체 = 승인된 RESUME 경계 (사건 + 러너 시도 기록 resume_from + 덱 상태 파일 k) 에서만 · 그 밖 중복 · 역행 = 미식별 ──
        _fake_restored(root, B73)
        _w(os.path.join(root, B73, 'ul_base.in'), 'variable ul_S2max equal 1e-05\n')
        lad_l, lad_p = [0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4]

        def put2(job, W=5000, dt=1e-6, summary='DONE'):
            shutil.rmtree(os.path.join(root, B73, job), ignore_errors=True)
            return _mk_arm(root, B73, job, {'W': W, 'dt': dt, 'steps': _ladder(lad_l, lad_p), 'summary': summary,
                                            'events': [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')]}, P)

        def ut_chain():
            return (arm_verdict(os.path.join(root, B73, 'UT'), B73, 'UT', P, root=root), selection_state(root, P), gate(root, B73, 'UVa', P))
        put2('UB')
        d = put2('UT', 10000, 5e-7, 'RM_STOP')
        _edit_rows(os.path.join(d, 'ul_steps.csv'), lambda rows: rows.insert(3, dict(rows[3], steady='0')))
        chk('R28 ULKRR-02 RESUME 없이 확인 단 (k 3) 같은 step 중복 — 앞 줄 steady 0 (Codex duplicate_without_resume) → UT 주 값 OK 아님 · 사유 · 선택 UNRESOLVED · UVa 거부',
            lambda: (lambda u, s, g: u['primary_status'] != 'OK' and u['rho_pct'] is None and any('ULKRR-02' in w for w in u['why'])
                     and s['stage'] == 'SELECTION_UNRESOLVED' and not g[0])(*ut_chain()))
        d = put2('UT', 10000, 5e-7, 'RM_STOP')
        _edit_rows(os.path.join(d, 'ul_windows.csv'), lambda rows: rows.insert(len(rows) - 2, dict(rows[-3], Ps_avg='9.999')))
        chk('R28 ULKRR-02 RESUME 없이 창 기록 중복 (같은 k · w · step · 다른 P) → UT 주 값 미식별 (사유) · UVa 거부',
            lambda: (lambda u, s, g: u['primary_status'] != 'OK' and any('ULKRR-02' in w for w in u['why']) and not g[0])(*ut_chain()))
        d = put2('UT', 10000, 5e-7, 'RM_STOP')
        _resume_layout(d, P, job='UT')
        chk('R28 양성 대조: 진짜 이어 돌림 (첫 시도 = 단 1 끝 restart · 상태 파일 뒤 단 2 창 둘 · 단 줄 · 사건을 P 9.999 로 남기고 끊김 → RESUME (k 1 · s_r) · '
            '러너 기록 resume_from=s_r) → 남긴 줄 3 을 버림 · UT 주 값 OK (ρ 0.2026…) · 선택 need_UV → UVa 허용',
            lambda: (lambda u, s, g: u['primary_status'] == 'OK' and abs(u['rho_pct'] - 0.2026077873428664) < 1e-12 and u['n_superseded_rows'] == 3
                     and s['stage'] == 'need_UV' and s['next'] == ['UVa'] and g[0])(*ut_chain()))
        for kw, what in (({'manifest': False}, '러너 시도 기록 (run_manifest resume_from) 없음'), ({'ev_k': 0}, 'RESUME 사건 k 0 ≠ 단 기록 · 상태 파일 k 1'),
                         ({'state_k': 0}, '상태 파일 ul_k 0 ≠ RESUME 사건 k 1'), ({'state_file': False}, '상태 파일 (state_unload_<s_r>.in) 없음')):
            d = put2('UT', 10000, 5e-7, 'RM_STOP')
            _resume_layout(d, P, job='UT', **kw)
            chk(f'R28 ULKRR-02 이어 돌림 꼴인데 {what} → 남긴 줄을 버리지 않는다 · UT 주 값 미식별 (사유) · UVa 거부',
                lambda: (lambda u, s, g: u['primary_status'] != 'OK' and any('ULKRR-02' in w for w in u['why']) and not g[0])(*ut_chain()))
    with tempfile.TemporaryDirectory() as root:
        # ── ULKRF-01 (Codex 수정 재확인 10-15 · one_auth_two_rollbacks · duplicate_event_only) — 승인 = 고유 경계 (k_r, s_r) 하나에 한 번 ·
        #    같은 경계의 RESUME 사건 중복 · 상충 (같은 step 다른 k) = 사유 있는 거부 (승인 하나를 둘로 늘리지 않는다) · 사건 되감기 정리도 같은 규칙 ──
        _fake_restored(root, B73)
        _w(os.path.join(root, B73, 'ul_base.in'), 'variable ul_S2max equal 1e-05\n')

        def put_lad(job, W=5000, dt=1e-6, summary='DONE'):
            shutil.rmtree(os.path.join(root, B73, job), ignore_errors=True)
            return _mk_arm(root, B73, job, {'W': W, 'dt': dt, 'steps': _ladder([0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4]), 'summary': summary,
                                            'events': [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')]}, P)

        def ut_resumed(**kw):
            d = put_lad('UT', 10000, 5e-7, 'RM_STOP')
            _resume_layout(d, P, job='UT', **kw)
            return arm_verdict(d, B73, 'UT', P, root=root), selection_state(root, P), gate(root, B73, 'UVa', P), read_run(d, P)
        put_lad('UB')

        def refused(tag):
            return lambda u, s, g, rr: (u['primary_status'] != 'OK' and u['rho_pct'] is None and any(tag in w for w in u['why'])
                                        and s['stage'] == 'SELECTION_UNRESOLVED' and not g[0])

        def n_cross(rr):
            return sum(1 for e in rr['events'] if e['event'] == 'CROSS')
        chk('R33 대조: 진짜 이어 돌림 한 번 (끊긴 시도 묶음 하나 · RESUME 한 줄) = 승인 (k 1 · s_r) 하나 · 남긴 줄 3 · 옛 사건 버림 · UT 주 값 OK · UVa 허용 (양성 그대로)',
            lambda: (lambda u, s, g, rr: u['primary_status'] == 'OK' and abs(u['rho_pct'] - 0.2026077873428664) < 1e-12 and u['n_superseded_rows'] == 3
                     and len(rr['resume_auth']) == 1 and n_cross(rr) == 1 and s['stage'] == 'need_UV' and g[0])(*ut_resumed()))
        chk('R33 ULKRF-01 러너 resume_from 한 줄 · 상태 파일 하나 · 같은 RESUME (k 1 · s_r) 두 줄 · 끊긴 시도 묶음 둘 (Codex one_auth_two_rollbacks — 옛 판 = 승인 둘 · '
            '두 번 되감아 주 값 OK · UVa 허용) → 같은 경계 사건 중복 = 승인 없음 · 남긴 줄 · 옛 사건을 버리지 않는다 · 주 값 미식별 (사유) · UVa 거부',
            lambda: (lambda u, s, g, rr: refused('ULKRF-01')(u, s, g, rr) and rr['resume_auth'] == [] and rr['n_superseded_rows'] == 0 and n_cross(rr) == 3)(
                *ut_resumed(repeat=2)))
        chk('R33 ULKRF-01 대조: 같은 묶음 둘에 RESUME 한 줄 (Codex one_event_two_rollbacks) → 둘째 되감기 = 승인 밖 → 주 값 미식별 · UVa 거부 (옛 판도 거부)',
            lambda: refused('ULKRR-02')(*ut_resumed(repeat=2, resumes=1)))
        chk('R33 ULKRF-01 같은 RESUME 두 줄 · 되감기 한 번 (Codex duplicate_event_only — 옛 판 = 사유 없이 허용) → 같은 경계 사건 중복 = 사유 있는 거부 · UVa 거부',
            lambda: refused('ULKRF-01')(*ut_resumed(dup_event=True)))
        chk('R33 ULKRF-01 같은 step · 다른 k 의 RESUME (k 1 · k 2 · 상태 파일 ul_k 1 — 상충 · 옛 판 = 허용) → 승인 없음 · 사유 있는 거부 · UVa 거부',
            lambda: refused('ULKRF-01')(*ut_resumed(conflict_k=2)))
        # ── ULPR-02 (사전 리뷰 10-21 · 변이 생존) — ULKRF-01 이 더한 사유 줄 · 조건마다 그 줄 하나를 지우면 이 시험이 그 이유로 실패한다 (거부 → 허용 · 또는 사유 없음) ──
        def resumed_edit(fn):
            d = put_lad('UT', 10000, 5e-7, 'RM_STOP')
            sr = _resume_layout(d, P, job='UT')
            fn(d, sr)
            return arm_verdict(d, B73, 'UT', P, root=root), selection_state(root, P), gate(root, B73, 'UVa', P), read_run(d, P)

        def ev_edit(fn):
            def f(d, sr):
                p = os.path.join(d, 'ul_events.csv')
                L = open(p).read().splitlines()
                i = next(n for n, x in enumerate(L) if x.startswith(f'RESUME,1,{sr},'))
                fn(L, i, sr)
                _w(p, '\n'.join(L) + '\n')
            return f
        chk('R33 ULPR-02 승인된 RESUME 바로 뒤에 러너 resume_from 밖 step (s_r + 1) 의 RESUME 한 줄 (사건 되감기 · 행 교체에는 걸리지 않는 자리) → 사유 (∉ 러너 '
            'resume_from) · 주 값 미식별 · UVa 거부 (그 사유 줄이 없으면 OK · 허용)',
            lambda: refused('∉ 러너 resume_from')(*resumed_edit(ev_edit(lambda L, i, sr: L.insert(i + 1, f'RESUME,1,{sr + 1},0,0,state')))))
        chk('R33 ULPR-02 승인된 RESUME 바로 뒤에 k 숫자 아닌 RESUME (RESUME,x,s_r) → 사유 (k · step 숫자 아님) · 주 값 미식별 · UVa 거부 (그 사유 줄이 없으면 허용)',
            lambda: refused('숫자 아님')(*resumed_edit(ev_edit(lambda L, i, sr: L.insert(i + 1, f'RESUME,x,{sr},0,0,state')))))
        chk('R33 ULPR-02 상태 파일 ul_k 0 ≠ RESUME 사건 k 1 → 사유 = 사건 ↔ 상태 파일 불일치 (≠ 상태 파일 — 행 교체 쪽 ULKRR-02 사유만으로 통과하지 않는다) · UVa 거부',
            lambda: refused('≠ 상태 파일')(*ut_resumed(state_k=0)))

        def stale_k_to_kr(L, i, sr):   # RESUME 바로 앞 = 끊긴 시도가 남긴 경계 뒤 사건 (k 2 · step > s_r) → k 1 (= k_r · 버릴 사건 k > k_r 아님)
            f = L[i - 1].split(',')
            f[1] = '1'
            L[i - 1] = ','.join(f)
        chk('R33 ULPR-02 사건 되감기 — RESUME 앞 경계 뒤 사건의 k 가 k_r (1) → 버릴 사건 k > k_r 아님 → 그 사건을 버리지 않는다 · 사유 · 주 값 미식별 · UVa 거부 '
            '(그 조건이 없으면 그 사건을 버리고 OK · 허용)',
            lambda: (lambda r: refused('버릴 사건 k > k_r')(*r) and any(e['event'] != 'RESUME' and e['k'] == 1 and e['step'] > r[3]['resume_auth'][0][1]
                                                                     for e in r[3]['events']))(resumed_edit(ev_edit(stale_k_to_kr))))
    with tempfile.TemporaryDirectory() as root:
        # ── ULKRF-02 (Codex 수정 재확인 10-15 · resume_completed_hold_5_windows) — 승인된 이어 돌림의 새 시도가 옛 시도보다 늦게 끝나도 (창 4 → 5) 새 시도 시작 =
        #    승인 경계 뒤 k 가 k_r + 1 로 되돌아오는 지점 (단 CSV) · step 역행 (창 CSV) — 먼저 오는 쪽 · 그 앞 옛 시도 줄 (k > k_r) 정리 · 승인 없는 되돌아옴 = 미식별 ──
        _fake_restored(root, B73)
        _w(os.path.join(root, B73, 'ul_base.in'), 'variable ul_S2max equal 1e-05\n')
        shutil.rmtree(os.path.join(root, B73, 'UB'), ignore_errors=True)
        _mk_arm(root, B73, 'UB', {'W': 5000, 'dt': 1e-6, 'steps': _ladder([0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4]), 'summary': 'DONE',
                                  'events': [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')]}, P)
        Rc = P['records']
        wcx, scx = Rc['windows_cols'], Rc['steps_cols']
        tr4, tr5 = _ut_trace(P, 4), _ut_trace(P, 5)

        def k2w(tr, col):
            return [r[wcx.index(col)] for r in tr['windows'] if r[wcx.index('k')] == '2']

        def k2s(tr, col):
            return [r[scx.index(col)] for r in tr['steps'] if r[scx.index('k')] == '2']
        chk('R34 대조: 생성 UT 덱 제어 흐름 (make_unload_decks.deck_sim · 입자 계산 없음) — 단 k 2 창 압력 0.0010 · 0.0009 · 0.0008 · 0.0008 · 0.0008 덱 MPa → '
            'S1 [0, 0, 0, 1, 1] · S2 전부 1 · 다섯째 창에 정상 끝 (n_windows 5 · steady 1) · 0.0009 · 0.0008 × 3 → 넷째 창 · 둘 다 R_M 멈춤 (단 k 1 끝 3,310,000)',
            lambda: k2w(tr5, 'Ps_avg') == ['0.001', '0.0009', '0.0008', '0.0008', '0.0008'] and k2w(tr5, 'S1') == ['0', '0', '0', '1', '1']
            and set(k2w(tr5, 'S2')) == {'1'} and k2s(tr5, 'n_windows') == ['5'] and k2s(tr5, 'steady') == ['1'] and len(k2w(tr4, 'w')) == 4
            and k2s(tr4, 'n_windows') == ['4'] and tr4['result'] == tr5['result'] == 'RM_STOP'
            and [r[scx.index('step')] for r in tr5['steps'] if r[scx.index('k')] == '1'] == ['3310000'])

        def ut_hold(nw_new, nw_old=None, auth=True):
            d, _tr = _ut_trace_arm(root, P, nw_new)
            if nw_old is not None:
                _hold_resume(d, P, nw_old, auth=auth)
            return arm_verdict(d, B73, 'UT', P, root=root), selection_state(root, P), gate(root, B73, 'UVa', P), read_run(d, P)
        f5 = ut_hold(5)
        f4 = ut_hold(4)
        chk('R34 대조: 새 시도 단독 (단 k 2 = 5 창 · 4 창 · 이어 돌림 없음) = UT 주 값 OK (ρ 같은 값) · 선택 need_UV · UVa 허용',
            lambda: all(u['primary_status'] == 'OK' and s['stage'] == 'need_UV' and g[0] for u, s, g, _rr in (f5, f4))
            and abs(f5[0]['rho_pct'] - f4[0]['rho_pct']) < 1e-12, f'{f5[0]["why"]} {f4[0]["why"]}')

        def hold_ok(n_drop):
            return lambda u, s, g, rr: (u['primary_status'] == 'OK' and abs(u['rho_pct'] - f5[0]['rho_pct']) < 1e-12 and u['n_superseded_rows'] == n_drop
                                        and rr['resume_auth'] == [(1, 3310000)] and [x['k'] for x in rr['steps']] == [0, 1, 2, 3, 4]
                                        and s['stage'] == 'need_UV' and g[0])
        chk('R34 ULKRF-02 승인된 이어 돌림 — 옛 시도 단 k 2 = 4 창 (단 끝 3,360,000) · 새 시도 = 5 창 (3,370,000 · 옛 것보다 늦다 — 단 CSV 에 step 역행 없음 · '
            'Codex resume_completed_hold_5_windows — 옛 판 = k [0, 1, 2, 2, 3, 4] 미식별 · UVa 거부) → k 가 k_r + 1 로 되돌아오는 줄 = 새 시도 시작 · '
            '옛 창 넷 + 단 줄 하나 버림 · UT 주 값 OK · UVa 허용',
            lambda: hold_ok(5)(*ut_hold(5, 4)))
        chk('R34 ULKRF-02 같은 길이 (4 → 4 창) · 짧음 (5 → 4 창 — 단 끝 역행) = 정상 (옛 창 넷 · 다섯 + 단 줄 하나 버림 · 주 값 OK · UVa 허용)',
            lambda: (lambda a, b: hold_ok(5)(*a) and hold_ok(6)(*b))(ut_hold(4, 4), ut_hold(4, 5)))
        chk('R34 ULKRF-02 승인 없는 되돌아옴 (같은 줄 · RESUME 사건 · resume_from · 상태 파일 없음 · 4 → 5 창) → 옛 줄을 버리지 않는다 · 주 값 미식별 (사유) · '
            'UVa 거부 (ULKRR-02 원결함 = 무승인 중복 삭제 금지 그대로)',
            lambda: (lambda u, s, g, rr: u['primary_status'] != 'OK' and u['rho_pct'] is None and bool(u['why']) and rr['n_superseded_rows'] == 0
                     and not g[0])(*ut_hold(5, 4, auth=False)))
    with tempfile.TemporaryDirectory() as root:
        # ── ULPR-01 (사전 공격 리뷰 10-21 PRE-UL-01 · 1저자 10-21 Q1 = 고친 뒤 발송) — 승인된 이어 돌림 경계 뒤 줄은 어느 시도가 썼는지 기록으로 증명될 때만 쓴다:
        #    옛 시도가 단 k_r + 1 의 창 · 단 줄 · 사건 (RM) 까지 쓰고 끊긴 뒤 새 시도가 그 단 줄을 다시 쓰기 전에 끝나면 (TIMEOUT · GUARD · 이동 중 TIMEOUT)
        #    옛 단 줄을 정상 관측으로 쓰지 않는다 (같은 꼴 fresh 와 같은 판정 · 교차 전 단 = 같은 하한) · 시도를 가를 수 없으면 쓰지 않는다 (보수) · 정상 이어 돌림 양성 그대로 ──
        _fake_restored(root, B73)
        _w(os.path.join(root, B73, 'ul_base.in'), 'variable ul_S2max equal 1e-05\n')
        LAD = ([0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4], [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')], 'RM_STOP')   # 교차 k 2 · 확인 k 3 · 4 · R_M k 4
        NOC = ([0.2, 0.25, 0.3, 0.35], [1.6, 1.4, 1.2, 0.4], [('CROSS', 4, 'first')], 'DONE')                           # 교차 k 4 (k 1–3 = 교차 전 · 사건 없는 단)
        _mk_arm(root, B73, 'UB', {'W': 5000, 'dt': 1e-6, 'steps': _ladder(LAD[0], LAD[1]), 'summary': 'DONE', 'events': list(LAD[2])}, P)

        def ut_mix(lad=LAD, **kw):
            """7:3 UT (기준 궤적 _mk_arm → _resume_mix) → (팔 판정, 선택, UVa 관문, read_run) · 만들기 · 판독 예외 = 그 예외 (시험 먼저 · 예외도 실패)."""
            try:
                shutil.rmtree(os.path.join(root, B73, 'UT'), ignore_errors=True)
                d = _mk_arm(root, B73, 'UT', {'W': 10000, 'dt': 5e-7, 'steps': _ladder(lad[0], lad[1]), 'summary': lad[3], 'events': list(lad[2])}, P)
                if kw:
                    _resume_mix(d, P, **kw)
                return arm_verdict(d, B73, 'UT', P, root=root), selection_state(root, P), gate(root, B73, 'UVa', P), read_run(d, P)
            except Exception as ex:  # noqa: BLE001
                return ex

        def ks(rr):
            return [x['k'] for x in rr['steps']]

        def k_windows(rr, k):
            return [x['w'] for x in rr['windows'] if x['k'] == k]

        def holds(r, pred):
            return not isinstance(r, Exception) and bool(pred(*r))

        def unid2(u, s, g, rr):   # 같은 꼴 fresh 판정 — 확인 단 2 없음 · 주 값 · 하한 · 점 추정 없음 · 선택 UNRESOLVED · UVa 거부
            return (u['primary_status'] == 'UNIDENTIFIED' and u['rho_pct'] is None and any('확인 단 2 없음' in w for w in u['why'])
                    and ks(rr) == [0, 1, 2, 3] and s['stage'] == 'SELECTION_UNRESOLVED' and not g[0])

        def okp(u, s, g, rr, sup):
            return (u['primary_status'] == 'OK' and abs(u['rho_pct'] - 0.2026077873428664) < 1e-12 and g[0] and ks(rr) == [0, 1, 2, 3, 4]
                    and rr['n_superseded_rows'] == sup)

        def show(r):
            if isinstance(r, Exception):
                return f'{type(r).__name__}: {r}'
            u, s, g, rr = r
            return (f'primary={u["primary_status"]} rho={u["rho_pct"]} lb={u["lower_bound_pct"]} traj={u["trajectory_status"]} k={ks(rr)} '
                    f'sup={rr["n_superseded_rows"]} ev={[(e["event"], e["k"]) for e in rr["events"]]} gate={g[0]} why={u["why"][:2]} pr={rr["problems"][:2]}')
        a0, a1, a3 = ut_mix(), ut_mix(kr=3, new_nw=2, resumed=False), ut_mix(kr=3, new_nw=2, end='GUARD', resumed=False)
        chk('R37 대조: 7:3 UT 한 시도 끝까지 (교차 k 2 · 확인 k 3 · 4 · R_M) = OK ρ 0.2026… · UVa 허용 · 같은 꼴 fresh 가 단 k 4 창 둘 뒤 TIMEOUT · GUARD = '
            'UNIDENTIFIED (확인 단 2 없음) · UVa 거부',
            lambda: holds(a0, lambda *r: okp(*r, 0)) and holds(a1, unid2) and holds(a3, unid2) and a3[0]['trajectory_status'] == 'GUARD',
            f'{show(a0)} | {show(a1)} | {show(a3)}')
        for kw, what, extra in (({'new_nw': 2}, '새 시도가 단 k 4 창 둘 뒤 TIMEOUT (옛 판 = OK ρ 0.2026… · UVa 허용)', lambda u, rr: k_windows(rr, 4) == [1, 2]),
                                ({'new_nw': 2, 'end': 'GUARD'}, '새 시도가 단 k 4 창 둘 뒤 GUARD (요약 GUARD · 옛 판 = OK · UVa 허용)',
                                 lambda u, rr: u['trajectory_status'] == 'GUARD' and k_windows(rr, 4) == [1, 2]),
                                ({'new_nw': 0}, '새 시도가 단 k 4 로 이동 중 TIMEOUT (새 창 없음 · 옛 판 = 옛 창 넷 · 단 줄 그대로 OK)', lambda u, rr: k_windows(rr, 4) == []),
                                ({'new_nw': 4}, '새 시도가 옛 시도와 같은 창 수 (넷) 뒤 단 줄 전 TIMEOUT (단 줄 ↔ 창 수 · 마지막 창 step 이 옛 · 새 둘 다와 같다)',
                                 lambda u, rr: k_windows(rr, 4) == [1, 2, 3, 4])):
            r = ut_mix(kr=3, old_nw=4, old_line=True, old_ev=True, **kw)
            chk(f'R37 ULPR-01 옛 시도 = 단 k 4 창 넷 · 단 줄 · RM 사건 뒤 요약 전 끊김 → RESUME (k 3 · s_r) → {what} → 옛 단 줄 · 창 · 사건을 쓰지 않는다 = 같은 꼴 fresh 판정 '
                '(UNIDENTIFIED · 확인 단 2 없음 · 단 k [0–3] · RM 사건 없음 · 남긴 줄 5) · UVa 거부',
                lambda r=r, extra=extra: holds(r, lambda u, s, g, rr: unid2(u, s, g, rr) and extra(u, rr) and rr['n_superseded_rows'] == 5
                                               and not any(e['event'] == 'RM' for e in rr['events'])), show(r))
        b1 = ut_mix(NOC, kr=2, new_nw=2, resumed=False)
        chk('R37 대조: 교차 전 단 (k 3) 창 둘 뒤 TIMEOUT (fresh) = LOWER_BOUND 0.225119763714296 % (k 2 = 0.25 µm) · 단 k [0–2]',
            lambda: holds(b1, lambda u, s, g, rr: u['primary_status'] == 'LOWER_BOUND' and abs(u['lower_bound_pct'] - 100 * 0.25 / h0um) < 1e-12
                          and ks(rr) == [0, 1, 2]), show(b1))
        for nn, what in ((2, '창 둘 (옛 판 = 옛 단 줄로 하한 0.27014371645715524 %)'),
                         (4, '옛 시도와 같은 창 넷 (사건 없는 단 — 단 줄이 어느 시도 것인지 기록으로 가를 수 없다)'),
                         (0, '이동 중 끝 (새 창 · 사건 없음 — 경계 뒤 줄이 어느 시도 것인지 기록으로 가를 수 없다)')):
            r = ut_mix(NOC, kr=2, old_nw=4, old_line=True, new_nw=nn)
            chk(f'R37 ULPR-01 교차 전 단 — 옛 시도 = 단 k 3 창 넷 · 단 줄 (사건 없는 단) 뒤 끊김 → RESUME (k 2) → 새 시도 {what} → 그 단 줄을 쓰지 않는다 = '
                'fresh 하한 그대로 (LOWER_BOUND 0.225119763714296 % · 단 k [0–2] · 남긴 줄 5)',
                lambda r=r: holds(r, lambda u, s, g, rr: u['primary_status'] == 'LOWER_BOUND' and not isinstance(b1, Exception)
                                  and u['lower_bound_pct'] == b1[0]['lower_bound_pct'] and ks(rr) == [0, 1, 2] and rr['n_superseded_rows'] == 5), show(r))
        pa = ut_mix(kr=1, new_nw=4, new_line=True, new_ev=True, rest=True)
        pb = ut_mix(kr=1, old_nw=2, new_nw=4, new_line=True, new_ev=True, rest=True)
        chk('R37 양성 대조: 옛 시도가 경계 뒤 아무것도 안 씀 (이동 중 끊김) · 옛 시도 창 둘만 (단 줄 · 사건 없음) → 새 시도가 단 k 2 부터 끝까지 → 주 값 OK (ρ 0.2026…) · '
            '남긴 줄 0 · 2 · UVa 허용',
            lambda: holds(pa, lambda *r: okp(*r, 0)) and holds(pb, lambda *r: okp(*r, 2)), f'{show(pa)} | {show(pb)}')
        pc = ut_mix(kr=3, old_nw=4, new_nw=4, new_line=True, new_ev=True, rest=True)
        chk('R37 양성 대조: 옛 시도 = 단 k 4 창 넷 (단 줄 전 · 다섯째 창 중 끊김) → 새 시도 = 창 넷 · 단 줄 · RM 사건 · 요약 (단 줄 ↔ 창이 옛 · 새 둘 다와 맞는다 — '
            'RESUME 뒤 새 시도 RM 사건 (그 단 끝 사건 · 같은 k · step) = 새 시도 단 줄) → 주 값 OK · 남긴 줄 4 · UVa 허용',
            lambda: holds(pc, lambda *r: okp(*r, 4)), show(pc))
        pd_, pd_f = ut_mix(NOC, kr=1, new_nw=4, new_line=True, new_state=True), ut_mix(NOC, kr=1, new_nw=4, new_line=True, new_state=True, resumed=False)
        chk('R37 양성 대조: 사건 없는 단 — 옛 시도 이동 중 끊김 → 새 시도가 단 k 2 를 끝내고 단 끝 restart · 상태 파일 (state_unload_<그 단 끝>) 뒤 k 3 이동 중 끝 '
            '(상태 파일 = 새 시도가 그 단 줄을 썼다) → 단 줄 그대로 · fresh 와 같은 하한 (k 2) · 남긴 줄 0',
            lambda: holds(pd_, lambda u, s, g, rr: holds(pd_f, lambda u2, s2, g2, rr2: u['primary_status'] == u2['primary_status'] == 'LOWER_BOUND'
                                                         and u['lower_bound_pct'] == u2['lower_bound_pct'] and ks(rr) == ks(rr2) == [0, 1, 2])
                          and rr['n_superseded_rows'] == 0), f'{show(pd_)} | {show(pd_f)}')
        pe, pe_f = ut_mix(NOC, kr=1, new_nw=4, new_line=True), ut_mix(NOC, kr=1, new_nw=4, resumed=False)
        chk('R37 시도 미확정 = 쓰지 않는다 (보수): 같은 꼴에서 단 끝 상태 파일 · 사건 · 경계 뒤 다른 단 · 창 역행이 없다 (단 줄 → restart 사이 끊김 — 옛 · 새 어느 시도 '
            '줄인지 기록으로 가를 수 없다) → 경계 뒤 줄 (창 넷 · 단 줄) 을 쓰지 않는다 = 단 k 2 단 줄이 없는 fresh 와 같은 하한 (k 1) · 남긴 줄 5',
            lambda: holds(pe, lambda u, s, g, rr: holds(pe_f, lambda u2, s2, g2, rr2: u['primary_status'] == u2['primary_status'] == 'LOWER_BOUND'
                                                        and u['lower_bound_pct'] == u2['lower_bound_pct'] and ks(rr) == ks(rr2) == [0, 1])
                          and rr['n_superseded_rows'] == 5), f'{show(pe)} | {show(pe_f)}')
        cor = ut_mix(kr=3, old_nw=2, old_line=True, old_ev=True, new_nw=4)
        chk('R37 ULPR-01 옛 단 줄 (n_windows 4) 이 옛 창 둘만 남긴 손상 기록 · RM 사건 → 새 시도 창 넷 뒤 TIMEOUT (단 줄이 새 창과 맞고 옛 창과는 다르다) → 버린 옛 단 끝 사건 '
            '(같은 k · step) = 옛 시도 단 줄 → 쓰지 않는다 = fresh 판정 (UNIDENTIFIED · 남긴 줄 3)',
            lambda: holds(cor, lambda u, s, g, rr: unid2(u, s, g, rr) and rr['n_superseded_rows'] == 3), show(cor))
        pl, pl_f = (ut_mix(NOC, kr=1, new_nw=4, new_line=True, next_nw=2),
                    ut_mix(NOC, kr=1, new_nw=4, new_line=True, next_nw=2, resumed=False))
        chk('R37 양성 대조: 새 시도 증거 = 경계 뒤 단 k 3 창 (k ≥ k_r + 2 — 옛 시도는 단 k_r + 1 줄만 남길 수 있다) · 단 끝 상태 파일 · 사건 없음 (지워진 restart 폴더 꼴) '
            '→ 단 k 2 단 줄 그대로 = fresh 와 같은 하한 (k 2) · 남긴 줄 0',
            lambda: holds(pl, lambda u, s, g, rr: holds(pl_f, lambda u2, s2, g2, rr2: u['primary_status'] == u2['primary_status'] == 'LOWER_BOUND'
                                                        and u['lower_bound_pct'] == u2['lower_bound_pct'] and ks(rr) == ks(rr2) == [0, 1, 2])
                          and rr['n_superseded_rows'] == 0), f'{show(pl)} | {show(pl_f)}')
        bad = ut_mix(kr=3, old_ev=True, new_nw=4, new_line=True, new_ev=True, rest=True)
        chk('R37 ULPR-01 모순: RESUME 앞에 경계 뒤 옛 사건 (RM) 이 있는데 옛 시도 창이 없다 (창 역행 없음) · 새 시도 기록은 있다 → 버리지 · 고르지 않고 주 값 미식별 '
            '(사유 ULPR-01) · UVa 거부',
            lambda: holds(bad, lambda u, s, g, rr: u['primary_status'] != 'OK' and u['rho_pct'] is None and any('ULPR-01' in w for w in u['why']) and not g[0]),
            show(bad))

        def gap_case():
            r = ut_mix(kr=1, old_nw=2, new_nw=4, new_line=True, new_ev=True, rest=True)
            if isinstance(r, Exception):
                return r
            d = r[3]['dir']
            try:
                _edit_rows(os.path.join(d, 'ul_windows.csv'), lambda rows: rows.remove([x for x in rows if x['k'] == '3' and x['w'] == '2'][-1]))
                return arm_verdict(d, B73, 'UT', P, root=root), selection_state(root, P), gate(root, B73, 'UVa', P), read_run(d, P)
            except Exception as ex:  # noqa: BLE001
                return ex
        gv = gap_case()
        chk('R37 ULPR-01 경계 뒤 단 줄 ↔ 그 단 창 기록 (n_windows · w 1 … n · 마지막 창 step) — 새 시도 단 k 3 의 창 w 2 줄 빠짐 → 시도 섞임 · 결손 = 주 값 미식별 '
            '(사유 ULPR-01) · UVa 거부',
            lambda: holds(gv, lambda u, s, g, rr: u['primary_status'] != 'OK' and any('ULPR-01' in w for w in u['why']) and not g[0]), show(gv))

        def sep_case():
            try:
                shutil.rmtree(os.path.join(root, B73, 'UB'), ignore_errors=True)
                st = _ladder(LAD[0], LAD[1]) + [{'lift_um': 0.4, 'P': 0.3, 'steady': True, 'nw': 4, 'kind': 'B', 'phase': 2, 'modeB': 1, 'n_move': 0},
                                                {'lift_um': 0.45, 'P': 0.2, 'steady': True, 'nw': 4, 'kind': 'B', 'phase': 2, 'modeB': 1, 'n_move': 0}]
                d = _mk_arm(root, B73, 'UB', {'W': 5000, 'dt': 1e-6, 'steps': st, 'summary': 'DONE', 'events': list(LAD[2])}, P)
                _resume_mix(d, P, kr=4, old_nw=2, old_events=[('SEPARATED', 2)], new_nw=4, new_line=True)
                return arm_verdict(d, B73, 'UB', P, root=root), read_run(d, P)
            except Exception as ex:  # noqa: BLE001
                return ex
        sv = sep_case()
        chk('R37 양성 대조: 분리 단 — 옛 시도 = 단 k 5 창 둘 + SEPARATED (창 사건 · 단 줄 없음) → RESUME (k 4) → 새 시도 = 창 넷 · 단 줄 (분리 없이 유지 끝) 뒤 k 6 이동 중 끝 '
            '→ 새 단 줄 그대로 (옛 창 둘 · SEPARATED 만 버림) · UB 주 값 OK',
            lambda: (not isinstance(sv, Exception) and sv[0]['primary_status'] == 'OK' and abs(sv[0]['rho_pct'] - 0.2026077873428664) < 1e-12
                     and ks(sv[1]) == [0, 1, 2, 3, 4, 5] and sv[1]['n_superseded_rows'] == 2 and not any(e['event'] == 'SEPARATED' for e in sv[1]['events'])),
            (f'{type(sv).__name__}: {sv}' if isinstance(sv, Exception) else
             f'{sv[0]["primary_status"]} k={ks(sv[1])} sup={sv[1]["n_superseded_rows"]} pr={sv[1]["problems"][:2]} why={sv[0]["why"][:2]}'))
    with tempfile.TemporaryDirectory() as root:
        # ── ULKRR-04 ID 형 · 필수 열 (팔 판독) — 소수 ID 를 정수로 자르지 않는다 · 열 결손 = 사유 있는 미식별 (예외 없음) ──
        def ub_id(edit=None):
            shutil.rmtree(os.path.join(root, B73), ignore_errors=True)
            d = _mk_arm(root, B73, 'UB', {'W': 5000, 'dt': 1e-6, 'steps': _ladder([0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4]), 'summary': 'DONE',
                                          'events': [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')]}, P)
            end = int([ln.split(',') for ln in open(os.path.join(d, 'ul_steps.csv')).read().splitlines()[1:]][2][6])
            if edit:
                edit(d, end)
            return arm_verdict(d, B73, 'UB', P, root=root)
        s0f = os.path.join(root, B73, 'in', f'atom_{P["beds"][B73]["s0"]}.liggghts')
        chk('R30 대조: 같은 UB 그대로 = OK', lambda: ub_id()['primary_status'] == 'OK')
        chk('R30 ULKRR-04 교차 끝점 원자 덤프 ID 2 → 2.5 (Codex parsing_fractional_atom_id) → 주 값 미식별 · 사유 = 정수 아님 (정수 2 로 자르지 않는다)',
            lambda: (lambda u: u['primary_status'] == 'UNIDENTIFIED' and u['rho_pct'] is None and any('정수' in w for w in u['why']))(
                ub_id(lambda d, e: _dump_field(os.path.join(d, 'dump', f'atom_{e}.dump'), 'id', 1, '2.5'))))
        chk('R30 ULKRR-04 교차 끝점 원자 덤프 머리 id → not_id (Codex parsing_missing_column) → 예외 없이 주 값 미식별 (사유)',
            lambda: (lambda u: u['primary_status'] == 'UNIDENTIFIED' and u['why'])(
                ub_id(lambda d, e: _dump_field(os.path.join(d, 'dump', f'atom_{e}.dump'), 'id', rename='not_id'))))
        chk('R30 ULKRR-04 교차 끝점 쌍 덤프 참조 ID (c_cpl[8] 2 → 2.5) → S3 NOT_COMPUTED → 주 값 미식별',
            lambda: (lambda u: u['primary_status'] == 'UNIDENTIFIED' and any('S3 NOT_COMPUTED' in w for w in u['why']))(
                ub_id(lambda d, e: _dump_field(os.path.join(d, 'dump', f'contact_{e}.dump'), 'c_cpl[8]', 0, '2.5'))))
        chk('R30 ULKRR-04 S0 원자 덤프 머리 id → not_id → 예외 없이 주 값 미식별 (S0 ID 집합 없음 — S3 NOT_COMPUTED)',
            lambda: ub_id(lambda d, e: _dump_field(s0f, 'id', rename='not_id'))['primary_status'] == 'UNIDENTIFIED')
    with tempfile.TemporaryDirectory() as root:
        # ── Q4 (가) 분리 · 분리 뒤 창 = 고유 · 연속 w + 그 팔 창 간격 (T_W 의 step) — 빈 구간 = 분리 연속 끊김 (Codex separation_missing_csv_window) ──
        def sep5(walls, nw, sev, edit=None):
            st = _ladder([0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4])
            st.append({'lift_um': 0.4, 'P': 0.0, 'steady': True, 'nw': nw, 'kind': 'B', 'phase': 2, 'modeB': 1, 'n_move': 0, 'wall': walls})
            shutil.rmtree(os.path.join(root, B73, 'UB'), ignore_errors=True)
            d = _mk_arm(root, B73, 'UB', {'W': 5000, 'dt': 1e-6, 'steps': st, 'summary': 'DONE',
                                          'events': [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')] + [(n, 5, w) for n, w in sev]}, P)
            if edit:
                edit(d)
            return arm_verdict(d, B73, 'UB', P, root=root)

        def okp(u):
            return u['primary_status'] == 'OK' and abs(u['rho_pct'] - 0.2026077873428664) < 1e-12

        def drop_w3(d):
            _edit_rows(os.path.join(d, 'ul_windows.csv'), lambda rows: rows.remove(next(r for r in rows if r['k'] == '5' and r['w'] == '3')))

        def shift_w3(d):   # w 는 연속인데 w 3 의 창 끝 step 만 + 1,000 (그 벽 덤프도 같은 step 으로 — 벽 결손이 아니라 간격만 틀림)
            box = {}

            def mv(rows):
                r = next(r for r in rows if r['k'] == '5' and r['w'] == '3')
                box['old'] = int(r['step'])
                r['step'] = str(box['old'] + 1000)
            _edit_rows(os.path.join(d, 'ul_windows.csv'), mv)
            src, dst = (os.path.join(d, 'dump', f'wall_{s}.dump') for s in (box['old'], box['old'] + 1000))
            os.rename(src, dst)
            _restep(dst, box['old'] + 1000)
        chk('R31 대조 (Q4 · 개정 3 §14-7): 예산 끝 선언 w 12 → POST_DONE w 15 (창 기록 연속 · 간격 = W) = DONE · 주 값 OK',
            lambda: (lambda u: okp(u) and u['trajectory_status'] == 'DONE' and u['separation']['declared_w'] == 12 and u['separation']['n_post'] == 4)(
                sep5([[-1.0]] * 10 + [[]] * 5, 15, (('SEPARATED', 'w12'), ('POST_DONE', 'w15')))))
        chk('R31 Q4 (가) 창 기록 w 3 빠짐 (w 1 · 2 · 4 · 5 · 6 · SEPARATED w2 · POST_DONE w6 — Codex separation_missing_csv_window) → DONE 아님 (SEP_INCOMPLETE) · 주 값 OK',
            lambda: (lambda u: okp(u) and u['trajectory_status'] == 'SEP_INCOMPLETE')(sep5([[]] * 6, 6, (('SEPARATED', 'w2'), ('POST_DONE', 'w6')), drop_w3)))
        chk('R31 Q4 (가) w 연속인데 창 간격 ≠ 그 팔 W (5,000 step) — w 3 창 끝 + 1,000 → SEP_INCOMPLETE · 주 값 OK',
            lambda: (lambda u: okp(u) and u['trajectory_status'] == 'SEP_INCOMPLETE')(sep5([[]] * 5, 5, (('SEPARATED', 'w2'), ('POST_DONE', 'w5')), shift_w3)))
        chk('R31 Q4 (가) separation(): 같은 k 안 w 1 · 2 · 4 (빈 구간) = w 2 선언이 끊김 (분리 뒤 창 초기화 · 최종 분리 아님) · 빈 구간 뒤 연속 두 0 창 (w 4 · 5) = '
            '새 선언 (w 5) · w 연속인데 간격 ≠ w_steps 도 끊김',
            lambda: (lambda a, a2, b: a['separated_final'] is False and a['gap_index'] == [2] and a['post_windows'] == []
                     and a2['gap_index'] == [2] and a2['declared_index'] == 3 and a2['post_windows'] == [3] and b['gap_index'] == [2])(
                separation([{'state': 'ZERO', 'step': 100 * w, 'k': 5, 'w': w, 'phase': 2} for w in (1, 2, 4)], 2, w_steps=100),
                separation([{'state': 'ZERO', 'step': 100 * w, 'k': 5, 'w': w, 'phase': 2} for w in (1, 2, 4, 5)], 2, w_steps=100),
                separation([{'state': 'ZERO', 'step': s, 'k': 5, 'w': w, 'phase': 2} for w, s in ((1, 100), (2, 200), (3, 350))], 2, w_steps=100)))
    with tempfile.TemporaryDirectory() as root:
        # ── Q5 문법 fixture PASS = 본 R · RJ2 · EXT 의 LIGGGHTS 전 사전 점검 (판정 JSON · 런 폴더 · 바이너리 · 덱 출처) — 1저자 10-14 강제 ──
        gfiles = {'in.hist_producer.liggghts': '# 합성 생산자 덱\n', 'in.hist_grammar.liggghts': '# 합성 문법 덱\n', 'plate_hist.stl': 'solid x\nendsolid x\n'}
        gpins = {n: ul_lib.sha256_bytes(t.encode()) for n, t in gfiles.items()}
        lsha = 'e' * 64

        def gp(mut=None, lmp=lsha, tag=None):
            base = os.path.join(root, tag or mut or 'ok')
            shutil.rmtree(base, ignore_errors=True)
            return grammar_prereq(_mk_gram(base, lsha, gfiles, mut), lmp, inputs=gpins)
        chk('R32 Q5 양성: 판정 PASS · rc 0 · 검사 19 전부 참 · 런 폴더 = 판정 폴더 · mode gram · end · LMP sha256 = 지금 바이너리 · 덱 둘 + 판 STL = 봉인 값 '
            '(단계 사본 · kit SHA256SUMS) → 허용', lambda: gp()[0] is True)
        for mut, what in (('absent', '판정 파일 없음'), ('bad_json', '판정 JSON 깨짐'), ('schema', 'schema 다름 (이력 시험 판정)'), ('status_fail', 'status FAIL · rc 2'),
                          ('rc_str', 'exit_code "0" (정수 아님)'), ('rc_bool', 'exit_code False (정수 아님)'), ('check_false', '검사 하나 거짓 (GB_tech)'),
                          ('check_missing', '검사 하나 없음 (GB_args)'), ('run_dir', '판정 run_dir ≠ 판정 파일 폴더'), ('mode', 'run_manifest mode=hist'),
                          ('no_end', 'run_manifest end 없음 (끝나지 않은 런)'), ('sums_sha', 'kit SHA256SUMS sha256 ≠ run_manifest sums_sha256'),
                          ('kit_deck', 'kit SHA256SUMS 의 문법 덱 sha256 ≠ 봉인 값'), ('no_kit', 'kit 폴더 없음'), ('stage_rc', 'GA rc 1'),
                          ('deck_copy', 'GB 덱 사본 ≠ 봉인 값'), ('deck_txt', 'GA deck.txt = 생산자 덱'), ('stl_copy', 'P 판 STL 사본 ≠ 봉인 값'),
                          ('no_stage', 'GB 단계 폴더 없음')):
            chk(f'R32 Q5 {what} → 거부 (사유)', lambda mut=mut: (lambda r: r[0] is False and bool(r[1]))(gp(mut)))
        chk('R32 Q5 지금 돌릴 바이너리 sha256 ≠ 문법 런 run_manifest lmp_sha256 → 거부', lambda: gp(lmp='f' * 64, tag='lmp')[0] is False)
        chk('R32 Q5 봉인 값 GRAMMAR_INPUTS = history_test 의 덱 둘 · 판 STL 의 실제 sha256 (039abb141 판 — 덱이 바뀌면 같은 묶음에서 고친다)',
            lambda: len(GRAMMAR_INPUTS) == 3 and GRAMMAR_INPUTS == {n: ul_lib.sha256_file(os.path.join(HERE, 'history_test', n)) for n in GRAMMAR_INPUTS})
        # ── Q3 (1저자 10-15 · Codex 수정 재확인 Q4 grammar_provenance) — 판정 JSON 대조에 더해 그 런 폴더 원자료를 승인된 판독기 (그 런 kit 사본의
        #    history_test/read_history.py --grammar · 봉인 sha256) 로 다시 읽어 검사 19 = JSON 이어야 통과 (JSON 만 반입해 실제 실행 PASS 를 인증하지 않는다) ──
        rh_t = _hist_reader()
        hsums = {}
        for ln in open(os.path.join(HERE, 'history_test', 'SHA256SUMS'), encoding='utf-8').read().splitlines():
            w_ = ln.split()
            if len(w_) == 2:
                hsums[w_[1]] = w_[0]
        rsha = ul_lib.sha256_file(os.path.join(HERE, 'history_test', 'read_history.py'))
        g_ok = gp(tag='q3_ok')
        chk('R36 Q3 양성: 원자료 = 승인된 판독기의 합성기 꼴 (그 판독기가 PASS 로 읽음) · kit 사본 판독기 · 표 = 봉인 값 → 사전 점검 허용 · 기록 = 원자료 재판독 '
            'PASS · 판독기 sha256 = 봉인 값 · 검사 19 = 판정 JSON',
            lambda: g_ok[0] is True and (g_ok[2].get('reread') or {}).get('status') == 'PASS' and (g_ok[2].get('reread') or {}).get('reader_sha256') == rsha
            and not (g_ok[2].get('reread') or {}).get('diff'), str(g_ok[1:])[:600])

        def raw_case(mut):
            r = gp(mut)
            raw = rh_t.grammar_info(os.path.join(root, mut, 'work', 'gram_20261014_000000'), rh_t.load_params())
            return r, raw
        for mut, what in (('raw_ga_error', 'GA 화면 끝에 ERROR 덧붙임 (Codex raw_ga_error_cached_pass)'),
                          ('raw_gb_mesh', 'GB 첫 판 mesh z → 99 (raw_gb_mesh_wrong_cached_pass)'),
                          ('raw_gb_screen', 'GB 화면 screen.out 지움 (raw_gb_screen_missing_cached_pass)'),
                          ('raw_gb_state', 'GB 마지막 상태 파일 값 0 (raw_gb_state_wrong_cached_pass)')):
            chk(f'R36 Q3 판정 JSON (PASS · 검사 19 참) 그대로 · {what} → 승인된 판독기로 다시 읽으면 FAIL · 검사 ≠ JSON → 사전 점검 거부 (사유 · 옛 판 = 허용)',
                lambda mut=mut: (lambda r, raw: raw['status'] == 'FAIL' and r[0] is False and any('재판독' in x for x in r[1]))(*raw_case(mut)))
        for mut, what in (('kit_reader', '그 런 kit 사본 판독기 고침 + kit SHA256SUMS · run_manifest sums_sha256 를 맞춤 (Codex different_reader_runner_seal — 옛 판 = 허용)'),
                          ('kit_params', '그 런 kit 사본 표 (history_params.json) 고침 + 봉인 맞춤'), ('kit_reader_missing', '그 런 kit 사본에 판독기 없음')):
            chk(f'R36 Q3 {what} → 승인된 판독기가 아니다 = 재판독하지 않고 사전 점검 거부 (사유)',
                lambda mut=mut: (lambda r: r[0] is False and any('판독기' in x for x in r[1]) and not (r[2].get('reread') or {}).get('status'))(gp(mut)))
        chk('R36 Q3 승인된 판독기 봉인 값 GRAMMAR_READER = history_test 의 read_history.py · history_params.json 실제 sha256 = history_test/SHA256SUMS 의 그 줄 '
            '(판독기 · 표가 바뀌면 같은 묶음에서 고친다)',
            lambda: set(GRAMMAR_READER) == set(_GRAM_TEST_READER_FILES)
            and all(GRAMMAR_READER[n] == ul_lib.sha256_file(os.path.join(HERE, 'history_test', n)) == hsums.get(n) for n in _GRAM_TEST_READER_FILES))
        # ── ULPR-02 (사전 리뷰 10-21 · 변이 생존) — Q3 재판독의 kit 목록 대조 · 프로세스 rc 조건 — 그 줄을 지우면 이 시험이 그 이유로 실패한다 ──
        g_ks = gp('kit_sums_reader')
        chk('R36 ULPR-02 그 런 kit 사본 판독기 = 봉인 바이트 그대로인데 그 런 kit SHA256SUMS 의 판독기 줄만 다른 값 (sums_sha256 맞춤 · 사전 리뷰 Q3a) → 목록 대조로 '
            '재판독하지 않고 사전 점검 거부 (사유 = 그 런 kit SHA256SUMS 의 read_history.py · 그 대조가 없으면 재판독 PASS 로 허용)',
            lambda: g_ks[0] is False and any('그 런 kit SHA256SUMS 의 read_history.py' in x for x in g_ks[1]) and not (g_ks[2].get('reread') or {}).get('status'),
            str(g_ks[1:])[:400])

        def fake_reread(rc):
            """재판독 rc 조건 시험 전용 — 판독기 자리에 시험 판독기 (PASS 판정 JSON (검사 19 참 · exit_code 0) 을 쓰고 rc 로 끝남) · readers 인자 = 그 두 파일 sha256
            (구현 봉인 GRAMMAR_READER 와 무관 — 승인 판정 뒤 rc 조건만 본다)."""
            fk = os.path.join(root, f'fake_reread_{rc}')
            os.makedirs(os.path.join(fk, 'run'), exist_ok=True)
            src = ('import json, sys\n'
                   'a = sys.argv\n'
                   'op = a[a.index("--out") + 1]\n'
                   'json.dump({"schema": ' + repr(GRAMMAR_SCHEMA) + ', "status": "PASS", "exit_code": 0, "checks": '
                   + repr({k: True for k in _GRAM_TEST_CHECKS}) + ', "problems": []}, open(op, "w"))\n'
                   f'sys.exit({rc})\n')
            _w(os.path.join(fk, 'read_history.py'), src)
            _w(os.path.join(fk, 'history_params.json'), '{}\n')
            rdr = {n: ul_lib.sha256_file(os.path.join(fk, n)) for n in _GRAM_TEST_READER_FILES}
            return _grammar_reread(os.path.join(fk, 'run'), fk, dict(rdr), {k: True for k in _GRAM_TEST_CHECKS}, readers=rdr)
        rr0, rr3 = fake_reread(0), fake_reread(3)
        chk('R36 ULPR-02 재판독 프로세스 rc ≠ 0 — 판독기가 PASS 판정 JSON (검사 19 참 · exit_code 0) 을 쓰고 rc 3 으로 끝남 → 재판독 문제 (rc 3 · 사유) · '
            '같은 판독기 rc 0 = 문제 없음 (rc 조건만 다르다 · 그 조건이 없으면 rc 3 도 통과)',
            lambda: rr0[0] == [] and rr0[1].get('rc') == 0 and rr0[1].get('status') == 'PASS' and rr3[1].get('rc') == 3 and any('rc 3' in x for x in rr3[0]),
            f'{rr0[0][:1]} {rr0[1].get("rc")} | {rr3[0][:1]} {rr3[1].get("rc")}')
    with tempfile.TemporaryDirectory() as root:
        # ── 중력 팔 복원 (choice C12) — R_M 의 setup (G1 · G2 · G2c) ↔ 출처 팔의 R_M 창 끝 (같은 머리 · run 0) ──
        src = _mk_arm(root, B73, 'UB', {'W': 5000, 'dt': 1e-6, 'steps': _ladder([0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4]),
                                        'events': [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')], 'summary': 'DONE'}, P)
        rm = int([ln.split(',') for ln in open(os.path.join(src, 'ul_events.csv')).read().splitlines() if ln.startswith('RM,')][0][2])
        gd = os.path.join(root, B73, 'G_UB')
        os.makedirs(os.path.join(gd, 'dump'))
        for nm in (f'atom_{rm}.dump', f'contact_{rm}.dump'):
            shutil.copy(os.path.join(src, 'dump', nm), os.path.join(gd, 'dump', nm))
        hdr = '    Step    Atoms         KinEng        ul_erot          ul_Ps       pressMPa            CPU \n'
        _w(os.path.join(gd, 'screen.txt'), 'LIGGGHTS-PUBLIC 3.8.0 (git 3d5c00f)\n' + hdr + f' {rm} 160417 1e-07 1e-08 0.0004 0.0004 0\n'
           'Loop time of 0 on 6 procs for 0 steps with 160417 atoms\n')
        R = P['records']
        _w(os.path.join(gd, 'ul_events.csv'), ','.join(R['events_cols']) + f'\nSTART,4,{rm},0.111402,0.00035,RM_branch\nGRAVITY_ON,0,{rm},0.111402,0.00035,g_aux\n'
           f'NO_BRACKET,0,{rm + 20000},0.111402,0.00035,le_Pmeas\n')
        _w(os.path.join(gd, 'ul_windows.csv'), ','.join(R['windows_cols']) + '\n')
        _w(os.path.join(gd, 'ul_steps.csv'), ','.join(R['steps_cols']) + '\n')
        _w(os.path.join(gd, 'run_manifest.txt'), f'source={src} rm_step={rm}\n')
        gv = None
        try:
            gv = arm_verdict(gd, B73, 'G_UB', P, root=root)
        except Exception:  # noqa: BLE001
            gv = None
        chk('R16 중력 팔 복원: R_M setup 줄 (KE · 원자) = 출처 팔 R_M 정규 줄 · G2 원자 · G2c 쌍 = 출처 팔 R_M 창 끝 덤프 → PASS · 판정 NO_BRACKET',
            lambda: gv['g_restore']['status'] == 'PASS' and gv['primary_status'] == 'NO_BRACKET')
        A = ul_lib.read_dump(os.path.join(gd, 'dump', f'atom_{rm}.dump'), 'custom')
        rows = A['rows']
        rows[0]['z'] += 1e-6
        ul_lib.write_custom(os.path.join(gd, 'dump', f'atom_{rm}.dump'), rm, A['cols'], rows)
        chk('R16 중력 팔 R_M 원자 하나 다름 → G2 FAIL → 복원 실패 = TECH (그 팔 값 없음)',
            lambda: (lambda g: g['g_restore']['status'] == 'FAIL' and g['primary_status'] == 'TECH')(arm_verdict(gd, B73, 'G_UB', P, root=root)))
        A0 = ul_lib.read_dump(os.path.join(src, 'dump', f'atom_{rm}.dump'), 'custom')
        ul_lib.write_custom(os.path.join(gd, 'dump', f'atom_{rm}.dump'), rm, A0['cols'], [dict(A0['rows'][0], x=A0['rows'][0]['x'] + 1e-3)] + A0['rows'])
        chk('R16 ULPR-03 중력 팔 R_M 원자 덤프에 같은 ID 두 줄 (첫 줄 x 다름 · 뒤 줄 = 출처 · 선언 수 = 행 수 — 옛 판 = 뒤 줄이 덮어 G2 PASS) → G2 관측 결손 '
            'NOT_COMPUTED (ID 중복) → 복원 PASS 아님 = TECH (C12)',
            lambda: (lambda g: g['g_restore'].get('G2') == 'NOT_COMPUTED' and g['g_restore']['status'] == 'FAIL' and g['primary_status'] == 'TECH')(
                arm_verdict(gd, B73, 'G_UB', P, root=root)))
        for p_ in (os.path.join(gd, 'dump', f'atom_{rm}.dump'), os.path.join(src, 'dump', f'atom_{rm}.dump')):   # 두 원자 덤프 = 같은 글자 · 머리 step 둘 다 R_M − 1
            ul_lib.write_custom(p_, rm - 1, A0['cols'], A0['rows'])
        chk('R16 ULPR-03 중력 팔 R_M 원자 덤프 두 개의 머리 step 이 서로 같지만 R_M − 1 (요청 step = R_M · START 사건) → G2 관측 결손 NOT_COMPUTED (머리 step) → TECH '
            '(요청 step 결합 · 서로 같다는 것만으로 PASS 하지 않는다)',
            lambda: (lambda g: g['g_restore'].get('G2') == 'NOT_COMPUTED' and g['primary_status'] == 'TECH')(arm_verdict(gd, B73, 'G_UB', P, root=root)))
    cc = None
    try:
        cc = {b: copy_commands(b, P) for b in BEDS}
    except Exception:  # noqa: BLE001
        cc = None
    chk('R15 원 파일 복사 명령 (침대마다 · 표에서): 체크포인트 · atom · contact · mesh · 원 로그 · 원 마지막 조각 덱 = cp -n 여섯 줄 · 10:0 = restart_settling_3600000 · 주소 · 사용자 이름 없음',
        lambda: all(len([x for x in cc[b] if x.startswith('cp -n ')]) == 6 for b in BEDS) and any('restart_settling_3600000.bin' in x for x in cc[B100])
        and not any(re.search(r'/home/|lustre|ibb-master|yonghoon', x) for b in BEDS for x in cc[b]))
    print(f'selftest: {"PASS" if not fails else "FAIL"} ({len(fails)} 실패)')
    return 1 if fails else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description='DEM 언로딩 키트 K4 읽는 쪽')
    ap.add_argument('cmd', nargs='?', choices=['inputs', 'restore', 'kebase', 's0p', 'arm', 'select', 'gate', 'report', 'copycmd', 'parentsums',
                                               'grammar'])
    ap.add_argument('args', nargs='*')
    ap.add_argument('--hist')
    ap.add_argument('--job', default='RJ')
    ap.add_argument('--lmp-sha', help='grammar: 지금 돌릴 LMP 바이너리 sha256 (문법 런의 바이너리와 같아야)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.cmd:
        ap.error('명령 (또는 --selftest)')
    if a.cmd == 'grammar':   # Q5 — 러너 사전 점검 (본 R · RJ2 · EXT 의 LIGGGHTS 전) · rc 0 허용 · 2 거부
        if len(a.args) != 1 or not a.lmp_sha:
            ap.error('grammar <…/gram_<시각>/grammar_verdict.json> --lmp-sha <지금 바이너리 sha256>')
        ok, pr, rec = grammar_prereq(a.args[0], a.lmp_sha)
        rr = rec.get('reread') or {}
        print(f'GRAMMAR_PREREQ status={"PASS" if ok else "REFUSE"} verdict={rec["verdict"]} verdict_sha256={rec["verdict_sha256"]} run_dir={rec["run_dir"]} '
              f'lmp_sha256={rec["lmp_sha256"]} grammar_deck_sha256={rec["grammar_deck_sha256"]} producer_deck_sha256={rec["producer_deck_sha256"]} '
              f'reread={rr.get("status")} reader_sha256={rr.get("reader_sha256")}'
              + ('' if ok else ' why=' + ' · '.join(pr[:6])))
        return 0 if ok else 2
    P = ul_lib.load_params()
    if a.cmd == 'copycmd':
        if len(a.args) != 1 or a.args[0] not in BEDS:
            ap.error('copycmd <침대>')
        print('\n'.join(copy_commands(a.args[0], P)))
        return 0
    if a.cmd == 'parentsums':
        if len(a.args) != 1 or not os.path.isdir(a.args[0]):
            ap.error('parentsums <부모 UT 런 폴더>')
        sys.stdout.write(parent_sums(os.path.abspath(a.args[0])))
        return 0
    need = {'inputs': 2, 'restore': 2, 'kebase': 2, 's0p': 1, 'arm': 3, 'select': 1, 'gate': 3, 'report': 1}[a.cmd]
    if len(a.args) != need:
        ap.error(f'{a.cmd}: 인자 {need} 개')
    root = os.path.abspath(a.args[0])

    def dump(obj, path=None):
        txt = json.dumps(obj, ensure_ascii=False, indent=1, default=lambda o: sorted(o) if isinstance(o, set) else str(o))
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(txt + '\n')
        return txt

    if a.cmd == 'inputs':
        r = inputs_check(root, a.args[1], P)
        print(dump(r))
        return 0 if r['ok'] else 2
    if a.cmd == 'restore':
        r = restore_verdict(root, a.args[1], a.job, a.hist, P)
        dump(r, os.path.join(root, a.args[1], a.job, 'restore_verdict.json'))
        print(f'RESTORE_VERDICT bed={a.args[1]} job={a.job} status={r["status"]} ' +
              ' '.join(f'{k}={(v.get("status") or v.get("ok") or v.get("seen") or v.get("pass"))}' for k, v in r['checks'].items()))
        return 0 if r['status'] == 'RESTORED' else 2
    if a.cmd == 'kebase':
        k = kebase(root, a.args[1], P)
        print(f'KE_BASE bed={a.args[1]} trans={k["trans"]} rot={k["rot"]} s2_limit={k["s2_limit"]}'
              + ('' if k['s2_limit'] is not None else f' — 기준 파일 미발행: {" · ".join(k["problems"][:4]) or "병진 · 회전 기준 없음"}'))
        return 0 if k['s2_limit'] is not None else 2
    if a.cmd == 's0p':
        r = s0p_decision(root, P)
        print(f'S0P status={r["status"]} s0={r["s0"]} tried={r["tried"]}')
        return 0 if r['status'] == 'PASS' else 2
    if a.cmd == 'arm':
        bed, job = a.args[1], a.args[2]
        r = arm_verdict(os.path.join(root, bed, job), bed, job, P, root=root)
        dump(r, os.path.join(root, bed, job, 'arm_verdict.json'))
        print(f'ARM_VERDICT bed={bed} job={job} primary={r["primary_status"]} rho_pct={r["rho_pct"]} bracket_pct={r["bracket_pct"]} '
              f'trajectory={r["trajectory_status"]} cancellation={r["cancellation"]} nonmonotone={r["nonmonotone"]} why={" · ".join(r["why"])}')
        return 0
    if a.cmd == 'select':
        s = selection_state(root, P)
        dump(s, os.path.join(root, B73, 'selection.json'))
        print(f'SELECTION stage={s["stage"]} delta_dt={s["delta_dt"]} delta_v={s["delta_v"]} dt_star={s["dt_star"]} tuple={s["tuple"]} '
              f'arm={s["arm"]} next={s["next"]} why={" · ".join(s["why"])}')
        return 0
    if a.cmd == 'gate':
        ok, why = gate(root, a.args[1], a.args[2], P)
        print(f'GATE bed={a.args[1]} job={a.args[2]} {"ALLOW" if ok else "REFUSE"} — {why}')
        return 0 if ok else 2
    r = report(root, P)
    dump(r, os.path.join(root, 'report.json'))
    print(f'REPORT selection={r["selection"]["stage"]} tuple={r["selection"]["tuple"]} pairs={[(x["a"], x["b"], x["relation"]) for x in r["pairs"]]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
