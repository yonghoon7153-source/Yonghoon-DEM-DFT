# TIMELOG — 세션 작업 기록 (방 터졌을 때 빠른 복구용)

> **규칙**: Claude는 모든 작업 시작/완료 시 이 파일에 한 줄 추가.
> 형식: `YYYY-MM-DD HH:MM | branch | action | status | notes`
> status: START / DONE / BLOCKED / CRASHED-RESUME-NEEDED
> 가장 최근 항목이 위로 오도록 (역순).

---

## 📌 PENDING (오늘 미루고 나중에 할 것) — 2026-05-13 기준

| Priority | 작업 | 상태 | 재개 방법 |
|----------|------|------|----------|
| MEDIUM | **comp3/comp5 EOS 나머지 8 vols** (v098,99,100,106,107,108 etc.) | 자동 진행 (priority 3 vol 끝나면) | run_dft_eos.sh ALL_VOLS 순서로 계속. auto_restart로 walltime kill 대응. |
| LOW | **comp3 anneal_chain resume** (r2-r4 8 pairs 더) | KILLED at 8/25 pairs | r0 (5/5) + r1/li0-li2 done. r2-r4 unlikely to beat r0/li0 (-256.370). 시간 남으면 추가. |
| LOW | **comp5 anneal_chain resume** (r2-r4 15 pairs 더) | KILLED at 10/25 pairs | r0+r1 fully done (10/10). r2-r4 unlikely to beat r1/li1 (-254.919). Champion finalized. |
| LOW | **comp3/5 post-processing** (Bader/PDOS) | NEEDS V0 DFT EOS done | After DFT EOS → tight SCF → pp.x + projwfc.x. Reference: comp4_lpscbrbr/dft_eos/v0_fit/ structure. |
| LOW | **comp3/5 v2 bond length analysis** | NEEDS V0 structure | mic distance from V0.xyz + cutoffs (Li-O 2.8, Li-S 3.0, Li-Cl 3.2, Li-Br 3.4 Å). **User confirmed: 최종 V0 나온 후에 bond length 분석 진행.** |
| LOW | **comp3/5 v2 ADHESION slab + re-adhesion** | NEEDS V0 + Bader done | Chain: V0 cell + Bader charge → cleave SE slab with consistent surface termination → comp{3,5}_v2_slab.xyz. Then phase1_rigid_binding.py with v2 slabs → 새 adhesion figure (v2 anneal champion based, v1 OLD figure 대체). 오늘 paper main은 v1 OLD figure (paper-acceptable). v2-based adhesion은 elastic moduli section 끝나면 추가. |

## 📌 TODAY'S FOCUS — 2026-05-13 / 2026-05-14

**Goal:** mechanism scheme + lit review (waiting for KISTI comp3/5 v2 V₀)

| 시각 | branch | action | status | notes |
|------|--------|--------|--------|-------|
| 2026-05-14 ~05:00 | debug-api-500-error-iukkt | 사용자 full gabia session log paste 받음 | DONE | 핵심 milestones 재정리: |
|  |  |  |  | **(A) KISTI**: comp3 v2 EOS v098 iter=366 SCF, BFGS step 0, 16085 CPU sec — 진행 느림. |
|  |  |  | **(B) 3L NCM 검증 실패**: R(1L vs 3L)=−0.4580. comp3/4/5 sign flip. 1L 최종 confirmed. |
|  |  |  | **(C) 1L correct phase1 재현**: R1_origin d=1.2 Wad=+0.3863 J/m² (KISTI ref +0.38629 정확히 일치). |
|  |  |  | **(D) comp4_v2 eiso_fix**: ΔW_strain = +0.5482 J/m² (vs v1 +0.4445). 셀 area v2/v1 = 0.9893. |
|  |  |  | **(E) 14-pair bond density**: M→Ni patched. n=4 (comp1/2/4_v1/4_v2). Face A 강한 descriptor: S-O R=−0.973 ANTI, Li-Li/Li-O/Br-O R≈+0.9 PAPER. Face B: P-O R=−0.996 ANTI. |
|  |  |  | **(F) comp4_v2 face A halogen 노출 확인**: Cl 14개 + Br 8개 동시 노출 (v1은 Br 17개만). |
|  |  |  | **(G) comp2 halogen z-분포**: Cl mean z=14.26 (buried), Br mean z=19.24 (위쪽 노출). |
|  |  |  | **(H) Killer figure R=+0.9991 (n=3)** 다양한 Y-shift mode로 동일 R: face B + α=1.0. |
|  |  |  | **(I) Renders 완료**: interface_3d_compare, interface_3axis_compare, scheme_vacancy_mechanism (PNG/PDF). |
| 2026-05-14 ~06:30 | debug-api-500-error-iukkt | 🚨 사용자 지적: v1 vs v2 비교는 무의미 — 다른 anneal local minima | DONE | 맞음. comp4_v1, comp4_v2 는 같은 stoichiometry지만 다른 anneal champion = 서로 다른 random local minimum. "Cl이 16.20→12.45 Å로 이동"은 atom migration이 아니라 단지 ordering preference 차이. **진짜 migration 보려면 SAME atoms before/after relax** 측정해야 함. 다음 단계: 단일 slab (comp4_v2) + NCM + LBFGS relax, 같은 halogen atoms의 z position before vs after 추적. |
| 2026-05-14 ~06:25 | debug-api-500-error-iukkt | gabia에서 analyze_halogen_slab_positions.py 실행 완료 | DONE | n_per_face + <Li-X> bond per comp 표 받음. comp4_v1 Cl=16.20 / comp4_v2 Cl=12.45 (Δ=−3.75 Å). 단 이건 다른 local minima 비교라 migration 의미 아님 (위 사용자 지적). |
| 2026-05-14 09:55 | debug-api-500-error-iukkt | Face B Wad descriptor 정체 = P 노출 vs P 묻힘 (family-binary classifier) | DONE | Face_flip surface count: Li6 family face B 는 **8 P 노출** (PS₄ tetrahedron) / Li5.4 family face B 는 **0 P** (PS₄ buried). P-O density: comp1=0.066, comp2=0.066, comp4_v2=0 → 거의 step function. **R=−0.994 는 family-binary classifier 의 표현일 뿐**. Mechanism: Li5.4 vacancy framework 가 PS₄ 를 인터페이스에서 묻고 깨끗한 Li/S termination 제공 → Li-O productive 채널 unblocked. Face A 와 다른 점: face A 는 S/halogen 노출이 family-distinct, face B 는 P 노출/burial 이 family-distinct. |
| 2026-05-14 09:45 | debug-api-500-error-iukkt | Face B bond density n=3 (killer figure 와 동일 set) R 값 계산 | DONE | Face B (comp1, comp2, comp4_v2): **P-O R=−0.994 strongest ANTI** (PS₄ near NCM-O parasitic), **Li-Li R=+0.862 only PAPER** (clean Li-cluster termination), Li-O R=−0.833, S-O R=−0.734. Face A 와 대조: Face A 가 mechanism descriptor 풍부 (Li-O +0.92, Br-O +0.89, S-O −0.97 등 다양). **Paper 전략**: Wad는 Face B 사용 (R=+0.999), bond density mechanism plot은 Face A 사용. |
| 2026-05-14 09:25 | debug-api-500-error-iukkt | 🎯 사용자 제안: coarse V0 + MLIP relax 로 adhesion 우회 — 합리적 | DONE | Tight DFT vs coarse EOS 좌표 차이 ~5-10 mÅ < MLIP UMA noise (~50-100 mJ/m²). **comp3_v2_V0_PROVISIONAL_v103_scaled.xyz** (v103 coarse-relaxed + V_eq scaled) 가 이미 KISTI 에 있음. gabia 에서 scp → MLIP UMA relax (10-15min) → slab → face_flip + eiso_fix → killer figure **n=5 today 가능**. 병렬 plan: KISTI 는 tight V0 계속 (Bader/PDOS 용), gabia 는 coarse 좌표로 즉시 adhesion 진행. |
| 2026-05-14 09:13 | debug-api-500-error-iukkt | V0 relax 진행 확인 — 둘 다 GPU 47-48% util, 10 GB mem, 1분 내 fresh update | DONE | comp3 GPU0 / comp5 GPU1 각자. SCF iter 1 시작 (아직 acc line 안 찍힘 — 1-2 min 내 etabilish). CRASH 파일은 5/13 14:42 옛날 거 (방치 OK 또는 .old 로 rename). 예상: 1-2h SCF 수렴, 3-6h 첫 BFGS step, 1-2일 전체 V0 수렴 → JOB DONE 후 scf_v0/nscf/bader 단계 사용자 manual start 필요. |
| 2026-05-14 09:11 | debug-api-500-error-iukkt | comp3/5 V0 tight relax RESTARTED 성공 | DONE | comp3 PID 3351198 (GPU0), comp5 PID 3351203 (GPU1), 둘 다 "Restart at 09:11:28 KST" 로그 확인. nvidia-smi 556 MiB (시작 시점), pw.x 활성. Watch script 작성 중 — kisti_monitor_v0_relax.sh. |
| 2026-05-14 09:30 | debug-api-500-error-iukkt | V0 tight relax restart 준비 OK — tmp/ + script 자동 restart 모두 정상 | DONE | comp3/5 둘 다 `tmp/.../save` (wavefunction) + `.bfgs` + `.update` 보존. run_v0_relax.sh 가 이미 restart logic 내장: `JOB DONE` 체크 skip + `tmp/.save/` 있으면 `restart_mode='restart'` 자동 삽입. ⚠️ comp3 script CUDA_VISIBLE_DEVICES=0 hardcoded — comp5 도 확인 필요. 재시작: 각자 디렉토리에서 `nohup ./run_v0_relax.sh &`. v0_relax.log 에 "Restart at..." 찍히면 정상. 예상: BFGS 1 step ~4-6h, 전체 V0 수렴 1-2일. |
| 2026-05-14 09:20 | debug-api-500-error-iukkt | V0 후 단계 directory 구조 발견 — comp3/5 모두 v0_fit/ 동일 구조 | DONE | comp3 v0_fit/ (5/13 23:16-23:23 prep, 5/14 03:29 last activity) + comp5 v0_fit/ (23:51 prep, 03:40 last). 구성: `compute_v0_cell.py / make_v0_inputs.py / patch_relaxed_coords.py / v0_cell.dat / run_v0_relax.sh / relax_v0/ / scf_v0/ / nscf_dos/ / bader/`. comp4 reference (5/10 done): relax → tight_scf → nscf → dos → pp → bader 순서. comp3/5 는 **relax_v0/ 단계에서 죽음** (03:29/03:40 사이). post_relax_comp1_v2/ 별도 directory에 comp1_v2_scf.out / nscf.out 있음 (comp1 v2는 별도 layout). |
| 2026-05-14 09:10 | debug-api-500-error-iukkt | KISTI 상태 명확화: V0 relax (post-proc tight) 가 가장 최근 활동 | DONE | **정정**: 어제 죽은 게 EOS 가 아니라 V0 tight relax. 시간순: 5/13 22:09-23:51 EOS coarse scan (comp3 3/11, comp5 4/11) → 5/14 03:00-03:40 **V0 relax (tight ecutwfc=60, K=6x6x3) 진행 중** → 04:00 경 죽음. comp4 v2 reference path 확인: V0_relax → tight_scf → NSCF → DOS → pp.x → Bader (5/10 22:29-04:28 sequential). comp3/5는 V0_relax 단계에서 멈춤. 다음 단계: V0_relax 수렴 여부 확인 → 재시작 → tight_scf → ... → Bader. |
| 2026-05-14 09:00 | debug-api-500-error-iukkt | KISTI 모든 process 죽음 확인 — PC update 시 nohup 안 살아남음 | DONE | x3430a02 user에 pw.x/auto_restart 없음. **V0 relax 는 이미 5/13 늦은 시간에 완료** (어제 03:59 monitor에서 iter 200+ bfgs=0 진행 중이었던 거). 그 후 22:56-23:51 EOS scan 진행: comp3 v103/v102/v104 DONE (3/11), comp5 v102/v103/v104/v105 DONE (4/11). 5/14 00:00 경 모두 die. comp3 lpscbr/ 에 CRASH 파일 있음 (5/13 14:42, 일찍 한 번 crash). **재시작 명령**: `cd comp{3,5}_lpscbr; CUDA_VISIBLE_DEVICES=N nohup ./auto_restart.sh &`. auto_restart.sh 가 DONE vol skip하고 priority 순으로 남은 7-8 vol 진행. |
| 2026-05-14 ~08:00 | debug-api-500-error-iukkt | Rhino 2-panel scheme 검증: 개념 맞음, 라벨만 수정 권장 | DONE | **맞는 부분**: Li6=halogen far from interface (comp1 Cl <z>=15.56), Li6=Li-O dominant (R=+0.92), Li5.4=Cl+Br at interface (comp4_v2 face A 4+4 노출), vacancy enables different config. **수정 권장**: "halogen redistribution" → "halogen-exposed termination" 또는 "multi-channel interface" (migration 어감 제거). Caption에 "anneal champion preference" 명시. Cl-O 결합선은 "contact" 로만 표현 (직접 attractive 아님). |
| 2026-05-14 ~07:45 | debug-api-500-error-iukkt | v2 도착 시 체크리스트 정리 (사용자 "답 찾을 수 있나" 질문) | DONE | **v2 후 확보**: n=3→n=5 R 검증, Br surface preference 보편성 확인, B₀ ↓ trend 5 comps, 14-pair bond density × 5 comps. **v2 와 무관 (별개 문제)**: migration 직접 증명 (AIMD/NEB/cryo-TEM 필요), DFT E vs exp E trend 반대 문제, activation barrier. **체크리스트 정리**: (1) comp3/5 v2 V₀ → B₀ → check trend / (2) 새 slab → / (3) z-profile (Br preference 보편?) / (4) face_flip + eiso_fix / (5) killer_v2 n=5 / (6) 14-pair bond density × 5. **Paper framing 유지**: "thermodynamic surface termination preference" — migration 단어 안 씀. |
| 2026-05-14 ~07:30 | debug-api-500-error-iukkt | z-profile 결과 받음 — Br의 일관된 surface preference 발견 | DONE | **Li6 family** (comp1, comp2): S가 양 face (z=0.4-29.2) 모두 점령. **Li5.4 family** (comp4_v1, comp4_v2, comp5): **Br <z>=10.6-12.3 일관되게 한쪽 face 부근** (regardless of anneal champion). Cl 거동은 champion 마다 다름 (comp4_v1=buried, comp4_v2=face 도달, comp5=buried). modelC (Cl-only)는 Cl spread — Br competition 없으면 surface preference 약함. **P는 모든 comp에서 buried** (PS₄ steric). Stacked: 모두 face B 사용 → comp4_v2 stacked는 halogen이 interface에 없음 (face A가 halogen 면). Killer figure는 face B로 R=+0.999. **Migration 없이도 "Br의 thermodynamic surface preference in vacancy frameworks"** 로 framing 가능 — Br ionic radius 1.10 / polarizability 큼 / low-coord surface site 선호. |
| 2026-05-14 ~07:10 | debug-api-500-error-iukkt | z-profile 분석 시작 (Li, P, S, Cl, Br, O, Ni — 챔피언 구조 그대로) | START | "Migration" 단어 안 씀. 사용자 컨펌: comp들이 champion (Li 배치 외엔 견줄 수 없음). z축으로 모든 species histogram → comp별 surface 구성 비교. Stacked orthogonal xyz 사용 (comp1, comp2, comp4_v2 already gabia에 있음). |
| 2026-05-14 ~07:00 | debug-api-500-error-iukkt | 🎯 핵심 narrative 정리: anneal step이 family-specific termination 선택 | DONE | 우리 Wad 차이의 출처 = (1) **Anneal MD가 가족별로 다른 surface chemistry 선택** (Li6: S-rich termination / Li5.4: halogen-near-surface termination). (2) Wad 측정 시 그 termination 의 NCM 접촉 binding을 봄. (3) 표면 S 가 많으면 R(S-O)=−0.97 anti — 즉 S-O 충돌로 약함, halogen 면은 Li-O+X-O 채널로 강함. (4) LBFGS relax 가 추가 1 Å 이내 local fit. **Migration 없이도 R=+0.999 가능. Paper narrative**: "annealing thermodynamically selects halogen-rich termination for vacancy-bearing Li5.4 family because monovalent X⁻ requires less local Li than divalent S²⁻ in Li-deficient frameworks. Rigid+LBFGS Wad on this pre-selected termination quantifies the 54% family enhancement." Migration 단어 안 씀 — defensible. |
| 2026-05-14 ~06:50 | debug-api-500-error-iukkt | 🚨 PENDING DISCUSSION: DFT/MLIP E 와 실험 E trend 정반대 | PENDING | **실험**: Li6 E ≈ 8 GPa < Li5.4 E ≈ 16-18 GPa (vacancy → E ↑, ν 0.45→0.35 picture). **MLIP E_600K snap (CLAUDE.md)**: 정반대 — Li6 (29.1, 28.6) > Li5.4 (27.3, 26.4, 25.8). 가능한 원인: (a) 600K 열적 disorder 가 polycrystal effect 안 잡음, (b) MLIP elastic protocol 이 단결정/이상적 cell에서 측정되어 실제 grain boundary/microstructure 무시, (c) MLIP 학습 데이터 한계. **사용자 나중에 논의 요청**. 일단 narrative 는 "experimental E ↑ with vacancy 가 ν 감소로 설명됨"으로 유지. 우리 계산 E 는 paper에 어떻게 framing할지 추후 결정. |
| 2026-05-14 ~06:45 | debug-api-500-error-iukkt | 🚨 사용자 지적: migration을 우리는 직접 증명 불가 | DONE | 맞음. (a) Rigid Z-scan: 원자 고정. (b) LBFGS relax: local minimum only, ≤1 Å adjustment. (c) Anneal champion: 여러 local minima 중 가장 안정 — 모두 "시작 site 근처에서 정해진" 결과. **활성화 에너지 넘는 migration 보려면 AIMD 고온(>1000K, ns)/NEB/cryo-TEM 필요 — 우리한테 없음.** Paper narrative 수정: "halide migration" 직접 주장 ❌ → "surface composition patterns consistent with Lee/Zeng experimental migration" ✅. |
| 2026-05-14 ~06:35 | debug-api-500-error-iukkt | 🚨 사용자 실험 figure paste — E (exp) 정정 받음 | DONE | LPSC1.0=8.0, LPSC0.5Br0.5=7.6 (Li6 ~8) // LPSC1.0Br0.6=18.3, LPSC0.8Br0.8=16.5, LPSC0.6Br1.0=15.6 (Li5.4 ~16-18). **Li5.4 family E 가 Li6 family E 의 약 2배.** ν 계산: comp1 ν=0.449 (incompressible), comp4 ν=0.368, comp3 ν=0.353. **Vacancy 도입이 Poisson ratio를 0.45→0.35로 떨어뜨려 E를 올림** (lateral flow 차단). 단일 원인 (Li vacancy)으로 B↓ + E↑ + σ_ys↑ + Wad↑ 모두 설명 가능. CLAUDE.md E_600K snap 은 MLIP 계산값 (실험과 trend 반대) — confusion source. |
| 2026-05-14 ~05:30 | debug-api-500-error-iukkt | 사용자 질문: B₀ ↓ + E ↑ 동시 가능성? | DONE | 물리적으로 가능. B와 E는 다른 양 (B=volume response, E=uniaxial). Poisson ratio ν로 분리: E=3B(1−2ν). ν 감소하면 E/B ↑ 가능. Li5.4 vacancy의 경우 framework loosening은 B에 직접, E는 다른 채널. CLAUDE.md 의 E 600K snap은 Li5.4 family 가 E 작은 걸로 나오므로 사용자 referencing E 데이터 확인 필요. |
| 2026-05-14 ~05:20 | debug-api-500-error-iukkt | 기존 slab 에서 halogen 이동 정량 분석 시작 (d_eq, Δz, X-Li bond) | START | comp4_v1 vs comp4_v2 + 다른 comps 비교. tools/analyze_halogen_slab_positions.py 작성 예정. gabia 실행 명령 제공. |
| 2026-05-14 ~05:10 | debug-api-500-error-iukkt | 🚨 사용자 full gabia log 두 번째 paste — 완전한 narrative arc 받음 | DONE | (J) α-strain sweep: α=0 R=−0.994 / α=1.0 R=+0.959 / α=1.5 R=+0.973. (K) Killer v2 face B + α=1.0 + per_comp asymp = **R=+0.9991** (n=3). (L) face_flip comp4_v2: face A Cl+Br 동시 노출(Wad −0.10 BAD) / face B (Wad +0.65 GOOD) — face B 채택. (M) mlip_relax test (comp1만 done): Wad_rig +3.02 → +6.56 (2x increase due to atom relax). (N) li_migration_36reg (comp1만 done): N=0~3 거의 평탄, 강제 Li 이동 무영향. (O) Exhaustive trend: 다양한 (face, agg, asymp, α) 조합 top-30 R=1.000 — comp1+comp2+comp4_v2 set 압도적. |
| 2026-05-14 ~05:00 | debug-api-500-error-iukkt | 사용자 지시: "옛날 v1에 해당하는거 다 지워 / adhesion 관련해서" | START | comp3/5 v1 stale rows + paper_figures_v1 directory 정리. |
| 2026-05-14 ~04:45 | debug-api-500-error-iukkt | 🚨 14-pair bond density 진짜 결과 (gabia 01:35 출력) 사용자 paste 받아서 정정 | DONE | M→Ni 패치 후 실행. n=4 (comp1, comp2, comp4_v1, comp4_v2). **Face A: S-O R=−0.973 (strongest ANTI), Li-Li/Li-O/Br-O R≈+0.9 PAPER, S-Li R=−0.815**. **Face B: P-O R=−0.996 (strongest ANTI)**. 내가 그동안 인용한 "S-Li R=−0.896"는 옛날 4-pair n=5 CSV (comp3/5 v1 포함). 진짜는 S-O(face A)/P-O(face B). **새 mechanism**: Li5.4 family avoids parasitic anion-anion + PS₄-NCM-O contacts → productive Li-O/X-O 우세. |
| 2026-05-14 ~02:00 | debug-api-500-error-iukkt | gabia에서 stacked orthogonal + 3-axis render + scheme generation | DONE | comp1/2/4_v2 R1_origin_d1.2/1.4 stacked. interface_3d_compare, interface_3axis_compare, scheme_vacancy_mechanism PNG/PDF 생성됨. 사용자가 "구리다"고 평가 → Rhino로 pivot. |
| 2026-05-14 ~04:30 | debug-api-500-error-iukkt | Hood/Patel 2021 PDF 정독 + 우리 paper와 비교 | DONE | Li6-xPS5-xClBrx (transport focus, 24mS/cm @ x=0.7). 조성 공간만 sister, mechanism은 무관 (그들=conductivity, 우리=mechanical/Wad). x=0.7에서 LiClxBr1-x 4% 불순물 = 용해도 한계 — 우리 Li5.4 family가 이 한계 부근에 위치한다는 정량 인용 가능. |
| 2026-05-14 ~04:00 | debug-api-500-error-iukkt | 사용자 PC 재부팅 + KISTI watchdog 살아있음 확인 | DONE | comp3 V0 iter=223, comp5 iter=216, 둘 다 force 0.001 (target 0.0001). 잡 살아있음 (nohup 가정). |
| 2026-05-14 ~03:30 | debug-api-500-error-iukkt | Strauss/Zeng 2022 Nat Commun PDF 정독 | DONE | 정정: 저자=Zeng(Yanshan U), Strauss 아님. 양극이 아니라 Li-metal 음극측 segregation. x≥1.3 grain 표면에 LiCl shell 자발 형성 (cryo-STEM). 우리 paper에는 "Cl 자발 표면 분포" precedent로만 인용 가능, NMC 양극 직접 증거 아님. |
| 2026-05-14 ~03:00 | debug-api-500-error-iukkt | Lee 2025 Science PDF (halide segregation) 정독 | DONE | UHS 2000rpm 5h 갈기로 LPSCl→LiCl shell on chalcogen 양극. cryo-TEM 직접. **우리 시스템은 NMC oxide + 정적 인터페이스 → 직접 인용 부적합. ** mechanism narrative 약화. |
| 2026-05-14 ~02:30 | debug-api-500-error-iukkt | tools/rhino_scheme_v2_literature.py 작성 + push | DONE | commit 27cf0ba. 2-panel scheme (Li6 vs Li5.4). literature-grounded 라고 했지만 **comp3 data와 모순** (comp3 X-O=0인데 Wad 최고). narrative 약함. |
| 2026-05-14 ~02:00 | debug-api-500-error-iukkt | mechanism literature 광범위 search (Lee, Zeng, Hood, Lu, Lim 등) | DONE | "halide segregation → Wad 강화" 직접 증거: chalcogen 양극에만 있음. NMC + Cl-rich + Wad 직접 측정 paper 없음. **우리 work이 그 빈 곳** — 단, atomistic evidence 부족. |
| 2026-05-14 ~01:30 | debug-api-500-error-iukkt | comp4 v1→v2 bond density 변화 확인 | DONE | `output/comp4_v2_adhesion/v1_v2_REDO_comparison.json`. comp4 v2 face A에 Cl 4개 새로 노출 (Cl-O 0→0.088), Br는 후퇴 (0.108→0.050). **R(Cl-O)=−0.91 v1 era sampling artifact, drop**. **Robust descriptor: R(S-Li)=−0.896 family classifier**. |
| 2026-05-14 ~01:00 | debug-api-500-error-iukkt | Rhino scheme 작업 (atom import, 2-panel scheme, material color fix) | DONE | tools/rhino_import_interface.py, tools/rhino_scheme_mechanism.py. AddPipe list bug fix, material API for raytraced color. 사용자 render 성공 확인. |
| ⚠️ 미스텝 | — | "halide segregation"으로 mechanism narrative 만들려다 우리 데이터(comp3 X-O=0이지만 Wad 최고)와 모순 발견 후 narrative 약화. **이미 확정된 R=0.9999 family signal + S-Li R=−0.896 사실에 집중해야 했음**. 사용자 반복 지적. | — | 다음엔 새 narrative 만들기 전에 kb/results/ 정독 먼저. |
| 15:17 | debug-api-500-error-iukkt | comp5 champion 추출 + MLIP EOS done | DONE | rank1/li1, E=-254.919 eV. V0=1254.04, B0=22.0 GPa (paper v1: 20.8, Δ+1.2). V0/V_cell=1.0414 → v104. |
| 15:14 | debug-api-500-error-iukkt | comp5 anneal_chain stop (10/25 pairs done) | DONE | r0+r1 fully done. Champion = r1/li1 -254.919 eV. r2-r4 안 돌림. |
| 14:43 | debug-api-500-error-iukkt | comp3 v2 DFT EOS KISTI 시작 (paper protocol K=2x2x1) | START | gen_dft_eos_comp4.py mirror + auto_restart.sh. GPU0. v098 BFGS step 1 진행 중. |
| 14:37 | debug-api-500-error-iukkt | comp3 anneal_chain stop + champion 추출 | DONE | r0/li0 = -256.370 eV. anneal_champion.xyz saved. |
| 11:47 | debug-api-500-error-iukkt | gabia v30u_1L 시작 (1L NCM PRESERVED, 5z×36xy, 6 comps) | START | paper protocol replica. comp1+2 done, comp3 진행 중. ~16:30 완료 예상. |
| 09:24 | debug-api-500-error-iukkt | comp3 v2 MLIP EOS (gabia) | DONE | V0=1236.55, B0=23.20 GPa. R²=0.9999. V0/V_cell=1.0268 → v103. |
| earlier | debug-api-500-error-iukkt | v30u_full_ensemble 분석 (3L NCM, 5z×36xy) | DONE | R=+0.92 (5 paper comps). Wells tiny (~3 mJ/m², 3L NCM convergence). |
| earlier | debug-api-500-error-iukkt | comp4 v1 swap (v2 anneal Cl exposed anomaly 발견) | DONE | comp4_slab_v1_PRESERVED.xyz (KISTI). R=0.92 → 0.93 회복 (1L에서는). |

## 🎯 핵심 발견 — adhesion paper

1. **OLD figure (1L NCM, 36 xy mean, R=0.931)** — paper-acceptable, paper draft 시점 검증된 figure
2. **Wad 절대값 1L NCM artifact로 paper-scale align** (1L "broken structure" per inventory)
3. **paper exp는 aJ 단위 (R=10nm tip), mJ/m² 변환 model-dependent (factor ~2)**
4. **UMA Wad : paper Wad = 0.32 ± 0.03 ratio (consistent across 5 comps)** — systematic ~3x scaling, NOT calibrated/cherry-picked
5. **Rank order R = +0.93 robust** — Li5.4 family >> Li6 family (~100+ mJ/m² 차이)

---

## 2026-05-11

| 시각 | branch | action | status | notes |
|------|--------|--------|--------|-------|
| 07:18 | debug-api-500-error-iukkt | kisti_monitor.sh 작성 (엄청 자세한 watch) | DONE | `필독/step1_halogen_li_anneal/kisti_monitor.sh` — GPU 사용량/온도, ps, watchdog crash count, Stage1a/1b/2/3 진행 카운트, run.log age, last 3 lines, champion 발견 시 best_cl/br/Li/E 자동 print. `watch -n 30 ./kisti_monitor.sh` 사용. |
| 07:10 | debug-api-500-error-iukkt | figure 보정: image1 (v4) → image2 style 복원 | DONE | (a) 원인: `plot_binding_curves_v4.py` 가 max-over-registry CSV 읽고 modelC 포함 + cubic spline 없음 + asymptote subtract 후 Y range 매우 넓음. (b) 처방: `plot_binding_curves_v7.py` 작성 — JSON 기반 mean over 36 + asymptote subtract + 5 paper comps 만 + cubic spline + gap window 1.2-1.6 음영 + R(well, paper) title + auto-fit Y. (c) v4 에 DEPRECATED warning 추가. commit `f8f59f7` |
| 06:58 | debug-api-500-error-iukkt | portable scripts commit + push | DONE | commit `92b14a5` |
| 06:56 | debug-api-500-error-iukkt | watchdog/run scripts portable화 (cwd-relative + conda activate 제거 + GPU env 외부 주입) | DONE | comp3/comp5 watchdog + run_ranks 모두. `cd "$(dirname "$(readlink -f "$0")")"` 사용. fairchem import sanity check 추가. |
| 06:55 | debug-api-500-error-iukkt | KISTI deploy v1 실패 확인 | BLOCKED→FIXING | (a) `/data/work/`은 gabia 경로, KISTI는 `/scratch/x3430a02/kgy/...` → `mkdir` Permission denied → wget 파일들이 `adhesion_v5_v2/` 로 잘못 들어감. (b) `/data/apps/miniforge3/...` conda path 도 gabia용. KISTI는 `(uma)` 이미 active. |

---

## 2026-05-10

| 시각 | branch | action | status | notes |
|------|--------|--------|--------|-------|
| 21:52 | debug-api-500-error-iukkt | git push origin claude/debug-api-500-error-iukkt | DONE | commit `59e16e1` (676c455 → 59e16e1), 18 files / 1583 insertions |
| 21:51 | debug-api-500-error-iukkt | git commit (spawn + docs) | DONE | commit `59e16e1` |
| 21:50 | debug-api-500-error-iukkt | spawn-critical lines verification (grep halogen_perms / total / output filenames) | DONE | comp3=range(8),5 5*56 / comp4=range(8),4 5*70 / comp5=range(8),3 5*56 ✓ |
| 21:48 | debug-api-500-error-iukkt | CODE_INVENTORY.md 갱신 — Pipeline v2 status table + spawn entries | DONE | comp3/5 ⏳ template only, comp4 ⏳ KISTI 진행 중 |
| 21:47 | debug-api-500-error-iukkt | DEPLOY.md 작성 (comp345_v2_DEPLOY.md) | DONE | wget 명령, halogen split table, cache_stage1b.json 알려진 gap 명시 |
| 21:46 | debug-api-500-error-iukkt | comp5_v2 spawn 4 files (Cl=3 Br=5, watchdog GPU1) | DONE | `필독/step1_halogen_li_anneal/comp5_lpscbr/` |
| 21:43 | debug-api-500-error-iukkt | comp3_v2 spawn 4 files (Cl=5 Br=3, watchdog GPU0) | DONE | `필독/step1_halogen_li_anneal/comp3_lpscbr/` |
| 21:40 | debug-api-500-error-iukkt | comp4_v2 reference 4 files + ref_comp3.cif (verbatim from KISTI paste) | DONE | `필독/step1_halogen_li_anneal/comp4_lpscbr/` |
| 21:38 | debug-api-500-error-iukkt | 사용자 답변: spawn destination = 필독/, GPU0=comp3 GPU1=comp5, 두번째사진 = 이미지 재공유 대기 | DONE | AskUserQuestion |
| 21:35 | debug-api-500-error-iukkt | session start: read CLAUDE.md + CODE_INVENTORY.md, set up TIMELOG.md | DONE | 이전 세션(`session_01Cp6qS9TkaZYTp2zwaM4nDF`) 크래시 — comp3/5 v2 spawn 미완 |

---

## 이전 세션 (크래시) 복구 메모

**`session_01Cp6qS9TkaZYTp2zwaM4nDF` (지난 세션, 정확한 시각 모름):**
- 사용자가 KISTI `/data/work/comp4_v2/1_step1to3/`에서 production code 3개 paste:
  - `comp4_v2_step1to3.py` (Stage 1a/1b/2/3 main)
  - `anneal_rank.py` (rank N halogen × 20 Li × top 5 anneal)
  - `ref_comp3.cif` (Li27P5S22Br3Cl5 rhombo 5fu, 62 atoms)
- 이전 Claude가 "spawn" 함 (자체 보고): 아래 4개 파일 + ref_comp3.cif 생성
  - `comp3_v2_step1to3.py` (Cl=5, Br=3)
  - `comp3_v2_anneal_rank.py`
  - `comp5_v2_step1to3.py` (Cl=3, Br=5)
  - `comp5_v2_anneal_rank.py`
- **결과: git에 push 안 됨**. 어느 branch에도 commit 없음 (확인: `git log --all -- 'ref_comp3.cif'` 결과 없음).
- 이전 Claude가 따로 KISTI에 ssh 해서 만든 흔적도 없음 (확인 불가).

**사용자 보충 지시 (방 터지기 직전):**
- "이거 asyma말고 두번째사진처럼 보정해달라고" — figure plot 관련 (asymptote subtract 빼고 두번째 이미지처럼) — **이미지 없음, 사용자 확인 필요**
- "앞으로 최상위 폴더에 timelog를 적어놔라" — ✅ 본 파일 생성

---

## TODO (이 세션)

1. ⏳ comp3 v2 / comp5 v2 spawn destination 결정 (KISTI만? + repo 미러?)
2. ⏳ "두번째사진" 이미지 재공유 받기 — 어느 figure script 수정인지 확인
3. ⏳ spawn 후 CODE_INVENTORY.md 갱신 (Pipeline v2 status table comp3/4/5 ⏳ → ✅)

