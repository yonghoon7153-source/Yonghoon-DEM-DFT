# Nd 3d XPS — 왜 DFT로 못 구하고 문헌(실험)값을 쓰는가 + 확실한 출처

**날짜** 2026-06-30 · **범위** Nd³⁺ 3d 결합에너지(XPS)의 계산 가능성 + 인용 출처 정리
**관련 db** `db/properties/xps_reference_nd_only.csv`, `xps_reference_sei.csv`

> **한 줄.** Nd 3d XPS는 **열린 4f³ 껍질의 many-body multiplet + shake 위성**이라 단일입자 DFT로 위치(범위조차)를 신뢰성 있게 못 줌 → **실험 문헌값**을 앵커로 씀. 반면 **B/O/S/P/Cl**(우리 도핑 모티프 지문)은 ΔSCF core-hole/Bader로 **계산 가능**. 아래에 값·이유·**검증된 출처**를 못박는다.

---

## 1. 왜 DFT로 Nd 3d BE를 못 구하나 (3중 이유)
1. **core-hole pseudopotential 실패** — Nd(란탄족, 4f³)에 3d core-hole PP **pseudization 실패** → QE ΔSCF 경로 자체가 막힘.
2. **many-body multiplet (근본)** — 3d hole 생성 시 최종상태 **3d⁹4f³** 의 강한 **3d–4f 정전결합** + **charge-transfer(4f–ligand 2p 혼성)** → 단일 피크가 아니라 **multiplet + screened/shake 위성** 으로 강도가 ~972–1005 eV에 퍼짐. Kohn–Sham 고유값 하나로 **원리적으로 재현 불가**.
3. **4f 자기상호작용 오류** — (LDA/GGA) 4f 오배치, **PBE+U로 Nd 화합물 다루면 metal화**(Mott–Hubbard 절연을 못 살림; 우리 `nd2o3_FINAL_summary` 기록). 4f는 spectator라 결합엔 안 끼지만 core-level 분광은 못 줌.

→ 정량 Nd 3d는 **DFT가 아니라 atomic/charge-transfer multiplet (CTM)** 영역.

## 2. 실험 문헌값 (정제된 범위)
| 항목 | 값 (eV) | 비고 |
|---|---|---|
| Nd³⁺ **3d5/2 main** | **980.7 – 982.5** | DB 표준 ref **980.7**; 산화물 측정 **981.5–982.5**(시료/보정에 따라 ~983.8까지) |
| **3d3/2** | **~1003 – 1005** | 3d5/2 + **스핀궤도 ~22.5** |
| **위성(satellite)** | **~972 – 977** | 저BE쪽 shake-down/screened, Nd³⁺ 특성(개별 위치는 출처따라 972~977) |
| **전체 3d 엔벨로프** | **~972 – 1005** | multiplet + SO + 위성 합 |
| 보정 | C 1s 284.8 | charge referencing |
| 화합물별 | Nd₂O₃≈NdPO₄≈NdCl₃ ~982.5(C), **Nd₂S₃ ~981.5**(약간 낮음) | per-ligand 이동은 작고 multiplet에 묻힘 → **estimate** |

**우리 CSV 표기**: 중심 **982.5**(측정 spread 상단) 사용 중. **DB ref 980.7**도 병기 권장 → 범위 **980.7–982.5**.

## 3. 확실한 출처 (웹 검증 2026-06-30)
### 실험값 (범위)
1. **NIST X-ray Photoelectron Spectroscopy Database, SRD 20** — 미국 표준, 직접 조회: https://srdata.nist.gov/xps/
2. **The International XPS Database, Neodymium (Nd) Z=60** — Nd 3d5/2 = **980.7 eV (±0.2)**: https://xpsdatabase.com/neodymium-nd-z60/
3. **"Rare earth oxides Eu₂O₃ and Nd₂O₃ analyzed by XPS," Surface Science Spectra 26, 014001 (2019)** (AIP/AVS) — Nd₂O₃ **직접 측정**, 저BE 어깨(위성): https://pubs.aip.org/avs/sss/article/26/1/014001
4. **Uwamino, Ishizuka, Yamatera, "X-ray photoelectron spectroscopy of rare-earth compounds," J. Electron Spectrosc. Relat. Phenom. 34 (1984)** — 고전 RE 3d 값 + 위성: https://www.sciencedirect.com/science/article/abs/pii/0368204884800602

### multiplet / 위성 / CTM (정량 이론)
5. **F. de Groot & A. Kotani, "Core Level Spectroscopy of Solids," CRC Press (2008)** — charge-transfer multiplet(CTM) 표준 교과서 (정량 계산의 근거)
6. **"The electronic structure of rare-earth oxides in the creation of the core hole," J. Electron Spectrosc. Relat. Phenom. (1999)** — RE 산화물 core-hole 최종상태: https://www.sciencedirect.com/science/article/abs/pii/S0301010499003808
7. **arXiv:2505.14284 (2025)** — 란탄족 dioxide core-level 광전자분광(f 국재 vs 혼성): https://arxiv.org/abs/2505.14284

(신뢰도: ①② = 직접 조회 가능한 표준 DB(최우선), ③④ = peer-reviewed 측정, ⑤⑥⑦ = multiplet/CTM 이론.)

## 4. 그럼 무엇은 계산되나 (B/O/S/P/Cl — 우리 도핑 지문)
Nd만 어렵지 **경원소는 됨** (열린-4f 없음):
| 단계 | 방법 | 산출 | 위치 |
|---|---|---|---|
| 싸게(경향) | **Bader 전하** → potential model (ΔBE≈kΔq) | free-S²⁻(최저BE) < B–S < PS₄-S, B³⁺/phosphate-P 높음 | 진행중 pp.x Bader |
| 정량 | **ΔSCF core-hole** (ORCA cluster `/data/apps/orca-6.1.1`, 또는 QE) | 절대 BE ±0.5–1 eV + 화학이동 | gabia/KISTI |
| Nd 정량 | **CTM** (CTM4XAS/Quanty) — DFT 아님 | 3d multiplet 라인셰이프 | (필요시) |

→ **free-S²⁻ / 삼각 BS₃ / phosphate P–O** 의 XPS 지문(S 2p·B 1s·P 2p·O 1s)은 **계산+실험 둘 다 검증 경로** 확보. **Nd 3d는 위 문헌값이 앵커.**

## 5. 결론
- **Nd 3d BE = 실험 문헌값**(①–④)이 ground truth. DFT는 multiplet 때문에 **범위조차 불안정** → cop-out이 아니라 **물리적으로 옳은 선택**(실험값이 multiplet·위성·차폐를 이미 포함).
- 우리 핵심 모티프(B/O/S/P/Cl) XPS는 **계산 가능** → 별도 ΔSCF/Bader로 testable.
- CSV(`xps_reference_nd_only.csv`, `xps_reference_sei.csv`)에 위 출처 박음.

## 참고
- db: `db/properties/xps_reference_nd_only.csv`, `xps_reference_sei.csv`
- 관련: `kb/results/nd2o3_FINAL_summary_2026_06_24.md`(PBE+U metal화), `nd_anode_cathode_sei_formation_2026_06_24.md`
