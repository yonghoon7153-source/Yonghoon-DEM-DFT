#!/usr/bin/env bash
# 고침 C 증거 모으기 — 작업 트리의 pa15_fix/ (code.diff · 적용 확인 · code_sha256.txt · 로그 (경로 가림) · 도구 · SHA256SUMS = REPORT.md 없이) + preattack15/SHA256SUMS.
# 쓰임: bash assemble_evidence.sh <작업 트리> <scratch 뿌리> <리포> <fixc 폴더>
set -u
WT=${1:?작업 트리}
SC=${2:?scratch 뿌리}
RP=${3:?리포}
FX=${4:?fixc 폴더}
EVR="$WT/docs/reviews/rint2_rr4_fix_evidence_20261109"
EV="$EVR/pa15_fix"
mkdir -p "$EV/logs" "$EV/tools"
cd "$WT" || exit 9
git diff 69d714d09 -- scripts/rint_r_chain.py scripts/test_rint_r_chain.py > "$EV/code.diff"
# 적용 확인 — 바탕 두 파일 (git show 69d714d09) + code.diff = 고친 두 파일 바이트
AP="$FX/apply_check"
rm -rf "$AP" && mkdir -p "$AP/scripts"
git show 69d714d09:scripts/rint_r_chain.py > "$AP/scripts/rint_r_chain.py"
git show 69d714d09:scripts/test_rint_r_chain.py > "$AP/scripts/test_rint_r_chain.py"
{
  echo "== 바탕 (git show 69d714d09)"
  (cd "$AP" && sha256sum scripts/rint_r_chain.py scripts/test_rint_r_chain.py)
  echo "== patch -p1 < code.diff"
  (cd "$AP" && patch -p1 --no-backup-if-mismatch < "$EV/code.diff" > /dev/null; echo "rc=$?")
  echo "== 적용 뒤 ↔ 작업 트리 (고친 판)"
  (cd "$AP" && sha256sum scripts/rint_r_chain.py scripts/test_rint_r_chain.py)
  sha256sum scripts/rint_r_chain.py scripts/test_rint_r_chain.py
  cmp "$AP/scripts/rint_r_chain.py" scripts/rint_r_chain.py && cmp "$AP/scripts/test_rint_r_chain.py" scripts/test_rint_r_chain.py && echo "바이트 같음 2/2"
} > "$FX/logs/apply_check.log" 2>&1
B1=$(git show 69d714d09:scripts/rint_r_chain.py | sha256sum | cut -d' ' -f1)
B2=$(git show 69d714d09:scripts/test_rint_r_chain.py | sha256sum | cut -d' ' -f1)
F1=$(sha256sum scripts/rint_r_chain.py | cut -d' ' -f1)
F2=$(sha256sum scripts/test_rint_r_chain.py | cut -d' ' -f1)
{
  echo "# 바탕 = 69d714d09 (= 회차 ④ 고침 e94f09905 + 기록 커밋 · scripts 같음 · 사전 공격 15 검토 판)"
  echo "$B1  scripts/rint_r_chain.py  (바탕)"
  echo "$B2  scripts/test_rint_r_chain.py  (바탕)"
  echo "# 고친 판 = 바탕 + code.diff = 이 커밋 · 시험 먼저 = 최종 시험을 바탕 사슬에 먼저 돌림 → 고침 → 같은 시험 · 변이 · 탐침 다시 = 이 바이트"
  echo "$F1  scripts/rint_r_chain.py  (고친 판)"
  echo "$F2  scripts/test_rint_r_chain.py  (고친 판)"
} > "$EV/code_sha256.txt"
# 로그 (경로 가림 · 원 이름 그대로 · py38 · probes_out 하위 폴더 포함)
(cd "$FX/logs" && find . -type f | sort) | while read -r f; do
  mkdir -p "$(dirname "$EV/logs/$f")"
  python3 "$FX/tools/sanitize_log.py" "$FX/logs/$f" "$EV/logs/$f" "$SC" "$WT" "$RP" > /dev/null
done
cp "$FX"/tools/*.py "$FX"/tools/*.sh "$EV/tools/"
(cd "$EV" && find . -type f ! -name SHA256SUMS ! -name REPORT.md | LC_ALL=C sort | sed 's|^\./||' | xargs sha256sum > SHA256SUMS)
(cd "$EVR/preattack15" && find . -type f ! -name SHA256SUMS | LC_ALL=C sort | sed 's|^\./||' | xargs sha256sum > SHA256SUMS)
wc -l "$EV/SHA256SUMS" "$EVR/preattack15/SHA256SUMS"
cat "$FX/logs/apply_check.log"
