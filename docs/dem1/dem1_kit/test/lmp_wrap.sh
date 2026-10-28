#!/bin/bash
# 테스트 전용 lmp_mpi 래퍼: rcheck(-log none)·삽입 덱은 진짜로 · $INJECT_DIR/inject_error 있으면 본 런을 "ERROR:" 로, inject_silent 있으면 조용히 실패
REAL=@REAL@
case " $* " in *" -log none "*|*"_ins.liggghts"*) exec $REAL "$@";; esac
[ -e "$INJECT_DIR/inject_error" ] && { echo "ERROR: Lost atoms: original 2491 current 2490 (../thermo.cpp:395)"; exit 1; }
[ -e "$INJECT_DIR/inject_silent" ] && exit 1
exec $REAL "$@"
