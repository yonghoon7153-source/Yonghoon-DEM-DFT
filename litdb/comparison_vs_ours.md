# 🔬 문헌 ↔ 우리 DEM+MPM — 차이 + 적용 인사이트

> 기준값: `our_dem_baseline.md`. 각 축마다 "문헌이 뭐라 하나 / 우리가 뭐라 하나 / 왜 다른가 / 어떻게 쓰나".
> 현재 digest: Varkey2026(할라이드 multi-contact DEM), Bazzoun2026(LPSCl DEM+FEM+RNM).

## A. 압밀 / porosity (E_SE 강성이 floor를 정한다)
- 문헌: Varkey(halide E=10.58) separator floor **21 %** / cathode **37 %** @350 MPa (강체 구, <20 % "추구 안 함").
- 우리: LPSCl pure-SE **~10 %** @300 (Minnmann), real_14 **15.6 %** — 같은 압력 **약 2× 더 치밀**.
- 왜 다른가: (a) halide E가 우리 E_eff 1.35보다 ~8× 뻣뻣 → 더 높은 잔류 porosity (우리 MPM E-sweep과 정합);
  (b) 우리 DEM 연화 + MPM 소성 흐름이 강체 구 floor(~20 %) 아래로 도달.
- 인사이트: **우리 porosity 관계식에 E_SE(강성) 항 + 조성 항 필수.** ~20 %는 강체 구 하드 floor.
  Heckel `ln(1/(1−D))=K·P+A` 후보 (우리 R²=0.965, P_y=138). 둘 다 ~100 MPa 탄성→소성 무릎 (= 우리 P_y).

## B. 전달 삼중항 — σ_ionic은 교차검증, σ_e/σ_thermal은 우리만
- 문헌(Bazzoun, **LPSCl 동일소재 + LIGGGHTS 동일코드**): RNM = 우리 Holm/Kirchhoff 그대로
  (R=1/(2σr_c), Σ(φi−φj)/R=0). 실험 σ_eff,ion **0.137/0.101/0.065 mS/cm @ f_CAM 70/75/80** (400 MPa, EIS).
- 우리: 같은 솔버 물리. 추세 일치 — 작은 SE→σ↑, CAM↑→σ↓, 압력↑→σ↑(~400 포화 ≈ 우리 P_y 138).
- 차이: 그들 RNM은 **구속저항만**(field spreading 없음) → 고-CAM서 과소(80 % RNM 0.031 ≪ exp 0.065);
  우리 Stage-E 소성 접촉면적이 이 과소를 일부 보정. 그들은 σ_e/σ_thermal 없음(우리 삼중항 우위).
- 인사이트: **Bazzoun 실험 σ_eff,ion = 우리 σ_ionic의 외부 절대 검증점** (그들 vol% CAM:SE → 우리 φ_SE 매핑 후).
  "missing direct validation"(다중압력 LPSCl σ_ionic) 확보.

## C. 역학 / morphology — MPM 고유 (문헌 DEM은 형상 못 바꿈)
- 문헌: Varkey "elasto-plastic"은 **CONTACT 힘법칙만**(Thornton–Ning), 입자는 완벽 구 — "구=타협,
  현실 형상=향후 과제" 명시. Bazzoun도 구만.
- 우리: MPM 진짜 소성 형상변화(SEM 일치), void-fill flow, Σdg 변형장.
- 왜: 강체 구 DEM·단상 연속체는 granular 재배열을 못 잡아 둘 다 연화 럼핑 필요 (frame [1]/[2]).
- 인사이트: **morphology·소성 floor(<20 %)·변형장 = 우리 MPM이 메우는 간극** (Varkey가 스스로 인정 = frame[5] 확증).

## D. 패킹 / Furnas dip — DEM·기하 소유, 소성 MPM 불가
- 문헌: Varkey RCP/rigid → dip @ AM 70–80 wt% (de Larrard 기하). Bazzoun 작은 SE→packing↑→σ↑(size=packing).
- 우리: DEM·de Larrard dip @ AM 70–85; **소성 연속체 MPM은 dip 재현 못 함**(material sweep로 증명, frame[4]).
- 인사이트: dip은 초기 강체 구 패킹(기하)에 산다 → DEM(또는 de Larrard)이 소유. porosity-incl-dip은 DEM.

## E. 우리 계산이 문헌을 "검증/교차검증"하는 지점 (강점으로 쓸 것)
- Bazzoun RNM(Holm+Kirchhoff) = 우리 네트워크 솔버 → 같은 물리, 추세 일치 (frame[4] 독립 교차검증).
- Bazzoun 실험 σ_eff,ion + 다중압력 = 우리가 부족했던 **외부 실험 앵커** 제공.
- Varkey E_SE=10.58·floor 21/37 % = 우리 "E 강성 → floor" 가설의 stiffer-SE 데이터점.
- Varkey 탄성→소성 무릎 ~100 MPa = 우리 Heckel P_y 138 재현(소재 일반성).

## F. 우리가 아직 못 하는 것 / 흡수할 것 (정직 목록 → 향후)
- **FEM 연속체 transport 기준** 없음 (Bazzoun COMSOL 보유) — RNM↔FEM 대조틀 흡수 가치.
- **다중압력 Heckel(LPSCl powder) 실측** — 우리 직접앵커 부족; Bazzoun σ-vs-P / Varkey P-vs-porosity로 보강.
- **명시적 바인더(SBR/CB/PTFE) 역학·이온저항 R_b** — Varkey/Bazzoun 보유, 우리 미모델.
- **multi-contact 구속항 F_mc** (Varkey) vs 우리 18× 연화 — 같은 증상(ρ>0.7 과강성) 다른 처방, 비교연구 거리.

---
## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
