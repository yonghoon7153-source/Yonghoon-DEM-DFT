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

{"id":"scf", "doc":"dft", "doc_sec":"§8 Kohn-Sham 방정식과 SCF","term":"SCF","full":"Self-Consistent Field (자기일관장)","cat":"기초 이론",
 "what":"전자밀도가 만드는 퍼텐셜이 다시 그 밀도를 결정하는 '닭-달걀' 관계를, 초기 추정 → 계산 → 갱신을 반복해 <b>입출력이 일치(self-consistent)</b>할 때까지 수렴시키는 절차. DFT 한 스텝의 심장.",
 "how":"초기 밀도 → 퍼텐셜 → Kohn–Sham 방정식 풀어 새 밀도 → mixing(예: β=0.3)으로 섞어 갱신 → 에너지 변화(conv_thr, 예 1e-8 Ry)가 임계값 이하가 되면 수렴. iteration 수와 'estimated scf accuracy'로 진행을 본다.",
 "ours":"러너/watch가 'iteration #'과 accuracy를 추적. SCF가 iter 1~2 만에 'JOB DONE'이면 skip 의심(ε∞ 삽질의 원인이었음)."},

{"id":"pseudo","term":"Pseudopotential","full":"의사퍼텐셜 (USPP/PAW/NC)","cat":"기초 이론",
 "what":"화학결합에 거의 관여 안 하는 <b>내각(core) 전자</b>를 명시적으로 안 풀고 매끈한 유효 퍼텐셜로 대체해 계산량을 줄이는 근사. 종류: Norm-Conserving(NC, 정확·무겁), Ultrasoft(USPP, 낮은 cutoff·빠름), PAW(정확+재구성, LOBSTER 필수).",
 "how":"원소별 UPF 파일을 pseudo_dir에서 로드. 종류에 따라 필요 cutoff(ecutwfc/ecutrho)가 다르다(USPP는 낮게, PAW는 ecutrho 높게). <b>비교하려면 같은 종류·같은 cutoff여야</b> — 절대에너지·물성이 계열마다 다르므로.",
 "ours":"elastic/EOS/gap/ε∞ = USPP(li/s/cl/br v1.4.uspp + P rrkjus). LOBSTER(ICOHP) = all-PAW 필수. MD(UMA) = pseudo 개념 없음. 'comp1=PAW'로 착각했다가 백업 확인 후 USPP로 정정한 게 오늘 큰 교훈."},

{"id":"kpoint", "doc":"dft", "doc_sec":"§10 Energy Cutoff와 K-point","term":"k-point","full":"브릴루앙 존 샘플링","cat":"기초 이론",
 "what":"주기적 결정에서 전자 상태는 역공간(k-space)의 함수라, 적분을 유한개 k점 격자로 근사한다. 격자가 촘촘할수록 정확하지만 무거움. <b>셀이 크면(역공간 작음) 적은 k로 충분</b>.",
 "how":"K_POINTS automatic n₁ n₂ n₃. 수렴은 절대 개수가 아니라 <b>k×L(격자길이 반영 밀도)</b>로 판단 — 큰 셀엔 작은 k. gap/전도체는 더 촘촘히 필요.",
 "ours":"comp1(cubic-52)=k444, modelc(rhombo-62)=k221. 셀이 달라 k숫자가 다른 게 정상 — comp2를 k222→k444로 올린 건 comp1과 같은 셀이라 밀도를 맞춘 것."},

{"id":"functional", "doc":"dft", "doc_sec":"§7 Hohenberg-Kohn · §8 Kohn-Sham (XC 항)","term":"XC Functional","full":"교환상관 범함수 (PBE 등)","cat":"기초 이론",
 "what":"DFT에서 유일하게 근사가 들어가는 부분 = 전자 교환+상관 에너지. GGA(PBE)가 표준, 밴드갭을 <b>과소평가</b>하는 경향(HSE 같은 hybrid가 보정하나 무거움).",
 "how":"pseudopotential에 함께 지정(예 pbe). gap이 실험보다 작게 나오는 건 PBE의 알려진 한계 — 경향/상대비교엔 유효.",
 "ours":"PBE 표준. ORCA SDCP 분자는 r²SCAN-3c(meta-GGA)."},

# ── 전자 구조 ─────────────────────────────────────────
{"id":"bandgap","term":"Band gap","full":"밴드 갭","cat":"전자 구조",
 "what":"채워진 최고 준위(VBM)와 빈 최저 준위(CBM) 사이의 에너지 간극. SE는 전자절연·이온전도가 이상적이라 bulk intrinsic 캐리어(σ_e ∝ exp(−Eg/2kT)) 관점에선 gap이 클수록 유리. <b>단 전기화학 안정성의 지표는 아니다</b> — 분해 onset은 반응 자유에너지가 결정하고 band-edge는 분해창을 2–3× 과대평가한다(Schwietert 2020; 우리 직접 증거: comp1/modelc VBM이 0.32 eV 다른데 onset은 동일). ESW 항목 참조.",
 "how":"<b>fixed-occupation nscf의 VBM/CBM 고유값</b>으로 읽는 게 정본. DOS의 문턱(threshold)으로 읽으면 ~0.3 eV 과소평가되니 금지.",
 "ours":"canonical(eigenvalue): comp1 2.066 / modelc 2.099 / +B₂O₃ 1.9671 / lpsocl 2.2309 eV · comp2 2.04는 <b>잠정</b>(legacy band_gaps, fixed-occ 재확인중 — eigenvalue canonical 아님). DOS-threshold(1.76/1.82)는 폐기. ⚠ 도핑 델타는 <b>같은 호스트끼리</b>: +O(LPSOCl)는 modelc 기준 +0.132, +B₂O₃는 modelc 기준 −0.132(comp1 2.066을 before로 쓰면 Cl 증량 효과가 섞인다). 그리고 gap↑이 실측 전자전도도 하락을 뜻하진 않는다 — Nd 도핑에선 bulk gap이 0.55 eV <b>좁아지는데</b> 실측 σ_e는 떨어졌다(계면/미세구조 지배, electronic.json)."},

{"id":"dos", "doc":"bandgap", "doc_sec":"§4 왜 DOS-threshold 판독은 틀리나","term":"DOS","full":"Density of States (상태밀도)","cat":"전자 구조",
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
 "ours":"골격 P–S: comp1 −5.938 / comp2 −5.913(강한 공유) ≫ 이온결합 Li–X. <b>Li–Cl/Li–Br(−2.111 / −1.934)은 comp2 값</b>이다 — comp1엔 Br이 없고 comp1의 Li–Cl은 −1.861. Li–Br이 Li–Cl보다 약한 건 <b>격자 연화</b>로 나타난다(comp2 E_VRH 22.06→20.03, B_VRH −18.2%; 동일 USPP·k444·cubic-52 비교쌍). ⚠ 이온전도 이득은 <b>미확인</b> — comp2 σ300 중앙 0.41× comp1, 3-seed 범위 0.12–1.48× inconclusive. '기계강성엔 둔감'도 틀렸다(bulk −18%는 계열 내 최대 변화). minimal-basis −5.12는 artifact(폐기)."},

{"id":"cobi", "doc":"cohp", "doc_sec":"§4 ICOBI — 결합 차수","term":"COBI / ICOBI","full":"Crystal Orbital Bond Index","cat":"화학 결합",
 "what":"결합 <b>차수(order, 몇 겹 결합인가)</b>를 무차원으로. ICOHP가 '얼마나 세냐(에너지)'라면 ICOBI는 '얼마나 겹치냐(전자쌍 공유 정도)'. 이온결합은 ICOBI가 작다.",
 "how":"LOBSTER가 COHP와 동시에 산출(cobiGenerator). ICOBI≈1이면 단일 공유결합.",
 "ours":"comp2 P–S 0.925(공유) vs Li–Br 0.280(이온성). ELF(시각)와 ICOBI(숫자)로 결합성격을 교차 확인."},

{"id":"lobster", "doc":"cohp", "doc_sec":"§5 LOBSTER 재투영과 charge spilling","term":"LOBSTER","full":"결합 후처리 프로그램","cat":"화학 결합",
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
 "ours":"comp1 relaxed E_VRH 22.06(문헌 23 일치). comp2만 comp1과 같은 cubic-52라 완전비교쌍 — <b>2026-07-26 완료: comp2 E_VRH 20.03 &lt; comp1 22.06</b>(−9.2%, B_VRH −18.2%, G_VRH −8.1% = Br 치환이 격자를 연화). 단 Pugh B/G는 3.14→2.79로 감소라 연성은 오히려 내려간다. modelc/lpsocl은 rhombo셀이라 순위/각주만."},

# ── 이온 수송 ─────────────────────────────────────────
{"id":"bvse","term":"BVSE","full":"Bond Valence Site Energy","cat":"이온 수송",
 "what":"결합가(bond valence) 경험식으로 Li⁺가 격자 각 지점에서 느끼는 <b>이동 퍼텐셜 지도</b>를 싸게 계산. 낮은 계곡을 잇는 경로 = 이온 채널, 문턱 = <b>상대적</b> 병목 지표(에너지 유사 척도이지 eV 장벽이 아님).",
 "how":"softBV 파라미터(Li–X R₀)로 BVSE=(BVS−1)² 맵 → 등가면/퍼콜레이션 분석으로 채널 연결성. DFT-NEB보다 훨씬 빠른 스크리닝. ⚠ <b>우리 구현의 단위는 valence²(무차원)</b>이지 eV가 아니다 — 문헌 softBV(Coulomb+Morse형 척력으로 eV 깊이 우물)와 같은 양이 아니므로 eV-BVSE 문헌값과 직접 비교 금지.",
 "ours":"comp1/modelc/b2o3 BVSE cube+percolation. 정량·순위는 원본 주기셀 값만 인용(큐빅박스는 표시용)."},

{"id":"md","term":"MD (MLIP)","full":"분자동역학 · UMA","cat":"이온 수송",
 "what":"원자를 뉴턴 방정식으로 시간에 따라 움직여 <b>유한온도에서 Li가 실제로 확산하는 궤적</b>을 얻는다. 힘을 DFT로 매번 계산하면 비싸서, 학습된 퍼텐셜(MLIP, 우리는 UMA)로 대체.",
 "how":"Langevin NVT(dt 2fs, 온도 고정) 평형 5ps + 생산 200ps. 여러 온도·여러 시드로 통계. MLIP라 <b>pseudopotential 개념이 없다</b>(DFT와 다른 축).",
 "ours":"UMA-s-1p1(omat), 600/800/1000K. 절대값 인용 금지·멀티시드 판정만. <b>시드 수는 조성마다 다르다</b> — comp1/modelc deck 앵커는 온도당 <b>단일 궤적</b>(오차막대 없음), modelc의 멀티시드 값은 3-seed×3-T 0.197±0.032, b2o3 3-seed, LPSOCl 4-seed, comp2 3-seed. 조성 간 비교는 같은 시드 프로토콜끼리만. UMA는 Li₃N엔 금지(편향)."},

{"id":"msd", "doc":"md", "doc_sec":"§3 MSD와 Einstein 관계 · §4 시간창 피팅","term":"MSD → D","full":"Mean Squared Displacement","cat":"이온 수송",
 "what":"시간에 따른 이온의 <b>평균제곱변위</b> ⟨r²(t)⟩. 확산이면 시간에 선형 → 기울기가 확산계수 D (Einstein 관계 ⟨r²⟩=6Dt).",
 "how":"MD 궤적에서 Li들의 변위를 시간창(예 2–50ps)으로 피팅. 초반 ballistic·후반 통계부족 구간은 제외.",
 "ours":"MSD 창 2–50ps 고정."},
 {"id":"beta-gate", "term":"β 게이트 (확산영역 판정)", "full":"diffusive-regime gate, β = dlogMSD/dlogt",
  "cat":"이온 수송",
  "doc":"beta-gate", "doc_sec":"§7 왜 0.8 인가 · §8 c 행 판별 · §11 셀 크기가 β 를 만든다 · §12 실무 순서",
  "what":"MSD∝t^β 의 지수 β로 '진짜 확산인가'를 판정하는 게이트. <b>β=1 은 물리다</b> — MSD=6Dt 가 D 의 <i>정의</i>라 β≠1 이면 D 가 창마다 달라지고, 그게 Arrhenius 로 그대로 전파된다. <b>0.8 은 우리가 정한 값이고 문헌 근거가 없다</b> — 조사한 범위에서 <b>β 를 문턱으로 쓰는 문헌을 못 찾았다</b>. 문헌 표준은 셋이다: ① 확산 <b>이벤트 수</b>(He/Zhu/Mo 2018, npj Comput. Mater. 4, 18) ② <b>창 스캔 검증</b>(Kahle/Marcolongo/Marzari 2020, EES — t′ 5/10/20/30 vs 40 ps) ③ <b>D 수렴 floor</b>(D&lt;1e-8 cm²/s). β 게이트는 그 셋의 <b>우리 쪽 대용품</b>이다. <b>🔴 그리고 0.8 은 폐기 수순이다 (2026-08-26 귀무 스윕)</b> — <b>완벽히 Fickian 인</b> 합성 계에 우리 실측 절편만 넣고 β 분포를 재면, 절편 2 Å²·홉 13.9(=modelc·b2o3 600 K 운영점)에서 <b>귀무 β 중앙값이 정확히 0.80, P(β&lt;0.8)=50 %</b> 다. 즉 <b>우리 운영점에서 고정문턱 0.8 은 동전던지기</b>다. 절편 4 Å²·홉 8.4(=LPSOCl 600 K)에선 귀무 중앙값이 0.58 이라 <b>관측 0.615 는 오히려 그 위</b> — 탈락이 아니라 정상이었다. ⛔ <b>정정 (2026-08-27, Codex 회신 F)</b>: 초판의 <i>〈시드 산포는 홉 수(−0.78)를 따른다 — He 2018 재현〉</i> 은 <b>철회</b>했다. <code>n_hop</code> 은 사실상 평균 D 이고(ρ=<b>+0.95</b>), <code>CV=sd/mean</code> 의 <b>분모가 그 평균 D</b> 라 상관이 상당 부분 기계적이다 — 평균 D 를 그대로 넣어도 −0.73 이 나오고, 두 상관의 차는 유의하지 않다(Williams/Steiger p≈0.09, leave-one-system-out 도 불안정). ⇒ 판정은 <b>① <code>D_inc</code>(구간 증분기울기 — 상수 절편이 대수적으로 소거된다)</b> ② 실제 점프 수 ③ block/seed CI 로 가고, <b>β 는 경보 · c 행은 t=0 외삽이라 보조</b>다. <b>⛔ 단 이건 면죄부가 아니다</b> — 게이트는 <b>양방향으로</b> 틀렸다(modelc/700 K 는 β 0.76 로 탈락했지만 케이지 절편이라 D 인용 가능, b2o3/700 K 는 0.85 로 통과했지만 여섯 창 전부 β 평평·m −22.8%). 인용 위험 <b>18건 중 β 사유는 2건</b>뿐이고 그 2건도 안 풀린다 — LPSOCl 600 K 는 MTO 곡선에서 <b>c 3.05→7.02 · m −24.5%</b> 라 β 와 무관하게 아확산 서명이 남는다. 바뀐 것은 통과/탈락 목록이 아니라 <b>진단명</b>이다: 〈β 가 낮다〉(원인 불명)→<b>표본 부족</b>(홉 수). ⚠ 처방은 <b>셀 하나가 아니다</b> — <b>MTO·창 스캔은 공짜로 잡음</b>을 줄이고(시드 산포 0.52→0.06), <b>셀은 편향</b>을 건드린다(D 가 1.64–1.70배). <b>잡음은 표본으로 줄지만 편향은 안 준다.</b> ⛔ 셀이 β 를 고치는지는 <b>미확정</b> — 창 스캔은 오히려 큰 셀이 나쁘다(작은 셀 0.76→0.98 회복 vs 큰 셀 0.87 정체·c +128 %). (CSV: <code>beta_gate_null_vs_hops_c2/c4_origin.csv</code>, <code>beta_vs_seed_spread_origin.csv</code>) β&lt;0.8은 케이지(자리 안 진동+드문 홉), β≈2는 탄도. ⚠ <b>β 만으로 판정하지 않는다</b> — 자유절편 c 가 창 따라 상수면 <b>케이지 절편</b>이라 D 는 무사하고(D 는 기울기에서 나온다), c 가 커지며 m 이 떨어지면 그때가 <b>진짜 아확산</b>이다.",
  "how":"로그-로그 눈금에서 적합 창(2–50 ps)의 기울기 + 창끝 MSD ≥ 3 Å² 병행. <b>2026-08-26 부터 β&lt;0.8 은 '케이지' 라고 단정하지 않는다</b> — 그 창의 자유절편 직선 (c,m) 이 함의하는 <b>귀무 β</b> 와 비교해 <code>β≈귀무(절편+홉 N 으로 설명가능)</code> / <code>β≪귀무(창이 직선이 아님)</code> 로 갈라 찍는다. 케이지 vs 멱함수 <b>확정</b>은 여전히 <code>--scan</code> 의 다중 창 c-추세 몫이다. R²로는 못 잡는다 — R² 0.975인데 β 0.61인 실측(LPSOCl 600 K). <b>확정 판정은 MTO 시드<i>평균곡선</i>으로만</b>(→ STO/MTO 항목): 같은 런을 STO 로 읽으면 시드 산포가 <b>8.7배</b>(0.52 vs 0.06)이고 β=1.14 같은 물리적 불가값이 섞인다. 도구: <code>msd_diffusive_check.py --mto --average --scan</code>.",
  "ours":"<b>원인이 셀 크기로 판정됐다 (2026-08-26).</b> 시간을 8배(200→1600 ps) 늘리면 600 K 가 <b>오히려 나빠진다</b>(β 0.64→0.37) — 이온이 상자를 가로질러 wrap 이 쌓이기 때문. 같은 잣대(MTO 시드평균)로 lpsocl 작은 셀(5.67 Å)은 <b>0.76·0.77 두 런셋에서 재현되게 실패</b>, 3×3×1(17.0 Å)은 <b>0.81 통과</b>(시드산포 0.006). 그리고 셀 확대 비용이 <b>원자 ×9 에 벽시계 ×1.2</b>로 실측됐다 — 62원자에선 GPU 가 놀고 있었다. ⚠ β 인용은 <code>db/properties/lpsocl_beta_registry.json</code> 의 <b>entry id 로</b> — 같은 이름에 0.615~0.82 <b>여섯 값</b>이 흩어져 있었다."},

{"id":"d-inc", "term":"D<sub>inc</sub> (구간 증분 확산계수)",
  "full":"incremental diffusivity — D<sub>inc</sub>(t₁,t₂) = [MSD(t₂) − MSD(t₁)] / [6(t₂ − t₁)]",
  "cat":"이온 수송",
  "doc":"beta-gate", "doc_sec":"§7-8b 교차리뷰 판정 · §8 c 행 판별",
  "what":"<b>2026-08-27 부터 우리의 주 판정축</b>이다 (교차리뷰 권고를 받아들인 것). 핵심은 <b>차분이 상수 절편을 대수적으로 소거한다</b>는 것이다: <code>MSD = c + 6Dt</code> 이면 <code>MSD(t₂) − MSD(t₁) = 6D(t₂−t₁)</code> 로 <b>c 가 사라진다</b>. 그래서 케이지 절편이면 창을 옮겨도 D<sub>inc</sub> 가 <b>평평</b>하고, 진짜 <code>t^α</code> 면 <code>D<sub>eff</sub> ∝ t^(α−1)</code> 로 계속 움직인다. ⇒ <b>케이지 vs 멱함수를 자유절편 c 보다 곧게 가른다.</b><br>왜 c 를 강등했나 — 자유절편은 <b>관측 범위 밖 t=0 으로의 외삽</b>이고 c–m 오차가 강하게 얽혀 있어서, 늦은 창에서 <b>음수로 튄다</b>(실측: modelc/700 K −4.68 Å²). c 행은 이제 <b>보조 진단</b>이다.",
  "how":"합성 검증이 가장 명확하다 — <code>MSD = 3.0 + 0.6t</code> (즉 c=3 Å², <b>D=0.1 Å²/ps 정확</b>) 를 넣으면 창 2–50 / 10–50 / 25–100 / 50–100 에서 <b>β 는 0.72 → 0.93 으로 움직이는데 D<sub>inc</sub> 는 네 창 모두 0.100</b> 이다. <b>낮은 β 가 D 가 틀렸다는 증거가 아니라는 것</b>이 한 줄로 보인다. 도구: <code>msd_diffusive_check.py --scan</code> 의 <code>★D_inc</code> 행 (selftest 52).",
  "ours":"⛔ <b>이 지표가 못 하는 것</b> — ① <b>느린 전이 vs 진짜 멱함수는 여전히 못 가른다</b>(둘 다 D<sub>inc</sub> 가 움직인다; 가르려면 더 긴 궤적에서 plateau 도달 여부를 봐야 한다) ② <b>오차막대가 없다</b> — 끝점 두 개만 쓰므로 잡음에 그대로 노출된다. 제대로 된 CI 는 <b>시드 외층 + 시간원점 block 내층</b> 계층 bootstrap 이어야 하고(lag 점이나 이온 개별 재표집은 <b>금지</b> — 각각 시간원점을 공유하고 집단홉 공분산을 파괴한다) <b>아직 미구현</b>이다 ③ lag 이 궤적 길이에 가까우면 MSD(t₂) 자체를 못 믿는다."},

{"id":"lag-tier", "term":"창 등급 (primary / sensitivity / exploratory)",
  "full":"analysis-window tiers by max lag vs trajectory length",
  "cat":"이온 수송",
  "doc":"beta-gate", "doc_sec":"§7-8b",
  "what":"창의 최대 lag <code>t₂</code> 가 궤적 길이 <code>T</code> 에 가까워지면 <b>그 lag 의 시간원점 수가 ≈(T−t₂)/Δt 로 0 에 수렴한다</b> — 값이 아니라 잡음이다. 그래서 창을 셋으로 나눈다: <b>primary</b> t₂ ≤ 0.5T (판정은 이것으로만) · <b>sensitivity</b> 0.5–0.7T (민감도 분석) · <b>exploratory_only</b> t₂ > 0.7T (<b>화면 진단 전용 — 판정·plateau·오차막대에 쓰지 않는다</b>).",
  "how":"<code>msd_diffusive_check.py --scan</code> 이 등급을 라벨에 찍고(<code>~</code>=sensitivity, <code>!</code>=exploratory) <b>exploratory 는 추세 계산에서 뺀다</b>. 창이 tmax 를 넘으면 잘라내고 중복을 없앤 뒤 버린 개수를 찍는다.",
  "ours":"⚠ <b>결과가 아프다</b>: 100 ps 궤적에서는 primary 가 <b>2개</b>밖에 안 남고 추세 판정에 4개가 필요해서 <b>추세표가 아예 안 나온다.</b> 우리 <code>arrhenius_6pt</code> 12런이 전부 100 ps라 그 c-추세 판독은 <b>형식적으로 판정 불가</b>가 됐다. 800 ps 면 9창 중 7개가 살아 정상 작동한다 — <b>지금 800 ps 를 도는 직접적 이유다.</b><br>⛔ 이 등급이 생긴 계기는 우리 도구 버그였다 — 창 목록이 고정 리터럴이라 tmax 100 ps 에서 <code>50-150</code> 과 <code>50-200</code> 이 <b>같은 50–100 을 두 번 찍고</b> 서로 다른 라벨로 나왔다. 값이 같으니 '두 창이 일치한다' 로 읽혔다."},

{"id":"sto-mto", "term":"STO / MTO (시간원점)",
  "full":"Single / Multi Time Origin — MSD 를 <b>언제부터</b> 재는가",
  "cat":"이온 수송",
  "what":"MSD 의 정의는 ⟨|r(t₀+τ) − r(t₀)|²⟩ 인데, 여기서 <b>τ(lag)= 얼마나 오래 봤나</b>이고 "
         "<b>t₀ = 언제부터 봤나</b>다. <b>STO</b> 는 t₀=0 하나만 쓰고, <b>MTO</b> 는 가능한 t₀ 를 "
         "전부 써서 평균한다. <b>둘 다 시간 축 얘기지 공간(셀 크기)과 무관하다</b> — 이름이 헷갈려 "
         "'MTO=시간, STO=공간' 으로 오해하기 쉽다(2026-08-25 실제 질문).<br>"
         "왜 필요한가: 우리 셀은 Li 가 27개뿐이라 STO 는 어떤 lag 이든 표본이 27개다. "
         "그러면 <b>빠른 채널을 우연히 잡은 이온 몇 개가 곡선을 지배</b>한다. MTO 는 <b>같은 궤적을 "
         "재활용</b>하므로 MD 를 더 안 돌리고 표본을 늘린다.<br>"
         "⚠ <b>단 '공짜' 에는 조건이 있다 — 궤적(traj.xyz)이 남아 있어야 한다.</b> "
         "MTO 는 원점을 옮겨가며 <code>r(t₀+τ)−r(t₀)</code> 를 다시 계산하는 것이라 "
         "<b>매 프레임의 좌표</b>가 필요하다. <code>msd.json</code> 에는 이미 평균 낸 "
         "곡선만 있고, <b>평균에서 원본 좌표를 되돌릴 수는 없다</b> — 그래서 궤적이 "
         "없으면 STO 곡선만 남고 MTO 는 <b>원리적으로 불가</b>하다"
         "(재계산이 비싼 게 아니라 아예 안 된다).",
  "how":"궤적에서 t₀ 를 프레임마다 옮겨 가며 같은 τ 의 변위를 모아 평균한다. "
        "⚠ <b>공짜지만 만능이 아니다</b>: ① 원점끼리 시간을 대부분 공유해 <b>독립이 아니다</b> — "
        "원점 1900개라고 표본이 1900배가 되지 않는다(재검토 실측 n_eff ≈ 3.2). "
        "② τ 가 궤적 길이에 가까우면 남는 원점이 몇 개 없어 <b>STO 보다 시끄러워진다</b> → "
        "우리 코드는 lag 을 프레임 수의 <b>절반까지만</b> 계산한다. "
        "도구: <code>disorder_ensemble_diffusion.py: msd_multi_origin()</code> 이 생성하고, "
        "<code>msd_diffusive_check.py --mto</code> 가 읽는다. 없으면 조용히 STO 로 후퇴하지 "
        "<b>않는다</b> — 어느 곡선을 봤는지 모르면 판정을 못 쓴다.",
  "ours":"⭐ <b>2026-08-25 — 이 둘이 결론을 뒤집었다.</b> LPSOCl 600 K 에서 시간 4배(200→800 ps) vs "
         "이온 9배(27→243 Li) 를 비교했는데, 앙상블 평균 β 가 "
         "<b>MTO 로는 0.76/0.76/0.81</b>(이온판 1등) · <b>STO 로는 0.85/0.83/0.80</b>(기준판 1등)로 "
         "<b>순위가 뒤집혔다</b>. 효과 크기(≤0.09)가 추정자 간 차이(≤0.09)와 같은 규모 ⇒ "
         "<b>β 로는 이 질문에 답할 해상도가 없다</b>는 것이 결론이다.<br>"
         "⛔ 700/900 K 21런은 재판정을 못 한다. <b>원인은 'MTO 를 저장 안 했다' 가 아니라 "
         "'궤적을 안 남겼다' 다</b> — MTO 가 없는 건 결과고 원인은 그 위다. 실측: "
         "b2o3 6·modelc 6·lpsocl 9 전부 <code>traj.xyz</code> 0개(kgy·gabia 어디에도 없음). "
         "반대로 궤적이 있는 15런은 이미 MTO 가 있어 오늘 바로 비교할 수 있었다. 옛 문구: "
         "돌았고 <b>궤적(traj.xyz)도 안 남겼다</b>. 그래서 소급 계산이 원리적으로 불가해 "
         "18런을 다시 돌리는 중(2026-08-25). ⇒ MD 는 <code>--save_traj</code> 없이 돌리지 않는다."},

 {"id":"time-vs-ions", "term":"시간 축 vs 이온 축 (통계를 어디서 버나)",
  "full":"궤적을 늘릴 것인가, 셀을 키울 것인가",
  "cat":"이온 수송",
  "what":"MSD 통계가 모자랄 때 늘릴 수 있는 축이 둘이다 — <b>시간</b>(더 오래 돌린다)과 "
         "<b>이온 수</b>(셀을 키운다). 비용은 둘 다 선형인데 <b>버는 것이 다르다</b>: "
         "시간 2배는 <b>긴 lag 만</b> 추가하고 이온 수는 그대로다. 이온 2배는 "
         "<b>모든 lag 에서</b> 표본이 2배가 되고 유한크기 효과도 완화된다.",
  "how":"같은 조건에서 한 축만 움직여 대조한다. ⚠ 생산시간을 맞춰야 축이 안 섞인다 — "
        "2026-08 대조에서 <code>lpsocl_3x3x1</code>(이온 9배)의 생산시간이 기준과 같은 "
        "199.9 ps 였던 것이 이 실험을 유효하게 만들었다.",
  "ours":"comp1 실측: <b>1600 ps(8배 연장) → 600 K β 0.64 → 0.37 로 오히려 악화</b>. "
         "그래서 '시간 축은 답이 아니다' 가 먼저 섰다. LPSOCl 재현 시도(2026-08-25)는 "
         "<b>안 갈렸다</b> — MTO/STO 가 순위를 뒤집어서(위 항목). "
         "⇒ 지금 서 있는 근거는 comp1 한 계이고, LPSOCl 에서 재현했다는 주장은 철회했다. "
         "카드: <code>kb/results/md_beta_estimator_disagreement_2026_08_25.md</code>"},

 {"id":"pmf", "doc":"md", "doc_sec":"§7 PMF — 궤적에서 자유에너지 지형 뽑기",
 "term":"PMF (자유에너지 지형)", "full":"potential of mean force, ΔF = −k<sub>B</sub>T·ln(ρ/ρ<sub>max</sub>)",
 "cat":"이온 수송",
 "what":"MD 궤적의 <b>시간평균 Li 밀도</b> ρ(r)를 자유에너지로 바꾼 3D 지도. MSD가 '얼마나 멀리 갔나'라면 PMF는 '어디에 얼마나 오래 있었나'다. BVSE와 달리 <b>Li 27개 전부·공공·상관 운동·격자 진동</b>이 이미 들어 있다.",
 "how":"밀도 최대점을 0으로 두고 문턱을 올리며 최대 연결 성분을 본다. <b>전이점</b>(최대 성분 급상승) = 침투 자유에너지 ΔF<sub>perc</sub>. ⚠ <b>첫-관통</b>은 1.4% 실가닥이라 안 쓴다(25 ps에서 +35% 요동, 전이점은 ±10 meV). 도구: tools/ionic/pmf_path_profile.py — BV 판과 같은 침투 관례라 나란히 비교된다.",
 "ours":"<b>LPSCl1.6 600 K</b>(단일 시드 MLIP-MD 100 ps): ΔF<sub>perc</sub> <b>0.173 eV</b> vs BV ΔE<sub>perc</sub> 0.228 (−56 meV) · 경로 8.4 Å/4구간(BV는 20.2 Å/11구간) · 문턱에서 채널 42.9 vol%(BV 0.5%). <b>같은 부피로 자르면 BV는 이어진 그물, 실제 Li 밀도는 고립 덩어리</b>. ⚠ ΔF<sub>perc</sub>는 <b>그 온도의 자유에너지지 Ea가 아니다</b>(오프셋 −50 meV, 계통적) — 온도·시드 수 병기 필수. ⚠ comp1 0.20 eV는 β 게이트 탈락 궤적이라 <b>표집 상한</b>(open_items #9)."},

{"id":"arrhenius", "doc":"md", "doc_sec":"§5 Arrhenius — 활성화에너지","term":"Arrhenius / Ea","full":"활성화에너지 · 전도도","cat":"이온 수송",
 "what":"확산이 온도에 지수적으로 의존: D=D₀·exp(−Ea/kT). log D vs 1/T 직선의 기울기 = <b>활성화에너지 Ea</b>(낮을수록 빠른 전도). σ는 Nernst–Einstein으로 D에서 환산.",
 "how":"3온도(600/800/1000K) D를 log-1/T에 피팅. 저온(400/500K)은 통계부족으로 제외 판정. Ea 오차막대는 시드 분산.",
 "ours":"<b>단일 궤적 deck 앵커</b>: comp1 0.253 / modelc 0.224 (comp1↔modelc 비교 전용, 시드 오차막대 없음). <b>멀티시드</b>: modelc 0.197±0.032 · b2o3 0.199±0.034 (3-seed×3-T) / LPSOCl 0.287±0.024 (4-seed×3-T) / comp2 0.275±0.033 (3-seed). LPSOCl vs modelc = +90 meV(둘 다 멀티시드). comp2는 800K 시드 산포가 커서 300K 외삽 σ 비율 판정 보류(0.12–1.48×, inconclusive). ⚠ 프로토콜이 다른 값끼리 빼면 안 됨."},

# ── 계면·안정성 ───────────────────────────────────────
{"id":"phonon","term":"Phonon","full":"격자 진동 · 동역학 안정성","cat":"계면·안정성",
 "what":"결정 격자의 진동 모드(포논) 주파수. <b>허수(음수) 주파수가 있으면 구조가 불안정</b>(안장점). 구조가 진짜 최소점인지 검증.",
 "how":"작은 변위에 대한 힘상수(동역학 행렬)의 고유값 → 주파수. Γ점만으로 1차 스크리닝, 전체 안정성은 q-격자.",
 "ours":"comp2 v3 champion = <b>UMA-s-1p1 Γ점 FD 스크린</b>에서 허수 0(허용치 20 cm⁻¹) = UMA 최소점 기준 통과. q-격자·DFT phonon은 미수행. 최저 실수모드 +32.7 cm⁻¹은 <b>Li 지배(55–74%)</b>라 판정 지표로만 쓰고 정량 인용은 금지(조화 Li 주파수는 강비조화). 첫 champion이 saddle(−45.8i)이라 phonon 검증이 없었으면 큰일날 뻔."},

{"id":"neb","term":"NEB / CI-NEB","full":"Nudged Elastic Band","cat":"계면·안정성",
 "what":"두 안정 상태(예 이웃 site) 사이 <b>최소에너지경로(MEP)와 안장점(장벽 Ea)</b>을 찾는 방법. 이미지 여러 개를 스프링으로 연결해 경로를 이완, CI(climbing image)가 안장을 정밀화.",
 "how":"끝점 2개 relax → 중간 이미지 보간 → 각 이미지 힘 계산·이완 반복(iteration). 프로파일 피크가 중간(대칭)이면 진짜 안장, 단조증가면 경로/끝점 재검토.<br><b>⚠ 수렴 판정은 장벽이 아니라 힘(Fmax)으로 한다 (2026-08-27).</b> 실측(li3nd 3×3×3): 장벽이 3.00 → 0.880 → 0.128 eV 로 <b>단조 감소</b>해 수렴처럼 보이는데, 같은 구간 Fmax 는 step 19 의 0.200 을 최저로 <b>정체하다 step 30 에 0.451 로 역주행</b>했다(문턱 0.05). <b>장벽이 내려가는데 힘이 커지면 경로가 아직 움직이는 중</b>이고 그 장벽은 지나가는 값이다 — 마지막 7스텝 = GPU 50시간이 Fmax 를 두 배 나쁘게 만들었다.<br>⛔ 우리가 붙였던 <i>\"QE 문턱 0.05 는 인용에 느슨하다\"</i> 는 <b>철회</b> — VASP 의 EDIFFG 를 잘못 옮긴 것이고 <b>0.05 가 QE neb.x 기본값</b>이다.",
 "ours":"<b>★ 대칭 홉이면 full NEB 를 안 돌아도 된다</b> — <code>tools/sei/symmetric_saddle.py</code> (2026-08-16). 양 끝점이 대칭 동등하면 안장이 경로 중점에 놓이므로, 중점에 뛰는 원자를 <b>고정</b>하고 나머지를 이완하면 그게 안장이다. <b>끝점 1 + 안장 1 = 2 relax</b> (full NEB 의 ~560 SCF 대신). 근거: 2×2×2 ccpath 에서 CI 가 값을 <b>1 μeV</b> 만 바꿨다(0.228980 → 0.228981) — 안장이 이미 중점에 있었다는 뜻.<br>⛔⛔ <b>li3nd 3×3×3 에서 이 방법이 막힌 근거(<code>고정 대상 원자가 1.240 Å 움직인다</code>)를 2026-08-27 저녁에 <span style='color:#be123c'>미확정으로 내렸다</span>.</b> 그 1.240 은 두 끝점을 <b>원자 순서대로 zip</b> 해 잰 값이라, ⓐ 두 끝점을 독립 이완하며 각각 얻은 <b>강체 표류</b>(셀은 병진 불변 — 물리가 아니다) ⓑ 같은 원소끼리의 <b>라벨 교환</b> 이 안 빠져 있다. 지문이 우리 기록에 이미 둘 있었다: <b>107/107 원자가 움직였고</b>, <b>Li 는 제 자리에서 0.03 Å 만 움직였는데 홉이 3.667 → 4.203 Å 으로 벌어졌다</b>(Li 가 안 움직였는데 거리가 변했으면 변한 건 <b>기준틀</b>이다). 이 파서의 docstring 도 그 좌표를 이미 <i>표류 구조</i>라 부른다.<br>⇒ 판정은 <code>--align_check</code> (2026-08-27 신설): 최적 PBC 병진을 <b>성분별 중앙값 고정점</b>으로 빼고(중앙값이라 진짜 움직인 소수 원자에 안 끌린다) 원소별 최소변위 재대응 후, 남는 잔여를 <b>홉 중점까지 거리의 함수</b>로 낸다. <b>far-field ≤ 0.05 Å → 인공물(중점법 부활, 3주 불필요)</b> · ≥ 0.30 Å → 실제 · 사이는 무판정. selftest 8/8 (순수 병진 1.10 Å 를 <i>인공물</i>로, 진짜 1.12 Å far-field 이완은 병진과 섞여도 <i>실제</i>로).<br>⛔ 이 도구가 <b>못 하는 것</b>: 공간군 회전·반사는 안 뺀다 · 잔여가 물리인지 <b>미수렴 표류</b>인지 못 가른다.<br>🔑 <b>그리고 「싼 우회로가 없다」 는 철회한다</b>(2026-08-27, 교차리뷰 I). 막힌 건 <i>중점법</i>과 <i>saddle 이식</i> 둘뿐이고 그 둘만 「변위장이 국소」 전제를 쓴다. <b>dimer / minimum-mode following 은 전 원자를 자유롭게 두므로 그 전제를 안 쓴다</b> — 고에너지 image 와 tangent 를 출발점으로 1차 안장을 직접 찾는다(단 발견한 안장에서 불안정 모드 양쪽으로 내려가 실제 A/B 끝점에 닿는지 검증 필요).<br>📐 <b>협동 이동 자체는 장벽을 무효화하지 않는다.</b> 정적 장벽은 전 원자 3N 차원 PES 의 두 basin 을 잇는 경로이고 「한 원자만 움직여야 한다」 는 조건이 없다. Nd 집단이완이 죽이는 것은 중점법·국소 frozen-shell·saddle 이식·「단일 Li 직선 홉」이라는 <b>이름</b>이지 full NEB 의 collective MEP 가 아니다. 허용되는 명칭: <i>3×3×3·one-neutral-vacancy 조건의 collective c→c vacancy–Nd relaxation barrier</i> — <b>Li₃Nd 의 고유 ionic Ea 라고 부르면 안 된다.</b><br><br>VGCF/hBN Li 확산: hBN표면 <b>&lt;0.01 eV(사실상 무장벽)</b> — 경로 전체 폭 7 meV가 이미지당 힘오차 46 meV/Å보다 작아 수치 인용 불가(Shi2017 0.10 eV와 '일치'로 쓰는 것도 금지) · graphene 0.273(문헌 일치) · gallery <b>2L2L 0.147 eV(대표, 2L 수렴 미확인 = 상한)</b>. barrier가 층수에 민감(1L1L 0.357→2L2L 0.147, −209 meV — gallery가 느린 채널↔빠른 채널로 뒤집힘)해 층수 트렌드 자체가 결과 — 1L1L 0.357은 대표값 아님. 혼합층 2×2 행렬 완성(2026-07-30): 209 meV 의 <b>98.9%가 VGCF(그래핀) 쪽</b>이고 h-BN만 2층으로 하면 오히려 +23.5 meV 악화. 기전은 <b>confinement</b>로 확정 — 같은 그래핀 1L→2L 이 <b>자유 표면에서는 +12 meV(NEB 허용오차 ~20 meV 안 = 0)</b>, 갤러리 안에서는 −207 meV. 따라서 '이중층 탄소 기판이 유리하다'로 일반화하면 안 되고 '<b>갇힌</b> Li 에 대해 벽 두께가 유리하다'로 한정해야 한다. 3L 포화는 미측정."},

{"id":"esw","term":"ESW / onset","full":"전기화학 안정성창 (grand-potential)","cat":"계면·안정성",
 "what":"SE가 산화/환원 없이 버티는 전압 범위. grand-potential(Li 화학퍼텐셜 함수) 방법으로 분해 시작 전압(onset)과 분해 산물을 예측. VBM≠onset(반응 자유에너지가 결정).",
 "how":"조성-전압 상평형(pymatgen grand-potential phase diagram) → onset 전압·반응식. 실험 CV와 대조.",
 "ours":"argyrodite onset 2.256V(Son2025 '<2.5V'·Zuo2022 반응식과 정합). 산화 분해: Li₆PS₅Cl→Li₃PS₄+LiCl+S."},

{"id":"adhesion","term":"Adhesion / Wad","full":"계면 접착일","cat":"계면·안정성",
 "what":"두 상(예 SE|전극)을 떼는 데 드는 에너지 = 계면 접착 강도. 기계적 밀착·계면 저항과 연결.",
 "how":"슬랩 두 개를 붙인 계면 에너지 − 각각의 표면 에너지. 기하 승계·저β 믹싱으로 수렴.",
 "ours":"adhesion.json. MLIP-elastic 상관은 2026-07-23 deprecated(재계산 필요)."},

# ── MLIP·자동화 ───────────────────────────────────────
{"id":"mlip", "doc":"md", "doc_sec":"§2 MLIP가 DFT 힘을 대체","term":"MLIP / UMA","full":"Machine-Learned Interatomic Potential","cat":"MLIP·자동화",
 "what":"DFT 데이터로 학습해 <b>원자간 힘을 DFT 정확도로 즉시</b> 내주는 신경망 퍼텐셜. MD·대규모·다샘플에 필수(DFT는 너무 비쌈). UMA는 foundation model(범용 학습).",
 "how":"구조→에너지/힘을 학습. pseudopotential·k-point 개념 없음. 검증(우리 조성에 편향 없나)이 중요.",
 "ours":"UMA-s-1p1로 MD·phonon·MLIP-EOS. LPSCl 계열엔 검증된 표준, Li₃N엔 금지."},

# ── 방법론·모델링 ─────────────────────────────────────
{"id":"abs_floor","term":"절대 바닥 (백분율의)","full":"absolute floor on a ratio","cat":"방법론·모델링",
 "what":"백분율은 <b>차이 ÷ 크기</b>다. 분모가 작으면 <b>크기 정보가 버려진다</b> — 그래서 판정마다 \"이 질문이 성립하는 최소 크기\"를 같이 걸어야 한다. 없으면 두 방향으로 틀린다: ① 분모가 작아 <b>없는 차이가 커 보인다</b> ② 분자와 분모가 같아져 <b>비율이 엉뚱한 이유로 1 에 붙는다</b>.",
 "how":"판정 규칙을 <code>pct ≥ P</code> 하나로 두지 말고 <code>abs ≥ A <b>그리고</b> pct ≥ P</code> 로 둔다. A 는 물리에서 온다 — 결합길이의 몇 %, 열진동 진폭, SCF 잡음처럼 <b>그 양이 무엇인지</b>가 정한다. 그리고 A 밑에서는 '작다' 가 아니라 <b>'판정하지 않는다'</b> 로 찍는다(작다고 말하면 그것도 주장이다).",
 "ours":"<b>2026-08-28 하루에 세 번 밟았다.</b><br>① <b>끝점 스칼라 일치도</b> — 0.0641 vs 0.0723 Å 을 <b>\"12 % 어긋남 ⇒ 대칭 등가 아님\"</b> 으로 찍었다. 절대차는 <b>0.008 Å</b>(원자 반지름의 1/100)로 잡음이다. → 바닥 0.02 Å·0.01 eV.<br>② <b>골격 COM(흐름 vs 재배열)</b> — <code>kept = COM제거후/원래</code> 인데 골격이 진동만 하면(MSD 0.3–1.1 Å²) 뺄 드리프트가 없어 <b>kept ≈ 1.0</b> 이고, 그게 \"재배열 — 구제 불가\" 로 찍혔다. <b>modelc 9개 중 8개</b>가 그렇게 오판됐다 — 같은 실행의 골격 β 검사는 <b>9/9 rigid</b> 였는데도. → 바닥 2 Å²(RMS 1.4) 밑이면 <b>판정 안 함</b>.<br>③ <b>모드 스캔 잡음문턱</b> — 10 meV 를 <b>미리 선언</b>했다가 교차리뷰 J 가 \"재서 정하라\" 고 반려. 안 재고 고른 바닥도 임의다.<br>🔍 ②는 <b>두 검사가 정반대를 말해서</b> 잡혔다. 한 보고서 안에서 두 지표가 반대를 가리키면 <b>데이터가 아니라 도구를 먼저 본다</b> — 오늘 네 번 그랬다(min-image 17.39 Å in 10.37 Å 셀 · 반전 중심 · van Hove 판정 · 이것)."},

{"id":"framework_gate","term":"골격 게이트","full":"framework (non-Li) rigidity gate","cat":"MLIP·자동화",
 "what":"MLIP-MD 에서 <b>Li 만 움직여야</b> 그 MSD 가 확산이다. 골격(비-Li)이 같이 움직이면 'D' 는 확산이 아니라 <b>구조 붕괴</b>다. Zhang npj 2026 이 MACE-MP-0 의 LGPS 골격이 1050–1500 K 에서 인위적으로 녹는 걸 잡았고, 우리 아레니우스 상한 1000 K 가 그 바로 아래다.",
 "how":"비-Li 원소별 MSD 의 β 를 재서 <b>β ≥ 0.30 이면 오염</b>. ⚠ 원소 8개 미만은 판정에서 뺀다 — 2~3개 평균은 한 원자가 한 번 뛰면 β 가 1 을 넘는다. 별도로 <b>골격 질량중심을 빼고</b> 다시 재면 '통째로 흐르는가(구제 가능)' vs '자리 재배열(구제 불가)' 가 갈리는데, <b>골격이 실제로 움직일 때만</b> 성립하는 질문이다(→ 절대 바닥 항목).",
 "ours":"<b>b2o3 ⛔</b> — 사전 등록(2026-08-25, 결과 보기 전 확정) 판정: 800 K 0.51/0.79/0.54 · 1000 K 0.50/0.78/0.47 · 1200 K 0.88–1.15 로 <b>3/3 전부 문턱 초과</b>. 장부가 UMA-MD 수송축 인용을 금지했다. 다만 <b>600 K 는 2/3 rigid</b> 라 800 K 이상만 확실히 무효다.<br><b>modelc ✅</b> — 600/800/1000 K × 시드 3개 <b>9/9 framework_rigid</b>(β −0.05 ~ 0.27, 2026-08-28 실측). 그 온도의 Li D 는 진짜 확산이다.<br>⛔ 이 게이트를 <b>안 걸고 낸 결론은 무효</b>다 — 2026-08-28 van Hove 발견 셋 중 둘이 b2o3 위에 있어 철회됐다. 새 조성·새 온도는 <b>인용 전에</b> 건다.",
 "doc":"md"},

{"id":"ordered_vs_disordered","term":"Ordered vs Disordered","full":"질서/무질서 구조 선택 — 어떤 LPSCl 셀로 계산하나","cat":"방법론·모델링",
 "what":"'질서셀 vs 무질서셀 누가 맞냐'는 잘못된 질문 — 진짜 질문은 <b>어떤 양을 계산하느냐</b>. 0 K DFT는 에너지 E를, 합성온도의 실험 무질서 구조는 F = E − TS_config를 산다. 무질서는 실패한 결정화가 아니라 <b>합성 T의 진짜 자유에너지 최소(부분 무질서 x*(T), 예: Kraft Cl 4d 62%)</b>를 급랭으로 실온에 동결한 것. Rietveld 점유율(예 48h occ 0.5)은 시공간 평균 확률이지 스냅샷이 아니다.",
 "how":"<b>0 K 미분·에너지(phonon·gap·formation/hull·elastic) → relaxed ordered 셀 / 유한온도 수송(σ·Ea) → 무질서 유지 + 다중 배열 앙상블 평균</b>. 무질서(48h 빈자리·anti-site)는 전도의 필요조건이 아니라 핵심 증강 레버 — 질서화하면 Ea 계통 과대(+0.03 eV, σ 1/4; comp1 vs modelc). 경고 사례: Deng SQS A=0.92 vs Torii ordered A=1.09 — 둘 다 A≈1(거의 등방)이지만 무질서 처리·D3 등 방법차만으로 A−1 부호가 흔들리는 미세 지표.",
 "ours":"canonical gap: comp1만 52at ordered 정형셀, modelc(62at)·+B₂O₃(128at)·LPSOCl(62at)은 배치 확정 단일-config 셀에서 동일 fixed-occ 레시피(electronic.json doping_family_2026_07_16). 수송은 d=0.5/1.0 × cfg0/1/2 disorder ensemble(UMA anneal+relax; v1 un-relaxed swap은 artifact 폐기). 단일 config 판정 금지(단일시드 1.33× 철회 교훈). 우리 A=1.14 ≈ Torii 1.09는 공유 편향(둘 다 ordered) 가능성 자기비판 유지 — 게다가 <b>A는 성분 선택에 민감</b>하다(comp1 relaxed 3추정치 1.14/0.75/0.92, 평균-Cij 기준 0.93; 저장값은 1번 삼중항 규약). 산포가 Deng 0.92↔Torii 1.09 간극(0.17)보다 크므로 Torii와의 근접을 정합 논거로 쓰지 않는다."},
]

def by_category():
    out = {c: [] for c in CATS_G}
    for g in GLOSSARY:
        out.setdefault(g["cat"], []).append(g)
    return out
