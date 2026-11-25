# CK 재현 묶음

대상 커밋 `f4441c426701bc35690541737d4664a37da4db36`.
제품 소스·POTCAR 본문·실제 계산 실행물은 이 ZIP에 포함하지 않아요.

Python 표준 라이브러리 + Bash/GNU 도구로 핵심 시험을 실행할 수 있어요.
`CHECKOUT`은 대상 커밋의 파일이 있는 저장소 루트예요. 테스트 스크립트들은 같은 폴더에 두세요.

```bash
python3 probe_pack_cj.py --source CHECKOUT --bash /bin/bash --assert-fixed
python3 repro_ci.py --source CHECKOUT --bash /bin/bash --assert-fixed
python3 probe_pack_ck.py --source CHECKOUT --bash /bin/bash
python3 probe_semantics_cj.py --source CHECKOUT --bash /bin/bash
```

- CI/CJ 원본 스크립트는 그대로예요. 결과 JSON은 스크립트 옆에 쓰므로 보존본을 덮지 않으려면 이 묶음의 작업용 복사본에서 실행하세요.
- CK 추가 스크립트는 CJ 드라이버 AST의 오류 주입 표와 결과 파일명만 바꿔 사용해요. 제품 소스는 변경하지 않아요. 추가 차단 사례 16개에 단언이 있고, 성공하는 find가 stdout.log를 누락시키는 1건은 신뢰 경계 진단이지 필수 차단 사례가 아니에요.
- 테스트용 임시 디렉터리에서만 파일을 만들고 정리해요. `PACK_ONLY` 및 텍스트 생성 가짜 VASP만 실행하며, 실제 VASP/QE/UMA는 실행하지 않아요.
- 메타데이터·기하 확인은 별도로 numpy/ASE가 필요해요:

```bash
python3 audit_metadata.py --source CHECKOUT --prompt CK_PROMPT.md --previous CJ_CHECKOUT
python3 check_results_ck.py
```

`check_results_ck.py`는 저장된 결과 파일의 핵심 판정을 다시 단언해요. native selftest 194개나 작성자 돌연변이 12개 완주를 뜻하지 않아요. 이번 환경에서 native selftest는 simple-dftd3 부재로 중단됐어요.

`metadata_ci.json`의 `cg_comparison`은 재사용된 이름이며, 이번 실행의 실제 비교 대상은 CJ 커밋 `a2374014b625fcc827d297529a6aba8104db32c2`예요.
