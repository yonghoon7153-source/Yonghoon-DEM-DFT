#!/usr/bin/env python3
"""Heckel fit for the DEM pressure series (pure-SE **and** composite beds).

Reads heckel/manifest.json — a list of points:
  [{"P_MPa": 100, "plate_z": 0.0xxxx, "atom": "...", "contacts": ["...","..."]}, ...]
(plate_z from each mesh_*.stl vertex; contacts optional → cross-checks the geometric lens.)

Computes per pressure:
  D_sphere = ΣV_sphere / V_box        (relative density, material-conserving)
  D_union  = (ΣV_sphere - ΣV_lens)/V_box   (geometric; <1 even when over-compressed)
Fits Heckel:  ln(1/(1-D)) = K·P + A   → P_y = 1/K,  σ_y ≈ P_y/3.

★★ P_y 해석 — 옛 판정문의 정정 (2026-08-11, Codex 적대리뷰 Q4) ★★
옛 문장은 "P_y ≈ 0.85 GPa 면 LPSCl 소성을 충실히 흉내낸 것"이라 적었다.  **틀렸다.**
E 를 18× 연화한 것이 이 DEM 의 설계이므로 P_y 가 단결정 H(850 MPa) 근처로 나오면
오히려 연화가 안 걸린 것이다 (판정 게이트는 이미 고쳤는데 이 docstring 만 남아 있었다).

  P_y 는 Li6PS5Cl 고유 항복압이 **아니라** 연화된 베드의
  **effective compaction parameter** 다.  850/P_y = 연화 배수로만 읽는다.

★ 지렛대 경고 (실측): D_union 이 1 에 가까운 고압점은 ln(1/(1-D)) 가 특이점 근처라
  적합을 지배한다.  real_14 복합 4압력에서 leave-one-out:
      전체 133.1 · −P100 116.1 · −P200 136.4 · −P300 133.1 · −**P600 258.1**
  P600 (D_union 0.9931) 하나가 P_y 를 2배로 흔든다.  ⇒ **다압력 P_y 를 인용할 때는
  leave-one-out 표를 함께** 낼 것.  1σ 구간은 회귀 전파값이지 95 % CI 가 아니다.
"""
import json, math, os, sys
import numpy as np

R_SE = 0.0005
BOX = 0.05


def read_atoms(atom, with_ids=False):
    """atom dump → (xyz[N,3], radius[N]).  Columns: id type x y z radius ...

    `with_ids=True` 면 (xyz, rad, {id: radius}) 를 돌려준다 — contact 덤프의 id 쌍을
    **실제 반지름**으로 되돌리는 데 쓴다 (복합 베드에서 필수, lens_from_contacts 참조).
    """
    xyz, rad, by_id = [], [], {}
    #  ★★★ 2026-08-30 (Codex R14 D-7) — **읽지 못한 것을 0 으로 돌려주지 않는다.**
    #    이 reader 는 LIGGGHTS 헤더 9줄 + `id type x y z radius` 6열을 가정한다.
    #    scaffold CSV(`type,x,y,z,r` 5열)를 넣으면 헤더 9줄이 데이터를 먹고 나머지가
    #    `len(p) < 6` 으로 전부 걸러져 **V_sphere = 0.0** 이 나온다 ⇒ `vol_and_lens` 가
    #    조용히 **ε_sphere = 100 %** 를 만든다 (실측: real14 CSV → (0.0, 0.0, …)).
    #    ⇒ 한 줄도 못 읽으면 **거부**한다.  "빈 침대" 와 "형식이 다른 파일" 은 다르다.
    with open(atom) as f:
        for _ in range(9): next(f)
        for line in f:
            p = line.split()
            if len(p) < 6: continue
            xyz.append((float(p[2]), float(p[3]), float(p[4])))
            rad.append(float(p[5]))
            if with_ids:
                by_id[int(float(p[0]))] = float(p[5])
    if not xyz:
        raise SystemExit(
            f'ABORT — `{atom}` 에서 원자를 한 줄도 못 읽었다.  이 reader 는 LIGGGHTS 덤프\n'
            f'  (헤더 9줄 + `id type x y z radius` 6열)만 읽는다.  scaffold CSV\n'
            f'  (`type,x,y,z,r` 5열)를 주면 헤더 9줄이 데이터를 먹고 나머지가 6열 미만으로\n'
            f'  걸러져 **V_sphere = 0 → ε_sphere = 100 %%** 가 조용히 나온다 (R14 D-7).\n'
            f'  ⇒ CSV 는 전용 adapter 로 읽을 것.  "빈 침대" 와 "형식이 다른 파일" 은 다르다.')
    xyz, rad = np.asarray(xyz, float), np.asarray(rad, float)
    return (xyz, rad, by_id) if with_ids else (xyz, rad)



def read_scaffold_csv(path):
    """scaffold CSV → `(xyz[N,3], rad[N], typ[N])`.  **box units 그대로** 돌려준다.

    ★★★ 2026-08-30 (Codex R14 D-7) — `read_atoms` 는 LIGGGHTS 덤프 전용이라 이 파일을
      **조용히 0 행**으로 읽는다 (헤더 9줄이 데이터를 먹고 나머지가 6열 미만).  그래서
      전용 reader 를 둔다.  형식:

        `# type,x,y,z,r  # LIGGGHTS box units (lateral 0..0.05 = 50um); …`
        `1,0.025033,0.040912,0.007308,0.006000`

    ⚠ **단위 함정** — 값은 **box unit** 이다 (lateral 0..0.05 = 50 µm ⇒ ×1000 = µm).
      두께를 µm 로 그대로 넣으면 부피가 10⁹ 배 틀린다.  그래서 이 함수는 변환하지 않고,
      `eps_sphere_from_scaffolds` 가 **한 곳에서만** 변환한다.
    ⚠ 한 행도 못 읽으면 **거부**한다 (빈 침대와 형식 불일치는 다르다).
    """
    xyz, rad, typ = [], [], []
    with open(path, encoding='utf-8') as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue                                   # 헤더·주석
            p_ = line.split(',')
            if len(p_) != 5:
                raise SystemExit(f'ABORT — {path}:{ln} 열이 {len(p_)} 개다 (5 여야 한다: '
                                 f'type,x,y,z,r).  다른 형식의 파일을 주지 않았는지 볼 것.')
            try:
                t = int(float(p_[0])); x, y, z, r = (float(v) for v in p_[1:])
            except ValueError as e:
                raise SystemExit(f'ABORT — {path}:{ln} 수치가 아니다 ({e})')
            if not (math.isfinite(x) and math.isfinite(y) and math.isfinite(z)
                    and math.isfinite(r)):
                raise SystemExit(f'ABORT — {path}:{ln} 비유한 값이 있다')
            if r <= 0:
                raise SystemExit(f'ABORT — {path}:{ln} 반지름이 {r} 이다 (> 0 이어야 한다)')
            xyz.append((x, y, z)); rad.append(r); typ.append(t)
    if not xyz:
        raise SystemExit(f'ABORT — {path} 에서 구를 한 줄도 못 읽었다.  주석·헤더만 있거나 '
                         f'형식이 다르다.  "빈 침대" 와 "형식 불일치" 는 다르다.')
    return np.asarray(xyz, float), np.asarray(rad, float), np.asarray(typ, int)


def eps_sphere_from_scaffolds(am_csv, se_csv, height_um, box_um=50.0):
    """scaffold CSV 두 개 + 정지 두께 → `ε_sphere` 원장 (dict).

        ε_sphere = 1 − Σ_i (4/3)π r_i³ / (L_x · L_y · H)

    ★ **lens 가 필요 없다** (R14 D-7) — 겹침 차감은 `ε_union` 의 것이고, ε_sphere 는
      **구 부피의 단순 합**이다 (소성 압밀에서 재료 보존 규약: 접촉에서 밀려난 재료가
      bulge 로 다시 나오므로 solid = 원래 구 부피의 합).  CLAUDE.md 의 porosity 규약 참조.
    ★ **벽 밖 clip 도 하지 않는다** — 기존 D_sphere 규약을 재현하는 것이 목적이다.

    ⚠⚠ **행 이름은 `AM+SE seed-sphere void` 다.**  첨가제(VGCF·PTFE·SDCP) 고체부피가
      빠져 있으므로 무한정한 *"electrode porosity"* 로 쓰면 추정량 오류다 (R14 D-7).
    ⚠ `height_um` 은 **µm**, 내부에서 box unit 으로 바꾼다 (파일이 box unit 이므로).
    """
    import hashlib
    out = {'convention': 'eps_sphere = 1 - sum(4/3 pi r^3) / (Lx*Ly*H)',
           'row_name': 'AM+SE seed-sphere void (첨가제 고체부피 제외)',
           'lens_subtracted': False, 'wall_clipped': False,
           'height_um': float(height_um), 'box_um': float(box_um)}
    L = float(box_um) / 1000.0                             # µm → box unit
    H = float(height_um) / 1000.0
    if not (L > 0 and H > 0):
        raise SystemExit(f'ABORT — box_um={box_um} · height_um={height_um} 는 양수여야 한다')
    tot = 0.0
    for tag, path in (('AM', am_csv), ('SE', se_csv)):
        if path is None:
            out[f'V_{tag}'] = 0.0; out[f'n_{tag}'] = 0; continue
        _, rad, _t = read_scaffold_csv(path)
        v = float(((4.0 / 3.0) * math.pi * rad ** 3).sum())
        out[f'V_{tag}'] = v; out[f'n_{tag}'] = int(len(rad))
        out[f'sha_{tag}'] = hashlib.sha256(open(path, 'rb').read()).hexdigest()[:16]
        tot += v
    out['V_box'] = L * L * H
    out['V_sphere'] = tot
    out['eps_sphere_pct'] = 100.0 * (1.0 - tot / out['V_box'])
    return out


def _lens_volume(dist, ra, rb):
    """두 구가 dist 만큼 떨어져 있을 때 겹침(렌즈) 부피.  벡터화."""
    dist = np.asarray(dist, float)
    out = np.zeros_like(dist)
    full = dist <= np.abs(ra - rb)                      # 작은 구가 통째로 들어감
    out[full] = (4.0 / 3.0) * math.pi * np.minimum(ra, rb)[full] ** 3
    m = (~full) & (dist < ra + rb) & (dist > 0)
    d, A, B = dist[m], ra[m], rb[m]
    out[m] = (math.pi * (A + B - d) ** 2
              * (d ** 2 + 2 * d * B - 3 * B ** 2 + 2 * d * A + 6 * A * B - 3 * A ** 2)
              / (12.0 * d))
    return out


def _pairs_within(qa, qb, cutoff, box, same):
    """cutoff 안의 (ia, ib) 쌍 — numpy 전용 셀리스트.  x·y 주기, z 비주기.

    ★ scipy 를 안 쓴다 (클라우드 컨테이너에 없고, 리포 규약도 numpy 전용).
    same=True 면 같은 배열이므로 ib > ia 만 남겨 중복을 지운다.
    """
    na, nb = len(qa), len(qb)
    if na == 0 or nb == 0:
        return np.empty(0, np.int64), np.empty(0, np.int64)
    h = float(cutoff)
    nx = max(1, int(box // h))
    hx = box / nx                                        # x·y 는 주기라 정확히 나눠 쓴다
    z0 = min(qa[:, 2].min(), qb[:, 2].min())

    def cell(q):
        cx = np.mod(np.floor(q[:, 0] / hx).astype(np.int64), nx)
        cy = np.mod(np.floor(q[:, 1] / hx).astype(np.int64), nx)
        cz = np.floor((q[:, 2] - z0) / h).astype(np.int64) + 1     # dz=-1 이 음수가 안 되게
        return cx, cy, cz

    ax, ay, az = cell(qa)
    bx, by, bz = cell(qb)
    nz = int(max(az.max(), bz.max())) + 3

    def key(cx, cy, cz):
        return (cx * nx + cy) * nz + cz

    bkey = key(bx, by, bz)
    order = np.argsort(bkey, kind='stable')
    bkey_s = bkey[order]
    ia_all, ib_all = [], []
    ar = np.arange(na)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                tk = key(np.mod(ax + dx, nx), np.mod(ay + dy, nx), az + dz)
                lo = np.searchsorted(bkey_s, tk, 'left')
                hi = np.searchsorted(bkey_s, tk, 'right')
                cnt = hi - lo
                tot = int(cnt.sum())
                if tot == 0:
                    continue
                ia = np.repeat(ar, cnt)
                base = np.repeat(np.cumsum(cnt) - cnt, cnt)
                ib = order[np.repeat(lo, cnt) + (np.arange(tot) - base)]
                ia_all.append(ia)
                ib_all.append(ib)
    if not ia_all:
        return np.empty(0, np.int64), np.empty(0, np.int64)
    ia = np.concatenate(ia_all)
    ib = np.concatenate(ib_all)
    keep = (ib > ia) if same else np.ones(len(ia), bool)
    return ia[keep], ib[keep]


def lens_from_geometry(xyz, rad, box=BOX):
    """겹침 렌즈 부피를 **atom 덤프 좌표만으로** 계산 (contact 덤프 불요).

    강체구이므로 LIGGGHTS 의 접촉 δ = rᵢ+rⱼ−dist 는 정확히 기하값이다 → 두 경로가
    같은 값을 줘야 하고, 둘 다 있는 압력점에서 그걸 교차검증한다.
    ★ 덱이 `boundary p p f` 이므로 x·y 는 **주기경계**다.  최소상 이미지를 안 쓰면
      경계층 접촉(≈ 2 r/L ≈ 2 %)을 통째로 놓친다.  z 는 비주기.

    ★ **반지름 클래스로 쪼개 푼다** (2026-08-07).  옛 구현은 cutoff 를 2·r_max 하나로
      잡았는데, 복합 베드(AM_P 6 / AM_S 2 / SE 0.5 µm)에서는 r_max=6 이라 SE-SE 후보쌍이
      4천만 개를 넘어 사실상 못 돌았다.  쌍의 진짜 cutoff 는 rᵢ+rⱼ 이므로 클래스별로
      나눠 걸면 **결과는 같고**(selftest 가 브루트포스와 대조) 후보쌍이 수만 개로 줄어든다.
    """
    if len(xyz) < 2:
        return 0.0
    q = np.asarray(xyz, float).copy()
    rad = np.asarray(rad, float)
    q[:, 0] %= box
    q[:, 1] %= box
    classes = np.unique(rad)
    idx = {c: np.flatnonzero(rad == c) for c in classes}
    V = 0.0
    for m, ca in enumerate(classes):
        for cb in classes[m:]:
            same = (ca == cb)
            A, B = idx[ca], idx[cb]
            ia, ib = _pairs_within(q[A], q[B], ca + cb, box, same)
            if len(ia) == 0:
                continue
            d = q[A[ia]] - q[B[ib]]
            d[:, 0] -= box * np.round(d[:, 0] / box)     # 최소상 이미지 (x, y)
            d[:, 1] -= box * np.round(d[:, 1] / box)
            dist = np.sqrt((d ** 2).sum(1))
            sel = dist < ca + cb
            if not sel.any():
                continue
            V += float(_lens_volume(dist[sel],
                                    np.full(int(sel.sum()), ca),
                                    np.full(int(sel.sum()), cb)).sum())
    return float(V)


def lens_from_contacts(contacts, r_se=R_SE, rad_by_id=None):
    """옛 경로 — contact 덤프의 δ 로 렌즈 부피.  덤프가 있을 때만 (기하 경로의 교차검증).

    컬럼 규약 (`compute pair/gran/local pos id force force_normal force_tangential
    torque contactArea delta contactPoint` = 26열):
      [0:6] pos1,pos2 · [6:9] id1,id2,periodic · [9:12] force · [12:15] f_n ·
      [15:18] f_t · [18:21] torque · [21] contactArea · [22] **delta** · [23:26] contactPoint

    ★ rad_by_id (id → 반지름) 를 주면 **다분산에서도 정확**하다.  안 주면 옛 동작
      (모든 접촉이 반지름 r_se 인 등반지름 SE)으로 떨어지는데, 이는 복합 베드
      (AM_P 6 / AM_S 2 / SE 0.5 µm)에서 **틀린 값**을 준다 — AM 이 낀 접촉의 렌즈를
      SE 반지름으로 계산하기 때문.  복합에서는 반드시 rad_by_id 를 넘길 것.
    """
    if isinstance(contacts, (str, bytes, os.PathLike)):
        # ★ 문자열을 넘기면 파이썬이 **글자 단위로** 순회해 '/' 를 파일로 열려 든다.
        #   조용히 0 을 돌려주거나 엉뚱한 예외를 내는 대신 여기서 세운다.
        raise TypeError('lens_from_contacts 는 파일 **리스트** 를 받는다 '
                        f'(문자열 하나를 받았다: {contacts!r}). [path] 로 감쌀 것.')
    V = 0.0
    for cf in (contacts or []):
        with open(cf) as f:
            for line in f:
                if line.startswith('ITEM'): continue
                p = line.split()
                if len(p) < 23: continue
                try: d = float(p[22])
                except ValueError: continue
                if d <= 0: continue
                if rad_by_id is None:
                    ra = rb = r_se
                else:
                    try:
                        ra = rad_by_id[int(float(p[6]))]; rb = rad_by_id[int(float(p[7]))]
                    except (KeyError, ValueError):
                        continue
                if d >= ra + rb: continue
                V += float(_lens_volume(np.array([ra + rb - d]),
                                        np.array([ra]), np.array([rb]))[0])
    return V


def vol_and_lens(atom, contacts, plate_z, geometric=True):
    """→ (V_sphere, V_lens, V_box, V_lens_contacts).

    V_lens 는 기본이 **기하 계산**(항상 가능) — contact 덤프는 교차검증용으로만 읽는다.
    옛 동작(contact 없으면 D_union=nan)이 4압력 중 3점을 못 쓰게 만들었다.
    """
    xyz, rad, by_id = read_atoms(atom, with_ids=True)
    V_sphere = float(((4.0/3.0)*math.pi*rad**3).sum())
    # ★ rad_by_id 를 반드시 넘긴다.  안 넘기면 lens_from_contacts 가 **모든 접촉을
    #   반지름 r_SE 인 등반지름**으로 계산한다 — AM_P 6 / AM_S 2 / SE 0.5 µm 인 복합
    #   베드에서는 틀린 값이고, 그 결과로 교차검증이 거짓 '불일치' 를 찍는다.
    #   (lens_from_contacts docstring 이 요구하던 것을 호출부가 지키지 않고 있었다.)
    V_c = lens_from_contacts(contacts, rad_by_id=by_id) if contacts else 0.0
    V_lens = lens_from_geometry(xyz, rad) if geometric else V_c
    return V_sphere, V_lens, BOX*BOX*plate_z, (V_c if contacts else float('nan'))


def heckel(P, D):
    """Linear fit ln(1/(1-D)) = K*P + A on points with D<1 (nan/D≥1 은 제외)."""
    P = np.asarray(P, float)
    D = np.asarray(D, float)
    m = np.isfinite(D) & (D < 0.999)
    P, D = P[m], D[m]
    if len(P) < 2: return None
    y = np.log(1.0/(1.0 - D))
    K, A = np.polyfit(P, y, 1)
    yhat = K*P + A
    ss = np.sum((y - y.mean())**2)
    r2 = 1 - np.sum((y - yhat)**2)/ss if ss > 0 else float('nan')
    Py = 1.0/K if K > 0 else float('nan')            # MPa
    return dict(K=K, A=A, r2=r2, Py_MPa=Py, sigma_y_MPa=Py/3.0)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    man = json.load(open(args[0] if args else 'heckel/manifest.json'))
    rows = []
    for e in man:
        Vs, Vl, Vb, Vc = vol_and_lens(e['atom'], e.get('contacts'), e['plate_z'])
        eps_s = (1 - Vs/Vb)*100
        D_s = Vs/Vb
        D_u = (Vs - Vl)/Vb if Vl > 0 else float('nan')
        eps_u = (1 - D_u)*100 if Vl > 0 else float('nan')
        rows.append(dict(P=e['P_MPa'], eps_s=eps_s, D_s=D_s, eps_u=eps_u, D_u=D_u,
                         Vl=Vl, Vc=Vc))
        print(f"  P={e['P_MPa']:>4} MPa  ε_sphere={eps_s:+6.2f}%  D_sphere={D_s:.4f}"
              f"   ε_union={eps_u:6.2f}%  D_union={D_u:.4f}")
    # ★ 두 경로가 다 있는 압력점에서 기하 ↔ contact-덤프 교차검증 (강체구면 같아야 한다)
    xs = [r for r in rows if np.isfinite(r['Vc']) and r['Vc'] > 0]
    if xs:
        print('\n렌즈 부피 교차검증 (기하 vs contact 덤프) — 강체구면 일치해야 한다:')
        for r in xs:
            rel = abs(r['Vl'] - r['Vc'])/max(r['Vc'], 1e-30)
            print(f"  P={r['P']:>4} MPa  기하={r['Vl']:.6g}  contact={r['Vc']:.6g}  "
                  f"차이 {rel:.2%}" + ('  ✓' if rel < 0.05 else '  ⚠ 불일치 — 조사 필요'))
    else:
        print('\n  ⚠ contact 덤프가 있는 압력점이 없어 렌즈 교차검증 불가 (기하 경로만)')
    P = [r['P'] for r in rows]
    print("\nHeckel fit on D_union (physical, <1):")
    fu = heckel(P, [r['D_u'] for r in rows])
    if fu:
        print(f"  R²={fu['r2']:.4f}  P_y={fu['Py_MPa']:.0f} MPa ({fu['Py_MPa']/1000:.2f} GPa)"
              f"  σ_y≈{fu['sigma_y_MPa']:.0f} MPa")
        # ★ 판정을 둘로 나눈다.  옛 게이트는 (R²>0.97 and 500<P_y<1200) 하나였는데, 그 P_y
        #   구간은 **연화 안 한** LPSCl(H≈850 MPa)을 기대한 값이다.  우리 DEM 은 E 를 18×
        #   연화한 것이 설계이므로 P_y 가 그 구간에 들어오면 오히려 이상하다 — 게이트가
        #   "설계대로 동작했다" 를 실패로 찍고 있었다 (CLAUDE.md 는 이미 6.5× 연화의
        #   정량으로 해석하고 있어 문서와 코드가 어긋나 있었다).
        lin = fu['r2'] >= 0.95
        soft = 850.0 / fu['Py_MPa'] if fu['Py_MPa'] > 0 else float('nan')
        print(f"  LPSCl 단결정 참조: σ_y≈300 MPa, H≈850 MPa")
        print(f"  ① 직선성 R²={fu['r2']:.4f} → "
              f"{'✓ Heckel 선형 (소성 압밀 거동)' if lin else '⚠ 곡선 — 탄성 한계 노출'}")
        print(f"  ② 연화 배수 = 850/{fu['Py_MPa']:.0f} = {soft:.1f}×  "
              f"(σ_y 축: 300/{fu['sigma_y_MPa']:.0f} = {300.0/fu['sigma_y_MPa']:.1f}×)")
        print(f"     ↳ 이것은 실패가 아니라 **연화의 정량**이다.  E_eff 18× 연화가 설계이고, "
              f"P_y 가\n       500~1200 MPa 였다면 오히려 연화가 안 걸린 것.  "
              f"입도 재배열·GB 슬라이딩·미세파괴를\n       유효 탄성률에 뭉뚱그린 몫이 이 배수로 나타난다.")
        print(f"  VERDICT: {'✓ 선형 Heckel + 정량화된 연화' if lin else '⚠ 비선형 — 조사 필요'}")
        # ★ leave-one-pressure-out — 고밀도점 지렛대를 **자동으로** 드러낸다 (Q4).
        #   ln(1/(1−D)) 는 D→1 에서 발산하므로 한 점이 P_y 를 두 배로 흔들 수 있다.
        if len(rows) >= 3:
            print('\n  leave-one-pressure-out P_y — 한 점이 결론을 만들고 있지 않은지:')
            worst = (0.0, None)
            for k in range(len(rows)):
                sub = [r for j, r in enumerate(rows) if j != k]
                f2 = heckel([r['P'] for r in sub], [r['D_u'] for r in sub])
                if not f2:
                    continue
                d = f2['Py_MPa'] - fu['Py_MPa']
                flag = '  ← ★ 지렛대' if abs(d) > 0.5 * fu['Py_MPa'] else ''
                print(f"    −P{rows[k]['P']:<4} (n={len(sub)})  P_y {f2['Py_MPa']:7.1f}"
                      f"  R² {f2['r2']:.4f}   Δ {d:+7.1f}{flag}")
                if abs(d) > abs(worst[0]):
                    worst = (d, rows[k]['P'])
            if worst[1] is not None and abs(worst[0]) > 0.5 * fu['Py_MPa']:
                print(f"    ⚠ P{worst[1]} 하나가 P_y 를 {abs(worst[0]):.0f} MPa "
                      f"({abs(worst[0]) / fu['Py_MPa']:.0%}) 움직인다 — P_y 를 단일값으로")
                print(f"      인용하지 말고 **범위 병기**할 것 (D_union 이 1 에 가까운 점의 지렛대).")

    print("\nHeckel fit on D_sphere (flags over-compression where D≥1):")
    fs = heckel(P, [r['D_s'] for r in rows])
    if fs:
        print(f"  R²={fs['r2']:.4f}  P_y={fs['Py_MPa']:.0f} MPa")
    over = [r['P'] for r in rows if r['D_s'] >= 1.0]
    if over:
        print(f"  ⚠ D_sphere≥1 (over-compression artifact) at P={over} MPa → use D_union there")


def _selftest():
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)

    #  ★★★ 2026-08-30 (R14 D-7) — scaffold CSV adapter 규약 고정.
    #    ⓐ 해석해 정확 일치 · ⓑ 실물 real14 가 원장 ε_sphere 재현 · ⓒ 음성 4종 fail-closed.
    import tempfile as _tf, os as _os
    _d = _tf.mkdtemp()
    _am = _os.path.join(_d, 'am.csv'); _se = _os.path.join(_d, 'se.csv')
    open(_am, 'w').write('# type,x,y,z,r\n1,0.01,0.01,0.01,0.006\n2,0.02,0.02,0.01,0.002\n')
    open(_se, 'w').write('# type,x,y,z,r\n6,0.03,0.03,0.01,0.0005\n')
    _r = eps_sphere_from_scaffolds(_am, _se, height_um=72.534)
    _V = (4.0 / 3.0) * math.pi * (0.006 ** 3 + 0.002 ** 3 + 0.0005 ** 3)
    chk('scaffold ⓐ 해석해 V_sphere', abs(_r['V_sphere'] - _V) < 1e-18)
    chk('scaffold ⓐ V_box 단위(µm→box)', abs(_r['V_box'] - 0.05 * 0.05 * 0.072534) < 1e-15)
    chk('scaffold ⓐ lens/clip 안 함', _r['lens_subtracted'] is False and _r['wall_clipped'] is False)
    _p = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
                       'docs', 'data')
    _real = _os.path.join(_p, 'real14_am_scaffold.csv')
    if _os.path.exists(_real):
        _rr = eps_sphere_from_scaffolds(_real, _os.path.join(_p, 'real14_se_scaffold.csv'),
                                        height_um=30.28)
        chk('scaffold ⓑ real14 개수 457/32832',
            _rr['n_AM'] == 457 and _rr['n_SE'] == 32832)
        #  ⚠ 이 한 줄이 규약 고정이다 — lens 를 빼거나 단위를 틀리면 여기서 깨진다.
        chk(f"scaffold ⓑ real14 ε_sphere {_rr['eps_sphere_pct']:.3f}% ≈ 원장 15.626%",
            abs(_rr['eps_sphere_pct'] - 15.626) < 0.01)
    _neg = 0
    for _txt in ('# h\n1,0.01,0.01,0.01,0.006,9\n', '# h\n1,nan,0.01,0.01,0.006\n',
                 '# h\n1,0.01,0.01,0.01,0\n', '# h\n# nothing\n'):
        _x = _os.path.join(_d, 'x.csv'); open(_x, 'w').write(_txt)
        try:
            read_scaffold_csv(_x)
        except SystemExit:
            _neg += 1
    chk('scaffold ⓒ 음성 4종 (6열·비유한·r=0·주석만)', _neg == 4)

    R = R_SE
    # 같은 반지름 두 구, 겹침 δ → 렌즈 부피 πδ²(6R−δ)/12 (contact 경로가 쓰는 바로 그 식)
    for delta in (0.2*R, 0.8*R, 1.5*R):
        dist = 2*R - delta
        xyz = np.array([[0.02, 0.02, 0.01], [0.02 + dist, 0.02, 0.01]])
        want = math.pi/12.0*delta**2*(6.0*R - delta)
        got = lens_from_geometry(xyz, np.array([R, R]))
        chk(f'등반지름 렌즈 부피 δ={delta/R:.1f}R', abs(got - want)/want < 1e-6)

    xyz = np.array([[0.02, 0.02, 0.01], [0.02 + 2.5*R, 0.02, 0.01]])
    chk('안 닿으면 0', lens_from_geometry(xyz, np.array([R, R])) == 0.0)

    # ★ 주기경계 (덱이 boundary p p f) — 경계를 가로지르는 접촉을 놓치면 안 된다
    d = 2*R - 0.5*R
    xyz = np.array([[BOX - d/2, 0.02, 0.01], [d/2, 0.02, 0.01]])   # x 경계 넘어 마주봄
    want = math.pi/12.0*(0.5*R)**2*(6.0*R - 0.5*R)
    chk('★ x 주기경계를 가로지르는 겹침을 잡는다',
        abs(lens_from_geometry(xyz, np.array([R, R])) - want)/want < 1e-6)
    xyz = np.array([[0.02, BOX - d/2, 0.01], [0.02, d/2, 0.01]])
    chk('★ y 주기경계도 마찬가지',
        abs(lens_from_geometry(xyz, np.array([R, R])) - want)/want < 1e-6)
    # z 는 비주기 — 바닥과 천장이 이어지면 안 된다
    xyz = np.array([[0.02, 0.02, 0.0], [0.02, 0.02, 0.012]])
    chk('z 는 되말리지 않는다 (바닥↔천장 가짜 접촉 금지)',
        lens_from_geometry(xyz, np.array([R, R])) == 0.0)

    # 완전 포함 (작은 구가 큰 구 안으로) → 작은 구 부피
    xyz = np.array([[0.02, 0.02, 0.01], [0.02 + 0.1*R, 0.02, 0.01]])
    got = lens_from_geometry(xyz, np.array([2*R, 0.5*R]))
    chk('완전 포함이면 작은 구 부피',
        abs(got - (4.0/3.0)*math.pi*(0.5*R)**3)/((4.0/3.0)*math.pi*(0.5*R)**3) < 1e-9)

    # ★ heckel() 이 리스트/nan/D≥1 을 견디는가 (2026-08-05 실제 크래시 회귀)
    f = heckel([100, 200, 300, 400], [0.69, float('nan'), 1.02, 1.18])
    chk('★ 리스트 입력에 죽지 않는다 (D<0.999 를 리스트에 걸던 TypeError)', f is None)
    f = heckel([100, 200, 300], [0.60, 0.70, 1.05])
    chk('D≥1 점은 fit 에서 빠진다', f is not None)
    f = heckel([100, 200, 300], [0.60, float('nan'), 0.80])
    chk('nan 점도 빠진다', f is not None and f['K'] > 0)

    # ★ 문자열 contacts 는 즉시 세운다 (글자 단위 순회 → '/' 를 파일로 열던 실제 사고)
    try:
        lens_from_contacts('/some/path')
        chk('★ 문자열 contacts → TypeError', False)
    except TypeError:
        chk('★ 문자열 contacts → TypeError', True)

    # ★ vol_and_lens 가 rad_by_id 를 실제로 넘기는가 (다분산 교차검증 회귀).
    #   AM(6R)-SE(R) 접촉 하나를 심고, contact 경로가 등반지름(r_SE)이 아니라
    #   실제 반지름 쌍으로 렌즈를 재는지 기하 경로와 대조한다.
    import tempfile as _tf, os as _os
    _d = _tf.mkdtemp(prefix='hk_')
    try:
        ra, rb = 6 * R, R
        dist = ra + rb - 0.4 * R                       # δ = 0.4R 겹침
        atom = _os.path.join(_d, 'atom.liggghts')
        with open(atom, 'w') as f:
            f.write('ITEM: TIMESTEP\n0\nITEM: NUMBER OF ATOMS\n2\n'
                    'ITEM: BOX BOUNDS pp pp ff\n0 0.05\n0 0.05\n-0.01 1\n'
                    'ITEM: ATOMS id type x y z radius\n'
                    f'1 1 0.02 0.02 0.01 {ra}\n'
                    f'2 3 {0.02 + dist} 0.02 0.01 {rb}\n')
        cont = _os.path.join(_d, 'contact.liggghts')
        cols = ['0'] * 26
        cols[0:6] = ['0.02', '0.02', '0.01', str(0.02 + dist), '0.02', '0.01']
        cols[6:9] = ['1', '2', '0']
        cols[22] = str(0.4 * R)                        # delta
        with open(cont, 'w') as f:
            f.write('ITEM: TIMESTEP\n0\nITEM: ENTRIES c\n' + ' '.join(cols) + '\n')
        Vs, Vl, Vb, Vc = vol_and_lens(atom, [cont], 0.02)
        chk('★ vol_and_lens 가 rad_by_id 로 다분산 렌즈를 잰다 (기하=contact)',
            Vl > 0 and abs(Vc - Vl) / Vl < 1e-6)
        # 옛 동작(등반지름 r_SE) 이었다면 크게 다르다 — 버그가 다시 오면 여기서 잡힌다
        wrong = lens_from_contacts([cont])             # rad_by_id 없이 = r_SE 등반지름
        # 이 기하(6R↔R, δ=0.4R)에서 등반지름 렌즈는 참값의 0.61배 = 39 % 오차.
        # 교차검증 허용치(5 %)를 8배 넘는 크기면 감지선으로 충분하다.
        chk('★ 등반지름 폴백은 다분산에서 틀린 값 (버그 재발 감지선)',
            abs(wrong - Vl) / Vl > 0.2)
    finally:
        import shutil as _sh
        _sh.rmtree(_d, ignore_errors=True)

    # 알려진 Heckel 직선을 심어두고 K/P_y 회수
    K0, A0 = 1.0/850.0, 0.5
    Ps = [100, 200, 300, 400]
    Ds = [1 - math.exp(-(K0*p + A0)) for p in Ps]
    f = heckel(Ps, Ds)
    chk('심어둔 Heckel 직선에서 P_y 회수', abs(f['Py_MPa'] - 850) < 1e-6 and f['r2'] > 0.999)

    # ★ 셀리스트(numpy) ↔ O(N²) 브루트포스 — 다분산·주기경계에서 같은 값을 줘야 한다.
    #   scipy cKDTree 를 numpy 셀리스트로 바꾸고 반지름-클래스 블로킹을 넣었으므로
    #   (복합 베드에서 옛 cutoff=2·r_max 는 후보쌍 4천만 개로 사실상 못 돌았다)
    #   "결과 불변" 을 여기서 못 박는다.
    def _brute(xyz, rad, box=BOX):
        q = np.asarray(xyz, float).copy(); q[:, 0] %= box; q[:, 1] %= box
        V = 0.0
        for i in range(len(q)):
            for j in range(i + 1, len(q)):
                d = q[i] - q[j]
                d[0] -= box * round(d[0] / box); d[1] -= box * round(d[1] / box)
                dist = float(np.sqrt((d ** 2).sum()))
                if dist >= rad[i] + rad[j]:
                    continue
                V += float(_lens_volume(np.array([dist]),
                                        np.array([rad[i]]), np.array([rad[j]]))[0])
        return V

    rng = np.random.default_rng(7)
    for nm, radset in (('단분산', [R]), ('이분산', [R, 4 * R]), ('삼분산', [R, 4 * R, 12 * R])):
        n = 250
        xyz = np.column_stack([rng.uniform(0, BOX, n), rng.uniform(0, BOX, n),
                               rng.uniform(0, 0.02, n)])
        rr = rng.choice(radset, n)
        a, b = lens_from_geometry(xyz, rr), _brute(xyz, rr)
        chk(f'★ 셀리스트 == 브루트포스 ({nm}, 주기경계)', abs(a - b) <= 1e-12 * max(b, 1e-30))

    # ★ contact 경로의 다분산 정확성 — rad_by_id 없이는 AM 낀 접촉을 SE 반지름으로 계산한다
    import tempfile, os as _os
    ra, rb, delta = 12 * R, 4 * R, 0.2 * R
    line = (' '.join(['0'] * 6) + ' 1 2 0 ' + ' '.join(['0'] * 12)
            + f' 0 {delta:.17g} 0 0 0\n')
    fh = tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False)
    fh.write('ITEM: ENTRIES x\n' + line); fh.close()
    want = _lens_volume(np.array([ra + rb - delta]), np.array([ra]), np.array([rb]))[0]
    got = lens_from_contacts([fh.name], rad_by_id={1: ra, 2: rb})
    bad = lens_from_contacts([fh.name])                     # 옛 동작 (등반지름 R_SE)
    _os.unlink(fh.name)
    chk('★ contact 경로: rad_by_id 로 다분산 렌즈가 정확', abs(got - want) < 1e-15 * max(want, 1))
    chk('★ rad_by_id 없으면 복합에서 틀린다 (그래서 넘겨야 한다)', abs(bad - want) > 0.5 * want)

    print(f'selftest: {ok}/{ok + len(fail)} PASS' + (f'   FAILED: {fail}' if fail else ''))
    return 0 if not fail else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(_selftest())
    main()
