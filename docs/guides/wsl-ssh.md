---
title: wsl ssh
created: 2026-09-16
updated: 2026-09-16
type: guide
tags: [tooling, workflow, wsl, network]
sources: [tools/bml, docs/guides/wsl-setup.md]
confidence: high
explored: false
verificationStatus: unverified
---

# 노트북에서 이 WSL 로 ssh — `bml ssh`

워크벤치를 여는 주소와 **같은 주소**다. `bmlin` 이 `192.168.0.40` 을 쓰면 ssh 도
거기로 간다. 다른 것은 포트 하나뿐이다.

```bash
bml ssh            # 켠다 (필요하면 openssh-server 설치까지)
bml ssh status     # 지금 상태만
bml ssh off        # 닫는다
```

## 왜 22 번이 아닌가

Windows 10/11 에는 OpenSSH **서버**가 선택 기능으로 들어 있다. 켜 두면 22 번을
잡는데, mirrored 네트워크에서는 WSL 이 Windows 의 망을 그대로 쓰므로 둘이 같은
포트를 놓고 다툰다. 그리고 **접속은 되긴 된다** — 다만 들어간 곳이 Windows 이고,
거기에는 저장소도 `.venv` 도 없다. "분명히 접속했는데 파일이 없다" 가 여기서
나온다.

기본값은 **2222** 다. 포트 번호가 곧 "어느 기계에 들어가는가" 가 된다. 바꾸고
싶으면 `.bml/env` 에:

```
WORKBENCH_SSH_PORT=2200
```

## 순서

### 1. WSL 안에서

```bash
bml ssh
```

- `openssh-server` 가 없으면 설치한다 (sudo 암호를 물을 수 있다).
- 호스트 키가 없으면 만든다.
- `/etc/ssh/sshd_config.d/bml.conf` 에 **우리 몫만** 쓴다 — 포트와
  "열쇠로만 로그인". `sshd_config` 자체는 건드리지 않으므로, 되돌리려면 그
  파일 하나만 지우면 된다 (`bml ssh off` 가 그렇게 한다).
- sshd 를 켜고, 그 포트를 정말 듣는지 확인한다.

**암호 로그인은 켜지 않는다.** WSL 계정은 암호가 없거나 약한 것이 보통이고,
이건 랜에 열어 두는 문이다. 한 번 뚫리면 저장소와 `data/` 가 그대로 딸려 간다.

### 2. Windows 쪽 — 관리자 PowerShell 에서 한 번

`bml ssh` 가 이 줄을 **채워서** 보여 준다. 관리자 권한이 필요해서 우리가 직접
돌리지는 않는다 (`bml mirrored` 와 같은 규칙: 짐작으로 남의 설정을 고치지 않는다).

```powershell
New-NetFirewallRule -DisplayName 'WSL ssh 2222' -Direction Inbound -Protocol TCP -LocalPort 2222 -Action Allow -Profile Private
```

`-Profile Private` 가 중요하다. 이걸 빼면 카페 와이파이에 붙었을 때도 열린다.

### 3. 네트워크가 mirrored 가 아니면 한 줄 더

```powershell
netsh interface portproxy add v4tov4 listenport=2222 listenaddress=0.0.0.0 connectport=2222 connectaddress=<이 WSL 의 주소>
```

`bml ssh` 가 그 주소를 읽어서 채워 준다. 다만 **NAT 에서는 WSL 주소가 다시 뜰
때마다 바뀐다** — 바뀌면 이 줄을 다시 넣어야 한다.

그게 싫으면 한 번만:

```bash
bml mirrored
```

mirrored 로 바꾸면 포워딩이 아예 필요 없어진다 (워크벤치 포트 5003 도 마찬가지다).
WSL 을 처음 세우는 이야기는 [[wsl-setup]] 에 있다.

### 4. 노트북에서 — 열쇠를 한 번

```bash
ssh-keygen -t ed25519            # 이미 있으면 건너뛴다
ssh-copy-id -p 2222 <계정>@192.168.0.40
```

암호 로그인을 꺼 두었으므로 이 **한 번**은 그 기계 앞에서 하거나, 노트북의
공개키(`~/.ssh/id_ed25519.pub`)를 WSL 의 `~/.ssh/authorized_keys` 에 직접 붙여
넣는다.

그 뒤로는:

```bash
ssh -p 2222 <계정>@192.168.0.40
```

## 제일 자주 걸리는 자리

**WSL 이 떠 있어야 닿는다.**

창을 다 닫으면 WSL 은 잠시 뒤 스스로 내려간다. 그러면 sshd 도 같이 사라지고,
노트북에서는 `Connection refused` 만 보인다 — 방화벽도 포워딩도 멀쩡한데.

- 워크벤치를 띄워 두면 (`bml`) 그 프로세스가 WSL 을 붙잡아 둔다. 랩의 중추
  서버라면 어차피 늘 떠 있어야 하므로 이것으로 끝이다.
- `systemd` 를 안 쓰는 WSL 은 **다시 뜰 때 sshd 가 꺼져 있다.** `/etc/wsl.conf` 에

  ```
  [boot]
  systemd=true
  ```

  를 넣고 `wsl --shutdown` 한 번이면, 그 뒤로는 WSL 이 뜰 때마다 같이 켜진다.

## 닫기

```bash
bml ssh off
```

우리가 쓴 설정 조각을 지우고 sshd 를 멈춘다. Windows 쪽 방화벽 규칙은 그대로
두고 지우는 명령만 알려 준다 — 그 규칙을 우리가 만든 것이 아닐 수도 있고,
다른 용도로 쓰고 있을 수 있다.

```powershell
Remove-NetFirewallRule -DisplayName 'WSL ssh 2222'
```

## 밖에서 (다른 공유기에서) 들어와야 한다면

이 문은 **같은 공유기 안**에서만 열린다. 밖에서 들어오는 것은 다른 문제이고,
이 저장소의 답은 ADR 0034 의 VPS 다 — 포트를 인터넷에 직접 여는 것이 아니라
우리 VPS 를 거친다. [[vps-first-run]] 을 보라.

명령 전체 목록은 [[bml-command]] 에 있다.
