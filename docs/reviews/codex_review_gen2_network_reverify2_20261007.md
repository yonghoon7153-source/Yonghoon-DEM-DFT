# 접촉망 세대 2 재검증 2 — 기존 반례는 막혔지만 새 실행 봉인은 HOLD

> 반입 표지 (10-07 · 메인 세션): 1저자가 채팅으로 붙여 준 Codex 판정문 원문 그대로 (요약 글머리 포함).  Codex 증거 ZIP (`codex_gen2_network_reverify2_20261007.zip` — 1저자 Windows Codex 작업 공간) 은 아직 리포에 없다 (받으면 `docs/reviews/codex_gen2_network_reverify2_evidence_20261007/` 로 반입).  함께 올린 ZIP 4 개 (verify_evidence · CLAUDE · gen2_design_20261006 · reviews · 10-06 20:36) 는 Codex 에 보낸 검토 묶음 (입력) 이다.

1저자 요약 (채팅): 재검증 완료했습니다. 핀은 `9d25757dc`입니다.
HOLD 유지 — 새 P1 없음, P2 네 건입니다.

* 세대·입력 지문을 삭제하면 감사가 우회됩니다.
* 새 다시 읽기 검사기가 0케이스를 PASS로 냅니다.
* 실제 의존 모듈 `fracture_model.py`가 봉인에서 빠졌습니다.
* CF 차원값을 약 2배로 바꿔도 게시·인계가 통과합니다.

기존 바꿔치기 반례는 막혔고, 정직한 CF 실패에서는 FULL이 유지됐습니다. 판정문에는 기존 결함의 닫힘과 발사 승인을 분리했습니다. 194 배치는 실행하지 않았습니다.

---

검토일: 2026-10-07 · 브랜치 `claude/stoic-knuth-NObVQ` · 고정 핀 **`9d25757dcdbd127731043c5d2293ae47e0202242`**.

요청서 반입 이력으로 핀을 정했다. 앞 코드 커밋 `c70b02c7b`나 이동하는 브랜치 끝을 핀으로 쓰지 않았다. 요청서 첨부는 커밋본과 바이트 동일하다. 등록문 첨부는 커밋본과 **Python 실행 경로를 찾는 두 줄만 다르며**, 수치·봉인·관문은 같다. 두 버전 모두 검토했다.

**새 P1은 이번 검증에서 발견하지 않았다. 새 P2 네 건, P3 한 건이다. 새 194 생산 및 v1.3 최종 인계는 HOLD.** 기존 수치 교정을 되돌리거나, 이미 검증한 v1.2 수치를 철회하라는 뜻은 아니다.

저장소·생산 코드·원장·Git 상태를 바꾸지 않았다. 고정 소스 사본에서 회귀, 합성 접촉망, 실제 생산자 CLI→후보 검사→게시→인계를 시험했다. **194 캠페인, DEM/MPM, WSL 실덤프 사전 점검은 실행하지 않았다.** 아래 실패 주입은 제어된 소프트웨어 시험이며 실침대에서 같은 실패가 발생했다는 관측이 아니다.

## 1. Q1 — 닫힘 범위

| 항목 | 판정 | 근거·한정 |
|---|---|---|
| G2RR-01 도장↔레코드 | **닫힘** | 실제 게시 폴더의 unknown·null·legacy·부분 결손·역사 모양 위장 변이를 인계가 거부. 정상 g2는 통과. 역사 스키마 검증 회귀도 통과한다. 새 실행기 선언 보증은 아래 별건이다. |
| G2RR-02 증서↔가지·역할·발행값 | **원래 반례 닫힘, 확장된 결합 보증은 부분** | CF→FULL, H12→H0, 증서 삭제·보존 위반은 실제 게시 전에 거부. 그러나 CF 증서 σ₀와 부모 σ₀의 연결이 빠져 있다(G2RR2-04). |
| G2RR-03 v1.2 검산기의 등록 큐 | **닫힘** | 원래 검산기 CLI: 정상 194행 rc=0; 빈 큐·plan 삭제·195행 중복 모두 rc=1. 새 g2 다시 읽기 도구의 빈 계획 통과는 별도 결함(G2RR2-02)이다. |
| G2R-02 | **부분** | 도장 대조는 닫혔다. 새 manifest 선언을 지우면 옛 형식으로 우회하는 실행 봉인 문제가 남는다(G2RR2-01). |
| G2R-03 | **풀이 교정·FULL 바꿔치기 방지 닫힘 / 발행 가지 전체의 증서 연결 부분** | +100% 옛 수치 반례는 계속 회복. FULL의 가지·역할·q 연결은 닫혔다. 이를 CF 차원값까지 완결된 보증으로 확대하지 않는다. |
| GEN2-01 | **등록된 미계산 정책 유지** | 관통 Rc=0인 협착-only는 값 없음+사유. 단락 수축의 정확해를 구현했다는 뜻은 아니다. |
| 새 배치 봉인·실덤프 사전 점검 | **부분 / 실행 증거 대기** | 등록 해시들은 재계산과 일치. 그러나 아래 P2와 WSL 사전 점검 증거가 남는다. |

독립 재실행 결과:

- 정상 합성 사슬: H0 `q=0.00400538`, `I_bottom=0.0200268809166404`, `τ²=10.980805104698456`(무차원).
- `full_cert_from_cf`, `full_cert_from_h12`, `missing_full_cert`, `missing_cf_cert`, `cf_bad_conservation`, `missing_constr_cert`: **6/6 게시 failed**. 거부 후 활성 파일이 없어서 τ가 `missing_input`인 것은 예상 결과이지 별도 풀이 결함이 아니다.
- 도장 control만 인계 통과; 나머지 다섯 변이는 전부 거부.
- 참 G=15,000.5인 고대비 막다른 가지 반례: 첫 CG 증서 거부 후 직접해 사다리로 회복. 참 G=1.45인 별도 13점 시험의 최대 상대오차는 `1.6442660633053663e−7`. **1e−6 증서 문턱이 모든 망의 σ 상대오차 1e−6을 보장한다는 뜻은 아니다.**

재현: 검토 묶음 루트에서 `python probes/acceptance.py`, `python probes/adversarial.py`, `python probes/numerics.py`, `python probes/reread_extra.py`. 실제 관측은 동명 `evidence/*.json`에 보존했다.

## 2. G2RR2-01 · P2 — 새 manifest의 필수 증거 삭제가 옛 형식 면제로 바뀐다

**무너지는 주장:** “새 배치 기대 세대·입력 지문은 삭제해도 retry/audit가 막는다.” 모든 산출물을 일관되게 위조한 반례가 아니다. 새 코드 지문·시도 증거·generation_probe는 남긴 채 일부 선언만 지웠다.

위치:

- [run_network_194_parallel.py:351](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9d25757dcdbd127731043c5d2293ae47e0202242/scripts/run_network_194_parallel.py#L351): top과 seal 양쪽에 기대 세대 키가 없으면 무조건 옛 manifest로 분류.
- [같은 파일:397](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9d25757dcdbd127731043c5d2293ae47e0202242/scripts/run_network_194_parallel.py#L397): 감사의 manifest 검사도 같은 면제.
- [같은 파일:1658](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9d25757dcdbd127731043c5d2293ae47e0202242/scripts/run_network_194_parallel.py#L1658): 선언이 있어야 케이스별 레코드 세대를 읽는다.
- [같은 파일:1707](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9d25757dcdbd127731043c5d2293ae47e0202242/scripts/run_network_194_parallel.py#L1707): `input_digest`가 dict일 때만 재계산. 키 삭제·null이면 검사를 생략.

새 29파일 지문과 정상 시도 영수증을 갖춘 **합성 1케이스 ROOT**에서 실제 audit CLI를 호출했다. 실제 워커를 발사한 기록이라고 주장하지 않는다.

| 변이 | audit rc | 결과 |
|---|---:|---|
| 양성 control | 0 | SEALED 1, g2 1, 입력 지문 일치 |
| 수확 JSON의 atom SHA만 변경 | 1 | 입력 지문 차이 검출 |
| 같은 변경 + `input_digest` 삭제 | **0** | `input_problems=[]` |
| 같은 변경 + `input_digest=null` | **0** | 동일 |
| 케이스 dual을 옛 레코드 모양으로, 기대 세대 g2 유지 | 1 | inferred_legacy≠g2 검출 |
| 같은 옛 레코드 + top/seal의 기대 세대 두 키 삭제 | **0** | `generation_declared=false`; 케이스 세대 검사를 생략 |

마지막 manifest를 실제 `generation_gate()`에 넣으면 차단 사유도 `[]`다. **retry의 세대 관문 우회**를 입증한 것이며, 실제 retry/워커 발사를 수행한 것은 아니다. 현재 인계 CLI에 `--tau-batch-manifest`를 반드시 주면 선언 부재를 별도로 막는다. 따라서 이 반례만으로 옛 레코드가 최종 인계됐다고 확대하지 않는다.

**최소 수정:** 새 실행 스키마에서 세대·입력 지문·형식을 필수화하고 run/retry/audit/merge가 같은 자격 검사를 쓰게 한다. 역사 허용은 “필드가 없다”가 아니라 알려진 옛 형식·발사 출처와 결합한다. 새 `generation_probe`·29파일 봉인이 남은 모양을 역사 기록으로 추론하지 않는다. 사본 둘을 같은 JSON에 두는 것은 누락 검사이지 독립 증거가 아님도 명시한다.

**해결 증거:** 위 네 우회 입력 모두 비영 종료; 진짜 역사 ROOT는 역사 모드에서만 읽기 가능; 정상 g2·원래 한쪽 삭제 반례는 그대로 유지.

재현: `python probes/seal_paths.py`; `evidence/seal_paths.json`의 `audit`, 각 ROOT의 `audit.json`·`cli.log`.

## 3. G2RR2-02 · P2 — g2 다시 읽기가 0케이스를 전부 PASS로 보고한다

**무너지는 주장:** “다시 읽기 rc=0이면 계획 전체 ID·증서·값을 검토했다.” G2RR-03을 고친 v1.2 검산기를 재개방하는 것이 아니라 **새 도구에서 같은 종류가 재발**한 것이다.

위치: [g2_network_reread.py:239](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9d25757dcdbd127731043c5d2293ae47e0202242/scripts/g2_network_reread.py#L239)의 `cohorts or []` 루프, [249](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9d25757dcdbd127731043c5d2293ae47e0202242/scripts/g2_network_reread.py#L249)의 루프 안 M1, [324](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9d25757dcdbd127731043c5d2293ae47e0202242/scripts/g2_network_reread.py#L324)의 실패 수만으로 성공 결정.

정상 실제 게시 산출물을 둔 1케이스 fixture에서 **원본 CLI** 실행:

| manifest | 읽은 케이스 | n_fail | rc |
|---|---:|---:|---:|
| 정상 | 1 | 0 | 0 |
| `plan` 삭제 | **0** | **0** | **0** |
| queue는 유지하고 `cohorts=[]` | **0** | **0** | **0** |
| queue는 유지하고 `cohorts` 삭제 | **0** | **0** | **0** |

M0의 기대 세대 g2 하나만 통과하고 M1·M2·H1은 호출되지 않는다. 실제 파일·배치 기록이 있어도 전혀 읽지 않으므로 물리적 실패나 빈 코호트의 정당한 결과가 아니다.

**최소 수정:** 루프 전에 manifest/plan/cohorts/queue의 타입·비어 있지 않음·중복·코호트 소속을 검사하고, 읽은 고유 ID 집합이 등록된 기대 집합과 같음을 루프 밖에서 검사한다. 생산의 194와 pilot의 3을 구분하는 명시적 등록 모드를 둔다. mutable queue 하나를 자기 자신의 유일한 기대 집합으로 쓰지 않는다.

**해결 증거:** 위 세 변이 및 한 코호트 누락·중복 ID·비등록 코호트 음성 대조, 정상 pilot 3·생산 194 양성 대조. n_fail만이 아니라 기대 수·읽은 수·집합 대조가 출력되어야 한다.

재현: `python probes/seal_paths.py`; `evidence/seal_paths.json`의 `reread` 및 `reread_*/cli.log`.

## 4. G2RR2-03 · P2 — 정적 닫힘 27⊆29가 실제 접촉 생산 경로를 빠뜨린다

**무너지는 주장:** “워커의 망 정지 경로 전체 전이 의존성이 봉인됐다.” 앞으로 함수 안 import가 추가될 수 있다는 추상적 우려가 아니다. **현재 기본 경로에 이미 누락이 있다.**

경로:

1. [analyze_contacts.py:1057](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9d25757dcdbd127731043c5d2293ae47e0202242/scripts/analyze_contacts.py#L1057) → `run_full_analysis`.
2. [dem_analysis_core.py:1821](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9d25757dcdbd127731043c5d2293ae47e0202242/scripts/dem_analysis_core.py#L1821) → `calc_fracture_stages`.
3. [같은 파일:1000](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9d25757dcdbd127731043c5d2293ae47e0202242/scripts/dem_analysis_core.py#L1000) → 함수 내부 `fracture_model` import.
4. [analyze_contacts.py:736](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9d25757dcdbd127731043c5d2293ae47e0202242/scripts/analyze_contacts.py#L736) → 그 결과를 full_metrics에 병합.

`fracture_model.py`는 [실행기 CODE_FILES:152](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9d25757dcdbd127731043c5d2293ae47e0202242/scripts/run_network_194_parallel.py#L152)에도, `DEP_LAZY`에도 없다. 실행기의 `HANDOVER_GROUPS`에는 **fracture가 포함**된다.

실제 `calc_fracture_stages` 호출: AM_P 두 구, 실 반지름 6 µm, 겹침 0.2 µm, raw r=0.006·δ=0.0002·scale=1000. **검토자 사본만** `K_IC_AM_P`를 0.3→30 MPa·m^0.5로 바꾸고 재수입했다.

- `frac_multicrack_pct`: **100→0%**, `frac_intact_pct`: **0→100%**.
- `code_fp`: 전후 모두 **`f3f54951a69eb5d9f55a205e2143a8807b047b257fc5685d7f369deafff532ea`**.
- 닫힘 목록도 동일하고 해석 오류 0; 누락 모듈은 계속 목록 밖.

이 값은 **의존성 연결을 보이는 변이**이지 파괴모델의 물리적 타당성을 재심한 것이 아니다. 이 모듈 변경이 FULL σ를 바꾼다는 증거도 아니다. 반면 “full_metrics/인계 fracture 열까지 같은 코드로 만들었다”는 전체 경로 봉인은 성립하지 않는다. 깨끗한 Git 체크·HEAD 검사는 다른 방어층으로 남아 있으므로, 임의의 추적 파일 변경이 모든 관문을 우회한다고 주장하지 않는다.

**최소 수정:** 실제 누락 모듈과 그 의존을 봉인하고 지문 재등록. `DEP_LAZY`를 적용 경로별로 완성한다. 정적 검사는 보조로 유지하되, 생산→게시의 import 관측 또는 누락 모듈 변이 시험으로 실제 경로를 확인한다. 물리 상수를 새로 고르라는 요구가 아니다.

**해결 증거:** 동일 변이에서 새 지문 변경·봉인 거부, 정상 값 보존. 새 등록문은 29파일·옛 지문을 그대로 쓰지 않는다.

재현: `python probes/dependency_gap.py`; `evidence/dependency_gap.json`.

## 5. G2RR2-04 · P2 — CF의 σ₀와 부모 σ₀가 갈려도 차원값을 발행한다

**무너지는 주장:** “숫자를 실은 CF도 같은 실행의 σ₀·온도와 결합된 증서로 보호된다.” FULL q와 τ를 바꾼 반례는 아니다.

위치:

- [tau_flux.py:583](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9d25757dcdbd127731043c5d2293ae47e0202242/scripts/tau_flux.py#L583): FULL의 σ_dim은 부모 σ₀, CF/협착-only는 **증서 자체 σ₀**로 재구성. 증서↔부모 대조를 ⑧에 맡겼다고 적었다.
- 그러나 [pipeline_service.py:237](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9d25757dcdbd127731043c5d2293ae47e0202242/webapp/pipeline_service.py#L237)의 `network_sigma0_problem`은 모드·legacy·full_metrics의 부모 값끼리 비교할 뿐 **증서 내부 σ₀를 읽지 않는다**. 호출은 [1006](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9d25757dcdbd127731043c5d2293ae47e0202242/webapp/pipeline_service.py#L1006).

실제 생산자 CLI가 쓴 후보에서 Hertz CF 증서의 `sigma_bulk_S_cm`만 0.003→0.006 S/cm로 바꾸고, CF 차원값을 그 증서로 다시 계산했다. 사본 네 곳의 같은 레코드를 일치시켰다. 부모 σ₀·온도·FULL·q·전류·기하·세대 도장은 그대로다.

| 값·판정 | 정상 | 반례 |
|---|---:|---:|
| 부모 σ₀ (S/cm) | 0.003 | 0.003 |
| CF 증서 σ₀ (S/cm) | 0.003 | **0.006** |
| CF q | 0.03926991 | 0.03926991 |
| CF σ_dim (mS/cm) | **0.117810** | **0.235619** |
| FULL q | 0.00400538 | 0.00400538 |
| 게시 / stop / g2 계약 / 인계 | 통과 | **모두 통과** |
| 다시 읽기 K1–K7 | 통과 | **모두 통과** |

따라서 “모든 사본과 증서를 전면 위조하면 못 잡는다”라는 한계에 속하지 않는다. **그대로 남은 부모와 증서가 명시적으로 불일치**하는데 빠진 대조 때문에 통과한다. 추가로 FULL 증서의 σ₀만 두 배로 바꿔도 수용된다(계산은 부모 값을 사용하므로 FULL 숫자는 그대로).

**최소 수정:** 이온 모드별 세 가지의 증서 σ₀를 해당 부모 `sigma_grain_S_cm` 및 실행 온도 규약과 대조한다. FULL도 표기 불일치를 허용하지 않는다. CF·협착-only의 차원값을 증서 내부 자기일관성만으로 수용하지 않는다. 전자·열은 해당 채널의 기준 전도도를 사용하며 이온 σ₀를 강제하지 않는다.

**해결 증거:** 위 반례 및 온도 변경 시 같은 유형을 게시·인계·다시 읽기에서 거부; 정상 온도 적용 결과와 정직한 가지 실패 양성은 보존.

재현: `python probes/branch_policy.py`; `evidence/branch_policy.json`의 `cf_sigma0_x2`, `full_cert_sigma0_x2`.

## 6. G2RR2-05 · P3 — 진단 가지가 통째로 없으면 공용 계약은 수용, K7은 거부

위치: [tau_flux.py:596](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9d25757dcdbd127731043c5d2293ae47e0202242/scripts/tau_flux.py#L596). 상태가 None이면 첫 검사를 통과하고 증서가 None이면 곧바로 성공한다.

실제 CLI 후보에서 Hertz CF의 `sigma_bulk_net`, `_mScm`, `_status`, `_reason`, `solve_certificate_bulk_net` 다섯 키를 삭제하면 **게시 done·인계 통과**다. 그러나 [g2_network_reread.py:112](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9d25757dcdbd127731043c5d2293ae47e0202242/scripts/g2_network_reread.py#L112)의 K7은 “숫자 없음↔상태 None”으로 거부한다.

없는 값을 수치로 발행하지 않았고 정상 계획에서 최종 K7이 막으므로 P3로 둔다. 다만 **“같은 계약을 다시 부르기만 한다”는 설명은 틀리다.** K7은 별도 자격을 추가한다. “정직한 실패=값 없음+이유”와 “기록 전체 결손”을 공용 계약에서 구분하고, K7은 그 공용 결과를 소비하게 하는 것이 맞다. 부재를 임의의 `not_computed`로 채우지 않는다.

재현: 같은 탐침의 `diagnostic_fields_absent`. 해결 증거는 게시·인계 거부와 정상 실패 양성 보존이다. 이 항목 단독으로 194 발사를 보류할 사유를 추가하지는 않는다.

## 7. Q2 — 저자의 진단 가지 정책은 수용한다

**동의.** 다음 두 상황을 갈라 두면 된다.

1. 계산 실패를 정직하게 기록한 가지: 그 가지만 미계산, 정상 FULL은 보존.
2. 숫자를 발행하면서 증서가 없거나 모순된 레코드: 조립·출처 모순으로 레코드 전체 거부.

정상 FULL을 불필요하게 폐기하는지 확인하기 위해 실제 CLI가 부르는 SciPy 풀이에 **H0 이온 CF에서만** 결함을 주입했다. 완성된 JSON에 실패 상태를 손으로 채운 시험이 아니다.

| 실제 생산자에 주입 | CF | FULL q | 게시·인계·K1–K7 |
|---|---|---:|---|
| 첫 spsolve 예외 | `not_computed / solve_failed`, 값 없음 | 0.00400538 | 모두 통과 |
| CF 각 사다리 풀이가 증서 불합격 해를 반환 | `not_computed / current_conservation_failed`, 값 없음 | 0.00400538 | 모두 통과 |

둘째는 spsolve, Jacobi CG, ILU GMRES까지 실제 사다리를 거쳤다. 증서의 실패 시도들은 남고, 채택된 해인 것처럼 숫자를 남기지 않는다. **요청서의 미시험 양성은 이 소프트웨어 통합시험 범위에서 보완됐다.** 실침대에 이 실패가 발생하는 빈도나 모든 예외 형태까지 보증하지 않는다. G2RR2-04·05는 이 정책을 완화해서 해결할 문제가 아니다.

## 8. Q3 — 새 실행 봉인

**부분 수용.** 설계 방향은 맞지만 완결되지는 않았다.

### (a) 생산자로부터 기대 세대를 유도

21구 사슬의 실제 생산자 출력과 공용 계약으로 “이 체크아웃이 어떤 세대를 내는가”를 재는 것은 적절한 **배선 스모크**다. 독립적인 모델 정확성 증거로 부르지 않는 한 같은 코드를 썼다는 이유만으로 기각하지 않는다. 등록된 기대 조합을 독립 오라클로 갖춘 회귀와 코드 핀이 함께 필요하다. 이번 합성 생산자 시험은 g2의 정상 조합과 기존 반례 거부를 지지한다.

하지만 이것은 manifest의 필수 선언을 생략할 근거가 아니다. G2RR2-01을 먼저 닫아야 한다. Windows 검토 환경에서는 실행기 전체 POSIX selftest와 **원형 `python -I -B` 발사 사전 점검**을 인증하지 않았다. WSL 기록으로 확인할 항목이다.

### (b) 전이 의존

정적 닫힘+명시적 지연 import 목록은 쓸 수 있다. 단 **현재 누락된 fracture_model부터** 넣어야 한다. 27⊆29는 수집기가 찾은 집합의 포함 관계일 뿐 완전성의 증명이 아니다. 모든 웹앱 화면·MPM 모듈을 무차별 봉인하라는 요구는 아니다.

### (c) 계약 상수는 봉인된 코드 한 곳에

동의. 같은 문턱·역할 표를 러너에 복제하지 않는 것이 맞다. 검토자가 승인한 상수와 조합을 독립 기대값으로 시험하고, 실행 영수증에 그 코드의 바이트를 고정하면 된다. 해시 일치만으로 코드의 의미가 맞다는 주장은 하지 않는다.

**독립 재계산은 일치했다:**

| 항목 | 결과 |
|---|---|
| 등록 입력 수 | lhs 130 + lhsx 64 = 194 |
| ID 지문 | `a04282d7275bd8f92b0afb4ac8b045f72f3867ccebbb7813b530b3901fd7b3bf` |
| 원자료 SHA 표 지문 | `da7c93f9a0887145ff171e381c8608cb79779d96aea5a595a25677dc361ef784` |
| 코호트 TSV 두 해시 | 등록값과 각각 일치 |
| 현재 CODE_FILES 29 지문 | `f3f54951a69eb5d9f55a205e2143a8807b047b257fc5685d7f369deafff532ea` |

194 수확 JSON에서 직접 문자열 표를 만들고 SHA256을 계산한 값이며 러너 함수와도 일치한다. **WSL 원덤프 바이트 194건을 직접 읽었다는 뜻은 아니다.** 위 의존성 보완 후 코드 지문은 새로 등록해야 한다.

## 9. Q4 — 사전 점검을 실침대 스모크와 LHS 시범으로 나누는 설계

**설계에 동의, 완료 판정은 대기.** real14·case15를 194의 ID로 위장해 넣을 필요 없다. 같은 `run_pipeline(stop_after='network')`을 통과시키고, LHS 셋으로 러너·merge·진짜 배치 기록 대조를 맡기면 역할 분담이 맞다.

필요한 증거는 다음과 같다.

- 핀·깨끗한 작업트리·Python/NumPy/SciPy 버전·실행기 코드 지문.
- 실침대 두 건 및 LHS 세 건의 실제 게시 JSON: 세 모드의 FULL/CF/협착 상태·증서·도장. 최소 해당 부분을 재독 가능한 형태로 함께 보존한다.
- pilot **정확한 세 ID**와 실제 manifest, 시도 영수증, merge·audit·reread 판정. “0건 PASS”나 일부 코호트만 읽은 성공은 배제.
- 정상 비관통은 valid_zero/NOT_PERCOLATING; Rc=0 협착-only는 not_computed와 사유; CF 과전도는 값과 모형 표지. 서로 대체하지 않는다.
- 이번에 보완한 정직한 가지 실패 양성을 상주 시험으로 옮긴다. 실침대에서 우연히 그런 실패가 나올 때까지 기다릴 필요는 없다.

smoke의 합성 batch H1은 P1/P3 자기대조라는 한정을 유지하고, pilot의 실제 기록 대조로 보완한다. 이 5건은 모든 194 기하의 과학적 타당성·자원 사용량을 인증하지 않는다. 194 완료 후 전수 상태·ID·증서·값 대조는 여전히 필요하다.

## 10. Q5 — 발사 전 최소 목록과 S3 순서

1. **G2RR2-01~04 수정과 해당 음성 대조**, 정상 생산·역사 읽기·정직한 가지 실패 양성 보존. G2RR2-05의 공용 계약 정리도 같은 수정에 권고한다.
2. 누락 의존을 포함한 **새 코드/실행 스키마 봉인 및 등록문 지문 갱신**. 옛 29파일 지문을 승인값으로 재사용하지 않는다. 194 ID·원자료·선별 cutoff는 그대로 유지한다.
3. 수정 핀의 WSL에서 원형 자체시험·실덤프 스모크·LHS3 pilot→게시→audit→reread 증거를 제출한다. 성공한 끝줄만이 아니라 원 프로세스 rc도 보존한다.
4. 위 결과 재검증 후 1저자 발사 승인. **이번 회신을 자동 또는 조건부 발사 GO로 읽지 않는다.**

**S3 재봉인이 반드시 194보다 먼저일 필요는 없다.** 이 194 경로는 S3 봉인을 소비하는 `run_s3_psi` 실행이 아니다. 두 실행을 명시적으로 분리하면 194 자체의 완전한 새 봉인과 S3의 봉인 갱신 의무는 별개다.

다만 S3를 실행하기 전에는 실제 수치 의존인 `lens_geometry`를 포함한 봉인 보완이 필요하다. 넣을지 말지를 취향으로 남겨 둘 수 없다. [seal_s3_prerun.py:99](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9d25757dcdbd127731043c5d2293ae47e0202242/scripts/seal_s3_prerun.py#L99)의 네 모듈 목록과 [run_s3_psi.py:243](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9d25757dcdbd127731043c5d2293ae47e0202242/scripts/run_s3_psi.py#L243)의 소비 검사 범위를 맞춰야 한다. 원래의 코호트 cutoff·baseline 선별을 오늘 값으로 다시 고르는 “재봉인”은 허용하지 않는다. S3 교정 전에는 해당 실행을 별도 HOLD로 남긴다.

## 11. 재현 범위와 자료

- 핀의 파일 **389개**를 Git blob SHA1과 SHA256으로 검증했다. 완전한 저장소 checkout은 아니며 git 객체가 없다. 크기 제한으로 `findings.json` 전체는 반입하지 못했으므로 원장 전체의 최신 상태를 인증하지 않는다. 닫힘 대상은 요청서·직전 판정문·코드와 탐침으로 판정했다.
- 기존 15개 회귀 진입점은 모두 rc=0. 출력 합계 **648 PASS**, 수치 모듈 과거 git 비교 4 SKIP 및 일부 선택적 검사 미실행이 있다. 특히 `run_contract`가 없는 사본에서는 RC7-01j2가 생략되므로 저자의 657 전체 재현이라고 하지 않는다.
- 원형 `g2_network_reread --selftest`는 Windows 심볼릭 링크 권한 `WinError 1314`에서 중단. 검사 로직을 바꾸지 않고 **시험 fixture의 symlink만 copy로 대체**한 별도 실행은 9/9 통과했다. POSIX 심볼릭 링크·병렬 실행기·WSL 운전 보증과 구별한다.
- 리뷰 독립 탐침 9개 진입점 실행 완료. 원래 반례 거부, 위 새 반례, 정상 양성의 관측 결과를 별도 검산한 **406항목** 일치. 이것은 **반례를 재현한 증거의 검산**이지 생산 PASS가 아니다.
- 전체 `check_all.sh`, POSIX 실행기 68/68, WSL 스모크 11/11, 새 194, 실제 실덤프 pilot 완료는 이번 실행 결과로 주장하지 않는다.
- 문서 작성 스킬은 닫힘 범위·한정어·재현 증거의 구분에 적용했고, 판정의 과학적 근거를 대신하지 않는다.

주요 재현 명령(검토 묶음 루트, 필요한 수치 라이브러리가 있는 Python):

```bash
python run_tests.py
python run_probes.py
python verify_evidence.py
```

원문 파일·소스 핀·수치·로그·음성/양성 fixture는 동봉 묶음에 있다. 검토용 변이는 `tmp`/`evidence`의 사본에만 만들었으며 생산 소스는 바꾸지 않았다.

**HOLD — 새 194 생산·v1.3 최종 인계. 기존 수치 교정과 정상 FULL 보존은 지지.**
