# 끝 보고 — shi2026_argyrodite_stack_pressure_viscoplastic_deformation (2026-11-24 · litdb-curator · 병렬 배치)

digest `litdb/papers/shi2026_argyrodite_stack_pressure_viscoplastic_deformation.md` (638 줄 · 표 셀수 0 · 떠 있는 행 0 · PI 배지 [] · 태그 elements Li, P, S, Cl / methods elastic (+ Raman — 용어집 대응 없음)) · 그림 `litdb/figures/shi2026_argyrodite_stack_pressure_viscoplastic_deformation/` (25 장 + figures.json).
서지: Shi, Wang, Liu, López-Pernía, Watt, Gan, Mijailovic, Guduru, Mitlin\*, Sheldon\* (+ Shi\*) · *Matter* 9, 102767 (2026) · DOI 10.1016/j.matt.2026.102767 · 접수 2025-06-25 / 채택 2026-03-13 / 온라인 2026-04-10 / 권호 2026-07-01.
병렬 규칙: 쓴 것 = digest + 그림 폴더 + 이 보고 파일 · `_sources.json` 은 추출 도구가 다시 씀 · git 안 함 · `build_index.py` 는 `--check` 만 (rc 1 = 배치 전체 미편입 18 편 중 이 편 `[dem]` 포함 — 생성 전이라 정상).

## (a) 넣을 인덱스
- **축 = DEM** — `webapp/data.py::literature_track()` (build_index 가 쓰는 판정) 결과 `dem` (낱말 점수 dem 3 `fem`·`contact`·`indentation` 대 dft 1 `argyrodite` · override 없음). ⇒ **`INDEX_DEM.md` 생성에 맡긴다** (`python3 tools/litdb/build_index.py` — 묶음은 '기타', 제목에 묶음 낱말이 없다).
- 선택 (사람 큐레이션 · 같은 그룹 자매편 `song2025_porous_argyrodite_modulus_fracture_toughness` 선례): `INDEX.md` § **"🧲 계면 점착 · 인터레이어 트랙"** 표 (`| slug | 논문 | 축 |`) 에 아래 행. Jeff Sakamoto 태그는 **달지 않는다** ((g)).

```
| `papers/shi2026_argyrodite_stack_pressure_viscoplastic_deformation.md` **(본문 17 pp + SI1 23 pp + SI2 2 pp (보고 양식) + SI3 코드 (MATLAB 3 · .mat 28) · 크롭 25장 (손 크롭 `tab_S2` 1) · 그림 10장 실독 · SI3 재계산)** | **[외부·exp+FEM·⭐⭐ LPSCl 점소성 상수 + Li\|LPSCl 공극 닫힘 시간 실측]** ✅ **Changmin Shi\***/Yixian Wang/Xing Liu/C. López-Pernía/J. Watt/C. Gan/A. Mijailovic/P. R. Guduru/**David Mitlin\***/**Brian W. Sheldon\*** (Brown · UT Austin · NJIT · LANL; 자금 DOE Battery500 + SK On), "**Stack pressure effects and viscoplastic deformation in argyrodite solid-state electrolyte**" — ***Matter* 9, 102767 (2026)**, DOI `10.1016/j.matt.2026.102767`. Li\|Li₆PS₅Cl\|Li 3–8 MPa · 반주기 영전류 유지 12 min / 1 h / 5 h → CCD 최고 **4.8 mA/cm²** (8 MPa · 5 h · 막대 평균 figure-read ≈4.2) vs 무유지 1.8–2.4 · cryo-FIB 공극 면적 분율 ≈14–16 → ≈2.3 % (5 h) · R_SEI+CT ≈11.4 → ≈9.9 Ω·cm² · 나노압입 역해석 **Y_SE 0.35 GPa · ε̇₀ 10⁻⁵ s⁻¹ · n 4** (E 22.1 · ν 0.30 = 문헌값, 인용 = Abaqus 매뉴얼) · 차단전극 ASR −5 % (8 MPa · 5 h) · 해석 = Li Coble 크리프 (2.1×10⁴ s @ 8 MPa · d 100 µm) + SEI 경화 가설. ⚠ `Fig. 2D` SI3 로 재현 안 됨 · `Fig. 5D` 12 min 도금 점 불일치 · 같은 펠릿의 겉보기 E 는 자매편 4.7 GPa | 점착 트랙 Li\|LPSCl 공극 대조 표적 · DEM 입자 접촉 항복 후보 · Li 층 크리프 시간 |
```

## (b) comparison 에 넣을 줄
**① `comparison_vs_ours_DEM.md` §I — 새 항목** (지금 마지막이 I-10 · 번호는 합칠 때 정한다):

```
### I-11. `shi2026_argyrodite_stack_pressure_viscoplastic_deformation` — ★★★ **Li|LPSCl 계면 공극이 스택압 8 MPa 에서 '수 시간' 에 닫힌다** + LPSCl 점소성 상수 (입자 층 후보) · ⚠ 점착 · 젖음은 모델에 없다

> **무엇을 주나.** Li|Li₆PS₅Cl|Li (360 MPa · 60 °C 2 h · 1 µm · 상대밀도 85–89 %) · 8 MPa · 반주기 영전류 유지 0/12 min/1 h/5 h → cryo-FIB 공극 길이 ≈2 → ≈0.7 µm · 면적 분율 ≈14–16 → ≈2.3 % (figure-read · SI3 로 8 점 중 6–7 점 재현) · R_SEI+CT ≈11.4 → ≈9.9 Ω·cm² · CCD 최고 4.8 mA/cm² (무유지 1.8–2.4).
> LPSCl 나노압입 역해석 **Y_SE 0.35 GPa · ε̇₀ 10⁻⁵ s⁻¹ · n 4** (과응력 꼴 · E 22.1 · ν 0.30 문헌값 고정 · 20 mN 40–60 s 유지의 상대 깊이에 맞춤).
> 접촉 FEM (Li E 5 GPa · ν 0.3 · ε̇₀ 0.05 s⁻¹ · n 6.6 · Y₀ 1–16 MPa · **마찰 · 점착 없는 경접촉**) 은 Y₀ ≤ 2 MPa 면 완전 닫힘을 **수 초 (SI 하한 ms–µs)** 로 예측 → 실측 (수 시간) 과 어긋남 → 저자: Li Coble 크리프 (2.1×10⁴ s @ 8 MPa · d 100 µm) + SEI 경화 · 젖음 불량 (가설).
>
> **★ 우리 축에 닿는 곳 셋.**
> ① **W_ad 보고서 7 절 (점착과 공극) 의 실험 대조 표적** — 공극 크기 · 밀도 · 닫힘 시간의 원자료 (SI3) 가 있다. 저자가 '젖음 불량' 을 미해결로 남겼고 접촉 FEM 의 점착이 0 이라, Li|LPSCl W/γ_Li (젖음각) 가 들어갈 자리가 비어 있다 (⚠ 우리 쌍 목록에 Li|LPSCl 은 아직 없다 · 값은 싣지 않는다).
> ② **DEM 입자 접촉 항복 후보** — Y_SE 0.35 GPa (국소) ↔ 침대 겉보기 Y ≈0.13 GPa (Vickers HV ≈0.38 GPa 의 Tabor 환산 · 카드 산술) ≈ `lee2025_heckel_…` Heckel σ_y,eff 0.10–0.13 — §I-3 규율대로 입자 = 국소 · 침대 = 검증.
> ③ **'스택압 → 접촉' 의 시간 규모** — 속도 무관 소성이면 수 초 · 실측은 수 시간: 평형 접촉만 내는 모델은 t → ∞ 의 상한이다.
>
> **⛔ 인용 금지 / 한정어**
> · `Fig. 2D` (선 분율 ≈7 → ≈3.5 %) 는 Methods 정의로 SI3 에서 재현되지 않는다 (재계산 71/77 → 12/15 %) — 인용 금지.
> · `Fig. 5D` 12 min 도금 점 (≈13.7 %) 은 공개 데이터 (17.0 %) 와 다르다 · 닫힘 크기는 손 마스크 (`BW` → `BW_sparse`) 의존이 크다.
> · E 22.1 · ν 0.30 은 이 논문 측정이 아니다 (인용 = Abaqus 매뉴얼) — 같은 펠릿 공정의 겉보기 E 는 [Song25Mech] 4.7 GPa (I-3).
> · Y_SE · ε̇₀ · n 은 40–60 s · 20 mN · 상대 깊이 맞춤 — 스택압 (σ < Y) 크리프에는 쓰지 않는다 (식 1 은 0 을 준다).
> · Coble · SEI 경화는 저자 가설 (d = 100 µm · 벌크 σ 8 MPa 가정 · Coble 은 t ∝ d³/σ) — "기전 확정" 으로 쓰지 않는다.
```

**② `comparison_vs_ours.md`** — 물성 4축 표에 **값 행으로 넣지 않는 것을 권한다** (겹치는 E 22.1 은 빌린 값이고 그 밖에 우리 DFT 대응 양이 없다). 넣는다면 아래 둘 (열 구조는 기존 표와 같음):
- 📑 Reference key 표 (`| 약칭 | 논문 | digest/status | 유형 |`):
```
| **[Shi26VP]** ⭐⭐ **LPSCl 점소성 (나노압입 역해석) + Li\|LPSCl 공극 닫힘 (cryo-FIB · 5 h) + 스택압 영전류 유지 CCD** · ⛔ E · ν 는 빌린 값 | **Changmin Shi\***/Y. Wang/X. Liu/C. López-Pernía/J. Watt/C. Gan/A. Mijailovic/P. R. Guduru/**David Mitlin\***/**Brian W. Sheldon\*** 2026 ***Matter* 9, 102767** (DOI 10.1016/j.matt.2026.102767) — "Stack pressure effects and viscoplastic deformation in argyrodite solid-state electrolyte" | ✅ `papers/shi2026_argyrodite_stack_pressure_viscoplastic_deformation.md` — 판정은 **§C 1행** + `comparison_vs_ours_DEM.md` **§I-11** | 실험 + 연속체 FEM (Abaqus UMAT · 원자단위 계산 0) |
```
- §C 표 (`| 주장 | 출처 | 우리 | 비고 |`):
```
| ⛔ **🆕 (2026-11-24) Li₆PS₅Cl 점소성 구성식 'E 22.1 · ν 0.30 · Y_SE 0.35 GPa · ε̇₀ 10⁻⁵ s⁻¹ · n 4' 의 E 는 측정이 아니다 — 우리 comp1 E_VRH 22.06 과 같은 수인 것은 출처 계열 (Deng 2016 PBEsol) 이 같아서다 (독립 확인 아님)** — 탄성 상수 인용 = Abaqus 매뉴얼 (ref 37) · Y · ε̇₀ · n 은 20 mN Berkovich 40–60 s 유지의 상대 깊이 변화에 맞춘 값 (`Fig. S10`) · 같은 펠릿 공정의 겉보기 E 는 [Song25Mech] 4.7 GPa | **[Shi26VP]** p.6 식 1 · p.8 `Table 2` · `Fig. S10` | comp1 E_VRH 22.06 GPa (DFT relaxed-ion · canonical) — 항복 · 크리프 대응 양 없음 | 같은 수 · 다른 근거 · 다공 펠릿 FEM 에 조밀 결정 E 를 넣은 사례 |
```

## (c) `pdf_map.tsv`
**필수 아님.** 지금 자동 매칭 (`--inbox --only shi2026`) 이 본문 + SI1 을 '1쪽 본문 69 %' 로 붙인다 · SI2 (2 쪽 보고 양식 · 그림 없음) 는 '짝 못 찾음' 으로 남는다 (그림에는 영향 없음). 셋을 이름으로 묶어 두려면 한 줄:
```
shi2026_argyrodite_stack_pressure_viscoplastic_deformation	viscoplastic2026_argyrodite_stack_pressure
```

## (d) 추가로 먹일 만한 논문 (8 편 · 최근 먼저 · 전부 litdb digest 없음 · 이 배치 batch.json 에도 없음)
1. **Roach, Zhu, Vema, McMeeking, Grey, Deshpande, Fleck** 2025 · *Eur. J. Mech. A/Solids* 113, 105710 — "Void growth in the lithium anode of a solid state battery" · Li 쪽 공극 성장 · 닫힘의 크리프 역학 (이 논문이 LLZTO 의 빠른 Li 흐름 · n = 6.6 근거로 인용 · ref 43). 왜: 방전 중 공극 · Li 크리프.
2. **Li, Huang, Qu, Fu, Chen, Shen, Lin** 2025 · *ACS Appl. Mater. Interfaces* 17, 3146 — "Void Evolution at the Li/LLZO Interface: Stack Pressure and Operating Temperature-Driven Creep Effect" · 스택압 × 온도 × 크리프 공극. 왜: 스택압 · 방전 중 공극 (산화물 쪽 대조).
3. **Jeong & Kim** 2024 · *ACS Energy Lett.* 9, 3237 — "Deformation Mechanism Maps of Pure Lithium: Their Application in Determining Stack Pressure for All-Solid-State Lithium-Ion Batteries" · `Table S1`·`Table S2` 상수의 원전 (오타 확인용). 왜: Li 크리프 · 스택압 선택.
4. **Morchhale, Tang, Ghahremani, Farahati, Kim** 2024 · *J. Power Sources* 624, 235605 — "Re-evaluating critical current density in solid-state batteries: Challenges and proposing an alternative" · argyrodite · 20 MPa · 영전류 유지 ≤ 30 min (반대 경향). 왜: 스택압 · 유지 프로토콜 직접 비교군.
5. **Zaman, Zhao, Martin, Zhang, Wang, Wang, Harris, Hatzell** 2023 · *ACS Appl. Mater. Interfaces* 15, 37401 — "Temperature and Pressure Effects on Unrecoverable Voids in Li Metal Solid-State Batteries". 왜: 방전 중 공극 · 스택압.
6. **Haslam, Wolfenstine, Jeff Sakamoto** 2022 · *J. Power Sources* 520, 230831 — "The effect of aspect ratio on the mechanical behavior of Li metal in solid-state cells" · **🏷 Jeff Sakamoto 공저** · Li 박 형상비 → 겉보기 항복 · 스택압 (이 논문 Li 박 두께 근거 · ref 19). litdb 에는 `kalnaus2023` 총설 안 인용으로만 있다.
7. **Athanasiou, Liu, Jin, Nimon, Visco, Lee, Park, Yun, Padture, Gao, Sheldon** 2022 · *Cell Rep. Phys. Sci.* 3, 100845 — "Rate-dependent deformation of amorphous sulfide glass electrolytes for solid-state batteries" · 같은 그룹 · 압입 FEM 점소성 역해석 방법의 원전 (ref 20). 왜: 황화물 SE 크리프 · 구성식. litdb 에는 `kalnaus2023` 안 인용으로만.
8. **Narayan & Anand** 2018 · *Extreme Mech. Lett.* 24, 21 (+ **Anand & Narayan** 2019 · *J. Electrochem. Soc.* 166, A1092) — Li 대변형 탄–점소성 모델 (항복 0.7–0.8 MPa · ε̇₀) · 이 논문 Li 소성 입력의 원전. 왜: Li 금속 구성식 (연속체 Li 층).
- 참고: Masias 2019 (*J. Mater. Sci.* 54, 2585 · Jeff Sakamoto 공저 · Li E · ν · 크리프 — ref 44) 는 **이 배치에서 이미 처리**됐다 (`masias2019_li_metal_elastic_plastic_creep_properties.report.md` 있음).

## (e) DEM-DFT 보고서에 쓸 거리 (쪽 = 인쇄 쪽 · 직접 봤는지)
| 쓸 곳 | 값 · 조건 | 근거 위치 | 직접 봤나 |
|---|---|---|---|
| DEM 입자 접촉 소성 (LPSCl) | **Y_SE 0.35 GPa · ε̇₀ 1×10⁻⁵ s⁻¹ · n 4** · 식 1 σ/Y = (1 + ε̇ᵖ/ε̇₀)^(1/n) (과응력 꼴 → σ < Y 에서 흐름 0) · E 22.1 · ν 0.30 (문헌 · 출처 불명) · 20 mN Berkovich · 40–60 s 유지 · 상대 깊이 맞춤 · 광유 속 · 4 표면 | p.6 식 1 · p.8 `Table 2` · `Fig. S10` · p.13–14 Methods | `Table 2` = PDF 글자 (이미지 미독) · `Fig. S10` 실독 |
| DEM 압밀 · 침대 검증 | 360 MPa · 4 min · 상온 일축 · 1 µm 분말 (NEI) · 60 °C 2 h → 상대밀도 85–89 % (진밀도 분모 미기재) · 기공 8–17 % · σ_ion 0.53 mS/cm · Vickers 29.4 N 대각선 ≈377 → ≈415 µm (0 → 5 h) → HV ≈0.38 → ≈0.32 GPa · Tabor Y ≈0.13 GPa [우리 산술] · Table 2 FEM 깊이 ≈38 µm vs 실측 ≈54–59 µm (상수가 큰 스케일에서 너무 단단) | p.2 · p.11 · `Fig. S14` · SI p.1 · `Fig. 4D–F` | `Fig. S14` · `Fig. 4` 실독 · `Fig. S1` 미독 |
| 연속체 Li 층 | E 5 GPa · ν 0.3 · ε̇₀ 0.05 s⁻¹ · n 6.6 · Y₀ 1 · 2 · 4 · 8 · 16 MPa (변수) · 문헌 Li 항복 0.7–0.8 MPa · 덴드라이트 모델은 완전 소성 (값 없음) | p.14 · p.9–10 | PDF 글자 |
| Li 크리프 시간 규모 | `Table S1` @ 8 MPa · d 100 µm: Coble **2.099×10⁴ s (5.8 h)** · 격자 확산 GBS 2.552×10² s · 전위관 GBS 5.885×10⁵ s · NH 2.446×10¹⁵ s · 전위 활주 10⁻⁵ s … · `Table S2` 식 · 상수 (b · G(T) · ν 0.36 · E(T) · D_l = 3.14×10⁻⁴ exp(−55700/RT)) — 오타 있음 → 원전 확인 | SI p.12–14 | PDF 글자 (`tab_S1`·`tab_S2` 이미지 미독) |
| **W_ad 보고서 7 절 (점착과 공극) — 실험 대조 표적** | 사이클 직후 공극 동전 모양 · 양쪽 ≈200 nm · ≤ 5 µm · 8 MPa 5 h 유지: 길이 ≈2.15/1.62 → ≈0.72/0.77 µm · 폭 ≈0.2–0.3 µm · 밀도 ≈0.34/0.48 → ≈0.15 µm⁻¹ · 면적 분율 ≈14.2/16.4 → ≈2.3 % (도금/탈리) · R_SEI+CT ≈11.4 → ≈9.9 Ω·cm² · 초기 계면 ASR 11 Ω·cm² (60 °C · 8 MPa) | p.4 · `Fig. 2C` · `Fig. 5D` · `Fig. 2F` · SI `Fig. S6` 캡션 | `Fig. 2` · `Fig. 5` 실독 + SI3 재계산 · `Fig. S6` 미독 |
| **W_ad 7 절 — 빈자리 (점착 · 젖음)** | 접촉 FEM = **마찰 · 점착 없는 경접촉** (W 80 · L 105 · h 10 µm · 8 MPa) · 저자 *"Poor wetting with the electrolyte is another possible factor that may limit void filling"* (정량 없음) · 우리 쌍 목록에 Li\|LPSCl 없음 — 값은 싣지 않는다 | p.10 · p.14 · `Fig. 5E–F` · `Fig. S12` | 실독 |
| 계면 모델의 SE 탄성 가정 | 공극 끝 최대 von Mises 116 MPa (≈2 nm² 요소 · 메시 의존 · 10 MPa 로 계산) < Y_SE 350 MPa → LPSCl 탄성 · Li 는 항복 | p.8–9 · `Fig. 5B–C` | 실독 |
| 스택압 영역 LPSCl 크리프 | 차단전극 정규화 ASR 5 h: 8 MPa ≈0.946 · 5 MPa ≈0.975 · LLZTO ≈1.00 (구성식 없음 · 셀 1 개씩) | p.7–8 · `Fig. 4G` | 실독 |
| 덴드라이트 균열 (정성) | G_net 유지 중 완화 (18 MPa ≈0.77 → ≈0.69 · 36 MPa ≈0.96 → ≈0.74 J/m²) — 같은 압력 최고값은 유지 유무 같음 · G_c 비교 없음 | p.11 · `Fig. 6` | 실독 |
| ⛔ 쓰지 말 것 | `Fig. 2D` 선 분율 (재현 안 됨) · `Table 1` 4.8 을 평균으로 · E 22.1 을 '측정' 으로 | §8b · §10 | — |
- 우리 원장과 겹치는 값: E 22.1 ≈ 우리 comp1 E_VRH 22.06 (출처 계열이 같아서 · 독립 확인 아님). W 값은 digest 에 싣지 않았다 (보고서 위치만: `docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html` 2 절 쌍 목록 · 7 절).

## (f) 그림 크롭 요약
- 추출 도구 24 장 (본문 그림 6 + 표 2 · SI 그림 14 + 표 2 (`Table S1`·`Table S3`)) + **손 크롭 1 장 `tab_S2.png`** — 도구가 '번호 공백 tS2' 로 보고 (테두리 · 그림 없는 글자 표라 앵커가 안 잡힘). SI p14 clip (85,272,515,766) 과 p15 clip (85,70,515,121) 을 위아래로 이어 300 dpi · 경계는 clip 글자 추출로 확인 · `figures.json` 에 `manual_crop` 사유 + `missing_labels[tS2].resolved` 기록 ⇒ **25 장 · 놓친 것 0**. SI2 (2 쪽 Cell Press 보고 양식) 에는 그림이 없다 (정상).
- 실독 10 장: `Fig. 1`–`Fig. 6` · `Fig. S10` · `Fig. S11` · `Fig. S12` · `Fig. S14` (+ 확대 3: `Fig. 2C` 길이 · `Fig. 2D` · `Fig. 5D`). 안 본 것: `Fig. S1`–`Fig. S9` · `Fig. S13` · 표 5 장 (PDF 글자 사용).
- 본문과 어긋난 그림: `Fig. 2D` (Methods 정의 재현 불가 · "< 10 %" 문장과 모순) · `Fig. 5B` (그림 · 캡션 10 MPa 대 본문 8 MPa) · `Fig. 5D` 12 min 도금 점 (공개 데이터와 ≈3.3 %p 차) · `Fig. 5F` (100 % 닫힘은 외삽) · `Fig. 6` (같은 압력 최고 G_net 동일) · `Fig. 4E` (= 대각선/7) · `Fig. 1C` ↔ `Table 1` (최고 셀 대 평균) · `Fig. 4B` ↔ `Fig. 4C` (같은 20 mN 에서 깊이 2 배 차).
- **SI3 '코드 (Sup3)' 절 = digest §8b 추가 완료** — 스크립트 3 개의 입력 · 출력 · 식 · 문턱 · 본문 대응 · 파일 이름 규칙 · 변수 표 · 재계산 (`Fig. 5D` 6–7/8 점 · `Fig. 2C` 7/8 점 재현 · `Fig. 2D` 재현 불가) · **.mat 은 28 개** (DataPoint 1 + 이미지 27 · 전달 메시지의 '29' 와 1 개 다름) · **FEM 코드는 없음** (본문은 'modeling code is shared' 라 함) · 데이터는 litdb 로 복사 안 함 · scipy 1.18.1 로 읽기만.
- **임시 파일 대조 (병렬 충돌 점검)**: 내 임시 파일은 처음부터 scratchpad 하위 폴더 `shi2026/` (공용 이름 아님) 에 있었고, digest 에 쓴 본문 · SI1 · SI2 글자를 PDF 에서 다시 뽑아 sha256 을 비교했다 → **세 파일 모두 바이트 동일** (c93f515582e68962 · 2af7c246b1336da6 · 84ddbeaa6d4bcc1e · 첫 쪽 = 이 논문 제목 · 'Matter, Volume 9' · 보고 양식) ⇒ 다른 논문 글자 섞임 없음. 이후 임시 파일은 slug 폴더로 옮겨 썼다.
- ⚠ **webapp PI 배지 오탐을 하나 밟았다 (고침)**: 머리말에 'Jeff Sakamoto 는 저자가 아니다' 라고 적었더니 `_paper_pis()` 가 `sakamoto` 배지를 붙였다 (부정 표지 NEG 에 '아님' 은 있고 '아니다' 는 없다). 문장을 이름 없이 바꿔 `pis = []` 로 확인. 같은 꼴이 다른 digest 에서도 생길 수 있어 `webapp/data.py::_paper_pis` 의 NEG/DROP 에 '아니다' (또는 '저자가 아') 를 더하는 것을 권한다 — 내 쓰기 범위 밖이라 손대지 않았다.

## (g) Jeff Sakamoto 저자 여부
**아니다.** 저자 10 명 (교신 Shi · Mitlin · Sheldon) 중에 없고, 참고문헌 15 (Chang 2021 *Nat. Commun.*) · 19 (Haslam 2022 *J. Power Sources*) · 44 (Masias 2019 *J. Mater. Sci.*) 의 공저자로만 나온다 ⇒ INDEX 행에 🏷 태그를 달지 않는다 · digest 저자 줄에도 그 이름을 넣지 않았다 (배지 오탐 방지).
