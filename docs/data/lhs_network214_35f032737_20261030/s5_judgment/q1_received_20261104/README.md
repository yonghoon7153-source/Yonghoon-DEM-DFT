# LHS Q1 11-04 원본 수령 — 배포 HOLD 유지

## 이번에 확인하는 것 / 확인하지 않는 것

- 확인 범위: 1저자 업로드의 크기·SHA256·멤버, JSON 바이트 보존, JSON에 기록된 수치의 산술 대조, Q7/Q6 결정의 전사.
- 제외: 원격 WSL 입력/솔버 재실행, 압력 기록 214행의 독립 검증, 단계 A 생성, 인계표 회귀, v1.3 배포 GO, 원장 verified 전환.

원본 `q1_settle_20261104.tar.gz` = **2,333 B** · SHA256 **`485aca07db04462bef971c1586e6c88f52623f5caa67edc0396e59ac1e212698`**. 반입 전에 대조했다. JSON은 archive에서 읽은 바이트 그대로이며 새 직렬화를 하지 않았다. 디렉터리 항목 네 개는 원본 archive에 남아 있으며, 그중 비어 있는 work 디렉터리는 두 개다. git에 별도 빈 디렉터리를 만들지는 않았다.

| 원본 멤버 | B | SHA256 |
|---|---:|---|
| `out_lhs00_123/settle_lhs00_123.json` | 3811 | `9fbe029cebde60a26e786544ff39d583fd1232c441620cbf010c22d80bc863e8` |
| `out_lhsx_026/settle_lhsx_026.json` | 3790 | `e556ad99b6d6b4f52e4b39725a0b0c5a4693f8dcbd7b5c5ce2e16bd3a5cd00a8` |

`intake.json`은 수령 후 만든 대조 기록이며 WSL 원본 산출물이 아니다. 각 원본 JSON에 shell rc 필드는 없다. rc 0/3과 압력 중단은 사용자 전달 내용으로 구분했다. `lhsx_026`의 원본 `verdict=HOLD`, B=false, why를 보존하고 1저자 Q7 포함 결정을 별도 칸으로 기록했다. 물리 원인 부재를 이 수령 대조로 새로 입증하지 않는다.

산술 = 원본 숫자만 사용. 각 가지의 B는 `abs(sigma_adaptive-record_v12) <= half_unit + 1e-12*max(1,abs(sigma_adaptive))`로 대조했다(기존 도구 `docs/data/lhs_network214_35f032737_20261030/s5_judgment/tools/s5_q1_electrode_settle.py`의 규칙). 두 시료 × 세 가지의 계산된 B는 기록과 같았다. FULL Δ는 `sigma_b7_inprocess/sigma_adaptive - 1`로 다시 계산했고 두 기록값과 같았다. 계산은 저장된 float64 수에 한정되며 원 실험/솔버를 재현한 시험이 아니다.

상세 결과·Q6/Q7·압력 보고와 다음 조건은 상위 README §11-7. 원본 SHA256 목록은 `SHA256SUMS`로 확인한다.
