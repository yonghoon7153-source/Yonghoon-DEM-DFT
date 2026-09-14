# COMSOL63_MESH_AXES_HANDOFF — 원문 보존 기록 (2026-09-14)

인계 ZIP `COMSOL63_MESH_AXES_HANDOFF.zip` 은 사용자 PC(WSL `~/mesh_axes/`)에서 풀었고, 이 폴더의 파일은 사용자가 그 압축 해제본에서
`cp --parents` 로 복사해 커밋한 것이다 (`2fa058a`). 이 폴더는 `.gitattributes` 의 `reviews/r14_repros/codex63/mesh_axes/** -text` 로
**줄끝 변환 없이** 저장된다 — md 원문 두 개(`outputs/mesh_axes/MESH_AXES_RESULTS_KO.md` 89 줄 · `outputs/NEXT_RUN_PLAN.md` 46 줄)는
CRLF 그대로다 (preflight 사본과 달리 sha256 이 명세와 바로 일치한다).

## 대조 결과 (이 저장소에서 실행, 2026-09-14)

| 검사 | 결과 |
|---|---|
| ZIP SHA-256 (`ZIP_SHA256.txt`, 사용자 WSL `sha256sum`) | `96321b9442855f7d0d8c48d1fed54c836387dc23210ad5a8117905f937b613db` — 전달받은 값과 일치 |
| `outputs/mesh_axes/package_manifest.json` | 139 항목 (manifest 자신 제외) · 비압축 337,639,621 B · scope "Only three newly authorized 5-second mesh-axis diagnostics; previous failed range evidence included as reference only" |
| 여기 보존한 항목 | **90 개** — 항목별 크기·sha256 **전부 일치**, 불일치 0 |
| 제외한 항목 | **49 개** — `FULL_LISTING.tsv`(압축 해제본 전체 목록 140 파일, 크기)의 크기가 명세와 전부 일치. 내용: `result_Model.mph` 3 (87,513,387 · 87,538,355 · 46,737,803 B) · `console.log` 3 (~20 MB) · batch/compile/worker 로그 · `*.java` 7 (staged·generated·제출본·`PreflightMeshFine5s.java`) · `figures/axis_comparison.{png,pdf}` · `dmodel.xml` 3 · `axes_profile_{N,P}.csv` 6 (7.3–8.3 MB) · `work/*.py` 11 |
| 명세 밖 파일 | `ZIP_SHA256.txt` · `FULL_LISTING.tsv` (이쪽이 만든 것) · `package_manifest.json` (자기 자신, 28,950 B = 목록 크기) |
| 목록 합계 | 140 파일 337,668,571 B = 명세 337,639,621 + manifest 28,950 |

제외 이유: mph·로그·java 는 공개 저장소에 두지 않는다 (원본 모델 계열 자료·기계 경로 포함 가능), 대용량 CSV 는 결과 요약이 `results/`
에 있다. 필요하면 사용자 PC 의 압축 해제본에서 같은 방법으로 추가한다.

## 이쪽에서 다시 계산해 확인한 것

- `results/Axes300R40_vs_Axes300R80_0_to_{1,5}s.csv` · `..._vs_Axes600R40_...`: 107/187 행, 시각 단조 증가, 0→1/5 s.
  `difference_V_second_minus_first_V` 최대 = 반경축 **2.5053108636261 mV @0.04 s**, 물리축 **1.08668e-11 V @0.001 s**;
  같은 행의 분해 δΔEeq +2.5506300937527 mV · δΔη −0.045776895549964 mV · δΔφL +4.576654234e-7 V; 분해 잔차 최대 7.35e-16 V.
- `..._profile_at_surface_peak.csv`: 표면 x 차 최대 **4.1823984380182e-5** @0.04 s · N · sample 240 · z=52 µm, x_first 0.011840794827564697.
- `*_native_steps.csv`: 저장 해 215/235/215 · 최대 step 0.05 s · 0.04 s 의 step 0.005/0.002/0.005 s · 마지막 시각 5.0 s.
- `native_evidence.json`: mesh1 300 요소(120/60/120) · 입자 Nel 40/80/40 · transient DOF 11725/21405/23365 · 속성 1143, 미독 0.
- `preserved_before.json`: 333 항목 · 191,105,291 B; 이전 인계본을 `outputs/COMSOL63_PREFLIGHT_HANDOFF.zip` 46,999,470 B ·
  `3bc4e4e4d14ff815a710998ac3e538712343933cef6d460eb5845f21e7235018` 으로 식별 — 실제 전달본(47,006,147 B · `097d4b65…c3b51`)과
  포장본 식별이 다르다. **미결로 둔다** (변조 단정도 전수 검증 완료도 아님; `docs/COMSOL_REBUILD_SPEC.md` §10-5).

## 확인하지 않은 것

COMSOL 재실행 · java 소스와 이전 소스의 동일성(패키지의 `independent_source_review.py` 주장) · mph 해시 · 이전 333 파일의 보존(그 파일이
여기 없다) · 물성·OCP 의 물리적 정확성. 판정은 `docs/COMSOL_REBUILD_SPEC.md` §10 — 전체 메시 수렴 미완 · 장시간 본 실행 보류.
