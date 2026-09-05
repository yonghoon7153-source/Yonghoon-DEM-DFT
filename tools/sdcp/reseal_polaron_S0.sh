#!/usr/bin/env bash
# reseal_polaron_S0.sh — 사전등록 재봉인 진단 (회신 U P0-5 대응, 2026-09-05)
#
# 왜 있나
#   probe 15/15 정상종료인데 `_pil_check_prereg` 가 막았다:
#     봉인 7b534427…  ← phase L 생성 시점의 사전등록 파일 SHA
#     현재 df5fdc48…  ← 지금 사전등록 파일 SHA (09-05 05:31 conformer 공개 조항 추가)
#   빌더 SHA 는 일치한다(cc38bff4). 즉 **입력을 만든 도구는 안 바뀌었고**, 바뀐 것은
#   사전등록 *문서*뿐이다. 그래도 규칙은 옳다 — "고쳤으면 새 사전등록이다".
#
# 이 스크립트가 하는 것 (읽기 전용 + 새 디렉터리)
#   ① 기존 MANIFEST_PILOT.json 에서 생성 인자를 **그대로** 꺼낸다 (손으로 안 적는다)
#   ② 그 인자로 phase L 입력을 **새 디렉터리**에 다시 만든다
#   ③ 새/옛 입력을 **바이트 대조**한다
#   ④ 판정을 찍는다
#
# ⛔ 이 스크립트가 못 하는 것 · 안 하는 것
#   · 기존 디렉터리를 **고치지 않는다.** 봉인을 옮겨 적지도, 출력을 지우지도 않는다.
#     (봉인만 맞추고 옛 출력을 통과시키는 것이 우리가 금지한 세탁 경로다 — 회신 W P0-5)
#   · phase L·probe 를 **다시 돌리지 않는다.** 재실행이 필요한지를 판정만 한다.
#   · 사전등록 내용이 옳은지는 안 본다 — 결박만 본다.
#   · ③이 "같다" 라고 해서 자동으로 승격되지 않는다. 승격은 사람이 한다.
#
# 사용법 (gabia)
#   bash reseal_polaron_S0.sh /data/work/runs/sdcp_polaron_S0_v3/<phase L 디렉터리>
set -u

BUILDER="${BUILDER:-$HOME/Yonghoon-DEM-DFT/tools/sdcp/build_v7c_trimer.py}"
OLD="${1:?phase L 디렉터리를 인자로 주세요}"
MAN="$OLD/MANIFEST_PILOT.json"
NEW="${NEW:-${OLD%/}_reseal_$(date +%H%M%S)}"

[ -f "$MAN" ] || { echo "⛔ $MAN 이 없다"; exit 2; }
[ -f "$BUILDER" ] || { echo "⛔ 빌더가 없다: $BUILDER"; exit 2; }

echo "=== ① 봉인 상태 ==="
python3 - "$MAN" "$BUILDER" <<'PY'
import hashlib, json, os, sys
man = json.load(open(sys.argv[1], encoding="utf-8"))
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
root = os.path.dirname(os.path.dirname(os.path.dirname(sys.argv[2])))
pre = os.path.join(root, man.get("prereg", ""))
print("  사전등록      :", man.get("prereg"))
print("  봉인 prereg   :", man.get("prereg_sha256"))
print("  현재 prereg   :", sha(pre) if os.path.isfile(pre) else "(파일 없음)")
print("  봉인 builder  :", (man.get("builder_sha256") or "?")[:64])
print("  현재 builder  :", sha(sys.argv[2]))
print("  parent_xyz    :", man.get("parent_xyz"))
print("  봉인 parent   :", man.get("parent_sha256"))
p = man.get("parent_xyz") or ""
print("  현재 parent   :", sha(p) if os.path.isfile(p) else "(파일 없음)")
PY

echo
echo "=== ② 재생성 인자 (manifest 에서 그대로) ==="
ARGS=$(python3 - "$MAN" <<'PY'
import json, shlex, sys
m = json.load(open(sys.argv[1], encoding="utf-8"))
a = ["--polaron_pilot",
     "--neutral_xyz", m["parent_xyz"],
     "--site", str(m["removed_H_1based"]),
     "--functional", m.get("functional", "r2SCAN-3c"),
     "--nprocs", str(m.get("nprocs", 1)),
     "--maxcore", str(m.get("maxcore_mb_per_proc", 3000))]
eps = sorted({v["epsilon"] for v in (m.get("environments") or {}).values()})
if eps:
    a += ["--eps"] + [("%g" % e) for e in eps]
if m.get("eps_basis"):
    a += ["--eps_why", m["eps_basis"]]
if str(m.get("loc_realization", "")).startswith("R1"):
    a += ["--loc_realization", "random"]
print(" ".join(shlex.quote(x) for x in a))
PY
)
echo "  $ARGS"
[ -n "$ARGS" ] || { echo "⛔ 인자를 못 뽑았다"; exit 2; }

echo
echo "=== ③ 새 디렉터리에 재생성 → $NEW ==="
# shellcheck disable=SC2086
python3 "$BUILDER" $ARGS --out "$NEW" 2>&1 | tail -20 || { echo "⛔ 재생성 실패"; exit 2; }

echo
echo "=== ④ 바이트 대조 — **재생성이 실제로 덮는 범위 안에서만** ==="
# ⛔⛔ 2026-09-05 첫 판의 버그: 옛 트리 전체(71개)와 새 트리(8개)를 통째로 비교해
#   "입력이 다르다" 는 **거짓 경보**를 냈다. `--polaron_pilot` 은 phase L 입력만 만들고,
#   `S/`·`S0P/` 는 나중에 `--polaron_seeds` 가 만든다 — 범위가 다른 것끼리 비교한 것이다.
#   ⇒ 판정은 **새 트리가 덮는 경로**에서만 하고, 덮지 않은 경로는 "2단계 필요" 로 따로 낸다.
python3 - "$OLD" "$NEW" <<'PY'
import hashlib, pathlib, sys
old, new = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
EXT = (".inp", ".xyz")          # 입력만. ORCA 출력·manifest 는 대조 대상이 아니다
def inputs(root):
    return {p.relative_to(root).as_posix(): sha(p)
            for p in sorted(root.rglob("*")) if p.is_file() and p.suffix in EXT}
a, b = inputs(old), inputs(new)
scope = sorted(set(b))                     # 재생성이 실제로 만든 것 = 판정 범위
missing = [k for k in scope if k not in a]  # 새쪽에만 = 옛 실행에 없던 입력 (진짜 변화)
diff    = [k for k in scope if k in a and a[k] != b[k]]
outside = sorted(set(a) - set(b))           # 이 단계가 안 만드는 것 (S/·S0P/ 등)
print(f"  판정 범위(새 트리가 만든 입력) {len(scope)}개 · 옛 트리 입력 총 {len(a)}개")
for k in missing[:10]: print(f"    + 새쪽에만(옛 실행에 없음): {k}")
for k in diff[:10]:    print(f"    ≠ 내용 다름: {k}")
print()
if not (missing or diff):
    print(f"  ✅ phase L 입력 {len(scope)}개가 **바이트 단위로 같다**.")
    print("     ⇒ 사전등록 개정은 phase L 생성 규칙을 바꾸지 않았다.")
else:
    print("  ⛔ phase L 입력이 다르다 — 개정이 생성 규칙을 바꿨다. phase L 부터 재실행.")
    raise SystemExit(1)
if outside:
    top = sorted({k.split("/")[0] for k in outside})
    print()
    print(f"  ⏳ 이 단계가 만들지 않는 입력 {len(outside)}개가 남아 있다 (최상위: {', '.join(top)}).")
    print("     `--polaron_seeds` 가 만드는 것이라 **2단계 대조가 따로 필요하다** —")
    print("     phase L 이 같다고 S/S0P 도 같다는 보장은 없다 (seed 선택이 그 사이에 있다).")
    print("     아래 ⑤ 를 이어서 돌린다.")
PY
rc=$?
echo
if [ "$rc" -ne 0 ]; then
  echo "옛 디렉터리는 손대지 않았다: $OLD"
  echo "새 디렉터리(비교용):        $NEW"
  exit "$rc"
fi

echo "=== ⑤ 2단계 — 새 봉인 manifest 로 phase S·probe 입력을 다시 만들어 대조 ==="
# phase L **출력**(.out/.gbw/.loc)이 있어야 seed 를 고를 수 있다. 그래서 옛 트리를 통째로
# 복사한 뒤 manifest 만 새 봉인으로 갈아끼우고, S/S0P 입력만 다시 만들어 대조한다.
# ⛔ 옛 트리는 여전히 안 건드린다. 그리고 이 복사본은 **대조용**이지 산출물이 아니다.
CMP="${NEW}_stage2"
rm -rf "$CMP"
cp -a "$OLD" "$CMP" || { echo "⛔ 복사 실패"; exit 2; }
cp -f "$NEW/MANIFEST_PILOT.json" "$CMP/MANIFEST_PILOT.json" || { echo "⛔ manifest 교체 실패"; exit 2; }
rm -rf "$CMP/S" "$CMP/S0P"          # 재생성 대상만 비운다 (L/L2 출력은 남긴다)
python3 "$BUILDER" --polaron_seeds "$CMP" 2>&1 | tail -15
python3 - "$OLD" "$CMP" <<'PY'
import hashlib, pathlib, sys
old, cmp = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
EXT = (".inp", ".xyz")
def inputs(root, subs=("S", "S0P")):
    out = {}
    for s in subs:
        d = root / s
        if d.is_dir():
            out.update({p.relative_to(root).as_posix(): sha(p)
                        for p in sorted(d.rglob("*")) if p.is_file() and p.suffix in EXT})
    return out
a, b = inputs(old), inputs(cmp)
only_a, only_b = sorted(set(a) - set(b)), sorted(set(b) - set(a))
diff = sorted(k for k in set(a) & set(b) if a[k] != b[k])
print(f"\n  옛 S/S0P 입력 {len(a)}개 · 새 봉인으로 만든 것 {len(b)}개")
for k in only_a[:8]: print(f"    − 옛쪽에만: {k}")
for k in only_b[:8]: print(f"    + 새쪽에만: {k}")
for k in diff[:8]:   print(f"    ≠ 내용 다름: {k}")
print()
if a and not (only_a or only_b or diff):
    print("  ✅ S/S0P 입력도 **바이트 단위로 같다**.")
    print("     ⇒ 이미 돈 probe 15/15 은 새 봉인 아래서도 같은 입력의 결과다. **재실행 불필요.**")
    print("     ⚠ 승격은 자동이 아니다 — 사람이 확인하고 결정한다.")
elif not a:
    print("  ⚠ 옛 트리에 S/S0P 입력이 없다 — 비교할 것이 없다.")
else:
    print("  ⛔ S/S0P 입력이 다르다 — seed 선택이나 생성 규칙이 바뀌었다. probe 를 다시 돌린다.")
PY
echo
echo "옛 디렉터리는 손대지 않았다: $OLD"
echo "1단계 새 디렉터리:          $NEW"
echo "2단계 대조 사본:            $CMP   (대조용이지 산출물이 아니다 — 확인 후 지워도 된다)"
