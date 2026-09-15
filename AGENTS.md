# AGENTS.md — Codex DEM/MPM worktree contract

이 파일은 Windows Codex와 WSL Ubuntu Claude가 같은 저장소를 병렬로 사용할 때의 고정 계약이다.

## Fixed identity

- Claude source branch: `claude/stoic-knuth-NObVQ`
- Codex work branch: `Codex/dem-mpm-crosscheck`
- Claude WSL checkout: `/home/yonghoon/Yonghoon-DEM-DFT-claude`
- Codex Windows worktree: `C:/Users/안용훈/Yonghoon-DEM-DFT-codex-dem-mpm`
- Codex WSL path: `/mnt/c/Users/안용훈/Yonghoon-DEM-DFT-codex-dem-mpm`

## Worktree safety

- 공용 checkout `C:/Users/안용훈/Yonghoon-DEM-DFT`에서 checkout/switch하지 않는다. 다른 채팅이 사용 중일 수 있다.
- Codex는 반드시 위 Codex worktree에서만 수정한다.
- 작업 전 `git status -sb`, `git worktree list`, 현재 브랜치와 HEAD를 확인한다.
- 기존 미추적·수정 파일은 이동, 삭제, stash, reset하지 않는다.
- `.git` worktree 연결은 Windows와 WSL이 모두 읽는 상대경로를 유지한다.
- PR은 사용자가 요청할 때만 만든다.
- force-push가 꼭 필요하고 사용자가 승인한 경우에도 `--force-with-lease`만 쓴다.

## When the user says “클로드 작업하고 왔어”

Codex worktree에서 다음 순서를 지킨다.

1. `git status -sb`를 확인한다.
2. 미커밋 변경이 있으면 rebase하지 않고 사용자에게 변경 파일을 먼저 알린다.
3. 깨끗하면 `git fetch origin`을 실행한다.
4. 아래로 Claude source branch의 신규 커밋과 변경 파일을 확인한다.

   ```bash
   git log --oneline HEAD..origin/claude/stoic-knuth-NObVQ
   git diff --name-status HEAD...origin/claude/stoic-knuth-NObVQ
   ```

5. `git rebase origin/claude/stoic-knuth-NObVQ`를 실행한다.
6. 충돌이 나면 임의로 버리거나 덮지 않는다. 충돌 파일, 양쪽 변경 의도, 충돌 원인을 사용자에게 보고한다.
7. 성공 후 현재 브랜치, HEAD, upstream, ahead/behind를 보고한다.
8. 그다음 사용자 요청 작업을 진행한다.

## Push contract

Codex branch를 처음 원격에 올릴 때만:

```bash
git push -u origin Codex/dem-mpm-crosscheck
```

upstream 설정 후에는:

```bash
git push
```

## DEM/MPM cross-review

- 기본은 한쪽이 구현하고 다른 쪽이 독립 검증한다. 같은 파일을 동시에 수정하지 않는다.
- Claude와 Codex가 병렬로 쓸 때는 소유 파일 범위를 먼저 나눈다.
- DEM과 MPM은 서로에게 맞춰 보정하지 않는다. 각각 실험에 독립 보정한 뒤 일치하면 교차검증, 불일치하면 모델 한계로 기록한다.
- DEM은 explicit contact/network transport, MPM은 plastic morphology/stress/strain을 주 역할로 둔다.
- 수치 검토에서는 unit/scale, pressure readout, sentinel, seed, grid resolution과 provenance를 확인한다.
