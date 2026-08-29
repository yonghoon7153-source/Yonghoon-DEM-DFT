# 원고·SI v6 감사 — 시뮬레이션 절 (2026-08-29)

대상: 협업자 제공 `Manuscript v6.docx` · `Supporting Information v6.docx` (2026-08-29 수령).
⚠ 이 문서들은 **리포 밖**에 있어 `check_review_findings --ban-sweep` 이 **한 번도 검사하지
않았다**.  CLAUDE.md ④ 가 경고한 형태 그대로다 — *"정본은 밖으로 강제되지 않으면 새어나간다."*

---

## 1. ⛔⛔ [P1] 철회된 세대의 수치가 본문·SI·그림에 살아 있다

| 자리 | 내용 |
|---|---|
| 본문 §전송 (line 39) | *"the simulated effective σ_ele increases from **1.98 to 3.00 S cm⁻¹**"* |
| SI **Table S3** | `σele_eff  SBE 1.98 · DBE 3.00 S cm⁻¹` |
| **Figure 4b** | 위 값의 그림 |

이 쌍의 비는 **1.515** = 이득 **+51.5 %** ⇒ **CL-24 로 철회된 계열**이다 (vox 0.4 격자 산물).
현재 정본은 `table_s3_data_20260827.md`:

| 규약 | σ_e SBE | σ_e DBE | 이득 |
|---|---|---|---|
| PTFE **미표현** (§3) | 72.32 mS cm⁻¹ | 81.26 | +12.37 % |
| PTFE **차단** (§2) | 53.99 | 70.61 | +30.78 % |

★ **Methods 는 이미 새 규약을 적고 있는데 숫자만 옛것이다.**  본문 Methods(line 62)가
*"voxel edge of 0.15 μm"* · *"eight half-voxel grid-origin shifts"* 라고 적는데, 1.98/3.00 은
**vox 0.4 · σ_SDCP 250 세대**의 값이다 (자릿수부터 다르다: 0.054–0.081 vs 1.98–3.00 S cm⁻¹).
⇒ 방법과 결과가 **서로 다른 런**을 가리킨다.

⚠⚠ **그리고 우리 ban-sweep 은 이것을 못 잡는다.**  등록부에 있는 것은 파생 백분율
(`+52.0 %` 등)이고 **그것을 만드는 σ 쌍(1.98 / 3.00)은 패턴에 없다.**  ⇒ 철회된 주장이
**검사가 볼 수 없는 형태**로 문서에 남을 수 있다.  등록부에 σ 쌍을 추가해야 한다 (후속).

## 2. [P1] Methods 가 `standard error` 를 쓴다 — R8 Q1 이 철회한 표현

본문 line 62 끝:
> *"conductivity ratios are reported as the paired mean with its **standard error**."*

R8 Q1: 8 origin 은 같은 침대의 **완전한 {0,½}³ factorial** 이라 복제 오차 자유도가 **0** 이다
⇒ `sd/√8` 은 표준오차가 아니다.  A3 §2 가 이름을 고정했다 —
**deterministic origin-sensitivity guard** (결정론적 origin 민감도 가드).

**교체 문장** (제안):
> Ratios are reported as the mean over the eight prescribed origin phases, together with the
> spread across those phases and the observed range; the eight phases form a complete
> factorial of a single bed rather than independent replicates, so no standard error or
> confidence interval is implied.

## 3. MPM 은 **이미 본문에 있다** — 다만 표가 그것을 숨긴다

준희 요청 *"MPM 을 본문 script 에 넣으면 좋겠다"* 에 대해: **Methods line 62 에 이미 있다** —
*"using the DEM simulation to generate the particle packing and the **material point method
(MPM)** to resolve its plastic deformation."*

그런데 **왜 몰랐나** — 이름이 전부 DEM 으로 붙어 있다:

| 자리 | 현재 라벨 | 실제 |
|---|---|---|
| **Table S2** 제목 | *"Material parameters used for the **DEM** simulations"* | DEM + **MPM** + 복셀 솔버 파라미터가 섞여 있다 |
| Table S2 안 | `Young's modulus (MPM continuum) 1.53` · `Poisson's ratio 0.49` · `Yield strength 0.30` | **MPM** 항목인데 표 제목은 DEM |
| Table S2 안 | `Voxel edge length 0.15 μm` | **복셀 수송 솔버** 항목 |
| **Table S3** 제목 | *"…obtained from the **DEM** simulations"* | σ 는 **복셀 FV 솔버** 산출 |
| **Figure 4a** 설명 | *"**DEM**-reconstructed …"* | DEM 패킹 + MPM 압밀 |
| 본문 line 39 | *"reconstructed using a discrete element method (DEM)"* | 2단계인데 1개로 읽힌다 |

⇒ **세 도구를 이름으로 갈라야 한다** (CLAUDE.md frame[5]):
1. **DEM (LIGGGHTS)** — 강체구 패킹·접촉망
2. **MPM (GPU, von Mises)** — SE 소성 변형을 고정 DEM 골격 위에서
3. **복셀 유한체적 솔버** — 위 미세구조 위에서 ∇·(σ∇φ)=0

Table S2 를 **세 블록**으로 나누고 제목을 *"Material and numerical parameters used for the
DEM–MPM–voxel transport workflow"* 류로 바꾸는 것이 최소 수정이다.

## 4. E 연화 서술 — 사용자 요청("영률 얘기는 숨기고 porosity 타겟팅 느낌으로")

**현재 문장** (line 62):
> *"the contact E of LPSCl was **softened from the dense-material value of 24 GPa to 1.35 GPa**,
> which reproduces the ~10 % porosity and 11–12 % contact overlap reported for cold-pressed
> LPSCl at 300 MPa."*

★ **요청은 정당하고, 지금 문장은 실제로 순서가 거꾸로다.**  우리가 한 일은 **porosity 를
표적으로 보정한 것**이고 E_eff 는 그 **노브**다 (CLAUDE.md frame[2]).  강조를 표적으로 옮기는 것은
사실에 더 가깝다.

**제안 문장** (표적을 앞으로, 노브를 뒤로):
> The contact stiffness of LPSCl was **calibrated against the measured compaction response** —
> the ~10 % porosity and 11–12 % contact overlap reported for cold-pressed LPSCl at 300 MPa —
> since rigid-sphere contacts cannot reproduce the plastic flattening, particle rearrangement
> and grain-boundary sliding that densify sulfide powders.  The calibrated contact modulus
> (1.35 GPa) is therefore an **effective parameter that lumps those unresolved mechanisms**,
> not the dense-material modulus (24 GPa), which is retained for reference in Table S2.

⚠⚠ **여기가 선이다 — 넘으면 안 되는 것 셋**:
1. **1.35 GPa 를 "LPSCl 의 영률" 로 읽히게 두면 안 된다.**  Table S2 가 `(dense) 24` 와
   `(DEM contact) 1.35 Calibrated` 를 **둘 다** 싣고 있는 것은 옳다 — **그 행을 지우면 안 된다.**
2. **연화 배수(18×)를 숨기지 않는다.**  숫자 둘이 표에 나란히 있으면 독자가 스스로 본다 —
   본문에서 "18배" 를 반복하지 않는 것과 **감추는 것**은 다르다.
3. 같은 이유로 **MPM 의 ν = 0.49** 도 그대로 둔다 (전단만 연화, K 는 실물 유지).  그것이
   연화가 **어디에만** 걸렸는지를 보이는 항목이다.

⇒ **강조는 옮기되 사실은 다 남긴다.**  심사자가 "1.35 는 어디서 왔나" 를 물으면 표가 답한다.

## 5. Table S3 갱신 — 옛 값 vs 정본

| 항목 | SI v6 (옛) | 정본 (2026-08-27 침대) |
|---|---|---|
| Thickness | 72.48 µm | **72.53** µm |
| Porosity | 7.87 / 7.39 % | **7.86 / 7.37 %** ⚠ **라벨 필요**: `ε_union` — 시뮬레이션 기하 진단값이지 통상 전극 porosity 가 아니다.  실험 앵커(~15.6 %) 대비 **과압축** |
| σ_ele | 1.98 / 3.00 S cm⁻¹ | ⛔ **철회** → 규약별 병기 (§1 표) |
| σ_ion | 2.03 / 2.15 ×10⁻⁴ | ⚠ **재측정 필요** — 현행 런은 `LEAN=2`(σ_e 전용)라 이온을 안 푼다 |
| 나머지 (coverage · contacts · connectivity · areal capacity) | — | **미확인** — 새 침대에서 다시 내야 한다 |

## 6. 해야 할 일 (우선순위)

| # | 항목 | 상태 |
|---|---|---|
| 1 | 본문 §전송 + Table S3 + Fig 4b 의 σ 값 교체 (규약 병기) | **[P1] 미착수** |
| 2 | Methods 의 `standard error` → origin-phase spread | **[P1] 미착수** |
| 3 | Table S2 를 DEM / MPM / 복셀 세 블록으로 분리, 제목 수정 | 미착수 |
| 4 | E 연화 문장을 porosity-표적 순서로 (§4 제안문) | 미착수 |
| 5 | Table S3 나머지 항목 새 침대에서 재측정 (σ_ion 포함 — 이온 런 필요) | 미착수 |
| 6 | ban 등록부에 **σ 쌍**(1.98/3.00) 추가 — 파생 백분율만으로는 못 잡는다 | 미착수 |
| 7 | 원고·SI 텍스트를 리포에 두어 sweep 사정권에 넣기 (규칙 22e 가 `.docx` 를 이미 훑는다) | 협업자 합의 필요 |

⚠ **1·2 는 지금 상태로 투고하면 안 되는 사유**다.  1 은 철회된 값이고, 2 는 우리가
이미 철회한 통계 표현이다.
