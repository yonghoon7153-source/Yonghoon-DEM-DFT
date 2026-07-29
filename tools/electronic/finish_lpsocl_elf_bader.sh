#!/usr/bin/env bash
# =============================================================================
# finish_lpsocl_elf_bader.sh — ELF/Bader 가 끝나면 **회수 가능한 크기**로 후처리.
#
# 왜 필요한가
#   산출 cube 는 수십 MB라 gzip+base64 로 못 옮긴다(COHP 때 이미 겪었다).
#   그래서 gabia 에서 *여기서* 후처리해 **작은 것만** 회수한다:
#     · CDD cube (rho_scf − rho_atomic) + .vesta 페어  → gabia 에 보관, 경로만 기록
#     · ELF 결합 중점값 CSV (b2o3/comp1 과 같은 양식)  → 회수 (수 KB)
#     · CDD 2D 슬라이스·3D 등가면 PNG                  → 회수 (수백 KB)
#     · Bader 원소별 net charge JSON                    → 회수 (1 KB)
#
# ⚠ 이 스크립트는 **기다리지 않는다.** 아직 안 끝난 단계는 건너뛰고 뭐가 없는지 알려준다.
#   ELF/Bader 가 도는 중에 여러 번 돌려도 안전하다.
#
#   bash tools/electronic/finish_lpsocl_elf_bader.sh
# =============================================================================
set -u; set +H
REPO=${REPO:-$HOME/Yonghoon-DEM-DFT}; [ -d "$REPO" ] || REPO=$HOME/work/Yonghoon-DEM-DFT
E=${ELF_DIR:-/data/work/runs/lpsocl_elf}
B=${BADER_DIR:-/data/work/runs/lpsocl_bader}
OUT=$E/postproc; mkdir -p "$OUT"
PY=${PY:-python3}
ok(){ [ -s "$1" ]; }
say(){ echo "[$(date +%H:%M:%S)] $*"; }

echo "===== 현재 산출물 ====="
for f in scf.out scf_atomic.out lpsocl_elf.cube lpsocl_rho_scf.cube lpsocl_rho_atomic.cube; do
  if ok "$E/$f"; then printf "  ✓ %-24s %8.1f MB\n" "$f" "$(du -m "$E/$f" | cut -f1)"
  else printf "  · %-24s (아직)\n" "$f"; fi
done
ok "$B/lpsocl_bader_summary.json" && echo "  ✓ bader summary" || echo "  · bader summary (아직)"
echo

# ── 1) ELF 결합 중점값 (b2o3/comp1 과 같은 양식) ────────────────────────────
if ok "$E/lpsocl_elf.cube"; then
  if [ -f "$REPO/tools/figures/sample_elf_bonds.py" ]; then
    say "ELF 결합 중점 샘플링"
    # ⚠ 구조는 cube 안의 원자좌표에서 읽는다 — --struct 인자는 없다.
    #   CUT 표에 O-P 1.9 / Li-O 2.5 가 이미 있어 LPSOCl 이 그대로 커버된다.
    $PY "$REPO/tools/figures/sample_elf_bonds.py" \
        --cube "$E/lpsocl_elf.cube" --system lpsocl \
        --out "$OUT/lpsocl_elf_bond_midpoint.csv" 2>&1 | tail -10 \
      || say "⚠ sample_elf_bonds 실패 — tail 확인"
  else
    say "⚠ tools/figures/sample_elf_bonds.py 없음 — git pull"
  fi
  # 결합별 ELF **프로파일** — 중앙 최솟값이 눈에 보이는 그림 + Origin CSV.
  #   ⚠ PNG(수백 KB)는 base64 로 못 옮긴다. **CSV 만 회수**해서 로컬에서 하우스 스타일로 다시 그린다
  #     (COHP 때와 같은 방식). PNG 는 gabia 에서 바로 보는 용도.
  if [ -f "$REPO/tools/figures/plot_elf_profile.py" ]; then
    say "ELF 결합별 프로파일"
    $PY "$REPO/tools/figures/plot_elf_profile.py" \
        --cube "$E/lpsocl_elf.cube" --label "LPSOCl (Li27P5S21OCl8)" \
        --out "$OUT/lpsocl_ELF_profiles.png" \
        --csv "$OUT/lpsocl_elf_profiles_origin.csv" 2>&1 | tail -12
  fi
else
  say "ELF cube 아직 — 결합 중점 건너뜀"
fi

# ── 2) CDD = rho_scf − rho_atomic ──────────────────────────────────────────
if ok "$E/lpsocl_rho_scf.cube" && ok "$E/lpsocl_rho_atomic.cube"; then
  if [ ! -s "$OUT/lpsocl_cdd.cube" ]; then
    say "CDD 계산 (rho_scf − rho_atomic)"
    $PY "$REPO/tools/electronic/cube_diff.py" --mode sub \
        --a "$E/lpsocl_rho_scf.cube" --b "$E/lpsocl_rho_atomic.cube" \
        --out "$OUT/lpsocl_cdd.cube" 2>&1 | tail -5
  fi
  if ok "$OUT/lpsocl_cdd.cube"; then
    say "CDD 그림 + VESTA 페어"
    $PY "$REPO/tools/electronic/plot_cdd.py" --cube "$OUT/lpsocl_cdd.cube" \
        --out "$OUT/lpsocl_cdd" 2>&1 | tail -4
    # ⚠ .vesta 는 ASCII 전용 + CRLF, cube 와 **같은 폴더**여야 IMPORT_DENSITY 가 산다
    $PY "$REPO/tools/electronic/cube_to_vesta_cdd.py" "$OUT/lpsocl_cdd.cube" 2>&1 | tail -3
  fi
else
  say "rho_scf/rho_atomic 둘 다 있어야 CDD — 건너뜀"
fi

# ── 3) Bader 요약 (기존 표와 같은 방법인지 대조) ────────────────────────────
if ok "$B/lpsocl_bader_summary.json"; then
  say "Bader 요약:"
  $PY - "$B/lpsocl_bader_summary.json" <<'PYC'
import json, sys
d = json.load(open(sys.argv[1]))
print("   ", d.get("method", "")[:100])
for k, v in d.get("per_species", {}).items():
    print(f"    {k:3s} n={v['n']:3d}  {v['mean']:+.3f}  [{v['min']:+.3f}, {v['max']:+.3f}]")
print("    ⚠ 비교 상대: db/properties/bader_b2o3_vs_lpscl16.csv (같은 AE plot_num=17 + kjpaw)")
print("       b2o3 Li +0.881 / P +4.691 / S_avg -1.80 / Cl -0.914")
print("       LPSCl16 Li +0.883 / P +4.340 / S_avg -1.736 / Cl -0.918")
PYC
fi

# ── 4) 회수 꾸러미 (작은 것만) ──────────────────────────────────────────────
PK=$OUT/retrieve; mkdir -p "$PK"; rm -f "$PK"/*
# ⚠ **PNG 는 꾸러미에 안 넣는다.** lpsocl_cdd_3d.png 354 KB + slice 137 KB 면 base64 가
#   600 KB 를 넘어 붙여넣기가 잘린다(15 KB 짜리도 한 번 CRC 깨진 전례가 있다).
#   그림은 gabia 에서 직접 보고, **회수는 CSV/JSON 만** — 로컬에서 하우스 스타일로 다시 그린다.
for f in "$OUT/lpsocl_elf_bond_midpoint.csv" "$OUT/lpsocl_elf_profiles_origin.csv" \
         "$B/lpsocl_bader_summary.json"; do
  [ -s "$f" ] && cp "$f" "$PK/" 2>/dev/null
done
N=$(ls -1 "$PK" 2>/dev/null | wc -l)
echo
echo "===== 회수 꾸러미 ($N 개) ====="
ls -la --time-style=+%m-%d\ %H:%M "$PK" 2>/dev/null | tail -n +2
if [ "$N" -gt 0 ]; then
  TAR=/tmp/lpsocl_retrieve.tgz; tar czf "$TAR" -C "$PK" .
  echo
  echo "회수: md5 $(md5sum "$TAR" | cut -d' ' -f1) · $(du -h "$TAR" | cut -f1)"
  echo "  base64 -w 200 $TAR   ← 이 출력을 붙여넣으면 repo 로 들어간다"
fi
echo
echo "⚠ cube 원본은 gabia 에 둔다 (수십 MB — repo 로 옮기지 않는다):"
echo "   $E/lpsocl_elf.cube · $OUT/lpsocl_cdd.cube (+ .vesta 페어, 같은 폴더)"
echo "   VESTA 로 보려면 이 둘을 **함께** 내려받아야 한다."
