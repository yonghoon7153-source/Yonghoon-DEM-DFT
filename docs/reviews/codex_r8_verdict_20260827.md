# Codex R8 판정 — W4 측정과 그 해석 (2026-08-27)

기준 스냅샷 `manuscript-track @ 381e8b8c`.  요청서 `codex_review_request_r8_20260827.md`
(⚠ 그 문서 헤더의 `0923b20d` 는 낡은 표기 — R8 판정은 `381e8b8c` 전체 상태 기준).

## 총평

**Table S3 는 원고 승격 HOLD.  정본 상태 = `PROVISIONAL_RAW_W4_PENDING`.**

살릴 수 있는 것은 하나: 고정 침대·고정 규약·**8개 사전지정 origin** 에서 관측한
protocol-specific 서술값 **R ≈ 1.30782**.

철회/수정: SE·CI · 물리적 bracket · 절대값 타당성 주장 · 현재 보정 논리.

| Q | 판정 |
|---|---|
| Q1 | **[P1] SE · ± · 95 % CI 철회** |
| Q2 | **[P1] bracket · "둘 다 하한" 철회** |
| Q3 | [P2] 외삽과 절대값 타당성 주장 하향 |
| Q4 | **[P1] DC 동일량 전제와 보정 순서 수정** |
| Q5 | [P2] porosity 는 **라벨 공개**, 공통모드 상쇄 주장 금지 |
| Q6 | 고정 SHA 기준 주장은 사실 · 별도 **[P1] W4 원자료·침대 provenance 부재** |

---

## Q1 — 8팔 SE (수용)

8팔은 같은 침대의 **완전한 {0,½}³ factorial** 이지 독립 복제가 아니다.  완전 factorial 은
7개 비상수 대비가 8점을 **전부 소모**하므로 **복제 기반 오차 자유도가 0** 이다.
⇒ `sd/√8` 은 표준오차가 아니다.

**대체 표기** (Codex 재계산, 우리 값과 일치):
- paired-ratio 평균 **1.307820** · **origin-phase SD 0.002977**
- 관측 범위 **1.301726 – 1.310448** (이득 30.173 – 31.045 %)
- 팔-폭/평균 0.667 %

조치:
- `±0.105 %p` · `95 % CI [30.58, 30.99]` **삭제**
- σ_e 절대값의 `±0.16` · `±0.11` 도 bare ± 대신 **origin-phase SD 또는 범위**
- `n = 8` → **"8 prescribed origin phases"**
- ★ **정본 estimator 를 하나로 고정** — `mean(DBE)/mean(SBE) = 1.307824` vs
  `mean(DBE/SBE) = 1.307820`.  **개정 A1 이 이미 후자(쌍대응 비의 산술평균)를 등록**했으므로
  **1.307820 이 정본**이다.
- 게이트(0.3027 % < 1.17 %)는 버리지 않되 **"동결된 비추론적 origin 일관성 검사"** 로
  개명한다 — 재현성·격자수렴·통계적 정밀도의 증거로 쓰지 않는다.

## Q2 — bracket 과 "둘 다 하한" (수용)

§4 **삭제**.  이유 둘:
1. W4b 미완료 → **첫 항이 측정값이 아니다** (스냅샷 시점에 부등식을 먼저 선언했다).
2. exact-zero 는 얇은 코팅보다 **국소 차단을 과대**할 수도, **공간적 코팅 범위를 과소**할
   수도 있다.  게다가 **각 절대 σ 가 단조로 변해도 비 σ_DBE/σ_SBE 의 방향은 정해지지 않는다.**

"수치적으로 사이에 둔다" 와 "둘 다 하한이다" 가 형식적으로 동시에 참일 수는 있으나,
그 경우 두 모델값은 물리값을 **bracket 하지 않는다**.

⇒ W4b 완료 후에도 **PTFE 표현 민감도의 두 점**으로만 보고한다
(`PTFE-off protocol result` · `centerline exact-zero protocol result`).
실험값이 그 사이에 있어도 **numerical straddling** 이지 물리적 상·하한이 아니다.

## Q3 — 문헌 대조 (수용)

- Kim 80/85/90 을 70.3 까지 외삽할 정당성 없음.  **직선 적합조차 70.3 에서 ≈13.8** 이라
  문서의 "20급" 도 유일 도출값이 아니다.  ⇒ **"조성을 맞추면 우리가 높다" 는 결론이 아니라 가설.**
- **`physically reasonable absolute magnitudes and not merely relative trends` 삭제** —
  솔버 자신의 신뢰 계약이 *"절대값은 contact-area cross-calibration 전에는 신뢰하지 말라"* 다.
- 유지 가능: **거친 scale comparison ("여러 자릿수 떨어져 있지 않다")** 뿐.
- ★★ **내부 모순 지적 (우리가 못 본 것)** — §5 는 "네 편향이 **모두 σ_e 를 올린다**" 고
  적고 §6 은 "**격자 축에서 현재 값은 하한**" 이라고 적는다.  현재 값이 격자 하한이면
  격자 미수렴은 **높은 값을 설명하는 항목이 아니다.**  ⇒ 편향 목록에서 격자를 빼거나
  절대값에 대한 방향이 **미측정**임을 명시해야 한다.

## Q4 — DC 관측량과 σ_VGCF 보정 (수용)

**Q4-a** — 같은 **수송 모드**이지만 같은 **관측량**은 아니다.  코드는 인접 셀 사이에
bulk σ 의 harmonic-mean 저항만 두고 **AM–AM · AM–탄소 · 탄소–탄소 excess contact
resistance 도, 집전체 접촉저항도 두지 않는다.**  Lee 의 two-terminal DCP 는 `R = V/I`,
`σ = L/(RA)` 로 환산하며 계면 de-embedding 이 기술돼 있지 않다.
⇒ 정확한 표현 = **"같은 수송 모드의 idealized bulk-model counterpart"**.
⇒ AM–AM · AM–탄소 접촉저항은 **dedicated term 이 없다**.  σ_VGCF 를 맞추면 그 결손 일부를
**수치적으로 흡수**할 수는 있으나 **섬유–섬유 접촉만의 물리 파라미터로 식별할 수 없다.**

**Q4-b** — 같은 조성은 **필요조건일 뿐 충분조건이 아니다**.  추가로 압밀압 · 밀도/공극률 ·
두께 · 온도 · 탄소 형상과 분산 · 집전체 경계/접촉 처리를 맞춰야 한다.  한 scalar 로 두
전극의 두 절대 target 을 동시에 맞출 수 있다는 보장도 없다.
⚠ **우리 문장이 너무 강했다** — *"PTFE 비대칭은 shared σ_VGCF 로 **원리적으로** 못 고친다"*
는 과하다.  같은 scalar 라도 **두 topology 의 민감도가 달라 비는 움직인다.**
정확한 서술 = **"PTFE-specific bias 를 인과적으로 교정하거나 식별할 수 없다."**

**Q4-c** — ③→④ 순서를 **뒤집어야 한다**:
1. 같은 조건의 anchor 와 calibration observable · σ 범위를 **사전 고정**
2. 그 **전체 후보 범위**에서 절대 σ 와 ratio 민감도를 **보정 전에** 측정
3. 한 조건으로 calibration
4. **사용하지 않은** 구조·조건으로 **holdout validation**

CL-39 의 `dR/dlnσ = −0.0099` 는 **옛 geometry 의 좁은 ×1.44 국소 결과**라 W4 나 더 큰
보정 범위의 불변성을 보증하지 않는다.  holdout 이 없으면 최종 표기는 **`calibrated`,
`validated` 가 아니다**.

## Q5 — porosity 와 두께 (수용)

**침묵 삭제보다 라벨 공개.**
- 7.86 / 7.37 % = conventional electrode porosity 가 아니라 **ε_union —
  simulation-geometry diagnostic** 으로 SI/방법·한계 절에 공개
- D4 의 `ε_sphere` 는 새 침대에서 별도 계산할 때까지 **pending**
- 72.53 µm = **terminal wall separation under the kinematic stopping rule** (두 침대 공통)

⚠ **우리 문장 둘이 과했다**:
1. *"MPM 이 두 침대를 기계적으로 구분하지 못했다"* → 실제 W2 기록은 **상별 변위와
   point cloud 가 달라졌음**을 보여 준다.  옳은 서술 = *"현재 정지 규약에서 terminal
   thickness 가 조성 판별량이 아니었다."*
2. *"과압축이 비에서 공통모드로 상쇄된다"* → 같은 속도·정지 위치는 **like-for-like 입력을
   보장할 뿐**이다.  R = 1.3078 은 **현 과압축 protocol 안의 contrast** 이지 과압축이
   제거된 실험 ratio 의 추정치가 아니다.

## Q6 — 재현 주장 (사실 확인 + 신규 [P1])

고정 SHA 기준 우리 주장은 **사실**: `manuscript-track @ c2f5b047` 에는 PTFE_STAMP 경로가
있고 `claude/stoic-knuth-NObVQ @ ce2f318f` 의 러너·payload·verdict 에는 PTFE stamp 및 관련
manifest 필드가 **없다**.  ⇒ *"stoic-knuth @ ce2f318f 의 sealed runner–payload–verdict
경로로는 W4 를 그대로 replay 할 수 없으며 backport 가 필요함"* 으로 적되 **반드시 SHA 병기**.
원고에는 브랜치 비교보다 **실행 SHA · 필수 옵션 · 계약 필드**를 기록한다.

★★ **더 큰 문제 (신규 [P1])** — `381e8b8c` 의 tracked run data 에 **W4 centerline 8팔
JSON/receipt 가 없고**, Table S3 에 **`input_digest` 가 없다**.  `latest_run` 근접 사고와
결합하면 **실제로 08-27 W2 침대를 읽었는지 대조할 수 없다.**

**종료조건**:
- W4 16개 arm payload/JSON 과 verdict receipt **커밋**
- 선택된 SBE/DBE run ID·경로 기록
- W2 기대 digest 와 **모든 팔의 `input_digest` 대조**
- code SHA · protocol ID · origin pairing 보존

그전까지 **`PROVISIONAL_RAW_W4_PENDING` · 원고 승격 HOLD**.

---

## 처분

| 항목 | 조치 | 상태 |
|---|---|---|
| Q1 SE/CI 철회 · SD/범위로 교체 | `table_s3_data_20260827.md` §2 | 적용 |
| Q1 정본 estimator = 1.307820 (개정 A1) | §2 | 적용 |
| Q2 §4 bracket 삭제 → 두 protocol 점 | §4 | 적용 |
| Q3 절대값 타당성 문장 삭제 · 외삽을 가설로 | §5 | 적용 |
| Q3 격자↔하한 내부 모순 해소 | §5·§6 | 적용 |
| Q4 "같은 관측량" → "idealized bulk-model counterpart" | §8 | 적용 |
| Q4 비대칭 문장 약화 · 보정 순서 재배열 | §8 | 적용 |
| Q5 porosity 라벨 공개 · 두 과한 문장 수정 | §1 | 적용 |
| Q6 SHA 병기 | §7 | 적용 |
| **Q6 W4 원자료 커밋** | kgy → 리포 | **미착수 (사용자 실행 필요)** |
| R8 요청서 헤더 커밋 표기 정정 | 요청서 | 적용 |
