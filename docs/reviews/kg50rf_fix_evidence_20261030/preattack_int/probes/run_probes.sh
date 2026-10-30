#!/bin/bash
# PAI — run every probe once and keep its stdout in ../logs/ (scratch = $1 · Codex ZIP extracted root = $2, optional)
#   order: make_d07_resume → c_real → cut_d2 → e2e (T · M · MX · TM2 · TM2 control · SUF) → mesh_escape → varstyles → pairs24 →
#          codex_cases (if $2) → shadow_import → lineage
P=$(cd "$(dirname "$0")" && pwd)
LG=$P/../logs; mkdir -p "$LG"
SP=${1:?scratch}; CX=$2
run() { local n=$1; shift; echo "== $n"; { echo "\$ $*"; nice -n 10 "$@"; echo "[rc=$?]"; } > "$LG/$n.log" 2>&1; tail -1 "$LG/$n.log"; }
run make_d07_resume python3 "$P/make_d07_resume.py" "$SP/d07"
run c_real bash "$P/c_real.sh" "$SP"
run cut_d2 bash "$P/cut_d2.sh" "$SP"
run e2e_T python3 "$P/e2e_d07.py" "$SP" T
run e2e_M python3 "$P/e2e_d07.py" "$SP" M
run e2e_MX python3 "$P/e2e_d07.py" "$SP" MX
run e2e_TM2 python3 "$P/e2e_d07.py" "$SP" TM2
run e2e_TM2_control env PAI_NOCHANGE=1 python3 "$P/e2e_d07.py" "$SP" TM2
run e2e_SUF python3 "$P/e2e_d07.py" "$SP" SUF
run mesh_escape bash "$P/mesh_escape.sh" "$SP"
run varstyles python3 "$P/varstyles.py" "$SP"
run pairs24 python3 "$P/pairs24.py" "$SP"
[ -n "$CX" ] && run codex_cases python3 "$P/codex_cases.py" "$CX" "$SP"
run shadow_import bash "$P/shadow_import.sh" "$SP"
run lineage bash "$P/lineage.sh"
