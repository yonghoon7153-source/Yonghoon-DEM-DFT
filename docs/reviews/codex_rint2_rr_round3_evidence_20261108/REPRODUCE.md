# 회차 ③ 독립 증거 재현

판정문: `codex_review_rint2_rr_round3_20261108.md`.
고정 입력: `package/repo/`, pin `17d45fb9cdfc7033bdfd41509527cea23ba1654c`.

연구 계산·실제 호스트 접속을 위한 명령이 아니다. 별도 임시 작업 폴더에서 작은 합성 기록과 소형 배열만 쓴다. 제품·등록·원장은 변경하지 않는다. Git을 사용하는 두 탐침은 증거 폴더 아래 새 합성 Git 저장소만 만든다. 실제 프로세스 죽이기/잠금 경쟁은 모의하며 Linux 현장 자격을 주장하지 않는다.

## 먼저 바이트 확인

ZIP을 푼 폴더에서:

```bash
python3 -I -B verify_evidence.py
```

이후 탐침을 다시 실행하면 결과 파일·시간·임시 경로가 바뀌므로 최초 배포 증거 해시와 달라질 수 있다. 원 배포 폴더를 보존하고 **별도 사본**에서 재현한다.

## 새 반례와 현재 소비자

Python 3.12 + NumPy/SciPy + Git을 사용한 검토 하네스다. 이 하네스 실행은 제품 Python 3.8 현장 자격을 대신하지 않는다. 명령은 ZIP을 푼 최상위에서 실행한다.

```bash
python3 -I -B -X utf8 pc12_attack/probe_pc12_independent.py
python3 -I -B -X utf8 contracts_probe.py
python3 -I -B -X utf8 contracts_p2p4_git.py
```

첫 명령은 새 RR3-01이 여전히 존재함을 **assert**하므로 이 핀에서는 rc 0이 ‘반례 재현 성공’이다. 단순한 제품 합격 selftest로 읽지 않는다. 생성 `pc12_attack/results.json`에서 원 실패/편집 뒤 `resume_ok`, `attempt_order_problem`, 실제 `_copy` 재거부를 대조한다. 모의는 `run_in_group`의 반환·산출에 한정되며 실제 생산·판독·결과 줄·자격 함수는 고정 소스를 사용한다.

사용자 트리를 직접 보려면 위 세 명령 및 아래 옛 탐침에 `RINT_REVIEW_REPO`를 지정할 수 있다:

```bash
export RINT_REVIEW_REPO=/absolute/path/to/fixed/repo
python3 -I -B -X utf8 /absolute/path/to/review/pc12_attack/probe_pc12_independent.py
```

PowerShell에서는 `$env:RINT_REVIEW_REPO='C:/absolute/path/to/repo'`를 사용한다. 실행 결과에 실제 소스 SHA가 기록된다. 수정 후에는 같은 공격 입력의 **거부**를 새 oracle로 명시해야 하며, 현 반례 존재 assert를 조용히 PASS로 바꾸지 않는다.

## 옛 반례·기대 변경

```bash
python3 -I -B -X utf8 run_old_probe.py
```

원 회차② 탐침의 기대를 그대로 유지했으므로 **rc 1·301/309**가 이 핀의 기록이다. 요청서의 8개 기대 변경과 일치한다. 역사 `report_c_raw` 93파일의 존재/해시 검사 2개는 이번 패키지에 없어 미실행으로 명시했다. 두 검사를 새 PASS로 세지 않았다. Windows 경로/O_NONBLOCK만 조정했고, 기존 Linux 신원 mock·순차 lock 대체는 그대로 공개했다.

원 preattack12 p1/p5/p6의 입력 재생 로그는 `preattack12_replay/`다. p5 원본은 새 strict reader가 None을 돌려주어 출력문에서 TypeError가 나는 것을 보존했다. None-safe 출력만 적용한 추가 로그로 후속 c1–c4를 확인했다. p2/p4의 전체 작성 측 fixture는 Windows symlink 권한으로 중단했으며 위 `contracts_p2p4_git.py`가 동일 핵심 입력을 **최소 실제 Git 경로**에 연결한 별도 12개 재현이다. `replay_preattack12.py` 전체 fixture 실패를 제품 실패나 통과로 세지 않는다.

## S0 소형 후보·순서·계획 결속

```bash
python3 -I -B -X utf8 s0_memory/probe_s0_memory.py package/repo s0_memory/independent_results.json
python3 -I -B -X utf8 s0_memory/probe_plan_binding.py package/repo s0_memory/plan_binding.json
python3 -I -B -X utf8 s0_memory/run_targeted_memory.py package/repo remote_old_carbon_3b12fbe2d.py remote_old_census_39104710a.py
```

옛 모듈은 고정 원격 원문의 사본이다. SHA-256:

- carbon: `5460dad164839b115eea07f5df21087af1ff214c221e4838d940f7de9f9ca221`.
- census: `6e527e6c7a16251c585443abb922325170975f63d953204d209065c2dc951937`.

최초 전달 사본은 끝 빈 줄 하나가 더 있었고 초기 실행 해시는 그 상태를 보존한다. 함수 변화는 없었다. 현재 배포 사본은 고정 원문 바이트다. 최초 임시 디렉터리 권한 실패도 보존했으며 리뷰 전용 tmp에서 최종 선택 시험 55/55·19/19를 확인했다. 실제 S0 CLI·침대·kgy/ibb/WSL을 실행한 기록이 아니다.

## 증거 위치와 판정 경계

- `integrity.json`, `remote_blob_check.json`, `remote_dependency_diff.json`: 포장·원격 pin 대조.
- `pc12_attack/`: 새 P2와 PC11/12 새 공격.
- `contracts_probe*`, `contracts_review.md`: RR2/PC9/PC10 독립 함수·문서 대조.
- `contracts_p2p4_git_evidence/`: 원 PC12 입력의 실제 Git 재현(순차/프로세스 모의).
- `round2_replay/`: 원 runtime 재생 및 rc 반례의 실제 Git 결과.
- `s0_memory/`: SELF-155의 합성 범위 및 채택 조건.
- `review_result.json`: 기계 판독 요약. 원 저장소 finding 상태를 수정하지 않는 외부 판정 기록.

전체 공유 게이트·실제 현장·통합·봉인·R 캠페인은 실행하지 않았다. **HOLD**를 유지한다.
