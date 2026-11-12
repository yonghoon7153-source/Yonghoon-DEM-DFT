#!/usr/bin/env python3
"""P1 G2c' 초안 A (8a2f9938ba71) · B (9c8bcdc260d3) 3 회차 고침 — 마지막 확인 산술 (내부 반박 리뷰 · Codex 아님 · 11-12).

읽기만 · 작은 산술 · LIGGGHTS · ibb · 네트워크 없음 · f3_choice.py 를 부르지 않고 같은 정의를 따로 짰다.
  W     = Σ_{reset_like} |Ft_원| / Σ_{공통} |Ft_원| · reset_like = |Ft − Ft_원| > 0.5 |Ft_원| (|Ft_원| > 0)
  칸    = 원쪽 덤프 BOX BOUNDS 의 x · y 를 P × Q 로 고르게 나눔 · 자리 = 감은 pos · 경계 1e-12·L 안 = 애매 (뺌)
  안쪽  = 두 원자 다 같은 칸 · 애매 아님 · 칸 하중 쌍 N = 안쪽 공통 쌍 중 |Ft_원| > 0
  규칙  = 전역 W ≤ 0.05 ∧ 칸마다 (N ≥ 100 이면) W_c ≤ 0.5 · 칸 하나라도 N < 100 = 계산 못 함 (UNCONFIRMED)
  소실  = 시험 쪽 Ft → 0 (감쇠 몫 무시 [추정]) · 정직 배경 = B (주기 파일) ↔ A(N)
부분: [W] 덤프 산술 · [P] 경로 규칙 손 반례 (임시 폴더 · 심볼릭) · [F] 첫 낱말 규칙 · [K] 합성 RJ 쌍 수 · [L] 장부 ↔ sacct 손 반례.
쓰는 법: python3 -I r4_check.py <run40000 폴더>
"""
import itertools
import math
import os
import sys
import tempfile

D = sys.argv[1]
NMIN, TAU_C, TAU_G = 100, 0.5, 0.05


def load(path):
    with open(path) as f:
        L = f.read().splitlines()
    ib = next(i for i, l in enumerate(L) if l.startswith('ITEM: BOX BOUNDS'))
    (xlo, xhi), (ylo, yhi) = (tuple(float(t) for t in L[ib + k].split()[:2]) for k in (1, 2))
    ie = next(i for i, l in enumerate(L) if l.startswith('ITEM: ENTRIES'))
    assert len(L[ie].split()) - 2 == 30
    rows = {}
    for ln in L[ie + 1:]:
        if not ln.strip():
            continue
        v = [float(t) for t in ln.split()]
        a, b = int(v[6]), int(v[7])
        p1, p2, ft = (v[0], v[1]), (v[3], v[4]), (v[15], v[16], v[17])
        if a > b:                                   # 작은 id 먼저 · 위치 맞바꿈 · 접선력 부호 반전
            p1, p2, ft, a, b = p2, p1, tuple(-t for t in ft), b, a
        assert (a, b) not in rows
        rows[(a, b)] = (p1, p2, ft)
    return rows, (xlo, xhi - xlo, ylo, yhi - ylo)


def nrm(t):
    return math.sqrt(sum(x * x for x in t))


def judge(T, O, lost=frozenset()):
    out = {}
    for k in O.keys() & T.keys():
        fo = O[k][2]
        ft = (0.0, 0.0, 0.0) if k in lost else T[k][2]
        w = nrm(fo)
        out[k] = (w, w > 0 and nrm([a - b for a, b in zip(ft, fo)]) > 0.5 * w)
    return out


def W(pp, keys=None):
    ks = list(pp) if keys is None else list(keys)
    den = sum(pp[k][0] for k in ks)
    return (sum(pp[k][0] for k in ks if pp[k][1]) / den) if den > 0 else None


def cidx(x, lo, L, P):
    u = (x - lo) % L
    return min(int(u / L * P), P - 1), any(abs(u - L * k / P) <= 1e-12 * L for k in range(P + 1))


def cell_of(p, box, P, Q):
    (cx, ax), (cy, ay) = cidx(p[0], box[0], box[1], P), cidx(p[1], box[2], box[3], Q)
    return (cx, cy), (ax or ay)


def inner_cells(O, box, P, Q):
    cells, amb = {}, 0
    for k, (p1, p2, _) in O.items():
        c1, a1 = cell_of(p1, box, P, Q)
        c2, a2 = cell_of(p2, box, P, Q)
        if a1 or a2:
            amb += 1
        elif c1 == c2:
            cells.setdefault(c1, set()).add(k)
    return cells, amb


def cell_table(pp, cells, P, Q):
    out = []
    for c in itertools.product(range(P), range(Q)):
        ks = [k for k in cells.get(c, ()) if pp[k][0] > 0]
        out.append((c, len(ks), W(pp, ks) if ks else None))
    return out


def verdict(pp, cells, P, Q, first='viol'):
    """규칙 그대로 · first='viol' = 위반 먼저 (VM 이 계산 못 함보다 앞) · 'unc' = 계산 못 함 먼저."""
    g = W(pp)
    tab = cell_table(pp, cells, P, Q)
    low = any(n < NMIN for _, n, _ in tab)
    viol = (g is not None and g > TAU_G) or any(n >= NMIN and w is not None and w > TAU_C for _, n, w in tab)
    if first == 'unc' and low:
        return 'UNC'
    return 'VM' if viol else ('UNC' if low else 'PASS')


def caught_value_only(pp, cells, P, Q):
    """칸 값만 (N 하한 무시 · f3_choice 의 (b) 셈과 같은 뜻): 전역 > 0.05 ∨ 어느 칸 W_c > 0.5."""
    g = W(pp)
    return (g is not None and g > TAU_G) or any(w is not None and w > TAU_C for _, _, w in cell_table(pp, cells, P, Q))


def region_pairs(O, box, xr, yr):
    """두 원자 다 영역 [x0, x1) × [y0, y1) (감은 자리 · 주기) 안인 쌍."""
    xlo, Lx, ylo, Ly = box

    def inside(p):
        u, w = (p[0] - xlo) % Lx, (p[1] - ylo) % Ly
        okx = ((u - xr[0]) % Lx) < (xr[1] - xr[0])
        oky = ((w - yr[0]) % Ly) < (yr[1] - yr[0])
        return okx and oky
    return frozenset(k for k, (p1, p2, _) in O.items() if inside(p1) and inside(p2))


A, box = load(f'{D}/A/post/c_40000.txt')
B, _ = load(f'{D}/B/post/c_40000.txt')
C, _ = load(f'{D}/C/post/c_40000.txt')
print('[W] 덤프 산술 (샌드박스 11-12 · 받은 묶음 · 리포 밖)')
print(f'  상자 x {box[1]} · y {box[3]} · 쌍 A {len(A)} · B {len(B)} · C {len(C)}')
ppB, ppC = judge(B, A), judge(C, A)
WB, WC = W(ppB), W(ppC)
print(f'  정직 전역 W: B {WB:.6f} (×{TAU_G / WB:.1f}) · C {WC:.6f} (×{TAU_G / WC:.1f})')
fts = sorted((nrm(A[k][2]) for k in A), reverse=True)
k73 = round(685 / 562605 * len(fts))
Wp = sum(fts[:k73]) / sum(fts)
print(f'  교차 NP 최악 대리 [추정]: 7:3 몫 685/562605 → 이 침대 {k73} 쌍 · |Ft| 상위면 W {Wp:.4f} (×{TAU_G / Wp:.2f})')
print(f'  생산 7:3 안쪽 몫 (11-02 ibb_result 141–147 행 local 476046 / 562605) = {476046 / 562605:.4f} · 칸 평균 안쪽 쌍 {476046 / 24:.0f} '
      f'(discriminating_frac 1.0 = 모든 쌍 |Ft| > 0 · 323957 판정 기록)')

GRIDS = ((6, 4, '7:3 RJ 쓴 NP 24'), (11, 1, '10:0 RJ 쓴 NP 11'), (5, 1, '0:10 · 5:5 쓴 NP 5'), (2, 2, '3:7 쓴 NP 4'), (3, 2, 'RJ2 쓴 EXT NP 6'))
for P, Q, lab in GRIDS:
    cells, amb = inner_cells(A, box, P, Q)
    tB, tC = cell_table(ppB, cells, P, Q), cell_table(ppC, cells, P, Q)
    ns = [n for _, n, _ in tB]
    mx = max((r for r in tB if r[2] is not None), key=lambda r: r[2])
    ok = [r for r in tB if r[1] >= NMIN and r[2] is not None]
    mx_ok = max(ok, key=lambda r: r[2]) if ok else None
    print(f'-- {P}x{Q} ({lab}) · 칸 {P * Q} · 안쪽 쌍 {sum(len(v) for v in cells.values())} · 애매 {amb} · 칸 하중 쌍 {min(ns)}–{max(ns)} · '
          f'N<{NMIN} 칸 {sum(n < NMIN for n in ns)}')
    print(f'   정직 B 칸 W 최대 {mx[2]:.4f} (칸 {mx[0]} · N {mx[1]} · ×{TAU_C / mx[2]:.1f})'
          + (f' · N≥{NMIN} 칸만 최대 {mx_ok[2]:.4f} (칸 {mx_ok[0]} · N {mx_ok[1]} · ×{TAU_C / mx_ok[2]:.1f})' if mx_ok else ' · N≥100 칸 없음')
          + f' · C 최대 {max(w for _, _, w in tC if w is not None):.4f}')
    print(f'   규칙 그대로 정직 판정: B {verdict(ppB, cells, P, Q)} · C {verdict(ppC, cells, P, Q)}')
    # 칸 하나 통째 (안쪽 쌍만 = L2)
    res = {'viol': {}, 'unc': {}}
    val = 0
    for c in itertools.product(range(P), range(Q)):
        pp = judge(B, A, frozenset(cells.get(c, ())))
        for f in res:
            v = verdict(pp, cells, P, Q, f)
            res[f][v] = res[f].get(v, 0) + 1
        val += caught_value_only(pp, cells, P, Q)
    print(f'   칸 하나 안쪽 쌍 통째 소실 (L2): 칸 값만 잡힘 {val}/{P * Q} · 규칙 그대로 (위반 먼저) {res["viol"]} · (계산 못 함 먼저) {res["unc"]}')
    # 반 칸 (공간 · x 왼쪽 반) · 두 칸 걸침 (칸 크기 · x 로 반 칸 밀림)
    wx, wy = box[1] / P, box[3] / Q
    half_c, half_g, half_k, two_c, two_g, two_k = [], [], 0, [], [], 0
    for cx, cy in itertools.product(range(P), range(Q)):
        lost = region_pairs(A, box, (cx * wx, cx * wx + wx / 2), (cy * wy, (cy + 1) * wy))
        pp = judge(B, A, lost)
        wc = W(pp, [k for k in cells.get((cx, cy), ()) if pp[k][0] > 0])
        half_c.append(wc)
        half_g.append(W(pp))
        half_k += caught_value_only(pp, cells, P, Q)
        lost2 = region_pairs(A, box, (cx * wx + wx / 2, cx * wx + 1.5 * wx), (cy * wy, (cy + 1) * wy))
        pp2 = judge(B, A, lost2)
        two_c.append(max(w for _, _, w in cell_table(pp2, cells, P, Q) if w is not None))
        two_g.append(W(pp2))
        two_k += caught_value_only(pp2, cells, P, Q)
    print(f'   반 칸 소실 (x 왼쪽 반 · 두 원자 다 그 안): 칸 W {min(half_c):.3f}–{max(half_c):.3f} · 전역 {min(half_g):.4f}–{max(half_g):.4f} · '
          f'잡힘 (칸 값만) {half_k}/{P * Q}')
    print(f'   두 칸 걸친 소실 (칸 크기 · x 반 칸 밀림): 칸 W 최대 {min(two_c):.3f}–{max(two_c):.3f} · 전역 {min(two_g):.4f}–{max(two_g):.4f} · '
          f'잡힘 (칸 값만) {two_k}/{P * Q}')
    if P != Q:                                     # 쓴 격자 축 맞바꿈 (P by Q 를 y · x 로 읽음)
        cs, _ = inner_cells(A, box, Q, P)
        hit = [c for c in itertools.product(range(P), range(Q)) if caught_value_only(judge(B, A, frozenset(cells.get(c, ()))), cs, Q, P)]
        xs = sorted({c[0] for c in hit})
        print(f'   축 맞바꿈 ({Q}x{P} 로 셈) · 참 {P}x{Q} 칸 하나 안쪽 쌍 소실 잡힘 (칸 값만) {len(hit)}/{P * Q} · 잡힌 참 칸의 x 번호 {xs}')
    if (P, Q) == (6, 4):                           # 곱이 같은 다른 격자로 셈
        for P2, Q2 in ((8, 3), (12, 2), (3, 8), (24, 1)):
            cs, _ = inner_cells(A, box, P2, Q2)
            k2 = sum(caught_value_only(judge(B, A, frozenset(cells.get(c, ()))), cs, P2, Q2) for c in itertools.product(range(P), range(Q)))
            print(f'   틀린 격자 {P2}x{Q2} 로 셈 (곱 24 = 사전 점검 통과 꼴) · 참 6x4 칸 소실 잡힘 (칸 값만) {k2}/24')

print('[P] 경로 규칙 손 반례 (A 15-5 PASS 행 그대로: (i) rt1_bin = rt2_ckpt = 로그 경로 = job_dir + /RT1/rt.bin 글자 · (ii) realpath(job_dir) = realpath(판독 잡 폴더))')


def rule(rec, reader):
    exp = rec['job_dir'] + '/RT1/rt.bin'
    return (rec['rt1_bin'] == exp and rec['rt2_ckpt'] == exp and rec['log'] == exp
            and os.path.realpath(rec['job_dir']) == os.path.realpath(reader))


def rec_of(jd, rt1=None, rt2=None, log=None):
    p = jd + '/RT1/rt.bin'
    return {'job_dir': jd, 'rt1_bin': rt1 or p, 'rt2_ckpt': rt2 or p, 'log': log or p}


with tempfile.TemporaryDirectory(prefix='r4_path_', dir=os.path.dirname(os.path.abspath(__file__))) as td:
    real = os.path.join(td, 'LUSTRE_HOME')
    for sub in ('w/bed/RJ/RT1', 'w/bed/RJ.t1/RT1', 'other/w/bed/RJ/RT1'):
        os.makedirs(os.path.join(real, sub))
    link = os.path.join(td, 'HOME')
    os.symlink(real, link)
    link2 = os.path.join(td, 'ALIAS')               # 링크의 링크 (사슬)
    os.symlink(link, link2)
    W0 = link + '/w'                                 # 러너 WORK_ROOT (링크 꼴 · 기본 $HOME/…)
    JD = W0 + '/bed/RJ'
    cases = [
        ('정직 · 판독 루트 링크 꼴', rec_of(JD), JD, True),
        ('정직 · 판독 루트 realpath 꼴', rec_of(JD), real + '/w/bed/RJ', True),
        ('정직 · WORK_ROOT 끝 / (JD 에 //)', rec_of(W0 + '//bed/RJ'), os.path.join(W0 + '/', 'bed', 'RJ'), True),
        ('정직 · WORK_ROOT 에 /./ ', rec_of(link + '/./w/bed/RJ'), JD, True),
        ('정직 · 링크 사슬 (ALIAS → HOME → 실제) · 판독 realpath', rec_of(link2 + '/w/bed/RJ'), real + '/w/bed/RJ', True),
        ('정직 · 판독 루트에 .. ', rec_of(JD), real + '/w/bed/../bed/RJ', True),
        ('바꿈 · 로그만 앞 시도 RJ.t1', rec_of(JD, log=W0 + '/bed/RJ.t1/RT1/rt.bin'), JD, False),
        ('바꿈 · 기록 둘만 앞 시도', rec_of(JD, rt1=W0 + '/bed/RJ.t1/RT1/rt.bin', rt2=W0 + '/bed/RJ.t1/RT1/rt.bin'), JD, False),
        ('바꿈 · 기록 · 로그 셋 앞 시도 (job_dir 그대로)', rec_of(JD, *(3 * [W0 + '/bed/RJ.t1/RT1/rt.bin'])), JD, False),
        ('바꿈 · 넷 다 앞 시도 (job_dir 포함)', rec_of(W0 + '/bed/RJ.t1'), JD, False),
        ('바꿈 · 다른 루트 같은 이름 (realpath 꼴 글자)', rec_of(JD, log=real + '/other/w/bed/RJ/RT1/rt.bin'), JD, False),
        ('바꿈 · 같은 파일 realpath 꼴 글자 (로그만)', rec_of(JD, log=real + '/w/bed/RJ/RT1/rt.bin'), JD, False),
    ]
    for lab, r, rd, want in cases:
        got = rule(r, rd)
        print(f'  {"✓" if got == want else "✗"} {lab}: 기대 {"통과" if want else "거부"} · 규칙 {"통과" if got else "거부"}')
    # RT1 하위 폴더만 다른 시도의 RT1 으로 심볼릭 (글자 · 잡 폴더 그대로) — 경로 규칙은 통과 · 잡는 것은 sha256 결합
    os.rename(os.path.join(real, 'w/bed/RJ/RT1'), os.path.join(real, 'w/bed/RJ/RT1.orig'))
    os.symlink(os.path.join(real, 'w/bed/RJ.t1/RT1'), os.path.join(real, 'w/bed/RJ/RT1'))
    print(f'  참고 · RT1 하위 폴더 = 앞 시도 RT1 의 심볼릭: 경로 규칙 {"통과" if rule(rec_of(JD), JD) else "거부"} '
          f'(→ RT1 끝 sha256 기록 ↔ 파일 실제 sha256 이 가름 · 15-5 sha 조건 · 바꿔치기가 RT1 전이면 RT1 이 그 자리에 쓴 파일 = 같은 왕복)')

print('[F] 치환 줄 첫 낱말 규칙 (A 15-5 · 15-4b 검사 13): 첫 낱말 read_restart · # 시작 제외 · ${ 없음 · 낱말 둘 · 정확히 하나')


def subst_lines(log):
    out = []
    for ln in log:
        w = ln.split()
        if w and w[0] == 'read_restart' and not ln.lstrip().startswith('#') and '${' not in ln and len(w) == 2:
            out.append(w[1])
    return out


logs = [
    ('정직 (머리 주석에 낱말 · 원 줄 · 치환 줄)', ['# RT2 — read_restart rt.bin', 'read_restart ${ckpt}', 'read_restart /h/w/bed/RJ/RT1/rt.bin'], 1),
    ('정직 · 줄 뒤 주석 (치환 줄 끝 공백)', ['read_restart ${ckpt}  # c', 'read_restart /h/w/bed/RJ/RT1/rt.bin  '], 1),
    ('정직 · arm_dt 꼴 주석 + #read_restart', ['# >>> block arm_dt — (read_restart 뒤)', '#read_restart x', 'read_restart ${ckpt}', 'read_restart /p'], 1),
    ('바꿈 · 명령 줄 둘', ['read_restart /a', 'read_restart /b'], 2),
]
for lab, log, want in logs:
    n = len(subst_lines(log))
    print(f'  {"✓" if n == want else "✗"} {lab}: 셈 {n} (기대 {want})')

print('[K] 합성 RJ (_mk_rj 2095 행) 쌍 덤프 줄 수 ↔ 칸 하한')
print(f'  지금 원 · R/g2 쌍 덤프 = 1 줄 (write_local … [crow]) · 7:3 쓴 격자 6×4 의 칸 하한 = 24 × {NMIN} = {24 * NMIN} 안쪽 하중 쌍 (원 · R/g2 · RT 각각) '
      f'→ 1 < {24 * NMIN} = 칸 계산 못 함 = UNCONFIRMED (RESTORED 를 단언하는 R14 · R17 · R18 · R29 · R30 이 뒤집힘)')

print('[L] B §8 · §9 장부 ↔ sacct 손 반례 (글 그대로: 장부 없는 잡 · 잡 없는 장부 줄 · 돌려받지 않은 시도 = 그 NP 결론 없음)')


def reconcile(sacct, ledger):
    no_ledger = sorted(set(sacct) - {l[0] for l in ledger})
    no_job = sorted({l[0] for l in ledger} - set(sacct))
    return ('결론 없음 → 1저자' if (no_ledger or no_job) else '대조 맞음'), no_ledger, no_job


lcases = [
    ('정직 · 건식 사전 멈춤 rc 3 (11-12 job 358667 꼴 · OUT 없음 · 장부 줄 없음) → 고쳐 건식 다시 → 샌드박스',
     ['dry_a', 'dry_b', 'sb'], [('dry_b', 200), ('sb', 40000)], '대조 맞음'),
    ('정직 · 대기 중 취소 (scancel · 돈 적 없음)', ['sb_cancel', 'sb'], [('sb', 40000)], '대조 맞음'),
    ('정직 · 잡 스크립트가 러너 전에 실패 (모듈 · 경로)', ['sb_x', 'sb'], [('sb', 40000)], '대조 맞음'),
    ('바꿈 · 이름 바꾼 잡 (sacct 이름 목록 밖) 에서 N 40000 한 번 더', ['sb'], [('sb', 40000), ('renamed', 40000)], '결론 없음 → 1저자'),
]
for lab, s, l, want in lcases:
    got, nl, nj = reconcile(s, l)
    print(f'  {"✓" if got == want else "✗"} {lab}: 글 그대로 = {got} (장부 없는 잡 {nl} · 잡 없는 장부 줄 {nj}) · 바라는 답 {want}')
