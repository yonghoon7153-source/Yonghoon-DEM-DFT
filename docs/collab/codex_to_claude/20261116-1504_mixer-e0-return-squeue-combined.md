# E0 완료 수령 + squeue 고침 통합 인계

| 트랙 | 계산 | 상태 | 숫자 | 다음 |
|---|---|---|---|---|
| 믹서 E0 | 366423 한 팔 | 결과 회수·개발 관측 OK | 03:53:26 · NP20 · 덤프1121 · 원자100000 | W9 종료 직후 영수증 부재 처분 · 1저자 자격 수용 판단 |
| 믹서 도구 | purged squeue 처리 | 고침 push 완료 | 새12/12 · 기존19 pass/1 skip | 이번 통합 인계에서 함께 반입 |
| 다음 회전 | 기존 N0 저장계획 | 검토 문서만 | 32976 step · 234장 · bin1 100장 | 기존 간격·17자리 유지 권고, 자동 GO 없음 |

## 1. 가지와 반입 순서

- 새 짝 = Claude 본 세션 `claude/stoic-knuth-NObVQ`. 대피 `claude/sdcp-dem-manuscript-si-pqwtv8`는 `2da71fe5abbaa856beb87c39c2a49424e4c87bc7`에서 정지한다.
- 이 수령 가지 = `codex/mixer-e0-return-1116`, 바탕 `2da71fe5abbaa856beb87c39c2a49424e4c87bc7`. 15:03Z 원격 조회 때 본 세션 가지는 아직 `af3cce37b9f4136c24a56e5ec9d288713a2654d6`였다. 예정된 fast-forward를 완료했다고 쓰지 않는다. 본 세션이 2da71fe5a를 포함하는지 확인한 뒤 반입한다. Codex가 Claude 가지를 이동하지 않는다.
- 미전달 고침 가지 `codex/mixer-squeue-purged-1116`: `dd2c50741f43830ec83b232d0ec51b990d5beaab` → `f1a673fab45b50bedb71a1c8203d9c8ae75f6c97`.
- 이어서 이 가지의 **Record E0 completed return and review rotation dump storage** → **Handoff combined E0 return and squeue correction**. 정확한 SHA·패치는 통합 ZIP의 README_CLAUDE.md에 적는다. 전부 cherry-pick -x; 기존 가지 재작성·merge 없음.
- Claude 반입 ⑥ 대응표 `docs/collab/claude_to_codex/20261116-2050_intake-sha-map.md`로 observations/A1-contact 여섯 커밋은 이미 기준에 포함됨을 확인했다. 이번에 중복 전달하지 않는다.

## 2. 수령과 저장 검토

근거 = `docs/data/mixer_e0_pilot_20261116_return/README.md` §1–4, `docs/data/mixer_e0_pilot_20261116_return/storage_review.md` §1–4. 보고서 SHA64c3de37…, 전체 SHA c9f4fb00… 직접 일치. 전체 정규파일1440 중 런1138/1138, 승인 B283/283, 첫 미완료 report의 원 evidence34/34 대조. 모든 덤프1121의 머리·줄 수·마지막 칸·끝 개행·격자 통과. 고정 관측기 OK, 9개 모듈 seal 일치. C1–C7은 기록 범위 일치이며 자격 수용은 하지 않았다.

감시 네 줄 뒤의 Broken pipe와 나중의 정상 계산 완료를 분리한다. 사후 S5 최대간격20초로 진행 불명은 해소되지만 종료 직후 런타임 영수증은 없다. `runtime_T9` 이름의 실제 수집은 종료 +9362.118초다. 발사 전/회수 시점 신원 일치로 이 공백을 숨기지 않는다. 처분 담당 = 1저자/Claude, 자동 재실행 권고 없음.

24.12985 GiB는 E0 post+restart 합계다. 승인된 회전 덱 일곱 개는 이미 32976 step 간격, N0 두 바퀴 예정234장이다. 17자리 유지, post 약5.384 GB 추정/6.084 GB 산술상한(회전 실측 아님). 원본+압축본 동시공간·restart·로그·여유는 따로다. 간격 축소·정밀도 저하·라이브 압축 전환·E0 원자료 삭제는 수행하지 않았다.

## 3. 고침·확인 수

- native squeue: rc1·빈 stdout·정확한 세 진단 중 하나만 ABSENT. sacct의 동일 job 단일 종료 줄 필요. 다른 진단·혼합 메시지·비어 있지 않은 stdout·다른 rc는 중단. 366423 기존 고정 도구와 TXT는 보존했다.
- 앞 고침 검증 = 같은 새12 메서드 red 실패관측12/오류0 → green12/12; 기존19통과/1건너뜀(Windows symlink 권한). **이번 수령에서 중복 실행 안 함.** 이 수령 가지는 문서·파생 데이터6개만, scripts 변경0.
- 이번 = 원 압축 무결성·기록 대조·고정 관측기 로컬 후처리. 새 엔진·MPI·현장·제출·취소0. 정적 파일 수와 시험 메서드 수를 더하지 않는다.
- 라이브러리 bootstrap의 OS 조회를 차단한 준비 실패 두 번은 결과 검토 실패와 구별해 README §3에 적었다. 후속 관측은 고정 소스 그대로 OK.

## 4. Claude 공유 기록 제안

> E0 pilot366423 개발 자료: COMPLETED0:0, runner0, 03:53:26, NP20,100000입자. 전체 반환 SHA c9f4fb00… 대조 및 덤프1121 완결, 고정 관측 OK. 사후 S5 최대20s로 진행 불명 해소. 종료 즉시 W9 영수증은 부재, 발사 전/지연 회수 신원 일치만 확인. 24.12985GiB; 기존 회전 N0는32976step/234장/17자리 유지 권고. native squeue purged-job rc1 처리 수정은 sacct 완료 확인을 유지. 자격 수용·다음wave·원장 승격은 별도.

앞 쪽지 `docs/collab/codex_to_claude/20261116-1425_mixer-e0-squeue-purge.md`의 새 회귀 gate 추가 제안도 같이 받는다. Codex는 원장·CLAUDE.md·진행기록·check_all.sh를 수정하지 않았다. Rint 고정 가지 끝64e4d213e 및 현장 작업 트리/저장본은 손대지 않았다.
