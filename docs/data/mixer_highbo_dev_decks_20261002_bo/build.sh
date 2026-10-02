#!/usr/bin/env bash
# 믹서 고-Bo 강성 축 — 개발 탐색 dev-bo 덱 · 되읽기 · 덱 비교 증거 재생성 (2026-10-02 · 사전등록 v2.8 §11 · 1저자 "ㄱㄱ")
#   사전등록 docs/reviews/mixer_highbo_stiffness_prereg_20260929.md §11 (dev-bo) · §3 (강성 축 · 쌍별 F₀ 보존) · §9 (공동 개입 B)
#   ⛔ 시뮬레이션 · ibb · WSL 실행 없음 — 덱 생성 (생성기 CLI) · 무입자 검사 (이름 → 덱 · 되읽기 · 덱 비교) 만.
#
#   리포 루트에서:   bash docs/data/mixer_highbo_dev_decks_20261002_bo/build.sh
#   재현 확인:       (같은 명령 뒤) cd docs/data/mixer_highbo_dev_decks_20261002_bo && sha256sum -c SHA256SUMS
#
#   폴더
#     decks/   dev-bo 실행 대상 2 (LHx10_ref_r2_s32452843 · LHx30_ref_r2_s32452843) — 런처 dev-bo 입력 (런 폴더로 옮기는 법 = README)
#   각 덱 폴더: in.mixer · gen_cmd.txt (정확한 생성 명령) · gen.log · deck_meta.json (경화 덱 — 생성기가 쓴다)
#   기준 덱 (읽기만 · 여기서 다시 쓰지 않는다) = docs/data/mixer_highbo_dev_decks_20260930_v26/decks/{LC,LH}_ref_r2_s32452843
#     (ibb dev-rot 에서 실제로 돈 덱 — 판독 JSON 의 출처 덱 sha256 5405067f… · 3125d244…) — 지금 생성기도 같은 바이트를 내는지 본다 (기존 팔 불변).
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT" || exit 2
D=docs/data/mixer_highbo_dev_decks_20261002_bo
V26=docs/data/mixer_highbo_dev_decks_20260930_v26/decks
BASE="--n-total 100000 --cgf 151.4"                       # gen_all.sh 기본 (N_TOTAL · CGF) · rpm = --fr 기본 (Fr 0.0827) 에서 유도
REF="--stiffen-se 20 --hold-bo-pairwise"                  # 사전등록 §3 v2.6 E_ref (×20) — dev-rot 과 같은 강성
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
gen decks/LHx10_ref_r2_s32452843 --arm LHx10 --seed 32452843 --revolutions 2 $REF
gen decks/LHx30_ref_r2_s32452843 --arm LHx30 --seed 32452843 --revolutions 2 $REF

echo "── 기존 팔 불변 — 지금 생성기의 LC_ref_r2 · LH_ref_r2 (같은 명령) = v26 커밋 덱 (= ibb dev-rot 실행 덱 · 바이트) ──"
for a in LC LH; do
  python3 scripts/make_mixer_deck.py --out "$TMP/v26_$a" $BASE --arm $a --seed 32452843 --revolutions 2 $REF > /dev/null 2>&1 \
    || { echo "⛔ 재생성 실패: ${a}_ref_r2"; exit 1; }
  if cmp -s "$TMP/v26_$a/in.mixer" "$V26/${a}_ref_r2_s32452843/in.mixer"; then
    echo "✓ ${a}_ref_r2_s32452843  $(sha256sum "$V26/${a}_ref_r2_s32452843/in.mixer" | cut -c1-16)  = v26 커밋 덱"
  else echo "⛔ ${a}_ref_r2_s32452843 — 지금 생성기 덱이 v26 커밋 덱과 다르다 (기존 팔이 바뀌었다)"; RC=1; fi
done

echo "── 이름 → 덱 (mixer_deck_diff.cell_expected_deck — 런처 dev-bo 관문이 쓰는 경로) = 커밋 덱 ──"
python3 - "$D" <<'PY' || RC=1
import os, sys
sys.path.insert(0, 'scripts')
import mixer_deck_diff as dd
D, bad = sys.argv[1], 0
for n in dd.DEV_BO:
    ok = dd.cell_expected_deck(n) == open(os.path.join(D, 'decks', n, 'in.mixer'), encoding='utf-8').read()
    print(('✓ ' if ok else '⛔ ') + f'{n} — 이름 → 생성 인자 → 덱 ' + ('바이트 동일' if ok else '다르다'))
    bad += not ok
sys.exit(1 if bad else 0)
PY

echo "── 되읽기 표 B (덱 텍스트만 · 같은 강성 ×20 · AM–AM 셋 · AM–벽 둘만 증가 · 나머지 정확히 같다) ──"
python3 scripts/mixer_deck_readback.py \
  --table B "$V26/LC_ref_r2_s32452843/in.mixer" "$D/decks/LHx10_ref_r2_s32452843/in.mixer" \
  --table B "$V26/LC_ref_r2_s32452843/in.mixer" "$D/decks/LHx30_ref_r2_s32452843/in.mixer" \
  --table B "$V26/LH_ref_r2_s32452843/in.mixer" "$D/decks/LHx10_ref_r2_s32452843/in.mixer" \
  --table B "$V26/LH_ref_r2_s32452843/in.mixer" "$D/decks/LHx30_ref_r2_s32452843/in.mixer" \
  --table B "$D/decks/LHx10_ref_r2_s32452843/in.mixer" "$D/decks/LHx30_ref_r2_s32452843/in.mixer" \
  --json "$D/readback.json" --md "$D/readback.md" || RC=1

echo "── 덱 비교 mixer_deck_diff — 가장 좁은 허용목록: A (AM–AM 셋) = FAIL 이어야 · B (AM–AM 셋 + AM–벽 둘) = PASS ──"
: > "$D/deck_diff.txt"
DDJ=()
ddiff() {  # ddiff <허용> <기대 rc> <기준 덱 폴더> <새 rel> — B 는 --expect-deck = 같은 명령의 재생성 덱 (gen 이 $TMP 에 만들어 둔 것)
  local allow="$1" want="$2" a="$3" b="$4" js="$TMP/dd_${#DDJ[@]}.json" rc
  if [ "$allow" = B ]; then
    { echo; echo "### python3 scripts/mixer_deck_diff.py $a/in.mixer $D/$b/in.mixer --allow B --expect-deck <재생성 $b>   (기대 rc $want)"; } >> "$D/deck_diff.txt"
    python3 scripts/mixer_deck_diff.py "$a/in.mixer" "$D/$b/in.mixer" --allow B --expect-deck "$TMP/$b/in.mixer" --json "$js" >> "$D/deck_diff.txt" 2>&1; rc=$?
  else
    { echo; echo "### python3 scripts/mixer_deck_diff.py $a/in.mixer $D/$b/in.mixer --allow $allow   (기대 rc $want)"; } >> "$D/deck_diff.txt"
    python3 scripts/mixer_deck_diff.py "$a/in.mixer" "$D/$b/in.mixer" --allow "$allow" --json "$js" >> "$D/deck_diff.txt" 2>&1; rc=$?
  fi
  echo "(rc $rc)" >> "$D/deck_diff.txt"
  [ "$rc" = "$want" ] || { echo "⛔ $allow $a → $b : rc $rc ≠ 기대 $want"; RC=1; }
  DDJ+=("$allow|$want|$rc|$a|$D/$b|$js")
}
ddiff A 1 "$V26/LH_ref_r2_s32452843" decks/LHx10_ref_r2_s32452843
ddiff A 1 "$V26/LH_ref_r2_s32452843" decks/LHx30_ref_r2_s32452843
ddiff B 0 "$V26/LH_ref_r2_s32452843" decks/LHx10_ref_r2_s32452843
ddiff B 0 "$V26/LH_ref_r2_s32452843" decks/LHx30_ref_r2_s32452843
ddiff B 0 "$V26/LC_ref_r2_s32452843" decks/LHx10_ref_r2_s32452843
ddiff B 0 "$V26/LC_ref_r2_s32452843" decks/LHx30_ref_r2_s32452843
ddiff B 0 "$D/decks/LHx10_ref_r2_s32452843" decks/LHx30_ref_r2_s32452843
python3 - "$D/deck_diff.json" "${DDJ[@]}" <<'PY' || RC=1
import hashlib, json, sys
out, rows = sys.argv[1], []
for spec in sys.argv[2:]:
    allow, want, rc, a, b, js = spec.split('|')
    r = json.load(open(js, encoding='utf-8'))[0]
    rows.append(dict(allow=allow, ref=a + '/in.mixer', new=b + '/in.mixer', expected_rc=int(want), rc=int(rc), verdict=r['verdict'],
                     changed=r['changed'], outside=r['outside'], missing=r['missing'], wrong_direction=r['wrong_direction'],
                     non_ced_diffs=r['non_ced_diffs'], target_mismatch=r['target_mismatch'],
                     ced=[dict(pair=t['pair'], ref=t['ref'], new=t['new'], ratio=t['ratio']) for t in r['table']]))
tool = 'scripts/mixer_deck_diff.py'
ok = all(r_['rc'] == r_['expected_rc'] for r_ in rows) and all(r_['verdict'] == ('PASS' if r_['allow'] == 'B' else 'FAIL') for r_ in rows)
json.dump(dict(tool=tool, tool_sha256=hashlib.sha256(open(tool, 'rb').read()).hexdigest(),
               note='A (AM–AM 셋만) 는 AM–벽 둘이 허용목록 밖이라 FAIL 이어야 한다 = B 가 통과하는 가장 좁은 허용목록 · '
                    'B 의 --expect-deck = 같은 생성 명령을 임시 폴더에 다시 돌린 덱 (CED 목표) · CED 밖 명령 (E · ν · dt · run · 기하 · 시드 · 삽입) 은 토큰까지 같다',
               verdict='PASS' if ok else 'FAIL', comparisons=rows),
          open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
open(out, 'a', encoding='utf-8').write('\n')
print(f"deck_diff: 기대대로 {sum(r_['rc'] == r_['expected_rc'] for r_ in rows)}/{len(rows)} (A FAIL {sum(r_['allow'] == 'A' for r_ in rows)} · "
      f"B PASS {sum(r_['allow'] == 'B' and r_['verdict'] == 'PASS' for r_ in rows)}) → {out}")
sys.exit(0 if ok else 1)
PY
sed -i "s#$TMP#<재생성 임시 폴더>#g" "$D/deck_diff.txt"

echo "── SHA256SUMS ──"
( cd "$D" && find decks -type f | LC_ALL=C sort | xargs sha256sum
  sha256sum readback.json readback.md deck_diff.json deck_diff.txt ) > "$TMP/sums" && mv "$TMP/sums" "$D/SHA256SUMS"
wc -l < "$D/SHA256SUMS" | xargs echo "SHA256SUMS 줄 수:"
[ "$RC" = 0 ] && echo "✓ 전부 PASS" || echo "⛔ 실패가 있다 (위 · readback.md · deck_diff.txt)"
exit "$RC"
