# Yonghoon Battery Lab Workbench

전고체·건식전극 셀의 충방전 데이터를 **`.wrd` 원본 그대로** 다루는 워크벤치.

WonATech Smart Interface (Zive WBCS3000) 가 저장하는 `.wrd` 파일을 직접 읽어서
CSV 로 내보내고, 질량·면적·비용량을 입력하면 mAh/g · mAh/cm² 프로파일을 즉시
그려 준다. 실험을 날짜·양극재·컷오프·C-rate 로 묶어 비교할 수 있다.

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
| 그룹·비교 | 날짜·양극재(high/mid Ni)·컷오프·C-rate·온도로 묶어 겹쳐 보기 |

## 빠른 시작

```bash
make setup     # 클론 직후 1회 (git 설정 + 의존성 + bml 등록)
bml            # 최신으로 맞추고 실행 → http://localhost:5003
```

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

설치와 자세한 설명: [`docs/guides/bml-command.md`](docs/guides/bml-command.md)
Windows/WSL: [`docs/guides/wsl-setup.md`](docs/guides/wsl-setup.md) —
`bml doctor` 가 환경을 점검하고 무엇을 고칠지 알려 준다.

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
