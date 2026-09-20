#!/usr/bin/env python3
"""AIMD Li+ jump statistics — clean intra/inter-cage distance picture (Fig-2d style).

Static-structure Li-Li distances are noisy (ordered approximant, all sites filled).
This instead samples the REAL mobile-Li distribution from an AIMD trajectory and
gives the quantities argyrodite papers actually plot:

  1. Van Hove self-correlation  Gs(r, dt)  -> P(a Li moved r in time dt).
       short dt = vibration peak (~0.5 A); longer dt grows secondary peaks at the
       characteristic JUMP distances (doublet / intra-cage / inter-cage).
  2. Cage-resolved hops: free anions (S-not-bonded-to-P + Cl) = ~immobile cage
       centres; a Li changing its nearest centre (persisting >= --hop_persist
       frames) = an INTER-cage hop. -> inter-cage hop RATE + hop-distance hist.
  3. MSD -> D (sanity / quantitative anchor).

numpy-only; reads multi-frame extended-xyz (traj.xyz from aimd_mlip.py). Run on the
server where the trajectories live (one trajectory per call; overlay systems in Origin).

Usage:
  python3 aimd_jump_stats.py --traj aimd/T600/traj.xyz --label comp1_T600 \
      --save_fs 20 --out_dir aimd_jump/comp1_T600 \
      --lags_ps 0.5 2 10 --hop_persist 5
  (save_fs auto-read from sibling aimd_results.json if present)
"""
import argparse, hashlib, json, re, shutil, sys
from pathlib import Path
import pathlib
import numpy as np

PS_BOND = 2.30


def read_traj(path):
    txt = open(path).read().splitlines()
    pos, cells, sym = [], [], None
    i, L = 0, len(txt)
    while i < L:
        if not txt[i].strip():
            i += 1; continue
        n = int(txt[i].split()[0])
        m = re.search(r'Lattice="([^"]+)"', txt[i + 1])
        cell = np.array([float(x) for x in m.group(1).split()]).reshape(3, 3)
        s, p = [], []
        for ln in txt[i + 2:i + 2 + n]:
            t = ln.split()
            s.append(t[0]); p.append([float(t[1]), float(t[2]), float(t[3])])
        if sym is None:
            sym = np.array(s)
        pos.append(p); cells.append(cell)
        i += 2 + n
    return sym, np.array(pos, float), np.array(cells, float)


def mic(pi, pj, cell):
    cinv = np.linalg.inv(cell)
    d = (pi @ cinv)[:, None, :] - (pj @ cinv)[None, :, :]
    d -= np.round(d)
    return np.linalg.norm(d @ cell, axis=2)


def unwrap(pos, cell):
    cinv = np.linalg.inv(cell)
    frac = pos @ cinv
    df = np.diff(frac, axis=0); df -= np.round(df)
    fuw = np.empty_like(frac)
    fuw[0] = frac[0]; fuw[1:] = frac[0] + np.cumsum(df, axis=0)
    return fuw @ cell


def free_anions(sym, pos0, cell):
    idx = {e: np.where(sym == e)[0] for e in set(sym)}
    P, S, Cl = (idx.get(e, np.array([], int)) for e in ("P", "S", "Cl"))
    bonded = set()
    if len(P) and len(S):
        d = mic(pos0[P], pos0[S], cell)
        for i in range(len(P)):
            for j in np.where(d[i] < PS_BOND)[0]:
                bonded.add(int(S[j]))
    freeS = np.array([s for s in S if s not in bonded], int)
    return np.concatenate([freeS, Cl]) if (len(freeS) or len(Cl)) else np.array([], int), \
        np.array(["S"] * len(freeS) + ["Cl"] * len(Cl))


def peak_position(rc, g, smooth_A=None):
    """봉우리 위치를 **bin 폭과 무관하게** 읽는다 → (interp, raw_argmax).

    `smooth_A` 를 주면 먼저 **Å 단위 고정폭** 가우시안으로 매끈하게 만든다. bin 수가
    아니라 Å 로 고정하는 게 핵심 — 그래야 dr 이 달라도 **같은 분해능**에서 비교된다.

    ⛔ 2026-08-28 (리뷰 L · §3-1) — 우리는 160-bin 히스토그램의 argmax 를 지표로 썼다.
      그런데 rmax 가 궤적마다 적응형이라 **bin 폭이 런마다 달랐다**(8→18.6 Å ⇒ 0.05→0.12 Å).
      리뷰 L 지적: modelc 600→800 K 의 차이 0.09 Å 는 **bin 폭과 같은 크기**다.
      ⇒ argmax 는 bin 격자에 양자화돼 있어 그 규모의 차이를 주장할 수 없다.
      꼭짓점 3점 포물선 보간은 격자를 벗어나므로, 같은 값이 여러 dr 에서 유지되면
      그건 binning 이 아니다.

    ⛔⛔ 2026-08-28 실측 — **격자만이 문제가 아니었다.** dr 0.025/0.05/0.10 으로 읽으니
      봉우리가 0.574 Å 움직였다. 이건 bin 폭(0.1 Å)보다 훨씬 크다. 원인은 다른 것:
      긴 lag 의 P_s 는 최대 근처가 **넓고 평평**해서, bin 을 잘게 쪼갤수록 bin 당 표본이
      줄어 argmax 가 **잡음으로 튄다.** ⇒ 잘게 쪼갠다고 더 정확해지지 않는다.
      두 원인(양자화 · 최빈값 잡음)은 dr 에 **반대 방향**으로 반응하므로 갈라서 봐야 한다.

    ⛔ 못 하는 것
      · 봉우리가 **끝 bin** 이면 보간을 못 한다 (raw 를 그대로 돌려준다 — 그때는
        rmax 가 잘못 잡힌 것이고 trunc_frac 이 따로 경고한다).
      · 다봉이면 최댓값 하나만 본다. 두 번째 봉우리는 `second_peak()` 소관이다.
      · smooth_A 는 **분해능의 하한**을 정한다. 그보다 작은 차이는 이 함수로 못 읽는다
        (읽히는 것처럼 보이면 그건 잡음이다).
    """
    g = np.asarray(g, dtype=float)
    if smooth_A:
        bw = float(rc[1] - rc[0])
        s = float(smooth_A) / bw
        if s >= 0.5:                    # 이미 격자가 smooth_A 보다 거칠면 그냥 둔다
            n = max(1, int(np.ceil(4.0 * s)))
            k = np.exp(-0.5 * (np.arange(-n, n + 1) / s) ** 2)
            g = np.convolve(g, k / k.sum(), mode="same")
    i = int(np.argmax(g))
    raw = float(rc[i])
    if i == 0 or i >= len(g) - 1:
        return raw, raw
    y0, y1, y2 = float(g[i - 1]), float(g[i]), float(g[i + 1])
    den = y0 - 2.0 * y1 + y2
    if den >= 0:                       # 진짜 극대가 아니다 (평평/잡음) — 보간 금지
        return raw, raw
    d = 0.5 * (y0 - y2) / den
    d = max(-1.0, min(1.0, d))         # 이웃 bin 밖으로는 안 나간다
    return raw + d * float(rc[1] - rc[0]), raw


def slice_window(pos, cells, dt_ps, t_from_ps, t_to_ps):
    """궤적을 [t_from, t_to] ps 로 자른다 (포함 · 프레임 0 기준 시각).

    왜 필요한가 (2026-09-18): melt-quench 궤적 한 파일에 융체·담금질·유리가 다 들어 있다.
    유리만 보려면 잘라야 하는데, 통째로 넣으면 담금질 중의 큰 이동이 유리의 홉 통계를 **덮는다**.

    ⛔ 못 하는 것
      · 온도를 안 본다 — **시각으로만** 자른다. 그 시각이 정말 유리인지는 부르는 쪽이 안다.
      · 창이 비면 **죽는다**. 빈 창을 조용히 전체로 되돌리지 않는다.
    """
    T = len(pos)
    t = np.arange(T) * dt_ps
    if t_from_ps is None and t_to_ps is None:
        return pos, cells, 0, T
    lo = 0 if t_from_ps is None else int(np.searchsorted(t, t_from_ps - 1e-9, "left"))
    hi = T if t_to_ps is None else int(np.searchsorted(t, t_to_ps + 1e-9, "right"))
    if hi - lo < 2:
        raise SystemExit(f"⛔ 창 [{t_from_ps}, {t_to_ps}] ps 에 프레임이 {hi-lo}개다 "
                         f"(궤적 {T} 프레임 · dt {dt_ps} ps) — 빈 창을 전체로 되돌리지 않는다")
    return pos[lo:hi], cells[lo:hi], lo, hi


def write_xyz(path, sym, pos, cell, comment=""):
    """extxyz 한 프레임. numpy-only 규약을 지킨다 (이 파일은 ase 를 안 쓴다)."""
    lat = " ".join(f"{x:.8f}" for x in np.asarray(cell, float).ravel())
    with open(path, "w") as fh:
        fh.write(f"{len(sym)}\n")
        fh.write(f'Lattice="{lat}" Properties=species:S:1:pos:R:3 pbc="T T T" {comment}\n')
        for a, r in zip(sym, np.asarray(pos, float)):
            fh.write(f"{a} {r[0]:.8f} {r[1]:.8f} {r[2]:.8f}\n")


def hop_endpoints(sym, pos, cells, Li, ev, dt_ps):
    """사건 하나 → (시작 구조, 끝 구조). **움직인 Li 를 최소이미지로 맞춰** 끝을 쓴다.

    왜 최소이미지인가: 끝 프레임을 원본 그대로 쓰면 그 Li 가 셀 경계를 넘었을 때
    **반대 방향으로 긴 경로**가 만들어진다 (NEB 보간이 셀을 가로지른다). 시작 위치를
    기준으로 가장 가까운 이미지로 옮겨 놓으면 보간이 짧은 쪽으로 간다.

    ⛔ 못 하는 것
      · 끝 구조가 **진짜 최소인지 모른다** — 이완은 부르는 쪽이 따로 한다.
      · 움직인 Li 하나만 이미지 보정한다. 다른 원자가 같이 넘어갔으면 그건 안 고친다
        (그런 사건이면 애초에 이 사건 정의가 안 맞는 것이다).
    """
    i0 = int(round(ev["t_start_ps"] / dt_ps))
    i1 = int(round(ev["t_end_ps"] / dt_ps))
    a = int(Li[ev["li_rank"]])
    cell = np.asarray(cells[i0], float)
    p0, p1 = np.array(pos[i0], float), np.array(pos[i1], float)
    inv = np.linalg.inv(cell)
    f = (p1[a] - p0[a]) @ inv
    p1[a] = p0[a] + (f - np.round(f)) @ cell      # 최소이미지로 당긴다
    return a, p0, p1, cell, float(np.linalg.norm(p1[a] - p0[a]))


def hop_census(uw_Li, dt_ps, lag_ps, min_dist):
    """**케이지 없이** 홉을 센다 — unwrap 변위가 문턱을 넘은 Li 의 수.

    왜 케이지를 안 쓰나 (2026-09-18): `free_anions()` 는 **P 에 안 묶인 S + Cl** 을 케이지
    중심으로 삼는데, 이 계는 PS₄ 보존율 1.00 이라 free S 가 **0 개**다. 중심이 Cl 12 개뿐이고
    한 변이 14 Å 이라 '가장 가까운 중심이 바뀌었나' 는 홉이 아니라 **큰 구역 이동**을 센다.
    아지로다이트용 정의를 비정질에 그대로 쓰면 조용히 다른 것을 재게 된다.

    ⭐ **lag 이 무엇을 세는지 바꾼다** (2026-09-18 — 시험이 내 오해를 잡았다):
      · `lag_ps = 0` → nlag = 창 전체 ⇒ 짝이 **하나뿐**이라 per_ion_max 는 사실상
        **양끝 순변위**다. **왕복은 안 보인다** (갔다 돌아오면 0).
      · `lag_ps` 를 짧게 주면 미끄럼창이 되어 **바깥 나들이(excursion)도 잡힌다**.
      ⇒ "홉이 있었나" 를 물으면 **짧은 lag**, "자리를 옮겼나" 를 물으면 **창 전체**다.
      둘은 다른 질문이고, 부르는 쪽이 어느 쪽인지 알고 골라야 한다.

    ⛔ 못 하는 것
      · 어느 lag 에서도 **이벤트 수의 하한**이다 — 한 이온이 여러 번 뛰어도 1 로 센다.
      · 홉인지 유동인지 안 가른다. 유리에 유동이 거의 없다는 **가정** 위에 있다.
      · 문턱을 정당화하지 않는다 — 부르는 쪽이 선언한다. (문턱이 판정을 지배한다)
    """
    nlag = max(1, int(round(lag_ps / dt_ps))) if lag_ps else len(uw_Li) - 1
    if nlag >= len(uw_Li):
        raise SystemExit(f"⛔ lag {lag_ps} ps 가 창보다 길다 ({len(uw_Li)} 프레임 × {dt_ps} ps)")
    d = np.linalg.norm(uw_Li[nlag:] - uw_Li[:-nlag], axis=-1)
    per_ion_max = d.max(axis=0)
    moved = per_ion_max >= min_dist
    #: ⭐ 2026-09-18 — **어느 이온이 언제** 였는지를 같이 낸다. NEB 후보 경로를 이 표에서
    #   기계적으로 뽑기 위해서다 (사람이 고르면 사후 선택이다).
    #   각 이온의 **최대 변위를 낸 창** (t_start, t_end) 을 그 이온의 대표 사건으로 삼는다.
    #   ⛔ 이온당 **하나만** 낸다 — 여러 번 뛰어도 제일 큰 것 하나다(하한인 이유).
    ev = []
    for j in np.where(moved)[0]:
        i0 = int(np.argmax(d[:, j]))
        ev.append({"li_rank": int(j), "t_start_ps": float(i0 * dt_ps),
                   "t_end_ps": float((i0 + nlag) * dt_ps), "disp_A": float(d[i0, j])})
    ev.sort(key=lambda e: -e["disp_A"])
    return {"lag_ps": float(nlag * dt_ps), "min_dist_A": float(min_dist), "events": ev,
            "n_Li": int(d.shape[1]), "n_moved": int(moved.sum()),
            "frac_moved": float(moved.mean()),
            "per_ion_max_A": {"max": float(per_ion_max.max()),
                              "median": float(np.median(per_ion_max)),
                              "p90": float(np.percentile(per_ion_max, 90))},
            "⛔_하한이다": "한 이온이 여러 번 뛰어도 **1 로 센다**. 그리고 lag = 창 전체면 "
                          "**왕복은 아예 안 보인다** (양끝 순변위와 같아진다)."}


def _sha256_file(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _pair_key(d, tag):
    """사건의 동일성 키 = **원시 끝점 쌍의 sha256**. 파일이 없으면 **중단**한다."""
    fi, ff = Path(d) / f"{tag}_i.xyz", Path(d) / f"{tag}_f.xyz"
    for f in (fi, ff):
        if not f.exists():
            raise SystemExit(f"⛔ {f} 가 없다 — **없음이 아니라 미회수**다. 합치지 않는다")
    return (_sha256_file(fi), _sha256_file(ff))


def merge_events_dirs(dirs, out_dir, known=None, log=print):
    """여러 lag 의 `events/` 를 **사전등록 규칙대로** 합친다 → 합집합 events 디렉터리.

    왜 (2026-09-20 · 재개조건 ① 카드 §2-①b). `hop_census` 는 한 번에 lag 하나만 돈다.
    lag 을 1·2·3·4 ps 로 돌리면 **같은 사건이 여러 번** 들어오는데, 합치는 규칙이 없으면
    사람이 고르게 된다 — 그게 사후 선택이다.

    규칙 (결과 보기 전에 박혔다)
      ① 사건의 동일성은 **원시 끝점 쌍의 sha256**(`_i.xyz`, `_f.xyz`)으로 본다.
         ev04/ev07 중복(2026-09-19 라운드1 무효 원인)을 잡았던 바로 그 기준이다.
      ② 같은 쌍이 여러 lag 에 있으면 **가장 짧은 lag** 을 남긴다. 동률이면 `disp_A` 큰 것.
         — 결정적이고 결과와 무관하다.
      ③ `known`(이미 판정된 모집단, 예: lag 5 ps 라운드2)과 겹치는 쌍은 `inherited_known`
         으로 **기록만** 하고 산출에서 뺀다 (다시 안 돌린다). 단 그중 `disp_A` 최대
         **한 건**만 `control` 로 남긴다 — 앞 라운드 판정을 재현하는지 보기 위해서다.
      ④ **n_new** = 산출 중 `new` 인 것의 수. `control` 은 안 센다.

    ⛔ 이 함수가 하지 않는 것
      · 사건을 **고르지 않는다**. 문턱이 이미 골랐고 여기서는 합칠 뿐이다.
      · 끝점이 0 K 극소인지 판정하지 않는다 — 그건 G-B7 이고 다음 단계다.
      · 서로 다른 문턱(`min_dist_A`)을 섞지 않는다. 다르면 시작하지 않는다.
      · 같은 lag 을 두 번 받지 않는다 (같은 dir 을 실수로 두 번 준 경우).
      · `truncated=true` 목록을 합치지 않는다 (사람이 N 을 고른 목록이다).
      · 창(`t_from/t_to`)이 같은지는 **검사하지 못한다** — events.json 에 안 들어 있다.
        부르는 쪽이 같은 창으로 돈 dir 만 준다.
    """
    dirs = [Path(x) for x in dirs]
    #: dir 하나면 합칠 게 없다 — 단 `known` 이 있으면 겹침 제거가 남으므로 허용한다.
    #  (실측 동기 2026-09-20: 짧은 lag 넷 중 **한 lag 에서만** 사건이 나오는 경우가 있다.
    #   그때 막아 버리면 정당한 경로가 도구 때문에 닫힌다.)
    if len(dirs) < 1:
        raise SystemExit("⛔ --merge_events 에 events 디렉터리가 없다")
    if len(dirs) < 2 and known is None:
        raise SystemExit("⛔ --merge_events 가 디렉터리 하나인데 --merge_known 도 없다 — "
                         "합칠 것도 뺄 것도 없다. 그 디렉터리를 그대로 쓴다")
    metas = []
    for d in dirs:
        ej = d / "events.json"
        if not ej.exists():
            raise SystemExit(f"⛔ {ej} 가 없다 — census 를 먼저 돌린다")
        m = json.loads(ej.read_text(encoding="utf-8"))
        if m.get("truncated"):
            raise SystemExit(f"⛔ {ej} 는 truncated=true 다 — 사람이 N 을 고른 목록이라 "
                             "합치지 않는다 (--hop_events_all 로 다시 돌린다)")
        metas.append((d, m))
    mins = {round(float(m["min_dist_A"]), 6) for _, m in metas}
    if len(mins) != 1:
        raise SystemExit(f"⛔ 문턱이 섞였다 (min_dist_A = {sorted(mins)}) — 같은 눈금만 합친다")
    lags = [round(float(m["lag_ps"]), 6) for _, m in metas]
    if len(set(lags)) != len(lags):
        raise SystemExit(f"⛔ 같은 lag 이 두 번 들어왔다 ({sorted(lags)}) — "
                         "같은 디렉터리를 두 번 주지 않았는지 본다")

    known_keys = {}
    if known is not None:
        kd = Path(known)
        kj = kd / "events.json"
        if not kj.exists():
            raise SystemExit(f"⛔ {kj} 가 없다 (--merge_known)")
        km = json.loads(kj.read_text(encoding="utf-8"))
        if round(float(km["min_dist_A"]), 6) not in mins:
            raise SystemExit("⛔ --merge_known 의 문턱이 다르다 "
                             f"({km['min_dist_A']} vs {sorted(mins)[0]}) — "
                             "같은 눈금이어야 겹침 판정이 성립한다")
        for e in km["events"]:
            known_keys[_pair_key(kd, e["tag"])] = e["tag"]

    rows = []
    for d, m in metas:
        L = round(float(m["lag_ps"]), 6)
        for e in m["events"]:
            rows.append({"lag_ps": L, "src_dir": str(d), "src_tag": e["tag"],
                         "ev": e, "key": _pair_key(d, e["tag"])})
    #: 규칙 ② — 짧은 lag 먼저, 동률이면 변위 큰 것 먼저. 앞선 것이 이긴다.
    rows.sort(key=lambda r: (r["lag_ps"], -float(r["ev"]["disp_A"])))
    seen, merged, dropped = {}, [], []
    for r in rows:
        if r["key"] in seen:
            dropped.append({"lag_ps": r["lag_ps"], "src": f'{r["src_dir"]}::{r["src_tag"]}',
                            "duplicate_of": seen[r["key"]]})
            continue
        seen[r["key"]] = f'{r["src_dir"]}::{r["src_tag"]}'
        merged.append(r)

    inh = [r for r in merged if r["key"] in known_keys]
    ctrl = max(inh, key=lambda r: float(r["ev"]["disp_A"])) if inh else None
    keep, inherited = [], []
    for r in merged:
        if r["key"] in known_keys:
            r["merge_status"] = "control" if r is ctrl else "inherited_known"
            r["known_tag"] = known_keys[r["key"]]
        else:
            r["merge_status"] = "new"
        (keep if r["merge_status"] != "inherited_known" else inherited).append(r)

    outd = Path(out_dir)
    evd = outd / "events"
    evd.mkdir(parents=True, exist_ok=True)
    man = []
    for k, r in enumerate(keep, 1):
        a = int(r["ev"]["atom_index"])
        tag = f"ev{k:02d}_atom{a}"
        for suf in ("i", "f"):
            shutil.copyfile(Path(r["src_dir"]) / f'{r["src_tag"]}_{suf}.xyz',
                            evd / f"{tag}_{suf}.xyz")
        man.append({**r["ev"], "tag": tag, "merge_status": r["merge_status"],
                    "source": {"dir": r["src_dir"], "tag": r["src_tag"],
                               "lag_ps": r["lag_ps"]},
                    **({"known_tag": r["known_tag"]} if "known_tag" in r else {})})
    n_new = sum(1 for r in keep if r["merge_status"] == "new")
    meta = {"rule": ("합집합 — sha256 쌍 중복제거 · **가장 짧은 lag 우선**(동률이면 disp_A) · "
                     "known 과 겹치면 inherited_known(제외), 그중 최대 하나만 control"),
            "truncated": False,
            "lag_ps": None, "lag_ps_set": sorted(lags),
            "⛔_lag_ps_는_하나가_아니다": "합집합이라 단일 lag 이 없다. `lag_ps_set` 을 본다.",
            "min_dist_A": sorted(mins)[0],
            "n_total_events": len(rows), "taken": len(man),
            "n_new": n_new, "n_control": sum(1 for r in keep
                                             if r["merge_status"] == "control"),
            "n_inherited_known": len(inherited),
            "n_duplicates_dropped": len(dropped),
            "merge_sources": [{"dir": str(d), "lag_ps": round(float(m["lag_ps"]), 6),
                               "n": len(m["events"])} for d, m in metas],
            "known_dir": str(known) if known else None,
            "inherited": [{"src": f'{r["src_dir"]}::{r["src_tag"]}',
                           "known_tag": r["known_tag"],
                           "disp_A": r["ev"]["disp_A"]} for r in inherited],
            "duplicates_dropped": dropped,
            "⛔_끝이_최소인지는_모른다": "이완은 다음 단계다 (G-B7).",
            "events": man}
    (evd / "events.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1),
                                     encoding="utf-8")
    log(f"[합집합] 입력 {len(rows)} 사건 (lag {sorted(lags)}) → 중복제거 {len(dropped)} 건 "
        f"→ 남은 {len(merged)} 건")
    if known is not None:
        log(f"  known({known}) 과 겹침 {len(inh)} 건 → inherited {len(inherited)} · "
            f"control {'1' if ctrl else '0'} 건")
    log(f"  ★ **n_new = {n_new}** (control 은 안 센다) · 산출 {len(man)} 쌍 → {evd}/")
    return meta


def _merge_cli(argv):
    """`--merge_events` 전용 파서. 본 파서의 required(--traj/--label/--out_dir)를
    느슨하게 만들지 않으려고 따로 둔다 — 정상 경로의 가드를 건드리지 않는다."""
    ap = argparse.ArgumentParser(prog="aimd_jump_stats.py --merge_events")
    ap.add_argument("--merge_events", nargs="+", required=True, metavar="EVENTS_DIR",
                    help="합칠 events 디렉터리들 (각 lag 의 census 산출). 궤적은 안 읽는다")
    ap.add_argument("--merge_out", required=True,
                    help="합집합 산출 루트 — <여기>/events/ 가 만들어진다")
    ap.add_argument("--merge_known", metavar="EVENTS_DIR", default=None,
                    help="이미 판정된 모집단(예: lag 5 ps 라운드2). 겹치는 쌍은 "
                         "inherited_known 으로 빠지고 그중 disp_A 최대 한 건만 control")
    a = ap.parse_args(argv)
    merge_events_dirs(a.merge_events, a.merge_out, known=a.merge_known)
    return 0


def van_hove(uw, dt_ps, lags_ps, rmax=None, nbins=160, dr=None):
    """자기 van Hove의 **radial displacement density** P_s(r,t) = 4πr²·G_s(r,t).

    ⛔ 2026-08-28 (리뷰 L · P0-4) — 열 이름을 `Gs_*` 로 썼는데 이건 G_s 가 아니다.
      |Δr| 의 히스토그램이라 **r² 야코비안이 이미 들어간** radial density 다. `Ps_*` 로 고쳤다.

    uw = **unwrap 된** (T, N, 3).

    읽는 법: 짧은 dt 는 진동 봉우리 하나(~0.5 Å)뿐이다. dt 를 늘렸을 때
      **자리 간격(~3 Å)에 두 번째 봉우리가 자라면 진짜 홉**, 첫 봉우리만 넓어지면
      cage 안에서 흔들리는 것이다.

    ★ 왜 MSD 와 다른가: 이건 **창을 안 고른다.** MSD 기울기는 어느 구간을 잡느냐에
      달렸지만(β·D_inc 논쟁 전부), 여기서는 분포 모양이 직접 답한다.

    ⛔⛔ 2026-08-28 실측 수정 — **판정 기준이 틀렸었다.**
      첫 판은 *"자리 간격에 두 번째 봉우리가 자라는가"* 로 봤다. 그건 합성 궤적(모든
      원자가 정확히 한 번, 정확히 3 Å 점프)에서는 보이지만 **진짜 확산에서는 안 보인다** —
      긴 lag 에서 분포는 이산 봉우리가 아니라 **넓은 분포로 퍼지고 봉우리가 밖으로 이동**한다.
      실측 대조(합성):
          cage      1st peak 0.68 → 0.62 → 0.68 → 0.73 Å  (안 움직인다)
          diffusive 1st peak 0.68 → 0.93 → 1.58 → 3.03 Å  (밖으로 이동한다)
      ⇒ **주 지표는 봉우리 위치의 이동**이다. 두 번째 봉우리는 부차 정보로만 남긴다.
      내 selftest 가 이걸 못 잡은 이유: 합성 fixture 가 *한 번씩 딱 3 Å 점프* 라
      실제 확산이 아니라 **이산 홉만** 시험하고 있었다. 진짜 데이터가 잡아줬다.

    ⛔⛔ rmax 를 8 Å 로 고정했던 것도 틀렸다 — 빠른 계는 50 ps 에 RMS 가 그걸 넘어
      **분포가 잘린 채** 봉우리가 범위 밖으로 나간다. rmax=None 이면 자동으로 잡고,
      잘린 비율을 같이 보고한다.

    ⛔ 못 하는 것
      · 절대 D 를 안 준다 — "확산 중인가" 만 본다.
      · 반드시 **unwrap 된 좌표**를 넣어야 한다. wrap 된 걸 넣으면 경계를 넘은 원자가
        셀 크기만 한 변위로 잡혀 없는 봉우리가 생긴다.
      · 시간원점을 전부 쓰므로 이웃 원점끼리 상관돼 있다 — 오차막대의 근거가 아니다.

    `dr` 를 주면 **bin 폭을 고정**한다 (rmax 는 dr 의 배수로 올림). 런마다 rmax 가
    달라도 bin 폭은 같아지므로 **런끼리 봉우리를 비교할 수 있다**. 안 주면 예전처럼
    nbins 를 고정하고 폭은 rmax/nbins 로 따라간다 — 그건 런간 비교에 못 쓴다.

    불변식 `∫r²P_s(r)dr = ⟨Δr²⟩` (= 다원점 MSD(t)) 를 매 lag 마다 같이 낸다.
    히스토그램이 잘리거나 격자가 거칠면 이 비가 1 에서 벗어난다 — **분포를 읽기 전에
    분포가 성립하는지** 보는 자리다.
    """
    T = len(uw)
    use = [l for l in lags_ps if max(1, int(round(l / dt_ps))) < T]
    skipped = [l for l in lags_ps if l not in use]
    if rmax is None and use:
        lag = max(1, int(round(max(use) / dt_ps)))
        dmax = float(np.linalg.norm(uw[lag:] - uw[:-lag], axis=2).max())
        rmax = max(8.0, 1.15 * dmax)      # 잘리면 봉우리가 범위 밖으로 나간다
    rmax = rmax or 8.0
    if dr:                                # bin 폭 고정 모드 (런간 비교용)
        nbins = max(4, int(np.ceil(rmax / dr)))
        rmax = nbins * dr                 # 폭이 정확히 dr 이 되도록 rmax 를 올린다
    edges = np.linspace(0, rmax, nbins + 1)
    rc = 0.5 * (edges[:-1] + edges[1:])
    w = float(edges[1] - edges[0])
    cols, hdr, trunc = [], [], []
    pk_i, pk_r, msd_d, msd_h, ratio = [], [], [], [], []
    for lag_ps in use:
        lag = max(1, int(round(lag_ps / dt_ps)))
        d = np.linalg.norm(uw[lag:] - uw[:-lag], axis=2).ravel()
        h, _ = np.histogram(d, bins=edges, density=True)
        cols.append(h); hdr.append(f"Ps_dt{lag_ps:g}ps")
        trunc.append(float((d > rmax).mean()))
        pi, pr = peak_position(rc, h)
        pk_i.append(round(pi, 3)); pk_r.append(round(pr, 3))
        md = float((d ** 2).mean())                 # 다원점 MSD(lag) — 원자료
        mh = float((rc ** 2 * h).sum() * w)         # ∫r²P_s dr — 히스토그램에서
        msd_d.append(round(md, 4)); msd_h.append(round(mh, 4))
        ratio.append(round(mh / md, 5) if md > 0 else None)
    return rc, cols, hdr, skipped, {
        "rmax_A": round(rmax, 2), "trunc_frac": trunc,
        "dr_A": round(w, 4), "nbins": int(nbins),
        "peak_A": pk_i, "peak_raw_A": pk_r,
        "msd_direct_A2": msd_d, "msd_hist_A2": msd_h, "msd_ratio": ratio,
    }


#: 불변식 허용 폭. 이 밖이면 히스토그램 자체를 못 믿는다 (잘림·격자).
MSD_INVARIANT_TOL = 0.02
#: 리뷰 L4 가 지정한 bin 폭 사다리
DR_LADDER = (0.025, 0.05, 0.10)


def dr_sweep(uw, dt_ps, lag_ps, drs=DR_LADDER, rmax=None, smooth_A=None):
    """같은 궤적·같은 lag 을 여러 **bin 폭**으로 읽어 봉우리가 움직이는지 본다.

    ★ 판정이 **둘**이다. 하나로 합치면 원인을 못 가른다(2026-08-28 실측에서 배웠다):

      `grid`  — Å 고정폭으로 매끈하게 만든 뒤의 산포. 모든 dr 이 **같은 분해능**을 보므로
                남는 차이는 순수하게 격자 탓이다. tol = smooth_A/2.
      `mode_noise` — 매끈하게 안 만든 argmax-보간의 산포. 여기가 크면 최빈값 자체가
                **표본 잡음으로 튄다**는 뜻이고, 그건 dr 을 줄여도 안 낫는다.

    돌려주는 값의 `peak_A` 는 **매끈하게 만든 쪽**이다 — 인용은 이걸로 한다.

    ⛔ 못 하는 것
      · 시드·시간원점 상관에서 오는 오차는 안 본다. `grid` 가 stable 이어도 시드 산포는 별개다.
      · `smooth_A` 보다 작은 차이는 **원리적으로 못 읽는다.** 이 도구로 0.09 Å 를
        주장하려면 smooth_A 가 그보다 작아야 하고, 그러면 mode_noise 가 커진다 —
        그 맞바꿈 자체가 답이다.
      · 다봉이면 최댓값만 따라간다. dr 이 바뀌며 다른 봉우리로 넘어가도 이유는 CSV 를 봐야 안다.
    """
    if rmax is None:                       # ★ 사다리 전체가 **같은 rmax** 를 써야
        lag = max(1, int(round(lag_ps / dt_ps)))   #   폭만의 효과가 분리된다
        dmax = float(np.linalg.norm(uw[lag:] - uw[:-lag], axis=2).max())
        rmax = max(8.0, 1.15 * dmax)
    if smooth_A is None:                   # 가장 거친 격자에 분해능을 맞춘다
        smooth_A = float(max(drs))
    rows = []
    for d_ in drs:
        rc_, cols_, _h, _sk, inf = van_hove(uw, dt_ps, [lag_ps], rmax=rmax, dr=d_)
        if not inf["peak_A"]:
            continue
        ps, _pr = peak_position(rc_, cols_[0], smooth_A=smooth_A)
        rows.append({"dr_A": d_, "peak_A": round(ps, 3),
                     "peak_nosmooth_A": inf["peak_A"][0],
                     "peak_argmax_A": inf["peak_raw_A"][0],
                     "msd_ratio": inf["msd_ratio"][0],
                     "trunc_frac": round(inf["trunc_frac"][0], 4)})
    if len(rows) < 2:
        return rows, {"verdict": "unknown", "spread_A": None, "tol_A": None,
                      "mode_noise": "unknown", "smooth_A": smooth_A}
    pk = [r["peak_A"] for r in rows]
    nsm = [r["peak_nosmooth_A"] for r in rows]
    spread = float(max(pk) - min(pk))
    spread_n = float(max(nsm) - min(nsm))
    tol = 0.5 * float(smooth_A)
    return rows, {
        "verdict": "stable" if spread <= tol else "unstable",
        "spread_A": round(spread, 3), "tol_A": round(tol, 3),
        "smooth_A": round(float(smooth_A), 4),
        "peak_mean_A": round(float(np.mean(pk)), 3),
        # ★ 매끈하게 안 한 최빈값이 얼마나 튀는가 — 이게 곧 **인용 가능한 최소 차이**다
        "mode_noise": "high" if spread_n > tol else "low",
        "mode_noise_spread_A": round(spread_n, 3),
        "resolvable_delta_A": round(max(spread, spread_n, tol), 3),
    }


def second_peak(rc, g, rmin=2.0):
    """`rmin` 밖에서 가장 큰 국소 봉우리 → (r, 높이). 없으면 (None, 0).

    "홉이 보이는가" 를 사람 눈 대신 숫자로 읽는다. 국소 최대만 센다 —
    단조 꼬리는 봉우리가 아니다.
    """
    m = rc > rmin
    if m.sum() < 3:
        return None, 0.0
    idx = np.where(m)[0]
    best, br = 0.0, None
    for i in idx[1:-1]:
        if g[i] >= g[i - 1] and g[i] >= g[i + 1] and g[i] > best:
            best, br = float(g[i]), float(rc[i])
    return br, best


def _selftest():
    import os
    import shutil
    """합성 궤적으로 판별력을 확인한다 — **음성 경로가 핵심**이다.

    양성(홉)만 보면 "무엇을 넣어도 봉우리가 보인다" 는 도구여도 통과한다.
    """
    ok = True

    def chk(c, m):
        nonlocal ok
        ok = ok and bool(c)
        print(f"  {'✓' if c else '✗'} {m}")

    rng = np.random.default_rng(0)
    T, N, dt = 2000, 60, 0.1                      # 200 ps · 100 fs 저장
    site = rng.normal(0, 20, (N, 3))

    def rattle(amp=0.35):
        return site[None, :, :] + rng.normal(0, amp, (T, N, 3))

    # ① cage 안 흔들림만 — 긴 lag 에서도 두 번째 봉우리가 **생기면 안 된다**
    uw = rattle()
    rc, cols, hdr, _sk, _i = van_hove(uw, dt, [0.5, 20.0, 100.0])
    r2, h2 = second_peak(rc, cols[-1])
    chk(h2 < 0.02, f"[vanHove·음성] 흔들림만이면 3 Å 대 봉우리가 없다 (h={h2:.4f})")
    r1 = rc[int(np.argmax(cols[0]))]
    chk(0.2 < r1 < 1.2, f"[vanHove] 짧은 lag 은 진동 봉우리 하나 (r={r1:.2f} Å)")

    # ★★ 2026-08-28 실측 수정 — 첫 판 fixture 는 *한 번씩 딱 3 Å 점프* 라
    #   **이산 홉만** 시험했다. 진짜 확산은 그런 봉우리를 안 만든다(분포가 퍼진다).
    #   그래서 실제 궤적에서 modelc T1000(확실히 확산하는 계)이 "cage 지배" 로 찍혔다.
    #   ⇒ **브라운 운동을 fixture 에 넣고, 판정은 봉우리 이동으로** 바꾼다.
    def peaks(uw_, lags=(0.5, 2.0, 10.0, 50.0)):
        rc_, cs, _h, _sk, info = van_hove(uw_, dt, list(lags))
        return [float(rc_[int(np.argmax(g))]) for g in cs], info

    pk_cage, _i = peaks(uw)
    chk(max(pk_cage) - min(pk_cage) < 0.3,
        f"[vanHove·음성] cage 는 봉우리가 **제자리**다 ({pk_cage[0]:.2f}→{pk_cage[-1]:.2f} Å)")

    step = rng.normal(0, 0.10, (T, N, 3))
    walk = site[None] + np.cumsum(step, axis=0) + rng.normal(0, 0.3, (T, N, 3))
    pk_diff, info_d = peaks(walk)
    chk(pk_diff[-1] - pk_diff[0] >= 0.5,
        f"[vanHove·양성·실측회귀] **확산은 봉우리가 밖으로 이동**한다 "
        f"({pk_diff[0]:.2f}→{pk_diff[-1]:.2f} Å) — 옛 판정(두 번째 봉우리)은 이걸 놓쳤다")
    chk(all(a <= b + 1e-9 for a, b in zip(pk_diff, pk_diff[1:])),
        "[vanHove] 확산이면 봉우리가 lag 과 함께 **단조로** 밀려난다")

    # ③ rmax 자동: 빠른 계가 잘리지 않아야 한다 (8 Å 고정이 실제로 잘랐다)
    fast = site[None] + np.cumsum(rng.normal(0, 0.5, (T, N, 3)), axis=0)
    _rc, _c, _h, _sk, inf = van_hove(fast, dt, [50.0])
    chk(inf["rmax_A"] > 8.0 and inf["trunc_frac"][0] < 0.02,
        f"[vanHove·실측회귀] 빠른 계는 rmax 를 키운다 ({inf['rmax_A']} Å · "
        f"잘림 {100*inf['trunc_frac'][0]:.2f} %)")
    _rc, _c, _h, _sk, inf8 = van_hove(fast, dt, [50.0], rmax=8.0)
    chk(inf8["trunc_frac"][0] > 0.02,
        f"[vanHove·음성] rmax 8 Å 로 고정하면 실제로 잘린다 "
        f"({100*inf8['trunc_frac'][0]:.1f} %) — 그래서 잘림 비율을 보고한다")

    # ④ 가드: 궤적보다 긴 lag 은 조용히 버리지 않고 **보고**한다
    _rc, _c, _h, sk, _i = van_hove(uw, dt, [1.0, 9999.0])
    chk(sk == [9999.0], f"[vanHove·가드] 궤적보다 긴 lag 을 보고한다 ({sk})")

    # ⑤ 가드: wrap 된 좌표는 unwrap 이 없으면 가짜 변위를 만든다
    L = 12.0
    cell = np.eye(3) * L
    drift = np.zeros((T, N, 3))
    drift[:, :, 0] = np.linspace(0, 3 * L, T)[:, None]
    wrapped = (site[None] + drift) % L
    uwr = unwrap(wrapped, cell)
    step_max = np.abs(np.diff(uwr, axis=0)).max()
    chk(step_max < L / 2, f"[vanHove·가드] unwrap 뒤 한 스텝이 셀 절반 미만 ({step_max:.2f})")
    pk_w, _i = peaks(wrapped, lags=(0.5, 50.0))
    chk(abs(pk_w[-1] - pk_w[0]) > 0.5,
        "[vanHove·음성] wrap 된 좌표를 그대로 넣으면 **가짜 이동**이 보인다 — unwrap 이 필수다")

    # ★★★ 배선 회귀 (2026-08-28) — 오늘 van Hove 버그 셋 중 **둘이 배선**이었다.
    #   함수 기본값을 None 으로 고쳐놓고 CLI 기본값 8.0 을 안 고쳐서, 실제 실행에서는
    #   적응형 rmax 가 한 번도 안 먹었다(33/33 궤적이 전부 잘림). selftest 는 함수를
    #   직접 불러서 **CLI 를 안 탔고** 그래서 통과했다.
    #   ⇒ 이제 파서 자체를 시험한다. 함수만 보는 테스트는 배선 버그를 못 잡는다.
    _ap = _build_parser()
    _d = {a.dest: a.default for a in _ap._actions}
    chk(_d.get("rmax") is None,
        f"[배선·실측회귀] `--rmax` **CLI 기본값이 None** 이어야 적응형이 산다 ({_d.get('rmax')})")
    chk(_d.get("save_fs") is None,
        "[배선] `--save_fs` 는 기본값을 두지 않는다 (추측하면 시간축이 통째로 틀린다)")
    _ns = _ap.parse_args(["--traj", "x", "--label", "y", "--out_dir", "z"])
    chk(_ns.rmax is None and _ns.lags_ps,
        "[배선] 기본 인자로 파싱했을 때도 rmax 가 None 이다")

    # ★★★ bin 폭 민감도 (2026-08-28, 리뷰 L4) — 고원이 격자 인공물인지 가른다 ★★★
    #   리뷰 L: modelc 600→800 K 의 0.09 Å 는 **bin 폭(0.05–0.12 Å)과 같은 크기**다.
    #   ⇒ argmax 는 격자에 양자화돼 있어 그 규모를 주장 못 한다. 보간 봉우리는 되나?
    _rmax_w = max(8.0, 1.15 * float(np.linalg.norm(
        walk[500:] - walk[:-500], axis=2).max()))
    _rows, _v = dr_sweep(walk, dt, 50.0, DR_LADDER, rmax=_rmax_w)
    chk(len(_rows) == 3 and _v["verdict"] == "stable",
        f"[dr사다리·양성] Å 고정폭으로 맞추면 dr {list(DR_LADDER)} 가 같은 봉우리를 준다 "
        f"(산포 {_v['spread_A']} Å ≤ {_v['tol_A']} Å)")
    chk(_v["spread_A"] <= _v["mode_noise_spread_A"] + 1e-9,
        f"[dr사다리] 평활이 격자 산포를 **줄인다** "
        f"({_v['spread_A']} ≤ 무평활 {_v['mode_noise_spread_A']} Å)")
    # ★★ 음성 ①: 넓고 평평한 최대에서는 **최빈값이 잡음으로 튄다** — 도구가 그걸 말해야 한다.
    #   (이건 격자 문제가 아니라 별개 원인이다. 하나로 합쳐 판정하면 이 구분이 사라진다)
    chk(_v["mode_noise"] == "high" and _v["mode_noise_spread_A"] > _v["tol_A"],
        f"[dr사다리·음성·실측] 브라운 궤적의 무평활 최빈값은 튄다 → high "
        f"({_v['mode_noise_spread_A']} Å) — dr 을 줄여도 안 낫는다")
    # ★★ 음성 ②: 격자를 일부러 거칠게 하면 **unstable 이라고 말해야** 한다.
    #   (양성만 있으면 "무엇을 넣어도 stable" 인 판정기여도 통과한다)
    _rows_c, _vc = dr_sweep(walk, dt, 50.0, (0.05, 1.2, 2.5), rmax=_rmax_w, smooth_A=0.10)
    chk(_vc["verdict"] == "unstable",
        f"[dr사다리·음성] 거친 격자(1.2·2.5 Å)를 섞으면 **unstable 이라고 말한다** "
        f"(산포 {_vc['spread_A']} Å > {_vc['tol_A']} Å)")
    # ★★ 음성 ③: **또렷한 봉우리**는 셋 다 통과해야 한다 — 위 음성들이 항상-불합격이 아님을 본다
    _sharp = site[None] + rng.normal(0, 0.03, (T, N, 3))
    _sharp[T // 2:, :, 0] += 3.0                    # 좁은 봉우리 하나가 3 Å 로 이동
    _rs, _vs = dr_sweep(_sharp, dt, 50.0, DR_LADDER, rmax=8.0)
    chk(_vs["verdict"] == "stable" and _vs["mode_noise"] == "low",
        f"[dr사다리·양성·대조] 또렷한 봉우리는 격자·잡음 **둘 다 통과**한다 "
        f"(격자 {_vs['spread_A']} · 잡음 {_vs['mode_noise_spread_A']} Å)")

    # ★★★ 불변식 ∫r²P_s dr = ⟨Δr²⟩ (리뷰 L4) — 분포를 읽기 전에 분포를 검사한다 ★★★
    _rc2, _c2, _h2, _sk2, inv_ok = van_hove(walk, dt, [10.0, 50.0], dr=0.05)
    chk(all(abs(x - 1.0) <= MSD_INVARIANT_TOL for x in inv_ok["msd_ratio"]),
        f"[불변식·양성] 안 잘린 히스토그램은 MSD 를 되돌려준다 "
        f"({inv_ok['msd_ratio']})")
    # 음성: **알려진 실제 실패**(#9 rmax 8 Å 고정 → 33/33 잘림)를 불변식이 독립으로 잡나
    _rc3, _c3, _h3, _sk3, inv_bad = van_hove(fast, dt, [50.0], rmax=8.0, dr=0.05)
    chk(inv_bad["msd_ratio"][0] < 1.0 - MSD_INVARIANT_TOL,
        f"[불변식·음성·실측회귀] 잘린 히스토그램은 MSD 를 **못 되돌려준다** "
        f"(비 {inv_bad['msd_ratio'][0]}) — trunc_frac 과 독립으로 잡힌다")
    # 봉우리가 끝 bin 이면 보간을 안 한다 (경계에서 조용히 틀린 값을 만들지 않는다)
    _g_edge = np.array([5.0, 4.0, 3.0, 2.0])
    chk(peak_position(np.array([0.5, 1.5, 2.5, 3.5]), _g_edge) == (0.5, 0.5),
        "[봉우리·가드] 끝 bin 이 최대면 보간하지 않고 argmax 를 그대로 준다")
    _pi, _pr = peak_position(np.array([0.0, 1.0, 2.0]), np.array([0.0, 1.0, 1.0]))
    chk(abs(_pi - 1.5) < 1e-9 and _pr == 1.0,
        f"[봉우리] 두 bin 이 같으면 그 사이로 간다 ({_pi:.2f} Å, argmax {_pr})")
    chk(_d.get("dr") is None and _d.get("dr_sweep") is None,
        "[배선] `--dr`·`--dr_sweep` 기본값이 None (평소 실행을 안 바꾼다)")
    _ns2 = _ap.parse_args(["--traj", "x", "--label", "y", "--out_dir", "z", "--dr_sweep"])
    chk(_ns2.dr_sweep == [], "[배선] `--dr_sweep` 를 값 없이 주면 기본 사다리를 쓴다")

    # ★★★ E2E (2026-08-28, 리뷰 L P0-1) — **실제 CLI 를 태운다.**
    #   `edges` NameError 는 홉이 잡힐 때만 나는데, 함수 단위 테스트는 main() 을 안 타서
    #   못 잡았다. 러너도 traceback 을 숨기고 성공으로 세어 33건이 "완료" 로 보고됐다.
    #   ⇒ 홉이 **실제로 잡히는** 합성 궤적을 만들어 CLI 를 돌리고 종료코드와 산출물을 본다.
    import subprocess
    import tempfile
    td = tempfile.mkdtemp(prefix="ajs_e2e_")
    # ⚠ **홉이 실제로 잡혀야 한다.** 첫 fixture 는 cage 중심이 하나뿐이라 홉이 0 이었고,
    #   그러면 `edges` 를 쓰는 줄이 아예 안 돌아 **회귀 테스트가 판별력이 없었다**
    #   (제거해도 통과했다 — 오늘 세 번째 '합성이 실제보다 쉽다').
    #   ⇒ cage 중심(자유 음이온) **둘**을 두고 Li 하나를 그 사이로 확실히 넘긴다.
    NF = 400
    cell = [[18., 0, 0], [0, 18., 0], [0, 0, 18.]]
    rows0 = [("P", [9., 9., 0.]),                       # PS4 (S 는 결합 → 자유 아님)
             ("S", [10.9, 9., 0.]), ("S", [7.1, 9., 0.]),
             ("S", [9., 10.9, 0.]), ("S", [9., 7.1, 0.]),
             ("Cl", [0., 0., 0.]), ("Cl", [6., 0., 0.]),  # ← cage 중심 2개
             ("Li", [0.6, 0., 0.]),                       # 이 Li 가 Cl1 → Cl2 로 넘어간다
             ("Li", [0., 3.0, 0.]), ("Li", [6., 3.0, 0.])]
    HOP_I = 7
    with open(os.path.join(td, "traj.xyz"), "w") as f:
        for t_ in range(NF):
            f.write(f"{len(rows0)}\nLattice=\"" +
                    " ".join(f"{v:.6f}" for r in cell for v in r) + "\"\n")
            for i, (sym, q) in enumerate(rows0):
                x = list(q)
                if i == HOP_I and t_ > NF // 2:
                    x[0] = 5.4            # 0.6 → 5.4 Å : 4.8 Å 이동 (문턱 2.5 초과)
                f.write(f"{sym} {x[0]:.6f} {x[1]:.6f} {x[2]:.6f}\n")
    json.dump({"save_fs": 100.0}, open(os.path.join(td, "aimd_results.json"), "w"))
    r = subprocess.run([sys.executable, os.path.abspath(__file__),
                        "--traj", os.path.join(td, "traj.xyz"), "--label", "e2e",
                        "--out_dir", os.path.join(td, "out"), "--lags_ps", "0.5", "5", "20",
                        # ★ 새 경로도 **CLI 로** 태운다 — 오늘 배선 버그가 셋이었다(사각 A)
                        "--dr_sweep"],
                       capture_output=True, text=True, timeout=180)
    chk(r.returncode == 0,
        f"[E2E·실측회귀] **실제 CLI 가 종료코드 0 으로 끝난다** "
        f"(rc={r.returncode}) — `edges` NameError 가 여기서 났다"
        + ("\n      " + (r.stderr or "").strip().splitlines()[-1] if r.returncode else ""))
    chk("NameError" not in (r.stderr or ""), "[E2E·실측회귀] traceback 이 없다")
    chk(os.path.isfile(os.path.join(td, "out", "e2e_vanhove.csv")),
        "[E2E] vanhove.csv 가 생긴다")
    hdr0 = open(os.path.join(td, "out", "e2e_vanhove.csv")).readline()
    chk("Ps_dt" in hdr0 and "Gs_dt" not in hdr0,
        f"[E2E·리뷰L] 열 이름이 **P_s**(=4πr²G_s) 다 — G_s 가 아니다 ({hdr0.split(',')[1].strip()})")
    chk(os.path.isfile(os.path.join(td, "out", "e2e_dr_sweep.csv")),
        "[E2E·배선] `--dr_sweep` 가 실제 CLI 에서 CSV 를 만든다")
    _jj = os.path.join(td, "out", "e2e_jumpstats.json")
    if os.path.isfile(_jj):
        _dd = json.load(open(_jj))
        chk(_dd.get("msd_invariant_ok") is True,
            f"[E2E·불변식] 실제 실행이 불변식을 통과하고 그걸 **기록**한다 "
            f"({_dd.get('msd_invariant_ok')})")
        chk((_dd.get("dr_sweep_verdict") or {}).get("verdict") in ("stable", "unstable"),
            "[E2E·배선] dr 사다리 판정이 summary 에 남는다")
    js = os.path.join(td, "out", "e2e_summary.json")
    if os.path.isfile(js):
        d_ = json.load(open(js))
        chk("D_cm2_s" not in d_ and "D_single_origin_diagnostic_cm2_s" in d_,
            "[E2E·리뷰L] 비정본 D 를 일반 이름으로 저장하지 않는다")
    shutil.rmtree(td, ignore_errors=True)

    # ── 창 슬라이스 · 케이지 없는 홉 집계 (2026-09-18) ────────────────────
    _pos = np.zeros((11, 2, 3)); _cells = [np.eye(3) * 10.0] * 11
    w, _, lo, hi = slice_window(_pos, _cells, 1.0, 3.0, 7.0)
    chk((lo, hi, len(w)) == (3, 8, 5), f"[창] 3–7 ps 를 5 프레임으로 자른다 (얻음 {lo},{hi},{len(w)})")
    w2, _, lo2, hi2 = slice_window(_pos, _cells, 1.0, None, None)
    chk((lo2, hi2) == (0, 11), "[창] 인자가 없으면 전체를 그대로 준다")
    try:
        slice_window(_pos, _cells, 1.0, 9.5, 9.9); _hit = False
    except SystemExit:
        _hit = True
    chk(_hit, "⛔음성: 창에 프레임이 2개 미만이면 **죽는다** (전체로 조용히 되돌리지 않는다)")

    #: 합성 — 값이 **정확히 예측되게** 만든다 (앞서 sin/cos 로 두고 암산하다 틀렸다)
    T, dtp = 51, 1.0
    uw = np.zeros((T, 3, 3))
    uw[:, 0, 0] = np.linspace(0, 5.0, T)                       # 이동체: 순변위 5.0 · 한 스텝 0.1
    uw[:, 1, 0] = 0.2 * (-1.0) ** np.arange(T)                 # 진동: 순변위 0 · 한 스텝 0.4
    #  ion 2 는 완전 정지
    full = hop_census(uw, dtp, 0, 2.0)
    chk(full["n_moved"] == 1 and full["n_Li"] == 3,
        f"[양성] lag=창전체 · 문턱 2 Å → **1/3 Li** (얻음 {full['n_moved']}/{full['n_Li']})")
    chk(abs(full["per_ion_max_A"]["max"] - 5.0) < 1e-6,
        f"이온별 최대변위가 실제 순변위다 ({full['per_ion_max_A']['max']:.3f})")
    # ⭐ lag 이 **누가 잡히는지** 를 바꾼다 — 짧은 lag 에서는 진동체가 잡히고 이동체가 안 잡힌다
    short = hop_census(uw, dtp, 1.0, 0.3)
    chk(short["n_moved"] == 1 and abs(short["per_ion_max_A"]["max"] - 0.4) < 1e-6,
        f"[양성] lag=1 프레임 · 문턱 0.3 Å → 진동체만 (최대 스텝 {short['per_ion_max_A']['max']:.3f})")
    # ⛔음성 — 문턱을 낮추면 진동까지 홉이 된다. 문턱은 **선언**이지 발견이 아니다.
    chk(hop_census(uw, dtp, 1.0, 0.05)["n_moved"] == 2,
        "⛔음성: 문턱 0.05 Å 면 이동체·진동체 **둘 다** 홉으로 센다")
    # ⛔음성 — 아무도 안 움직이면 0 (0 을 '못 쟀다' 로 뭉개지 않는다)
    still = np.zeros((T, 3, 3))
    chk(hop_census(still, dtp, 0, 2.0)["n_moved"] == 0,
        "⛔음성: 정지 궤적이면 **0** 이다 (없는 홉을 만들지 않는다)")
    try:
        hop_census(uw, dtp, 999.0, 2.0); _h2 = False
    except SystemExit:
        _h2 = True
    chk(_h2, "⛔음성: lag 이 창보다 길면 **죽는다**")
    # ⭐⛔음성 — **왕복**: lag=창전체면 안 보이고, 짧은 lag 면 보인다. 이게 lag 의 뜻이다.
    back = np.zeros((T, 1, 3))
    back[:, 0, 0] = np.concatenate([np.linspace(0, 4, T // 2 + 1), np.linspace(4, 0, T - T // 2)[1:]])
    chk(hop_census(back, dtp, 0, 2.0)["n_moved"] == 0,
        "⛔음성: 왕복은 **lag=창전체에서 안 보인다** — 그건 순변위이지 홉이 아니다")
    chk(hop_census(back, dtp, 10.0, 1.0)["n_moved"] == 1,
        "[양성] 같은 왕복이 **lag 10 프레임에서는 잡힌다** — lag 이 질문을 바꾼다")

    # ── 사건 목록 (2026-09-18) — NEB 후보를 **기계적으로** 뽑는 근거 ──────────
    ev_full = hop_census(uw, dtp, 0, 2.0)["events"]
    chk(len(ev_full) == 1 and ev_full[0]["li_rank"] == 0,
        f"[양성] 사건 목록에 **이동체만** 들어간다 (얻음 {[e['li_rank'] for e in ev_full]})")
    chk(ev_full[0]["t_start_ps"] == 0.0 and ev_full[0]["t_end_ps"] == 50.0,
        f"사건의 창이 최대 변위를 낸 구간이다 ({ev_full[0]['t_start_ps']}–{ev_full[0]['t_end_ps']} ps)")
    #: 왕복 궤적 — lag 10 에서 **오르막 구간**이 사건으로 잡혀야 한다 (내리막이 아니라)
    ev_b = hop_census(back, dtp, 10.0, 1.0)["events"]
    chk(len(ev_b) == 1 and ev_b[0]["t_end_ps"] <= 26.0,
        f"[양성] 왕복에서 **오르막 창**이 잡힌다 (t_end {ev_b[0]['t_end_ps']} ≤ 26)")
    # ⛔음성 — 문턱 밑 이온은 목록에 없다 (n_moved 와 목록 길이가 **같아야** 한다)
    _hc = hop_census(uw, dtp, 1.0, 0.05)
    chk(_hc["n_moved"] == len(_hc["events"]) == 2,
        f"⛔음성: 목록 길이 = n_moved (얻음 {len(_hc['events'])} vs {_hc['n_moved']})")
    chk([e["disp_A"] for e in _hc["events"]] == sorted((e["disp_A"] for e in _hc["events"]), reverse=True),
        "사건이 변위 **내림차순**이다 (상위 N 을 자를 수 있게)")
    chk(hop_census(still, dtp, 0, 2.0)["events"] == [],
        "⛔음성: 홉이 없으면 목록도 **빈다** (없는 사건을 만들지 않는다)")
    # ⭐⛔음성 — **늦게** 뛰는 이온. 앞 fixture 는 첫 창이 곧 최대 창이라
    #   `argmax` 를 `0` 으로 바꿔도 시험이 안 잡혔다 (2026-09-18 깨보기 실측).
    #   30 프레임 가만히 있다가 뛰는 이온을 넣어야 창 선택이 검사된다.
    late = np.zeros((T, 1, 3))
    late[30:41, 0, 0] = np.linspace(0, 3.0, 11)
    late[41:, 0, 0] = 3.0
    lc = hop_census(late, dtp, 5.0, 1.0)
    chk(len(lc["events"]) == 1 and lc["events"][0]["t_start_ps"] > 0,
        f"⛔음성: 늦게 뛰면 **늦은 창**이 사건이다 (t_start {lc['events'][0]['t_start_ps']} > 0)")
    chk(abs(lc["events"][0]["disp_A"] - lc["per_ion_max_A"]["max"]) < 1e-9,
        f"사건의 변위 = 그 이온의 **최대** 변위 ({lc['events'][0]['disp_A']:.3f} "
        f"vs {lc['per_ion_max_A']['max']:.3f}) — 첫 창을 쓰면 어긋난다")


    # ── CLI 경로 (--hop_events_all / --hop_events_top) ────────────────────
    #   ⛔ 위 시험들은 전부 **함수를 직접** 부른다. 이 파일은 그래서 한 번 물렸다
    #     (rmax 를 함수에서만 고치고 배선을 안 고쳤는데 selftest 가 통과했다).
    #     --hop_events_all 은 **배선이 전부**라 CLI 를 타야 한다.
    import subprocess
    import sys as _sys
    import tempfile
    td = tempfile.mkdtemp()
    # 이온 3개가 서로 다른 크기로 뛰는 합성 궤적 (문턱 1.0 Å 을 셋 다 넘는다)
    nT, nA, dtp2 = 60, 4, 1.0
    L = 20.0
    P = np.zeros((nT, nA, 3))
    #: ⚠ 점프를 **lag 안에** 끝내야 한다. 처음엔 10 ps 램프로 썼는데 lag 5 ps 는
    #   절반(1.5/1.2/0.9 Å)만 보고 셋 중 둘만 넘겼다 — 내 산수가 틀렸던 자리다.
    for a, amp in enumerate([3.0, 2.4, 1.8, 0.2]):          # 마지막은 진동 = 문턱 아래
        P[:, a, 0] = a * 4.0
        P[20:23, a, 0] += np.linspace(0, amp, 3)            # 2 ps 안에 끝난다
        P[23:, a, 0] += amp
    syms = ["Li"] * nA
    with open(f"{td}/t.xyz", "w") as fh:
        for t in range(nT):
            fh.write(f"{nA}\n")
            fh.write(f'Lattice="{L} 0 0 0 {L} 0 0 0 {L}" Properties=species:S:1:pos:R:3 '
                     f'pbc="T T T" time={t * dtp2}\n')
            for a in range(nA):
                fh.write(f"{syms[a]} {P[t, a, 0]:.6f} {P[t, a, 1]:.6f} {P[t, a, 2]:.6f}\n")

    def cli(*extra):
        return subprocess.run(
            [_sys.executable, __file__, "--traj", f"{td}/t.xyz", "--label", "x",
             "--out_dir", f"{td}/o_{abs(hash(extra)) % 99999}",
             "--save_fs", "1000",          # dt 1.0 ps — aimd_results.json 이 없는 합성 궤적
             "--hop_census_lag_ps", "5.0", "--hop_min_dist", "1.0", *extra],
            capture_output=True, text=True, timeout=180)

    r_all = cli("--hop_events_all")
    chk("전부" in r_all.stdout,
        f"[CLI·양성] --hop_events_all 이 '전부' 를 찍는다 (rc={r_all.returncode})")
    # ⛔음성 — 이 fixture 는 Li 만 있다(자유 음이온 0). 예전엔 여기서
    #   `argmin of an empty sequence` 로 **처리 안 된 채 죽었다** — 사람은 "도구가 깨졌다"
    #   로 읽지만 사실은 "이 계엔 케이지가 없다" 는 결과다.
    chk("케이지 중심) 이 **0 개**" in r_all.stdout or "케이지 중심)이 **0 개**" in r_all.stdout
        or "0 개** — 케이지 기반" in r_all.stdout,
        "⛔음성: 케이지 중심 0 개면 **건너뛴다고 말한다** (죽지 않는다)")
    chk("argmin" not in (r_all.stdout + r_all.stderr),
        "⛔음성: 처리 안 된 numpy 오류가 사람에게 보이지 않는다")
    n_ev = r_all.stdout.count("ev0") + r_all.stdout.count("ev1")
    chk(n_ev == 3, f"[CLI] 문턱(1.0 Å)을 넘긴 3 개를 다 뽑는다 (뽑힌 수 {n_ev}) — "
                   f"진동 이온 1 개는 안 뽑힌다")
    # ⛔음성 — 상위 N 으로 **자르면 화면이 말해야** 한다
    r_top = cli("--hop_events_top", "2")
    chk("**2 개만**" in r_top.stdout and "위반" in r_top.stdout,
        f"⛔음성: 상위 N 으로 자르면 **화면에** 경고한다 — 조용히 자르지 않는다")
    # ⛔음성 — 둘을 같이 주면 시작하지 않는다
    r_both = cli("--hop_events_all", "--hop_events_top", "2")
    chk(r_both.returncode != 0 and "같이 줬다" in (r_both.stdout + r_both.stderr),
        f"⛔음성: --hop_events_all 과 --hop_events_top 을 같이 주면 **거부**한다 "
        f"(rc={r_both.returncode})")
    # ⛔음성 — 기록에 규칙과 잘림 여부가 남는다
    import glob as _glob
    ejs = _glob.glob(f"{td}/o_*/events/events.json")
    if ejs:
        import json as _json
        ej = _json.loads(pathlib.Path(sorted(ejs)[0]).read_text(encoding="utf-8"))
        chk("truncated" in ej and "rule" in ej,
            "⛔음성: events.json 에 rule 과 truncated 가 남는다")
    else:
        chk(False, "⛔음성: events.json 이 안 만들어졌다")
    shutil.rmtree(td, ignore_errors=True)

    # ══ 합집합 (--merge_events) — 2026-09-20 재개조건 ① 카드 §2-①b ════════
    import tempfile
    _tmp = Path(tempfile.mkdtemp(prefix="mergeev_"))

    def _mkdir_ev(name, lag, evs, min_dist=2.0, truncated=False, write_xyz_for=None):
        """events 디렉터리 하나를 손으로 만든다. evs = [(tag, atom, disp, payload)]"""
        d = _tmp / name
        d.mkdir(parents=True, exist_ok=True)
        man = []
        for tag, atom, disp, payload in evs:
            man.append({"li_rank": atom, "t_start_ps": 0.0, "t_end_ps": lag,
                        "disp_A": disp, "atom_index": atom, "tag": tag})
            if write_xyz_for is None or tag in write_xyz_for:
                (d / f"{tag}_i.xyz").write_text(f"1\nX\nLi 0 0 0  # {payload}i\n")
                (d / f"{tag}_f.xyz").write_text(f"1\nX\nLi 0 0 {disp}  # {payload}f\n")
        (d / "events.json").write_text(json.dumps(
            {"rule": "t", "truncated": truncated, "lag_ps": lag,
             "min_dist_A": min_dist, "n_total_events": len(man),
             "taken": len(man), "events": man}, ensure_ascii=False), encoding="utf-8")
        return d

    def _dies(fn, frag):
        try:
            fn()
        except SystemExit as e:
            return frag in str(e)
        except Exception:
            return False
        return False

    #: lag1 과 lag2 가 사건 'A' 를 공유한다 (payload 가 같으므로 sha256 이 같다)
    _d1 = _mkdir_ev("lag1", 1.0, [("ev01_atom10", 10, 3.0, "A"),
                                  ("ev02_atom11", 11, 2.4, "B")])
    _d2 = _mkdir_ev("lag2", 2.0, [("ev01_atom10", 10, 3.0, "A"),
                                  ("ev02_atom12", 12, 2.2, "C")])
    _m = merge_events_dirs([_d1, _d2], _tmp / "u1", log=lambda *a, **k: None)
    chk(_m["taken"] == 3 and _m["n_duplicates_dropped"] == 1,
        f"[양성] 합집합 4 → 중복 1 제거 → 3 (얻은 taken={_m['taken']}, "
        f"dropped={_m['n_duplicates_dropped']})")
    _srcA = [e for e in _m["events"] if e["source"]["tag"] == "ev01_atom10"][0]
    chk(_srcA["source"]["lag_ps"] == 1.0,
        f"[양성] 중복은 **짧은 lag** 이 이긴다 (남은 것 lag={_srcA['source']['lag_ps']})")
    chk(_m["n_new"] == 3 and _m["n_control"] == 0 and _m["n_inherited_known"] == 0,
        "[양성] known 을 안 주면 전부 new")
    chk(all((_tmp / "u1" / "events" / f"{e['tag']}_{s_}.xyz").exists()
            for e in _m["events"] for s_ in ("i", "f")),
        "[배선] 끝점 xyz 가 산출 디렉터리에 복사된다 (다음 단계가 바로 읽는다)")
    chk(all("atom_index" in e and "tag" in e for e in _m["events"]),
        "[배선] events.json 이 couple_endpoints_from_events 가 읽는 꼴이다")

    #: known = lag5 가 'A' 와 'B' 를 이미 갖고 있다 → inherited 1 · control 1(disp 큰 A)
    _dk = _mkdir_ev("lag5", 5.0, [("ev01_atom10", 10, 3.0, "A"),
                                  ("ev02_atom11", 11, 2.4, "B")])
    _m2 = merge_events_dirs([_d1, _d2], _tmp / "u2", known=_dk,
                            log=lambda *a, **k: None)
    chk(_m2["n_new"] == 1 and _m2["n_control"] == 1 and _m2["n_inherited_known"] == 1,
        f"[양성] known 겹침 2 → new 1 · control 1 · inherited 1 "
        f"(얻은 {_m2['n_new']}/{_m2['n_control']}/{_m2['n_inherited_known']})")
    _ctl = [e for e in _m2["events"] if e["merge_status"] == "control"][0]
    chk(abs(_ctl["disp_A"] - 3.0) < 1e-9,
        f"[양성] control 은 **disp_A 최대** 한 건 (얻은 {_ctl['disp_A']})")
    chk(_m2["taken"] == 2 and len(_m2["inherited"]) == 1,
        "[양성] inherited 는 산출에서 빠지되 **기록으로 남는다** (조용히 안 버린다)")
    chk(_m2["n_new"] == 1,
        "[양성] ★ control 은 n_new 에 **안 센다** (재현 대조지 새 사건이 아니다)")

    #: 겹침 0 이면 control 0
    _dk0 = _mkdir_ev("lag5b", 5.0, [("ev01_atom99", 99, 9.9, "Z")])
    _m3 = merge_events_dirs([_d1, _d2], _tmp / "u3", known=_dk0,
                            log=lambda *a, **k: None)
    chk(_m3["n_control"] == 0 and _m3["n_new"] == 3,
        "[경계] known 과 겹침이 0 이면 control 도 0")

    # ── 음성 경로 — 틀린 입력을 **잡아내는지** ─────────────────────────────
    chk(_dies(lambda: merge_events_dirs([_d1], _tmp / "x", log=lambda *a, **k: None),
              "--merge_known 도 없다"),
        "[음성] dir 하나 + known 없음 → 거부한다 (합칠 것도 뺄 것도 없다)")
    _m1 = merge_events_dirs([_d1], _tmp / "u4", known=_dk, log=lambda *a, **k: None)
    chk(_m1["n_new"] == 0 and _m1["n_control"] == 1 and _m1["n_inherited_known"] == 1,
        f"[경계] dir 하나라도 known 이 있으면 돈다 — lag1 2 건이 전부 known 과 겹쳐 "
        f"new 0 · control 1 (얻은 {_m1['n_new']}/{_m1['n_control']})")
    _empty = _tmp / "noev"; _empty.mkdir(exist_ok=True)
    chk(_dies(lambda: merge_events_dirs([_d1, _empty], _tmp / "x",
                                        log=lambda *a, **k: None), "가 없다"),
        "[음성] events.json 이 없는 디렉터리를 거부한다")
    _dt = _mkdir_ev("trunc", 3.0, [("ev01_atom20", 20, 2.5, "D")], truncated=True)
    chk(_dies(lambda: merge_events_dirs([_d1, _dt], _tmp / "x",
                                        log=lambda *a, **k: None), "truncated"),
        "[음성] truncated=true 목록은 합치지 않는다 (사람이 N 을 골랐다)")
    _dm = _mkdir_ev("mix", 3.0, [("ev01_atom21", 21, 2.5, "E")], min_dist=1.5)
    chk(_dies(lambda: merge_events_dirs([_d1, _dm], _tmp / "x",
                                        log=lambda *a, **k: None), "문턱이 섞였다"),
        "[음성] 서로 다른 min_dist_A 를 섞으면 거부한다")
    _dsame = _mkdir_ev("lag1b", 1.0, [("ev01_atom22", 22, 2.5, "F")])
    chk(_dies(lambda: merge_events_dirs([_d1, _dsame], _tmp / "x",
                                        log=lambda *a, **k: None), "같은 lag"),
        "[음성] 같은 lag 이 두 번 들어오면 거부한다 (같은 dir 두 번)")
    _dnox = _mkdir_ev("noxyz", 4.0, [("ev01_atom23", 23, 2.5, "G")],
                      write_xyz_for=set())
    chk(_dies(lambda: merge_events_dirs([_d1, _dnox], _tmp / "x",
                                        log=lambda *a, **k: None), "미회수"),
        "[음성] 끝점 xyz 가 없으면 **없음이 아니라 미회수**로 보고 중단한다")
    _dkm = _mkdir_ev("lag5c", 5.0, [("ev01_atom10", 10, 3.0, "A")], min_dist=1.5)
    chk(_dies(lambda: merge_events_dirs([_d1, _d2], _tmp / "x", known=_dkm,
                                        log=lambda *a, **k: None), "문턱이 다르다"),
        "[음성] --merge_known 의 문턱이 다르면 거부한다 (겹침 판정이 성립 안 한다)")
    shutil.rmtree(_tmp, ignore_errors=True)

    #: ⛔ 판정 출력은 **마지막 시험 뒤**다. 앞에 두면 뒤에 붙는 시험이 ok 를 떨어뜨려도
    #   화면은 PASS 라고 말한다 — 종료코드와 화면이 갈린다 (2026-09-20 실측).
    print("selftest " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def _build_parser():
    ap = argparse.ArgumentParser()
    ap.add_argument("--traj", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--save_fs", type=float, default=None,
                    help="fs between saved frames (auto from aimd_results.json if omitted)")
    ap.add_argument("--lags_ps", type=float, nargs="+", default=[0.5, 2.0, 10.0])
    ap.add_argument("--jump_lag_ps", type=float, default=2.0)
    ap.add_argument("--hop_smooth_ps", type=float, default=2.0,
                    help="rolling-mode window (ps) that removes boundary-vibration flicker "
                         "from the per-frame cage label before counting hops")
    ap.add_argument("--t_from_ps", type=float, default=None,
                    help="이 시각부터 (포함) — 융체·담금질을 빼고 유리만 보려면 쓴다")
    ap.add_argument("--t_to_ps", type=float, default=None, help="이 시각까지 (포함)")
    ap.add_argument("--hop_events_top", type=int, default=None,
                    help="홉 사건 상위 N 개의 시작·끝 구조를 뽑는다 (NEB 후보 · 계산 0). "
                         "⚠ N 을 사람이 고르는 것이라 사전등록 규칙과 어긋날 수 있다 — "
                         "소셀 NEB 는 --hop_events_all 을 쓴다")
    # ⭐ 2026-09-18 — NEB 카드 §0b-②-1 비준: *"문턱을 넘긴 것 **전부**. N 을 사람이
    #   고르지 않는다 — **문턱이 고른다**."* 상위 N 은 그 규칙을 어길 수 있는 손잡이다.
    ap.add_argument("--hop_events_all", action="store_true",
                    help="문턱을 넘긴 사건을 **전부** 뽑는다 (사전등록 규칙용). "
                         "--hop_events_top 과 같이 주면 거부한다")
    ap.add_argument("--hop_census_lag_ps", type=float, default=None,
                    help="케이지 없이 변위로 홉을 센다 — 이 lag 로 (0 = 창 전체)")
    ap.add_argument("--hop_min_dist", type=float, default=2.5,
                    help="min unwrapped displacement (A) across a cage transition to count it "
                         "as a real inter-cage hop (excludes ~1 A rattle)")
    # ⛔ 2026-08-28 — 여기가 **8.0 으로 남아 있어서** 함수 쪽 적응형 rmax 가
    #   한 번도 안 먹었다. 실측 33/33 궤적이 전부 잘려서 못 읽는 상태로 나왔다.
    #   함수 기본값만 고치고 **배선을 안 고친 것**이다 — selftest 는 함수를 직접
    #   불러서 CLI 를 한 번도 안 탔고, 그래서 통과했다.
    ap.add_argument("--rmax", type=float, default=None,
                    help="기본 None = 가장 긴 lag 의 최대 변위에서 자동으로 잡는다. "
                         "고정하면 빠른 계에서 분포가 잘린다")
    ap.add_argument("--nbins", type=int, default=160)
    # ⛔ 2026-08-28 (리뷰 L · §3-1) — nbins 고정 + rmax 적응형이면 **bin 폭이 런마다 다르다**.
    #   런간 봉우리 비교를 하려면 폭을 고정해야 한다. --dr 를 주면 nbins 는 무시된다.
    ap.add_argument("--dr", type=float, default=None,
                    help="bin 폭 [Å] 고정 (런간 비교용). 주면 --nbins 대신 이걸 쓴다")
    ap.add_argument("--dr_sweep", type=float, nargs="*", default=None,
                    metavar="DR",
                    help=f"bin 폭 민감도 사다리. 값 없이 주면 {list(DR_LADDER)} 를 쓴다")
    ap.add_argument("--dr_sweep_lag_ps", type=float, default=None,
                    help="민감도를 볼 lag [ps] (기본: --lags_ps 의 마지막)")
    return ap


def main():
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    #: 합집합 모드 — 궤적을 안 읽으므로 본 파서의 required 를 타지 않는다.
    if "--merge_events" in sys.argv:
        sys.exit(_merge_cli(sys.argv[1:]))
    ap = _build_parser()
    args = ap.parse_args()

    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    save_fs = args.save_fs
    if save_fs is None:
        sib = Path(args.traj).parent / "aimd_results.json"
        if sib.exists():
            try:
                save_fs = float(json.load(open(sib)).get("save_fs"))
            except Exception:
                pass
    if save_fs is None:
        sys.exit("ERROR: --save_fs required (could not auto-read aimd_results.json)")
    dt_ps = save_fs / 1000.0

    sym, pos, cells = read_traj(args.traj)
    #: ⭐ 2026-09-18 — 창 슬라이스. melt-quench 한 파일에서 **유리 구간만** 보려면 필요하다.
    pos, cells, _w_lo, _w_hi = slice_window(pos, cells, dt_ps, args.t_from_ps, args.t_to_ps)
    if args.t_from_ps is not None or args.t_to_ps is not None:
        print(f"[창] 프레임 {_w_lo}–{_w_hi-1} = {_w_lo*dt_ps:.1f}–{(_w_hi-1)*dt_ps:.1f} ps "
              f"({_w_hi-_w_lo} 프레임)")
    T = len(pos)
    cell0 = cells[0]
    Li = np.where(sym == "Li")[0]
    cen, ctype = free_anions(sym, pos[0], cell0)
    print(f"[{args.label}] frames={T}  dt={dt_ps:.4f} ps  total={T*dt_ps:.1f} ps  "
          f"Li={len(Li)}  cages={len(cen)} ({int((ctype=='S').sum())}S+{int((ctype=='Cl').sum())}Cl)")

    # unwrapped Li (for displacements/MSD/van Hove)
    cart_uw = unwrap(pos, cell0)
    Li_uw = cart_uw[:, Li, :]

    # ---- MSD -> D ----
    msd = ((Li_uw - Li_uw[0]) ** 2).sum(-1).mean(-1)        # (T,)
    t = np.arange(T) * dt_ps
    w = (t > 0.2 * t[-1]) & (t < 0.9 * t[-1])
    D = None
    if w.sum() > 5:
        slope = np.polyfit(t[w], msd[w], 1)[0]              # A^2/ps
        D = slope / 6.0 * 1e-16 / 1e-12                     # cm^2/s
    np.savetxt(out / f"{args.label}_msd.csv",
               np.c_[t, msd], delimiter=",", header="t_ps,MSD_A2", comments="")

    # ---- 케이지 없는 홉 집계 (2026-09-18) ----
    hopc = None
    if args.hop_census_lag_ps is not None:
        hopc = hop_census(Li_uw, dt_ps, args.hop_census_lag_ps, args.hop_min_dist)
        print(f"[홉집계] lag {hopc['lag_ps']:.1f} ps · 문턱 {hopc['min_dist_A']} Å → "
              f"**{hopc['n_moved']}/{hopc['n_Li']} Li** 이동 ({100*hopc['frac_moved']:.1f} %) · "
              f"이온별 최대변위 중앙값 {hopc['per_ion_max_A']['median']:.2f} Å · "
              f"p90 {hopc['per_ion_max_A']['p90']:.2f} · max {hopc['per_ion_max_A']['max']:.2f}")
        print("  ⛔ 이 수는 **하한**이다 — 되돌아온 홉이 한 번으로 보인다.")
        (out / f"{args.label}_hop_census.json").write_text(
            json.dumps(hopc, ensure_ascii=False, indent=1), encoding="utf-8")

        #: ⭐ NEB 후보 뽑기 — **기계적**이다. 변위 내림차순 상위 N, 사람이 안 고른다.
        if args.hop_events_all and args.hop_events_top:
            raise SystemExit("⛔ --hop_events_all 과 --hop_events_top 을 같이 줬다. "
                             "어느 규칙인지 알 수 없으므로 시작하지 않는다.")
        n_take = len(hopc["events"]) if args.hop_events_all else args.hop_events_top
        if n_take:
            evd = out / "events"; evd.mkdir(exist_ok=True)
            man = []
            #: ⛔ 자르면 **화면에** 말한다. events.json 안에만 적으면 아무도 안 본다.
            if n_take < len(hopc["events"]):
                print(f"    ⚠ 문턱을 넘긴 사건 {len(hopc['events'])} 개 중 **{n_take} 개만** "
                      f"뽑는다 — 사전등록 규칙이 '전부' 면 이건 위반이다 (--hop_events_all)")
            else:
                print(f"    ✓ 문턱을 넘긴 사건 **전부** {n_take} 개 (N 을 문턱이 골랐다)")
            for k, ev in enumerate(hopc["events"][:n_take], 1):
                a, p0, p1, cell, d_mic = hop_endpoints(sym, pos, cells, Li, ev, dt_ps)
                tag = f"ev{k:02d}_atom{a}"
                write_xyz(evd / f"{tag}_i.xyz", sym, p0, cell, f"t_ps={ev['t_start_ps']}")
                write_xyz(evd / f"{tag}_f.xyz", sym, p1, cell, f"t_ps={ev['t_end_ps']}")
                man.append({**ev, "atom_index": a, "tag": tag,
                            "disp_minimum_image_A": d_mic,
                            "⚠_이미지보정": abs(d_mic - ev["disp_A"]) > 1e-6})
                print(f"    {tag}: {ev['t_start_ps']:.0f}→{ev['t_end_ps']:.0f} ps · "
                      f"변위 {ev['disp_A']:.2f} Å" +
                      (f" (최소이미지 보정 후 {d_mic:.2f})" if abs(d_mic - ev['disp_A']) > 1e-6 else ""))
            (evd / "events.json").write_text(
                json.dumps({"rule": ("변위 내림차순 · 이온당 사건 1개 · " +
                                     ("**문턱을 넘긴 전부**(--hop_events_all, NEB 카드 §0b-②-1)"
                                      if args.hop_events_all else
                                      "상위 N(--hop_events_top) ⚠ 사람이 N 을 골랐다")),
                            "truncated": n_take < len(hopc["events"]),
                            "lag_ps": hopc["lag_ps"], "min_dist_A": hopc["min_dist_A"],
                            "n_total_events": len(hopc["events"]), "taken": len(man),
                            "⛔_끝이_최소인지는_모른다": "이완은 다음 단계다. 되돌아오는 나들이면 "
                                                      "끝이 시작으로 무너질 수 있다.",
                            "events": man}, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"  → {evd}/  ({len(man)} 쌍 · events.json)")

    # ---- Van Hove self Gs(r, dt) ----
    rc, cols, hdr, skipped, vhinfo = van_hove(Li_uw, dt_ps, args.lags_ps,
                                             args.rmax, args.nbins, dr=args.dr)
    # ⛔ 2026-08-28 (리뷰 L · P0-1) — 아래 inter-cage 히스토그램이 `edges` 를 쓰는데
    #   그건 van_hove() 의 **지역변수**다. van_hove 를 함수로 뽑을 때 이 참조를 안 고쳤고,
    #   **홉이 하나라도 잡히면 NameError** 로 죽었다. 같은 격자를 여기서 다시 만든다.
    edges = np.linspace(0, vhinfo["rmax_A"], vhinfo["nbins"] + 1)
    if skipped:
        print(f"  ! lag {skipped} ps 는 궤적({T*dt_ps:.1f} ps)보다 길어 건너뛴다")
    np.savetxt(out / f"{args.label}_vanhove.csv", np.c_[[rc] + cols].T,
               delimiter=",", header=",".join(["r_A"] + hdr), comments="")
    # ★ 25개를 쓸어 담을 때 CSV 25장을 눈으로 볼 수는 없다 — **판정을 한 줄로** 찍는다.
    #   보는 것: 긴 lag 에서 자리 간격(≳2 Å)에 두 번째 봉우리가 자랐는가.
    vh_verdict = []
    for lp, g, tf, pk, pkr, mr in zip(
            [x for x in args.lags_ps if x not in skipped], cols,
            vhinfo["trunc_frac"], vhinfo["peak_A"], vhinfo["peak_raw_A"],
            vhinfo["msd_ratio"]):
        r2, h2 = second_peak(rc, g)
        vh_verdict.append({"lag_ps": lp, "first_peak_A": round(pk, 2),
                           "first_peak_raw_A": round(pkr, 2),
                           "second_peak_A": None if r2 is None else round(r2, 2),
                           "second_peak_h": round(h2, 5), "trunc_frac": round(tf, 4),
                           "msd_ratio": mr})
    # ★ 분포를 읽기 **전에** 분포가 성립하는지 본다 (리뷰 L4 · 불변식 ∫r²P dr = ⟨Δr²⟩).
    #   여기가 어긋나면 아래 봉우리 판정은 전부 무의미하다 — 그래서 먼저 찍는다.
    bad_inv = [(v["lag_ps"], v["msd_ratio"]) for v in vh_verdict
               if v["msd_ratio"] is None or abs(v["msd_ratio"] - 1.0) > MSD_INVARIANT_TOL]
    if vh_verdict:
        _r = [v["msd_ratio"] for v in vh_verdict if v["msd_ratio"] is not None]
        print(f"  불변식 ∫r²P_s dr / ⟨Δr²⟩ = "
              f"{min(_r):.4f}–{max(_r):.4f} (허용 1±{MSD_INVARIANT_TOL})"
              + ("" if not bad_inv else "  ⇒ ⛔ **히스토그램을 못 믿는다**"))
        if bad_inv:
            print(f"     lag {[b[0] for b in bad_inv]} ps 에서 벗어난다 — 잘림"
                  f"({100*max(v['trunc_frac'] for v in vh_verdict):.1f} %) 또는 격자가 거칠다. "
                  f"봉우리 판정을 인용하지 말 것")
    if vh_verdict:
        a, b = vh_verdict[0], vh_verdict[-1]
        shift = b["first_peak_A"] - a["first_peak_A"]
        print(f"  vanHove: dt {a['lag_ps']:g}→{b['lag_ps']:g} ps · **1st peak "
              f"{a['first_peak_A']} → {b['first_peak_A']} Å (Δ{shift:+.2f})** · "
              f"rmax {vhinfo['rmax_A']} Å · dr {vhinfo['dr_A']:.3f} Å · "
              f"잘림 {100*b['trunc_frac']:.1f} %")
        # ⚠ 봉우리는 이제 **보간값**이다 (argmax 는 bin 격자에 양자화돼 있다).
        #   dr 규모의 차이를 주장하려면 --dr_sweep 으로 격자 무관성을 먼저 보여야 한다.
        if abs(shift) < 2.0 * vhinfo["dr_A"]:
            print(f"     ⚠ 이동량 {abs(shift):.2f} Å 가 **bin 폭 {vhinfo['dr_A']:.3f} Å 의 "
                  f"2배 미만**이다 — `--dr_sweep` 없이 이 차이를 주장하지 말 것")
        # ★ 주 지표는 **봉우리 이동**이다 (2026-08-28 실측 수정 — van_hove docstring 참조)
        if b["trunc_frac"] > 0.02:
            print(f"  ⇒ ⛔ 분포의 {100*b['trunc_frac']:.1f} % 가 rmax 밖이다 — **잘려서 못 읽는다.** "
                  f"--rmax 를 키울 것")
        elif shift >= 0.5:
            # ⚠ 판정 문구에 다른 판정의 어휘를 안 쓴다 (watch 분류기가 겹쳐 센 적 있다).
            # ⛔ 2026-08-28 (리뷰 L · P0-2) — 카드에는 "갇힘/고원/확산" 세 체제라고 써 놓고
            #   **코드는 shift ≥ 0.5 를 전부 '확산' 이라고 찍고 있었다.** 문서와 코드가 갈렸다.
            #   (그 전에 넣었다고 생각한 편집이 실제로는 안 붙었는데, selftest 가 판정 **문구**를
            #    안 보기 때문에 통과했다 — 오늘 세 번째 같은 유형이다.)
            SITE_LO, SITE_HI = 3.2, 4.8
            if SITE_LO <= b["first_peak_A"] <= SITE_HI:
                print(f"  ⇒ **움직인다 — 자리 간격 고원**이다 (봉우리 {b['first_peak_A']} Å, "
                      f"Δ{shift:+.2f}). 홉이 대략 한 번 수준이라 **이 구간에서는 D 에 둔감**하다 "
                      f"— 빠르기 비교에 쓰지 말 것")
            else:
                print(f"  ⇒ **확산한다** — 봉우리가 {shift:+.2f} Å 밖으로 이동했다 "
                      f"(고원 밖: {b['first_peak_A']} Å)")
        elif shift <= 0.2:
            print(f"  ⇒ ⚠ **봉우리가 제자리다** ({shift:+.2f} Å) — 이 창에서는 "
                  f"cage 안 흔들림이 지배적이다")
            if vhinfo["rmax_A"] > 12:
                print(f"     ⚠ 다만 rmax 가 {vhinfo['rmax_A']} Å 로 잡혔다 — "
                      f"**소수는 멀리 갔다.** 봉우리는 최빈값이라 그 꼬리를 안 센다")
        else:
            print(f"  ⇒ ⚠ 중간 ({shift:+.2f} Å) — 어느 쪽도 주장하지 않는다. "
                  f"더 긴 lag 이 필요하다")

    # ---- bin 폭 민감도 (리뷰 L4) ----
    # 고원(600→800 K 3 %)이 진짜 물리인지 **격자 인공물**인지 가른다.
    sweep_rows, sweep_verdict = [], None
    if args.dr_sweep is not None:
        drs = tuple(args.dr_sweep) if args.dr_sweep else DR_LADDER
        lag_s = args.dr_sweep_lag_ps or [x for x in args.lags_ps if x not in skipped][-1]
        sweep_rows, sweep_verdict = dr_sweep(Li_uw, dt_ps, lag_s, drs, rmax=args.rmax)
        print(f"  dr 사다리 (lag {lag_s:g} ps · smooth {sweep_verdict['smooth_A']} Å):")
        for r_ in sweep_rows:
            print(f"    dr {r_['dr_A']:.3f} Å → peak {r_['peak_A']:.3f} Å "
                  f"(무평활 {r_['peak_nosmooth_A']:.3f} · argmax {r_['peak_argmax_A']:.3f}) · "
                  f"불변식 {r_['msd_ratio']} · 잘림 {100*r_['trunc_frac']:.1f} %")
        if sweep_verdict["verdict"] == "stable":
            print(f"  ⇒ **격자 무관** — 산포 {sweep_verdict['spread_A']} Å "
                  f"≤ 허용 {sweep_verdict['tol_A']} Å. 봉우리 "
                  f"{sweep_verdict['peak_mean_A']} Å 는 binning 인공물이 아니다")
        elif sweep_verdict["verdict"] == "unstable":
            print(f"  ⇒ ⛔ **격자에 민감하다** — 산포 {sweep_verdict['spread_A']} Å "
                  f"> 허용 {sweep_verdict['tol_A']} Å. 이 봉우리로 온도·조성을 "
                  f"비교하면 안 된다")
        else:
            print(f"  ⇒ ⚠ 사다리 점이 부족해 판정 못 한다 ({len(sweep_rows)}점)")
        if sweep_verdict.get("mode_noise") == "high":
            print(f"  ⇒ ⛔ **최빈값이 표본 잡음으로 튄다** (무평활 산포 "
                  f"{sweep_verdict['mode_noise_spread_A']} Å) — dr 을 줄여도 안 낫는다. "
                  f"분포의 최대가 넓고 평평하다는 뜻이다")
        if sweep_verdict.get("resolvable_delta_A") is not None:
            print(f"  ⇒ **인용 가능한 최소 차이 ≈ {sweep_verdict['resolvable_delta_A']} Å** — "
                  f"이보다 작은 온도·조성 차이는 이 지표로 주장하지 말 것")
        if sweep_rows:
            np.savetxt(out / f"{args.label}_dr_sweep.csv",
                       np.array([[r_["dr_A"], r_["peak_A"], r_["peak_nosmooth_A"],
                                  r_["peak_argmax_A"], r_["msd_ratio"], r_["trunc_frac"]]
                                 for r_ in sweep_rows]),
                       delimiter=",",
                       header="dr_A,peak_smoothed_A,peak_nosmooth_A,peak_argmax_A,"
                              "msd_ratio,trunc_frac",
                       comments="")

    # ---- cage-resolved hops (inter-cage), flicker-robust ----
    # naive "nearest-centre changed" counts boundary vibration as hops. Instead:
    #   (1) smooth each Li's per-frame cage label by a rolling MODE (kills flicker)
    #   (2) count transitions in the smoothed label ONLY if the Li's unwrapped
    #       displacement across the transition window exceeds --hop_min_dist (a
    #       real cage-to-cage move, not a ~1 A rattle).
    cart = pos[:, :, :]
    # ⛔ 2026-09-18 — 케이지 중심이 **하나도 없는** 궤적(자유 음이온 0)에서
    #   argmin 이 빈 축을 받아 `ValueError: argmin of an empty sequence` 로 죽었다.
    #   처리 안 된 numpy 오류라 사람은 "도구가 깨졌다" 로 읽는다 — 사실은
    #   **이 계에 케이지가 없다**는 결과다. '못 함' 과 '없음' 을 가른다.
    if len(cen) == 0:
        print("    ⚠ 자유 음이온(케이지 중심)이 **0 개** — 케이지 기반 홉 집계를 건너뛴다. "
              "변위 기반 집계(--hop_census_lag_ps)는 그대로 유효하다.")
        cage_skipped = True
    else:
        cage_skipped = False
        assign = np.empty((T, len(Li)), int)
        for ti in range(T):
            assign[ti] = np.argmin(mic(cart[ti, Li], cart[ti, cen], cells[ti]), axis=1)

    sw = max(3, int(round(args.hop_smooth_ps / dt_ps)))      # rolling-mode window
    h = sw // 2

    def rolling_mode(a):
        o = np.empty(len(a), int)
        for t in range(len(a)):
            seg = a[max(0, t - h):min(len(a), t + h + 1)]
            o[t] = np.bincount(seg).argmax()
        return o

    inter_hops, flick = 0, 0
    hop_dists = []
    for k in (range(len(Li)) if not cage_skipped else []):
        a = assign[:, k]
        flick += int((np.diff(a) != 0).sum())
        sm = rolling_mode(a)
        for ti in np.where(np.diff(sm) != 0)[0]:
            lo, hi = max(0, ti - h), min(T - 1, ti + h)
            d = np.linalg.norm(Li_uw[hi, k] - Li_uw[lo, k])
            if d >= args.hop_min_dist:
                inter_hops += 1
                hop_dists.append(d)
    intra_changes = flick
    total_ps = T * dt_ps
    rate = inter_hops / len(Li) / (total_ps / 1000.0)       # hops / Li / ns
    hop_dists = np.array(hop_dists)
    if len(hop_dists):
        hh, _ = np.histogram(hop_dists, bins=edges, density=True)
        np.savetxt(out / f"{args.label}_intercage_hopdist.csv", np.c_[rc, hh],
                   delimiter=",", header="r_A,P_intercage_hop", comments="")

    summary = {
        "label": args.label, "frames": T, "dt_ps": dt_ps, "total_ps": total_ps,
        "n_Li": len(Li), "n_cages": int(len(cen)),
        "cage_Cl_fraction": round(float((ctype == "Cl").mean()), 3) if len(ctype) else None,
        # ⛔ 2026-08-28 (리뷰 L · P0-4) — 이 D 는 **정본 창(2–50 ps)이 아니다.**
        #   single-origin 20–90 % 적합이다. 일반 이름으로 두면 정본 D 와 섞인다.
        "D_single_origin_diagnostic_cm2_s": D,
        "⛔_D_규약": ("정본은 MSD 창 2–50 ps · 자유절편이다(CLAUDE.md). 이 값은 "
                     "single-origin 20–90 % 적합이라 **정본 D 로 인용 금지** — 진단용이다."),
        # ⛔ 케이지가 없어 건너뛴 것과 **0 건**은 다르다 — 0 으로 그리지 않는다.
        "cage_analysis_skipped": cage_skipped,
        "inter_cage_hops": None if cage_skipped else inter_hops,
        "inter_cage_hop_rate_per_Li_per_ns": None if cage_skipped else round(rate, 4),
        "inter_cage_hop_dist_mean_A": round(float(hop_dists.mean()), 3) if len(hop_dists) else None,
        "transient_cage_flickers": None if cage_skipped else flick,
        "hop_smooth_frames": sw,
        "hop_min_dist_A": args.hop_min_dist,
        "van_hove": vh_verdict, "van_hove_info": vhinfo,
        "msd_invariant_ok": (not bad_inv) if vh_verdict else None,
        "dr_sweep": sweep_rows or None, "dr_sweep_verdict": sweep_verdict,
        "files": [f"{args.label}_{s}.csv" for s in ("vanhove", "msd", "intercage_hopdist")],
    }
    (out / f"{args.label}_jumpstats.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    print(f"\n-> {out}/  (vanhove.csv = Fig-2d-style distance distribution; "
          f"inter-cage hop rate = long-range/σ proxy)")


if __name__ == "__main__":
    main()
