# 건식 후막 Bimodal 전고체 복합양극 — 실험 파트 (2차년도)

> **과제:** (상위) 세라믹 공정 기반 황화물계 전해질 및 고용량 후막 전극 친환경 제조·응용기술 개발
> (세부) **세라믹 catholyte 기반 전극 성능 향상을 위한 단결정 양극재 제조 기술 개발**
> 기간 2025.10.01 ~ 2028.12.31 · 주관 ㈜엘앤에프 · 공동 한국전자기술연구원(KETI) / 한양대학교(이종원)

이 브랜치(`claude/solid-state-cathode-improvement-hevry0`)는 **건식 후막 bimodal 전고체
복합양극의 성능 개선**을 위한 **독자적 실험 파트**입니다. DEM/MPM 시뮬레이션 브랜치
(`claude/stoic-knuth-NObVQ`)와 **연계**하되, 실험(소재·전극제작·전기화학·EIS-TLM)과
2차년도 설계 업무를 이쪽에서 관리합니다.

```
DEM/MPM (stoic-knuth)  ──전달/역학 시뮬레이션──┐
                                              ├──► P2D / ML 설계 (양 브랜치 공유)
실험 (이 브랜치)        ──소재/전극/전기화학──┘
```

## 폴더 구조
| 경로 | 내용 |
|---|---|
| `docs/project/` | 과제 개요, 2차년도 계획, 킥오프/연차보고서/회의록 digest, 이슈·수정 로그 |
| `docs/project/sources/` | 원본 자료 (kickoff PDF, 연차보고서 PDF, 6/25 성능평가 PDF, 회의노트 docx) |
| `db/` | 구조화된 실험 데이터베이스 (CSV) — 소재·전기화학·로딩·모델·SEM |
| `litdb/` | **논문 에이전트(litdb-curator)** 문헌 DB 시스템 (DEM 브랜치에서 이식·적응) |
| `.claude/agents/litdb-curator.md` | 논문 에이전트 정의 |

## 빠른 시작
- **무슨 데이터 있나** → `db/README.md` (데이터 사전)
- **어디까지 되어있나(진행현황)** → `docs/project/06_STATUS.md`
- **2차년도 뭐하나** → `docs/project/01_YEAR2_PLAN.md`
- **과제 전체 그림** → `docs/project/00_PROJECT_OVERVIEW.md`
- **킥오프/보고서 문제됐던 부분/수정** → `docs/project/05_ISSUES_AND_FIXES.md`
- **미팅 기록(날짜별)** → `docs/project/meetings/`
- **건식·바이모달 관련 논문** → `litdb/DRY_THICKFILM_INDEX.md`
- **논문 정리** → PDF 업로드 후 **"논문 에이전트 실행해줘"** → `litdb/papers/` + `litdb/INDEX.md` 갱신

## 핵심 소재 명명 (혼동 주의 — 자세히는 `db/materials/`)
| 실험 명 | 연차보고서 명 | 종류 | Ni/Co/Mn (ICP) | D50 | 비용량 | 표면 |
|---|---|---|---|---|---|---|
| **No.1** | NCM_2 (L&F) | 단결정 소립 | 82.5 / 12.7 / 4.8 | 3.94 µm | 205.9 mAh/g | 매끈 |
| **No.2** | NCM_3 (L&F) | 단결정 소립 | 86.9 / 5.7 / 7.4 | 3.84 µm | 213 mAh/g | 표면 잔류물(satellite) |
| **Poly** | 대립(우리소재) | 다결정 대립 811 | ~Ni 88 | ~10 µm(2차) | 200 mAh/g | cauliflower(다수 1차입자) |
| (NCM_1) | NCM_1 (자체구입) | 단결정, 미사용 | 78 / 17 / 4 (EDS) | 5.0 µm | (DC 198.7) | 응집·불순물 |

> ⚠ 연차보고서의 `NCM_1/2/3` ↔ 실험의 `No.1/No.2/Poly`는 **다른 명명체계**.
> `NCM_1`(자체구입, 5 µm 응집)은 No.1/No.2/Poly 세트에 **포함되지 않음**.
