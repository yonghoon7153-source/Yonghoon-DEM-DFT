# gate94_evidence — G93-N1 수정 · 검증 원 로그 (2026-10-07)

모든 로그는 스크래치패드 원본의 바이트 사본 (`cp -p`). 이름만 내용을 알리도록 바꿨다. `*.log` 은 gitignore 대상이라 `git add -f` 로 넣었고, 요청 커밋 tree 에 있는지 `git ls-tree` 로 확인한다 (93차 G93-N2 재발 방지).

| 크기 (B) | sha256 | 파일 |
|---:|---|---|
| 6228 | `b0eca85bdd6c359ee407848e995bbebfac0265bb4a63b41d134d5b7b2d3002b2` | `00_red_test_g93_1failed_keyerror_io1686.log` |
| 921 | `b71250c704728b27fa46b14ae2c7a0ff520a3c89632f98bd0cba7c789cb89993` | `01_green_204passed.log` |
| 312 | `8899a63b17011500db1c242a00b9f5f76e574f9fc49770a9e559c1a9bbdeeb3b` | `02_green_after_helper_reuse_204passed.log` |
| 944 | `7c390b9ce13ac232bda49cca186849b429144c8f94f12d39e1a74ad1d5491221` | `03_replay_g93_emit_expect.log` |
| 389 | `3ddc3e867be9623ad54a9614cb2dbfda8302e55f3cac42e812cd24767834b82e` | `04a_replay_g93_rc0.log` |
| 424 | `ab722ad5ee6b757dac999df1b554e0e2c6384806873c31b0f20b20846c54ee52` | `04b_replay_g92_k04_env_updated_rc0.log` |
| 353 | `02d706e9c80c3243d3924c7288575567dfc2080534163f577c71d089928937fb` | `06_make_receipt_27b0917e2_rc0.log` |
| 5792 | `965fd26cf3b811aa7731e57edaba61358a9fe338ba41b0468bd816d0d4470c0f` | `08_env_profile_168fd41a5.log` |
| 6130 | `59c4dfc1a041a754f97230642944bd2e18cdad536d0f9d0b58b78f980d98d998` | `10a_full_pytest_168fd41a5_1failed_wiki_raw_sha.log` |
| 3744 | `88543351ad5ed7ba158418c366a62bd0851d667ad2e5557c4580c9eb4022698f` | `10b_full_pytest_fe72f9b81_2323passed.log` |
| 10291 | `aac953766897d24fbb223facb3da0e18fc85b01da644b3c2ef9e8d07d2607bdc` | `11_smoke_168fd41a5_rc0.log` |
| 54748 | `47ff73249133948889bb6712b713f1c750a42c9897d0db2eee247b983495a2fa` | `12_full_replay_168fd41a5_422_of_422_rc0.log` |
| 201 | `c65b86a141abb6ed849fbbd514bd746d6395a1abf12f3fec16f8320c56886144` | `aborted/README.txt` |
| 5792 | `601369f793388f734081747a46062358ea637b352b25efda05cfee2a504a15bc` | `aborted/run1_08_env_profile_49c769cb5.log` |
| 1555 | `a7b768afff710c350290969b4bbe99ca72f2745f7761e4fd3332822662c22bfc` | `aborted/run1_10_pytest_49c769cb5_container_restart.log` |

- 00 RED (수정 전 · `3a7d68069` + 새 시험) · 01 · 02 GREEN (stage3 모듈 4 + 새 시험 · 204) · 03 · 04 변이 · 06 영수증 (clean `27b0917e2`).
- 08 · 11 · 12: clean `168fd41a5` 순차 (시작 = 끝 HEAD · dirty 0). 10a: 같은 HEAD 의 전체 pytest — 1 failed (`test_wiki_tools_survive_a_cp949_console[lint.py]` · 위키 raw 2026-10-07 브리핑의 sha256 선언 오류).
- 10b: 위키 정정 `fe72f9b81` 의 전체 pytest — 2323 passed · 1 xfailed · rc 0 (시작 = 끝 HEAD · dirty 0). `168fd41a5` ↔ `fe72f9b81` 차이는 위키 raw 파일 하나 (smoke · 재생은 위키를 읽지 않는다).
- aborted/run1: 1 차 검증 (`49c769cb5`) 이 pytest 34 % 에서 컨테이너 재시작으로 끊김 · rc 줄 없음. 보존 중 원 로그 끝에 메모를 한 번 덧붙였다가 원래 크기 1,555 B 로 잘라 되돌렸다 (메모는 aborted/README.txt).
