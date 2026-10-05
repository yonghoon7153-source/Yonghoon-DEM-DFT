#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""믹서 정확 좌표 프레임 — 체크포인트 (double) 에서 `run 0` 으로 보조 판독량 s1 · s2 의 덤프 해상도 보충 (2026-10-05 · 강성 축 사전등록 §12-4 (나)).

    python3 scripts/mixer_exact_frames.py deck <런 디렉터리> --ckpt {settled,a,b} --work <새 디렉터리>   # 덱 · 영수증 · sbatch · 입력 링크
    (ibb)   cd <새 디렉터리> && srun -p cpu --qos cpu-60 -n 1 -t 00:20:00 <lmp_mpi> -in in.exact > log.exact 2>&1   # deck 이 정확한 줄을 찍는다
    python3 scripts/mixer_exact_frames.py read <런 디렉터리> <hp 덤프> [<hp 덤프> …] [--g6 <g6 덤프> …] --json out.json
    python3 scripts/mixer_exact_frames.py --selftest

━━ 왜 (1저자 10-05 *"가,다 하고 나도 해당 방법으로 진행해보자"* 의 (나)) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  보조 판독기 (scripts/mixer_contact_reader.py — s1 SE–SE 접촉 군집 · s2 AM–SE 부착) 는 런의 덤프를 읽는다.  덱의 `dump dmp` 에 dump_modify format 이
  없어 좌표가 LIGGGHTS 기본 `%g` (6 유효숫자 · 반폭 ≤ 5e-8 m) 이고, 시험 운전 (docs/data/mixer_contact_reader_refs_20261005/) 에서 LC · E0 의 s1 범위
  [확실, 가능] 이 [0, 1] 의 대부분이었다.  체크포인트 (restart 파일) 는 위치를 **double** 로 담는다 → 그것을 읽어 `run 0` (적분 없음) 으로 같은 step 의
  덤프를 두 벌 (hp = `%.17g` · g6 = 기본 `%g`) 쓰면, **같은 배치**에서 셋을 나란히 잰다:
    (i)   정확 — hp 의 double 좌표에 등록 규칙 (판독기 frame_quantities 그대로).  범위가 접힌다: 좌표 반폭 ~1e-15 m (판독기 유효숫자 상한 13) ·
          반경 = 계획 템플릿 상수의 double (비트 같음 — `radius constant` 라 반올림 없음) → 반경 반폭 0 (판독기 classify_pairs · ambiguous_at_hp).
          ⚠ 판독기 규칙을 hp 에 그대로 적용한 범위 (reader_resolution_on_hp · 진단) 는 반경 자릿수 바닥 (S = max(관측, 6) → 반경 반폭
          SE 5e-11 · AM 5e-10 m) 안의 접촉 (겹침 < 0.1 · 0.55 nm) 에서 열릴 수 있다 — 좌표 반올림이 아니라 그 규칙 탓 (셀프테스트 ㉘).
    (ii)  등록 규칙 @ %g — hp 값을 파이썬 '%g' 로 반올림한 좌표 · 반경 (판독기가 런 덤프에서 보는 것) + 그 [확실, 가능].
    (iii) (--g6) 에뮬레이션 문자열 = LIGGGHTS 자신의 `%g` 텍스트 (원자마다 x y z radius) — 하나라도 다르면 TECH.
  ⇒ 덤프 해상도가 그 런에서 실제로 무엇을 가렸는지 (등록 값 ↔ 참 값 · 놓친 접촉 · 없는데 센 접촉) 를 직접 본다.

━━ 지위 (§12-4 (나) — LU 열람 전 등록) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  **보고 전용 · 관문 아님 · 정의 불변** (s1 · s2 · 접촉 = rsq < (r_i + r_j)² 엄격).  등록 프레임 (계획 t₀ 덤프 · bin 1 덤프 격자) 을 대신하지 않는다 —
  체크포인트 step 은 등록 프레임이 아니다.  프레임 = `restart/settled.bin` (정착 끝 = 1 + 2·정착 step — 캠페인 덱이면 등록 t₀ 덤프 1,037,408 + 21 step)
  + 마지막 두 체크포인트 (`a.bin` · `b.bin` 은 `restart N` 이 번갈아 쓴다 — 완주한 2 바퀴 런 (끝 7,139,962) 이면 6,800,000 · 7,000,000 = 둘 다 bin 1 안 ·
  어느 파일이 어느 step 인지는 체크포인트 머리에서 읽는다).  M 없음 — 칸 분산 · 혼합 지수를 계산하지 않는다 (가져오는 판독기 함수 = 프레임 선택뿐).

━━ deck — 덱 변환 (make_mixer_resume.transform 을 그대로 부른다 · CLI 는 부르지 않는다) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  원 in.mixer → transform (create_box → `read_restart <절대경로>` + step 출력 · 삽입 · 템플릿 · 분포 · 그 region · unfix · write_restart · shell mkdir ·
  앞쪽 run 삭제) → 여기서 더 지운다: 원 dump (dmp) · 그 dump_modify · undump · `restart` → 마지막 run 자리에 hp · g6 dump + `run 0`.
  재료 · 접촉 · 메시 · 벽 · 적분 · thermo · move/mesh 는 글자 그대로 (transform 이 남긴 그대로).
  ⛔ **런 폴더에는 아무것도 쓰지 않는다** — make_mixer_resume 의 CLI (prepare) 는 체크포인트를 복사하고 덤프를 옮기므로 부르지 않는다.  새 작업 폴더
  (비었거나 없을 것 · 런 폴더와 서로 포함 관계 아님) 에 덱 (in.exact) · 영수증 (exact_receipt.json — 체크포인트 sha256 · 머리 step · 덱 sha256) ·
  sbatch (run_exact.sbatch) · 덱이 읽는 입력 (STL) 의 심볼릭 링크 · 빈 exact/ 를 만든다.
  체크포인트 머리 = LIGGGHTS-PUBLIC 3.x write_restart.cpp header() (매직 없음 · 플래그 int + 값: VERSION · SMALLINT · TAGINT · BIGINT · UNITS · NTIMESTEP ·
  DIMENSION · NPROCS …) — 공개 소스 3d5c00f 판독.  못 읽으면 step 미상으로 덱은 만들고 (경고) read 가 덤프 TIMESTEP · 로그의 EXACT_STEP 으로만 잇는다.
  ⚠ hp 의 `dump_modify … format "…"` 는 LIGGGHTS 옛 문법 (생성기 dump_modify_format 과 같은 규칙) — **ibb 바이너리 실측 전**.  적용이 안 되면 hp 토큰이
  %.17g 가 아니어서 read 가 TECH 로 멈춘다 (조용히 %g 를 정확 값으로 읽지 않는다).

━━ read — 검사 (어긋나면 TECH · 값 없음) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  판독기 phase_map (deck_meta · 템플릿 반경) · frame_plan (계획 t₀ 덤프 = 원자 기준) · hp 열 = id type x y z radius · hp 토큰 = 정확히 `%.17g` ·
  원자 (id, type) = 런의 t₀ 덤프 · 반경 = 계획 (frame_quantities) · = t₀ 덤프 (%g) · t₀ 원자 수 = n_atoms_planned (판독기와 같은 규칙) ·
  영수증 (같은 런 폴더 · in.exact sha256 · 체크포인트 sha256 다시 계산 · 머리 step = 덤프 TIMESTEP · 로그 EXACT_STEP = TIMESTEP) · g6 (있으면) ·
  불변식 확실 ≤ 정확 ≤ 가능 (스칼라 · 접촉 수 — 어기면 도구 결함) · 접촉 쌍 독립 재계수 = 판독기 수.
  bin = 판독기 bin 식 (measure_mixing_index.bin_of) — 체크포인트 step 이 등록 bin 1 창 안인지 · 덤프 격자 위인지 적는다.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shlex
import struct
import sys
import time
from datetime import datetime, timezone

import numpy as np
from scipy.spatial import cKDTree

_SCR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCR)
import mixer_contact_reader as R                                                          # noqa: E402  phase_map · frame_plan · frame_quantities
from mixer_contact_reader import Tech, Undefined, S1_KEYS, S2_KEYS, AM_PHASES             # noqa: E402
import make_mixer_resume as _mmr                                                          # noqa: E402
from make_mixer_resume import transform, logical_commands, _tokens, deck_params           # noqa: E402  캠페인 재개와 같은 변환 · CLI 는 안 부른다
from make_mixer_deck import dump_modify_format                                            # noqa: E402  (다) 와 같은 형식 규칙
#  ★ 판독기 (measure_mixing_index) 에서는 프레임 선택 · bin 식만 (M · 칸 분산 함수는 가져오지 않는다 — 셀프테스트 ㉒)
from measure_mixing_index import deck_plan, planned_t0, bin_of                            # noqa: E402
from measure_bed_aspect import validate_frame, read_dump                                  # noqa: E402

SCHEMA = 'mixer_exact_frames/1'
DECK_SCHEMA = 'mixer_exact_frames_deck/1'
REGISTERED = 'docs/reviews/mixer_highbo_stiffness_prereg_20260929.md §12-4 (나) — 보고 전용 · 관문 아님 · 정의 불변'
CKPTS = ('settled', 'a', 'b')
DECK_FILE, RECEIPT_FILE, SBATCH_FILE, OUT_SUB = 'in.exact', 'exact_receipt.json', 'run_exact.sbatch', 'exact'
HP_COLS = ('id', 'type', 'x', 'y', 'z', 'radius')
FLOAT_COLS = ('x', 'y', 'z', 'radius')
STEP_TAG = 'EXACT_STEP'
LMP_DEFAULT = '/lustre/home/yonghoon/LIGGGHTS-PUBLIC/src/lmp_mpi'
#: ibb SLURM 기본값 — 런처 (launch_highbo.sh) 의 SB_PARTITION · SB_QOS · SB_ENV · MPIRUN_FLAGS 와 같다.  런의 launch_record.json 이 있으면 그 값을 쓴다.
SLURM_DEFAULT = dict(partition='cpu', qos='cpu-60', time='00:20:00', conda_env='myenv', path_prefix='',
                     mpirun_flags='--oversubscribe --bind-to none')
#: measure_mixing_index 에서 가져와도 되는 이름 (M 없음 — 셀프테스트 ㉒)
FRAME_TOOL_NAMES = frozenset({'deck_plan', 'planned_t0', 'bin_of'})
#: LIGGGHTS 입력 · 파일명에서 뜻이 있는 글자 (공백 · % = 다중 파일 · * = step · $ = 변수 · # = 주석 · 따옴표 · & = 줄 잇기)
UNSAFE_PATH = re.compile(r'[\s%*$#"\'&;]')
#: write_restart.cpp header() 의 처음 여덟 항목 (enum 순서 그대로)
_HDR = ('VERSION', 'SMALLINT', 'TAGINT', 'BIGINT', 'UNITS', 'NTIMESTEP', 'DIMENSION', 'NPROCS')
NOTE = ('보고 전용 — 관문 아님 · 정의 불변 (§12-4 (나)).  체크포인트 프레임은 등록 프레임 (t₀ 덤프 · bin 1 격자) 이 아니다.  '
        'exact = double 좌표 (collapsed · ambiguous_at_hp = hp 정밀도 · 반경 = 계획 double) · rounded = 같은 배치를 %g 로 반올림한 좌표에 '
        '등록 규칙 + [확실 lo, 가능 hi] (판독기 규칙 그대로) · exact.reader_resolution_on_hp = 진단 (판독기 반경 자릿수 바닥 포함)')


def _sha_file(path):
    return R._sha_file(path)


# ═════════════════════════════ 체크포인트 · 덱 ═════════════════════════════
def restart_header(path, nbytes=4096):
    """체크포인트 머리 → dict(version, sizes, units, ntimestep, dimension, nprocs).

    LIGGGHTS-PUBLIC 3.x (공개 소스 3d5c00f) write_restart.cpp header(): 매직 없이 처음부터 (플래그 int32 · 값) — VERSION (int n + 문자 n 개 · NUL 포함) ·
    SMALLINT · TAGINT · BIGINT (크기 int) · UNITS (문자열) · NTIMESTEP (bigint) · DIMENSION · NPROCS (int) … · x86 = little-endian.
    플래그 순서 · 크기가 어긋나면 ValueError — step 을 추정하지 않는다."""
    with open(path, 'rb') as f:
        buf = f.read(nbytes)
    pos = 0

    def take(n):
        nonlocal pos
        if n < 0 or pos + n > len(buf):
            raise ValueError(f'머리가 짧다 ({len(buf)} B) — LIGGGHTS 3.x restart 머리가 아니다')
        b = buf[pos:pos + n]
        pos += n
        return b

    def i32():
        return struct.unpack('<i', take(4))[0]

    def flag(k):
        f_ = i32()
        if f_ != k:
            raise ValueError(f'머리 플래그 {f_} ≠ {k} ({_HDR[k]}) — LIGGGHTS 3.x restart 머리가 아니다')

    def text():
        n = i32()
        if not 0 < n <= 1024:
            raise ValueError(f'머리 문자열 길이 {n} — LIGGGHTS 3.x restart 머리가 아니다')
        b = take(n)
        if b[-1:] != b'\0':
            raise ValueError('머리 문자열이 NUL 로 끝나지 않는다')
        return b[:-1].decode('ascii', errors='replace')

    flag(0)
    version = text()
    flag(1)
    smallint = i32()
    flag(2)
    tagint = i32()
    flag(3)
    bigint = i32()
    if bigint not in (4, 8):
        raise ValueError(f'머리 bigint 크기 {bigint}')
    flag(4)
    units = text()
    flag(5)
    step = struct.unpack('<q' if bigint == 8 else '<i', take(bigint))[0]
    flag(6)
    dim = i32()
    flag(7)
    nprocs = i32()
    if step < 0 or dim not in (2, 3) or nprocs < 1:
        raise ValueError(f'머리 값이 이상하다 (step {step} · dimension {dim} · nprocs {nprocs})')
    return dict(version=version, sizes=dict(smallint=smallint, tagint=tagint, bigint=bigint), units=units,
                ntimestep=int(step), dimension=int(dim), nprocs=int(nprocs))


def restart_files(deck_text):
    """덱 → ({'settled': write_restart 파일, 'a': restart 첫 파일, 'b': 둘째}, restart 간격) — 상대 경로 그대로 (덱이 런 폴더에서 돈다).
    `restart N a b` · `thermo N` 이 하나씩이 아니면 make_mixer_resume.deck_params 가 거부한다."""
    every, fa, fb, _ = deck_params(deck_text)
    wr = [t for t in (_tokens(b) for _, b in logical_commands(deck_text)) if t[:1] == ['write_restart']]
    if len(wr) != 1 or len(wr[0]) != 2:
        raise SystemExit(f'⛔ 덱의 write_restart 가 {len(wr)} 줄 — settled 체크포인트를 정할 수 없다')
    return dict(settled=wr[0][1], a=fa, b=fb), int(every)


def deck_inputs(text):
    """덱이 읽는 입력 파일 (명령의 `file <경로>` — mesh/surface STL 등) · 순서대로 중복 없이."""
    out = []
    for _, b in logical_commands(text):
        t = _tokens(b)
        for k, tok in enumerate(t[:-1]):
            if tok == 'file' and t[k + 1] not in out:
                out.append(t[k + 1])
    return out


def exact_deck(deck_text, ckpt_abs, label, step=None, run_name=''):
    """원 덱 → (정확 좌표 덱 텍스트, info{dropped, inputs}).  거부 = SystemExit.

    make_mixer_resume.transform 을 **그대로** 부른 뒤 (create_box → read_restart · 삽입 · 템플릿 · 분포 · 그 region · unfix · write_restart ·
    shell mkdir · 앞쪽 run 삭제 · 재료 · 접촉 · 메시 · 벽 · 적분 · thermo · move/mesh 는 글자 그대로) 여기서 더 바꾼다:
      원 dump · 그 dump_modify · undump · `restart` 삭제 · step 변수 · 출력 이름 (RESUME_STEP → EXACT_STEP) · 마지막 run → hp · g6 dump + `run 0`."""
    if label not in CKPTS:
        raise SystemExit(f'⛔ ckpt {label!r} — {CKPTS} 중 하나')
    if not os.path.isabs(ckpt_abs):
        raise SystemExit(f'⛔ 체크포인트 경로 {ckpt_abs!r} 가 절대경로가 아니다 — 덱은 작업 폴더에서 돌므로 절대경로로 읽는다')
    if UNSAFE_PATH.search(ckpt_abs):
        raise SystemExit(f'⛔ 체크포인트 경로 {ckpt_abs!r} 에 LIGGGHTS 가 뜻을 붙이는 글자 (공백 · % · * · $ · # · 따옴표 · & · ;) — 쓰지 않는다')
    base, info = transform(deck_text, ckpt_abs, 0)
    L = base.split('\n')
    if not (len(L) > 3 and L[0].startswith('# ⚠ 재개 덱') and L[1].startswith('#   체크포인트') and L[2].startswith('#   원 덱과 다른 곳')):
        raise SystemExit('⛔ make_mixer_resume.transform 의 머리가 예상과 다르다 — 변환 규칙이 바뀌었는지 확인하기 전에는 쓰지 않는다')
    cmds = logical_commands('\n'.join(L[3:]))                              # transform 의 머리 세 줄 (재개 목표 step) 은 이 덱에 맞지 않는다
    toks = [_tokens(b) for _, b in cmds]
    dump_ids = {t[1] for t in toks if t[:1] == ['dump'] and len(t) > 1}
    hp_fmt = dump_modify_format(HP_COLS)
    out, dropped, seen = [], [], dict(run=0, variable=0, print=0)
    for (_, block), t in zip(cmds, toks):
        kw = t[0] if t else ''
        if kw in ('restart', 'dump') or (kw in ('dump_modify', 'undump') and len(t) > 1 and t[1] in dump_ids):
            dropped.append(' '.join(t))
            continue
        if kw == 'variable' and t[1:] == ['resume_step', 'equal', 'step']:
            seen['variable'] += 1
            out.append('variable        exact_step equal step')
            continue
        if kw == 'print' and len(block) == 1 and 'RESUME_STEP' in block[0]:
            seen['print'] += 1
            out.append(f'print           "{STEP_TAG} ${{exact_step}} ckpt {label}"')
            continue
        if kw == 'run':
            seen['run'] += 1
            dropped.append(' '.join(t))
            out += ['# ★ 정확 좌표 덤프 — 같은 step 두 벌: hp = %.17g (double 왕복 · 정확 값) · g6 = LIGGGHTS 기본 %g (판독기가 런 덤프에서 보는 형식 · '
                    '에뮬레이션 대조)',
                    '#   ⚠ dump_modify format = LIGGGHTS-PUBLIC 3.x 옛 문법 (한 줄 형식 · 공개 소스 판독 · 바이너리 실측 전) — 안 먹으면 read 가 TECH',
                    f'dump hp all custom 1 {OUT_SUB}/hp_*.liggghts {" ".join(HP_COLS)}',
                    f'dump_modify hp format "{hp_fmt}"',
                    f'dump g6 all custom 1 {OUT_SUB}/g6_*.liggghts {" ".join(HP_COLS)}',
                    '# run 0 = 적분 없음 — 덤프의 위치 = 체크포인트의 double 그대로',
                    'run 0']
            continue
        out.extend(block)
    if seen != dict(run=1, variable=1, print=1):
        raise SystemExit(f'⛔ transform 출력 모양이 예상과 다르다 {seen} — run · step 변수 · 출력이 하나씩이어야 한다')
    hdr = [f'# 정확 좌표 프레임 덱 — scripts/mixer_exact_frames.py 가 {run_name or "런"}/in.mixer 에서 만들었다 (손으로 고치지 말 것 · '
           '강성 축 사전등록 §12-4 (나) · 보고 전용)',
           f'#   체크포인트 {label} = {ckpt_abs} · 머리 step {step if step is not None else "미상"} · run 0 (적분 없음)',
           '#   원 덱과 다른 곳: make_mixer_resume.transform (create_box → read_restart · 삽입 · 템플릿 · 분포 · write_restart · shell mkdir · 앞쪽 run 삭제)',
           '#   + 원 dump · restart 삭제 · 마지막 run → hp (%.17g) · g6 (기본 %g) dump + run 0 · ⛔ 출력은 이 작업 폴더 (exact/) 에만 — 런 폴더에 쓰지 않는다']
    text = '\n'.join(hdr + out).rstrip('\n') + '\n'
    return text, dict(dropped=list(info['dropped']) + dropped, inputs=deck_inputs(text))


def _launch_env(run, lmp, slurm):
    """바이너리 · SLURM 값 — 명령 인자 > 런의 발사 봉인 (launch_record.json — 같은 바이너리 · 같은 환경) > 기본값."""
    rec = {}
    lr = os.path.join(run, 'launch_record.json')
    if os.path.isfile(lr):
        try:
            with open(lr, encoding='utf-8') as f:
                rec = json.load(f)
        except (OSError, ValueError):
            rec = {}
    env = dict(SLURM_DEFAULT)
    sl = rec.get('slurm') if isinstance(rec.get('slurm'), dict) else {}
    for k in ('partition', 'qos', 'conda_env', 'path_prefix', 'mpirun_flags'):
        if isinstance(sl.get(k), str) and (sl[k] or k == 'path_prefix'):
            env[k] = sl[k]
    for k, v in (slurm or {}).items():
        if v is not None:
            env[k] = v
    path = lmp or rec.get('lmp_realpath') or rec.get('lmp_path') or LMP_DEFAULT
    sha = _sha_file(path) if os.path.isfile(path) else None
    seal = rec.get('lmp_sha256')
    return env, dict(path=path, source='--lmp' if lmp else ('launch_record.json' if rec.get('lmp_realpath') or rec.get('lmp_path') else 'default'),
                     sha256=sha, run_seal_sha256=seal, matches_run_seal=(sha == seal) if (sha and seal) else None)


def _sbatch_text(work, run_name, label, env, lmp):
    L = ['#!/bin/bash',
         f'#SBATCH --job-name=exact_{label}_{run_name[:40]}',
         f'#SBATCH --output={work}/slurm_exact_%j.out',
         f'#SBATCH --qos={env["qos"]}',
         f'#SBATCH --partition={env["partition"]}',
         '#SBATCH -n 1',
         f'#SBATCH --time={env["time"]}',
         '# 정확 좌표 프레임 (scripts/mixer_exact_frames.py deck 이 썼다 · 강성 축 사전등록 §12-4 (나)) — 고치지 말 것 (영수증이 sha256 을 적는다)',
         '# ⛔ 원 런 폴더에는 쓰지 않는다: cwd = 이 작업 폴더 · 체크포인트는 read_restart 로 읽기만 · 형식 = 재개-위상 영수증 job 235118 과 같은 mpirun -np 1',
         '']
    if env.get('conda_env'):
        L += ['source ~/.bashrc', f'conda activate {env["conda_env"]}']
    if env.get('path_prefix'):
        L.append(f'export PATH={shlex.quote(env["path_prefix"])}:$PATH')
    L += [f'cd {shlex.quote(work)} || exit 3',
          f'mpirun {env["mpirun_flags"]} -np 1 {shlex.quote(lmp)} -in {DECK_FILE} > log.exact 2>&1']
    return '\n'.join(L) + '\n'


def _where(step, t0, spr, de, rot):
    """체크포인트 step 의 자리 — (bin · 등록 bin 1 창 안 · t₀ 와의 차 · 덤프 격자 위)."""
    if step is None:
        return dict(bin=None, in_bin1=False, step_minus_t0=None, on_dump_lattice=None)
    b = bin_of(step, t0, spr) if rot else None
    return dict(bin=b, in_bin1=bool(rot and b == R.REG_BIN), step_minus_t0=int(step - t0),
                on_dump_lattice=bool(step >= t0 and (step - t0) % de == 0))


def _where_txt(w, t0, rot):
    if w['step_minus_t0'] is None:
        return 'step 미상 (머리를 못 읽었다)'
    rel = f't₀ {t0:,} {"+" if w["step_minus_t0"] >= 0 else "−"} {abs(w["step_minus_t0"]):,} step'
    lat = '덤프 격자 위' if w['on_dump_lattice'] else '덤프 격자 밖'
    if not rot:
        return f'회전 없음 (E0) · {rel} · {lat}'
    return f'bin {w["bin"]}{" = 등록 bin 1 창 안" if w["in_bin1"] else ""} · {rel} · {lat} (등록 프레임이 아니다)'


def build_deck(run_dir, ckpt, work, lmp=None, slurm=None, quiet=False):
    """deck 명령 — 작업 폴더에 덱 · 영수증 · sbatch · 입력 링크 · 빈 exact/.  거부 = SystemExit (**아무것도 쓰기 전**).  반환 = 영수증 dict."""
    if ckpt not in CKPTS:
        raise SystemExit(f'⛔ --ckpt {ckpt!r} — {CKPTS} 중 하나')
    run = os.path.realpath(run_dir)
    deck_path = os.path.join(run, 'in.mixer')
    if not os.path.isfile(deck_path):
        raise SystemExit(f'⛔ {run_dir}: in.mixer 없음')
    try:
        pm = R.phase_map(run)                                              # deck_meta · deck_sha256 · 템플릿 반경 (판독기와 같은 확인)
    except Tech as e:
        raise SystemExit('⛔ 런 폴더 검사 (판독기 phase_map) 실패: ' + ' · '.join(e.reasons))
    with open(deck_path, encoding='utf-8', errors='replace') as f:
        deck_text = f.read()
    files, every = restart_files(deck_text)
    ck = os.path.realpath(os.path.join(run, files[ckpt]))
    if not os.path.isfile(ck) or os.path.getsize(ck) == 0:
        raise SystemExit(f'⛔ 체크포인트 {ckpt} = {os.path.join(run, files[ckpt])} 가 없거나 비었다')
    try:
        hdr, hdr_err = restart_header(ck), None
    except (ValueError, OSError) as e:
        hdr, hdr_err = None, str(e)
    step = hdr['ntimestep'] if hdr else None
    plan = deck_plan(deck_path)
    t0, spr, de, rot = planned_t0(plan), plan['steps_per_rev'], plan['dump_every'], plan['steps_run'] > 0
    total = plan['steps_total']
    settled = total - plan['steps_run']                                    # write_restart 는 정착 두 run 뒤 · 회전 앞 (1 + 2·정착)
    last2 = [every * k for k in (total // every - 1, total // every) if k > 0]
    text, info = exact_deck(deck_text, ck, ckpt, step=step, run_name=os.path.basename(run))
    bad = [f_ for f_ in info['inputs'] if os.path.isabs(f_) or '..' in f_.split('/') or not os.path.exists(os.path.join(run, f_))]
    if bad:
        raise SystemExit(f'⛔ 덱 입력 {bad} 이 런 폴더에 없다 (또는 절대 · 상위 경로) — 작업 폴더에 링크할 수 없다')
    w = os.path.abspath(work)
    wr = os.path.realpath(w)
    if wr == run or wr.startswith(run + os.sep) or run.startswith(wr + os.sep):
        raise SystemExit(f'⛔ 작업 폴더 {work} 가 런 폴더 {run} 와 같거나 서로 안에 있다 — 런 폴더에는 아무것도 쓰지 않는다')
    if os.path.lexists(w) and (not os.path.isdir(w) or os.listdir(w)):
        raise SystemExit(f'⛔ 작업 폴더 {work} 가 비어 있지 않다 (또는 파일이다) — 덮지 않는다 (새 폴더를 준다)')
    env, binary = _launch_env(run, lmp, slurm)
    where = _where(step, t0, spr, de, rot)
    #  ── 여기부터 쓴다 (작업 폴더에만) ──
    os.makedirs(wr, exist_ok=True)
    os.mkdir(os.path.join(wr, OUT_SUB))
    with open(os.path.join(wr, DECK_FILE), 'w', encoding='utf-8') as f:
        f.write(text)
    links = {}
    for f_ in info['inputs']:
        dst = os.path.join(wr, f_)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        src = os.path.realpath(os.path.join(run, f_))
        os.symlink(src, dst)
        links[f_] = src
    sb = _sbatch_text(wr, os.path.basename(run), ckpt, env, binary['path'])
    with open(os.path.join(wr, SBATCH_FILE), 'w', encoding='utf-8') as f:
        f.write(sb)
    srun = (f'cd {shlex.quote(wr)} && srun -p {env["partition"]} --qos {env["qos"]} -n 1 -t {env["time"]} '
            f'{shlex.quote(binary["path"])} -in {DECK_FILE} > log.exact 2>&1')
    stp = step if step is not None else '<step>'
    nxt = (f'python3 scripts/mixer_exact_frames.py read {shlex.quote(run)} {shlex.quote(os.path.join(wr, OUT_SUB, f"hp_{stp}.liggghts"))} '
           f'--g6 {shlex.quote(os.path.join(wr, OUT_SUB, f"g6_{stp}.liggghts"))} --json <출력.json>')
    rec = dict(schema=DECK_SCHEMA, registered=REGISTERED, note=NOTE,
               created_utc=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
               tool='scripts/mixer_exact_frames.py', tool_sha256=_sha_file(os.path.abspath(__file__)),
               resume_transform=dict(file='scripts/make_mixer_resume.py', sha256=_sha_file(os.path.abspath(_mmr.__file__))),
               run=os.path.basename(run), run_dir=run, work_dir=wr,
               deck_source=dict(path=deck_path, sha256=pm['deck_sha256']), deck_meta_sha256=pm['deck_meta_sha256'],
               plan=dict(t0_step=int(t0), steps_per_rev=float(spr), dump_every=int(de), steps_total=int(total), rotation=bool(rot),
                         settled_planned=int(settled), restart_every=int(every), last_two_restarts_if_complete=last2),
               ckpt=dict(label=ckpt, file=files[ckpt], path=ck, sha256=_sha_file(ck), bytes=os.path.getsize(ck), header=hdr,
                         header_error=hdr_err, step=step, **where,
                         planned_match=(None if step is None else (step == settled if ckpt == 'settled' else step in last2))),
               deck=dict(file=DECK_FILE, sha256=_sha_file(os.path.join(wr, DECK_FILE))),
               sbatch=dict(file=SBATCH_FILE, sha256=_sha_file(os.path.join(wr, SBATCH_FILE))),
               dumps=dict(hp=dict(columns=list(HP_COLS), format=dump_modify_format(HP_COLS)),
                          g6=dict(columns=list(HP_COLS), format='LIGGGHTS 기본 (id · type %d · 나머지 %g)')),
               links=links, dropped_commands=info['dropped'], binary=binary, slurm=env, commands=dict(srun=srun, sbatch=f'cd {shlex.quote(wr)} && sbatch {SBATCH_FILE}', read=nxt))
    with open(os.path.join(wr, RECEIPT_FILE), 'w', encoding='utf-8') as f:
        f.write(R.dumps_strict(rec) + '\n')
    if not quiet:
        print(f'→ {wr}/{DECK_FILE} · {RECEIPT_FILE} · {SBATCH_FILE} · {OUT_SUB}/ (빈 폴더) · 링크 {" · ".join(links) or "없음"} (런 폴더 원본 · 쓰지 않는다)')
        print(f'   런 {rec["run"]} · 체크포인트 {ckpt} = {ck} · sha256 {rec["ckpt"]["sha256"][:16]}… · 머리 step '
              f'{"미상 — " + hdr_err if step is None else f"{step:,}"} · {_where_txt(where, t0, rot)}')
        if step is not None and rec['ckpt']['planned_match'] is False:
            print(f'   ⚠ 이 체크포인트 step 이 계획과 다르다 (settled 계획 {settled:,} · 완주면 마지막 두 체크포인트 {last2}) — 미완주 · 다른 파일인지 확인')
        if binary['matches_run_seal'] is False:
            print(f'   ⚠ 바이너리 {binary["path"]} sha256 {str(binary["sha256"])[:12]}… ≠ 런 발사 봉인 {str(binary["run_seal_sha256"])[:12]}…')
        print('   ibb (한 코어 · 분 단위 · 출력은 작업 폴더에만):')
        if env.get('conda_env'):
            print(f'     source ~/.bashrc && conda activate {env["conda_env"]}' + (f'   # PATH 앞에 {env["path_prefix"]} (런 봉인)' if env.get('path_prefix') else ''))
        print(f'     {srun}')
        print(f'   또는 (sbatch — 재개-위상 영수증 job 235118 과 같은 mpirun -np 1 형식):  {rec["commands"]["sbatch"]}')
        print(f'   다음: {nxt}')
    return rec


# ═════════════════════════════ read ═════════════════════════════
def _raw_dump(path):
    """LIGGGHTS 평문 덤프 → dict(step, cols, rows (토큰 문자열 목록)) — validate_frame 을 넘은 파일에만 쓴다 (토큰 그대로 보려고)."""
    with open(path, encoding='utf-8', errors='replace') as f:
        L = f.read().split('\n')
    i = next(k for k, l in enumerate(L) if l.startswith('ITEM: ATOMS'))
    j = next(k for k, l in enumerate(L) if l.startswith('ITEM: TIMESTEP'))
    return dict(step=int(L[j + 1].strip()), cols=L[i].split()[2:], rows=[l.split() for l in L[i + 1:] if l.strip()])


def _emu(a):
    """LIGGGHTS %g 의 에뮬레이션 (값마다 파이썬 '%g' → float)."""
    return np.array([float('%g' % v) for v in np.asarray(a, dtype=float).tolist()])


def _t0_reference(fp, pm):
    """런의 계획 t₀ 덤프 (판독기 frame_plan 이 고른 · 검사한 그 파일) → 원자 기준 (id 순 · type · 반경).
    t₀ 원자 수 = deck_meta n_atoms_planned (판독기 analyse_run 과 같은 규칙 — 어긋나면 TECH)."""
    D = read_dump(fp['t0_path'])
    ids = np.asarray(D['id']).astype(np.int64)
    if len(ids) != pm['n_planned']:
        raise Tech(f't₀ (step {fp["t0_step"]}) 원자 수 {len(ids)} ≠ deck_meta n_atoms_planned {pm["n_planned"]}')
    o = np.argsort(ids, kind='stable')
    return dict(step=int(fp['t0_step']), path=fp['t0_path'], sha256=_sha_file(fp['t0_path']), ids=ids[o],
                type=np.asarray(D['type']).astype(np.int64)[o], radius=np.asarray(D['radius'], dtype=float)[o])


def _receipt_for(hp, run):
    """hp 덤프 (<작업 폴더>/exact/hp_<step>.liggghts) → (영수증, 작업 폴더).  출처 사슬을 다시 잰다 — 어긋나면 Tech."""
    d = os.path.dirname(hp)
    work = os.path.dirname(d)
    rp = os.path.join(work, RECEIPT_FILE)
    if os.path.basename(d) != OUT_SUB or not os.path.isfile(rp):
        raise Tech(f'{os.path.basename(hp)}: {RECEIPT_FILE} 를 찾을 수 없다 (덤프가 deck 작업 폴더의 {OUT_SUB}/ 에 있어야 한다) — 출처 사슬이 끊긴다')
    try:
        with open(rp, encoding='utf-8') as f:
            rec = json.load(f)
    except (OSError, ValueError) as e:
        raise Tech(f'{rp}: 영수증을 읽을 수 없다 ({e})')
    probs = []
    if not isinstance(rec, dict) or rec.get('schema') != DECK_SCHEMA:
        raise Tech(f'{rp}: schema ≠ {DECK_SCHEMA}')
    if rec.get('run_dir') != run:
        probs.append(f'영수증의 런 폴더 {rec.get("run_dir")} ≠ read 에 준 런 폴더 {run} — 다른 런의 체크포인트 덤프다')
    dk = os.path.join(work, DECK_FILE)
    if not os.path.isfile(dk) or _sha_file(dk) != (rec.get('deck') or {}).get('sha256'):
        probs.append(f'{DECK_FILE} sha256 ≠ 영수증 — 덱이 바뀌었거나 없다')
    ck = (rec.get('ckpt') or {}).get('path')
    if not ck or not os.path.isfile(ck) or _sha_file(ck) != rec['ckpt'].get('sha256'):
        probs.append(f'체크포인트 {ck} 의 sha256 ≠ 영수증 (deck 뒤에 바뀌었거나 없다) — 이 덤프가 어느 상태에서 왔는지 잇지 못한다')
    src = os.path.join(run, 'in.mixer')
    if (rec.get('deck_source') or {}).get('sha256') != _sha_file(src):
        probs.append('런의 in.mixer sha256 ≠ 영수증 (덱을 만든 뒤 원 덱이 바뀌었다)')
    if probs:
        raise Tech([f'{os.path.basename(hp)}: {p_}' for p_ in probs])
    return rec, work


def _log_steps(work):
    """작업 폴더의 LIGGGHTS 로그에서 덱의 출력 (EXACT_STEP <step>) — {로그 이름: [step …]} (없으면 빈 dict)."""
    out = {}
    for nm in ('log.exact', 'log.liggghts', 'log.lammps'):
        p_ = os.path.join(work, nm)
        if os.path.isfile(p_):
            with open(p_, encoding='utf-8', errors='replace') as f:
                st = [int(m.group(1)) for m in re.finditer(rf'^{STEP_TAG} (\d+)\b', f.read(), re.M)]
            if st:
                out[nm] = st
    return out


def _pair_audit(D, Dr, pm):
    """같은 배치의 정확 (hp) · 반올림 (%g) 좌표 → (상 쌍별 {exact · registered · lost · gained · ambiguous_at_hp}, 반경 = 계획 double?).
      exact = hp 좌표의 등록 판정 · registered = 반올림 좌표의 등록 판정 · lost = 참인데 놓침 · gained = 아닌데 셈 ·
      ambiguous_at_hp = hp 정밀도 안에서 갈리는 쌍 (가능 − 확실 · 좌표 반폭 + 반경 반폭).
    판정 = 판독기 classify_pairs 그대로 (u = P[ib] − P[ia] · 엄격 <) — 판독기 접촉 수와 대조한다 (어긋나면 도구 불일치 = TECH).
    hp 정밀도 범위: 좌표 반폭 = 판독기 유효숫자 규칙 (hp 는 13 자리 상한 → ~1e-15 m) · 반경 반폭 = **0** — hp 반경이 계획 템플릿 상수의 double 과
    비트까지 같을 때 (`radius constant` = 반올림 없음).  아니면 판독기 반경 규칙 (S = max(관측, 6)).
    ⚠ 판독기의 반경 자릿수 바닥 (S = max(관측, 6) → 반경 반폭 SE 5e-11 · AM 5e-10 m) 은 짧은 십진 반경을 그 폭만큼 불확실하게 둔다 —
      판독기 자신의 hp 범위 (reader_resolution_on_hp) 가 그 폭 안의 접촉에서 열리는 것은 이 규칙 탓이지 좌표 반올림이 아니다 (셀프테스트 ㉘)."""
    t = np.asarray(D['type']).astype(np.int64)
    idx = {p_: np.flatnonzero(t == v['type']) for p_, v in pm['phases'].items()}
    P = np.column_stack([D['x'], D['y'], D['z']]).astype(float)
    Pr = np.column_stack([Dr['x'], Dr['y'], Dr['z']]).astype(float)
    r, rr = np.asarray(D['radius'], dtype=float), np.asarray(Dr['radius'], dtype=float)
    h = R.half_width(P, R.sigfigs_effective(P))
    plan_r = np.full(len(r), np.nan)
    for p_, v in pm['phases'].items():
        plan_r[t == v['type']] = v['radius_m']
    r_exact = bool(np.array_equal(r, plan_r))
    hr = np.zeros_like(r) if r_exact else R.half_width(r, R.sigfigs_effective(r))
    z3, z1 = np.zeros_like(P), np.zeros_like(r)
    pad = (2.0 * math.sqrt(3.0) * (float(np.abs(P - Pr).max(initial=0.0)) + float(h.max(initial=0.0)))
           + 2.0 * (float(np.abs(r - rr).max(initial=0.0)) + float(hr.max(initial=0.0))) + 1e-12)

    def cls(ia, ib):
        ce, lo, hi = R.classify_pairs(P, r, h, hr, ia, ib)
        cr = R.classify_pairs(Pr, rr, z3, z1, ia, ib)[0]
        return dict(exact=int(ce.sum()), registered=int(cr.sum()), lost=int((ce & ~cr).sum()), gained=int((~ce & cr).sum()),
                    ambiguous_at_hp=int(hi.sum() - lo.sum()))
    ise = idx['SE']
    tree = cKDTree(P[ise])
    pr = tree.query_pairs(2.0 * float(r[ise].max()) + pad, output_type='ndarray') if len(ise) > 1 else np.zeros((0, 2), np.int64)
    out = {'SE-SE': cls(ise[pr[:, 0]], ise[pr[:, 1]])}
    for p_ in AM_PHASES:
        ix = idx[p_]
        if not len(ix):
            out[f'{p_}-SE'] = dict(exact=0, registered=0, lost=0, gained=0, ambiguous_at_hp=0)
            continue
        lists = cKDTree(P[ix]).query_ball_tree(tree, float(r[ix].max()) + float(r[ise].max()) + pad)
        ja = np.repeat(np.arange(len(ix), dtype=np.int64), [len(l_) for l_ in lists])
        js = np.fromiter((j_ for l_ in lists for j_ in l_), dtype=np.int64, count=int(len(ja)))
        out[f'{p_}-SE'] = cls(ix[ja], ise[js])
    return out, r_exact


def _g6_check(g6, st, ids_s, typ_s, strs):
    """(iii) g6 (LIGGGHTS 기본 %g) 토큰 = 에뮬레이션 문자열 ('%g' % hp 값) — 원자 (id 순) · 열 x y z radius 마다.  다르면 Tech."""
    probs = validate_frame(g6)
    if probs:
        raise Tech(f'{os.path.basename(g6)}: g6 프레임 검사 실패 {probs[:3]}')
    raw = _raw_dump(g6)
    if raw['step'] != st or tuple(raw['cols']) != HP_COLS:
        raise Tech(f'{os.path.basename(g6)}: g6 step {raw["step"]} · 열 {raw["cols"]} ≠ hp step {st} · {list(HP_COLS)}')
    cols = list(zip(*raw['rows']))
    gid = np.array([int(v) for v in cols[0]], dtype=np.int64)
    o = np.argsort(gid, kind='stable')
    if len(gid) != len(ids_s) or not np.array_equal(gid[o], ids_s) or not np.array_equal(np.array([int(v) for v in cols[1]])[o], typ_s):
        raise Tech(f'{os.path.basename(g6)}: g6 원자 집합 (id · type) ≠ hp')
    bad = []
    for k, c in enumerate(FLOAT_COLS):
        g = [cols[2 + k][i] for i in o.tolist()]
        bad += [(int(ids_s[i]), c, g[i], strs[c][i]) for i in range(len(g)) if g[i] != strs[c][i]]
    if bad:
        raise Tech(f'{os.path.basename(g6)}: g6 (LIGGGHTS %g) ≠ 에뮬레이션 (파이썬 %g) {len(bad)} 값 (예: id · 열 · g6 · 에뮬레이션 {bad[:3]}) — '
                   '반올림 에뮬레이션을 믿을 수 없다')
    return dict(status='MATCH', file=os.path.abspath(g6), sha256=_sha_file(g6), n_values=len(ids_s) * len(FLOAT_COLS))


def _read_one(run, pm, fp, ref, hp, g6_map):
    """hp 덤프 하나 → (프레임 행, 출처 조각).  어긋나면 Tech · SE 0 = Undefined."""
    hp = os.path.abspath(hp)
    nm = os.path.basename(hp)
    if not os.path.isfile(hp):
        raise Tech(f'{hp}: 없음')
    probs = validate_frame(hp)
    if probs:
        raise Tech(f'{nm}: 프레임 검사 (헤더 · 스키마) 실패 {probs[:3]}')
    sha_hp = _sha_file(hp)
    raw = _raw_dump(hp)
    st = raw['step']
    if tuple(raw['cols']) != HP_COLS:
        raise Tech(f'{nm}: 열 {raw["cols"]} ≠ {list(HP_COLS)} — 정확 덱의 hp dump 가 아니다')
    cols = dict(zip(HP_COLS, zip(*raw['rows'])))
    for c in ('id', 'type'):
        bad = [v for v in cols[c] if not re.fullmatch(r'-?\d+', v)]
        if bad:
            raise Tech(f'{nm}: {c} 토큰이 정수 (%d) 가 아니다 (예: {bad[:3]})')
    for c in FLOAT_COLS:
        bad = [v for v in cols[c] if ('%.17g' % float(v)) != v]
        if bad:
            raise Tech(f'{nm}: {c} 토큰 {len(bad)} 개가 %.17g 가 아니다 (예: {bad[:3]}) — dump_modify format 이 적용되지 않았거나 다른 형식 · '
                       '정확 값으로 읽지 않는다')
    rec, work = _receipt_for(hp, run)
    hstep = (rec.get('ckpt') or {}).get('step')
    if hstep is not None and hstep != st:
        raise Tech(f'{nm}: 덤프 TIMESTEP {st} ≠ 체크포인트 머리 step {hstep} ({rec["ckpt"]["label"]}) — 다른 상태의 덤프다')
    logs = _log_steps(work)
    off = {k: v for k, v in logs.items() if any(s_ != st for s_ in v)}
    if off:
        raise Tech(f'{nm}: 로그의 {STEP_TAG} {off} ≠ 덤프 TIMESTEP {st}')
    if hstep is None and not logs:
        raise Tech(f'{nm}: 체크포인트 머리도 로그의 {STEP_TAG} 도 없다 — 덤프 step 을 체크포인트에 잇지 못한다')
    ids = np.array([int(v) for v in cols['id']], dtype=np.int64)
    typ = np.array([int(v) for v in cols['type']], dtype=np.int64)
    o = np.argsort(ids, kind='stable')
    if len(ids) != len(ref['ids']) or not np.array_equal(ids[o], ref['ids']) or not np.array_equal(typ[o], ref['type']):
        raise Tech(f'{nm}: 원자 집합 (id · type) 이 t₀ 덤프 (step {ref["step"]}) 와 다르다 — {len(ids)} 개 vs t₀ {len(ref["ids"])} 개 '
                   '(잃은 · 늘어난 · type 이 바뀐 원자)')
    X = {c: np.array([float(v) for v in cols[c]])[o] for c in FLOAT_COLS}
    Xr = {c: _emu(X[c]) for c in FLOAT_COLS}
    if not np.array_equal(Xr['radius'], ref['radius']):
        k_ = int(np.flatnonzero(Xr['radius'] != ref['radius'])[0])
        raise Tech(f'{nm}: 반경 (%g) 이 t₀ 덤프와 다르다 (예: id {int(ref["ids"][k_])} · {Xr["radius"][k_]!r} vs {ref["radius"][k_]!r})')
    D = dict(id=ids[o], type=typ[o], **X)
    Dr = dict(id=ids[o], type=typ[o], **Xr)
    try:
        q_e, q_r = R.frame_quantities(D, pm), R.frame_quantities(Dr, pm)
    except Tech as e:
        raise Tech([f'{nm}: {r_}' for r_ in e.reasons])
    except Undefined as e:
        raise Undefined(f'{nm}: {e}')
    fl, r_exact = _pair_audit(D, Dr, pm)
    amb = {k: fl[k].pop('ambiguous_at_hp') for k in fl}
    mis = [k for k in fl if fl[k]['exact'] != q_e['pairs'][k] or fl[k]['registered'] != q_r['pairs'][k]]
    if mis:
        raise Tech(f'{nm}: 접촉 수 독립 재계수 ≠ 판독기 {mis} ({fl} vs 정확 {q_e["pairs"]} · 반올림 {q_r["pairs"]}) — 도구 불일치')
    lo, hi = q_r['resolution']['lo'], q_r['resolution']['hi']
    ex = {**{k: q_e['s1_se_clusters'][k] for k in S1_KEYS}, **{k: q_e['s2_am_se_attach'][k] for k in S2_KEYS}}
    viol = [k for k in S1_KEYS + S2_KEYS if ex[k] is not None and not (lo[k] <= ex[k] <= hi[k])]
    viol += [f'pairs.{k}' for k in q_e['pairs'] if not (q_r['resolution']['pairs_lo'][k] <= q_e['pairs'][k] <= q_r['resolution']['pairs_hi'][k])]
    if viol:
        raise Tech(f'{nm}: 불변식 확실 ≤ 정확 ≤ 가능 이 깨졌다 {viol} — 판독기 · 이 도구의 결함 의심 (값을 내지 않는다)')
    collapsed = all(v == 0 for v in amb.values())                      # hp 정밀도 (좌표 ~1e-15 m · 반경 = 계획 double) 에서 접촉 집합이 정해진다
    if st in g6_map:
        strs = {c: ['%g' % v for v in X[c].tolist()] for c in FLOAT_COLS}
        g6r = _g6_check(g6_map[st], st, ids[o], typ[o], strs)
    else:
        g6r = dict(status='NOT_GIVEN')
    pl = fp['plan']
    where = _where(st, fp['t0_step'], pl['steps_per_rev'], pl['dump_every'], fp['mode'] == 'rot2')
    ck = rec['ckpt']
    row = dict(step=int(st), ckpt=ck['label'], ckpt_file=ck['file'], **where, planned_match=ck.get('planned_match'),
               ckpt_header_step=hstep, log_steps=logs, n=q_e['n'],
               hp=dict(file=hp, sha256=sha_hp), g6=g6r,
               exact=dict(s1_se_clusters=q_e['s1_se_clusters'], s2_am_se_attach=q_e['s2_am_se_attach'], pairs=q_e['pairs'],
                          collapsed=bool(collapsed), ambiguous_at_hp=amb, radius_matches_plan_exactly=r_exact,
                          reader_resolution_on_hp=q_e['resolution']),
               rounded=dict(s1_se_clusters=q_r['s1_se_clusters'], s2_am_se_attach=q_r['s2_am_se_attach'], pairs=q_r['pairs'],
                            resolution=q_r['resolution']),
               rounding=fl, invariant_ok=True)
    prov = dict(restart=dict(ckpt=ck['label'], path=ck['path'], sha256=ck['sha256']),
                deck=dict(ckpt=ck['label'], path=os.path.join(work, DECK_FILE), sha256=rec['deck']['sha256']),
                receipt=dict(ckpt=ck['label'], path=os.path.join(work, RECEIPT_FILE), sha256=_sha_file(os.path.join(work, RECEIPT_FILE))),
                dumps=[[int(st), hp, sha_hp]] + ([[int(st), g6r['file'], g6r['sha256']]] if g6r['status'] == 'MATCH' else []))
    return row, prov


def _bin_window(t0, spr, total):
    """판독기 bin 식 (bin_of) 으로 bin 1 에 드는 정수 step 의 [처음, 끝] (끝 ≤ 덱 끝)."""
    lo = t0 + int(math.floor(spr)) - 2
    while bin_of(lo, t0, spr) < R.REG_BIN:
        lo += 1
    while bin_of(lo - 1, t0, spr) == R.REG_BIN:
        lo -= 1
    hi = min(int(total), t0 + int(math.ceil(2 * spr)) + 2)
    while hi >= lo and bin_of(hi, t0, spr) > R.REG_BIN:
        hi -= 1
    return [int(lo), int(hi)] if hi >= lo else None


def read_run(run_dir, hp_paths, g6_paths=()):
    """read 명령 → 결과 dict (status OK · TECH · UNDEFINED).  TECH · UNDEFINED 면 값 (frames) 없음."""
    t_all = time.time()
    run = os.path.realpath(run_dir)
    res = dict(schema=SCHEMA, registered=REGISTERED, note=NOTE, run=os.path.basename(run), run_dir=run, status=None, reasons=[], mode=None,
               plan=None, t0_reference=None, frames=None,
               provenance=dict(tool_sha256=_sha_file(os.path.abspath(__file__)), reader_sha256=_sha_file(os.path.abspath(R.__file__)),
                               frame_tools_sha256=R._frame_tools_sha(), deck_source_sha256=None, deck_meta_sha256=None,
                               restarts=[], exact_decks=[], receipts=[], dumps=[]),
               timing=None)
    try:
        if not hp_paths:
            raise Tech('hp 덤프가 없다')
        pm = R.phase_map(run)
        res['provenance'].update(deck_source_sha256=pm['deck_sha256'], deck_meta_sha256=pm['deck_meta_sha256'])
        fp = R.frame_plan(run, pm)
        pl = fp['plan']
        res['mode'] = fp['mode']
        res['plan'] = dict(t0_step=int(fp['t0_step']), steps_per_rev=float(pl['steps_per_rev']), dump_every=int(pl['dump_every']),
                           steps_total=int(pl['steps_total']), settled_planned=int(pl['steps_total'] - pl['steps_run']),
                           n_atoms_planned=int(pm['n_planned']),
                           bin1=(dict(bin=R.REG_BIN, window_steps=_bin_window(fp['t0_step'], pl['steps_per_rev'], pl['steps_total']),
                                      registered_frames=[int(fp['bin_steps'][0]), int(fp['bin_steps'][-1])], n_registered_frames=len(fp['bin_steps']))
                                 if fp['mode'] == 'rot2' else None))
        ref = _t0_reference(fp, pm)
        res['t0_reference'] = dict(step=ref['step'], file=ref['path'], sha256=ref['sha256'], n=int(len(ref['ids'])))
        g6_map = {}
        for g in g6_paths:
            g = os.path.abspath(g)
            if not os.path.isfile(g):
                raise Tech(f'{g}: 없음')
            try:
                s_ = _raw_dump(g)['step']
            except (StopIteration, ValueError, IndexError):
                raise Tech(f'{os.path.basename(g)}: g6 머리를 읽을 수 없다')
            if s_ in g6_map:
                raise Tech(f'g6 덤프 둘이 같은 step {s_}')
            g6_map[s_] = g
        rows, steps = [], set()
        for hp in hp_paths:
            row, prov = _read_one(run, pm, fp, ref, hp, g6_map)
            if row['step'] in steps:
                raise Tech(f'hp 덤프 둘이 같은 step {row["step"]}')
            steps.add(row['step'])
            rows.append(row)
            for k_, k2 in (('restart', 'restarts'), ('deck', 'exact_decks'), ('receipt', 'receipts')):
                res['provenance'][k2].append(prov[k_])
            res['provenance']['dumps'] += prov['dumps']
        extra = sorted(set(g6_map) - steps)
        if extra:
            raise Tech(f'g6 덤프 step {extra} 에 짝 hp 가 없다')
        res['frames'] = sorted(rows, key=lambda r_: r_['step'])
        res['status'] = 'OK'
    except Tech as e:
        res.update(status='TECH', reasons=e.reasons, frames=None)
    except Undefined as e:
        res.update(status='UNDEFINED', reasons=[str(e)], frames=None)
    if res['status'] != 'OK':                                              # 값이 없으면 부분 출처 목록도 남기지 않는다
        for k in ('restarts', 'exact_decks', 'receipts', 'dumps'):
            res['provenance'][k] = []
    res['timing'] = dict(total_s=time.time() - t_all, frames=len(res['frames'] or []))
    return res


_LABEL = {'se_frac_in_clusters': '(s1) 군집 SE 분율', 'largest_frac': '(s1) 가장 큰 성분 분율', 'mean_size_number': '(s1) 수평균 성분 크기',
          'se_attached_any_frac': '(s2) 아무 AM 에 붙은 SE', 'se_attached_frac_AM_P': '(s2) AM_P 에 붙은 SE', 'se_attached_frac_AM_S': '(s2) AM_S 에 붙은 SE',
          'se_per_am_AM_P': '(s2) AM_P 하나당 SE', 'se_per_am_AM_S': '(s2) AM_S 하나당 SE'}
_FMT = {'mean_size_number': '.3f', 'se_per_am_AM_P': '.2f', 'se_per_am_AM_S': '.2f'}


def report(res):
    print(f"{res['run']} · {res['status']}" + (f" · {res['mode']}" if res.get('mode') else '')
          + ' · 정확 좌표 보충 (§12-4 (나) · 보고 전용 · 관문 아님 · 정의 불변)')
    if res['status'] != 'OK':
        for r_ in res['reasons']:
            print(f'   ⚠ {r_}')
        return
    pl = res['plan']
    if pl['bin1']:
        w = pl['bin1']['window_steps']
        rf = pl['bin1']['registered_frames']
        print(f"   t₀ {pl['t0_step']:,} · 등록 bin 1 창 = step {w[0]:,}–{w[1]:,} (등록 프레임 {rf[0]:,}–{rf[1]:,} · {pl['bin1']['n_registered_frames']} 장 · "
              f"덤프 간격 {pl['dump_every']:,})")
    else:
        print(f"   회전 없음 (E0) — 등록 프레임 = t₀ {pl['t0_step']:,} 하나")
    rot = res['mode'] == 'rot2'
    for f in res['frames']:
        g6 = f['g6']
        print(f"  ── step {f['step']:,} · {f['ckpt']} ({f['ckpt_file']}) · {_where_txt(f, pl['t0_step'], rot)} · g6 대조 {g6['status']}"
              + (f" ({g6['n_values']:,} 값)" if g6['status'] == 'MATCH' else '')
              + (' · ⚠ 계획 step 과 다름' if f.get('planned_match') is False else ''))
        print(f"     {'양':<24s} {'정확':>10s} {'등록 규칙 @ %g':>15s}   [확실, 가능] (@ %g)")
        lo, hi = f['rounded']['resolution']['lo'], f['rounded']['resolution']['hi']
        for k in S1_KEYS + S2_KEYS:
            src_e = f['exact']['s1_se_clusters'] if k in S1_KEYS else f['exact']['s2_am_se_attach']
            src_r = f['rounded']['s1_se_clusters'] if k in S1_KEYS else f['rounded']['s2_am_se_attach']
            ff = _FMT.get(k, '.4f')
            print(f"     {_LABEL[k]:<24s} {R._fmt(src_e[k], ff):>10s} {R._fmt(src_r[k], ff):>15s}   [{R._fmt(lo[k], ff)}, {R._fmt(hi[k], ff)}]")
        plo, phi = f['rounded']['resolution']['pairs_lo'], f['rounded']['resolution']['pairs_hi']
        for k, v in f['rounding'].items():
            print(f"     접촉 {k:<19s} {v['exact']:>10,d} {v['registered']:>15,d}   [{plo[k]:,}, {phi[k]:,}] · 반올림이 놓침 {v['lost']:,} · 없는데 셈 {v['gained']:,}")
        rh = f['exact']['reader_resolution_on_hp']
        n_open = sum(rh['pairs_hi'][k] - rh['pairs_lo'][k] for k in rh['pairs_hi'])
        print(f"     정확 쪽: hp 정밀도에서 접촉 집합 {'결정됨 ✓' if f['exact']['collapsed'] else '모호 ✗ ' + str(f['exact']['ambiguous_at_hp'])} "
              f"(좌표 유효숫자 {rh['sigfigs_xyz']} · 반폭 ≤ {rh['half_width_max_m']:.0e} m · 반경 = 계획 double "
              f"{'✓' if f['exact']['radius_matches_plan_exactly'] else '✗'})"
              + (f" · 판독기 규칙 그대로면 반경 자릿수 바닥 탓에 {n_open} 쌍이 열림 (진단)" if n_open else ''))
        print(f"     반올림 쪽: 유효숫자 {f['rounded']['resolution']['sigfigs_xyz']} · 좌표 반폭 최대 {f['rounded']['resolution']['half_width_max_m']:.3g} m")
    print(f"   시간 {res['timing']['total_s']:.1f} s")


# ═════════════════════════════ 합성 고정구 (셀프테스트) ═════════════════════════════
_R_PLAN = dict(R._R_PLAN)                               # AM_P 6.813e-4 · AM_S 3.028e-4 · SE 7.57e-5 m (캠페인 덱의 radius constant)
_TYPE = {'AM_P': 1, 'AM_S': 2, 'SE': 3}


def _syn_deck(revs=2, restart_every=150):
    """합성 덱 — deck_plan · phase_map · make_mixer_resume.transform 이 읽는 최소 구조 + restart · write_restart · 메시 한 장.
    정착 125 ×2 · 덤프 50 · 바퀴 160 step (주기 0.16 s / dt 1e-3) ⇒ t₀ 250 · 정착 끝 251 · 2 바퀴면 끝 571 · bin 1 = 450 · 500 · 550."""
    return ('# 합성 덱 (mixer_exact_frames 셀프테스트)\n'
            'atom_style granular\natom_modify map array sort 0 0\nboundary f f f\nunits si\n'
            'region reg block -0.03 0.03 -0.03 0.03 -0.03 0.03 units box\ncreate_box 4 reg\n'
            'fix m1 all property/global youngsModulus peratomtype 1e9 1e9 2e8 1e9\n'
            'pair_style gran model hertz tangential history\npair_coeff * *\ntimestep 1e-3\n'
            'fix Drum all mesh/surface file Drum.stl type 4 scale 0.02\n'
            'fix walls all wall/gran model hertz tangential history mesh n_meshes 1 meshes Drum\n'
            'fix pt1 all particletemplate/sphere 10487 atom_type 1 density constant 4800 radius constant 0.0006813\n'
            'fix pt2 all particletemplate/sphere 11887 atom_type 2 density constant 4800 radius constant 0.0003028\n'
            'fix pt3 all particletemplate/sphere 13901 atom_type 3 density constant 2000 radius constant 7.57e-05\n'
            'fix pdd all particledistribution/discrete 32452867 3 &\n    pt1 0.5 pt2 0.3 pt3 0.2\n'
            'region ins_reg cylinder x 0.0 0.0 0.01 -0.002 0.002 units box\n'
            'fix ins all insert/pack seed 32452843 distributiontemplate pdd &\n'
            '    insert_every once overlapcheck yes region ins_reg particles_in_region 31 ntry_mc 20000\n'
            'fix integrS all nve/sphere\nthermo 50\nthermo_modify lost ignore norm no\n'
            f'shell mkdir post\nshell mkdir restart\nrestart {restart_every} restart/a.bin restart/b.bin\nrun 1\n'
            'dump dmp all custom 50 post/mix_*.liggghts id type x y z vx vy vz fx fy fz radius\n'
            'run 125\nunfix ins\nrun 125\nwrite_restart restart/settled.bin\n'
            'fix mvD all move/mesh mesh Drum rotate origin 0 0 0 axis 1. 0. 0. period 0.16\n'
            f'run {320 if revs == 2 else 0}\n')


def _fake_restart(path, step, nprocs=20, tail=b'\x5a' * 512):
    """LIGGGHTS 3.x write_restart.cpp header() 모양의 머리 + 아무 바이트 (셀프테스트 전용)."""
    def fi(f, v):
        return struct.pack('<ii', f, v)

    def fs(f, s):
        b = s.encode('ascii') + b'\0'
        return struct.pack('<ii', f, len(b)) + b
    head = (fs(0, 'Version LIGGGHTS-PUBLIC 3.8.0, compiled 2026-03-26-14:37:06 by yonghoon, git commit 3d5c00f') + fi(1, 4) + fi(2, 4)
            + fi(3, 8) + fs(4, 'si') + struct.pack('<iq', 5, int(step)) + fi(6, 3) + fi(7, int(nprocs)))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(head + tail)


def _write_lig(path, atoms, step, ffmt):
    """LIGGGHTS dump custom 모양 (열 = id type x y z radius · 값마다 뒤에 공백 · dump_custom.cpp vformat) — ffmt = '.17g' (hp) | 'g' (g6 · 기본)."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(f'ITEM: TIMESTEP\n{step}\nITEM: NUMBER OF ATOMS\n{len(atoms)}\nITEM: BOX BOUNDS ff ff ff\n'
                '-0.03 0.03\n-0.03 0.03\n-0.03 0.03\nITEM: ATOMS id type x y z radius \n')
        f.write(''.join(f'{int(i)} {int(t)} {x:{ffmt}} {y:{ffmt}} {z:{ffmt}} {r:{ffmt}} \n' for i, t, x, y, z, r in atoms))


def _g(v):
    """LIGGGHTS 기본 %g (C printf) 의 에뮬레이션 — 파이썬 '%g' (둘 다 바르게 반올림한 십진 6 자리) → float."""
    return float('%g' % v)


def _oracle(atoms, rnd=False):
    """독립 산술 (판독기 함수를 부르지 않는다) — 모든 쌍 rsq < (r_i + r_j)² → s1 · s2 · 접촉 수.  rnd = 좌표 · 반경을 %g 로 반올림한 뒤."""
    f = _g if rnd else float
    A = [(int(i), int(t), f(x), f(y), f(z), f(r)) for i, t, x, y, z, r in atoms]
    se = [a for a in A if a[1] == _TYPE['SE']]
    ix = {a[0]: k for k, a in enumerate(se)}
    par = list(range(len(se)))

    def find(k):
        while par[k] != k:
            par[k] = par[par[k]]
            k = par[k]
        return k

    def touch(a, b):
        dx, dy, dz = b[2] - a[2], b[3] - a[3], b[4] - a[4]
        return dx * dx + dy * dy + dz * dz < (a[5] + b[5]) * (a[5] + b[5])
    n_ss = 0
    for p in range(len(se)):
        for q in range(p + 1, len(se)):
            if touch(se[p], se[q]):
                n_ss += 1
                par[find(p)] = find(q)
    roots = [find(k) for k in range(len(se))]
    sizes = {}
    for r_ in roots:
        sizes[r_] = sizes.get(r_, 0) + 1
    n_se = len(se)
    out = dict(se_frac_in_clusters=sum(s for s in sizes.values() if s >= 2) / n_se, largest_frac=max(sizes.values()) / n_se,
               mean_size_number=n_se / len(sizes), pairs={'SE-SE': n_ss})
    att_any = set()
    for p_ in AM_PHASES:
        am = [a for a in A if a[1] == _TYPE[p_]]
        hit = [(a[0], s[0]) for a in am for s in se if touch(a, s)]
        att = {s_ for _, s_ in hit}
        att_any |= att
        out[f'se_attached_frac_{p_}'] = len(att) / n_se
        out[f'se_per_am_{p_}'] = len(hit) / len(am) if am else None
        out['pairs'][f'{p_}-SE'] = len(hit)
    out['se_attached_any_frac'] = len(att_any) / n_se
    del ix
    return out


def _fixture(seed=20261005):
    """얕은 겹침 (수 nm) · 좌표 ≈ 0.01 m 의 합성 정확 배치 → (원자 목록, 범주 수).  쌍마다 무작위 방향 · 위치를 뽑아 독립 산술로 범주를 정한다:
      lost = 참 접촉인데 %g 반올림 좌표에서 등록 규칙이 놓침 · kept = 둘 다 접촉 (얕음) · gained = 참 접촉 아닌데 반올림에서 접촉 · deep = 겹침 300 nm.
    쌍끼리 3 mm 떨어져 서로 안 닿는다 (AM_P–SE 중심 거리 0.76 mm)."""
    rng = np.random.default_rng(seed)
    want = [('SE', 'lost', 3), ('SE', 'kept', 2), ('SE', 'gained', 2), ('SE', 'deep', 2),
            ('AM_P', 'lost', 2), ('AM_P', 'kept', 1), ('AM_S', 'lost', 1), ('AM_S', 'deep', 1)]
    atoms, nid, slot, got = [], 1, 0, {}

    def centre(k):
        return np.array([0.0105 + 0.003 * (k % 3), 0.0105 + 0.003 * ((k // 3) % 3), 0.0105 + 0.003 * (k // 9)])
    for ph, cat, cnt in want:
        for _ in range(cnt):
            ra, rb = _R_PLAN[ph], _R_PLAN['SE']
            rs = ra + rb
            for _try in range(20000):
                u = rng.normal(size=3)
                u /= np.linalg.norm(u)
                depth = {'lost': 1, 'kept': 1, 'gained': -1, 'deep': 1}[cat] * (6e-7 if cat == 'deep' else rng.uniform(2e-9, 8e-9))
                pa = centre(slot) + rng.uniform(-2e-5, 2e-5, 3)
                pb = pa + (rs - depth) * u
                de = [float(pb[k]) - float(pa[k]) for k in range(3)]
                dr = [_g(float(pb[k])) - _g(float(pa[k])) for k in range(3)]
                q_e = de[0] * de[0] + de[1] * de[1] + de[2] * de[2]
                rr = _g(ra) + _g(rb)
                q_r = dr[0] * dr[0] + dr[1] * dr[1] + dr[2] * dr[2]
                if min(abs(q_e - rs * rs), abs(q_r - rr * rr)) <= 1e-9 * rs * rs:      # 합 순서 (einsum ↔ 파이썬) 로 갈릴 수 있는 경계는 버린다
                    continue
                ex, rd = q_e < rs * rs, q_r < rr * rr
                if (cat == 'lost' and ex and not rd) or (cat in ('kept', 'deep') and ex and rd) or (cat == 'gained' and not ex and rd):
                    break
            else:
                raise RuntimeError(f'고정구: {ph} {cat} 를 못 만들었다')
            atoms.append([nid, _TYPE[ph], *pa.tolist(), ra])
            atoms.append([nid + 1, _TYPE['SE'], *pb.tolist(), rb])
            nid += 2
            slot += 1
            got[(ph, cat)] = got.get((ph, cat), 0) + 1
    for _ in range(2):                                                  # 홑 SE 둘 · 홑 AM_P 하나 (분모가 1 이 아니게)
        atoms.append([nid, _TYPE['SE'], *centre(slot).tolist(), _R_PLAN['SE']])
        nid += 1
        slot += 1
    atoms.append([nid, _TYPE['AM_P'], *centre(slot).tolist(), _R_PLAN['AM_P']])
    return atoms, got


def _syn_run(root, name, atoms, revs=2, steps=(250, 450, 500, 550), meta_patch=None, ckpt_steps=None):
    """합성 런 폴더 (in.mixer · deck_meta.json · Drum.stl · post/ (%g) · restart/ (머리 있는 가짜 체크포인트))."""
    d = os.path.join(root, name)
    os.makedirs(os.path.join(d, 'post'))
    deck = _syn_deck(revs)
    with open(os.path.join(d, 'in.mixer'), 'w') as f:
        f.write(deck)
    meta = dict(schema=R.DECK_META_SCHEMA, deck_sha256=hashlib.sha256(deck.encode()).hexdigest(),
                types={'1': 'AM_P', '2': 'AM_S', '3': 'SE', '4': 'WALL'}, radius_m=dict(_R_PLAN), n_atoms_planned=len(atoms),
                revolutions=revs, steps=dict(t0_planned=250, dump_every=50))
    if meta_patch:
        meta_patch(meta)
    with open(os.path.join(d, 'deck_meta.json'), 'w') as f:
        json.dump(meta, f)
    with open(os.path.join(d, 'Drum.stl'), 'w') as f:
        f.write('solid drum\nendsolid drum\n')
    for st in (steps if revs else (250,)):
        R._write_frame(os.path.join(d, 'post', f'mix_{st}.liggghts'), atoms, st)
    for lab, st in (ckpt_steps or dict(settled=251, a=450, b=300)).items():
        _fake_restart(os.path.join(d, 'restart', f'{lab}.bin'), st)
    return d


def _tree(d):
    """폴더 나무의 지문 — (상대 경로 · 종류 · 내용 sha256 또는 링크 대상).  읽기만 하면 바뀌지 않는다."""
    out = []
    for root, dirs, files in os.walk(d, followlinks=False):
        dirs.sort()
        for nm in sorted(dirs + files):
            p = os.path.join(root, nm)
            rel = os.path.relpath(p, d)
            if os.path.islink(p):
                out.append((rel, 'link', os.readlink(p)))
            elif os.path.isdir(p):
                out.append((rel, 'dir', ''))
            else:
                out.append((rel, 'file', _sha_file(p)))
    return out


# ───────────────────────────── selftest ─────────────────────────────
def _selftest():                                            # noqa: C901
    import ast
    import shutil
    import tempfile
    ok, fail = 0, []

    def chk(name, fn):
        nonlocal ok
        try:
            cond = bool(fn())
        except (Exception, SystemExit) as e:                # noqa: BLE001 — 스텁 · 결함이 예외로 터져도 FAIL 로 센다
            print(f'        ({type(e).__name__}: {str(e)[:200]})')
            cond = False
        if cond:
            ok += 1
        else:
            fail.append(name)
        print(('  PASS  ' if cond else '  FAIL  ') + name)

    def refused(fn, why=''):
        try:
            fn()
        except SystemExit as e:
            return why in str(e)
        return False

    root = os.path.dirname(_SCR)
    DECKS = {'LC': 'docs/data/mixer_highbo_dev_decks_20260930_v26/decks/LC_ref_r2_s32452843',      # ibb dev-rot 실행 덱 (5405067f…)
             'LU637': 'docs/data/mixer_highbo_dev_decks_20261005_u/decks/LU637_ref_r2_s32452843',   # dev-u (ibb 실행 중)
             'E0': 'docs/data/mixer_highbo_dev_decks_20260930_v26/decks/E0_ref_s32452843'}           # 회전 0 · 균일 삽입
    texts = {k: open(os.path.join(root, v, 'in.mixer'), encoding='utf-8').read() for k, v in DECKS.items()}
    CK = '/scratch/run_x/restart/settled.bin'

    def cmds_of(t):
        return [(b, _tokens(b)) for _, b in logical_commands(t)]

    #  ── ① ~ ⑤ 덱 변환 (커밋된 실제 덱) ─────────────────────────────────────────────────────────────────
    def _d1():
        good = True
        for k, t in texts.items():
            out, info = exact_deck(t, CK, 'settled', step=1037429, run_name=k)
            cs = [x for _, x in cmds_of(out) if x]
            kws = [x[0] for x in cs]
            rr = [x for x in cs if x[0] == 'read_restart']
            dumps = [x for x in cs if x[0] == 'dump']
            dm = [x for x in cs if x[0] == 'dump_modify']
            i_rr = kws.index('read_restart')
            fmt = re.search(r'^dump_modify hp format "([^"]*)"$', out, re.M)
            good &= (len(rr) == 1 and rr[0][1:] == [CK] and 'create_box' not in kws
                     and cs[i_rr + 1] == ['variable', 'exact_step', 'equal', 'step'] and cs[i_rr + 2][0] == 'print'
                     and STEP_TAG in ' '.join(cs[i_rr + 2])
                     and not any(x[0] == 'fix' and len(x) > 3 and re.match(r'(particletemplate|particledistribution|insert)/', x[3]) for x in cs)
                     and not any(x[0] in ('unfix', 'write_restart', 'restart', 'shell', 'region', 'undump') for x in cs)
                     and [d_[1] for d_ in dumps] == ['hp', 'g6'] and 'dmp' not in [x[1] for x in cs if x[0].startswith('dump')]
                     and dumps[0][2:] == ['all', 'custom', '1', 'exact/hp_*.liggghts', *HP_COLS]
                     and dumps[1][2:] == ['all', 'custom', '1', 'exact/g6_*.liggghts', *HP_COLS]
                     and len(dm) == 1 and dm[0][1] == 'hp' and fmt is not None
                     and fmt.group(1).split(' ') == ['%d', '%d', '%.17g', '%.17g', '%.17g', '%.17g']
                     and len(fmt.group(1).split(' ')) == len(dumps[0]) - 6 and fmt.group(1) == dump_modify_format(HP_COLS)
                     and [x for x in cs if x[0] == 'run'] == [['run', '0']] and cs[-1] == ['run', '0']
                     and kws.index('dump') < kws.index('run'))
        return good
    chk('① ★ 커밋 실제 덱 셋 (LC_ref_r2 · LU637_ref_r2 · E0_ref) → read_restart <절대경로> 한 번 · 바로 뒤 EXACT_STEP 출력 · create_box · 삽입 · 템플릿 · '
        '분포 · unfix · write_restart · restart · shell · region · 원 dump (dmp) 없음 · dump hp · g6 (id type x y z radius) · dump_modify hp 형식 토큰 6 = '
        '열 수 (%d %d %.17g ×4 · 생성기 dump_modify_format 과 같다) · run 은 `run 0` 하나뿐이고 마지막 명령', _d1)

    KEEP = ('fix', 'pair_style', 'pair_coeff', 'timestep', 'compute', 'thermo', 'thermo_style', 'thermo_modify', 'neighbor', 'neigh_modify',
            'atom_style', 'atom_modify', 'hard_particles', 'boundary', 'newton', 'communicate', 'units')

    def _d2():
        good = True
        for k, t in texts.items():
            out, _ = exact_deck(t, CK, 'a', step=7000000, run_name=k)
            src = [('\n'.join(b), x) for b, x in cmds_of(t) if x and x[0] in KEEP
                   and not (x[0] == 'fix' and len(x) > 3 and re.match(r'(particletemplate|particledistribution|insert)/', x[3]))]
            dst = [('\n'.join(b), x) for b, x in cmds_of(out) if x and x[0] in KEEP]
            ids = {x[1] for _, x in src if x[0] == 'fix'}
            good &= ([b for b, _ in src] == [b for b, _ in dst]
                     and {'m1', 'm2', 'm3', 'm4', 'm5', 'mC', 'm9', 'gravi', 'Drum', 'Front', 'Back', 'walls', 'integrS', 'mvD', 'mvF', 'mvB'} <= ids)
        return good
    chk('② 남기는 명령 = 원 덱 그대로 (글자 · 순서) — 재료 (m1–m5 · mC · m9) · 접촉 (pair_style · pair_coeff) · timestep · 중력 · 메시 (Drum · Front · Back) · '
        '벽 · 적분 · compute · thermo · move/mesh (mvD · mvF · mvB) · atom_style … units', _d2)
    chk('③ 체크포인트 경로가 절대경로가 아니거나 LIGGGHTS 가 뜻을 붙이는 글자 (공백 · % · * · $ · #) 면 거부',
        lambda: (refused(lambda: exact_deck(texts['LC'], 'restart/settled.bin', 'settled'), '절대')
                 and all(refused(lambda b=b: exact_deck(texts['LC'], f'/scratch/run{b}x/restart/settled.bin', 'settled'), 'LIGGGHTS')
                         for b in (' ', '%', '*', '$', '#'))))
    chk('④ 체크포인트 파일 = 덱에서 — settled = write_restart · a · b = `restart N a b` (LC: 200,000 · E0: 51,871)',
        lambda: (restart_files(texts['LC']) == (dict(settled='restart/settled.bin', a='restart/a.bin', b='restart/b.bin'), 200000)
                 and restart_files(texts['E0'])[1] == 51871))

    def _d5():
        pl = deck_plan(os.path.join(root, DECKS['LC'], 'in.mixer'))
        t0, spr, tot = planned_t0(pl), pl['steps_per_rev'], pl['steps_total']
        every = restart_files(texts['LC'])[1]
        last2 = [every * k for k in range(tot // every - 1, tot // every + 1)]
        settled = 1 + 2 * pl['steps_fill']
        return (t0 == 1037408 and settled == 1037429 and settled - t0 == 21 and tot == 7139962 and last2 == [6800000, 7000000]
                and bin_of(settled, t0, spr) == 0 and [bin_of(s_, t0, spr) for s_ in last2] == [1, 1]
                and all((s_ - t0) % pl['dump_every'] != 0 for s_ in [settled] + last2))
    chk('⑤ LC_ref_r2 계획 산술 (덱에서) — t₀ 1,037,408 · 정착 끝 (settled) 1,037,429 = t₀ + 21 (bin 0) · 끝 7,139,962 · 마지막 두 체크포인트 '
        '6,800,000 · 7,000,000 = 둘 다 bin 1 (판독기 bin 식) · 셋 다 덤프 격자 밖 (등록 프레임이 아니다)', _d5)

    with tempfile.TemporaryDirectory() as td:
        #  ── ⑥ ~ ⑧ deck 명령 (커밋 LC 덱의 복사 런 · 가짜 체크포인트 · 가짜 STL) ────────────────────────────────────
        run = os.path.join(td, 'LC_ref_r2_s32452843')
        os.makedirs(os.path.join(run, 'post'))
        for f_ in ('in.mixer', 'deck_meta.json'):
            shutil.copyfile(os.path.join(root, DECKS['LC'], f_), os.path.join(run, f_))
        for f_ in ('Drum.stl', 'Front.stl', 'Back.stl'):
            with open(os.path.join(run, f_), 'w') as fh:
                fh.write(f'solid {f_}\nendsolid\n')
        for lab, st in (('settled', 1037429), ('a', 7000000), ('b', 6800000)):
            _fake_restart(os.path.join(run, 'restart', f'{lab}.bin'), st)
        R._write_frame(os.path.join(run, 'post', 'mix_1037408.liggghts'), [[1, 3, 0.01, 0.01, 0.01, 7.57e-05]], 1037408)
        before = _tree(run)
        W = os.path.join(td, 'work_settled')
        rec = None
        try:
            rec = build_deck(run, 'settled', W, quiet=True)
        except BaseException as e:                                           # noqa: BLE001 — 스텁이면 None
            print(f'        (build_deck: {type(e).__name__}: {str(e)[:160]})')

        def _d6():
            dk = open(os.path.join(W, DECK_FILE), encoding='utf-8').read()
            ck = os.path.realpath(os.path.join(run, 'restart', 'settled.bin'))
            links = {n_: os.path.realpath(os.path.join(W, n_)) for n_ in ('Drum.stl', 'Front.stl', 'Back.stl')}
            sb = open(os.path.join(W, SBATCH_FILE), encoding='utf-8').read()
            return (sorted(os.listdir(W)) == sorted(['Back.stl', 'Drum.stl', 'Front.stl', DECK_FILE, OUT_SUB, RECEIPT_FILE, SBATCH_FILE])
                    and os.listdir(os.path.join(W, OUT_SUB)) == []
                    and all(os.path.islink(os.path.join(W, n_)) and v == os.path.realpath(os.path.join(run, n_)) for n_, v in links.items())
                    and re.search(r'^read_restart\s+(\S+)$', dk, re.M).group(1) == ck
                    and rec['ckpt']['sha256'] == _sha_file(ck) and rec['ckpt']['header']['ntimestep'] == 1037429
                    and rec['deck']['sha256'] == _sha_file(os.path.join(W, DECK_FILE))
                    and rec['run_dir'] == os.path.realpath(run) and rec['ckpt']['bin'] == 0 and rec['ckpt']['step_minus_t0'] == 21
                    and '#SBATCH -n 1' in sb and '-np 1' in sb and f'cd {os.path.realpath(W)}' in sb and 'in.exact' in sb
                    and _tree(run) == before)
        chk('⑥ ★ deck: 새 폴더에 in.exact · exact_receipt.json · run_exact.sbatch · 빈 exact/ · STL 셋 = 런 폴더 원본으로의 심볼릭 링크 · read_restart = '
            '체크포인트 실제 경로 · 영수증 (체크포인트 sha256 · 머리 step 1,037,429 · bin 0 · t₀ + 21 · 덱 sha256) · sbatch (-n 1 · mpirun -np 1 · cd 작업 폴더) · '
            '★ 런 폴더 나무 (이름 · 내용 · 링크) 가 앞뒤 같다', _d6)

        def _d7():
            ok7 = True
            ok7 &= refused(lambda: build_deck(run, 'settled', run, quiet=True), '런 폴더')
            ok7 &= refused(lambda: build_deck(run, 'settled', os.path.join(run, 'sub'), quiet=True), '런 폴더')
            ok7 &= refused(lambda: build_deck(run, 'settled', W, quiet=True), '비어')                   # 이미 쓴 폴더 (덮지 않는다)
            ok7 &= refused(lambda: build_deck(run, 'c', os.path.join(td, 'w_c'), quiet=True), 'ckpt')
            run2 = os.path.join(td, 'run_noB')
            shutil.copytree(run, run2, symlinks=True)
            os.remove(os.path.join(run2, 'restart', 'b.bin'))
            ok7 &= refused(lambda: build_deck(run2, 'b', os.path.join(td, 'w_b2'), quiet=True), '체크포인트')
            os.remove(os.path.join(run2, 'Front.stl'))
            ok7 &= refused(lambda: build_deck(run2, 'a', os.path.join(td, 'w_a2'), quiet=True), 'Front.stl')
            with open(os.path.join(run2, 'in.mixer'), 'a') as fh:
                fh.write('# 바뀐 덱\n')
            ok7 &= refused(lambda: build_deck(run2, 'a', os.path.join(td, 'w_a3'), quiet=True), 'deck_sha256')
            return (ok7 and not any(os.path.exists(os.path.join(td, w_)) for w_ in ('w_c', 'w_b2', 'w_a2', 'w_a3'))
                    and not os.path.exists(os.path.join(run, 'sub')) and _tree(run) == before)
        chk('⑦ deck 거부 (아무것도 쓰기 전): 작업 폴더 = 런 폴더 · 런 폴더 안 · 이미 쓴 폴더 · 모르는 ckpt · 체크포인트 없음 · 덱 입력 (STL) 없음 · '
            'in.mixer ≠ deck_meta.deck_sha256 — 거부한 작업 폴더는 생기지 않고 런 폴더는 그대로', _d7)

        def _d8():
            p_ = os.path.join(td, 'hdr.bin')
            _fake_restart(p_, 6800000, nprocs=20)
            h_ = restart_header(p_)
            with open(p_, 'r+b') as fh:                                     # 플래그 하나를 망가뜨린다
                fh.seek(len('Version LIGGGHTS-PUBLIC 3.8.0, compiled 2026-03-26-14:37:06 by yonghoon, git commit 3d5c00f') + 9)
                fh.write(struct.pack('<i', 9))
            bad = False
            try:
                restart_header(p_)
            except ValueError:
                bad = True
            with open(p_, 'wb') as fh:
                fh.write(b'\x00\x00')
            short = False
            try:
                restart_header(p_)
            except ValueError:
                short = True
            run3 = os.path.join(td, 'run_badhdr')
            shutil.copytree(run, run3, symlinks=True)
            with open(os.path.join(run3, 'restart', 'a.bin'), 'wb') as fh:
                fh.write(b'not a restart file' * 10)
            r3 = build_deck(run3, 'a', os.path.join(td, 'w_badhdr'), quiet=True)
            return (h_['ntimestep'] == 6800000 and h_['nprocs'] == 20 and h_['units'] == 'si' and h_['sizes']['bigint'] == 8 and bad and short
                    and r3['ckpt']['header'] is None and r3['ckpt']['header_error'] and r3['ckpt']['bin'] is None)
        chk('⑧ 체크포인트 머리 (write_restart.cpp header — 플래그 int + 값) → step 6,800,000 · nprocs · units · bigint 8 · 플래그 어긋남 · 짧은 파일 = '
            'ValueError · 머리를 못 읽으면 덱은 만들고 영수증에 step 미상 + 사유 (read 가 덤프 TIMESTEP · 로그로 잇는다)', _d8)

        #  ── ⑨ ~ ㉓ read (합성 정확 배치 — 알려진 답 = 독립 산술) ────────────────────────────────────────────────
        atoms, cats = _fixture()
        S = _syn_run(td, 'LU212_ref_r2_s32452843', atoms)
        works = {}
        for lab in CKPTS:
            try:
                works[lab] = os.path.join(td, f'w_{lab}')
                build_deck(S, lab, works[lab], quiet=True)
            except BaseException as e:                                       # noqa: BLE001
                print(f'        (build_deck 합성 {lab}: {type(e).__name__}: {str(e)[:160]})')
        steps = dict(settled=251, a=450, b=300)

        def hp(lab, st=None, fmt='.17g', at=None):
            p_ = os.path.join(works[lab], OUT_SUB, f'hp_{st or steps[lab]}.liggghts')
            _write_lig(p_, atoms if at is None else at, st or steps[lab], fmt)
            return p_

        def g6(lab, at=None):
            p_ = os.path.join(works[lab], OUT_SUB, f'g6_{steps[lab]}.liggghts')
            _write_lig(p_, atoms if at is None else at, steps[lab], 'g')
            return p_
        HP = [hp(lab) for lab in CKPTS]
        G6 = [g6(lab) for lab in CKPTS]
        for lab in CKPTS:                                                    # LIGGGHTS 로그의 출력 (덱의 print) 흉내
            with open(os.path.join(works[lab], 'log.exact'), 'w') as fh:
                fh.write(f'LIGGGHTS (Version …)\n{STEP_TAG} {steps[lab]} ckpt {lab}\n')
        s_before = _tree(S)
        w_before = {lab: _tree(works[lab]) for lab in CKPTS}
        res = None
        try:
            res = read_run(S, HP, G6)
        except BaseException as e:                                           # noqa: BLE001
            print(f'        (read_run: {type(e).__name__}: {str(e)[:160]})')
        res = res or {}
        untouched = _tree(S) == s_before and all(_tree(works[l_]) == w_before[l_] for l_ in CKPTS)     # ㉑ — 변이 시험 전에 잰다
        frs = {f_['ckpt']: f_ for f_ in (res.get('frames') or [])}
        ex_o, rd_o = _oracle(atoms), _oracle(atoms, rnd=True)

        def same(q, o):
            s1, s2 = q['s1_se_clusters'], q['s2_am_se_attach']
            return (all(abs(s1[k] - o[k]) <= 1e-12 for k in S1_KEYS) and all(abs(s2[k] - o[k]) <= 1e-12 for k in S2_KEYS)
                    and q['pairs'] == o['pairs'])
        chk('⑨ read: 합성 런 · 체크포인트 셋 → OK · rot2 · 프레임 step 순 (251 settled · 300 b · 450 a) · bin 0 · 0 · 1 · 등록 bin 1 창 안 = 450 만 · '
            't₀ 기준 +1 · +50 · +200 · 덤프 격자 위 = 300 · 450',
            lambda: (res['status'] == 'OK' and res['mode'] == 'rot2' and [f_['step'] for f_ in res['frames']] == [251, 300, 450]
                     and [f_['bin'] for f_ in res['frames']] == [0, 0, 1] and [f_['in_bin1'] for f_ in res['frames']] == [False, False, True]
                     and [f_['step_minus_t0'] for f_ in res['frames']] == [1, 50, 200]
                     and [f_['on_dump_lattice'] for f_ in res['frames']] == [False, True, True]))
        chk(f'⑩ ★ 정확 값 = 독립 산술 (double 좌표 · 모든 쌍) · 등록 규칙 @ %g = 독립 산술 (반올림 좌표) — 고정구 {sorted(cats.items())} → '
            f'SE–SE 참 접촉 7 · 반올림 등록 6 (놓침 3 · 없는데 셈 2) · AM_P–SE 3 → 1 · AM_S–SE 2 → 1',
            lambda: (all(same(f_['exact'], ex_o) and same(f_['rounded'], rd_o) for f_ in frs.values())
                     and ex_o['pairs'] == {'SE-SE': 7, 'AM_P-SE': 3, 'AM_S-SE': 2} and rd_o['pairs'] == {'SE-SE': 6, 'AM_P-SE': 1, 'AM_S-SE': 1}
                     and frs['a']['rounding']['SE-SE'] == dict(exact=7, registered=6, lost=3, gained=2)
                     and frs['a']['rounding']['AM_P-SE'] == dict(exact=3, registered=1, lost=2, gained=0)
                     and frs['a']['rounding']['AM_S-SE'] == dict(exact=2, registered=1, lost=1, gained=0)))

        def _inv():
            good = len(frs) == 3
            for f_ in frs.values():
                lo, hi, ex = f_['rounded']['resolution']['lo'], f_['rounded']['resolution']['hi'], f_['exact']
                for k in S1_KEYS:
                    good &= lo[k] <= ex['s1_se_clusters'][k] <= hi[k]
                for k in S2_KEYS:
                    good &= lo[k] <= ex['s2_am_se_attach'][k] <= hi[k]
                for k, v in ex['pairs'].items():
                    good &= f_['rounded']['resolution']['pairs_lo'][k] <= v <= f_['rounded']['resolution']['pairs_hi'][k]
                el, eh = ex['reader_resolution_on_hp']['lo'], ex['reader_resolution_on_hp']['hi']
                good &= (f_['exact']['collapsed'] is True and ex['reader_resolution_on_hp']['sigfigs_xyz'] >= 13
                         and all(v == 0 for v in ex['ambiguous_at_hp'].values()) and ex['radius_matches_plan_exactly'] is True
                         and all(el[k] == eh[k] == ex['s1_se_clusters'][k] for k in S1_KEYS)
                         and all(el[k] == eh[k] == ex['s2_am_se_attach'][k] for k in S2_KEYS)
                         and f_['rounded']['resolution']['sigfigs_xyz'] == 6 and f_['invariant_ok'] is True)
                good &= any(lo[k] < hi[k] for k in S1_KEYS + S2_KEYS)                    # 반올림 쪽 범위는 실제로 열려 있다 (판별력)
            return good
        chk('⑪ ★ 불변식 확실 ≤ 정확 ≤ 가능 — 모든 스칼라 (s1 셋 · s2 다섯) · 접촉 수 · 모든 프레임 · 정확 쪽 범위는 접힌다 (hp 유효숫자 ≥ 13 · lo = 등록 = hi) · '
            '반올림 쪽은 6 유효숫자 · 범위가 열려 있다', _inv)
        chk('⑫ (iii) 에뮬레이션 = 합성 %g 파일 (LIGGGHTS 기본 형식 · 값 뒤 공백) — g6 MATCH · 원자 31 × 값 4',
            lambda: len(frs) == 3 and all(f_['g6']['status'] == 'MATCH' and f_['g6']['n_values'] == 31 * 4 for f_ in frs.values()))

        def tech(hps, g6s=(), why='', run_dir=None):
            r_ = read_run(run_dir or S, hps, g6s)
            return r_['status'] == 'TECH' and r_.get('frames') is None and any(why in s_ for s_ in r_['reasons'])

        def mut(fn):
            at = [list(a) for a in atoms]
            fn(at)
            return at
        _G6_BAD = os.path.join(works['a'], OUT_SUB, 'g6_bad', 'g6_450.liggghts')
        _write_lig(_G6_BAD, atoms, 450, 'g')
        with open(_G6_BAD, encoding='utf-8') as fh:
            _L = fh.read().split('\n')
        _t = _L[9].split(' ')
        _t[2] = _t[2][:-1] + ('1' if _t[2][-1] != '1' else '2')                         # x 마지막 자리 하나
        _L[9] = ' '.join(_t)
        with open(_G6_BAD, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(_L))
        chk('⑬ g6 토큰 하나 (x 의 마지막 자리) 가 에뮬레이션과 다르면 TECH', lambda: tech([HP[1]], [_G6_BAD], 'g6'))
        chk('⑭ 원자 집합 · type 이 t₀ 덤프와 다르면 TECH — (a) 원자 하나 없음 (b) 한 원자의 type 이 바뀜 (SE → AM_S)',
            lambda: (tech([hp('a', at=mut(lambda at: at.pop(4)))], (), '원자')
                     and tech([hp('a', at=mut(lambda at: at[5].__setitem__(1, _TYPE['AM_S'])))], (), '원자')))
        chk('⑮ hp 가 %.17g 가 아니면 (dump_modify format 이 안 먹어 기본 %g 로 찍힘) TECH — 정확 값으로 읽지 않는다',
            lambda: tech([hp('a', fmt='g')], (), '%.17g'))

        def _d16():
            hp('a')                                                                   # 원상태
            ck = os.path.join(S, 'restart', 'a.bin')
            raw = open(ck, 'rb').read()
            try:
                with open(ck, 'ab') as fh:
                    fh.write(b'\x00')
                return tech([HP[1]], (), 'sha256')
            finally:
                with open(ck, 'wb') as fh:
                    fh.write(raw)
        chk('⑯ 덱을 만든 뒤 체크포인트가 바뀌면 (sha256 다시 계산) TECH', _d16)
        chk('⑰ 덤프 TIMESTEP ≠ 체크포인트 머리 step (settled 폴더에 step 252 덤프) → TECH · 로그의 EXACT_STEP ≠ TIMESTEP 도 TECH',
            lambda: (tech([hp('settled', st=252)], (), 'step')
                     and (open(os.path.join(works['b'], 'log.exact'), 'w').write(f'{STEP_TAG} 301 ckpt b\n') > 0)
                     and tech([HP[2]], (), STEP_TAG)
                     and (open(os.path.join(works['b'], 'log.exact'), 'w').write(f'{STEP_TAG} 300 ckpt b\n') > 0)))
        S2 = os.path.join(td, 'other_run')
        shutil.copytree(S, S2, symlinks=True)
        chk('⑱ 영수증의 런 폴더 ≠ read 에 준 런 폴더 → TECH (다른 런의 체크포인트 덤프)', lambda: tech([HP[1]], (), '런 폴더', run_dir=S2))
        chk('⑲ 영수증 없음 (덤프를 작업 폴더 밖으로 옮김) → TECH (출처 사슬이 끊긴다)',
            lambda: tech([shutil.copyfile(HP[1], os.path.join(td, 'hp_450.liggghts')) and os.path.join(td, 'hp_450.liggghts')], (), RECEIPT_FILE))

        def _d20():
            r_ = read_run(S, HP, G6)
            js = json.loads(R.dumps_strict(r_))
            pv = js['provenance']
            ck = {lab: _sha_file(os.path.join(S, 'restart', f'{lab}.bin')) for lab in CKPTS}
            return (pv['tool_sha256'] == _sha_file(os.path.abspath(__file__)) and pv['reader_sha256'] == _sha_file(R.__file__)
                    and {x['ckpt']: x['sha256'] for x in pv['restarts']} == ck
                    and sorted(x['sha256'] for x in pv['exact_decks']) == sorted(_sha_file(os.path.join(works[l_], DECK_FILE)) for l_ in CKPTS)
                    and sorted(x[2] for x in pv['dumps']) == sorted(_sha_file(p_) for p_ in HP + G6)
                    and pv['deck_source_sha256'] == _sha_file(os.path.join(S, 'in.mixer')) and js['schema'] == SCHEMA)
        chk('⑳ 엄격 JSON (allow_nan=False) · 출처 sha256 — 이 도구 · 판독기 · 체크포인트 셋 · 정확 덱 셋 · 덤프 (hp · g6) · 원 덱', _d20)
        chk('㉑ ★ read 는 런 폴더 · 작업 폴더 셋에 아무것도 쓰지 않는다 (나무 지문 — 이름 · 내용 · 링크 — 이 read 앞뒤 같다)',
            lambda: bool(res) and untouched)

        def _imports():
            tree = ast.parse(open(os.path.abspath(__file__), encoding='utf-8').read())
            got = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module == 'measure_mixing_index':
                    got |= {a.name for a in node.names}
                if isinstance(node, ast.Import) and any(a.name == 'measure_mixing_index' for a in node.names):
                    got.add('*')
            return got

        def keys_rec(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    yield k
                    yield from keys_rec(v)
            elif isinstance(o, list):
                for v in o:
                    yield from keys_rec(v)
        chk('㉒ M 없음 — measure_mixing_index 에서 가져오는 이름 ⊆ 프레임 선택 · bin 식 (deck_plan · planned_t0 · bin_of) · 결과 키에 M · S0 · SR · s2 없음',
            lambda: (_imports() <= FRAME_TOOL_NAMES and res.get('status') == 'OK' and len(res.get('frames') or []) == 3
                     and not (set(keys_rec(res)) & R.M_KEYS)))
        E = _syn_run(td, 'E0_ref_s32452843', atoms, revs=0, ckpt_steps=dict(settled=251))
        try:
            build_deck(E, 'settled', os.path.join(td, 'w_e0'), quiet=True)
            _write_lig(os.path.join(td, 'w_e0', OUT_SUB, 'hp_251.liggghts'), atoms, 251, '.17g')
            re0 = read_run(E, [os.path.join(td, 'w_e0', OUT_SUB, 'hp_251.liggghts')])
        except BaseException as e:                                           # noqa: BLE001
            print(f'        (E0: {type(e).__name__}: {str(e)[:160]})')
            re0 = {}
        chk('㉓ E0 (회전 0 · t₀ 만) — settled 프레임 OK · mode t0_only · bin 없음 (회전 런이 아니다) · t₀ + 1 · g6 없음 = NOT_GIVEN · 정확 값 = 독립 산술',
            lambda: (re0['status'] == 'OK' and re0['mode'] == 't0_only' and re0['frames'][0]['bin'] is None
                     and re0['frames'][0]['in_bin1'] is False and re0['frames'][0]['step_minus_t0'] == 1
                     and re0['frames'][0]['g6']['status'] == 'NOT_GIVEN' and same(re0['frames'][0]['exact'], ex_o)))

        #  ── ㉔ ~ ㉖ 도구 자신의 가드가 실제로 걸리는가 (결함 주입 — 판독기 frame_quantities 를 잠깐 바꾼다) ─────────────────────
        def inject(mod):
            _fq, n_ = R.frame_quantities, [0]

            def fq(D, pm):
                q = _fq(D, pm)
                n_[0] += 1
                mod(q, n_[0] % 2 == 1)                                     # _read_one 은 정확 → 반올림 순서로 부른다
                return q
            R.frame_quantities = fq
            try:
                return read_run(S, [HP[1]])
            finally:
                R.frame_quantities = _fq

        def _hi_wrong(q, is_exact):
            if not is_exact:
                q['resolution']['hi']['se_frac_in_clusters'] = -1.0
        r24 = inject(_hi_wrong)
        chk('㉔ 결함 주입: 반올림 쪽 가능 (hi) 이 정확 값보다 작게 나오면 → TECH "불변식" (값을 내지 않는다)',
            lambda: r24['status'] == 'TECH' and r24['frames'] is None and any('불변식' in s_ for s_ in r24['reasons']))

        def _pairs_wrong(q, is_exact):
            if is_exact:
                q['pairs']['SE-SE'] += 1
        r25 = inject(_pairs_wrong)
        chk('㉕ 결함 주입: 판독기 접촉 수가 독립 재계수 (_pair_audit — 같은 후보 · classify_pairs) 와 다르면 → TECH "도구 불일치"',
            lambda: r25['status'] == 'TECH' and any('도구 불일치' in s_ for s_ in r25['reasons']))
        N2 = _syn_run(td, 'n_plan_33', atoms, meta_patch=lambda m: m.__setitem__('n_atoms_planned', len(atoms) + 2))
        build_deck(N2, 'a', os.path.join(td, 'w_n2'), quiet=True)
        _write_lig(os.path.join(td, 'w_n2', OUT_SUB, 'hp_450.liggghts'), atoms, 450, '.17g')
        r26 = read_run(N2, [os.path.join(td, 'w_n2', OUT_SUB, 'hp_450.liggghts')])
        chk('㉖ t₀ 원자 수 (31) ≠ deck_meta n_atoms_planned (33) → TECH (판독기 analyse_run 과 같은 규칙 — 체크포인트 프레임도 같은 원자 기준)',
            lambda: r26['status'] == 'TECH' and any('n_atoms_planned' in s_ for s_ in r26['reasons']))

        def _d28():
            ra, rb = _R_PLAN['AM_S'], _R_PLAN['SE']
            pa = np.array([0.0123456789012, 0.0111111111111, 0.0105])
            u = np.array([1.0, 1.0, 0.5]) / 1.5
            pb = pa + (ra + rb - 3e-10) * u                                   # AM_S–SE 겹침 0.3 nm — 판독기 반경 바닥 (5e-10 + 5e-11 m) 안
            at = [[1, _TYPE['AM_S'], *pa.tolist(), ra], [2, _TYPE['SE'], *pb.tolist(), rb], [3, _TYPE['SE'], 0.0165, 0.0165, 0.0135, rb]]
            F = _syn_run(td, 'radius_floor', at)
            build_deck(F, 'a', os.path.join(td, 'w_rf'), quiet=True)
            hp_ = os.path.join(td, 'w_rf', OUT_SUB, 'hp_450.liggghts')
            _write_lig(hp_, at, 450, '.17g')
            r_ = read_run(F, [hp_])
            f_ = r_['frames'][0]
            rh = f_['exact']['reader_resolution_on_hp']
            return (r_['status'] == 'OK' and f_['exact']['pairs']['AM_S-SE'] == 1 and f_['exact']['radius_matches_plan_exactly'] is True
                    and f_['exact']['collapsed'] is True and f_['exact']['ambiguous_at_hp'] == {'SE-SE': 0, 'AM_P-SE': 0, 'AM_S-SE': 0}
                    and rh['sigfigs_radius'] == 6 and rh['pairs_lo']['AM_S-SE'] == 0 and rh['pairs_hi']['AM_S-SE'] == 1)
        chk('㉘ ★ 판독기 반경 자릿수 바닥 (S = max(관측, 6) → 반경 반폭 AM 5e-10 · SE 5e-11 m) — 겹침 0.3 nm AM_S–SE 는 판독기 규칙 그대로의 hp 범위에서 '
            '열리지만 (확실 0 · 가능 1), hp 반경 = 계획 템플릿 double (비트 같음) 이면 반올림이 없으므로 hp 정밀도 감사는 모호 0 · 접힘 — 정확 값 = 1 접촉', _d28)

    def _d27():
        pl = deck_plan(os.path.join(root, DECKS['LC'], 'in.mixer'))
        t0, spr = planned_t0(pl), pl['steps_per_rev']
        return ([_where(s_, 250, 160.0, 50, True)['bin'] for s_ in (409, 410, 569, 570)] == [0, 1, 1, 2]
                and _where(410, 250, 160.0, 50, True)['in_bin1'] and not _where(409, 250, 160.0, 50, True)['in_bin1']
                and _bin_window(250, 160.0, 571) == [410, 569]
                and _bin_window(t0, spr, pl['steps_total']) == [4089172, 7139962]
                and _bin_window(t0, spr, pl['steps_total'])[0] <= 4119120 and 7139808 <= _bin_window(t0, spr, pl['steps_total'])[1]
                and [_where(s_, t0, spr, pl['dump_every'], True)['bin'] for s_ in (4089171, 4089172)] == [0, 1])
    chk('㉗ bin 식 경계 = 판독기 bin_of 그대로 — 합성 계획 (t₀ 250 · 바퀴 160) 409 → bin 0 · 410 → 1 · 569 → 1 · 570 → 2 · bin 1 창 [410, 569] · '
        'LC_ref_r2 계획 창 [4,089,172, 7,139,962] (4,089,171 은 bin 0) 이 등록 프레임 4,119,120–7,139,808 을 품는다', _d27)

    print(f'\nmixer_exact_frames selftest: {ok}/{ok + len(fail)} PASS' + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description='믹서 정확 좌표 프레임 — 체크포인트에서 run 0 으로 s1 · s2 의 덤프 해상도 보충 '
                                             '(강성 축 사전등록 §12-4 (나) · 보고 전용 · 관문 아님 · 정의 불변 · M 없음)')
    ap.add_argument('--selftest', action='store_true', help='합성 고정구 셀프테스트 (LIGGGHTS 없음)')
    sub = ap.add_subparsers(dest='cmd')
    d = sub.add_parser('deck', help='작업 폴더에 정확 좌표 덱 · 영수증 · sbatch · 입력 링크 (런 폴더에 쓰지 않는다)')
    d.add_argument('run_dir', help='런 디렉터리 (in.mixer · deck_meta.json · restart/)')
    d.add_argument('--ckpt', required=True, choices=CKPTS, help='settled = write_restart (정착 끝) · a · b = restart N a b 의 두 파일')
    d.add_argument('--work', required=True, help='새 작업 디렉터리 (없거나 비었을 것 · 런 폴더와 서로 포함 관계 아님)')
    d.add_argument('--lmp', default=None, help=f'LIGGGHTS 실행 파일 (기본 = 런의 launch_record.json 의 lmp_realpath, 없으면 {LMP_DEFAULT})')
    d.add_argument('--qos', default=None, help='SLURM QOS (기본 = 런 봉인, 없으면 cpu-60)')
    d.add_argument('--partition', default=None, help='SLURM partition (기본 = 런 봉인, 없으면 cpu)')
    d.add_argument('--time', default=None, help='SLURM 시간 한도 (기본 00:20:00)')
    d.add_argument('--conda-env', default=None, help='sbatch 의 conda env (기본 = 런 봉인, 없으면 myenv)')
    r = sub.add_parser('read', help='hp (%%.17g) · g6 (%%g) 덤프 → 정확 · 등록 규칙 @ %%g · [확실, 가능] (엄격 JSON)')
    r.add_argument('run_dir', help='런 디렉터리 (deck 에 준 것과 같은 폴더)')
    r.add_argument('hp', nargs='+', help='<작업 폴더>/exact/hp_<step>.liggghts (체크포인트마다 하나)')
    r.add_argument('--g6', nargs='+', default=[], help='<작업 폴더>/exact/g6_<step>.liggghts — 주면 에뮬레이션 = LIGGGHTS %%g 텍스트 대조')
    r.add_argument('--json', required=True, help='결과 JSON 경로 (엄격 JSON · allow_nan=False)')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    if a.cmd == 'deck':
        build_deck(a.run_dir, a.ckpt, a.work, lmp=a.lmp,
                   slurm=dict(qos=a.qos, partition=a.partition, time=a.time, conda_env=a.conda_env))
        return 0
    if a.cmd == 'read':
        res = read_run(a.run_dir, a.hp, a.g6)
        report(res)
        with open(a.json, 'w', encoding='utf-8') as f:
            f.write(R.dumps_strict(dict(schema=SCHEMA, registered=REGISTERED, argv=list(sys.argv), result=res)) + '\n')
        print(f'→ {a.json}')
        return 0 if res['status'] == 'OK' else 1
    ap.error('deck · read · --selftest 중 하나')
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
