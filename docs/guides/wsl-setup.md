---
title: wsl setup
created: 2026-08-20
updated: 2026-08-20
type: guide
tags: [tooling, workflow, wsl]
sources: [docs/guides/bml-command.md]
confidence: high
explored: false
verificationStatus: unverified
---

# WSL 에서 쓰기

Windows + WSL 에서 `bml` 로 워크벤치를 띄우는 방법. 막히면 먼저:

```bash
bml doctor
```

환경을 점검하고 **무엇을 어떻게 고쳐야 하는지**까지 알려 줍니다.

## 0. WSL 설치 (한 번)

PowerShell 을 **관리자로** 열고:

```powershell
wsl --install
```

재부팅하면 Ubuntu 가 뜨고 사용자 이름·비밀번호를 묻습니다. 이미 있다면
WSL2 인지 확인하세요 (WSL1 은 네트워크·성능이 다릅니다):

```powershell
wsl -l -v          # VERSION 이 2 여야 합니다
wsl --set-version Ubuntu 2   # 1 이면 변환
```

## 1. 필요한 패키지

Ubuntu 는 `python3-venv` 를 **기본으로 넣어 주지 않습니다.** 이게 WSL 에서
가장 많이 걸리는 지점입니다.

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git curl build-essential
```

Node 는 Ubuntu 저장소 버전이 너무 낮습니다 (18 이상 필요):

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
node -v          # v22.x
```

브라우저를 WSL 에서 열려면 (선택, 있으면 깔끔합니다):

```bash
sudo apt install -y wslu
```

## 2. git 줄바꿈 설정 — **먼저 하세요**

Windows 쪽 git 이 스크립트를 CRLF 로 체크아웃하면 WSL 의 bash 가
`bad interpreter: No such file or directory` 로 죽습니다. 메시지에 줄바꿈
얘기가 전혀 없어서 원인을 찾는 데 한참 걸립니다.

```bash
git config --global core.autocrlf input
```

저장소에 `.gitattributes` 가 있어 새로 클론하면 문제가 없지만, 위 설정을
해 두면 다른 저장소에서도 안 겪습니다.

**이미 겪었다면:**

```bash
cd ~/Yonghoon-DEM-DFT
git config core.autocrlf false
git rm --cached -r . && git reset --hard
```

## 3. 저장소는 WSL 안에 — `/mnt/c` 에 두지 마세요

```bash
cd ~
git clone https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT.git
cd Yonghoon-DEM-DFT
```

`/mnt/c/...` (Windows 드라이브) 에 두면 파일 접근이 **10배 이상 느리고**,
`bml dev` 의 자동 새로고침이 파일 변경을 놓칩니다. `bml doctor` 가 이걸
발견하면 경고합니다.

> `.wrd` 원본은 Windows 쪽(`C:\Zive Data\...`)에 있어도 됩니다. 업로드할 때만
> 읽으므로 느려도 상관없습니다. WSL 에서는 `/mnt/c/Zive Data/...` 로 보입니다.

## 4. 설치

```bash
make setup
```

git 설정 · 의존성 · `bml` 등록까지 한 번에 합니다. 처음이라 1~3분 걸립니다.

`~/.local/bin` 이 PATH 에 없다는 경고가 나오면:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
exec bash
```

## 5. 실행

```bash
bml
```

`http://localhost:5003` 이 Windows 기본 브라우저에서 열립니다. WSL2 는
localhost 를 Windows 쪽으로 자동 포워딩하므로 주소는 그대로입니다.

| | |
|---|---|
| `bml` | 최신화 + 실행 |
| `bml dev` | 핫 리로드 |
| `bml stop` | 내리기 |
| `bml status` | 실행 상태 |
| `bml doctor` | 환경 점검 |

## PowerShell 에서 바로 치고 싶다면

`tools/bml.cmd` 를 Windows PATH 에 있는 폴더로 복사하면 WSL 에 들어가지 않고도
`bml` 을 칠 수 있습니다. PowerShell 에서:

```powershell
mkdir "$env:USERPROFILE\bin" -Force
copy \\wsl$\Ubuntu\home\<사용자>\Yonghoon-DEM-DFT\tools\bml.cmd "$env:USERPROFILE\bin\"
[Environment]::SetEnvironmentVariable("Path", "$env:Path;$env:USERPROFILE\bin", "User")
```

새 PowerShell 창에서:

```powershell
bml
bml stop
```

배포판이 여러 개면 하나를 지정합니다:

```powershell
setx BML_WSL_DISTRO Ubuntu
```

## 안 될 때

**`bml: command not found`**
: PATH 문제입니다. 4번의 `export PATH=...` 를 하고 새 터미널을 여세요.
  급하면 `~/Yonghoon-DEM-DFT/tools/bml` 로 직접 실행됩니다.

**`bad interpreter: No such file or directory`**
: CRLF 입니다. 2번을 하세요.

**`ensurepip is not available`** / venv 생성 실패
: `sudo apt install -y python3-venv`.

**브라우저가 안 열립니다**
: 주소를 직접 여세요 — `http://localhost:5003`.
  `sudo apt install wslu` 하면 자동으로 열립니다.

**Windows 브라우저에서 localhost:5003 이 안 열립니다**
: WSL2 의 localhost 포워딩이 꺼져 있을 수 있습니다. 두 가지 방법:

```bash
# 1) WSL IP 로 직접 (bml doctor 가 알려 줍니다)
hostname -I | awk '{print $1}'      # 예: 172.20.1.5 → http://172.20.1.5:5003

# 2) 모든 인터페이스에 바인딩
WORKBENCH_HOST=0.0.0.0 bml
```

포워딩 자체를 켜려면 Windows 쪽 `%USERPROFILE%\.wslconfig` 에:

```ini
[wsl2]
localhostForwarding=true
```

그리고 `wsl --shutdown` 후 다시 시작합니다.

**포트 5003 이 이미 쓰이고 있습니다**
: `bml stop`. Windows 쪽 프로그램이 잡고 있으면
  `WORKBENCH_PORT=6001 bml` 로 옮기세요.

**`bml dev` 인데 파일을 고쳐도 안 바뀝니다**
: 저장소가 `/mnt/c` 에 있으면 파일 변경 감지가 동작하지 않습니다. 3번대로
  WSL 안으로 옮기세요.

**WSL 을 껐다 켜고 싶다**
: PowerShell 에서 `wsl --shutdown`. 다음 `bml` 이 알아서 다시 띄웁니다.

## 두 사람이 같이 쓸 때

각자 자기 WSL 에 클론하고 각자 `bml` 을 씁니다. 데이터(`data/`)는 git 에
올라가지 않으므로 각자의 것입니다. 같은 데이터를 보려면 공유 위치를
가리키세요:

```bash
WORKBENCH_DATA=/mnt/c/Users/공용/battery-data bml
```

git 규칙(pull --rebase --autostash, 충돌 처리)은 [[bml-command]] 와
`CLAUDE.md` 2장에 있습니다.

## 관련

- [[bml-command]] — `bml` 명령 전체 설명
- [[extension-roadmap]] — 다음에 붙일 분석
