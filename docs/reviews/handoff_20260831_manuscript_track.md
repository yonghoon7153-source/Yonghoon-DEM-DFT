# 인계 — manuscript-track (2026-08-31)

앞 인계: `docs/reviews/handoff_20260830_manuscript_track.md`.  그 문서의 §6(인용 금지)은
**그대로 유효**하다.  이 문서는 그 뒤 **95 커밋**(`bde5929e..c0436bd0`)을 인계한다.

## 0. 한 줄

원고에 실을 **전자 축 수치가 확정됐고**(σ_e 비 · 접점 분포), 그 값을 그림으로 옮기는
사슬(뷰어 콜러바 → 그림 → 캡션)이 라벨까지 닫혔다.  **이온 축은 4 시나리오 중 1개만
완주**했고 나머지 셋이 kgy 에서 돌고 있다.

---

## 1. ★ 먼저 할 것 — 이 브랜치를 따라잡는다

```bash
cd ~/Yonghoon-DEM-DFT              # 로컬 리포 경로에 맞게
git fetch origin manuscript-track
git checkout manuscript-track
git merge --ff-only origin/manuscript-track
git log --oneline -1               # c0436bd0 이면 최신
```

⚠ `--ff-only` 가 거부하면 로컬에 미푸시 커밋이 있는 것이다.  **강제로 덮지 말고**
`git log --oneline origin/manuscript-track..HEAD` 로 무엇인지 먼저 본다.
⚠ `git fetch --depth` 금지 (얕은 클론이 검사기의 SHA 실재 확인을 깬다).

따라잡은 뒤 상태 확인:

```bash
bash scripts/check_all.sh          # ⚠ 파이프로 넘기지 말 것.  로그 마지막 줄을 읽는다
```

읽어야 할 정본 3개 (순서대로):
1. `docs/reviews/table_s3_data_20260827.md` §18~§20 — 접점·운영규칙·이온 8팔
2. `docs/reviews/ms_si_v6_edit_sheet_20260831.md` §H~§K — 원고 편집 시트(저자 결정 포함)
3. `docs/reviews/codex_r18_verdict_20260831.md` — 마지막 적대 리뷰 판정

---

## 2. 지금 돌고 있는 것 — 이온 8팔 시나리오 2~4 (kgy)

등록: `docs/reviews/ion_8arm_prereg_20260831.md`.  4 시나리오 × 8 origin = 32 팔.

| 시나리오 | `SIGMA_ION_SDCP` | 상태 |
|---|---|---|
| 1 | `0` | ✅ 완주 · 반입 완료 (`docs/data/ion8_isd0_20260831`, 원장 §20) |
| 2 | `5.5216e-05` (Maxwell–Garnett 역산) | 진행 중 — job `isd55216e-05` |
| 3 | `5.21007e-04` (RSA 역산, D13 보정값) | 대기 |
| 4 | `1.0e-03` | 대기 |

**회수 절차** (kgy 에 이 세션이 만들어 둔 것):

```bash
watch -n 120 bash ~/w.sh           # 진행 감시.  16/16 이면 완주
bash ~/pack.sh isd55216e-05        # 축소 → 검증 → 커밋 → 푸시까지 한 번에
```

`~/pack.sh` 가 마지막에 두 줄을 찍는다 — `σ_e w4 비트동일` / `σ_ion SBE~DBE`.
그 두 줄을 원장 §20 에 이어 적는다 (시나리오별 절 추가).

⚠⚠ **런 도중 `~/dem-mt` 워크트리를 건드리지 마라** — 체크아웃도, 되돌리기도
`_code_sha` 를 `+dirty` 로 바꿔 receipt 계약을 깬다 (실사고 기록: 원장 §19).
코드를 봐야 하면 `git show origin/manuscript-track:<경로>` 로 `/tmp` 에 떠낸다.
⚠ **kgy `dem-venv` 에 pip install 금지** — 의존이 numpy 를 끌어올리면 살아 있는 런 밑에서
numpy 가 바뀐다.  플로팅은 격리 venv(`/tmp/fig4a-venv`)를 쓴다.

---

## 3. 이 세션에서 닫힌 것

### 3-1. 이온 8팔 시나리오 1 — σ_ion 을 실은 첫 코호트 (원장 §20)

`r = 0` 에서 **DBE < SBE** (STEP B 단일팔과 방향 일치).  그리고 **부수 소득이 더 크다**:
σ_e 가 `w4_ptfe_centerline_20260827` 과 **16/16 팔 비트 동일**하게 나왔다 — 이온 축 값이
다르고, LEAN 이 다르고, 그 사이 4일치 코드가 움직였는데도.
⇒ ⓐ 공짜 like-for-like 회귀 ⓑ 전자·이온 독립성이 **코호트 규모**로 확인.

### 3-2. 적대 리뷰 R16 · R17 · R18

| | 무엇 | 결과 |
|---|---|---|
| R16 | 하루치 판단 6개 채점 | 판정기 구멍·차단 규약·시트 정정 (`02c351cf`, `37a780e3`) |
| R17 | 이온 절대값을 생산 규약 하나로 확정해도 되는가 | **P1 2건** — 판정기가 공용 계약을 우회 (`df7f1ef3`).  해제조건 2개 미해결 (§6) |
| R18 | PTFE 표면 피복 연산자 둘 (구현 **전** 검증) | **A·B 둘 다 기각.**  내 근거 3개가 원자료 대조에서 틀렸다 — 판정 원문 `codex_r18_verdict_20260831.md` |

★ R18 의 교훈 하나는 규율로 남았다 — **±5 % 는 허용 창(tolerance window)이지 측정
불확실도가 아니다.**  둘을 섞으면 브래킷이 없는 곳에 브래킷이 생긴다.

### 3-3. Fig 4a 라벨 사슬 — 뷰어에서 캡션까지

뷰어 콜러바가 **철회된 "접점" 해석**을 그대로 찍고 있었다.  그림에 박히면 되돌릴 수 없는
자리라 끝까지 고쳤다:

- 제목 `Carbon point density near AM` → **`Conductive-additive density near AM`**
  (SDCP 는 탄소가 아니다) + `NOT a contact count` 명시
- 비교 뷰는 **정규화 기준을 일반화** — `normalized to <낮은 쪽> median` 을 자동으로 고른다
  (우리 원고는 SBE 지만 다른 조합도 나오므로)
- 눈금은 정규화된 **정량 수치** (low/high 라벨 아님)
- 밴드 정의(0.3 µm, center)는 캡션 소관으로 넘김 — 그림 안에 안 적는다
- 철자 **미국식** (`Color`, `center`)
- `scripts/check_colorbar_fit.mjs` 에 가드 4개 추가.  ⚠ 그 가드가 **자기 회귀를 잡았다**
  (템플릿 리터럴이 홑따옴표 정규식을 빠져나갔다) → 정규식이 두 따옴표 형태를 다 본다

### 3-4. 접점 분포 — 원자료 + 그림

`scripts/cbd_contacts_per_am.py` (전수 6,790만 점, 개체 단위, AM 표면 **바깥** 껍질).
원자료 `docs/data/cbd_contacts_20260831/contacts_{SBE,DBE}_band015.json` (AM 1,271개 전수 분포).
그림 `scripts/plot_cbd_contacts.py` → `docs/figures/cbd_contacts_box.{png,svg,csv}`
(`--horizontal --no-violin` = 사용자 Origin 판에 violin 이 없어서 상자 전용).

### 3-5. σ_e 막대 그림 (Fig 4b)

`scripts/plot_sigma_e_bars.py` — **payload 에서 재계산**한다 (문서의 자기 신고를 읽지 않는다).
→ `docs/figures/sigma_e_bars.{png,svg,csv}`.

### 3-6. 축소기 진단 모드

`reduce_arm_payloads.py --diagnostic` — ARMS<8 런의 provenance 를 **표지와 함께** 반입한다
(트리 sentinel + payload 내 키 2중).  코호트 판정기는 그 표지를 보면 `DIAGNOSTIC_TREE` 로
**HOLD** 한다.  축소 직후 자기 검증까지 한다 — *축소본에 코호트 판정기를 돌려 거부되지
않으면 실패*.  ⇒ 진단 런이 실수로 코호트 값으로 쓰이는 경로가 막혔다.

### 3-7. 원고 편집 시트 (`ms_si_v6_edit_sheet_20260831.md`)

- §H — 리포가 **두 보고 형식을 동시에** 말하고 있었다 (저자 결정 필요 항목)
- §I — Abstract 문장별 판독.  ★ **소유자 분리 확정: 저자 담당은 모델 절뿐이다**
- §J — Table S2 실물 판독: ρ_SDCP 부재 · σ_SE 기준 불일치.  ★ **재실행 없이 정확히 환산된다**
- §K — PTFE 차단 축의 **최대 문안 고정** + §K-4 **저자 결정 = 언급하지 않는다**

---

## 4. 확정 수치 (인용 가능 — ban sweep 통과)

**σ_e** (구 스탬프 · centerline 규약 · 8 origin factorial, 쌍대응 산술평균):

```
SBE 53.99 mS/cm  (팔 폭 53.62 – 54.53,  1.70 %)
DBE 70.61 mS/cm  (팔 폭 70.04 – 71.40,  1.33 %)
비  1.307820     (쌍대응 산포 0.0805 % · 비대응 0.3027 %)
arm0  SBE 0.054530439566226836 S/cm · DBE 0.0714004401030127 S/cm
```

⚠ **보고 단위는 비다.** origin 이 움직이면 두 침대가 함께 움직여서 비의 산포가 절대값의
**1/20** 이다.  ⚠ 8 위상은 한 침대의 완전 `{0,½}³` factorial이라 **복제 자유도 0** —
표준오차·신뢰구간으로 부르지 않는다 (R8 Q1).  산포와 관측 범위만 적는다.

**AM 입자당 도전재 접점** (0.15 µm 껍질 · 개체 단위 · VGCF+SDCP · PTFE 제외):

```
중앙값 74 → 86 (+16.2 %)     평균 74.34 → 85.65
p10–p90  61–88 → 71–100      최소–최대 42–106 → 55–118
접점 0 인 AM = 0 / 1,271 (양 침대)
```

⚠⚠ **밴드를 반드시 같이 적는다** — 0.30 µm 면 `89 → 112 (+25.8 %)` 로 1.6배 커진다.
⚠ 중앙값 %(+16.2)와 평균 %(+15.2)를 **섞지 않는다**.  원장 정본은 중앙값이다.

**σ_ion** (시나리오 1, `SIGMA_ION_SDCP = 0`):

```
SBE 0.5503 – 0.5534 mS/cm      DBE 0.5380 – 0.5410 mS/cm
```

**침대 조성** (양 침대 공통 VGCF 1,643,483 물질점):
PTFE 235,046 → 115,555 · SDCP 0 → 138,988 · 전극 두께 L = 72.534 µm.

**문헌 앵커**: 34 mS/cm (Lee 2025) · 38.6–65.2 (Kim 2024).

---

## 5. 하면 안 되는 것 (전부 유효)

1. **결과를 보고 사전등록 문턱·창을 바꾸지 않는다** (prereg §7).  PTFE 규약 판정
   *"채택 안 함"* 은 그대로다 — 본문이 centerline 을 쓰는 것은 **편집 결정**이지 판정
   번복이 아니다.
2. **금지 표현 6개** — `docs/reviews/ptfe_convention_prereg_20260829.md` 의 §이후결정에 원문이 있다.
   요지: *부피를 더 그려서 / 실험에 더 가까워서 / 더 현실적이라서* 골랐다고 **쓰지 않는다**.
3. **`quotation_ban` 값을 인용하지 않는다** — 정본은 `docs/reviews/claims.json` 의
   `quotation_ban`.  **어떤 파생 문서에도 그 목록을 베껴 적지 않는다** (이 문서 포함).
   `bash scripts/check_all.sh` 가 잡는다.
4. **검사기가 대상의 자기 신고를 읽게 하지 않는다** — 반드시 원자료에서 재계산.
5. **LHS 확장을 `ibb` 에 제출하지 않는다.**
6. **litdb 를 이 브랜치에서 검색하지 않는다** — 여기는 65장 동결본.  정본은 202장,
   `origin/claude/friendly-meitner-lldvar`.
7. **kgy 에서 `git pull` 하지 않는다** — `git fetch` + 일회용 `/tmp` 클론.
8. **커밋·푸시는 `manuscript-track` 에만.  PR 만들지 않는다.**
9. **런 도중 `~/dem-mt` 워크트리 금지** (§2).
10. **kgy `dem-venv` 에 pip install 금지** (§2).
11. `git fetch --depth` 금지.
12. **유럽식(영국식) 철자 금지** — `colour`→`color`, `centre`→`center`.

작업 규율: 원격은 *"붙여넣기 블록 제공 → 사용자 실행 → 출력 회수"* · **경고를 명령 블록
앞에** 쓴다 · 새 스크립트 전에 `scripts/` 를 먼저 찾는다 · 새 도구엔 `--selftest` + 음성
경로 · 커밋 전 `bash scripts/check_all.sh` (**파이프 금지**, 래퍼 종료코드 말고 **로그
마지막 줄**을 읽는다) · 작업 단위마다 커밋·푸시.

---

## 6. 남은 것 (우선순위)

1. **이온 8팔 시나리오 2·3·4 회수** (§2).  전 시나리오 완주 후 `ion_8arm_prereg` 판정.
2. **웹앱 비교뷰 PNG 재export** — 새 콜러바 확인 + 패널 라벨 `A · SBE arm0` → `SBE` / `DBE`.
3. **R17 해제조건 2개** — 0.003 세트의 별도 판정 프로토콜 · W2 `input_digest` 정확 일치.
4. **원고 시트 §H 저자 결정** — 두 보고 형식 중 택1.
5. **§J-5 행동 항목** — Table S2 의 σ_SE 기준·ρ_SDCP 표기.
6. **미해결 원장 11건** (`findings.json` status open/hold) — SR-02/03 · DR3-05/06 ·
   CDXIJ-2 · CDXR2-2/5 · R5CX-09 · SELF-07/10/11.
7. 앞 인계 §5 의 잔여 (OAT prereg 승격 · `post_SE_heckel_300` ⓐ/ⓑ 판별 · 미결 #5/#8/#18).

---

## 7. 도구 메모

- **kgy 헬퍼** (이 세션에서 만듦): `~/w.sh` 진행 감시 · `~/pack.sh <job>` 축소→검증→커밋→푸시 ·
  `~/mt-push` 푸시 자격.  ⚠ 전부 `~/dem-mt` 를 **읽기만** 한다.
- **그림 3종은 전부 원자료에서 재계산한다** (`plot_cbd_contacts` · `plot_sigma_e_bars` ·
  뷰어 export).  문서 숫자를 받아 그리는 경로는 없다 — 규율 4번의 그림판.
- `check_all.sh` 와 `.github/workflows/discipline.yml` 에 두 그림 도구의 selftest 가
  배선돼 있다 (CI 에 `matplotlib` 추가).
- ⚠ `ap.error()` 를 쓰면 메시지가 `SystemExit(2)` 에 먹혀 회귀 검사가 실패한다 —
  **`raise SystemExit(msg)`** 를 쓴다.
