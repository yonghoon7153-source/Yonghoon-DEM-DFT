# 인계 — `claude/sdcp-dem-manuscript-si-pqwtv8` → `claude/stoic-knuth-NObVQ` 병합

**작성** 2026-09-15 · **작성 세션** sdcp-dem-manuscript-si 브랜치
**대상 독자** origin(stoic-knuth) 쪽에서 병합을 수행·검증할 세션

---

## 0. 한 줄

이 브랜치는 `origin/claude/stoic-knuth-NObVQ`(`be0ae9568`)를 **완전히 포함**한다.
**fast-forward 다 — 충돌이 원리적으로 없다.**  그러나 *"충돌이 없다"* 와 *"검증됐다"* 는
전혀 다른 말이고, 아래 §5 가 그 차이를 다룬다.

---

## 1. 브랜치 기하 (실측, 2026-09-15)

| 브랜치 | 원격 SHA | merge-base | 우리가 앞선 | 저쪽이 앞선 | 병합 형태 |
|---|---|---|---:|---:|---|
| `claude/stoic-knuth-NObVQ` | `be0ae9568` | `be0ae9568` | **142** | **0** | ✅ fast-forward |
| `manuscript-track` | `f70446c5f` | `f70446c5f` | **219** | **0** | ✅ fast-forward |
| `claude/dft-script-generator-webapp-GPSAG` (리포 기본) | `3fe789ff6` | `bf0dd1a32` | 2,859 | **16** | ⛔ **계보가 다르다** |

우리 HEAD = `984874f8d`.

⚠ **리포의 GitHub 기본 브랜치는 `claude/dft-script-generator-webapp-GPSAG` 인데 그것은 이
작업 계보가 아니다** (우리 기준으로 2,859 앞서고 16 뒤진다).  `CLAUDE.md` 가 *"Working
branch: `claude/stoic-knuth-NObVQ`"* 라고 적고 있고 실측 기하도 그와 일치한다.
⇒ **PR 을 열 때 base 를 기본 브랜치로 두면 안 된다.**  base = `claude/stoic-knuth-NObVQ`.

⚠ `litdb/` 는 이 브랜치에서 **2026-07-16 동결 스냅샷**이다.  정본은
`origin/claude/friendly-meitner-lldvar`(`634da438b`).  **병합이 litdb 정본을 건드리지
않는지 확인할 것** (`git diff --stat be0ae9568..984874f8d -- litdb/` 가 비어야 한다).

---

## 2. 변경 규모

```
133 files changed, 32,310 insertions(+), 196 deletions(-)
날짜 범위 2026-08-26 … 2026-09-14 · 커밋 142
```

**삭제가 196 줄뿐**이라는 것이 중요하다 — 거의 전부 **추가**다 (새 스크립트·새 문서·새
원자료).  기존 생산 경로를 덮어쓴 것이 적어서 fast-forward 가 안전한 구조적 이유다.
그래도 §5 의 확인은 해야 한다.

디렉터리별 (상위):

| 파일 수 | 추가 줄 | 자리 |
|---:|---:|---|
| 52 | +8,728 | `docs/data/` (원자료·코호트·수확) |
| 6 | +1,261 | `dem_scripts/ps_sweep_6mah_20260914/` (P:S 스윕 덱 5 + README) |
| 1 | +927 | `scripts/audit_constriction_deleted.py` |
| 1 | +822 | `docs/area_contract_20260913.md` |
| 1 | +795 | `scripts/lhs_descriptor_harvest.py` |
| 1 | +777 | `docs/session_20260911_progress.md` |
| 1 | +618 | `scripts/make_ps_sweep_decks.py` |
| 1 | +504 | `scripts/measure_rho.py` |
| 1 | +464 | `scripts/seal_area_cohort.py` |
| 1 | +435 | `scripts/constriction_reference.py` |
| 1 | +423 | `scripts/phase_a_arms_from_payload.py` |
| 1 | +382 | `scripts/check_audit_adjudication.py` |
| 1 | +344 | `scripts/audit_transport_cap_equivalence.py` |

---

## 3. 142 커밋의 작업줄기 여덟

| 커밋 | 줄기 | 무엇 |
|---:|---|---|
| 30 | **면적 계약 · 봉인 (AREA / S3)** | 협착저항 ψ 규약, `docs/area_contract_20260913.md`, 코호트 봉인 도구(`seal_area_cohort.py`·`seal_s3_prerun.py`), S3 런 **전** 사전등록 |
| 16 | **적대리뷰 판정문 L1~L5** | 접촉면적·솔버·스케일링·등급·ML 다섯 층의 외부 판정 등재 및 수리 |
| 15 | **Phase A 팔 캠페인** | V100 만료로 잃은 STEP2 재생성, 양 끝(W1·W4) 재현, `pa_arms_watch.sh`, `phase_a_arms_from_payload.py` |
| 14 | **자기감사 SELF** | 내 검사기 자신의 사각지대(false-green) 적발 — `SELF-28~32` 포함 |
| 12 | **Codex 라운드 R2~R5** | 외부 적대리뷰 4라운드 요청서·판정문 보존·수리 |
| 11 | **LHS 코호트 · 디스크립터** | `lhs_descriptor_harvest.py`, `docs/lhs130_harvest_contract_20260913.md`, `measure_rho.py` |
| 5 | **원장 · 규율 · CI** | `check_all.sh` 확장, `quotation_ban` 스윕, 판정 자기일관 검사 |
| 4 | **P:S 스윕 덱 (PS-01)** | `make_ps_sweep_decks.py` + 6 mAh 덱 5개 — **이번 세션의 사고, §4** |
| 35 | (기타) | 원장 갱신·세션 진행기록·소규모 수리 |

---

## 4. 이번 세션(09-14~15)이 새로 넣은 것 — `PS-01`

P:S 스윕 덱 5개가 **입자를 0개 삽입하고 죽었다.**  원인이 **둘**이었고 둘 다 실측으로
확정했다.  정본은 원장 `PS-01` 과 `dem_scripts/ps_sweep_6mah_20260914/README.md` §4-보 · §4-보-2.

### 원인 ① `maxattempt` 는 입자당이 아니라 **삽입 전체의 시도 예산**

원본 덱의 15,000 으로 159,167 개를 요청하면 입자당 0.094 회다.  실측:

| maxattempt | 요청 | 삽입 | |
|---:|---:|---:|---|
| 15,000 | 159,167 | **0** | ⛔ |
| 15,000 | 100 | 100 | ✓ (기계는 멀쩡하다) |
| 200,000 | 159,167 | **159,167** | ✓ |

### 원인 ② **MPI 분해 축** — z 분할이면 삽입 영역이 한 proc 에만 걸린다

박스가 0.05 × 0.05 × **1.01 m** 로 z 로 길어 LIGGGHTS 가 `1 by 1 by P` 로 쪼갠다.
삽입 영역은 z 0.005–0.30 이라 한 proc 에만 걸리고 나머지가 전부 실패한다.
`processors * * 1` 로 x·y 분할을 강제하면 해결된다.

| np | 격자 | maxattempt | 삽입 (요청 159,167) | |
|---:|---|---:|---:|---|
| 1 | — | 200,000 | **159,167** | ✓ 경고 없음 |
| **2** | `2 by 1 by 1` | 400,000 | **159,167** | ✓ **생산 규약 · 실배치 확인** |
| 2 | `1 by 1 by 2` | 400,000 | 0 | ⛔ |
| 4 | `2 by 2 by 1` | 400,000 | 0 | ⛔ |
| 4 | `2 by 2 by 1` | 4,000,000 | 119,679 | ⛔ |
| 10 | `5 by 2 by 1` | 400,000 | 142,965 | ⛔ |
| 10 | `5 by 2 by 1` | 4,000,000 | 16,202 | ⛔ |

### ⚠⚠ 기전을 모른다 — 알아야 할 한정

- 예산에도 랭크에도 **단조롭지 않다**.  예산을 10배 올리면 np=4 는 0 → 119,679 로 **늘고**
  np=10 은 142,965 → 16,202 로 **줄었다**.
- `16,202` 가 마침 `159,167 − 142,965` 와 **정확히 같은 것**도 설명하지 못한다.
- np=10 의 x 폭 0.01 m ≈ AM_P 지름 0.009 m 는 부분 원인일 수 있으나, np=4 (0.025 m =
  충분히 넓다)가 0 인 것은 그것으로 설명되지 않는다.

⇒ **기전 대신 관측을 규약으로 썼다**: `np ∈ {1, 2}` 만 정확한 개수를 냈다.

⛔ **부분 삽입 런은 전량 폐기한다.**  10 % 빠진 침대는 조성이 다른 **다른 물건**이다.

### 생성기에 박은 강제 (selftest 50 → **61 PASS**)

- `--maxattempt` 노브 + 기본값 = 예상 입자수 × 3 (하한 200,000)
- **방출 게이트** — `maxattempt < 1.2 × 예상 입자수` 면 `sys.exit`, 덱을 안 내보낸다
- `processors * * 1` 을 `region reg_box` 앞에 삽입 (멱등)
- **`--mpi > 2` 거부** (`--allow-unverified-mpi` 로만 강행)
- 헤더가 *"원본과 다르다"* 를 적는다 — `volumefraction … 전부 불변` 이 거짓이 되지 않게

⛔ **금지선 1.2 는 증거 기반 하한이지 충분 조건이 아니다.**  아는 점은 둘뿐 —
0.094배 실패 · 1.2566배 성공.  참 문턱은 **모른다**.

### ⬜ PS-01 에 남은 것 (원장 note 에도 있다)

1. **빌드가 다르다** — 원본 `real_4` 는 같은 `maxattempt 15000` 으로 완주한 실측 scaffold 가
   `docs/data/phase_a_6mah/precompute.json` 에 있는데, 지금 빌드(`LIGGGHTS-PUBLIC 3.8.0`,
   2026-03-26, git `3d5c00f2`)에선 0 이 된다.  침대 비교를 막지는 않지만 *"원본과 같은
   조건"* 이라고 쓰려면 확인이 필요하다.
2. **나머지 4덱(`7:3`·`5:5`·`3:7`·`0:10`)은 아직 한 번도 완주하지 않았다** (§6).

---

## 5. 병합 전에 **반드시** 할 것

fast-forward 라는 사실은 *"git 이 자동으로 붙는다"* 는 뜻일 뿐이다.  아래는 붙은 뒤에
리포가 **자기일관한가**를 보는 검사이고, 이 리포에서 그것은 자동이 아니다.

### ① 커밋 전 게이트 — 이것을 건너뛰면 남의 GPU 런이 선다

```bash
bash scripts/check_all.sh          # 인자 없이 = 리포가 맞나
```

`CLAUDE.md` 규율: **`--selftest` 는 "검사기가 맞나", 인자 없는 실행은 "리포가 맞나"** 를
본다.  둘은 서로를 대신하지 않는다.  같은 실수를 두 번 했고(철회값 인용 · 원장의 잘못된
`kind`), 둘 다 selftest 는 초록이었고 CI 가 60 초 뒤 빨간불을 냈다.  두 번째는 러너의
fail-closed 게이트라 **사용자의 GPU 런을 막았다**.

⚠ **`check_all.sh | tail` 처럼 파이프로 받지 말 것** — 종료코드가 삼켜진다.  이 세션이
정확히 그래서 빨간 게이트를 두 번 연속 밀었다 (원장 `SELF-29`).

### ② CI 가 같은 것을 돈다

`.github/workflows/discipline.yml` — push/PR 마다.  ⚠ `fetch-depth: 0` 필수 (검사기가
SHA 실재를 본다).

### ③ 원장 자기일관

`scripts/check_review_findings.py` 가 `docs/reviews/findings.json` 의 `claimed_fixed_sha`
가 **실재하는 커밋**인지 본다.  **fast-forward 면 SHA 가 그대로 살아 있으므로 통과해야
정상이다** — 빨간불이 나면 병합이 아니라 다른 문제다.

### ④ 인용 금지 스윕

`check_review_findings.py --ban-sweep` 이 `docs/reviews/claims.json` 의 `quotation_ban`
등록부로 `CLAUDE.md`·`docs/`·`wiki/`·`webapp/`·덱생성기를 훑어 **표지 없는 철회값**을
오류로 낸다.  pptx 도 읽는다 (zip + run 이어붙이기 + 발표순서).

### ⑤ litdb 정본 무침범

```bash
git diff --stat be0ae9568..984874f8d -- litdb/    # 비어야 한다
```

---

## 6. 병합과 **무관하게** 지금 밖에서 돌고 있는 것

⚠ 이것들은 **리포에 없다** — ibb 클러스터(`166.104.39.171:43612`, 사용자 계정)에서 돈다.
병합이 이것을 기다릴 필요는 없지만, **결과가 나오면 리포에 등재해야** 한다.

| 배치 | 상태 (09-15 00:40) |
|---|---|
| `lhs00_` | 109 중 106 완주 · 3 실행 |
| `lhsx_` | 64 중 50 완주 · 14 실행 (남은 시간 약 3일 21시간) |
| `ps_` | 5 중 **1 실행**(`ps_10_0_r45`) · 4 대기 |

`ps_10_0_r45` 는 삽입 **159,167 · `Less insertions` 경고 없음** 으로 예측치와 정확히
일치했다 (np=2).  나머지 4덱은 코어 대기 중.

⛔ **각 덱이 끝날 때마다 검산 의무**가 있다 (기전을 모르므로):

```bash
grep -E "inserted [0-9]+ particle|Less insertions" <케이스>/log.liggghts
```

예상 총수 — `10:0` 159,167 · `7:3` 160,422 · `5:5` 161,258 · `3:7` 162,095 · `0:10` 163,349.
**경고가 있거나 개수가 다르면 그 런은 폐기**한다.

---

## 7. 원장 상태 — 여기가 진짜 남은 일이다

`docs/reviews/findings.json` **252건**:

| 상태 | 수 | 뜻 |
|---|---:|---|
| `open` | **99** | 미해결 |
| `claimed_fixed` | 141 | **내가 고쳤다고 주장**했고 독립 검증은 안 됐다 |
| `verified` | **8** | 독립 검증됨 |
| `wontfix` | 4 | |

⚠⚠ **`claimed_fixed` 141 vs `verified` 8 이 이 리포의 가장 큰 미결이다.**  고쳤다는 주장이
검증된 것의 **17배**다.  origin 쪽에서 이 브랜치를 받는다는 것은 그 141건의 주장을 함께
받는다는 뜻이다.

### `open` 99건 중 P1 (발췌 — 전수는 원장을 볼 것)

- **접촉·면적 층 (`L1-*`, `SELF-28`, `AREA-*`)** — `L1-01` 하한>상한이어도 정상 면적을 낸다 ·
  `L1-02` `V_overlap` 이 구 교집합이 아니다(깊으면 **음수**) · `L1-03` 상 쌍 인자가 없다 ·
  `SELF-28` `geom` cap 이 결속하면 ψ=0 이 되어 협착저항이 **삭제**된다 ·
  `AREA-12` S2 는 솔버에 대해 **항등 변환**이다
- **솔버 층 (`L2-*`)** — `L2-01` ψ 가 분모에 있다(문헌은 곱한다) · `L2-02` 정상 미퍼콜을
  양의 fallback 으로 **복원**한다 · `L2-04` 벽에 안 닿는 사슬을 **관통으로 판정** ·
  `L2-05` 막다른 가지 하나가 σ 를 4 % 바꾼다
- **스케일링 층 (`L3-*`)** — `L3-01` 정상 Stage-E 0 을 raw 양수로 **대체** ·
  `L3-02` 이온 T1 의 AM power gate 가 주 생산 호출에 **전달되지 않는다**
- **등급·ML 층 (`L4-*`·`L5-*`)** — `L4-01` 정상 미전도를 0 Ω 처럼 취급 ·
  `L5-01` σ 를 y 에서 빼도 σ 로 코호트를 **선별**한다
- **Phase A (`PA12-*`)** — receipt 만 보고 payload 와 대조 안 함 · origin 이 등록 집합인지
  검사 안 함 · 음성대조 ⑨ 가 **장식**이었다(퇴행시켜도 15/15 초록)
- **디스크립터 (`DESC-*`)** — τ 실패가 기하량까지 삼킴 · τ 가 관통을 보증하지 않음 ·
  Physics 피복률이 확대/미확대 길이를 혼용
- **문헌·앵커 (`R20-*`, `AUD-*`)** — Bazzoun digest **100배 단위 오류**가 논거를 떠받침 ·
  예측기 탄소 앵커가 **리포에 없는 논문**을 인용

---

## 8. origin 세션이 지켜야 할 규율 (이 리포 고유)

`CLAUDE.md` 가 정본이고 충돌 시 그것이 이긴다.  특히:

1. **철회값 인용 금지** — `claims.json` `quotation_ban` 등록부가 강제한다.  `+52.0 %`,
   `+42.15 %`, `f_artifact = 0.147`, `×35.79` 등.  **반올림한 형태로 다시 적는 것도 금지**
   (잘린 표기는 패턴에 안 걸려 스윕이 **거짓 초록**을 낸다 — 실제로 그런 사고가 있었다).
2. **수치를 철회하는 커밋은 같은 커밋에서 원장·파생 문서를 고친다** (규율 ④).
3. **고치기 전에 재현 테스트 먼저** (규율 ②).
4. **코드 쓰기 전 사다리** — 필요한가 → **이 리포에 이미 있나** → stdlib → 기존 의존 (규율 ①).
5. **부분집합 필터로 훑으면 조용히 초록이 된다** (규율 ⑤) — *"후보를 고르는 코드가 곧
   사각지대"*.
6. 커밋·PR·코드주석에 **모델 식별자를 넣지 않는다**.

---

## 9. 권장 절차

```bash
git fetch origin claude/stoic-knuth-NObVQ claude/sdcp-dem-manuscript-si-pqwtv8
git merge-base --is-ancestor origin/claude/stoic-knuth-NObVQ \
                             origin/claude/sdcp-dem-manuscript-si-pqwtv8 \
  && echo "fast-forward 확인"

git checkout claude/stoic-knuth-NObVQ
git merge --ff-only origin/claude/sdcp-dem-manuscript-si-pqwtv8

bash scripts/check_all.sh          # ⚠ 파이프로 받지 말 것
python3 scripts/make_ps_sweep_decks.py --selftest      # 61 PASS 여야 한다
git diff --stat be0ae9568..HEAD -- litdb/              # 비어야 한다
```

`--ff-only` 를 쓰는 이유: 만에 하나 기하가 바뀌었으면 **조용히 merge 커밋을 만들지 말고
멈추라**는 뜻이다.
