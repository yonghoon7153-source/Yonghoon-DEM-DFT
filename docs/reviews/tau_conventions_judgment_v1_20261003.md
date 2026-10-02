# τ (굴곡도) 정의 닫기 — 판단 메모 (2026-10-03)

- 근거: τ 목록 (`docs/reviews/tau_inventory_20261003.md`, 27 변형 · 불일치 I-01~I-22) · 에이전트 기록 (`fam_retry_result_20261002.md` 10-03 절) · litdb 정본 카드 7 편 + `comparison_vs_ours_DEM.md` §J · COMSOL 5.6 Battery Design Module User's Guide 텍스트 (`comsol/BDM_UG.txt`) · 리포 코드 (`claude/stoic-knuth-NObVQ` HEAD `1afd37a9a`, **읽기만** — 리포에 쓴 것 0 건; 수치 재계산은 scratchpad `tau_memo_calc.py` · `tau_chain_check2.py`).
- 비준된 전제 (다시 열지 않음): **D1** 열 셋 f = σ_eff/σ₀ · T = φ/f · τ = √T · **D2** 면적 모드 Hertz · physics 둘 다 + 게이트 · **D3** φ = 질량 보존 φ · **D4** 이온 → 전자 → 열 · LHS-25 · LHS-26 을 LHS (130 + 64) · ps45 재계산 전에 닫는다.
- 표기: **(유도)** = 커밋된 `docs/data/case_master.csv` 열로 소비처 식을 다시 계산 (n = 157, 25 °C 코퍼스) · **(우리 산술)** = 원문 수치로 계산 · **[미확인]** = 근거 없음 · 제안 ID `TAU-xx` · `CL-94` 는 **원장 미등재 제안**.
- 이 메모가 쓴 숫자 중 claims.json `quotation_ban` 37 패턴과 겹치는 것은 없다 (대조함).

---

## §0. 한 줄 결론 + 1저자가 정할 것

**한 줄 결론** — 우리 **T = φ·σ₀/σ_eff (= 웹앱 τ_Lap,eff²)** 는 문헌의 "tortuosity factor" (Tjaden κ = τ² · Landesfeind τ · Nguyen conventional τ · TauFactor τ · Park τ_e · Minnmann 보고 τ² · COMSOL τ_F) 와 **식 · 정규화 (전체 단면 · 관통 방향 · 전 SE 부피) 가 같은 양**이다.  그런데 리포가 "COMSOL/EIS input" 이라 붙인 값은 그 **제곱근 √T** 라 COMSOL 에 그대로 넣으면 σ_eff 가 √T 배 (코퍼스 중앙 2.5×, physics 3.2×) 과대다.  기하 τ 셋 (τ_Dij · τ_Dij,all · 벽 τ) 은 τ_geo 범주로 타당하지만 수송 τ 가 아니고, 접촉 저항 0 가지 (τ_Lap,geom) 는 원기둥 R_bulk 때문에 **T < 1** (26/157 — 연속체 하한 위반) 이 나와 절대값을 쓸 수 없다.  값은 SE 가 많은 쪽 (φ_SE ≥ 0.44) 에서 Minnmann 과 −25 … +10 %, SE 가 적은 쪽 (φ_SE ≤ 0.35) 에서는 **실험보다 3–10 배 낮게** (Hertz-geom 모드; physics 1.7–6.6 배) 앉는다.

| # | 정할 것 | 선택지 | 권고 (근거 절) |
|---|---|---|---|
| 1 | **f 의 정규화 상자** (D3 의 짝) | (i) 판 간격 f + T = φ_mc/f — 상자 섞임 · (ii) f_mc = f_gap·L_gap/L_mc, T = φ_mc/f_mc · (iii) f_gap + T = φ_구합/f_gap | **(ii)** — T 가 현행 솔버 T 와 같은 값 (부피 보존 z-신장에서 불변), 인계 열만으로 T = φ/f 재현.  (i) 은 T 를 L_gap/L_mc 배 (LHS 0.898–0.985 · lhsx 0.867–0.931) 낮춘다 → 금지 · (iii) 은 T 가 (ii) 와 같지만 표의 φ (D3) 로 T 를 재현할 수 없다 (§3-6) |
| 2 | **비관통 N/A 규칙** | f 빈칸 · f = 0 | **f = 0 + 상태 `NOT_PERCOLATING`** (L0 띠 · 솔버와 `calc_percolation` 일치 때만) · T · τ 빈칸 (= ∞) · 그 밖 비정상은 셋 다 빈칸 (§5) |
| 3 | **physics 열 게이트 (D2)** | 지금 인계 · S3 뒤 인계 | 계산 · 인계하되 **"세대 1" 표지 + 물리 타깃 HOLD** (ψ 분모 `L2-01` · `L1-01/03` · `DESC-03` · `LHS-25` 열림).  ⛔ physics 가 SE-poor 쪽 실험에 더 가깝다는 이유로 고르지 않는다 — 그 차이의 주원인 후보가 ψ 배치다 (§3-7) |
| 4 | **"COMSOL/EIS input" 정정 범위** | 라벨만 · 라벨 + T 열 | 라벨 + **T 행 · T 내보내기 열 신설** (숫자 불변) — √T 행에서 COMSOL · EIS 낱말 제거 (`TAU-01`) |
| 5 | **등급 · COMSOL 2D 의 τ 축** | 그대로 · 웹앱 도우미로 통일 | Stage-E σ (Cronau(r_SE) · 파괴 인자 포함) 로 만든 값을 **τ 라 부르지 않는다** · 문턱 (√ 척도 1.8–6.0, 출처 없음) 은 "내부 등급선" 표지 — T 축으로 옮기면 문턱 제곱 (`TAU-03` · `TAU-16`) |
| 6 | **프레임 [1] "pure-SE ≈ 10 % @ 300 MPa (Minnmann)"** | 그대로 · 출처 미확인 등재 | **`CL-94` (제안) 등재 + 한 커밋 정정** — Minnmann 2021 본문 · SI 어디에도 없다 · MPM σ_y 0.30 보정이 이 앵커 위에 있다 (`TAU-10`) |
| 7 | **single.html:1847 "1.4 % 오차로 일치 — parameter-free external validation"** | 유지 · 철회 | **철회** — 한 케이스 · Hertz 모드만 (같은 φ 띠 n = 12 에서 T_H 2.36–4.87, 같은 케이스 physics √T 2.37) · σ₀ 기준 다름 (`TAU-02`) |
| 8 | **LHS-25 처방** | 안 A (입자별 표면 예산) · 안 B (라게르 면) | **진단 C0–C1 먼저 → 안 A (β_AM 1 · β_SE {1.0, 1.10}) → 결론이 갈리는 침대만 안 B**.  "Tabor 의 F = 실제 E 로 다시 만든 힘 (현행) 인가 평형 DEM 힘인가" 는 C1 을 본 뒤 정한다 (§6) |
| 9 | **LHS-26 처방** | 반지름 규칙 · 설계 상 | **설계 상 (`block`) 에서 모양 인자** · rough 는 1.40/1.10 출처가 생기기 전까지 인계 제외 유지 (§6-7) |
| 10 | **전자 · 열 T 정의 (D4 다음)** | — | 이온 인계 뒤.  전자: σ₀ 가 입자마다 다르다 (AM_P GB 인자) → 단일 σ₀ 규약 먼저 · 열: 다상 φ · k₀ 정의 + `CL-12` 세대 (§5-4) |
| 11 | **키 이름** | T · κ · tau2 | `f_ion_<mode>` · `tau2_ion_<mode>` · `tau_ion_<mode>` (mode = `hertz` · `physics`) — `tau2` 는 카드 명명 권고 (T = 두께 · 온도, κ = 열전도와 충돌) |
| 12 | **τ_e (전극 tortuosity factor)** | 지금 · 후속 | **인계 비차단 · 한정어로** — 관통 침대의 위상 dead-end 가 작다 (LHS 중앙 0.03 %) · 비관통 24 침대가 차이가 큰 집합 · 접촉망 τ_e 는 후속 (§7) |

---

## §1. 문헌 명명 대조표 — 양 하나에 한 줄

| 양 | 우리 기호 · 정의 | Tjaden 2018 (`tjaden2018_…`) | Landesfeind 2016 (`landesfeind2016_…`) | Nguyen 2020 (`nguyen2020_…`) | Minnmann 2021 (`minnmann2021_…`) | Park 2020 (`park2020_…`) | TauFactor (`taufactor_…`) | COMSOL 5.6 BDM UG |
|---|---|---|---|---|---|---|---|---|
| **f** | f = σ_eff/σ₀ (= φ/T) · 솔버 `sigma_full` (`network_conductivity.py:857` · 1156) | "ε/τ² 'diffusibility' / 'effective relative diffusivity'" (p.47 기호표 · p.49) | 1/N_M (이름 없음, Eq 1 A1373) · ⚠ Eq 7 의 **f = 비례인자** (다른 양) | 1/N_M (Eq 1, p1) | σ_i,eff/σ_i,0 (Eq 4 성분, 이름 없음, p.5) | εσ/τ 의 무차원부 (SI p.6 Eq S1·S2, 이름 없음) | D_eff/D (TauFactor.m:3490–3496) | **"effective transport factor" f_e = ε_p/τ_F** (Eq 6-6, p.375) |
| **T** | T = φ·σ₀/σ_eff · (유도) T_H 중앙 6.21 | **κ = τ² "tortuosity factor"** (Eq 2, p.48) · D_eff = (ε/κ)D_bulk "also valid for ionic and electronic conductivities" (Eq 3) | **τ "effective tortuosity"** N_M = τ/ε (Eq 5, A1374) · Eq 8 (A1375) · "τ in Eq. 5 appears often as τ²" (A1374) | **τ "conventional tortuosity factor"** τ/ε = κ₀/κ_eff (Eq 1, p1) — 관통 Dirichlet | **τ_i² "tortuosity factor"** (Eq 4, p.5) — ⚠ 인쇄식 (σ_eff/σ₀)·φ 는 역수 오식, 보고값 = φσ₀/σ_eff (SI Table S2 전 행 0.7 % 안, 카드 §4.3) | **τ_e · τ_s "tortuosity of electrolyte / active material"** (SI p.6 Eq S1·S2 · SI p.13) — "factor" 낱말 없음 · 값 미보고 | **τ "Tortuosity Factor (D:D)"** τ = D·VolFrac/D_eff (TauFactor.m:3495) | **τ_F "fluid tortuosity factor"** (p.375) · "tortuosity τF,i" (p.342) · τ_L "tortuosity factors" (p.449–450) · 배터리 "Electrolyte tortuosity τl" (p.266, 식 없음) |
| **√T** | τ = √T = 웹앱 τ_Lap,eff (`app.py:2610`) | "τ" (식 3 의 τ; flux τ = √κ — 리뷰는 기하 τ 와 같은 기호, p.61) | "τ² 관례의 τ" (A1374 문장) | — | τ_i (√ 는 보고하지 않음 — "2.07" 은 카드 산술) | — | — (Duquesnoy 는 CSV = τ, 그림 = √ — 카드 역링크) | — (입력 칸 없음) |
| **τ_geo** | τ_Dij · τ_Dij,all · 벽 τ = 경로 길이 / 쌍의 \|Δz\| (`dem_analysis_core.py:569–651` · 654–736 · `lhs_descriptor_harvest.py:1361–1416`) | **τ = Δl/Δx "tortuosity" (geometric)** (Eq 1, p.48) · τ_geo (Holzer, p.48) | **τ_path** (Eq 3, A1373) · τ_geo · τ̄_geo — "strictly distinguish" (A1374) | "geometrical tortuosities" (p2 · p7, 식 없음) | **τ_i = l_i/l_0 "geometric tortuosity"** (Eq 3, p.5) — 정의만, 측정 없음 | — | — (모드 1–3 은 flux) | — |
| **τ_e** | — (리포에 없음) | — | Eq 13 τ = R_Ion·A·κ·ε/(2d) (A1382, 차단 대칭셀 TLM — Nguyen 의 eSCM 원조) | **τ_e "electrode tortuosity factor"** τ_e/ε = R_ion·A_CC·κ₀/L (Eq 2, p8) | EIS-TLM 이지만 셀이 전자 차단 + 양단 Li-In → 관통형에 가깝다 [판독 — nguyen 카드 ⑤] | — | mode 6 "Electrode Tortuosity" (TauFactor.m:3681–3685 · 계수 3 유도 [미확인]) | — |
| **N_M** | 1/f = T/φ (열 없음) · `R_bruggeman_over_full` = N_M/N_M(B) (`network_conductivity.py:1185`) | **N_M = σ_bulk/σ_eff = τ²/ε "MacMullin number"** (Eq 5, p.49) | **N_M = κ/κ_eff** (Eq 1) = τ/ε (Eq 5) · Archie N_M = ε^−m (Eq 2, A1373) | N_M = κ₀/κ_eff (Eq 1) ("McMullin"/"Mullin" 오기) | — (이름 없음) | — | — | — (= 1/f_e) |
| **Bruggeman** | `sigma_bruggeman` = φ^1.5 (`network_conductivity.py:1125`) ⇒ T_B = φ^−½ · √T_B = φ^−¼ | τ² = ε^(1−α), α = 1.5 (Eq 6, p.49) · γ 붙인 Eq 8 | τ = ε^(1−m) = ε^−α, **α = 0.5** (Eq 6, A1374) · N_M(B) = ε^−1.5 | — | — ("Bruggeman" 낱말 없음) | — | — | **τ_F = ε_p^(−1/2)** (p.376 · p.450) · "multiplies … by the porosity to the power of 1.5" (Electrophoretic, p.414) |

- ⚠ **같은 기호 다른 양** (이름표에 꼬리표 필수): ① Park **τ_e** (전해질 = 우리 T) ≠ Nguyen **τ_e** (전극 tortuosity factor) ≠ 우리 `_e` (전자) — 전자 꼬리표는 `_el_` (tjaden 카드 권고) · ② Landesfeind **f** (Eq 7 비례인자) ≠ 우리 f · ③ "formation factor": 우리 docstring `F_e = σ_eff/σ_AM,input` (`network_conductivity.py:13–15`, ≤ 1) 은 Archie (Landesfeind Eq 2 의 N_M = ε^−m, ≥ 1) 의 **역수** · ④ "geo/geom" 셋 (`I-08`): τ_Lap,geom (flux · CF) · Track-B `tau_geo` (flux · AM 여집합) · COMSOL 2D 파라미터 `tau_geo` (= Dijkstra, 기하) · ⑤ Bruggeman α: Tjaden/COMSOL 1.5 (f 지수) ↔ Landesfeind 0.5 (T 지수) ↔ √T 관례 0.25.
- **COMSOL Tortuosity 입력 = T (우리 `tau2`), √T 아님.**  확실성: **종 수송 인터페이스는 인쇄 식으로 확정** — Eq 6-6 f_e = ε_p/τ_F (p.375, Transport of Concentrated Species 의 다공 매질 확산 절 — 에이전트 기록의 "Diluted Species 375쪽" 은 쪽 머리말과 다르다) · D_e = (ε_p/τ_L)·D_L (p.449, Theory for Transport of Diluted Species) · Bruggeman τ = ε_p^(−1/2) (p.376 · p.450).  **배터리 인터페이스 (Porous Electrode 노드, p.266) 는 식을 인쇄하지 않는다** — "Electrode tortuosity τs · Electrolyte tortuosity τl … may also be used by the Effective Transport Parameter Correction" 뿐.  같은 모듈의 τ_F 정의 · Electrophoretic 의 "porosity^1.5" (p.414) · Landesfeind A1374 의 "Comsol … ε/τ = ε^1.5" 가 같은 관례를 가리키므로 **높음 — 단 인쇄 근거 없음** → GUI Equation 보기 캡처 1 장으로 닫는다 (미실행).
- COMSOL 자체 표기도 흔들린다: 같은 양을 "fluid tortuosity factor" (p.375) · "tortuosity" (p.342 · p.347) · "tortuosity factors" (p.449) 로 부르고, p.376 은 "the effective transport factor is τ_F = ε_p^−1/3" 라고 이름을 바꿔 적는다.  **⇒ COMSOL 의 "tortuosity" 낱말 = tortuosity factor = T.**
- Arzt 1982 는 τ 를 다루지 않는다 (§6 접촉면적 전용).

---

## §2. 우리 27 변형 — 판정표

문헌 비교값 약어 (ASSB 복합양극 · 조건 포함):
**[M]** Minnmann 이온 T 2.40 · 3.23 · 4.27 · 15.3 · 130 (φ_NCM 25/33/42/53/61 vol% · φ_SE 0.61–0.25 · 380 MPa 압밀 · ~40 MPa 측정 · σ₀ = 순수 SE 펠릿 1.6 mS/cm @25 °C · 순수 τ² ≡ 1 · SI Table S2 = 카드 §5.0); fine SE 61 vol% 33.8 · **[M√]** 같은 값의 √ 1.55–11.4 · **[P]** Park 측정 σ_eff 역산 T ≈ 4.3 / 11 / 21 (σ₀ 3.0 환산 · NCM 60/70/80 wt% · ε_e 0.477/0.347/0.217 · 추세 전용 — park 카드 §4-T(4)); √ 2.1 / 3.3 / 4.6 · **[G]** ASSB SE 상 기하 τ: 이 7 카드에 값 없음 [미확인]; 참고만 — 액체 LIB **기공**상 FMM · pore centroid 1.01–1.26 (tjaden §3-D Table 5) · **[E]** ASSB τ_e: 없음.

판정 5 단계: **타당** · **조건부** (조건 · 한정어 붙여 사용) · **이름만 틀림** (양은 맞음) · **정의 결함** (계산이 문헌 정의와 어긋남) · **쓰지 말 것**.

| ID | 이름 · 키 | 필드 양 (§1) | 정의 file:line | 입력 φ · σ₀ · 면적 | 우리 값 (n · 출처) | 문헌 비교 | 판정 | 필요한 수정 |
|---|---|---|---|---|---|---|---|---|
| **A. 기하 (τ_geo)** | | | | | | | | |
| T01 | τ_Dij 표본판 `tortuosity_mean/median/std/recommended` | τ_geo | `dem_analysis_core.py:569–651` (쌍 200 · seed 42 :611–615 · [1, 20) :629 · 폴백 :598–605) | — · — · SE 접촉 그래프 (중심 거리) | case_master n=163 1.149–17.49 (1.484) · LHS 웹앱 117/130 1.281–8.101 · lhsx 64 1.260–1.594 | [G] | **조건부** — 비관통 침대에 유한값 (`DESC-02W`: case_master 6/163 · LHS 11/130) 만 정의 결함 | 폴백 삭제 → None + 상태 (`TAU-05`) · 라벨 "기하 · 쌍 Δz" |
| T02 | τ_Dij,all `tortuosity_all_*` | τ_geo (FMM 형) | `dem_analysis_core.py:654–736` | — · — · 같은 그래프 | 커밋 표 없음 · ps45 5 건 1.194–1.235 (서술, `session_20260923_progress.md:833`) | [G] | **타당** | 툴팁 "τ_Dij 와 같거나 작다" 철회 (보장 아님 `I-17`, `single.html:1835`) |
| T03 | 수확기 옛 τ `tortuosity_dijkstra_SE` (solid_zrange) | τ_geo | `lhs_descriptor_harvest.py:1249–1358` · `_tau_sample` :1361–1416 | — · — · 원자 기하 그래프 | 14/130 1.318–2.040 · lhsx 31/64 1.271–1.541 | [G] | **쓰지 말 것** (T04 로 대체 · `LHS-08`) | 없음 (보류 유지 `lhs_design_dataset.py:739–742`) |
| T04 | 벽 τ `tortuosity_SE_wall(_median)` | τ_geo | 같은 함수, 벽 띠 :1334–1350 · 규약 :229 | — · — · 같은 그래프 | 130: 106 OK 1.292–4.151 (1.494) · 64/64 1.262–1.600 (1.365) · ps45 1.239–1.289 · 절단 0 | [G] | **타당** ("Tortuosity (기하학적)") | README 문구 "수송 τ (tortuosity factor) 가 아니다" → "flux τ 도, 그 제곱 (tortuosity factor) 도 아니다" · 덱 분모 "두께" (`LREL-05`) |
| T05 | 뷰어 경로 τ `paths[].tortuosity` | τ_geo (경로별) | `analyze_contacts.py:628–718` | — | 커밋 없음 | — | **조건부** (시각화 전용) | 라벨 "시각화 경로 · 통계 아님" |
| T06 | legacy 경로 τ `tortuosity_paths.json` | τ_geo | `analyze_contacts.py:808–841` (i ↔ i 짝 최대 5) | — | 커밋 없음 | — | **조건부** (시각화 전용) | 같음 |
| T07 | τ_Dij_R · v59 proxy | 혼종 (R 가중으로 고른 경로의 유클리드 길이) | `physics_fit_v60_tau_R_real.py:78–199` · `v59_tau_3way.py:76–82` | — · — · physics | 커밋 없음 | — | **쓰지 말 것** (개선 없음 CLAUDE.md:1783) | 보관 표지 |
| **B. flux T 형 (선형) — τ_F = φσ₀/σ** | | | | | | | | |
| T14 | STEP3 pore-τ `step3.pore.tau` | T (기공 확산) | `step3_sigma.py:1591–1672` (τ = ε/D_rel :1663) | ε 전 기공 (닫힌 기공 포함) · D₀ = 1 · 복셀 | 커밋 4 건 전부 None (비관통) · 서술 1,415 → 4.97e9 (`DR3-07`) | TauFactor 정의와 같음 (Li⁺ 아님) | **조건부** (구조 지표로만 — Li⁺ 수송 τ 아님) | 키 `tau2_pore_void_vox` 권고 · `TAU-04` |
| T15 | Track-B `tau_full` | T (이온 · 복셀 · CF 계열 `CL-81`) | `step3_sigma.py:3286–3296` · `mpm_webapp_payload.py:2481–2506` | φ = 전도상 복셀 분율 · 단일 σ 가드 · 복셀 | 커밋 없음 | [M] (정의 같음 · 접촉 저항 항 0) | **타당** (규약 문자열 `linear` 명시) | 꼬리표 `vox_cf` |
| T16 | Track-B `tau_geo` | T (AM 여집합 flux) | `mpm_webapp_payload.py:2507–2520` | φ_geo = 1 − AM 분율 · D = 1 | 커밋 없음 | — | **이름만 틀림** ('geo' 인데 flux) | `tau2_flux_amcomp_vox` |
| T17 | τ²_Lap 계열 `tau_sq_Lap_eff` · `tau_eff2` · SI 그림 τ²_Lap,eff | **T** | `build_tau_regime_db.py:137` · `tau_all_backfill.py:134` · `plot_tau_regime_si.py:98–100` | T08 과 같음 | (유도) H 1.945–3646 (6.212) · P 1.436–4401 (10.07) | [M] · [P] | **타당** (= D1 의 T · 게이트 조건) | 인계 `tau2` 의 원형 (§5) |
| T18 | 문헌 앵커 CSV `tau_ion_sq` · `tau_el_sq` | T (문헌) | `docs/data/minnmann2021_sigma_tau_porosity.csv` | — | tau_ion_sq 1–34 · tau_el_sq 1–120 | [M] | **조건부** — 61 vol% 거친 SE 행에 fine-SE 값 34 (SI S2 거친 SE = 130) · 25 vol% σ_ion "~1.4" (S2 0.408 mS/cm) · 42 vol% wt 73 (S1 = 70) · :2 에 인쇄식 Eq 4 | `TAU-12` (SI Table S2 로 교체) |
| **C. flux √T 형 — τ = √(φσ₀/σ)** | | | | | | | | |
| T08 H | τ_Lap,eff Hertz 열 | √T (FULL) | `webapp/app.py:2610` · :2744 | φ 구합 · σ₀ = `_sigma_grain_context` (T 짝, :7495) · **c_cpl[22] 기하 교차 원판** (`L1-04`, "Hertz" 는 이름만) | (유도) 157: 1.395–60.39 (2.492) | [M√] · [P] √ | **이름만 틀림** — 양은 맞는 √T, "COMSOL/EIS input" · "GB 포함" 라벨이 틀림 | `TAU-01` · 인계는 T 로 (§5) |
| T08 P | τ_Lap,eff physics 열 | √T (FULL) | `app.py:2611–2612` · :2745–2746 | 같음 · physics v1 면적 (`plastic_coverage.py:393–395`) | (유도) 1.198–66.34 (3.173) | 같음 | **조건부** — ψ 분모 (`L2-01`) 세대 1 · `L1-01/03` · `LHS-25` | `TAU-13` 게이트 |
| T09 | τ_Lap,geom = τ_Laplace,bulk | √T (CF = 협착 0) | `app.py:2613–2614` · :2747–2748 | 같음 · 면적 무관 (H↔P 차 ≤ 0.19 %) | (유도) 0.789–20.80 (1.206) · **< 1 이 26/157** | 대응 없음 (Minnmann "true geometrical" 은 개념만) | **정의 결함** — 원기둥 R_bulk 로 T < 1 가능 (§3-5) · 'geom' ≠ τ_geo | `TAU-07` · 인계 안 함 |
| T10 | 등급 `__tau_lap_eff` | √T + 재료 인자 | `grade_engine.py:927–935` (σ 선택 :775–784) | φ 구합 · **3.0 고정** · Stage-E physics 우선 (Cronau(r_SE) · 파괴 인자 포함) | (유도) 1.198–66.34 (3.173) · 웹앱 H 대비 0.852–1.584 (1.227) | — | **정의 결함** (τ 에 재료 인자 섞임 · 온도 불변성 깨짐 `L4-04`) | `TAU-03` |
| T11 | 등급 `__tau_lap_bulk` | √T_CF | `grade_engine.py:937–945` | 3.0 고정 · CF | = T09 | — | **정의 결함** (T09 + "Bruggeman φ^−0.5 ≈ 1.85" 지수 틀림 — √ 관례면 φ^−0.25, :180) | `TAU-07` |
| T12 | COMSOL 2D `tau_Laplace_eff` (→ `tau_eff`) · `tau_Laplace_bulk` (→ `tau_bulk`) | √T | `export_comsol_2d.py:67–79` · 표 :104–107 · README :660 | 3.0 상수 (:48) · Stage-E 우선 | 산출물 없음 | — | **정의 결함** — COMSOL τ_F 칸에 √T · README 식 φ 자리 반대 ("σ_eff = σ_grain / (φ·tau_eff²)") | `TAU-01` |
| T13 | 오프라인 재계산 계열 (`tau_Lap_eff` · `tau_L_*` · `tau_lap_*` …) | √T (혼합) | `build_tau_regime_db.py:93–95` · `compare_laplace_dijkstra.py:55–67` · `tau_all_backfill.py:125–134` 외 | 스크립트마다 σ 모드 다름 | `docs/db/section7_10case_sweep.csv` n=10 1.21–5.16 (σ 모드 미기록) | — | **조건부** (보관 · SI 진단) | 거듭제곱 · σ 원천 표지 |
| **D. 파생 · 재표지 · 유령** | | | | | | | | |
| T19 | C(τ) logpoly2 | τ_geo 의 회귀 함수 | `generate_comparison_plots.py:4789` · :6066–6069 · `predictor_engine.py:110–156` | T01 recommended → mean | — | — | **타당** (적합 특징 — 수송 τ 주장 아님) | 문서에 "C(τ_geo)" 명기 (CLAUDE.md:2076 "Laplace" 서술 `I-21`) |
| T20 | σ_brug 비 `sigma_ratio` = φ·f_perc/τ_geo² | Bruggeman 꼴 + 기하 τ | `dem_analysis_core.py:1112–1154` (:1147) · 행 ×3.0 리터럴 `analyze_contacts.py:276–278` | φ 구합 · 3.0 리터럴 | n=163 0–0.491 (0.128) | — | **조건부** (어림식 · 기하 τ ≤ flux τ 라 σ 과대 방향) | 'σ_Bruggeman' 행 이름 충돌 (`I-07`) 정리 |
| T21 | 망 Bruggeman `sigma_bruggeman` = φ^1.5 | Bruggeman (암묵 T = φ^−½) | `network_conductivity.py:1119–1125` · :1167–1168 · :1183–1185 | φ = 망 노드 (전 SE) 구합 | n=163 0.043–0.580 | [M] 대비 1.9–65× 벗어남 (Minnmann §16-3) | **타당** (기준선 · 구형 · 균질 한정 — Tjaden R2) | α 관례 표기 (1.5 형) |
| T22 | 비율 "Constriction overhead" — 웹앱 τ_Lap,eff/τ_Dij · 등급 τ_eff/τ_bulk | flux ÷ 기하 · (Stage-E) ÷ CF | `app.py:2626–2631` · :2760–2765 · 라벨 :2142–2143 · `grade_engine.py:183–190` · :947–953 | 섞임 | 웹앱 0.508–20.29 (1.711) · 등급 1.504–3.689 (2.588) · √(CF/FULL) H 1.76–3.50 (2.01) | Tjaden 같은 시료 flux/기하 **1.24–1.59** (접촉 저항 없이) | **정의 결함** (협착 배수가 아님) | `TAU-08` |
| T23 | ML `tau_se` | **T14 재표지** (기공) | `ml_cycle_surrogate.py:28` · :86 · selftest `train_cycle_surrogate.py:223` | — | — | — | **쓰지 말 것** (STEP3 자신이 금지 `step3_sigma.py:1623–1625`) | `TAU-04` |
| T24 | 예측기 · ML `tau` | τ_geo (T01 mean) | `predictor_engine.py:279–285` · `design_performance_corpus.csv` · `ml_design_structure.py:65` | — | n=291 1.149–4.324 · structure nested R² 0.921 | [G] | **조건부** (τ > 8 행 삭제 = 코호트 선별 `L5-01` · 비관통 유한값 `DESC-02W`) | 상태 열로 거르기 |
| T25 | PyBaMM `Bruggeman coefficient` ← τ | 자리 틀림 (지수 b 자리) | `webapp/pybamm_predictor.py:72` (porosity = 공극 :70) | ε = 공극 (ASSB 전해질상 = SE 여야) | 호출자 없음 | — | **쓰지 말 것** | `TAU-15` |
| T26 | 유령 키 `tortuosity_electronic_*` · `tortuosity_lap_eff` · `tau_lap_eff` · `tau_dij(_R)` | 없음 | 소비자만 (`generate_comparison_plots.py:6067–6069` · `app.py:2892–2915` · `refresh_warnings.py:76–95` …) — 생산자 0 (git grep) | — | 커밋 자료 0 | — | **정의 결함** (σ_e C(τ) 가 조용히 SE 이온 τ · 경고 영영 안 뜸) | `TAU-06` |
| T27 | "formation factor" F_e = σ_eff/σ_input | **f** | `network_conductivity.py:13–15` (docstring) · CLAUDE.md:150 | — | (유도) f_H 3.5e-5–0.356 (0.0467) | Minnmann f_ion 0.255 → 0.00191 (카드 §5.0) | **이름만 틀림** (Archie 이름은 1/f) | 문서 · `TAU-17` |

목록 대조: 인용한 목록 · 카드 줄 번호를 스팟 점검했다 — 전부 맞고, 잔차는 셋뿐이다: `active_fractions` 는 :999–1021 (목록 "1013–1016" 은 ±2 줄) · Arzt 카드 L-1 이 접촉 면적 상한식의 자리를 `network_conductivity.py` 로 추정했으나 실제 정의는 `plastic_coverage.py:266–404` (`film_area_from_overlap`, 망은 :316–320 에서 부른다) · COMSOL Eq 6-6 쪽 (§1).

---

## §3. 값의 합리성 — 필드와 맞대기

### 3-1. σ₀ 는 T 에서 약분된다 — 그래서 "정규화" 가 아니라 "기준 상태" 가 문제다
- 망은 ρ = 1 로 풀고 출력에서 σ_bulk 를 곱한다: `sigma_full_mScm = σ_ratio × σ_bulk × 1000` (`network_conductivity.py:1156`), 이온 σ_bulk = `se_material.sigma_grain_S_cm(T)` (:1226).  웹앱은 같은 출처 · 같은 온도의 σ₀ 로 나눈다 (`app.py:2601` → `_sigma_grain_context` :7495).  모든 간선 저항 (R_bulk · Holm) 이 1/σ 에 비례하므로 **T = φ/σ_ratio, f = σ_ratio — σ₀ 값 (3.0 이든 1.6 이든) 이 사라진다.**  (예외: 등급 · COMSOL 2D 는 3.0 상수 + Stage-E σ → 불변성 깨짐, `L4-04` · `TAU-03`.)
- 그러므로 Minnmann (σ₀ = 순수 SE 펠릿 1.6 mS/cm @25 °C) 과 T 를 비교할 때 **σ₀ 수치를 맞출 필요는 없다.**  σ₀ 가 들어가는 곳은 절대 σ_eff 뿐 — 같은 미세구조면 우리 σ_eff 는 3.0/1.6 = 1.875 배로 나온다 (σ_eff 끼리 직접 비교 금지 — minnmann 카드 §11).
- 남는 차이는 **기준 상태**다: Minnmann 은 순수 SE 펠릿의 τ² 를 **정의로 1** 로 둔다 (SI §3).  우리 T 는 간선 재료 (σ = 펠릿값, `CL-91`) 기준이고, 망이 SE–SE Holm 저항을 **그 위에 다시** 더한다 (부분 이중계상, CLAUDE.md CL-81 절).  같은 기준으로 맞추려면 **우리 순수 SE 침대의 T (T_pure,ours) 로 나눠야** 하는데 그 값은 리포에 없다 [미확인] — 원기둥 R_bulk 는 1 아래로, Holm 은 1 위로 미므로 방향도 미정.  ⬜ 검사 제안: 순수 SE 침대 망 1 회.

### 3-2. 우리 T vs Minnmann 2021 (SI Table S2) — φ_SE 로 짝지음 (±0.04)
우리 φ = 구합 φ (`phi_se`) · FULL 해 · (유도) · Minnmann φ_SE = 기공 14 % 포함 전체 부피 기준 (카드 §5.0).  T 는 일관된 상자면 φ 장부에 무관하다 (§3-6) — 짝짓기 축만 φ_mc 로 바꾸면 우리 점이 왼쪽으로 ≈ 2 % 이상 옮겨 간다 (case_master 의 (1−ε_union,쌍렌즈)/(1−ε_구합) 중앙 0.980 · 쌍 렌즈 union 은 정확 union 보다 낮게 잡혀 (`SELF-72`) 실제 이동은 이보다 크다).

| φ_NCM (vol%) | φ_SE | Minnmann T_ion | 우리 n | T Hertz-geom 중앙 [범위] | T physics 중앙 [범위] | T_H / T_M |
|---|---|---|---|---|---|---|
| 25 | 0.613 | 2.40 | 6 | 2.65 [2.21–3.24] | 2.28 [1.93–2.95] | 1.10 |
| 33 | 0.536 | 3.23 | 2 | 2.73 [2.59–2.86] | 2.51 [2.49–2.53] | 0.85 |
| 42 | 0.444 | 4.27 | 12 | 3.20 [2.36–4.87] | 4.15 [3.04–5.66] | 0.75 |
| 53 | 0.330 | 15.3 | 57 | 5.40 [3.89–18.6] | 8.77 [6.28–39] | 0.35 |
| 61 | 0.248 | 130 (fine SE 33.8) | 46 | 13.5 [6.21–26.6] | 19.7 [9.64–66.8] | 0.10 (fine 대비 0.40) |

### 3-3. 우리 T vs Park 2020 역산 (σ₀ 3.0 환산 · 추세 전용)
| NCM wt% | ε_e | Park T | 우리 n | T_H 중앙 [범위] | T_P 중앙 | T_H / T_Park |
|---|---|---|---|---|---|---|
| 60 | 0.477 | 4.3 | 9 | 3.11 [2.78–4.87] | 4.45 | 0.72 |
| 70 | 0.347 | 11 | 28 | 4.79 [2.73–11.7] | 7.58 | 0.44 |
| 80 | 0.217 | 21 | 36 | 15.1 [7.0–552] | 20.2 | 0.72 |

### 3-4. Bruggeman 배수 · flux ÷ 기하
| 비 | 우리 (유도, n = 157) | 문헌 |
|---|---|---|
| T / φ^−½ (Bruggeman 배수) | H 중앙 3.40 (IQR 2.54–6.71) · P 5.42 (3.94–9.62) | Minnmann 이온 1.9–65× (42 vol% 2.8×) · Park 2–24× · 액체 전극 1.5–3× (Landesfeind A1386) |
| √T_FULL / τ_Dij | H 1.711 (IQR 1.37–2.10) · P 2.09 (1.53–2.62) | Tjaden 같은 시료 기공상 **1.24–1.59** (표 4·5 쌍 셋, 우리 산술 — 접촉 저항 없음) |
| √T_CF / τ_Dij | **0.80** (IQR 0.69–1.03) | 같은 시료에서 flux ≥ 기하가 늘 성립 (Tjaden p.60 식 22 문장) — 우리 CF 는 **반대 방향** |

- ⇒ 웹앱 "Constriction overhead" (τ_Lap,eff/τ_Dij ≈ 1.7) 는 협착으로 읽을 수 없다: 접촉 저항이 없는 연속 기공상도 1.24–1.59 를 낸다.  우리 안의 순수 협착 배수는 같은 망 FULL/CF — √ 로 중앙 2.01 (H) 이다.

### 3-5. CF 가지가 T < 1 을 내는 이유 — 재유도 + 솔버 실측
- 사슬 N 개 · 반지름 r · 중심 간격 d · 상자 단면 A (사슬 하나) · 판 간격 L = (N−1)d + 2r.
- CF 간선 저항 R = 2 × (d/2)/(σπr²) = d/(σπr²) (`network_conductivity.py:401–403` — 반쪽마다 **입자 단면 전체 πr² 의 원기둥**).
- G = σπr²/((N−1)d) → f = G·L/(σA) = (πr²/A)·L/((N−1)d) · φ = N·(4/3)πr³/(A·L) (구합, :1120–1123).
- **T_CF = φ/f = (4/3)·r·d·N(N−1)/L²  →  N → ∞: (4/3)(r/d)** · d = 2r 이면 → **2/3** (√ 0.816) · d = 1.78r (순수 SE ⟨δ⟩ ≈ 지름의 11 %, CLAUDE.md E_SE 절) 이면 0.75.  T_CF < 1 ⇔ d > 4r/3.
- 같은 부피의 연속체는 T ≥ 1 이다: 단면 A(z) 인 1D 도체에서 T = ⟨A⟩⟨1/A⟩ ≥ 1 (Cauchy–Schwarz, 우리 유도) · TauFactor 관통 모드도 "τ ≥ 1" (taufactor 카드 ⟦10-03⟧ 정밀화 표) · 곧은 관통 기공 τ = 1 (Nguyen Fig 3).  원인: 구의 지름 방향 평균 단면은 (4/3πr³)/(2r) = (2/3)πr² 인데 원기둥은 πr² → 곧은 사슬에서 1.5 배 과전도.  3D 망에서는 접촉마다 단면을 따로 주므로 (SE 배위수 Z) 구 하나가 대표하는 도체 부피가 ≈ 0.75·Z 배로 부푼다 (d ≈ 2r, 우리 산술).
- **솔버 실측 (scratchpad `tau_chain_check2.py`, 리포 코드 import · 쓰기 0):** 평행 사슬 4 개 (띠마다 ≥ 3 입자) — N 30 · d/r 1.9998 → T_CF **0.6445** (식 0.6445) · N 120 · d/r 1.78 → **0.7413** (식 0.7413) · 같은 사슬의 T_FULL (c_cpl[22] 원판) 2.11–2.18 (d/r 1.78).
- ★ 덤: 사슬 **하나** (띠 입자 < 3) 로 돌리면 폴백 L1 (판 간격 15/85 %, :230–235) 이 조용히 켜져 T_CF 가 0.511 (N 30 · d/r 2.0) · 0.570 (N 30 · d/r 1.78) · 0.530 (N 120 · d/r 1.78) 로 **21–29 % 더 낮다** — 전압은 15–85 % 띠 사이에 걸리는데 σ 는 판 간격 전체로 정규화하기 때문이다.  ⇒ `LHS-17` 의 무기록 폴백은 퍼콜레이션 이름표만이 아니라 **σ · T 값도** 바꾼다 (LHS 130/130 은 L0 확인됨 — CLAUDE.md J20-b · 역사 코퍼스는 빈도 [미확인]).

### 3-6. φ 상자 (D3) 가 T 에 주는 영향
- 질량 보존 장부 (`dem_analysis_core.py:1274–1283`): L_mc = L_gap·(1−ε_구합)/(1−ε_union) · φ_SE,mc = (1−ε_union)·V_SE/ΣV ⇒ **φ_SE,mc·L_mc = φ_구합·L_gap** (우리 유도).
- 부피 보존 z-신장 (단면이 1/s 로 줄고 길이가 s 배, s = L_mc/L_gap) 이면 G → G/s², σ_eff → σ_eff/s, φ → φ/s ⇒ **T 불변**, f 만 1/s 배.  "bulge" 그림 (상자 = 판 간격, φ = 구합) 도 같은 T 를 준다.  ⇒ 일관된 두 상자 어디서든 **T = φ_구합·σ₀/σ_full (= 현행 웹앱 T)**.
- 섞은 짝 (φ_mc ÷ 판 간격 f) 만 T 를 s⁻¹ 배 낮춘다: 배포 v1.1 의 L_gap/L_mc = LHS 0.898–0.985 (중앙 0.959) · lhsx 0.867–0.931 (0.894) (`docs/data/lhs_release_20261001_v11/*.csv` 의 `thickness_wall_gap_um` ÷ `thickness_mass_conserving_um`).  ⇒ §0 결정 1 (ii).

### 3-7. 어디서 높고 낮은가 · 왜 (가설 — 미검정)
| 구간 | 우리 위치 | 후보 원인 (방향) |
|---|---|---|
| SE 많음 (φ_SE ≥ 0.44) | Minnmann 대비 H 0.75–1.10 · P 0.78–0.97 · Park 0.72 | 정합 범위.  단 42 vol% 띠 안에서도 T_H 2.36–4.87 로 퍼진다 (한 케이스로 "일치" 를 말할 수 없는 이유, `TAU-02`) |
| SE 적음 (φ_SE ≤ 0.35) | Minnmann 대비 **H 0.10–0.35 · P 0.15–0.57** · Park 대비 H 0.44–0.72 | ① 입경비 — 우리 생산 기본 SE ⌀1 µm · AM_P:AM_S:SE 크기비 12:4:1 (CLAUDE.md Fan 2026 · Furnas 절), Minnmann SE D50 3.45 · D90 20 µm ↔ NCM D̄ 3 µm (카드 §2.1): 작은 SE 가 같은 φ 에서 더 잘 잇는다 (그들의 fine SE 만으로 61 vol% T 130 → 33.8) · ② CBD · 바인더 차단 없음 (Landesfeind §9 ⑩: T 과소 방향) · ③ 원기둥 R_bulk 과전도 (§3-5) · ④ c_cpl[22] 면적 (탄성 Hertz 의 ≈2 배, `L1-04`) · ⑤ 연화 E 로 큰 겹침 = 높은 배위수 · ⑥ (반대 방향) 펠릿 σ₀ 위 Holm 이중계상은 T 를 **올린다** — 그런데도 낮다 |
| physics T > Hertz T | 143/157 에서 σ_physics < σ_Hertz (중앙 비 0.664) | physics 면적은 탄성 가지 (δ/R* < 0.0011) 를 빼면 max(πR*δ, A_LIGG, cap) ≥ c_cpl[22] 인데 (`plastic_coverage.py:393–395`) 저항이 더 크다 → **주원인 후보 = ψ 분모 배치** R_c = 1/(2σaψ) (`network_conductivity.py:444`, `L2-01` · 곱 배치면 반대가 될 것으로 예상 [미검증]).  ⛔ 실험에 더 가깝다고 physics 를 고르지 않는다 |
| CF | T_CF 0.62–433 (1.454) · < 1 이 26/157 | §3-5 — 절대값 비교 금지, 같은 망 안의 FULL/CF 분해에만 |

---

## §4. 고칠 결함 — 우선순위 (제안 ID · 원장 미등재)

⛔ 공통 제약: `network_conductivity.py` · `plastic_coverage.py` 는 S3 봉인 수치 모듈 (`seal_s3_prerun.py:99–100` `NUMERIC_MODULES`) — 주석 한 줄도 바이트 지문을 바꿔 S3 런 검증에 걸린다 (claims.json `CL-92` 비고).  09-28 `c0c2d4f44` 가 이 파일을 바꾼 이력이 있어 현재 봉인 상태 [미확인] → **이 두 파일은 건드리지 않고**, f/T/τ 는 봉인 밖 새 도우미 (예: `scripts/tau_flux.py`) 에서 계산한다.  규칙 J20-l: 코드 → 웹앱 → 게이트 → 커밋 한 묶음.

### P1
| ID | 결함 | file:line | 시험 먼저 → 최소 수정 | 웹앱 짝 |
|---|---|---|---|---|
| TAU-01 | **√T 에 "COMSOL/EIS input"** — COMSOL τ_F = T (§1) · EIS-TLM 은 τ_e 계열일 수 있음 → 넣으면 σ_eff √T 배 과대 | `app.py:1947` · 2050–2051 · 2140–2141 · 2606 · 2615 · 2623 · 2740 · 2757 · 9543–9544 · `single.html:1823` · 1841 · 1843–1847 · 1852 · `grade_engine.py:14` · 164–167 · 925 · `export_comsol_2d.py:72` · 104–105 · **660 (φ 자리 반대)** · `lhs_design_dataset.py:884` (→ 배포 · 인계 열 사전 TSV) · **3192 · 3222 (selftest 가 옛 문구를 강제)** · `plot_section7_design_rules.py:106` · `docs/bruggeman_tortuosity_network_20261002.md:32` · `docs/stage4_electrochem_research.md:44` · CLAUDE.md:25 | ① `export_comsol_2d.numerical_parameters` 합성 입력 → COMSOL τ_F 행 값 == φσ₀/σ (지금 실패) ② 웹앱 τ 블록 렌더 시험: √T 행에 "COMSOL" 없음 · T 행 있음 ③ selftest ㉓b 기대 문자열을 먼저 바꾼다 → 라벨 · README 식 · T 열 추가 (숫자 불변) | 케이스 τ 블록 · 툴팁 · 등급 툴팁 · 배포 README |
| TAU-02 | **"Minnmann 2.07 vs 우리 2.10 — 1.4 % 일치 · parameter-free external validation"** — 한 케이스 (particulate_11 Hertz; physics √T 2.369) · 같은 φ 띠 n = 12 T_H 2.36–4.87 · σ₀ 기준 다름 (§3-1) · "42 vol% CAM ↔ 42.7 vol% SE" 혼용 · σ₀ 라벨 "LPSCl bulk MLIP-MD value" (`CL-91` = 펠릿값) | `single.html:1845` · 1847 | 툴팁 문자열 시험 → 문구 철회 + "같은 관례의 대조 (T 4.41 vs 4.27, 단일 케이스 · 모드 의존)" | 같은 파일 |
| TAU-03 | **"τ_Laplace,eff" 한 이름에 입력 넷** (웹앱 raw H/P · 등급 Stage-E + 3.0 고정 · COMSOL 2D 같음 · regime DB raw H) — 등급/웹앱 H 0.852–1.584 (1.227) | `app.py:2610–2612` · `grade_engine.py:775–784` · 927–945 · `export_comsol_2d.py:68–79` · `build_tau_regime_db.py:93–95` | 같은 metrics → 등급 값 == 웹앱 값 (모드별) · σ_grain ×4 → T 불변 (등급 툴팁의 L4-04 예) → 한 도우미 · Stage-E 판은 "τ" 이름 제거 | 등급 표 · 그룹 비교 `grade:` 파라미터 |
| TAU-10 | **프레임 [1] "pure-SE porosity ≈ 10 % @ 300 MPa (Minnmann et al.)"** — Minnmann 2021 본문 · SI 에 순수 시료 기공값도 "300 MPa" 도 없다 (카드 §0) | CLAUDE.md:464 · 1101 · 1123 · 1143 · 1259 · 1310 · 1322 · 1325 · 1356 · 1392 · `mpm3d_compaction.py:19` · 618 (help) · `docs/mpm3d_calibration.md` (9 곳) · minnmann2022 카드 :429 (정본 브랜치) | 원장 **`CL-94` (제안)**: "MPM σ_y 0.30 보정 앵커 '순수 SE 10 % @300 MPa' 의 출처 [미확인] — Minnmann 2021 (본문 + SI) 에 없음" · status hold → 같은 커밋에서 문구를 "출처 [미확인] (Minnmann 2021 아님)" 으로 · 정정 뒤 정확 문자열을 `quotation_ban` 에 | 웹앱 해당 화면 없음 (보고) |
| TAU-13 | **physics T 가 ψ 분모 세대 1** — 게이트 없이 인계하면 "더 정교한 면적" 으로 오독 | `network_conductivity.py:425–452` (봉인) · `plastic_coverage.py:393–395` (봉인) | 코드 수정 없음 — 인계 열에 `ion_net_psi = legacy_divide` · 물리 타깃 HOLD (§5) · S3 판정 뒤 재계산 | physics 열 머리에 "세대 1 (ψ 분모)" |

### P2
| ID | 결함 | file:line | 시험 먼저 → 최소 수정 | 웹앱 짝 |
|---|---|---|---|---|
| TAU-04 | 기공 τ 가 ML `tau_se` 로 | `ml_cycle_surrogate.py:28` · 86 · `train_cycle_surrogate.py:223` | `build_matrix` 시험: pore.tau None · trackb tau_full X → `tau2_ion_vox` = X → 특징 이름 교체 (`tau2_pore_void_vox` 는 구조 축으로 따로) | 웹앱 화면 없음 (보고) |
| TAU-05 | 비관통 침대에 유한 τ_Dij (`DESC-02W`) | `dem_analysis_core.py:573` · 586 · 598–605 | 합성: 위 띠만 닿는 성분 → None (지금 유한) · σ_ionic T1 LOOCV 비트 불변 확인 (T1 은 f_p > 0 행만) → 폴백 삭제 + 상태.  ⚠ σ_e Stage 22.5 는 τ > 0 을 요구하고 (`generate_comparison_plots.py:6083`, 유령 키 → SE τ) σ_thermal T1 은 τ std · median 을 특징으로 쓴다 (:6909 · 6919) — 비관통-SE 6 침대 (input_2mAh_real_16 · a9_p00/02/06/08/10) 는 σ_e · κ 값이 있어 그 적합에 들어 있을 수 있다 [미확인] → 비트 불변이 깨지면 1저자 결정 (적합 동결 vs 재적합) | τ 블록 "— (미관통)" · 예측기 None 처리 |
| TAU-06 | 유령 `tortuosity_electronic_*` · `tau_lap_eff` | `generate_comparison_plots.py:6067–6069` · 6480 · `generate_fitting_report.py:675` · `app.py:2892–2915` · `refresh_warnings.py:76–95` · `electronic_nested_cv.py:187–191` | Stage 22.5 계수 비트 불변 시험 → 죽은 키 제거 · 보고서 문구 "σ_e 의 C(τ) 는 SE 이온 기하 τ" · 경고는 계산된 T 로 (또는 삭제) | 경고 배지 |
| TAU-07 | τ_Lap,geom ('geom' 오명 · T < 1 가능) | `app.py:1946` · 2138–2139 · 2613 · 9545 · `single.html:1837–1841` ("τ_Dij 의 0.8배 · GB") · `grade_engine.py:176–181` (φ^−0.5 — √ 관례면 φ^−0.25) · `export_comsol_2d.py:106–107` · `docs/literature_review_dem_mpm_assb.md:106` · taufactor 카드 §(2) | 곧은 사슬 시험 T_CF = (4/3)r d N(N−1)/L² (§3-5, 기록용) → 이름 "τ (flux · 접촉 저항 0 · 모델 내부 대비)" · 인계 안 함 | 같은 묶음 |
| TAU-08 | "Constriction overhead" 섞인 비 | `app.py:2142–2143` · `single.html:1849–1853` (낡은 "n=56 · 1.76×") · `grade_engine.py:183–190` · 947–953 (분자 Stage-E physics ÷ 분모 raw CF) | 등급 overhead == √(σ_CF/σ_full) 같은 모드 시험 → 협착 배수 = τ_FULL/τ_CF 로 정의 · 웹앱 행 이름 "flux ÷ 기하" | 같은 묶음 |
| TAU-12 | Minnmann 앵커 CSV 낡은 행 | `docs/data/minnmann2021_sigma_tau_porosity.csv:2` · 8–12 | SI Table S2 값으로 교체 (61 vol% 거친 SE 130 · fine 33.8 별행 · σ 전 행) · 인쇄식 Eq 4 문구 정정 | SI 그림은 42 vol% 한 점만 하드코딩 (`plot_tau_regime_si.py:134–136`) — 영향 없음 |
| TAU-14 | 띠 폴백이 σ · T 값을 바꾼다 (`LHS-17` 증거 추가) | `network_conductivity.py:230–247` (봉인) · `dem_analysis_core.py:505–523` | 인계 게이트: 띠 규칙 L0 일 때만 값 (§5) · 폴백 표지 열 | 웹앱 표에 띠 규칙 표시 |

### P3
| ID | 결함 | file:line | 수정 | 웹앱 짝 |
|---|---|---|---|---|
| TAU-09 | 망 `active_fraction` (바닥 = 집전체 기준) ↔ `ionic_active_pct` (위 = 분리막 기준) | `network_conductivity.py:999–1021` (봉인) ↔ `dem_analysis_core.py:741–768` | 이온 접근성은 분리막 기준 (Nguyen 방향 논리) — 이온 `active_fraction` 은 소비처 없음 (`NET_MERGE_KEYS` `pipeline_service.py:83–97` 에 전자만) → 열 사전 규칙만 · 이름 정정은 S3 뒤 | 없음 (보고) |
| TAU-11 | 카드가 Minnmann Eq 4 를 보고값 꼴로만 적음 (인쇄 역수 오식 미표기) | 정본 litdb: `bielefeld2020_…:136` · 505 · `interfacial_impedance_formulation_…:173` · `taufactor_…:146` / 반대 방향 (인쇄식을 맞는 식처럼): 리포 `docs/lit_minnmann2021_…:147` · CSV :2 | 한 줄 한정어 "(보고값 꼴 · 인쇄 Eq 4 는 σ 비 역수 — minnmann2021 카드 §4.3 · §17 #1)" — 카드는 정본 브랜치 커밋 | — |
| TAU-15 | PyBaMM 휴면 코드: τ → Bruggeman 지수 자리 · porosity = 공극 · 문서 처방 충돌 (`I-11`) | `pybamm_predictor.py:70–72` · `docs/stage4_…:44` ↔ `docs/stage2_…:55` | 삭제 또는 "tortuosity factor" 옵션 + T + φ_SE 로 재작성 · 문서 T 로 통일 | 호출자 없음 |
| TAU-16 | 등급 문턱 출처 "Tippens 2019, Famprikis 2019" 없음 (감사 D #97) · √ 척도 | `grade_engine.py:14` · 165–167 | "내부 등급선" 표지 · T 축 전환 시 문턱 제곱 | 등급 툴팁 |
| TAU-17 | "formation factor" = f (Archie 와 역수) | `network_conductivity.py:13–15` (봉인) · CLAUDE.md:150 | 문서 정정 · docstring 은 S3 뒤 | — |
| TAU-18 | 덱 τ_wall 분모 "두께" (`LREL-05` 열림) | `docs/report_20261021/build_deck_v2.py:316` · 325 | 원장대로 | — |
| TAU-19 | "τ_Dij,all ≤ τ_Dij" 보장 문구 (`I-17`) | `single.html:1835` · `docs/bruggeman_…:30` | 문구 삭제 (ps45 실측 3.5–4.3 % 작음은 예시로만) | 같은 파일 |
| TAU-20 | σ₀ 출처 라벨 제각각 (`I-15`) | `single.html:1845` · `export_comsol_2d.py:48` · 94–95 | "펠릿값 (Cronau 2021 SI 그림 S2c 하단 · CL-91)" 통일 | 같은 묶음 |

---

## §5. 망 인계 열 사전 초안 — 이온 먼저 (D4)

### 5-1. 열 (모드 = `hertz` · `physics`, 같은 정의 · 면적만 다름)
| 열 | 식 (정확히) | 이름 · 한정어 |
|---|---|---|
| `f_ion_<mode>` | f = σ_eff,mc/σ₀ = σ_ratio × (L_gap/L_mc) — σ_ratio = G_FULL·L_gap/(box_x·box_y) (솔버 `sigma_full`), L_gap = 판 간격, L_mc = 질량 보존 두께 (§0 결정 1 (ii)) | "유효 전도도 비 (diffusibility · COMSOL f_e · 1/N_M)" · σ₀ 수치에 무관 (§3-1) |
| `tau2_ion_<mode>` | T = φ_SE,mc / f_ion (= φ_구합·σ₀/σ_full — 현행 웹앱 T 와 같은 수) | "**tortuosity factor (flux · 접촉망 · Holm 협착 포함 · 관통형 conventional)** — COMSOL Tortuosity τ_F 입력 = 이 열" |
| `tau_ion_<mode>` | τ = √T | "τ² 관례의 τ (Minnmann √τ²) — **COMSOL 입력 아님**" |
| `ion_net_status` | OK · NOT_PERCOLATING · BAND_FALLBACK · SOLVER_ANOMALY · NOT_COMPUTED | 값 규칙 5-2 |
| `ion_net_area_mode` | `hertz` = LIGGGHTS c_cpl[22] 기하 교차 원판 π(rδ − δ²/4) (`L1-04`, 탄성 πR*δ 의 ≈ 2 배) · `physics` = v1 Tabor · 부피 · 기하 cap (`plastic_coverage.py:266–404`) | — |
| `ion_net_psi` | `legacy_divide` (세대 1) | physics 열에만 의미 (`L2-01`) |
| `ion_sigma0_mScm` · `ion_sigma0_T_C` | 3.0 · 25 (온도 런이면 `se_material` Arrhenius 값과 그 T) | "σ₀ = 간선 재료 σ = 펠릿값 (Cronau 2021 SI 그림 S2c µC-Li₆PS₅Cl 평탄 하단, `CL-91`) — f = σ_eff/σ₀ 의 기준" |
| `phi_basis` · `L_basis` | `mass_conserving` · `L_mc` | D3 |

### 5-2. 값 규칙 · 게이트
| 게이트 | 내용 | 실패 시 |
|---|---|---|
| G1 띠 | 솔버 띠 = L0 (입자 자기 반지름 2 배 · 양 끝 ≥ 3) — L1 폴백은 곧은 사슬에서 T 를 21–29 % 낮춘다 (σ 26–40 % 과대, §3-5) | BAND_FALLBACK · 셋 다 빈칸 |
| G2 관통 | 솔버 관통 성분 유무 == `calc_percolation` `percolation_pct` > 0 (같은 띠) | 불일치 → 빈칸 + 사유 |
| G3 비관통 | 관통 성분 없음 (G1 · G2 통과) | **f = 0 · T · τ 빈칸 (= ∞)** — "이온적으로 죽은 전극" 으로 읽지 말 것 (`ionic_active_pct` 는 유한, J20-p) |
| G4 온도 짝 | σ₀ 와 σ_full 같은 T — 시험: σ_grain 두 값 → T 비트 동일 (landesfeind 카드 §11-③) | 빈칸 |
| G5 수치 | G_eff ≤ 2·Σg (`network_conductivity.py:846`) · f ≤ φ (T ≥ 1 — 연속체 하한, FULL 은 코퍼스 157/157 통과) | SOLVER_ANOMALY · 표지 |
| G6 physics | ψ 세대 · cap_conflict 비율 (`L1-01`) · 탄성 가지 비율 · ψ 절벽 (a_eff/r_min ≥ s*, R_c → 0) 접촉 수 · LHS-25 Λ_i > 1 입자 수 | 값은 싣되 **물리 타깃 HOLD** |

### 5-3. 붙일 한정어 (열 사전 문구)
- "flux 기반 · 관통 (두 평행 띠 Dirichlet) **conventional tortuosity factor** (Nguyen Eq 1) — **electrode tortuosity factor τ_e (Nguyen Eq 2) 가 아니다** · 차단 대칭셀 EIS-TLM 의 τ (Landesfeind Eq 13 형) 와 **한정어 없이 비교하지 않는다**."
- "COMSOL Tortuosity 입력 = `tau2` (Eq 6-6, p.375 — 배터리 인터페이스 식은 인쇄 근거 없음 [미확인])."
- "z 한 축 (Tjaden 식 21 τ_C 와 직접 비교 금지) · 형상 · CBD 차단 없음 · σ₀ 펠릿값 위 Holm 접촉 저항 = 부분 이중계상 가능 (크기 미상)."
- "φ = 전 SE (비관통 · 고립 포함) — dead 부피가 T 를 키운다 (Nguyen Fig 2: 같은 N_M 에서 −35 %) → **1차 수송량은 f**."
- 문헌 T 와 맞댈 때: "Minnmann 은 순수 SE 펠릿 τ² ≡ 1 기준 (σ₀ 1.6 mS/cm @25 °C) — 우리 T 는 간선 재료 기준 (§3-1)."
- 인계하지 않는 것: CF 가지 (T < 1 가능) · Stage-E σ 로 만든 τ · 기하 τ (이미 `tortuosity_SE_wall` 로 따로 있음).

### 5-4. 전자 · 열 (D4 다음 — 정의 결정 먼저)
| 채널 | 막는 것 | 권고 |
|---|---|---|
| 전자 | σ₀ 가 입자마다 다르다 (`sigma_AM_relative` GB 인자, AM_P < 1) — Track-B 도 같은 경우 τ 를 None 으로 둔다 (`mpm_webapp_payload.py:2488–2505`) · σ_AM 50 mS/cm 는 모델 기준값 (`CL-92`) | 단일 σ₀ = σ_AM,input 기준 f · T 를 정의하고 GB 인자를 T 에 흡수한다고 명시 — 또는 f 만 |
| 열 | 다상 (AM–AM · AM–SE · SE–SE) · k_weight 가지가 옛 코퍼스에서 실행 안 됨 (`CL-12`) | φ = 전 고체 · k₀ 정의 결정 후, 세대 표지 |

---

## §6. LHS-25 · LHS-26 닫기 설계

### 6-1. "기하 원판의 약 3 배" 의 기준은 무엇인가 — **겹침 (교차) 원**이다
- 그 "기하 원판" = LIGGGHTS `c_cpl[22]` = 두 구의 **기하 교차 원판** (같은 반지름이면 π(rδ − δ²/4)) — `parse_liggghts.py:51–56` (`L1-04`: A_LIGG/A_Hertz = 2 − d/(2r), r 0.5 µm · δ/R* 0.05 에서 1.9875 배).  망의 "Hertz" 모드도 이 면적을 쓴다 (`network_conductivity.py:303` · 353).
- "≈ 3 배" 의 출처 = 비포화 LHS 침대의 physics v1 ÷ Hertz-geom 피복률 비: AM_P 2.364–3.373 (중앙 2.958) · AM_S 2.459–3.974 (3.203) (`docs/reviews/lhs_coverage_reasonableness_20261001.md:189`, :246 "실제 E (24 GPa) Tabor 면적이 DEM 기하 원판의 ≈ 3 배").
- Arzt 카드 L-6 대조: 원판이 겹침 원이므로 Tabor ≈ **Arzt 압밀 한계 초기 접촉 (겹침 원의 1.27–1.40 배, D 0.84–0.90) 의 약 2 배**.  (우리 산술 · 단분산 · 방향 참고) Arzt 근거리 (소결) 극한 = "upper bound for the contact areas" (p.1886) 의 초기 접촉 a(r=1) = 11(1 − 1/R′) 은 D 0.90 · 0.95 에서 겹침 원의 1.85 · 1.87 배 → Tabor 3 배는 **그 상한도 ≈ 1.6 배 넘는다**.

### 6-2. 진단 — Arzt 카드 L-3 을 한 군데 고친다
- 카드 L-3: Σ_j A_tabor,ij = Σ_j F_ij/H = 4πR_i²·p̄_i/H (Love–Weber) → 포화 ⇔ p̄_i ≥ H (0.85 GPa, `plastic_coverage.py:40`) → 평균장 0.35–0.42 라 "응력 꼬리 입자 현상" 이라 했다.
- **그런데 코드의 F 는 평형 접촉력이 아니다**: A_tabor = F_real/H, F_real = (4/3)·E*_real·√R*·δ^1.5, E*_real ≈ 22.4 GPa (`plastic_coverage.py:35–46` · 349–352) 를 **연화 E (SE 1.35 GPa) 로 생긴 DEM 겹침 δ** 에 쓴다.  Love–Weber 항등식은 DEM 힘 F_DEM (300 MPa 와 평형) 에만 선다.  ⇒ Σ_j A_tabor,ij/(4πR_i²) = **κ_i · p̄_i,DEM/H**, κ_i = ΣF_real/ΣF_DEM.  차수 (우리 산술 · Hertz 근사 · DEM 의 AM 모듈러스 [미확인]): E*_real/E*_DEM ≈ 15 (AM–SE) · ≈ 30 (SE–SE — `L1-03` 으로 AM–SE E* 를 같이 씀) ⇒ 포화 문턱 p̄_i ≈ H/κ ≈ **30–60 MPa** (≪ 300 MPa).
- ⇒ 포화는 "응력 꼬리" 가 아니라 **AM 의 하중이 AM–SE 접촉으로 지나가는 침대 (SE 많은 침대) 에서 일반적**이어야 한다 — 관측 (LHS 29/130 · lhsx 62/64 포화, `LHS-25`) 과 같은 방향.  둘 (H0 응력 꼬리 · H1 힘 재팽창 κ) 은 접촉 덤프 (법선력 `c_cpl[13–15]`) 만으로 가를 수 있다 (C1).
- 곁가지 (판정 아님): 평형 F_DEM 을 Tabor 에 넣으면 A_tabor ≈ (3/κ) × 원판 ≈ 0.1–0.2 × 원판 (같은 차수 산술) 이라 max(하한, ·) 에서 physics 가 기하 원판으로 접힌다 — "physics 면적의 증가분은 전부 E_real 힘 재구성에서 온다" 는 뜻이라 **모형 질문**이다 (1저자 결정 거리, C1 뒤).

### 6-3. 후보
| | 안 A — 입자별 표면 예산 (arzt 카드 L-4) | 안 B — 라게르 면 상한 (L-5) |
|---|---|---|
| 규칙 | Λ_i = Σ_j A_ij^raw/(β_i·4πR_i²) · s_i = min(1, 1/Λ_i) · A_ij ← A_ij^raw·min(s_i, s_j) · β_AM = 1 (정확) · β_SE {1.0, 1.10} | A_ij ≤ A_face,ij (radical plane 면 다각형) · 강한 판 = 원판 ∩ 다각형 |
| 근거 | Arzt 식 (7) · (A4)–(A6) · nisar2024 (22)–(25) · zunker2024 II (32)–(33) | Arzt p.1885 각주 · Fig. 5 ▲ — 다분산 일반화는 우리 가정 |
| 비용 | 접촉 목록 한 번 더 (bincount) | 프레임마다 분할 — 리포에 라게르 도구 없음 (`git grep` 0 · pyvoro 미설치) |
| 다루는 것 | 합 (평균장 축소) | 개별 접촉 충돌 |
| 약점 | 큰 접촉 · 작은 접촉을 같은 비율로 깎음 · 하한 밑으로 내려갈 수 있음 | 재배열 큰 저밀도에서 느슨 · 새 의존성 |

**권고**: A 를 기본으로, β 는 런 전에 고정 (β 로 목표를 맞추지 않는다).  예산을 **가장 바깥** (max(lower, ·) 뒤) 에 두고 하한 밑으로 내려간 접촉을 `budget_below_lower` 로 센다 — 이 순서 자체가 1저자 결정 (arzt 카드 L-4).  B 는 A 로 결론이 바뀌는 침대만.

### 6-4. 사전등록 검사 (결과 보기 전 등록 · 판정선 수치는 1저자 비준 뒤)
| 검사 | 무엇 | 통과 · 판정 |
|---|---|---|
| C0 | 130 + 64 + ps45 의 접촉 덤프로 A_physics 재계산 → 상별 Λ_i 분포 · Λ > 1 입자 비율 · "침대 포화 ⇔ AM Λ > 1" | 포화 침대 전부가 Λ > 1 입자를 가져야 (아니면 다른 원인) |
| C1 | AM 마다 κ_i = ΣF_real/ΣF_DEM · p̄_i,DEM = ΣF_DEM/(4πR_i²) · 항등식 Λ_i(tabor) = κ_i·p̄_i/H 수치 확인 (원자 응력 말고 접촉 목록 — 비리얼 반분 주의) | H0 (p̄_i > H) vs H1 (κ_i·p̄_i > H) 중 포화를 설명하는 쪽 |
| C2 | 안 A (β_SE 1.0 · 1.10): AM 피복률 ≤ 100 % 구성상 (194/194 assert) · `budget_below_lower` 수 · v2 분모 붕괴 18 침대 회복 여부 · ρ(피복률, SE/고체) 부호 · Λ ≤ 1 만 있는 침대 비트 불변 | 비트 불변 · 상한 assert 는 반드시 통과 |
| C3 | 망 physics σ (예산 전/후) — ψ 배치 고정 (legacy) | 보고만 (`L2-01` 과 얽힘: 면적을 줄이면 ψ 벌점이 줄어 σ 가 **오를** 수 있다) |
| C4 | 안 A 가 침대 순위를 바꾸면 (순위 상관 문턱은 런 전 등록) 그 침대만 안 B | — |

### 6-5. 코드 자리
| 자리 | 봉인 | 할 일 |
|---|---|---|
| `scripts/coverage_physics_vs_hertzian.py` (AM–SE physics 누적 ≈ :480–560) | 아님 | 안 A 패스 (새 함수 · 시험 먼저) |
| `scripts/plastic_coverage.py:266–404` (접촉별 면적) | **봉인** | 건드리지 않음 |
| `scripts/network_conductivity.py:303–353` (간선 면적) | **봉인** | 봉인 밖 래퍼에서 간선 사후 패스 또는 S3 뒤 |
| 웹앱 physics 피복률 · 망 physics 열 · 툴팁 | — | 같은 정의 · 이름 (J20-l) |

### 6-6. 1저자 결정으로 남기는 것
① 예산 위치 (하한 앞/뒤) ② β_SE 범위 ③ C1 결과에 따라 Tabor 힘을 F_real 로 둘지 F_DEM 으로 둘지 (모형) ④ C4 문턱.

### 6-7. LHS-26 — 모양 인자를 설계 상에서
- 지금: rough 피복률 `sf = SHAPE_FACTOR.get(lbl)` (`coverage_physics_vs_hertzian.py:534`; AM_P 1.40 · AM_S 1.10 `dem_analysis_core.py:26–30`) 의 lbl 이 `type_map_resolve.py:134` 의 반지름 규칙 (총칭 `${r_AM}` → r > 0.004 sim → AM_P) 에서 온다 → mono_AM_P 인데 r ≤ 4 µm 인 9 침대 (lhs00_118 · 121 · 124 · 125 · 126 · lhsx_003 · 017 · 048 · 062) 가 1.10.
- 수정: 설계 CSV 의 `block` (mono_AM_P / mono_AM_S / bimodal — `lhs_design_dataset.py:365`) 을 상 이름의 정본으로 넘기는 명시 덮어쓰기 (`phase_override`) · 반지름 규칙은 덱이 총칭 변수일 때의 진단으로만.  시험 먼저: 위 9 침대 → 1.40 (지금 1.10).  ps45 는 r_AM_P 4.5 · r_AM_S 2.0 µm 라 규칙과 설계가 같다 (`ps45_handover.csv`).
- 남는 것: 1.40 / 1.10 값 자체의 출처 (B3) 는 이 카드들에 없다 [미확인] → rough 는 인계 제외 유지 (J20-m).

---

## §7. τ_e 공백

- 리포에 **electrode tortuosity factor 경로가 없다**: 접촉망은 양 끝 띠 Dirichlet 관통형 (`network_conductivity.py:225–249` · 590–593) · STEP3 도 관통형 (`step3_sigma.py:835–840`) · TauFactor mode 6 대응 없음 (nguyen 카드 판정).
- 인계에 문제인가: **ML 구조 기술자로서는 아니다** — T 는 conventional τ 로 정의가 닫혀 있고 한정어로 충분하다 (§5-3).  **COMSOL/P2D 매개변수로는 문제다** — Nguyen 은 τ_e 를 권한다 (p5 · p8, 단 "recommended" 이지 검증 아님).
- 차이 크기 감각 (우리 산술): 관통 침대의 위상 dead-end (위 띠 도달 − 관통, 배포 v1.1 `top_reachable_pct − percolation_pct`) = LHS 106 침대 중앙 **0.03 %** (최대 10.98 %) · lhsx 64 ≤ 0.04 % → Nguyen 의 잘 퍼콜된 구 충전 (dead-end 4 · 8 % → τ_e/τ +0.8 · +3.9 %) 보다 작다.  ⚠ 위상 dead-end 는 flux dead-end (최대 flux 2 % 문턱) 의 **하한** · ASSB 경계조건 (이중층 = AM–SE 접촉만) 이 다르다 (nguyen 카드 ⑥).  **차이가 큰 집합 = 비관통 24 침대** (T = ∞ 인데 τ_e 는 유한).  관통 침대의 비관통 SE 몫 (100 − percolation_pct) 은 중앙 0.27 % · p90 10.2 % · 최대 56.8 % — 그만큼 φ 가 T 를 부풀린다 (f 는 무관).
- 최소안 (후속 · 미구현 · 미검증): SE 망 + AM–SE 접촉을 축전 sink 로 (ω → 0 극한 = 접촉 면적 비례 균일 sink) · AM 등전위 (σ_e ≫ σ_ion 가정 — 저 CAM 에서 깨짐, Minnmann τ_el² 120 @25 vol%) · 분리막 쪽 띠 Dirichlet · 집전체 쪽 차단 → 희소 솔브 1 회 → R_eff → R_ion = 3·R_eff (Nguyen Eq 5) → τ_e = ε·R_ion·A·σ₀/L.  sink 가중이 접촉 면적이므로 **LHS-25 가 먼저** 닫혀야 한다.  실험 앵커도 둘로 갈린다: Bazzoun (완전 차단 대칭셀 → eSCM 형) ↔ Minnmann (전자 차단 + 양단 Li-In → 관통형) [판독].

---

## §8. 더 볼 문헌 — 에이전트 제안 통합 (중복 제거 · ★ = 상위 5)

| 순위 | 서지 (카드 참고문헌 표의 원문 그대로) | 출처 카드 | 왜 |
|---|---|---|---|
| ★1 | Landesfeind, J., Ebner, M., Eldiven, A., Wood, V. & Gasteiger, H. A. Tortuosity of battery electrodes: validation of impedance-derived values and critical comparison with 3D tomography. J. Electrochem. Soc. 165, A469–A476 (2018). | nguyen ref 29 (= minnmann [61] · landesfeind §14) | 같은 전극의 임피던스 τ ↔ 영상 τ — 정의 · 방법 차이의 실측 크기 (§1 τ_e 행 · §7) |
| ★2 | [13] Holzer L, Wiedenmann D, Münch B, et al. The influence of constrictivity on the effective transport properties of porous layers in electrolysis and fuel cells. J Mater Sci. 2013;48(7):2934–2952. | tjaden [13] (= landesfeind [6]) | τ_eff ↔ τ_geo 엄격 구분 + 협착 β — FULL / CF / 기하 분해의 문헌 틀 (§3-4) |
| ★3 | H. F. Fischmeister, E. Arzt and L. R. Olsson, Powder Metall. 21, 179 (1978). | arzt [3] | impingement 구간 (D ≈ 0.97 까지) 압분 배위수 · 접촉면적 **실측** — [8] "H. F. Fischmeister and E. Arzt, Powder Metall. To be published." (출판 서지 [미확인] — 찾으면 1순위) 의 가장 가까운 대체 · β_SE · 판정선 근거 (§6) |
| ★4 | [12] a) J. Park, D. Kim, W. A. Appiah, J. Song, K. T. Bae, K. T. Lee, J. Oh, J. Y. Kim, Y.-G. Lee, M.-H. Ryou, Y. M. Lee, Energy Storage Mater. 2019, 19, 124; b) J. Park, J. Y. Kim, D. O. Shin, J. Oh, J. Kim, M. J. Lee, Y.-G. Lee, M.-H. Ryou, Y. M. Lee, Chem. Eng. J. 2020, 391, 123528. | park [12] | Park Fig S9 식의 인용원 — ASSB 디지털트윈 τ 의 산출법 · 값 (§3-3 의 역산을 원값으로) |
| ★5 | [43] D. Hlushkou, A. E. Reising, N. Kaiser, S. Spannenberger, S. Schlabach, Y. Kato, B. Roling, and U. Tallarek, J. Power Sources, 396, 363 (2018). | minnmann [43] | Minnmann 이 ASSB tortuosity · 기공 13–17 % 비교 문헌으로 인용 — 미세구조 기반 ASSB τ 의 두 번째 앵커 후보 (내용 [미확인]) |
| 2 | [14] Wiedenmann D, Keller L, Holzer L, et al. Three-dimensional pore structure and ion conductivity of porous ceramic diaphragms. AIChE J. 2013;59(5):1446–1457. | tjaden [14] (= landesfeind [10]) | Landesfeind Eq 4 (N_M ≡ τ̄_geo/(εβ)) 원식 — τ_geo 지수 [미확인] 닫기 |
| 2 | Malifarge, S., Delobel, B. & Delacourt, C. Determination of tortuosity using impedance spectra analysis of symmetric cell. J. Electrochem. Soc. 164, E3329–E3334 (2017). | nguyen ref 18 | 전자 저항 임의값 대칭셀 TLM — ASSB τ_e (r_el ≪ r_ion 이 안 설 때) |
| 2 | Pouraghajan, F. et al. Quantifying tortuosity of porous Li-ion battery electrodes: comparing polarization-interrupt and blocking-electrolyte methods. J. Electrochem. Soc. 165, 2644–2653 (2018). | nguyen ref 20 | eRDM vs eSCM 실측 + 접촉저항 넣은 일반 TLM |
| 2 | [25] N. Kaiser, S. Spannenberger, M. Schmitt, M. Cronau, Y. Kato, and B. Roling, J. Power Sources, 396, 175 (2018). | minnmann [25] | 임피던스 → ASSB 유효 이온전도도 · tortuosity 선행 |
| 2 | c) L. Froboese, J. F. v. d. Sichel, T. Loellhoeffel, L. Helmers, A. Kwade, J. Electrochem. Soc. 2019, 166, A318 | park [18c] | Park 의 조성 의존 LPSCl σ₀ 식 출처 — Park 비교의 순환 여부 |
| 2 | [32] Z. Siroma, N. Fujiwara, S. Yamazaki, M. Asahi, T. Nagai, and T. Ioroi, Electrochim. Acta, 160, 313 (2015). | minnmann [32] | Minnmann TLM 식 [1] 원전 |
| 2 | [63] Cooper SJ, Eastwood DS, Gelb J, et al. Image based modelling of microstructural heterogeneity in LiFePO4 electrodes for Li-ion batteries. J Power Sour. 2014;247:1033–1039. | tjaden [63] (= landesfeind [12]) | 같은 시료 κ_geo vs κ_flux (식 21–22) |
| 2 | Cooper, S. J., Bertei, A., Finegan, D. P. & Brandon, N. P. Simulated impedance of diffusion in porous media. Electrochim. Acta 251, 681–689 (2017). | nguyen ref 42 | 망 임피던스 (τ_e) 구현 참고 |
| 3 | [11] Epstein N. On tortuosity and the tortuosity factor in flow and diffusion through porous media. Chem Eng Sci. 1989;44(3):777–779. | tjaden [11] | κ = τ² 명명 원전 |
| 3 | [33] Y. Kato, S. Shiotani, K. Morita, K. Suzuki, M. Hirayama, and R. Kanno, The journal of physical chemistry letters, 9, 607 (2018). | minnmann [33] | EIS 와 독립인 사이클 기반 τ |
| 3 | [18] I. V. Thorat, D. E. Stephenson, N. A. Zacharias, K. Zaghib, J. N. Harb, and D. R. Wheeler, J. Power Sources, 188, 592 (2009). | landesfeind [18] (= tjaden [47] · nguyen ref 16) | eRDM 원조 · α 관례 |
| 3 | [34] M. Ender, J. Joos, T. Carraro, and E. Ivers-Tiffee, J. Electrochem. Soc., 159, A972 (2012). | landesfeind [34] | 복셀 Laplace N_M (STEP3 와 같은 계열) |
| 3 | [61] Stephenson DE, Hartman EM, Harb JN, et al. Modeling of particle-particle interactions in porous cathodes for lithium-ion batteries. J Electrochem Soc. 2007;154(12):A1146. | tjaden [61] | 리뷰 목록에서 접촉망에 가장 가까운 모형 |
| 3 | O. Molerus, Powder Technol. 12, 259 (1975). | arzt [14] | 힘 ↔ 외부압 f = 4πp/(ZD) — §6-2 평균장 원전 |
| 3 | A. K. Kakar and A. C. D. Chaklader, J. appl. Phys. 38, 3223 (1967). · P. J. James, Powder Metall. 20, 199 (1977). | arzt [18] · [19] | 압분 접촉면적 실측 |
| 3 | Morasch, R., Landesfeind, J., Suthar, B. & Gasteiger, H. A. Detection of binder gradients using impedance spectroscopy and their influence on the tortuosity of Li-ion battery graphite electrodes. J. Electrochem. Soc. 165, A3459 (2018). | nguyen ref 33 | 구배 전극 방향 의존 τ — graded-z |
| — | 낮음 · 서지는 카드 표 참조: Usseglio-Viretta 2018 (nguyen ref 28) · Lu 2020 (ref 34) · Zahn 2017 (ref 12) · Clennell 1997 · Djian 2007 · Ebner 2014 (landesfeind [13] [14] [32]) · van Brakel & Heertjes 1974 · Chung 2013 · Zhang 2015 · Tjaden 2016 (tjaden [12] [56] [64] [27]) · Ross 1982 · Arzt, Ashby & Easterling (미출판 [미확인]) · Fischmeister & Arzt [8] (미출판 [미확인]) (arzt [2] [15] [8]) · Ito 2017 · Nam 2018 · Jung 2019 · Neumann 2020 · Danner 2016 (park [11] [15d] [18b] [14] [19c]) · Asano 2017 (minnmann [27]) | | |

- 목록 밖 (출처 탐색 자체가 필요): 프레임 [1] "순수 SE ≈ 10 % @ 300 MPa" 의 실제 출처 — 에이전트 제안 0 건 [미확인] (`TAU-10`).  COMSOL 배터리 인터페이스 식은 문헌이 아니라 GUI Equation 보기로 닫는다 (§1).
