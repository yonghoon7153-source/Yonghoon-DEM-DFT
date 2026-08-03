#!/usr/bin/env bash
# =============================================================================
# gabia_july_evidence.sh — 2026-07 서버 사용 데이터 결과지 (증빙용)
#
# 용도설명서 4트랙에 대응하는 **실제 산출 수치**를 db 에서 읽어 터미널에 찍는다.
# 전월 증빙(5.pdf)과 같은 양식: `====` 제목 배너 + `▶` 소제목 + 실측 출력.
#
#   cd ~/Yonghoon-DEM-DFT && bash tools/reports/gabia_july_evidence.sh
#   (한 섹션씩 캡처하려면)  bash tools/reports/gabia_july_evidence.sh 1
#
# ⚠ 값을 여기에 하드코딩하지 않는다 — db 파일에서 읽는다. 파일이 없으면 그 줄만
#   건너뛰고 무엇이 없는지 알린다(없는 값을 있는 척 찍지 않기 위해).
# =============================================================================
set -u
cd "$(dirname "$0")/../.." || exit 1
ONLY=${1:-0}
PY=${PY:-python3}
bar(){ printf '%s\n' "=============================================================="; }
sec(){ [ "$ONLY" = 0 ] || [ "$ONLY" = "$1" ] || return 1; bar; echo "  $2"; bar; }
sub(){ echo "▶ $*"; }
miss(){ echo "  (없음: $1)"; }
# ⚠ 하우스 CSV 는 Origin 호환을 위해 BOM 을 붙여 쓴다 → 첫 줄 주석이 grep -v "^#" 에
#   안 걸린다(실측). BOM 을 먼저 떼고 주석을 거른다.
nocom(){ sed '1s/^\xEF\xBB\xBF//' "$1" | grep -v '^#'; }

# ═══ ① 할로겐 공치환(Br) 조성 전주기 검증 ═══════════════════════════════
if sec 1 "① Li6PS5Cl0.5Br0.5 (Br 공치환) — 구조확정 · phonon · 결합차수"; then
sub "champion 구조 확정 (안장점 → DFT relax 재확인)"
$PY - <<'PY'
import json, os, textwrap
p = "db/compositions/comp2.json"
if not os.path.exists(p):
    print("  (없음: %s)" % p)
else:
    ch = json.load(open(p)).get("champion", {})
    for k in ("id", "label", "structure", "supersedes", "provenance"):
        if k in ch:
            for i, ln in enumerate(textwrap.wrap(str(ch[k]), 92)):
                print(f"  {k if i==0 else '':12s} {ln}")
PY
sub "Γ-점 phonon 재계산 (허수모드 개수로 동역학적 안정 판정)"
$PY - <<'PY'
import json, os
p = "db/properties/comp2_v3_phonon_uma.json"
if not os.path.exists(p):
    print("  (없음: %s)" % p)
else:
    d = json.load(open(p))
    for k in ("label", "nat", "method", "n_imaginary_beyond_tol",
              "imag_tol_cm1", "uma_fmax_at_V0_eVA", "relax_rmsd_vs_V0_A", "verdict"):
        if k in d: print(f"  {k:24s} {str(d[k])[:88]}")
PY
sub "결합차수 — Br 이 Li-할로겐을 약화시키는 기원 (ICOHP / ICOBI)"
[ -f db/properties/comp2_icohp_origin.csv ] && head -8 db/properties/comp2_icohp_origin.csv | sed 's/^/  /' || miss comp2_icohp_origin.csv
sub "Li-할로겐 결합길이 (Cl vs Br, 동일 구조)"
[ -f db/properties/comp2_halide_lengths_origin.csv ] && head -6 db/properties/comp2_halide_lengths_origin.csv | sed 's/^/  /' || miss comp2_halide_lengths_origin.csv
sub "탄성상수 (relaxed-ion 12-strain, comp1 대비)"
[ -f db/properties/comp2_vs_comp1_elastic.csv ] && head -8 db/properties/comp2_vs_comp1_elastic.csv | sed 's/^/  /' || miss comp2_vs_comp1_elastic.csv
echo
fi

# ═══ ② LPSOCl 결합화학 3중 독립검증 ═════════════════════════════════════
if sec 2 "② LPSOCl (O 치환) — ELF · Bader · COHP 3중 독립검증"; then
sub "ELF 결합 서술자 (중앙 40-60% 최솟값; >0.70 공유 · <0.30 이온)"
[ -f db/properties/elf_bonds_3sys_origin.csv ] && nocom db/properties/elf_bonds_3sys_origin.csv | sed 's/^/  /' || miss elf_bonds_3sys_origin.csv
sub "Bader 순전하 (all-electron plot_num=17, net = ZVAL - N_bader)"
for f in db/properties/bader_ae_modelc_LPSCl16.csv db/properties/bader_ae_lpsocl.csv \
          db/properties/bader_ae_b2o3.csv; do
  [ -f "$f" ] && { echo "  [$(basename "$f" .csv)]"; nocom "$f" | sed 's/^/    /'; }
done
sub "ICOHP 결합세기 (LOBSTER, eV/bond — 음수 클수록 강한 결합)"
[ -f db/properties/lpsocl_icohp_origin.csv ] && nocom db/properties/lpsocl_icohp_origin.csv | head -8 | sed 's/^/  /' || miss lpsocl_icohp_origin.csv
sub "BVSE Li 채널 부피 % (원본 주기셀 — 정량은 orig 열만)"
[ -f db/properties/bvse_3system_channel_origin.csv ] && nocom db/properties/bvse_3system_channel_origin.csv | head -8 | sed 's/^/  /' || miss bvse_3system_channel_origin.csv
sub "밴드갭 (고정점유 nscf VBM/CBM 고유값 — DOS 문턱 판독 금지)"
$PY - <<'PY'
import json, os
# ⚠ **정본 블록(eigenvalue_gaps_*)만** 읽는다. electronic.json 에는 비교용 하위블록
#   (comparison_*)도 있어서 전체를 훑으면 정본이 아닌 값이 섞여 나온다(실측).
p = "db/properties/electronic.json"
if not os.path.exists(p):
    print("  (없음: %s)" % p)
else:
    d = json.load(open(p))
    for blk, v in d.items():
        if not blk.startswith("eigenvalue_gaps") or not isinstance(v, dict):
            continue
        print(f"  [{blk}]")
        for sysname, rec in v.items():
            if isinstance(rec, dict) and "gap_eV" in rec:
                print(f"    {sysname:24s} {rec['gap_eV']:.4f} eV")
PY
echo
fi

# ═══ ③ SDCP–LiNiO2 계면 DFT+U ═══════════════════════════════════════════
if sec 3 "③ SDCP - LiNiO2(104) 계면 결합 DFT+U (Phase-A UMA -> Phase-B 재채점)"; then
sub "Phase-B 총에너지 원장 (plateau 규약 · 오차막대 포함)"
[ -f db/properties/sdcp_v7c_phaseB_energies.csv ] && head -7 db/properties/sdcp_v7c_phaseB_energies.csv | cut -c1-118 | sed 's/^/  /' || miss sdcp_v7c_phaseB_energies.csv
sub "슬랩-우선 재설계 후 SCF 수렴 궤적 (진단 도구 판정)"
S=/data/work/runs/sdcp_linio2_binding/phaseB_v7c_slabfirst/slab
if [ -f "$S/scf.out" ]; then
  $PY tools/sdcp/scf_convergence_doctor.py --scf_out "$S/scf.out" --scf_in "$S/scf.in" 2>/dev/null \
    | head -12 | sed 's/^/  /'
else miss "$S/scf.out"; fi
sub "Phase-A UMA 자세 스크린 (결합에너지 상위 자세)"
[ -f db/properties/sdcp_linio2_binding_phaseA.csv ] && head -6 db/properties/sdcp_linio2_binding_phaseA.csv | sed 's/^/  /' || miss sdcp_linio2_binding_phaseA.csv
echo
fi

# ═══ ④ 데이터 규율 게이트 · 자율검증 인프라 ═════════════════════════════
if sec 4 "④ 데이터 규율 게이트 + 자율검증 인프라"; then
sub "확산영역 게이트 — MSD log-log 기울기로 D/Ea 인용 가부 판정"
# ⚠ MD 산출물은 서버마다 루트가 다르다(gabia /root/work, kgy ~/work). 후보를 훑는다.
MSDDIR=""
for c in "$HOME/work/runs/comp2_disorder_relaxed" /root/work/runs/comp2_disorder_relaxed \
         /data/work/runs/comp2_disorder_relaxed; do
  [ -d "$c" ] && { MSDDIR="$c"; break; }
done
if [ -n "$MSDDIR" ]; then
  $PY tools/ionic/msd_diffusive_check.py --glob "$MSDDIR/d0.50_cfg*/T*/msd.json" 2>/dev/null \
    | head -14 | sed 's/^/  /'
else miss "comp2_disorder_relaxed (MD 산출 디렉토리)"; fi
sub "db 에 박힌 인용 규율 플래그 (계산 결과 파일이 스스로 제약을 들고 다닌다)"
$PY - <<'PY'
import glob, json, os, re
# ⚠ cut -c 는 UTF-8 을 바이트로 잘라 글자를 깨뜨린다(실측) → 파이썬에서 글자 단위로 자른다.
hits, files = [], set()
pat = re.compile(r"인용 금지|인용 보류|표시 전용|절대값 인용")
for p in sorted(glob.glob("db/properties/*.json")):
    try: txt = open(p, encoding="utf-8").read()
    except Exception: continue
    for m in re.finditer(r'"([A-Za-z_]+)"\s*:\s*"((?:[^"\\]|\\.)*)"', txt):
        v = m.group(2)
        if pat.search(v):
            files.add(p)
            hits.append((os.path.basename(p), m.group(1), re.sub(r"\s+", " ", v)))
seen, shown = set(), []      # 한 파일이 목록을 독점하지 않게 파일당 1건만 예시로 찍는다
for h in hits:
    if h[0] in seen: continue
    seen.add(h[0]); shown.append(h)
for f, k, v in shown[:4]:
    print(f"  [{f}] {k}")
    print(f"    {v[:96]}")
print(f"  → 인용 제약을 스스로 들고 다니는 db 항목 {len(files)} 개 / 플래그 {len(hits)} 건")
PY
sub "당월 git 활동 (전량 git-tracked)"
echo "  커밋 $(git log --since=2026-07-01 --until=2026-08-01 --oneline | wc -l) 건 · \
변경파일 $(git log --since=2026-07-01 --until=2026-08-01 --name-only --pretty=format: | sort -u | grep -c .) 종"
echo "  db/properties 등록 항목 $(ls db/properties | wc -l) 개 · \
kb/results 기록 $(ls kb/results 2>/dev/null | wc -l) 편 · litdb digest $(ls litdb/papers/*.md 2>/dev/null | wc -l) 편"
sub "감시 도구 실계기 (다중 작업 생존·진행 판정)"
$PY tools/ionic/watch_all.py 2>/dev/null | head -12 | sed 's/^/  /'
echo
fi
