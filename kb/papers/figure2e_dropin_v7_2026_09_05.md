---
title: "원고 v6→v7 Figure 2e 드롭인 — 본문·캡션·Methods 교체안 (C-12 v36 설계 반영)"
date: 2026-09-05
updated: 2026-09-05
tags: [manuscript, figure2e, sdcp, adsorption, c12, citability]
status: 1저자 확인 대기
kind: manuscript-draft
system: sdcp
confidence: high
verificationStatus: verified
verifiedAt: 2026-09-05
verifiedBy: self
explored: false
authoredBy: agent
claimType: prescriptive
evidenceScope: multi-source-primary
---

# Figure 2e 드롭인 (v7)

> 대체하는 것: `kb/papers/dft_sentences_for_manuscript_v6_2026_09_04.md` §1·§4 ·
> `docs/manuscripts/methods_dft_v9_for_coauthors.md` §6 본문 ¶34 교체안
> 왜 대체하나: 그 둘의 **잡 설계 서술이 낡았다** — "twelve poses per species,
> four pre-registered and eight drawn from a stratified prospective holdout" 라고
> 적혀 있는데, 실제로 나간 것은 **C-12 v36 · 19잡**이고 구성이 다르다 (§0).

---

## 0. 먼저 — 실제로 나간 계산이 무엇인가 (v36 번들에서 직접 셈)

`runs/sdcp_c12_2026_08_30/sdcp_c12_v36.zip` 의 `job.json` 19개를 그대로 센 것이다.
**추정 아님.**

| kind | 개수 | 무엇 |
|---|---:|---|
| `prospective_pose` | 10 | 복합체(슬랩+조각) — 2 조각 × 2 자세 × 2 자기시드 = 8, + 진공수렴 짝 2 |
| `clean_ref` | 3 | 조각 없는 슬랩 — pm1 · net4, + 진공수렴 짝 1 |
| `mol_ref` | 6 | 상자 안 단분자 — 조각당 3 |
| **계** | **19** | 전부 static 단일점 |

- 조각: `sdcp_neutral` (술폰산기 EDOT 반복단위) · `ptfe_c10` (C₁₀F₂₂)
- 자세 역할: `primary` · `sensitivity`(ptfe) / `stress_sensitivity`(sdcp)
- 자기 시드: `afm2424_pm1` · `afm2424_net4`
- k-mesh: 슬랩 **3×4×1**, 단분자 **Γ**
- 셀: c = **36.6551 Å**, 진공수렴 짝은 **40.6551 Å**
- **v36 에서 늘어난 것**: `clean_ref` 3잡. 그래서 **각 조각의 절대 흡착에너지**도 낸다
  (v35 는 차만 냈다).

### 자세 스크린 (DFT 를 보기 전에 동결)

`db/properties/prospective_basins_2026_08_29.json` (freeze sha `94675e66…`) 에서 센 것:

| | ptfe_c10 | sdcp_neutral |
|---|---:|---:|
| 표면 자리 | 7 | 7 |
| 방향 | 12 (피보나치) | 13 (피보나치 12 + `sulfonate_down`) |
| roll | 4 (0·90·180·270°) | 4 |
| 후보 자세 | 336 | 364 |
| 기하 게이트 통과 | 112 | 109 |
| 구분되는 basin | **96** | **101** |

자리 7종: `Li_top` · `Ni_top` · `O_top` · `LiNi_bridge` · `LiO_bridge` · `NiO_bridge` · `hollow`

⛔ **E_pose(스크린 에너지)는 원고에 쓰지 않는다** — MLIP 값이고 `do_not_cite` 다.
스크린은 *"자세를 어떻게 골랐나"* 를 말할 때만 인용한다.

---

## 1. 본문 ¶34 — 삭제할 것

⛔ **삭제 1** (마감문서 `⛔_금지_서술` 에 글자 그대로 있다):

> *"The stronger interaction expected for SDCP originates from its polar sulfonate
> moieties, which can interact more effectively with exposed surface sites of
> LiNi₀.₈Co₀.₁Mn₀.₁O₂ (NCM811) than non-polar PTFE.[19]"*

근거였던 `O···Li 2.09 Å` 는 2026-08-29 철회다. 우리가 좌표를 직접 재봤다:
술포네이트 O ↔ 슬랩 Li **4.88–5.39 Å**(배위 아님), 실제 최근접 접촉은
**탄소결합 H ··· 슬랩 O/Ni 2.44–2.46 Å**. 술포네이트는 표면 근처에 있지도 않다.
⚠ 이 두 거리는 **legacy wave1 기하의 재판독**이라 본문에 넣을 값이 아니다 — 삭제 근거일 뿐이다.

⛔ **삭제 2** (자리표시자): *"Additional text related to DFT."*

---

## 2. 본문 ¶34 — 교체안 (영문, 그대로 붙여넣기)

빈칸은 **세 개뿐**이고 전부 C-12 반송으로 채워진다.

> Density functional theory calculations comparing representative SDCP and PTFE
> segments on a Ni-rich oxide surface are shown in Figure 2e; the computational
> models and parameters are given in Figure S3 and Table S1. SDCP was represented
> by its sulfonate-bearing EDOT repeat unit and PTFE by a C₁₀F₂₂ segment, both on a
> LiNiO₂(104) slab used as a model for the layered NCM811 surface. Adsorption
> geometries were selected before any DFT calculation by screening several hundred
> candidate poses per segment, spanning seven distinct surface sites, systematically
> sampled molecular orientations and four in-plane rotations, and clustering the
> geometrically admissible poses into distinct binding basins (Figure S3); from these,
> one lowest-energy pose and one contrasting pose per segment were frozen for DFT
> evaluation. Each frozen geometry was then evaluated as a static single point,
> together with the corresponding bare slab and isolated molecule in matched cells,
> under a common electronic-structure protocol and for two initial antiferromagnetic
> orderings of the slab. The resulting adsorption energies were **[[E_ads_SDCP]] eV**
> for the SDCP repeat unit and **[[E_ads_PTFE]] eV** for the PTFE segment, giving a
> difference of **[[ΔE_ads]] eV**.
> These values are single-point energies on machine-learned rather than DFT-relaxed
> geometries, and describe an isolated segment on a clean, vacuum-terminated surface
> at 0 K; they therefore represent a model-level comparison of the two binder
> chemistries rather than the interfacial adhesion of the processed electrode.
> **The calculated difference refers to the adsorption of each segment as a whole,
> and the present data do not allow the stronger affinity to be attributed to any
> particular functional group.** This stronger surface affinity is also reflected in
> the post-mixing morphology. …(이하 기존 문장 유지)

### 왜 이 문장들인가

| 문장 | 왜 |
|---|---|
| "selected before any DFT calculation" | 자세 동결이 사전등록 사항이다. 이 한 마디가 *"결과 보고 자세 골랐나"* 를 막는다 |
| "several hundred candidate poses … seven distinct surface sites" | ⚠ **"twelve orientations" 이라고 못 박지 않는 이유**: 방향 수가 조각마다 다르다 (ptfe 12 · sdcp 12 + `sulfonate_down` 13). 하나로 적으면 한쪽이 틀린다. 정확한 수(336 / 364)는 **SI 로 내린다** — 본문은 "several hundred" 로 충분하다 |
| basin 수(96 / 101) | **본문에 안 넣는다.** SI Figure S3 캡션에 넣는다 — 본문에서 무게가 과하다 |
| "one lowest-energy pose and one contrasting pose" | 실제 역할이 `primary` + `sensitivity`/`stress_sensitivity` 다. "holdout" 이라 쓰지 않는다 — v36 은 홀드아웃 설계가 아니다 |
| "together with the corresponding bare slab and isolated molecule in matched cells" | v36 이 `clean_ref` 를 넣은 이유. 이게 있어야 절대 E_ads 를 쓸 자격이 생긴다 |
| "two initial antiferromagnetic orderings" | **initial** 이 핵심 — 도달한 상태가 아니라 초기조건이다 (wave1 에서 이걸 안 구분해 basin 사고가 났다) |
| 굵은 마지막 문장 | 삭제한 P0-1 의 대체. 관측된 것(조각 전체의 차)만 말하고 기전을 주장하지 않는다 |

### 빈칸 채우는 법 (C-12 반송 뒤)

| 빈칸 | 출처 | 조건 |
|---|---|---|
| `[[E_ads_SDCP]]` | `E_C(sdcp) − E_S − E_G(sdcp)` | 절대값 — `clean_ref` 게이트 통과가 전제 |
| `[[E_ads_PTFE]]` | 같은 식, control | 같음 |
| `[[ΔE_ads]]` | `E_ads(sdcp) − E_ads(ptfe)` | **차가 절대값보다 신뢰도 높다** |

⛔ **게이트가 절대값을 막으면** 두 칸을 비우고 문장을 이렇게 줄인다:

> The SDCP repeat unit adsorbed more strongly than the PTFE segment by
> **[[ΔE_ads]] eV** under this fixed-geometry protocol.

🔁 **재개 조건 (결과 보기 전에 선언됨, 그대로 지킨다)**: `|D_raw| < 0.05 eV` 면 **미해결**이다 —
계산을 늘리지 않고, 원고는 그 문단을 쓰지 않는다. `0.05 ≤ |D_raw| < 0.06 eV` 면
*"판정이 미시험 축(k)에 민감하다"* 를 본문에 적는다.

---

## 3. `[19]` 를 어떻게 하나

**판정: `[19]` 는 삭제되는 문장과 함께 빠진다. 교체 문단으로 옮기지 않는다.**

이유는 인용의 역할이다. `[19]` 는 *"극성 술포네이트가 표면과 더 잘 상호작용한다"* 라는
**기전 주장**을 뒷받침하러 붙어 있었다. 그 주장이 우리 데이터로 반증돼 문장이 통째로
빠지므로, 인용도 갈 곳이 없다. 교체 문단은 **우리 계산 결과만** 말하고 남의 기전을
빌리지 않는다 — 그래서 새 인용이 필요 없다.

⚠ **1저자가 확인할 것 하나**: `[19]` 가 원고 다른 곳에서도 인용되는가.
- **다른 데서도 쓰인다** → 그냥 여기서만 빼면 된다. 번호는 안 바뀐다.
- **여기서만 쓰인다** → 참고문헌 목록에서 빠지고 **[20] 이후 번호가 하나씩 당겨진다.**
  Word 자동번호면 저절로 되지만, 수동 번호면 전수 확인이 필요하다.

그리고 이건 **레퍼런스 규율**에 걸린다 (2026-07 Kim/Cui 교훈): 인용은 링크가 아니라
로컬 PDF/litdb digest 로 **역할을 확인한 뒤** 넣는다. `[19]` 의 실제 서지는 이 repo 에
없다 — 원고 참고문헌 목록이 repo 밖이라 확인 못 했다. **형님이 [19] 가 무엇인지 알려주면**
"다른 데서도 쓰이는가" 까지 같이 정리한다.

### 참고 — 이 주제로 붙일 수 있는 문헌은 따로 있다

litdb 에 **바인더 흡착 대조군 2편**이 있다 (`kb/syntheses/binder_adsorption_charge_state_2026_08_29.md`):
`[Han25]` ICEP · `[Kang25]` bollard-anchored (Adv. Mater. 2025, 37, 2416872).

⛔ 다만 **절대값 이식 금지**다 — 면이 다르고(우리 (104) / 둘 다 (001)),
엔진이 다르고(VASP PAW / CASTEP USPP / PFP NNP), 기준·U·조각 크기가 전부 다르다.
⭕ 옮길 수 있는 것은 **부호 방향**(불소계 대조군 대비 극성 바인더가 더 깊게 붙는다)과
**대조군 설계 관행**뿐이다. 쓰려면 Discussion 에 *"consistent with"* 수준으로만 넣는다.

⚠ 그리고 `[Kang25]` 는 함정이 있다 — 그쪽 −2.24 eV 는 `–COO⁻ ··· Na⁺ ··· O²⁻`
**양이온 브리지**라 "COO⁻ 결합" 이 아니라 "Na⁺ 2개 결합" 이다. 우리 문단이 기전을
주장하지 않는 것과 같은 이유로, 이 논문을 기전 근거로 인용하면 안 된다.

---

## 4. Figure 2e 캡션

현재 `"(e) DFT."` → 교체:

> (e) Calculated adsorption energies of representative SDCP and PTFE segments on a
> LiNiO₂(104) surface used as a model for the NCM811 surface. Values are static
> single-point energies at fixed, pre-selected geometries.

⛔ 캡션에 `sulfonate anchoring` · `polar interaction` 을 쓰지 않는다 (§1).
⚠ *"fixed, pre-selected geometries"* 를 캡션에도 넣는 이유: 그림만 보고 인용하는
독자가 **"DFT 로 이완한 최소점"** 으로 읽는 것을 막는다.

---

## 4-b. SI Figure S3 캡션 — 본문에서 내린 수치가 여기로 간다

현재 `"Figure S3. DFT"` → 교체 (**빈칸 없음, 지금 바로 됨**):

> **Figure S3.** Pose screening used to select the adsorption geometries evaluated by
> DFT. Candidate poses were generated on the LiNiO₂(104) surface at seven distinct
> sites (Li-top, Ni-top, O-top, Li–Ni bridge, Li–O bridge, Ni–O bridge and hollow),
> for twelve molecular orientations sampled on a Fibonacci sphere — with one
> additional sulfonate-down orientation for the SDCP repeat unit — and four in-plane
> rotations, giving 336 candidates for the PTFE segment and 364 for the SDCP repeat
> unit. Of these, 112 and 109 respectively passed the geometric admissibility
> criteria and clustered into 96 and 101 distinct binding basins. Screening was
> performed with a machine-learned interatomic potential and was frozen before any
> DFT calculation; the screening energies are used only for pose selection and are
> not reported as adsorption energies.

⚠ 마지막 문장이 **필수**다. 이게 없으면 E_pose 가 흡착에너지로 읽힌다 (`do_not_cite` 위반).
그림 자체는 `tools/figures/fig_c12_pose_screen.py` 가 낸다 —
Origin-ready CSV 는 `db/properties/c12_pose_screen_geometry.csv` (197행).
⛔ 그 그림에는 **에너지 축이 없다.** 일부러 뺐다.

---

## 5. Methods §DFT calculations — 두 곳 교체 (빈칸 없음, 지금 바로 됨)

### 5-1. 자가도핑 모델 서술 (사전등록 금지어)

기존:

> *"(the self-doped form C₁₁H₁₅O₆S₂ was obtained by removing a hydrogen atom, leaving a
> charge-neutral unit with an oxidized backbone compensated by the tethered sulfonate group)"*

H 를 떼면 **양성자 + 전자**가 같이 빠진다. 자가도핑은 사슬에서 **전자만** 빠지고 그 양전하를
tethered 술포네이트가 보상하는 과정이다. 둘은 다른 사건이다.

교체:

> An oxidized model, C₁₁H₁₅O₆S₂, was constructed by removing one hydrogen atom from the
> acidic side chain, giving a charge-neutral open-shell unit in which the oxidized backbone
> is compensated by the tethered sulfonate group. **Removing a hydrogen atom removes a
> proton together with an electron and therefore does not reproduce the self-doping process
> itself, in which the backbone is oxidized and the resulting positive charge is compensated
> by the covalently bound sulfonate; this structure is used only as a representative
> oxidized model.**

⛔ **이 단락에 수치를 넣지 않는다.** wave1 의 doped 항목은 `not_citable` 전건이고,
폴라론 pilot 은 아직 판정이 안 섰다.

### 5-2. "DFT 로 이완했다" 로 읽히는 문장

기존:

> *"…the lowest-energy configuration of each species on the surface Li and Ni sites was
> evaluated by DFT."*

교체:

> …the selected configuration of each species was evaluated by DFT **as a static single
> point on the machine-learned geometry** (no ionic relaxation).

이유: `NSW = 0` 이다. 지금 문장은 DFT 최소점으로 읽힌다.
그리고 *"on the surface Li and Ni sites"* 도 부정확하다 — 스크린은 **7 자리**를 봤고
동결된 자세가 Li/Ni top 이라는 보장이 없다.

### 5-3. 자기 상태

기존: *"antiferromagnetic LiNiO₂ (104) slab"*

교체: > …an **initially** antiferromagnetic LiNiO₂(104) slab (two orderings, denoted
> pm1 and net4; the converged magnetic state of each job is reported in Table S1).

이유: 자기 상태는 **선언**이지 판정이 아니다. wave1 에서 시작 배열과 도달 상태가
갈려 값이 섞인 전례가 있다 — 그때 실제로 뒤집힌 것은 언제나 같은 Ni 하나(#82)였다.

---

## 6. 1저자가 결정할 것

1. **§2 교체 문단**을 넣을지 — 넣으면 빈칸 3개가 C-12 반송까지 `[[…]]` 로 남는다.
   (대안: Figure 2e 자체를 C-12 반송까지 미룬다. 그러면 §1 삭제만 먼저 한다.)
2. **`[19]` 가 원고 다른 곳에도 쓰이는가** — §3.
3. C-12 반송 시 **절대값 두 개를 쓸지 차만 쓸지** — 게이트가 정하지만 방침은 미리.
4. §5 세 곳은 **지금 바로** 넣어도 된다 (수치 무관).

---

## 부록 — 이 문서가 보증하지 않는 것

- **C-12 결과값**. 아직 안 왔다. §2 의 빈칸은 빈칸이다.
- **원고 참고문헌 목록**. repo 밖이라 `[19]` 의 서지를 확인 못 했다 (§3).
- **Figure 2e 그림 자체**. 여기 있는 것은 본문·캡션 텍스트다.
- **영문 교정**. 문법은 봤지만 저널 스타일 교정은 안 거쳤다.
