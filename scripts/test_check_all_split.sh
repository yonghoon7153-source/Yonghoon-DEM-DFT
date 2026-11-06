#!/usr/bin/env bash
# 게이트 나누기 시험 — `CHECK_ALL_RANGE` · `CHECK_ALL_LIST` · `CHECK_ALL_TIMES` (scripts/check_all.sh).
#
# ★ 왜 (1저자 11-06 (가) — 게이트를 나눠 돌린다 · *"이런건 권고 안받고 (가) 처럼하면돼"*):
#   게이트 (check_all.sh 전체) 가 11-05 에 Bash 백그라운드 한도 2 h 에서 두 번 잘렸다 (122 ✓ · 126 ✓ 에서 끊김 · ✗ 0).
#   단계를 줄이지 않고 (1저자 10-21 *"줄이지는 말고"*) 같은 단계를 순서대로 나눠 같은 HEAD 에서 차례로 돌린다.
#   push 판정 = 나눈 부분이 모두 같은 HEAD · 깨끗한 트리에서 끝나고 · 범위가 1..N 을 빈틈 · 겹침 없이 덮고 · ✗ 0.
#
# ★ 고치기 전 check_all.sh 에는 이 세 변수가 없다 → 어떤 시험이든 게이트 전체를 돌기 시작해 시간 한도에 걸린다 = 실패.
#
#   bash scripts/test_check_all_split.sh
set -uo pipefail
cd "$(dirname "$0")/.."
CA=scripts/check_all.sh
PASS=0; NG=0
ok() { printf '  ✓ %s\n' "$1"; PASS=$((PASS+1)); }
ng() { printf '  ✗ %s\n' "$1"; NG=$((NG+1)); }
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
TAB=$(printf '\t')
#  바깥 게이트가 나눠 도는 중이면 (이 시험이 그 한 단계) 바깥 변수가 안으로 샌다 → 시험 안의 호출은 늘 깨끗한 환경에서 시작한다.
ca() { env -u CHECK_ALL_RANGE -u CHECK_ALL_LIST -u CHECK_ALL_TIMES "$@" timeout -k 5 15 bash "$CA"; }

#  기대 단계 수 = 원문의 `run '…'` 호출 수 − (node 가 없으면 node 블록 안의 호출 수)
n_src=$(grep -c -E "^[[:space:]]*run '" "$CA")
n_node=$(awk '/^if command -v node/{f=1} f && /^[[:space:]]*run '"'"'/{c++} f && /^fi$/{f=0} END{print c+0}' "$CA")
if command -v node >/dev/null 2>&1; then n_exp=$n_src; else n_exp=$((n_src - n_node)); fi

echo "── 게이트 나누기 시험 (기대 단계 수 $n_exp · 원문 run $n_src · node 블록 $n_node) ──"

# T1 목록 모드 = 돌리지 않고 번호 · 이름만 · 15 s 안에 끝난다 · 1..N 빈틈 없음
ca CHECK_ALL_LIST=1 > "$TMP/list.txt" 2>&1; rc=$?
n_list=$(grep -c -E "^[0-9]+${TAB}" "$TMP/list.txt")
contig=$(grep -E "^[0-9]+${TAB}" "$TMP/list.txt" | cut -f1 | awk 'BEGIN{e=1;ok=1} {if ($1+0 != e) ok=0; e++} END{print ok}')
if [ "$rc" = 0 ] && [ "$n_list" = "$n_exp" ] && [ "$contig" = 1 ] \
   && ! grep -q -E '^  [✓✗] ' "$TMP/list.txt"; then
  ok "T1 목록 모드 = 단계 $n_list 개 · 번호 1..$n_list 빈틈 없음 · 실행 0 (rc $rc)"
else
  ng "T1 목록 모드 (rc $rc · 목록 $n_list · 기대 $n_exp · 연속 $contig)"
fi

# T2 범위 형식이 틀리면 rc 2 · 아무 단계도 돌지 않는다
for bad in 'abc' '5' '0-3' '7-3' '3-x' '-5' '1-2-3' ' 1-2' '1-2 ' '٣-٤' '1-' '-'; do
  ca CHECK_ALL_RANGE="$bad" > "$TMP/bad.txt" 2>&1; rc=$?
  if [ "$rc" = 2 ] && ! grep -q -E '^  [✓✗] ' "$TMP/bad.txt"; then
    ok "T2 틀린 범위 '$bad' = rc 2 · 실행 0"
  else
    ng "T2 틀린 범위 '$bad' (rc $rc)"
  fi
done

# T3 범위가 단계 수 N 밖이면 돌리기 전에 거른다 (rc 2 · 실행 0) — N 은 시작 때 목록 모드로 센다
ca CHECK_ALL_RANGE=99999-99999 > "$TMP/empty.txt" 2>&1; rc=$?
if [ "$rc" = 2 ] && ! grep -q -E '^  [✓✗] ' "$TMP/empty.txt"; then
  ok "T3 범위 시작 > N = rc 2 · 실행 0 (빈 부분이 초록으로 나오지 않는다)"
else
  ng "T3 범위 시작 > N (rc $rc)"
fi

# T4 한 단계 범위 (1-1 = run_contract --selftest · 1 s 안) = 그 단계 하나만 돈다 · 요약 줄 · 시간 기록
ca CHECK_ALL_RANGE=1-1 CHECK_ALL_TIMES="$TMP/t.tsv" > "$TMP/one.txt" 2>&1; rc=$?
n_ok=$(grep -c -E '^  ✓ ' "$TMP/one.txt"); n_ng=$(grep -c -E '^  ✗ ' "$TMP/one.txt")
lbl1=$(grep -E "^1${TAB}" "$TMP/list.txt" | cut -f2-)
if [ "$rc" = 0 ] && [ "$n_ok" = 1 ] && [ "$n_ng" = 0 ] \
   && grep -q -F "  ✓ $lbl1" "$TMP/one.txt" \
   && grep -q -E "^CHECK_ALL_PART range=1-1 total=${n_exp} ran=1 fail=0\$" "$TMP/one.txt" \
   && [ "$(wc -l < "$TMP/t.tsv")" = 1 ] \
   && grep -q -E "^1${TAB}[0-9]+${TAB}ok${TAB}" "$TMP/t.tsv" \
   && ! grep -q -F '전부 통과' "$TMP/one.txt"; then
  ok "T4 범위 1-1 = 단계 1 하나 ✓ · total=$n_exp ran=1 · 시간 기록 한 줄 · '전부 통과' 문구 없음"
else
  ng "T4 범위 1-1 (rc $rc · ✓ $n_ok · ✗ $n_ng)"
fi

# T5 목록 모드는 범위를 무시하고 전부 낸다 (나누기 계획은 늘 전체에서 세운다)
ca CHECK_ALL_LIST=1 CHECK_ALL_RANGE=3-4 > "$TMP/list2.txt" 2>&1; rc=$?
n_list2=$(grep -c -E "^[0-9]+${TAB}" "$TMP/list2.txt")
if [ "$rc" = 0 ] && [ "$n_list2" = "$n_exp" ]; then
  ok "T5 목록 + 범위 = 그래도 전부 $n_list2 개"
else
  ng "T5 목록 + 범위 (rc $rc · $n_list2)"
fi

# T6 범위 끝이 N 을 넘으면 거부 (rc 2) — 나눈 부분의 끝을 잘못 적어 마지막 단계를 빠뜨리는 것과 구별하려고 정확한 N 까지만 받는다
ca CHECK_ALL_RANGE="1-$((n_exp + 1))" > "$TMP/over.txt" 2>&1; rc=$?
if [ "$rc" = 2 ] && ! grep -q -E '^  [✓✗] ' "$TMP/over.txt"; then
  ok "T6 범위 끝 N+1 = rc 2 · 실행 0"
else
  ng "T6 범위 끝 N+1 (rc $rc)"
fi

echo
echo "게이트 나누기 시험: $PASS 통과 · $NG 실패"
[ "$NG" = 0 ]
