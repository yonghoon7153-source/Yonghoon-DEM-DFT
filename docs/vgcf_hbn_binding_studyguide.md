# h-BN coating on VGCF — Li 결합·확산 계산 스터디 가이드

> 대학원생용 자료 (2026-07-22). 이 프로젝트가 **무엇을 왜 계산하는지**, 숫자를 **어떻게
> 읽는지**를 개념 단위로 설명한다. 결과 원본: `db/properties/vgcf_hbn_binding_matrix.json`.

---

## 1. 배경 — 왜 이걸 계산하나

리튬 금속 음극은 용량이 크지만 **덴드라이트**(Li가 삐죽삐죽 자라 단락) 때문에 위험하다.
해결책 중 하나가 **집전 구조체(host)에 Li를 고르게 분산**시키는 것. 우리 후보는:

- **VGCF** (Vapor-Grown Carbon Fiber): 다층 그래핀(흑연) 섬유 = 전자 잘 통하는 골격
- **h-BN** (hexagonal Boron Nitride): 그래핀과 같은 벌집 구조인데 **절연체** — 코팅층 역할

아이디어: **VGCF를 h-BN으로 코팅**하면, VGCF는 전자를 나르고 h-BN은 전해질 부반응을 막으며,
그 **사이 공간(gallery)에 Li가 끼어(intercalation)** 균일하게 저장되지 않을까?

이걸 검증하려면 두 가지를 계산해야 한다:
1. **결합 에너지 E_bind** — Li가 이 구조체에 얼마나 세게/약하게 붙나 (조건 ①: 적당한 lithiophobicity)
2. **확산 장벽 barrier** — 붙은 Li가 얼마나 잘 움직이나 (조건 ②: 낮아야 균일 분산)

---

## 2. 핵심 개념 4가지 (이것만 이해하면 표가 읽힌다)

### 2.1 흡착(adsorption) vs 삽입(intercalation)
- **흡착** = Li가 표면 **위**에 앉음 (한 면만 Li와 접촉)
- **삽입** = Li가 두 층 **사이**에 낌 (양쪽 면이 Li를 감쌈 → 배위 2배 → 더 세게 붙음)

우리 표에서 `[ads.]`는 표면 흡착, `[intercal.]`은 gallery 삽입이다. gallery가 항상 제일
세게 붙는 이유가 바로 "양쪽에서 잡아서"다.

### 2.2 E_bind의 부호 (vs 고립 Li 원자)
```
E_bind = E(host+Li) − E(host) − E(Li atom)
```
- **음수** = 붙는 게 이득 (안정). 더 음수일수록 더 세게 붙음
- 기준이 **고립 Li 원자** 한 개다 (진공에 떠 있는 Li). 이건 문헌(Shi 2017)과 맞춘 관례

### 2.3 Lithiophobicity — Li가 host를 좋아하나 벌크-Li를 좋아하나
"Li가 여기 붙는 게 좋나?"의 진짜 기준은 **고립 원자**가 아니라 **덩어리 Li 금속**이다
(실제로 Li는 금속 덩어리로 존재하니까). 그래서:
```
lithiophobicity = E_bind + E_coh(Li)
```
- **E_coh(Li)** = Li 금속의 응집 에너지 = Li 한 개를 벌크에서 떼는 비용. **우리 계산값 1.724 eV**
  (E(Li atom) −14.927 − E(Li bulk) −15.054 Ry에서 유도; 실험 1.63과 근사)
- **양수(+)** = host보다 **벌크 Li가 더 좋음** = Li가 host를 싫어함 = **lithiophobic**
- **음수(−)** = host가 더 좋음 = **lithiophilic**

왜 lithiophobic이 (약간) 좋은가? 너무 lithiophilic(Cu처럼)이면 Li가 특정 자리에 **뭉쳐서**
덴드라이트 씨앗이 된다. **적당히 lithiophobic**하면 Li가 한 곳에 안 몰리고 퍼진다. 단,
너무 lithiophobic이면 아예 안 붙으니, **약한 lithiophobic + 낮은 확산장벽**이 이상적.

### 2.4 Shi eq5 — 샌드위치 판정 (VGCF가 Cu 역할을 하나?)
문헌(Shi 2017)은 h-BN|Li|**Cu** 샌드위치를 봤다. 우리는 Cu 대신 VGCF다. 판정식:
```
gallery E_bind < min(VGCF 단독, h-BN 단독)  →  샌드위치가 두 단일면보다 강함 = 성립
```
성립하면 "VGCF가 Cu의 구조적 역할(샌드위치 안정화)을 한다"는 뜻.

---

## 3. 계산 셋업 (한 눈에)

| 항목 | 값 | 왜 |
|---|---|---|
| 방법 | QE, PBE-D3BJ (grimme-d3, dftd3_version 4) | vdW 포함 (층간 결합 중요) |
| ecut | 60 Ry (wfc) / 480 Ry (rho), PAW | 수렴 확인된 값 |
| 슈퍼셀 | 4×4 (Li–Li 이미지 거리 9.84 Å) | 희박 Li 극한 (한 Li가 이웃 Li 안 느낌) |
| k-mesh | 3×3×1 | 얇은 슬랩이라 면내만 촘촘 |
| 진공 | 18 Å | 슬랩끼리 안 느끼게 |
| 격자 | a=2.46 Å (h-BN을 그래핀에 −1.6% 압축) | 공통 격자라야 샌드위치·eq5 자기일관 |
| 힘 수렴 | 1e-3 Ry/Bohr (=0.026 eV/Å) | Shi는 0.01; 우리는 보수적 |

**모델 종류** (총 18개, zip에 POSCAR로 들어있음):
- 단일 표면: graphene, hbn (+ 각 2층 버전)
- Li 흡착: Li_on_graphene, Li_on_hbn (+ 2층)
- 이층 스택(코팅): bilayer = h-BN on VGCF (+ 층수 조합 4종)
- Gallery Li: Li_in_gallery (+ 층수 조합 4종)

---

## 4. 결과 — 2×2 결합 매트릭스

### 4.1 E_bind (eV, vs 고립 Li 원자)

| 사이트 | 1층 | 2층 | 유형 |
|---|---|---|---|
| VGCF 표면 | −1.100 | −1.252 | 흡착 |
| h-BN 표면 | −0.264 | −0.273 | 흡착 |
| **Gallery** (h-BN\|Li\|VGCF) | **−1.574** | (아래 매트릭스) | **삽입** |

**Gallery 층수 2×2 매트릭스** (VGCF층 × h-BN층):

| | h-BN 1층 | h-BN 2층 |
|---|---|---|
| **VGCF 1층** | −1.574 | −1.592 |
| **VGCF 2층** | −1.580 | **−1.626 ← 논문 대표값** |

> **왜 2L2L(−1.626)이 논문 대표값인가.** 참조 논문 Liu 2022(Adv. Mater. Interfaces 9,
> 2200011)가 **h-BN 2층** gallery(h-BN\|Li\|Cu)를 계산했다. 공정 비교하려면 우리도 h-BN 2층을
> 써야 한다. 그리고 VGCF는 실제로 **다층 흑연섬유**라 VGCF 2층이 물리적으로 현실적(참조의
> 벌크 Cu에도 더 가까움). 그래서 **h-BN 2층 + VGCF 2층 = 2L2L**이 (참조 정합 + 실물 정합)
> 대표. 1L1L(−1.574)은 "얇은 극한에서도 값 유지"라는 **층수 수렴 증거**로 인용
> (4칸 스프레드 52 meV = layer-converged). 즉 매트릭스는 대표값 하나 + 수렴 증명이 목적.

### 4.2 읽는 법 세 가지

**(a) Gallery가 항상 제일 세다** (−1.57~−1.63) — VGCF(−1.10)나 h-BN(−0.26) 단독보다 훨씬.
양쪽에서 잡으니까(개념 2.1). → **Shi eq5 성립**: gallery < min(VGCF, hBN) → VGCF가 Cu 역할.

**(b) 층수 민감도가 갈린다** (같은 방법의 차이값이라 오프셋 상쇄, 순수 층수 효과):
| | Δ(2층−1층) | 해석 |
|---|---|---|
| VGCF 표면 | **−0.151 eV** (민감★) | 그래핀은 도체 → Li⁺ 전하가 2층째로 퍼져 결합 강화 |
| h-BN 표면 | −0.009 eV (수렴) | 절연체 → 2층째가 전하 못 받음 → 층수 무관 |
| gallery (h-BN층) | −0.018 eV (수렴) | h-BN 캡 두께 무관 |
| gallery (VGCF층) | −0.006 eV (수렴) | **gallery 안에선 VGCF 층수도 무관!** |

→ 핵심: 표면 흡착은 VGCF 층수에 민감한데 **gallery 안에선 그 민감성이 사라진다**. 이유는
gallery에선 Li 전하 분산을 이미 h-BN 캡이 해주고 있어서, 아래 VGCF 한 층 더 있는 게 별 보탬
안 됨. **실무적 의미: gallery E_bind는 1층 모델로 이미 수렴값** → 비싼 2층 모델 불필요.

**(c) 전부 lithiophobic이되 gallery는 약하게** (lithiophobicity = E_bind + 1.724):
| 사이트 | 값 | 판정 |
|---|---|---|
| h-BN | +1.46 | 강한 lithiophobic (Li 거의 안 붙음) |
| VGCF | +0.47~+0.62 | 중간 |
| **gallery** | **+0.10~+0.15** | **약한 lithiophobic** ← 이상적 구간 |

→ **스토리 헤드라인**: gallery는 (i) 가장 안정하게 Li를 잡으면서 (ii) 여전히 약한
lithiophobic이라 **Li가 한 곳에 안 뭉치고 gallery 전체에 균일 삽입**될 조건. 그리고 VGCF가
Cu처럼 구조를 안정화하되 **Cu(−2.50, 강한 lithiophilic)의 과잉 앵커링 없이** 한다.

---

## 4.5 참조 논문 비교 (Liu 2022) + CDD

논문에 참조로 들어갈 **Liu 2022 (Adv. Mater. Interfaces 9, 2200011)** 는 h-BN\|Li\|**Cu**
샌드위치를 계산했다. 우리는 Cu 대신 **VGCF**. 둘 다 vs 고립 Li 원자 기준이라 직접 비교 가능:

| 사이트 | Liu 2022 (바닥=Cu) | 우리 (바닥=VGCF) | 해석 |
|---|---|---|---|
| Li on h-BN | −0.33 | −0.264(1L)/−0.273(2L) | **거의 일치** (우리 약간 약함: D3BJ+격자압축) |
| Li on 바닥재 | Cu −2.50 | VGCF −1.10~−1.25 | **VGCF는 Cu보다 훨씬 완만한 앵커** (탄소 vs 금속) |
| 샌드위치(gallery) | −3.16 | −1.626 (2L2L) | 우리가 약함 = **바닥이 Cu→VGCF라서** |

**→ 이게 우리 논문의 차별점이자 CDD로 시각화할 핵심**: VGCF는 Cu의 **구조적 역할**(샌드위치
최강 = Shi eq5 성립)을 하되, **Cu의 과잉 lithiophilic 앵커링(−2.50) 없이 완만하게(−1.1)**
한다. 완만한 앵커 = Li가 한 곳에 안 뭉치고 **균일 분산**되기 좋음. (h-BN 값이 Liu와 맞는 건
우리 방법 검증도 겸함.)

### CDD (Charge Density Difference) — 전하 재분포 시각화
```
CDD = ρ(Li+host) − ρ(host) − ρ(Li)     (같은 셀·같은 grid 3개 SCF)
```
Liu 그림 (f)(g)의 노랑(전하 축적)/청록(전하 결핍) 등가면이 바로 이거다. **읽는 법**:
- Li는 2s 전자 1개를 내놓고 **Li⁺**가 됨 → Li 주변은 **결핍(청록)**, 받는 쪽은 **축적(노랑)**
- **어디에 축적되나 = 누가 전자 받개(anchor)냐**를 보여줌

**우리 CDD 결과 (계산 완료, kgy — 3패널 iso 0.002 e/Bohr³ 통일)**:
- **Li on graphene**: 위=청록(Li 2s 결핍, 위로 뻗던 전자가 사라진 자리), 아래=노랑(Li–그래핀
  계면 축적). 깨끗한 **상하 다이폴** = Li⁺·전형적 이온 흡착. Liu의 Li–Cu (f)와 대응(도체가 전자
  받개). → **레퍼런스 패널**.
- **Li on h-BN**: 전하 전이 **최소**(h-BN 절연체) → 노랑 제일 적음 = 약결합(−0.26)의 전자적 근거.
- **gallery 2L2L**: 노랑이 **위(h-BN)·아래(VGCF) 양쪽**으로 뻗음 = Li가 **양면에 전자 줌**
  (bidirectional). 전하이동 최대(Δρ 진폭 ≈ h-BN의 **4배**). → **hero 패널**.

**전하이동 크기 순위**: h-BN(최소) < graphene < **gallery(최대)** — E_bind 순위와 **방향 일치**.
단 배율은 다름(CDD ~4× vs E_bind ~6×) → 결합엔 전하이동 외에 **vdW·배위**도 기여.

> **⚠ 핵심 뉘앙스 (예측 대비 정정 — 논문 셀링포인트)**: gallery에서 **h-BN 쪽에도 노랑이 뜬다**
> (초기 예측 "거의 없음"과 다름). 그러나 이건 **h-BN이 전자받개로 변신한 게 아니다** — h-BN은
> 여전히 절연 수동캡이다. 메커니즘: **VGCF가 진짜 받개(Cu 역할)** → Li가 VGCF로 전자 주고, 층
> 사이에 **갇힌 Li⁺가 h-BN 표면을 유도분극(polarization)/스크리닝**해서 h-BN 쪽 밀도가 유도적으로
> 쌓인 것. 즉 "**h-BN = passive cap / VGCF = acceptor / Li = 양면배위·구속**"이 eq5(VGCF=Cu 역할)의
> 전자구조적 실체다. (h-BN이 혼자면 lithiophobic인데 VGCF와 함께면 전하 재분포가 생기는 것 자체가
> gallery 최강결합 −1.626의 근거.)

→ CDD 그림 3종(graphene/h-BN/gallery_2L2L)이 Liu (c)(d)(e)+(f)(g)와 **1:1 대응**하는 비교그림.
**그림 사양**: 셋 다 iso 0.002 통일(비교 공정), 등가면 mode **Positive(노랑,+축적)/Negative(청록,−결핍)**,
**parallel 투영**(거리·lobe 정직), unit-cell 프레임 off. 계산 `tools/vgcf_hbn/run_cdd_kgy.sh`,
vesta 변환 `tools/electronic/cube_to_vesta_cdd.py` (3-SCF 차분, relaxed 구조).

## 5. 확산 (조건 ②) — NEB 진행 중

결합만 좋으면 안 되고 **Li가 움직여야** 균일 분산이 된다. 그래서 **CI-NEB로 확산 장벽**을 계산 중:

- **경로**: 이웃 hollow(육각형 중심)→hollow 한 칸 홉 (2.46 Å), bridge가 안장점(TS)
- **검증 앵커**: h-BN 표면 Shi2017 = 0.10 eV / graphene 표면 문헌 ~0.3 eV
- **핵심 신규값**: gallery 안 확산장벽 (문헌에 없음 — 우리 논문의 기여)

**예비 결과 (drag 법) + CI-NEB 진행 상황**:
- graphene 표면 0.281 eV (문헌 ~0.3과 일치 ✅ 방법 검증)
- h-BN 표면 0.010 eV (약결합이라 PES 평평 → NEB로 재확인 중)
- **CI-NEB (GPU, kgy — QE 7.4.1 from-source 빌드)**: Pass 1(endpoint relax) **3/4 완료**
  (hbn·graphene·gallery-1L), **2L2L relax 중**. 끝나면 Pass 2로 4개 배리어 자동 산출
  (7이미지, ~1~2일). gallery·2L2L = **핵심 신규값**(문헌에 없음).

판정 프레임: gallery barrier가 **≲0.4 eV면** "안정하면서도 이동 가능 = 균일 삽입층 성립".

---

## 6. 구조체 후보 종합 판정 기준 (이 프로젝트의 논리)

좋은 Li host 구조체 = **(A) 적당한 lithiophobicity** (안 뭉침) + **(B) 낮은 확산장벽** (잘 퍼짐).
- (A): gallery +0.10~0.15 = 약한 lithiophobic ✅ (본 계산 확정)
- (B): gallery barrier (NEB 진행중) — 이게 낮으면 h-BN@VGCF가 균일 Li 저장 구조체로 성립

---

## 부록. 구조 파일 읽기 (zip 안 POSCAR)
- 각 POSCAR = QE relax의 **초기 모델**(as-built). 원소 순서 = C/B/N/Li, Cartesian.
- gallery 구조는 VESTA에서 c축 Boundary 타일링하면 Li가 h-BN|VGCF 층 사이 낀 게 보인다.
- 이완된 최종 구조는 kgy의 `.out`에서 별도 추출(interlayer 3.90→3.78 등 미세 변화).
