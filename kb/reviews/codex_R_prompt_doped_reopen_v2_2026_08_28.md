---
title: "Codex 회신 R 요청 프롬프트 — doped 재개 설계 v2 의 계산 전 심사"
date: 2026-08-28
updated: 2026-08-28
tags: [review, codex, sdcp, reopen, estimand, prompt]
status: 발송 대기
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 회신 R 요청 — 재개 설계 v2 를 **계산 전에** 심사받는다

회신 O 가 v1 카드를 P0 전면 반려하며 준 처방을 v2 로 구현했다. 규율 그대로 —
**계산을 하나도 던지기 전에** 설계를 심사받는다. 통과해야 Stage 0 (기체상) 시작.

---

## 붙여넣을 프롬프트

```
당신은 계산재료 리뷰어다. 앞선 회신 O 에서 우리의 doped estimand 카드 v1 을 P0 전면
반려하며 재승인 조건 7 을 줬다. 1저자가 재개를 결정해 v2 설계를 만들었다.
**아직 아무 계산도 던지지 않았다** — 이 설계가 조건을 실제로 채우는지, 던지기 전에
심사해 달라.

계: 자가도핑 전도성 고분자(SDCP, PEDOT-S 계열) 바인더의 LiNiO2(104) 흡착.
목표 질문: "붙을 때 백본 캐리어를 유지하는가" (단일 E_ads 스칼라 아님).

── v2 설계 요약 ──

[A. 화학종 (조건 ①)]
구성 규칙: DPn/+m = n-량체(반복단위 C11H16O6S2, 연결부마다 -H2)에서 술폰산기 m 개를
H-원자 제거로 탈양성자화한 알짜중성 종. 백본 홀 m 개, counterion 없음(자기보상), Q=0.
정확한 원자수·NELECT 는 빌더가 계산해 manifest 에 고정 (손으로 안 적는다).

  S1  DP3/+1 (33%)  doublet M=1
  S2  DP4/+1 (25%)  doublet M=1        <- S1과 조성 bracket (실측 25-35% 양끝)
  S3a DP6/+2 (33%)  closed-shell singlet bipolaron M=0
  S3b DP6/+2 (33%)  triplet 2-polaron M=2
  S3c DP6/+2 (33%)  broken-symmetry open-shell singlet M=0 (국소 반대부호)
  N1-N3 DP3/0·DP4/0·DP6/0 중성 대조

교차 크기 비교는 직접 총에너지 금지, 동일 N 의 U_eff = E(+2)+E(0)-2E(+1) 만 보조.
종 간 열역학 비교가 필요할 때만 H-원자 reservoir 를 (1/2)E(H2) 로 선언.

[B. estimand (조건 ②③)]
주: E_ads^ad = E_C(s*) - E_S(B0) - E_M(m0), s* 는 사전 선언된 multistart 탐색의 최저
   복합체 상태 ("전역 최소" 라 부르지 않음).
주 관측량: 연속 carrier_retention — 분자 조각 스핀·전하 적분, Löwdin + Hirshfeld/Bader
   병기(방법 태그 필수), 단일 분할법 스칼라로 판정하지 않음.
보조: dE_loc^vert 는 두 국소화 상태가 bias 제거 후 반복 재현될 때만. 한쪽이 서지 않으면
   dE_loc = NA_STATE_NOT_IDENTIFIED 로 종료 (코드가 정의역 공백을 선언).
conditioning(제어)과 realized(관측) 분리: 회신 O 의 스키마 그대로 채택.

[C. 게이트 v2 (조건 ④)]
G1' state-selection policy 동일 (전부 자유 바닥상태 or 선언된 대응 제약) + 수치 설정도
    기준·대상 동일 (LREAL all-F 포함)
G2' 계별 기대 스핀 표(위 A) + 경쟁 다중도 스캔 + SCF stability
G3' 분할법 강건성 — Löwdin·Hirshfeld/IAO 가 같은 우세 방향일 때만 분류, 스칼라 문턱 없음
G4' per-Ni signed moment vector + flip indices 로 basin 식별. carrier 이동이 만든 국소
    Ni 변화는 답일 수 있으므로 basin 오류와 분리 판정
G5' 판정바닥 분리 (자리대비 30 meV / carrier-gap / 사슬수렴 — 각각 따로 선언.
    ⚠ 30 meV 자체가 UMA 유래라 DFT 전용 바닥은 미해결로 등재돼 있음)
G+  원자·전자 보존 반응식 · 동일 Hamiltonian · SCF/힘 수렴 · conformer >=2 ·
    vertical/adiabatic 구분 · state-existence 재현성

[D. Stage 0 — 기체상, 이 심사 통과 후에만]
방법: ORCA r2SCAN-3c (기존 n-시리즈와 동일 프로토콜) + 핵심 상태 range-separated
hybrid(wB97X-D 급) 교차검사.
  Z1 S1: SO3-seed/backbone-seed fresh-start multistart x conformer 2
  Z2 S2: 동일 multistart (S1<->S2 bracket)
  Z3 S3a/b/c: 같은 기하 vertical 먼저 -> 각자 adiabatic 분리 보고, polaron 간격 2종
  Z4 N1-N3 짝 대조
  Z5 분할법 교차 전 잡
슬랩 단계(그 다음): doped 와 대조군을 같은 down_dir·roll·gap 으로 짝짓고 cross 자세를
doped 에도 추가 (v1 캠페인의 자세 불일치 결함 교정).

[E. 병행 트랙 (조건 ⑥⑦)]
⑥ 기준 분자 3종 free-spin(NUPDOWN=-1)·LREAL=F 재실행 (외주, ~75분) — 회신 P 설계 그대로
⑦ machine manifest: estimand_id·화학종 규칙·Q/NELECT·state-selection policy·중단 코드를
   빌더 출력 -> 회수 분석기 게이트로 연결

[실험 요청] EPR spin count(polaron/bipolaron 분율) · 독립 carrier/산화도 측정 ·
고형 counterion 조성. 실험이 불가하면 두 스핀 섹터를 조건부 병기가 최종 형태.

── 심사 요청 (우선순위대로) ──

1. **조건 ①이 채워졌나.** "빌더가 NELECT 를 계산해 manifest 에 고정" 이 '확정' 의
   요구를 충족하나, 아니면 카드에 정확한 분자식·전자수를 지금 명시해야 하나?
   "counterion 없음(자기보상)" 선언이 고형 실물(H+/Na+ 잔존)과 어긋날 때 이 설계의
   어떤 결론이 살아남나?

2. **S1/S2 bracket 설계가 맞나.** DP3/+1 과 DP4/+1 은 도핑률만 다른 게 아니라 사슬
   길이도 다르다 — 두 효과가 얽히는데 bracket 이라 부를 수 있나? 분리하려면 무엇이
   더 필요한가 (예: DP6/+2 가 33% 를 다른 길이에서 재현하는 것으로 충분한가)?

3. **S3 스핀 섹터 셋의 비교 규약.** vertical(같은 기하) 비교의 그 '같은 기하' 를
   어느 상태에서 이완한 기하로 잡아야 하나? A7b(BS)의 스핀 오염 보고만으로 충분한가,
   아니면 근사 스핀 정화(Yamaguchi 급)까지 요구해야 하나?

4. **carrier_retention 의 정의.** "분자 조각 스핀·전하 적분(Löwdin+Hirshfeld 병기)" 이
   기체상 Stage 0 에는 잘 정의되지만, 슬랩 단계에서 분자-표면 경계를 어떻게 긋는지가
   미정이다. Stage 0 심사 시점에 이것까지 고정해야 하나, 슬랩 설계 때로 미뤄도 되나?

5. **Z1-Z5 목록의 과부족.** 안 돌려도 되는 것과 빠진 것. 특히 conformer 2개·polaron
   간격 2종이 최소로 충분한가? hybrid 교차검사를 전 잡이 아니라 '핵심 상태' 로 좁힌
   것이 어디까지 정당한가?

6. **G5' 의 미해결을 안고 가도 되나.** 자리대비 판정바닥 30 meV 가 UMA 유래인 채로
   DFT 에 쓰이고 있음을 우리 스스로 미해결로 등재했다. Stage 0(기체상)에는 그 바닥이
   안 걸리지만, 슬랩 단계 전에 DFT 전용 바닥을 유도하는 것을 재개 조건에 추가해야 하나?

7. **이 v2 가 여전히 놓치고 있는 것** — 회신 O 8번의 물음 그대로: 평균 재료의 ensemble
   을 단일 microstate 로 치환하는 오류가 v2 에도 남아 있는 자리가 있나? (예: conformer
   2개가 ensemble 을 대표한다는 암묵 가정, "counterion 없음" 이상화)

형식: 각 항목 P0/P1/P2 + 근거. 동의는 "동의" 한 줄. 전체 판정으로 Stage 0
GO / 조건부 GO / NO-GO 를 명시해 달라.
```

---

## 왜 이 프롬프트인가

- **던지기 전 심사**가 규율이다 — v1 의 교훈. GO/NO-GO 를 명시적으로 요구해서
  "조건부 승인을 통과로 오독" 하는 우리 패턴(회신 M 때)을 차단한다.
- 1·7번이 본체다: 조건 ① 충족 여부와, v2 에 **남아 있는** ensemble→microstate 오류.
- 6번은 우리가 등재해 둔 미해결(30 meV 출처)을 스스로 심사대에 올린 것.
