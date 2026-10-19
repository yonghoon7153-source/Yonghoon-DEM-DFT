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
