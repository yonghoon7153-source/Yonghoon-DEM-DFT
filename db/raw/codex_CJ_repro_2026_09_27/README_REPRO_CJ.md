# CJ 재현물 — a2374014b625fcc827d297529a6aba8104db32c2

이 ZIP에는 제품 소스·실제 POTCAR·과학 계산 결과가 없습니다. 해당 커밋 checkout을 `--source`로 지정하세요. 입력/배포 소스는 수정하지 않고, 별도 임시 폴더에서 합성 파일과 PACK_ONLY/가짜 VASP만 사용합니다. 스크립트 옆의 JSON·로그는 리뷰 관측치이며 실행하면 같은 이름 결과 JSON을 덮어쓰므로 보존하려면 별도 복사본 디렉터리에서 실행하세요.

## 기존 CI 회귀 (이번 CJ에서 통과)

```bash
python3 repro_ci.py --source /path/to/checkout --bash /bin/bash --assert-fixed
bash repro_pack_ci.sh /path/to/checkout/db/inputs/wad_aprime_v5_vasp_2026_09_27
```

두 스크립트는 이전 회신의 원문입니다. Python 실행 경로와 재현 디렉터리는 공백 없는 경로를 사용하세요. 결과: `results_ci.json`, 실행 기록 `ci_regression.log`. 이름에 CI가 남아 있어도 대상 manifest가 `85bfebdb...`이면 이번 CJ 실행 결과입니다.

## CJ 추가 포장 경계 (현재 커밋에서 assertion 실패)

```bash
python3 probe_pack_cj.py --source /path/to/checkout --bash /bin/bash --assert-fixed
```

Python 표준 라이브러리와 bash/coreutils/tar만 필요합니다. 과학 계산을 전혀 하지 않고 PACK_ONLY만 실행합니다.

최종 assertion 실패는 `mgmt_echo_error`가 필수 관리 파일을 빼고도 종료 0이 되는 **현재 P1 재현 성공**입니다. `--assert-fixed`를 빼면 모든 관측을 저장하고 종료 0으로 끝납니다. 그 종료 0은 제품 승인 뜻이 아닙니다.

결과: `pack_cj_results.json`, `pack_cj_run.log`.

- 필수 수정 재현: `mgmt_echo_error`, `manifest_echo_error`.
- 선택 권고/지정 잔여위험: `sha_valid_output_then_error`, `sha_nonhex64`, `second_mv_error`, `post_promotion_cleanup_error`.
- 플랫폼 진단: Windows에서만 `windows_bsdtar` 추가. 이번 관측은 CRLF/LF 차이로 fail-closed이며 Linux BSD 전체에 대한 주장으로 쓰지 마세요.

실패 주입은 BASH_ENV 함수입니다. 실제 디스크를 채우거나 권한을 변경하지 않습니다. 대상 소스는 무수정입니다.

## TITEL / None 집계

```bash
python3 probe_semantics_cj.py --source /path/to/checkout
```

결과: `semantic_cj_results.json`. 합성 18잡으로 TITEL 차단·r1 경계, 무엔트로피 None/0.0 처리를 기록합니다. 과학적 수치 검증이 아닙니다.

## 신원·기하 및 native selftest 한계

```bash
python3 audit_metadata.py --source /path/to/cj/checkout --prompt /path/to/CJ_prompt.md --previous /path/to/ci/checkout
```

numpy·ASE가 필요합니다. native selftest에는 추가로 simple-dftd3가 필요하고, 이번에는 그 의존성이 없어 미완료로 기록했습니다. 결과 `metadata_ci.json`의 이름과 `cg_comparison` 키는 이전 도구의 이름이지만, `--previous`에는 **CI 커밋**을 넣어 비교했습니다. 175/175 또는 mutation 11/11 재현 기록이 아닙니다.

이번 Windows 실행의 Bash는 `C:/Program Files/Git/bin/bash.exe`입니다. 최소 shell 스크립트는 coreutils PATH가 없는 환경에서 `bash -l repro_pack_ci.sh ...`로 실행했습니다.
