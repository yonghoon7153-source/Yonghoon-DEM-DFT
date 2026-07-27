# -*- coding: utf-8 -*-
"""
glossary.py — 용어 설명집 데이터.
각 항목: id/term/full/cat + what(개념) · how(계산·판독법) · ours(우리 캠페인 적용).
"카테고리 → 용어 → 세부(무엇/어떻게/우리것)"로 보면 분야가 다 잡히게.
"""

CATS_G = ["기초 이론", "전자 구조", "화학 결합", "기계 물성", "이온 수송", "계면·안정성", "MLIP·자동화", "방법론·모델링"]

GLOSSARY = [
# ── 기초 이론 ─────────────────────────────────────────
{"id":"dft","term":"DFT","full":"Density Functional Theory (밀도범함수이론)","cat":"기초 이론",
 "what":"수많은 전자의 상호작용 문제를 파동함수 대신 <b>전자 밀도 ρ(r)</b> 하나의 범함수로 바꿔 푸는 양자역학 계산법. 정확한 다체 슈뢰딩거 방정식은 못 푸니, Kohn–Sham이 '같은 밀도를 주는 가상의 비상호작용 전자계'로 치환해 풀 수 있게 만들었다. 바닥상태 에너지·힘·전자구조를 제1원리(경험 파라미터 없이)로 얻는다.",
 "how":"① 결정 구조(원자 좌표+격자) 입력 → ② 교환상관 범함수(PBE 등)와 기저(평면파+cutoff), pseudopotential, k-point 격자 선택 → ③ <b>SCF</b> 반복으로 전자밀도를 자기일관되게 수렴 → ④ 총에너지·힘(→구조최적화)·응력(→탄성/EOS)·고유값(→밴드/gap) 산출. 후처리로 DOS/ELF/Bader/COHP 등을 뽑는다.",
 "ours":"Quantum ESPRESSO(평면파+pseudopotential)로 gap·EOS·elastic·ε∞를, LOBSTER로 ICOHP를 계산. canonical 레시피는 methods 페이지 참조 — pseudo/ecut/k가 물성·조성마다 달라 비교 전 반드시 확인."},

{"id":"scf","term":"SCF","full":"Self-Consistent Field (자기일관장)","cat":"기초 이론",
 "what":"전자밀도가 만드는 퍼텐셜이 다시 그 밀도를 결정하는 '닭-달걀' 관계를, 초기 추정 → 계산 → 갱신을 반복해 <b>입출력이 일치(self-consistent)</b>할 때까지 수렴시키는 절차. DFT 한 스텝의 심장.",
 "how":"초기 밀도 → 퍼텐셜 → Kohn–Sham 방정식 풀어 새 밀도 → mixing(예: β=0.3)으로 섞어 갱신 → 에너지 변화(conv_thr, 예 1e-8 Ry)가 임계값 이하가 되면 수렴. iteration 수와 'estimated scf accuracy'로 진행을 본다.",
 "ours":"러너/watch가 'iteration #'과 accuracy를 추적. SCF가 iter 1~2 만에 'JOB DONE'이면 skip 의심(ε∞ 삽질의 원인이었음)."},

{"id":"pseudo","term":"Pseudopotential","full":"의사퍼텐셜 (USPP/PAW/NC)","cat":"기초 이론",
 "what":"화학결합에 거의 관여 안 하는 <b>내각(core) 전자</b>를 명시적으로 안 풀고 매끈한 유효 퍼텐셜로 대체해 계산량을 줄이는 근사. 종류: Norm-Conserving(NC, 정확·무겁), Ultrasoft(USPP, 낮은 cutoff·빠름), PAW(정확+재구성, LOBSTER 필수).",
 "how":"원소별 UPF 파일을 pseudo_dir에서 로드. 종류에 따라 필요 cutoff(ecutwfc/ecutrho)가 다르다(USPP는 낮게, PAW는 ecutrho 높게). <b>비교하려면 같은 종류·같은 cutoff여야</b> — 절대에너지·물성이 계열마다 다르므로.",
 "ours":"elastic/EOS/gap/ε∞ = USPP(li/s/cl/br v1.4.uspp + P rrkjus). LOBSTER(ICOHP) = all-PAW 필수. MD(UMA) = pseudo 개념 없음. 'comp1=PAW'로 착각했다가 백업 확인 후 USPP로 정정한 게 오늘 큰 교훈."},

{"id":"kpoint","term":"k-point","full":"브릴루앙 존 샘플링","cat":"기초 이론",
 "what":"주기적 결정에서 전자 상태는 역공간(k-space)의 함수라, 적분을 유한개 k점 격자로 근사한다. 격자가 촘촘할수록 정확하지만 무거움. <b>셀이 크면(역공간 작음) 적은 k로 충분</b>.",
 "how":"K_POINTS automatic n₁ n₂ n₃. 수렴은 절대 개수가 아니라 <b>k×L(격자길이 반영 밀도)</b>로 판단 — 큰 셀엔 작은 k. gap/전도체는 더 촘촘히 필요.",
 "ours":"comp1(cubic-52)=k444, modelc(rhombo-62)=k221. 셀이 달라 k숫자가 다른 게 정상 — comp2를 k222→k444로 올린 건 comp1과 같은 셀이라 밀도를 맞춘 것."},

{"id":"functional","term":"XC Functional","full":"교환상관 범함수 (PBE 등)","cat":"기초 이론",
 "what":"DFT에서 유일하게 근사가 들어가는 부분 = 전자 교환+상관 에너지. GGA(PBE)가 표준, 밴드갭을 <b>과소평가</b>하는 경향(HSE 같은 hybrid가 보정하나 무거움).",
 "how":"pseudopotential에 함께 지정(예 pbe). gap이 실험보다 작게 나오는 건 PBE의 알려진 한계 — 경향/상대비교엔 유효.",
 "ours":"PBE 표준. ORCA SDCP 분자는 r²SCAN-3c(meta-GGA)."},

# ── 전자 구조 ─────────────────────────────────────────
{"id":"bandgap","term":"Band gap","full":"밴드 갭","cat":"전자 구조",
 "what":"채워진 최고 준위(VBM)와 빈 최저 준위(CBM) 사이의 에너지 간극. 전자·이온 전도의 절연성과 전기화학 안정성의 1차 지표. SE는 전자절연·이온전도가 이상적이라 gap이 클수록 유리.",
 "how":"<b>fixed-occupation nscf의 VBM/CBM 고유값</b>으로 읽는 게 정본. DOS의 문턱(threshold)으로 읽으면 ~0.3 eV 과소평가되니 금지.",
 "ours":"canonical(eigenvalue): comp1 2.066 / comp2 2.04 / modelc 2.099 / lpsocl 2.2309 eV. DOS-threshold(1.76/1.82)는 폐기."},

{"id":"dos","term":"DOS","full":"Density of States (상태밀도)","cat":"전자 구조",
 "what":"에너지 E에서 전자가 차지할 수 있는 상태의 개수 분포 g(E). 어디에 상태가 몰려있고 어디가 비었는지(gap)를 보여준다. 페르미 준위 근처 형태가 전도 특성을 좌우.",
 "how":"① SCF → ② 촘촘한 k로 <b>nscf</b> → ③ dos.x/projwfc.x로 g(E) 산출 → ④ E축(페르미를 0으로) vs g(E) 그래프. gap = g(E)=0인 구간. 스무딩(가우시안 broadening) 적용해 그림.",
 "ours":"db/properties에 *_dos_smooth.csv(modelc/b2o3 등). 사이트 Charts 탭에서 클릭하면 Plotly로 렌더."},

{"id":"pdos","term":"PDOS","full":"Projected DOS (부분 상태밀도)","cat":"전자 구조",
 "what":"DOS를 <b>원소·궤도별로 분해</b>한 것. 'VBM은 어느 원자의 어느 오비탈에서 오는가'를 알려줘 결합의 화학적 기원을 규명.",
 "how":"projwfc.x가 각 원자 s/p/d에 파동함수를 투영. 원소별 곡선을 겹쳐 그린다.",
 "ours":"lpsocl/lpscl16/b2o3 pdos_element CSV. argyrodite VBM = S 3p(자유 S²⁻ + PS₄ 비결합 S) — Banik/Zeier와 정합."},

{"id":"elf","term":"ELF","full":"Electron Localization Function","cat":"전자 구조",
 "what":"전자가 공간의 각 지점에 <b>얼마나 국소화(쌍을 이뤄 몰려있나)</b>되어 있는지를 0~1로 나타내는 실공간 스칼라장. 공유결합(높은 값의 다리)·고립전자쌍·이온결합(원자 주변 껍질)을 <b>눈으로</b> 구분.",
 "how":"밀도와 그 기울기로 계산 → cube 파일 → VESTA/사이트에서 등가면(isosurface) 또는 슬라이스로 본다. <b>0.5 근처=금속적 균질, 1에 가까운 다리=공유결합, 원자 주변 국소 껍질=이온결합</b>. ICOBI(정량 결합차수)와 상보적(ELF는 시각, ICOBI는 숫자).",
 "ours":"b2o3_elf_bonds.csv 등. P–S 공유 골격 vs Li–X 이온성을 ELF로 시각화."},

{"id":"bader","term":"Bader charge","full":"Bader 전하 분석","cat":"전자 구조",
 "what":"전자밀도의 '골짜기(zero-flux 면)'로 공간을 원자별 영역으로 나눠, 각 원자가 <b>실제로 몇 개의 전자를 가졌나(산화수 경향)</b>를 정량. 전하 이동·도핑 효과를 본다.",
 "how":"밀도 cube → Bader 코드(zero-flux partition) → 원자별 전하. 형식전하와 비교해 이온성/공유성 판단.",
 "ours":"bader_b2o3_vs_lpscl16.csv. O/B 도핑 시 전하 재분배 확인."},

# ── 화학 결합 ─────────────────────────────────────────
{"id":"cohp","term":"COHP / ICOHP","full":"Crystal Orbital Hamilton Population","cat":"화학 결합",
 "what":"두 원자 사이 결합의 <b>세기(에너지 기여)</b>를 에너지축으로 분해. 음수=결합성(bonding), 양수=반결합성. 에너지 적분값 <b>ICOHP</b>(eV, 음수 클수록 강함)가 결합강도 단일 지표.",
 "how":"DFT 파동함수를 원자궤도 기저로 재투영(LOBSTER) → 원자쌍별 -COHP(E) → 페르미까지 적분 = ICOHP. <b>all-PAW nscf + charge spilling<5%</b> 필요.",
 "ours":"comp1 P–S ≈ −6.0(강한 공유 골격) ≫ Li–Cl −2.11 > Li–Br −1.93(약한 이온). Br이 약해 이온전도↑·기계강성엔 둔감. minimal-basis −5.12는 artifact(폐기)."},

{"id":"cobi","term":"COBI / ICOBI","full":"Crystal Orbital Bond Index","cat":"화학 결합",
 "what":"결합 <b>차수(order, 몇 겹 결합인가)</b>를 무차원으로. ICOHP가 '얼마나 세냐(에너지)'라면 ICOBI는 '얼마나 겹치냐(전자쌍 공유 정도)'. 이온결합은 ICOBI가 작다.",
 "how":"LOBSTER가 COHP와 동시에 산출(cobiGenerator). ICOBI≈1이면 단일 공유결합.",
 "ours":"comp2 P–S 0.925(공유) vs Li–Br 0.280(이온성). ELF(시각)와 ICOBI(숫자)로 결합성격을 교차 확인."},

{"id":"lobster","term":"LOBSTER","full":"결합 후처리 프로그램","cat":"화학 결합",
 "what":"평면파 DFT 결과를 국소 원자궤도 기저로 재투영해 COHP/COBI/전하를 뽑는 후처리 도구.",
 "how":"QE nscf(all-PAW, nbnd 넉넉, ecut 높게) → lobsterin 설정 → LOBSTER 실행. charge spilling<5%가 신뢰 기준.",
 "ours":"comp2 spilling 1.37% ✅. all-PAW라 elastic(USPP)과 pseudo가 다른 게 정상(물성별 축이 다름)."},

# ── 기계 물성 ─────────────────────────────────────────
{"id":"eos","term":"EOS / B₀","full":"상태방정식 · 부피탄성률","cat":"기계 물성",
 "what":"부피를 바꾸며 에너지 E(V)를 재 <b>Birch–Murnaghan</b>으로 피팅. 최소점=V₀, 곡률=<b>B₀(부피탄성률, 압축 저항)</b>. hydrostatic(등방 압축) 강성.",
 "how":"여러 부피에서 고정셀 relax → E(V) → BM3 fit → V₀, B₀, B′. 좁은 그리드면 B′는 신뢰 못 함.",
 "ours":"comp1 26.23 / comp2 25.8 / modelc 21.71 / lpsocl 24.71 GPa. elastic의 B_VRH(harmonic)와는 다른 양이니 혼동 금지."},

{"id":"elastic","term":"Elastic Cij / VRH","full":"탄성상수 · Voigt-Reuss-Hill","cat":"기계 물성",
 "what":"작은 변형에 대한 응력 반응 = 탄성텐서 Cij(6×6). 이걸 방향 평균해 <b>B(부피)·G(전단)·E(영률)</b>를 얻는다(VRH=Voigt상한·Reuss하한의 평균). Pugh(B/G)로 연성/취성, Debye로 격자 강성.",
 "how":"6 Voigt 방향 × ±변형 12개 SCF → 응력에서 Cij 열별 추출 → VRH 평균. <b>relaxed-ion</b>(변형 후 원자 이완)이 실험과 맞음(clamped-ion은 ~2.3× 과대). 노이즈는 k-density·strain 크기로 좌우.",
 "ours":"comp1 relaxed E_VRH 22.06(문헌 23 일치). comp2만 comp1과 같은 cubic-52라 완전비교쌍 — 지금 USPP·k444로 재측정 중. modelc/lpsocl은 rhombo셀이라 순위/각주만."},

# ── 이온 수송 ─────────────────────────────────────────
{"id":"bvse","term":"BVSE","full":"Bond Valence Site Energy","cat":"이온 수송",
 "what":"결합가(bond valence) 경험식으로 Li⁺가 격자 각 지점에서 느끼는 <b>이동 퍼텐셜 지도</b>를 싸게 계산. 낮은 계곡을 잇는 경로 = 이온 채널, 문턱 = 대략적 확산 장벽.",
 "how":"softBV 파라미터(Li–X R₀)로 BVSE=(BVS−1)² 맵 → 등가면/퍼콜레이션 분석으로 채널 연결성. DFT-NEB보다 훨씬 빠른 스크리닝.",
 "ours":"comp1/modelc/b2o3 BVSE cube+percolation. 정량·순위는 원본 주기셀 값만 인용(큐빅박스는 표시용)."},

{"id":"md","term":"MD (MLIP)","full":"분자동역학 · UMA","cat":"이온 수송",
 "what":"원자를 뉴턴 방정식으로 시간에 따라 움직여 <b>유한온도에서 Li가 실제로 확산하는 궤적</b>을 얻는다. 힘을 DFT로 매번 계산하면 비싸서, 학습된 퍼텐셜(MLIP, 우리는 UMA)로 대체.",
 "how":"Langevin NVT(dt 2fs, 온도 고정) 평형 5ps + 생산 200ps. 여러 온도·여러 시드로 통계. MLIP라 <b>pseudopotential 개념이 없다</b>(DFT와 다른 축).",
 "ours":"UMA-s-1p1(omat), 600/800/1000K, 3-seed. 절대값 인용 금지·멀티시드 판정만. UMA는 Li₃N엔 금지(편향)."},

{"id":"msd","term":"MSD → D","full":"Mean Squared Displacement","cat":"이온 수송",
 "what":"시간에 따른 이온의 <b>평균제곱변위</b> ⟨r²(t)⟩. 확산이면 시간에 선형 → 기울기가 확산계수 D (Einstein 관계 ⟨r²⟩=6Dt).",
 "how":"MD 궤적에서 Li들의 변위를 시간창(예 2–50ps)으로 피팅. 초반 ballistic·후반 통계부족 구간은 제외.",
 "ours":"MSD 창 2–50ps 고정."},

{"id":"arrhenius","term":"Arrhenius / Ea","full":"활성화에너지 · 전도도","cat":"이온 수송",
 "what":"확산이 온도에 지수적으로 의존: D=D₀·exp(−Ea/kT). log D vs 1/T 직선의 기울기 = <b>활성화에너지 Ea</b>(낮을수록 빠른 전도). σ는 Nernst–Einstein으로 D에서 환산.",
 "how":"3온도(600/800/1000K) D를 log-1/T에 피팅. 저온(400/500K)은 통계부족으로 제외 판정. Ea 오차막대는 시드 분산.",
 "ours":"comp1 0.253 / modelc 0.224 / lpsocl 0.271 eV. comp2 계산중(s2 단일 0.312 — 3-seed 완성 전 판정 보류)."},

# ── 계면·안정성 ───────────────────────────────────────
{"id":"phonon","term":"Phonon","full":"격자 진동 · 동역학 안정성","cat":"계면·안정성",
 "what":"결정 격자의 진동 모드(포논) 주파수. <b>허수(음수) 주파수가 있으면 구조가 불안정</b>(안장점). 구조가 진짜 최소점인지 검증.",
 "how":"작은 변위에 대한 힘상수(동역학 행렬)의 고유값 → 주파수. Γ점만으로 1차 스크리닝, 전체 안정성은 q-격자.",
 "ours":"comp2 v3 champion STABLE(최저 +32.7 cm⁻¹). 첫 champion이 saddle(−45.8i)이라 phonon 검증이 없었으면 큰일날 뻔."},

{"id":"neb","term":"NEB / CI-NEB","full":"Nudged Elastic Band","cat":"계면·안정성",
 "what":"두 안정 상태(예 이웃 site) 사이 <b>최소에너지경로(MEP)와 안장점(장벽 Ea)</b>을 찾는 방법. 이미지 여러 개를 스프링으로 연결해 경로를 이완, CI(climbing image)가 안장을 정밀화.",
 "how":"끝점 2개 relax → 중간 이미지 보간 → 각 이미지 힘 계산·이완 반복(iteration). 프로파일 피크가 중간(대칭)이면 진짜 안장, 단조증가면 경로/끝점 재검토.",
 "ours":"VGCF/hBN Li 확산: hBN표면 ~0.007(near-flat) · graphene 0.273(문헌 일치) · gallery 0.357(양면 confinement trap). 2L2L 진행중."},

{"id":"esw","term":"ESW / onset","full":"전기화학 안정성창 (grand-potential)","cat":"계면·안정성",
 "what":"SE가 산화/환원 없이 버티는 전압 범위. grand-potential(Li 화학퍼텐셜 함수) 방법으로 분해 시작 전압(onset)과 분해 산물을 예측. VBM≠onset(반응 자유에너지가 결정).",
 "how":"조성-전압 상평형(pymatgen grand-potential phase diagram) → onset 전압·반응식. 실험 CV와 대조.",
 "ours":"argyrodite onset 2.256V(Son2025 '<2.5V'·Zuo2022 반응식과 정합). 산화 분해: Li₆PS₅Cl→Li₃PS₄+LiCl+S."},

{"id":"adhesion","term":"Adhesion / Wad","full":"계면 접착일","cat":"계면·안정성",
 "what":"두 상(예 SE|전극)을 떼는 데 드는 에너지 = 계면 접착 강도. 기계적 밀착·계면 저항과 연결.",
 "how":"슬랩 두 개를 붙인 계면 에너지 − 각각의 표면 에너지. 기하 승계·저β 믹싱으로 수렴.",
 "ours":"adhesion.json. MLIP-elastic 상관은 2026-07-23 deprecated(재계산 필요)."},

# ── MLIP·자동화 ───────────────────────────────────────
{"id":"mlip","term":"MLIP / UMA","full":"Machine-Learned Interatomic Potential","cat":"MLIP·자동화",
 "what":"DFT 데이터로 학습해 <b>원자간 힘을 DFT 정확도로 즉시</b> 내주는 신경망 퍼텐셜. MD·대규모·다샘플에 필수(DFT는 너무 비쌈). UMA는 foundation model(범용 학습).",
 "how":"구조→에너지/힘을 학습. pseudopotential·k-point 개념 없음. 검증(우리 조성에 편향 없나)이 중요.",
 "ours":"UMA-s-1p1로 MD·phonon·MLIP-EOS. LPSCl 계열엔 검증된 표준, Li₃N엔 금지."},

# ── 방법론·모델링 ─────────────────────────────────────
{"id":"ordered_vs_disordered","term":"Ordered vs Disordered","full":"질서/무질서 구조 선택 — 어떤 LPSCl 셀로 계산하나","cat":"방법론·모델링",
 "what":"'질서셀 vs 무질서셀 누가 맞냐'는 잘못된 질문 — 진짜 질문은 <b>어떤 양을 계산하느냐</b>. 0 K DFT는 에너지 E를, 합성온도(500–550°C)의 실험 무질서 구조는 F = E − TS_config를 산다. 무질서는 metastable이 아니라 <b>합성 T의 진짜 자유에너지 최소</b>를 급랭으로 얼려둔 것. Rietveld 점유율(예 48h occ 0.5)은 시공간 평균 확률이지 스냅샷이 아니다.",
 "how":"<b>0 K 미분·에너지(phonon·gap·formation/hull·elastic) → relaxed ordered 셀 / 유한온도 수송(σ·Ea) → 무질서 유지 + 다중 배열 앙상블 평균</b>. 무질서(48h 빈자리·anti-site)가 전도의 원인 그 자체라 질서화 = 원인 삭제 = Ea 과대. 경고 사례: Deng SQS A=0.92 vs Torii ordered A=1.09 — 무질서 처리만으로 결론 부호 반전.",
 "ours":"canonical gap 4개 = ordered 52-atom 정형셀. 수송은 d=0.5/1.0 × cfg0/1/2 disorder ensemble(UMA anneal+relax; v1 un-relaxed swap은 artifact 폐기). 단일 config 판정 금지(단일시드 1.33× 철회 교훈). 우리 A=1.14 ≈ Torii 1.09는 공유 편향(둘 다 ordered) 가능성 자기비판 유지."},
]

def by_category():
    out = {c: [] for c in CATS_G}
    for g in GLOSSARY:
        out.setdefault(g["cat"], []).append(g)
    return out
