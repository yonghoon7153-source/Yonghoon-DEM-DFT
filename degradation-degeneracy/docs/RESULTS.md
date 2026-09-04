# RESULTS — full-cell 곡선으로 LAM_PE와 LAM_NE를 분리할 수 있는가

> 이 파일은 `tools/make_results.py`가 결과 파일에서 자동 생성한다. 직접 수정하지 말 것.

> ✅ provenance 검증 통과 — `manifest_존재`, `config_hash`, `clean_worktree`, `필수_입력_존재`, `run_spec_schema`, `sig_version`, `optimizer_정책`, `producer_곡선일치`, `목적함수_순서`, `입력봉인_교차일치`, `입력_스냅샷`, `곡선_producer_재검`, `코드_identity`, `시작_provenance`, `start_파일_존재`, `attempt_파일_존재`, `attempt_파일_일치`, `start_파일_일치`, `실행중_코드불변`, `시작종료_서명일치`, `_참고_코드재계산불가`, `입력_digest_재해시`, `run_signature_기록`, `run_signature_재계산`, `채점파일_정본`, `출력봉인_재계산`, `조건집합_서명일치`, `출력_완전성`, `출력_격자완전성`, `행별_서명`, `단일_서명`, `manifest와_일치`, `restart_출처`, `비교입력_grid`, `비교입력_halfcell`, `wsweep_provenance`, `파생_case_comparison.yaml`

생성: 2026-08-18 01:50 UTC  
입력: `results/grid_fit_v4`  
artifact producer git/source_digest: `c0f1daa0d92a7625c3602799c81db04b5e2e5783` / `d50295f980ccaa81`  
report generator git/source_digest/dirty: `d4f43d1ab4bb2ff709a3984f4247fe7afc1e991b` / `e5fa9749fd899e3d` / `False`  
앵커 fits_sha256: `18ebb8e7b32ef879ea0badfd2d72d64446aa0b01b4aba6c9db692cf224926b46`  
앵커 curves_sha256(sealed): `b69dc7bee0bb2e32aba73b6ace91255d964bceb41f9361886de7275bf48aa8b8`  
(대조: `artifacts/artifact_index.yaml` — 두 값이 같은 묶음이 이 보고서의 근거다)  

## 질문

2026-08-05 연구세미나 22p에서 `LAM_PE ≈ LAM_NE ≈ 13%`, `LLI ≈ 17%`가 나왔다. 이것이 실제 물리인가, 아니면 full-cell 곡선 하나로는 두 전극을 가를 수 없어서 생긴 **fitting degeneracy**인가.

정답을 아는 PyBaMM 합성 곡선을 격자로 만들고, 기존 α·β fitting이 그 정답을 복원하는지 채점해 답한다.

## 핵심 결론

1. dQ/dV 항을 넣으면 recovery failure 가 918/1476 (62.2%) → 926/1476 (62.7%) 로 **사실상 변화가 없다**(차이 2%p 이내). 즉 34p의 dQ/dV 추가는 이 합성 격자에서 최종 오차를 측정 가능하게 줄이지 못한다. (행별 max-mode 절대오차의 평균 2.5%p → 2.4%p, raw PE/NE 오차 반대부호 비율 68% → 48% — **물리적 상쇄로 해석 불가**)

   ⓘ **위 반대부호 비율을 '34p가 상쇄를 줄였다'로 읽지 마세요.** 이 지표는 raw 오차의 부호만 세는데, 목적함수마다 전역 편향의 부호가 달라 그 차이가 그대로 잡힙니다. 목적함수별 평균편향을 뺀 뒤 다시 세면 방향이 뒤집힙니다. 전압 민감도로 가중하지 않은 파라미터 오차 부호는 full-cell 곡선에서 실제로 상쇄되는 양을 재지도 않습니다.

   ⚠ **이 순위는 모집단에 따라 뒤집힙니다.** 복원가능군에서는 34p−33p = 0.5%p인데 전체 격자에서는 -2.6%p입니다. 복원불가군(참 α<1)은 grid 기준에서 정답이 표현 불가능한 조건이라 제외에 근거가 있지만, **그 제외가 우열을 바꾸므로** 어느 모집단인지 없이 인용하면 안 됩니다.

   ⚠ **두 목적함수의 optimizer protocol이 다릅니다.** dQ/dV 계열은 매끄러운 해를 초기값으로 받고(`pocv_dvdq_dqdv` 중 100%), `pocv_dvdq`는 그 시드 제공자라 받지 않습니다(0%). adaptive 조기 종료까지 겹치면 평가 budget도 달라집니다. 따라서 위 수치는 **현재 pipeline에서 관측된 값**이지 목적함수의 정보량 비교가 아닙니다. 어느 쪽이 유리한지도 단정할 수 없습니다 — 비볼록 문제에서 특정 seed가 항상 더 좋은 basin으로 데려간다는 보장이 없기 때문입니다. 정보량을 비교하려면 동일 seed·동일 restart budget·early stop off의 paired 재실행이 필요합니다.

2. 참값이 뚜렷이 다른 조건(|ΔLAM|_true ≥ 6%p)에서 fitting이 두 전극을 같다고 답한 것은 **1/245 (0.41%)** 다. 참 격차 9.9%p → 복원 격차 10.5%p, shrinkage 1.06. 

   이 관측이 어느 쪽을 지지하는지 **동일가중 합성격자의 조건부 사건률 비**로 보면 (population=recoverable)

   > P(같다고 답 | 참 격차 < 2%p) = 24/66 (36.36%)
   > P(같다고 답 | 참 격차 ≥ 6%p) = 1/245 (0.41%)
   > 사건률 비 = 89.1

   같은 지표를 **전체 생성성공 격자**(population=all)에서 재계산하면 작은 격차에서 "같다" 34/93 (36.56%), 넓은 격차 붕괴 64/604 (10.60%), 사건률 비 **3.45** 다. 즉 위 값은 복원가능군 선택에 강하게 의존한다 — 두 값을 **함께** 인용하지 않으면 안 된다.

   **이 값을 '두 전극이 실제로 비슷하다'로 읽을 수 없다.** 세 가지 때문이다.

   1. **임계 의존** — 같은 데이터에서 (참격차, 동일판정) 임계를 흔들면 사건률 비가 2.2~130.5(중앙값 16.1)로 움직인다 (이 범위는 첫 `<tol` 정의 패널의 값이다 — exact-zero 정의 패널은 별도로 최대 165.4 였다). 현재 조합은 이웃보다 유독 높은 **국소 봉우리**다 — 이 값을 대표값으로 인용하면 사후선택이 된다. 아래 임계 민감도 표를 함께 볼 것.

   2. **posterior가 아님** — 이건 두 합성 가설 아래의 *사건률 비*다. `P(참값이 같다 | fitting이 같다고 답함)`으로 바꾸려면 실제 셀 집단의 사전확률과, 여기서 버린 중간 격차 구간의 주변분포가 필요하다. 격자점을 같은 빈도로 센 것은 실제 셀의 분포가 아니다.

   3. **부분집단 조건화** — 복원가능군(population=recoverable)에서만 센 값이다. 실제 셀이 그 부분집단에 속한다는 독립 근거가 없으면 적용할 수 없고, 전체 격자에서는 값이 크게 달라진다(아래 표).

   → 지금 자료로 방어할 수 있는 문장은 하나뿐이다: **이 합성 격자의 복원가능군에서, 참 격차가 뚜렷한 조건이 '같다'로 붕괴하는 일은 드물었다.** 22p가 물리인지 degeneracy인지는 이것만으로 판정되지 않는다.

   ⚠ 이 숫자들은 임계 설정에 의존한다. 붕괴로 세려면 격차를 6%p에서 2%p 아래로 끌어내려야 하므로 최소 4%p의 격차 오차가 필요한데, 실측 격차 오차는 중앙값 2.6%p·99분위 5.7%p다. 부호를 살려 행별로 보면 복원 격차가 판정 임계까지 남긴 여유(= tol − 복원 격차)는 중앙값 -8.2%p·최대 1.8%p 이고, 넓은 격차 245조건 중 격차가 줄어든 방향은 98조건이다. 이 값들은 **기술통계일 뿐, 붕괴가 관측 가능했다는 근거가 아니다** — 같은 결과에서 뽑은 오차분포로 그 결과의 낮은 사건률을 방어할 수 없다. 낮은 사건률의 견고성은 아래 임계 민감도 표와 모집단 제한으로만 판단할 것.

3. **22p 조건(LAM_PE≈LAM_NE≈13%, LLI≈17%) 근방의 recovery failure 는 1/8 (12.50%)** (목적함수 `pocv_dvdq`, noise=0, radius=0.021 안의 최근접 8 grid 조건, raw max-mode 오차 > 2%p 임계)  — 행별 max-mode 절대오차의 평균 1.7%p, raw PE/NE 오차 반대부호 비율 50%, 참 PE-NE 격차 1.0%p → 복원 격차 1.9%p. ⚠ **이 8점은 참값이 모두 같은 격자점이 아니다** — PE=NE 가 4/8, |ΔLAM|>0 이 4/8 이고 최대 참 격차가 2.0%p 다. 평균 참 격차는 1.0%p 다. 여기에 wide-gap(≥6%p)은 **하나도 없으므로**, 이 표본으로는 "참 격차가 큰 조건이 '같다'로 붕괴하는가" 를 물을 수 없다 — 그 질문의 답은 위 2번이다. 이 8개는 실제 셀이 아니라 설계 격자의 최근접 점이며, 임계·반경·noise·목적함수를 바꾸면 값이 달라진다.

4. **생성성공 격자의 52%는 선택한 grid-reference 의 현재 α-window eligibility criterion 을 통과하지 못한다**(`src/scoring.py`: `alpha_true >= 1 − atol`). 이 판정은 설정된 box bounds 도, β 도, 물리적 표현 가능성도 검사하지 않는다 — 두 α 값 하나만 본다. 위 숫자는 모두 그 안쪽 **목적함수당 1476조건** 에서만 센 값이며(파일의 objective-condition 행 합계는 5904), 바깥을 섞으면 목적함수 간 차이가 묻힌다. 이는 데이터의 물리 속성이 아니라 **현재 채점 규칙의 자격 판정**이다. **단 위 2번의 전체 생성성공 격자 값(population=all)은 이 안쪽 바깥을 함께 센 예외다.** gap 분석의 분모는 noise=0 의 66·245조건, 22p 는 8조건으로 각각 다르다.

   → **목적함수 간 비교(결론 2)의 인용 정본은 공정 paired 보고서 `docs/RESULTS_PAIRED_FIXED5.md` 다** (`results/paired_fixed5_v4` 에서 생성). 위 1번은 비대칭 pipeline(adaptive 조기 종료 + warm start 연쇄)에서 관측된 값이므로 단독 인용하지 말 것.

### 이 결론이 말하지 않는 것

- **격자 공백(F14)**: 완방 프레임 guard 때문에 저LLI 영역에 고LAM_PE 조건이 없다. 저LLI(≤2%)에서 도달한 최대 LAM_PE는 `0.08`, 격자 전체 최대는 `0.2`. 고LAM_PE 결론은 고LLI가 동반된 조건에서만 검증된 것이다.
- **restart 불일치율(F4)**: adaptive 조기 종료로 조건마다 restart 수가 달라, multi-start 불일치율을 목적함수 간 비교 지표로 쓰지 않았다. `degeneracy_summary.yaml`의 `restart_conditioned` 항목에 restart 수로 조건화한 값만 있다.
- **방법 바이어스(F5)**: 판정 기준 2%p가 방법 자체의 계통 편향과 같은 크기일 수 있어, 바이어스를 뺀 보정 판정을 표에 나란히 뒀다. 두 값이 크게 다르면 그 목적함수의 결론은 약하다.
- **운용 범위가 한 점이다 (외적타당도 #48, 2026-09-04 승격).** 격자 전체가
  `protocol.c_rate = 0.05` **한 C-rate** 에서, `charge_first` **한 프로토콜**로,
  컷오프 `4.2 V / 2.5 V` **한 쌍**에서 나왔다 (`configs/base.yaml`). 0.05C 는
  준평형(pOCV)이라 **과전압이 거의 없는 가장 유리한 조건**이다.
  `[해석]` 그러므로 이 보고서의 복원 성적은 **"pOCV 급 측정에서의 상한"** 으로
  읽어야 한다. 운용 C-rate(0.5C·1C)에서는 과전압이 곡선 모양을 바꾸므로 같은
  판정이 성립한다는 근거가 **이 자료 안에 없다.** Phase 1j 가 잰
  과전압 서명(무전류 대비 18.7 mV, 288점 전부 한쪽 부호)이 0.05C 에서도
  0 이 아니라는 것까지가 우리가 아는 전부다.
- **셀 간 산포가 0 이다 (외적타당도 #49, 2026-09-04 명시).** 모든 조건이
  `parameter_set: Chen2020_composite` **하나**에서 나왔다 — 전극 두께·공극률·
  체적분율·최대농도가 3069개 조건 전부에서 **같은 값**이다
  (NE 흑연 vf 0.735 + Si 0.015, PE vf/porosity 0.335, `pe_max_conc` 63104).
  곧 이 격자에는 **제조 산포도, 셀 간 편차도, 파라미터 불확실성도 없다.**
  `[해석]` 실제 진단은 "이 셀의 파라미터를 안다" 는 가정 위에 서지 않는다.
  반쪽전지 기준곡선이 **다른 셀의 것**이면 창 좌표 자체가 틀어지므로, 여기
  보고된 오차막대는 **그 축을 포함하지 않는다.** Cui 2024 의 반복측정 산포
  (PE 1–12 mV / NE 8–93 mV)조차 이 격자에는 들어와 있지 않다.
- 모두 **합성 데이터** 결과다. 실제 셀의 모델 오차(SEI, 저항 분포 등)는 여기에 없다. 합성 truth 생성이 LLI를 양·음극 초기농도에 일률적으로 적용하는 **한 가지 규약**에 조건부이기도 하다 (SEI·plating·전극별 endpoint 이동은 같은 총 inventory loss에서도 다른 곡선을 만든다). 실제 셀이 더 나쁠지 나을지는 **증명되지 않았다** — 복잡성이 추가 정보를 만들 수도, 없앨 수도 있다.

## 목적함수 4종 비교

복원가능군(F1)만, 노이즈 전체 합산.

| objective | n | degeneracy | (바이어스 보정) | 평균 max-mode \|err\| | raw 반대부호 |
|---|---|---|---|---|---|
| pOCV only | 1476 | 78% | 67% | 4.7%p | 29% |
| pOCV + dV/dQ  (33p 기존) | 1476 | 62% | 15% | 2.5%p | 68% |
| pOCV + dV/dQ + dQ/dV  (34p 개선) | 1476 | 63% | 25% | 2.4%p | 48% |
| dQ/dV only | 1476 | 77% | 66% | 5.0%p | 22% |

### 전체 격자 (복원불가군 포함)

복원불가군(참 α<1)은 **현재 grid-reference 의 α-window eligibility rule 밖**이다 (`src/scoring.py`: `alpha_true >= 1 − atol`). 위 표에서 뺀 근거는 그것이다. 이것은 bounds 전체의 표현 가능성 판정도, 다른 reference·parameterization 에서의 불가능성 판정도 아니다. 다만 그 제외가 난이도와 무관하지 않으므로(저LLI에서 복원가능 비율이 훨씬 낮다) 전체군을 같이 싣는다.

> ⚠ **두 표에서 33p와 34p의 우열이 뒤집힙니다.** 결론 문장에 어느 모집단인지 반드시 함께 쓰세요.

| objective | n | degeneracy | (바이어스 보정) | 평균 max-mode \|err\| | raw 반대부호 |
|---|---|---|---|---|---|
| pOCV only | 3069 | 80% | 81% | 5.3%p | 27% |
| pOCV + dV/dQ  (33p 기존) | 3069 | 74% | 53% | 3.8%p | 55% |
| pOCV + dV/dQ + dQ/dV  (34p 개선) | 3069 | 72% | 50% | 3.8%p | 45% |
| dQ/dV only | 3069 | 81% | 70% | 5.4%p | 21% |

### 노이즈 수준별 (F10)

34p − 33p 의 recovery failure 차이는 noise 0 → +4%p, noise 0.001 → +0%p, noise 0.005 → -2%p 다. 노이즈 수준에 따라 **방향이 바뀐다** — 한 수준만 인용하면 안 된다. 관측 방향·크기는 noise 수준과 실행 protocol 에 함께 의존하므로 표 전체를 함께 본다. 이것은 dQ/dV 의 정보량 우열을 증명하지 않는다 — optimizer difficulty 와 분리되지 않았다.

| objective | noise | n | degeneracy | (바이어스 보정) | 평균 max-mode \|err\| | raw 반대부호 |
|---|---|---|---|---|---|---|
| pOCV only | 0 | 492 | 78% | 64% | 4.8%p | 29% |
| pOCV only | 0.001 | 492 | 78% | 68% | 4.6%p | 28% |
| pOCV only | 0.005 | 492 | 77% | 68% | 4.8%p | 31% |
| pOCV + dV/dQ  (33p 기존) | 0 | 492 | 60% | 12% | 2.4%p | 71% |
| pOCV + dV/dQ  (33p 기존) | 0.001 | 492 | 62% | 14% | 2.4%p | 69% |
| pOCV + dV/dQ  (33p 기존) | 0.005 | 492 | 64% | 20% | 2.6%p | 64% |
| pOCV + dV/dQ + dQ/dV  (34p 개선) | 0 | 492 | 64% | 22% | 2.4%p | 51% |
| pOCV + dV/dQ + dQ/dV  (34p 개선) | 0.001 | 492 | 62% | 25% | 2.3%p | 45% |
| pOCV + dV/dQ + dQ/dV  (34p 개선) | 0.005 | 492 | 62% | 27% | 2.5%p | 47% |
| dQ/dV only | 0 | 492 | 76% | 66% | 4.9%p | 22% |
| dQ/dV only | 0.001 | 492 | 77% | 65% | 4.9%p | 20% |
| dQ/dV only | 0.005 | 492 | 78% | 67% | 5.1%p | 23% |

## 22p 실험 조건 판정

*모두 `noise = 0` 조건이다. 노이즈가 있으면 값이 달라진다(F10) — `objective_comparison.yaml`의 `verdict_22p.noise` 참조.*

> ⚠ **이 8점은 참값이 모두 같은 격자점이 아니다.** PE=NE 가 4/8, |ΔLAM|>0 이 4/8 이고 최대 참 격차가 2.0%p 다. 여기에 wide-gap(≥6%p)은 **하나도 없으므로** 22p 판정에 쓸 수 있는 것은 "참 격차가 큰 조건이 붕괴하는가" 가 아니라 국소 n=8 표본의 복원 성적뿐이다 (그 질문의 답은 결론 2 다).

| objective | 근방 조건 | recovery failure | 평균 max-mode \|err\| | err LAM_PE | err LAM_NE | raw 반대부호 |
|---|---|---|---|---|---|---|
| pocv | 8 | 88% | 2.8%p | -1.3%p | 1.2%p | 50% |
| pocv_dvdq | 8 | 12% | 1.7%p | -1.7%p | 0.1%p | 50% |
| pocv_dvdq_dqdv | 8 | 12% | 1.9%p | -1.9%p | 0.1%p | 50% |
| dqdv_only | 8 | 50% | 3.8%p | -2.3%p | -3.2%p | 12% |

> ⚠ **`raw 반대부호` 열을 degeneracy의 지문으로 읽지 마세요.** 이 열은 raw 오차의 부호가 반대인 비율일 뿐이고, 목적함수마다 전역 편향의 부호가 다르면 그 차이가 그대로 잡힙니다. 편향을 중심화하면 목적함수 간 순서가 뒤집힙니다. 또 전압 민감도로 가중하지 않은 파라미터 오차 부호는 full-cell 곡선에서 실제로 상쇄되는 양을 재지 않습니다.

## 전극 격차를 구분하는가 — 22p 질문의 직접적인 답

*`noise = 0` 조건 기준.*

22p 근방 격자점은 **참 격차가 작다** — PE=NE 가 4/8, |ΔLAM|>0 이 4/8 이고 최대 참 격차가 2.0%p 다. 거기서 복원값이 비슷하게 나오는 건 아무 증거가 못 된다. 물어야 할 것은 반대 방향이다 — **참값이 뚜렷이 다를 때도 fitting이 둘을 같다고 말하는가.**

| objective | 넓은 격차 조건 n | **격차 붕괴율** | shrinkage | 거짓 분리율 | 붕괴에 필요한 격차오차 / 실측 중앙값 |
|---|---|---|---|---|---|
| pocv | 245 | **17/245 (6.94%)** | 1.05 | 33/66 (50.00%) | 4%p / 2.2%p |
| pocv_dvdq | 245 | **1/245 (0.41%)** | 1.06 | 42/66 (63.64%) | 4%p / 2.6%p |
| pocv_dvdq_dqdv | 245 | **2/245 (0.82%)** | 1.10 | 34/66 (51.52%) | 4%p / 2.0%p |
| dqdv_only | 245 | **11/245 (4.49%)** | 1.07 | 26/66 (39.39%) | 4%p / 1.9%p |

- **격차 붕괴율**: 참 격차 ≥ 6%p인데 복원 격차 < 2%p로 답한 비율. 높을수록 "두 전극이 비슷하다"는 관측이 무의미해진다.
- **shrinkage**: 복원 격차 / 참 격차의 평균. 1이면 격차를 그대로 복원, 0에 가까우면 전부 뭉갠다.
- **거짓 분리율**: 참값은 같은데 다르다고 답한 비율 (반대 방향 오류).
- **붕괴에 필요한 격차오차**: 붕괴로 세려면 격차를 6%p에서 2%p 아래로 끌어내려야 하므로 최소 4%p의 격차 오차가 필요합니다. 이 값이 실측 격차오차 중앙값보다 크면, **낮은 붕괴율의 일부는 측정이 아니라 오차 스케일이 임계 간격보다 작다는 사실에서 옵니다** — 관측률 전체가 임계 설정만의 결과라는 뜻은 아니지만, 그대로 떼어 인용하지 마세요.

### 임계 민감도 — 위 숫자를 인용하기 전에 볼 것

같은 데이터에서 (참 격차 cutoff, 동일 판정 tol) 두 임계만 바꿔 사건률 비를 다시 센 것이다 (`pocv_dvdq`, noise=0, 복원가능군). 값이 한 자릿수에서 수십까지 움직이면, 특정 조합의 값은 **측정이 아니라 선택**이다.

> ⓘ **이 격자에서 두 정의는 인용 지점(`참 격차 ≥ 6%p`, `동일 판정 < 2%p`)에서 같은 집합이다** — 양쪽 모두 66조건이다. 격자 step 이 2%p 라 `< 2%p` 가 `= 0` 과 같아지기 때문이다. 두 패널을 **서로 독립인 두 확인으로 읽지 마세요**; 정의가 갈리는 것은 `동일 판정` 임계를 3%p 이상으로 넓힐 때부터다.

**참값 "같다" = 참 격차 < tol**

| 참 격차 ≥ \ 동일 판정 < | 1%p | 2%p | 3%p | 4%p | 5%p |
|---|---|---|---|---|---|
| **2%p** | 2.2<br><sub>12/66 ÷ 36/426</sub> | — | — | — | — |
| **4%p** | 3.7<br><sub>12/66 ÷ 16/326</sub> | 3.5<br><sub>24/66 ÷ 34/326</sub> | 4.2<br><sub>99/166 ÷ 46/326</sub> | — | — |
| **6%p** | 44.5<br><sub>12/66 ÷ 1/245</sub> | 89.1<br><sub>24/66 ÷ 1/245</sub> | 13.3<br><sub>99/166 ÷ 11/245</sub> | 6.9<br><sub>121/166 ÷ 26/245</sub> | 5.0<br><sub>183/247 ÷ 36/245</sub> |
| **8%p** | 32.5<br><sub>12/66 ÷ 1/179</sub> | 65.1<br><sub>24/66 ÷ 1/179</sub> | 106.8<br><sub>99/166 ÷ 1/179</sub> | 130.5<br><sub>121/166 ÷ 1/179</sub> | 18.9<br><sub>183/247 ÷ 7/179</sub> |

**참값 "같다" = 참 격차 정확히 0**

| 참 격차 ≥ \ 동일 판정 < | 1%p | 2%p | 3%p | 4%p | 5%p |
|---|---|---|---|---|---|
| **2%p** | 2.2<br><sub>12/66 ÷ 36/426</sub> | — | — | — | — |
| **4%p** | 3.7<br><sub>12/66 ÷ 16/326</sub> | 3.5<br><sub>24/66 ÷ 34/326</sub> | 4.8<br><sub>45/66 ÷ 46/326</sub> | — | — |
| **6%p** | 44.5<br><sub>12/66 ÷ 1/245</sub> | 89.1<br><sub>24/66 ÷ 1/245</sub> | 15.2<br><sub>45/66 ÷ 11/245</sub> | 8.7<br><sub>61/66 ÷ 26/245</sub> | 6.6<br><sub>64/66 ÷ 36/245</sub> |
| **8%p** | 32.5<br><sub>12/66 ÷ 1/179</sub> | 65.1<br><sub>24/66 ÷ 1/179</sub> | 122.0<br><sub>45/66 ÷ 1/179</sub> | 165.4<br><sub>61/66 ÷ 1/179</sub> | 24.8<br><sub>64/66 ÷ 7/179</sub> |

각 칸은 `사건률 비` 아래에 `분자/분모 ÷ 분자/분모`를 함께 적었다. `∞`는 넓은 격차군에서 붕괴가 0건이라는 뜻이며, 요약 통계의 min/max 범위에서는 제외되므로 개수를 `gap_analysis.lr_sensitivity_n_infinite`로 따로 센다. 표의 최댓값을 대표값으로 쓰지 말 것.

### 모집단을 바꾸면 (복원불가군 포함)

| 모집단 | 작은 격차에서 "같다" | 넓은 격차 붕괴 | 사건률 비 |
|---|---|---|---|
| 복원가능군 | 24/66 (36.36%) | 1/245 (0.41%) | 89.09 |
| 전체 생성성공 격자 | 34/93 (36.56%) | 64/604 (10.60%) | 3.45 |

복원가능군 조건화는 물리적 근거가 있지만(참 α<1이면 정답이 재구성 창 밖), **그 조건화가 사건률 비를 크게 바꾼다**는 사실은 결론과 같은 무게로 적어야 한다.

## 곡률 진단 (Hessian) — 참고용, 결론 근거 아님

> ⛔ **이 절은 문서 상단 provenance 검증 범위 밖입니다.** 상단의 초록 검사 목록은 fit artifact 를 검증한 결과이며, Hessian 산출물의 곡선·`obj_cfg`·`v_col`·reference·표본·`eps` 연결은 **어느 검사도 보지 않습니다**. 비인용 부록으로만 읽으세요 (A·A'·B·C 미수정).

> ⚠⚠ **이 절의 수치를 식별성(degeneracy) 근거로 인용하지 마세요.** 적대적 리뷰에서 세 가지가 확인됐습니다 (F33). ① 목적함수가 보간·미분·peak 연산을 포함해 비매끄러운데 절대 step `eps` 하나를 모든 파라미터에 씁니다 — 34p 조건수 중앙값이 eps=1e-3/1e-4/1e-5에서 12.8/229/17381로 움직입니다. 수렴하지 않았다는 뜻입니다. ② `min_eigval_positive`가 100%가 아닌 만큼은 양의 정부호 국소 최소점임이 **입증되지 않은** 지점이고, 그것이 실제 saddle 인지 유한차분·비매끄러움 artifact 인지 현재 자료로는 **구분하지 않습니다**. 그런데도 flat score와 결합 판정은 그대로 집계됩니다. ③ `α_PE·α_NE 결합`은 **같은 부호**를 세는데, 22p 가설(한쪽 과대·다른쪽 과소)은 α에서 부호가 **반대**입니다 — 지표가 묻는 질문이 가설과 다릅니다.

optimizer 가 반환한 해에서 목적함수의 2차 미분입니다 — 그 점이 정상점(stationary)임은 검증되지 않았습니다. 아래는 진단 참고로만 두고, 결론이나 optimizer 방어 문장에 쓰지 않습니다.

| objective | n | 조건수(중앙값) | flat score | 최소고윳값>0 | α_PE·α_NE 결합 |
|---|---|---|---|---|---|
| pocv_dvdq | 200 | 3.64e+04 | 2.8e-05 | 96% | 0% |

- **조건수**는 매끄러운 목적함수라면 작을수록 최적점이 잘 정의돼 있다는 뜻이다. 다만 그 해석은 아래 조건이 모두 만족될 때만 쓸 수 있다.
- ⚠ **조건수의 절대값도, 목적함수 간 순서도 인용하지 마세요.** 목적함수가 여러 스케일에서 울퉁불퉁하면 수치 Hessian 이 수렴하지 않아 eps 를 바꾸면 값이 자릿수 단위로 움직입니다 (F23). 순서가 eps 에 안정적이라는 근거는 확인되지 않았습니다 (이 표는 eps=0.0001, objective 1개).
- **최소고윳값>0** — 100%가 아니면 그만큼은 양의 정부호 국소 최소점임이 입증되지 않은 지점입니다. 실제 saddle 인지 유한차분·비매끄러움 효과인지는 **구분하지 않습니다**. 그 조건들의 조건수는 해석하지 마세요.
- **α_PE·α_NE 결합** — 평평한 방향에서 두 전극이 같은 부호로 묶여 있는 비율입니다. **22p 가설(한쪽 과대·다른쪽 과소)은 부호가 반대**라 이 지표는 그 가설에 적용할 수 없습니다 (F33). 진단 참고로만 보세요.

## multi-start 진단 — 진짜 degeneracy와 최적화 난이도의 구분

같은 조건을 여러 초기값에서 다시 풀었을 때 어떻게 갈리는지를 봅니다. **두 실패 모드는 처방이 정반대**라 반드시 나눠야 합니다.

> 아래 표는 **무작위 restart끼리만** 비교한 것입니다(F21b). dQ/dV 목적함수는 첫 restart에 매끄러운 해를 초기값으로 받으므로, 그것을 포함하면 최적 J에 닿는 restart가 정의상 하나뿐이 되어 항상 multimodal로 찍힙니다.

| objective | n | **flat valley** | multimodal | unique min |
|---|---|---|---|---|
| dqdv_only | 1468 | **1%** | 95% | 4% |
| pocv | 1421 | **6%** | 79% | 14% |
| pocv_dvdq | 1405 | **4%** | 61% | 35% |
| pocv_dvdq_dqdv | 1465 | **1%** | 97% | 2% |

- **flat valley** — 같은 J(허용 `j_tol`) 안에서 해가 `p_tol` 보다 멀다. 이 solver·restart 예산에서 관측된 **실용적 flatness 신호**이며, 데이터가 그 조합을 구분하지 못한다는 구조적 증명은 아니다.
- **multimodal** — J가 다른 국소최소가 여럿 잡혔다. **optimizer difficulty 와 일치하는 관측**이며, 목적함수의 고유 정보량 부족과 분리되지 않는다.
- **unique min** — 관측된 restart 범위에서 다른 동등해를 찾지 못했다. 전역 유일해의 증명이 아니다.

*분류 임계와 예산: `j_tol`·`p_tol`·restart 5개 (`src/scoring.py`).*

> ⚠ **`pocv_dvdq_dqdv`의 multimodal이 97%로 극단적입니다.** flat valley 판정은 restart 2개 이상이 같은 J에 닿아야 성립하므로, 이렇게 지형이 울퉁불퉁하면 flat valley가 있어도 **관측되지 않습니다.** 이 목적함수의 낮은 flat valley 값을 "degeneracy가 적다"로 읽으면 안 됩니다. (예전에는 여기서 Hessian을 대안으로 안내했으나, 그 지표도 eps 미수렴·안장점 혼입·가설과 다른 부호 규약으로 근거가 되지 못합니다 — F33.)

> ⚠ `degeneracy_summary.yaml`의 `restart_conditioned` 블록에 있는 `agree_frac`과 `p_spread`는 인용하지 마세요. adaptive 조기 종료 때문에 `agree_frac`은 restart를 5까지 간 조건에서 **정의상 0**이고, `p_spread = 0`은 qualifying restart 가 하나였거나 **여러 restart 가 같은 파라미터에 수렴한** 경우 모두 가능하므로 단독으로 해석하지 마세요. 위 표가 그 자리를 대신합니다.

## 기준 곡선 비교 — Case 1 (전 범위 half-cell) vs Case 2 (격자 곡선)

> ⚠ **이것은 reference 단독의 인과효과가 아닙니다.** 두 실행은 기준 곡선 외에 bounds preset·초기값 `p_ini`·half-cell cache/recipe·mode 변환도 함께 다릅니다. 따라서 아래 수치는 **두 reference-specific fitting pipeline 에서 관측된 값**으로만 읽어야 하며, reference 단독 효과를 주장하려면 나머지 축을 통제한 별도 대조가 필요합니다. 아래 `reference별_허용차이`·`_인과범위` 를 함께 보세요.

| artifact | 경로 | provenance |
|---|---|---|
| grid | `results/grid_fit_v4` | ✅ 통과 |
| halfcell | `results/halfcell_fit_v4` | ✅ 통과 |

공통 1476조건 (전체 3069 중, grid 기준 복원가능군으로 맞춤)

| objective | degeneracy | (바이어스 보정) | 평균 max-mode \|err\| |
|---|---|---|---|
| pOCV only | 59% / 78% | 48% / 67% | 4.2%p / 4.7%p |
| pOCV + dV/dQ  (33p 기존) | 7% / 62% | 6% / 15% | 1.4%p / 2.5%p |
| pOCV + dV/dQ + dQ/dV  (34p 개선) | 10% / 63% | 5% / 25% | 1.4%p / 2.4%p |
| dQ/dV only | 100% / 77% | 50% / 66% | 6.1%p / 5.0%p |

*(각 칸 = **Case 1 halfcell** / Case 2 grid)*

> ⚠ 두 pipeline 은 reference 외에도 다음이 다르다: ['bounds', 'bounds_preset', 'halfcell_cache', 'halfcell_meta_sha', 'halfcell_recipe', 'halfcell_sha', 'p_ini', 'reference']. 이 표는 '기준 곡선 단독 효과'가 아니라 **reference-specific fitting pipeline 의 차이**로 읽어야 한다.

> ⚠ '(바이어스 보정)' 열의 계수는 비교 모집단(공통 ∩ grid 복원가능)의 noise=0 행에서 다시 추정한 값이다 — 각 artifact 파일에 저장된 전체-모집단 보정과 다를 수 있다. halfcell 쪽 '복원가능'은 측정이 아니라 고정값이므로(아래 참조) 기저는 keep 으로만 제한된다.

> ⚠ halfcell 쪽의 "복원불가 0%"는 **측정이 아닙니다.** `src/scoring.py`가 `reference != "grid"`이면 `recoverable=True`로 고정합니다(전 범위 테이블이라 창 부족이 없다는 물리적 근거). 그래서 위 표는 **두 실행의 공통 조건 중 grid 기준에서 복원가능한 것**으로 행 수를 맞춰 비교한 것입니다.

## dQ/dV 가중치 — 임의 튜닝이 아니라는 근거

`w_dqdv`를 [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]로 훑어 degeneracy 비율이 최소가 되는 값을 찾았다 (층화 표본 468조건, restart 5).

- 노이즈 평균 최적: **w_dqdv = 0.0** (degenerate_frac_corrected = 15.2%), 기본값 w=1.0일 때 30.0%
- noise=0.0: 최적 w = 0.0 (15.2%, n=79)
- noise=0.001: 최적 w = 0.0 (13.9%, n=79)
- noise=0.005: 최적 w = 0.0 (16.5%, n=79)

모든 노이즈 수준에서 같은 w가 최적 — 단일 값 채택 근거 있음.

> sweep은 본 실행과 같은 설정으로 돌렸습니다 — 두 run_spec 의 optimizer·warm_start·bounds·reference·v_col 대조로 확인 (warm_start=True, restart 5). `w=0`은 `pocv_dvdq`와, `w=1`은 `pocv_dvdq_dqdv`와 정의가 같으므로 위 표의 두 끝점은 목적함수 비교표와 일치해야 합니다 — `tools/check_sweep_consistency.py`가 확인합니다.

결과: 실행 디렉터리의 `wsweep/objectives_optimized.yaml` — configs/ 로의 승격은 검토 후 커밋으로 한다 (F79)

## 그림

- `results/grid_fit_v4/figures/gap_recovery_pocv.png` — gap_pocv
- `results/grid_fit_v4/figures/gap_recovery_pocv_dvdq.png` — gap_pocv_dvdq
- `results/grid_fit_v4/figures/gap_recovery_pocv_dvdq_dqdv.png` — gap_pocv_dvdq_dqdv
- `results/grid_fit_v4/figures/gap_recovery_dqdv_only.png` — gap_dqdv_only
- `results/grid_fit_v4/figures/objective_panel_noise0.png` — noise_0
- `results/grid_fit_v4/figures/objective_panel_noise0.001.png` — noise_0.001
- `results/grid_fit_v4/figures/objective_panel_noise0.005.png` — noise_0.005
- `results/grid_fit_v4/figures/weight_sweep.png` — weight_curve

## 재현

```bash
./scripts/setup_env.sh && source .venv/bin/activate
./run.sh --mode verify
./run.sh --mode grid --config configs/grid_fine.yaml --nproc $(nproc) --out results/grid_curves_v4
./run.sh --mode fit   --in results/grid_curves_v4 --out results/grid_fit_v4 --nproc $(nproc) --objective pocv,pocv_dvdq,pocv_dvdq_dqdv,dqdv_only --n-restarts 5
./run.sh --mode score --in results/grid_fit_v4

# Hessian 절은 이 재현 체인에 들어 있지 않습니다 (A·B 미수정).
#   분리배치에서 hessian 모드는 곡선을 찾지 못하고, 실행하면
#   degeneracy_summary.yaml 을 변이시켜 이 보고서를 stale 로 만듭니다.
./run.sh --mode wsweep --in results/grid_curves_v4 --out results/grid_fit_v4/wsweep --nproc $(nproc) --w-grid 0.0,0.25,0.5,0.75,1.0,1.25,1.5,1.75,2.0 --w-stride 2 --n-restarts 5
python -m src.halfcell --config configs/base.yaml --method ocp --force --verify
./run.sh --mode fit   --in results/grid_curves_v4 --out results/halfcell_fit_v4 --nproc $(nproc) --objective pocv,pocv_dvdq,pocv_dvdq_dqdv,dqdv_only --reference halfcell --bounds halfcell --n-restarts 5
./run.sh --mode score --in results/halfcell_fit_v4
./run.sh --mode report --in results/grid_fit_v4 --compare results/halfcell_fit_v4
```

> **재현 범위**: 위 명령은 이 산출물의 서명된 fit(objective·restart·clean/noisy·adaptive·warm start·reference·bounds preset) · weight sweep(w_grid·stride·restart) · half-cell 기준 곡선(method) 과 Case 1↔2 비교 설정을 복원합니다. 아직 명령으로 내보내지 않는 축은 sweep 의 bounds·reference·tol·optimizer method · **Hessian 절 전체**(기본 eps 포함 — 명령을 싣지 않습니다) 입니다 — 해당 절은 `manifest.yaml` 의 `run_spec` 을 직접 보고 맞춰야 합니다.

관련 문서: `docs/06_REVIEW_DECISIONS.md`(해석 규칙), `docs/07_LAM_LLI.md`(열화모드 정의), `docs/GPU_NOTES.md`(GPU 판정)
