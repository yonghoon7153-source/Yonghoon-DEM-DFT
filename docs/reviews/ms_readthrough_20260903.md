# 원고 문장별 읽기 — DEM/MPM/복셀 관점 판정 (2026-09-03)

원문은 `docs/manuscript/body_snapshot_20260903.md` (판간 diff 포함).
형식: 영어 문장 → 번역 → **우리 모델이 무엇을 말할 수 있고 무엇을 말할 수 없는가**.
⚠ 원고를 고치려는 문서가 **아니다** — 시뮬 절이 실험 문장을 넘겨짚지 않게 하는 것이 목적이다.

---

## ★★ 세 문단 누적 결산 — 한 장

### ✅ 우리가 숫자를 대는 자리 (셋)

| 원고 문장 | 우리 값 | 근거 |
|---|---|---|
| DBE 0.5+0.5 vs SBE 1.0 wt%, 동일 총 바인더 | 8팔 대조의 **정의** | 침대 조성 일치 |
| *"cross-sectional SEM … **fewer voids**"* | porosity **7.86 → 7.37 %** (−6.2 %), 두께 72.53 동일 | 대시보드 실측 |
| *"enables a **lower PTFE fraction**"* | PTFE 스탬프 ON 시 SBE **−25.2 %** vs DBE **−13.0 %** ⇒ 비 1.1263 → 1.3092 | CL-49 |

### ⛔ 아무 말도 하지 않는 자리 (넷)

| 원고 문장 | 왜 못 하나 |
|---|---|
| PTFE **fibrillation** · 자립성 · 도우 형성 | 모델에 **fibril 이 없다** — PTFE 는 차단 복셀(sid 9)일 뿐 |
| **탄성 회복** 0.69 → 0.82 | `--protocol hold` 에 **unload 가 없다**.  ⇒ **언급하지 않기로 확정 (저자 지시 09-03)** |
| **SAICAS** 수평 절단력 | 모델에 **바인더 응집력이 없다** (PTFE=차단·SDCP=도체, 붙이는 항 없음) |
| XRD 2차상 부재 | 상은 **입력**이지 결과가 아니다 — **면허**로만 인용 |

⚠ **탄성 회복 실무 규칙**: `E = 9.0 / 1.8 GPa` 를 탄성 회복 문장 **근처에 두지 않는다**.
두면 독자가 *"모델이 0.69 → 0.82 를 냈다"* 로 읽는다.  `E` 는 **Table S2 물성 행에만**.

### ★★ 강해진 것 — 하한 축 하나가 실험 영수증을 얻었다

우리는 PTFE 를 **균일 분산**으로 찍는다.  **응집을 표현하지 않는다.**
원고 Figure 3a 의 F 원소 맵이 **SBE 의 F-rich 섬유 도메인**을 직접 보여준다.

```
실물 SBE   F-rich 도메인이 뭉쳐 있다
우리 SBE   PTFE 가 고르게 퍼져 있다
⇒ 우리 SBE 는 실물보다 "잘 만들어진" 전극  ⇒ σ_e(SBE) 과대평가
⇒ R = σ_e(DBE)/σ_e(SBE) 를 **과소평가**  ⇒ 보고 이득은 이 축에서 **하한**
```
★ 지금까지 우리 주장이었고, 이제 **원고 자신의 그림이 근거**다.
(네 하한 축: 격자 미수렴 · **PTFE 응집** ← 앵커 획득 · SDCP 압착 접촉 · 접촉저항 일반)

---

## 문단 1 — Figure 2g (기계) · 2h/2i (펠릿 σ)

**E: PTFE 1.8 → SDCP 9.0 GPa (AFM force–distance, 압착 바인더 필름)**
✅ **우리 코드에 이미 그 값** — `ADD_E_SET` 2026-08-18 (옛 SDCP 23.6 · PTFE 5.6 폐기).
⚠⚠ **그런데 격자 스윕 침대는 전부 2026-08-12 판 = SDCP E 23.6 (옛 값)** (CL-56).
⇒ 원고 본문에 9.0 을 쓰는 건 맞으나 **시뮬 절에서 "같은 물성" 으로 읽히면 안 된다** — 침대 앵커 명시.
⚠ 범주: AFM 은 **압착 필름** 탄성률, 우리는 **상(phase)** 탄성률로 쓴다.  **PTFE 1.8 도 같은 방법이라
비(5배)는 안전**하고 절대값에만 규약이 붙는다.

**σ_ion 3.57 / 0.97 / 2.86 mS cm⁻¹ · σ_ele 0.30 / 0.12 / 1.53 ×10⁻⁷ S cm⁻¹ (9:1 wt)**
✅ 두 비가 코드에 있다 — `2.86/3.57 = 0.801` = `σ_ion×0.80` · `1.53/0.30 = 5.1` = `σ_e×5.1`
   (`scripts/coating_presets.py`).
★ 이 세 값이 **우리 D13 펠릿 보정의 표적**이다.  ⚠ 규약 5개 미기록 (성형압·인가압·온도·
   두께/면적·블로킹 전극) — **CL-62**, 협력자 이메일로 닫힌다.
⚠⚠ **"이 규약 안에서" 가 가장 필요한 자리**: 이 문장의 절대값 `~10⁻⁷ S/cm`(SE-바인더 **펠릿 복합**)
   와 우리 상 σ_SDCP `250 S/cm`(**복셀 상**)은 **9 자릿수** 차이인 **다른 양**이다.
   `coating_presets.py` 주석이 이미 *"σ 비는 manuscript pellet-COMPOSITE — phase σ 아님"* 이라 못박았다.
   ⇒ **같은 표에 두지 말 것.**

**"not achieved at the expense of ionic and electronic transport"**
✅ 우리 8팔이 전극 수준에서 재현: σ_ion **+0.8 %**(사실상 무손실) · σ_e **+30.9 %**.

**"compensates for … reduced PTFE content"**
★★ 원고가 스스로 **두 원인이 섞여 있다**고 말한다: `DBE 이득 = SDCP 추가 + PTFE 감소`.
   큐에 걸린 **σ_SDCP = 0 판별 팔**(`sdcp_inert_prereg_20260903.md`)이 정확히 이 둘을 가른다.

---

## 문단 2 — DBE/SBE 정의 + 대조 실험

**"SDCP alone cannot produce a mechanically coherent freestanding electrode during hot rolling"**
⛔ 모델에 fibrillation 이 없어 **지지도 반박도 못 한다** — 순수 실험 근거.
⚠ 공정도 다르다: **hot rolling** vs 우리 **300 MPa 단축 압축**.

**"reducing the PTFE content to 0.5 wt% without SDCP → incomplete dough … capacity decay"**
★★ **이 대조군은 우리 판별 팔과 다르고, 그래서 상보적이다.**

| | 총 바인더 | SDCP 부피 | 기하 | 무엇을 재나 |
|---|---|---|---|---|
| 원고 중간 (PTFE 0.5 단독) | **0.5 wt%** | 없음 | **다름** (porosity 변함) | PTFE 감소 효과 (기계+수송 섞임) |
| 우리 판별 팔 (σ_SDCP=0) | 1.0 wt% | 있음 | **바이트 동일** | SDCP **전도 몫만** |

★ **우리 팔은 실험으로 만들 수 없다** — *"거기 있는데 전도는 안 하는 SDCP"* 는 실물에 없다.
   ⇒ **시뮬레이션만 할 수 있는 분해**이고, 이것이 시뮬 절의 존재 이유 중 하나다.

---

## 문단 3 — XRD · SEM(F 맵·단면) · AFM 나노압입

**XRD**: 상 배정의 **면허**.  우리 모델에 2차상 칸이 없다는 전제를 실험에 건다.
**F 맵**: 위 §하한 축 참조 — **가장 큰 소득**.
**단면 SEM**: porosity −6.2 % 로 **정량화**.  ⚠ `ε_sphere`(구 부피 합) vs **2D 단면 면적률** = 다른
측정 ⇒ *"일치"* 가 아니라 *"같은 방향, 이만한 크기"*.
**탄성 회복 0.69 → 0.82**: ⛔ **언급하지 않는다** (저자 지시).

⚠ 마지막 문장의 두 절은 **근거 등급이 다르다** — *"재분배"* 는 Figure 3a 직접 관측,
*"입자 접촉 유지"* 는 사이클 함의인데 이 문단에 사이클 데이터가 없다.  뒤 절은 이후 절이 받아야 한다.

---

## 문단 4 — SAICAS (Figure 3c,d)

**원고 최초의 3팔 분해다.**  우리 사전등록과 같은 산술 형태다.

```
PTFE 절반 감소   0.33 → 0.17 N/mm   Δ = −0.16   (−48.5 %)
SDCP 투입        0.17 → 0.37        Δ = +0.20   (+117.6 %)
순 효과          0.33 → 0.37        Δ = +0.04   (+12.1 %)

보상률 = (DBE − 중간)/(SBE − 중간) = 0.20/0.16 = 1.25  ⇒ 손실의 125 % 회복 = 25 % 초과
```
★ *"restore, and **slightly enhance**"* 의 정확한 숫자.  SBE 대비 `+12 %` 와 병기 가능하나
**문장이 "보상을 넘었다" 를 주장하므로 `125 %` 가 자기일관**이다.

⛔ 시뮬 절에서 SAICAS 를 건드리지 않는다 (바인더 응집력 부재).
★ *"particle-level contact network"* 는 우리 접촉망과 **다른 것**이다 — 우리 것은 **수송 접촉**이지
기계 응집이 아니다.  받치려면 **기하·전도 증거**로: `porosity −6.2 %` · `도전재덮임 AM_S 13.10 →
15.50 % (+18.3 %)`.

### ★★ 이 문단이 드러낸 구조적 공백

```
기계 축 (SAICAS)   SBE 0.33  ·  중간 0.17  ·  DBE 0.37     ← 3점 완비
전도 축 (우리)      SBE 1.000 ·  중간  ??   ·  DBE 1.308    ← 중간이 비어 있다
```
⇒ 두 축을 **같은 세 점** 위에 놓으려면 **`PTFE 0.5 단독` 팔**(총 바인더 0.5)이 필요하다.
그러면 `보상률(기계) = 1.25` 옆에 `보상률(전도) = ?` 를 쓸 수 있다.
⚠ **비용**: 바인더 질량이 달라 **새 침대**다 (DEM/MPM 재생성 + STEP3) — σ-only 팔보다 비싸다.
⚠ **해석**: 원고가 그 조성을 *"incomplete dough … capacity decay"* 라 했다 = **실물로 못 만드는 전극**.
   모델은 σ_e 를 계산해 주지만 **"제조 불가 조성의 전도도"** 라벨이 필요하다
   (우리 degenerate-network 케이스와 같은 부류).

---

## 미결 — 다음 세션이 이어받을 것

1. **참고문헌 +1 정정** (원문 대조로 확정): CL-61 · CL-62 · 편집 시트 §2-6/§2-7
   → Patil `[36]` · Jung `[37]` · Hong `[38]`.  ⚠ `[39]` 신규 등장 (단면 SEM).
2. **`docs/sdcp_master.md` §3.2** 를 원고의 *"partially dissociated"* 에 맞춰 정정
   (원고가 앞서 있고 우리 문서가 뒤처졌다 — 판간 diff §⓵ 참조).
3. **침대 앵커 명시**: 원고 E = 9.0 인데 격자 스윕 침대는 **23.6** (CL-56).
4. **Figure 2e DFT** 가 어느 계산인지 확인 (우리 `E_bind` 는 INVALID 상태).
5. 다음 문단부터 이어 읽기 — **읽기 전에 이 파일과 스냅샷을 먼저 갱신할 것.**

---

# 문단 5 — ★★ 우리 파트 (DEM/MPM + 복셀 수송) — 2026-09-04

원문·개정본은 `body_snapshot_20260903.md` §우리 파트.  **이 문단만 우리가 저자다** — 다른 문단은
*"넘겨짚지 않기"* 가 목표였지만 여기는 **우리가 정확성을 책임진다**.

## ★★★ 반드시 Methods 에 들어가야 할 문장 — **AM-freeze** (저자 지시로 고정)

본문이 *"plastic densification"* 이라고만 하면 **전체 충전물이 소성 치밀화한 것**으로 읽힌다.
실제로는 **SE 만** 소성 변형하고 **AM 은 고정 장애물**이다.

```
In the MPM stage the DEM-derived AM skeleton was held fixed as a rigid obstacle and only
the solid electrolyte was treated as a deformable material, so that the plastic
densification reported here is that of the solid electrolyte phase.
```

★ **이것은 약점이 아니라 설계다.**  AM 을 풀면 강체 AM 이 force chain 으로 하중을 가려
porosity 가 **36–41 %** 로 튄다 (실측).  AM-freeze 4근거: ① frame[5] — AM load-bearing 은 rigid
접촉망 현상이라 연속체 MPM 이 표현 불가 ② mobile-rigid AM 은 over-shielding ③ AM-as-material 은
n_grid ≥ 384 에서 CFL/OOM ④ DEM AM 이 이미 검증된 300 MPa 골격이라 움직이면 drift.
⇒ **이유를 한 줄 붙이면 오히려 방어가 된다.**

## 검산 — 원고 수치는 우리 정본과 5자리까지 일치한다

```
원고 비   70.61 / 53.99 = 1.307835
정본 R (centerline)     = 1.307820      차이 1.5e-5  ⇒ **centerline 규약 확정**
centerline SBE 53.99    = 생산 규약 73 mS/cm 의 74 %  (−26 %, CL-49 정합)
CA 접촉수 74 → 86 = +16.2 %   vs   σ_e +30.8 %   ⇒ **비선형**
```

## 문장별 조치 (우선순위)

| 급 | 문장 | 조치 |
|---|---|---|
| **P0** | ⑧ σ_ele | **규약 라벨 필수** — `53.99/70.61` 은 **centerline(PTFE 차단)** 이다.  생산 규약(PTFE 미표현)은 σ_e 가 **73 mS/cm** 로 26 % 높고 **비도 다르다**(그 비는 CL-33 계열이라 여기 적지 않는다 — 정본은 `claims.json`).  ⚠ Methods 가 어느 규약을 적고 있는지 **확인 필요** |
| **P0** | ⑨ 전류장 | *"overall higher electronic current density"* → **집중도 −17.8 %** 로 교체.  안 고치면 **그림이 문장을 반박**한다 (S18 에서 DBE 가 더 흐리다) |
| **P1** | ② 방법 | ✅ `constructed`·`followed by` 로 개정됨.  잔여: `powder packing` **`and compaction`** · 뒷절 복원 · Methods 에 AM-freeze |
| **P1** | ⑧⑩ | **격자 미수렴 + 하한** 한 줄.  ★ 근거를 **원고 자신의 Figure 3a**(PTFE 응집)로 댈 수 있다 |
| **P1** | ⑦ | `0.15 µm` **= 복셀 한 칸(one voxel edge)** 명시.  자의적 선택이 아니라 격자에서 온 값이라는 게 방어다 |
| **P2** | ④ `solely` | *"SDCP 추가 + PTFE 절반 감소"* 두 원인을 명시.  앞 문단이 이미 인정하므로 여기서만 뭉뚱그리면 자기모순 |
| **P2** | ⑥ `most` | 중앙값이 오르면 **정의상 참**이라 약하다 → **실제 분율 + 10-백분위**(가장 CA-빈곤한 입자도 오르는가)가 *"국소가 아니다"* 의 진짜 증거 |
| **P2** | ⑩ | `demonstrate` → `indicate` (짝 침대 **한 쌍** · 미수렴 격자) |
| **P2** | ⑧ | `53.99/70.61` → `54.0/70.6` + 비 `1.31` (8팔 SE 0.1–0.35 %p · 미수렴 ⇒ 4자리는 가짜 정밀도) |

## ★ 넣을 수 있는데 안 들어간 우리 수치 다섯

```
econn 연결률       100 / 100 %          "fully percolated" 를 정량으로
porosity           7.86 → 7.37 %        Figure 3b "fewer voids" 와 연결
σ_ion              +0.8 %                "comparable ionic" 을 정량으로
전류 집중 p99.8    ×1447 → ×1189        프레임 무관 헤드라인 (−17.8 %)
접촉수 vs σ_e      +16.2 % → +30.8 %     비선형 = 망 위상이 바뀌었다는 신호
```

## 문장 후보 (그대로 붙여 쓸 수 있게)

**⑤ 퍼콜 + 분산** — *"연결성이 아니라 국소 밀도의 차이"* 가 이 문단의 정확한 요약이다:
```
Both electrodes retain fully percolated electronic networks (100 % of the carbon phase
connected to the current collector in both cases), so the difference is one of local
density rather than connectivity.
```

**⑨ 전류장** (프레임 무관으로):
```
The ionic distributions are essentially unchanged (sigma_ion differs by 0.8 % between the
two electrodes), whereas the electronic field is markedly less concentrated in the DBE:
the 99.8th-percentile current density falls from 1447 to 1189 times the through-plane
mean, a 17.8 % reduction in current focusing. The DBE panel therefore appears fainter on
the shared colour scale not because it carries less current, but because the same current
is carried over more parallel paths.
```

**⑩ 결론 + 하한**:
```
Because the model represents PTFE as uniformly dispersed rather than aggregated into the
fibril-rich domains observed in Figure 3a, and because the ratio is not grid-converged,
the reported gain is a conservative estimate.
```

**Methods 각주 — 절대값 규약**:
```
The absolute conductivities are model responses under a stated closure and are not
directly comparable to the two-terminal TLM values measured on the same electrode, which
are lower by ~2 orders of magnitude because the voxel representation fuses touching cells
and therefore carries no explicit particle-particle contact resistance. The ratio is not
grid-converged: refining the voxel edge raises it monotonically, so the reported value is
a lower bound.
```
⚠ `444배` 를 본문에 쓸 필요는 없다 — *"~2 orders"* + **이유**(접촉저항 부재)면 충분하고,
**차이의 이름을 우리가 안다**는 점에서 오히려 강하다.

---

# 문단 5 — 저자 확정본 (2026-09-04 세션에서 문장별 합의)

★ 아래는 **저자와 문장별로 합의해 확정한 것**이다.  제안이 아니라 **결정**이다.

## 확정된 문장

**②** `reconstructed` → **`constructed`** · `coupled with` → **`followed by`**
```
To directly evaluate this effect, three-dimensional SBE and DBE microstructures were
constructed by a discrete element method (DEM) simulation of powder packing followed by a
material point method (MPM) simulation of plastic densification
```
⇒ 잔여 권고(미반영): `powder packing` **`and compaction`** · 뒷절(`Figure S16`/`Table S2`/`[40,41]`) 복원.

**③** `reconstructed microstructures` → **`the resulting microstructures`** (② 와 일관).
⚠ 저자 결정: **규약 문장은 본문에 안 넣는다.**  (뒤 TLM 문단이 절대값 차이를 다루면 충분)

**④** 저자 검토 후 **원문 유지 결정.**  (권고했던 `By construction` · 두 원인 명시는 미채택)

**⑤** **원문 유지.**  `uniformly dispersed` **넣는 것으로 저자 확정.**
⚠ 내가 뺄 것을 권했으나 저자가 유지를 택했다 — 결정 존중.

**⑥** `most` → **`85 %`**  ← ★ 원자료에서 새로 계산 (아래 §신규 수치)
```
Indeed, 85 % of AM particles in the DBE exhibit CA densities above the SBE median,
indicating that this enrichment extends throughout the electrode rather than being
confined to localized regions.
```

**⑦** `0.15 μm` 뒤에 **`(equal to one voxel edge of the transport grid)`** 삽입 — 확정.

**⑧** 수치는 **`53.99 / 70.61` 유지** (그림에도 같은 값이 들어가 있어 일관성 우선).
σ_ion 을 **같은 문장에 병기**하고 SI 로 보낸다:
```
Consistently, the simulated effective σele increases from 53.99 to 70.61 mS cm−1
(Figure 4b), whereas the effective σion remains essentially unchanged at 0.553 and
0.558 mS cm−1 for the SBE and DBE, respectively (Figure S_).
```

**⑨** 이온 절을 빼고 전자에 집중 (`whereas` 중복 제거) + **핫스팟 완화**를 괄호로:
```
The corresponding ionic and electronic current-density fields are presented in Figures S_
and S_, respectively. The DBE shows a higher electronic current density carried over more
parallel paths, which relieves rather than intensifies local current hot spots (the
mean-normalized 99.8th-percentile current density falls from 1447 to 1189).
```
⚠ 내가 *"S18 에서 DBE 가 더 흐리다"* 고 한 것은 **썸네일 오독**이었다 — 큰 그림에서는
DBE 가 더 조밀하고 빨강(핫스팟)이 적다.  **원문 방향이 맞았고 내 P0 경고는 철회**했다.

**⑩** 미확정.  권고: `demonstrate` → `indicate` · `and distributes the electronic current
more evenly` 추가 (⑨ 를 결론이 받게).

## ★★ 기억할 것 — Table 에 넣을 항목 (저자 지시 2026-09-04)

`σ_ion` 결과(`0.553 / 0.558`)를 실으면 **그 입력이 어딘가 있어야 추적된다.**
저자 결정: **Table (S2) 에 넣는다.**

```
The SDCP phase was assigned an ionic conductivity of 1 × 10−3 S cm−1 in the transport
solver; this is an assumed value.
```

⚠ 이것이 원장의 옛 판단(*"Table S2 의 SDCP 이온전도도 칸이 비어 있는 것은 옳다"*)을
**바꾼다** — 그때는 σ_ion 결과를 안 실었기 때문이다.  결과를 실으면 입력도 실어야 한다.

★ **역산값과 혼동하지 말 것** (저자 지적):
```
펠릿 RVE 역산   σ_ion(SDCP)* = 0.62×10⁻³ S/cm   (확인 런 2.8655 vs 표적 2.86, 4/4 시드,
                                                 2026-08-25 동결)
전극 8팔 입력   1.0×10⁻³ S/cm                    ← 코드 기본값, 가정
```
동결 문서 §14-3 이 **이식을 금지**했으므로 전극 런은 `1e-3` 로 돌았다.  ⇒ `assumed` 가 맞다.
★★ **저자 최종 결정 (2026-09-04)**: **`1.0 × 10⁻³ S cm⁻¹` 을 Table 에 그대로 넣는다.**
역산값(0.62e-3)은 **본문·표에 쓰지 않는다** — 규약 구속이라 전극 런에 이식되지 않았고,
그 사실을 원고에서 설명할 이유가 없다.  저자 표현: *"그게 시뮬레이션의 묘미"* —
**입력을 밝히고 그 입력에서 나온 결과를 보고하면 된다.**
⇒ Table 행: `σ_ion(SDCP)  1 × 10⁻³ S cm⁻¹  ·  assumed`
⇒ 역산값·이식금지·네 시나리오는 **우리 원장에만** 남긴다 (이 문서 + 편결 시트 §3-3).

## ★ 신규 수치 — 원자료에서 오늘 계산 (`docs/figures/cbd_contacts.csv`, n=1,271 씩)

```
SBE 중앙값(74) 초과 비율     DBE 1083/1271 = 85.2 %      SBE 631/1271 = 49.6 %

백분위       SBE   DBE     Δ%          ← 분포 전체가 평행 이동한다
   5 %        58    68   +17.2         ★ 아래 꼬리가 위 꼬리보다 더 오른다
  10 %        61    71   +16.4            = CA-빈곤 입자가 우선 구제된다
  25 %        67    78   +16.4            = "국소가 아니다" 의 진짜 증거
  50 %        74    86   +16.2
  75 %        81    93   +14.8
  90 %        88   100   +13.6
  95 %        91   104   +14.3
최소/최대   42–106  55–118
```
⚠ 저자는 **⑥ 에 `85 %` 만** 넣기로 했다.  백분위는 SI·캡션 후보로 남긴다.

## ⚠⚠ σ_ion — 원장에 **이미 64팔이 있었다** (내가 "없다"고 한 것은 오류)

`ms_si_v7_edit_sheet_20260901.md` §3-3, **4 시나리오 × 8 origin × 2 침대 = 64 팔 완주**:

| σ_ion(SDCP) 가정 | SBE | DBE | 비 R |
|---|---:|---:|---:|
| 0 | 0.5534 | 0.5410 | 0.9776 |
| 5.52×10⁻⁵ | 0.5534 | 0.5425 | 0.9804 |
| 5.21×10⁻⁴ | 0.5534 | 0.5518 | 0.9972 |
| **1.0×10⁻³** | **0.5534** | **0.5580** | **1.0083** | ← 본문이 쓰는 것

등록된 판정: **네 시나리오에서 `|R−1| < 2.3 %`, 방향 미결정** (`r` 을 바꾸면 부호가 뒤집힌다).
⇒ 저자 결정: **`1×10⁻³` 하나만 보고**하되 문장의 주장은 *"essentially unchanged"* 로 둔다.
그 주장은 **네 시나리오 전부에서 참**이므로 방어된다.  ⛔ *"SDCP 가 이온 전도를 올린다"* 는
여전히 **쓸 수 없다**.

★★ **내 오류 기록** — 오늘 같은 실수를 세 번 했다: Patil `0.62` · litdb 인덱스 · 이 σ_ion.
셋 다 **원장에 있는데 확인 전에 "없다"고 말했다.**  원장 자신이 적어둔 교훈
*"'모른다' 는 결론도 검증 대상이다"* 를 내가 안 지켰다.
⇒ **"없다" 를 말하기 전에 `grep` 을 먼저 한다.**

## 다음 문단 (실험 검증 — TLM · SSRM · KPFM) 착수분

**첫 문장**: `experimentally verified` → **`examined experimentally`** 권고.
`verified` 는 *"시뮬이 예측하고 실험이 확증했다"* 는 약속이라, 절대값 대조를 불러온다.
저자 방침(*"시뮬은 맞출 필요 없다, 오더와 상대크기만"*)과도 어긋난다.

**셋째 문장**: `predicted by the DEM simulations` → **`the simulations`** 또는
**`the DEM–MPM simulations`**.  우리 것은 DEM 만이 아니다 (DEM → MPM → 복셀 FV).
`predicted` 도 `verified` 와 같은 계열 — `consistent with the simulated increase in σele` 권고.

---

# 실험 절 대조 — ★ 압력 불일치 (2026-09-04, 저자 지시로 기억)

## ⚠⚠ 시뮬 압력과 실물 압력이 다르다 — **시뮬 Methods 에 명시할 것**

원고 Experimental Section (mold cell assembly) 실측:
```
양극 성형     433 MPa      ← 복합 양극을 SE 층에 눌러 붙일 때
셀 조립       200 MPa      ← 집전체 넣고 전체 압축
```
우리 침대:
```
DEM/MPM 압밀  300 MPa
```

⇒ **우리 침대는 300 MPa 로 만들었는데 실물 양극은 433 MPa 로 눌렸다.**
다공도는 압력에 민감하다 (우리 Heckel `P_y = 138 MPa`) ⇒ **다공도·접촉 통계에 직접 걸린다**
(`porosity 7.86 / 7.37 %` · `CA 접촉수 74 / 86` 이 전부 300 MPa 침대의 값이다).

★ **조치**: Methods 시뮬 절에 **압력이 다르다는 사실을 적는다.**  숨기면 심사자가 두 절을
나란히 놓고 묻는다.  적으면 "규약을 안다" 가 된다.

⚠ 그리고 **캘린더링 압력·간극·온도가 원고에 없다** — `433 MPa` 는 **몰드 셀 성형압**이지
도우를 필름으로 만드는 캘린더링이 아니다.  최종 다공도를 정하는 것은 캘린더링 쪽인데
그 조건이 비어 있다.  ⇒ 우리 300 MPa 를 무엇과 비교해야 하는지도 확정되지 않는다.

## 실험 절에서 확인된 것 (우리 모델과 일치 — 기록)

```
조성        NCM811 : LPSCl(1 µm) : VGCF = 70 : 27 : 3          ✅ 우리 침대와 동일
바인더      총 1.0 wt% 고정                                     ✅
SBE / DBE   PTFE 1.0  /  PTFE 0.5 + SDCP 0.5                    ✅
볼밀        200 rpm 1 h  →  Thinky 2000 rpm 5 min               ✅ seed_sdcp 의 "고전단으로
                                                                   0.2–0.5 µm 단입자" 전제와 정합
질량 하중   16 mg cm⁻²
섬유화      85 °C 핫플레이트에서 5회 늘리고 접기                  ⛔ 우리 모델에 fibrillation 없음
```

## 실험 쪽 소관 (우리가 손대지 않는다 — 참고만)

· 혼합 순서가 SBE·DBE 에서 다르다 (DBE 는 SDCP 먼저 → PTFE 나중; SBE 는 PTFE 만)
  ⇒ 두 전극이 받은 전단 이력이 다를 수 있다.  ⚠ 우리 모델은 이것을 표현하지 않는다.
· 캘린더링 조건(온도·간극·속도) 미기재
· `stretched and folded five times` 의 정량 지표(연신비 등) 없음
· C-SUS 코팅 절: 코팅 방법·건조 조건·초음파 펄스 on/off 시간 미기재 (~200 nm 재현 불가)

---

# Methods (우리 파트) 재작성 — 저자 확정본 2026-09-04

## 주간미팅 피드백 (저자 전달, 러프 메모)

```
A  DEM/MPM 서술 비중 축소 · 실제로 한 것 위주       D ★ "문제가 없다고 모듈러스를 줄였다" 가
B  DEM/MPM/DFT 파라미터 표는 별도 파일(SI)             포장처럼 읽힌다 → "porosity 타겟에
C  중요한 것·필요한 수식은 다 유지                      맞춰 보정했다" 로 진행
E  Simulation 절 안에 reference · 유효 σ_ion·σ_e 문헌 레인지 (금요일)
```

★ **D 가 핵심이었다.**  옛 문장은 *"강체 구는 소성 평탄화·재배열·입계 미끄러짐을 재현 못 하므로
E 를 24 → 1.35 GPa 로 낮췄다"* 로 **물리적으로 정당화**했는데, 그것이 변명으로 읽혔다.
⇒ **"측정 다공도·겹침을 재현하도록 보정했다"** 는 **사실 서술**로 바꾸면 논쟁이 사라진다.
⚠ 우리 원장의 frame[2](연화 = 빠진 입상 기전의 lumping, 3중 교차검증)는 **여전히 유효**하다 —
   원고에 그 논거를 **쓰지 않기로** 한 것이지 판정을 뒤집은 것이 아니다.

## ⛔ 고친 P0 둘

**P0-① Methods 가 본문과 다른 규약을 적고 있었다**
```
옛 Methods:  "PTFE was not resolved on the conduction grid"
             = PTFE omitted from the electronic grid  ⇒  σ_e 72.32 / 81.26 · 비 1.1237
본문:        53.99 / 70.61 · 비 1.3078
             = PTFE centerline voxels excluded
```
⇒ 재현하면 **다른 값이 나온다.**  고친 문장:
`voxels lying on the centerline of a PTFE fibril were excluded from both grids, so that
PTFE acts as a blocking phase.`
⚠ 편집 시트 §2-2 지시는 **SI Table S3 에 두 규약을 다 싣고 어느 쪽도 굵게 하지 않는 것**이다.
  본문이 한쪽을 쓰는 것은 편집 결정이고 그 사실을 문장이 밝혀야 한다.

**P0-② `standard error` 는 우리가 하지 않은 통계**
8 origin 은 같은 침대의 완전 half-voxel 조합이라 **복제 자유도 0** ⇒ 표준오차가 정의되지 않는다.
고친 문장: `Shifting the grid origin resamples the same packing rather than generating a new
one, so the eight solutions are not independent replicates. Ratios are therefore reported as
the mean over the eight origin-matched SBE/DBE pairs; the spread across origins is 0.08 %,
an order of magnitude smaller than the spread of the absolute conductivities.`
★ `0.08 %` = 쌍대응 산포 실측 (절대값 팔 폭 SBE 1.70 % · DBE 1.33 % 대비 ~20배 작다).

## 그 밖에 확정된 것

· **AM-freeze 한 절 유지** — `the active material was held fixed as a rigid obstacle, so the
  plastic densification reported here is that of the electrolyte phase.`
· **접촉 모델 이름만 넣고 수식은 안 넣는다** — `using a Hookean contact model with hysteretic
  unloading`.  ⚠ **Hertz/hooke 수식을 쓰면 E 가 물성처럼 보여 D 항목 논쟁이 되살아난다.**
  재현성은 모델 이름으로 충분하고, 요구받으면 그때 넣는다.
· 두께 **72.5 µm** 명시 · `50 × 50 µm²` 는 **cross-section** 임을 밝힘
· 파라미터 전부 **Table S2** 로 (입자수·반경·E·ν·σ_y·복셀·σ 배정)
· 영국식 철자 없음 확인 (`fibers` · `centerline` ✓)

## ⚠ 미해결

· **`reconstructed` 가 Methods 에 남아 있다** — 본문은 `constructed` 로 고쳤다.  **불일치.**
· `[9, 52]` 문헌 번호가 다공도·겹침 앵커로 맞는지 미확인.

## 길이 대조 (Methods 절별 단어 수, 우리가 실측)

```
C-SUS coating  92 · Dry electrode fab 149 · Mold cell 121 · Pouch cell 133
Electrochemical 169 · Material charac 275 ← 실험 최장
DEM-MPM (ours) 400  ← Methods 전체 1,339 단어의 30 %, 실험 최장의 1.45배
```
⇒ **소제목을 둘로 나누면**(`Microstructure generation` / `Effective transport`) 표기상 해소된다
(195 + 205 단어로 각각 `Material charac` 보다 짧다).  내용은 그대로 둔다.

# Figure 4 — 새 구성 (저자 확정 2026-09-04)

```
(a) 3D 전자 전도망 + 컬러바 (AM 입자별 CA 접촉수)     ← 본문 ⑤⑥
(b) CA 접촉수 바이올린 플롯 + 유효 σ_e               ← 본문 ⑦⑧
(c) Nyquist + TLM R_ele                              (d) SSRM 저항 맵
```

## ⚠⚠ 갱신 필수 — 현재 그림이 옛 세대다

| | 현재 | 확정 |
|---|---|---|
| (a) 컬러바 | `298 – 673` (접촉수, v6) | **SBE 중앙값 정규화 density** (무차원, 1 근처) |
| (b) σ_e | `1.98 / 3.00` **S** cm⁻¹ | **53.99 / 70.61 mS cm⁻¹** ← **단위 S → mS** |
| (b) σ_ion | `0.203 / 0.215` | ⛔ **제거 → SI** |
| 캡션 | *"ionic and electronic"* | **electronic 만** · `reconstructed` → `constructed` |

★ **`S → mS` 가 가장 위험하다** — 축 라벨을 안 바꾸고 숫자만 바꾸면 1000배 틀린다.
★ 바이올린에 **중앙값 선**을 넣으면 본문 `74 → 86` 이 그림에서 바로 읽힌다.
★ 바이올린이 본문 ⑥(`85 %`)을 그림으로 만든다 — 백분위 5 % 58→68 · 95 % 91→104 로
  **분포 전체가 평행 이동**하는 것이 형태로 드러난다.

## 캡션 — ✅ 저자 확정 (2026-09-04)

```
Figure 4. (a) DEM-MPM constructed electronic conduction networks of the SBE and DBE, with
each AM particle colored by the local CA density within 0.3 μm of the particle surface,
normalized to the SBE median. (b) Distribution of the number of CA contacts per AM particle
(violin plots; horizontal lines mark the medians) and the corresponding effective electronic
conductivities. (c) Nyquist plots of SBE and DBE cathode symmetric cells with the electronic
resistances extracted using the TLM-based equivalent circuit. (d) SSRM resistance maps of
polished SBE and DBE cross-sections.
```

## ⛔⛔ (a) 는 **density** 이지 contacts 가 아니다 — 내가 캡션에서 뭉갰다

원장이 이미 못박아 둔 것 (handoff §3-3, Fig 4a 라벨 사슬):
> 뷰어 콜러바가 **철회된 "접점" 해석**을 그대로 찍고 있었다.
> 제목 `Carbon point density near AM` → **`Conductive-additive density near AM`**
> **`NOT a contact count` 명시** · 눈금은 **정규화된 정량 수치**(low/high 라벨 아님)
> 밴드 정의(0.3 µm, center)는 **캡션 소관** — 그림 안에 안 적는다

본문도 둘을 나눠 쓴다: **(a) = local CA density (0.3 µm, SBE 중앙값 정규화)** ·
**(b) = number of CA contacts (0.15 µm 껍질, 개체 단위)**.
⇒ **두 패널이 다른 반경·다른 양**이라 캡션이 그것을 밝혀야 한다 (확정본에 반영됨).

⚠ **내 앞선 지시 "컬러바 42–118" 은 틀렸다** — 그건 **접촉수** 범위다.
(a) 는 **SBE 중앙값으로 정규화한 무차원 density** 라 눈금이 1 근처다.


---

# Table S2 · S3 · Figure S16 — 저자 확정 (2026-09-04)

## ★★ CL-61 정정 — **σ_e(SDCP) = 250 은 저자의 4-probe 실측이다**

저자 확인 (2026-09-04): *"이건 저자가 4-probe 로 잰 거야."*

⇒ **CL-61 의 *"저자 지정값 · 문헌 앵커 없음"* 서술을 상향한다.**  표 라벨도
`Assumed` 가 아니라 **`Measured`** 다 (Table S2 반영 완료).
⚠ **여전히 남는 결손 하나 — 시편 규약**: 4-probe 를 **캐스팅 필름 / 압착 펠릿 / 분말**
중 무엇으로 쟀는지.  `--sigma-sdcp` help 가 이미 *"cast film 인지 pressed pellet 인지
UNRECORDED"* 라고 적고 있다.  ★ 오늘 Patil 카드가 보인 대로 **필름(접촉저항 없음) vs
펠릿(접촉저항 포함)** 이 자릿수를 가르므로, 융합-복셀 규약과의 정합성이 여기 걸린다.
⇒ **저자에게 이것 하나만 물으면 이 축이 닫힌다.**

## Table S2 — 확정 상태

✅ 반영됨: `Young's modulus (dense) 24 GPa` **행 삭제**(피드백 D — 24 vs 1.35 대비가
표에서 논쟁을 되열지 않게) · Source 넷 정정(**SDCP Measured** · NCM/VGCF **Assumed** ·
VGCF 78.5 만 Calculated) · **σ_ion(SDCP) 1.0×10⁻³ Assumed 추가** · `ν (DEM contact) 0.3`
추가 · thickness 를 S3 로 이관 · 제목 `DEM–MPM`.

★ `ν = 0.3` 은 **DEM 접촉모델 입력**이라 넣는 것이 옳다 (E* 에만 들어가는 2차 인자).
⛔ **그 값에서 K·G 를 유도해 물성으로 적지 않는다** — 원장이 경고한 자리.  현재 표에 없다 ✓

⚠ 남은 것:
· **`ν (DEM contact)` 단위가 `GPa-`** 로 되어 있다 → **무차원 `-`**
· **PTFE 의 기하가 없다** — Methods 가 `centerline voxels of a PTFE fibril` 규약을 쓰므로
  **fibril 직경 행이 있어야** 그 규약이 정의된다
· `Calibrated` 각주가 표에 보이지 않는다.  문안:
  `Parameters marked "Calibrated" were adjusted so that the compacted packing reproduces
   the porosity and contact overlap measured for cold-pressed LPSCl.`

## Table S3 — 확정 상태

✅ 갱신됨: `Median CBD contacts 433/517` → **`Median CA contacts 74/86`** ·
`σ_ele 1.98/3.00 S cm⁻¹` → **`54.0/70.6 mS cm⁻¹`**(단위 포함) ·
`σ_ion 2.03/2.15×10⁻⁴` → **`5.53/5.58×10⁻⁴ S cm⁻¹`** · thickness **72.53** ·
porosity **7.86/7.37** · 제목 `DEM–MPM`.

★ **유효숫자는 `54.0 / 70.6` 으로 본문·표를 통일했다** (저자 결정).  8팔 산포가
1.3–1.7 % 라 3자리가 자기일관이다.  ⚠ **Figure 4b 가 `53.99/70.61` 이면 어긋난다 — 확인 필요.**

⚠ 남은 것 둘:
· **`VGCF coverage of AM 13.1 → 15.5 %` 라벨이 틀렸다** — 늘어난 2.4 %p 는 **SDCP 몫**이고
  VGCF 함량은 두 전극이 같다.  대시보드도 `도전재덮임`(conductive additive) 이다.
  ⇒ **`CA coverage of AM`** 으로.  (바로 아래 행은 CBD → CA 로 이미 고쳤다.)
· **`Areal capacity 3.24/3.23 mAh cm⁻²`** 는 **NCM 비용량(mAh/g) 가정**을 품는다.
  편집 시트가 그것을 *"비용량 미상"* 으로 판정했으므로 **어떤 비용량을 썼는지** 각주 필요.

## Figure S16 — 캡션 권고

현재: `Constructed SBE and DBE geometries used for the DEM-MPM simulations.`
(첨가제 상만 보이고 NCM·LPSCl 은 안 보인다 · 척도 없음 · 같은 골격이라는 언급 없음)

권고:
```
Figure S16. Constructed SBE and DBE geometries used for the DEM-MPM simulations
(50 × 50 × 72.5 μm3), showing the additive phases only; the NCM and LPSCl particles are
omitted for clarity. Both geometries share the same DEM-generated AM/SE skeleton.
```
★ 마지막 문장이 **본문 ④(`differences arise solely from their binder phases`)를 그림으로
뒷받침**한다 — 지금은 그 연결이 없다.
