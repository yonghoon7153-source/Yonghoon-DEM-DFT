# CI 재현물

대상 커밋: `c25e0ce2008b5c33dc6113b249cc8aa22097db2e`.
제품 소스는 ZIP에 넣지 않았습니다. 해당 커밋의 별도 checkout을 지정하세요.
자료는 합성 출력이며 실제 VASP/UMA/QE를 실행하지 않습니다. 소스는 읽기 전용이고 임시 파일은 별도 TemporaryDirectory/mktemp에 만듭니다.

## 종합 시험 (Python 표준 라이브러리 + bash/coreutils/tar)

```bash
python3 repro_ci.py --source /path/to/checkout --bash /bin/bash
```

Windows에서 실제 사용한 bash: `C:/Program Files/Git/bin/bash.exe`.
가짜 VASP 실행 명령을 러너가 단어 분리하므로 Python 실행 파일·재현 스크립트 디렉터리는 공백 없는 경로를 사용하세요.
`results_ci.json`을 스크립트 옆에 씁니다. 기본 종료 0은 **관측 기록 완료**이며 제품 승인 뜻이 아닙니다.

수정 후 다음 명령으로 CI P1 음성시험을 assertion으로 검사할 수 있습니다. 현 대상 커밋에서는 assertion 실패가 정상입니다.

```bash
python3 repro_ci.py --source /path/to/fixed/checkout --bash /bin/bash --assert-fixed
```

## P1 최소 재현 (Python 불필요)

```bash
bash repro_pack_ci.sh /path/to/checkout/db/inputs/wad_aprime_v5_vasp_2026_09_27
```

현 커밋: 내부 러너 종료 0·성공 메시지·관리 파일만 담긴 목록을 출력한 뒤, 재현 스크립트 자체는 기대값 4 불일치로 종료 1입니다.
Windows Git Bash에서 coreutils PATH가 없는 환경은 `bash -l repro_pack_ci.sh ...`로 실행하세요. 이는 테스트 환경 설정이며 제품 소스 수정은 아닙니다.
실패 주입은 `BASH_ENV`의 find 함수 하나뿐입니다. 실제 권한/디스크 장애를 일으키지 않습니다.

## 신원·기하 대조 (numpy + ASE; native selftest는 추가 dftd3 필요)

```bash
python3 audit_metadata.py --source /path/to/ci/checkout --prompt /path/to/CI_prompt.md --previous /path/to/cg/checkout
```

`metadata_ci.json`의 native_selftest는 simple-dftd3 부재로 미완료라고 기록돼 있습니다. 155건 PASS의 독립 재현으로 읽지 마세요.

첨부 JSON은 이번 실행의 관측치입니다. 스크립트를 실행하면 같은 이름 결과 파일을 새로 씁니다. 이전 결과 보존이 필요하면 복사본 디렉터리에서 실행하세요.
