#!/bin/bash
# PRE2-impl-01 payload 끝-끝 (깨끗한 사본 head_93d) — 임시 폴더 지우고 다시 → census 요약
D=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview2_impl
cd "$D" || exit 9
rm -rf "$D"/p2svp_*
export PRE_REPO="$D/head_93d" OPENBLAS_NUM_THREADS=1
timeout 900 nice -n 19 python3 -I probe2_sv_unsplit_payload.py 2>&1 | cut -c1-900
for d in "$D"/p2svp_*; do
  python3 -I - "$d" <<'EOF'
import json, sys
d = sys.argv[1]
m = json.load(open(d + '/p.json'))['mpm_metrics']['step3']['manifest']
c = m['ca_ext']['cjunc']['evidence'].get('census') or {}
print(d.rsplit('/', 1)[-1], {k: c.get(k) for k in ('n_pieces', 'n_positions', 'n_live_positions', 'n_bridging_components',
                                                    'n_unsplit_bridging_components', 'n_vx_faces_by_sid')})
EOF
done
