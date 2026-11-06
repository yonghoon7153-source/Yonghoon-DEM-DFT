# MLA-01–03 수정 후보 — 외부 재확인 대기

검토 핀 `b57fe91503ba68cec6f41aec247851262788e48f`의 외부 판정은 정적 준비·문서 경계를 한정 수용하고 제출·작업시작 코드에서 P1 하나/P2 둘을 발견했다. 이번에는 시험을 먼저 추가한 뒤 초안을 수정했다. **자체 종결하지 않는다. MLA-01/P1·MLA-02/P2·MLA-03/P2와 전체 HOLD 유지. 실제 sbatch·MPI·연구 계산0회.**

| ID | 후보 변경 | 검출 근거와 한계 |
|---|---|---|
| MLA-01 | 제출 환경의 SBATCH_/SLURM_/SALLOC_/SRUN_를 거부하고 허용된7환경키만 전달. 자원·시간·경로를 명령행 고정. 작업시작에서 rank/node/CPU/QoS/partition 및 array/heterogeneous 표지 확인 | 원6변수+별칭 음성 대조와 정상 인자/환경 대조, 할당 불일치에서 mock MPI0회. 실제 SLURM 적용/환경 진위/MPI 프로세스 관측은 미검증 |
| MLA-02 | 설치 경로와 공통 저자 GO/정책에 묶인 admission lock·예약/결과 원장. 서로 다른 팔도 같은 한도 사용. pending/uncertain/failed 제출은 다음 팔 HOLD | 동시성1 경쟁·동일case경쟁·동시성2 후세번째·불명확/실패/timeout/interruption 후 다른팔 차단. 실제 Lustre 원자성 미검증 |
| MLA-03 | 제출/시작의 fresh 집합에 종료 영수증 등 추가, dangling symlink 포함. 영수증은 배타 생성 | 기존 job_end면 MPI0회·바이트 보존. 실행 중 생긴 충돌 파일도 보존하며 HOLD. 정상·비정상 exit와 spawn error의 TECH 흔적 보존 |

## 보수적 예약의 미완료 범위

공통 원장은 하나의 승인된 설치 루트에만 적용한다. 같은 정책을 복사해 다른 루트에서 쓰면 install_root 불일치로 거부한다. 서로 다른 정책/설치를 임의로 승인하는 행위를 인증하는 도구는 아니다. 실제 저자 승인 문서의 진위와 단일 설치 신원은 별도 검토 사항이다.

예약은 submitted/pending/uncertain을 보존하며 자동 해제하지 않는다. 실시간 관측과 예약을 합산하므로 자기 작업을 이중 계수하여 보수적으로 거부할 수 있다. 프로세스 강제 중단으로 lock이 남으면 자동 삭제하지 않는다. 다음 파동에는 정확한 scheduler 대조와 별도로 검토된 수동 해제 절차가 필요하며 이번에는 삭제/재시도 명령을 제공하지 않는다. 이 제한을 완료된 first8 운영 기능으로 과장하지 않는다.

실제 scheduler의 walltime/output 해석·환경 진위, 바이너리/MPI/런타임·STL·100k 양성 경로·현재 자원/디스크, MXD2R와 저자 NP/동시성/순서·범위 GO는 남는다. 초안의 `.example`은 execution_authorized=false이며 등록/실행 허가를 만들지 않는다.

## 검증과 원본 보존

원본 외부 ZIP·판정·관측 JSON은 external에 바이트 그대로 보존했다. 외부 판정의 상대경로는 그 ZIP 기준이므로 판정문은 보관 텍스트로 두고 원 Markdown은 원본 ZIP에 남겼다. 원 snapshot89개·전달115멤버는 고정 Git 핀/원래 ZIP과 대조했다. 세부는 intake_verification.json.

수정 전 새 시험13메서드에서32개의 subtest/단언 실패와 누락 TECH 영수증 오류1개를 보존했다. 이는13개와 합산하지 않는다. 최종 새14메서드, 기존 제출10, 작업시작8, hard-stop1메서드(실제 입력7종)가 Python3.12.14와3.8.20에서 각각 통과했다. 버전별 반복이나 양성/음성 관측을 별도 고유 시험으로 합산하지 않는다. 실제 subprocess는 모두 mock이며 hard-stop 시험의 셸은 sentinel만 사용한다.

환경·예약상한·불명확 상태·종료 배타 생성의4개 가드 변이를 scratch에서 되돌렸을 때 각 지정 시험이 단언 실패로 검출했다. 신원 해시만 달라져 거부되는 오검출을 피하려고 변이 job-start의 봉인 값은 변이 사본 안에서 함께 갱신했다. 기존 실패 기록·원래 source seal·40개 계획 자산과 생성기/판독기·옛18·D3 SOP는 보존했다. 전체 check_all/현장 실행은 반복하지 않았다. 이번 새 모의 시험은 공용 check_all/CI에 연결하지 않았으며 통합 때 별도 연결·합친 트리 검증이 필요하다.

최소 재현은 준비 폴더의 test_mla_boundaries.py·test_submit_draft.py·test_job_start_draft.py·test_prepare_only.py다. `replay_mutations.py`는 인자로 지정한 새 결과 디렉터리에만 로그를 쓰고 scratch 사본을 변이한다. 원본 소스·연구 경로는 바꾸지 않는다. 원래 README의 hard-stop 입력8종 오기는 실제7종으로 정정했다.

## 인계

1저자 요청대로 LHS inventory·LHS N의 한정 외부 수용과 이번 믹서 후보를 종합해 Claude에 인계한다. LHS 수용과 달리 이 후보는 외부 재확인 대기다. `review_request.md`는 별도 Codex 반박 창용이며 발송은1저자다. 공유 기록은 ledger_proposal.json 제안만 두고 직접 변경하지 않았다. Rint② 우선·통합 시점은1저자 결정이다.
