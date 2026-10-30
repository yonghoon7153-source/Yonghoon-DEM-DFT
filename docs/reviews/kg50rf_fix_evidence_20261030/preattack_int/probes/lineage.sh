#!/bin/bash
# PAI probe — sha256 of scripts/resume_ckpt.sh (whole · first 1033 lines) at each commit bf8cf21c6..HEAD, plus the
#   heredoc boundaries.  Read-only (git show into a pipe).
cd "$(dirname "$0")/../../../../.." || exit 9
for c in $(git rev-list --reverse bf8cf21c6^..HEAD); do
  full=$(git show "$c:scripts/resume_ckpt.sh" 2>/dev/null | sha256sum | cut -c1-16)
  h1033=$(git show "$c:scripts/resume_ckpt.sh" 2>/dev/null | head -1033 | sha256sum | cut -c1-16)
  pyend=$(git show "$c:scripts/resume_ckpt.sh" 2>/dev/null | grep -n '^PY$' | head -1 | cut -d: -f1)
  printf '%s  full %s  head1033 %s  first-PY-line %s  %s\n' "${c:0:9}" "$full" "$h1033" "$pyend" "$(git log -1 --format=%s "$c" | cut -c1-70)"
done
