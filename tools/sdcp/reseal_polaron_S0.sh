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
echo "=== ④ 바이트 대조 (입력만 — 출력은 비교 대상이 아니다) ==="
python3 - "$OLD" "$NEW" <<'PY'
import hashlib, pathlib, sys
old, new = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
# 입력만 본다. ORCA 출력(.out/.gbw/.loc/.property.txt)과 manifest 는 제외 —
# manifest 는 봉인이 바뀌니 당연히 다르고, 그 차이는 이 대조의 대상이 아니다.
EXT = (".inp", ".xyz")
def inputs(root):
    return {p.relative_to(root).as_posix(): sha(p)
            for p in sorted(root.rglob("*")) if p.is_file() and p.suffix in EXT}
a, b = inputs(old), inputs(new)
only_a, only_b = sorted(set(a) - set(b)), sorted(set(b) - set(a))
diff = sorted(k for k in set(a) & set(b) if a[k] != b[k])
print(f"  옛 입력 {len(a)}개 · 새 입력 {len(b)}개")
for k in only_a[:10]: print(f"    − 옛쪽에만: {k}")
for k in only_b[:10]: print(f"    + 새쪽에만: {k}")
for k in diff[:10]:   print(f"    ≠ 내용 다름: {k}")
print()
if not (only_a or only_b or diff):
    print("  ✅ 입력이 **바이트 단위로 같다**.")
    print("     ⇒ 사전등록 개정은 생성 규칙을 안 바꿨다. 이미 돈 phase L·probe 출력은")
    print("       새 봉인 아래서도 같은 입력의 결과다. **재실행 불필요.**")
    print("     ⚠ 다만 승격은 자동이 아니다 — 이 출력을 사람이 확인하고 결정한다.")
else:
    print("  ⛔ 입력이 다르다. 사전등록 개정이 생성 규칙을 바꿨다는 뜻이다.")
    print("     ⇒ phase L 부터 **다시 돌린다.** 옛 출력은 새 사전등록의 결과가 아니다.")
PY
echo
echo "옛 디렉터리는 손대지 않았다: $OLD"
echo "새 디렉터리(비교용):        $NEW"
