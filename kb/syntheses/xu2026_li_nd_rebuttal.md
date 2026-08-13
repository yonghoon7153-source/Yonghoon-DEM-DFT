---
title: Xu 2026 의 "Li–Nd alloy SEI" 주장은 열역학·전자구조로 기각된다
date: 2026-08-11
updated: 2026-08-13
tags: [sei, li3nd, xu2026, argyrodite, nd, rebuttal]
status: 방어 중 — Li₃Nd c→c NEB **완료·인용 가능** (0.229 eV, CI) · 셀 수렴만 진행 중
confidence: medium
verificationStatus: verified
verifiedAt: 2026-08-11
verifiedBy: both
explored: false
authoredBy: agent
effort: high
claimType: interpretive
evidenceScope: multi-source-mixed
targetVenue: Paper#2 SEI 절 + 공동연구 회신 (docs/collab/sei_reply_draft_2026_08_11.md)
---

## Thesis

Xu 2026(LPSC-NdO)이 사이클 후 XPS 소피크 하나로 세운 "Nd³⁺ 가 Li 에 환원되어
Li–Nd alloy SEI" 서사는, Li–Nd 이원계에 안정 ordered 상이 0개(최근접 Li₃Nd 도
hull +0.197 eV/atom·theoretical)이고 0 V 평형 산물은 NdP 쪽이며 그 Li₃Nd 마저
실측 금속이라는 세 겹의 근거로 지지되지 않는다.

## Argument

1. **열역학**: MP 기준 Li–Nd 이원계 안정 ordered 상 0개. 가장 가까운 준안정상
   mp-976264 Li₃Nd 가 hull **+0.197 eV/atom** (theoretical 플래그) —
   kb/reviews/sei_neb_li3nd_rereview_request_2026_08_11.md.
2. **평형 산물**: grand-potential 0 V 산물은 0.3 Li₂O + 0.8 Li₃P + 4.1 Li₂S +
   0.2 **NdP** + 1.6 LiCl — Nd 는 합금이 아니라 인화물로 간다
   (kb/results/nd_anode_cathode_sei_formation_2026_06_24.md).
3. **전자구조**: 그 Li₃Nd 를 직접 계산하니 **금속** — N(E_F)=5.324 states/eV
   (±0.5 eV 평균 4.374), 채널은 Li s/p + Nd s/p/d
   (db/properties/sei_electronic_class.json). 금속상은 "전자차단 SEI 성분" 이점
   서사와 양립하지 않고, Xu 자신의 σ_e 4.7× 감소 관측과도 긴장 관계다.
4. **상대 근거의 얇음**: Xu 는 계산 0·Rietveld 0, 근거는 Nd 3d ~995 eV 소피크
   라벨 하나 (litdb/papers/xu2026_ndo_codoping_argyrodite.md §4·§11-7).

검증 경계: ①②는 자체 적대 리뷰, ③의 인용 문안("조건절 의무")은 Codex NEB 재리뷰가
확인. Li₃Nd DOS 실측 자체는 오늘 1회 계산 — 재현 런은 아직 없다.

### 4. Li 이동장벽 — **0.229 eV** (2026-08-13 완료, 인용 가능)

`/data/work/runs/sei_neb_v2_ccpath/li3nd` · `db/properties/sei_neb.json` 의
`v2_ccpath/li3nd` (`citable: true`, 4개 루트 중 유일).

| | |
|---|---|
| 홉 | Wyckoff **c→c**, 3.667 Å (8c 부격자, a/√2 = 3.666) |
| Ea | 정 0.228981 / 역 0.228958 eV — **대칭** (차 23 μeV) |
| CI | `CI_scheme = auto`, climbing image 5. no-CI 0.228980 → CI 0.228981 (**1 μeV**) |
| 셀·전하 | 2×2×2, 31원자. **금속이라 tot_charge = 0 · mv smearing · jellium 없음** |
| 수렴 | 경로 오차 0.039 < 0.05 eV/Å · 끝점 독립 이완 Δ 0 mV |

CI 가 값을 안 바꾼 게 결함이 아니다 — 대칭 홉이라 안장점이 경로 중앙에 있고
이미지 격자가 이미 그 점을 밟고 있었다. **비대칭 홉에서는 이렇게 안 된다**
(li3po4g c-d 처럼 자리가 다르면 CI 가 실제로 값을 올린다).

⛔ 같은 상의 `v2/li3nd` 2.072 eV 는 **c→b**, 즉 공공이 비싼 자리로 밀려가는
"일어나지 않는 홉" 이다. 장벽으로 인용하지 않는다 (`kb/results/li3nd_endpoint_asymmetry_2026_08_12.md`).

**인용 문안 (조건절 의무 — `sei_electronic_class.json` `cite_with`)**

> Even if Li₃Nd were to form kinetically — it lies 0.197 eV/atom above the Li–Nd
> convex hull and no stable ordered Li–Nd phase exists — it is metallic
> (N(E_F) = 5.324 states/eV) and presents a low Li migration barrier of 0.23 eV.
> It therefore cannot act as the electron-blocking interphase invoked in ref. X.

장벽만 떼어 쓰면 P2(안정상 0개)와 **모순돼 보인다**. 조건절과 hull 거리를 반드시 같이 쓴다.

## Counter-arguments

- **DB≠자연**: MP hull 은 0 K ordered convex hull. 실제 계면에선 준안정 kinetic
  산물이 국소적으로 생길 수 있다 — 그래서 우리 장벽 숫자도 "설령 생겼다 치더라도"
  조건절 + hull 거리를 반드시 병기한다 (db/properties/sei_electronic_class.json 의
  cite_with 규칙).
- **frozen-4f 한계**: 우리 DOS 는 4f 를 코어에 동결. 편재 채널만으로 N(E_F)>0 이면
  4f 를 더해도 gap 이 열리지 않아 금속 판정은 한 방향으로 안전하지만, 강상관 4f
  물리(콘도류)는 원리적으로 못 본다.
- **hull 오차**: +0.197 은 theoretical 항목이라 수십 meV 급 스캔·범함수 오차를
  가진다 — 다만 0.197 eV/atom 은 그 오차 규모를 크게 웃돈다.
- **조성 격차**: Xu 는 x=0.025 희석 극한, 우리는 x=0.2. 희석 한계의 국소 계면
  화학이 다를 수 있고, 우리 반박은 벌크 열역학+전자구조 층위다 — 그들 스펙트럼
  자체의 재배정까지 완결한 것은 아니다.

## Gap

- ~~Li₃Nd NEB 진행 중~~ → **완료 (2026-08-13)**. 0.229 eV, CI, 인용 가능.
  조건절 동반 의무는 그대로. 남은 것은 **셀 수렴 1건**: 2×2×2(31원자) 의 공공–공공
  이미지 상호작용이 미검증이다. 3×3×3(107원자, `sei_neb_v2_cc333`) 진행 중 —
  수십 meV 안에 들어오면 절대값 인용까지 열린다. 그 전까지는 **상 사이 비교**로만 쓴다.
- XPS ~995 eV 피크의 대안 배정(NdP? Nd⁰? 환원 NdOx?) — 우리가 계산으로 채울 수
  있는 빈칸이나 아직 착수 안 함.
- x=0.025(Xu 조성)에서의 grand-potential 재계산 없음 — 반박의 조성 이식성 미검.
