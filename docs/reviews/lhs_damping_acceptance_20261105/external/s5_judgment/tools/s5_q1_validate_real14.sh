#!/bin/bash
# Q1 확정 도구 (s5_q1_electrode_settle.py) 검증 — 커밋된 real_14 덤프로 여덟 경우 (리포는 읽기만 · 쓰기 = <새 빈 폴더> 안).
#   기대: cg = INCONCLUSIVE (rc 4) · inc · incfull = INCLUDE (rc 0) · negA · negA0 · negB · negRun · negCode = HOLD (rc 3)
# 사용: bash s5_q1_validate_real14.sh <리포 (B7 과 망 코드 바이트 같은 트리)> <새 빈 폴더> <받은 B7 manifest.json>
set -u
W=$1; V=$2; MAN=$3
H=$W/docs/data/lhs_network214_35f032737_20261030/s5_judgment/tools
T=$H/s5_q1_electrode_settle.py
F=$H/s5_q1_validate_fixtures.py
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
if [ -e "$V" ]; then echo "⛔ $V 가 이미 있다 (새 폴더에만 쓴다)"; exit 2; fi
mkdir -p "$V/dumps" "$V/case" "$V/old" "$V/oldd" "$V/oldsrc" "$V/oldsrcd" "$V/fx"
cd "$V" || exit 2
D=$W/docs/data/real14_reference_20260928
gunzip -c "$D/atom_2060000.liggghts.gz" > "$V/dumps/atom_2060000.liggghts"
gunzip -c "$D/contact_2060000.liggghts.gz" > "$V/dumps/contact_2060000.liggghts"
cp "$D/mesh_2060000.stl" "$D/input_real_14.liggghts" "$V/dumps/"
python3 "$W/scripts/parse_liggghts.py" "$V/dumps/atom_2060000.liggghts" "$V/dumps/contact_2060000.liggghts" \
    "$V/dumps/mesh_2060000.stl" "$V/dumps/input_real_14.liggghts" -o "$V/case" > "$V/parse.log" 2>&1 || { echo '⛔ parse'; exit 2; }
for d in old oldd; do for f in atoms.csv contacts.csv mesh_info.json input_params.json; do cp "$V/case/$f" "$V/$d/$f"; done; done
# B7 (= 이 트리의 망 코드) CLI — 웹앱 파이프라인과 같은 인자
python3 "$W/scripts/network_conductivity.py" "$V/case/atoms.csv" "$V/case/contacts.csv" -o "$V/case" \
    -t 1:AM_P,2:AM_S,3:SE -s 1000 --contact-mode both > "$V/b7cli.log" 2>&1 || { echo '⛔ B7 CLI'; exit 2; }
# v1.2 세대 모듈 (11fcf91e8) — 그대로 (CG 경로) · CG 문턱만 끈 사본 (직접해)
git -C "$W" archive -o "$V/old_scripts.tar" 11fcf91e8a1f4837b83892b7e4a81125eaeee4e5 scripts || { echo '⛔ git archive'; exit 2; }
tar -xf "$V/old_scripts.tar" -C "$V/oldsrc"
tar -xf "$V/old_scripts.tar" -C "$V/oldsrcd"
python3 -I "$F" forcedirect "$V/oldsrcd/scripts/network_conductivity.py" || exit 2
python3 "$V/oldsrc/scripts/network_conductivity.py" "$V/old/atoms.csv" "$V/old/contacts.csv" -o "$V/old" \
    -t 1:AM_P,2:AM_S,3:SE -s 1000 --contact-mode both > "$V/oldcli.log" 2>&1 || { echo '⛔ 옛 CLI'; exit 2; }
python3 "$V/oldsrcd/scripts/network_conductivity.py" "$V/oldd/atoms.csv" "$V/oldd/contacts.csv" -o "$V/oldd" \
    -t 1:AM_P,2:AM_S,3:SE -s 1000 --contact-mode both > "$V/olddcli.log" 2>&1 || { echo '⛔ 옛 CLI (직접해 사본)'; exit 2; }
python3 -I "$F" prov "$V" || exit 2
cp -r "$V/case" "$V/case_negA"; cp -r "$V/case" "$V/case_negA0"; cp -r "$V/oldd" "$V/oldd_negB"; cp -r "$V/case" "$V/case_run"
python3 -I "$F" fixtures "$V" "$MAN" || exit 2
run() {  # 이름 · 인자들
  nm=$1; shift
  python3 -I "$T" --repo "$W" --case real14 --out "$V/out_$nm" "$@" > "$V/run_$nm.log" 2>&1
  echo "== $nm rc=$?"
}
O=$V/old/network_conductivity_dual.json; OD=$V/oldd/network_conductivity_dual.json
run cg      --case-dir "$V/case"       --v12-dual "$O"  --v12-prov "$V/old/network_provenance.json"
run inc     --case-dir "$V/case"       --v12-dual "$OD" --v12-prov "$V/oldd/network_provenance.json" --assume-v12-direct
run negA    --case-dir "$V/case_negA"  --v12-dual "$OD" --assume-v12-direct
run negA0   --case-dir "$V/case_negA0" --v12-dual "$OD" --assume-v12-direct
run negB    --case-dir "$V/case"       --v12-dual "$V/oldd_negB/network_conductivity_dual.json" --assume-v12-direct
run incfull --case-dir "$V/case_run"   --v12-dual "$OD" --v12-prov "$V/oldd/network_provenance.json" --assume-v12-direct \
    --b7-manifest "$V/fx/manifest_ok.json" --b7-reread "$V/fx/reread_ok.json"
run negRun  --case-dir "$V/case_run"   --v12-dual "$OD" --assume-v12-direct --b7-manifest "$V/fx/manifest_ok.json" --b7-reread "$V/fx/reread_badrun.json"
run negCode --case-dir "$V/case_run"   --v12-dual "$OD" --assume-v12-direct --b7-manifest "$V/fx/manifest_badcode.json" --b7-reread "$V/fx/reread_ok.json"
python3 -I "$F" collect "$V" "$V/q1_settle_validation.json"
