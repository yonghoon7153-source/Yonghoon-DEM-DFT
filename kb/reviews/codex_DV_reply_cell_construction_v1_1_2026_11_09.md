---
title: "DV 회신 — 셀구축 v1.1 + b2o3 B·O 배치 카드 개정 1 v1.1: NO-GO (1 단계 생산 보류) · P1 4 (큐 실패 전파 · 완료 구조 결속 · 포논 빈 캐시 정체성 · B 결합 음이온 분류) · P2 6 · P3 2 · Q1–Q7 · 1 단계 해제조건 네 묶음"
date: 2026-11-09
updated: 2026-11-09
tags: [review, b2o3, cell-construction, uma, dft, phonon, framework, codex, reply, letter]
letter: DV
track: b2o3
channel: codex
kind: reply
status: 회신 원문 (2026-11-09 · 사용자 붙여넣기) — NO-GO · 기준 커밋 ad4f41b8 · 생산 계산 안 함 · 재현 수치는 합성 시험 값
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: mixed
evidenceScope: multi-source-primary
---

> 프롬프트 `codex_DV_prompt_cell_construction_v1_1_2026_11_09.md` 에 대한 Codex 회신 **원문 그대로** (사용자가 2026-11-09 대피 세션에 붙여 넣음). 고치지 않는다.
> 링크의 `C:/Users/Administrator/Documents/Codex/...` 경로는 Codex 쪽 작업 사본이다 (이 저장소 경로가 아니다).
> 맨 아래 부록 셋은 사용자가 회신과 같이 붙여 넣은 검증 기록 JSON 이다 — 내용 그대로 (`framework_probe_results.json` 은 공백 · 줄바꿈만 접었다 · 파싱 결과 같음).

---

NO-GO — 현재 1단계 생산 실행은 보류입니다. 실제 45×3 구조 생성과 이전 핵심 반례들은 상당수 해결됐습니다. 하지만 러너의 실패 전파, 완료 산출물 검증, 실행 전 판독기가 아직 닫히지 않았습니다. 포논·골격 분석에서 발견한 문제는 해당 후속 단계의 해제조건으로 구분했습니다.

대상은 **`ad4f41b8c79920947e7f8b0b52b72a129052a537`**입니다. 원본 저장소는 수정하지 않았고 생산 UMA·DFT·MD는 실행하지 않았습니다.

실제 host로 45개 B 배치 × 3가족 = 135구조를 생성해 조성·부모 구조·Li 거리를 독립 검사했습니다. 생성기 38건, 포논 10건, 골격 22+14건, MSD 217건 selftest를 통과했습니다. 어닐 selftest는 Windows에서 열린 로그의 임시폴더 정리 오류가 발생했고, 임시폴더만 보존하는 조건에서는 25건을 통과했습니다. 따라서 전부 원형 그대로 통과했다고 보고하지는 않습니다.

P0는 확인하지 못했습니다. 아래 P1은 직접 재현했습니다.
1. P1 · 1단계 — 실행과 결과 검사가 실패해도 큐가 성공으로 끝납니다.
   run_uma_kgy.sh:258
   생성된 큐에서 실행 명령을 exit 7, --check_results를 exit 1로 만들었는데 큐는 exit 0이었습니다. 마지막 echo의 성공이 최종 종료코드가 됩니다.
   로컬 Bash 5.3 기본 모드에서는 echo "$(date …) … rc=$?"의 로그마저 둘 다 rc=0으로 나왔습니다. 이 로그 현상은 서버 Bash에서 확인하지 않았지만, 실패 코드를 전달하지 않는 문제는 코드에 남아 있습니다.
   최소 수정: 각 명령 직후 run_rc, check_rc를 저장하고, 저장한 값을 출력하며, 둘 중 하나라도 실패하면 큐도 nonzero로 종료하세요. 실행 실패만·검사 실패만·둘 다 실패·둘 다 성공의 네 경우를 시험하면 됩니다.
2. P1 · 1단계 — 완료 구조를 삭제하거나 교체해도 재개와 결과 검사가 통과합니다.
   run_anneal.py:310, 결과 검사:373
   정상 완료 후 post_relax.xyz를 다른 조성의 구조로 바꾸거나 삭제했습니다. 두 경우 모두:
   - check_results(..., require_converged=True) → 문제 목록 []
   - 같은 입력으로 재개 → 실행 0건, 종료코드 0
   입력 정체성은 이제 확인하지만 그 입력의 결과라고 읽을 실제 구조는 확인하지 않습니다. 이후 판독기가 옛 에너지와 교체된 구조를 연결할 수 있습니다.
   최소 수정: 완료 시 실제로 저장한 구조의 해시를 기록하고, 재개 생략과 결과 검사에서 파일 존재·판독 가능·해시 일치를 같은 함수로 확인하세요. 불일치하면 거부하거나 명시적으로 재실행해야 합니다.
3. P1 · 포논 전 — 캐시만 비우면 정체성과 힘이 서로 다른 계산에 속할 수 있습니다.
   uma_phonon.py:118
   정체성 검사는 캐시가 비어 있지 않을 때만 수행하고, 기존 정체성 파일은 새로 쓰지 않습니다.
   합성 퍼텐셜로 다음을 재현했습니다.
   - 안장점 A 계산 → UNSTABLE
   - 힘 캐시만 비우고 정체성 파일은 유지
   - 같은 출력 접두어로 최소점 B 계산 → STABLE
   - 다시 A 계산 → 거짓 STABLE
   마지막 계산은 입력 힘 확인 1회만 하고 B의 캐시를 사용했습니다. 두 구조 모두 입력 힘 조건을 통과하는 정지점입니다.
   최소 수정: 정체성 파일이 있으면 캐시의 비어 있음과 관계없이 대조하세요. 또는 비어 있는 캐시를 새로 시작할 때 정체성도 함께 갱신해야 합니다. A 정체성＋B 힘 상태를 허용하면 안 됩니다.
4. P1 · 골격 MD 전 — B 중심은 세지만 B에 붙은 S·O의 분류는 아직 고치지 않았습니다.
   framework_site_census.py:130
   결합 음이온을 찾는 경로는 여전히 P만 찾습니다. B는 자유 원자 목록에 추가됐지만, B에 붙은 S는 자유 S로 남습니다.
   B–S 거리 2.0 Å를 유지하는 BS₃ 강체 회전에서 사건 3개, 동일한 좌표의 PS₃에서는 0개가 나왔습니다. 현재 구현은 두 중심의 다면체 회전을 다르게 셉니다.
   최소 수정: B 중심 이동과 B 결합 음이온의 이탈을 구분하고, 선언한 B–S/B–O 기준으로 결합 음이온을 자유 집합에서 제외하세요. 강체 회전 음성시험과 실제 결합 이탈 양성시험이 필요합니다. 이 항목 때문에 1단계 UMA까지 막을 필요는 없습니다.
P2와 실행 계약의 남은 항목은 다음과 같습니다.
- 생성 manifest가 부모–자식 짝을 검증하지 않습니다.
  b2o3_enumerate.py:907
  실제 생성물에서 부모 B가 [30,92]인 항목에 다른 부모의 자식 B [30,31]을 넣고 자식 해시를 갱신해도 verify=[]였습니다. li_candidates.json 삭제·손상도 검증을 통과했습니다.
  최소 수정: 부모와 자식은 선언한 S→O 치환 외에 원소·좌표·셀·B/Li 배치가 같아야 한다는 검사를 추가하고, 후보 보고서의 기록된 해시도 실제로 읽으세요. 정상 생성한 이번 135구조 자체에서는 이 불일치가 없었습니다.
- 대기 후 실행하는 입력은 제출 때 검증한 입력과 다시 대조하지 않습니다.
  run_uma_kgy.sh:255
  제출 검사 후 후보를 바꾸면 큐는 변경된 파일을 읽습니다. 실행 시 run_identity는 변경된 파일을 기록할 뿐, 승인된 manifest와 같았는지는 확인하지 않습니다.
  최소 수정: 입력·소스를 고정된 사본으로 실행하거나, 대기가 끝난 직후 제출 때의 해시를 재검사하세요.
- 신·구 census를 섞으면 이미 관측한 B 사건이 집계에서 사라집니다.
  framework_site_census.py:434
  B 사건 1개가 있는 새 기록에 B 미측정인 옛 기록 하나를 추가하면 B 집계 전체를 제외합니다. 그 뒤 봉인 문장은 **“골격은 … 자리를 떠나지 않았다”**가 됩니다.
  최소 수정: 혼합 집계를 거부하거나 관측 범위별로 분리하세요. 미측정 표시는 필요하지만 이미 관측한 사건을 없애는 근거가 되지는 않습니다.
- 끝 꼴과 G3의 판독 계약이 아직 하나로 정해지지 않았습니다.
  프로토콜:101, G3:107
  M=6, 수렴 5개, 그중 끝 꼴 변경 2개면 G1은 통과합니다. 그런데 G3를 2/6으로 읽으면 섞임이 아니고, 2/5로 읽으면 섞임입니다. 끝 꼴도 가교 O·혼합 배위·미결합 O를 어떻게 분류할지 정해져 있지 않습니다.
  최소 수정: 분모·결합 기준·경계 부등호·미분류 처리·구조별 꼴 판정을 유효 설정에 넣고 판독기에 연결하세요. 이는 아직 없는 구현의 결함을 추측한 것이 아니라, 결과 전에 닫아야 할 명세의 빈칸입니다.
- 새 개정 결정이 옛 k 재개 행동을 다시 참조합니다.
  decisions.json:11794의 “카드 4b 재개 규칙 그대로”는 옛 2×2×1 재계산을 가리킵니다. 새 개정은 4×2×1입니다.
  최소 수정: proposed 개정의 참조를 새 9_DFT 규칙으로 바꾸세요. 봉인된 옛 문서를 수정할 필요는 없습니다. DFT 전 조건입니다.
Windows selftest의 열린 md.log 정리 오류도 P2입니다. 로그를 예외 경로에서도 닫으면 됩니다. Linux 생산 실행에서 같은 실패가 난다고 확인한 것은 아닙니다.

P3로는 두 문구만 정리하면 됩니다. 파일럿 긴 결과의 제외는 **“선택된 \(t_a\)보다 긴 결과를 제외”**로 쓰고, 비용표의 k 탐침 추가 횟수는 2→3으로 맞추세요.

Q1. DU P1 1–9의 닫힘
DU 항목	이번 판정
1. Ewald 계수	해제. α=0.25/0.5/0.75에서 −2.93084839 eV로 일치했고 독립 계산과도 맞았습니다.
2. Li 공공 후보	제한된 생성법으로 해제. spglib 경로 제거, void 방법 명시, 실제 host 거리 검사 확인.
3. 반올림 중복 제거	해제. 45개 B 쌍 전부, 가족별 45개 확인.
4. 어닐 재개·실패	부분 해제. 입력·시간·seed 변경과 failed 재시도는 고쳤지만 위 P1-1·2가 남습니다.
5. 가족별 k 대비	설계상 해제. 세 가족·두 격자·세 발동이 맞습니다. 원장 참조는 정리해야 합니다.
6. 후처리 구조 계보	설계상 해제. 갈래 b는 타당합니다. 실제 산출물 결속은 판독기에서 확인해야 합니다.
7. 포논 캐시	부분 해제. 직접 입력 변경은 잡지만 빈 캐시＋옛 정체성 전환은 놓칩니다.
8. 허수 모드 판정	해제. 비병진 −20 cm⁻¹가 SOFT로 판정됩니다.
9. 골격 거리·결측	원래 반례 해제. 2.90 Å는 사건 0, NaN·음의 간격은 invalid. B 확장에는 위 문제가 남습니다.


과거 영향 기록은 옛 census JSON의 재집계와 원격 원궤적 재판독을 구분해서 읽어야 합니다. 전자가 같다는 사실로 새 B 결합 규칙까지 과거 결론이 검증됐다고 확장하면 안 됩니다. 닫힌 Nd 트랙을 다시 열라는 요구는 없습니다.

Q2. void 후보 50개와 거리 문턱 — 조건부 찬성입니다.

현재 선언한 초기 구조 생성법에는 적절합니다. 실제 선택 구조의 최소 Li–Li는 2.1084 Å, 후보–P 최소 거리는 2.6097 Å였습니다. 현재 사용한 거리 문턱 안에서는 27-image와 ASE 독립 최소상 계산이 일치했습니다.

후보 50개끼리 모두 2.1 Å 이상일 필요는 없습니다. 실제로 함께 선택하는 Li 4개가 쌍 제약을 지켜야 하며, 그 검사는 작동합니다.

다만 “가능한 Li 공공을 모두 찾았다” 또는 “물리적으로 완전한 후보 집합”이라는 뜻은 아닙니다. 이번 제한된 탐색을 위해 문턱을 다시 맞추거나 생산 계산을 추가할 필요는 없습니다.

Q3. 전수 Ewald 최저 초기점 하나 — 이번 범위에서는 찬성입니다.

검증한 후보 집합에서 거리 제약을 만족하는 Li₄ 조합은 208,250개이고, 현재 경로는 그 안의 최저를 선택합니다. 욕심 채우기보다 명확한 개선입니다.

상위 여러 초기점을 추가해야만 이번 탐색을 시작할 수 있는 것은 아닙니다. 대신 결론은 **“선언한 초기점 생성·탐색 절차에서 얻은 결과”**로 제한하세요. 어닐이 Li 초기점 의존성을 없앴다는 주장은 여전히 할 수 없습니다.

Q4. 전자구조와 안정성이 다른 구조인 갈래 b — 찬성입니다.

다음 표현이면 됩니다.
“에너지 비교에서 선택된 시작 가족의 대표 구조를 DFT로 이완하여 띠틈을 계산했다. 골격 안정성은 별도로 선정한 UMA 구조 세 개에서 검사했다.”

**“승자 가족에서 선택한 대표 구조의 띠틈”**은 가능하지만, 설명 없이 **“승자 가족의 띠틈”**이라고 일반화하는 것은 피하세요. 두 검사가 같은 원자구조를 검증한 것처럼 연결해서도 안 됩니다. 각 구조의 부모·자식 해시와 역할을 함께 제시하면 추가 DFT 이완 없이도 정직하게 보고할 수 있습니다.

Q5. 탐침·승자·k·EOS — 방향은 맞고, 판독기에서 네 가지를 닫아야 합니다.
- 파일럿은 하나의 연속 100 ps 궤적에서 20/50/100 ps 구조를 복사해 각각 이완해야 합니다. 세 독립 런이나 중간 이완 후 이어 돌린 궤적으로 바꾸면 다른 절차입니다. 현재 md.traj는 이 구현에 필요한 시점을 보존할 수 있습니다.
- 세 끝점 모두 구조·유한 에너지·수렴이 확인돼야 길이를 결정해야 합니다. 하나가 없거나 미수렴이면 파일럿 미완료로 남겨야 합니다.
- 가족 탈락, 기준 가족 결측, 끝 꼴 미분류 때 승자와 짝 비교를 어떻게 보류할지 정해야 합니다.
- EOS의 B 범위는 각 가족에 독립적으로 적용한 경우도 확인해야 합니다. 공통 B 하나를 움직이면 보정이 인위적으로 상쇄될 수 있습니다.
마지막 항목의 산술 예로, 같은 \(P=2\) GPa·\(V=2436.33\) Å³에서 보정은 B 범위에 따라 약 −1.402∼−0.936 eV입니다. 공통 B에서는 유지되는 0.15 eV 차가 가족별 B를 독립적으로 허용하면 뒤집힐 수 있습니다. 추가 EOS 계산 요구가 아니라 판독기에 넣을 음성시험입니다.

Q6. 판독기 전에 1단계를 시작해도 되나 — 지금은 안 됩니다.

프로토콜:49 자체가 판독기와 음성시험을 실행 전 조건으로 정했습니다. 이번에는 그 조건을 유지하는 실질적 이유도 있습니다. 끝 꼴·G3 분모·결측 처리가 결과를 보기 전에 확정돼야 합니다.

생성·manifest 검증·합성시험은 계속할 수 있습니다. 생산 UMA 이완 거름부터는 판독기를 먼저 갖추세요.

Q7. 전역 관측창 문구 — 개정을 권합니다.

봉인 원문은 보존하고, 새 개정으로 “그보다 높은 장벽은 원래 못 본다”를 대체하는 것이 맞습니다.

가정한 단일 반응 기회와 일정한 사건률 아래에서:
- 기대 사건 1에 해당하는 장벽: 0.77446 eV
- 그때 한 번 이상 볼 확률: 63.2%
- 95% 검출에 해당하는 장벽: 0.67991 eV
이는 딱 잘리는 관측 한계가 아닙니다. 같은 모형에서 0.77446 eV보다 **0.10 eV 높은 장벽도 검출확률이 약 26.9%**입니다. 시도빈도·반응 기회 수·정상성 가정을 함께 적어야 합니다. NIST의 일정 사건률 모형

1단계 실행 전 최소 해제조건은 네 묶음입니다.
1. 큐 실패 전파: 실행·검사의 실제 종료코드를 보존하고 nonzero를 전달할 것.
2. 실물 결속: 완료 구조의 존재·해시를 재개와 결과 검사에서 확인하고, 대기 후 입력도 승인된 사본과 대조할 것.
3. 생성 짝 검증: 부모–자식의 허용된 S→O 변경만 인정하고 후보 보고서 해시도 검사할 것.
4. 판독기＋음성시험: G1–G4, 공통 성공 짝, 끝 꼴·G3 분모·결측 처리, 연속 파일럿 세 끝점, 승자–차저를 구현한 뒤 유효 개정을 비준할 것.
포논 캐시와 B 결합 분류는 각각 포논·골격 MD 전에 고치면 됩니다. 이 둘을 이유로 위 네 조건을 충족한 UMA 1단계까지 계속 막지는 않겠습니다.

재현 자료: [검증 기록](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_DV_20261109/VERIFICATION.json) · [실행·포논 반례](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_DV_20261109/dv_execution/probe_results.json) · [골격 반례](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_DV_20261109/framework_probe_results.json)

---

## 부록 A — VERIFICATION.json (사용자 붙여넣기 · 원문)

```json
{
  "target_commit": "ad4f41b8c79920947e7f8b0b52b72a129052a537",
  "original_repo_modified": false,
  "snapshot_files_checked": 18,
  "changed_snapshot_paths": [],
  "production_UMA_DFT_MD_executed": false,
  "scope": "Read-only snapshot review; geometry/Ewald generation, synthetic calculators, local synthetic trajectories, shell mocks.",
  "limitations": [
    "No original remote production trajectory replay.",
    "Native Windows anneal selftest raises WinError32 when cleaning open md.log; assertions retested with temporary-folder retention only.",
    "Bash mock tested GNU Bash5.3.15, not target server shell.",
    "No production GPU, fairchem checkpoint, QE or Linux launch verified."
  ],
  "artifacts": {
    "framework_probe_results.json": "305e9ca77f368ea6c930a9fbed59123dc6835a474fbe525c1fad92a602f8b454",
    "framework_site_census_selftest.log": "278143577b86a36e463ed357526a1eb43206cf65dee3ee5cd526a14517059326",
    "msd_diffusive_check_selftest.log": "4012ee74b029da4713b71b179626410e846c96541deb9ca82dc02501ee456d60",
    "dv_execution/probe_results.json": "38910097a37c9fbef73f8e5d9a3107cee53cbfd0687fb3db9a075eead13a98f7",
    "dv_execution/run_anneal.py.selftest.log": "542e1500de9ceae2c34a01a71f396e5a16a9daff630f62a7dfbe947d938d6600",
    "dv_execution/run_anneal.keep_tmp.selftest.log": "6f5ca0ce4fb01207b4bb28f63f81d48d0ea9793b1db7a9d51a6af98c3230e86d",
    "dv_execution/uma_phonon.py.selftest.log": "02c3ddab87f1181338c0e022f69a04d508f9f9a14e22350a7283c4efb9c97ddd",
    "dv_enumeration/probe_results.json": "b3a6cfb68545eda680f2dc8ee4414da21a6e205e4752439452bcec892103b6a4",
    "dv_enumeration/manifest_pair_result.json": "172896705e938ed3155a52704ab1c897a9bf38ef2d208f23e5488453f988d047",
    "dv_design/design_fixtures.json": "f63e6698bc6b6ce3d5eaacb93b1fb6c7414b9570a01c43debef43830c8412eb8"
  }
}
```

## 부록 B — dv_execution/probe_results.json (사용자 붙여넣기 · 원문)

```json
{
  "ase_version": "3.29.0",
  "scope": "DV review only: synthetic calculators, real ASE, zero production UMA/DFT/MD.",
  "artifacts": "C:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DV_20261109\\dv_execution\\artifacts\\a4bc7645cb80",
  "du_final_step_fixed": {
    "steps": 1,
    "fmax": 0.049599,
    "converged": true
  },
  "du_resume_fixed": {
    "time_ps": "⛔ one: 같은 이름의 기존 기록과 입력 · 설정이 다르다 (다른 칸 ['stage', 'time_ps']) — 새 --out 을 쓰라 (같은 폴더에 섞지 않는다)",
    "seed": "⛔ one: 같은 이름의 기존 기록과 입력 · 설정이 다르다 (다른 칸 ['seed']) — 새 --out 을 쓰라 (같은 폴더에 섞지 않는다)",
    "relax_fmax": "⛔ one: 같은 이름의 기존 기록과 입력 · 설정이 다르다 (다른 칸 ['relax_fmax']) — 새 --out 을 쓰라 (같은 폴더에 섞지 않는다)",
    "coordinates": "⛔ one: 같은 이름의 기존 기록과 입력 · 설정이 다르다 (다른 칸 ['input_file_sha256', 'input_struct']) — 새 --out 을 쓰라 (같은 폴더에 섞지 않는다)"
  },
  "du_failure_fixed": {
    "first": [
      1,
      0
    ],
    "retry": [
      0,
      1
    ]
  },
  "output_replaced_passes": {
    "stored_struct_hash": "f80cad727d7265ae",
    "actual_struct_hash": "0ed255e8ecaf1374",
    "check_problems": [],
    "resume_rc_nran": [
      0,
      0
    ],
    "actual_symbols": [
      "He"
    ]
  },
  "output_missing_passes": {
    "output_exists": false,
    "check_problems": [],
    "resume_rc_nran": [
      0,
      0
    ]
  },
  "phonon_cache_reset_identity_mismatch": {
    "first_A_verdict": "STABLE",
    "B_fresh_verdict": "UNSTABLE",
    "A_rerun_verdict": "UNSTABLE",
    "force_calls": [
      13,
      13,
      1
    ],
    "old_identity": "309dd0f3d548682f6b9d8cec5bd08404d469246996169b5597c491f8cf36cbc9",
    "sidecar_after_B": "309dd0f3d548682f6b9d8cec5bd08404d469246996169b5597c491f8cf36cbc9",
    "report_B_identity": "801474a7f76f15499020915ecba57372777be75c12d50e3f4a1fd5dc35c46de6",
    "min_A_original": 734.539,
    "min_A_rerun": -734.392
  },
  "phonon_false_stable_after_cache_reset": {
    "saddle_original": "UNSTABLE",
    "minimum_regenerated": "STABLE",
    "saddle_rerun": "STABLE",
    "saddle_rerun_force_calls": 1
  },
  "du_soft_fixed": true
}
```

## 부록 C — framework_probe_results.json (사용자 붙여넣기 · 내용 그대로 · 공백만 접음)

```json
{"old_skew_counterexample":{"n_frames":250,"dt_ps":0.1,"total_ps":25.0,"min_frames":100,"thresholds":{"o_bond_A":2.0,"s_bond_A":2.6,"o_escape_A":2.5,"s_escape_A":3.0,"disp_escape_A":2.0,"min_ps":10.0},"n_framework":2,"n_P_bonded_anions":1,"n_free":1,"verdict":"framework_rigid","free_elems_tracked":["B","Cl","O","P","S"],"n_events":0,"by_elem":{},"events":[],"margin_max_by_elem_kind":{"S/P-bonded":{"max_A":2.9,"escape_A":3.0,"atom":1},"P/free":{"max_A":0.2499999999999999,"escape_A":2.0,"atom":0}},"⛔":"이 판정은 '자리를 떠났나' 만 본다. β 경보는 지우지 않는다 — 결과 파일에 병기한다."},"old_nan_counterexample":{"n_frames":250,"dt_ps":0.1,"total_ps":25.0,"verdict":"invalid","invalid_reasons":["좌표에 NaN/inf — 프레임 [50, 51, 52, 53, 54] … (200 개)"],"n_events":null,"by_elem":{},"events":[],"margin_max_by_elem_kind":{},"⛔":"invalid 는 '사건 0' 이 아니다 — 판정 불가다. 집계 (--aggregate) 는 invalid 런이 있으면 멈춘다."},"old_negative_dt_counterexample":{"n_frames":250,"dt_ps":-0.1,"total_ps":-25.0,"verdict":"invalid","invalid_reasons":["프레임 간격 -0.1 — 양의 유한값이어야 한다"],"n_events":null,"by_elem":{},"events":[],"margin_max_by_elem_kind":{},"⛔":"invalid 는 '사건 0' 이 아니다 — 판정 불가다. 집계 (--aggregate) 는 invalid 런이 있으면 멈춘다."},"rigid_BS3_rotation":{"n_frames":250,"dt_ps":0.1,"total_ps":25.0,"min_frames":100,"thresholds":{"o_bond_A":2.0,"s_bond_A":2.6,"o_escape_A":2.5,"s_escape_A":3.0,"disp_escape_A":2.0,"min_ps":10.0},"n_framework":4,"n_P_bonded_anions":0,"n_free":4,"verdict":"framework_mobile","free_elems_tracked":["B","Cl","O","P","S"],"n_events":3,"by_elem":{"S":{"events":3,"n_atoms":3,"atoms":[1,2,3]}},"events":[{"kind":"free","elem":"S","atom":1,"start_ps":1.7000000000000002,"length_ps":23.3,"peak_disp_A":4.0},{"kind":"free","elem":"S","atom":2,"start_ps":1.7000000000000002,"length_ps":23.3,"peak_disp_A":4.0},{"kind":"free","elem":"S","atom":3,"start_ps":1.7000000000000002,"length_ps":23.3,"peak_disp_A":3.999999999999999}],"margin_max_by_elem_kind":{"B/free":{"max_A":1.3322676295501878e-15,"escape_A":2.0,"atom":0},"S/free":{"max_A":4.0,"escape_A":2.0,"atom":1}},"⛔":"이 판정은 '자리를 떠났나' 만 본다. β 경보는 지우지 않는다 — 결과 파일에 병기한다."},"rigid_PS3_rotation_control":{"n_frames":250,"dt_ps":0.1,"total_ps":25.0,"min_frames":100,"thresholds":{"o_bond_A":2.0,"s_bond_A":2.6,"o_escape_A":2.5,"s_escape_A":3.0,"disp_escape_A":2.0,"min_ps":10.0},"n_framework":4,"n_P_bonded_anions":3,"n_free":1,"verdict":"framework_rigid","free_elems_tracked":["B","Cl","O","P","S"],"n_events":0,"by_elem":{},"events":[],"margin_max_by_elem_kind":{"S/P-bonded":{"max_A":2.000000000000001,"escape_A":3.0,"atom":1},"P/free":{"max_A":1.3322676295501878e-15,"escape_A":2.0,"atom":0}},"⛔":"이 판정은 '자리를 떠났나' 만 본다. β 경보는 지우지 않는다 — 결과 파일에 병기한다."},"modern_B_only":{"schema":"framework_event_rate_aggregate/v1","group_definition":{"P_center":"census kind=free · elem=P","S_free":"census kind=free · elem=S","Cl":"census kind=free · elem=Cl","P-bonded_S":"census kind=P-bonded · elem=S","P-bonded_O":"census kind=P-bonded · elem=O","free_O":"census kind=free · elem=O","B_center":"census kind=free · elem=B"},"group_n_card":{"P_center":32,"S_free":48,"Cl":64},"runs":[{"seed":1,"T_K":600,"path":"C:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DV_20261109\\framework_fixture\\modern.json","n_frames":4000,"dt_ps":0.1,"total_ps":400.0,"n_free":1,"n_P_bonded_anions":0,"verdict":"framework_mobile","groups":{"P_center":{"N_ev":0,"N_at":0,"t1_ps":null},"S_free":{"N_ev":0,"N_at":0,"t1_ps":null},"Cl":{"N_ev":0,"N_at":0,"t1_ps":null},"P-bonded_S":{"N_ev":0,"N_at":0,"t1_ps":null},"P-bonded_O":{"N_ev":0,"N_at":0,"t1_ps":null},"free_O":{"N_ev":0,"N_at":0,"t1_ps":null},"B_center":{"N_ev":1,"N_at":1,"t1_ps":10}}}],"by_T":{"600":{"n_runs":1,"seeds":[1],"exposure_ns":0.4,"groups":{"P_center":{"sum_N_ev":0,"rate_per_ns_cell":0.0,"ci95":{"lo":0.0,"hi":7.489330683884973,"kind":"one-sided 95 % upper (n = 0)"},"k_runs":0,"k_of":1,"t1_median_ps":"> 400","sum_N_at":0,"per_run_N_ev":[0],"dispersion_index_var_over_mean":null,"moved_atom_fraction":0.0},"S_free":{"sum_N_ev":0,"rate_per_ns_cell":0.0,"ci95":{"lo":0.0,"hi":7.489330683884973,"kind":"one-sided 95 % upper (n = 0)"},"k_runs":0,"k_of":1,"t1_median_ps":"> 400","sum_N_at":0,"per_run_N_ev":[0],"dispersion_index_var_over_mean":null,"moved_atom_fraction":0.0},"Cl":{"sum_N_ev":0,"rate_per_ns_cell":0.0,"ci95":{"lo":0.0,"hi":7.489330683884973,"kind":"one-sided 95 % upper (n = 0)"},"k_runs":0,"k_of":1,"t1_median_ps":"> 400","sum_N_at":0,"per_run_N_ev":[0],"dispersion_index_var_over_mean":null,"moved_atom_fraction":0.0},"P-bonded_S":{"sum_N_ev":0,"rate_per_ns_cell":0.0,"ci95":{"lo":0.0,"hi":7.489330683884973,"kind":"one-sided 95 % upper (n = 0)"},"k_runs":0,"k_of":1,"t1_median_ps":"> 400","sum_N_at":0,"per_run_N_ev":[0],"dispersion_index_var_over_mean":null},"P-bonded_O":{"sum_N_ev":0,"rate_per_ns_cell":0.0,"ci95":{"lo":0.0,"hi":7.489330683884973,"kind":"one-sided 95 % upper (n = 0)"},"k_runs":0,"k_of":1,"t1_median_ps":"> 400","sum_N_at":0,"per_run_N_ev":[0],"dispersion_index_var_over_mean":null},"free_O":{"sum_N_ev":0,"rate_per_ns_cell":0.0,"ci95":{"lo":0.0,"hi":7.489330683884973,"kind":"one-sided 95 % upper (n = 0)"},"k_runs":0,"k_of":1,"t1_median_ps":"> 400","sum_N_at":0,"per_run_N_ev":[0],"dispersion_index_var_over_mean":null},"B_center":{"sum_N_ev":1,"rate_per_ns_cell":2.5,"ci95":{"lo":0.06329451996072469,"hi":13.929108477347244,"kind":"Garwood two-sided 95 %"},"k_runs":1,"k_of":1,"t1_median_ps":10.0,"sum_N_at":1,"per_run_N_ev":[1],"dispersion_index_var_over_mean":null}}}},"apparent_activation":{"P_center":{"fitted":false,"why":"사건 ≥ 10 인 온도 0 개 < 2 — 카드 조건 미충족 · 맞추지 않는다"},"S_free":{"fitted":false,"why":"사건 ≥ 10 인 온도 0 개 < 2 — 카드 조건 미충족 · 맞추지 않는다"},"Cl":{"fitted":false,"why":"사건 ≥ 10 인 온도 0 개 < 2 — 카드 조건 미충족 · 맞추지 않는다"}},"sealed_sentences":["600 K · P_center: 사건 0 (1 × 400 ps · 단측 95 % 상한 ≈ 7.49 /ns/셀).","600 K · S_free: 사건 0 (1 × 400 ps · 단측 95 % 상한 ≈ 7.49 /ns/셀).","600 K · Cl: 사건 0 (1 × 400 ps · 단측 95 % 상한 ≈ 7.49 /ns/셀)."],"⚠":"census 는 P 중심 규칙 — BS₃ 의 S 는 '자유 S' 로 분류된다 (카드 결과와 같이 적는다) · B 중심은 2026-11-09 부터 센다 (B_center)","B_center":"센다 (모든 census 파일이 B 를 봤다)"},"mixed_legacy_modern_B":{"schema":"framework_event_rate_aggregate/v1","group_definition":{"P_center":"census kind=free · elem=P","S_free":"census kind=free · elem=S","Cl":"census kind=free · elem=Cl","P-bonded_S":"census kind=P-bonded · elem=S","P-bonded_O":"census kind=P-bonded · elem=O","free_O":"census kind=free · elem=O"},"group_n_card":{"P_center":32,"S_free":48,"Cl":64},"runs":[{"seed":1,"T_K":600,"path":"C:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DV_20261109\\framework_fixture\\modern.json","n_frames":4000,"dt_ps":0.1,"total_ps":400.0,"n_free":1,"n_P_bonded_anions":0,"verdict":"framework_mobile","groups":{"P_center":{"N_ev":0,"N_at":0,"t1_ps":null},"S_free":{"N_ev":0,"N_at":0,"t1_ps":null},"Cl":{"N_ev":0,"N_at":0,"t1_ps":null},"P-bonded_S":{"N_ev":0,"N_at":0,"t1_ps":null},"P-bonded_O":{"N_ev":0,"N_at":0,"t1_ps":null},"free_O":{"N_ev":0,"N_at":0,"t1_ps":null}}},{"seed":2,"T_K":600,"path":"C:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DV_20261109\\framework_fixture\\legacy.json","n_frames":4000,"dt_ps":0.1,"total_ps":400.0,"n_free":1,"n_P_bonded_anions":0,"verdict":"framework_rigid","groups":{"P_center":{"N_ev":0,"N_at":0,"t1_ps":null},"S_free":{"N_ev":0,"N_at":0,"t1_ps":null},"Cl":{"N_ev":0,"N_at":0,"t1_ps":null},"P-bonded_S":{"N_ev":0,"N_at":0,"t1_ps":null},"P-bonded_O":{"N_ev":0,"N_at":0,"t1_ps":null},"free_O":{"N_ev":0,"N_at":0,"t1_ps":null}}}],"by_T":{"600":{"n_runs":2,"seeds":[1,2],"exposure_ns":0.8,"groups":{"P_center":{"sum_N_ev":0,"rate_per_ns_cell":0.0,"ci95":{"lo":0.0,"hi":3.7446653419424867,"kind":"one-sided 95 % upper (n = 0)"},"k_runs":0,"k_of":2,"t1_median_ps":"> 400","sum_N_at":0,"per_run_N_ev":[0,0],"dispersion_index_var_over_mean":null,"moved_atom_fraction":0.0},"S_free":{"sum_N_ev":0,"rate_per_ns_cell":0.0,"ci95":{"lo":0.0,"hi":3.7446653419424867,"kind":"one-sided 95 % upper (n = 0)"},"k_runs":0,"k_of":2,"t1_median_ps":"> 400","sum_N_at":0,"per_run_N_ev":[0,0],"dispersion_index_var_over_mean":null,"moved_atom_fraction":0.0},"Cl":{"sum_N_ev":0,"rate_per_ns_cell":0.0,"ci95":{"lo":0.0,"hi":3.7446653419424867,"kind":"one-sided 95 % upper (n = 0)"},"k_runs":0,"k_of":2,"t1_median_ps":"> 400","sum_N_at":0,"per_run_N_ev":[0,0],"dispersion_index_var_over_mean":null,"moved_atom_fraction":0.0},"P-bonded_S":{"sum_N_ev":0,"rate_per_ns_cell":0.0,"ci95":{"lo":0.0,"hi":3.7446653419424867,"kind":"one-sided 95 % upper (n = 0)"},"k_runs":0,"k_of":2,"t1_median_ps":"> 400","sum_N_at":0,"per_run_N_ev":[0,0],"dispersion_index_var_over_mean":null},"P-bonded_O":{"sum_N_ev":0,"rate_per_ns_cell":0.0,"ci95":{"lo":0.0,"hi":3.7446653419424867,"kind":"one-sided 95 % upper (n = 0)"},"k_runs":0,"k_of":2,"t1_median_ps":"> 400","sum_N_at":0,"per_run_N_ev":[0,0],"dispersion_index_var_over_mean":null},"free_O":{"sum_N_ev":0,"rate_per_ns_cell":0.0,"ci95":{"lo":0.0,"hi":3.7446653419424867,"kind":"one-sided 95 % upper (n = 0)"},"k_runs":0,"k_of":2,"t1_median_ps":"> 400","sum_N_at":0,"per_run_N_ev":[0,0],"dispersion_index_var_over_mean":null}}}},"apparent_activation":{"P_center":{"fitted":false,"why":"사건 ≥ 10 인 온도 0 개 < 2 — 카드 조건 미충족 · 맞추지 않는다"},"S_free":{"fitted":false,"why":"사건 ≥ 10 인 온도 0 개 < 2 — 카드 조건 미충족 · 맞추지 않는다"},"Cl":{"fitted":false,"why":"사건 ≥ 10 인 온도 0 개 < 2 — 카드 조건 미충족 · 맞추지 않는다"}},"sealed_sentences":["이 셀·이 프로토콜에서 600 K 의 골격은 2 × 400 ps 동안 자리를 떠나지 않았다 (사건 빈도 단측 95 % 상한 ≈ 3.7 /ns/셀)."],"⚠":"census 는 P 중심 규칙 — BS₃ 의 S 는 '자유 S' 로 분류된다 (카드 결과와 같이 적는다) · B 중심은 2026-11-09 부터 센다 (B_center)","B_center":"미측정 — B 를 안 본 옛 census 파일이 섞였다 (0 으로 적지 않는다 · 2026-11-09)"}}
```
