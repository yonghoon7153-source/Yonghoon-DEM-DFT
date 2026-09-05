---
title: Research Agent Home
tags: [moc, research-agent]
updated: 2026-09-05 16:44
---

# Research Agent Home

> [!summary] 상태 (2026-09-05 16:44 KST)
> 누적 6편 · 분석 완료 5편 · triage 대기 0편 · 제외 1편 · research-agent v0.1.7

## 키워드 MOC
- [[dem battery]] — DEM(discrete element method) 기반 전극/복합양극 시뮬레이션
- [[dft battery]] — DFT/first-principles 기반 배터리 재료·계면 계산
- [[anode-less assb]] — Anode-less / anode-free 전고체전지 (추적 중단, 아카이브)

## 최근 디제스트
- [[2026-09-04]]

## 우선순위 상위 논문 (IF → 관련도)
| # | Tier | IF | 저널 | 노트 |
|---|---|---|---|---|
| 1 | A | 48.5 | Nature | [[2026 - Liu - Planar Li deposition and dissolution enable practical]] |
| 2 | A | 26.8 | Advanced Materials | [[2025 - Unknown - Revealing the Neglected Role of Passivation Layers of]] |
| 3 | A | 15.7 | Nature Communications | [[2025 - Ketter - Using resistor network models to predict the transport]] |
| 4 | A | 15.7 | Nature Communications | [[2026 - Kissel - Mechanofusion-derived cathode composite microstructures]] |
| 5 | B | 15.7 | Nature Communications | [[2026 - Wang - Domain oriented universal machine learning potential]] |

## 선별 품질
- [[피드백 보정]] — 판정 0건 누적
- 논문 노트 맨 아래 `## 피드백`에서 하나만 체크하면 반영된다

## 사용법
- 12:00 `ra noon` — alert 수집·triage·심층분석·DB·vault 갱신
- 09:00 `ra morning` — 디제스트 생성·메일 발송
- 주 1회 `ra feedback --show` — 체크박스 수집·보정 보고서 갱신
- 수동: `ra ingest --json file.json`, `ra analyze --paper-id <id> --from-file <json>`, `ra status`

```dataview
TABLE tier, if, journal, relevance FROM "Papers" WHERE status != "rejected" SORT if DESC
```
