<!-- digest 표준 양식 (standard depth — 1저자 우선순위 낮음 · Perspective). 형식 이웃 = nam2026_dpe_microstructure_review.md (framework/positioning 카드).
     쪽 표기 = 학술지 쪽 글자 (ASAP 판 — 쪽 번호 A–L · 이 카드는 PDF 쪽 1–17 로 적는다).  SI (Table S1, DOCX) 미보유.
     값 표지: [인쇄] = 본문 · 표 · 캡션 · [판독] = 그림 · [우리 대조] = 정본 litdb 카드 · 우리 문서와 맞춘 것 · [추정] · [미확인].
     본문 전부 pdftotext 정독 · 그림 4 + 표 2 + TOC 1 = 크롭 7 장 접촉 시트로 열람. -->
# 고분자계 전해질 (SPE · 겔 · 이온겔 · 복합) **모델링을 고르는 틀** — 목적 (기전 · 예측 · 선별/최적화 · 신호 분류) × 근거 (물리 · 데이터 · 혼성) × 결합도 (비결합 · 뭉뚱그림 · 약결합 · 완전결합) × 축척 (분자 · 메조 · 연속체/소자 · 신호/데이터) · 이온겔 모델 연구 24 편 지도 = **메조 축척 0 · 완전결합 0** · 고분자 전해질 함유 복합전극은 ASSB 무기 SE 전극 모델 (Alabdali · Ben Hadj Ali) 에서 배워야 — Zhang · Sun · Elia · **Franco** · **Gerbaldi** (ACS Energy Lett. 2026, Perspective)

> slug `zhang2026_polymer_electrolyte_modeling_perspective` · DOI `10.1021/acsenergylett.6c02246` · type `perspective (모델링 방법론 틀 · 고분자계 전해질 · 이온겔 문헌 지도 · 복합전극 microstructure / percolation / random-resistor-network 연결 — 새 계산 없음)` · PDF `10._Modeling_Approaches_for_Polymer-Based_Electrolytes_in_Advanced_Batteries_Bridging_Processing_Structure_and_Performance.pdf` · digested `2026-10-13` · status ✅
>
> **저자**: **Ying Zhang**† (Politecnico di Torino GAME Lab · INSTM GISEL) · **Pei Sun**† (UPJV LRCS · LAMFA · RS2E) · Giuseppe A. Elia (PoliTo GAME Lab · ALISTORE) · **Alejandro A. Franco\*** (UPJV LRCS · ALISTORE · RS2E · IUF — alejandro.franco@u-picardie.fr) · **Claudio Gerbaldi\*** (PoliTo GAME Lab — claudio.gerbaldi@polito.it) · † 공동 1저자 · *ACS Energy Letters* (ASAP — 권 · 쪽 미정, *"XXXX, XXX, XXX–XXX"*) · 접수 2026-07-22 · 수정 09-05 · 승인 **2026-09-15** · **CC-BY 4.0** · 참고문헌 170 편 · SI = Table S1 (이온겔 모델 연구 분류표, DOCX — **업로드에 없음**) · 연구비 PRIN 2022 (EnabLi) · MASE ORANGEES · MITI CNRS 등 · 저자 고지: *"AI tools were used solely for language polishing"* [인쇄 p.12].
> **정본 litdb 이웃 (이 글이 인용 · 카드 있음)**: [`alabdali2023_cgmd_wet_manufacturing_ssb_cathode`](alabdali2023_cgmd_wet_manufacturing_ssb_cathode.md) (= ref 154) · [`sun2026_dem_extrusion_recirculation_dry_electrode`](sun2026_dem_extrusion_recirculation_dry_electrode.md) (= ref 161, 같은 공동 1저자 Pei Sun) · [`bielefeld2019_microstructural_modeling_composite_cathode`](bielefeld2019_microstructural_modeling_composite_cathode.md) (= ref 158) · [`bielefeld2020_effective_ionic_conductivity_binder`](bielefeld2020_effective_ionic_conductivity_binder.md) (= ref 159) · [`minnmann2024_microstructure_porosity_visualization`](minnmann2024_microstructure_porosity_visualization.md) (= ref 160).

---

## 0. 결론 먼저 — 우리에게 쓸모 (정직하게: 낮음 · 방법론 틀로만)
- 대상은 **고분자계 전해질** (우리 계 = 황화물 LPSCl 무기 SE) — 물질 수치는 하나도 옮길 것이 없다.  새 계산 · 새 자료 없음.
- 쓸모 둘:
  1. **모델 분류 틀 4 축** (목적 · 근거 · 결합도 · 축척) — 우리 DEM+MPM 파이프라인을 외부 어휘로 적을 때 쓸 수 있다 (§7).
  2. 복합전극 수송을 **"상 정의 → 국소 물성 부여 → 연결성 · tortuosity · 접촉 면적 · 퍼콜레이션 평가 → percolation 해석 / kMC / random-resistor-network / FE 로 유효 수송 → 연속체로 전달"** 하는 절차를 권한다 [인쇄 p.11] — **우리 DEM 접촉망 (Kirchhoff/Holm) 이 바로 그 random-resistor-network 갈래**다 (외부 권고와 우리 방법의 일치 — 근거가 아니라 위치 표시).
- 그 밖: *"Models that focus mainly on ionic conductivity while neglecting compaction state, interface mechanics, and contact evolution may therefore not fully capture rate performance and cycling behavior"* [인쇄 p.10] — 우리 압밀 (DEM) + 접촉망 + 형상 (MPM) 분업의 필요를 외부 문장으로 적은 것.

## 1. 한 줄 요약
고분자계 전해질의 거동은 명목 조성이 아니라 **제조 중 형성된 물질 상태** (배위 · 결정성 · 액상 영역 · 충전재 계면 · 망) 가 정한다는 전제 위에서, 모델 연구를 **목적 · 근거 · 결합도 · 축척/자료 수준** 4 축으로 분류하는 진단 틀을 제안하고, 이온겔 모델 연구 24 편 (2013– ) 을 지도로 그려 *"분자 축척 · 기전 목적 · 비결합"* 에 몰려 있고 **메조 축척 · 완전결합 · 데이터 기반이 비어 있음**을 보인 뒤, 고분자 전해질 함유 복합전극에 대해 ASSB 무기 SE 복합전극 제조-미세구조 모델과 다공 전극 공정 모델 (ARTISTIC CGMD+DEM) 에서 전략을 옮겨 오라고 권한다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| Y. Zhang†, P. Sun†, G. A. Elia, **A. A. Franco\***, **C. Gerbaldi\*** (PoliTo · UPJV LRCS) | ACS Energy Lett. 2026 (ASAP) · CC-BY 4.0 | 10.1021/acsenergylett.6c02246 | 고분자계 전해질 (SPE · 겔 · 이온겔 · 고분자-세라믹 복합) · 고분자 전해질 함유 복합전극 | Perspective (참고문헌 170 · 새 자료 없음) |

---

## 3. 핵심 내용 · 수치 (전부 [인쇄], 그림 판독은 표지)

### 3-1. 진단 틀 4 축 (Fig. 2 · p.5–6)
| 축 | 범주 |
|---|---|
| **목적 (objective)** | (i) 기전 (mechanistic) (ii) 예측 (predictive) (iii) 선별 · 최적화 (iv) 분류 · 신호 분석 |
| **근거 (basis)** | (i) 물리 기반 (ii) 데이터 기반 (iii) 혼성 (physics–data) |
| **결합도 (process coupling)** | (i) 비결합 (ii) 뭉뚱그림/실효 결합 (lumped) (iii) 약결합 (일방 · 단계 · 순차 교환) (iv) 완전결합 (상호 의존을 한 정식화에서 풂) — ⚠ 축척 사이 정보 전달 (scale-bridging) 과는 **다른 축**이라고 명시 |
| **축척/자료 수준** | (i) 분자 (ii) 메조 (도메인 · 망 · 연결 경로) (iii) 연속체/소자 (iv) 신호/자료 (스펙트럼 · 영상 · 곡선) |
- 집계 규칙: 여러 축척에 걸친 연구는 각 칸에 하나씩 · 결합도는 **가장 높게 명시된 수준** · 목적은 **주된** 것 하나 [인쇄 p.6].

### 3-2. 이온겔 모델 연구 지도 (Fig. 3 · p.6–7)
- **24 편** (2013 년 첫 직접 관련 연구부터) · 상세는 SI Table S1 [인쇄 p.6] — SI 미보유 [미확인].
- Fig. 3a (근거 × 축척, 배치 수): 물리 기반 — 분자 **20** · 메조 0 · 연속체/소자 1 · 신호 0 / 데이터 기반 — 전부 0 / 혼성 — 분자 2 · 메조 0 · 연속체 1 · 신호 2 [인쇄 p.6 + 판독 일치].
- Fig. 3b: 가장 큰 칸 = **기전 · 분자 · 비결합 18** · 약결합은 예측 · 연속체/소자 에만 · **완전결합 0 · 분류/신호 목적 0 · 메조 0 · 순수 데이터 기반 0** [인쇄 p.6].
- 저자 해석: 이온겔 모델링은 기전 해석에 치우쳤고, 메조 축척 (도메인 · 연결 경로 · 분포 계면) 이 *"underrepresented modeling level"* [인쇄 p.7].

### 3-3. 표 1 — 질문별 대표 방법 · 출력 (p.5)
| 질문 | 대표 방법 | 전형적 출력 |
|---|---|---|
| 어떤 화학이 에너지/전기화학적으로 유리한가 | DFT · AIMD · NEB | 결합/용매화 에너지 · 배위 자리 · 분해 경향 · 이동 장벽 |
| 이온 · 사슬 · 이온성 액체가 국소적으로 어떻게 움직이나 | 고전 MD · 분극 역장 MD | 자기확산 · 전도도 추정 · 배위 분포 · 체류시간 · 분절 이동도 |
| **형상 · 불균일이 이온 경로에 어떻게 작용하나** | **조립 MD · DPD · SCF · 망/퍼콜레이션 모델** | **도메인 간격 · 상 연결성 · tortuosity · 퍼콜레이션 문턱 · 경로 연속성** |
| 기계 · 유변이 공정성 · 안정성에 | 연속체 역학 · 점탄성/유변 · 위상장 | 모듈러스 · 응력/변형장 · 계면 진화 · 박리 지표 |
| 운전 조건에서 전해질/전극 응답 | 연속 수송 · 다공전극 이론 · 농후용액 이론 · 전기화학-기계 | 농도 · 전위장 · 전류 분포 · 분극 · 응력 · 셀 전압/용량 |
| 임피던스 해석 | 등가회로 · DRT 등 | 벌크/계면 저항 · CPE · 이완시간 · 과정 분리 |
| 예측 · 선별 · 최적화 가속 | ML · 베이즈 최적화 | 후보 순위 · 전도도 경향 · 최적 조성 |

### 3-4. 표 2 — 이온겔 밖 대표 연구 6 편 분류 (p.8)
Borodin 2006 (PEO/LiTFSI · 기전 · 물리 · 비결합 · 분자) · Webb 2015 (예측 · 약결합 · 분자+메조 — 동적 결합 퍼콜레이션) · Tagliazucchi 2025 (블록공중합체 · **완전결합** · 메조+연속체) · Bonilla 2021 (LLZO/PEO · 뭉뚱그림 — 유효매질/퍼콜레이션) · Grazioli 2019 (PEO/LiPF₆ · **완전결합** 전기화학-기계 · 연속체) · Wang 2020 (선별/최적화 · 혼성 · CG-MD + 베이즈) [인쇄].

### 3-5. 고분자 전해질 함유 복합전극 (p.9–11 · Fig. 4)
- ASSB 복합전극에서 지금은 **무기 (특히 황화물) SE** 가 주로 이온 전도 상 [인쇄 p.8].
- 배울 두 이웃 분야 (Fig. 4): ① 다공 복합전극의 공정-미세구조 모델 — **ARTISTIC (CGMD + DEM)** 이 슬러리 · 건조 · 캘린더링을 풀고, 건식 압출 전극의 **DEM** 모델도 있다 (ref 161 = Sun 2026) — 단 고분자는 바인더/탄소-바인더 영역으로만 다뤄지고 **Li⁺ 전도 상이 아니다** · ② ASSB 무기 SE 복합전극 — Alabdali (NMC622 · Li₆PS₅Cl · 탄소-바인더 3 입자종 제조 모의, ref 154) · Alabdali 2024 (슬러리 입도 · 고형분 → 코팅 · 미세구조, ref 51) · Ben Hadj Ali 2025 (제조 모의 미세구조 → 3D 전기화학 방전, ref 36; 완전결합 기계-전기화학, ref 164) [인쇄 p.9].
- 차이: 무기 SE 는 별도 입자 상 · 고분자 전해질은 **바인더 · 매트릭스 · 기계 숙주 · Li⁺ 전도체를 한꺼번에** [인쇄 p.10].
- 한계 셋: 미세구조를 실측 재구성 · 미리 정한 구조로만 쓰고 **제조 공정과 잇지 않음** · *"raw-material-to-cell"* 틀 부재 (Gallo-Bueno ML 은 DOE 자료 의존 · 블랙박스) · **제조 때 만든 퍼콜레이션 경로가 운전 중 변함** (전기화학-기계) [인쇄 p.10].

### 3-6. 로드맵 (p.11–13)
- 물질 상태를 명목 조성 이상으로 정의 (분자량 · 염/액상 함량 · 경화 이력 · 팽윤 · 형상 · 측정 온도 · 셀 구성) · 데이터 기반 모델에도 같은 표준 보고 요구.
- **관측량의 역할을 명시** — 제약 · 서술자 · 매개변수화 입력 · 초기/경계조건 · **보정과 독립인 검증 표적** 중 무엇인지 [인쇄 p.11].
- 구조 표현 절차: 상 정의 → 국소 물성 → 연결성 · tortuosity · 접촉 면적 · 퍼콜레이션 문턱 → **퍼콜레이션 해석 · kMC · random-resistor-network · FE** 로 유효량 → 연속체/소자로 전달 [인쇄 p.11].
- 결합도는 모델링 목적이 정당화하는 만큼 (의역) — 무시하면 그 운전 영역에서 왜 무시해도 되는지 근거를 적는다 [인쇄 p.11].

## 4. 방법 · 입자 처리
- 문헌 분류 · 틀 제안만 (새 모델 없음).  입자 처리 = 논의 대상 모델에 따라 다름 (CGMD · DEM 은 입자 · 나머지는 연속체).

## 5. Figure set
| Fig / Table | 내용 | 우리 활용 |
|---|---|---|
| TOC | 모델링 → 합리적 · 공정 인지 · 소자 관련 설계 (개념) | — |
| 1 | 축척별 대표량 (배위수 · tortuosity · 반응 불균일 …) · 실험 ↔ 모델 정보 흐름 · 조성 → 공정 → 구조 → 물성 → 성능 사슬 | 우리 사슬 (DEM 압밀 → 망 → STEP3/4) 설명 그림의 참고 틀 |
| 2 | 4 축 진단 틀 (목적 · 근거 · 결합도 · 축척) | ★ 우리 파이프라인 분류에 그대로 (§7) |
| 3 | 이온겔 24 편 지도 (a) 근거 × 축척 열지도 (b) 목적 × 결합도 거품 | 메조 공백 = 접촉망/DEM 같은 메조 모델의 자리 |
| 4 | 이웃 분야에서 옮길 두 전략: 다공 전극 공정 모델 (ARTISTIC) · 무기 SE 복합전극 모델 (Alabdali) | 우리 DEM 은 둘째 갈래 (무기 SE · 입자 접촉망) 에 속함 |
| Table 1 | 질문 → 방법 → 출력 | 메조 줄 (망/퍼콜레이션 → tortuosity · 퍼콜레이션 문턱) |
| Table 2 | 이온겔 밖 6 편 분류 | 완전결합 예시 두 편 |

## 6. Post-processing
- 저자: 문헌 분류 (집계 규칙 §3-1) → 열지도 · 거품 그림.  우리: 본문 정독 · Fig. 3a 수치 ↔ 본문 대조 · 정본 카드 대조 (ref 154 · 158 · 159 · 160 · 161).

---

## 7. 우리 DEM+MPM 대비 (관련도 낮음 — 틀만)
| 축 | 우리 파이프라인을 이 틀로 적으면 [우리 해석] |
|---|---|
| 목적 | 기전 (압밀 · 접촉망 · 형상) + 예측 (조성 → 공극 · σ · tortuosity) + 선별/최적화 (LHS 설계 · ML 대리모델 — CLAUDE.md "설계→구조 ML 예측기") |
| 근거 | 물리 기반 (LIGGGHTS DEM · MPM · Kirchhoff/Holm 망 · STEP3 복셀 FV · STEP4 BV) + 혼성 (σ 스케일링 법칙 · GPR/Ridge 대리모델) |
| 결합도 | **약결합 (단계 · 순차)** — DEM 덤프 → 망 · DEM 골격 → MPM 스캐폴드 → STEP3 σ → STEP4 반응 (일방 전달) · 완전결합 아님 |
| 축척 | 메조 (DEM 입자 접촉망 · MPM 복셀) + 연속체/소자 (STEP4) + 신호/자료 (EIS/DRT 해석 훅) |
- 이 글이 지적한 **메조 공백** (이온겔) 과 *"구조 표현 → RRN → 연속체 전달"* 절차는 우리 DEM 접촉망이 하는 일과 같은 자리다 — 고분자 전해질 계가 아니므로 **근거가 아니라 위치 표시**.
- *"관측량의 역할 (보정 vs 독립 검증)"* 을 적으라는 권고 = 우리 frame[4] (DEM · MPM 각자 실험에 보정 · 서로 맞추지 않음) 와 같은 원칙 — 외부 문장으로 인용할 만하다 [우리 해석].
- 우리 첨가제 상 (PTFE 절연 바인더 · SDCP 전자 전도 고분자 — CLAUDE.md STEP3 첨가제 감사) 에 *"고분자 상의 여러 역할 (바인더 · 매트릭스 · 기계 숙주 · 전도체)"* 은 표현 규약 점검 항목으로만 [추정].

## 8. 적용 인사이트
1. 우리 방법 소개 (논문 Methods · 세미나) 에서 4 축 어휘로 위치를 한 줄로 적을 수 있다 — *"physics-based, weakly (sequentially) coupled, mesoscale contact-network + continuum"*.
2. *"제조 때 만든 퍼콜레이션 경로가 운전 중 변한다"* — 우리 A10 접촉 원장 · 제하 팔 부재 (F-SB1) 와 같은 공백 지적.

## 9. 인용 가능 문장
- "Models that focus mainly on ionic conductivity while neglecting compaction state, interface mechanics, and contact evolution may therefore not fully capture rate performance and cycling behavior." (Zhang et al., *ACS Energy Lett.* 2026, Perspective)
- "Effective transport … estimated … using percolation analysis, kinetic Monte Carlo, random-resistor-network, or finite-element calculations" — 메조 수송 표현 절차의 외부 서술.

## 10. 주의/한계
1. **물질계 다름** — 고분자 · 이온겔 중심 · 황화물 무기 SE 수치 전이 불가.
2. 지도는 이온겔 **24 편** 뿐 · SI Table S1 미보유 (분류의 근거 연구 목록 [미확인]).
3. Perspective — 틀 제안 · 문헌 분류 (자기 그룹 연구 다수 인용: Franco 그룹 ARTISTIC · Alabdali · Ben Hadj Ali · Sun).
4. ASAP 판 — 권 · 쪽 번호 미정.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 그대로)
| 번호 | 서지 | 왜 |
|---|---|---|
| 36 | Ben Hadj Ali, S.; Alabdali, M.; Viallet, V.; Seznec, V.; Franco, A. A. A computational workflow for the simulation of solid state battery electrodes from manufacturing to electrochemical performance. J. Power Sources 2025, 630 | 제조 모의 → 3D 전기화학 (ASSB) — 우리 DEM → STEP4 와 같은 사슬 (정본 카드 없음) |
| 164 | Ben Hadj Ali, S.; … Franco, A. A. Fully coupled mechanoelectrochemical modeling of 3D-resolved microstructures for solid state batteries manufactured by wet proc[ess] … | 완전결합 기계-전기화학 (정본 카드 없음 · 서지 일부 잘림 — PDF 원문 끝) |
| 51 | Alabdali, M.; Zanotto, F. M.; Notredame, B.; Viallet, V.; Seznec, V.; Franco, A. A. Experimental and Computational Analysis of Slurry-Based Manufacturing of Solid-State Battery Composite Cathode. Batteries Supercaps 2024, 8 (2) | 슬러리 입도 · 고형분 → ASSB 양극 미세구조 |
| 162 | Taghikhani, K.; Huber, W.; Weddle, P. J.; Asle Zaeem, M.; Berger, J. R.; Kee, R. J. Modeling coupled electro-chemo-mechanical phenomena within all-solid-state battery composite cathodes. J. Mech. Phys. Solids 2025, 198, 106060 | ASSB 복합양극 전기화학-기계 결합 모델 |
| 163 | Liu, C.; Roters, F.; Raabe, D. Role of grain-level chemomechanics in composite cathode degradation of solid-state lithium batteries. Nat. Commun. 2024, 15, 7970 | 결정립 화학역학 (li2026 리뷰에도 인용) |
| 154 · 158 · 159 · 160 · 161 | Alabdali 2023 · Bielefeld 2019 · Bielefeld 2020 · Minnmann 2024 · Sun 2026 | 정본 카드 있음 |

## 원문 대조 기록 (2026-10-13)
- 본문 17 쪽 pdftotext 정독 · 표 1 · 2 렌더 대조 · Fig. 3a 열지도 숫자 ↔ 본문 대조 (일치).
- 크롭 7 장 (TOC · 그림 4 · 표 2) · 캡션 = 텍스트 층 (TOC 는 캡션 없음 — 큐레이터 표기).
- 정본 litdb 전수 검색 (papers/ 목록 + DOI · 제목 · 저자 grep): 같은 논문 카드 없음.

## 🔗 관련 카드
`alabdali2023_cgmd_wet_manufacturing_ssb_cathode` · `sun2026_dem_extrusion_recirculation_dry_electrode` · `bielefeld2019_microstructural_modeling_composite_cathode` · `bielefeld2020_effective_ionic_conductivity_binder` · `minnmann2024_microstructure_porosity_visualization` · `ngandjong2021_dem_calendering_digital_twin` · `duquesnoy2023_ml_multiobjective_manufacturing_optimization` · `nam2026_dpe_microstructure_review` · `balasubramanian2026_rfb_electrolyte_kmc_lbm_preprint` (같은 Franco 그룹 · kMC+LBM).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
