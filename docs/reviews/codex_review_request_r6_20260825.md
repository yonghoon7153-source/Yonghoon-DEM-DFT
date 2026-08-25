# Codex 6차 리뷰 요청 — **원고 주장에 코드가 충분한가** (2026-08-25)

⚠ **5차와 스코프가 다르다.**  5차는 "이 코드를 감사하라" 였고, 그래서 리뷰가 코드 결함을
무한히 찾았다 (그것이 감사자의 일이다).  이번엔 묻는 것을 좁힌다:

> 이 브랜치는 아래 **원고 주장**을 뒷받침해야 한다.  그 주장들에 대해 코드가 **충분히**
> 믿을 만한가?  충분하지 않다면 **어느 주장이** 왜 못 서는가?

코드 위생 지적은 환영하지만 **P 등급을 붙이지 말아 달라** — 주장에 걸리는 것만 P1/P2 로.
그래야 이 브랜치가 닫히는 조건이 정의된다.

---

## 0. 재현

```bash
git clone <bundle> repo && cd repo
git checkout claude/sdcp-dem-manuscript-si-pqwtv8
bash scripts/check_all.sh                    # 검사기 selftest + 리포 실물
python3 scripts/mutation_sweep_20260825.py   # 돌연변이 배터리 (~20 분)
```
⚠ `scipy`·`numpy` 가 필요하다.  없으면 solver 의존 시험은 **건너뛰고 그렇게 보고**한다
(5차에서 리뷰어가 크래시를 손으로 "환경 탓" 이라 판단해야 했던 것을 고쳤다).

---

## 1. 원고가 실제로 주장하는 것

정본 = `docs/manuscript_draft/DEM_methodology_and_tables_v1.docx`
(⛔ 파일 머리에 DRAFT 배너 — 수송값은 hold).

**A. Manuscript §4 Experimental Section** — 미세구조 재구성 방법 (DEM → MPM → 복셀).
**B. SI Table S2** — 재료 파라미터 (기계 물성 · σ 배정).
**B. SI Table S3** — 구조·수송 파라미터.  ★ **현재 전 칸이 `—` 다** (수송은 재측정 대기,
구조는 vox 0.15 재추출 대기).

⇒ **지금 이 브랜치가 뒷받침해야 하는 주장은 "방법" 이지 "값" 이 아니다.**
   값은 C(GPU 16런) 뒤에 들어온다.

### 이번 리뷰가 답해 주길 바라는 것

1. **방법 서술이 코드와 일치하는가.**  §4 와 Table S2 가 적은 규약(복셀 크기·스탬프·
   plate rule·σ 배정·경계조건)이 `step3_sigma.py`·`mpm_webapp_payload.py` 가 실제로 하는
   것과 같은가.  다르면 그것은 **원고 결함**이다.
2. **값이 들어올 때 그 값이 봉인되는가.**  C 를 돌리면 Table S3 이 채워진다.  그때
   "이 값이 이 규약에서 나왔다" 를 기계가 보증하는가 (run receipt · protocol id · 증거 계약).
3. **철회된 값이 다시 못 들어오는가.**  p1 정량값이 원고·요약·발표로 새는 경로가 남았는가.

---

## 2. 5차 이후 무엇을 했나 (P1 6 · P2 4)

| R5 | 조치 |
|---|---|
| CX-01 `P2_EXTRA` 2단계 shell 확장 | 문자 allowlist(부정 목록 아님) + 생성물 실물 검사.  `L-13` 5시험 |
| CX-02 schema downgrade | 세대를 **규약 완비**로 관찰 (`observed_generation`).  신고 < 관찰이면 HOLD.  `F1~F5` |
| CX-03 run identity 미봉인 | **run receipt** — resolved config·code SHA·origin 일정.  OUTDIR 이 receipt digest 로 갈린다.  `H1~H8` · `L-14a/b/c` |
| CX-04 임의 8-origin | `{0,vox/2}³` 를 vox 에서 **계산**해 equality.  ⚠ **내 픽스처 5개가 전부 z-only 였다** — 먼저 고치고 게이트를 세웠다.  `㊺a~f` |
| CX-05 PNM·collector status-only | `COMPONENT_RESULT` 결과 계약 + **미등록 component 는 HOLD**.  `G1~G7` |
| CX-06 canonical ban 모순 | CL-33/41/58 → `hold` · ban 12→22 패턴 · CLAUDE.md·역사문서·**원고 `.docx`** 정합 |
| CX-07 pass-mutant·harness | `across_dir` 불변량을 레지스트리 전 축으로 · harness 셋 · `M_UNWRITTEN`.  ⚠ **범주 오선택은 미해결** (§4) |
| CX-08 기각 receipt 미소비 | `HOLD/REJECTED_TREE`.  `㊻a/b` |
| CX-09 SWCNT plate 하드코딩 | 생산 σ 표를 공용 함수로 (`electronic_sigma_table`/`ionic_sigma_table`).  `rxn-table-production` |
| CX-10 blind 파생 bucket | 값 무관 상수.  회귀를 **이름이 아니라 거동**으로 (`J-4a/b`) |
| CX-11 bundle SHA | clone HEAD == intended SHA · SHA-256 출력 |

---

## 3. ★ 이번에 내가 만든 사고 — 그대로 적는다

**CX-07 을 고치면서 harness 에 결함 셋을 새로 넣었고, 고친 뒤 배터리를 한 번도
끝까지 안 돌리고 커밋했다.**  사용자 기계에서 41 중 36 이 빨간불이 났고, 그 36 은
**전부 내 오탐**이었다 (실제 코드 결함 0):

· `_tid` 가 `B2 설명` 꼴(콜론 없음)에서 ID 를 못 떼어 **기대 ID 가 아무것도 안 맞았다**
· 시험 이름에 런타임 값이 박혀 있어(`㉗a … (30.95…)`) 거동이 바뀌면 이름도 바뀌고,
  이름으로 baseline 을 비교하니 정상 적발이 전부 "시험이 사라졌다" 로 분류됐다
· `.sh` mutant 를 **파이썬으로** compile 해 셸 변이가 전부 "문법 오류" 가 됐다

⇒ 셋 다 고쳤고 이번엔 **끝까지 돌린 결과를 첨부한다**.
⚠ 그러나 이것은 R5-CX-07 이 지적한 바로 그 부류(harness 자신이 못 미덥다)가 **한 번 더**
  일어난 것이다.  이 자리를 특히 봐 달라.

**둘째 — R5-CX-06 대응이 내구적이지 않았다 (SELF-08, 요청서 작성 중 자체 발견).**
원고 `.docx` 의 Table S3 셀에서 hold 값을 뺐는데, 그 `.docx` 는 **생성물**이고 정본은
`docs/manuscript_draft/build.js` 다.  생성기에는 그 값이 그대로 남아 있어서
`node build.js` 한 번이면 철회값이 표에 되살아난다.  그런데 철회-스윕은 **"누수 0"** 을 냈다:

· `BAN_SCAN_GLOBS` 에 `docs/**/*.js` 가 없어 **생성기를 아예 안 읽었다**
  (덱 생성기 `scripts/seminar_deck/*.js` 는 같은 이유로 이미 등재돼 있는데 원고 쪽만 빠졌다)
· 원고 `.docx` 자신은 머리 배너가 원장을 지목해 **파일 전체가 면제**라, 출력 쪽에서는
  원리적으로 못 잡는다 — 즉 **표 셀을 실제로 지키는 자리는 생성기뿐이었다**
· ★ 거울상 하나 더: **⛔ DRAFT 배너도 `.docx` 에만 손으로 넣어 뒀다** ⇒ 재생성하면 배너가
  사라지고 원고가 면제를 잃어 D 절 설명 문단이 **전부 누수로 뒤집힌다**

⇒ 글롭에 생성기를 넣고(`node_modules` 제외), 셀·배너·D2 메모를 전부 생성기 쪽에 두었다.
   회귀 `22f`(글롭을 도로 빼면 FAIL 하는 것을 확인) · `22g`(남의 코드는 안 읽는다).
⚠ 이것도 **검사기가 못 읽는 매체에서 조용히 초록**이 되는 그 부류다 (CDXIJ-4/9 의 pptx,
  A1 의 AST 필터에 이어 **세 번째**).  매체가 이번엔 '생성기' 였다.

**★ 그래서 리포의 생성기를 전수로 훑었다** (산출물을 쓰는 파일 = `Packer.toBuffer` ·
`python-pptx` · `writeFileSync(process.argv…)` 로 잡음).  다섯이 나왔다:

| 생성기 | 스윕 대상 | 철회값 |
|---|---|---|
| `docs/manuscript_draft/build.js` | **이제 덮음** (이번 고침) | 있었음 → 제거 |
| `scripts/seminar_deck/build.js` | 덮음 (전부터) | 없음 |
| `scripts/make_network_pptx.py` | 안 덮음 (`.py` 정책) | **없음** (직접 확인) |
| `scripts/seminar_deck_extract.py` | 안 덮음 (`.py` 정책) | **없음** (직접 확인) |
| `webapp/app.py` | 안 덮음 (`.py` 정책) | 있으나 **철회 배너 문자열 자체** (`_RETR`, fail-closed 주입기) |

⇒ 지금 실제 누수는 0 이다.  ⚠ 다만 **정책 구멍은 남는다**: `scripts/*.py` 를 글롭에서 뺀 것은
  *"그쪽 등장은 대부분 철회를 설명하는 주석"* 이라는 근거인데, **생성기는 주석이 아니라
  산출물을 만든다**.  오늘은 `.py` 생성기 셋이 다 깨끗해서 문제가 안 됐을 뿐이고, 규칙이
  막아 준 것이 아니다.  ⇒ 이 판단(전부 `.py` 를 넣으면 정당한 주석 언급이 쏟아진다 vs
  생성기만 골라 넣으면 "고르는 코드가 사각지대" 라는 A1 의 교훈에 걸린다)을 **봐 달라**.


**셋째 — `_tid` 를 고치자 배터리가 처음으로 제대로 돌았고, 곧바로 6 행이 계약을 못 맞췄다
(SELF-09).**  다섯은 배터리 자신의 결함이었고 **하나는 진짜 회귀 공백**이었다:

· ★ **R5-CX-03 의 영수증 대조에 회귀가 없었다** — `sr01_stamp_compare.py` 의 `if receipt:`
  를 통째로 지워도 selftest 는 초록이었다.  `run_contract` 의 H1~H8 은 순수 함수
  `receipt_match` 를 지키지 **그 함수를 부르는 자리**를 지키지 않는다.
  ⇒ 8y1~8y4 신설(81 → 85), 게이트를 지우면 8y2·8y3 이 실제로 FAIL 하는 것을 확인했다.
  **함수를 시험한 것과 그 함수를 부르는 자리를 시험한 것은 다르다** — R5 에서 이 구분을 놓쳤다.
· `[] or sorted(...)` 는 `sorted(...)` 라 M_UNWRITTEN 변이가 **완전한 no-op** 이었다
· 영수증 행이 `sr01` 을 변이시키고 **`run_contract` selftest** 를 돌렸다 (파일↔명령 짝 오류)
· origin 두 게이트는 **서로 여분**이라 하나만 꺼도 다른 하나가 잡는다 — 단독 변이의 rc=0 을
  '회귀 없음' 으로 오보했다.  여분은 결함이 아니므로 상류 한 점을 눌러 둘을 같이 죽이는
  한 행으로 합쳤다
· PNM/collector 계약을 끄면 **무엇이든 거부**가 되어 '거부해야 한다' 시험이 **거저 통과**한다.
  실제로 무는 것은 **정상 증인**이다 ⇒ ★ **음성 시험만으로는 '전부 거부' 회귀를 못 잡는다.**

⚠ 다섯 모두 **기대집합이 틀려 있었다**.  즉 배터리가 `적발` 이라고 적은 다른 행들도
  *기대 id 가 옳다는 보장은 없다* — **이 자리를 봐 달라**: 기대집합 자체를 어떻게 검증하나?

---

## 4. 스스로 못 닫은 것

· **회계 범주 오선택** (R5-CX-07 잔여) — `--step3-maxiter→mode` 처럼 범주를 **낮게** 적는
  것은 정적으로 못 잡는다.  옵션을 토글해 규약 해시가 움직이는지 봐야 하고 그것은
  solver 런이다.  `protocol` 로 적고 안 적히는 축은 `M_UNWRITTEN` 이 잡지만 반대 방향은 못 잡는다.
· **`σ_SDCP = 250` 출처** — 캐스트 필름인지 압착 펠릿인지 미상.  펠릿이면 접촉저항이
  포함된 값인데 복셀 솔버는 접촉을 융합하므로 이중계상이다 (CL-47 이 σ_VGCF 에서 지적한 부류).
  **사용자 회신 대기.**
· **`ρ_SDCP`** — 코드에 `1.30 g/cm³` 가 "PROXY, REPLACE with the user's manuscript value" 로
  박혀 있다.  wt%→vol% 환산에 쓰이므로 침대 조성이 걸린다.
· **실침대 CPU census** (B) — kit 침대가 사용자 기계에만 있어 이 리포에서 못 돈다.

## 5. 이 요청이 **주장하지 않는 것**

σ_e 절대값 · SBE/DBE 이득 비 — `claims.json` 의 `quotation_ban` 이 강제한다.
p1 과 p2 산출물은 섞지 않는다.
