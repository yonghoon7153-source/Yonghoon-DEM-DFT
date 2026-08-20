# Codex 교차검증 세션 — 부트스트랩

배터리 워크벤치 브랜치(`claude/battery-charge-discharge-webapp-dq4ja3`)를
원본으로 삼아, Codex 가 **자기 브랜치·자기 폴더**에서 독립 리뷰를 하게 만드는
절차다. DEM/MPM 채팅에서 쓰던 방식과 같은 틀이다.

## 0. 준비 (사람이 Windows 에서 한 번만)

공용 폴더 `C:\Users\안용훈\Yonghoon-DEM-DFT` 는 건드리지 않고, 워크벤치
브랜치에서 Codex 전용 브랜치와 worktree 를 딴다:

```powershell
git -C C:\Users\안용훈\Yonghoon-DEM-DFT fetch origin
git -C C:\Users\안용훈\Yonghoon-DEM-DFT worktree add `
  C:\Users\안용훈\Yonghoon-DEM-DFT-codex-bml `
  -b Codex/bml-crosscheck origin/claude/battery-charge-discharge-webapp-dq4ja3
```

worktree 라서 저장소를 다시 받지 않고, 폴더가 분리돼 있어 Claude 쪽
체크아웃(`~/bml`, WSL)과 파일 충돌이 없다. 이 저장소는 브랜치마다 다른
프로젝트를 담으므로(ADR 0009) **공용 폴더에서 checkout 으로 브랜치를 바꾸는
것은 금지**다 — worktree 만 쓴다.

## 1. Codex 채팅에 붙여넣는 프롬프트

아래를 그대로 붙여넣는다. (리뷰 과제 자체는
[codex-review-request.md](codex-review-request.md) 를 이어서 붙인다.)

```text
배터리 워크벤치 저장소 리뷰 채팅을 시작해.

이 채팅의 고정 작업환경:
- Codex worktree: C:\Users\안용훈\Yonghoon-DEM-DFT-codex-bml
- Codex branch: Codex/bml-crosscheck
- 원본(소스) branch: claude/battery-charge-discharge-webapp-dq4ja3
- Claude WSL checkout: /home/yonghoon/bml  (실행·수정은 그쪽 담당)
- 공용 폴더 C:\Users\안용훈\Yonghoon-DEM-DFT 에서는 checkout/switch/수정 금지

먼저 worktree 루트의 AGENTS.md 를 읽고, 아래를 읽기 전용으로 확인해:
- git status -sb
- git branch --show-current
- git rev-parse HEAD
- git worktree list
- origin/claude/battery-charge-discharge-webapp-dq4ja3 대비 ahead/behind

브랜치가 Codex/bml-crosscheck 가 아니면 아무것도 수정하지 말고 즉시 알려줘.

역할 분담:
- 구현은 Claude 쪽이 한다. 너는 독립 교차검증자다.
- 리뷰 산출물(md)만 이 브랜치에 커밋한다. 소스 코드는 고치지 말고,
  수정이 필요한 곳은 리뷰 문서에 제안으로 적어라.
- 검증 우선순위: 단위(tick/Ah/C), 부호, 사이클 경계, 기준 사이클(3),
  정규화 분모(활물질 wt%), 파서-스펙 일치, 문서-코드 일치.

가드레일:
- 기존 미추적·수정 파일을 이동·삭제·stash·reset 하지 않는다.
- data/, *.wrd, .venv/, node_modules/ 는 절대 커밋하지 않는다.
- push 는 내가 요청할 때만, PR 도 요청할 때만 만든다.
- 셸 스크립트는 LF 다. CRLF 로 저장하지 마라 (.gitattributes 가 강제한다).
- 내가 "클로드 작업하고 왔어" 라고 말하기 전에는 원본 브랜치를 당겨오지 마라.
  그 문구를 말하면 이렇게 동기화한다 (rewrite 금지, merge 만):
    git fetch origin
    git merge --no-ff origin/claude/battery-charge-discharge-webapp-dq4ja3

우선 저장소의 구조(wrdkit → api → web 의존 방향), 핵심 파일, 테스트 경로,
도메인 불변식(CLAUDE.md 3장)을 간단히 정리한 뒤 다음 지시를 기다려줘.
```

## 2. 실행 검증이 필요할 때 (선택)

기본은 읽기 전용 분석이다. 테스트까지 돌려보게 하려면:

```powershell
cd C:\Users\안용훈\Yonghoon-DEM-DFT-codex-bml
py -3 -m venv .venv-codex
.venv-codex\Scripts\python -m pip install -e packages/wrdkit[dev]
.venv-codex\Scripts\python -m pip install -r apps/api/requirements-dev.txt
$env:PYTHONPATH="packages\wrdkit\src;apps\api"
.venv-codex\Scripts\python -m pytest
```

`bml` 은 WSL 전용이므로 Windows 쪽에서 실행하지 않는다. 웹 검증이 필요하면
Claude 쪽(WSL, `~/bml`)에서 한다.

## 3. 끝났을 때

- Codex 의 리뷰 산출물: `docs/reviews/2026-08-20-codex-review.md`
  (Codex/bml-crosscheck 브랜치에 커밋)
- 우리 쪽 산출물: `docs/reviews/2026-08-20-internal-audit.md`
  (claude/battery-charge-discharge-webapp-dq4ja3 브랜치)
- 교차검증·종결 절차는 [codex-review-request.md](codex-review-request.md) 의
  마지막 절을 따른다.
