# 본체 브랜치로 넘기는 merge 브리프 — `claude/bms-alpha-beta-verify`

> **이 파일은 본체(`claude/14-gate-code-review-9qkx05`) 세션에 그대로 붙여 넣어 읽히려고 쓴 것이다.**
> 서브 브랜치가 무엇을 했고, merge 가 안전한 이유와 **안전하지 않은 한 곳**, 그리고 본체가 직접
> 확인해야 할 명령을 전부 적는다. 요약을 믿지 말고 **여기 적힌 명령을 실제로 돌려** 확인하라 —
> 이 저장소의 규율이 그것이다 ("검증 없는 완료 선언 금지").

작성 시점의 서브 HEAD: `511cea3`. 본체 HEAD: `de36bb9`. 분기점(merge-base): `fdd3929`.

---

## 0. 한 문장

**서브가 `bms-balancing/` 에서 175 커밋을 쌓았고, 본체와 겹치는 파일은 0 개다. 단 `webapp/` 6 파일은
경계를 넘었고 그 처리만 본체가 정하면 된다.**

---

## 1. merge 대상 — 경로별

| 경로 | 무엇 | 본체와 겹치나 |
|---|---|---|
| `bms-balancing/**` | 서브 소유. 하네스 코드·테스트 311개·문서·보존 묶음 | **안 겹침** (본체가 손댄 적 없음) |
| `webapp/**` (6 파일) | **경계 넘음** — §3 참조 | 안 겹침 (지금은), 소유는 본체 |
| `wiki/**` · `degradation-degeneracy/**` · 루트 문서 | 서브가 **읽기만** 했다. 한 글자도 안 고쳤다 | — |

`bms-balancing/` 은 92 MB 이고 그중 77 MB 가 `reviews/r14_repros/` 의 **외부 전달 묶음 원문 보존**이다
(COMSOL handoff ZIP 아홉 개의 md·json·csv·txt; mph·로그·java·py·그림은 제외). 이 bytes 는 옆의
`package_manifest.json` 이 sha256 으로 서명하고 있어 **정규화하면 안 된다** — §5-3 참조.

---

## 2. 충돌이 없다는 것을 본체가 직접 확인하는 법

```bash
B=$(git merge-base origin/claude/14-gate-code-review-9qkx05 origin/claude/bms-alpha-beta-verify)

# (a) 양쪽이 같이 건드린 파일 — 비어 있어야 한다
comm -12 \
  <(git diff --name-only $B origin/claude/bms-alpha-beta-verify | sort) \
  <(git diff --name-only $B origin/claude/14-gate-code-review-9qkx05 | sort)

# (b) 서브가 bms-balancing 밖에서 건드린 것 — webapp 6 개만 나와야 한다
git diff --name-status $B origin/claude/bms-alpha-beta-verify -- . ':(exclude)bms-balancing'

# (c) 본체가 fork 이후 건드린 경로 — wiki/ 만 나와야 한다
git diff --name-only $B origin/claude/14-gate-code-review-9qkx05 | sed 's#/[^/]*$##' | sort -u

# (d) 실제 merge 를 시험만 해 본다 (커밋하지 않는다)
git merge --no-commit --no-ff origin/claude/bms-alpha-beta-verify
git merge --abort
```

작성 시점 실측: (a) **0 줄** · (b) **6 줄(전부 webapp)** · (c) **wiki/ 만**.

---

## 3. ⚠ 경계를 넘은 유일한 곳 — `webapp/` 6 파일

`CLAUDE.md` 하드룰 1 은 서브가 `bms-balancing/` 밖을 **읽기만** 한다고 못 박는다. 이 여섯은 그것을 넘었다.
**사용자가 세션에서 직접 두 번 지시했다** ("지금까지 이룬 것들 webapp 에 차근차근 정리를 해줘요" ·
"협업방향은 이제 끝났으니까 없애도 돼" · 이후 "원문 유지하고 밑에 쉽게 풀어 설명하는 것"). 우회로
(문서만 `bms-balancing/` 에 두고 배선은 본체에 넘기기)로는 **화면에 안 떠서** 지시의 핵심을 못 지켰다.

| 파일 | 변경 |
|---|---|
| `webapp/templates/bms.html` | **신규** — BMS 세 갈래의 "지금까지 이룬 것" (`/bms`) |
| `webapp/templates/alphabeta.html` | **신규** — 옛 `handover.html` 본문을 **한 글자도 안 고치고** 되살리고 §0 용어 + 절마다 "쉬운 말로" 칸 (`/alphabeta`) |
| `webapp/templates/handover.html` | **삭제** (git rename 으로 잡혀 `alphabeta.html` 과 R062 로 보인다) |
| `webapp/app.py` | `/handover` 라우트 → `/bms` · `/alphabeta` 둘 |
| `webapp/templates/base.html` | nav 절 "방향" → "BMS 트랙" (두 줄) · `plain.css` 링크 |
| `webapp/static/css/plain.css` | **신규** — "쉬운 말" 칸·용어 목록 스타일 (토큰만 써서 라이트/다크 따라감) |
| `webapp/README.md` | 라우트 표 두 줄 |

**본체가 고를 것 — 둘 중 하나:**

1. **그대로 받는다.** 그러면 `CLAUDE.md` 하드룰 1 의 소유 경로 줄에 예외를 **한 줄** 적는다
   (이름 정본이 한 줄인 것과 같은 이유로, 예외도 한 곳에만).
2. **되돌리고 본체가 다시 만든다.** `webapp/templates/bms.html` 과 `alphabeta.html` 은 그대로 가져가면
   되고, 나머지 넷은 라우트·nav 배선뿐이다.

**검증 범위 (서브가 못 한 것)**: 서브 컨테이너에 Flask 가 없어 **화면을 띄워 보지 못했다.** 확인한 것은
jinja2 구문(템플릿 18 개) · `app.py` 구문 · 라우트↔템플릿↔nav 이름 일관 · CSS 클래스 34 개 존재 ·
태그 균형까지다. **브라우저에서 뜨는 것은 아직 확인되지 않았다.**

**덤으로 신고**: `webapp/templates/pipeline.html:366,433` 이 게이트 라운드 수를 **"57라운드"** 로
하드코딩하고 있다. 실제는 61차 대응까지 마감이라 넉 라운드 뒤처졌다. 서브가 안 고쳤다 — 본체가 61 로
맞추든지, `/trust` 처럼 **세어서** 만드는 자리로 바꾸든지 정하면 된다 (하드룰 4 가 경고하는 바로 그 모양이다).

---

## 4. 서브가 낸 것 — 세 갈래

### 4-1. ③ BML α·β 열화 정량화 — **과학적 결론이 나온 곳**

네 단계를 밟았고 각 단계가 앞 단계의 답을 뒤집었다. 정본은 `bms-balancing/reviews/BML_R1_RESPONSE.md`.

1. 규진팀 결과 CSV 97 행을 세었다 — **32 행이 상자 경계에 정확히 붙음** · 16 행이 음수 LAM ·
   한 상태의 LAM_NE 폭 34.7 %p (§2)
2. 원본 MATLAB 을 받아 주장 사슬을 **전부 철회**하고 소스에서 다시 세웠다. 반복값의 원인은
   `rng(0)` 전역 오염이고 **규진팀이 이미 찾아 고친 것**이다 (§9)
3. 우리가 다시 뽑았다 — 그들 파이프라인(rng 없이)과 우리 포팅이 **~1e-3 안에서 일치**, 경고 0,
   시작점 의존 1e-7 (§10·§11)
4. **pyDMA 공개 검증 예제(P45B)에 걸었다** (§12) — **LLI 는 세 구현이 0.09~0.18 %p 안에서 일치**하고
   **LAM 두 축은 1.0~1.5 %p 로 흩어지며 CU2 음극은 부호까지 갈린다.** pyDMA **자신의 두 방법도** 같은
   축에서 갈린다
5. **결정 실험 (§12-5)** — γ 초기값을 0.25 → 0.0200 으로, 하한을 0 → 0.02 로 옮겼는데 **CU2 의 네 값이
   표시 자리까지 전부 같다.** 즉 **LAM 차이는 설정이 아니라 식별 가능성**이다
6. **그 결론을 도구에 반영 (§13)** — `fit_cycles --widths` 가 사이클마다 폭을 **점추정과 같은 행에** 낸다

> **본체에 값어치가 있는 지점**: 이것은 `degradation-degeneracy` 의 축퇴 결론("A 축에서 LLI 가 항상 가장
> 좁다")과 **같은 모양**이고, 합성 진실이 아니라 **남의 데이터·남의 구현**에서 독립으로 나왔다.
> 게이트 요청문에 실으면 리뷰어가 "합성 진실에만 기댄다" 는 축을 더는 못 쓴다. 62차 준비는
> `HANDOFF_TO_GATE.md` §2d 에 따로 적어 뒀다.

### 4-2. ② α·β 검증 하네스

산출 다섯 종(`matrix`·`profile`·`degeneracy`·`shape`·`cycles`)에 계약·서명·validator. 외부 적대적
게이트 리뷰 **R13 조건 7 닫음 · R14 GO**(`3aca090`). 테스트 **311 passed**.

**R14 GO 의 범위를 넓히지 말 것** — R14 범위 한정이고 전체 하네스·BML 과학 타당성·COMSOL·장시간 실행
승인이 아니다. 리뷰어가 전수 재실행을 하지 않았다고 스스로 밝혔다.

### 4-3. ① 마이크로쇼츠 COMSOL 6.3 재구축

정본은 `bms-balancing/docs/COMSOL_REBUILD_SPEC.md` §8~§18. 원본 모델에 대한 우리 주장(M1)을 **철회**하고
명세를 다시 썼다. 여섯 축 + 코어 대조군의 진단이 **원문 대조·재계산**까지 끝났다.

**이 갈래에는 "모델 검증 완료" 도 "본 실행 GO" 도 없다.** 전체 수렴 미완 · 장시간 운전 보류 · 전해질
양수는 후처리 검사 · 4.25 V CV 가 양극 OCP 표 하한과 충돌하는 문제 그대로.

---

## 5. merge 전에 본체가 직접 돌려 볼 것

### 5-1. 테스트

```bash
cd bms-balancing && python3 -m pytest tests/ -q     # 311 passed 기대
```

`WORKING_STATE.md` 의 "N passed 기대" 핀과 수집 수가 **같아야** 한다 (`test_i6d_04` 가 기계로 검사한다).

### 5-2. 하네스 계약

```bash
cd bms-balancing
python3 scripts/check_u14.py --new out --schema-only     # 스키마·내용·조건
python3 scripts/check_rails.py out/cycles_*.csv 2>/dev/null || echo "(cycles 산출은 사용자 기계에 있다)"
```

⚠ `check_u14` 의 rc 0 을 기대하지 말 것 — **작업 트리가 dirty 하면 provenance 로 막히는 것이 정상**이고
그게 그 게이트의 일이다. 봐야 할 것은 `PROMOTION` 줄의 `blocked_by` 에서 **schema·content·unit·
controls·numbers·alias 가 0** 인가다.

### 5-3. ⚠ 보존 묶음의 bytes — 여기가 제일 깨지기 쉽다

`reviews/r14_repros/codex63/*/` 는 **외부에서 온 원문 bytes** 이고 옆의 `package_manifest.json` 이
sha256 으로 서명한다. `.gitattributes` 의 `-text` 규칙이 줄끝 정규화를 막고 있다.

```bash
# 묶음마다 이렇게 확인한다 (저장소 **루트**에서)
python3 - <<'CHECK'
import hashlib, json, pathlib, subprocess
root = pathlib.Path("bms-balancing/reviews/r14_repros/codex63")
for d in sorted(x for x in root.iterdir() if x.is_dir()):
    mans = sorted(d.rglob("package_manifest.json"))
    if not mans:
        continue
    # ⚠ 묶음에는 **이전 묶음의 manifest 가 같이 들어온다** (core16_control 에는 셋).
    #   폴더 이름으로도 payload 수로도 못 고른다 (둘 다 실측으로 빗나갔다).
    #   이번 것은 **자기 entry 가 디스크에 가장 많이 있는** manifest 다 — 보존이 그것만 복사했기 때문이다.
    def present(m):
        try: es = json.loads(m.read_text(encoding="utf-8")).get("entries") or []
        except Exception: return (-1, m)
        return (sum(1 for e in es if (d / e["path"]).is_file()), m)
    _, man = max((present(m) for m in mans), key=lambda t: t[0])
    m = json.loads(man.read_text(encoding="utf-8"))
    ok = bad = skip = 0
    for e in m["entries"]:
        rel = f"{d}/{e['path']}"
        try: blob = subprocess.run(["git", "show", f"HEAD:{rel}"], capture_output=True, check=True).stdout
        except subprocess.CalledProcessError:
            skip += 1; continue
        if hashlib.sha256(blob).hexdigest() == e["sha256"]: ok += 1
        else: bad += 1; print("   X", e["path"])
    print(f"{d.name:16s} 일치 {ok:4d} · 불일치 {bad} · 미보존 {skip:3d}   (manifest: {man.parent.name})")
CHECK
```

작성 시점 실측 — 여덟 묶음 전부 **불일치 0**:

```
core16_control   일치  162 · 불일치 0 · 미보존  72   (manifest: core16_control)
late_cap_a       일치  140 · 불일치 0 · 미보존  61   (manifest: late_cap_a)
mesh_axes        일치   90 · 불일치 0 · 미보존  49   (manifest: mesh_axes)
r160_timecap     일치  186 · 불일치 0 · 미보존  81   (manifest: radial160_timecap)
r320_timecap     일치  114 · 불일치 0 · 미보존  46   (manifest: radial320_timecap)
radial160        일치  112 · 불일치 0 · 미보존  48   (manifest: radial160)
radial320        일치  103 · 불일치 0 · 미보존  44   (manifest: radial320)
time_caps        일치  136 · 불일치 0 · 미보존  65   (manifest: time_caps)
```

**불일치는 전부 0 이어야 한다.** 0 이 아니면 어딘가에서 줄끝이 정규화된 것이고, 그러면 그 묶음은
증거로 못 쓴다. 실제로 한 번 그랬다 — `r320_timecap` 에서 `.gitattributes` 규칙보다 커밋이 먼저 가서
80 파일이 LF 로 정규화됐고, 원본 bytes 로 되돌려야 했다 (경위는 그 묶음의 `README.md`).

**세 가지를 틀리기 쉽다 (셋 다 서브가 실제로 틀렸다):**
- `git show HEAD:<경로>` 는 **저장소 루트** 기준이다. `bms-balancing/` 안에서 접두사 빼고 치면 전부
  "미보존" 으로 나온다 (실측: `일치 0 · 불일치 0 · 미보존 201`)
- 묶음에 **manifest 가 여럿**이다 (`core16_control` 에는 셋). `rglob` 으로 아무거나 집으면 엉뚱한
  것과 대조한다 (실측: `일치 21 · 불일치 1`)
- **폴더 이름으로도, payload 수로도 못 고른다.** `r160_timecap` 의 manifest 는 `radial160_timecap/` 에
  있고(이름 안 맞음), `radial160` 에는 더 큰 `time_caps` manifest 가 딸려 있다(수로도 안 맞음).
  위 스크립트가 쓰는 **"자기 entry 가 디스크에 가장 많이 있는 것"** 이 여덟 묶음 전부에서 맞았고
  차이도 컸다 (162 vs 51 · 186 vs 112 · 114 vs 35 …)

### 5-4. webapp — 본체 기계에서 **실제로 띄워** 볼 것

서브가 못 한 유일한 검증이다.

```bash
cd webapp && ./bms.sh          # 찍히는 포트로 들어가 /bms 와 /alphabeta
```

`/alphabeta` 는 왼쪽 nav `BMS 트랙` 아래 두 줄, 맨 위에 §0 용어 절, 각 절 끝에 초록 왼쪽선의
"쉬운 말로" 칸이 있어야 한다. CSS 가 새로 생겼으니 **Ctrl+Shift+R** 한 번.

---

## 6. merge 뒤에 본체가 **판단**할 것

1. **`webapp/` 를 받을지 되돌릴지** (§3) — 받으면 `CLAUDE.md` 하드룰 1 에 예외 한 줄
2. **`pipeline.html` 의 "57라운드"** (§3 끝) — 61 로 맞출지, 세는 자리로 바꿀지
3. **루트 `.gitignore` 에 `cells/` 한 줄** — 서브가 못 고치는 자리라 신고만 해 뒀다
   (`HANDOFF_TO_GATE.md` §2b). 저장소가 public 이고 그 디렉터리에 **규진팀 원자료 xlsx 사본**이 들어간다
4. **62차 게이트 준비** (`HANDOFF_TO_GATE.md` §2d) — P0 추세 13→2, 61차가 스스로 적은 진단, 요청 전
   `/self-review` 와 순서 전체 e2e 제안, pyDMA 외부 검증 증거의 위치
5. **`wiki/` 에 올릴 후보** (`HANDOFF_TO_GATE.md` §3) — 방법론 개념 페이지·Schmitt 계열 구현 결함 등.
   서브가 못 건드리는 자리라 목록만 뒀고 채택은 본체가 정한다
6. **축퇴 폭 측정법을 본체에 쓸지** (`HANDOFF_TO_GATE.md` §2) — 서브가 쓴 방법과 그 한계를 적어 뒀다

---

## 7. 서브가 **안 닫은 것** (인계)

| 항목 | 상태 |
|---|---|
| `legacy_transition_approved` · 기록용 CLI 인자 필수화 · U18-05 | 열림 |
| R13 조건 6(동적 인증) · 조건 8(다섯 축: snapshot·manifest·run receipt·partial 수명·locator) | 열림 |
| `openpyxl` 을 `ENV_KEYS` 에 넣을지 | 열림 |
| r11 대체 증거 | 열림 |
| pOCV 가 원자료인지 필터본인지 (U2) | 한 곡선으로는 원리적으로 못 가른다. 두 해석을 다 적어 뒀다 |
| γ 직접 적합(표현력)·공유 가능값 증인 (U9) | 미구현 |
| **held-out 예측** | 다른 셀의 **독립** 반쪽전지가 있어야 한다 — 가장 강한 검증인데 데이터가 없다 |
| 우리 `fit_gamma_si` 가 Track C 의 γ 0.224 를 재현 못 함 (하한 0.02 에 붙음) | 열림, **우선순위 낮음** — §12-5 때문에 LAM 결론을 안 바꾼다 |
| `mode_profile_extrema`(도달 가능성 격자)를 cycles 폭에 붙이기 | 안 했다 (상태 경로는 둘을 같이 쓴다) |
| COMSOL B (물리 300→600, 입자 320 고정, 원래 cap·16코어) | **계획 확인 단계** — 실행 미승인·미제출 |
| 옛 TIME_CAPS raw ZIP 두 개의 차이 원인 | **계속 미확인** |

---

## 8. 이 브랜치가 지킨 규율 — merge 뒤에도 유지해야 하는 것

1. **정본은 artifact + 문서다.** 화면·요약·대화의 숫자는 사본이고 인용 근거가 아니다 (하드룰 4).
   서브 문서 곳곳의 "인용 금지" 배너를 떼지 말 것
2. **경고를 떼지 않는다.** "충족" 옆의 "그러나 전체 수렴은 미완", "GO 는 범위 한정", "이 폭은 하한이다" —
   떼면 다른 주장이 된다
3. **안 잰 것과 0 을 구분한다.** `width_status` 가 tagged union 인 이유이고, 본체 게이트 61차 P1-3 과
   같은 축이다
4. **원자료는 커밋하지 않는다.** 규진팀 xlsx · `.mph` · MATLAB 원본. 저장소는 public 이다.
   문서에는 **결론만** 있고, 재현하려면 원자료를 가진 기계가 필요하다
5. **보존 묶음의 bytes 는 불변이다** (§5-3). 원본 영수증·실패 기록·failed 판정을 고치지 않는다
6. **merge 방향은 본체 ← 서브 하나뿐이다.** 반대로 가면 게이트 증거 사슬이 흐려진다 (하드룰 1)

---

## 9. 본체 세션에 붙여 넣을 요청문 (짧은 판)

> `claude/bms-alpha-beta-verify` (`511cea3`) 를 이 브랜치로 merge 하려 한다. 분기 이후 서브가 175 커밋을
> 쌓았고 본체는 `wiki/` 만 건드려서 **겹치는 파일이 0 개**다. 다만 서브가 `webapp/` 6 파일을 고쳐
> 하드룰 1 을 넘었으니 그 처리를 정해 달라.
>
> `bms-balancing/MERGE_BRIEF_FOR_GATE.md` 를 열어 §2 의 확인 명령 넷, §5 의 검증 넷(테스트 311 ·
> 하네스 계약 · **보존 묶음 bytes** · webapp 화면)을 **직접 돌려** 확인한 뒤, §6 의 판단 여섯을 해 달라.
> 요약을 믿지 말고 명령을 돌려라 — 특히 §5-3 의 보존 bytes 는 틀리기 쉬운 함정이 둘 있다.
>
> merge 뒤 얻는 것: pyDMA 외부 검증(§4-1)이 게이트 요청문에 실을 **새 축의 증거**다. 62차 준비는
> `bms-balancing/HANDOFF_TO_GATE.md` §2d 에 적어 뒀다.
