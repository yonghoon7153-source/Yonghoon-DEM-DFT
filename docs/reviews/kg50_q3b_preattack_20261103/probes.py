"""Q3 (나) 사전 공격 탐침 — 시험 하네스 (scripts/test_resume_ckpt.py) 의 합성 장면 함수를 그대로 써서 도구 (scripts/resume_ckpt.sh) 를 돌린다.
도구 원본은 안 건드린다.  usage: python3 docs/reviews/kg50_q3b_preattack_20261103/probes.py [P1 P2 P3 P4 …]"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import test_resume_ckpt as T  # noqa: E402

SCRIPT = os.path.join(ROOT, 'scripts/resume_ckpt.sh')
C = T.C
ck = 'restart_%s/restart_compress_1000000.bin' % C
mf = T.qb_main(case=C)
raw = T.qb_raw(mf, C, ck)
st17 = 'plate_%s_%s.stl' % (C, T.SFX)


def show(tag, r, extra=''):
    g = re.findall(r'^- (G[0-3][^\n]*)', r['rep'], re.M)
    ph = re.findall(r'압축 루프 재개 준비 \(Q3 \(나\)[^\n]*', r['out'])
    print('[%s] trial=%s main=%s' % (tag, r['trial'], r['main']))
    for x in ph[-1:]:
        print('   tool:', x[:260])
    for x in g:
        print('   ', x[:200])
    if extra:
        print('   ', extra)


def slot_order(cmds):
    """LIGGGHTS/LAMMPS Modify::add_fix 규칙: 같은 ID 다시 정의 = 같은 칸에 바꿔 넣음 · unfix = 칸 지움 · 새 ID = 끝에 붙임 (템플릿 · property/global 제외하고 보임)"""
    out = []
    for l in cmds:
        w = l.split()
        if not w:
            continue
        if w[0] == 'fix' and len(w) >= 4:
            if w[3].startswith(('property/global', 'particletemplate', 'particledistribution')):
                continue
            if w[1] in out:
                continue                     # 같은 칸 (자리 그대로)
            out.append(w[1])
        elif w[0] == 'unfix' and len(w) >= 2 and w[1] in out:
            out.remove(w[1])
    return out


def prefix_main(text):
    L = T.nocomment(text)
    return L[:[i for i, l in enumerate(L) if l.strip().startswith('label loop_press')][0]]


def prep_resume(text):
    L = T.nocomment(text)
    a = [i for i, l in enumerate(L) if l.strip().startswith('read_restart')][0]
    b = [i for i, l in enumerate(L) if l.strip().startswith('label loop_press')][0]
    return L[a + 1:b]


def P1():
    # 루프 위상을 본 덱 run 합에서만 정한다 — 체크포인트를 쓴 런의 원 로그 (판정 step) 와 대조하지 않는다.
    #   원 로그를 루프 진입 E' (≠ 본 덱의 400,002) 로 만든다: 원 런은 1,000,001 (또는 1,002,502) 에 판정했는데 도구는 run 2 → 1,000,002 판정.
    for E_log, why in ((400001, '원 런 판정 = 1,000,001 (1 step 어긋남 · 첫 긴 run off-by-one 꼴)'),
                       (397502, '원 런 판정 = 997,502 · 1,002,502 (반 주기 어긋남 · 작업 폴더 본 덱 ≠ 실제로 돈 덱)')):
        log = T.qb_orig_log(E_log, 5000, 1000000)
        js = re.findall(r'^\s*(\d+) .*\nLoop time', log, re.M)
        r = T.qb_flow(SCRIPT, mf, raw, 1000000, T.qb_trial_log(1000000, [2, 1998]), E_log, 5000)
        show('P1 E_log=%d' % E_log, r, '원 로그 판정 step (Loop time 앞 줄) 끝 셋 = %s · %s' % (js[-3:], why))


def P2():
    # LIGGGHTS 칸 순서 (다시 정의 = 첫 정의 칸 · unfix+fix = 끝) ↔ 순서 고침 결과 (마지막 정의 줄 순서).
    raw17 = T.qb_raw(mf, C, ck, order='r075', stl=st17)
    r = T.qb_flow(SCRIPT, mf, raw17, 1000000, T.qb_trial_log(1000000, [2, 1998]), 400002, 5000, stl_more=(st17,))
    wd = r['w_decks'].get('input_%s_%s.liggghts' % (C, T.SFX), b'').decode('utf-8', 'replace')
    so_m, so_r, so_raw = slot_order(prefix_main(mf)), slot_order(prep_resume(wd)), slot_order(prep_resume(raw17))
    show('P2a 실제 D0.7 덱 꼴 (QB17 장면)', r)
    print('    원 런 체크포인트 때 fix 칸 순서 :', so_m)
    print('    도구 순서 고침 뒤 재개 덱 칸 순서:', so_r)
    print('    dem_restart.py 산출 그대로 칸 순서:', so_raw)
    # 같은 꼴에 비가환 fix (setforce) 하나 — 본 덱: gravi 98.1 바로 뒤에 fz · 재개 덱: integr 바로 뒤에 fz (dem_restart.py 꼴)
    fz = 'fix fz g_se_ins setforce NULL NULL 0.0'
    mfz = T.qb_main(case=C, extra=[('fix gravi all gravity 98.1 vector 0.0 0.0 -1.0', 'fix gravi all gravity 98.1 vector 0.0 0.0 -1.0\n' + fz)])
    rawz = T.qb_raw(mfz, C, ck, order='r075', stl=st17).replace('fix integr all nve/sphere\n', 'fix integr all nve/sphere\n' + fz + '\n', 1)
    assert rawz.count(fz) == 1
    r = T.qb_flow(SCRIPT, mfz, rawz, 1000000, T.qb_trial_log(1000000, [2, 1998]), 400002, 5000, stl_more=(st17,))
    wd = r['w_decks'].get('input_%s_%s.liggghts' % (C, T.SFX), b'').decode('utf-8', 'replace')
    show('P2b + 비가환 fix setforce (본 덱 gravi 다음 칸)', r,
         '정적 대조 %s' % ('통과' if '재개 덱 정적 대조: 통과' in r['out'] else '거부'))
    print('    원 런 칸 순서 :', slot_order(prefix_main(mfz)))
    print('    도구 재개 덱  :', slot_order(prep_resume(wd)))
    # LIGGGHTS 와 같은 칸 순서로 낸 재개 덱 (gravi 9.81 → fz → 판 메시 …) 은 정적 대조가 거부하는가
    rawL = T.qb_raw(mfz, C, ck, order='r075', stl=st17)
    g981 = 'fix gravi all gravity 9.81 vector 0.0 0.0 -1.0\n'
    rawL = rawL.replace('fix integr all nve/sphere\n' + g981, 'fix integr all nve/sphere\n' + g981 + fz + '\n', 1)
    assert rawL.count(fz) == 1
    r = T.qb_flow(SCRIPT, mfz, rawL, 1000000, T.qb_trial_log(1000000, [2, 1998]), 400002, 5000, stl_more=(st17,))
    wd = r['w_decks'].get('input_%s_%s.liggghts' % (C, T.SFX), b'').decode('utf-8', 'replace')
    show('P2c 원 런과 같은 칸 순서 (gravi 9.81 · fz 를 integr 뒤) 로 낸 재개 덱', r,
         '정적 대조 %s · 도구 재개 덱 칸 %s' % ('통과' if '재개 덱 정적 대조: 통과' in r['out'] else '거부', slot_order(prep_resume(wd))))


def P3():
    # 원 런이 체크포인트 전에 지운 fix (ins_mix · unfix) 를 재개 덱 준비 구간에 둠 → 순서 고침이 본 덱 자리 (삽입) 로 옮김 → 정적 대조?
    insl = ('fix ins_mix all insert/pack seed 15900013 distributiontemplate pdd_mix maxattempt 3000 insert_every once overlapcheck yes '
            'all_in no vel constant 0.0 0.0 -0.5 region reg_mix volumefraction_region 0.321')   # 본 덱 120–124 줄 (& 이음) 을 한 줄로
    raw17 = T.qb_raw(mf, C, ck, order='r075', stl=st17)
    rawi = raw17.replace('fix integr all nve/sphere\n', insl + '\nfix integr all nve/sphere\n', 1)
    r = T.qb_flow(SCRIPT, mf, rawi, 1000000, T.qb_trial_log(1000000, [2, 1998]), 400002, 5000, stl_more=(st17,))
    probs = [l for l in r['out'].splitlines() if 'ins_mix' in l][:3]
    show('P3 체크포인트 전에 unfix 된 ins_mix 를 준비 구간에', r, ' | '.join(p.strip()[:200] for p in probs))


def P4():
    # 같은 명령 n 번 (재개 덱) < m 번 (본 덱) — 재개 덱에 thermo 1000 한 번만 (본 덱 155 · 212 두 자리) → 마지막 자리로 가는가
    raw17 = T.qb_raw(mf, C, ck, order='r075', stl=st17)
    i = raw17.index('thermo_style    custom step atoms ke cpu\n')
    j = raw17.index('\n', raw17.index('thermo', i + 10)) + 1
    raw1 = raw17[:i] + raw17[j:]
    assert raw1.count('thermo 1000') + raw1.count('thermo          1000') == raw17.count('thermo 1000') + raw17.count('thermo          1000') - 1
    r = T.qb_flow(SCRIPT, mf, raw1, 1000000, T.qb_trial_log(1000000, [2, 1998]), 400002, 5000, stl_more=(st17,))
    mv = re.findall(r'\[thermo[^\]]*\] → 본 덱 \d+ 줄 자리', r['out'])
    show('P4 thermo 1000 한 번 (본 덱 두 자리)', r, '옮김: %s' % mv)


if __name__ == '__main__':
    for n in (sys.argv[1:] or ['P1', 'P2', 'P3', 'P4']):
        globals()[n]()
