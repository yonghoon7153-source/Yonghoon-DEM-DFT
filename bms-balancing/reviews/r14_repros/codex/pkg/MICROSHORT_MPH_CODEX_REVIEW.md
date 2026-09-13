# 마이크로 쇼츠 COMSOL 분석 문서 검토

검토일: 2026-09-13. 요청문: `REQ_MPH_MICROSHORT.md`.
대상 커밋: `94add7b5d48ad5d19448d562a0909b15ce4dc056`.
분석 문서가 들어온 `26c477c8` 이후 해당 문서의 변경은 없다.

## 판정

**현재 분석 문서를 확정 진단과 수정 지시서로 채택하는 것은 NO-GO다.**

M1의 핵심 산술은 맞는다. 주어진 좌표와 선형 OCP 구간을 사용하면 셀 OCP 차이는
**−14.274885 mV**, 음극/양극 호스트 사이트 감소는 **5.078234% / 5.840113%**다.
그러나 이 사실에서 **“csinit에 dm을 빠뜨린 버그이며, cEeqref 두 줄을 먼저 고쳐야 한다”**는 결론은 나오지 않는다.
반응 OCP의 실제 입력 경로와 초기화 경로가 증명되지 않았고, 같은 식을 만족하는 의도적 모델도 존재한다.

따라서 **M1 전체가 거짓이라는 판정은 아니다.** 확인된 식, 조건부 영향, 미확정 설계 의도를 분리해야 한다.
이 판정은 COMSOL 모델 자체가 올바르다는 승인도 아니다.

원본 `.mph`, `dmodel.xml`, 네 `.xlsx`는 이번 검토에서 확보하지 못했다. COMSOL 실행은 0회다.
저장소 문서 574행, 첨부 요청문, 공식 COMSOL 6.4 문서와 1차 연구를 대조하고, 첨부 숫자로 독립 산술 및 논리 반례를 실행했다.
하네스 회귀시험은 이 분석의 진위를 입증하지 않으므로 이번 작업에서 재실행하지 않았다.

## 1. M1: 무엇이 남고 무엇이 무너지는가

| 주장 | 판정 | 이유 |
|---|---|---|
| A1: 입자 SOC는 cs/cs,max | 일반 정의는 확인 | COMSOL 이론이 정의한다. 그러나 반응 Eeq의 실제 인자가 그 SOC인지는 별도 설정이다. |
| A2: 초기 입자 SOC=x/dm | 조건부 성립 | 해당 cmax 설정과 csinit이 실제로 선택되고, 저장해 등 다른 초기화가 없어야 한다. |
| A3: 사이트가 약 (1−LAM)² | 조건부 성립 | 정확히는 (1−LAM)×dm. 전체 호스트 용량에 대한 식이며, 전압 한계 사이 단자 Ah 감소율과 같지는 않다. |
| A4: dm 없는 csinit은 누락 버그 | **입증 실패** | 의도적 부피·사이트 밀도 동시 감소 + 독립 Li 재고 지정 모델이 모든 인용 식과 양립한다. |
| A5: Li 수지는 맞음 | 범위를 좁혀 성립 | 인용된 활성 고체 Li 재고의 대수적 항등식이다. 전체 원소 수지·실측 c_lit의 정의·실제 초기화까지 입증한 것은 아니다. |

### 1.1 cEeqref의 의미와 반응 OCP의 소비 경로는 구분해야 한다

COMSOL 6.4 이론은 `cs,max`를 총 반응 사이트 농도로 설명하고 입자 SOC를 `cs/cs,max`로 정의한다.
그러므로 “cmax는 사이트 수와 무관하다”는 방향으로 A3를 깨는 것은 맞지 않는다.
공식 예제에서도 재료의 `cEeqref`는 최대 리튬 농도로 명시된다.
[공식 이론](https://doc.comsol.com/6.4/doc/com.comsol.help.battery/battery_ug_electrochem_battery.06.63.html),
[cEeqref 설명](https://doc.comsol.com/6.4/doc/com.comsol.help.models.battery.li_battery_1d_for_thermal_models/li_battery_1d_for_thermal_models.html).

하지만 **Porous Electrode Reaction의 Eeq에는 별도 From material/User defined 설정이 있다.**
공식 1D 예제는 `Eeq_neg(liion.cs_surface/csmax_neg)`를 사용자가 직접 입력한다.
이 경로에서는 입자 노드의 cmax와 다른 파라미터로 정규화할 수 있다.
`pin1.cEeqref=dm*csmax`만으로 모든 Eeq가 반드시 `x/dm`을 읽는다고 결론 낼 수 없다.
[공식 1D 예제의 반응 설정](https://doc.comsol.com/6.4/doc/com.comsol.help.models.battery.li_battery_1d/li_battery_1d.html).

정적 반례는 다음처럼 간단하다. 인용된 `epss`, `pin1.cEeqref`, `csinit`을 그대로 두고 활성 반응식을
`Eeq_table(cs_surface/csmax_pristine)`로 설정하면 입자 점유율은 x/dm이지만 OCP 표는 x를 읽는다.
**실제 원본이 이 설정이라는 주장은 아니다.** 제공된 증거만으로 배제되지 않는 COMSOL 지원 설정이므로,
원본 `per1`→선택 재료→함수 인자까지 확인해야 한다.

### 1.2 “미사용 cs_NCM_init이 있으므로 누락”의 논리 반례

전극 i에 대해 f=1−LAM, d=dm이라 두면 인용된 모델은 다음과 같다.

\[
\epsilon_i=\epsilon_i^0 f_i,\quad c_{max,i}=c_i^0d_i,\quad c_i(0)=c_i^0x_i.
\]

“접근 가능한 활성 부피는 f배, 남은 재료의 유효 사이트 밀도는 d배, 활성 Li 재고는 별도 nLi_target으로 지정한다”는
현상론적 모델에서는 x가 pristine 최대농도에 대한 농도 좌표다. 현재 점유율이 x/d인 것은 의도와 일치한다.
초기 점유율 0.01203012와 0.95228958은 모두 0–1 안에 있다.
미사용 `cs_NCM_init`은 과거 시도나 폐기된 초기화 대안으로도 설명된다.
**그 변수의 존재는 실수의 단서이지만 유일한 의도를 증명하지 않는다.**

반대로 외부 계약이 “입력 LAM은 전극 전체 호스트 용량 감소율이고 이를 한 번만 적용한다”이면 목표는
`H/H0=1−LAM`인데 현재 구현은 `(1−LAM)×dm`이므로 그 계약과 불일치한다.
이 조건이 확인되면 epss-only 수정은 합리적이다. 그래도 “csinit을 잘못 입력했다”라는 특정 원인까지 정해지는 것은 아니다.

### 1.3 산술은 재현되지만 x_NCM_init의 독립 검산은 아직 불가능하다

실행: `python outputs/mph_review_checks.py`.

| 양 | 독립 계산 |
|---|---:|
| 음극 x/dm | 0.012030119996 |
| 양극 x/dm | 0.952289581792 |
| 음극 OCP 변화 | −4.539982 mV |
| 양극 OCP 변화 | −18.814867 mV |
| nominal OCP 차 | 3.052365171 V |
| rescaled OCP 차 | 3.038090286 V |
| 둘의 차 | **−14.274885 mV** |
| 음극 호스트 사이트 감소 | 5.078234% |
| 양극 호스트 사이트 감소 | 5.840113% |

**여기서 0.92406389는 계산 입력으로 받았다.** 요청문에는 이 값을 Li 수지식에서 다시 구하는 데 필요한
`LLI`, `C_lit0_ref1`의 숫자가 없다. 따라서 이 x값을 독립 도출했다고 말할 수 없다.
제시된 x로 역산하면 활성 고체 Li 재고 1.188225683 mol/m², dLi 0.040097733 mol/m²가 암묵적으로 요구된다.
이 역산은 원자료 확인을 대신하지 않는다.

### 1.4 수정안에도 보존량 선택이 필요하다

문서 350–373행의 epss-only안은 nLi_target을 유지하면서 호스트 용량 해석을 바꾸는 **모델 선택**이다.
남은 입자의 cmax는 일정하고 활성 물질 접촉/부피만 감소한다고 가정할 때 적절하다.
실제 COMSOL 열화 예제도 활성 부피분율 감소를 사용하지만, 전해질 부피분율 유지와 확산계수 변화를 별도로 설정한다.
LAM을 “입자 수 감소” 하나로 정의하거나 공극률 변화를 자동 추론해서는 안 된다.
[COMSOL LMO 열화 예제](https://doc.comsol.com/6.4/doc/com.comsol.help.models.battery.lmo_decomposition/lmo_decomposition.html).

두 전극 csinit에 dm만 곱하면 인용된 x를 유지하는 한 Li 재고가 **0.035172528 mol/m²,
현재 재고의 약 2.9601%** 더 줄어든다. 따라서 “짝을 맞추자”도 자동으로 보존적인 수정은 아니다.

또 369–370행의 cmax-only 대안에서 **BOL 기준 nLi_0까지 aged dm으로 바꾸라는 부분은 수정해야 한다.**
BOL 재고를 고정하고 다음처럼 현재 점유율을 풀면 된다.

\[
\theta_{p,0}=\frac{nLi_0-dLi_{LLI}-\epsilon_n^0 L_n c_n^0d_n\theta_{n,0}}
{\epsilon_p^0L_pc_p^0d_p},\qquad c_{i,init}=c_i^0d_i\theta_{i,0}.
\]

nLi_0의 기준까지 바꾸는 것은 보존을 위해 필수인 작업이 아니라 기준 재고의 재정의다.

## 2. 문서 자체에서 새로 확인된 결론 과장과 오류

### 2.1 20–22, 181–184행: OCP 재표본화를 실제 충전 곡선·ICA 피크 변화로 확대했다

요청문은 solution 비교를 하지 않았다고 정직하게 신고한다. 그러나 원문 요약은 충전 구간 전체의 셀전압과 ICA 봉우리 위치가
그만큼 바뀐다고 단정한다. 제시된 −5~−20 mV는 **고정된 양극 x에서 OCP 인자를 재정규화한 값**이다.
셀전압에는 음극 OCP, 두 전극의 x(q), 과전압, 확산 및 CC/CV 제어가 함께 들어간다.
특히 최대농도 변경은 삽입 반응의 자유 사이트·반응속도에도 영향을 줄 수 있으므로 “OCP 눈금만 틀렸다”도 너무 좁다.

고칠 문구: “인용된 정규화가 활성 Eeq에 사용된다고 가정하면 초기 평형 OCP 차가 −14.27 mV다.
충전 해와 ICA 피크의 변화량은 미검증이다.” §8의 한계를 §0·§3에도 적용해야 한다.

### 2.2 451–471행: 후반 휴지 감쇠는 쇼츠 전용 신호가 아니다

완전 평형·등온·부반응 없음·누설 없음의 DFN에서 정적인 LLI/LAM이 지속 감쇠를 만들지 않는다는 좁은 명제는 맞다.
그것이 12 h 휴지의 마지막 6–8 h에 모든 다른 효과가 사라진다는 뜻은 아니다.

반례 1: 무쇼츠 수동 완화 `V=V∞+20 mV·exp(−t/10 h)`는 6 h와 12 h에서도 각각
**−1.097623, −0.602388 mV/h**의 기울기가 있다. 이는 해당 COMSOL의 예측이 아니라 고정 시간창 주장의 논리 반례다.
실제 1차 연구도 전압 감쇠법에 12–20 h의 완화 교란을 보고한다.
[Roth 외 JES 2023 논문](https://doi.org/10.1149/1945-7111/acb669),
[저자 연구실 공개 결과 요약](https://www.epe.ed.tum.de/fileadmin/w00bzo/ees/OnePager_PDF/SIM/2023-03-01_TR_Relaxation_Effects_in_Self-Discharge_Measurements_of_Lithium-Ion_Batteries.pdf).

반례 2: 완화가 끝나도

\[
V(q)=U_p(y_0-q/Q_p)-U_n(x_0+q/Q_n),\quad
\frac{dV}{dq}=-\frac{U'_p}{Q_p}-\frac{U'_n}{Q_n},\quad
\dot V=-\frac{I_{leak}}{C_{diff}},\quad C_{diff}=\frac{dq}{dV}.
\]

LAM은 Qp/Qn을, LLI와 밸런스는 OCP 기울기를 읽는 위치를 바꾼다. **문서 자신의 Cdiff 식이 LLI/LAM 민감도 경로를 가진다.**
동일한 쇼츠 전도도와 전압에서 Cdiff가 절반이면 기울기 크기는 두 배다.

반례 3: 동일한 기존 쇼츠와 동일한 시작 상태를 여러 사이클에서 반복하면 기울기가 일정할 수 있다.
그러므로 465행의 “일정하면 쇼츠 아님”도 성립하지 않는다. 기울기 증가 역시 쇼츠 성장만의 증거가 아니다.

σ≈0에서 LLI/LAM을 sweep하여 평탄한 결과를 얻어도, σ>0에서의 Cdiff 민감도나 1D 모델에 없는 오버행·부반응·열 드리프트를
배제한 것은 아니다. 후반 휴지는 유용한 **후보 관측량**으로 유지하되 실제 셀의 완화와 비쇼츠 자기방전 범위를 함께 평가해야 한다.

### 2.3 480행: 시간상수 식의 차원이 틀렸다

`C_cell`이 앞에서 사용한 Ah, `i_leak`이 A이면

\[
[C_{cell}V_{nom}/i_{leak}]=\mathrm{V\cdot h}\ne\mathrm{h}.
\]

전하 소모시간은 `C_cell/I_leak`, 국소 저항성 전압 감쇠시간은 `R_short·Cdiff = Cdiff·V/I_leak`이다.
Cdiff는 Ah/V여야 시간 단위가 된다. 비선형 OCV에서는 `t=R∫Cdiff(V)/V dV`를 써야 하므로 일반적으로 단일 시간상수가 아니다.
또 `sigma_eff·V/L_sep`는 A/m²다. 이를 쓰면 Cdiff도 면적당 값이어야 하고,
셀 단위 Cdiff에는 `I=A_cell·sigma_eff·V/L_sep`를 짝지어야 한다.

### 2.4 232–247행: OCP의 출처·원인 순위와 LAM의 이식 불가를 과도하게 단정했다

재료 이름과 함수 이름은 원본 표가 덮어써지지 않았다는 증거가 아니다. Q_el의 항등식도 용량 기준을 만들었다는 증거이며,
OCP 표의 provenance를 입증하지 않는다. 두 원곡선과 실험 전압이 없으므로 “가장 큰 단일 원인”의 순위도 미검증이다.

raw α의 곡선 의존성과 normalized LAM 비율은 구분해야 한다. `U2(w)=U1(a·w+b)`처럼 같은 물리를 공통 affine 좌표로 바꾸면
전극 용량 스케일 Q2=a·Q1이고 `1−Qaged/QBOL`에서 a는 상쇄된다.
따라서 “곡선이 다르면 이 LAM 비율은 반드시 이식 불가”에는 반례가 있다.
실제 비선형 곡선 형상 차이는 검증이 필요하며 LLI의 원점 문제까지 이 불변성을 확장할 수는 없다.

OCP 교체만 하고 끝낼 것이 아니라 BOL 전극 밸런스·사용 창·온도·방향·capacity 좌표와 재고의 변환을 먼저 정의해야 한다.

### 2.5 210–221, 381–386행: 3.3배 변환은 조건부로 맞지만 교정안이 같은 모델을 보존하지 않는다

Porous Conductive Binder는 전극상의 전도도에도 공극 보정을 적용한다.
따라서 “binder에는 전자 전도도 보정이 없다”는 반론은 공식 설명과 맞지 않는다.
[COMSOL Porous Conductive Binder](https://doc.comsol.com/6.4/doc/com.comsol.help.battery/battery_ug_electrochem_battery.06.51.html).

실제 고체 보정 지수가 1.5라면 `0.45^1.5=0.301869177`, 역수는 **3.3126933**이며 저항·누설 표의 산술도 재현된다.
다만 활성 지수와 식은 원본에서 확인해야 한다. intrinsic conductivity를 sweep했다고 명시했다면 이는 정상적인
intrinsic→effective 변환이지 3.3배 과대표기라는 뜻은 아니다. 같은 값인 epsl/epss도 복붙 의도를 증명하지 않는다.

등가적인 순수 저항 경로에서는 식이 `σ·epss^b`이므로 두 입력을 그 경로만으로 독립 추정하기 어렵다.
이는 `σ·epss`와 다르다. 보정이 전혀 없으면 epss가 그 전도도 식에서 빠지므로 “보정이 없어도 같은 곱 축퇴가 남는다”는
요청문 문구는 수정해야 한다.

권장안대로 **물리적** epss=1, epsl=0.45라 쓰면 분율 합은 1.45다.
이를 단순 유효 계수로 쓰겠다면 실제 분율이라는 해석을 버려야 하고, COMSOL의 다른 활성 항에서 소비되지 않는지 확인해야 한다.
더 명확한 방법은 물리적 분율을 유지한 채 No correction과 `sigma_eff`의 정의를 분리하는 것이다.
동일한 baseline을 유지하려면 현재 값을 `sigma_eff=0.301869177·sigma_short`로 옮겨야 한다.
값을 그대로 두고 보정만 없애면 **유효 전도도를 3.3127배 늘린 새 모델**이 된다.
분리막 양끝 전위차가 같을 때 누설전류도 그 배율로 증가한다. 연성 해 전체의 누설전류 배율은 별도 계산 대상이다.

### 2.6 535–540행: 제공된 XML 추출기가 노드 소유권과 활성 상태를 보존하지 못한다

부모 PhysicsFeature의 범위를 **첫 번째** `</PhysicsFeature>`까지 잘라서 후손을 포함하고 부모의 뒤쪽은 버린다.
그 잘린 문자열에서 첫 `entityFlags`를 찾으므로 자식의 DISABLED를 부모의 것으로 오인할 수 있다.
반대로 비활성 조상의 상태를 자식에 전파하지도 않는다.

검산 스크립트의 작은 중첩 XML에서 활성 부모+비활성 자식을 주면 원문 추출기는 부모를 disabled로 출력하고,
자식 csinit을 부모에 출력하며 부모 자신의 epss를 놓쳤다.
**실제 dmodel.xml을 잘못 읽었다는 직접 증거는 아니다.** 그러나 “추출 명령이 실행됐다”는 사실만으로
노드별 활성/소비 관계가 검증됐다고 할 수 없다.

XML tree parser로 직접 자식의 필드, 조상 경로, own/inherited flags, study/solver scope를 분리해 내보내야 한다.
문자열 등장 횟수는 consumer 수와 같지 않으므로 M4·M5의 소비자 0 주장도 활성 표현식 참조 관계로 확인해야 한다.

## 3. M2–M8 나머지 판정

| 항목 | 판정과 필요한 수정 |
|---|---|
| M2 | 전자 전도 보정과 조건부 산술은 지지. exponent·실제 식 확인 필요. “복붙”, “과대표기”는 의도/표기 계약 없이는 단정 불가. |
| M3 | 서로 다른 OCP 기준을 점검하자는 방향은 타당. 라이브러리 원본 여부, 주원인 순위, 모든 normalized LAM의 이식 불가는 미입증. |
| M4 | 활성 모델 참조 그래프를 확인하면 정적으로 판정 가능. 현재는 작성자의 XML 보고에 의존한다. 값이 일치한다는 사실만으로 어떤 파일에서 복사했는지 유일한 출처까지 증명되지는 않는다. |
| M5 | 같은 임계값 자체는 오류가 아니다. 방향이 반대인 crossing에 쓸 수 있다. impl1은 ge2가 쓰는 상태를 바꾸므로 “아무 결과도 안 바뀜”은 넓다. 충방전 제어에 영향 없는지와 후처리에 영향 없는지를 구분해야 한다. |
| M6 | `∫I(V−V0)dt = W−V0ΔQ`는 기준전압에 대한 에너지로 정의할 수 있다. “무의미”보다 “단자 에너지/효율로 해석할 근거 없음”이 정확하다. 실제 cdc1 CC/CV/rest 전류와 i_app가 일치하는지가 더 강한 검증점이다. |
| M7 | 양극 CDC의 충전 양수 규약은 공식 예제로 확인된다. 주어진 ODE에서 Cap은 감소한다. “음수”는 Cap 초기값도 필요하다. 부호만 바꿔도 휴지 내부누설을 빠뜨린 외부전류 적분은 물리적 SOC가 되지 않는다. |
| M8 | 현재 설정과 저장해·dataset의 불일치는 가능한 정적 발견이지만 원본 해 metadata가 없어 재확인하지 못했다. solution 이름만으로 모든 해의 파라미터를 확정해서는 안 된다. |

M5에서 빈 global reinitialization 표 하나만으로 모든 event 효과나 중단을 배제할 수 없다.
공식 Stop Condition에는 표현식과 별도로 implicit event를 선택하는 경로가 있고 event의 하위 공간 reinitialization도 존재한다.
[Stop Condition](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_ref_solver.36.212.html),
[Implicit Event](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_ref_equationbased.32.100.html).

M7의 충전 양수 근거는 공식 plating 예제의 충전 그래프 필터 `liion.cdc1.Icell>0`이다.
[Lithium Plating and Stripping](https://doc.comsol.com/6.4/doc/com.comsol.help.models.battery.li_plating/li_plating.html).

## 4. Q1–Q6에 대한 직접 답변

1. **Q1:** 표준 입자 SOC의 분모는 최대농도가 맞다. 이 모델의 활성 반응 Eeq가 실제 어떤 농도 정규화를 소비하는지는
   per1과 material model input을 더 읽어야 한다. A1의 일반 정의를 뒤집지는 못했고, A1→실제 OCP 영향의 연결이 아직 비어 있다.
2. **Q2:** 의도적 사이트 밀도 감소와 독립 초기 Li 재고 모델은 가능하다. 따라서 미사용 변수로 누락을 증명할 수 없다.
   그런 모델에서 cEeqref를 되돌리면 설계를 바꾸는 것이 맞다.
3. **Q3:** 접촉 상실/활성 입자 감소를 표현한다면 epss-only가 자연스럽다. cmax-only와는 비표면적·수송·반응속도 효과가 달라
   같은 capacity 비율이어도 동역학적으로 동등하지 않다. 요구 LAM의 물리 의미를 먼저 합의한다.
4. **Q4:** binder의 전자 전도도 보정은 공식적으로 지원된다. 3.3127배는 b=1.5와 인용 epss에서 맞는 변환이다.
   실제 지수·보정식·sigma의 명명 계약을 확인해야 “잘못 표기”라고 판정할 수 있다.
5. **Q5:** **성립하지 않는다.** 후반 6–8 h만으로 완화나 비쇼츠 자기방전을 배제할 수 없고, Cdiff를 통해 LLI/LAM도 기울기를 바꾼다.
   일정 기울기도 기존 쇼츠와 양립한다. 후보 신호축으로 낮추고 검증해야 한다.
6. **Q6:** socicd1의 진짜 비활성은 그 초기화 경로를 제거한다. 하지만 Study와 Solver의 초기값이 다른 solution을 읽을 수 있다.
   반응 Eeq 경로, 초기 species mode, study/solver 초기값 출처, 선택 dataset/solution을 함께 확인해야 한다.
   Model Builder에서 완전히 disabled인 노드를 Study가 몰래 re-enable한다고 주장할 근거는 없다.
   [Particle Intercalation](https://doc.comsol.com/6.4/doc/com.comsol.help.battery/battery_ug_electrochem_battery.06.47.html),
   [Study 초기값 설정](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_ref_solver.36.012.html),
   [Solver Dependent Variables](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_ref_solver.36.130.html).

## 5. 수정 우선순위

**“M1 두 줄 수정”부터 시작하지 말고 다음 증거를 먼저 고정해야 한다.**

1. MPH SHA-256와 선택 study/solution/dataset/paramValues를 기록한다.
2. 활성 pin1 maximum concentration·initial concentration source, per1 Eeq, 선택 재료와 함수 인자,
   study/solver 초기값 출처를 경로를 보존하는 XML 또는 COMSOL export로 제시한다.
3. 요구하는 LAM을 `H/H0=1−LAM`인지, 부피와 사이트 밀도 두 기작을 묶은 값인지 정의하고 BOL Li 기준을 고정한다.
4. 원본과 epss-only 대안에서 실제 초기 cs, effective cmax, Eeq의 입력값, 양극·음극 OCP, 활성 Li 재고를 비교한다.
   완전한 정적 연결 검증 또는 COMSOL 평가로 특정 모델의 값을 확인한다.
5. 그 후 동일 프로토콜의 전압 궤적과 ICA, 휴지 전압을 비교한다. sigma를 바꿀 때는 baseline의 유효 전도도를 보존한다.
6. 휴지 판정은 시간창·SOC·온도·Cdiff·완화 모델·비쇼츠 자기방전의 불확실성을 포함해 재설계한다.

원문의 §2 난간 분석도 별건 요청과 연결되므로 주의해야 한다.
`LAM_PE=LAM_NE=1−x_cell`만으로 `LLI=1−x_cell`은 나오지 않는다. 예를 들어 x_cell=0.9,
두 a 비율=1, c_lit 비율=0.98이면 LAM 둘은 0.1, LLI는 0.02다.
출력값이 경계에 같다는 사실만으로 최적화의 bounds나 식별 불가능한 방향을 “정확히 안다”고 할 수도 없다.
또 §7의 기본 `np.allclose`는 machine-epsilon 증명이 아니다. 0.1과 0.1000009도 기본 허용오차에서 통과한다.
이들은 해당 실측 행이 틀렸다는 판정이 아니라 제시된 논증/검증법의 한계다.

## 6. 산출물과 재현 범위

- `mph_review_checks.py`: 표준 Python만 쓰는 조건부 산술 및 중첩 XML/완화/단위 반례.
- `mph_review_checks_results.json`: rc 0으로 실행한 출력.
- `mph_comsol_semantics.md`: COMSOL 공식 문서 경로와 설정별 근거.
- `mph_physics_claims.md`: 물리 반례와 1차 연구 근거.
- 이 보고서의 판단은 위 자료를 중복 제거해 종합한 것이다.

첨부 요청문과 Git 요청문 SHA-256은 모두
`6d5e115b50b373598840b3d47836c4c5dd8d4c967dba078f016484997c4b9e0d`.
검토 문서 SHA-256은 `67c58eb7af015ec905648cd5ce65022737ecc57d13163b74bf584a6fad88313e`.
문서 Git blob은 `8f497ed2b85d154bc2e4e4389a77adcb00558df2`.

**최종: 확정 버그·수정 지시서로서는 NO-GO. 조건부 정적 진단과 검증 가설로 고쳐야 한다.**
