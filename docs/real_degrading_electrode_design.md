# 진짜 열화하는 전극(real degrading electrode) — 하이브리드 사이클 chemo-mech 설계

2026-07-22, 사용자 지시: "난 진짜 전극을 만들고 싶어" + (A) A10 심화 + (B) STEP4 계면상.
사이클 열화를 **voxel 지오메트리에 실제 반영**하되, 매 사이클 전체 파이프라인을 돌리지
않는 **하이브리드**(ledger 빠른 경로 + MPM 진짜 재변형 앵커).  A10 설계문서
(`a10_cycle_chemomech_design.md`)의 옵션 A/B를 **결합·확정**한 상위 설계.

**★ 적대리뷰 반영 (2026-07-22, wf_05cb35c3, 22 확정/major 3·minor 17)**: M1(§2.5 외삽 논거
코드-반증 → 정직 재라벨+LOAO/blind/shape-sweep) · M2(§4 σ_ion≡1 = 하한, 3앵커→2앵커) ·
M3(§3 A-2 crack = J2 MPM 불가 → (a)기하 debond/void + (b)FEM/phase-field) · minor N1-N5(§6
조각별 체크리스트).  ★ 현 산출 = **frozen-geometry contact-ledger 프록시**(0/6 조각 구현).

## 0. 핵심 결정 (사용자 승인 2026-07-22)
- **깊이 = 하이브리드**: ledger(전 N, 빠름) + MPM 재변형(적응 앵커 N∈{0,5,10,25,50,100},
  초기 촘촘 §2.5, 진짜 지오메트리)로 ledger 규칙을 **캘리브+검증**.  → ledger = "진짜 지오메트리
  열화"에 정합된 빠른 **기전-동기 보간**(앵커-사이 N-모양은 ASSUMED-FORM, LOAO/blind로 오차 노출
  §2.5).  정확도 부족 시 앵커 증설 → 풀MPM 수렴.
- **frame[5] 분업 엄수**: MPM = 기계 재변형(지오메트리·응력장·SE morphology·void/재유동) ·
  DEM/ledger = 접촉망·percolation·transport 부기 · **취성 crack(G_c/Auerbach) = FEM/phase-field 소관**
  (현 J2 MPM 아님, M3) · STEP4 = 화학 계면상(SEI/CEI).  겹치지 않게.

## 1. 현 상태 (출발점)
- **Pristine 지오메트리 = 이미 진짜**: MPM 300MPa 소성압밀 결과(se_dump = 실제 변형 SE 형상).
- **A10 v1 (옵션 A ledger)**: AM 수축을 **gap 계산 안에서만** 반영(강체구), Griffith/Bucci CZM →
  f_broken/A_rel/R_ct/σ_rel/Γ* → Kirchhoff 재솔브.  **voxel 지오메트리는 안 바뀜.**
- **한계(정직)**: 입자내부 균열·소성 재배열·τ 스파이크 과소평가.  ← MPM 재변형 앵커가 메움.

## 2. 하이브리드 아키텍처

```
 사이클 N ─┬─ [빠른 경로] ledger(전 N):  AM수축→gap→CZM→f_broken→Kirchhoff → σ(N),R_contact(N)
           │        ▲ 캘리브(G_c·δcr·re-contact f)
           └─ [진짜 앵커] MPM 재변형(적응 N):
                 AM 반경 ΔV/SOC (SC 수축/poly 팽창) → MPM 재평형(SE 소성 재유동, void 생성)
                 → 응력장·plastic-strain field → ★재복셀화★
                 → STEP3/4 재솔브 → σ_e(N)·coverage(N)·void(N)·두께(N) [진짜 지오메트리]
                 (취성 crack은 A-2(b) FEM/phase-field 소관 — 여기선 void/재유동만, M3)
```
- **캘리브 루프**: ledger의 **실제 궤적-구동 DOF = {δcr, ε=dv·soc_swing, rewet_frac}**(+§2.5-2
  주입항 계수)를 **실험(§4)**에 회귀, MPM 앵커로 shape 검증.  ⚠ **G_c는 fit 목록서 제외**(∂궤적/∂G_c=0
  인 inert, Γ*-게이트 표기만; 진짜 레버 원하면 Griffith 에너지판정 구현).  제약: **독립-구속 수 ≥ DOF**
  (원 앵커 수 아님; N=0·구성적 σ_ion≡1은 카운트 제외).  δcr↔rewet_frac 분리식별성은 profile-likelihood로.
- **검증 대조군(옵션 C)**: 측정 R_int(N) 밴드(A11-② rint_cycle_traj) 안에 드는가.

## 2.5. ★ "외삽 아니냐" 우려 — 정직한 현황 (적대리뷰 M1 반영, 2026-07-22)
사용자 우려: ledger가 MPM 앵커 사이를 채우면 **외삽 아닌가 → 부정확**.
**★ 적대리뷰 판정(코드 반증, CONFIRMED): 사용자 직관이 옳다. 아직 실질 해소 안 됨.**
- 앵커-사이 궤적의 **N-모양**(=채워지는 바로 그 부분)은 검증된 기전이 아니라 **Miner ASSUMED-FORM**이
  만든다 (`cycle_contact_ledger.py` L222-225·L270이 스스로 "ASSUMED-FORM…중간 궤적은 가정" 라벨).
  gap_nm은 루프 밖 1회 계산(L177)이라 접촉 간 응력 재분배 없음; N=1 즉시파단 소진 후 N>1은 누적법칙만.
- "G_c를 최소자승 fit"은 **불가능**: `a.gc`는 `gamma_star`(L191) 스칼라에만 등장 → ∂궤적/∂G_c=0 →
  **G_c는 궤적을 안 움직이는 inert 파라미터**.  실제 궤적-구동 DOF = {δcr, ε=dv·soc_swing, rewet_frac}.
- σ_ion·σ_e 채널이 구성적 ≡1이라(§4·M2) "노브 2개(G_c·δcr)" 과적합-방지 논거도 성립 불가.
⇒ 앵커 사이는 "검증된 물리 예측"이 **아니라** "**가정된 모양의 보간**".  "외삽 아님"(N∈[0,100] 내)은
  기술적으론 참이나 **무관** — 진짜 위험은 **misspecified-shape 보간 오차**이고, 아래 (4)의 in-sample
  오차막대는 이걸 **못 잰다(하한만)**.

**★ 실질 해소책 (값싸고 즉시 — 이걸 해야 우려가 진짜 닫힘):**
1. **정직 재라벨**: ledger = "**기전-동기 basis에 앵커를 회귀하는 보간(interpolation)**; 앵커-사이
   N-모양(누적법칙)은 MPM/So로 검증 전까지 **ASSUMED-FORM**(코드 라벨과 일치)".  "MECHANISTIC =
   검증된 물리 예측" 주장 **삭제**.
2. **누적법칙 shape-family 스윕** {√N, 선형, Miner}: 앵커가 법칙들을 실제로 **구별**하는지 검사.
   구별 못 하면 모양은 **식별불가** → 그렇게 명시 (자매 `rint_cycle_traj.py` §F1 shape-family 밴드 규율의
   자연 확장).
3. **적응적 앵커 밀도**: 초기(N=0/5/10/25) 촘촘 (So "첫사이클 최대손실"), 후기(50/100) 성김.
   외삽 구간(N>100)은 마지막 앵커로 **닫음**.
4. **정직한 오차 노출 — in-sample 아님**: (a) **LOAO**(leave-one-anchor-out): 5앵커 fit→6번째 예측
   →그 오차 = 앵커-사이 진짜 오차.  (b) **비앵커 중간 N(예 N=15)에 blind full-MPM 1점** = 진짜
   out-of-sample 검증.  at-anchor 잔차는 '하한' 라벨로만 병기.  앵커 증설 트리거를 in-sample 아니라
   **LOAO/blind 오차**로.
5. **분리 식별성**: live DOF = {δcr, ε, rewet_frac}; dv·soc_swing·fatigue-form은 문헌 production-lock;
   **δcr↔rewet_frac 2D profile-likelihood로 분리 식별성 입증**.  G_c는 fit 목록에서 제거(Γ*-게이트
   표기만; 진짜 레버로 쓰려면 Griffith U_el(δ) vs G_c·A 에너지판정을 구현).
6. **frame[4] 정합**: ledger 노브 캘리브 타깃 = **실험(§4 Kang&Shin/Yun)**, MPM은 독립 교차검증
   (일치=신뢰·불일치=정량화 한계).  MPM→ledger는 frame[5] "COUPLING=scaffold" 승인 멀티피델리티라
   검증만 실험에 두면 정당 — "MPM-vs-ledger 일치"를 *독립* 검증이라 부르지 말 것.
7. **최대정확 상한 = 풀 MPM**: 앵커 증설로 연속 수렴(정확도↔비용 다이얼).

⇒ **정직한 결론**: "해소할 올바른 골격은 있으나(적응앵커→풀MPM 수렴), 현 논거는 오버클레임이었음 →
(1)재라벨 + (2)shape-sweep + (4)LOAO·blind로 교체하면 우려가 **실질 해소**".  그 전까지 앵커-사이는
ASSUMED-FORM 보간으로 정직 표기.

## 3. 조각 (구현 단위 — 각 3각 적대리뷰)

### (A) 기계 열화
- **A-1. MPM 사이클 재변형 모듈** (`mpm3d_compaction.py --cycle-deform`): am_scaffold 반경을
  ΔV(SOC)로 조정 → 고정AM 갱신 → SE MPM 재평형(기존 servo/hold) → se_dump' 재변형 형상 + **재복셀
  그리드-불변**(dx·원점·nx/ny/nz·FLOOR·lateral_box·SE→id 위상 전 N 고정, N4).  ★GPU (체크포인트만).
  frame[5]=MPM 소관.  **⚠ poly 부호(M3/N3)**: SC=격자수축(−5.1%, 접촉손실).  poly=Parks +19% 외피
  **팽창**+내부 void 분율(접촉 유지/압축) — 강체 등방 수축으로 모델링 금지; 격자 ΔV/3 전량을 외반경에
  걸지 말 것(A9 균열흡수 할인+Kang&Shin 크기가중, `--dv-pct-poly` 노브).  등방근사(Kondrakov c축
  비등방 무시) 명시 or c-정렬 최악값 밴드.  입계파괴는 a10 §7대로 FEM/MPM 채널 라우팅(정정 확정).
- **A-2. 기하 열화 = coverage/void (M3 재작성 — J2 MPM이 정당하게 주는 것만)**:
  - (a) **AM-SE 분리 = 기하 debond + SE 소성 재유동**을 **coverage(N)/void(N)로 보고** (MPM의 검증된
    강점: void-fill·morphology).  "응력-파괴/crack"으로 부르지 **않음** — 현 J2 MPM엔 응력장·crack
    필드 자체가 없고(szz는 0차원 전역 스칼라), von Mises가 σ_y에 클램프돼 Griffith 문턱과 겹쳐
    crack≡항복으로 퇴화하며, 취성 LPSCl(K_IC 0.23)에 연성 dg 측도는 재료클래스 불일치이기 때문.
  - (b) **진짜 취성 파괴가 필요하면 = FEM/phase-field 소관**(frame[5], 현 J2 MPM 아님).  필요조건:
    cohesive-zone/phase-field(Bucci) + **명시 AM-SE traction-separation** + **per-point 응력텐서 export**
    + **crack-band 정칙화**(G_c를 dx로 스케일해 소산 mesh-객관화) + **dx-수렴 테스트**(void·τ vs 격자
    ≥2 해상도).  수렴 전까지 MPM crack-void는 **ASSUMED-FORM 라벨**(Miner와 동일 규율).
  - AM 파단은 기존 DEM Auerbach(f_intact)와 **중복 없이** 결합(AM내부=frame[5] FEM/MPM, 접촉면=ledger).
- **A-3. ledger 캘리브·보간**: `cycle_contact_ledger.py`에 `--mpm-anchor N=path` 훅 →
  MPM 앵커로 **{δcr,ε,rewet_frac} fit(G_c 제외)** → 전 N 보간.  출력 coverage(N)·σ_e/σ_ion(N)·
  R_contact(N) + **LOAO/blind 오차막대**(§2.5-4).  ⚠ σ_ion(N)은 v1 구성적 상수(M2) → MPM 앵커점에만
  국한, ledger 보간 금지.
- **A-4. percolation(N)**: 재복셀/ledger 후 연결성분(econn·f_perc) → 끊김 궤적.  rnm_sigma에서
  **'CG 미수렴(침묵 0.0)' vs '미퍼콜' 분리**(connected_components 판정만 진짜 0.0, 이미 구현).

### (B) 화학 열화
- **B-1. STEP4 계면상 성장** (`step4_dyn.py`): 지금 ASR_film=0 슬롯을 **ASR_film(N)** 성장으로:
  Koerver 첫사이클 점프 + √N(SC, 확산제한 CEI) / 선형(poly) — R_int(N) 설계문서 §3.1 형태 재사용.
  → R_chem(N) 직접 산출.  방전곡선(N) = 계면상↑ → 분극↑.
- **B-2. R_int(N) 통합**: R_int(N)=R_contact(N)[A, ledger+MPM] + R_chem(N)[B, STEP4] +
  R_collector(N)[기존].  → 이종기술 cycled(150)를 **assumed-form에서 모델-산출로 승격**.

## 4. 출력·검증 (진짜 전극의 증거)
- 궤적: σ_e(N)·coverage(N)·두께(N)·R_contact/chem/int(N)·용량(N)·방전곡선(N)·Γ*(N).
  ⚠ **σ_ion(N)은 v1서 구성적 상수(≡1)** — MPM 앵커점에만, ledger 보간 금지(M2).
- 앵커 검증: ① Kang&Shin R_int(N) **4.4×↔B-NCA(bimodal) / 1.5×↔U-NCA(mono)** 모양 (라벨 페어링
  정정, N1-F10); 기계 몫 = **방향** 재현(mono R_ct 1.05× / bimodal 1.51×), 크기(4.4×) 미재현 = 화학이
  bimodal 증폭 ② So 첫사이클 최대손실 ③ **Yun R_ion +23% = 미포착(구조적 하한)**: v1은 ε_SE=0으로
  σ_ion_rel≡1.000 상수라 재현 불가 → '정합' 아니라 **알려진 하한 오차**로 리포트(M2) ④ Jung SC/PC
  retention 부호 ⑤ 측정 R_int(N) 밴드 내(옵션 C).  → **"2앵커(방향) 정합 + σ_ion 하한"**(3앵커 정합 아님).
- **진짜 지오메트리 증거**: MPM 앵커의 재변형 se_dump'(**void 생성·SE 재유동** 시각화; crack은 A-2(b)
  구현 전까지 표기 안 함) via viz_mpm.  crack 필드 없는데 crack 시각화를 증거로 주장 금지(M3).

## 5. 구현 순서 (GPU 상황 + 적대리뷰 F17 게이트 반영)
- **구현 상태: 0/6 조각.** 현 산출 = **frozen-geometry contact-ledger 열화 프록시(옵션 A) only**
  (F18).  "하이브리드/진짜 열화 전극" 주장은 A-1(--cycle-deform se_dump' 1점) + A-3(--mpm-anchor
  캘리브·held-out 검증) 착지까지 **보류**.  로드맵서 '설계 확정'↔'구현 완료' 분리.
- **순서**: (i) 문서 blocker M1·M2·M3 반영(이 커밋) → (ii) **B-1**(STEP4 계면상, N1 리뷰, selftest)
  → (iii) **A-3** 스캐폴드('unvalidated scaffold' 플래그 뒤) → (iv) **A-1 거친 MPM 앵커 1점 먼저**
  (F17: A-3 production 커밋 전 필수) → (v) A-3 캘리브 production → (vi) A-2(재작성판 (a)기하/void).
- **F17 blind 게이트**: **앵커 1계열을 캘리브 미사용 blind 검증셋으로 예약** — 성공판정은 blind에서만
  (Kang/Yun로 짓고 같은 데이터로 검증하는 것 방지).
- 각 조각 = **코드·전기화학·물리 3각 적대리뷰** 후 커밋.

## 6. 미결 + 조각별 3각리뷰 체크리스트 (적대리뷰 minor N1-N5 편입)
**설계 미결:**
1. ΔV 앵커: SC −5.1%(Kondrakov) vs 5.9%(Yun/Kang) — 스윕축.  poly는 팽창 부호(A-1 M3).
2. G_c: Γ*-게이트 표기만(fit 아님); 진짜 레버 원하면 Griffith 에너지판정 구현.
3. MPM 재변형 SE 재유동 프로토콜: servo(정압) vs hold(변위) — 재습윤 물리 + **재팽창 BC**(새 고체
   AM셀서 SE 체적보존 퇴출/이류, mask 성장금지+platen 완화; N4-F5a) 명문화 후 A-1 방전절반 코딩.
4. B-1 계면상 성장 형태 poly/SC 분기 = D_s/i0 분리축 규약.

**조각별 커밋-전 체크리스트 (minor):**
- **N1 (R_int 전방모델, B-1/B-2)**: R_chem = **kim2025 R_ct(N) 독립앵커 직접주입**(측정−모델 잔차 아님);
  **로그-가법 분해** ln R_rel = ln g_mech + ln g_chem (동일계면 곱셈 co-scale, 가법이 교차항 전가);
  전하이동은 **i0(N)↓ 한 채널만**(ASR_film=순수 필름 옴성, 이중계산 금지); 성장법칙 = coating(첫점프
  진폭)×crystallinity(지수), √N는 CEI 두께 일반형만(흑연-SEI 계수 이식 금지); "assumed-form→모델-산출
  승격"은 Jung/Conforto fit 후에만(현재 취소).
- **N2 (Γ* 게이트)**: repo Γ*는 Bucci 원식과 **H 부호 반대 + A_AM 소실**(크기의존) → **케이스 내 상대
  라벨로만**, **절대 verdict 'damage-expected' 삭제**.  헤드라인은 δcr-vs-입자크기 gap(AM_P 6µm 102nm
  &gt;δcr / AM_S 2µm 34nm &lt;δcr)으로.
- **N3 (poly 부호)**: A-1에 반영(팽창+void).  헤드라인 무영향(방향≠크기), 문서/강조 수준.
- **N4 (수치 위생)**: 재복셀 그리드-불변(≥2 해상도 384·512 비율수렴); coverage(N)=analytic만; partial
  모드 **seed 앙상블(≥8, mean±band)**; 재팽창 BC 명문화; A-3는 A-1 앵커 착지 전 'unvalidated' 플래그.
- **N5 (정직성)**: 제목 '진짜 열화 전극'은 A-1/A-3 착지까지 'frozen-geometry 프록시'로; §2.5-2 "물리
  주입"을 **명시적 MPM-ROM**(6-10 스냅샷→(N,ΔV)→{void,τ,coverage,area} 저차원맵 + LOAO)로 형식화;
  ov0 층위혼합(18×-연화 겹침 + 문헌 δcr) → gap 비교 전 ov0 real-E 재스케일 or MPM 접촉-개구 직접사용.
