---
title: "회신 P — INCAR 감사 fail-open · 추출부호 철회 · LREAL 회계 정정 (P0 3건)"
date: 2026-08-28
updated: 2026-08-28
tags: [review, codex, sdcp, incar, lreal, verdict]
status: 접수 — 구현 중
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-28
verifiedBy: codex
explored: false
authoredBy: human
effort: max
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 회신 P (2026-08-28) — 원문 보존

> 요청 프롬프트: `kb/reviews/codex_P_prompt_wave1_incar_audit_2026_08_28.md`
> 검토 고정점: 커밋 423a9255 + INCAR CSV 36행.
>
> **판정 요약**: 미질문 P0 3건(감사 fail-open · +0.34 endpoint 부재 · LREAL 회계) ·
> 1 마감 P1(허용문장 수정 후 재-ratify) · 2 추출부호 **P0 철회** · 3 LREAL **P0**
> (all-F 가 정본, 분자 T 재실행은 A_mix−A_F 를 못 잰다) · 4 동시변경 P1(delta_joint) ·
> 5 MAGMOM P1(seed 계보 주장에는 **P0**) · 6 감사축 P0(스키마 수정 전 "전수 통과" 금지) ·
> 7 neutral pending P1(상태명 reference_equivalence 로, 허용/보류 모순 제거).

아래는 회신 원문 그대로 (전사 수정 없음).

---

검토 고정점: 브랜치 `claude/friendly-meitner-lldvar`, 커밋 423a9255 및 첨부 CSV 36행.

## 먼저 고쳐야 할 미질문 위험

- **P0 — 전수 감사의 "동일" 판정이 fail-open이다.** 첨부 CSV에서 `SIGMA`, `KSPACING`, `NBANDS`, `NELM`, `ADDGRID`, `MAGMOM`은 36행 전부 공란이다. 따라서 "SIGMA=0.05가 36잡 동일"은 이 증거로 확인되지 않았다. 현재 `incar_diff`는 전부 미검출된 키를 단일값처럼 취급해 차이 목록에서 없앤다. `all_missing_unverified`와 `verified_equal`을 반드시 분리해야 한다.

- **P0 — +0.34 eV의 두 phase-B endpoint는 이번 CSV에 없다.** `complex_doped`와 `complex_doped_extr` 행이 0개이므로 이번 전수 감사가 그 부호를 검증했다는 연결은 성립하지 않는다.

- **P0 — `LREAL=.TRUE.`를 작은 원자당 오차로 간주할 근거가 없다.** `.TRUE.`는 `Auto`가 아니며, VASP는 잠재적으로 매우 부정확하고 권장하지 않는 방식으로 설명한다. 최종 에너지 비교에는 동일한 설정, 가능하면 `LREAL=.FALSE.` 단일점을 권고한다. "수 meV/atom" 기대는 최적화된 `Auto/ROPT` 문맥을 `.TRUE.`에 옮겨 쓴 것이다.

## 판정 요약

| 항목 | 판정 |
|---|---|
| 1. doped 범위 마감 | P1 — 마감은 정당, 허용 문장은 수정·재승인 |
| 2. 추출 부호 +0.34 eV | **P0 — 열역학적 추출 부호로는 철회** |
| 3. LREAL 회계 | **P0 — 현재 회계와 측정 설계가 틀림** |
| 4. NUPDOWN+LREAL 동시 변경 | P1 — 공동효과만 필요하면 가능, 분해에는 불가 |
| 5. MAGMOM 미검증 | P1, seed 계보·독립재현 주장에는 **P0** |
| 6. 감사 누락 축 | **P0 — 스키마 수정 전 "전수 통과" 금지** |
| 7. neutral pending 분할 | P1 — 방향은 맞으나 상태명·허용 필드 수정 |

## 1. 범위 마감 — P1

범위 마감 자체는 정당하다. 회신 O의 7조건은 doped 수치를 생산하려면 충족할 조건이지, 수치를 생산하지 않기로 한 경우까지 계산을 강제하는 의무가 아니다. 따라서 "현 프로토콜의 doped 흡착 수치를 만들지 않는다"는 자원 배분 결정을 되돌릴 필요는 없다.

다만 마감은 부정적 과학 결론이 아니다. 활성 doped closure 의 허용 문장은 다음처럼 고쳐야 한다.

1. "단일 E_ads가 정의되지 않는다" → **"현재 n=1 wave1 프로토콜은 인용 가능한 doped E_ads를 식별하지 못한다."**
2. "총자화가 맞지 않아 상태 배정이 불가능하다" → **"총자화만으로 carrier·국소 자기상태를 유일하게 배정할 수 없다."**
3. "Li 추출은 +0.34 eV로 불리하다" → 원고 허용문장에서 제거한다. 2번 판정처럼 원시 endpoint 차이로만 보존 가능하다.
4. "단량체는 자가도핑 캐리어를 담기에 부적합하다" → **"n=1,+1-hole 모델은 명목상 한 repeat당 한 hole이므로, 목표인 25–35% 평균 도핑과 extended-polaron estimand를 대표하지 않는다."**

한 hole/repeat가 명목상 100% hole loading이라는 것은 맞지만, 이것이 "단량체가 캐리어를 담을 수 없다"거나 실제 SDCP에 캐리어가 없다는 뜻은 아니다.

따라서 **마감은 유지하고 허용 문장만 수정한 뒤 재-ratify**하면 된다. doped E_ads를 다시 여는 계산은 필요 없다.

## 2. 추출 부호 +0.34 eV — P0

`mol_doped` 기준 에너지가 두 복합체의 직접 차에서 소거된다는 대수는 맞다. 그러나 그것만으로 "Li 추출이 열역학적으로 불리하다"는 estimand가 성립하지 않는다.

phase-B 결과에서 두 endpoint의 최종 총자화는 약 2.378과 0.518 μB로 다르다. 또한 각각 `r0_g20`과 `r180_g20`에서 온 서로 다른 endpoint이며, DFT basin 최소라는 입증 없이 MLIP 기하의 단일점으로 비교됐다.

서로 다른 pose 자체는 adiabatic basin-minimum 추출 에너지에서 금지사항이 아니다. 하지만 그 경우 양쪽 모두 같은 탐색·완화·상태선택 규칙으로 얻은 basin 최소여야 한다. 현재 자료는 그 조건을 충족하지 않는다. 같은 LREAL을 썼다는 사실도 두 서로 다른 기하에서의 투영 오차가 정확히 소거됨을 보장하지 않는다.

현재 보존 가능한 최대 문장은 다음뿐이다.

> 회신된 두 labeled endpoint의 단일점 에너지 차이는 E_extr − E_intact ≈ +0.34 eV였다. 두 endpoint의 자기상태와 basin 최소 동등성은 확인되지 않았으므로 이를 일반적인 추출 자유에너지나 열역학적 부호로 해석하지 않는다.

이 문장도 내부 기록용 `citable:no`가 맞다. 열역학적 부호를 복구하려면 다음 중 estimand를 먼저 고정해야 한다.

- vertical extraction: pose와 원자 배치를 가능한 한 고정한 동일 상태 비교
- adiabatic extraction: 양쪽 basin에서 동일한 DFT 탐색·완화·상태선택 후 최소끼리 비교

`ISMEAR=1` endpoint라면 에너지 convention과 실제 `SIGMA`도 함께 재감사해야 한다.

## 3. LREAL 비대칭 — P0

현재 혼합식과 목표 all-F 식: A_mix = E_C^T − E_S^T − E_M^F · A_F = E_C^F − E_S^F − E_M^F.
각 계의 LREAL 오차를 ε_X = E_X^T − E_X^F 라 하면 **A_mix − A_F = ε_C − ε_S** 이다.
따라서 남는 것은 "복합체 속 분자 원자 30–35개의 오차"가 아니다. 그 해석에는 ε_C ≈ ε_S + ε_M 이라는 환경독립·가산성 가정이 추가로 필요하다.

분자만 `LREAL=T`로 재실행하면 ε_M 은 측정할 수 있고 A_T = A_mix − ε_M 이라는 **all-T 값**은 만들 수 있다. 그러나 이것은 A_mix − A_F 를 측정하지 않는다. 비가산 잔차 ε_C − ε_S − ε_M 는 그대로 미측정이다.

따라서 canonical endpoint는 **all-F** 가 적절하다.

- 절대 E_ads: molecule F + complex F + matching slab F
- 동일 슬랩·basin을 쓰는 0.346 eV cross-fragment 차이: slab은 대수적으로 소거되므로 SDCP/PTFE의 관련 complex F와 각 free-spin molecule F만 있으면 된다.
- 현재 molecules는 이미 F이므로, 우선 필요한 분자 계산은 `free-spin + F`다.

## 4. NUPDOWN과 LREAL 동시 변경 — P1

동시에 바꾼 3잡은 실행 가능하지만 그 결과는 delta_m 이나 delta_LREAL 이 아니라 **delta_joint** 라고 불러야 한다. A = E(M0,F) 에서 제안한 3잡은 C = E(free,T) 를 만들고 C−A 만 준다. 분리하려면 분자마다 B = E(free,F) 와 C = E(free,T) 가 필요하다: δ_m = B−A · δ_LREAL = C−B. 즉 신규 6잡. 상호작용까지 분해하면 E(M0,T) 포함 9잡.

다만 이번 의사결정에 all-T endpoint는 필요하지 않다. 비용 대비 권고 순서:

1. 3개 기준분자를 `free-spin, LREAL=F`로 실행해 spin-reference 동등성 확인
2. 0.346 eV를 살릴 가치가 있을 때만 관련 SDCP/PTFE complex를 F로 재실행
3. 절대 E_ads까지 복구할 때 matching slab F 추가
4. 별도 방법론 연구가 아니라면 분자 T 계산은 생략

## 5. MAGMOM 미검증 — P1, seed 계보에는 P0

`MAGMOM`은 단순 메타데이터가 아니다. 최종 자기해가 초기값에 강하게 의존할 수 있다. `ISYM=0`이 symmetry 문제는 줄여도, 국소 basin 선택 문제를 없애지는 않는다.

입력 INCAR와 실행 provenance가 없으므로 현재 **금지해야 할 서술**:

- pm1/net4 초기 seed를 실제로 투입했다
- 서로 다른 두 seed가 같은 결과를 독립 재현했다
- 최종 basin이 특정 seed의 계보를 보존했다

잡 이름은 입력 증거가 아니다. 현재 **허용 가능한 표현**:

- "pm1/net4로 라벨된 회신 잡"
- "최종 OUTCAR의 per-Ni signed moment·flip index·occupation fingerprint에서 realized basin A/B가 관찰됐다"
- 해당 realized state의 원시 에너지

Seed 계보는 pre-dispatch INCAR 원본 해시, runner가 사용한 사본 해시, 회신 산출물의 run provenance를 연결해야 복구된다. 사후에 만든 expected manifest만으로는 부족하다.

## 6. INCAR 밖의 감사 축 — P0

감사 스키마부터 다음 상태를 구분해야 한다: `verified_equal` · `verified_different` · `all_missing_unverified` · `not_applicable` · `parse_error`. 주장에 필요한 키가 `all_missing_unverified` 또는 `parse_error`이면 fail-closed해야 한다. 이번 표에서 NELECT 산술과 `LREAL T 28 / F 8`은 확인되지만, 공란인 SIGMA 등을 동일하다고 승인하면 안 된다.

추가 감사 항목 최소 세트: KPOINTS 실제 mesh·shift·weight 또는 KSPACING / POTCAR 해시·원소 순서·TITEL/LEXCH·VASP 버전 / POSCAR·CONTCAR 해시, 셀·진공·선택고정, endpoint 기하 대응 / CHGCAR·WAVECAR 실제 read 증거와 부모 해시 (ICHARG 되울림만으로는 승계 증명 불가) / 마지막 완결 run segment·전자·이온 수렴·NELM 도달 / 에너지 convention 과 실제 SIGMA / FFT grid·NBANDS·ADDGRID·LREAL/ROPT / U·dispersion 전체 파라미터 / DIPOL 중심·dipole correction 조건 / 최종 국소자화·occupation·realized basin fingerprint / 실행 바이너리·빌드·계산 환경.

전자수 합계가 정확하고 홀수라는 사실은 doublet과 **양립**한다는 뜻이지, doublet ground state나 올바른 국소 carrier state를 증명하지는 않는다.

## 7. neutral 마감의 pending 처리 — P1

분할 방향은 맞다. 다만 상태명은 `closed_for_scope_pending_spin_equivalence` 보다 **`closed_for_scope_pending_reference_equivalence`** (또는 protocol_equivalence) 가 정확하다.

현재 neutral closure 는 exact value와 0.346 eV를 위쪽에서 허용하면서 뒤에서는 조건부 보류한다. **이 모순은 제거해야 한다.**

pending 동안의 분할:

- 유지: 원시 총에너지, 입력/회신 single-point 접촉기하, 자리선호 `NO_VERDICT`
- 금지: 절대 E_ads, 0.346 eV headline, mixed-protocol 값을 확정값으로 부르는 서술
- 주의: 접촉기하는 DFT 최적구조나 안정구조가 아니라 "평가된 기하"로만 표기
- 복구: 사전 문턱을 통과한 free-spin/F 기준과 필요한 complex/slab F 비교가 확보된 뒤 에너지 주장만 승격

## 최종 결론

- doped 범위 마감은 되돌리지 않는다.
- 활성 마감 문서의 허용 문장, 특히 +0.34 eV 문장을 수정하고 재-ratify한다.
- +0.34 eV는 열역학적 추출 부호가 아니라 상태가 맞지 않은 두 endpoint의 원시 차이로만 보존한다.
- `LREAL=.TRUE.` 분자 보정이라는 현재 설계는 all-F 오차를 측정하지 못한다.
- 감사기는 "전부 공란"을 "전부 동일"로 처리하지 않도록 먼저 고친다.
- neutral은 범위 마감 상태를 유지하되 `pending_reference_equivalence`로 넓히고, 절대값과 0.346 eV는 계속 non-citable로 둔다.
