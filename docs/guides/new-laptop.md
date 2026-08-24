---
title: new laptop
created: 2026-08-24
updated: 2026-08-24
type: guide
tags: [tooling, workflow, wsl, onboarding]
sources: [tools/bml, docs/adr/0011-central-instance-for-data.md, docs/guides/wsl-setup.md]
confidence: high
explored: true
verificationStatus: verified
verifiedAt: 2026-08-24
---

# 새 노트북 한 대 붙이기 — `wsl --install` 부터

중추 서버(데스크톱)는 이미 떠 있다는 전제다. 이 문서는 **새 노트북**에서
그것을 보게 하는 데까지다. 전부 붙여넣을 수 있게 적었다.

**중추 서버를 보기만 할 기계는 가벼운 편이다.** `bml` 이 중추 서버를 열 때는
파이썬 가상환경도 프론트엔드 빌드도 하지 않는다 — `git` 과 `curl` 만 있으면
된다. 데이터도 안 받는다 (그건 중추 서버 한 대에만 있다 — ADR 0011).

## 1. Windows 쪽 (관리자 PowerShell, 한 번)

```powershell
wsl --install
```

재부팅 뒤 Ubuntu 창이 뜨고 사용자 이름·암호를 묻는다. 여기서 막히면
[[wsl-setup]] 0번 절로 간다 — `0x80370114` 는 가상화가 꺼져 있다는 뜻인데
**오류 문구에 '가상화' 라는 말이 한 번도 안 나온다.**

## 2. `.exe` 가 도는지 먼저 본다

WSL 터미널에서:

```bash
ipconfig.exe | head -3
```

주소가 나오면 (글자가 깨져 보여도 정상 — CP949 다) 넘어간다.
`cannot execute binary file: Exec format error` 가 나오면 **interop 이 죽은
것**이다. 거의 항상 `/etc/wsl.conf` 의 `systemd=true` 때문이다: systemd 는
WSL 안에서 `systemd-binfmt` 를 건너뛰므로(`ConditionVirtualization=!wsl`),
`.exe` 를 `/init` 에 넘기는 등록을 아무도 걸지 않는다.

```bash
# 지금 살리기 (커널에 직접, systemd 를 안 거친다)
sudo sh -c 'echo ":WSLInterop:M::MZ::/init:PF" > /proc/sys/fs/binfmt_misc/register'
ipconfig.exe | head -3

# 다음 부팅에도 살리기 — 조건을 비워야 그 서비스가 돈다
sudo mkdir -p /etc/systemd/system/systemd-binfmt.service.d
sudo sh -c 'printf "[Unit]\nConditionVirtualization=\n" > /etc/systemd/system/systemd-binfmt.service.d/wsl.conf'
sudo sh -c 'echo :WSLInterop:M::MZ::/init:PF > /usr/lib/binfmt.d/WSLInterop.conf'
sudo systemctl daemon-reload && sudo systemctl restart systemd-binfmt
```

`/etc/wsl.conf` 에 `systemd=true` 가 꼭 필요한 게 아니면 그 줄을 지우고
PowerShell 에서 `wsl --shutdown` 해도 된다 — 이 워크벤치는 systemd 를 안 쓴다.

**이게 죽어 있으면** `bml mirrored` 도, `bml status` 의 LAN 주소 읽기도, WSL
안에서 `wsl.exe --shutdown` 을 부르는 것도 안 된다. `bml doctor` 가 짚어 준다.

## 3. 저장소를 받는다

```bash
sudo apt update && sudo apt install -y git curl
cd ~
git clone -b claude/battery-charge-discharge-webapp-dq4ja3 \
  https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT.git
cd Yonghoon-DEM-DFT
make setup-git          # pull.rebase, autostash, 커밋 훅
```

**브랜치를 반드시 적는다.** `main` 은 비어 있고, 이 워크벤치의 집은
`claude/battery-charge-discharge-webapp-dq4ja3` 다 (ADR 0009). 그리고 **한 작업
폴더에서 브랜치를 오가지 않는다** — 바꾸는 순간 상대 프로젝트 파일이 사라진다.

## 4. `bml` 을 PATH 에 건다

```bash
./tools/bml install
exec $SHELL -l          # 새 PATH 를 이 터미널에 반영
```

`bml` · `bmlin` · `bmlout` 세 이름이 걸린다. 셋 다 저장소의 `tools/bml` 을
부르는 껍데기라, `bml` 을 고치면 나머지도 같이 따라온다. 저장소 폴더를 옮겼거나
브랜치를 바꿔서 그 파일이 없어지면, 껍데기가 어느 쪽인지 보고 맞는 명령을 준다.

## 5. 볼 주소를 정한다 — `bmlin` / `bmlout`

주소는 **두 자리**로 따로 기억한다. 성격이 다르기 때문이다: LAN 주소는 한 번
정하면 안 바뀌고, 터널 주소는 **열 때마다 달라질 수 있다.**

```bash
# 랩 안에서 쓸 주소 — 중추 서버의 `bml status` 의 '접속 주소' 줄
bmlin 192.168.0.40

# 밖에서 쓸 주소 — 중추 서버에서 `bml share` 가 알려 준 것
bmlout https://3ff01ea5035fa6.lhr.life
```

한 번 적어 두면 그다음부터는 **주소 없이** 자리만 바꾼다:

```bash
bmlin      # 랩에 오면
bmlout     # 밖에 나가면
```

닿는지 확인한 뒤에만 갈아 끼운다. 실패해도 **적어 둔 주소는 지우지 않는다** —
자리를 옮기는 중일 뿐일 수 있다. 그리고 한쪽이 안 되면 반대쪽을 짚어 준다.

`bml status` 가 두 자리를 다 보여 주고 지금 붙은 쪽에 `●` 를 찍는다.

## 6. 그다음부터

```bash
bml           # 최신화 + 중추 서버 열기 (자리는 마지막에 고른 것)
bml status    # 어디에 붙어 있나, 무엇이 떠 있나
bml doctor    # 환경이 이상하면 여기부터
```

브라우저가 **암호를 한 번 묻는다** (중추 서버에 공유 암호가 걸려 있을 때).
쿠키는 한 달 간다.

## 자주 걸리는 것

**`bmlin` 이 8초 만에 timeout**
: 지금 그 망에 중추 서버가 없다. 밖이면 `bmlout`.

**`bmlout` 이 `HTTP 503`**
: 주소는 살아 있는데 그 뒤에 서버가 없다 — 중추 서버 쪽 터널이 끊긴 것이다.
  그 기계에서 `bml share stop` 후 `bml share`, 새 주소로 `bmlout <새 주소>`.

**`bmlout` 이 `Could not resolve host`**
: 이름 자체를 못 찾았다. 랩 망은 터널 도메인(`lhr.life`)을 DNS 에서 거르는
  일이 흔하다 — **랩 안에서는 터널을 쓰지 말고 `bmlin` 을 쓴다.** 밖인데도
  이러면 터널이 닫힌 것이다.

**셀이 0개인 멀쩡한 화면**
: 자기 서버를 보고 있다. `bml status` 에 `중추 서버 …` 줄이 없으면 그것이다.
  `bmlin` 또는 `bmlout` 으로 붙인다.

**`bml` 이 포트 5003 충돌로 죽는다**
: `bml stop`. 그래도 남고 이 기계가 mirrored WSL 이면 **Windows 쪽이 잡은
  포트**일 수 있다 — 그건 WSL 안에서 못 끈다. 화면이 짚어 주는 대로
  `netsh interface portproxy reset`(관리자 PowerShell) 을 먼저 본다.

## 관련

- [[wsl-setup]] — WSL 설치가 막힐 때, 그리고 Windows/WSL 함정 전부
- [[central-server]] — 중추 서버 쪽 설정 (주소·방화벽·mirrored·터널)
- [[bml-command]] — `bml` 명령 전체
- [[getting-started]] — 화면 쓰는 법 (올리기·질량·조성)
