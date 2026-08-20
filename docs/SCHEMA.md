# docs/ 규칙

이 저장소의 문서는 세 종류다.

| 위치 | 성격 | 규칙 |
|---|---|---|
| `adr/` | 설계 결정 | 번호 순, 불변. 뒤집을 땐 새 ADR 을 쓰고 옛 것을 `대체됨` 으로 표시 |
| `raw/` | 불변 원본 | 스펙·세션 기록·외부 자료. **수정 금지**, 새 발견은 추가만 |
| 나머지 | 컴파일된 위키 | frontmatter 필수, `[[wikilink]]` 2개 이상 |

## ADR

`docs/adr/NNNN-kebab-slug.md`. 최소 구성:

```markdown
# ADR NNNN — 한 줄 제목

- 상태: 채택 | 제안 | 대체됨 (YYYY-MM-DD)
- 관련: <파일 경로들>

## 맥락
왜 결정이 필요했나. 무엇이 문제였나.

## 결정
무엇을 하기로 했나. 명령형 한 문단.

## 결과
좋아진 것과 **치른 대가**를 함께. 대가가 없다고 쓰지 않는다.

## 대안
고려했다 버린 선택지와 버린 이유.
```

## 위키 페이지 frontmatter

```yaml
---
title: 페이지 제목
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: concept | entity | comparison | query | guide | research-question | synthesis
tags: []
sources: [raw/specs/wrd-binary-format.md]
confidence: high | medium | low
explored: false
verificationStatus: unverified | verified | disputed
verifiedAt: YYYY-MM-DD            # verified 일 때만
verifiedBy: agent | human | both  # verified 일 때만
---
```

### 세 가지 직교 품질 축

| 필드 | 추적 대상 | 규칙 |
|---|---|---|
| `confidence` | 증거 강도 | high 로 올릴 때 반대해석/데이터 공백을 1줄 기록 |
| `verificationStatus` | 원본 대조 | 새 페이지는 `unverified`, 충돌은 양쪽 `disputed` |
| `explored` | 사람이 읽었는가 | **사람만** `true` 로 바꾼다 |

## 로그

`docs/log.md` 는 append-only. `## [YYYY-MM-DD] action | subject`.
action: `create` `update` `ingest` `verify` `lint` `fix` `start`.
충돌 시 양쪽 항목을 모두 남긴다.

## 태그

소문자, 하이픈. 페이지 3개 이상 모일 주제만 태그로 승격.
시드: `wrd-format` `electrochem` `degradation` `api` `web` `tooling` `dry-electrode`

## 검사

`make wiki-lint` (= `python3 tools/wiki_lint.py`). 오류 0 이어야 커밋한다.
