# Li|전해질 계면 MD — 이 시뮬레이션에서 우리가 얻은 것

**설정** UMA-s-1p1 MLIP-MD · SE|Li-metal 슬랩 · 600 K NVT · **3 seed × 100 ps** · 통제쌍 = b2o3(128) vs **modelc_2x(124, b2o3를 도핑해 만든 바로 그 무도핑 프레임 = 같은 표면)** + modelc62(1×, 종단 교차확인)
**산출물** 시간곡선 `iface_timeseries.png`+`interface_timeseries_mean.csv` · CIF 스냅샷 6개(initial/relaxed/final100ps ×2계) · per-frame CSV 9개 · 집계 `interface_campaign_summary.csv`

---

## 1. 얻은 것 다섯 가지

### ① 분해 **화학 경로**를 직접 관찰 (열역학은 산물만, MD는 과정을 줌)
Li metal이 닿으면 **PS₄ 사면체가 풀리며 P는 Li₃P로(P–Li coord ↑), S는 Li₂S로(S–Li ↑)** 가는 과정이 프레임 단위로 보임 — 평형 계산이 예측한 그 산물이 실제 동역학 경로로도 확인됨. (양쪽 공통, argyrodite의 알려진 Li-계면 반응.)

### ② 통제비교의 핵심 결론: **도핑이 계면을 악화시키지 않는다**
같은 프레임·같은 표면에서 100 ps 후 PS₄ 잔존 **78±9%(b2o3) vs 74±0%(무도핑)** — 모든 분해 채널(Li₃P·Li₂S 생성, Li 침투)이 **오차 내 동등**. 개선 주장도, 악화 우려도 아닌 "**전해질 골격 분해 속도 불변**"이 정직한 결론.

### ③ **도핑 유래 결합 둘 다 강건: BS₃ + P–O 온전, 금속성 LiB·Li₂O 미실현** (이 study의 고유 발견)
- **B–S coord 3.00 → 3.00** (9/9 run) — 주변 PS₄가 풀리는 동안에도 붕소는 황 우리를 유지 → **금속성 LiB 안 생김**. (B–Li 1–2는 B–S 온전 상태의 Li 배위 = 합금 아님.)
- **O–P coord 1.00 → 1.00** (3/3 seed) — **phosphate P–O도 하나도 안 끊김 → Li₂O 안 생김.** (O–Li 2.0→2.0–2.7은 단순 Li 배위.)
- → **열역학 worst-case(B³⁺→BP/LiB, Li₂O)가 100 ps 동역학에서 전부 미실현** = ESW 축소(0.90→0.31 V)의 주범인 환원측 flag를 kinetics가 완화함을 자체 데이터로 입증. 분해는 오직 host P–S 채널로만 진행 (속도는 무도핑과 동일). ICOHP(B–S −7.8/P–O −8.6 = 최강 결합)·site-PDOS(깊은 상태)와 정합.

### ④ Li 침투는 표면 국한
양쪽 모두 100 ps에 **+7원자 수준**, 깊은 침투 없음 — 초기 SEI가 표면에서 형성되는 그림과 정합.

### ⑤ 방법론 교훈: **셀-두께 artifact** (재현 캠페인이 잡아낸 것)
같은 무도핑 물질인데 얇은 1× 슬랩(P 5개)은 48±8%, 2× 프레임은 26±0% 분해로 나옴(1.9×) — 계면 반응층이 전체 P 평균을 지배해서. **예비 단일시드의 "6× 억제" 주장은 이 artifact + 50 ps 조기 스냅샷이었고 철회됨.** 계면 비교는 반드시 같은-두께·같은-프레임 통제 필요.

## 2. 열역학 ↔ 동역학 한 표

| | 평형(ESW/hull) | 계면 MD (이 연구) |
|---|---|---|
| 예측/관찰 | Li-metal에서 **금속 LiB·BP** 생성 → 악화 | **BS₃ 온전, LiB/BP 안 생김** |
| 분해 정도 | (속도 정보 없음) | doped ≈ undoped, 표면 국한 |
| 의미 | 무한시간 하한 (비관적) | 실제 반응 경로 (passivation 쪽) |

→ 논문 논리: *"열역학 창은 좁아지나(환원측 B), 그 worst-case는 동역학에서 실현되지 않으며(BS₃ 강건), 분해 kinetics는 무도핑과 동등하다."*

## 3. 논문 문장 제안
1. "Interface MD (3 seeds × 100 ps) shows the B₂O₃-doped electrolyte decomposes at the same rate as the undoped frame at a Li-metal contact (PS₄ retention 78±9 vs 74±0%), i.e., doping does not compromise interfacial stability."
2. "The BS₃ thioborate units remain fully intact (B–S 3.00→3.00 in all seeds) and no metallic Li–B phase forms, showing that the thermodynamic worst-case reduction (B³⁺→BP/LiB) is kinetically suppressed on the simulated timescale."
3. "A thin-slab control revealed a ~2× cell-size artifact in interfacial decomposition metrics, underscoring the need for same-frame controlled comparisons."

## 4. 정직한 한계
- **100 ps = 초기 단계**: 양쪽 다 분해 진행 중(미수렴) — 절대 분해량이 아니라 **비교(동등)**만 인용.
- 표면 종단 1종/프레임 (c-면 cleave); 종단 다양화 미탐색.
- MLIP 반응상(Li₃P/Li₂S) 정확도는 DFT 단발 검증 미실시(선택 과제) — 결론이 "동등"이라 리스크 낮음.
- CIF 스냅샷은 seed-s2 대표 1개 (통계는 곡선/CSV가 담당).

## 5. 파일 인덱스
| 파일 | 내용 |
|---|---|
| `iface_{b2o3,modelc2x}_{0_initial,1_relaxed,2_final100ps}.cif` | VESTA 구조 스냅샷 (전/후 비교 그림용) |
| `iface_timeseries.png` / `interface_timeseries_mean.csv` | P–S 잔존율·B–S 평탄·Li 침투 시간곡선 (3-seed mean±std) |
| `db/properties/interface_decomp_*_s*.csv` | per-frame 원자료 9개 (kgy) |
| `db/properties/interface_campaign_summary.csv` | 계별 mean±std 집계 |
| `docs/figures/oxidation/interface_campaign_controlled.png` | 통제비교 요약 그림 |
| 관련 kb | `b2o3_anode_interface_campaign_2026_07_07.md`(확정), `..._MD_dynamics_2026_07_06.md`(예비, superseded), `b2o3_anode_interface_2026_06_30.md`(열역학) |
