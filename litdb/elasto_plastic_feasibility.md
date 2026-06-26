# ⚙️ Elasto-plastic 접촉모델 — 실행 가능성 · 적용 가능 부분 · 우리 모델 대비 장단점

> 대상: Varkey 2026 multi-contact 탄소성 DEM(`papers/varkey2026_*`) + Thornton–Ning(1998) + **So 2021
> 경도-항복캡 DEM**(`papers/so2021_*`) + Martin–Bouvard 2003 Storåkers 소성접촉(`papers/martinbouvard2003_*`).
> 기준: 우리 DEM(hooke/hysteresis + 18× 연화 + Stage-E) & MPM(champion J2 1.53/0.15). `our_dem_baseline.md`.
> 결론 한 줄: 그들의 "elasto-plastic"은 접촉 힘법칙(CONTACT)일 뿐 입자 형상(SHAPE) 소성이 아니다 —
> 진짜 형상 소성은 이미 우리 MPM이 가짐.
> ★ **핵심 발견(So 2021)**: **접촉에 항복캡을 넣으면 real E로 18× 연화 없이 실험 밀도(상대밀도 0.98)
> 도달 가능** → "연화 irreducible"은 강체 구의 본질이 아니라 *우리 DEM에 항복캡이 없는 탓*. ⇒ 항복캡 DEM
> (경로 A)이 가장 가치 있는 적용.

---

## 0. 먼저 — "elasto-plastic"은 3층위다 (혼동 금지)

| 층위 | 무엇 | Varkey | So2021 | M&B2003 | 우리 DEM | 우리 MPM |
|---|---|---|---|---|---|---|
| **(1) 접촉 힘-변위 LAW** | δ에서 항복 → 소성 분기 + 잔류겹침 | ✅ Thornton–Ning | ✅ H-cap | ✅ Storåkers | ✗ (hooke, ~선형 Hertz) | ✅ J2 |
| **(2) 접촉 AREA 소성** | 접촉면적 소성 확대(전달용) | △ 면적% | ✅ A_con·H | ✅ A=2πc(m)²rh | ✅ **Stage-E**(Tabor+vol) | (해당없음) |
| **(3) 입자 SHAPE 소성** | 입자 자체가 변형·흐름 | ✗ (강체 구) | ✗ (강체 구) | ✗ (truncated sphere) | ✗ (강체 구) | ✅ **진짜 형상변화** |

→ 문헌 DEM 전부 **(1) [+(2)]만**, **(3) SHAPE는 23년째 아무도 못 함**(M&B2003→Varkey2026→Bazzoun2026 일관).
우리는 **(2)+(3)**을 이미 가짐. 그래서 "elasto-plastic 도입"의 실질 = **(1) 접촉 항복 LAW를 우리 DEM에
넣을지** — (3) 진짜 소성은 이미 MPM이 함.

---

## 1. 실행 가능성 (구현 경로 3가지)

### 경로 A — 항복캡 접촉 LAW를 LIGGGHTS에 ★★ 1순위 (So 2021이 입증한 선례)
- **가능성: 높음.** LIGGGHTS는 이미 hysteretic/cohesion 접촉(Luding, EEPA 계열) 지원 → 항복압력 p_y(또는
  경도 H) 캡 + 영구겹침 접촉으로 교체 가능. 우리 `input_real_*.liggghts`의 pair_style 교체 수준.
- **핵심 실험**: **real E_SE(24 GPa) + 접촉 항복(p_y LPSCl 0.05–0.30 GPa, 또는 H-cap F_th=2/3·H·A_con) +
  영구겹침**으로 300 MPa porosity가 나오는가? → 성공 시 **경험적 18× 연화를 물리 항복법칙으로 대체/제거**.
- ★ **검증된 선례**: **So 2021**(우리가 인용하는 2D[27]의 같은 그룹 후속)이 이미 입증 — real E_SE=24 GPa
  (연화 없이) + 경도 항복캡으로 LPS pure-SE 상대밀도 **0.30→0.98 @600 MPa** 달성. 즉 경로 A는 가설이 아니라
  **이미 작동을 보인 방법** (단 LPS+Si라 LPSCl로 재보정 필요).
- 노력: ~1–2주(calibration). 비용: 무료(LIGGGHTS).

### 경로 B — Multi-contact 구속항 F_mc (Giannis/Varkey)
- **가능성: 중.** F_mc=β·ν·a_ij·P_ij 는 입자별 응력텐서 σᵖ=(1/Vᵖ)Σlⁿ⊗fⁿ 누적 + 접촉 결합 필요 →
  LIGGGHTS 소스(C++) 커스텀 또는 Ansys Rocky(상용, Varkey 사용).
- **용도**: ρ>0.7 치밀영역 과강성 — 우리 18× 연화가 노리는 증상의 물리적 대안. "연화 ≈ F_mc?" 비교연구.
- 노력: 높음(커스텀) 또는 상용. 

### 경로 C — 진짜 소성 (이미 보유)
- **MPM champion(J2, E=1.53/σ_y=0.15)**. 입자 형상변화·void-fill·변형장. **추가 구현 불필요.**

**판정**: 경로 A(항복캡 DEM)가 즉시 가능 + So 2021 선례 + 18× 연화 제거 가능성 = 최우선. B는 비교연구, C는 완료.

---

## 2. 내가 적용할 수 있는 부분 (steal smart)

1. **★ 항복캡으로 18× 연화 대체** (경로 A): So 2021 H-cap(F_th=2/3·H·A_con) 또는 Thornton–Ning p_y를
   LIGGGHTS에 + real E_SE. So 2021이 LPS로 0.98 달성 입증 → LPSCl @300 MPa 재현 직접 시험.
2. **Storåkers 소성 접촉면적 A=2πc(m)²·r·h** (M&B2003, c(m) 0.5 선형경화→1.45 이상소성) → 우리 **Stage-E
   (Tabor+volume) 면적**과 A/B 비교 (물리 유도 vs 경험 보정).
3. **Multi-contact F_mc ↔ 18× 연화 비교** (경로 B): 같은 증상 다른 처방, paper-grade.
4. **두 메커니즘 분해**(M&B2003): 경상 force-network(K_h, N₂₂/N₁₁) + 연상 excluded-volume 과변형 →
   우리 **복합 porosity 관계식의 두 항**(하드-네트워크 조성항 + 소프트-경화항).
5. **크기비 기하항**(McGeary 7:1 무릎, 0.154·d_c) → Furnas-dip / porosity 관계식의 (조성×크기비) 항 근거.
6. **Bond 모델**(Sangrós SBR/CB/PTFE) — 바인더 도입 시 템플릿.
7. **다중압력 검증**(Varkey 100–350 / Bazzoun 100–400 MPa) — 우리 단일앵커(Minnmann) 확장.

---

## 3. 우리 모델 대비 — 그들의 elasto-plastic이 **좋은 점**

| # | 그들이 나은 점 | 우리 현황 |
|---|---|---|
| 1 | **항복캡 접촉으로 real E 사용**(So 2021) → 18× 연화 불필요 | 우리 DEM은 항복캡 없음 → E를 18× 낮춤(경험적) |
| 2 | **물리적 접촉 LAW**(Thornton–Ning 항복+잔류겹침 / Storåkers) | hooke/hysteresis(~선형 Hertz, 접촉 소성 없음) |
| 3 | **치밀영역 과강성 물리항 F_mc** | 경험적 18× 연화(fudge) |
| 4 | **다중압력 검증**(4압력, 두께<1%) | 주로 단일앵커(Minnmann 300 MPa) |
| 5 | **물리유도 소성 접촉면적**(Storåkers c(m)) | Stage-E(Tabor+volume, 경험 보정) |
| 6 | **명시적 바인더 bond**(R_b) | 바인더 미모델 |

→ 핵심: **항복캡·물리 접촉 LAW·다중압력 검증**에서 앞선다. 우리 18× 연화의 "경험적" 약점을 그들의
항복법칙이 **물리적으로 제거**할 수 있다(경로 A, So 2021 입증).

---

## 4. 우리 모델 대비 — 그들의 elasto-plastic이 **못 미치는 점**

| # | 그들이 못 하는 것 | 우리는 |
|---|---|---|
| 1 | **입자 SHAPE 소성 전무**(강체 구/truncated; 23년째 문헌 공통 한계) | MPM 진짜 형상변화(SEM ✓) |
| 2 | **void-fill flow·변형장 없음** | MPM 부피보존 흐름 + Σdg 변형장(열화 개시) |
| 3 | **σ_ionic만**(So/Varkey) | σ_ionic+σ_e+σ_thermal 삼중항(LOOCV 0.97/0.95/0.90) |
| 4 | **multi-contact 평균장** | MPM 연속체는 접촉 결합 exact |
| 5 | **소재 불일치**(Varkey halide / So LPS+Si / M&B 금속) | LPSCl 기준 (Bazzoun만 동일소재) |
| 6 | 전달 접촉면적%만 (Tabor 소성 coverage 아님) | Stage-E 소성 coverage(Hertz·Tabor) |
| 7 | **비구형 입자**(각질 inclusion이 압밀 더 방해, Bouvard) — future work | 우리도 구만(공통 한계) |

→ **핵심**: 그들의 elasto-plastic은 (1) 접촉 LAW 층위라 **입자 형상·morphology·변형장·σ 삼중항을 못 준다**.
바로 우리 **MPM+네트워크가 메우는 간극**(frame[5]) — Varkey/So 본인이 "향후 과제"로 인정 = frame[5] 확증.

---

## 5. ⚠ 핵심 정정 — "연화 IRREDUCIBLE"은 *우리 DEM에 항복캡이 없어서*다 (So 2021)

So 2021 digest가 이 절의 통념(\"접촉 LAW 도입해도 ~20% floor 못 넘음\")을 **반증**했다. 정정:
- **비변형 기하 패킹 floor**(McGeary): 변형 없는 강체 구 = ~14–37% porosity 한계 (overlap 0).
- **항복캡 + 영구겹침**: 강체 구라도 접촉에 **항복캡 + 영구 overlap(h_eq)**을 넣으면 그 아래로 치밀화 —
  **So 2021이 real E_SE=24 GPa로 LPS pure-SE 상대밀도 0.98(porosity ~2%)@600 MPa 달성**. 영구겹침이
  displaced-material proxy(= 우리 ε_sphere 규약)라 sub-20%로 내려감.
- **우리 DEM**: hooke/hysteresis = ~선형 Hertz, **항복캡 없음** → 같은 압력서 overlap 부족 → 그래서 E를
  18× 낮춰 overlap 강제. 즉 **\"연화 IRREDUCIBLE\"은 강체 구의 본질이 아니라 우리 DEM에 항복캡이 없는 탓**
  (So 2021 agent 지적). Varkey \"<20% 안 함\"도 **물리 floor가 아니라 계산비용**(고밀도서 timestep↓) 진술.

⇒ **재정의된 경로 A**: real E_SE + 항복캡(Thornton–Ning p_y / So 2021 H-cap)을 LIGGGHTS에 넣으면 **18× 연화
없이** 실험 porosity 도달 가능 — So 2021이 (다른 소재로) 입증. **우리 LPSCl @300 MPa 재현은 미검증이나
강하게 동기부여됨**(경로 A 1순위).
⚠ 단: (i) MPM cap/jam dead-end(CLAUDE.md)과 **모순 아님** — 그건 *연속체 볼륨 cap*, 이건 *이산 접촉 항복*
(다른 메커니즘). (ii) 항복캡을 넣어도 **입자 형상 SHAPE 흐름·morphology·변형장은 여전히 못 줌**(overlap은
기하 proxy) → 그건 MPM 영역(frame[5] 유지).

---

## 6. 종합 판정 & 추천 액션
- **실행 가능성**: 경로 A(항복캡 DEM) = 즉시 가능 + So 2021 선례, ~1–2주. 경로 B(F_mc) = 비교연구.
  경로 C(진짜 소성) = MPM으로 완료.
- **가장 가치 있는 적용**: ① **So 2021 H-cap을 LPSCl로 재보정 → 18× 연화 대체 시험** + ② **F_mc ↔ 연화
  비교** + ③ Storåkers/Thornton–Ning 접촉면적 → Stage-E A/B.
- **그들 우위**: 항복캡(real E)·물리 접촉 LAW·다중압력 검증·바인더 → **흡수 대상**.
- **그들 한계(우리 우위)**: 형상 소성·morphology·변형장·σ 삼중항·exact 결합 → **MPM+네트워크 보유**.
- **냉정한 결론(So 2021 반영)**: elasto-plastic CONTACT(항복캡) 도입은 단순 정밀화가 아니라 **경험적 18×
  연화를 제거**할 수 있는 경로다 — So 2021이 real E + H-cap으로 입증(상대밀도 0.98). **압밀 방어력의 질적
  도약**(fudge 제거). 단 \"진짜 소성(형상·morphology·변형장)\"은 여전히 MPM 영역 → 도입해도 frame[5] 분업은
  유지(DEM=항복캡 접촉+전달, MPM=형상 소성). **추천: 경로 A를 1순위로.**

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
