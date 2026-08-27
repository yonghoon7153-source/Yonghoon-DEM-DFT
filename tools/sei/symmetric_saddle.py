#!/usr/bin/env python3
"""symmetric_saddle.py — **대칭 홉**의 장벽을 relax 2회로 얻는다 (full NEB 대체).

왜 (2026-08-16)
  li3nd c→c 의 셀 수렴을 확인하려면 3×3×3(107원자) 장벽이 필요하다. 그런데 full NEB 은
  이미지 7 × 스텝 ~80 ≈ **560 SCF** 다. 이 홉은 대칭이라 그럴 필요가 없다:

    · 양 끝점이 **대칭 동등**하면 안장점은 경로 중앙에 대칭으로 놓인다.
    · 실측 증거: 2×2×2 ccpath 에서 CI 가 값을 **1 μeV** 만 바꿨다
      (`no-CI 0.228980 → CI 0.228981`). 안장점이 이미 중점 이미지 위에 있었다는 뜻이다.

  → 중점에 뛰는 원자를 **고정**하고 나머지를 이완하면 그게 안장점이다.
    끝점 1 + 안장 1 = **2 relax**. 수십~수백 배 싸다.

⛔ 대칭이 아니면 쓰면 안 된다
  비대칭 홉(li3nd c→b 처럼 자리 종류가 다름)은 안장점이 중점에 없다. 두 근거 중
  하나가 있어야 통과하고, **어느 쪽으로 통과했는지 기록한다**:
    (a) `meta.endpoints_symmetry_equivalent = true` — spglib orbit 판정
    (b) **측정된 끝점 에너지 축퇴** |ΔE| ≤ 20 meV — 이완된 두 끝점 에너지가 같다
  (b) 를 넣은 이유: cc333 은 build 가 "끝점 미이완" 으로 조기 반환해 meta.json 이
  없는데, 재생성하면 `.ep_hash` 가 달라져 **이미 돌린 끝점 relax 를 버린다**.
  그리고 (b) 는 메타데이터가 아니라 실측이라 근거로 더 낫다.
  ⚠ (b) 는 **필요조건이지 충분조건이 아니다** — 대칭 비동등한 두 자리가 우연히 같은
  에너지일 수 있다. (b) 로만 통과하면 경고를 남긴다.

프로토콜 일치
  안장 입력은 `ep_initial/relax.in` 의 헤더(cell·k·q·smearing·PP·cutoff)를 **그대로
  복사**해 만든다. 다시 계산하지 않는다 — 그래야 두 에너지가 같은 규약이 된다.

  python3 tools/sei/symmetric_saddle.py --work /data/work/runs/sei_neb_v2_cc333 --tag li3nd
  python3 tools/sei/symmetric_saddle.py --work ... --tag li3nd --collect
  python3 tools/sei/symmetric_saddle.py --selftest

이 도구가 못 하는 것
  · 안장점을 **찾지** 않는다. 대칭으로 결정된 중점을 쓴다 — 대칭이 깨지면 틀린다.
  · 비대칭 홉·다중 안장 경로에 못 쓴다 (거부한다).
  · 경로 형상(반응좌표)을 주지 않는다. 장벽 높이 하나만 준다.
  · 이완 후 **수직 힘**은 보고만 한다 — 자동으로 판정하지 않는다.
  · 셀 수렴을 대신 해주지 않는다. 다른 셀에서 이 도구를 두 번 돌려 비교하는 것이 목적이다.
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ⛔ 2026-08-16 (Codex 리뷰) — Windows 기본 인코딩(cp949)에서 selftest 가 죽었다.
#   파일은 open(..., encoding="utf-8") 로 막았지만 **stdout 도 막아야** 한다.
#   재설정이 안 되는 환경(파이프·리다이렉트)에서는 표식을 ASCII 로 낮춘다.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    _OK, _NG = "\u2713", "\u2717"
except Exception:                                    # pragma: no cover
    _OK, _NG = "OK", "XX"


def _p(s):
    """비-UTF8 stdout 에서도 죽지 않고 찍는다."""
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode("ascii"))
#: 끝점 에너지 축퇴 문턱 [eV] — 이보다 크면 대칭 홉으로 안 본다.
#:  0.229 eV 장벽 대비 20 meV 는 9% — 그 이상 어긋나면 중점이 안장점이라는 전제가 흔들린다.
ENDPOINT_TOL_EV = 0.020
#: 고정 대상 원자가 끝점 사이에서 움직여도 되는 한계 [Å] — 넘으면 Ea 오염 (리뷰 F2)
FROZEN_SHIFT_TOL_A = 0.05


def _pos_block(txt, start):
    """start 부터의 첫 ATOMIC_POSITIONS 블록 → [(sym,[x,y,z])] (angstrom 만)."""
    m = re.search(r"ATOMIC_POSITIONS\s*\(?(\w+)", txt[start:])
    if not m or m.group(1).lower() != "angstrom":
        return None
    s = start + m.end()
    rows = []
    for l in txt[s:].splitlines()[1:]:
        q = l.split()
        if len(q) >= 4 and re.match(r"^[A-Z][a-z]?\d*$", q[0]):
            rows.append((q[0], [float(q[1]), float(q[2]), float(q[3])]))
        elif rows:
            break
    return rows or None


def last_force(txt):
    """마지막 `Total force = X` [Ry/au]. 없으면 None."""
    f = re.findall(r"Total force\s*=\s*([\d.eE+-]+)", txt)
    return float(f[-1]) if f else None


def read_relaxed(outp, allow_unconverged=False):
    """이완 좌표를 읽는다 → (rows, err, info).

    ⚠ 2026-08-16 — 옛 판은 `Begin final coordinates` 만 봤다. 그런데 QE 는 BFGS 가
    **수렴했을 때만** 그 블록을 찍는다. cc333 끝점은 nstep 한도에서 끝나(16h41m)
    그 블록이 없고, 힘이 0.018 Ry/au (문턱 1e-3 의 **18배**) 에서 진동만 했다.
    그런 산출물을 조용히 '이완됨' 으로 쓰면 안 되고, 그렇다고 좌표가 없는 것도 아니다.
    → 마지막 BFGS 스텝의 ATOMIC_POSITIONS 로 후퇴하되 **미수렴을 명시**한다.
    """
    if not os.path.isfile(outp):
        return None, f"없음: {outp}", {}
    t = open(outp, encoding="utf-8", errors="replace").read()
    if "JOB DONE" not in t:
        return None, f"아직 안 끝났다 (JOB DONE 없음): {outp}", {}
    info = {"last_total_force_Ry_au": last_force(t),
            "max_steps_reached": "The maximum number of steps has been reached" in t}
    i = t.rfind("Begin final coordinates")
    if i >= 0:
        rows = _pos_block(t, i)
        info["converged"] = True
        if rows:
            return rows, None, info
    # ── 미수렴 후퇴 ──
    info["converged"] = False
    j = t.rfind("ATOMIC_POSITIONS")
    rows = _pos_block(t, j) if j >= 0 else None
    if rows is None:
        return None, f"좌표를 못 읽었다: {outp}", info
    if not allow_unconverged:
        return None, (f"⛔ 이완이 수렴하지 않았다: {outp}\n"
                      f"      마지막 Total force = {info['last_total_force_Ry_au']} Ry/au "
                      f"(= {(info['last_total_force_Ry_au'] or 0)*25.711:.2f} eV/Å)"
                      + (", nstep 한도 도달" if info["max_steps_reached"] else "") + "\n"
                      f"      좌표는 있다 — 미수렴을 감수하고 쓰려면 --allow_unconverged"), info
    return rows, None, info


#: 안장 판정 문턱 — 구속 해제 후 이동 원자에 **홉 방향으로** 남은 힘 [Ry/au].
#:  relax 의 forc_conv_thr(1e-3)과 같은 눈금을 쓴다. 대칭점이면 0 이어야 하므로
#:  남은 값은 수치잡음 + 대칭 깨짐이다.
SADDLE_FORCE_TOL_RY_AU = 1.0e-3
#: ±δ 탐침 변위 [Å] — 안장이면 양쪽 다 에너지가 **내려가야** 한다.
PROBE_DELTA_A = 0.10


def atom_forces(outp):
    """QE 출력의 마지막 `Forces acting on atoms` 블록 → [[fx,fy,fz], ...] (Ry/au)."""
    t = open(outp, encoding="utf-8", errors="replace").read()
    i = t.rfind("Forces acting on atoms")
    if i < 0:
        return None
    out = []
    for l in t[i:].splitlines()[1:]:
        m = re.search(r"atom\s+\d+\s+type\s+\d+\s+force\s*=\s*"
                      r"([-\d.eE+]+)\s+([-\d.eE+]+)\s+([-\d.eE+]+)", l)
        if m:
            out.append([float(m.group(k)) for k in (1, 2, 3)])
        elif out:
            break
    return out or None


def final_energy(outp):
    """relax.out 의 마지막 총에너지 [eV]. Ry → eV."""
    t = open(outp, encoding="utf-8", errors="replace").read()
    e = re.findall(r"^!\s+total energy\s+=\s+([-\d.]+)\s+Ry", t, re.M)
    return float(e[-1]) * 13.605693122994 if e else None


def parse_input_positions(relax_in):
    """relax.in 의 ATOMIC_POSITIONS (angstrom) → [(sym,[x,y,z])].

    ★ 왜 relax.**in** 인가 (2026-08-16): cc333 의 relax.**out** 은 미수렴 BFGS 가
    50스텝 밀어낸 표류 구조라 홉이 3.667 → 4.203 Å 로 벌어지고 이웃 하나가 1.24 Å
    움직였다. 반면 relax.in 은 이상 좌표(홉 3.667, 나머지 변위 0.000)로 깨끗하다.
    고정셸 방식은 여기서 새로 시작한다 — 표류를 승계하지 않는다.
    """
    txt = open(relax_in, encoding="utf-8").read()
    i = txt.index("ATOMIC_POSITIONS")
    return _pos_block(txt, i)


def parse_cell(relax_in):
    """relax.in 의 CELL_PARAMETERS angstrom → 3×3 리스트."""
    t = open(relax_in, encoding="utf-8").read()
    m = re.search(r"CELL_PARAMETERS\s*\(?angstrom\)?\s*\n((?:\s*[-\d.eE+]+\s+[-\d.eE+]+\s+[-\d.eE+]+\s*\n){3})", t)
    if not m:
        return None
    return [[float(x) for x in l.split()] for l in m.group(1).strip().splitlines()]


def _inv3(m):
    """3×3 역행렬. 특이하면 None."""
    det = (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
           - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
           + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
    if abs(det) < 1e-12:
        return None
    c = [[m[(i+1) % 3][(j+1) % 3]*m[(i+2) % 3][(j+2) % 3]
          - m[(i+1) % 3][(j+2) % 3]*m[(i+2) % 3][(j+1) % 3] for j in range(3)]
         for i in range(3)]
    return [[c[j][i]/det for j in range(3)] for i in range(3)]   # adj/det = 전치


def min_image(d, cell):
    """최소이미지로 변위를 편다. cell 이 없으면 그대로 돌려준다.

    ⛔⛔ 2026-08-27 실측 버그 — 옛 판은 `n ∈ {-1,0,1}³` 만 훑었다. 그러면 **원시 벡터가
      셀보다 훨씬 길 때 못 접는다**: 한 방향으로 최대 1 셀만 뺄 수 있으니 25 Å 짜리는
      15 Å 로만 줄어든다. 끝점 변위(≈1 Å)에서는 안 드러났고, **반전상**(셀 밖에 놓일 수
      있다)을 비교하기 시작하자 곧바로 나왔다 — 10.37 Å 셀에서 잔차 17.39 Å 이 찍혔다.
      그 셀의 min-image 최대는 √3·10.37/2 = 8.98 Å 이라 **물리적으로 불가능한 값**이다.
      → 분수좌표로 먼저 접고, 그 뒤에 ±1 을 훑는다(비직교 셀에서는 접기만으로
        최단이 보장되지 않는다 — 두 단계가 다 필요하다).
    """
    if not cell:
        return d
    import itertools
    inv = _inv3(cell)
    if inv is not None:
        f = [sum(d[k]*inv[k][a] for k in range(3)) for a in range(3)]
        f = [x - round(x) for x in f]
        d = [sum(f[a]*cell[a][k] for a in range(3)) for k in range(3)]
    best, bn = d, sum(x * x for x in d)
    for n in itertools.product((-1, 0, 1), repeat=3):
        c = [d[k] + sum(n[j] * cell[j][k] for j in range(3)) for k in range(3)]
        nn = sum(x * x for x in c)
        if nn < bn:
            best, bn = c, nn
    return best


def endpoint_dir(work_tag_dir, name):
    """끝점 디렉터리 — **수렴본을 고른다.**

    ⛔⛔ 2026-08-16 — 이어달리기는 `ep_initial_r2/` 처럼 새 디렉터리에 들어간다
      (미수렴 원본을 덮지 않으려고). watch 의 [0/4] 는 `_r2` 를 보는데 이 도구는
      `ep_initial/` 만 읽고 있었다 — 그대로 두면 **수렴본을 두고 미수렴 원본으로**
      고정셸을 만든다. 화면과 도구가 다른 파일을 보는 상태였다.

    규칙: `<name>_r2`, `<name>_r3`, … 중 **수렴한 것 중 가장 나중 것**을 쓰고,
    하나도 수렴 안 했으면 원본 `<name>` 을 돌려준다(그럼 게이트가 막는다).
    """
    import glob as _g
    cands = [os.path.join(work_tag_dir, name)]
    cands += sorted(_g.glob(os.path.join(work_tag_dir, name + "_r*")))
    conv = []
    for c in cands:
        o = os.path.join(c, "relax.out")
        if not os.path.isfile(o):
            continue
        try:
            if "Begin final coordinates" in open(o, encoding="utf-8", errors="replace").read():
                conv.append(c)
        except OSError:
            pass
    return conv[-1] if conv else os.path.join(work_tag_dir, name)


def _symmetry_gate(meta, ini_out, fin_out):
    """대칭 근거를 판정한다 → (basis, warn, |ΔE|, sym, detail).

    ⛔⛔ 2026-08-16 (Codex 리뷰) — 앞 판은 **두 갈래로 fail-open** 이었다:
      (a) `endpoints_symmetry_equivalent = False` 인데 에너지 차만 작으면 통과했다.
          spglib 가 "다른 자리" 라고 판정한 홉을 에너지 우연으로 덮은 것이다.
      (b) `JOB DONE` 없는 **실행 중** 끝점도 에너지만 같으면 통과했다.
          미수렴 중간 에너지는 대칭 증거가 될 수 없다 (cc333 이 정확히 그 상태였다).

    지금 규칙:
      sym is False → **무조건 거부.** 에너지로 뒤집지 않는다.
      sym is True  → 통과. 단 |ΔE| 가 문턱을 넘으면 **conflict** 로 표시한다
                     (대칭이라는데 에너지가 다르면 둘 중 하나가 틀린 것이다).
      sym is None  → **완료·수렴된 동일 프로토콜 끝점**에서만 에너지 축퇴를 근거로 쓴다.
    """
    sym = meta.get("endpoints_symmetry_equivalent")
    st = {}
    for name, outp in (("ep_initial", ini_out), ("ep_final", fin_out)):
        info = {"exists": os.path.isfile(outp)}
        if info["exists"]:
            txt = open(outp, encoding="utf-8", errors="replace").read()
            info["job_done"] = "JOB DONE" in txt
            info["converged"] = "Begin final coordinates" in txt
            info["last_force_Ry_au"] = last_force(txt)
            info["energy_eV"] = final_energy(outp)
        st[name] = info
    e1 = st["ep_initial"].get("energy_eV")
    e2 = st["ep_final"].get("energy_eV")
    de = abs(e2 - e1) if (e1 is not None and e2 is not None) else None
    both_done = all(st[n].get("job_done") for n in st)
    both_conv = all(st[n].get("converged") for n in st)
    detail = {"endpoint_state": st, "endpoint_energy_diff_eV": de,
              "both_job_done": both_done, "both_converged": both_conv}

    # (a) spglib 가 아니라고 하면 끝 — 에너지로 뒤집지 않는다
    if sym is False:
        return None, None, de, sym, {**detail, "refusal": "spglib_says_inequivalent"}

    if sym is True:
        warn = None
        if de is not None and de > ENDPOINT_TOL_EV:
            warn = (f"⚠⚠ **conflict**: spglib 는 대칭 동등이라는데 끝점 에너지가 "
                    f"{de*1000:.1f} meV 다르다 (문턱 {ENDPOINT_TOL_EV*1000:.0f}). "
                    f"둘 중 하나가 틀렸다 — 이완 미수렴이거나 구조가 의도와 다르다. "
                    f"장벽을 쓰기 전에 원인을 확인할 것.")
        return "meta.endpoints_symmetry_equivalent=true (spglib orbit)", warn, de, sym, detail

    # (b) sym 정보가 없을 때만 에너지 축퇴로 후퇴 — 단 **완료·수렴** 끝점에서만
    if not both_done:
        return None, None, de, sym, {**detail, "refusal": "endpoints_still_running"}
    if not both_conv:
        return None, None, de, sym, {**detail, "refusal": "endpoints_unconverged"}
    if de is not None and de <= ENDPOINT_TOL_EV:
        return (f"measured endpoint degeneracy |ΔE| = {de*1000:.1f} meV "
                f"≤ {ENDPOINT_TOL_EV*1000:.0f} meV (완료·수렴 끝점)",
                ("⚠ spglib 판정이 없어 **끝점 에너지 축퇴**로만 통과했다. 필요조건이지 "
                 "충분조건이 아니다 — 같은 홉이 더 작은 셀에서 대칭 동등으로 확인됐는지 볼 것."),
                de, sym, detail)
    return None, None, de, sym, {**detail, "refusal": "no_degeneracy"}


def _symmetry_refusal(tag, sym, de, detail=None):
    why = (detail or {}).get("refusal", "")
    lines = [f"⛔ {tag}: 대칭 근거가 없다 — 중점법을 쓸 수 없다.",
             f"   meta.endpoints_symmetry_equivalent = {sym!r}",
             "   끝점 에너지 차 |ΔE| = "
             + (f"{de*1000:.1f} meV" if de is not None else "측정 불가")]
    lines.append({
        "spglib_says_inequivalent":
            "   ⛔ spglib 가 **대칭 비동등**으로 판정했다. 에너지가 같아도 뒤집지 않는다 "
            "— 비대칭 홉은 안장점이 중점에 없다.",
        "endpoints_still_running":
            "   ⛔ 끝점이 아직 도는 중이다 (JOB DONE 없음). 중간 에너지는 대칭 증거가 아니다.",
        "endpoints_unconverged":
            "   ⛔ 끝점 이완이 수렴하지 않았다. 미수렴 에너지 축퇴는 대칭 증거가 아니다.",
        "no_degeneracy":
            f"   ⛔ 에너지 차가 문턱 {ENDPOINT_TOL_EV*1000:.0f} meV 를 넘는다.",
    }.get(why, "   ⛔ 근거 없음"))
    lines += ["   full NEB 을 쓸 것. (정말 강행하려면 --force — 근거를 db 에 남길 것)"]
    return "\n".join(lines)


def build(work, tag, force=False, allow_unconverged=False):
    d = os.path.join(work, tag)
    meta_p = os.path.join(d, "meta.json")
    meta = json.load(open(meta_p, encoding="utf-8")) if os.path.isfile(meta_p) else {}

    ep_i, ep_f = endpoint_dir(d, "ep_initial"), endpoint_dir(d, "ep_final")
    ini_out = os.path.join(ep_i, "relax.out")
    fin_out = os.path.join(ep_f, "relax.out")
    ini_in = os.path.join(ep_i, "relax.in")
    if os.path.basename(ep_i) != "ep_initial" or os.path.basename(ep_f) != "ep_final":
        print(f"   ↻ 이어달리기 수렴본을 쓴다: {os.path.basename(ep_i)} · {os.path.basename(ep_f)}")
    first, e1, i1 = read_relaxed(ini_out, allow_unconverged)
    last, e2, i2 = read_relaxed(fin_out, allow_unconverged)
    if first is None or last is None:
        return 1, (f"⛔ {tag}: 이완된 끝점이 필요하다.\n   {e1 or ''}\n   {e2 or ''}\n"
                   f"   먼저: bash tools/sei/run_sei_neb.sh endpoints {tag}")
    unconv = [n for n, i in (("ep_initial", i1), ("ep_final", i2)) if not i.get("converged")]
    if [s for s, _ in first] != [s for s, _ in last]:
        return 1, f"⛔ {tag}: 두 끝점의 원자 목록이 다르다 — 같은 계가 아니다"

    basis, warn, de, sym, sym_detail = _symmetry_gate(meta, ini_out, fin_out)
    if basis is None and not force:
        return 1, _symmetry_refusal(tag, sym, de, sym_detail)
    if basis is None:
        basis = "⛔ --force (대칭 근거 없음)"

    cell = parse_cell(ini_in)
    # 뛰는 원자 = 두 끝점 사이 변위가 가장 큰 원자
    disp = [min_image([b[k] - a[k] for k in range(3)], cell)
            for (_, a), (_, b) in zip(first, last)]
    dn = [sum(x * x for x in v) ** 0.5 for v in disp]
    j = max(range(len(dn)), key=lambda i: dn[i])
    dmax = dn[j]
    others = sorted(dn)[-2] if len(dn) > 1 else 0.0
    if dmax < 0.5:
        return 1, (f"⛔ {tag}: 두 끝점이 사실상 같은 구조다 (최대 변위 {dmax:.3f} Å) — "
                   f"뛰는 원자가 없다")

    # 중점 구성: 모든 원자를 두 끝점의 중간으로 (= NEB 7이미지의 4번째와 같은 선형보간)
    mid = [(s, [first[i][1][k] + disp[i][k] / 2.0 for k in range(3)])
           for i, (s, _) in enumerate(first)]

    # ── 안장 입력: 끝점 relax.in 헤더를 **그대로** 쓴다 (프로토콜 일치 보장) ──
    src = open(ini_in, encoding="utf-8").read()
    head = src[:src.index("ATOMIC_POSITIONS")]
    tail_i = src.index("K_POINTS")
    tail = src[tail_i:]
    head = head.replace(f"prefix          = '{tag}_ep_initial'", f"prefix          = '{tag}_saddle'")
    lines = [head.rstrip("\n"), "", "ATOMIC_POSITIONS angstrom"]
    for i, (s, p) in enumerate(mid):
        # 뛰는 원자만 고정한다 (if_pos 0 0 0). 나머지는 자유 이완.
        fix = "  0 0 0" if i == j else ""
        lines.append(f"  {s:3s} %16.10f %16.10f %16.10f{fix}" % tuple(p))
    lines += ["", tail.rstrip("\n")]

    sd = os.path.join(d, "saddle")
    os.makedirs(sd, exist_ok=True)
    open(os.path.join(sd, "relax.in"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    json.dump({
        "tag": tag, "work": work,
        "method": ("대칭 홉 중점 구속 이완. 뛰는 원자를 두 끝점의 중점에 if_pos=0 0 0 으로 "
                   "고정하고 나머지를 이완한다. 프로토콜은 ep_initial/relax.in 헤더를 그대로 복사."),
        "moving_atom_index_0based": j, "moving_atom_symbol": mid[j][0],
        "hop_distance_A": round(dmax, 4),
        "second_largest_displacement_A": round(others, 4),
        "endpoints_symmetry_equivalent": sym,
        "symmetry_basis": basis,
        "symmetry_detail": sym_detail,
        "endpoints_converged": not unconv,
        "unconverged_endpoints": unconv,
        "endpoint_last_force_Ry_au": {"ep_initial": i1.get("last_total_force_Ry_au"),
                                      "ep_final": i2.get("last_total_force_Ry_au")},
        "endpoint_energy_diff_eV": (round(de, 6) if de is not None else None),
        "symmetry_warning": warn,
        "supercell": meta.get("supercell"), "min_cell_A": meta.get("min_cell_A"),
        "protocol_hash_of_endpoint": meta.get("protocol_hash"),
        "limitations": [
            "안장점을 찾지 않는다 — 대칭으로 결정된 중점을 쓴다",
            "대칭이 깨지면 틀린다. 이완 후 수직 힘을 확인할 것",
            "장벽 높이만 준다 (경로 형상 없음)",
        ],
    }, open(os.path.join(sd, "saddle_meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    return 0, (f"✓ {tag}: 안장 입력 생성 → {sd}/relax.in\n"
               f"   뛰는 원자 #{j} {mid[j][0]} · 홉 {dmax:.3f} Å "
               f"(다음으로 큰 변위 {others:.3f} Å)\n"
               + ((f"   ⛔ 끝점 미수렴: {' · '.join(unconv)} — "
                   f"마지막 힘 {i1.get('last_total_force_Ry_au')}/{i2.get('last_total_force_Ry_au')} Ry/au "
                   f"(문턱 1e-3). 장벽이 그만큼 오염된다\n") if unconv else "")
               + f"   대칭 근거: {basis}\n"
               + (f"   {warn}\n" if warn else "")
               + f"   셀 {meta.get('supercell')} · 최소변 {meta.get('min_cell_A')} Å\n"
               f"   실행:  cd {sd} && mpirun -np <N> pw.x -in relax.in > relax.out")


def collect(work, tag, radius=None, allow_unconverged=False):
    d = os.path.join(work, tag)
    if radius:
        base = os.path.join(d, f"frozen_R{radius:g}")
        ep = os.path.join(base, "endpoint", "relax.out")
        sd = os.path.join(base, "saddle", "relax.out")
    else:
        ep = os.path.join(endpoint_dir(d, "ep_initial"), "relax.out")
        sd = os.path.join(d, "saddle", "relax.out")
    for p in (ep, sd):
        if not os.path.isfile(p):
            return 1, f"⛔ 없음: {p}"
    # ⛔ 리뷰 F5 — 옛 판은 JOB DONE 도 수렴도 안 봤다. 아직 도는 중인 relax.out 에서
    #   깔끔한 Ea 가 나왔다(실측 재현). 에너지 줄이 있으면 무조건 읽었기 때문이다.
    bad = []
    for name, p in (("endpoint", ep), ("saddle", sd)):
        txt = open(p, encoding="utf-8", errors="replace").read()
        if "JOB DONE" not in txt:
            bad.append(f"{name}: 아직 안 끝났다 (JOB DONE 없음)")
            continue
        if "Begin final coordinates" not in txt:
            f = last_force(txt)
            bad.append(f"{name}: 이완 미수렴 (마지막 힘 {f} Ry/au"
                       + (f" = {f*25.711:.2f} eV/Å" if f else "") + ")")
    if bad and not allow_unconverged:
        return 1, ("⛔ 회수 거부 — 아래를 감수하려면 --allow_unconverged:\n   "
                   + "\n   ".join(bad))
    e_end, e_sad = final_energy(ep), final_energy(sd)
    if e_end is None or e_sad is None:
        return 1, "⛔ 총에너지를 못 읽었다"
    ea = e_sad - e_end
    # 구속 원자에 남은 힘 — 대칭이 지켜졌는지의 지표 (판정은 사람이)
    t = open(sd, encoding="utf-8", errors="replace").read()
    fm = re.findall(r"Total force =\s+([\d.eE+-]+)", t)
    meta = {}
    mp = (os.path.join(d, f"frozen_R{radius:g}", "frozen_meta.json") if radius
          else os.path.join(d, "saddle", "saddle_meta.json"))
    if os.path.isfile(mp):
        meta = json.load(open(mp, encoding="utf-8"))
    out = {
        "tag": tag, "root": os.path.basename(work.rstrip("/")),
        "Ea_eV": round(ea, 6), "E_endpoint_eV": round(e_end, 6), "E_saddle_eV": round(e_sad, 6),
        "total_force_last_Ry_au": float(fm[-1]) if fm else None,
        "method": ("frozen-shell symmetric-midpoint" if radius
                   else "symmetric-midpoint constrained relax (2 SCF relaxations, not NEB)"),
        "relax_radius_A": radius,
        "supercell": meta.get("supercell"), "min_cell_A": meta.get("min_cell_A"),
        "converged": not bad,
        "convergence_notes": bad,
        "caveat": ("대칭 홉 전제. 절대값 인용 전에 다른 셀에서 같은 방법으로 한 번 더 재고 "
                   "차이를 볼 것 — 이 도구의 용도가 그 비교다."),
    }
    return 0, ((f"⚠ {' · '.join(bad)}\n" if bad else "")
               + f"{tag} ({out['root']}, 셀 {out['supercell']}, 최소변 {out['min_cell_A']} Å)\n"
               f"  E_endpoint = {e_end:.6f} eV\n"
               f"  E_saddle   = {e_sad:.6f} eV\n"
               f"  ── Ea      = {ea:.4f} eV ──\n"
               f"  마지막 Total force = {out['total_force_last_Ry_au']} (Ry/au) "
               f"— 구속점이 대칭점이면 작아야 한다\n"
               f"  JSON: {json.dumps(out, ensure_ascii=False)}")


def build_frozen(work, tag, radius, force=False):
    """고정셸 방식: 원거리 원자를 묶고 공공 주변만 이완한다.

    왜 (2026-08-16)
      3×3×3 은 107원자 = **자유도 321** 이라 nstep 50 으로 못 끝났다(16h41m, 잔여 힘
      0.018 Ry/au = 문턱의 18배). 전이완을 끝내려면 GPU 8~12일이다.
      그런데 우리가 재려는 건 **이미지 상호작용의 셀 의존성**이고, 공공에서 먼 원자는
      두 셀 모두 이상 격자 위치에 있어 사실상 같다. 그 원자를 고정하면 자유도가
      크게 줄어 BFGS 가 빨리 끝난다.

    ⛔ 반드시 지킬 것
      · 끝점과 안장에 **같은 중심·같은 반경·같은 자유 원자 집합**을 쓴다.
        (다르면 E 차에 프로토콜 차이가 섞인다)
      · 2×2×2 대조군도 **같은 규약**으로 다시 잰다. 전이완 0.229 와 직접 비교하지 않는다.
      · 반경이 셀 수직 폭의 절반을 넘으면 자유영역이 자기 이미지와 닿아 의미가 없다 — 거부한다.

    산출: <tag>/frozen_R<r>/{endpoint,saddle}/relax.in  (+ frozen_meta.json)
    """
    d = os.path.join(work, tag)
    ini_in = os.path.join(endpoint_dir(d, "ep_initial"), "relax.in")
    fin_in = os.path.join(endpoint_dir(d, "ep_final"), "relax.in")
    for f in (ini_in, fin_in):
        if not os.path.isfile(f):
            return 1, f"⛔ 없음: {f} — build_neb_inputs.py 로 끝점 입력부터 만들 것"

    # ⛔ 리뷰 F1 — build 와 **같은** 대칭 게이트를 탄다 (중점=안장 전제가 동일하므로)
    meta_p = os.path.join(d, "meta.json")
    meta = json.load(open(meta_p, encoding="utf-8")) if os.path.isfile(meta_p) else {}
    basis, warn, de, sym, sym_detail = _symmetry_gate(
        meta, os.path.join(endpoint_dir(d, "ep_initial"), "relax.out"),
        os.path.join(endpoint_dir(d, "ep_final"), "relax.out"))
    if basis is None and not force:
        return 1, _symmetry_refusal(tag, sym, de, sym_detail)
    if basis is None:
        basis = "⛔ --force (대칭 근거 없음)"

    first = parse_input_positions(ini_in)
    last = parse_input_positions(fin_in)
    if not first or not last or len(first) != len(last):
        return 1, "⛔ relax.in 의 ATOMIC_POSITIONS 를 못 읽었다 (또는 원자 수가 다르다)"
    if [s for s, _ in first] != [s for s, _ in last]:
        return 1, "⛔ 두 끝점의 원자 목록이 다르다"

    cell = parse_cell(ini_in)
    if cell is None:
        return 1, "⛔ CELL_PARAMETERS 를 못 읽었다"
    import math
    V = abs(_det3(cell))
    widths = [V / _norm(_cross(cell[(i + 1) % 3], cell[(i + 2) % 3])) for i in range(3)]
    # ⛔⛔ 2026-08-16 (Codex 리뷰 P0) — 가드 기준은 면 높이가 아니라 **λ₁(최단 격자 병진)** 이다.
    #   자유영역(반경 R 구)이 자기 이미지와 겹치지 않으려면 2R ≤ λ₁ 이어야 한다.
    #   면 높이로 재면 fcc 에서 1.22배 보수적이라 쓸 수 있는 반경을 부당하게 깎는다.
    lam1 = _shortest_translation(cell)
    if radius > lam1 / 2.0 and not force:
        return 1, (f"⛔ 반경 {radius} Å 이 λ₁/2 ({lam1/2:.2f} Å)를 넘는다 — "
                   f"자유영역이 자기 이미지와 겹친다.\n"
                   f"   λ₁ {lam1:.2f} Å · 면높이 {[round(x,2) for x in widths]} Å (보수적 하한)\n"
                   f"   권장 설계: 셀 간 비교는 R=3.5·4.0 · 반경 수렴 스캔은 3.5/4/5/6 Å\n"
                   f"   --force 로 강행 가능")

    disp = [min_image([b[k] - a[k] for k in range(3)], cell)
            for (_, a), (_, b) in zip(first, last)]
    dn = [math.sqrt(sum(x * x for x in v)) for v in disp]
    j = max(range(len(dn)), key=lambda i: dn[i])
    dmax = dn[j]
    others = sorted(dn)[-2] if len(dn) > 1 else 0.0
    if dmax < 0.5:
        return 1, f"⛔ 두 끝점이 같은 구조다 (최대 변위 {dmax:.3f} Å)"
    if others > 0.3 * dmax and not force:
        return 1, (f"⛔ 뛰는 원자 외에도 크게 움직인다 (2위 변위 {others:.3f} Å > 홉 {dmax:.3f} 의 30%) "
                   f"— 단일 홉 입력이 아니다. --force 로 강행 가능")

    # ── ② 중점이 안장점인가: 대칭 연산과 mask 불변성을 **기록**한다 ─────────────
    #  Codex 리뷰: "끝점이 대칭 동등" 만으로 직선 중점이 안장점이라는 보장은 없다.
    #  필요한 건 두 끝점을 **교환하는 실제 대칭 연산**이 존재하고, 그 연산이 중점과
    #  free/frozen mask 를 보존하는 것이다. 그래도 얻는 것은 "홉 방향 정류점" 까지이고,
    #  횡방향 안정성·off-axis 안장 부재는 별도 확인(구속 해제 raw force · ±δ)이 필요하다.
    #  여기서는 **가장 단순한 후보 연산 = 중점에 대한 반전** 을 검사한다:
    #    x → 2·ctr − x 가 (첫 끝점 집합) → (둘째 끝점 집합) 을 원자 종까지 맞춰 옮기나.
    # ── 중심 = 홉 중점 (끝점·안장 **공통**)
    ctr = [first[j][1][k] + disp[j][k] / 2.0 for k in range(3)]
    def _inversion_maps_endpoints(tolA=0.30):
        """중점 반전이 first → last 를 (종까지) 옮기는지. (성립여부, 최대 잔차)"""
        import math as _m
        used, worst = set(), 0.0
        for i, (s, q) in enumerate(first):
            img = [2 * ctr[k] - q[k] for k in range(3)]
            best, bj = 1e9, None
            for jj, (s2, r) in enumerate(last):
                if s2 != s or jj in used:
                    continue
                dd = min_image([r[k] - img[k] for k in range(3)], cell)
                nn = _m.sqrt(sum(x * x for x in dd))
                if nn < best:
                    best, bj = nn, jj
            if bj is None:
                return False, None
            used.add(bj)
            worst = max(worst, best)
        return worst <= tolA, worst

    inv_ok, inv_res = _inversion_maps_endpoints()

    freeze = []
    for i, (s, p) in enumerate(first):
        v = min_image([p[k] - ctr[k] for k in range(3)], cell)
        freeze.append(math.sqrt(sum(x * x for x in v)) > radius)
    freeze[j] = False                      # 뛰는 원자는 항상 자유(안장에선 좌표 고정)
    # mask 도 같은 연산에 대해 불변이어야 한다 — 아니면 끝점과 안장의 자유영역이
    # 대칭적으로 다르고, 그 비대칭이 그대로 Ea 에 들어간다.
    import math as _m
    mask_inv_ok = True
    for i, (s, q) in enumerate(first):
        img = [2 * ctr[k] - q[k] for k in range(3)]
        v = min_image([img[k] - ctr[k] for k in range(3)], cell)
        # 반전상의 중심거리는 원본과 같아야 하므로 freeze 판정도 같아야 한다
        if (_m.sqrt(sum(x * x for x in v)) > radius) != freeze[i]:
            mask_inv_ok = False
            break
    n_free = sum(1 for f in freeze if not f)
    if n_free < 8 and not force:
        return 1, (f"⛔ 자유 원자가 {n_free}개뿐이다 — 반경 {radius} Å 이 너무 작다. "
                   f"--relax_radius 를 키울 것")

    src = open(ini_in, encoding="utf-8").read()
    head = src[:src.index("ATOMIC_POSITIONS")]
    tail = src[src.index("K_POINTS"):]
    outd = os.path.join(d, f"frozen_R{radius:g}")

    mid = [(s, [first[i][1][k] + disp[i][k] / 2.0 for k in range(3)])
           for i, (s, _) in enumerate(first)]

    # ⛔⛔ 리뷰 F2 — 고정 원자는 **두 파일에서 같은 좌표**여야 한다.
    #   옛 판은 끝점에 first[i], 안장에 mid[i] 를 썼다. 변위가 0 이 아닌 원거리 원자는
    #   두 계산에서 서로 다른 위치에 못박히고, 이완으로 풀 수도 없으니 그 차이가
    #   **그대로 Ea 에 들어간다**. 실측 재현: 0.4 Å 강체 오프셋이 게이트를 통과했다.
    #   → 고정 원자는 양쪽 다 mid[i] 를 쓴다(= 두 끝점의 평균, 대칭점).
    frozen_shift = max((dn[i] for i in range(len(dn)) if freeze[i]), default=0.0)

    # ⛔⛔ 2026-08-27 실측 — 위 게이트는 **relax.in** 으로 잰다. 갓 지은 입력은 정의상
    #   홉 외 변위가 0.000 이라 게이트가 **거저 통과한다.** 실제로 ccpath(2×2×2)는
    #   0.000 으로 통과했는데, 같은 끝점의 **이완 좌표**로 재면 1.035 Å 였다.
    #   ⇒ 그대로 뒀으면 고정 원자가 1 Å 어긋난 채 못박혀 그 차이가 Ea 에 직접 들어갔다.
    #   (cc333 이 1.240 으로 막힌 것도 물리가 아니라 `_r2` 가 있어서 이완 좌표를 봤기 때문이다.)
    #   → 전제 검사는 **이완 좌표**로 한다. 정렬(병진·라벨)까지 뺀 뒤의 잔여로 잰다.
    relaxed_shift, relaxed_note = None, ""
    _r = {}
    for nm in ("ep_initial", "ep_final"):
        rows, _err, _inf = read_relaxed(os.path.join(endpoint_dir(d, nm), "relax.out"),
                                        allow_unconverged=True)
        if rows and len(rows) == len(first):
            _r[nm] = (rows, _inf)
    if len(_r) == 2:
        rep = align_report(_r["ep_initial"][0], _r["ep_final"][0], cell, far_r=radius)
        if "error" not in rep:
            relaxed_shift = rep["aligned_max_excl_hop_A"]
            unconv = [k for k, (_x, i) in _r.items() if i.get("converged") is False]
            relaxed_note = (f"   (이완 끝점 기준 · 병진 {rep['translation_norm_A']} Å·"
                            f"라벨 {rep['n_relabeled']}개 제거 후"
                            + (f" · ⚠ 미수렴: {', '.join(unconv)}" if unconv else "") + ")")
    gate_val = max(frozen_shift, relaxed_shift or 0.0)
    if gate_val > FROZEN_SHIFT_TOL_A and not force:
        _src = ("갓 지은 좌표" if frozen_shift >= (relaxed_shift or 0.0) else "이완 좌표")
        return 1, (f"⛔ 고정 대상 원자가 끝점 사이에서 {gate_val:.3f} Å 움직인다 "
                   f"(문턱 {FROZEN_SHIFT_TOL_A} Å, {_src} 기준) — 국소 홉이 아니거나 반경이 너무 작다.\n"
                   f"   갓 지은 좌표 {frozen_shift:.3f} · 이완 좌표 "
                   f"{'—' if relaxed_shift is None else f'{relaxed_shift:.3f}'} Å\n"
                   + (relaxed_note + "\n" if relaxed_note else "")
                   + f"   고정 원자를 한 좌표에 못박으면 그 차이가 Ea 에 직접 들어간다. "
                   f"--relax_radius 를 키울 것 (--force 로 강행 가능)")
    if relaxed_shift is None and not force:
        return 1, ("⛔ 끝점 **이완 좌표가 없어** 전제(뛰는 원자 외에는 가만있다)를 검사할 수 없다.\n"
                   "   갓 지은 좌표의 홉 외 변위는 정의상 0 이라 게이트가 거저 통과한다 "
                   "(2026-08-27 실측: 통과한 ccpath 의 실제 값은 1.035 Å 였다).\n"
                   "   끝점 relax 를 먼저 끝낼 것 (--force 로 강행 가능 — 권장 안 함)")

    def emit(sub, rows, fix_moving):
        os.makedirs(os.path.join(outd, sub), exist_ok=True)
        h = head.replace(f"prefix          = '{tag}_ep_initial'",
                         f"prefix          = '{tag}_frozen_{sub}'")
        L = [h.rstrip("\n"), "", "ATOMIC_POSITIONS angstrom"]
        for i, (s, p) in enumerate(rows):
            frz = freeze[i]
            # 고정 원자는 **양쪽 동일 좌표**(mid) · 자유 원자는 각 상태의 좌표
            pos = mid[i][1] if frz else p
            fx = "  0 0 0" if (frz or (fix_moving and i == j)) else ""
            L.append(f"  {s:3s} %16.10f %16.10f %16.10f{fx}" % tuple(pos))
        L += ["", tail.rstrip("\n")]
        open(os.path.join(outd, sub, "relax.in"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    emit("endpoint", first, fix_moving=False)
    emit("saddle", mid, fix_moving=True)

    # ⛔⛔ 2026-08-16 (Codex 리뷰) — `if_pos 0 0 0` 은 QE 가 그 원자의 **힘 성분을
    #   마스킹**한다(INPUT_PW). 그래서 relax.out 의 전역 `Total force` 로는 구속된 Li 의
    #   잔여 힘을 **검증할 수 없다** — 0 으로 찍히는 게 당연하고, 그걸 "안장점이다" 의
    #   근거로 쓰면 순환이다. 구속을 **푼** 단일점을 따로 만들어 raw force 를 받는다.
    #   (안장 relax 가 끝난 뒤 그 좌표로 이 입력을 채워 돌린다 — --emit_check 참조)
    chk = os.path.join(outd, "saddle_rawforce")
    os.makedirs(chk, exist_ok=True)
    hchk = (head.replace(f"prefix          = '{tag}_ep_initial'",
                         f"prefix          = '{tag}_frozen_rawforce'")
                .replace("calculation     = 'relax'", "calculation     = 'scf'"))
    open(os.path.join(chk, "README.txt"), "w", encoding="utf-8").write(
        "안장 relax 가 끝난 뒤 그 좌표로 이 scf 를 돌려 **구속 없는** 힘을 본다.\n"
        "  python3 tools/sei/symmetric_saddle.py --work <W> --tag <T> \\\n"
        f"    --relax_radius {radius:g} --emit_check\n"
        "왜: if_pos 0 0 0 은 힘 성분을 마스킹하므로 relax.out 의 Total force 로는\n"
        "    구속된 원자의 잔여 힘을 검증할 수 없다 (QE INPUT_PW).\n"
        "판정: 이동 원자에 남은 힘의 **홉 방향 성분**이 작아야 안장점이다.\n"
        "      횡방향 성분이 크면 off-axis 안장이거나 대칭이 깨진 것이다.\n")
    open(os.path.join(chk, "header.in"), "w", encoding="utf-8").write(hchk)

    meta = {
        "tag": tag, "work": work, "method": "frozen-shell symmetric-midpoint",
        "relax_radius_A": radius, "freeze_center_xyz": [round(x, 6) for x in ctr],
        "n_atoms": len(first), "n_free": n_free, "n_frozen": len(first) - n_free,
        "dof_free": 3 * n_free, "dof_total": 3 * len(first),
        "moving_atom_index_0based": j, "moving_atom_symbol": first[j][0],
        "hop_distance_A": round(dmax, 4), "second_largest_displacement_A": round(others, 4),
        "_cell": [[round(x, 8) for x in v] for v in cell],
        "_hop_vector": [round(x, 8) for x in disp[j]],
        "lambda1_A": round(lam1, 3),
        "max_radius_A": round(lam1 / 2.0, 3),
        "cell_face_heights_A": [round(x, 3) for x in widths],
        "recommended_design": {
            "cross_cell_comparison": [3.5, 4.0],
            "radius_convergence_scan": [3.5, 4.0, 5.0, 6.0],
            "converged_when": "반경 2회 연속 · 셀 2단계에서 |ΔEa| ≤ 0.02–0.03 eV",
            "note": "5/7 Å 는 2×2×2 의 λ₁/2 = 5.19 Å 를 넘어 부적합했다",
        },
        "min_face_height_A": round(min(widths), 3),
        "cell_vector_lengths_A": [round(_norm(v), 3) for v in cell],
        "supercell": meta.get("supercell"),
        "min_cell_A": meta.get("min_cell_A"),
        "symmetry_basis": basis,
        "symmetry_detail": sym_detail,
        "symmetry_warning": warn,
        "endpoint_energy_diff_eV": (round(de, 6) if de is not None else None),
        "max_frozen_atom_shift_A": round(frozen_shift, 4),
        "started_from": "relax.in (ideal) — relax.out 의 표류 구조를 승계하지 않는다",
        "midpoint_saddle_evidence": {
            "inversion_maps_endpoints": inv_ok,
            "inversion_max_residual_A": (round(inv_res, 4) if inv_res is not None else None),
            "freeze_mask_inversion_invariant": mask_inv_ok,
            "what_this_gives": ("중점이 홉 방향 **정류점**이라는 데까지. 횡방향 안정성과 "
                                "off-axis 안장 부재는 보장하지 않는다."),
            "still_required": [
                "안장 relax 뒤 구속을 **푼** single-point 의 raw force (if_pos 가 힘을 마스킹한다)",
                "중점에서 홉 방향 ±δ 로 에너지가 양쪽 다 내려가는지",
                "대표 셀·반경 1건에 3–5 image CI-NEB 또는 dimer 교차검증",
            ],
        },
        "contract": ("끝점과 안장이 **같은 중심·반경·자유집합**을 쓴다. "
                     "다른 셀과 비교하려면 그 셀도 같은 radius 로 이 도구를 돌릴 것. "
                     "전이완 값(예: 2×2×2 의 0.229)과 직접 비교하지 말 것 — 프로토콜이 다르다."),
        "limitations": ["원거리 이완을 버린다 — 절대 장벽은 전이완보다 약간 높게 나온다",
                        "그 편향은 두 셀에서 같은 방향이라 **차이**에는 대부분 상쇄된다",
                        "대칭 홉 전제 (안장 = 중점)"],
    }
    json.dump(meta, open(os.path.join(outd, "frozen_meta.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    return 0, (f"✓ {tag}: 고정셸 입력 생성 → {outd}/\n"
               f"   반경 {radius} Å · 자유 {n_free}/{len(first)}원자 "
               f"(자유도 {3*n_free} / {3*len(first)}, {100*n_free/len(first):.0f}%)\n"
               f"   중심 = 홉 중점 · 홉 {dmax:.3f} Å (2위 변위 {others:.3f}) · "
               f"고정원자 최대 이동 {frozen_shift:.3f} Å\n"
               f"   λ₁ {lam1:.2f} Å (반경 상한 {lam1/2:.2f}) · 면높이 {[round(x,1) for x in widths]} Å · "
               f"슈퍼셀 {meta.get('supercell')} · 대칭근거 {basis}\n"
               f"   ⚠ 끝점·안장이 같은 자유집합을 쓴다. **다른 셀도 같은 radius 로** 돌릴 것.\n"
               f"   실행 (순서대로, 같은 노드):\n"
               f"     cd {outd}/endpoint && mpirun -np <N> pw.x -in relax.in > relax.out\n"
               f"     cd {outd}/saddle   && mpirun -np <N> pw.x -in relax.in > relax.out\n"
               f"   회수:  python3 tools/sei/symmetric_saddle.py --work {work} --tag {tag} "
               f"--collect --relax_radius {radius:g}")


def _shortest_translation(cell, R=3):
    """최단 비영 격자 병진 λ₁ — 점결함 이미지 거리의 정본 지표.
    (면 높이는 격자 평면 간 거리라 슬랩용이고 basis 의존. fcc 에서 1.22배 차이)"""
    import itertools
    best = float("inf")
    for n in itertools.product(range(-R, R + 1), repeat=3):
        if n == (0, 0, 0):
            continue
        v = [sum(n[k] * cell[k][c] for k in range(3)) for c in range(3)]
        best = min(best, _norm(v))
    return best


def _cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]


def _norm(v):
    return sum(x*x for x in v) ** 0.5


def _det3(m):
    return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
            - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
            + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))


def verify_saddle(work, tag, radius):
    """②③ **판정** — 안장인지 아닌지를 숫자로 닫는다.

    닫힘 조건 (셋 다 만족해야 `saddle_verified: true`)
      ③-1  구속 해제 raw force 의 **홉 방향** 성분 |F·u| ≤ 1e-3 Ry/au   → 정류점
      ③-2  같은 힘의 **횡방향** 성분도 같은 문턱 이하                   → off-axis 아님
      ②    E(+δ) < E(saddle) **그리고** E(−δ) < E(saddle)              → 최댓점(안장)

    하나라도 어긋나면 `saddle_verified: false` 와 어긋난 항목을 돌려준다.
    ⚠ 이걸 통과해도 남는 것: 대표 1건에 3–5 image CI-NEB 또는 dimer 교차검증.
      이 검사는 **중점이 안장이다** 를 확인하지, 그 경로가 최소에너지 경로임을 보장하지 않는다.
    """
    outd = os.path.join(work, tag, f"frozen_R{radius:g}")
    fmp = os.path.join(outd, "frozen_meta.json")
    if not os.path.isfile(fmp):
        return None, f"⛔ 없음: {fmp}"
    fm = json.load(open(fmp, encoding="utf-8"))
    j = fm["moving_atom_index_0based"]
    hop = fm.get("_hop_vector")
    if not hop:
        return None, "⛔ frozen_meta 에 홉 벡터가 없다"
    n = _norm(hop)
    u = [x / n for x in hop]

    need = {"rawforce": "scf.out", "probe_plus": "scf.out", "probe_minus": "scf.out",
            "saddle": "relax.out"}
    miss = [f"{k}/{v}" for k, v in need.items()
            if not os.path.isfile(os.path.join(outd, k, v))]
    if miss:
        return None, ("⛔ 아직 안 돈 것: " + ", ".join(miss)
                      + f"\n   먼저: --emit_check 로 입력을 만들고 각각 pw.x 를 돌릴 것")

    F = atom_forces(os.path.join(outd, "rawforce", "scf.out"))
    if not F or len(F) <= j:
        return None, "⛔ rawforce/scf.out 에서 원자별 힘을 못 읽었다"
    f = F[j]
    f_along = sum(f[k] * u[k] for k in range(3))
    f_perp = _norm([f[k] - f_along * u[k] for k in range(3)])

    e_s = final_energy(os.path.join(outd, "saddle", "relax.out"))
    e_p = final_energy(os.path.join(outd, "probe_plus", "scf.out"))
    e_m = final_energy(os.path.join(outd, "probe_minus", "scf.out"))

    fails = []
    if abs(f_along) > SADDLE_FORCE_TOL_RY_AU:
        fails.append(f"③-1 홉 방향 잔여 힘 {abs(f_along):.2e} > {SADDLE_FORCE_TOL_RY_AU:.0e} Ry/au "
                     f"— 정류점이 아니다")
    if f_perp > SADDLE_FORCE_TOL_RY_AU:
        fails.append(f"③-2 횡방향 힘 {f_perp:.2e} > {SADDLE_FORCE_TOL_RY_AU:.0e} Ry/au "
                     f"— off-axis 안장이거나 대칭이 깨졌다")
    if None in (e_s, e_p, e_m):
        fails.append("② 탐침 에너지를 못 읽었다")
    else:
        if e_p >= e_s:
            fails.append(f"② E(+δ) {e_p:.6f} ≥ E(saddle) {e_s:.6f} — 그 방향으로 올라간다")
        if e_m >= e_s:
            fails.append(f"② E(−δ) {e_m:.6f} ≥ E(saddle) {e_s:.6f} — 그 방향으로 올라간다")

    out = {
        "saddle_verified": not fails,
        "raw_force_along_hop_Ry_au": round(f_along, 8),
        "raw_force_perp_Ry_au": round(f_perp, 8),
        "force_tol_Ry_au": SADDLE_FORCE_TOL_RY_AU,
        "probe_delta_A": PROBE_DELTA_A,
        "E_saddle_eV": (round(e_s, 6) if e_s is not None else None),
        "E_plus_eV": (round(e_p, 6) if e_p is not None else None),
        "E_minus_eV": (round(e_m, 6) if e_m is not None else None),
        "dE_plus_meV": (round((e_p - e_s) * 1000, 2) if None not in (e_p, e_s) else None),
        "dE_minus_meV": (round((e_m - e_s) * 1000, 2) if None not in (e_m, e_s) else None),
        "failures": fails,
        "still_required_after_this": (
            "대표 (셀, 반경) 1건에 3–5 image CI-NEB 또는 dimer 교차검증. "
            "이 검사는 중점이 안장임을 확인하지, 그 경로가 최소에너지 경로임을 보장하지 않는다."),
        "note_if_pos": ("raw force 는 **구속을 뺀** scf 에서 읽었다. relax.out 의 Total force 는 "
                        "if_pos 가 성분을 마스킹해 이 검증에 쓸 수 없다 (QE INPUT_PW)."),
    }
    json.dump(out, open(os.path.join(outd, "saddle_verification.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    return out, None


def emit_check(work, tag, radius):
    """② ③ 을 **닫는** 입력 3개를 만든다 (안장 relax 가 끝난 뒤 실행).

    왜 이게 필요한가
      ③ `if_pos 0 0 0` 은 QE 가 그 원자의 힘 성분을 **마스킹**한다(INPUT_PW). 그래서
         안장 relax 의 `Total force` 로는 구속된 원자의 잔여 힘을 검증할 수 없다 —
         0 으로 찍히는 게 당연하고, 그걸 근거로 쓰면 순환이다.
      ② "끝점이 대칭 동등" 은 중점이 **홉 방향 정류점**이라는 데까지만 준다.
         정말 안장이려면 그 방향으로 **양쪽 다 에너지가 내려가야** 한다.

    만드는 것 (전부 scf 단일점 — relax 아님)
      rawforce/  안장 좌표 · **구속 전부 해제** → 이동 원자의 raw force
      probe_plus/ · probe_minus/  안장에서 홉 방향 ±δ → 에너지가 양쪽 다 낮아야 안장

    판정은 --collect 가 한다. 이 함수는 입력만 만든다.
    """
    d = os.path.join(work, tag)
    outd = os.path.join(d, f"frozen_R{radius:g}")
    fmp = os.path.join(outd, "frozen_meta.json")
    sad = os.path.join(outd, "saddle", "relax.out")
    if not os.path.isfile(fmp):
        return 1, f"⛔ 없음: {fmp} — 먼저 --relax_radius {radius:g} 로 입력을 만들 것"
    if not os.path.isfile(sad):
        return 1, f"⛔ 없음: {sad} — 안장 relax 를 먼저 돌릴 것"
    fm = json.load(open(fmp, encoding="utf-8"))
    rows, err, info = read_relaxed(sad)
    if rows is None:
        return 1, f"⛔ 안장 좌표를 못 읽었다: {err}"

    j = fm["moving_atom_index_0based"]
    cell = fm.get("_cell")
    hop = fm.get("_hop_vector")
    if not hop:
        return 1, "⛔ frozen_meta 에 홉 벡터가 없다 — 입력을 다시 만들 것"
    n = _norm(hop)
    u = [x / n for x in hop]                      # 홉 방향 단위벡터

    src = open(os.path.join(outd, "saddle", "relax.in"), encoding="utf-8").read()
    head = src[:src.index("ATOMIC_POSITIONS")]
    tail = src[src.index("K_POINTS"):]

    def emit_scf(sub, rows2, note):
        os.makedirs(os.path.join(outd, sub), exist_ok=True)
        h = (head.replace("calculation     = 'relax'", "calculation     = 'scf'")
                 .replace(f"prefix          = '{tag}_frozen_saddle'",
                          f"prefix          = '{tag}_chk_{sub}'"))
        L = [h.rstrip("\n"), "", "ATOMIC_POSITIONS angstrom"]
        # ⛔ 구속을 **전부 뺀다** — if_pos 가 없어야 raw force 가 나온다
        for s, q in rows2:
            L.append(f"  {s:3s} %16.10f %16.10f %16.10f" % tuple(q))
        L += ["", tail.rstrip("\n")]
        open(os.path.join(outd, sub, "scf.in"), "w", encoding="utf-8").write("\n".join(L) + "\n")
        open(os.path.join(outd, sub, "WHY.txt"), "w", encoding="utf-8").write(note + "\n")

    emit_scf("rawforce", rows,
             "안장 좌표 그대로, 구속 전부 해제. 이동 원자의 raw force 를 본다.\n"
             f"판정: 홉 방향 성분 |F·u| ≤ {SADDLE_FORCE_TOL_RY_AU} Ry/au 여야 정류점이다.\n"
             "      횡방향 성분이 크면 off-axis 안장이거나 대칭이 깨졌다.")
    for sgn, sub in ((+1, "probe_plus"), (-1, "probe_minus")):
        r2 = [(s, list(q)) for s, q in rows]
        r2[j] = (r2[j][0], [r2[j][1][k] + sgn * PROBE_DELTA_A * u[k] for k in range(3)])
        emit_scf(sub, r2,
                 f"안장에서 이동 원자를 홉 방향 {sgn:+d}·{PROBE_DELTA_A} Å 옮긴 단일점.\n"
                 "판정: 안장이면 E(±δ) 가 **둘 다** E(saddle) 보다 낮아야 한다.\n"
                 "      한쪽만 낮으면 안장이 아니라 경사면 위 점이다.")

    return 0, (f"✓ {tag}: ②③ 검증 입력 3개 생성 → {outd}/\n"
               f"   rawforce · probe_plus · probe_minus  (전부 scf 단일점, 구속 없음)\n"
               f"   홉 방향 u = [{u[0]:.4f}, {u[1]:.4f}, {u[2]:.4f}] · δ = {PROBE_DELTA_A} Å\n"
               f"   실행:\n"
               + "".join(f"     cd {outd}/{s} && mpirun -np <N> pw.x -in scf.in > scf.out\n"
                         for s in ("rawforce", "probe_plus", "probe_minus"))
               + f"   판정:  python3 tools/sei/symmetric_saddle.py --work {work} --tag {tag} "
                 f"--relax_radius {radius:g} --collect")


def selftest():
    import shutil
    import tempfile
    td = tempfile.mkdtemp(prefix="symsaddle_st_")
    ok = True

    def chk(c, m):
        nonlocal ok
        ok &= bool(c)
        _p(f"  {_OK if c else _NG} {m}")

    def mk(tag, sym, ini, fin, cell=None):
        d = os.path.join(td, tag)
        for n in ("ep_initial", "ep_final"):
            os.makedirs(os.path.join(d, n), exist_ok=True)
        json.dump({"endpoints_symmetry_equivalent": sym, "supercell": [3, 3, 3],
                   "min_cell_A": 15.56, "protocol_hash": "deadbeef"},
                  open(os.path.join(d, "meta.json"), "w", encoding="utf-8"))
        c = cell or [[15.0, 0, 0], [0, 15.0, 0], [0, 0, 15.0]]
        hdr = ("&CONTROL\n    calculation     = 'relax'\n"
               f"    prefix          = '{tag}_ep_initial'\n/\n"
               "&SYSTEM\n    ibrav           = 0\n    tot_charge      = 0.0\n/\n\n"
               "ATOMIC_SPECIES\n  Li 6.94 li.UPF\n\n")
        for n, rows in (("ep_initial", ini), ("ep_final", fin)):
            p = os.path.join(d, n)
            body = "ATOMIC_POSITIONS angstrom\n" + "".join(
                f"  {s:3s} {x:16.10f} {y:16.10f} {z:16.10f}\n" for s, (x, y, z) in rows)
            k = "K_POINTS automatic\n  2 2 2 0 0 0\n\nCELL_PARAMETERS angstrom\n" + \
                "".join("  %16.10f %16.10f %16.10f\n" % tuple(v) for v in c)
            open(os.path.join(p, "relax.in"), "w", encoding="utf-8").write(hdr + body + "\n" + k)
            open(os.path.join(p, "relax.out"), "w", encoding="utf-8").write(
                "Begin final coordinates\n" + body + "End final coordinates\n"
                "!    total energy              =    -100.0000 Ry\nJOB DONE.\n")
        return d

    A = [("Li", (0.0, 0.0, 0.0)), ("Li", (5.0, 0.0, 0.0)), ("Li", (0.0, 5.0, 0.0))]
    B = [("Li", (3.667, 0.0, 0.0)), ("Li", (5.0, 0.0, 0.0)), ("Li", (0.0, 5.0, 0.0))]

    # 양성 — 대칭 홉
    mk("good", True, A, B)
    rc, msg = build(td, "good")
    chk(rc == 0, "대칭 홉이면 안장 입력을 만든다")
    sp = os.path.join(td, "good", "saddle", "relax.in")
    chk(os.path.isfile(sp), "saddle/relax.in 이 생긴다")
    txt = open(sp, encoding="utf-8").read()
    chk(txt.count("  0 0 0") == 1, "[핵심] 구속(if_pos)이 **정확히 한 원자**에만 붙는다")
    chk("1.8335000000" in txt.replace(" ", " "), "뛰는 원자가 중점(3.667/2=1.8335)에 놓인다")
    chk("CELL_PARAMETERS" in txt and "K_POINTS" in txt, "셀·k 가 끝점 입력에서 승계된다")
    chk("'good_saddle'" in txt, "prefix 가 안장용으로 바뀐다")
    m = json.load(open(os.path.join(td, "good", "saddle", "saddle_meta.json"), encoding="utf-8"))
    chk(m["moving_atom_index_0based"] == 0 and abs(m["hop_distance_A"] - 3.667) < 1e-6,
        "뛰는 원자와 홉 거리를 맞게 기록한다")

    # ── 음성 ──
    mk("asym", False, A, B)
    # 두 끝점 에너지를 크게 벌린다 → (b) 경로도 막혀야 한다
    fp = os.path.join(td, "asym", "ep_final", "relax.out")
    # ⚠ open(fp,"w").write(open(fp, encoding="utf-8").read()) 은 **쓰기가 먼저 평가돼 파일을 자른 뒤** 읽는다.
    _s = open(fp, encoding="utf-8").read()
    open(fp, "w", encoding="utf-8").write(_s.replace("-100.0000 Ry", "-99.0000 Ry"))
    rc, msg = build(td, "asym")
    chk(rc == 1 and "대칭 근거가 없다" in msg, "[음성] 비대칭 + 에너지 불일치를 거부한다")
    chk("meV" in msg, "[음성] 거부 사유에 실측 |ΔE| 를 적는다")
    rc, _ = build(td, "asym", force=True)
    chk(rc == 0, "[음성] --force 로만 강행된다")
    mm = json.load(open(os.path.join(td, "asym", "saddle", "saddle_meta.json"), encoding="utf-8"))
    chk("--force" in str(mm.get("symmetry_basis")), "[음성] --force 로 통과하면 그렇게 기록한다")

    # ★ meta 없이 **끝점 에너지 축퇴**로만 통과 (cc333 의 실제 상황)
    d0 = mk("nometa", None, A, B)
    os.remove(os.path.join(d0, "meta.json"))
    rc, msg = build(td, "nometa")
    chk(rc == 0 and "measured endpoint degeneracy" in msg,
        "[핵심] meta 없어도 끝점 에너지 축퇴로 통과한다 (cc333 상황)")
    chk("필요조건이지" in msg, "[핵심] 그때 충분조건이 아니라는 경고를 띄운다")
    mm = json.load(open(os.path.join(td, "nometa", "saddle", "saddle_meta.json"), encoding="utf-8"))
    chk(mm.get("endpoint_energy_diff_eV") == 0.0 and mm.get("symmetry_warning"),
        "[핵심] 근거·ΔE·경고를 meta 에 남긴다")

    mk("same", True, A, A)
    rc, msg = build(td, "same")
    chk(rc == 1 and "같은 구조" in msg, "[음성] 끝점이 같으면 거부한다 (뛰는 원자 없음)")

    d = mk("noout", True, A, B)
    os.remove(os.path.join(d, "ep_final", "relax.out"))
    rc, msg = build(td, "noout")
    chk(rc == 1 and "이완된 끝점이 필요하다" in msg, "[음성] 끝점 미이완이면 거부한다")

    # ★ cc333 실제 상황: JOB DONE 인데 final coordinates 없음 (nstep 한도)
    d0 = mk("unconv", True, A, B)
    for n in ("ep_initial", "ep_final"):
        fp = os.path.join(d0, n, "relax.out")
        s0 = open(fp, encoding="utf-8").read()
        body = s0[s0.index("ATOMIC_POSITIONS"):s0.index("End final coordinates")]
        open(fp, "w", encoding="utf-8").write(
            "     The maximum number of steps has been reached.\n"
            "     End of BFGS Geometry Optimization\n" + body +
            "     Total force =     0.018069     Total SCF correction =     0.000028\n"
            "!    total energy              =    -100.0000 Ry\nJOB DONE.\n")
    rc, msg = build(td, "unconv")
    chk(rc == 1 and "수렴하지 않았다" in msg, "[핵심] 미수렴 끝점을 기본값으로 거부한다")
    chk("0.46 eV/Å" in msg or "eV/Å" in msg, "[핵심] 잔여 힘을 eV/Å 로도 알려준다")
    rc, msg = build(td, "unconv", allow_unconverged=True)
    chk(rc == 0 and "끝점 미수렴" in msg, "[핵심] --allow_unconverged 면 진행하되 경고한다")
    mm = json.load(open(os.path.join(td, "unconv", "saddle", "saddle_meta.json"), encoding="utf-8"))
    chk(mm.get("endpoints_converged") is False and mm.get("unconverged_endpoints"),
        "[핵심] 미수렴 사실이 saddle_meta 에 박힌다")
    chk(abs(mm["endpoint_last_force_Ry_au"]["ep_initial"] - 0.018069) < 1e-9,
        "[핵심] 잔여 힘 값을 기록한다")

    d = mk("notdone", True, A, B)
    p = os.path.join(d, "ep_final", "relax.out")
    _s = open(p, encoding="utf-8").read()                      # ⚠ 같은 truncate-before-read 함정
    open(p, "w", encoding="utf-8").write(_s.replace("JOB DONE.", ""))
    rc, msg = build(td, "notdone")
    chk(rc == 1, "[음성] JOB DONE 없는 relax.out 을 안 받는다")

    # 최소이미지: 홉이 셀 경계를 넘어도 3.667 로 펴져야 한다
    small = [[7.0, 0, 0], [0, 7.0, 0], [0, 0, 7.0]]
    C = [("Li", (6.5, 0.0, 0.0)), ("Li", (2.0, 0.0, 0.0)), ("Li", (0.0, 2.0, 0.0))]
    D = [("Li", (0.5, 0.0, 0.0)), ("Li", (2.0, 0.0, 0.0)), ("Li", (0.0, 2.0, 0.0))]
    mk("pbc", True, C, D, cell=small)
    rc, _ = build(td, "pbc")
    mm = json.load(open(os.path.join(td, "pbc", "saddle", "saddle_meta.json"), encoding="utf-8"))
    chk(rc == 0 and abs(mm["hop_distance_A"] - 1.0) < 1e-6,
        f"[PBC] 경계를 넘는 홉을 최소이미지로 편다 (6.5→0.5 는 1.0 Å, got {mm['hop_distance_A']})")

    # collect
    sd = os.path.join(td, "good", "saddle")
    # ⚠ F5 가드가 생겨서 fixture 도 **끝난 relax** 여야 한다 (JOB DONE + final coordinates).
    #   옛 fixture 는 둘 다 없었는데 통과했다 — 그게 F5 가 잡은 결함이다.
    open(os.path.join(sd, "relax.out"), "w", encoding="utf-8").write(
        "Begin final coordinates\nATOMIC_POSITIONS angstrom\n"
        "  Li  0.0 0.0 0.0\nEnd final coordinates\n"
        "     Total force =     0.000123\n"
        "!    total energy              =    -99.9832 Ry\nJOB DONE.\n")
    rc, msg = collect(td, "good")
    chk(rc == 0 and "Ea" in msg, "collect 가 Ea 를 낸다")
    ea = json.loads(msg.split("JSON: ")[1])["Ea_eV"]
    chk(abs(ea - (0.0168 * 13.605693122994)) < 1e-3, f"Ea 가 ΔE 와 맞는다 ({ea:.4f} eV)")

    # ══ 고정셸 경로 (리뷰 F3 — 이 170줄이 selftest 에 하나도 없었다) ══════════
    import math as _m
    CELL = [[14.0, 0, 0], [0, 14.0, 0], [0, 0, 14.0]]

    def mkf(tag, sym, ini, fin, cell=CELL, e_fin="-100.0000", out_rows=None, conv=True):
        d = os.path.join(td, tag)
        for n in ("ep_initial", "ep_final"):
            os.makedirs(os.path.join(d, n), exist_ok=True)
        json.dump({"endpoints_symmetry_equivalent": sym, "supercell": [3, 3, 3],
                   "min_cell_A": 15.56}, open(os.path.join(d, "meta.json"), "w", encoding="utf-8"))
        hdr = ("&CONTROL\n    calculation     = 'relax'\n"
               f"    prefix          = '{tag}_ep_initial'\n/\n"
               "&SYSTEM\n    ibrav           = 0\n/\n\nATOMIC_SPECIES\n  Li 6.94 li.UPF\n\n")
        k = ("K_POINTS automatic\n  2 2 2 0 0 0\n\nCELL_PARAMETERS angstrom\n"
             + "".join("  %16.10f %16.10f %16.10f\n" % tuple(v) for v in cell))
        def _body(rows):
            return "ATOMIC_POSITIONS angstrom\n" + "".join(
                f"  {s:3s} {x:16.10f} {y:16.10f} {z:16.10f}\n" for s, (x, y, z) in rows)
        for idx, (n, rows, en) in enumerate((("ep_initial", ini, "-100.0000"),
                                             ("ep_final", fin, e_fin))):
            open(os.path.join(d, n, "relax.in"), "w", encoding="utf-8").write(
                hdr + _body(rows) + "\n" + k)
            # 이완 좌표는 입력과 **다를 수 있다** — out_rows 로 그 차이를 만든다
            ob = _body(out_rows[idx] if out_rows else rows)
            tail = f"!    total energy              =    {en} Ry\nJOB DONE.\n"
            open(os.path.join(d, n, "relax.out"), "w", encoding="utf-8").write(
                ("Begin final coordinates\n" + ob + "End final coordinates\n" + tail) if conv
                else ("     Total force =     0.018000\n" + ob
                      + "     The maximum number of steps has been reached\n" + tail))
        return d

    # 뛰는 Li 하나 + 근거리 이웃 + 원거리 원자들
    # 자유 원자 ≥ 8 가드를 만족하도록 근거리를 현실적으로 채운다
    NEAR = [("Li", (7.0, 0.0, 0.0)), ("Li", (0.0, 3.0, 0.0)), ("Li", (0.0, -3.0, 0.0)),
            ("Li", (1.8, 2.5, 0.0)), ("Li", (1.8, -2.5, 0.0)), ("Li", (1.8, 0.0, 2.5)),
            ("Li", (1.8, 0.0, -2.5)), ("Li", (3.0, 3.0, 0.0))]
    FAR = [("Li", (0.0, 0.0, 6.5)), ("Li", (6.5, 6.5, 6.5))]
    A2 = [("Li", (0.0, 0.0, 0.0))] + NEAR + FAR
    B2 = [("Li", (3.667, 0.0, 0.0))] + NEAR + FAR
    mkf("fz", True, A2, B2)
    rc, msg = build_frozen(td, "fz", 4.0)
    chk(rc == 0, "[고정셸] 대칭 홉이면 입력을 만든다")
    fd = os.path.join(td, "fz", "frozen_R4")
    chk(os.path.isfile(os.path.join(fd, "endpoint", "relax.in"))
        and os.path.isfile(os.path.join(fd, "saddle", "relax.in")),
        "[고정셸] endpoint·saddle 둘 다 생긴다")

    def rows_of(f):
        L = open(f, encoding="utf-8").read().splitlines()
        i = [n for n, l in enumerate(L) if l.startswith("ATOMIC_POSITIONS")][0]
        out = []
        for l in L[i + 1:]:
            q = l.split()
            if len(q) >= 4 and re.match(r"^[A-Z][a-z]?$", q[0]):
                out.append((q[0], [float(x) for x in q[1:4]], "0 0 0" in l))
            elif out:
                break
        return out
    E = rows_of(os.path.join(fd, "endpoint", "relax.in"))
    S = rows_of(os.path.join(fd, "saddle", "relax.in"))
    chk(len(E) == len(S) == 1 + len(NEAR) + len(FAR), "[고정셸] 원자 수 보존")
    chk([r[2] for r in E][1:] == [r[2] for r in S][1:],
        "[고정셸] 고정/자유 집합이 endpoint·saddle 에서 동일하다")
    # ★ F2 회귀: 고정 원자는 두 파일에서 **같은 좌표**
    same = all(abs(a[1][k] - b[1][k]) < 1e-9 for a, b in zip(E, S) if a[2]
               for k in range(3))
    chk(same, "[핵심 F2] 고정 원자가 endpoint·saddle 에서 같은 좌표다")
    chk(sum(1 for r in E if r[2]) >= 1, "[고정셸] 원거리 원자가 실제로 고정된다")
    chk(not E[0][2] and S[0][2], "[고정셸] 뛰는 원자는 끝점에서 자유·안장에서 고정")
    fm = json.load(open(os.path.join(fd, "frozen_meta.json"), encoding="utf-8"))
    chk(fm.get("supercell") == [3, 3, 3] and fm.get("lambda1_A") and fm.get("min_face_height_A"),
        "[핵심 F4] frozen_meta 에 셀 식별정보(λ₁·면높이)가 있다")
    # ★ Codex P0 회귀 — λ₁ > 면높이 여야 한다 (직교 셀이면 같다). 둘을 혼동하면 안 된다.
    chk(fm["lambda1_A"] >= fm["min_face_height_A"] - 1e-9,
        f"[핵심 P0] λ₁({fm['lambda1_A']}) ≥ 면높이({fm['min_face_height_A']}) — 지표를 안 뒤바꿨다")
    chk(abs(fm.get("max_radius_A", 0) - fm["lambda1_A"] / 2) < 1e-6,
        "[핵심 P0] 반경 상한이 **λ₁/2** 다 (면높이/2 가 아니다)")
    chk(fm.get("recommended_design", {}).get("cross_cell_comparison") == [3.5, 4.0],
        "[④] 권장 반경 설계가 기록된다")
    ev = fm.get("midpoint_saddle_evidence") or {}
    chk("inversion_maps_endpoints" in ev and "freeze_mask_inversion_invariant" in ev,
        "[②] 중점=안장 근거(대칭연산·mask 불변성)를 기록한다")
    chk(len(ev.get("still_required") or []) >= 3,
        "[②] 아직 필요한 검증(raw force·±δ·CI-NEB 교차)을 명시한다")
    chk(os.path.isfile(os.path.join(fd, "saddle_rawforce", "README.txt")),
        "[③] if_pos 마스킹 때문에 구속 해제 단일점 안내를 만든다")
    chk(fm.get("symmetry_basis") and fm.get("max_frozen_atom_shift_A") is not None,
        "[F4] 대칭근거·고정원자 이동량을 기록한다")

    # ── 음성 ──
    mkf("fz_asym", False, A2, B2, e_fin="-99.0000")
    rc, msg = build_frozen(td, "fz_asym", 4.0)
    chk(rc == 1 and "대칭 근거가 없다" in msg, "[핵심 F1] 고정셸도 비대칭 홉을 거부한다")

    # ⛔ 가드 기준이 λ₁/2 로 바뀌었다 (면높이/2 가 아니다) — 14 Å 직교셀이면 λ₁=14, 상한 7
    rc, msg = build_frozen(td, "fz", 8.0)
    chk(rc == 1 and "λ₁/2" in msg, "[음성] 반경이 **λ₁/2** 를 넘으면 거부")
    rc, _ = build_frozen(td, "fz", 6.0)
    chk(rc == 0, "[음성] λ₁/2 안쪽 반경은 통과 (면높이/2 로 재면 부당하게 막혔을 값)")

    rc, msg = build_frozen(td, "fz", 0.5)          # 자유 원자 거의 없음
    chk(rc == 1, "[음성] 반경이 너무 작으면 거부")

    # ★ ① fail-open 회귀 — spglib False 를 에너지 축퇴로 뒤집으면 안 된다
    mkf("fz_false_deg", False, A2, B2)             # sym=False 인데 에너지는 같음
    rc, msg = build_frozen(td, "fz_false_deg", 4.0)
    chk(rc == 1 and "대칭 비동등" in msg,
        "[핵심 ①] sym=False 는 **에너지가 같아도** 거부한다 (fail-open 1)")

    # ★ ① fail-open 회귀 — 아직 도는 중인 끝점은 축퇴가 있어도 거부
    d_run = mkf("fz_running", None, A2, B2)
    for n in ("ep_initial", "ep_final"):
        fp = os.path.join(d_run, n, "relax.out")
        s0 = open(fp, encoding="utf-8").read()
        open(fp, "w", encoding="utf-8").write(s0.replace("JOB DONE.", ""))
    rc, msg = build_frozen(td, "fz_running", 4.0)
    chk(rc == 1 and "아직 도는 중" in msg,
        "[핵심 ①] 실행 중 끝점은 에너지 축퇴로도 통과 못 한다 (fail-open 2)")

    # ★ ① sym=True 인데 에너지가 크게 다르면 conflict 경고
    mkf("fz_conflict", True, A2, B2, e_fin="-99.0000")
    rc, msg = build_frozen(td, "fz_conflict", 4.0)
    chk(rc == 0 and "conflict" in msg,
        "[핵심 ①] sym=True + 에너지 불일치는 통과하되 conflict 로 표시한다")

    # ★ F2 회귀 (음성): 원거리 원자가 끝점 사이에서 움직이면 거부
    FARM = [("Li", (0.0, 0.0, 6.5)), ("Li", (6.9, 6.5, 6.5))]   # 원거리 하나가 0.4 Å 이동
    mkf("fz_shift", True, [("Li", (0.0, 0.0, 0.0))] + NEAR + FAR,
        [("Li", (3.667, 0.0, 0.0))] + NEAR + FARM)
    rc, msg = build_frozen(td, "fz_shift", 4.0)
    chk(rc == 1 and "고정 대상 원자가" in msg,
        "[핵심 F2] 고정 대상이 움직이면 거부한다 (Ea 오염 방지)")

    # ★★ 2026-08-27 실측 회귀 (음성) — **갓 지은 좌표로는 통과하는데 이완 좌표로는 깨지는**
    #   경우. ccpath 가 정확히 이랬다: relax.in 기준 0.000 통과 · 실제 이완 1.035 Å.
    #   옛 게이트는 relax.in 만 봐서 이걸 놓쳤고, 고정 원자가 1 Å 어긋난 채 못박혔을 것이다.
    FAR_REL = [("Li", (0.0, 0.0, 6.5)), ("Li", (6.5, 6.5, 7.5))]     # 이완에서 1.0 Å 이동
    mkf("fz_relaxed_breaks", True, A2, B2,
        out_rows=([("Li", (0.0, 0.0, 0.0))] + NEAR + FAR,
                  [("Li", (3.667, 0.0, 0.0))] + NEAR + FAR_REL))
    rc, msg = build_frozen(td, "fz_relaxed_breaks", 4.0)
    chk(rc == 1 and "이완 좌표" in msg,
        "[핵심·실측회귀] 갓 지은 좌표로 통과해도 **이완 좌표로 깨지면** 거부한다")

    # ★ 그 짝(음성): 끝점 이완이 아직 없으면 전제를 **검사할 수 없다** — 거저 통과 금지
    mkf("fz_no_relax", True, A2, B2)
    for _n in ("ep_initial", "ep_final"):
        os.remove(os.path.join(td, "fz_no_relax", _n, "relax.out"))
    rc, msg = build_frozen(td, "fz_no_relax", 4.0)
    chk(rc == 1 and "검사할 수 없다" in msg,
        "[핵심·실측회귀] 이완 좌표가 없으면 통과시키지 않고 그렇게 말한다")

    # ★ 미수렴 이완이어도 게이트는 돌되 **미수렴을 명시**한다 (조용히 쓰지 않는다)
    mkf("fz_unconv", True, A2, B2, conv=False,
        out_rows=([("Li", (0.0, 0.0, 0.0))] + NEAR + FAR,
                  [("Li", (3.667, 0.0, 0.0))] + NEAR + FAR_REL))
    rc, msg = build_frozen(td, "fz_unconv", 4.0)
    chk(rc == 1 and "미수렴" in msg,
        "[핵심·실측회귀] 미수렴 이완으로 막을 때 미수렴이라고 말한다")

    # ★ F5 회귀: 안 끝난 relax.out 에서 Ea 를 만들지 않는다
    for sub in ("endpoint", "saddle"):
        open(os.path.join(fd, sub, "relax.out"), "w", encoding="utf-8").write(
            "!    total energy              =    -100.0000 Ry\n")   # JOB DONE 없음
    rc, msg = collect(td, "fz", 4.0)
    chk(rc == 1 and "JOB DONE" in msg, "[핵심 F5] 아직 도는 중이면 회수를 거부한다")
    rc, msg = collect(td, "fz", 4.0, allow_unconverged=True)
    chk(rc == 0 and "Ea" in msg, "[F5] --allow_unconverged 면 경고와 함께 회수")

    shutil.rmtree(td, ignore_errors=True)

    # ── 이어달리기 디렉터리 선택 (2026-08-16) ──────────────────────────────
    #   watch 의 [0/4] 는 ep_*_r2 를 보는데 이 도구는 원본만 읽고 있었다 —
    #   수렴본을 두고 미수렴 원본으로 고정셸을 만들 뻔했다.
    import tempfile as _tf
    _d = _tf.mkdtemp(); _t = os.path.join(_d, "li3nd"); os.makedirs(_t)
    def _mkep(name, converged):
        os.makedirs(os.path.join(_t, name), exist_ok=True)
        body = "     Total force =     0.001\n"
        body += ("Begin final coordinates\nEnd final coordinates\n" if converged
                 else "     The maximum number of steps has been reached.\n")
        open(os.path.join(_t, name, "relax.out"), "w", encoding="utf-8").write(body)
    _mkep("ep_initial", False)
    chk(os.path.basename(endpoint_dir(_t, "ep_initial")) == "ep_initial",
        "[이어달리기] 수렴본 없으면 원본")
    _mkep("ep_initial_r2", True)
    chk(os.path.basename(endpoint_dir(_t, "ep_initial")) == "ep_initial_r2",
        "[이어달리기] 수렴한 _r2 를 고른다")
    _mkep("ep_initial_r3", False)
    chk(os.path.basename(endpoint_dir(_t, "ep_initial")) == "ep_initial_r2",
        "[이어달리기·음성] 미수렴 _r3 로 가지 않는다")
    _mkep("ep_initial_r4", True)
    chk(os.path.basename(endpoint_dir(_t, "ep_initial")) == "ep_initial_r4",
        "[이어달리기] 수렴본이 여럿이면 가장 나중 것")
    chk(os.path.basename(endpoint_dir(_t, "ep_final")) == "ep_final",
        "[이어달리기·음성] 없는 끝점은 원본 경로")

    _p("selftest " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


# ══ P0-1 (교차리뷰 I · 2026-08-27) — 겉보기 변위에서 **비물리 성분을 먼저 뺀다** ══
#
#  왜 생겼나: `build_frozen` 도, `build_neb_inputs.endpoint_displacement_max_A` 도
#  두 끝점을 **원자 순서대로 zip** 해서 변위를 잰다. 그 값은 다음을 포함한다:
#    (a) 두 끝점을 독립 이완하며 각각 생긴 **강체 표류** — 셀은 병진 불변이라 물리가 아니다
#    (b) 같은 원소끼리의 **라벨 교환** — 이완 중 순서가 바뀌면 없던 변위가 생긴다
#  cc333 의 `1.240 Å` 블로커와 `107/107 원자 이동` 은 (a) 의 전형적 지문이다.
#  이 절은 (a)·(b) 를 뺀 **잔여 변위**를 내서, 비국소 이완이 진짜인지 가른다.
FAR_FIELD_R_A = 6.0        # 이 거리 밖을 far-field 로 본다 (홉 중점 기준)
ARTIFACT_TOL_A = 0.05      # far-field 잔여가 이 밑이면 겉보기 변위는 인공물이었다
REAL_TOL_A = 0.30          # 이 위면 정렬로 설명 안 된다 = 실제 비국소 이완


def _optimal_pbc_translation(first, last, cell, skip=(), iters=80):
    """두 좌표 집합을 잇는 최적 강체 병진 (성분별 중앙값 고정점).

    중앙값을 쓰는 이유: 진짜로 움직인 소수 원자(뛰는 Li·재배열 Nd)에 끌려가지 않는다.
    평균을 쓰면 그 원자들이 병진 추정을 오염시켜, 빼야 할 것을 못 빼고
    빼면 안 되는 것을 빼게 된다.
    """
    sk = set(skip)
    idx = [i for i in range(len(first)) if i not in sk]
    t = [0.0, 0.0, 0.0]
    conv = False
    for _ in range(iters):
        d = [min_image([last[i][1][k] - first[i][1][k] - t[k] for k in range(3)], cell)
             for i in idx]
        med = [sorted(v[k] for v in d)[len(d) // 2] for k in range(3)]
        if max(abs(x) for x in med) < 1e-9:
            conv = True
            break
        t = [t[k] + med[k] for k in range(3)]
    return t, conv


def _assign_by_element(first, last, cell, shift):
    """원소별 최소변위 대응 → (match, n_reassigned, method).

    match[i] = last 쪽 인덱스. 같은 원소 안에서만 짝을 짓는다.
    """
    import math as _m
    groups = {}
    for i, (s, _) in enumerate(first):
        groups.setdefault(s, [[], []])[0].append(i)
    for j, (s, _) in enumerate(last):
        if s not in groups:
            groups[s] = [[], []]
        groups[s][1].append(j)

    def cost(i, j):
        d = min_image([last[j][1][k] - first[i][1][k] - shift[k] for k in range(3)], cell)
        return _m.sqrt(sum(x * x for x in d))

    try:
        from scipy.optimize import linear_sum_assignment as _lsa
        import numpy as _np
        method = "hungarian(scipy)"
    except Exception:
        _lsa, method = None, "greedy-global"

    match, nre = {}, 0
    for s, (ii, jj) in groups.items():
        if len(ii) != len(jj):
            return None, None, f"⛔ 원소 {s} 개수가 다르다 ({len(ii)} vs {len(jj)})"
        if _lsa is not None:
            C = _np.array([[cost(i, j) for j in jj] for i in ii], float)
            r, c = _lsa(C)
            for a, b in zip(r, c):
                match[ii[a]] = jj[b]
        else:
            pairs = sorted(((cost(i, j), i, j) for i in ii for j in jj))
            ui, uj = set(), set()
            for _c, i, j in pairs:
                if i in ui or j in uj:
                    continue
                match[i] = j
                ui.add(i)
                uj.add(j)
    for i, j in match.items():
        if i != j:
            nre += 1
    return match, nre, method


def align_report(first, last, cell, far_r=FAR_FIELD_R_A):
    """정렬(병진 제거 + 라벨 재대응) 뒤의 잔여 변위 보고서.

    ⛔ 이 함수가 **못 하는 것**
      · 공간군 **회전·반사** 연산은 시도하지 않는다 — 병진과 라벨 교환만 뺀다.
        두 끝점이 회전으로 연결돼 있으면 그 성분이 잔여 변위로 남아 '실제'로 오판된다.
      · 잔여 변위가 **물리인지 이완 미수렴 표류인지 못 가른다.** 수렴 여부는 호출자가
        relax.out 에서 확인해 같이 찍어야 한다 (align_endpoints 가 그렇게 한다).
      · 홉 원자를 '가장 크게 움직인 원자' 로 잡는다 — 진짜 홉이 아니어도 그렇게 잡힌다.
      · far-field 원자가 없으면(작은 셀) **판정하지 않고 그렇게 말한다.**
    """
    import math as _m
    n = len(first)
    if n != len(last) or n == 0:
        return {"error": "⛔ 원자 수가 다르거나 0 이다"}
    if sorted(s for s, _ in first) != sorted(s for s, _ in last):
        return {"error": "⛔ 두 끝점의 원소 구성이 다르다"}

    def _nrm(v):
        return _m.sqrt(sum(x * x for x in v))

    raw = [_nrm(min_image([last[i][1][k] - first[i][1][k] for k in range(3)], cell))
           for i in range(n)]
    hop = max(range(n), key=lambda i: raw[i])

    shift, tconv = _optimal_pbc_translation(first, last, cell, skip=(hop,))
    match, nre, method = _assign_by_element(first, last, cell, shift)
    if match is None:
        return {"error": method}

    res = [_nrm(min_image([last[match[i]][1][k] - first[i][1][k] - shift[k]
                           for k in range(3)], cell)) for i in range(n)]
    hop2 = max(range(n), key=lambda i: res[i])
    d_hop = min_image([last[match[hop2]][1][k] - first[hop2][1][k] - shift[k]
                       for k in range(3)], cell)
    ctr = [first[hop2][1][k] + d_hop[k] / 2.0 for k in range(3)]
    dist = [_nrm(min_image([first[i][1][k] - ctr[k] for k in range(3)], cell))
            for i in range(n)]

    far = [i for i in range(n) if i != hop2 and dist[i] > far_r]
    ff = max((res[i] for i in far), default=None)
    out = {
        "n_atoms": n,
        "translation_A": [round(x, 4) for x in shift],
        "translation_norm_A": round(_nrm(shift), 4),
        "translation_converged": tconv,
        "assignment": method,
        "n_relabeled": nre,
        "hop_atom": {"index_raw": hop, "index_aligned": hop2,
                     "element": first[hop2][0],
                     "raw_A": round(raw[hop], 4), "aligned_A": round(res[hop2], 4)},
        "raw_max_excl_hop_A": round(max((raw[i] for i in range(n) if i != hop), default=0.0), 4),
        "aligned_max_excl_hop_A": round(max((res[i] for i in range(n) if i != hop2),
                                            default=0.0), 4),
        "far_field_R_A": far_r,
        "n_far_field": len(far),
        "far_field_max_A": None if ff is None else round(ff, 4),
    }
    # 거리 구간별 잔여 (비국소성이 실제면 far-field 까지 꼬리가 남는다)
    bins, edges = [], [2.0, 4.0, 6.0, 8.0, 1e9]
    lo = 0.0
    for hi in edges:
        sel = [res[i] for i in range(n) if i != hop2 and lo <= dist[i] < hi]
        if sel:
            bins.append({"r_A": f"{lo:.0f}–{'∞' if hi > 1e8 else f'{hi:.0f}'}",
                         "n": len(sel), "max_A": round(max(sel), 4),
                         "median_A": round(sorted(sel)[len(sel) // 2], 4)})
        lo = hi
    out["by_distance"] = bins

    # ── 국소성: 변위장이 거리에 따라 주는가 (공공 중심 응답의 모양인가) ──────────
    #   실측 계기(2026-08-27 cc333): 중앙값이 2–4 Å 0.44 · 6–8 Å 0.44 로 **안 준다.**
    #   같은 날 ccpath 는 1.04 → 0.95 → 0.32 로 준다. 이 차이가 눈에 보여야 한다.
    pop = [b for b in bins if b["n"] >= 3]
    if len(pop) >= 2:
        inner, outer = pop[0]["median_A"], pop[-1]["median_A"]
        ratio = (outer / inner) if inner > 1e-9 else None
        out["locality"] = {
            "inner_bin": pop[0]["r_A"], "inner_median_A": inner,
            "outer_bin": pop[-1]["r_A"], "outer_median_A": outer,
            "outer_over_inner": None if ratio is None else round(ratio, 3),
            "monotone_decreasing": all(pop[i]["median_A"] >= pop[i + 1]["median_A"]
                                       for i in range(len(pop) - 1)),
        }
        if ratio is not None and ratio >= 0.5:
            out["locality"]["note"] = ("⚠ 변위장이 거리에 따라 **안 준다** — 공공 중심 "
                                       "국소 응답의 모양이 아니다. 전역 재배열이거나 "
                                       "미수렴 optimizer 의 배회다 (이 도구는 못 가른다).")
    out["max_distance_A"] = round(max(dist), 2)

    if out["raw_max_excl_hop_A"] <= ARTIFACT_TOL_A:
        # ⛔ 위양성 차단 (2026-08-27 실측에서 걸림) — 갓 지은 끝점은 정의상 홉 외 변위가 0 이다.
        #   거기에 "인공물" 을 찍으면 *정렬이 뭔가를 걷어냈다* 는 정반대 인상을 준다.
        out["verdict"] = "무정보"
        out["verdict_text"] = (
            f"⚪ 홉 외 원자가 **애초에 안 움직였다** (raw {out['raw_max_excl_hop_A']} Å). "
            f"정렬이 뭘 걷어낸 게 아니라 **걷어낼 게 없었다** — 갓 지은 좌표의 지문이다. "
            f"이 판정은 아무것도 보증하지 않는다. **이완 좌표(`--align_source out`)로 다시 볼 것.**")
    elif ff is None:
        out["verdict"] = "판정불가"
        out["verdict_text"] = (
            f"⚠ 홉 중점에서 {far_r} Å 밖에 원자가 없다 (셀 최대거리 {out['max_distance_A']} Å) — "
            f"이 셀로는 far-field 를 볼 수 없다. `--far_r {max(2.0, 0.6*out['max_distance_A']):.1f}` "
            f"쯤으로 줄이거나 큰 셀이 필요하다. **위 거리별 표는 그대로 유효하다.**")
    elif ff <= ARTIFACT_TOL_A:
        out["verdict"] = "인공물"
        out["verdict_text"] = (f"❌ 정렬 뒤 far-field 최대가 {ff:.3f} Å ≤ {ARTIFACT_TOL_A} — "
                               f"겉보기 변위는 **병진/라벨 인공물**이었다. "
                               f"비국소 이완의 증거가 아니다.")
    elif ff >= REAL_TOL_A:
        out["verdict"] = "실제"
        out["verdict_text"] = (f"✅ 정렬 뒤에도 far-field 가 {ff:.3f} Å ≥ {REAL_TOL_A} 남는다 — "
                               f"병진·라벨로 설명되지 않는다. (다만 이완 미수렴 표류는 "
                               f"이 도구가 못 가른다 — 수렴 여부를 같이 볼 것)")
    else:
        out["verdict"] = "회색"
        out["verdict_text"] = (f"⚠ far-field 최대 {ff:.3f} Å 이 {ARTIFACT_TOL_A}–{REAL_TOL_A} "
                               f"사이다 — 어느 쪽도 주장하지 않는다.")
    return out


# ══ P0-2 예비 — **공짜 판정**: 잔여가 물리인가 미수렴 배회인가 ═════════════════
#
#  2026-08-27 정렬 진단이 남긴 질문: cc333 끝점의 1.234 Å 잔여가 실제 이완인지,
#  nstep 한도에서 끝난 optimizer 의 배회인지. 새 계산 없이 relax.out 안에 답이 있다 —
#  QE 는 **모든 BFGS 스텝의 좌표**를 찍기 때문이다. 두 가지를 본다:
#
#   ① 배회지수 = Σ|스텝별 이동| / |순 이동|.  1 에 가까우면 한 방향으로 곧게 간 것(실제
#      이완), 크면 왔다갔다 한 것(배회). 미수렴이어도 ①이 1 근처면 "느린 이완" 이다.
#   ② 두 끝점의 **모드 일치도** = 각자 출발점 기준 순변위 3N 벡터의 코사인.
#      배회는 두 계산에서 정렬될 이유가 없다. 정렬돼 있으면 **격자 자체의 모드**다.
#      ← 이게 P0-2(전역 soft mode) 의 직접 지문이다.
RY_EV = 13.605693122994
RYAU_EVA = 25.711


def _all_pos_blocks(txt):
    """relax.out 의 **모든** ATOMIC_POSITIONS 블록 → [rows, …] (스텝 순서)."""
    out, i = [], txt.find("ATOMIC_POSITIONS")
    while i >= 0:
        rows = _pos_block(txt, i)
        if rows:
            out.append(rows)
        i = txt.find("ATOMIC_POSITIONS", i + 1)
    return out


def trace_report(steps, cell, energies=None, forces=None):
    """한 끝점의 BFGS 궤적 요약. 반환 dict.

    ⛔ 못 하는 것
      · 배회지수가 1 이어도 **그 방향이 물리적으로 옳다는 보증은 없다** — 곧게 갔다는 것뿐.
      · 스텝 사이 강체 병진만 뺀다. 회전은 안 뺀다.
      · 블록이 2개 미만이면 궤적이 아니다 — 그렇게 말하고 끝낸다.
    """
    import math as _m
    n = len(steps)
    if n < 2:
        return {"error": f"⛔ BFGS 블록이 {n}개다 — 궤적이 아니다 (수렴본만 남았거나 첫 스텝)"}
    nat = len(steps[0])
    if any(len(s) != nat for s in steps):
        return {"error": "⛔ 스텝마다 원자 수가 다르다"}

    def _al(a, b):                        # b 를 a 에 맞춰 병진 제거한 변위 리스트
        t, _c = _optimal_pbc_translation(a, b, cell)
        return [min_image([b[i][1][k] - a[i][1][k] - t[k] for k in range(3)], cell)
                for i in range(nat)]

    def _nrm(v):
        return _m.sqrt(sum(x * x for x in v))

    net = _al(steps[0], steps[-1])
    path = [0.0] * nat
    for s in range(n - 1):
        d = _al(steps[s], steps[s + 1])
        for i in range(nat):
            path[i] += _nrm(d[i])
    hop = max(range(nat), key=lambda i: _nrm(net[i]))
    keep = [i for i in range(nat) if i != hop]
    sum_net = sum(_nrm(net[i]) for i in keep)
    sum_path = sum(path[i] for i in keep)
    # 마지막 3 스텝에서 아직 움직이는가
    tail = 0.0
    for s in range(max(0, n - 4), n - 1):
        tail += max(_nrm(v) for i, v in enumerate(_al(steps[s], steps[s + 1])) if i != hop)
    return {
        "n_steps": n, "n_atoms": nat, "hop_index": hop,
        "net_max_A": round(max(_nrm(net[i]) for i in keep), 4),
        "net_median_A": round(sorted(_nrm(net[i]) for i in keep)[len(keep) // 2], 4),
        "path_max_A": round(max(path[i] for i in keep), 4),
        "wander_index": round(sum_path / sum_net, 3) if sum_net > 1e-9 else None,
        "tail3_move_A": round(tail, 4),
        "net_vector": [net[i] for i in range(nat)],
        "energy_drop_eV": (round((energies[-1] - energies[0]) * RY_EV, 4)
                           if energies and len(energies) >= 2 else None),
        "energy_tail3_eV": (round((energies[-1] - energies[-4]) * RY_EV, 5)
                            if energies and len(energies) >= 4 else None),
        "force_first_eVA": round(forces[0] * RYAU_EVA, 4) if forces else None,
        "force_last_eVA": round(forces[-1] * RYAU_EVA, 4) if forces else None,
    }


def inversion_match(first, last, ctr, cell):
    """홉 중점 반전 `x → 2·ctr − x` 의 원자 대응 P 와 그 최악 잔차. → (match, worst)

    ⛔ **문턱을 두지 않는다** (2026-08-27 자체수정). 처음엔 `worst > 1.0 Å` 이면 match 를
      None 으로 버리게 했는데, 그러면 정작 보려던 경우 — cc333 처럼 끝점이 1.23 Å 어긋난
      경우 — 에 코사인을 아예 못 본다. 문턱이 판정을 삼킨다.
      → 대응은 언제나 돌려주고, **잔차를 같이 보고**해서 읽는 쪽이 할인하게 한다.
      match 가 None 인 것은 대응 자체가 성립 못 할 때뿐이다(원소 개수 불일치).

    왜 필요한가 (2026-08-27, 실측이 가르쳐 준 것):
      두 끝점이 **대칭 등가**면 이완 변위장은 *같지* 않고 **대칭 연산으로 관계**된다.
      그래서 같은 index 로 잰 코사인은 서로 다른 자리의 변위를 비교하게 되어
      **0 근처가 나오는 것이 정상**이다 — 그걸 "배회" 로 읽으면 정반대 결론이 난다.
      실측: ccpath 두 끝점의 이완 스칼라가 소수 4자리까지 같은데 raw 코사인은 0.018 이었다.

    ⛔⛔ 2026-08-27 두 번째 버그 — 옛 판은 **index 순서대로 greedy** 로 짝을 지었다
      (`used` 에 담아 가며). 앞 원자가 좋은 짝을 선점하면 **뒤 원자에는 아무거나 남고**,
      그 찌꺼기가 `worst` 를 지배한다. 그래서 대칭이 멀쩡한 ccpath 에서도 잔차가
      셀보다 크게 나왔다. → 이미 있는 `_assign_by_element`(scipy Hungarian, 없으면
      전역정렬 greedy)를 쓴다. **같은 문제를 두 번 푸는 코드를 만들지 않는다.**
    """
    import math as _m
    inv_first = [(s, [2 * ctr[k] - q[k] for k in range(3)]) for s, q in first]
    match, _nre, method = _assign_by_element(inv_first, last, cell, [0.0, 0.0, 0.0])
    if match is None:
        return None, None
    worst = 0.0
    for i, j in match.items():
        dd = min_image([last[j][1][k] - inv_first[i][1][k] for k in range(3)], cell)
        worst = max(worst, _m.sqrt(sum(x * x for x in dd)))
    return match, worst


def mode_overlap(a_vec, b_vec, skip=(), match=None, sign=1.0):
    """두 끝점의 순변위 3N 벡터 코사인.

    match 를 주면 `b_vec[match[i]]` 와 비교하고, sign=-1 이면 부호를 뒤집는다
    (반전 대칭이면 변위 벡터도 뒤집히므로 `cos(d_A[i], −d_B[P(i)])` 가 옳은 비교다).
    """
    import math as _m
    sk = set(skip)
    idx = [i for i in range(min(len(a_vec), len(b_vec))) if i not in sk]
    if match is not None:
        idx = [i for i in idx if match.get(i) is not None and match[i] not in sk]
    _b = (lambda i: b_vec[match[i]]) if match is not None else (lambda i: b_vec[i])
    num = sum(sum(a_vec[i][k] * sign * _b(i)[k] for k in range(3)) for i in idx)
    na = _m.sqrt(sum(sum(x * x for x in a_vec[i]) for i in idx))
    nb = _m.sqrt(sum(sum(x * x for x in _b(i)) for i in idx))
    return None if na < 1e-9 or nb < 1e-9 else round(num / (na * nb), 4)


# ══ 사전등록 선행검사 2건 — 둘 다 **고정 기하 SCF** 로 끝난다 ═══════════════════
#
#  ① smearing 사다리 (kb 2026-08-11 등록 · 회신 I N5 재확인)
#     `degauss = 0.02 Ry ≈ 0.272 eV` 이고 장벽이 0.229 eV 다 — **같은 자릿수**다.
#     0.02 → 0.01 → 0.005 로 내리며 장벽이 사전 허용폭 안에 있는지 본다.
#  ② pristine ±δ 모드 스캔 (회신 I P0-2 의 싼 판)
#     공공 없는 셀을 **관측한 이완 모드 방향으로** 밀어 E(λ) 를 본다. λ=0 이 최소면
#     그 이완은 공공이 유발한 것이고, 내려가면 **격자 자체가 그 모드로 불안정**하다
#     (그 경우 끝점 정의가 무효라 MD 로 옮겨도 해결이 안 된다).
#
#  ⛔ 둘 다 **프로토콜을 다시 유도하지 않는다.** 돌고 있는 런의 입력에서 그대로 읽는다
#     (PP·k·ecut·전하·smearing 종류). 다시 유도하면 NEB 와 다른 조건이 될 수 있고,
#     그러면 비교가 성립하지 않는다 — 이 repo 가 이미 두 번 밟은 함정이다.
SMEAR_LADDER_RY = (0.02, 0.01, 0.005)
# ⛔ 리뷰 J2 — ±0.25 는 **국소 곡률을 보기엔 이미 크다.** 작은 진폭을 넣는다.
#   ±1.5·±2 는 넣지 않는다 — λ=1 까지 계속 내려가면 외삽보다 **변위 구조 이완**이 낫다.
MODE_SCAN_LAMBDAS = (-1.0, -0.5, -0.25, -0.10, -0.05, 0.0, 0.05, 0.10, 0.25, 0.5, 1.0)


def _sha(path, n=16):
    """파일 SHA256 앞 n 글자. 없으면 'MISSING'.

    왜 남기나(리뷰 J): 입력이 뭘로 만들어졌는지 나중에 못 되짚으면, 값이 흔들렸을 때
    **PP 가 바뀐 건지 설정이 바뀐 건지 못 가른다.**
    """
    import hashlib
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for b in iter(lambda: f.read(1 << 20), b""):
                h.update(b)
        return h.hexdigest()[:n]
    except OSError:
        return "MISSING"


def parse_qe_header(src_in):
    """QE 입력(relax.in · neb.in)에서 **프로토콜 조각**을 그대로 뜯어온다.

    반환: {pseudo_dir, ecutwfc, ecutrho, tot_charge, smearing, degauss, conv_thr,
           mixing_beta, species:[(el, mass, upf)], kpts:str, cell:[[..]]}
    ⛔ 못 하는 것: 값을 검증하지 않는다 — **있는 그대로** 옮긴다. 그게 이 함수의 목적이다.
      neb.in 은 BEGIN_ENGINE_INPUT 안쪽만 본다(&PATH 는 SCF 와 무관하다).
    """
    if not os.path.isfile(src_in):
        return None, f"⛔ 없음: {src_in}"
    t = open(src_in, encoding="utf-8", errors="replace").read()
    i = t.find("BEGIN_ENGINE_INPUT")
    if i >= 0:
        t = t[i:]
    out = {"src": src_in}

    def _s(key, cast=str, default=None):
        m = re.search(rf"^\s*{key}\s*=\s*'?([^'\n,!]+)'?", t, re.M)
        if not m:
            return default
        v = m.group(1).strip()
        try:
            return cast(v.replace("d", "e").replace("D", "e")) if cast is not str else v
        except ValueError:
            return default
    out["pseudo_dir"] = _s("pseudo_dir")
    out["ecutwfc"] = _s("ecutwfc", float)
    out["ecutrho"] = _s("ecutrho", float)
    out["tot_charge"] = _s("tot_charge", float, 0.0)
    out["smearing"] = _s("smearing", str, "mv")
    out["degauss"] = _s("degauss", float)
    out["conv_thr"] = _s("conv_thr", str, "1.0d-8")
    out["mixing_beta"] = _s("mixing_beta", str, "0.3")
    sp = []
    m = re.search(r"ATOMIC_SPECIES\s*\n((?:\s*\S+\s+\S+\s+\S+\s*\n)+)", t)
    if m:
        for l in m.group(1).strip().splitlines():
            p = l.split()
            if len(p) >= 3:
                sp.append((p[0], p[1], p[2]))
    out["species"] = sp
    # ⛔ 2026-08-27 (리뷰 J · P0) — 옛 판은 파싱 실패 시 조용히 `2 2 2 0 0 0` 을 넣었다.
    #   그러면 **엔진 블록을 복제한다는 이 함수의 약속이 깨진다** — NEB 가 3×3×3 으로 돌았는데
    #   비교용 SCF 가 2×2×2 로 나가고, 그 차이가 장벽 차이로 보고된다. 기본값을 없앤다.
    m = re.search(r"K_POINTS\s*(\w+)\s*\n\s*([\d\s]+)\n", t)
    out["kpts"] = (m.group(1), m.group(2).strip()) if m else None
    m = re.search(r"CELL_PARAMETERS\s*\(?angstrom\)?\s*\n"
                  r"((?:\s*[-\d.eE+]+\s+[-\d.eE+]+\s+[-\d.eE+]+\s*\n){3})", t)
    out["cell"] = ([[float(x) for x in l.split()] for l in m.group(1).strip().splitlines()]
                   if m else None)
    miss = [k for k in ("pseudo_dir", "ecutwfc", "cell", "kpts", "degauss") if not out.get(k)]
    if miss or not sp:
        return None, (f"⛔ {src_in} 에서 못 읽은 것: {miss or ''} "
                      f"{'ATOMIC_SPECIES' if not sp else ''}\n"
                      f"   기본값으로 메우지 않는다 — 엔진 블록을 **그대로 복제**하는 것이 "
                      f"이 함수의 유일한 목적이다 (리뷰 J P0).")
    out["src_sha256"] = _sha(src_in)
    out["upf_sha256"] = {e: _sha(os.path.join(out["pseudo_dir"], u)) for e, _m, u in sp}
    return out, None


def write_scf(path, prefix, hdr, rows, degauss=None, tot_charge=None):
    """고정 기하 SCF 입력 하나. hdr 는 parse_qe_header 산출물."""
    els = sorted({s for s, _ in rows})
    sp = [x for x in hdr["species"] if x[0] in els]
    if len(sp) != len(els):
        return f"⛔ ATOMIC_SPECIES 에 없는 원소가 있다: {sorted(els - {x[0] for x in sp})}"
    L = ["&CONTROL", "    calculation     = 'scf'", f"    prefix          = '{prefix}'",
         "    outdir          = './tmp'", f"    pseudo_dir      = '{hdr['pseudo_dir']}'",
         "    tprnfor         = .true.", "/",
         "&SYSTEM", "    ibrav           = 0", f"    nat             = {len(rows)}",
         f"    ntyp            = {len(sp)}",
         f"    ecutwfc         = {hdr['ecutwfc']:g}",
         f"    ecutrho         = {hdr['ecutrho']:g}" if hdr.get("ecutrho") else None,
         f"    tot_charge      = {(hdr['tot_charge'] if tot_charge is None else tot_charge):.1f}",
         "    occupations     = 'smearing'", f"    smearing        = '{hdr['smearing']}'",
         f"    degauss         = {(hdr['degauss'] if degauss is None else degauss):g}", "/",
         "&ELECTRONS", f"    conv_thr        = {hdr['conv_thr']}",
         f"    mixing_beta     = {hdr['mixing_beta']}", "    electron_maxstep = 200", "/",
         "", "ATOMIC_SPECIES"]
    L = [x for x in L if x is not None]
    for e, m_, u in sp:
        L.append(f"  {e:3s} {m_}  {u}")
    L += ["", "ATOMIC_POSITIONS angstrom"]
    for s, p in rows:
        L.append(f"  {s:3s} %16.10f %16.10f %16.10f" % tuple(p))
    L += ["", f"K_POINTS {hdr['kpts'][0]}", "  " + hdr["kpts"][1], "", "CELL_PARAMETERS angstrom"]
    for v in hdr["cell"]:
        L.append("  %16.10f %16.10f %16.10f" % tuple(v))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")
    return None


def read_neb_images(d, tag):
    """`<tag>.xyz`(전 이미지) + `<tag>.dat`(에너지 프로파일) → (frames, energies, err)

    ⛔ 못 하는 것: 이미지 수가 두 파일에서 다르면 **짝을 맞추지 않고 거부한다**
      (엉뚱한 이미지를 안장으로 고르면 그 뒤가 전부 틀린다).
    """
    xp, dp = os.path.join(d, f"{tag}.xyz"), os.path.join(d, f"{tag}.dat")
    if not os.path.isfile(xp):
        return None, None, f"⛔ 없음: {xp}"
    frames, lines = [], open(xp, encoding="utf-8", errors="replace").read().splitlines()
    i = 0
    while i < len(lines):
        try:
            n = int(lines[i].split()[0])
        except (ValueError, IndexError):
            i += 1
            continue
        rows = []
        for l in lines[i + 2:i + 2 + n]:
            p = l.split()
            if len(p) >= 4 and re.match(r"^[A-Z][a-z]?$", p[0]):
                rows.append((p[0], [float(x) for x in p[1:4]]))
        if len(rows) == n:
            frames.append(rows)
        i += 2 + n
    if not frames:
        return None, None, f"⛔ {xp} 에서 이미지를 못 읽었다"
    en = []
    if os.path.isfile(dp):
        for l in open(dp, encoding="utf-8", errors="replace"):
            p = l.split()
            if len(p) >= 2:
                try:
                    en.append(float(p[1]))
                except ValueError:
                    pass
    if en and len(en) != len(frames):
        return None, None, (f"⛔ 이미지 수 불일치: {tag}.xyz {len(frames)}개 · "
                            f"{tag}.dat {len(en)}개 — 짝을 못 맞춘다")
    return frames, (en or None), None


def hop_center(fr, la, cell):
    """반전 중심 = **두 끝점 사이에서** 제일 많이 다른 원자의 중점. → (hop, ctr, dif)

    ⛔ 이걸 함수로 뽑은 이유(2026-08-27): bfgs_trace 가 중심을 `그 끝점 이완 중 최대 이동
      원자` 로 잡고 있었다. 그건 공공 이웃이지 뛰는 원자가 아니다 — 뛰는 Li 는 제 끝점
      안에서 0.03 Å 밖에 안 움직인다. 중심을 고르는 규약은 build_frozen·align_report 와
      **하나여야** 하고, 하나면 테스트할 수 있다.
    """
    nat = len(fr)
    dif = [min_image([la[i][1][k] - fr[i][1][k] for k in range(3)], cell) for i in range(nat)]
    hop = max(range(nat), key=lambda i: sum(x * x for x in dif[i]))
    return hop, [fr[hop][1][k] + dif[hop][k] / 2.0 for k in range(3)], dif


def bfgs_trace(work, tag, base_dirs=False):
    """P0-2 예비 진단 — 새 계산 없이 relax.out 궤적으로 물리/배회를 가른다."""
    import math as _m
    d = os.path.join(work, tag)
    cell = None
    rep, vec = {}, {}
    for nm in ("ep_initial", "ep_final"):
        ed = os.path.join(d, nm) if base_dirs else endpoint_dir(d, nm)
        p = os.path.join(ed, "relax.out")
        if not os.path.isfile(p):
            return 1, f"⛔ 없음: {p}"
        if cell is None:
            cell = parse_cell(os.path.join(ed, "relax.in"))
            if cell is None:
                return 1, "⛔ CELL_PARAMETERS 를 못 읽었다"
        t = open(p, encoding="utf-8", errors="replace").read()
        en = [float(x) for x in re.findall(r"!\s+total energy\s+=\s+([-\d.]+)\s+Ry", t)]
        fo = [float(x) for x in re.findall(r"Total force\s+=\s+([\d.eE+-]+)", t)]
        blocks = _all_pos_blocks(t)
        r = trace_report(blocks, cell, en, fo)
        if "error" in r:
            return 1, f"⛔ {nm}: {r['error']}"
        r["converged"] = "Begin final coordinates" in t
        r["max_steps_reached"] = "The maximum number of steps has been reached" in t
        r["dir"] = os.path.basename(ed)
        vec[nm] = r.pop("net_vector")
        rep[nm] = r
        rep[nm + "_final_rows"] = blocks[-1]

    A, B = rep["ep_initial"], rep["ep_final"]

    # ── 대칭 매핑을 넣은 코사인 (이게 옳은 비교다 — 위 inversion_match docstring 참조) ──
    fr, la = rep["ep_initial_final_rows"], rep["ep_final_final_rows"]
    # ⛔⛔ 2026-08-27 네 번째 버그 — 옛 판은 반전 중심을 `A["hop_index"]` 로 잡았다.
    #   그건 **그 끝점 이완 중에** 제일 많이 움직인 원자다(= 공공 이웃). **뛰는 원자가 아니다** —
    #   뛰는 Li 는 제 끝점 안에서 0.03 Å 밖에 안 움직인다. 엉뚱한 중심으로 반전을 걸었으니
    #   잔차가 클 수밖에 없었고, 그래서 스칼라가 소수 4자리까지 같은 ccpath 마저
    #   "대칭 등가가 아니다" 로 찍혔다 — **출력 안에서 모순이 났고 그게 신호였다.**
    #   → 중심은 **두 끝점 사이에서** 제일 많이 다른 원자의 중점이다 (build_frozen·
    #     align_report 와 같은 규약).
    hop, ctr, dif = hop_center(fr, la, cell)
    skip = {hop}          # 뛰는 원자만 뺀다 — 이완장 자체는 비교 대상이다
    cos_raw = mode_overlap(vec["ep_initial"], vec["ep_final"], skip)
    match, worst = inversion_match(fr, la, ctr, cell)
    cos_sym = (mode_overlap(vec["ep_initial"], vec["ep_final"], skip, match, -1.0)
               if match else None)
    # 잔차로 **읽는 강도**를 조절한다 (문턱으로 버리지 않는다 — inversion_match docstring)
    inv_ok = worst is not None and worst <= 0.5

    # ── 이완 스칼라 일치도: 대칭 등가면 두 끝점의 이완 **크기**가 같아야 한다 ────────
    # ⛔ 2026-08-27 자체수정 — 처음엔 **%만** 봤다. 그랬더니 cc333 `_r2` 가 순변위
    #   0.0641 vs 0.0723 Å 로 "12 % 어긋남 ⇒ 대칭 등가가 아니다" 로 찍혔는데,
    #   절대차는 **0.008 Å** 이다. 그건 어긋남이 아니라 잡음이다.
    #   작은 양의 백분율은 아무것도 뜻하지 않는다 — **절대 바닥을 같이 본다.**
    ABS_FLOOR_A, ABS_LOUD_A, ABS_FLOOR_EV = 0.02, 0.05, 0.010

    def _rel(x, y):
        m = (abs(x) + abs(y)) / 2.0
        return None if m < 1e-9 else round(abs(x - y) / m * 100, 2)
    dmax = abs(A["net_max_A"] - B["net_max_A"])
    dmed = abs(A["net_median_A"] - B["net_median_A"])
    dE = abs((A["energy_drop_eV"] or 0) - (B["energy_drop_eV"] or 0))
    scal = {"net_max_pct": _rel(A["net_max_A"], B["net_max_A"]),
            "net_median_pct": _rel(A["net_median_A"], B["net_median_A"]),
            "energy_drop_pct": _rel(A["energy_drop_eV"] or 0, B["energy_drop_eV"] or 0),
            "net_max_abs_A": round(dmax, 4), "net_median_abs_A": round(dmed, 4),
            "energy_drop_abs_eV": round(dE, 5)}
    pct_max = max([scal[k] for k in ("net_max_pct", "net_median_pct", "energy_drop_pct")
                   if scal[k] is not None], default=0.0)
    same = max(dmax, dmed) <= ABS_FLOOR_A and dE <= ABS_FLOOR_EV
    differ = (max(dmax, dmed) >= ABS_LOUD_A or dE > ABS_FLOOR_EV) and pct_max >= 5.0

    L = [f"■ 끝점 BFGS 궤적 진단 — {tag}"]
    for nm in ("ep_initial", "ep_final"):
        r = rep[nm]
        if r["dir"] != nm:
            L.append(f"   ⚠ **{r['dir']} 는 이어달리기다** — 아래 궤적은 그 구간뿐이고, "
                     f"앞 구간(`{nm}`)의 이동은 안 보인다. 앞 구간은 `--align_base` 로.")
        L += [f"   [{r['dir']}] {r['n_steps']}스텝 · 원자 {r['n_atoms']} · "
              f"{'수렴' if r['converged'] else '⛔ 미수렴' + (' (스텝 한도)' if r['max_steps_reached'] else '')}",
              f"      힘 {r['force_first_eVA']} → {r['force_last_eVA']} eV/Å · "
              f"E 낙차 {r['energy_drop_eV']} eV (마지막 3스텝 {r['energy_tail3_eV']})",
              f"      홉 제외 순변위 최대 {r['net_max_A']} · 중앙 {r['net_median_A']} Å",
              f"      **배회지수 {r['wander_index']}** (경로합/순변위합 · 1=곧게, 클수록 왔다갔다)",
              f"      마지막 3스텝 이동량 {r['tail3_move_A']} Å"]
    L.append("")
    L.append(f"   ★ 이완 **스칼라 일치도** (대칭 등가면 두 끝점의 이완 크기가 같아야 한다):")
    L.append(f"      순변위 최대 Δ{scal['net_max_abs_A']} Å ({scal['net_max_pct']}%) · "
             f"중앙 Δ{scal['net_median_abs_A']} Å ({scal['net_median_pct']}%) · "
             f"E 낙차 Δ{scal['energy_drop_abs_eV']} eV ({scal['energy_drop_pct']}%)")
    if same:
        L.append(f"      ⇒ ✅ 사실상 **동일**하다 (절대차가 {ABS_FLOOR_A} Å·"
                 f"{ABS_FLOOR_EV} eV 안) — 두 끝점이 실제로 대칭 등가고, 이완은 "
                 "**재현되는 물리적 응답**이다 (배회가 아니다).")
    elif differ:
        L.append(f"      ⇒ ⛔ **어긋난다** (절대차 {max(dmax, dmed):.3f} Å · {pct_max}%) — "
                 "두 끝점이 대칭 등가가 아니다. 각자 **다른 국소 최소**로 들어갔다는 뜻이다. "
                 "끝점 ΔE 가 작다는 것만으로 대칭 등가라고 부른 것을 재검토할 것.")
    else:
        L.append(f"      ⇒ 중간 — 어느 쪽도 주장하지 않는다. "
                 f"(⚠ % 가 커 보여도 **절대차가 {max(dmax, dmed):.3f} Å 뿐**이면 그건 "
                 f"어긋남이 아니라 잡음이다 — 작은 양의 백분율은 뜻이 없다.)")

    L.append("")
    L.append(f"   ★ 모드 일치도 — raw {cos_raw} · **대칭매핑 {cos_sym}** "
             f"(반전 잔차 {None if worst is None else round(worst, 3)} Å · "
             f"중심 = 끝점 간 최대차 원자 #{hop} {fr[hop][0]} "
             f"{_m.sqrt(sum(x*x for x in dif[hop])):.3f} Å 의 중점)")
    L.append("      ⚠ **raw 코사인은 여기서 뜻이 없다.** 대칭 등가면 두 변위장은 *같은* 게 아니라 "
             "**대칭 연산으로 관계**돼 있어서, 같은 index 로 재면 서로 다른 자리를 비교하게 된다 "
             "— 0 근처가 정상이다. 볼 것은 **대칭매핑** 쪽이다.")
    if cos_sym is None:
        L.append("      ⇒ 반전 대응 자체를 못 만들었다 (원소 개수 불일치).")
    elif not inv_ok:
        L.append(f"      ⇒ ⛔ **반전 잔차가 {worst:.2f} Å 로 크다** — 두 끝점이 애초에 반전으로 "
                 f"안 겹친다. 즉 **대칭 등가가 아니다.** 이 경우 대칭매핑 코사인 "
                 f"({cos_sym}) 도 참고값일 뿐이다. 위 **스칼라 일치도**를 먼저 볼 것.")
    elif cos_sym >= 0.7:
        L.append("      ⇒ ✅ 두 이완이 **반전으로 겹친다** = 같은 물리적 응답이다.")
    elif cos_sym <= 0.3:
        L.append("      ⇒ ⛔ 반전으로도 안 겹친다 — 공유 응답의 증거가 없다.")
    else:
        L.append("      ⇒ 중간.")

    w = [rep[n]["wander_index"] for n in ("ep_initial", "ep_final") if rep[n]["wander_index"]]
    if w and max(w) >= 2.0:
        L.append(f"   ⚠ 배회지수 최대 {max(w)} — 경로가 순변위의 2배 넘게 길다. 곧은 이완이 아니다.")
    elif w:
        L.append(f"   ✔ 배회지수 최대 {max(w)} — 두 끝점 다 대체로 곧게 갔다 "
                 f"(느린 이완이지 배회가 아니다).")
    L.append("")
    L.append("   ⛔ 이 진단이 못 하는 것: 곧게 갔다고 **옳은 방향**이라는 보증은 없다 · "
             "스텝 간 회전은 안 뺀다 · 반전 말고 다른 대칭 연산은 안 본다 · "
             "**이 폴더의 이완 구간만** 본다 (이어달리기면 앞 구간은 안 보인다 — `--align_base`) · "
             "이것만으로 P0-2 를 닫지 못한다 (pristine rattle 이 본 검사다).")
    op = os.path.join(d, "bfgs_trace.json")
    try:
        for k in ("ep_initial_final_rows", "ep_final_final_rows"):
            rep.pop(k, None)
        json.dump({"tag": tag, "hop_between_endpoints": hop,
                   "hop_between_endpoints_A": round(_m.sqrt(sum(x*x for x in dif[hop])), 4),
                   "mode_overlap_cos_raw": cos_raw,
                   "mode_overlap_cos_symmetry_mapped": cos_sym,
                   "inversion_residual_A": None if worst is None else round(worst, 4),
                   "relax_scalar_mismatch_pct": scal,
                   "endpoints": rep}, open(op, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        L.append(f"   → {op}")
    except OSError:
        pass
    return 0, "\n".join(L)


def selftest_trace():
    """궤적 진단 selftest — 음성 경로(배회)가 핵심이다."""
    import math as _m
    ok = True

    def chk(c, m):
        nonlocal ok
        ok &= bool(c)
        _p(f"  {_OK if c else _NG} {m}")

    A, N = 5.19, 3
    cell = [[A * N, 0, 0], [0, A * N, 0], [0, 0, A * N]]
    base = [("Nd", [i * A, j * A, k * A]) for i in range(N) for j in range(N) for k in range(N)]
    base += [("Li", [i * A + A / 2, j * A, k * A])
             for i in range(N) for j in range(N) for k in range(N)]
    nat = len(base)

    def mode(i):                      # 결정론적 '모드' 방향
        v = [_m.sin(i * 1.7), _m.cos(i * 2.3), _m.sin(i * 3.1)]
        n = _m.sqrt(sum(x * x for x in v)) or 1.0
        return [x / n for x in v]

    def steps_straight(nst=8, amp=1.2):        # 한 방향으로 곧게
        return [[(s, [p[k] + mode(i)[k] * amp * t / (nst - 1) for k in range(3)])
                 for i, (s, p) in enumerate(base)] for t in range(nst)]

    def steps_wander(nst=8, amp=0.4, ph=0.0, off=7):  # 왔다갔다 (순변위 작고 경로 길다)
        return [[(s, [p[k] + mode(i + off)[k] * amp * _m.sin(t * 1.9 + ph) for k in range(3)])
                 for i, (s, p) in enumerate(base)] for t in range(nst)]

    r = trace_report(steps_straight(), cell)
    chk(r["wander_index"] is not None and r["wander_index"] < 1.2,
        f"[궤적·양성] 곧은 이완의 배회지수 ≈ 1 ({r['wander_index']})")
    r2 = trace_report(steps_wander(), cell)
    chk(r2["wander_index"] >= 2.0,
        f"[궤적·음성] 배회하면 배회지수가 커진다 ({r2['wander_index']})")

    a = trace_report(steps_straight(), cell)["net_vector"]
    b = trace_report(steps_straight(), cell)["net_vector"]
    chk(abs(mode_overlap(a, b) or 0) >= 0.99, "[궤적·양성] 같은 모드면 코사인 ≈ 1")
    # ★ 음성 핵심: 두 계산이 **다른 방향**으로 배회하면 코사인이 안 선다.
    #   (같은 방향으로 배회하면 코사인은 높게 나오고, 그건 오판이 아니다 —
    #    "공유된 무른 방향이 있다" 는 뜻이라 우리가 찾는 바로 그 신호다.)
    c = trace_report(steps_wander(off=7), cell)["net_vector"]
    e = trace_report(steps_wander(off=31, ph=2.1), cell)["net_vector"]
    chk(abs(mode_overlap(c, e) or 1) <= 0.3,
        f"[궤적·음성] 방향이 다른 배회는 코사인이 안 선다 ({mode_overlap(c, e)})")

    # ★★ 2026-08-27 실측 회귀 — **대칭 등가 쌍은 raw 코사인이 0 근처가 정상이다.**
    #   ccpath 두 끝점의 이완 스칼라가 소수 4자리까지 같은데 raw 코사인은 0.018 이었다.
    #   그걸 '배회' 로 읽으면 정반대 결론이 난다. 대칭매핑을 넣어야 1 이 나온다.
    #   (a) 매처가 **목록 순서가 섞여도** 반전 짝을 찾아내는가
    ctr_t = [A * N / 2.0] * 3
    inv = [(s, [2 * ctr_t[k] - p[k] for k in range(3)]) for s, p in base]
    order = list(range(len(base)))
    for st in ("Nd", "Li"):                       # 원소 안에서 순서를 뒤집는다 (비자명 순열)
        g = [i for i in order if base[i][0] == st]
        for a_, b_ in zip(g, reversed(g)):
            order[a_] = b_
    shuf = [inv[order[i]] for i in range(len(inv))]
    m_inv, w_inv = inversion_match(base, shuf, ctr_t, cell)
    chk(m_inv is not None and w_inv < 1e-6 and any(m_inv[i] != i for i in m_inv),
        f"[궤적·대칭] 목록이 섞여도 반전 짝을 찾는다 (잔차 "
        f"{None if w_inv is None else round(w_inv, 6)}, 비자명 순열)")

    #   (b) 반전으로 관계된 변위장: **raw 는 낮고 대칭매핑은 1** 이어야 한다
    dA = [mode(i) for i in range(nat)]
    dB = [None] * nat
    for i, j in m_inv.items():
        dB[j] = [-x for x in dA[i]]
    chk((mode_overlap(dA, dB, (), m_inv, -1.0) or 0) >= 0.99,
        "[궤적·대칭] 반전으로 관계된 변위장은 **대칭매핑 코사인 ≈ 1**")
    raw = abs(mode_overlap(dA, dB) or 1)
    chk(raw <= 0.5,
        f"[궤적·대칭·실측회귀] 같은 쌍의 **raw 코사인은 낮다** ({raw:.3f}) — "
        f"raw 를 '배회' 로 읽으면 안 된다")

    # ★★★ 실측회귀 (2026-08-27) — **반전 중심을 어디서 잡는가.**
    #   옛 판은 `그 끝점 이완 중 최대 이동 원자` 를 썼다(= 공공 이웃). 그래서 스칼라가
    #   소수 4자리까지 같은 ccpath 마저 "대칭 등가 아님" 이 나왔다. 여기서는 **진짜로
    #   반전 대칭인 한 쌍**을 만들어, 중심을 옳게 잡으면 잔차가 0 에 붙는지 본다.
    aC, bC = 3.0, 4                                   # 단일 원소 단순입방 (반전 대칭이 자명)
    cellC = [[aC * bC, 0, 0], [0, aC * bC, 0], [0, 0, aC * bC]]
    site = [(x * aC, y * aC, z * aC) for x in range(bC) for y in range(bC) for z in range(bC)]
    M = [aC / 2, 0.0, 0.0]                            # (0,0,0) 과 (a,0,0) 의 중점
    def _key(p):
        return tuple(round(v % (aC * bC), 6) for v in p)
    idx = {_key(p): i for i, p in enumerate(site)}
    Q = [idx[_key([2 * M[k] - p[k] for k in range(3)])] for p in site]  # 반전이 만드는 자리 치환
    u = [[x * 0.12 for x in mode(i * 3 + 1)] for i in range(len(site))]  # 임의 이완장
    A_i, B_i = idx[_key((0.0, 0.0, 0.0))], idx[_key((aC, 0.0, 0.0))]
    # ⚠ 두 끝점의 **원자 목록이 같아야** 한다 (같은 index = 같은 원자). 그래서 공통 원자
    #   + 맨 뒤에 '뛰는 원자' 하나로 만든다. 자리를 하나씩 빼며 만들면 목록이 어긋난다.
    common = [i for i in range(len(site)) if i not in (A_i, B_i)]
    first_s = [("Li", [site[i][k] + u[i][k] for k in range(3)]) for i in common]
    #   최종은 초기의 **반전상**: 자리 q 에 앉은 원자는 −u(2M−q) 만큼 밀린다
    last_s = [("Li", [site[i][k] - u[Q[i]][k] for k in range(3)]) for i in common]
    first_s.append(("Li", [site[A_i][k] + u[A_i][k] for k in range(3)]))   # 뛰는 원자: A → B
    last_s.append(("Li", [site[B_i][k] - u[A_i][k] for k in range(3)]))
    hopC, ctrC, _d = hop_center(first_s, last_s, cellC)
    _mm2, wC = inversion_match(first_s, last_s, ctrC, cellC)
    chk(wC is not None and wC < 0.05,
        f"[궤적·중심·실측회귀] 진짜 반전쌍이면 잔차가 0 에 붙는다 ({wC})")
    ctr_bad = [first_s[0][1][k] for k in range(3)]    # 엉뚱한 중심(옛 버그의 모양)
    _mm3, wBad = inversion_match(first_s, last_s, ctr_bad, cellC)
    chk(wBad is not None and wBad > 5 * (wC or 1e-9) and wBad > 0.5,
        f"[궤적·중심·음성] 중심을 잘못 잡으면 잔차가 커진다 ({wBad:.2f} vs {wC:.3f}) "
        f"— 잔차는 **중심 선택도** 재고 있다")
    chk(abs(mode_overlap(a, [[0.0, 0.0, 0.0]] * nat) or 1) if False else
        mode_overlap(a, [[0.0, 0.0, 0.0]] * nat) is None,
        "[궤적·가드] 영벡터면 코사인을 계산하지 않는다")
    chk("error" in trace_report([base], cell), "[궤적·가드] 블록 1개면 궤적이 아니라고 말한다")
    chk("error" in trace_report([base, base[:-1]], cell), "[궤적·가드] 원자 수가 다르면 거부")
    return ok


def smear_ladder(work, tag, ladder=SMEAR_LADDER_RY):
    """① smearing 사다리 입력 — **고정 기하**로 끝점·안장을 각 degauss 에서 SCF.

    ⛔ 이 검사가 **못 하는 것** (먼저 읽을 것)
      · 기하는 `degauss = 0.02` 에서 최적화된 것이다. degauss 를 바꾸면 최적 기하도
        조금 바뀌는데 **여기서는 안 바꾼다.** 즉 이건 *고정 기하 민감도*이고,
        이완까지 다시 한 값이 아니다. 이게 크게 흔들리면 그때 이완을 다시 한다.
      · k-point 는 그대로 둔다. smearing 과 k 는 짝으로 수렴하는 양이라, 이 사다리만으로
        "수렴했다" 고 말할 수 없다 — **"안 흔들린다" 까지**다.
      · 안장은 NEB 가 준 최고에너지 이미지다. CI 를 안 켰으면 격자에 걸린 값이다.
    """
    d = os.path.join(work, tag)
    hdr, err = parse_qe_header(os.path.join(d, "neb.in"))
    if hdr is None:
        return 1, err
    frames, en, ferr = read_neb_images(d, tag)
    if frames is None:
        return 1, ferr
    if en is None:
        return 1, (f"⛔ {tag}.dat 이 없어 **어느 이미지가 안장인지 못 고른다.** "
                   f"임의로 고르면 그 뒤가 전부 틀린다 — 거부한다.")
    isad = max(range(len(en)), key=lambda i: en[i])
    if isad in (0, len(en) - 1):
        return 1, (f"⛔ 최고에너지가 **끝점**(image {isad+1})이다 — 경로가 단조라 "
                   f"안장이 없다. 이 상태로 장벽 민감도를 재는 것은 뜻이 없다.")
    picks = [("ep_initial", frames[0]), ("saddle", frames[isad]), ("ep_final", frames[-1])]
    out = os.path.join(d, "smear_ladder")
    made = []
    for g in ladder:
        gt = f"{g:g}".replace(".", "p")
        for nm, rows in picks:
            p = os.path.join(out, f"g{gt}", nm, "scf.in")
            e = write_scf(p, f"{tag}_{nm}_g{gt}", hdr, rows, degauss=g)
            if e:
                return 1, e
            made.append(p)
    meta = {"tag": tag, "why": "kb 2026-08-11 등록 선행조건 + 회신 I N5",
            "protocol_sha256": hdr["src_sha256"], "upf_sha256": hdr["upf_sha256"],
            "src_sha256": {f: _sha(os.path.join(d, f))
                           for f in (f"{tag}.xyz", f"{tag}.dat", "neb.in")},
            "ladder_Ry": list(ladder), "protocol_source": hdr["src"],
            "degauss_of_run_Ry": hdr["degauss"], "n_images": len(frames),
            "saddle_image_1based": isad + 1,
            "profile_eV": en,
            "barrier_of_run_eV": round(max(en) - en[0], 6),
            "fixed_geometry": True,
            "⛔_한계": ["기하는 0.02 에서 최적화된 것 — 이완을 다시 하지 않는다",
                      "k-point 고정 — smearing 과 k 는 짝이라 '수렴' 은 못 말한다",
                      "안장은 NEB 최고에너지 이미지 (CI 안 켰으면 격자에 걸린 값)"]}
    json.dump(meta, open(os.path.join(out, "meta.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    L = [f"■ smearing 사다리 입력 — {tag}",
         f"   프로토콜 출처: {hdr['src']} (degauss {hdr['degauss']:g} Ry · "
         f"{hdr['smearing']} · q {hdr['tot_charge']:.1f} · k {hdr['kpts'][1]})",
         f"   이미지 {len(frames)}개 · **안장 = image {isad+1}** · "
         f"런의 장벽 {max(en)-en[0]:.4f} eV",
         f"   만든 입력 {len(made)}개 → {out}/g<degauss>/{{ep_initial,saddle,ep_final}}/scf.in",
         "",
         "   돌리는 법 (한 폴더씩, 같은 셸에서):",
         f"     for G in {out}/g*; do for S in ep_initial saddle ep_final; do",
         "       ( cd \"$G/$S\" && $MPIRUN -np 1 --oversubscribe $PW -in scf.in > scf.out 2>&1 )",
         "     done; done",
         "",
         f"   읽는 법:  python3 tools/sei/symmetric_saddle.py --work {work} --tag {tag} --collect_ladder",
         "",
         "   ⛔ 못 하는 것: 고정 기하다(이완 다시 안 함) · k 고정 · 안장은 NEB 최고 이미지."]
    return 0, "\n".join(L)


def collect_ladder(work, tag):
    """① 사다리 회수 — **fail-closed.** 설정한 전 점이 갖춰지지 않으면 판정하지 않는다.

    ⛔ 2026-08-27 (리뷰 J · P0-1) — 옛 판은 일부 degauss 만 있어도 판정하고 **rc=0 으로
      성공 종료**했다. 그러면 "3점 사다리" 라고 적힌 결과가 실제로는 2점일 수 있고,
      화면만 보고는 그걸 모른다. 빠진 게 하나라도 있으면 **거부한다.**
    """
    d = os.path.join(work, tag, "smear_ladder")
    mp = os.path.join(d, "meta.json")
    if not os.path.isfile(mp):
        return 1, f"⛔ 없음: {mp} — 먼저 --smear_ladder 로 입력을 만들 것"
    meta = json.load(open(mp, encoding="utf-8"))
    NEED = ("ep_initial", "saddle", "ep_final")
    rows, miss, bad = [], [], []
    for g in meta["ladder_Ry"]:
        gt = f"{g:g}".replace(".", "p")
        e, f_ = {}, {}
        for nm in NEED:
            op = os.path.join(d, f"g{gt}", nm, "scf.out")
            if not os.path.isfile(op):
                miss.append(f"g{gt}/{nm}")
                continue
            t = open(op, encoding="utf-8", errors="replace").read()
            if "JOB DONE" not in t:
                miss.append(f"g{gt}/{nm}(미완료)")
                continue
            if re.search(r"convergence NOT achieved", t):
                bad.append(f"g{gt}/{nm}(SCF 미수렴)")
                continue
            m = re.findall(r"!\s+total energy\s+=\s+([-\d.]+)\s+Ry", t)
            if not m:
                bad.append(f"g{gt}/{nm}(에너지 없음)")
                continue
            e[nm] = float(m[-1]) * RY_EV
            fm = re.findall(r"Total force\s+=\s+([\d.eE+-]+)", t)
            f_[nm] = float(fm[-1]) * RYAU_EVA if fm else None
        if len(e) == 3:
            rows.append({"degauss_Ry": g,
                         # 리뷰 J: 양쪽에서 따로 판정하고 endpoint splitting 을 기록한다
                         "barrier_fwd_eV": round(e["saddle"] - e["ep_initial"], 5),
                         "barrier_rev_eV": round(e["saddle"] - e["ep_final"], 5),
                         "endpoint_split_meV": round((e["ep_final"] - e["ep_initial"]) * 1000, 2),
                         "force_eVA": {k: (None if v is None else round(v, 4))
                                       for k, v in f_.items()}})
    L = [f"■ smearing 사다리 — {tag}  (고정 기하)"]
    if miss or bad:
        L += [f"   ⏳ 없는 점 {len(miss)}: {', '.join(miss[:6])}" + (" …" if len(miss) > 6 else "")]
        if bad:
            L.append(f"   ⛔ 못 쓰는 점 {len(bad)}: {', '.join(bad[:6])}")
        L.append("   ⇒ **판정하지 않는다.** 설정한 전 점이 갖춰져야 사다리다 "
                 "(일부만으로 판정하면 몇 점짜리인지 화면에서 안 보인다 — 리뷰 J P0-1).")
        return 1, "\n".join(L)
    if not rows:
        return 1, "\n".join(L + ["   ⛔ 회수할 결과가 없다"])

    # 힘 게이트 — 고정 기하가 각 degauss 에서도 정류점 근처인가
    FMAX = 0.05
    hot = [(r["degauss_Ry"], k, v) for r in rows for k, v in r["force_eVA"].items()
           if v is not None and v > FMAX]
    L.append("   degauss   장벽(정) [eV]  장벽(역) [eV]  끝점 split [meV]   |F| max [eV/Å]")
    for r in rows:
        fv = [v for v in r["force_eVA"].values() if v is not None]
        L.append(f"     {r['degauss_Ry']:<8g} {r['barrier_fwd_eV']:<14.4f} "
                 f"{r['barrier_rev_eV']:<14.4f} {r['endpoint_split_meV']:<16.2f} "
                 f"{(max(fv) if fv else float('nan')):.3f}")
    out = {"tag": tag, "rows": rows, "fixed_geometry": True}
    verdict = []
    for key, nm in (("barrier_fwd_eV", "정방향"), ("barrier_rev_eV", "역방향")):
        b = [r[key] for r in rows]
        spread = (max(b) - min(b)) * 1000
        last = abs(b[-1] - b[-2]) * 1000 if len(b) >= 2 else None
        # ⛔ 리뷰 J3 — 문턱을 조인다. 18/36 은 **rate 영향 등급**이지 수치수렴 문턱이 아니다.
        if spread <= 5:
            v = f"✅ 수치적으로 안정 (범위 {spread:.1f} meV ≤ 5)"
        elif spread <= 18:
            v = f"⚠ 민감도 경고 ({spread:.1f} meV) — 인용 시 명시"
        elif spread <= 36:
            v = f"⛔ **300 K 장벽 인용 불가** ({spread:.1f} meV) · 600 K 정성 해석만 조건부"
        else:
            v = f"⛔⛔ **NO-GO** ({spread:.1f} meV > 36) — degauss 내리고 **이완부터 다시**"
        verdict.append((nm, spread, last, v))
        out[key + "_spread_meV"] = round(spread, 2)
    L.append("")
    for nm, spread, last, v in verdict:
        L.append(f"   ★ {nm} 장벽 범위 **{spread:.1f} meV** → {v}")
        if last is not None:
            L.append(f"      마지막 두 degauss 차이 {last:.1f} meV "
                     f"(수렴이면 이게 범위보다 작아야 한다)")
    if hot:
        L.append(f"   ⛔ 잔류력이 {FMAX} eV/Å 를 넘는 점 {len(hot)}개: "
                 + ", ".join(f"g{g:g}/{k} {v:.3f}" for g, k, v in hot[:4]))
        L.append("      ⇒ 고정 기하가 그 degauss 에서 정류점이 아니다 — **경로를 다시 이완**해야 한다.")
    L += ["", "   ⛔ `max−min` 은 **관측 범위이지 오차상한이 아니다** (리뷰 J3).",
          "      이 사다리는 *3×3×3 k-grid 에서, degauss 0.02 로 찾은 고정 경로*의 민감도까지다 —",
          "      relaxed barrier 도 k 수렴도 증명하지 않는다. dense-k corner check 가 따로 필요하다."]
    json.dump(out, open(os.path.join(d, "ladder_result.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    return 0, "\n".join(L)


def mode_scan(work, tag, lambdas=MODE_SCAN_LAMBDAS):
    """② pristine ±δ — 공공을 **메운** 셀을 관측한 이완 모드로 밀어 E(λ) 를 본다.

    만드는 법
      · 완전 격자 = 갓 지은 `ep_initial` (107) + 뛰는 원자의 `ep_final` 자리 (= 공공 자리).
        두 끝점의 합집합이 Li 부격자 전체다 — 격자를 다시 짓지 않는다.
      · 모드 u = (이완 ep_initial) − (갓 지은 ep_initial), 메운 원자는 u = 0.
      · 스캔 = 완전 격자 + λ·u.

    ⛔ **못 하는 것**
      · **모드 하나만** 본다. 다른 방향의 soft mode 는 이 검사가 못 본다 —
        음성이 나와도 "이 모드로는 안정" 까지다.
      · 조성이 바뀐다(공공 없음) → **NEB 끝점 에너지와 직접 비교 금지.** λ 끼리만 비교한다.
      · 전하는 중성으로 강제한다(공공이 없으니 q=0 이 자연스럽다).
      · 이완이 아니라 single point 다. λ=0 이 최소여도 **다른 기하가 더 낮을 수** 있다.
    """
    d = os.path.join(work, tag)
    ini_d, fin_d = endpoint_dir(d, "ep_initial"), endpoint_dir(d, "ep_final")
    base_i, base_f = os.path.join(d, "ep_initial"), os.path.join(d, "ep_final")
    built_i = parse_input_positions(os.path.join(base_i, "relax.in")) \
        if os.path.isfile(os.path.join(base_i, "relax.in")) else None
    built_f = parse_input_positions(os.path.join(base_f, "relax.in")) \
        if os.path.isfile(os.path.join(base_f, "relax.in")) else None
    if not built_i or not built_f:
        return 1, f"⛔ 갓 지은 끝점을 못 읽었다: {base_i}/relax.in · {base_f}/relax.in"
    rel_i, err, info = read_relaxed(os.path.join(ini_d, "relax.out"), allow_unconverged=True)
    if rel_i is None:
        return 1, f"⛔ ep_initial 이완 좌표: {err}"
    if len(rel_i) != len(built_i):
        return 1, "⛔ 갓 지은 것과 이완본의 원자 수가 다르다"
    cell = parse_cell(os.path.join(base_i, "relax.in"))
    hdr, herr = parse_qe_header(os.path.join(base_i, "relax.in"))
    if cell is None or hdr is None:
        return 1, herr or "⛔ CELL_PARAMETERS 를 못 읽었다"

    hop, _ctr, dif = hop_center(built_i, built_f, cell)
    vac = built_f[hop]                       # 뛰는 원자의 도착 자리 = ep_initial 의 공공 자리
    import math as _m
    # ⛔ 리뷰 J2 — **전역 병진 성분을 먼저 뺀다.** 안 빼면 스캔이 셀 전체를 밀고,
    #   그건 에너지가 변하지 않는 방향이라 곡률을 희석한다(그리고 λ 축의 뜻이 흐려진다).
    tshift, tconv = _optimal_pbc_translation(built_i, rel_i, cell)
    u = [min_image([rel_i[i][1][k] - built_i[i][1][k] - tshift[k] for k in range(3)], cell)
         for i in range(len(built_i))]
    umax = max(_m.sqrt(sum(x * x for x in v)) for v in u)
    ideal = [(s, list(p)) for s, p in built_i] + [(vac[0], list(vac[1]))]
    u.append([0.0, 0.0, 0.0])                # 메운 원자는 안 민다 (완전 격자의 제자리다)

    # ── preflight (리뷰 J P0) — 완전 격자가 진짜 완전한가. 틀리면 전 λ 가 무의미하다 ──
    comp = {}
    for sym, _q in ideal:
        comp[sym] = comp.get(sym, 0) + 1
    pf, warn = {"composition": comp, "n_atoms": len(ideal)}, []
    dmin, dpair = 1e9, None
    for i in range(len(ideal)):
        for j in range(i + 1, len(ideal)):
            dd = min_image([ideal[j][1][k] - ideal[i][1][k] for k in range(3)], cell)
            n = _m.sqrt(sum(x * x for x in dd))
            if n < dmin:
                dmin, dpair = n, (i, j)
    pf["min_distance_A"] = round(dmin, 4)
    pf["min_distance_pair"] = dpair
    if dmin < 1.5:
        warn.append(f"⛔ 최소 원자간 거리 {dmin:.3f} Å < 1.5 — 중복 좌표이거나 자리가 겹쳤다")
    # 메운 Li 가 **이상 격자자리**인가: 나머지 Li 들이 만드는 최근접 거리 분포와 같은가
    li = [i for i, (sym, _q) in enumerate(ideal) if sym == "Li"]
    def _nn(i, pool):
        return min(_m.sqrt(sum(x * x for x in min_image(
            [ideal[j][1][k] - ideal[i][1][k] for k in range(3)], cell)))
            for j in pool if j != i)
    if len(li) > 3:
        nn_fill = _nn(len(ideal) - 1, li)
        others = sorted(_nn(i, li) for i in li[:-1])
        med = others[len(others) // 2]
        pf["filled_nn_A"], pf["li_nn_median_A"] = round(nn_fill, 4), round(med, 4)
        if abs(nn_fill - med) > 0.35:
            warn.append(f"⛔ 메운 Li 의 최근접 {nn_fill:.3f} Å 이 나머지 Li 중앙값 "
                        f"{med:.3f} 와 {abs(nn_fill-med):.3f} Å 어긋난다 — 이상 격자자리가 아니다")
    if not tconv:
        warn.append("⚠ 병진 제거가 수렴하지 않았다")
    if warn:
        return 1, ("⛔ preflight 실패 — 완전 격자가 성립하지 않는다:\n   "
                   + "\n   ".join(warn)
                   + f"\n   (조성 {comp} · 원자 {len(ideal)} · 최소거리 {dmin:.3f} Å)\n"
                   + "   이걸 무시하고 돌리면 **전 λ 가 무의미**하다.")

    out = os.path.join(d, "mode_scan")
    made = []
    for lam in lambdas:
        lt = f"{lam:+.2f}".replace(".", "p").replace("+", "p").replace("-", "m")
        rows = [(ideal[i][0], [ideal[i][1][k] + lam * u[i][k] for k in range(3)])
                for i in range(len(ideal))]
        p = os.path.join(out, f"lam{lt}", "scf.in")
        e = write_scf(p, f"{tag}_pristine_{lt}", hdr, rows, tot_charge=0.0)
        if e:
            return 1, e
        made.append(p)
    meta = {"tag": tag, "why": "회신 I P0-2 의 싼 판 — pristine 이 이 모드로 불안정한가",
            "preflight": pf,
            "translation_removed_A": round(_m.sqrt(sum(x*x for x in tshift)), 4),
            "protocol_sha256": hdr["src_sha256"], "upf_sha256": hdr["upf_sha256"],
            "lambdas": list(lambdas), "n_atoms_pristine": len(ideal),
            "n_atoms_vacancy_cell": len(built_i),
            "mode_source": os.path.join(ini_d, "relax.out"),
            "mode_converged": info.get("converged"),
            "mode_max_A": round(umax, 4),
            "filled_site_from": f"ep_final atom #{hop} ({vac[0]})",
            "tot_charge": 0.0, "protocol_source": hdr["src"],
            "⛔_한계": ["메운 Li 의 u=0 은 **임의의 mode completion** 이다 — 음성 결과는 "
                      "더 약한 결론만 허용한다 (리뷰 J2)",
                      "모드 하나만 본다 — 음성이어도 '이 모드로는 안정' 까지다",
                      "조성이 다르다(공공 없음) — NEB 끝점 에너지와 직접 비교 금지",
                      "single point 다 — λ=0 최소여도 다른 기하가 더 낮을 수 있다"]}
    json.dump(meta, open(os.path.join(out, "meta.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    L = [f"■ pristine 모드 스캔 입력 — {tag}",
         f"   완전 격자 {len(ideal)}원자 (공공셀 {len(built_i)} + 메운 자리 1) · "
         f"조성 {''.join(f'{k}{v}' for k, v in sorted(comp.items()))}",
         f"   preflight ✅ 최소거리 {dmin:.3f} Å · 메운 Li 최근접 "
         f"{pf.get('filled_nn_A')} (나머지 중앙값 {pf.get('li_nn_median_A')})",
         f"   전역 병진 {meta['translation_removed_A']} Å 제거",
         f"   모드: {os.path.basename(ini_d)}/relax.out 의 이완 변위 "
         f"(최대 {umax:.3f} Å · {'수렴' if info.get('converged') else '⛔ 미수렴'})",
         f"   λ = {', '.join(f'{x:+g}' for x in lambdas)} · 전하 중성(q=0)",
         f"   만든 입력 {len(made)}개 → {out}/lam*/scf.in",
         "",
         "   돌리는 법:",
         f"     for S in {out}/lam*; do",
         "       ( cd \"$S\" && $MPIRUN -np 1 --oversubscribe $PW -in scf.in > scf.out 2>&1 )",
         "     done",
         "",
         f"   읽는 법:  python3 tools/sei/symmetric_saddle.py --work {work} --tag {tag} --collect_scan",
         "",
         "   ⛔ 모드 하나만 본다 · 조성이 달라 NEB 끝점과 직접 비교 금지 · single point 다."]
    return 0, "\n".join(L)


def collect_scan(work, tag):
    """② 모드 스캔 회수 — **곡률 부호**로 판정한다. fail-closed.

    ⛔ 2026-08-27 (리뷰 J · P0-2) — 옛 판은 λ=0 **하나만** 있어도 "λ=0 이 최소" 라고
      찍고 rc=0 을 냈다. 점 하나로 최소를 주장한 것이다. 이제 설정한 전 λ 가 없으면 거부한다.

    ⛔ 리뷰 J2 — 판정 기준도 바꾼다. *"어느 λ 가 가장 낮은가"* 가 아니라 **짝수부**

        Δ_even(a) = [E(+a) + E(−a)] / 2 − E(0)

      의 부호로 본다. Δ_even 은 홀수부(선형 힘 항)를 지우므로 **국소 곡률**만 남는다.
      작은 진폭 두 개에서 **재현되는 음의 곡률**이 있어야 불안정이다.
    """
    d = os.path.join(work, tag, "mode_scan")
    mp = os.path.join(d, "meta.json")
    if not os.path.isfile(mp):
        return 1, f"⛔ 없음: {mp} — 먼저 --mode_scan 으로 입력을 만들 것"
    meta = json.load(open(mp, encoding="utf-8"))
    pts, miss, bad = {}, [], []
    for lam in meta["lambdas"]:
        lt = f"{lam:+.2f}".replace(".", "p").replace("+", "p").replace("-", "m")
        op = os.path.join(d, f"lam{lt}", "scf.out")
        if not os.path.isfile(op):
            miss.append(f"λ={lam:+g}")
            continue
        t = open(op, encoding="utf-8", errors="replace").read()
        if "JOB DONE" not in t:
            miss.append(f"λ={lam:+g}(미완료)")
            continue
        if re.search(r"convergence NOT achieved", t):
            bad.append(f"λ={lam:+g}(SCF 미수렴)")
            continue
        m = re.findall(r"!\s+total energy\s+=\s+([-\d.]+)\s+Ry", t)
        if not m:
            bad.append(f"λ={lam:+g}(에너지 없음)")
            continue
        pts[round(float(lam), 6)] = float(m[-1]) * RY_EV
    L = [f"■ pristine 모드 스캔 — {tag}"]
    if miss or bad:
        L.append(f"   ⏳ 없는 점: {', '.join(miss) if miss else '—'}")
        if bad:
            L.append(f"   ⛔ 못 쓰는 점: {', '.join(bad)}")
        L.append("   ⇒ **판정하지 않는다.** 곡률은 ±쌍이 다 있어야 나온다 "
                 "(옛 판은 λ=0 하나로 '최소' 를 주장했다 — 리뷰 J P0-2).")
        return 1, "\n".join(L)
    if 0.0 not in pts:
        return 1, "\n".join(L + ["   ⛔ λ=0 이 없으면 기준이 없다"])
    e0 = pts[0.0]
    L.append("   λ        ΔE [meV]")
    for lam in sorted(pts):
        L.append(f"    {lam:+6.2f}  {(pts[lam]-e0)*1000:+10.2f}"
                 + ("   ← 기준" if lam == 0.0 else ""))

    # ── 짝수부 = 국소 곡률 (홀수부/선형 힘 항이 지워진다) ──────────────────
    amps = sorted({abs(l) for l in pts if l != 0 and -abs(l) in pts and abs(l) in pts})
    ev = [(a, ((pts[a] + pts[-a]) / 2 - e0) * 1000) for a in amps]
    L.append("")
    if not ev:
        L.append("   ⛔ ±쌍이 하나도 없다 — 곡률을 못 낸다. λ 를 대칭으로 설정할 것.")
        return 1, "\n".join(L)
    L.append("   진폭 a    Δ_even(a) = [E(+a)+E(−a)]/2 − E(0)  [meV]")
    for a, v in ev:
        L.append(f"    {a:6.2f}   {v:+10.2f}")
    small = [x for x in ev if x[0] <= 0.15] or ev[:2]
    neg = [x for x in small if x[1] < 0]
    L.append("")
    if len(small) >= 2 and len(neg) == len(small):
        L.append(f"   ⇒ ⛔ **작은 두 진폭에서 음의 곡률이 재현된다** "
                 f"({', '.join(f'a={a:g}: {v:+.1f}' for a, v in small)}) — "
                 f"이 trial direction 으로 **불안정**하다. NEB HOLD 유지하고 "
                 f"**변위 구조에서 이완**을 걸 것.")
    elif any(v < 0 for _a, v in ev) and all(v >= 0 for a, v in small):
        far = [(a, v) for a, v in ev if v < 0]
        L.append(f"   ⇒ ⚠ λ=0 **근처는 양의 곡률**인데 먼 진폭에서 낮다 "
                 f"({', '.join(f'a={a:g}: {v:+.1f}' for a, v in far)}) — "
                 f"국소 soft mode 가 아니라 **멀리 있는 lower-basin 후보**다. "
                 f"국소 안정성과는 다른 얘기다.")
    else:
        L.append("   ⇒ ✅ **전부 양의 곡률** — 다만 말할 수 있는 것은 "
                 "*\"이 한 방향에서 불안정을 검출하지 못했다\"* 까지다.")
    L += ["", "   ⛔ **이 결과 하나로 P0-2 를 닫을 수 없다** (리뷰 J2).",
          "      모드 하나만 봤고, 메운 Li 의 u=0 은 임의의 mode completion 이다.",
          "      닫으려면 symmetry-off pristine rattle 이완 2–3개 또는 관련 q 의 phonon/Hessian.",
          "   ⛔ 수치 바닥을 **미리 선언하지 않는다** — λ=0 반복 계산·더 엄격한 SCF·",
          "      dense-k spot check 로 **재서** 이 표와 나란히 놓을 것 (리뷰 J3)."]
    json.dump({"tag": tag, "points_eV": {str(k): v for k, v in pts.items()}, "e0_eV": e0,
               "delta_even_meV": {str(a): v for a, v in ev}},
              open(os.path.join(d, "scan_result.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    return 0, "\n".join(L)


def selftest_prereq():
    """선행검사 2건 selftest — **음성 경로 포함.**

    이 입력들은 GPU 를 태운다. 잘못 만들면 며칠을 버리므로, 여기서 보는 것은
    "만들어지는가" 가 아니라 **"틀린 입력을 만들기를 거부하는가"** 다.
    """
    import glob as _g
    import shutil
    import tempfile
    ok = True

    def chk(c, m):
        nonlocal ok
        ok &= bool(c)
        _p(f"  {_OK if c else _NG} {m}")

    td = tempfile.mkdtemp(prefix="prereq_st_")
    TAG = "li3nd"
    # ⚠ Li 부격자가 규칙적이어야 preflight(메운 Li 의 최근접 == 나머지 중앙값)를 탄다.
    #   3 × 3.667 = 11.001 로 두면 0 · 3.667 · 7.334 가 주기적으로 등간격이 된다.
    CELL = [[11.001, 0, 0], [0, 11.001, 0], [0, 0, 11.001]]
    ROWS = [("Li", [0.0, 0.0, 0.0]), ("Li", [3.667, 0.0, 0.0]),
            ("Nd", [5.185, 0.0, 0.0]), ("Nd", [0.0, 5.185, 0.0])]

    def _blk(rows):
        return "ATOMIC_POSITIONS angstrom\n" + "".join(
            f"  {s:3s} {p[0]:16.10f} {p[1]:16.10f} {p[2]:16.10f}\n" for s, p in rows)

    def _tail():
        return ("\nK_POINTS automatic\n  3 3 3 0 0 0\n\nCELL_PARAMETERS angstrom\n"
                + "".join("  %16.10f %16.10f %16.10f\n" % tuple(v) for v in CELL))

    def _sys(deg=0.02, q=0.0):
        return ("&CONTROL\n    calculation     = 'scf'\n"
                "    pseudo_dir      = '/data/work/pseudo'\n/\n"
                "&SYSTEM\n    ibrav           = 0\n    ecutwfc         = 60\n"
                "    ecutrho         = 480\n"
                f"    tot_charge      = {q:.1f}\n    occupations     = 'smearing'\n"
                f"    smearing        = 'mv'\n    degauss         = {deg}\n/\n"
                "&ELECTRONS\n    conv_thr        = 1.0d-8\n    mixing_beta     = 0.3\n/\n\n"
                "ATOMIC_SPECIES\n  Li   6.940  li.UPF\n  Nd 144.242  nd.UPF\n\n")

    d = os.path.join(td, TAG)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "neb.in"), "w", encoding="utf-8").write(
        "BEGIN\nBEGIN_PATH_INPUT\n&PATH\n  CI_scheme='no-CI'\n  degauss = 9.99\n/\n"
        "END_PATH_INPUT\nBEGIN_ENGINE_INPUT\n" + _sys() + _blk(ROWS) + _tail()
        + "END_ENGINE_INPUT\nEND\n")

    # ── 헤더 파서: &PATH 안쪽 값에 속으면 안 된다 (거기에도 degauss 를 심어 뒀다) ──
    hdr, err = parse_qe_header(os.path.join(d, "neb.in"))
    chk(hdr is not None and abs(hdr["degauss"] - 0.02) < 1e-9,
        f"[선행·파서] neb.in 의 **엔진 블록** degauss 를 읽는다 "
        f"({hdr['degauss'] if hdr else err})")
    chk(hdr and len(hdr["species"]) == 2 and hdr["kpts"][1] == "3 3 3 0 0 0",
        "[선행·파서] 원소·k-point 를 그대로 옮긴다")
    chk(parse_qe_header(os.path.join(d, "nope.in"))[0] is None,
        "[선행·파서·음성] 없는 파일은 거부")

    # ── ① 사다리 ─────────────────────────────────────────────────────────────
    NIMG = 5
    frames = []
    for i in range(NIMG):
        frames.append([(s, [p[0] + 0.1 * i, p[1], p[2]]) for s, p in ROWS])
    open(os.path.join(d, f"{TAG}.xyz"), "w", encoding="utf-8").write("".join(
        f"{len(f)}\nimage {n+1}\n" + "".join(
            f"{s} {p[0]:.10f} {p[1]:.10f} {p[2]:.10f}\n" for s, p in f) for n, f in enumerate(frames)))
    PROF = [0.0, 0.12, 0.23, 0.10, 0.004]          # 최고 = image 3
    open(os.path.join(d, f"{TAG}.dat"), "w", encoding="utf-8").write(
        "".join(f"{i/4:.4f}  {e:.6f}  0.001\n" for i, e in enumerate(PROF)))
    rc, msg = smear_ladder(td, TAG, (0.02, 0.01))
    chk(rc == 0 and "안장 = image 3" in msg, f"[사다리] 최고에너지 이미지를 고른다 ({msg[:40]})")
    made = sorted(_g.glob(os.path.join(d, "smear_ladder", "g*", "*", "scf.in")))
    chk(len(made) == 6, f"[사다리] 2 degauss × 3 구조 = 6 입력 ({len(made)})")
    t1 = open(made[0], encoding="utf-8").read()
    chk("degauss         = 0.01" in t1 or "degauss         = 0.02" in t1,
        "[사다리] degauss 가 실제로 갈린다")
    chk("calculation     = 'scf'" in t1 and "nat             = 4" in t1
        and "tot_charge      = 0.0" in t1,
        "[사다리] scf · 원자수 · 전하가 런 프로토콜을 그대로 따른다")
    chk("li.UPF" in t1 and "3 3 3 0 0 0" in t1, "[사다리] PP·k 를 그대로 옮긴다")

    #   음성 ①-a: .dat 이 없으면 **안장을 임의로 고르지 않는다**
    shutil.move(os.path.join(d, f"{TAG}.dat"), os.path.join(d, "dat.bak"))
    rc, msg = smear_ladder(td, TAG, (0.02,))
    chk(rc == 1 and "안장인지 못 고른다" in msg, "[사다리·음성] 프로파일 없으면 거부")
    shutil.move(os.path.join(d, "dat.bak"), os.path.join(d, f"{TAG}.dat"))
    #   음성 ①-b: 이미지 수가 어긋나면 거부
    open(os.path.join(d, "bad.dat"), "w").write("0 0\n1 1\n")
    _f, _e, _err = read_neb_images(d, TAG)
    open(os.path.join(d, f"{TAG}.dat"), "a").write("9 9 9\n")
    chk(read_neb_images(d, TAG)[2] and "불일치" in read_neb_images(d, TAG)[2],
        "[사다리·음성] xyz·dat 이미지 수가 다르면 짝을 안 맞추고 거부")
    open(os.path.join(d, f"{TAG}.dat"), "w", encoding="utf-8").write(
        "".join(f"{i/4:.4f}  {e:.6f}  0.001\n" for i, e in enumerate(PROF)))
    #   음성 ①-c: 최고점이 끝점이면(단조 경로) 거부
    open(os.path.join(d, f"{TAG}.dat"), "w", encoding="utf-8").write(
        "".join(f"{i/4:.4f}  {e:.6f}  0.001\n" for i, e in enumerate([0, .1, .2, .3, .4])))
    rc, msg = smear_ladder(td, TAG, (0.02,))
    chk(rc == 1 and "안장이 없다" in msg, "[사다리·음성] 단조 경로는 거부 (안장이 없다)")
    open(os.path.join(d, f"{TAG}.dat"), "w", encoding="utf-8").write(
        "".join(f"{i/4:.4f}  {e:.6f}  0.001\n" for i, e in enumerate(PROF)))
    smear_ladder(td, TAG, (0.02, 0.01))

    #   회수: 허용폭 판정 양·음
    def _mkout(g, nm, ry):
        gt = f"{g:g}".replace(".", "p")
        p = os.path.join(d, "smear_ladder", f"g{gt}", nm)
        os.makedirs(p, exist_ok=True)
        open(os.path.join(p, "scf.out"), "w", encoding="utf-8").write(
            f"!    total energy              =    {ry:.8f} Ry\nJOB DONE.\n")
    for g, sad in ((0.02, 0.0168), (0.01, 0.01685)):        # 장벽 0.2286 vs 0.2293 eV
        _mkout(g, "ep_initial", -100.0)
        _mkout(g, "ep_final", -100.0)
        _mkout(g, "saddle", -100.0 + sad)
    rc, msg = collect_ladder(td, TAG)
    chk(rc == 0 and "수치적으로 안정" in msg,
        "[사다리·회수] 5 meV 안이면 '수치적으로 안정'")
    chk("정방향" in msg and "역방향" in msg and "끝점 split" in msg,
        "[사다리·회수] 양쪽 장벽과 끝점 splitting 을 따로 낸다 (리뷰 J1)")
    #   ★★ P0-1 회귀: **일부 점만 있으면 판정하지 않는다** (옛 판은 rc=0 으로 통과했다)
    import shutil as _sh
    _sh.rmtree(os.path.join(d, "smear_ladder", "g0p01", "saddle"))
    rc, msg = collect_ladder(td, TAG)
    chk(rc == 1 and "판정하지 않는다" in msg,
        "[사다리·회수·P0회귀] **점이 빠지면 거부**한다 (옛 판은 일부만으로 판정+성공종료)")
    _mkout(0.01, "saddle", -100.0 + 0.0200)                 # 43 meV 튐 — 복구 겸
    rc, msg = collect_ladder(td, TAG)
    chk("NO-GO" in msg, "[사다리·회수·음성] 36 meV 넘으면 NO-GO 라고 말한다")
    #   SCF 미수렴 문자열이 있으면 그 점을 못 쓰는 점으로 센다
    open(os.path.join(d, "smear_ladder", "g0p01", "saddle", "scf.out"), "a").write(
        "     convergence NOT achieved after 200 iterations\n")
    rc, msg = collect_ladder(td, TAG)
    chk(rc == 1 and "SCF 미수렴" in msg, "[사다리·회수·음성] SCF 미수렴 점을 조용히 안 쓴다")

    # ── ② 모드 스캔 ──────────────────────────────────────────────────────────
    d2 = os.path.join(td, "sc")
    for nm in ("ep_initial", "ep_final"):
        os.makedirs(os.path.join(d2, nm), exist_ok=True)
    BUILT_I = ROWS
    BUILT_F = [("Li", [7.334, 0.0, 0.0])] + ROWS[1:]
    REL_I = [(s, [p[0], p[1] + (0.3 if s == "Nd" else 0.02), p[2]]) for s, p in BUILT_I]
    for nm, rows in (("ep_initial", BUILT_I), ("ep_final", BUILT_F)):
        open(os.path.join(d2, nm, "relax.in"), "w", encoding="utf-8").write(
            _sys() + _blk(rows) + _tail())
    open(os.path.join(d2, "ep_initial", "relax.out"), "w", encoding="utf-8").write(
        "Begin final coordinates\n" + _blk(REL_I) + "End final coordinates\n"
        "!    total energy              =    -100.0 Ry\nJOB DONE.\n")
    LAM = (-0.5, -0.10, -0.05, 0.0, 0.05, 0.10, 0.5)
    rc, msg = mode_scan(td, "sc", LAM)
    chk(rc == 0 and "preflight ✅" in msg, f"[스캔] preflight 통과 후 입력을 만든다 ({msg[:44]})")
    sc = sorted(_g.glob(os.path.join(d2, "mode_scan", "lam*", "scf.in")))
    chk(len(sc) == len(LAM), f"[스캔] λ {len(LAM)}개 ({len(sc)})")
    t2 = open(sc[0], encoding="utf-8").read()
    chk(f"nat             = {len(BUILT_I)+1}" in t2,
        f"[스캔·핵심] 공공을 **메운다** — 원자 {len(BUILT_I)} → {len(BUILT_I)+1}")
    chk("tot_charge      = 0.0" in t2, "[스캔·핵심] 공공이 없으니 전하는 중성이다")
    mj = json.load(open(os.path.join(d2, "mode_scan", "meta.json"), encoding="utf-8"))
    chk(mj["preflight"]["min_distance_A"] > 1.5 and "upf_sha256" in mj,
        "[스캔] preflight 와 PP 해시를 meta 에 남긴다 (리뷰 J P0)")
    z = [x for x in sc if "lamp0p00" in x]
    zr = _pos_block(open(z[0], encoding="utf-8").read(),
                    open(z[0], encoding="utf-8").read().index("ATOMIC_POSITIONS"))
    chk(all(abs(zr[i][1][k] - ([*BUILT_I, BUILT_F[0]][i][1][k])) < 1e-6
            for i in range(len(zr)) for k in range(3)),
        "[스캔·핵심] λ=0 은 **갓 지은 완전 격자** 그대로다")

    #   ★★ P0-2 회귀: λ=0 **하나만** 있으면 판정하지 않는다
    def _scanout(lam, ry, tail="JOB DONE.\n"):
        lt = f"{lam:+.2f}".replace(".", "p").replace("+", "p").replace("-", "m")
        pp = os.path.join(d2, "mode_scan", f"lam{lt}")
        os.makedirs(pp, exist_ok=True)
        open(os.path.join(pp, "scf.out"), "w", encoding="utf-8").write(
            f"!    total energy              =    {ry:.8f} Ry\n" + tail)
    _scanout(0.0, -100.0)
    rc, msg = collect_scan(td, "sc")
    chk(rc == 1 and "판정하지 않는다" in msg,
        "[스캔·회수·P0회귀] **λ=0 하나로는 판정 안 한다** (옛 판은 '최소' 라고 찍었다)")

    #   양성 ①: 작은 두 진폭에서 **음의 곡률 재현** → 불안정
    for lam, ry in ((-0.5, -100.0 - 0.02), (-0.10, -100.0 - 0.001), (-0.05, -100.0 - 0.0004),
                    (0.0, -100.0), (0.05, -100.0 - 0.0004), (0.10, -100.0 - 0.001),
                    (0.5, -100.0 - 0.02)):
        _scanout(lam, ry)
    rc, msg = collect_scan(td, "sc")
    chk(rc == 0 and "음의 곡률이 재현" in msg and "불안정" in msg,
        "[스캔·회수·양성] 작은 진폭 음의 곡률 → 불안정")
    chk("Δ_even" in msg, "[스캔·회수] 판정을 **짝수부(곡률)** 로 한다 — 최저 λ 가 아니라")

    #   양성 ②: 근처는 양의 곡률인데 **먼 곳만** 낮다 → 국소 soft mode 아님
    for lam, ry in ((-0.10, -100.0 + 0.002), (-0.05, -100.0 + 0.0006),
                    (0.05, -100.0 + 0.0006), (0.10, -100.0 + 0.002),
                    (-0.5, -100.0 - 0.03), (0.5, -100.0 - 0.03)):
        _scanout(lam, ry)
    rc, msg = collect_scan(td, "sc")
    chk("lower-basin" in msg, "[스캔·회수] 근처 양 + 먼 곳 음 → **먼 lower-basin 후보**로 구분")

    #   음성: 전부 양의 곡률 → **약한 결론만**
    for lam, ry in ((-0.5, -100.0 + 0.05), (0.5, -100.0 + 0.05)):
        _scanout(lam, ry)
    rc, msg = collect_scan(td, "sc")
    chk("검출하지 못했다" in msg and "닫을 수 없다" in msg,
        "[스캔·회수·음성] 전부 양이면 '검출 못 함' 까지만 — P0-2 를 닫지 않는다")

    #   preflight 음성: 좌표가 겹치면 만들지 않는다
    d3 = os.path.join(td, "dup")
    for nm in ("ep_initial", "ep_final"):
        os.makedirs(os.path.join(d3, nm), exist_ok=True)
    DUP_I = [("Li", [0.0, 0.0, 0.0]), ("Li", [0.05, 0.0, 0.0]), ("Nd", [5.185, 0.0, 0.0])]
    DUP_F = [("Li", [3.667, 0.0, 0.0])] + DUP_I[1:]
    for nm, rows in (("ep_initial", DUP_I), ("ep_final", DUP_F)):
        open(os.path.join(d3, nm, "relax.in"), "w", encoding="utf-8").write(
            _sys() + _blk(rows) + _tail())
    open(os.path.join(d3, "ep_initial", "relax.out"), "w", encoding="utf-8").write(
        "Begin final coordinates\n" + _blk(DUP_I) + "End final coordinates\n"
        "!    total energy              =    -100.0 Ry\nJOB DONE.\n")
    rc, msg = mode_scan(td, "dup", (-0.05, 0.0, 0.05))
    chk(rc == 1 and "preflight 실패" in msg,
        "[스캔·preflight·음성] 최소거리가 이상하면 **입력을 안 만든다**")

    chk(collect_scan(td, "nope")[0] == 1 and collect_ladder(td, "nope")[0] == 1,
        "[선행·가드] 입력을 안 만들었으면 회수를 거부")
    shutil.rmtree(td, ignore_errors=True)
    return ok


def align_endpoints(work, tag, source="in", far_r=FAR_FIELD_R_A, allow_unconverged=True,
                    base_dirs=False):
    """P0-1 진단: 두 끝점의 겉보기 변위에서 병진·라벨을 뺀다.

    source="in"  → 갓 지은 좌표 (relax.in)   · source="out" → 이완 좌표 (relax.out)
    **둘 다 돌려서 비교하는 것이 이 도구의 용법**이다: in 이 깨끗한데 out 이 크면
    그 차이는 이완(또는 이완 표류)에서 온 것이다.

    base_dirs=True 면 `_r2`·`_r3` 이어달리기를 **따라가지 않고** `ep_initial/`·`ep_final/`
    원본을 본다. 08-17 사고가 정확히 여기였다 — 한쪽은 갓 지은 입력을, 다른 쪽은
    이완본을 보고 "다른 홉" 이라는 결론을 냈다. 두 규약을 나란히 돌려야 그게 안 숨는다.
    """
    d = os.path.join(work, tag)
    got, conv = {}, {}
    for nm in ("ep_initial", "ep_final"):
        ed = os.path.join(d, nm) if base_dirs else endpoint_dir(d, nm)
        if source == "in":
            p = os.path.join(ed, "relax.in")
            if not os.path.isfile(p):
                return 1, f"⛔ 없음: {p}"
            got[nm], conv[nm] = parse_input_positions(p), None
        else:
            rows, err, info = read_relaxed(os.path.join(ed, "relax.out"), allow_unconverged)
            if rows is None:
                return 1, f"⛔ {nm}: {err}"
            got[nm], conv[nm] = rows, info.get("converged")
        got[nm + "_dir"] = ed
    cell = parse_cell(os.path.join(got["ep_initial_dir"], "relax.in"))
    cell2 = parse_cell(os.path.join(got["ep_final_dir"], "relax.in"))
    if cell is None:
        return 1, "⛔ CELL_PARAMETERS 를 못 읽었다"
    if cell2 and max(abs(cell[i][k] - cell2[i][k]) for i in range(3) for k in range(3)) > 1e-6:
        return 1, "⛔ 두 끝점의 셀이 다르다 — 이 진단은 같은 셀에서만 뜻이 있다"

    rep = align_report(got["ep_initial"], got["ep_final"], cell, far_r)
    if "error" in rep:
        return 1, rep["error"]
    rep["source"] = source
    rep["endpoint_convention"] = "base(ep_*)" if base_dirs else "resolved(_r* 우선)"
    rep["endpoint_dirs"] = [got["ep_initial_dir"], got["ep_final_dir"]]
    rep["relax_converged"] = {k: conv[k] for k in ("ep_initial", "ep_final")}

    L = [f"■ 끝점 정렬 진단 — {tag} (source=relax.{source} · "
         f"{'원본 ep_*' if base_dirs else '수렴본 _r* 우선'})",
         f"   끝점: {os.path.basename(got['ep_initial_dir'])} · "
         f"{os.path.basename(got['ep_final_dir'])}"]
    if source == "out":
        bad = [k for k, v in conv.items() if v is False]
        if bad:
            L.append(f"   ⛔ **이완 미수렴**: {', '.join(bad)} — 아래 잔여 변위에는 "
                     f"미수렴 표류가 섞여 있다. 이 도구는 그것을 못 가른다.")
    L += [f"   강체 병진 제거: |t| = {rep['translation_norm_A']} Å "
          f"{'(수렴)' if rep['translation_converged'] else '(⚠ 미수렴)'}",
          f"   라벨 재대응: {rep['n_relabeled']} 개 ({rep['assignment']})",
          f"   홉 원자: {rep['hop_atom']['element']} "
          f"raw {rep['hop_atom']['raw_A']} → 정렬 {rep['hop_atom']['aligned_A']} Å",
          f"   홉 제외 최대: raw {rep['raw_max_excl_hop_A']} → "
          f"**정렬 {rep['aligned_max_excl_hop_A']}** Å",
          "   거리별 잔여 [Å]:"]
    for b in rep["by_distance"]:
        L.append(f"     r {b['r_A']:>6}  n={b['n']:<4} 중앙 {b['median_A']:<8} 최대 {b['max_A']}")
    L.append(f"   far-field(>{far_r} Å, n={rep['n_far_field']}) 최대 = {rep['far_field_max_A']} Å")
    loc = rep.get("locality")
    if loc:
        L.append(f"   국소성: {loc['inner_bin']} 중앙 {loc['inner_median_A']} → "
                 f"{loc['outer_bin']} 중앙 {loc['outer_median_A']} "
                 f"(비 {loc['outer_over_inner']}, "
                 f"{'단조감소' if loc['monotone_decreasing'] else '**단조감소 아님**'})")
        if loc.get("note"):
            L.append("   " + loc["note"])
    L += ["", "   " + rep["verdict_text"]]
    op = os.path.join(d, f"align_report_{source}{'_base' if base_dirs else ''}.json")
    try:
        json.dump(rep, open(op, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        L.append(f"   → {op}")
    except OSError:
        pass
    return 0, "\n".join(L)


def selftest_align():
    """정렬 진단 selftest — **음성 경로 포함**.

    음성 경로가 핵심이다: 강체 병진·라벨 교환처럼 *물리가 아닌* 겉보기 변위를
    이 도구가 실제로 걷어내는지. 양성만 있으면 통과해도 아무것도 보증 못 한다.
    """
    import math as _m
    ok = True

    def chk(c, m):
        nonlocal ok
        ok &= bool(c)
        _p(f"  {_OK if c else _NG} {m}")

    A, N = 5.19, 3
    cell = [[A * N, 0, 0], [0, A * N, 0], [0, 0, A * N]]
    base = []
    for i in range(N):
        for j in range(N):
            for k in range(N):
                base.append(("Nd", [i * A, j * A, k * A]))
                base.append(("Li", [i * A + A / 2, j * A, k * A]))
    hop_i = next(i for i, (s, p) in enumerate(base) if s == "Li")

    def moved(shift=(0, 0, 0), noise=0.0, far_move=0, swap=None, hop=3.667):
        out = []
        for i, (s, p) in enumerate(base):
            q = [p[k] + shift[k] + (noise if (i + k) % 3 == 0 else -noise) for k in range(3)]
            out.append((s, q))
        out[hop_i] = (out[hop_i][0], [out[hop_i][1][0] + hop] + out[hop_i][1][1:])
        if far_move:
            ctr = base[hop_i][1]
            far = sorted((i for i, (s, p) in enumerate(base)
                          if s == "Nd" and i != hop_i),
                         key=lambda i: -_m.sqrt(sum((base[i][1][k] - ctr[k]) ** 2
                                                    for k in range(3))))[:far_move]
            for i in far:
                out[i] = (out[i][0], [out[i][1][0] + 1.12, out[i][1][1], out[i][1][2]])
        if swap:
            a, b = swap
            out[a], out[b] = (out[a][0], out[b][1]), (out[b][0], out[a][1])
        return out

    # ── 음성 ① 순수 강체 병진 (|t| = 1.10 Å) — 인공물로 판정해야 한다 ──
    r = align_report(base, moved(shift=(0.6, 0.6, 0.7), noise=0.005), cell)
    chk(r["raw_max_excl_hop_A"] > 1.0, "[정렬·음성] 병진 전에는 raw 가 1 Å 넘게 보인다")
    chk(abs(r["translation_norm_A"] - 1.1) < 0.05, "[정렬·음성] 병진 |t|≈1.10 Å 를 찾는다")
    chk(r["verdict"] == "인공물",
        f"[정렬·음성] 순수 병진은 **인공물**로 판정 (far {r['far_field_max_A']})")

    # ── 음성 ② 같은 원소 라벨 교환 — 재대응으로 사라져야 한다 ──
    nds = [i for i, (s, _) in enumerate(base) if s == "Nd"]
    r = align_report(base, moved(swap=(nds[0], nds[-1])), cell)
    chk(r["n_relabeled"] >= 2 and r["verdict"] == "인공물",
        f"[정렬·음성] 라벨 교환은 재대응으로 사라진다 (재대응 {r['n_relabeled']}개)")

    # ── 양성 ③ 진짜 far-field 이완 6개 × 1.12 Å — 살아남아야 한다 ──
    r = align_report(base, moved(far_move=6), cell)
    chk(r["verdict"] == "실제" and r["far_field_max_A"] > 1.0,
        f"[정렬·양성] 실제 비국소 이완은 살아남는다 (far {r['far_field_max_A']})")

    # ── 양성 ④ 병진 + 진짜 이완이 섞여도 진짜만 남는다 (제일 현실적) ──
    r = align_report(base, moved(shift=(0.6, 0.6, 0.7), far_move=6), cell)
    chk(r["verdict"] == "실제" and abs(r["translation_norm_A"] - 1.1) < 0.05,
        f"[정렬·양성] 병진+이완 혼합에서 병진만 빠진다 (|t|={r['translation_norm_A']}, "
        f"far {r['far_field_max_A']})")

    # ★★ 실측회귀 (2026-08-27): 원시 벡터가 **셀보다 훨씬 길어도** 접혀야 한다.
    #   옛 min_image 는 ±1 셀만 훑어서 한 방향으로 한 셀치만 뺐다. 끝점 변위(≈1 Å)에서는
    #   안 드러나다가, 셀 밖에 놓이는 **반전상**을 비교하자마자 10.37 Å 셀에서 잔차
    #   17.39 Å 이 나왔다 — 그 셀의 min-image 상한(√3·L/2 = 8.98)을 넘는 **불가능한 값**이다.
    L = A * N
    lim = _m.sqrt(3) * L / 2
    for v in ([2.7 * L, -3.4 * L + 1.0, 5.1 * L - 0.5], [-9.2 * L, 0.0, 0.0]):
        mi = min_image(v, cell)
        chk(_m.sqrt(sum(x * x for x in mi)) <= lim + 1e-6,
            f"[정렬·min_image·실측회귀] 셀의 {abs(v[0])/L:.1f}배 벡터도 상한 {lim:.2f} Å 안으로 "
            f"접힌다 ({_m.sqrt(sum(x*x for x in mi)):.2f})")

    # ── 가드 ⑤ 원소 구성이 다르면 거부 ──
    bad = [(s if i else "Xx", p) for i, (s, p) in enumerate(base)]
    chk("error" in align_report(base, bad, cell), "[정렬·가드] 원소 구성이 다르면 거부")

    # ── 가드 ⑥ far-field 원자가 없으면 판정하지 않는다 + 권장 far_r 를 준다 ──
    r = align_report(base, moved(far_move=6), cell, far_r=100.0)
    chk(r["verdict"] == "판정불가" and "--far_r" in r["verdict_text"],
        "[정렬·가드] far-field 가 비면 판정불가 + 권장 far_r")

    # ── ⑦ 위양성 차단(실측에서 걸린 것): **갓 지은 좌표**는 홉 외 변위가 정의상 0 이다.
    #     거기에 '인공물' 을 찍으면 정렬이 뭔가를 걷어냈다는 정반대 인상을 준다.
    r = align_report(base, moved(), cell)
    chk(r["verdict"] == "무정보",
        f"[정렬·위양성] 홉만 움직인 좌표는 '인공물' 이 아니라 **무정보** ({r['verdict']})")

    # ── ⑧ 국소성: 거리에 따라 주는 장 vs 안 주는 장을 구분한다 ──
    import math as _mm
    ctr0 = base[hop_i][1]
    # 거리에 무관한 0.5 Å 장. 방향은 index 로 결정론적으로 흩어 **강체 병진이 아니게** 한다
    #   (전 원자를 같은 방향으로 밀면 그건 병진이라 도구가 옳게 걷어낸다).
    flat = []
    for i, (s, p) in enumerate(base):
        v = [_mm.sin(i * 1.7), _mm.cos(i * 2.3), _mm.sin(i * 3.1)]
        n = _mm.sqrt(sum(x * x for x in v)) or 1.0
        flat.append((s, [p[k] + 0.5 * v[k] / n for k in range(3)]))
    flat[hop_i] = (flat[hop_i][0], [base[hop_i][1][0] + 3.667] + base[hop_i][1][1:])
    r = align_report(base, flat, cell)
    _loc = r.get("locality") or {}
    chk((_loc.get("outer_over_inner") or 0) >= 0.5 and "안 준다" in (_loc.get("note") or ""),
        f"[정렬·국소성] 거리에 안 주는 장을 그렇게 부른다 (비 {_loc.get('outer_over_inner')})")
    # 음성쌍: **방사형으로 감쇠하는** 장 = 점결함 응답의 교과서 모양. 경고가 붙으면 안 된다.
    #   (방향을 방사형으로 두는 게 중요하다 — 전부 +x 로 밀면 그건 병진에 가까워
    #    중앙값 제거가 먹어버리고, 그러면 이 검사가 감쇠를 본 게 아니게 된다.)
    decay = []
    for i, (s, p) in enumerate(base):
        v = min_image([p[k] - ctr0[k] for k in range(3)], cell)
        d = _mm.sqrt(sum(x * x for x in v)) or 1.0
        amp = 2.0 * _mm.exp(-d / 2.0)
        decay.append((s, [p[k] + amp * v[k] / d for k in range(3)]))
    decay[hop_i] = (decay[hop_i][0], [base[hop_i][1][0] + 3.667] + base[hop_i][1][1:])
    r = align_report(base, decay, cell)
    _loc = r.get("locality") or {}
    chk(_loc.get("monotone_decreasing") is True and "note" not in _loc,
        f"[정렬·국소성·음성] 방사형 감쇠장에는 경고를 안 붙인다 (비 {_loc.get('outer_over_inner')})")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="/data/work/runs/sei_neb_v2_cc333")
    ap.add_argument("--tag", default="li3nd")
    ap.add_argument("--collect", action="store_true", help="돌린 뒤 Ea 를 뽑는다")
    ap.add_argument("--force", action="store_true", help="비대칭인데도 강행 (권장 안 함)")
    ap.add_argument("--relax_radius", type=float, default=None,
                    help="고정셸 방식: 이 반경[Å] 밖 원자를 고정하고 공공 주변만 이완한다. "
                         "끝점·안장에 **같은** 중심·반경·자유집합을 쓴다")
    ap.add_argument("--allow_unconverged", action="store_true",
                    help="끝점 이완이 수렴 안 했어도 마지막 스텝 좌표로 진행 (결과에 명시된다)")
    ap.add_argument("--emit_check", action="store_true",
                    help="안장 relax 결과 좌표로 **구속 없는** scf 입력을 만든다 "
                         "(if_pos 마스킹 때문에 relax.out 힘으로는 검증이 안 된다)")
    ap.add_argument("--scan", default=None,
                    help="반경 스캔 (예: '3.5,4,5,6'). 각 반경으로 입력 세트를 만든다 — "
                         "두 번 연속 |ΔEa| ≤ 0.02~0.03 eV 면 반경 수렴")
    ap.add_argument("--align_check", action="store_true",
                    help="P0-1(리뷰 I): 두 끝점 변위에서 **강체 병진·라벨 교환을 빼고** "
                         "남는 잔여를 낸다 — 비국소 이완이 진짜인지 가른다")
    ap.add_argument("--align_source", choices=("in", "out", "both"), default="both",
                    help="in=갓 지은 좌표 · out=이완 좌표 · both=둘 다(권장)")
    ap.add_argument("--far_r", type=float, default=FAR_FIELD_R_A,
                    help=f"far-field 기준 거리 [Å] (기본 {FAR_FIELD_R_A})")
    ap.add_argument("--align_base", action="store_true",
                    help="이어달리기(_r2·_r3)를 따라가지 않고 **원본 ep_initial/ep_final** 을 본다. "
                         "08-17 사고(한쪽은 갓 지은 입력·한쪽은 이완본)를 드러내려면 "
                         "이것과 기본 규약을 나란히 돌린다")
    ap.add_argument("--smear_ladder", action="store_true",
                    help="① degauss 사다리 SCF 입력 (kb 2026-08-11 선행조건 · 회신 I N5). "
                         "고정 기하 — 이완을 다시 하지 않는다")
    ap.add_argument("--collect_ladder", action="store_true", help="① 사다리 결과 회수")
    ap.add_argument("--mode_scan", action="store_true",
                    help="② pristine ±δ 모드 스캔 입력 (회신 I P0-2 의 싼 판). "
                         "공공을 메운 셀을 관측한 이완 모드로 밀어 E(λ) 를 본다")
    ap.add_argument("--collect_scan", action="store_true", help="② 모드 스캔 결과 회수")
    ap.add_argument("--ladder", default=",".join(f"{x:g}" for x in SMEAR_LADDER_RY),
                    help="① degauss 값들 [Ry]")
    ap.add_argument("--lambdas", default=",".join(f"{x:g}" for x in MODE_SCAN_LAMBDAS),
                    help="② λ 값들")
    ap.add_argument("--bfgs_trace", action="store_true",
                    help="끝점 relax.out 의 **BFGS 궤적**으로 물리/배회를 가른다 "
                         "(새 계산 없음): 배회지수 + 두 끝점 모드 일치도")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        rc = selftest()
        return 0 if (selftest_align() and selftest_trace()
                     and selftest_prereq() and rc == 0) else 1
    if a.bfgs_trace:
        r, m = bfgs_trace(a.work, a.tag, a.align_base)
        print(m)
        return r
    for _flag, _fn, _arg in (
            ("smear_ladder", smear_ladder, tuple(float(x) for x in a.ladder.split(","))),
            ("mode_scan", mode_scan, tuple(float(x) for x in a.lambdas.split(","))),
            ("collect_ladder", collect_ladder, None),
            ("collect_scan", collect_scan, None)):
        if getattr(a, _flag):
            r, m = (_fn(a.work, a.tag, _arg) if _arg is not None else _fn(a.work, a.tag))
            print(m)
            return r
    if a.align_check:
        srcs = ("in", "out") if a.align_source == "both" else (a.align_source,)
        rc = 0
        for s in srcs:
            # ⚠ 미수렴 좌표를 **일부러** 읽는다 — 미수렴 표류를 보는 것이 이 진단의 목적이다.
            #   대신 보고서가 미수렴을 ⛔ 로 명시한다 (조용히 쓰지 않는다).
            r, m = align_endpoints(a.work, a.tag, s, a.far_r, allow_unconverged=True,
                                   base_dirs=a.align_base)
            print(m)
            print()
            rc = rc or r
        return rc
    if a.relax_radius is not None and a.relax_radius <= 0:
        # ⛔ 리뷰 F6 — 진리값으로 분기하면 0 이 전이완(수일짜리)으로 조용히 샌다
        print("⛔ --relax_radius 는 0 보다 커야 한다 (고정셸 반경 [Å]). "
              "전이완을 원하면 이 옵션을 아예 빼라")
        return 2
    if a.relax_radius and not a.collect:
        rc, msg = build_frozen(a.work, a.tag, a.relax_radius, a.force)
    elif a.collect:
        rc, msg = collect(a.work, a.tag, a.relax_radius, a.allow_unconverged)
    else:
        rc, msg = build(a.work, a.tag, a.force, a.allow_unconverged)
    print(msg)
    return rc


if __name__ == "__main__":
    sys.exit(main())
