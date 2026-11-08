# MLAR-01 경로 문자 경계 — 한정 독립 재확인 요청 (2026-11-09)

**대상은 11-08 MLA B 검토에서 남은 MLAR-01/P1 수정 후보뿐이다. 전체 HOLD, 실제 연구 결과 0건이다.** 실제 제출·MPI·DEM·값 열람·운영 재봉인·현장 자격·등록·배포·통합·원장 종결 승인을 요청하지 않는다. 발송은 1저자가 맡는다.

## 검토 신원

- 원 외부 검토 핀: `a2e0396241c4e4cddea3c8771872f9fdcc650ef7`.
- 이번 새 가지 바탕: `40d9658c07eb578d03dff7905b301da7efacf582`.
- 새 후보의 push된 핀과 파일 신원: 전달 ZIP의 `PIN.txt`, `source_inventory.json`.
- 원 판정 수령 신원: `receipt.json`. 외부 원 증거 ZIP은 리포에 반입하지 않는다.
- 원 12의존 봉인: `527e244e4ebd6f0cb04c6cfb2ff5f3a52fb01996`. 합성 fixture에 원 바이트를 쓰는 것이며 최신 B/R01/seed를 운영 봉인으로 교체한 것이 아니다.

원 판정은 MLA-01 부분/열림, MLA-02 제출/예약 및 MLA-03 로컬 파일/모의 경로의 원 결함 한정 종결 가능이다. MLAR-01은 기존 MLA-01의 잔여 경로이며 독립 P1 두 건으로 중복 계상하지 않는다. 이번 판정도 각 범위를 분리해 적어 달라.

원 launch/recheck README의 외부 대기·OPEN은 당시 기록으로 보존한다. 이를 이번 `receipt.json`의 새 한정 판정과 구분하고, 후보가 역사 README를 소급 수정하지 않았음을 함께 확인해 달라.

## 질문

1. **원 경로 반례 차단:** `canonical_runner`가 기존 네 바인딩 `python`·`job_start`·`stdout`·`stderr`에서 TAB·VT·FF를 runner 생성 또는 fake sbatch 이전에 거부하는가? 원 CR 사례는 전체 우회가 아니었다는 구분을 유지하는가?
2. **정상·추가 문자 경계:** `str.isspace()`인 Unicode 공백·C0·DEL 거부 정책이 실제 입력과 맞고 정상 경로의 canonical runner 바이트·인자가 보존되는가? C1 전체 거부나 shell quoting을 통한 Slurm 파서 안전성으로 확대하지 않는가? 과도한 정상 입력 거부나 검사를 건너뛸 실제 경로가 있다면 최소 반례를 적어 달라.
3. **기존 방어 회귀:** SBATCH_/SLURM_/SALLOC_/SRUN_ 환경 음성, 명시된 환경 allowlist/고정 자원 argv, 실제 할당 표지의 기존 음성 모의가 유지되는가? 실제 scheduler나 MPI를 시험한 것으로 과장하지 않는가?
4. **제출/런 실패의 분리:** MLA-02·03 한정 판정을 보존하고, `SUBMITTED` 이후 런 실패를 자동 캠페인 HOLD로 전파하지 않는 사실과 승인 운영자의 감시·STOP·후속 파동 중단 책임을 분명히 적었는가? 미완료 end/충돌/잔존 예약을 완료·자동 해제·재시도로 승격하지 않는가?
5. **보존과 비활성 경계:** 원 40자산·12의존/source seal·job-start·MLA-02/03 구현·옛18·D3 SOP가 의도한 범위에서 보존됐는가? 운영 source seal 전환·최종 묶음·현장 자격·NP/동시성/순서·별도 실행 GO가 여전히 별개인가?

## 읽을 근거와 판정 한계

`README.md`, `receipt.json`, 수정된 제출 초안, `test_runner_paths.py`, `run_mock_checks.py`, `evidence.json`, `source_inventory.json`, `ledger_proposal.json`을 함께 대조한다. 정확한 안전 재현 명령·Python 신원·수정 전후 로그 및 rc는 `evidence.json`에 기록한다. Windows 문법 어댑터를 적용하지 않은 canonical 함수(수정 전/후 각각)의 문자 검사와 Windows 문법/용량 어댑터를 적용한 전체 제출 모의를 구분해 달라. 첨부 원 증거의 스크립트나 제출/작업시작/sbatch/commands 초안을 실제 실행하는 요청이 아니다. 정적 소스와 작은 합성 모의만으로 닫을 수 없는 현장 사실은 NOT_ESTABLISHED로 남겨 달라.

검토 ZIP 추출 루트의 안전 재현 명령 두 개는 `README.md`의 안전 재현 절에 있다. 수정 전은 기대 rc1, 최종 LF 후보의 새 시험/기존 회귀는 기대 rc0이다. 각각 존재하지 않는 새 작업 폴더를 사용한다. 중간 CRLF 후보 통과와 최종 LF 재검증은 같은 suite의 반복이며 고유 시험 수로 더하지 않는다.

재현은 고정 Git blob 또는 ZIP snapshot 바이트를 기준으로 한다. Windows worktree의 줄바꿈 변환으로 인한 자산 SHA 불일치와, 원인 미확정인 archive 산출물 자산 SHA 불일치의 준비 중단 두 건을 별도 보존했다. 둘 다 대상 시험 0건이며 정책 시험 결과에 합산하지 않는다. 정식 수정 전 입력은 원 ZIP의 준비 73파일을 scratch에 복사해 바탕 B Git tree blob OID 73/73과 대조한 snapshot이다. 이 신원과 후보 변경분을 대조하고 worktree 체크아웃이나 실패한 archive 산출물 자체가 봉인 바이트라고 가정하지 말아 달라.

닫힐 수 있는 범위는 **MLAR-01의 경로 문자 경계와 그 수정의 회귀/보존 범위**다. MLA-02/03 원 결함의 좁은 수용 근거를 전체 런 실패 자동 차단이나 POSIX/Lustre/crash 복구 인증으로 확대하지 않는다. 정상 rc0, 해시 일치, 정적 자산 수용, 이전 R01/seed 수용은 실행 GO가 아니다.

새 P1/P2/P3가 있으면 파일·최소 반례·영향·최소 수정·닫힘 증거를 적어 달라. 없으면 MLAR-01 범위의 수용과 남은 운영/승인 경계를 함께 명시해 달라. 실제 저자 선택·원장 변경·예약 해제·현장 실행을 이 검토가 대신하지 않는다.
