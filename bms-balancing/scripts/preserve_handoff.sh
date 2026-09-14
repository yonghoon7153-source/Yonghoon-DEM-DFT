#!/usr/bin/env bash
# COMSOL 6.3 handoff ZIP 을 **bytes 그대로** 저장소에 보존한다 (codex63 묶음 여덟 번째부터 이 스크립트로).
#
#   ./scripts/preserve_handoff.sh <zip 경로> <묶음이름> \
#       --expect-size <bytes> --expect-sha <sha256> --expect-manifest-sha <sha256>
#
# 예 (WSL):
#   ./scripts/preserve_handoff.sh \
#     "/mnt/c/Users/Administrator/Documents/카카오톡 받은 파일/COMSOL63_LATE_CAP_A_HANDOFF.zip" late_cap_a \
#     --expect-size 780744308 \
#     --expect-sha 63bdb39c2956e1865441e26ffff344017b6c884519a7e94cf7c8acbf717e60b7 \
#     --expect-manifest-sha d7c19bb00a90fe42fa647d70adc5d5b98549b60750d4cfc0f2d7bc0c4de8ccc2
#
# ⚠ 왜 스크립트인가 — **순서 때문이다.** r320_timecap 때 `.gitattributes` 의 `-text` 규칙보다 커밋이 **먼저**
#   가는 바람에 git 이 체크인에서 CRLF→LF 정규화를 걸었고, 커밋된 bytes 가 manifest 의 sha256 과 갈렸다.
#   80 개 파일을 원본 bytes 로 되돌려야 했고, 그중 하나는 줄끝이 섞여 있어(104 줄 중 102 번째만 맨 LF)
#   일괄 치환으로는 복원이 안 됐다. 경위는 `reviews/r14_repros/codex63/r320_timecap/README.md`.
#   그래서 이 스크립트는 **규칙을 먼저 넣고 커밋한 뒤에** 파일을 푼다. 순서를 사람이 기억하지 않게 한다.
#
# ⚠ ZIP 안의 스크립트·COMSOL 은 **실행하지 않는다.** 이 스크립트가 하는 일은 읽기·해시·복사뿐이다.
# ⚠ mph·로그·java·그림·py·중첩 ZIP·대용량 profile CSV 는 보존하지 않는다 (저장소는 public 이고 용량이 있다).
#   보존한 것만 manifest 의 sha256 과 대조하고, 제외한 것은 목록에 크기만 남긴다.
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$HERE" || exit 1

#: 보존할 확장자와 크기 상한. r320_timecap 실측에서 뽑았다 — 보존한 것 중 최대가 1,462,629 B 이고
#: 제외한 profile CSV 중 최소가 21,063,079 B 라, 그 사이 어디든 같은 집합을 준다. 8 MiB 로 둔다.
KEEP_EXT="json csv md txt"
MAX_KEEP_BYTES="${MAX_KEEP_BYTES:-8388608}"

ZIP="${1:-}"; NAME="${2:-}"; shift 2 2>/dev/null || true
EXP_SIZE=""; EXP_SHA=""; EXP_MSHA=""
while [ $# -gt 0 ]; do
  case "$1" in
    --expect-size)         EXP_SIZE="$2"; shift 2 ;;
    --expect-sha)          EXP_SHA="$2";  shift 2 ;;
    --expect-manifest-sha) EXP_MSHA="$2"; shift 2 ;;
    *) echo "! 모르는 인자: $1" >&2; exit 2 ;;
  esac
done

if [ -z "$ZIP" ] || [ -z "$NAME" ]; then
  sed -n '2,12p' "${BASH_SOURCE[0]}" >&2; exit 2
fi
case "$NAME" in *[!A-Za-z0-9_-]*|"") echo "! 묶음이름은 글자·숫자·_·- 만: '$NAME'" >&2; exit 2 ;; esac
[ -f "$ZIP" ] || { echo "! ZIP 이 없다: $ZIP" >&2; exit 2; }

DEST="reviews/r14_repros/codex63/$NAME"
[ -e "$DEST" ] && { echo "! 이미 있다 (덮지 않는다): $DEST" >&2; exit 2; }

echo "══ 1. 수신 ZIP 자체 ════════════════════════════════════════════════"
SIZE="$(stat -c %s "$ZIP")"
SHA="$(sha256sum "$ZIP" | cut -d' ' -f1)"
printf '  크기      %s bytes\n  SHA-256   %s\n' "$SIZE" "$SHA"
fail=0
if [ -n "$EXP_SIZE" ]; then
  if [ "$SIZE" = "$EXP_SIZE" ]; then echo "  → 크기 전달값과 일치"
  else echo "  ✗ 크기 불일치 (전달값 $EXP_SIZE)"; fail=1; fi
fi
if [ -n "$EXP_SHA" ]; then
  if [ "$SHA" = "$EXP_SHA" ]; then echo "  → SHA 전달값과 일치"
  else echo "  ✗ SHA 불일치 (전달값 $EXP_SHA)"; fail=1; fi
fi
[ "$fail" = 0 ] || { echo "! 수신본이 전달값과 다르다 — 여기서 멈춘다 (변조 단정이 아니라 확인 필요)" >&2; exit 1; }

echo
echo '══ 2. .gitattributes 규칙을 **먼저** 넣고 커밋 ═════════════════════'
RULE="reviews/r14_repros/codex63/$NAME/** -text"
if grep -qF "$RULE" .gitattributes; then
  echo "  이미 있다: $RULE"
else
  printf '%s\n' "$RULE" >> .gitattributes
  git add .gitattributes
  git commit -q -m "bms: .gitattributes — ${NAME} 묶음 원문 bytes 보존 규칙 (묶기 **전에** 넣는다)" \
    -m "r320_timecap 에서 규칙보다 커밋이 먼저 가 CRLF→LF 정규화로 80 파일의 bytes 가 manifest sha 와 갈렸다. 순서를 먼저 고정한다." \
    && echo "  추가·커밋: $RULE" || { echo "! 규칙 커밋 실패" >&2; exit 1; }
fi

echo
echo "══ 3. 임시 디렉터리에 풀기 (실행 없음) ═════════════════════════════"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
unzip -q -o "$ZIP" -d "$TMP" || { echo "! unzip 실패" >&2; exit 1; }
echo "  풀린 항목 $(find "$TMP" -type f | wc -l) 개 → $TMP"

echo
echo "══ 4. manifest 찾기·자체 해시 대조 ═════════════════════════════════"
MAN="$(find "$TMP" -name package_manifest.json -type f | head -1)"
[ -n "$MAN" ] || { echo "! package_manifest.json 을 못 찾았다" >&2; exit 1; }
MSHA="$(sha256sum "$MAN" | cut -d' ' -f1)"
echo "  manifest   ${MAN#$TMP/}"
echo "  self-SHA   $MSHA"
if [ -n "$EXP_MSHA" ]; then
  if [ "$MSHA" = "$EXP_MSHA" ]; then echo "  → 전달값과 일치"
  else echo "  ✗ 불일치 (전달값 $EXP_MSHA) — 멈춘다"; exit 1; fi
fi

echo
echo "══ 5. payload 전수 대조 + 보존 대상 복사 ═══════════════════════════"
MAN_REL_OUT="$TMP/.man_rel"
DEST="$DEST" TMP="$TMP" MAN="$MAN" KEEP_EXT="$KEEP_EXT" MAX_KEEP_BYTES="$MAX_KEEP_BYTES" MAN_REL_OUT="$MAN_REL_OUT" \
python3 - <<'PY' || exit 1
import hashlib, json, os, pathlib, shutil, sys
dest = pathlib.Path(os.environ["DEST"]); tmp = pathlib.Path(os.environ["TMP"])
man  = pathlib.Path(os.environ["MAN"])
keep_ext = {"." + e for e in os.environ["KEEP_EXT"].split()}
cap = int(os.environ["MAX_KEEP_BYTES"])
m = json.loads(man.read_text(encoding="utf-8"))
entries = m.get("entries") or []
if not entries:
    print("! manifest 에 entries 가 없다", file=sys.stderr); sys.exit(1)

# ZIP 이 한 겹 더 감싸는 경우가 있다 — manifest 의 첫 경로로 뿌리를 찾는다
probe = entries[0]["path"]
root = tmp
if not (tmp / probe).exists():
    cand = [d for d in tmp.iterdir() if d.is_dir() and (d / probe).exists()]
    if len(cand) != 1:
        print(f"! manifest 경로의 뿌리를 못 찾았다 ({probe})", file=sys.stderr); sys.exit(1)
    root = cand[0]

ok = bad = miss = 0; kept = 0; skipped = 0; listing = []
for e in entries:
    src = root / e["path"]
    listing.append((e.get("bytes", -1), e["path"]))
    if not src.is_file():
        miss += 1; print(f"  ✗ ZIP 에 없다: {e['path']}"); continue
    h = hashlib.sha256(src.read_bytes()).hexdigest()
    if h == e["sha256"]:
        ok += 1
    else:
        bad += 1; print(f"  ✗ sha 불일치: {e['path']}")
    p = pathlib.Path(e["path"])
    if p.suffix.lower() in keep_ext and src.stat().st_size <= cap:
        out = dest / p
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, out)          # bytes 그대로 (텍스트 변환 없음)
        kept += 1
    else:
        skipped += 1

print(f"\n  manifest 명세 {len(entries)} · ZIP 안 sha 일치 {ok} · 불일치 {bad} · 없음 {miss}")
print(f"  보존 {kept} · 제외 {skipped} (mph·로그·java·그림·py·중첩 ZIP·{cap//1048576} MiB 초과 CSV)")
if bad or miss:
    print("! ZIP 내부가 manifest 와 다르다 — 멈춘다", file=sys.stderr); sys.exit(1)

# ⚠ manifest 자신은 `entries` 에 **없다** (`self_excluded`). 위 루프만 돌면 대조의 기준이 되는 파일이
#   저장소에 안 남는다 — 그러면 나중에 "보존 bytes 가 맞는가" 를 물을 방법 자체가 사라진다.
#   (2026-09-14 합성 ZIP 시험이 잡은 결함이다. 앞선 일곱 묶음은 손으로 복사해서 문제가 없었다.)
man_rel = man.relative_to(root) if man.is_relative_to(root) else pathlib.Path(man.name)
man_out = dest / man_rel
man_out.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(man, man_out)
print(f"  manifest 자신도 보존: {man_rel} "
      f"(self-SHA {hashlib.sha256(man_out.read_bytes()).hexdigest()[:16]}…)")
# ⚠ 묶음 안에 **이전 묶음의 manifest 가 같이 들어오는 일이 있다** (late_cap_a 에 radial320_timecap 것이
#   딸려 왔다). 그러니 뒤에 오는 검사가 `rglob` 으로 아무거나 집으면 엉뚱한 것과 대조한다 — 이번 것의
#   경로를 그대로 넘긴다. (2026-09-14 실측: 그렇게 집어서 "일치 21 · 불일치 1" 이 나왔다.)
pathlib.Path(os.environ["MAN_REL_OUT"]).write_text(str(man_rel), encoding="utf-8")

dest.mkdir(parents=True, exist_ok=True)
(dest / "FULL_LISTING.tsv").write_text(
    "".join(f"{b}\t./{p}\n" for b, p in sorted(listing, key=lambda t: t[1])), encoding="utf-8")
print(f"  FULL_LISTING.tsv {len(listing)} 행")
PY

printf '%s  %s\n' "$SHA" "$ZIP" > "$DEST/ZIP_SHA256.txt"

echo
echo "══ 6. **복사한 뒤** 다시 대조 (디스크 bytes 가 manifest 와 같은가) ══"
DEST="$DEST" MAN="$MAN" python3 - <<'PY' || exit 1
import hashlib, json, os, pathlib
dest = pathlib.Path(os.environ["DEST"])
m = json.loads(pathlib.Path(os.environ["MAN"]).read_text(encoding="utf-8"))
ok = bad = 0
for e in m["entries"]:
    p = dest / e["path"]
    if not p.is_file():
        continue
    if hashlib.sha256(p.read_bytes()).hexdigest() == e["sha256"]: ok += 1
    else: bad += 1; print(f"  ✗ {e['path']}")
print(f"  보존 {ok+bad} 개 중 sha 일치 {ok} · 불일치 {bad}")
raise SystemExit(1 if bad else 0)
PY

echo
echo
echo "══ 7. 다음 (사람이 확인하고 친다) ══════════════════════════════════"
MAN_REL="$(cat "$TMP/.man_rel" 2>/dev/null || echo '')"
PREFIX="$(git rev-parse --show-prefix)"          # 저장소 루트에서 본 이 디렉터리
cat <<NEXT
  git add "$DEST"
  git commit -m "bms: ${NAME} 원문 보존 (md·json·csv·txt; mph·log·java·py·그림 제외)"
  git push -u origin claude/bms-alpha-beta-verify

  그 다음 커밋 안의 bytes 를 재대조한다 (줄끝 정규화가 안 먹었는지 — 이 스크립트의 존재 이유).
  ⚠ 두 가지를 틀리기 쉽다: \\`git show HEAD:<경로>\\` 는 **저장소 루트** 기준이고,
    묶음에 이전 묶음의 manifest 가 딸려 오는 일이 있어 **이번 것을 명시**해야 한다.
  python3 - <<'CHECK'
import hashlib, json, pathlib, subprocess
dest = "${PREFIX}${DEST}"                     # 저장소 루트 기준
man  = pathlib.Path(dest) / "${MAN_REL}"      # 이번 묶음의 manifest (rglob 쓰지 말 것)
m = json.loads(man.read_text(encoding="utf-8"))
print("manifest self-SHA:", hashlib.sha256(man.read_bytes()).hexdigest())
ok = bad = skip = 0
for e in m["entries"]:
    rel = f"{dest}/{e['path']}"
    try: blob = subprocess.run(["git","show",f"HEAD:{rel}"],capture_output=True,check=True).stdout
    except subprocess.CalledProcessError: skip += 1; continue
    if hashlib.sha256(blob).hexdigest() == e["sha256"]: ok += 1
    else: bad += 1; print("  X 커밋 bytes 불일치:", e["path"])
print("커밋(HEAD) 안 bytes: 일치 %d · 불일치 %d · 미보존 %d" % (ok, bad, skip))
CHECK
NEXT
