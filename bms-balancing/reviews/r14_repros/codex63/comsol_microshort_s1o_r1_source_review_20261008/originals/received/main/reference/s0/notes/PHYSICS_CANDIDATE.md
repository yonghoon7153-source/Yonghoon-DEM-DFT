# 물리 / Java 정적 검토 메모

기준: pinned commit `fd7ce941a7c4d3989f80a133271189d67a6a0074`. 직접 읽은 Java는 `sources/Normal480Candidate.java.txt` (99,959 B, SHA256 `c70526cf6884eabc57b63dd43dce4b47fb0decf59af68d3f550f1b987d053797`)다. 이름은 source480이고 입자는 320/320이다. 상위 폴더 이름 particle640은 이 원본을 640으로 만들지 않는다. Java/분석 프로그램 import·실행·compile·COMSOL·JVM·native는 0이다.

## 1. 실제 설정과 원 설계의 차이 — 확인

| 항목 | 실제 NORMAL480 직접 증거 | 결론 |
|---|---|---|
| 1D 형상 | Java 587, 610–615: N52/sep25/P44 µm, Interval | x는 음극→양극; domain 1/2/3, boundary 1/2/3/4 |
| 모델 면적 | 588, 639–640: A_c=1 m², A_cell=1.53938 cm² 별도 | A_c는 1D 모델 전류 환산용. 실험 면적의 확정 증거 아님 |
| 분리막 | 646–652: PorousConductiveBinder domain2; epss_short=1-epsl_sep (594), epsl_sep=.45 (593), NoCorr, isotropic sigma | 실제 epss=.55. SPEC 197의 epss=1을 현재 소스의 사실로 쓰면 안 된다. READY 56도 .55 확인 |
| 전자전도 | 651–652: NoCorr/userdef/diag(sigma_short); 607의 1e−20 S/m | 전자 실효전도에 .55^1.5 또는 .45^1.5를 또 곱하지 않음. near-zero는 수학적 0이 아님 |
| 경계 | 653–658: ElectricGround at1; ElectrodeNormalCurrentDensity at4, nis=i_app | 실제 0.1C CC 경계. SPEC 206–218 CDC/4.25V/12h는 원 설계. Java CDC 참조는 450의 if(false) 안 |
| 초기재고 | 589–603 | LLI=.0439355, LAM_NE=.0257219788, LAM_PE=.0296398242는 이미 입력된 상수. 정상=누설 near-zero, 무열화 셀 아님 |
| 입자와 농도 | 89–101, 641–645: explicit csinit, csinit=x_init*csmax; SOC/InitialChargeInventory off; cl=1200 | x_Gr_init 한 개를 고르고 x_NCM_init을 nLi_target 식으로 종속 설정하면 고체 총 Li 동일 |
| 실제 확산 | 70–74, 94, 596–599 | Dg=7.1e−15, Dp=1e−13, De=7.5e−11 m²/s, rpN7.5/rpP10µm, t+=.363. 내장 재료 확산표의 값으로 바꾸어 계산하면 안 됨 |
| 온도·OCP | 90,97,598; 142,151,159; NMC Eeq/dEeqdT 표; 619–622 | 298.15 K. OCP에는 298 K 기준 엔트로피 보정 .15K 포함. 외삽 none 유지 |
| mesh | 660–661,674 | 입자 320/320, 공간120/60/120 |
| 시간·저장 | 398–407,681–682 | 실제 solver rtol1e−6가 study rtol1e−5 뒤 덮어씀. cap .000125s(<.1s) 후 .1s; strict; tout=tsteps; tstepsstore=1 |
| 초기화 | 678; 391–431 | CDI 생성, type 속성은 명시하지 않음. auto sequence 후 transient consistent 기본값을 runtimeSettings로 읽는 구조 |

위 차이는 기존 수용을 재개방하는 결과가 아니다. S0 요청이 원 설계의 설명을 현재 소스와 같다고 가정한 두 지점을 바로잡는 일이다. epss를 1로 바꾸는 것은 이 후보에 포함하지 않는다.

## 2. 좌표·부호를 정한 지배식 — 원문에서 유도

x=0을 음극 집전체, x=L을 양극 집전체로 둔다. j_F는 산화/탈리튬 반응이 양(+)인 면적당 Faradaic 전류밀도이고 a_s는 체적당 활성 표면적이다.

- 전극: i_s=-sigma_eff ∂phi_s/∂x, ∂i_s/∂x=-a_s j_F; ∂i_e/∂x=+a_s j_F. 따라서 ∂(i_s+i_e)/∂x=0.
- 전해질: i_e=-kappa_eff ∂phi_e/∂x+(2RT/F)kappa_eff(1-t_plus)chi ∂ln(c_e)/∂x. chi는 사용 재료 활동도 미분 항이고 임의로 1이라 놓지 않는다.
- 정적 공극률 하의 염 수지: eps_e ∂c_e/∂t=∂(D_transport ∂c_e/∂x)/∂x+(1-t_plus)a_s j_F/F. 여기 D_transport는 COMSOL 식에 실제 소비되는 보정 포함 계수다. 소스 fDl=epsl^b만으로 별도 epsl 곱의 중복 여부를 단정하지 않고 방정식 export와 일치시킨다.
- 구형 입자: ∂c_s/∂t=D_s r^−2 ∂(r²∂c_s/∂r)/∂r, 중심 ∂c_s/∂r=0, 표면 -D_s ∂c_s/∂r=j_F/F. a_s=3eps_s/r_p는 구형 ParticleBasedArea의 기하학적 표현이다.
- 분리막에는 삽입 반응이 없다: ∂i_s/∂x=∂i_e/∂x=0, i_s=-sigma_short ∂phi_s/∂x. phi_s/P>phi_s/N일 때 관습 전류는 분리막에서 P→N(-x), 전자는 N→P(+x).
- 휴지 외부 경계: phi_s(0)=0, i_s(L)=0; 전해질은 집전체에서 이온 전류/염 flux 0, 내부 경계는 연속. 따라서 분리막 i_e=-i_s=j_leak>0.
- j_leak=-mean_sep(i_s)=sigma_short[phi_s(77µm)-phi_s(52µm)]/L_sep. 균일·상수 sigma, source-free separator에서 성립한다. 이것을 집전체 단자 V=phi_s(121µm)-phi_s(0)로 대체하면 전극 전자 저항 강하를 빠뜨린다.
- R_N=∫_N a_s j_F dx=j_leak, R_P=∫_P a_s j_F dx=-j_leak. dn_N/dt=-j_leak/F, dn_P/dt=+j_leak/F. 전체 전극 고체 Li 및 폐쇄 전해질 Li 합 보존. 전해질 국소 농도는 변해도 전체 염 수지는 경계 flux와 총반응으로 정해진다.

전자 누설을 나타내는 항은 Li를 없애는 sink가 아니다. 기존 LLI 입력은 시작 재고의 감산이고 시간 진행 중 SEI/도금/죽은 Li 생성식이 아니다. 완전 재충전 후 용량 회복 여부는 동일한 cutoffs/전류/종료 정책으로 비교해야 하며, 강한 단락이 충전 완료를 못 하거나 휴지 중 OCP 범위를 벗어나면 '회복 불가'처럼 보일 수 있다. 고정 sigma 모델에 누적 LLI/LAM 성장식은 없다.

전하/질량식 계열은 [COMSOL 6.3 lithium-ion theory](https://doc.comsol.com/6.3/doc/com.comsol.help.battery/battery_ug_electrochem_battery.06.60.html)와 [interface description](https://doc.comsol.com/6.3/doc/com.comsol.help.battery/battery_ug_electrochem_battery.06.02.html)로 교차 확인했다. 위 부호·적분식은 현재 geometry/반응구조에 대한 독립 유도다. 기본 경계/구형 입자/계수 소비식은 S1 전 exported equations/readback 검증을 요구한다.

## 3. '균일 평형에서 휴지'의 정확한 뜻

무누설·무전류 상태라면 균일 xN,xP,ce에서 phi_s,N=0, phi_e=-U_N, phi_s,P=U_P-U_N가 가능하다. 유한 sigma를 t=0부터 연결하면 전위차가 있는 상태는 전류를 흘리므로 **엄밀한 평형이 아니다**. 정확한 명칭은 '같은 균일 농도에서 시작한 자기방전 초기값 문제'다. 각 sigma에서 초기 농도·온도·재고는 같고 대수 전위는 전류 연속 조건을 만족하도록 달라져야 한다.

[COMSOL 6.3 CDI 설명](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_ref_solver.36.055.html)은 CDI가 농도를 초기값에 고정하여 전위를 풀며 기본 Primary가 평형전위 제약을 쓴다고 명시한다. 따라서 현 소스처럼 type을 명시하지 않은 CDI의 성공만으로 유한 sigma의 nonlinear 반응 전류가 일관적이라고 단정할 수 없다. transient consistency 및 반응/누설 적분 잔차를 확인해야 한다. Secondary CDI를 대안으로 검토할 수 있으나 속성 키와 설치본 기능 증거 없이 후보에 새 API를 넣지 않는다.

휴지 후보는 ecd1 nis=0을 쓰면 되고 새 CDC·이벤트·스위치가 필요하지 않다. 모든 sigma의 농도를 새로 만들므로 기존 480s 충전 이력의 불균일을 우회한다. OCP plateau에서는 실제 Li 이동이 작지 않아도 V 변화가 작을 수 있다. xN가 0에 가까운 원 시작점은 기울기는 크나 OCP 경계·초기 확산·비선형 오염이 커, 중간 표내 조성을 선택할 이유가 있다. xN=.5 같은 큰 기울기 변화 knot를 정확히 시작점으로 쓰면 한쪽 기울기 문제가 생길 수 있어 부모 계산이 고른 knot 사이 값을 따른다.

## 4. 출력 필드 — 실제 존재 증거

| 관측량 | 현 Java 실제 식/라인 | 단위·주의 |
|---|---|---|
| 누설 전류밀도 | 439: `-comp1.intd2(comp1.liion.Isx)/L_sep`; 440 header `leak_leftward_A_m2` | 이미 출력됨. 길이 적분 단독은 A/m이며 I가 아니다. L_sep로 나눈 뒤 A_c를 곱해야 모델 전류 A |
| 반응 적분 | 439: `comp1.intd1(comp1.liion.ivtot)`, domain3 동일 | A/m²; rest에서 RN≈j, RP≈−j를 검사 |
| 고체 Li | 436: `intd1(liion.epss*liion.cs_average)`, domain3 동일 | mol/m² |
| 전해질 Li | 437: 세 domain의 `intd(epsl*cl)` 합 | mol/m² |
| 전극 평균 조성 | 438: `intd1(cs_average)/(L_el*cs_Gr_max)` 등 | 일정 epss·csmax라 부피 평균과 재고 기반 평균 동일 |
| 표면 조성 | 386–387/439: `liion.socloc_surface` min/max, 552 local profile | 입자 평균과 구분 |
| 전위·반응 | 445–447: `phis`, `phil`, `liion.Eeq_per1`, `liion.eta_per1`, `liion.etamid_per1`, `liion.Isx` at collectors | 단자 V는 point4.phis−point1.phis. sep Δphi는 기존 integration of phis derivative 또는 새 boundary2/3 전위 전용 EvalPoint로 별도 추출 |
| 공간 프로파일 | 552,560–574: 두 전극241점/각 stored time, FE interpolation | 시간 interpolation off는 결과 Interp 설정이며 solver 저장보간 정책과 다름 |

I_leak(t)=A_c*j_leak(t). A_cell*j_leak는 실험 대응 미확정 상태에서 물리적 셀 전류라고 주장하지 않는다. 부호 확인은 -sigma*phi_s gradient 및 RN/RP와 독립 대조한다.

## 5. 저장·cap 변경의 서로 다른 의미

원본은 tout=tsteps 및 tstepsstore=1이므로 요청 tlist만 줄여도 모든 accepted step이 저장된다. 동시에 maxstep=.1 s이면 1h에 최소 약36,000 step이 남는다. 저장 축과 step 축을 따로 검증해야 한다.

[COMSOL 6.3 Time API](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_api_solver.51.50.html)는 tout=tlist와 tstepsbdf=strict를 문서화한다. 전자는 요청 시각 출력을 뜻하고 후자는 실제 step이 요청 시각을 포함하도록 한다. 후보는 strict를 유지해 공통 요청 시각을 고정한다. 설치본에서 실제 accepted/stored time readback이 필요하며 일반적으로 tout=tlist는 '보간 출력' 정책이므로 postprocessing timeinterp=off만으로 시간 보간 부재를 주장할 수 없다.

후보는 full solution field 보존을 택한다. 선택 변수만 저장하는 새 API는 삽입하지 않는다. CSV 열 축소는 MPH state field 축소와 다르며 물리 검증을 위해 입자/전해질 상태를 유지한다. 이 정책이 표본 수에 비례해 파일 크기를 줄일 것이라는 것은 추론이며 저장량 보장은 아니다.

## 6. S1 전/중 검증이 필요한 미확인 지점

- 실제 CDI type, transient consistent 옵션과 유한 sigma 초기잔차.
- current field/관측식은 기존 source에 있음. 새 rest·유한 sigma에서의 단위/readback와 부호는 아직 실행 검증 없음.
- 요청-only 저장 API는 문서 확인이나 local 6.3 runtime 기능·시간 동일성은 미확인.
- source-only geometry 식에서 eps_s와 transport fDl가 생성 방정식에 어떻게 결합되는지는 기존 equation export를 읽어 확정; 현재 구조를 몰래 수정하지 않음.
- 새 시작 SOC에서 장기 입자/공간/rtol/cap 민감도는 미확인. 기존 120–150s 충전 입자 민감도를 이 조건의 error floor로 재사용 금지.
- terminal zero current는 상대오차를 j≈0 baseline로 나눌 수 없음. 반응 잔차/보존은 절대 물리 단위와 전역 스케일을 함께 써야 함.
- finite sigma 진짜 t=0 전압 기울기는 DAE consistency·표면 확산 응답 영향. reduction의 dV/dt는 mean-state OCV prediction이라는 라벨 필요.

## 7. 후보 방식

candidate 디렉터리에 실행 불가 확장자의 full source, review-only diff와 변경표를 둔다. COMSOL 호출 전에 무조건 거부하는 entry guard도 둔다. 실제 실행본은 사용자 별도 승인 뒤 change-limited 검증·수신 검토·실행 승인 절차에서 새로 고정해야 한다. 기존 launcher/consumer/contract는 480s·기존 dense grid 계약을 가지고 있으므로 그대로 연결하면 안 된다. 이번은 Java 후보이며 실행 패키지가 아니다.

최종 제안값은 xN=.445, xP=.5811516557009895 (동일 nLi_target), OCV=3.72372150634V이다 (부모 오프라인 산술). sigma1e−20/1.7e−8/1.7e−7/1.7e−6 S/m, T3600s,401 요청시각, strict/tout=tlist 및 부모 cap schedule을 반영했다. 후보의 기본 sigma는 단일1.7e−7이고 native/sweep 코드는 비활성이다. full source77,277B SHA256 a90d1e66db796f6b8077fa1d158620d1ec548265a1508b698e35da8ef6e3492c. 원본 대비 unified diff42,205B SHA256 ae8d8246e010b8bdb310e03e34d2bfcb6bc506922c5a9ee9d1e8949b06b52791. 실제 실행은0이다.
