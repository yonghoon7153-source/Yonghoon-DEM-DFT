# Research Seminar — Cascade final package

최종 구성은 본문 21장 + 부록 7장, 총 28장이다.

## 파일

- `Research_Seminar_2026_08_cascade_final.pptx` — 발표용 최종 덱
- `Research_Seminar_2026_08_cascade_final_script_ko.md` — 슬라이드별 한국어 대본
- `Research_Seminar_2026_08_cascade_final_defense_QA_ko.md` — 예상 질문 24건과 방어 답변
- `Research_Seminar_2026_08_cascade_final_terminology_symbols.md` — 용어·기호·claim boundary
- `Research_Seminar_2026_08_cascade_final_source_ledger.md` — 슬라이드별 정본 출처표
- `claude_cascade_final_review_prompt_2026_08_11.md` — Claude 최종감사 요청문

## 발표 서사

`problem → provenance → cascade → audited gates → deployment questions → targeted DFT → ML label acquisition`

핵심 결론은 winner 선언이 아니라 다음 세 가지다.

1. versioned 47-species O/F snapshot
2. G1–G4의 audited 11-member heuristic endpoint
3. 다음 configuration-level label을 고르는 acquisition plan

## 검증 상태

- 28/28 slides에 speaker notes와 `[Sources]` 블록이 있다.
- notes의 66개 source reference가 모두 로컬 경로로 확인됐다.
- `slides_test.py` canvas overflow 검사 통과.
- Microsoft PowerPoint에서 28장을 실제 PNG로 export해 제목 잘림·겹침·placeholder를 확인했다.
- 재현 경로가 없던 radar 2개는 제거하고 canonical DB 표·카드로 교체했다.

