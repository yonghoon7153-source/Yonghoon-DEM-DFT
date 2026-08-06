#!/usr/bin/env python3
"""qe_to_vasp.py — 확정된 Phase-B QE 입력 6개를 **외주용 VASP 패키지**로 변환한다.

왜 이렇게 하나 (2026-08-06)
  gabia(48 GB A6000) 한 장으로는 226원자 스핀분극 DFT+U 가 안 들어간다는 것이 7개 조합
  실측으로 확인됐다(kb/projects/sdcp_phaseB_direction_2026_08_06.md). 외주로 돌리려면
  필드 표준인 VASP 입력이 필요하다.

  ⚠ **xyz 에서 새로 만들지 않고 QE scf.in 에서 변환한다.** scf.in 에는 최종 셀·좌표·
    Ni1/Ni2 AFM 배정·U·자화 시드가 이미 확정돼 들어 있다. 거기서 뽑아야 "우리가 돌리려던
    그 계산"과 한 글자도 안 어긋난다.

⚠⚠ 코드가 바뀌면 절대값이 바뀐다 — 반드시 지킬 것
  · QE(USPP/PAW) 총에너지와 VASP(PAW) 총에너지는 **비교 불가**다.
  · 우리가 내는 값은 전부 차이(E_ads·Δ·ΔE_rxn·ΔE_extract)이므로, **6개 job 이 전부
    같은 코드·같은 설정**이기만 하면 내부적으로 일관된다. 절대 섞지 말 것.
  · U 는 투영 방식에 의존한다. QE 는 ortho-atomic, VASP 는 Dudarev(LDAUTYPE=2)의
    PAW 구 투영이라 같은 숫자가 같은 물리를 뜻하지 않는다. 다만 U(Ni)=6.2 eV 는
    Materials Project 의 VASP GGA+U 관례값이기도 하므로 이식이 부자연스럽지 않다.
    ⚠ 이 대응은 **원전 확인이 필요**하다(문헌 인용 전 검증할 것).

  python3 tools/sdcp/qe_to_vasp.py --src /data/work/runs/sdcp_v2/phaseB_v3 \\
                                   --out /data/work/runs/sdcp_v2/phaseB_vasp
"""
import argparse
import os
import re
import sys
from collections import OrderedDict

import numpy as np

RY2EV = 13.605693
# VASP PAW 는 QE USPP 와 기저가 달라 컷오프를 환산할 수 없다. POTCAR ENMAX 기준으로 잡는다.
#   O PAW(ENMAX 400 eV)가 최대 → 1.3× = 520 eV = Materials Project 표준.
ENCUT = 520.0
# VASP 권장 POTCAR (외주처가 라이선스 보유분에서 꺼낸다). 순서가 POSCAR 종 순서와 같아야 한다.
POTCAR_REC = OrderedDict([
    ("Li", "Li_sv"), ("Ni", "Ni_pv"), ("O", "O"), ("C", "C"), ("H", "H"), ("S", "S"),
])


def parse_scf_in(path):
    """QE scf.in → {cell, symbols(Ni1/Ni2 유지), positions, starting_mag, U}"""
    txt = open(path, errors="ignore").read()
    lines = txt.splitlines()

    cell = None
    for i, ln in enumerate(lines):
        if ln.strip().upper().startswith("CELL_PARAMETERS"):
            cell = np.array([[float(x) for x in lines[i + k].split()[:3]] for k in (1, 2, 3)])
            break
    if cell is None:
        raise SystemExit(f"⛔ {path}: CELL_PARAMETERS 없음")

    sym, pos = [], []
    for i, ln in enumerate(lines):
        u = ln.strip().upper()
        if u.startswith("ATOMIC_POSITIONS"):
            crystal = "CRYSTAL" in u
            for j in range(i + 1, len(lines)):
                s = lines[j].split()
                if len(s) < 4 or not re.match(r"^[A-Za-z]", s[0]):
                    break
                sym.append(s[0])
                p = np.array([float(s[1]), float(s[2]), float(s[3])])
                pos.append(p @ cell if crystal else p)
            break
    if not sym:
        raise SystemExit(f"⛔ {path}: ATOMIC_POSITIONS 없음")

    # starting_magnetization(i) 는 **분율**이다 (n↑−n↓)/n_valence.
    smag = {}
    for m in re.finditer(r"starting_magnetization\((\d+)\)\s*=\s*(-?[\d.]+)", txt):
        smag[int(m.group(1))] = float(m.group(2))
    order = []
    for ln in lines:
        m = re.match(r"^\s*([A-Za-z][A-Za-z0-9]*)\s+[\d.]+\s+\S+\.UPF", ln)
        if m:
            order.append(m.group(1))
    mag_by_species = {order[i - 1]: v for i, v in smag.items() if 0 < i <= len(order)}

    U = {}
    for m in re.finditer(r"^\s*U\s+(\S+)-(\S+)\s+([\d.]+)", txt, re.M):
        U[m.group(1)] = float(m.group(3))

    nbnd = re.search(r"nbnd\s*=\s*(\d+)", txt)
    return {"cell": cell, "sym": sym, "pos": np.array(pos), "mag": mag_by_species,
            "U": U, "nbnd": int(nbnd.group(1)) if nbnd else None,
            "degauss_ry": float((re.search(r"degauss\s*=\s*([\d.]+)", txt) or [0, 0.03])[1])
            if re.search(r"degauss", txt) else None}


def write_job(d, data, name, kpts="2 2 1"):
    os.makedirs(d, exist_ok=True)
    cell, sym, pos = data["cell"], data["sym"], data["pos"]

    # ⚠ Ni1/Ni2 는 **VASP 에서 같은 원소**다. AFM 은 종 분리가 아니라 **MAGMOM 원자별 부호**로
    #   낸다. 그래서 POSCAR 안에서 Ni1 무리 → Ni2 무리 순서를 유지하고 MAGMOM 을 맞춰 쓴다.
    groups = OrderedDict()                       # 'Li','Ni1','Ni2','O',... 순서 보존
    for i, s in enumerate(sym):
        groups.setdefault(s, []).append(i)

    vasp_species, counts, idx_all, magmom = [], [], [], []
    for lab, idxs in groups.items():
        el = "Ni" if lab.startswith("Ni") else lab
        if vasp_species and vasp_species[-1] == el:
            counts[-1] += len(idxs)              # Ni1 뒤에 Ni2 가 오면 한 블록으로 합친다
        else:
            vasp_species.append(el); counts.append(len(idxs))
        idx_all += idxs
        # QE starting_magnetization 은 분율 — VASP MAGMOM 은 μB 다. 부호만 승계하고
        # 크기는 물리값으로 준다(LiNiO2 의 Ni³⁺ 는 저스핀 d⁷ → ~1 μB).
        f = data["mag"].get(lab, 0.0)
        mu = (1.0 if f > 0 else -1.0) if abs(f) > 1e-8 else 0.0
        if el != "Ni":
            mu = 0.6 if abs(f) > 1e-8 else 0.0   # 라디칼 시드(S 등)는 작게
        magmom += [mu] * len(idxs)

    with open(os.path.join(d, "POSCAR"), "w") as f:
        f.write(f"{name}  (from QE scf.in — Phase-B v3, 2026-08-06)\n1.0\n")
        for v in cell:
            f.write("  %18.12f %18.12f %18.12f\n" % tuple(v))
        f.write("  " + "  ".join(vasp_species) + "\n")
        f.write("  " + "  ".join(str(c) for c in counts) + "\n")
        f.write("Cartesian\n")
        for i in idx_all:
            f.write("  %18.12f %18.12f %18.12f\n" % tuple(pos[i]))

    u_ni = data["U"].get("Ni1") or data["U"].get("Ni") or 6.2
    ldaul = " ".join("2" if e == "Ni" else "-1" for e in vasp_species)
    ldauu = " ".join(f"{u_ni}" if e == "Ni" else "0.0" for e in vasp_species)
    ldauj = " ".join("0.0" for _ in vasp_species)
    mm = " ".join(f"{m:g}" for m in magmom)

    with open(os.path.join(d, "INCAR"), "w") as f:
        f.write(f"""SYSTEM = SDCP/LiNiO2(104) Phase-B v3 : {name}

# ── 단일점 (구조 이완 없음) ─────────────────────────────────────────
#  기하는 MLIP(UMA, freeze_frac 0.85)로 이완한 것이다. 절대 이완하지 말 것 —
#  6개 job 이 같은 기하 규약 위에 있어야 차이값이 성립한다.
IBRION = -1
NSW    = 0
ISIF   = 0
PREC   = Accurate
ENCUT  = {ENCUT:.0f}          # POTCAR ENMAX(O 400 eV)의 1.3배 = MP 표준
                              # ⚠ QE 의 ecutwfc(Ry)에서 환산한 값이 아니다 — 기저가 다르다
EDIFF  = 1E-5
ALGO   = Normal
LREAL  = Auto                 # 226원자 규모에서 실공간 투영이 훨씬 싸다
LWAVE  = .FALSE.
LCHARG = .FALSE.
NELM   = 200

# ── 스핀 · AFM ──────────────────────────────────────────────────────
#  QE 의 Ni1/Ni2 부격자 배정을 그대로 옮겼다. VASP 에서는 같은 원소이므로
#  종 분리가 아니라 **MAGMOM 원자별 부호**로 AFM 을 준다.
ISPIN  = 2
MAGMOM = {mm}

# ── DFT+U (Dudarev) ────────────────────────────────────────────────
#  ⚠ U 는 투영 방식 의존적이다. QE 는 ortho-atomic, 여기는 PAW 구 투영이다.
#    U(Ni)=6.2 eV 는 Materials Project 의 VASP GGA+U 관례값과 같으나,
#    인용 전 원전 확인이 필요하다.
LDAU      = .TRUE.
LDAUTYPE  = 2
LDAUL     = {ldaul}
LDAUU     = {ldauu}
LDAUJ     = {ldauj}
LDAUPRINT = 1
LMAXMIX   = 4                 # d 전자계 필수 (안 넣으면 U 수렴이 흔들린다)

# ── 점유수 ─────────────────────────────────────────────────────────
#  금속성 Ni 표면이라 smearing. QE 는 Marzari-Vanderbilt 0.03 Ry(0.41 eV)였다.
ISMEAR = 1
SIGMA  = 0.2

# ── 분산 보정 ──────────────────────────────────────────────────────
#  QE 는 grimme-d3 였다. 자세마다 값이 달라 상쇄되지 않으므로 **6개 전부** 동일 적용.
IVDW = 11

# ── 병렬 (외주처 하드웨어에 맞게 조정) ──────────────────────────────
#  ⚠ 이 계산의 병목은 메모리다. NCORE 로 밴드를 쪼개고 랭크를 늘려야 한다.
#    gabia 48 GB 한 장에서는 QE 로 55-60 GB 급이 필요해 실패했다.
NCORE = 4
""")

    with open(os.path.join(d, "KPOINTS"), "w") as f:
        f.write(f"auto mesh (표준 레시피 복원)\n0\nGamma\n{kpts}\n0 0 0\n")

    with open(os.path.join(d, "POTCAR.spec"), "w") as f:
        f.write("# POTCAR 를 이 순서로 이어 붙일 것 (POSCAR 종 순서와 반드시 일치):\n")
        f.write("#   cat " + " ".join(f"$PP/{POTCAR_REC[e]}/POTCAR" for e in vasp_species)
                + " > POTCAR\n")
        for e in vasp_species:
            f.write(f"{e}\t{POTCAR_REC[e]}\n")
    return vasp_species, counts, len(sym)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="/data/work/runs/sdcp_v2/phaseB_v3")
    ap.add_argument("--out", default="/data/work/runs/sdcp_v2/phaseB_vasp")
    ap.add_argument("--kpts", default="2 2 1",
                    help="k-mesh. 기본 '2 2 1' = 표준 레시피(scf_u62.in) 복원. "
                         "gabia 에서 메모리 때문에 Γ-only 로 강제했던 것을 되돌린다.")
    ap.add_argument("--zip", action="store_true", help="끝나고 zip 으로 묶는다")
    a = ap.parse_args()

    JOBS = ("slab", "complex_doped", "complex_doped_extr", "complex_neutral",
            "mol_doped", "mol_neutral")
    os.makedirs(a.out, exist_ok=True)
    made = []
    for j in JOBS:
        p = os.path.join(a.src, j, "scf.in")
        if not os.path.isfile(p):
            print(f"⛔ 없음: {p}"); continue
        d = parse_scf_in(p)
        sp, ct, nat = write_job(os.path.join(a.out, j), d, j, a.kpts)
        print(f"✓ {j:22s} nat={nat:4d}  {'+'.join(f'{e}{c}' for e, c in zip(sp, ct))}")
        made.append(j)

    with open(os.path.join(a.out, "README_외주.md"), "w") as f:
        f.write(README.format(n=len(made), jobs="\n".join(f"  - {j}" for j in made),
                              kpts=a.kpts))
    rs = os.path.join(a.out, "run.sh")
    with open(rs, "w") as f:
        f.write(RUNSH.replace("@@JOBS@@", " ".join(made)))
    os.chmod(rs, 0o755)

    if a.zip:
        import shutil
        z = shutil.make_archive(a.out.rstrip("/"), "zip",
                                os.path.dirname(a.out), os.path.basename(a.out))
        print(f"\nzip → {z}  ({os.path.getsize(z)/1024:.0f} KB)")
    print(f"\n패키지 → {a.out}")
    print("   외주처는 run.sh 하나만 실행하면 된다 (POTCAR 경로만 설정).")
    return 0 if made else 1


README = """# SDCP × LiNiO₂(104) — Phase-B DFT+U 외주 의뢰서

## 무엇을 알고 싶은가
황화물 SE 첨가제(SDCP) 분자가 LiNiO₂ 양극 표면에서 **Li⁺ 를 뽑아내는가**.
MLIP(UMA) 스캔에서 라디칼(doped) 종만 표면 Li 를 2.35 Å 끌어내 술폰산 O 에
1.94–1.98 Å 로 배위했고(216 자세 중 9개에서 독립 재현), 중성 종은 108/108 에서
그 경로가 나오지 않았다. MLIP 은 산화상태를 명시적으로 보지 않아
Ni³⁺→Ni⁴⁺ 산화 대가를 안 물므로, **DFT+U 로 판정해야 한다.**

## 계산 (단일점 {n}개, 구조 이완 없음 · k-mesh {kpts} Γ-centered)
{jobs}

## 뽑을 값
```
E_ads(doped)   = E(complex_doped)      − E(slab) − E(mol_doped)     # 흡착에너지
E_ads(neutral) = E(complex_neutral)    − E(slab) − E(mol_neutral)   # 흡착에너지
Δ              = E_ads(doped) − E_ads(neutral)
ΔE_rxn(doped)  = E(complex_doped_extr) − E(slab) − E(mol_doped)     # **반응**에너지
ΔE_extract     = E(complex_doped_extr) − E(complex_doped)           # ★ 핵심
```
`ΔE_extract` 가 핵심이다 — 같은 조성·같은 셀의 두 기하 차이라 슬랩·분자 기준항이
전부 상쇄된다. **음수면 Li 추출이 열역학적으로 유리**하다는 뜻이다.

## 반드시 지켜야 할 것
1. **구조를 이완하지 말 것** (`NSW=0`, `IBRION=-1`). 기하는 MLIP 으로 이완한 것이고,
   {n}개 job 이 같은 기하 규약 위에 있어야 차이값이 성립한다.
2. **{n}개 job 을 전부 같은 설정**으로 돌릴 것 (ENCUT·ISMEAR·SIGMA·U·IVDW·PREC).
   하나라도 다르면 그 job 만 다른 수치 체계가 되어 차이값이 깨진다.
3. **MAGMOM 을 바꾸지 말 것.** Ni 의 +/− 배열이 AFM 부격자다. 초기값을 뭉개면
   다른 자기 상태로 수렴해 ΔE 가 추출이 아니라 스핀 전이를 재게 된다.
4. 수렴 후 **각 job 의 총 자화·절대 자화를 보고**해 줄 것. 세 복합체의 절대 자화가
   2 μB 이상 벌어지면 그 결과는 쓸 수 없다.

## 참고 — 우리 쪽에서 못 돌린 이유
226원자 · 스핀분극 · DFT+U 를 QE 7.4.1 GPU 로 48 GB A6000 한 장에서 시도했으나,
방어 가능한 최저 설정(진공 11 Å, ecutwfc 50 Ry, ecutrho 360 Ry, PPCG)에서도
실측 peak 47.6 GB 로 실패했다. 크래시 자리가 newd → cegterg → becmod 로 계속
옮겨간 것으로 보아 필요량은 **55–60 GB 급**이다. 80 GB 카드 1장 또는 다중 GPU/노드
평면파 분산이면 충분하다.

## 산출물로 받고 싶은 것
- job 별 `OUTCAR` (또는 최소한 최종 `free energy TOTEN` · 자화 · SCF 수렴 이력)
- 사용한 POTCAR 종류와 VASP 버전
- 실제 사용한 INCAR (수정했다면 무엇을 왜 바꿨는지)
"""




RUNSH = r'''#!/usr/bin/env bash
# =============================================================================
# run.sh — SDCP × LiNiO2(104) Phase-B DFT+U. **이것만 실행하면 됩니다.**
#
#   1) 아래 VASP_PP_PATH 를 귀사의 POTCAR 라이브러리 경로로 바꿔 주세요.
#   2) 필요하면 VASP_CMD 를 귀사의 실행 방식으로 바꿔 주세요.
#   3) bash run.sh
#
# 중간에 끊겨도 다시 실행하면 **끝난 job 은 건너뜁니다** (OUTCAR 의 완료 표시로 판단).
# 모두 끝나면 결과 요약(RESULTS.txt)이 자동으로 만들어집니다.
# =============================================================================
set -uo pipefail

# ── 여기 두 줄만 환경에 맞게 ────────────────────────────────────────────────
VASP_PP_PATH=${VASP_PP_PATH:-/opt/vasp/potpaw_PBE.54}   # <각 원소 폴더가 들어 있는 상위 경로>
VASP_CMD=${VASP_CMD:-"mpirun -np 32 vasp_std"}          # <귀사의 실행 명령>
# ---------------------------------------------------------------------------

JOBS=(@@JOBS@@)
HERE=$(cd "$(dirname "$0")" && pwd); cd "$HERE"
echo "=== SDCP Phase-B DFT+U · $(date) ==="
echo "  POTCAR 경로 : $VASP_PP_PATH"
echo "  실행 명령   : $VASP_CMD"
echo

# POTCAR 조립 — POSCAR 의 종 순서와 반드시 같아야 합니다.
build_potcar () {
  local d=$1
  [ -s "$d/POTCAR" ] && return 0
  local specs; specs=$(awk 'NR>1 && $1!~/^#/ {print $2}' "$d/POTCAR.spec")
  : > "$d/POTCAR"
  for s in $specs; do
    if [ -f "$VASP_PP_PATH/$s/POTCAR" ]; then cat "$VASP_PP_PATH/$s/POTCAR" >> "$d/POTCAR"
    elif [ -f "$VASP_PP_PATH/$s/POTCAR.Z" ]; then zcat "$VASP_PP_PATH/$s/POTCAR.Z" >> "$d/POTCAR"
    else echo "  !! POTCAR 없음: $VASP_PP_PATH/$s/POTCAR"; rm -f "$d/POTCAR"; return 1; fi
  done
  echo "  POTCAR 조립: $(echo $specs | tr '\n' ' ')"
}

# 작은 job 부터 — 설정 오류를 몇 분 만에 잡습니다.
ORDER=(mol_doped mol_neutral slab complex_doped complex_doped_extr complex_neutral)
for j in "${ORDER[@]}"; do
  [ -d "$j" ] || continue
  if grep -q "General timing and accounting" "$j/OUTCAR" 2>/dev/null; then
    echo "[$j] 이미 완료 — 건너뜀"; continue
  fi
  echo "[$j] 시작 $(date +%H:%M:%S)"
  build_potcar "$j" || { echo "[$j] POTCAR 실패 — 중단"; exit 1; }
  ( cd "$j" && eval "$VASP_CMD" > vasp.log 2>&1 )
  if grep -q "General timing and accounting" "$j/OUTCAR" 2>/dev/null; then
    e=$(grep -a "free  energy   TOTEN" "$j/OUTCAR" | tail -1 | awk '{print $(NF-1)}')
    m=$(grep -a "number of electron" "$j/OUTCAR" | tail -1 | awk '{print $NF}')
    echo "[$j] 완료  TOTEN = $e eV  ·  총자화 = $m"
  else
    echo "[$j] !! 미완 — $j/vasp.log 와 OUTCAR 끝부분을 확인해 주세요"
    tail -5 "$j/vasp.log" 2>/dev/null
  fi
done

# ── 결과 정리 ──────────────────────────────────────────────────────────────
E () { grep -a "free  energy   TOTEN" "$1/OUTCAR" 2>/dev/null | tail -1 | awk '{print $(NF-1)}'; }
{
  echo "SDCP x LiNiO2(104) Phase-B DFT+U — 결과  ($(date))"
  echo "=================================================================="
  for j in "${ORDER[@]}"; do
    [ -d "$j" ] || continue
    printf "%-22s TOTEN = %-18s  |mag| = %s\n" "$j" "$(E $j)" \
      "$(grep -a 'number of electron' "$j/OUTCAR" 2>/dev/null | tail -1 | awk '{print $NF}')"
  done
  echo
  python3 - <<'PY' 2>/dev/null || echo "(python3 없음 — 위 TOTEN 으로 아래 식을 직접 계산해 주세요)"
import re, os
def E(j):
    p = os.path.join(j, "OUTCAR")
    if not os.path.isfile(p): return None
    m = re.findall(r"free  energy   TOTEN\s*=\s*(-?[\d.]+)", open(p, errors="ignore").read())
    return float(m[-1]) if m else None
e = {j: E(j) for j in ("slab","complex_doped","complex_doped_extr",
                       "complex_neutral","mol_doped","mol_neutral")}
def ads(cx, mol):
    return None if None in (e[cx], e["slab"], e[mol]) else e[cx]-e["slab"]-e[mol]
ad, an = ads("complex_doped","mol_doped"), ads("complex_neutral","mol_neutral")
rx = ads("complex_doped_extr","mol_doped")
if ad is not None: print(f"E_ads(doped, physisorbed)   = {ad:+.4f} eV")
if an is not None: print(f"E_ads(neutral, physisorbed) = {an:+.4f} eV")
if None not in (ad,an):   print(f"Delta = E_ads(d)-E_ads(n)   = {ad-an:+.4f} eV")
if rx is not None:        print(f"dE_rxn(doped)               = {rx:+.4f} eV   (reaction, NOT adsorption)")
if None not in (e["complex_doped_extr"], e["complex_doped"]):
    dx = e["complex_doped_extr"] - e["complex_doped"]
    print(f"*** dE_extract(doped)       = {dx:+.4f} eV   <-- KEY NUMBER")
    print("    negative => Li extraction is thermodynamically favourable")
PY
} | tee RESULTS.txt

echo
echo "=== 끝. RESULTS.txt 와 각 job 의 OUTCAR 를 회신해 주세요. ==="
'''

if __name__ == "__main__":
    sys.exit(main())
