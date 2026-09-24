# LHS 130 인계표 적대 리뷰 — 두께·공극률·상 부피분율

> ⚠ 이 파일은 Codex 판정문 **원문 보존본**이다 (사용자가 2026-09-25 에 붙여 넣은 그대로).  요청서 =
> `docs/reviews/codex_request_lhs_porosity_thickness_20260924.md`.  우리 쪽 대응 (수용 · 검증 · 원장 등재) 은
> `docs/reviews/lhs_handover_judgments_20260924.md` J18 과 `docs/reviews/findings.json` `HND-01` ~ `HND-06`.
> 본문의 GitHub 링크 · 리뷰어 작업공간 파일 (`lhs_handover_evidence_20260924/` 아래) · LIGGGHTS 공개 소스 커밋은
> 리뷰어 쪽 자료라 이 리포에 없다 — 문서 참조 검사 예외는 `docs/reviews/doc_refs_allowlist.tsv` 에 등재.

검토일: 2026-09-24~25 KST  
대상: `claude/stoic-knuth-NObVQ` · **425cee2222f80520bf1e6e457bf17491cfb821be**  
범위: 정의·수확·인계 계약. 설계 130점 재심, 시뮬레이션, 생산 코드 수정, Git 상태 변경은 하지 않았다.

## 0. 결론

**현행 인계표를 ‘물리적 전극 구조의 ML 타깃’으로 외부 배포하는 것은 HOLD.** 데이터 130행을 폐기하거나 다시 뽑으라는 뜻은 아니다.

- 주 두께는 **동일 프레임의 플래튼–바닥 기준면 간격**이다.
- 등록된 (가)는 그대로 보존하되, **명목 구 부피 / 틀 간격 부피**라는 이름과 규약으로 내보낸다. 이것을 그대로 공간 점유율·실험 공극률로 인증하지 않는다.
- **(나) ≈ 단단한 바닥에서 얻었을 값**은 REJECT. 산술 변환이지 접촉역학의 반사실 계산이 아니다.
- ‘1.98r’는 공개 구현에서의 접촉 겹침 1.98r가 아니다. **양면 평면 아래쪽의 점착–중력 평형**이라는 매우 구체적인 후보가 9건 좌표를 반올림 정밀도까지 재현한다. 단 실제 LHS 실행 바이너리·덱 전체·접촉 이력을 확보하지 못했으므로 **원인 확정은 아니다**.
- 음수 공극률을 기록 전용으로 두더라도, 같은 분모의 **φ_SE+φ_AM>1**이 학습 타깃에 남는다. 현행 생성기는 이를 `OK`로 내보내고 벽 진단은 버린다. ‘기록만 하면 안전하다’는 처방이 현재 인계 경로에는 구현돼 있지 않다.

| 질문 | 판정 | 핵심 |
|---|---|---|
| Q1 주 값 | **REVISE** | (가)는 명목 규약값으로 유지. (나)의 hard-bottom 해석은 REJECT. (다)도 합집합 공극률은 아님 |
| Q2 두께 | **ACCEPT, 한정** | 같은 프레임의 벽 기준 간격. 실험의 하중·상태·측정 구간을 맞춰야 함 |
| Q3 덱의 바닥 확인 | **REVISE** | 현재 함수는 과거 명령의 존재를 검사할 뿐, 최종 활성 벽을 검증하지 못함 |
| Q4 관통을 기록만 | **REJECT** | 중심 통과·완전 이탈은 정상 압입과 구분해야 함. 발생 경위·물리 적격성은 미확인 |
| Q5 음수 처리 | **REVISE** | 원값 보존 + 타깃별 적격성. 0 접기·행 전체 삭제·union으로 무표지 교체 금지 |
| Q6 웹앱/기존 코퍼스 | **REVISE** | 재사용 전 전수 provenance 감사 필요. ‘플래튼−고체 윗면’ 하나로는 부족 |
| Q7 경계의 다른 영향 | **REVISE** | 상별 cap, coverage의 모집단, τ의 아래 밴드가 서로 다른 공간을 보고 있음 |

### 증거의 등급과 한계

1. 고정 커밋의 수확 JSON **130개**, 설계 CSV, 코호트 TSV, 교차검사 TSV를 직접 읽고 집계했다. 문서의 요약 숫자를 답으로 복사하지 않았다.
2. **입자수 × 설계 반지름의 구 부피**로 φ를 별도 재계산했다. JSON φ와 최대 절대차 **2.220446049250313e−16**. 다만 반지름을 원 덤프에서 다시 읽은 검증은 아니다.
3. 원 atom/contact/STL/LHS 덱 전체 130세트는 이 작업 공간에 없다. SHA **문자열**은 코호트와 atom/contact/deck 각각 130/130 일치한다. 이를 원파일 해시 재검증·원 덤프 재수확 성공으로 표현하지 않는다.
4. 생산 Python의 실제 순수 함수를 합성 입력으로 호출했다. `dem_analysis_core`는 networkx가 없는 환경에서 필요한 함수의 **변경하지 않은 AST 본문**만 불러왔다. DEM·MPM·접촉 솔버는 실행하지 않았다.
5. LIGGGHTS 공개 소스는 별도 커밋 `3d5c00f20519e6bb6eb6756f51f1ad36564e649d`로 고정했다. 이것이 사용한 실행 파일과 같다는 증거는 아직 없다.
6. **데이터 커밋의 판단문은 J16까지이며 J17이 없다.** 요청 본문에 추가된 저자 의도는 검토했지만, 이를 그 커밋에 이미 봉인된 사실로 간주하지 않았다. 같은 커밋의 LHS-14도 `open`이다.

재현 자료는 이 판정문과 같은 작업 공간의 `lhs_handover_evidence_20260924/`에 있다. 실행 명령은 §9.

## 1. 독립 재집계 — 대체로 맞지만 ‘계산 성공’과 ‘물리적 적격’은 다르다

단위: 공극률 %, 공극률 차이 %p, 두께 µm. 분위수는 선형 보간이다.

| 양 | 최소 | 중앙 | p90 | 최대 |
|---|---:|---:|---:|---:|
| (가) ε | −2.434742 | 9.885653 | 21.968483 | 27.073355 |
| (나)−(가) | 0.185846 | 0.607316 | 1.064575 | 2.528347 |
| ΔH | 0.088235 | 0.232753 | 0.411757 | 1.072400 |
| 바닥 밖 / ΣV, % | 0.187904 | 0.594773 | 1.446247 | 4.388617 |
| 위판 밖 / ΣV, % | 0.021053 | 0.080546 | 0.163088 | 0.213956 |
| 플래튼−고체 윗면, µm | −1.213300 | −0.519150 | −0.369940 | −0.269300 |

설계군별 (가) 중앙: bimodal **9.321460**, mono_AM_S **12.462088**, mono_AM_P **10.996257** %. (나)−(가) 중앙은 각각 **0.602901 / 0.476887 / 1.201691 %p**. 군별 차이를 공통 상수로 보정할 수 없다.

- 바닥 아래 중심: **42케이스, 682입자** = AM_S 618 + SE 62 + mono AM 2.
- 완전히 바닥 아래: **15케이스, 80입자**.
- 완전히 위판 위: **3케이스, SE 7입자**. 바닥/위판 중 어느 쪽이든 중심 이탈이 있는 경우는 **43케이스**.
- 음수: (가) **18**, (나) **16**, (다)를 계산해도 **16**.
- τ: `ELECTRODE_BAND_EMPTY=110`, `NOT_PERCOLATING=6`, `OK=14`. **110건 모두 아래 밴드가 비고**, 위 밴드도 빈 것은 그중 2건이다.
- 교차검사 TSV의 LHS 130행은 SAME, 최대 잔차 **5.595524044110789e−14 %p**. 하지만 [scripts/lhs_phi_crosscheck.py:41](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/425cee2222f80520bf1e6e457bf17491cfb821be/scripts/lhs_phi_crosscheck.py#L41)는 같은 원자 집합·같은 plate_z를 두 산식에 공급한다. **웹앱의 실제 파일 선택 경로까지 검증한 시험이 아니다.**

요청서의 p90 21.9 / 1.43은 분위수·반올림 규칙을 명시해 위 수치와 정리하면 된다. 판정을 바꿀 규모의 오류는 아니다.

## 2. Q1 — (가)를 보존하되, (나)를 단단한 바닥 보정으로 쓰지 말 것

### HND-01 · P1 · ‘pushback = hard-bottom’ 해석은 성립하지 않는다

**무너지는 결론:** (나)로 바꾸면 LHS를 바닥 AM인 생산 코퍼스와 같은 물리 규약으로 비교할 수 있다는 주장.

위치: [scripts/lhs_descriptor_harvest.py:307](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/425cee2222f80520bf1e6e457bf17491cfb821be/scripts/lhs_descriptor_harvest.py#L307)의 분자와 [scripts/lhs_descriptor_harvest.py:337](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/425cee2222f80520bf1e6e457bf17491cfb821be/scripts/lhs_descriptor_harvest.py#L337)의 pushback. 판단문 J14의 ‘빈틈 보존’ 해석도 분모를 밝혀야 한다.

A=LxLy, V=AH, S=ΣV_i, W=벽 밖 cap들의 합이라고 두면:

```
(가) εa = (V−S)/V
(나) εb = (V+W−S)/(V+W)
(다) εc = (V−S+W)/V

(나)의 공극 부피 = (다)의 공극 부피 = V−S+W
(가)의 공극 부피 = V−S
εb = εc / (1+W/V)
```

즉 ‘빈틈 보존’은 **(다)의 잘라낸 공간과 비교할 때만** 맞다. (가) 대비 공극 부피는 W만큼 증가한다. 세 식은 모두 구 부피의 **중복 합산**을 유지하며, 실제 공극 합집합을 계산하지 않는다.

**실제 함수 반례:** 단위가 일관된 합성 상자 A=1, H=2, r=0.5인 구 하나를 z=1에서 z=−1.2로 옮긴다.

| 위치 | (가) ε | (나) ε | (다) ε |
|---|---:|---:|---:|
| 구 전체가 틀 안 | 73.82006122% | 73.82006122% | 73.82006122% |
| 구 전체가 바닥 밖 | **73.82006122%** | 79.25190087% | **100%** |

원 공간은 완전히 비었는데 (가)는 불변이다. 따라서 (가)의 정확한 의미는 **전체 입자의 명목 물질 부피를 틀 부피로 나눈 장부 값**이지, 틀 내부의 실제 점유율이 아니다. 원값의 보존은 타당하지만 해석을 제한해야 한다.

**주 값 권고**

- 등록 타깃의 연속성과 원자료 보존 목적: **(가)**. `phi_*_sphere_nominal_gap` 및 `porosity_spheresum_nominal_gap_pct`로 정의하고 기존 등록 열은 명시적 alias로 남긴다.
- 틀 내부에 실제로 포함되는 **구 표현의 부피 합**을 묻는 목적: **(다)**가 ROI 정의에는 맞다. 밖의 입자를 삭제하는 것이 아니라 집계 공간을 자르는 것이다. 다만 입자 간 중첩 때문에 아직 진짜 공극률은 아니다.
- 실험 공극률을 주장하는 목적: **셋 중 어느 것도 지금 상태로 충분하지 않다.** ROI 안의 합집합·물질부피 보존·압축 상태 중 어떤 정의를 대응시키는지 먼저 정해야 한다.
- **(나)는 대안 산술 지표로만** 남긴다. 생산 코퍼스 보정값·오차막대·실제 hard-bottom 두께라는 이름은 사용하지 않는다.

얇은 층의 충전율을 η로 놓고 **나머지 침대를 고정한다는 추가 가정**을 하면 ΔH=W/(ηA), η≤1이므로 W/A는 그 제한된 쌓기 모형의 최소 증가량이다. 실제 벽 재질 변경은 재배열·하중망·점착·벽 마찰·압밀량까지 바꾼다. 따라서 이 부등식을 실제 hard-bottom 재압축 결과의 하한으로 옮길 수 없고, **실제 편향 방향은 모른다**.

바닥의 SE 재질은 사용자 의도에 부합할 수 있다. 그러나 `primitive type SE`는 접촉 물성 선택이지 유한 두께·공극·변형장·SE 체적을 가진 분리막을 만드는 명령이 아니다. [공식 wall/gran 설명](https://www.cfdem.com/media/DEM/docu/fix_wall_gran.html)은 이를 입자–벽 접촉 모델로 정의한다. ‘SE 접촉물성을 쓴 평면 바닥 proxy’까지가 방어 가능한 표현이다.

**해결 증거:** 인계 사전의 이름·단위·분모·영역 정의, b의 반사실 주장 삭제, LHS/생산의 서로 다른 boundary_model_id. 물리적 hard-bottom 환산을 유지하려면 별도 검증이 필요하지만 이 리뷰에서 새 런을 지시하거나 실행하지 않는다.

## 3. Q2 — 두께는 실제 기준면 간격, 다른 높이는 다른 열

**ACCEPT:** H_gap=z_plate−z_floor. 이번 130에서는 z_floor=0이라는 전제하에 H_gap=plate_z다. mesh와 atom의 동일 시점 확보는 옳은 수정이다.

- `H_pushback`: 계산된 등가 두께. **측정 두께가 아니다.**
- `H_envelope=max(z+r)−min(z−r)`: 명목 구의 외피 높이. 이탈 입자·극값 하나에 지배될 수 있다.
- `max(z+r)`만은 두께가 아니다. 반드시 기준 바닥을 적어야 한다.
- 실험 비교: **같은 가압 상태의 기준면 간격**이라면 H_gap이 가장 직접적이다. 마이크로미터의 측정 하중·제하 여부, SEM의 절단/제하 상태, 집전체·분리막 포함 여부가 다르면 즉시 등치할 수 없다. 이 정보는 이번 증거에 없어 **모른다**.

J3의 분모 일치는 옳다. (가)는 S/(AH_gap), (나)는 S/(AH_pushback), (다)는 (S−W)/(AH_gap)로 한 묶음이어야 한다. 단 **내부적으로 닫힌다고 올바른 물리량이 되는 것은 아니다.**

STL 꼭짓점 평균이 평판 높이가 되는 조건도 필요하다. [scripts/lhs_descriptor_harvest.py:217](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/425cee2222f80520bf1e6e457bf17491cfb821be/scripts/lhs_descriptor_harvest.py#L217)는 평판·법선·유한값 검사를 하지 않는다. **z=0과 z=2의 삼각형을 함께 넣어도 높이 1을 받아들인다**. 실제 130 STL이 이렇다는 주장은 아니며, ‘평판임을 보증하는 검사’가 없다는 반례다.

**고칠 것:** 별도의 `plate_planarity_span`·평판 방향 검사·단위/scale·timestep/출처, H_gap/H_envelope/H_pushback 분리. 임의 높이 보정이나 외피로의 조용한 fallback은 금지한다.

## 4. Q3 — check_deck_floor는 활성 벽 증명이 아니다

### HND-02 · P2 · 삭제된 벽·교체 전 벽·부분 그룹 벽이 모두 통과한다

위치: [scripts/lhs_descriptor_harvest.py:243](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/425cee2222f80520bf1e6e457bf17491cfb821be/scripts/lhs_descriptor_harvest.py#L243)~286. 발견한 모든 primitive zplane 중 **min(z)**를 고른다.

실제 함수 호출 결과:

```
fix floor all ... primitive type 3 zplane 0
unfix floor
run 100
→ z=0 반환                    # 실제 활성 floor 없음

fix floor all ... zplane 0
unfix floor
fix floor all ... zplane 2
run 100
→ z=0, n_zplane_walls=2 반환  # 최종 floor는 2

fix floor AM_only ... zplane 0
→ z=0 반환                    # 모든 상을 구속한다는 증거 없음
```

**무너지는 결론:** 이 함수가 통과했으므로 원 덤프 시점에 모든 입자의 실제 바닥이 0이었다는 일반적 보증.

이 반례가 현재 130 덱에 존재한다고 확인한 것은 아니다. mesh-only·변수 z는 현재 거부하므로 그 자체가 조용한 0 대입은 아니다. 위험은 과거 primitive 명령이 함께 있을 때 mesh·unfix·재정의·조건 분기를 무시하고 통과하는 경우다.

**고칠 것:** 범용 LIGGGHTS 해석기를 급조하지 말고 지원하는 덱 문법을 제한한다. 활성 fix ID의 생명주기, group, wall type의 상 사상, restart/include/조건 분기의 처리 범위를 정의한다. 지원하지 않는 동적 규약은 ‘검증 불가’로 분리하고 원 실행 로그/최종 활성 경계 증거를 요구한다. 바닥 좌표 확인과 관통 입자의 물리 적격성 검사는 **서로 다른 검사**다.

**해결 증거:** 위 세 변이체가 거부되거나 최종 벽으로 정확히 해석되고, 실제 LHS 덱 전체의 지원 문법 검사/활성 경계 증거가 봉인될 것.

## 5. Q4 — 1.98r의 정체: 아래쪽 점착 평형을 조건부로 재현했다

### HND-03 · P1 · ‘작은 부피 몫이므로 정상 분리막 압입으로 기록만’은 불충분

기존 LHS-13/14의 **해석 및 적격성 문제를 강화하는 증거**다. 새 수치 결함 130건을 확정한 것은 아니다.

### 5-1. 기하학적 깊이와 솔버 접촉 겹침을 분리해야 한다

공개 소스의 Plane은 중심의 **양쪽 거리**를 쓴다:
[src/primitive_wall_definitions.h:133](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/primitive_wall_definitions.h#L133),
부호 전달은 [src/fix_wall_gran.cpp:1062](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/fix_wall_gran.cpp#L1062) 및 [src/fix_wall_gran_base.h:181](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/fix_wall_gran_base.h#L181).

```
바닥 아래 cap 깊이 d = r−z                 [바닥 0]
접촉모델의 겹침 δn = r−|z|                [접촉일 때]
```

| 중심 위치 | d/r | 접촉 δn/r |
|---|---:|---:|
| z=+0.98r | 0.02 | 0.02 |
| z=−0.98r | **1.98** | **0.02** |
| z=−1.20r | 2.20 | 접촉 없음 |

따라서 `overlap_over_r`라는 현재 필드 이름은 중심이 평면을 넘은 뒤 접촉 겹침과 달라진다. `outside_cap_depth_over_radius`로 구별하고, 실제 접촉 겹침은 별도 계측해야 한다. 완전히 아래에 있는 입자는 ‘더 큰 압입’이 아니라 해당 평면의 접촉 범위를 벗어났다. 반발력 방향도 평면의 어느 쪽인지에 따라 바뀐다.

### 5-2. 정확히 반복되는 자리의 수치 재현

[src/normal_model_hooke_hysteresis.h:138](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/normal_model_hooke_hysteresis.h#L138)의 강성과 163~173의 포화 이력 가지에서:

```
k2 = q k1
δ_lim = q/(q−1) · 2φf r
Fn = k2(δn−δ_lim) + k1 δ_lim
   = k2(δn−2φf r)

평면 아래쪽, 정지, 다른 수직 접촉력 없음:
−Fn−mg = 0
δn/r = 2φf − mg/(k2 r)
d/r  = 2−2φf + mg/(k2 r)
```

입력: E_AM=1.4e8, E_SE=1.35e6 Pa(sim), ν=.25/.30, ρ_AM=4800 kg/m³, characteristicVelocity=2 m/s(sim), g=9.81 m/s²(sim). **추가 조건 q=3, φf=.01**은 저장소 생산 참조 덱 [docs/data/phase_a_6mah/in.real_4.liggghts:57](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/425cee2222f80520bf1e6e457bf17491cfb821be/docs/data/phase_a_6mah/in.real_4.liggghts#L57)에 실재한다. 이 값들이 각 LHS 덱에도 동일한지는 아직 직접 확인하지 못했다.

혼합 유효 E*=**1,468,923.809292497 Pa(sim)**. 합성식은 [src/global_properties.cpp:432](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/global_properties.cpp#L432)다.

| 실제 반지름 | k1, N/m(sim) | 예측 d/r | 예측 중심 z, µm | JSON 중심 z, µm |
|---|---:|---:|---:|---:|
| 1 µm | 865.1678303893 | **1.980075993638** | **−0.980075993638** | −0.980076 |
| 0.5 µm | 432.5839151947 | **1.980037996819** | **−0.490018998410** | −0.490019 |

일치하는 9건:
`029,037,056,075,079,085,093,107,110` (모두 lhs00_ 접두어).
1 µm 7건, 0.5 µm 2건. 최대 중심 좌표 차이 **6.37e−9 µm**로 기록 정밀도보다 작다.
실제 예: [docs/data/lhs_descriptors_20260924/lhs00_037.json:43](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/425cee2222f80520bf1e6e457bf17491cfb821be/docs/data/lhs_descriptors_20260924/lhs00_037.json#L43).

**매우 강한 기전 후보**지만, 실제 이력·바이너리 인증을 대신하지 않는다. q와 φf를 이 9건에 맞춰 적합한 것은 아니며, 저장소 참조 덱에 있는 값을 대입했다. 포화 이력 가지 도달, 인력 허용, 최종 정지 및 다른 수직력 부재를 조건으로 쓴 해석이다. 관통이 처음 발생한 순간·삽입 문제인지·시간간격 문제인지·벽을 통과한 뒤 이력의 이동인지까지는 **모른다**. 그 원인을 이 최종 좌표로 역확정하지 않는다.

### 5-3. 처방: 임의 깊이 컷과 ‘전부 OK’의 양자택일을 버릴 것

- ½r_max 컷 제거는 유지한다. 물리적 근거 없는 58건 탈락을 되살릴 이유는 없다.
- 동시에 **중심 평면 통과**, **완전 이탈**, **접촉 범위 안 정상 방향의 겹침**을 별도 상태로 구분한다. 평면이라는 기하 경계는 임의의 깊이 허용치와 다르다.
- 43케이스의 이탈 진단은 원값과 함께 남기고, 물리적 전극 타깃 사용은 경계 검증 전 `HOLD_BOUNDARY`로 둔다. 나머지 87건이 자동 합격이라는 뜻도 아니다.
- 소량의 부피는 φ의 작은 수치 영향만 제한한다. 힘의 지지·접촉망·극값으로 정의한 τ 밴드에 주는 영향까지 작다는 보증은 아니다.
- 기록을 남기는 **자료 보존**은 가능하다. 실험 분리막 위 전극을 검증했다는 **물리 적격성 부여**는 아직 불가다.

**해결 증거:** 동일 실행 바이너리/소스 SHA, 실제 LHS의 q·φf·점착 계수·중력 구간, 해당 입자의 마지막 여러 프레임과 가능하면 벽/입자 힘·접촉 이력. 기존 출력으로 먼저 확인할 수 있다. 새 캠페인 재실행 여부는 그 뒤의 결정이다.

## 6. Q5 — 음수는 지우지 말고, 타깃 자격을 따로 정할 것

### HND-04 · P1 · 벽 진단과 적격성이 실제 인계표에서 사라진다

기존 LHS-15를 수리하는 과정에서 반드시 닫아야 하는 **실제 소비자 경로**다.

- 수확기는 [scripts/lhs_descriptor_harvest.py:615](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/425cee2222f80520bf1e6e457bf17491cfb821be/scripts/lhs_descriptor_harvest.py#L615)에서 φ와 porosity 상태를 무조건 `OK`로 둔다.
- [scripts/lhs_design_dataset.py:731](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/425cee2222f80520bf1e6e457bf17491cfb821be/scripts/lhs_design_dataset.py#L731)~813의 `build_handover`는 그 상태로 값을 채운다.
- `HANDOVER_EXTRA`에는 **wall_record / deck_floor / 바닥 이탈 수 / 물리적 학습 적격성**이 없다.
- 기본 수확 디렉터리도 [scripts/lhs_design_dataset.py:1238](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/425cee2222f80520bf1e6e457bf17491cfb821be/scripts/lhs_design_dataset.py#L1238)에서 **20260919**다. 이는 요청서가 알고 있는 상태이며, 기본값만 바꿔도 위 진단 유실은 남는다.

**실제 함수 반례: lhs00_005를 인계 함수에 통과시킴**

```
phi_se = 0.5135813340456643
phi_am = 0.4996409958699752
porosity = −1.3222329915639541 %
phi_se_status = OK
porosity_status = OK
wall_record / boundary_model_id / ml_target_status = 인계 열에 없음
```

따라서 ‘ε는 RECORD_ONLY이므로 학습 안전’은 거짓이다. 두 φ는 합 **1.013222329916**을 그대로 타깃으로 낸다.

**무엇이 음수의 원인이라고 말할 수 있나**

벽 밖 부피를 뺀 (다)도 16건 음수다. 그 경우 S−W>V이므로 **ROI 안의 명목 구 부피 합에도 중복이 필요하다**는 결론은 맞다. 그러나 ‘이건 벽 문제가 아니고 입자 겹침 문제뿐’은 너무 강하다. 벽 경계가 압밀·재배열과 입자 간 겹침을 유발했을 수 있어 원인 분리는 안 된다.

최저 사례 [docs/data/lhs_descriptors_20260924/lhs00_054.json:18](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/425cee2222f80520bf1e6e457bf17491cfb821be/docs/data/lhs_descriptors_20260924/lhs00_054.json#L18):

```
φ_SE + φ_AM = 1.024347416558
εa = −2.434741655767 %
εb = −1.687510600717 %
εc = −1.699910946828 %
```

이 사례는 중심의 벽 이탈이 없다. 관통 가드 하나로 음수를 해결할 수 없다는 반례이기도 하다.

**권고**

1. **130행 전부 원값 보존**. 음수를 0으로 접지 않는다. 음수라는 이유로 coverage 등 다른 정상 타깃도 함께 삭제하지 않는다.
2. `calculation_status`와 `physical_target_status`를 분리한다. 계산 가능한 명목 지표와 [0,1]의 공간 점유율은 같은 타깃이 아니다.
3. 등록 식 자체를 예측하는 **DEM 명목 지표 에뮬레이터**라면 음수/φ합>1도 그 규약의 유효 출력으로 학습할 수 있다. 그 모델을 ‘실제 공극률 예측기’로 소개하지 않는다.
4. 물리적 공극률/부피분율을 예측하려면 적격 정의를 별도로 검증한다. 그때까지 해당 물리 타깃은 보류하며, 기존 명목값은 남긴다. **양수 112행만 뽑아 원 130 설계의 무편향 성능이라고 보고하지 않는다.**
5. 제외/보류율을 설계족·AM 함량·입자크기별로 공개하고 적용영역을 제한한다. QC 표지를 공변량으로 넣는 것만으로 잘못된 라벨이 치유되지는 않는다.
6. 이미 음수 사례를 제외해 온 생산 코퍼스와 통합하지 않는다. 필터와 물리 경계가 둘 다 다른 도메인이다.

### HND-05 · P2 · 현재 ε_union은 진짜 union의 대체재가 아니다

위치: [scripts/dem_analysis_core.py:51](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/425cee2222f80520bf1e6e457bf17491cfb821be/scripts/dem_analysis_core.py#L51)~107. S−Σ(pair lens)에서 끝난다. 삼중 이상 교집합, 완전 포함, 벽 clipping이 없다.

실제 함수에 반지름 1의 구 3개, 쌍 거리 0.2(정삼각형으로 실현 가능)를 넣으면:

```
reported V_union = 1.878672406847
union의 자명한 하한(구 하나) = 4.188790204786
```

하한보다 작으므로 합집합일 수 없다. 구 3개가 동심이면 d≤0인 쌍을 건너뛰어 **12.566370614359**, 참값은 **4.188790204786**이다.

이 극단 합성 예가 130에 실제로 존재한다는 주장은 아니다. **‘union’이라는 이름만 보고 물리적 라벨로 교체하면 안 된다**는 계약 반례다. 필요한 것은 ROI 안의 구 합집합을 다루는 별도 계산(해석/기하/수렴 확인된 복셀 방식 등)이다. AM–SE 중첩의 상별 점유 배분도 정의해야 φ_AM+φ_SE+ε=1이 의미를 갖는다. 합집합 공극률만 바꾸고 기존 φ 두 개를 남기는 혼합은 금지한다.

## 7. Q6 — 기존 코퍼스는 전수 provenance 감사 후 재사용

SELF-47/48/49의 핵심 진단에 동의한다. 다만 **전수 '플래튼−고체 윗면' 체크만으로 통과시키지는 않는다.**

실제 함수 재현:

| 동일 입자: z=1, r=.5 | core.get_plate_z | recompute.get_plate_z |
|---|---|---|
| mesh 없음 | **1.0**, estimated_center | **1.5075** |
| mesh_info에 과거 plate_z=10 | **10** | **10** |

출처: [scripts/dem_analysis_core.py:110](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/425cee2222f80520bf1e6e457bf17491cfb821be/scripts/dem_analysis_core.py#L110), [scripts/recompute_porosity_dual.py:185](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/425cee2222f80520bf1e6e457bf17491cfb821be/scripts/recompute_porosity_dual.py#L185)~229.
두 함수는 무메시에서 서로 다른 양을 내고, 높은 과거 plate는 둘 다 수용한다.
[scripts/parse_liggghts.py:294](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/425cee2222f80520bf1e6e457bf17491cfb821be/scripts/parse_liggghts.py#L294)~324는 atom/contact/mesh를 각각 선택한다.
[scripts/analyze_contacts.py:508](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/425cee2222f80520bf1e6e457bf17491cfb821be/scripts/analyze_contacts.py#L508)는 porosity>25만 경고하고 음수에 대한 대응이 없다.

**지금 고쳐야 하는 최소 계약**

- atom/contact/plate의 시점과 소스 SHA를 결합. 같은 시점 STL 또는 **동일 시점의 검증된 플래튼 위치 이력**을 사용하고 출처를 구분한다.
- 원 mesh 부재 시 `UNKNOWN_THICKNESS`. 최고 중심/고체 외피를 측정 플래튼으로 바꿔 부르지 않는다.
- STL 평판·유한값·단위·벽 기준 및 실제 LxLy를 확인한다.
- 음수 ε, φ합>1, 중심/완전 이탈, cap 합, plate gap을 **보이는 진단**으로 내보낸다. 자동 보정은 하지 않는다.
- 과거 산출물을 덮어쓰지 않고 `measurement_protocol_id`와 이전/새 값을 함께 보존한다.

코퍼스 감사는 행마다 소스/시점/기준면/scale → 원 입자수·부피 → 새·옛 φ/ε 차이 → 경계 QC 순서다. 양의 큰 plate gap은 좋은 의심 신호지만 보편적인 오류 증명은 아니다. 반대로 음의 gap도 옳은 시점의 보증이 아니다. 임의 `±몇 µm`나 `1.005` 보정으로 적격을 만들어서는 안 된다.

현재 LHS 130의 `SAME`은 두 계산식의 일치다. 이를 이미 저장된 다른 코퍼스의 입력 경로와 결과를 인증하는 증거로 확대하지 않는다.

## 8. Q7 — 경계가 달라지면 φ만이 아니라 coverage·τ도 달라진다

### 8-1. 상별 clipping에는 상별 cap 부피가 필요하다

`_wall_side`는 전체 V_out과 **중심 이탈 입자수의 상별 집계**만 저장한다. 입자수로 AM/SE의 빠진 부피를 복원할 수 없다. r³ 가중이 다르기 때문이다.

(다)의 φ를 내려면 `V_AM,out_floor`, `V_AM,out_plate`, SE의 두 값도 직접 구 적분으로 저장해야 한다. 전체 W를 AM/SE 질량비나 평균 φ비로 나누지 않는다. x,y 주기면은 잘라 버리는 외벽이 아니므로 최소영상/주기 영역 규약을 함께 유지한다.

### 8-2. coverage는 '전체 입자의 내부 AM–SE 접촉 지표'다

[scripts/lhs_descriptor_harvest.py:353](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/425cee2222f80520bf1e6e457bf17491cfb821be/scripts/lhs_descriptor_harvest.py#L353)는 z·바닥·플래튼을 인자로 받지 않는다. 따라서 어느 입자가 틀 밖으로 나갔는지에 따라 집계 대상을 바꾸지 않는다. 벽 접촉은 pair/gran/local의 입자쌍 목록에 포함되는 별도 SE 입자가 아니다.

- SE 물성 바닥과의 접촉을 **SE 입자 피복률에 이미 포함했다**고 말할 수 없다.
- 현재 피복률은 전체 dump의 AM 모집단이고, (다)의 φ는 ROI 내부를 보게 된다. 둘을 함께 제공한다면 서로 다른 모집단이라는 사실을 명시한다.
- ROI 피복률을 별도로 만들 경우 경계에서 부분 입자·노출 표면·접촉 patch를 어떻게 집계할지 먼저 정의해야 한다. 기존 등록 열을 조용히 바꾸지 않는다.
- `hertz` 별칭이 실제로 LIGGGHTS 기하 접촉면적 채널이라는 기존 `area_channel` 한정은 계속 유지한다.

### 8-3. τ 문제의 주된 실측 위치는 '위'가 아니라 '아래'다

기존 LHS-08 보류를 유지한다. 새로 같은 결함을 중복 등재할 필요는 없다.

[scripts/lhs_descriptor_harvest.py:461](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/425cee2222f80520bf1e6e457bf17491cfb821be/scripts/lhs_descriptor_harvest.py#L461)~510에서 모든 입자의 min(z−r)가 아래 밴드를 정한다. 현재 진단은 대안 **위판 인원**만 계산한다.

실제 lhs00_000:

```
전체 고체 z_lo = −1.905430 µm
밴드 두께      =  1.000000 µm
아래 밴드 끝   = −0.905430 µm
SE의 최저 표면 = −0.657750 µm
→ 아래 밴드 SE = 0
```

동시에 최대 SE 성분은 **92.5356%**, 고체 z범위 대비 span은 **96.2535%**다. 이것이 실제로 관통한다는 증거는 아니지만, 지금의 ‘밴드 빔’이 단순히 SE가 산산조각났다는 뜻도 아니다. [docs/data/lhs_descriptors_20260924/lhs00_000.json:100](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/425cee2222f80520bf1e6e457bf17491cfb821be/docs/data/lhs_descriptors_20260924/lhs00_000.json#L100).

**110건 전부 bottom empty**이므로 `alt_n_top`만 늘려서는 주된 사각지대를 못 본다. 동일 고정 geometry에서 실제 바닥/플래튼 기준의 양쪽 band 진단을 추가하고, 밴드 인원과 같은 성분 연결까지 보아야 한다. 적격 실패를 τ=0이나 σ=0으로 바꾸지 않는다. 현재 인계 함수가 τ 숫자 열을 제외하는 것은 유지할 안전장치다.

### 권고 인계 열 — 기존 값 보존 + 해석을 분리

다음은 새 표를 만들었다는 뜻이 아니라, 재생성 전에 확정할 계약 제안이다.

| 분류 | 제안 열 | 정의/용도 |
|---|---|---|
| 주 두께 | `thickness_wall_gap_um` | 같은 프레임의 z_plate−z_floor, sim×1000 |
| 등록 alias의 정본 의미 | `phi_se_spheresum_nominal_gap`, `phi_am_spheresum_nominal_gap` | 각 상의 **전체** 명목 구 부피 / LxLyH_gap |
| 기록/유도량 | `porosity_spheresum_nominal_gap_pct_RECORD_ONLY` | 100(1−두 φ 합), 독립 타깃 아님 |
| 부피 감사 | `V_*_full_um3`, `V_*_out_floor_um3`, `V_*_out_plate_um3` | *=AM/SE; 겹침 중복을 포함하는 구 합임을 명시 |
| 보조 등가 지표 | `thickness_pushback_equiv_um`, `porosity_pushback_equiv_pct` | (나), **hard-bottom 예측 아님** |
| 보조 ROI 지표 | `phi_*_clipped_spheresum_gap`, `porosity_clipped_spheresum_gap_pct` | (다), 아직 합집합 점유율 아님; 미계산이면 빈칸 |
| 외피 진단 | `solid_bottom_um`, `solid_top_um`, `thickness_envelope_um`, `plate_minus_solid_top_um` | 실험 두께의 자동 대체물 아님 |
| 경계 QC | `n_*_center_out`, `n_*_fully_out`, `outside_cap_depth_over_radius_max` | floor/plate 별; 가장 깊은 입자 ID·상·r·z도 보존 |
| 적격성 | `calculation_status`, `physical_target_status`, `hold_reason_codes`, `phi_sum_gt_one` | 숫자 산출 성공과 물리/ML 용도 허용을 분리 |
| 프로비넌스 | `measurement_protocol_id`, `boundary_model_id`, `scale`, `timestep`, 원파일 4종 SHA | atom/contact/deck/mesh; 도구 커밋도 포함 |
| coverage/τ | 기존 area_channel·분모·cap 수·tau_status + 양쪽 band 진단 | 벽을 포함하는지, 모집단과 ROI를 명시 |

벽 기록을 JSON에만 두고 CSV에서 버리면 위 계약은 실패다. 외부 전달 시 CSV 열과 데이터 사전·기계판독 계약·원 수확 JSON을 연결해야 한다.

## 9. 재현과 해제 조건

### 재현

폴더 `lhs_handover_evidence_20260924`에서 실행:

```bash
python probe_handover.py stats      # 130 JSON/설계/TSV 재계산
python probe_handover.py functions  # 실제 Python 함수의 경계·union 반례
python probe_handover.py wall       # 공개 모델 산술의 조건부 재현; 시뮬레이션 아님
python probe_handover.py export     # 실제 build_handover, 파일을 내보내지 않음
```

실행 환경: bundled Python + numpy. 정상 종료 rc=0은 **리뷰 재현 스크립트가 끝났다는 의미**이지 대상 도구에 GO라는 뜻이 아니다. `probe_output.txt`, `provenance.json`, 130개 고정 JSON과 검토용 소스 사본을 보존했다. 사본은 줄바꿈/파일 끝 개행이 정규화된 텍스트이며, 원 Git blob과의 대조에서 이 차이를 제외한 내용 일치를 확인했다. SHA를 사본의 byte-for-byte 해시로 오독하지 말 것.

### 최소 해제 조건

1. **명목 규약값의 전달과 물리적 타깃 인증을 분리**하고 (나)의 hard-bottom 해석을 철회한다.
2. 인계 경로가 최신 수확 snapshot을 명시적으로 선택하며, 벽 QC·상태·전체 source hashes·규약 ID를 실제로 전달하도록 한다. 음수/이탈 사례로 end-to-end 회귀를 남긴다.
3. 중심 통과/완전 이탈이 있는 데이터의 용도와 타깃별 HOLD를 명시한다. ‘작은 부피이므로 영향 없음’을 해제 근거로 쓰지 않는다.
4. 바닥 활성 상태와 STL 평판/시간 정합의 지원 범위를 검사 계약으로 만든다. 일반적 덱 검증인 것처럼 광고하지 않는다.
5. 기존 물리 코퍼스와 합치거나 실험 공극률로 쓰려면 별도 provenance·물리 적격 감사가 선행한다. τ의 현재 보류를 유지한다.

**새 런은 이번 리뷰의 자동 결론이 아니다.** 기존 덱·로그·최종 근방 프레임에서 1.98r 기전과 경계 상태를 먼저 확인할 수 있다. 그것으로 해결되지 않는 물리적 대응은 모른다고 남겨야 한다.

## 10. finding 요약 — 과장하지 않은 범위

| ID | 등급 | 내용 | 영향/해결 증거 |
|---|---|---|---|
| HND-01 | P1 | pushback을 hard-bottom 보정으로 해석 | 코퍼스 간 물리 등가 주장 붕괴; 등가 산술값으로 재라벨 또는 독립 검증 |
| HND-02 | P2 | check_deck_floor가 비활성/교체/부분 그룹 벽 수용 | 일반 검증 보증 붕괴; 활성 경계/지원 문법 음성대조 |
| HND-03 | P1 | 양면 평면 이탈을 정상 압입으로 취급 | 물리적 분리막 proxy 인증 보류; 9건의 조건부 평형 재현과 실제 실행 증거 대조 |
| HND-04 | P1 | 적격 진단이 인계표에서 소실되고 음수 φ/ε는 OK | ‘기록 전용이므로 학습 안전’ 붕괴; 실제 export 회귀 |
| HND-05 | P2 | pair-lens를 참 union으로 취급 | union으로 물리 타깃을 대체할 수 없음; 다중교집합/ROI 검증 |
| HND-06 | P2 | STL의 z 평균을 평판 검증 없이 높이로 수용 | 일반 높이 인증의 구멍; 실제 130 실패라고 주장하지 않음. 평판/법선 검사 필요 |

LHS-10/11의 분모와 같은 시점 mesh 선택 수정, LHS-12의 임의 ½r_max 컷 제거는 부정하지 않는다. 다만 **그 수정의 성공으로 LHS-13/15 및 물리 해석까지 닫힌 것은 아니다.**
