#!/bin/bash
# 우리 트리 재현 (10-28) — 리포 뿌리에서: bash docs/reviews/codex_kg50_resume_recheck_20261028/_repro_ours_20261028/repro_ours.sh <빈 임시 폴더>
# ① 실제 awk 시험 절단기 (resume_ckpt.sh 693 줄의 awk 프로그램 그대로) 를 Codex 변이 덱에 돌려 Codex 전사본과 바이트 대조
# ② 실제 bash `resume_ckpt.sh -C` 로 09-27 r075 압축 덱 쌍 정적 대조 (KG50R-01)
# DEM · SLURM · 원격 접속 없음.  출력은 이 폴더의 awk_trial/ · r075_bash_C/ 에 쓴다.
set -u
TMP="$1"; [ -d "$TMP" ] || { echo "임시 폴더 없음"; exit 2; }
H=$(cd "$(dirname "$0")" && pwd); E=$H/../independent; TOOL=scripts/resume_ckpt.sh
[ -f "$TOOL" ] || { echo "리포 뿌리에서 실행"; exit 2; }
echo "tool sha256 $(sha256sum $TOOL | cut -c1-64)" > $H/awk_trial/table.txt
AWKP=$(sed -n '693p' $TOOL | sed -E "s/^ *awk -v t=\\\$TS '([^']*)'.*/\1/")
echo "awk 프로그램 (693 줄): $AWKP" >> $H/awk_trial/table.txt
echo "awk = $(readlink -f "$(command -v awk)")" >> $H/awk_trial/table.txt
for d in deck scheduler; do for f in $E/$d/*_trial.liggghts; do b=${f%_trial.liggghts}; [ -f $b.liggghts ] || continue
  awk -v t=2000 "$AWKP" $b.liggghts > $TMP/t.liggghts
  # scheduler/ 고정물은 Codex Windows 에서 text 모드로 써서 CRLF — CR 을 빼고 비교 (deck/ 은 바이트 그대로 LF)
  if cmp -s $TMP/t.liggghts $f; then r=같음; elif cmp -s <(tr -d '\r' < $TMP/t.liggghts) <(tr -d '\r' < $f); then r="같음 (CR 만 다름 · Windows CRLF 고정물)"; else r=다름; fi
  echo "$d/$(basename $b): 실제 awk 시험 덱 ↔ Codex 전사 = $r · run 줄: $(grep -nE '^ *run |^[0-9]+$' $TMP/t.liggghts | tail -3 | tr '\n' ' ')" >> $H/awk_trial/table.txt
done; done
mkdir -p $TMP/W/restart_pse_r075_a; : > $TMP/W/plate_pse_r075_a_r30.stl; : > $TMP/W/restart_pse_r075_a/restart_compress_1500000.bin
bash $TOOL -C docs/data/pure_se_r075_20260927/input_pse_r075_a.liggghts docs/data/pure_se_r075_20260927/input_pse_r075_a_r30.liggghts restart_pse_r075_a/restart_compress_1500000.bin 1500000 $TMP/W > $H/r075_bash_C/out.txt 2>&1
echo "rc=$?" >> $H/r075_bash_C/out.txt
