# ADR 0001 — にほんちず 의 집은 브랜치 `nihonchizu` 다. `main` 에 머지하지 않는다

- 상태: 채택 (2026-09-27)
- 관련: bml 의 [ADR 0009](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/claude/battery-charge-discharge-webapp-dq4ja3/docs/adr/0009-branch-is-the-home.md), `tools/nihon` 의 `HOME_BRANCH`

## 맥락

이 저장소는 브랜치마다 전혀 다른 프로젝트를 담는다.

| 브랜치 | 내용 | 실행 | 포트 |
|---|---|---|---|
| `nihonchizu` | にほんちず — 일본 지도 노트 (이 프로젝트) | `nihon` | 5004 |
| `claude/battery-charge-discharge-webapp-dq4ja3` | 충방전 워크벤치 (bml) | `bml` | 5003 |
| `claude/friendly-meitner-lldvar` | DFT 판 | `dft` | 5001 |

`main` 은 비어 있고, 앞으로도 비어 있는 것이 정상이다. 처음 이 프로젝트를 만든
`claude/japan-map-webpage-l0bm3e` 는 세션이 자동으로 붙인 임시 이름이라 집으로 쓰지 않는다.

## 결정

**`nihonchizu` 브랜치가 이 프로젝트의 영구적인 집이다.** `main` 은 별개이며 머지하지 않는다.

1. 클론은 `git clone -b nihonchizu …` 가 정상 절차다. README 도 그렇게 쓴다.
2. 브랜치 이름은 `tools/nihon` 의 `HOME_BRANCH` 한 곳에만 적는다.
3. 다른 프로젝트와 한 기계에서 쓸 때는 `git worktree` 로 폴더를 나눈다. `git checkout` 으로 오가지 않는다.
4. CI 는 브랜치를 가리지 않는다 (`branches: ['**']`).
5. 포트는 5004 — bml(5003)·dft(5001) 과 겹치지 않는다.

## 결과

- "왜 main 에 안 올리나" 가 저장소 안에서 답해진다.
- 클론 명령이 길어진다. 대가지만, `nihon doctor` 가 잘못 받은 것을 잡아 준다.
