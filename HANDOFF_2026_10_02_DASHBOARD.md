# 인수인계 카드 — 2026-10-02 대시보드 교체 (본진 동결 · 서브 덧붙이기만 · fast-forward 복귀)

작성: 본진 세션 (클라우드 컨테이너) · 2026-10-02. 사용자 결정: "다른 대시보드에서 작업" (토큰이 차는 동안 ASSB 논문
에이전트 등). 이 카드는 **새 세션이 처음 읽는 문서**다. 새 세션은 다른 컨테이너라 본진 세션의 스크래치패드를 볼 수
없다 — 필요한 것은 전부 이 파일과 저장소 안에 있다.

방식은 2026-09-28 `claude/gate80-standby-9a26dd5f` 대피와 같다 (`BRANCHES.md` 해당 절 — 그때 123 커밋을 충돌 0 으로
fast-forward 복귀했다). **소유 경로는 가르지 않고 시간만 가른다.**

---

## §0 규칙 다섯 (이것만 지키면 복귀는 fast-forward 한 번이다)

1. **본진 `claude/14-gate-code-review-9qkx05` 은 동결이다.** 서브 브랜치로 작업하는 동안 아무도 본진에 커밋하지 않는다.
   원래 본진 세션도 커밋하지 않는다 (그 세션은 이 카드를 쓴 커밋을 끝으로 멈췄다). 이 한 줄이 ff 복귀를 보장한다.
2. **서브는 본진 head 에서 시작한다.** 하네스가 만든 브랜치가 다른 곳 (예: `main`) 에서 갈라져 있으면 §2 절차로 본진 head
   위에 다시 세운다. 시작 SHA 는 붙여넣기 프롬프트가 알려 준다 (이 카드가 든 커밋).
3. **이력을 고쳐 쓰지 않는다.** rebase · squash · amend(push 뒤) · force-push 금지. 게이트 요청문이 커밋 SHA 를 인용한다
   (87차 요청 `672ab83b2` · 판정 대상 `b8d4b6933`) — SHA 가 바뀌면 리뷰어의 판정 대상이 사라진다.
4. **덧붙이기만 한다.** 원장 (`degradation-degeneracy/docs/08_REVIEW_RESPONSE.md`) 은 새 절, 상태 문서는 새 절 + 옛 문단은
   취소선, 요청문 · 리뷰 패키지 · 증거는 새 파일/디렉터리, `wiki/log.md` 는 끝에 항목 추가, `wiki/index.md` 는 줄 추가.
   기존 문단을 고쳐 쓰지 않는다 (정정은 취소선 + 새 문장).
5. **루트 `CLAUDE.md` 하드룰은 그대로다.** RUN_SCOPE (`degradation-degeneracy/` 의 `src/ tools/ configs/ scripts/ run.sh
   requirements*.txt`) 를 고치는 것은 게이트 루프 절차 (승인 기록 → 고정 표 → RED → GREEN → 변이 → 영수증 → 전체 회귀 ·
   smoke · 전체 재생 → 요청문) 로만 · 비밀정보 금지 · 수치의 정본은 artifact + `RESULTS*.md`.

## §1 지금 상태 (2026-10-02 · 본진 head = 이 카드가 든 커밋)

### 1-1. 게이트 루프 (`degradation-degeneracy`) — **87차 회신 대기**

| 항목 | 값 |
|---|---|
| 라운드 | 단계 3 **라운드 2b 제한 구현** 완료 (R2-a 실물 v6 leg gate · R2-c 이름 체계 · G84-N2) — 사용자 승인 원장 §126 ("1번 3번 진행하자") |
| 판정 대상 코드 | `b8d4b6933` — RUN_SCOPE 3 파일 (`tools/preserve.py` · `src/fitting.py` · `run.sh` · `src/io.py` 불변) |
| source_digest | `f1f4378f46610f08` → **`864edfb73b9695a1`** (이 카드 커밋에서도 그대로 — 카드는 RUN_SCOPE 밖) |
| 요청 HEAD | `672ab83b2` · 요청문 `degradation-degeneracy/docs/22p_gap/GATE87_REQUEST.md` · 원장 §127 · 증거 `docs/22p_gap/gate87_evidence/` (README 전체 sha256) |
| 고정 표 | `docs/22p_gap/STAGE3_IMPL_ROUND1_SPEC.md` §13 (§13-7 = pybamm 상한 **보류**) |
| 검증 (clean `7fbaa45b`) | 전체 pytest 2109 passed / 1 xfailed / rc 0 · strict smoke rc 0 · 등록부 전체 변이 재생 374/374 rc 0 · 요청문 커밋에서 docs-lint 등 438 passed |
| 발송 | 발송문은 아래 §5 (사용자가 Codex 에 붙여 보낸다 — 보냈는지는 사용자에게 확인) |
| 아님 | 실행 GO · 새 연구 leg · 운영 원장에 v6 계획 항목 · 세대표 등록 · p_ini · class 변경 · 투영 게시 · requirements 상한 |

87차 회신이 오면 (서브에서 처리해도 된다 — 본진 동결이므로 충돌 없음):
1. 수신 패키지를 **바이트 그대로** 보존 — `.gitattributes` 에 `docs/22p_gap/gate87_review/** -text !eol` 을 **먼저** 커밋한 뒤
   파일 추가 (85 · 86차와 같은 절차 · 줄끝 정규화 금지).
2. 원장 `08_REVIEW_RESPONSE.md` 새 절 §128 (접수) · `docs/GATE70_WORKING_STATE.md` 다음 단계 줄 (새 문장 + 옛 문장 취소선).
3. P1 발견이 있으면 사용자 승인 → `/finding` (RED 먼저) → 같은 게이트 절차. 승인 없이 RUN_SCOPE 를 건드리지 않는다.
4. 리뷰어가 원문 로그를 더 달라고 하면 `gate87_evidence/` 에 있는 것만 "커밋 파일" 로 부른다 (ZIP · 스크래치패드에만 있는
   것을 커밋 파일이라 부르지 않는다 — 85차 교훈). 로그는 `.gitignore *.log` 때문에 `git add -f`.

### 1-2. 사용자 결정 대기 (서브가 혼자 정하지 않는다)

| 항목 | 근거 |
|---|---|
| `requirements.txt` pybamm ~~상한 (`<26.9` 등)~~ 고정 (목적별 프로필) | `wiki/entities/pybamm.md` — ~~26.9 #5755 가 합성 truth 를 ≤2.7 mV 움직임 (실측)~~ 26.8 ↔ 26.9 환경 차이로 합성 truth ≤2.7 mV (실측 · #5755 단독 인과 미확정 — 2026-10-03 정정). RUN_SCOPE 변경 = 영수증 재생성 → 게이트 라운드 승인 범위. **Codex 사전 검토 회신 (2026-10-03):** C 검증 · B 정본 재생성 · D 생산 guard 분리 고정 권고 · G87-N1 종결 뒤 별도 라운드 (`degradation-degeneracy/docs/22p_gap/PYBAMM_PIN_PREREVIEW_REPLY_20261003.md`) |
| ASSB `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §3-b 미결 판단 거리 · 후속 논문 요청 후보 | 2026-09-30 복귀 기록 (`BRANCHES.md`) 이후 그대로 |
| COMSOL 0–480 s 분석 위치 | 사용자: "걱정 안 해도" — 이 작업 흐름 밖. `bms-balancing/docs/COMSOL_REBUILD_SPEC.md` §38–§39 가 마지막 |
| webapp `/bms` · `/microshort` 스냅샷 갱신 | 2026-09-30 복귀 기록 그대로 |

### 1-3. ASSB 논문 흐름 (서브의 주 작업 후보)

- 마지막 처리: **assb 89호** (Zhang Z. 2024 EES · 3차 묶음 파일 50 · `c8b6643d5` digest · `4e8fbdf34` 원장). 다음 번호 **90호**.
- 큐의 정본: `bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6 (§6-1 처리 상태 · §6-3-* 수령분 · §6-4 처리 순서 "먹인 순서
  그대로") · 요청 원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 (행마다 흡수 표시 · 지목 횟수 · ★) · §3-b (보류 판단).
- 에이전트: `.claude/agents/paper-curator.md` ("논문 에이전트") — digest `wiki/raw/papers/<slug>.md` (sha256 봉인) · 그림
  `wiki/raw/figures/<slug>/` (`wiki/tools/extract_figures.py`) · 카드 `wiki/questions/assb-contact-loss-vs-lampe.md` (채움표 ·
  Evidence) · 개념 `wiki/concepts/assb-lampe-contact-product-degeneracy.md` 등 · `index.md` · `log.md`.
- 한 편 = 커밋 둘이 관례: `ingest(wiki): assb NN호 — …` (digest · 위키) → `docs(bms): NN호 흡수 반영 — …` (원장 · 인수인계).
- 위키 규칙: `wiki/CLAUDE.md` · `wiki/SCHEMA.md` · 끝마다 `python3 wiki/tools/lint.py` 0 errors · raw 본문은 **Write 도구로**
  쓴다 (unquoted heredoc 금지 — 백틱이 실행된다, 두 번 실측).
- `wiki/tools/extract_figures.py` 를 고치면 (2026-09-30 두 번 있었다) `BRANCHES.md` 의 이번 절 "대피 중 누적" 표에 한 행.

### 1-4. 그 밖의 진행 중 흐름

- 매일 오는 GitHub 연구 브리핑: `wiki/guides/daily-github-briefing-triage.md` 절차 (네 축 · 1차 대조 · 브리핑만으로 RUN_SCOPE
  금지 · 시험 설치는 버리는 venv).
- `bms-balancing/` 의 COMSOL · MSC 흐름: 사용자가 요청할 때만.

## §2 서브 시작 절차 (새 세션이 처음 할 일)

```bash
cd <repo>
git fetch origin claude/14-gate-code-review-9qkx05
git rev-parse origin/claude/14-gate-code-review-9qkx05      # 붙여넣기 프롬프트의 시작 SHA 와 같아야 한다
B=$(git branch --show-current); echo "$B"
```

- **경우 A — 하네스 브랜치가 본진 이름 그대로**: `git pull --ff-only origin claude/14-gate-code-review-9qkx05` 뒤 바로 작업.
  이때는 서브가 곧 본진이다 — §3 의 복귀 절차가 필요 없다. `CLAUDE.md` 임시 줄만 "다른 대시보드 세션이 본진에서 직접 작업
  중 · 원래 세션은 커밋하지 않는다" 로 고친다.
- **경우 B — 다른 이름 (예: `claude/xxxx`)**:
  1. `git rev-list --count origin/claude/14-gate-code-review-9qkx05..HEAD` — 0 이면 고유 커밋이 없다 (하네스가 `main` 등에서
     만든 빈 브랜치). 그때만 `git checkout -B "$B" origin/claude/14-gate-code-review-9qkx05`.
     0 이 아니면 **멈추고 사용자에게 보인다** (그 커밋이 무엇인지 모른 채 덮지 않는다).
  2. 원격에 `$B` 가 이미 있고 커밋이 있으면 역시 멈춘다. 없으면 `git push -u origin "$B"`.
  3. 등록 커밋 하나: 루트 `CLAUDE.md` 하드룰 1 아래 임시 줄에 서브 이름을 적는다 (하드룰 1 "하네스가 우선이고 이 줄을 같이
     고친다") · `BRANCHES.md` 의 "2026-10-02 대피" 절 표의 서브 이름 칸 · 분기점 SHA 실측 일치. 메시지 `대피 등록 — …`.
- 환경: 새 컨테이너는 의존성이 다를 수 있다. 게이트 작업 (pytest · smoke) 을 할 때만 `degradation-degeneracy/` 에서
  `pip install -r requirements.txt` 후 `python -c "import pybamm; print(pybamm.__version__)"` 를 확인한다. **26.9 이상이면**
  수치 골든이 움직일 수 있다 (§1-2 · 최대 2.7 mV) — 시험이 깨지면 고치지 말고 버전과 함께 보고한다. ASSB 논문 작업만
  할 때는 설치가 필요 없다 (`pymupdf` 정도).

## §3 복귀 절차 (서브 → 본진 · 경우 B 에서만)

복귀 **전** 검사:

```bash
git fetch origin claude/14-gate-code-review-9qkx05 "$B"
git merge-base --is-ancestor origin/claude/14-gate-code-review-9qkx05 "origin/$B" && echo FF_OK
git status --porcelain | wc -l     # 0
```

- **FF_OK** → 체크아웃 없이 원격 fast-forward:
  `git push origin "origin/$B:refs/heads/claude/14-gate-code-review-9qkx05"` (거부되면 ff 가 아니다 — 아래로).
  이어서 정리 커밋 하나 (본진 이름 브랜치에서): `CLAUDE.md` 임시 줄 삭제 (blob 이 분기 전과 같아야 한다 — `git rev-parse
  <이 카드 커밋>^:CLAUDE.md` 와 비교) · `BRANCHES.md` 이번 절 끝에 결과 표 (복귀 SHA · "고유 커밋 0" 실측
  `git log "origin/$B" ^origin/claude/14-gate-code-review-9qkx05` 빈 출력 · 한 일 요약 · 본진에서 이어 갈 것).
- **FF_OK 가 안 나오면** 본진이 움직인 것이다 (규칙 1 위반 — 누가 왜 커밋했는지 먼저 확인). **rebase 하지 않는다** (규칙 3).
  서브에서 `git merge --no-ff origin/claude/14-gate-code-review-9qkx05` 로 본진을 들여온 뒤 ff 로 올린다. 충돌 규칙:

  | 파일 | 규칙 |
  |---|---|
  | RUN_SCOPE 6 경로 | **자동 해결 금지** — 충돌 목록을 사용자에게 보이고 판단을 받는다 (digest · 영수증 · 요청문 SHA 가 걸린다) |
  | `wiki/log.md` | append-only — 양쪽 항목 전부 보존 · 날짜순 |
  | `wiki/index.md` | 줄 합집합 (같은 페이지 두 줄이면 나중 것 + 옛 것 삭제 없이 사용자 확인) |
  | `08_REVIEW_RESPONSE.md` · 상태 문서 | 양쪽 절 전부 보존 · 절 번호가 겹치면 뒤에 들어온 쪽에 `§NNN-b` 를 붙이고 머리에 한 줄 |
  | `ASSB_WANTED_PAPERS.md` · `ASSB_TRANSFER_NOTE.md` · ASSB 카드 | 행 합집합 · 같은 행을 양쪽이 고쳤으면 사용자 확인 |
  | `CLAUDE.md` · `BRANCHES.md` | 서브 쪽 판 + 본진 쪽 추가 줄 |
  | 보존 묶음 (`*_review/` · `*_evidence/` · `reviews/`) | 바이트 그대로 — 양쪽이 같은 경로에 다른 바이트면 멈춘다 |

  merge 뒤 `python3 wiki/tools/lint.py` 0 errors · `degradation-degeneracy/` 에서 `python -m pytest tests/test_docs_lint.py -q`
  · RUN_SCOPE 가 merge 로 움직였으면 전체 회귀 · smoke 를 다시 돈다.
- 서브 브랜치는 지우지 않는다 · 복귀 뒤 새 커밋을 얹지 않는다 (`claude/bms-alpha-beta-verify` · `gate80-standby` 와 같은 처리).

## §4 대피 중 누적 기록 (서브가 덧붙인다)

복귀 커밋에서 "한 일 요약" 을 쓸 때 빠뜨리지 않도록, 아래 종류는 그때그때 `BRANCHES.md` 이번 절 "대피 중 누적" 표에
한 행씩 적는다: RUN_SCOPE 를 건드린 커밋 · `wiki/tools/*.py` 수정 · 보존 규칙 (`.gitattributes`) 추가 · 원장 절 번호 · 게이트
요청문 발송. 행마다 RUN_SCOPE 안/밖을 적는다.

## §5 87차 발송문 (사용자가 Codex 에 붙여 보낸다 · 이미 보냈으면 기록만)

```
87차 게이트 리뷰 요청 — 단계 3 라운드 2b 제한 구현 결과 (R2-a 실물 v6 leg gate · R2-c 이름 체계 · G84-N2)

첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

- 저장소: yonghoon7153-source/Yonghoon-DEM-DFT · 브랜치 claude/14-gate-code-review-9qkx05
- 요청 HEAD: 672ab83b2 (요청문 · 원장 §127 · 증거 — RUN_SCOPE 밖)
- 판정 대상 코드: b8d4b6933 — RUN_SCOPE 변경 커밋 하나 (tools/preserve.py · src/fitting.py · run.sh · src/io.py 불변)
- source_digest: f1f4378f46610f08 → 864edfb73b9695a1
- 고정 표: degradation-degeneracy/docs/22p_gap/STAGE3_IMPL_ROUND1_SPEC.md §13 (코드 변경 전 커밋 0b21490d · 사용자 승인 원장 §126)
- 요청문: degradation-degeneracy/docs/22p_gap/GATE87_REQUEST.md
- 원문 로그: degradation-degeneracy/docs/22p_gap/gate87_evidence/ (README 에 파일별 실행 상태 · 전체 sha256)

요지
- v5 승인 spec (leg_spec_version 2) 바이트 · digest 불변 (골든 b8f90ad9… · 운영 원장 grid_fit_v5 0838df84…) · v6 는 leg_run_spec_v3 + 닫힌 stage3 축 (planned-leg/v4 envelope 에서 유도)
- 계획 index: prospective 선택 키 planned_envelope · stage3_context (v3 ⇔ 둘 다 · envelope 결속 · 유도값 대조 · 경로 · provider 키 집합)
- 진입점 stage3_context_from_plan 한 곳 · CLI --stage3-plan · run.sh --stage3-plan (fit 전용) · _stage3_preflight / _prepare_stage3 우회 없음
- 소비자 분기: v3 계획 + 문맥 없음 거부 (legacy fallback 금지) · v2 계획 + 문맥 거부 · 미지 버전 거부
- 세대 이름 v6 하나 · validator digest 미등록

검증 (clean 7fbaa45b): 전체 pytest 2109 passed / 1 xfailed / rc 0 · strict smoke rc 0 · 등록부 전체 변이 재생 374/374 rc 0 (1 회차는 하네스 시간 상한으로 254 에서 중단 — 근거로 세지 않음). 변이 -g87 22: 1 회차 3 생존 (시험 s03_04 자기비일관 위조 — 시험 정정, 생산 코드 불변) → 22/22.

판정 요청: §13 닫힘 · v5 골든 불변 · 진입점 우회 없음 · 라운드 2b 종결 가부.
아님: 실행 GO · 새 연구 leg · 운영 원장 v6 계획 항목 · 세대표 등록 · p_ini · class 변경 · 투영 게시 · requirements 상한.
```

## §6 이번 세션에서 배운 운영 교훈 (서브도 같은 함정에 빠지지 않게)

- 하네스의 백그라운드 명령은 **2 시간 상한**이 있다. 등록부 전체 변이 재생 (~2 h 45 min) 은 `setsid nohup … &` 로 분리 실행하고
  `until grep -q '^replay rc=' log; do sleep 20; done` 대기를 다시 건다 (87차 1 회차가 254/374 에서 잘렸다 — 근거로 세지 않음).
- 변이 재생 · 전체 pytest 는 **하나씩** (병렬이면 디스크가 찬다). 디스크가 차면 큰 임시 파일부터 지운다.
- 변이가 살아남으면 먼저 **시험이 자기일관 위조를 만드는지** 본다 (87차 3 생존 · 85차와 같은 모양 — 앞 검사가 가려 뒤
  검사에 도달하지 못함).
- 증인 (EXPECT witness) 은 고정 이유만 — digest · 경로 · 임시 디렉터리 이름이 든 메시지는 안 된다 (G67-T1-b). 시험 단언에
  고정 메시지를 붙이면 된다.
- production 진입점 탐침은 pytest 안 (smoke namespace) 이나 `git archive` 사본에서만 (86차 G86-C1 — 운영 등록부 오염).
- 백그라운드 명령이 실행 중일 때 커밋하지 않는다 (HEAD 를 고정하는 시험이 있다 — 2026-09-14 교훈).
