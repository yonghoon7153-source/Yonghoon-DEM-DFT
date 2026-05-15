# Literature DB 자동화 도구

> 문헌을 자동 fetch + 정리 + 검색 가능한 **개인 "Bible" DB** 구축 방법.
> 안용훈 PhD 프로젝트 (황화물 코팅 ML screening) 맥락에서 추천.

---

## TL;DR — 추천 스택

| 단계 | 도구 | 역할 |
|------|------|------|
| **Paper Discovery** | **OpenAlex** + Semantic Scholar API | 250M+ paper 자동 검색 |
| **Full-text fetch** | arXiv API + Sci-Hub (avoid for legal) | PDF/abstract 다운로드 |
| **Citation 관리** | Zotero + zotero API | bibtex, tag, organize |
| **Embedding / 의미 검색** | sentence-transformers + chroma DB | semantic search |
| **AI 요약** | OpenAI API 또는 Claude API | 각 paper auto-summary |
| **Knowledge graph** | neo4j (선택) | paper-concept-author 연결 |

---

## 1. Paper 검색 API

### 1.1 OpenAlex ⭐ 가장 추천
- **무료** (단, 2026년 2월부터 free API key 필요)
- **250M+ paper** 메타데이터
- **PyAlex** Python library: 의미 검색 + 키워드 검색
- **장점**: rate limit 관대 (100K/day with key), 메타데이터 풍부
- **단점**: full-text는 없음 (메타데이터/abstract만)

**사용 예**:
```bash
pip install pyalex
```
```python
from pyalex import Works
results = Works().search("argyrodite Li6PS5Cl cathode adhesion").get()
for work in results[:10]:
    print(work["title"], work["doi"], work["abstract"])
```

**Reference**: [PyAlex GitHub](https://github.com/J535D165/pyalex)

### 1.2 Semantic Scholar API ⭐
- **무료**, AI-powered (S2 graph 임베딩 활용)
- **200M+ paper**, 인용 그래프 강력
- Rate limit: 100 requests / 5 minutes (free), API key 신청으로 더 높임
- **장점**: paper 임베딩 직접 활용 가능 (similarity search)

**사용 예**:
```bash
pip install semanticscholar
```
```python
from semanticscholar import SemanticScholar
sch = SemanticScholar()
papers = sch.search_paper("argyrodite halide segregation NCM")
for p in papers:
    print(p.title, p.tldr)  # tldr = AI 한 줄 요약!
```

### 1.3 Crossref
- 메타데이터 표준. DOI 기반 lookup 안정적.
- `habanero` Python library.

### 1.4 arXiv API
- preprint 검색. Materials/chemistry는 cond-mat.mtrl-sci 카테고리.
- `arxiv` Python library.

### 1.5 Google Scholar
**비공식 API만 존재 (scholarly library)**. Rate limit 강함. 보조용으로만.

---

## 2. 자동화 워크플로우 — "내 Bible 만들기"

### 2.1 키워드 기반 자동 수집

```python
# scripts/automation/literature_harvest.py (구현 예정)
from pyalex import Works
from semanticscholar import SemanticScholar
import json
from pathlib import Path

KEYWORDS = [
    "argyrodite Li6PS5Cl",
    "halide substituted Li argyrodite Br Cl Li5.4",
    "all-solid-state battery cathode adhesion",
    "sulfide solid electrolyte NCM interface",
    "Li migration MLIP machine learning interatomic potential",
    "UMA universal materials atomistic FAIRChem",
    # ... 추가 키워드
]

def harvest(keywords, max_per_keyword=50):
    db = {}
    for kw in keywords:
        for work in Works().search(kw).get(per_page=max_per_keyword):
            db[work["id"]] = {
                "title": work["title"],
                "doi": work.get("doi"),
                "abstract": work.get("abstract"),
                "year": work.get("publication_year"),
                "authors": [a["author"]["display_name"] for a in work.get("authorships", [])][:5],
                "keyword": kw,
                "cited_by_count": work.get("cited_by_count"),
            }
    return db

if __name__ == "__main__":
    db = harvest(KEYWORDS)
    Path("kb/literature_db/raw.json").write_text(json.dumps(db, indent=2))
    print(f"Harvested {len(db)} papers")
```

### 2.2 AI 요약 (Claude API 또는 OpenAI API)

각 paper의 abstract를 우리 프로젝트 맥락에서 요약:

```python
# scripts/automation/auto_summary.py (구현 예정)
import anthropic
client = anthropic.Anthropic()

def summarize_for_us(abstract, title):
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{
            "role": "user",
            "content": f"""Paper title: {title}
Abstract: {abstract}

본 abstract를 다음 관점에서 한국어로 3-5줄 요약하시오:
1. 어떤 descriptor / 측정값을 제공하는가?
2. 우리 프로젝트 (LPSCl 도핑 + UMA + NCM 코팅 ML screening)에 어떻게 활용 가능한가?
3. 인용해야 할 핵심 정량값 (있다면)?
"""
        }]
    )
    return response.content[0].text
```

### 2.3 Semantic search DB 구축

각 paper abstract를 embedding으로 변환 → 의미 기반 검색:

```python
# scripts/automation/build_semantic_db.py (구현 예정)
from sentence_transformers import SentenceTransformer
import chromadb

client = chromadb.PersistentClient(path="kb/literature_db/chroma")
collection = client.get_or_create_collection("papers")
model = SentenceTransformer("all-MiniLM-L6-v2")

for paper_id, paper in db.items():
    text = f"{paper['title']}\n{paper.get('abstract', '')}"
    embedding = model.encode(text).tolist()
    collection.add(
        ids=[paper_id],
        embeddings=[embedding],
        metadatas=[paper],
        documents=[text],
    )

# 검색 시
query = "vacancy migration mechanism argyrodite NCM interface"
results = collection.query(query_texts=[query], n_results=10)
for hit in results['metadatas'][0]:
    print(hit['title'], hit['doi'])
```

### 2.4 BibTeX export (Zotero / Mendeley 호환)

```python
# scripts/automation/export_bibtex.py (구현 예정)
from pybtex.database import BibliographyData, Entry

bibdata = BibliographyData()
for pid, paper in db.items():
    entry = Entry('article', fields={
        'title': paper['title'],
        'author': ' and '.join(paper['authors']),
        'year': str(paper['year']),
        'doi': paper.get('doi', ''),
        'abstract': paper.get('abstract', ''),
    })
    bibdata.entries[pid] = entry
bibdata.to_file('kb/literature_db/references.bib')
```

Zotero에 import → 자동 정리.

---

## 3. "Bible" DB 검색 인터페이스 (제안)

### 3.1 CLI tool
```bash
# 검색
python scripts/automation/search_bible.py "Cl-O Pauli repulsion adhesion"
# → Top 10 paper + AI summary 출력

# 새 paper 추가 (수동)
python scripts/automation/add_paper.py --doi 10.1021/...

# 자동 업데이트 (cron job)
python scripts/automation/literature_harvest.py --update
```

### 3.2 Web UI (Phase 2 옵션)
- Streamlit / Gradio로 간단 web app
- Search bar + paper card view
- 개인 노트 추가 기능

### 3.3 Claude Code 통합
- 본 repo에서 Claude가 직접 literature DB 검색 + 인용 가능
- `kb/literature_db/raw.json` 을 자동으로 참조

---

## 4. 구현 우선순위 (Phase별)

### Phase 1 (즉시 ~ 1개월): 기본 harvesting
- [x] OpenAlex + Semantic Scholar API 사용법 학습
- [ ] `scripts/automation/literature_harvest.py` 구현
- [ ] 키워드 리스트 작성 (argyrodite, MLIP, NCM coating, ...)
- [ ] 100~500 paper 수집 + raw.json 저장

### Phase 2 (1-3개월): 의미 검색 + AI 요약
- [ ] Sentence-transformer embedding
- [ ] Chroma DB 구축
- [ ] Claude API 통합 (AI summary)
- [ ] CLI search tool

### Phase 3 (3-6개월): Knowledge graph
- [ ] neo4j 또는 simple graph
- [ ] paper-concept-author 연결
- [ ] 새 paper alert (RSS-like)

### Phase 4 (6-12개월): Production
- [ ] Web UI (Streamlit)
- [ ] Zotero 양방향 sync
- [ ] BibTeX auto-export
- [ ] Citation 추천 (writing 도움)

---

## 5. 추가 도구

### 5.1 ChemNLP
화학 paper specific NLP. 화학식, 반응 자동 추출.
- GitHub: https://github.com/AI4Chemistry/chemnlp

### 5.2 Mat2Vec
재료과학 word embedding. composition → 잠재 표현.
- Paper: Tshitoyan et al. Nature 2019.

### 5.3 LitLLM
Scientific literature review toolkit. 자동 review 생성.
- [arxiv 2024](https://arxiv.org/html/2402.01788v2)

### 5.4 PaperQA
"바이블 자동 Q&A". 본 컬렉션에서 자연어 질문 → 답변 + 인용.
- pip install paper-qa
- 본 프로젝트에 매우 적합.

### 5.5 AutoResearchClaw
자율 research (idea → paper). Phase 4 검토 대상.
- GitHub: https://github.com/aiming-lab/AutoResearchClaw

---

## 6. 키워드 리스트 (suggested for harvest)

본 프로젝트 관련 priority keywords:

### Argyrodite / Sulfide SE
- argyrodite Li6PS5Cl Br I
- halide substituted lithium argyrodite
- Li5.4PS4.4 Cl Br
- LPSCl LPSBr halogen ratio
- sulfide solid electrolyte conductivity
- anion site disorder 4a 4d argyrodite

### 계면 / Adhesion
- all-solid-state battery cathode interface
- sulfide / NCM interface stability
- LiNbO3 ZrO2 buffer coating cathode
- Li2S surface termination argyrodite
- W_ad adhesion energy solid electrolyte cathode

### MLIP / Computational
- machine learning interatomic potential MLIP universal
- UMA FAIRChem universal materials
- MACE NequIP CHGNet M3GNet foundation model
- DFT high-throughput screening battery materials
- atomate2 jobflow workflow MLIP

### ML / Screening
- active learning materials discovery battery
- Bayesian optimization solid electrolyte
- inverse design generative model materials
- composition-property mapping machine learning

### Halide segregation / Doping
- halide segregation Cl Br argyrodite interface
- cation doping LPSCl Na K Mg
- anion doping F I substitution argyrodite

### Mechanism / Descriptors
- bond density descriptor adhesion
- Madelung field solid electrolyte
- ionic radius compatibility site preference
- Pauli repulsion anion oxide interface

---

## Sources

- [OpenAlex docs](https://developers.openalex.org/)
- [PyAlex GitHub](https://github.com/J535D165/pyalex)
- [Semantic Scholar API](https://pypi.org/project/semanticscholar/)
- [Research Paper APIs 2026 (IntuitionLabs)](https://intuitionlabs.ai/articles/research-paper-apis-scientific-literature)
- [LitLLM Toolkit](https://arxiv.org/html/2402.01788v2)
