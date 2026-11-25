DI 수정본 — dad10ecf 기준 적용용 패치

수정 파일은 tools/ionic/melt_quench_uma.py, tools/ionic/li2s2_stage1_runner.py 두 개입니다.
실패 시드의 재담금질 차단, 보존된 실행 비용 대조, 그룹 조회 불가 시 차단,
그룹 정리 시간 계상, 단조 시계와 동일 부팅 근거에 의한 고아 실행 비용 처리를 반영했습니다.
runner selftest에 9개 검사를 추가했습니다. 기존의 invalid 복구 양성 경로도 통과합니다.

저장소 루트에서 먼저 git apply --check li2s2_DI_fixes.patch로 확인하고,
충돌이 없을 때 git apply li2s2_DI_fixes.patch로 적용할 수 있습니다.
기준 커밋 이후 두 파일이 수정되었다면 새 변경을 덮어쓰지 말고 해당 차이를 대조해야 합니다.

검증: 드라이버 191/191, 러너 56/56 (Windows worker thread).
수정 6가지를 각각 되돌린 변이본은 모두 해당 음성시험에서 실패했습니다.
패치는 git apply --check 및 실제 적용 후 두 파일 SHA 일치를 확인했습니다.
Linux 전용 실제 프로세스 시험은 이 환경에서 실행하지 못했습니다.
배포 환경에서 두 도구의 --selftest를 실행하고 남은 프로세스가 없는지 확인해야 합니다.
이 묶음은 코드 수정·검증 자료이며 실제 담금질을 시작하거나 proposed 결정을 active로 바꾸지 않았습니다.

보존 폴더는 기존 run_root/A 또는 B 아래에 둡니다. 같은 시드의 과학적 pass/fail은 재실행할 수 없습니다.
invalid 재시도는 이전 run_id를 명시한 STOP 확인과 연결되며 이전 실행 비용도 남습니다.
새 실행에는 stage1_attempt.json이 생깁니다. plan 생성 이전에 중단돼도 이 파일을 보존해야 합니다.
옛 고아 실행에 단조 시계/부팅 기록이 없으면 비용 미확정으로 막힙니다. 0이나 UTC 어림으로 대체하지 않습니다.
