---
title: bml command
created: 2026-08-20
updated: 2026-08-20
type: guide
tags: [tooling, workflow]
sources: [docs/adr/0003-timeseries-on-disk-summaries-in-db.md, docs/adr/0009-branch-is-the-home.md]
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

## 먼저: 이 저장소에는 프로젝트가 둘 있습니다

같은 저장소인데 **브랜치마다 내용이 완전히 다릅니다.**

| 브랜치 | 내용 | 실행 | 포트 |
| --- | --- | --- | --- |
| `claude/battery-charge-discharge-webapp-dq4ja3` | 충방전 워크벤치 (`apps/`, `packages/wrdkit`) | `bml` | 5003 |
| `claude/friendly-meitner-lldvar` | DFT 판 (`webapp/app.py`, `factory/`, `kb/`) | `dft` | 5001 |

그래서 **한 폴더에서 두 브랜치를 오가면 안 됩니다.** 브랜치를 바꾸는 순간
상대 프로젝트의 파일이 작업 폴더에서 통째로 사라지고, 그쪽 실행기는 원인 대신
`No such file or directory` 만 뱉습니다. 실제로 한 번 그렇게 DFT 판이 멈췄습니다.

각자 폴더를 주세요. `git worktree` 를 쓰면 저장소는 한 번만 받고 폴더만
둘로 나눌 수 있습니다:

```bash
# DFT 판이 이미 ~/Yonghoon-DEM-DFT 에 있다면, 워크벤치는 옆에 따로 놓습니다
git -C ~/Yonghoon-DEM-DFT worktree add ~/bml \
  claude/battery-charge-discharge-webapp-dq4ja3
cd ~/bml
```

두 폴더는 각자 HEAD 를 가지므로 한쪽에서 pull 해도 다른 쪽은 그대로입니다.
포트도 5003 / 5001 로 겹치지 않습니다.

`bml` 은 워크벤치가 아닌 폴더에서 실행되면 **pull 하기 전에** 멈추고 위
방법을 안내합니다. 남의 브랜치를 rebase 하고 나서 알아차리면 이미 늦기
때문입니다.

## 설치 (각자 한 번만)

처음부터 받는 경우라면 **`-b` 로 브랜치를 지정해 클론**하세요. 이 프로젝트의
집은 그 브랜치이고 `main` 은 별개입니다 — 임시 우회가 아니라 정상 절차입니다.

```bash
git clone -b claude/battery-charge-discharge-webapp-dq4ja3 \
  https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT.git bml
cd bml
./tools/bml install     # ~/.local/bin/bml 로 심볼릭 링크
bml                     # 의존성·빌드·실행까지 알아서
```

DFT 판도 쓰고 있다면 위 "프로젝트가 둘" 절의 `worktree` 방법을 쓰세요.

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
echo "alias bml='$HOME/bml/tools/bml'" >> ~/.zshrc   # 클론한 폴더 경로로
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
| `bml use <주소>` | 이 기계가 볼 중추 서버를 정한다 — 그 뒤 `bml` 은 그것을 연다 |
| `bml use off` | 해제 (이 기계가 자기 서버를 띄운다) |
| `bml password <암호>` | 바깥에 열 때 쓸 공유 암호 (6자 이상) |
| `bml share` | 임시 터널 — 다른 공유기에 있는 사람도 접속 (켜는 동안만) |
| `bml check` | 커밋 전 검사 (pytest · tsc · vitest · eslint · ruff · docs · bml 회귀) |
| `bml doctor` | 환경 점검 — 안 되면 여기부터 |
| `bml repair` | 파이썬 환경을 새로 만든다 (의존성이 꼬였을 때) |
| `bml repair web` | `node_modules` 와 빌드를 새로 만든다 |
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
   pull 이 `tools/bml` 자신을 갱신했다면 **새 버전으로 다시 시작합니다**
   (`✓ bml 이 갱신됐습니다 — 새 버전으로 다시 시작합니다`). 안 그러면 방금
   받은 수정이 이번 실행에는 반영되지 않습니다.
2. **의존성** — `requirements.txt` · `requirements-dev.txt` ·
   `pyproject.toml` · `package-lock.json` 의
   해시를 `.bml/deps.stamp` 에 기록해 두고, 바뀌었을 때만 다시 설치합니다.
   상대가 패키지를 추가해도 `bml` 한 번이면 따라잡습니다.
   처음 실행은 1~3분 걸립니다 (가상환경 생성 + 설치).
3. **빌드** — `apps/web/src` 가 `dist` 보다 새로울 때만 다시 빌드합니다.
4. **실행** — 이미 떠 있으면 새로 띄우지 않고 그 주소를 알려 줍니다. 다만
   **떠 있는 것이 지금 코드인지 확인한 뒤**입니다: 그 서버가 어느 커밋으로
   떴는지(`.bml/server.head`)를 지금 HEAD 와 견주고, 표식이 없거나(옛 버전
   `bml` 이 띄운 서버) 화면 번들이 소스보다 낡았으면 갈아끼웁니다.

   > 이 확인이 없던 동안, pull 을 받아도 옛 화면이 계속 나왔습니다 — 새 버튼이
   > 안 보인다는 신고가 그것이었습니다. "돌고 있다" 와 "지금 코드를 돌고 있다"
   > 는 다릅니다.

## 실패하면 이유를 알려 줍니다

서버가 안 뜨면 트레이스백을 그대로 쏟지 않고, 무엇이 원인이고 무엇을 치면
되는지 한 줄로 말합니다:

```
! 서버가 시작하자마자 멈췄습니다.

  원인  가상환경의 async 패키지(sniffio/anyio)가 서로 안 맞습니다.
  해결  bml repair
```

알아보는 상황: 의존성 깨짐 · 패키지 누락 · 포트 점유 · DB 스키마 불일치 ·
앱 로딩 실패. 그 밖의 경우에는 로그 마지막 25줄을 보여 줍니다.

## 자주 나오는 상황

**포트 5003 이 사용 중이라고 나옵니다**
: `bml` 이 알아서 가려 줍니다. **자기가 띄운 서버**가 죽어 있으면 말없이
  갈아끼우고, **남의 프로그램**이면 죽이지 않고 pid·명령줄과 함께 멈춥니다
  (누군가의 실험이 돌고 있을 수 있으니까요). 남의 것이면
  `WORKBENCH_PORT=6001 bml` 로 옮기면 됩니다.

**pull 이 충돌났습니다**
: 코드는 양쪽 의도를 확인해 합칩니다. `docs/log.md` 는 append-only 이므로
  **양쪽 항목을 모두 남깁니다**. 자세한 규칙은 `CLAUDE.md` 2장.

**`bml: command not found`**
: PATH 에 `~/.local/bin` 이 없습니다. 위의 `export PATH=...` 를 추가하고 새
  터미널을 여세요. 급하면 `./tools/bml` 로 직접 실행해도 됩니다.

**갑자기 `tools/bml` 이 없다고 합니다**
: 그 폴더가 다른 브랜치로 넘어갔습니다 (DFT 판을 체크아웃했거나, 누가
  `git checkout` 을 했거나). 심볼릭 링크는 사라진 파일을 가리키고 있는
  상태입니다. 위 "프로젝트가 둘" 절의 방법으로 폴더를 나눈 뒤
  `cd ~/bml && ./tools/bml install` 로 링크를 다시 걸어 주세요.

**`bml` 이 "이 폴더에는 다른 프로젝트가 체크아웃돼 있습니다" 라고 멈춥니다**
: 의도된 정지입니다. 그 폴더는 DFT 판 같은 다른 프로젝트의 작업 폴더이고,
  거기서 pull 하면 남의 브랜치를 rebase 하게 됩니다. 메시지에 나온
  `git worktree add` 를 그대로 실행하세요.

**`bml` 이 "다른 폴더의 워크벤치가 쓰고 있습니다" 라고 멈춥니다**
: 워크벤치를 두 폴더에 두고 양쪽에서 띄운 상태입니다. 죽이지 않고 멈추는
  이유는 **폴더마다 `data/` 가 다르기 때문**입니다 — 조용히 갈아끼우면 올려 둔
  `.wrd` 가 사라진 것처럼 보입니다. 메시지가 그 폴더와 pid 를 알려 주니
  셋 중 하나를 고르세요: 그쪽을 계속 쓰거나, 그쪽을 `stop` 하고 이쪽을 띄우거나,
  `WORKBENCH_PORT` 로 둘 다 띄우거나.

**포트를 누가 쓰는지 모르겠습니다**
: 실패 메시지가 pid·명령줄·실행 위치를 함께 보여 줍니다. 대개 거기서
  정체가 드러납니다. `bml doctor` 도 같은 정보를 냅니다.

**서버가 안 뜹니다**
: 실패 메시지에 원인과 해결 명령이 함께 나옵니다. 그래도 모르겠으면
  `bml doctor` → `bml repair` 순으로 시도하세요. 빌드 실패면 `bml check` 가
  원인을 보여 줍니다.

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
