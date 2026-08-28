---
title: "Codex 회신 P 요청 프롬프트 — wave1 INCAR 전수 감사 + doped 마감 심사"
date: 2026-08-28
updated: 2026-08-28
tags: [review, codex, sdcp, incar, closure, prompt]
status: 발송 대기
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 회신 P 요청 — 실측 감사 결과와 마감 판단을 같이 심사

회신 O 직후 두 가지가 생겼다: ① 1저자가 doped 를 **범위 마감**으로 닫고 ratify 했다
② INCAR 되울림 전수 감사에서 **새 비대칭(LREAL)** 이 나왔다. 둘 다 심사가 필요하다.

---

## 붙여넣을 프롬프트

```
당신은 계산재료 리뷰어다. 앞선 회신 O(P0 전면 반려·슬랩 NO-GO)를 우리가 어떻게
처리했는지, 그리고 그 뒤 실측에서 나온 새 발견을 심사해 달라.

배경 1 — 회신 O 처리:
- 우리는 회신 O 의 재승인 조건 7 을 밟는 대신, doped 흡착을 **범위 마감**했다.
  "이 프로토콜(n=1 단량체·wave1 설정)에서는 흡착 수치를 만들지 않는다" 를 확정하고
  거버넌스에 active 로 등록했다. 재개는 예정돼 있고, 재개 조건을
  planned_upgrade_triggers(회신 O 7조건 + 자세 설계 수정)와
  mandatory_invalidation_triggers(이 마감 자체를 반증하는 것들)로 분리했다.
- 살아남긴 것: 추출 부호 +0.34 eV(부호만) · 기체상 ORCA 열역학(DPE/LCA/EA).
- 금지한 것: doped E_ads 수치 일체 · doped vs neutral 비교 · 홀 위치 서술 · 자리선호.
- neutral 마감은 회신 O 6번을 받아 closed_for_scope_pending_spin_equivalence 로 내렸다.

배경 2 — 그 뒤 나온 실측 (INCAR 되울림 36잡 전수):
회수 드롭에 입력 INCAR 이 없어서 OUTCAR 되울림으로 전수 감사했다.

  통과:
   - 전자수 보존이 네 조각 전부 정확: clean_slab 1488 + mol(108/107/194/74)
     = complex(1596/1595/1682/1562). doped 가 홀수(1595)로 doublet 과 정합.
   - ENCUT 520 · PREC accurate · ISMEAR 0/SIGMA 0.05 · EDIFF 1e-6 · LASPH T 가 36잡 동일.
   - LDAU 는 Ni 에만 U=6.2, 나머지 LDAUL=-1. ICHARG 2/1 은 설계된 상 사슬.
     IDIPOL 3(슬랩·복합체)/4(분자상자)는 계 모양에 맞는 정상 선택.

  ★ 새 발견 — 기준과 대상의 비대칭이 **스핀 말고 하나 더** 있다:
   - LREAL: 복합체(224원자) T · 기준 슬랩(192원자) T · **기준 분자(32~35원자) F**
   - 즉 같은 분자가 복합체 안에서는 실공간 투영으로, 기준으로는 역공간으로 계산됐다.
     슬랩 쪽 오차는 complex-slab 사이에서 상쇄되지만 이 몫은 상쇄되지 않는다.
   - 우리 판단: 절대 E_ads 에는 남고, 자리대비(ΔE_site)와 추출 부호에는 소거된다.
     0.346 eV 헤드라인에는 부분적으로 남는다(SDCP 35원자 vs PTFE 32원자의 잔차 차이).
   - 크기는 **미측정**이다. 우리는 이것을 delta_LREAL 로 부르고, 기준 분자를
     LREAL=T 로 재실행해 측정하자고 제안한다.

  원리적 한계: MAGMOM 과 ADDGRID 는 VASP 가 되울리지 않는다. 입력 INCAR 이 없는
  이 드롭에서는 **확인할 방법이 아예 없다**. 자기 초기값이 미검증이라는 뜻이다.

제안: 기준 분자 3종(sdcp_neutral·ptfe_c10·ptfe_dimer, box24)을 같은 기하에서
  NUPDOWN=-1 + LREAL=T 로 재실행해 delta_m 과 delta_LREAL 을 한 번에 잡는다 (잡 3개).

심사해 달라:

1. **범위 마감이 정당한가.** 회신 O 의 7조건을 밟지 않고 "이 프로토콜에서는 만들지
   않는다" 로 닫은 것이 회피인가 정당한 자원 배분인가? 특히 마감 문서가
   "허용 서술" 로 남긴 네 문장 — 그중 "단량체 모델은 자가도핑 캐리어를 담기에
   부적합하다(100% 산화에 해당)" 를 방법론적 한계로 원고에 쓰는 것이 타당한가,
   아니면 그것도 우리가 증명하지 않은 주장인가?

2. **추출 부호 +0.34 eV 를 살려 둔 것이 맞나.** 근거는 complex_doped 와
   complex_doped_extr 의 차라 mol_doped 기준 결함이 안 들어간다는 것이다. 그런데
   그 두 잡은 phaseB(ISMEAR=1) 산이고, 같은 드롭의 mol_doped 자화가 0.175 였다.
   복합체끼리의 차라 정말 안전한가? 부호만 인용하는 것으로 충분한가?

3. **LREAL 비대칭의 크기 추정이 맞나.** 우리는 "복합체 안 분자 원자 30~35개의
   실공간 투영 오차" 가 잔차라고 봤다. 이 회계가 맞나? LREAL=.TRUE. 가 ROPT 없이
   원자당 수 meV 급이라는 통설이 이 계(ENCUT 520, PREC accurate, PAW)에 적용되나?
   그리고 delta_LREAL 을 "기준 분자만 LREAL=T 로 재실행" 으로 측정하는 설계가
   실제로 그 양을 재나 — 아니면 복합체 쪽을 LREAL=F 로 돌려야 하나?

4. **delta_m 과 delta_LREAL 을 한 잡에서 같이 바꾸는 것이 옳은가.** 우리는 잡 수를
   아끼려고 NUPDOWN 과 LREAL 을 동시에 바꾸자고 했다. 그러면 두 효과가 섞여
   개별 크기를 모르게 된다. 3잡 vs 6잡(각각 따로)의 trade-off 를 어떻게 봐야 하나?

5. **MAGMOM 미검증이 어디까지 무효화하나.** 자기 초기값을 확인할 수 없다는 것이
   pm1/net4 시드 계보 주장과 basin A/B 판정에 어떤 제약을 거나? "두 시드를 줬다"
   는 서술을 아예 못 쓰게 되나, 아니면 provenance 로 보완 가능한가?

6. **이 감사가 놓친 축이 무엇인가.** 우리는 INCAR 되울림 키만 봤다. 같은
   "기준과 대상이 같은 조건인가" 물음에서 INCAR 밖에 있는 축(k-점 밀도, 셀 모양,
   진공, POTCAR, 대칭)을 어떻게 점검해야 하나?

7. **neutral 마감을 pending 으로 내린 처리가 적정한가.** delta_m 에 이제
   delta_LREAL 이 더해졌다. 절대값과 0.346 eV 를 조건부 보류로 두고 원시 총에너지·
   접촉기하·자리선호 NO_VERDICT 를 유지하는 현재 분할이 맞나?

형식: 각 항목에 P0/P1/P2 와 근거. 동의는 "동의" 한 줄. 반박에 지면을 써라.
우리가 틀렸으면 틀렸다고 하고, 마감을 되돌려야 하면 그렇게 말해라.
```

---

## 왜 이 프롬프트인가

- **1번**이 본체다. 마감은 우리가 스스로 내린 판단이라 외부 심사가 없으면 "안 되니까
  덮었다" 와 구분이 안 된다.
- **3·4번**은 새 발견을 우리가 제대로 회계했는지 묻는다. 특히 4번은 우리가 비용을
  아끼려다 정보를 잃는 전형적 자리다 — 스스로 먼저 올린다.
- **5번**은 감사의 **못 하는 것**을 심사대에 올린 것이다. MAGMOM 미검증은 우리가
  고칠 수 없는 종류의 구멍이라, 어디까지 무효화되는지 남이 정해 주는 게 낫다.
