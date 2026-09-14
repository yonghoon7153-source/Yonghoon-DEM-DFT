---
title: handoff merge 20260914
created: 2026-09-14
updated: 2026-09-14
type: guide
tags: [workflow, git, handoff]
sources: [docs/adr/0009-branch-is-the-home.md, docs/adr/0034-our-own-vps-in-front.md, docs/log.md]
confidence: high
explored: true
verificationStatus: verified
verifiedAt: 2026-09-14
---

# 인계 — 워크벤치 브랜치의 병합 가능성 (전수 조사용)

**작성** 2026-09-14 · **작성 세션** `claude/battery-charge-discharge-webapp-dq4ja3`
**대상 독자** origin 쪽에서 병합을 판단·수행·검증할 세션

---

## 0. 한 줄

**병합할 수 있는 브랜치는 딱 하나고, 그것은 fast-forward 다.** 나머지 원격
브랜치는 전부 **공통 조상이 없다** — 같은 저장소에 사는 다른 프로젝트들이고,
합치는 것은 병합이 아니라 접붙이기다. `main` 도 그중 하나다.

---

## 1. 브랜치 기하 (실측, 2026-09-14)

우리 HEAD = **`b42c0cf51`** (`claude/battery-charge-discharge-webapp-dq4ja3`)

| 상대 브랜치 | 원격 SHA | merge-base | 우리가 앞선 | 저쪽이 앞선 | 병합 형태 |
|---|---|---|---:|---:|---|
| `claude/battery-charge-discharge-webapp-vag24d` | `a7efba10b` | **`a7efba10b`** | **306** | **0** | ✅ **fast-forward** |
| `main` | `bf0dd1a32` | **없음** | 356 | 1 | ⛔ 계보 없음 |
| `claude/friendly-meitner-lldvar` | `634da438b` | **없음** | 356 | 3,558 | ⛔ 계보 없음 |
| `claude/bms-alpha-beta-verify` | `698d226de` | **없음** | 356 | 734 | ⛔ 계보 없음 |
| `claude/stoic-knuth-NObVQ` | `ed9050e0f` | **없음** | 356 | 2,861 | ⛔ 계보 없음 |

`merge-base` 가 **없음**이라는 것은 두 히스토리가 첫 커밋부터 별개라는 뜻이다.
`--allow-unrelated-histories` 로 억지로 붙일 수는 있지만 **그러면 안 된다**
(§3).

`origin/HEAD` 는 설정돼 있지 않다. **GitHub 기본 브랜치를 PR base 로 잡지 말 것.**

### vag24d 가 fast-forward 인 이유

`merge-base(dq4ja3, vag24d) == vag24d` 다. 즉 vag24d 의 모든 커밋이 이미
dq4ja3 안에 있다. vag24d 는 **2026-08-24 에 멈춘 옛 워크벤치 브랜치**고,
그 뒤 306 커밋이 전부 dq4ja3 에 쌓였다.

    git merge-base origin/claude/battery-charge-discharge-webapp-dq4ja3 \
                   origin/claude/battery-charge-discharge-webapp-vag24d
    # → a7efba10b...  (= vag24d 의 HEAD)

---

## 2. 이 저장소의 구조적 사실 — 먼저 읽을 것

**한 저장소에 프로젝트가 여럿이고, 각자의 집이 브랜치다** (`CLAUDE.md` §0.7,
ADR 0009). 브랜치를 바꾸면 상대 프로젝트의 파일이 **사라진다** — 같은 경로를
공유하지 않기 때문이다. 그래서:

- **`main` 에 머지하지 않는다.** `main` 이 비어 있는 것은 고칠 결함이 아니라
  결정이다 (ADR 0009). 비었다고 "정리" 하지 말 것.
- **한 작업 폴더에서 두 브랜치를 오가지 않는다.** 폴더는 `git worktree add`
  로 나눈다. 이 규칙을 어기면 상대 프로젝트의 실행기가 원인 대신
  `No such file` 만 뱉는다.
- 원격 브랜치 목록(2026-09-14 기준, 최근순)과 각자의 정체:

| 브랜치 | 최근 커밋 | 무엇 |
|---|---|---|
| `claude/bms-alpha-beta-verify` | 2026-09-14 | BMS 밸런싱 — **별개 프로젝트** |
| `claude/sdcp-dem-manuscript-si-pqwtv8` | 2026-09-14 | SDCP/DEM 원고 — **별개** |
| `claude/stoic-knuth-NObVQ` | 2026-09-14 | 위의 병합 대상 — **별개** |
| `claude/friendly-meitner-lldvar` | 2026-09-14 | DFT 판 (`webapp/app.py`, 포트 5001) — **별개** |
| **`claude/battery-charge-discharge-webapp-dq4ja3`** | **2026-09-13** | **이 워크벤치 (여기)** |
| `claude/battery-charge-discharge-webapp-vag24d` | 2026-08-24 | 이 워크벤치의 **옛 브랜치** — 유일한 병합 대상 |
| `claude/phase-a-96arm-kgy` 외 다수 | ~2026-09-12 | 전부 별개 프로젝트 |

---

## 3. 하면 안 되는 것 (명시)

1. **`--allow-unrelated-histories` 로 다른 브랜치와 합치지 않는다.**
   충돌이 안 나도 두 프로젝트의 파일이 한 트리에 섞여 양쪽 실행기가 깨진다.
2. **`main` 으로 PR 을 열지 않는다** (ADR 0009).
3. **이미 push 된 히스토리를 rewrite 하지 않는다** — `rebase -i`,
   `commit --amend`, `push --force`. 두 사람이 같은 브랜치를 쓴다.
4. **`docs/log.md` 는 append-only** 다. 충돌 시 **양쪽 항목을 모두 남긴다.**
5. **`data/`, `*.wrd`, `.venv/`, `node_modules/`, `*.db`, `.env` 는 커밋하지
   않는다.** `git add -A` 전에 `git status` 를 본다.

---

## 4. 무엇이 들어 있나 (`vag24d..dq4ja3`)

```
252 files changed, 63,234 insertions(+), 1,357 deletions(-)
커밋 306 · 2026-08-24 … 2026-09-13
```

접두사별: `fix` 143 · `feat` 62 · `update` 43 · `docs` 24 · `create` 17 ·
`verify` 9 · `ingest` 3 · `test` 2 · `lint` 2 · `refactor` 1

디렉터리별 (파일 수 / 추가 줄):

| 파일 | 추가 | 자리 |
|---:|---:|---|
| 115 | +23,811 | `apps/web` (React·TS·uPlot 화면) |
| 52 | +12,833 | `docs` (ADR 22장 + 위키 + 리뷰 기록) |
| 36 | +9,523 | `packages/wrdkit` (순수 과학 코어) |
| 34 | +8,984 | `apps/api` (FastAPI) |
| 12 | +8,065 | `tools` (`bml`, `vps-setup.sh`, 회귀 시험) |

### 작업줄기 여섯

1. **`.wrd` 파서 확장** — Smart Interface **2.13**(ADR 0016)과 **2.17**,
   CCCV 방전의 바닥 전압, 계측기의 "일반 데이터 보고서" 출력(`export.py`).
2. **EIS** — Biologic `.mpr` 읽기, 등가회로 피팅, DRT, 전송선 모델
   (ADR 0019·0021·0022·0028·0029).
3. **GITT** — 확산 꼬리, 사다리, 측정 조건의 소유권 (ADR 0026·0027).
4. **화면** — 셀 라이브러리, 그룹 폴더(ADR 0025·0035), dQ/dV·dV/dQ,
   한 셀의 세 구역(ADR 0024), 축 고정(ADR 0017).
5. **원격 접속** — 중계기(ADR 0030) → Cloudflare 터널(ADR 0031, 이 랩에서
   불가) → **우리 VPS**(ADR 0034·0036·0037). `tools/vps-setup.sh` 428줄.
6. **도구·신뢰성** — `bml` 의 포트 소유 판정, 터널 판정, 데이터 폴더,
   설치, 백업. `tools/tests/` 13개.

새 ADR 22장: 0016 … 0037 (`git diff --name-only --diff-filter=A
origin/claude/battery-charge-discharge-webapp-vag24d..HEAD -- docs/adr/`).

### 2026-09-13 하루 (VPS 를 실제로 세운 날) — 커밋 18개

`vps-setup.sh` 가 **처음으로 실제 기계에서 끝까지 돌았고**, 그 과정에서
설치본의 버그 다섯이 드러나 전부 고치고 시험을 붙였다:

| 커밋 | 무엇 |
|---|---|
| `f45945b63` | `pipefail` × `grep -q` — **맞는 값을 틀렸다고 읽었다** (7곳) |
| `60468b22c` | 배포판 nginx 의 기본 서버 위에 또 세워 nginx 가 통째로 거절 |
| `157ae749d` | 자기가 쓰다 만 파일에 자기가 걸려 매번 `BML_REPLACE` 요구 |
| `e32bde929` | 셸 없는 전용 계정을 "키가 없다" 로 읽었다 |
| `f34aa0475` | `status` 가 두 줄 아래에서 스스로를 반박했다 |
| `4674146fd` | 우리 것으로 못 알아본 https 에 LAN 점검표를 줬다 |
| `e4332dcea` `35927c586` `0edf5e063` `b61f776a8` | 관문 통과·망 구조 실측 기록 |
| `5ac832bbb` `b42c0cf51` | ADR 0036·0037 |

같은 날 파서 쪽: `13fecb844`(CCCV 바닥 전압 — 멀쩡한 21,235행 파일이 통째로
"잘림" 으로 판정되던 것), `da52e6dee`(보고서 TXT 출력).

---

## 5. 전수 확인 — 이 명령들을 돌려서 직접 재라

받는 쪽이 **우리 말을 믿지 말고 직접 재는** 순서다.

### 5.1 기하 (병합 전)

```bash
git fetch origin --prune
H=origin/claude/battery-charge-discharge-webapp-dq4ja3
B=origin/claude/battery-charge-discharge-webapp-vag24d

git merge-base $H $B                      # → a7efba10b (= $B 의 HEAD)
git rev-list --left-right --count $B...$H # → 0  306
git rev-list --count $B..$H               # → 306
```

`merge-base` 가 `$B` 의 HEAD 와 같으면 fast-forward 가 맞다. 다르면
**이 문서가 낡은 것이니 병합을 멈추고 다시 재라.**

### 5.2 다른 브랜치와 정말 계보가 없는지

```bash
for b in main claude/friendly-meitner-lldvar claude/bms-alpha-beta-verify \
         claude/stoic-knuth-NObVQ; do
  printf '%-45s %s\n' "$b" \
    "$(git merge-base $H origin/$b 2>&1 | head -1 || echo '없음')"
done
```

전부 빈 줄/오류면 계보가 없는 것이다. **하나라도 SHA 가 나오면** 그 브랜치는
이 프로젝트와 얽혀 있다는 뜻이니 그 자리에서 멈추고 사람에게 묻는다.

### 5.3 금지 파일이 섞이지 않았는지

```bash
git diff --name-only $B..$H | grep -E '^data/|\.wrd$|^\.venv/|node_modules/|\.db$|^\.env$'
```

**아무것도 안 나와야 한다.**

### 5.4 코드가 실제로 도는지 (체크아웃 뒤)

```bash
make setup-git          # pull.rebase · autostash · 커밋 훅
make check              # pytest + vitest + tsc + eslint + wiki-lint
```

2026-09-13 기준 실측: **vitest 708 통과 / 49 파일**, `tools/tests/` 셸·파이썬
회귀 13종 통과, `wiki-lint` 오류 0. `make check` 의 **종료 코드**를 봐야 한다 —
`make check | tail` 로 이어 붙이면 파이프라인 값이 `tail` 의 것이 되어
**빨간 검사를 초록으로 읽는다** (이 세션에서 실제로 한 번 당했다: `824ad29f7`).

알려진 잡음: `eslint` 경고 5건(`Plot.tsx`, EIS/GITT 화면의
`react-hooks/exhaustive-deps`) — 오류 아님, 이 브랜치 이전부터 있었다.
`wiki-lint` 경고 1건(`docs/log.md` 날짜 오름차순) — 2026-08-25/26 자리의
오래된 것.

### 5.5 도메인 규칙이 안 깨졌는지 (숫자를 내는 코드라면 필수)

`CLAUDE.md` §3 과 `.claude/skills/electrochem-invariants` 를 읽고, 실측
`.wrd` 가 있으면:

```bash
WRDKIT_SAMPLE=/path/to/real.wrd python3 -m pytest packages/wrdkit/tests -q
```

`trailing_bytes` 가 0 이어야 한다.

---

## 6. 미해결 — 병합해도 남는 것

받는 쪽이 "다 끝난 것" 으로 오해하면 안 되는 목록이다.

1. **Codex 리뷰 12건이 안 고쳐졌다.**
   `docs/reviews/2026-08-24-codex-screens-and-partials-result.md`
   (높음 3 · 중간 7 · 낮음 2, **승인 보류**). 그 문서 자체가 *"대응: 아직 안
   함"* 이라고 적고 있다. 그중 **높음 #2 (uPlot 확대 버튼이 실제 브라우저에서
   죽어 있다)** 는 이 세션에서 uPlot 소스로 **사실 확인까지 마쳤다** —
   시험이 통과한 이유는 우리 가짜가 스케일을 동기적으로 채웠기 때문이다.
2. **VPS 쪽 느슨한 끝 셋** (`docs/log.md` 2026-09-13 항목):
   - **8443 을 열어 뒀다** (NSG + iptables + nginx). 안 쓰게 됐으니 닫아야
     한다 — 9월 말까지 안 닫으면 그냥 닫는다.
   - `test.bmlwork.kr` 이 한양대 필터에 `newly-registered-domain` 으로
     막혀 있다. 주 1회 재서 풀리면 이름 둘을 하나로 합친다.
   - 공인 IP 가 `Ephemeral` 이다. 인스턴스를 지우면 `193-123-161-75.sslip.io`
     도 같이 죽는다 (이름 안에 IP 가 들어 있다).
3. **관문 10개 중 7번**(랩 PC 랜선 뽑았다 꽂기)을 안 쟀다. 9번(VPS 재부팅)이
   같은 재연결 경로를 밟았으므로 급하지는 않다.
4. **2.17 파일의 `planned_cycles` 가 300 으로 읽힌다** — 그 스케줄의
   `loop → 6STEP x300` 이 사이클 루프가 아니라 전류 차단 펄스 루프이기
   때문이다. 일부러 두었고 `docs/log.md` 에 근거를 적어 뒀다.

---

## 7. 권고

- **`vag24d` 를 dq4ja3 로 fast-forward 하거나, 그냥 지운다.** 옛 브랜치를
  살려 둘 이유가 없다면 지우는 쪽이 낫다 — 남아 있으면 다음 사람이 어느 쪽이
  집인지 헷갈린다. `CLAUDE.md` 는 집이 `dq4ja3` 라고 적고 있고 실측 기하도
  그와 일치한다.
- **다른 브랜치와는 아무것도 하지 않는다.** 계보가 없다.
- 병합을 하든 안 하든, **§6 의 네 항목은 그대로 남는다.** 그것을 누가 언제
  할지가 이 인계의 진짜 내용이다.
