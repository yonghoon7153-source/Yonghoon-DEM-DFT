#!/usr/bin/env python3
"""package_lpsocl.py — LPSOCl(Li27P5S21OCl8, O-doped LPSCl1.6) 전 데이터를 논문 폴더 구조로 묶는다.

폴더 규약은 사용자의 **B2O3 논문 폴더**를 그대로 따른다:
  1-1. bvse / 1-2. 이온전도도 / 1-3. voronoi
  2-1. DOS, PDOS / 2-2. 산화안정성 (w. Li, LPSCl interface)
  3-1. bond length / 3-2. bader / 3-3. elf / 3-4. ICOHP
  99. extra

⚠ **없는 축은 빈 폴더 + MISSING.md 로 남긴다.** 채워 넣거나 조용히 빼지 않는다 —
   B2O3 에는 있고 LPSOCl 에는 없는 축이 무엇인지가 그 자체로 정보다(다음 계산 목록).

실행:  python3 tools/package_lpsocl.py [--out DIR] [--zip]
"""
import argparse
import csv
import json
import os
import shutil
import zipfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB, DOCS, TOOLS = ROOT / "db", ROOT / "docs", ROOT / "tools"

# (폴더, [(원본 상대경로, 설명)], 없을 때 사유)
LAYOUT = [
    ("1-1. bvse", [
        ("db/properties/bvse_3system_channel_origin.csv",
         "3계(undoped LPSCl1.6 / +O(LPSOCl) / +B2O3) 채널% vs iso 레벨. **Origin-ready**"),
        ("db/properties/bvse_channel_volume.csv", "채널 부피"),
        ("db/properties/bvse_cubic_approx/bvse_orig_vs_cubic.csv",
         "원본 주기셀 vs 큐빅 근사 비교 — **정량·순위는 orig 만 인용**"),
        ("db/properties/bvse_cubic_approx/bvse_orig_vs_cubic.json", "동 JSON"),
        ("db/properties/bvse_cubic_approx/box_variance_16origins.json",
         "큐빅 박스 원점 16개 표본 편차 (±1.3%p)"),
    ], None),

    ("1-2. 이온전도도", [
        ("db/properties/lpsocl_md_arrhenius.json", "UMA-MD Arrhenius (600/800/1000 K, 멀티시드)"),
        ("db/properties/lpsocl_arrhenius_origin.csv", "**Origin-ready** Arrhenius"),
        ("docs/figures/lpsocl/lpsocl_arrhenius.png", "Arrhenius 그림"),
        ("tools/ionic/fig_lpsocl_arrhenius.py", "그림 생성 스크립트"),
        ("tools/ionic/run_lpsocl_md.sh", "MD 실행 스크립트"),
    ], None),

    ("1-3. voronoi", [], "LPSOCl voronoi 미계산. B2O3 만 있음(b2o3_voronoi_disorder.csv)."),

    ("2-1. DOS, PDOS", [
        ("db/properties/lpsocl_dos_gap.json", "band gap — **fixed-occupations nscf VBM/CBM**"),
        ("db/properties/lpsocl_dos_smooth.csv", "**Origin-ready** total DOS"),
        ("db/properties/lpsocl_pdos_element_smooth.csv", "**Origin-ready** 원소별 PDOS"),
        ("db/properties/lpsocl_pdos_element_PERATOM.csv", "**Origin-ready** 원소별 PDOS (원자당 정규화)"),
        ("tools/electronic/standard_dos/lpsocl/build_lpsocl_v0_dos.py", "DOS 빌드"),
        ("tools/electronic/standard_dos/lpsocl/fig_lpsocl_dos.py", "DOS 그림"),
    ], None),

    ("2-2. 산화안정성 (w. Li, LPSCl interface)", [
        ("db/properties/lpsocl_interface.json", "계면 반응성 (grand-potential ESW / pseudo-binary)"),
        ("tools/oxidation/run_lpsocl_interface.sh", "실행 스크립트"),
    ], None),

    ("3-1. bond length", [], "LPSOCl 전용 bond length 파일 없음. "
     "단 thermal_thprime.json 의 `bondswap_extension/_bond_counts/lpsocl_62at` 에 결합 수가 있어 "
     "99. extra 에 넣었다. B2O3 는 b2o3_bond_lengths(_full).json 로 전용 파일 보유."),

    ("3-2. bader", [], "LPSOCl Bader 미계산. bader_b2o3_vs_lpscl16.csv 는 **B2O3 vs LPSCl1.6** 이라 "
     "LPSOCl(+O) 이 아니다 — 넣지 않는다."),

    ("3-3. elf", [], "LPSOCl ELF 미계산. b2o3_elf_bonds.csv / modelc_elf_bonds.csv 만 있음. "
     "실행 스크립트는 준비돼 있다(99. extra 의 run_lpsocl_elf_gabia.sh)."),

    ("3-4. ICOHP", [
        ("db/properties/lpsocl_icohp.json", "ICOHP (LOBSTER)"),
    ], None),

    ("99. extra", [
        # 구조
        ("db/structures/lpsocl_v0.xyz", "V0 구조 (xyz)"),
        ("db/structures/lpsocl_v0.vasp", "V0 구조 (POSCAR — VESTA Boundary 타일링용)"),
        ("db/structures/lpsocl_v0.vesta", "VESTA 세션 (**ASCII+CRLF 규약**)"),
        ("db/structures/lpsocl_relaxV0.xyz", "relax 후 V0"),
        ("db/structures/lpsocl_cubic_approx.vasp", "큐빅 근사 (표시용 — 정량 인용 금지)"),
        # EOS
        ("db/properties/lpsocl_eos_dft_result.json", "EOS DFT 결과"),
        ("db/properties/lpsocl_eos_fit.csv", "EOS 피팅"),
        ("db/properties/lpsocl_eos_origin.csv", "**Origin-ready** EOS"),
        # 실행 스크립트
        ("scripts/doping/prepare_dft_eos_lpsocl.py", "EOS 준비"),
        ("scripts/doping/sbatch_dft_eos_lpsocl_chain.sh", "KISTI EOS 체인"),
        ("scripts/doping/submit_lpsocl_chain.sh", "제출"),
        ("scripts/doping/watch_lpsocl_eos.sh", "watch"),
        ("tools/elastic/run_lpsocl_suite_gabia.sh", "탄성 스위트"),
        ("tools/electronic/run_lpsocl_elf_gabia.sh", "ELF 실행 (**미실행**)"),
        ("tools/electronic/setup_lpsocl_eps_ibb.sh", "유전율 셋업"),
    ], None),
]

# 후보 구조는 별도 하위 폴더로
CANDIDATE_DIR = "99. extra/lpsocl_candidates"


def canonical_block():
    """다른 파일에 흩어져 있는 LPSOCl 값을 한 장으로. **인용 규율 포함.**"""
    out = {"composition": "Li27P5S21OCl8 (O-doped LPSCl1.6, 62 atoms)",
           "label": "LPSOCl", "packaged": str(date.today())}
    try:
        out["band_gap_eV"] = json.load(open(DB / "properties" / "lpsocl_dos_gap.json"))
    except Exception:
        pass
    for f, key in (("phonon_stability_sweep.json", "phonon"),
                   ("thermal_thprime.json", "thermal_thprime")):
        try:
            d = json.load(open(DB / "properties" / f))
            hits = {}

            def walk(o, p=""):
                if isinstance(o, dict):
                    for k, v in o.items():
                        if "lpsocl" in str(k).lower():
                            hits[p + "/" + str(k)] = v
                        else:
                            walk(v, p + "/" + str(k))
                elif isinstance(o, list):
                    for i, v in enumerate(o[:50]):
                        walk(v, p + f"[{i}]")
            walk(d)
            if hits:
                out[key] = hits
        except Exception:
            pass
    try:
        el = json.load(open(DB / "properties" / "elastic.json"))
        s = json.dumps(el, ensure_ascii=False)
        i = s.lower().find("lpsocl_v0")
        if i > 0:
            out["elastic_entry_excerpt"] = s[max(0, i - 200):i + 900]
    except Exception:
        pass
    return out


DISCIPLINE = """# ⚠ 인용 규율 (이 폴더 전체에 적용)

이 데이터는 **Yonghoon-DEM-DFT** repo 에서 자동 추출한 것이다. 원본이 정본이고 이 사본은 스냅샷이다.

## 반드시 지킬 것

1. **Band gap** — fixed-occupations nscf 의 VBM/CBM 고유값만 인정한다. **DOS 임계 판독 금지**(~0.3 eV 과소).
   Canonical: comp1 2.066 / modelc(LPSCl1.6) 2.099 / +B2O3 1.9671 / **LPSOCl 2.2309 eV**.

2. **BVSE** — 정량·순위는 **원본 주기셀(orig) 값만** 인용한다.
   큐빅 근사는 **표시용**이고 원점 16개 표본에서 ±1.3%p 편차가 있다.

3. **MLIP-MD (UMA)** — **σ 절대값 인용 금지.** 비율도 멀티시드 판정만.
   Ea 오차막대는 600 K 3-시드 기준.
   ⚠ 2026-07-28 갱신: 규율의 근거가 재정의됐다 — "MLIP 절대값은 (a) 훈련 functional 이 그 계에 맞고
   (b) 같은 물질군 실험 검증을 거친 경우에만" 신뢰 가능하고, 우리 UMA 는 둘 다 미충족이다.
   (근거: kim2024 = functional 에 따라 σ 8배 / lee2024 ESI Table S1 = optB88-MTP 는 실험과 맞고
   **AIMD 가 840배 틀림**)

4. **평균류 지표**는 그림 표시 창과 **같은 창**(−8..0 eV)에서 계산·인용한다.

5. **VESTA** — .vesta 는 ASCII 전용 + CRLF (em-dash 등 비ASCII 가 IMPORT_DENSITY 파싱을 깨뜨린 사례).
   구조는 xyz + POSCAR(.vasp) 페어로 본다 (xyz 는 격자가 없어 Boundary 타일링 불가).

## 비어 있는 폴더

`MISSING.md` 가 있는 폴더는 **아직 계산하지 않은 축**이다. 조용히 빼지 않고 남겨둔 것이며,
그 목록이 곧 다음 계산 후보다.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path.home() / "lpsocl_package"))
    ap.add_argument("--zip", action="store_true")
    a = ap.parse_args()

    out = Path(a.out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    manifest, missing = [], []
    for folder, items, absent in LAYOUT:
        d = out / folder
        d.mkdir(parents=True, exist_ok=True)
        n = 0
        for rel, desc in items:
            src = ROOT / rel
            if not src.exists():
                manifest.append({"folder": folder, "file": rel, "status": "SOURCE_MISSING",
                                 "desc": desc})
                continue
            shutil.copy2(src, d / src.name)
            manifest.append({"folder": folder, "file": src.name, "src": rel,
                             "status": "ok", "desc": desc})
            n += 1
        if absent:
            (d / "MISSING.md").write_text(
                f"# {folder} — 데이터 없음\n\n{absent}\n\n"
                "⚠ 조용히 빼지 않고 폴더를 남겼다. **이 목록이 다음 계산 후보다.**\n",
                encoding="utf-8")
            missing.append((folder, absent))
        print(f"  {folder:42s} {n}개" + ("   ⟵ MISSING" if absent else ""))

    # 후보 구조 묶음
    cand = ROOT / "db" / "structures" / "lpsocl_candidates"
    if cand.exists():
        cd = out / CANDIDATE_DIR
        cd.mkdir(parents=True, exist_ok=True)
        k = 0
        for f in sorted(cand.iterdir()):
            if f.is_file():
                shutil.copy2(f, cd / f.name)
                k += 1
        print(f"  {CANDIDATE_DIR:42s} {k}개")

    (out / "00_인용규율_READ_FIRST.md").write_text(DISCIPLINE, encoding="utf-8")
    (out / "00_canonical_values.json").write_text(
        json.dumps(canonical_block(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with open(out / "00_manifest.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["folder", "file", "src", "status", "desc"])
        w.writeheader()
        w.writerows(manifest)

    print(f"\n→ {out}")
    if missing:
        print(f"\n⚠ 비어 있는 축 {len(missing)}개 (다음 계산 후보):")
        for f, why in missing:
            print(f"   · {f} — {why.splitlines()[0][:80]}")

    if a.zip:
        z = str(out) + ".zip"
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
            for p in out.rglob("*"):
                if p.is_file():
                    zf.write(p, p.relative_to(out.parent))
        print(f"\n→ {z}  ({os.path.getsize(z)/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
