# Li|전해질 계면 MD — 이 시뮬레이션에서 우리가 얻은 것

**설정** UMA-s-1p1 MLIP-MD · SE|Li-metal 슬랩 · 600 K NVT · **3 seed × 100 ps** · 통제쌍 = b2o3(128) vs **modelc_2x(124, b2o3를 도핑해 만든 바로 그 무도핑 프레임 = 같은 표면)** + modelc62(1×, 종단 교차확인)
**산출물** 시간곡선 `iface_timeseries.png`+`interface_timeseries_mean.csv` · CIF 스냅샷 6개(initial/relaxed/final100ps ×2계, **논문 구조그림은 CIF 렌더 채택**) · 2.5D GIF(보조) · per-frame CSV 9개 · 집계 `interface_campaign_summary.csv`

---

## 1. 얻은 것 다섯 가지

### ① 분해 **화학 경로**를 직접 관찰 (열역학은 산물만, MD는 과정을 줌)
Li metal이 닿으면 **PS₄ 사면체가 풀리며 P는 Li₃P로(P–Li coord ↑), S는 Li₂S로(S–Li ↑)** 가는 과정이 프레임 단위로 보임 — 평형 계산이 예측한 그 산물이 실제 동역학 경로로도 확인됨. (양쪽 공통, argyrodite의 알려진 Li-계면 반응.)

### ② 통제비교의 핵심 결론: **도핑이 계면을 악화시키지 않는다**
같은 프레임·같은 표면에서 100 ps 후 PS₄ 잔존 **78±9%(b2o3) vs 74±0%(무도핑)** — 모든 분해 채널(Li₃P·Li₂S 생성, Li 침투)이 **오차 내 동등**. 개선 주장도, 악화 우려도 아닌 "**전해질 골격 분해 속도 불변**"이 정직한 결론.

### ③ **도핑 유래 결합 둘 다 강건: BS₃ + P–O 온전, 금속성 LiB·Li₂O 미실현 — 매몰 기하 한정** (이 study의 고유 발견; 노출 종단은 아래 ✅ 참조)
- **B–S coord 3.00 → 3.00** (9/9 run) — 주변 PS₄가 풀리는 동안에도 붕소는 황 우리를 유지 → **금속성 LiB 안 생김**. (B–Li 1–2는 B–S 온전 상태의 Li 배위 = 합금 아님.)
- **O–P coord 1.00 → 1.00** (3/3 seed) — **phosphate P–O도 하나도 안 끊김 → Li₂O 안 생김.** (O–Li 2.0→2.0–2.7은 단순 Li 배위.)
- → **열역학 worst-case(B³⁺→BP/LiB, Li₂O)가 100 ps 동역학에서 전부 미실현** = ESW 축소(0.90→0.31 V)의 주범인 환원측 flag를 kinetics가 완화함을 자체 데이터로 입증. 분해는 오직 host P–S 채널로만 진행 (속도는 무도핑과 동일). ICOHP(B–S −7.8/P–O −8.6 = 최강 결합)·site-PDOS(깊은 상태)와 정합.
- ✅ **조건 해소 (2026-07-09, 종단 roll-scan 완결 → `interface_termination_scan.csv` + campaign 문서 §5)**: 위 결론은 **매몰-도판트 기하(B 37.8/45.3 Å)**의 결과가 맞음. B를 표면 1.5 Å에 노출한 재시험에서 **B는 직접 접촉 시 실제로 리튬화**(B–S 3.00→1.50, B–Li→5.0–5.5; 2/2 seed) — 그러나 같은 cleave 무도핑 통제(표면 P) 대비 **host가 2.6× 보호되고(PS₄ 손실 8±2 vs 22±0%) Li 침투가 정지**(−0.5 vs +4) → worst-case의 "실현"이 곧 **희생 방패**로 작동. 매몰 B는 O-노출 기하에서도 3.00→3.00(3번째 확인). **정리: 매몰 = 생존자, 노출 = 방패 — 어느 쪽도 악화가 아님.**

### ④ Li 침투는 표면 국한
양쪽 모두 100 ps에 **+7원자 수준**, 깊은 침투 없음 — 초기 SEI가 표면에서 형성되는 그림과 정합.

### ⑤ 방법론 교훈: **셀-두께 artifact** (재현 캠페인이 잡아낸 것)
같은 무도핑 물질인데 얇은 1× 슬랩(P 5개)은 48±8%, 2× 프레임은 26±0% 분해로 나옴(1.9×) — 계면 반응층이 전체 P 평균을 지배해서. **예비 단일시드의 "6× 억제" 주장은 이 artifact + 50 ps 조기 스냅샷이었고 철회됨.** 계면 비교는 반드시 같은-두께·같은-프레임 통제 필요.

## 2. 열역학 ↔ 동역학 한 표

| | 평형(ESW/hull) | 계면 MD (이 연구) |
|---|---|---|
| 예측/관찰 | Li-metal에서 **금속 LiB·BP·Li₂O** 생성 → 악화 | **BS₃·P–O 온전, LiB/Li₂O 안 생김** |
| 분해 정도 | (속도 정보 없음) | doped ≈ undoped, 표면 국한 |
| 의미 | 무한시간 하한 (비관적) | 실제 반응 경로 (passivation 쪽) |

→ 논문 논리: *"열역학 창은 좁아지나(환원측 B), 그 worst-case는 동역학에서 실현되지 않으며(BS₃·P–O 강건), 분해 kinetics는 무도핑과 동등하다."*

## 3. 이 결과가 "무엇이 **아닌가**" — 오해 방지 2가지

### 3.1 산화안정성 향상이 아니다 (이건 **환원측** 결과)
Li metal = 가장 **환원적인** 환경(0 V). B–S/P–O가 버틴 건 환원측 이야기고, **산화**(전자를 뽑는 고전압측)는 ESW ox onset·VBM이 정한다 — 그쪽은 도핑 전후 **동등**(onset 2.14→2.03 V, VBM=S 3p·free-S 불변).

| | vs 무도핑 | vs 열역학 예측(자기 자신) |
|---|---|---|
| **산화측** (고전압) | **동등** (onset 2.03 vs 2.14 V, 취약 사이트 free-S 그대로) | — |
| **환원측** (Li metal) | **동등** (host 분해 속도 같음) | **예측보다 좋음** (LiB·BP·Li₂O 미실현) |

→ 정확한 주장: **"전기화학 안정성을 개선하지도 훼손하지도 않는다 + 도판트 유래 추가 패널티가 실제로 없다."** ("향상"으로 쓰면 ESW 창 축소 0.90→0.31 V로 반격당함.)

### 3.2 종단이 보호 모드를 결정: **매몰이면 생존자, B-노출이면 방패** (2026-07-09 종단 스캔으로 업데이트)
원 기하(매몰)에서는 방패가 아니었다 — host PS₄ 분해가 무도핑과 **동일**(22±9 vs 26±0%). 문헌의 "도핑=방패" 3메커니즘과 대조:

| 방패 메커니즘 (문헌) | 원리 | 매몰 기하 (원 캠페인) | B-노출 종단 (roll-scan) |
|---|---|---|---|
| ① 희생 분해 → 절연 필름 (LiF, Li₃BO₃) | 도판트가 **먼저 분해**되며 전자차단막을 깔아 self-limiting | 미작동 — BS₃·P–O가 안 분해되니 필름 재료를 안 내놓음 | **작동 실증** — B 리튬화(B–Li→5.0–5.5) 후 host 보존 2.6×·Li 침투 정지 |
| ② host 결합 강화 | 도판트가 host 골격 결합의 장벽을 올림 | 미작동 — 강화는 자기 결합만(B–S −7.8/P–O −8.6), host P–S ICOHP −6.1 불변 | 동일 (host 보호는 ①의 산물층 효과) |
| ③ 취약 사이트 치환/표면 농축 | 공격 지점(free S²⁻)을 대체·커버 | 미작동 — ~4% 희박 + O는 phosphate 코너로 감 | **부분 작동** — 최전선 자리에 P 대신 B가 서는 국소 버전 |

→ outlook 문장(업데이트): *"묽은 bulk 도핑은 도판트가 매몰된 종단에서는 방패가 아니라 불활성 생존자다(bulk doping ≠ coating). 그러나 **B가 표면에 노출된 종단은 B₂O₃/Li₃BO₃ 코팅의 희생-보호 메커니즘 ①을 국소적으로 자발 재현**한다(host PS₄ 보존 8±2 vs 22±0%, Li 침투 정지) — 코팅 전략의 타당성을 bulk-도핑 데이터가 역으로 지지."*

## 4. 논문 문장 제안
1. "Interface MD (3 seeds × 100 ps) shows the B₂O₃-doped electrolyte decomposes at the same rate as the undoped frame at a Li-metal contact (PS₄ retention 78±9 vs 74±0%), i.e., doping does not compromise interfacial stability."
2. "Both doping-derived bonds survive Li-metal contact intact (B–S 3.00→3.00, O–P 1.00→1.00 in all seeds); neither metallic LiB nor Li₂O forms — the thermodynamic worst-case reduction is kinetically suppressed, and decomposition proceeds only through the host P–S channel."
3. "B₂O₃ doping neither improves nor degrades electrochemical stability: oxidation onset and the vulnerable free-S site are unchanged, and interfacial decomposition kinetics match the undoped electrolyte."
4. "A thin-slab control revealed a ~2× cell-size artifact in interfacial decomposition metrics, underscoring the need for same-frame controlled comparisons."
5. "A termination scan shows the protection mode is geometry-dependent: buried dopants remain inert spectators (decomposition kinetics equal to undoped), whereas a B-exposed termination undergoes sacrificial lithiation (B–S 3.00→1.50, B–Li→5.0–5.5) that protects the host — PS₄ loss drops to 8±2% versus 22±0% for the P-exposed undoped control at the same cleave, and Li penetration is arrested. In no tested geometry does doping degrade the interface."
6. "A clean-build front-line test (cleave-integrity audited) shows that even the strongest dopant-derived bond is not immune at direct metallic contact: an exposed PS₂O₂ tetrahedron loses both intact P–O bonds within 100 ps (exposed O ending in a Li₂O-like environment) and degrades faster than the intact-PS₄ control at the same depth (34±2% vs 22±3% P–S loss). The front-line hierarchy — B-fronted 8% ≪ PS₄ ~22% ≲ PS₂O₂ ~34% — establishes that protection at a Li-metal contact arises only from burial or from a sacrificial product that stays anchored at the interface (realized only by B)."

## 5. 정직한 한계
- **100 ps = 초기 단계**: 양쪽 다 분해 진행 중(미수렴) — 절대 분해량이 아니라 **비교(동등/보호)**만 인용. B-노출 방패층의 장기 자기제한 여부도 100 ps 밖.
- ~~표면 종단 1종/프레임~~ → **c-roll 종단 스캔 완결(2026-07-09)**: 매몰 원기하 + B-노출(0.51, 감사 통과 → **방패**) + 0.16(artifact 철회, `audit_cleave_bonds.py` 신설) + **0.71 clean 재시험 완결** (PS₂O₂ 34±2% vs PS₄ 통제 22±3% — O 코너 비보호·가속 방향; P–O도 접촉면 절단 = **세 게이트 전멸**, s3 per-atom 도장만 대기). 최전선 위계: **B 8 ≪ PS₄ ~22 (두 cleave 재현) ≲ PS₂O₂ ~34**. 남은 것: 종단당 n=2 seed, 측면 registry(`--shift_ab`)·a-면 슬랩 미탐색.
- MLIP 반응상(Li₃P/Li₂S) 정확도는 DFT 단발 검증 미실시(선택 과제) — "동등" 결론은 리스크 낮음; **B-노출의 Li–B–S 산물층은 MLIP 의존이 커서 "MLIP 수준" 명시하고 인용**.
- CIF 스냅샷은 seed-s2 대표 1개 (통계는 곡선/CSV가 담당).

## 6. 파일 인덱스
| 파일 | 내용 |
|---|---|
| `iface_{b2o3,modelc2x}_{0_initial,1_relaxed,2_final100ps}.cif` | VESTA 구조 스냅샷 — **논문 전/후 비교 그림용 (채택)** |
| `iface_timeseries.png` / `interface_timeseries_mean.csv` | P–S 잔존율·B–S 평탄·Li 침투 시간곡선 (3-seed mean±std) |
| `iface_MD_2p5d.gif` | 2.5D 애니메이션 (보조 자료 — 발표용 옵션, 그림은 CIF 렌더 사용) |
| `db/properties/interface_decomp_*_s*.csv` | per-frame 원자료 9개 (kgy) |
| `db/properties/interface_campaign_summary.csv` | 계별 mean±std 집계 (매몰 기하 캠페인) |
| `db/properties/interface_termination_scan.csv` | 종단 roll-scan 8 run (B-노출/O-노출 + 통제, per-seed) + 판정 주석 |
| `docs/figures/oxidation/interface_campaign_controlled.png` | 통제비교 요약 그림 |
| 관련 kb | `b2o3_anode_interface_campaign_2026_07_07.md`(확정), `..._MD_dynamics_2026_07_06.md`(예비, superseded), `b2o3_anode_interface_2026_06_30.md`(열역학) |
