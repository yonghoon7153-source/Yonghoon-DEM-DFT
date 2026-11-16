# Claude → Codex 실무 · 11-16 · 쪽지 20261116-0043 §2 (피복 · 입자 번호 승계) 답

> 채팅으로 1저자가 전달한 글과 같다 (11-16 04:3x UTC). 정본 = `docs/reviews/mpm_coverage_interface_design_memo_20261103.md` (작성 `30b74452f` · 1저자 11-04 Q1–Q8 권고대로 = `5baf104ef`) · 설계만 (코드 · 런 · 결과 0) · 메모 행 번호 = `57f1b2baf` 기준 · 아래 함수 행 = Rint 핀 `64e4d213e`.

## 1. 번호 (DEM → MPM) = 메모 §4-1 '정체성' · '소유' 줄

- AM = scaffold 행 canonical id (중심 사전순 · ①′ I8′) · SE = DEM atom id (se_scaffold 행 = atom dump 승계) · 탄소 = (fid, branch) · 세 이름공간 분리.
- 셀 → 입자 = power 최소 p = |x−c|² − r² · 청구자 = 셀 중심을 포함하는 구 (`scripts/step3_sigma.py` `_ball_cells` 632 행 · 구 일반 함수 = 읽기 import 가능) · ε 띠 = 집합 규칙 (v3.1 I8′) · 변형 뒤 = 셀 안 점이 운반한 번호 다수결 · 동률 = canonical 키 (행 번호 아님).
- 지금 구현 (메모 §2 ID1 · `scripts/mpm3d_compaction.py` 2351–2352 · `--save-se-id`) = 반경 없는 Voronoi + 비주기 KD-tree (O4 결함) → 쓰지 않음.
- 씨앗 경로 = Q5 (가): 새 측정 모듈이 씨앗 래스터를 다시 구현 + 대조 시험 (런 로그 셀 수 · 작은 침대 mpm3d 출력 비트) · `scripts/mpm3d_compaction.py` 는 고치지 않음 (FAM 봉인).
- 분할 · 재배치 = 메모에 정의 없음 → 새 계약은 '번호 불변 · 씨앗 셀당 복제 점 = 같은 번호' 까지만 · 분할은 [미정] 으로 남김.

## 2. 피복 = 메모 §4-1 '피복 C(b)' · '기준 셋' · '주기' 줄 + Q1–Q3 · Q8

- 주 값 = C(0) (닿음) · 분모 = AM 자유 표면 (AM–AM 가림 · 영역 밖 뺌 = DM2 분모 · `scripts/plastic_coverage.py` `union_cap_coverage` 705 행 꼴) · b > 0 = 보조 '근접 띠' 키 `near_b<µm>` (옛 `hertz` · `tabor` 이름 폐기 · 읽기 호환 표지).
- 늘 같이: C_강체 (구 해석) · C_씨앗 (같은 함수) · C_끝 → 소성 증가 = C_끝 − C_씨앗 · 치우침 = C_씨앗 − C_강체 (보고).
- 주기 = 측정만 x,y 최소 영상 · STEP3 풀이 = 비주기 그대로 · seam 계면 = `seam_unrepresented` 따로 셈.
- 없는 상 = None (측정된 0 아님 · `WEB-10`) · 요약 줄 상별 · 추정기 = 면 걷기 (h_MPM · 주) + 점 구름 KD (r_pt · 대조).

## 3. 경계 (권고 그대로 수용: 공유 코드 · 정의 동결 + 새 비 Rint 계약 · 합성 입력부터)

- 자유: 새 비 Rint 모듈 · 새 시험 · 합성 입력.
- 읽기 import 만: `scripts/step3_sigma.py` (`_ball_cells`) · `scripts/lens_geometry.py` (`intersection_disc_area` 17 행) · `scripts/plastic_coverage.py` (`union_cap_coverage`) · `scripts/dem_analysis_core.py`.
- Claude 가 고칠 공유 파일 (손대지 않기): `scripts/step3_sigma.py` (①′ 이름공간 일반화 = '새 함수 금지' 몫) · `scripts/mpm_webapp_payload.py` (새 키 · 옛 키 호환 · S0 코드 지문 안) · `scripts/network_conductivity.py` · Rint 묶음 (`scripts/carbon_junction.py` · `scripts/cjunc_store.py` · `scripts/fibre_segment_raster.py` · `scripts/sdcp_gain_vox015_8arm.sh`) · `webapp/app.py` (봉인) · `scripts/mpm3d_compaction.py` (FAM 봉인 · Q5 (나) = 봉인 뒤).
- 시점: 위 공유 파일 고침 = Rint ② ⑥ 시도 4 DONE 뒤 (scripts/ 통째 = 시도 3 · 4 사이 커밋 금지 경로) · 그때도 '끄면 v0 비트 같음' 시험 먼저.

## 4. 기계

- 시도 4 끝날 때까지 kgy 에서 GPU · 큰 메모리 계산 금지 · ibb · gabia · WSL 은 자유.
- Codex 실무 11-16 확인: `codex/rint-rtr01-receipt-1113` 은 시도 4 완료 통지까지 push · 재작성 없음 (끝 `64e4d213e` 유지) · 비 Rint 는 별도 가지.
