# r_int ① 구현·①′ 면적 규약 독립 리뷰 — 2026-10-03

## 0. 판정

**G1 = HOLD. G2 = HOLD.**

수정 착수를 금지한다는 뜻이 아니다. **제시된 처방만으로 결함이 닫히거나, 현재 면적 계약 그대로 ②를 구현해도 된다는 판정은 내릴 수 없다.** 기존 기본 OFF의 모든 전도도 결과를 폐기하라는 판정도 아니다.

- G1: AM same-sid 허용목록은 올바른 응급처방이다. 그러나 iid만 추가하면 OFF에서도 존재하는 AM 전류 지도 오염이 남는다. 요청↔실제 적용 계약은 주 전자·이온뿐 아니라 wetted/bare 솔브까지 필요하다. 반응·Joule·STEP4는 별도 규약임을 기계적으로 구분해야 한다.
- G2: 막 ASR와 접합 R_j를 나누는 방향은 타당하다. 그러나 **Σg_film을 맞추면 계면 위치 오류까지 닫힌다**는 주장은 반증됐다. 미등록/간극 접점의 L1 fallback, 접합 저항의 단위·기준면, 서로 다른 모델 간 bound/Δlnσ 판정도 고쳐야 한다.
- 새로 재현한 소비처·검사·설계 결함은 아래에서 P2로 분류했다. **기본 OFF scalar σ를 새로 무너뜨리는 추가 P1은 입증하지 못했다.** 기존 P1-1의 r-ON 가짜 VGCF 저항은 실제 함수로 재현됐다.

심각도는 현재 선택형 프로토타입과 이번 진입 판정 기준이다. 미구현 초안의 오류를 이미 생산에서 발생한 결함으로 쓰지 않는다.

## 1. 핀·범위·추가 로그

- 구현 핀: **5e0efdb8d185fb3a7fc152983ebf543f7b873e1c**.
- 문서·소비처를 읽은 브랜치 핀: **62f9e4cb3e969d13cf0c311858b5159ac75d6396**.
- step3_sigma.py / mpm_webapp_payload.py / check_method_discipline.py의 Git blob은 두 핀에서 각각 동일하다.
- 내려받은 23개 파일은 로컬 바이트로 Git blob SHA-1을 재계산해 전부 일치했다. source_manifest.json 및 evidence_root/probe_units_identifiability.json에 전체 해시가 있다.
- 사용자 추가 shell 로그도 inputs/supplement_log.txt에 보존하고 독립 실행 결과와 대조했다. 빈 diff 로그만으로 핀을 추정하지 않았다.
- 생산 코드 변경·checkout·fetch·시뮬레이션 캠페인·GPU 실행 없음. 읽기 전용 GitHub 조회, 작은 CPU FV/회로 탐침, 실제 producer의 합성 입력 실행, 메모리 내 AST 변이만 수행했다.
- 실침대 payload/원 격자가 없으므로 가짜 접점의 **실생산 빈도·오차 분포**는 미측정이다.

재현 환경: Python 3.12.14 / NumPy 2.3.5 / SciPy 1.16.3. 제공 probe_outputs의 3.11.15 / 2.4.6 / 1.17.1과 다르지만 아래 **인쇄된 유효 숫자**는 같았다. 플랫폼 간 미출력 자릿수의 비트 동일까지 주장하지 않는다.

| 재현 | 결과 | 제공 결과와 대조 |
|---|---|---|
| step3_sigma.py --selftest-rint | exit 0, PASS | 추가 로그의 유효 출력 48줄 일치; 시험 개수라는 뜻은 아님 |
| probe_p1_pid_inherit.py | exit 0 | 16줄 일치 |
| probe_p21_face_area.py | exit 0 | 18줄 일치 |
| probe_p22_cli.py | exit 0 | 3줄 일치 |
| 규칙 J 전체, 원본 | PASS | 독립 실행 |
| 규칙 J 전체, 주 전자 rint 전달 삭제 변이 | **PASS** | 잘못된 초록 재현 |
| 변이 payload의 실제 check_arm | **exit 0** | 잘못된 초록 재현 |

로그: evidence_gates/reproduction_comparison.json, reproduction_metadata.json, *.stdout.txt. 전체 check_all을 돌렸다는 주장은 하지 않는다.

## 2. 우선 finding

### RINT-01 — P1 · 기존 P1-1 CONFIRMED: AM pid를 섬유 경계로 읽는다

**위치:** scripts/step3_sigma.py:242–258, 647–676.

한 VGCF 가닥에 AM pid 0/1/2가 남아 있으면 VGCF|VGCF r=1e−4 Ω·cm²에서 σ_e가 **11.1111 → 0.131752 S/cm**로 떨어지고 가짜 면 두 개가 기록된다. pid를 −1로 두면 해당 면은 0이다. 실제 rasterize로도 두 AM 목을 통과하는 섬유에서 가짜 면 두 개가 재현됐다.

**무너지는 것:** 현 same-sid 규칙을 VGCF·SE로 그대로 확장해도 입자/가닥 경계를 잰다는 주장.
**안 무너지는 것:** rint=None의 scalar σ, 검증된 다른-sid 직렬 막 산술.

**최소 수정:** ①에서는 same-sid를 AM_S/AM_P에만 허용하고 CLI·API·면 규칙 모두에서 강제한다. 지원하지 않는 소유번호를 가진 요청을 면 0 경고만으로 넘기지 않는다. ②③은 final sid 마스크와 분리 이름공간의 iid가 선행한다.

**해결 증거:** 현재 가짜 면 탐침이 거부돼야 하고, 실제 서로 다른 두 AM에는 막이 남아야 한다. 가닥 내부는 pid 오염 여부와 무관하게 막이 생기지 않아야 한다.

재현: python source/docs/reviews/codex_rint_stage1_request_20261003/probe_p1_pid_inherit.py

### RINT-02 — P2 · 기존 P2-3 확대: 주 솔브만 검사하면 collector 변이는 살아남는다

**위치:** scripts/mpm_webapp_payload.py:1980–1983, 2252–2257, 2278, 2876–2879; scripts/check_method_discipline.py:1634–1748, 1777–1794; scripts/sdcp_gain_verdict.py:210–212.

실제 producer 합성 입력:

| 상태 | 주 σ_e (S/cm) | 주 계면 기록 | 기존 J 사후 단언 |
|---|---:|---|---|
| OFF | 0.001049433228717753 | 없음 | PASS |
| ON, AM_S\|AM_S=0.001 | 0.0010352120036449418 | 3,816면·요청 표 일치 | PASS |
| **주 솔브 rint 전달만 삭제** | **OFF와 비트 동일** | CLI model=r1, 실제 faces 없음 | **PASS** |

추가로 **wetted 호출의 rint만 삭제**하면 주 σ_e·3,816면·표는 그대로라 요청서의 주 ON 시험을 만족한다. 그러나 wetted σ가 **0.0009487 → 0.0009606 S/cm**, collector R_geom이 **0 → 0.0544 Ω·cm²**로 변한다. bare 호출만 변이하면 차이가 0 clamp 뒤에 가려지는 경로도 있다. 원본 네 호출에는 현재 rint가 올바르게 연결돼 있다. 이것은 **현재 누락된 인자**가 아니라 **제안한 검사로도 놓치는 변이**다.

또한 model을 실제 솔브에서만 만들고 “model≠None이면 대조”하면, 배선 삭제로 model=None이 된 경우 전제가 거짓이므로 통과한다.

**최소 수정:** 독립적으로 보존한 requested 표를 기준으로 각 enabled/successful solve의 applied 표·모델·단위·소유번호 지원을 대조한다. electronic_main / electronic_wetted / electronic_bare / ionic 각각의 영수증 또는 동등하게 검증된 공통 호출기를 둔다. producer 발행 전·fresh/cache check_arm·최종 판정기에서 동일 계약을 소비한다.

**해결 증거:** 위 네 호출의 인자 삭제를 하나씩 심으면 각각 해당 시험이 실패해야 한다. 원본의 수치·실제 면·표 검증도 함께 통과해야 한다.

재현: python evidence_gates/probe_payload_mutation.py
증거: evidence_gates/payload_mutation/summary_extended.json, rule_J_mutant.stdout.txt, contract_edges.json.

### RINT-03 — P2 · 새 관찰 CONFIRMED: iid만 추가하면 OFF의 AM 전류 지도는 여전히 틀리다

**위치:** scripts/step3_sigma.py:1113–1115; scripts/mpm_webapp_payload.py:1989, 3029; 초안:110.

실제 rasterize에 두 AM 구와 접선 VGCF 선분을 넣었다. **입력 섬유점은 모두 AM 밖**이지만 찍힌 탄소 20셀 중 8셀이 AM pid를 물려받는다. rint OFF에서:

| AM | 현재 입자별 대리값 | final sid로 AM만 집계 | 배수 |
|---|---:|---:|---:|
| 0 | 0.0383162435 | 0.0003027511 | 126.5602 |
| 1 | 0.0377561038 | 0.0003121740 | 120.9457 |

값은 함수의 내부 |J_z| 대리량이며 실험 전류밀도로 인용하면 안 된다. **입자 순위까지 역전**된다. 탄소가 닻을 내린 전류라는 별도 지표를 정의할 수는 있지만, 현 집계는 AM 내부 평균이라는 뜻과 다르다.

반면 reaction은 :1891,1902에서 AM sid를 먼저 가리고, am_surface_patches는 :3340,3362에서 먼저 가린다. 독립 탐침에서 이 두 결과는 pid 정리 전후 비트 동일했다. 모든 pid 소비처가 같은 결함은 아니다.

**최소 수정:** per_particle_current에 final sid∈{1,2} 및 유효 pid 마스크. raw pid를 보존해도 소비처가 소유권을 지키면 된다. iid는 별도로 만든다.

**중요한 계약 수정:** 초안:41,53의 “r OFF 전 산출 비트 동일”과 이 수정은 양립하지 않는다. σ·φ·정상 reaction/patch는 보존하되, **je 소유권 수정은 버전·의도한 변경 예외**로 선언한다. 잘못된 je를 비트 동일 때문에 보존하지 않는다.

재현: python evidence_consumers/probe_consumers.py → consumer_results.json의 pid.

### RINT-04 — P2 · 기존 P2-4 CONFIRMED: Joule 지도는 계면의 주 소산을 보여주지 않는다

**위치:** scripts/step3_sigma.py:1492–1494; scripts/mpm_webapp_payload.py:2164–2168; webapp/static/js/viewer3d.js:3394,3463.

두 슬래브 실제 함수 탐침, σ=1 S/cm, h=0.5 µm, r=0.01 Ω·cm²:

- σ_eff: 1 → **0.0476190476 S/cm**.
- 실제 계면 소산 몫: **0.9523809539**, 독립 직렬식 0.9523809524와 일치.
- 그런데 정규화 Joule 지도의 ON/OFF 최대 차는 **2.03e−6**, hot_frac_50는 둘 다 **0.425**.

r를 적용한 전류로 bulk J²/σ를 계산하는 것은 bulk 소산으로서 맞다. **계면의 I²R을 누락한 지도를 전체 발열 위치로 읽는 것**이 틀리다.

**최소 수정:** bulk-only 이름·included/excluded 항목·지도 밖 interface 소산 몫을 기계 필드와 화면에 함께 남긴다. 총 발열 hotspot은 금지한다. 전체 지도가 필요하면 계면 면 지도 또는 등록된 셀 배분 연산자를 추가하고 bulk+interface(+plate) 총량을 IV와 대조한다. 주석만으로 현 hot_frac_50가 총소산 지표가 되지는 않는다.

재현: python evidence_consumers/probe_consumers.py → joule.

### RINT-05 — P2 · 기존 P2-4 CONFIRMED: STEP4로 넘어가면 막이 소실된다

**위치:** scripts/mpm_webapp_payload.py:2737–2755, 2771–2789; scripts/step3_sigma.py:1867–1874; scripts/step4_dyn.py:970–971,1062,3067–3083.

producer의 실제 np.savez_compressed AST 호출을 실행·포착하면 저장 키는 10개이고 **rint 표·iid·적용 여부가 없다**. STEP4는 σ 표로 bulk-only 간선을 만든다. 이것은 STEP4 캠페인을 돌린 결과가 아니라 실제 저장식 실행과 소비 코드 대조다.

별도 두 경로 reaction 탐침의 실제 OFF 해는 정규화 [1,1]. 한 경로에 같은 막을 일관되게 넣은 직렬 기준해는 **[0.1031390135,1.8968609865]**다. reaction의 KCL 통과만으로 r-ON σ와 같은 물리를 썼다고 할 수 없다.

**최소 수정:** r-ON + save-step4-grid는 현 단계에서 거부한다. rxn은 “막 없는 반응수송 대조”로 scope를 분리하거나 r-ON에서 비활성화한다. 장래에는 기록만 추가하지 말고 reader가 실제 법칙을 소비·검증해야 한다.

**한정:** 이번 범위 밖인 STEP4 물리를 즉시 구현하라는 요구가 아니다. 서로 다른 scope를 한 모델인 것처럼 내보내는 계약 결함이다. r-ON과 공동 결론에 사용하면 그 결론은 기각 대상이다.

재현: python evidence_consumers/probe_consumers.py → serialization, reaction_scope.

### RINT-06 — P2 · 설계 반증: 접촉 총면적 정규화는 계면 위치를 고치지 못한다

**위치:** 초안:100; 요청서:84; scripts/step3_sigma.py:985–1005.

N개 막 간선의 Σg_film=1/R_c를 맞춘다고 단자 저항이 R_c가 되는 것은 아니다. 각 면 양쪽이 공통 등전위 노드일 때만 단순 병렬이다. 일반 FV에서는 I_e=g_e Δφ_e이고 소산은 Σg_e(Δφ_e)²다.

**실제 rasterize·solve_sigma_z 반례:** R=1 µm AM 두 구, δ=0.02 µm, bridge=0.24 µm. sid·σ·전극은 고정하고 iid 후보 경계만 기존 pid / 기하 접촉 중간면으로 바꿨다. 각각 면적 정규화해 **Σg_film=6.25176938064e−7 S가 동일**하다.

| h (µm) | 기존 pid의 σON/σOFF | 접촉 평면의 σON/σOFF |
|---:|---:|---:|
| 0.2 | 0.6241260201 | 0.6474454905 |
| 0.1 | 0.6755034001 | 0.6999486508 |

모두 CG 수렴. 더 단순한 같은 bulk 회로에서 같은 Σg_film=1인 두 배치의 단자 R은 **1 vs 22/13**, +69.23%다. 균일 FV 블록의 같은 15면 경계를 옮겨도 0.5269418141 vs 0.7291597217이 된다.

**최소 수정:** 접촉면 위치·support·위상과 총막 면적은 별도 계약으로 둔다. 두 구는 교차 원판의 평면/경계 분할을 명시하고 브리지 소유 규칙을 거기에 맞춘다. 또는 별도 lumped contact port 모델을 정의하고 bulk 접근저항과 결합을 검증한다. “정규화로 위치까지 해결”은 삭제한다.

**해결 증거:** 비등전위·비대칭 전극·불균일 σ의 기준해, 좌표 이동·입자 순서 변경·격자 세분화에서 단자 전류·국소 flux·에너지를 검증한다. 막 면적 합만 검사해서는 안 된다.

재현: python evidence_area/probe_area_contract.py → AM_boundary_placement, voxel_boundary_placement.

### RINT-07 — P2 · 설계 단위 누락: R_j를 ASR로 바꿀 때 µm²는 cm²가 아니다

**위치:** 초안:100; scripts/step3_sigma.py:261–273.

초안의 R_c N h² [Ω·cm²]는 h를 cm로 넣으면 맞다. 하지만 생산의 vox는 µm다. 따라서 명시할 식은:

r_face [Ω·cm²] = R_c [Ω] × N × h_um² × 10⁻⁸.

현재 솔버의 r_face×10⁴ 환산은 **맞다**. 이를 고치라는 지적이 아니다. r × (N h_um²/A_true_um²) 형태는 면적 단위가 상쇄되지만, 독립 단위 Ω인 R_j에는 상쇄가 없다.

실제 interface_face_g에 R_j=100 Ω, N=1, h=1 µm, 유한한 고전도 σ=10⁸ S/cm를 넣었다:

- 올바른 r_face=10⁻⁶ Ω·cm² → **G=0.00999999000001 S**.
- 초안 식을 µm 그대로 수치화한 r_face=100 → **G≈10⁻¹⁰ S**.

저항이 약 10⁸배 커진다. 이는 **아직 구현하지 않은 식의 단위 위험**이지 현재 산출에서 발생한 10⁸배 오류가 아니다. direct junction edge를 넣는다면 현 조립 단위에서 g_code=10⁴/R_j임도 고정해야 한다.

재현: python evidence_root/probe_units_identifiability.py → junction_units. 독립 재검산도 PASS.

### RINT-08 — P2 · 설계 미폐쇄: D4 fallback과 D5의 “정확” 표지

**위치:** 초안:55,96,103,139,181–183.

1. :96은 미해상 계면에 L1을 금지하는데 :103은 미등록 면을 L1으로 보낸다. 간극 브리지/양자화 연결에는 물리 접촉 면적 자체가 없을 수 있다. 표지만 붙여도 면적·연결성이 생기지 않는다.
2. 미해상 접점이라고 기존 격자에 축방향·half-cell·접근 저항이 없는 것은 아니다. lead 1 Ω + 순접점 5 Ω + lead 1 Ω의 측정 7 Ω을 R_j로 다시 넣고 lead를 유지하면 **9 Ω**이다.
3. 같은 두 fid가 서로 떨어진 두 곳에서 접촉할 수 있다. 쌍 ID 하나와 접합 instance 하나는 다르다. 등전위 두 가닥 사이 동일 접합 두 개는 R_j/2다.
4. R_j=0이면 노드를 만들지 않는 규칙은 임의의 마지막 fid 승리와 같지 않다. 올바른 0 한계는 해당 DOF의 수학적 축약이다.

**최소 수정:** 정량 contact-film mode는 unsupported gap/unregistered 사례를 거부하거나 등록된 절단·터널링 모형으로 분리한다. legacy 유지 팔을 두는 것은 가능하지만 “참 접촉 면적 적용”으로 부르지 않는다. 이중 노드는 아래 Q5의 포트·소유권·중복·에너지 계약까지 포함해야 한다.

재현: python evidence_area/probe_area_contract.py → junction_reference. D4 자체는 초안 논리 모순 검토이며 실데이터 비율을 재었다는 뜻이 아니다.

### RINT-09 — P2 · 설계 반증: FULL≤voxel≤CF와 동일 Δlnσ는 불변식이 아니다

**위치:** 초안:149–150; scripts/network_conductivity.py:401,421,664; scripts/step3_sigma.py:991.

서로 다른 bulk 근사·노드·전극 결합을 가진 두 망에 같은 r/A를 더해도 상대 변화는 다르다. baseline R=1 Ω / 10 Ω에 같은 막 1 Ω을 추가하면:

- σON/σOFF = **0.5 / 0.9090909091**.
- Δlnσ = **−0.6931471806 / −0.0953101798**.

둘 다 막 구현은 정확하다. 따라서 Δlnσ 불일치만으로 막 배선 실패라 판정할 수 없다. 서로 다른 그래프의 σ 순서는 더더욱 자동 보장되지 않는다. 원통 bulk·Maxwell 협착의 서로 반대 편향을 나열해도 bound 증명이 되지 않는다.

**최소 수정:** FULL/CF는 모델 간 대조로 사용한다. 수학적 상하한은 동일 그래프의 edgewise 순서 또는 별도 변분 증명이 있을 때만 붙인다. 같은 그래프·같은 BC에서 r 증가에 따른 전도도 비증가와 에너지 항등식은 진짜 검사로 남긴다.

재현: python evidence_area/probe_area_contract.py → sensitivity_and_bounds.

## 3. Q1–Q8 직접 답

### Q1. 허용목록·iid와 pid 소비처

**부분 동의.** 응급 same-sid 허용목록 + final-sid-masked iid는 적절하다. 그러나 “iid를 만들고 pid 소비처는 그대로”는 RINT-03을 남긴다. per_particle_current만이라도 AM 소유권을 강제한다. reaction·surface patch는 이미 AM을 가리므로 같이 뜯어고칠 근거가 없다.

iid도 단일 winner voxel 하나로 교차 섬유의 다중 소유권을 표현할 수는 없다. ②의 voxel→복수 fid 멤버십 원장은 별도로 필요하다.

### Q2. 혼합안 D1–D4

| 결정 | 판정 | 필요한 한정 |
|---|---|---|
| D1 막 전용 | 동의 | r은 단위 면적당 막 저항. 미해상 협착을 맞추기 위한 튜닝 노브로 쓰지 않음 |
| D2 쌍별 혼합 | 방향 동의, 계약 미완 | 쌍 종류 외에도 해당 국소 계면의 해상도·법선 품질·3중점·접촉 support 검증 |
| D3 DEM 면적 | 수정 동의 | “탄성 Hertz”가 아니라 “LIGGGHTS 기하 교차 원판”으로 이름 고정. physics 병기는 LHS-25 뒤 |
| D4 유지+L1+표지 | 반대 | 미등록 연결/간극의 물리법칙을 따로 정의하거나 정량 모드에서 거부·절단 |

L1 보정 자체를 틀렸다고 판정하지 않는다. 매끄럽게 해상된 계면에서 축별 면 밀도 |n_k|/h²를 이용하면 막 에너지 적분의 합리적 근사가 된다. 그러나 균일 jump 평면의 면적 합 일치가 유한 격자에서의 해 정확성을 증명하지는 않는다. n=(cos30°,sin30°), 서로 다른 표본 jump=(1,2)이면 L1/축별 대안의 전류는 **1.3660254 / 1.25**, 에너지는 **2.0980762 / 1.75**다. 이는 둘 중 하나의 연속 극한이 틀렸다는 증명이 아니라, 면적 시험만으로 선택할 수 없다는 반례다.

5³ centroid 창과 radius/h≥3은 **검증할 후보**이지 오차 상한이 아니다. 곡률·상 대비·3중점·작은 접점에서 비균일 jump 기준해가 필요하다.

SE–SE는 운반된 입자 ID와 **변형 후** 계면 기하로 막 법칙을 정의한다. 변형 전 DEM 접촉 면적을 아무 표지 없이 같은 법칙에 끼워 넣지 않는다. Voronoi 태그를 운반한 경우 그것이 실재 grain boundary 관측인지, 채택한 tessellation 규약인지도 구분한다.

### Q3. 접촉면 이동 규칙과 vox 사다리

**별도 규칙이 필요하다. (b)만으로 닫히지 않는다.** RINT-06이 실제 함수 반례다.

vox 사다리는 다음을 고정·기록한 뒤 수치 수렴 증거로 쓴다:

- 물리 형상, 브리지 길이·판정, 접촉 instance 원장, 계면 위치·면적 원천.
- 전극 위치/접촉·periodic image 중복 규약, origin 위상.
- 입력 σ의 뜻, r/R_j, solver 오차 및 정규화.
- 적어도 하나의 해석/독립 기준 접점과 여러 origin에서의 오차.

σON/σOFF만 안정하면 안 된다. 두 절대 σ, 접점 수·실현/미실현 수·면적, 전류 분배, 계면 소산도 같이 보고한다. ON/OFF의 공유 오차가 비에서 상쇄될 수 있다. “수렴 불가”는 **“미수렴하거나 잘못된 형상·면적으로 수렴할 수 있음”**으로 고친다. 임의의 허용 %는 이 리뷰에서 새로 만들지 않았다.

### Q4. parser·게이트·매니페스트

**제안은 필요하지만 충분하지 않다.**

- extend + nargs='+'는 적절하다. 반복 플래그 사이에서도 unordered pair 중복을 거부한다.
- 채널 검사에는 override·온도 적용이 끝난 **실제 σ 표**를 쓴다. 기본 이름 allowlist만으로 전도/절연을 판정하지 않는다.
- API의 float sid 절삭·bool 수치 변환도 막는다. 지원되는 same-sid 소유번호가 없으면 거부한다.
- requested / enabled / solved / applied를 분리한다. 모든 성공 솔브의 실제 영수증을 요청 표에 대조한다. model이 None이면 검사도 생략하는 구조는 금지한다.
- main·ionic뿐 아니라 wetted/bare도 포함한다.
- n_faces>0 ∧ σON<σOFF는 **선정한 직렬 시험 형상**의 조건이다. 모든 생산 형상에 강제하면 과잉차단이다. 계면이 등전위에 놓이거나, 해당 조성이 한 팔에 없거나, explicit r=0이면 엄격한 감소가 없을 수 있다.
- 0-face는 absent geometry / disabled channel / unsupported identity / failed solve로 나눠 보고한다. 서로 다른 상태를 “면 0” 하나로 덮지 않는다.

### Q5. fid·이중 노드·R_j

**일관된 FV/graph 설계는 가능하다. “이중 노드라 정확”은 아니다.**

권고 최소 구조:

1. 교차 셀에 참여한 모든 fid를 보존하고, 각 축방향 연결을 자기 fid의 DOF에 잇는다. 세 가닥이면 적어도 세 멤버십을 처리한다.
2. 접합 instance별 양쪽 포트에 R_j 간선을 하나만 추가한다. 기존 융합 연결이 병렬 우회로로 남지 않게 한다. 주기 영상·선분 중복을 제거하되 진짜 여러 접합은 합치지 않는다.
3. R_j의 측정 기준면과 남겨 둔 축/half-cell/접근 저항을 일치시킨다. 단섬유 σ와 직경 보존 규약도 함께 봉인한다.
4. 물리 단위를 가진 간선 원장으로 행렬, 연결성 판정, 전류, 소산을 모두 만든다. 현 floating-component pruning보다 **먼저** 접합 연결성을 반영해야 한다.
5. I_e=g_e(φ_i−φ_j), P_e=g_e(φ_i−φ_j)²를 원장에서 산출하고 KCL·ΣP=IV를 검증한다. 같은 함수 이름 재호출만으로 I3를 충족했다고 하지 않는다.
6. R_j→0의 노드 축약, R_j→∞의 가닥 간 절연과 가닥 내부 연속성, same-cell/face/diagonal/3중/다중접합·origin 이동을 시험한다.

R_j 값이 없으면 시나리오 기구 개발은 가능하지만 재료 예측으로 승격할 수 없다.

### Q6. 대조인가 bounding인가

**대조로는 유효하지만, 자동 bounding도 아니다.** 위 RINT-09 때문에 단순 sandwich/동일 Δlnσ를 합격조건에서 뺀다.

현재 목록에 추가할 축: 전극의 유한 저항·접촉 집합, 입자 한 노드로 소실되는 접촉 방향·다중 포트 상호작용, 주기 접점 중복, AM relative-σ 규칙, 한 모델에만 있는 탄소 경로, R_j 접합 counting, CG/전도도 대비. 특히 network_conductivity.py:664의 경계 컨덕턴스가 간선값에 의존하므로 막을 추가할 때 수치 전극 저항까지 바뀌지 않게 분리해야 한다.

같은 voxel의 OFF 기준선은 외부 FV 구현과 대조할 수 있다. 단 BC·전극 셀/half-cell·축 방향·상별 σ·pruning·판을 맞춰야 한다. TauFactor 공식 문서도 mirror/periodic/다상 solver를 구분하므로, “같은 배열”만으로 같은 문제는 아니다. 이번에는 TauFactor를 실행하지 않았다. [공식 문서](https://taufactor.readthedocs.io/en/latest/notebooks/00-overview.html)

### Q7. 펠릿/분말 → 내부값 변경의 최소 조건

**단순히 σ를 올리고 r을 추가하면 닫히지 않는다. P/I의 P부터 정확히 이름 붙여야 한다.**

- AM 10/5 mS/cm는 현 코드에서 상별 국소 σ로 쓰지만 출처 지위는 corpus-fit hook이다.
- VGCF 100 S/cm는 측정된 분말값 그 자체로 입증되지 않았다. 도입 커밋 **087d1a07c91b956a7f6ac47207eb6daa86d14e21**(2026-07-09)의 실제 추가 코드도 default=100을 hook으로 넣는다. 현재 diameter_preserving_sigma는 **σ×A_real/A_vox**를 실제 계산한다(:1387–1415). 따라서 현재 입력의 역할은 국소 섬유 closure이지 자동으로 특정 분말 실험값이 아니다.
- SE 3.0 mS/cm의 입내/입계 분해 역시 현재 입력 숫자만으로 식별되지 않는다. se_material의 σ·T_ref 선언이 있다고 입내 측정이 되는 것은 아니다.

도입 증거는 evidence_root/vgcf_origin_excerpt.json에 보존했다. 이것은 기본값·hook 지위의 원기록이며, 후속 문헌 전체의 감사나 접촉을 몇 % 흡수했는지의 측정은 아니다. **“VGCF100=분말값이므로 이중계상량을 안다”는 요청서 문구는 철회**한다. 이중계상 위험은 남지만 크기·분해는 미식별이다.

최소 조건:

1. 재료 등급·조성·SOC·온도·압력·측정 방향·시편 형태·전극/입계 분리 방법을 원문/SI에서 확인한다. DOI/판/표·그림/단위·환산과 채택 이유를 남긴다.
2. 상 내부 σ, film r, R_j가 각각 제외/포함하는 저항을 명시한다. 단섬유 terminal 저항에서 이미 포함된 lead/access를 중복하지 않는다.
3. σ_internal과 r를 같은 전극 유효값 하나로 동시에 정하지 않는다. 합성 1D에서 동일 σ_eff=0.003 S/cm는 σ_grain=0.003/0.006/0.03에 서로 다른 음이 아닌 r(첫 경우 0)를 붙여 모두 재현된다. 이는 실재 값 추천이 아니라 비식별성 반례다.
4. 보정 자료·검증 holdout을 사전 분리한다. 같은 측정으로 σ·r를 맞추고 일치했다고 검증 성공으로 쓰지 않는다.
5. 결손이면 “내부값 미확인/감도 시나리오”로 남기고 headline 절대값에 쓰지 않는다.

병기 열은 최소한 **legacy effective-hook / intrinsic+explicit-interface scenario**, 실제 phase σ(T_ref,T), r/R_j, 면적·접점 정의, 자료 출처/추정 여부, calibration/holdout 구분, 모델 ID를 가진다. 기존 팔을 소급해 “내부값”이라고 바꾸지 않는다. 단섬유·입내값이 나왔다고 과거 코호트와 같은 규약으로 섞지 않는다.

재현: python evidence_root/probe_units_identifiability.py → identifiability.
출처 정정 대상: 요청서 §5–6; 초안:45,159; 현 코드 :21–43,1358–1415.

### Q8. 추가 P1과 기타 소비처

기존 P1-1 외에 **현재 기본 OFF scalar σ의 새 P1은 입증하지 않았다**. 새 중요한 결함은 RINT-02~09의 P2다. r-ON 산출을 현재 상태로 합쳐 원고·발열·STEP4 공동 결론을 내면 해당 결론을 지지하지 못한다.

추가 방어 항목: rint_ctx_from은 caller sid를 그대로 받는다(:290–295). 잘못된 same-shape sid를 넘기면 계면 몫 0.95238→0, |J|max 약 **101배**가 재현된다. 하지만 현 생산에서 그런 잘못된 caller를 확인한 것은 아니므로 P3 API 방어 결함으로 둔다. sid 지문만으로도 부족하다. res가 보유한 pid 참조를 나중에 바꾸면 저장된 9면은 그대로인데 진단 계면 몫은 0이 된다(:1082). 불변 간선 원장 또는 sid·pid/iid·σ·경계/면 법칙 전체에 대한 무결성 확인이 필요하다.

## 4. 자기리뷰 P3 9건 재판정

| 항목 | 판정·등급 | 결론 |
|---|---|---|
| 1. r=0 ULP/키 | CONFIRMED P3 | σ·φ는 비트 동일, 분담 차 1.68e−18와 interface=0 추가 키. 수치 중요성은 없지만 전 산출 동일 계약에는 위배 |
| 2. API cast | CONFIRMED P3 | (1.7,3)→(1,3), True→1, unknown sid 허용 후 왕복 실패. CLI와 API 모두 엄격 검사 |
| 3. OFF↔ON compare HOLD | CONFIRMED P3 | r 축만 expected로 두면 파생 model에서 HOLD. model만 면제해도 현 producer의 미분류 6필드에서 추가 HOLD; registry 보완 필요 |
| 4. no-ion+r_i | CONFIRMED P3 | 실제 payload에 model=r1이나 ion 적용/면 없음. 모순 요청 거부 또는 disabled 요청으로 명확히 기록 |
| 5. NODIGEST 캐시 | **부분, 미래 배선 조건** | digest 충돌은 재현. 하지만 ON 영수증은 OFF manifest를 거부하고, 현 러너는 rint 추가 플래그를 막음. 현재 무음 캐시 오사용은 입증 안 됨 |
| 6. 쌍별 민감도 없음 | 확장 요구 | 전체 계면 소산 합 자체는 맞는 양. 이것을 개별 쌍의 민감도로 읽을 때 문제 |
| 7. 이름 충돌 | P3 명명 | 유사한 명칭이지 실제 동일 키 overwrite를 찾은 것은 아님. terminal ASR와 internal-interface ASR scope를 분리 |
| 8. viewer 상 손실 표지 | CONFIRMED P3 | interface는 상이 아니므로 “상/계면 소산”으로 수정 |
| 9. caller sid | CONFIRMED P3 | API 오사용/가변 pid로 진단 오염 가능. 실제 생산 mismatch라고 단정하지 않음 |

추가 compare 미분류 키는 electronic_field_pts, fibre_segment_ledger, field_requested, ionic_field_pts, ptfe_block_cells, ptfe_block_scope이다. 이 항목은 기존 registry drift이며 rint 구현이 새로 만들었다고 분류하지 않는다.

## 5. 최소 해제조건

### G1 — ① 수정 완료 판정 전

1. same-sid owner를 CLI·API·솔버에서 강제하고 parser empty/repeat/type/disabled 조합을 닫을 것.
2. 요청 표를 독립 보존하고 네 솔브의 실제 적용 영수증을 producer·check_arm·최종 판정기가 공통 검사할 것. 모든 호출부 삭제 변이가 각각 잡힐 것.
3. AM je의 sid 소유권을 고치고 r-OFF 호환성 예외를 명시할 것.
4. bulk-only Joule·CONTACT_FREE reaction을 기계 필드/화면에 표시하고 unsupported STEP4 export를 거부할 것.
5. 진단 맥락의 불변성, zero/absent/disabled/failed 구분, OFF/zero scalar 회귀를 검증할 것.

### G2 — ①′ 계약 채택·② 구현 진입 전

1. 총면적 정규화의 “위치도 해결/항상 병렬 정확” 주장을 철회하고 계면 support·소유권 규칙을 별도 봉인할 것.
2. D4의 미등록/간극 접점을 정량 film 경로에서 어떻게 다룰지 고정할 것. 적용 범위 밖 L1 자동 fallback은 금지할 것.
3. Ω·cm²/Ω/µm 및 direct-edge 단위·R_j 기준면·남기는 access/axial 저항을 명시할 것.
4. 다중 fid·접합 instance·주기·0/∞ 한계·연결성 pruning·단일 간선 원장과 보존 시험을 등록할 것.
5. vox 검증을 면적/비 안정성만이 아니라 위치·전류·에너지 기준해로 확장하고, 미증명 cross-model bound/동일 Δlnσ 강제를 제거할 것.
6. D3의 이름/physics 지연, σ 입력의 실제 출처 지위, 보정/holdout 분리를 문서에 반영할 것.

입내·접합 재료값의 부재는 **② 기구의 합성 검증 자체**를 막지 않는다. 다만 ④/⑤의 재료 예측·원고 인용은 그 값과 불확실성이 닫히기 전까지 별도 HOLD다.

## 6. 재현·산출물 안내

리뷰 폴더에서 Python+NumPy+SciPy 환경으로 다음을 실행한다. GPU/DEM/MPM 캠페인은 필요 없다.

```text
python evidence_gates/run_reproductions.py
python evidence_gates/probe_payload_mutation.py
python evidence_gates/probe_contract_edges.py
python evidence_gates/run_extra.py
python evidence_consumers/probe_consumers.py
python evidence_area/probe_area_contract.py
python evidence_root/probe_units_identifiability.py
```

- source/ : 핀된 원본 23개 파일. 수정하지 않음.
- evidence_gates/ : 제공 탐침 대조·실제 producer 변이·전체 규칙 J·check_arm·계약 결과.
- evidence_consumers/ : 실제 rasterize/지도/reaction·저장식 탐침. serialization은 AST 호출 포착임을 명시.
- evidence_area/ : 실제 FV 접촉 위치 반례 + 독립 회로/설계 검토.
- evidence_root/ : 단위·식별성·파일 해시 검산, VGCF 도입 코드 발췌.
- inputs/ : 요청서·추가 로그 원본.
- README.md : 환경 및 자세한 재현 순서.

범위 밖/미완료: 실침대 빈도·분포, 실제 fid/SE-id 새 구현, GPU 경로, 장시간 생산, TauFactor 실행, 문헌 재료값의 새 채택. 문서에 적힌 과거 실측을 새로 재현한 것으로 세지 않았다.

**최종: G1 HOLD · G2 HOLD.**
