# LHS214 FULL 모형 한계 재검증 증거 묶음

먼저 `codex_review_lhs214_fix_reverify_20261015.md`를 읽는다. 검토 핀 `9e3ef54ca228111360bfe5f6d9dad4ebe26d54af`, 기준 `0c557e72aaffdf6cfd033c0667c643de4501c5b1`. 결론 HOLD. 생산 코드·등록·원장·Git 수정 및 새 214 발사는 없다.

## 구성

- `source/`, `base/`: GitHub의 고정 커밋 파일 사본. 완전한 Git 저장소가 아니다. 수집한 파일의 SHA256·Git blob·크기는 각각 `source_manifest.json`, `base_manifest.json`에 있다. 기준 사본은 필요한 scripts/webapp 및 지정 자료 중심이다.
- `probes/`: 독립 반례, 기존 A4 실행 어댑터, 대기 지문 시험.
- `evidence/`: 실제 출력·로그·선정 HTML·합성 생산자 파일과 빌드 출력.
- `notes/`: 수치·소비자·화면·A4의 상세 설명.
- `package_manifest.json`: 압축에 포함한 각 파일의 SHA256·크기. `integrity.json`: 고정 원문 사본의 최종 무변경 대조.

`consumers_release_verified`의 출력은 **시험 전용**이다. 선택행은 실제 작은 생산자→게시→P0–P4 인계에서 얻었지만, 나머지 행·감사·배치 기록은 합성이다. 실제 214 데이터의 공개·학습용 배포가 아니다. 화면 CSV의 0.6/0.9 등은 stale 값 재등장 여부를 겨냥한 의도적 변이다. 증서의 1e308 역시 유한성 검사용 변이이며 실침대 관측값이 아니다.

## 재현

NumPy·SciPy·Flask 및 리포 의존성이 설치된 Python으로 묶음 루트에서 실행한다. 원 검토에서는 Windows와 제공된 Python을 썼으며, 기존 두 의존성 폴더를 sys.path에 추가했다. 탐침의 의존성 경로가 없는 환경에서는 자체 Python에 해당 라이브러리가 있어야 한다. OMP/OPENBLAS/MKL 스레드는 1이며 검토 전용 임시 폴더만 쓴다. `tmp`가 없으면 빈 폴더로 만든다.

```text
python -X utf8 -B probes/l214_numeric.py
python -X utf8 -B probes/l214_numeric.py --selftests
python -X utf8 -B probes/l214_consumers.py
python -X utf8 -B probes/l214_consumers.py --negative
python -X utf8 -B probes/l214_consumers.py --release
python -X utf8 -B probes/l214_display.py --tree source --producers
python -X utf8 -B probes/l214_display.py --tree base
python -X utf8 -B probes/l214_a4.py
python -X utf8 -B probes/receipt_identity.py
```

수치·소비자·화면 탐침은 실제 리포 함수를 부른다. A4는 제출 스크립트의 section N/T/R/W와 비교식을 그대로 쓰고 Git의 show/diff/archive 읽기만 해시 검증된 사본 공급으로 대체한다. 자료 9개도 실행 전 해시·크기 대조한다. archive 대체는 수집된 필요한 scripts/webapp 파일을 공급하며 전체 저장소 복제라고 주장하지 않는다. 현재 핀과 기준의 scripts/webapp 차이 23개는 고정 Git tree 비교와 일치했다.

영수증 selftest는 격리 자식 Python의 `GEN_PROBE`에 **설치된 외부 의존성 경로만** 공급했다. 판정식·기대 실패 집합·등록 값·수치식은 바꾸지 않았다. 비준 전환 반례는 원 등록 문서가 아닌 임시 사본에서만 수행한다.

`--release`는 실제 build/check 함수를 쓰지만 원천 공급 어댑터와 합성 나머지 행을 사용한다. `notes/consumers.md`의 한정을 유지해야 한다. 어댑터를 실제 생산 감사나 전수 결과 검증으로 인용하면 안 된다.

## 최종 실행 결과

| 실행 | 결과 | 근거 |
|---|---|---|
| 독립 A4 | 32/32, 생산자 예외 0 | `evidence/a4_independent.json` |
| L214 모형 한계 selftest | 55/55 | `numeric_selftest_model_limit.log` |
| 네트워크 selftest·상태 | rc 0, 상태 31/31 | `numeric_selftest_network.log` |
| τ / 세대 계약 / 인계 체인 | 55/55 · 44/44 · 34/34 | `consumers_baseline.json` |
| provenance | 284/284 | `baseline_provenance.log` |
| v1.2 다시 읽기 | 22/22 | `baseline_reread_v12_complete.log` |
| g2 다시 읽기 | 29/29 | `baseline_reread_final.log` |
| v1.3 배포 회귀 | 254/256 | `baseline_release_final.log` |
| 대기 지문 영수증 | 99/99 | `receipt_identity/selftest_dependency_only.log` |

배포 회귀의 V10a는 Windows 경로 구분자 기대 차이, V16a는 Git 없는 고정 파일 사본의 HEAD 조회 실패다. 수치·봉인·인계 해시 불일치로 세지 않았고, PASS로 고쳐 쓰지도 않았다. `baseline_consumers_final_summary.json`에 세부 근거가 있다.

초기 `baseline_*`, `_full_inputs`, `_complete` 로그의 누락 자료·임시폴더·격리 Python 의존성 실패도 보존했다. 최종 결과는 위 표와 `_final` 로그를 따른다. 이 표는 전체 check_all·실제 WSL 발사 점검 통과를 뜻하지 않는다.

패키지에서 재생성 가능한 scratch(`tmp`, `display_work`, `consumers_temp` 등)는 제외했다. 재현 시 새 임시 출력이 만들어진다. 고정 source/base의 원문은 편집하지 않는다.
