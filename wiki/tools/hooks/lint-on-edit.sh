#!/bin/bash
# PostToolUse hook: run the wiki lint after any Edit/Write to a wiki .md file.
# Read-only check — reports errors back to the agent (exit 2), never modifies files.
# 킷 원본과 다른 점: 위키가 `wiki/` 하위라 경로 필터와 lint 경로에 wiki/ 가 붙는다.

INPUT=$(cat)
FILE=$(printf '%s' "$INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('tool_input',{}).get('file_path',''))" 2>/dev/null)

# only lint wiki content files
case "$FILE" in
  "$CLAUDE_PROJECT_DIR"/wiki/concepts/*.md|"$CLAUDE_PROJECT_DIR"/wiki/entities/*.md|\
  "$CLAUDE_PROJECT_DIR"/wiki/comparisons/*.md|"$CLAUDE_PROJECT_DIR"/wiki/queries/*.md|\
  "$CLAUDE_PROJECT_DIR"/wiki/guides/*.md|"$CLAUDE_PROJECT_DIR"/wiki/questions/*.md|\
  "$CLAUDE_PROJECT_DIR"/wiki/syntheses/*.md|"$CLAUDE_PROJECT_DIR"/wiki/raw/*|\
  "$CLAUDE_PROJECT_DIR"/wiki/index.md|"$CLAUDE_PROJECT_DIR"/wiki/SCHEMA.md)
    ;;
  *)
    exit 0
    ;;
esac

OUT=$(python3 "$CLAUDE_PROJECT_DIR/wiki/tools/lint.py" 2>&1)
if [ $? -ne 0 ]; then
  echo "wiki lint failed after editing $FILE:" >&2
  printf '%s\n' "$OUT" | grep -A100 'ERRORS' | head -30 >&2
  exit 2
fi
exit 0
