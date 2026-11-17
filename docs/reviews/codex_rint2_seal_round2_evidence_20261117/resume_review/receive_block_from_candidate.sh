cd ~/sdcp && umask 022
T=<넘김 기록 시각>; FROM=kgy; TO=gabia; BR=<원장 가지>; RB=~/sdcp/ca1_relay/${T}_${FROM}_to_${TO}.bundle
sha256sum "$RB"                                                     # = 넘김 기록
git bundle list-heads "$RB" | grep "refs/heads/$BR"                 # 커밋 = 넘김 기록의 원장 끝 커밋
if [ -d ca1_ledger.parked ]; then git -C ca1_ledger.parked -c pull.rebase=false pull -q --ff-only "$RB" "$BR" && mv ca1_ledger.parked ca1_ledger; else git clone -q -b "$BR" "$RB" ca1_ledger; fi
test "$(git -C ca1_ledger rev-parse HEAD)" = <넘김 기록의 원장 끝 커밋> && echo RECV_OK   # RECV_OK 가 없으면 멈추고 1저자 (사슬을 띄우지 않는다)
