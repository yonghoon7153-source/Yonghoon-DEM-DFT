#!/usr/bin/env python3
"""build_v5_vasp_package.py — A′ V5 (LPSCl|Ag(111) 작은 주기 계면) **VASP 외주 패키지** · 반송 검사 · W/G3/G4/G5 집계.

왜 있나 (2026-09-27 · 1저자 "v5 관련해서 vasp 용으로 외주건으로 한번 만들어보고 codex 리뷰 받자 · 될지는 모르지만 준비는 해둬볼게")
  V5 는 우리 GPU 한 장(48 GB)에 안 들어가 RESOURCE_BLOCKED 였다 (QE CPU 추정 89–109 GB @70 Ry · 축소 변형도 61–80 GB).
  외주(큰 CPU 노드의 VASP)라면 들어간다. 이 도구는 **봉인된 S3v2 패키지를 입력으로 읽어** V5 18 잡을 VASP 로 옮긴다 —
  구조를 새로 만들지 않는다 (좌표는 S3v2 구조 파일 sha 로 결박 · 다르면 만들지 않는다).

왜 새 파일인가 (코드 규율 사다리): QE 입력을 만든 `build_aprime_s3.py` 는 S3/S3v2 봉인에 **파일 sha 로 결박**돼 있다.
  거기에 VASP 경로를 섞으면 "어느 판이 무엇을 만들었나" 가 흐려진다. 이 파일은 봉인 산출물(구조·잡 목록·쌍극자 구간)만 읽는 번역기다.
  쌍극자 구간 규칙은 `build_aprime_interfaces.dip_region` (개정 2) 의 결과(S3v2 jobs.json 의 emaxpos·eopreg)를 그대로 옮긴다.

무엇을 만드나 (--build)
  · jobs/<잡>/ POSCAR (종 순서 Li P S Cl Ag · 데카르트 · 원래 원자 번호 대응표는 jobs.json) · INCAR · INCAR.r1 (사전등록 재시도) · KPOINTS · POTCAR.spec
  · run_all.sh (업체 러너: 입력 sha 검사 → POTCAR 조립(업체 라이선스) → 실행 → 종료·수렴 검사 → 미수렴이면 INCAR.r1 로 **1 회만** → 반송 묶음)
  · README.md (업체용) · jobs.json (잡 명세·구조 sha·원자 대응·쌍극자·s-dftd3 2체 D3 기대값) · MANIFEST.sha256 (sha256sum -c 형식)
설정 (VASP · 개정 3 초안): PBE PAW (Li_sv·P·S·Cl·Ag) · ENCUT 520 eV · PREC Accurate · EDIFF 1e-6 · ISMEAR 1 · SIGMA 0.136 eV (= QE degauss 0.01 Ry)
  · LASPH · LREAL F · ISYM 0 · ISPIN 1 · IVDW 12 (D3-BJ 2체 · PBE 계수 명시) · LDIPOL IDIPOL 3 · DIPOL_z = (진공 중앙 − 0.5) mod 1 · Γ 3×2×1
  G4 변형: ENCUT 650 (QE e70 자리) · Γ 4×3×1 (k1) · SIGMA 0.068 (s05).  재시도 INCAR.r1: AMIX 0.1 · BMIX 0.01 · NELM 300 (그 밖 동일).

반송 검사 (--check) — fail-closed: 파일 누락 MISSING · 입력 변경 INPUT_MODIFIED (허용 성능 태그 NCORE/NPAR/KPAR/NSIM/LPLANE/LSCALU/LSCALAPACK 만 예외)
  · POTCAR TITEL/ZVAL 불일치 POTCAR_MISMATCH · 없음 POTCAR_UNVERIFIED · 비정상 종료 NOT_TERMINATED · 전자 미수렴 SCF_NOT_CONVERGED
  · NIONS/NELECT 불일치 SYSTEM_MISMATCH · Edisp 없음 D3_UNVERIFIED · Edisp 가 s-dftd3 2체 기대값과 1 % 넘게 다름 D3_MISMATCH (감쇠·3체 오설정 탐지)
집계 (--collect) — 카드 v5 식: W = [F(far) − F(bound)]/A (F = TOTEN 자유에너지 · E(σ→0) 병기) · ΔD3 = [Edisp(far) − Edisp(bound)]/A · W_PBE = W − ΔD3
  · G3 (표본 ①): |ΔW| ≤ 0.01 두 검사 모두 · G4: |ΔW| ≤ 0.02 변형마다 · G5 (UMA JSON 있을 때): W_UMA+D3 := W_UMA + ΔD3_VASP (개정 1 과 같은 구조)
    → Δ_i = W_VASP − W_UMA+D3 · 표본마다 |Δ| ≤ 0.10 · 종결 군(S ①②⑤ · Li ③④) |mean Δ| ≤ 0.05 · 5/5 유효 · G3·G4 PASS → PASS (분모 5 고정)

⛔ 이 도구가 못 하는 것
  · POTCAR 파일을 만들거나 검사하지 못한다 (VASP 라이선스 — 업체 보유분) · 반송된 TITEL/ZVAL 줄과 POTCAR sha 만 본다.
  · VASP 값을 QE 값(V2·V4)과 한 표에서 빼거나 섞지 않는다 — 코드·PP 가 달라 절대값·차이 모두 다른 비교군이다.
  · OUTCAR 문구는 VASP 버전마다 조금씩 다르다 — 특히 `Edisp` 줄. 첫 납품(파일럿 1 잡)으로 파서를 확인한 뒤 전체를 받는다.
  · UMA 에너지를 계산하지 않는다 (`relax_uma_d3.py --energies` 의 JSON 을 받는다) · 결과를 보고 표본·문턱·분모를 바꾸지 않는다.
  · 업체 기계의 시간·메모리를 보장하지 않는다 — README 의 추정은 평면파·밴드 수에서 낸 대략값이다.

사용
  python3 tools/wad/build_v5_vasp_package.py --build --pkg db/inputs/wad_aprime_s3v2_2026_09_26 --out db/inputs/wad_aprime_v5_vasp_2026_09_27
  python3 tools/wad/build_v5_vasp_package.py --check --out <패키지> --ret <반송 폴더(run/…)>
  python3 tools/wad/build_v5_vasp_package.py --collect --out <패키지> --ret <반송 폴더> [--uma uma.json] [--json result.json]
  python3 tools/wad/build_v5_vasp_package.py --selftest
"""
import argparse
import hashlib
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

SPECIES_ORDER = ("Li", "P", "S", "Cl", "Ag")
POTCAR_MAP = {"Li": "Li_sv", "P": "P", "S": "S", "Cl": "Cl", "Ag": "Ag"}
ZVAL = {"Li": 3.0, "P": 5.0, "S": 6.0, "Cl": 7.0, "Ag": 11.0}          # PAW_PBE (54) 표준 원자가
ENCUT_BASE, ENCUT_G4E = 520.0, 650.0
SIGMA_BASE = 0.136                                                    # eV = QE degauss 0.01 Ry (13.6057 × 0.01)
KP_G4K = (4, 3, 1)
D3_PARAMS = {"s6": 1.0, "s8": 0.7875, "a1": 0.4289, "a2": 4.4407}     # S1 결박값 (QE dftd3_version 4 · PBE BJ)
PERF_TAGS = ("NCORE", "NPAR", "KPAR", "NSIM", "LPLANE", "LSCALU", "LSCALAPACK")
RESCUE = {"AMIX": "0.1", "BMIX": "0.01", "NELM": "300"}
DIP_MIN_CLEAR_A = 4.0
D3_REL_TOL = 0.01
G3_DW, G4_DW, G5_PER, G5_MEAN = 0.01, 0.02, 0.10, 0.05
G5_SAMPLES = {"①": ("V5_s_outer_A_bound", "V5_s_outer_A_far"), "②": ("V5_s_outer_B_bound", "V5_s_outer_B_far"),
              "③": ("V5_li_outer_A_bound", "V5_li_outer_A_far"), "④": ("V5_li_outer_B_bound", "V5_li_outer_B_far"),
              "⑤": ("V5_s_outer_A_p05_bound", "V5_s_outer_A_far")}
G5_GROUPS = {"s_outer": ("①", "②", "⑤"), "li_outer": ("③", "④")}
EV_J, A2_M2 = 1.602176634e-19, 1e-20
HB2M = 3.80998212                                                     # ħ²/2mₑ [eV·Å²] — 평면파 수 추정용


class PkgError(Exception):
    pass


def _sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def _sha_text(t):
    return hashlib.sha256(t.encode()).hexdigest()


# ───────────────────────── 입력 만들기 ─────────────────────────
def poscar_text(atoms, comment):
    """종 순서 SPECIES_ORDER 로 묶은 POSCAR (데카르트). 반환: (본문, 원래 원자 번호 목록 = POSCAR 순서)."""
    sym = atoms.get_chemical_symbols()
    unknown = sorted(set(sym) - set(SPECIES_ORDER))
    if unknown:
        raise PkgError(f"POSCAR: 모르는 원소 {unknown}")
    order = [i for sp in SPECIES_ORDER for i, s in enumerate(sym) if s == sp]
    present = [sp for sp in SPECIES_ORDER if sp in sym]
    c = atoms.cell.array; p = atoms.get_positions()
    L = [comment, "1.0"] + ["  " + " ".join(f"{x:16.10f}" for x in c[k]) for k in range(3)]
    L += ["  " + " ".join(present), "  " + " ".join(str(sym.count(sp)) for sp in present), "Cartesian"]
    L += ["  " + " ".join(f"{x:16.10f}" for x in p[i]) for i in order]
    return "\n".join(L) + "\n", order, present


def parse_poscar_cart(text):
    """selftest·검사용 — (종 목록, 개수, 셀, 좌표) 로 되읽는다."""
    ln = text.splitlines()
    cell = [[float(x) for x in ln[k].split()] for k in (2, 3, 4)]
    sp = ln[5].split(); nn = [int(x) for x in ln[6].split()]
    pos = [[float(x) for x in l.split()[:3]] for l in ln[8:8 + sum(nn)]]
    return sp, nn, cell, pos


def dipol_z(emaxpos, eopreg):
    """QE 톱니 불연속 구간 중심(emaxpos + eopreg/2) → VASP DIPOL_z. VASP 의 보정 불연속은 DIPOL ± ½ 에 놓이므로 중심 − ½ (mod 1)."""
    return (emaxpos + 0.5 * eopreg - 0.5) % 1.0


def check_dip_clear(atoms, emaxpos, eopreg, min_clear=DIP_MIN_CLEAR_A):
    """구간 [emaxpos, emaxpos+eopreg]·c 의 가장자리에서 어느 핵(주기 영상 포함)이든 ≥ min_clear. 아니면 PkgError."""
    c = float(atoms.cell.array[2, 2]); lo, hi = emaxpos * c, (emaxpos + eopreg) * c
    worst = min(min(abs(z + s * c - lo), abs(z + s * c - hi)) if not (lo <= z + s * c <= hi) else 0.0
                for z in atoms.get_positions()[:, 2] for s in (-1, 0, 1))
    if worst < min_clear - 1e-3:      # emaxpos·eopreg 는 dip_region 이 소수 5 자리로 반올림 → c ≤ 40 Å 에서 재계산 오차 ≤ 2e-4 Å
        raise PkgError(f"쌍극자 구간 [{lo:.3f}, {hi:.3f}] Å 에서 가장 가까운 핵까지 {worst:.3f} Å < {min_clear} Å")
    return round(worst, 3)


def incar_text(job, encut, sigma, dz, rescue=False):
    L = [f"SYSTEM = A-prime V5 {job} (single point){' - pre-registered retry r1' if rescue else ''}",
         "GGA = PE", "PREC = Accurate", f"ENCUT = {encut:.1f}", "EDIFF = 1E-6",
         f"NELM = {RESCUE['NELM'] if rescue else 200}", "NELMIN = 6", "ALGO = Normal",
         "ISPIN = 1", "ISMEAR = 1", f"SIGMA = {sigma:.4f}", "LASPH = .TRUE.", "LREAL = .FALSE.", "ISYM = 0",
         "IBRION = -1", "NSW = 0",
         "IVDW = 12", f"VDW_S6 = {D3_PARAMS['s6']}", f"VDW_S8 = {D3_PARAMS['s8']}", f"VDW_A1 = {D3_PARAMS['a1']}", f"VDW_A2 = {D3_PARAMS['a2']}",
         "LDIPOL = .TRUE.", "IDIPOL = 3", f"DIPOL = 0.5 0.5 {dz:.6f}",
         "LWAVE = .FALSE.", "LCHARG = .FALSE."]
    if rescue:
        L += [f"AMIX = {RESCUE['AMIX']}", f"BMIX = {RESCUE['BMIX']}"]
    return "\n".join(L) + "\n"


def kpoints_text(k):
    return f"Gamma-centred mesh (A-prime V5)\n0\nGamma\n{k[0]} {k[1]} {k[2]}\n0 0 0\n"


def parse_incar(text):
    d = {}
    for ln in text.splitlines():
        ln = ln.split("#")[0].split("!")[0].strip()
        if "=" in ln:
            k, v = ln.split("=", 1); d[k.strip().upper()] = " ".join(v.split())
    return d


def estimate(atoms, encut, kp):
    """대략 규모 — NELECT · 기본 NBANDS · 평면파 수 · 파동함수 메모리(모든 k 합). 업체 기계 시간은 추정하지 않는다."""
    sym = atoms.get_chemical_symbols(); n = len(sym)
    nel = sum(ZVAL[s] for s in sym); nb = int(math.ceil(nel / 2 + n / 2))
    V = abs(float(atoms.get_volume())); kmax = math.sqrt(encut / HB2M)
    npw = V * kmax ** 3 / (6 * math.pi ** 2)
    nk_full = kp[0] * kp[1] * kp[2]; nk_irr = (nk_full + 1) // 2 + (1 if nk_full % 2 == 0 else 0)
    return {"NIONS": n, "NELECT": nel, "NBANDS_default": nb, "NPW_per_k": int(npw), "nk_full": nk_full, "nk_irr_est": nk_irr,
            "wfc_GB_all_k": round(nb * npw * 16 * nk_irr / 1e9, 1)}


def d3_2body_eV(atoms):
    """s-dftd3 2체 D3(BJ) — VASP Edisp 대조용 기대값 [eV]. 없으면 None (검사가 D3_UNVERIFIED 로 둔다)."""
    try:
        import numpy as np
        from dftd3.interface import RationalDampingParam, DispersionModel
    except Exception:
        return None
    B = 0.529177210903
    m = DispersionModel(atoms.get_atomic_numbers(), atoms.get_positions() / B, atoms.cell.array / B, np.array([True, True, True]))
    return float(m.get_dispersion(RationalDampingParam(**D3_PARAMS, s9=0.0), grad=False)["energy"]) * 27.211386245988


RUN_ALL = r'''#!/usr/bin/env bash
# =============================================================================
# run_all.sh — A′ V5 VASP 단일점 18 잡 (필요 시 잡마다 사전등록 재시도 INCAR.r1 **1 회**)
#   필수 환경변수: VASP_CMD   (예: "mpirun -np 128 vasp_std")
#                 POTCAR_DIR (PAW_PBE 폴더 — <POTCAR_DIR>/Li_sv/POTCAR · P · S · Cl · Ag)
#   선택: PERF_TAGS_FILE (NCORE/NPAR/KPAR/NSIM/LPLANE/LSCALU/LSCALAPACK 만 허용) · JOBS="잡1 잡2" (일부만 · 파일럿)
#   ⛔ INCAR·POSCAR·KPOINTS 를 고치지 마세요 — 성능 태그는 PERF_TAGS_FILE 로만. 고친 입력은 반송 검사에서 무효가 됩니다.
#   ⛔ POTCAR 는 반송하지 않습니다 (라이선스) — TITEL/ZVAL 줄과 sha256 만 남깁니다.
# =============================================================================
set -u
HERE=$(cd "$(dirname "$0")" && pwd); cd "$HERE"
: "${VASP_CMD:?VASP_CMD 를 주세요 (예: mpirun -np 128 vasp_std)}"
: "${POTCAR_DIR:?POTCAR_DIR 를 주세요 (PAW_PBE 폴더)}"
ALLOW='^[[:space:]]*(NCORE|NPAR|KPAR|NSIM|LPLANE|LSCALU|LSCALAPACK)[[:space:]]*='
sha256sum -c --quiet MANIFEST.sha256 || { echo "⛔ 패키지 파일이 MANIFEST 와 다르다 — 실행하지 않는다"; exit 2; }
if [ -n "${PERF_TAGS_FILE:-}" ]; then
  BAD=$(grep -vE '^[[:space:]]*(#|$)' "$PERF_TAGS_FILE" | grep -vE "$ALLOW" || true)
  [ -z "$BAD" ] || { echo "⛔ PERF_TAGS_FILE 에 허용 밖 태그: $BAD"; exit 2; }
fi
JOBS=${JOBS:-$(cat JOBS.txt)}
mkdir -p run
{ echo "date_utc $(date -u +%FT%TZ)"; echo "host $(hostname)"; echo "VASP_CMD $VASP_CMD"; echo "POTCAR_DIR $POTCAR_DIR";
  echo "PERF_TAGS $(grep -vE '^[[:space:]]*(#|$)' "${PERF_TAGS_FILE:-/dev/null}" 2>/dev/null | tr '\n' ';')"; } >> run/env.txt
[ -f run/status.tsv ] || printf "job\tattempt\trc\tterminated\tconverged\tn_elec_steps\tTOTEN_eV\twall_s\n" > run/status.tsv
run_one(){  # $1 잡 · $2 시도(""|r1) · $3 INCAR 파일
  local job=$1 att=$2 inc=$3 d; d=run/${job}${2:+_$2}; mkdir -p "$d"
  cp "jobs/$job/POSCAR" "jobs/$job/KPOINTS" "$d/"; cp "jobs/$job/$inc" "$d/INCAR"
  [ -n "${PERF_TAGS_FILE:-}" ] && grep -vE '^[[:space:]]*(#|$)' "$PERF_TAGS_FILE" >> "$d/INCAR"
  : > "$d/POTCAR"
  while read -r p; do [ -n "$p" ] || continue; cat "$POTCAR_DIR/$p/POTCAR" >> "$d/POTCAR" || { echo "⛔ POTCAR $p 없음"; return 3; }; done < "jobs/$job/POTCAR.spec"
  grep -E "TITEL|ZVAL|VRHFIN" "$d/POTCAR" > "$d/POTCAR.titel"; sha256sum "$d/POTCAR" | cut -d' ' -f1 > "$d/POTCAR.sha256"
  local t0 t1 rc term conv nel E; t0=$(date +%s); (cd "$d" && $VASP_CMD > stdout.log 2>&1); rc=$?; t1=$(date +%s)
  term=0; grep -q "General timing and accounting" "$d/OUTCAR" 2>/dev/null && term=1
  conv=0; grep -q "aborting loop because EDIFF is reached" "$d/OUTCAR" 2>/dev/null && conv=1
  grep -q "EDIFF was not reached" "$d/OUTCAR" 2>/dev/null && conv=0
  nel=$(grep -cE "^(DAV|RMM|CG|SDA):" "$d/OSZICAR" 2>/dev/null); nel=${nel:-0}
  E=$(grep "free  energy   TOTEN" "$d/OUTCAR" 2>/dev/null | tail -1 | awk '{print $5}')
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$job" "${att:-0}" "$rc" "$term" "$conv" "$nel" "${E:-NA}" "$((t1-t0))" >> run/status.tsv
  rm -f "$d/POTCAR" "$d/WAVECAR" "$d/CHGCAR" "$d/CHG" "$d/vasprun.xml"
  [ "$term" = 1 ] && [ "$conv" = 1 ]
}
for job in $JOBS; do
  [ -d "jobs/$job" ] || { echo "⛔ 모르는 잡 $job"; exit 2; }
  if run_one "$job" "" INCAR; then echo "✓ $job"
  else echo "… $job 미종료·미수렴 → 사전등록 재시도 1 회 (INCAR.r1: AMIX 0.1 · BMIX 0.01 · NELM 300)"
       run_one "$job" r1 INCAR.r1 && echo "✓ $job (r1)" || echo "⛔ $job r1 도 실패 — 값 없음으로 둔다 (다른 설정으로 더 돌리지 않는다)"
  fi
done
tar czf V5_vasp_return.tgz run MANIFEST.sha256 && sha256sum V5_vasp_return.tgz > V5_vasp_return.tgz.sha256
echo "✅ 끝 — V5_vasp_return.tgz 와 V5_vasp_return.tgz.sha256 을 보내 주세요"
'''


def _readme(jobs, est, pkg_sha):
    rows = "\n".join(f"| `{j['dir']}` | {j['role']} | {j['nions']} | {j['encut']:.0f} | {'×'.join(map(str, j['kpts']))} | {j['sigma']:.3f} |" for j in jobs)
    return f"""# A′ V5 — VASP 단일점 외주 패키지 (LPSCl | Ag(111) 작은 주기 계면)

> 상태: **준비본 (실행 미정)** · 설계 리뷰(Codex CE) 전 · 결정 `D-2026-09-27-wad-aprime-v5-vasp-route` **proposed**
> 원본: 봉인 S3v2 패키지 (구조 파일 sha 결박) · 이 패키지 MANIFEST.sha256 의 sha256 = `{pkg_sha}` (보낼 때 메일 본문에 적는다)

## 무엇을 하나
PBE+D3(BJ) **단일점(SCF) 18 개** — 이완 없음. 좌표는 이미 정해져 있습니다 (POSCAR 그대로).

| 잡 | 역할 | 원자 | ENCUT (eV) | k (Γ) | SIGMA (eV) |
|---|---|---|---|---|---|
{rows}

## 돌리는 법
1. **파일럿 1 잡 먼저** (파서 확인용 · 반송해 주세요): `JOBS=V5_s_outer_A_far VASP_CMD="mpirun -np <N> vasp_std" POTCAR_DIR=<PAW_PBE> bash run_all.sh`
2. 확인 연락을 받으면 전체: `VASP_CMD=... POTCAR_DIR=... bash run_all.sh` (이미 끝난 잡도 다시 돕니다 — 파일럿 폴더는 `run/` 밖으로 옮겨 두세요)
3. 성능 태그는 `PERF_TAGS_FILE=perf.txt` 로만 (허용: NCORE NPAR KPAR NSIM LPLANE LSCALU LSCALAPACK). **INCAR·POSCAR·KPOINTS 는 고치지 마세요.**
4. 한 잡이 수렴하지 않으면 러너가 미리 정한 재시도(INCAR.r1 · AMIX 0.1 · BMIX 0.01 · NELM 300)를 **한 번만** 합니다. 그래도 안 되면 그 잡은 비워 둡니다 — 다른 설정으로 더 돌리지 마세요.

## POTCAR (업체 라이선스 보유분)
PAW_PBE **Li_sv · P · S · Cl · Ag** (PBE_54 권장 · Materials Project 와 같은 선택). 각 잡의 `POTCAR.spec` 순서대로 러너가 조립합니다.
POTCAR 파일은 **보내지 마세요** — 러너가 TITEL/ZVAL 줄과 sha256 만 남깁니다.

## 돌려받을 것
`V5_vasp_return.tgz` + `.sha256` (러너가 만듭니다): 잡별 OUTCAR · OSZICAR · INCAR(실행본) · KPOINTS · POSCAR · POTCAR.titel · POTCAR.sha256 · stdout.log · `run/status.tsv` · `run/env.txt`.
VASP 버전·컴파일러·노드/코어 수를 `run/env.txt` 에 한 줄씩 덧붙여 주세요.

## 규모 (대략 · 우리 추정)
NIONS 176–200 · NELECT {est['nel_min']:.0f}–{est['nel_max']:.0f} · 기본 NBANDS ~{est['nb_max']} · 평면파 ~{est['npw_max']:,}/k (ENCUT 520) · 파동함수 전체 ~{est['wfc_max']} GB (k 4–7 개 합).
비스핀 · 금속(Ag) 슬랩 · 진공 포함 · LREAL=F. 시간은 기계마다 달라 파일럿 1 잡의 벽시계로 전체를 가늠합니다.

## English summary
18 single-point PBE+D3(BJ) SCF runs (no relaxation) on fixed geometries; PAW_PBE Li_sv/P/S/Cl/Ag; ENCUT 520 eV; ISMEAR 1, SIGMA 0.136 eV;
IVDW 12 with explicit PBE-BJ parameters; dipole correction along z (LDIPOL, IDIPOL 3, DIPOL given). Please run one pilot job first
(`JOBS=V5_s_outer_A_far`) and return it; do not edit INCAR/POSCAR/KPOINTS (performance tags only via PERF_TAGS_FILE); do not send POTCAR files.
"""


def build(pkg, out, want_d3=True):
    from ase.io import read
    qe = json.load(open(os.path.join(pkg, "qe", "jobs.json"), encoding="utf-8"))
    man_path = os.path.join(pkg, "s3_manifest.json"); man = json.load(open(man_path, encoding="utf-8"))
    if qe.get("s3_manifest_sha256") != _sha(man_path):
        raise PkgError("S3 manifest sha 가 qe/jobs.json 에 적힌 값과 다르다 — 봉인 패키지가 아니다")
    ssha = man["structures_sha256"]
    v5 = [j for j in qe["jobs"] if j.get("model") == "V5" and j.get("kind") != "probe"]
    if len(v5) != 18:
        raise PkgError(f"V5 잡이 18 개가 아니다 ({len(v5)}) — 카드 표본(5 표본 · G3 3 · G4 6)과 다르다")
    os.makedirs(os.path.join(out, "jobs"), exist_ok=True)
    jobs, cache, d3c = [], {}, {}
    for j in v5:
        st = j["structure"]; sp = os.path.join(pkg, "structures", f"{st}.extxyz")
        if st not in ssha or _sha(sp) != ssha[st]:
            raise PkgError(f"{j['dir']}: 구조 {st} 의 sha 가 봉인 manifest 와 다르다")
        at = cache.setdefault(st, read(sp))
        tags = j.get("tags") or {}; g4 = tags.get("G4", "") or ""
        encut = ENCUT_G4E if "e70" in g4 else ENCUT_BASE
        sigma = SIGMA_BASE / 2 if ("s05" in g4 or tags.get("degauss_halved")) else SIGMA_BASE
        kp = tuple(j["kpts"])
        if "k1" in g4 and kp != KP_G4K:
            raise PkgError(f"{j['dir']}: G4 k1 인데 k 가 {kp}")
        emx, eop = j["dip"]["emaxpos"], j["dip"]["eopreg"]
        clear = check_dip_clear(at, emx, eop); dz = dipol_z(emx, eop)
        d = os.path.join(out, "jobs", j["dir"]); os.makedirs(d, exist_ok=True)
        pos, order, present = poscar_text(at, f"A-prime V5 {j['dir']} | src {st} sha {ssha[st][:16]}")
        files = {"POSCAR": pos, "INCAR": incar_text(j["dir"], encut, sigma, dz), "INCAR.r1": incar_text(j["dir"], encut, sigma, dz, rescue=True),
                 "KPOINTS": kpoints_text(kp), "POTCAR.spec": "\n".join(POTCAR_MAP[s] for s in present) + "\n"}
        for n, t in files.items():
            open(os.path.join(d, n), "w").write(t)
        g4t = g4.replace("G4_", "").rsplit("_", 1)[0] if g4 else ""
        role = {"scf": "표본 끝점", "g3": "G3 끝점 검사 (c+2)", "g4": f"G4 수치 검사 ({ {'e70': 'ENCUT 650', 'k1': 'k 4×3×1', 's05': 'SIGMA ½'}.get(g4t, g4t) })"}[j["kind"]]
        sym = at.get_chemical_symbols()
        jobs.append({"dir": j["dir"], "kind": j["kind"], "role": role, "structure": st, "structure_sha256": ssha[st], "nions": len(sym),
                     "composition": {s: sym.count(s) for s in present}, "nelect_expected": sum(ZVAL[s] for s in sym),
                     "potcar_titel_expected": [f"PAW_PBE {POTCAR_MAP[s]}" for s in present], "encut": encut, "sigma": sigma, "kpts": list(kp),
                     "dipol_z": round(dz, 6), "qe_dip": {"emaxpos": emx, "eopreg": eop}, "dip_min_clearance_A": clear,
                     "poscar_order_to_original_index": order, "area_A2": round(float(abs(at.cell.array[0][0] * at.cell.array[1][1] - at.cell.array[0][1] * at.cell.array[1][0])), 6),
                     "files_sha256": {n: _sha_text(t) for n, t in files.items()},
                     "d3_2body_eV_sdftd3": ((d3c[st] if st in d3c else d3c.setdefault(st, d3_2body_eV(at))) if want_d3 else None), "estimate": estimate(at, encut, kp),
                     "qe_job_pw_in_sha256": j.get("pw_in_sha256")})
    E = [x["estimate"] for x in jobs]
    est = {"nel_min": min(e["NELECT"] for e in E), "nel_max": max(e["NELECT"] for e in E), "nb_max": max(e["NBANDS_default"] for e in E),
           "npw_max": max(e["NPW_per_k"] for e in E), "wfc_max": max(e["wfc_GB_all_k"] for e in E)}
    open(os.path.join(out, "run_all.sh"), "w").write(RUN_ALL); os.chmod(os.path.join(out, "run_all.sh"), 0o755)
    open(os.path.join(out, "JOBS.txt"), "w").write("\n".join(x["dir"] for x in jobs) + "\n")
    meta = {"schema": "aprime_v5_vasp_package/v1", "date": "2026-09-27", "status": "준비본 (실행 미정 · Codex CE 리뷰 전 · 결정 proposed)",
            "source_package": pkg, "source_s3_manifest_sha256": qe["s3_manifest_sha256"], "source_seal": "db/properties/wad_aprime_s3v2_seal_2026_09_26.json",
            "card": "db/properties/wad_aprime_pilot_prereg_v5_2026_09_25.json", "amendment": "db/properties/wad_aprime_pilot_prereg_v5_amendment_3_vasp_v5_2026_09_27.json",
            "tool_sha256": _sha(os.path.abspath(__file__)), "settings": {"potcar": POTCAR_MAP, "zval": ZVAL, "encut": ENCUT_BASE, "encut_g4e": ENCUT_G4E, "sigma": SIGMA_BASE,
            "d3": D3_PARAMS, "perf_tags_allowed": PERF_TAGS, "rescue": RESCUE, "d3_rel_tol": D3_REL_TOL},
            "G5_samples": {k: list(v) for k, v in G5_SAMPLES.items()}, "G5_groups": {k: list(v) for k, v in G5_GROUPS.items()}, "estimate": est, "jobs": jobs}
    json.dump(meta, open(os.path.join(out, "jobs.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    lines = []
    for root, _, fs in os.walk(out):
        for f in sorted(fs):
            p = os.path.join(root, f); r = os.path.relpath(p, out)
            if r in ("MANIFEST.sha256", "README.md") or r.startswith("run/"):
                continue
            lines.append(f"{_sha(p)}  {r}")
    open(os.path.join(out, "MANIFEST.sha256"), "w").write("\n".join(sorted(lines, key=lambda s: s.split("  ", 1)[1])) + "\n")
    msha = _sha(os.path.join(out, "MANIFEST.sha256"))
    open(os.path.join(out, "README.md"), "w").write(_readme(jobs, est, msha))
    return meta, msha


# ───────────────────────── 반송 검사 ─────────────────────────
def parse_outcar(text):
    r = {"terminated": "General timing and accounting" in text,
         "converged": ("aborting loop because EDIFF is reached" in text) and ("EDIFF was not reached" not in text)}
    m = re.findall(r"free\s+energy\s+TOTEN\s*=\s*(-?\d+\.\d+)", text); r["TOTEN_eV"] = float(m[-1]) if m else None
    m = re.findall(r"energy\(sigma->0\)\s*=\s*(-?\d+\.\d+)", text); r["E_sigma0_eV"] = float(m[-1]) if m else None
    m = re.findall(r"Edisp\s*(?:\(eV\))?\s*[:=]\s*(-?\d+\.\d+)", text); r["Edisp_eV"] = float(m[-1]) if m else None
    m = re.search(r"NIONS\s*=\s*(\d+)", text); r["NIONS"] = int(m.group(1)) if m else None
    m = re.search(r"NELECT\s*=\s*(-?\d+\.?\d*)", text); r["NELECT"] = float(m.group(1)) if m else None
    m = re.search(r"^\s*(vasp\.\S+)", text, re.M); r["version"] = m.group(1) if m else None
    return r


def parse_titel(text):
    t = [" ".join(x.split()[:2]) for x in re.findall(r"TITEL\s*=\s*(.+)", text)]
    z = [float(x) for x in re.findall(r"ZVAL\s*=\s*(-?\d+\.?\d*)", text)]
    return t, z


def check_job(job, pkgdir, attdir, rescue=False):
    """한 시도 폴더 → 상태 dict. 상태는 문자열 하나 (OK 가 아니면 값은 판정에 안 쓴다)."""
    need = ("OUTCAR", "OSZICAR", "INCAR", "KPOINTS", "POSCAR")
    r = {"dir": os.path.basename(attdir), "rescue": rescue}
    if not os.path.isdir(attdir) or any(not os.path.isfile(os.path.join(attdir, f)) for f in need):
        r["status"] = "MISSING"; r["missing"] = [f for f in need if not os.path.isfile(os.path.join(attdir, f))]; return r
    for f in ("POSCAR", "KPOINTS"):
        if _sha(os.path.join(attdir, f)) != job["files_sha256"][f]:
            r["status"] = "INPUT_MODIFIED"; r["why"] = f; return r
    ours = parse_incar(open(os.path.join(pkgdir, "jobs", job["dir"], "INCAR.r1" if rescue else "INCAR")).read())
    ran = parse_incar(open(os.path.join(attdir, "INCAR")).read())
    extra = {k for k in ran if k not in ours and k not in PERF_TAGS}
    diff = {k for k in ours if ran.get(k) != ours[k]}
    if extra or diff:
        r["status"] = "INPUT_MODIFIED"; r["why"] = f"INCAR 태그 다름 {sorted(diff)} · 허용 밖 추가 {sorted(extra)}"; return r
    tp = os.path.join(attdir, "POTCAR.titel")
    if not os.path.isfile(tp):
        r["status"] = "POTCAR_UNVERIFIED"; return r
    t, z = parse_titel(open(tp).read())
    exp_z = [ZVAL[s] for s in job["composition"]]
    if t != job["potcar_titel_expected"] or [round(x, 3) for x in z] != [round(x, 3) for x in exp_z]:
        r["status"] = "POTCAR_MISMATCH"; r["why"] = f"TITEL {t} · ZVAL {z}"; return r
    o = parse_outcar(open(os.path.join(attdir, "OUTCAR"), errors="replace").read()); r.update(o)
    if not o["terminated"]:
        r["status"] = "NOT_TERMINATED"; return r
    if not o["converged"] or o["TOTEN_eV"] is None:
        r["status"] = "SCF_NOT_CONVERGED"; return r
    if o["NIONS"] != job["nions"] or (o["NELECT"] is not None and abs(o["NELECT"] - job["nelect_expected"]) > 1e-3):
        r["status"] = "SYSTEM_MISMATCH"; r["why"] = f"NIONS {o['NIONS']} · NELECT {o['NELECT']}"; return r
    if o["Edisp_eV"] is None:
        r["status"] = "D3_UNVERIFIED"; return r
    ref = job.get("d3_2body_eV_sdftd3")
    if ref is not None and abs(o["Edisp_eV"] - ref) > D3_REL_TOL * abs(ref):
        r["status"] = "D3_MISMATCH"; r["why"] = f"Edisp {o['Edisp_eV']:.4f} vs s-dftd3 2체 {ref:.4f} eV"; return r
    r["status"] = "OK"; return r


def check(out, ret):
    meta = json.load(open(os.path.join(out, "jobs.json"), encoding="utf-8"))
    run = os.path.join(ret, "run") if os.path.isdir(os.path.join(ret, "run")) else ret
    res = {}
    for job in meta["jobs"]:
        base = check_job(job, out, os.path.join(run, job["dir"]))
        if base["status"] != "OK" and os.path.isdir(os.path.join(run, job["dir"] + "_r1")):
            r1 = check_job(job, out, os.path.join(run, job["dir"] + "_r1"), rescue=True)
            res[job["dir"]] = {**r1, "first_attempt": base["status"]} if r1["status"] == "OK" else {**base, "r1": r1["status"]}
        else:
            res[job["dir"]] = base
    return meta, res


# ───────────────────────── 집계 ─────────────────────────
def collect(out, ret, uma=None):
    meta, res = check(out, ret)
    J = {j["dir"]: j for j in meta["jobs"]}
    ok = lambda n: res.get(n, {}).get("status") == "OK"
    def W(b, f, key="TOTEN_eV"):
        if not (ok(b) and ok(f)) or res[b].get(key) is None or res[f].get(key) is None:
            return None
        return (res[f][key] - res[b][key]) * EV_J / (J[b]["area_A2"] * A2_M2)
    smp = {}
    for k, (b, f) in G5_SAMPLES.items():
        smp[k] = {"bound": b, "far": f, "W_J_m2": W(b, f), "W_sigma0_J_m2": W(b, f, "E_sigma0_eV"), "dD3_J_m2": W(b, f, "Edisp_eV")}
        smp[k]["W_PBE_J_m2"] = (smp[k]["W_J_m2"] - smp[k]["dD3_J_m2"]) if (smp[k]["W_J_m2"] is not None and smp[k]["dD3_J_m2"] is not None) else None
    base = smp["①"]["W_J_m2"]
    Wi, Wii = W("V5_s_outer_A_G3_c2_bound", "V5_s_outer_A_G3_c2_far_i"), W("V5_s_outer_A_G3_c2_bound", "V5_s_outer_A_G3_c2_far_ii")
    g3 = {"W_i": Wi, "W_ii": Wii, "dW_i": (Wi - base) if (Wi is not None and base is not None) else None,
          "dW_ii": (Wii - base) if (Wii is not None and base is not None) else None, "threshold": G3_DW}
    g3["status"] = "INCOMPLETE" if (g3["dW_i"] is None or g3["dW_ii"] is None) else ("PASS" if max(abs(g3["dW_i"]), abs(g3["dW_ii"])) <= G3_DW else "FAIL")
    g4 = {}
    for tag, lab in (("e70", "ENCUT 650"), ("k1", "k 4×3×1"), ("s05", "SIGMA ½")):
        Wx = W(f"V5_s_outer_A_G4_{tag}_bound", f"V5_s_outer_A_G4_{tag}_far")
        dw = (Wx - base) if (Wx is not None and base is not None) else None
        g4[tag] = {"variant": lab, "W": Wx, "dW": dw, "status": "INCOMPLETE" if dw is None else ("PASS" if abs(dw) <= G4_DW else "FAIL")}
    st4 = {v["status"] for v in g4.values()}
    g4["status"] = "INCOMPLETE" if "INCOMPLETE" in st4 else ("FAIL" if "FAIL" in st4 else "PASS")
    rec = {"schema": "aprime_v5_vasp_collect/v1", "samples": smp, "G3": g3, "G4": g4, "jobs": res,
           "jobs_not_ok": sorted(n for n, v in res.items() if v["status"] != "OK"),
           "⛔": "VASP 비교군 — QE V2·V4 값과 빼거나 섞지 않는다"}
    if uma is not None:
        d = {}
        for k, s in smp.items():
            eb, ef = uma.get(s["bound"]), uma.get(s["far"])
            if eb is None or ef is None or s["W_J_m2"] is None or s["dD3_J_m2"] is None:
                d[k] = None; continue
            w_uma = (ef - eb) * EV_J / (J[s["bound"]]["area_A2"] * A2_M2)
            d[k] = s["W_J_m2"] - (w_uma + s["dD3_J_m2"])
        g5 = {"Delta_J_m2": d, "per_sample_max": G5_PER, "group_mean_max": G5_MEAN,
              "group_mean": {g: (sum(d[x] for x in m) / len(m) if all(d[x] is not None for x in m) else None) for g, m in G5_GROUPS.items()},
              "overall_mean_info": (sum(v for v in d.values()) / 5 if all(v is not None for v in d.values()) else None)}
        if any(v is None for v in d.values()):
            g5["status"] = "INCOMPLETE (분모 5 고정 · 교체 금지)"
        elif any(abs(v) > G5_PER for v in d.values()) or any(abs(m) > G5_MEAN for m in g5["group_mean"].values()):
            g5["status"] = "FAIL"
        elif g3["status"] != "PASS" or g4["status"] != "PASS":
            g5["status"] = f"INCOMPLETE (G3 {g3['status']} · G4 {g4['status']} — 오차표만)"
        else:
            g5["status"] = "PASS"
        rec["G5"] = g5
    return rec


# ───────────────────────── selftest ─────────────────────────
def _fake_outcar(E, Ed, nions, nelect, conv=True, term=True, edisp_line=True):
    t = [" vasp.6.4.2 20Jul23 (build Nov  1 2023) complex", f"   number of dos      NEDOS =    301   number of ions     NIONS = {nions:6d}",
         f"   NELECT = {nelect:12.4f}    total number of electrons"]
    if edisp_line:
        t.append(f"  Edisp (eV):  {Ed:12.5f}")
    t.append(" ------------------------ aborting loop because EDIFF is reached ----------------------------------------" if conv
             else " ------------------------ aborting loop EDIFF was not reached (unconverged)  ----------------------------")
    t += [f"  free  energy   TOTEN  =  {E:18.8f} eV", f"  energy  without entropy=  {E + 0.01:18.8f}  energy(sigma->0) =  {E + 0.005:18.8f}"]
    if term:
        t.append(" General timing and accounting informations for this job:")
    return "\n".join(t) + "\n"


def _selftest():
    import tempfile
    import numpy as np
    from ase import Atoms
    from ase.io import write
    ok = bad = 0
    def ck(c, m):
        nonlocal ok, bad
        if c:
            ok += 1
        else:
            bad += 1; print("  ✗", m)
    # ① POSCAR 종 묶기 · 대응표 되돌리기
    at = Atoms("AgLiSAgClP", positions=[[0, 0, 1], [1, 0, 5], [2, 0, 6], [0, 1, 2], [3, 0, 7], [4, 0, 8]], cell=[10, 10, 30], pbc=True)
    txt, order, present = poscar_text(at, "t")
    sp, nn, cell, pos = parse_poscar_cart(txt)
    ck(sp == ["Li", "P", "S", "Cl", "Ag"] and nn == [1, 1, 1, 1, 2] and present == sp, f"POSCAR 종 순서 Li P S Cl Ag · 개수 — {sp} {nn}")
    ck(all(np.allclose(pos[k], at.positions[order[k]]) for k in range(len(order))), "POSCAR 좌표 ↔ 원래 번호 대응표가 되돌려진다")
    try:
        poscar_text(Atoms("Fe", positions=[[0, 0, 0]], cell=[5, 5, 5]), "x"); ck(False, "⛔음성 모르는 원소 Fe 를 받아들였다")
    except PkgError:
        ck(True, "")
    # ② DIPOL = 중심 − ½ · 여유 검사
    ck(abs(dipol_z(0.85963, 0.03119) - 0.375225) < 1e-6 and abs(dipol_z(0.2, 0.02) - 0.71) < 1e-9, f"DIPOL_z = (emaxpos + eopreg/2 − ½) mod 1 — {dipol_z(0.85963, 0.03119)}")
    sl = Atoms("Ag2", positions=[[0, 0, 5.0], [0, 0, 22.0]], cell=[10, 10, 32.058], pbc=True)
    ck(abs(check_dip_clear(sl, 0.85963, 0.03119) - (27.558 - 22.0)) < 1e-2, f"쌍극자 구간 여유 = min(아래 가장자리 − 최고 원자, 바닥 영상 − 위 가장자리) — {check_dip_clear(sl, 0.85963, 0.03119)}")
    sl2 = Atoms("Ag2", positions=[[0, 0, 1.0], [0, 0, 20.0]], cell=[10, 10, 32.058], pbc=True)
    ck(abs(check_dip_clear(sl2, 0.85963, 0.03119) - (1.0 + 32.058 - 28.558)) < 1e-2, "여유를 기판 바닥의 위쪽 주기 영상이 정할 때도 잰다 (4.5 Å)")
    for zbad, why in ((26.0, "위쪽 원자가 구간 1.6 Å 앞"), (-1.0 + 32.058 * 0.0 + 30.0 - 32.058 + 32.058 * 0 + 0.1, "바닥 영상")):
        try:
            check_dip_clear(Atoms("Ag2", positions=[[0, 0, 1.0], [0, 0, zbad]], cell=[10, 10, 32.058], pbc=True), 0.85963, 0.03119)
            ck(False, f"⛔음성 쌍극자 여유 부족({why})을 통과시켰다")
        except PkgError:
            ck(True, "")
    try:
        check_dip_clear(Atoms("Ag2", positions=[[0, 0, 32.058 - 1.5], [0, 0, 10.0]], cell=[10, 10, 32.058], pbc=True), 0.85963, 0.03119)
        ck(False, "⛔음성 기판 바닥의 위쪽 영상이 구간 쪽 여유 부족인데 통과")
    except PkgError:
        ck(True, "")
    # ③ INCAR 변형 · 재시도 · 파서
    i0, ir = parse_incar(incar_text("x", 520, 0.136, 0.3752)), parse_incar(incar_text("x", 650, 0.068, 0.3752, rescue=True))
    ck(i0["ENCUT"] == "520.0" and i0["SIGMA"] == "0.1360" and i0["IVDW"] == "12" and i0["VDW_A2"] == "4.4407" and i0["DIPOL"] == "0.5 0.5 0.375200"
       and i0["LREAL"] == ".FALSE." and "AMIX" not in i0, "INCAR 기본: ENCUT 520 · SIGMA 0.136 · IVDW 12 · BJ 계수 · DIPOL · LREAL F · 혼합 태그 없음")
    ck(ir["ENCUT"] == "650.0" and ir["SIGMA"] == "0.0680" and ir["AMIX"] == "0.1" and ir["BMIX"] == "0.01" and ir["NELM"] == "300", "INCAR 변형 · 재시도(r1) 태그")
    ck(kpoints_text((4, 3, 1)).splitlines()[2:4] == ["Gamma", "4 3 1"], "KPOINTS Γ 4×3×1")
    # ④ 반송 검사 (가짜 패키지 1 잡 + 가짜 OUTCAR)
    with tempfile.TemporaryDirectory() as T:
        out, ret = os.path.join(T, "pkg"), os.path.join(T, "ret", "run")
        atv = Atoms("Li2SAg2", positions=[[0, 0, 5], [1, 1, 6], [2, 2, 7], [0, 0, 1], [3, 3, 2]], cell=[10, 10, 30], pbc=True)
        pos, order, present = poscar_text(atv, "v")
        jd = os.path.join(out, "jobs", "J1"); os.makedirs(jd)
        files = {"POSCAR": pos, "INCAR": incar_text("J1", 520, 0.136, 0.3), "INCAR.r1": incar_text("J1", 520, 0.136, 0.3, True), "KPOINTS": kpoints_text((3, 2, 1))}
        for n, t in files.items():
            open(os.path.join(jd, n), "w").write(t)
        comp = {s: atv.get_chemical_symbols().count(s) for s in present}
        job = {"dir": "J1", "nions": 5, "composition": comp, "nelect_expected": 2 * 3 + 6 + 2 * 11, "potcar_titel_expected": [f"PAW_PBE {POTCAR_MAP[s]}" for s in present],
               "files_sha256": {n: _sha_text(t) for n, t in files.items()}, "d3_2body_eV_sdftd3": -10.0, "area_A2": 100.0}
        def mk(att="J1", outcar=None, incar=None, titel=None, drop=None):
            d = os.path.join(ret, att); os.makedirs(d, exist_ok=True)
            for n in ("POSCAR", "KPOINTS"):
                open(os.path.join(d, n), "w").write(files[n])
            open(os.path.join(d, "INCAR"), "w").write(incar if incar is not None else files["INCAR"] + "NCORE = 16\nKPAR = 2\n")
            open(os.path.join(d, "OSZICAR"), "w").write("DAV:   1  ...\n")
            open(os.path.join(d, "OUTCAR"), "w").write(outcar if outcar is not None else _fake_outcar(-100.0, -10.02, 5, 34.0))
            open(os.path.join(d, "POTCAR.titel"), "w").write(titel if titel is not None else
                 "".join(f"   VRHFIN =x\n   TITEL  = PAW_PBE {POTCAR_MAP[s]} 10Sep2004\n   POMASS = 1; ZVAL   = {ZVAL[s]:8.3f}    mass and valenz\n" for s in present))
            if drop:
                os.remove(os.path.join(d, drop))
            return d
        d = mk(); r = check_job(job, out, d)
        ck(r["status"] == "OK" and abs(r["TOTEN_eV"] + 100.0) < 1e-9 and abs(r["Edisp_eV"] + 10.02) < 1e-9 and abs(r["E_sigma0_eV"] + 99.995) < 1e-9,
           f"반송 OK (성능 태그 NCORE·KPAR 허용) · TOTEN · Edisp · E(σ→0) — {r.get('status')} {r.get('why')}")
        cases = [("MISSING", dict(drop="OUTCAR")), ("INPUT_MODIFIED", dict(incar=files["INCAR"].replace("ENCUT = 520.0", "ENCUT = 400.0"))),
                 ("INPUT_MODIFIED", dict(incar=files["INCAR"] + "ALGO = Fast\nISMEAR = 0\n")), ("POTCAR_MISMATCH", dict(titel="   TITEL  = PAW_PBE Li 17Jan2003\n   ZVAL   =    1.000\n")),
                 ("POTCAR_UNVERIFIED", dict(drop="POTCAR.titel")), ("NOT_TERMINATED", dict(outcar=_fake_outcar(-100, -10.02, 5, 34.0, term=False))),
                 ("SCF_NOT_CONVERGED", dict(outcar=_fake_outcar(-100, -10.02, 5, 34.0, conv=False))), ("SYSTEM_MISMATCH", dict(outcar=_fake_outcar(-100, -10.02, 6, 34.0))),
                 ("SYSTEM_MISMATCH", dict(outcar=_fake_outcar(-100, -10.02, 5, 35.0))), ("D3_UNVERIFIED", dict(outcar=_fake_outcar(-100, -10.02, 5, 34.0, edisp_line=False))),
                 ("D3_MISMATCH", dict(outcar=_fake_outcar(-100, -10.8, 5, 34.0)))]
        for want, kw in cases:
            import shutil
            shutil.rmtree(os.path.join(ret, "J1"), ignore_errors=True)
            r = check_job(job, out, mk(**kw))
            ck(r["status"] == want, f"⛔음성 {want} 을 못 잡았다 — {r['status']} {r.get('why', '')}")
        # KPOINTS/POSCAR 변조
        shutil.rmtree(os.path.join(ret, "J1"), ignore_errors=True); d = mk(); open(os.path.join(d, "KPOINTS"), "w").write(kpoints_text((2, 2, 1)))
        ck(check_job(job, out, d)["status"] == "INPUT_MODIFIED", "⛔음성 KPOINTS 변조 → INPUT_MODIFIED")
        # 재시도 선택: 첫 시도 미수렴 · r1 OK → r1 채택 · 첫 상태 보존
        meta = {"jobs": [job]}; json.dump(meta, open(os.path.join(out, "jobs.json"), "w"))
        shutil.rmtree(os.path.join(ret, "J1"), ignore_errors=True)
        mk(outcar=_fake_outcar(-100, -10.02, 5, 34.0, conv=False)); mk("J1_r1", incar=files["INCAR.r1"])
        _, res = check(out, os.path.dirname(ret))
        ck(res["J1"]["status"] == "OK" and res["J1"]["rescue"] and res["J1"]["first_attempt"] == "SCF_NOT_CONVERGED", f"재시도 r1 채택 · 첫 시도 상태 보존 — {res['J1']}")
        shutil.rmtree(os.path.join(ret, "J1_r1")); mk("J1_r1", incar=files["INCAR"])     # r1 폴더에 r1 이 아닌 INCAR
        _, res = check(out, os.path.dirname(ret))
        ck(res["J1"]["status"] == "SCF_NOT_CONVERGED" and res["J1"]["r1"] == "INPUT_MODIFIED", "⛔음성 r1 폴더가 사전등록 INCAR.r1 이 아니면 채택 안 함")
    # ⑤ 집계 — 가짜 18 잡으로 W · G3 · G4 · G5
    with tempfile.TemporaryDirectory() as T:
        out, ret = os.path.join(T, "pkg"), os.path.join(T, "ret", "run")
        names = sorted({n for v in G5_SAMPLES.values() for n in v} | {f"V5_s_outer_A_G3_c2_{x}" for x in ("bound", "far_i", "far_ii")}
                       | {f"V5_s_outer_A_G4_{t}_{e}" for t in ("e70", "k1", "s05") for e in ("bound", "far")})
        A = 202.2; dE = lambda Wv: Wv * A * A2_M2 / EV_J
        E = {n: -1000.0 for n in names}; Ed = {n: -30.0 for n in names}
        for k, (b, f) in G5_SAMPLES.items():
            E[f] = E[b] + dE(0.50 if k != "③" else 0.60); Ed[f] = Ed[b] + dE(0.55)
        E["V5_s_outer_A_far"] = E["V5_s_outer_A_bound"] + dE(0.50)
        E["V5_s_outer_A_p05_bound"] = E["V5_s_outer_A_far"] - dE(0.45)
        for x, w in (("far_i", 0.505), ("far_ii", 0.509)):
            E[f"V5_s_outer_A_G3_c2_{x}"] = E["V5_s_outer_A_G3_c2_bound"] + dE(w)
        for t, w in (("e70", 0.51), ("k1", 0.49), ("s05", 0.50)):
            E[f"V5_s_outer_A_G4_{t}_far"] = E[f"V5_s_outer_A_G4_{t}_bound"] + dE(w)
        at = Atoms("Li", positions=[[0, 0, 5]], cell=[10.055, 20.11, 32.0], pbc=True); present = ["Li"]
        pos, _, _ = poscar_text(at, "v"); jobs = []
        for n in names:
            jd = os.path.join(out, "jobs", n); os.makedirs(jd)
            files = {"POSCAR": pos, "INCAR": incar_text(n, 520, 0.136, 0.3), "INCAR.r1": incar_text(n, 520, 0.136, 0.3, True), "KPOINTS": kpoints_text((3, 2, 1))}
            for fn, t in files.items():
                open(os.path.join(jd, fn), "w").write(t)
            jobs.append({"dir": n, "nions": 1, "composition": {"Li": 1}, "nelect_expected": 3.0, "potcar_titel_expected": ["PAW_PBE Li_sv"],
                         "files_sha256": {fn: _sha_text(t) for fn, t in files.items()}, "d3_2body_eV_sdftd3": Ed[n], "area_A2": A})
            d = os.path.join(ret, n); os.makedirs(d)
            for fn in ("POSCAR", "KPOINTS", "INCAR"):
                open(os.path.join(d, fn), "w").write(files[fn])
            open(os.path.join(d, "OSZICAR"), "w").write("DAV: 1\n"); open(os.path.join(d, "OUTCAR"), "w").write(_fake_outcar(E[n], Ed[n], 1, 3.0))
            open(os.path.join(d, "POTCAR.titel"), "w").write("   TITEL  = PAW_PBE Li_sv 10Sep2004\n   ZVAL   =    3.000\n")
        json.dump({"jobs": jobs}, open(os.path.join(out, "jobs.json"), "w"))
        uma = {n: 0.0 for n in names}                                     # Δ_i = W − (W_UMA + ΔD3) · ΔD3 = 0.55 설계
        uma["V5_s_outer_A_far"] = dE(-0.06)    # ① Δ = 0.50 − 0.49 = +0.01 · ⑤ (① 의 far 공유) Δ = 0.45 − 0.49 = −0.04
        uma["V5_s_outer_B_far"] = dE(-0.06)    # ② +0.01
        uma["V5_li_outer_A_far"] = dE(0.03)    # ③ W 0.60 → +0.02
        uma["V5_li_outer_B_far"] = dE(-0.06)   # ④ +0.01  → 군 평균 S −0.0067 · Li +0.015
        rc = collect(out, os.path.dirname(ret), uma)
        s1 = rc["samples"]["①"]
        ck(abs(s1["W_J_m2"] - 0.50) < 1e-6 and abs(s1["dD3_J_m2"] - 0.55) < 1e-6 and abs(s1["W_PBE_J_m2"] + 0.05) < 1e-6, f"W = ΔF/A · ΔD3 · W_PBE = W − ΔD3 — {s1}")
        ck(abs(rc["samples"]["⑤"]["W_J_m2"] - 0.45) < 1e-6, "표본 ⑤ 는 ① 의 far 를 쓴다")
        ck(rc["G3"]["status"] == "PASS" and abs(rc["G3"]["dW_ii"] - 0.009) < 1e-6, f"G3 PASS (ΔW 0.005·0.009 ≤ 0.01) — {rc['G3']['status']}")
        ck(rc["G4"]["status"] == "PASS", f"G4 PASS — {rc['G4']['status']}")
        ck(rc["G5"]["status"] == "PASS" and abs(rc["G5"]["Delta_J_m2"]["①"] - 0.01) < 1e-6 and abs(rc["G5"]["Delta_J_m2"]["⑤"] + 0.04) < 1e-6
           and abs(rc["G5"]["group_mean"]["s_outer"] + 0.02 / 3) < 1e-6, f"G5: Δ = W − (W_UMA + ΔD3) · 군 평균 · PASS — {rc['G5']['status']} {rc['G5']['Delta_J_m2']}")
        uma_g = dict(uma); uma_g["V5_s_outer_B_far"] = dE(-0.06 + 0.09); uma_g["V5_s_outer_A_far"] = dE(-0.06 + 0.09)   # S 군 Δ ①② −0.08 · ⑤ −0.13
        ck(collect(out, os.path.dirname(ret), uma_g)["G5"]["status"] == "FAIL", "⛔음성 표본 ⑤ |Δ| 0.13 → FAIL (군 평균만이 아니라 표본마다도 본다)")
        uma_m = dict(uma); uma_m["V5_s_outer_A_far"] = dE(-0.06 + 0.07); uma_m["V5_s_outer_B_far"] = dE(-0.06 + 0.07)   # ① −0.06 · ② −0.06 · ⑤ −0.11? → 조정
        uma_m["V5_s_outer_A_far"] = dE(-0.06 + 0.055); uma_m["V5_s_outer_B_far"] = dE(-0.06 + 0.07)                        # ① −0.045 · ② −0.06 · ⑤ −0.095 → 군 평균 −0.067
        rm = collect(out, os.path.dirname(ret), uma_m)["G5"]
        ck(rm["status"] == "FAIL" and all(abs(v) <= 0.10 for v in rm["Delta_J_m2"].values()) and abs(rm["group_mean"]["s_outer"]) > 0.05,
           f"⛔음성 표본마다는 통과 · S 군 평균 |−0.067| > 0.05 → FAIL — {rm['status']} {rm['group_mean']}")
        # ⛔ 음성: G3 far_ii +0.012 → G3 FAIL → G5 는 PASS 가 아니다 (오차표만)
        open(os.path.join(ret, "V5_s_outer_A_G3_c2_far_ii", "OUTCAR"), "w").write(_fake_outcar(E["V5_s_outer_A_G3_c2_bound"] + dE(0.512), Ed["V5_s_outer_A_G3_c2_far_ii"], 1, 3.0))
        rc2 = collect(out, os.path.dirname(ret), uma)
        ck(rc2["G3"]["status"] == "FAIL" and rc2["G5"]["status"].startswith("INCOMPLETE (G3 FAIL"), f"⛔음성 G3 FAIL → G5 PASS 아님 — {rc2['G5']['status']}")
        open(os.path.join(ret, "V5_s_outer_A_G3_c2_far_ii", "OUTCAR"), "w").write(_fake_outcar(E["V5_s_outer_A_G3_c2_far_ii"], Ed["V5_s_outer_A_G3_c2_far_ii"], 1, 3.0))
        # ⛔ 음성: 표본 ③ 의 Δ 를 키움 → FAIL
        uma3 = dict(uma); uma3["V5_li_outer_A_far"] = dE(-0.12)            # ③ Δ = 0.60 − 0.43 = 0.17
        ck(collect(out, os.path.dirname(ret), uma3)["G5"]["status"] == "FAIL", "⛔음성 표본 ③ |Δ| 0.17 > 0.10 → G5 FAIL")
        # ⛔ 음성: 표본 ② bound 누락 → INCOMPLETE (분모 5 고정)
        os.remove(os.path.join(ret, "V5_s_outer_B_bound", "OUTCAR"))
        rc4 = collect(out, os.path.dirname(ret), uma)
        ck(rc4["G5"]["status"].startswith("INCOMPLETE (분모 5") and rc4["samples"]["②"]["W_J_m2"] is None, f"⛔음성 표본 누락 → INCOMPLETE · W None — {rc4['G5']['status']}")
    print(f"{'✅' if not bad else '⛔'} build_v5_vasp_package selftest {ok}/{ok + bad}")
    return 0 if not bad else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--build", action="store_true"); ap.add_argument("--check", action="store_true"); ap.add_argument("--collect", action="store_true")
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--pkg", default="db/inputs/wad_aprime_s3v2_2026_09_26")
    ap.add_argument("--out"); ap.add_argument("--ret"); ap.add_argument("--uma"); ap.add_argument("--json"); ap.add_argument("--no_d3", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if a.build:
        meta, msha = build(a.pkg, a.out, want_d3=not a.no_d3)
        print(f"✅ {len(meta['jobs'])} 잡 → {a.out} · MANIFEST.sha256 sha256 {msha}")
        print(f"   규모: {meta['estimate']}")
        return 0
    if a.check or a.collect:
        if a.collect:
            uma = None
            if a.uma:
                u = json.load(open(a.uma, encoding="utf-8")); uma = {k.split("/")[-1].replace(".extxyz", ""): v["E_UMA_eV"] for k, v in u.get("energies", {}).items()}
            rec = collect(a.out, a.ret, uma)
            for k, s in rec["samples"].items():
                print(f"  {k} W {s['W_J_m2']} · W_PBE {s['W_PBE_J_m2']} · ΔD3 {s['dD3_J_m2']}")
            print(f"  G3 {rec['G3']['status']} · G4 {rec['G4']['status']}{' · G5 ' + rec['G5']['status'] if 'G5' in rec else ''} · 미완 {rec['jobs_not_ok']}")
            if a.json:
                json.dump(rec, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        else:
            _, res = check(a.out, a.ret)
            for n, r in res.items():
                print(f"  {n:34s} {r['status']}{(' · ' + str(r.get('why'))) if r.get('why') else ''}")
        return 0
    ap.error("--build · --check · --collect · --selftest 중 하나")


if __name__ == "__main__":
    sys.exit(main())
