#!/usr/bin/env bash
# 믹서 고-Bo 강성 축 — DEV 덱 · 되읽기 증거 재생성 (2026-09-30)
#   사전등록 docs/reviews/mixer_highbo_stiffness_prereg_20260929.md §2 · §3 · §8-2 (DEV7) · Codex 9 차 §3 (표 B · 표 E) · §6-2
#   ⛔ 시뮬레이션 · ibb · WSL 실행 없음 — 덱 생성 (생성기 CLI) · 무입자 검사 (되읽기 · 덱 비교) 만.
#
#   리포 루트에서:   bash docs/data/mixer_highbo_dev_decks_20260930/build.sh
#   재현 확인:       (같은 명령 뒤) sha256sum -c docs/data/mixer_highbo_dev_decks_20260930/SHA256SUMS
#
#   폴더
#     decks/       DEV 실행 대상 7 (E0_ref ×3 seed · E0_ref2 · E0_ref_dthalf · LC_ref_r2 · LH_ref_r2) — 다음 단계 (런처 dev 정책) 입력
#     compare/     soft 대조 전용 5 (현 생성기 기본 — E0 셋은 09-28 에 실행된 덱과 바이트 동일) — 실행 대상 아님
#     check_only/  ×28 LC · LH 2 바퀴 — 비영 CED 의 ×28 덱 검산 전용 (Codex 9 차 §6-2) — 실행 대상 아님
#   각 덱 폴더: in.mixer · gen_cmd.txt (정확한 생성 명령) · gen.log · deck_meta.json (경화 · dt 덱만 — 생성기가 쓴다)
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT" || exit 2
D=docs/data/mixer_highbo_dev_decks_20260930
BASE="--n-total 100000 --cgf 151.4"                       # gen_all.sh 기본 (N_TOTAL · CGF) · rpm = --fr 기본 (Fr 0.0827) 에서 유도
REF="--stiffen-se 14 --hold-bo-pairwise"                  # 사전등록 §3 E_ref
REF2="--stiffen-se 28 --hold-bo-pairwise"                 # 사전등록 §3 E_ref2 (개발 · 진단 전용)
TMP=$(mktemp -d) || exit 2
trap 'rm -rf "$TMP"' EXIT
RC=0

gen() {  # gen <하위폴더/이름> <생성기 인자…> — 덱 · 명령 · 로그.  같은 명령을 임시 폴더에 한 번 더 돌려 in.mixer 바이트 동일 (재현) 확인
  local rel="$1"; shift
  local out="$D/$rel"
  rm -rf "$out"; mkdir -p "$out"
  local cmd="python3 scripts/make_mixer_deck.py --out $out $BASE $*"
  echo "$cmd" > "$out/gen_cmd.txt"
  if ! $cmd > "$out/gen.log" 2>&1; then echo "⛔ 생성 실패: $rel"; cat "$out/gen.log"; exit 1; fi
  rmdir "$out/data" 2>/dev/null || true                   # 3 상 덱은 섬유 파일이 없어 data/ 가 빈 폴더
  python3 scripts/make_mixer_deck.py --out "$TMP/$rel" $BASE "$@" > /dev/null 2>&1 || { echo "⛔ 재생성 실패: $rel"; exit 1; }
  if cmp -s "$out/in.mixer" "$TMP/$rel/in.mixer"; then echo "✓ $rel  $(sha256sum "$out/in.mixer" | cut -c1-16)  (재생성 바이트 동일)"
  else echo "⛔ $rel — 같은 명령의 재생성 덱이 다르다"; RC=1; fi
}

echo "── 덱 생성 (생성기 $(sha256sum scripts/make_mixer_deck.py | cut -c1-16)) ──"
gen decks/E0_ref_s32452843          --arm E0 --seed 32452843 --revolutions 0 $REF
gen decks/E0_ref_s49979687          --arm E0 --seed 49979687 --revolutions 0 $REF
gen decks/E0_ref_s67867967          --arm E0 --seed 67867967 --revolutions 0 $REF
gen decks/E0_ref2_s32452843         --arm E0 --seed 32452843 --revolutions 0 $REF2
gen decks/E0_ref_dthalf_s32452843   --arm E0 --seed 32452843 --revolutions 0 $REF --dt-factor 0.5
gen decks/LC_ref_r2_s32452843       --arm LC --seed 32452843 --revolutions 2 $REF
gen decks/LH_ref_r2_s32452843       --arm LH --seed 32452843 --revolutions 2 $REF
gen compare/E0_soft_s32452843       --arm E0 --seed 32452843 --revolutions 0
gen compare/E0_soft_s49979687       --arm E0 --seed 49979687 --revolutions 0
gen compare/E0_soft_s67867967       --arm E0 --seed 67867967 --revolutions 0
gen compare/LC_soft_r2_s32452843    --arm LC --seed 32452843 --revolutions 2
gen compare/LH_soft_r2_s32452843    --arm LH --seed 32452843 --revolutions 2
gen check_only/LC_ref2_r2_s32452843 --arm LC --seed 32452843 --revolutions 2 $REF2
gen check_only/LH_ref2_r2_s32452843 --arm LH --seed 32452843 --revolutions 2 $REF2

#  ★ soft E0 셋 = 09-28 에 실제로 돈 E0 덱 (docs/data/mixer_e0_contract_20260928/README.md 의 기대 덱 sha256 앞 16 자리)
echo "── soft E0 = 09-28 실행 덱 (기대 sha256 앞 16) ──"
for pair in 32452843:a38cdc7494671979 49979687:b8ba25ace11e1300 67867967:f38f0093433d251a; do
  sd=${pair%%:*}; want=${pair##*:}
  got=$(sha256sum "$D/compare/E0_soft_s$sd/in.mixer" | cut -c1-16)
  if [ "$got" = "$want" ]; then echo "✓ E0_soft_s$sd  $got"; else echo "⛔ E0_soft_s$sd  $got ≠ $want"; RC=1; fi
done

echo "── 되읽기 (표 E · E0 · DT · B — 덱 텍스트만 · 생성기 import 없음) ──"
dk() { echo "$D/$1/in.mixer"; }
python3 scripts/mixer_deck_readback.py \
  --table E  "$(dk compare/LC_soft_r2_s32452843)"  "$(dk decks/LC_ref_r2_s32452843)" \
  --table E  "$(dk compare/LH_soft_r2_s32452843)"  "$(dk decks/LH_ref_r2_s32452843)" \
  --table E  "$(dk compare/LC_soft_r2_s32452843)"  "$(dk check_only/LC_ref2_r2_s32452843)" \
  --table E  "$(dk compare/LH_soft_r2_s32452843)"  "$(dk check_only/LH_ref2_r2_s32452843)" \
  --table E  "$(dk decks/LC_ref_r2_s32452843)"     "$(dk check_only/LC_ref2_r2_s32452843)" \
  --table E0 "$(dk compare/E0_soft_s32452843)"     "$(dk decks/E0_ref_s32452843)" \
  --table E0 "$(dk compare/E0_soft_s49979687)"     "$(dk decks/E0_ref_s49979687)" \
  --table E0 "$(dk compare/E0_soft_s67867967)"     "$(dk decks/E0_ref_s67867967)" \
  --table E0 "$(dk decks/E0_ref_s32452843)"        "$(dk decks/E0_ref2_s32452843)" \
  --table DT "$(dk decks/E0_ref_s32452843)"        "$(dk decks/E0_ref_dthalf_s32452843)" \
  --table B  "$(dk compare/LC_soft_r2_s32452843)"  "$(dk compare/LH_soft_r2_s32452843)" \
  --table B  "$(dk decks/LC_ref_r2_s32452843)"     "$(dk decks/LH_ref_r2_s32452843)" \
  --table B  "$(dk check_only/LC_ref2_r2_s32452843)" "$(dk check_only/LH_ref2_r2_s32452843)" \
  --json "$D/readback.json" --md "$D/readback.md" || RC=1

echo "── 덱 비교 mixer_deck_diff (--allow E · EB · B, --expect-deck = 같은 명령의 재생성 덱) ──"
: > "$D/deck_diff.txt"
DDJ=()
dd() {  # dd <허용> <기준 rel> <새 rel> — 기대 덱 = 새 덱을 같은 명령으로 재생성한 것 (gen 이 $TMP 에 만들어 둔 것)
  local allow="$1" a="$2" b="$3" js="$TMP/dd_${#DDJ[@]}.json"
  { echo; echo "### --allow $allow   $a → $b   (--expect-deck = 재생성 $b)"; } >> "$D/deck_diff.txt"
  python3 scripts/mixer_deck_diff.py "$(dk "$a")" "$(dk "$b")" --allow "$allow" --expect-deck "$TMP/$b/in.mixer" --json "$js" \
    >> "$D/deck_diff.txt" 2>&1 || RC=1
  DDJ+=("$allow|$a|$b|$js")
}
dd E  compare/LC_soft_r2_s32452843  decks/LC_ref_r2_s32452843
dd E  compare/LH_soft_r2_s32452843  decks/LH_ref_r2_s32452843
dd E  compare/E0_soft_s32452843     decks/E0_ref_s32452843
dd E  compare/E0_soft_s49979687     decks/E0_ref_s49979687
dd E  compare/E0_soft_s67867967     decks/E0_ref_s67867967
dd E  decks/E0_ref_s32452843        decks/E0_ref2_s32452843
dd E  decks/E0_ref_s32452843        decks/E0_ref_dthalf_s32452843
dd E  compare/LC_soft_r2_s32452843  check_only/LC_ref2_r2_s32452843
dd E  compare/LH_soft_r2_s32452843  check_only/LH_ref2_r2_s32452843
dd E  decks/LC_ref_r2_s32452843     check_only/LC_ref2_r2_s32452843
dd EB compare/LC_soft_r2_s32452843  decks/LH_ref_r2_s32452843
dd EB compare/LC_soft_r2_s32452843  check_only/LH_ref2_r2_s32452843
dd B  compare/LC_soft_r2_s32452843  compare/LH_soft_r2_s32452843
dd B  decks/LC_ref_r2_s32452843     decks/LH_ref_r2_s32452843
dd B  check_only/LC_ref2_r2_s32452843 check_only/LH_ref2_r2_s32452843
python3 - "$D/deck_diff.json" "${DDJ[@]}" <<'PY'
import hashlib, json, sys
out, rows = sys.argv[1], []
for spec in sys.argv[2:]:
    allow, a, b, js = spec.split('|')
    r = json.load(open(js, encoding='utf-8'))[0]
    rows.append(dict(allow=allow, ref=a, new=b, verdict=r['verdict'], e_case=r.get('e_case'), changed=r['changed'],
                     non_ced_diffs=r['non_ced_diffs'], e_rule=r.get('e_rule', []), missing=r['missing'],
                     wrong_direction=r['wrong_direction'], target_mismatch=r['target_mismatch']))
tool = 'scripts/mixer_deck_diff.py'
json.dump(dict(tool=tool, tool_sha256=hashlib.sha256(open(tool, 'rb').read()).hexdigest(),
               note='--expect-deck = 같은 생성 명령을 임시 폴더에 다시 돌린 덱 (E · EB 는 전 명령 토큰 동일 · B 는 CED 목표)',
               verdict='PASS' if all(r_['verdict'] == 'PASS' for r_ in rows) else 'FAIL', comparisons=rows),
          open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
open(out, 'a', encoding='utf-8').write('\n')
print(f"deck_diff: {sum(r_['verdict'] == 'PASS' for r_ in rows)}/{len(rows)} PASS → {out}")
PY
sed -i "s#$TMP#<재생성 임시 폴더>#g" "$D/deck_diff.txt"

echo "── SHA256SUMS ──"
( cd "$D" && find decks compare check_only -type f | LC_ALL=C sort | xargs sha256sum
  sha256sum readback.json readback.md deck_diff.json deck_diff.txt ) > "$TMP/sums" && mv "$TMP/sums" "$D/SHA256SUMS"
wc -l < "$D/SHA256SUMS" | xargs echo "SHA256SUMS 줄 수:"
[ "$RC" = 0 ] && echo "✓ 전부 PASS" || echo "⛔ 실패가 있다 (위 · readback.md · deck_diff.txt)"
exit "$RC"
