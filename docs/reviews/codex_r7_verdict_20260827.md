# Codex R7 판정 — **B 트랙 `CALIB_VALIDATED` 철회** (2026-08-27)

> 대상 스냅샷: `934265e5` (R7 요청서가 실제 공개된 커밋).  요청서 = `codex_review_request_r7_20260827.md`.
> **전부 수용했다.**  아래는 판정 요지와 이 리포에 반영한 커밋의 대응표다.
> ⚠ 이 문서는 리뷰 원문의 **요지 보존본**이다 — 정본 처분은 각 대상 문서에 반영돼 있다.

## 0. 결론

> **B 트랙의 `CALIB_VALIDATED` 는 철회해야 한다.  Q1 은 (c), 다만 (b) 에 매우 가깝다.**
> F_e ≡ F_ion 은 구조적 항등식이 맞지만, 외부 전자 실험값이 공유 차단 가정을 반증할
> 가능성은 남는다.  그러나 **PDE/RVE 가 독립적인 예측 정보를 보탠 것은 아니다.**

## 1. P1 findings (판정에 걸리는 것)

| # | 지적 | 처분 |
|---|---|---|
| P1-1 | `CALIB_VALIDATED` 는 과학적 의미가 과하다.  T1 = 공유 감쇠 가정의 **약한 외부 일관성 검사** · T2 = 래스터 가짜연결 **음성대조** · T3 = 전도도 **단조성 검사**.  반면 ⑥ 은 **실제 모델급 기각**인데 판정 밖으로 밀렸다 | ✅ `CALIB_FROZEN_WITH_REPRESENTATION_FAILURE` 로 교체 (freeze §4c) |
| P1-2 | ② 의 0.17 µm 는 **사후 규칙**.  탐색적 engineering convention 으로 동결은 가능하나 **사전등록된 confirmatory calibration 으로 부를 수 없다** | ✅ 0.12 와 병기 · `post-hoc log-nearest nominal` 로 격하 (freeze §3) |
| P1-3 | **B 원자료가 검토 스냅샷에 없다** — JSON 이 kgy 로컬이고 표의 수치는 stdout 전사.  ③ 의 2.8655, T1 네 시드값을 독립 대조할 수 없다.  `check_all`·65 돌연변이·펠릿 selftest 는 **측정기·게이트**를 검증할 뿐 그 과학 런의 원자료를 재현하지 않는다 | ✅ `EVIDENCE: PROVISIONAL_RAW_JSON_PENDING` 등재.  ⬜ **JSON 이 리포에 들어와야 해소** (kgy 푸시 자격증명) |
| P1-4 | Q5 의 p1 값과 Q6 의 미완성 통계 규약이 각각 **원고와 A 판정을 막는다** | ✅ 금요일 문서에서 p1 값 격리 (week plan §4) · ✅ A 통계 개정 A1 등록 (unblinding 전) |

## 2. Q1 — T1 은 무엇인가: **(c), 매우 (b) 에 가까움**

Codex 의 증명 (요지): T1 조건에서 도체는 SE 하나뿐이고 PTFE·`sid 9` 가 양망 0 이므로
어떤 양수 `c` 에 대해 `σ_e(x) = c·σ_ion(x)` 다.  면 conductance·행렬·우변이 모두 `c` 배 ⇒
`L_e = c·L_ion`, `b_e = c·b_ion` ⇒ **`φ_e = φ_ion`**.  전류와 σ_eff 는 `c` 배지만 매트릭스
전도도도 `c` 배이므로 **formation factor 가 정확히 같다**: `F_e = F_ion`.

⇒ T1 은 **RVE 의 독립 전자 예측 검정이 아니라**, *"이온에서 얻은 동일 공간 차단율을
전자에도 써도 되는가"* 라는 **매우 넓은 외부 일관성 검사**다.
★ 완전한 (b) 가 아닌 이유: 외부 전자 감쇠비가 크게 벌어졌다면 공유-mask 가정이 기각돼
`BLOCKING_NOT_TRANSFERABLE` 이 가능했다.  실험의 0.272 ↔ 0.400 이 ×3 안에 들어와 통과했다.

**T2**: 비겹침 RSA 에서는 실접촉이 거의 없으므로 PASS 는 주로 *"복셀 인접이 가짜
z-spanning 을 만들지 않았다"* 는 QA.
**T3**: PTFE 셀을 0 으로 만들면 감소하고 σ_SDCP 를 올리면 증가하는 **Rayleigh 단조성** 검사.
둘 다 유용하지만 `CALIB_VALIDATED` 를 단독 지지하지 못한다.

**권장 표기 (채택함)**:
```
CALIB_FROZEN_WITH_REPRESENTATION_FAILURE
  T1: SHARED_ATTENUATION_CONSISTENT — weak/structural transfer
  T2: RASTER_NONSPANNING_QA_PASS
  T3: MONOTONICITY_QA_PASS
  SDCP_E: CURRENT_RVE_REPRESENTATION_REJECTED
  EVIDENCE: PROVISIONAL_RAW_JSON_PENDING
```

## 3. Q2 — ② 동결: **(ii) 병기 + 현재 confirmatory 판정은 (iii) 무효**

- 0.17 이 T1 에 **불리한** 후보였다는 점은 전자값을 향한 cherry-picking 이 아니었다는 **정황**.
- 그러나 **로그 최근접이라는 손실함수 자체가 결과를 본 뒤 정해졌으므로** preregistration
  위반은 사라지지 않는다.
- 같은 grid·seed 를 지금 다시 등록해 재실행해도 **이미 본 데이터라 prospectivity 가 회복되지
  않는다.**
⇒ 0.12 와 0.17 을 모두 보고하고 0.17 은 `post-hoc log-nearest nominal` 로만 유지.
새 검증은 **선택 손실함수·grid·tie-break·도달 불가 처리법을 먼저 고정**한 뒤 더 미세한
표현 또는 독립 조건에서 한다.

## 4. Q3 — ⑥ 이 기각한 것: **(b) 내 RVE 구성**

정확히는 **"비겹침 RSA 형상 + 현행 voxel stamp 가 만든 접촉 위상"의 모델 클래스**를 기각.
무한대에 가까운 상 전도도(t = 10⁴)에서도 1.719× 에 머문다는 것은 **그 고정 topology 안에서**
강한 증강이 불가능하다는 유효한 반증이다.  **기각하지 않는 것**: ① 일반적인 voxel FV 솔버
② 실제 SDCP 의 전자전도 물성 ③ 접촉·중첩·터널링을 포함한 다른 voxel RVE.
⇒ 원고 문구 (채택): *"현재 비겹침 RSA 펠릿 RVE 는 압착 펠릿의 SDCP 접촉망을 포함하지 않아
관측된 +SDCP 전자 증강을 재현하지 못했다."*

## 5. Q4 — 검사기 세 건 (P 없음, 그러나 한계 명시 필요)

**4a `code_sha`** — scripts/ 밖 untracked 가 거동을 바꾸는 경로가 **있다**: repo root 의
untracked `sitecustomize.py` + `PYTHONPATH=$REPO` (또는 root 에서 `python -c`) → import hook /
`numpy.load` 변경 → 실행은 달라지는데 plain SHA.  `.pth` 실행행도 site 디렉터리면 매 시작 실행.
⇒ 현재 값은 **`git tracked state` 이지 hermetic execution hash 가 아니다**.
`code_sha clean` **하나를 판정 증거로 쓰지 말 것**.  ✅ 그 한계를 `_code_sha` docstring 에 명시.
⬜ (미착수) 영수증에 `PYTHONPATH`·`sys.path`·인터프리터·로드된 모듈 해시·`sitecustomize` 위치.

**4b 자동 seed** — 덮으면 안 되는 사례가 **있다**: 여러 줄 죽은 가지(`if false; then \n VAR=…\n fi`)
나 호출되지 않는 함수 안의 대입도 "러너가 대입한다" 로 센다.  현재 러너는 관련 flag 를 먼저
무조건 초기화하므로 **판정 영향 없음 (P 없음)**.
✅ 음성 대조 신설: **L-1d** (그 한계를 시험으로 **고정** — 통과하면 한계 그대로, 실패하면
누군가 제어흐름 인식을 넣은 것) · **L-1e** (조립 줄의 FLAG 10개가 전부 **줄머리 무조건 대입**
을 갖는가 = 실제 방어선).
★ 이 과정에서 **내 첫 판 시험이 두 군데 틀렸다**: `local` 접두사를 안 봤고, `$LEAN_FLAGS` 를
`LEAN_FLAG` 로 잘라 잡아 없는 변수를 만들었다.  한 줄짜리 `if false; then VAR=` 로 시험한 것도
틀렸다 (자동 seed 의 `^\s*` 앵커가 이미 배제한다 — Codex 의 예시는 여러 줄이다).

**4c `--step3-require-gpu`** — CPU/GPU σ parity 는 이 리포에서 **검증된 적이 없다** (selftest 는
폴백/중단만 본다).  그러나 **`numeric` 분류 자체는 맞다**: backend 를 고르는 것은 `--step3-gpu`
이고, 이 플래그는 성공한 GPU 계산을 바꾸지 않으며 실패 시 어차피 거부될 CPU 결과를 미리
멈출 뿐이다.  ⇒ physics hash 에 넣지 말고 실제 component backend 를 계속 봉인.
✅ *"same σ either way"* 문구를 **`expected within solver tolerance`** 로 약화 + **CPU/GPU 혼합
cohort 금지** 를 두 파일에 명시.

## 6. Q5 — 문헌 밴드와 p1 값: **W4 (p2) 뒤로 미룬다**

*"같은 자릿수" 도 정량 비교다.*  plate rule 변경량에 **상한이 없으므로** 단서를 달아도 p1 의
73/54.6 을 현재 모델의 값처럼 쓸 근거가 없다.
⇒ 금요일 문서: **문헌 밴드 `~1–65 mS cm⁻¹` 만** 남기고 우리 값과의 일치 문장 삭제.
꼭 필요하면 본문 증거가 아니라 `legacy p1 diagnostic; not comparable to p2` 로만 격리.
✅ week plan §4 에 반영 (보류 블록으로 접어 둠).

## 7. Q6 — A 트랙 사전등록 충분성: **[P1] 통계 규약 미고정**

빠진 것 일곱: `R` 이 ratio of means 인지 mean of paired ratios 인지 · `.125↔.15` pairing 을
µm 로 할지 정규화 bit 로 할지 · off/on 각각의 ΔR 계산식 · `A = 1 − ΔR_on/ΔR_off` 의 SE/공분산
전파 · `ΔR_off ≈ 0` 처리 · 경계 30/70 % 근처 불확실성 · paired ↔ unpaired 중 정본 gate.
또한 **arm 0 포함 8팔 고정, 사후 제외 불가** · pairing 은 **정규화 bit tuple**.
> *"결과가 아직 완전히 blind 이고 payload 를 아무도 열지 않았다면, unblinding 전에 버전된
> amendment 로 분석식을 고정하는 것은 가능하다."*

✅ **개정 A1 등록** (`sdcp_bridge_prereg_amendment_A1_20260827.md`) — 일곱 항목 전부 + 불능
조건 둘(`INDETERMINATE_PRECISION` · `INDETERMINATE_NO_GRID_EFFECT`) 신설.  **문턱 30/70 불변.**
⚠ blind 근거 3종을 그 문서 §0 에 검증 가능한 형태로 적었다 (봉인이 값을 안 찍음 ·
`--collect-only` 미실행 · JSON 이 클라우드에 없음).

## 8. 최종 처분 (Codex 표 + 우리 반영 상태)

| 항목 | 처분 | 상태 |
|---|---|---|
| B | `CALIB_VALIDATED` → `CALIB_FROZEN_WITH_REPRESENTATION_FAILURE` | ✅ |
| ② | 0.17 은 탐색적 nominal, 0.12 와 병기 | ✅ |
| ⑥ | 현 nonoverlap-RSA RVE representation rejected | ✅ |
| 금요일 원고 | 문헌 band 만, p1 우리 값 삭제 | ✅ |
| A | **통계 amendment 전 판정 금지** | ✅ A1 등록 (unblinding 전) |
| 흡수 / 원고 수치 승격 | **여전히 HOLD** | ✅ 유지 |
| B 원자료 JSON | 리포에 넣어야 `PROVISIONAL` 해소 | ⬜ kgy 푸시 대기 |
| 영수증에 실행환경(PYTHONPATH·모듈 해시) | 미착수 | ⬜ |
