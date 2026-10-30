#!/bin/bash
set -u
export PATH=/usr/bin:/bin
W='/c/Users/Administrator/Documents/Codex/d07scope30/independent/gate_probe/new_call_unreviewed_duration'
AD='/c/Users/Administrator/Documents/Codex/d07scope30/independent/gate_probe/new_call_unreviewed_duration/attempt'
REP='/c/Users/Administrator/Documents/Codex/d07scope30/independent/gate_probe/new_call_unreviewed_duration/report.md'
SELF='/c/Users/Administrator/Documents/Codex/d07scope30/repo/scripts/resume_ckpt.sh'
HELPER='/c/Users/Administrator/Documents/Codex/d07scope30/independent/gate_probe/new_call_unreviewed_duration/FAKE_helper.py'
APT='2dc7f693263708d7788ab721386182c6109a8f9278797ecc43f5165d6715f1e8'
APH='24625186aed5d432300c2c1d12d406375e3249b73a6920c01b15140393f979d8'
MIS='819b6d01d3e54f88d45a90beda5897275a6797b8d908b393fd76f4befb8fba41'
C='kg50_d07_b50'
SFX='r56'
ATT='attempt'
J='333858'
TONLY='0'
G0='1'
G1='1'
G2='1'
G3='1'
USER='review_fixture'
CALLS='/c/Users/Administrator/Documents/Codex/d07scope30/independent/gate_probe/new_call_unreviewed_duration/fake_sbatch_calls.txt'
REVIEWED_RECEIPT='7b845f6574142d86903b646b1d0ac7ab6866f43ec96ed1642d34a5e929860bcc'
ACK_REVIEWED_RECEIPT='0'
squeue(){ return 0; }
qre(){ printf "%s" "$1"; }
sbatch(){ printf "%s\n" "$*" >> "$CALLS"; printf "900001\n"; }
for once in 1; do
  if [ $G0 = 1 ] && [ $G1 = 1 ] && [ $G2 = 1 ] && [ $G3 = 1 ]; then
    if [ $TONLY = 1 ]; then echo "- 🧪 시험만 (-T) — G0–G3 통과 · 본 제출 안 함" >> $REP; echo "결정: 시험만 (-T)" >> $AD/result.txt; TPASS="$TPASS $C"
    else
      # 10-28 밤 (KG50R-04 · Q4): 본 제출 바로 전 — 그 케이스 잡 다시 (이번 시험 job 은 뺀다 · 조회 실패 = 안 냄) · 도구 sha256 다시 · 이 시도가 이미 냈는지
      BLK=""
      QL2=$(squeue -u $USER -h -o '%i %j' 2>/dev/null) || BLK="본 제출 직전 squeue 조회 실패 (돌고 있는지 모른다)"
      if [ -z "$BLK" ]; then BZ=$(printf '%s\n' "$QL2" | awk -v j="$J" 'NF>=2 && $1!=j {print $2}' | grep -xE "$(qre $C)" | tr '\n' ' ')
        [ -n "$BZ" ] && BLK="본 제출 직전 큐에 그 케이스 잡: ${BZ}(이번 시험 $J 은 뺌)"; fi
      T2=$(sha256sum < "$SELF" 2>/dev/null | cut -c1-64); H2=$(sha256sum < $HELPER 2>/dev/null | cut -c1-64)
      [ -z "$BLK" ] && { [ "$T2" != "$APT" ] || [ "$H2" != "$APH" ]; } && BLK="도구 sha256 이 승인값과 다름 — 지금 resume_ckpt.sh ${T2:-없음} · dem_restart.py ${H2:-없음}"
      [ -z "$BLK" ] && [ -e $AD/main_job.txt ] && BLK="이 시도는 이미 본 제출함 (job $(cat $AD/main_job.txt))"
      # 10-30 (KG50R-F02 · 1저자 Q2 (3)): 실행 입력 다섯 (재개 덱 · 러너 · 시험 덱 · 시험 러너 · 체크포인트) 전부 다시 + 영수증 파일 자체가 시험 전에
      #   이 호출이 쓴 그것 (메모리 sha256 · sha256sum -c 만으로는 줄이 빠지거나 덧붙은 영수증도 통과) — 하나라도 다르면 본 제출 안 함
      [ -z "$BLK" ] && [ "$(sha256sum < $AD/main_inputs.sha256 2>/dev/null | cut -c1-64)" != "$MIS" ] \
        && BLK="실행 입력 영수증 $ATT/main_inputs.sha256 이 시험 전에 이 호출이 쓴 것과 다름 (10-30 KG50R-F02 · 메모리 sha256 ${MIS:-없음})"
      [ -z "$BLK" ] && ! CKO=$(sha256sum -c --quiet $AD/main_inputs.sha256 2>&1) \
        && BLK="실행 입력 (재개 덱 · 러너 · 시험 덱 · 시험 러너 · 체크포인트) 이 시험 때와 다름 (sha256 ≠ $ATT/main_inputs.sha256 · 10-28 사전 공격 C · 10-30 KG50R-F02): $(printf '%s' "$CKO" | tr '\n' ' ' | cut -c1-600)"
      if [ -n "$BLK" ]; then echo "- ⛔ 본 제출 안 함 (10-28 KG50R-04) — $BLK" >> $REP; echo "결정: 본 제출 안 함 — $BLK" >> $AD/result.txt
      else echo "- 본 제출 직전 다시 확인 (10-28 KG50R-04 · Q4): 큐에 그 케이스 잡 없음 (이번 시험 $J 뺌) · 도구 sha256 = 승인값 · 실행 입력 다섯 sha256 = 영수증 · 영수증 = 이 호출이 쓴 것 (10-30 KG50R-F02)" >> $REP
        # 10-28 밤 2 (사전 공격 D): 본 sbatch 도 시험 쪽 (Q9d) 과 같은 규칙 — 종료 코드 0 · 숫자 job 번호 ('id' 또는 'id;cluster') 일 때만 ✅
        JM=$(sbatch --parsable $W/run_${C}_$SFX.sh); JMR=$?
        if [ $JMR = 0 ] && [[ "$JM" =~ ^([0-9]+)(;[^[:space:]]*)?$ ]]; then JM=${BASH_REMATCH[1]}
          echo "- ✅ 본 제출 job $JM (run_${C}_$SFX.sh, 제출 폴더 $L)" >> $REP; echo "$JM" > $AD/main_job.txt; echo "결정: 본 제출 job $JM" >> $AD/result.txt
        else JX=$(printf '%s' "$JM" | tr '\n' ' ' | cut -c1-300)
          echo "- ⛔ 본 제출 실패 (sbatch 종료 코드 $JMR · 출력 [$JX] · job 번호 꼴 아님 · 10-28 사전 공격 D — 큐를 손으로 확인)" >> $REP
          echo "결정: 본 제출 실패 — sbatch 종료 코드 $JMR · 출력 [$JX]" >> $AD/result.txt; fi
      fi
    fi
  else echo "- ⛔ 본 제출 안 함 — 위 G0/G1/G2/G3 확인 후 사람이 판단" >> $REP; echo "결정: 본 제출 안 함 (G0–G3)" >> $AD/result.txt; fi
done
