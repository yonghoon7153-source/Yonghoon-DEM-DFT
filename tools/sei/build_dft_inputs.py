#!/usr/bin/env python3
"""build_dft_inputs.py — SEI 상들의 **갭 + DOS/PDOS** QE 입력 일괄 생성.

체인 (조성마다)
  ① vc-relax  — MP 구조는 VASP/PAW 로 이완된 것이라 우리 QE/USPP 평형부피와 다르다.
                 부피가 다르면 갭이 움직이므로 먼저 우리 조건으로 이완한다. (셀이 작아 싸다)
  ② scf       — 이완된 기하에서
  ③ **nscf (occupations='fixed', 조밀 k)** — ★ 갭은 **여기서 VBM/CBM 고유값으로만** 낸다
  ④ nscf + dos.x     — 전체 DOS (그림용)
  ⑤ projwfc.x        — PDOS (원소·궤도 분해)

⚠⚠ **갭을 DOS 문턱으로 읽지 말 것** (CLAUDE.md 규율). DOS 는 Gaussian 퍼짐 때문에
  ~0.3 eV 과소평가된다. 갭의 정본은 ③의 고유값이고, DOS/PDOS 는 **그림과 성분 분해용**이다.

⚠ PBE 갭은 이 계열(넓은 갭 절연체)에서 계통적으로 30–50% 과소평가된다.
  실험값과 나란히 놓지 말고 **6종 사이의 상대 비교**와 같은 방법의 문헌값 대조로 쓴다.

⚠ Nd 계열(LiNdO₂·Nd₂O₃·Nd₂S₃): 우리 pseudo 는 z_valence=14 로 **4f 가 valence** 다.
  PBE 만으로는 4f 가 E_F 에 걸려 갭이 무의미해진다. 우리 repo 노트가 이미
  "PBE+U 는 Nd 4f 를 잘못 배치하고, **갭 가장자리가 4f 면 실패한다**" 고 적어 놓았고
  이 세 상이 정확히 그 경우다. → `--nd_u` 로 U 를 걸 수는 있지만 **기본은 진단용**이며,
  최종 수치는 MP 의 frozen-4f 값을 출처 명시해 인용하는 편이 정직하다.

  python3 tools/sei/build_dft_inputs.py                 # 입력 생성 + pseudo 점검
  python3 tools/sei/build_dft_inputs.py --nd_u 6.0      # Nd 4f 에 U (진단용)
"""
import argparse
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import electronic_class as EC          # noqa: E402  (금속/절연체 단일 출처)

ECUTWFC, ECUTRHO = 60.0, 480.0        # Ry — USPP/PAW 기준 (pseudo 요구 최대 47/326 위)
KDENS_SCF, KDENS_NSCF = 0.30, 0.15    # Å⁻¹ 간격 — 갭용 nscf 를 2배 조밀하게
# ⚠ DOS/PDOS 용 nscf 는 **대칭을 끄고**(projwfc 의 d_matrix 회피) 돌아야 하는데,
#   그러면 k 점이 전부 명시적으로 풀려 폭증한다. 갭만큼 조밀할 필요도 없으므로 성기게.
KDENS_DOS = 0.28
DEGAUSS = 0.01                        # Ry — scf 만 (nscf 는 fixed)
WORK = "/data/work/runs/sei_dft"
PROV = "db/properties/sei_structures_provenance.json"


def zval(path):
    """UPF 헤더에서 z_valence. nbnd 를 정하려면 전자 수를 알아야 한다."""
    import re
    try:
        head = open(path, errors="ignore").read(6000)
    except OSError:
        return None
    # ⛔⛔ 2026-08-11 — 옛 정규식 `[\d.]+` 가 **과학표기를 잘랐다**. psl kjpaw UPF 는
    #   z_valence="1.100000000000E+01" 로 쓰는데 E 앞에서 끊겨 Nd 가 **1.1 전자**가 됐다.
    #   그 값이 nbnd 를 정하므로: lindo2 nbnd 51(필요 53)·nd2s3 62(필요 81) → 03/04 전멸.
    #   nd2o3 는 nbnd 21 = 필요 21, **여유 0밴드**로 우연히 살았다 (값 3.948 은 유효하나
    #   재실행으로 견고화할 것). build_neb_inputs.zval 은 처음부터 넓은 정규식이라 무사.
    m = re.search(r'z_valence\s*=\s*"?\s*([\d.eEdD+-]+)', head, re.I)
    if m:
        return float(m.group(1).replace("D", "E").replace("d", "e"))
    m = re.search(r"([\d.eEdD+-]+)\s+Z valence", head, re.I)  # UPF v1 텍스트 헤더
    return float(m.group(1).replace("D", "E").replace("d", "e")) if m else None


#: ⛔ PP 핀 — build_neb_inputs.py 의 PP_PIN 과 **같은 값이어야 한다**.
#:   bulk(여기) → endpoint → NEB 가 서로 다른 PP 로 돌면 기하를 승계할 수 없다
#:   (Codex 재리뷰: "open-4f+U bulk 좌표를 frozen-4f NEB 가 승계할 수 있다").
PP_PIN = {"Nd": "Nd.pbe-spdn-kjpaw_psl.1.0.0.UPF"}

# ── 열린 껍질 전이금속 (2026-10-27 · CEI 생성물 갭 카드) ───────────────────────
#: 이 원소가 들어간 상은 **자성 상태를 선언해야** 갭이 정의된다 (자성 배치 · U 가 여럿이면
#:   스칼라 갭이 없다 — CLAUDE.md 보고량 규율). 선언 없이 오면 입력을 **안 만든다**.
OPEN_SHELL_TM = ("V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu")
#: MP 의 GGA+U 규약 — U 는 **O·F 가 있는 계에서만** 3d 에 건다 (pymatgen MPRelaxSet).
#:   숫자는 기억값이라 gabia 블록에서 pymatgen 설정으로 대조한다. 표에 없는 원소는 추측하지
#:   않고 멈춘다. ⚠ VASP(PAW 사영)의 U 를 QE ortho-atomic 사영에 같은 숫자로 건다 —
#:   **같은 상태가 아니다**. MP 갭과의 대조는 '같은 자릿수·같은 순위' 로만 한다.
MP_U_3D = {"Co": 3.32, "Mn": 3.9, "Ni": 6.2}
MP_U_ANIONS = ("O", "F")
MAG_THR = 0.1           # μB — 이보다 작은 자리 모멘트는 '모멘트 없음'


def el_of(label):
    """종 라벨 → 원소 (`Mn1` → `Mn`)."""
    return re.sub(r"\d+$", "", label)


def magmom_sidecar(path):
    """구조 파일 옆 `<base>.magmom.json` (fetch_sei_structures --pick --with_magnetism) 또는 None."""
    p = os.path.splitext(path)[0] + ".magmom.json"
    return json.load(open(p)) if os.path.isfile(p) else None


def species_from_magmoms(symbols, magmoms, thr=MAG_THR):
    """자리별 MP 모멘트 → (자리별 종 라벨, {라벨: 평균 모멘트 μB}).

    QE 는 씨앗 모멘트를 **종** 단위로 준다. 한 원소에 + 와 − 가 같이 있으면(반강자성)
    `El1`(+) · `El2`(−) · `El3`(|m|≤thr) 로 나눈다 — 안 나누면 평균이 0 이 돼 강자성·비자성
    씨앗으로 둔갑한다. 부호가 하나뿐인 원소는 라벨을 원소 그대로 둔다(옛 입력과 같은 꼴).
    ⛔ 못 하는 것: MP 배치가 바닥상태인지 모른다 — 'MP 가 계산한 상태' 를 옮길 뿐이다.
    """
    if len(symbols) != len(magmoms):
        raise ValueError(f"자리 수 {len(symbols)} ≠ 모멘트 수 {len(magmoms)}")
    split = set()
    for e in set(symbols):
        ms = [m for s, m in zip(symbols, magmoms) if s == e]
        if any(m > thr for m in ms) and any(m < -thr for m in ms):
            split.add(e)
    labels = []
    for s, m in zip(symbols, magmoms):
        if s in split:
            labels.append(s + ("1" if m > thr else "2" if m < -thr else "3"))
        else:
            labels.append(s)
    mean = {}
    for lab in sorted(set(labels)):
        ms = [m for l_, m in zip(labels, magmoms) if l_ == lab]
        mean[lab] = sum(ms) / len(ms)
    return labels, mean


def ecut_for(elements, ecut_min):
    """이 상의 (ecutwfc, ecutrho) — 기본 60/480 과 원소별 바닥값(--ecut_min) 중 큰 것."""
    w, r = ECUTWFC, ECUTRHO
    for e in elements:
        if e in ecut_min:
            w, r = max(w, ecut_min[e][0]), max(r, ecut_min[e][1])
    return w, r


def parse_ecut_min(items):
    """['Mn=65,780'] → {'Mn': (65.0, 780.0)}. 틀린 꼴은 멈춘다."""
    out = {}
    for it in items or []:
        m = re.fullmatch(r"([A-Z][a-z]?)=(\d+(?:\.\d+)?),(\d+(?:\.\d+)?)", it.strip())
        if not m:
            raise ValueError(f"--ecut_min '{it}': 'El=wfc,rho' 꼴이어야 한다 (예 Mn=65,780)")
        out[m.group(1)] = (float(m.group(2)), float(m.group(3)))
    return out


def hubbard_mp_lines(species, elements):
    """MP 규약 U 줄 (QE HUBBARD 카드 본문). O·F 가 없으면 [] (MP 는 황화물에 U 를 안 건다).

    표(MP_U_3D)에 없는 열린 껍질 TM 이 O·F 와 같이 오면 **멈춘다** — U 를 추측하지 않는다.
    """
    if not any(a in elements for a in MP_U_ANIONS):
        return []
    miss = sorted(e for e in elements if e in OPEN_SHELL_TM and e not in MP_U_3D)
    if miss:
        raise ValueError(f"MP U 표에 없는 원소 {miss} — 추측하지 않는다")
    return [f"  U {s}-3d {MP_U_3D[el_of(s)]}" for s in species if el_of(s) in MP_U_3D]


def tag_of(path):
    """구조 파일 경로 → 태그. `sei_` 접두는 **있으면** 벗기고, 확장자는 **무엇이든** 벗긴다.

    ⛔⛔ 2026-09-17 — 옛 코드는 `basename[len("sei_"):-len(".vasp")]` 로 **길이로 잘랐다.**
      접두/확장자가 그 형태일 때만 맞고, 아니면 앞 4글자·뒤 5글자를 그냥 먹는다:
        `NdPO4_mp-aaaaafhw.cif` → `O4_mp-aaaaaf`   ← 오류 없이 조용히 틀린 태그
      그 태그가 prefix·outdir·electronic_class 조회에 전부 쓰이므로, 갭 게이트가
      `unregistered` 로 빠지고 산출물 폴더 이름도 쓰레기가 된다. 길이가 아니라
      **모양으로** 자른다.

    ⛔ 이 함수가 못 하는 것: 태그가 레지스트리 키와 맞는지 **확인하지 않는다**
      (그건 electronic_class.normalize 몫이다 — `_mp-...` 는 거기서 떨어진다).
    """
    b = os.path.basename(path)
    if b.startswith("sei_"):
        b = b[len("sei_"):]
    return os.path.splitext(b)[0]


def find_pseudos(pdir):
    """pseudo 디렉터리에서 원소 → 파일명. ⚠ 없는 원소는 그대로 보고한다.

    ⛔ 알파벳 첫 번째를 고르던 옛 동작은 함정이었다 — frozen-4f 를 넣어도
      `Nd.paw.z_14...` 가 `Nd.pbe-spdn...` 보다 앞서서 옛 PP 가 계속 이긴다.
    """
    out = {}
    files = sorted(os.listdir(pdir))
    for f in files:
        if not f.lower().endswith((".upf",)):
            continue
        el = f.split(".")[0].split("_")[0]
        el = el[0].upper() + el[1:].lower() if len(el) > 1 else el.upper()
        out.setdefault(el, f)
    for el, want in PP_PIN.items():
        if el not in out:
            continue
        if want in files:
            if out[el] != want:
                print(f"   ★ {el} PP 를 핀으로 교체: {out[el]} → {want}")
            out[el] = want
        else:
            print(f"   ⛔ {el} 핀({want})이 없다 — 이 원소를 뺀다 "
                  f"(옛 {out[el]} 로 조용히 돌지 않는다)")
            out.pop(el)
    return out


def kmesh(cell, dens):
    import numpy as np
    b = 2 * np.pi * np.linalg.inv(cell).T
    # ⚠ round 를 쓰면 비 1.35 가 1 로 내려가 그 축이 Γ-only 가 된다(실측: Nd2S3 [5,3,1]).
    #   장축이라도 k=2 는 싸므로 ceil 로 올림해 안전하게 간다.
    return [max(1, int(np.ceil(np.linalg.norm(v) / dens))) for v in b]


def make_control_structures(a, files):
    """--supercell / --rattle_seeds → 파생 .vasp 를 만들고 그 경로 목록을 돌려준다.

    회신 I (2026-08-27) §2 P0-2 · 실행순서 3 의 control 용:
      *"pristine 3×3×3 에 대칭 끄고 rattle 여러 개 → 이완. 같은 Nd 패턴이 나오면
        끝점부터 다시."*
    공공이 **없는** 셀에서도 같은 재배열이 나오면 원인은 공공이 아니라 셀 자체의
    soft mode 이고, 그러면 cc333 의 두 끝점이 애초에 무효다.

    rattle 은 **결정론적**이다 (`default_rng(seed)`) — 같은 명령이 같은 구조를 준다.
    seed 0 = 무변형 기준선(순수 초격자). 기준선이 있어야 "rattle 이 만든 것"과
    "초격자가 원래 그런 것"을 가른다.

    ⛔ 이 함수가 못 하는 것:
      · 대칭이 실제로 깨졌는지 **검사하지 않는다** (nosym 은 QE 쪽 플래그일 뿐이다).
      · 이완이 원본 대칭으로 되돌아가는지 못 본다 — 그건 이완 **결과** 분석 몫이다.
      · rattle 크기가 soft mode 를 깨우기에 충분한지 보장하지 않는다. 너무 작으면
        원위치로 돌아가고, 너무 크면 무관한 국소최소로 떨어진다. 여러 크기가 필요하면
        --rattle 을 바꿔 여러 번 돌려라.
    """
    import numpy as np
    from ase.io import read, write
    sc = [int(x) for x in a.supercell.split()] if a.supercell else [1, 1, 1]
    if len(sc) != 3 or any(x < 1 for x in sc):
        sys.exit(f"⛔ --supercell '{a.supercell}': 양의 정수 3개여야 한다")
    if a.rattle_seeds and a.rattle <= 0:
        sys.exit("⛔ --rattle_seeds 를 줬는데 --rattle 이 0 이다 — 변형 없는 사본만 K개 나온다")
    ctl = os.path.join(a.work, "_control_structures")
    os.makedirs(ctl, exist_ok=True)
    out = []
    for f in files:
        base = tag_of(f)
        prim = read(f)
        for s in range(0, a.rattle_seeds + 1):
            at = prim * tuple(sc)
            if s > 0:
                rng = np.random.default_rng(s)
                at.positions = at.positions + rng.normal(0.0, a.rattle, at.positions.shape)
            p = os.path.join(ctl, f"sei_{base}_p{''.join(map(str, sc))}_r{s}.vasp")
            write(p, at, format="vasp", direct=True)
            out.append(p)
            print(f"  control 구조 {os.path.basename(p)} — {len(at)}원자 · "
                  f"rattle {a.rattle if s else 0.0:.3f} Å (seed {s})")
    return out


def selftest():
    """태그 유도 · pseudo 핀 · 갭 게이트를 확인한다. **음성 경로 포함.**

    ⚠ 양성만 있는 selftest 는 통과해도 아무것도 보증하지 않는다 (CLAUDE.md 코드 규율).
      그래서 각 항목마다 "옛 동작이었다면 무엇이 틀렸을까" 를 같이 넣는다.
    """
    import electronic_class as _EC
    bad = []

    def eq(got, want, what):
        if got != want:
            bad.append(f"{what}: {got!r} ≠ {want!r}")

    # ① 태그 유도 — 접두 있음/없음 × 확장자 vasp/cif
    eq(tag_of("db/structures/sei_li2o_mp-1960.vasp"), "li2o_mp-1960", "sei_+vasp")
    eq(tag_of("db/structures/cei_gap_targets/NdPO4_mp-aaaaafhw.cif"),
       "NdPO4_mp-aaaaafhw", "접두없음+cif")
    eq(tag_of("LiNdPO34_mp-aaaabbrr.cif"), "LiNdPO34_mp-aaaabbrr", "접두없음+cif(Li)")
    eq(tag_of("/tmp/P2O5.cif"), "P2O5", "mp-id 없음")
    eq(tag_of("sei_x_p333_r1.vasp"), "x_p333_r1", "control 파생본")
    # ② 음성 — 옛 길이 슬라이싱이 내던 값이 **지금은 안 나와야** 한다
    old = lambda f: __import__("os").path.basename(f)[len("sei_"):-len(".vasp")]
    if old("NdPO4_mp-aaaaafhw.cif") == tag_of("NdPO4_mp-aaaaafhw.cif"):
        bad.append("음성① 옛 길이슬라이싱과 결과가 같다 — 수정이 안 걸렸다")
    #   ⚠ 이 고정값은 내가 손으로 센 것을 selftest 가 **틀렸다고 잡아준 것**이다
    #     (2026-09-17: "O4_mp-aaaaaf" 로 적었는데 실제는 [4:-5] = "4_mp-aaaaafh").
    eq(old("NdPO4_mp-aaaaafhw.cif"), "4_mp-aaaaafh", "음성① 옛 동작 재현(고정값)")
    # ③ 태그가 electronic_class 키로 정규화되는지 — 갭 게이트가 여기에 달렸다
    eq(_EC.normalize(tag_of("NdPO4_mp-aaaaafhw.cif")), "ndpo4", "정규화 → 레지스트리 키")
    eq(_EC.normalize(old("NdPO4_mp-aaaaafhw.cif")), "4",
       "음성② 옛 태그는 엉뚱한 키('4')로 정규화된다")
    if _EC.get(_EC.normalize(old("NdPO4_mp-aaaaafhw.cif"))).get("class") != "unregistered":
        bad.append("음성② 엉뚱한 키가 등록돼 있다 — 시험이 무의미해졌다")
    # ④ 갭 게이트 — 미등록/금속은 03 을 만들면 안 된다는 판정이 살아 있는가
    for t, want in (("li3nd", "metal"), ("ndpo4_없는태그", "unregistered")):
        eq(_EC.get(t).get("class"), want, f"게이트 {t}")
    # ⑤ PP 핀 — frozen-4f 가 아니면 이 캠페인 입력은 성립하지 않는다
    eq(PP_PIN.get("Nd"), "Nd.pbe-spdn-kjpaw_psl.1.0.0.UPF", "Nd PP 핀")

    print("\n".join("⛔ " + b for b in bad) if bad
          else "✓ selftest 통과 (태그 유도 5 · 음성 3 · 게이트 2 · PP 핀 1)")
    return max(1 if bad else 0, _selftest_tm())


def _selftest_tm():
    """2026-10-27 TM 경로 — 가짜 UPF·구조로 main() 을 실제로 돌려 입력 글자를 본다. 음성 포함."""
    import contextlib
    import io
    import tempfile
    from ase import Atoms
    from ase.io import write
    bad = []

    def chk(c, m):
        if not c:
            bad.append(m)

    # ① 순수 함수
    lab, mean = species_from_magmoms(["Mn", "Mn", "O", "O"], [4.6, -4.6, 0.0, 0.01])
    chk(lab == ["Mn1", "Mn2", "O", "O"] and abs(mean["Mn1"] - 4.6) < 1e-9, "AFM 은 Mn1/Mn2 로 나뉜다")
    lab, mean = species_from_magmoms(["Ni", "Ni", "S"], [2.0, 1.9, 0.0])
    chk(lab == ["Ni", "Ni", "S"], "[음성] 부호가 하나면 나누지 않는다 (옛 입력 꼴)")
    lab, _ = species_from_magmoms(["Mn", "Mn", "Mn"], [4.0, -4.0, 0.0])
    chk(lab == ["Mn1", "Mn2", "Mn3"], "+ · − · 0 자리 셋")
    try:
        species_from_magmoms(["Mn"], [1.0, 2.0]); chk(False, "[음성] 길이 불일치를 통과시켰다")
    except ValueError:
        pass
    chk(hubbard_mp_lines(["Co", "S"], ["Co", "S"]) == [], "[음성] 황화물엔 U 없음 (MP 규약)")
    chk(hubbard_mp_lines(["Mn1", "Mn2", "O", "P"], ["Mn", "O", "P"])
        == ["  U Mn1-3d 3.9", "  U Mn2-3d 3.9"], "O 가 있으면 종마다 U")
    try:
        hubbard_mp_lines(["Cu", "O"], ["Cu", "O"]); chk(False, "[음성] 표에 없는 Cu 에 U 를 지어냈다")
    except ValueError:
        pass
    chk(ecut_for(["Mn", "S"], {"Mn": (65.0, 780.0)}) == (65.0, 780.0), "Mn 바닥값")
    chk(ecut_for(["Li", "S"], {"Mn": (65.0, 780.0)}) == (ECUTWFC, ECUTRHO), "[음성] Mn 없으면 기본")
    try:
        parse_ecut_min(["Mn:65"]); chk(False, "[음성] 틀린 --ecut_min 꼴을 받았다")
    except ValueError:
        pass

    # ② main() 통합 — 갭 게이트는 '절연체' 로 고정해 03 까지 만들게 한다
    with tempfile.TemporaryDirectory() as T:
        pp, st, w = (os.path.join(T, x) for x in ("pp", "st", "w"))
        os.makedirs(pp); os.makedirs(st)
        for el, z in (("Mn", 15), ("O", 6), ("Co", 17), ("S", 6), ("Ni", 18)):
            open(os.path.join(pp, f"{el.lower()}_stub.UPF"), "w").write(
                f'<PP_HEADER z_valence="{z}.0"/>\n')

        def put(name, at, mags=None, syms=None):
            write(os.path.join(st, name + ".vasp"), at, format="vasp", direct=True)
            if mags is not None:
                json.dump({"symbols": syms or at.get_chemical_symbols(), "magmoms": mags},
                          open(os.path.join(st, name + ".magmom.json"), "w"))

        put("MnO_mp-1", Atoms("Mn2O2", scaled_positions=[[0, 0, 0], [.5, .5, 0], [.5, 0, 0],
                                                          [0, .5, 0]], cell=[4.4] * 3, pbc=True),
            [4.6, -4.6, 0.0, 0.0])
        put("CoS2_mp-2", Atoms("CoS2", scaled_positions=[[0, 0, 0], [.3, .3, .3], [.7, .7, .7]],
                               cell=[5.5] * 3, pbc=True), [0.9, 0.0, 0.0])
        put("MnS2_mp-3", Atoms("MnS2", scaled_positions=[[0, 0, 0], [.3, .3, .3], [.7, .7, .7]],
                               cell=[6.1] * 3, pbc=True))                       # 모멘트 파일 없음
        put("NiS2_mp-4", Atoms("NiS2", scaled_positions=[[0, 0, 0], [.3, .3, .3], [.7, .7, .7]],
                               cell=[5.7] * 3, pbc=True), [1.0, 0.0, 0.0], syms=["S", "Ni", "S"])

        def run(extra, work, pattern="*.vasp"):
            old_argv, old_get = sys.argv, EC.get
            sys.argv = ["x", "--pattern", os.path.join(st, pattern), "--pseudo_dir", pp,
                        "--work", work] + extra
            EC.get = lambda tag, reg=None: {"class": "insulator"}
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    main()
            finally:
                sys.argv, EC.get = old_argv, old_get

        def rd(tag, fn):          # 없으면 "" — 시험이 죽지 않고 ⛔ 로 보고하게
            q = os.path.join(w, tag, fn)
            return open(q).read() if os.path.isfile(q) else ""
        run(["--tm_state", "mp", "--hubbard", "mp", "--ecut_min", "Mn=65,780",
             "--fixed_cell", "CoS2_mp-2", "--pseudo_dir_run", "/remote/pp"], w)
        v = rd("MnO_mp-1", "01_vcrelax.in")
        chk("Mn1" in v and "Mn2" in v and "ntyp            = 3" in v, "MnO: 종 Mn1/Mn2/O")
        chk("starting_magnetization(1) = 0.3067" in v and
            "starting_magnetization(2) = -0.3067" in v, "MnO: 씨앗 ±4.6/15")
        chk("U Mn1-3d 3.9" in v and "U Mn2-3d 3.9" in v, "MnO: MP U 두 종")
        chk("ecutwfc         = 65.0" in v and "ecutrho         = 780.0" in v, "MnO: Mn 컷오프 바닥")
        chk("pseudo_dir      = '/remote/pp'" in v, "--pseudo_dir_run 이 입력에 적힌다")
        g = rd("MnO_mp-1", "03_nscf_gap.in")
        chk("tot_magnetization = 0" in g and "nspin           = 2" in g, "MnO: AFM tot_mag 0")
        c = os.listdir(os.path.join(w, "CoS2_mp-2"))
        chk("01_relax.in" in c and "01_vcrelax.in" not in c, "CoS2: 고정셀이면 01_relax.in 만")
        r = rd("CoS2_mp-2", "01_relax.in")
        chk("calculation     = 'relax'" in r and "&CELL" not in r, "CoS2: relax · &CELL 없음")
        chk("HUBBARD" not in r, "[음성] CoS2: 황화물에 U 가 붙지 않는다")
        chk("tot_magnetization = 1" in rd("CoS2_mp-2", "03_nscf_gap.in"), "CoS2: Σ0.9 → 1")
        chk("ecutwfc         = 60.0" in r, "[음성] CoS2: Mn 바닥값이 새지 않는다")
        chk(not os.path.isdir(os.path.join(w, "MnS2_mp-3")), "[음성] 모멘트 파일 없으면 안 만든다")
        chk(not os.path.isdir(os.path.join(w, "NiS2_mp-4")), "[음성] 원소 순서가 다르면 안 만든다")
        meta = json.load(open(os.path.join(w, "MnO_mp-1", "00_build_meta.json")))
        chk(meta["species"] == ["Mn1", "Mn2", "O"] and meta["hubbard"]
            and meta["cell_policy"] == "vc-relax", "메타가 종·U·셀 정책을 적는다")
        # 음성: --tm_state 없이는 TM 상을 안 만든다
        w2 = w + "_nostate"
        run([], w2, "MnO_mp-1.vasp")
        chk(not os.path.isdir(os.path.join(w2, "MnO_mp-1")), "[음성] --tm_state 없으면 TM 상 안 만든다")

    print("\n".join("⛔ " + b for b in bad) if bad else "✓ TM 경로 selftest 통과 (25)")
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pattern", default="db/structures/sei_*.vasp")
    ap.add_argument("--pseudo_dir", default="/data/work/pseudo")
    ap.add_argument("--work", default=WORK)
    # ⚠⚠ 2026-08-07 진단으로 밝혀진 것: Nd 3종의 갭이 −0.02 eV 로 닫힌 건
    #   "PBE 가 4f 에 약해서"가 **아니라 스핀분극을 안 켠 탓**이 크다.
    #   Nd³⁺ = 4f³ 인데 nspin=1 이면 전자 3개가 7겹 f 다중항에 **분수 점유**로 퍼진다
    #   → 부분점유 밴드 = 정의상 금속. 게다가 occupations='fixed' 는 nocc=nelec/2 번째
    #   밴드까지 채우므로 VBM·CBM 이 **같은 평평한 f 다중항 안**에서 잡혀 갭이 0 이 된다.
    #   실측 증거: 화학이 전혀 다른 세 상이 −0.021/−0.022/−0.028 로 7 meV 안에서 일치했고,
    #   E_F ±0.5 eV DOS 의 95~96% 가 Nd_f 였다(peak 49/106/243 states/eV = 평평한 밴드).
    #   ★ 우리 Nd₂O₃@LPSCl1.6 계산은 nspin=2 + starting_magnetization + Hubbard U 를
    #     썼고(tools/nd/build_lobster_nd.py), 거기선 빈 4f 가 +1.77 eV 에 구경꾼으로 앉아
    #     갭 1.632 eV 가 살아남았다. 같은 처방을 여기에도 준다.
    ap.add_argument("--nd_spin", action="store_true", default=True,
                    help="Nd 계에 nspin=2 + starting_magnetization (기본 켬)")
    ap.add_argument("--no_nd_spin", dest="nd_spin", action="store_false")
    ap.add_argument("--nd_mag", type=float, default=0.3,
                    help="Nd starting_magnetization (4f³ 국소모멘트 씨앗)")
    ap.add_argument("--nd_u", type=float, default=6.0,
                    help="Nd 4f 에 U [eV] (0 = 안 걺). 기본 6.0 — 란타나이드 4f 통상값")
    # ── 회신 I P0-2 control (pristine 초격자 + rattle → nosym 이완) ──────────
    ap.add_argument("--supercell", default=None,
                    help="'n1 n2 n3' — 읽은 구조를 이 배수로 확장 (예: '3 3 3')")
    ap.add_argument("--rattle", type=float, default=0.0,
                    help="가우시안 rattle 표준편차 [Å]")
    ap.add_argument("--rattle_seeds", type=int, default=0,
                    help="rattle 시드 K개 — r0(무변형 기준선) + r1..rK 를 만든다")
    ap.add_argument("--degauss", type=float, default=DEGAUSS,
                    help=f"smearing 폭 [Ry] (기본 {DEGAUSS}). ⚠ control 로 쓸 때는 **대조 대상과 "
                         "같은 값**이어야 한다 — cc333 NEB 는 0.02 로 돌았다")
    ap.add_argument("--control_relax", action="store_true",
                    help="P0-2 control 모드: **nosym 고정셀 relax 입력 하나만** 만든다 "
                         "(vc-relax/scf/갭/DOS 단계 없음). 셀은 원본 그대로 둔다 — "
                         "묻는 것이 '내부좌표가 재배열하는가' 이기 때문이다")
    ap.add_argument("--diagnose_undetermined", action="store_true",
                    help="⚠ electronic_class=undetermined 상도 갭 단계를 만든다 (진단 전용). "
                         "그 숫자는 갭이 아니다 — db 에 넣지 말 것")
    # ── 2026-10-27 CEI 생성물 갭 카드 (cei_product_gap_card_2026_10_27.json) ────────
    ap.add_argument("--pseudo_dir_run", default=None,
                    help="입력에 **적을** pseudo_dir (기본 = --pseudo_dir) — 여기서 만들고 다른 "
                         "기계에서 돌릴 때. z_valence 는 --pseudo_dir 에서 읽는다")
    ap.add_argument("--tm_state", choices=("mp",), default=None,
                    help="열린 껍질 TM 상의 자성 상태 — 'mp' = 구조 옆 <base>.magmom.json 의 MP 배치. "
                         "안 주면 TM 상은 입력을 만들지 않는다")
    ap.add_argument("--hubbard", choices=("none", "mp"), default="none",
                    help="TM 3d U — 'mp' = MP 규약 (O·F 가 있는 계만 · Co 3.32 · Mn 3.9 · Ni 6.2 eV)")
    ap.add_argument("--ecut_min", action="append", default=[], metavar="El=wfc,rho",
                    help="원소별 컷오프 바닥값 — 그 원소가 든 상만 올린다 (예 Mn=65,780)")
    ap.add_argument("--fixed_cell", nargs="*", default=[], metavar="TAG",
                    help="이 태그들은 vc-relax 대신 **고정셀 relax** (01_relax.in) — 분자결정 등")
    ap.add_argument("--selftest", action="store_true",
                    help="태그 유도·게이트 자체시험 (음성 경로 포함)")
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    from ase.io import read

    try:
        ecut_min = parse_ecut_min(a.ecut_min)
    except ValueError as e:
        sys.exit(f"⛔ {e}")
    pool = find_pseudos(a.pseudo_dir)
    files = sorted(glob.glob(a.pattern))
    if not files:
        sys.exit(f"⛔ {a.pattern} 에 구조가 없다")
    os.makedirs(a.work, exist_ok=True)
    if a.supercell or a.rattle_seeds:
        files = make_control_structures(a, files)
    prov = json.load(open(PROV)) if os.path.isfile(PROV) else {}

    # ── pseudo 점검을 먼저 전부 한다 — 중간에 죽는 것보다 낫다 ──────────────
    need, missing = set(), set()
    for f in files:
        need |= set(read(f).get_chemical_symbols())
    for el in sorted(need):
        if el not in pool:
            missing.add(el)
    print(f"pseudo 디렉터리 {a.pseudo_dir}")
    for el in sorted(need):
        print(f"  {el:3s} {pool.get(el, '⛔ 없음')}")
    if missing:
        print(f"\n⛔ pseudo 없음: {', '.join(sorted(missing))}")
        print("   → pslibrary/SSSP 에서 받아 넣은 뒤 다시 실행할 것. 해당 조성은 건너뛴다.")

    made, skipped = [], []
    for f in files:
        tag = tag_of(f)
        at = read(f)
        els = sorted(set(at.get_chemical_symbols()))
        if any(e in missing for e in els):
            print(f"\n⏭  {tag} — pseudo 없음({','.join(e for e in els if e in missing)})")
            skipped.append(tag); continue
        # ★ 2026-10-27 — 열린 껍질 TM 은 **자성 상태를 선언해야** 갭이 정의된다
        #   (CEI 생성물 갭 카드). 선언이 없거나 자리 대응이 안 되면 입력을 만들지 않는다.
        syms = at.get_chemical_symbols()
        tm_open = [e for e in els if e in OPEN_SHELL_TM]
        labels, lab_mag, side = syms, {}, None
        if tm_open:
            side = magmom_sidecar(f)
            why = None
            if a.tm_state != "mp":
                why = f"열린 껍질 TM {tm_open} — 자성 상태 미선언 (--tm_state mp)"
            elif side is None:
                why = "자성 배치 파일 <base>.magmom.json 없음 — 상태를 지어내지 않는다"
            elif side.get("symbols") != syms:
                why = "magmom.json 의 원소 순서가 구조와 다르다 — 자리 대응을 모른다"
            elif "Nd" in els:
                why = "Nd + TM 동시 — 이 경로는 둘을 같이 다루지 않는다"
            if why:
                print(f"\n⏭  {tag} — {why}")
                skipped.append(tag); continue
            labels, lab_mag = species_from_magmoms(syms, side["magmoms"])
        spc = sorted(set(labels))
        tm_spin = bool(tm_open) and any(abs(v) > MAG_THR for v in lab_mag.values())
        ecw, ecr = ecut_for(els, ecut_min)
        fixed_cell = tag in a.fixed_cell

        # ★★ 2026-08-11 — **금속에는 fixed-occ 갭 단계(03)를 만들지 않는다.**
        #   금속엔 VBM/CBM 이 없는데 occupations='fixed' 는 nelec/2 번째까지 채우므로
        #   "그 밴드와 다음 밴드의 차" 라는 **숫자가 나온다**. extract_gap.py 가 사후에
        #   '금속/반금속' 이라 라벨을 붙이긴 하지만 그건 계산을 막지 않는다 —
        #   그 숫자가 db 갭 표에 들어가면 그때는 못 잡는다. 아예 안 만든다.
        ecls = EC.get(tag)
        ecl = ecls.get("class")
        # ★ 자체검토 P1-8 — 레지스트리는 undetermined 를 "NEB·갭 **모두** 막는다" 라고
        #   써 놨는데 코드는 metal 만 막고 있었다. 그래서 lindo2/nd2o3/nd2s3 이 여전히
        #   03 을 만들고 gap.json 에 −0.02 eV 를 "금속/반금속(겹침)" 으로 남겼다 —
        #   레지스트리가 "방법의 실패지 금속성이 아니다" 라고 못박은 바로 그 숫자다.
        #   ⚠ 진단용으로 뽑고 싶으면 --diagnose_undetermined 로 명시적으로 켠다.
        skip_gap = ecl == "metal" or (ecl == "undetermined" and not a.diagnose_undetermined)
        skip_reason = {"metal": "electronic_class=metal — 금속엔 VBM/CBM 이 없다",
                       "undetermined": "electronic_class=undetermined — "
                                       + str(ecls.get("blocker", ""))[:160]}.get(ecl, "")
        # ★ 자체검토 P1-9 — unregistered 를 경고만 하고 절연체처럼 진행하고 있었다.
        #   로더 docstring("미등록을 조용히 절연체로 간주하지 않는다")과 어긋났고,
        #   다른 소비자는 전부 차단하는데 여기만 통과였다. 실제 미등록 태그가 이미 있다
        #   (sei_li3po4_mp-13725 → li3po4). 갭 단계만 막고 DOS 는 돌게 둔다.
        if ecl == "unregistered":
            print(f"\n⚠ {tag} 가 sei_electronic_class.json 에 없다 — 절연체로 **가정하지 않는다**. "
                  f"갭 단계를 건너뛴다. 레지스트리에 등록한 뒤 다시 돌릴 것")
            skip_gap = True
            skip_reason = "레지스트리 미등록 — 금속/절연체를 추측하지 않는다"

        d = os.path.join(a.work, tag)
        os.makedirs(d, exist_ok=True)
        cell = at.cell.array
        k_scf, k_nscf = kmesh(cell, KDENS_SCF), kmesh(cell, KDENS_NSCF)
        has_nd = "Nd" in els
        nat, ntyp = len(at), len(spc)

        # ⚠⚠ occupations='fixed' 인 nscf 는 QE 가 **nbnd = nelec/2 로 딱 맞춘다** —
        #   전도대가 없어 CBM 을 못 본다. nbnd 를 명시해야 갭이 나온다 (2026-08-06).
        zs = {e: zval(os.path.join(a.pseudo_dir, pool[e])) for e in els}
        if any(v is None for v in zs.values()):
            bad = [e for e, v in zs.items() if v is None]
            print(f"\n⏭  {tag} — UPF 에서 z_valence 를 못 읽었다: {','.join(bad)}")
            skipped.append(tag); continue
        # ⛔⛔ 2026-08-29 — **원자가에 없는 껍질에 U 를 걸고 있었다.**
        #   PP_PIN 이 Nd 를 frozen-4f (`Nd.pbe-spdn…`, z_valence ≈ 11, 4f 가 core)로 고정하는데
        #   `--nd_u` 기본값 6.0 이 그대로 `HUBBARD U Nd-4f` 를 찍었다. 4f 가 원자가에 없으므로
        #   그 U 는 걸 대상이 없다 — QE 가 죽거나(원자궤도 없음) 조용히 무시한다.
        #   nd_frozen4f.py 의 판별 기준을 그대로 쓴다: z ≈ 14 = 4f 원자가 · z ≈ 11 = frozen.
        if has_nd and a.nd_u > 0 and zs.get("Nd") is not None and zs["Nd"] < 12.0:
            sys.exit(
                f"⛔ {tag}: Nd PP 가 frozen-4f 다 (z_valence {zs['Nd']:.1f} < 12, "
                f"{pool['Nd']}) — 4f 가 core 에 있어 `HUBBARD U Nd-4f {a.nd_u}` 는 걸 대상이 없다.\n"
                "   frozen-4f 로 갈 거면 `--nd_u 0 --no_nd_spin`, 4f 를 원자가에 둘 거면 "
                "z≈14 PP 로 바꿔라. 어느 쪽이든 **비교 대상(cc333/NEB)과 같은 선택**이어야 한다.")
        nelec = sum(zs[e] for e in at.get_chemical_symbols())
        # Nd 계는 스핀분극 + U 로 간다 (아래 --nd_spin 주석). n_nd 는 tot_magnetization 용.
        n_nd = at.get_chemical_symbols().count("Nd")
        spinpol = bool(has_nd and a.nd_spin and n_nd)
        # ⚠ nspin=2 + tot_magnetization 이면 다수스핀 점유가 (nelec+M)/2 로 늘어난다.
        #   여유를 그만큼 더 준다 — 안 그러면 CBM 을 못 본다.
        pad = (3 * n_nd) // 2 if spinpol else 0
        # TM: MP 모멘트 합을 정수로 — 03(fixed) 의 tot_magnetization 시작값 (02 뒤 sync 가 고친다)
        M0 = int(round(sum(side["magmoms"]))) if tm_spin else 0
        if tm_spin:
            pad = (abs(M0) + 1) // 2 + 4
        try:
            hub_tm = hubbard_mp_lines(spc, els) if (tm_open and a.hubbard == "mp") else []
        except ValueError as e:
            print(f"\n⏭  {tag} — {e}")
            skipped.append(tag); continue
        tm_seed = {}
        for lab in spc:
            mm = lab_mag.get(lab, 0.0)
            if tm_spin and abs(mm) > MAG_THR:
                tm_seed[lab] = max(-1.0, min(1.0, mm / zs[el_of(lab)]))
        nbnd = int(nelec / 2 * 1.35) + 8 + pad      # 점유 + 넉넉한 빈 상태 (CBM 용)
        nbnd_dos = int(nelec / 2 * 1.60) + 12 + pad  # DOS 용은 더 여유 (&ELECTRONS 주석)

        def block(calc, kpts, fixed, extra="", nosym=False, verbose=False, dos=False):
            occ = ("    occupations     = 'fixed'\n" if fixed else
                   f"    occupations     = 'smearing'\n    smearing        = 'mv'\n"
                   f"    degauss         = {a.degauss}\n")
            hub = ""
            if has_nd and a.nd_u > 0:
                hub = f"\nHUBBARD (ortho-atomic)\n  U Nd-4f {a.nd_u}\n"
            if hub_tm:
                hub = "\nHUBBARD (ortho-atomic)\n" + "\n".join(hub_tm) + "\n"
            L = [f"&CONTROL", f"    calculation     = '{calc}'",
                 f"    prefix          = '{tag}'", "    outdir          = './tmp'",
                 f"    pseudo_dir      = '{a.pseudo_dir_run or a.pseudo_dir}'",
                 "    tprnfor         = .true.",
                 # ⚠ projwfc.x 는 **파동함수 파일**이 있어야 돈다. nscf 의 disk_io 기본값이
                 #   낮으면 끝나고 지워져 projwfc 가 MPI_ABORT 로 죽는다(실측 2026-08-06:
                 #   dos.x 는 됐는데 projwfc.x 만 실패). nscf 에서만 남긴다.
                 ("    disk_io         = 'medium'" if calc == "nscf" else ""),
                 # ⚠⚠ verbosity 는 **&CONTROL 소속**이다. &SYSTEM 에 넣어 9/9 가
                 #   read_namelists 에서 즉사했다 (2026-08-07). real_space 를 &ELECTRONS 대신
                 #   &SYSTEM 에 넣어 같은 사고를 낸 게 하루 전이다 — 네임리스트 소속을
                 #   추측하지 말고 확인할 것.
                 #   k 점이 100개를 넘으면 QE 는 verbosity='low' 에서 밴드를 아예 안 찍는다
                 #   (실측: li2o k 1098개 → 'bands (ev)' 0개 → 갭 추출 전멸).
                 ("    verbosity       = 'high'" if verbose else ""),
                 "    tstress         = .true." if calc == "vc-relax" else "", "/",
                 "&SYSTEM", "    ibrav           = 0", f"    nat             = {nat}",
                 f"    ntyp            = {ntyp}", f"    ecutwfc         = {ecw}",
                 f"    ecutrho         = {ecr}",
                 # ⚠ DOS 용 nscf 는 밴드를 더 준다. 제일 위 몇 밴드는 Davidson 이 항상
                 #   제일 늦게 수렴하는데, 여유 밴드가 그 실패를 흡수한다(어차피 안 쓴다).
                 (f"    nbnd            = {nbnd_dos if dos else nbnd}"
                  if calc == "nscf" else ""),
                 # ⚠ projwfc.x 가 'Error in routine d_matrix (2)' 로 죽는다 — 대칭연산을
                 #   구면조화함수에 적용하는 회전행렬을 못 만든다. 표준 우회는 대칭 끄기.
                 ("    nosym           = .true." if nosym else ""),
                 # ★ Nd 4f³ 는 스핀분극 없이는 분수 점유가 되어 갭이 정의되지 않는다
                 #   (위 --nd_spin 주석 참조). 씨앗 모멘트를 Nd 종에만 준다.
                 ("    nspin           = 2" if (spinpol or tm_spin) else ""),
                 (f"    starting_magnetization({spc.index('Nd') + 1}) = {a.nd_mag}"
                  if spinpol else ""),
                 # TM — MP 자리 모멘트의 종 평균 ÷ z_valence (QE 씨앗은 원자가 전자 편극 비율)
                 *[f"    starting_magnetization({spc.index(lab) + 1}) = {v:.4f}"
                   for lab, v in tm_seed.items()],
                 # ⚠ QE 는 `occupations='fixed'` + `nspin=2` 조합에서 tot_magnetization 을
                 #   **요구한다**(없으면 read_namelists 에서 즉사). Nd³⁺ = 4f³ 이므로
                 #   홀전자 3개 × Nd 개수. 이 값이 곧 ↑/↓ 점유 밴드 수를 가른다.
                 (f"    tot_magnetization = {3 * n_nd}" if (spinpol and fixed) else ""),
                 (f"    tot_magnetization = {M0}" if (tm_spin and fixed) else ""),
                 ("    noinv           = .true." if nosym else ""),
                 occ.rstrip(), "/",
                 # ⚠⚠ DOS 용 nscf 만 문턱을 푼다 (2026-08-07 licl 04 단독 실패).
                 #   증상: `c_bands (1): too many bands are not converged` → MPI_ABORT.
                 #   원인: LiCl 은 갭 6.26 eV 짜리 이온결정이라 빈 전도대가 거의
                 #   자유전자꼴이고, nosym 으로 k 점이 전 BZ 로 늘어난 상태에서
                 #   conv_thr 1e-8(→ ethr ~1e-9)을 제일 위 밴드까지 요구하면 안 닫힌다.
                 #   ★ 여기서 문턱을 푸는 게 **정당한 이유**: 이 단계 산출은 DOS **모양**뿐이고
                 #     갭은 03 단계 고유값이 정본이다. DOS 의 degauss 0.007 Ry(≈0.095 eV)가
                 #     이미 1e-6 Ry 보다 다섯 자리 굵다 — 정밀도가 남아돈다.
                 #   ⛔ 03(갭) 단계는 **절대 안 푼다.** 그 값이 논문에 실린다.
                 "&ELECTRONS",
                 ("    conv_thr        = 1.0d-6" if dos else "    conv_thr        = 1.0d-8"),
                 # Davidson 부분공간을 키우면 잘 안 닫히는 밴드가 닫힌다(기본 2 → 4).
                 ("    diago_david_ndim = 4" if dos else ""),
                 "    mixing_beta     = 0.3", "    electron_maxstep = 200", "/"]
            if calc in ("relax", "vc-relax"):
                L += ["&IONS", "/"]
            if calc == "vc-relax":
                L += ["&CELL", "    cell_dofree     = 'all'", "/"]
            L = [x for x in L if x != ""]
            body = "\n".join(L) + "\n\nATOMIC_SPECIES\n"
            from ase.data import atomic_masses, atomic_numbers
            for e in spc:
                body += (f"  {e:3s} {atomic_masses[atomic_numbers[el_of(e)]]:8.3f}  "
                         f"{pool[el_of(e)]}\n")
            body += "\nCELL_PARAMETERS angstrom\n"
            for v in cell:
                body += "  %16.10f %16.10f %16.10f\n" % tuple(v)
            body += "\nATOMIC_POSITIONS angstrom\n"
            for s_, p in zip(labels, at.positions):
                body += f"  {s_:3s} %16.10f %16.10f %16.10f\n" % tuple(p)
            body += hub
            body += f"\nK_POINTS automatic\n  {kpts[0]} {kpts[1]} {kpts[2]} 0 0 0\n"
            return body + extra

        # ── P0-2 control 모드 — nosym 고정셀 relax 하나만 (회신 I 실행순서 3) ──
        #   셀을 고정하는 이유: 묻는 것이 "내부좌표가 재배열하는가" 이고, cc333 과
        #   **같은 셀**이어야 대조가 성립한다. vc-relax 는 셀까지 움직여 비교를 깬다.
        if a.control_relax:
            cin = os.path.join(d, "00_control_relax.in")
            open(cin, "w").write(block("relax", k_scf, False, nosym=True))
            json.dump({"mode": "P0-2 control (회신 I 실행순서 3)",
                       "구조": os.path.abspath(f), "원자수": nat,
                       "supercell": a.supercell, "rattle_A": a.rattle,
                       "질문": "공공 없는 pristine 셀에서도 같은 Nd 재배열이 나오는가",
                       "판정": "나오면 원인은 공공이 아니라 셀 자체의 soft mode "
                               "⇒ cc333 끝점 두 개가 무효, 끝점부터 다시",
                       "⛔_이_입력이_못_하는_것":
                           "이완 후 대칭 복원 여부를 자동 판정하지 않는다 — "
                           "symmetric_saddle.py --align_check 로 사후 비교할 것"},
                      open(os.path.join(d, "control_meta.json"), "w"),
                      ensure_ascii=False, indent=1)
            print(f"\n{tag}: control relax 입력 {cin} ({nat}원자, nosym, 셀 고정)")
            continue
        # ★ 2026-10-27 — 고정셀 태그(분자결정: PBE 에 분산력이 없어 분자 사이 부피가 정의되지
        #   않는다)는 01_relax.in. 반대쪽 파일이 남아 있으면 러너가 헷갈리므로 지운다.
        rname, oname = (("01_relax.in", "01_vcrelax.in") if fixed_cell
                        else ("01_vcrelax.in", "01_relax.in"))
        if os.path.isfile(os.path.join(d, oname)):
            os.remove(os.path.join(d, oname))
        open(os.path.join(d, rname), "w").write(
            block("relax" if fixed_cell else "vc-relax", k_scf, False))
        open(os.path.join(d, "02_scf.in"), "w").write(block("scf", k_scf, False))
        # ★ 갭의 정본 — fixed occupations + 조밀 k. nbnd 를 넉넉히 줘 CBM 을 잡는다
        gap_in = os.path.join(d, "03_nscf_gap.in")
        if skip_gap:
            # 입력을 지우고 사유를 남긴다 — 옛 입력이 남아 있으면 러너가 그걸 돌린다
            if os.path.isfile(gap_in):
                os.remove(gap_in)
            # ⚠ gap 은 None 으로 — 문자열을 넣으면 결산의 :9.3f 포맷이 죽는다 (2026-08-11 실측)
            json.dump({"tag": tag, "gap": None, "verdict": "NOT_APPLICABLE",
                       "electronic_class": ecl,
                       "reason": skip_reason or "electronic_class 게이트",
                       "electronic_class_evidence": ecls.get("evidence"),
                       "do_instead": "04~06 (DOS/PDOS) 로 E_F 에 상태가 있는지 확인한다. "
                                     "그게 금속 선언의 근거가 된다.",
                       "registry": "db/properties/sei_electronic_class.json"},
                      open(os.path.join(d, "03_GAP_NOT_APPLICABLE.json"), "w"),
                      ensure_ascii=False, indent=2)
        else:
            open(gap_in, "w").write(block("nscf", k_nscf, True, verbose=True))
        k_dos = kmesh(cell, KDENS_DOS)
        open(os.path.join(d, "04_nscf_dos.in"), "w").write(
            block("nscf", k_dos, False, nosym=True, dos=True))
        open(os.path.join(d, "05_dos.in"), "w").write(
            f"&DOS\n  prefix = '{tag}'\n  outdir = './tmp'\n"
            f"  fildos = '{tag}.dos'\n  degauss = 0.007\n/\n")
        open(os.path.join(d, "06_projwfc.in"), "w").write(
            f"&PROJWFC\n  prefix = '{tag}'\n  outdir = './tmp'\n"
            f"  filpdos = '{tag}'\n  degauss = 0.007\n  ngauss = 0\n/\n")
        note = ""
        # ⚠ 2026-08-11 — 경고문이 PP 를 안 보고 찍혔다. frozen-4f(z≈11)로 갈아끼운 뒤에도
        #   "4f 가 valence 다" 라고 말해 사람을 헷갈리게 한다. z_valence 로 분기한다.
        nd_frozen = has_nd and (zval(os.path.join(a.pseudo_dir, pool["Nd"])) or 99) <= 12
        if has_nd and nd_frozen:
            note = ("  ★ Nd frozen-4f PP 다 (z≈11, 4f 가 core) — 스핀분극·U 가 필요 없다. "
                    "갭은 fixed-occ 규율 그대로.")
        elif has_nd:
            note = "  ⚠ Nd 4f 가 valence 다 — "
            if spinpol and a.nd_u > 0:
                note += (f"nspin=2 · M_tot={3 * n_nd} μB · U(Nd 4f)={a.nd_u} eV. "
                         "2026-08-07 이전 실행(스핀 없음·U 없음)의 −0.02 eV 는 "
                         "**분수 점유 인공물**이었다 — 이 설정이 그걸 고친다.")
            elif spinpol:
                note += f"nspin=2 · M_tot={3 * n_nd} μB, U 없음 → 갭 과소 가능."
            else:
                note += ("**스핀분극 없음** → 4f³ 가 분수 점유가 되어 갭이 정의되지 않는다. "
                         "이 설정의 갭은 인용 금지(진단용).")
        print(f"\n✓ {tag:26s} {nat:3d}원자 {'+'.join(els):14s} "
              f"k scf {k_scf} / gap {k_nscf} / dos {kmesh(cell, KDENS_DOS)} (nosym) · "
              f"전자 {nelec:.0f} → nbnd {nbnd} "
              + (f"(점유 ↑{int((nelec + 3*n_nd)/2)}/↓{int((nelec - 3*n_nd)/2)}, M={3*n_nd} μB)"
                 if spinpol else
                 f"(점유 {int(nelec/2)} + 빈 {nbnd - int(nelec/2)})"))
        if skip_gap:
            print(f"  ⛔ **03(갭) 단계를 만들지 않았다** — {skip_reason}")
            print(f"     04~06 (DOS/PDOS) 는 그대로 돈다. 사유: 03_GAP_NOT_APPLICABLE.json")
        if note:
            print(note)
        if tm_open or fixed_cell or (ecw, ecr) != (ECUTWFC, ECUTRHO):
            print(f"  ★ 종 {'/'.join(spc)} · nspin {2 if tm_spin else 1}"
                  + (f" · 씨앗 " + ", ".join(f"{k} {v:+.3f}" for k, v in tm_seed.items())
                     + f" · tot_mag(03 시작) {M0}" if tm_spin else "")
                  + f" · U {'; '.join(x.strip() for x in hub_tm) if hub_tm else '없음'}"
                  + f" · ecut {ecw:g}/{ecr:g} · {'고정셀 relax' if fixed_cell else 'vc-relax'}")
        # 입력의 출처를 옆에 남긴다 — 어느 구조·모멘트·규약으로 만들었는지 (2026-10-27)
        import hashlib
        json.dump({"tag": tag, "structure": f,
                   "structure_sha256": hashlib.sha256(open(f, "rb").read()).hexdigest(),
                   "species": spc, "nspin": 2 if (tm_spin or spinpol) else 1,
                   "tm_state": (a.tm_state if tm_open else None),
                   "magmom_sidecar": (os.path.splitext(f)[0] + ".magmom.json") if side else None,
                   "starting_magnetization": tm_seed or None,
                   "tot_magnetization_initial": M0 if tm_spin else None,
                   "hubbard": hub_tm or None, "hubbard_policy": a.hubbard if tm_open else None,
                   "ecut_wfc_rho": [ecw, ecr], "cell_policy": "fixed" if fixed_cell else "vc-relax",
                   "pseudo": {e: pool[e] for e in els},
                   "pseudo_dir_written": a.pseudo_dir_run or a.pseudo_dir,
                   "k_scf": k_scf, "k_gap": k_nscf, "nbnd_gap": nbnd,
                   "gap_step": "skipped: " + skip_reason if skip_gap else "03_nscf_gap.in"},
                  open(os.path.join(d, "00_build_meta.json"), "w"), ensure_ascii=False, indent=1)
        made.append(tag)

    print(f"\n생성 {len(made)}개 · 건너뜀 {len(skipped)}개 → {a.work}")
    print("\n실행:  bash tools/sei/run_sei_dft.sh")
    print("⚠ 갭은 03_nscf_gap 의 고유값으로만 낸다 — DOS 문턱 판독 금지.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
