# 위키 색인

> 내용 목록. 모든 위키 페이지를 종류별로 한 줄 요약과 함께 싣는다. 논문 digest(`raw/papers/`)는
> 컴파일 페이지가 아니므로 여기 세지 않고 아래 "Raw 논문" 절에 참고로만 적는다.
> 마지막 갱신: 2026-10-02 | 전체 페이지: 20 | Total pages: 20

## Entities (satellite 프로젝트)

- [[li2s-assb-reference-cell]] — pristine Li2S · LPSCl · AB = 30:50:20 + Li–In 으로 문헌 수준 500–600 mAh g⁻¹(기준 미확인) 을 재현하는 1단계 프로젝트 (2026-09-11 등록).
- [[anode-free-li2s-assb]] — reference cell 이후 Li–In 을 빼는 2단계 프로젝트 (계획). Li 재고 = 양극 활성화량, Li 침적 균일성이 관건.

## Concepts (개념)

- [[li2s-assb-composite-cathode]] — 30:50:20 복합양극의 삼상 퍼콜레이션 논리, 액체계 75:25 와의 차이, 전압창 제약(미검증 배경).
- [[li2s-activation-first-charge]] — 첫 충전에서 활성화한 만큼만 이후 용량이 된다(Kim 2023 Fig. S1), 3.2 V 단조 plateau 와 직접 전환, 활성화 변수표.
- [[carbon-dimensionality-electron-network]] — 2D 접촉 탄소 vs 1D 네트워크 탄소의 분업 (Kim 2023 Gr/CNT), CNT 소량 최적, AB 단일 조성에의 함의.
- [[capacity-normalization-li2s-vs-sulfur]] — **1672 (S) ↔ 1166 (Li2S)**, 환산 0.6978 (2026-10-06 에 "1675" 의 자기모순을 정정). **1전자 천장 583 / 2전자 1166** 두 줄 병기 규율, 황 분광 전 SE 유래 황 분율(우리 셀 58.8 %) 계산 규율.
- [[dc-polarization-conductivity-separation]] — 복합양극의 σ_e⁻ 와 σ_Li⁺ 를 따로 재는 방법. 원전(Kwok 2023) 레시피 · digest 5편이 같은 레시피를 어떻게 다르게 썼나 · **우리가 쓸 프로토콜 확정**(인가 전압 20–50 mV, 계보를 타고 1 V 까지 커진 것이 가장 위험하다).
- [[mixing-equipment-ball-mill-thinky]] — ball mill · planetary · Thinky ARE-310 의 성격과 혼합 조건 기록 양식.

## Comparisons (비교)

- [[composite-cathode-mixing-routes]] — one-step BM · two-step · Li2SO4–PVP 탄화 · 에탄올 용액 · Kim 2023 선례를 제어 변수/미세구조/위험/장비로 비교.

## Guides (절차)

- [[new-project-kickoff]] — 새 실험 프로젝트를 satellite 로 등록하는 킥오프 프롬프트 (repo-root 상대 경로판).
- [[paper-ingest-mode]] — 논문 수치·정의를 verbatim atom 으로 분해하는 opt-in 모드 (기본은 /paper 전문 digest).
- [[seminar-prep-from-digest]] — digest 하나를 논문 세미나 발표로 옮기는 표준 절차 (/seminar).
- [[reference-cell-experiment-plan]] — **실행 계획 한 장.** digest 23편이 정한 순서(0 분모 확정 → 1 압력·온도 2×2 → 2 DC 분극 세 칸 → 3 컷오프 상·하한 → 4 집전체 n=3)와 각 단계의 판정 기준 · 기록 체크리스트 · 숫자 표기 규율 7개.
- [[wsl-li2s-setup]] — WSL(Ubuntu) 에서 `li2s` 한 단어로 대시보드를 열기까지, PDF 넣기, /chat 키.

## Questions (열린 질문)

- [[reference-cell-500-600-mahg]] — (status: active) 병목은 활성화 / 퍼콜레이션 / 입자 / 단위 착시 중 무엇인가.
- [[operating-stack-pressure-floor]] — (status: open) 운전 압력 하한은 얼마이고, 그것을 정하는 것은 **양극 내부인가 집전체 계면인가**. 문헌 좌표 **0–200 MPa**, 저압은 공짜가 아니며 포화 압력은 전극계마다 5–15 MPa 로 움직인다.
- [[one-step-vs-two-step-mixing]] — (status: open) 혼합 순서가 Li2S 이용률을 바꾸는가, 바꾼다면 SE 보호 때문인가 계면 때문인가.

## Syntheses (종합)

- [[interface-quality-not-bulk-conductivity]] — 고체 복합양극의 병목은 벌크 전도도가 아니라 **계면의 질**이다. ASSB 네 편이 전자 전도도를 **정반대 방향으로** 움직이며 비슷한 개선을 냈다는 관측에서 나온 논지. 반론 7개 보존 (2026-10-01).

## Queries (질의·발표 기록)

- [[kim2023-seminar-prep]] — Kim 2023 논문 세미나: 한 줄 메시지 · 5막 · 16장 슬라이드 설계 · 양단위 숫자표 · 비판 · 예상 질문 10.
  - 산출물: `queries/kim2023-seminar-draft.pptx` — 위 설계(16장)를 표지·마무리 포함 **18장** 덱으로.
    ⚠ 렌더러 없는 환경에서 만들어 **시각 QA 가 휴리스틱뿐**이다 (`log.md` 2026-09-11) — 한 번 열어 볼 것.
- [[kimjt2023-seminar-prep]] — **Kim JT 2023**(*Nat. Commun.*, Li2S2/Li2S 혼합 생성물) 세미나: 한 줄 메시지 · 5막 · **16장** 슬라이드(★ 8장 = 15분 판) · 양단위 숫자표 · 비판 3+3 · 예상 질문 10. 중심은 **간판 셀이 1전자 천장을 79 % 넘는다**는 것과, 가져갈 것은 주장이 아니라 **583 mAh g⁻¹(Li2S) 라는 눈금**이라는 것.

## Raw 논문 (참고 — 색인 카운트에 포함하지 않음)

이 절은 `raw/papers/` 의 digest 목록이다. **액체계/고체계**를 갈라 적는다 — 옮길 수 있는 것과
없는 것이 여기서 갈리기 때문이다 (단위·전압창·passivation 화학).

**액체 전해질 계**
- `raw/papers/kim2023_reinforced-electrical-networking-high-loading-li2s-cathode.md` — Kim et al., *Carbon Energy* 5 (2023) e308. Li2S/Gr/CNT compact 양극(75:25, 1 GPa), 흑연 full cell 800 사이클, 첫 충전 직접 전환(LiPs 없음). 그림 19장 (본문 8 + SI 11).

**전고체 계 (ASSB)** — 수집 순서가 아니라 발행 연도 순으로 적는다.
- `raw/papers/wan2021_lii-libr-catalyst-solid-state-li2s-s-reactions.md` — Wan et al., *Nano Lett.* 21 (2021) 8488. 활물질은 MoS2 지만 Fig. 2 의 곁가지가 **Li2S@LiI–LiBr vs 무첨가 Li2S 직접 대조**다 — 첨가제가 있으면 첫 충전이 **2.80 V 평탄 plateau**, 없으면 plateau 없이 3.5 V 까지 끌려간다. 무게 대가 39.9 wt%. 그림 5장.
- `raw/papers/wang2023_high-capacity-assb-li-s-low-density-solid-electrolyte.md` — Wang et al., *Nat. Commun.* 14 (2023) 1895. **S8** 60 wt% + 저밀도 Li3PS4–2LiBH4 SE(1.491 g cm⁻³)로 SE 부피분율을 35.4 vol% 까지. 1144.6 mAh g⁻¹(S)·800 사이클. 우리 30:50:20 은 이미 SE 48–52 vol%[재현]라 이 논문의 병목에 해당하지 않는다. 그림 4장.
- `raw/papers/kimjt2023_mixed-discharge-products-li2s2-li2s-asslsb.md` — Kim (**Jung Tae**) et al., *Nat. Commun.* **14** (2023) 6404 (UWO, 교신 Xueliang Sun). ⚠ **위 kim2023(한양대)·kim2025 와 다른 Kim 이다.** ASSLSB 의 방전 생성물이 **Li2S 단독이 아니라 Li2S + Li2S2 혼합**이라는 주장 — S K-edge XANES 2471.3 eV 어깨 + ToF-SIMS Li3S2⁺/Li3S⁺. 하한 컷오프를 0.6 V vs Li–In 에 묶고 LiI 6 wt% 로 1500 사이클. ★ 우리가 가져간 것은 주장이 아니라 **1전자 천장 583 mAh g⁻¹(Li2S)** 라는 눈금과 **"황 분광 전에 SE 유래 황 분율을 계산하라"** 는 규율이다 ([[capacity-normalization-li2s-vs-sulfur]]). ⚠ 활물질은 **S8** 이고 Li2S 셀이 없다. 운전 구속압 150 MPa. 그림 4장.
- `raw/papers/yu2024_nanocrystallite-cus-n-doped-carbon-host-all-solid-state-li2s.md` — Yu et al., *Adv. Energy Mater.* 14 (2024) 2400845. CuS(29 wt%)/N-도핑 탄소 호스트 + nano-Li2S. 첫 충전 이용률 51 → 91 %, 10 mg cm⁻² 에서 9.6 mAh cm⁻². **전자 전도도를 200배 낮추고도 개선됐다**는 것이 축. 그림 7장.
- `raw/papers/kwok2023_interfacial-redox-mediator-high-performance-asslsb.md` — Kwok, Xu, Kochetkov, Zhou, **Nazar**, *Energy Environ. Sci.* **16** (2023) 610. ★ **이 위키 DC 분극 전도도 분리의 원전** ([[dc-polarization-conductivity-separation]]) — Huang 2026 이 셀 구성의 출처로 인용하고 면적 0.785 cm² 가 그대로 전해졌다. 내용: Li2S 나노입방체(~60 nm)를 **<30 nm LiVS2 껍질**로 감싼 core–shell 을 **탄소 0 wt%** 로 Li2S:LiVS2:LPSCl = **30:20:50 wt%** 만으로 돌려 상온 1 mA cm⁻² **1,000 사이클**. 이용률 77 %(Li2S 기준) vs 탄소 대조군 30 %. ⚠ **혼합·성형압·운전압이 본문에 한 글자도 없다**(Methods 전량 ESI, 미확보). 그림 7장 + 표 2장.
- `raw/papers/kim2025_high-areal-capacity-sulfur-cathode-dual-phase-electrolyte-assb.md` — Kim et al., *Adv. Energy Mater.* 15 (2025) 2500867. LPSCl 을 쪼개 30 wt% 만 600 rpm 6 h 밀링하는 **two-step**. 12 mg(S) cm⁻² 에서 10.1 mAh cm⁻²·150 사이클 92 %. **one-step 과의 승패가 3–6 mg cm⁻² 에서 교차**한다는 것이 진짜 발견. kim2023 과 같은 1저자. 그림 5장.
- `raw/papers/hao2025_nanosized-li2s-amorphous-matrix-asslsb.md` — **Xiaoge Hao** et al., *JACS* **147** (2025) 42184 (EIT 닝보 + UWO, 교신 Changhong Wang·Xueliang Sun — `kimjt2023`·`zhangj2026` 와 같은 그룹). 상용 Li2S + **FeCl3 15 wt%** 를 함께 밀링해 **밀링 중 고상 치환반응**으로 ≈4 nm Li2S + **비정질 LiFeS2** 를 동시에 만든다 — ★ 이 위키의 **여섯째 제작 경로("반응성 밀링")**. 고로딩 **19.1 mg cm⁻²(Li2S) 에서 13.2 mAh cm⁻²**. ★ **첨가제 기여를 Fe K-edge XAS 로 실제로 배제한 드문 논문**(4상태 전부 불변, `[재현]` 자기 용량 4.6 %). ⚠ 그러나 **대조군이 같은 밀링을 겪었는지 본문에 없고**(FFT 가 안 겪었음을 시사) 그 대조군 첫 방전이 `[도표]` **≈10 mAh g⁻¹(Li2S)** — CV 에 피크가 **아예 없다**. 그리고 "활물질 함량 48 %" 는 `[재현]` **mol% 를 wt% 로 쓴 값**이다(실제 45.9 또는 41.0 %). Methods 가 전량 SI 이고 **본문에 `MPa`·`°C`·`rpm` 이 한 번도 없다**. 그림 5장.
- `raw/papers/park2026_low-pressure-operation-carbon-coated-current-collector-asslsb.md` — Park et al., **Ying Shirley Meng** 그룹 + LG ES, *Adv. Energy Mater.* **16** (2026) e04272. ★ **우리와 같은 30:50:20 · LPSCl · AB · Li–In** 을 bare / graphite / carbon black 코팅 Al 집전체에 라미네이트해 운전 스택압을 **75 → 1 MPa 로 7단계 스캔**했다. CB 코팅박은 **10 MPa 상온 350사이클 78 %**, bare Al 은 같은 조건에서 **10사이클에 붕괴**. ★ **집전체 표면만 바꿨다** — H5 의 가장 깨끗한 근거. ⚠ 간판 수치 셋이 원문 안에서 성립하지 않아 **인용 금지**(단위 섞은 65.5→21.0 Ω · "5–10배"는 실제 2.4–3.9배 · "1 C 에서 96 %"는 C/10 복귀값). 혼합은 **two-step**(Cronk one-step 과 짝). 그림 7장.
- `raw/papers/gao2024_cu-i-codoping-activating-li2s-redox-kinetics-assb.md` — Gao et al., *Small* **20** (2024) 2404171. Li2S + **CuI** 를 510 rpm 20 h 공밀링(BPR 20:1)해 Cu⁺/I⁻ 를 넣고 LPSCl·VGCF·Li–In·**운전 50 MPa** 로 돌렸다. 첫 방전 **174.6 → 1165.2 mAh g⁻¹(Li2S)**, 2 C 6,200 사이클. ★ **활성화 사다리의 현재 최저 plateau — 1.72–1.75 V vs Li–In = `[재현]` 2.34–2.37 V vs Li/Li⁺.** 같은 할로겐을 **LiI 가 아니라 CuI 로** 넣으면 요오드 경로의 2.8 V 벽이 깨진다 (같은 논문 안에 85Li2S–15LiI 대조셀이 있다). ⚠ "co-doping" 의 격자 치환 증거는 본문에 없다 (격자상수 미인쇄, Li 공공은 Cu Kα XRD 로 결정 불가). 그림 6장 + 표 1장.
- `raw/papers/qu2025_volume-changes-li-s-solid-state-battery-components-cycling.md` — Qu et al., *Nano Energy* 138 (2025) 110887. 정압(LVDT)·정용적 fixture 로 **수직 변위와 스택 압력을 실시간 측정**. 운전 7 MPa, 첫 몇 사이클에 14–20 µm 수축, Li2S 첫 충전 한 번에 그 절반. 그림 8장.
- `raw/papers/wangd2025_overcoming-conversion-limitation-tpb-mixed-conductors.md` — Wang (Daiwei) et al., *Nat. Mater.* **24** (2025) 243. **S8** 양극의 SE 를 통째로 **혼합이온–전자전도체**(비정질 Li–Ti–P–S)로 바꿔 **삼상 계면 의존 자체를 없앤다** — σ_Li⁺ 를 60 °C 에서 10 % 안으로 고정한 채 σ_e 만 5,203배 올려 첫 방전 838.6 → 1,281.6 mAh g⁻¹(S). ★ 가져갈 것 둘: **시클로헥산–UV–vis 추출로 "죽은 황" 을 질량으로 재는 법**(전기화학과 독립, n=4)과 **시료 정체가 명시된 DC 분극 프로토콜**. 제1저자가 위 wang2023 과 동일인이고 자기 2023 작업을 스스로 비판한다. ⚠ wang2023(Daiwei Wang)·wang2026(Yanjie Wang)과 구분할 것. 그림 5장.
- `raw/papers/wangx2026_dual-conductivity-optimization-high-rate-ultralong-life-asslsb.md` — **XinXu** Wang et al., *Adv. Mater.* **38** (2026) e22976. ⚠ **위 wang2023·wangd2025(둘 다 Daiwei Wang)·wang2026(Yanjie Wang)과 다른 Wang 이다.** 활물질이 **Li2Se0.2S0.8**(Se 를 황 자리에 치환한 고용체)라 ★ **이 위키 제3의 분모**를 들고 온다 — **환산 ×0.69783 을 적용하면 안 되고** 이론 천장이 1166.7 → **968.9 (−17.0 %)** 로 내려간다 ([[capacity-normalization-li2s-vs-sulfur]]). 첫 방전 370.9 → **720.9 mAh g⁻¹(활물질)**. ★ **제목의 "dual-conductivity" 중 전자 쪽은 비어 있다** — σ_e 를 올린 뒤에도 4.58×10⁻⁹ S cm⁻¹ 로 같은 시료 σ_Li⁺ 의 **1/1048** 이고, 그 ×2.03 은 `[재현]` 밴드갭 27 meV 의 진성 캐리어 효과 1.69 로 거의 전부 설명된다. ⚠ **Experimental 절이 통째로 없다**(SI 미확보) — rpm 조차 없다. 그림 5장.
- `raw/papers/feng2026_anode-free-asslsb-fe-stabilized-polysulfides.md` — Feng et al., *ACS Energy Lett.* (2026), UCSD + Brookhaven (교신 Ping Liu). 상용 Li2S + **FeCl3 10 mol%** 를 Ar 하에서 밀링해(반응성 밀링) 첫 충전 **861 mAh g⁻¹(FLS) = `[재현]` 1669 (S) = 이용률 99.8 %**, ICE **99 %**, 500사이클 80 %. ★ **이 위키 최초의 "촉매" 배정** — Fe 는 산화상태가 "slight" 하게 왕복·복귀하고 자기 용량이 `[재현]` 5 % 뿐이다. ⚠ **제목이 두 번 과장한다**: (a) "Anode-less" 인데 **조립 후 Li 박을 눌러 붙여 80 °C 8 h 프리리튬화**한다 — Li 금속 공정이 그대로 있다. (b) "Polysulfides" 인데 측정된 것은 **S–S 모티프**이고 Li2Sx 증거가 없다(저자 자신이 DFT 절에서 "polysulfide-**like**" 라 쓴다). ★★ **압력–온도 교환을 의식적으로 쓴 첫 사례** — "practical stack pressure 를 유지한 채 접촉을 확보하려고 60 °C 를 골랐다" 고 명시하고, 뒤에서 **상온이 장기적으로 낫다**고 자인한다. 운전 50 MPa. Methods 전량 SI 미확보. 그림 5장.
- `raw/papers/cronk2026_highly-utilized-practical-li-s-positive-electrode-assb.md` — Cronk et al., *Nat. Commun.* 17 (2026) 3298. **우리와 같은 30:50:20** 을 one-step 고에너지 밀링(500 rpm 1 h, BPR 1:30)으로. 황 표면 Li3PS4+n interphase + **LPSCl 산화환원까지 용량으로** 쓴다. 11 mAh cm⁻²·25 °C·500 사이클, Li2S 반쪽셀 723 mAh g⁻¹(Li2S). 그림 7장.
- `raw/papers/huang2026_high-entropy-sulfides-kinetic-accelerators-assb.md` — Huang et al., *J. Energy Chem.* 118 (2026) 352. **S8** 양극 + 고엔트로피 황화물 6 wt%. LPSCl·Li–In·상온. 탄소만일 때 S 이용률 39 % → 첨가제로 76 %. DC 분극으로 복합체 σ_e⁻·σ_Li⁺ 분리 측정. 그림 24장 (본문 5 + SI 19).
- `raw/papers/jeong2026_reconciling-triple-phase-boundaries-tortuosity-assb.md` — Jeong et al., *Joule* 10 (2026) 102541. 탄소 호스트의 **입자 크기(전극 스케일 수송)와 기공 크기(입자 스케일 TPB)를 분리**. 전자 전도도가 6배 낮은 마이크론·마이크로포어 호스트가 율속·수명에서 이긴다. 탄소 21 wt% 복합양극 σ_e 0.015–0.108 S cm⁻¹ 는 우리 AB 20 wt% 의 첫 외부 눈금. 그림 7장.
- `raw/papers/lee2026_decoupled-sulfur-redox-pathways-initial-chemical-states-assb.md` — Lee et al., *Chem. Eng. J.* 546 (2026) 179625. 같은 셀에서 **출발 활물질만 S8 ↔ Li2S** 로 바꾸면 경로가 갈린다. 양극 비율 30:20:50 이 우리와 같으나 보고 용량이 Li2S 이론용량을 넘는다(단위 주의). 그림 6장.
- `raw/papers/liu2026_li4sns4-molecular-mediator-low-barrier-li2s-chemistry.md` — Liu et al., *Adv. Funct. Mater.* 2026, e77927. 상용 Li2S + SnS2 를 **6 h 소결**해 ≈30 nm Li4SnS4 껍질을 in-situ 로 기른다 — 밀링이 아닌 **고상 소결 코팅**. 첫 충전 개시 전위 2.94 → **2.41 V**, 첫 방전 846 mAh g⁻¹(Li2S). ★ 제목의 "mediator" 는 같은 논문의 **Sn 3d 불변**이 반증한다(정적 계면층). Li4SnS4 함량 미기재. 그림 5장.
- `raw/papers/hong2026_high-valence-cation-lattice-expansion-activating-li2s.md` — Hong et al., *Adv. Mater.* **38** (2026) e72513. 상용 Li2S + **ZrS2** 를 550 rpm 6 h 공밀링해 Zr⁴⁺ 를 Li 자리에 치환(Rietveld 점유율 0.0144)했다는 **이 위키 최초의 "격자 치환형" 사례** — 무게 대가가 **16.7 wt%** 로 요오드·CuI 계 40–44 wt% 의 2/5 다. ★★ **같은 논문에서 입자 칸과 복합체 칸의 σ 를 동시에 쟀다** — 입자 σ_e > ×8500 인데 **복합체 σ_e 는 ×1.36** 로 KB 40 wt% 퍼콜레이션 고원에 묻힌다. ⚠ "격자 팽창" 은 부분 증명 — HRTEM +7.44 % 와 Rietveld 기준 +1.26 % 가 **6배 어긋나는데 본문은 "consistent"** 라 쓴다. 운전 구속압 **200 MPa**(이 위키 최고). 그림 5장.
- `raw/papers/wang2026_molecular-coordination-triple-synergy-cathode-assb.md` — Wang Yanjie et al., *Energy Storage Mater.* 91 (2026) 105492. LGPS 기반 S8/C 양극 + 유기 소분자 DABDT. 황 이용률 48.5 → 97.04 % 주장. **Experimental 절이 통째로 없고** 전도도 실측 0회, Li⁺ 확산 주장이 자기 EIS/DRT 와 10¹⁰ 배 어긋난다. 그림 5장.
- `raw/papers/zhang2026_anode-free-assb-nanocrystalline-amorphous-li2s-na-collector.md` — Zhang et al., *Adv. Energy Mater.* (2026). **anode-free** + 반응형 나노결정–비정질 Li2S + **Na 집전체**, 운전 스택압 0/1/4 MPa. pristine Li2S 첫 방전 ≈270 vs 처리 971 mAh g⁻¹(Li2S). 그림 21장 (본문 6 + SI 15).
- `raw/papers/zhangj2026_strain-coordination-long-cycling-assb.md` — Zhang (Jiaxu) et al., *Nat. Commun.* 17 (2026) 7858. ⚠ **위 zhang2026(산둥대 Qi Zhang)과 다른 Zhang 이다.** 활물질이 **FeS2**(Li2S 는 방전 생성물)라 Li2S 양극 논문이 아니고 **전략 논문**이다 — FeS2 의 팽창과 prelithiated Si 의 수축을 **부호로 상쇄**해 셀 몰부피 변화 −17.2 → +2.6 %, **15 MPa 저압 운전**. 우리에게 값있는 것은 **LTO zero-strain 기준자 · 용량당 응력 σc · 압력별 EIS 스윕** 세 도구다 (H5 기계적 제한). 그림 7장.
