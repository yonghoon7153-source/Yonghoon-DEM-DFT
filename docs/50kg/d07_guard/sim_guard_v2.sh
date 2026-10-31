# sim_guard_v2.sh — d07_guard_v2.sh 흉내 시험 (가짜 HOME · 가짜 scancel/squeue/sleep · LIGGGHTS · SLURM 없음)
#   bash sim_guard_v2.sh <guard_v2.sh> <장면> [fill]
#   fill = 승인값 네 줄 (OLDATT= · OKR= · OKL= · OKD=) 을 줄째 흉내 값으로 바꿔 돌린다 (채우기 전 판 · 채운 판 둘 다) · 없으면 주어진 판 그대로
#     (unfilled · partialfill* · lmpdup 은 fill 여부와 상관없이 그 장면의 값을 넣는다)
#   세계 = 10-31 -T 뒤 실제와 같게:
#     멈춘 폴더 kg50_d07_b50.main1031 = 원 로그 + 물려받은 시도 attempt_r56_1030_152123_2568313 (10-30 본 호출 기록 · 영수증 29ff619a… · 시험 job 333908 · 본 job 333911)
#     작업 폴더 kg50_d07_b50 = 멈춘 폴더 cp -a · 원 로그 → log.liggghts.main1031 · -T 시도 attempt_r56_1031_220500_1111 (영수증 다섯 줄 · 시험 job 333999 · 결정: 시험만 (-T))
#     영수증 · 신원 줄 = 도구와 같은 꼴 (resume_ckpt.sh 의 sha256sum 다섯 줄 '<sha>  <실제 경로>' · runnerck render() 의 echo 문자열) · 경로 = 작업 폴더 실제 경로 (cd -P)
#   흉내 도구 (창 A) = 실제 본 호출 흐름: 작업 폴더 → kg50_d07_b50.prev_1031_230000 로 밀기 → 멈춘 폴더 cp -a (물려받은 시도가 다시 생김 · -T 시도는 밀린 폴더로)
#     → 새 시도 → 영수증 → 시험 job 444444 → (지킴이가 시험을 취소했으면 결정: 본 제출 안 함) → 결정 · 본 job 555555 → 신원 줄 · inherit 만 밀지 않고 그 자리에
#   장면 (기대 = results.txt):
#     옛     happy recdiff lmpdiff reject cmpdiff twonew early jobgone unfilled
#     새     deckdiff ckpdiff mismatch partialfill partialfill_att partialfill_lmp partialfill_upper partialfill_short realfmt inherit inherit2 move
#     덧붙임 tdeck tckp trec lmpdup jobfail
set -u
GRD=$1; SC=$2; FILL=${3:-}
SIM=$(mktemp -d); H=$SIM/home; B=$SIM/bin; mkdir -p $H $B
# realfmt: HOME 아래 dem_test 가 링크 (ibb 처럼 실제 경로 /lustre/… ≠ $HOME/…) — 영수증 · 신원 줄은 실제 경로
if [ "$SC" = realfmt ]; then mkdir -p $SIM/lustre/home/yonghoon/dem_test; ln -s $SIM/lustre/home/yonghoon/dem_test $H/dem_test; else mkdir -p $H/dem_test; fi
L=$H/dem_test; mkdir -p $L/logs
C=kg50_d07_b50; SUF=main1031; S=$L/$C.$SUF; W=$L/$C
INHERIT=attempt_r56_1030_152123_2568313; OLDATT=attempt_r56_1031_220500_1111; NEWATT=attempt_r56_1031_230000_4242
h(){ printf '%s' "$1" | sha256sum | cut -c1-64; }
LMP=$(h lmp); DECK=$(h deck); RUN=$(h run); TDK=$(h tdeck); TRN=$(h trun)
CKP=45a838c18d19e3c1399a97f5948d52ad0995490f6a55040e6a6ffec8fecd2d70
LMPP=$SIM/opt/lmp_mpi; [ "$SC" = realfmt ] && LMPP=/home/yonghoon/LIGGGHTS-PUBLIC/src/lmp_mpi
# 세계의 실제 덱 · 체크포인트 sha256 — tdeck · tckp 만 승인값과 다른 세계 (보고의 영수증 sha256 은 그 세계 그대로)
DECKW=$DECK; CKPW=$CKP
[ "$SC" = tdeck ] && DECKW=$(h deck2)
[ "$SC" = tckp ] && CKPW=$(h ckp2)
# 멈춘 폴더 (10-30 본 job 333911 의 작업 폴더를 10-31 에 이 이름으로 옮긴 것)
mkdir -p $S/restart_$C $S/post_$C $S/$INHERIT
printf 'LIGGGHTS log (흉내)\n====== SETTLING COMPLETE ======\n  200001   488285\n' > $S/log.liggghts
IA=$S/$INHERIT
cat > $IA/main_inputs.sha256 <<'EOF'
8e129f421a8491975f83527f79c8418318b2af30baeedd7440cfcede2d45c5e5  /lustre/home/yonghoon/dem_test/kg50_d07_b50/input_kg50_d07_b50_r56.liggghts
aad9ac227a3d5dec24dd0515f262299d81a4da283112dfb0cdf42e0b5e379750  /lustre/home/yonghoon/dem_test/kg50_d07_b50/run_kg50_d07_b50_r56.sh
94db4187093b417468ac7a2da6a0b43e5312e04507539251be45cbe2b8011ea1  /lustre/home/yonghoon/dem_test/kg50_d07_b50/input_kg50_d07_b50_r56t.liggghts
c00746e68b8420b45d41ec2a6a20dc72161f9974cc6a30a403b994991e24146f  /lustre/home/yonghoon/dem_test/kg50_d07_b50/run_kg50_d07_b50_r56t.sh
aa833368651d9bf811c7b39331149ca939bfedf1bbe0511e2d66bf329fde15a8  /lustre/home/yonghoon/dem_test/kg50_d07_b50/restart_kg50_d07_b50/restart_settling_20001.bin
EOF
echo 333908 > $IA/job_t.txt; echo 333911 > $IA/main_job.txt; echo 333908 > $S/job_r56t.txt
printf 'G0 1 G1 1 G2 1 G3 1 · 시험 job 333908 · 로그 output_kg50_d07_b50_r56t_333908.out · 잡 안 덱 신원 1 (G0 에 듦)\n결정: 본 제출 job 333911\n' > $IA/result.txt
echo 'LMP_IDENTITY (10-30 KG50R-F02): lmp_mpi=/home/yonghoon/LIGGGHTS-PUBLIC/src/lmp_mpi sha256=ee2d77261bac9e7fa4e9311c8709e74bf7583a13225a5bc35a791bef9be60a3f deck=/lustre/home/yonghoon/dem_test/kg50_d07_b50/input_kg50_d07_b50_r56.liggghts sha256=8e129f421a8491975f83527f79c8418318b2af30baeedd7440cfcede2d45c5e5 checkpoint=/lustre/home/yonghoon/dem_test/kg50_d07_b50/restart_kg50_d07_b50/restart_settling_20001.bin sha256=aa833368651d9bf811c7b39331149ca939bfedf1bbe0511e2d66bf329fde15a8' > $L/logs/output_${C}_r56_333911.out
# 10-31 -T 호출이 만든 작업 폴더 (멈춘 폴더 cp -a · 원 로그 이름 바꿈 · -T 시도)
cp -a $S $W; mv $W/log.liggghts $W/log.liggghts.$SUF
WR=$(cd -P $W && pwd -P)
rec(){ printf '%s  %s\n' "$1" "$WR/input_${C}_r56.liggghts" "$2" "$WR/run_${C}_r56.sh" "$TDK" "$WR/input_${C}_r56t.liggghts" "$TRN" "$WR/run_${C}_r56t.sh" "$3" "$WR/restart_$C/restart_after_settling.bin"; }
idl(){ printf 'LMP_IDENTITY (10-30 KG50R-F02): lmp_mpi=%s sha256=%s deck=%s sha256=%s checkpoint=%s sha256=%s\n' "$LMPP" "$1" "$WR/input_${C}_r56.liggghts" "$2" "$WR/restart_$C/restart_after_settling.bin" "$3"; }
mml(){ printf 'LMP_IDENTITY_MISMATCH (10-30 KG50R-F02): deck %s sha256 %s (checked %s) checkpoint %s sha256 %s (checked %s) - mpirun not started\n' "$WR/input_${C}_r56.liggghts" "$1" "$2" "$WR/restart_$C/restart_after_settling.bin" "$3" "$4"; }
rec "$DECKW" "$RUN" "$CKPW" > $SIM/rec.txt
REC_SHA=$(sha256sum < $SIM/rec.txt | cut -c1-64)
TA=$W/$OLDATT; mkdir $TA; cp $SIM/rec.txt $TA/main_inputs.sha256; echo 333999 > $TA/job_t.txt
printf 'G0 1 G1 1 G2 1 G3 1 · 시험 job 333999 · 로그 output_kg50_d07_b50_r56t_333999.out · 잡 안 덱 신원 1 (G0 에 듦)\n결정: 시험만 (-T)\n' > $TA/result.txt
# 장면별 세계 (지킴이 전)
[ "$SC" = trec ] && echo "$TDK  $WR/extra_after_report" >> $TA/main_inputs.sha256   # -T 보고 (영수증 sha256) 뒤 -T 영수증이 바뀜
[ "$SC" = cmpdiff ] && echo extra >> $W/log.liggghts.$SUF
[ "$SC" = early ] && mkdir $W/attempt_r56_1031_225959_7777
[ "$SC" = inherit2 ] && rm -rf $W/$INHERIT   # 작업 폴더에서만 지움 (멈춘 폴더에는 그대로 — 본 호출 복사가 다시 데려온다)
# 승인값 (흉내)
VA=$OLDATT; VR=$REC_SHA; VL=$LMP; VD=$DECK; DOFILL=$FILL
case "$SC" in
  unfilled) VA=__FILL_T_ATTEMPT__; VR=__FILL_RECEIPT_SHA256__; VL=__FILL_LMP_SHA256__; VD=__FILL_DECK_SHA256__; DOFILL=1;;
  partialfill) VL=__FILL_LMP_SHA256__; VD=__FILL_DECK_SHA256__; DOFILL=1;;
  partialfill_att) VA=__FILL_T_ATTEMPT__; DOFILL=1;;
  partialfill_lmp) VL=__FILL_LMP_SHA256__; DOFILL=1;;
  partialfill_upper) VL=$(printf '%s' "$LMP" | tr a-f A-F); DOFILL=1;;
  partialfill_short) VL=${LMP:0:63}; DOFILL=1;;
  lmpdup) VL=$DECK; DOFILL=1;;
esac
if [ -n "$DOFILL" ]; then
  sed -e "s|^OLDATT=.*|OLDATT=$VA|" -e "s|^OKR=.*|OKR=$VR|" -e "s|^OKL=.*|OKL=$VL|" -e "s|^OKD=.*|OKD=$VD|" $GRD > $H/d07_guard_v2.sh
else cp $GRD $H/d07_guard_v2.sh; fi
# 가짜 scancel · squeue · sleep (첫 줄 없음 = bash 가 셸 스크립트로 돌린다)
cat > $B/scancel <<'EOF'
echo "$*" >> "$SIMDIR/scancel.log"; rm -f "$SIMDIR/running_$1"
EOF
cat > $B/squeue <<'EOF'
j=""; while [ $# -gt 0 ]; do [ "$1" = -j ] && j=$2; shift; done
if [ -n "$j" ] && [ -e "$SIMDIR/state_$j" ]; then cat "$SIMDIR/state_$j"; elif [ -n "$j" ] && [ -e "$SIMDIR/running_$j" ]; then echo RUNNING; fi
exit 0
EOF
cat > $B/sleep <<'EOF'
/bin/sleep 0.05
EOF
chmod +x $B/*
export SIMDIR=$SIM
tool(){
  for i in $(seq 1 400); do grep -q '이제 창 A' $SIM/out.txt 2>/dev/null && break; [ -e $SIM/done ] && return 0; /bin/sleep 0.05; done
  grep -q '이제 창 A' $SIM/out.txt 2>/dev/null || return 0
  if [ "$SC" = inherit ]; then /bin/sleep 0.5          # 밀지 않음 — 물려받은 시도 (job_t 333908) 와 -T 시도가 있는 채로 0.5 s
  else
    mv $W $L/$C.prev_1031_230000; cp -a $S $W; mv $W/log.liggghts $W/log.liggghts.$SUF
    case "$SC" in move|inherit2) /bin/sleep 0.5;; esac  # 작업 폴더에 물려받은 시도만 있는 창 (다시 생긴 폴더 · ibb 의 큰 cp -a 가 끝나기 전과 같다)
  fi
  A=$W/$NEWATT; mkdir $A; echo '도구 신원 (흉내)' > $A/tool.txt; /bin/sleep 0.3
  if [ "$SC" = recdiff ]; then rec "$DECKW" "$(h run2)" "$CKPW" > $A/main_inputs.sha256; else cp $SIM/rec.txt $A/main_inputs.sha256; fi
  [ "$SC" = twonew ] && mkdir $W/attempt_r56_1031_230001_9999
  echo 444444 > $A/job_t.txt; touch $SIM/running_444444; /bin/sleep 0.5
  if [ -e $SIM/running_444444 ]; then :; else printf 'G0 0 G1 0 G2 0 G3 0 · 시험 job 444444 (취소됨)\n결정: 본 제출 안 함 (G0–G3)\n' > $A/result.txt; return 0; fi
  if [ "$SC" = reject ]; then rm -f $SIM/running_444444; printf 'G0 1 G1 0 G2 1 G3 1 · 시험 job 444444\n결정: 본 제출 안 함 (G0–G3)\n' > $A/result.txt; return 0; fi
  rm -f $SIM/running_444444; echo 555555 > $A/main_job.txt; touch $SIM/running_555555
  printf 'G0 1 G1 1 G2 1 G3 1 · 시험 job 444444 · 로그 output_%s_r56t_444444.out · 잡 안 덱 신원 1 (G0 에 듦)\n결정: 본 제출 job 555555\n' $C > $A/result.txt
  /bin/sleep 0.5
  IL=$LMP; ID=$DECKW; IK=$CKPW
  [ "$SC" = lmpdiff ] && IL=$(h lmp2)
  [ "$SC" = deckdiff ] && ID=$(h deck3)
  [ "$SC" = ckpdiff ] && IK=$(h ckp3)
  case "$SC" in jobgone|mismatch) rm -f $SIM/running_555555;; jobfail) echo FAILED > $SIM/state_555555;; esac   # 신원 줄 전에 순서를 고정
  { idl "$IL" "$ID" "$IK"
    if [ "$SC" = mismatch ]; then mml "$ID" "$(h deck4)" "$IK" "$IK"; else echo 'LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0 흉내)'; fi
  } > $L/logs/output_${C}_r56_555555.out
  return 0
}
tool &
HOME=$H PATH=$B:$PATH timeout 40 bash $H/d07_guard_v2.sh > $SIM/out.txt 2>&1; RC=$?
touch $SIM/done; wait 2>/dev/null
echo "[$SC] rc=$RC · scancel: $(cat $SIM/scancel.log 2>/dev/null | tr '\n' ' ')"
sed 's/^/    /' $SIM/out.txt | cut -c1-300
rm -rf $SIM
