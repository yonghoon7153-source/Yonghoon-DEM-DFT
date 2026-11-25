# 끝 보고 — wang2019_li_se_interface_dynamics_stack_pressure_current_density (2026-11-24 · litdb-curator)

> 이 파일이 있으면 이 편은 끝난 것이다. 공유 파일 (INDEX · comparison · pdf_map) 은 손대지 않았다 — 아래 (a)–(c) 를 메인 세션이 합친다. git 작업 없음.

## 쓴 파일
- `litdb/papers/wang2019_li_se_interface_dynamics_stack_pressure_current_density.md` — digest 438 줄 (§0–§16 · Figure set 표 · 비판 13 항 · 용어 사전 · 먹일 참고문헌 표)
- `litdb/figures/wang2019_li_se_interface_dynamics_stack_pressure_current_density/` — fig_1–8 · fig_S1 · fig_S2 · tab_S1 · figures.json (missing_labels S3–S8 에 not_cropped 사유) · **digitized.csv 129 행** (판독 + Table S1 재계산 · note 열에 축 · 식 · 가정)
- `litdb/figures/_sources.json` — 추출 도구가 다시 씀 (손으로 안 고침)
- 점검: 웹앱 파서로 확인 — 제목 · type · digested 날짜 정상 · elements 태그 Li, La, Zr, Ta, Al, O · methods `—` (사전 목록 해당 없음 — EIS · 정전류뿐) · **PI 배지 `sakamoto` 붙음** · Figure set 주석 11 키 (f1–f8 · fS1 · fS2 · tS1) 전부 잡힘. `build_index.py --check` rc=1 은 '어느 인덱스에도 없는 digest 16 편' (이 편 포함 · 같은 날 묶음) 때문 — 정상. `extract_figures.py --audit` 에서 이 편 ⚠ 없음.

## 핵심 한 문단 (메인이 사용자에게 옮길 것)
Li | Ta-LLZO | Li 대칭셀을 Instron 하중 제어로 3.2 → 0 MPa (0.4 MPa · 5 h 단) 내리며 단방향 박리 → 임계 적층압 **0.4 / 1.2 / 2.0 MPa @ 0.1 / 0.2 / 0.4 mA cm⁻²** (0.05 는 폭주 없음) · Ni 기준전극으로 보면 분극은 **박리 전극만** · 임계압 위에서는 압력 따라 저주파 저항이 가역. 저자 1차 모형 (전류 변형률 jM/(ρFl₀) vs Li 거듭제곱 크리프 m 6.6) 에 대해 우리가 `Table S1` 로 다시 계산하니 ① **`Fig. 8` 의 크리프 점은 아래 축 라벨보다 한 단 위 압력의 값** (근거 넷 · 이웃 점 비 검산은 T 무관) 이라 본문의 '0.1 mA cm⁻² · 0.4 MPa 에서 모형 = 실측' 은 라벨 읽기의 산물이고, ② **모형 교차압은 j^0.15 (0.97–1.33 MPa) 로 거의 평평한데 실측은 ≈ j^1** — 그 식으로는 전류 의존을 못 맞춘다. ⛔ 전부 LLZO 계 (Li 와 화학적으로 안정 — LPSCl 로 옮기지 않는다).
그림: 크롭 11 장 중 그림 10 장 **전부 실독** (Fig. 2 · 6 은 확대 크롭으로 다시) · Table S1 은 PDF 글자. 본문과 어긋난 것: Fig. 8 축 밀림 (위) · Fig. 3A 압력 단 ≈2.5 h (방법 2 h) · Fig. 3B 'ECR 0.1 Hz' (방법 하한 1 Hz) · 표지 넷 vs RC 셋 · Fig. 3C 캡션 R_int vs 축 R_ECR · Fig. 5 그려진 최대 ≈8.2 V (본문 9 V) · Fig. 2 의 0.4 mA cm⁻² 는 3.2 MPa 첫 단부터 상승 (본문 '높은 압력에서 평탄') · Fig. 6 캡션 단위 오기 (mA → mAh) · Fig. 3A DC ≈280 Ω cm² < Fig. 3B 고주파 ≈333 Ω cm² (같은 셀이라면 불가능) · Fig. 4C 두께 4.4 배인데 저항 1.2 배.

---

## (a) `litdb/INDEX.md` 에 넣을 행

**넣을 절**: `## 🧲 계면 점착 · 인터레이어 트랙 — LPSCl 이 한쪽 면인 계면/벌크 역학의 실측 앵커 (2026-09-23 신설)` (표 `| slug | 논문 | 축 |`). `build_index` 는 이 편을 [dft] 트랙 (INDEX.md) 으로 분류한다. 같은 날 Li 금속 계면 묶음 (seymour2021 · lee2022 · kim2026 · masias2019 · shi2026 …) 을 위해 메인이 새 절을 연다면 그 절이 더 맞다.
그 절 머리 상자에 예외 한 줄 (제안): `> ⛔ 예외 (2026-11-24): \`wang2019_li_se_…\` 는 **Li | LLZO** 다 (LPSCl 아님) — 박리 공극 · 임계 적층압의 기전 원전으로만 둔다. 값은 LPSCl 로 옮기지 않는다.`

```
| `papers/wang2019_li_se_interface_dynamics_stack_pressure_current_density.md` **(본문 15 pp + SI 3 pp · 크롭 11장 (그림 10 + 표 1) · 그림 10/10 실독 · 판독·재계산 CSV 129행)** | 🏷 **Jeff Sakamoto 공저** · **[외부·exp·⭐⭐ Li 금속 박리 쪽 공극 · 임계 적층압의 원전 · ⛔ LLZO 계 (LPSCl 아님) · 점착 정량 없음]** ✅ Michael J. Wang · Rishav Choudhury · **Jeff Sakamoto\*** (Univ. Michigan), "**Characterizing the Li-Solid-Electrolyte Interface Dynamics as a Function of Stack Pressure and Current Density**" (***Joule* 3, 2165–2178 (2019)**, DOI `10.1016/j.joule.2019.06.017`). Li\|Ta-LLZO\|Li 대칭셀 · Instron 하중 제어 3.2 → 0 MPa (0.4 MPa · 5 h 단) 단방향 박리: **임계 적층압 0.4 / 1.2 / 2.0 MPa @ 0.1 / 0.2 / 0.4 mA cm⁻²** (0.05 는 폭주 없음 · 'loosely defining' · n = 1 · 발산 한 단 앞 전조) · Al-LLZO 도 같은 단 (`Fig. S1`) · Ni 측면 기준전극 3-전극: 분극은 **박리 전극만** (WE −2.74 → +5.4 V vs Ni · CE −2.82 V 평탄) · 임계압 위 2.4 ↔ 1.2 MPa 에서 저주파 R_ECR ≈5 배 가역 (figure-read) · 0.4 MPa 양방향 (0.35 mAh cm⁻²/반주기) 은 갈고리 +9 mV 에 포화 · 1차 모형 ε̇_j = jM/(ρFl₀) vs ε̇_creep = Aσ^m e^(−Q/RT) (`Table S1`: m 6.6 · Q 37 kJ mol⁻¹ · A 9e-41 = 감쇠 10⁻⁴ 반영) — ⚠ **`Fig. 8` 크리프 점은 아래 축 라벨보다 한 단 위 압력의 값** (우리 재계산 · 본문 '0.4 MPa 일치' 는 라벨 읽기) · **모형 σ⋆ ∝ j^0.15 (0.97–1.33 MPa) vs 실측 ≈ j^1** · 압력과 누적 박리 (17–42 µm) 교락 | 점착 트랙 (인접 · 점착 정량 없음) · 연속체 · DEM 입력 (σ_crit(j) · Li 크리프 — 대조 표적) |
```

talk 역링크: 해당 없음 (`litdb/talks/*` 인입 대기열에 이 논문 없음 — 확인함).

## (b) 비교 문서

**주: `comparison_vs_ours_DEM.md` §I** (계면 점착 · 인터레이어 트랙) 끝에 새 블록 (번호는 같은 날 묶음과 맞춰 메인이 정한다):

```
### I-(다음 번호). `wang2019_li_se_interface_dynamics_stack_pressure_current_density` — (인접 축 · 점착 정량 없음 · ⛔ **Li | LLZO**) 박리 쪽 공극의 **임계 적층압 σ_crit(j)** + Li 크리프 균형식 — **그 식은 실측의 전류 의존을 못 맞춘다**

> **무엇을 주나.** Li | Ta-LLZO | Li 대칭셀을 Instron **하중 제어** 로 3.2 → 0 MPa (0.4 MPa · 5 h 단) 내리며 단방향 박리 (*Joule*, 3, 2165 (2019)). 임계 적층압 **0.4 / 1.2 / 2.0 MPa @ 0.1 / 0.2 / 0.4 mA cm⁻²** (0.05 는 0.4 MPa 까지 폭주 없음 · 'loosely defining' · n = 1) · 발산 한 단 앞에 완만한 전조 (`figure-read`: 0.8 / 1.6 / ≥2.4 MPa 단) · 0.4 mA cm⁻² 는 3.2 MPa 첫 단부터 (E−E₀)/E₀ ≈0.8. Ni 측면 기준전극: 분극은 **박리 전극만** (20 h 까지 WE +0.11 V vs CE −0.003 V · `Fig. S2`). 임계압 위 2.4 ↔ 1.2 MPa: R_ECR ≈45 ↔ ≈255 Ω cm² 가역 (`Fig. 3C` · 외삽 비중 큼). 양방향 0.4 MPa · 0.35 mAh cm⁻²/반주기: 반주기 끝 갈고리 +9 mV 에 포화 (`Fig. 6`).
>
> **★ DEM · 연속체 쪽에 닿는 곳.**
> ① **경계조건이 우리와 같다 (하중 제어)** — I-7 의 정간극 지그와 반대. 이 편의 적층압은 명목값을 그대로 써도 된다 (그림 계단은 명목보다 ≈0.05 MPa 낮다 — 무시 가능).
> ② **1차 크리프 균형식 (ε̇_j = jM/(ρFl₀) vs Aσ^6.6 e^(−Q/RT)) 은 σ_crit(j) 를 재현하지 못한다** — ✎ 우리 재계산 (`Table S1` · 298 K 가정) σ⋆ = 0.97 / 1.08 / 1.20 / 1.33 MPa ∝ j^0.15 vs 실측 ≈ j^(0.8–1.2). 또 `Fig. 8` 의 크리프 점은 아래 축 라벨보다 한 단 위 압력의 값이라, 본문의 '0.1 mA cm⁻² · 0.4 MPa 일치' 는 라벨 읽기의 산물이다. ⇒ 우리 모형이 m 6.6 + 명목 적층압으로 이 표를 못 맞춰도 모형 실패로 읽지 않는다 — 설명해야 할 것은 **겉보기 지수 ≈1** (선형 공급 · 국소 응력 · 누적 손상).
> ③ **A = 9 × 10⁻⁴¹ 은 물성이 아니라 마찰 · 배럴링 감쇠 10⁻⁴ 를 곱한 모형 매개변수** — σ⋆ 가 감쇠 가정에 끌려간다 (0.1 mA cm⁻²: 없음 0.28 → 10⁻³ 0.79 → 10⁻⁴ 1.08 MPa). 크리프 입력은 원전 (`masias2019_li_metal_elastic_plastic_creep_properties` · LePage 2019) 에서.
> ④ **σ_crit 은 j 만이 아니라 반주기 용량 · 누적 박리의 함수** — 단방향은 발산까지 17–42 µm 를 벗겼고, 양방향 1.7 µm/반주기는 임계압의 ⅓ 에서도 포화한다. 압력과 시간 (누적 박리) 이 같이 움직이는 프로토콜이라 둘을 가르지 못한다.
> ⑤ **점착은 두 자리에서 반대 방향** (논문 서술의 우리 정리 · 정량 0): Li | 기판 마찰 · 점착 → 크리프 공급 ↓ (공극 ↑) · Li | SE 접촉 · 점착 회복 → 공극 ↓. W_ad 보고서 7 절의 W(Li | 표면) 는 어느 계면의 값인지 먼저 적는다.
>
> **⛔ 인용 금지 / 한정어**
> · LLZO 값 → LPSCl 이식 금지 (LPSCl 은 Li 와 반응 · SEI). LPSCl 짝은 `shi2026_argyrodite_stack_pressure_viscoplastic_deformation` · Kasemchainan 2019 (카드 없음).
> · σ_crit 은 '0.4 MPa 단 · 정성 판정 · n = 1 · 단방향 5 h 단 · 750 µm Li · 170 °C 열처리 계면' 조건부.
> · `Fig. 8` '0.4 MPa 에서 모형 일치' 인용 금지 · Ȧ/A₀ 를 면적 손실 속도로 인용 금지 (유도식 없음 · 단위 의문) · R_ECR 을 정량 입력으로 쓰지 않는다.
> · frame[4]: 대조 표적이지 보정 표적이 아니다.
> 상세: digest §3b · §3f · §5.11 · §10.
```

**`comparison_vs_ours.md`: 없음** (우리 물성 4 축 값이 없다 · LLZO). 단 `build_index --check` 가 DFT 트랙 digest 의 '미편입' 을 세므로 넣는다면 §E 표에 해석 틀 한 줄만 (선택):

```
| **🆕 (2026-11-24) Li 금속 박리 (방전) 쪽 분극은 계면 *화학* 이 아니라 Li 공급 *역학* — Li 와 안정한 LLZO 에서 3-전극으로 분리 · 압력으로 가역 · 임계 적층압 0.4 / 1.2 / 2.0 MPa @ 0.1 / 0.2 / 0.4 mA cm⁻² (⛔ LLZO · LPSCl 이면 SEI 가 끼어든다)** | **[Wang19SP]** `Fig. 2` · `Fig. 5` · `Fig. S2` · `Fig. 3C` | 우리 §E 는 환원 화학 (산물 · SEI) 축만 — 박리 역학 축 없음 · Li 금속 W_ad 는 보고서 7 절 제안 단계 | ⚪ 축 다름 (수치 비교 아님 · 해석 틀만) |
```
(넣으면 Reference key 에 `[Wang19SP]` = `wang2019_li_se_interface_dynamics_stack_pressure_current_density`.)

## (c) `pdf_map.tsv`
**필요 없음** — `extract_figures.py --inbox --only wang2019_li_se_interface --dry` 가 본문 · SI 를 스스로 짝지었다 ("제목 73%"). 파일은 '자동 매칭이 못 붙인 것만' 적는 곳이다.

## (d) 추가로 먹일 만한 논문 (8 편 · 연도 내림차순 · 전부 litdb 카드 없음 — `litdb/papers` 확인)
2024–2026 후속은 같은 날 묶음 (kim2026 · shi2026 · chatterjee2025 · sandoval2025 · metzler2025 · metzler2026 · cicvaric2026 · lu2026) 이 이미 들어왔다. 그 밖의 2024–2026 편은 서지를 확인할 수 없어서 넣지 않았다 (기억으로 만든 서지는 싣지 않는다). 아래 서지 출처를 칸마다 적었다.

| # | 서지 | 왜 | 서지 확인 | 우선 |
|---|---|---|---|---|
| 1 | Wang, M.J., Kazyak, E., Dasgupta, N.P., Sakamoto, J., "Transitioning solid-state batteries from lab to market: Linking electro-chemo-mechanics with practical considerations", *Joule* 5, 1371 (2021) | 압력 · Li 두께 · 실용 조건 관점 (Sakamoto 계 · 이 논문의 후속 시각) | `kalnaus2023` 참고문헌 [10] | ★ |
| 2 | Lewis, J.A. et al., "Linking void and interphase evolution to electrochemistry in solid-state batteries using operando X-ray tomography", *Nat. Mater.* (2021) | 박리 공극을 **직접 영상** — 이 논문의 빈칸 (§10-⑪) | 제목 · 저널 · 연도: `yadav2021` 참고문헌 (권 · 쪽은 그 표에서 깨짐 → 확인 필요) | ★★ |
| 3 | Kasemchainan, J., Zekoll, S., Jolly, D.S., Ning, Z., Hartley, G.O., Marrow, J., Bruce, P.G., "Critical stripping current leads to dendrite formation on plating in lithium anode solid electrolyte cells", *Nat. Mater.* 18, 1105 (2019) | **LPSCl** 판 — 임계 박리 전류 0.2 (3 MPa) · 1.0 mA cm⁻² (7 MPa) (`deysher2022` 인용값) · 박리 공극 → 다음 석출 덴드라이트 | `tron2023` 참고문헌 표 (저자 · 권 · 쪽) · `banerjee2020` 제목 | ★★★ |
| 4 | LePage, W.S. et al., "Lithium mechanics: roles of strain rate and temperature and implications for lithium metal batteries", *J. Electrochem. Soc.* 166, A89–A97 (2019) | `Table S1` A′ · m · Q 의 원전 — 연속체 크리프 입력 (Masias 는 이미 카드 있음) | 이 논문 ref [27] | ★★ |
| 5 | Krauskopf, T., Hartmann, H., Zeier, W.G., Janek, J., "Toward a fundamental understanding of the lithium metal anode in solid-state batteries — an electrochemo-mechanical study on the garnet-type solid electrolyte Li6.25Al0.25La3Zr2O12", *ACS Appl. Mater. Interfaces* 11, 14463–14477 (2019) | 공공 확산 한계 + 압력 — 실측 σ_crit ∝ ≈j^1 을 설명할 '선형 공급' 후보 | 이 논문 ref [17] | ★★ |
| 6 | Wang, M.J., Wolfenstine, J.B., Sakamoto, J., "Temperature dependent flux balance of the Li/Li7La3Zr2O12 interface", *Electrochim. Acta* 296, 842–847 (2019) | 같은 플럭스 균형의 **온도 축** (같은 저자) | 이 논문 ref [3] | ★★ |
| 7 | Wang, M., Sakamoto, J., "Correlating the interface resistance and surface adhesion of the Li metal-solid electrolyte interface", *J. Power Sources* 377, 7–11 (2018) | **Li | SE 점착 ↔ R_int 실측** — W_ad 보고서 7 절에 바로 닿는다 | 이 논문 ref [10] | ★★★ |
| 8 | Koshikawa, H. et al., "Dynamic changes in charge-transfer resistance at Li metal/Li7La3Zr2O12 interfaces during electrochemical Li dissolution/deposition cycles", *J. Power Sources* 376, 147–151 (2018) | 공극 가설의 원전 (용해 중 R_ct 변화) | 이 논문 ref [16] | ★ |

(연속체 공극 모형의 phase-field · 압력 구동 계면 진화 계열 논문도 후보지만 서지를 확인하지 못해 목록에 넣지 않았다 — 같은 날 `chatterjee2025` 가 이 갈래의 첫 카드다.)

## (e) DEM-DFT 보고서에 쓸 거리 (전부 **Li | LLZO** 값 · LPSCl 이식 금지)

| # | 쓸 곳 | 점 | 쪽 · 그림 · 표 | 그림 직접 봄? |
|---|---|---|---|---|
| 1 | W_ad 7 절 (점착과 공극) | 점착이 **두 자리에서 반대 방향**: Li | 기판 마찰 · 점착 → 배럴링 → 크리프 감쇠 10⁻³–10⁻⁴ → 공급 ↓ → 공극 ↑ / Li | LLZO 접촉 · 점착 회복 (15 min 휴지로 부족) → 공극 ↓. 정량 0 — W(Li | 표면) 를 낼 때 '어느 계면의 W' 인지 먼저 적는 근거 | p.2173 (감쇠 서술) · p.2171–2172 · `Fig. 6` · `Table S1` (A vs A′) | `Fig. 6` 봄 · `Table S1` 은 PDF 글자 |
| 2 | W_ad 7 절 (Li 친화성) | 실측 계면은 **열처리로 젖힌 계면**: 400 °C 3 h Li₂CO₃ 제거 + Li 압착 3.2 MPa 후 ≈170 °C · ≈1 MPa 가열 → 낮은 R_int ('Int' 호가 작다). 젖음각 · 점착은 재지 않았다 | p.2176–2177 · `Fig. 3B` · `Fig. 4C` | 봄 |
| 3 | W_ad 7 절 (Young–Dupré ↔ 공극) | 이 논문 현상의 원자 기준은 `seymour2021_…` (W ≥ 2σ_m 일 때만 공공이 계면에 안 남음) — 연결은 개념뿐 (이 논문은 W 를 안 잰다) | — (다른 카드) | — |
| 4 | 연속체 · DEM 입력 (임계 압력 · 전류) | **σ_crit = 0.4 / 1.2 / 2.0 MPa @ 0.1 / 0.2 / 0.4 mA cm⁻²** · 0.05 는 0.4 MPa 까지 폭주 없음 · 발산 한 단 앞 전조 (0.8 / 1.6 / ≥2.4 MPa 단) · 조건: 750 µm Li (l₀ 700) · 0.4 MPa · 5 h 단 · 단방향 · 누적 박리 17–42 µm · n = 1 → **대조 표적** | p.2167 · `Fig. 2` | 봄 (확대 크롭 포함) |
| 5 | 연속체 입력 (Li 크리프 물성) | `Table S1`: A′ 7e-37 · **A 9e-41 (감쇠 10⁻⁴ 반영 = 모형 매개변수)** · m 6.6 · Q 37 kJ mol⁻¹ · M · ρ · F · l₀ 700 µm · T 미기재. 원전 대조는 `masias2019_…` (n 6.56 · σ_y 0.73–0.81 MPa · 그 카드 값) | SI p.3 `Table S1` · p.2173 | 표 이미지는 안 봄 (PDF 글자) |
| 6 | 연속체 모형 검증 | 1차 균형식 σ⋆ = 0.97 / 1.08 / 1.20 / 1.33 MPa ∝ j^0.15 (✎ 298 K) vs 실측 ≈ j^1 · `Fig. 8` 크리프 점 한 단 밀림 (근거 넷 · digitized.csv) — 우리 모형이 이 표를 m 6.6 으로 못 맞춰도 모형 실패가 아니다 | p.2173–2174 · `Fig. 8` · `Table S1` | 봄 |
| 7 | 연속체 입력 (모형 범위) | 분극은 **박리 전극만** — 20 h 까지 WE +0.11 V vs CE −0.003 V (0.2 mA cm⁻²) → 박리 계면부터 모형화 | p.2169–2170 · `Fig. 5` · `Fig. S2` | 봄 |
| 8 | 연속체 입력 (계면 저항 항) | 공극 없는 영역에서도 압력 의존: R_ECR ≈45 ↔ ≈255 Ω cm² (2.4 ↔ 1.2 MPa · 0.1 mA cm⁻² · 가역 · 바퀴마다 감소) · DC 진폭 +27 → +11 % — 정량은 약함 (ECR 호 일부만 측정 · 외삽) | p.2168–2169 · `Fig. 3A–C` | 봄 |
| 9 | 연속체 입력 (운전 조건) | σ_crit 은 반주기 용량의 함수: 0.4 MPa (0.2 mA cm⁻² 의 σ_crit ⅓) · 0.35 mAh cm⁻²/반주기 → 갈고리 +9 mV 에 포화 → (반주기 용량 × 적층압) 2 차원으로 물어야 한다 | p.2171–2172 · `Fig. 6` | 봄 |
| 10 | DEM 경계조건 | **하중 제어** (Instron 5944 · 1 mm min⁻¹ 전환) — 우리 DEM 압밀 · 박리와 같은 종류 · 명목 적층압 그대로 사용 가능 | p.2177 · `Fig. 1` | 봄 |

## (f) 그림 크롭 요약
- 11 장 (본문 `Fig. 1`–`Fig. 8` + SI `Fig. S1` · `Fig. S2` + `Table S1`) · **놓친 그림 0** · 손 크롭 0.
- 도구의 '번호 공백' S3–S8 은 **오탐** — SI 글의 'in Figure 5' (Fig. S2 캡션) · 'in Figure 8' (Table S1 제목) 을 S5 · S8 로 읽었다. figures.json missing_labels 6 항목에 not_cropped 사유를 달았다.
- 실독: 그림 **10/10** (Fig. 2 · 6 은 확대 크롭으로 한 번 더) · Table S1 은 PDF 글자 · 그래픽 초록 (PDF p.1) 은 크롭 없음 (쪽 렌더로 봄). `--audit` ⚠ 없음.
- scratchpad 대조: 내 임시 글자 파일은 공용 이름이 아니라 `scratchpad/wang2019/` 하위 폴더였고, 지금 slug 폴더 (`scratchpad/wang2019_li_se_interface_dynamics_stack_pressure_current_density/`) 에 새로 뽑은 판과 **바이트 동일** (SHA-256 같음 · 제목 · 저자 · "Joule 3, 2165–2178" 확인) — 다른 논문 글자 섞임 없음. 인용한 문장의 쪽도 그 판에서 다시 대조했다. 수치는 PDF 쪽 렌더로도 봤다.

## (g) Jeff Sakamoto 저자 여부
**예** — 교신 저자 (`*`) 이자 Lead Contact (셋째 저자 · jeffsaka@umich.edu). digest 저자 줄에 **Jeff Sakamoto** 로 적었고 웹앱 PI 배지 `sakamoto` 가 붙는 것을 파서로 확인했다. INDEX 행 둘째 칸 맨 앞에 `🏷 **Jeff Sakamoto 공저** · ` 를 넣어 두었다 (위 (a)).
