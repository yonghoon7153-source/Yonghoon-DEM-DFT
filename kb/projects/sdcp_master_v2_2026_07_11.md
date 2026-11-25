# Self-Doped Conducting Polymer 전도성 바인더 — 물질·계면화학·매뉴스크립트·모델·로드맵 단일 레퍼런스 **v2**

(2026-07-11 개정 · 원본 2026-07-10 sdcp_master.md 기반 · **DFT-방 2026-07-10/11 대량 반영**:
§1.3 분광 판정 신설(doped 확정), §2.1 히스토리 4행 추가(재구성-슬랩 아티팩트 적발 → 클린-슬랩 재랭킹
→ Phase-B DFT+U 진행), §2.2 스펙 이행 체크, §3.1/3.3 표면 H-transfer 재판정(스크린 음성),
§3.6 Li⁺ 패키지 정량 완료, §3.8 수치 회복, **§3.9 신설**(H-form 화해 + H↔Li 교환 에너지학),
§6 metadata 갱신, §7 로드맵 현행화, §8 파일맵 확장.
상태 표기: ✅앵커 / 🔶INTERIM / ⚠proxy / ❌무효 / ★2026-07-11 신규)

---
## 0. 한눈 요약

**SDCP** = 자가도핑 전도성 고분자 (S-PEDOT계: EDOT 백본 + ether-링크 methyl-분지 alkyl-술폰산 side chain).
**용도**: dry-process ASSB 양극(NCM+LPSCl)에서 PTFE 3약점(전자절연·분산불량·약접착)을 보완하는
전도성 바인더 — SBE(PTFE-only) vs DBE(PTFE+SDCP dual) + C-SUS.

**현재 상태 한 줄 (★갱신)**: **v7c ORCA opt+freq 완료 → 실험 IR·Raman과 대조해 "실물 = 자가도핑(–SO₃⁻)"
분광 판정 완료 ✅ / UMA 슬랩 재구성 아티팩트 적발 → 클린 DFT-슬랩 재구축 → Phase-A 재랭킹 완료
(doped −5.196 ≫ neutral −2.733 eV, Δ2.46 — 옛 Δ0.04는 슬랩 아티팩트로 판정) 🔶UMA-레벨 앵커 /
Phase-B DFT+U 교차검증 진행 중(5-SCF, 분자 2/5 완료, U-ramp 확정) / Li⁺ 3-사이트 패키지 ✅ 완료
(doped = 평탄 사다리) / H↔Li 교환 에너지학 ✅ 완료(operando SO₃Li 논거).**

---
## 1. 물질 — SDCP는 무엇인가

### 1.1 분자 구조 (최종 = v7c; 3세대 오류 계보 포함 — 원본 §1.1 유지)

```
monomer (neutral): C₁₁H₁₆O₆S₂
side chain:  ring–CH₂–O–CH₂CH₂–CH(CH₃)–SO₃H
ring:        thieno[3,4-b][1,4]dioxine (진짜 EDOT 코어 — S가 오각형 중앙)
SMILES: neutral CC(S(=O)(=O)O)CCOCC1COc2cscc2O1 / doped 라디칼(charge 0, mult 2, H 제거)
```
- 구조 오류 계보(구세대 pentyl → v7 링-이성질체 → **v7c 확정**)와 4중 감사(§2.3)는 원본 그대로 유효.
- ★**합성서 대조 확인(2026-07-11)**: 특허/제조예 문서의 **PSIBM-EDT(B-루트, butane-2-sulfonate)가
  정확히 v7c 골격과 일치** — 공정: NaH+설톤 개환(단량체 Na형) → **산화중합(FeSO₄/persulfate,
  H₂SO₄ 7.8당량 수용액)** → 이온교환수지(Na→H) → 60 °C 진공건조. §3.9의 H-form 논의의 근거 문서.
- ★**ORCA v7c 신원 지문 (실측 확정)**: neutral S–O 1.46/1.47/**1.66** Å(긴 결합에 O–H 0.97) vs
  doped **1.495/1.498/1.496 Å 완전 등가**; doped ⟨S²⟩=0.7552(깨끗한 doublet); 스핀밀도 = 술포네이트
  3-O에 ~65% + 백본 π ~35% → **doped = 산소-중심 술포네이트 라디칼(–SO₃•), 백본 부분 비편재**.
  O–H BDE 실측 4.24 eV (r2SCAN-3c; 이전 추정 4.4 → 갱신).

### 1.2 물성 표 — 원본 유지, 1행 갱신
| 물성 | 값 | 출처 | 상태 |
|---|---|---|---|
| 형상 (전극 내) | 0.2–0.5 µm 분산 입자 | S2/S3 | ✅ |
| E (탄성계수) | 23.6 GPa (PTFE 5.6) | Fig2d/S6 | ✅ |
| σ_ion (pellet) | 3.57→2.86 mS/cm (×0.80) | Fig2f | ✅ |
| σ_e (pellet) | 0.30→1.53 ×10⁻⁷ S/cm (×5.1) | Fig2g/S10 | ✅ |
| 열/구조 | XRD 무변화(S8), **Raman/FTIR = 자가도핑 판정 완료 (§1.3)** | 2b/S7 + ★v7c 대조 | ✅ **강화** |
| ρ, σ_e(필름), σ_y | (원본 그대로: proxy/폐기/hook) | | ⚠/❌ |

### 1.3 ★분광 판정 (2026-07-10/11 완결) — "실물 SDCP = 자가도핑(–SO₃⁻) 상태"

**증거 4종 (독립)**:
| # | 증거 | 데이터 |
|---|---|---|
| ① | IR에 O–H 부재 (음성) | 계산 neutral만 3624 cm⁻¹; 실험 FTIR(400–4000 커버)에 부재 |
| ② | Raman 1062 = νs(SO₃⁻) (양성) | 실험 1062 실측; 계산 doped 강한 클러스터 936–1042 (대칭 3-등가 SO₃만 가능) |
| ③ | IR 1133/1178 재배정 | Raman이 심판: **1133 = ν(C–O–C) 에터**(Raman-약), 1178 = νas(SO₃)/ring — 기존 "1133=νs(SO₃)" 추정 정정 |
| ④ | 기하+스핀 (계산 독립) | S–O 3-등가 1.50 Å, 스핀 3-O 분산, ⟨S²⟩ 0.755 |
| (+) | Raman 1423 = C=C 공액 백본 | 실험 최강 피크 — 전도성 백본 실재 |

- **판정 논리**: O–H는 IR-강/Raman-약 → 판정 정본 = FTIR(4000까지 커버). "측정 Raman이 3400에서
  끊겨 판단 불가"(구 주간보고 p.3)는 **해소** — Raman >3500 재측정은 보조 확인으로만.
- **원본 §3.2의 "Raman은 B3LYP 별도런" 계획 → 변경**: 실제로는 **r2SCAN-3c NumFreq Raman으로 완료**
  (neutral 허수 1개 −13.8 cm⁻¹ = floppy torsion, 지문영역 무영향).
- 앵커링 품질: 관능기 지문 실험–계산 ~20–40 cm⁻¹; 백본 C=C ±80(단량체 vs 폴리머, 원리적).
- 입문 설명·배정표·그림 전체: `kb/projects/sdcp_v7c_structure_spectroscopy_report_2026_07_10.md`
  (+ `sdcp_v7c_band_assignment_beginner.csv`, annotated 구조 PNG 2종, IR/Raman 실험-계산 겹침 4종).

---
## 2. 계면 화학 (DFT/MLIP) — 히스토리와 현재 상태

### 2.1 계산 히스토리 (정직 기록 — ★4행 추가)
| 단계 | 값 (doped/neutral) | 판정 |
|---|---|---|
| Phase B (bare-anion ref) | −18.17 / −6.33 eV | ❌ reference 과대 |
| 정합-ref MLIP (구세대 분자) | −4.797 / −3.020 | ❌ 오분자 |
| v7 ORCA | — | ❌ 링 이성질체 격리 |
| **★v7c ORCA opt+freq 완료 (07-09/10)** | E −1676.256250 / −1675.600576 Eh, HURRAY·opt 허수 0 | ✅ 분자 확정 (지문 §1.1) |
| **★재구성-슬랩 Phase-A (07-09 밤)** | −0.935 / −0.893 (Δ0.04, sulfonate_down_r0) | ❌ **슬랩 아티팩트** — reference/slab_relaxed.xyz가 UMA 재이완 중 **상부 Ni층 붕괴 + Ni 1개 이탈**(z=8.1) 판명. 붕괴·포화 표면이 도핑 효과를 가림 |
| **★클린-슬랩 Phase-A (07-10, 확정)** | **champion doped chelation_r90 = −5.196 / neutral(chel_r0) = −2.733 eV (Δ 2.46)**; sulfonate_down 계열 −4.69/−4.25 vs −2.60/−2.26 (Δ~2 eV); etherO ≈ 동등; 슬랩 = **scf_u62의 DFT-이완 (104) 추출**(`slab_clean`, 6층×4 Ni 검증) + **전체 고정**(`--freeze_frac 1.0`) — 재구성 원천 차단. sanity: 분자 무해리, **S–O(표면) 1.51 Å 공유 앵커** | 🔶 **UMA-레벨 앵커** (도핑 라디칼 = 화학흡착 −4~−5 eV vs neutral O-배위 −2~−2.7) |
| **★Phase-B DFT+U 교차검증 (진행)** | 5-SCF(slab/complex_doped/complex_neutral/mol×2, scf_u62 세팅·AFM 인덱스 상속·FSM). **분자 2/5 완료**: mol_doped −518.392712 / mol_neutral −519.683103 Ry. slab/complex = **U-ramp 2단계(u0→u62) 필수 실측 확정**(FSM만으론 슬로싱; 원 lineage의 scf_u0+startingpot='file'이 열쇠) | 🔶 진행 — 완료 시 VERDICT = Δ(doped−neutral) |
| 살아남은 방향성 | **doped ≫ neutral** | ✅ 이제 UMA 수치로 회복 (§3.8), DFT 확증 대기 |

- ★**footprint/γ 주의**: 구값 27.2 Ų / 0.55 J/m²는 **재구성-슬랩 산출물 → 동반 무효**. 클린 챔피언
  (chelation_r90)으로 재측정 예정 (Phase-B 후 일괄).

### 2.2 재계산 스펙 — 이행 체크 (★)
1. v7c 분자 ✔ 2. 동일-세팅 refs ✔ 3. 배향 3계열 ✔(6배향 실행) 4. **O–H 온전성 ✔ — §3.1 스크린으로
   6배향 전부 확인** 5. DFT U-ramp 교차검증 → **진행 중** (dipole corr는 미적용 — Δ에서 상쇄, 필요시 후속)
6. footprint/γ → 클린 챔피언으로 **재측정 대기** 7. **Li⁺ 패키지 ✔ 완료 (§3.6)** — NEB 장벽만 2단계 옵션.
- 재사용 실증: **scf_u62의 slab/AFM/U-ramp 유산이 전부 재사용됨** (클린 슬랩 추출 + AFM 인덱스 상속 + u0 레시피).

### 2.3 구조 검증 프로토콜 — 원본 유지 (4중 감사 + 기하 지문은 §1.1 실측치로 갱신됨)

---
## 3. 메커니즘 스토리 Q&A — 생존 판정 **v2** (★3.1/3.3 재판정, 3.6/3.8 정량 회복, 3.9 신설)

**한눈 인덱스**: 3.1 🔶**재정의** · 3.2 ✅**완결** · 3.3 ✅(④가 챔피언 실측) · 3.4 ✅ · 3.5 ✅ ·
3.6 ✅**정량 완료** · 3.7 ✅개연(강) · 3.8 🔶**수치 회복(UMA)** · **3.9 ★신설(H-form 화해 + H↔Li 교환)**

### 3.1 "산-염기 H⁺ transfer로 표면 OH?" → 🔶 **재정의 (스크린 음성)**
★**실측(07-11)**: 클린-슬랩 UMA 이완 6배향 전부 — **술포네이트를 표면에 접촉시킨 배향 포함** —
산성 O–H 0.98–0.99 Å 온전, **H 반경 3.5 Å 내 표면 O 전무**(이완이 O–H를 표면 반대로 돌림).
→ **직접 H→표면 전달은 정적 전구체(수소결합조차) 없음**. 양성자-전달 MD는 우선순위 하향.
**수정된 문장**: "표면 OH 생성 경로는 정적 증거 없음; H의 거취는 §3.9의 이온교환 경로(수분/Li⁺욕)가
지배" — 원답의 캐비엇("주요 공급원 주장은 과대")이 사실상 본문으로 승격된 셈.

### 3.2 "자가도핑이 실제 상태라는 근거?" → ✅ **완결 (계산×실험 대조 완료)**
원답의 실험 3종(Raman SO₃⁻ ~1060, 무도판트 전도성, polaron 흡수)에 더해 —
★**우리 대조로 확정**: 실험 Raman **1062** = 계산 doped νs(SO₃⁻)와 일치(neutral로는 재현 불가),
실험 FTIR O–H 부재 = 계산 neutral-전용 3624 부재, 실험 Raman 1423 = 공액 C=C. **§1.3 판정 그 자체.**
관전 포인트였던 "ether C–O–C가 1060 영역과 겹치나" → **1133으로 분리 배정 완료**(Raman-약이 결정타).

### 3.3 "NCM 앵커링 시나리오" → ✅ 유지, **④가 실측 챔피언**
①H-transfer 경로: **정적으로 비활성**(3.1) ②직접 배위 ③bidentate: 유지.
★**④ ether-보조 chelation = 클린-슬랩 챔피언 실측** (doped chelation_r90 −5.196 eV). 단, 최종
결합모드는 시작배향 라벨과 달리 **S–O(표면 격자O) 1.51 Å 공유결합 앵커**로 이완 — "라디칼이 앉은
술포네이트 O가 표면 O와 직접 결합"이 실제 모티프 (스핀밀도 §1.1과 자기일관).

### 3.4 "SO₃H/SO₃⁻ 둘 다 안정?" → ✅ 유지 (기하 지문 실측 §1.1; 열역학은 §3.9로 정량화)

### 3.5 "혼합 폴리머의 계면?" → ✅ 유지 ("모든 SO₃ unit이 계면 형성에 기여" 문장 유효;
경로별 정량은 Phase-B + §3.9가 채우는 중)

### 3.6 "3역할(앵커/Li⁺호핑/e⁻전도)?" → ✅ **② Li⁺ 호핑 정량 완료 (★07-11 Li⁺ 패키지)**
로컬 ORCA r2SCAN-3c, 분자+Li⁺ 3-사이트 결합에너지 (eV):
| 사이트 | neutral | doped | Δ(d−n) |
|---|---|---|---|
| SO₃ O,O-이좌 | −2.51 | −3.28 | −0.77 |
| 곁사슬 ether O | −2.88 | −2.93 | −0.05 |
| EDOT O,O-킬레이트 | −1.61 | **−3.36** | −1.76 |
- **호핑 지표 = 자리간 편차**: doped **0.43 eV** vs neutral **1.27 eV** (3배 평탄) → doped는
  근등가 O-사이트 사다리(`SO₃⁻→ether-O→EDOT-O`) = **연결된 Li⁺ 경로**; neutral은 ether 단일
  우물에 갇힘(trap형·절연적). **원답 ②의 "사다리" 예측이 수치로 성립.**
- 구보고 p.6 문장 업데이트: "neutral은 Li이 작용기를 **피한다**" → "**한 자리에 갇히고 경로가
  끊긴다**"가 정확 (결론 동일, 메커니즘 정교화).
- 캐비엇: 기체상 단량체+맨 Li⁺ — 차이/편차만 인용. 실제 장벽은 NEB 2단계(옵션).

### 3.7 "NCM 주위 클러스터?" → ✅ 개연(강) — 원본 유지 (판별 실험/스위치 동일)

### 3.8 "doped ≫ neutral 강흡착 스토리" → 🔶 **수치 회복 (UMA), DFT 확증 진행**
- **UMA 클린-슬랩**: doped −5.196 / neutral −2.733 (Δ2.46) — 옛 Δ0.04는 **슬랩 아티팩트**였음이
  판명되어 방향성이 **강한 수치로 복귀**. 해석: doped **라디칼은 공유 화학흡착**(S–O 1.51 Å),
  neutral은 O-배위 — Kang 2025 사다리(이온성≫극성≫vdW)와 정합.
- **절대값 인용은 Phase-B DFT+U VERDICT 후** (진행: 분자 2/5, slab u0→u62).

### 3.9 ★신설 — H-form 논쟁 화해 + H↔Li 교환 에너지학 (07-11 완결)

**(a) 화해 구도** (합성서 "이온교환했으니 SO₃H 무조건 존재" vs 우리 "IR에 O–H 없음"):
> **"H-form 맞음(조성·H⁺ 총량). 단 그 H는 상온에서 S–O–H 공유결합으로 있지 않다"** —
> ① 폴라론 상쇄 몫(도핑률 α ~25–35%)의 술포네이트엔 **애초에 H 배정 없음** (이온교환은 양이온만
> 교체, 백본 탈도핑 아님) ② 나머지 SO₃H는 초강산(pKa≈−2) + 흡습 매트릭스(수용액 공정, 60 °C
> 건조로 결합수 제거 불가) → 잔류 수분에 **이온화**(SO₃⁻ + H₃O⁺) ③ Nafion "H-form"과 동일한
> 교과서 현상. **판정 실험 제안**: 엄격 무수화(>110 °C 진공) 후 FTIR — O–H가 나타나면 양쪽 주장
> 완전 화해("무수=SO₃H / 대기=이온화").

**(b) 교환 에너지학 (로컬 ORCA so3li/anion, r2SCAN-3c)**:
| 량 | 값 | 뜻 |
|---|---|---|
| DPE (SO₃H→SO₃⁻+H⁺) | +14.17 eV | 맨 양성자 비용 (문헌 ~14.0 → sanity OK) |
| **LCA (SO₃⁻+Li⁺→SO₃Li)** | **−6.76 eV** | **비면 Li⁺를 잠근다** |
| 교환 (맨 H⁺ 기준) | +7.42 eV | = DPE−LCA (검산 통과) |
| EA (radical+e⁻→anion) | +3.67 eV | 자가도핑형↔SO₃⁻형 연결 |
- **펀치라인**: 양성자 수용처만 있으면 교환은 성립 — **PA(H₂O)=7.16 → 물 1개로 +0.26 eV(본전),
  물 2개(PA 8.37)로 −0.95 eV(내리막)**; 벌크 수화/SE 염기는 더 내리막.
- **통합 결론(곁사슬의 일생)**: 합성 직후 H-form(조성) → 대기 수분에 이온화(IR O–H 부재) →
  전지 내 Li⁺ 바다에서 **operando 형태 = SO₃Li** (LCA −6.76) — 경로는 표면(LNO)이 아니라
  저장고와의 이온교환(3.1 스크린 음성과 정합). **부가 이득**: SO₃H 잔존 시 황화물 SE 산-공격
  (H₂S) 우려 → SO₃Li화는 그 위험 제거 + Li⁺ 정거장 추가 = 설계에 유리한 방향.

---
## 4. 전극 수준 (매뉴스크립트 앵커) — 원본 유지
(SBE/DBE/@C-SUS 체계, S12 dual-binder 물리, Fig3a/4b/4c/6d-f/7 수치, Fig4(e)·7(c,d) 슬롯,
미확보 = SBE/DBE 조성 wt% — 변동 없음)

## 5. 문헌 맥락 — 원본 유지
(Kang 2025 bollard 사다리 = §3.8 방향의 외부 지지 — 이제 자체 UMA 수치로도 성립;
Han 2025 ICEP = §3.6 사다리의 실험 선례; novelty 포지셔닝 동일 — **(i) 3기능 단일분자**는
§3.6 정량으로, **(ii) γ→coh→MPM 매핑**은 Phase-B 후 γ 재산출로 각각 강화 예정)

## 6. 모델 구현 — 원본 유지 + metadata 갱신
- ★`anchor_status`: `INVALID_WRONG_MONOMER_recompute_pending` → **`VALID_v7c_phaseA_clean_UMA
  (doped_chel_r90 −5.196 / neutral_chel_r0 −2.733; DFT+U confirm pending)`**
- γ/coh 갱신은 클린 footprint 재측정 + Phase-B 후 일괄 (§2.1 주의 참조).

## 7. 로드맵 (★현행화)
1. **DFT 트랙**: ✔v7c 확정 → ✔ORCA opt+freq → ✔IR/Raman 실험 대조 판정(§1.3) → ✔클린-슬랩
   재구축(scf_u62 추출) → ✔Phase-A 재랭킹(§2.1) → ✔Li⁺ 패키지(§3.6) → ✔H↔Li 교환(§3.9)
   → 🔶**Phase-B DFT+U 5-SCF 진행**(분자 2/5; slab u0→u62 U-ramp; gabia) → footprint/γ 재산출
   → coh 앵커 갱신 → (옵션) Li⁺ NEB 장벽 / SO₃Li 형태의 Li-지형 / 무수-FTIR 판정 실험(실험실)
2. A4 마지막 관문 (SuperP thinky divergence 런) — 변동 없음
3. 비교셋 (블로커: SBE/DBE 조성 wt%) — 변동 없음
4. STEP3 이중-전도 σ 배정 — 변동 없음

## 8. 파일 맵 (★확장)
- 이 문서: `kb/projects/sdcp_master_v2_2026_07_11.md` (DEM-DFT repo) → DEM-MPM 방 `docs/sdcp_master.md` 교체용
- **분광 판정 완전판(입문 설명 포함)**: `kb/projects/sdcp_v7c_structure_spectroscopy_report_2026_07_10.md`
- **Phase-A 클린 랭킹 데이터**: `db/properties/sdcp_linio2_binding_phaseA.csv` (12배향 + 아티팩트 기록)
- **Li⁺ 결합 + 교환 에너지학 + 표면 스크린**: `db/properties/sdcp_v7c_li_binding.csv`
- 도구: `tools/sdcp/phaseA_v7c_orient_scan.py`(--freeze_frac), `extract_scf_slab.py`(클린 슬랩+AFM 맵),
  `phaseB_v7c_dft_binding.py`(5-SCF 생성기, AFM 인덱스 상속·U-ramp 대응), `run_phaseB_gabia.sh`
  (U-ramp 2단계 런처), `sbatch_phaseB_kisti_chain.sh`(백업), watch 2종
- 산출 그림/CSV: annotated 구조 2종, IR/Raman 계산·실험 겹침 4종, arbitration, Li-binding bar,
  배정표 CSV (분광 보고 §9 인벤토리 참조)
- 원본(그 방): `docs/sdcp_master.md`, `docs/sdcp_manuscript_anchors.md`, litdb 2편, backlog A4/A4′

---
*다음 갱신 트리거: Phase-B 5/5 → §2.1에 DFT VERDICT 행 + §3.8 ✅승격 + footprint/γ + §6 coh 앵커.*
