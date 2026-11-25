#!/usr/bin/env bash
# setup_pseudo_kgy.sh — Nd Q3′ (card nd_q3p_same_cell_card_2026_10_27) pseudopotentials on kgy.
#   ① PAW psl set (Bader SCF): MD5 must equal the Q2 kgy record (db/raw/nd_q2_decomp_2026_10_23/run_kgy/*/scf.out).
#   ② NC set (ELF SCF) into NC_DIR: Nd UPF from the repo (Q3 conversion) + SG15 (Li P S Cl 1.2 · O 1.0) — a copy already on
#      this machine is used only if its MD5 matches the Q3 ELF record (db/raw/nd_q3_elf_2026_10_19/scf.out); otherwise downloaded
#      from SG15_URL and checked the same way. NC_DIR/.md5_ok is written only when all six match.
# Env: W (worktree, required) · PAW_DIR (/home/kgy/work/pseudo) · NC_DIR (/home/kgy/work/runs/nd_q3p_1027/pseudo_nc) ·
#      SG15_URL · SEARCH (dirs to look in) · PAW_LIST / NC_LIST (override the "file md5" lists — selftest only)
# Exit: 0 both sets OK · 3 PAW missing or MD5 differs (Bader must not run) · 4 NC incomplete (ELF skipped, Bader can run)
# Cannot: judge whether a pseudo is physically right — it only proves it is the same file the earlier runs used.
#   bash setup_pseudo_kgy.sh --selftest
set -u
md5(){ md5sum "$1" 2>/dev/null | cut -d' ' -f1; }
PAW_LIST_DEF="Li.pbe-sl-kjpaw_psl.1.0.0.UPF 4449e4b2026dd225cbf03a6cd6c9364f
P.pbe-n-kjpaw_psl.1.0.0.UPF 06b8cad1975795032ee26009bb7624c7
S.pbe-nl-kjpaw_psl.1.0.0.UPF a0db168fa6a42edaf368e88c1856b871
Cl.pbe-nl-kjpaw_psl.1.0.0.UPF daecd58dfbed9f74c5ea20c0112c952a
O.pbe-n-kjpaw_psl.0.1.UPF 0234752ac141de4415c5fc33072bef88
Nd.pbe-spdn-kjpaw_psl.1.0.0.UPF af9d8c60a66e158c564458cc346d9fb1"
NC_LIST_DEF="Li_ONCV_PBE-1.2.upf c91dd4cee9943b136ac3b62641658f95
P_ONCV_PBE-1.2.upf 0688a67b2b263c6b42d3d97c42745426
S_ONCV_PBE-1.2.upf f9d020296ee6110346977bfd66d424f6
Cl_ONCV_PBE-1.2.upf 0f993535b366f580ecbcdacce103c843
O_ONCV_PBE-1.0.upf 2e7c0b1a1696cff0b124505fc5a2822d
Nd3plus_f-in-core.dojo_psp8_conv.upf 465d92ca243ebaf807c6f9e83c47e09b"

main(){
  local PAW_DIR=${PAW_DIR:-/home/kgy/work/pseudo} NC_DIR=${NC_DIR:-/home/kgy/work/runs/nd_q3p_1027/pseudo_nc}
  local SG15_URL=${SG15_URL:-http://www.quantum-simulation.org/potentials/sg15_oncv/upf}
  local SEARCH=${SEARCH:-/home/kgy/work/pseudo /home/kgy/apps /home/kgy/work/runs}
  local NDREPO="${W:?W (worktree) is required}/db/inputs/nd_q3_elf_nc_2026_10_19/pseudo"
  local paw_ok=1 nc_ok=1 f m got c
  while read -r f m; do
    [ -n "$f" ] || continue
    got=$(md5 "$PAW_DIR/$f")
    if [ "$got" = "$m" ]; then echo "  PAW ✓ $f"; else echo "  PAW ⛔ $f (${got:-없음} ≠ ${m:0:8})"; paw_ok=0; fi
  done <<< "${PAW_LIST:-$PAW_LIST_DEF}"
  mkdir -p "$NC_DIR"; rm -f "$NC_DIR/.md5_ok"
  while read -r f m; do
    [ -n "$f" ] || continue
    if [ "$(md5 "$NC_DIR/$f")" != "$m" ]; then
      rm -f "$NC_DIR/$f"
      [ -f "$NDREPO/$f" ] && [ "$(md5 "$NDREPO/$f")" = "$m" ] && cp "$NDREPO/$f" "$NC_DIR/$f" && echo "  NC  ← 저장소 $f"
      if [ ! -f "$NC_DIR/$f" ]; then
        # shellcheck disable=SC2086
        for c in $(find $SEARCH -maxdepth 4 -name "$f" -type f 2>/dev/null); do
          [ "$(md5 "$c")" = "$m" ] && { cp "$c" "$NC_DIR/$f"; echo "  NC  ← $c"; break; }
        done
      fi
      if [ ! -f "$NC_DIR/$f" ]; then
        case "$f" in *ONCV*) curl -fsSL -m 90 -o "$NC_DIR/$f" "$SG15_URL/$f" 2>/dev/null && echo "  NC  ← $SG15_URL/$f" ;; esac
      fi
    fi
    got=$(md5 "$NC_DIR/$f")
    if [ "$got" = "$m" ]; then echo "  NC  ✓ $f"; else echo "  NC  ⛔ $f (${got:-없음} ≠ ${m:0:8})"; nc_ok=0; rm -f "$NC_DIR/$f"; fi
  done <<< "${NC_LIST:-$NC_LIST_DEF}"
  [ "$nc_ok" = 1 ] && touch "$NC_DIR/.md5_ok"
  [ "$paw_ok" = 1 ] || { echo "⛔ PAW 세트가 기록과 다르다 — Bader SCF 를 돌리지 않는다"; return 3; }
  [ "$nc_ok" = 1 ] || { echo "⚠ NC 세트가 다 안 갖춰졌다 — ELF 는 건너뛴다 (Bader 는 돈다)"; return 4; }
  echo "✅ PAW 6 · NC 6 MD5 일치"; return 0
}

if [ "${1:-}" = "--selftest" ]; then
  T=$(mktemp -d); ok=0; bad=0
  ck(){ if [ "$2" = "$3" ]; then ok=$((ok+1)); else bad=$((bad+1)); echo "  ✗ $1 — got '$2' want '$3'"; fi; }
  mkdir -p "$T/paw" "$T/w/db/inputs/nd_q3_elf_nc_2026_10_19/pseudo" "$T/other" "$T/web"
  for e in Li P; do echo "paw $e" > "$T/paw/$e.paw"; done
  echo "nd nc" > "$T/w/db/inputs/nd_q3_elf_nc_2026_10_19/pseudo/Nd.nc"
  echo "li sg15" > "$T/other/Li_ONCV_X.upf"; echo "o sg15" > "$T/web/O_ONCV_X.upf"
  PL="Li.paw $(md5 "$T/paw/Li.paw")
P.paw $(md5 "$T/paw/P.paw")"
  NL="Nd.nc $(md5 "$T/w/db/inputs/nd_q3_elf_nc_2026_10_19/pseudo/Nd.nc")
Li_ONCV_X.upf $(md5 "$T/other/Li_ONCV_X.upf")
O_ONCV_X.upf $(md5 "$T/web/O_ONCV_X.upf")"
  run(){ ( W=$T/w PAW_DIR=$T/paw NC_DIR=$T/nc SEARCH=$T/other SG15_URL=file://$T/web PAW_LIST=$PL NC_LIST=$NL main ) > "$T/log" 2>&1; echo $?; }
  ck "양성: 저장소 · 이 기계 사본 · 내려받기 셋 다 → rc 0" "$(run)" 0
  ck "양성: .md5_ok 생김" "$([ -f "$T/nc/.md5_ok" ] && echo y || echo n)" y
  ck "양성: 출처 세 줄 (저장소 · 사본 · URL)" "$(grep -c '  NC  ←' "$T/log")" 3
  ck "양성: 다시 돌리면 받지 않는다 (이미 맞음)" "$(run):$(grep -c '  NC  ←' "$T/log")" "0:0"
  echo "tampered" > "$T/paw/P.paw"
  ck "⛔음성: PAW 하나가 다르면 rc 3" "$(run)" 3
  echo "paw P" > "$T/paw/P.paw"
  rm -rf "$T/nc"; echo "wrong li" > "$T/other/Li_ONCV_X.upf"; rm -f "$T/web/Li_ONCV_X.upf"
  ck "⛔음성: 사본 MD5 가 틀리고 받을 곳도 없으면 rc 4" "$(run)" 4
  ck "⛔음성: 그때 .md5_ok 가 없다 · 틀린 사본을 안 가져왔다" "$([ -f "$T/nc/.md5_ok" ] && echo y || echo n):$([ -f "$T/nc/Li_ONCV_X.upf" ] && echo y || echo n)" "n:n"
  echo "corrupt" > "$T/web/O_ONCV_X.upf"; rm -rf "$T/nc"; echo "li sg15" > "$T/other/Li_ONCV_X.upf"
  ck "⛔음성: 내려받은 파일 MD5 가 틀리면 rc 4 · 지운다" "$(run):$([ -f "$T/nc/O_ONCV_X.upf" ] && echo y || echo n)" "4:n"
  ( PAW_LIST=$PL main ) > /dev/null 2>&1; ck "⛔음성: W 없으면 멈춘다" "$?" 1
  rm -rf "$T"; echo "selftest: ✓ $ok · ✗ $bad"; [ "$bad" = 0 ] && exit 0 || exit 1
fi
main
