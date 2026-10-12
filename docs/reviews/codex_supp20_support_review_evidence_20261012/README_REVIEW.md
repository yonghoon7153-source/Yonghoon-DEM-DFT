# 보충 20 지원 독립 검토 증거

대상: `b429c3c1df0956d2721861d89cc29a2d56f2b581`  
기준: `3cedd40a5911d0606bf33ed2085d5cb93c4db2e0`  
작성: 2026-10-12

먼저 `codex_review_supp20_support_20261012.md`를 읽는다. 판정은 **보충 지원 전체·214 배포 HOLD**, 새 P2 하나와 P3 하나다. 기존 194의 R7 기술 차단 해제는 유지한다. 이 묶음은 생산 실행 승인이나 실제 보충 20 수치 산출물이 아니다.

## 내용

- `source/`: 고정 핀의 검토·시험 의존 파일 1,016개. 전체 리포나 Git checkout이 아니다. 원 파일은 수정하지 않았다.
- `source_manifest.json`: 각 파일의 Git blob SHA-1, SHA-256, 바이트 수. `tree.json`/`commit.json`은 고정 핀 조회 기록이다.
- `baseline/`: 비교한 이전 버전 파일. 수치 봉인 32개 및 HANDOVER 파일과 변경 대상 스크립트를 포함한다.
- `probes/`: 독립 반례와 설계 재계산. 제품 코드 수정이 아니다.
- `evidence/`: 로그·수치·diff·원천 재검증. 최종 원 파일 무변경 검사는 `final_qa.json`이다.
- `notes/`: 분야별 검토 작업 기록. 최종 판정은 위 본문을 따른다.
- `submitted/`: 사용자가 보낸 요청서.
- `MANIFEST.sha256.json`: 이 전달 묶음의 파일 지문. 자신은 목록에서 제외한다.

## 재현

압축을 짧은 경로에 풀고 이 README가 있는 폴더에서 실행한다. Python, NumPy, SciPy, pandas, Matplotlib가 필요하다. 검토 환경 버전은 `evidence/final_qa.json`에 있다. 기존 로컬 의존 라이브러리 경로가 없는 환경에서는 설치된 패키지를 사용한다.

```text
python run_checks.py snapshot_contract
python run_checks.py runner_probe design_probe release_probe
python run_checks.py builder reread adapter dataset lhsx
python run_checks.py release
python run_checks.py final_qa
```

`run_checks.py`는 결과를 `evidence/`에 갱신한다. 전달된 결과를 먼저 보존한 사본에서 재실행한다. 합성 중간 파일은 `tmp/`에 생성한다. production194 또는 supp20 실제 배치는 실행하지 않는다.

`release_probe.py`는 제출 시험의 합성 입력을 사용한다. build 동안에만 실제 τ 원천 다시 읽기를 대역으로 둔다. 실제 build, 배치별/배치 간 계약, 산출 표/재적합, `check_v13`은 그대로 실행한다. 기존 g1 숫자의 시험용 세대 표지를 실제 g2 수치 증거로 쓰면 안 된다.

## 명시적인 한계

- 배포 시험: 232 PASS / 2 FAIL. Windows 경로 문자열과 Git checkout HEAD 가정 두 실패를 그대로 남겼다.
- Linux 실행기 전체 자체시험: Windows의 `os.wait4` 부재로 완료하지 못했다. 130/130 재현으로 세지 않았다.
- `check_all`, Linux fast16+real4, 실제 194·20 배치는 실행하지 않았다.
- 현재 핀에는 r3 수확·실제 보충 g2 결과가 없다. 최종 raw/TSV 입력 봉인은 후속 확인 대상이다.
- 원천 폴더가 길면 Windows에서 260자 경로 제한을 만날 수 있다. 최종 지문 검사는 확장 경로를 사용한다.

이전 R7 전체 리포와 다운로드 당시 환경은 묶음 밖이다. `prepare_source.py`/`acquire_extra.py`는 획득 기록이며, 동봉 증거 재현에는 실행할 필요 없다. `compare.json`의 GitHub 비교 파일 목록만으로 전체 변경을 판정하지 않았으며 선택된 스크립트는 고정 tree의 blob을 직접 대조했다.
