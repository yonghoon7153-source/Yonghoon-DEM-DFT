- ⚠ **계산 입력은 v41 과 동일합니다** — 잡 목록 19개(1단계 12 · 2단계 7)·INCAR·POSCAR·KPOINTS·POTCAR 규격·
  사전등록이 그대로이고, 잡 집합 지문(job_keys sha16 `8a7ae28f`)이 v41 과 같습니다. 19잡 폴더의 입력 파일은
  v41 zip 과 **바이트 단위로 동일**합니다 (저희가 대조했습니다 — 회신해 주신 7잡의 `job.json`·`POSCAR`·`static/INCAR`·
  `static/KPOINTS`·`run_job.sh`·`POTCAR_ASSEMBLE.sh` 도 v42 와 바이트 동일). 물리적으로 같은 계산입니다.
- **바뀐 것은 러너·문서뿐입니다** — `run_staged.sh` · `README_REQUEST.md` · `SUBMIT_CONTRACT.md` ·
  `MANIFEST.json`(스크립트 해시·반송 목록) · `governance/decisions.json`(저희 결정 원장 사본 — C-12 항목은 v41 과 같습니다).
  ① **완주한 잡의 거부를 실패와 가릅니다.** v41 러너는 같은 extraction 에서 1단계를 다시 부르면 완주 잡의
     "이미 산출물이 있습니다" 거부를 실패로 집계해 2물결(`refs/mol__*__box24__nzmag` 2잡)이 **구조적으로**
     열리지 않았습니다 — 09-21 회신에 적어 주신 그대로이고, 저희 결함입니다.
  ② `SKIP_COMPLETE=1` — **완주가 증명된** 잡(모든 상 `General timing` · receipt 의 `_runner_start` 정확히 1개)만
     건너뜁니다. "산출물이 있다" 는 자격이 아니라서 qdel 잔재(0스텝 찌꺼기)는 건너뛰지 않고 실패로 셉니다.
  ③ `CONTINUE_FROM=<v41 extraction 루트>` — **완주하신 7잡(≈97 h)을 다시 돌리지 않습니다.** 새 extraction 에서
     러너가 봉인·census·실행파일 대조를 끝낸 **뒤에** v41 완주 잡의 산출물(receipt·`static/` 산출물)을 옮겨 옵니다.
     옮기기 전에 잡마다 입력 바이트 동일 · 같은 PP 트리 · 같은 VASP/launcher · 같은 조립본 해시 · 실제로 돈 기하 동일을
     확인하고, 하나라도 어긋나면 **아무것도 옮기지 않고** 멈춥니다. 기록 `CONTINUATION.json` 이 반송 목록에 추가됐습니다.
  ④ 왜 손으로 옮기면 안 되는가 (둘 다 코드로 확인했습니다): v41 extraction 에 v42 스크립트를 덮으면 census 가
     `files_sha256` 불일치로 거부하고(봉인이 MANIFEST·ZIP 해시에 묶여 있고 봉인은 바꾸지 않습니다), 새 extraction 에
     완주 폴더를 **먼저** 복사하면 봉인 스크립트가 "생산 산출물이 이미 있습니다" 로 최초 봉인을 거부합니다.
- **하실 일 (요약 — 메일 §1′ 블록이 정본입니다)**: v42 zip 을 **새 빈 디렉터리**에 풀고, §1′ 블록에서
  `CONTINUE_FROM=/home/kgy/projects/sdcp_c12_v41_2026_09_11/sdcp_c12_v41` (v41 을 푸신 묶음 루트 — 다르면 고쳐 주십시오) 를
  확인한 뒤 `bash run_staged.sh 1`. 기대 출력: `✓ 승계 <잡>` 7줄 · `[_wave1.txt] … 건너뜀 7 · 실패 0` · `vacconv/*` 3잡 실행 ·
  `[_wave2.txt] 잡 2` 에서 `nzmag` 2잡 실행(`canary 기하 = 부모(…) 와 동일`) · `✅ 1단계 통과 — STAGE1_PASS.json`.
  그 다음 `bash run_staged.sh 2` (7잡). v41 extraction 은 **지우지 말고 그대로** 두십시오 (승계 기록이 그 경로·MANIFEST·봉인 해시를 가리킵니다).
  v41 의 `vacconv/clean_slab__afm2424_pm1__c2` 잔재(`vasp.out` 만)는 승계 대상이 아니며 v42 에서 새로 실행됩니다 (러너가 `승계 안 함 … OUTCAR 가 없다` 로 찍습니다).
- **저희 쪽 검증**: 회신해 주신 7잡 실물 폴더를 픽스처로, 실제 `run_staged.sh 1` 을 (stub VASP 로) 끝까지 돌렸습니다 —
  7잡 승계·건너뜀 · vacconv 3 + nzmag 2 실행 · nzmag 가 승계된 부모 기하로 실행 · receipt 불변 · `✅ 1단계 통과` · 이어서
  `run_staged.sh 2` 까지. 승계 자격 검사는 음성 경로 15건(입력 불일치·다른 PP·다른 VASP·찌꺼기·receipt 중복·경로 오류 등)을 selftest 로 겁니다.
- 09-21 회신의 실행 조건(`64core.q` 노드 1개 · `VASP_NPROC=64` · `VASP_NODES=1` · `NODE_MEM_GB=500` · `JOBS_PARALLEL=1`)은
  그대로 쓰시면 됩니다 — 러너 사전검사가 그 조건으로 통과했었고 v42 는 그 검사를 바꾸지 않았습니다. README·메일 §0 의
  "시작 전 확인" 다섯 가지는 이미 답을 주셨으므로 다시 답하실 필요 없습니다.
- 그 밖의 실행 절차·반송 목록·게이트·walltime 계약은 **v41 과 동일**합니다.
