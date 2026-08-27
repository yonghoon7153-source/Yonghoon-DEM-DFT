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
| [0026](adr/0026-the-diffusion-tail-needs-a-start-a-ladder-and-a-choice.md) | 확산 꼬리는 시작점·시작 개수·회로 셋이 함께 정한다 | σ 를 실축 폭(Ω)으로 시작하던 차원 오류, 확산 회로의 재시작 8→24, `(전고체,풀셀)` 프리셋에 Ws 추가, `circuit=auto` |
| [0027](adr/0027-a-measurement-has-its-own-conditions.md) | 측정은 제 조건을 갖는다, 셀은 빈 칸만 채운다 | EIS·GITT 에 그룹·시험일·양극재·공정·온도, 물려받기는 빈 칸만 (`inherited` 로 표시), 셀 고르기는 드롭다운이 아니라 창 |
| [0028](adr/0028-solid-state-is-a-transmission-line.md) | 전고체 복합전극은 아크가 아니라 전송선이다 | Bisquert 전송선을 회로 원소로 (PyEIS `cir_RsTL` 대조), 전고체 프리셋 교체, 면적이 있으면 Ω·cm² |
| [0029](adr/0029-fit-the-way-zview-users-fit.md) | ZView 처럼 순차로 맞추되, 그 결과는 답이 아니라 시작점이다 | 회로의 직렬 블록을 고주파부터 하나씩 풀어 시작점 하나를 만들고 다중시작 주머니에 넣는다 (켜서 나빠질 수 없다), 오차가 대역 끝에 몰리면 그렇다고 적는다 |
| [0030](adr/0030-a-local-relay-instead-of-editing-hosts.md) | 이름이 막힌 기계에서는 hosts 를 고치지 말고 중계기를 띄운다 | `bmlonly` 가 `/etc/hosts` 대신 127.0.0.1:5013 에 중계기를 띄워 터널 엣지의 IP 로 넘긴다 (SNI·Host 는 터널 이름), sudo·관리자 PowerShell·재부팅 복구가 사라진다 |
| [0031](adr/0031-our-own-name-through-a-cloudflare-tunnel.md) | 고정 주소는 우리 도메인 + Cloudflare 터널로 얻는다 *(이 랩에서는 7844 가 막혀 못 씀 — 실측)* | 토큰과 이름이 둘 다 있을 때만 `cloudflared tunnel run --token` 으로 우리 이름을 열고, 실패해도 랜덤 주소로 흘러가지 않는다 — localhost.run 커스텀 도메인($9/월)과 결과가 같은데 무료다 |
| [0032](adr/0032-the-same-run-downloaded-twice-replaces-not-appends.md) | 같은 계측을 두 번 내려받은 파일은 이어 붙이지 않고 갈아 끼운다 | 구동 중인 셀을 114·200 사이클에서 각각 내려받으면 뒤엣것이 앞엣것을 담고 있다 — 이어 붙이면 314 사이클이 되고 유지율이 도로 올라간다. `acquisition_key` 가 같으면 긴 쪽만 남기고 짧은 쪽은 가린다 (지우지 않는다) |
| [0033](adr/0033-a-place-to-write-down-what-got-in-the-way.md) | 쓰다가 걸린 것을 겪은 자리에 적는다 | 상단 막대 오른쪽에 의견 칸 — 불편·질문·제안 셋으로 나누고, '정리됨' 은 지우는 것이 아니라 접는 것이며 다시 열 수 있다. 알림 점은 브라우저의 `localStorage` 로 판정한다 (로그인이 없으므로) |
| [0034](adr/0034-our-own-vps-in-front.md) | 고정 주소는 우리 VPS 한 대로 얻는다 | SSH 는 나간다 (22·443 실측) — 남의 터널을 사는 대신 `ssh -R` 로 우리 기계에 넘기고 거기 nginx + Let's Encrypt 가 `bml.bmlwork.kr` 을 받는다. DNS 는 회색 구름(프록시의 100 MB 업로드 상한을 피한다) |
| [0035](adr/0035-folders-instead-of-a-flat-list.md) | 목록은 폴더로 접고, 지난번과 달라진 수를 폴더 이름에 적는다 | 이미 있는 그룹 → 소그룹을 파일 탐색기처럼 접었다 편다. 폴더 이름 끝의 `+2 −1` 은 **내가** 지난번에 이 화면을 떠날 때의 셀 id 집합과 견준 것 — 개수가 아니라 집합이라 하나 들어오고 하나 나간 날도 보인다 (안혁주 제안) |

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
`adr/0025-groups-nest-one-level.md` ·
`adr/0026-the-diffusion-tail-needs-a-start-a-ladder-and-a-choice.md` ·
`adr/0027-a-measurement-has-its-own-conditions.md` ·
`adr/0028-solid-state-is-a-transmission-line.md` ·
`adr/0029-fit-the-way-zview-users-fit.md` ·
`adr/0030-a-local-relay-instead-of-editing-hosts.md` ·
`adr/0031-our-own-name-through-a-cloudflare-tunnel.md` ·
`adr/0032-the-same-run-downloaded-twice-replaces-not-appends.md` ·
`adr/0033-a-place-to-write-down-what-got-in-the-way.md` ·
`adr/0034-our-own-vps-in-front.md`

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
- [[vps-first-run]] — **고정 주소 만들기.** 버릴 수 있는 VPS 로 열 단계를 먼저 통과시키고, 그 다음에 실제 이름을 건다
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
