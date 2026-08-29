---
title: "Codex 회신 T 요청 — SDCP 흡착에너지를 원고에 넣는 최단 경로 (neutral 해제 + doped 상태선언)"
date: 2026-08-29
updated: 2026-08-29
tags: [review, codex, sdcp, adsorption, estimand, vasp, spin, prompt]
status: 발송 대기
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 회신 T 요청 — 흡착에너지 두 개를 살리는 최단 경로

> 배경 파일: `db/properties/sdcp_neutral_closed_2026_08_28.json` ·
> `db/properties/sdcp_doped_closed_2026_08_28.json` ·
> `db/properties/sdcp_wave1_job_energies_2026_08_28.csv` ·
> `kb/methodology/estimand_before_running_2026_08_28.md` ·
> `kb/reviews/codex_O_sdcp_doped_estimand_reply_2026_08_28.md`

---

## 붙여넣을 프롬프트

```
당신은 계산재료 리뷰어다. 우리는 고분자 바인더(SDCP)가 LiNiO₂(104) 표면에 붙는
흡착에너지를 원고에 넣으려 한다. **두 값이 필요하고 둘 다 막혀 있다.**
막힌 이유가 서로 다르고, 우리가 제안하는 해제 경로도 다르다.
각각에 GO / 조건부 GO / NO-GO 를 주고, P0(착수 차단) / P1(착수 후 보완)로 나눠라.

━━━ 배경: 우리가 여기까지 온 경로 ━━━
sdcp_doped 흡착에너지를 **여덟 번** 계산했고 여덟 번 반려됐다. 표면상 사유는 매번 달랐다
(주기이미지 겹침 / MLIP 3.4× 과대 / 자세 산포 0.146 eV / 추출 끝점을 결합에너지로 오인 /
ISMEAR·쌍극자 미설정 / 두 시드 105 meV 불일치 / 그 105 meV 의 원인 오진).
여덟 번 다 "제대로 돌렸나"는 통과했고 "맞는 양을 재고 있나"는 여덟 번째에야 물었다.
**중성형은 여덟 번 다 살아남았고 doped 만 죽었다** (닫힌 껍질 vs 열린 껍질).

━━━ 계 ━━━
· 기판: LiNiO₂(104) 슬랩 192원자, AFM(Ni³⁺ 반강자성), **금속성**, 산화환원 활성
· 흡착종 A: `sdcp_neutral` C₁₁H₁₆O₆S₂ — **닫힌 껍질**
· 흡착종 B: `sdcp_doped`  C₁₁H₁₅O₆S₂ — SO₃H 탈양성자 + HOMO 전자 1개 제거,
  알짜중성 **doublet**, NELECT 107(홀수). 홀은 백본 π 폴라론(n=1 에서 SO₃ 35 % / 백본 65 %)
· 대조군: PTFE C₁₀F₂₂ (32원자) 와 PTFE dimer (14원자)
· 계산: VASP PBE+D3(zero) +U(Ni), ENCUT 520, ISMEAR 0/SIGMA 0.05,
  ISPIN 2, LDIPOL, box24 정본. 기하는 MLIP(UMA) 로 고르고 DFT 단일점.
· 상자 수렴 실측: SDCP 0.322 meV · PTFE 0.057–0.066 meV (게이트 10 meV) — 통과

═══ 문제 1: neutral 은 "저울이 다르다" 로 막혀 있다 ═══

실측값 (pm1 branch, box24, eV):
  sdcp_neutral  Li-top −0.7675 · Ni-top −0.7582 · cross(Li@Ni) −0.7728 · cross(Ni@Li) −0.7633
                자세 4종 산포 14.6 meV
  ptfe_c10      Li-top −0.4124 · Ni-top −0.3626
  ptfe_dimer    Li-top −0.3663 · Ni-top −0.3302
  헤드라인 후보: 가장 약한 SDCP(−0.7582) − 가장 강한 c10(−0.4124) = **0.3459 eV**
                (net4 basin 맞춤에서도 0.3468 — 시드에 둔감)

**막힌 이유**: `E_ads = E_complex − E_slab − E_mol` 에서
  · 기준 분자는 **NUPDOWN 고정(중성=0)** + LREAL 설정 불일치로 돌았고
  · 복합체·슬랩은 **NUPDOWN=−1 자유**로 돌았다.
즉 **제약된 기준에서 자유로운 복합체를 뺐다.**

**우리 제안 (해제 1단계)**: 기체 기준계 3종(sdcp_neutral, ptfe_c10, ptfe_dimer)을
**NUPDOWN=−1 + LREAL=.FALSE.** 로 재실행해 δ_m·δ_LREAL 을 잰다. 기하는 고정.
INCAR 변경은 **NUPDOWN 한 줄뿐**이다 (static 상의 LREAL 은 원래 .FALSE. 였다).
2단계(0.346 을 실제로 살릴 때): 관련 complex 를 LREAL=.FALSE. 로 재실행.
슬랩은 cross-fragment 차에서 소거되므로 불필요하다고 판단했다.

Q1-1. 이 1→2단계 순서가 맞는가? 슬랩이 정말 소거되는가 —
      complex 와 slab 의 LREAL 이 다르면 그 차가 소거되지 않는 경로가 있나?
Q1-2. 기준 분자만 자유 스핀으로 바꾸면 **닫힌 껍질이라 어차피 0 으로 수렴**할 텐데,
      그렇다면 δ_m ≈ 0 이고 이 재실행은 형식적 절차인가, 아니면 실제로 값이 바뀔 수
      있는 경로가 있는가? (우리는 형식적일 가능성이 높다고 본다 — 그렇다면 그 사실
      자체를 근거로 기존 값을 복권해도 되나?)
Q1-3. **자세 표본이 비대칭**이다: SDCP 4자세 vs PTFE 각 2자세. SDCP 는 cross 자세를
      더 봐서 최저가 −0.7675 → −0.7728 로 5.2 meV 내려갔다. PTFE 가 3배를 얻어도
      346 → ~330 meV 라 결론은 안 바뀐다고 봤다. 이 논증이 성립하나, 아니면 PTFE 에도
      같은 수의 자세를 줘야 하나?
Q1-4. **정규화가 순위를 뒤집는다**: 분자당 SDCP(−0.7728) > c10(−0.4124) > dimer(−0.3663)
      인데 원자당은 dimer(−26.2 meV) > SDCP(−22.1) > c10(−12.9) 다. CF₂ 단위당으로도
      dimer(−91.6) > c10(−41.2). 우리는 헤드라인을 "원자수가 맞춰진 c10(32) vs
      SDCP(35) 의 분자당 비교" 로 한정하고 **dimer 를 근거에서 뺀다**고 결정했다.
      이게 충분한가? 어떤 정규화가 이 질문(바인더 접착)에 옳은가?
Q1-5. dense-k 가 sdcp_neutral 에는 하나도 안 갔고 c10 과 (인용불가인) sdcp_doped 에
      갔다. c10 실측 k 민감도는 E_ads 0.22 meV 였다. transfer 로 충분한가?

═══ 문제 2: doped 는 "양이 정의되지 않는다" 로 닫혀 있다 ═══

회신 M/N/O 3연속으로 **단일 스칼라 E_ads 가 이 계에서 정의되지 않음**이 확정됐다:
  분자 스핀상태 × 슬랩 AFM basin × 홀 위치(분자/슬랩) 가 전부 정당한 서로 다른 SCF 해.

실측 (wave1, static, 총자화 μB):
  mol_doped box24                 E −200.3454   mag **1.000** (doublet 선언됨)
  complex Li-top pm1              E −1146.2963  mag **−0.306**
  complex Li-top net4             E −1146.1123  mag **+3.724**
  complex Ni-top net4             E −1146.1313  mag **+3.631**
  clean_slab net4                 E  −944.8464  mag +5.999
⇒ 슬랩 AFM(0) + 분자 doublet(1) = 1 이어야 하는데 **−0.31 도 3.72 도 1 이 아니다.**
   복합체가 자유 스핀이라 어느 상태로 굴러떨어졌는지 선언되지 않았다.

**우리 제안**: estimand 카드가 주는 세 선택지
  ① 상태를 선언해 X(상태) 로 정의 ② 집계 규칙을 미리 적는다 ③ 질문을 바꾼다
중 **①** 을 택한다. 구체적으로:
  · 선언: 홀은 분자에(백본 π 폴라론) · 슬랩 AFM basin 하나로 고정 · **복합체 NUPDOWN=1**
  · 세 계(mol·slab·complex) 전부 같은 policy 로 제약
  · 주 estimand: `E_ads(hole-on-molecule, AFM basin X, doublet)` — **조건부 값으로 명시**
  · 동반 보고: `carrier_retention` = complex OUTCAR 의 원자별 모멘트를 분자 영역에서
    적분한 **연속값**. 이분법 주장("홀이 슬랩으로 갔다") 금지
  · 필요한 계산: 복합체를 선언한 상태로 재실행 — 자세 2개면 226원자 2잡

Q2-1. **NUPDOWN=1 로 복합체를 제약하는 것이 정당한 상태 선언인가?**
      우리 걱정: 회신 O 가 *"전 계에 같은 NUPDOWN 값이 아니라 같은 state-selection
      policy"* 라고 했는데, 우리 제안은 결국 "전 계에 같은 값"에 가까워 보인다.
      다만 슬랩은 AFM 상쇄로 0, 분자는 1, 복합체는 0+1=1 이라 **가산적으로 일관**한다고
      본다. 이 논증이 성립하나?
Q2-2. NUPDOWN 제약이 **홀 위치를 강제하지 못한다**는 반론이 가능하다 —
      총자화 1 을 유지하면서도 홀이 슬랩 Ni 로 옮겨간 해가 존재할 수 있다.
      그렇다면 "hole-on-molecule" 선언을 총자화로 강제할 수 없고, 별도 제약이나
      사후 검증(carrier_retention 문턱)이 필요하다. 우리는 **문턱을 사전에 정하고
      미달이면 그 자세를 NO_STATE 로 버리는 것**을 생각한다. 문턱을 어떻게 정해야
      사후선택이 안 되나?
Q2-3. **원자 투영 모멘트로 carrier_retention 을 정의해도 되나?** 우리는 OUTCAR 의
      per-ion magnetization 을 분자 원자에 대해 합산할 계획이다. 이것이 정성적 분할임을
      알고 있다. Bader / spin-density difference 가 필수인가, 아니면 연속값 + 분할방법
      병기로 충분한가? 두 분할이 갈리면 어떻게 하나?
Q2-4. 닫힘 문서의 **조건2** 는 *"n=1 에 홀 하나 = 고리당 100 % 산화인데 목표는 25–35 %
      평균 도핑"* 이라 **모델이 물질을 대표하지 못한다**는 것이다. 상태를 선언해서
      E_ads 가 정의되더라도 **이 문제는 남는다.** 그렇다면
      (a) 조건부 값으로 원고에 넣되 대표성 한계를 명시 (b) n=4~6 올리고머로 간다
      (c) 질문을 바꾼다 — 셋 중 어느 쪽인가? (b) 의 최소 규모는?
Q2-5. 닫힘 문서는 **"부분 재개 없음 — 일곱 조건 중 일부만 채우고 숫자를 만들지 않는다"**
      로 못박혀 있다. 우리 점검으로는 회신 O 7조건 중 ⑤(기체상 선행검사)는 R4 가
      8잡 조건부 GO 를 이미 냈고, ⑥(neutral spin-equivalence)은 위 문제 1 의 재실행과
      같은 작업이며, ①②③⑦ 은 설계·문서, ④ 는 코드다. **즉 새 계산은 ⑤⑥ 뿐이다.**
      이 판단이 맞나? 틀렸다면 어느 조건이 우리가 생각하는 것보다 무거운가?

═══ 공통 ═══
Q3-1. 두 값을 같은 그림/표에 올릴 때, neutral 은 자유 스핀·doped 는 제약 상태라
      **선언 정책이 다르다.** 이걸 한 그림에 올려도 되나? (오늘 우리가 문헌에서 잡은
      실패가 정확히 이것이다 — ICEP 논문 Fig 2g 가 흡착 3개와 H-이동 반응 1개를
      한 축에 올렸다.) 올린다면 무엇을 병기해야 하나?
Q3-2. 우리가 **안 물어본 것 중** 이 데이터로 판정 가능한 게 있으면 그것도.

━━━ 답변 형식 ━━━
· 문제1 / 문제2 각각: GO / 조건부 GO / NO-GO + P0 목록(착수를 막는 것만)
· Q1-1~5, Q2-1~5, Q3-1~2 각각: 답 + **그 답이 틀렸을 때 우리가 관측할 증거 하나**
· 마지막에: "원고에 오늘 쓸 수 있는 문장"을 그대로 써 달라 (neutral 용 / doped 용)
```

---

## 이 요청의 배경 (프롬프트 밖)

- 1저자·교신 요구는 단순하다 — **흡착에너지 두 개를 원고에 넣는 것**.
- 그래서 이 요청은 "더 검사해 달라"가 아니라 **"어디까지가 최단 경로인가"** 다.
- 문제 1 은 값이 흔들려서가 아니라 **저울이 안 맞아서** 막혔다 — 성격이 문제 2 와 다르다.
- 문제 2 는 우리가 처음으로 ①(상태 선언)을 시도하는 것이다. 여덟 번은 전부
  "자유롭게 돌리고 나온 값을 해석" 이었다.
- Q2-2 가 이 요청의 핵심 위험이다 — NUPDOWN 이 총자화만 묶고 **홀 위치는 안 묶는다**.
