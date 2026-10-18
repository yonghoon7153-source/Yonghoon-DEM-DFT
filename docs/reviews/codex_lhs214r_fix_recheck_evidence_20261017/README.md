# LHS214 수정 재확인 전달 묶음 — 2026-10-17

먼저 `codex_review_lhs214r_fix_recheck_20261017.md`를 읽으세요. 판정 **HOLD**, 새 P2 1건/P3 2건입니다. 원 L214R-01–11 반례는 닫혔고 WEB-09 전체 Δ 규약은 부분입니다.

## 대상·구성

- 코드 `60ba39e224aff48a030dccfe750342f3bf9db61f`, 기준 `6cb2569569ec74b7f5a96e0ef19494e872da5272`.
- `submitted/`: 받은 요청서. 요청서/새 증거를 담았다는 후속 커밋은 미확인. 코드 핀을 최신으로 바꾸지 않음.
- `source/`, `base/`: 실행에 필요한 고정 원격 파일 스냅샷. 전체 Git checkout이 아님. 원 Git blob/SHA256/크기 명세 동봉.
- `probes/`: 독립 탐침, 이전 탐침의 원 바이트 `.b64`, 명시적 파생 실행기.
- `evidence/`: JSON·로그·최종 HTML·합성 게시/인계/배포 fixture·원격 트리와 커밋 조회 기록.
- `notes/`: 수치·소비자·화면별 상세 검토 기록. 최종 판정과 ID는 주 보고서 기준.
- `tmp/`: 작은 합성 보조 배치와 수치 변이 사본. 생산 자료 아님. 일부 증거의 원 실행 절대경로를 보존하기 위해 포함.
- `PACKAGE_MANIFEST.json`: 전달 파일 SHA256/크기. ZIP 자체 SHA는 ZIP 옆 전달 영수증에 있음.

원 코드/기준 파일 무결성 검사는 `integrity.json`을 참고하세요. 패키지 해시는 전송 동일성을 보장하며, 과학적·판정 의미의 무오류를 보장하지 않습니다.

## 재현 범위와 환경

실행 환경은 Windows, 제공 Python 런타임과 NumPy/SciPy/Flask 등 기존 라이브러리입니다. 의존성 루트 두 곳은 `../lhs_coverage_review_20260930/deps`, `../gen2_network_reverify3_20261007/deps`이며 **라이브러리는 ZIP에 포함하지 않습니다**. 다른 기계에서는 동등한 라이브러리를 Python 환경에 설치하고 경로를 환경에 맞게 공급해야 합니다. source/base를 고쳐 의존성을 해결하지 마세요.

원 실행 Python:

```powershell
$py = 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$r = 'C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs214r_fix_recheck_20261017'
```

아래 실행은 증거 파일을 새로 쓰므로 **보존용 ZIP을 먼저 유지하고 복제된 검토 폴더에서** 실행하세요. 모두 작은 진단용 사례이며 새 214 배치·DEM 시뮬레이션·실제 배포를 실행하지 않습니다.

### 새 P2: 원 생산자 → 변이 → 소비 경로

```powershell
& $py -X utf8 -B "$r/probes/consumer_chain_derivative.py"
& $py -X utf8 -B "$r/probes/consumer_h0_resurrection.py"
& $py -X utf8 -B "$r/probes/numeric_adversarial.py"
```

선택 1행만 실제 원천 재독을 수행하며 나머지 213행은 합성 배포 fixture입니다. 게시 승격 전체 함수 재실행이 아니라 게시 판정 함수·정지 계약·실제 인계/build/check를 실행합니다. 자세한 변이와 어댑터 범위는 보고서 §1 및 `notes/consumers.md`에 있습니다.

### 새 P3: 화면·영수증

```powershell
& $py -X utf8 -B "$r/probes/display_run_command.py" fresh probes/display_fresh.py source
& $py -X utf8 -B "$r/probes/receipt_fences.py"
```

### 정상 대조·기존 반례·제출 시험

```powershell
& $py -X utf8 -B "$r/probes/normal_impact.py"
& $py -X utf8 -B "$r/probes/numeric_runner.py" --tests
& $py -X utf8 -B "$r/probes/numeric_runner.py"
& $py -X utf8 -B "$r/probes/consumer_chain_derivative.py" --negative
& $py -X utf8 -B "$r/probes/consumer_chain_derivative.py" --release
& $py -X utf8 -B "$r/probes/consumer_submitted_checks.py"
& $py -X utf8 -B "$r/probes/consumer_adversarial.py"
& $py -X utf8 -B "$r/probes/root_checks.py"
```

화면 원 68사례·기준/수정 비교의 정확한 실행은 `notes/display.md`에 있습니다. 원 탐침을 바이트 그대로 저장했지만 실행은 경로·핀 또는 고쳐진 기대를 명시적으로 바꾼 파생 실행입니다. “전체 탐침 무변경 재실행”이라고 일반화하지 마세요. `.b64` fallback은 이전 검토 폴더가 없어도 원 탐침 바이트를 공급합니다.

`normal_impact.py`는 확보하지 못한 작성자의 10-16 A4 대신, 확보한 10-15 fixture로 독립 대조를 구성했습니다. 최초 실행기의 helper 이름/새 bool 기대 오류를 고친 뒤 최종 36/36을 얻었습니다. 그 초기 탐침 오류를 제품 결함으로 세지 않았습니다. N 비교의 출력 설명에 이전 “키 넷 제외” 문자열이 남지만 실제 `L214_ADDED=()`이며 제외 수는 0입니다.

현 활성 등록과 실제 지문 불일치로 D1이 실패하는 것은 예상 결과입니다. 코드 판정, 등록 승인, 재봉인, 실제 발사는 별개이며 이 ZIP은 실행 승인이 아닙니다.
