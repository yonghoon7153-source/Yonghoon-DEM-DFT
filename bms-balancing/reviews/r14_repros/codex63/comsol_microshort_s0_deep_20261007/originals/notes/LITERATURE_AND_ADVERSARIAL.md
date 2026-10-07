# S0 문헌·자기 반박 메모

이 메모의 창·기울기·부호·margin 예시는 대안 검토다. 최종 채택 정의는 S0_REPORT_KO.md C2–C3 및 S1_SCOPE_DRAFT_KO.md가 우선한다. 특히 수치 감도가 크면 구별 불가가 아니라 INCONCLUSIVE다. 최종 NOT 조건은 |D|≤1mV, |S|≤1mV/h 및 5E_D≤1mV, 5E_S≤1mV/h를 모두 요구한다.

작성일: 2026-10-07. 대상 원장 commit: `fd7ce941a7c4d3989f80a133271189d67a6a0074`(부모 검토의 고정값). 아래 로컬 줄 번호는 `../sources/` 복사본 기준이다. 요청서와 deep brief는 Downloads 원문도 읽었다. 수행: 정적 독해·문헌 조회·식 유도. COMSOL/native/동봉 Java·분석 프로그램 실행 0, 실험 비교 0, 실험 저항→σ 역산 0. 문헌 실험값은 원 연구 맥락 설명용이며 현재 모델 또는 사용자 실험의 적합·비교에 사용하지 않았다.

표시: **확인** = 직접 읽은 원문/공식 자료의 사실; **조건부 추론** = 명시한 이상화 아래의 도출; **미확인** = S0 또는 조회 자료로 확정 불가. 웹 접근이 막힌 경우 출판사/저자 기관의 색인 본문으로 확인했음을 구별했다. 인용문은 웹페이지당 합계 25단어 미만이다.

## 1. 주요 판단

**조건부 추론, 높음.** 1D 균질 전자전도 S1은 `σ → I_leak → 전극별 Li 이동 → V(t)` 사슬을 확인하는 계산으로 유용하다. Fe 용해·석출·국소 성장·열적 피드백 또는 LLI 발생량을 직접 확인하는 계산은 아니다. “실제 미세단락을 구별했다”와 “동일 모델에서 유한 σ 효과가 수치적으로 구별되었다”를 분리해야 한다.

**확인, 높음.** `MICROSHORT_MPH_REVIEW.md:535–558`은 휴지 후반 기울기가 단락 전용 채널이라는 주장을 이미 철회했다. `MSC_SEMINAR_2026-09-23_APPLICATION.md:88–99`는 가설과 합성 모형 결과를 구분한다. 그 문서의 1–2%, 1.00–1.04, 가짜 열화 모드의 같은 크기 같은 결과는 현재 COMSOL 모델 또는 Fe 실셀의 보편 법칙이 아니다.

**조건부 추론, 높음.** 순수 단락은 충전 상태·에너지를 잃게 하지만 보존 모형의 Li 원자를 제거하지 않는다. 재충전으로 SOC를 복원할 수 있어도 단락이 계속 켜져 있으면 측정 중 외부 회수 용량은 줄어든다. 전극 OCP 불변 또한 측정 ICA 피크 위치 불변을 보장하지 않는다.

**확인, 높음.** 요청서 §3-3의 `r=1e−2 → 0.01C → 1%/h`는 10배 오류다. r의 분모가 0.1C이므로 `r=1e−2 → 0.001C → 약 0.1%/h`다. 또한 요청서의 `epss=1`은 현재 Java와 다르다. 직접 읽은 `Normal480Candidate.java.txt:593–594`는 `epsl_sep=0.45`, `epss_short=1-epsl_sep=0.55`; `:650–652`는 binder가 이 값과 `NoCorr`, 등방 `sigma_short` tensor를 사용함을 보여준다. 이 메모는 epss=1을 현재 사실로 채택하지 않는다.

## 2. 1차·공식 출처 원장

### L1 — 휴지 완화와 자기방전 관측량

Thomas Roth et al., *Relaxation Effects in Self-Discharge Measurements of Lithium-Ion Batteries*, Journal of The Electrochemical Society 170, 020502 (2023), DOI `10.1149/1945-7111/acb669`.

- [출판사 본문](https://doi.org/10.1149/1945-7111/acb669)
- [저자 기관 1쪽 결과 요약](https://www.epe.ed.tum.de/fileadmin/w00bzo/ees/OnePager_PDF/SIM/2023-03-01_TR_Relaxation_Effects_in_Self-Discharge_Measurements_of_Lithium-Ion_Batteries.pdf)
- 기관 요약의 짧은 인용: “Voltage relaxation disturbs for 12 – 20h”.
- **확인, 높음(색인 본문); 직접 열기는 robots/서버 오류.** Samsung INR21700–50E NCA/Si-graphite 및 비상용 NMC622/graphite pouch에서 전압감쇠·전압유지·용량손실을 비교했다. 전압 완화는 시간 단위, anode overhang은 주 단위까지 영향을 줄 수 있다. 전압 기반과 용량 기반 방법은 다른 Li 재고 변화를 읽는다.
- **전용 금지:** “현재 1D도 반드시 12–20 h 완화한다”는 결론은 나오지 않는다. overhang을 구현하지 않은 1D에는 그 경로가 없다.

### L2 — 외부 저항 모사, 37 Ah NMC

*Online Estimation of Internal Short Circuit Resistance for Large-Format Lithium-Ion Batteries Combining a Reconstruction Method of Model-Predicted Voltage*, World Electric Vehicle Journal 13(9), 170 (2022), DOI `10.3390/wevj13090170`.

- [출판사 원문 §4.1, §5](https://www.mdpi.com/2032-6653/13/9/170)
- 짧은 인용: “NMC batteries with rated capacity of 37 Ah”.
- **확인, 높음(출판사 색인 본문); 직접 열기는 429.** 7개 37 Ah NMC 모듈의 한 셀에 외부 저항·스위치를 연결했고 100 Ω, 10 Ω, 100→10 Ω 변경을 사용했다. 25°C 동적 운전·휴지·충전 조건이다.
- **전용 금지:** 외부 저항은 내부 국소 열원이나 전류집중을 재현하지 않는다. 해당 연구의 단계별 저항 설명은 soft/hard 보편 규정이 아니다.

### L3 — 외부 저항 모사, 50 Ah NCM의 3P 단위

*Investigation on Internal Short Circuit Identification of Lithium-Ion Battery Based on Mean-Difference Model and Recursive Least Square Algorithm*, IntechOpen, §3.0–3.4.

- [저자의 연구 본문](https://www.intechopen.com/chapters/68485)
- 짧은 인용: “The cell has a capacity of 50 Ah.”
- **확인, 높음(본문 직접 접근).** 50 Ah NCM의 세 병렬 셀을 유효 150 Ah 요소로 취급했다. 1/10/100 Ω와 추가 1000 Ω를 사용했다. 1000 Ω는 보통 SOC에서 검출하지 못했고 매우 낮은 SOC에서 8 h 40 min 후 검출했다. §3.4는 외부 저항과 실제 단락의 차이, 일반 자기방전과의 전압 구분 한계를 인정한다.
- **전용 금지:** 해당 검출시간은 특정 알고리즘·모듈·프로토콜·계측의 결과다. S1 시간 또는 일반 검출한계가 아니다.

### L4 — 국소 단락의 접촉, 셀 크기와 위치

Gi-Heon Kim / NREL, *Numerical and Experimental Investigation of Internal Short Circuits in a Li-ion Cell*, 2011 DOE Annual Merit Review, ES109, slides 12–15.

- [DOE 원본 PDF](https://www.energy.gov/sites/prod/files/2014/03/f10/es109_kim_2011_p.pdf)
- 짧은 인용: “Cell response varies with short location and cell electrical configuration”.
- **확인, 높음(원본 PDF).** 20 Ah 모델에서 전극간 1 mm² 단락은 약 20 Ω·0.16 A; 집전체간 경로는 약 10 mΩ·300 A 사례다. 위치 변경 사례는 4.7 mΩ·520 A와 10 mΩ·300 A를 대조한다. 해당 슬라이드에 전극 화학계가 명시되지 않아 여기서도 특정하지 않는다. 계산 사례이며 보편 저항 분포가 아니다.
- **전용 금지:** 이 열폭주 연구의 큰 전류 영역을 등온 1D 사다리 상한의 직접 근거로 쓰지 않는다.

### L5 — soft/hard의 접촉 및 단락 소멸

NREL, DOE *FY 2013 Annual Progress Report for Energy Storage R&D*, IV.B.6, 인쇄 pp.182–184(PDF pp.68–70).

- [DOE 원본 PDF](https://www.energy.gov/sites/prod/files/2014/05/f16/fy13_es_4_battery_testing_analysis_design.pdf)
- 짧은 인용: “if the active material is part of the ISC circuit”.
- **확인, 높음(원본 PDF).** 8 Ah Dow Kokam stacked pouch의 10% SOC 시험은 활성층 접촉과 Al–Cu 집전체 접촉 응답을 구분한다. 집전체 단락의 급격한 전압 감소는 약 50 ms 뒤 Al tab 용융으로 회복됐다. 검토 구간의 전극 화학계는 미기재다.
- **조건부 추론:** 고정 σ는 접촉 소멸·재형성·내부 병렬층 퓨즈 격리를 표현하지 않는다. 이 사례가 모든 Fe 단락의 소멸 기작은 아니다.

### L6 — Fe를 포함한 금속 오염의 전기화학 경로

H. Nakajima and T. Kitahara (2015), *Diagnosis Method to Detect the Incorporation of Metallic Particles in a Lithium Ion Battery*, ECS Transactions 68(2), 59–74, DOI `10.1149/06802.0059ecst`.

- [DOI](https://doi.org/10.1149/06802.0059ecst)
- [저자 소속기관 논문 초록](https://kyushu-u.elsevierpure.com/ja/publications/diagnosis-method-to-detect-the-incorporation-of-metallic-particle/)
- 짧은 인용: “copper, nickel, iron, and stainless steel”.
- **확인, 중간(기관 초록 색인).** 양극 금속 입자의 산화 용해 후 음극 전착을 연구했고 Cu/Ni/Fe/stainless steel의 CV·SEM/EDX와 EIS 변화를 다뤘다.
- **미확인:** 사용자 Fe 입자의 크기·용해 문턱·성장속도·온도의존성은 이 초록에서 얻지 못했다. 수 µm–수십 µm를 보편 크기로 확증하지 않는다.

### L7 — 금속 입자 성장의 공식 연구 사례

TIAX / Sriramulu et al., *Implantation, Activation, Characterization and Prevention/Mitigation of Internal Short Circuits in Lithium-Ion Cells*, DOE 2012 AMR ES142, slides 4–16.

- [DOE 원본 PDF](https://www.energy.gov/sites/default/files/2014/03/f10/es142_sriramulu_2012_p.pdf)
- 짧은 인용: “the anode, and grow back to the cathode”.
- **확인, 높음(원본 PDF).** 금속 입자의 양극측 용해·음극측 석출·분리막 관통 성장 경로를 검토했다. Ni coin-cell 사후 분석과 ≥2.6 Ah 18650 유도 단락 사례가 있다. 열적 결과는 외부 열·전기 환경과 내부 저항의 조합에 달렸다고 명시한다.
- **전용 금지:** Ni/LCO-graphite 그림은 Fe/NCM811-graphite 정량 증거가 아니다. 모든 금속 오염이 동일 경로라는 주장도 하지 않는다.

### L8 — LLI/LAM의 전극 기반 분해

M. Dubarry, C. Truchot, B. Y. Liaw (2012), *Synthesize battery degradation modes via a diagnostic and prognostic model*, Journal of Power Sources 219, 204–216, DOI `10.1016/j.jpowsour.2012.07.016`.

- [DOI](https://doi.org/10.1016/j.jpowsour.2012.07.016)
- [INL 기관 논문 기록·초록](https://inl.elsevierpure.com/en/publications/synthesize-battery-degradation-modes-via-a-diagnostic-and-prognos/)
- **확인, 중간(기관 초록 색인):** 전극별 거동·loading ratio·전극내/전극간 열화로 가상의 곡선을 구성한다. 아래 비교표는 이 논문의 도표를 재현한 것이 아니라 보존식으로 독립 도출했다.

### L9 — CE와 비가역 capacity loss의 비동일성

*Deciphering coulombic loss in lithium-ion batteries and beyond*, Nature Communications (2025), DOI `10.1038/s41467-025-60833-y`.

- [논문 본문](https://www.nature.com/articles/s41467-025-60833-y)
- [PMC 원문](https://pmc.ncbi.nlm.nih.gov/articles/PMC12216820/)
- **확인, 높음(논문 직접 접근):** 전하손실과 비가역 용량손실이 일대일이 아니고 전극간 inventory compensation이 중요함을 전기화학 측정으로 논의한다. “CE 결손 = 그만큼 LLI”를 일반식으로 쓰지 않을 근거다.
- **전용 금지:** 해당 화학 부반응·보상 기작은 현재 전자단락 모형에 구현됐다는 뜻이 아니다.

## 3. B3 — 문헌 저항과 σ 사다리를 나란히 읽기

| 문헌 대상 | 저항/접촉 범위 | 해석 | 옮기지 않는 것 |
|---|---|---|---|
| L2: 37 Ah NMC, 외부 저항, 25°C | 100 Ω, 10 Ω | 전기적 누설 모사 | Fe σ·크기·국소 온도 |
| L3: 50 Ah NCM×3P, 유효 150 Ah | 1000/100/10/1 Ω | 크기·SOC·알고리즘 의존 탐지 | 보편 soft/hard 문턱 |
| L4: 20 Ah 국소 모델, 화학계 미기재 | 전극간 약 20 Ω; 집전체 4.7–10 mΩ 사례 | 접촉·경로·열집중의 차이 | 등온 모델의 안전성 |
| L5: 8 Ah stacked pouch, 10% SOC | 활성층 soft-like / 집전체 hard-like | 접촉·퓨즈·지속성 | 작은 R이면 지속 hard라는 규칙 |

**조건부 추론, 높음.** 함께 볼 척도는 `I/Q`(h⁻¹), `I·T/Q`(SOC 비율), 국소 `I²R` 위치다. 이는 문헌 R에서 현재 모델 σ를 구하는 작업이 아니다. 설명용 고정전압 3.7 V를 가정하면 100 Ω는 37 mA다. 37 Ah에서는 0.100%/h, 150 Ah에서는 0.0247%/h이다. 이 값은 문헌의 측정 감쇠율이 아니라 단위 확인용 `V/(RQ)` 산술이다.

현재 사다리는 자체 면적당 `j_leak/Q_el`과 ΔV 예측으로 정한다. 부모 검토가 선택한 3600 s, `σ=1.7e−8,1.7e−7,1.7e−6 S/m` 및 정상 `1e−20`은 이 문헌표와 **나란히만** 둔다. “문헌 R 범위와 대응하는 σ” 열은 만들지 않는다.

`MICROSHORT_MPH_REVIEW.md:109–124`의 저항표는 **원본의** `epss=0.45`, 가정된 Bruggeman 1.5에 의존한다. 현재 source의 NoCorr에는 0.301869 계수를 그대로 옮기면 안 된다. 실제 source의 `epss=0.55` 의미와 전도식 소비자 확인은 부모 보고서의 정적 추적이 최종 근거다.

“문헌 범위에 든다”만으로 사다리를 정당화할 수 없다. 관측시간 내 SOC 이동·OCP 기울기·상태 허용범위·보존·수치 구별 가능성이 기준이다. 등온 모델이 강한 σ에서 수렴해도 실제 안전성이 확인되는 것은 아니다.

## 4. A3 — Li 장부와 관측량의 독립 재도출

아래는 **조건부 추론**이다. leakage 이외 side reaction, 활성 부피 변화, Li 경계 유출입이 없다고 가정한다. `j_l>0`는 방전 방향 누설 크기(A/m²), `q`는 저장된 충전량(C/m²), `N_N,N_P`는 전극 Li 재고(mol/m²)이다. 외부 전류 0, 준정상 총 반응에서:

```text
dq/dt = -j_l
dN_N/dt = -j_l/F,  dN_P/dt = +j_l/F
d(N_N+N_P+N_e)/dt = 0    (닫힌계; 구현된 전해질 재고 정의)
```

일시적 전해질 저장·이중층 경로가 있으면 전극별 순간 등식의 잔차도 포함한다. 보존검사에서 N_e를 임의로 생략하거나 항상 일정하다고 먼저 결론내리지 않는다. 전자는 음극→양극 단락 경로로, Li⁺는 이온 경로로 움직인다. 통상 전류 부호는 전자 운동 방향과 반대다. `I_ext=0`이 내부 반응 0은 아니다.

| 관측량 | 순수 전자단락: 고정 host·총 Li | LLI | LAM | 구분 한계 |
|---|---|---|---|---|
| 충전 V–Q_ext | 같은 내부 상태 창까지 더 많은 Q 필요; 반응속도 `I_ch−I_l` | 전극 정렬·stoichiometry 창 변경 | host capacity·반응면적 변경 | curve 하나로 원인 유일성 없음 |
| 방전 V–Q_ext | 내부 방전 `I_dis+I_l`; 외부 회수 Q 감소 | recharge로 inventory deficit 제거 안 됨 | recharge로 host 손실 제거 안 됨 | 계속 새는 RPT도 capacity deficit 생성 |
| ICA | U_N,U_P 불변, Q_ext 좌표·polarization 변화 | 정렬·사용창으로 peak 변화 가능 | capacity scale·활성면적으로 변화 가능 | peak 불변·한 방향 이동은 범용 지문 아님 |
| 휴지 V·dV/dt | SOC 감소 + 기존/유도 gradient 완화 | 고정 LLI는 추가 손실속도가 아니나 C_diff·초기상태 변경; 진행 side reaction은 drift 가능 | 고정 LAM도 C_diff·완화 변경 | 정상 휴지와 Li 장부 함께 필요 |
| CE | matched 내부 끝점·계속되는 leakage에서 <1 | 진행 LLI는 결손 가능; 과거 LLI 값 자체는 매 cycle CE<1 강제 안 함 | 고정 LAM 자체도 CE<1 강제 안 함 | CE→LLI 직접 환산 금지 |
| recharge | SOC deficit 복원 가능, leak 지속 시 외부 capacity deficit 반복 | fixed inventory deficit 유지 | fixed host deficit 유지 | 상태 복원과 capacity 복원 구분 |
| 반복 cycle | 동일 상태·시간·σ면 같은 패턴 반복; 고정 모델의 누적 LLI/LAM 없음 | 성장 law가 있어야 누적 변화 | damage law가 있어야 누적 변화 | MSC만으로 cycle별 열화 누적 보장 안 됨 |

LLI는 총 Li 원자 파괴가 아니라 **cyclable inventory** 손실이다. SEI로 이동한 Li까지 포함한 원자수는 보존될 수 있어도 intercalation 재고는 줄어든다. LAM이 Li를 포획하면 LLI와 결합될 수 있어 실셀 열화가 순수 모드들로 독립 분해된다고 보장할 수 없다.

같은 내부 상태 창의 가역 전하 `Δq>0`, 충·방전 누설 적분 `L_ch,L_dis≥0`이면:

```text
Q_ch,ext = Δq + L_ch
Q_dis,ext = Δq - L_dis
CE = (Δq-L_dis)/(Δq+L_ch) < 1
```

이는 matched electrochemical endpoints에서의 식이다. 임의 초기 cycle, 서로 다른 cutoff gradient, inventory recovery에는 이를 그대로 적용할 수 없다. `1−CE`를 다음 cycle host/Li 재고에서 다시 빼면 pure short 모델에 허위 LLI를 추가한다.

### ICA의 열역학 불변과 측정량 불변은 다르다

준평형에서 충전 상태 좌표 q, `C_diff=dq/dV>0`라 하면:

```text
charge:     dQ_ext/dV   = [I_ch /(I_ch-I_l(V))]  C_diff(V)
discharge: |dQ_ext/dV|  = [I_dis/(I_dis+I_l(V))] C_diff(V)
```

고정 저항도 `I_l(V)=V/R`이므로 prefactor가 V와 함께 변한다. C_diff의 극대점에서 prefactor의 도함수가 0이 아니면 곱의 극대점이 이동한다. 유한율 polarization은 이를 더 바꾼다. `MSC_SEMINAR...:75`의 열역학 불변 취지를 “측정 ICA peak 위치는 언제나 같다”로 확대하지 않는다. 저율일수록 누설/측정 전류비가 커지는 반면 고율은 polarization이 커지는 tradeoff도 남는다.

## 5. A4 — 균질 1D가 답하는 질문과 잃는 물리

| 차이 | 가능한 질문 | 누락의 영향 |
|---|---|---|
| 국소 filament / 전면 분산 | 평균 내부 전하 이동과 self-discharge | 같은 총 I도 국소 j·SOC 고갈은 더 큼. 확산 제한은 I 감소, 열 feedback은 증가 가능하므로 평균 V 편향 부호는 미정 |
| 접촉·집전체 path | 정의된 전극–전자전도 separator topology | collector/active-contact 다른 연결을 대표하지 못함(L4/L5) |
| 등온 / hotspot | 고정 T의 누설·전극 response | 열폭주·separator shutdown·hotspot 불가 |
| 고정 σ / 성장·끊김 | 일정 경로의 지속 누설 | 성장·소멸·재형성은 후반 drift와 분산 변경 |
| 전자통로 / Fe side reaction | 총 Li 보존 내부 방전 | Fe shuttle 또는 2차 SEI/LLI는 같은 V에도 다른 재고 가능 |
| 단면 평균 / in-plane 상태 | through-plane·입자 확산 | current crowding·국소 SOC·overhang 불가 |
| 상수 Ohm / contact 비선형 | `I∝Δφ` 가정 아래 반응 | `σ(T,V,t)`를 상수 한 개로 식별 불가 |

**조건부 추론, 높음.** Q1은 “같은 모델·상태에서 finite σ의 평균 자기방전이 정상 완화와 수치 차이를 넘는가”로 답할 수 있다. Q2 충전 비교는 S2의 별도 실행이며 S1만으로 확인할 수 없다. Q3의 Li 이동·보존은 S1 출력으로 분석할 수 있지만 실제 Fe가 2차 LLI를 만드는지는 현재 모델 밖이다. Q4 fit 오독은 별도 S3 문제다.

최소 2D 대안은 through-plane+in-plane, 전극/집전체 전도, 국소 contact 위치·면적, 열전도·국소 열원, 동일 초기 총 재고를 명시한다. 성장을 질문하면 접촉/증착 law를 추가해야 한다. 공간 자유도와 짧은 국소 시간상수로 비용이 늘겠지만 S0만으로 비용 배수를 확정할 수 없다. 2D라는 이유만으로 Fe 성장 기작이 생기지 않는다.

## 6. C — relaxation 및 검출 설계

**독립 도출.** 같은 초기 농도·재고·gradient를 공유하는 정상/단락 쌍에 대해 다음 채널을 미리 고정한다.

```text
D_V(t) = [V_sigma(t)-V_sigma(0+)] - [V_0(t)-V_0(0+)]
D_m(window) = slope_window(V_sigma)-slope_window(V_0)
Q_l(t) = integral_0^t j_l(s) ds
```

0+는 명시적으로 정의한다. σ on 직후 전위·과전압 점프 `V_sigma(0+)−V_0(0+)`를 별도 기록하고 누적 drift에 섞지 않는다. 동일 농도·직전 이력에서 σ만 다른 것이 대조다. 시작 전압을 억지로 같게 만들려고 서로 다른 SOC를 선택하면 안 된다.

누설 자체가 gradient를 바꾸므로 정상 subtraction이 모든 완화를 제거한다는 보장은 없다. 전극 Li 변화와 `Q_l/F`의 일치는 mechanism 확인이고 V 기반 검출과 별도 판정한다. 정상 σ≈0에서 작은 숫자상 I_l가 보이는 것만으로 검출 성공이라고 하지 않는다.

기울기는 사전 고정 시간창의 선형회귀로 정의할 수 있다. 예를 들어 승인된 3600 s 안에서 300–600 s와 1800–3600 s 같은 창을 고정하고 끝점 포함·가중치를 명시한다. 로그 출력이면 초기 샘플 수의 편향을 피하도록 동일 평가 격자 또는 시간 가중 회귀를 사용한다. 결과를 보고 고른 유리한 창은 exploratory로 분리한다.

수치 비교 기준은 **이번 같은 휴지 문제**의 tolerance·step·출력정책·공간격자 변화 envelope다. 과거 charge 자료의 µV/mV 차이는 관찰치이지 이번 휴지의 보장 error floor가 아니다. `3×envelope`를 선택한다면 engineering margin이며 통계적 3σ 또는 false-positive 확률이 아님을 명시한다.

SOC는 |dV/dq|가 큰 interior가 전압 signal에 유리하지만 table 끝점·kink·저농도·강한 polarization을 함께 피한다. 평탄 OCV에서 Li 이동은 분명하고 ΔV는 작을 수 있다. 따라서 “전압 미구별”과 “누설 없음”을 같은 판정으로 쓰지 않는다. OCP 기울기로 voltage drift를 나눌 때도 plateau/kink에서 ill-conditioning이 생긴다.

## 7. 다섯 현실적 반증과 확인 방법

| # | 설계를 무너뜨릴 반증 | S1 이전 검사 | 승인된 S1 내부 확인 | 판정/조치 |
|---|---|---|---|---|
| F1 | 누설 경로가 반응에 잘못 연결되거나 전도 보정·부호·단위가 틀림 | domain/boundary·NoCorr·epss·σ 소비자; old Bruggeman 미전용; A와 A/m² 분리 | separator 양끝 전자 flux, total current, 반응적분·Li 장부, `j_l≈σΔφ/L` 대조 | INCONCLUSIVE; σ fit으로 가리지 않음 |
| F2 | 정상/단락의 초기 Li·gradient·이력이 다름 | 초기 concentration 재고 또는 restart source/time 고정; 전압만 일치 금지 | 첫 시각 상태·초기화 보정 비교; 점프/drift 분리 | mismatched pair 무효; 같은 상태로 정의 |
| F3 | relaxation 잔차·출력 보간·미분 민감도가 signal | 창/가중치/끝점 고정; 과거 차이를 floor로 쓰지 않음 | 같은 휴지의 baseline와 finite σ refinement 및 저장정책 대조 | signal≤envelope면 NOT_DISTINGUISHABLE_WITHIN_T; envelope 불안정이면 INCONCLUSIVE |
| F4 | 준평형·상수 OCP 기울기 예측이 틀림 | OCP interval·kink·상태 이동·τ_relax 확인 | Q_l는 맞는데 ΔV만 다른지, 평균/표면 x·Δφ_sep−OCV 확인 | 축약모형 검증과 누설 검출 분리; 비선형 예측 사용 |
| F5 | 이 결과를 실제 Fe 존재·성장 진단으로 일반화함 | 누락 기작 목록·L1/L4–L7·질문 범위 대조 | S1만으로 actual Fe 가설은 반증/확증 불가능하다고 표시 | within-model sensitivity로 수용; Fe 목표면 별도 국소·반응 모형 |

F5는 S1 안에서 해결할 수 없는 **식별 불가능성** 자체가 반증이다. “문헌에도 Fe가 있으니 이 σ가 Fe다”라는 추론을 막는다.

## 8. S1 비실행 사유, 대안 및 요구 보강

목표가 오직 Fe 존재·크기·성장률, 실제 저항, soft/hard 위험도 또는 LLI 발생량의 정량 진단이면 현재 fixed-σ 1D 실행은 그 질문을 식별하지 못한다. 먼저 질문·모형을 맞춰야 한다. current/재고 관측이 정의되지 않았거나 같은 초기상태 대조가 불가능할 때도 V-only 사다리를 먼저 실행할 근거가 약하다.

반대로 현재 모형의 누설 구현·재고·반응 연계, transport·초기화, specified 시간의 수치 구별 가능성을 확인하는 것은 유효한 목적이다. OCV 축약만으로 이 DFN 구현 검증까지 대체할 수 없으므로 이 목적이면 2D가 무조건 선행할 필요는 없다.

요구서에 보강할 사항:

1. V-based distinguishability와 leakage/inventory consistency의 두 축을 둔다.
2. 단일 휴지에서 CE/충방전/ICA를 검증했다고 하지 않는다. S0 유도로 남기고 S2/S3를 구분한다.
3. 총 원자 재고와 cyclable Li 재고를 구분한다. pure MSC 보존은 현 모델의 sink 부재이지 Fe 실셀에 LLI가 없다는 뜻이 아니다.
4. σ on 초기 점프와 누적 drift를 모두 기록한다.
5. ICA 위치 불변과 `LAM_PE≈LAM_NE≈LLI` 공통 fit 신호는 범용 정리가 아니다.
6. Fe의 Ohmic/time-invariant/temperature-insensitive 성질은 미확인이다. fixed σ는 계산 정의다.
7. 요청서의 r→C-rate 10배 오류 및 실제 source epss mismatch를 정정한다.
8. “구별 불가”는 정해진 T·상태·관측량·수치정책 아래의 결과다. 물리적 σ=0 판정으로 확장하지 않는다.

**추천: S1 조건부 찬성.** 고정 1D 모델 내부의 누설·재고·전압 일관성과 3600 s 내의 수치 구별 가능성으로 목적을 한정할 때. 실제 Fe 기작·열화·안전성 입증으로 확대하지 않는다.
