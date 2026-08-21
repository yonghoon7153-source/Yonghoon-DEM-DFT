# 문서 인덱스

## 설계 결정 (ADR)

| # | 제목 | 요지 |
|---|---|---|
| [0001](adr/0001-store-raw-capacity-only.md) | 정규화된 용량은 저장하지 않는다 | raw mAh 만 저장, mAh/g 는 조회 시 계산 |
| [0002](adr/0002-own-wrd-parser.md) | `.wrd` 를 직접 파싱한다 | 자체 MS-NRBF 리더, numpy 만 의존 |
| [0003](adr/0003-timeseries-on-disk-summaries-in-db.md) | 시계열은 디스크, 요약만 DB | npz + SQLite |
| [0004](adr/0004-cycle-three-reference.md) | 기준 사이클은 3번 | formation 을 열화로 세지 않는다 |
| [0005](adr/0005-multi-criterion-knee.md) | Knee 는 기준 하나로 정하지 않는다 | 4종 계산 + 근거 제시 |
| [0006](adr/0006-frontend-stack.md) | React + TypeScript + uPlot | 대용량 곡선을 가볍게 |
| [0007](adr/0007-electrode-composition.md) | 조성은 성분 목록으로 기록한다 | 활물질 wt% 의 출처를 남긴다 |
| [0008](adr/0008-cell-state-weighted-evidence.md) | 구동중/종료는 가중 근거로 판정 | 근거를 함께 보여 준다 |
| [0009](adr/0009-branch-is-the-home.md) | 이 워크벤치의 집은 브랜치다 | `main` 은 별개, 머지하지 않는다 |
| [0010](adr/0010-user-saved-cell-presets.md) | 프리셋은 사람이 저장한다 | 조성 + 지름·비용량·기준전극, 질량은 담지 않는다 |
| [0011](adr/0011-central-instance-for-data.md) | 데이터는 중추 서버 한 대에 | git 으로 옮기지 않는다, 백업이 push 를 대신한다 |
| [0012](adr/0012-attribution-not-authentication.md) | 이름은 기록이지 신원 확인이 아니다 | 검증 없는 이름, 기록은 flush 리스너가 자동으로 |

## 리뷰 (외부 교차검증)

| 문서 | 용도 |
|---|---|
| [codex-session-bootstrap](reviews/codex-session-bootstrap.md) | Codex 전용 브랜치·worktree 부트스트랩 프롬프트 |
| [codex-review-request](reviews/codex-review-request.md) | Codex 에게 붙여넣는 전수 리뷰 과제 + 종결 절차 |
| [codex-review-round2](reviews/codex-review-round2.md) | Codex 2차 리뷰 과제 — 갱신 검증 + 2차 대상 20건 |
| [codex-review-round3](reviews/codex-review-round3.md) | Codex 3차 리뷰 과제 — 2차 갱신 검증 |
| [codex-knee-reply-2](reviews/codex-knee-reply-2.md) | 재검증 회답 — 7건 중 5건 닫음, joint event model 이 남았다 |
| [codex-knee-reply](reviews/codex-knee-reply.md) | Codex 에게 보내는 회답 — 15건 처리 결과와 다음 라운드 요청 |
| [2026-08-21-codex-knee-review](reviews/2026-08-21-codex-knee-review.md) | knee 리뷰 15건 대응 기록 — 14건 닫음, 문턱 보정 1건은 왜 남겼나 |
| [codex-review-knee](reviews/codex-review-knee.md) | knee 판정 집중 리뷰 과제 — 상수 과적합·세 직선 승격 편향 |
| [2026-08-20-internal-audit](reviews/2026-08-20-internal-audit.md) | Claude 쪽 전수 감사(확정 65건) + Codex 교차표 |
| [2026-08-20-codex-review](reviews/2026-08-20-codex-review.md) | Codex 독립 리뷰 원문 (확정 33건) |

파일명: `adr/0001-store-raw-capacity-only.md` · `adr/0002-own-wrd-parser.md` ·
`adr/0003-timeseries-on-disk-summaries-in-db.md` ·
`adr/0004-cycle-three-reference.md` · `adr/0005-multi-criterion-knee.md` ·
`adr/0006-frontend-stack.md` · `adr/0007-electrode-composition.md` ·
`adr/0008-cell-state-weighted-evidence.md` · `adr/0009-branch-is-the-home.md` ·
`adr/0010-user-saved-cell-presets.md` · `adr/0011-central-instance-for-data.md` ·
`adr/0012-attribution-not-authentication.md`

## 스펙

- [`raw/specs/wrd-binary-format.md`](raw/specs/wrd-binary-format.md) —
  `.wrd` 바이너리 포맷 전체 구조. 파서 구현의 근거.

## 가이드

- [[getting-started]] — **처음 쓰는 사람용.** 올리기 → 질량·조성 입력 → 화면 읽기
- [[bml-command]] — `bml` 한 줄로 최신화 + 실행. 협력자 설치 방법 포함
- [[wsl-setup]] — Windows/WSL 에서 쓰는 법. 막히는 지점과 해결까지
- [[central-server]] — 한 대를 중추 서버로. 공유·원본 되받기·백업
- [[extension-roadmap]] — 충방전 다음에 붙일 분석(dQ/dV, EIS, DRT)과 그 순서

## 에이전트 하네스

`.claude/skills/` 6종 — 이 저장소에서 반복되는 작업의 절차:

| 스킬 | 언제 |
|---|---|
| `electrochem-invariants` | 컬럼을 읽거나 용량을 계산하는 코드를 고치기 전 |
| `adding-an-analysis` | 새 분석(EIS, DRT, dQ/dV)을 붙일 때 |
| `extending-the-wrd-parser` | 파싱 실패나 처음 보는 enum 을 만났을 때 |
| `verifying-against-a-real-file` | 숫자를 만드는 작업을 끝냈다고 말하기 전 |
| `shared-branch-workflow` | 세션 시작, 커밋 전, push 거절 시 |
| `preparing-for-review` | 외부 리뷰를 요청하기 전 |

`.claude/commands/` — `/sync` `/check` `/wrap` `/adr` `/verify` `/status`

Total pages: 4
