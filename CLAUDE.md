# CLAUDE.md — Yonghoon-DEM-DFT 모노레포

이 저장소를 여는 모든 에이전트가 먼저 읽는 상시 규칙. 프로젝트별 상세는 각 하위
디렉터리와 `wiki/` 에 있다.

## 저장소 지도

| 경로 | 무엇 |
|---|---|
| `degradation-degeneracy/` | **주 연구 프로젝트** — PyBaMM 합성 truth 로 LLI/LAM fitting degeneracy 판별. 13라운드 적대적 게이트 리뷰 중 |
| `wiki/` | mothership LLM Wiki — 지식 지도 (`wiki/README.md`, 규칙은 `wiki/SCHEMA.md`) |
| `kit_*` `ps_zips` `se_curve` `run_mpm.sh` 등 | DEM/MPM 계열 — **다른 브랜치 소유**. 이 브랜치에서 건드리지 않는다 |
| `src/` `index.html` `vite.config.js` | 웹 뷰어 (별건) |

## 하드 룰

1. **브랜치**: push 는 `claude/zip-git-gpu-setup-vdqdtd` 로만. 다른 브랜치 금지.
2. **비밀정보**: 토큰·비밀번호·API 키를 대화나 파일에 넣지 않는다. 자격증명은
   실행 터미널에서만.
3. **RUN_SCOPE 경계**: degradation-degeneracy 의 code identity(`source_digest`)는
   `src/ tools/ configs/ scripts/ run.sh requirements*.txt` 만 본다. `wiki/`·
   `.claude/`·루트 문서는 그 밖 → 이 파일들을 고쳐도 게이트 리뷰 대상 코드
   identity 는 안 바뀐다. 반대로 저 6개를 고치면 **기존 산출물이 무효화**될 수
   있다 (재생성 비용 ~28분 + 10시간).
4. **정본**: 연구 수치의 정본은 artifact + `degradation-degeneracy/docs/RESULTS*.md`.
   위키·요약·대화에 적힌 숫자는 사본이며 인용 근거가 아니다.

## 작업 규율 (외부 하네스 3종에서 적응 — `wiki/concepts/agent-harness-patterns.md`)

### 1. 검증 없는 완료 선언 금지 (superpowers: verification-before-completion)

"통과했다/고쳤다/동작한다"는 **방금 실행한 출력**으로만 말한다. 기억·이전 실행·
"~일 것이다"는 근거가 아니다.

- 주장 → 그것을 증명하는 명령을 지금 실행 → 전체 출력과 exit code 확인 → 그 다음 주장
- 이 저장소의 증명 명령: `python -m pytest tests/ -q` (전체) ·
  `./scripts/smoke_e2e.sh` (strict e2e, clean 커밋에서) — 둘 다
  `degradation-degeneracy/` 안에서
- 금지 표현: "should", "probably", "아마", "될 겁니다" (검증 전에는 그냥 안 한 것)

### 2. 발견은 실패하는 테스트부터 (superpowers: TDD RED-first + 우리 고유 교훈)

리뷰 발견·버그를 고칠 때 **재현 테스트를 먼저** 쓰고 **실패를 눈으로 본 뒤** 고친다.
절차는 `/finding`.

- 새 테스트가 **처음부터 통과**하면 그건 성공이 아니라 **fixture 가 진실을
  가리고 있었다**는 신호다. 이 저장소에서 4회 이상 실측된 패턴 — validator 를
  강화할 때마다 fixture 가 먼저 깨져야 정상이고, 안 깨지면 fixture 가 위조
  통로였다는 뜻이다.
- 리뷰어가 준 반례(repro)는 그대로 회귀 테스트로 고정한다.

### 3. 최소주의 사다리 — 단, 검증 코드는 예외 (ponytail 적응)

새 코드를 쓰기 전 사다리: 없어도 되나 → 이 저장소에 이미 있나(재사용) → stdlib
→ 이미 깔린 의존성 → 한 줄 → 그제서야 최소 구현. **문제를 다 읽은 뒤에** 적용한다.

**이 저장소의 예외 (절대 줄이지 않는다)**: provenance 서명·validator 검사·
fail-closed 분기·회귀 테스트·인용 금지 배너. 13라운드가 붙인 것들이며 리뷰어가
계속 **더** 요구하는 축이다. 사다리는 이쪽이 아니라 **중복·재구현**에 쓴다
(같은 로직이 두 파일에 있는가, 기존 helper 로 되는가). 절차는 `/lean-review`.

### 4. 기계용 문서는 밀도, 사람용 보고는 명료 (caveman 적응 — 부분 채택)

- **기계용**(게이트 리뷰 요청문, 에이전트 핸드오프): 발견별 표·경로·검사 이름
  중심으로 압축. 수사·반복 금지. 절차는 `/gate-request`.
- **사람용**(사용자 보고, 문서, 커밋 메시지): 압축하지 않는다. 이 프로젝트의
  산출물은 판단 근거이고, 줄이면 근거가 사라진다. caveman 의 전역 압축 모드는
  **채택하지 않음** (사유는 wiki 개념 페이지).

## 컨텍스트 관리 (수동)

**자동 압축 설정은 두지 않는다.** `.claude/settings.json` 에 있던
`autoCompactEnabled`/`autoCompactWindow` 는 2026-08-11 제거했다 — 임계값을
낮추면 압축이 연달아 돌고, 올려도 세션 환경변수
(`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`) 가 이기기 때문에 프로젝트 설정으로는
제어가 안 됐다. `.claude/statusline.sh` 는 사용률 게이지만 표시하고 아무것도
권하지 않는다. 압축이 필요하면 사람이 `/compact` 을 치거나 새 세션을 연다.

대신 **컨텍스트를 덜 먹는 방식으로 일한다**:

- 큰 파일을 통째로 다시 읽지 않는다. `Read` 는 `offset`/`limit` 로, 위치
  확인은 `Grep` 으로. (`src/io.py` 1465줄, `tests/test_compare.py` 2451줄 —
  한 번 전체를 읽으면 그것만으로 창이 크게 찬다.)
- **진행 중 상태는 파일이 정본이다.** 좌표(파일:줄)·발견 목록·다음 단계는
  작업 문서에 떨군다. 예: `degradation-degeneracy/docs/GATE14_WORKING_STATE.md`
  — 14차 게이트를 재개할 때 `src/io.py` 를 다시 열 필요가 없게 만든 문서.
  진행 중 판단·미결 항목은 위키(`/wiki-wrap`) 나 `docs/`, 리뷰 요청문은
  스크래치패드에. 요약이 아니라 파일이 근거다.

## 커맨드

| 커맨드 | 용도 |
|---|---|
| `/finding` | 리뷰 발견 → RED 테스트 → 수정 → GREEN → fixture 감사 |
| `/lean-review` | 현재 diff 에 최소주의 사다리 적용 (검증 코드 carve-out) |
| `/self-review` | 다각 렌즈 적대적 자체 리뷰 (게이트 리뷰 요청 전) |
| `/gate-request` | 게이트 리뷰 요청문 생성 (기계용 밀도) |
| `/wiki-*` | LLM Wiki 운영 7종 (`wiki/README.md`) |

## 게이트 리뷰 루프

비싼 본 실행(~10시간) 전에는 항상: 수정 → 전체 테스트 + strict smoke → push →
대상 커밋 SHA 명시한 요청문 → **GO 나온 뒤에만** 실행. 절차와 이유는
`wiki/guides/gate-review-loop.md`, 발견 원장은
`degradation-degeneracy/docs/08_REVIEW_RESPONSE.md`.
