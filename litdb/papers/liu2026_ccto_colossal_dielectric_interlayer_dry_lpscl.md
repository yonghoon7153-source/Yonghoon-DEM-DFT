<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md.
     2026-11-06 작성: 크롭 65장 (본문 그림 6 + SI 그림 54 + SI 표 5) 중 그림 25장을 실제로 보고 figure-read 값을 넣었다.
     SI 그림 4장 (S2 · S14 · S22 · S38) 은 도구가 '그래픽 없음' 으로 건너뛰어 손으로 잘랐다 (figures.json manual_crop).
     벡터 그림 (Fig. S23 · S37 · S39) 은 PDF 경로 좌표로, 래스터 (Fig. S5 · Fig. 5a,e) 는 픽셀로 다시 읽어 본문 숫자와 대조했다 (§10).
     재판독 스크립트 = tools/litdb/liu2026_ccto_readout.py (s23 · s39 · s37 · s5 · f5a · --selftest).
     이 digest 는 우리 절대값을 문헌값 옆에 두지 않는다 (의뢰 조건 · CLAUDE.md §litdb) — 우리 일과는 방법 · 정의 수준으로만 엮었다 (§7). -->

# Colossal-dielectric cathode interface engineering enables interfacial stability in dry-processed Li₆PS₅Cl solid-state batteries — Liu et al. (*J. Colloid Interface Sci.* **729** (2027) 141891) — **[외부]**

> slug `liu2026_ccto_colossal_dielectric_interlayer_dry_lpscl` · DOI `10.1016/j.jcis.2026.141891` · type `exp + 계산 보조 (분자 DFT B3LYP-D3 · 주기 DFT CP2K PBE / PBE+U · AIMD 600 K · 고전 MD GROMACS) — 유한요소 · 전기장 모의 0 · 유전율 측정 0` · PDF `litdb/inbox/Colossal-dielectric cathode interface engineering enables interfacial stability in dry-processed Li6PS5Cl solid-state batteries.pdf` (본문 14 pp) + `litdb/inbox/Sup) Colossal-dielectric … .pdf` (SI 70 pp: Fig. S1–S54 · Table S1–S5 · SI 제목은 *"… All-Solid-State Batteries"*) · digested `2026-11-06` · status ✅ · 태그 **[외부]**
> elements: Li, P, S, Cl, Ca, Cu, Ti, O, F, N, C, Fe, Ni, Co, Mn
> methods: DFT, AIMD, MD, DOS, PDOS, ELF, ESW, XPS, Raman

> **저자**: **Liequan Liu**ᵃᵇ · Zhilin Wuᵃ · Delong Xuᵇ · Yaohui Quᵈ · Jianxin Caiᵇ · **Ze Zhang**ᵇ\* · **Ke Li**ᵃ\* · **Lingfeng Zhu**ᶜ\* — ᵃ 南昌大 School of Advanced Manufacturing · ᵇ 南昌大 School of Chemistry and Chemical Engineering · ᶜ RMIT University School of Science (Melbourne) · ᵈ 江西师范大 Jiangxi Provincial Key Lab of Green Hydrogen and Advanced Catalysis. 접수 2026-08-26 · 수정 2026-10-25 · 수리 2026-10-28 · 온라인 2026-11-02 · **OA CC BY**. 지원 NSFC 52463025 · Jiangxi 리튬이온전지 재료 중점실험실 2024SSY05202 · Jiangxi 자연과학기금 20242BAB25248 · JXAST 청년인재 2023QT07. CRediT 에서 **Software 는 Lingfeng Zhu (RMIT)** 다 — 계산 담당으로 읽힌다. 데이터: *"available in the Manuscript and the Supporting Information"* (원자 구조 · 입력 파일 공개 없음).
> **[외부]** — 남창대 · 강서사범대 · RMIT. 우리 그룹 · 팔로우 랩 · 공저 아님.
>
> **계보 / litdb 연결**: ref [12] (in-situ poly(sulfate) 코팅) = `[Deng26PS]` `papers/deng2026_polysulfate_layer_moisture_oxidation_lpsc.md` · ref [20] (건식 ZrO₂₋ₓ 양극 껍질 코팅, *Small* e73805) = `papers/choi2026_bzox_dry_zro2x_nmc_shell_coating.md` · ref [23] (*"A dielectric electrolyte composite with high lithium-ion conductivity for high-voltage solid-state lithium metal batteries"*, *Nat. Nanotechnol.* 18 (2023) 602 — 유전체 충전재 복합전해질 개념의 직계 선행) = **litdb digest 없음** · ref [10] (PTFE 의 전자띠 공학 안정화, *Adv. Energy Mater.* 16 (2026) e70845) = digest 없음. SI ref [22] 는 1저자 자신의 앞 논문 (MOF 기반 고체전해질, *Nano Energy* 154 (2026) 111986) — SI 캡션의 복붙 흔적이 그쪽 어휘다 (§10-⑮).

> **본 digest 에서 실제로 본 그림 (2026-11-06) — 25장**: `Fig. 1` `Fig. 2` `Fig. 3` `Fig. 4` `Fig. 5` `Fig. 6` (본문 전부) · `Fig. S5` `Fig. S13` `Fig. S14` `Fig. S22` `Fig. S23` `Fig. S24` `Fig. S25` `Fig. S26` `Fig. S31` `Fig. S33` `Fig. S34` `Fig. S36` `Fig. S37` `Fig. S38` `Fig. S40` `Fig. S42` `Fig. S46` `Fig. S53` `Fig. S54`.
> **이미지로 안 보고 PDF 벡터 · 텍스트로만 읽은 것**: `Fig. S39` (곡선 좌표로 0.1 mA 교차점 계산) · `Fig. S2` · `Fig. S12` · `Fig. S16` · `Fig. S41` (그림 안 숫자 라벨은 PDF 텍스트).
> **안 본 것 (35장)**: `Fig. S1` `Fig. S3`–`Fig. S4` `Fig. S6`–`Fig. S11` `Fig. S15` `Fig. S17`–`Fig. S21` `Fig. S27`–`Fig. S30` `Fig. S32` `Fig. S35` `Fig. S43`–`Fig. S45` `Fig. S47`–`Fig. S52` · 표 5장 (`Table S1`–`Table S5`) 은 PDF 텍스트가 정확해서 이미지로 안 봤다.
> 그림에서만 읽은 값은 **`figure-read ≈`**, 우리가 계산해 낸 값은 **(우리 산수)** 로 표시했다. 벡터 · 픽셀 재판독 (`Fig. S23` · `Fig. S37` · `Fig. S39` · `Fig. S5` · `Fig. 5a`) 은 `tools/litdb/liu2026_ccto_readout.py` 로 다시 낼 수 있다 (PDF 는 litdb/inbox — 리포 밖).

---

## 0. 이 digest 를 읽는 법 — 먼저 읽을 것 여섯

1. **'거대 유전체' = 상용 CaCu₃Ti₄O₁₂ (CCTO) 분말** (Hunan Yuxiling New Materials, AR 99 %) — 직접 합성하지 않았고, `Fig. S31` 에서 입자는 **≈1–10 µm, 큰 것은 20 µm 넘게** 보인다 (figure-read · 본문은 'nanoparticles · nanofillers' 라 부른다). 이 분말을 **PAN : LiTFSI : Pyr₁₃TFSI : CCTO = 3 : 3 : 8 : 4 (질량비)** 로 DMF 22 mL 에 섞은 용액을, **이미 다 만든 습식 양극 원판 (Ø 12 mm) 위에 25 µL 떨어뜨려** 말린 막이 **PLIC** 다 (CCTO 없는 대조 = **PLI**). 두께 **≈3 µm** (`Fig. S34` 마이크로미터 0.051 → 0.054 mm) · CCTO **≈0.2 mg cm⁻²**.
2. **건식 공정은 SE 막에만 쓰였다.** LPSC : PTFE = 99 : 1 → 손으로 반죽 → **고에너지 볼밀로 피브릴화** → 80 °C 열압 → ≈50 µm · Ø 19 mm. **양극은 평범한 습식 슬러리**다 (활물질 : Super P : **PVDF** : **Pyr₁₃TFSI** = 75 : 5 : 10 : 10, NMP, 탄소코팅 Al 박). 즉 PTFE 와 CCTO 는 **서로 다른 층에 있고 섞이지 않는다.**
3. **이온성 액체가 셀 곳곳에 있다** — 양극 안 10 wt% · 중간층 고형분의 44 wt% · Li 금속 쪽에 Li-IL (1 M LiTFSI/Pyr₁₃TFSI) 5 µL. 엄밀히는 '전고체' 가 아니라 **IL 이 든 하이브리드 (준고체) 셀**이다 (§10-⑥).
4. **CCTO 의 순효과를 재는 대조는 PLI ↔ PLIC 이다.** `Fig. 1c,d` 는 '중간층 없음 ↔ PLIC' 라 *중간층 자체* 의 효과와 *CCTO* 의 효과가 섞여 있다. **PLI 만으로도 ACIPO (끝없는 충전) 는 사라진다** — PLI 셀이 LFP 로 ≈480–495 사이클, NCM811 로 80 사이클을 돈다. CCTO 몫은 σ · 창 · σ_e 에서 작고, 장기 사이클에서만 크다 (§3b · §10-②).
5. **유전율을 한 번도 재지 않는다.** *"ε ≈ 10⁴–10⁵"* 는 인용이고 (`Fig. S24` 는 결정구조 그림일 뿐), 기전의 핵심인 '계면 전기장 균질화' 는 저자 스스로 *"We **hypothesize**"* · *"**may** induce interfacial polarization"* 로 적었다. 공간전하층 (space-charge layer) 은 **한 번도 언급되지 않는다**. TEM · ToF-SIMS · 유한요소 · 전기장 모의도 **0** 이다.
6. **본문 숫자와 자기 그림이 여러 곳에서 어긋난다** (우리가 벡터 · 픽셀로 다시 읽은 것, §10-③): σ 1.44/1.40 → 그려진 점 **1.36/1.28 mS cm⁻¹** (그러면 *"둘 다 LPSC-PTFE 보다 높다"* 가 성립 안 함) · LPSC-PTFE 창 라벨 3.69 V → 자기 기준 (0.1 mA) 교차는 **≈3.88 V** · AIMD D 6.77×10⁻⁵ = **MSD 기울기 그 자체** (1/6 누락 의심) · '1100 사이클' → 데이터 끝 **≈1055–1060**.

---

## 0b. 의뢰 질문 넷에 대한 답 (요약 — 상세는 본문 절)

### Q1. '바인더 같다' 는 느낌 — 맞는 것과 다른 것

**맞는 것**: PLIC 는 **고분자 (PAN) 기지에 무기 입자 (CCTO) 를 섞은 용액을 전극 위에 바르고 말린 '고분자 복합 막'** 이다. 바인더 용액을 조제해 바르는 공정과 생김새가 같고, 저자는 그 막이 양극 공극으로 **일부 스며들어 'gradient interphase'** 를 만든다고 하며 (`Fig. S32`–`Fig. S33`), **'CCTO 의 기계적 보강'** 으로 LFP 부피변화에도 금이 안 간다고 말한다 (`Fig. 6a–d` · `Fig. S50`–`Fig. S51`). 결착제 같은 *역학적* 역할을 일부 주장하는 셈이다.
**다른 것**: ① 기능이 **입자를 묶는 결착이 아니라, 건식 LPSC 막과 양극 (활물질 + 탄소) 을 떼어 놓는 '이온은 통하고 전자는 막는 칸막이'** 다 — 저자 표현으로 *"complete physical separation between LPSC, cathode active materials, and conductive carbon"*. ② **양극의 바인더는 따로 있다** (PVDF 10 wt%). ③ **건식 공정의 PTFE 피브릴 바인더와는 관계가 없다** — PTFE 는 SE 막 (1 wt%) 에만 있고 CCTO 는 그 막에 안 들어간다. ④ CCTO 는 **양극 입자 코팅 (껍질) 도 아니다** — 입자 하나하나를 싸는 `choi2026` (건식 ZrO₂₋ₓ 껍질) 과 달리, 전극 표면에 **한 겹** 얹은 막의 **충전재 (22 wt% · ≈7 vol%, 우리 산수 §4g)** 다. ⑤ 고형분 무게의 **44 % 가 이온성 액체** (≈50 vol%, 우리 산수) — '고체 바인더' 보다 **'이온겔 (겔 고분자 전해질) 중간층'** 이 맞는 이름이다.
⇒ **판정**: *바인더가 아니다. 바인더 같은 고분자 용액 공정으로 만든 '양극 쪽 이온겔 중간층 (artificial interlayer)' 이고, CCTO 는 그 겔의 무기 충전재다.* 느낌이 맞은 지점은 '공정 · 재료가 바인더를 닮았다' 는 것이고, 틀린 지점은 '역할' 이다.

### Q2. 기전 주장과 그 근거

| 주장 | 근거로 든 측정 · 계산 | 판정 (§10) |
|---|---|---|
| ① 물리적 격리 + 전자 차단 → ACIPO 억제 · 고전압 | DC 분극 σ_e (`Fig. S14` · `Fig. S38`) · 부유시험 (`Fig. 3g`) · LSV (`Fig. S23` · `Fig. S39`) · 충전곡선 (`Fig. 1c,d` · `Fig. S22`) | **가장 탄탄** — 단 대부분 **PLI 도 같이 한다**. CCTO 몫은 σ_e 3.36 → 1.05×10⁻¹¹ S cm⁻¹ (3.2×) · 창 4.57 → 4.62 V |
| ② 거대 유전율 → 계면 전기장 균질화 | **측정 · 계산 없음** (*"hypothesize"* · *"may"*) | **근거 0** — ε 를 안 쟀고, 정상상태 이온전도 매질에서 전기장은 σ 가 정한다 (§6 · §10-①) |
| ③ CCTO 의 TFSI⁻ 고정 → 염 해리 · 자유 Li⁺ 증가 | DFT 결합에너지 TFSI⁻–CCTO −4.19 eV (`Fig. 2e`) · Raman 분해 (`Fig. 3i` · `Fig. S41`) · MD 배위수 (`Fig. 4a–d`) | **약함** — Raman 차이 ≤ 3.3 %p · 대역 겹침 · 기체상 결합에너지 (§10-⑧ · ⑭) |
| ④ Li⁺ 이동 기전 전환 ('음이온 사슬 보조' → 'CCTO 표면 전도') · D 6–7× | 고전 MD MSD (`Fig. 4e`) · 결합에너지 (`Fig. S42`) | **정의 안 된 D** — MSD 총 ≈2 Å² (도약 1회 미만) (§10-⑧i) |
| ⑤ LiF · Li₃N 많은 CEI | XPS (`Fig. 6e–g` · `Fig. S53`–`Fig. S54`) | **약함** — 분석면은 중간층 겔 표면 · LiF 1.9 → 2.6 % · 'Li₃N' 귀속 의심 (§10-⑦) |
| ⑥ 기계적 보강 (균열 · 팽윤 억제) | AFM · SEM · EDS · 사진 (`Fig. 6a–d` · `Fig. S49`–`Fig. S51`) | 정성 — 거칠기 수치 · 기계 시험 0 |
| (CCTO 가 Mott-Hubbard 절연체 · 입계가 산소 풍부 · 미세 축전기 배열) | CP2K PBE+U DOS · 띠구조 · ELF (`Fig. 2a–d` · `Fig. S26`) | **계산이 주장을 못 받친다** — 원시셀 AFM 불가 · U 미기재 · Γ-only DOS · 벌크 셀에 입계 없음 (§8 · §10-⑧) |

**계산 요약** (상세 §8): 분자 DFT = ORCA 6.0 · B3LYP + D3 (BJ 감쇠 문헌 인용) · def2-TZVP / def2/J · 고분자 중합도 10 · E_bind = E(A/B) − E(A) − E(B) (BSSE · 용매 모델 없음). 주기 DFT = CP2K · PBE · GTH · DZVP-MOLOPT-SR-GTH · LPSC 400 Ry (2×2×2 '원시셀 기준') · CCTO 1000 Ry · **DFT+U (U 값 미기재)** · AFM 을 원시셀 Cu 에 부과 · SCF 9×9×9 k · **PDOS · ELF 는 Γ 파동함수**. AIMD = LPSC · **NPT 600 K · 1 atm · 1 fs · 총 ≈3.8 ps** (`Fig. S5` figure-read). 고전 MD = GROMACS 2025.3 · Sobtop 역장 · RESP 전하 (CCTO 는 REPEAT) · 1.5 nm 절단 · PME · 500 K 가열 → 298.15 K 담금 (평형 총 20 ns) → **NPT 50 ns 생산**. 유전율 값의 출처는 **인용 [23]** 뿐 — 계산 · 측정 0.

### Q3. 연구 진행 순서와 단계별 핵심 수치 → §0c 표 · §5

### Q4. 우리 일과의 연결 → §7 (숫자 섞지 않음)

---

## 0c. 연구 진행 순서 (설계 동기 → 재료 → 제작 → 분석 → 전기화학)

| 단계 | 무엇을 했나 | 핵심 수치 (논문 값 · figure-read 는 표시) | 그림 |
|---|---|---|---|
| 1 동기 | 건식 LPSC-PTFE 막 + 습식 양극을 **직접 맞대면** 끝없는 충전 (ACIPO) | NCM811 (LiNbO₃ 코팅): 시작 ≈2.2 V · 180 mAh g⁻¹ 에서 ≈2.6 V · 삽도 ≈700–1250 mAh g⁻¹ 를 ≈3.45–3.5 V 에서 (figure-read) · LFP: ≈3.45–3.47 V 평탄이 ≈720 mAh g⁻¹ 까지 (figure-read) · LPSC-PTFE LSV 라벨 **3.69 V** | `Fig. 1c` · `Fig. S22` · `Fig. S23` |
| 2 SE 막 | LPSC : PTFE 99 : 1 · 볼밀 피브릴화 · 80 °C 열압 | 분말 σ **5.5** (30 °C) · 22.5 (60 °C) mS cm⁻¹ · Ea **0.41** eV · σ_e 7.02×10⁻⁹ S cm⁻¹ → 막 σ **1.39** · 4.75 mS cm⁻¹ · Ea **0.35** eV · σ_e 8.57×10⁻¹¹ · t_Li⁺ 0.94 · CCD **0.27** mA cm⁻² · Li‖Li 650 h @0.2 mA cm⁻² (95 mV) · Li‖Cu CE ≈97.5 % · 두께 ≈50–55 µm · 15×10 cm² 시트 · 30 µm 는 단락 잦음 | `Fig. S1`–`Fig. S21` |
| 3 재료 고르기 | CCTO 의 전자구조 (DFT) · TFSI⁻ 결합 · IL 양이온 18종 HOMO/LUMO 선별 → Pyr₁₃⁺ | 'gap ≈1.5 eV' (인용 [24,25]) · TFSI⁻–CCTO **−4.19 eV** · Pyr₁₃⁺ HOMO −13.13 / LUMO −3.34 eV (gap **9.79** eV, `Table S1` — 본문은 9.6) · 가격 89.98 ¥/5 g (`Table S2`) | `Fig. 2` · `Fig. S26` · `Fig. S27` · `Fig. S40` |
| 4 중간층 | PLI (3:3:8) · PLIC (3:3:8:4) DMF 용액 → 양극 원판에 25 µL 적하 → 상온 12 h + 60 °C 진공 12 h | 두께 **3 µm** · CCTO ≈0.2 mg cm⁻² · XRD PAN 17° 봉우리 PAN > PLI > PLIC · CCTO 회절선 유지 | `Fig. 3a–e` · `Fig. S28`–`Fig. S35` |
| 5 중간층 물성 | EIS · DC 분극 · LSV · 부유 · CV · Raman | σ (적층) **1.40 / 1.44** mS cm⁻¹ (그려진 점 1.28 / 1.36, §10-③) · Ea 0.29 / 0.30 eV · σ_e 3.36 / 1.05×10⁻¹¹ · 창 **4.57 / 4.62 V** · 부유 PLI 4.6 V 부터 누설 · 도금 과전압 51.6 / 50.8 mV · 자유 TFSI⁻ 11.8 / **8.5 %** | `Fig. 3f–i` · `Fig. S36`–`Fig. S41` |
| 6 기전 모의 | GROMACS MD · DFT 결합에너지 · ESP | CN Li–O(TFSI⁻) **4.33 → 3.47** · Li–N(PAN) 0.85 → 0.74 · Li–O(CCTO) **1.29** · 총 5.18 → 5.50 · D **1.18 → 7.58×10⁻¹⁰** cm² s⁻¹ · Li⁺ 결합 TFSI⁻ −6.26 / PAN −2.96 / CCTO −4.26 eV | `Fig. 4` · `Fig. S42`–`Fig. S43` |
| 7 셀 | LFP‖Li (1 C · 30 °C) · 율속 · NCM811‖Li (0.5 C · 2.8–4.4 V) · LFP 파우치 | LFP PLIC 112.6 → 100.4 mAh g⁻¹ **(1100th, 89.2 %)** / PLI 112.5 → 89.5 (480th, 79.6 %) · 율속 PLIC 170.1/162.5/148.3/115.2 · PLI 169.7/156.2/111.4/99.7 · NCM PLIC 142.3 → 114.2 (150th, 80.3 %) / PLI 111.3 → 68.0 (80th, 61.1 %) · 파우치 169.6 mAh g⁻¹ @0.1 C · 25 사이클 · CE > 99.9 % · 6×8 cm² · 5 mg cm⁻² · 0.85 mAh cm⁻² | `Fig. 5` · `Fig. S44`–`Fig. S48` |
| 8 사후 | AFM · SEM · EDS · XPS (양극 면) | LiF **1.9 → 2.6 %** · 'Li₃N' **0.7 → 1.5 %** · 원소 C 32.6/34.8 · F 28.4/27 · Li 6.5/5.1 · N 7.6/10.9 · O 17.2/14.7 · S 7.7/7.6 % (PLI/PLIC) | `Fig. 6` · `Fig. S49`–`Fig. S54` |

---

## 1. 한 줄 요약

건식 Li₆PS₅Cl–PTFE (99 : 1) 막을 **습식 LFP · NCM811 양극과 직접 맞대면 충전이 끝나지 않는 기생 산화 (저자 용어 ACIPO)** 가 나는데, 양극 위에 **PAN · LiTFSI · Pyr₁₃TFSI 이온겔에 상용 CaCu₃Ti₄O₁₂ 분말 22 wt% 를 섞은 ≈3 µm 막 (PLIC)** 을 떨어뜨려 입히면 그것이 사라지고 LFP‖Li 가 1 C 로 오래 돈다. **격리 효과의 대부분은 CCTO 없는 같은 겔 (PLI) 로도 나오며**, '거대 유전율' 의 역할은 측정 · 계산 어느 쪽으로도 확인되지 않은 가설이다.

---

## 2. 메타 / 동기 / 질문

| 저자 | 저널/년 | DOI | 조성 | 연구유형 |
|---|---|---|---|---|
| L. Liu · Z. Wu · D. Xu · Y. Qu · J. Cai · **Z. Zhang\*** · **K. Li\*** · **L. Zhu\*** | *J. Colloid Interface Sci.* 729 (2027) 141891 (온라인 2026-11-02) | 10.1016/j.jcis.2026.141891 | SE = 상용 Li₆PS₅Cl (Shenzhen Kejing) + PTFE 1 wt% · 중간층 = PAN (Mw 15,000) / LiTFSI / Pyr₁₃TFSI / CaCu₃Ti₄O₁₂ · 양극 = LFP · NCM811 (Fig. 1c 는 LiNbO₃ 코팅 NCM811) · 음극 = Li 금속 | exp 주축 + DFT/AIMD/MD 보조 |

**동기 (서론)**: 건식 공정은 무용매 · 박막 (< 30 µm) · 배치 재현성 때문에 상용화 1순위인데, **건식 PTFE 결착 황화물 막과 기존 습식 양극의 짝** 이 맞지 않는다. 저자가 드는 원인 둘: ① **PTFE** — *"During charging, the strong electron-withdrawing nature of fluorine in PTFE facilitates **electron injection** into its frontier orbitals, weakening C–F bonds and triggering irreversible defluorination to form LiF and carbonaceous residues [10]"* (⚠ 전자 주입 = **환원** 이다 — §10-⑱) ② **LPSC 의 S²⁻** 가 도전 탄소 · 양극과 닿으면 심하게 산화되어 이온 · 전자 절연 산물을 만든다. 이것이 **ACIPO** (*anomalous capacity originating from interfacial parasitic oxidation*) — 저자가 만든 이름이다.
**질문**: 그 접촉을 끊는 중간층을 넣으면서 이온 전도를 잃지 않을 수 있나? 그 중간층에 **거대 유전체 CCTO** 를 넣으면 무엇이 더 좋아지나?
**저자 결론** (`Conclusion`): *"The plausible underlying mechanism lies in the intrinsic giant dielectric property of CCTO, which homogenizes the interfacial electric field and eliminates localized current hotspots … Most importantly, CCTO facilitates the in-situ formation of robust LiF- and Li₃N-rich CEI layers"*. 끝 단락에서 스스로 *"Further efforts will focus on **direct experimental validation** to consolidate the proposed mechanistic picture"* 라 적었다 — 기전이 검증 전이라는 저자 자신의 인정이다.

---

## 3. 핵심 수치 총정리 ★

### 3a. 재료 · 건식 SE 막 (LPSC-PTFE)

| 양 | 값 | 조건 | 근거 |
|---|---|---|---|
| LPSC 분말 σ | **5.5** mS cm⁻¹ (30 °C) · ≈22.5 (60 °C) · `Table S3` 5.49 | SS/SS EIS 1 MHz–0.1 Hz · 30–60 °C | `Fig. S1` (안 봄) |
| LPSC 분말 Ea | **0.41** eV — 저자: *"grain boundary-limited"* | 30–60 °C 4 점 | `Fig. S1` |
| LPSC 분말 σ_e | 7.02×10⁻⁹ S cm⁻¹ (그림 · 본문) · `Table S3` 7.09×10⁻⁶ **mS** cm⁻¹ (= 7.09×10⁻⁹ S cm⁻¹ — 두 값이 0.07 어긋남) | DC 10 mV · 3600 s · Is 1.89×10⁻⁶ mA | `Fig. S2` (텍스트) |
| 막 σ | **1.39** mS cm⁻¹ (30 °C) → 4.75 (60 °C) · Ea **0.35** eV | 같은 EIS · R(30 °C) figure-read ≈11 Ω | `Fig. S13` |
| 막 σ_e | **8.57×10⁻¹¹** S cm⁻¹ · Is 2.97×10⁻⁶ mA (3600 s 에도 전류가 아직 내려가는 중, 본 그림) | DC 10 mV · 3600 s | `Fig. S14` |
| t_Li⁺ | **0.94** (I₀ 11.12 · Is 10.52 µA) | Li‖Li · 10 mV | `Fig. S15` (SI 텍스트) |
| Li 핵생성 과전압 (SS) | 본문 **56.8 mV** · 그림 라벨 **50.5 mV** (어긋남) | SS‖LPSC-PTFE‖Li CV 1 mV s⁻¹ | `Fig. S16` (텍스트) |
| j₀ | 0.09 mA cm⁻² (Tafel) | Li‖Li · ±0.1 V · 0.5 mV s⁻¹ | `Fig. S17` |
| CCD | **0.27** mA cm⁻² — *"moderate tolerance"* | Li‖Li | `Fig. S18` |
| Li‖Li 수명 | 0.2 mA cm⁻² · 0.2 mAh cm⁻² · ≈95 mV 로 **650 h**, 이후 덴드라이트 단락 (SI 서술) | | `Fig. S19` |
| Li‖Cu | CE ≈97.5 % · 200 사이클 · 도금 과전압 24.6 mV | 0.2 mA cm⁻² · 0.2 mAh cm⁻² · 상한 1 V | `Fig. S21` |
| 두께 · 크기 | ≈50 µm (단면 SEM) · 55 µm (마이크로미터) · 15×10 cm² 시트 · ≈30 µm 는 *"high incidence of short circuits"* 라 55 µm 선택 | | `Fig. S9` · `Fig. S11` |
| XRD | PTFE 18° 봉우리는 1 wt% 라 막에서 안 보임 · LPSC = PDF# 97-041-8490 | Cu Kα | `Fig. S12` (텍스트) |
| LSV 창 | 라벨 **3.69 V** (우리 벡터 판독: 0.1 mA 교차 **≈3.88 V** 삽도 · ≈3.93 V 본도) | SS‖막‖Li · 0–6 V · **5 mV s⁻¹** · 차단 100 µA (= 50 µA cm⁻² ⇒ SS 2.0 cm²) | `Fig. S23` |

> 🔢 **홉 수 검산** (규약 `D-2026-09-27-barrier-hop-count` · ν₀ 10¹³ s⁻¹ **가정**): 위 Ea 는 σ 아레니우스의 겉보기 활성화에너지다 (단일 장벽이 아니다). 그래도 차수만 보면 303 K 에서 0.35 eV → Γ ≈ 1.5×10⁷ s⁻¹ (평균 대기 ≈70 ns) · 0.41 eV → Γ ≈ 1.5×10⁶ s⁻¹ (≈0.7 µs) — mS cm⁻¹ 급 '빠르다' 서술과 차수 모순 없음.

### 3b. 중간층 PLI ↔ PLIC — CCTO 의 순효과는 이 열의 차이다

| 양 | PLI | PLIC | 차이 (PLIC/PLI) | 근거 |
|---|---|---|---|---|
| σ (적층, 30 °C) 본문 · `Table S3` | 1.40 | 1.44 mS cm⁻¹ | ×1.03 | `Fig. 3f` 라벨 |
| σ (30 °C) **그려진 점** (벡터 좌표) | **1.284** | **1.357** mS cm⁻¹ | ×1.06 | `Fig. S37` (우리 판독 · `Fig. 3f` figure-read 도 ≈1.28 / ≈1.37) |
| σ 60 °C (벡터) | 3.569 | 3.973 | ×1.11 | `Fig. S37` |
| Ea | 0.29 | 0.30 eV (벡터 재적합 0.294 / 0.309) | PLIC 가 오히려 큼 | `Fig. S37` |
| R (30 °C, EIS 고주파 절편) | figure-read ≈19.5 Ω | ≈18 Ω | — (LPSC-PTFE 단독 ≈11 Ω) | `Fig. S36` · `Fig. S13` |
| σ_e | 3.36×10⁻¹¹ (Is 6.75×10⁻⁷ mA) | **1.05×10⁻¹¹** S cm⁻¹ (Is 1.54×10⁻⁷ mA ≈ 0.15 nA) | ÷3.2 | `Fig. S38` |
| LSV 창 (0.1 mA) | 4.57 V (벡터 4.58) | **4.62 V** (벡터 4.62) | +0.05 V | `Fig. S39` |
| 부유시험 첫 누설 | **4.6 V** (≈40 µA · 4.7 V 에선 ≈75 → 120 µA 상승, figure-read) | **4.7 V** (≈45 µA, figure-read · 4.6 V 까지 ≲5 µA) | 한 칸 (0.1 V) | `Fig. 3g` |
| Li 도금 개시 과전압 | 51.6 mV | 50.8 mV | −0.8 mV (LPSC-PTFE 50.5 mV 와 셋 다 같다) | `Fig. 3h` · `Fig. S16` |
| Raman 자유 TFSI⁻ / SSIP+CIP / AGG+CCTO-TFSI⁻ | 11.8 / 62.8 / 25.3 % | **8.5** / 64.2 / 27.3 % | −3.3 / +1.4 / +2.0 %p | `Fig. S41` |
| MD CN Li–O(TFSI⁻) / Li–N(PAN) / Li–O(CCTO) / 합 | 4.33 / 0.85 / — / 5.18 | **3.47** / 0.74 / **1.29** / 5.50 | | `Fig. 4d` |
| MD D_Li⁺ | 1.18×10⁻¹⁰ | **7.58×10⁻¹⁰** cm² s⁻¹ | ×6.4 | `Fig. 4e` |
| LFP‖Li 1 C 수명 | 112.5 → 89.5 mAh g⁻¹ (480th · 79.6 %) · 그림은 ≈495 사이클에서 급락하며 끝남 (figure-read) | 112.6 → 100.4 (1100th · 89.2 %) · 그림 데이터 끝 **≈1055–1060** (픽셀 판독) | | `Fig. 5a` |
| 율속 0.1/0.2/0.5/1 C | 169.7 / 156.2 / 111.4 / 99.7 (회복 169.9) | 170.1 / 162.5 / **148.3** / 115.2 (그려진 0.5 C 점 ≈143–145, 픽셀 판독) | | `Fig. 5e` |
| NCM811‖Li 0.5 C · 2.8–4.4 V | 111.3 → 68.0 (80th · 61.1 %) — 기준 = 첫 사이클 | 142.3 → 114.2 (150th · 80.3 %) — 기준 = 2–3 번째 (첫 점 ≈135 · 최대 ≈157 @≈50, figure-read) | | `Fig. S46` |
| XPS LiF / 'Li₃N' (전체 원자 %) | 1.9 / 0.7 | 2.6 / 1.5 | +0.7 / +0.8 %p | `Fig. 6g` |

### 3c. 셀 · 파우치

- **LFP‖Li · 1 C · 30 °C** (`Fig. 5a`): 위 표. CE *"consistently above 99.8 %"*. ⚠ *"five parallel tests and averaged"* 라 적었지만 **어느 그림에도 오차막대가 없다**.
- **1 C 의 전류밀도** (우리 산수 · 1 C = 170 mAh g⁻¹ 가정): 로딩 1.5–4 mg cm⁻² 면 **0.26–0.68 mA cm⁻²** — 막의 CCD **0.27 mA cm⁻²** 와 같거나 2.5 배 위. 어느 로딩으로 1100 사이클을 돌렸는지 미기재.
- **in-situ EIS + DRT** (`Fig. 5b–d`, 첫 충방전 0.1 C): Nyquist 반원 둘 다 ≈0–80 Ω (figure-read) · DRT 세 대역 — τ ≈10⁻⁴ s '**CEI**' · ≈0.1 s 'ct' · ≈10 s 'Diffusion'. 삽도 τ_CEI 봉우리 높이 PLIC ≈15 · PLI ≈18–20 (figure-read · 차이 ≈1.2 배).
- **파우치** (`Fig. 5f,g` · `Fig. S48`): LFP 5 mg cm⁻² · 0.85 mAh cm⁻² · 6×8 cm² · Li 50 µm · Cu 집전체 · 0.1 C · 169.6 mAh g⁻¹ · 25 사이클 거의 무손실 · CE > 99.9 %. 총 용량 ≈41 mAh (우리 산수). 접기 · 자르기 · 못 찌르기 뒤에도 LED 점등 · *"no signs of thermal runaway, fire, or explosion"* (정성). ⚠ 삽도 구조도에 **PLIC 층이 그려져 있지 않다** (LFP / LPSC Film / Li / Cu 만).

### 3d. 분광 (Raman · XPS)

- **Raman** (`Fig. 3i`, 760 → 730 cm⁻¹ 역축): 본문 대역 = 자유 TFSI⁻ **732** · SSIP **740** · CIP/AGG/CCTO-TFSI⁻ **745** cm⁻¹. 그림의 성분 중심은 figure-read **≈736.5 · ≈742.5 · ≈748** 이고 범례는 *"SSIP/CIP"* · *"ACG/CCTO-TFSI⁻"* (본문과 SSIP · CIP 배정이 다름 · 'ACG' 오식). 데이터 점 산포가 봉우리 높이의 ±20 % 급 (figure-read).
- **XPS** (`Fig. 6e–g` · `Fig. S53`–`Fig. S54`, 사이클 뒤 'LFP 양극 면'): F 1s = −CF₃ ≈688.5 eV 가 거의 전부 · LiF ≈685 eV 는 기준선 수준 (figure-read). N 1s = N⁺(Pyr₁₃⁺) ≈402.2 · **'LiN₃'** 라벨 ≈400.7 (작음) · N(TFSI⁻) ≈399.0 eV (figure-read). **SI 의 P 2p · Cl 1s (LPSC 원소) · Ti 2p · Ca 2p · Cu 2p (CCTO 원소) 스펙트럼은 전부 잡음뿐** (본 그림) · O 1s 는 'C=O' 한 성분 (Li₂O 성분 없음) · Li 1s 는 산포 점에 'LiF₃' · 'LiN₃' · 'ROCO₂Li' 를 맞춘 것 · S 2p 는 SO₂–CF₃ 이중선 + 작은 LiₓSᵧO_z.

### 3e. 계산 결과 (방법은 §8)

| 양 | 값 | 근거 |
|---|---|---|
| CCTO 띠틈 | 본문 *"~1.5 eV [24,25]"* (인용) · 띠구조에서 비점유 첫 띠 (β) ≈ +1.2–1.9 eV (figure-read) | `Fig. 2a,b` |
| CCTO 자기 상태 | 본문 'AFM' · 그림의 α/β DOS 가 거울상이 아니고 HOCO 가 다름 (β HOCO ≈ −0.3 eV, figure-read) | `Fig. 2a` |
| TFSI⁻–CCTO 결합에너지 | **−4.19 eV** | `Fig. 2e` |
| Li⁺ 결합에너지 | TFSI⁻ **−6.26** · PAN **−2.96** · CCTO **−4.26** eV | `Fig. S42` |
| HOMO / LUMO (eV, 기체상 B3LYP) | PAN −9.29 / −0.85 · LiTFSI −8.76 / −1.33 · **TFSI⁻ −4.07 / +4.20** · Pyr₁₃⁺ −13.13 / −3.34 · PTFE −9.43 / −1.23 | `Fig. S40` |
| IL 양이온 18종 gap (eV) | 상위 넷 TPM 9.63 · **Pyr₁₃ 9.79** · Pyr₁₂ 10.12 · PP₁₃ (1M3P) 9.60 · 최저 1-benzyl-3-methylimidazolium 5.25 | `Table S1` · `Fig. 2f` |
| ESP | TFSI⁻ 의 O 가 최저 (−0.2 a.u.) · Pyr₁₃⁺ 는 전부 양 | `Fig. S43` (안 봄 · 본문) |
| AIMD D_Li⁺ (LPSC) | **6.77×10⁻⁵ cm² s⁻¹** — **600 K** (본문에는 온도 표기 없음) · 그려진 적합선 기울기 = 0.677 Å² ps⁻¹ = 6.77×10⁻⁵ cm² s⁻¹ (픽셀 판독) ⇒ D = 기울기/6 이면 ≈1.1×10⁻⁵ | `Fig. S5` |
| MD | 위 §3b 표 | `Fig. 4` |

---

## 4. 재료 & 방법 ★ (공정 순서 그대로 · 우리가 흉내 낼 때 필요한 조건 전부)

### 4a. 재료
LPSC (AR) · PTFE (AR, **Mw 7,700,000**) — Shenzhen Kejing · LiTFSI 99.9 % · Pyr₁₃TFSI AR 99 % — Aladdin · PAN (AR, **Mw 15,000**) · DMF — Macklin · **CCTO AR 99 % — Hunan Yuxiling New Materials** (상용 분말, 입도 미기재 · `Fig. S31` 로만).

### 4b. 건식 SE 막 (LPSC-PTFE)
LPSC : PTFE = **99 : 1** (질량) → **손으로 갈아 반죽 (dough-like)** → **고에너지 볼밀 '피브릴화 완료까지'** (rpm · 시간 · 볼/분말 비 · 분위기 **전부 미기재**) → **80 °C 열압** → ≈50 µm → Ø 19 mm 펀칭 → Ar 글러브박스 보관. ⚠ `Fig. S25` 공정도는 **압연 (calendering)** 을 그린다 — 방법 절은 열압이다.

### 4c. Li-IL · PLI · PLIC 용액
- **Li-IL**: Pyr₁₃TFSI 150 °C 진공 12 h 건조 → 1 M LiTFSI 용해 (상온 12 h 교반) → 다시 150 °C 진공 12 h.
- **PLI**: LiTFSI : PAN : Pyr₁₃TFSI = **3 : 3 : 8** (질량) 을 DMF 22 mL 에 12 h 교반.
- **PLIC**: LiTFSI : PAN : Pyr₁₃TFSI : CCTO = **3 : 3 : 8 : 4** 를 DMF 22 mL 에 12 h 교반. ⚠ **절대 질량이 없다** — 용액 농도를 알 수 없다. CCTO 분산 처리 (초음파 · 분쇄 · 분산제) **없음**.

### 4d. 양극 (습식) + 중간층
- LFP 또는 NCM811 : Super P : **PVDF** : **Pyr₁₃TFSI** = **75 : 5 : 10 : 10** · NMP 슬러리 → **탄소코팅 Al 박** → 60 °C 밤새 건조 → Ø 12 mm → 활물질 **1.5–4 mg cm⁻²**. ⚠ 양극 IL 은 **Li 염 없는 순수 Pyr₁₃TFSI** 로 적혀 있다.
- **중간층**: 원판에 PLI/PLIC 용액 **25 µL 적하** → 상온 자연 증발 12 h → 60 °C 진공 12 h → CCTO **≈0.2 mg cm⁻²**. ⚠ `Fig. S25` 는 **닥터블레이드 도포**를 그린다 — 방법 절은 적하다.
- 전압창: LFP‖Li **2.5–4.0 V** · NCM811‖Li **2.8–4.4 V** · NEWARE · CR2032.

### 4e. 셀 조립
SS 를 쓰는 셀 (SS/SS · Li/SS) 은 **SS 박도 양극과 똑같이** PLI/PLIC 를 적하 · 건조 (그래서 'PLIC σ' 는 SS(PLIC)‖LPSC-PTFE‖SS(PLIC) 적층의 값으로 읽힌다 — 논문이 적층 구성을 그림으로 주지 않는다). **Li 금속 쪽에 Li-IL 5 µL** 를 조립 전 떨어뜨린다. 모든 측정 30 °C · 전위는 Li/Li⁺ 기준.

### 4f. 측정 정의 (식 1–4)
- **σ = L/(R·S)** (L = 두 SS 사이 거리 · S = SS 면적 · R = 'intrinsic impedance') · **σ = σ₀ exp(−Ea/kT)** (σ₀ 를 'finger-forward factor' 라 부른다 — 'pre-exponential factor' 의 번역 오류).
- **σ_e = L·Is/(ΔV·S)** · ΔV 10 mV · 3600 s · ⚠ L · S 의 **숫자가 어디에도 없다**.
- **LSV**: SS/Li · 0–6 V · **5 mV s⁻¹** · 응답전류 차단 **100 µA (50 µA cm⁻²)** ⇒ SS 면적 2.0 cm² 가 함의된다 (우리 산수).
- **CV**: SS/Li −0.25–0.5 V · 1 mV s⁻¹ · **t_Li⁺**: Bruce–Vincent (식 4) · 10 mV · **Tafel/CV**: Li‖Li ±0.1 V · 0.5 mV s⁻¹ · **Li‖Cu**: 0.2 mA cm⁻² · 0.2 mAh cm⁻² · 상한 1 V.
- **XRD** Bruker D8 Cu Kα · *"2θ range of 5–50 degrees"* (⚠ 그림들은 10/5–80° 까지 그린다) · **FESEM** JSM6701F + EDS · AFM · Raman · XPS (장비 · 조건 미기재).

### 4g. 우리 산수 — 논문이 안 준 양 (가정 명시)
| 양 | 값 | 가정 |
|---|---|---|
| 중간층 조성 (질량) | PAN 16.7 · LiTFSI 16.7 · **IL 44.4** · **CCTO 22.2 wt%** | 3 : 3 : 8 : 4 |
| 중간층 조성 (부피) | PAN ≈23 · LiTFSI ≈20 · **IL ≈50** · **CCTO ≈7 vol%** | 밀도 가정 PAN 1.18 · LiTFSI 1.33 · Pyr₁₃TFSI 1.45 · CCTO 5.05 g cm⁻³ (교과서값 · 이 논문에 없음) |
| 중간층 고형분 면밀도 | ≈0.9 mg cm⁻² | CCTO 0.2 mg cm⁻² ÷ (4/18) |
| 치밀층이면 두께 | ≈5.6 µm | 위 밀도로 평균 1.62 g cm⁻³ — 실측 증분 3 µm (`Fig. S34`, 눈금 1 µm) 와 같은 차수 · 나머지는 양극 공극 침투 또는 측정 분해능 |
| 유효 유전율 상승 | **≈ +23 %** (기지 대비) | Maxwell-Garnett · 구형 · 비연결 · ε_CCTO ≫ ε_기지 극한 ⇒ ε_eff/ε_m ≈ (1+2f)/(1−f), f ≈ 0.07 — **CCTO 의 ε 가 10⁴ 든 10⁵ 든 결과가 같다** |
| 유전 이완 시간 τ = ε/σ | ≈1–4 ns (ε 10–40 ε₀) · ε 를 10⁴ ε₀ 로 잡아도 ≈1 µs | 겔 σ ~ 1 mS cm⁻¹ (논문이 말하는 차수) |
| 1 C 전류밀도 | 0.26–0.68 mA cm⁻² | 1 C = 170 mAh g⁻¹ · 로딩 1.5–4 mg cm⁻² |

---

## 5. 결과 — 섹션별 상세 (그림 실독 포함)

### 5.1 문제 정의 — ACIPO (`Fig. 1`, `Fig. S22`) ★
- `Fig. 1a,b` 는 만화다: 왼쪽 — LPSC-PTFE 와 양극이 붉은 띠로 맞닿고 e⁻ 화살표가 LPSC 에서 양극으로 → *Interfacial decomposition · Electrolyte oxidation · Capacity fading · Safety risk*. 오른쪽 — 가운데 **반투명 판 (interfacial film)** 이 끼고 e⁻ 가 양극 안에서 되돌아감 → *Stable interface · Suppress ACIPO · High voltage stability · Excellent performance*.
- **`Fig. 1c` (본 그림)** — NCM811/LPSC-PTFE/Li (본문: **LiNbO₃ 코팅** NCM811). **충전 곡선만** 있다 (캡션은 *"charge and discharge"*). 시작 ≈2.15–2.2 V 에서 살짝 꺼졌다가 천천히 올라 180 mAh g⁻¹ 에서도 ≈2.6 V (figure-read). 삽도: ≈700 mAh g⁻¹ 에서 ≈3.45–3.5 V 에 닿은 뒤 1250 mAh g⁻¹ 까지 그 전위에서 잡음 섞인 평탄. 즉 **NCM811 의 탈리튬 전위 (≳3.6–3.7 V) 에 한 번도 못 간다**. 판 안 글씨 *"Wihtout Interfacial Film"* (오식).
- **`Fig. 1d`** — NCM811/PLIC/Li: ≈3.67 V 에서 ≈3.85 V 로 뛰고 완만히 올라 **≈150–155 mAh g⁻¹ 에서 4.4 V** (figure-read). 정상 충전.
- **`Fig. S22` (손 크롭 · 본 그림)** — LFP/LPSC-PTFE/Li: 2.66 V 에서 수직 상승 → 3.28 V → 완만히 3.45 V (≈90 mAh g⁻¹) → **≈3.45–3.47 V 평탄이 ≈720 mAh g⁻¹ 까지** (figure-read). ⚠ **이 평탄 전위는 LFP 자신의 충전 평탄 전위**다 — 기생 산화 · 연성 단락 · 셔틀을 이 곡선 하나로는 가를 수 없다 (§6 · §10-⑤).
- 저자: *"severe ACIPO is consistently observed at voltages as low as 3.5 V"* — 원인은 *"direct contact between LPSC/PTFE and cathode components (active materials and conductive carbon), which triggers parasitic oxidative reactions … as predicted by the thermodynamic instability analysis"*. **산물 분석 · 셀 분해 · OCV 유지 · 단락 진단은 없다.**

### 5.2 건식 LPSC-PTFE 막 (`Fig. S1`–`Fig. S21`)
§3a 표 그대로. 저자 서술: 볼밀이 *"induces PTFE fibrillation, which forms a continuous fibrous network that mechanically interlocks LPSC particles"* · 막은 *"remarkable mechanical flexibility"* (`Fig. S8` 사진) · *"reliable production … ~55 µm"*. **σ 가 분말 5.5 → 막 1.39 mS cm⁻¹ 로 75 % 떨어진다** (PTFE 1 wt% · 볼밀 · 기공의 몫을 가르지 않는다). **`Fig. S13` (본 그림)**: Nyquist 는 차단전극 직선만 · 고주파 절편 30/40/50/60 °C ≈11 / 7.7 / 5.2 / 3.5 Ω (figure-read) · σ 1.37 → 4.73 · ln σ 직선 0.35 eV. **`Fig. S14` (손 크롭 · 본 그림)**: 31 nA → ≈2.7–3 nA, 3600 s 에서도 내려가는 중.
⚠ **`Fig. S19` 캡션**에 *"Li/CPEs/Li"* · *"Li/FAEIS/Li symmetric cell and partial magnified views at 300–310 h"* · **`Fig. S15`** 에 *"Li/CMEFI/Li"* · **`Fig. S18`** 에 *"Li/CPE/Li"* — 이 논문에 없는 계 이름 (다른 원고의 복붙 흔적).

### 5.3 LSV 창 (`Fig. S23`, `Fig. S39`) ★ — 우리 ESW 축과 정의가 다르다
- **`Fig. S23` (본 그림 + 벡터 판독)**: LPSC-PTFE · SS‖막‖Li · 0–6 V · 5 mV s⁻¹. ≈1.1 V · ≈2.1 V 에 작은 혹, ≈3.3 V 부터 상승, ≈4.6 V 혹 · ≈5.6 V 큰 봉우리 (figure-read). 삽도 (2–4 V) 의 0.1 mA 점선과 곡선이 만나는 곳: **PDF 경로 좌표로 3.876 V** (본도 곡선 3.925 V) — 그런데 라벨은 **3.69 V**. 3.69 V 에서 전류는 ≈0.06 mA (우리 판독: 0.05 mA 교차 3.62 V).
- **`Fig. S39` (벡터 판독만 · 이미지는 안 봄)**: PLI 0.1 mA 교차 **4.584 V** (라벨 4.57) · PLIC **4.623 V** (라벨 4.62) — 이쪽은 라벨이 기준과 맞는다.
- ⇒ 같은 기준이면 LPSC-PTFE → PLIC 개선폭은 **≈0.74 V** 이지 본문의 *"nearly 1 V higher"* 가 아니다 (우리 산수).
- ⚠ **이 '창' 은 무엇의 창인가**: PLI/PLIC 측정은 **SS 위 겔막**의 산화 개시다 — LPSC 의 산화 한계가 아니다. 탄소 없는 차단 전극 · 5 mV s⁻¹ 빠른 주사라 **동역학적 overshoot** 계열의 값이다 (`comparison_vs_ours.md` §B① 의 여러 행과 같은 부류). 중간층은 LPSC 의 onset 을 옮긴 것이 아니라 **LPSC 가 고전위 전극에 닿는 일을 없앴다** (§7a).

### 5.4 CCTO 계산 (`Fig. 2a–e`, `Fig. S26`) — 계산이 주장을 받치나
- **`Fig. 2a` (본 그림)**: PDOS, 위 β · 아래 α, x 축 = E − E_αHOCO (−7–6 eV). 범례 TDOS · OPDOS · O 2p · Ca 3d · Cu 3d · Ti 3d. **α 와 β 가 거울상이 아니다** — 비점유 쪽 Cu 3d 봉우리 위치 · 세기가 다르고, **β HOCO 점선이 ≈ −0.3 eV** 에 따로 있다 (figure-read). 보상된 반강자성이면 총 DOS 의 α · β 가 같아야 한다 (§10-⑧a). 0–0.5 eV 근처에 DOS 꼬리가 붙어 있어 DOS 로는 갭을 읽기 어렵다 (Γ-only + 넓힘).
- **`Fig. 2b`**: bcc 경로 Γ–H–N–Γ–P–H|P–N (원시셀 사용과 일치). 비점유 첫 묶음 ≈ +1.2–1.9 eV 는 거의 β (파랑) — 본문의 '상부 Hubbard 띠' 로 보이는 평평한 띠. ⚠ 본문은 *"upper Hubbard band … clearly visible at 1.2 eV **below** the Fermi level"* — 상부 Hubbard 띠는 비점유 띠라 **Fermi 준위 위** 여야 한다 (그림도 위에 있다).
- **`Fig. 2c,d`**: ELF 3D 등치면 (정육면체 상자 · 고리 모양 등치면) · 2D 단면 (캡션 '(101) 면' · 축 0–≈15 × 0–≈12.5 Bohr). 양이온 자리 주위의 붉은 고리 = 반심 (semicore) 껍질 신호로 보인다 (GTH 반심 가성퍼텐셜에서 흔하다 · 우리 해석). 본문: *"Cu atoms have the highest electron density"* — ELF 는 전자 밀도가 아니다.
- **`Fig. S26` (본 그림)**: 두 2D ELF 단면 (캡션 '(001) 면', 각 ≈ −2.3–9.6 Bohr ≈ 6.3 Å 폭 — 원시셀 벡터 길이 쪽). 본문: *"ELF mapping (Fig. S26) demonstrates that **grain boundary** regions are enriched in oxygen"* — **그림은 결정 벌크의 주기 단면이다. 입계가 없다.**
- **`Fig. 2e`**: CCTO 조각 위 TFSI⁻ (F 쪽이 내려다봄) · **BE −4.19 eV**. 이 결합에너지를 **어떤 모델 (주기 슬랩 / 클러스터) · 어떤 코드 · 전하 처리로 냈는지 SI 에 없다.** `Fig. S42` 의 CCTO 조각은 원자 색 구성이 다른 **비주기 클러스터**로 보인다 (본 그림).
- 저자 서사: **Mott-Hubbard 절연 입자 + 절연 입계 = 직렬 미세 축전기 → 거대 ε (IBLC)** · 그 절연성이 *"electronically isolate LPSC-PTFE"*. ⚠ 통상 IBLC 그림은 **반도체 입자 + 절연 입계** (전도도 대비가 있어야 Maxwell–Wagner 분극이 생긴다 — 일반 지식 · 이 digest 에서 원전 확인 안 함). '입자도 절연' 이면 그 기전이 서지 않는다 — 저자 서사 안의 모순.

### 5.5 이온성 액체 고르기 (`Fig. 2f`, `Table S1`, `Table S2`, `Fig. S40`)
- **`Fig. 2f` · `Table S1`**: 18 양이온의 기체상 HOMO/LUMO (B3LYP) — imidazolium 류 gap 5.2–6.8 eV · 4차 암모늄 · pyrrolidinium · piperidinium 류 9.0–10.1 eV. 본문: 네 후보 *"with gaps in the range of 9.5–10 eV"* (⚠ Pyr₁₂ 는 10.12) → 가격 (`Table S2`: Pyr₁₃ 89.98 · PP₁₃ 442.9 · TPM 571.9 · Pyr₁₂ 589.9 ¥/5 g) → **Pyr₁₃⁺ 선택**, *"large energy gap (9.6 eV)"* (⚠ `Table S1` 은 **9.788545**). `Table S2` 의 음이온 이름은 *"bis(fluoromethanesulfonyl)imide"* — TFSI 가 아니다 (이름 오기 또는 다른 염 가격).
- **`Fig. S40` (본 그림)**: PAN −9.29/−0.85 · LiTFSI −8.76/−1.33 · **TFSI⁻ −4.07/+4.20** · Pyr₁₃⁺ −13.13/−3.34 · PTFE −9.43/−1.23 eV. SI 본문은 *"Pyr₁₃⁺ has the lowest HOMO … significantly lower than PAN, LiTFSI, PTFE"* 라며 **TFSI⁻ 의 −4.07 eV 를 비교에서 뺐다**. 같은 논리라면 가장 먼저 산화될 것은 TFSI⁻ 다. 그리고 Pyr₁₃TFSI 는 **PLI · PLIC 둘 다 (그리고 양극에도)** 있어서 PLI ↔ PLIC 차이를 설명할 수 없다 (§10-⑧h).

### 5.6 중간층 구조 (`Fig. 3a–e`, `Fig. S28`–`Fig. S35`)
- **`Fig. 3a,b` AFM**: 500 nm 막대 · 높이 ±150 nm · PLI 는 계단 · 골이 크고 PLIC 는 매끈 (정성 · Ra/Rq 수치 없음).
- **`Fig. 3c,d` 단면 FESEM** (100 µm 막대): 수십 µm 두께의 띠 (figure-read — 3 µm 층은 이 배율에서 안 보인다). 본문은 이 그림으로 *"both interlayers partially infiltrate into the porous cathode structure, forming a gradient interphase"* 를 말한다 — 이 배율로는 판단 불가.
- **`Fig. S33` (본 그림)**: PLIC 양극 단면 EDS (50 µm). C · N · O · F · **S (조밀)** · Al (아래 띠 = 집전체) · **Fe (희박!)** · Cu · Ca · Ti (희박한 점). LFP 의 주원소인 Fe 가 듬성하고 P 지도는 없다. Cu/Ca/Ti 의 듬성한 점으로 *"homogeneously distributed throughout the entire LFP cathode matrix, extending from the surface to the bulk"* 를 말한다 — **정량 선분석 없이 낮은 계수의 점 지도로는 '전 두께 침투' 와 '배경 계수' 를 가를 수 없다.** 게다가 전 두께에 퍼졌다면 '3 µm 위층' 과 맞지 않는다.
- **`Fig. S34` (본 그림)**: 디지털 마이크로미터 LFP **0.051 mm** → LFP-PLIC **0.054 mm** — '3 µm' 은 눈금 1 µm 기기의 단일 판독 두 개의 차이다.
- **`Fig. S31` (본 그림)**: CCTO 분말 — 100/50/20 µm 막대. 각진 입자 **≈1–10 µm, 큰 것 ≈20 µm 이상** (20 µm 막대 기준 figure-read). EDS 에서 **Cu 가 Ti 와 안 겹치는 뭉침**이 보인다 (CuO 같은 2차상 가능성 — 추정 · 논문 언급 없음). ⚠ **3 µm 층 안에 1–20 µm 입자** — 기하가 안 맞는다. 분쇄 · 분산 단계도 없다.
- **`Fig. 3e` XRD**: PLI 는 17–20° PAN 넓은 혹 · PLIC 는 혹이 약하고 CCTO 날카로운 선 (≈34 · 49 · 62 · 72°, figure-read). 저자: PAN 결정성 감소 → 전도도 증가.
- `Fig. S28`–`Fig. S30` · `Fig. S32` · `Fig. S35` 는 안 봤다 (SI 서술: PLI 는 기공 많고 PLIC 는 치밀 · 원소 균질).

### 5.7 중간층 전기화학 (`Fig. 3f–h`, `Fig. S36`–`Fig. S39`) ★
- **σ**: §3b. **`Fig. S37` 은 벡터라 표식 좌표를 직접 읽었다** — 30 °C 에서 PLIC **1.357** · PLI **1.284** mS cm⁻¹ (60 °C 3.973 · 3.569). 본문 · `Fig. 3f` 라벨 · `Table S3` 의 1.44 · 1.40 과 다르고, LPSC-PTFE 1.39 보다 **둘 다 낮다**. 본문 *"Notably, both composites outperform the pristine LPSC-PTFE electrolyte"* 는 자기 그림과 어긋난다.
- **`Fig. S36` (본 그림)**: 30 °C 고주파 절편 PLIC ≈18 Ω · PLI ≈19.5 Ω (figure-read) — LPSC-PTFE 단독 ≈11 Ω (`Fig. S13`) 보다 크다. 겔층이 직렬로 저항을 더한 것이 정상이고, 같은 L/S 라면 σ 는 1.39 × 11/18 × (1.05–1.11) ≈ **0.9 mS cm⁻¹** 쪽이어야 한다 (우리 산수 · 증분 두께 3–6 µm 가정).
- **σ_e (`Fig. S38`, 손 크롭 · 본 그림)**: PLI 40 nA → ≈0.7 nA · PLIC 14.5 nA → ≈0.15 nA. PLIC 의 Is 0.15 nA 는 nA 급 전위기의 바닥 근처다.
- **부유시험 (`Fig. 3g`)**: NCM811/PLI·PLIC/Li · 4.1 → 4.7 V · 10 h 씩. 계단마다 충전 스파이크 (≈140–440 µA). 저자: *"PLI starts to show a significant increase in leakage current at 4.6 V, while PLIC maintains stable operation up to 4.7 V"* — 그림의 PLIC 도 **4.7 V 에서 ≈45 µA** 로 한 자릿수 뛴다 (figure-read · 그림 라벨도 PLIC 의 개시를 4.7 V 에 찍는다). 그리고 *"We **hypothesize** that this phenomenon arises from electric field homogenization of CCTO"*.
- **CV (`Fig. 3h`)**: 도금 개시 과전압 PLIC 50.8 · PLI 51.6 mV — LPSC-PTFE 자체 (`Fig. S16` 라벨 50.5 mV) 와 같다. *"extremely low energy barrier"* 는 0.8 mV 차이에 기댄다. 본문은 LPSC-PTFE 비교 근거를 **`Fig. S15`** 로 인용 (S15 는 t_Li⁺ 그림 — 오인용).

### 5.8 Raman 용매화 (`Fig. 3i`, `Fig. S41`)
PLIC 자유 TFSI⁻ **8.5 %** (PLI 11.8) · '배위 TFSI⁻' 91.5 % (PLI 88.1). 저자: *"CCTO can competitively participate in TFSI⁻ coordination, weakening the Li⁺–TFSI⁻ interaction … leading to more complete dissociation of lithium salts"*. ⚠ 745 cm⁻¹ 대역 하나에 **CIP · AGG 와 CCTO-TFSI⁻ 가 같이** 들어 있어 *Li⁺ 와 더 짝지은 TFSI⁻* 와 *CCTO 에 붙은 TFSI⁻* 를 못 가른다. 자유 TFSI⁻ 가 **줄었다**는 관측은 문자 그대로 읽으면 **해리 감소** 쪽이다. 차이는 −3.3 / +1.4 / +2.0 %p · 스펙트럼 하나 · 데이터 산포 큼 (본 그림).

### 5.9 MD (`Fig. 4`, `Fig. S42`, `Fig. S43`) ★
- **`Fig. 4a–c` RDF/CN (본 그림)**: Li–N(PAN) 첫 봉우리 ≈0.22 nm (g ≈10.6 PLI · ≈8.8 PLIC) · Li–O(TFSI⁻) ≈0.20–0.21 nm (g ≈43 · ≈36) · Li–O(CCTO) ≈0.20 nm (g ≈16) 뒤로 결정 CCTO 의 날카로운 혹 (0.43 · 0.55 nm). CN 점선 계단이 §3b 값과 맞는다.
- **`Fig. 4d`**: 막대 0.74/0.85 · 3.47/4.33 · 1.29. 산수 확인 — 4.33/5.18 = 83.6 % ✓ · 3.47/4.33 = −19.9 % ✓ · 0.74 + 3.47 + 1.29 = 5.50 ✓.
- **`Fig. 4e` MSD (본 그림)**: y 축 *"Mean square displament (nm²)"* 0–0.03 · x 축 *"Simiulation time (ns)"* 0–50. PLIC: t = 0 에서 ≈0.0055 → ≈8 ns 까지 평평 → 직선 상승 → ≈40–48 ns 에 **≈0.022 nm² 고원 · 끝에서 ≈0.020 으로 하강**. PLI: ≈0.006 → 30 ns ≈0.0075 → 50 ns ≈0.012 (끝에서 상승). **총 MSD ≈2.2 Å² (RMS ≈1.5 Å) · PLI ≈1.2 Å²** — Li–O 첫 배위 거리 (≈2 Å) 보다 작은 변위다. D 는 맞춤 창에 따라 몇 배씩 바뀌고 그 창은 미기재. 7.58/1.18 = 6.4 (*"6–7 times"*) ✓.
- **홉 수 검산** (규약 · ν₀ 10¹³ s⁻¹ **가정** · T = 298 K · t = 50 ns): 실험 겉보기 Ea ≈0.30 eV 를 넣으면 Γ ≈ 8×10⁷ s⁻¹ → **N = Γ·t ≈ 4 도약** — 50 ns 창에서 Li 하나가 몇 번 못 뛴다. MSD 가 확산 영역에 못 들어간 것과 차수가 맞는다 (이 D 는 확산계수로 정의되지 않는다).
- **`Fig. 4f,g`**: 상자 스냅숏 (PLIC 오른쪽 아래에 CCTO 로 보이는 뭉침). **`Fig. 4h`**: 기전 만화 (PLI = 'Slow Li⁺' · PLIC = 'Fast Li⁺', CCTO 를 nm 크기 덩이로 그림).
- **`Fig. S42` (본 그림)**: Li⁺ 결합 TFSI⁻ −6.26 · PAN −2.96 (사슬 조각 위 Li) · CCTO −4.26 eV (비주기 클러스터 위 Li). 저자: *"follow the same trend as the coordination numbers"*.
- **`Fig. S43`** (안 봄): ESP — TFSI⁻ O 최저 −0.2 a.u. · Pyr₁₃⁺ 전부 양 → *"TFSI⁻ anions are stronger electron donors than PAN"*.

### 5.10 셀 성능 (`Fig. 5`, `Fig. S44`–`Fig. S48`)
- **`Fig. 5a` (본 그림 + 픽셀 판독)**: x 눈금 0–1000 · 오른쪽 축 = 1100 사이클 위치. **PLIC 마지막 표식 ≈1055–1060 사이클** — '1100th 89.2 %' 라벨보다 ≈40 사이클 짧다. 첫 몇 사이클 ≈115–117 mAh g⁻¹ (figure-read) 인데 기준 112.6 이 어느 사이클인지 미기재. PLI 는 ≈470 에서 ≈92 → **≈480–495 에서 82–84 로 급락하며 끝** — 단락 같은 급사로 보이지만 논문은 끝 모양을 다루지 않는다.
- **`Fig. 5b–d` DRT**: §3c. 본문 *"The PLI exhibits a significantly enhanced CEI relaxation peak **after cycling**"* — 데이터는 **첫 충방전**뿐이다 (캡션 *"during the first charge-discharge process"*). 범례 *"Disharge"* 오식.
- **`Fig. 5e` 율속 (본 그림 + 픽셀 판독)**: PLIC 0.5 C 표식 **≈143–145** (본문 148.3) · 1 C ≈110–113 (본문 115.2) · PLI 0.5 C ≈114–118 (본문 111.4) · 1 C ≈100–104 (본문 99.7). 본문 숫자가 그림보다 PLIC 쪽은 높고 PLI 쪽은 낮다 — 차이 2–5 mAh g⁻¹ (표식 반지름 ≈1.7 mAh g⁻¹). PLI 회복 *"169.9 mAh g⁻¹ … with more pronounced capacity decay"* — 시작 169.7 보다 높은데 '더 큰 감소' 라는 서술은 안 맞는다.
- **`Fig. S46` (본 그림)**: NCM811 0.5 C · PLIC 첫 점 ≈135 → 2–3 번째 ≈142 → ≈50 사이클에 ≈157 최대 → 150 사이클 114.2. **최대 대비 유지율 ≈73 %** (우리 산수) · PLI 는 첫 점 111.3 이 기준 · ≈72 사이클에 계단 하락 (88 → 71) · 80 사이클 68.0. 두 셀의 **기준점이 다르다**.
- `Fig. S44` · `Fig. S45` · `Fig. S47` · `Fig. S48` (전압 곡선) 안 봤다.

### 5.11 사후 분석 — 형상 · XPS (`Fig. 6`, `Fig. S49`–`Fig. S54`) ★
- **`Fig. 6a,b` AFM** (1 µm 막대, ±150 nm): PLI 거칠고 PLIC 매끈 (정성).
- **`Fig. 6c,d` SEM + 삽도 사진**: PLI 면은 수십 µm 균열 · 덩이 · 박리 · PLIC 면은 균일한 다공 질감. 삽도 = **LPSC-PTFE 의 양극 쪽 면**: PLI 쪽은 검은 · 은회색 거친 면, **PLIC 쪽은 양극 지름 크기의 노랗-갈색 원판**이 남아 있다 (figure-read · 색). 저자는 *"remains flat and smooth without obvious corrosion traces"* — 그 색이 PLIC 층의 전사인지 변색인지 논문이 가르지 않는다.
- **`Fig. 6e–g` · `Fig. S53` · `Fig. S54` (본 그림)**: §3d. 핵심 셋 — ① **분석면에서 P · Cl (LPSC) 도 Ti · Ca · Cu (CCTO) 도 안 잡힌다** ⇒ XPS (깊이 ~10 nm, 일반 지식) 가 본 것은 **3 µm 겔 중간층의 LPSC 쪽 표면** 이다 — LFP 입자 위 CEI 가 아니다. S 7.6–7.7 % 는 TFSI 의 S 로 설명된다 (S 2p = SO₂–CF₃). ② 'Li₃N' 성분은 그림 라벨이 **'LiN₃'** (아자이드) 이고 위치 ≈400.7 eV — Li₃N 의 통상 N 1s (≈396–397 eV, 일반 문헌값 · 원전 확인 안 함) 와 멀다. PAN 니트릴 N (≈399.5–400 eV 부근, 일반 지식) 과 겹칠 수 있다. ③ 본문이 열거한 무기 CEI 성분 중 **Li₂O 는 O 1s 에 성분이 없다** (한 성분 'C=O') · Li 1s 는 잡음 위 맞춤 · 'LiF₃' 라벨 (존재하지 않는 화합물).
- 원소 파이 (`Fig. 6g`) 는 C · F · Li · N · O · S 로만 100 % — 측정한 P · Cl · Ti · Ca · Cu 는 (잡음이라) 빠졌다. **Li 총량은 6.5 → 5.1 % 로 줄었는데** 'LiF + Li₃N' 은 늘었다고 한다. N 증가 (7.6 → 10.9 %) 는 N 1s 에서 Pyr₁₃⁺ 성분이 커진 것과 맞는다 — 표면에 IL 양이온이 더 많다.
- `Fig. S49` (사후 SEM) · `Fig. S50`–`Fig. S51` (사후 EDS — PLI 가 LFP 부피변화로 '압출') · `Fig. S52` (순수 Pyr₁₃TFSI XPS 기준) 은 안 봤다.

---

## 6. 메커니즘 종합 — 저자 그림 (`Fig. 6h`) 과 대안 해석

**저자 그림** (`Fig. 6h`): 왼쪽 — 중간층 없음: LPSC 가 양극 · SP 와 맞닿아 e⁻ 가 넘어가고 'Overcharge'. 가운데 — PLIC: 양극 입자를 감싼 겔 + 분홍 CEI · e⁻ 가 막힌다 (*"Colossal-Dielectric & Electrical Insulation"*). 오른쪽 — PLI: 'Swell' · 'Crack' · *"Unstable Electrical Insulation"*. 결론 문단의 세 줄: ① 거대 유전 → 계면 전기장 균질화 · 국부 전류 열점 제거 ② CCTO 의 전자 절연 → 누설 경로 차단 ③ (*"most importantly"*) LiF–Li₃N 풍부 CEI 유도.

**우리가 읽은 증거의 무게**:
1. **격리 (①의 '물리적 분리' 부분)** 는 실재한다 — 중간층이 있으면 ACIPO 가 없다. 그런데 **이것은 겔 (PAN + LiTFSI + IL) 이 하는 일**이고 CCTO 는 거기에 σ_e 3×↓ · 창 +0.05 V 를 더한다.
2. **'거대 유전 → 전기장 균질화'** 는 사슬이 비어 있다. (a) ε 측정 없음 (b) 7 vol% 분산이면 유효 ε 는 기지의 ≈1.2 배 (유효매질 산수 §4g — CCTO 의 ε 크기와 무관) (c) 정상상태 이온 전도 매질에서 거시 전기장은 E = J/σ 로 **σ 가 정한다** · ε 는 τ = ε/σ (ns–µs) 동안의 과도 응답만 바꾼다 (d) 저자도 'hypothesize' · 'may'. ⇒ 지금 상태로는 **같은 부피분율의 아무 절연 산화물 충전재 (Al₂O₃ · SiO₂ · TiO₂) 와 구별되는 주장이 아니다** — 저유전 충전재 대조군이 없다 (§10-①).
3. **TFSI⁻ 고정 · 해리 증가** — Raman 은 방향이 모호하고 (자유 TFSI⁻ 감소), DFT 결합에너지는 진공 · 단일 배치 · 하전종 · 클러스터 값, MD 는 CCTO 를 nm 덩이로 넣어 표면적을 과장한다 (`Fig. S31` 의 µm 입자 대비).
4. **LiF/Li₃N CEI** — 분석면이 겔 표면이고 차이가 작으며 Li₃N 귀속이 흔들린다.
5. **기계적 보강** — 정성 형상뿐.

**논문이 가르지 않은 ACIPO 의 대안 해석** (추정 · 우리 쪽 정리): ⓐ **LPSC 지속 산화** (저자) — 산물 · 기체 분석 없음 ⓑ **연성 단락 (soft short)** — CCD 0.27 mA cm⁻² 막 · 3.45 V 평탄 = LFP 평형 전위 · NCM811 셀이 OCV 보다 낮은 2.2 V 에서 시작 ⓒ **IL 매개 셔틀** — 양극 10 wt% IL 과 Li 쪽 Li-IL 이 있는 셀에서 LPSC 산화 산물 (S · 폴리설파이드 계열) 이 녹아 오갈 수 있다 ⓓ **대조 셀 양극에 Li 염이 없다** — 중간층 용액 (LiTFSI 함유) 이 양극 공극에 스미면 양극 안 Li⁺ 경로 자체가 바뀐다 (교락). 진단 실험 (사후 OCV · 셀 분해 XPS · 기체 · 단락 저항) 이 하나라도 있었으면 갈렸다.

---

## 7. 우리 일과의 대조 ★★ (숫자를 섞지 않는다 — 방법 · 정의 수준)

> 규율: 문헌 수치는 소환값이고 우리 db 절대값과 같은 줄에 두지 않는다 (CLAUDE.md §litdb · 의뢰 조건). 우리 값은 원장 (`db/properties/canonical_registry.json` · `citation_hazards.json`) 에 있고 여기서는 **이름 · 정의 · 방법만** 부른다.

### 7a. comp1 (= Li₆PS₅Cl, 이 논문의 명목 조성)
- **겹치는 계산량이 사실상 없다.** 이 논문의 LPSC 계산은 CP2K PBE 기하 최적화 + AIMD 한 개뿐이다 — 띠틈 · 산화 창 · 탄성 · ICOHP · EOS 가 없다.
- **이온 수송**: 이 논문 = AIMD · NPT · 600 K **한 온도** · ≈3.8 ps · 궤적 1 · MSD 적합 ≈0.1–3.8 ps · D = 기울기 (1/6 누락 의심) · 무질서 (S/Cl 4a/4d · Li 48h) 처리 미기재. 우리 = MLIP-MD (UMA-s-1p1) · NVT Langevin · 평형 5 ps + 생산 200 ps · **MSD 창 2–50 ps 고정** · 3 온도 아레니우스 (CLAUDE.md §데이터 규율). ⇒ **보고량 정의가 다르다** (우리 창 기준이면 이 궤적은 창 아래 끝에도 겨우 닿는다). 수치 대조 안 함 — 우리 MLIP-MD 절대값은 원래 인용 금지이고, 이 논문 D 는 정의부터 흔들린다.
- **관측창 한 줄** (규약 `D-2026-10-05-md-observation-window` · ν₀ 10¹³ s⁻¹ **가정**): 600 K · 3.8 ps → Ea_max ≈ kT·ln(ν₀t) ≈ **0.19 eV** (Li 48 개 중 하나라도면 + kT ln 48 ≈ 0.39 eV) — 이 궤적이 보장하는 것은 그 아래 장벽의 사건뿐이다.
- **셀 정책**: 이 논문은 '기본 수렴 BFGS' · AIMD 는 NPT (셀이 움직인다). 우리 argyrodite 는 **고정셀 + EOS (조건부)** 가 기본 (CLAUDE.md) — 비교 축이 아니다.
- **산화 창**: 이 논문의 LSV 값 (LPSC-PTFE 라벨 3.69 / 우리 판독 ≈3.88 V · PLIC 4.62 V) 은 **5 mV s⁻¹ · 차단 전극 · 전류 문턱** 의 동역학 값이고, PLIC 의 값은 **겔막의 성질**이다. 우리 ESW 는 grand-potential **층① (S²⁻-limited onset)** — LPSC 자신의 열역학 개시다. 정의가 달라 같은 줄에 두지 않는다. ⭐ 이 논문은 **'LPSC 의 onset 은 그대로 두고 LPSC 가 고전위에 닿는 일을 없앴다'** 는 해법이라 우리 축① 과 모순도 확증도 아니다 — `comparison_vs_ours.md` §B 의 *"표면 개질로는 onset 이 안 움직인다"* 계열 (`[Deng26PS]`) 의 **전극 수준 판**이다.
- **띠틈 규약**: 이 논문은 LPSC 띠틈을 안 낸다. CCTO 는 **Γ-only DOS** 로 그렸다 — 우리 규약 (fixed-occ nscf 고유값만 · DOS 문턱 판독 금지) 에서는 쓰지 않는 판독 방식이다.

### 7b. CEI 트랙 (Nd 계면 · `db/properties/cei_figs/index.html` · 1저자 = 실험 쪽)
- **같은 문제, 다른 해법 부류.** CEI 트랙의 보고량은 0 K hull 위 (Nd 치환) LPSCl ‖ 양극 산화물 **접촉의 분해 산물 분포와 산물 띠틈**이다 ('분해 산물의 재분배'). 이 논문은 그 접촉을 **아예 없애는** 물리 격리 부류다. 이 논문에는 황화물 분해 산물 데이터가 **없다** (ACIPO 셀의 사후 분석 0 · 분석면에 P · Cl 미검출) ⇒ CEI 트랙의 산물 예측을 검증 · 반박할 수 없다.
- **이 논문의 'CEI' 는 우리 CEI 와 다른 물건이다** — TFSI · IL 유래 유기 표면 (−CF₃ · Pyr₁₃⁺ · SO₂–CF₃) 이고, 그것도 LFP 입자 위가 아니라 **겔 중간층의 LPSC 쪽 면**이다.
- **옮길 만한 것 하나 — 증거의 종류**: CEI 원장의 금지 서술 *"갭은 전도도가 아니다 — 캐리어 농도 · 이동도 · 결함 · 접촉 · 상 연결성을 모른 채 '샌다' 도 '막는다' 도 확정하지 않는다"* 와 정확히 같은 함정이 이 논문 §3.2 에 있다 (*"This Mott-Hubbard insulating property enables the colossal-dielectric interface to electronically isolate LPSC-PTFE"* — DFT 갭 하나로 격리를 말함). 반대로 이 논문이 **DC 분극으로 막의 σ_e 를 잰 것**은 맞는 종류의 증거다 (단 정규화 불일치 §10-④ · CCTO 몫은 3×). ⇒ 우리 CEI 서술에서 *'전자 절연 산물'* 을 말할 때 필요한 것은 산물 갭 + **이런 종류의 σ_e 측정**이라는 외부 사례로만 쓴다. (CEI 원고 같이 읽기 규칙: 한국어 해석 + 우리 계산 비교만.)

### 7c. cascade 축 ① NCM 계면 (`db/properties/cascade_axes_bundle_closed_2026_11_05.json` — 닫힘 · 허용/금지 서술 그대로)
- 축 ① 의 보고량 = MP 닫힌계 **의사이원 (pseudo-binary) 반응 경향** (도핑 LPSCl ↔ LiNiO₂ full/half 대리) 과 **산물의 전자 등급** (metallic / wide …) — **스크리닝 규모의 상대값 · 등급**이다.
- 이 논문은 도핑이 없고, ACIPO 셀의 산물을 하나도 확인하지 않았다 ⇒ **축 ① 을 이 논문으로 검증하지 않는다.** `Fig. 1c` (LNO 코팅 NCM811 + LPSC 직접 접촉 → 끝없는 충전) 는 축 ① 이 걸러 내려는 '접촉 분해 · 자기부동태 실패' 의 **정성 장면**일 뿐이다.
- 닫힘 기록의 금지 서술 (선택 집합을 '좋은 도펀트' 로 · 순위 · MP 갭 절대값) 은 이 digest 어디에도 쓰지 않았다.

### 7d. 건식 공정 · PTFE — litdb 건식 digest 와 우리 SDCP/PTFE (C-12)
| litdb digest | 그쪽이 다루는 것 | 이 논문과의 관계 |
|---|---|---|
| `lee2025_corolling_dryprocess_lpscl_ptfe` | 건식 LPSCl-PTFE 박막 SE (co-rolling) · 저압 작동 | **가장 가까운 짝** — 이 논문의 SE 막과 같은 부류. 이 논문은 압연이 아니라 볼밀 + 열압 (방법) · 공정도는 압연 (`Fig. S25`) |
| `hippauf2019_dry_film_ptfe_sulfide_cathode_sheet` | 건식 **복합양극** 시트 (PTFE 0.1 wt%) | 대조: 이 논문은 양극을 **습식**으로 두고 SE 만 건식. 건식-습식 혼성의 짝맞춤 문제를 중간층으로 푼 것 |
| `frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure` | 볼밀 강도 (DEM E_col · f_col · E_m) ↔ 미세구조 | 이 논문의 '고에너지 볼밀 피브릴화 완료까지' 는 **조건 0** — σ 5.5 → 1.39 mS cm⁻¹ 하락의 공정 몫을 알 수 없다. 우리 DEM 축에 넣을 공정창 없음 |
| `kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode` · `matthews2024_ptfe_nanofibril_network` | PTFE 피브릴화의 FEM · 형상 | 이 논문의 피브릴 SEM (`Fig. S6`) 은 안 봤다 · 피브릴 정량 없음 |
| `kang2025_bollard_anchored_binder_dry_electrode` | 건식 전극 바인더 고정 설계 | 바인더 설계 축 — 이 논문은 바인더를 건드리지 않는다 (Q1) |
| `choi2026_bzox_dry_zro2x_nmc_shell_coating` (이 논문 ref [20]) | **양극 입자 하나하나**에 건식 ZrO₂₋ₓ 껍질 (전하 전도성) | **대조의 축**: 입자 코팅 (Choi · 건식 기계 코팅 · 전도성 산화물) ↔ 전극 표면 한 겹 이온겔 막 (이 논문 · 용액 적하 · 절연 충전재) |
| `schmitt2026_chemomech_stability_dry_cathode_separator_sheets` (같은 날 litdb 에 들어온 편) | PTFE 건식 양극 · 분리막 시트 vs 냉간압축 펠릿 · **분리막 PTFE 는 저전위에서 환원 (LiF + C) · 양극 쪽 PTFE 는 분해 안 보임** (그 digest 정리) | 이 논문의 동기 문장 *'PTFE 가 충전 중 전자 주입으로 탈불소'* 를 **양극 쪽 문제**로 놓은 것과 방향이 반대인 실측 정리 — 건식 분리막 PTFE 의 위험은 음극 쪽 (환원) 이다 (§10-⑱) |
| `liu2025_dry_processing_high_energy_li_batteries_review` · `mun2025_dry_electrode_technology_assb_review` | 건식 공정 총설 | 맥락 |

- **우리 SDCP/PTFE C-12** (`db/properties/sdcp_c12_closed_2026_09_30.json` · 값 citable false — 숫자를 두지 않는다): 우리 양은 **UMA 로 고른 고정 기하 위 PBE+U+D3 단일점의 '흡착 전자에너지 차'** 이고, 닫힘 기록은 그것을 *'결합 세기 · binding energy'* 로 부르기와 *PTFE 고분자 · 피복률 · 계면 저항으로 확장* 을 금지한다. ⭐ **이 논문의 DFT '결합에너지' 는 같은 종류의 양**이다 (진공 · 단일 배치 · 전자에너지 차) — 오히려 더 비어 있다 (BSSE · 용매 · 구조 공개 · 표면 정의 없음). 그런데 논문은 그것으로 *"anchoring"* · *"strong interfacial interaction"* · 산화 억제 · 수송을 말한다 — **우리가 스스로 금지한 해석의 외부 사례**로 쓸 수 있다.
- **PTFE 와 양극**: 이 논문은 PTFE 분해를 동기로 들지만 **PTFE 의 몫을 따로 시험하지 않았다** (PTFE 없는 LPSC 펠릿 대조 없음) · 그 서술은 환원 반응을 양극 쪽 문제로 적었다 (§10-⑱). 우리 C-12 (PTFE 조각의 LiNiO₂ 위 흡착) 에 보탤 데이터는 없다.

### 7e. 유전체 · 강유전체 코팅 선행 — litdb 현황
- **1차 digest 없음.** BaTiO₃ 나노점 양극 코팅 · 유전 충전재 복합전해질 (이 논문 ref [23]) 같은 원저가 litdb 에 **없다**.
- **2차 언급만 있다**: `liang2026_interface_bottleneck_solid_state_batteries` (리뷰 ref [75] — LLZO 입계에 강유전 BaTiO₃ · 내부 전기장으로 덴드라이트 억제) · `gandla2026_layered_cathode_degradation_diagnostics_review` (DPC-STEM 으로 LCO/LPSCl 계면 전하 축적을 보고 BaTiO₃ 로 억제 — 그 리뷰는 *"공간전하층은 부차적"* 으로 정리).
- **공간전하층 현상 원전**: `haruyama2014_space_charge_layer_oxide_cathode_sulfide_se` (정성 · 정량 없음). ⚠ 이 논문은 공간전하층을 **한 번도 말하지 않는다** — 유전체의 고전적 논리 (산화물 양극/황화물 계면의 SCL 을 유전층으로 줄인다) 와 다른 틀 (분산 충전재 · 전기장 균질화) 을 쓴다.

### 7f. 항목별 대조표
| 항목 | 이 논문 | 우리 | 차이 / 판정 |
|---|---|---|---|
| LPSC 모델 · 무질서 | CP2K '원시셀 2×2×2' (상자는 정육면체로 그려짐 `Fig. S5a`) · 무질서 미기재 | comp1 — 원장의 셀 · 배열 규약 | 비교 안 함 |
| 이완 | BFGS 기본 수렴 · AIMD NPT | 고정셀 + EOS (조건부) | 정책 다름 |
| 이온 수송 | AIMD 600 K · 3.8 ps · D = 기울기 | MLIP-MD · 200 ps · MSD 2–50 ps · 3 온도 | 보고량 정의 다름 → **수치 대조 금지** |
| 산화 창 | LSV 5 mV s⁻¹ · 100 µA · 겔막 | grand-potential 층① | 정의 다름 · 중간층은 onset 을 안 옮긴다 |
| 띠틈 | CCTO PBE+U (U 미기재) · Γ-only DOS | fixed-occ nscf 고유값 · DOS 판독 금지 | 대조 대상 없음 · 판독 방식이 우리 금지 방식 |
| 전자 차단 | DC 분극 σ_e (막) | 띠틈만 (σ_e 축 없음) | 그들의 측정 **종류**가 우리에게 없는 축 (`[Deng26PS]` 과 같은 지적) |
| 흡착/결합 | B3LYP-D3 기체상 · 단일 배치 · BSSE 없음 · −4 eV 급 | C-12: UMA 기하 위 PBE+U+D3 단일점 · citable false · 이름 규율 | **같은 종류의 양** · 우리 금지 해석을 그들이 한다 |
| 계면 반응 | 산물 분석 없음 | cascade 축 ① · CEI hull 산물 | 데이터 없음 |
| MD 규율 | 홉 수 · 관측창 · 맞춤 창 미기재 | 홉 수 · 관측창 규약 (`D-2026-09-27` · `D-2026-10-05`) | 우리 규약으로 다시 잰 결과 §5.9 · §7a |

---

## 8. DFT/계산 방법 ★ (SI 전문 + 그림에서 확인한 것)

- **분자 DFT**: 구조 = **Avogadro** · 기하 최적화 · 단일점 = **B3LYP** + **DFT-D3** (refs: Grimme 2010 D3 · **Grimme 2011 감쇠함수 논문** ⇒ D3(BJ) 로 읽힌다) · **def2-TZVP** + **def2/J** 보조기저 · **ORCA 6.0** · 고분자 중합도 **10** · E_bind = E(A/B) − E(A) − E(B) · **BSSE 보정 없음 · 용매 모델 없음 · 배치 탐색 서술 없음** · ESP = **Multiwfn** · 시각화 = **VMD**.
- **주기 DFT — LPSC**: **CP2K** (입력은 Multiwfn 이 생성) · **PBE** · **GTH** 가성퍼텐셜 · **DZVP-MOLOPT-SR-GTH** · 평면파 절단 **400 Ry** · BFGS · PBC · '기본 수렴 기준' · *"A 2×2×2 supercell was constructed from its primitive cell"* (원시셀이면 104 원자 · 정육면체 상자가 아니어야 하는데 `Fig. S5a` 는 정육면체 — 실제 셀 모호) · k 점 미기재 · **무질서 처리 미기재** · 분산 보정 미기재.
- **AIMD — LPSC**: 같은 설정 · **NPT** · **600 K** · **1.0 atm** · dt **1.0 fs** · 열浴 · 압浴 이름 없음 · 길이 **미기재 → `Fig. S5b` 로 ≈3.8 ps** · 궤적 1 · 온도 1 · D 보고 6.77×10⁻⁵ cm² s⁻¹ (그려진 적합선 기울기와 같은 값 · §10-③c).
- **주기 DFT — CCTO**: **DFT+U** (Anisimov 1991 · Dudarev 1998 인용) — **U 값 · 적용 궤도 미기재** · PBE · GTH · DZVP-MOLOPT-SR-GTH · 절단 **1000 Ry** · *"An antiferromagnetic state was imposed on the copper atoms in the **primitive cell**"* · 단일점 SCF **9×9×9 k** · 띠 경로 = **SeeK-path** (bcc 경로) · **PDOS · ELF = Γ 점 파동함수** (*"based on the Γ-point wave function"*) · 시각화 VMD · VESTA.
- **TFSI⁻–CCTO · Li⁺–CCTO 결합**: 모델 (슬랩/클러스터) · 코드 · 전하 처리 · 기판 크기 **전부 미기재** (`Fig. 2e` · `Fig. S42` 의 그림만).
- **고전 MD**: **GROMACS 2025.3** · 조성 = 실제 몰비 · 정육면체 PBC · 초기 = **packmol** · 역장 = **Sobtop** (2026.1.16) · 전하 = **RESP** (위 DFT · Multiwfn + Sobtop) · **CCTO = REPEAT 전하** · LJ · 실공간 정전 절단 **1.5 nm** · **PME** · 최급강하 EM (최대 step 0.01 nm) · **500 K 가열 · 유지 → 298.15 K 담금 · 1 bar · 평형 총 20 ns** · **NPT 생산 50 ns**. **미기재**: 시간 간격 · 열浴/압浴 · 상자 크기 · 분자 수 · Li 수 · MD 의 PAN 사슬 길이 · CCTO 덩이 크기 · 강체 여부 · 이온 전하 척도 (IL MD 에서 흔한 0.8 배 등) · MSD 맞춤 창 · 시드 수.
- **유전율 · 전기장**: 계산 **없음**. 유한요소 · 연속체 전기장 · 공간전하 모의 **없음**. ε ≈ 10⁴–10⁵ 는 인용 [23].
- **후처리 · 도구**: DOS/PDOS · 띠구조 · ELF (3D · 2D) · 결합에너지 · HOMO/LUMO · ESP · RDF/CN · MSD → D. 도구 = Multiwfn · VMD · VESTA · SeeK-path · Sobtop · packmol. 수치는 그림 라벨로만 보고 (원자료 · 구조 파일 공개 없음).

---

## 9. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1a,b | ACIPO 만화 · 중간층 개념도 (LPSC-PTFE ‖ Cathode, 가운데 반투명 판) | 발표용 개념 그림 정도 — 기전 근거 아님 |
| 1c | NCM811 (LNO 코팅)/LPSC-PTFE/Li 충전만: 시작 ≈2.2 V · 180 mAh g⁻¹ 에 ≈2.6 V · 삽도 ≈3.45–3.5 V 평탄 1250 mAh g⁻¹ 까지 (figure-read) | '직접 접촉 = 끝없는 충전' 의 장면. ⚠ NCM 탈리튬 전위에 못 감 · 원인 진단 없음 (§6) |
| 1d | NCM811/PLIC/Li 충전: ≈3.85 V → 4.4 V @≈150–155 mAh g⁻¹ (figure-read) | 정상 충전 대조. ⚠ PLI 곡선이 없어 CCTO 몫을 못 가른다 |
| 2a | CCTO PDOS (α/β · Ca/Cu/Ti 3d · O 2p) — α/β 비대칭 · β HOCO ≈ −0.3 eV (figure-read) | ⚠ 'AFM' 과 어긋남 · Γ-only DOS — 우리 띠틈 규약상 판독 금지 방식의 예 |
| 2b | CCTO 띠구조 (bcc 경로) — 비점유 첫 띠 ≈ +1.2–1.9 eV 거의 β | 갭은 이쪽에서 읽는 게 낫다. 본문 'UHB 1.2 eV *below* E_F' 는 오기 |
| 2c,d | ELF 3D · 2D | 반심 껍질 고리 · '전자 밀도' 로 읽은 본문 오류 |
| 2e | TFSI⁻/CCTO 결합 −4.19 eV | ≳2 eV → 배위수 규칙 (`D-2026-10-05-adsorption-site-coordination`) · **구조 비공개 → 배위 미확인** · 자리 포화 에너지로만 |
| 2f | IL 양이온 18종 기체상 HOMO/LUMO · Pyr₁₃ 강조 | ⚠ 하전종 진공 궤도에너지 비교 — 산화 안정 지표 아님 |
| 3a,b | AFM PLI/PLIC (±150 nm) | 정성 |
| 3c,d | 단면 FESEM 100 µm | 3 µm 층 미분해 — 'gradient interphase' 근거 못 됨 |
| 3e | XRD: PAN 혹 약화 · CCTO 선 유지 | 결정성 정성 |
| 3f | σ vs T (라벨 1.44 / 1.40 · 점 ≈1.37 / ≈1.28 figure-read) | ⚠ 라벨 ↔ 점 불일치 (`Fig. S37` 벡터 확인) |
| 3g | 부유시험 4.1–4.7 V: PLI 4.6 V ≈40 µA · PLIC 4.7 V ≈45 µA (figure-read) | 겔 중간층의 고전위 누설 — 'PLIC 4.7 V 안정' 은 4.6 V 까지가 정확 |
| 3h | SS/Li CV · 도금 과전압 50.8 / 51.6 mV | 차이 0.8 mV — 의미 없음 |
| 3i | Raman 740 대 분해 (PLIC · PLI) | ⚠ 대역 겹침 · 자유 TFSI⁻ 감소 = 해리 증가의 반대 방향일 수 있음 |
| 4a–c | RDF · CN (Li–N(PAN) · Li–O(TFSI⁻) · Li–O(CCTO)) | CN 산수는 맞다 — 해석 (nm CCTO 덩이) 이 문제 |
| 4d | CN 막대 0.74/0.85 · 3.47/4.33 · 1.29 | 위와 같음 |
| 4e | MSD 50 ns: PLIC ≈0.022 nm² 고원 · PLI ≈0.012 (figure-read) | 🔴 총 변위 < 1 도약 · 홉 수 검산 N ≈ 4 — **D 로 정의되지 않음**. 우리 MSD 규율 설명용 반례 |
| 4f,g | MD 상자 스냅숏 | — |
| 4h | 수송 기전 만화 | — |
| 5a | LFP‖Li 1 C 장기: PLIC 끝 ≈1055–1060 (픽셀) · PLI ≈495 급락 | ⚠ '1100th' ↔ 데이터 끝 |
| 5b | in-situ EIS 첫 충방전 (Nyquist 묶음) | — |
| 5c,d | DRT: τ ≈10⁻⁴ s 'CEI' · 0.1 s ct · 10 s 확산 | ⚠ 같은 τ 를 Li‖Li 에선 SEI 로 (`Fig. S20`) · 첫 사이클뿐 |
| 5e | 율속 (PLIC 0.5 C 점 ≈143–145 vs 본문 148.3, 픽셀) | ⚠ 본문 숫자 ↔ 점 |
| 5f | 파우치 0.1 C 25 사이클 + 구조도 (PLIC 층 안 그림) | 소형 (≈41 mAh, 우리 산수) |
| 5g | 파우치 접기 · 자르기 · 못 찌르기 LED | 정성 안전 시연 |
| 6a,b | 사후 AFM | 정성 |
| 6c,d | 사후 SEM + LPSC-PTFE 양극쪽 면 사진 (PLIC 쪽 노랗-갈색 원판) | 색 변화 미해석 |
| 6e,f | F 1s · N 1s ('LiN₃' 라벨 ≈400.7 eV) | ⚠ Li₃N 귀속 의심 |
| 6g | 원소 파이 (C F Li N O S) · LiF 1.9→2.6 · Li₃N 0.7→1.5 % | ⚠ 분석면 = 겔 표면 · 작은 차이 |
| 6h | 실패 · 보호 기전 만화 | — |
| S5 | AIMD LPSC 600 K: Li 궤적 · MSD 0–3.8 ps · 적합선 기울기 0.677 Å² ps⁻¹ (픽셀) | 🔴 D = 기울기 (1/6 누락 의심) · 관측창 ≈0.19 eV — 우리 AIMD 감사 사례 |
| S13 | LPSC-PTFE EIS · σ(T) · 0.35 eV (R(30 °C) ≈11 Ω figure-read) | 정규화 점검의 기준점 (§10-④) |
| S14 | LPSC-PTFE σ_e (DC 10 mV · 3600 s · Is 2.97 nA) | ⚠ 식 (3) 재현 안 됨 (§10-④) |
| S22 | LFP/LPSC-PTFE/Li: ≈3.45–3.47 V 평탄 ≈720 mAh g⁻¹ (figure-read) | 평탄 = LFP 평형 전위 — 연성 단락과 못 가름 |
| S23 | LPSC-PTFE LSV · 라벨 3.69 V (벡터 교차 ≈3.88 V) | 🔴 라벨 ↔ 기준 불일치 · kinetic overshoot 계열 |
| S24 | CCTO 결정구조 그림 | ε 근거 아님 (구조만) |
| S25 | 공정도: 볼밀 · 압연 → 건식 LPSC 막 / 용액 → 닥터블레이드 → 중간층 양극 | Q1 판정의 그림 근거 (막은 전극 위에 바른다) · ⚠ 방법 (열압 · 적하) 과 공정도 불일치 |
| S26 | ELF 2D 두 면 (원시셀 폭) | 🔴 '입계 산소 풍부' 주장 — 벌크 셀에 입계 없음 |
| S31 | CCTO 분말 SEM/EDS: ≈1–20 µm (figure-read) · Cu 뭉침 | 3 µm 층과 기하 불일치 · 'nano' 표현 반증 |
| S33 | PLIC 양극 단면 EDS (Cu/Ca/Ti 희박 점 · Fe 희박) | 침투 깊이 판단 불가 |
| S34 | 마이크로미터 0.051 → 0.054 mm | '3 µm' = 1 µm 눈금 기기 두 판독의 차 |
| S36 | PLIC · PLI EIS 30–60 °C (R(30 °C) ≈18 / ≈19.5 Ω) | 적층 R > 단독 R ↔ σ '상승' 주장 모순 |
| S37 | PLIC · PLI ln σ vs 1000/T (벡터: 1.357/1.284 mS cm⁻¹ @30 °C) | 🔴 headline σ 와 불일치의 정본 근거 |
| S38 | PLI · PLIC σ_e (Is 0.675 / 0.154 nA) | CCTO 몫 = 3.2× · 측정 바닥 근처 |
| S39 | PLI · PLIC LSV 4.57 / 4.62 V (벡터 4.58 / 4.62) | 라벨이 기준과 맞는 쪽 — S23 과 대비 |
| S40 | HOMO/LUMO 5종 (TFSI⁻ −4.07 eV 포함) | 🔴 SI 본문이 TFSI⁻ 를 빼고 비교 |
| S41 | Raman 분율 파이 (텍스트로 읽음) | 차이 ≤ 3.3 %p |
| S42 | Li⁺ 결합 −6.26 / −2.96 / −4.26 eV (CCTO = 비주기 클러스터) | 배위 미확인 · 하전종 진공 값 |
| S46 | NCM811‖Li 0.5 C 150 사이클 (PLIC 첫 점 ≈135 · 최대 ≈157) | 유지율 기준점 불일치 |
| S53 | PLI 쪽 사후 XPS 9종 (P 2p · Cl 1s 잡음) | LPSC 원소 미검출 = 분석면은 겔 |
| S54 | PLIC 쪽 사후 XPS 12종 (P · Cl · Ti · Ca · Cu 전부 잡음 · O 1s 한 성분) | 같은 판정 + Li₂O 주장 반증 |
| Table S1 | IL 양이온 18종 HOMO/LUMO/gap (6 자리) | Pyr₁₃ gap 9.788545 — 본문 9.6 과 대조 |
| Table S2 | IL 가격 (¥/5 g) | 음이온 이름 오기 |
| Table S3 | 막 물성 비교 (σ · Ea · 창 · σ_e — σ_e 단위 mS cm⁻¹) | 본문 숫자의 표 정본 (그림과 어긋나는 값 포함) |
| Table S4 | 고분자 전해질 σ/창 비교 | 범주 다른 비교 |
| Table S5 | 사이클 성능 비교 (전고체 황화물 셀들과) | ⚠ IL 하이브리드 LFP 셀과 전고체 NCM/LCO 셀을 한 표에 |

---

## 10. 비판 — 이 논문의 약한 곳 ★

**🔴 ① '거대 유전' 이 측정도 계산도 되지 않았다.** PLIC · CCTO 분말의 ε · 유전손실 · 주파수 의존이 없다. `Fig. S24` 는 결정구조 그림이다. 우리 유효매질 산수 (§4g) 로는 ≈7 vol% 고립 입자가 기지 ε 를 ≈1.2 배로 올리는 데 그치고, 그 값은 CCTO 의 ε 가 10⁴ 이든 10⁵ 이든 같다. 정상상태 이온전도 매질의 전기장은 σ 가 정한다 (τ = ε/σ ≈ ns–µs). 저자 스스로 'hypothesize' · 'may'. **저유전 충전재 (Al₂O₃ · SiO₂) 같은 부피분율 대조군이 없어** '거대 유전' 과 '아무 절연 충전재' 를 가를 수 없다.

**🔴 ② 대조 설계 — CCTO 의 몫이 작고 그 큰 몫은 장기 사이클 하나다.** `Fig. 1` 의 극적 대비는 '중간층 없음 vs PLIC' 다. PLI ↔ PLIC 는 σ (본문) ×1.03 · 창 +0.05 V · σ_e ÷3.2 · 도금 −0.8 mV · Raman −3.3 %p. 수명 차 (LFP · NCM) 는 크지만 n · 오차막대가 없고 *"five parallel tests and averaged"* 의 분산이 어디에도 없다.

**🔴 ③ 본문 숫자 ↔ 자기 그림 (우리 재판독).**
- (a) σ(30 °C) 본문 1.44 / 1.40 ↔ `Fig. S37` 벡터 표식 **1.357 / 1.284** mS cm⁻¹ — LPSC-PTFE 1.39 보다 둘 다 낮으니 *"both composites outperform the pristine LPSC-PTFE"* 가 그림과 어긋난다 (Ea 재적합 0.309 / 0.294 eV 는 라벨 0.30 / 0.29 와 맞음 — 즉 그림 데이터가 원자료로 보인다).
- (b) LPSC-PTFE LSV 라벨 3.69 V ↔ 자기 기준 (100 µA) 교차 **3.876 V** (삽도 경로 좌표) · 3.925 V (본도). PLI · PLIC 라벨은 기준과 맞다 (4.58 · 4.62) ⇒ 개선폭 '≈1 V' → **≈0.74 V**.
- (c) AIMD `Fig. S5`: 그려진 적합선 기울기 **0.677 Å² ps⁻¹ = 6.77×10⁻⁵ cm² s⁻¹** (픽셀 적합 · 585 열) = 보고 D 6.77×10⁻⁵ — **D = MSD/(6t) 의 1/6 이 빠진 것으로 보인다** (그러면 ≈1.1×10⁻⁵). 본문은 이 값을 **600 K** 라는 말 없이 *"high Li⁺ diffusion coefficient"* 로 RT 수송 근거에 쓴다. (GROMACS 쪽 `Fig. 4e` 의 D 는 기울기/6 과 차수가 맞는다.)
- (d) LFP 1 C '1100th' ↔ 데이터 끝 **≈1055–1060 사이클** (픽셀: 눈금 0.7015 px/사이클 · 마지막 분홍 표식 x 871 · 오른쪽 축 x 899 = 1100).
- (e) 율속 PLIC 0.5 C 본문 148.3 ↔ 그려진 점 ≈143–145 (픽셀) — 다른 칸도 본문이 PLIC 쪽은 높게 · PLI 쪽은 낮게 적혔다 (2–5 mAh g⁻¹).
- (f) Li 핵생성 과전압 본문 56.8 mV ↔ `Fig. S16` 라벨 50.5 mV.
- (g) Pyr₁₃⁺ gap 본문 9.6 eV ↔ `Table S1` 9.788545 eV · *"9.5–10 eV"* 네 후보 중 Pyr₁₂ 10.12.
- (h) LPSC 분말 σ_e 7.02 (그림 · 본문) ↔ 7.09×10⁻⁹ S cm⁻¹ (`Table S3`).

**🔴 ④ 전도도 정규화가 서로 맞지 않는다 (우리 산수 · R 은 figure-read).** 같은 SS/SS 셀의 LPSC-PTFE 에 대해 — 이온: σ 1.39 mS cm⁻¹ · R ≈11 Ω ⇒ **L/S ≈ 0.016 cm⁻¹** · 전자: σ_e 8.57×10⁻¹¹ · Is 2.97 nA · 10 mV ⇒ **L/S ≈ 2.9×10⁻⁴ cm⁻¹** — **≈50 배 남짓** (R figure-read 에 따라 52–55) 다르다. 막 두께 50–55 µm 와 LSV 가 함의하는 SS 2.0 cm² 로는 L/S ≈ 2.75×10⁻³ 이고, 그러면 σ ≈0.25 mS cm⁻¹ · σ_e ≈ 8×10⁻¹⁰ S cm⁻¹ 가 나온다. PLI · PLIC 도 이온/전자 L/S 비가 ≈38–55 배. **L · S 의 숫자를 논문이 주지 않아 어느 쪽이 맞는지 가릴 수 없다** — 어느 쪽이든 '전자 절연 3배' 같은 비교는 같은 정규화 안에서만 뜻이 있다. 또 적층 R (≈18–19.5 Ω) 이 단독 막 R (≈11 Ω) 보다 큰데 σ 가 '올랐다' 는 것은 적층 두께가 1.7–1.8 배여야 성립한다 (3 µm 층과 모순).

**🔴 ⑤ ACIPO 의 정체가 진단되지 않았다.** LFP 셀 평탄 ≈3.45 V = LFP 자신의 평형 전위 · NCM811 셀은 NCM 의 OCV 보다 낮은 ≈2.2 V 에서 시작 · 막 CCD 0.27 mA cm⁻² · IL 이 든 셀. 지속 산화 · 연성 단락 · IL 매개 셔틀을 가르는 실험 (사후 OCV · 분해 XPS/라만 · 기체 · 단락 저항) 이 없다. 그리고 **대조 셀 양극의 IL 에는 Li 염이 없다** — 중간층 용액이 LiTFSI 를 양극 공극으로 공급하는 효과와 '격리' 효과가 섞인다.

**🔴 ⑥ '전고체' 표기.** IL 이 양극 10 wt% · 중간층 고형분 44 wt% (≈50 vol%) · Li 쪽 5 µL. SI 제목은 *"All-Solid-State"* 다. `Table S5` 는 이 하이브리드 LFP 셀을 **전고체 황화물 NCM/LCO 셀들**과 같은 표에 놓는다.

**🔴 ⑦ 사후 'CEI' 는 겔 중간층의 표면이다.** P · Cl · Ti · Ca · Cu 가 하나도 안 잡힌다 (`Fig. S53` · `Fig. S54`) — XPS 는 LFP 입자 위 CEI 를 보지 못했다. LiF 1.9 → 2.6 % · 'Li₃N' 0.7 → 1.5 % 는 작고 · 한 시료 · 맞춤 의존이다. 'Li₃N' 은 그림 라벨 'LiN₃' · 위치 ≈400.7 eV (통상 Li₃N 과 멀다, 일반 문헌값) · Li 1s 'LiF₃' · O 1s 에 Li₂O 성분 없음인데 본문은 Li₂O 를 무기 CEI 로 열거한다.

**🔴 ⑧ 계산.**
- (a) **AFM 을 원시셀 Cu 에 부과** — CCTO 원시셀 (Im-3, Z = 1 · 20 원자) 에는 Cu 가 **3 개**라 보상 반강자성이 원리적으로 불가 (우리 추론) · 결과 DOS 는 α/β 가 비대칭이고 HOCO 가 다르다 (`Fig. 2a`) — 'AFM' 이 아니라 순자기모멘트가 있는 상태로 보인다. 실험 AFM 배열을 쓰려면 관용 셀 (40 원자) 이 필요하다.
- (b) **U 값 미기재** — DFT+U 에서 Mott 갭은 U 가 만든다. *"DOS unambiguously identifies CCTO as a classic Mott-Hubbard insulator"* 는 입력이 출력을 정한 순환이다.
- (c) **PDOS · ELF 가 Γ 점뿐** — 20 원자 셀 Γ-only DOS 는 이산 준위를 넓힌 것이다 (SCF 는 9×9×9 인데 분석은 Γ).
- (d) *"upper Hubbard band … 1.2 eV below the Fermi level"* — 물리 오기.
- (e) **'ELF 로 입계를 봤다'** (`Fig. S26`) — 벌크 주기 셀에 입계가 없다.
- (f) IBLC 서술 '절연 입자 + 절연 입계' — 통상 그림 (반도체 입자 + 절연 입계, 일반 지식) 과 다르고, 그 자체로 거대 ε 가 안 나온다.
- (g) **결합에너지** −4.19 (TFSI⁻–CCTO) · −4.26 (Li⁺–CCTO) eV 는 화학결합 규모 (≳ 2 eV) — 우리 규칙 (`D-2026-10-05-adsorption-site-coordination`) 으로는 **배위수부터** 세야 하는데 구조 비공개 → **'배위 미확인'** · `Fig. S42` 의 CCTO 는 잘라낸 비주기 클러스터라 저배위 자리일 공산이 크다 ⇒ '그 자리의 결합 포화 에너지' 로만 읽는다. 하전종 (TFSI⁻ · Li⁺) 진공 값이라 Coulomb 항이 지배하고 (TFSI⁻–Li⁺ −6.26 eV 는 기체상 이온쌍), BSSE · 용매 · 배치 탐색이 없다.
- (h) **HOMO/LUMO** — 전하가 다른 종 (양이온 · 음이온 · 중성) 의 진공 궤도에너지를 한 줄에 놓았다 (양이온은 깊게 · 음이온은 얕게 밀린다). SI 본문은 TFSI⁻ (−4.07 eV) 를 빼고 비교했다. Pyr₁₃TFSI 는 PLI · PLIC 모두에 있어 둘의 차이를 설명 못 한다.
- (i) **MD** — CCTO 를 nm 덩이로 넣었다 (`Fig. 4h` · 스냅숏) ↔ 실제 1–20 µm 입자 (`Fig. S31`) — 표면/부피비가 수 자릿수 과장되어 Li–O(CCTO) CN 1.29 는 실제 막의 대표값이 아니다. REPEAT 고정 전하라 **유전 응답이 MD 에 없다** (CCTO 는 '음전하 O 표면을 가진 산화물 덩이' 로만 들어간다). MSD 총 ≈2 Å² · 홉 수 N ≈ 4 (0.30 eV · 298 K · 50 ns) → D 로 정의 안 됨. 맞춤 창 · 열浴 · 상자 · 분자 수 · 시드 미기재.
- (j) **AIMD** — 600 K 한 온도 · ≈3.8 ps · 궤적 1 · 1/6 의심 · 무질서 미기재 · 셀 모호 · 관측창 ≈0.19 eV.

**⚠ ⑨ 입자 크기 ↔ 층 두께.** 1–20 µm CCTO 와 3 µm 층 — 분쇄 · 분산 단계 없이 연속막이 될 수 없다. 'nanoparticles · nanofillers' 표현은 `Fig. S31` 과 맞지 않는다 (SI 서술 *"primary particle size of approximately 1 µm, with a significant fraction of nanoparticles"* 의 nano 분율도 그림에서 안 보인다 — 20 µm 막대 배율).

**⚠ ⑩ 'gradient interphase'** 는 100 µm 배율 단면 (`Fig. 3c,d`) 과 희박 점 EDS (`Fig. S33`) 에 기댄다 — 선분석 · FIB 단면 · TEM 없음.

**⚠ ⑪ DRT 귀속.** τ ≈10⁻⁴ s 를 Li‖Li 에서는 SEI (본문 · `Fig. S20`), LFP‖Li 에서는 CEI 로 — Li 음극이 있는 완전셀에서 양 · 음극을 가르지 않았다. '사이클 후' 라 쓰고 첫 사이클만 보였다. τ_CEI 봉우리 차이는 figure-read ≈1.2 배.

**⚠ ⑫ 1 C 전류 ↔ CCD.** 0.26–0.68 mA cm⁻² vs 0.27 mA cm⁻² — 어느 로딩인지 미기재.

**⚠ ⑬ 유지율 기준점.** NCM PLIC 는 2–3 번째 사이클 (142.3) 기준 · 최대 ≈157 대비 ≈73 % · PLI 는 첫 사이클 기준. LFP PLIC 기준 112.6 의 사이클 미기재 (첫 점 ≈115–117).

**⚠ ⑭ Raman 해석 방향.** 대역 겹침 · 스펙트럼 하나 · ≤ 3.3 %p. '자유 TFSI⁻ 감소' 는 '해리 증가' 의 반대 방향일 수 있다.

**⚠ ⑮ 오식 · 복붙 흔적.** 캡션 *"cplpssal-dielectric"* · 그림 *"Wihtout"* · *"Simiulation"* · *"displament"* · *"Disharge"* · *"ACG"* · *"LiN₃"* · *"LiF₃"* · SI 캡션 *"Li/CMEFI/Li"* (`Fig. S15`) · *"Li/CPE/Li"* (`Fig. S18`) · *"Li/CPEs/Li … Li/FAEIS/Li … 300–310 h"* (`Fig. S19`) · LPSC 에 *"SPEs"* (`Fig. S1` · `Fig. S13` · `Table S3`) · 'finger-forward factor' · `Table S2` 음이온 이름 · `Fig. S25` 공정 (압연 · 닥터블레이드) ↔ 방법 (열압 · 적하) · XRD 범위 5–50° ↔ 그림 5/10–80° · 본문 *"Li striping"* · CV 근거를 `Fig. S15` 로 인용.

**⚠ ⑯ '최초' 주장.** *"this work pioneers the integration of colossal dielectric CCTO into solid-state electrolytes"* — 유전체 충전재 복합전해질은 저자 ref [23] 이 이미 있다 (다른 유전체). CCTO 한정 최초 여부는 이 digest 에서 검증하지 않았다.

**⚠ ⑰ 파우치 안전.** ≈41 mAh (우리 산수) · 0.1 C · 25 사이클 · LED 점등 정성. 정량 안전 시험 (온도 · 전압 기록) 없음.

**⚠ ⑱ PTFE 서술의 전위 방향.** *"electron injection into its frontier orbitals … defluorination"* 은 **환원**이다 — 양극 충전 (산화) 문제의 근거로 쓰였다. PTFE 의 몫을 따로 시험하지도 않았다. 같은 날 들어온 `schmitt2026_chemomech_stability_dry_cathode_separator_sheets` 는 건식 분리막 PTFE 의 분해를 **저전위 (환원) 쪽**에서 보고, 양극 쪽 PTFE 는 분해가 안 보인다고 정리한다 — 이 논문의 동기 문장과 반대 방향의 실측이다.

**(공정)** 볼밀 조건 0 · CCTO 입도 분포 0 · 용액 농도 (절대 질량) 0 · 원자료 · 구조 파일 공개 0.

---

## 11. 우리 원장 매핑 (요약표)

| 우리 쪽 | 이 논문이 주는 것 | 판정 |
|---|---|---|
| `canonical_registry.json` comp1 항목들 (띠틈 · B₀ · 탄성 · Ea · ICOHP) | 없음 (LPSC 계산은 AIMD 하나) | 대조 없음 |
| ESW 축 ① (S²⁻-limited onset) | 겔막의 LSV · LPSC-PTFE LSV (라벨 불일치) | 정의 다름 — 같은 줄 금지 |
| ESW 축 ② (전자 접근) — 우리에게 σ_e 축 없음 | 막 σ_e (DC 분극) | 측정 종류만 참고 (정규화 불일치) |
| CEI 트랙 (산물 재분배 · 산물 띠틈) | 황화물 산물 0 · '갭 → 격리' 의 외부 함정 사례 | 산물 대조 없음 · 금지 서술 실증 1건 |
| cascade 축 ① (닫힘) | 정성 장면 (`Fig. 1c`) | 검증 안 함 |
| SDCP/PTFE C-12 (citable false) | 같은 종류의 진공 단일 배치 결합에너지 · 금지 해석의 외부 사례 | 숫자 병치 금지 |
| MD 규약 (홉 수 · 관측창 · MSD 창) | 위반 사례 셋 (AIMD 3.8 ps · 1/6 · MD MSD < 1 도약) | 교육용 반례 |
| 흡착 배위 규칙 (`D-2026-10-05-adsorption-site-coordination`) | −4.19 · −4.26 eV · 구조 비공개 | '배위 미확인' |

---

## 12. 적용 인사이트 ★

1. **'중간층이 이온은 통하고 전자는 막는다' 를 증명하는 최소 세트**는 ① 같은 정규화의 σ_ion 과 σ_e (L · S 숫자 공개) ② 충전재 없는 대조 (이 논문의 PLI) ③ 충전재 종류 대조 (고 ε vs 저 ε, 같은 부피분율) 다. 이 논문은 ② 만 했다. 우리가 코팅 · 중간층 계산을 실험 쪽에 제안할 때 이 세 칸을 같이 건다.
2. **'유전율 → 계면 전기장' 주장은 유효매질 · τ = ε/σ 두 줄로 먼저 거른다** — 분산 충전재는 기지 ε 를 부피분율만큼만 올리고, 전도 매질에서 ε 는 과도 응답만 바꾼다. 공간전하층 (평형 이중층) 논리라면 Debye 길이 · 접촉 기하를 따로 세워야 한다.
3. **LSV '창' 은 라벨이 아니라 곡선에서 다시 읽는다** — 벡터 그림이면 경로 좌표로 문턱 교차를 계산할 수 있다 — 이번 판독은 **`tools/litdb/liu2026_ccto_readout.py`** (`s23` · `s39` · `s37` · `s5` · `f5a` · `--selftest`) 로 재현된다. 같은 꼴의 논문별 판독 스크립트가 `tools/litdb/richards2016_si_figs.py` · `*_digitize.py` 에 있다 (일반 도구는 아니다). ⚠ 채우기만 있는 도형 (삽도 강조 상자 · 화살표) 을 곡선으로 섞으면 교차가 엉뚱하게 나온다 (이번에 한 번 밟음 — 스크립트가 거른다). `[Ling26]` (Table S4 50 µA ↔ 그림 3.05 V) 에 이은 같은 유형의 두 번째 사례.
4. **AIMD 의 D 는 그려진 적합선 기울기와 대조한다** — D = 기울기/6 (3D). 기울기 그대로면 6 배 과대. 우리 문헌 감사 체크 한 줄로 쓸 만하다.
5. **고전 MD 의 '6 배 빠른 D' 는 총 MSD 부터 본다** — 첫 배위 거리² 보다 작으면 D 가 아니다 (홉 수 검산으로 바로 걸린다).
6. 우리 그룹 `kang2025_highvoltage_parasitic_reaction_benefit_sulfide_assb` 는 고전압 기생반응이 **이득이 될 수도** 있다는 쪽이다 — 이 논문은 기생 산화를 전부 해로운 것으로 놓는다. 두 편을 같이 읽으면 '어느 기생반응이 자기부동태로 끝나고 어느 것이 끝없는 용량이 되나' 가 질문이 된다 (축 ① 의 산물 전자 등급과 같은 질문).

---

## 13. 인용 가능 문장 (영문 초안)

- *"Liu et al. separated a dry-processed Li₆PS₅Cl–PTFE membrane from wet-processed cathodes with a ≈3 µm PAN/LiTFSI/Pyr₁₃TFSI ionogel interlayer containing CaCu₃Ti₄O₁₂ filler, which removed the non-terminating charge plateau observed under direct contact (J. Colloid Interface Sci., 729, 141891 (2027))."*
- *"In that work, most of the stabilization was already obtained with the filler-free ionogel interlayer; the dielectric permittivity of the composite was not measured."*
- (방법 경고) *"Electrochemical windows reported from linear sweep voltammetry depend on the current threshold and scan rate and refer to the measured film, not to the intrinsic oxidation onset of the sulfide."*

---

## 14. 주의 / 한계 (인용 규율)

- ⛔ **'CCTO 의 거대 유전율이 계면 전기장을 균질화한다'** 를 사실로 인용하지 않는다 — 저자 가설 · 측정 0.
- ⛔ **'ESW 4.62 V'** 를 LPSC 또는 Li₆PS₅Cl 의 안정창으로 인용하지 않는다 — 겔막 LSV (5 mV s⁻¹ · 100 µA) 값이다. LPSC-PTFE '3.69 V' 는 자기 기준과도 어긋난다.
- ⛔ **σ 1.44 / 1.40 mS cm⁻¹ · '중간층이 σ 를 올린다'** 를 인용하지 않는다 — 그려진 점은 1.36 / 1.28 이고 적층 R 이 더 크다.
- ⛔ **AIMD D 6.77×10⁻⁵ cm² s⁻¹** 를 인용하지 않는다 (600 K · 3.8 ps · 1/6 의심) · **MD D 1.18 / 7.58×10⁻¹⁰** 과 '6–7 배' 를 인용하지 않는다 (MSD < 1 도약).
- ⛔ **결합에너지 (−4.19 · −4.26 · −6.26 · −2.96 eV) 를 '결합 세기 · 고정 세기'** 로 인용하지 않는다 — 진공 단일 배치 · 하전종 · 배위 미확인. 우리 SDCP/PTFE 값과 **나란히 두지 않는다** (그쪽은 citable false).
- ⛔ **'LiF/Li₃N 풍부 CEI'** 를 이 논문 근거로 쓰지 않는다 — 분석면이 겔 표면 · 차이 작음 · 귀속 의심.
- ⛔ **'전고체'** 성능 비교 (`Table S5`) 에 이 셀을 넣지 않는다 — IL 하이브리드.
- ✅ 쓸 수 있는 것: '건식 LPSC-PTFE 막과 습식 양극의 직접 접촉에서 끝없는 충전이 관측되고, 고분자 이온겔 중간층으로 그것이 사라진다' (정성) · 'CCTO 충전재가 겔막의 DC 전자 누설을 PLI 대비 ≈3 배 줄였다 (같은 정규화 안의 상대값)' · 방법 경고 사례 (LSV 라벨 · AIMD 1/6 · MD MSD · 갭 → 격리 · 결합에너지 해석).
- 우리 쪽 숫자는 원장 (`canonical_registry.json` → `citation_hazards.json` → `decisions.json`) 에서만 가져오고, 이 논문 숫자와 같은 줄에 두지 않는다.

---

## 15. 기법 용어 미니사전

- **ACIPO** — 저자 조어 *anomalous capacity originating from interfacial parasitic oxidation*. 충전이 정상 용량을 넘어 계속되는 현상을 '계면 기생 산화' 로 해석한 이름 (원인 진단은 없음).
- **CCTO (CaCu₃Ti₄O₁₂)** — A-자리 정렬 페로브스카이트 (Im-3). 세라믹에서 10³–10⁵ 급의 거대 유전율이 보고되는 물질. 그 기원은 흔히 **IBLC** (internal barrier layer capacitor: 반도체 입자 + 절연 입계의 Maxwell–Wagner 분극) 로 설명된다 (일반 지식) — 즉 **미세구조 (외인성) 효과**라 벌크 결정 DFT 로는 직접 안 나온다.
- **Mott-Hubbard 절연체** — 전자 간 반발 (U) 로 d 띠가 하부 (점유) · 상부 (비점유) Hubbard 띠로 갈라져 갭이 생긴 절연체. DFT+U 에서는 U 가 그 갈라짐을 만든다.
- **유효매질 (Maxwell-Garnett)** — 기지에 고립 구형 입자를 분율 f 로 넣었을 때 유효 유전율 근사. 입자 ε 가 기지보다 훨씬 크면 ε_eff/ε_m ≈ (1+2f)/(1−f) 로 **입자 ε 에 무관**해진다.
- **유전 이완 시간 τ = ε/σ** — 전도 매질에서 전하 · 전기장 분포가 정상상태로 가는 시간. 그보다 긴 시간에는 전기장이 σ 로 정해진다.
- **ELF (electron localization function)** — 전자쌍 국재도 지표 (0–1). 전자 밀도가 아니다. 반심 가성퍼텐셜에선 양이온 주위에 껍질 고리가 보인다.
- **REPEAT 전하** — 주기계 정전퍼텐셜에 맞춘 원자 점전하. 고정 전하라 MD 에서 분극 (유전 응답) 이 없다.
- **RESP 전하** — 분자 정전퍼텐셜에 맞춘 점전하 (구속 맞춤).
- **SSIP · CIP · AGG** — 용매 분리 이온쌍 · 접촉 이온쌍 · 응집체. TFSI⁻ 의 740 cm⁻¹ 부근 Raman 대역 위치로 가른다 (대역이 겹친다).
- **DRT (distribution of relaxation times)** — 임피던스를 시정수 분포로 펼쳐 과정별로 가르는 해석. 같은 τ 대역이 양 · 음극 어느 쪽인지는 셀 구성으로만 가린다.
- **부유시험 (floating test)** — 전압을 계단식으로 올려 각 단에서 정전위로 유지하며 누설 (정상) 전류를 보는 시험.
- **Bruce–Vincent t_Li⁺** — Li‖Li 정전위 분극의 초기/정상 전류와 분극 전후 계면 저항으로 구하는 Li⁺ 수송수.
- **이온겔 (ionogel)** — 이온성 액체를 고분자 망에 가둔 준고체 전해질. 이 논문의 PLI/PLIC 가 여기에 해당한다 (부피 절반이 IL).
