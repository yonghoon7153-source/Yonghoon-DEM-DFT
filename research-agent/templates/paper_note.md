---
title: "{{title}}"
aliases: ["{{short_title}}"]
authors: {{authors_yaml}}
journal: "{{journal}}"
year: {{year}}
doi: "{{doi}}"
url: "{{url}}"
if: {{if}}
tier: "{{tier}}"
relevance: {{relevance}}
status: {{status}}
keywords: {{keywords_yaml}}
tags: {{tags_yaml}}
source: {{source}}
date_added: {{date_added}}
analyzed_at: {{analyzed_at}}
evidence_level: {{evidence_level}}
ra_id: "{{id}}"
---

# {{title}}

**{{authors_line}}** — *{{journal}}* ({{year}}) · IF {{if}} · Tier {{tier}} · 관련도 {{relevance}}
{{doi_line}}
키워드: {{keyword_links}}

> [!abstract] 한 줄 요약
> {{one_liner}}

## 선정 이유
{{selection_reason}}

## 핵심 내용
{{key_findings_md}}

## 방법
- **시스템**: {{m_system}}
- **기법**: {{m_technique}}
- **파라미터**: {{m_parameters_md}}
- **검증**: {{m_validation}}

> [!tip] 내 연구와의 연결
> **DEM** — {{c_dem}}
> **DFT/MLIP** — {{c_dft}}
> **실험(축 C)** — {{c_exp}}

### 비교할 수치
{{numbers_md}}

## 논문 작성에 쓸 곳
- **Introduction**: {{u_intro}}
- **Methods**: {{u_methods}}
- **Discussion**: {{u_discussion}}

> [!quote] 인용 문장 초안
> {{citation_sentence}}

{{scooping_block}}
> [!warning] 비판 포인트 / 세미나 질문
{{critique_md}}

## Follow-up
{{follow_up_md}}

## 원문 초록
{{abstract_block}}

---
*related:* {{related_links}} · *digest:* {{digest_link}}
