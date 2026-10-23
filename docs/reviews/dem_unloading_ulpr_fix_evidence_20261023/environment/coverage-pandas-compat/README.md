# Coverage P8 환경 원인 분리 — 2026-10-23

판정: pandas 3.1.0의 기본 CSV 부동소수점 파싱과, pandas 2.x에서 측정한 legacy 반환값 바이트 핀 사이의 환경 차이다. 현재 ULPR 변경이 원인이 아니다. 공유 코드·핀·원장·Git 상태를 수정하지 않았다. 증거는 이 디렉터리에만 생성했다.

## 실행과 결과

공통: `/workspace/Yonghoon-DEM-DFT`에서 `/workspace/.cloud-setup/nonrint/activate.sh`를 source. Python 3.11.17, NumPy 2.4.6, SciPy 1.17.1. BLAS/OMP/MKL/NumExpr 1 thread.

| 환경 | 실행 | 결과 |
|---|---|---|
| 기존 pandas 3.1.0 | `python3 -I scripts/coverage_physics_vs_hertzian.py --selftest` | rc 1, 15/16 통과; legacy ①의 summary SHA만 불일치 |
| 외부 overlay pandas 2.3.3 + pytz 2026.5 | `python3 -I -B`에서 overlay를 sys.path에 추가하고 원본 스크립트를 runpy로 실행 | rc 0, 16/16 통과 |

기존 로그: `coverage-current.log`. overlay 전체 selftest 로그: `coverage-pandas233.log`. 저장 full_metrics와 per-AM CSV는 두 환경 모두 원래 핀과 같다.

| 항목 | pandas 3.1.0 | pandas 2.3.3 / 기존 핀 |
|---|---|---|
| summary SHA256 | `7b157b3dcc9cfda0d3be74ab7b884aa4185b8d16bc7234aac2c3a95fa8acc9cf` | `6624d46ed2ce5c9470f086d6f83b633dc9561ec0d0c9df012ade0c299a659ef1` |
| AM_S.hertzian_mean | 0.6097808985329525 | 0.6097808985329526 |
| AM_S.delta_mean_pct | 76.24197327312643 | 76.2419732731264 |

`parser_probe.py`로 **동일한 fixture 파일**을 각 pandas 버전에서 읽었다. atoms.csv는 같고 contacts.csv는 10개 셀에서 float.hex가 다르다. 원문 숫자와 양쪽 binary float는 `current/current/contacts.csv`, `parser-current.json`, `parser-pandas233.json`, `parser-difference.json`으로 대조 가능하다. 이는 비반올림 반환값 두 필드에 전파된다. 이 검사는 pandas 3의 수치가 물리적으로 틀렸다는 판정이 아니라 기존 바이트 계약과 환경의 불일치를 분리한 것이다.

`probe.py`는 현재 compute_case와 `git show e72067854:scripts/coverage_physics_vs_hertzian.py`로 읽은 pre-v2 compute_case를 같은 fixture에 실행한다. 두 소스의 산출 SHA 3개는 각각의 환경 안에서 모두 같다. 이 옛 코드 비교는 현재 plastic_coverage와 dem_analysis_core를 사용한다. 해당 두 파일과 현재 coverage 파일은 모두 HEAD blob과 worktree SHA256이 같다(`current/result.json`, `pd233-run/result.json`).

## 최소 환경 조치

재현해 검증한 핀은 `pandas==2.3.3` + `pytz==2026.5`. NumPy 2.4.6을 유지했다. 이번 triage에서는 공유 venv를 수정하지 않았으며, 두 패키지만 `pandas233/` 외부 overlay에 설치했다. 공유 환경에 핀 적용 및 전체 게이트 재실행은 root 담당이다. 이 좁은 결과는 union 전체 검사나 다른 fullgate 실패의 해결을 주장하지 않는다.

설치 원시 로그: `install-pandas233.log`, `install-pytz.log`. 최초 no-deps 설치는 pytz가 없어 probe가 ImportError였고, pytz 추가 뒤 재실행했다. `pd233-probe.log`는 성공 재실행 로그다.

재현 명령(실제 실행한 경로):

```bash
source /workspace/.cloud-setup/nonrint/activate.sh
python3 -I -B /workspace/.cloud-setup/nonrint/gate-triage-coverage/probe.py \
  --repo /workspace/Yonghoon-DEM-DFT \
  --out /workspace/.cloud-setup/nonrint/gate-triage-coverage/replay \
  --overlay /workspace/.cloud-setup/nonrint/gate-triage-coverage/pandas233
python3 -I -B - <<'PY'
import runpy, sys
sys.path.insert(0, '/workspace/.cloud-setup/nonrint/gate-triage-coverage/pandas233')
sys.argv = ['scripts/coverage_physics_vs_hertzian.py', '--selftest']
runpy.run_path('/workspace/Yonghoon-DEM-DFT/scripts/coverage_physics_vs_hertzian.py', run_name='__main__')
PY
```

실행 경로는 로그 기록이다. `probe.py`, `parser_probe.py`는 --repo/--out/--overlay/--fixture 인자로 경로를 받는다. 이 README 안 CLI는 원래 실행 위치를 기록하며 다른 위치에서는 그 인자를 바꾼다. overlay 패키지 바이트는 증거 manifest에서 제외하며 버전과 설치 로그로 식별한다.
