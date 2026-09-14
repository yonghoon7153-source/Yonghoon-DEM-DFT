#!/usr/bin/env bash
# F8: run_states.sh with the `flock` binary absent from PATH (verify's three commands replaced by a fast shim that embeds BMS_RUN_ID)
S="$(cd "$(dirname "$0")" && pwd)"; W="$S/wt/bms-balancing"; REALPY="$(command -v python3)"
mkdir -p "$S/shim" "$S/path_noflock"
cat > "$S/shim/python3" <<SH
#!/usr/bin/env bash
if [ "\$1" = "-m" ] && [ "\$2" = "bms_balancing.verify" ]; then
  case "\$3" in
    degeneracy) printf '{"state":"100","run_id":"%s","LAM_NE_percent":{"span":1.0}}\n' "\$BMS_RUN_ID"; exit 0;;
    matrix|profile) out=""; while [ \$# -gt 0 ]; do [ "\$1" = "--out" ] && out="\$2"; shift; done
        printf 'gamma_Si,obj,run_id\n0.1,1.0,%s\n' "\$BMS_RUN_ID" > "\$out"; echo "wrote \$out"; exit 0;;
  esac
fi
exec $REALPY "\$@"
SH
chmod +x "$S/shim/python3"
for d in /usr/local/bin /usr/bin /bin; do for f in "$d"/*; do n="$(basename "$f")"; [ "$n" = flock ] && continue; [ -e "$S/path_noflock/$n" ] || ln -s "$f" "$S/path_noflock/$n"; done; done
run_case () {  # run_case <label> <PATH>
  local out="$S/f8 out $1"; rm -rf "$out"; mkdir -p "$out"
  (cd "$W" && env -i HOME="$HOME" PATH="$2" BMS_DATA_ROOT="$S/data/가형 관련/degradation mode" OUT="$out" STATES=100 STARTS=1 bash scripts/run_states.sh > "$S/f8_$1.stdout" 2> "$S/f8_$1.stderr"; echo "rc=$?")
  echo "-- stderr (flock / diagnostic lines):"; sed 's/\x1b\[[0-9;]*m//g' "$S/f8_$1.stderr" | grep -n "flock\|run id\|FAIL\|실패\|전부 통과" | cut -c1-150
  echo "-- out dir:"; ls -A "$out" | tr '\n' ' '; echo; echo "-- 'flock' in degeneracy .log:"; grep -c flock "$out/degeneracy_100_Li.json.log" 2>/dev/null
}
echo "### CASE A: flock absent"; run_case noflock "$S/shim:$S/path_noflock"
echo "### CASE B: flock present (control)"; run_case withflock "$S/shim:/usr/local/bin:/usr/bin:/bin"
echo "### run_states.sh guards for flock:"; grep -n "command -v\|flock" "$W/scripts/run_states.sh" | cut -c1-120
