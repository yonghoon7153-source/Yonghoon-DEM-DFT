# 최종 release 감사 보고 — Research_Seminar_2026_08_cascade_final (28장)

> 감사자: Claude · 2026-08-11 밤 · 요청: final package 동봉 리뷰 프롬프트.
> 대상: 덱 28장 + 지원 문서 4종. 전 슬라이드 텍스트 정독 + 핵심 2장 렌더 육안 + 수치 전수 검산.

## 판정: **ACCEPT** (블로커 0 · 사실 정정 1 · 사용자 선택 1)

## A. 데이터 계보 — 통과
- 273 = 91 × 3 attempted run slots ✓ (S3·S5, script 동일)
- 47 = 2026-06-25 versioned snapshot, 37 ox + 10 F, **141 records** ✓ (champions.csv 141행 실측 재확인)
- 273→47 을 물리 funnel 로 그린 곳 **없음** ✓ (S5 노트가 명시적으로 부정)
- 47→43→25→11 은 post-hoc audit 로만 ✓ · G5 = ranking-only ✓ · x 라벨 nominal ✓

## B. 수치 전수 검산 — 전부 일치
| 슬라이드 주장 | 원자료 | 판정 |
|---|---|---|
| S15: LiF ΔE_H2S 0 / MgO −19.2·−74.3 / CaO −74.3·−253.3 / Cu₂O −340.9 | `cascade_stability_axes.csv` (T11) | ✓ 4/4 |
| S15·S14: Cu₂O ΔG_hyd,lit +1.267 (MS proxy) | themes.json `dG_hyd_MS_lit` | ✓ |
| S14: MgO·CaO cost tier 1 | themes.json | ✓ |
| S18: 9/35 one-direction, 26/9/12 | `cascade_air_axis_lit_vs_tier.csv` | ✓ |
| S19: B₂O₃ stops G4 · **Nd₂O₃ stops G3** | scorecard first-stop | ✓ (정정 반영 잘됨) |
| S20: Cr₂O₃ Vox 2.356 · HfO₂ Vred 1.242 | themes.json | ✓ |
| S20: **champion site Li_24g (둘 다)** | `cascade_v23_litransport.csv` `cation_site` | ✓ — **빌드 기록 층의 사실.** 이전 내 지적(heuristic)은 문헌 선호 층 얘기였고, 캠페인 구조가 실제로 Li_24g 에 앉힌 건 맞다. 두 층 다 참 |
| S20: v1 #1 → v2 rank #8 | `codoping_ml_v2.csv` rank=8 | ✓ |
| S6 로스터 47종·5족·PASS 11 bold·† 2 | scorecard | ✓ (렌더 육안) |
| 120 순열 · unique kill 0 · 6/6 trade-off | guide·scorecard·ox-transport CSV | ✓ (기존 검산 유지) |

## C. 지시서 이행 — 통과
- SDCP **0회 등장** ✓ (원장 4행 재구성: 1.33× / β / DOS / raw-HSAB 강등)
- N1 로스터 ✓ (내 초안 디자인 채택) · N2 질문-축 지도 ✓ (+실후보 열 보강 — 개선)
- N3 레이더 대신 **S15 T11 트레이드오프 표** — 수치 검증되는 대체안으로 인정
- evidence 태그(OURS/STATIC/CURATED/LITERATURE/MP-THERMO) 화면 배치 ✓ · source 3층 체계 ✓
- 지원 문서 4종: script 28절(장수 일치) · defense QA · terminology · source ledger — 상호 모순 없음

## 사실 정정 1 (블로커 아님)
source_ledger §radar: "`cascade_radar_axes_origin.csv`·`fig_cascade_radar.py`·`cascade_radar_*.png` 가
저장소와 origin branch 에 없어 재현 불가" → **사실과 다름.** 세 파일 모두 origin
`claude/friendly-meitner-lldvar` 커밋 `9ee411a3`(2026-08-11) 에 존재:
- `db/properties/cascade_radar_axes_origin.csv` (47행 × 8축)
- `tools/figures/fig_cascade_radar.py` (재생성 1분)
- `docs/figures/cascade/cascade_radar_{6panel,pair_CrHf}.png`
Codex 클론이 push 이전 시점이었던 것으로 보임. **원장 문구만 정정 필요** — 덱 자체는 레이더 없이도 일관됨.

## 사용자 선택 1
레이더(육각형/팔각형)는 사용자가 명시적으로 원했던 그림. 소스가 실존하므로 원하면
부록 1장(또는 S20 우측)으로 복원 가능 — 발표자 취향 결정 사항. 복원 시 위 경로 그대로.

## 결론
28장 덱·대본·QA·용어집·원장 모두 release 가능. 남은 손작업은 종전과 동일
(발표 길이 확정, 리허설). 이 보고와 함께 패키지 전체를 kb/seminars/ 에 등재함.
