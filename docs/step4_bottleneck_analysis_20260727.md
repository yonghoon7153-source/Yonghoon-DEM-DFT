# STEP4 2C 병목 해부 — near-null 근본원인 · 게이트 정정 · 치료 레이어링 (2026-07-27)

케이스: **VGCF1_PTFE1** (260421_215235_ab3785) · repo branch `claude/stoic-knuth-NObVQ`
근거: V100 실측 포렌식 + 5-축 병렬 진단(솔버 해부 / 그리드 물리 실측 / 옛-2C 회귀 분리 /
R1-R5 평가 / A5 미니벤치) + 같은 세션의 치료 구현(`scripts/step4_dyn.py`).
⚠ 본문 라인 번호는 **진단 시점(치료 패치 전) step4_dyn.py 기준** — 패치 후 +400여 줄
이동했으므로 함수명(_cg / _nearnull_amg_M / newton / CellSystem.__init__)을 정본 좌표로 삼을 것.

---

## 0. 한 줄 요약

**섬유 additive(VGCF 1wt%, 서브-퍼콜)가 e-망을 수만 개의 약결속/부유 조각으로 파편화**
→ 구조적 near-null(λ~1e-11, 차원 O(10⁴)≫12) → GPU Jacobi-CG 사망 → CPU nnAMG 11 s/iter
→ Newton 깊은 보정해 목표(abs ~2.7e-13~2.7e-14 = **0.05×교정 노이즈바닥**, rtol 아님)에서
솔브당 18-46분 → 스텝당 1-3 h → 2C 완주 사실상 불가.  기존 완화(6394a01 게이트)는
**대수적 no-op**(정정 §4).  치료 = 부유 pruning(해-불변, 기본 ON) + EW inexact-Newton(기본 ON)
+ GPU V-cycle 미러(기본 ON) + σ-contrast cap(opt-in) — 전부 구현·selftest 완료, **V100 실검증 대기**.

---

## 1. 증상 타임라인

| 시점 | 사건 | 수치 |
|---|---|---|
| 2026-07-20~21 | (기준선) 2C CCCV **완주** — 3.18 mAh/cm² SDCP/SBE/DBE 침대 | 72.48 µm, dof ≈2.8-2.9M, near-null 장치 없는 솔버(49687dd)로 정상 종료 |
| 2026-07-22 | 새 VGCF1_PTFE1 침대 0.2C에서 CG 발산/정체 | 8b2853f SPD-safe 폴백 → 6d72345/77fa751 수용 완화 → 1cf8d43 **near-null-B AMG(nnAMG)** 이식 |
| 2026-07-23 | nnAMG 실전 미발동 발견(트리거 결함) → 근본수정 + 승자 직행 래치 | 5559420, bf9dd2e (~34% 절감) |
| ~07-26 | **0.2C 실측: 3일에 방전창 2.1% (스텝 19)** | 스텝당 수 시간 |
| 07-26 | 2C 재시도 → 매 솔브 nnAMG escalate → 계층 재빌드 **OOM Killed** → `_NN_ACCEPT_RTOL=1e-7` 게이트 | 6394a01 |
| 07-26~27 | 게이트 후에도 **스텝당 1-3 h** (nnAMG 100-250 it × 11 s/it × Newton 2-4회) | 2C 완주 며칠 규모 = 사실상 불가 |
| 07-27 | 5-축 진단 → 게이트 no-op 확정 + near-null 정체 실측 + 치료 구현 | 본 문서 |

V100 실측 솔버 단가 (dof 4,443,161 = e 2,699,262 + i 1,743,899; BV 1,214,921면):

| 경로 | 단가 | 도달 바닥 | 비고 |
|---|---|---|---|
| GPU Jacobi-CG (cupy) | — | 미수렴 (info=20000) | 런 초반 gpu_dead 래치 |
| CPU plain AMG | 빌드 56-77 s + 2.1-2.6 s/it | abs ~2.7e-12 stall | 목표(2.9e-13) 미달 |
| CPU Jacobi | 0.55 s/it | abs ~1.4e-12 stall | 자기바닥 |
| **nnAMG** (near-null-B) | **11 s/it** (LOBPCG 12-15 s 런1회) | 수렴함 | 얕은 50 it≈9분 / 깊은 100-250 it=**18-46분** |

---

## 2. 진단 1 — 솔버 아키텍처 전수 해부 (step4_dyn.py 1721줄)

### 2-1. _cg 6단 사다리 + 라치 5개
① GPU Jacobi-CG → ② 전처리 선택(nnamg_direct 래치면 nnAMG 직행 / amg_ok면 plain AMG /
Jacobi) → ③ stale-AMG 재구축 → ④ Jacobi SPD-safe 폴백 → ⑤ nnAMG escalate → ⑥ 최종가드
(시작보다 나쁘면 x0 반환 + MPM_S4_DUMP_FAIL 덤프).  라치는 `sys_._pc_cache`에 살아
**스텝을 넘어 지속**:

| 래치 | set 조건 | 해제 | 효과 |
|---|---|---|---|
| gpu_dead | GPU 실솔브 미수렴/예외 | 없음 | 이후 GPU 시도 전부 생략 |
| deep_weak | deep(r<1e-4) 솔브 info≠0 | **없음 (sticky)** | 이후 모든 Newton이 r<1e-4에서 **조기 break** |
| amg_useless | AMG 발산+Jacobi 승 | 없음 | plain AMG 생략 |
| nnamg_direct | escalate에서 nnAMG 승자 | 직행해 열화 시 | 1순위 직행 + 재escalate 생략 |
| nnamg_dead | nnAMG 구축 자체 불가 | 없음 | escalate 봉쇄 |

전처리 교체는 CG 해를 바꾸지 않음(해-불변 주석) → R1(GPU V-cycle)은 안전한 drop-in.

### 2-2. ★깊은 abs 목표(2.7e-13~2.72e-14)의 출처 = atol, rtol 아님
- newton 보정해 CG는 `_cg(J, −Fv, rtol=1e-5, atol=atol_cg)` 단일 콜사이트,
  **atol_cg = 0.05·agg_floor_abs** (agg_floor_abs = 4×교정 KCL 노이즈, calibrate_floor).
- tgt = max(rtol·‖b‖, atol)에서 b=−Fv → Newton 수렴할수록 ‖Fv‖↓ → rtol항 붕괴 →
  ‖Fv‖₂ < atol/1e-5 (≈2.7e-9) 순간 **목표가 절대 atol에 고정**.
- 산술 정합: floor_rel≈1.6e-5 → agg_floor_abs≈5.4e-12 → atol_cg≈**2.7e-13**(현장 로그
  '목표 2.91e-13'); 2.72e-14는 meas_agg≈1.36e-13으로 교정된 런의 0.05×floor.
- ⚠ 현장 귀속 "rtol 1e-9·‖b‖"는 **오독** — 2.91e-13/‖b‖≈1e-9였을 뿐, `_cg` 시그니처
  기본 rtol=1e-9는 프로덕션에서 아무도 안 씀(rtol=1e-9 사용처는 테스트 1곳뿐).
- 이 절대 목표가 Jacobi 자기바닥(1.4e-12)·plain AMG 정체(2.7e-12)보다 **1-2자릿수 아래**
  → nnAMG escalate는 게이트와 무관하게 **정당** (배경의 '정직한 한계' 코드 수준 확증).

### 2-3. 스텝당 1-3 h의 구성
스텝 = solve_galv → Illinois 괄호법이 ev(V) **2-4회** 호출 → 각 ev = newton 1콜 →
콜당 비-deep 솔브(nnAMG 직행 ~50 it≈9분) 1-2회 + 깊은 솔브(atol 목표, 100-250 it=18-46분)
0-1회(deep_weak 래치 후엔 0).  **지배 비용 = nnAMG apply 11 s/it × 총 CG iter** →
R1이 단가(11→0.1-0.3 s/it), R2가 횟수(느슨한 η)를 깎는 직교 지렛대.

### 2-4. CPU-전용 조각 비용 귀속
plain AMG 빌드 56-77 s(재구축 반복 가능) / nnAMG: LOBPCG 12벡터 12-15 s(런 1회) +
sym-scale 3중곱+B-주입 AMG 빌드(**OOM 위험 지점**, B 9열이 coarse 블록을 키움 = plain 대비
4-5× 느린 원인 일부) + apply ~11 s/it / scipy cg Jacobi 0.55 s/it (SpMV ~33.5M nnz 지배).
GPU-가능 조각은 현재 cupy Jacobi-CG 블록뿐 → R1의 표적은 **apply**.

---

## 3. 진단 2 — 그리드 물리 실측 (near-null의 정체를 데이터로 증명)

실측 대상: 실제 step4_grid.npz (125×125×301, vox 0.4 µm, z_top 119.3 µm;
sid: void 5.5 / AM_S 49.3 / VGCF 8.1 / SE 37.1 %).

### 3-1. near-null 정체 = 6-conn VGCF 조각의 약결속/부유 모드

| 측정 | 값 | 의미 |
|---|---|---|
| VGCF 26-conn 성분 | 7,103 (최대 346,049 vox = 90%) | 모서리-접촉으론 "거의 한 덩어리" |
| VGCF **6-conn**(=FV 행렬 그래프) 성분 | **54,650** (med 2 vox, max 1,148) | 행렬이 보는 실제 조각 수 |
| e-망(AM∪VGCF) 6-conn 성분 | 8,115 (집전체 접촉 152) | |
| **부유** 성분 (AM 0 ∧ 집전체 0) | **7,963개 / 18,453 vox** (e-망의 0.68%) | BV면(AM 전용)도 판도 없음 = **정확 특이 블록** |
| ├ ≥2복셀 | 4,112 | ‖J·v‖_inf = **0.0** 직접 증명 (프로덕션 CellSystem 조립) |
| └ 단일복셀 | 3,851 | diag=0 zero-row (GPU 1/diag 가드 없음 → inf 위험) |
| 약결속 면 g-비 | VGCF-AM harm(100, 0.01) ≈ 0.02 vs 내부 100 = **5,000×** | 클러스터당 저-λ 모드 ~1개 |

union-anchored 필터(cond_e|cond_i 라벨)는 SE가 앵커라 SE-매몰 VGCF 섬을 keep — 실측
드롭 22복셀뿐.  ⇒ J는 Newton 내내 특이.  **"모서리-접촉 웹, 면-분절 섬유"가 핵심 병리.**

### 3-2. near-null 차원 = O(10⁴) ≫ 12 (R3 기각 근거)
full-res 변분 상계(Courant-Fischer, LOBPCG 무관하게 엄밀): Jacobi-프레임 λ_D<1e-3 성분
29,704 / **<1e-4: 10,561** / <1e-5: 76 (+정확0 4,112).  LOBPCG 교차확인(k=40): 최저 40개
전부 λ_D<1e-5, D-질량 99.6-99.8% VGCF 국소화, 모드가 다수 클러스터에 분산(준축퇴 부공간
회전) = 차원≫k의 독립 증거.  실런의 "LOBPCG 12벡터 λ 1.22-1.45e-11"은 꼬리 맨 아래 12개.

### 3-3. σ-contrast cap 실측 (조건수 이득 vs 물리 비용)

| cap | λ_D 꼬리 상승 | λ_D<1e-4 성분 | Dirichlet CG iters | σ_eff(e) Δ | 셀-V 왜곡 @2C |
|---|---|---|---|---|---|
| 없음 | — | 10,561 | 276 | (2.821e-3 S/cm) | — |
| **200×** | **44-49×** (이론 50× 일치) | **0** | **52** | **−7.82%** | **≤2.5 µV** (총 9.3 mV의 0.03%) |
| 1000× | | | 104 | −2.57% | |
| 2000× | | | 140 | −1.34% | |

★레거시 voxel_conductivity.py:139-143의 "<0.2%"는 이 VGCF-풍부 기하(8.1 vol%, 119 µm)에
**비전이** — full-res −7.8%가 정정(stride-2의 −0.23%는 다운샘플이 섬유 연결을 파괴한
아티팩트).  근거 해부: VGCF-AM 계면 g는 −0.49%만 변함(조화평균 AM 지배); 손실은 긴
관통-섬유 경로에 집중.  셀-레벨은 전자 옴강하 0.01-0.03 mV ≪ 이온 84-90 mV라 안전.
⇒ **시간전개(V·용량)엔 cap 200× 안전 / σ_e-류 수송 메트릭 보고는 uncapped 유지 필수.**
단 부유 클러스터의 정확0은 cap으로 불변 → pruning이 별도로 필요.

---

## 4. 진단 3 — "예전 2C는 됐다" 회귀 분리 + ★정직한 정정

### 4-1. 옛 완주 침대 vs 현 침대

| | 2C 완주 (07-20~21) | 현 VGCF1_PTFE1 (실패) | 배율 |
|---|---|---|---|
| areal / 두께 | 3.18 mAh/cm² / 72.48 µm | 6.70 / 119.3 µm | 2.1× / 1.6× |
| dof (e+i) | ≈2.77M/2.90M | 4.44M | 1.6× |
| BV 면 | 425k/504k | 1,214,921 | 2.4× |
| I_1C | 9.068e-8 A | 1.676e-7 A | 1.85× |
| R_int / D_s | 0 / 3e-14 | 50 Ω·cm² / 3e-15 | 물리축 |
| VGCF | **2.97wt%, 47,683섬유, 퍼콜(econn 100%, 고립 0)** | 1wt%, 서브-퍼콜 (부유 7,963) | ★위상 차이 |
| 솔버 | 49687dd (near-null 장치 전무)로 완주 | nnAMG 필수 | |

### 4-2. ★브리핑 정정 (기록 교체 필수)
"옛 2C 침대는 VGCF/PTFE 섬유 없음"은 **오류** — 옛 침대에도 VGCF 2.97wt%(부피 기준
현 케이스의 ~2.2배)가 있었고 **완주했다**.  ⇒ "섬유가 생겨서 느려졌다"는 서사는 틀림.
회귀의 지배 원인은 **양이 아니라 연결 위상**: 1wt% 서브-퍼콜 파편화(부유 7,963 +
약결속 46,536 클러스터).

### 4-3. 원인 랭킹
① **VGCF 1wt% 서브-퍼콜 파편화** (구조적 영공간 ~7,963 + 약결속 near-null O(10⁴))
≫ ② 후막/대형계 (dof 1.6×, 조건수 ~2.6×, BV 2.4×) > ③ σ 대비 10⁴ (**양쪽 시대 동일 =
트리거 아님, 증폭기** — 약결속면 368,576개의 g-비 2.0e-4) > ④ R_int/D_s/창 (물리축,
조건수 무관).

### 4-4. 클러스터 수 규약 (혼동 방지)

| 집계 | 수 | 규약 |
|---|---|---|
| econn (payload MPM점, 26-conn) | 15,260 | 뷰어/econn 지표 |
| npz sid 26-conn | 7,103 | 모서리-접촉 |
| npz sid **6-conn** | **54,650** | **행렬(FV)이 보는 수 = 솔버-관련** |
| e-망 부유 (AM·판 무접촉) | 7,963 | 정확 특이 |

전부 O(10⁴) 동일 방향 — 정의·해상도 차이일 뿐 모순 아님.

---

## 5. ★정직한 정정 — 6394a01 게이트는 대수적 no-op

- `_NN_ACCEPT_RTOL=1e-7` 게이트: `_accept = max(_tgt, 1e-7·‖b‖)`인데 유일 프로덕션
  콜사이트가 rtol=1e-5를 넘기므로 1e-5·‖b‖ ≥ 1e-7·‖b‖ 항상 성립 → **_accept ≡ _tgt**.
  게이트는 escalate 판정을 **단 한 번도 바꾸지 않았다** (git show 6394a01로 확인 —
  그 시점에도 rtol=1e-5).  6394a01의 단위테스트는 rtol=1e-9 시나리오라 프로덕션과 불일치.
- 실전에서 매-솔브 escalate를 실제로 막은 것은 (i) _CGStop 자기-바닥 info=0 휴리스틱
  (best_r ≤ 0.1·r0)과 (ii) bf9dd2e의 nnamg_direct 래치.
- 원리적으로도 못 막음: accept가 ‖b‖-상대라 후기 Newton(‖b‖ 노이즈로 붕괴)에선
  1e-7·‖b‖ ≪ atol.  ⇒ **OOM 재발 방지의 실담보가 게이트가 아니므로**, 래치 이전 구간에
  조건이 재현되면 재빌드 OOM 재발 가능 — "게이트가 지켜준다"는 전제 폐기.
- 따라서 6394a01은 "OOM 근본해결"이 아니라 **불필요-escalate 서사의 오귀속**이었고,
  속도 병목(깊은 보정해의 nnAMG 정당 필요)은 애초에 게이트 사정권 밖.
- 코드 반영: `_NN_ACCEPT_RTOL` 주석 정정(no-op 명기) + selftest **S5a**(100조합 대수
  no-op 회귀 고정) + 실효 대안 `MPM_S4_NN_ACCEPT_ABS_FRAC`(절대바닥 결합형 accept,
  기본 0=OFF) 추가.
- deep_weak 래치도 명시: 첫 deep-실패 후 모든 Newton이 r<1e-4에서 조기 break(해제 없음)
  — conv.worst_resid 배지가 정직 보고하지만 "2C tol_rel=1e-8 수렴"으로 오독 금지.

---

## 6. 진단 4·5 — 치료 후보 R1-R5 평가와 미니벤치

### 6-1. 평가 요약

| 후보 | 판정 | 기대 이득 | 공수/리스크 | 핵심 근거 |
|---|---|---|---|---|
| C0 부유 pruning | ★채택 (기본 ON) | GPU-CG 부활 후보, 정확0 4,112 소거 | 공짜·**해-불변**(RHS=0) | ‖J·v‖=0 직접 증명; STEP3 n_floating_dropped 선례 |
| R2 EW inexact-Newton | ★채택 (기본 ON) | 총 CG iter 2-5× 절감 | S, 물리 해 불변(정확-F 재계산이 흡수) | 초기 Newton 목표 η~1e-2 → nnAMG 발동을 후반으로 국한 |
| R1 GPU V-cycle 미러 | ★채택 (기본 ON, GPU시) | 11 → 0.05-0.3 s/it (30-100×) | M; 메모리 0.7-2.4 GB ≪ 32 GB | 전처리=해-불변; ω-Jacobi 대칭 스무더로 SPD 보장 |
| R4 σ-contrast cap | 채택 (opt-in) | λ꼬리 44-49×↑, CG 276→52 | S + **A/B 정량 런 필수** | §3-3; σ_eff −7.8%라 보고용은 uncapped |
| R5 supernode lumping | v2 보류 | near-null **존재 자체 소멸**, dof −12% | L (pos_* 위치맵·φ(z)·audit 연쇄) | 허브 max 840면 ≪ 옛 supernode-B 병리 5,000 — 원리적 배제 아님 |
| R3 deflation k=64-128 | **기각** | — | — | 차원 O(10⁴)의 <1% 커버; 소-k deflation 발산 실측(1cf8d43); B-확장은 coarse 비대→OOM 재유발 |

R3 기각은 `_nearnull_amg_M` docstring에 박아 재론 방지.  R2·게이트류가 공유하는 가정
("near-null 방향 오차는 J·v≈0라 잔차·merit에 안 실림 = 전류 ~0 고립 클러스터의 φ 오차
= 물리 무해")의 원천 해소는 C0/R4/R5뿐 — §8 정직 한계.

### 6-2. A5 미니벤치 (클라우드 CPU 테스트베드)
- **병리-보존 다운샘플 레시피 확정**: any-presence 풀링은 VGCF 8.1→59%로 폭증시켜
  병리를 소멸(단일 백본) — **carbon 점유 ≥s³/4 문턱 풀링**이 상분율(8.9 vs 8.1%)과
  클러스터 통계(stride-2: 17,126 ≈ econn 15,260)를 동시 재현.  후속 프록시 연구 필수 규약.
- 실계 8-자릿수 대비 보존 조립 성공 (stride-3: N=168,033, BV 132,079면, nnz 1.08M =
  실계 1/26) — (a)Jacobi (b)AMG (c)nnAMG-B12 (c2)프로덕션 미러 (d)B48 (d')deflation48
  (e)cap200 + EW 프록시 + LOBPCG 꼬리 + cap ΔI_tot 비교 장치 완비.
- **§F1 정직**: 솔버 타이밍 표는 보고 시점 미완(배터리 실행 중) — 수치 날조 없음.
  재현: `scratchpad/bench_a5.py --stride 3 --jac-cap 30000 --jac-budget 180 --k48`
  (→bench_s3.json) 후 `--stride 2`.  ⚠ scratchpad는 세션-휘발 — 표 완성 시 본 문서에 추기.
- 외삽 주의: iter-수 **비율**만 신뢰, 절대 s/it를 4.44M dof로 선형 스케일 금지(대역폭 한계).

---

## 7. 치료 구현 (이번 세션, scripts/step4_dyn.py — V100 실검증 대기)

전부 selftest(`_selftest_solver` S1-S5) 통과, env try/finally 복원, 기본값은
"구 경로 bitwise 보존 또는 해-불변"만 ON:

| env | 기본 | 내용 | 해 영향 |
|---|---|---|---|
| `MPM_S4_PRUNE_FLOAT` | **1 (ON)** | CellSystem 조립 시 e-망 6-conn 라벨 → AM(sid 1·2)·집전체 band 무접촉 성분 드롭 (카운트 로그+meta) | **해-불변** (RHS=0 정확특이 제거) |
| `MPM_S4_EW` | **1 (ON)** | newton rtol=1e-5 → EW choice-2 η_k=clip(0.9·(‖F_k‖/‖F_{k-1}‖)², 1e-5, 0.1) + safeguard + over-solve 하한 + Armijo 거부 시 tight(1e-5) 재솔브 1회 | Newton 고정점 불변 (η_min=구식 1e-5 = 느슨화 전용) |
| `MPM_S4_GPU_AMG` (+`_F32`) | **1 (ON)** (GPU∧cupy시) | pyamg 계층 CPU 1회 빌드(ω-Jacobi 2/3 대칭 스무더) → A/P/R cupy CSR 미러, V(1,1) apply GPU, coarsest CPU LU 캐시, 예외 1회 시 CPU 자가 강등 | 전처리=해-불변; F32는 전처리 정밀도만 |
| `MPM_S4_CONTRAST_CAP` | **0 (OFF)** | rasterize 후 망별 min-positive×cap 클램프(레거시 규약); 대비>1e3 감지 시 200 권장 힌트 출력; capped 런은 meta에 기록 → σ-메트릭 보고 금지 라벨 | e-망 σ_eff −7.8%@200× (셀-V ≤2.5 µV — A/B 승격 전 opt-in) |
| `MPM_S4_ATOL_FLOOR_FRAC` | 0.05 (=현행) | 깊은 보정해 atol = frac·agg_floor_abs; 0.5로 올리면 목표가 Jacobi 자기바닥 위 = nnAMG 없이 종료 | opt-in — V100 KCL/E-bal 감사 통과 전 기본 변경 금지 |
| `MPM_S4_NN_ACCEPT_ABS_FRAC` | 0 (OFF) | escalate accept에 frac·agg_floor_abs 병합 (‖b‖-상대 게이트의 후기-Newton 무력 보완) | opt-in |

부수: `_NN_ACCEPT_RTOL` no-op 정정 주석 + S5a 회귀 · GPU Jacobi 1/diag zero-row 가드 경로는
pruning이 원인(단일복셀 부유) 자체를 제거 · run meta에 `solver_env`(pruning 카운트/cap/EW/
GPU-AMG/atol_frac) 감사 기록 — capped 런 판별 자동화.

**기대 체인** (V100 검증 전 추정치임을 명기): R2(횟수 2-5×↓) × R1(단가 11→0.05-0.3 s/it)
→ 스텝당 1-3 h → **~2-10분**; C0로 GPU Jacobi-CG 부활 시 추가 단축; R4 ON이면 nnAMG
사다리 자체가 비활성권 후보.

**남은 것 (V100)**: ① 해-불변 검증 A/B — PRUNE on/off로 delivered/E-bal/KCL 동일성
② cap A/B — V(t) RMS·delivered <0.1%p, j_BV 상관 >0.999, collector 접점 gB 민감도
(유일 국소 민감점), Q_ohm(e) carbon 몫 ③ 2C 재실행 본런 ④ (선택) VGCF 2.97wt% 조성을
이 6.7 mAh 침대에 시딩한 1런 = "조성(퍼콜) vs 두께" 최종 분리.

---

## 8. 근본원인 서사 + 잔존하는 정직한 한계

**서사**: VGCF 1wt%는 이 침대에서 서브-퍼콜 — 26-conn으론 웹처럼 보이지만 FV 행렬의
6-conn으론 54,650조각이고, 각 조각은 내부 g=100 vs AM-계면 g≈0.02의 5,000× 약결속
(+ 7,963개는 아예 부유 = 정확 특이).  σ 대비 10⁴는 이를 near-null(λ~1e-11, 차원 O(10⁴))로
증폭하고, 후막(dof 4.44M)이 비용을 키운다.  GPU Jacobi가 죽고, plain AMG/Jacobi는
abs ~1e-12에서 자기바닥에 앉는데, Newton 깊은 보정해 목표는 atol=0.05×교정 노이즈바닥
= 2.7e-13~2.7e-14로 그 **아래** — nnAMG(11 s/it)만 도달 가능 → 18-46분/솔브 → 1-3 h/스텝.

**잔존 한계 (§F1 명기)**:
1. 깊은 보정해 목표가 Jacobi 자기바닥 아래인 구조는 C0/R2/R1로도 불변 — nnAMG의
   "정당한 필요"는 남는다.  회피는 `MPM_S4_ATOL_FLOOR_FRAC=0.5`(opt-in, 감사 통과 조건).
2. EW·accept 게이트류는 공히 "near-null 방향 오차 = 물리 무해" 가정 위 — 원천 해소는
   C0(부유)·R4(감쇠)·R5(소멸)뿐.  AM-브릿지 약결속 46,536 클러스터의 near-null은
   pruning 후에도 잔존.
3. 모든 배속 수치는 **V100 실검증 전 기대치**; cap의 −7.8%/≤2.5 µV는 이 기하 실측 —
   다른 VGCF wt%/두께로 ASSUMED 전이 금지(재측정).
4. capped 결합(BV) 시스템의 Newton 심층 수렴은 e-망 스펙트럼/σ_eff 분석의 **예상**이지
   증명 아님 — V100 1런 검증 항목.
5. A5 타이밍 표 미완(§6-2) — 완성 후 추기.

---

## 9. STEP6 surrogate — 파이프라인 내 위치 (수요-측 치료, R1-R5와 직교)

R1-R5가 "솔브 단가/횟수"를 깎는 **공급-측**이라면, STEP6은 "비싼 솔브 호출 수 자체"를
줄이는 **수요-측**: `STEP4 실솔브(앵커) ↔ STEP6 전파(surrogate) ↔ 후보 스크리닝`.

설계 요지 (`scripts/step6_surrogate.py` v1, MLIP식 — 병렬 임무 산출 설계서):
- STEP4 npz 코퍼스에서 (state_t → state_{t+1}) **전이쌍** 추출; 쿨롱 계수
  (Δx̄=−I·dt/cap)는 **정확 물리 하드코딩**, η/확산-지연 **잔차만 학습** (MLIP 규약).
- numpy-only **ridge 위원회**(bootstrap + random feature subset): 평균=예측,
  분산=오차밴드(mV); **σ>gate → ANCHOR-NEEDED** 마킹 = 실솔버 호출 지점
  (on-the-fly active learning) + ev warm-start 제공.
- 기존 자산 재사용: ml_cycle_surrogate(feature 스키마·import-guard·provenance) ·
  ml_design_loop(scalarize/APP_OBJECTIVES/sobol → rank_candidates 점수화; 위원회-draw
  argmax 빈도로 p_pick = Thompson식) · eis_drt_ica(R0/R_ct/τ_w 물리소자 = 스텝별 유효저항
  Q_*/I² feature) · cycling_data_ingest(§F1 게이트 규약).
- selftest = 합성 RC-방전 ODE(TEST-ONLY) — 클라우드 numpy-only 통과 설계.
- 규약: 모든 출력 **SURROGATE/UNCALIBRATED** 라벨 + **LOCO(런 단위)** 검증 강제.
- 정직 한계: 앵커 호출 시점의 깊은 보정해 nnAMG 필요는 STEP6으로도 잔존 —
  공급-측(§7)과 병용해야 총 벽시계가 내려간다.

---

## 10. V100 실행 가이드 (2C 재실행)

```bash
cd ~/Yonghoon-DEM-DFT && git pull                  # 치료 반영 (step4_dyn.py)
cd <VGCF1_PTFE1 킷 폴더>                            # step4_grid.npz 있는 곳
source ~/Yonghoon-DEM-DFT/scripts/activate_dem.sh

# 기본 런 (pruning·EW·GPU V-cycle 전부 기본 ON — env 불필요):
bash step4_only.sh

# cap 권장 런 (A/B 'on' 팔 — 시간전개 전용, σ-메트릭 보고 금지):
MPM_S4_CONTRAST_CAP=200 bash step4_only.sh

# 회귀분리/검증 팔 (필요 시):
MPM_S4_PRUNE_FLOAT=0 bash step4_only.sh            # 해-불변 A/B (delivered/E-bal 동일해야)
MPM_S4_EW=0 MPM_S4_GPU_AMG=0 bash step4_only.sh    # 구식 경로 bitwise 복원
# (opt-in, 감사 통과 후에만) MPM_S4_ATOL_FLOOR_FRAC=0.5 — 깊은 목표를 노이즈바닥의 1/2로
```

기록할 것: 스텝당 벽시계 · 솔버 경로 로그(GPU 생존/pruning 카운트/η 궤적/nnAMG 발동 여부)
· meta `solver_env` · KCL/E-bal 감사 · cap 팔은 V(t)·delivered·j_BV 상관 비교(§7 승격 조건).

---

*근거 데이터: V100 포렌식(임무 브리핑) · step4_grid.npz 직접 분석(진단2·5, scratchpad
a2_*/bench_a5 계열 — 세션-휘발) · git 49687dd/8b2853f/…/6394a01 커밋 본문(진단3) ·
docs/sdcp_318_base_sbe_dbe_comparison.md(옛 침대 사양) · voxel_conductivity.py:139-143
(cap 선례).  본 문서가 이 사안의 정본; 세션 기록의 "옛 침대 섬유 없음" 서술은 §4-2로 정정.*

---

## 부록 — 3렌즈 적대검증 결과 (2026-07-27 resume, wf_707e0321)

**V1 수치리뷰: PASS-with-findings** — 6개 검증축(전처리 대칭성 7e-15·SPD 실측·EW 무한루프
불가·cupy-부재 bitwise·라치 상태기계 적대프로브·실그리드 pruning 7,954성분 재현) 회귀 없음.
발견 medium 1 + low 4 → **medium(cap이 i-망에도 적용되는 경로: 토이서 셀-V 0.516mV 왜곡,
A2 근거는 e-망 전용)은 즉시 수정** — cap을 e-망 전용으로 제한, i-망 고대비는 경고만.
low 중 2건 수정(EW safeguard dead-code → 클립-전 η 저장 / step6 np.trapezoid WSL 가드),
2건 이월(GPU 자가강등 mid-CG 전처리 교체 = best-effort 문서화, V100서 확인 · i-망 부유
171성분/180복셀 = e-망 pruning이 98.6% 해소, 잔여는 v2).

**V2 §F1 리뷰: PASS — 위반 0건.** 라벨(SURROGATE/UNCALIBRATED/ASSUMED/TEST-ONLY) 전수 확인,
날조 앵커 0, 문서↔실그리드 수치 전부 exact 재현(8,115성분·부유 7,963·VGCF 54,650조각 등),
sklearn 은닉 의존 없음(AST). selftest 2회 md5 동일(결정론).

**V3 통합+재벤치: PASS 2/2.** selftest 46줄 전부 OK. stride-3 병리-보존 벤치(N=168k):
- Jacobi-CG: **cap200 → 7,362→1,418 iter = ×5.2** (A2 독립실측 276→52=×5.3과 교차검증 일치)
- AMG-PCG: iter ×46-51 (uncapped 159 it / capped 144 it)
- GPU 배속·EW 상한은 클라우드 미검증 → **V100 A/B 프로토콜로 확정** (아래 실행 가이드).

수정 반영 후 재검증: STEP4-V2 SELFTEST PASS + step6 8/8 (2026-07-27).
