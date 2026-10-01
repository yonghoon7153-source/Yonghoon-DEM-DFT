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

**전고체 계 (ASSB)**
- `raw/papers/huang2026_high-entropy-sulfides-kinetic-accelerators-assb.md` — Huang et al., *J. Energy Chem.* 118 (2026) 352. **S8** 양극 + 고엔트로피 황화물 6 wt%. LPSCl·Li–In·상온. 탄소만일 때 S 이용률 39 % → 첨가제로 76 %. DC 분극으로 복합체 σ_e⁻·σ_Li⁺ 분리 측정. 그림 24장 (본문 5 + SI 19).
- `raw/papers/zhang2026_anode-free-assb-nanocrystalline-amorphous-li2s-na-collector.md` — Zhang et al., *Adv. Energy Mater.* (2026). **anode-free** + 반응형 나노결정–비정질 Li2S + **Na 집전체**, 운전 스택압 0/1/4 MPa. pristine Li2S 첫 방전 ≈270 vs 처리 971 mAh g⁻¹(Li2S). 그림 21장 (본문 6 + SI 15, 21/21 판독).
