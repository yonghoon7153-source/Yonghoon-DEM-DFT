#!/usr/bin/env python3
"""ps73 압축 중 스냅숏 덱 — 체크포인트 하나를 읽고 시간을 진행하지 않은 채 (`run 0`) atom · contact · mesh 덤프만 쓴다.

1저자 10-08 *"처음 mesh 랑 닿았을 때, compression 중간, 3100000, 맨 마지막"* (네 시점 von Mises 공동 스케일 그림).  원 런은 압축 중
contact 덤프가 없고 (이완 단계부터) atom 덤프의 c_strs 는 대각 셋뿐이라 von Mises 를 만들 수 없다 → 3,100,000 때처럼 체크포인트에서 접촉을
다시 계산해 덤프한다 (`../snap_3100000_20261008/README.md` 의 만든 법 그대로 · 이 생성기는 그 절차를 다른 step 에도 쓰게 한 것).

덱 = 가지 실험 t0 덱 (`../in.branch_t0_syntax.liggghts`) 의 첫 `run 0` 앞까지 (1저자가 3,100,000 에 쓴 awk 와 같은 자름) 에서 두 줄만 바꾸고
(① 출발 step 검사 `!= 3100000` → `!= S` ② 판 높이 `pz_branch` → 그 step 의 메쉬 덤프 높이) 접촉 덤프 · `run 0` · `print "SNAP_DONE"` 을 붙인다.
판 높이 = 리포의 메쉬 덤프 묶음 (`../../ps73_compaction_curve_20261006/raw/ps73_curve_1.tgz` · 5,000 step 마다 605 장) 의 그 step 값 (평평한 판
— 꼭짓점 z 가 하나가 아니면 거부).  판 STL = `../plate_branch3100000.stl` 과 같은 꼴 (z 만 다름).

run 0 은 입자를 움직이지 않는다 — 접촉 힘은 체크포인트의 위치 · 속도 · 접선 이력에서 다시 계산한 값이다.  판 위치는 벽 접촉에만 쓰인다
(입자–입자 접촉 덤프에는 벽 힘이 없다).

  python3 make_snap_decks.py --steps 1000000 2200000 --out <폴더>     # in.snap_<S>.liggghts · plate_snap_<S>.stl
  python3 make_snap_decks.py --verify 1000000 --log snap.log --snap-atoms post/atom_1000000.liggghts --orig-atoms <원 런 atom_1000000>
  python3 make_snap_decks.py --selftest
"""
import argparse
import hashlib
import os
import re
import sys
import tarfile
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.normpath(os.path.join(HERE, '..'))
T0_DECK = os.path.join(KIT, 'in.branch_t0_syntax.liggghts')
PLATE_3100000 = os.path.join(KIT, 'plate_branch3100000.stl')
MESH_TGZ = os.path.normpath(os.path.join(KIT, '..', 'ps73_compaction_curve_20261006', 'raw', 'ps73_curve_1.tgz'))

STEP_LINE = 'if "${br_step0} != 3100000" then'
PZ_LINE = 'variable pz_branch equal 0.111302'
SNAP_BLOCK = ('dump dmp_contact_snap all local 5000 ${out}/snap/contact_*.liggghts &\n'
              '    c_cpl[1] c_cpl[2] c_cpl[3] c_cpl[4] c_cpl[5] c_cpl[6] c_cpl[7] c_cpl[8] &\n'
              '    c_cpl[9] c_cpl[10] c_cpl[11] c_cpl[12] c_cpl[13] c_cpl[14] c_cpl[15] c_cpl[16] &\n'
              '    c_cpl[17] c_cpl[18] c_cpl[19] c_cpl[20] c_cpl[21] c_cpl[22] c_cpl[23] c_cpl[24] &\n'
              '    c_cpl[25] c_cpl[26]\n'
              'dump_modify dmp_contact_snap first yes\n'
              'run 0\n'
              'print "SNAP_DONE"\n')


# 체크포인트가 최종 궤적의 것인가 — 원 런 로그의 그 step thermo 줄 (README `../../ps73_compaction_curve_20261006/README.md` §2 계보:
# r1 0 → 1,450,000 · r3 → 1,650,000 · r6 → 2,400,000 · r7 → 2,650,000 · r8 → 끝).  스냅숏 setup 줄 KE 가 이 값과 같아야 한다 (재개 G1 과 같은 규칙).
KE_REF = {
    1000000: ('2.3504113e-07', 160420, 'r1 output_ps_7_3_r45_181338.out 4375 행 (restart_settling_1000000 = r1 이 쓴 것 · r4 는 209,000 까지만)'),
    2200000: ('1.1878694e-05', 160420, 'r6 output_ps_7_3_r45_r6_198529.out 3420 행 (restart_compress_2200000 = r6 · r7 은 2,400,000 부터)'),
    3100000: ('1.695918e-05', 160420, 'r8 output_ps_7_3_r45_r8_220537.out 2860 행 (가지 실험 KE_REF 와 같음)'),
}
ATOM_KEYS = ('id', 'type', 'x', 'y', 'z', 'radius', 'vx', 'vy', 'vz')


def setup_ke(log_text, step):
    """스냅숏 로그의 run 0 setup thermo 줄 → (atoms, KE).  머리 줄 (Step … KinEng) 바로 뒤 줄 중 첫 칸이 step 인 것."""
    lines = log_text.splitlines()
    for i, ln in enumerate(lines):
        t = ln.split()
        if len(t) >= 3 and t[0] == 'Step' and 'KinEng' in t:
            for nx in lines[i + 1:i + 3]:
                u = nx.split()
                if len(u) >= 3 and u[0] == str(step):
                    return int(u[1]), float(u[2])
    raise ValueError(f'로그에 step {step} setup thermo 줄이 없다')


def read_dump(path):
    """LIGGGHTS atom 덤프 → {id: 행 dict (문자열 그대로)} · TIMESTEP."""
    with open(path, encoding='ascii') as fh:
        lines = fh.read().splitlines()
    step = int(lines[lines.index('ITEM: TIMESTEP') + 1])
    k = next(i for i, ln in enumerate(lines) if ln.startswith('ITEM: ATOMS'))
    cols = lines[k].split()[2:]
    rows = {}
    for ln in lines[k + 1:]:
        if not ln.strip():
            continue
        v = ln.split()
        d = dict(zip(cols, v))
        rows[int(d['id'])] = d
    return step, cols, rows


def verify(step, log_path, snap_atoms, orig_atoms):
    """체크포인트 내용 검사 — ① setup KE · 원자 수 = 원 런 로그 (상대 1e-6) ② 스냅숏 atom 덤프의 id · type · 위치 · 반경 · 속도 = 원 런
    덤프 (글자 그대로 · 같은 덤프 형식) ③ step 이 둘 다 같다.  하나라도 어긋나면 이 체크포인트는 최종 궤적 것이 아니다 (쓰지 않는다)."""
    out = {'step': step, 'ok': True, 'why': []}
    ref = KE_REF.get(step)
    n, ke = setup_ke(open(log_path, encoding='utf-8', errors='replace').read(), step)
    out['setup'] = {'atoms': n, 'ke': ke}
    if ref:
        kr, nr = float(ref[0]), ref[1]
        out['ref'] = {'atoms': nr, 'ke': kr, 'source': ref[2]}
        if n != nr or not abs(ke - kr) <= 1e-6 * abs(kr):
            out['ok'] = False
            out['why'].append(f'setup KE · 원자 {ke:.8g} · {n} ≠ 원 런 {kr:.8g} · {nr}')
    else:
        out['why'].append('KE 기준값 없음 (KE_REF 에 이 step 이 없다 — ② ③ 만)')
    s1, c1, a = read_dump(snap_atoms)
    s2, c2, b = read_dump(orig_atoms)
    if s1 != step or s2 != step:
        out['ok'] = False
        out['why'].append(f'덤프 step {s1} · {s2} ≠ {step}')
    if set(a) != set(b):
        out['ok'] = False
        out['why'].append(f'원자 id 집합 다름 (스냅숏 {len(a)} · 원 {len(b)})')
    else:
        keys = [k for k in ATOM_KEYS if k in c1 and k in c2]
        bad = [i for i in a if any(a[i][k] != b[i][k] for k in keys)]
        out['n_atoms_compared'] = len(a)
        out['keys_compared'] = keys
        out['n_mismatch'] = len(bad)
        if bad:
            out['ok'] = False
            out['why'].append(f'위치 · 속도 다른 원자 {len(bad)} 개 (예 id {bad[:3]})')
    return out


def cut_before_run0(text):
    """첫 `run 0` 줄 앞까지 (awk '/^run 0/{exit} {print}' 와 같은 답 — 줄 끝 개행 포함)."""
    out = []
    for line in text.splitlines(keepends=True):
        if line.startswith('run 0'):
            return ''.join(out)
        out.append(line if line.endswith('\n') else line + '\n')
    raise ValueError('t0 덱에 run 0 줄이 없다')


def mesh_z(step, tgz=MESH_TGZ):
    """메쉬 덤프 묶음의 그 step 판 높이 (덱 단위 문자열 그대로) — 5,000 배수 · 묶음에 있고 · 평평 (꼭짓점 z 하나) 이어야."""
    if step % 5000:
        raise ValueError(f'step {step} — 메쉬 덤프는 5,000 step 마다 (배수 아님)')
    with tarfile.open(tgz) as t:
        m = [x for x in t.getmembers() if x.isfile() and x.name.endswith(f'/mesh_{step}.stl')]
        if len(m) != 1:
            raise ValueError(f'step {step} — 메쉬 덤프 묶음에 mesh_{step}.stl 이 {len(m)} 개')
        zs = set(re.findall(r'vertex\s+\S+\s+\S+\s+(\S+)', t.extractfile(m[0]).read().decode('ascii')))
    if len(zs) != 1:
        raise ValueError(f'step {step} — 판이 평평하지 않다 (꼭짓점 z {sorted(zs)})')
    z = zs.pop()
    float(z)
    return z


def plate_stl(z):
    v = lambda a, b: f'vertex {a} {b} {z}\n'
    return ('solid plate\n'
            'facet normal 0 0 -1\nouter loop\n' + v('0.0', '0.0') + v('0.05', '0.05') + v('0.05', '0.0') + 'endloop\nendfacet\n'
            'facet normal 0 0 -1\nouter loop\n' + v('0.0', '0.0') + v('0.0', '0.05') + v('0.05', '0.05') + 'endloop\nendfacet\n'
            'endsolid plate\n')


def snap_deck(step, z, t0_text):
    head = cut_before_run0(t0_text)
    for old in (STEP_LINE, PZ_LINE):
        n = head.count(old)
        if n != 1:
            raise ValueError(f't0 덱에서 바꿀 줄 "{old}" 가 {n} 번 (1 번이어야)')
    head = head.replace(STEP_LINE, f'if "${{br_step0}} != {step}" then')
    head = head.replace("기대 3100000 (체크포인트가 다르다)", f"기대 {step} (체크포인트가 다르다)")
    head = head.replace(PZ_LINE, f'variable pz_branch equal {z}')
    note = (f'# ── 스냅숏 (make_snap_decks.py · step {step} · 판 높이 {z} = 메쉬 덤프 mesh_{step}.stl) — 위는 t0 덱의 첫 run 0 앞까지 '
            f'(바꾼 줄 = 출발 step 검사 · pz_branch) · 아래 = 접촉 덤프 + run 0 (시간 진행 없음)\n')
    return head + note + SNAP_BLOCK


def build(steps, out_dir, t0_path=T0_DECK, tgz=MESH_TGZ):
    t0 = open(t0_path, encoding='utf-8').read()
    os.makedirs(out_dir, exist_ok=True)
    rows = []
    for s in steps:
        z = mesh_z(s, tgz)
        deck, stl = snap_deck(s, z, t0), plate_stl(z)
        for name, body in ((f'in.snap_{s}.liggghts', deck), (f'plate_snap_{s}.stl', stl)):
            with open(os.path.join(out_dir, name), 'w', encoding='utf-8', newline='\n') as fh:
                fh.write(body)
        rows.append((s, z))
    return rows


def selftest():
    ok, fail = 0, []

    def chk(name, cond, extra=''):
        nonlocal ok
        if cond:
            ok += 1
            print(f'  PASS  {name}')
        else:
            fail.append(name)
            print(f'  FAIL  {name}  {extra}')

    t0 = open(T0_DECK, encoding='utf-8').read()
    # ① 3,100,000 = 1저자가 돌린 덱 그대로 (awk 자름 + 붙인 덩어리 · 두 줄 바꿈이 같은 값으로 되돌아간다) + 판 STL = 커밋본 바이트
    z31 = mesh_z(3100000)
    d31 = snap_deck(3100000, z31, t0)
    awk = cut_before_run0(t0)
    chk(f'S1 3,100,000 판 높이 = t0 덱 pz_branch ({z31})', z31 == '0.111302')
    chk('S2 3,100,000 덱 = awk 자름 + 주석 한 줄 + 접촉 덤프 덩어리 (1저자 10-08 실행과 같은 명령 줄)',
        d31 == awk + d31[len(awk):] and d31.endswith(SNAP_BLOCK) and d31[len(awk):].count('\n') == SNAP_BLOCK.count('\n') + 1)
    chk('S3 판 STL 3,100,000 = 커밋본 plate_branch3100000.stl 바이트 같음', plate_stl(z31) == open(PLATE_3100000, encoding='utf-8').read())
    # ② 다른 step 은 두 줄만 다르다 (+ 주석 줄)
    z1 = mesh_z(1000000)
    d1 = snap_deck(1000000, z1, t0)
    diff = [(a, b) for a, b in zip(d31.splitlines(), d1.splitlines()) if a != b]
    chk(f'S4 1,000,000 판 높이 0.132302 ({z1})', z1 == '0.132302')
    chk(f'S5 1,000,000 덱 ↔ 3,100,000 덱 = 세 줄만 다름 (step 검사 · pz_branch · 주석) ({len(diff)})',
        len(diff) == 3 and len(d1.splitlines()) == len(d31.splitlines())
        and any('!= 1000000' in b for _, b in diff) and any(b == 'variable pz_branch equal 0.132302' for _, b in diff))
    chk('S6 덱 끝 = run 0 · SNAP_DONE · 그 앞 run 0 없음 (시간 진행 없음)',
        d1.count('\nrun 0\n') == 1 and d1.rstrip().endswith('print "SNAP_DONE"') and '\nrun ' not in d1.replace('\nrun 0\n', '\n'))
    # ③ 거부 — 5,000 배수 아님 · 묶음에 없음 · 평평하지 않은 판 · t0 덱에 바꿀 줄 없음
    for name, fn in (('S7 5,000 배수 아님 거부', lambda: mesh_z(976000)),
                     ('S8 묶음에 없는 step 거부', lambda: mesh_z(9000000)),
                     ('S9 바꿀 줄 없는 덱 거부', lambda: snap_deck(1000000, '0.1', t0.replace(PZ_LINE, 'variable pz_branch equal 0.2'))),
                     ('S10 run 0 없는 덱 거부', lambda: cut_before_run0('a\nb\n'))):
        try:
            fn()
            chk(name, False, '거부 안 함')
        except ValueError:
            chk(name, True)
    with tempfile.TemporaryDirectory() as td:
        tg = os.path.join(td, 'm.tgz')
        src = os.path.join(td, 'post_x')
        os.makedirs(src)
        with open(os.path.join(src, 'mesh_5000.stl'), 'w') as fh:
            fh.write('solid a\nfacet normal 0 0 -1\nouter loop\nvertex 0 0 0.1\nvertex 1 1 0.2\nvertex 1 0 0.1\nendloop\nendfacet\nendsolid a\n')
        with tarfile.open(tg, 'w:gz') as t:
            t.add(src, arcname='post_x')
        try:
            mesh_z(5000, tg)
            chk('S11 기운 판 (꼭짓점 z 둘) 거부', False)
        except ValueError:
            chk('S11 기운 판 (꼭짓점 z 둘) 거부', True)
        rows = build([1000000, 2200000], os.path.join(td, 'out'))
        names = sorted(os.listdir(os.path.join(td, 'out')))
        chk(f'S12 build = 덱 · 판 STL 두 쌍 ({names}) · 2,200,000 판 높이 0.120302',
            names == ['in.snap_1000000.liggghts', 'in.snap_2200000.liggghts', 'plate_snap_1000000.stl', 'plate_snap_2200000.stl']
            and dict(rows)[2200000] == '0.120302')
    # ④ 검사 — 같은 덤프 · 원자 하나 위치 바꿈 · 로그 KE 다름
    with tempfile.TemporaryDirectory() as td:
        def dump(path, step, rows):
            with open(path, 'w') as fh:
                fh.write(f'ITEM: TIMESTEP\n{step}\nITEM: NUMBER OF ATOMS\n{len(rows)}\nITEM: BOX BOUNDS pp pp ff\n0 1\n0 1\n0 1\n'
                         'ITEM: ATOMS id type x y z radius vx vy vz c_strs[1] c_strs[2] c_strs[3] c_ke\n')
                for r in rows:
                    fh.write(' '.join(r) + '\n')
        base = [[str(i), '1', f'0.{i}1', '0.2', '0.3', '0.0045', '1e-6', '0', '-2e-6', '-1', '-2', '-3', '0'] for i in range(1, 5)]
        dump(os.path.join(td, 'o.txt'), 1000000, base)
        same = [r[:9] + ['-1.0000001', '-2', '-3', '0'] for r in base]            # c_strs 끝자리는 달라도 된다 (합산 순서)
        dump(os.path.join(td, 's.txt'), 1000000, same)
        moved = [r[:] for r in same]
        moved[2][4] = '0.30000001'
        dump(os.path.join(td, 'm.txt'), 1000000, moved)
        log_ok = os.path.join(td, 'ok.log')
        open(log_ok, 'w').write('Setting up run ...\n    Step    Atoms         KinEng            CPU       pressMPa \n'
                                '  1000000   160420  2.3504113e-07              0  0.00089837058 \nLoop time of 0\n')
        log_bad = os.path.join(td, 'bad.log')
        open(log_bad, 'w').write('    Step    Atoms         KinEng            CPU       pressMPa \n  1000000   160420  2.4e-07  0  0.0009 \n')
        v1 = verify(1000000, log_ok, os.path.join(td, 's.txt'), os.path.join(td, 'o.txt'))
        chk(f'S13 같은 체크포인트 = 통과 (KE · 원자 · 위치 · 속도 · c_strs 끝자리 무관) {v1["why"]}', v1['ok'] and v1['n_mismatch'] == 0)
        v2 = verify(1000000, log_ok, os.path.join(td, 'm.txt'), os.path.join(td, 'o.txt'))
        chk(f'S14 위치 하나 다름 = 거부 ({v2["why"]})', not v2['ok'] and v2['n_mismatch'] == 1)
        v3 = verify(1000000, log_bad, os.path.join(td, 's.txt'), os.path.join(td, 'o.txt'))
        chk(f'S15 setup KE 다름 = 거부 ({v3["why"]})', not v3['ok'])
        chk('S16 KE 기준값 = 원 런 로그 셋 (1,000,000 r1 · 2,200,000 r6 · 3,100,000 r8 = 가지 실험 KE_REF)',
            set(KE_REF) == {1000000, 2200000, 3100000} and KE_REF[3100000][0] == '1.695918e-05')
    print(f'\n{ok} PASS · {len(fail)} FAIL')
    return 0 if not fail else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description='ps73 압축 중 스냅숏 덱 (체크포인트 → run 0 → atom · contact · mesh 덤프)')
    ap.add_argument('--steps', type=int, nargs='+', help='체크포인트 step (5,000 배수 · 메쉬 덤프 묶음에 있어야)')
    ap.add_argument('--out', help='덱 · 판 STL 을 쓸 폴더')
    ap.add_argument('--verify', type=int, metavar='STEP', help='스냅숏 검사 — 그 step 의 setup KE · 원자 덤프를 원 런과 대조')
    ap.add_argument('--log', help='--verify: 스냅숏 로그 (snap.log)')
    ap.add_argument('--snap-atoms', help='--verify: 스냅숏 atom 덤프 (post/atom_<S>.liggghts)')
    ap.add_argument('--orig-atoms', help='--verify: 원 런 atom 덤프 (post_ps_7_3_r45/atom_<S>.liggghts)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.verify is not None:
        if not (a.log and a.snap_atoms and a.orig_atoms):
            ap.error('--verify 에는 --log · --snap-atoms · --orig-atoms 가 필요하다')
        v = verify(a.verify, a.log, a.snap_atoms, a.orig_atoms)
        print(('✓' if v['ok'] else '✗') + f" step {v['step']} — setup KE {v['setup']['ke']:.8g} · 원자 {v['setup']['atoms']}"
              + (f" (원 런 {v['ref']['ke']:.8g} · {v['ref']['atoms']})" if 'ref' in v else '')
              + f" · 위치 · 속도 다른 원자 {v.get('n_mismatch', '—')} / {v.get('n_atoms_compared', '—')}"
              + ('' if not v['why'] else ' · ' + ' · '.join(v['why'])))
        return 0 if v['ok'] else 2
    if not (a.steps and a.out):
        ap.error('--steps 와 --out 이 필요하다 (또는 --selftest)')
    for s, z in build(a.steps, a.out):
        print(f'step {s}: 판 높이 {z} → in.snap_{s}.liggghts · plate_snap_{s}.stl')
    print('sha256:')
    for n in sorted(os.listdir(a.out)):
        if n.startswith(('in.snap_', 'plate_snap_')):
            print('  ' + hashlib.sha256(open(os.path.join(a.out, n), 'rb').read()).hexdigest()[:16] + '  ' + n)
    return 0


if __name__ == '__main__':
    sys.exit(main())
