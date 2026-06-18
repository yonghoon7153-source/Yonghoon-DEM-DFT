# Nd vs O 분리 — "Nd가 특별한가, O 운반체일 뿐인가" 정량 캠페인

작성 2026-06-18. 동기: "지금 이득(P–O −8.43·산화·phosphate)이 다 O 효과 아니냐"는 정당한 지적.
O-only/Nd-only는 **non-physical**(Nd₂O₃로만 도핑) → 의미 없음. **의미 있는 비교 = 같은 O를 주는 다른 양이온**.

---

## 0. 질문 재정의 (synthesizable한 형태로)
> "같은 O를 delivering하는 산화물 중, **Nd³⁺ 양이온이 다른 양이온이 못 하는 걸 하는가**?"
- 비교군: **Nd₂O₃ vs La₂O₃**(4f⁰ rare-earth = Nd-4f 특이성 분리) vs **Y₂O₃/Al₂O₃**(다른 3+) vs **Li₂O**(순수 isovalent O 운반체).

---

## 1. MP 빠른 스크린 (descriptor, compute 0 — `tools/oxidation/oxophilicity_descriptor.py`)
- **oxophilicity(M) = Ef/anion(M-sulfide) − Ef/anion(M-oxide)** [eV/anion, >0=O 선호, 클수록 강한 getter].
- M = Nd, La, Ce, Y, Sm, Gd, Sc, In, Ga, Al, Mg, Ca, Zn, Li, Na, Zr, Ti, Ta, Nb.
- **판정**: Nd가 plain O-운반체(Li/Mg/Al)보다 **위**면 → Nd³⁺에 진짜 추가 O-친화(getter) 있음. Nd≈Li면 → 그냥 운반체.
- La/Ce/Y와의 위치 → rare-earth 일반성 vs Nd 특이성.
- ⚠️ 이건 **이진 산화물 기준 스크린**(proxy). host 안 실제 값은 DFT(아래).
- 실행: kserver116/gabia (MP 필요), `python3 oxophilicity_descriptor.py --out oxophilicity.json`.

---

## 2. DFT 결정 실험 (MPI/QE, KISTI — 최대 설계)
**host**: modelc (Li₅.₄PS₄.₄Cl₁.₆), nd와 동일 120-atom 셀·동일 setup(PAW kjpaw, k661, nspin2 — Nd/La면 +U on 4f).

### 2A. 양이온-스왑 시리즈 (cation 역할 isolate — 가장 깨끗)
같은 구조·같은 O 배열·같은 Li 공공에서 **양이온만 Nd↔La↔Y↔Al↔(Li)** 교체 후 relax:
| 측정 | 분리하는 것 |
|---|---|
| **ΔΔE = E(M+O) − E(La+O)** | Nd vs La = **4f 특이성** (La는 4f⁰) |
| eigenvalue gap | 갭 narrowing이 Nd-4f/5d인지 generic 3+인지 |
| grand-potential 산화 onset | cation이 O 너머로 산화를 바꾸나 |
| PDOS (M 5d/4f 위치) | CBM 낮추는 게 Nd 5d 맞는지 |

→ **Nd vs La가 핵심**: gap·산화·E가 La와 같으면 "그냥 rare-earth+O", 다르면 "Nd-4f 특이".

### 2B. O-getter 직접 측정 (host 안에서 — proxy 아닌 진짜)
Nd-도핑 셀에서 **O를 Nd 근처(P–O–Nd) ↔ Nd에서 먼 곳(P–O, Nd 없음)** 로 옮겨 relax:
- **ΔE_getter = E(O far from Nd) − E(O near Nd)**.
- ΔE_getter > 0 (크게) → **Nd가 O를 실제로 host 안에서 붙잡음** = getter 정량 (binary-oxide descriptor보다 강한 증거).
- La/Al로도 반복 → 어느 양이온이 O를 제일 잘 잡나.

### 2C. (확장) O-incorporation 반응에너지
modelc + ½M₂O₃ → (M,O)-doped + 부산물. 동일 reference로 M별 ΔE_inc 비교 → "Nd가 O를 제일 favorable하게 넣나".

---

## 3. 결정 metric (이게 "다 O냐?"를 가름)
| 결과 | 결론 |
|---|---|
| ΔE_getter(Nd) ≫ 0 **and** Nd > La/Al | **Nd 고유 getter** = Nd 노벨티 ✅ |
| gap(Nd) ≠ gap(La) | 갭 narrowing이 **Nd-4f 특이** ✅ |
| Nd ≈ La ≈ Li 전부 | **"다 O다"** — Nd는 운반체 ❌ (정직히 인정) |

---

## 4. 실행 (MPI/HPC)
- 각 dopant = 120-atom relax + scf + nscf(gap) + (선택)nscf_dos → QE MPI on KISTI (nd run과 동일 launch, ~0.5일/개).
- 최소셋: **Nd, La, Li₂O** (4f 분리 + 순수-O). 풀셋: +Y, +Al.
- 빌더: nd LOBSTER 빌더(`tools/nd/build_lobster_nd.py`)처럼 nd scf를 text-edit해 양이온만 교체 → relax/scf/nscf 생성 (작성 예정).

## 5. 한 줄
> **O-only/Nd-only(non-physical) 대신 "Nd₂O₃ vs La₂O₃/Li₂O"로 양이온을 바꿔 비교.** MP oxophilicity(빠른 스크린) + DFT 양이온-스왑·O-getter(결정). **Nd vs La가 4f 특이성을, ΔE_getter가 host 안 getter를 정량** → "Nd가 필요한가 vs 다 O인가"를 결판.
