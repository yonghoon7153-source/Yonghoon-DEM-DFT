#!/bin/bash
# D2 예 (ibb kg50_d2_b50 r4 · NP 4) — 고친 도구의 runnerck 함수를 글 그대로 떼어 모래 상자에서 돌린다 (판정 아님 · 러너 글 보기용)
#   모래 상자 = <SB>/lustre/home/yonghoon/dem_test/kg50_d2_b50 (실제 폴더) · <SB>/home/yonghoon → <SB>/lustre/home/yonghoon (링크 · ibb /home → /lustre 꼴)
#   인자: 작업트리 · 모래 상자 (빈 새 폴더)
WT=$1; SB=$2
TOOL=$WT/scripts/resume_ckpt.sh; DD=$WT/docs/data/kg50_resume_tests_20261027/d2_main_1028_0942
mkdir -p "$SB/lustre/home/yonghoon/dem_test/kg50_d2_b50" "$SB/home"
ln -s "$SB/lustre/home/yonghoon" "$SB/home/yonghoon"
W=$SB/home/yonghoon/dem_test/kg50_d2_b50; WR=$(cd -P "$W" && pwd -P)
cp "$DD/input_kg50_d2_b50_r4.liggghts" "$W/"; cp "$DD/input_kg50_d2_b50_r4t.liggghts" "$W/"
# 헬퍼 러너 = 받은 D2 러너 그대로, cd 만 모래 상자 실제 경로 (ibb 에서는 /lustre/home/yonghoon/dem_test/kg50_d2_b50)
sed "s#^cd /lustre/home/yonghoon/dem_test/kg50_d2_b50\$#cd $SB/lustre/home/yonghoon/dem_test/kg50_d2_b50#" "$DD/run_kg50_d2_b50_r4.sh" > "$W/run_kg50_d2_b50_r4.sh"
sed -n '/^runnerck(){ python3 -I - "\$@" <<'"'"'PY'"'"'$/,/^}$/p' "$TOOL" > "$SB/runnerck_fn.sh"
echo "runnerck 함수 줄 수: $(wc -l < "$SB/runnerck_fn.sh") · 도구 sha256 $(sha256sum < "$TOOL" | cut -c1-64)"
source "$SB/runnerck_fn.sh"
runnerck "$W/run_kg50_d2_b50_r4.sh" kg50_d2_b50 r4 4 "$W" "$WR" "$W/input_kg50_d2_b50_r4.liggghts" "$W/input_kg50_d2_b50_r4t.liggghts" \
  "$W/run_kg50_d2_b50_r4.sh" "$W/run_kg50_d2_b50_r4t.sh"
echo "runnerck rc=$?"
for f in run_kg50_d2_b50_r4.sh run_kg50_d2_b50_r4t.sh; do
  echo "===== $f (모래 상자 앞머리 $SB 를 지운 글 = ibb 에서 쓸 글)"
  sed "s#$SB##g" "$W/$f"
  echo "===== $f sha256 (모래 상자 글) $(sha256sum < "$W/$f" | cut -c1-64)"
done
