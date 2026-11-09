# MIP-01 Windows namespace 잔여 반례 수령·수정 후보 — 2026-11-09

커밋: `<<sha:Reject unsupported Windows paths in inactive verifier>>`. 가지 `codex/mixer-windows-path-fix-1109`, 바탕은 확인한 B 최신 `69d714d094c4d210e5bf931d5c520e64ca0a751d`다. 기존 가지의 rebase·force·amend는 없다.

검토 핀 `3ca47af5b0acd1b39c1d437949413ef3ac31b831`의 판정은 **MIP-01 부분 해결·OPEN 유지**다. MIPR-01/P2는 같은 결함의 잔여 재현 ID이며 별도 P2로 중복 계상하지 않는다. 새 P1/P3 없음. 양쪽 Windows extended 표기의 verify에서 rc0·43→44·재검사rc1이 보고됐다. 일반 경로 가드·자산·메타·정책 수용은 보존한다. 원 판정과 수령 ZIP은 변경하지 않았다.

이번 후보는 Windows extended/device/UNC namespace를 지원하지 않는다고 명시하고, snapshot/candidate/evidence 세 인자의 원 표기부터 공통 거부한다. 절대경로·resolve 뒤에도 지원 범위를 확인하며 기존 lexical 조상 링크·일반 중첩·snapshot 경계는 유지한다. 기존 폴더의 변경은 verifier 하나뿐이다. candidate43·의존86·자산40·메타8·결속·source inventory는 그대로다.

수정 전후 같은 새 시험과 기존 일반 경로/loader 회귀의 결과는 `docs/reviews/mixer_windows_path_fix_20261109/verification_summary.json` 및 전달 증거에 있다. 원입력은 보존하고 scratch 복사본만 사용했다. 실제 장치·공유 접근이나 실제 OS 링크/동시 변경 자격을 수행했다고 주장하지 않는다. 시험 수 단위는 합산하지 않는다.

선행 사본 둘은 `be4388d0c1d3836bc44df0eada6793fbffdcd6e7`(앞선 `2ac1a2482f0290566ac1d67d972f7c9544a9d291`/원 `73e659273fd2ed6406a4c90011fc6079c7adf95f`와 동등), `d310f741a636954b600c9e4f000bfccba2fee3ce`(검토 핀 `3ca47af5b0acd1b39c1d437949413ef3ac31b831`와 동등)다. Claude는 최신 B에서 원본/동등 반입을 확인해 중복을 건너뛰고 필요한 선행 사본 → 이번 수정 순서로 `cherry-pick -x`한다. 전달 대응표와 패치를 함께 제공한다.

**반박 창 필요:** MIP-01 잔여 namespace 경로의 사전 거부·입력 그래프 보존·일반 양성 회귀 한정 재확인. 발송은 1저자다. 원장 제안은 동일 MIP-01의 다음 `claimed_fixed` 후보/재확인 대기이며 종결·verified를 주장하지 않는다. 공유 원장 직접 수정은 없다.

전체 HOLD, 연구 결과0, 실제 값 열람·연구 실행·제출·MPI·운영 재봉인0이다. Rint 파일·그 시험·리뷰는 건드리지 않았고 LHS/DEM 판정을 변경하지 않는다. 정책과 별도인 현장 자격·wave 승인·실행 GO는 그대로 남는다.
