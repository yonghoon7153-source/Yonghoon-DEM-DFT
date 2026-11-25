---
title: "Codex 검토 요청 — VASP 외주 원샷 번들 (자리 선호 + E_ads)"
tags: [review/codex, sdcp, vasp, dft+u, handoff]
date: 2026-08-11
status: 회신 대기
대상: tools/sdcp/vasp_handoff_bundle.py (+ 내장 analyze_results.py)
---

# 무엇을 검토해 달라는 것인가

SDCP/PTFE 자리 선호를 **DFT+U 로 최종 판정**하기 위한 VASP 외주 번들 생성기다.
UMA 판정은 ptfe_c10 `MARGINAL_TENDENCY` · ptfe_dimer `SIGN_CONSISTENT_SMALL` 로 끝났고
(2026-08-11 유한설계 분류, 양쪽 검토 합의), DFT 가 다음이자 마지막 층이다.

**요구사항이 "원샷"이다** — 외주에 한 번 보내면 두 번째 왕복 없이 자리 선호와
흡착에너지가 다 나와야 한다. 그래서 기존 dft-handoff(자세 쌍만)를 넘어서:

| 구성 | 내용 |
|---|---|
| tier1/ | ptfe_c10 (5방향) + ptfe_dimer (3방향) 자격쌍 — 방향당 대표 roll 1개 |
| tier2/ | sdcp_neutral (6) + sdcp_doped (5) — 선택 실행 |
| refs/ | clean slab ×2 자기초기값 + 기체상 분자 ×4 (**E_ads 기준계**) |
| analyze_results.py | **stdlib 전용 독립 분석기** — 수렴 게이트 → 등록 유지(CONTCAR 최근접 양이온 MIC) → ΔE·E_ads·유한설계 분류 → RESULTS.json |
| MANIFEST.json | commit·gate_version·파일별 sha256·POTCAR 스펙 |

잡 수 (전체): 자세 52 + 기준계 6 ≈ **58**. tier1 만이면 20 + 6.

자기 초기값 2종(afm_balanced/afm_net4)은 **조각당 대표 1쌍에만** 건다(탐침).
나머지는 afm_balanced 하나 — 탐침에서 30 meV 넘게 갈리면 전체 재검토라는 규칙.

selftest 가 전 경로를 검증한다 (합성 자세 → 번들 생성 → 가짜 OUTCAR → 분석기 →
심은 ΔE/E_ads/분류 복원 일치 + PAIR_MIGRATED 게이트 작동 확인). GPU·실데이터 불필요:
`python3 tools/sdcp/vasp_handoff_bundle.py --selftest`

# 질문 (우선순위 순)

## Q1. INCAR 물리 — 이대로 외주 보내도 되나

슬랩 잡 (site_screen.INCAR_TEMPLATE 승계):
```
PBE+U(Ni d 6.2, Dudarev) · LASPH · IVDW=11(D3 zero damping) · ENCUT 520
ISMEAR=0/SIGMA 0.05 · LDIPOL/IDIPOL=3 · IBRION=2/NSW 200/EDIFFG -0.02
ISPIN=2 · MAGMOM=POSCAR 순서 재매핑(검산 내장) · LREAL=Auto · LORBIT=11 · LCHARG=.TRUE.
```
- IVDW=**11 유지**가 맞나? (2026-08-08 외주 수령분과의 일관성 때문에 11 을 유지 중.
  그쪽 JSON 이 11 을 'BJ' 로 잘못 표기했던 것도 이미 기록해 뒀다.)
- U=6.2(Ni) 는 그 외주와 같은 값이다. 다른 값을 쓸 이유가 있나?
- 열린 껍질 조각(sdcp_doped 라디칼)이 슬랩에 흡착된 잡 — NELECT 를 안 건드리고
  중성으로 두는 게 맞다고 봤다(라디칼+슬랩 = 중성 전체). 놓친 게 있나?
- ISYM 을 명시 안 했다(기본값). Selective dynamics + 흡착분자면 대칭이 거의 없어
  무해하다고 봤는데, 명시적으로 꺼야 하나?

## Q2. E_ads 기준계 일관성 — 오차 예산이 δ=30 meV 안에 드나

`E_ads = E(pose) − E(clean slab) − E(mol gas)`. 성분 간 차이:

| 항목 | pose/clean | mol | 일치? |
|---|---|---|---|
| 범함수·분산 | PBE+U(Ni)+D3(11) | PBE+D3(11), **U 없음(Ni 없음)** | ✔ (U 는 Ni 원자에만) |
| LREAL | Auto | Auto (일관성 우선으로 통일) | ✔ |
| 쌍극자 보정 | LDIPOL/IDIPOL=3 | **없음** | ⚠ 중성 분자·14 Å 상자라 ~meV 로 봤다 |
| k | 2 2 1 | Γ | ⚠ 분자는 Γ 로 충분 |
| EDIFF | 1e-5 | 1e-6 | ✔ (기준계가 더 조임) |

이 오차 예산이 판정 임계 δ=30 meV 대비 충분히 작은가? 특히 **쌍극자 보정 비대칭**이
걱정이다 — clean slab 도 LDIPOL 인데 분자만 없다. 세 성분 중 slab 쌍이 상쇄되므로
분자 쪽 무보정만 남고, 중성 분자면 무시 가능하다고 판단했다. 반박 바란다.

## Q3. 자기 탐침 경제 — 대표 1쌍에만 2종 초기값

전 쌍 ×2 면 잡이 ~100개가 된다. 탐침 설계(대표쌍만 2종, 30 meV 갈리면 전체 재검토)가
방법론적으로 수용 가능한가, 아니면 자기상태가 자세마다 다르게 수렴할 위험이 커서
전 쌍 2종이 필수인가? (2026-08-03 U 즉시투입 FM 붕괴 전력이 있어 조심스럽다.)

## Q4. 분석기의 등록 유지 게이트

CONTCAR 에서 분자 원자 ↔ 슬랩 Li/Ni 최근접 거리(MIC)로 시작 라벨과 대조한다
(`PAIR_MIGRATED` 차단). 충분한가? UMA 쪽 게이트는 결합 변화·추출·재구성까지 봤는데,
DFT 회수에서는 최근접 양이온 유지만 본다. 분자 결합 무결성(내부 결합 변화) 검사를
분석기에 추가해야 하나 — stdlib 로 공유결합 반경 테이블을 내장하는 비용 대비?

## Q5. δ=30 meV 가 DFT+U 층에서도 맞는 임계인가

UMA 층의 30 meV 는 방법 해상도로 정했다. DFT+U 에서 같은 셀·같은 설정의 두 자세 ΔE 는
그보다 정밀할 텐데(수 meV?), δ 를 내리면 판정력이 오르지만 자기상태·k-수렴 잔차가
그 아래 숨는다. DFT 층의 defensible δ 를 추천해 달라.

## Q6. k-mesh 2 2 1 (Γ) — 1×4 슬랩 셀

셀이 1×4 로 이방적인데 2 2 1 균등 메쉬다. ΔE(같은 셀 쌍 차이)에서는 k-오차가 크게
상쇄된다고 보고 유지했다. E_ads 절대값에는 남는다. 바꿔야 하나?

## Q7. 원샷 관점 빠진 것

이 번들로 못 하는 것이 나중에 두 번째 메일이 될 게 있나? (예: DOS/Bader 요청,
U-ramp 용 CHGCAR — LCHARG=.TRUE. 로 남기게는 해 뒀다, vibrational correction 등)

# 답 형식

Q 마다 **동의/수정/반박** + 수정이면 정확한 INCAR/코드 라인. 번들은 아직 외주에
안 보냈다 — 이 회신 반영 후 생성·발송한다.

---

# 부록 — 자체 리뷰(2026-08-11, 실행 검증 포함) 반영분

우리 쪽 적대 리뷰가 먼저 끝났다. **실제 2026-08-08 외주 납품 OUTCAR(.gz) 3개로 분석기
파서를 직접 돌려** 검증했고, 아래는 이미 고쳐서 커밋됐다 — 재지적 불필요:

| # | 발견 | 조치 |
|---|---|---|
| P0-1 | CONTCAR 없으면 등록유지 게이트가 **무음으로 꺼짐** (ok=true 로 판정 진입) | `REGISTRY_UNVERIFIED` 게이트 신설 + README 에 OUTCAR+CONTCAR 필수 명기 |
| P0-2 | 스펙 `Ni: Ni` 인데 실납품 TITEL 은 **Ni_pv** — 재사용 시 58잡 전부 MISMATCH 제외 | 스펙을 Ni_pv 로 (Phase-B 연속성) + 분석기가 "전 잡 일관 변형" 은 경고로 강등(혼합은 치명 유지) |
| P1-1 | 0바이트 CONTCAR 하나가 분석기 전체를 IndexError 로 전멸 | try/except → None → 위 게이트로 합류 |
| P1-2 | discover_pairs 가 프로토콜 지문 혼합을 무검사 통과 (verdict 는 하드 exit) | 지문 균질성 검사 + 깨진 JSON 관용 로드 |
| P1-3 | SCF 실패 시 탈출로 없음 → 2차 왕복 확정 | README 에 사전 승인 사다리(ALGO=All → 믹싱 완화) + NOTES.txt 기록 의무 |
| P1-4 | walltime·CHGCAR 보관·VASP 버전 지침 부재 | README 에 전부 추가. E_int/E_deform 은 범위 밖으로 명기 |
| P2 | POSCAR leftover 원소가 헤더에서 증발(잠복) · 자세별 z-범위로 고정 평면이 어긋날 수 있음 · 반쪽 번들 잔존 · 고아 잡 · 0쌍 zip | 원소별 grouping · **공유 zcut**(clean 슬랩 기준, n_fixed 감사 내장) · 스테이징+원자적 rename · 쌍 xyz 선검사 · 0쌍 중단. OUTCAR.gz 지원, NELM 전 스텝 검사, vasp 버전 기록 추가 |

파서 정합 실측: E0/NELM(세미콜론 줄)/TITEL/Iteration/magnetization 정규식 5종이 실물
VASP 5.4.4 OUTCAR 에서 전부 정확. 분자 상자 이미지 분산 ≈ −1.0 meV (vac=14 Å, δ 대비 무시).

→ 남은 것은 위 본문의 **물리 질문(Q1·Q2·Q3·Q5·Q6)** 이다. 코드 배선 쪽은 이중 검증됐다.
