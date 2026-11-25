# SELF_REVIEW v42 — "mirae 가 이 번들로 또 헛돌 수 있는 자리" (적대적 자체 리뷰 · 2026-09-21)

전제 사실 (코드로 확인): v41 extraction 에서 7잡 완주 · 12잡 미실행. 이어가기 후보 둘은 **둘 다 그대로는 안 된다.**
- (B) v41 extraction 에 v42 스크립트 덮어쓰기 → `census.py`: `배포 파일이 바뀌었다 3건 [README·SUBMIT·run_staged.sh]` (rc 1);
  MANIFEST 까지 덮으면 `봉인이 다른 MANIFEST 에 대한 것이다 (fd5e… ≠ …)` (rc 1). 봉인은 바꾸지 않는다 — 구조적으로 막힘.
- (A 문자 그대로) 새 extraction 에 완주 폴더 먼저 복사 → `SEAL_POTCAR_ROOT.sh`: `생산 산출물이 이미 있습니다: ./refs/mol__ptfe_c10__box24/static/OSZICAR` (rc 1, 봉인 안 만듦).
- ⇒ 확정 절차 = **A″**: 새 extraction + `SKIP_COMPLETE=1 CONTINUE_FROM=<v41 루트> bash run_staged.sh 1`. 러너가 봉인·census·실행파일 대조 **뒤에**
  완주 잡을 옮겨 오고(자격 검사 fail-closed), 물결에서 건너뛴다. 근거 e2e: 회수본 7잡 실물 폴더 + 실제 `run_staged.sh 1`·`2` 전체 경로 (stub VASP)
  → `✓ 승계 7 · 건너뜀 7 · vacconv 3 + nzmag 2 실행 · ✅ 1단계 통과 · 2단계 7잡 완주 (rc 3 = 탐색용 정책의 정상 종료코드)`.
  증거: `runs/sdcp_c12_2026_08_30/e2e_v42_evidence/` (E1_run_stage1.log · E1_run_stage2.log · E1_CONTINUATION.json · E1_STAGE1_PASS.json · 드라이버 2개).

| # | 헛돌 수 있는 자리 | 막았나 | 근거 (시험·코드) |
|---|---|---|---|
| 1 | v41 처럼 완주 잡의 거부가 실패로 집계돼 2물결이 안 열림 | ✅ | 커밋 8046d4dde 의 표지(ok/skip/fail) + e2e 14건. v42 번들 `run_staged.sh` 에 `_wave_status`·`SKIP_COMPLETE` 실재 확인 (파일 grep 12건) |
| 2 | 완주 폴더를 손으로 새 extraction 에 복사 → SEAL 거부 | ✅ 문서·코드 | 위 (A) 실측. README·SUBMIT·메일 §1′ 이 "손으로 옮기지 마십시오" 를 세 번 말한다 |
| 3 | 옛 extraction 에 새 스크립트 덮어쓰기 → census 거부 | ✅ 문서·코드 | 위 (B) 실측. 같은 문구 |
| 4 | 승계 자격 미달인데 옮겨서 판정에서 90 h 뒤 막힘 (다른 PP·다른 VASP/launcher·입력 불일치·조립본 불일치·기하 불일치) | ✅ | 승계 블록 ③④ 검사 · selftest 음성 15건(입력 POSCAR 변조·PP SHA·VASP SHA·planned·조립본·static/POSCAR·기존 산출물 충돌·gz 중복·완주 0·상대경로·없는 경로·자기 자신·봉인 없음·SKIP_COMPLETE 없이) 전부 "아무 파일도 안 옮김" 확인. **일부러 깨기**: 입력 동일성 die 를 끄니 그 음성 1건만 빨강 (rc 1) → 복원(sha 동일) |
| 5 | qdel 잔재(v41 `vacconv/clean_slab__afm2424_pm1__c2`: vasp.out + receipt 2행)를 완주로 오인 | ✅ | 승계는 `static/OUTCAR 가 없다` 로 미승계 → 새로 실행 (실물 픽스처 e2e 가 그 잔재를 그대로 재현해 통과) |
| 6 | nzmag 2잡의 PARENT_GEOM 이 승계된(건너뛴) 부모의 기하를 못 집음 | ✅ | run_job.sh 는 단일점이면 **부모 루트 POSCAR** 를 쓴다(relax 없음). 실물 e2e 에서 실제 run_job.sh 가 `canary 기하 = 부모(../mol__*__box24) 와 동일` 을 두 번 찍고, canary static/POSCAR == 부모 POSCAR == 회수본 부모 static/POSCAR 바이트 동일. 승계 검사도 같은 규칙으로 static/POSCAR 를 대조한다 |
| 7 | 완주 7잡의 결과가 1단계 게이트(STAGE1_PASS)에 안 먹힘 | ✅ | 분석기는 v41·v42 바이트 동일. (i) v41 문맥 + 실물 봉인으로 7잡 per-job 게이트 전부 통과(RESULTS jobs ok). (ii) E1(v42 MANIFEST 문맥·새 봉인)에서 8 선결조건 전부 ✓ · `Δ_vac 0.0 meV` · `δ_gas −0.086 meV`(실물 box20/24 에너지) · STAGE1_PASS.json 기록. 봉인 시각 대조는 분석기에 없다(코드 확인) |
| 8 | 2단계에서 셸에 남은 CONTINUE_FROM 이 새 헛돌이 됨 | ✅ | 2단계는 승계 대상 0 이면 `⚠ 승계 없이 진행` (E1 stage 2 실측) · CONTINUATION.json 은 이전 기록을 `previous_record` 로 보존 |
| 9 | 메일 실행 블록에 `exit 1` 이 있어 로그인 셸이 끊김 | ✅ | GO=0 패턴 · selftest 가 승계 블록에 `exit` 부재를 음성으로 검사 |
| 10 | 메일/README 의 실행 블록이 러너 필수 변수와 갈림 | ✅ | 승계 블록은 `_run_env_block` 정본에서 파생(9변수) · selftest 가 렌더 결과에서 검사 · 메일 렌더러가 승계 블록과 기본 블록을 갈라 뽑는다(렌더러 selftest 4/4) |
| 11 | 잡 입력이 v41 과 달라짐 (그러면 승계도 거부되고 물리도 다름) | ✅ | v41.zip 대비 130파일 중 125 바이트 동일(다른 5 = MANIFEST·README·SUBMIT·decisions.json·run_staged.sh) · 회수본 7잡 입력 6파일 cmp 동일 · job_keys sha16 8a7ae28f 동일 · REGEN_v42.sh 가 허용 밖 차이를 GO=0 으로 막는다 |
| 12 | mirae 가 습관대로 §2 블록(승계 없이)으로 돌려 19잡을 처음부터 (97 h 낭비) | ⚠ 문서만 | 메일 §1′ 을 §2 앞에 두고 §2 제목을 "처음부터 (승계하지 않을 때만)" 로 바꿨다. 강제는 못 한다 |
| 13 | CONTINUE_FROM 경로 오타 (루트가 아닌 상위/하위 폴더) | ✅ | 블록의 GO 검사(MANIFEST·봉인 존재) + 러너의 `묶음 **루트**를 가리켜야 합니다` · 상대경로 거부 · 메일에는 실측 경로 `/home/kgy/projects/sdcp_c12_v41_2026_09_11/sdcp_c12_v41` 를 박았다(회수본 provenance·로그에서 읽음 — **추정이므로 "다르면 고쳐 주십시오" 를 적었다**) |
| 14 | 회수 압축본(OUTCAR.gz)을 CONTINUE_FROM 으로 주는 경우 | ✅ | gz 만 있어도 승계·건너뛰기 자격 인정(selftest 양성) · OUTCAR 와 .gz 둘 다면 거부(분석기 규칙과 동일) |
| 15 | WAVECAR·CHGCAR 수 GB 복사로 디스크 부족 → 중간 실패 | ⚠ 부분 | 같은 파일시스템이면 hardlink(0 바이트) · 아니면 복사. 복사 중 실패는 "어디까지 옮겼는지" 를 찍고 멈춘다(폴더 새로 풀라고 안내). 디스크 검사는 안 한다 |
| 16 | §0 "답 받기 전 시작 금지" 를 보고 다시 기다림 | ⚠ 문서만 | CHANGES/메일 변경 절에 "이미 답을 주셨으므로 다시 답하실 필요 없음" 명시. §0 자체는 README 정본이라 남아 있다 |
| 17 | 이 번들의 MANIFEST `repo_commit`·IDENTITY `repo_commit` 이 최종 커밋이 아님 | ⚠ **미완(설계상)** | 생성기는 dirty tree 에서 번들을 만들지 않아, 지금 산출물은 **임시 클론의 임시 커밋**(a1e61bf…)으로 만든 것이다. 커밋 뒤 `bash runs/sdcp_c12_2026_08_30/REGEN_v42.sh` 로 셋(zip·IDENTITY·SEND_MAIL)을 최종 sha 로 다시 만든다 — REGEN 은 v41 대비 허용 밖 차이를 스스로 막는다 |

## 이 리뷰가 못 본 것 (숨기지 않는다)
- **실물 VASP·POTCAR·mirae 파일시스템**: e2e 는 stub VASP·가짜 PP 트리다. 실물 receipt 의 실행파일/launcher/POTCAR 열이 새 봉인과 같을지는
  "같은 vasp_std 절대경로·같은 mpirun·같은 potpaw 트리·같은 allowlist" 를 mirae 가 유지한다는 전제다. 승계 블록 ③ 이 이전 봉인과 새 봉인의
  VASP/launcher/PP SHA 동일을 **옮기기 전에** 검사하므로 어긋나면 90 h 뒤가 아니라 첫 실행에서 멈춘다 — 그때는 번들 재발급이 아니라 환경 확인이다.
- **1단계 통과 (10잡)**: STAGE1_PASS 의 stage1_jobs 는 10 (nzmag 2는 control). E1 의 5 stub 잡 에너지는 실물 근처 값을 **내가 넣은 것**이라
  Δ_vac=0 은 픽스처의 산물이다 — 증명한 것은 "7 실물 잡의 반송물이 v42 문맥의 모든 게이트를 지난다" 이지 물리 판정이 아니다.
- **decisions.json 사본**이 v41 과 다르다(다른 캠페인 결정 32건 추가 · C-12 항목 동일). `--check_governance` 는 v42 사본으로 통과(rc 0).
- v41 의 `PLACEMENT_PROBE.json`·`_placement.tsv` 는 승계해도 분석기가 읽지 않는다 — 배치 증거는 새 extraction 의 프로브가 새로 남긴다.
