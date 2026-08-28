#!/usr/bin/env python3
"""scfin_to_struct.py — QE scf.in / VASP OUTCAR → xyz + POSCAR + .vesta + 거리 점검(+에너지 CSV).

계산에 **실제로 들어간** 기하를 그대로 꺼낸다. Phase-A 스캔 xyz 가 아니라 scf.in 을
읽는 이유: 스캔 셀은 c=40 Å 인데 파이프라인이 슬랩 셀(c=28.79 Å)로 다시 앉히기
때문에, 눈으로 봐야 하는 건 **재배치 후**의 기하다.

**--outcar (2026-08-28 추가)** — wave1 VASP 결과처럼 *결과만 회수된* 드롭에서
기하·에너지를 같은 파일 하나로 꺼낸다. OUTCAR 는 좌표·셀·이온별 모멘트·총에너지를
전부 들고 있으므로 입력 파일이 안 돌아와도 **본 것을 그릴 수 있다**.

⚠⚠ **에너지는 전자 스텝 TOTEN 을 읽으면 안 된다 (LDA+U 함정, 실측).**
  ptfe_c10 Li-top pm1 static 에서 전자스텝 마지막 `energy(sigma->0) = -1094.74765`,
  최종 이온스텝 블록 `= -1123.35770` — **28.6 eV 차**다. U 이중계산 보정이 최종
  블록에서만 더해지기 때문이다 (OSZICAR 의 `E0=` 와 일치하는 쪽이 정본).
  그래서 판독은 vasp_handoff_bundle.py 의 ANALYZER 를 **빌려 쓴다** — 복사하면
  규약이 두 곳으로 갈린다(사각 C).

⚠ 2026-07-17 에 doped 결합에너지를 철회한 원인이 이 지점이었다 — 분자가 수직으로 서서
  티오펜 S 가 **c 를 넘은 이미지 슬랩의 O 와 1.506 Å**(결합거리)이었고, 그러면 E_bind 가
  한 표면이 아니라 두 표면 몫이 된다. 그래서 구조만 뽑지 않고 거리를 같이 찍는다.

⚠⚠ **거리를 층으로 갈라야 한다. 안 가르면 두 방향으로 다 틀린다 (2026-08-03, 실제로 다 틀림).**
  ① 흡착 접촉  sh_z == 0 (자기 셀 포함) — 슬랩은 면내로 **연속된 하나의 표면**이다.
     분자가 셀 모서리에 앉으면 진짜 결합상대가 shift (1,1,0) 에 있다. 자기 셀만 재면
     그 결합(1.887 Å)을 놓치고 6.348 Å 을 보고 "떠 있다"고 오판한다.
  ② 진공 너머  sh_z != 0 — 여기만 **인공 두 번째 표면**이다. 샌드위치 판정은 이 층에서만.
  ③ 면내 피복  sh_z == 0, 분자↔분자 — 분자가 옆 셀 자기 자신과 닿으면 피복률이 과하다.
  [참고] 슬랩↔슬랩 면내(Ni–O 1.94 Å, Ni–Ni 2.88 Å)는 **결정 그 자체**다. 판정에 넣지 마라.

⚠⚠ **xyz 와 vasp 는 반드시 같은 원자 순서로 쓴다 (2026-08-03).** POSCAR 는 같은 원소가
  연속해야 하는데 복합체는 O 가 슬랩과 분자 양쪽에 흩어져 있어 재정렬이 불가피하다.
  예전 판은 vasp 만 재정렬해서 두 파일의 원자 순서가 달랐고, 뷰어에서 서로 다른
  구조처럼 보였다(실측 제보). 순서를 한 번만 정하고 두 파일에 똑같이 쓴다.

  cd ~/Yonghoon-DEM-DFT
  python3 tools/sdcp/scfin_to_struct.py --selftest
  python3 tools/sdcp/scfin_to_struct.py --scf_in .../complex_doped/scf.in --out ~/sdcp_poses
  python3 tools/sdcp/scfin_to_struct.py --outcar <drop>/tier1/*/static/OUTCAR.gz \\
      --out db/structures/sdcp_wave1 \\
      --energy_csv db/properties/sdcp_wave1_job_energies_2026_08_28.csv \\
      --refs <drop>/refs

관례(CLAUDE.md): 구조 배포는 **xyz + POSCAR(.vasp) 페어**. xyz 는 격자가 없으므로
VESTA 에서 Boundary 타일링을 하려면 .vasp 쪽을 연다.

이 도구가 **못 하는 것**
  · 계산의 물리적 타당성을 판정하지 않는다. 기하를 꺼내 **거리 세 층**을 찍어줄 뿐이다.
  · `--energy_csv` 는 **게이트 통과 판정이 아니다.** 입력 무결성(MANIFEST 해시)·INCAR
    대조·상별 완결성은 vasp_handoff_bundle.py 의 ANALYZER 몫이고, 결과만 회수된
    부분 드롭에서는 그 분석기가 (정당하게) exit 2 로 멈춘다. 여기 나오는 숫자는
    **OUTCAR 원문 판독값**이지 캠페인 인용값이 아니다 — 인용 자격은
    db/properties/sdcp_wave1_citable.json 이 정한다.
  · 자기 basin 을 총자화로만 분류한다(A≈4 · B≈6 μB). 국소 모멘트 패턴은 안 본다 —
    범위 밖이면 `unresolved` 로 두고 E_ads 에 표시만 한다.
  · 분자 기준(box24)이 **어떤 전자상태인지** 검사하지 않는다. mol_doped 총자화 0.175
    (doublet 이면 1.000) 같은 문제는 여기서 안 잡힌다 — estimand 카드 §4 몫이다.
"""
import argparse
import csv
import itertools
import os
import re
import sys

import numpy as np

# 공유결합 반지름 (Å, Cordero 2008). 분자/슬랩 분할용 연결성 판정에만 쓴다.
RCOV = {"H": 0.31, "Li": 1.28, "B": 0.84, "C": 0.76, "N": 0.71, "O": 0.66,
        "F": 0.57, "P": 1.07, "S": 1.05, "Cl": 1.02, "Ni": 1.24}
BOND_SCALE = 1.25
# 분자 씨앗: 슬랩(LiNiO2)에 없는 원소만 고른다. O 는 양쪽에 다 있으므로 씨앗이 못 된다
# — 연결성으로 흡수시킨다.
MOL_SEED = ("C", "H", "S", "N", "F", "P", "B", "Cl")


def read_extxyz(path):
    """Phase-A 가 ASE 로 쓴 pose xyz. 2번째 줄 Lattice="..." 에 셀이 들어 있다.

    ⚠ 원본 자세를 그대로 볼 수 있어야 한다 — scf.in 쪽 수치가 이상할 때
      '스캔이 그렇게 낸 것'인지 'phaseB 가 망친 것'인지 가르는 유일한 대조군이다.
    """
    with open(path, errors="ignore") as f:
        lines = f.read().splitlines()
    nat = int(lines[0].split()[0])
    m = re.search(r'Lattice="([^"]+)"', lines[1])
    if not m:
        raise SystemExit(f"⛔ {path} 2번째 줄에 Lattice=\"...\" 가 없다 — 셀 없는 순수 xyz 는 못 쓴다")
    cell = np.array([float(x) for x in m.group(1).split()]).reshape(3, 3)
    labels, pos = [], []
    for ln in lines[2:2 + nat]:
        v = ln.split()
        labels.append(v[0]); pos.append([float(x) for x in v[1:4]])
    return cell, labels, np.array(pos)


def is_outcar(path):
    return os.path.basename(path).upper().startswith("OUTCAR")


def read_any(path):
    if is_outcar(path):
        return read_outcar(path)[:3]
    return read_extxyz(path) if path.lower().endswith((".xyz", ".extxyz")) else read_scf_in(path)


# ══ VASP OUTCAR ═══════════════════════════════════════════════════════════════
#: 자기 basin 분류 — clean_slab 실측 총자화. A ≈ 4 · B ≈ 6 μB (차 49.718 meV).
#: ⚠ 이 두 수는 **net4 branch 전용**이다. pm1 은 전 Ni 쌍이 상쇄돼 총자화 ≈ 0 이라
#:   basin 이 갈리지 않는다 — 그래서 pm1 은 basin 을 묻지 않고 'pm1' 로 적는다.
BASIN_MU = {"A": 4.0, "B": 6.0}
BASIN_TOL = 0.35        # μB — 이 밖이면 판정하지 않는다(unresolved). 실측 최대 편차 0.11
PM1_MU_MAX = 0.5        # μB — 이 아래면 pm1 branch


def basin_of(mag_total):
    """총자화 → 자기 basin 라벨. 모르면 'unresolved' (fail-closed).

    ⚠ 이것은 **분류**지 검증이 아니다. 같은 총자화가 서로 다른 국소 배열에서
      나올 수 있다 — 국소 모멘트 패턴 감사는 vasp_handoff_bundle 의 ANALYZER 몫.
    """
    if mag_total is None:
        return "unresolved"
    if abs(mag_total) <= PM1_MU_MAX:
        return "pm1"
    for lab, mu in BASIN_MU.items():
        if abs(abs(mag_total) - mu) <= BASIN_TOL:
            return lab
    return "unresolved"


def _analyzer(_cache={}):
    """vasp_handoff_bundle.py 안의 ANALYZER 문자열을 실행해 OUTCAR 판독기를 **빌려온다**.

    ⚠ 왜 import 가 아니라 exec 인가: 그 분석기는 번들에 *파일로 들어가는 문자열*이라
      모듈 속성이 아니다. 여기서 정규식을 복사하면 `energy(sigma->0)` 규약이 두 곳으로
      갈린다 — 사각 C(같은 규약의 두 경로), selftest_blind_spots 카드 참조.
    """
    if "ns" not in _cache:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import vasp_handoff_bundle as V
        ns = {"__name__": "vhb_analyzer"}
        exec(compile(V.ANALYZER, "<vasp_handoff_bundle.ANALYZER>", "exec"), ns)
        for fn in ("read_outcar", "_read_outcar_raw", "_last_run_segment"):
            if fn not in ns:
                raise SystemExit(f"⛔ ANALYZER 에 {fn} 이 없다 — 번들 판독기가 바뀌었다")
        _cache["ns"] = ns
    return _cache["ns"]


def _species_from_outcar(t, nat):
    """POTCAR TITEL + `ions per type` → 원자별 원소 기호.

    ⚠ TITEL 은 `PAW_PBE Ni_pv 06Sep2000` 처럼 **준중심 변형 접미사**가 붙는다.
      Ni_pv 를 그대로 원소로 쓰면 뷰어가 모르는 종이 되므로 `_pv`/`_sv`/`_h` 를 뗀다.
    """
    tit = re.findall(r"TITEL\s*=\s*(.+)", t)
    ipt = re.search(r"ions per type\s*=\s*([\d\s]+)", t)
    if not tit or not ipt:
        raise SystemExit("⛔ OUTCAR 에서 TITEL/ions per type 을 못 읽었다 — 원소 배정 불가")
    counts = [int(v) for v in ipt.group(1).split()]
    # ⚠ TITEL 은 반복 인쇄될 수 있다. **중복 제거로 접으면 안 된다** — 같은 원소를 두 종으로
    #   나눈 계(자기 부격자 분리 POTCAR)에서 종 수가 줄어 배정이 밀린다. 앞에서부터 자른다.
    if len(tit) % len(counts) == 0 and len(tit) >= len(counts):
        tit = tit[:len(counts)]
    if len(counts) != len(tit):
        raise SystemExit(f"⛔ TITEL {len(tit)}종 ≠ ions per type {len(counts)}종")
    els = [x.split()[1].split("_")[0] for x in tit]
    if sum(counts) != nat:
        raise SystemExit(f"⛔ ions per type 합 {sum(counts)} ≠ POSITION 원자수 {nat}")
    return [e for e, c in zip(els, counts) for _ in range(c)]


def read_outcar(path):
    """OUTCAR(.gz) → (cell, labels, pos, meta). 라벨은 Ni 국소모멘트 부호로 부격자를 살린다.

    meta = {E0, mag_total, basin, nions, normal_end, moments, source}

    ⚠⚠ **에너지는 최종 이온스텝 블록의 energy(sigma->0) 다.** 전자스텝 TOTEN 을 읽으면
      LDA+U 이중계산 보정이 빠져 28.6 eV 어긋난다(실측, 모듈 docstring 참조). 그 규약은
      ANALYZER 하나에만 있고 여기서는 빌려 쓴다.
    """
    ns = _analyzer()
    oc = ns["read_outcar"](path)
    if oc is None:
        raise SystemExit(f"⛔ {path} 없음")
    if oc.get("read_error"):
        raise SystemExit(f"⛔ {path} 판독 실패: {oc['read_error']}")
    if not oc.get("positions"):
        raise SystemExit(f"⛔ {path} 에 POSITION 블록이 없다 — 기하를 못 꺼낸다")
    t, _seg = ns["_last_run_segment"](ns["_read_outcar_raw"](path)[0])
    pos = np.array(oc["positions"], float)

    k = t.rfind("direct lattice vectors")
    if k < 0:
        raise SystemExit(f"⛔ {path} 에 direct lattice vectors 가 없다")
    cell = []
    for ln in t[k:].splitlines()[1:4]:
        v = ln.split()
        if len(v) < 6:
            raise SystemExit(f"⛔ 격자 줄 파싱 실패: {ln!r}")
        cell.append([float(x) for x in v[:3]])
    cell = np.array(cell, float)

    els = _species_from_outcar(t, len(pos))
    # Ni 부격자: 수렴된 **국소 모멘트 부호**로 가른다 (seed 가 아니라 결과다 — pm1/net4 가
    # 같은 기하에서도 다른 그림이 되는 이유가 여기 보인다).
    mom = oc.get("moments")
    labels = list(els)
    if mom and len(mom) == len(els):
        for i, e in enumerate(els):
            if e == "Ni":
                labels[i] = "Ni1" if mom[i] >= 0 else "Ni2"
    meta = {"E0": oc["E0"], "mag_total": oc["mag_total"], "nions": oc["nions"],
            "normal_end": oc["normal_end"], "moments": mom,
            "basin": basin_of(oc["mag_total"]), "source": os.path.abspath(path)}
    return cell, labels, pos, meta


def read_scf_in(path):
    """CELL_PARAMETERS angstrom / ATOMIC_POSITIONS angstrom 만 읽는다 (이 생성기의 형식)."""
    with open(path, errors="ignore") as f:
        lines = f.read().splitlines()
    cell, labels, pos = [], [], []
    mode = None
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        head = s.split()[0].upper()
        if head == "CELL_PARAMETERS":
            if "angstrom" not in s.lower():
                raise SystemExit(f"⛔ CELL_PARAMETERS 단위가 angstrom 이 아니다: {s}")
            mode = "cell"; continue
        if head == "ATOMIC_POSITIONS":
            if "angstrom" not in s.lower():
                raise SystemExit(f"⛔ ATOMIC_POSITIONS 단위가 angstrom 이 아니다: {s}")
            mode = "pos"; continue
        if head in ("K_POINTS", "ATOMIC_SPECIES", "HUBBARD") or s.startswith("&"):
            mode = None; continue
        if mode == "cell":
            v = s.split()
            if len(v) == 3:
                cell.append([float(x) for x in v])
            if len(cell) == 3:
                mode = None
        elif mode == "pos":
            v = s.split()
            if len(v) >= 4:
                labels.append(v[0]); pos.append([float(x) for x in v[1:4]])
            else:
                mode = None
    if len(cell) != 3 or not labels:
        raise SystemExit(f"⛔ {path} 에서 셀/좌표를 못 읽었다")
    return np.array(cell), labels, np.array(pos)


# ⚠ QE 라벨은 자기/U 를 나누려고 원소 뒤에 숫자를 붙인다 (Ni1, Ni2). 뷰어에 넘길
#   .xyz/.vasp 에는 **원소 기호**가 가야 하므로 뒤 숫자를 뗀다.
def element(label):
    m = re.match(r"^([A-Z][a-z]?)", label)
    if not m:
        raise SystemExit(f"⛔ 라벨에서 원소를 못 읽었다: {label}")
    return m.group(1)


def group_by_species(elems, labels, pos):
    """POSCAR 규격(같은 원소 연속)에 맞게 한 번만 재정렬하고, 그 순서를 xyz 에도 쓴다."""
    uniq = sorted(set(elems), key=elems.index)          # 첫 등장 순서 유지
    idx = [i for e in uniq for i, x in enumerate(elems) if x == e]
    return ([elems[i] for i in idx], [labels[i] for i in idx], pos[np.array(idx)],
            uniq, [elems.count(e) for e in uniq])


# 슬랩 전용 원소 — flood-fill 이 절대 흡수하면 안 된다 (리뷰 §2-8).
#   화학흡착(분자 O ↔ 표면 Ni 1.9 Å = 결합거리)이 생기면 옛 판은 그 결합을 타고
#   슬랩을 통째로 흡수했다 — 실측: mol 조각 129/130 인데 전부 ✓ 로 통과.
SLAB_ONLY = ("Li", "Ni")
MOL_O_MAX = 8            # v7c 분자 자체 O 6 + H-전이로 문 표면 O 1 + 여유 1


def split_molecule(cell, elems, pos):
    """C/H/S 씨앗에서 공유결합 반지름으로 자라며 분자를 집는다. 나머지가 슬랩.

    리뷰 §2-8 반영:
      · **MIC** — 셀 모서리에 걸친 분자는 랩된 좌표로는 절단돼 보인다. 최소이미지로 잰다.
      · **슬랩원소 가드** — Li/Ni 는 SDCP 분자에 없는 원소다. 화학흡착 결합(O–Ni)을
        타고 자라는 것을 원소 수준에서 차단한다. (전이된 H 가 붙든 표면 O 하나를
        같이 물든 그건 조성 출력에 드러난다 — 조용히 붕괴하는 것과 다르다.)
      · **붕괴 판정** — 그래도 분자 조각이 전체의 절반을 넘으면 분할이 무너진 것이다.
        조용히 통과시키지 않고 ⛔ 를 찍고 exit 1 (판정 도구는 판정을 남긴다).
    """
    n = len(elems)
    r = np.array([RCOV.get(e, 1.0) for e in elems])
    inv = np.linalg.inv(cell)
    df = (pos[:, None, :] - pos[None, :, :]) @ inv
    df -= np.round(df)                                   # 최소이미지 (MIC)
    d = np.linalg.norm(df @ cell, axis=-1)
    bond = d < BOND_SCALE * (r[:, None] + r[None, :])
    np.fill_diagonal(bond, False)
    metal = np.array([e in SLAB_ONLY for e in elems])
    mol = np.array([e in MOL_SEED for e in elems])
    while True:                                          # 씨앗에 붙은 O 까지 흡수
        grown = (mol | (bond & mol[None, :]).any(axis=1)) & ~metal
        if (grown == mol).all():
            break
        mol = grown
    if (~mol).any() and mol.any():
        comp = {}
        for e in np.array(elems)[mol]:
            comp[e] = comp.get(e, 0) + 1
        comp_s = "".join(f"{e}{c}" for e, c in sorted(comp.items()))
        # 붕괴의 실제 서명 = **슬랩 O 를 대량 흡수** (Li/Ni 는 위에서 원소로 막았다).
        # 크기 비율(n/2)로 재면 작은 시험계에서 오판하므로 조성으로 잰다:
        # v7c 분자 자체 O 6개 + H-전이로 표면 O 1개까지 = 정상 상한 MOL_O_MAX.
        n_o = comp.get("O", 0)
        if n_o > MOL_O_MAX:
            raise SystemExit(
                f"⛔ 분자/슬랩 분할 붕괴 — 분자 조각({comp_s})의 O 가 {n_o}개 "
                f"(정상 상한 {MOL_O_MAX} = 자체 6 + H-전이 여유). flood-fill 이 표면 O 를 "
                f"연쇄 흡수했다. BOND_SCALE({BOND_SCALE})/씨앗을 점검할 것. "
                "이 상태의 ①②③ 판정은 전부 무의미하다 — 여기서 멈춘다.")
        if n_o == 7:
            print(f"  ⚠ 분자 조각({comp_s})의 O 가 7개 — 자체 6개 + 표면 O 하나를 물었다. "
                  "H-전이 흔적이면 정상. 아니면 분할 의심.")
    return mol


def unwrap_fragment(cell, pos, sel):
    """`sel` 조각을 PBC 로 **한 덩어리로 편다**(unwrap). 나머지 원자는 그대로.

    ⚠⚠ **③ 면내 피복이 이것 없이는 오탐한다 (2026-08-28 실측).** 분자가 셀 경계를
      걸치면 그 분자의 *내부 결합*이 shift (-1,0,0) 에서 보인다. `same=True` 는
      (0,0,0) 만 빼므로 그 결합이 "옆 셀 분자와 1.369 Å" 으로 찍혔다 —
      **C-F 1.369 Å 은 접촉이 아니라 공유결합이다.** 16개 중 8개가 이렇게 ⚠ 를 달았다.
      (①②는 안전하다: ① 은 서로 다른 집합이고, ② 는 sh_z != 0 만 보는데 분자는 z 로
      감기지 않는다. 그래서 ③ 에만 편 좌표를 쓴다.)

    ⛔ 못 하는 것: 조각이 결합으로 안 이어져 있으면(끊어진 분자) 이어진 부분만 편다.
    """
    idx = np.flatnonzero(sel)
    if len(idx) < 2:
        return pos.copy()
    inv = np.linalg.inv(cell)
    out = pos.copy()
    seen = {int(idx[0])}
    stack = [int(idx[0])]
    r = None
    while stack:
        i = stack.pop()
        d = pos[idx] - out[i]
        f = d @ inv
        f -= np.round(f)
        dm = f @ cell
        dist = np.linalg.norm(dm, axis=1)
        if r is None:
            r = 3.0                                  # Å — 결합 상한(가장 긴 것이 S-O ~1.8)
        for k, j in enumerate(idx):
            j = int(j)
            if j in seen or dist[k] > r:
                continue
            out[j] = out[i] + dm[k]
            seen.add(j); stack.append(j)
    return out


#: 재중심 후 분자의 분율 span 이 이 값을 넘으면 한 셀 안에 담기지 않는다 → 경고하고 포기.
MOL_SPAN_MAX = 0.95


def recenter_on_fragment(cell, pos, sel):
    """`sel` 조각이 **셀 가운데(면내 0.5, 0.5)** 에 오도록 전 원자를 평행이동한다.

    왜 필요한가 (2026-08-28, 실측 제보): 분자가 셀 경계에 걸쳐 있으면 VESTA 기본
    Boundary(0–1)에서 **분자가 두 조각으로 잘려 보인다.** 실제로 16개 전부 그랬다
    (ptfe 계열은 a 축, sdcp_neutral 은 b 축으로 갈림).

    ⚠ **좌표는 물리적으로 동일하다** — 주기 평행이동은 대칭 조작이다. 에너지·거리·
      결합 무엇도 안 바뀐다. 다만 OUTCAR 원문과 숫자가 달라지므로 이동량을 파일
      주석에 남긴다 (`--no_recenter` 로 끌 수 있다).

    ⚠ z 는 건드리지 않는다. 슬랩+진공은 c 방향으로 감으면 슬랩이 잘린다.

    → (pos_new, dfrac | None). 담을 수 없으면 (원본, None).
    """
    inv = np.linalg.inv(cell)
    un = unwrap_fragment(cell, pos, sel)
    # ⚠ 감김(주기 결합) 검출 — 셀보다 긴 조각은 반드시 경계를 돌아 자기와 이어진다.
    #   그런 조각은 BFS 로 한 덩어리로 펼 수 없다(일관된 배치가 존재하지 않는다):
    #   MIC 로는 결합인 쌍이 편 좌표에서는 멀어진다. 그때는 포기한다 — 조용히 자르지 않는다.
    idx = np.flatnonzero(sel)
    df = (pos[idx][:, None, :] - pos[idx][None, :, :]) @ inv
    df -= np.round(df)
    d_mic = np.linalg.norm(df @ cell, axis=-1)
    d_un = np.linalg.norm(un[idx][:, None, :] - un[idx][None, :, :], axis=-1)
    bonded = (d_mic < 3.0) & ~np.eye(len(idx), dtype=bool)
    if bonded.any() and (d_un[bonded] > d_mic[bonded] + 0.5).any():
        return pos, None                        # 감겨 있다 — 이동으로는 못 고친다
    f = un[sel] @ inv
    span = f.max(axis=0) - f.min(axis=0)
    if (span[:2] >= MOL_SPAN_MAX).any():
        return pos, None                        # 한 셀보다 길다 — 이동으로는 못 고친다
    com = f.mean(axis=0)
    d = np.array([0.5 - com[0], 0.5 - com[1], 0.0])
    out = (un + d @ cell)
    fo = out @ inv
    fo[:, :2] -= np.floor(fo[:, :2])            # 면내만 접는다
    out = fo @ cell
    # 접는 과정에서 분자가 다시 갈릴 수 있다 (경계에 딱 걸친 원자) — 한 번 더 편다.
    return unwrap_fragment(cell, out, sel), d


def write_xyz(path, elems, pos, comment):
    with open(path, "w") as f:
        f.write(f"{len(elems)}\n{comment}\n")
        for e, p in zip(elems, pos):
            f.write(f"{e:<3s} {p[0]:16.8f} {p[1]:16.8f} {p[2]:16.8f}\n")


def write_poscar(path, cell, order, counts, pos, comment):
    with open(path, "w") as f:
        f.write(comment.replace("\n", " ") + "\n1.0\n")
        for v in cell:
            f.write(f"  {v[0]:18.12f} {v[1]:18.12f} {v[2]:18.12f}\n")
        f.write("  " + "  ".join(order) + "\n")
        f.write("  " + "  ".join(str(c) for c in counts) + "\n")
        f.write("Cartesian\n")
        for p in pos:
            f.write(f"  {p[0]:18.12f} {p[1]:18.12f} {p[2]:18.12f}\n")



# ═══ VESTA 프리셋 ═══════════════════════════════════════════════════════════
# 사용자의 기존 SDCP 분자 .vesta (ORCA 판) 양식을 그대로 승계한다 — C/S/O/H 의
# 반지름·색이 같아야 분자 그림끼리 나란히 놓을 수 있다. 여기에 슬랩 원소만 더한다.
#   (radius, R,G,B, R2,G2,B2)   뒤 3색은 VESTA 보조색
VSTYLE = {
    "C":  (0.35,  76,  76,  76, 128,  73,  41),
    "S":  (0.48, 255, 250,   0, 255, 250,   0),
    "O":  (0.38, 254,   3,   0, 254,   3,   0),
    "H":  (0.20, 255, 255, 255, 255, 204, 204),
    "Li": (0.42,  70, 175,  90,  70, 175,  90),
    "Ni": (0.46,  40,  90, 200,  40,  90, 200),
    # F 는 사용자의 기존 분자 .vesta 에 없던 원소다 (PTFE 조각이 처음). VESTA 기본 F 는
    # 옅은 연두라 **흰 배경에서 사라진다**(Ni 절반이 안 보였던 그 실측과 같은 함정) —
    # 진한 청록으로 둔다. S(노랑)·O(빨강)·Li(초록)·Ni(파랑/보라)와 안 겹친다.
    "F":  (0.32,   0, 160, 180,   0, 160, 180),
}
# ⚠ **반지름은 셀 크기에 맞춰 키워야 한다 (2026-08-03 실측).** 위 값은 ~10 A 분자용이라
#   11.5 x 18.3 x 28.8 A 결정 셀에 그대로 쓰면 화면의 1% 짜리 **점**이 된다. 비율은
#   분자 .vesta 와 같게 두고 전체를 상수배 한다 → 분자 그림과 상대 크기가 유지된다.
RAD_SCALE_DEFAULT = 1.7
# ⚠ scf.in 은 Ni1/Ni2 (AFM 부격자)를 라벨로 구분해 들고 있다. .vasp/.xyz 로 나갈 때는
#   원소 Ni 로 뭉개지지만 **.vesta 는 site 단위 색을 쓰므로 부격자를 살릴 수 있다** —
#   NiO6 팔면체가 파랑/회색으로 갈리면 반강자성 배치가 그림에서 바로 읽힌다.
# ⚠ **흰 배경에 옅은 회색을 쓰면 원자가 사라진다 (실측: Ni 절반이 안 보였다).**
#   AFM 쌍은 파랑/보라로 — 둘 다 흰 배경에서 진하고, O(빨강)·S(노랑)·Li(초록)와 안 겹친다.
NI_SUB = {"Ni1": (40, 90, 200), "Ni2": (150, 60, 170)}
# (A1, A2, max_len, show_polyhedra)
VBONDS = [("Ni", "O", 2.40, 1),   # NiO6 팔면체 + 분자 O 와의 흡착결합(1.89 A)도 여기서 그려진다
          ("Li", "O", 2.60, 0),
          ("C", "C", 1.70, 0), ("C", "H", 1.15, 0), ("C", "O", 1.65, 0),
          ("C", "S", 1.95, 0), ("S", "O", 1.80, 0), ("O", "H", 1.10, 0),
          ("C", "F", 1.60, 0)]      # PTFE 조각 — C-F 는 1.33~1.36 A


def write_vesta(path, cell, labels, elems, pos, title, scale=RAD_SCALE_DEFAULT):
    """CRYSTAL 형식 .vesta. 좌표는 **분율**이어야 한다 (MOLECULE 판은 Cartesian).

    ⚠ CLAUDE.md: .vesta 는 **ASCII 전용 + CRLF**. 비ASCII 한 글자가 파싱을 깨뜨린 전례가
      있으므로 이 함수가 쓰는 문자열에는 한글·em-dash 를 절대 넣지 않는다.
    """
    a, b, c = (np.linalg.norm(v) for v in cell)
    ang = lambda u, v: np.degrees(np.arccos(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))))
    al, be, ga = ang(cell[1], cell[2]), ang(cell[0], cell[2]), ang(cell[0], cell[1])
    frac = pos @ np.linalg.inv(cell)

    # 사이트 라벨: 참조 .vesta 와 같은 **영숫자만** 쓴다 (밑줄/비ASCII 는 파싱 위험).
    #   AFM 부격자는 색으로도 갈리지만 라벨에도 남긴다 — NiA = spin up, NiB = spin down.
    seen, site_lab = {}, []
    for e, lb in zip(elems, labels):
        stem = {"Ni1": "NiA", "Ni2": "NiB"}.get(lb, e)
        seen[stem] = seen.get(stem, 0) + 1
        site_lab.append(f"{stem}{seen[stem]}")

    L = ["#VESTA_FORMAT_VERSION 3.5.4", "", "", "CRYSTAL", "", "TITLE",
         title.encode("ascii", "replace").decode("ascii"), "", "GROUP", "1 1 P 1  ", "SYMOP",
         " 0.000000  0.000000  0.000000  1  0  0   0  1  0   0  0  1   1",
         " -1.0 -1.0 -1.0  0 0 0  0 0 0  0 0 0", "TRANM 0",
         " 0.000000  0.000000  0.000000  1  0  0   0  1  0   0  0  1", "LTRANSL", " -1",
         " 0.000000  0.000000  0.000000  0.000000  0.000000  0.000000", "LORIENT",
         " -1   0   0   0   0",
         " 1.000000  0.000000  0.000000  1.000000  0.000000  0.000000",
         " 0.000000  0.000000  1.000000  0.000000  0.000000  1.000000", "LMATRIX",
         " 1.000000  0.000000  0.000000  0.000000", " 0.000000  1.000000  0.000000  0.000000",
         " 0.000000  0.000000  1.000000  0.000000", " 0.000000  0.000000  0.000000  1.000000",
         " 0.000000  0.000000  0.000000", "CELLP",
         f"  {a:9.6f}  {b:9.6f}  {c:9.6f}  {al:9.6f}  {be:9.6f}  {ga:9.6f}",
         "  0.000000   0.000000   0.000000   0.000000   0.000000   0.000000", "STRUC"]
    for i, (e, sl, f) in enumerate(zip(elems, site_lab, frac), 1):
        L.append(f"  {i:3d}  {e:<2s}  {sl:>10s}  1.0000  {f[0]:10.6f} {f[1]:10.6f} "
                 f"{f[2]:10.6f}    1        -")
        L.append("                            0.000000   0.000000   0.000000  0.00")
    L += ["  0 0 0 0 0 0 0", "THERI 1"]
    for i, sl in enumerate(site_lab, 1):
        L.append(f"  {i:3d} {sl:>10s} -0.000000")
    L += ["  0 0 0", "SHAPE",
          "  0       0       0       0   0.000000  0   192   192   192   192", "BOUND",
          "       0        1         0        1         0        1", "  0   0   0   0  0",
          "SBOND"]
    present = set(elems)
    n = 0
    for a1, a2, mx, poly in VBONDS:
        if a1 not in present or a2 not in present:
            continue
        n += 1
        # ⚠ 플래그는 **사용자의 기존 .vesta 와 한 글자도 다르지 않게** `0 1 1 0 1` 로 둔다.
        #   그 파일이 정상 렌더되는 known-good 조합이다. 여기를 임의로 0 으로 바꿨더니
        #   결합이 안 그려졌다(실측) — 이 5개 정수의 의미를 추측으로 건드리지 않는다.
        #   boundary_mode(2번째)=1 이라 **셀 경계를 넘는 결합**도 그려진다. 이 계의
        #   흡착결합이 실제로 shift (1,1,0) 이므로 이게 0 이면 분자가 떠 보인다.
        L.append(f"  {n}  {a1:>5s} {a2:>5s}    0.00000  {mx:9.5f}  0  1  1  0  1  "
                 f"{0.110 * scale:.3f}  0.000 127 127 127")
    L += ["  0 0 0 0", "SITET"]
    for i, (e, lb, sl) in enumerate(zip(elems, labels, site_lab), 1):
        rad, r1, g1, b1, r2, g2, b2 = VSTYLE.get(e, (0.40, 160, 160, 160, 160, 160, 160))
        rad *= scale
        if lb in NI_SUB:
            r1, g1, b1 = NI_SUB[lb]; r2, g2, b2 = r1, g1, b1
        L.append(f"  {i:3d} {sl:>10s}  {rad:.4f} {r1:3d} {g1:3d} {b1:3d} "
                 f"{r2:3d} {g2:3d} {b2:3d}  50  0")
    L += ["  0 0 0 0 0 0", "VECTR", " 0 0 0 0 0", "VECTT", " 0 0 0 0 0", "SPLAN",
          "  0   0   0   0", "LBLAT", " -1", "LBLSP", " -1", "DLATM", " -1", "DLBND", " -1",
          "DLPLY", " -1", "PLN2D", "  0   0   0   0", "ATOMT"]
    for k, e in enumerate(sorted(present, key=lambda x: list(elems).index(x)), 1):
        rad, r1, g1, b1, r2, g2, b2 = VSTYLE.get(e, (0.40, 160, 160, 160, 160, 160, 160))
        rad *= scale
        L.append(f"  {k}  {e:>9s}  {rad:.4f} {r1:3d} {g1:3d} {b1:3d} {r2:3d} {g2:3d} {b2:3d}  50")
    # SCENE: c 축을 화면 위로 세운 측면 시점 (슬랩은 위에서 보면 층이 안 보인다)
    L += ["  0 0 0 0 0 0", "SCENE",
          " 1.000000  0.000000  0.000000  0.000000", " 0.000000  0.000000  1.000000  0.000000",
          " 0.000000 -1.000000  0.000000  0.000000", " 0.000000  0.000000  0.000000  1.000000",
          "  0.000   0.000", "  0.000", "  1.000", "HBOND 0 2", "", "STYLE",
          "DISPF 37749698", "MODEL   0  1  0", "SURFS   0  1  1", "SECTS  32  1",
          "FORMS   0  1", "ATOMS   0  0  1", "BONDS   1", "POLYS   1", "VECTS 1.000000",
          "FORMP", "  1  1.0   0   0   0", "ATOMP", " 24  24   0  50  2.0   0", "BONDP",
          f"  1  16  {0.110 * scale:.3f}  0.000 127 127 127", "POLYP", "  50 1  0.030 150 150 150",
          "ISURF", "  0   0   0   0", "TEX3P", "  1         -INF         -INF", "SECTP",
          "  1  5.00000E-01  5.00000E-01  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00",
          "CONTR", " 0.1 -1 1 1 10 -1 2 5", " 2 1 2 1", "   0   0   0", "   0   0   0",
          "   0   0   0", "   0   0   0", "HKLPP", " 192 1  1.000 255   0 255", "UCOLP",
          "   0   0  1.000   0   0   0", "COMPS 0", "LABEL 1    12  1.000 0", "PROJT 0  0.962",
          "BKGRC", " 255 255 255", "DPTHQ 0 -0.5000  3.5000", "LIGHT0 1"]
    ident = [" 1.000000  0.000000  0.000000  0.000000", " 0.000000  1.000000  0.000000  0.000000",
             " 0.000000  0.000000  1.000000  0.000000", " 0.000000  0.000000  0.000000  1.000000",
             " 0.000000  0.000000 20.000000  0.000000", " 0.000000  0.000000 -1.000000"]
    L += ident + ["  26  26  26 255", " 179 179 179 255", " 255 255 255 255"]
    for k in (1, 2, 3):
        L += [f"LIGHT{k}"] + ident + ["   0   0   0   0"] * 3
    L += ["SECCL 0", "", "TEXCL 0", "", "ATOMM", " 204 204 204 255", "  25.600", "BONDM",
          " 255 255 255 255", " 128.000", "POLYM", " 255 255 255 255", " 128.000", "SURFM",
          "   0   0   0 255", " 128.000", "FORMM", " 100 100 100 255", "  44.800", "HKLPM",
          " 255 255 255 255", " 128.000", ""]
    body = "\n".join(L)
    assert body.isascii(), "non-ASCII leaked into .vesta"
    with open(path, "w", encoding="ascii", newline="\r\n") as f:
        f.write(body)


def pair_min(cell, labels, pos, sel_a, sel_b, layer, same=False):
    """sel_a ↔ sel_b 최소 거리. `layer` 로 어떤 이미지를 볼지 고른다.

    ⚠⚠ **이 함수의 layer 분리가 이 도구의 전부다. 두 번 틀렸다 (2026-08-03).**

      1차 오판 — 전 원자쌍을 훑어 슬랩의 면내 격자 결합(Ni–O 1.94 Å, Ni–Ni 2.88 Å)을
        '이미지 샌드위치'로 찍었다. 슬랩은 a·b 로 주기적인 결정이라 그 결합은 정상이다.
      2차 오판 — 반대로 흡착거리를 **자기 셀 안에서만** 재서, 셀 모서리 근처에 앉은
        분자의 진짜 결합상대(shift (1,1,0) 의 Ni, 1.887 Å)를 놓치고 6.348 Å 을 보고
        "떠 있다"고 판정했다. 슬랩은 면내로 **연속된 하나의 표면**이다.

      물리적으로 옳은 분리는 이것뿐이다:
        layer='surface' (sh_z == 0, 자기 셀 포함) → **진짜 표면**. 흡착 접촉거리.
        layer='vacuum'  (sh_z != 0)              → **진공 너머의 인공 두 번째 표면**.
                                                    2026-07-17 샌드위치 철회의 그 축.
    """
    ia, ib = np.flatnonzero(sel_a), np.flatnonzero(sel_b)
    if not len(ia) or not len(ib):
        return None
    best = None
    for sh in itertools.product((-1, 0, 1), repeat=3):
        if layer == "surface" and sh[2] != 0:
            continue
        if layer == "vacuum" and sh[2] == 0:
            continue
        # ⚠ 같은 집합끼리 비교할 때 (0,0,0) 은 **분자 내부 결합**(C–H 1.08 Å 등)을 집는다.
        #   대각선만 지우는 걸로는 부족하다 — 그 shift 자체를 빼야 이미지 접촉만 남는다.
        if same and sh == (0, 0, 0):
            continue
        d = np.linalg.norm(pos[ia][:, None, :]
                           - (pos[ib][None, :, :] + np.array(sh) @ cell), axis=-1)
        i, j = np.unravel_index(np.argmin(d), d.shape)
        rec = (d[i, j], labels[ia[i]], labels[ib[j]], sh)
        if best is None or rec[0] < best[0]:
            best = rec
    return best


def default_tag(path):
    """출력 접두어. OUTCAR 은 `<job>/<phase>/OUTCAR.gz` 라 **두 단계 위**가 잡 이름이다."""
    if is_outcar(path):
        d = os.path.dirname(os.path.abspath(path))
        return f"{os.path.basename(os.path.dirname(d))}__{os.path.basename(d)}"
    if path.lower().endswith((".xyz", ".extxyz")):
        return os.path.splitext(os.path.basename(path))[0]
    return os.path.basename(os.path.dirname(os.path.abspath(path)))


def emit_struct(path, out, tag=None, scale=RAD_SCALE_DEFAULT, quiet=False, recenter=True):
    """한 계산 → xyz + .vasp + .vesta + 거리 세 층 감사. → meta(dict)"""
    tag = tag or default_tag(path)
    meta = {}
    if is_outcar(path):
        cell, labels0, pos0, meta = read_outcar(path)
        prov = (f"as-run geometry read back from {meta['source']} "
                f"(VASP static single point, NSW=0) | "
                f"E(sigma->0)={meta['E0']:.6f} eV | mag_tot={meta['mag_total']} muB | "
                f"slab magnetic basin={meta['basin']}")
    else:
        cell, labels0, pos0 = read_any(path)
        prov = f"UNRELAXED single-point geometry from {os.path.abspath(path)}"
    elems0 = [element(x) for x in labels0]
    elems, labels, pos, order, counts = group_by_species(elems0, labels0, pos0)

    # ── 분자를 셀 가운데로 (뷰어에서 안 잘리게). 물리적으로 동일한 평행이동이다.
    rec_note = ""
    if recenter:
        mol0 = split_molecule(cell, elems, pos)
        if mol0.any() and (~mol0).any():
            pos2, d = recenter_on_fragment(cell, pos, mol0)
            if d is None:
                print(f"  ⚠ {tag}: 분자 면내 span 이 셀의 {MOL_SPAN_MAX:.0%} 이상 — "
                      "재중심으로 못 담는다. 원본 좌표 유지 (뷰어에서 Boundary 를 넓힐 것)")
            else:
                pos = pos2
                rec_note = (f" | recentered: molecule COM moved to cell center, "
                            f"shift frac=({d[0]:+.4f},{d[1]:+.4f},0) — same structure, "
                            f"coords differ from OUTCAR by this lattice translation")

    c_len = np.linalg.norm(cell[2])
    span = pos[:, 2].max() - pos[:, 2].min()
    comment = (f"{tag} | nat={len(elems)} | cell a={np.linalg.norm(cell[0]):.3f} "
               f"b={np.linalg.norm(cell[1]):.3f} c={c_len:.3f} A | "
               f"z-span={span:.3f} A | vertical vacuum={c_len - span:.3f} A | {prov}{rec_note}")
    os.makedirs(out, exist_ok=True)
    write_xyz(os.path.join(out, f"{tag}.xyz"), elems, pos, comment)
    write_poscar(os.path.join(out, f"{tag}.vasp"), cell, order, counts, pos, comment)
    # ⚠ .vesta 제목은 ASCII 만 (CLAUDE.md). basin 라벨은 영숫자라 안전하다.
    vt = (f"{tag} (nat {len(elems)}) - as-run geometry, NiO6 polyhedra + "
          f"AFM sublattice colors (NiA blue / NiB purple)")
    if meta:
        vt += f" - basin {meta['basin']}, E0 {meta['E0']:.4f} eV"
    write_vesta(os.path.join(out, f"{tag}.vesta"), cell, labels, elems, pos, vt, scale=scale)
    meta.update({"tag": tag, "nat": len(elems), "out": out})
    if not quiet:
        _audit(cell, labels, elems, pos, order, counts, tag, out, c_len, span)
    return meta


def _audit(cell, labels, elems, pos, order, counts, tag, out, c_len, span):
    print(f"\n══ {tag}  (nat {len(elems)}) ══")
    print(f"  cell  a {np.linalg.norm(cell[0]):.3f}  b {np.linalg.norm(cell[1]):.3f}"
          f"  c {c_len:.3f} A     z-span {span:.3f} → 수직 진공 {c_len - span:.3f} A")
    print(f"  xyz 와 vasp 는 **같은 원자 순서·같은 좌표** ({'+'.join(f'{e}{c}' for e, c in zip(order, counts))})")

    mol = split_molecule(cell, elems, pos)
    if not (mol.any() and (~mol).any()):
        print("  (단일 조각 — 분자/슬랩 분할 없음)")
        print(f"  → {out}/{tag}.xyz + .vasp + .vesta")
        return

    # ── ⓪ z 단면: 슬랩 위에 얹혀 있는 게 맞나 ───────────────────────────
    zs, zm = pos[~mol][:, 2], pos[mol][:, 2]
    print(f"  ⓪ z 범위  슬랩 [{zs.min():6.2f}, {zs.max():6.2f}]   "
          f"분자 [{zm.min():6.2f}, {zm.max():6.2f}]  (A)")

    # ── ① 흡착 접촉 — **면내 주기를 포함한** 진짜 표면과의 거리 ──────────
    ads = pair_min(cell, labels, pos, mol, ~mol, "surface")
    print(f"  ① 흡착 접촉  분자({mol.sum()}) ↔ 표면({(~mol).sum()})  "
          f"{ads[0]:.3f} A  ({ads[1]}↔{ads[2]}, shift {ads[3]})")
    print("     (슬랩은 면내로 연속된 하나의 표면 — shift 가 (±1,±1,0) 이어도 같은 표면이다)")
    if ads[0] < 2.5:
        print("     ✓ 화학흡착 (결합거리)")
    elif ads[0] < 3.2:
        print("     ✓ 근접 접촉")
    elif ads[0] < 4.0:
        print("     ⚠ 물리흡착 경계 — 화학결합 없음")
    else:
        print("     ⛔ 4 A 초과 — 접촉이 아니다. 흡착 자세가 아니라 떠 있는 것이다.")

    # ── ② 진공 너머 = 인공 두 번째 표면 (2026-07-17 철회의 그 축) ────────
    vac_s = pair_min(cell, labels, pos, mol, ~mol, "vacuum")
    vac_m = pair_min(cell, labels, pos, mol, mol, "vacuum", same=True)
    print(f"  ② 진공 너머 (c 를 넘는 이미지만)  분자↔슬랩 {vac_s[0]:.3f} A "
          f"(shift {vac_s[3]})  ·  분자↔분자 {vac_m[0]:.3f} A")
    img = min(vac_s[0], vac_m[0])
    if img < 2.5:
        print("     ⛔ 결합거리 — 이미지 샌드위치. 이 자세의 E_bind 는 단일표면 값이 아니다.")
    elif img < 3.5:
        print("     ⚠ vdW 접촉 — E_bind 에 이미지 상호작용이 섞인다. 진공을 키울 것.")
    else:
        print("     ✓ 진공 분리 확보 (2026-07-17 철회 사유 없음)")

    # ── ③ 면내 피복 — 분자끼리 옆 셀에서 닿나 ───────────────────────────
    #    ⚠ 편 좌표로 잰다. 안 그러면 셀 경계를 걸친 분자의 내부 결합을 접촉으로 센다.
    lat = pair_min(cell, labels, unwrap_fragment(cell, pos, mol), mol, mol,
                   "surface", same=True)
    print(f"  ③ 면내 피복  분자 ↔ 옆 셀 분자 {lat[0]:.3f} A "
          f"({lat[1]}↔{lat[2]}, shift {lat[3]})"
          f"{'  ⚠ 3.5 A 미만 — 피복률이 너무 높다' if lat[0] < 3.5 else ''}")
    ss = pair_min(cell, labels, pos, ~mol, ~mol, "surface", same=True)
    print(f"     [참고] 슬랩 ↔ 옆 셀 슬랩 {ss[0]:.3f} A ({ss[1]}↔{ss[2]}) = 격자 결합, 정상")
    print(f"  → {out}/{tag}.xyz + .vasp + .vesta")


# ══ 잡 이름 · 에너지 표 ════════════════════════════════════════════════════════
#: E_ads 를 만들지 않는 조각과 그 사유. **코드에 박는다** — 카드에 적어두면 9일이면
#: 잊힌다(사각 D, 처방 E). 뚫으려면 --allow_not_citable 을 명시해야 한다.
NOT_CITABLE = {
    "sdcp_doped": "상태 미선언 다중해 — mol_doped 총자화 0.175(doublet 이면 1.000, "
                  "ISMEAR=1/SIGMA=0.2 를 고립분자에 건 결과). 2026-08-28 회신 M/N",
}
CSV_COLS = ["job", "role", "fragment", "pose", "seed_branch", "phase", "n_ions",
            "E_total_eV", "mag_total_muB", "slab_basin", "slab_ref_job",
            "E_slab_ref_eV", "mol_ref_job", "E_mol_ref_eV", "E_ads_eV", "note"]


def job_fields(job):
    """wave1 디렉터리 이름 → (role, fragment, pose, seed_branch).

    ⚠ 이 도구가 못 하는 것: 이름이 규약을 안 지키면 role='unknown' 으로 두고 **추측하지
      않는다**. 잘못 추측한 role 은 잘못된 기준을 빼는 것과 같다.
    """
    p = job.split("__")
    if job.startswith("mol__"):
        # pose 칸에 상자 크기를 적는다 — 정본은 box24, box20 은 상자 수렴 점검용이다.
        return "mol_ref", p[1], (p[2] if len(p) > 2 else ""), ""
    if job.startswith("clean_slab"):
        m = re.search(r"afm\d+_(\w+)$", job)
        return "slab_ref", "clean_slab", "", (m.group(1) if m else "")
    if len(p) >= 4:
        m = re.search(r"afm\d+_(\w+)$", p[-1])
        return "complex", p[0], p[2], (m.group(1) if m else "")
    return "unknown", p[0], "", ""


def collect_refs(refs_dir):
    """refs/ → ({('slab',branch,basin,phase)|('mol',frag,box,phase): (job, E)}, [meta…])

    ⚠ 슬랩 basin 은 파일 이름이 아니라 **수렴된 총자화**로 정한다. 이름의 `basinA` 는
      의도이지 결과가 아니다 — wave1.5 에서 net4 가 의도와 다른 basin 으로 떨어진 것이
      회신 M P0 의 출발점이었다.
    """
    out, metas = {}, []
    if not refs_dir or not os.path.isdir(refs_dir):
        return out, metas
    for job in sorted(os.listdir(refs_dir)):
        for phase in ("static", "dense"):
            p = os.path.join(refs_dir, job, phase, "OUTCAR.gz")
            if not os.path.isfile(p) and not os.path.isfile(p[:-3]):
                continue
            _c, _l, pos, meta = read_outcar(p)
            meta.update(tag=f"{job}__{phase}", nat=len(pos))
            metas.append(meta)
            role, frag, box, tail = job_fields(job)
            if role == "slab_ref":
                out[("slab", tail.split("_")[0], meta["basin"], phase)] = (job, meta["E0"])
            elif role == "mol_ref":
                out[("mol", frag, box, phase)] = (job, meta["E0"])
    return out, metas


def energy_rows(metas, refs, allow_not_citable=False):
    """잡 meta 목록 + refs → CSV 행. E_ads 를 못 만들면 **빈칸 + 사유**를 남긴다.

    규약 (2026-08-28, 레지스트리와 일치 확인됨):
      · 정본 분자 기준은 **box24** (box20 은 상자 수렴 점검용).
      · dense 상의 E_ads 는 dense 슬랩 + **static 분자** — 진공 상자 분자는 Γ 하나라
        k 를 늘려도 같은 값이다. c10 에서 이 규약이 E_ads 0.22 meV · ΔE_site 0.003 meV
        를 재현한다(citable 파일의 "k 직접검증 ΔE 0.0 · E_ads 0.2 meV").
      · net4 는 슬랩 basin(A≈4 · B≈6 μB)을 **복합체 총자화로 맞춰서** 뺀다. 안 맞추면
        슬랩 basin gap 49.718 meV 가 차에 섞인다 (회신 M P0).
    """
    rows = []
    for m in sorted(metas, key=lambda x: x["tag"]):
        job, phase = m["tag"].rsplit("__", 1)
        role, frag, pose, branch = job_fields(job)
        r = dict.fromkeys(CSV_COLS, "")
        r.update(job=job, role=role, fragment=frag, pose=pose, seed_branch=branch,
                 phase=phase, n_ions=m["nat"], E_total_eV=f"{m['E0']:.6f}",
                 mag_total_muB=f"{m['mag_total']:.6f}" if m["mag_total"] is not None else "",
                 slab_basin=m["basin"])
        notes = []
        if not m.get("normal_end"):
            notes.append("⛔ OUTCAR 정상종료 없음")
        if role == "complex":
            slab = refs.get(("slab", branch, m["basin"], phase)) \
                or refs.get(("slab", branch, m["basin"], "static"))
            mol = refs.get(("mol", frag, "box24", "static"))
            if m["basin"] == "unresolved":
                notes.append("자기 basin 미판정 — 기준 슬랩을 맞출 수 없다")
            elif slab is None:
                notes.append(f"기준 슬랩 없음 (branch={branch}, basin={m['basin']})")
            if mol is None:
                notes.append(f"기준 분자 없음 (mol__{frag}__box24)")
            if frag in NOT_CITABLE and not allow_not_citable:
                notes.append("⛔ E_ads 생략: " + NOT_CITABLE[frag])
            elif slab and mol:
                r["slab_ref_job"], r["E_slab_ref_eV"] = slab[0], f"{slab[1]:.6f}"
                r["mol_ref_job"], r["E_mol_ref_eV"] = mol[0], f"{mol[1]:.6f}"
                r["E_ads_eV"] = f"{m['E0'] - slab[1] - mol[1]:.6f}"
                if phase == "dense":
                    notes.append("dense-k: 슬랩은 dense, 분자는 static(Γ 하나라 k 무관)")
        r["note"] = " · ".join(notes)
        rows.append(r)
    return rows


#: CSV 인코딩 — repo 규약(tools/ionic/*.py 다수와 동일). ⚠ 이것 없이 쓰면 **Excel 이
#: UTF-8 을 못 알아보고 한글 note 열이 깨진다** (2026-08-28 실측 제보). Origin 도 같다.
CSV_ENCODING = "utf-8-sig"


#: 감사 키에 없지만 **이 캠페인의 판정에 직접 걸리는** 것들. 특히
#:  · SIGMA  — phaseB 의 mol_doped 0.175 를 만든 그 키 (ISMEAR 와 짝으로만 의미가 있다)
#:  · NELECT — 회신 O 재승인 조건 ① 이 명시적으로 요구하는 값
#:  · NSW    — 단일점인지 이완인지 (기하 승계 서술의 근거)
INCAR_EXTRA = ("SIGMA", "NELECT", "NELM", "EDIFF", "PREC", "NBANDS", "NSW", "KSPACING")


def read_incar_echo(path):
    """OUTCAR 의 INCAR 되울림 → dict. 감사키 + INCAR_EXTRA.

    ⛔ 못 하는 것: MAGMOM·ADDGRID 는 VASP 가 안 되울린다 — 원리적으로 None 이다
      (통과도 실패도 아닌 **unverified**). INCAR 원본이 회수되지 않은 드롭에서는
      그 두 키를 확인할 방법이 아예 없다.
    """
    ns = _analyzer()
    t, _ = ns["_last_run_segment"](ns["_read_outcar_raw"](path)[0])
    out = {k: ns["_echo_val"](t, k) for k in ns["AUDIT_KEYS_RUNTIME"]}
    for k in INCAR_EXTRA:
        m = re.search(r"(?m)^\s{2,}" + k + r"\s*=\s*([^\n;|]+?)(?:\s{2,}\w+\s*=|$)", t)
        out[k] = m.group(1).strip() if m else None
    # ⚠ SIGMA 는 자기 줄이 없다 — `ISMEAR = 0;   SIGMA = 0.05 ...` 처럼 ISMEAR 줄에
    #   붙어 나온다. 위 일반 패턴이 못 잡아 36잡 전부 공란이 됐고, 회신 P 가 그 공란을
    #   "동일" 로 승격한 fail-open 을 잡았다. 전용 패턴으로 따로 읽는다.
    if out.get("SIGMA") is None:
        m = re.search(r"ISMEAR\s*=\s*-?\d+\s*;\s*SIGMA\s*=\s*([\d.Ee+-]+)", t)
        out["SIGMA"] = m.group(1) if m else None
    return out


#: OUTCAR 이 원리적으로 되울리지 않는 키 — '없음' 이 아니라 **미검증**이다.
ECHO_NEVER = ("MAGMOM", "ADDGRID")


def incar_key_status(rows):
    """잡별 INCAR echo → 키별 **검증 상태** 5분류 (회신 P P0 — fail-closed 스키마).

    ⛔⛔ 왜 이 함수가 따로 있나 (2026-08-28 회신 P P0, 실제 사고):
      종전 incar_diff 는 "값이 갈린 키" 만 돌려줬다. 그러면 **전부 공란인 키**
      (SIGMA·KSPACING·NBANDS·NELM — 파싱 실패)가 갈린 키 목록에 안 나타나, 호출부가
      그것을 "36잡 동일" 로 읽었다. **미검증을 통과로 승격한 fail-open** 이다.
      이제 상태를 먼저 가르고, 갈림(diff)은 verified 인 키에서만 정의한다.

    → {key: {"status": verified_equal|verified_different|all_missing_unverified|
              partial_missing|not_applicable,
             "values": {value: [job…]} (verified 만), "n_missing": int}}
    """
    keys = sorted({k for r in rows for k in r if k not in ("job", "role", "fragment")})
    out = {}
    for k in keys:
        vals, miss = {}, []
        for r in rows:
            v = r.get(k)
            if v is None or v == "":
                miss.append(r["job"])
            else:
                vals.setdefault(str(v), []).append(r["job"])
        if k in ECHO_NEVER and not vals:
            st = "not_applicable"          # OUTCAR 이 원리적으로 안 되울림 — 별도 표기
        elif not vals:
            st = "all_missing_unverified"  # 파싱 실패/부재 — ⛔ '동일' 로 읽으면 안 된다
        elif miss:
            st = "partial_missing"
        elif len(vals) > 1:
            st = "verified_different"
        else:
            st = "verified_equal"
        out[k] = {"status": st, "values": vals, "n_missing": len(miss)}
    return out


def incar_diff(rows, key_of=lambda r: r["job"]):
    """잡별 INCAR echo → **검증된 값이 실제로 갈린 키만**.

    ⚠ 이 함수는 갈림만 본다 — 공란/미검증 판정은 incar_key_status() 몫이고,
      호출부는 반드시 둘을 같이 보고해야 한다 (회신 P: "전부 공란" ≠ "전부 동일").
    """
    diff = {}
    for k, st in incar_key_status(rows).items():
        if st["status"] == "verified_different":
            diff[k] = st["values"]
    return diff


def write_energy_csv(path, rows):
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    with open(path, "w", newline="", encoding=CSV_ENCODING) as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLS)
        w.writeheader()
        for r in rows:
            w.writerow(r)


# ══ selftest ═════════════════════════════════════════════════════════════════
_OUT_HEAD = """ vasp.6.3.0 fake
   VRHFIN =Li: 1s2s2p
   TITEL  = PAW_PBE Li_sv 10Sep2004
   VRHFIN =C: s2p2
   TITEL  = PAW_PBE C 08Apr2002
   ions per type =               2   1
   NIONS = 3
"""


def _fake_outcar(e_final=-20.0, e_scf=-10.0, nat=3, counts="2   1", banner=None,
                 lattice="10.0 0.0 0.0\n     0.0 10.0 0.0\n     0.0 0.0 10.0"):
    """전자스텝과 최종 블록이 **다른 값**인 OUTCAR (LDA+U 함정 재현)."""
    body = (_OUT_HEAD.replace("ions per type =               2   1",
                              f"ions per type =               {counts}")
            + f"  energy without entropy =  {e_scf}  energy(sigma->0) =  {e_scf}\n"
            + "      direct lattice vectors                 reciprocal lattice vectors\n"
            + "     " + lattice.replace("\n", "  0 0 0\n") + "  0 0 0\n"
            + " POSITION                                       TOTAL-FORCE (eV/Angst)\n"
            + " ---------------------------------------------------------------\n"
            + "".join(f"   {1.0 + i:.5f}  {2.0:.5f}  {3.0:.5f}   0.0 0.0 0.0\n"
                      for i in range(nat))
            + " ---------------------------------------------------------------\n"
            + " magnetization (x)\n\n# of ion       s       p       d       tot\n"
            + "------------------------------------------\n"
            + "".join(f"    {i + 1}        0.0   0.0   0.0   {0.5 if i % 2 == 0 else -0.5}\n"
                      for i in range(nat))
            + "\n  FREE ENERGIE OF THE ION-ELECTRON SYSTEM (eV)\n"
            + f"  free  energy   TOTEN  =  {e_final} eV\n"
            + f"  energy  without entropy=  {e_final}  energy(sigma->0) =  {e_final}\n"
            + " number of electron    10.0000000 magnetization       6.0000000\n"
            + " General timing and accounting\n")
    return (banner + body) if banner else body


def selftest():
    import tempfile
    fails = []

    def chk(ok, msg):
        print(("  ✓ " if ok else "  ✗ ") + msg)
        if not ok:
            fails.append(msg)

    print("── scfin_to_struct selftest ──")
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "OUTCAR")
        open(p, "w").write(_fake_outcar())
        cell, labels, pos, meta = read_outcar(p)

        # ★ 양성 — 기본 판독
        chk(len(pos) == 3 and [element(x) for x in labels] == ["Li", "Li", "C"],
            "OUTCAR → 원소 배정 (TITEL + ions per type)")
        chk(abs(cell[0][0] - 10.0) < 1e-9, "OUTCAR → 셀")

        # ⛔ 음성 1 — **전자스텝 TOTEN 을 읽으면 안 된다** (LDA+U 이중계산 함정).
        #    실측 28.6 eV 차. 여기서 -10 을 잡으면 그 버그가 재발한 것이다.
        chk(abs(meta["E0"] - (-20.0)) < 1e-9,
            f"에너지는 **최종 이온스텝** 블록 (전자스텝 -10 이 아니라 -20): {meta['E0']}")

        # ⛔ 음성 2 — ions per type 합이 POSITION 원자수와 다르면 멈춘다
        p2 = os.path.join(td, "bad_counts", "OUTCAR")
        os.makedirs(os.path.dirname(p2))
        open(p2, "w").write(_fake_outcar(counts="2   5"))
        try:
            read_outcar(p2); ok = False
        except SystemExit:
            ok = True
        chk(ok, "음성: ions per type 합 ≠ POSITION 원자수 → 멈춘다")

        # ⛔ 음성 3 — 이어붙은 OUTCAR 는 **마지막 완결 실행**만 (옛 값이 이기면 안 된다)
        p3 = os.path.join(td, "appended", "OUTCAR")
        os.makedirs(os.path.dirname(p3))
        open(p3, "w").write(_fake_outcar(e_final=-33.0)
                            + _fake_outcar(e_final=-44.0, banner=" vasp.6.3.0 second run\n"))
        chk(abs(read_outcar(p3)[3]["E0"] - (-44.0)) < 1e-9,
            "음성: 이어붙은 OUTCAR 는 마지막 실행(-44) — 첫 실행(-33) 아님")

        # basin 분류: 범위 밖은 판정하지 않는다 (fail-closed)
        chk(basin_of(3.999) == "A" and basin_of(5.999) == "B" and basin_of(0.0003) == "pm1",
            "basin 분류 A/B/pm1")
        chk(basin_of(4.9) == "unresolved" and basin_of(None) == "unresolved",
            "음성: basin 범위 밖·결측 → unresolved (가까운 쪽으로 반올림하지 않는다)")

        # ⛔ 음성 4 — basin 이 unresolved 면 E_ads 를 만들지 않는다
        refs = {("slab", "net4", "A", "static"): ("clean_slab__afm2424_net4_basinA", -100.0),
                ("mol", "ptfe_c10", "box24", "static"): ("mol__ptfe_c10__box24", -10.0)}
        base = dict(nat=3, normal_end=True, E0=-111.5)
        good = dict(base, tag="ptfe_c10__d__Litop__afm2424_net4__static",
                    mag_total=4.0, basin="A")
        bad = dict(base, tag="ptfe_c10__d__Litop__afm2424_net4__static",
                   mag_total=4.9, basin="unresolved")
        rg = energy_rows([good], refs)[0]
        rb = energy_rows([bad], refs)[0]
        chk(abs(float(rg["E_ads_eV"]) - (-1.5)) < 1e-9, "E_ads = 복합체 − 슬랩(basin) − 분자")
        chk(rb["E_ads_eV"] == "" and "basin" in rb["note"],
            "음성: basin 미판정이면 E_ads 빈칸 + 사유 (기본 basin 으로 때우지 않는다)")

        # ⛔ 음성 5 — NOT_CITABLE 조각은 E_ads 를 만들지 않는다
        refs2 = dict(refs)
        refs2[("mol", "sdcp_doped", "box24", "static")] = ("mol__sdcp_doped__box24", -10.0)
        dop = dict(base, tag="sdcp_doped__d__Litop__afm2424_net4__static",
                   mag_total=4.0, basin="A")
        rd = energy_rows([dop], refs2)[0]
        chk(rd["E_ads_eV"] == "" and "인용 불가" not in rd["note"] and "생략" in rd["note"],
            "음성: NOT_CITABLE 조각은 E_ads 빈칸 (총에너지는 남긴다)")
        chk(energy_rows([dop], refs2, allow_not_citable=True)[0]["E_ads_eV"] != "",
            "--allow_not_citable 로만 뚫린다")

        # ⛔ 음성 6 — 셀 경계를 걸친 분자의 **내부 결합**을 면내 피복으로 세면 안 된다
        #    (2026-08-28 실측: C-F 1.369 Å 이 "옆 셀 분자와 접촉" 으로 찍혀 16개 중 8개가
        #     ⚠ 를 달았다. 1.369 Å 은 접촉이 아니라 공유결합이다.)
        cellb = np.eye(3) * 10.0
        # C-F 두 원자가 경계를 사이에 두고 1.4 Å (9.8 과 0.2 -> 랩된 좌표로는 9.6 Å 떨어져 보임)
        posb = np.array([[9.8, 5.0, 5.0], [0.4, 5.0, 5.0]])
        selb = np.array([True, True])
        naive = pair_min(cellb, ["C", "F"], posb, selb, selb, "surface", same=True)
        fixed = pair_min(cellb, ["C", "F"], unwrap_fragment(cellb, posb, selb),
                         selb, selb, "surface", same=True)
        chk(abs(naive[0] - 0.6) < 1e-6,
            f"(재현) 편기 전에는 내부 결합이 면내 접촉으로 보인다: {naive[0]:.3f} A")
        chk(fixed[0] > 9.0,
            f"음성: 편 좌표로는 옆 셀 분자까지 {fixed[0]:.3f} A — 내부 결합을 안 센다")

        # ★ 재중심 — 경계를 걸친 분자가 셀 가운데로 오고, 전 원자가 [0,1) 안에 있다
        #   (2026-08-28 실측 제보: VESTA 기본 Boundary 0-1 에서 분자가 두 조각으로 보였다)
        cellr = np.eye(3) * 10.0
        posr = np.array([[5.0, 5.0, 2.0],            # 슬랩 역할 (Li)
                         [9.8, 5.0, 6.0], [0.9, 5.0, 6.0]])   # 경계 걸친 C-F (wrap 1.1 A)
        elr = ["Li", "C", "F"]
        selr = np.array([False, True, True])
        pr, dr = recenter_on_fragment(cellr, posr, selr)
        fr = pr @ np.linalg.inv(cellr)
        chk(dr is not None and abs(pr[1][0] - pr[2][0]) < 2.0,
            f"재중심 후 분자가 한 덩어리 (C-F 간격 {abs(pr[1][0]-pr[2][0]):.2f} A, 종전 8.9)")
        chk((fr[1:, :2] > 0.05).all() and (fr[1:, :2] < 0.95).all(),
            "재중심 후 분자 전체가 셀 내부 (기본 Boundary 0-1 에서 안 잘림)")
        chk(abs(pr[0][2] - 2.0) < 1e-9 and abs(pr[1][2] - 6.0) < 1e-9,
            "z 는 안 건드린다 (슬랩+진공 방향)")

        # ⛔ 음성 8 — 경계를 돌아 자기와 이어진(감긴) 조각은 재중심으로 못 담는다.
        #   셀보다 긴 사슬은 반드시 이 형태가 된다 (끝끼리 MIC 로 결합거리 안).
        posl = np.array([[0.1 + 2.4 * i, 5.0, 5.0] for i in range(5)])   # 0.1..9.7, 끝 간격 0.4
        sell = np.ones(5, bool)
        pl, dl = recenter_on_fragment(cellr, posl, sell)
        chk(dl is None and np.allclose(pl, posl),
            "음성: 감긴(주기 결합) 조각 → 재중심 포기(원본 유지), 조용히 절단하지 않는다")

        # ⛔ 음성 10 (회신 P P0 — 실제 사고 재현) — **전부 공란인 키를 '동일' 로
        #   승격하면 안 된다.** 종전 incar_diff 는 SIGMA 전 잡 공란을 갈린 키 목록에서
        #   빼서, 호출부가 "36잡 동일" 로 읽었다. fail-open 이었다.
        ir0 = [{"job": "a", "role": "complex", "fragment": "x", "SIGMA": None, "ENCUT": "520"},
               {"job": "b", "role": "mol_ref", "fragment": "x", "SIGMA": None, "ENCUT": "520"}]
        st0 = incar_key_status(ir0)
        chk(st0["SIGMA"]["status"] == "all_missing_unverified",
            "음성(회신 P): 전 잡 공란 키는 all_missing_unverified — verified_equal 아님")
        chk(st0["ENCUT"]["status"] == "verified_equal", "값이 실제로 같은 키만 verified_equal")
        st1 = incar_key_status([dict(ir0[0], SIGMA="0.05"), ir0[1]])
        chk(st1["SIGMA"]["status"] == "partial_missing",
            "음성: 일부만 공란이면 partial_missing — 그 잡들은 미검증")
        st2 = incar_key_status([{"job": "a", "role": "c", "fragment": "x", "MAGMOM": None}])
        chk(st2["MAGMOM"]["status"] == "not_applicable",
            "MAGMOM 은 OUTCAR 이 원리적으로 안 되울림 — not_applicable 로 분리")

        # ⛔ 음성 9 — incar_diff 는 **갈린 키만** 집어야 한다 (같은 키를 오탐하면
        #   진짜 비대칭이 노이즈에 묻힌다). 실제로 이 검사가 LREAL T/F 를 찾아냈다.
        ir = [{"job": "complex", "role": "complex", "fragment": "x",
               "LREAL": "T", "ENCUT": "520", "NUPDOWN": "-1"},
              {"job": "mol", "role": "mol_ref", "fragment": "x",
               "LREAL": "F", "ENCUT": "520", "NUPDOWN": "0"}]
        dd = incar_diff(ir)
        chk(set(dd) == {"LREAL", "NUPDOWN"},
            f"incar_diff 가 갈린 키만 집는다 (ENCUT 는 같으니 제외): {sorted(dd)}")
        chk(dd["LREAL"] == {"T": ["complex"], "F": ["mol"]},
            "incar_diff 가 어느 잡이 어느 값인지 보존한다")
        chk(incar_diff([ir[0], dict(ir[0], job="c2")]) == {},
            "음성: 전부 같으면 빈 dict — 없는 차이를 만들지 않는다")

        # ⛔ 음성 7 — CSV 에 BOM 이 없으면 Excel 이 한글 note 열을 깨뜨린다 (실측 제보)
        cp = os.path.join(td, "e.csv")
        write_energy_csv(cp, [dict(rg, note="한글 사유")])
        head = open(cp, "rb").read(3)
        chk(head == b"\xef\xbb\xbf", f"음성: CSV 는 utf-8-sig(BOM) — repo 규약. 실제 앞 3바이트 {head!r}")

        # 구조 3종이 실제로 써지고, .vesta 는 ASCII 전용 + CRLF (CLAUDE.md)
        emit_struct(p, os.path.join(td, "o"), quiet=True)
        vp = os.path.join(td, "o", os.listdir(os.path.join(td, "o"))[0])
        vp = [x for x in os.listdir(os.path.join(td, "o")) if x.endswith(".vesta")][0]
        raw = open(os.path.join(td, "o", vp), "rb").read()
        chk(raw.decode("ascii", "ignore").encode() == raw and b"\r\n" in raw,
            ".vesta 는 ASCII 전용 + CRLF")

    print(f"── {'PASS' if not fails else 'FAIL ' + str(len(fails))} ──")
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scf_in", nargs="+", default=[],
                    help="QE scf.in 또는 Phase-A pose .xyz (확장자로 자동 판별)")
    ap.add_argument("--outcar", nargs="+", default=[],
                    help="VASP OUTCAR / OUTCAR.gz (결과만 회수된 드롭용)")
    ap.add_argument("--out", default=None)
    ap.add_argument("--tag", default=None, help="출력 접두어 (기본: 상위 디렉터리명)")
    ap.add_argument("--vesta_scale", type=float, default=RAD_SCALE_DEFAULT,
                    help="VESTA 원자 반지름 배율. 셀이 크면 키운다 (기본 1.7)")
    ap.add_argument("--energy_csv", default=None,
                    help="--outcar 전용. 잡별 총에너지·E_ads 표 (Origin-ready)")
    ap.add_argument("--refs", default=None,
                    help="refs/ 디렉터리 (clean_slab__* · mol__*). E_ads 에 필요")
    ap.add_argument("--allow_not_citable", action="store_true",
                    help=f"NOT_CITABLE 조각({'/'.join(NOT_CITABLE)})의 E_ads 도 계산")
    ap.add_argument("--incar_csv", default=None,
                    help="--outcar 전용. 잡별 INCAR 되울림 표 + 갈린 키 요약")
    ap.add_argument("--no_recenter", action="store_true",
                    help="분자 재중심(뷰어에서 안 잘리게) 끄기 — OUTCAR 원문 좌표 그대로")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.scf_in or a.outcar):
        ap.error("--scf_in 또는 --outcar 중 하나는 필요하다")
    if a.energy_csv and not a.refs:
        ap.error("--energy_csv 는 --refs 가 있어야 한다 (기준 없이 E_ads 를 만들지 않는다)")

    metas = []
    for path in list(a.scf_in) + list(a.outcar):
        if a.out:
            metas.append(emit_struct(path, a.out, tag=a.tag, scale=a.vesta_scale,
                                     recenter=not a.no_recenter))
        else:
            cell, labels, pos, meta = read_outcar(path)
            meta.update(tag=default_tag(path), nat=len(pos))
            metas.append(meta)

    if a.incar_csv:
        paths = list(a.outcar)
        if a.refs and os.path.isdir(a.refs):
            for job in sorted(os.listdir(a.refs)):
                for ph in ("static", "dense"):
                    q = os.path.join(a.refs, job, ph, "OUTCAR.gz")
                    if os.path.isfile(q) or os.path.isfile(q[:-3]):
                        paths.append(q)
        irows = []
        for q in paths:
            tag = default_tag(q)
            job, phase = tag.rsplit("__", 1)
            role, frag, _pose, _b = job_fields(job)
            r = {"job": job + "__" + phase, "role": role, "fragment": frag}
            r.update(read_incar_echo(q))
            irows.append(r)
        cols = ["job", "role", "fragment"] + sorted(set(k for r in irows for k in r)
                                                    - {"job", "role", "fragment"})
        os.makedirs(os.path.dirname(os.path.abspath(a.incar_csv)) or ".", exist_ok=True)
        with open(a.incar_csv, "w", newline="", encoding=CSV_ENCODING) as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for r in irows:
                w.writerow({k: ("" if r.get(k) is None else r[k]) for k in cols})
        print(f"\n══ INCAR 되울림 {len(irows)}잡 → {a.incar_csv} ══")
        stat = incar_key_status(irows)
        groups = {}
        for k, st in stat.items():
            groups.setdefault(st["status"], []).append(k)
        eq = sorted(groups.get("verified_equal", []))
        print(f"  ✓ verified_equal ({len(eq)}): {', '.join(eq)}")
        # ⛔ 회신 P P0 — 공란을 '동일' 로 승격하지 않는다. 미검증은 미검증으로 찍는다.
        for st_name, mark in (("verified_different", "⚠"),
                              ("partial_missing", "⚠"),
                              ("all_missing_unverified", "⛔"),
                              ("not_applicable", "⛔")):
            ks = sorted(groups.get(st_name, []))
            if not ks:
                continue
            if st_name == "verified_different":
                for k in ks:
                    by = stat[k]["values"]
                    print(f"  {mark} **{k}** 이 {len(by)}가지로 갈림 (verified_different):")
                    for v, jobs in sorted(by.items(), key=lambda x: -len(x[1])):
                        short = ", ".join(j.split("__")[0] + "/" + j.split("__")[-1]
                                          for j in jobs[:4])
                        print(f"      {v!s:<28s} ({len(jobs)}잡) {short}"
                              f"{' …' if len(jobs) > 4 else ''}")
            else:
                note = {"partial_missing": "일부 잡에서 공란 — 그 잡들은 미검증",
                        "all_missing_unverified": "전 잡 공란 — 파싱 실패/부재. '동일' 아님",
                        "not_applicable": "OUTCAR 이 원리적으로 안 되울림 — 확인 불가"}[st_name]
                print(f"  {mark} {st_name} ({len(ks)}): {', '.join(ks)} — {note}")
        n_bad = len(groups.get("all_missing_unverified", [])) + len(groups.get("not_applicable", []))
        print(f"  ⛔ '전수 통과' 는 말할 수 없다 — 미검증 키 {n_bad}개가 남는 한 "
              f"이 표는 verified 키에 대해서만 말한다 (회신 P P0)")

    if a.energy_csv:
        refs, ref_metas = collect_refs(a.refs)
        print(f"\n══ 기준 {len(refs)}건 ({a.refs}) ══")
        for m in ref_metas:                          # 기준도 표에 남긴다 — 뺄셈이 파일 안에서 재현되게
            print(f"  {m['tag']:<46s} E0 {m['E0']:14.6f}  mag {m['mag_total']:8.4f}  basin {m['basin']}")
        rows = energy_rows([m for m in metas + ref_metas if m.get("E0") is not None], refs,
                           a.allow_not_citable)
        write_energy_csv(a.energy_csv, rows)
        n_ads = sum(1 for r in rows if r["E_ads_eV"])
        print(f"  → {a.energy_csv}  ({len(rows)}행 · E_ads {n_ads}건)")
        print("  ⚠ 이 표는 OUTCAR **원문 판독값**이다 — 게이트 통과 판정이 아니다. "
              "인용 자격은 db/properties/sdcp_wave1_citable.json 이 정한다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
