---
title: 인수인계 2026-08-20 밤 — 밤새 도는 것 · 아침에 볼 것
date: 2026-08-20
updated: 2026-08-20
tags: [handoff, gabia, neb, gap, disk]
status: 진행
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-20
verifiedBy: "당일 실행·검증 결과를 그대로 옮김 (91 tests · lint 0 errors · validator 0 위반)"
explored: false
authoredBy: agent
effort: low
claimType: process
evidenceScope: single-source
---

# 인수인계 — 2026-08-20 밤

## 밤새 도는 것 (gabia, 전부 정상)

| 작업 | 상태 | 볼 것 |
|---|---|---|
| `intra_211_k05_n15` (NEB, n=15/k=0.5) | ETA ~2 h. **fmax 가 처음으로 내려간다** (0.558→0.382) | 최종 프로파일 — 밴드 불연속이 닫히는지 |
| `inter_split_211` (split NEB) | step 233/400, fmax 오름 | `citable=false` 로 찍힐 것 (미수렴 밴드 위) |
| comp1 fixed-occ gap scf | 887 s/반복 — 느리다 | ★ nscf 시작 시 **irr k-point 170** 이 뜨는지 |
| `disorder_ensemble_diffusion` (modelc high-T MD) | 6h41m째 | 유실된 `A-highT-reseed-traj` 재생성 = β 게이트 입력 |

GPU 여유 3.4 GB — **새 작업 추가 금지.** `intra_211_k05_n15` 끝나고.

명령: `watch -n 30 bash tools/neb_diffusion/watch_cage_neb.sh` ·
`watch -n 60 bash tools/electronic/watch_gap_nscf.sh`
gabia 갱신: `git fetch origin claude/friendly-meitner-lldvar && git reset --hard FETCH_HEAD`
(결과 json 은 repo 에 회수해뒀으므로 reset 으로 잃는 것 없음)

## 오늘 판정된 것

- **comp1 2×2×2 밴 해제** → `reference`. Ea 0.2856 eV, 정본 대비 1.6–2.3× 인데 무질서
  앙상블 1σ(0.027 eV → 600 K 에서 1.69배) 안이다. 이상한 값이 아니다. 단 단일시드·β 미평가라
  정본은 아니다. → `kb/results/comp1_supercell_md_reassessment_2026_08_20.md`
- **gap 방법 플래그 하향**: '방법 불일치 의심' → **방법 비동질**. 정본이 EF 를 함께 적은 것으로
  보아 `parse_eig_gap.py`(고유값, smearing 무관) 재파싱본이다. DOS-threshold 오염이 아니다.
- **NEB 밴드가 찢어진다** (세 판 전부). 끝점은 수렴했고 홉 거리도 안 변했다.
  다른 Li 가 2–3.9 Å 씩 같이 움직인다 = **협동 이동**. 단일 Li NEB 질문이 성립하지 않는다.
  ⚠ 원인 (a)무질서의 물리 / (b)끝점을 독립 이완한 우리 버그 — **아직 안 갈렸다.**
- **Wu 2026 (Ta@LPSClBr)**: NEB 자체는 매끄럽다(fig_3 직접 봄). 정렬 이상화라 질문이 성립한 것.
  진짜 약점은 x_DFT 0.25 vs 명목 0.06(4배) · 두 셀을 **다르게** 부풀림(+3.7 % vs +26 %)이라
  Ta 효과와 팽창 효과가 분리 안 됨 · Fig S12c ↔ Fig 3l 내부 모순.

## 다음 실험 (결정됨)

**정렬 comp1 로 같은 NEB.** 매끄러우면 (a) 확정 → "단일이온 NEB 는 이상화" 판정이 굳는다.
정렬에서도 찢어지면 (b), 끝점을 **결합해서** 만들도록 고쳐야 한다
(시작을 이완 → 그 구조에서 이동 Li 만 옮겨 끝점 생성).

## 내일 주제

연구세미나. 3–7장 대본은 `kb/seminars/cascade_deck_3to7_script_2026_08_20.md` 에 있고,
**8–12장은 아직 안 봤다** (사용자가 보내주기로).

## 디스크 (닫힘)

C: 24 → **75.4 GB**. codex 임시 12.6 GB 삭제 + DEM 이미지 48.8 GB D: 이관.
⛔ `bml_kisti` 18 GB 는 **보존** — 파일명 168종 중 67종이 백업에 없다.
⚠ D: 가 이제 유일본을 둘 들고 있다 (KISTI 백업 + DEM 이미지). 이중화 우선순위 상승.
