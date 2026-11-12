#!/usr/bin/env python3
"""P1 G2c' 초안 A 15-5b — PFA-02 (마지막 사전 공격 · 내부 · Codex 아님) 의 고를 길 셋을 **같은 산술** 로 비교한다.

  (a) 전역 W 문턱을 낮춤 (0.05 → 0.04 · 0.03 · 0.025 · 0.02)
  (b) 전역 W 0.05 는 그대로 + 쓴 격자 칸별 '안쪽 쌍' W 의 최댓값 (칸 문턱 0.5 · 칸마다 안쪽 하중 쌍 ≥ n_min)
  (c) 한계로만 적음 (= 지금 판 · (a) 의 0.05 줄)

같은 산술 = 리뷰 `pfa_w_check.py` 와 같은 정의: 덤프 읽기 (작은 id 먼저 · 방향 바뀐 행 = 위치 맞바꿈 · 힘 9 · shear 3 부호 반전) ·
r = |Ft - Ft_원| / |Ft_원| (|Ft_원| > 0 쌍) · reset_like = r > 0.5 · W = Σ_reset |Ft_원| / Σ_공통 |Ft_원| ·
소실 모형 = 시험 쪽 Ft -> 0 (감쇠 몫 무시 [추정]) · 정직 배경 = B (주기 파일 · 한 step 늦은 이력) ↔ A(N).
칸 = 상자 [lo, lo+L) 를 P × Q 로 고르게 나눈 칸 (원 런 = `processors * * 1` · `balance` 없음 전제) · 위치는 상자로 감음 ·
경계에서 1e-12·L 안 = 애매 (칸 안쪽 집합에서 뺌 · 수만 보고).
  L1 (리뷰 모형) = 칸 하나 통째 소실 = 큰 id 원자 자리가 그 칸인 쌍 전부 (분할 · 덤프 사본 쪽 근사)
  L2 (최소 모형) = 그 칸 '안쪽 쌍' (두 원자 다 그 칸 · 애매 아님) 만 — 읽는 쪽 i 선택과 무관하게 반드시 잃는 쌍
읽기만 (받은 11-12 샌드박스 덤프 · 리포 밖) · LIGGGHTS · ibb · 네트워크 없음.
쓰는 법: python3 -I f3_choice.py <run40000 폴더>  (그 아래 A · B · C/post/c_40000.txt)
"""
import math
import sys

D = sys.argv[1]
TAU_A = (0.05, 0.04, 0.03, 0.025, 0.02)
TAU_CELL = 0.5
N_MIN = 100           # 칸마다 안쪽 하중 쌍 (|Ft_원| > 0) 하한 — 밑이면 그 칸 계산 못 함 (UNCONFIRMED · 생산 침대는 칸마다 수천 [추정])
SHARE_73 = 685 / 562605   # 7:3 [연속] 사후 reset_like 몫 (11-02 RESULT 8 행) — 교차 NP 정직 최악 대리 (이 쌍들이 하중 상위라면)
GRIDS = ((6, 4, '7:3 RJ 쓴 NP 24'), (11, 1, '10:0 RJ 쓴 NP 11'), (5, 1, '0:10 · 5:5 RJ 쓴 NP 5'),
         (2, 2, '3:7 RJ 쓴 NP 4'), (3, 2, 'RJ2 쓴 (EXT NP 6) · 읽는 NP 6'))


def load(path):
    rows, box = {}, None
    with open(path) as f:
        lines = f.read().splitlines()
    ib = next(i for i, l in enumerate(lines) if l.startswith('ITEM: BOX BOUNDS'))
    bx = [float(t) for t in lines[ib + 1].split()[:2]]
    by = [float(t) for t in lines[ib + 2].split()[:2]]
    box = (bx[0], bx[1] - bx[0], by[0], by[1] - by[0])
    i = next(i for i, l in enumerate(lines) if l.startswith('ITEM: ENTRIES'))
    for ln in lines[i + 1:]:
        if not ln.strip():
            continue
        v = [float(x) for x in ln.split()]
        a, b = int(v[6]), int(v[7])
        if a > b:
            v = v[3:6] + v[0:3] + [v[7], v[6]] + v[8:9] + [-x for x in v[9:18]] + v[18:21] + [-x for x in v[21:24]] + v[24:]
        key = (min(a, b), max(a, b))
        assert key not in rows, ('dup', key)
        rows[key] = v
    return rows, box


def norm(x):
    return math.sqrt(sum(t * t for t in x))


def per_pair(T, O, lost=frozenset()):
    """공통 쌍마다 (|Ft_원|, reset_like) — 소실 쌍은 시험 Ft = 0."""
    out = {}
    for k in sorted(set(T) & set(O)):
        fo = O[k][15:18]
        ft = [0.0, 0.0, 0.0] if k in lost else T[k][15:18]
        no = norm(fo)
        rs = no > 0 and norm([a - b for a, b in zip(ft, fo)]) > 0.5 * no
        out[k] = (no, rs)
    return out


def wsum(pp, keys=None):
    ks = pp.keys() if keys is None else keys
    den = sum(pp[k][0] for k in ks)
    num = sum(pp[k][0] for k in ks if pp[k][1])
    return (num / den) if den > 0 else None


def cell_of(x, y, box, P, Q):
    lo_x, Lx, lo_y, Ly = box
    u, w = (x - lo_x) % Lx, (y - lo_y) % Ly
    amb = (min(abs(u - Lx * k / P) for k in range(P + 1)) <= 1e-12 * Lx or
           min(abs(w - Ly * k / Q) for k in range(Q + 1)) <= 1e-12 * Ly)
    return (min(int(u / Lx * P), P - 1), min(int(w / Ly * Q), Q - 1)), amb


def cells(O, box, P, Q):
    big, inner, n_amb = {}, {}, 0
    for k, v in O.items():
        c1, a1 = cell_of(v[0], v[1], box, P, Q)
        c2, a2 = cell_of(v[3], v[4], box, P, Q)
        big.setdefault(c2, set()).add(k)          # L1: 큰 id 원자 자리 (방향 맞춘 뒤 v[3:6])
        if a1 or a2:
            n_amb += 1
        elif c1 == c2:
            inner.setdefault(c1, set()).add(k)    # L2 · (b): 두 원자 다 그 칸
    return big, inner, n_amb


def cell_max(pp, inner, P, Q):
    """(b) 칸별 안쪽 W 의 최댓값 · 칸마다 안쪽 하중 쌍 수의 최솟값 · 계산 못 하는 칸 수 (하중 쌍 < N_MIN)."""
    ws, nmin, nbad = [], None, 0
    global NMAX
    NMAX = 0
    for cx in range(P):
        for cy in range(Q):
            ks = [k for k in inner.get((cx, cy), ()) if pp[k][0] > 0]
            nmin = len(ks) if nmin is None else min(nmin, len(ks))
            NMAX = max(NMAX, len(ks))
            if len(ks) < N_MIN:
                nbad += 1
            w = wsum(pp, ks) if ks else None
            if w is not None:
                ws.append(w)
    return (max(ws) if ws else None), nmin, nbad, len(ws)


A, box = load(f'{D}/A/post/c_40000.txt')
B, _ = load(f'{D}/B/post/c_40000.txt')
C, _ = load(f'{D}/C/post/c_40000.txt')
print(f'상자 x [{box[0]}, {box[0] + box[1]}) · y [{box[2]}, {box[2] + box[3]}) · 쌍 A {len(A)} B {len(B)} C {len(C)}')

ppB, ppC = per_pair(B, A), per_pair(C, A)
WB, WC = wsum(ppB), wsum(ppC)
print(f'== 정직 전역 W: B {WB:.6f} · C {WC:.6f} (리뷰 0.003086 · 0.000391 과 같은지)')

fts = sorted((norm(A[k][15:18]) for k in A), reverse=True)
kprox = max(1, round(SHARE_73 * len(fts)))
Wprox = sum(fts[:kprox]) / sum(fts)
print(f'== 교차 NP 정직 최악 대리 [추정]: 7:3 reset 몫 {SHARE_73:.5f} → 이 침대 {kprox} 쌍 · 그 쌍이 |Ft| 상위라면 W = {Wprox:.4f} '
      f'(관측 꼴 = reset 쌍은 하중 작은 쌍 · B 48 중 27 = 하위 10 %)')

print('== (a) 전역 W 문턱 — 정직 여유 · 최악 대리 여유')
for t in TAU_A:
    print(f'  τ {t:<5}: 정직 B ×{t / WB:.1f} · C ×{t / WC:.1f} · 교차 NP 최악 대리 ×{t / Wprox:.2f}')

print('== 쓴 격자마다: (a) 칸 하나 통째 소실 잡힘 수 · (b) 칸별 안쪽 W (정직 최대 · 소실 칸 값 · 잡힘)')
for P, Q, label in GRIDS:
    big, inner, n_amb = cells(A, box, P, Q)
    nc = P * Q
    mB, nminB, nbadB, njB = cell_max(ppB, inner, P, Q)
    nmaxB = NMAX
    mC, _, _, _ = cell_max(ppC, inner, P, Q)
    n_inner = sum(len(v) for v in inner.values())
    print(f'-- {P}x{Q}x1 ({label}) · 칸 {nc} · 안쪽 쌍 {n_inner}/{len(A)} · 애매 {n_amb} · 칸마다 안쪽 하중 쌍 {nminB}–{nmaxB} · '
          f'N_MIN {N_MIN} 밑 칸 {nbadB}/{nc}')
    print(f'   (b) 정직 칸별 안쪽 W 최대: B {mB:.4f} (칸 {njB}) · C {mC:.4f} · 칸 문턱 {TAU_CELL} 여유 B ×{TAU_CELL / mB:.1f}'
          if mB else f'   (b) 정직 칸별 안쪽 W: 계산 칸 없음')
    for model, sets in (('L1', big), ('L2', inner)):
        caught_a = {t: 0 for t in TAU_A}
        caught_b, lost_cell_w, gw = 0, [], []
        for cx in range(P):
            for cy in range(Q):
                lost = frozenset(sets.get((cx, cy), ()))
                pp = per_pair(B, A, lost)
                w = wsum(pp)
                gw.append(w)
                for t in TAU_A:
                    caught_a[t] += w > t
                ks = [k for k in inner.get((cx, cy), ()) if pp[k][0] > 0]
                wc = wsum(pp, ks) if ks else None
                lost_cell_w.append(wc)
                mx, _, _, _ = cell_max(pp, inner, P, Q)
                caught_b += (w > 0.05) or (mx is not None and mx > TAU_CELL)
        lw = [x for x in lost_cell_w if x is not None]
        print(f'   {model}: 전역 W {min(gw):.4f}–{max(gw):.4f} (평균 {sum(gw) / len(gw):.4f}) · (a) 잡힘 ' +
              ' · '.join(f'{t}→{caught_a[t]}/{nc}' for t in TAU_A) +
              f' | (b) 소실 칸 안쪽 W {min(lw):.4f}–{max(lw):.4f} · 잡힘 (전역 0.05 ∨ 칸 {TAU_CELL}) {caught_b}/{nc}')
