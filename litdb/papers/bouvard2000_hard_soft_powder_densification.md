# 경/연 분말 혼합물의 가압 압밀 거동 — Bouvard (Powder Technology 2000)

> slug `bouvard2000_hard_soft_powder_densification` · DOI `10.1016/S0032-5910(99)00293-4` · type `exp+theory(review)` · PDF `Bouvard_2000_PowderTech_Densification_of_hard_and_soft_powder_mixtures.pdf` · digested `2026-06-23` · status ✅

## 1. 한 줄 요약
경(rigid, 비변형) 입자 + 연(plastic/visco-plastic, 변형) 입자 혼합물의 가압 압밀을 **연상 항복응력 vs 압력**으로 두 체제로 나눈 리뷰 — **(A) 저압(σ_y_soft ≫ P): 재배열 지배, 경입자 多가 오히려 유리; (B) 고압(연입자 변형 지배): 경입자가 압밀을 방해**하고, 경입자가 **작을수록·각질일수록·percolating할수록** 더 심하게 방해. 우리 **SE(연)+AM(경)** 복합체의 porosity-vs-조성 (Furnas/dip) 이야기의 **물리적 원형(prototype)** — 단 소재는 금속·세라믹, 압밀은 HIP/die-press 고온이라 절대값 전이 불가, 추세·메커니즘만 차용.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| D. Bouvard (INP Grenoble, GPM2, UMR CNRS 5010) | Powder Technology 111 (2000) 231–239 | 10.1016/S0032-5910(99)00293-4 | **해당 없음** (금속+세라믹 모델계: Astroloy/Ag/Pb/Al(연) + alumina/WC/TiB₂/carbide(경)) | 실험 리뷰 + 패킹 수치모사 해석 (DEM 아님) |

> ⚠ **우리 소재(LPSCl+NMC811) 아님.** "연=soft 금속(Astroloy 초합금·Ag·Pb·Al·Co), 경=hard 세라믹(alumina·WC·TiB₂·carbide)." 우리 매핑: **연 SE(LPSCl, plastic) ↔ soft / 경 AM(NMC811, rigid) ↔ hard**. 이 매핑이 §7 비교의 핵심.

## 3. 핵심 물성 (수치)
> 전부 **상대밀도(relative density, ρ_rel = ρ_porous/ρ_full)** 단위. 압력·온도·조성은 각 예제계마다 다름. 이온/전자/열 전도도·coverage·Z·E_SE·Heckel·PSD는 **이 논문에 없음(전달·소성 파라미터 리뷰 아님)** → n/a. **모든 ρ 값은 그림(Fig 1·4·5·7·8)에서 읽은 digitized 추세** 또는 본문 stated.

| 물성 | 값 | 조건 (P, 조성) | stated/digitized | 비고 |
|---|---|---|---|---|
| 상대밀도 (pure soft) | **0.995** | Astroloy 단상, 100 MPa·1000°C·3h HIP | stated | 순연(純軟) 완전치밀 근접 |
| 상대밀도 (+18% 경) | **0.95** | Astroloy+18 vol% alumina, 同조건 | stated | 경 18% → 0.045 손실 |
| 상대밀도 (+35% 경) | **0.86** | Astroloy+35 vol% alumina, 同조건 | stated | 경 35% → 0.135 손실 (큰 hindrance) |
| 크기비 r 효과 (TiB₂) | ρ=0.98 (r 最低) → 0.92 (r 最高) | Ti-alloy+22 vol% TiB₂, 200 MPa·800°C·3h | stated | **작은 경입자(낮은 r)일수록 더 치밀** |
| Ag–WC 등밀도점 | **ρ=0.85**: 40 vol% WC(r=2.5) ≡ 25 vol% WC(r=10) | die-press 600 MPa, 상온 | stated | r↑(경입자 큼)면 더 많이 넣어도 同밀도 — 경입자 클수록 방해 작음 |
| 상대밀도 (Al+60%carbide) | **~0.85 (20°C) / ~0.91 (450°C)** | Al+60 vol% carbide, die 600 MPa | stated (Fig 7) | 60% 경입자인데 고밀도 → "surprising"; 온도↑→σ_y_Al↓→재배열↑ |
| carbide 초기/최종 충진 | 초기 ρ≈0.5서 30%부피 → ρ=0.91서 55%부피(최대패킹) | Al+60%carbide | stated | 경입자 골격이 재배열로 치밀화 (carbide 자체 변형·파쇄 無) |
| WC–Co 트렌드(역전) | Co **낮을수록** 더 치밀 (Fig 8: 0%>5%>10%>16%>24%) | WC+0–24 vol% Co, die press 상온 | stated+digitized | **재배열 지배 체제** — 경입자 多가 유리(통상과 반대) |
| percolation 임계분율 (mono, r=1) | **f_hard = 0.32** (기하 0.32) | 수치모사 (Lange/Bouvard 패킹) | stated | bonded면 0.32, **sliding 허용시 0.96** (Jagota–Scherer) |
| percolation 임계분율 vs r (Fig 11) | r=1: ~0.32 · r=2: **0.18** · r≈3–4: ~0.13 | 단분산 구 패킹 수치모사 | stated(r=2)+digitized | **작은 경입자(큰 r=d_soft/d_hard)** → 훨씬 낮은 분율서 percolate |
| 클러스터 통계 (Fig 10) | f_incl=0.1→58% 고립·23% 쌍 · 0.2→32% 고립·18% 쌍 · **0.35 첫 percolation** · 0.5→95% 단일클러스터 | 단분산 구 10000개 패킹 | stated | 고립→aggregate→percolation 정량 |
| σ_ionic / σ_e / σ_thermal | **n/a** | | | 전달 논문 아님 |
| coverage / Z / E_SE / σ_y / Heckel / PSD | **n/a** | | | 소성 파라미터·전달 리뷰 아님 (정성 메커니즘만) |

> **크기비 정의 (논문 고유, 중요):** `r = (연입자 평균크기)/(경입자 평균크기) = d_soft / d_hard`.
> r ≫ 1 = 경입자가 연입자보다 훨씬 작음(→ percolate 쉬움, 방해 큼); r ≪ 1 = 경입자가 큼(→ 고립, 방해 작음).
> ⚠ **우리 r̄(=r_SE/r_AM, SE가 작으니 ≪1)의 역수 방향**이지만 *방해의 물리*는 동일: "작은 경상(rigid)이 percolating 골격을 만들면 압밀을 막는다."
> 우리계: 경=AM(큰 입자), 연=SE(작은 입자) → 이 논문 r = d_SE/d_AM ≈ **0.1–0.4 (r ≪ 1, 경입자 큼)** → Fig 11 좌측 = percolation 임계 ~0.3–0.4 (경입자 분율 높아야 percolate).

## 4. 방법 (실험 리뷰 + 패킹 수치모사 — DEM/MPM 아님) ★
이 논문은 **시뮬레이션 코드 논문이 아니라** 저자 그룹의 여러 실험 데이터([1–7], 모델계 [8–14])를 모아 메커니즘으로 해석한 **리뷰**다. §4를 우리 템플릿대로 "DEM/MPM/전달솔버"로 채울 게 거의 없으므로 **실험 압밀 프로토콜 + 분석모델**로 적응.

- **code / version**: 없음 (실험 리뷰). 단 percolation 임계는 **저자(Bouvard & Lange [17], Besson & Bouvard [10])의 입자 패킹 수치모사** 결과를 인용 — 단분산(또는 이분산) 구 ~10⁴–10⁵개를 cubic box에 무작위 배치, 일부를 "inclusion(경)" 라벨링 → 클러스터 분석(Fig 10·11). **이것이 우리 DEM 패킹/percolation 분석의 1세대 선조**이나, 힘·접촉법칙 없는 **순기하 패킹**(우리 LIGGGHTS 접촉역학과 다름).
- **DEM 접촉법칙**: n/a (DEM 아님).
- **재료 파라미터 (소성, 실험 관찰)**: 정량 σ_y·E 표 없음. 정성: 연상은 visco-plastic(고온 HIP) 또는 plastic(Al·Pb·Ag), 경상은 rigid·non-deforming. **온도가 σ_y_soft 조절자**(Al 60%carbide: 20°C ρ0.85 → 450°C ρ0.91, σ_y_Al 감소로 재배열·변형 촉진).
- **bond/binder 모델**: WC–Co granule 제조에 **polyethyleneglycol 2 wt% 바인더**(과립화용, 압밀 메커니즘 아님). 우리 SBR/CB와 무관.
- **MPM/continuum (있으면)**: **Delie & Bouvard [14]** — circular visco-elastic 연입자 + 임의형상 rigid inclusion의 **정사각 배열을 수치적으로 변형 계산**(2D, isotropic). → "고비표면·각질 inclusion이 압밀에 불리"를 정량 확인. **이것이 이 논문에서 MPM/연속체-소성에 가장 가까운 부분** (우리 MPM의 정성 선조 — 단 2D 주기배열, 진짜 morphology 아님).
- **전달 솔버**: n/a (전달 평가 없음).
- **입자 처리** ★ (DEM판 "무질서 처리"):
  - 실험 = **진짜 입자**(연입자 진짜 소성 변형 + 형상변화 — SEM Fig 2·3·6에서 직접 관찰; 경입자 진짜 rigid·각질/구형 구분).
  - 패킹 수치모사 = **구만**(단/이분산), 무작위 배치, **힘 없는 순기하** (percolation·클러스터용).
  - Delie–Bouvard 모델 = circular(2D 원) 연입자 + 임의형상 경 inclusion, **진짜 변형장 계산**(visco-elastic).
  - ⇒ 이 논문은 **"진짜 형상 소성"을 실험·미세구조로 직접 보는 쪽**(우리 MPM이 시뮬로 채우는 그 물리) — 우리 DEM의 δ-overlap 프록시도, 우리 MPM의 J2도 아닌 **실측 기준점**.
- **도메인/RVE / seeds / 압력범위**: 실험 — die compression 또는 (hot) isostatic pressing; 압력 **100–600 MPa**, 온도 상온–1000°C, 시간 ~수 h(HIP) 또는 ~10⁴–10⁵ s. 패킹 모사 ~10⁴–10⁵ 구.
- **특이사항**: 모든 분말은 **Turbula shaker–mixer 건식 혼합** 후 die에 직접 충진(달리 명시 없으면). 경입자 형상은 제조법상 **각질(angular)**이 기본.

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | Astroloy 단상 vs +18%·+35% alumina **압밀곡선 ρ vs 시간**(1000°C·100 MPa HIP) | 경상 분율↑ → 최종밀도↓ 정량(0.995→0.95→0.86); 우리 porosity-vs-AM%의 고온 HIP 원형 |
| 2 | Astroloy+35% alumina **SEM**(연 clear/경 alumina dark): 연상이 경입자 접촉부 공극을 메움 + **alumina inclusion 균열(break-up)** | 연상 void-fill + **경상 percolating network가 응력 일부 받음**(균열이 그 증거) — 우리 force-chain/AM 응력분담의 미세구조 증거 |
| 3 | Ti-alloy+22% TiB₂ **SEM**, 크기비 大/小 비교: (a) 잔류공극이 세라믹 클러스터 내부 (b) 연속 세라믹망 + 큰 공극 | 작은 경입자(낮은 r)가 **연속 골격** 형성 → 공극 가둠; 우리 SE-rich/AM-rich 공극 위치 |
| 4 | Ag–WC **ρ vs WC vol%**(0–40%), r=0.08/1/2.5/10 별 곡선 (600 MPa die) | **크기비 r 정량 효과**: 작은 WC(큰 r)일수록 동일 부피서 밀도 더 떨어짐; r=10(WC 큼)은 40%여도 거의 방해 없음. 우리 size=packing 추세 |
| 5 | Pb+18% **구형 vs 각질** inclusion 압밀곡선(150°C, 8 MPa iso) | **형상 효과 분리**: 각질이 구형보다 압밀 더 방해 — 우리 (구만 쓰는) DEM·MPM이 못 보는 축 |
| 6 | Pb+구형 vs 각질 inclusion **SEM** @ρ=0.9: 구형은 연상 변형 적게, 각질은 강하게 둘러싸야 | 형상→필요 변형량 차이; 우리 coverage(Tabor)·morphology에 형상 미반영 한계 직시 |
| 7 | Al+60% carbide **ρ vs 축응력**(0–600 MPa), 20°C vs 450°C | 60% 경입자인데 600 MPa서 ρ0.85–0.91; **온도(σ_y_soft)가 압밀 레버**; 우리 E_eff/σ_y 연화의 실험적 근거 |
| 8 | WC–Co **ρ vs 축응력**, Co 0/5/10/16/24 vol% (상온 die) | **역전 트렌드**: Co(연) 적을수록 더 치밀 = **재배열 지배 체제**(경입자 多 유리); 우리 dip의 "저압·기하 패킹" 쪽 극단 |
| 9 | **모식도**: 경입자 분율 따라 isolated / aggregates / percolation 3체제 | 우리 percolation/dip 3-zone 그림의 교과서 원형 |
| 10 | 단분산 구 패킹 **클러스터 분포**(f_incl 0.1–0.5): 고립%·percolating 클러스터 출현 | f_incl=0.35서 첫 percolation, 0.5서 95% 단일 — 우리 f_perc·연결성 임계의 기하 기준선 |
| 11 | **percolation 임계분율 vs 크기비 r** (수치모사): r=1→0.32, r=2→0.18, r→대 더 낮음 | **percolation은 크기비의 함수** — 우리 porosity 관계식의 (조성×크기) 항을 정당화하는 핵심 그림 |

## 6. Post-processing ★
- **무엇**:
  - **상대밀도 ρ_rel = (다공체 무게밀도)/(완전치밀 무게밀도)** — 압밀의 1차 지표(우리 (1−porosity)와 동치).
  - **압밀 동역학 곡선** ρ(t) (HIP) / ρ(P) (die) 피팅 — 우리 Heckel과 같은 자리이나 **Heckel 형태(ln 1/(1−D)=KP+A) 명시 안 함** (HIP는 시간의존 creep이라 Heckel 부적합; die press는 ρ-vs-P 곡선만).
  - **클러스터 분석**(Fig 10): 패킹 내 inclusion을 라벨링 → 연결성분 크기분포 → 고립/aggregate/percolating 분율.
  - **percolation 임계분율**(Fig 11): 첫 spanning 클러스터 출현 분율을 크기비 r의 함수로.
  - **임계 부피분율(critical volume fractions)**: 3체제 경계 분율 = f(r) — Fig 9 모식 + Fig 11 곡선.
- **도구**: 자체 입자패킹 코드(Bouvard–Lange [17], Besson–Bouvard [10]); Delie–Bouvard 2D 변형계산 [14]; SEM(미세구조); Jagota–Scherer [16]·Lange "excluded volume" [9] 해석.
- **수치화·플롯·기록 방식**: ρ vs 시간/응력 곡선군(조성·r·온도 패러미터), percolation 임계 vs r 단일곡선, 클러스터 분포 로그-로그. **모두 추세·임계 위주, 보편 압밀법칙(Heckel) 정량 피팅은 없음.**

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
> 매핑: **연 soft = SE(LPSCl, plastic) / 경 hard = AM(NMC811, rigid)**. 단 소재(금속·세라믹)·압밀(HIP/고온 die)·압력(100–600 MPa, 일부 고온)이 우리(LPSCl 냉간 300 MPa)와 달라 **절대값 직접 전이 불가 — 추세·메커니즘만**.

| 항목 | 이 논문 | 우리 | 차이 / 이유 (rigid·plastic / 소재 / 2D·3D / 기하·역학) |
|---|---|---|---|
| 압밀 메커니즘 2분 | 저압→재배열(경 多 유리) / 고압→연 변형(경 방해) | DEM=재배열·packing+overlap-proxy / MPM=진짜 연 소성 void-fill | **우리 frame[5] 분업의 실험적 선조** — 우리는 둘을 두 모델로 분담, 이 논문은 한 압력축 위 두 체제로 봄 |
| 경상 분율↑ 효과 | **고압서 경상이 압밀 방해**(0.995→0.95→0.86 @18→35% alumina) | DEM/MPM: AM↑ → porosity↑(고-AM 쪽) | **같은 방향** ✓ — AM(rigid)이 SE 흐름·재배열을 막음 |
| 작은 경입자가 더 방해 | r↑(경 작음) → percolate 쉽고 압밀 더 막음 (Fig 4·11) | 우리 size=packing: SE/AM 크기비가 porosity·dip 위치 좌우 | **방향 정합** — 단 우리 경(AM)은 큰 입자(r=d_SE/d_AM≪1)라 percolation 임계가 Fig 11 좌측(높은 경분율 필요) |
| percolation 임계 | f_hard=0.32(r=1,mono)·0.18(r=2); sliding시 0.96 | 우리 f_perc·CN 임계(SE backbone 기준), Furnas dip AM~70–85wt% | **기하 percolation 동일 물리**; 단 그들은 경상 percolation(방해), 우리 dip은 연·경 합동 최적패킹 |
| Furnas/dip | **명시적 dip 곡선 없음**; "경 多가 저압선 유리"(WC–Co Fig 8 역전)는 dip의 한쪽 극단 | DEM·de Larrard dip AM 70–85wt%(기하), **MPM 소성연속체는 dip 재현 못 함** | 이 논문은 dip을 직접 그리진 않으나 **dip의 기하 기원(rigid 골격 재배열)**을 뒷받침 |
| 진짜 형상 소성 | **실험·SEM으로 직접 관찰**(Fig 2·6 연상 변형·각질 둘러쌈) + Delie–Bouvard 2D 변형모델 | MPM이 시뮬로 재현(SEM 코어보존+경계평탄화 ✓); DEM은 δ-overlap 프록시 | **우리 MPM의 실측 검증 대상** — 우리가 옳게 가는 그 morphology를 실험이 보여줌 |
| 형상(각질/구) 축 | **각질>구형 더 방해**(Fig 5·6), Delie–Bouvard 정량 | 우리 DEM·MPM **둘 다 구만** → 이 축 없음 | **우리 공통 한계** — frame 밖. 비구형은 future work(Varkey도 동일 자인) |
| 온도(σ_y) 레버 | 온도↑→σ_y_soft↓→압밀↑(Al carbide 0.85→0.91) | 우리 E_eff 1.35/σ_y 0.15–0.30 softened — granular 메커니즘 럼핑 | **연화 정당화의 실험 근거**: 실제 연상 σ_y는 온도·재배열로 크게 낮아짐 = 우리 18× 연화의 물리 |
| 전달(σ_ion/e/th) | **없음** | 우리 삼중항 + Kirchhoff/Holm | 이 논문은 압밀·패킹 전용 — 전달은 전적으로 우리 영역 |
| 차원/스케일 | 실험 3D(절대) + 패킹모사 3D | DEM 3D, MPM 2D/3D | 패킹 3D는 우리와 동일 차원 — **percolation 임계 수치(0.32 등) 직접 참조 가능** |

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **porosity 관계식의 (조성 × 크기비) 항을 이 논문이 직접 정당화.** Fig 11(percolation 임계 = f(r))과 Astroloy 0.995→0.95→0.86(경분율↑)은 우리 "porosity = f(φ_SE, E_SE-stiffness, **크기비**)"에서 **크기비 항이 필수**임을 실험으로 뒷받침. 특히 "작은 rigid상이 percolating 골격을 만들면 floor가 올라간다"는 **rigid-sphere floor(~20%)의 기하 기원**과 직결 — 우리 MPM이 dip을 못 만드는 이유(소성연속체엔 rigid 골격이 없음)와 같은 동전.
- ② **두 체제(재배열 vs 연-변형)가 우리 frame[5] 분업의 실험 선조.** 저압·재배열·경상골격 = **DEM·de Larrard 기하**(dip 소유), 고압·연상소성 void-fill = **MPM morphology**(SEM 일치). 이 논문은 둘을 한 압력축에서 보여주므로, 우리 "DEM=transport/packing, MPM=mechanics/morphology" 분담의 **단일계 교과서 근거**로 인용 가능.
- ③ **WC–Co 역전 트렌드(Fig 8: 연상 적을수록 치밀)**는 우리 dip의 "저압·기하 패킹이 지배하면 AM(rigid) 많은 쪽이 오히려 치밀"이라는 한쪽 극단을 실증 → 우리 dip이 단순 "SE 많을수록 치밀"이 아니라 **압력·체제 의존**임을 강화. 다만 이는 **재배열 지배 체제**(σ_y_soft ≫ P)이고, 우리 LPSCl 300 MPa는 **연상 변형 지배(σ_y_SE ~50–300 MPa ≲ P)** 쪽이라 직접 동일시는 주의.

## 9. 인용 가능 문장 (deck/paper용)
- "Bouvard's review of hard/soft powder compaction establishes the two governing regimes that our DEM and MPM divide between: a low-pressure rearrangement regime, favoured by a *high* rigid-particle fraction, and a soft-deformation regime in which rigid particles *hinder* densification — more severely when they are small, angular, or form a percolating skeleton (percolation threshold f_hard ≈ 0.32 for size ratio r = 1, dropping to 0.18 at r = 2)."
- "The experimental observation that a percolating rigid skeleton bears part of the applied stress and arrests densification (Bouvard 2000; alumina-inclusion break-up, Fig 2) is the physical origin of the rigid-sphere porosity floor that our plastic MPM cannot reach and that DEM captures through its discrete rigid network."

## 10. 주의/한계 (over-claim 방지)
- **소재 전이 불가**: 금속(Astroloy·Ag·Pb·Al·Co) + 세라믹(alumina·WC·TiB₂·carbide). **LPSCl·NMC811 아님.** σ_y·E·온도 거동이 우리 황화물 SE와 전혀 다름 → **절대 ρ·임계분율 수치는 추세·기하 percolation(차원만 같은 3D)에 한해 참조**, 우리 porosity 절대값과 직접 비교 금지.
- **압력·온도 레짐 다름**: 100–600 MPa + 상온~1000°C(HIP creep 포함). 우리 LPSCl 냉간 300 MPa 단일과 다름. 특히 HIP는 시간의존 creep → **Heckel 정량 피팅 없음**(이 논문은 ρ-vs-P/t 곡선·임계만).
- **digitized 주의**: ρ 곡선 값(Fig 1·4·5·7·8)·percolation 임계(Fig 11 r≠2 점)는 **그림에서 읽은 추세**(±) — stated 텍스트 값(0.995/0.95/0.86, r=1→0.32, r=2→0.18, Al carbide 600MPa 0.85/0.91, 클러스터 58/32/95%)과 구분.
- **DEM/MPM 코드 아님**: 시뮬 파라미터(접촉법칙·E_eff·grid)는 n/a. 패킹 수치모사는 **힘 없는 순기하**(우리 LIGGGHTS 접촉역학과 다름) — percolation/클러스터 기하만 차용, 압밀 force-chain은 SEM 정성뿐.
- **크기비 r 방향 주의**: 논문 r = d_soft/d_hard (연/경). 우리 r̄ = r_SE/r_AM (작은 SE/큰 AM) → **이 논문 r과 같은 양**(연/경 모두 SE/AM), 단 우리계는 r ≪ 1 영역(경=AM이 큼) → Fig 11 좌측. "작은 경입자가 percolate"의 직접 적용 X (우리 경=AM은 큰 입자); 대신 "**작은 연상(SE)이 큰 경상(AM) 골격의 공극을 채운다**"가 우리 그림 — 같은 percolation 물리의 거울상.
- **전달 없음**: σ_ionic/e/thermal·coverage·Z·Heckel·tortuosity 전부 n/a. 이 논문은 **압밀·패킹·percolation 전용** → 우리 전달 삼중항과는 비교 불가, 압밀·dip 쪽만.
- **형상 축은 우리 한계를 비춤**: 각질>구형 방해(Fig 5·6)는 **우리 DEM·MPM 둘 다 구만 써서 못 보는 축** — 이 논문을 인용해 "비구형 효과는 future work"임을 정직하게 명시(Varkey 2026·Bazzoun 2026도 동일 자인).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
