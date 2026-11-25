# CHANGELOG


## [0.1.12] — 2026-09-06 · 수신 (Claude Code 측)
### Added — `[RA-NEWS]` 주간 뉴스 아카이브 **수신 쪽**
`cowork/PROPOSAL_v018_news.md` 의 **A안**을 붙였다. 9/11 17:00 KST 부터 오는 메일을 받는다.
발신은 Cowork, 수신은 이쪽 — 두 판 연속 저쪽 다음-단계 표에서도 이 칸이었다.

- **`research_agent/news.py` 신규** — `build_news` / `render_week` / `import_news` /
  `sync_news_from_mail`. `vault/News/<금요일>.md` + `data/news.jsonl`(`source` URL 기준 중복 없음).
- **`ra news`** — 인자 없이 아카이브 현황, `--sync` 로 메일 걷기, `--import-file` 로 메일 없이
  payload 하나 주입(시험·복구), `--force` · `--lookback` · `--no-commit`.
  ⚠ `ra sync`(논문)와 **일부러 분리**했다 — 뉴스 IMAP 이 실패해도 논문 동기화가 멈추면 안 된다.
- **축소 덮어쓰기 거부** — 같은 주가 더 적은 항목으로 다시 오면 안 쓰고 이유를 찍는다.
  덮어쓸 때(`--force`, 또는 항목이 늘었을 때)는 `.backup/` 에 남긴다. `Vault.write_digest` 와 같은 처방.
- **선점 경보를 노트 맨 위 callout 으로** 올린다 (`scooping: true`). 판정은 보낸 쪽이 했고
  이쪽은 눈에 띄게 둘 뿐이다.
- 남은 두 질문에 답했다: **wikilink 안 건다**(`news.wikilinks: false`) · **`ra news` 로 따로 돈다**.
  본문에 원래 `[[` 가 있으면 내용이라 그대로 두되 `wikilinks_passed_through` 로 세어 돌려준다.

### Changed — IMAP 걷기를 한 벌로 (`handoff.fetch_tagged_json`)
`sync_from_mail` 안에 있던 IMAP 순회를 꺼내 handoff·news 가 **같은 함수**를 쓴다. 두 벌이면
한쪽만 고쳐지는 순간(dedupe·lookback·인코딩) 나머지가 조용히 뒤처진다. 메일에서 payload 를
꺼내는 부분은 `payloads_from_message` 로 **순수 함수** 분리 — 남의 바이트를 파싱하는 자리라
메일함 없이 시험할 수 있어야 한다. 동작은 그대로(`[RA-HANDOFF]` 경로 무변경).

### Tests — `tests/test_news.py` 20건 (대부분 음성)
첫 메일이 9/11 에나 오는 코드라 "되면 이렇게 된다"는 실물이 알려 준다. 지금 잠글 것은
**조용히 망가지는 쪽**이다: 논문 payload 거부 · 날짜 못 읽으면 `News/None.md` 안 만들기 ·
축소 덮어쓰기 거부 · `source` 없는 항목 안 버리기 · 우리가 wikilink 안 만들기 ·
헤드라인의 `:`·따옴표가 frontmatter 안 깨기 · 뉴스가 논문 DB 로 안 새기 · 두 태그가 실제로 다른지.

뮤테이션으로 확인했다 — 보호 5개를 하나씩 빼면 해당 시험이 **전부 죽는다**.

⚠ 픽스처 교훈: `message_from_string` 으로 만든 메일은 `get_payload(decode=True)` 가
한글 첨부를 깨뜨린다(raw-unicode-escape). 실물 경로는 `message_from_bytes` + base64 라
그런 일이 없다 — **픽스처가 실물보다 험하면 없는 버그를 쫓게 된다.** bytes 왕복으로 고쳤다.

92 passed (+20).


## [0.1.11] — 2026-09-06
### Fixed — ⛔ 검증기가 **올바른 전달에 경보**를 냈다 (false NO-GO)
v0.1.10 의 `--verify` 는 멀쩡한 전달에서 항상 최소 2건 MISSING 을 냈다.
`CHANGELOG_<ver>.md`(규약상 받는 쪽이 splice 하고 버린다)와 `MANIFEST_<ver>.md`(전달 문서
자신)를 repo 에서 찾았기 때문이다. **늑대가 왔다고 매번 외치는 검사는 두세 판 안에
아무도 안 보고, 그러면 진짜 유실이 묻힌다.** 도구를 만든 이유가 사라지는 종류의 버그다.

- **`kind: transient` 신설** — 전달 전용 파일. repo 기준 검증에서는 `skip` 으로 건너뛴다.
  `--transient` 로 지정하고, 매니페스트 자신은 자동 분류된다.
- **`--from <dir>` 신설** — 전달 묶음(평면 디렉터리)에서 basename 으로 대조한다.
  **repo 에 복사하기 전에** 확인할 수 있고, 이때는 `transient` 까지 전부 검사한다.
  v0.1.10 은 `ROOT` 를 스크립트 위치에서 유도해 **이미 복사한 뒤에만** 작동했다 —
  정작 필요한 자리(복사 전 확인)에서 못 쓰는 도구였다.

> ⚠ *"⛔ 가 뜨면 병합하지 말 것"* 이라는 지시는 **그대로 둔다.** 문제는 지시가 아니라
> 경보가 틀린 것이었다. 경보를 고치는 게 맞지 지시를 약하게 하면 안 된다 (그쪽 §2 인용).

### Added — 검증기 자신의 시험 `tests/test_manifest.py` (신규, 9건)
검증 도구에 시험이 없었다. 제일 중요한 시험은 "잡는다" 가 아니라
**"멀쩡한 전달에서 조용하다"**(`test_correct_delivery_is_silent_in_repo`) 이다 —
검사 도구는 거짓 경보 하나가 참 경보 열보다 비싸다.
`transient` 처리를 되돌리면 그 시험이 실패하는 것을 뮤테이션으로 확인했다.
나머지: 묶음 모드에서 안 떠난 파일 잡기(v0.1.8 시나리오) · MISMATCH · MISSING ·
표 줄 수 == 첨부 개수 · 옛 형식을 조용히 통과시키지 않기.

Cowork 트리 **57 passed** (48 → 57).


## [0.1.10] — 2026-09-06
### Changed — 매니페스트에 문서도 넣는다 (`kind: code|doc`)
v0.1.9 매니페스트는 코드 8개만 담았고 첨부는 10개였다. 그러면 *"첨부 10개 중 8개가
목록에 있다"* 를 받는 쪽이 **손으로** 조정해야 한다 — 개수 대조가 다시 사람 일이 되고,
이 스크립트를 만든 이유가 사라진다.
- `--doc` 뒤에 오는 파일은 `kind: doc` 으로 표에 들어간다. **매니페스트 자신도 자동 포함.**
- 자기 참조라 해시를 못 내는 매니페스트는 `—` 로 두고 **존재만** 확인한다(`ok(self)`).
- 표 머리에 *"표의 줄 수 == 실제 첨부 개수"* 를 명시. 다르면 그 자체가 유실 신호다.

### Changed — 규약 9' 는 이미 v0.1.9 에 들어가 있습니다
*"버그 수정의 일부인 새 인자엔 안전한 기본값을 두지 않는다"* 는 v0.1.9 에서 보낸
`cowork/DELIVERY_PROTOCOL.md` 의 **9'** 항목입니다(매니페스트 해시 `5035e7e8cd9d75ec` 로
일치 확인된 그 파일). 이번 판에서 그 절에 **위반 사례 두 건**(v0.1.6 즉사 / v0.1.8 무증상)을
표로 붙여 눈에 띄게 했습니다.

### 파일
매니페스트 표 참조 (`MANIFEST_0.1.10.md`).


## [0.1.9] — 2026-09-06
### Changed — 전달 규약 §7 폐기, 매니페스트를 **기계로** 뽑는다
§7("CHANGELOG 파일 목록과 첨부를 1:1 대조")은 **두 번 연속 안 걸렸다** — v0.1.6 `feedback.py`,
v0.1.8 `cli.py`. 두 번 다 회신문에 "대조했다"고 적혀 있었다. 목록도 사람이 쓰고 대조도
사람이 하면 같은 순간에 두 번 실수해서 안 걸린다.

- **`scripts/make_manifest.py` (신규)** — 실제 파일에서 경로·줄수·바이트·sha256[:16] 표를
  생성한다. 보내는 쪽에 파일이 없으면 표 아래 `⛔` 로 **전달 전에** 드러난다.
- **받는 쪽 검증** `--verify MANIFEST_<ver>.md` → `MISSING`/`MISMATCH`.
  하나라도 걸리면 병합하지 않는다.
- ★ 받는 쪽 검증이 결정적인 이유: **v0.1.8 의 `cli.py` 는 실제로 Cowork 의 전송 목록에
  있었다.** 유실은 Cowork 의 시야 밖 구간에서 났다. 보내는 쪽 점검을 아무리 강화해도
  그 구간은 못 덮는다 — 받는 쪽이 도착한 파일로 해시를 맞춰 봐야 잡힌다.

### Changed — 버그 수정의 일부인 인자에 기본값을 두지 않는다
`borderline_sample(..., has_answer_slot)` 을 **기본값 없는 키워드 전용**으로 바꿨다.
`=None` 이면 호출자(`cli.py`)가 유실됐을 때 조용히 옛 동작(쿨다운 무조건 적용)으로 돌아간다.
v0.1.6 은 `ModuleNotFoundError` 로 즉사해 바로 걸렸지만 v0.1.8 은 **안 죽어서** VERSION 만
0.1.8 이 된 채 안 고쳐질 뻔했다. **안 죽는 쪽이 더 나쁘다.**
회귀 1건(`test_has_answer_slot_has_no_default`) — 시그니처에 기본값이 생기면 실패한다.

### 파일 (7개)
```
research_agent/feedback.py     ← has_answer_slot 기본값 제거 (키워드 전용·필수)
tests/test_feedback.py         ← 호출부 갱신 + 시그니처 회귀 1건
scripts/make_manifest.py       ← 신규
cowork/DELIVERY_PROTOCOL.md    ← §7 폐기, 7'·8'·9' 신설
VERSION · pyproject.toml · research_agent/__init__.py
```
Cowork 트리 **48 passed**.


## [0.1.8] — 2026-09-05
### Fixed — ⚠ P1: 물어봤다는 기록이 답할 자리보다 먼저 확정되고 있었다
`cmd_morning` 의 순서가 이랬다:
```
_build_digest → fb.mark_asked(...)          ← 기록 확정
_send_digest  → 메일 (IMAP/SMTP)            ← 제일 잘 깨지는 단계
_vault_sync   → write_borderline_stub(...)  ← 자리 생성
```
발송이 예외로 죽으면 `cmd_morning` 이 예외를 올려 `_vault_sync` 가 안 돈다. 그러면 그 논문은
`borderline_asked_at` 만 찍힌 채 stub 이 없고, 30일 쿨다운에 걸려 다시 뽑히지도 않는다 —
**한 달 동안 묻지도 답하지도 못하는 논문**이 조용히 생긴다. 09-04 사고도 발송 계열이었으니
가정이 아니라 실제 경로다.

**ⓐ 채택 — 순서를 뒤집었다.** ①-b 에서 배운 것과 같은 형태다: *순서가 곧 안전장치다.*
- **`_prepare_borderline(v, border)`** — `_build_digest` 안에서 **렌더보다도 먼저** stub 을 만든다.
  자리 생성 → (렌더·발송) → `mark_asked` 로 DB 확정.
- 파일을 못 쓴 논문은 목록에서 **빼서 디제스트에도 안 싣는다.** "물어봤는데 답할 데가 없다" 를
  아예 만들지 않는다.
- `mark_asked` 가 `setdefault` 로 바뀌었다 — stub 파일에 찍힌 `asked_at` 과 DB 값이 어긋나면
  나중에 둘을 대조할 수 없다.
- dry-run 은 stub 도 안 만든다 (게이트 3 유지).

**두 번째 겹 (ⓒ 를 보조로)** — `borderline_sample(..., has_answer_slot=callable)`:
쿨다운의 전제는 "물어봤으니 답할 자리가 있다" 이다. 그 전제가 깨졌으면(asked 인데 노트 없음)
쿨다운을 적용하지 않는다. 순서 보장이 어디선가 또 뚫려도 논문이 영영 묻히지 않는다.
ⓒ 가 증상 차단이라는 지적은 맞아서 **원인 수정(ⓐ)을 주 방어로 두고 보조로만** 넣었다.

회귀 4건. **뮤테이션 2/2 잡힘** — 순서를 되돌리면
`test_answer_slot_exists_before_asking_is_committed` · `test_asked_at_is_consistent_between_stub_and_db`,
두 번째 겹을 무력화하면 `test_asked_without_a_slot_ignores_the_cooldown` 이 실패한다.

### 파일 (6개)
```
research_agent/cli.py          ← _prepare_borderline, has_answer_slot 전달
research_agent/feedback.py     ← borderline_sample(has_answer_slot=), mark_asked setdefault
tests/test_feedback.py         ← P1 회귀 4건
VERSION · pyproject.toml · research_agent/__init__.py
```
Cowork 트리 **47 passed** (43 → 47).

<!-- CHANGELOG.md 맨 위에 이 절만 붙여 주십시오. 파일 자체는 보내지 않습니다 (규약 개정). -->

## [0.1.7] — 2026-09-05
### Fixed — ⛔ P0 ①-b: harvest 실패가 사용자 체크를 지우고 있었다 (fail-closed 로 전환)
`_vault_sync` 가 `fb.harvest` 예외를 삼키고 노트 재생성을 계속했다. 주석에는 *"피드백은
부가 기능 — 실패해도 vault 동기화는 계속된다"* 라고 적어 뒀는데 **이 모듈에서는 그 판단이
거꾸로였다.** harvest 실패는 "아직 안 걷었다"는 뜻이고, 그 상태의 재생성이 바로 harvest
순서가 막으려던 파괴 경로다. sqlite 락 하나로 판정이 전손되고, 사용자는 지워진 걸 모르니
다시 체크하지도 않는다.

**게이트를 둘 걸었다.** 하나로는 다른 경로로 재발한다 — v0.1.3 에서 배운 것과 같다.
- **게이트 1 (실행 단계)** — harvest 가 예외로 죽으면 **노트를 한 장도 다시 쓰지 않는다.**
  MOC·홈은 DB 파생물이라 그대로 갱신한다. `_vault_sync` 가 `{harvest_ok, notes, stubs,
  harvested}` 를 돌려주고, `runs.status` 가 `"degraded"` 로 남아 조용히 지나가지 않는다.
- **게이트 2 (파일 단계)** — `Vault.unharvested_feedback()`: 노트에 DB 가 모르는 판정이
  적혀 있으면 `write_paper_note` 가 **덮어쓰기를 거부**한다. harvest 실패 경로는 예외뿐이
  아니다(ra_id 파싱 실패, 경로 누락…). `write_digest` 의 축소 덮어쓰기 거부와 같은 계열.

회귀 2건. **뮤테이션으로 각각 확인** — 게이트 1을 되돌리면
`test_harvest_failure_does_not_regenerate_notes`, 게이트 2를 무력화하면
`test_note_with_unharvested_check_is_never_overwritten` 이 실패한다.

### Fixed — ⛔ P0 ③: 경계선 표본이 물어보면서 답할 자리를 안 줬다
`borderline_sample()` 은 `rejected` 에서 뽑는데 그 논문들은 분석이 없어
`_vault_sync` 의 `if p.status == "rejected" and not p.analysis: continue` 에 걸려
**노트가 아예 안 만들어졌다.** 그런데 디제스트는 "노트 맨 아래 `## 피드백`에 남기면 됩니다"
라고 안내했다. 사용자는 Obsidian 을 열고 그 논문을 못 찾는다 → 오탈락 측정치가 구조적으로
영원히 0이고, 더 나쁘게는 **"물어봤는데 답이 없으니 다 무관한 게 맞구나"** 로 읽힌다.
v0.1.6 이 경고한 *"좁아진다는 사실 자체가 안 보인다"* 가 그대로 재현됐다.

**A안 채택** — `Vault.write_borderline_stub()`:
- `vault/Borderline/<노트명>.md` 에 **판정만 받는 최소 노트**. Papers 위계를 안 어지럽힌다.
- frontmatter 에 `ra_id`(harvest 매칭용)·`relevance`·`asked_at`·`feedback`,
  본문에 **왜 뺐는지**(`relevance_reason`)와 초록/스니펫, 그리고 `## 피드백`.
- `_vault_sync` 가 `extra.borderline_asked_at` 이 있는 논문에 stub 을 만든다.
- `feedback.harvest()` 가 **`Papers/` 와 `Borderline/` 를 둘 다** 훑는다. 여기서 빠지면
  측정이 영원히 0이라 기본 스캔 대상에 넣었다 (`vault.borderline_dir`, 기본 `Borderline`).
- 디제스트가 제목이 아니라 **`[[위키링크]]`** 로 노트를 가리킨다.

회귀 3건 — stub 생성 / stub 판정이 DB 까지 오는지 / 디제스트 링크.

### Changed — `CHANGELOG.md` 를 정본 목록에서 제외
v0.1.6 전달에서 Cowork 판이 Claude Code 의 병합 기록 두 절을 지웠다. 공동 이력이라
한쪽 정본이 될 수 없다. ⇒ **파일을 보내지 않고 새 절만 조각 파일로 보낸다.**

### 파일 (10개)
```
research_agent/cli.py          ← _vault_sync fail-closed + stub 생성 + runs degraded
research_agent/vault.py        ← unharvested_feedback / write_borderline_stub / borderline_dir
research_agent/feedback.py     ← harvest 가 Borderline/ 도 훑는다
research_agent/digest.py       ← 경계선 블록 위키링크
tests/test_feedback.py         ← P0 회귀 5건 추가
tests/test_dryrun_safety.py    ← _vault_sync 반환 모양(dict) 반영
VERSION · pyproject.toml · research_agent/__init__.py
cowork/DELIVERY_PROTOCOL.md    ← CHANGELOG 규약
```
Cowork 트리 **43 passed** (36 → 38 → 43).

## [0.1.6] — 2026-09-05
### Added — 피드백 루프 (`research_agent/feedback.py`, 신규 파일)
논문 노트 맨 아래 `## 피드백`에서 **유용함 / 무관 / 읽음 / 안 봄** 중 하나를 체크하면
선별 품질이 실측된다. `triage.py`(Claude Code 정본)는 건드리지 않았다 — 전부 신규 파일 + 훅.

- **`harvest()` 는 노트를 다시 쓰기 전에 돈다.** `Vault.write_paper_note` 는 매번 템플릿에서
  노트를 통째로 재생성하므로, 걷어 오기를 먼저 하지 않으면 사용자가 체크한 것이 조용히 지워진다.
  09-04 디제스트 사고와 **같은 계열의 손실**이라 `_vault_sync` 첫 줄에 고정하고 회귀로 묶었다
  (`test_feedback_survives_note_regeneration` — harvest 를 빼면 실패하는 것을 확인).
- 매칭은 파일명이 아니라 frontmatter `ra_id` 로 한다 — 제목·연도 보정으로 파일명이 바뀌어도 안 끊긴다.
- **표본이 모자라면 학습하지 않는다.** 축별 보정값은 `min_samples`(기본 8) 이상일 때만 생기고,
  총 보정폭은 ±0.10 으로 묶여 있으며, 적용 자체가 `feedback.apply_to_scoring` 로 **기본 꺼짐**이다.
  그때까지 이 모듈이 하는 일은 보고뿐이다. n=4 로 만든 가중치는 없느니만 못하다.
- 보고서 `vault/00_MOC/피드백 보정.md` — Tier별·IF구간별·키워드별·축별 정밀도, threshold 점검.
  **IF 구간 표가 "IF 우선 정렬"이 옳았는지 실측한다** — 아니라는 답이 나올 수 있게 만들어 뒀다.
- `ra feedback [--show] [--dry-run] [--min-samples N]` 신설. `ra noon`/`ra morning` 은
  `_vault_sync` 를 통해 자동으로 수집한다.

### Added — 경계선 표본 (오탈락 측정)
vault 에는 threshold 를 통과한 논문만 있으므로 정밀도는 보이지만 **오탈락은 영영 안 보인다.**
5년짜리 시스템에서 이건 읽는 범위를 조용히 좁힌다. 그래서 디제스트에
`## 경계선 확인` 을 붙여 threshold 바로 아래(기본 0.25–0.35) 논문을 **2편만** 물어본다.
- 이미 판정한 논문·최근 30일 안에 물어본 논문은 다시 뽑지 않는다 (`borderline_asked_at`).
- **0편인 날에는 붙이지 않는다** — 빈 디제스트를 경계선 표본으로 채우는 것은 잡음이다.

### Fixed — 게이트 3: dry-run 이 디제스트 파일도 만들지 않는다
`_build_digest` 가 dry-run 여부와 무관하게 `write_digest` 를 부르고 있었다. 게이트 2(축소
덮어쓰기 거부)가 피해는 막지만 "dry-run 은 아무것도 쓰지 않는다"는 약속은 지켜지지 않았다.
이제 dry-run 은 경로만 계산해 돌려주고, `ra digest --dry-run` 미리보기도 **파일이 아니라
방금 만든 본문**을 쓴다 (게이트 2가 쓰기를 거부하면 미리보기가 옛 파일을 보여주던 문제도 같이 해소).

### Added — Battery Weekly (클라우드 전용, repo 무관)
논문 디제스트와 **완전히 분리된** 주간 산업·정책 메일. 금요일 17:00 KST.
뉴스가 없거나 무관한 주에는 **보내지 않는다.** repo 코드가 아니라 Cowork 예약 작업이므로
Claude Code 쪽에서 할 일은 없다.

### Fixed — Claude Code 리뷰 반영 (2026-09-05, 병합 전 수정)
- `digest._feedback_footer` — `if not fb` 검사를 `n = int(fb.get(...))` **앞으로** 옮겼다.
  동작은 같았지만 읽는 순서가 뒤집혀 있었다.
- `digest.select_for_digest` — 두 번째 루프가 창과 무관하게 `analyzed` 를 전부 담고 있었다.
  발송이 되는 동안은 `digested` 로 바뀌어 자기제한이지만, **메일이 며칠 실패하면 무한정 쌓이고**
  복구된 첫 디제스트가 읽을 수 없게 커진다. `digest.max_backlog`(기본 30) 상한을 두고
  **우선순위 높은 쪽부터** 남긴다. 잘린 논문은 `analyzed` 로 남아 다음 회차 후보가 된다.
  회귀 2건 추가 → 전체 **38 passed**.

### Changed — 전달 규약 개정 (`cowork/DELIVERY_PROTOCOL.md`)
v0.1.6 전달에서 9개 중 5개만 도착했고 빠진 쪽에 신규 모듈이 있었다.
tarball 의 위험은 덮어쓰기, 개별 전달의 위험은 **빠뜨림**이다. 세 항목을 추가했다 —
① 나눠 보내지 않고 한 번에 ② 신규 모듈을 맨 앞에 ③ CHANGELOG 파일 목록과 첨부를 1:1 대조.

### 파일
```
research_agent/feedback.py     ← 신규
research_agent/cli.py          ← _vault_sync harvest 훅, _build_digest dry_run, cmd_feedback
research_agent/vault.py        ← feedback_block 매핑, 홈 MOC 링크
research_agent/digest.py       ← 경계선 블록, 피드백 푸터
templates/paper_note.md        ← ## 피드백 섹션, frontmatter feedback:
tests/test_feedback.py         ← 신규 18건
VERSION · pyproject.toml · research_agent/__init__.py · CHANGELOG.md
```
전체 `python -m pytest -q` → **36 passed** (Cowork 트리 기준).

## [0.1.5] — 2026-09-04
### Changed — 전달 규약 (Claude Code §1 제안 수용)
- **tarball 전달을 폐기한다.** Cowork 트리는 v0.1.0 에서 갈라진 fork 라, 통째로 보내면 Claude Code 가
  매번 델타를 손으로 골라내야 하고 목록이 길어지면 하나를 놓친다(v0.1.3·v0.1.4 에서 반복).
  이제 **바뀐 파일만 개별 전달**한다. 정본 경계는 `cowork/DELIVERY_PROTOCOL.md` 에 명문화.
- 선점 경보 대상에 **SDCP/전도성 고분자 폴라론 국재·spin share DFT** 추가 (Claude Code §4).
  C-12 는 v36(19잡)·보고량이 E_ads 절대값+차로 확장돼 "바인더 흡착 DFT" 긴급도 상향.
- alert 0통은 **알려진 상태**로 두고 다음 주 초 `is_empty` 연속 일수로 재판정 (양쪽 합의).
  0건으로 끝난 실행은 이미 `runs.status = "ok"` 로 기록되므로 실패로 남지 않는다 — 확인 완료.

## [0.1.4] — 2026-09-04 · 병합 (Claude Code 측)
Cowork v0.1.4 의 **신규분만** 가져왔다 (0.1.3→0.1.4 델타는 작다):
`digest.py`(창 계측) · `cli.py` 한 줄(`digest_stats(db, papers, cfg)`) · VERSION·pyproject·__init__.
⛔ 그쪽 tarball 은 또 자기 baseline 에서 갈라져 나와 브랜치 정본이 빠져 있다 —
`config/agent.yaml`(mode: file) · `research_profile.md`(249줄) · `exporters/litdb.py`(markdown 어댑터 없음) ·
`tests/test_litdb_markdown.py` 없음. **덮지 않았다.** 테스트 24 passed 유지.

## [0.1.4] — 2026-09-04
### Added — 디제스트 창 튜닝 계측 (Claude Code §3 합의)
- `mail.digest_window_hours: 36` 은 **근거 없이 정한 값**이다. 추측으로 바꾸는 대신, 판단에 필요한
  네 지표를 매 morning 실행이 `runs.summary` 에 기록하도록 계측을 넣었다:
  `weekday` · `is_empty`(n_papers==0) · `oldest_selected_age_h`(선택된 논문 중 가장 오래된 것) ·
  `n_redigested`(이미 digested 였는데 다시 뽑힌 편수) · `window_h`.
  판정 기준도 미리 정해 뒀다 — 0편 비율 30 % 초과면 창이 짧다 / 0편이 월요일에 몰리면 주말 공백이
  원인이라 72 h / `n_redigested` 가 0이 아니면 "마지막 발송 이후 전부"로 바꾸는 것은 위험하다.
  **데이터를 보고 기준을 만들지 않는다 — 기준을 먼저 정하고 데이터가 채워지면 판단한다.**
- `digest_stats` 에 `n_alerts`(선점 경보 건수) 추가 — 디제스트 제목·frontmatter 에 노출.

### ⚠ 운영 발견 — Scholar alert 가 이 메일함에 **한 통도 오지 않고 있다**
- 2026-09-04 12:00 NOON 첫 실전 실행: alert 0건 → `[SILENT]` 로 정상 종료.
- Gmail `in:anywhere` (스팸·휴지통 포함) 전수 검색 결과 `scholaralerts-noreply@google.com` 발신 메일이
  **역대 0통**. 파이프라인은 옳게 동작했으나 **입력이 비어 있다.**
- 원인 후보: (a) alert 가 다른 Google 계정(개인 gmail)으로 발송 (b) 수신 주소 오기 (c) 등록 직후라
  아직 신규 논문이 없음. → 사용자 확인 필요. 이 문제가 풀리기 전까지 파이프라인은 매일 조용히 돈다.

## [0.1.3] — 2026-09-04 · 병합 (Claude Code 측)
Cowork v0.1.3 tarball 을 브랜치 상태와 병합했다. 회신문 §5 의 정본 지정을 그대로 따랐다.
- Cowork 정본으로 교체: `cli.py`(dry-run 게이트) · `vault.py`(write_digest 방어 + `_scooping_block`) ·
  `digest.py`(경보 렌더) · `tests/test_dryrun_safety.py` · `VERSION`/`pyproject.toml`/`__init__.py` ·
  `prompts/deep_analysis.md` · `templates/paper_note.md` · `hermes/.../deep_analysis_schema.md` · `cowork/README.md`
- **덮지 않음**(브랜치가 정본): `exporters/litdb.py`(markdown 어댑터) · `config/research_profile.md`(482줄) ·
  `config/agent.yaml`(`litdb.mode: markdown`) · `tests/test_litdb_markdown.py` · `tests/test_triage_db.py` ·
  `data/` · `vault/`(복원한 2026-09-04 디제스트 164줄)
- `triage.py` **머지** — 이쪽 캠페인 용어를 기준으로, Cowork 표에서 빠진 것을 보탰다:
  · 축 A `MPM`·`Taichi`·`voxel`·`Kirchhoff`·`Bruggeman`·`constriction`·`Holm` (MPM 은 그 브랜치 90일 최다 주제인데 없었다)
  · **축 C 한 줄 신설** — `EIS`·`symmetric cell`·`Li-In`·`ASR`·`areal capacity` (이쪽 표에 통째로 없었다)
  · 축 A 물성 — 배위수·force chain·fabric tensor·Von Mises·유효전도도 / 감점에 `CALPHAD`·`potassium-ion`·`BMS`
  실측: 축A 0.950 · 축B 0.625 · 축C 0.800 · 무관 0.000
- 테스트 **24 passed** (이쪽 18 + Cowork 6) — 회신문 §5 의 예측치와 일치


## [0.1.3] — 2026-09-04
### Fixed — P1 데이터 손실 (Claude Code 보고, 실측 피해 발생)
- **`ra morning --dry-run` 이 dry-run 이 아니었다.** `args.dry_run` 이 메일 발송만 막고
  `_vault_sync`·`_git_commit` 은 게이트 밖에 있었다. 디제스트 창(36 h)이 지나 재생성이 0편을 내자
  그 빈 결과가 기존 파일을 덮었고, 2026-09-04 디제스트가 164줄 → 22줄로 소실됐다(Claude Code 가 tarball 에서 복원).
  → dry-run 이면 **메일·vault·git 전부** 건너뛴다.
- `cmd_noon` 에 `--dry-run` 신설 (이전엔 아예 없어 커밋을 막을 방법이 없었다).
- **`Vault.write_digest` 가 더 적은 편수로 기존 디제스트를 덮지 않는다.** frontmatter 의 `n_papers` 를
  비교해 새 결과가 더 적으면 쓰지 않고 이유를 로그로 남긴다. `--force` 로만 덮어쓸 수 있고,
  덮어쓸 때도 `vault/Digests/.backup/<date>.<타임스탬프>.md` 로 원본을 남긴다.
  (게이트 하나만으로는 부족하다 — 둘 다 있어야 같은 사고가 재발하지 않는다.)
- 회귀 테스트 `tests/test_dryrun_safety.py` 6건 — 사고 메커니즘 자체(0편이 5편을 덮는 것)와
  dry-run 부작용 차단을 각각 검증. 총 14 passed.
### Added
- `ra sync` 가 병합 후 **분석이 비어 있는 `triaged` 논문을 자동으로 큐에 넣는다.**
  클라우드가 초록 수준까지만 본 논문을 로컬(교내망·PDF)에서 `paper-analyst` 로 이어받는 경로.

## [0.1.2-dev] — 2026-09-04 (진행 중)
### Added — 브랜치 판정 반영 (Claude Code 2차 보고)
- `config/research_profile.md` **FILLED** — 두 브랜치 전수 조사 결과로 채움. 축이 **셋**임이 확인됨:
  A(DEM/MPM/voxelization, `stoic-knuth-NObVQ` 2652커밋) · B(DFT/MLIP, `friendly-meitner-lldvar`) · C(실험 협업, 이종원 그룹)
- 분석 스키마: `connection_to_my_work.anode_free` → **`.experimental`**(축 C), **`scooping_alert{hit,target,why}`** 신설
- 디제스트·노트에 **선점 경보** 렌더링 — 경보 논문은 Tier와 무관하게 최상단
- `triage.py` 용어 가중치를 세 축 기준으로 재작성 (MPM·Taichi·voxel·Kirchhoff·Holm·LOBSTER·ICOHP·BVSE·EIS·Li-In 등 추가)
- Cowork 트리거 2개를 메모리 `/areas/research-profile.md` 우선 참조로 교체 + 경보·비판 체크리스트 주입
### Fixed — Cowork 추측 오류 3건 (브랜치가 정정)
- "DFT→MLIP→DEM→FEM 단일 파이프라인" → 축은 별개 (사용자 명시 금지 사항)
- "MPM/voxelization은 문헌 단계" → **production**, 최근 90일 최다 주제(283회)
- "두 litdb 통합 여부 미결" → 2026-07-16 결정 완료. 정본은 `friendly-meitner-lldvar/litdb/`(208장), `stoic-knuth` 것(64장)은 **동결**
### Changed
- `sources.scholar_email.enabled: false` — alert 수집은 클라우드 전담(중복 방지). 같은 IMAP 자격증명은 `ra sync`의 handoff 병합에만 사용
### Changed — 연구 프로필을 '추측'에서 '브랜치가 채우는 슬롯'으로
- `config/research_profile.md` 를 **STUB**으로 초기화. Cowork(클라우드)가 추측으로 쓴 연구 내용 전부 제거.
  이 파일은 두 브랜치(`claude/friendly-meitner-lldvar`, `claude/stoic-knuth-NObVQ`)를 읽은 Claude Code가 채운다.
- 사용자 정정 반영: 연구 축은 **DFT/MLIP** 과 **DEM/MPM/voxelization** 두 개이며 **서로 별개**.
  "DFT→MLIP→DEM→FEM 멀티스케일 파이프라인"이라는 서술을 모든 프롬프트·스킬·문서에서 제거.
- `prompts/deep_analysis.md`, Hermes SKILL.md, `paper-analyst` 서브에이전트, Cowork NOON 프롬프트에서
  연구자 정체 서술을 삭제하고 "프로필이 유일한 근거, 비어 있으면 연결점을 지어내지 말 것"으로 대체.
- 클라우드 작업은 repo를 못 읽으므로 메모리 `/areas/research-profile.md` 를 프로필 소스로 참조하도록 변경.

## [0.1.1] — 2026-09-04
### Changed
- 키워드 `anode-less assb` 추적 중단(사용자 요청). `config/agent.yaml`에서 `active: false` — 기존 노트 2편은 아카이브로 보존, 새 alert는 `rejected("키워드 추적 중단")`
- triage: 비활성 키워드에만 잡힌 논문은 자동 rejected (`TriageConfig.active_keywords`)
- Cowork 클라우드 작업 2개 등록(NOON 12:00 / MORNING 09:00 KST) — `cowork/README.md`
- 첫 디제스트(2026-09-04) Cowork Gmail로 발송·DB 기록

## [0.1.0] — 2026-09-04 (prototype)
### Added
- `ra` CLI: status / ingest / triage / analyze / vault / litdb / digest / noon / morning / sync / handoff / schedule
- Google Scholar alert 파서 (HTML `gse_alrt_title` + text fallback, `scholar_url` unwrap, DOI 추출) + fixture 테스트
- IMAP 수집(Gmail 앱 비밀번호), 수동/bootstrap JSON 드롭 폴더
- Crossref/OpenAlex/Semantic Scholar 메타·초록 보강 (로컬 전용, 실패 시 무시)
- 저널 IF 테이블(JCR 2024 근사값, 80여 종) + 정규화 매칭 + 프리프린트 처리
- Triage: 규칙 기반 관련도(3축 core/system/property 가중치) + LLM 재평가 병합, IF-우선 priority, Tier A/B/C
- 심층 분석 계약(`prompts/deep_analysis.md` JSON 스키마) + 큐 프로토콜(`data/analysis/pending`) + 검증/적용(tier 재계산)
- LLM 백엔드: anthropic / claude-cli / hermes(큐) / none
- SQLite DB(papers·alerts·digests·runs) + JSONL 미러, idempotent upsert(DOI/제목 병합)
- Obsidian vault 렌더: 논문 노트(frontmatter·callout·wikilink), 키워드 MOC, 홈 MOC(dataview), 디제스트
- 디제스트 결정적 렌더(Tier별 깊이, 오늘의 한 줄, References) + SMTP 발송(md→html, .md 첨부)
- 클라우드↔로컬 릴레이 `ra-handoff/1` (self-mail JSON 첨부, `ra sync` 병합)
- litdb 내보내기 (file: JSONL/SQLite 병합 · cli: `litdb add DOI`)
- Hermes 스킬 `paper-agent`(SKILL.md, scripts, references) + cron 등록 가이드
- Claude Code: CLAUDE.md, `/paper-noon` `/paper-morning` `/paper-sync`, `paper-analyst` 서브에이전트
- Cowork 예약 작업 프롬프트(noon/morning) 사본 (`cowork/`)
- 문서: README, ARCHITECTURE, SETUP_CLAUDE_CODE, SETUP_HERMES
- Bootstrap: 6편(Nature Commun. ×3, Nature, Adv. Mater., Front. Chem.) 수집·분석·디제스트 생성

### Known limitations
- 샌드박스에서는 출판사 API/페이지 접근이 제한돼 일부 논문이 title/snippet 근거로 분석됨 → 로컬 재분석 필요
- litdb `field_map`은 실제 브랜치 스키마 확인 전 기본값
- `ra quick`(alert 즉시 인사이트)은 미구현(v0.2)
