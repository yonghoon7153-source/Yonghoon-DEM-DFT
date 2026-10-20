# 원고 · SI 수정 체크리스트 — σ_e 앵커 교체 · DBE SDCP 1 µm 덩어리 · σ₀ 결정 대기 (2026-10-19)

> ★ 10-19 C 결정 (1저자) = 등록 v2 §3-D — LPSCl σ_ion 7.45 × 10⁻⁴ · SDCP 이온 σ 2.48 × 10⁻⁴ S/cm (Bazzoun 2026 · CAM 70 wt% EIS 0.137 mS/cm 앵커) · C 칸은 그 규칙대로 (SBE σ_ion 0.137 · 옛 DBE 침대 0.138 · 새 DBE 침대 = 최종 16 팔).


목적: 1저자 10-19 결정으로 바뀌는 원고 · SI 자리를 한곳에 표시한다 (A 앵커 교체 · B DBE 재압밀 · C σ₀ · D 파생 문장).
입력: manuscript.pdf (sha256 ffb824e4…) · si.docx (sha256 7e034a20…) 에서 뽑은 글 (리포 밖 추출본 · 원고 파일은 커밋하지 않는다) · 맥락 = 옛 등록 `docs/reviews/sdcp_sigma_e_dcp_anchor_registration_20261012.md` · 새 등록 `docs/reviews/sdcp_sigma_e_dcp_anchor_registration_v2_20261019.md` §0 · §1 · §3 · §6.
**값 나오면 일괄 수정 · 지금은 표시만** — 새 런 값은 전부 ⬜ 값 대기 · 그림 이미지 안의 글자는 추출 글에 없어 따로 확인한다.

표기: L = 원고 왼쪽 줄 번호 · 바뀌는 이유 **A** = 실험 앵커 교체 (SBE 1.63 · DBE 4.68 mS cm⁻¹ · 10-16 DC 분극) + σ_VGCF 를 SBE 에 보정 (SBE 시뮬 ≈ 1.63 은 맞춘 값 · DBE 는 예측) / **B** = DBE 침대만 SDCP 평균 1 µm 덩어리 (0.30 µm 1 차 입자) 로 재압밀 · SBE 침대 그대로 / **C** = LPSCl σ₀ (결정 대기) / **D** = 위 값에 기대는 문장 · 주장.

## 본문 (manuscript)

| # | 위치 | 지금 | 바뀌는 이유 | 새 값 출처 |
|---|---|---|---|---|
| M01 | p.8 · 결과 DEM–MPM 문단 · L252–253 "The model geometries and material parameters are summarized in Figure S15 and Table S2" | 그림 S15 · 표 S2 를 가리킴 (문장은 그대로) | B (S15 의 DBE 기하 · 표 S2 SDCP 행) · A (표 S2 VGCF 행) | SI01 · SI02–SI10 을 따라감 |
| M02 | p.8 · L254–255 "Although both electrodes retain a fully percolated electronic network through vapor-grown carbon fiber" | 두 전극 전자망 완전 연결 (표 S3 연결도 100 · 100) | B — DBE 는 재압밀 침대에서 다시 확인 | 최종 16 팔 (⬜ 값 대기) |
| M03 | p.8 · L255–256 "incorporation of SDCP increases the local density of CA … (Figure 5a)" | DBE 에서 AM 주변 CA 밀도 증가 | B · D | 최종 16 팔 · 그림 5a (⬜ 값 대기) |
| M04 | p.8 · L256–258 "When normalized to the median CA density of the SBE, 85% of the AM particles" | 85 % | B (정규화 기준 = SBE 중앙값은 그대로) | 등록 v2 §6 (a) → 최종 16 팔 (⬜ 값 대기) |
| M05 | p.8 · L258–259 "indicating that the conductive enrichment is broadly distributed throughout the electrode" | "broadly distributed … rather than confined to isolated regions" | D (B) — SDCP 개체가 ~1/24 로 줄면 국소화될 수 있음 | 최종 16 팔 결과 보고 문장 정함 |
| M06 | p.8 · L259–261 "the median number of CA contacts per AM particle increases from 74 … to 86" | 74 (SBE) → 86 (DBE) | B — DBE 86 바뀜 (덩어리 하나 = 개체 하나) · SBE 74 는 그대로 예상 | 등록 v2 §6 (b) → 최종 16 팔 (⬜ 값 대기) |
| M07 | p.8 · L260–262 "based on the number of distinct conductive entities located within a 0.15 μm shell" | 개체 수 정의 · 0.15 μm 껍질 | B — 정의는 그대로 · "SDCP 덩어리 = 개체 하나" 한 줄을 넣을지 | 등록 v2 §6 · `scripts/cbd_contacts_per_am.py` 정의 확인 필요 |
| M08 | p.8 · L262–263 "raises the simulated effective electronic conductivity (σele_eff) from 54.0 to 70.6 mS cm−1" | 54.0 → 70.6 mS cm−1 | A (SBE = 실측 1.63 에 맞춘 값 · DBE = 예측) · B (DBE 침대) · D ("raises" 는 DBE > SBE 일 때만) | SBE ≈ 1.63 (등록 v2 §1 · §3-A) · DBE ⬜ 값 대기 (§3-C → 최종 16 팔 · 방향 예측 없음 §3) |
| M09 | p.8 · L263–266 "The ionic current distributions remain comparable … larger number of parallel pathways (Figures S16 and S17)" | 이온 분포 비슷 · DBE 전자 병렬 경로 많음 | A (전자 장 — σ* · NCM σ 로 SBE 도 바뀜) · B (DBE) · C (결정 대기 — 이온 장 크기만 · SBE 는 정확히 비례 · DBE 는 SDCP 이온 σ (Q2) 에 따라 근사) · D | 최종 16 팔 LEAN=4 (⬜ 값 대기) · σ₀ = 결정 대기 |
| M10 | p.8 · L266–270 "SDCP does not merely add an electronically conductive binder phase … without compromising Li+ conduction" | 접촉 증가 · 전류 재분배 · Li⁺ 전도 손실 없음 | D (B · C 결과에 따라) | 최종 16 팔 뒤 문장 정함 |
| M11 | p.9 · L271–276 "The simulation-derived improvement … was experimentally verified … consistent with the enhanced σele_eff predicted" | Rele 59.7 → 48.5 Ω cm² (실험 · 그대로) ↔ "predicted" | A · D — SBE 는 이제 실측에 맞춘 값 · 비교가 되는 것은 DBE 예측 ↔ 4.68 뿐 | 등록 v2 §1 (1.63 · 4.68 · 비 2.86) · §4 한정어 |
| M12 | p.9 · 같은 문단 (추가 후보) | 전극 σ_e 실측값이 본문에 없음 | A — 10-16 DC 분극 SBE 1.63 · DBE 4.68 mS cm⁻¹ (2 전극 · 지름 10 mm · 두께 90 · 80 µm) 를 본문에 넣을지 | 등록 v2 §1 (값 있음) · 1저자 결정 |
| M13 | p.10 · L322–325 "consistent with the greater density and broader distribution of conductive contacts predicted" | GITT 1.33 (실험 · 그대로) ↔ 시뮬 접촉 예측 | D (M04–M06 새 값에 따라) | 최종 16 팔 뒤 문장 정함 |
| M14 | p.12 · 결론 L391–393 "Microstructural simulations and transport analyses reveal that SDCP increases conductive contacts" | 접촉 증가 · 병렬 경로 · Li⁺ 전도 손실 없음 | D (B · C) | 최종 16 팔 뒤 문장 정함 |
| M15 | p.14 · Experimental "Electrochemical measurements" L448–450 "and their σele by DC polarization at 0.5 V for 30 min" | 바인더–LPSCl 혼합물 DC 분극만 기술 | A — 보정 기준이 된 전극 DC 분극 방법 추가 필요 (2 전극 · 지름 10 mm · ±5–20 mV 8 점 I–V · 600 s 유지의 끝 60 s 평균 · 두께 90 · 80 µm) | 등록 v2 §1 (측정 압력 · 온도 · 두께를 잰 상태 = 등록에 없음 → 1저자) |
| M16 | p.16 · Methods L510–514 "compacted to a final electrode thickness of 72.5 μm" · L524–525 "333 × 333 × 484 voxels (5.4 × 107 in total)" | 72.5 μm · 격자 칸 수 (두 침대 공통) | B — DBE 재압밀 뒤 정지 두께가 같은지 확인 필요 (다르면 z 칸 수 · 총수 바뀜) | 등록 v2 §3-B R2 (⬜ 값 대기) |
| M17 | p.16 · Methods L521–522 "VGCF fibers, PTFE fibrils and SDCP particles were then seeded into the pore space" | "SDCP particles" (Ø0.30 μm 낱알) | B — DBE: 0.30 µm 1 차 입자의 평균 1 µm 덩어리 (볼밀 뒤 SEM) · 내부 채움 0.64 · NCM 부착 몫 0.5 (둘 다 가정) | 등록 v2 §0 · §3-B · §4 (덩어리 수 · 1 차 입자 수 = R2 ⬜ 값 대기) |
| M18 | p.16 · Methods 전도도 문단 L522–532 근처 (추가) | σ_VGCF 보정 서술 없음 (표 S2 는 78.5 "Calculated") | A — "VGCF 복셀 σ 를 SBE 실측 1.63 mS cm⁻¹ 에 맞춤 (1 점 보정) · DBE 는 예측" 추가 | 등록 v2 §0 · §3-A (σ* ⬜ 값 대기) |
| M19 | p.16 · Methods L535–537 "ratios are reported as the mean over the eight origin-matched SBE/DBE pairs … (0.08%)" | 쌍 산포 0.08 % · "ratios are reported" | A · B (새 런의 산포) · D (본문 · SI 에 비 숫자가 없음) | 최종 16 팔 (⬜ 값 대기) |
| M20 | p.16–17 · Methods L537–541 "The ohmic loss carried by each phase was evaluated as" (식 3) | 상별 옴 손실 정의 — 결과 숫자는 글에 없음 | 확인 필요 — 그림에 상별 몫이 있으면 A · B 로 바뀜 · 어디에도 없으면 문단 정리 검토 | 최종 16 팔 LEAN=4 (⬜ 값 대기) |
| M21 | p.25 · Figure 5 캡션 (a) "Electronic conduction networks … colored according to the local CA density around each AM particle" | 그림 5a 지도 | B (DBE 지도 · SBE 정규화 기준 그대로) | 등록 v2 §6 (a) → 최종 16 팔 (⬜ 값 대기) |
| M22 | p.25 · Figure 5 캡션 (b) "Distributions of CA contacts per AM particle and the effective σele obtained from the simulations" | 그림 5b (74 · 86 분포 · 54.0 · 70.6 막대) | A · B — 캡션에 "SBE = 실측 보정 · DBE = 예측" 표시 · 실측 1.63 · 4.68 표식을 넣을지 | 등록 v2 §6 (b) → 최종 16 팔 (⬜ 값 대기) · 1저자 |
| M23 | p.25 · Figure 5a · 5b 이미지 안 글자 | 추출 글에 없음 — 85 % · 74 · 86 · 54.0 · 70.6 · σ 축 범위가 그림 안에 있는지 모름 | A · B — 확인 필요 | 최종 16 팔 (⬜ 값 대기) |
| M24 | p.6 · L188–192 "initially micrometer-sized SDCP particles are fragmented into finer domains" · "no discernible large agglomerates" | 실험 SEM 서술 (크기 숫자 없음) | D — 모델이 "~1 µm 덩어리 (agglomerate)" 로 바뀜 → 낱말 충돌 · SEM 크기 한 줄로 모델과 잇기 검토 | 등록 v2 §0 (1저자 판독 0.8–1.3 µm · 만든 직후 = Figure S1 수 µm) |
| M25 | p.17–20 · 참고문헌 | σ₀ 문헌 앵커 없음 | C (결정 대기) — 문헌 앵커 σ₀ 를 쓰면 새 문헌 (후보 Bazzoun 2026, J. Power Sources 661, 238682 — 값은 litdb 정본 카드에서) 추가 | 결정 대기 (등록 v2 §3-D) |

## SI

| # | 위치 | 지금 | 바뀌는 이유 | 새 값 출처 |
|---|---|---|---|---|
| SI01 | [SI ¶56] Figure S15 "Constructed SBE and DBE geometries used for the DEM–MPM simulations" | DBE 기하 그림 | B (DBE 그림 다시 · SBE 그대로) — 등록 v2 §6 목록에 없음 | R2 뒤 새 DBE 침대 (⬜ 값 대기) |
| SI02 | [SI ¶57] 표 S2 캡션 "Parameters marked "Calibrated" were adjusted such that the compacted packing reproduces …" | "Calibrated" = 압밀 보정만 뜻함 | A — σ_VGCF 도 "Calibrated" 가 됨 (기준 = SBE DC 분극 1.63 mS cm⁻¹) → 두 보정을 나눠 적기 | 등록 v2 §6 (표 S2 문구) |
| SI03 | [SI ¶57] 표 S2 캡션 "PTFE was seeded as drawn fibrils …" 뒤 (추가) | SDCP 시딩 설명 없음 | B — SDCP 덩어리 시딩 한 문장 (1 차 0.30 µm · 평균 1 µm · 채움 0.64 · 부착 0.5 가정) | 등록 v2 §3-B · §4 |
| SI04 | [SI 표 2 행 13] LPSCl · Ionic conductivity · 3.0 × 10−3 S cm−1 · Ref. S4 | 3.0 × 10⁻³ · Ref. S4 | C (결정 대기) — 10-12 보고 기준 1.5 × 10⁻³ 또는 문헌 앵커 유효 bulk · 출처 칸도 바뀜 | 결정 대기 (등록 v2 §3-D Q1) |
| SI05 | [SI 표 2 행 16] VGCF · Electronic conductivity (compressed powder) · 1.0 × 102 · Ref. S9 | 100 S cm⁻¹ · Ref. S9 | A — 모델 입력이 아니게 됨 → 행 삭제 또는 "참고" 지위 · S9 가 100 을 받치는지 대조 확인 필요 (`CL-47` 정정: 출처 없이 넣은 값) | 1저자 결정 |
| SI06 | [SI 표 2 행 17] VGCF · Electronic conductivity (voxel, diameter-preserving) · 78.5 · Calculated | 78.5 S cm⁻¹ · Calculated | A — σ* (복셀 유효값) · 출처 "Calibrated (SBE DC polarization)" · "diameter-preserving" 문구 정리 | 등록 v2 §3-A S2 (⬜ 값 대기) |
| SI07 | [SI 표 2 행 20] SDCP · Particle diameter · 0.30 μm · Measured | 0.30 μm · Measured | B — "1 차 입자 0.30 µm · 덩어리 평균 1 µm (SEM)" · 등록 v2 §0 의 "원고 Figure 2f · S5" 는 이 판 번호와 다름 (이 판: 볼밀 뒤 = Figure 3c · 만든 직후 = Figure S1) — 확인 필요 | 등록 v2 §0 · §6 |
| SI08 | [SI 표 2] SDCP 새 행 후보 | (없음) | B — 덩어리 평균 지름 1 µm · 내부 채움 0.64 (Assumed) · NCM 부착 몫 0.5 (Assumed) 행을 넣을지 | 등록 v2 §3-B · §4 · 1저자 |
| SI09 | [SI 표 2 행 21] SDCP · Young's modulus · 9.0 GPa · Measured | 9.0 GPa | 확인 필요 (B) — 재압밀은 옛 kit_DBE 와 "같은 세대" 로 돈다 · 그 침대가 실제 쓴 SDCP E 가 9.0 인지 R0 로 확인 (`CL-56`: 08-12 침대는 SDCP 23.6 · VGCF 10 · PTFE 0.3 GPa — 행 15 · 18 도 같은 대조) | 등록 v2 §3-B R0 · R2 (⬜ 값 대기) |
| SI10 | [SI 표 2 행 23] SDCP · Ionic conductivity · 1.0 × 10−3 · Assumed | 1.0 × 10⁻³ S cm⁻¹ | C (결정 대기) — Q2: σ₀ 와 같은 비로 낮출지 | 결정 대기 (등록 v2 §3-D Q2) |
| SI11 | [SI ¶59] 표 S3 캡션 "Structural and transport parameters obtained from the DEM simulations." | 캡션 | A · D — "SBE σele = 실측 보정 · DBE = 예측" 표시 · 값 출처 낱말 (DEM–MPM + 복셀 풀이) 확인 필요 | 등록 v2 §6 |
| SI12 | [SI 표 3 행 2] Thickness · 72.53 / 72.53 µm | 72.53 · 72.53 | SBE 그대로 · DBE = B (재압밀 정지 두께 확인 필요) · §6 목록에 없음 | 등록 v2 §3-B R2 (⬜ 값 대기) |
| SI13 | [SI 표 3 행 3] Porosity · 7.86 / 7.37 % | 7.86 · 7.37 | SBE 그대로 · DBE = B — 등록 v2 §6 목록에 없음 | R2 · 최종 침대 (⬜ 값 대기) |
| SI14 | [SI 표 3 행 4] SE coverage of AM · 86.6 / 86.6 % | 86.6 · 86.6 | SBE 그대로 · DBE = B (재압밀로 바뀔 수 있음 — 확인 필요) · §6 목록에 없음 | 최종 침대 (⬜ 값 대기) |
| SI15 | [SI 표 3 행 5] CA coverage of AM · 13.1 / 15.5 % | 13.1 · 15.5 | SBE 그대로 · DBE = B · §6 목록에 없음 | 최종 16 팔 (⬜ 값 대기) |
| SI16 | [SI 표 3 행 6] Median CA contacts per AM · 74 / 86 | 74 · 86 | SBE 74 그대로 (예상) · DBE = B (덩어리 = 개체 하나) | 등록 v2 §6 (b) → 최종 16 팔 (⬜ 값 대기) |
| SI17 | [SI 표 3 행 7] Electronic connectivity · 100 / 100 % | 100 · 100 | SBE 그대로 · DBE = B | 최종 16 팔 (⬜ 값 대기) |
| SI18 | [SI 표 3 행 8] Current-focusing factor, electronic · 79.5 / 71.5 | 79.5 · 71.5 | A (SBE 도 바뀜 — σ* · NCM 4.1 × 10⁻³ 로 전류 장이 바뀜) · B (DBE) | 등록 v2 §6 → 최종 16 팔 LEAN=4 (⬜ 값 대기) |
| SI19 | [SI 표 3 행 9] σele_eff · 54.0 / 70.6 mS cm−1 | 54.0 · 70.6 | A · B — SBE ≈ 1.63 (맞춘 값) · DBE = 예측 (옛 값은 σ_VGCF 78.5 · NCM 0.01 · SDCP 250 으로 계산 — 옛 등록 §0) | 등록 v2 §1 · §3-A · §3-C → 최종 16 팔 (⬜ 값 대기) |
| SI20 | [SI 표 3 행 10] σion_eff · 0.553 / 0.558 mS cm−1 | 0.553 · 0.558 | C (결정 대기) — σ₀ 1.5 면 SBE ≈ 0.28 (비례) · 문헌 앵커면 그 값 · DBE 는 B 도 | 등록 v2 §3-D · 최종 16 팔 (⬜ 값 대기) |
| SI21 | [SI ¶62] Figure S16 "Simulated ionic current density distributions in the SBE and DBE" | 이온 전류 밀도 그림 | C (결정 대기) — 색 눈금 크기 (균일 σ₀ 보정은 모양을 안 바꿈 · SBE 정확 · DBE 는 Q2 에 따라) · B (DBE 지도) | 등록 v2 §3-D · §6 → 최종 16 팔 (⬜ 값 대기) |
| SI22 | [SI ¶64] Figure S17 "Simulated electronic current density distributions in the SBE and DBE" | 전자 전류 밀도 그림 | A (SBE 도 바뀜) · B (DBE) | 등록 v2 §6 → 최종 16 팔 (⬜ 값 대기) |
| SI23 | [SI ¶100] Ref. S4 (Cronau 2021) | 표 S2 행 13 · 캡션의 출처 | C (결정 대기) — σ₀ 출처가 바뀌면 행 13 에서 빠짐 (캡션 [S4] 는 남음) · 문헌 앵커면 새 문헌 추가 | 결정 대기 |
| SI24 | [SI ¶105] Ref. S9 (Endo 2001) | 표 S2 행 16 출처 | A — 행 16 을 지우면 안 쓰이는 문헌 → 번호 정리 | 1저자 결정 (SI05 와 같이) |
| SI25 | SI 추가 후보 — 전극 DC 분극 원자료 | (없음) | A — SBE R 7.016 Ω · DBE R 2.178 Ω (8 점 I–V) · 두께 · 지름 그림 또는 표를 SI 에 넣을지 | 등록 v2 §1 (값 있음) · 1저자 |

참고 — 등록 v2 의 그림 번호는 이 판과 다르다: §0 "원고 Figure 2f · S5" (이 판 2f = LPSCl 혼합물 σele · S5 = 순수 NCM SEM · SDCP 가 보이는 SEM = Figure 3c) · §6 "전류 밀도 그림 S14 · S15" (이 판 = S16 · S17).  등록 문서를 고칠 때 같이 맞춘다.

## 문장 · 주장 점검 (값에 따라 표현을 바꿀 수 있는 곳)

1. **CA 밀도 · 접촉 증가 (M03–M06 · M13 · M14)** — 같은 SDCP 부피가 ~24 배 적은 개체로 모인다 (등록 v2 §6 산술).  덩어리를 못 받은 AM 은 SBE 와 비슷해져 85 % 가 내려가고, 74 → 86 증가 폭이 줄 수 있다 (추정).  값이 나오면 "increases" · "broadly distributed" 를 그대로 둘지 정한다.
2. **"raises … from 54.0 to 70.6" (M08)** — SBE 는 이제 실측에 맞춘 값이다.  "SBE 를 실측 1.63 에 보정 → DBE 예측 X (실측 4.68)" 꼴로 바꾼다.  "모델이 실험을 재현" 은 쓰지 않는다 (보정 1 점 + 비교 1 개 · 측정 n = 1 · 2 전극 — 등록 v2 §4).
3. **"experimentally verified" · "consistent with … predicted" (M11)** — 실측 DC 비 2.86 과 TLM Rele 비 1.23 (59.7 / 48.5, 산술) 은 서로 다르다 → "방향 일치" 까지만 쓴다.  실측 비 2.86 에는 PTFE 1 → 0.5 wt% 몫도 들어 있다 — DBE–SBE 차이를 SDCP 로만 돌리지 않는다 (등록 v2 §4 · 모델 DBE 도 PTFE 0.5 wt%).
4. **병렬 경로 · 전류 집중 (M09 · SI18)** — σ* 는 옛 등록의 3.41 S cm⁻¹ 보다 낮다 (앵커가 4.47 → 1.63).  SDCP (256.6) ↔ VGCF σ 대비가 옛 ≈ 3 배에서 75 배 이상 (산술) 으로 커져 DBE 전류가 SDCP 덩어리로 몰릴 수 있다 → 79.5 > 71.5 순서와 "larger number of parallel pathways" 가 뒤집힐 수 있다 (추정 · 값 대기).
5. **"without compromising Li+ conduction" (M10 · M14)** — DBE σ_ion 은 재압밀 침대에서 다시 나온다 (옛 0.558 vs 0.553).  σ₀ 를 낮추고 (예: 문헌 앵커 어림 0.74 mS cm⁻¹ · 판정 아님) SDCP 이온 σ (1.0 mS cm⁻¹ 가정) 를 그대로 두면 SDCP 가 SE 보다 이온을 잘 나르는 꼴이 되어 이 문장을 근거 없이 받친다 → Q1 · Q2 를 같이 정한다.
6. **σ₀ 와 실측 3.57 mS cm⁻¹ (C)** — p.6 L175 의 순수 LPSCl EIS 3.57 mS cm⁻¹ (이 연구 측정) 과 다른 σ₀ 를 모델에 넣으면, Methods 에 "복셀 모델에 접촉 · 입계 저항 항이 없어 유효 bulk 값으로 낮춤" 같은 한 줄이 필요하다 (`CL-81`).
7. **SDCP 크기 낱말 (M17 · M24 · SI07)** — 모델 "~1 µm agglomerate" ↔ 본문 "fragmented into finer domains" · "no discernible large agglomerates" (L189–192) · "finely dispersed SDCP" (L229).  같은 낱말로 맞춘다.  원고 SEM 의 0.2–0.5 µm 판독과 1 µm 의 공존은 미해결이다 (등록 v2 §4).
8. **비 보고 (M19)** — Methods 는 "ratios are reported as the mean over the eight … pairs" 라 적는데 본문 · SI 에 비 숫자가 없다 → 새 값 때 비를 같이 적거나 문장을 정리한다.
9. **두께 · 측정 조건 (M15 · M16)** — 모델 두께 72.53 µm (두 침대 공통) ↔ 실측 시료 SBE 90 · DBE 80 µm.  σ 는 두께와 무관한 양이라 보정에는 문제없지만, DC 값을 적을 때 두께 · 2 전극 (지그 · 리드 · 접촉 포함) 을 함께 적는다.
10. **낮음 — 그대로 둘 가능성이 큰 곳** — 초록 L35 · 서론 L110 · L127 · 결론 L391 의 "electronic connectivity" 와 TOC L729 "reinforces the electronic network that PTFE alone disrupts" 는 실험 (Rele · SSRM · KPFM) 근거다.  p.8 L248–250 "expected to provide an additional benefit" 도 틀만 있다.  시뮬 결과와 어긋나지 않는지만 본다.

## 건드리지 않는 것

- **SBE 침대 기하 값** — 표 S3 의 SBE 두께 72.53 · 기공 7.86 · SE coverage 86.6 · CA coverage 13.1 · 접촉 74 · 연결도 100: SBE 침대가 그대로이고 σ 와 무관한 기하 (최종 런 출력으로 같은지만 확인).
- **DEM 골격 · 압밀 보정** — 1,271 NCM811 · 146,420 LPSCl · r 2.5 / 0.5 μm · 70:27 · 50 × 50 μm² · Hookean · 표 S2 행 4 · 7–12 (E 1.35 · ν 0.3 · E 1.53 · ν 0.49 · σ_y 0.30): 두 침대 공통 골격이고 재압밀은 SDCP 크기 한 가지만 바꾼다 (등록 v2 §3-B R1).
- **고정 풀이 설정** — 복셀 0.15 μm (표 S2 행 3) · 50 × 50 μm² (행 2) · VGCF 지름 0.15 (행 14) · 1 V · 조화평균 전도 · 식 (2) · origin 8 개 (2 × 2 × 2) · PTFE centerline 원섬유 설명 (캡션 · 행 18–19): 등록 v2 §2 고정 · PTFE 표현 바꿈은 1저자의 다음 단계 결정 때 다시.
- **표 값이 이미 새 런과 같은 행** — NCM811 σ_e 4.1 × 10⁻³ (행 6 · Ref. S6) · SDCP σ_e 256.6 (행 22 · Measured): 값 그대로.  옛 표 S3 은 코드 0.01 · 250 으로 돌았고 새 런부터 표와 같은 값으로 돈다 (옛 등록 §0 · 등록 v2 §2).
- **기계 물성 (SDCP 크기와 무관)** — NCM E 140 (행 5) · VGCF E 100 (행 15) · PTFE E 1.8 (행 18): 그대로 (침대가 실제 쓴 E 대조만 SI09 와 같이 · `CL-56`).
- **Methods 역할 문장** — L531–532 "NCM811, VGCF and SDCP carried the electronic network and LPSCl and SDCP the ionic network": 문장 그대로 · SDCP 이온 σ 값만 C (SI10).
- **실험 · DFT 수치 전부** — SDCP 256.6 S cm⁻¹ · 206.2 Ω sq⁻¹ · 189 nm · DC 0.30 / 0.12 / 1.53 × 10⁻⁷ S cm⁻¹ · EIS 3.57 / 0.97 / 2.86 mS cm⁻¹ · AFM 9.0 / 1.8 GPa · SAICAS · 탄성 회복 · Rele 59.7 / 48.5 / 42.6 · 표 S4 · S5 · GITT 1.33 · 거칠기 · Wa · 용량 · 사이클 · XRD · DFT (표 S1 · −0.96 / −0.79 eV · 1.83 / 2.54 Å): 측정 · DFT 값이라 이번 변경과 무관.
- ⚠ **찾아 바꾸기 금지 (숫자만 같음)** — p.6 L176 "2.86 mS cm−1 with SDCP" (EIS σ_ion) = 새 DC 비 2.86 과 같은 숫자 · [SI 표 5 행 7] DBE@C-SUS Rint 12.4 Ω cm² = 옛 앵커 12.4 와 같은 숫자 · p.6 L172 "0.30 × 10−7" 과 표 S2 행 12 σ_y 0.30 GPa = SDCP 지름 0.30 과 같은 숫자 · p.6 L173 "1.53 × 10−7" 은 새 SBE 1.63 과 비슷한 숫자.
- **옛 앵커 · 옛 비 · 없는 낱말** — 4.47 · 12.4 mS cm⁻¹ · σ* 3.41 · 비 1.24 / 1.31 / 1.3078 / "+31 %" · ionic tortuosity · SDCP "bridge" 주장: 원고 · SI 글에 없다 (검색 0 건 · "bridge" 는 화학 ethylenedioxy bridge 뿐) → 지울 곳 없음 (그림 이미지 안은 M23 에서 확인).
- **실험 · 모식도 그림** — Figure 1–4 · 5c · 5d · 6–8 · S1–S14 · S18–S28: 실험 · 모식도라 그대로 (Figure 3c · S1 은 SDCP 1 µm 의 근거로 인용될 수 있음 — SI07).
- **별건 (이번 범위 밖)** — p.16 L515–517 "~10% porosity and 11–12% contact overlap reported for cold-pressed LPSCl at 300 MPa.[9]" · 표 S2 캡션 [S4]: A–D 와 무관 · 출처는 원장 `CL-94` (hold) 에서 따로 본다.

## 값 채움 (10-20 · final16 SBE + final8 DBE)

> 1저자 10-20: *"서술 같은건 내가 알아서 할거야 · 사족 달지마"* — 자리마다 {옛 값 → 새 값 · 근거} 만.
> 원천: ① final16 SBE 8 팔 (σ_VGCF 0.347 · 등록 v2 §7 09:49 줄 · kgy `~/sdcp/final16_1019_collect.json`) · ② final8 DBE 8 팔 (σ_VGCF 2.618 · §7 18:59 줄 · `~/sdcp/final8_dbe_vgcf2618_collect.json`) ·
> ③ 웹앱 :5002 ⚖ 비교 a0 두 팔 (10-20 19:2x · 1저자 화면 · A = SBE final16 a0 · B = DBE final8 a0 · 팔 (0,0,0) · 코호트 평균 아님).
> σ = ①② 8 팔 평균 · 침대 값 (두께 · 기공 · 덮임 · 연결도 · 탄소 성분 수) = ③ (STEP3 origin 과 무관한 침대 계산 · 8 팔 같음 확인 = 조각 ②) · 지도 · 그림 = ③ a0.  ⬜ = kgy 에서 뽑을 값.

### 본문

| # | 옛 값 → 새 값 | 근거 |
|---|---|---|
| M02 | 전자 연결도 100 · 100 % → 100 · 100 % | ③ `econn_summary.connected_pct` |
| M03 | (문장에 숫자 없음) · 그림 5a 양 (AM 근접 점유량 중앙값 · 접점 아님) 438 → 522 → 438 → 485 (+10.5 %) | ③ · 옛 = Table S3 원장 §10-3 |
| M04 | 85 % → ⬜ (새 DBE 접점 중 SBE 중앙값 74 초과 비율) | 옛 85 % = 개체 접점 0.15 µm 1083/1271 = 85.2 % (`docs/data/cbd_contacts_20260831/` 로 다시 계산해 같음) |
| M05 | (M04 값) → ⬜ | M04 |
| M06 | 74 → 86 → 74 → ⬜ | SBE = 같은 침대 · `docs/data/cbd_contacts_20260831/contacts_SBE_band015.json` 중앙값 74 |
| M07 | 0.15 µm 껍질 · 개체 수 → 그대로 · 새 DBE 의 SDCP 개체 = 덩어리 하나 | `scripts/additives.py:709–713` |
| M08 | 54.0 → 70.6 → **1.62 → 4.73** mS cm⁻¹ (8 팔 1.6209 · 4.7287) · 실측 1.63 · 4.68 | ①② |
| M09 | 두 안 — 아래 표 | ③ |
| M10 | σion 0.553 · 0.558 → 0.137 · 0.138 mS cm⁻¹ (0.13704 · 0.13823 · 비 1.0087) | ①② |
| M11 | Rele 59.7 → 48.5 Ω cm² (실험 · 그대로) · "predicted" σele → DBE 4.73 = 보정값 (DC 4.68) | ② · §7 15:47 |
| M12 | (없음) → DC σele SBE 1.63 · DBE 4.68 mS cm⁻¹ (2 전극 · Ø10 mm · 90 · 80 µm) | 등록 v2 §1 |
| M13 | (M04–M06 값) → ⬜ | M04–M06 |
| M14 | (M04–M06 · M09 · M10 값) → ⬜ · M10 = 1.0087 | M04–M10 |
| M15 | (없음) → 2 전극 · Ø10 mm · ±5 · 10 · 15 · 20 mV 8 점 · 600 s 유지의 끝 60 s 평균 · R 7.016 · 2.178 Ω (r² 0.999999 · 0.99993) · 두께 90 · 80 µm · 압력 · 온도 · 두께 잰 상태 [미확인] | 등록 v2 §1 · `docs/data/sdcp_dc_polarization_20261016/README.md` |
| M16 | 72.5 µm · 333 × 333 × 484 → 72.53 · 72.53 µm · 격자 그대로 (vox 0.15 · 두께 같음) | ③ `mpm_metrics.thickness_mpm_um` · §7 R1 시도 5 줄 |
| M17 | SDCP Ø0.30 µm 낱알 → DBE: 0.30 µm 1 차 입자의 평균 1 µm 덩어리 · 덩어리당 24 · 내부 채움 0.64 (가정) · NCM 부착 몫 0.5 (가정 · 실현 몫 ⬜) · 시딩 점 138,988 → 116,532 | §7 R1 · R2 |
| M18 | (없음) → σ_VGCF SBE 0.347 (DC 1.63) · DBE 2.618 (DC 4.68 · 사다리 점 · S2 보간 2.54) S cm⁻¹ · ×7.54 · LPSCl σ₀ 7.45 × 10⁻⁴ (Bazzoun 0.137 mS cm⁻¹) · SDCP 이온 2.48 × 10⁻⁴ S cm⁻¹ | §7 S2 · 15:21 · 15:47 · §3-D |
| M19 | 짝 산포 0.08 % → σ_e 짝 비 2.917 (a0–a6 짝 7 · sd 0.010 = 0.35 % · 8 짝 ⬜) · σ_ion 비 1.0087 (평균의 비 · 8 짝 ⬜) | §7 09:07 · 18:59 |
| M20 | (글에 숫자 없음) → 전자 소산 몫 SDCP 0 → 0.0300 % · 이온 소산 몫 SDCP 0 → 1.51 % (③ a0) · 상별 8 팔 ⬜ | ③ |
| M21 | 그림 5a → ③ a0 두 팔 · 정규화 기준 = SBE 중앙값 438 | ③ |
| M22 | 그림 5b 74 · 86 · 54.0 · 70.6 → 74 · ⬜ · 1.62 · 4.73 (8 팔 범위 SBE ⬜ · DBE 4.7054–4.7524) | ①② |
| M23 | 그림 5a · 5b 이미지 안 글자 → M21 · M22 값 | M21 · M22 |
| M24 | SEM 서술 (숫자 없음) → 모델 SDCP 평균 1 µm 덩어리 (1저자 SEM 판독 0.8–1.3 µm) | 등록 v2 §0 |
| M25 | (없음) → A. M. Bazzoun, J. Piruzjam, S. Hink, L. Rubacek, A. Fill, K. P. Birke · J. Power Sources 661 (2026) 238682 · DOI 10.1016/j.jpowsour.2025.238682 · 제목 [미확인 — 카드에 없음] | litdb 정본 카드 `bazzoun2026_dem_fem_rnm_ionic` (정본 가지 추적 ref `9ab132cd3`) |

### SI

| # | 옛 값 → 새 값 | 근거 |
|---|---|---|
| SI01 | 그림 S15 DBE 기하 → 새 DBE 침대 (③ B · final16 DBE a0 와 같은 침대) | §7 R1 · R2 |
| SI02 | "Calibrated" = 압밀 보정 → + VGCF σ (SBE · DBE 각자 전극 DC) · LPSCl σ₀ (Bazzoun) | §7 · §3-D |
| SI03 | (SDCP 시딩 문장 없음) → M17 값 | §7 R1 · R2 |
| SI04 | LPSCl σ_ion 3.0 × 10⁻³ · Ref. S4 → 7.45 × 10⁻⁴ S cm⁻¹ · Calibrated (composite EIS · CAM 70 wt% · 0.137 mS cm⁻¹ · Bazzoun 2026) | §3-D |
| SI05 | VGCF 분말 1.0 × 10² · Ref. S9 → 모델 입력 아님 | `CL-47` 정정 · M18 |
| SI06 | VGCF 복셀 78.5 · Calculated → SBE 0.347 · DBE 2.618 S cm⁻¹ · Calibrated (전극 DC) | §7 S2 · 15:47 |
| SI07 | SDCP 지름 0.30 µm · Measured → 1 차 0.30 µm · DBE 덩어리 평균 1 µm (SEM) | 등록 v2 §0 |
| SI08 | (없음) → 덩어리 1 µm · 내부 채움 0.64 (Assumed) · 부착 몫 0.5 (Assumed · 실현 ⬜) | 등록 v2 §3-B · §4 |
| SI09 | SDCP E 9.0 GPa → 9.0 (두 침대 실제 값) | §7 R0 · R2 |
| SI09b | 표 S2 행 15 VGCF E 100 GPa → 두 침대 실제 값 10 GPa | §7 R0 (`ADD_E_SET_20260818`) · R1 (`--add-e-override VGCF=10`) · `CL-93` |
| SI10 | SDCP 이온 σ 1.0 × 10⁻³ · Assumed → 2.48 × 10⁻⁴ S cm⁻¹ (LPSCl 과 같은 배수 0.2483 · Assumed) | §3-D |
| SI11 | 표 S3 캡션 → σele SBE · DBE 둘 다 전극 DC 보정 | ①② |
| SI12 | 두께 72.53 · 72.53 µm → 72.53 · 72.53 | ③ · §7 R1 시도 5 |
| SI13 | 기공 7.86 · 7.37 % → 7.86 · 7.37 (ε_union 진단값) | ③ · §7 R1 시도 5 |
| SI14 | SE coverage 86.6 · 86.6 % → 86.60 · 86.60 (Tabor 0.26 µm · `coverage_AM_S_tabor_pct`) · Hertz 65.70 · 65.70 | ③ · `webapp/static/js/viewer3d.js:9145–9150` |
| SI15 | CA coverage 13.1 · 15.5 % → 13.10 · 13.50 (`coverage_AM_S_add_mpm_pct` · PTFE 포함) | ③ · `scripts/mpm3d_compaction.py:3764–3766` · `:3881` |
| SI16 | 접점 중앙값 74 · 86 → 74 · ⬜ | M06 |
| SI17 | 전자 연결도 100 · 100 % → 100 · 100 | ③ |
| SI18 | 두 안 — 아래 표 | ③ |
| SI19 | σele 54.0 · 70.6 → 1.62 · 4.73 mS cm⁻¹ (1.6209 · 4.7287) | ①② |
| SI20 | σion 0.553 · 0.558 → 0.137 · 0.138 mS cm⁻¹ (0.13704 · 0.13823) | ①② |
| SI21 | 그림 S16 → ③ a0 두 팔 · 이온 focus_top 11.61 · 11.40 | ③ |
| SI22 | 그림 S17 → ③ a0 두 팔 · 전자 focus_top 91.59 · 204 | ③ |
| SI23 | Ref. S4 = 행 13 출처 → 행 13 에서 빠짐 (캡션 [S4] 남음) · 새 문헌 = M25 | §3-D |
| SI24 | Ref. S9 → SI05 와 같이 | SI05 |
| SI25 | (없음) → R 7.016 · 2.178 Ω · 쌍 저항 7.003–7.023 · 2.141–2.199 Ω · r² 0.999999 · 0.99993 · 두께 90 · 80 µm · Ø10 mm | 등록 v2 §1 · `docs/data/sdcp_dc_polarization_20261016/dc_reading.json` |

### SI18 · M09 — 두 안 (값만)

| 자리 | (가) 삭제 — 권고 | (나) 새 값 |
|---|---|---|
| SI18 표 S3 행 8 (옛 79.5 · 71.5 = `focus_over_local_mean` · J₉₉.₈/⟨\|J\|⟩_cond) | 행 삭제 | `focus_over_local_mean` SBE ⬜ · DBE ⬜ / 화면 a0 `focus_top` (J₉₉.₈/J_app) SBE 91.59 · DBE 204 |
| M09 "… larger number of parallel pathways (Figures S16 and S17)" | 비교 구절만 삭제 · 이온 분포 문장 유지 (이온 focus_top a0 11.61 · 11.40) | 전자 focus_top a0 SBE 91.59 · DBE 204 (옛 435.1 · 375.8) · σ*/σ_AM SBE 85 · DBE 640 |

### kgy 에서 뽑을 값

| 자리 | 양 | 키 (파일:줄) |
|---|---|---|
| M04 · M05 · M06 · M13 · M22 · SI16 · 그림 5b | 새 DBE 침대 접점 (0.15 µm · 개체) | payload 에 없음 → `scripts/cbd_contacts_per_am.py` (침대 `phase.npy` · `fibre.npy` · `se_dump.npy` + `am_scaffold.csv`) · 명령 ① |
| SI18 (나) | 전자 J₉₉.₈/⟨\|J\|⟩_cond · J₉₉.₈/J_app · ⟨\|J\|⟩_cond/J_app (8 팔) | `mpm_metrics.step3.field_scale_e.focus_over_local_mean` · `.local_mean_over_j_app` (`scripts/mpm_webapp_payload.py:916–917`) · `.focus_top` (`:2193` — (나) 일 때만) |
| M09 (이온) | 이온 집중 (8 팔) | `mpm_metrics.step3.field_scale_ion.*` (`:2551–2561`) |
| M19 | σ_e · σ_ion 짝 비 (같은 origin · 8 짝) | `step3.sigma_e_eff_S_cm` (`:2141`) · `step3.sigma_ion_eff_S_cm` (`:2578`) · `step3.manifest.origin_shift_um` (`:3008`) |
| M20 | 상별 소산 몫 (8 팔) | `step3.dissipation_share` (`:2151–2152`) · `step3.ion_dissipation_share` (`:2586–2587`) |
| M17 · SI08 | SDCP 실현 부착 몫 · 덩어리 수 | `mpm_metrics.additives.SDCP.seeding.{realized_anchor_frac, n_clusters_am, n_clusters_bulk, n_seeded}` (`scripts/additives.py:746–749` · `scripts/mpm3d_compaction.py:2775–2781` · 운반 `scripts/mpm_webapp_payload.py:807–810`) |
| M22 | SBE σ_e 8 팔 범위 | `step3.sigma_e_eff_S_cm` |
| SI12–SI15 · SI17 | 침대 값 8 팔 같음 | `mpm_metrics.thickness_mpm_um` · `.porosity_mpm_pct` (`:3324–3325`) · `.coverage_AM_S_tabor_pct` · `_hertz_pct` (`:3336–3337`) · `.coverage_AM_S_add_mpm_pct` (`:3331`) · `econn_summary.connected_pct` · `.n_carbon_clusters` (`:1742–1743`) |
| AM_P 칸 | AM_P 입자 수 · AM_P 칸 값 | payload `particles[].type` · `coverage_AM_P_tabor_pct` (`:240` — 없는 상 = 0.0) · `coverage_AM_P_rigid_tabor_pct` (`:260–261` — None) · `coverage_AM_P_add_mpm_pct` (`scripts/mpm3d_compaction.py:1141` — 0.0) |

```bash
# ① 접점 (kgy · CPU · 기존 도구 · 출력 JSON 하나를 ~/sdcp 에 쓴다 · 작업트리 = 최종 16 팔과 같은 298a73197)
cd ~/dem-anchor1019b && . ~/dem-venv/bin/activate
ls ~/sdcp/kit_DBE_sdcp1um/*scaffold*          # am_scaffold.csv 자리 확인
python3 scripts/cbd_contacts_per_am.py --bed ~/sdcp/kit_DBE_sdcp1um/run_VGCF3_PTFE0.5_SDCP0.5_20261019_191217_2231061 \
    --scaffold ~/sdcp/kit_DBE_sdcp1um/am_scaffold.csv --out ~/sdcp/contacts_DBE_sdcp1um_band015.json
```

```bash
# ② 팔 JSON 값 (kgy · 읽기만 · stdlib · 파일을 쓰지 않는다 · 팔 JSON 하나씩 raw_decode —
#    합성 139 MB 두 개 시험 = 1.2 s · 최고 RSS 279 MB) · ① 뒤면 끝에 --contacts 두 개를 붙인다:
#    --contacts ~/dem-anchor1019b/docs/data/cbd_contacts_20260831/contacts_SBE_band015.json ~/sdcp/contacts_DBE_sdcp1um_band015.json
python3 -I - ~/sdcp/final16_1019 ~/sdcp/final8_dbe_vgcf2618 --dbe16 ~/sdcp/final16_1019 <<'EOF'
import argparse, glob, json, os, re, statistics as st
from collections import Counter

ap = argparse.ArgumentParser()
ap.add_argument('sbe_dir'); ap.add_argument('dbe_dir')
ap.add_argument('--dbe16', help='(선택) final16 DBE 폴더 — 같은 origin 의 σ_ion 대조')
ap.add_argument('--contacts', nargs=2, metavar=('SBE_JSON', 'DBE_JSON'),
                help='(선택) cbd_contacts_per_am.py 출력 두 개')
a = ap.parse_args()
DEC = json.JSONDecoder()


def vals(text, key):
    out = []
    for m in re.finditer(r'"%s"\s*:\s*' % re.escape(key), text):
        try:
            out.append(DEC.raw_decode(text, m.end())[0])
        except ValueError:
            pass
    return out


def first(vs, ok):
    return next((v for v in vs if ok(v)), None)


def g(d, path):
    for k in path.split('.'):
        if not isinstance(d, dict) or k not in d:
            return None
        d = d[k]
    return d


def read_arm(p):
    text = open(p, encoding='utf-8').read()
    mm = first(vals(text, 'mpm_metrics'), lambda v: isinstance(v, dict) and 'porosity_mpm_pct' in v) or {}
    ec = first(vals(text, 'econn_summary'), lambda v: v is None or (isinstance(v, dict) and 'connected_pct' in v))
    pa = first(vals(text, 'particles'), lambda v: isinstance(v, list) and v and isinstance(v[0], dict)) or []
    del text
    s3 = mm.get('step3') or {}
    return dict(file=os.path.basename(p), mm=mm, s3=s3, man=s3.get('manifest') or {}, ec=ec or {},
                types=Counter(q.get('type') for q in pa))


def mS(r, k):
    v = r['s3'].get(k)
    return None if v is None else 1e3 * v


Q = [  # (이름 = payload 키, 꺼내는 함수)
    ('σ_e [mS/cm] (step3.sigma_e_eff_S_cm)', lambda r: mS(r, 'sigma_e_eff_S_cm')),
    ('σ_ion [mS/cm] (step3.sigma_ion_eff_S_cm)', lambda r: mS(r, 'sigma_ion_eff_S_cm')),
    ('step3.cg_info', lambda r: r['s3'].get('cg_info')),
    ('step3.ion_cg_info', lambda r: r['s3'].get('ion_cg_info')),
    ('step3.n_dof', lambda r: r['s3'].get('n_dof')),
    ('field_scale_e.focus_over_local_mean (옛 표 S3 행 8)', lambda r: g(r['s3'], 'field_scale_e.focus_over_local_mean')),
    ('field_scale_e.focus_top ((나) 일 때만)', lambda r: g(r['s3'], 'field_scale_e.focus_top')),
    ('field_scale_e.local_mean_over_j_app', lambda r: g(r['s3'], 'field_scale_e.local_mean_over_j_app')),
    ('field_scale_ion.focus_over_local_mean', lambda r: g(r['s3'], 'field_scale_ion.focus_over_local_mean')),
    ('field_scale_ion.focus_top', lambda r: g(r['s3'], 'field_scale_ion.focus_top')),
    ('field_scale_ion.local_mean_over_j_app', lambda r: g(r['s3'], 'field_scale_ion.local_mean_over_j_app')),
    ('econn_summary.connected_pct', lambda r: r['ec'].get('connected_pct')),
    ('econn_summary.n_isolated', lambda r: r['ec'].get('n_isolated')),
    ('econn_summary.n_carbon_clusters', lambda r: r['ec'].get('n_carbon_clusters')),
    ('mpm_metrics.thickness_mpm_um', lambda r: r['mm'].get('thickness_mpm_um')),
    ('mpm_metrics.porosity_mpm_pct', lambda r: r['mm'].get('porosity_mpm_pct')),
    ('mpm_metrics.coverage_AM_S_tabor_pct', lambda r: r['mm'].get('coverage_AM_S_tabor_pct')),
    ('mpm_metrics.coverage_AM_S_hertz_pct', lambda r: r['mm'].get('coverage_AM_S_hertz_pct')),
    ('mpm_metrics.coverage_AM_S_add_mpm_pct', lambda r: r['mm'].get('coverage_AM_S_add_mpm_pct')),
    ('mpm_metrics.coverage_AM_P_tabor_pct', lambda r: r['mm'].get('coverage_AM_P_tabor_pct')),
    ('mpm_metrics.coverage_AM_P_rigid_tabor_pct', lambda r: r['mm'].get('coverage_AM_P_rigid_tabor_pct')),
    ('mpm_metrics.coverage_AM_P_add_mpm_pct', lambda r: r['mm'].get('coverage_AM_P_add_mpm_pct')),
    ('particles type AM_P 수', lambda r: r['types'].get('AM_P', 0)),
    ('particles type AM_S 수', lambda r: r['types'].get('AM_S', 0)),
    ('additives.SDCP.agg_d_um', lambda r: g(r['mm'], 'additives.SDCP.agg_d_um')),
    ('additives.SDCP.seeding.realized_anchor_frac', lambda r: g(r['mm'], 'additives.SDCP.seeding.realized_anchor_frac')),
    ('additives.SDCP.seeding.n_clusters_am', lambda r: g(r['mm'], 'additives.SDCP.seeding.n_clusters_am')),
    ('additives.SDCP.seeding.n_clusters_bulk', lambda r: g(r['mm'], 'additives.SDCP.seeding.n_clusters_bulk')),
    ('additives.SDCP.seeding.n_seeded', lambda r: g(r['mm'], 'additives.SDCP.seeding.n_seeded')),
]


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and v == v


def f6(v):
    return '—' if v is None else (f'{v:.6g}' if isinstance(v, float) else str(v))


def summ(xs):
    xs = [x for x in xs if num(x)]
    if not xs:
        return '—'
    if len(set(xs)) == 1:
        return f'{f6(float(xs[0]))} (팔 {len(xs)} 같음)'
    return (f'{f6(st.fmean(xs))} · sd {f6(st.stdev(xs) if len(xs) > 1 else 0.0)} · '
            f'{f6(min(xs))}–{f6(max(xs))} (n {len(xs)})')


def org(r):
    o = r['man'].get('origin_shift_um')
    return tuple(round(float(x), 9) for x in o) if o else None


arms = {}
for bed, pat in (('SBE', os.path.join(a.sbe_dir, 'p2_SBE_sph_a[0-7].json')),
                 ('DBE', os.path.join(a.dbe_dir, 'p2_DBE_sdcp1um_sph_a[0-7].json'))):
    fs = sorted(glob.glob(pat))
    print(f'{bed}: {len(fs)} 파일 ({pat})' + ('' if len(fs) == 8 else '  ⚠ 8 이 아니다'))
    arms[bed] = [read_arm(p) for p in fs]

print('\n| 팔 | origin_shift_um | σ_e [mS/cm] | σ_ion [mS/cm] | cg · ion_cg | e focus_over_local_mean | '
      'sigma_vgcf_S_cm | percentile_basis (e · ion) |')
print('|---|---|---|---|---|---|---|---|')
for bed in ('SBE', 'DBE'):
    for r in arms[bed]:
        s3, man = r['s3'], r['man']
        print(f"| {r['file']} | {org(r)} | {f6(Q[0][1](r))} | {f6(Q[1][1](r))} | {s3.get('cg_info')} · "
              f"{s3.get('ion_cg_info')} | {f6(g(s3, 'field_scale_e.focus_over_local_mean'))} | "
              f"{man.get('sigma_vgcf_S_cm')} | {g(s3, 'field_scale_e.percentile_basis')} · "
              f"{g(s3, 'field_scale_ion.percentile_basis')} |")

print('\n| 양 (payload 키) | SBE | DBE |')
print('|---|---|---|')
for name, fn in Q:
    print(f"| {name} | {summ([fn(r) for r in arms['SBE']])} | {summ([fn(r) for r in arms['DBE']])} |")
for k in ('sigma_vgcf_S_cm', 'sigma_am_s_S_cm', 'sigma_sdcp_S_cm', 'sigma_ion_se_S_cm', 'sigma_ion_sdcp_S_cm',
          'vox_um', 'ptfe_stamp', 'input_digest'):
    print(f"| step3.manifest.{k} | {sorted({str(r['man'].get(k)) for r in arms['SBE']})} | "
          f"{sorted({str(r['man'].get(k)) for r in arms['DBE']})} |")
for k in ('dissipation_share', 'ion_dissipation_share'):
    for ph in sorted({p for b in arms for r in arms[b] for p in (r['s3'].get(k) or {})}):
        print(f"| step3.{k}.{ph} [%] | {summ([100 * (r['s3'].get(k) or {}).get(ph, 0) for r in arms['SBE']])} | "
              f"{summ([100 * (r['s3'].get(k) or {}).get(ph, 0) for r in arms['DBE']])} |")

sm = {org(r): r for r in arms['SBE']}
dm = {org(r): r for r in arms['DBE']}
keys = sorted(k for k in sm if k is not None and k in dm)
print(f'\n짝 (같은 origin_shift_um): {len(keys)}' + ('' if len(keys) == 8 else '  ⚠ 8 이 아니다'))
for name, fn in Q[:2]:
    rr = [fn(dm[k]) / fn(sm[k]) for k in keys if num(fn(dm[k])) and num(fn(sm[k])) and fn(sm[k])]
    if rr:
        print(f'{name} 짝 비 DBE/SBE: 평균 {st.fmean(rr):.5f} · sd {st.stdev(rr) if len(rr) > 1 else 0:.5f} · '
              f'{min(rr):.5f}–{max(rr):.5f} (n {len(rr)})')

if a.dbe16:
    old = {org(r): r for r in (read_arm(p) for p in sorted(glob.glob(os.path.join(a.dbe16, 'p2_DBE_sdcp1um_sph_a[0-7].json'))))}
    dd = [abs(dm[k]['s3']['sigma_ion_eff_S_cm'] / old[k]['s3']['sigma_ion_eff_S_cm'] - 1)
          for k in keys if k in old and old[k]['s3'].get('sigma_ion_eff_S_cm')]
    print(f'\nσ_ion final8 DBE ↔ final16 DBE: 짝 {len(dd)} · 최대 상대 차 {max(dd) if dd else None}')

if a.contacts:
    K = 'conductive only (VGCF+SDCP)'
    cs = [json.load(open(p, encoding='utf-8'))[K]['counts'] for p in a.contacts]
    m0 = st.median(cs[0])
    for bed, c in zip(('SBE', 'DBE'), cs):
        q = sorted(c)
        print(f'접점 {bed}: 중앙값 {st.median(c)} · 평균 {st.fmean(c):.2f} · p10 {q[len(q) // 10]} · '
              f'p90 {q[-max(1, len(q) // 10)]} · 0 인 AM {sum(1 for v in c if v == 0)}/{len(c)} · '
              f'SBE 중앙값 {m0} 초과 {sum(1 for v in c if v > m0)}/{len(c)} = '
              f'{100 * sum(1 for v in c if v > m0) / len(c):.1f} %')
EOF
```

```bash
# ③ 그림 5b 접점 분포 (① 뒤 · 출력 = ~/sdcp/fig5b_1020/cbd_contacts.{svg,png,csv} · _origin.csv)
cd ~/dem-anchor1019b && mkdir -p ~/sdcp/fig5b_1020
cp docs/data/cbd_contacts_20260831/contacts_SBE_band015.json ~/sdcp/fig5b_1020/
cp ~/sdcp/contacts_DBE_sdcp1um_band015.json ~/sdcp/fig5b_1020/contacts_DBE_band015.json
python3 scripts/plot_cbd_contacts.py --data ~/sdcp/fig5b_1020 --out ~/sdcp/fig5b_1020/cbd_contacts
```

### 그림 (등록 v2 §6)

| 그림 | 무엇 | 원천 | 1저자 할 일 |
|---|---|---|---|
| 5a | AM 근접 도전재 밀도 (AM 중심 r + 0.3 µm 안 가중 점 점유량 · 접점 아님) · 공동 눈금 p5–p95 · 중앙값 낮은 쪽 = 1 (SBE 438) | 웹앱 :5002 ⚖ 비교 "전기 배선" (`wiring`) · A = `~/sdcp/final16_1019/p2_SBE_sph_a0.json` · B = `~/sdcp/final8_dbe_vgcf2618/p2_DBE_sdcp1um_sph_a0.json` · `webapp/static/js/viewer3d.js:8294–8350` · `:9662–9700` · 첨가제 점 표본 seed 고정 (`scripts/mpm_webapp_payload.py:3205`) → final16 DBE a0 와 같은 그림 (코드 판독) | 화면 · 컬러바 PNG · 캡션 origin (0,0,0) |
| 5b | 접점 분포 (바이올린 · 중앙선) + σele 막대 | 접점 = 명령 ① → ③ · σ = ①② 8 팔 평균 1.62 · 4.73 · 범위 = 조각 ② · `scripts/fig4b_sigma_conventions.py` = 옛 값 (53.99 · 70.61) 이 박힌 옛 그림 | 명령 ① ③ · σ 막대 |
| S15 | SBE · DBE 기하 | 웹앱 단일 뷰어 · DBE = B 팔 JSON (새 침대) · SBE 침대 그대로 | DBE 렌더 |
| S16 | 이온 전류 밀도 | ⚖ 비교 "⚡ 이온 전류밀도 필드" (`ji_field`) · A · B 위와 같음 · 공동스케일 · 기준 p99.8-max (기본) = 천장 SBE (p99.8 절대 0.2206 · 0.2177 A cm⁻² @1V · B ×0.987) / @1C-peak = 천장 SBE (B ×0.982) · `viewer3d.js:9731–9798` | 프레임 고름 · 캡션 프레임 표지 |
| S17 | 전자 전류 밀도 | ⚖ 비교 "⚡ 전자 전류밀도 필드" (`je_field`) · 공동스케일 · p99.8-max = 천장 DBE (20.56 · 133.7 A cm⁻² @1V · A ×0.154) / @1C-peak = 천장 DBE (296.8 · 661 mA cm⁻² @1C · A ×0.449) | 〃 |
| 등록 | `python3 webapp/mpm_lab_register.py --payload <PC 의 팔 JSON> --name <이름> --url http://localhost:5002/mpm-lab/upload` (또는 `--dest <mpm_lab 폴더>`) · ⛔ :5001 | `webapp/mpm_lab_register.py:319–325` | a0 둘 = 19:2x 화면에 있음 |

S16 · S17 의 p99.8 절대 · 배수 = ③ 화면 값 (focus_top × ⟨J⟩) 의 산술.

### 바뀌는 사실

| # | 바뀌는 사실 | 자리 |
|---|---|---|
| F1 | σele 두 전극 모두 전극 DC 보정값 (σ_VGCF SBE 0.347 · DBE 2.618) — 모델 예측 σele 없음 | M08 · M11 · M22 · SI11 · SI19 |
| F2 | 모델 σ_e 비 2.917 ↔ 실험 2.871 = 두 보정에서 나온 값 | M11 · M19 |
| F3 | 탄소망 유효 σ 한 값 78.5 (Calculated) → 전극별 두 값 (×7.54) | SI06 · M18 |
| F4 | 전자 focus_top 순서 옛 SBE 435.1 > DBE 375.8 → 새 a0 SBE 91.59 < DBE 204 (뒤집힘) | M09 · M10 · M14 · SI18 · SELF-45 §K 회신문 ("ordering survives") |
| F5 | 이온 focus_top a0 11.61 → 11.40 (−1.8 %) · σ_ion 비 1.0087 (SDCP 이온 σ 2.48 × 10⁻⁴ 가정) | M09 · M10 · M14 |
| F6 | CA coverage DBE 15.5 → 13.5 % (SBE 13.1 그대로 · DBE − SBE +2.4 → +0.4 %p) · 양에 PTFE 포함 | SI15 |
| F7 | 그림 5a 양 (AM 근접 점유량 중앙값) 438 → 522 (+19.1 %) → 438 → 485 (+10.5 %) | M03 · M21 |
| F8 | 탄소 연결 성분 수 옛 3069 → 8546 (×2.785) → 새 a0 3069 → 2747 (−10.5 %) | 원고 "conductive clusters" 문장 (있으면) · 웹앱 툴팁 `viewer3d.js:9116–9117` (옛 ×2.7) |
| F9 | 85 % 의 원 계산 = 개체 접점 0.15 µm (1083/1271) ↔ 본문 낱말 "CA density" · 그림 5a 양 = r + 0.3 µm 점 점유량 | M04 · M21 |
| F10 | SDCP 개체 id: 옛 DBE (낱알) = AM 에 붙은 낱알은 host AM 번호 하나 · 공극 낱알은 하나씩 / 새 DBE = 덩어리 하나 (`scripts/additives.py:315` · `:731–741` · `:709–713`) | M06 · M07 · 등록 v2 §6 "~24 배" |
| F11 | AM_P 칸 0 (두 전극 · SE 덮임 Hertz · Tabor · 도전재 덮임) = AM_P 입자 0 (NCM811 단일 크기 1,271 개 · Table S3 원장 §10-2 · 8 팔 확인 = 조각 ② `particles type`) → N/A · 생산자가 없는 상에 0.0 (`scripts/mpm_webapp_payload.py:240` · `scripts/mpm3d_compaction.py:1141`) · 강체 coverage = None (`:260–261`) · 웹앱은 AM_S 없을 때만 행을 숨김 (`viewer3d.js:9156–9158`) — 표시 결함 후보 (고치지 않음) | SI14 · SI15 · 웹앱 |
| F12 | 웹앱 "e-집중 p99.8 (× J_app)" = `focus_top` (`viewer3d.js:9098`) ≠ 옛 표 S3 행 8 의 양 (`focus_over_local_mean`) · 그 행 툴팁의 *"논문: current-focusing factor"* = SELF-45 §K 가 망 내부 양에 붙인 이름 | SI18 · 웹앱 |
| F13 | SDCP 크기 바꿈 a0 1.9385 → 1.8965 (−2.2 %) 와 시딩 점 138,988 → 116,532 가 같이 바뀜 | M17 · §7 10:50 |
| F14 | 표 S2 행 15 VGCF E 100 GPa ↔ 두 침대 10 GPa | SI09b |
| F15 | 면적용량 3.24 mAh cm⁻² (웹앱) = payload 자동 산출 (Chen2020 창) · Table S3 원장 §10-5 = n/a (비용량 미상) | 면적용량 행 (있으면) |
| F16 | TLM Rele 비 1.23 (59.7 / 48.5) ↔ DC 비 2.86 | M11 |
