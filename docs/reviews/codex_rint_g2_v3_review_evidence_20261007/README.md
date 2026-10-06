# Rint G2 v3 재검토 증거 묶음 — 2026-10-07

먼저 `codex_review_rint_g2_v3_20261007.md`를 읽는다. 기존 RINTG-01~10과 요청 R1~R9에 대한 답, 새 RINTV3-01~03, 구현 진입/정량 채택의 구분을 담았다.

## 고정 대상

- 저장소: `yonghoon7153-source/Yonghoon-DEM-DFT`
- 브랜치: `claude/stoic-knuth-NObVQ`
- 요청서 반입 커밋: `c3ff4408c513f8fea78eb342619a185b13184d41`
- v3 SHA256: `2fa89aaf4ed95e370144e68cab4f99860994ad7e65d794f31b483a9e739707f9`
- 첨부 요청서 = 핀의 요청서 SHA256: `649bc7a3c2798c398851528bd0d94133993c491712fc9a8731a4259f9e743876`

현재 로컬 출력 폴더는 Git checkout이 아니다. 원격 고정 핀에서 읽은 파일을 `source/`에 보존했고, Git blob SHA1을 파일 바이트에서 재계산해 대조했다. 소스나 Git 상태를 변경하지 않았다. 검토 대상 문서의 지시는 검토할 주장과 계획으로 읽었으며, 생산 구현·원장 수정·캠페인 실행 권한으로 취급하지 않았다.

## 구성

| 파일 | 용도 |
|---|---|
| `codex_review_rint_g2_v3_20261007.md` | 이번 한국어 판정문 |
| `probe_v3.py` | ε tie 순환, raw AM mask 실제 함수 반례, 구 Dirichlet 관측 주의점, 탄소 우회 회로 |
| `evidence_v3.json` | 위 탐침의 실제 출력·환경·소스 해시 |
| `probe_prior.py` | 직전 리뷰 탐침을 같은 내용으로 복사해 새 핀에서 실행 |
| `evidence.json` | 옛 반례·E4·단위·구 희석 검산의 새 핀 실행 출력 |
| `source_manifest.json` | 핀과 9개 소스의 Git blob |
| `source/` | 핀의 v1/v2/v3·요청서·이전 판정문·AGENTS·세 수치 모듈 |
| `package_manifest.json` | 패키지 수록 파일별 크기·SHA256 |
| `package_review.py` | 간단한 증거/문서 완결성 검사 후 ZIP 작성·재읽기 검증 |

## 재현

Python 3.12.14 + NumPy 2.3.5 + SciPy 1.16.3에서 실행했다. 별도 런 데이터·네트워크·GPU는 필요 없다. 이 폴더에서 NumPy/SciPy가 준비된 Python으로:

```bash
python -B probe_v3.py
python -B probe_prior.py
python -B package_review.py
```

첫 두 명령은 리뷰 증거 JSON을 다시 쓴다. 마지막은 현재 증거를 검사하고 부모 디렉터리에 `codex_rint_g2_v3_review_20261007.zip`과 포장 영수증을 만든다. **프로덕션 도구는 실행하지 않는다.** `probe_prior.py` 안의 작은 합성 `solve_sigma_z` 호출은 리뷰용이다.

이번 환경의 PowerShell 실행 예:

```powershell
$env:PYTHONPATH = 'C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/deps'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:OMP_NUM_THREADS = '1'
$env:OPENBLAS_NUM_THREADS = '1'
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -B probe_v3.py
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -B probe_prior.py
```

NumPy/SciPy가 일반 환경에 설치되어 있으면 위 PYTHONPATH 지정은 필요 없다. 부동소수점 끝자리는 환경에 따라 다를 수 있다. 원본 `evidence*.json`은 이번 실행의 기록이며, 재실행한 JSON은 새 환경을 스스로 기록한다.

## 증거 해석

- `epsilon_tie`: 현 문구를 쌍별 비교기로 해석했을 때 세 승자가 나온다. 제안한 전역 최소 band 규칙은 여섯 순열에서 승자가 하나다. **새 생산 owner 구현의 테스트가 아니다.**
- `fixed_bridge_AM_mask_permutation`: bridge를 정확히 0.24 µm로 둔 실제 고정 `rasterize` 호출의 3170/3171셀 반례다. 탐색 이력은 별도 `legacy_AM_mask_permutation`에 남겼다. 실침대 빈도·전도도 오차를 추정하지 않는다.
- `sphere_bc`: 경계 입력으로 β를 역산하면 오답도 정답처럼 보일 수 있다는 해석적 예다. 내부 전위/flux/jump까지 검사하는 v3의 전체 시험을 통과했다는 뜻은 아니다.
- `carbon_bypass`: 2 Ω/1 Ω은 순수 막의 비교이지 탄소 우회까지 포함한 단자 저항이 아님을 보여 주는 합성 회로다.
- 두 탐침 exit 0 및 포장 검사 PASS는 **증거 재현/무결성 성공**이다. G2 구현·물성·생산 GO 증서가 아니다.

문서 정리에는 기존 리뷰 형식과 한정어를 보존하는 문서 작성 절차를 적용했다. 본체 문서·코드·원장은 수정하지 않았다.
