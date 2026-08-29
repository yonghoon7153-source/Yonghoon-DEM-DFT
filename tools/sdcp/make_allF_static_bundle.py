#!/usr/bin/env python3
"""make_allF_static_bundle.py — ⛔ **폐기 (2026-08-29). 쓰지 마라.**

`vasp_handoff_bundle.py --closure` 를 써라.

왜 폐기했나: 이 도구는 복합체의 AFM 씨앗을 스스로 만들려 했는데, 부격자 원장은
**슬랩 기준 인덱스**로 부호를 주고 복합체 POSCAR 는 원자 순서가 다르다. 정본 생성기는
`_assert_slab_lineage` + 순열 재매핑으로 그걸 처리한다. 그 기계를 병렬로 다시 만드는 것은
CLAUDE.md 가 금지하는 중복이고, 틀리면 **자기 배치가 조용히 어긋난다** (2026-08-12 에
"파일 순서로 반 갈랐더니 실제 부격자와 24/48 일치" = 동전 던지기였던 이력이 있다).

회신 U P0-5 의 처방도 "새 도구" 가 아니라 **기존 생성기의 closure mode** 였다.
그 모드는 e2e selftest 로 전 endpoint 의 LREAL/.FALSE./NSW=0/IBRION=-1/IVDW=11 과
relax 상 부재를 확인한다.

── 아래는 폐기 전 원문 ──

조각 간 대비(ΔΔE_ads) 하나를 살리기 위한 **최소 번들**.

회신 T (2026-08-29) 최단 경로 그대로:
  *"0.35 eV 조각 간 대비만 필요: neutral/c10 분자 static 2잡 + 해당 complex all-F static 2잡"*

왜 이것만으로 되나 (회신 T Q1-1):
  ΔΔE_ads = (E_C^SDCP − E_M^SDCP) − (E_C^PTFE − E_M^PTFE)
  양쪽이 **정확히 같은 slab 에너지·구조·자기 basin** 을 쓰면 slab 은 대수적으로 소거된다.
  ⇒ 차이만 보고하면 slab-F 불필요. **절대 E_ads 를 보고하려면 slab-F 필수** (--with_slab).

무엇을 고치나:
  · `LREAL = .FALSE.`  — 복합체·분자 **양쪽 다**. 서로 다른 흡착종이라 소거되지 않는다.
  · `NUPDOWN = -1`     — 복합체가 자유였으므로 기준 분자도 자유. (닫힌 껍질이라 M≈0 예상)
  · **고정 기하**       — `IBRION=-1 NSW=0`. 재이완하면 "스핀 제약 해제 + 구조경로 변화" 가
                          섞여 순수 δ_m 이 아니게 된다 (회신 T 지적).

⛔ 이 도구가 **못 하는 것**:
  · 자세를 다시 고르지 않는다. 기존 자세를 그대로 쓴다 — 자세 선택 문제(회신 T P0-1)는
    **별건**이고 이 번들로 해결되지 않는다.
  · POTCAR 를 넣지 않는다 (라이선스). `POTCAR_SPEC.txt` 로 변형을 지정한다.
  · 결과를 판정하지 않는다. 회수·판정은 기존 분석 경로 몫이다.
  · 절대 E_ads 는 `--with_slab` 없이는 만들 수 없다 — 그때는 차이만 인용해야 한다.

  python3 tools/sdcp/make_allF_static_bundle.py \\
      --complexes db/structures/sdcp_wave1 \\
      --mols /data/work/runs/sdcp_refs_freespin_v1/refs \\
      --out /data/work/runs/sdcp_allF_v1
  python3 tools/sdcp/make_allF_static_bundle.py --selftest
"""
import argparse
import glob
import hashlib
import json
import os
import shutil
import sys

COMMON = """GGA      = PE
PREC     = Accurate
ENCUT    = 520
ISMEAR   = 0
SIGMA    = 0.05
ALGO     = Normal
NELM     = 200
NELMIN   = 6
ISPIN    = 2
ISYM     = 0
LASPH    = .TRUE.
ADDGRID  = .TRUE.
LORBIT   = 11
AMIN     = 0.01
IVDW     = 11
NCORE    = 4
"""

#: 복합체·슬랩만 U 를 건다 (Ni 있음). 분자에는 Ni 가 없다.
LDAU = """LDAU      = .TRUE.
LDAUTYPE  = 2
LDAUL     = {ldaul}
LDAUU     = {ldauu}
LDAUJ     = {ldauj}
LDAUPRINT = 2
LMAXMIX   = 4
"""

STATIC = """SYSTEM = {system} [all-F static, fixed geometry]
# 회신 T 최단 경로 — LREAL=.FALSE. · NUPDOWN=-1 · 고정 기하.
{common}EDIFF    = 1E-6
IBRION   = -1
NSW      = 0
LREAL    = .FALSE.
NUPDOWN  = {nupdown}
{magmom}{dipol}{ldau}LWAVE    = .FALSE.
LCHARG   = .FALSE.
"""


def _seed_magmom(poscar, frag, seed):
    """AFM 부격자 MAGMOM — **`vasp_handoff_bundle.seed_configs` 를 그대로 쓴다.**

    ⛔⛔ 2026-08-29 — 이 번들 초판은 복합체에 MAGMOM 을 **안 썼다.** 그러면 AFM 씨앗이
      없어 wave1 과 **다른 자기 basin** 으로 수렴할 수 있고, 그 값을 wave1 과 비교하면
      basin 을 가로질러 뺀 것이 된다 — 회신 U P0-4 가 경고한 바로 그것이다.
      wave1 의 INCAR 되울림은 MAGMOM 이 **전 36잡 공란**이라(OUTCAR 미echo) 되짚을 수
      없으므로, **같은 생성기**로 다시 만들어 씨앗 topology 를 receipt 에 기록한다.

    → (magmom 줄, {poscar_index: 부호} ) 또는 (빈 문자열, None)
    """
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import vasp_handoff_bundle as VH
        from ase.io import read
        at = read(poscar, format="vasp")
        sym = at.get_chemical_symbols()
        nslab = max((i for i, s in enumerate(sym) if s in ("Li", "Ni", "O")), default=-1) + 1
        while nslab > 0 and sym[nslab - 1] not in ("Li", "Ni", "O"):
            nslab -= 1
        # ⚠ 원장은 **좌표로 확정한 Ni1/Ni2 부격자**다. 파일 순서로 반 갈랐던 옛 구현은
        #   실측에서 24/48 일치(동전 던지기)였다 — 개수만 24/24 였을 뿐 다른 자기 배치다.
        _root = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))))          # tools/sdcp/x.py → repo
        _lp = os.path.join(_root, "db", "properties", "afm_ledger.json")
        if not os.path.isfile(_lp):
            raise FileNotFoundError(f"부격자 원장이 없다: {_lp}")
        led = json.load(open(_lp))
        seeds = VH.seed_configs(at, nslab, frag, led)
        mag = seeds.get(seed)
        if not mag:
            return "", None
        sign = {i: mag[i] for i in range(nslab) if sym[i] == "Ni"}
        return ("MAGMOM   = " + " ".join(f"{m:g}" for m in mag) + "\n",
                {str(k): v for k, v in sign.items()})
    except Exception as e:                       # 조용히 넘어가지 않는다
        sys.exit(f"⛔ {os.path.basename(poscar)}: AFM MAGMOM 씨앗을 만들지 못했다 ({e}). "
                 "MAGMOM 없이 복합체를 돌리면 wave1 과 다른 자기 basin 으로 갈 수 있고, "
                 "그 값은 비교에 못 쓴다 (회신 U P0-4). --no_magmom 으로 강제할 수 있으나 "
                 "그 번들은 닫힘에 쓰지 마라")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def read_poscar_species(p):
    """POSCAR 6·7행에서 (원소목록, 개수). 원소행이 없으면 None."""
    L = open(p).read().splitlines()
    if len(L) < 8:
        return None
    els = L[5].split()
    if not els or els[0][0].isdigit():
        return None
    try:
        cnt = [int(x) for x in L[6].split()]
    except ValueError:
        return None
    return els, cnt


def emit(jd, name, poscar, has_ni, com_frac=None, frag=None, seed=None,
         nupdown=-1, magmom_line="", no_magmom=False):
    os.makedirs(jd, exist_ok=True)
    dst = os.path.join(jd, "POSCAR")
    shutil.copy(poscar, dst)
    sp = read_poscar_species(dst)
    if sp is None:
        sys.exit(f"⛔ {poscar}: POSCAR 원소행을 못 읽었다 — 조용히 넘어가지 않는다")
    els, cnt = sp
    ni_sign = None
    if has_ni and not no_magmom and not magmom_line:
        magmom_line, ni_sign = _seed_magmom(dst, frag, seed)
    ldau = ""
    if has_ni:
        # Ni 만 U=6.2 (우리 규약), 나머지 −1/0
        ldau = LDAU.format(
            ldaul=" ".join("2" if e == "Ni" else "-1" for e in els),
            ldauu=" ".join("6.2" if e == "Ni" else "0.0" for e in els),
            ldauj=" ".join("0.0" for _ in els))
    dip = ""
    if com_frac is not None:
        dip = ("LDIPOL   = .TRUE.\nIDIPOL   = 4\n"
               f"DIPOL    = {com_frac[0]:.4f} {com_frac[1]:.4f} {com_frac[2]:.4f}\n")
    elif has_ni:
        dip = "LDIPOL   = .TRUE.\nIDIPOL   = 3\n"      # 한쪽만 흡착한 슬랩
    open(os.path.join(jd, "INCAR"), "w").write(
        STATIC.format(system=name, common=COMMON, dipol=dip, ldau=ldau,
                      nupdown=nupdown, magmom=magmom_line))
    open(os.path.join(jd, "KPOINTS"), "w").write(
        "auto\n0\nGamma\n1 1 1\n0 0 0\n" if not has_ni else
        "auto\n0\nGamma\n2 2 1\n0 0 0\n")
    rec = {"name": name, "poscar_src": os.path.abspath(poscar),
           "poscar_sha256": sha(dst), "incar_sha256": sha(os.path.join(jd, "INCAR")),
           "species": els, "counts": cnt, "n_ions": sum(cnt),
           "has_ni": has_ni, "nupdown": nupdown,
           "magmom_seeded": bool(magmom_line)}
    if ni_sign:
        # 회신 U P0-4 — 총자화가 아니라 **국소 Ni topology** 로 판정한다.
        #   씨앗 부호를 여기 박아 둬야 회수 때 vasp_handoff_bundle.global_sign 으로
        #   부분 반전을 잡을 수 있다.
        rec["ni_sign_poscar_idx"] = ni_sign
        rec["n_ni"] = len(ni_sign)
    return rec


def com_fractional(poscar):
    try:
        from ase.io import read
        at = read(poscar, format="vasp")
        f = at.get_scaled_positions()
        m = at.get_masses()
        return (f * m[:, None]).sum(0) / m.sum()
    except Exception:
        return None


def build(a):
    os.makedirs(a.out, exist_ok=True)
    jobs = []

    # ── 복합체 ────────────────────────────────────────────────────────────
    pats = a.frags.split(",")
    for f in sorted(glob.glob(os.path.join(a.complexes, "*.vasp"))):
        b = os.path.basename(f)[:-5]
        if not any(b.startswith(p + "__") for p in pats):
            continue
        if a.basin and a.basin not in b:
            continue
        frag = next(p for p in pats if b.startswith(p + "__"))
        seed = next((s for s in ("afm2424_pm1", "afm2424_net4") if s in b), a.basin)
        jobs.append(emit(os.path.join(a.out, "complex", b), b, f, has_ni=True,
                         frag=frag, seed=seed, no_magmom=a.no_magmom))

    # ── 기체 기준 분자 (box24) ────────────────────────────────────────────
    for p in pats:
        hits = sorted(glob.glob(os.path.join(a.mols, f"mol__{p}__box24", "POSCAR")))
        if not hits:
            sys.exit(f"⛔ mol__{p}__box24/POSCAR 을 {a.mols} 에서 못 찾았다. "
                     "기준 분자 없이는 E_ads 를 만들 수 없다 — 조용히 건너뛰지 않는다")
        nm = f"mol__{p}__box24"
        jobs.append(emit(os.path.join(a.out, "refs", nm), nm, hits[0],
                         has_ni=False, com_frac=com_fractional(hits[0])))
        # ── 회신 U B3 (P0) — **비영 MAGMOM 대조** ─────────────────────────
        #   `NUPDOWN=-1` 은 "무제약" 이지 "singlet 확정" 이 아니다. 그런데 생성기가
        #   중성 분자에 MAGMOM 0 만 주므로, **비영 자기해를 탐색했다는 증거가 없다.**
        #   같은 POSCAR·같은 all-F 로 비영 시작을 하나 둔다. 둘이 같은 에너지·같은
        #   singlet 으로 수렴하면 기준을 닫고, 더 낮은 다른 상태가 나오면
        #   **자동 채택하지 말고** MOLECULAR_STATE_UNRESOLVED 로 멈춘다.
        sp = read_poscar_species(hits[0])
        if sp and not a.no_spin_control:
            nat = sum(sp[1])
            nz = "MAGMOM   = " + " ".join(["1.0", "-1.0"] + ["0.0"] * (nat - 2)) + "\n"
            jobs.append(emit(os.path.join(a.out, "refs", nm + "__nzmag"),
                             nm + "__nzmag", hits[0], has_ni=False,
                             com_frac=com_fractional(hits[0]), magmom_line=nz))

    # ── 슬랩 (절대 E_ads 를 낼 때만) ──────────────────────────────────────
    if a.with_slab:
        for f in sorted(glob.glob(os.path.join(a.slabs, "*.vasp"))):
            b = os.path.basename(f)[:-5]
            if a.basin and a.basin not in b:
                continue
            jobs.append(emit(os.path.join(a.out, "refs", b), b, f, has_ni=True))

    man = {
        "schema": "sdcp_allF_static/v1",
        "무엇": "회신 T 최단 경로 — 조각 간 대비(ΔΔE_ads)를 all-F·고정기하로 다시 낸다",
        "고친_것": ["LREAL = .FALSE. (복합체·분자 양쪽)",
                    "NUPDOWN = -1 (복합체가 자유였으므로 기준도 자유)",
                    "고정 기하 (IBRION=-1 NSW=0) — 재이완하면 δ_m 이 아니게 된다"],
        "⛔_이_번들이_주지_않는_것": [
            "절대 E_ads (슬랩 없이는 차이만 인용 가능)" if not a.with_slab else None,
            "자세 선택 문제의 해결 — 회신 T P0-1 은 **별건**이다",
            "dense-k 검증 (회신 T Q1-5: 0.346 정밀값에는 P0)",
        ],
        "허용_서술_후보": "동일 realized AFM basin 과 LREAL=.FALSE. 고정기하 규약에서, "
                          "평가한 중성 SDCP 조각의 자세들은 평가한 CF3-(CF2)8-CF3 조각의 "
                          "자세들보다 흡착 전자에너지가 더 음수였다",
        "jobs": jobs, "n_jobs": len(jobs),
    }
    man["⛔_이_번들이_주지_않는_것"] = [x for x in man["⛔_이_번들이_주지_않는_것"] if x]
    mp = os.path.join(a.out, "MANIFEST.json")
    json.dump(man, open(mp, "w"), ensure_ascii=False, indent=1)

    open(os.path.join(a.out, "POTCAR_SPEC.txt"), "w").write(
        "원소별 PAW 변형 (라이선스로 POTCAR 미포함)\n"
        "  Li -> Li_sv   Ni -> Ni_pv   O -> O   C -> C   H -> H   S -> S   F -> F\n"
        "⚠ wave1 과 **같은 변형**이어야 한다. 다르면 총에너지가 비교 불가다.\n")
    open(os.path.join(a.out, "run_all.sh"), "w").write(
        "#!/usr/bin/env bash\n# VASP_CMD=\"mpirun -np 48 vasp_std\" bash run_all.sh\n"
        "set -uo pipefail\nfor d in complex/*/ refs/*/; do\n"
        "  [ -f \"$d/OUTCAR\" ] && grep -aq 'General timing' \"$d/OUTCAR\" && "
        "{ echo \"skip $d\"; continue; }\n"
        "  echo \"== $d\"; ( cd \"$d\" && ${VASP_CMD:?VASP_CMD 를 지정하라} > vasp.log 2>&1 )\n"
        "done\n")
    print(f"→ {a.out} · 잡 {len(jobs)}개")
    for j in jobs:
        print(f"   {j['name'][:58]:58s} {j['n_ions']:4d}원자 "
              f"{'U(Ni)' if j['has_ni'] else '분자 '}")
    if not a.with_slab:
        print("⚠ 슬랩이 없다 — **조각 간 차이만** 인용 가능하다 (절대 E_ads 불가). "
              "절대값이 필요하면 --with_slab")
    return man


def selftest():
    import tempfile
    ok = bad = 0

    def chk(c, m):
        nonlocal ok, bad
        print(("  ⭕ " if c else "  ⛔ ") + m)
        ok, bad = ok + bool(c), bad + (not c)

    def poscar(path, els, cnt, n):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        L = ["t", "1.0", "20 0 0", "0 20 0", "0 0 20", " ".join(els),
             " ".join(map(str, cnt)), "Direct"]
        L += [f"0.{i%9}0 0.{(i+1)%9}0 0.{(i+2)%9}0" for i in range(n)]
        open(path, "w").write("\n".join(L) + "\n")

    with tempfile.TemporaryDirectory() as td:
        cx, ml, out = f"{td}/cx", f"{td}/ml", f"{td}/out"
        poscar(f"{cx}/sdcp_neutral__p__Nitop__afm2424_pm1__static.vasp",
               ["Li", "Ni", "O", "C", "H", "S"], [48, 48, 96, 11, 16, 2], 221)
        poscar(f"{cx}/ptfe_c10__p__Litop__afm2424_pm1__static.vasp",
               ["Li", "Ni", "O", "C", "F"], [48, 48, 96, 10, 22], 224)
        poscar(f"{ml}/mol__sdcp_neutral__box24/POSCAR",
               ["O", "C", "H", "S"], [6, 11, 16, 2], 35)
        poscar(f"{ml}/mol__ptfe_c10__box24/POSCAR", ["C", "F"], [10, 22], 32)
        A = argparse.Namespace(complexes=cx, mols=ml, out=out, with_slab=False,
                               slabs=cx, basin="pm1",
                               frags="sdcp_neutral,ptfe_c10", selftest=False,
                               no_magmom=True, no_spin_control=False)
        man = build(A)
        chk(man["n_jobs"] == 6,
            f"잡 6개 (복합체 2 + 분자 2 + 비영MAGMOM 대조 2) — 실제 {man['n_jobs']}")
        nz = [j for j in man["jobs"] if j["name"].endswith("__nzmag")]
        chk(len(nz) == 2 and all(j["magmom_seeded"] for j in nz),
            "[양성 U-B3] 기체 기준마다 **비영 MAGMOM 대조**가 붙는다")
        nzi = open(f"{out}/refs/mol__sdcp_neutral__box24__nzmag/INCAR").read()
        chk("MAGMOM   = 1.0 -1.0" in nzi and "NUPDOWN  = -1" in nzi,
            "  비영 시작 + 무제약 — 같은 all-F 설정으로 자기해를 실제로 탐색한다")
        inc = open(f"{out}/refs/mol__sdcp_neutral__box24/INCAR").read()
        chk("LREAL    = .FALSE." in inc, "[양성] 분자 INCAR 에 LREAL=.FALSE.")
        chk("NUPDOWN  = -1" in inc, "[양성] 분자 INCAR 에 NUPDOWN=-1 (자유 스핀)")
        chk("NSW      = 0" in inc and "IBRION   = -1" in inc,
            "[양성] 고정 기하 — 재이완하지 않는다")
        chk("LDAU" not in inc, "[음성] 분자에는 U 를 안 건다 (Ni 가 없다)")
        cinc = open(glob.glob(f"{out}/complex/sdcp_neutral__*/INCAR")[0]).read()
        chk("LDAU      = .TRUE." in cinc and "6.2" in cinc, "[양성] 복합체에는 U(Ni)=6.2")
        chk("LREAL    = .FALSE." in cinc, "[양성] 복합체도 LREAL=.FALSE. (소거 안 되므로)")
        chk(cinc.count("2") > 0 and "LDAUL" in cinc, "[양성] LDAUL 이 원소 순서를 따른다")
        # 음성: 기준 분자가 없으면 조용히 넘어가지 않는다
        A2 = argparse.Namespace(**{**vars(A), "mols": f"{td}/empty", "out": f"{td}/o2"})
        try:
            build(A2); chk(False, "[음성] 기준 분자 없으면 중단")
        except SystemExit:
            chk(True, "[음성] 기준 분자 없으면 **중단** (E_ads 를 못 만드므로)")
        # 음성: 원소행 없는 POSCAR 는 거부
        bad_p = f"{td}/bad/x.vasp"
        os.makedirs(os.path.dirname(bad_p), exist_ok=True)
        open(bad_p, "w").write("t\n1.0\n20 0 0\n0 20 0\n0 0 20\n2\nDirect\n0 0 0\n0 0 1\n")
        try:
            emit(f"{td}/o3", "x", bad_p, has_ni=False); chk(False, "[음성] 잘린 POSCAR 거부")
        except SystemExit:
            chk(True, "[음성] 원소행 없는 POSCAR 는 **거부** (조용히 넘어가지 않는다)")
        chk("절대 E_ads" in json.dumps(man, ensure_ascii=False),
            "슬랩 없으면 '절대 E_ads 불가' 를 manifest 에 남긴다")
        chk(all(not j["magmom_seeded"] for j in man["jobs"] if j["has_ni"]),
            "  (전제) 이 시험은 --no_magmom 이라 복합체에 MAGMOM 이 없다")
        # ⛔ 음성 U-P0-4 — 씨앗을 못 만들면 **조용히 MAGMOM 없이 내보내면 안 된다**.
        A3 = argparse.Namespace(**{**vars(A), "no_magmom": False, "out": f"{td}/o4"})
        try:
            build(A3)
            chk(False, "[음성 U-P0-4] AFM 씨앗 실패 시 중단")
        except SystemExit as e:
            chk("MAGMOM" in str(e) or "자기 basin" in str(e),
                "[음성 U-P0-4] AFM 씨앗을 못 만들면 **중단** — MAGMOM 없는 복합체는 "
                "wave1 과 다른 basin 으로 갈 수 있어 비교에 못 쓴다")
    print(f"selftest: {ok} 통과 / {bad} 실패")
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--complexes", default="db/structures/sdcp_wave1")
    ap.add_argument("--mols", default="/data/work/runs/sdcp_refs_freespin_v1/refs")
    ap.add_argument("--slabs", default="db/structures/sdcp_wave1")
    ap.add_argument("--out", default="/data/work/runs/sdcp_allF_v1")
    ap.add_argument("--frags", default="sdcp_neutral,ptfe_c10",
                    help="쉼표목록. 기본은 회신 T 최단 경로(dimer 제외 — 원자수 14 라 "
                         "분자당 비교의 근거로 쓰지 않기로 했다)")
    ap.add_argument("--basin", default="pm1",
                    help="이 문자열이 든 복합체만. 양쪽이 **같은 basin** 이어야 slab 이 소거된다")
    ap.add_argument("--with_slab", action="store_true",
                    help="절대 E_ads 까지 낼 때만. 없으면 조각 간 차이만 인용 가능")
    ap.add_argument("--no_magmom", action="store_true",
                    help="⚠ AFM 씨앗 없이 낸다 — **닫힘에 쓰지 마라** (자기 basin 미보증)")
    ap.add_argument("--no_spin_control", action="store_true",
                    help="⚠ 비영 MAGMOM 기체 대조를 빼면 회신 U B3(P0) 를 못 채운다")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    build(a)


if __name__ == "__main__":
    main()
