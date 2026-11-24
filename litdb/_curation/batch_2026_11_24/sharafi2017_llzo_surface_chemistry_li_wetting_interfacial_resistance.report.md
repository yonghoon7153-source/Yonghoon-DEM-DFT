# 끝 보고 — sharafi2017_llzo_surface_chemistry_li_wetting_interfacial_resistance (2026-11-24 · litdb-curator · 배치 #4)

쓴 파일 셋뿐이다.
- digest `litdb/papers/sharafi2017_llzo_surface_chemistry_li_wetting_interfacial_resistance.md` (363 줄 · 표 10 개 · 칸 수 검사 어긋난 줄 0 · Python-Markdown 렌더에서 표 10 개)
- 그림 `litdb/figures/sharafi2017_llzo_surface_chemistry_li_wetting_interfacial_resistance/` (크롭 11 장 + 동영상 프레임 43 장 + 1 fps 꼬리 시트 2 장 + figures.json)
- 이 보고 파일

`litdb/figures/_sources.json` 은 추출 도구가 다시 썼다 (손 안 댐). 공유 파일 · git 은 안 건드렸다.
⚠ 메인 체크포인트 커밋 (4739c5a7 · 55c16687) 에 digest 의 앞선 판이 들어가 있다. 지금 작업 트리와는 5 줄 다르다 (본문 정확도 수정). 다음 커밋에 같이 넣으면 된다.

확인한 것
- 웹앱 `/paper/<slug>` 200 · `paper_figure_notes` 가 11 개 키 (f1–f5 · fS1–fS4 · tS1 · tS2) 에 붙는다. 동영상 행은 Fig. 1–3 에 잘못 붙지 않는다 (첫 칸을 로마 숫자로 썼다).
- `_paper_pis` = `['sakamoto']` · digested = 2026-11-24 · `pytest webapp/tests/test_v3_literature.py` 20 passed.
- `build_index.py --check`: 이 slug 는 "어느 인덱스에도 없음 [dft]" 와 "comparison_vs_ours.md 미편입" 두 곳에만 뜬다. 아래 (a) · (b) 를 넣으면 풀린다.
- talk 인입 대기열 (`litdb/talks/*`) 에는 이 논문이 없다. 역링크는 필요 없다.
- `--audit` 에서 이 slug 는 경고 없음 · `--inbox --only sharafi2017 --dry` 는 본문 · SI 를 자동으로 짝지었다 (제목 52 %).

---

## (a) `litdb/INDEX.md` 에 넣을 행

**절**: `## 🧲 계면 점착 · 인터레이어 트랙 — LPSCl 이 한쪽 면인 계면/벌크 역학의 실측 앵커 (2026-09-23 신설)` (표 `| slug | 논문 | 축 |`)

같은 절 머리 인용 블록의 예외 줄들 (giovannetti2008 · wang2015) 다음에 아래 한 줄을 더한다.

```
> ⛔ 예외 (2026-11-24): `sharafi2017` 은 G_c 가 아니라 **DFT(PBE) 점착 일 W_ad + 녹은 Li 접촉각**이다 — 가넷 LLZO 계면이라 우리 DFT W 와 **같은 줄 금지** · 방법 (같은 방법 · 같은 Li 면의 σ_Li · registry → UBER → 이완 → Young–Dupré) 과 순서 (LLZO ≫ LiOH > Li₂CO₃) 만 이식한다.
```

행:

```
| `papers/sharafi2017_llzo_surface_chemistry_li_wetting_interfacial_resistance.md` **(본문 8 pp + SI 4 pp + SI 동영상 3 · 크롭 11장 (도구 9 + 손 크롭 2 = `Fig. S1` · `Table S1`) 중 10장 실독 + 판독 확대 3 · 동영상 프레임 43장 (5 s 간격) + 1 fps 꼬리 시트 2)** | 🏷 **Jeff Sakamoto 공저** · **[외부·exp+DFT(PBE)·⭐⭐⭐ Li 친화성 정량 (DFT W_ad → Young–Dupré θ → 녹은 Li 접촉각) 의 선례 · ⛔ G_c 실측과 다른 부류 — DFT 점착 일 + 녹은 Li 젖음각 · 가넷 LLZO (argyrodite 아님)]** ✅ **Asma Sharafi**/**Eric Kazyak** (공동1)/A. L. Davis/S. Yu/T. Thompson/**D. J. Siegel**/**Neil P. Dasgupta\***/**Jeff Sakamoto\*** (U. Michigan), "**Surface Chemistry Mechanism of Ultra-Low Interfacial Resistance in the Solid-State Electrolyte Li₇La₃Zr₂O₁₂**" — ***Chem. Mater.* 29, 7961–7968 (2017)**, DOI `10.1021/acs.chemmater.7b03002`. Li₆.₂₅Al₀.₂₅La₃Zr₂O₁₂ 표면의 Li₂CO₃ · LiOH 오염이 Li 를 밀어낸다 — 녹은 Li 접촉각 Li₂CO₃ **142°** · DP-LLZO **146°** · WP **141°** (그림 142°) · WP + 500 °C HT **95°** (반복 · 오차 없음) · 동영상 = 오염 표면에서는 굴러 떨어지고 HT 표면에서는 뒤집어도 붙어 있다. VASP-PAW **PBE (분산 보정 없음 · LiOH 만 vdW-DF2)** · 450 eV · σ_Li = Li(001) 20 층 **0.452 J m⁻²** · registry 강체 격자 → UBER (1.96 / 3.04 / 2.32 Å) → 이온 이완 · 진공 8 Å · `Table S2` W_ad Li\|LLZO **0.667** (θ 61.6°) · Li\|LiOH **0.191** (125.3°) · Li\|Li₂CO₃ **0.096 J m⁻²** (142.0°). 175 °C 12 h 전처리 뒤 R_Li–LLZO **400 → 2 Ω cm²** (HT 없음 → 400–500 °C · N = 3) · CCD **0.3 mA cm⁻²** · ±0.2 mA cm⁻² 100 사이클. ⚠ 강체 탐색 W (`Fig. S2`–`S4` figure-read ≈0.48 / 0.05 / 0.17) 와 최종 값의 차를 설명 안 함 (Li\|LLZO θ 86 → 62°) · 'Li 가 LLZO 를 잘 적신다' 는 계산 (측정 95° > 90°) · '≈15 % 남은 오염' 은 `Fig. 1d` 로 재현 안 됨 · `Fig. 4c` 계면 호 figure-read ≈270 vs 본문 ≈400 Ω cm² · 계면 하나 값인지 둘 합인지 미기재 | 점착 보고서 7 절 (Li 친화성 · W → θ) 의 방법 선례 · 오염 상 (Li₂CO₃ · LiOH) = 소Li 의 DFT · 실측 앵커 · ⛔ 우리 W 와 같은 줄 금지 · 순서만 이식 |
```

## (b) `comparison_vs_ours.md` 에 넣을 줄

물성 4 축 (A–D) 에는 넣지 않는다 (가넷 · 우리 계 값 없음). 두 군데에 넣는다.

① `## 📑 Reference key (출처 약칭)` 표 (`| 약칭 | 논문 (저자·년·저널) | digest/status | 유형 |`):

```
| **[Sharafi17Wet]** 🔧 **방법 선례 — DFT W_ad → Young–Dupré θ → 녹은 Li 접촉각 대조** · ⛔ **가넷 LLZO — A–D 물성 4축 진입 금지** · ⛔ **우리 W 와 같은 줄 금지** (PBE 분산 없음 · 강체/이완 미분리 · LLZO 종결 미기재) | **Asma Sharafi**/**Eric Kazyak** (공동1)/A. L. Davis/S. Yu/T. Thompson/D. J. Siegel/**Neil P. Dasgupta\***/**Jeff Sakamoto\*** (U. Michigan) 2017 ***Chem. Mater.* 29, 7961–7968** (DOI 10.1021/acs.chemmater.7b03002) — "Surface Chemistry Mechanism of Ultra-Low Interfacial Resistance in the Solid-State Electrolyte Li₇La₃Zr₂O₁₂" | ✅ `papers/sharafi2017_llzo_surface_chemistry_li_wetting_interfacial_resistance.md` (2026-11-24 · 그림 10 장 실독 · 동영상 3 편 프레임) | exp + DFT (Li 금속 \| 고체 점착 · 젖음) |
```

② `## E. 환원 / 음극(Li 금속) 계면` 표 (`| 주장 | 출처 | 우리 | 일치 |`) 맨 위:

```
| **🆕 (2026-11-24) Li 금속 젖음은 표면 오염층이 가른다 — DFT (PBE · 분산 없음) Li\|LLZO W_ad 0.667 J m⁻² (θ 61.6°) ≫ Li\|LiOH 0.191 (125.3°) > Li\|Li₂CO₃ 0.096 (142.0°) · 녹은 Li 실측 Li₂CO₃ 142° · DP-LLZO 146° · WP 141° · WP + 500 °C HT 95° · 175 °C 전처리 뒤 R_Li–LLZO 400 → 2 Ω cm²** — ⚠ 가넷 LLZO (argyrodite 아님) · 순서는 강체/이완 · σ_Li ±10 % 에 튼튼하고 깨끗한 계면의 절대 θ 는 이완 단계에 ≈25° 흔들린다 (강체 figure-read ≈0.48 → 0.667 · θ 86 → 62°) · 측정 95° 는 90° 를 넘는다 | **[Sharafi17Wet]** `Fig. 2` · `Fig. 3` · `Table S2` · `Fig. S2`–`S4` · `Fig. 1d` · `Fig. 4d` | 우리 Li\|X W → θ 는 **아직 없다** (점착 보고서 `docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html` 7 절 = 제안) — W 값은 `db/properties/adhesion.json` · `db/properties/wad_*` 에서만 · 오염 상 Li₂CO₃ · LiOH 는 LPSCl 건조실 노출 산물이기도 하다 (`kim2026_moisture_surface_degradation_lpscl_dryroom` 반응식 1 · 2) | 🔧 방법 선례 (값 비교 없음) |
```

(선택) `comparison_vs_ours_DEM.md` **§I** 에 카드 하나 (I-10 다음):

```
### I-11. `sharafi2017_llzo_surface_chemistry_li_wetting_interfacial_resistance` — ★★ Li|X 점착 일 → 젖음각 (Young–Dupré) 의 DFT · 실측 대조 선례 — G_c 가 아니다
- 양: DFT (PBE) W_ad (Li|LLZO 0.667 · Li|LiOH 0.191 · Li|Li₂CO₃ 0.096 J m⁻²) + 녹은 Li 접촉각 (95–146°) — 박리 · 파괴 에너지 (G_c) 와 다른 부류.
- 옮길 것: σ_Li 를 같은 방법 · 같은 Li 면으로 (Li(001) 0.452 J m⁻²) · registry 강체 탐색 → UBER → 이완 → θ · 순서 비교로만.
- 옮기지 않을 것: 절대 θ (이완 단계에 ≈25° · σ_Li ±10 % 에 ±10° 흔들림) · '≈15 % 잔류' 설명.
- DEM 쪽: Li–벽 접촉각 같은 입력이 필요하면 이 논문의 순서 (깨끗한 산화물 > 수산화물 > 탄산염) 를 정성 근거로만 쓴다.
```

## (c) `pdf_map.tsv`

필요 없다. 자동 매칭이 본문 · SI 를 짝지었다 (`--inbox --only sharafi2017 --dry` → [제목 52 %] · 본문 `sharafi2017_llzo_wetting_main.pdf` · SI `sharafi2017_llzo_wetting_SI1.pdf`). 원래 업로드 이름 (`4._Surface_Chemistry_Mechanism_of_…`) 으로 바뀌어도 제목 토큰이 그대로라 더 잘 붙는다. 동영상 (.avi) 은 추출 도구 대상이 아니다.

## (d) 추가로 먹일 만한 논문 (≤ 8)

이번 배치 18 편 (Seymour 2021 · Yang 2021 둘 · Wang 2019/2020 · Masias 2019 · Kazyak 2020 · Lee 2022 · Fuchs 2023 · Kim 2026 · Lu 2026 · Sandoval 2025 · Metzler 2025/2026 · Shi 2026 · Cicvarić 2026 · Chatterjee) 은 뺐다.
⚠ **2024–2026 후보는 내가 서지를 자신할 수 있는 것이 이 배치 밖에 없다** — 최근 Ag–C · 공극 · Li 친화성 편은 이미 이 배치에 들어 있다. 아래는 그래서 2020 → 2015 → 1994 순서다.
'서지 확인 필요' 표시는 내 기억이다 (다른 litdb digest 참고문헌으로 맞춘 것은 그렇게 적었다).

| # | 논문 | 왜 | litdb |
|---|---|---|---|
| 1 | Y.-G. Lee et al., "High-energy long-cycling all-solid-state lithium metal batteries enabled by silver–carbon composite anodes", *Nat. Energy* 5, 299 (2020) | **Ag–C 층 원전** — 우리 Ag–C 점착 트랙의 출발점 | 인용만 (spencerjolly2023 · liao2025 · minnmann2021 참고문헌 — 서지 일치) · digest 없음 |
| 2 | J. Kasemchainan et al., "Critical stripping current leads to dendrite formation on plating in lithium anode solid electrolyte cells", *Nat. Mater.* 18, 1105 (2019) | **방전 (stripping) 중 공극** → 다음 도금에서 덴드라이트 · 적층압 | 인용만 (tron2023 · INDEX 등 11 곳 — 서지 일치) · digest 없음 |
| 3 | T. Krauskopf et al., Li 금속 \| Li₆.₂₅Al₀.₂₅La₃Zr₂O₁₂ 전기화학–역학 연구, *ACS Appl. Mater. Interfaces* 11, 14463 (2019) | Li\|LLZO 의 stripping 공극 · 적층압 · Li 크리프 — 이 논문의 '전처리 175 °C' 몫을 가를 대조 | 이름만 (banerjee2020 T12) · digest 없음 · 서지 확인 필요 |
| 4 | N. D. Lepley & N. A. W. Holzwarth, "Modeling interfaces between solids: Application to Li battery materials", *Phys. Rev. B* 92, 214201 (2015) | **황화물 쪽 DFT 점착 방법 원전** (Li\|Li₂S · Li₃PS₄ 등) — 우리 계에 가장 가까운 W 정의 | 인용만 (wang2022 ref 26 등) · digest 없음 · 서지 확인 필요 |
| 5 | A. Sharafi et al., "Impact of Air Exposure and Surface Chemistry on Li−Li₇La₃Zr₂O₁₂ Interfacial Resistance", *J. Mater. Chem. A* 5, 13475 (2017) — Jeff Sakamoto 공저 | 이 논문 ref 13 · **오염층이 생기는 쪽**의 DFT · 실험 짝 — '오염 표면의 효과' 원전 | 인용만 (banerjee2020 ref 261) · digest 없음 · 서지는 이 논문 참고문헌에서 확인 |
| 6 | X. Han et al., "Negating Interfacial Impedance in Garnet-Based Solid-State Li Metal Batteries", *Nat. Mater.* 16, 572 (이 논문 참고문헌 표기 2016) | ALD Al₂O₃ 로 가넷을 친Li 로 — 녹은 Li 젖음 대비의 코팅 쪽 대조 | 인용만 (banerjee2020) · digest 없음 · 서지는 이 논문 ref 9 |
| 7 | C.-L. Tsai et al., "Li₇La₃Zr₂O₁₂ Interface Modification for Li Dendrite Prevention", *ACS Appl. Mater. Interfaces* 8, 10617 (2016) | **Au 스퍼터 층** (58 Ω cm²) — Li 합금 귀금속 층의 원형 → Ag 층과 같은 축 | 없음 · 서지는 이 논문 ref 8 |
| 8 | J. R. Smith, T. Hong, D. J. Srolovitz, "Metal-Ceramic Adhesion and the Harris Functional", *Phys. Rev. Lett.* 72, 4021 (1994) | 이 논문 ref 34 · **UBER 로 계면 거리 · 점착을 맞추는 방법 원전** | 없음 (wang2015 의 Srolovitz 는 다른 논문) · 서지는 이 논문 참고문헌에서 확인 |

## (e) DEM-DFT 점착 보고서 7 절에 쓸 거리

| 보고서 7 절 축 | 쓸 점 | 쪽 · 그림 · 표 | 직접 봤나 |
|---|---|---|---|
| Li 친화성 (실험 정의) | 녹은 Li sessile drop — Li₂CO₃ 142° · DP 146° · WP 141° (그림 142°) · WP + 500 °C HT 95° · 측정법 (Li 산화막 걷기 · 데운 주사기 · Ar 300 °C 핫플레이트 · ImageJ 접선) · 동영상 = 굴러 떨어짐 vs 뒤집어도 붙음 | p. 7963 · `Fig. 2` · p. 7966 'Contact Angle Measurements' · SI Video 1–3 | `Fig. 2` 봤다 · 동영상은 프레임 43 장 (접촉 시트) + 원본 크기 14 장 + 1 fps 꼬리 시트 2 장 |
| Young–Dupré cos θ = W/γ_Li − 1 | W_ad = σ_Li (1 + cos θ) · σ_Li = Li(001) 20 층 PBE **0.452 J m⁻²** (본문 반올림 0.45) · `Table S2` 의 θ 는 0.452 로 정확히 재현 (우리 산수) · W = γ ⇔ 90° · W = 2γ ⇔ 0° (= Seymour 문턱) | p. 7963 · p. 7966 'DFT Calculations' · `Table S2` (SI p. 2) | `Table S2` 는 SI 쪽 렌더와 PDF 글자로 읽었다 (PNG 는 안 열었다) |
| DFT 경향 ↔ 측정 접촉각을 맞춘 방법 | registry 강체 격자 (5 × 5 @ 2 Å · 4 × 4 @ 3 Å) → UBER 거리 → 이온 이완 → W → θ · Li₂CO₃ 142 vs 142° 일치 · 깨끗한 LLZO 62 vs 95° (저자: ≈15 % 잔류 오염) · **순서 LLZO ≫ LiOH > Li₂CO₃ 는 강체 · 이완 · σ_Li ±10 % 에 안 뒤집히고, 절대 θ 는 이완에 ≈25° 흔들린다** (강체 figure-read ≈0.48 → 0.667 · θ 86 → 62°) · σ_Li ±10 % → LLZO ±10° · Li₂CO₃ ±2° (우리 산수) | p. 7963–7964 · p. 7966 · `Fig. 3` · `Fig. S2` · `Fig. S3` · `Fig. S4` · `Table S1` | 다 봤다 (`Fig. S2`–`S4` 는 원본 크기 + SI 쪽 렌더) |
| 오염 표면의 효과 | Li₂CO₃ · LiOH 가 덮인 LLZO 는 순수 Li₂CO₃ 와 같은 각 · DFT W 0.096 / 0.191 J m⁻² · WP 가 탄산염을 줄이고 HT 가 수산화물을 걷는다 · 걷으면 R 400 → 2 Ω cm² (175 °C 전처리 뒤) · 같은 두 상이 LPSCl 건조실 노출 산물 (kim2026 digest 반응식 1 · 2) → Ag–C 층 표면 오염도 따로 계산할 표면 | p. 7962–7964 · `Fig. 1` · `Fig. S1` · `Fig. 4d` | 다 봤다 (`Fig. 1d` 는 500 dpi 확대로 판독) |
| 우리 방법과의 차 (보고서 부록 A 대비) | W_sep (고정 기하) vs W_ad (이완) · D3 유무 · registry 평균 vs 최저 · 진공 8 Å vs 끝점 10 Å · 종결 미기재 — θ 를 낼 때 어느 W 인지 선언 | digest §7a | — |
| 한계 문장의 근거 | 0 K 고체 Li W 로 녹은 Li 각을 겨눈 선례가 Li₂CO₃ 에서만 맞고 깨끗한 LLZO 에서 33° 벌어졌다 → "순서를 견주는 데 쓴다" 를 지지 · 측정 95° 는 90° 를 넘는다 | p. 7963–7964 · `Fig. 2d` · `Fig. 3b` | 봤다 |

## (f) 그림 · 동영상 크롭 요약

- 도구 9 장: `Fig. 1`–`5` · `Fig. S2`–`S4` · `Table S2`.
- 손 크롭 2 장 (figures.json `manual_crop` · `missing_labels` 에 resolved):
  · `Fig. S1` — 그림은 SI 1 쪽 래스터 8 띠, 캡션은 SI 2 쪽 머리에 있어서 도구가 '그래픽 없음' 으로 건너뛰었다.
  · `Table S1` — 캡션이 Fig. S1 캡션과 한 글 블록이라 번호 공백으로 떴다 (SI 2 쪽 벡터 격자).
- 실독 10 장: 그림 9 + `Table S1` (손 크롭 확인용). 판독 확대 렌더 3 장 (`Fig. 1d` · `Fig. 4c` · `Fig. 5a`) 은 임시 폴더라 저장 안 했다. 안 연 것: `tab_S2.png` (SI 쪽 렌더 + PDF 글자로 대신).
- 캡션 고침 (원문은 `caption_auto` 에 보존):
  · f1 · f4 · f5 — 꼬리에 본문이 붙어 있던 것을 잘랐다.
  · fS2 · fS3 · fS4 · tS2 — W_ad 가 제어 문자 셋으로 깨진 것을 'W_ad' 로 바꿨다.
- 동영상: 5 초 간격 프레임 43 장 (`movie1_001–010` · `movie2_001–012` · `movie3_001–021`) + 1 fps 꼬리 시트 2 장 (`movie1_tail_1fps_sheet.jpg` 36–51 s · `movie2_tail_1fps_sheet.jpg` 44–61 s).
  · 5 초 간격이 Video 1 · 2 의 '굴러 떨어지는 순간' 을 놓쳐서 꼬리 시트를 더 뽑았다.
  · figures.json `movies` 블록에 본 장 · 보인 것을 적었다. 웹앱은 `movies` 를 읽지 않는다 (기록용).
- 놓친 것 없음. ⚠ `--clean` 은 손작업 가드에 막힌다 (손 크롭 2) — 정말 다시 뽑으면 동영상 jpg 도 같이 지워지니 그때는 ffmpeg 를 다시 돌린다 (명령은 figures.json `movies.note`).
- ⚠ 프레임 시각 관례: `ffmpeg -vf fps=1/5` 의 프레임 k 는 영상 **(k − 0.5) × 5 s** 다 (PSNR 로 확인: `movie1_010.jpg` = 47.5 s · 54 dB). 같은 명령을 쓴 `litdb/figures/yang2021_atomistic_li_stripping_plating_interface_md/figures.json` 의 `movies.note` 는 '(k−1)·5 s' 라 적었다 → 2.5 s 어긋났을 가능성 (내 파일 아님 · 확인 권고).
- 임시 파일 대조 (조정자 병렬 충돌 주의 반영): 내 임시 글자는 처음부터 scratchpad 의 `sharafi/` 하위 폴더 (`sharafi/main.txt` · `sharafi/SI1.txt`) 에 있었다 · 공용 이름 루트 파일은 안 썼다. PDF 에서 slug 폴더로 다시 뽑은 글자와 sha256 이 같다 (main `d6101686…` · SI1 `3ab68212…`). 제목 · 저자 (Sharafi) · 쪽 표기 (*Chem. Mater.* 2017, 29, 7961–7968) · 핵심 값 (0.452 · 0.667 · 1.96 / 3.04 / 2.32 Å) 도 확인했다. 12 쪽 전부를 PDF 쪽 렌더로도 직접 읽었다 → 다른 논문 글자가 섞이지 않았다. 판독용 확대 렌더 · 접촉 시트도 같은 하위 폴더에서 내 PDF · 내 프레임으로만 만들었다.
- 그림과 본문이 어긋난 곳 (digest §10): WP-LLZO 141° (본문) vs 142° (`Fig. 2c`) · `Fig. 4c` 계면 호 ≈270 vs 본문 ≈400 Ω cm² · `Fig. 1d` 탄산염 3.8 → 11.6 → 4.9 % vs '거의 그대로' · '≈15 % 남음' 재현 안 됨 + 원문의 그림 번호 '2d' 오기 · W 부호 (`Fig. S2`–`S4` 음수 vs `Table S2` 양수) · `Fig. S4` 세로축 'W₋ad' · `Fig. 5b` 단위 'Ω.cm⁻²' · 결론 '2 Ω cm⁻²'.

## (g) Jeff Sakamoto 저자 여부

**예 — 교신저자다** (Neil P. Dasgupta 와 공동 교신 · 끝 저자). INDEX 행 둘째 칸 맨 앞에 `🏷 **Jeff Sakamoto 공저** · ` 를 단다 (위 (a) 에 넣었다). digest 저자 줄에 **Jeff Sakamoto** 로 적었고 웹앱 `_paper_pis` 가 `['sakamoto']` 를 낸다.
