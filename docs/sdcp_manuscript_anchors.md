# SDCP 매뉴스크립트 앵커 (Figures_v7, 2026-07-09 추출) — 모델 재배선 근거

사용자 매뉴스크립트 figure(15p: main 7 + SI S1-S22)에서 추출한 **실측 앵커**.  이전 웹서치 proxy
(conformal 필름·E 2 GPa·σ 315-1089 S/cm)는 전부 폐기/교체.

## 시스템
**Dry-processed ASSB cathode** (hot-rolling): NCM + LPSCl + PTFE + SDCP.
- **SBE** = Standard(PTFE-only) Binder Electrode / **DBE** = Dual(PTFE+SDCP) Binder Electrode
- +@C-SUS = SDCP/graphene 200nm 코팅 집전체(S14: 코팅 후 전도도 불변 1.3e4 S/cm; Fig5 접착 693→1029 aJ)
- wt% 조성은 methods 텍스트(미제공) — **TODO: 사용자 확인**

## SDCP 물성 (모델 입력)
| 항목 | 값 | 출처 | 모델 반영 |
|---|---|---|---|
| **형상** | as-made ~3µm 입자(S2) → 전극 내 **0.2-0.5µm 분산 입자**(S3, 노란원) | SEM | ★ kind='particle', SDCP_D=0.30µm; surface_frac=AM-앵커 몫(0.5 hook) + bulk 분산 |
| **E** | **23.6 GPa** (PTFE 5.6; long-tail~100) | AFM 모듈러스맵 Fig2d/S6 | ★ E=23.6 앵커 (LPSCl급 → rigid-proxy σ_y=1.0 §F1) |
| σ_ion (LPSCl+X pellet) | 3.57→**2.86** mS/cm (×0.80) vs PTFE 0.97 (×0.27) | Fig2f | STEP3: SDCP는 이온 저차단 |
| σ_e (LPSCl+X pellet) | 0.30→**1.53** e-7 S/cm (×5.1) vs PTFE 0.12 (×0.4) | Fig2g/S10 | STEP3: e-부스팅; econn 도체 유지 ✓ |
| 합성 | EDOT-MeOH+sultone→Na염 monomer→산화중합→이온교환 SO₃H | Fig2a/S4-5 | DFT monomer와 동일 ✓ |
| 열/구조 | XRD 무변화(S8), Raman/FTIR PEDOT+SO₃H(2b/S7) | | |

## 전극-수준 발견 (모델이 겨냥할 것)
- **S12: SDCP 단독 = dough 형성 불가** → PTFE fibrillation web이 필수 → **비교셋 = SBE(PTFE) vs DBE(PTFE+SDCP)**, SDCP-단독 런은 비물리
- **Fig3a: DBE에서 PTFE 분산 균일화** (SBE F-map 응집 → DBE 균일) — SDCP가 PTFE 뭉침을 억제 = 우리 fibrillation/분산 축과 연결 후보
- Fig3c-d: elastic recovery 0.69→0.82 / Fig4: R_ele 59.7→48.5 Ωcm², c-AFM 저저항 면적↑ / Fig6-7: 1000cyc@2C 안정, 저압(5MPa)서 격차 최대
- **Fig4(e) 'Electrochemical modeling' 빈 패널 + Fig7(c,d) placeholder** — 우리 3D 구조+연결성(econn) 시각화의 목표 슬롯

## 모델 반영 상태 (2026-07-09)
- additives.py: SDCP_D=0.30, v_obj=구부피, process rows regime='particle'+surface_frac(0.5/0.5/0.3 hook)
- mpm3d: kind='particle' 시딩(AM-앵커 몫 seed_coat(shell=반지름) + bulk 균일 in-pore), E=23.6 앵커,
  σ_y=1.0 rigid-proxy(§F1), **CFL dt 가드**(additive E가 SE 스택 초과 시 dt 캡 — VGCF 10도 소급 커버),
  metadata morphology/E_anchor/variant/INTERIM
- 유지: doped/neutral variant(coh·econn 처리), E_bind INTERIM(−4.8/−3.0 MLIP, DFT U-ramp 대기), ρ1.3 proxy(methods 대기)

## ★ 구조 정정 + E_bind 무효화 + cluster 가설 (2026-07-10) ★
**분자 구조가 달랐다** (사용자 발견, Fig 2a/S5 대조):
- 이전 DFT monomer: **C₁₁H₁₅O₅S₂** — 곧은 pentyl 사슬 말단 1차 술폰산 (EDOT–(CH₂)₅–SO₃H형)
- 실제 SDCP monomer: **C₁₁H₁₆O₆S₂** — `ring–CH₂–O–CH₂CH₂–CH(CH₃)–SO₃H` (EDOT-MeOH + methyl-sultone
  개환, S5).  차이: ① **ether –O– 링커** (O5→O6 — ether O 고립전자쌍의 표면 Li⁺ 배위 채널을 이전 모델이
  원천 누락; sulfonate+ether **chelation** 가능성) ② 말단 1차 → **methyl-분지 2차 술폰산** (입체/전자환경)
  ③ footprint/배좌 상이.
- ⇒ **E_bind −4.797/−3.020 eV 및 γ 0.93/0.42 J/m² 전면 무효** (`INVALID_WRONG_MONOMER`) — 재계산 스펙:
  올바른 monomer(위 구조; doped = 중성 radical charge0 doublet), 동일-세팅 refs(slab 공유), 다중 시작
  배향에 **ether-O-down/chelation 계열 포함**, PBC-aware H 확인, 수렴 후 DFT U-ramp 교차검증 + footprint
  재측정 → γ 재산출.  방향(doped≫neutral)은 bollard 사다리·술폰산 화학으로 개연 유지되나 **수치는 백지**.

**NCM 주위 cluster 가설 (사용자) — 물리 판정: 그럴 수 있음 (강함)**:
- **ordered/interactive mixing**: 건식 혼합에서 미세 guest 입자(0.2-0.5µm SDCP)는 부착력이 자중을 압도해
  조대 host(5µm NCM) 표면에 부착·장식됨 — 분체공학 표준 메커니즘 (제약 dry-coating/ordered mixture 문헌).
- **화학 선택성**: 술폰산-산화물(NCM) 이온성 앵커 ≫ 황화물(LPSCl) 상호작용 → NCM-선택적 장식 개연
  (pellet 호환성은 매뉴스크립트 σ 유지로 확인).  bollard 논문의 NMC 표면 앵커-patch EDS가 유사 선례.
- 반증 관찰: S3 (전극 표면)는 주로 SE 영역의 단독 입자 — NCM-인접 clustering은 S3 시야로 판정 불가.
- **모델 반영**: `--sdcp-clump` (process-row 기본 bm/thinky **1** = S3-충실 단독; handmix 3; >1 = cluster
  가설 시험) — anchored 몫을 AM 표면 cluster 중심 + 주변 산포로 시딩.  판별 도구 = SBE/DBE payload의
  SDCP→AM 근접 분석 (drape-식) + 실험 SEM/EDS.

## A4 마감 계획 (2026-07-10, "SDCP와 같이 닫기")
① VGCF `coat_embed` — **은퇴로 해결**: 10µm 강성 섬유는 5µm NCM을 '코팅' 못 함 (라벨이 처음부터 섬유
   물리와 불일치; Kim2025 코팅 우려는 carbon-black 것).  VGCF thinky ≡ ballmill이 물리로 확정 (기록
   데이터와 정합).  dead-cond 제거.
② SuperP thinky **divergence 검증런 1개** (마지막 관문): SuperP 2wt% thinky vs 기록된 ballmill 2wt%.
   사전등록: porosity **11.94 동일**(volume-pin) / **SE-cov 하락**(film이 AM|SE 계면 점유 — Kim2025 σ_i
   차단의 구조적 기반, emergent) / **add-cov AM_S ≫ 35.8**(film이 AM 표면 sf 0.70로 도포) / metadata
   `coat:{shell 0.2, surface_frac 0.70}` + cb_mix 부재.
③ σ_e 방향(coat_block → σ_e 붕괴) = 저항 수준 = webapp whatif ✓ / 구조-수준은 STEP3 Kirchhoff 몫 (econn
   binary는 표현 불가 — 명시 완료).  ①②완료 시 **A4 CLOSED**.

### 메커니즘 스토리 생존 판정 — 구조 정정 후 (2026-07-10)
사용자 DFT-측 논의(산-염기 surface-OH / 자가도핑 실재 / 앵커링 3시나리오 / 혼합폴리머 계면 귀결 /
Li⁺ tridentate)를 정정 구조(ether-O + methyl-분지 2차 술폰산)에 대해 판정:
- **유지**: ①산-염기 H⁺→surface OH (head 국소; α-Me +I ↔ β-ether −I 상쇄, 여전히 강산) ③앵커링
  3시나리오 ④양 상태 local-min+trigger ⑤"도핑 레벨 무관 모든 SO₃ unit이 계면 기여" — 논문 문장 유효.
- **유지+보강**: ②자가도핑 실재 — 근거가 실험(실물=에터 포함)이라 원래 옳은 구조의 증거; 틀린 건 시뮬
  모델뿐 (⚠시뮬 Raman은 재계산 + side-chain ether C-O-C 모드 ~1100 추가 → 배정 재확인).
  ⑥Li⁺ tridentate → **ether O = PEO형 Li⁺ 사이트 추가** = SO₃⁻+ether 단일이온전도체 모티프 완성 —
  Fig2f σ_ion 유지(×0.80)·ICEP(AMPS+PEO) 선례와 정합, 이온전도 서사 강화.
- **추가 필요**: 앵커링 시나리오 ④ ether-보조 chelation (재계산 시작배향 포함됨).
- **무효 유지**: 절대 수치 전부 + 삽입형 기하 재검증 (ether 유연성/메틸 입체).
- **재사용**: LiNiO₂ slab relaxation/U-ramp E_slab은 분자-무관 → 전부 유효; 재계산 = 분자+complex만.

### "1분자 3역할" (anchoring + Li-hopping + polaron) 판정 — 정정 구조 (2026-07-10)
- ①앵커링: 유지(head). ②**Li⁺ hopping: 크게 보강** — 정정 구조는 반복단위당 사이트 2개(SO₃⁻ 음이온
  사이트 + ether-O PEO형 사이트) → `SO₃⁻→ether→SO₃⁻` 사다리로 hop 거리↓장벽↓ (ICEP AMPS+PEO 선례).
  ③polaron: backbone 불변, packing 영향은 실물 σ_e ×5.1이 커버.  PVdF(접착만)·bollard PC(절연 2기능)
  대비 **SDCP만 3기능** = novelty 포지셔닝의 분자 버전.
- 정밀화: (a) 미세구조 한정 — 연속 interlayer가 아니라 **앵커된 0.3µm 입자의 NCM|SE 접촉 둘레**에서
  작동 (= 우리 particle+anchoring 시딩의 배치와 자기일관). (b) 역할② 정량 한 칸 — pellet ×0.80은
  '덜 차단' 증거; **재계산 패키지에 Li⁺ 결합(SO₃⁻ vs ether-O) + 사이트간 NEB 장벽 추가** 권고.
- STEP3 설계 노트: SDCP = 스택 최초의 **이중-전도 상** (PTFE 0/0 · VGCF e · SuperP e · **SDCP e+Li⁺**)
  → network solver에서 σ_e·σ_ion 동시 배정 (pellet 앵커 ×5.1/×0.80).
