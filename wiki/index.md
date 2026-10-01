# 위키 색인

> 내용 목록. 모든 위키 페이지를 종류별로 한 줄 요약과 함께 싣는다. 논문 digest(`raw/papers/`)는
> 컴파일 페이지가 아니므로 여기 세지 않고 아래 "Raw 논문" 절에 참고로만 적는다.
> 마지막 갱신: 2026-10-01 | 전체 페이지: 16 | Total pages: 16

## Entities (satellite 프로젝트)

- [[li2s-assb-reference-cell]] — pristine Li2S · LPSCl · AB = 30:50:20 + Li–In 으로 문헌 수준 500–600 mAh g⁻¹(기준 미확인) 을 재현하는 1단계 프로젝트 (2026-09-11 등록).
- [[anode-free-li2s-assb]] — reference cell 이후 Li–In 을 빼는 2단계 프로젝트 (계획). Li 재고 = 양극 활성화량, Li 침적 균일성이 관건.

## Concepts (개념)

- [[li2s-assb-composite-cathode]] — 30:50:20 복합양극의 삼상 퍼콜레이션 논리, 액체계 75:25 와의 차이, 전압창 제약(미검증 배경).
- [[li2s-activation-first-charge]] — 첫 충전에서 활성화한 만큼만 이후 용량이 된다(Kim 2023 Fig. S1), 3.2 V 단조 plateau 와 직접 전환, 활성화 변수표.
- [[carbon-dimensionality-electron-network]] — 2D 접촉 탄소 vs 1D 네트워크 탄소의 분업 (Kim 2023 Gr/CNT), CNT 소량 최적, AB 단일 조성에의 함의.
- [[capacity-normalization-li2s-vs-sulfur]] — 1675 (S) ↔ 1166 (Li2S), 환산 0.698, Kim 2023 수치 양단위 표, 우리 목표 단위 문제, 표기 규율.
- [[mixing-equipment-ball-mill-thinky]] — ball mill · planetary · Thinky ARE-310 의 성격과 혼합 조건 기록 양식.

## Comparisons (비교)

- [[composite-cathode-mixing-routes]] — one-step BM · two-step · Li2SO4–PVP 탄화 · 에탄올 용액 · Kim 2023 선례를 제어 변수/미세구조/위험/장비로 비교.

## Guides (절차)

- [[new-project-kickoff]] — 새 실험 프로젝트를 satellite 로 등록하는 킥오프 프롬프트 (repo-root 상대 경로판).
- [[paper-ingest-mode]] — 논문 수치·정의를 verbatim atom 으로 분해하는 opt-in 모드 (기본은 /paper 전문 digest).
- [[seminar-prep-from-digest]] — digest 하나를 논문 세미나 발표로 옮기는 표준 절차 (/seminar).
- [[wsl-li2s-setup]] — WSL(Ubuntu) 에서 `li2s` 한 단어로 대시보드를 열기까지, PDF 넣기, /chat 키.

## Questions (열린 질문)

- [[reference-cell-500-600-mahg]] — (status: active) 병목은 활성화 / 퍼콜레이션 / 입자 / 단위 착시 중 무엇인가.
- [[one-step-vs-two-step-mixing]] — (status: open) 혼합 순서가 Li2S 이용률을 바꾸는가, 바꾼다면 SE 보호 때문인가 계면 때문인가.

## Syntheses (종합)

- [[interface-quality-not-bulk-conductivity]] — 고체 복합양극의 병목은 벌크 전도도가 아니라 **계면의 질**이다. ASSB 네 편이 전자 전도도를 **정반대 방향으로** 움직이며 비슷한 개선을 냈다는 관측에서 나온 논지. 반론 7개 보존 (2026-10-01).

## Queries (질의·발표 기록)

- [[kim2023-seminar-prep]] — Kim 2023 논문 세미나: 한 줄 메시지 · 5막 · 16장 슬라이드 설계 · 양단위 숫자표 · 비판 · 예상 질문 10.
  - 산출물: `queries/kim2023-seminar-draft.pptx` — 위 설계(16장)를 표지·마무리 포함 **18장** 덱으로.
    ⚠ 렌더러 없는 환경에서 만들어 **시각 QA 가 휴리스틱뿐**이다 (`log.md` 2026-09-11) — 한 번 열어 볼 것.

## Raw 논문 (참고 — 색인 카운트에 포함하지 않음)

이 절은 `raw/papers/` 의 digest 목록이다. **액체계/고체계**를 갈라 적는다 — 옮길 수 있는 것과
없는 것이 여기서 갈리기 때문이다 (단위·전압창·passivation 화학).

**액체 전해질 계**
- `raw/papers/kim2023_reinforced-electrical-networking-high-loading-li2s-cathode.md` — Kim et al., *Carbon Energy* 5 (2023) e308. Li2S/Gr/CNT compact 양극(75:25, 1 GPa), 흑연 full cell 800 사이클, 첫 충전 직접 전환(LiPs 없음). 그림 19장 (본문 8 + SI 11).

**전고체 계 (ASSB)** — 수집 순서가 아니라 발행 연도 순으로 적는다.
- `raw/papers/wan2021_lii-libr-catalyst-solid-state-li2s-s-reactions.md` — Wan et al., *Nano Lett.* 21 (2021) 8488. 활물질은 MoS2 지만 Fig. 2 의 곁가지가 **Li2S@LiI–LiBr vs 무첨가 Li2S 직접 대조**다 — 첨가제가 있으면 첫 충전이 **2.80 V 평탄 plateau**, 없으면 plateau 없이 3.5 V 까지 끌려간다. 무게 대가 39.9 wt%. 그림 5장.
- `raw/papers/wang2023_high-capacity-assb-li-s-low-density-solid-electrolyte.md` — Wang et al., *Nat. Commun.* 14 (2023) 1895. **S8** 60 wt% + 저밀도 Li3PS4–2LiBH4 SE(1.491 g cm⁻³)로 SE 부피분율을 35.4 vol% 까지. 1144.6 mAh g⁻¹(S)·800 사이클. 우리 30:50:20 은 이미 SE 48–52 vol%[재현]라 이 논문의 병목에 해당하지 않는다. 그림 4장.
- `raw/papers/yu2024_nanocrystallite-cus-n-doped-carbon-host-all-solid-state-li2s.md` — Yu et al., *Adv. Energy Mater.* 14 (2024) 2400845. CuS(29 wt%)/N-도핑 탄소 호스트 + nano-Li2S. 첫 충전 이용률 51 → 91 %, 10 mg cm⁻² 에서 9.6 mAh cm⁻². **전자 전도도를 200배 낮추고도 개선됐다**는 것이 축. 그림 7장.
- `raw/papers/kim2025_high-areal-capacity-sulfur-cathode-dual-phase-electrolyte-assb.md` — Kim et al., *Adv. Energy Mater.* 15 (2025) 2500867. LPSCl 을 쪼개 30 wt% 만 600 rpm 6 h 밀링하는 **two-step**. 12 mg(S) cm⁻² 에서 10.1 mAh cm⁻²·150 사이클 92 %. **one-step 과의 승패가 3–6 mg cm⁻² 에서 교차**한다는 것이 진짜 발견. kim2023 과 같은 1저자. 그림 5장.
- `raw/papers/qu2025_volume-changes-li-s-solid-state-battery-components-cycling.md` — Qu et al., *Nano Energy* 138 (2025) 110887. 정압(LVDT)·정용적 fixture 로 **수직 변위와 스택 압력을 실시간 측정**. 운전 7 MPa, 첫 몇 사이클에 14–20 µm 수축, Li2S 첫 충전 한 번에 그 절반. 그림 8장.
- `raw/papers/wangd2025_overcoming-conversion-limitation-tpb-mixed-conductors.md` — Wang (Daiwei) et al., *Nat. Mater.* **24** (2025) 243. **S8** 양극의 SE 를 통째로 **혼합이온–전자전도체**(비정질 Li–Ti–P–S)로 바꿔 **삼상 계면 의존 자체를 없앤다** — σ_Li⁺ 를 60 °C 에서 10 % 안으로 고정한 채 σ_e 만 5,203배 올려 첫 방전 838.6 → 1,281.6 mAh g⁻¹(S). ★ 가져갈 것 둘: **시클로헥산–UV–vis 추출로 "죽은 황" 을 질량으로 재는 법**(전기화학과 독립, n=4)과 **시료 정체가 명시된 DC 분극 프로토콜**. 제1저자가 위 wang2023 과 동일인이고 자기 2023 작업을 스스로 비판한다. ⚠ wang2023(Daiwei Wang)·wang2026(Yanjie Wang)과 구분할 것. 그림 5장.
- `raw/papers/cronk2026_highly-utilized-practical-li-s-positive-electrode-assb.md` — Cronk et al., *Nat. Commun.* 17 (2026) 3298. **우리와 같은 30:50:20** 을 one-step 고에너지 밀링(500 rpm 1 h, BPR 1:30)으로. 황 표면 Li3PS4+n interphase + **LPSCl 산화환원까지 용량으로** 쓴다. 11 mAh cm⁻²·25 °C·500 사이클, Li2S 반쪽셀 723 mAh g⁻¹(Li2S). 그림 7장.
- `raw/papers/huang2026_high-entropy-sulfides-kinetic-accelerators-assb.md` — Huang et al., *J. Energy Chem.* 118 (2026) 352. **S8** 양극 + 고엔트로피 황화물 6 wt%. LPSCl·Li–In·상온. 탄소만일 때 S 이용률 39 % → 첨가제로 76 %. DC 분극으로 복합체 σ_e⁻·σ_Li⁺ 분리 측정. 그림 24장 (본문 5 + SI 19).
- `raw/papers/jeong2026_reconciling-triple-phase-boundaries-tortuosity-assb.md` — Jeong et al., *Joule* 10 (2026) 102541. 탄소 호스트의 **입자 크기(전극 스케일 수송)와 기공 크기(입자 스케일 TPB)를 분리**. 전자 전도도가 6배 낮은 마이크론·마이크로포어 호스트가 율속·수명에서 이긴다. 탄소 21 wt% 복합양극 σ_e 0.015–0.108 S cm⁻¹ 는 우리 AB 20 wt% 의 첫 외부 눈금. 그림 7장.
- `raw/papers/lee2026_decoupled-sulfur-redox-pathways-initial-chemical-states-assb.md` — Lee et al., *Chem. Eng. J.* 546 (2026) 179625. 같은 셀에서 **출발 활물질만 S8 ↔ Li2S** 로 바꾸면 경로가 갈린다. 양극 비율 30:20:50 이 우리와 같으나 보고 용량이 Li2S 이론용량을 넘는다(단위 주의). 그림 6장.
- `raw/papers/liu2026_li4sns4-molecular-mediator-low-barrier-li2s-chemistry.md` — Liu et al., *Adv. Funct. Mater.* 2026, e77927. 상용 Li2S + SnS2 를 **6 h 소결**해 ≈30 nm Li4SnS4 껍질을 in-situ 로 기른다 — 밀링이 아닌 **고상 소결 코팅**. 첫 충전 개시 전위 2.94 → **2.41 V**, 첫 방전 846 mAh g⁻¹(Li2S). ★ 제목의 "mediator" 는 같은 논문의 **Sn 3d 불변**이 반증한다(정적 계면층). Li4SnS4 함량 미기재. 그림 5장.
- `raw/papers/wang2026_molecular-coordination-triple-synergy-cathode-assb.md` — Wang Yanjie et al., *Energy Storage Mater.* 91 (2026) 105492. LGPS 기반 S8/C 양극 + 유기 소분자 DABDT. 황 이용률 48.5 → 97.04 % 주장. **Experimental 절이 통째로 없고** 전도도 실측 0회, Li⁺ 확산 주장이 자기 EIS/DRT 와 10¹⁰ 배 어긋난다. 그림 5장.
- `raw/papers/zhang2026_anode-free-assb-nanocrystalline-amorphous-li2s-na-collector.md` — Zhang et al., *Adv. Energy Mater.* (2026). **anode-free** + 반응형 나노결정–비정질 Li2S + **Na 집전체**, 운전 스택압 0/1/4 MPa. pristine Li2S 첫 방전 ≈270 vs 처리 971 mAh g⁻¹(Li2S). 그림 21장 (본문 6 + SI 15).
- `raw/papers/zhangj2026_strain-coordination-long-cycling-assb.md` — Zhang (Jiaxu) et al., *Nat. Commun.* 17 (2026) 7858. ⚠ **위 zhang2026(산둥대 Qi Zhang)과 다른 Zhang 이다.** 활물질이 **FeS2**(Li2S 는 방전 생성물)라 Li2S 양극 논문이 아니고 **전략 논문**이다 — FeS2 의 팽창과 prelithiated Si 의 수축을 **부호로 상쇄**해 셀 몰부피 변화 −17.2 → +2.6 %, **15 MPa 저압 운전**. 우리에게 값있는 것은 **LTO zero-strain 기준자 · 용량당 응력 σc · 압력별 EIS 스윕** 세 도구다 (H5 기계적 제한). 그림 7장.
