# 이번 주 원고 마감 계획 — v6 실물 대조 후 확정 (2026-08-25)

> 입력: `Manuscript v6.docx` · `SI v6.docx` 실물 (사용자 업로드, 텍스트 추출 대조 완료).
> 지시: DEM/MPM 비중 축소 · 실험 중심 · 표는 별도 파일 · 수식 포함 · 보정은
> "porosity 타겟팅" 서술로 · **금요일까지 유효 σ_ion/σ_e 문헌 레인지 (litdb 기반)**.

---

## 0. ⚠⚠⚠ 먼저 — v6 SI 의 Table S3 은 **철회 세대 값이다** (이번 주 최우선)

v6 실물에서 확인 (SI 텍스트 추출):

| S3 항목 | SBE | DBE | 문제 |
|---|---|---|---|
| σele_eff | 1.98 | 3.00 S cm⁻¹ | **비 +51.5 % = 철회 헤드라인 계열** (CL-24, vox 0.4 점-스탬프 세대. 원장 `quotation_ban` 소관) |
| σion_eff | 2.03e-4 | 2.15e-4 | 비 +5.9 % = 같은 철회 세대 이온 이득 계열 |
| Porosity | 7.87 | 7.39 % | 같은 세대 침대 |
| Thickness | 72.48 | 72.48 µm | 〃 |

**세대 불일치의 증거가 표 안에 있다**: Table S2 는 vox **0.15** · SDCP E **9.0 GPa (Measured)** ·
PTFE E **1.8 GPa (Measured)** 를 선언하는데, S3 의 수치는 **vox 0.4 · SDCP 23.6 · PTFE 0.30
세대 침대**의 산출이다 (CL-56).  파라미터 표와 결과 표가 **다른 시뮬레이션**을 가리킨다.
또한 σele_eff 1.98–3.00 S cm⁻¹ = 1,980–3,000 mS cm⁻¹ 는 같은 재료계 실측
(Lee 2025 34 · Kim 2024 38.6–65.2 mS cm⁻¹, CL-46)의 **30–60배**라 절대값도 방어 불가.

⇒ **Table S3 전체 재생성이 투고의 필요조건**이다 (D3 재압밀 + 새 STEP3).  아래 §3.

## 1. ✅ 이 대조에서 닫힌 것 — B 사전등록의 G1

원고 본문이 전자 값을 직접 준다: *"decreases from 0.30 × 10⁻⁷ S cm⁻¹ for pristine LPSCl to
0.12 × 10⁻⁷ S cm⁻¹ with PTFE, but increases more than fivefold"* → 1.53 × 10⁻⁷ 정합
(0.30 × 5.1 = 1.53 ✓).  이온도 본문 확인: 3.57 → 0.97 (PTFE).
⇒ `sdcp_ion_calib_prereg_20260825.md` §2 의 **G1 충족** — 출처 = 원고 본문 수치 (그림 판독보다
강함).  ⚠ 패널 표기는 v6 본문에서 σ 문장에 패널 번호가 안 붙어 있어 "본문 수치" 로 기록.

## 2. 이번 주 리스트 (순서 = 의존 순서)

| # | 일 | 어디서 | 소요 | 산출 |
|---|---|---|---|---|
| **W1** | **A 판별 런 4개** (기존 침대 — 재압밀 안 기다림) | kgy V100 | 1–2일 | σ_e 비의 보고 규약 결정 (브리지 규약 or "Ø0.30 이 이산화로 못 푼다" 문장) |
| **W2** | **재압밀** — SBE/DBE 침대를 Table S2 의 측정 E (SDCP 9.0 · PTFE 1.8)로 | kgy | 수 시간 | 새 침대 (S2↔S3 세대 일치) |
| **W3** | **B G2 구현 ✅ (2026-08-25)** — `apply_ptfe_blocking`(sid 6→9) + `--step3-ptfe-block-um` + 펠릿 측정기 `pellet_rve_sigma.py`(selftest 11/11) + 러너 `run_pellet_calib.sh`.  → **B 펠릿 런** (kgy, 팔당 ~4 s) | CPU | 런 수 분 | 이온 행 개방 여부 판정 + **σ_SDCP=250 을 Figure 2 앵커 값으로 대체** |
| **W4** | **STEP3 최종** — 새 침대 × 8팔 × vox 0.15 구 스탬프, A 가 정한 규약 + B 가 준 σ 표 | kgy V100 | ~1일 | **Table S3 전량 재생성** (두께·porosity·면적용량·coverage·σ) |
| **W5** | **Methods(Simulation) 최종문** — 비중 축소 · 수식 3개 · "porosity 타겟팅" 보정 서술 · 참고문헌 절 내 삽입 | 문서 | — | 원고 절 |
| **W6** | **금요일: σ 문헌 레인지 문단** (§4 초안 완성돼 있음 — litdb 기반) | 문서 | — | 제출용 문단 + 참고문헌 |
| **W7** | 표 3종(DEM·MPM·DFT) **별도 파일** 분리 + 라벨 정정 (아래 §5) | 문서 | — | SI 표 파일 |

의존: W4 는 W1·W2 뒤 (W3 는 병렬, 이온 행에만 걸림).  W5·W6·W7 은 **지금 바로** 가능.
⚠ W4 전에 S3 를 부분적으로도 채우지 않는다 (지금 값은 철회 세대).

## 3. Methods 보정 서술 — 지시대로 한 줄 (방어 서사는 리비전용으로 별도 보관)

> "The effective contact modulus of LPSCl (1.35 GPa for DEM; 1.53 GPa, ν = 0.49, σ_y = 0.30 GPa
> for MPM) was **calibrated to reproduce the experimentally reported porosity of cold-pressed
> LPSCl (~10 % at 300 MPa)** [Minnmann ref]; all other parameters are literature or measured
> values (Table S2)."

수식 3개 (준희 요구 — 변수가 들어가는 식):
① 접촉 힘법칙 (hooke/hysteresis, E*·δ) ② von Mises J2 항복 (σ_y) ③ 복셀 전도
`∇·(σ(r)∇φ) = 0` (+ σ_eff 정의).  ⚠ E 병기 규칙: "1.35 GPa" 단독 금지 — **어느 모듈러스
(입자 영률) + 어느 접촉모델**인지 항상 병기 (Paulick 2015 Eq.1 근거, litdb 카드).

## 4. ★ 금요일 제출용 — 유효 전도도 문헌 레인지 (전부 litdb 정본 카드 기반)

**이온 (복합 양극 유효 σ_ion, 실측):**
- Bazzoun 2026 (JPS 661, 238682 · **같은 LPSCl+NMC 계**): σ_eff,ion = **0.065–0.137 mS cm⁻¹**
  (f_CAM 80→70 wt%, EIS full-blocking, 400 MPa) · LPSCl 펠릿 **1.02 mS cm⁻¹**
- Cronau (단결정): **3.0 mS cm⁻¹** (상한 앵커) · 이 원고 자신의 neat 펠릿 **3.57 mS cm⁻¹**
- ⇒ 레인지 문장: 복합 전극 유효 이온전도는 **10⁻² ~ 10⁻¹ mS cm⁻¹ 급**, 펠릿급 1–3.6.

**전자 (복합 양극 유효 σ_e, 실측):**
- Lee 2025 (Nat. Commun., LPSCl+NCM811+VGCF3+PTFE0.5): **34 mS cm⁻¹**
- Kim 2024: **38.6–65.2 mS cm⁻¹**
- ⚠ PTFE 함량 민감 (Lee: 0.5→5 wt% 에서 σ_e 3,000배 붕괴 — 표면 코팅 기전)
- ⇒ 레인지 문장: 건식 황화물 복합 양극 유효 전자전도는 **수십 mS cm⁻¹ 급** (10⁻² S cm⁻¹).

**상(phase) 값 — 표 라벨 근거:**
- NCM σ_e: Amin & Chiang 2016 (JES 163:A1512, 단상 소결 펠릿): **5×10⁻⁸ → 1.4×10⁻² S cm⁻¹**
  (x=0→0.75, 30 °C — **SOC 의존 4–5 자릿수**).  Table S2 의 1.0×10⁻² 는 이 밴드 안
  (x≈0.7 상당) — 라벨을 "Calculated" → **"Effective (calibrated; within measured band of
  Ref [A&C])"** 로.
- NCM σ_ion: A&C **~9×10⁻⁹ S cm⁻¹** (51 °C) = LPSCl 의 1/3×10⁵ ⇒ "AM=전자망/SE=이온망"
  상 배정의 실측 근거 (Methods 한 줄로 인용 가능).
- VGCF: 분말 압축 **~83–100 S cm⁻¹** vs 단섬유 10⁴ (CL-47 — 차이는 접촉저항) ⇒ S2 라벨
  "Calculated" → **"Compressed-powder value (effective network constant)"**.
- SDCP σ_e 250: 출처 미상 (캐스트 필름 vs 펠릿) — **B 런이 Figure 2 앵커 값으로 대체 예정**.
  대체 전 인용 유지 시 "assumed" 라벨 필요.

⚠ 재생성 후 S3 의 σele_eff 는 위 실측 레인지(수십 mS cm⁻¹)와 **자릿수 비교 가능**해진다
(vox 0.15 세대 kit 값이 그 근방이었음 — 정확 수치는 W4 산출로만 적는다).

## 5. 표 라벨 정정 (별도 파일로 옮기면서 함께)

| 자리 | 지금 | 고침 |
|---|---|---|
| S2 · NCM σ_e "Calculated" | 출처 불명확 | "Effective (within Amin & Chiang band)" + ref |
| S2 · VGCF 100 "Calculated" | CL-47 라벨 오류 부류 | "Compressed powder (effective)" |
| S2 · SDCP 250 "Calculated" | 출처 미상 | B 결과로 대체, 임시 "Assumed" |
| S3 전체 | 철회 세대 | **W4 재생성 전 공백 유지** |

## 6. 실행 참조

```bash
# kgy venv
source ~/dem-venv/bin/activate        # 또는 직접: ~/dem-venv/bin/python3
# A 트랙 (사전등록 고정.  ⚠ 표기 갱신 2026-08-25: P2_EXTRA 로 브리지를 넘기는 옛 표기는
# allowlist 가 옳게 거부한다 — 정식 축 SDCP_BRIDGE 를 쓴다, bridge prereg §7 개정과 동일)
ARMS=8 LEAN=2 VOX=0.15  bash scripts/sdcp_gain_vox015_8arm.sh
ARMS=8 LEAN=2 VOX=0.125 bash scripts/sdcp_gain_vox015_8arm.sh
ARMS=8 LEAN=2 VOX=0.15  SDCP_BRIDGE=0.01 bash scripts/sdcp_gain_vox015_8arm.sh
ARMS=8 LEAN=2 VOX=0.125 SDCP_BRIDGE=0.01 bash scripts/sdcp_gain_vox015_8arm.sh
# B 트랙 STAGE 1 (W3 — G2 구현 완료, CPU 수 분)
bash scripts/run_pellet_calib.sh      # → docs/data/pellet_calib_20260825/*.json
```
