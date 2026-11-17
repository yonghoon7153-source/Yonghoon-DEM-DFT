# 문서 참조 — Windows 상대 경로 구분자 고침 (2026-11-17)

바탕 = `5a04acd15ee35ef218264c00a59f1b19c8aea2d1`. 가지 = `codex/doc-refs-path-1117`. 1저자가 요청한 문서 검사기 고침만 다룬다. 탈압 30열 판독·연속성 구현은 반입⑧ push 뒤 그 끝에서 시작한다.

## 변경

scripts/check_doc_refs.py의 `walk_docs()`가 반환하는 문서 상대 경로에서 역슬래시를 `/`로 바꾼다. 동작 변경은 이 한 줄이다. 예외표 docs/reviews/doc_refs_sha_exceptions.tsv 및 SHA 도달 기준·문맥 판정·대체참조 검사·정확한 문서/SHA 짝은 그대로다. 면제 항목을 추가하거나 검사를 건너뛰지 않는다.

기존 96관측(고유 문서/SHA77쌍)은 Windows의 역슬래시 문서 식별자가 기존 슬래시 예외 키와 맞지 않아 발생했다. 같은 문서의 미등재 SHA 및 다른 문서의 같은 SHA는 계속 오류다. 자기 검사에서 `relpath`만 Windows/POSIX 꼴로 각각 주입해 실제 `walk_docs → scan_text` 경로를 확인한다.

## 시험 먼저 / 전후 확인

| 확인 | 고치기 전 | 고친 뒤 |
|---|---|---|
| 기존 자기 검사 | Windows/Linux 각각50/50 | 기존50개 유지 |
| 같은 새 자기 검사 포함53개 | Windows/Linux 각각51/53·rc1; 새 두 조건 실패 | Windows/Linux 각각53/53·rc0 |
| Windows 전체 문서 검사 | 없는 경로0·없는 커밋96·rc1 | 없는 경로0·없는 커밋0·rc0 |
| Linux 전체 문서 검사 | rc0 | rc0; stdout/stderr 합친 출력 바이트 동일 |

새 검사는 ① Windows 문서 키·정확 예외, ② POSIX 목록 보존·Windows와 동일, ③ 다른 문서/미등재 SHA 거부다. 세 번째는 고치기 전에도 통과한다. 기존50 + 새3 = 53이며 두 OS 반복을 합산하지 않는다. 시험만 먼저 추가한 파일을 저장하고 rc1을 확인한 뒤 정규화 한 줄을 넣었다.

Windows Python3.12.14, 로컬 WSL/Linux Python3.12.3에서 확인했다. WSL 자기 검사는 독립 임시 Git 저장소만 만들었다. 전체 문서 검사에서는 Windows 작업 트리의 Git 메타 위치를 Linux에서 읽을 수 있게 환경 경로만 지정했으며, 검사기·문서·예외·ref 내용은 바꾸지 않았다. Linux 전후 전체 출력은 같은 문서 집합(이번 인계 문서 추가 전)에 대한 비교다. 전체190단계 게이트는 실행하지 않았다.

근거와 파일 해시는 docs/reviews/doc_refs_path_fix_20261117/verification.json에 있다. 원 전체 검사 로그에는 역사 자료의 외부 경로가 있어 리포에 넣지 않았다. 현장 실행·원자료/연구 값 열람·재봉인·GO 없음. Rint 및 공유 원장/진행 기록/check_all.sh 변경 없음.

## 재현

리포 루트에서 다음을 실행한다. 문서·소형 자기 검사이며 연구 엔진은 호출하지 않는다.

```text
python -I -X utf8 -B scripts/check_doc_refs.py --selftest
python -I -X utf8 -B scripts/check_doc_refs.py
```

인계 ZIP의 `test_only.patch`는 바탕 검사기에 자기 검사3개만 추가한다. 그 상태의 기대는51/53·rc1이다. 완성 커밋의 검사기 기대는53/53·rc0이다. Linux 전후 전체 검사는 같은 문서·원격 ref를 둔 상태에서 비교한다.
