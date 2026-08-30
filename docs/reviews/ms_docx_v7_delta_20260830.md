# 공저자용 docx ↔ 리포 정본 대조 — 수정 목록 (2026-08-30)

> 대상: `docs/manuscript/Methods_simulation_v7_for_coauthors.docx`
> (사용자 업로드본과 **바이트 동일** — sha256 `24fc40d0…`, 47,902 B ⇒ 08-29 생성판 그대로다).
> 정본: `table_s3_data_20260827.md` · `ptfe_convention_prereg_20260829.md` ·
> `methods_simulation_v7_draft.md` · `si_caption_audit_20260829.md`.
>
> ⚠ 아래는 **문서가 틀렸다**가 아니라 **리포가 그 뒤로 앞서갔다**는 목록이다.
> 08-29 시점에는 전부 맞았다.

---

## 0. ⚠⚠ 구조적 원인 — 생성기가 정본을 **안 읽는다**

`scripts/build_methods_docx.py` docstring:

> *"The draft (`docs/manuscript/methods_simulation_v7_draft.md`) is the canon;
> this script only lays it out."*

**그렇지 않다.**  본문·해제조건·표가 전부 스크립트 안에 **하드코딩**돼 있고 `.md` 를 읽는
코드가 한 줄도 없다 (`read_text`/`open` 은 draft 를 안 연다).  ⇒ 둘이 이미 갈렸다:

| | draft.md | docx |
|---|---|---|
| 민감도 표 이름 | **Table S3c** | Table S3**b** |
| 본문 보고 형식 | **공칭 규약 값 하나** + 같은 문단에 대안 병기 | *"어느 쪽도 주 규약으로 지정하지 않고 동등한 두 sensitivity 점"* |

★ 이것은 `SELF-08`("스윕이 원고 **생성기**를 안 읽어 `.docx` 만 고친 수정이 내구적이지
않았다")과 **같은 결함의 거울상**이다 — 이번엔 생성기가 사실상 정본이고 `.md` 가 표류한다.
⇒ **아래 수정은 `.docx` 가 아니라 `build_methods_docx.py` 에 넣어야 내구적이다.**

---

## 1. ★ 가장 큰 것 — 보고 **형식**이 바뀌었다 (해제조건 ①)

docx 는 *"어느 쪽도 주 규약으로 지정하지 않고 **동등한 두 sensitivity 점**으로 적습니다"*
라고 쓰고, Full·Compact 두 판 모두 `reported as equivalent sensitivity points rather than
one primary result` 로 적는다.

**그 형식은 R11 A-1 이후 폐기됐다.**  경위(`ptfe_convention_prereg` §이후결정 · R11 A-1):

1. *"동등 병기"* 는 내가 제안한 형식인데, litdb 를 찾아보니 **그 형식의 출판 선례가 없다**.
   가장 가까운 Bazzoun 2025(같은 재료계·같은 LIGGGHTS)는 파라미터 민감도를 **별도 절**에
   싣고 본문은 **공칭값 하나**를 쓴다.  ⇒ 내가 지어낸 형식이었다.
2. ⇒ **본문 = 공칭 규약 값 하나**(centerline) · **Table S3c = 규약 민감도**.

**고칠 문장 (Full · Compact 양쪽)**

| 지금 | 고침 |
|---|---|
| `reported as equivalent sensitivity points rather than one primary result` | 본문은 centerline 값 하나로 서술하고, **같은 문단에** `PTFE omitted` 값을 병기하며, 규약 변화는 `Table S3c` 로 내린다 |
| (없음) | `selected for reporting, but not calibrated` 를 **명시** — 등록된 검사는 *"교정됐는가"* 를 물었고 답이 **아니오**(표현 부피 0.43, 밴드 [0.5, 2.0] 밖)였다 |

⛔ **쓰면 안 되는 여섯**(정본 = 같은 절): *"centerline 이 참값에 가깝다"* · *"부피를 더
그리니 전도가 더 맞다"* · *"실험에 더 가까워서 골랐다"* · *"부피 측정이 centerline 선택을
지지한다"* · *"0 % 보다 43 % 가 물리적으로 더 가깝다"* · *"centerline 이 더 현실적인
규약이다"*.  ⇒ 부피비는 *"어느 쪽이 교정됐나"* 를 잰 양이고, *"어느 쪽이 전도를 더 맞게
내나"* 는 **재지 않았다** (차단은 부피가 아니라 **연결 위상**을 따른다).

---

## 2. 해제조건 표 — 다섯 줄이 낡았다

| # | docx | 지금 | 근거 |
|---|---|---|---|
| ① | 해소 (동등 병기) | ✅ 해소이나 **형식이 다르다** — §1 | R11 A-1 |
| ④ | **미해소** — *"계산기에서 전송만 남았습니다"* | ✅ **해소** — 32팔 + `run_receipt` + `cohort_manifest` + `verdict_receipt` 커밋.  제3자가 리포만으로 판정기를 돌려 **1.307820 / 1.123672 재도출**, `out_sha256` 32/32 일치 | `docs/data/w4_ptfe_centerline_20260827/` · `w4b_ptfe_off_20260827/` |
| ⑤ | 진행 중 — *"구조 지표 다섯 행은 새 침대에서 다시 뽑아야"* | 🔵 **구조 지표는 측정·등재 완료** (§3).  남은 것은 σ_ion 한 행이고, 그것도 *"진행 중"* 이 아니다 (§4) | 원장 §10 · §6-1 |
| ⑦ | **미해소** — *"Figure 4b … 다시 그려야"* | ✅ **Fig 4b 재작도 완료** (두 규약 병기) / 🔵 **Fig 4a 후보 3/4** (08-30, 슬랩 택1만 남음) | 원장 머리말 · 인계 20260830 §2 |
| ⑧ | 부분 해소 — *"Figure S16–S18 캡션은 아직 감사하지 않았습니다"* | ✅ **전수 감사 완료** — 오귀속 **3곳** | `si_caption_audit_20260829.md` |

⇒ 머리말의 *"해제조건 8개 중 **4개가 남아** 있습니다"* 도 갱신 대상이다.

⚠ 다만 ④ 에 **한정어가 필요하다**: 커밋된 것은 **scalar decision-audit package** 이지
원자료가 아니다 (팔당 131 MB → 5.8 kB, 필드 해는 버렸다).  **솔버 재실행은 여전히 kgy
원본이 필요**하고 매니페스트에 `src_sha256` 만 남아 있다.  ⇒ *"판정은 재도출된다"* 는
맞고 *"원자료가 리포에 있다"* 는 **틀리다.**

---

## 3. Table S3 — **네 행은 값이 있다** (docx 는 대괄호)

| 행 | docx | 넣을 값 | 규약 (같이 안 적으면 인용 불가) |
|---|---|---|---|
| SE coverage of AM | `[미측정]` | **86.6 / 86.6 %** | **Tabor 밴드 0.26 µm**.  같은 침대에서 Hertz 65.7 · 복셀 인접 40.4 도 나온다 — **섞어 인용 금지**.  v6 의 86.7 을 재현한 규약이 Tabor 다 |
| VGCF coverage of AM | `[미측정]` | **13.1 / 15.5 %** | 첨가제 인접 복셀.  v6 의 13.0 / 15.4 재현 |
| Electronic connectivity | `[미측정]` | **100 / 100 %** | 26-연결 |
| Median CBD contacts per AM | `[미측정]` | **74 → 86 ea** | **전도성만 (VGCF + SDCP)**, 껍질 0.15 µm, **개체 수**(점 수 아님).  ⌐ 절연 바인더 포함 시 **80 → 88** |

⚠⚠ **접촉 수는 규약이 이득까지 바꾼다** — 전도성만이면 **+16.2 %**, PTFE 를
*"conductive binder domain"* 에 넣으면 **+10.0 %**.  본문이 이 수를 **기전 근거**로 쓰므로
규약을 함께 적지 않으면 못 쓴다.
⚠ **v6 의 `433 → 517` 은 재현되지 않는다** (절대값 5.8배 차).  v6 이 무엇을 셌는지 기록이
없다.  **방향과 상대 크기는 정합**(+16.2 % vs +19.4 %) ⇒ *"SDCP 가 AM 당 접촉을 늘린다"* 는
본문 주장은 유지되고 **절대 수치만** 규약과 함께 갱신된다.
⚠ `AM_P` 계열이 전부 0 인 것은 **결측이 아니라 모집단 부재**다 (이 침대의 NCM811 이 단일 크기).

★ 등급 주의: 이 넷은 **값의 기록**이지 σ_e 축처럼 리포에서 재도출되는 증거가 **아니다**
(입력 점구름·metrics JSON 이 kgy 에만 있다, 원장 §10-4).  원고는 그렇게 인용할 것.

---

## 4. Table S3 — **두 행은 사유가 틀렸다**

### σ_ion,eff — `[미측정 — 이온 전용 런 진행 중]`

⛔ **"미측정" 이 아니라 "쟀는데 못 쓴다"** 이고, **해제는 런 완주가 아니다.**
cohort 는 돌았고 비가 **1 보다 작게** 나왔는데 그것이 물리가 아니라 **입력 규약의 비대칭**이다:
SBE 의 바인더 1 wt% 가 전도 격자에 **한 셀도 없고**(`ptfe_cells_observed = 0`), DBE 에서만
SDCP 가 실재하면서 자기 자리의 전해질을 σ 가 **1/3** 인 상으로 바꾼다.  ⇒ 채우면
*"SDCP 가 이온 전도를 떨어뜨린다"* 를 싣는 셈인데 그것은 **모델이 바인더를 안 그린 결과**다.
**8팔이 다 나와도 같다.**

**고칠 사유**: `[not filled — the ionic cohort ran, but the two beds are not treated
symmetrically in the conduction grid; unblocked pending the pellet calibration that anchors
σ_ion(SDCP) and the binder ionic-blocking length]`

### Areal capacity — `[미측정 — 새 침대에서 재산출 필요]`

⛔ **재산출 문제가 아니라 성립 불가다.**  두 전극은 **같은 AM scaffold**(`n_AM = 1271` ·
`seed_AM_frac_pct = 45.68` 동일)를 쓰고 정지 두께도 같다(72.534 µm) ⇒ **면적 용량이 서로
다를 수 없다.**  SI v6 의 `3.11 / 3.07` 을 재현하는 비용량은 각각 **195.5 / 193.0 mAh g⁻¹**
— 즉 v6 의 두 값은 **같은 침대에 서로 다른 비용량을 곱한 것처럼** 보인다.

면적 하중은 산술만으로 확정됐다: `0.4568 × 72.534 µm × 4.8 g cm⁻³ = **0.015904 g cm⁻²**`
(양 전극 동일).  **여기 곱할 비용량이 원고 어디에도 없다.**

**고칠 사유**: `[n/a — both electrodes share the AM scaffold and the stop thickness, so the
areal loading is identical (0.015904 g cm⁻²); the specific capacity used in the v6 values is
not stated anywhere in the manuscript]` ⇒ **협업자 회신 대기.  추정해 적지 않는다 (§F1).**

---

## 5. 그 밖에

| 자리 | 고침 |
|---|---|
| `Table S3b (신설)` | **`Table S3c`** — draft.md 가 S3c 로 부르고 본문이 그 이름을 인용한다 |
| §5 서두 *"σ_ele 만 새 침대이고 나머지가 옛 침대이면 독자는 구별할 수 없습니다"* | **네 행은 이제 새 침대 실측**이므로 그 사유가 그 행들에는 더 이상 안 걸린다.  남은 두 행(σ_ion · areal)에만 적용 |
| ε_union 7.86 / 7.37 · thickness 72.53 | ✅ 정본과 일치 — 그대로 |
| σ_ele 네 수(72.3 / 81.3 / 54.0 / 70.6)와 비(1.124 / 1.308), spread·range | ✅ 정본과 일치 — 그대로 |
| Limitations 의 *"restoring the additive contacts … recovers about a fifth"* | ✅ A 트랙 h0(19.7 %)와 정합 — 그대로.  ⚠ *"binder-omitted 규약에서만 쟀다"* 한정어 유지 |

---

## 5-1. ★ Figure 4a 생성 경로 — **사용자가 확인해 줬다** (2026-08-30)

draft `methods_simulation_v7_draft.md` 가 이 항목을 ⛔ 로 막고 있었다:

> *"⛔ 다만 **v6 Fig 4a 의 생성 경로를 우리가 모른다** — 스타일을 맞출 수 없으므로
> 후보를 내고 협업자가 판단한다."*

**풀렸다.  v6 Figure 4a 는 DEM 웹앱의 3D 뷰어 산출물이다** (사용자 확인):

| 설정 | 값 |
|---|---|
| 도구 | DEM 웹앱 3D 뷰어 (`webapp/templates/single.html` → `/results/<case_id>/3d-data`) |
| 확대 | **≈ 2.25** |
| 스케일 기준 | **DBE 로 고정** (두 패널이 같은 프레임을 쓰도록) |

⇒ **재렌더 경로가 바뀐다.**  08-30 에 만든 matplotlib 산란 슬랩 후보(`/tmp/fig4a/*.png`)는
v6 과 **다른 도구**이고 스타일이 안 맞는다.  08-27 재압밀 침대를 **같은 뷰어·같은 설정**으로
다시 뽑는 것이 맞다.

⚠ 슬랩 택1 문제(과플롯)는 **그 후보에만** 걸린 문제라 이 경로에서는 사라진다.
그 측정(잉크% 동일 · 고유색 12~15배 차 ⇒ 두꺼운 슬랩 과플롯)은 **버리지 않고** 기록으로
남긴다 — 같은 산란 방식을 다시 쓸 일이 있으면 얇은 쪽(0.45–0.55)이다.

⚠ 남은 확인: 뷰어의 색이 **무엇을 칠하는가** (v6 캡션이 그것을 말해야 한다) · 두 패널이
같은 색 범위를 쓰는지.  `DBE 로 고정` 이 그 공동 스케일 규약이다.

---

## 6. 순서

1. **`build_methods_docx.py` 를 고친다** (docx 가 아니라).  §1 형식 · §2 다섯 줄 ·
   §3 네 행 · §4 두 사유 · §5 표 이름.
2. `--selftest` 에 **정본 대조**를 넣는다 — 구조 지표 네 행이 `table_s3_data` §10-1 과
   같은지 **읽어서 비교**.  지금은 두 곳에 같은 수를 손으로 적고 있어 또 갈라진다.
3. 재생성 → 공저자 배포.
4. ⚠ **비용량 하나만 받으면** areal capacity 행이 닫힌다 (§4).
5. **Figure 4a 는 웹앱 뷰어로 재렌더** (§5-1) — matplotlib 후보 경로는 접는다.
