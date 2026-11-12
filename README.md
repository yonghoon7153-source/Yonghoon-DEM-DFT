# lit-reader — 연구실 문헌 DB (텍스트판)

이 브랜치는 코드가 아니라 **자료**다. 이 저장소 `claude/friendly-meitner-lldvar` 의 `litdb/papers/` digest 를 연구실 PC 의 문헌 도구가 읽어 만든
**읽기 카드 · 뽑은 수치 · 장 서문**을 매일 밤 텍스트로 올린다. 사람이 보는 화면(논문 그림 포함)은 연구실 PC 에만 있다.
**이 브랜치에 커밋하지 않는다** — 다음 밤에 통째로 다시 덮인다. 다른 브랜치에 합치지도 않는다.

마지막 갱신 2026-11-12 09:44 · 논문 5편 · 읽기 카드 2편 · 수치 4건 · 장 1개

## 다른 브랜치의 세션에서 쓰는 법

```bash
git fetch origin lit-reader
git show origin/lit-reader:papers.csv | head -n 5          # 논문 목록 — 어느 장인지, 카드가 내린 한 줄 결론
git show origin/lit-reader:chapters/se-argy.md             # 장 서문 — 그 장에서 밝혀진 것 · 엇갈리는 곳 · 열린 문제 · 먼저 읽을 논문
git show origin/lit-reader:cards/<slug>.md                 # 논문 한 편의 읽기 카드
git show origin/lit-reader:values/<slug>.csv               # 그 논문에서 뽑은 수치 (digest 줄 번호 · 인용문)
git grep -n -i "Li6PS5Cl" origin/lit-reader -- cards chapters   # 낱말로 찾기
git worktree add ../lit-reader origin/lit-reader                  # 많이 읽을 때: 폴더로 펼쳐 놓고 grep (다 쓰면 git worktree remove)
```

찾는 순서: 주제에 맞는 장의 `chapters/<id>.md` 로 흐름을 잡고 → 거기 근거로 달린 slug 의 `cards/<slug>.md` →
숫자가 필요하면 `values/<slug>.csv` → 마지막으로 digest 원문(`claude/friendly-meitner-lldvar` 의 `litdb/papers/<slug>.md`)의 그 줄.

## 들어 있는 것

| 파일 | 내용 |
|---|---|
| `papers.csv` | 논문마다 한 줄: slug · 제목 · 저자 · 연도 · 축(dft/dem) · 장 · 카드의 한 줄 결론 · 카드 유무 · 수치 수 · DOI · digest 경로 |
| `chapters/<장 id>.md` | 장 서문(문장마다 근거 논문의 slug) · 이 장의 값 · 아직 열린 문제 · 먼저 읽을 논문 · 이 장의 논문 목록 |
| `cards/<slug>.md` | 읽기 카드: 결론 · 요점 · 본문 · 용어 · 우리 연구에 주는 뜻 · 핵심 수치 · 조심할 것. `(L61–63)` 은 digest 의 줄 번호 |
| `values/<slug>.csv` | 그 논문의 핵심 수치 절에서 뽑은 값: 물성 · 계 · 값 · 단위 · 조건 · 근거(basis) · 검증(status) · 줄 · 인용문 |
| `ml_values.csv` | 같은 값을 물성마다 한 단위로 맞춘 표 (σ 는 mS/cm, Ea 는 eV …) — 기계 학습 · 비교의 출발점 |
| `missing.csv` | 우리 논문들이 여러 번 인용하는데 라이브러리에 없는 논문 (DOI · 몇 편이 인용) |

CSV 는 UTF-8(BOM) · CRLF 다 (엑셀에서 그대로 열린다).

## 얼마나 믿을 수 있나

- 카드와 장 서문은 AI 가 쓰고 **기계 검사를 통과한 것만** 실렸다. 카드의 문장에는 digest 의 근거 줄이 붙고, 숫자는 그 줄에
  같은 표기로 있어야 실렸다. 장 서문의 문장은 근거 카드(slug)를 달고, 숫자는 그 카드에 있어야 실렸다.
- 요약과 해석은 틀릴 수 있다. **결정에 쓰는 숫자는 digest 원문의 그 줄에서 확인한다.**
- 수치의 `status` 가 verified 면 인용문이 그 줄에 그대로 있다. `basis` 는 stated(본문에 적힘) · figure_read(그림에서 읽음) ·
  derived_by_digest(digest 가 계산) · cited_from_other(다른 논문 인용). `answer_cut` 이 yes 면 답이 길이 제한에 잘려 일부만 있다.
- 장 서문에 '낡음' 이 있으면 그 뒤 그 장의 카드가 바뀐 것이다 — 다음 밤에 다시 쓴다.

## 장

| 장 id | 이름 | 장 서문 제목 |
|---|---|---|
| `se-argy` | 아지로다이트 조성 설계 | (아직 없음) |
