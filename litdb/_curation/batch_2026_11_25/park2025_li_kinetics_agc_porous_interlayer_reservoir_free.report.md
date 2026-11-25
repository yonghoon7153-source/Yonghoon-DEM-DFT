# 끝 보고 — park2025_li_kinetics_agc_porous_interlayer_reservoir_free (배치 2026-11-25 · #3)

- digest: `litdb/papers/park2025_li_kinetics_agc_porous_interlayer_reservoir_free.md` (새 파일 · 한국어 standalone · §0–§16 · §16 = 남의 카드에 돌려줄 답)
- 그림: `litdb/figures/park2025_li_kinetics_agc_porous_interlayer_reservoir_free/` — 크롭 32 장 (본문 그림 7 · 본문 표 1 · SI 그림 23 · SI 표 1) · 전부 도구 (`--slug … --pdf 본문 SI --clean`) · 손 크롭 0 · 다시 자름 0. **32 장 전부 Read 로 봤어요** + 확대 · 화소 판독 6 곳 (scratchpad · 저장 안 함).
- 해시: inbox 두 파일 sha256 이 batch.json papers[2] 와 맞았어요 (본문 `d9685f2b…` · SI `c4f555db…`).
- 공유 파일 · git 은 안 건드렸어요. `litdb/figures/_sources.json` 은 추출 도구가 스스로 다시 써요 — 제 실행 직후에는 병렬 에이전트 실행과 겹쳐 이 slug 항목이 빠져 있었는데, 뒤의 실행이 다시 만들어서 지금은 641 편 · 이 slug 32 장으로 들어 있어요 (손 안 댐). 메인 체크포인트 커밋 `a9366eb7` 이 그림 폴더 (33 파일) 를 이미 담고 있고, digest 는 미추적이에요.
- 점검 (읽기만): `build_index.py --check` → 이 digest 는 '어느 인덱스에도 없음 [dft]' + 'comparison_vs_ours 미편입' 만 걸려요 ((a) · (b) 를 넣으면 풀려요). `extract_figures.py --inbox --only park2025_li_kinetics` (매칭표만) → 본문 + SI 자동 매칭 `[제목 82%]`. 웹앱 (파일 안 씀 · `PYTHONDONTWRITEBYTECODE=1` · `-p no:cacheprovider`): `/paper/<slug>` 200 · `paper_figures` 32 · `paper_figure_notes` 32 (Figure set 표가 32 장 모두에 붙음) · `_paper_pis` = [] · 원소 페이지 Ag · Li · C · P · S 에 연결 (Cl 은 안 붙임 — 의도) · `methods: —` (목록 기법 없음). 시험: `test_v3_markdown` + `test_v3_literature` 45 통과 · `test_webapp -k "sakamoto or litdb_figure or recent_digests or digest_date or element_papers or glossary_papers or figure_comment"` 7 통과 1 실패 = `test_recent_digests_are_on_every_litdb_surface` (INDEX · comparison 미편입 — 합치면 풀려요).
- 🎤 talk 역링크: 해당 없음 (`litdb/talks/*` 인입 대기열에 이 편 없음).

**메인이 먼저 알아야 할 것**
1. **'≈29 %' 의 정체** — cryo FIB-SEM 단면 **한 장** (figure-read ≈6.7 × 4.7 µm) 의 **2D 면적 기공률** 이고, 이 논문의 세 층 (카본블랙 Super C65 : Ag = 3 : 1 · PVDF 5 % · 7.2 µm · SS316 위 · Li₃PS₄ 에 **단축 380 MPa** 로 붙인 뒤) 의 값이에요 (`Fig. S13` · `Fig. S14` 그림 안 'Porosity 29.1 / 29.2 / 29.2 %'). 저자는 '흔한 Ag/C 층' 값이라고 안 썼어요 — 그 말은 `metzler2026_…` (Metzler 원문) 과 `kang2026_…` 카드 쪽 표현이에요. 첫 1 mAh cm⁻² 뒤에는 4.4 (탄소) · 8.2 (Ag 200) · 3.1 % (Ag 50). ✎ 이 29 % 로 부피 수지를 맞추면 층 안에 들어갔다는 Li 금속 0.5 mAh cm⁻² (≈2.4 µm) 가 처음 기공 부피 (≈2.1 µm) 보다 커서, 층이 18–24 % 부풀었거나 3D 기공이 더 커야 해요 (원문은 이 산수를 안 함 · digest §10-⑦). **DEM 입력이면 '2D · 380 MPa · 이 배합' 을 같이 달아 주세요.**
2. **[우리 그룹] `kang2026_…` 의 입력값 출처가 이 논문과 안 맞아요** (고치지 않았어요): 표 S3 D_interlayer **3.15 × 10⁻¹⁰ m² s⁻¹** (Ref. S3 = 이 논문 · S4) — 이 논문에 있는 값은 GITT **3.14 × 10⁻⁹ cm² s⁻¹** (Ag 50 · 0–0.2 V · 단위는 `Fig. S9a` 축) = 3.14 × 10⁻¹³ m² s⁻¹ 로 **가수는 같고 지수가 10³ 달라요** · 그리고 그 D 는 층의 화학 확산이라 Kang 모형 (Coble 점도) 의 표면 확산과 다른 양이에요 · κ_e **1000 S m⁻¹** (S3) — 이 논문의 전자 전도 숫자는 탄소 **1 × 10² S m⁻¹** (ref 23 인용) 하나뿐이에요. S2 · S4 는 못 봐서 확정은 아니에요.
3. **SE 는 Li₃PS₄ · 셀은 80 °C** 예요 (아지로다이트 실온 아님). 그런데 박리 시험 그림 (`Fig. S5`) 라벨만 'LPSCl' 이에요 — 박리 시험을 LPSCl 로 했는지 라벨만 옮겼는지 원문으로 못 갈라요.
4. **안정 지도 (`Fig. 3e`) 는 판정선이 아니에요** — K · δs · Ds · 쓴 σ · φ 가 없어요. ✎ 원문 식과 `Fig. 3c` 값으로 실험 조건 (1 MPa · φ 0.29 · K = 1) 을 넣으면 창 전체가 θ < 1 인데, 실험에서 Ag 50 층은 1 MPa 에서 세 전류 모두 집전체 쪽에 닿았어요. 그림의 θ(50 nm, 0.1 mA cm⁻²) ≈12 (figure-read) 는 σφ ≈3.9 MPa 를 뜻해요.
5. **'Li₀.₉₈Ag₀.₀₂' 는 봉우리 하나 (d ≈2.48 Å · ≈36°) — bcc Li (110) 과 같은 자리**라 순수 Li 와 못 갈라요. 'Ag 가 석출 Li 쪽으로 갔다' 의 직접 근거는 EDS (`Fig. S10` · `S17` · 정성) 예요.
6. **EIS 숫자 하나가 표와 그림에서 달라요** — Ag–C 50 nm · 0.1 mA cm⁻² 의 R_interface: `Table S1` 172.9 대 `Fig. 6i` ≈200 (화소) · 표 합 510.8 대 `Fig. S22c` 저주파 끝점 ≈593 (figure-read). 나머지 다섯 점은 맞아요. 단위도 본문 · 표 'Ω' 대 그림 축 'Ω cm²' (표 합이 Ω cm² 축 끝점과 맞으니 Ω cm² 로 보여요).
7. 도구의 '번호 공백 14 건' (`f8`–`f21`) 은 본문 한 줄 'Figure 21b' (SI 그림 오기) 가 만든 허상이에요 — 빠진 그림 없어요. `tab_S1` 의 auto_fallback (캡션 위 크롭) 은 눈으로 보니 맞아요.
8. 참고문헌 [26] Coble 의 저널이 'Jpn. J. Appl. Phys.' 로 잘못 적혔어요 (Crossref: *J. Appl. Phys.* 34, 1679 (1963) · DOI 10.1063/1.1702656).

---

## (a) `litdb/INDEX.md` 에 넣을 행

**절**: `## 🌱 Li 금속 음극 — 공극 · 점착 · 핵생성 · 적층압 · Ag/C 인터레이어 (2026-11-24 · 18 편 + 11-24b 12 편)` — 행 순서상 **Ag/C 묶음 끝** (`xie2024_agc_buffer_layer_lithiation_delithiation_mechanism` 행 다음 · `shi2026_argyrodite_stack_pressure_viscoplastic_deformation` 행 앞). 이 배치 셋을 넣으면 절 머리 '18 편 + 11-24b 12 편' 과 첫 인용 줄의 편수도 고쳐야 해요.

| `papers/park2025_li_kinetics_agc_porous_interlayer_reservoir_free.md` **(본문 11 pp + SI 20 pp (그림 S1–S23 · 표 S1 · Note S1) · 크롭 32 장 (도구 32 · 손 크롭 0 · 번호 공백 경고 14 = 본문 'Figure 21b' 오기 — 빠진 그림 없음) · 32 장 전부 실독 · 화소 판독 6 곳 · 2026-11-25)** | **[외부·exp+연속체 (2D 선형 탄성 고유변형 FE · 확산 FE · Coble 척도식)·⭐⭐ Ag–C 다공 층 안 Li 이동 · Ag/C 층 '≈29 %' (2D) 의 원 출처 · ⛔ SE = Li₃PS₄ · 80 °C · 원자 단위 계산 0 · 점착 = 테이프 박리 정성뿐 · 우리 W 와 같은 줄 금지]** ✅ **Se Hwan Park**/Kaustubh G. Naik/Bairav S. Vishnugopi/Partha P. Mukherjee/**Kelsey B. Hatzell\*** (Princeton · Purdue · DOE EFRC MUSIC), "**Lithium Kinetics in Ag–C Porous Interlayer in Reservoir-Free Solid-State Batteries**" — ***Adv. Energy Mater.* 15, 2405129 (2025)**, DOI `10.1002/aenm.202405129` (CC BY-NC-ND · 자료 요청 시). 카본블랙 Super C65 (50 nm) : Ag NP (200 또는 50 nm) = 3 : 1 + PVDF 5 % · **7.2 ± 0.2 µm** on SS316 10 µm ‖ Li₃PS₄ 펠릿 (80 MPa) · 층 \| SE **380 MPa** · Li 포일 상대 전극 · **80 °C · 1 / 5 MPa**. 처음 2D 기공 **29.1 / 29.2 / 29.2 %** (cryo FIB-SEM · 380 MPa 뒤) → 1 mAh cm⁻² 뒤 4.4 / **8.2 (Ag 200)** / 3.1 %. 1 MPa · 0.5 mA cm⁻²: 탄소만 = 층 균열로 Li 새어 나감 · **Ag 200 = Li 가 SE \| 층 사이 (층이 들림)** · Ag 50 = 집전체 쪽 덴드라이트 · 5 MPa = 셋 다 집전체 쪽 섬유 다발 · 전류 ↓ (0.25 · 0.1) → 집전체 쪽 · 조밀. XRD (1 mAh cm⁻²): Ag 200 · 1 MPa 만 금속 Ag 잔존 (+ LiAg · Li₉Ag₄) · Ag 50 = Li₉Ag₄ + Li₁₀Ag₃. GITT D 4.45 × 10⁻¹⁰ / 1.59 × 10⁻⁹ / 3.14 × 10⁻⁹ cm² s⁻¹ · 핵생성 과전압 Ag 200 15.3 ± 7.8 대 Ag 50 < 1 mV · 첫 CE Ag 200 67.0 / 40.8 / 66.6 · Ag 50 50 / 65.6 / 77.4 % (0.5 / 0.25 / 0.1) · 단락 Ag 200 10–12 / 3–5 / > 20 · Ag 50 4–6 / 20+ / 20+ 사이클. 저자 기전 = Coble 크리프 플럭스 (∝ σ/r²) 대 Li⁺ 환원 플럭스 (∝ I/φ). 🔴 K · δs · Ds · `Fig. 3e` 의 σ · φ 미기재 (✎ 실험 조건이면 θ < 1) · GITT 조건 τ ≪ L²/D 미충족 (✎) · 응력 '크기 효과' 는 기하 효과 (최대값 비슷 · figure-read) · 'Li₀.₉₈Ag₀.₀₂' = bcc Li (110) 과 겹친 봉우리 하나 · ✎ 29 % 로는 부피 수지 안 맞음 · `Fig. 3` 캡션 a/b 뒤바뀜 · `Table S1` 대 `Fig. 6i` 한 칸 불일치 · 'Ω' 대 'Ω cm²' · `Fig. S5` 라벨 LPSCl · 표본 대부분 n = 1 | 점착 트랙: W_ad 보고서 8-3 ('자리 = 속도 경쟁' — 압력 · 전류 · Ag 입경으로 SE 쪽 ↔ 집전체 쪽 뒤집힘 · 테이프 박리에서 집전체 쪽이 약함) · 7-1 Ag 행 (합금 완결도의 입경 · 압력 의존) · SUS 행 (SS316 셀 선례 둘째) · 8-4 (서브 µm 기공 안 Li = 확산 크리프 · 탄소만 층의 응집 파괴 → Li 길) · DEM 기하 입력 (7.2 µm · 2D 29 % · 50 / 200 nm · ✎ Ag 5–6 vol%) · ⛔ 29 % 를 '흔한 Ag/C 층' · Lee 2020 층 · 3D 값으로 인용 금지 · 이웃 `lee2020_…` [7] · `spencerjolly2023_…` [13] · `xie2024_…` [29] (점착 비대칭 입력과 같은 방향) · `metzler2026_…` (SI S5 로 인용) · `kang2026_…` (SI [S3] · D · κ_e 출처 불일치) · 병렬 `sandoval2023_…` [11] |

---

## (b) `comparison_vs_ours.md` · `comparison_vs_ours_DEM.md` 에 넣을 줄

### b-1. `comparison_vs_ours.md` `📑 Reference key` 표에 한 행 (4 칸: 약칭 | 논문 | digest/status | 유형) — `[Xie24AgC]` 행 다음 (Ag–C 묶음)

| **[Park25AgC]** ⭐⭐ **Ag–C 다공 인터레이어 (Super C65 : Ag NP 3 : 1 · 7.2 µm · SS316 위) 안 Li 이동 — Ag 입경 (50 · 200 nm) · 적층압 (1 · 5 MPa) · 전류 (0.1–0.5 mA cm⁻²) 로 석출 자리 · 형태가 갈린다 · 처음 2D 기공률 ≈29 % (380 MPa 뒤 cryo FIB-SEM)** · ⛔ **A–D 4축 진입 금지 (SE 물성 측정 0 · SE = Li₃PS₄ · 80 °C)** · ⛔ 점착 = 테이프 박리 정성뿐 · 우리 W 와 같은 줄 금지 | Se Hwan Park/Kaustubh G. Naik/Bairav S. Vishnugopi/Partha P. Mukherjee/Kelsey B. Hatzell\* (Princeton · Purdue) 2025 ***Adv. Energy Mater.* 15, 2405129** (DOI 10.1002/aenm.202405129 · CC BY-NC-ND) — "Lithium Kinetics in Ag–C Porous Interlayer in Reservoir-Free Solid-State Batteries" | ✅ `papers/park2025_li_kinetics_agc_porous_interlayer_reservoir_free.md` — 판정은 §E 2 행 + `comparison_vs_ours_DEM.md` §I 블록 · §A 한 줄 | 실험 (단면 SEM/EDS · cryo FIB-SEM 2D 기공 · XRD · EDXRD · GITT · EIS · 테이프 박리) + 연속체 (2D 선형 탄성 FE · 확산 FE · Coble 척도식) · 원자 단위 계산 0 |

### b-2. `comparison_vs_ours.md` §E 표에 두 행 (4 칸: 주장 | 출처 | 우리 | 일치)

| **🆕 (2026-11-25) Ag–C 층에서 Li 가 쌓이는 *자리*는 계면 점착 순서만이 아니라 Li 크리프 플럭스 (∝ σ/r²) 대 Li⁺ 환원 플럭스 (∝ I/φ) 의 *속도 경쟁*으로 갈린다 — 같은 층 (카본블랙 : Ag 3 : 1 · 7.2 µm · SS316 · Li₃PS₄ · 80 °C) 에서 1 MPa · 0.5 mA cm⁻² 면 Ag 200 nm = SE \| 층 사이 (층이 들림) · Ag 50 nm = 집전체 쪽 (덴드라이트) · 탄소만 = 균열로 새어 나감 · 5 MPa 또는 전류 ↓ 면 집전체 쪽 · 조밀** — 자리는 단면 SEM/EDS 로 봤고, 경쟁식은 척도식 (K · δs · Ds · σ · φ 미기재) · 테이프 박리 (정성) 는 층 \| 집전체 쪽이 약함 | [Park25AgC] p.2–6 · `Fig. 1` · `Fig. 3c,e` · `Fig. 5` · `Fig. S6` · `Fig. S19` | 우리 W 쌍 (W_ad 보고서 §2 · `db/properties/adhesion.json` · `db/properties/wad_*` · 값은 위치만) 은 0 K 고정 기하 분리 일 — 크리프 · 전류 경쟁은 모형 밖 · SUS 쌍 없음 | — (정성 · W 순서를 자리 예측으로 쓰지 말라는 실험 근거 · 맞출 표적 아님) |
| **🆕 (2026-11-25) Ag 입경 · 적층압이 Li–Ag 합금 완결도를 바꾼다 — 첫 1 mAh cm⁻² 뒤 200 nm Ag 는 1 MPa 에서 금속 Ag 가 남고 (LiAg · Li₉Ag₄ 와 함께) · 50 nm Ag 나 5 MPa 면 Ag 가 사라져 Li₉Ag₄ · Li₁₀Ag₃ 만 · 10 mAh cm⁻² 뒤 석출층 전체에 d ≈2.48 Å bcc 봉우리 (저자 동정 Li₀.₉₈Ag₀.₀₂)** | [Park25AgC] p.5–9 · `Fig. 4` · `Fig. 7` · `Fig. S16` · `Fig. S23` | Li–Ag 합금 계산 0 · W_ad 7-1 Ag 행 (Ag(111) = 합금 전 · 충전 중 = Li-풍부 합금 후보) | 🟡 방향 근거 (문헌) · ⚠ 2.48 Å 한 봉우리는 bcc Li (110) 과 겹쳐 Li₀.₉₈Ag₀.₀₂ 와 순수 Li 를 못 가른다 · 상 순서는 [SJ23AgC] · [Ko25MIL] 과 같은 방향 · '접촉 상실이 원인' 은 확산 FE (매개변수 미기재) 로 '확산 거리 아님' 만 배제 |

### b-3. `comparison_vs_ours_DEM.md` §I 블록 (지금 I-33 이 끝 · 번호는 메인이 정해 주세요 — 병렬 둘이 같은 자리를 쓸 수 있어요)

### I-xx. `park2025_li_kinetics_agc_porous_interlayer_reservoir_free` — ★★ (exp + 척도식 · ⛔ W 아님 · ⛔ G_c 아님) **Ag–C 층 안 Li 는 확산 크리프로 지나고, 그 속도 (∝ σ/r²) 가 환원 속도 (∝ I/φ) 를 못 따라가면 SE 쪽에 쌓인다** — 압력 · 전류 · Ag 입경으로 자리가 뒤집힘 · 처음 2D 기공 29 % (380 MPa 뒤)

> **무엇을 주나.** 카본블랙 Super C65 (50 nm) : Ag NP (200 / 50 nm) = 3 : 1 + PVDF 5 % · **7.2 ± 0.2 µm** on SS316 10 µm ‖ Li₃PS₄ (80 MPa 펠릿) · 층 \| SE **380 MPa** · **80 °C · 1 / 5 MPa** · 0.1–0.5 mA cm⁻² · 2 mAh cm⁻² (*Adv. Energy Mater.*, 15, 2405129 (2025)). 처음 2D 기공 29.1–29.2 % (cryo FIB-SEM 단면 한 장 · 380 MPa 뒤) → 1 mAh cm⁻² 뒤 4.4 / 8.2 / 3.1 %. 1 MPa · 0.5: 탄소만 균열 · **Ag 200 SE 쪽 (층 들림)** · Ag 50 집전체 쪽 덴드라이트 · 5 MPa 셋 다 집전체 쪽 · 전류 ↓ → 조밀.
>
> **★ 우리 축에 닿는 곳.**
> ① **W 순서 ≠ 자리** — 같은 층 · 같은 계면에서 압력 · 전류 · Ag 입경만으로 SE 쪽 ↔ 집전체 쪽이 뒤집혔다 → W 순서는 '느린 극한에서 어디가 열리나' 의 후보 (I-20 Metzler 2025 의 '핵생성 세기로 자리 예측 안 함' 과 같은 방향). 테이프 박리는 층 \| SUS 쪽이 약함 (정성 · I-33 Xie 의 점착 입력 순서와 같은 방향).
> ② **Li 흐름 법칙** — 1 µm Li 항복 95 MPa (298 K · ref 25) ≫ 적층압 1–5 MPa → 서브 µm 기공 안 Li 는 확산 크리프 (σ 선형 · r⁻²) 로 본다 · I-16 (`masias2019_…`) 의 벌크 멱법칙 크리프 (n 6.56) 를 층 안 기공에 그대로 쓰지 않는다 · 원자 입력은 W 가 아니라 Li \| C · Li \| Li–Ag 계면 확산 (δs Ds · ✎ `Fig. 3c` 로 역산 ≈2 × 10⁻²² m³ s⁻¹).
> ③ **DEM 기하 (시나리오 입력 후보)** — 층 7.2 µm (측정) · 2D 기공 29 % (측정 · 380 MPa) · Ag 50 / 200 · C 50 nm (공칭) · 3 : 1 질량 · ✎ Ag 5.2–5.9 vol% (고체) · ✎ Ag 입자 수 64 배 차 · 탄소만 층은 1 MPa 에서 수십 µm 조각으로 응집 파괴 → 균열이 Li 길 (I-26 '연결 기공 ≠ Li 길' 과 같은 방향).
>
> **⛔ 인용 금지 / 한정어**
> · 29 % 를 '흔한 Ag/C 층' · Lee 2020 층 · 3D 기공률로 쓰지 않는다 (✎ 부피 수지 긴장 — digest §10-⑦).
> · `Fig. 3e` θ = 1 을 판정선으로 · `Fig. 3a,b` 응력 (MPa) 을 입력으로 · GITT D 를 Coble Ds 로 쓰지 않는다.
> · SE = Li₃PS₄ · 80 °C — LPSCl 실온 값으로 옮기지 않는다.
> 상세: digest §3a · §3b · §6 · §7 · §10 · §12.

### b-4. (권장) `comparison_vs_ours_DEM.md` §A (압밀 / porosity) 에 한 줄

> 2026-11-25 추가 — `park2025_li_kinetics_agc_porous_interlayer_reservoir_free` [Park25AgC] — Ag–C 층 (카본블랙 : Ag 3 : 1 · PVDF 5 % · 캐스팅 · **7.2 ± 0.2 µm** · 시료 9 개) 을 Li₃PS₄ 에 **단축 380 MPa** 로 붙인 뒤 cryo FIB-SEM 단면 **2D 기공률 29.1 / 29.2 / 29.2 %** (단면 한 장 + 반복 한 장 · 분할 문턱 미기재 · 기공 최대 90 × 10⁻³ µm² ✎ 등면적 지름 0.34 µm) → Li 1 mAh cm⁻² 뒤 4.4 / 8.2 / 3.1 % · ✎ 처음 기공 부피 (2.1 µm) 가 층 안 Li 금속 0.5 mAh cm⁻² (2.4 µm) 보다 작아 29 % 를 3D 값으로 확정하지 않는다 · 같은 질문의 다른 2D 값 = `metzler2026_…` 26.7 → 18.5 % (500 MPa · ImageJ).

---

## (c) `pdf_map.tsv`

**필요 없어요** — digest 를 쓴 뒤 `extract_figures.py --inbox --only park2025_li_kinetics` (매칭표만) 가 본문 + SI 를 자동으로 붙였어요 (`[제목 82%]`). 굳히고 싶으면 한 줄:

```
park2025_li_kinetics_agc_porous_interlayer_reservoir_free	park2025_agc_porous_interlayer
```

---

## (d) 추가로 먹일 만한 논문 (≤ 8 · 최근 먼저)

발견 검색: Crossref REST 주제어 검색 5 번 (제목 없이 · 2025-01 이후 · 'silver carbon interlayer lithium creep pore size anode-free' · 'Coble creep lithium porous interlayer solid-state' · 'Ag-C interlayer stack pressure lithium plating morphology' · 'carbon interlayer porosity lithium deposition location sulfide' · 'silver nanoparticle size interlayer lithium alloying') + DOI 확인 15 번. 일반 클라이언트 이름 · 개인정보 없음. OpenAlex (피인용 목록) 는 프록시가 막아서 못 썼어요 (한 번만 시도). 대조: `litdb/papers/` · `litdb/_curation/*/` grep (DOI · 제목).

| # | 논문 (저자 · 저널 권, 첫쪽 (연도)) | 왜 (이 논문의 빈칸 · 우리 축) | litdb | 목록 |
|---|---|---|---|---|
| 1 | Park J., Kim J., Lee S. … Song T. · *Adv. Sci.* 13, e00057 (2026) — "Carbon Interlayer with Uniformly Anchored ZnO Nanoparticles: Surface-Energy-Driven Coble Creep for Practical Anode-Free Solid-State Batteries" · DOI 10.1002/advs.202600057 | 이 논문의 Coble 틀에 **표면 · 계면 에너지 항**을 넣은 쪽 (제목 기준) — W_ad 7 절 '친Li ↔ 크리프 속도' 를 잇는 다리 | 없음 | 없음 · Crossref 확인 |
| 2 | Hong S., Lee Y., Oh H. … Jung H. · *ACS Energy Lett.* 11, 5051 (2026) — "Mesoporous Carbon Hosts with Tailored Pore Structure for Lithium Deposition in Anode-Free All-Solid-State Batteries" · DOI 10.1021/acsenergylett.6c00964 | 기공 크기 → Li 석출 (이 논문 J ∝ 1/r² 의 실험 시험) · DEM 기공 분포 입력 | 없음 | 없음 · Crossref 확인 |
| 3 | Han E., Cho Y., Jeon Y. … Song H. · *Small* 21, e04978 (2025) — "Lithium Metal Ingrowth Toward a Porous Structure via Coble Creep along Lithium-Carbon Interface Without Ionic Conductors" · DOI 10.1002/smll.202504978 | **Li \| C 계면을 따라 도는 Coble 크리프** — 이 논문에 숫자가 없는 δs · Ds 의 실험 쪽 · W_ad 7-1 Li \| C 행 | 없음 | 없음 · Crossref 확인 |
| 4 | Kamikawa Y. *et al.* · *Adv. Sci.* 12, 2404840 (2025) — "Unraveling the Mechanisms of Lithium-Alloy Plating in Ag–C Anode: In situ SEM Study" · DOI 10.1002/advs.202404840 | Ag–C 층 Li–Ag 석출의 **in situ** SEM — 이 논문 (사후 단면) 의 시간축 · 8-3 | 없음 | 없음 · Crossref 확인 (Crossref 저자 목록이 1 명뿐 — 공저자 확인 필요) |
| 5 | Oh J. · *Batteries & Supercaps* 9, e70514 (2026) — "Low Stack Pressure Anode Interfaces in Sulfide-Based All-Solid-State Batteries With Lithium Plating" · DOI 10.1002/batt.70514 | 황화물 저압 음극 계면 리뷰 — DEM 압력 단계 · 8-4 의 지도 | 없음 | 없음 · Crossref 확인 |
| 6 | Cakmakci Lee N., Lee H., Kim G. … Jeong Y. · *Fibers Polym.* 27, 3673 (2026) — "Surfactant-Assisted Silver Nanoparticle Anchoring on CNT Interlayer for Anode-Free Solid-State Batteries" · DOI 10.1007/s12221-026-01457-x | Ag NP 를 **CNT 섬유**에 붙인 층 — DEM 의 Ag–C 층 ↔ 섬유 (VGCF) 기하 대조 | 없음 | 없음 · Crossref 확인 |
| 7 | Park S. H., Jun D., Jung J. E., Lee S. G., Lee G. H., Lee Y. J. · *J. Mater. Chem. A* 10, 21995 (2022) — "Clarification of Li deposition behavior on anodes with a porous interlayer in Li-free all-solid-state batteries" · DOI 10.1039/d2ta06466a (ref 14) | 이 논문의 **직접 선행** — 기공 크기 · 표면 성질 · 점착 비대칭 · Coble (이 논문이 다시 쓰는 틀의 원전) · 8-3 | 없음 (`xie2024_…` · `sandoval2025_…` 에 인용만) | **목록에 있음** (11-24b `extra_papers` #12) · Crossref 확인 |
| 8 | Yoon S. G., Vishnugopi B. S., Alsaç E. P. … Mukherjee P. P., McDowell M. T. · *ACS Nano* 18, 20792 (2024) — "Synergistic Evolution of Alloy Nanoparticles and Carbon in Solid-State Lithium Metal Anode Composites at Low Stack Pressure" · DOI 10.1021/acsnano.4c07687 (ref 8) | 합금 NP + 탄소 복합 음극 · 저압 · 같은 연속체 그룹 (Vishnugopi · Mukherjee) — 입경 · 압력 축 대조 | 없음 | 없음 · Crossref 확인 |

- 그 밖 (≤ 2024 · 8 편 밖 · 다 Crossref 확인): Park S. H. *et al.* *Adv. Sci.* 9, 2203130 (2022) (ref 9 · 기공 크기 의존 Li 석출 3D 음극 · DOI 10.1002/advs.202203130) · Chen Y. *et al.* *Nature* 578, 251 (2020) (ref 18 · Coble 크리프 원전 관찰 · DOI 10.1038/s41586-020-1972-y) · Xu C. *et al.* *PNAS* 114, 57 (2017) (ref 25 · 작은 Li 의 항복 · DOI 10.1073/pnas.1615733114 · `sedlatschek2026_…` 에 인용만) · Cho S. *et al.* *Adv. Funct. Mater.* 32, 2208629 (2022) (ref 34 · Ag 대 AgLi 흡착 에너지 근거 · DOI 10.1002/adfm.202208629) · Røe I. T., Schnell S. K. *J. Mater. Chem. A* 9, 11042 (2021) (ref 12 · Cu 위 Li 표면 확산 DFT · DOI 10.1039/d1ta02300d — W_ad 7 절 흡착 · 확산 쪽).
- 같은 배치 병렬 편: ref [11] Sandoval *et al.* *Joule* 7, 2054 (2023) = `sandoval2023_alloy_interlayers_structural_electrochemical_evolution_anode_free` (서지만 · 합친 뒤 교차 링크).

---

## (e) W_ad · DEM-DFT 보고서 (`docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html`) 에 쓸 거리

### e-1. 7-1 표 (대상 표면) — 행마다
- **은 (Ag) 행 '같이 볼 것'** — "충전 중 Li 가 만나는 은 쪽 면은 Li-풍부 합금" 에 **조건**을 붙일 근거: 첫 1 mAh cm⁻² 뒤 200 nm Ag 는 1 MPa 에서 금속 Ag 가 남고 (LiAg · Li₉Ag₄ 와 함께) · 50 nm Ag 나 5 MPa 면 Ag 가 사라져 Li₉Ag₄ · Li₁₀Ag₃ 만 (`Fig. 4` · p.5–6 · **직접 봤음**). 10 mAh cm⁻² 뒤 석출층 전체에 bcc 봉우리 (`Fig. 7` · 봤음) — 상 이름 'Li₀.₉₈Ag₀.₀₂' 는 bcc Li 와 겹쳐 '묽은 고용체' 근거로는 약함 (EDS `Fig. S10` · `S17` 정성 쪽이 Ag 이동의 근거).
- **카본블랙 행** — Super C65 (50 nm) · 구조 정보 (Raman · BET · XPS) 0 → 모형 선택 근거는 못 됨. 리튬화 먼저 (충전 곡선 경사 · `Fig. S4` · 봤음) 는 `hiraoka2025_…` 와 같은 방향.
- **스테인리스 행** — SS316 10 µm 셀 선례 **둘째** (Lee 2020 은 LPSCl · 이 편은 Li₃PS₄). 테이프 박리에서 SUS 박만 떨어지고 층은 SE 에 남음 (`Fig. S6` · 봤음 · 정성 · 380 MPa 뒤) → 'C \| 스테인리스' 가 운전 중 처음 벌어질 계면이라는 7-1 문장을 받쳐 줌.

### e-2. 8-3 (Ag/C 층에서 Li 는 어디에 쌓이나)
- **새 문장 후보의 핵심**: 같은 층 · 같은 계면에서 압력 · 전류 · Ag 입경으로 자리가 뒤집혔다 (`Fig. 1` · `Fig. 5` · `Fig. S19` · 봤음) → 기존 8-3 의 "핵생성 세기 (W 의 순서) 하나로 Li 가 쌓이는 자리를 예측하지 않는다" (Metzler 2025) 와 같은 결론을 **다른 손잡이 (속도)** 로 보여 줌.
- 저자 설명은 Coble 크리프 플럭스 대 환원 플럭스 (`Fig. 3c,e` · 봤음) — 경쟁식의 상수 (K · δs · Ds · σ · φ) 가 없다는 한정어를 같이.
- **11-24b digest 와 맞는지**: `lee2020_…` (60 nm Ag · 2 MPa · 60 °C → 집전체 쪽) = 이 편의 '작은 Ag + 충분한 압력 → 집전체 쪽' 과 같은 방향 ✓ · `xie2024_…` 의 점착 세기 입력 순서 (SE/BL > BL/CC) = 이 편 테이프 박리와 같은 방향 ✓ · `metzler2026_…` (얇은 C + 스퍼터 Ag · 4 MPa · LPSCl) 는 Li 가 Cu \| C 사이 · C 가 SE 쪽으로 밀림 — 이 편의 Ag 200 · 1 MPa (Li 가 SE \| 층 사이 · 층이 집전체 쪽으로 들림) 와 **반대 자리** (층 · 압력 · 계가 다름 — 모순이 아니라 '자리는 조건 의존' 의 예) · `ko2025_…` (가넷 위 Au · Cu 층은 SE 쪽에 Li 가 쌓여 층이 들림) = 이 편 Ag 200 · 1 MPa 와 같은 꼴 ✓ · `spencerjolly2023_…` · `choi2025_…` 의 상 순서 (LiAg → Li₉Ag₄ → Li₁₀Ag₃) = 이 편 200 nm 가 앞 단계에 멈춘 꼴 ✓.

### e-3. 8-4 (공극 · 적층압 · 균열 — DEM · 연속체)
- **Li 흐름 법칙**: 서브 µm 기공 안 Li 는 확산 크리프 — 1 µm Li 항복 95 MPa (298 K) · 35 MPa (363 K) (ref 25 인용 · p.2) ≫ 적층압. 8-4 의 'Li 금속은 적층압 아래에서 늘 흐른다 (벌크 항복 0.73–0.81 MPa · 크리프 지수 6.56)' 옆에 "층 기공 안에서는 다른 법칙 (σ 선형 · 크기 의존)" 한 줄.
- **층 응집 파괴**: 탄소만 층은 1 MPa 에서 수십 µm 조각으로 갈라지고 그 틈으로 Li 가 새어 나옴 (`Fig. S7` · `S8` · 봤음) — 8-4 의 'Li 침투는 Li 로 찬 균열이 열리며 자란다' (SE 쪽) 의 층 쪽 짝.
- **압력 두 단계 (1 · 5 MPa)**: 5 MPa 면 셋 다 집전체 쪽 · 석출 평탄이 40–80 mV 덜 깊음 (`Fig. S4` figure-read).

### e-4. DEM 쪽 기하 숫자 — 측정 / 공칭 / 가정 / 우리 산수 (digest §3a 표의 요약)

| 양 | 값 | 성격 | 근거 (직접 봤는지) |
|---|---|---|---|
| 층 두께 | 7.2 ± 0.2 µm (9 시료 7.1–7.4) | 측정 (단면 SEM · 380 MPa 뒤로 보임) | p.9 · `Fig. S2` (봤음) |
| 처음 기공률 | 29.1 / 29.2 / 29.2 % | 측정 — 2D cryo FIB-SEM · 단면 한 장 + 반복 · 380 MPa 뒤 | `Fig. S13` · `S14` (봤음) |
| 충전 1 mAh cm⁻² 뒤 기공률 | 4.4 / 8.2 / 3.1 % | 측정 (2D) | p.3 · `Fig. 2` (봤음) |
| 기공 크기 | 처음 ≤ 90 × 10⁻³ µm² (✎ ≤ 0.34 µm) · 충전 뒤 대부분 < 20 × 10⁻³ µm² (✎ < 160 nm · 본문 '≈100 nm') | 측정 (2D) | `Fig. 2g` · `S13g` (봤음) |
| 카본블랙 입경 | 50 nm (Super C65) | 공칭 | p.3 · `Fig. S1a` (봤음) |
| Ag 입경 | 200 · 50 nm (SkySpring) · SEM 에서 200 nm 는 µm 덩어리 | 공칭 · figure-read | `Fig. S1b,c` (봤음) |
| 질량비 | 카본블랙 : Ag = 3 : 1 · 카본블랙 : PVDF = 95 : 5 | 레시피 | p.9 |
| Ag 부피 분율 | 고체 중 5.2–5.9 % · 층 전체 3.7–4.2 % | ✎ (카본블랙 1.8–2.1 g cm⁻³ 가정 · 29 % = 3D 가정) | — |
| 적재량 | Ag ≈0.28–0.32 · 카본블랙 ≈0.83–0.95 mg cm⁻² | ✎ (같은 가정 · 원문 없음) | — |
| 입자 수 밀도 | Ag 50 nm ≈560–640 µm⁻³ · Ag 200 nm ≈9–10 µm⁻³ · 카본블랙 1 차 ≈1 × 10⁴ µm⁻³ | ✎ (구형 가정) | — |
| 집전체 · SE | SS316 10 µm · Li₃PS₄ 80 mg Ø 10 mm (80 MPa · ✎ ≈0.5–0.7 mm) | 레시피 · ✎ | p.9–10 |
| 압력 | 조립 380 MPa (층 \| SE · 단축) · 10 MPa (Li 포일) · 운전 1 · 5 MPa · 80 °C | 조건 | p.10 |
| Li 석출 | 2 mAh cm⁻² ≈9.7 µm (✎) · 5 MPa 단면 ≈9–12 µm (figure-read) · 섬유 수백 nm → 기둥 수 µm | ✎ · 그림 · 본문 | `Fig. 1d–f` · `S11` (봤음) |
| 모형 영역 | 응력 2 × 2 µm 2D (Ag ≈80 대 ≈8 개) · 확산 600 × 600 nm | 모형 가정 | `Fig. 3a,b` · `S16` (봤음) |
| 모형 물성 | E_Ag 90 (50 nm) / 70 (200 nm) · E_C 9.5 GPa · ν 0.37 / 0.3 · Ω_Li 1 × 10⁻⁵ (Ag) / 2 × 10⁻⁶ (C) m³ mol⁻¹ · c 1000 mol m⁻³ | 모형 입력 (문헌) | `Table 1` (글자층 · 크롭 대조) |
| 크리프 척도 | J/K (50 nm) ≈0.42 × 10⁻³ µm s⁻¹ per MPa · ✎ δs Ds ≈2.0–2.4 × 10⁻²² m³ s⁻¹ | figure-read · ✎ | `Fig. 3c` (화소 판독) |

### e-5. 보고서 문장 후보 (랩 인용 꼴 · 회사 이름 없음 · 내부 사정 없음)
1. (8-3) "Li 가 쌓이는 자리는 압력 · 전류 · Ag 입경으로 뒤집혔다. 카본블랙 : Ag = 3 : 1 (질량) 의 7.2 µm 층을 스테인리스 박 위에 두고 Li₃PS₄ 에 붙인 80 °C 셀에서, 1 MPa · 0.5 mA/cm² 면 Ag 200 nm 층은 Li 가 고체전해질과 층 사이에 쌓여 층이 들렸고 Ag 50 nm 층은 집전체 쪽에 쌓였다. 5 MPa 에서는 세 층 모두 집전체 쪽이었고, 전류를 0.1 mA/cm² 로 낮추면 같은 층에서도 집전체 쪽에 조밀하게 쌓였다. 저자는 이를 층의 서브 µm 기공을 지나는 Li 확산 크리프와 Li⁺ 환원 속도의 경쟁으로 설명했다 — 경쟁식의 상수는 적혀 있지 않다. 테이프로 뗀 시험에서는 집전체 쪽이 먼저 떨어졌다 (Adv. Energy Mater., 15, 2405129 (2025)). W 의 순서는 '느릴 때 어느 계면이 열리나' 의 후보이고 자리의 예측이 아니다."
2. (7-1 Ag 행) "Ag 입경과 압력이 합금이 끝까지 가는지를 바꿨다 — 첫 1 mAh/cm² 뒤 200 nm Ag 는 1 MPa 에서 금속 Ag 가 남았고, 50 nm Ag 나 5 MPa 에서는 Li₉Ag₄ · Li₁₀Ag₃ 만 보였다 (Adv. Energy Mater., 15, 2405129 (2025))."
3. (8-4) "층 기공 안의 Li 는 확산 크리프로 움직인다고 본 연구가 있다. 지름 1 µm Li 의 항복 응력 (실온 약 95 MPa) 이 적층압 (1–5 MPa) 보다 훨씬 커서, 서브 µm 기공 안의 Li 는 전위 소성이 아니라 계면 · 표면 확산으로 흐르고 그 속도는 응력에 비례하고 기공 크기의 제곱에 반비례한다는 틀이다 (Adv. Energy Mater., 15, 2405129 (2025) · 항복 값은 그 논문이 인용한 PNAS, 114, 57 (2017)). 벌크 Li 의 멱법칙 크리프를 층 안 기공에 그대로 쓰지 않는다."
4. (8-4 · DEM) "같은 배합의 7.2 µm Ag–C 층을 380 MPa 로 고체전해질에 붙인 뒤 cryo FIB-SEM 단면으로 잰 면적 기공률은 약 29 % 였고, 첫 1 mAh/cm² 뒤에는 3–8 % 로 줄었다 (Adv. Energy Mater., 15, 2405129 (2025)) — 단면 한 장씩의 2D 값이다."
5. (8-4) "탄소만 쓴 층은 1 MPa 에서 수십 µm 조각으로 갈라지고 그 틈으로 Li 가 새어 나왔다 (Adv. Energy Mater., 15, 2405129 (2025)) — 층 자체의 응집 파괴가 Li 길이 되는 경우다."
- 8-7 표에 넣을 행 (꼴은 기존 행과 같게): `Adv. Energy Mater., 15, 2405129 (2025) | Li | Ag–C 다공 층 · Li₃PS₄ · 80 °C · 단면 SEM · cryo FIB-SEM · XRD · 연속체 | 8-3 자리 = 속도 경쟁 · 8-4 층 안 크리프 · 2D 기공률`.

### e-6. 11-24b digest 들의 '🔗 이어 읽기 · 바로잡기' 절 · 빈칸과의 대조 (그 파일들은 안 고쳤어요)
- `kang2026_…` 🔗 절 L443 · §10 L445 "흔한 Ag/C 층 기공 ≈29 % (Park 2025)" → 원문 29 % 는 **이 배합 · 2D · 380 MPa 뒤** 의 값 · '흔한' 은 원문 표현 아님 · 충전 뒤 3–8 % 도 같이 · 그리고 같은 카드 표 S3 의 D_interlayer · κ_e 출처 불일치 (메인이 먼저 알 것 2).
- `metzler2026_…` L137 ("흔한 Ag/C 층은 ≈29 % (ref S5)") → 원문 확인 (29.1–29.2 %) · 같은 2D 부류.
- `lee2020_…` §10-⑤ · §14 · §16 (기공 미기재) → 이 논문 값은 다른 배합 · 다른 압착이라 Lee 의 칸을 채우지 않음 · '비슷한 배합의 대역 참고' 로만 · ✎ 29 % 를 3D 로 두면 이 배합 Ag ≈0.28–0.32 mg cm⁻² (Lee 의 질량 숫자 0.05–0.11 mg cm⁻² 의 3–6 배 — Lee §10-⑤ 불일치와 같은 쪽).
- `xie2024_…` §10 (다공도 40 % 'demonstrative') → 측정 대역 참고 = 2D 29 % (처음) · 3–8 % (충전 뒤).
- `sandoval2025_electro_chemo_mechanics_anode_free_ssb` 🔗 절 → 같은 모형 계열 **아님** (관점 논문 · 자체 모형 0 · 같은 EFRC · 공저자 넷 겹침 · 이 편 미인용).

### e-7. 우리 쪽 원고 · 카드와 닿는 곳 (내부용 — 공유 보고서에는 안 씀)
- **[우리 원고] `ahn2026_cej_agno3_pvp_li3n_anodefree`** 의 Coble 항 D_pore 25 / 45 / 50 nm 는 'Assumed' — 이 논문의 측정 기공 (2D · Ag 50 층 충전 뒤 대부분 < 160 nm · 처음 ≤ 0.34 µm) 이 가정 대역의 대조 근거가 될 수 있어요 (배합 · 45 °C · 20 MPa 와 다름 · 값 이식 아님).
- **[우리 그룹] `kang2026_…`** — 메인이 먼저 알 것 2.

---

## (f) 그림 · 자료 크롭 요약

- 크롭 **32 장** = 본문 그림 7 (`fig_1`–`fig_7`) + 본문 표 1 (`tab_1`) + SI 그림 23 (`fig_S1`–`fig_S23`) + SI 표 1 (`tab_S1`) · 전부 도구 · **손 크롭 0 · 다시 자름 0 · 빈칸 0**.
- `tab_S1` = auto_fallback ('아래가 백지라 캡션 위를 잘랐다') — 눈으로 보니 표 두 블록 (Ag–C 200 · 50 nm) + 아래 캡션이 다 들어 있어 맞아요.
- `figures.json` 의 `missing_labels` 14 건 (`f8`–`f21`) = 본문 p.8 'Figure 21b' 한 줄 (SI 그림 오기 · 아마 `Fig. S22b`) 때문 — 실제로 빠진 그림 없음 · `manual_crop` 불필요.
- **본 것: 32 장 전부** (Read). 확대 · 화소 판독 6 곳 (`Fig. 6i` · `Fig. S22b,c` · `Fig. 3c` · `Fig. 3e` · `Fig. 3a,b` · 본문 p.2 문장) — scratchpad 에만 두고 저장 안 했어요.
- 동영상 · 원자료: 없음 (SI 에 보충 영상 · 원자료 목록 없음 · batch.json not_received 도 빈칸).

## (g) Jeff Sakamoto 저자 여부

**아니에요.** 저자 다섯 = Se Hwan Park · Kaustubh G. Naik · Bairav S. Vishnugopi · Partha P. Mukherjee · Kelsey B. Hatzell (Crossref 저자 목록도 같음). Sakamoto 는 참고문헌 [3] (Wang 2020 *Nat. Commun.*) · [6] (Jeong 2024 *Adv. Energy Mater.*) · [17] (Haslam 2022 *J. Power Sources*) · [28] (Fuchs 2024 *Nat. Mater.*) 에만 나와요 → INDEX 행에 🏷 를 달지 않아요.
