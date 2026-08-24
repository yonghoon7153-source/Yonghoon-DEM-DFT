# Codex 리뷰 과제 — 화면이 사람을 어디로 보내는가 (WSL·터널·주소 판정)

[codex-session-bootstrap.md](codex-session-bootstrap.md) 로 세션을 연 뒤, 맨
아래 "붙여넣는 프롬프트" 를 그대로 붙여넣는다.

이 리뷰는 **주제 하나**다: `tools/bml` 이 사람에게 무엇을 시키는가. 도메인
수치(mAh/g, knee, dQ/dV)는 이 변경이 한 줄도 건드리지 않았으므로 범위 밖이다.

## 왜 이 리뷰가 필요한가

이 묶음은 전부 **한 사람이 실제로 막힌 자리**에서 나왔다. 데스크톱(Windows
재설치 직후)을 중추 서버로 세우고 노트북에서 보게 하는 동안, 화면이 시키는
대로 했다가 틀린 일이 여섯 번 있었다. 고친 것은 계산이 아니라 **화면과 판정**
이고, 그래서 위험도 계산이 아니라 이런 것이다:

1. **화면이 사람을 틀린 데로 보낸다.** 파일 내용을 명령처럼 찍어서 PowerShell
   에 붙여넣게 만들었다. 살아 있는 터널을 "닫혔을 수도" 라고 해서 닫게 만들
   뻔했다. 이런 실패는 테스트가 통과해도 남는다.
2. **저장소 바깥을 건드리기 시작했다.** `bml mirrored` 는 Windows 쪽
   `%USERPROFILE%\.wslconfig` 를 **고친다.** 이 저장소가 자기 트리 밖의 파일을
   쓰는 것은 이번이 처음이다.
3. **판정이 조용히 틀리면 아무도 모른다.** 주소 하나를 잘못 고르면 "왜 안
   되지" 만 남는다. 실제로 그렇게 한 번 틀렸다 (`284a4582` — 랩 망이 172.x 라
   진짜 LAN 주소를 WSL 것으로 오해해 버렸다).

그리고 이 변경의 전부가 **셸 스크립트**다 (`tools/bml`, +611줄). 이 저장소에서
테스트가 가장 얇은 층이다.

## 범위

```bash
git log --oneline a7efba10..284a4582
git diff --stat a7efba10..284a4582
```

| 파일 | 무엇 |
|---|---|
| `tools/bml` | 아래 새 함수 18개 + `cmd_status`·`cmd_share`·`cmd_use` 화면 |
| `tools/tests/test_bml_client.sh` | +250줄 (89 → 151건) |
| `tools/tests/test_bml_tunnel.sh` | +51줄 (33 → 48건) |
| `docs/guides/central-server.md` | mirrored 두 길(A: `bml mirrored`, B: portproxy) |
| `docs/guides/wsl-setup.md`, `bml-command.md` | 한 줄씩 |
| `docs/log.md` | 커밋마다 한 항목 (`bml feed` 가 짝을 센다) |

새 함수:

```
file_line  win_exe  windows_ipconfig  windows_ipv4_by_adapter  windows_lan_pick
windows_lan_address  windows_home  windows_home_candidate
wslconfig_mirror_command  wslconfig_set_mirrored  cmd_mirrored
nat_hint  door_state  known_commands  suggest_commands  cmd_unknown
url_host  dns_public_json_verdict  dns_public_state
```

## 무엇을 확인했고 무엇을 못 했나

**확인한 것 (실측):**

- `wslconfig_mirror_command` 의 PowerShell 한 줄 — **실제 PowerShell 7.4.6** 으로
  다섯 경우를 돌렸다: 없던 파일 / `[wsl2]`+memory·processors / `[experimental]`
  만 / `networkingMode=NAT` / 이미 mirrored. `memory=8GB` 가 살아남고 고친 줄의
  CRLF 가 유지되는 것까지 봤다 (처음 쓴 `.*` 는 `\r` 을 먹어서 그 줄만 LF 가
  됐다 → `[^\r\n]*`).
- `bml mirrored` 가 사용자 데스크톱에서 실제로 돌았다 —
  `/mnt/c/Users/Administrator/.wslconfig` 를 찾아 "이미 mirrored" 로 판정.
- `windows_lan_address` 는 한국어/영어 `ipconfig` 출력 픽스처로.

**못 한 것 (여기가 의심스러운 자리다):**

- **mirrored 가 실제로 켜지는 것을 못 봤다.** 사용자 기계에서 `.wslconfig` 는
  고쳐졌지만 `wsl --shutdown` 이후 상태를 아직 확인 못 했다. Windows 11 22H2
  미만이면 조용히 무시된다는 것은 문서 근거뿐이고 실측이 아니다.
- **`dns_public_state` 의 DoH 경로를 한 번도 실행해 보지 못했다.** 개발
  컨테이너의 프록시가 1.1.1.1 을 막는다 (403). JSON 파싱만 픽스처로 고정했다.
  `nslookup`/`dig` 분기도 두 도구가 없어 돌려 보지 못했다.
- **`bml share` 로 연 터널에 밖에서 붙어 보지 못했다.** 랩 망이 `lhr.life` 를
  DNS 에서 거르고 외부 DNS(53)도 막아서, 데스크톱·노트북 어느 쪽에서도 확인이
  안 된다. "터널은 살아 있다" 는 ssh 가 주소를 받아 왔다는 것에서 온 추론이다.
- `win_exe` 의 System32 대체 경로 — `appendWindowsPath=false` 인 기계를 실제로
  못 만들어 봤다.

## 요청서를 쓴 뒤에 나온 것

- `a1b2` 이후 `win_exe` 가 한 번 더 틀렸다: `[ -x /mnt/c/.../ipconfig.exe ]` 는
  **interop 이 꺼져 있어도 참**이다 (drvfs 가 모든 파일에 실행 비트를 붙인다).
  빈 출력을 "쓸 주소가 없다" 로 읽어서 사람을 랜선 보러 보냈다. 출력이 비면
  실패로 보도록 고쳤다. **이 종류(“할 수 있다”와 “했다”를 안 가르는 판정)가
  이 묶음에 더 있는지 봐 달라.**

## 특히 봐 달라는 것

1. **저장소 바깥 파일 쓰기** (`cmd_mirrored`, `wslconfig_set_mirrored`).
   `cat "$tmp" > "$f"` 로 덮어쓴다 (drvfs 에서 rename 이 권한에 걸리는 것을
   피하려고). 중간에 죽으면 어떻게 되나? 백업(`.bml-bak`)은 고칠 때만 만들고
   안 고쳤으면 지운다 — 이 판단이 맞나? `[wsl2]` 절이 두 번 있는 파일은?
   `.wslconfig` 가 심볼릭 링크거나 읽기 전용이면?
2. **주소 판정** (`windows_lan_pick`). 어댑터 **이름**으로 거른다
   (`vEthernet|WSL|Loopback|VirtualBox|Hyper-V|Bluetooth|Teredo|isatap`).
   대역으로 거르던 것을 이름으로 바꾼 이유는 랩 망이 172.16–31 을 쓰기
   때문이다. 이름이 지역화되는 Windows 가 있나? 어댑터를 사람이 이름 바꾸면?
   여러 개일 때 첫 번째를 고르는데, 그 순서를 믿어도 되나?
3. **`cmd_unknown` 이 pull 을 돈다.** 모르는 명령을 만나면 `sync_repo` 를
   부르고, 새 bml 이 실려 있으면 그 명령 그대로 재실행한다. 오타 한 번에
   네트워크 왕복과 rebase 가 일어난다 — 받아들일 만한가? `BML_REEXECED` 말고
   무한 반복이 가능한 경로가 있나?
4. **`door_state`** — `/api/samples` 가 401 이면 잠긴 것으로 본다. 서버가 다른
   이유로 401 을 줄 수 있나? `bml status` 가 매번 이 요청을 한 번 더 보내는
   비용은?
5. **`dns_public_state`** — 이 기계의 resolver 를 일부러 건너뛰고 1.1.1.1 에
   묻는다. 호스트 이름이 제3자에게 나간다 (이미 공개 주소이긴 하다). 화면에
   그 사실을 적었는데 충분한가? `url_host` 의 글자 제한
   (`[A-Za-z0-9.-]` 아니면 거부)이 셸 주입을 실제로 막나?
6. **화면 규칙** — "들여쓴 초록 줄은 붙여넣는 명령, `│` 로 시작하는 줄은 파일
   내용". 이 규칙이 `tools/bml` 전체에서 지켜지나? 색이 꺼진 자리(파이프·로그)
   에서도 구분이 남나? 우리가 놓친 자리가 있나?
7. **테스트가 무엇을 잡고 무엇을 못 잡나.** 62건이 늘었는데 (89→151, 33→48)
   대부분 문자열 검사다. 실제 회귀를 잡을 수 있는 모양인가, 아니면 구현을
   복사한 것인가?

## 하지 말아 달라는 것

- 도메인 수치·`wrdkit`·API 는 건드리지 않았다. 범위 밖이다.
- "테스트를 더 쓰라" 는 그 자체로는 지적이 아니다. **어떤 회귀가 지금 안
  잡히는지**를 짚어 달라.
- 화면 문구의 취향은 범위 밖이다. **문구가 사람을 틀린 행동으로 보내는가**만
  본다.

## 붙여넣는 프롬프트

```
이 저장소(claude/battery-charge-discharge-webapp-dq4ja3 브랜치)의
a7efba10..284a4582 를 리뷰해 주세요. 커밋 9개, 대부분 tools/bml (셸)입니다.

이 변경은 계산을 바꾸지 않습니다. 바꾸는 것은 (1) 사람이 읽는 화면과 (2)
그 화면이 시키는 행동, (3) 주소·상태 판정입니다. 그래서 "코드가 도는가" 가
아니라 "화면대로 했을 때 사람이 옳은 곳에 도착하는가" 를 봐 주세요.

배경: 한 사람이 Windows 를 새로 깐 데스크톱을 중추 서버로 세우고 노트북에서
보게 하는 동안 여섯 번 막혔고, 이 커밋들은 그 여섯 자리를 하나씩 고친
것입니다. docs/log.md 의 2026-08-24 항목에 각 자리의 증상과 판단 근거가
남아 있습니다 — 커밋 메시지와 짝을 이룹니다.

먼저 CLAUDE.md 를 읽어 주세요. 특히 §0.3(계측기가 아는 것을 사람에게 다시
묻지 않는다), §0.4(모르면 None 을 반환하고 이유를 적는다), §0.5(CRLF),
§0.8(우리 것임을 증명한 뒤에만 죽인다). 이 변경들은 그 규칙을 근거로
정당화됩니다 — 규칙을 잘못 적용한 곳이 있으면 그것부터 짚어 주세요.

중점:
1. bml mirrored 가 저장소 바깥 파일(Windows 의 %USERPROFILE%\.wslconfig)을
   고칩니다. 이 저장소가 자기 트리 밖에 쓰는 것은 처음입니다. 안전한가요?
   (백업 정책, 덮어쓰기 방식, 중간에 죽는 경우, 심볼릭 링크·읽기 전용)
2. windows_lan_pick 이 ipconfig 의 어댑터 '이름' 으로 거릅니다. 이름이
   지역화되거나 사용자가 바꾼 Windows 에서 무너지지 않나요?
3. cmd_unknown 이 모르는 명령을 만나면 git pull 을 돌고 재실행합니다.
4. door_state / dns_public_state / block_layer_meaning — 판정이 틀렸을 때
   사람이 하게 되는 행동이 무엇인지까지 보고 판단해 주세요.
5. url_host 의 입력 제한이 셸 주입을 실제로 막는지.
6. 테스트 62건이 늘었는데(89→151, 33→48) 실제 회귀를 잡는 모양인지, 구현을
   문자열로 베낀 것인지.

확인 못 한 것을 미리 밝힙니다 (여기가 가장 의심스럽습니다):
- mirrored 가 실제로 켜지는 것을 못 봤습니다 (wsl --shutdown 이후 미확인).
- dns_public_state 의 DNS-over-HTTPS 경로를 한 번도 실행 못 했습니다
  (개발 컨테이너 프록시가 1.1.1.1 을 막습니다). JSON 파싱만 픽스처로 고정.
- bml share 로 연 터널에 망 밖에서 붙어 보지 못했습니다.
- win_exe 의 System32 대체 경로 (appendWindowsPath=false 기계 미확보).

지적은 심각도(높음/중간/낮음)와 파일·줄 번호, 그리고 **재현 절차 또는 깨지는
입력**을 함께 주세요. "테스트를 더 쓰라" 는 어떤 회귀가 지금 안 잡히는지까지
적어 주셔야 대응할 수 있습니다. 도메인 수치·wrdkit·API 는 이번 범위 밖입니다.
```
