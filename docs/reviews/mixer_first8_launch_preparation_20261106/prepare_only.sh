#!/usr/bin/env bash
# Deliberate hard stop. This package has no remote/execution implementation.
# Future execution requires a separately reviewed implementation and pinned GO.
printf '%s\n' 'PREPARATION_ONLY: all actions disabled; see commands.txt and blockers.json. No GO environment variable enables this file.' >&2
exit 64
