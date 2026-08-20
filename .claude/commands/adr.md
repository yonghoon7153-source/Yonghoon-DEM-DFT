---
description: 설계 결정 기록(ADR)을 한 장 만듭니다
argument-hint: <한 줄 제목>
allowed-tools: Bash(ls:*), Read, Write, Edit
---

`$ARGUMENTS` 에 대한 ADR 을 작성합니다.

1. `ls docs/adr/` 로 다음 번호를 확인합니다.
2. `docs/adr/NNNN-kebab-slug.md` 를 만듭니다. 형식은 `docs/SCHEMA.md` 참조:

   - `## 맥락` — 왜 결정이 필요했나. 무엇이 문제였나.
   - `## 결정` — 무엇을 하기로 했나. 명령형 한 문단.
   - `## 결과` — 좋아진 것과 **치른 대가**. 대가가 없다고 쓰지 않습니다.
   - `## 대안` — 고려했다 버린 선택지와 버린 이유.

3. `docs/index.md` 의 ADR 표에 한 줄 추가합니다.
4. `python3 tools/wiki_lint.py` 로 확인합니다.

기존 ADR(`0001` ~ `0006`)의 밀도와 정직함을 기준으로 삼으세요. 특히
`0005-multi-criterion-knee.md` 는 "왜 이 방법이고 다른 방법이 아닌가" 를
적는 방식의 예입니다.
