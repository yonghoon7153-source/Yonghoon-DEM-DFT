---
name: shared-branch-workflow
description: The two-person git flow for this repository — rebase with autostash, small commits, and the specific conflict rules for log.md and lockfiles.
when_to_use: At the start of any session, before any commit, and whenever a push is rejected.
---

# Shared-branch workflow

Two people work on the same branch from terminals. Everything below exists to
keep that from producing duplicate work or a tangled history.

## Session start — always

```bash
make sync      # git pull --rebase --autostash
```

`--autostash` shelves uncommitted work, rebases, and puts it back. There is no
"I have changes so I cannot pull" state. Run it before you read the code, not
after you have written some.

Then look at what the other person did:

```bash
git log --oneline -15
```

## Before a commit

```bash
make check     # tests + lint + docs lint
```

Commit small and often. A large commit is a large rebase conflict.

Prefixes: `feat:` `fix:` `docs:` `test:` `refactor:` `ingest:` `update:`
`create:` `lint:` `verify:`.

## When push is rejected

```
! [rejected] ... (non-fast-forward)
```

means the other person pushed first.

```bash
make sync && make check && git push
```

**Never `--force`.** On a shared branch it deletes their commits.

## Conflict rules

| File | Rule |
|---|---|
| `docs/log.md` | append-only — **keep both sides** |
| `docs/index.md` | keep both entries, recount `Total pages` |
| `package-lock.json`, `uv.lock` | do not hand-edit; regenerate with the tool |
| source | read both intents and merge; never take one side wholesale |

After resolving, `make check` must pass before `git rebase --continue`.

## Avoiding duplicate work

Announce long work in `docs/log.md` before starting:

```markdown
## [2026-08-20] start | EIS 파서 조사
```

The other person sees it on their next `make sync`.

For work that will hold a file open for hours, branch instead:

```bash
git switch -c claude/<topic>
# ... when done
git switch <shared-branch> && make sync && git merge claude/<topic>
```

## Never rewrite pushed history

`git rebase -i`, `git commit --amend` and `git push --force` are fine on local
commits nobody has pulled. On anything already pushed they break the other
person's checkout. If a pushed commit is wrong, add a commit that fixes it.

## Never commit

`data/` (uploaded originals and parse caches), `*.wrd`, `.venv/`,
`node_modules/`, `*.db`, `.env`. They are in `.gitignore`, but check
`git status` before `git add -A` anyway.
