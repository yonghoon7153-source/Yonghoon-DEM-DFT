# 6차 믹서 LH 리뷰 증거

정본 회신은 꾸러미의 `docs/reviews/codex_review_mixer_highbo_round6_20260928.md`입니다.
대상 핀: `18787ab98a13361c37b2343bd07ae276142d0953`.

이 폴더의 scripts/, dem_scripts/, docs/, AGENTS.md는 검산용 소스 사본입니다. **생산 리포에 덮어쓰거나 그대로 병합하지 마십시오.** 23개 원본은 sources.json의 Git blob SHA와 source_hash_verification.json으로 대조됩니다. __pycache__는 패키지에 포함하지 않습니다.

## 증거 구분

- agent_launch/: 실제 시작 checker와 런처 Python 관문의 합성 반례. 셸 런처 자체는 발사하지 않습니다.
- agent_phase/: 실제 영수증 producer/consumer의 합성 메시·로그 반례. Python run-status 기록 코드만 실행합니다.
- agent_science/: 실제 생성기의 메모리상 CED/dt 계산 및 명시된 접촉 근사.
- design_probe.py: 메모리상 덱의 개입 시점과 contrast/E0 산술.
- fixture_helpers.py: 이전 독립 리뷰의 합성 입력 생성 코드를 로컬 동봉. main은 이번 probe에서 호출하지 않습니다.
- selftests/: 해당 핀의 Python selftest 출력. 별도 agent_phase/phase_selftest_python.*는 30 중 Python 28개만 실행한 기록입니다.

## 재현

NumPy/SciPy가 있는 Python 환경에서 이 폴더를 cwd로 사용합니다. PYTHONDONTWRITEBYTECODE=1, PYTHONUTF8=1, PYTHONIOENCODING=utf-8을 설정합니다.

```bash
python3 verify_sources.py
python3 agent_launch/probe_launch.py
python3 agent_phase/phase_probe.py
python3 agent_science/stiffness_probe.py --compact
python3 design_probe.py
python3 agent_phase/capture_selftest.py
```

probe의 rc 0은 '회귀가 없으므로 생산 GO'가 아닙니다. 정상 대조가 통과하고 **지적한 결함이 실제로 재현됨**을 assertion으로 확인했다는 뜻입니다. 각 하위 도구의 실제 반환값은 출력 JSON에 있습니다. 합성 폴더의 임시 경로·날짜·해시는 재실행 때 달라질 수 있습니다.

DEM/MPI/sbatch/scancel은 실행하지 않았습니다. 실데이터 M/겹침, 신규 rank 계측, scheduler 정지 여부는 인증하지 않습니다. Bash test_launcher 98 전수와 check_all은 이번 환경에서 실행하지 않았습니다.

## 바이트 보존

ZIP 내 MANIFEST.json은 자기 자신을 제외한 모든 파일의 길이·SHA256을 기록합니다. 압축 후 엔트리를 다시 읽어 대조했습니다. 소스와 원출력은 EOL 변환 없이 취급하십시오. source_hash_verification.json은 원 소스의 Git blob ID를 확인하는 별도 검사입니다.
