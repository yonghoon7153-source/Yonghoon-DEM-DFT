#!/usr/bin/env python3
"""make_allF_static_bundle.py — 조각 간 대비(ΔΔE_ads) 하나를 살리기 위한 **최소 번들**.

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
NUPDOWN  = -1
{dipol}{ldau}LWAVE    = .FALSE.
LCHARG   = .FALSE.
"""


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


def emit(jd, name, poscar, has_ni, com_frac=None):
    os.makedirs(jd, exist_ok=True)
    dst = os.path.join(jd, "POSCAR")
    shutil.copy(poscar, dst)
    sp = read_poscar_species(dst)
    if sp is None:
        sys.exit(f"⛔ {poscar}: POSCAR 원소행을 못 읽었다 — 조용히 넘어가지 않는다")
    els, cnt = sp
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
        STATIC.format(system=name, common=COMMON, dipol=dip, ldau=ldau))
    open(os.path.join(jd, "KPOINTS"), "w").write(
        "auto\n0\nGamma\n1 1 1\n0 0 0\n" if not has_ni else
        "auto\n0\nGamma\n2 2 1\n0 0 0\n")
    return {"name": name, "poscar_src": os.path.abspath(poscar),
            "poscar_sha256": sha(dst), "incar_sha256": sha(os.path.join(jd, "INCAR")),
            "species": els, "counts": cnt, "n_ions": sum(cnt),
            "has_ni": has_ni}


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
        jobs.append(emit(os.path.join(a.out, "complex", b), b, f, has_ni=True))

    # ── 기체 기준 분자 (box24) ────────────────────────────────────────────
    for p in pats:
        hits = sorted(glob.glob(os.path.join(a.mols, f"mol__{p}__box24", "POSCAR")))
        if not hits:
            sys.exit(f"⛔ mol__{p}__box24/POSCAR 을 {a.mols} 에서 못 찾았다. "
                     "기준 분자 없이는 E_ads 를 만들 수 없다 — 조용히 건너뛰지 않는다")
        nm = f"mol__{p}__box24"
        jobs.append(emit(os.path.join(a.out, "refs", nm), nm, hits[0],
                         has_ni=False, com_frac=com_fractional(hits[0])))

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
                               frags="sdcp_neutral,ptfe_c10", selftest=False)
        man = build(A)
        chk(man["n_jobs"] == 4, f"잡 4개 (복합체 2 + 분자 2) — 실제 {man['n_jobs']}")
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
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    build(a)


if __name__ == "__main__":
    main()
