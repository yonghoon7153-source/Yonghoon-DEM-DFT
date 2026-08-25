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
| [0013](adr/0013-dqdv-on-a-voltage-grid.md) | dQ/dV 는 전압 격자 위에서 | 평탄부에서 ΔV→0, CV 구간은 빼고 격자로 옮겨 미분 |
| [0014](adr/0014-share-with-a-tunnel-and-one-password.md) | 바깥에서 볼 때만 문을 단다 | 임시 터널 + 공유 암호 하나, 랩 안에서는 아무것도 안 바뀐다 |
| [0015](adr/0015-dvdq-and-a-choice-of-smoother.md) | dV/dQ 는 용량 격자 위에서, 평활은 고를 수 있게 | 봉우리 간격이 곧 용량, SG 차수 1 은 이동평균과 같다 |
| [0016](adr/0016-smart-interface-213-is-a-second-file-shape.md) | Smart Interface 2.13 은 두 번째 파일 모양이다 | 압축된 헤더 봉투 + 고정 레이아웃, 버전으로 잠근다 |
| [0017](adr/0017-the-axis-lock-sets-the-default-view.md) | 축 고정은 기본 화면을 정한다 | 확대·이동 중에는 잠시 놓고, '전체' 가 그 화면으로 되돌린다 |
| [0018](adr/0018-formationless-schedules-anchor-at-cycle-one.md) | formation 이 없으면 1번 사이클에 앵커한다 | 루프 밖에 충방전이 없으면 formation 도 없다, ADR 0004 의 예외 |
| [0019](adr/0019-eis-is-its-own-section-with-two-fitting-worlds.md) | EIS 는 독자 섹션, 그 안에서 액체와 전고체를 가른다 | 같은 두 반원이 다른 것을 뜻한다, 저장은 Ω·Hz 만 |
| [0020](adr/0020-gitt-pairs-two-different-samples.md) | GITT 의 한 점은 서로 다른 두 샘플에서 온다 | 펄스 끝의 용량 + 휴지 끝의 전압, 가정을 검사한 뒤에만 D |
| [0021](adr/0021-double-bacon-watts-onset-and-point.md) | Double Bacon-Watts 로 knee-onset 과 knee-point 를 함께 구한다 | 검출되면 primary, 승격·유효성 게이트, sub-linear 한계 명시 |
| [0022](adr/0022-one-mpr-can-hold-many-spectra.md) | `.mpr` 한 파일이 스펙트럼 여럿을 담는다 (SOC 스캔) | 행 위치를 풀어서 정하고, 스윕마다 전위·용량을 들려 보낸다 |
| [0023](adr/0023-memoise-on-the-inputs-not-on-a-clock.md) | 캐시 키는 입력 그 자체다 (무효화하지 않는 캐시) | 컬럼과 knee 를 메모리에 남긴다, 상한은 바이트, `wrdkit` 은 캐시 없이 둔다 |
| [0024](adr/0024-three-sections-one-cell.md) | 세 섹션은 독립이고, 셀 하나가 그것들을 잇는다 | 섹션마다 대시보드·라이브러리·비교·업로드, 관계는 `sample_id` 하나, SOC 스캔은 올릴 때 정한다 |
| [0025](adr/0025-groups-nest-one-level.md) | 그룹은 한 단계만 겹친다, 그리고 셀은 한 자리에만 산다 | 그룹 → 소그룹 → 셀, `parent_id` 하나로 깊이 2, 상위로 거를 때는 `group_scope` 가 자손까지 편다 |

## 리뷰 (외부 교차검증)

| 문서 | 용도 |
|---|---|
| [2026-08-22-codex-review-remote-access-result](reviews/2026-08-22-codex-review-remote-access-result.md) | **원격 접근 리뷰 결과 (확정 21건)** — 대응 현황 표를 여기서 갱신한다 |
| [2026-08-24-codex-screens-and-partials-reply](reviews/2026-08-24-codex-screens-and-partials-reply.md) | **부분 사이클 리뷰 회답 (12건 전부 닫음)** — #6 은 결론을 바꿨고 ADR 0017 에 이유가 있다 |
| [codex-review-eis-gitt](reviews/codex-review-eis-gitt.md) | EIS·DRT·GITT 리뷰 과제 (보낸 것) — b6df17bb..7b0531d1, Claude 쪽 적대 리뷰와 교차 |
| [2026-08-24-codex-screens-reply](reviews/2026-08-24-codex-screens-reply.md) | **화면 리뷰 회답 (15건 전부 닫음)** — 대응 현황 표를 여기서 갱신한다 |
| [codex-review-screens-and-wsl](reviews/codex-review-screens-and-wsl.md) | 화면·WSL 리뷰 과제 (보낸 것) |
| [codex-review-remote-access](reviews/codex-review-remote-access.md) | 원격 접근 리뷰 과제 (보낸 것) |
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
`adr/0012-attribution-not-authentication.md` ·
`adr/0013-dqdv-on-a-voltage-grid.md` ·
`adr/0014-share-with-a-tunnel-and-one-password.md` ·
`adr/0015-dvdq-and-a-choice-of-smoother.md` ·
`adr/0016-smart-interface-213-is-a-second-file-shape.md` ·
`adr/0017-the-axis-lock-sets-the-default-view.md` ·
`adr/0018-formationless-schedules-anchor-at-cycle-one.md` ·
`adr/0019-eis-is-its-own-section-with-two-fitting-worlds.md` ·
`adr/0020-gitt-pairs-two-different-samples.md` ·
`adr/0021-double-bacon-watts-onset-and-point.md` ·
`adr/0022-one-mpr-can-hold-many-spectra.md` ·
`adr/0023-memoise-on-the-inputs-not-on-a-clock.md` ·
`adr/0024-three-sections-one-cell.md` ·
`adr/0025-groups-nest-one-level.md`

## 스펙

- [`raw/specs/wrd-binary-format.md`](raw/specs/wrd-binary-format.md) —
  `.wrd` 바이너리 포맷 전체 구조. 파서 구현의 근거.
- [`raw/specs/biologic-mpr-format.md`](raw/specs/biologic-mpr-format.md) —
  BioLogic `.mpr`/`.mpt`/`.mps` 구조. EIS 리더 구현의 근거.

## 가이드

- [[whats-new]] — **이번에 바뀐 것 쓰는 법.** 띄우는 법부터 SOC 스캔·knee 두 점까지
- [[new-laptop]] — **새 노트북 한 대 붙이기.** `wsl --install` 부터 `bmlin`/`bmlout` 까지
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

Total pages: 6
