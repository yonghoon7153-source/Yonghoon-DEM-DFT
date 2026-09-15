# 다음 모델 목적·기준 상태·장기 실행 준비도 — 결정용 정리

2026-09-15. **전체 수렴 미완·장시간 운전 보류. 후보 C 미승인.** 이번 작업은 기존 문서·소스·작업 상태·입력 명세의 읽기 전용 점검과 이 문서 작성뿐이다. COMSOL 호출/제출, 실행용 Java 생성, 기준 재실행, 모델 수정은 각각0회다. 초기 Eeq/OCV 산술이나 완료된 CDC 시험을 재계산하지 않았다. NEXT_RUN_PLAN·원본·실패 기록·영수증은 변경하지 않았으며 새 전달 ZIP도 만들지 않았다.

**권고는 300/320·16코어의 provisional 모델을 기능 진단 기준으로 삼고, 다음 한 건으로 전해질 농도 감시·중단 기능의 추가와 제한된 작동 시험을 승인받는 것이다.** 원본/실험과의 정량 대응을 먼저 완료해야 하는 업무라면 자료 확보가 선행되어야 하므로, 아래 목적 선택은 사용자가 확정해야 한다. 이 문서는 기능 진단 경로를 권고할 뿐 그 경로 또는 실행을 승인된 것으로 취급하지 않는다.

## 1. 다음 목적의 선택

| 목적 | 현재 증거로 가능한 일 | 현재 할 수 없는 주장 | 권고 |
|---|---|---|---|
| 6.3 provisional 기준 모델의 보호·프로토콜 작동 진단 | 명시된 가상 기준 입력에서 보호 조건, 전류 경계 소유권, 단계/종료 동작을 제한 시험으로 검증 | 실제 셀·원본6.4의 전압, 용량, 쇼츠 전도도를 재현했다는 주장 | **다음 작업의 임시 목적에 권고. 사용자 확정 필요** |
| 원본6.4·실험 셀 대응 및 마이크로 쇼츠 정량 해석 | 확보된 간접 리뷰와 재구축 입력의 대응/차이 식별 | 실험 조건과 상태가 확인되지 않은 채 sigma를 보정하거나 정량 추정 | 최종 연구 목적과 연결되지만 지금은 입력/상태 대응이 미완 |

처음 인계 요청은 6.3-native 마이크로쇼츠 모델의 재구축·검증이었고, 이후 사용자는 짧은 수치 진단을 단계별 승인했다. 이는 기능 진단을 이어갈 근거지만, 실험 정량 해석을 포기하거나 기능 진단을 다음 최우선 과제로 명시 확정했다는 뜻은 아니다. **선택할 항목은 “다음 승인 작업의 목적이 provisional 기능 진단인가, 실제 셀 정량 대응인가”**다. 원자료 부재가 provisional 기능 진단 자체를 불가능하게 하지는 않는다.

근거: [초기 인계](C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/work/COMSOL63_LOCAL_HANDOFF/CONTEXT_AND_CAVEATS.md), [현지 모델 결정](C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/MODEL_DECISIONS.md), [원자료 검색 기록](C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/inputs/original_data_inventory.json). 후보 C 문서는 사용자 첨부의 검토 의견으로 읽었으며 그 안의 조건부 실행안을 실행 지시로 취급하지 않았다.

## 2. 기준 모델과 해 선택

| 역할 | 기존 이름·job | 선택 이유와 제한 |
|---|---|---|
| 기능 진단의 권고 기준 | Caps300R320H0125C16 / `5d1a87652ed54e6a945d4f2af4aeda70` | 물리300(120/60/120)·입자320/320·16코어. 기존 동일16코어 후기 cap 비교와 B 물리축 비교의 기준이다. 현재 해는 **고정 전류 0.1C의 0–5초 해**, 완성 CDC/장기 모델이 아님 |
| 물리축 교차 확인 자료 | Caps600R320H0125C16 / `56975e4d24054b23bcec87553875f729` | 기존 B 결과 재사용. 더 세밀하다는 이유만으로 필수 기준으로 승격하지 않음. 이 해 자체의 후기 시간 민감도는 미검증 |
| CDC 구현·짧은 사건 시험의 참조 | PreflightCdcEvents20s / `b1bed498d08847a8abaa5fa1c6485cea` | 물리75/입자10·2코어의 별도 합성 전이 시험. 300/320 모델로 통합됐거나 그 격자에서 사건 정확도가 검증된 것으로 간주하지 않음 |

정본 Java SHA를 이번에 읽어 기존 식별과 일치함을 확인했다.

- [300/320 C16 소스](C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/comsol63/core16_control/Caps300R320H0125C16.java): `4db47e27dcf0d8d2977dc786dab2c3ba40e98a6adf42d7201bf1c66ab802537e`.
- [600/320 B 소스](C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/comsol63/physical600_b/Caps600R320H0125C16.java): `f230dcc0ccc2bb88c73b978ad9ebc564eb5e1c72cd328f24802d3f4435623906`.
- [짧은 CDC eventtol 소스](C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/comsol63/preflight/PreflightCdcEvents20s.java): `6c38a3126d43e384e723e797c33da1bdf816ed14ae14ea883e5fa977435da9f1`.
- [CDC 첫 충전 소스](C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/comsol63/preflight/PreflightCdcStart5s.java): `aa77620013cd18ea8240df88f4934ec234d707bf65a547432cde12d528198a60` / job `3bc366486dfe42f5a5c5310fc2dc15bf`.

300의 동일16코어 후기 cap 비교 최대 전압 차는0.0023442301413 mV, 표면 x 차는3.8702635005e−8이었다. B의 정확 공통987시각 최대 전압 차는1.07714000e−8 mV, 표면 x 차는5.2300400e−9이었다. 각각 기존1 mV·1e−4 표본 기준을 충족했다. B에서는 Eeq·과전압 상쇄가 관찰되므로 작은 단자전압 차이를 각 성분/참값 정확도로 해석하지 않는다. [CORE16 결과](C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/core16_control/CONTROL16_RESULTS_KO.md), [B 결과](C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/physical600_b/PHYSICAL600_B_RESULTS_KO.md).

관측된 한 job 전체 시간은300에서약942초,600에서약1421초였고 transient 자유도는79,485+12에서158,325+12로 늘었다. 이것은 해당 두 job 기록이며 일반적 성능 배율이 아니다. 보호 배선이라는 다음 목적에 추가 공간 해상도가 필요하다는 증거가 없어300을 권고한다. **어느 기준도 장시간 검증 완료가 아니다.** [시간 기록](C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/physical600_b/execution_timing.json).

C는 선택적 미완으로 보류한다. 나중에600을 실제 운용 기준으로 선택하거나 “후기 강화 cap에서도300과600의 관계가 유지되는가”가 설정 선택을 바꾼다면 유용하다. 그때 C−B는600의 cap 민감도, C−A는 강화 cap에서 물리축 민감도를 제공한다. 네 해의 같은 시각·위치 signed 차분은 해당2×2 조건의 진단이며 일반적 상호작용 부재나 수렴 차수가 아니다. C 결과가 초과이면600/cap 선택을 재검토하고, 충족이면 해당5초 진단까지만 수용하는 결정 규칙을 먼저 승인받아야 한다. 이번 다음 작업인 보호 누락 보완을 위해 C가 선행할 필요는 없다.

## 3. 물리 입력·비교 상태 대응표

“현지 직접 있음”, “다른 PC의 검토/추출 기록만 있음”, “확보 근거 없음”을 구분했다. 아래 수치는 기존 자료를 옮긴 것이며 새 전기화학 계산이 아니다.

| 항목 | 현지6.3 provisional 입력/근거 | 원본6.4·실험 대응 상태 |
|---|---|---|
| 원본 파일 | 새6.3 Java/MPH/로그·입력 재료·저장소 스냅샷·과거 리뷰 있음 | 2026-09-13 Documents/Downloads/Desktop의 지정 패턴 검색에서 `ICA_degradation mode.zip` 및 기대 원본 MPH 해시 일치본 미발견. 현재 입력/인계 폴더와 두 인계 ZIP의 항목 명세에도 원본 MPH/XLSX 없음. 전 PC/다른 이름/다른 위치까지 없다는 증명은 아님 |
| 실험 원자료 | 네 결과 XLSX에 관한 간접 리뷰와 일부 수치 설명 있음 | 원본 결과 XLSX4개 현지 확보 근거 없음. 전압·전류·시간·온도 원시 trace, 실험 SOP, 전극 half-cell 곡선, 실제 피팅 코드/잔차는 검토한 현지 입력에서 미확보. 결과표는 전압 trace가 아님 |
| OCP 출처 | 설치6.3 `battery_lib.mph`의 Graphite MCMB(mat35), NMC811(mat54), 전해질mat50을 내장. 재료 라이브러리 SHA `92cfd07d16fcb148ab1de4adbf48a3b9c6f709c2b8f04d9c571e4d702c4473f6` | 원본6.4/규진팀 half-cell 표와의 숫자·좌표 직접 대조 미완. 재료 이름이 같다는 것으로 동등성 인정하지 않음 |
| OCP 조성 좌표·온도 | 반응의 실제 표면 `cs/csmax`; 전역 cell SOC나 입자 평균과 다름. Eeq 온도 보정 사용, T=298.15 K. N 사용표 교집합[0,.98], P[.2228930343076256,.983245033354389], 최종 외삽none | 실험 곡선의 stoichiometry/정규화·온도·휴지 기준과 맞는지 미확인. OCP 표의 범위를 particle 평균이나 cell SOC 범위로 바꾸지 않음 |
| cmax | N31507, P50707.7 mol/m³. P 설치 라이브러리 기본50060에서 재구축 제안값으로 명시 변경. from_mat→def.csmax 소비 사슬 확인 | 과거 원본 현재편집 XML 리뷰에는31507/50707.7이 보고됨. 옛 저장해는 userdef/dm 선택이 달라 숫자만 같은 것으로 저장해 동등성 주장 불가 |
| 활성량·LAM | 두께52/25/44µm. epss0 N=.63122/P=.58803, LAM N=.0257219788/P=.0296398242. epss=epss0×(1−LAM) 한 번, 결과 N=.614983772541864/P=.5706008941756741. binder=.1, epsl=1−.1−epss | 재구축안의 열화 입력; 해당 실험 셀·cycle·적합 좌표와 실효 활성질량/면적의 대응 미확정. 결과 XLSX의 alpha/beta/LLI를 독립 직접측정량으로 승격하지 않음 |
| 초기 Li | LLI=.0439355, C_lit0_ref1=.003765381 Ah, A_cell=1.53938 cm²를 이용한 입력 재고식. 고체1.1882256785342784 mol/m², 초기 전해질약.0486772853809121 mol/m² | 입력식 및 현지 짧은 해의 재고 일관성은 있음. C_lit의 물리적 정의·용량 단위 전달·열화행 선택이 실험 시작재고를 재현하는지는 미확정 |
| 초기 상태 | N x=.01172068149, P x=.9240638866948166; 입자 초기농도 지정, 전역SOC 초기화off. cl=1200 mol/m³. t=0은 CDI/DAE 일관성 초기화 이후 | 초기 농도 균일 설정/5초 무부하 결과가 실제 실험의12시간 휴지 직후 상태를 입증하지 않음. 실험 충·방전 이력, 시작SOC·온도·휴지 길이 대응 미확인 |
| 과거3.0524 V 비교 상태 | 현지 무부하2.1653333265 V의 Eeq 산술은 완료; 새 재계산 불필요. 부하 초기전압과 무부하OCV도 구분 | 과거3.0524 V의 동일 dataset·solution·savepoint·재고·휴지/부하 상태 연결 미확정. offset·OCP·초기조성·Li 변경으로 맞추지 않음 |
| C-rate 기준 용량 | Q_areal=90129.5830315564 C/m²=25.035995286543443 Ah/m². 손상 전 P 활성분율과 지정창 .927−.215로 정한 정규화 용량 | 해석에서 얻은 가용용량 또는 실측 정격용량이 아님. .215는 현재 P OCP 하한보다 낮지만 이 식은 우선 전류 정규화 정의; 표밖 완주를 허용한다는 뜻 아님 |
| 전류·면적 | i_1C=25.035995286543443 A/m²; 0.1C inward +2.503599528654345 A/m². physics A_c=1m²이므로 모델 총전류+2.503599528654345 A. A_cell 환산약.3854mA는 기존 기록값 | A_c와 실셀면적을 혼동하지 않음. 실제 실험 cycler의 전류/용량 정의·기록과 직접 대응 미완 |
| 물성·누설 의미 | 반경 N7.5/P10µm; D_s N7.1e−15/P1e−13m²/s. 등온, D_e7.5e−11m²/s, t+=.363. 중앙 binder epss=.55/epsl=.45, 전자NoCorr의 실효sigma1e−20S/m | near-zero 기준이지 수학적무누설 아님. 원본의 sigma·Bruggeman 소비식과 정확 환산 관계 미완. epsl 기반 전극 전자전도 보정, LAM에 따른 공극 변화 및 실제 국소 쇼츠와1D 유효전도도의 정량 연결도 검증 필요 |

입력 근거: [MODEL_DECISIONS](C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/MODEL_DECISIONS.md), [최초 짧은 검증](C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/VALIDATION_RESULTS.md), [현재300 소스의 입력](C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/comsol63/core16_control/Caps300R320H0125C16.java), [원본 검색 범위](C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/inputs/original_data_inventory.json), [과거 원본/워크북 리뷰](C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/work/COMSOL63_LOCAL_HANDOFF/references/MICROSHORT_MPH_V2_CODEX_REVIEW.md), [워크북 좌표·단위의 한계](C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/work/COMSOL63_LOCAL_HANDOFF/references/mph_v2_workbooks_review.md).

확보 여부를 이번에 보강한 범위는 `outputs/inputs`·인계 폴더의 관련 파일명, `outputs/inputs/COMSOL63_WINDOWS_HANDOFF.zip`21항목, 그 안과 대응하는 `MICROSHORT_MPH_V2_REVIEW_PACKAGE.zip`17항목의 명세 확인이다. 원자료가 다른 개인 폴더에 새로 도착했는지 전역 재검색하지 않았다. 다른 PC의 리뷰가 원본을 읽었다는 사실과 현지에서 원본 바이트를 확보했다는 사실을 구분한다.

원본 비교에서 특히 중요한 것은 **현재 편집 모델과 저장해 모델의 분리**다. 과거 리뷰는 `pg19→dset1→sol1→savepoint6`에 연결된 저장 모델이 현재 XML과 다른 활성분율·cmax 선택자·초기농도 및 P초기x(.9189896)를 가졌다고 기록한다. 현재 선택입력의 P x≈.924064와 그 저장해를 섞어 검증하지 않는다. 다음 정량 대응에는 원본 파일 SHA, 대상 dataset/solution/savepoint, 대상 실험 셀/cycle/시작 상태가 한 묶음으로 필요하다. 이 연결이 없으면 이미 설명된 초기전압 산술을 반복해도 미완이 해소되지 않는다.

## 4. 장기 실행 전 준비도: 구현됨 / 시험됨 / 미완

각 칸은 서로 다른 질문에 답한다. 구형 사전진단에서 구현·시험된 기능이 현행300/320 고정전류 모델에 이미 통합됐다는 뜻은 아니다.

| 항목 | 구현됨 | 시험됨 | 미완 |
|---|---|---|---|
| 초기화·Eeq·재고 | 명시 초기농도, CDI, cmax/OCP 소비 사슬, Li 적분 | 무부하·부하5초와 후속 수치 진단. 초기2.1653 V 분해 완료 | 실제 원본/실험 시작 상태 대응; pre-CDI 값과 반환t=0 혼동 금지 |
| OCP/고체 표면 보호 | 현재300/B에 최종4함수 extrap=none, StopCondition 한 노드·활성2조건. N/P 공간 표면 extrema 사용 | 별도75/10 경계fixture `08e0fc5d41e147678f3940e98100ec12`에서표면 이탈 감지·정지 | 모든 Newton trial/연속 공간의 사전 차단 아님. P OCP/entropy 교집합 외 목표 실행 불가 시 미완으로 종료. N 양끝/P다른경계 등 모든 분기의 강제발동 시험은 미확인 |
| 전해질 농도 | 전체3domain `cl` MinLine/MaxLine 내보내기 및 양수 **후처리 검사** | 기존5초 표본에서 양수. B 최소약1194.4372mol/m³ | **현재 StopCondition에 cl 조건 없음. 실행 중 감시·중단 배선/발동 시험 누락** |
| 입자 내부 농도 | 최초 short 소스에 cs_center·cs_average·cs_surface extrema 출력. 현행300/B는 표면·평균 프로파일 중심 | 최초75/10에서 중심/평균/표면의 표본 검사 | 현행R320 전 내부 반경(z,r) min/max 관측·농도상한/하한 중단 근거 없음. 중심·평균·표면3개만으로 내부 극값 보호 완료라 하지 않음. 추가차원 관측 지원 API/평가 범위 확인 후 별도 구현·시험 필요 |
| 첫 충전·2.7 V 적용 범위 | 사전진단 CDC가 boundary4를 단독 소유; ecd1 제거, Charge_first, Vmin 방전 조건 | CdcStart5s: 초기 부하V≈2.2306<2.7에서도 양의CC충전5초 유지 | 실제2.7 V에서 방전 종료하는 장기 실행은 아직 없음. 현행300/B에는 CDC 생성 없음; 향후 통합 검증 필요 |
| CC→CV→휴지→방전 | 별도 CDC fixture, Vmax2.24/Vmin2.10, cutoff .08C, 휴지2초 | PreflightCdcEvents20s에서 .184572751532/.457403699045/2.45740569904초 전이, 첫cycle2.62420555994초 완료 | 실제4.25 V/.01C/12h 경로는 미검증. 재사용할 작동 근거가 있으므로 “모든 전이 미착수”로 쓰지 않음 |
| 사건 허용오차·첫cycle종료 | fixture eventtol1e−6, cycle_counter>.5, eventout 및 정지전후저장 | 휴지2.000002초, 방전종료 오차약9.7713e−5mV. 끝행은 다음충전의 재초기화 상태; 두번째cycle 양의시간 적분 아님 | 이 오차를12h에 외삽 불가. 300/320 통합시 eventtol·종료원인·전후행/재초기화 취급을 명시하고 확인해야 함 |
| 실제 목표 설정 | CdcStart에4.25 V/.01C/12h/2.7 V 설정 자체는 있음 | 첫5초 충전 시작만 시험 | 표내 평형상한4.185562 V는 유한전류4.25 도달 불가능 증명도 CV완수 보장도 아님. OCP범위 중단과 정상cycle완료를 분리할 장기 종료 계약 필요 |
| 시간·출력 제어 | 고정전류5초: expr/strict/전체accepted저장. 별도CDC short: const .05초와 eventout | 기존300 후기cap 민감도 및 B accepted이력; short eventtol 비교 | phase별 장시간 cap/rtol·출력 간격·사건 주변 정밀도·데이터량 제한을 통합한 모델 없음. 단순 tlist 연장/12h에 .1초 복사 금지 |
| 오류·미완 분류 | 기존 worker 실패와 후처리 물리판정 분리, 범위실패 산출물 보존 | 범위fixture는 raw failed/후처리 Nonfinite point4, 과학분류 INCOMPLETE_RANGE_STOP | 새 전해질/입자 내부 실패·시간예산·solver 실패마다 다른 원인 기록 필요. batch rc0만으로PASS 불가 |

CDC 근거는 [사전 진단 결과 4절](C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/preflight/PREFLIGHT_RESULTS_KO.md), [독립 소스·실행범위 감사](C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/preflight/INDEPENDENT_PREFLIGHT_AUDIT.md), [job 식별](C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/preflight/jobs.json)이다. 현재 source에는 불사용 CDC 관련 문자열/분기가 남아 있으나 실제 run의 boundary4는 ecd1이고 CDC를 생성하지 않는다. 따라서 코드에 `cdc1` 문자열이 있다는 사실만으로 통합 완료로 세지 않았다.

최초 MODEL_DECISIONS/VALIDATION_RESULTS의 “CDC 미구현·전이 미검증” 표현은 그 문서 작성 단계의 기록이다. 뒤의 사전진단은 일부를 완료했다. 반대로 최근 NEXT_RUN_PLAN의 장기 배선 미완은 **짧은 CDC/2.7 V 시작 시험을 처음부터 반복하라는 뜻으로 해석하지 않는다.** 이 문서는 이전 기록을 변경하지 않고 시점·대상 모델별 범위를 구분한다.

COMSOL의 최대step, strict 요청시각, 저장 설정은 서로 다른 제어다. 특히 strict는 요청시각에step을 두지만 사이step도 가능하며, accepted저장과 출력보간 설정은 별개다. 장기 제어 설계는 이 구분을 유지해야 한다. [공식 시간간격 안내](https://www.comsol.com/support/knowledgebase/1254). StopCondition은 step 뒤의 조건 평가이지 연속 모든 시각의 양수성을 보장하는 장치가 아니다. [6.3 StopCondition API](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_api_solver.51.47.html). CDC는 전압/전류에 따른 cycling 경계 기능이다. [6.3 CDC](https://doc.comsol.com/6.3/doc/com.comsol.help.battery/battery_ug_electrochem.07.060.html). 공식 자료는 동작 의미의 근거이며 이 프로젝트 작업 순서의 권고는 위 현지 증거에 따른 판단이다.

## 5. 가장 먼저 할 구체적 작업 한 건 — 사용자 승인 대기

**조건: 다음 목적을 provisional 기능 진단으로 사용자가 선택할 때, 300/320 C16 복제본에 전해질 농도 감시·중단 기능을 추가하고 정상/강제트리거의 제한된 기능시험을 수행한다.** 기존 CDC 전이 시험이나 C를 반복하는 작업이 아니다. 현재 후처리 전용인 cl 검사를 solver 중단 사슬에 연결하는 누락 한 건을 해소한다.

종류는 **코드 변경 + 검토 + 새COMSOL solve 최대2회**를 제안한다. 이번에는 이 중 아무것도 시작하지 않았다. 두 solve는 동일 변경의 비발동/발동을 구분하기 위한 것이며, 자동 재시도는 포함하지 않는다.

| 항목 | 승인받을 구체안 |
|---|---|
| 기준 해 | 기존 Caps300R320H0125C16 / job `5d1a87652ed54e6a945d4f2af4aeda70` / 위 SHA `4db47e27…02537e`. 재실행 없이 재사용 |
| 변경 축 | 전체3domain 전해질 cl의 공간 최소값을 읽는 solver 감시·중단 조건만 추가. 관련 관측/종료원인 출력과 식별 이름은 명시 변경. OCP·표면 guard는 유지 |
| 고정 | physical300(120/60/120), 입자320/320,16코어, t=0 동일 초기화, 0.1C, sigma1e−20S/m, 물성·반경·초기조성·재고·OCP·scale·rtol1e−6·initialstep1e−5. cap `if(t<0.1[s],0.000125[s],0.1[s])`, 기존187요청시각/241좌표 및 저장설정 유지 |
| 정상 경로1회 | 상한5초. 검사 하한=0mol/m³로 두어 cl≤0 중단 판정을 추가한다. 기존 양수 농도 범위에서 미발동하는지와 기존 해 대비 차이를 확인한다 |
| 발동 경로1회 | 같은 모델·초기화·물리입력, **검사 임계값만1198mol/m³로 올린 테스트 fixture**. 기존 cl 초기1200/5초최소약1194.4372 기록상5초안 발동을 기대한다. 결과를 보고 임계값을 재조정하지 않음 |
| 임계값 의미 | 1198은 물리적 고갈 한계·생산 설정이 아닌 배선 시험값이다. 실제 농도를 음수로 강제하거나 초기Li를 바꾸지 않음. 정상경로0 기준도 모든 Newton trial의 유효성을 보장하지 않으며 장기 보호 여유한계 확정은 별도 |
| 정상 성공 | 실제 domain1/2/3 감시 배선·조건/단위 되읽기, cl/OCP 표본 유효, 해당 중단 미발동,5초완료. 기존187요청 및 정확 공통저장별 최대 ΔV≤1mV/pointwise Δx≤1e−4; 공통 수는 미리 고정하지 않음. 예기치 않은 accepted 이력/비교차이도 숨기지 않고 기록 |
| 발동 성공 | named 전해질 조건이 실제로 발동; 저장된 직전step은 검사 임계 위·정지step은 이하임을 같은 평가 정의로 확인, 발생domain/시각/cl 기록. 정지 후 양의시간 진행 없음. 물리완주PASS가 아니라 **TEST_TRIGGER_DETECTED**로 보고 |
| 실패/미완 |5초안 트리거 없음, 다른 조건 우선 발동, 비유한/solver 오류, 단위/감시범위/전후값 확인 불가이면 기대 기능시험 미완/실패. 원인을 그대로 기록하고 자동 재시도·임계값/물성 변경 없음. INCOMPLETE_RANGE_STOP으로 자동 재분류하지 않음 |
| 시험 해석 | 공간 extrema의 평가점 정의와 solverstep후 검사 한계를 명시. 양수 임계값으로 강제한 한 번의 발동은 각domain의 개별발동, 실제cl=0접근시solver거동, 거부된trial 또는 연속공간 보호를 모두 시험한 것이 아님 |
| 자원·추론 |16코어, 각 job 벽시계 대기한도1800초를 제안(총solve 최대2회); 원래300 job 약942초 관측을 참고한 여유이지 완료 보장 아님. Astra High: 단일 보호 변화·종료원인·수치 비간섭 확인이 필요. 승인 후 도구허용범위/timeout 의미/RAM·저장 여유 확인 |
| 진행 제한 | 각 제출 전에 동일 조건 완료/진행 job 확인. 불명확하면 중복 제출 금지. 첫 정상 경로 실패·필수 검사 미완이면 두번째도 시작하지 않고 회신. 모든 구현·시험은 별도 파일에, 원본불변 |

이 한 건으로 해소하는 것은 **후처리에서만 보던 전해질 농도 조건의 solver 중단 배선과 제한된 비발동/발동 근거**다. 해소하지 못하는 것은 원본/실험 대응, 실제 고갈점의 강건한 처리, 입자 내부 보호, 300/320에 CDC/장기 시간제어 통합, 모든 단계·실제4.25 V/.01C/12h 운전, 전체 수렴 및 유한쇼츠 정량 정확도다.

위2회 제안은 사용자에게 선택 가능한 구체안이며 이번 승인에 포함되지 않는다. 만약 다음 목적이 **실제 셀 정량 해석**이면 이 구현안을 보류하고 원본 파일+실험 셀/cycle/프로토콜/trace/OCP 좌표의 대응 자료 확보를 먼저 선택해야 한다. 자료가 확보되지 않은 상황에서 C 또는 보호 시험 성공으로 정량 해석을 승인하지 않는다.

## 6. 이번 종료 상태

이번 산출물은 이 결정 문서 한 건이다. 기존 실패·INCOMPLETE_RANGE_STOP·원본을 유지하고, OCP 외삽 금지·전해질 양수 후처리라는 **현재 구현 상태**를 변경하지 않았다. TIME_CAPS raw ZIP 차이 원인 미확인도 유지한다. 추가 메시/시간반감, 보호구현/기능시험, 전체 프로토콜·12시간휴지·유한sigma·sweep은 모두 별도 승인 대상이다.

다음 결정은 **provisional 기능 진단을 우선할지 사용자 확정 → 동의 시 위 전해질 보호 한 건의 구현·2회 제한시험을 별도 승인**이다. 현재는 승인 대기이며 어느 solve도 제출하지 않는다.
