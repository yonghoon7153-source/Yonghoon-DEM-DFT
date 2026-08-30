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
