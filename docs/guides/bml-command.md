---
title: bml command
created: 2026-08-20
updated: 2026-08-24
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
./tools/bml install                   # 링크 + 셸 설정의 PATH 한 줄
export PATH="$HOME/.local/bin:$PATH"  # 지금 이 터미널에 반영
bml                                   # 의존성·빌드·실행까지 알아서
```

DFT 판도 쓰고 있다면 위 "프로젝트가 둘" 절의 `worktree` 방법을 쓰세요.

의존성은 `bml` 이 처음 실행될 때 설치합니다. git 설정까지 한 번에 하려면
`make setup` 을 쓰세요 — `install` 도 그 안에 들어 있습니다.

### `bml: command not found` — 실제로 걸린 자리

`install` 은 `~/.local/bin/` 에 `bml` · `bmlin` · `bmlout` 세 개를 쓰고,
`$SHELL` 에 맞는 셸 설정(`~/.bashrc` 또는 `~/.zshrc`)에 PATH 한 줄을 넣습니다.
같은 줄을 두 번 넣지는 않습니다.

세 개는 심볼릭 링크가 아니라 **저장소의 `tools/bml` 을 부르는 껍데기 한 장**
입니다. 링크였을 때는 가리키는 파일이 사라지면 bash 가
`No such file or directory` 한 줄만 뱉었고, 그 문장에는 *무엇이* 없는지가
없어서 사람은 자기가 명령을 잘못 친 줄 알았습니다. 껍데기는 저장소가
통째로 없어진 것인지, 브랜치가 넘어가서 그 파일만 없는 것인지 보고 그때
맞는 명령을 줍니다.

**그 줄은 새 터미널에서만 읽힙니다.** 그래서 위 블록의 `export` 한 줄이
따로 있습니다 — 이걸 빼면 `install` 을 했는데도 바로 다음 줄에서
`command not found` 가 나고, 사람은 설치가 실패한 줄 압니다. 노트북에
깔면서 실제로 그렇게 됐습니다.

막히면:

```bash
which bml          # ~/.local/bin/bml 이 나와야 합니다
bml doctor         # PATH·WSL·python3-venv·node·CRLF·포트를 한 번에 짚습니다
```

`doctor` 는 PATH 의 `bml` 이 **다른 트리**를 가리키는 경우도 경고합니다.
worktree 를 둘 쓰면 한쪽에서 고친 것이 다른 쪽에서 안 보이기 때문입니다.

저장소 안에서는 언제든 `./tools/bml <명령>` 으로 경로째 부를 수 있습니다 —
PATH 문제와 무관하게 항상 됩니다.

다른 위치에 두고 싶으면 인자로 줍니다: `./tools/bml install /usr/local/bin`
(권한이 필요하면 `sudo`).

### 그 기계가 중추 서버가 아니라면 — `bml use` 까지 해야 끝입니다

**여기서 멈추면 안 됩니다.** 남의 컴퓨터·노트북에서 그냥 `bml` 을 치면
**그 기계에** 서버가 뜹니다. 데이터는 git 을 타고 오지 않으므로 셀이 0개인
멀쩡한 화면이 뜨고, 주소까지 똑같은 `localhost:5003` 이라 어느 쪽을 보고
있는지 화면으로는 구분이 안 됩니다 — 데이터가 날아간 것처럼 보입니다.

```bash
bml use 192.168.0.40    # 중추 서버의 LAN 주소 (포트 생략하면 5003)
bml
bml status              # 원본 개수가 중추 서버와 같아야 합니다
```

주소는 중추 서버에서 `bml status` 의 `접속 주소` 줄이 알려 줍니다.
`bml use` 는 **닿는 것을 확인한 뒤에만** 저장하므로, 저장이 안 되면 주소를
잘못 쓴 것이 아니라 중추 서버가 아직 안 열린 것입니다 (그쪽 `WORKBENCH_HOST`,
Windows 방화벽, WSL portproxy — [[central-server]] 참고).

그 기계에는 **`.bml/env` 를 직접 만들지 마세요.** `WORKBENCH_DATA` /
`WORKBENCH_HOST` 는 중추 서버 한 대만 하는 설정입니다. `bml use` 가 알아서
한 줄만 적습니다.

중추 서버에서도 그 파일을 **손으로 덮어쓰지 않습니다.** 한 줄을 넣는 가장 쉬운
방법이 `cat > .bml/env` 인데, 그러면 나머지 줄이 함께 사라집니다 — 실제로 그렇게
`WORKBENCH_HOST` 가 날아가서 서버는 떠 있는데 노트북이 못 붙었습니다.
`bml data` · `bml host` · `bml password` · `bml use` 는 각각 자기 줄만 고칩니다.

브라우저로 보기만 할 사람은 이 절 전체가 필요 없습니다 — 중추 서버 주소를
그냥 열면 됩니다. 설치할 것이 없습니다.

**alias 로 쓰고 싶다면** (`install` 대신):

```bash
echo "alias bml='$HOME/bml/tools/bml'" >> ~/.zshrc   # 클론한 폴더 경로로
```

`install` 쪽을 권합니다. **어느 디렉터리에서 쳐도** 동작하는 것은 둘 다
같지만, alias 는 `bmlin`/`bmlout` 을 따로 걸어야 하고, 파일이 사라졌을 때
셸이 주는 것은 여전히 `No such file or directory` 한 줄뿐입니다.

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
| `bml data` | 데이터가 어느 폴더에 있는지 (`.wrd` 개수까지) |
| `bml data <경로>` | 데이터를 그 폴더로 — 없는 폴더는 적지 않는다 |
| `bml data off` | 저장소 안의 `data/` 로 되돌린다 (원본은 그 드라이브에 그대로) |
| `bml host open` | 이 서버를 네트워크에 연다 (다른 기계가 보게) |
| `bml host local` | 이 기계 안에서만 |
| `bml password <암호>` | 바깥에 열 때 쓸 공유 암호 (6자 이상) |
| `bml share` | 임시 터널 — 다른 공유기에 있는 사람도 접속 |
| `bml share stop` | 그 터널을 닫는다 (`bml stop` 도 함께 닫는다) |
| `bml mirrored` | WSL 을 mirrored 네트워크로 — 다른 기계가 이 서버를 보게 (WSL 에서 실행) |
| `bmlin [주소]` | 랩 안(LAN) 주소로 갈아 끼우고 연다 — 주소는 한 번만 적으면 됩니다 |
| `bmlout [주소]` | 밖(터널) 주소로 갈아 끼우고 연다 — 터널은 열 때마다 주소가 바뀔 수 있습니다 |
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

**`bml 을 찾지 못했습니다` — 저장소는 있는데 그 파일이 없다고 합니다**
: 그 폴더가 다른 브랜치로 넘어갔습니다 (DFT 판이나 원고 판을 체크아웃했거나,
  누가 `git switch` 를 했거나). 이 저장소에는 프로젝트가 셋이고, 브랜치를
  바꾸면 상대 프로젝트 파일이 통째로 사라집니다. 화면이 주는
  `git -C <폴더> switch claude/battery-charge-discharge-webapp-dq4ja3` 을
  그대로 실행하면 돌아옵니다. 두 브랜치를 같이 써야 하면 위 "프로젝트가 둘"
  절대로 폴더를 나누세요 (`git worktree add`) — 같은 폴더에서 오가면 이
  일이 반복됩니다.

  (실측: 2026-08-24 에 중추 서버가 `claude/sdcp-dem-manuscript-si-pqwtv8`
  로 넘어가 있었고, 화면에 남은 것은 `No such file or directory` 한 줄뿐
  이었습니다. 그래서 `install` 이 링크 대신 껍데기를 쓰게 바꿨습니다.)

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
