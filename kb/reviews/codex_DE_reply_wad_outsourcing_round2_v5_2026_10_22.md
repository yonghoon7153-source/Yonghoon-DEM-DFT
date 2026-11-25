---
title: "DE 회신 — W_ad 외주 2차 묶음 v5 (9ddfbe448 · MANIFEST 714324cc…): GO · 발송 동의 · P0/P1 없음 · 비차단 P2 1 (selftest 시험 이름의 -0 설명)"
tags: [review, wad, adhesion, vasp, outsourcing, runner, checker, codex, reply, letter]
letter: DE
date: 2026-10-22
track: wad
channel: codex
kind: reply
status: 수령 2026-10-22 (사용자 붙여넣기 · 원문 보존 · 마크다운 링크의 Codex 로컬 경로만 파일 이름 · 행으로 줄임 · 판정은 본문대로 GO · 재현 자료 summary.json 은 붙여넣기에 없음 — 이름만)
confidence: medium
verificationStatus: verified
verifiedAt: 2026-10-22
verifiedBy: self
explored: false
authoredBy: external
claimType: mixed
evidenceScope: multi-source-primary
---

> 프롬프트: `codex_DE_prompt_wad_outsourcing_round2_v5_2026_10_22.md` (기준 커밋 `9ddfbe448`) · 트랙 W_ad (1저자 = 사용자). 아래는 원문이다 (고치지 않는다 · W 숫자 없음).

---

GO — 이번 변경 범위에서 DD의 재승인 조건 셋은 해제됐습니다. 묶음 v5 발송에 동의합니다. P0/P1 없음, 비차단 P2 문구 1건입니다.
대상은 커밋 `9ddfbe448f4efab34311eb1d7e12b6ba5e6eb906`, 아래 MANIFEST로 고정합니다.

```
714324cca0d0f05e39966543e3ffa76956fe51109e13f192cad6dc7f8e04cfed
```

Q-DE-1 — 봉인 필터: GO
[1916행 (line 1916)](build_round2_vasp_package.py:1916)이 `run_aborted` 루트의 감사 불가 기록을 보존하고, 실제 봉인 거부까지 연결합니다.
독립 자식 프로세스 CLI 시험 12건이 모두 기대 결과였습니다.

* 정상 반송: 종료 0, 등록부 생성.
* `listdir(run_aborted)`만 EIO 또는 PermissionError로 실패: 종료 2, `AUDIT_UNREADABLE`, 등록부 미생성.
* 새 보존 조건만 제거한 대조판: 같은 오류 네 사례에서 종료 0과 등록부 생성으로 DD 결함이 다시 나타났습니다.
* 후속 `scandir`는 정상 작동하도록 유지했습니다. 전체 디렉터리 접근을 막아 우연히 차단된 시험이 아닙니다.

[독립 실행 결과](summary.json)
Q-DE-2 — rc 원문 전달: GO
[359행 (line 359)](build_round2_vasp_package.py:359)의 환경변수 전달은 적절합니다. `\060`·`\061`을 `awk -v`의 이스케이프 처리에 노출하지 않고, 기존 정규식이 원문을 검사하게 합니다.
`ENVIRON`에서 읽은 숫자 문자열의 비교 특성도 정상 입력 처리와 모순되지 않습니다. 따라서 이번 해결에 Bash 검사를 중복 추가할 필요는 없습니다. [GNU awk 문서](https://www.gnu.org/s/gawk/manual/gawk.html), [mawk 문서](https://invisible-island.net/mawk/manpage/mawk.html)
다만 제가 이 환경에서 gawk·mawk를 직접 재실행한 것은 아닙니다. 이 부분은 배포 러너의 데이터 흐름·공식 의미론·제공된 Linux 실행 결과를 대조한 판정입니다. Python 측 44개 판정 사례는 독립 실행해 기대값과 일치했습니다.
Q-DE-3 — 도구·러너·MANIFEST 결박: GO
독립 확인 결과:

* MANIFEST 170개 항목의 해시 모두 일치.
* 배포 파일 전체 172개 확인.
* v4 대비 변경은 선언한 네 파일뿐.
* 잡 입력 166개 바이트와 24개 잡 행은 동일.
* 배포 `run_all.sh`와 `run_all_text()` 출력 동일.
* 실제 도구 SHA와 `jobs.json.tool_sha256` 동일.
* 기존 D3 기록값을 정확히 같은 원자·좌표·격자에 연결한 재생성에서 172개 파일 전부 바이트 일치.

마지막 검사는 생성 결정성과 결박 검사입니다. D3 값을 새로 계산하거나 그 과학적 타당성을 재검증한 것은 아닙니다.
부록 A도 예상한 두 실패만 허용했고, 추가 실패를 주입하면 거부했습니다.
Q-DE-4 — 같은 종류의 수정과 P2: GO, 문구 1건 잔존
INCAR 값의 이스케이프 문제를 함께 고친 것은 타당합니다. ENCUT도 숫자 꼴 검사 뒤 비교하도록 러너와 Python을 맞췄습니다.
독립 Python 시험에서 경계 사례 20개와 실제 `check_attempt` 기록을 통과시킨 상태 전이 6종을 확인했습니다.

* `520`, `520.0000`: ⓑ 판정 경로로 진행.
* `5.2e2`, `520abc`, `\06520`, `520.06`: `STAGE_A_INELIGIBLE`, ⓑ 경로에 진입하지 않음.
* DD의 함수를 복원하면 `5.2e2`가 다시 허용되어, 시험이 수정점을 실제로 검출합니다.

배포 셸에서도 `enc_eq`가 실제 ⓑ·r2 실행 앞에 연결돼 있습니다. 새 차단 결함은 발견하지 못했습니다.
남은 P2 — selftest 설명 한 줄이 아직 틀립니다.
[3422행 (line 3422)](build_round2_vasp_package.py:3422)은 `-0`까지 “검사기는 `ATTEMPT_MISMATCH`”라고 묶습니다. 정상 합성 기록의 `rc=-0`은 Python에서 정수 0이 되어 검사기가 받아들이므로, 이 출력 문구는 실제 동작과 다릅니다.
다음처럼 나누면 됩니다.
`0.5·1e3는 검사기 ATTEMPT_MISMATCH; -0은 Python OK / runner SCF_UNVERIFIED.`
이번 편지와 새 빌드 기록의 정정은 맞습니다. 미등록 흔적 보장 범위를 반송되어 도착한 자료로 한정한 설명도 맞습니다. 이 시험 이름 잔존만으로 v5를 다시 만들거나 발송을 보류할 필요는 없습니다.
Q-DE-5 — 발송: GO
위 MANIFEST의 v5를 업체에 보내도 됩니다. 승인된 물리 설계·문턱·잡 행렬은 다시 열지 않았으며, 이번 변경으로 그 승인을 뒤집을 결함은 찾지 못했습니다.
검증 범위는 구분합니다. Linux 전체 `186/186`, 배포본 `184/186`, 작성자의 mutation 7종은 제공된 실행 보고입니다. 저는 별도로 Python 음성시험·CLI 봉인·수정 제거 대조·파일 해시·기록값 기반 재생성을 확인했습니다. 실제 VASP·UMA·DFT 계산과 원본 저장소 수정은 하지 않았습니다.
추가 발송 해제조건은 없습니다.
