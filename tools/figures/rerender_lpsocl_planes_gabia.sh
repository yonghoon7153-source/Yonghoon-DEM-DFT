#!/usr/bin/env bash
# rerender_lpsocl_planes_gabia.sh — LPSOCl ELF 평면을 **jet** 컬러맵으로 다시 렌더한다.
#   (2026-08-04 요청: b2o3·LPSCl16 슬라이드 family 와 같은 "쩅한" 색으로 통일)
#
# 왜 서버인가: lpsocl_elf.cube 가 수십 MB라 repo 에 없다. 여기서 한 번 돌면
#   평면 캐시(npz)가 생겨서 **그 다음부터는 색 바꾸는 데 cube 가 필요 없다**
#   (어디서든 tools/figures/restyle_elf_planes.py).
#
# 안전: 순수 CPU(numpy/matplotlib) — GPU 안 쓴다. SDCP slab pw.x 와 같이 돌아도 되지만
#   CPU 를 뺏지 않게 nice 로 돌린다. 기존 산출물은 건드리지 않고 새 폴더에 쓴다.
#
#   bash tools/figures/rerender_lpsocl_planes_gabia.sh
set -u
REPO=${REPO:-$HOME/Yonghoon-DEM-DFT}; [ -d "$REPO" ] || REPO=$HOME/work/Yonghoon-DEM-DFT
E=${ELF_DIR:-/data/work/runs/lpsocl_elf}
OUT=${OUT:-$E/postproc/planes_jet}
CMAP=${CMAP:-jet}
PY=${PY:-python3}

if pgrep -f "elf_planes_lpsocl.py" >/dev/null 2>&1; then
  echo "⛔ elf_planes_lpsocl.py 가 이미 돌고 있다 — 중복 실행 방지"; exit 1
fi
[ -f "$E/lpsocl_elf.cube" ] || { echo "⛔ cube 없음: $E/lpsocl_elf.cube"; exit 1; }

cd "$REPO" || exit 1
echo "── 도구 최신화 (브랜치 파일만 체크아웃) ──"
git fetch origin claude/friendly-meitner-lldvar 2>&1 | tail -2
git checkout FETCH_HEAD -- tools/figures/elf_planes_lpsocl.py \
                           tools/figures/restyle_elf_planes.py || exit 1
git --no-pager log -1 --format="  도구 커밋 %h %s" FETCH_HEAD

mkdir -p "$OUT"
echo "── 렌더 (cmap=$CMAP) ──"
nice -n 10 $PY tools/figures/elf_planes_lpsocl.py \
    --cube "$E/lpsocl_elf.cube" --out "$OUT" \
    --label "LPSOCl (Li27P5S21OCl8)" --tag lpsocl \
    --cmap "$CMAP" --save_npz 2>&1 | grep -a -v '^\s*$'

echo
echo "── 산출 ──"; ls -la "$OUT" | grep -a -E "png|npz|csv"
echo
echo "회수 (로컬에서):"
echo "  scp root@121.78.116.27:'$OUT/*.png' ."
echo "  scp root@121.78.116.27:'$OUT/lpsocl_elf_planes.npz' .    # 평면 캐시 — 다음 색 변경은 이걸로"
echo "색만 또 바꾸려면 (cube 불필요, 로컬에서도 됨):"
echo "  python3 tools/figures/restyle_elf_planes.py --npz lpsocl_elf_planes.npz --out planes_X --cmap turbo"
