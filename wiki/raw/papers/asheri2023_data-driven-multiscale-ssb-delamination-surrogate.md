---
title: "Asheri, Fathidoost, Glavas, Rezaei, Xu 2023 — Data-driven multiscale simulation of solid-state batteries via machine learning (Comput. Mater. Sci. 226, 112186)"
source_url: local-upload/20._Data-driven_multiscale_simulation_of_solid-state_batteries_via_machine_learning.pdf + code https://github.com/mFathidoost/battery @ 4683a6f22820be933b11c8f54dcef2fdefba1c1c
source_url_note: "본문 15 쪽(그림 11 · 표 5 · 식 49 · 참고문헌 73), SI 없음. 순수 계산 편 — 실험 0. 코드 저장소는 읽기 전용 클론으로 실행 없이 조회(.sav 미로드 · 노트북 JSON 텍스트 · 데이터 파싱만), 라이선스 미표기라 파일을 복사 · 커밋하지 않는다(파일별 sha256 은 본문 표). 크로퍼 자동 16(그림 11 · 표 5) — Read 6 장(Fig. 5 · 7 · 8 · 9 · 10 · 11) + Fig. 9–11 원본 래스터 픽셀 판독 + 식 (26)(32)(45) 렌더; 안 본 것은 §12. 원자료는 커밋하지 않는다."
source_doi: 10.1016/j.commatsci.2023.112186
source_license: "© 2023 Elsevier B.V. All rights reserved — 오픈액세스 아님; 코드 저장소 라이선스 미표기"
pdf_sha256: 4fb0b00c73fb90152d01c8d3ac11e364eefc52bc25833e39ac3fccf8f27a57a4
code_repo: https://github.com/mFathidoost/battery
code_commit: 4683a6f22820be933b11c8f54dcef2fdefba1c1c
ingested: 2026-09-23
sha256: ba51f555f5d3bfefccdb9f18f259f807cd8a32e5d408e9ff1d8c6b2422350b0e
---
# 수집 목적

`assb` 섹션 **58호**. 큐 **59번** — 2차 묶음(큐 40~59, 원장 §1 상단 순서)의 **스무째 · 마지막 편** (`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-g).
닻은 `questions/assb-contact-loss-vs-lampe.md`. 원장(`bms-balancing/docs/ASSB_WANTED_PAPERS.md`) 행: 15호 Rahman 2024 가 "**유일한 SSB-ML 인용**('interface damage')" 으로 지목(15호 ref [22]) · 원장 정정 "측정 아님, **시뮬 대리모형**".

이 digest 의 1순위 물음: **(1) 계면 박리 변수는 거시 식의 어느 자리로 들어가는가** — 37호 틀(`ε_p` = `LAM_PE` 동어반복 ↔ `A_eff·k` 곱) · 56호 틀(`φ` 자리) **(2) `θ(N)` 을 내는가** — 사이클 축 · 시간 축 **(3) 대리모형은 원 모델의 식별성을 물려받는가** — 학습 데이터가 원 모델 출력이면 식별성은 원 모델 것(28호 '역범죄' 선례) · 학습/검증 분할 · 불확실성(36호 기준) **(4) 사용자가 준 코드 저장소로 논문 주장(정확도 · 효율)을 실행 없이 어디까지 확인할 수 있는가.**

A. Asheri*(a,b), M. Fathidoost(b), V. Glavas(a), S. Rezaei**(b), B.-X. Xu**(b) —
**"Data-driven multiscale simulation of solid-state batteries via machine learning"**,
*Computational Materials Science* **226** (2023) 112186, doi `10.1016/j.commatsci.2023.112186`.
`[인쇄]` Received 17 October 2022 · revised 17 February 2023 · Accepted 5 April 2023 · Available online 24 April 2023 · "© 2023 Elsevier B.V. All rights reserved." — 오픈액세스 아님. Full length article.
소속: (a) **Volkswagen Group, Wolfsburg**(Asheri · Glavas) · (b) **TU Darmstadt, Mechanics of Functional Materials**(Fathidoost · Rezaei · Xu). 교신 셋(* Asheri, ** Rezaei · Xu). `[인쇄]` Disclaimer: "The results, opinions and conclusions … are not necessarily those of Volkswagen Aktiengesellschaft." 계산 자원 Lichtenberg(Hessen).
**계보 겹침**: Glavas 는 **56호**(Bielefeld · Weber · Rueß · **Glavas** · Janek 2022)의 공저자 — VW Wolfsburg 고리(56 · 57호 Weber 도 VW). 이 편의 유일한 실험 이미지 Fig. 1b 는 **23호 Koerver 2017**(ref [4], "reprinted with permission")이다. 56 · 57호 · 01호 인용 0.

본문 PDF **15 쪽**(그림 11 · 표 5 · 식 49 · 참고문헌 73). SI 없음. PDF sha256 은 frontmatter `pdf_sha256`.

**코드 · 데이터 저장소** (사용자 제공 · 읽기 전용 클론 · **아무것도 실행하지 않았고 `.sav` 는 로드하지 않았다** — 파일 크기 · 헤더 바이트 · 피클 안 ASCII 문자열만 봤다; `.ipynb` 는 JSON 텍스트로 셀 소스 · 저장된 출력만; `.txt` 는 pandas 로 파싱):
`https://github.com/mFathidoost/battery` · 커밋 `4683a6f22820be933b11c8f54dcef2fdefba1c1c`(mFathidoost, 2022-11-07, "Add files via upload" — 단일 커밋) · **LICENSE 파일 없음 · README 에 라이선스 문구 없음 ⇒ 라이선스 미표기** — 저장소 파일을 이 저장소에 복사 · 커밋하지 않는다.

| 파일 | 바이트 | sha256 | 정체(실행 없이 확인한 것) |
|---|---:|---|---|
| `README.md` | 603 | `bad8da1b9ba9c9838c8f69ec3da938e00da6bd33a28b696bc0bb26a3c178c1e4` | 세 J 범위 · "J\*=2609.6J" · 겹침 설명 |
| `final_data.txt` | 2,337,950 | `e1534f8ce3dcebfb7e637536d3bc66b2ed996fd6f95dae2528df656665d7f23f` | 탭 구분 7 열 × **12,304 행**(손상 학습 자료) |
| `benchmark_wo_damage.txt` | 269,479 | `9231fd4db064a5472a3622961b9ac663e427813984ac0f377d40d70db6aa7001` | 5 열 × **6,286 행**(벤치마크, 손상 없음) |
| `smallJ.ipynb` | 259,816 | `91c11f0977da429e7b7dc7e1fb179a8b0996c1a8fd367dd23be98b3babafaf8c` | Keras 학습 · 평가 · 가중치 내보내기 |
| `mediumJ.ipynb` | 277,022 | `e6edc5dd5ab37d82e0b2d9dc27353491de985b743fe89016df61f8f104a392f3` | 〃 |
| `bigJ.ipynb` | 139,892 | `a21d7b99121bdb8773fbfea4ab91cecd933ef5f66fce253c7a88aa5e30fa5284` | 저장 모델 로드 · 평가(학습 셀은 주석) |
| `benchmark_wo_damage.ipynb` | 101,477 | `7226be2fdfbbc0507161d1589fad36cbf6a1f164f08f32e6dfaa31af8750effa` | sklearn MLP 로드 · 평가(학습 셀은 주석) |
| `smallJ.sav` | 301,078 | `a626cdbf311f10c90310f2159557f7c4c9f8f09a37d68dea07055491012653b0` | 피클 머리 `keras.engine.sequential` · Keras 2.3.1 · Dense **3072** relu → Dense 3 relu · 입력 4 |
| `MediumJ.sav` | 202,696 | `8547de69e0bf663255709fb80dcb75e62a44b25926ad542877ede1f8eb280412` | 〃 Dense **2048** |
| `bigJ.sav` | 18,366 | `9f71aa42dce0970b1271419ad1fef5860d4b678eadfb04b0bab42fdd4e08ad21` | 〃 Dense **128** |
| `benchmark_wo_damage.sav` | 275,172 | `e01f20fcfb2d10dc1ad2cd51749f7978e6fd26f4f5b4987b0a1d1bac1c7a41fd` | 피클 머리 `sklearn.neural_network._multilayer_perceptron.MLPRegressor` · `_sklearn_version` 0.24.0 · 문자열 `out_activation_` 뒤 **`identity`** · `activation` relu · `solver` adam |

없는 것: MOOSE 미세 FE 입력 · 거시(2단) MOOSE 입력 · C++ 신경망 서브루틴 · 셀 수준 결과(Fig. 5 · 9–11)의 자료 — **셀 수준 주장은 저장소로 재현할 수 없다.** 노트북은 저장소에 없는 파일을 읽고 쓴다(`ann_data_ec.txt` · `MLP_160321_MaxMinScale_log_soc_ec_v4.sav` · `model_128_1000_101021.sav` · `1024_500_smallJ-10nov.sav` · `MediumJ-10nov.sav`) — 저장소의 `.sav`/`.txt` 가 그 파일들과 같은 것인지는 이름 · 구조로만 대응시켰다(해시 대조 불가).

> ⚠ **표기**: `[인쇄]` = 지면에 문자 그대로 있는 것 · `[도표]` = 그림을 열어 읽은 값(figure-read ≈) ·
> `[코드]` = 저장소 파일(노트북 저장 출력 · 피클 헤더 문자열 · 데이터 파싱)에서 읽은 것 ·
> `[재현]` = 지면 · 저장소 수치로 이 위키가 다시 계산한 것 · `[해석]`/`[추론]` = 이 위키의 해석. 표시가 없는 서술은 원문이 실제로 말한 것이다.
> ⚠ **이 편은 순수 계산 편이다.** 실험 0 · 측정 0. "박리가 용량을 X % 깎는다" 류는 전부 **모델 명제**이고, 대리모형의 "정확도" 는 **원 모델 대비 충실도**다.

---

# 판정 (먼저)

> ★★★★ **박리의 자리 — 글은 "활성 계면 면적" 이라 말하고, 식의 결합은 `ε_p`(`LAM_PE`) 자리다.** `[인쇄]` 식 (32) `a = (S/V)(1 − ε_e)(1 − ⟨d⟩)` · (33) `⟨d⟩ = ∫_s d dA / ∫_s dA` · (31) `J_eff = a·J_s` · "the loss of contact between the active material and the solid electrolyte is considered to be the same as ⟨d⟩. In the limit case when ⟨d⟩ = 1, the whole interface is damaged and the active particle becomes isolated." 그런데 미세 문제의 경계조건은 **손상과 무관하게 입자 표면 전체로** `J_s` 를 넣는다 — `[인쇄]` "a uniform ion flux is considered at the surface of the particles" · "The microscopic pore wall flux is applied as a constant flux to the active particle", 그리고 `[코드]` 학습 자료 12,304 행 **전부**에서 `soc_dot / (2|j|)` = **0.9987–1.0013**(원판 입자, 둘레/넓이 = 2/R) — 손상 `⟨d⟩` 가 0.45 까지 자란 행을 포함해서다. `[해석]` ⇒ 거시에서 `a` 를 `(1 − ⟨d⟩)` 만큼 줄이면 같은 전류를 대는 `J_s` 가 `1/(1 − ⟨d⟩)` 배가 되고, 대표 입자는 그만큼 빨리 찬다 — **`ε_s → ε_s(1 − ⟨d⟩)` 와 같은 결합**, 즉 "입자 분율 `⟨d⟩` 가 통째로 빠지고 나머지는 온전히 붙어 있다" 이다. 37호 틀의 **`ε_p` 동어반복 쪽**이지 `A_eff ↔ k`(표면 피복, 용량 불변) 쪽이 아니다. 56호의 `φ`(표면 피복률) 자리와도 다르다 — 56호는 피복이 입자 **안** 확산 경계를 바꾸고, 이 편은 미세 경계를 안 바꾼다.
> `[재현]` 방증: 저율 극한에서 이 결합이 주는 용량 손실은 `∫⟨d⟩ d(SOC) / 0.5` 다. 학습 자료(`|j|` ≤ 0.01 궤적)로 적분하면 `G_c` 4.21 → **8.8–8.9 %** · 5.97 → **3.9–4.0 %** · 13.92 → **0.3 %**. 지면 1 C 셀(Fig. 9 · 11)의 끝 시각 `[도표]` 무손상 ≈3560 s ↔ 4.21 ≈3250 s(**−8.7 %**) · 5.97 ≈3450 s(**−3.1 %**). 4.21 은 거의 겹치고 5.97 은 방향 · 크기가 같다(셀은 SOC 1 전에 끊겨 적분 상한이 짧다). 순수 동역학(`A_eff·k`) 자리였다면 1 µm 입자 · 1 C 에서 이 크기가 나오기 어렵다(`[추론]`).
>
> ★★★★ **`θ(N)` — 0. 구조적으로 못 낸다.** 셀 계산은 **한 번의 정전류 방전**(0.5 → 1 `c_max`, 1 · 2 · 5 C)뿐이다. 그리고 (i) 출력층 ReLU 가 `ċ_surface`, `ċ_bulk` ≥ 0 을 강제해 **충전(탈리튬)을 표현할 수 없다** (ii) 대리모형 입력 `(G_c, J_s, c̄_surface, c̄_bulk)` 에 **손상 상태 `⟨d⟩` 도 경화 변수 `ξ` 도 없다** — KKT 이력 변수를 기억 없는 사상으로 대신했다(저자 스스로 "Recurrent Neural Network, to account for the history effects" 를 향후 과제로 인쇄). ⇒ 두 번째 사이클을 돌리면 손상을 처음부터 다시 쌓는다(`[추론]`). 카드 `θ(N)` **0/58**. 얻은 것은 **한 방전 안의 `⟨d⟩(t)`** 이고, `[재현]` 그것은 사실상 **`⟨d⟩(SOC; G_c)`** 다(아래 판정 3).
>
> ★★★★ **대리모형은 원 모델의 식별성을 물려받고, 검증도 원 모델 안에서 닫힌다.** 학습 · 시험 자료는 전부 같은 MOOSE 화학-기계 모델의 출력이고, `[코드]` 분할은 `train_test_split(test_size=0.25, random_state=40)` **행 무작위** — 시험 행은 학습 행과 **같은 90 궤적**(`G_c` 3 × `j` 30)의 이웃 시간 단계다 ⇒ 표 4 · 5 의 R² 0.99 는 **궤적 안 보간 충실도**다. "unseen" 검증(Fig. 8)은 `G_c` 5 · 10 J m⁻² 두 점(학습 범위 4.21–13.92 **안**)이고 두 점의 `j`(0.1 · 0.07)는 **학습 격자 값**이다. 셀 수준 손상 계산(Fig. 9–11)은 `[인쇄]` "the chemo-mechanical case was not simulated using the FE² method (due to very high computational costs)" — **기준해가 없다.** 불확실성 · 앙상블 · 신뢰구간 · 보정(36호 기준) **0**. 실험 대조 **0**. 28호 부류로 말하면: 이 편에는 역문제가 없으므로 '역범죄' 는 성립하지 않지만, **"정확도" 가 곧 "원 모델과의 일치"** 이고 원 모델 자체의 검증은 지면 어디에도 없다.
>
> ★★★ **코드 · 데이터로 확인한 것 / 어긋난 것** (§11). ✅ 표 4 R² 0.9979 · MSE 0.0001 ↔ 벤치마크 노트북 시험 0.99796 · 1.06×10⁻⁴ · 은닉 704(=11·64) · 학습 자료 12,304 행 · `G_c` {4.21, 5.97, 13.92} · 은닉 128/2048/3072 · 입력 4 · 출력 ReLU(손상 모델). ❌ **표 5 의 R²₁ 0.99184 는 bigJ 노트북의 *학습* R²**(시험은 0.99199)이고, 세 손상 노트북 모두 `r2_score(y_pred, y_true)` 로 **인자 순서가 뒤집혀** 있다 · R²₂ 0.99556 · R²₃ 0.99316 · MSE₂,₃ 6×10⁻⁵ 는 노트북 출력에 없다(중간 시험 0.99415 · 1.21×10⁻⁵, 작은 j 쪽 0.99950 · 8.0×10⁻⁶) · 벤치마크 모델은 Keras 가 아니라 **sklearn MLPRegressor**이고 출력 활성은 **`identity`**(지면: ReLU) · 식 (41) L2 항은 세 Keras 모델에 **없다**(`kernel_regularizer: null`) · **플럭스 값의 단위가 두 척도로 섞였다**(D1 — 지면 `J_s` = 783 · 261 · 183 mol m⁻² s⁻¹ 는 자료 `j` × 2609.6 인데, Fig. 8 의 채움 시간 ≈245 s 는 `j` ÷ 2609.6 이어야 나온다 — 차이 2609.6² ≈ 6.8 × 10⁶).
>
> ★★★ **15호의 '유일한 SSB-ML' 인용과의 대조** — 15호 문장(`[인쇄]` "introduced a data-driven multiscale simulation framework (leveraging artificial neural networks) to predict and analyze the degradation in solid-state batteries, focusing on interface damage") 은 이 편 초록과 **어휘상 맞다.** 그러나 이 편의 "degradation" 은 **한 방전 안의 계면 손상과 그 방전 용량**이고 수명 · 사이클 · SOH · RUL 은 0 이다; ML 은 **FE 미세 문제의 대리(surrogate)** 이지 상태 추정기가 아니다. 15호 digest 의 판정("이 편이 아는 유일한 SSB-ML 라벨은 `simulated`")은 그대로 맞고, 한 줄을 더한다: **SBMS(15호 주제)에 옮길 수 있는 추정 · 예측 기능은 이 편에 없다.**

---

# 0. 원문에 없어서 확인이 필요한 것

- **미세 경계조건이 손상 부위에서 어떻게 되는가** — 지면은 "uniform ion flux" 만 말한다. `[코드]` 자료는 입자 총 유입이 `d` 와 무관함을 보인다(판정 1). 손상 부위를 막고 온전한 부위에 몰아준 것인지, 전 둘레 균일인지는 MOOSE 입력이 없어 모른다 — **어느 쪽이든 입자 채움 속도는 `d` 와 무관**하므로 판정은 안 바뀐다.
- **정규화 규약** — README "J\*=2609.6J" 외에 `j` · 시간 · 농도 무차원화 식이 지면 · 저장소 어디에도 없다. `[재현]` `1/2609.6 = 3.832×10⁻⁴ = c_max × 10⁻⁸` — `c_max·D/R` 이면 `R` = 1 µm 에서 `D` = **1.0 × 10⁻¹⁴** m² s⁻¹(표 2 `D₁` = 7 × 10⁻¹⁵). Fig. 8 에서 읽은 시간 단위(무차원 1 ≈ 98–100 s ≈ `R²/D`)도 같은 `D` 를 가리킨다. 표 2 값이 실제 미세 계산 값인지 확인 불가.
- **셀 계산의 국소 `j` 분포** — 셀 두께 방향 `J_s` 가 학습 범위(`|j|` 10⁻⁴–0.3) 안에 있었는지 지면은 말하지 않는다. `[재현]` Fig. 8 시간 척도로 환산하면 1 C 채움(≈3450 s)은 `|j|` ≈0.007(`−log₁₀` ≈2.1, 중간 망) · 2 C ≈0.014(작은/중간 겹침) · 5 C ≈0.036(작은-`−log` 망) — **세 C-율이 서로 다른 신경망에 걸린다**(평균 기준, 국소 분포 미상).
- **겹침 구간(`−log₁₀|j|` 1.6–2 · 2.5–3.02)에서 어느 망을 쓰는가** — README 는 "to get better prediction for the cases near the borders" 만, 지면은 겹침 자체를 말하지 않는다. 전환 규칙 0.
- **unseen `G_c` 5 · 10 J m⁻² 의 `Y₀` · `H`** — 표 2 는 세 쌍(4.21 · 5.97 · 13.92 대응)만 인쇄. Fig. 8 의 FE 기준해가 어떤 `Y₀` · `H` 로 돌았는지 미상.
- **`S/V`, 활물질 분율** — 식 (32) 의 `(1 − ε_e)` = 0.7 은 도전상(`ε_c` 0.3)을 포함한 값으로 읽힌다(`[해석]`). 1 C = 11.7 A m⁻² 가 주는 용량과는 활물질 ≈0.38–0.4 가 맞는다(`[재현]` 0.4 × 60 µm × 0.5 × 38320 × F ≈ 12.3 Ah m⁻²). 어느 분율로 `a` 를 셌는지 미상.
- **식 (26) 의 형태** — 인쇄된 BV 는 `η = 0` 에서 `J_s = (i₀/F)(2c̄ − 1)` ≠ 0 (`c̄` ≠ 0.5). 오식인지 구현인지는 MOOSE 코드가 없어 모른다(D8).

---

# 1. 서지 · 낱말 지문

**★ 단어 지문** (규칙: NFKC 뒤 · 대소문자 구분 · 낱말 경계 · 본문(참고문헌 전)):

| `identifiab` | `uncertaint` | `conf.interval` | `Bayes` | `posterior` | `calibrat` | `LLI` | `LAM` | `degradation mode` | `contact loss` | `MPa` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **0** | **0** | **0** | 0 | 0 | **2** | 0 | **0** | 0 | **3** | **0** |

NFKC 변경 본문 **900 자** — 전부 수학 이탤릭(U+1D4xx: `𝑐` 135 · `𝑖` 109 · `𝑠` 50 · `𝑑` 48 · `𝐽` 47 …) — **열 변화 0**. 소프트 하이픈 0 · 줄끝 하이픈 **70 곳**(이으면 `fracture energ*` 20 → 21 · `cycl*` 1 → 2 · `capacity` 7 → 8 · `experiment*` 6 → 7 — 11 열 변화 0).
- `calibrat` 2 = 남의 편 서술 1(Nascimento "can be calibrated") + "**In order to calibrate and test the surrogate model**" 1 — **학습의 뜻**이지 불확실성 보정이 아니다.
- `contact loss` 3 = 셋 다 **결론 문장**("the consequent contact loss and capacity fade" · "the contact loss … occurs faster" · "delamination and contact loss") — 박리 = 접촉 손실을 등치하는 어휘. 정량 0.
- 보조: `delamina*` 22 · `damage` 56 · `surrogate` 34 · `train*` 19 · `test*` 12 · `unseen` 4 · `ReLU` 9 · `validat*` 1(남의 편) · `histor*` 1(향후 과제) · `extrapol*` 0 · `interpol*` 0 · `overfit*` 1(L2 항 설명) · `error` 1 · `noise` 0 · `cycl*` 2(서론 "cycles of charge and discharge" · "cyclic loading") — **사이클을 계산한 곳 0** · `pressure` 1(Christensen P2D 서술) · `experiment*` 7(전부 남의 편 · OCP 출처) · `isolat*` 2 · `threshold` 0.

---

# 2. 방법 (§2)

## 2.1 두 단계 모델 (식 (1)–(33), 표 1)

- **거시(셀, 1D)**: Li 금속 음극 · 분리막 `L_s` 40 µm · 복합양극 `L_c` 60 µm. `[인쇄]` "only a half cell configuration is considered". 전해질 단일 이온 전도(`t₊⁰` ≈ 1, LLZO 근거) ⇒ `ċ₂ = 0`(식 (5)) · 옴 법칙 `i₂ = −κ_eff∇φ₂`(식 (8)) · `i₁ = −σ_eff∇φ₁` · Bruggeman `ε^(1+α)`(α 값 미인쇄) · 전하 보존 (12)(13).
- **미세(입자)**: 벤치마크는 구 1D 방사 Fick(식 (43)–(46)); 손상 계산은 **2D 원판 AM + SE 매트릭스**(Fig. 6 — 안 봄; `[인쇄]` "we first examine a circular active material particle in a matrix of solid electrolyte. An extension to spherical particles is straightforward"). 화학-기계 결합: 이방 고유변형 `Ω = diag(2, 2, −1)·Ω/3`(식 (16), NMC, Xu 2018) · 확산에 응력 구배 항(식 (19)) · 계면 **결합 영역 모델**(식 (20)–(25), 모드 무관 손상 `d`, 퇴화 함수 `(1−d)ⁿ`, 경화 `ξ`, KKT) — Rezaei, Asheri, Xu 2021 *JMPS* [11]. 경계: 왼쪽 `u_x` = 0 · 위아래 주기 · 오른쪽 **스프링** `F = −K_spring u_x`(`K_spring` 8.15 × 10⁴ N m⁻¹) — **적층 압력 없음**.
- **척도 잇기**: BV (26)–(29), `c̄_surface` 는 표면 평균 · `J_eff = a·J_s`(31) · **`a = (S/V)(1 − ε_e)(1 − ⟨d⟩)`**(32, Bai 2019 [31] 인용).
- **파라미터**(표 2 · 3, 문헌 인용): `E₁` 140 GPa · `ν₁` 0.3 · `Ω` 4.566 × 10⁻⁶ m³ mol⁻¹ · `D₁` 7 × 10⁻¹⁵ m² s⁻¹ · `c₁,max` 38320 · `Y₀` 0.977/1.47/2.86 · `H` 5.294/7.33/18.165 Pa m · `k₀` 3.26 × 10¹⁶ Pa m⁻¹ · T 298.15 K; `E₂` 150 GPa · `κ` 2.44 × 10⁻² S m⁻¹ · `σ` 10 S m⁻¹ · `k₂` 10⁻¹⁰ · `ε_e` 0.3 · `ε_c` 0.3. OCP 식 (30) = Danner 2016 [63] 의 **액체셀 NMC 적합식**(조성 x/y/z 미지정). 농도 창 0.5–1 `c_max`, 초기 0.5.

## 2.2 대리모형 (§2.2, 식 (34)–(42))

- 흐름(Fig. 2 — 안 봄, 텍스트): 거시가 `J_s` 를 내면 대리모형이 `(ċ_surface, ċ_bulk, ḋ)` 를 내고 명시적 오일러(34)–(36)로 갱신. **순차(sequential) 결합** — FE² 의 동시 풀이 대신.
- 자료 생성: `[인쇄]` "A range of values for J_s … is obtained by running a FE² simulation … Next, using several J_s values from this range, individual microscale simulations are performed (for each simulation a constant J_s is used)." — **각 미세 계산은 일정 `J_s`**, 셀 안의 `J_s(t)` 는 시간에 따라 변한다 ⇒ 학습 분포(일정 플럭스 궤적)와 사용 분포(변동 플럭스)가 다르다(`[해석]`; 이력 없는 입력이라 모델은 이 차이를 모른다).
- FFNN, 입력 min–max(`J_s` 는 `log₁₀` 뒤), 은닉 ReLU, **출력 ReLU**(`[인쇄]` "to ensure fulfillment of the physics (i.e. to have always non-negative values for damage growth)") · 손실 = MSE + L2(식 (41)) · 평가 MSE · R²(식 (42), 출력 평균).
- 구현: MOOSE 로 미세 자료 → Python 3.8.8 · Keras · scikit-learn(전처리) → 가중치를 텍스트로 내보내 MOOSE C++ 서브루틴에서 적분점마다 평가.

---

# 3. 결과 — 벤치마크 (§3.1, 손상 없음 · 역학 없음)

- 구 1D Fick 미세 문제 · R_s 1 µm · 1 C = 11.7 A m⁻². FE² 시간 단계 수렴(Fig. 4b — 안 봄) → `dt` = 5 × 10⁻⁵ 채택(단위 미인쇄).
- `[인쇄]` "J_s ∈ [2.8 × 10⁻⁷, 2.6 × 10³] mol/(m² s)" · "J_s = m×10ⁿ with m∈[1, 9] and n = −7, −6, …, 3" · "around 6000 data sets" · 은닉 1 층 **704** 노드 · 표 4 R² **0.9979** · MSE **0.0001**.
- **Fig. 5 (봤다)** `[도표]` 전압: ANN-assisted 와 FE² 가 3.6 V 무릎 직전까지 겹치고, 끝 ≈3520 s(ANN) ↔ ≈3540 s(FE²) — 무릎 모양이 조금 다르다(FE² 가 먼저 휜다). 표면 농도 0.5 → ≈0.98 거의 겹침.
- 효율: `[인쇄]` "It takes **4 days** to run this problem using FE² method on a computer with 48 cores … while it takes only **20 min** to run it using the data-driven method on the same machine." `[재현]` ×288. ⚠ **이 비교는 이 벤치마크 한 건뿐**이고, 오프라인 자료 생성 비용(MOOSE 미세 계산 90 궤적 + 학습)은 포함되지 않았다.
- `[코드]` 벤치마크 노트북: 읽는 파일 `ann_data_ec.txt` **6,285 행**(저장소 `benchmark_wo_damage.txt` 6,286 행과 머리가 같다) · `j` **46 값, −1 … −10⁻⁵**(5 자릿수) · 필터 `0.0458 < −log₁₀|j| < 3.1` 로 **29 값 · 4,017 행**만 사용 · 학습 3,012 / 시험 25 % · 목표 `c_dot` 에 `−log₁₀` 변환(지면에 없음) · 저장 모델 로드(학습 셀 주석) → **시험 R² 0.99796 · MSE 1.06 × 10⁻⁴** — 표 4 와 일치 ✅. `soc_dot/(3|j|)` 0.979–1.016(구, 3/R) ✓.

---

# 4. 결과 — 화학-기계 + 손상 (§3.2)

## 4.1 미세 계산 (Fig. 7 — 봤다)

- `G_c` ∈ {4.21, 5.97, 13.92} J m⁻² · `[인쇄]` "J_s ∈ [2.8 × 10⁻⁷, 8.3 × 10²] mol/(m² s)" · "around 12304 data sets" ✅(`[코드]` 정확히 12,304).
- **Fig. 7** (`G_c` 5.97 · `J_s` 783): `[도표]` (a)(b) 시작 — 농도 0.5 균일, `d` 색띠 최대 1.2 × 10⁻³⁸(수치 0). (c)(d) 중간 — 입자 농도 0.66–0.76, 이방 확산 전선(z 방향 수축 · x 방향 팽창), 위아래 계면에 **가는 흰 틈**이 보이나 `d` 는 여전히 ≈0. (e)(f) 끝 — 표면 1.0 · 중심 ≈0.85, **위아래 "normal opening"**(흰 틈)과 **어깨의 "severe sliding"** 호에 국소 `d` 최대 **0.37**. ⇒ `[해석]` 틈(열림)과 손상 변수가 같은 곳에 있지 않다 — 위아래 정점은 흰 틈인데 색은 어깨에 있다. `⟨d⟩` 는 **어깨 미끄럼 손상의 면적 평균**이고 "열린 틈 면적" 이 아니다.
- `[코드]` 자료 구조: 90 궤적(3 `G_c` × 30 `j`), `j` = −0.3 … −10⁻⁴(무차원, 3.5 자릿수), 궤적당 100–181 행, 모든 궤적 시작 `c` = `soc` = 0.5. **표면이 1 에 닿으면 끝** — `j` −0.3 은 `soc` 0.94–0.95 에서, `|j|` ≤ 0.002 는 ≈1.000 에서.
- `[재현]` **손상은 사실상 리튬화 상태의 함수다** — `ḋ` 를 궤적별로 적분(`Δt = Δsoc/soc_dot`)하면:

| `G_c` [J m⁻²] | 개시 SOC (`⟨d⟩` > 10⁻³) | `⟨d⟩` @ SOC 0.9 | 끝 `⟨d⟩` (SOC ≈1) | 저율 용량 손실 `∫⟨d⟩dSOC/0.5` |
|---|---|---|---|---|
| 4.21 | 0.727–0.731 (`j` −0.3: 0.712) | 0.203–0.205 (−0.3: 0.238) | 0.44–0.45 | 8.8–8.9 % |
| 5.97 | 0.777–0.782 (−0.3: 0.762) | 0.089–0.090 (−0.3: 0.111) | 0.23–0.24 | 3.9–4.0 % |
| 13.92 | 0.892–0.893 (−0.3: 0.874) | 0.0023 (−0.3: 0.0067) | 0.034 | 0.3 % |

  `|j|` ≤ 0.03 에서 `⟨d⟩(SOC)` 곡선이 **≈1 % 안에서 겹친다**; 가장 큰 `|j|`(0.3 · 0.1)에서만 개시가 조금 이르고 값이 10–16 % 크다. ⇒ 대리모형의 세 출력 중 `ċ_bulk` 는 입력 `j` 의 닫힌 식(질량 보존, `soc_dot = 2|j|`)이고, `ḋ` 는 대부분 `f′(SOC; G_c)·2|j|` 다(`[해석]`).

## 4.2 대리모형 (§3.2.2, 표 5)

- `[인쇄]` 자료를 `J_s` 로 **세 부분집합** → 망 셋(은닉 1 층, **128 · 2048 · 3072** 노드) · 출력 ReLU · 표 5 R² 0.99184 / 0.99556 / 0.99316 · MSE 0.00001 / 0.00006 / 0.00006.
- `[코드]` README 세 범위(`−log₁₀|j|` < 2 · 1.6–3.02 · > 2.5) = 노트북 필터 · 부분집합 행 수 **4,465 / 4,489 / 4,847**(겹침 때문에 합 13,801 > 12,304) · 이름은 **로그 값 기준**이라 `smallJ` = **큰 `|j|`**(3072 노드) · `bigJ` = **작은 `|j|`**(128 노드). Keras `Dense(…, relu) → Dense(3, relu)` · `loss='mse'` · `optimizer='adam'` · `metrics=['accuracy']`(회귀에 무의미) · 500 에폭 · 배치 80 · 검증 분할 · 조기 종료 없음 · 정규화 항 없음.
- **Fig. 8 (봤다)** unseen `G_c`: (a–c) `G_c` 5 · `J_s` 261 — `[도표]` 표면 · 벌크 농도 0.5 → 1 이 ≈245 s 에 끝, ANN 이 ≈1–2 % 뒤처짐 · `⟨d⟩` 개시 ≈120 s, 끝 **≈0.31**(FE) ↔ ANN 약간 늦음. (d–f) `G_c` 10 · `J_s` 183 — 끝 ≈350 s, 벌크에서 ANN 이 눈에 띄게 아래(끝 ≈0.98 ↔ FE ≈0.99), `⟨d⟩` 끝 **≈0.075**, 개시 ≈230 s. `[해석]` (e) 의 어긋남은 **닫힌 식(`soc_dot = 2|j|` 직선)을 망이 틀린 것** — 질량 보존 위반이 거시로 들어간다. 두 곡선 쌍 모두 오차 척도 · 반복 0.

## 4.3 셀 계산 (§3.2.3 — Fig. 9 · 10 · 11 봤다, 원본 래스터 픽셀 판독 병행)

- **Fig. 9** (1 C · `G_c` 5.97): `[도표]` 끝 시각 무손상 ≈3560 s ↔ 손상 ≈3450 s(**−3.1 %**) · `⟨d⟩`(두께 평균) 개시 ≈2000 s → 끝 ≈0.19. `[인쇄]` 손상은 분리막 가까운 입자에서 먼저. `[재현]` 개시 ≈2000/3560 = 0.56 전달 ⇒ SOC ≈0.78 — 미세 자료 개시 SOC(0.78)와 맞는다.
- **Fig. 10** (1 · 2 · 5 C · `G_c` 5.97): `[도표]` 끝 ≈3450 · ≈1890 · ≈715 s · 끝 `⟨d⟩` ≈0.19 · 0.20 · 0.205 · 개시 ≈2000 · ≈950 · ≈290 s. `[인쇄]` "at higher C-rates the cell potential drops faster and the delivered capacity is smaller" · "At higher C-rates damage starts earlier and evolves faster". `[재현]` **전하 축으로 옮기면**: 전달 전하(1 C·s 단위) 3450 · **3780** · 3575 — **2 C 가 1 C 보다 ≈10 % 더, 5 C 도 ≈4 % 더 낸다**(D10). 개시 전하 2000 · 1900 · ≈1450 — 5 C 에서만 뚜렷이 이르다. 끝 `⟨d⟩` 는 세 율이 거의 같다 ⇒ "damage … evolves faster" 는 **시간 축 명제**이고, 리튬화 축에서는 미세 자료대로 대부분 율 무관이다(`[해석]`).
- **Fig. 11** (1 C · `G_c` 13.92 · 9 · 5.97 · 5 · 4.21): `[도표]` 끝 ≈3625 · ≈3600 · 3450 · 3370 · 3250 s · 끝 `⟨d⟩` ≈0.03 · 0.09 · 0.19 · 0.27 · 0.41. `[인쇄]` "Three of these fracture energies 13.92, 5.97, 4.21 J/m² are also the ones used for training … the other two are chosen arbitrarily from the range" — `G_c` **9** 는 Fig. 8 에서 검증한 10 이 아니다. ⚠ `G_c` 13.92 · 9 의 끝(≈3600–3625 s)이 **Fig. 9 무손상(≈3560 s)보다 늦다** — 식 (32) 로는 손상이 용량을 늘릴 수 없다(D11; 판독 오차 ≈±25 s).
- 효율: `[인쇄]` "it is expected that the data-driven method is much more computationally efficient" — 손상 사례의 시간 비교 **0**(FE² 미실행).

---

# 5. 결론 (인쇄 요지)

`[인쇄]` "The sequential data-driven multiscale framework … is benchmarked against the conventional concurrent method for a mechanically uncoupled example. Results show a good agreement" · "The surrogate model is capable of predicting the damage evolution even for unseen values of fracture energy" · "by discharging at higher C-rates the interface delamination starts earlier and evolves quicker, which means the contact loss … occurs faster" · "The more brittle the interface is, the faster the damage evolves. This can be considered in material choice and design". 향후: RNN(이력) · 지배식 제약(PINN) · 미세 물성 · 기하 입력 확장.

---

# 6. 박리의 자리 — 판정 근거 정리

1. **식이 말하는 것**: 손상은 거시 식에 `a` 한 곳으로만 들어간다(식 (31)(32)). BV (26) · `i₀` (27) · OCP (30) · 입자 확산 (19) 어디에도 `⟨d⟩` 없음. (`d` 는 미세에서 계면 견인력 (22)만 줄인다 — 역학 경로.)
2. **미세 경계가 말하는 것**: `[코드]` 입자 총 유입 = `j × 둘레`, `d` 와 무관(12,304 행, ±0.13 %).
3. `[해석]` 두 사실을 합치면 **`a·(1−⟨d⟩)` 는 입자 수(= `ε_s`)를 줄인 것과 같다** — 대표 입자의 `c̄` 는 "살아남은 입자" 의 것이고, 빠진 분율의 Li 는 추적되지 않는다(합계 보존 없음). 37호 줄의 두 선택지 중 **"`ε_p(N)` — 정의상 `LAM_PE`"** 쪽. 글의 서사("reduction of the surface available for reaction, affects the charge transfer … surface concentration increases faster")는 동역학 서사지만, 1 µm 입자 1 C 에서 실제로 곡선을 움직이는 것은 **입자당 과충전 속도**다.
4. `[재현]` 방증: 저율 극한 손실(미세 자료 적분)과 1 C 셀 손실(그림)이 `G_c` 4.21 에서 8.9 ↔ 8.7 %, 5.97 에서 3.9 ↔ 3.1 %.
5. ⇒ **이 모델로 ASSB 합성 truth 를 만들면 박리는 truth 단계에서 `LAM_PE`(동적, 방전 중 증가)와 같은 손잡이다** — 카드 물음을 시험하지 않고 미리 답한다(37호 새 제약 3 의 두 번째 표본, `[추론]`).

---

# 7. 이 편을 ASSB 합성 truth 에 쓸 때 (`[추론]`)

- **쓸 수 있는 것**: (i) `⟨d⟩(SOC; G_c)` 모양 — 개시 SOC 0.73–0.89 · 끝 0.03–0.45(표 §4.1), 이방 고유변형이 만드는 **SOC 문턱형** 손상 곡선의 한 예 (ii) "손상이 리튬화 상태로 정해지고 율에는 약하다" 는 모델 명제(`|j|` ≤ 0.03) (iii) 방전 중 `⟨d⟩` 가 커지는 **한 반주기 안의 동적 `LAM`** 이라는 형태.
- **쓰면 안 되는 것**: (i) `θ(N)` — 없음 (ii) 손상 ↔ 면적의 규약 — 이 편의 결합은 `LAM` 자리이므로 `A_eff` truth 로 옮기면 뜻이 바뀐다 (iii) 대리모형 자체 — 이력 없음 · 충전 불가 · 망 전환 규칙 미상 (iv) C-율 효과(D10 · D11 이 풀리기 전).
- **요구로 번역**: 미세-거시 결합 모델로 truth 를 만들 때 **질량 보존 검사** — "미세 입자 채움 속도 × 입자 부피 분율 = 거시 소스" 가 손상이 있을 때도 성립하는가. 성립하지 않으면 그 손상 변수는 `ε_p` 손잡이다.

---

# 8. 계보 대조

| 편 | 접촉/박리 변수 | 거시 자리 | `θ(N)` |
|---|---|---|---|
| 01호 Bielefeld 2019 | `θ`(퍼콜레이션 이용률) | 용량 | 0 |
| 37호 Li 2024 | `A_eff` | BV 분모만 — `A_eff ↔ k` 항등 | 0 |
| 56호 Bielefeld 2022 | `φ`(표면 피복, void) | 3D 해상 — 입자 안 확산 경계 | 0 |
| **58 = 이 편** | `⟨d⟩`(CZM 손상 면적 평균) | `a·(1−⟨d⟩)` + 미세 전 표면 유입 ⇒ **`ε_p`** | **0**(한 방전 안 `⟨d⟩(t)`) |

- 27호 경고("P2D 에서 접촉 손실이 들어갈 곳은 용량과 면적을 함께 깎는 손잡이 하나뿐") — 이 편은 FE² 두 단계를 쓰면서도 **같은 한 손잡이로 돌아왔다**: 미세를 해상했는데 결합이 `a` 한 곳이기 때문이다(`[해석]`).
- 23호 Koerver 2017 — 이 편의 유일한 실험 연결은 Fig. 1b 로 재게재한 SEM 한 장이다. 정량 대조 0.
- 36호 Thelen 2024(확률적 ML 기준) — 불확실성 0 · 보정 0 · 분포 밖 검사 0. 35호 Roman 2021 의 신뢰구간 보고와도 대조적.

---

# 9. 곱 축퇴 처방 — 마흔한 번째 적용

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R·C` | EIS 0 · 이중층 없음 | ❌ |
| **2단계** 면적 대조군 | **모델 안**: 손상 on/off(Fig. 9) = "면적만 바꾼 쌍" 의 모델판 — 그러나 결합상 `ε_p` 쌍 | ⚠ 이름은 면적, 결합은 `LAM` |
| **3단계-a** `Ea` | 298.15 K 한 점 | ❌ |
| **4단계** 두 영역 | 없음 | ❌ |
| 율 스윕 줄 | 1 · 2 · 5 C — 저율 기준 없음 · `[재현]` 전하 축에서 2 C > 1 C(D10) | ❌ (그림 자체가 율 순서를 어긴다) |
| 이완 OCP 줄(38호) | 0 | ❌ |

**곱이 선 자리**: 이 모델에서는 곱이 **서지 않는다 — 한 칸으로 무너진다.** `⟨d⟩` 는 `ε_s` 와 같은 결합이라 `(1−⟨d⟩)·ε_s` 가 한 인자이고, `A_eff ↔ k` 쪽 자리는 이 모델에 **따로 없다**(`i₀` 불변). ⇒ 새 줄 **"박리 변수의 거시 자리는 미세 경계조건이 정한다 — 질량 보존 검사(입자 채움 속도 ↔ 거시 소스)와 저율 극한 용량 손실(`∫⟨d⟩dSOC` ↔ ≈0)로 `ε_p` 자리 ↔ `A_eff·k` 자리를 가른다"**. 대리모형 편에 거는 부칙: 대리의 학습 분할이 궤적 안 행 무작위면 R² 는 충실도의 상한이지 일반화가 아니다 — 궤적 단위(또는 `G_c` · `j` 격자점 단위) 분할을 요구한다.

**⚠ 이것이 곱을 푼 것은 아니다** — 전부 모델 명제이고, `ε_p` 자리 판정은 인쇄 식 + 자료 질량 보존 + 그림 판독의 결합 위에 있다(MOOSE 입력 미열람).

---

# 10. Q1–Q8 / 채움표 행

| Q1 정량 | Q2 독립관측 | Q3 라벨층위 | Q4 유일성 | Q5 Li-In | Q6 압력 | Q7 dead Li | Q8 화학·OCP |
|---|---|---|---|---|---|---|---|
| **이동 없음 — 층 하나(모델 명제)** "박리 `⟨d⟩` 는 `a·(1−⟨d⟩)` 로 들어가지만 미세 유입이 `d` 무관이라 결합은 `ε_p`(`LAM_PE`) 자리; `⟨d⟩` 는 한 방전 안에서 SOC 의 함수(개시 0.73–0.89, 끝 0.03–0.45)". `θ(N)` **0/58**(한 방전 · 충전 불가 · 이력 없음) | 없음 — 실험 0 | ★ 층 하나 — **"simulated-surrogate: 원 모델 출력으로 학습 · 행 무작위 분할로 검증 · 셀 수준 기준해 없음 · 불확실성 0"** | **0/58 — 쉰 번째 성질 "대리의 충실도(원 모델 대비 R², 같은 궤적 안 행 분할)를 정확도로 인쇄했고, 원 모델 자체는 검증하지 않았다 — 그리고 그 원 모델에서 박리는 `LAM` 과 같은 손잡이다"** | 해당 없음(음극 미해상, 반쪽전지) | 없음(`MPa` 0 · 스프링 경계만) | 해당 없음 | 없음 — 남의 액체셀 NMC OCP 적합식 입력 |

누적 **≈20.0 → ≈20.0 (새 칸 0)**.

---

# 11. 어긋남 (실제로 어긋난 것만)

- **D1 플럭스 척도** — 지면 `J_s` 783 · 261 · 183 mol m⁻² s⁻¹(Fig. 7 · 8) = `[코드]` `j` 0.3 · 0.1 · 0.07 × **2609.6** 정확히; 상한 8.3 × 10² · 2.6 × 10³ 도 × 2609.6 쪽(0.318 · 1.0). README 는 "J\*=2609.6J". `[재현]` 2D 원판 채움 시간 `Δc·(R/2)/J` 는 `J = j/2609.6` 이면 **250 s**(Fig. 8a `[도표]` ≈245 s ✓), 인쇄값 261 이면 **3.7 × 10⁻⁵ s**. ⇒ 인쇄된 플럭스는 물리값의 **2609.6² ≈ 6.8 × 10⁶ 배**. 하한 2.8 × 10⁻⁷ 은 어느 환산으로도 격자 끝(`|j|` 10⁻⁴ · 10⁻⁵ · 필터 8 × 10⁻⁴)과 안 맞는다.
- **D2 벤치마크 자료 범위** — 지면 "n = −7, …, 3"(11 자릿수) · "around 6000" ↔ `[코드]` `j` 10⁻⁵–1(5 자릿수) · 필터 뒤 29 값 · **4,017 행**.
- **D3 벤치마크 모델 종류 · 출력 활성** — 지면 Keras · 출력 ReLU ↔ `[코드]` sklearn MLPRegressor 0.24.0 · `out_activation_` **identity**(피클 문자열) · 목표 `c_dot` 에 `−log₁₀`(지면에 없음).
- **D4 표 5** — R²₁ 0.99184 = bigJ 노트북 **학습** R²(시험 0.99199); R²₂ · R²₃ · MSE₂,₃ 는 노트북 출력에 없다(mediumJ 시험 0.99415 · MSE 1.21 × 10⁻⁵; smallJ 0.99950 · 8.0 × 10⁻⁶). 노트북이 논문 수치를 낸 실행이 아닐 수 있다(저장 파일 이름 날짜 2021-10/11, 저장소 2022-11-07).
- **D5 R² 인자 순서** — 손상 노트북 셋 모두 `r2_score(y_pred, y_true)`(sklearn 규약은 `(y_true, y_pred)`, 비대칭). 벤치마크는 올바름.
- **D6 식 (41) L2 항** — 세 Keras 모델 `kernel_regularizer: null`(λ = 0). λ 값 지면 미인쇄.
- **D7 "non-zero"** — ReLU 는 ≥ 0 이다. `[코드]` 자료 `d_dot` 음수 23 행(최소 −3.35 × 10⁻⁶) — KKT 비가역과 어긋나는 후처리 잡음, ReLU 가 잘라낸다. 같은 ReLU 가 `ċ` < 0(충전)을 막는다.
- **D8 식 (26)** — 인쇄 BV 는 `η = 0` 에서 `J_s = (i₀/F)(2c̄ − 1)`(렌더로 확인) — 평형에서 플럭스가 0 이 아니다(`[해석]`, 오식 가능).
- **D9 식 (45)** — `∂c₁/∂r = J_s`(렌더로 확인) — `D₁` 이 빠져 차원이 안 맞는다.
- **D10 율 순서** — `[도표]`+`[재현]` Fig. 10a 전달 전하 2 C ≈3780 > 5 C ≈3575 > 1 C ≈3450(1 C·s 단위) ↔ `[인쇄]` "the delivered capacity is smaller" at higher C. 시간 축에서만 참. `[해석]` 가능한 원인 하나: 세 율이 서로 다른 망에 걸린다(§0) — 확인 불가.
- **D11 손상 > 무손상** — `[도표]` Fig. 11a `G_c` 13.92 ≈3625 s · 9 ≈3600 s ↔ Fig. 9 무손상 ≈3560 s. 식 (32) 는 `a` 를 줄이기만 한다.
- **D12 unseen 검증 설계** — `G_c` 5 · 10 의 `Y₀`/`H` 미인쇄 · 두 점의 `j` 는 학습 격자 값 · Fig. 11 은 검증 안 한 9 를 "arbitrarily" 사용.
- **D13 `D₁`** — 정규화 인자 · 시간 단위가 가리키는 `D` ≈1 × 10⁻¹⁴ ↔ 표 2 7 × 10⁻¹⁵(`[재현]`, 정규화 식 미인쇄 — 조건부).
- **D14 초록 "with respect to the theories and thermodynamics law"** — 물리 제약은 출력 ReLU(부호) 하나뿐이고, Fig. 8e 에서 닫힌 질량 보존 식을 망이 어긴다.

---

# 12. 그림 — 무엇을 봤나

자동 크롭 **16**(그림 11 · 표 5). **Read 6 장**: Fig. 5 · 7 · 8 · 9 · 10 · 11. 추가로 Fig. 9–11 **원본 래스터**(1800 px, 쪽 13 의 JPEG 3 개)를 뽑아 색 분류 픽셀 판독으로 끝 시각을 읽었고(틀 0 · 4000 s 눈금 = 틀선 가정), 식 (26) · (32) · (45)는 쪽 렌더로 확인했다.
**안 봄**: Fig. 1(개요 · 23호 SEM 재게재) · Fig. 2(흐름도 — 텍스트로) · Fig. 3(ANN 도식) · Fig. 4(구 개략 · FE² `dt` 수렴) · Fig. 6(미세 격자 · 경계조건 — 텍스트로). 표 1–5 는 PDF 텍스트로.
본문 서술과 어긋난 그림: **Fig. 10**(전하 축 율 순서, D10) · **Fig. 11**(13.92 · 9 가 무손상보다 늦게 끝남, D11). Fig. 7 은 서술("both a normal and a shear gap")과 맞지만 `d` 색은 어깨(미끄럼)에만 있다.

---

# 13. 참고문헌 중 후속 후보 (73 번호, 서지 기준 — 미열람 · 전부 큐 밖)

- **[11] Rezaei, Asheri, Xu 2021 *J. Mech. Phys. Solids* 157, 104612** — 이 편 CZM 의 원전(모드 의존 · 플럭스 영향 · ASSB 균열). `d` 가 플럭스를 막는 판이 여기 있는지가 §6 판정의 대조점.
- **[31] Bai, Zhao, Liu, Xu 2019 *J. Power Sources* 422, 92** — 식 (32) `a` 의 출처 · FE² 두 단계 원형.
- [19] Sultanova & Figiel 2021 *Comput. Mater. Sci.* 186, 109990 — AM\|SE 견인-분리 법칙(고분자 고체).
- [16] Bucci … Carter 2017 *J. Mater. Chem. A* 5, 19422 — ASSB 기계 파손 CZ 모델.
- [33] Fathiannasab … Chen 2020 *JES* 167, 100558 — 단층촬영 재구성 ASSB 3D 모델.
- [29] Wolff, Röder, Krewer 2018 *Electrochim. Acta* 284, 639 — 단일 이온 전도 P2D(`ċ₂ = 0` 근거).
- [63] Danner … Latz 2016 *JPS* 334, 191 — OCP 식 (30) 출처(액체셀).
- [4] Koerver 2017 = 23호(흡수됨).

---

# 14. 이 digest 가 주장하지 않는 것

- **"박리는 실제로 `LAM_PE` 다" 라고 하지 않는다** — 이 **모델의 결합**이 `ε_p` 자리라는 것까지다(인쇄 식 + 자료 질량 보존 + 그림 판독; MOOSE 입력 미열람).
- **표 5 가 조작됐다고 하지 않는다** — 저장소 노트북 출력과 안 맞는다는 것까지다(다른 실행일 가능성이 크다).
- **D1 에서 어느 쪽이 맞는지 단정하지 않는다** — Fig. 8 시간과 맞는 쪽은 `j/2609.6` 이라는 것까지(R = 1 µm · `c_max` 38320 · 2D 원판 가정 위).
- **D10 · D11 을 수치 결함으로 확정하지 않는다** — 그림 판독(±≈25 s)과 논문 서술 · 식의 대조까지다.
