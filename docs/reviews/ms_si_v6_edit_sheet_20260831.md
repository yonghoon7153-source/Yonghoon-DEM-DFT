# 원고·SI v6 수정 시트 — 그대로 적용 가능한 형태 (2026-08-31)

> **왜 이 문서가 있나.**  `ms_si_v6_audit_20260829.md` 가 고칠 것을 **진단**했지만 문장 단위
> 대체안이 흩어져 있어 워드에 옮기기 어려웠고, [P1] 두 건이 이틀째 **미착수**였다.
> 이 문서는 판단을 새로 하지 않는다 — 감사와 원장(`table_s3_data_20260827.md`)에 이미
> 확정된 것을 **찾을 문자열 / 바꿀 문자열** 로 편다.
>
> ⚠⚠ **대상 파일이 리포 밖에 있다** (`Manuscript v6.docx` · `Supporting Information v6.docx`,
> 협업자 제공).  그래서 `check_review_findings --ban-sweep` 이 **한 번도 검사하지 않았다** —
> CLAUDE.md ④ 가 경고한 형태 그대로다.  적용 후 두 파일을 리포에 넣는 것이 감사 항목 #7 이고
> 협업자 합의가 필요하다.  **넣기 전까지 이 시트가 유일한 대조 수단이다.**

---

## A. [P1] 철회된 세대의 σ 가 본문·SI·그림에 살아 있다

**무엇이 문제인가**: 실린 쌍의 비는 **1.515** (= +51.5 %) 이고 이것은 **vox 0.4 격자 산물**로
CL-24 가 철회한 계열이다.  자릿수부터 다르다 — 현재 정본은 `10⁻²` S cm⁻¹ 대이고 실린 값은
`10⁰` 대다.  ★ **Methods 는 이미 새 규약을 적고 있다** (*"voxel edge of 0.15 μm"* ·
*"eight half-voxel grid-origin shifts"*) ⇒ **방법과 결과가 서로 다른 런을 가리킨다.**

### A-1. 본문 §transport (v6 line 39)

| | |
|---|---|
| **찾기** | `the simulated effective σ_ele increases from 1.98 to 3.00 S cm⁻¹` |
| **바꾸기** | `the simulated effective σ_ele increases from 54.0 to 70.6 mS cm⁻¹ (a ratio of 1.308) with the binder's centerline voxels excluded from conduction; omitting the binder from the electronic grid instead gives 72.3 → 81.3 mS cm⁻¹ (1.124). The setting used here was selected for reporting but is not calibrated (Table S3c).` |

⚠ **단위가 S → mS 로 바뀐다** — 옮길 때 첨자까지 확인할 것.
⚠ 본문이 한 숫자를 쓰는 것은 **편집 결정**이고 그 사실을 문장 자신이 밝힌다.  사전등록의
PTFE 규약 판정(*"채택 안 함"*)은 그대로이며 **이 문장은 그것을 뒤집지 않는다.**

### A-2. SI Table S3 — σ 행

| 규약 | σ_e SBE | σ_e DBE | 비 |
|---|---:|---:|---:|
| PTFE omitted from the electronic grid | **72.32** mS cm⁻¹ | **81.26** | **1.123672** |
| PTFE centerline voxels excluded | **53.99** | **70.61** | **1.307820** |

⛔ **한 규약만 싣지 않는다.**  두 줄을 다 싣고 어느 쪽도 굵게 하지 않는다.
⛔ 옛 행(`1.98 / 3.00`)은 **지운다** — 병기하지 않는다 (철회된 값이다).

### A-3. Figure 4b

생성기가 이미 정본 수치로 재작도돼 있다: `python3 scripts/fig4b_sigma_conventions.py`.
캡션은 그 파일의 `CAPTION` 상수를 **그대로** 쓴다 (selftest 가 문구를 감시한다).

### A-4. ⚠ 후속 — 등록부에 σ 쌍을 넣어야 한다

ban-sweep 등록부에 있는 것은 **파생 백분율**이고 그것을 만드는 **σ 쌍 `1.98 / 3.00` 은
패턴에 없다.**  ⇒ 철회된 주장이 **검사가 볼 수 없는 형태**로 문서에 남을 수 있다.
(감사 항목 #6, 미착수.)

---

## B. [P1] Methods 가 `standard error` 를 쓴다 — R8 Q1 이 철회한 표현

**무엇이 문제인가**: 8 origin 은 같은 침대의 **완전한 `{0,½}³` factorial** 이라 복제 오차
자유도가 **0** 이다.  `sd/√8` 은 표준오차가 아니다.  즉 **우리가 하지 않은 통계를 했다고
적혀 있다.**

| | |
|---|---|
| **찾기** | `conductivity ratios are reported as the paired mean with its standard error` |
| **바꾸기** | `Ratios are reported as the mean over the eight prescribed origin phases, together with the spread across those phases and the observed range; the eight phases form a complete factorial of a single bed rather than independent replicates, so no standard error or confidence interval is implied.` |

⚠ 문서 전체에서 `standard error` · `SE` · `95 % CI` · `±` 를 **원고 표현으로** 쓴 자리를
전부 훑을 것.  숫자는 맞고 **이름만 낡았다** (A3 §2 가 고정한 이름 =
*deterministic origin-sensitivity guard*).

---

## C. Table S2 — 세 블록으로 나누고, σ 행을 재료 앵커와 분리

제목 *"Material parameters used for the **DEM** simulations"* 에 DEM + MPM + 복셀 솔버
파라미터가 섞여 있다.  행 사양은 **`ms_si_v6_audit_20260829.md` §3-1 에 확정**돼 있다.

| | |
|---|---|
| **제목 찾기** | `Material parameters used for the DEM simulations` |
| **제목 바꾸기** | `Material and numerical parameters used for the DEM–MPM–voxel transport workflow` |

블록: ① DEM (LIGGGHTS) ② MPM (von Mises) ③ 복셀 수송 솔버.
★ ③ 안에서 **재료 앵커**(`σ_ion(SE)`)와 **유효 상 전도도**(`σ_e(VGCF)` · `σ_e(SDCP)`)를
다시 가른다 — 복셀 격자가 닿은 셀을 융합해 접촉저항을 표현하지 않으므로 뒤 둘은 물성이
아니다 (CL-47 · 원장 §15).  `σ_SDCP = 250` 은 `Assumed` 가 아니라
**`Effective (convention-dependent); provenance unrecorded`** 로 적는다.

⛔ `E (dense) 24` 와 `E (DEM contact, calibrated) 1.35` 행을 **둘 다 남긴다** — 지우면 연화
배수를 감추는 것이 된다.  MPM `ν = 0.49` 도 남긴다 (연화가 **전단에만** 걸렸음을 보이는 항목).

---

## D. E 연화 문장 — 표적을 앞으로, 노브를 뒤로

지금 문장은 순서가 거꾸로다 (노브를 먼저 말한다).  우리가 한 일은 **porosity 를 표적으로
보정한 것**이고 `E_eff` 는 그 노브다 (frame[2]).

| | |
|---|---|
| **찾기** | `the contact E of LPSCl was softened from the dense-material value of 24 GPa to 1.35 GPa` |
| **바꾸기** | `The contact stiffness of LPSCl was calibrated against the measured compaction response — the ~10 % porosity and 11–12 % contact overlap reported for cold-pressed LPSCl at 300 MPa — since rigid-sphere contacts cannot reproduce the plastic flattening, particle rearrangement and grain-boundary sliding that densify sulfide powders. The calibrated contact modulus (1.35 GPa) is therefore an effective parameter that lumps those unresolved mechanisms, not the dense-material modulus (24 GPa), which is retained for reference in Table S2.` |

⛔ **넘으면 안 되는 선 셋**: ① `1.35 GPa` 를 "LPSCl 의 영률" 로 읽히게 두지 않는다
② 연화 배수를 **숨기지 않는다** (표에 두 숫자가 나란히 있으면 독자가 스스로 본다 —
본문에서 반복하지 않는 것과 감추는 것은 다르다) ③ MPM `ν = 0.49` 를 지우지 않는다.

---

## E. Table S3 나머지 행 — 새 침대 값으로 교체

| 행 | v6 (옛) | 정본 (2026-08-27 침대) | 근거 |
|---|---|---|---|
| Thickness | 72.48 µm | **72.53** µm | 원장 §5 |
| SE coverage of AM | 86.7 % | **86.6 / 86.6** % | 원장 §10-1 (**Tabor 밴드 0.26 µm**) |
| VGCF coverage of AM | 13.0 / 15.4 % | **13.1 / 15.5** % | 원장 §10-1 |
| Electronic connectivity | — | **100 / 100** % | 26-연결 |
| Conductive-additive contacts per AM | 433 → 517 | **74 → 86** (+16.2 %) | 원장 §10-3, `cbd_contacts_per_am.py` |
| Porosity | 7.87 / 7.39 % | **7.86 / 7.37** % | ⚠ 라벨 필수 — `ε_union`, 통상 전극 porosity 가 **아니다** |
| AM+SE seed-sphere void | (없음) | **11.8471 / 11.8471 %** | 원장 §16 |
| Areal loading | — | **0.015904 / 0.015904** g cm⁻² | 원장 §10-1 |
| Areal capacity | — | **n/a** | 비용량 미상 (§10-5) |
| σ_ion | 2.03 / 2.15 ×10⁻⁴ | ⚠ **보류** | STEP B 판정 대기 |

### E-1. ⛔ 접촉 수는 규약을 **함께** 적지 않으면 인용 불가

`433 → 517` 은 웹앱의 **가중 점 수**이고 `74 → 86` 은 **개체 수**다 (굵은 섬유 하나 = 접촉 1).
5.8 배 차이의 정체가 그것이다 — 틀린 값이 아니라 **다른 양**이다.
정본 규약 = *"AM 구 표면 바깥 0.15 µm 껍질 안의 첨가제 물질점이 속한 **서로 다른 개체 수**"*.

★ 그리고 **PTFE 를 전도성 도메인에 넣느냐가 이득을 바꾼다**: 전도성만 74→86 (**+16.2 %**) ·
절연 바인더 포함 80→88 (+10.0 %).  본문이 이 수를 기전 근거로 쓰므로 규약을 명시할 것.
접촉이 0 인 AM 은 **양 침대 모두 0 / 1271**.

### E-2. ⚠ 두 porosity 행은 **다른 규약**이다 — 섞어 읽히면 안 된다

`ε_union` (7.86 / 7.37 %) 과 `ε_sphere` (11.8471 %) 는 분자 규약이 다르다 (겹침 차감 유무 ·
첨가제 포함 여부).  차 ≈ 4.4 %p 의 분해는 **아직 검증하지 않았다**.  나란히 적을 때 두
규약임을 반드시 밝힌다.

### E-3. ★ `ε_sphere` 행은 두 전극을 **가르지 않는다**

scaffold CSV 의 SHA 가 SBE·DBE 에서 **동일**하다 (`6184147f…` AM · `9f2529a0…` SE) = 같은
골격에 첨가제만 다르다.  두께도 같다.  ⇒ 면적 하중 행과 같은 성격 — **"동일하게 통제된 축"**
으로 적는다.  차이를 시사하는 자리에 놓으면 오독을 부른다.

---

## F. Figure 4a 캡션 — 뷰어 숫자를 쓰지 않는다

⛔ 뷰어의 `438 → 522` (그리고 v6 의 `433 → 517`)는 **철회**다: `d ≥ r` 하한이 없고, 개체가
아니라 **점**을 세며(점 목록을 복제하면 값이 2배가 된다), 6.3 % 부표본이다.
✅ 대체 = **`74 → 86` (+16.2 %)**, 0.15 µm 껍질·도전상만·개체 단위·전수.

⚠ 뷰어에서 뽑은 컬러바 PNG 를 쓸 때는 **2026-08-31 이후 판**이어야 한다 — 그 전 판은
제목이 `weighted contacts per AM` 이고, 그것이 그림 안에서 철회된 해석을 되살린다
(ban-sweep 은 PNG 속 글자를 못 읽는다).

---

## G. 이름 — DEM 이 아닌 것을 DEM 이라 부르는 자리 3곳

| 자리 | v6 | 실제 |
|---|---|---|
| Table S2 제목 | *"… the **DEM** simulations"* | DEM + MPM + 복셀 솔버 |
| Table S3 제목 | *"… obtained from the **DEM** simulations"* | σ 는 **복셀 FV 솔버** 산출 |
| Figure 4a 설명 | *"**DEM**-reconstructed …"* | DEM 패킹 + **MPM 압밀** |

세 도구를 이름으로 가른다 (frame[5]): **DEM (LIGGGHTS)** 패킹·접촉망 /
**MPM (GPU, von Mises)** 고정 DEM 골격 위의 SE 소성 / **복셀 유한체적 솔버** ∇·(σ∇φ)=0.

---

## 적용 순서

1. **B** (한 문장, 위험 0) → 2. **A-1 · A-2** (수치 교체) → 3. **E** (표 행) →
4. **G** (제목) → 5. **C · D** (표 재구성 · 문장 재배열) → 6. **A-3 · F** (그림 재생성)

⚠ 적용 후 반드시: 두 docx 를 리포에 넣고 `python3 scripts/check_review_findings.py`
(ban-sweep 이 `.docx` 를 훑는다).  **넣지 않으면 다음 세대에서 같은 누수가 반복된다** —
그것이 이 감사가 발견한 것 자체다.

---

## H. ⚠ 리포가 **두 보고 형식을 동시에** 말하고 있다 — 저자 결정 필요 (2026-08-31 발견)

이 항목은 v6 docx 가 아니라 **우리 쪽**의 미해결이다.  원고를 고치기 전에 정해야 한다 —
안 정하면 docx 를 어느 형식으로 고칠지가 정해지지 않는다.

### H-1. 경위

| 판정 | 형식 |
|---|---|
| **R10 재판정 1** | 두 규약을 **동등하게** 싣고 어느 쪽도 primary 로 지정하지 않는다 |
| **R11 A-1** (이후) | ⛔ 위 형식 **폐기**.  본문 = **공칭 하나**(centerline) + 같은 문단에 대안 병기, 규약 변화는 **Table S3c** 로 내린다 |

R11 A-1 의 근거: *"동등 병기"* 는 우리가 제안한 형식인데 **litdb 에 그 형식의 출판 선례가
없었다.**  같은 재료계·같은 LIGGGHTS 인 Bazzoun 2025 는 파라미터 민감도를 **별도 절**에 싣고
본문은 공칭값 하나를 쓴다.

### H-2. 지금 상태 — 같은 파일이 두 형식을 말한다

| 자리 | 문자열 | 형식 |
|---|---|---|
| `build_methods_docx.py:135` (Methods Stage 3) | `reported as equivalent sensitivity points rather than one primary result` | **옛 (R10)** |
| `:167` (Values paragraph) | `reported as two equivalent model-form sensitivity points` | **옛 (R10)** |
| `:221` (Compact) | `reported as equivalent sensitivity points` | **옛 (R10)** |
| `MAINTEXT_EDITS` | `One nominal setting in the body …` | **새 (R11 A-1)** |
| `fig4b_sigma_conventions.py:42` (캡션) | `shown as equivalent sensitivity points rather than one primary result` | **옛 (R10)** |

⚠ 135 는 `ms_docx_v7_delta` §1 이 **문자열 대 문자열로 지목해 고치라고 한 바로 그것**인데
그대로다.  2026-08-31 에 캡션·Values 에 *"본문이 centerline 을 쓰는 것은 편집 결정"* 이라는
문장을 얹었지만, 그것은 **모순을 덮은 것이지 푼 것이 아니다.**

### H-3. 갈래 (저자가 고른다)

- **㉠ R11 A-1 대로 정리** — 본문·Methods 를 공칭 형식으로 통일하고, 그림 캡션은 "여기가
  민감도 자리" 임을 명시한다.  ⇒ 선례 있는 형식.  `fig4b` selftest 의
  `rather than one primary result` 검사를 **캡션 문맥에 맞게** 고쳐야 한다.
- **㉡ 그림만 동등 병기, 본문은 공칭** — 실질적으로 ㉠ 과 같고 문구 정리 범위만 작다.
- **㉢ R10 형식 복귀** — 본문도 동등 병기.  ⚠ 그러면 R11 A-1 의 선례 조사 결과를 **뒤집는
  것**이므로 그 사유를 원장에 적어야 한다.

⛔ 어느 갈래든 **금지 표현 여섯**은 그대로다 (`ptfe_convention_prereg` §이후결정):
*"centerline 이 참값에 가깝다"* · *"부피를 더 그리니 전도가 더 맞다"* · *"실험에 더 가까워서
골랐다"* · *"부피 측정이 centerline 선택을 지지한다"* · *"0 % 보다 43 % 가 물리적으로 더
가깝다"* · *"centerline 이 더 현실적인 규약이다"*.

⛔ 그리고 **사전등록 판정(*"채택 안 함"*)은 어느 갈래에서도 뒤집히지 않는다.**  본문이
centerline 을 쓰는 것은 **편집 결정**이고, 그 사실을 문장 자신이 밝혀야 한다
(`selected for reporting, but not calibrated`).

### H-4. ⚠ 그리고 구조적 원인이 따로 있다

`build_methods_docx.py` docstring 은 *"draft(.md)가 정본이고 이 스크립트는 배치만 한다"* 고
적지만 **사실이 아니다** — 본문·표가 전부 스크립트에 하드코딩돼 있고 `.md` 를 읽는 코드가
한 줄도 없다.  ⇒ 어느 갈래를 고르든 수정은 **`.docx` 가 아니라 생성기에** 넣어야 내구적이다
(`SELF-08` 의 거울상).

---

## I. Abstract 문장별 판독 — 저자와 함께 (2026-08-31)

문장을 하나씩 읽고 **우리 모델이 무엇을 말할 수 있고 무엇을 말할 수 없는지** 가른 기록.
결정은 저자가 했고 이 절은 그 결과다.

| | 문장 | 판단 |
|---|---|---|
| S1 | 건식 공정 = 지속가능 경로 | 통과 |
| S2 | PTFE 의 세 결점 | **배경·문헌 — 우리 모델 밖.** 넘어감 |
| S3 | SDCP 도입 | DFT 는 DFT 브랜치. ⚠ σ_SDCP 라벨만 조치 (C) |
| **S4** | 1 wt% 고정, PTFE→SDCP 부분 치환 | ★ **우리 데이터가 착지하는 문장** — 아래 I-1 |
| S5 | 집전체 SDCP–그래핀 코팅 | post-cycling 앵커를 **소비**하는 쪽.  넘어감 |
| S6 | 성능 수치 (4C · 1000 cyc · 파우치) | **순수 실험.** 넘어감 — 단 전역 플래그 둘 (I-3) |
| **S7** | general design principle | ★ **비어 있는 자리** — 아래 I-2 |

### I-1. S4 — 말할 수 있는 것 / 없는 것

**전제**: SBE = PTFE 1.0 wt% · DBE = PTFE 0.5 + SDCP 0.5 — 실험의 치환을 그대로 재현한다.
두 침대가 **같은 DEM AM+SE 입력 골격**을 쓴다 (scaffold CSV SHA256 동일: AM `6184147f…` ·
SE `9f2529a0…`) ⇒ AM 패킹이 정확히 통제됐다.  **원고에 이 문장이 없다 — 넣으면 강해진다**
("두 전극이 정말 같은 미세구조냐" 에 해시로 답할 수 있다).

⚠⚠ **정정 (2026-08-31, 저자 지적으로 발견)** — 이 세션 초판은 위 해시를 근거로
*"바인더 교체의 기계적 결과가 골격에 반영되지 않았다"* 고 적었다.  **틀렸다.**
· 동일한 것은 **DEM 입력 골격**이지 압밀 결과가 아니다 (`am_scaffold.csv` 는 LIGGGHTS 덤프 =
  MPM 의 **입력**, AM 은 고정 격자 장애물).
· **첨가제는 MPM 물질점이 맞다** — `mpm3d_compaction.py` Stage 1 이 VGCF/SuperP/PTFE/SDCP 를
  각자의 (µ, λ, σ_y) 로 append 한다 (ADD_E_SET: PTFE 1.80 · SDCP 9.00 GPa).
· 압밀 결과는 **실제로 다르다**: porosity 7.86 vs 7.37 % · `input_digest` 04b5a565… vs d1022e09…
· ⇒ AM 이 고정인 것은 **frame[5] 설계 결정**(연속체가 강체 점접촉을 못 그린다)이지 바인더를
  무시해서가 아니다.
· ⇒ 따라서 `ε_sphere` 11.8471 % 가 양쪽 같은 것은 **독립 증거가 아니다** — 같은 입력 +
  같은 정지 두께의 산술이고, 게다가 §16-2 대로 **첨가제 고체부피를 안 센다**.
  "두 전극이 같다" 의 근거로 쓰면 순환이다.

**C2 (electronic transport) = 우리 것** — 값 + 기전:
σ_e 72.32→81.26 (+12.4 %, PTFE 미표현) · 53.99→70.61 (+30.8 %, PTFE 차단), 8팔 factorial.
AM 당 도전성 첨가제 접촉 **74 → 86** (+16.2 %, 개체 수, 껍질 0.15 µm).
★ **전자 연결성이 양쪽 100 %** 이고 접촉 0인 AM 이 양쪽 0/1271 ⇒ 이득은 **퍼콜레이션이 아니라
망 굵기**다.  원고가 "percolation" 서사를 쓰면 우리 데이터와 어긋난다.

**C1 (fibrillar framework) · C3 (cohesion) · C4 (resilience)** — **저자 결정: 우리 모델의
목적성 밖.**  ⇒ 실험 근거로만 서고, **Methods·SI 가 시뮬레이션이 뒷받침하는 것처럼 읽히게
두지 않는다** (같은 문단에 묶이면 그렇게 읽힌다).
⚠ 막는 이유는 "골격 고정" 이 아니라 **응집력·회복탄성 판독기가 파이프라인에 없다**는 것이다
(초판의 이유 서술은 위 정정으로 무효).

### I-2. S7 — 전자축 design principle 세 문장이 **비어 있다**

*"general design principle"* 은 일반화 근거를 청구하는데 우리 침대는 레시피 한 쌍이다.
그런데 **전자 축에 대해서만은 실제로 있다**:

1. **이득의 출처가 갈렸다** (CL-44/45, 두 격자에서 h1) — 새 도체 **부피**가 주된 원천
   (93.6 % @vox 0.15 · 69.6 % @vox 0.4), σ-치환은 소수 지분.
   ⇒ *"이미 있는 것의 전도도를 올리는 것"이 아니라 **"도전 부피를 더하는 것"**이 이득을 산다.*
2. **문턱 효과가 아니다** — 연결성 양쪽 100 %, 접촉 0인 AM 양쪽 0.  망을 **굵히는** 이야기다.
3. **σ_SDCP 감도가 열등선형(포화)** (CL-11 5점 스윕) ⇒ σ_SDCP 가 2배 틀려도 이득이 2배로
   안 움직인다.  *더 전도성 좋은 폴리머보다 **부피·분산**이 레버다.*
   ⚠ 스윕 **절대값은 vox 0.4 계열이라 인용 금지** — **모양만** 말한다.

⚠ 일반화 한계도 같이: 레시피 한 쌍 · 침대 하나 · 격자 미수렴 축에서 하한 · 3 mAh cm⁻² 급.

### I-3. ⚠ 전역 플래그 둘 — abstract 밖에서 되살아난다

S6 을 넘어가는 것은 거기 우리 것이 하나도 없기 때문이고, 아래 둘은 **본문 어디서든 우리 σ 를
셀 성능 옆에 놓는 순간** 다시 걸린다:

- **㉠ 다른 전극이다.**  모델 침대 면적하중 0.015904 g cm⁻² (원장 §10-1, areal capacity **n/a**),
  캠페인 라벨 3.18 mAh 계열 ⇒ **3 mAh cm⁻² 급**.  abstract 헤드라인은 **5 mAh cm⁻² 파우치**다.
  두께·하중이 다르면 수송 병목이 다르다.  ⇒ *"시뮬레이션이 이 성능을 설명한다"* 로 읽히는
  배치를 피한다.  정직한 배치 = **시뮬레이션은 기전, 실험은 성능**이고, 같은 기전이
  스케일업에서도 작동한다는 것은 **주장이지 우리가 보인 것이 아니다**.
- **㉡ STEP4 rate 값은 세대가 다르다.**  2C CCCV 결과(CC끝 81.5→83.0 %, ΔV 9.3 mV =
  옴 4.5 + 반응 4.8)는 **W2 재압밀 이전** 침대다.  현재 σ 런은 전부 `--no-step4` 라 새 침대에서
  STEP4 를 돌린 적이 없다.  ⇒ 새 σ 와 **같은 표·같은 문단에 넣지 않는다** —
  week_plan §0 이 잡은 세대 불일치(S2 는 새 세대, S3 은 옛 세대)와 **같은 부류**다.
  인용하려면 새 침대 STEP4 재실행이 선행이다.

### I-4. ⚠ 확인 요청 — 집전체가 Al 인가 SUS 인가

abstract 는 *"stainless steel current collector"* 인데 우리 앵커 라벨은 **`bare-Al`** 이다
(원고 Fig 6e 앵커: bare-Al SBE 110 · DBE 46 · C-SUS 30 Ω·cm²; 벌크 R ≈ 0.002 ⇒ 계면이
**5만 배** 병목).  갈래 셋:

| | | |
|---|---|---|
| ⓐ | 기준이 Al 인데 abstract 가 SUS 로 적힌 것 | abstract 오기 |
| ⓑ | 실험이 Al → SUS 로 바뀌고 앵커 라벨이 낡은 것 | 코드 라벨 수정 |
| **ⓒ** | 대조가 **bare-Al vs C-SUS** 라면 | ⚠⚠ **금속과 코팅을 동시에 바꾼 교락** |

ⓒ 면 *"코팅이 계면을 개선했다"* 가 안 선다 (대조군이 다른 금속이다).  SR-01 게이트⑤ 2×2 가
같은 함정이었다.  리포에 **`sus` 시나리오(코팅 없는 SUS, 실측 50 / 투영 150)** 가 따로 있어
`bare-SUS vs C-SUS` 라는 옳은 대조가 가능하다 — 실험이 어느 쌍을 쟀는지 확인이 필요하다.

⚠ 그리고 `csus` 앵커는 코드가 스스로 `SBE_CSUS_{:g}_proxy_DBE_anchored` 로 라벨한다 =
**SBE + C-SUS 조합은 실측이 없다** (DBE 앵커로 채운 proxy).  그 조합을 실으면 밝혀야 한다.
⚠ **그래핀은 기하로 모델에 없다** — primer 는 면저항 한 숫자(σ 1.3e4 S/cm × 200 nm)로만
들어간다.  층 내부 기전은 실험 소관이다.

### I-5. 이 판에서 확정된 행동 항목

| # | 항목 | 상태 |
|---|---|---|
| 1 | `standard error` → origin-phase spread (항목 B) | **저자 승인** — methodology 패스에서 적용 |
| 2 | σ_SDCP 라벨 = 유효 상 전도도 · provenance unrecorded (항목 C) | 코드 ✅ · docx 미착수 |
| 3 | 3 mAh cm⁻² 모델 ↔ 5 mAh cm⁻² 파우치가 다른 전극임을 명시 | 미착수 |
| 4 | S7 에 전자축 design principle 3문장 (I-2) | 미착수 |
| 5 | 집전체 Al/SUS 확인 (I-4) | **저자 확인 대기** |
| 6 | S4 에 골격 해시 문장 추가 (같은 DEM 입력 골격) | 미착수 |
| 7 | "percolation" 서사가 있으면 "망 굵기" 로 정정 | 미착수 |

### I-6. ★ 소유자 분리 — **저자 담당은 모델 절뿐이다** (2026-08-31 저자 확정)

abstract 본문·실험 서사는 **공저자와 함께 검증된 부분**이라 손대지 않는다.  저자 몫은
강준희 지시대로 **DEM/DFT methodology + table 을 별도 파일**로 내는 것이다.
⇒ 위 항목을 소유자별로 다시 가른다.

| 소유 | 항목 |
|---|---|
| **저자 (모델 절 · Table S2/S3 · Fig 4a/4b)** | 1 `standard error` 교체 · 2 σ_SDCP 라벨 · 6 골격 해시 문장 · 7 percolation→망 굵기 · 4 전자축 design principle 3문장 · ㉡ STEP4 세대 + 전극 스펙 명시 |
| **공저자 (질문만 넘긴다, 고치지 않는다)** | 5 집전체 Al/SUS 교락 여부 · 3 본문이 3 ↔ 5 mAh cm⁻² 를 잇는 배치인가 |

**공백의 두 종류** — 섞으면 안 된다:

- **㉠ 남의 주장의 공백** (agglomeration · cohesion · resilience · 1000 cyc · 파우치):
  저자 책임이 아니다.  ⚠ **다만 하나는 지킨다** — 그 주장들이 우리 시뮬레이션과 **같은
  문단에 묶이지 않게** 한다.  묶이면 우리가 뒷받침한 것처럼 읽힌다.
- **㉡ 우리 모델이 내야 하는데 아직 없는 것** — 이것이 진짜 우리 공백이다:

| | 공백 | 상태 |
|---|---|---|
| a | **바인더망 자체의 연결성 지표** — PTFE 를 절반 빼면 그 망이 끊기는가 | ⛔ 없다.  세울 수 있다 (바인더상만 연결성분) |
| b | 새 침대 STEP4 (rate 를 새 세대로) | ⛔ 미실행 — 현재 런은 전부 `--no-step4` |
| c | σ_ion 한 행 | 🔵 STEP B 판정 대기 |
| d | SDCP E_bind DFT | DFT 브랜치 |
| e | **σ_SDCP = 250 의 출처** (캐스트 필름인가 압착 펠릿인가) | ⛔ 기록 없음 |

★ **e 가 제일 싸고 제일 위험하다.**  아는 사람에게 묻는 것으로 끝나는데, **펠릿값이면
압착으로 좋아진 접촉이 이미 그 값에 들어 있고 우리는 그 기하를 복셀로 또 그린다** =
같은 효과를 두 번 세게 된다 (원장 §15-1).

⚠ 저자 결정: ① 격자 미수렴 · ② 접촉저항 부재 · ③ 절대값 미교정 은 **원고에 적지 않는다**
(내부 인지 사항).  ⚠ 다만 ②는 집전체 R_int 절이 *"바닥 판이 완전 접촉이라 σ_e_eff 는 벌크 망
값"* 이라는 전제 위에 서 있으므로, 그 절을 쓸 때 한 구절이 필요해질 수 있다 — 그 자리에서 재검토.

---

## J. Table S2 실물 판독 — 밀도 부재 · σ_SE 불일치 (2026-08-31, v6 SI 텍스트 추출)

### J-1. ρ_SDCP 는 **원고에 없다**

Table S2 에 **밀도 열 자체가 없다** (PTFE·SDCP·LPSCl 전부).  코드 주석
(`additives.py:25` — *"REPLACE with the user's manuscript value"*)이 기대한 값이 **문서에
존재하지 않는다.**  ⇒ `ρ_SDCP = 1.30` 은 generic PEDOT 문헌값으로 남는다.

⚠⚠ **그런데 이 값이 σ_ion 비의 부호를 정한다** (2026-08-31 발견):

```
SBE  PTFE 1.0            바인더 부피 0.4545
DBE  PTFE 0.5 + SDCP 0.5             0.6119  = SBE 의 1.346배
     ⇒ 같은 1 wt% 인데 DBE 가 SE 를 34.6 % 더 밀어낸다 (ρ 2.2 vs 1.3)

ρ_SDCP = 1.1 → 1.500배 · 1.3 → 1.346 · 1.7 → 1.147 · 2.2 → **1.000 (페널티 소멸)**
```

모델 안에서 두 항이 싸운다 — ① SDCP 가 이온을 통과시킨다(r>0, DBE 유리)
② SDCP 부피가 커서 SE 를 밀어낸다(DBE 불리).  그래서
`r 0.0184 → R 0.980` · `0.1737 → 0.997` · `0.3333 → 1.008` 로 **부호가 r 과 ρ 에 함께 걸린다.**
⇒ **ρ_SDCP 실측이 GPU 0 시간짜리 최우선 항목이다.**

### J-2. ★ `Ionic conductivity` 칸이 **비어 있는 것은 옳다**

| SDCP 행 | 값 | 라벨 |
|---|---|---|
| Particle diameter | 0.30 µm | Measured |
| Young's modulus | 9.0 GPa | Measured |
| Electronic conductivity | 250 S cm⁻¹ | Calculated |
| **Ionic conductivity** | **–** | **–** |

원고가 σ_ion(SDCP) 를 **주장하지 않는다.**  우리 비식별 결론(STEP B h0 · D13 ρ-축퇴)과
정합하므로 **그 칸을 억지로 채우지 않는다.**

### J-3. ⛔ **Table S2 와 우리 런이 다르다** — ⚠ **정정: 표가 맞고 런이 틀렸다**

```
Table S2      LPSCl Ionic conductivity   3.0 × 10⁻³ S cm⁻¹   (Ref. S5)
STEP B 런                                3.57 × 10⁻³          (Fig 2f neat 펠릿)
                                          ↑ 19 % 차이
```

선언된 파라미터와 실행값이 다르다 — `week_plan` §0 이 잡은 세대 불일치와 **같은 부류**다.

⚠⚠ **2026-08-31 정정 (저자 지적)** — 초판은 *"Table S2 를 3.57 로 고쳐라"* 라고 적었다.
**틀렸다.**  `3.0 × 10⁻³ (Ref. S5)` 는 **DEM 생산 규약값이고 문헌 앵커**다.  어긋난 것은
**우리 런 쪽**이다: STEP B 가 `SIGMA_ION_SE=0.00357` 로 override 했다.

⚠ **그리고 그 override 를 저자가 결정하지 않았다.**  사전등록 §3 이
`--sigma-ion-se 0.00357 (Fig 2f neat, 전 시나리오 동일)` 이라고 **출처는 적었지만
Table S2 의 3.0 과 다르다는 사실은 안 밝혔다.**  등록했다는 것이 저자가 봤다는 뜻이 아니다.
동기는 있었다 — r-역산이 Fig 2f neat(3.57)에서 나왔으므로 `x = 6.2e-4` 가 `r = 0.1737` 이
되려면 σ_SE 도 3.57 이어야 한다 (3.0 에 6.2e-4 를 넣으면 `r = 0.2067` 로 **다른 시나리오**다).
D13 §3 이 그 셋을 나란히 적어 뒀는데 내가 하나를 고르고 **고른 사실을 표면화하지 않았다.**

★ **상주 규칙 (이 사고에서)**: 규약값(Table S2)에서 벗어나는 파라미터를 쓸 때는 사전등록에
*"이것은 Table S2 의 X 와 다르다"* 를 **명시**한다.  출처를 적는 것으로는 부족하다.

### J-3b. ★ 재실행 없이 정확히 환산된다

고정 기하의 선형 FV 에서 `A(σ)φ = b` 의 `A` 는 σ 에 선형이다.  모든 이온상을 `k` 배 하면
`A → kA` 이고 **φ 는 불변**, 전류가 `k` 배 ⇒ `σ_eff` 가 **정확히** `k` 배다 (근사가 아니다).

| | σ_SE 3.57e-3 | **σ_SE 3.0e-3 (Table S2)** | R |
|---|---:|---:|---:|
| SBE (r 무관) | 0.6586 mS cm⁻¹ | **0.5534** | — |
| DBE MG r=0.0184 | 0.6455 | 0.5425 | 0.980238 |
| DBE RSA r=0.1737 | 0.6567 | 0.5518 | 0.997162 |
| DBE PROD r=0.3333 | 0.6640 | 0.5580 | 1.008257 |

`k = 3.0/3.57 = 0.840336` (r 보존).  ★ **R 은 안 바뀐다** — 판정(h0)에 영향 없다.
펠릿-정합 σ_SDCP 를 생산 σ_SE 로 옮기면 `0.1737 × 0.003 = 5.21e-4 S/cm`.

⚠ 이것은 **유도값**이지 런 출력이 아니다.  원고에 실으려면 1팔로 확인한다
(`SIGMA_ION_SE=0.003 SIGMA_ION_SDCP=5.21e-4`, ~50분).  항등식이므로 어긋나면 그것이 발견이다.

### J-3c. ★★ 절대값이 실측의 4배다 — 원인은 미세구조가 아니라 σ_SE 기준

저자 지적(*"0.6 이거 높다"*)이 맞다.  같은 재료계 실측과 대조하면:

| | σ_ion,eff | 기준 σ_SE | **F = σ_eff/σ_SE** |
|---|---:|---:|---:|
| Bazzoun 2026 (LPSCl+NMC, f_CAM 70 wt%, EIS 400 MPa) | 0.137 mS cm⁻¹ | 1.02 (펠릿 실측) | **0.1343** |
| 우리 (Table S2 규약) | 0.5534 | 3.00 (Ref. S5) | **0.1845** |

절대값은 **4.0배** 차이지만 **F 로는 1.37배 — 자릿수 정합**이다.
⇒ **차이의 정체는 `σ_SE` 기준값 선택이다**: `3.00` 은 단결정급, Bazzoun 의 `1.02` 는
입계 포함 펠릿급.  복합 전극 안의 SE 는 입계가 있으므로 물리적으로는 펠릿급에 가깝다.
(원고 자신의 Fig 2f neat 는 3.57 로 Bazzoun 보다 3.5배 높다.)

★ **행동**: 원고에 σ_ion 절대값을 실을 때 **F 를 같이 적는다.**  심사자가 Bazzoun 을 알면
4배를 바로 짚고, F 가 있으면 그 자리에서 답이 된다.
⚠ 미확인: v6 의 0.203 이 실측에 더 가까워 보이는 것이 우연인지 — 그것은 vox 0.4 세대 값이고
격자 미수렴이 반대 방향으로 상쇄했을 가능성이 있다.

### J-3d. (구 권고 — 무효)

### J-4. ✅ VGCF 는 이미 두 값을 병기한다 — SDCP 도 같은 형식으로

| VGCF 행 | 값 | 라벨 |
|---|---|---|
| Electronic conductivity (compressed powder) | 1.0 × 10² S cm⁻¹ | Calculated |
| Electronic conductivity (**voxel, diameter-preserving**) | 78.5 S cm⁻¹ | Calculated |

★ 항목 C 가 요구한 *"유효 상 전도도(voxel-network convention)"* 구분이 **VGCF 에서는 이미
되어 있다.**  ⇒ `σ_e(SDCP) 250` 도 같은 형식으로 맞춘다.
⚠ 그리고 250 이 `Calculated` 로 적혀 있는데 우리 리포는 **출처 미기록**이라 적는다 —
누가 무엇을 계산했는지 확인이 필요하다 (원장 §15-1).

### J-5. 이 절이 만드는 행동 항목

| # | 항목 | 소유 |
|---|---|---|
| J-a | **ρ_SDCP 실측값 확보** — 부호가 여기 걸려 있다 | 저자/재료 담당 |
| J-b | Table S2 의 LPSCl σ_ion 3.0 → 3.57 (또는 런을 3.0 으로) | 저자 |
| J-c | σ_e(SDCP) 250 을 VGCF 형식으로 병기 + `Calculated` 근거 확인 | 저자 |
| J-d | σ_ion(SDCP) 칸은 **비워 둔다** (채우지 않는 것이 옳다) | — |

---

## K. PTFE 차단 보정 — **쓸 수 있는 최대 문안이 고정됐다** (2026-08-31, R18)

`codex_r18_verdict_20260831.md` 로 D13 의 PTFE 차단 축이 닫혔다.  두 연산자(부분부피 ·
브릿지 역이용)로 브래킷을 메우려던 시도가 **둘 다 기각**됐고 (원장 R18-1~3),
`UNREACHABLE` 이 그대로 유지된다.

### K-1. 이 축을 원고에서 **언급할 경우**의 최대 문안

⚠ 언급하지 않는 것도 선택지다 (저자 결정).  **언급한다면** 이 이상 주장하지 않는다:

> Within the preregistered 0.12-µm voxel binary EDT-shell representation, the PTFE-pellet
> target (0.97 mS cm⁻¹) fell between the two adjacent representable shell states
> (1.518 and 0.717 mS cm⁻¹, normalized to σ_SE = 3.57 mS cm⁻¹).  We therefore selected no
> blocking thickness and did not treat the PTFE correction as calibrated.  This deterministic
> bracket reflects operator resolution and model form; it is neither a confidence interval nor
> a bound on physical fibril size or conductivity.

### K-2. ⛔ 이 축에서 **쓰면 안 되는 표현**

| 쓰면 안 되는 것 | 왜 |
|---|---|
| 브래킷을 *"불확실 구간"* · *"상·하한"* 으로 부르기 | 물리량의 구간이 아니라 **인접한 두 표현 상태**다 (R18 Q7) |
| `b` 를 **피브릴 두께·직경**으로 해석 | `b` 는 이미 스탬프된 PTFE **바깥**의 유효 계면 거리다 (R18-1) |
| *"가까운 쪽(b=0.17)을 골랐다"* | 사전등록이 근접 선택을 금지했고 실제로 안 골랐다 |
| PTFE 보정을 **calibrated** 로 서술 | 표적에 도달하지 못했다 |

### K-3. 후속 (원고 밖)

**Q6 — 보존형 cut-cell / capsule face 연산자**가 유일하게 살아남은 경로다: 피브릴
**중심선 + 직경**에서 각 FV face 의 **열린 면적분율 α** 를 계산해 `G_face = α·G₀`.
국소적 · 방향 보존 · KCL 정합이고 **격자 원점을 바꿔 수렴을 직접 시험**할 수 있다.
코드에 `capsule` 예약 경로가 있다 (`scripts/mpm_webapp_payload.py:596`).
⚠ 셀을 찍는 규약이 아니라 **face 개구율**이라 피브릴이 복셀보다 얇아도 성립한다 —
`ptfe_convention_prereg` 의 `capsule`(참 직경 셀 스탬프)과 **다른 물건**이다.
⚠ 직경이나 `R_int` 를 다시 표적에 맞추면 그것도 calibration 이지 validation 이 아니다.
**이 논문 일정 밖.  새 사전등록 필요.**

| # | 항목 | 소유 | 상태 |
|---|---|---|---|
| K-a | 이 축을 원고에서 언급할지 결정 | 저자 | ✅ **2026-08-31 저자 결정 = 언급하지 않는다** |
| K-b | Q6 연산자 사전등록 — 이 논문 밖 | 다음 라운드 | 대기 |

### K-4. K-a 결정 기록 (2026-08-31)

**언급하지 않는다.**  근거 셋:
1. 이 계산에 기대는 숫자가 **원고에 하나도 없다** — 펠릿 RVE 는 전극과 별개로 만든 보정용
   계산이고, 본문의 전극 σ 는 거기서 나오지 않는다.  빼도 무너지는 문장이 없다.
2. Table S3 각주를 쓰지 않기로 한 저자 결정과 일관된다 (각주는 *실린* 숫자에 붙는 것이었고,
   이 축은 **실리지도 않은** 숫자다 — 더 선택적이다).
3. 도달하지 못한 보정은 결과가 아니다.

⚠ 다만 **성격이 다른 문장 하나**는 이 결정과 무관하게 살아 있다 — *"복셀 표현은 PTFE 의
부피 점유만 담고 표면 피복은 담지 않는다"* 는 **모델 범위** 서술이지 실패한 보정 얘기가
아니다.  심사자가 물으면 그때 한 문장으로 답한다 (우리에게 유리한 방향 — 그 축에서 이득이
보수적이라는 뜻이다).  §K-1 문안은 **쓰지 않되 폐기하지 않고** 이 문서에 남긴다.
