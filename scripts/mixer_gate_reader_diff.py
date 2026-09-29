#!/usr/bin/env python3
"""mixer_gate_reader_diff.py — 발사 관문 (`launch_highbo.sh rest` 의 파이썬 블록) ↔ 판독기 (`measure_mixing_index.analyse`)
**차등 시험** (Codex 6 차 Q1 · 2026-09-29 · 1저자 비준 09-28 밤 *"돌려도 돼"*).

왜 — 관문은 bin 0 창의 입력 집합 (파일 · step · bin) 을 판독기와 **따로 구현**한다 (HBR5-02).  `test_launcher.sh HL④o` 는
`STEP_RE` 문자열이 같은지만 본다 — glob 범위 · step 변환 · 중복 · bin 식 · epsilon · t₀ 계산이 앞으로 갈라져도 잡지 못한다
(Codex 6 차 §3).  ⇒ Codex 가 실제로 돌린 경계 사례 여덟을 **같은 합성 폴더**에 두고, 관문 rc 와 판독기 결과가 등록된 표대로
짝을 이루는지 상주 시험한다.  NumPy 로 M 을 다시 계산하는 것이 아니라 **판독기 자신**을 부른다 (Codex: 필수조건 아님 · 우리는 부른다).

| 사례 | 관문 rc | 판독기 |
|---|---:|---|
| smoke_normal | 0 | 진짜 증서 (complete · tech_smoke []) |
| smoke_after_duplicate (bin 0 안 같은 step 복제) | 1 | bin 0 24/25 · complete=false |
| smoke_after_offgrid (bin 0 안 격자 밖 step 410) | 1 | 완전한 25/25 라도 tech_smoke 있음 |
| smoke_after_e0_duplicate (E0 t₀ 덤프 둘) | 1 | t₀ 기준이 유일하지 않음 → 거부 (SystemExit) |
| smoke_after_bin1_duplicate (bin 1 복제) | 0 | 스모크 밖 · complete · tech_smoke [] |
| smoke_with_later_bin_additions (증서 뒤 bin 1+ 프레임 추가) | 0 | 진행 중 생기는 후속 프레임 허용 |
| fractional_duplicate_1200 (1000.25 step/rev · bin 0 의 마지막 step 복제) | 1 | bin 0 25/26 · complete=false |
| fractional_duplicate_1240 (같은 설정 · 첫 bin 1 step 복제) | 0 | complete · tech_smoke [] |

★ 2026-09-30 (강성 축 §5-a 중간 판정 · piece 4) — 같은 방식으로 **bin 3 창**: 사전조건 `mixer_smoke_blind.interim_window_problems` ↔ bin 3 판독
`measure_mixing_index.bin_window_stats` ↔ 전체 판독기 `analyse` (by_rev · expected_by_bin = bin_of 와 따로 쓴 식) — 정상 · bin 3 마지막 복제 · 첫 bin 4 복제 ·
bin 3 결손 · bin_of 변이 판별력 (1000.25 step/rev · bin 3 만 다른 구름).

기록만 (판정 아님 · Codex §3 "증서 신뢰 경계"): `opaque_allowlisted_certificate` (Q5 허용목록 투영만으로 관문 rc 0 — 런처 입력으로
충분하다는 뜻) · `tampered_certificate_narrows_bin0` (증서 `plan.steps_per_rev` 를 손으로 1.0 으로 바꾸면 추가한 복제가 창 밖으로
밀려 rc 0 — 증서 필드는 신뢰된 주장이라 맹검 투영기는 이 필드를 손대면 안 된다.  HBR5-02 재개방 사유 아님).

합성 파일만 · LIGGGHTS · MPI · SLURM 호출 없음.  픽스처는 Codex 6 차 증거 꾸러미 `fixture_helpers.smoke_fixture` 와 같은 기하
(4 × 4 × 24 알 · 덤프 200…8200 간격 40 · t₀ 200 · 16×16×4 · n_min 20 · r 0.013138) 를 리포 모듈로 다시 만든다 (그 파일을 import
하지 않는다 — 증거 사본은 읽기 전용 기록).

    python3 scripts/mixer_gate_reader_diff.py            # 전부 (≈ 5 s)
    python3 scripts/mixer_gate_reader_diff.py --selftest # 같음 (등재 드라이버용)
    python3 scripts/mixer_gate_reader_diff.py --json out.json
"""
from __future__ import annotations

import contextlib
import copy
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent            # scripts/
ROOT = HERE.parent
LAUNCHER = ROOT / 'dem_scripts' / 'mixer_20260921' / 'launch_highbo.sh'
sys.path.insert(0, str(HERE))
import measure_mixing_index as mi          # noqa: E402
import measure_bed_aspect as mba           # noqa: E402
import mixer_deck_diff as dd               # noqa: E402
import check_contact_validity as cv        # noqa: E402
import mixer_restart_phase_test as pt      # noqa: E402

FIRST, REST = 'LH_s32452843', ('LH_s49979687', 'LH_s67867967')
REF = 'E0_s32452843'
REG = dict(r_container=0.013138, cells=16, x_cells=4, n_min=20, axis='x')     # 사전등록 §2-3 · §8 ③ (관문 REG 와 같아야 한다)
#  판독기 입력 규약을 흉내 내는 최소 덱 — dt 1e-3 · 덤프 40 · 삽입 1 · 정착 100+100 · 회전 period 1 (= 1000 step/rev) · 8000 step
DECK = ('timestep .001\ndump dmp all custom 40 post/mix_*.liggghts id type x y z radius\nrun 1\nrun 100\nrun 100\n'
        'fix mvD all move/mesh mesh Drum rotate origin 0 0 0 axis 1 0 0 period 1\nrun 8000\n')


def _sha(p):
    return pt._sha(str(p))


def _js(p, v):
    Path(p).write_text(json.dumps(v, ensure_ascii=False, indent=1), encoding='utf-8')


def _rundir(td, name, deck):
    p = td / name
    (p / 'post').mkdir(parents=True)
    (p / 'in.mixer').write_text(deck, encoding='utf-8')
    for n in ('Drum', 'Front', 'Back'):
        shutil.copyfile(ROOT / f'dem_scripts/mixer_20260919/{n}.stl', p / f'{n}.stl')
    return p


def _cloud(kind):
    """4 (y,z) 모서리 × 4 x-슬랩 × 24 알 (같은 점) — 칸마다 24 ≥ n_min.  seg = 층상 시작 · mid = 부분 혼합 · ref = E0 기준."""
    P, types = [], []
    for j, (y, z) in enumerate([(-.008, -.008), (-.008, .008), (.008, -.008), (.008, .008)]):
        for x in (-.003, -.001, .001, .003):
            for k in range(24):
                P.append([x, y, z])
                if kind == 'seg':
                    types.append(1 if j < 2 else 3)
                else:
                    n_am = {'ref': (10, 14), 'mid': (3, 21), 'mid2': (6, 18)}[kind][0 if j < 2 else 1]
                    types.append(1 if k < n_am else 3)
    P = np.asarray(P)
    n = len(P)
    return dict(id=np.arange(1, n + 1), type=np.asarray(types), x=P[:, 0], y=P[:, 1], z=P[:, 2], radius=np.full(n, 1e-5))


def _dump(p, step, D):
    keys = list(D)
    hdr = f'ITEM: TIMESTEP\n{step}\nITEM: NUMBER OF ATOMS\n{len(D[keys[0]])}\nITEM: BOX BOUNDS ff ff ff\n-1 1\n-1 1\n-1 1\n'
    body = '\n'.join(' '.join(format(float(x), '.17g') for x in row) for row in zip(*(D[k] for k in keys)))
    Path(p).write_text(hdr + 'ITEM: ATOMS ' + ' '.join(keys) + '\n' + body + '\n', encoding='utf-8')


def _bind(run, binary):
    rec = dict(schema=cv.LAUNCH_SCHEMA, run=run.name, stage='first', backend='local', lmp_sha256=_sha(binary),
               lmp_realpath=os.path.realpath(binary),
               sha256={f: _sha(run / f) for f in ('in.mixer', 'Drum.stl', 'Front.stl', 'Back.stl')})
    _js(run / 'launch_record.json', rec)
    return rec


def _gate_code():
    src = LAUNCHER.read_text(encoding='utf-8')
    blocks = re.findall(r"<<'PY'[^\n]*\n(.*?)\nPY\n", src, re.S)
    hit = [b for b in blocks if 'cert, out, first, lmp_path, root' in b]
    if len(hit) != 1:
        raise SystemExit(f'⛔ launch_highbo.sh 의 rest 관문 블록을 찾지 못했다 ({len(hit)} 개)')
    return hit[0]


def _quiet(fn, *a, **kw):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **kw)


def _reader(run, ref):
    try:
        z = _quiet(mi.analyse, str(run), str(ref), REG['r_container'], cells=REG['cells'], x_cells=REG['x_cells'],
                   n_min=REG['n_min'], axis=REG['axis'])
    except SystemExit as e:
        return dict(refused=str(e))
    return dict(complete=z['smoke']['complete'], tech_smoke=list(z['smoke']['tech_smoke']),
                expected=z['smoke']['expected'], present=z['smoke']['present'])


def build(td, deck=DECK):
    """합성 첫 시드 + E0 기준 + 나머지 둘 (코호트) + 봉인 + 진짜 증서 → (run, ref, cert, 증서 원본, invoke)."""
    run = _rundir(td, FIRST, deck)
    ref = _rundir(td, REF, deck.replace('run 8000', 'run 0'))
    for s in range(200, 8201, 40):
        _dump(run / 'post' / f'mix_{s}.liggghts', s, _cloud('seg' if s == 200 else 'mid'))
    _dump(ref / 'post/mix_160.liggghts', 160, _cloud('ref'))
    _dump(ref / 'post/mix_200.liggghts', 200, _cloud('ref'))
    binary = td / 'binary'
    binary.write_bytes(b'mock-identity-not-executed')
    rec = _bind(run, binary)
    for n in REST:
        _rundir(td, n, dd.expected_deck('LH', int(n.split('_s')[1])))
    rec['cohort'] = {n: {f: _sha(td / n / f) for f in ('in.mixer', 'Drum.stl', 'Front.stl', 'Back.stl')} for n in (FIRST,) + REST}
    _js(run / 'launch_record.json', rec)
    v = _quiet(mi.analyse, str(run), str(ref), REG['r_container'], cells=REG['cells'], x_cells=REG['x_cells'],
               n_min=REG['n_min'], axis=REG['axis'])
    cert = td / 'smoke.json'
    _js(cert, [v])
    gate = _gate_code()

    def invoke():
        p = subprocess.run([sys.executable, '-c', gate, str(cert), str(td), FIRST, str(binary), str(ROOT), *REST],
                           capture_output=True, text=True, encoding='utf-8')
        return dict(rc=p.returncode, stdout=p.stdout, stderr=p.stderr)
    return run, ref, cert, v, invoke


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--selftest', action='store_true', help='(등재 드라이버용 · 기본 동작과 같다)')
    ap.add_argument('--json', help='결과 JSON 을 여기에')
    a = ap.parse_args(argv)
    res, fails = {}, []

    def case(name, got, want, note=''):
        ok = all(got.get(k) == v for k, v in want.items())
        res[name] = dict(got=got, want=want, ok=ok)
        print(('  ✓ ' if ok else '  ✗ ') + f'{name}: {note} — got {json.dumps({k: got.get(k) for k in want}, ensure_ascii=False)}')
        if not ok:
            fails.append(name)

    with tempfile.TemporaryDirectory(prefix='gate_reader_diff_') as tmp:
        td = Path(tmp)
        run, ref, cert, original, invoke = build(td / 'smoke')
        case('smoke_normal', dict(rc=invoke()['rc'], **_reader(run, ref)), dict(rc=0, complete=True, tech_smoke=[], expected=25, present=25),
             '진짜 증서 → 관문 0 · 판독기 25/25')
        src, dup = run / 'post/mix_400.liggghts', run / 'post/copy_400.liggghts'
        shutil.copyfile(src, dup)
        case('smoke_after_duplicate', dict(rc=invoke()['rc'], **_reader(run, ref)), dict(rc=1, complete=False, present=24),
             '★ bin 0 안 같은 step (400) 복제 → 관문 1 · 판독기 24/25 complete=false')
        dup.unlink()
        off = run / 'post/mix_410.liggghts'
        off.write_text(src.read_text(encoding='utf-8').replace('ITEM: TIMESTEP\n400\n', 'ITEM: TIMESTEP\n410\n'), encoding='utf-8')
        r_ = _reader(run, ref)
        case('smoke_after_offgrid', dict(rc=invoke()['rc'], complete=r_.get('complete'), present=r_.get('present'),
                                         has_tech=bool(r_.get('tech_smoke'))),
             dict(rc=1, complete=True, present=25, has_tech=True), '★ bin 0 안 격자 밖 step 410 → 관문 1 · 판독기 25/25 인데 tech_smoke 있음')
        off.unlink()
        e0dup = ref / 'post/copy_200.liggghts'
        shutil.copyfile(ref / 'post/mix_200.liggghts', e0dup)
        r_ = _reader(run, ref)
        case('smoke_after_e0_duplicate', dict(rc=invoke()['rc'], refused=('refused' in r_)), dict(rc=1, refused=True),
             '★ E0 t₀ 덤프 둘 → 관문 1 · 판독기 거부 (t₀ 유일하지 않음)')
        e0dup.unlink()
        later = run / 'post/copy_1400.liggghts'
        shutil.copyfile(run / 'post/mix_1400.liggghts', later)
        case('smoke_after_bin1_duplicate', dict(rc=invoke()['rc'], **_reader(run, ref)), dict(rc=0, complete=True, tech_smoke=[], present=25),
             'bin 1 복제 → 스모크 밖 · 관문 0 · 판독기 complete')
        later.unlink()
        early = copy.deepcopy(original)
        early['provenance']['run']['frames'] = mi.frame_bundle([(s, p) for s, p in mba.frames(str(run / 'post')) if 200 <= s < 1200])
        _js(cert, [early])
        case('smoke_with_later_bin_additions', dict(rc=invoke()['rc']), dict(rc=0), '증서가 bin 0 까지만 본 뒤 bin 1+ 프레임이 생겨도 관문 0')
        #  기록 (판정 아님) — Q5 허용목록 투영 · 증서 필드 신뢰 경계
        opaque = {k: copy.deepcopy(original[k]) for k in ('run', 'provenance', 'plan', 't0_step')}
        opaque['smoke'] = dict(complete=original['smoke']['complete'], tech_smoke=original['smoke']['tech_smoke'],
                               qc_repr=dict(**{'pass': original['smoke']['qc_repr']['pass']}))
        _js(cert, [opaque])
        case('opaque_allowlisted_certificate', dict(rc=invoke()['rc']), dict(rc=0),
             '(기록) Q5 허용목록 (run · provenance · plan · t0_step · smoke.complete/tech_smoke/qc_repr.pass) 만으로 관문 0')
        tampered = copy.deepcopy(opaque)
        tampered['plan']['steps_per_rev'] = 1.0
        _js(cert, [tampered])
        shutil.copyfile(src, dup)
        case('tampered_certificate_narrows_bin0', dict(rc=invoke()['rc']), dict(rc=0),
             '(기록 · 신뢰 경계) 증서 plan.steps_per_rev 를 1.0 으로 손대면 복제가 창 밖 → 관문 0 — 맹검 투영기는 이 필드를 손대면 안 된다')
        dup.unlink()
        _js(cert, [original])

        #  비정수 주기 — 1000.25 step/rev: 관문의 bin 식 (floor + 1e-9) 이 판독기와 같은가
        run2, ref2, cert2, orig2, invoke2 = build(td / 'fractional', DECK.replace('period 1\n', 'period 1.00025\n'))
        res['fractional_window'] = dict(steps_per_rev=orig2['plan']['steps_per_rev'], expected=orig2['smoke']['expected'])
        case('fractional_smoke_normal', dict(rc=invoke2()['rc'], expected=orig2['smoke']['expected']), dict(rc=0, expected=26),
             '1000.25 step/rev → bin 0 = 26 장 · 관문 0')
        for step, want_rc, want_c in ((1200, 1, False), (1240, 0, True)):
            d_ = run2 / f'post/copy_{step}.liggghts'
            shutil.copyfile(run2 / f'post/mix_{step}.liggghts', d_)
            case(f'fractional_duplicate_{step}', dict(rc=invoke2()['rc'], **_reader(run2, ref2)), dict(rc=want_rc, complete=want_c),
                 f'★ step {step} 복제 ({"bin 0 마지막" if step == 1200 else "첫 bin 1"}) → 관문 {want_rc} · 판독기 complete={want_c}')
            d_.unlink()

        #  ★ 판별력 — 관문의 bin 식 (floor((s − t₀)/spr + 1e-9)) 이 판독기와 갈라지면 (예: epsilon 0.5) 위 표가 깨지는가.
        #    (규율 ②: 시험이 "틀린 코드" 를 실제로 잡는지 — 정규식 문자열 대조 HL④o 는 이것을 못 본다)
        mut = _gate_code().replace('math.floor((s_ - t0) / spr + 1e-9) == 0', 'math.floor((s_ - t0) / spr + 0.5) == 0')
        assert mut != _gate_code(), '관문의 bin 식을 찾지 못했다 — 변이 시험 무효'
        d_ = run2 / 'post/copy_1200.liggghts'
        shutil.copyfile(run2 / 'post/mix_1200.liggghts', d_)
        pm = subprocess.run([sys.executable, '-c', mut, str(cert2), str(td / 'fractional'), FIRST, str(td / 'fractional' / 'binary'),
                             str(ROOT), *REST], capture_output=True, text=True, encoding='utf-8')
        d_.unlink()
        case('mutation_bin_epsilon_detected', dict(rc_mutated=pm.returncode), dict(rc_mutated=0),
             '★ 관문 bin 식을 epsilon 0.5 로 변이 → 같은 복제 (1200) 가 rc 0 (등록 1 과 다름) = 이 시험이 갈라짐을 잡는다')

        #  ★ 중간 판정 (강성 축 §5-a · bin 3 = 4 바퀴 · 2026-09-30 piece 4) — 사전조건 (mixer_smoke_blind.interim_window_problems = bin_window_files)
        #    ↔ bin 3 판독 (measure_mixing_index.bin_window_stats) ↔ 전체 판독기 analyse.  analyse 의 bin 묶음 (by_rev) · 계획 격자 (expected_by_bin) 는
        #    bin_of 와 **따로 쓴 식** 이다 — 셋이 갈라지면 이 표가 깨진다.  bin 3 프레임만 다른 구름 (mid2) 이라 창이 한 장이라도 밀리면 평균이 바뀐다.
        import mixer_smoke_blind as sb
        fdeck = DECK.replace('period 1\n', 'period 1.00025\n')
        spr_f = 1000.25
        b3 = [s for s in range(200, 8201, 40) if int(np.floor((s - 200) / spr_f + 1e-9)) == 3]      # 3240 … 4200 (25 장)
        irun = _rundir(td / 'interim', 'LC_ref_r8_s15485863', fdeck)
        iref = _rundir(td / 'interim', 'E0_ref_s15485863', fdeck.replace('run 8000', 'run 0'))
        _dump(iref / 'post/mix_200.liggghts', 200, _cloud('ref'))
        for s in range(200, 8201, 40):
            _dump(irun / 'post' / f'mix_{s}.liggghts', s, _cloud('seg' if s == 200 else ('mid2' if s in b3 else 'mid')))

        def _interim():
            pre = sb.interim_window_problems(str(irun))
            w = _quiet(mi.bin_window_stats, str(irun), str(iref), REG['r_container'], 3, cells=REG['cells'], x_cells=REG['x_cells'],
                       n_min=REG['n_min'], axis=REG['axis'])
            z = _quiet(mi.analyse, str(irun), str(iref), REG['r_container'], cells=REG['cells'], x_cells=REG['x_cells'], n_min=REG['n_min'],
                       axis=REG['axis'])
            r3 = z['by_rev'].get(3) or {}
            return dict(pre_ok=not pre, stats_complete=bool(w['complete']), reader_complete=r3.get('n') == z['lattice']['expected_by_bin'].get(3),
                        same_M=bool(w['M_bin'] is not None and r3.get('M_mean') is not None and abs(w['M_bin'] - r3['M_mean']) < 1e-12))
        case('interim_bin3_normal', _interim(), dict(pre_ok=True, stats_complete=True, reader_complete=True, same_M=True),
             '1000.25 step/rev · bin 3 = 3240 … 4200 — 사전조건 통과 · bin 3 판독 완전 · 전체 판독기 bin 3 25/25 · 같은 M')
        for step, ok_ in ((4200, False), (4240, True)):
            d_ = irun / f'post/copy_{step}.liggghts'
            shutil.copyfile(irun / f'post/mix_{step}.liggghts', d_)
            case(f'interim_duplicate_{step}', _interim(), dict(pre_ok=ok_, stats_complete=ok_, reader_complete=ok_, **({'same_M': True} if ok_ else {})),
                 f'★ step {step} 복제 ({"bin 3 마지막" if step == 4200 else "첫 bin 4"}) → 사전조건 · bin 3 판독 · 전체 판독기 모두 {"통과" if ok_ else "불완전"}')
            d_.unlink()
        miss = irun / 'post/mix_4200.liggghts'
        keep = miss.read_text(encoding='utf-8')
        miss.unlink()
        case('interim_missing_4200', _interim(), dict(pre_ok=False, stats_complete=False, reader_complete=False),
             '★ bin 3 마지막 계획 덤프 없음 (= 아직 4 바퀴 전) → 셋 다 불완전')
        miss.write_text(keep, encoding='utf-8')
        real_bo = mi.bin_of
        mi.bin_of = lambda s_, t0_, spr_: int(np.floor((s_ - t0_) / spr_ + 0.5))
        try:
            mut_i = _interim()
        finally:
            mi.bin_of = real_bo
        case('mutation_interim_bin_epsilon_detected', dict(same_M=mut_i['same_M'], pre_ok=mut_i['pre_ok']), dict(same_M=False, pre_ok=True),
             '★ bin_of 를 epsilon 0.5 로 변이 → 사전조건은 여전히 통과하지만 bin 3 판독이 전체 판독기의 bin 3 (따로 쓴 식) 과 갈라진다 = 이 시험이 잡는다')

    res['scope'] = ('합성 파일만 · 관문 = launch_highbo.sh rest 의 파이썬 블록 (추출 실행) · 판독기 = measure_mixing_index.analyse · '
                    'LIGGGHTS/MPI/SLURM 없음')
    if a.json:
        _js(a.json, res)
    print()
    if fails:
        print(f'✗ {len(fails)} 건 불일치: {fails}')
        return 1
    print('✓ 전부 통과 — 관문 rc ↔ 판독기 결과가 등록된 표 (Codex 6 차 §3) 대로 짝을 이룬다.  '
          '⚠ 합성 폴더의 시험이다 — 실제 런의 스모크는 사람이 §8 ①–④ 를 확인한다')
    return 0


if __name__ == '__main__':
    sys.exit(main())
