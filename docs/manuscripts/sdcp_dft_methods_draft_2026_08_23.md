# SDCP 원고 v5 — DFT 파트 근거 (2026-08-23)

원고: **"Integrated binder and current-collector engineering with a self-doped conducting
polymer for high-rate, low-pressure dry-processed all-solid-state battery cathodes"**
(Bae, Kang, **An**, Jin, Lee) — Manuscript/SI v5.

산출물: `SDCP_DFT_methods_TableS1.docx` (생성기 `sdcp_dft_methods_build.js`)

**정본 = 발주 번들 `sdcp_wave1_2026_08_12` (v3) 하나뿐.**
그 이전 판(Phase-A UMA 랭킹 · 2026-08-08 VASP 납품)은 **전부 대체됐다** — 아래 어떤 수치도
그쪽에서 가져오지 않는다.

---

## 1. 원고의 DFT 결론

**SDCP 반복단위가 PTFE 조각보다 NCM811 표면에 더 강하게 흡착한다** — 근거는 DFT 흡착에너지.

```
E_ads = E(slab+molecule) − E(slab) − E(molecule)          ← 본문 별행 수식 (3)
        ↑ 같은 AFM seed    ↑ 같은 seed  ↑ box24 정본
```

⚠ 번호는 **(3)** 이다 — 본문 DEM 절이 (1)·(2) 를 이미 쓴다. DFT 절이 DEM 앞으로 가면 다시 매긴다.
수식은 일반 텍스트(이탤릭·아래첨자)로 넣어 뒀다. Word 수식 개체로 바꾸려면 영진 님 쪽에서
(1)·(2) 와 같은 방식으로 교체하면 된다.

들어가는 자리: 본문 `*Computational details*:` · SI **Table S1** · **Figure 2e**(값) ·
**Figure S3**(모델 그림).

---

## 2. wave1 번들 — 무엇을 돌리고 있나

30잡 / VASP 실행 43회 (static 30 · relax 8 · dense 5).

| 묶음 | 잡 | 내용 |
|---|---:|---|
| `refs` | 10 | clean slab × AFM seed 2 · 기체 분자 4조각 × 상자 2종(+20/+24 Å) |
| `tier1` | 8 | `ptfe_c10`(C₁₀F₂₂) · `ptfe_dimer`(C₄H₂F₈) × (Li-top/Ni-top) × seed 2 |
| `tier2` | 12 | `sdcp_neutral`(+cross pose 2) · `sdcp_doped` × (Li-top/Ni-top) × seed 2 |

**조각 4종**

| 조각 | 조성 | 원자 | 전자상태 |
|---|---|---:|---|
| `sdcp_neutral` | C₁₁H₁₆O₆S₂ (–SO₃H) | 35 | closed-shell singlet |
| `sdcp_doped` | C₁₁H₁₅O₆S₂ (–SO₃•) | 34 | doublet (`NUPDOWN 1`) |
| **`ptfe_c10`** | **C₁₀F₂₂** | 32 | singlet — **PTFE 대표** |
| `ptfe_dimer` | C₄H₂F₈ | 14 | singlet — C₁₀ 대조군, **단독 인용 금지** |

**계산 조건** (INCAR·KPOINTS·POSCAR 실측)

| 항목 | 값 |
|---|---|
| 방법 | PBE + U(Ni 3d) 6.2 eV (Dudarev, LMAXMIX 4) + D3(IVDW 11) |
| 컷오프 | ENCUT 520 eV · PREC Accurate · ADDGRID |
| smearing | ISMEAR 0 / SIGMA 0.05 eV |
| 수렴 | EDIFF 1e-6 eV (복합체·슬랩 단일점) · 분자 relax EDIFFG −0.02 eV/Å |
| k | **static 2 × 3 × 1** · dense 검증 3 × 4 × 1 · 분자 Γ only |
| 슬랩 | LiNiO₂(104) 1 × 4 · 4층 · **192원자**(Li₄₈Ni₄₈O₉₆) |
| 셀 | 면내 18.272 × 11.512 Å (γ 108.4°) · c 30.261 Å |
| 진공 | 흡착종 ↔ 주기 이미지 **15.9–16.4 Å** (복합체 POSCAR 실측) |
| 구속 | z ≤ **17.396 Å** 의 **144/192** 고정 |
| 자성 | AFM, seed 2종 — `afm2424_pm1`(net 0, **정본**) · `afm2424_net4`(net +4 μB) · Ni ±1.02 μB |
| 쌍극자 | LDIPOL T / IDIPOL 3 (슬랩) · IDIPOL 4 (분자) |
| 기타 | ISPIN 2 · ISYM 0 · LASPH T · LORBIT 11 · LREAL Auto |
| POTCAR | PBE PAW 5.4 — `Li_sv Ni_pv O S C F H` |

**기하 출처** — 복합체는 UMA-s-1p1 이완본 위의 **단일점**. 자세 탐색은 자리 7종 ×
피보나치 12방향(+화학태그 2) × roll 4, FIRE fmax 0.05 eV/Å 로 조각당 364–392 자세를 훑고
**조각당 Li 위 최선 · Ni 위 최선 1쌍**을 DFT 로 넘겼다 (`contract_mode: champion`).

**게이트 (fail-closed — 실패하면 그 조각의 E_ads 를 만들지 않는다)**
상자 20↔24 Å ≤ 10 meV · dense-k ΔE·E_ads ≤ 10 meV · seed 산포 ≤ 10 meV ·
PAIR_MIGRATED / PAIR_COLLAPSED 검사. 회수 후 `analyze_results.py` 가 자동으로 돈다.

---

## 3. 원고 문구를 묶는 제약 3개 (MANIFEST 원문)

| # | 원문 | 원고에서 |
|---|---|---|
| 1 | `claim_scope`: "E_ads 는 UMA 기하 위 단일점이라 완전 이완 흡착에너지가 아니다" | ⛔ **SI 에 안 넣기로 결정**(2026-08-23) — 내부 보관 + 리비전 회신 문구: `kb/syntheses/sdcp_eads_revision_defense_2026_08_23.md` |
| 2 | `branch_policy`: "pm1 same-seed conditional — branch minimum 미주장" | *"at the magnetic ground state"* 금지 → *"the same antiferromagnetic configuration"* 로 |
| 3 | `k_label_rule`: 직접 dense 한 건 `ptfe_c10`·`sdcp_doped` 둘뿐, 나머지는 `K_TRANSFER_SCREENED` | *"k-point converged"* 금지 → **mesh 병기만**(각주도 뺐다 — 위 카드 참조) |

---

## 4. 열려 있는 것

1. **E_ads 수치** — wave1 회수 대기. 게이트 통과 후 Figure 2e · 본문에 삽입.
2. **Ref. S4** — U(Ni 3d) = 6.2 eV 출처 논문 (우리 규약값, 원전 미보유)
3. **Ref. S5** — LiNiO₂ AFM 배열 출처 논문
4. **Figure S3** — 계산 모델 그림 (슬랩 + 조각 3종). 구조는 wave1 POSCAR 에 다 있다.

---

## 5. 원고 형식 — 같이 고칠 것

| | 현재 | 고침 |
|---|---|---|
| 약어 | `density functional theory` 본문 **0회** — DFT 가 정의 없이 쓰인다 | Fig. 2e 문단(첫 등장)에서 풀고 Methods 는 약어만 |
| SI 참고문헌 | SI Table S2(DEM) 가 `[107] [109] [110]` — 영진 님 임시 자리표시 | 참고자료 형식대로 **Ref. S1/S2/S3** S-계열 + SI 끝에 S-목록 (본문 번호로 이어 붙이는 쪽을 택하면 1–32 뒤로 — **둘 중 하나로 통일**) |
| 용어 | SI Table S2 `Elastic modulus` / 참고자료 `Young's modulus` / 본문 `*E*` | **Young's modulus** (기호 *E*)로 통일 |

---

## 6. VASP → Quantum ESPRESSO 변환표

원고는 QE 로 기술한다(사용자 지시). 숫자를 낸 코드와 Methods 가 다르면 사실과 어긋나므로
**원고에 실릴 숫자를 QE 로 다시 내는 것이 안전한 길**이다. 되돌릴 때는 왼쪽을 오른쪽으로.

| QE 표기 (docx) | wave1 VASP 실제 | 비고 |
|---|---|---|
| Quantum ESPRESSO (pw.x) | VASP 5.4.4 / 6.x · PBE PAW 5.4 | |
| ecutwfc 60 Ry / ecutrho 480 Ry | `ENCUT = 520` eV | 우리 QE 표준 조합 |
| conv_thr 1 × 10⁻⁶ Ry | `EDIFF = 1E-6` eV | VASP 쪽이 ~14× 더 조임 — 과대주장 아님 |
| forc_conv_thr 1 × 10⁻³ Ry bohr⁻¹ | `EDIFFG = −0.02` eV Å⁻¹ | 0.026 vs 0.02 — 거의 동치 |
| Gaussian smearing 0.05 eV | `ISMEAR = 0 / SIGMA = 0.05` | 그대로 |
| `vdw_corr='grimme-d3'` | `IVDW = 11` | D3 zero damping |
| `dipfield=.true., edir=3` | `LDIPOL / IDIPOL = 3` | 분자 `IDIPOL 4` → `assume_isolated='martyna-tuckerman'` |
| `lda_plus_u`, Hubbard_U(Ni) 6.2 eV | `LDAU / LDAUTYPE=2 / LDAUU=6.2 / LMAXMIX=4` | QE simplified rot-inv = Dudarev |
| `nosym=.true.` | `ISYM = 0` | |
| `tot_magnetization = 1` (doped 분자) | `NUPDOWN = 1` | |
| (QE PAW 기본 포함) | `LASPH` · `ADDGRID` · `LREAL = Auto` | QE 표기 불필요 |
| Γ-centred 2 × 3 × 1 / 3 × 4 × 1 | 동일 | `kmesh_effective` 기준 |
