#!/bin/bash
# fetch_paw_pseudos.sh — stage the 6 all-PAW (kjpaw) pseudos into ./pseudo/ for
# the LOBSTER ICOHP run (icohp_paw_kisti.sh). LOBSTER rejects USPP, so every
# species must be kjpaw(PAW).
#
# RUN ON A KISTI LOGIN NODE — compute nodes have no outbound internet.
#   bash tools/electronic/fetch_paw_pseudos.sh [target_dir]   # default: .
#   sbatch tools/electronic/icohp_paw_kisti.sh
#
# Any file already present and valid is kept (e.g. an O 0.1 pseudo you already
# have). A 403/hotlink error page is ~36 B and is rejected by the size gate.
set -u
cd "${1:-.}"; mkdir -p pseudo
FILES="Li.pbe-sl-kjpaw_psl.1.0.0.UPF P.pbe-n-kjpaw_psl.1.0.0.UPF \
S.pbe-nl-kjpaw_psl.1.0.0.UPF Cl.pbe-nl-kjpaw_psl.1.0.0.UPF \
O.pbe-n-kjpaw_psl.0.1.UPF B.pbe-n-kjpaw_psl.1.0.0.UPF"
isupf(){ [ -s "$1" ] && [ "$(wc -c <"$1" 2>/dev/null)" -gt 2000 ]; }  # real UPF >> 36 B error page
ok=0; miss=""
for f in $FILES; do
  if isupf "pseudo/$f"; then echo "have  $f"; ok=$((ok+1)); continue; fi
  for url in "https://pseudopotentials.quantum-espresso.org/upf_files/$f" \
             "https://www.quantum-espresso.org/upf_files/$f"; do
    curl -fsSL -o "pseudo/$f.part" "$url" 2>/dev/null || wget -qO "pseudo/$f.part" "$url" 2>/dev/null || true
    if isupf "pseudo/$f.part"; then mv "pseudo/$f.part" "pseudo/$f"; echo "got   $f ($(wc -c <"pseudo/$f") B)"; ok=$((ok+1)); break; fi
    rm -f "pseudo/$f.part"
  done
  isupf "pseudo/$f" || { echo "FAIL  $f"; miss="$miss $f"; }
done
echo "---- $ok/6 present in pseudo/ ----"
if [ -n "$miss" ]; then
  echo "missing:$miss"
  echo "이름이 pslibrary 버전과 다를 수 있음 — 이 목록 알려주면 맞는 파일명으로 고쳐줄게."
  exit 1
fi
echo "ALL 6 READY  ->  sbatch tools/electronic/icohp_paw_kisti.sh"
