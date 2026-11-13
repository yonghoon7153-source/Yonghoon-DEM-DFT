# 내부 사전 공격 — 외부 판정 아님

CLAUDE.md의 사전 공격 ③에 따라 별도 에이전트에게 source.diff와 관련 소스·시험만 제공했다. 작성 측 요청서·설명·문서는 읽지 않았다. 리포 파일 수정 없음. 결과는 원 외부 반박 판정과 구분한다.

## 1. 관측

| 검사 | 상태 | 해석 |
|---|---|---|
| 제공 회귀 | 1: 10/10 | 작성 측 시험의 반복이지 새 고유 시험10개가 아님 |
| 별도 작은 탐침 | 1: 7/7 | 원 source audit+builder 실패, 목적지 디렉터리·dangling symlink, 목적지 audit 없음, source 디렉터리, 옮긴 뒤 실패 보고, 기존 불완전 팔 제거 관찰 |
| 변이8개 | 1: 제공 회귀6개 검출 + 별도 탐침2개 검출 | 삭제·순서/오류 처리·store-off·고유 보존·symlink·source writer 퇴역 경계 |
| 현재 후보의 새 차단 결함 | 0: 관측하지 못함 | 단일 작성자·새 팔 자격 전제 안에서만 |

6개 중 store-off 가드를 지운 변이는 보존 파일을 읽는 assertion 자리의 FileNotFoundError로 검출됐다. 나머지5개는 assertion 실패다. 살아남은2개는 dangling-symlink 가드 제거와 변경하지 않은 source writer 퇴역 제거이며 별도 탐침에서 각각1실패로 잡혔다. 전부 제공10개만으로 잡혔다고 적지 않는다.

## 2. 시험의 한정

제공 builder 실패 시험은 source에 옛 audit이 없는 fixture다. 옛 source audit까지 둔 실패는 별도 탐침이 검사한다. dangling symlink 보존도 별도 탐침으로 확인했다. Windows Git Bash와 실제 Windows symlink에서 관찰했으며 Linux/Lustre 자격이 아니다.

기존 불완전 캐시 검사 조각은 옛 OUT을 먼저 지운다. 그 뒤 퇴역 실패 때 전체 러너가 불완전한 옛 팔까지 보존한다는 주장은 금지한다. 이번 보장은 새 팔 게시 중단과 audit 기록 보존/누락 처리다. 해당 한정을 README §2에 명시했다.

consumer는 audit 자기 기록을 요약하며 과학 팔 hash와 결속하지 않는다. 이 수정은 원 최종 폴더 잔존 경로를 막을 뿐 감사 기록의 진위 증명을 추가하지 않는다. audit 누락이 전체 HOLD를 자동 발동한다고 검증하지 않았다. 전체 러너·판정기·신호·현장·연구·GPU 실행은 하지 않았다.

## 3. 증거

evidence/internal_attack_results.json은 원 결과 JSON의 줄바꿈을 LF로 정규화한 사본이다. 원 보고·탐침·변이·로그는 전달 ZIP의 private_evidence/internal_attack/에 보존한다. 실행 경로가 있는 원 로그/스크립트는 공개 리포에 반입하지 않는다. source.diff와 최종 소스·시험 해시는 preservation.json과 evidence/green_summary.json에서 대조한다.
