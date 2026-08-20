# AGENTS.md — Yonghoon Battery Lab Workbench

전고체/건식전극 셀의 충방전 데이터를 다루는 워크벤치. WonATech Smart Interface 가
쓰는 `.wrd` 바이너리를 직접 읽어서 CSV·프로파일·사이클 지표로 바꾸고, 실험을
그룹으로 묶어 비교한다.

에이전트(너)는 이 저장소의 **구현자이자 사서**다. 규칙 원본은 `docs/SCHEMA.md`,
설계 결정은 `docs/adr/`. 코드를 고치기 전에 해당 영역의 ADR 을 먼저 읽는다.

## 0. 이 저장소의 불변 규칙 (Non-negotiables)

1. **정규화된 값은 저장하지 않는다.** DB 에는 항상 raw mAh / V / s 만 넣는다.
   mAh/g · mAh/cm² 는 조회 시점에 계산한다. 건식전극은 질량·면적이 자주 바뀌고,
   질량을 고치면 **재파싱 없이** 모든 수치가 즉시 따라와야 한다.
2. **원본 파일은 불변.** `data/uploads/` 에 올라온 `.wrd` 는 절대 수정·삭제하지
   않는다. sha256 으로 중복을 판정한다.
3. **계측기가 아는 것을 사람에게 다시 묻지 않는다.** cutoff 전압, C-rate, 계획
   사이클 수, 샘플링 주기는 `.wrd` 안의 schedule 에 들어 있다. 파싱해서 채워 넣고,
   사용자 입력은 **덮어쓰기(override)** 로만 취급한다.
4. **모르면 `None` 을 반환하고 이유를 적는다.** 추정값을 실측값처럼 내보내지
   않는다. `KneeResult.reason`, `ResolvedCell.missing_for()`, `CellReport.evidence`
   가 그 패턴이다.
5. **파싱 계층에 도메인 가정을 심지 않는다.** `wrdkit/nrbf.py` 와 `wrdkit/wrd.py`
   는 파일이 선언한 대로만 읽는다. 컬럼 목록은 파일에서 읽고 하드코딩하지 않는다.

## 1. 구조

```
packages/wrdkit/        순수 과학 코어 (numpy 만 의존, 웹/DB 무관)
  nrbf.py               MS-NRBF (.NET BinaryFormatter) 리더
  wrd.py                .wrd → 컬럼별 numpy 배열
  schedule.py           스케줄(스텝/컷오프/루프) 디코딩
  cycles.py             스텝·사이클 분할, 프로파일 추출
  composition.py        전극 조성(AM:SE:도전재:바인더) 파싱과 활물질 wt%
  normalize.py          질량/면적/비용량 → mAh/g, mAh/cm², C-rate
  knee.py               용량 급감(knee) 검출 4종
  health.py             구동 중/종료 판정 + 대표 지표
  export.py             CSV/XLSX 출력
  downsample.py         LTTB (그래프용 축약)
apps/api/               FastAPI — 업로드, 저장, 조회, 내보내기
apps/web/               React + TypeScript + Vite — GUI
docs/                   llm-wiki (SCHEMA/index/log) + ADR + 포맷 스펙
.claude/skills/         반복 작업의 절차 6종 — 코드를 고치기 전에 해당 스킬을 읽는다
.claude/commands/       /sync /check /wrap /adr /verify /status
tools/                  wiki lint / status / new-page
data/                   업로드 원본과 파싱 캐시 (git 에 올리지 않는다)
```

의존 방향은 **한 방향**이다: `web → api → wrdkit`. `wrdkit` 은 FastAPI 도 DB 도
import 하지 않는다. 새 분석(EIS, DRT, dQ/dV)은 **먼저 `wrdkit` 에 순수 함수로**
넣고, 그 다음에 API 라우터를 붙인다.

## 2. Git — 2인 공용 저장소 규칙

이 저장소는 **두 사람이 같은 브랜치를 공유**한다. 아래를 지키면 충돌과 중복
커밋이 거의 생기지 않는다.

### 세션 시작 — 항상 이것부터

```bash
make sync          # git pull --rebase --autostash 와 동일
```

`--autostash` 가 작업 중이던 변경을 자동으로 넣었다 빼주므로 "커밋 안 했는데
pull 이 안 된다" 가 없다. `make sync` 없이 작업을 시작하지 않는다.

이 저장소는 `git config pull.rebase true` / `rebase.autoStash true` 를 전제로 한다.
클론 직후 한 번 `make setup-git` 을 실행하면 설정된다.

### 커밋

- **작게, 자주.** 한 커밋 = 한 가지 변경. 큰 커밋은 rebase 충돌을 크게 만든다.
- prefix 는 log action 과 동일: `feat:` `fix:` `docs:` `test:` `refactor:`
  `ingest:` `update:` `create:` `lint:` `verify:`
- 커밋 메시지에 **모델 이름·세션 링크를 넣지 않는다**.
- 남의 커밋 위에 이미 push 된 히스토리는 **절대 rewrite 하지 않는다**.
  `git rebase -i`, `git commit --amend`, `git push --force` 는 이미 push 한
  커밋에는 쓰지 않는다. (아직 push 안 한 로컬 커밋은 자유)

### push 가 거절되면

```bash
make sync && make check && git push
```

`rejected (non-fast-forward)` 는 상대가 먼저 push 했다는 뜻이다. **`--force` 로
덮지 말 것.** rebase 후 테스트를 다시 돌리고 push 한다.

### 충돌이 났을 때

- **코드 충돌**: 양쪽 의도를 확인하고 합친다. 한쪽을 통째로 버리지 않는다.
- **`docs/log.md` 충돌**: append-only 다. **양쪽 항목을 모두 남긴다.**
- **`docs/index.md` 충돌**: 양쪽 항목을 모두 남기고 `Total pages` 를 다시 센다.
- **lock 파일 충돌** (`uv.lock`, `package-lock.json`): 손으로 고치지 말고
  해당 도구로 재생성한다.
- 해결 후 `make check` 가 통과해야 `git rebase --continue`.

### 중복 작업 방지

- 작업 시작 전 `git log --oneline -15` 로 상대가 방금 뭘 했는지 본다.
- 큰 작업은 `docs/log.md` 에 먼저 한 줄 남기고 시작한다
  (`## [YYYY-MM-DD] start | <무엇을>`). 상대가 pull 하면 보인다.
- 같은 파일을 오래 잡아야 하면 브랜치를 따로 판다:
  `git switch -c claude/<주제>` → 끝나면 공용 브랜치로 merge.

### 절대 커밋하지 않는 것

`data/` (업로드 원본·파싱 캐시), `*.wrd`, `.venv/`, `node_modules/`,
`*.db`, `.env`. `.gitignore` 에 있지만 `git add -A` 전에 `git status` 를 본다.

## 3. 도메인 규칙 (틀리면 데이터가 조용히 망가진다)

- **시간은 .NET tick (100 ns)** 이다. 초로 쓰려면 `1e7` 로 나눈다.
  `wrd.seconds()` 를 쓰고 직접 나누지 않는다.
- **용량 단위**는 `UnitCoulomb` 플래그가 정한다 (False=Ah, True=C).
  항상 `wrd.charge_mah()` / `discharge_mah()` 를 거친다.
- **`CHARGE Q`/`DISCHARGE Q` 는 사이클마다 0 으로 리셋되는 누적값**이다.
  사이클 용량은 스텝 구간의 **차분**으로 구한다 (`segment_steps`).
- **`CELL STATUS`: 1=휴지, 3=충전, 4=방전.** 전류 부호와 일치함을 확인했다.
  스텝 분할은 `TOTAL STEP` (전역 스텝 카운터) 변화로 한다.
- **평균 전압은 에너지 가중** (`E/Q`) 이다. 단순 산술평균이 아니다.
- **활물질 wt% 는 조성에서 나온다.** mAh/g 의 분모는 전극 전체가 아니라 활물질
  질량이다. 이름을 못 알아본 성분은 **절대 활물질로 분류하지 않는다** — 분모에
  조용히 들어가기 때문이다. 0 wt% 성분은 지우지 말고 기록으로 남긴다.
- **기준 사이클은 3번**이다. 1~2번은 formation 이라 몇 % 는 설계상 잃는다.
  용량 유지율과 "초기 쿨롱효율" 은 기본적으로 3번 사이클 기준으로 계산한다.
  knee 탐색도 3번부터 시작한다 — formation 손실을 열화로 세면 안 된다.
- **구동 중인 셀의 마지막 사이클은 잘려 있다.** 절대 그 값을 보고하지 않는다.
  `CycleSummary.complete` 가 False 면 제외하고, 직전 완료 사이클을 쓴다.
- 긴 실험은 `..._011.wrd`, `..._012.wrd` 로 쪼개진다. 사이클 번호를 이어 붙이려면
  `cycle_offset` 을 쓴다.

## 4. 작업 흐름

```bash
make sync         # 세션 시작 — pull --rebase --autostash
make dev          # API(8000) + web(5173) 동시 실행
make test         # pytest + vitest + tsc
make check        # test + lint (커밋 전 필수)
make wiki-lint    # docs/ 위키 정합성
```

새 기능은 이 순서로 붙인다:

1. `docs/adr/` 에 결정을 한 장 적는다 (형식은 기존 ADR 참고).
2. `packages/wrdkit/` 에 순수 함수 + 테스트.
3. `apps/api/` 에 라우터 + 스키마.
4. `apps/web/` 에 화면.
5. `docs/log.md` 에 한 줄, 필요하면 `docs/` 위키 페이지.

**테스트 없이 `wrdkit` 을 고치지 않는다.** 합성 픽스처
(`packages/wrdkit/tests/synthetic.py`)가 실제 `.wrd` 를 바이트 단위로 만들어 주므로
20 MB 실측 파일 없이도 전 경로를 검증할 수 있다. 실측 파일이 있으면
`WRDKIT_SAMPLE=/path/to.wrd pytest` 로 추가 검증이 돈다.

## 5. 리뷰

이 저장소는 외부 리뷰(Codex 등)를 받는다. 리뷰가 쉽도록:

- 한 PR/커밋 묶음은 한 가지 주제만.
- 새 알고리즘에는 **왜 그 기준인지**를 docstring 에 적는다
  (`knee.py` 의 4종 기준 설명이 그 예다).
- 숫자를 바꾸는 변경은 실측 파일 기준 before/after 를 커밋 메시지에 남긴다.

## 6. Parity Contract

`AGENTS.md` 와 `CLAUDE.md` 는 같은 규칙의 미러다. 한쪽을 고치면 다른 쪽도 고친다.
`make wiki-lint` 가 parity 를 검사한다.
