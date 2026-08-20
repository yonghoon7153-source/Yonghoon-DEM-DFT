---
title: bml command
created: 2026-08-20
updated: 2026-08-20
type: guide
tags: [tooling, workflow]
sources: [docs/adr/0003-timeseries-on-disk-summaries-in-db.md]
confidence: high
explored: false
verificationStatus: unverified
---

# `bml` — 한 줄로 최신화 + 실행

두 사람이 같은 브랜치를 씁니다. 실행 전에 pull 을 잊으면 상대 작업이 없는
채로 보게 되고, 나중에 rebase 충돌이 커집니다. `bml` 은 그 순서를 강제합니다:

```
pull --rebase --autostash  →  의존성 확인  →  필요하면 빌드  →  실행
```

작업 중이던 변경이 있어도 `--autostash` 가 알아서 넣었다 빼주므로, 커밋하지
않은 상태에서 그냥 `bml` 을 치면 됩니다.

## 설치 (각자 한 번만)

작업은 `claude/battery-charge-discharge-webapp-dq4ja3` 브랜치에 있습니다. `main` 은 비어 있으니 **`-b` 로 지정해
클론**하세요.

```bash
git clone -b claude/battery-charge-discharge-webapp-dq4ja3 \
  https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT.git
cd Yonghoon-DEM-DFT
./tools/bml install     # ~/.local/bin/bml 로 심볼릭 링크
bml                     # 의존성·빌드·실행까지 알아서
```

의존성은 `bml` 이 처음 실행될 때 설치합니다. git 설정까지 한 번에 하려면
`make setup` 을 써도 됩니다.

`~/.local/bin` 이 PATH 에 없다는 경고가 나오면 셸 설정에 한 줄 추가하고 새
터미널을 엽니다:

```bash
# bash → ~/.bashrc   ·   zsh → ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

다른 위치에 두고 싶으면 인자로 줍니다: `./tools/bml install /usr/local/bin`
(권한이 필요하면 `sudo`).

**alias 로 쓰고 싶다면** (심볼릭 링크 대신):

```bash
echo "alias bml='$HOME/경로/Yonghoon-DEM-DFT/tools/bml'" >> ~/.zshrc
```

심볼릭 링크 쪽을 권합니다 — 스크립트가 링크를 따라가 저장소 위치를 스스로
찾으므로 **어느 디렉터리에서 쳐도** 동작합니다.

## 쓰는 법

| 명령 | 하는 일 |
|---|---|
| `bml` | 최신으로 맞추고 웹앱 실행 → http://localhost:5003 |
| `bml dev` | 같은 주소, 핫 리로드 (코드 고칠 때) |
| `bml stop` | 내리기 |
| `bml restart` | 내리고 다시 (pull 포함) |
| `bml status` | 지금 뭐가 돌고 있는지 + 브랜치/미커밋/ahead·behind |
| `bml pull` | 실행 없이 최신화만 |
| `bml check` | 커밋 전 검사 (pytest · tsc · vitest · eslint · ruff · docs) |
| `bml logs` | 서버 로그 따라가기 |
| `bml help` | 도움말 |

### 하루 흐름

```bash
bml              # 아침 — 최신으로 맞추고 띄운다
                 # ... 데이터 보고, .wrd 올리고 ...
bml stop         # 퇴근
```

코드를 고치는 날이면:

```bash
bml dev          # 핫 리로드로 띄우고
                 # ... 고치고 ...
bml check        # 커밋 전 검사
git add -A && git commit -m "fix: ..." && git push
```

## 주소가 항상 같습니다

`bml` 과 `bml dev` 둘 다 **http://localhost:5003** 입니다. 북마크 하나면 됩니다.

- `bml` — FastAPI 한 프로세스가 API(`/api`)와 빌드된 웹앱을 같이 서빙합니다.
  node 프로세스가 뜨지 않아 가볍고, 계측 PC 에 그냥 띄워 두기 좋습니다.
- `bml dev` — Vite 가 5003 에서 화면을 서빙하고 `/api` 는 뒤의 8000 으로
  넘깁니다. 파일을 고치면 즉시 반영됩니다.

포트를 바꾸려면:

```bash
WORKBENCH_PORT=6001 bml
```

## 무슨 일이 일어나는지

1. **pull** — `git pull --rebase --autostash`. 실패해도 로컬 상태로 계속
   진행하되 경고합니다. rebase 가 걸려 있으면 멈추고 해결하라고 알려 줍니다.
   최근 커밋 3개를 보여 주므로 상대가 뭘 했는지 바로 보입니다.
2. **의존성** — `requirements.txt` · `pyproject.toml` · `package-lock.json` 의
   해시를 `.bml/deps.stamp` 에 기록해 두고, 바뀌었을 때만 다시 설치합니다.
   상대가 패키지를 추가해도 `bml` 한 번이면 따라잡습니다.
   처음 실행은 1~3분 걸립니다 (가상환경 생성 + 설치).
3. **빌드** — `apps/web/src` 가 `dist` 보다 새로울 때만 다시 빌드합니다.
4. **실행** — 이미 떠 있으면 새로 띄우지 않고 그 주소를 알려 줍니다.

## 자주 나오는 상황

**포트 5003 이 사용 중이라고 나옵니다**
: 이전에 띄운 게 남아 있습니다. `bml stop` 후 다시. 다른 프로그램이 쓰고 있다면
  `WORKBENCH_PORT=6001 bml` 로 옮기세요.

**pull 이 충돌났습니다**
: 코드는 양쪽 의도를 확인해 합칩니다. `docs/log.md` 는 append-only 이므로
  **양쪽 항목을 모두 남깁니다**. 자세한 규칙은 `CLAUDE.md` 2장.

**`bml: command not found`**
: PATH 에 `~/.local/bin` 이 없습니다. 위의 `export PATH=...` 를 추가하고 새
  터미널을 여세요. 급하면 `./tools/bml` 로 직접 실행해도 됩니다.

**서버가 안 뜹니다**
: `bml logs` 로 마지막 로그를 봅니다. 빌드 실패면 `bml check` 가 원인을
  보여 줍니다.

**데이터는 어디 있나요**
: `data/uploads/` 에 올린 `.wrd` 원본, `data/runs/` 에 파싱 캐시,
  `data/workbench.db` 에 요약이 들어갑니다. **git 에는 올라가지 않습니다** —
  두 사람이 각자의 데이터를 가집니다. 같은 데이터를 보려면 `data/` 를 공유
  드라이브에 두고 `WORKBENCH_DATA` 로 가리키세요:

```bash
WORKBENCH_DATA=/srv/battery-data bml
```

## 관련

- [[wsl-setup]] — Windows/WSL 에서 쓸 때의 준비와 함정
- [[extension-roadmap]] — 다음에 붙일 분석
- `CLAUDE.md` 2장 — 2인 공용 git 규칙 전문
- `.claude/skills/shared-branch-workflow/SKILL.md` — 에이전트용 같은 규칙
