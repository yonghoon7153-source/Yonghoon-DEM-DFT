# 믹서 E0 역사 증거 내부 목록 — 수령 보충 (2026-11-13)

| Q | 필요한 것 | 권고 | 상태 |
|---|---|---|---|
| E0-R3 | Q5·건식 역사 증거의 원바이트/목록 관계 | 원 작성 측이 가림·수정 이력과 누락4의 정확한 원바이트를 확인하여 별도 정정본으로 회신. 지금 목록 재생성이나 로그 재실행으로 메우지 않음 | 내부 완전성 확인0 |

새 물리/코드 결함 판정이 아니다. 원 후보의 내용 판정을 철회하거나 새 P1/P2/P3로 계상하지 않는다. **전체 HOLD · 운영 재봉인 전 미해소**. 원 작성 측 회신은 1저자 경유; 자동 발송 없음.

## 1. 직접 대조

원 tgz SHA256 `2dc4e8af7eb37d521bd1961c1645cfb9845f9cb9f2d7ef433c5bf858f6333cc5`를 메모리에서 다시 읽어, 받은 정확한 멤버 바이트로 내부 목록을 대조했다. 새 ZIP 포장 중 누락·변형된 것이 아니다. 바깥 MANIFEST의 payload186은 정확히 맞고, 아래 **내부 목록**은 별개다.

| 원 tgz 내부 목록 | 일치 | 불일치 | 원 tgz에 없음 |
|---|---:|---:|---:|
| mixer_e0_v2/fix_q5/SHA256SUMS | 30/46 | 16 | 0 |
| mixer_e0_v2/reseal_dry/SHA256SUMS | 12/16 | 0 | 4 |
| mixer_e0_v2/review/scripts2/SHA256SUMS | 10/10 | 0 | 0 |

세부 파일·기대/현재 해시 = `docs/reviews/mixer_e0_pilot_registration_20261113/historical_manifest_receipt.json`. Q5의 불일치는 README와 과거 출력 로그에 있다. 가림 때문인지 등 최초 원인은 **미확정**이며 추정으로 해소하지 않는다. 건식 누락4는 summary.tsv, S1 build report.json, cand_reseal_files.sha256, K4_probe.out이다(정확한 멤버는 JSON).

앞 쪽지의 '9첨부 원바이트 동일'·'payload186 일치'·SELF-170 집중 회귀는 그대로다. 과거 **내부 목록 전수 일치**나 건식 재현 완결을 뜻하지 않는다. 활성 등록 후보와 규칙·문턱, 운영 source seal은 고치지 않았다.

## 2. 반입

- 바탕 B `56f4cfbb1d26371007b460a992d4cfc1ef68e950`; 같은 `codex/mixer-e0-1113`의 앞 두 커밋 다음.
- 추가 커밋 = `<<sha:docs: record inherited mixer evidence manifest gaps>>`.
- 파일 = 위 JSON + `docs/collab/codex_to_claude/20261113-0226_mixer-e0-historical-manifest-receipt.md`. 지운·옮긴 파일 없음.
- 검산 = tgz 바이트·내부 목록만. 본안 시험 재실행0. 앞 두 무인자 검사 결과를 이어받으며, 새 쪽지 경로는 doc refs 재검사한다.
- 공유 기록 제안: 진행 기록 믹서 E0 줄 뒤에 "11-13 수령 보충: 원 tgz 바깥 MANIFEST186 일치, 내부 Q5 목록16 불일치·건식4 원멤버 부재. 원인 미확정·원본/목록 무수정·원 작성 측 정정 확인 전 운영 재봉인 HOLD."를 추가. 원장 상태 변경 제안 없음.
