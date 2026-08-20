# Yonghoon Battery Lab Workbench

전고체·건식전극 셀의 충방전 데이터를 **`.wrd` 원본 그대로** 다루는 워크벤치.

WonATech Smart Interface (Zive WBCS3000) 가 저장하는 `.wrd` 파일을 직접 읽어서
CSV 로 내보내고, 질량·면적·비용량을 입력하면 mAh/g · mAh/cm² 프로파일을 즉시
그려 준다. 실험을 날짜·양극재·공정·C-rate 로 묶어 비교할 수 있다.

Excel 로 옮기고 Origin 에서 다시 그리는 과정을 없애는 것이 목표다.

## 왜 만들었나

- Smart Interface 에서 데이터를 꺼내려면 매번 손으로 내보내야 한다.
- 건식전극은 질량이 자주 바뀌는데, 질량이 바뀌면 mAh/g · mAh/cm² 를 전부 다시
  계산해야 한다.
- 셀이 수십 개 쌓이면 "3번 셀 지금 몇 사이클이지, 용량 유지율 얼마지" 를 답하는
  데만 한참 걸린다.

이 워크벤치는 **원본 mAh 만 저장**하고 정규화는 조회할 때 계산한다. 질량을
고치면 재파싱 없이 모든 수치와 그래프가 즉시 따라온다.

## 할 수 있는 것

| | |
|---|---|
| `.wrd` 업로드 | 계측기 메타데이터·스케줄·전 사이클을 한 번에 파싱 |
| CSV / XLSX 내보내기 | raw · 사이클 요약 · 프로파일(Origin 붙여넣기용) |
| 충방전 프로파일 | 사이클 선택 → 전압 vs 용량, mAh / mAh·g⁻¹ / mAh·cm⁻² / % 축 전환 |
| 사이클 지표 | 방전용량, 쿨롱효율, 에너지효율, 평균전압, 이력(hysteresis) |
| 셀 상태 판정 | **구동 중 / 종료** 를 자동 판정하고 근거를 함께 제시 |
| 대표 지표 | 마지막 완료 사이클 용량, 3번 사이클 대비 유지율, 3번 사이클 초기 쿨롱효율 |
| Knee 검출 | 용량이 급감하기 시작하는 사이클을 4가지 기준으로 탐지 |
| 그룹·비교 | 날짜·양극재(high/mid Ni)·공정·C-rate 로 거르고, 직접 만든 실험 그룹으로 묶어 겹쳐 보기 |

## 빠른 시작

> **브랜치 주의 — 이 저장소에는 프로젝트가 둘 있습니다.**
> 브랜치마다 내용이 완전히 다릅니다.
>
> | 브랜치 | 내용 | 실행 | 포트 |
> | --- | --- | --- | --- |
> | `claude/battery-charge-discharge-webapp-dq4ja3` | 이 워크벤치 | `bml` | 5003 |
> | `claude/friendly-meitner-lldvar` | DFT 판 (`webapp/app.py`) | `dft` | 5001 |
>
> **이 워크벤치의 집은 위 브랜치입니다.** `main` 은 이 프로젝트가 아니고,
> 앞으로도 여기를 `main` 에 머지하지 않습니다 ([ADR 0009](docs/adr/0009-branch-is-the-home.md)).
> 그러니 `-b` 로 브랜치를 지정해 클론하는 것은 임시 우회가 아니라 정상 절차입니다.
>
> **한 폴더에서 두 브랜치를 오가지 마세요.** 브랜치를 바꾸면 상대 프로젝트의
> 파일이 사라집니다. 둘 다 쓴다면 아래 `git worktree` 방법을 쓰세요.

### Linux · macOS

```bash
git clone -b claude/battery-charge-discharge-webapp-dq4ja3 \
  https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT.git
cd Yonghoon-DEM-DFT
./tools/bml install     # bml 을 PATH 에 등록 (1회)
bml                     # 의존성·빌드·실행까지 알아서 → http://localhost:5003
```

`bml` 이 처음 실행될 때 가상환경을 만들고 의존성을 설치합니다 (1~3분).
`make setup` 을 따로 부를 필요가 없습니다.

### Windows (WSL)

WSL 안에서 합니다. 세 가지를 먼저 해야 합니다 — Ubuntu 가 `python3-venv` 를
기본으로 넣어 주지 않고, Node 저장소 버전이 낮고, git 이 CRLF 로 체크아웃하면
WSL 의 bash 가 스크립트를 실행하지 못합니다.

```bash
# 1. 패키지
sudo apt update && sudo apt install -y python3 python3-venv python3-pip git curl wslu
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash - && sudo apt install -y nodejs

# 2. 줄바꿈 (이걸 빠뜨리면 "bad interpreter" 가 납니다)
git config --global core.autocrlf input

# 3. 저장소는 WSL 안에 — /mnt/c 에 두면 10배 느리고 자동 새로고침이 안 됩니다
#    ★ -b 로 브랜치를 지정해야 합니다. 이 프로젝트의 집은 이 브랜치입니다.
cd ~
git clone -b claude/battery-charge-discharge-webapp-dq4ja3 \
  https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT.git
cd Yonghoon-DEM-DFT

# 4. 실행 (의존성·빌드까지 bml 이 알아서 합니다)
./tools/bml install
bml            # → http://localhost:5003 (Windows 기본 브라우저가 열립니다)
```

**이미 `~/Yonghoon-DEM-DFT` 폴더가 있어서 클론이 실패했다면** — 그 폴더에
무엇이 들어 있는지부터 보세요. 안에 DFT 판(`webapp/app.py`)이 있다면
**`git checkout` 을 하면 안 됩니다.** 그 파일들이 통째로 사라집니다.

```bash
ls ~/Yonghoon-DEM-DFT/webapp/app.py 2>/dev/null && echo "DFT 판입니다 — checkout 금지"
```

DFT 판이 들어 있다면, 저장소는 그대로 두고 **워크벤치만 옆 폴더에** 붙입니다.
`git worktree` 는 같은 저장소를 폴더 둘로 나눠 쓰는 기능이라 다시 받을 필요가
없고, 두 폴더가 각자 HEAD 를 가지므로 서로를 건드리지 않습니다:

```bash
git -C ~/Yonghoon-DEM-DFT worktree add ~/bml \
  claude/battery-charge-discharge-webapp-dq4ja3
cd ~/bml
./tools/bml install && bml
```

폴더가 비어 있거나 `main` 만 받은 경우라면 잃을 게 없으니 브랜치만 맞추면
됩니다:

```bash
cd ~/Yonghoon-DEM-DFT
git fetch origin
git checkout claude/battery-charge-discharge-webapp-dq4ja3
ls Makefile tools/bml     # 둘 다 보이면 정상입니다
./tools/bml install && bml
```

막히면 **`bml doctor`** 가 환경을 점검하고 무엇을 어떻게 고칠지 알려 줍니다.
전체 설명: [`docs/guides/wsl-setup.md`](docs/guides/wsl-setup.md)

PowerShell 에서 바로 치고 싶으면 `tools/bml.cmd` 를 Windows PATH 에 두면 됩니다.

### 명령

`bml` 한 줄이 `git pull --rebase --autostash` → 의존성 확인 → 빌드 → 실행을
순서대로 한다. 두 사람이 같은 브랜치를 쓰므로 pull 을 빠뜨리지 않는 것이
중요하다.

| | |
|---|---|
| `bml` | 최신화 + 실행 (http://localhost:5003) |
| `bml dev` | 같은 주소, 핫 리로드 |
| `bml stop` | 내리기 |
| `bml status` | 실행 상태 + 브랜치/미커밋/ahead·behind |
| `bml check` | 커밋 전 검사 |
| `bml doctor` | 환경 점검 (WSL 포함) |
| `bml repair` | 파이썬 환경 재설치 (의존성이 꼬였을 때) |

자세한 설명: [`docs/guides/bml-command.md`](docs/guides/bml-command.md)

`make` 를 직접 쓸 수도 있다 — `make serve` (한 포트), `make dev` (핫 리로드),
둘 다 http://localhost:5003 이다.

터미널만으로도 쓸 수 있다:

```bash
wrdkit info  cell.wrd
wrdkit convert cell.wrd --out-dir ./csv --basis mAh/g --mass 31.6 --wt 80 --diameter 13
wrdkit cycles cell.wrd --basis mAh/g --mass 31.6 --wt 80 > cycles.csv
```

## 구조

```
packages/wrdkit/   과학 코어 — .wrd 파서, 사이클 분석, 정규화, knee 검출
apps/api/          FastAPI — 업로드·저장·조회·내보내기
apps/web/          React + TypeScript — GUI
docs/              설계 결정(ADR), 포맷 스펙, 위키
```

`.wrd` 포맷을 리버스 엔지니어링한 기록은
[`docs/raw/specs/wrd-binary-format.md`](docs/raw/specs/wrd-binary-format.md) 에 있다.

## 공용 저장소 규칙

두 사람이 같은 브랜치를 공유한다. **세션 시작은 항상 `make sync`**,
**커밋 전에는 `make check`**. 자세한 규칙은 [`CLAUDE.md`](CLAUDE.md) 2장.

## 앞으로

충방전 GUI 를 기준으로 EIS 피팅 · DRT · dQ/dV(ICA) · 쿨롱효율 장기 추세를
같은 데이터 모델 위에 붙인다. 계획은 [`docs/adr/`](docs/adr/) 참조.

- 컷오프 전압·온도로 거르고 묶기 — 값은 파싱해서 들고 있지만(셀 상세에 표시)
  아직 필터·그룹 축이 아니다. API 쿼리 파라미터와 Library 필터를 함께 붙여야 한다.
- Library 화면에 C-rate 필터 — API 는 이미 받는데 화면에 컨트롤이 없다.
