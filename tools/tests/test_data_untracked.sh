#!/usr/bin/env bash
#
# data/ 아래 것이 저장소에 실려 다니지 않는가.
#
# 실제로 일어난 일: `.gitignore` 가 `data/uploads/*` 와 `data/runs/*` 두 줄만
# 막고 있었는데, EIS 를 붙이면서 파싱 캐시가 `data/spectra/` 라는 **새 폴더**로
# 갔다.  그 폴더는 두 줄 중 어느 것에도 안 걸려서, `.npz` 23개가 커밋에
# 딸려 들어가 그 뒤로 계속 pull 마다 오갔다:
#
#     data/spectra/1/points.npz | Bin 13250 -> 7133 bytes
#
# 이것이 조용한 이유는 아무것도 안 깨지기 때문이다.  캐시는 원본에서 다시
# 만들 수 있는 것이라 (`_load_points`) 없어도 되고, 있어도 되고, 상대 기계의
# DB 에는 그 행이 없어서 읽히지도 않는다.  다만 저장소가 계속 무거워지고,
# CLAUDE.md §2 가 "절대 커밋하지 않는 것" 이라고 못박은 바로 그것이다.
#
# `.gitignore` 를 `data/*` 로 넓혀 새 캐시 폴더에도 저절로 맞게 했고, 이
# 테스트가 다시 새어 나가는지를 본다.
#
# 사용: bash tools/tests/test_data_untracked.sh   (실패 0 이면 exit 0)

set -uo pipefail

HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd -P "$HERE/../.." && pwd)"

pass=0
fail=0

ok()   { pass=$((pass + 1)); printf '  ok   %s\n' "$1"; }
bad()  { fail=$((fail + 1)); printf '  FAIL %s\n' "$1"; [ $# -gt 1 ] && printf '       %s\n' "$2"; }

printf 'data/ 추적 여부\n'

# 1. 추적되는 것은 .gitkeep 뿐이다.
tracked="$(git -C "$REPO" ls-files data/ | grep -v '/\.gitkeep$' || true)"
if [ -z "$tracked" ]; then
  ok 'data/ 아래 추적되는 파일은 .gitkeep 뿐'
else
  bad 'data/ 아래에 추적되는 파일이 있다' "$(printf '%s' "$tracked" | tr '\n' ' ')"
fi

# 2. 아직 없는 캐시 폴더도 미리 막혀 있다 -- 다음에 폴더가 하나 더 늘어도
#    여기 한 줄을 더 적어야 하는 일이 없도록.
for path in data/spectra/1/points.npz data/gitt/9/points.npz \
            data/drt/3/gamma.npz data/uploads/x.wrd data/workbench.db; do
  if git -C "$REPO" check-ignore -q --no-index "$path"; then
    ok "무시됨: $path"
  else
    bad "무시되지 않는다: $path" '.gitignore 의 data/* 줄을 확인하세요'
  fi
done

# 3. 그래도 .gitkeep 은 살아 있어야 한다 -- 빈 폴더는 git 이 못 담으므로,
#    이것까지 막으면 클론한 기계에 data/uploads 가 아예 안 생긴다.
for keep in data/uploads/.gitkeep data/runs/.gitkeep; do
  if git -C "$REPO" check-ignore -q --no-index "$keep"; then
    bad "$keep 이 무시된다" '빈 폴더가 클론에 안 담긴다'
  else
    ok "살아 있음: $keep"
  fi
done

printf '\n%d 통과 · %d 실패\n' "$pass" "$fail"
[ "$fail" -eq 0 ]
