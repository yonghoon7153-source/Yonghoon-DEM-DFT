---
title: "MLIP(UMA) 차기 캠페인 후보 제안서 — cascade 확장 7건"
tags: [project/mlip-next, uma, mlip-md, neb, interface, proposal]
date: 2026-07-27
status: proposal
---

# MLIP(UMA) 차기 캠페인 후보 제안서 (2026-07)

> 목적: cascade v23(91 화합물 × 273 cascade, UMA 스크리닝→DFT 승격)처럼 **UMA를 스크리닝 엔진으로 쓰는
> 차기 캠페인 후보 7건**을 정리한다. 사용자가 명시 요청한 **① Li 금속 계면 반응성**을 포함.
> 근거 소스: `db/properties/cascade_v23_themes.json`(테마 축·champion), `db/properties/interface_campaign_summary.csv`
> (기존 Li|SE 3-seed 캠페인), `db/properties/codoping_ml_v2_meta.json`(co-doping ML — hypothesis generator),
> litdb: choi2025(MLIP W_ad·SMD), kraft2017(total 0.46 vs bulk Ea), zhu2020·taklu2021(공기안정),
> shi2017/liu2022(hBN·계면층), bucci2017/2018(기계 계면 임계), 인프라: `tools/vgcf_hbn`(NEB)·`tools/ionic`·`tools/modelc_v3`(MD)·`tools/adhesion_v30u`(W_ad).

## 공통 규율 (모든 후보에 적용 — CLAUDE.md 승계)

- **UMA-s-1p1(omat)** = LPSCl 계열 MD의 검증 표준. **Li₃N 사용 금지**(2026-06 결정론적 편향 판정)는 그대로 유효.
- MD 표준: Langevin NVT, dt 2 fs, friction 0.02, equilib 5 ps / prod 200 ps, **MSD 창 2–50 ps 고정**,
  아레니우스 600/800/1000 K 3점, **σ·D 절대값 인용 금지 — 비율도 멀티시드 판정만**(단일시드 1.33× 철회 사례).
- 문헌값(Kraft 0.46 eV, Bucci G_c 4 J/m² 등)은 **소환 앵커** — 우리 값과 같은 표에 절대값으로 섞지 않는다.
- 신규 상/신규 화학이 나오는 순간 **DFT 스팟체크가 세트** — UMA 단독 수치는 스크리닝 단계까지만.
- gabia에서 pw.x와 UMA 동시 실행 금지(nvidia-smi 확인), 실행 스크립트 pgrep 가드 관례 유지.

---

## ① Li|SE(도핑) 계면 반응성 스크리닝 ★사용자 명시 요청

**물리 질문**: cascade/co-doping ML top 도펀트가 Li 금속 접촉에서 분해 깊이·SEI 조성을 실제로 바꾸나?
B₂O₃에서 본 "sacrificial shield"(termination scan: B-exposed가 host PS₄를 2.6× 보존) 같은 보호 기전이 다른 도펀트에도 있나?

**방법 (UMA 셋업)**: 기존 SE|Li 캠페인 프로토콜 승계 — 2x frame(124–128원자급) 도핑 SE 슬랩 | Li 금속 슬랩,
verified-carry 기하. Langevin NVT 300 K(+가속 판정용 600 K 1점), **3-seed × 100–200 ps**.
관측량은 기존 analyzer 그대로: PS₄ 보존율, 원소별 Li 침투 깊이, 도펀트 배위(B–S류) per-frame 추적.
대상 4–6계: reduction_anode 테마 top(CaO·HfO₂·CaF₂·LiF·ScF₃ 중) + co-doping ML top pair 1–2쌍 + undoped 대조.

**기존 자산**: `interface_campaign_summary.csv`·`interface_termination_scan.csv`의 프로토콜과 per-seed analyzer(kgy repo),
`anode_interface_b2o3.json`(열역학 짝 — 같은 도펀트의 MD vs grand-potential 대조), cascade v23 champion 도핑 셀.

**자원·기간**: kgy RTX3090(기존 캠페인 실적지) 또는 gabia. 시스템당 3-seed×100 ps는 기존 실적 기준 수일
→ 6계 전체 **약 2–3주**.

**리스크·UMA 유효성**: LPSCl 계열은 **N 무함유 → UMA Li₃N 금지조항 비저촉**(명시해 둔다). 단 계면 산물로
나오는 신규 상(Li₂S·Li₃P·LiCl·LiB·Li₂O·불화물 등)은 UMA 검증 범위 밖 → 대표 산물 2–3상 DFT single-point/EOS
스팟체크 필수. thin-slab artifact 재발 금지(modelc62 1x 슬랩이 같은 물질에서 PS_loss 1.9× — 2x frame 최소).
100 ps에서 분해가 self-limit 안 되므로 정량은 **같은 시간창 상대비교만**.

**co-doping ML 연결**: codoping_ml_v2는 현재 "HYPOTHESIS GENERATOR — NOT VALIDATED". 이 캠페인의 PS_loss·침투
깊이가 top pair의 **첫 실측 검증 라벨**이 된다.

**안 되면 알게 되는 것**: 도펀트가 계면 분해를 유의미하게 못 바꾸면 "bulk 도핑으로 음극 계면을 잡는다"는 축을
접고 코팅(⑦)으로 자원을 모을 근거가 생긴다.

---

## ② 입계(GB) 수송 — Σ tilt GB Ea vs bulk

**물리 질문**: LPSCl 다결정에서 GB가 수송 병목인가? 우리 bulk MD Ea(~0.25 eV급)와 문헌 total Ea의 간극
(kraft2017: 임피던스 total 0.46 eV, **bulk+GB 미분리** — 방향 앵커로만 사용)을 GB Ea가 설명하나?

**방법 (UMA 셋업)**: F-43m 기반 tilt GB bicrystal 주기셀(셀당 GB 2면, ~600–1200원자, Σ3(111)·Σ5(310)류 2유형).
γ-surface/강체 이동 스캔으로 저에너지 GB 선별 → UMA relax → **600/800/1000 K Langevin NVT 3-seed**,
MSD 2–50 ps 창. GB 슬래브(±5 Å) vs bulk 영역 분리 MSD + GB-면내/수직 성분 분해로 "GB가 빠른 길인가 벽인가" 판정.

**기존 자산**: `tools/ionic`·`tools/modelc_v3`의 MD 파이프라인(aimd_mlip.py, disorder_ensemble_diffusion.py,
msd_origin.py), 아레니우스 3점·600 K 3-시드 오차막대 규율 그대로.

**자원·기간**: gabia A6000(큰 셀 VRAM). GB 구축·선별 1주 + 2유형×3T×3seed **약 3–4주**.

**리스크·UMA 유효성**: argyrodite GB 원자 구조는 문헌에 정립돼 있지 않음(음이온 무질서+Li 부격자) —
**GB 모델 구축 자체가 결과의 절반**. GB 코어(저배위 P/S)는 bulk 검증 범위의 경계 → GB 에너지 DFT 스팟체크 1건.
Kraft 0.46은 total 임피던스 — 우리 GB Ea 절대값과 직접 비교 금지, "GB Ea > bulk Ea 인가"의 방향 판정만.

**co-doping ML 연결**: 직접 연결은 약함. 후속으로 도펀트 GB 편석(segregation) 캠페인의 발판.

**안 되면 알게 되는 것**: GB Ea ≈ bulk이면 "LPSCl의 저항은 GB 고유 물성이 아니라 접촉/공극(가공) 문제"라는
판정 — DEM 트랙(접촉 면적·압밀)에 힘이 실린다.

---

## ③ 표면 H₂O 첫 반응 스텝 — 공기안정 테마의 kinetics 검증

**물리 질문**: 수분 열화 첫 단계(H₂O 흡착 → P–S 가수분해 개시)가 도핑으로 늦춰지나?
zhu2020은 열역학(Li₃PO₄ 형성 구동력 −0.608 eV/H₂O)만 줬고 kinetics는 공백 — 그 반쪽을 채운다.
cascade air_stability 테마는 큐레이션(HSAB) 등급 — 이걸 계산 근거로 승격.

**방법 (UMA 셋업)**: LPSCl(001)류 슬랩(termination scan 관례 승계, ~100–200원자) + H₂O 1–4분자.
UMA relax(흡착 지형) + 300–500 K 단시간 MD(10–20 ps × 다수 시드)로 해리 이벤트 통계 → 대표 해리 경로 1–2개
drag/CI-NEB. 비교: undoped vs air_stability top(ZnO·SnO₂·Cu₂O — taklu2021 Cu-도핑 H₂S 절반 앵커) vs 산화물 champion.

**기존 자산**: `tools/vgcf_hbn` drag/NEB 인프라(drag_build_kgy.py, neb_build_kgy.py), termination_scan 슬랩 관례,
cascade air_hsab 테마(검증 대상), zhu2020·taklu2021 digest.

**자원·기간**: kgy(작은 셀) 스크린 1–2주 + KISTI DFT 스팟(대표 경로 CI-NEB) 1주 → **약 3주**.

**리스크·UMA 유효성**: **분자 H₂O·H 전달은 omat 학습 분포의 경계** — 이 후보의 최대 리스크. UMA는 흡착
지형·이벤트 유무 스크리닝까지만, 해리 barrier 정본은 QE CI-NEB(즉 UMA=정찰, DFT=정본으로 역할 고정).
zhu2020 수치는 소환값 — 우리 barrier와 같은 표에 절대값 혼합 금지.

**co-doping ML 연결**: 가장 직접적. air_stability(soft acid Cu·Ag)와 electronic_insulation의 정면 상충이
themes에 co-doping 동기로 명시돼 있음 — top pair의 표면 버전 검증이 그대로 논문 포인트.

**안 되면 알게 되는 것**: 도펀트별 첫-스텝 barrier 차이가 노이즈 이내면 공기안정 개선은 표면 kinetics가 아니라
상 형성 열역학·입자 형상 문제 — 실험 쪽 제언(코팅·조습 공정)이 바뀐다.

---

## ④ 도핑 표면 work of adhesion — choi2025 SMD-PMF 이식

**물리 질문**: 도핑이 SE|Li(·SE|코팅) W_ad를 어느 방향으로 바꾸나 — rigid-cleavage의 dangling-bond
과대평가(calib 문서: 100–1000×) 없이. choi2025가 보인 "제작법이 W_ad 지배"를 우리 프로토콜로 통제.

**방법 (UMA 셋업)**: adhesion_v30u 36-registry rigid 스크리닝(UMA)으로 순위 → top/bottom 3쌍만
**SMD+Jarzynski PMF**(choi2025 파라미터 출발: k=0.01 eV/Å²/atom, v=0.01 Å/ps, 조건당 3회 독립 pull)
→ 기존 binding-curve(Morse)와 3자 교차. 절대값이 아니라 **순위가 rigid와 일치하는가**가 1차 질문.

**기존 자산**: `tools/adhesion_v30u` 전체(uma_screen_all_pairs.py, bond_density_36reg — Li–O/Cl–O 결합밀도
descriptor는 choi2025의 Cu–Ta/Cu–N 카운트와 같은 발상으로 외부 확증됨), `db/properties/adhesion.json`, choi2025 digest §8.

**자원·기간**: gabia(pw.x 동시 실행 금지 주의) 또는 kgy. 스크린 1주 + SMD 3쌍×3회 1–2주 → **약 2–3주**.

**리스크·UMA 유효성**: **UMA vacuum 민감성이 급소** — 30 Å OK / 60 Å에서 10× 과대 기록(adhesion_energy.md).
SMD는 vacuum을 열며 당기므로 분리거리 상한을 짧게 고정하고 PMF plateau를 이른 창에서 읽는 프로토콜 필요
+ pull 속도 수렴 테스트 필수(choi2025 Fig S5 관례). W_ad 절대값 인용 금지, 계열 내 상대·순위만.
Li 계면은 N 무함유 → Li₃N 조항 비저촉.

**co-doping ML 연결**: 현재 co-doping 목적함수에 접착 축이 없음 — 이 캠페인이 themes에 "adhesion" 축을
추가할 데이터를 만든다.

**안 되면 알게 되는 것**: SMD-PMF 순위가 rigid 순위와 같으면 "싼 rigid 스크리닝 계속 사용" 면허.
다르면 기존 adhesion 순위 전체 재감사 대상 — 어느 쪽이든 방법론 결론이 남는다.

---

## ⑤ 균열/파괴 인성 프록시 — notched slab (DEM 트랙 연결)

**물리 질문**: 도핑·조성(Cl-rich 포함)이 LPSCl 취성 파괴 저항(G_c 프록시)을 바꾸나?
bucci2017/2018의 임계(균열 방지 G_c ≥ 4 J/m², compliant SE E<25 GPa가 오히려 취약 — 소환 앵커)와
DEM 파괴 파라미터에 원자론 근거를 공급.

**방법 (UMA 셋업)**: pre-notched 주기 슬랩(~5–10k원자, notch 길이 2종으로 크기 의존 체크),
준정적 인장(변형률 스텝 + relax) 또는 300 K 저속 인장 MD. crack 개시 변형률·응력, 에너지 해방률 프록시,
crack tip 소성 여부(연성/취성). 계: undoped vs modelc(Cl-rich) vs B₂O₃ vs mechanical_soft top(MnO·Cr₂O₃) 중 2종.

**기존 자산**: elastic 체인(`tools/elastic`, fit_elastic_cij — E_GPa·pugh 테마와 정합 체크), bucci 임계값 앵커,
DEM 트랙(LIGGGHTS 복합전극)의 파괴/접촉 파라미터 수요 — 산출을 DEM 입력 등급으로 넘긴다.

**자원·기간**: gabia A6000(대형 셀 단일 GPU 적합). 수렴 테스트 포함 **약 3–4주**.

**리스크·UMA 유효성**: crack tip = 결합 파단 직전의 원거리 배열 — **MLIP OOD가 가장 심한 구간**.
UMA E 절대값 부풀림은 이미 기록(themes caveat "절대값은 UMA 부풀림 — 내부 상대비교만") → G_c류 절대값
인용 금지, 같은 셋업 내 조성 상대비교만. notch 크기·변형률 의존 수렴 테스트를 결과 이전에 확보.

**co-doping ML 연결**: ductility(Pugh)·mechanical_soft 테마의 상위 검증 라벨 — 프록시(B/G)가 실제 파괴
순위를 예측하는지 자체가 ML 피처 검증.

**안 되면 알게 되는 것**: 조성 간 차이가 노이즈 이내면 파괴는 조성이 아니라 미세구조(공극·GB·접촉) 지배 —
DEM/공정 레버가 정답이라는 판정으로 논문 프레임이 명확해진다.

---

## ⑥ NCM|SE 양극 계면 상호확산 (KISTI급)

**물리 질문**: 고전압 양극 접촉에서 원소 상호확산(P/S→산화물 쪽, TM→SE 쪽)이 어디서 시작되고,
도핑·코팅 박막이 이를 차단하나 — ESW(열역학)와 실측 열화 사이의 kinetics 공백.

**방법 (UMA 셋업)**: LiNiO₂(001)|LPSCl 슬랩(수백 원자 — sdcp_linio2 자산의 산화물 슬랩 재사용),
UMA relax + 600–800 K 가속 MD **3-seed × 100 ps**, 원소별 z-침투 프로파일(① analyzer 재사용).
비교축: undoped vs oxidative_stability top 도핑 vs ⑦ champion 산화물 박막 삽입. 계면 DFT 스팟(SCF·부분 이완)은 KISTI.

**기존 자산**: `kb/projects/sdcp_linio2_binding.md`(LiNiO₂ 슬랩·binding 프로토콜), ① 계면 analyzer,
adhesion 슬랩 스택 프로토콜, 코팅 문헌 축(sundar2025·choi2026 bzox digest).

**자원·기간**: gabia(UMA MD) + KISTI(DFT 스팟, QOS 제출 제한 유의). **약 5–6주 — 7건 중 최대.**

**리스크·UMA 유효성**: **MLIP는 산화수·스핀 상태를 출력하지 못하고 하전 셀(q≠0)·폴라론 국소화 분기를
다루지 못한다** — 학습 참조계가 전하중성 supercell PES 하나뿐이기 때문. (단 '원리적으로 못 본다'는 과장이다:
in-distribution 범위에선 (탈)리튬화에 수반되는 Jahn–Teller 왜곡·TM–O 결합거리 변화 같은 **산화환원 구동 구조
에너지는 PES에 인코딩돼 있다**.) 그래도 주장 범위는 "확산 기하·원소 이동"까지로 못박고 산화환원 서사는 금지. Ni 산화물 표면의 UMA 유효성
스팟체크(DFT 대비 표면 에너지·계면 SCF) 선행. 규모·리스크 모두 커서 착수 순위는 뒤.

**co-doping ML 연결**: oxidative_stability 테마 top(Sc₂O₃·Cr₂O₃ 등, 단 ox_V 축퇴 caveat)의 계면 검증 무대.

**안 되면 알게 되는 것**: UMA 시간창에서 상호확산이 안 보이면 계면 열화는 열적 확산이 아니라 전압 구동 —
grand-potential ESW 체인이 이 축의 정본임을 재확인하고 MD 확장은 접는다.

---

## ⑦ 코팅상 자체의 Li 투과 barrier — champion oxide NEB

**물리 질문**: cascade champion 산화물이 코팅으로 쓰일 때 Li이 실제로 통과 가능한가 —
"절연·안정은 좋은데 Li이 못 지나가면 무용"이라는 코팅 후보의 마지막 게이트. themes의 ionic_transport는
호스트 채널 프록시라 **코팅상 내부 수송은 현재 공백**.

**방법 (UMA 셋업)**: champion 산화물 4–6종(B₂O₃·Sc₂O₃·Gd₂O₃·Y₂O₃·Al₂O₃; DFT 검증 이력은 B₂O₃·Nd₂O₃뿐)
bulk supercell(2×2×2급)에서 Li vacancy/interstitial CI-NEB 5–7 images — **ASE NEB + UMA 1차 스크린 →
최저 barrier 2상만 QE neb.x(kgy) 검증**. cascade v23 EOS 구조를 시작점으로 사용.

**기존 자산**: `tools/vgcf_hbn` NEB 인프라 전체(neb_build_kgy.py·run_neb_kgy.sh·watch 관례 + 2L2L 스팟체크로
전제 반증한 교훈 = 스팟 DFT를 결과 앞에 두는 습관), `tools/neb_diffusion`, li3n NEB의 DFT 파이프라인
(2-point 구속이완·drag 체인), cascade_v23 champion 구조·EOS.

**자원·기간**: kgy RTX3090. UMA 스크린 수일 + QE NEB 2상 1–2주 → **총 약 2주. 7건 중 최저 비용.**

**리스크·UMA 유효성**: 대상 산화물은 N 무함유 — Li₃N 금지조항 비저촉이지만 **교훈은 그대로 적용**:
UMA 단독 barrier 인용 금지(li3n에서 UMA 0.054 eV가 thin-slab 아티팩트로 철회되고 DFT 0.1182 eV가 정본이
된 사례가 정확히 이 실패 모드). **MLIP는 전하중성 supercell PES만 학습한다** — 하전 셀(q≠0, 배경전하 보정)·폴라론 자기포획 준안정 분기·
스핀 상태 분기를 다루지 못한다. (⚠ '중성 원자 proxy'라는 옛 표현은 틀렸다: 중성 셀에 Li를 넣으면 DFT
바닥상태가 **Li⁺ + 호스트 CBM/폴라론 전자**라, MLIP가 재현하는 것도 중성 Li⁰가 아니라 그 Li⁺-유사 상태다.)
이 항목의 1순위 리스크는 전하 상태가 아니라 위의 **thin-slab 아티팩트**와 **비정질 코팅 가능성**이다.
비정질 코팅이 실제 형태일 수 있음 → 결정 barrier는 상한/하한이 아니라 "결정상 기준값"으로만.

**co-doping ML 연결**: "Li 투과성" 축을 themes에 신규 등록할 데이터 — 코팅 후보 선정이 절연×안정×투과의
기하평균으로 완성된다.

**안 되면 알게 되는 것**: champion 전부 barrier ≳1 eV면 "벌크 산화물 코팅" 콘셉트 기각 —
초박막·비정질·Li 함유 상(LiBO₂류)으로 후보 공간을 재정의해야 한다는 명확한 신호.

---

## 추천 착수 순서 (3건)

1. **① Li|SE 계면 반응성** — analyzer·프로토콜이 이미 3-seed 캠페인으로 실전 검증됐고, 사용자 명시 요청이며,
   co-doping ML의 첫 실측 라벨을 바로 생산한다.
2. **⑦ 코팅 Li 투과 NEB** — 최저 비용(kgy 2주)으로 cascade 스토리의 빠진 반쪽(스크리닝→투과 게이트)을 닫는다.
3. **② GB 수송** — bulk-vs-total Ea 간극이라는 가장 큰 서사를 우리 데이터로 답하지만, GB 모델 구축 리스크가
   있어 인프라가 도는 ①⑦ 뒤가 안전하다.

> 공통 유의: 어느 후보든 첫 산출물은 "UMA 스크리닝 결과 + DFT 스팟체크 계획"까지가 한 세트다.
> UMA 단독 수치가 db/properties에 canonical로 등록되는 일이 없도록 status 필드에 단계(screening/verified)를 명시한다.
