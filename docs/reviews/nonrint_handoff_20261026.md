# Claude 반입 준비: Rint 외 5개 트랙의 고정 핀 인덱스 (2026-10-26)

쉽게 말하면, **코드 핀은 실제 수정이고 리뷰·종결 ZIP은 그 수정을 확인한 근거**다. 나중에 Claude에게는 둘을 함께 전달한다. 종결 확인서만으로 구현이 옮겨지는 것은 아니다.

이 문서는 **나중에 Claude가 반입할 구현과 근거를 구분하는 인덱스**다. 이 Codex non-Rint 트랙의 실제 중심 가지 반입은 계속 보류이며, merge/rebase/cherry-pick이나 물리 실행 명령을 수행하지 않았다. 종결 ZIP만 전달하면 구현 전체를 받은 것이 아니다. 특히 수용된 ULPRI 소비자 구현은 별도 가지에 있다.

## 1. 현재 읽기 전용 관찰

관찰 시각: 2026-10-26 20:03 KST. 중심 `claude/stoic-knuth-NObVQ`는 `93d93bc02f5a68d6551137ab420dbc0eea40b455`, source `claude/sdcp-dem-manuscript-si-pqwtv8`는 `446b5bf543c39120e0003f3a7e2272264d1e97a8`다. 이전 9db 관찰은 작업 증거로 보존하며 현재 상태로 재사용하지 않는다. source에는 Rint 후속 기록과 별도 50kg 수정 기록이 추가되었다. 50kg의 claimed_fixed/partial 기록은 별도 트랙이며 현재 5개 트랙이나 P2의 GO로 전이하지 않는다.

Claude의 [18:00 사실 회신](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/446b5bf543c39120e0003f3a7e2272264d1e97a8/docs/collab/claude_to_codex/20261026-1800_nonrint-facts.md)이 7fd4 커밋부터 원격에 존재한다. 이는 앞서 받은 수동 전사본과 별도 Git blob이다. 원격 문서의 restart 해시 미기록 설명은 아직 남아 있으므로 [18:16 접수·정정 기록](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/18c7b83f97f84808d3283d8bbc37725b48bc5924/docs/collab/codex_to_claude/20261026-1816_nonrint-facts-reply.md)과 함께 읽는다. 특정 restart의 과거 예상 해시는 이미 기록되어 있고, 사용자 전달로 정정 수용을 확인했다. 현재 ibb 여섯 파일의 존재·실제 해시는 사용자가 확인하는 중이며 이 문서 작성자는 접근하거나 대신 실행하지 않았다.

D2/D3 믹서 외부 리뷰의 새 수신 기록은 관찰 범위에서 발견하지 못했다. source의 kg50 d2/d3 이름은 믹서 트랙 리뷰가 아니다.

## 2. 구현과 리뷰 핀

코드 후보는 실제 해당 수정·직접 검사의 대상이며, 리뷰 핀에는 후속 증거가 포함된다. 아래 구현/회귀와 해당 문서·증거를 함께 검토해야 한다. 종결 기록은 이를 대체하지 않는다.

| 트랙 | 최신 구현 후보 | 제출 리뷰 핀 | 나중에 반입할 내용 / 현재 한계 |
| --- | --- | --- | --- |
| 언로딩 | `643344fee22a5d1131a59c8cd46bcf6c9a09d65b` | `4c29705fa1c4ba94737a858b206fa4f4c5bb2bde` | ULPRI 표지 경계 수정 및 회귀·봉인 자료. ULPRI-01/02 좁은 외부 종결 수용; 물리 실행 GO 아님. |
| LHS214 | `ed6ed401f904d9f818cbdced42d111a7b1efb8d2` | `854857e576a2a8aba07ec861dbee39d4bb59efae` | 사전 점검·영수증 SHA 경계 수정과 증거. 실제 재발사/기계 입력은 별도 조건. |
| DEM 세대2 / T12 | `3eecce8af503556b678f8f4a02343e6bce3d0b83` | `96f15ed17e03181b6096fb65f71ec7f577f17523` | 계획/소비자 계약·고정 핀 52·오프라인 보호. T12R-01 외부 종결; 실제 P2와 설계 전체 GO 아님. |
| 믹서 D2 | `34782a1874435e317f44c9d8f2045d53ceaf4dcc` | `045e0b3098e8fe5a64d6eb0da310da776e68f995` | 검증기가 결속된 D2 소비자와 직접 시험. 외부 검토 대기; 발송/반입 수행 안 함. |
| 믹서 D3 | `9c2f7b47fd4559ee4c08f23e667cdae92badbb04` | `e0daf7b234bcc7935259d786e270268372abe2a2` | 유한 격자 후보 reader와 직접 시험·설계 자료. 외부 검토 대기; 발송/반입 수행 안 함. |

DEM/T12 계열의 중간 제출 핀은 아래 순서다. 모두 최신 종결 가지의 조상이므로 별개 독립 묶음처럼 중복 반입하지 않는다.

| 단계 | 고정 제출 핀 | 역할 |
| --- | --- | --- |
| DEM 계획 | `2443a63eaa87d52e385a35f8bab4225efa0d25fe` | 비준된 계획 수정·T12 준비 인계 |
| T12 소비자 계약 | `2b4b40ea5e375659bfad8243c1ccb6fe0ef2853f` | 고정 소비자 52개 합성 관측·별도 게이트 증거 |
| ULPRI 종결 기록 | `bffc42cab29da37b45f8a713e30e8572b91e7da3` | 외부 ULPRI-01/02 종결·T12 외부 검토 인계. ULPRI 구현 가지를 포함하지 않음 |
| T12R 수정 | `96f15ed17e03181b6096fb65f71ec7f577f17523` | runner의 자동 fetch 차단·상주 오프라인 회귀 |
| T12R-01 종결 | `58b6ccb0d754b07b6f1695328267c9aa531a4bb6` | 수용된 오프라인 경계의 문서 전용 종결. 추가 재검토 요청 없음 |

언로딩의 이전 정수 교정 리뷰 핀 `01c1aaf5be8acdf7d1716f34cc86fc77d8e27362`는 최신 ULPRI `4c29705fa1c4ba94737a858b206fa4f4c5bb2bde`의 조상이다. 이전 ZIP과 판정은 역사 증거로 보존한다.

## 3. 실제 Git 그래프에 따른 범위와 중복

다섯 트랙의 공통 출발점은 `7799a2ff64ba462b42ce05edd3e63b7c2854d557`다. 다음은 **차이 범위 표기이지 즉시 실행할 반입 명령이 아니다**. 범위의 왼쪽 끝은 제외한다.

| 독립 묶음 | 시작점 제외 → 최종 핀 포함 | 커밋 수 |
| --- | --- | ---: |
| 언로딩 전체 | `7799a2ff64ba462b42ce05edd3e63b7c2854d557..4c29705fa1c4ba94737a858b206fa4f4c5bb2bde` | 6 |
| LHS214 | `7799a2ff64ba462b42ce05edd3e63b7c2854d557..854857e576a2a8aba07ec861dbee39d4bb59efae` | 4 |
| DEM 계획부터 T12R 종결까지 | `7799a2ff64ba462b42ce05edd3e63b7c2854d557..58b6ccb0d754b07b6f1695328267c9aa531a4bb6` | 11 |
| 믹서 D2 | `7799a2ff64ba462b42ce05edd3e63b7c2854d557..045e0b3098e8fe5a64d6eb0da310da776e68f995` | 4 |
| 믹서 D3 | `7799a2ff64ba462b42ce05edd3e63b7c2854d557..e0daf7b234bcc7935259d786e270268372abe2a2` | 4 |

이 다섯 범위는 고유 Codex 커밋 29개다. 그중 DEM 최신 11개 범위는 DEM 4개 + T12 3개 + ULPRI 종결 문서 1개 + T12R 2개 + T12R 종결 문서 1개다. 같은 조상을 여러 범위에서 다시 고르지 않는다. 언로딩 최신 6개에는 이전 ULPR 4개와 ULPRI 2개가 포함된다.

현재 중심 핀에서 공통 출발점까지는 **Claude/Rint 이력 64개**가 이미 상속돼 있다. 그러므로 중심 핀부터 Codex 최종 핀까지의 전체 범위를 그대로 Codex 작업으로 취급하면 안 된다. Claude source→중심 가지의 동기화는 Claude가 별도 관리할 사안이며 이 인덱스가 이를 실행하거나 승인하지 않는다.

ULPRI와 최신 DEM/T12 종결 트리 사이에는 변경 경로 53개가 겹치며 모두 동일 Git blob과 파일 모드다. 이는 종결 기록에서 보존한 역사 지원 자료다. 나머지 독립 묶음 쌍의 변경 경로 겹침은 0개였다. 위 고정 source의 공통 출발점 이후 변경과 다섯 Codex 범위 변경의 교집합도 0개다. **이는 관찰한 두 트리의 경로·바이트 대조이지 미래 통합 무충돌 보장이 아니다.** 실제 반입 시 같은 내용은 중복 도입하지 않고, 대상 트리가 바뀌었다면 다시 대조한다.

질의 `3fab532fa0409c5300e8f2c3336cd408259a6064`와 회신 접수 `18c7b83f97f84808d3283d8bbc37725b48bc5924`는 58b6 뒤의 **서신 두 개**다. 구현·종결 29개에 섞어 세지 않는다. 이 인덱스 역시 문서 인계이며 코드 범위가 아니다.

## 4. 놓치면 안 되는 소비자 경계

최신 T12 종결 트리는 ULPRI 4c의 후손이 아니다. 현재 checkout의 언로딩 키트는 수용된 4c와 README, SHA256SUMS, active_rules.json, seal_kit.py, ul_gates.py, ul_reader.py 등 6개 파일이 다르다. **고정 T12 runner가 Git에서 4c를 읽어 52개를 통과한 것과, 현지 통합 소비자 파일이 4c 구현으로 반입된 것은 별개다.**

Claude가 나중에 구현을 반입할 때에는 ULPRI 구현/회귀/봉인 자료를 독립 묶음으로 포함하고, 통합된 실제 생산자/소비자 파일·기대 계약을 직접 검증해야 한다. 고정 핀 회귀는 역사적 기준으로 계속 별도 유지한다. 직접 T12/오프라인·D2·D3 검사와 공유 CI의 연결은 그때의 제안/검토 항목이며 이 문서가 공유 CI나 원장을 수정하지 않는다. 과거 155를 통합 트리 PASS로 옮기지 않는다.

## 5. 기존 제출 ZIP 신원

아래 ZIP은 이미 만들어진 자료이며 새 발송이나 검토를 요청한 것이 아니다. 전체 SHA256은 전달자가 파일을 대조하기 위한 값이다. 작은 종결 ZIP은 문서·선택 증거만 포함하므로 구현 ZIP/고정 원격 핀과 함께 전달한다.

| 고정 핀 | ZIP 파일 | SHA256 |
| --- | --- | --- |
| [01c1aaf5be8a](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/tree/01c1aaf5be8acdf7d1716f34cc86fc77d8e27362) | codex-unloading-ulpr-01c1aaf5be8a.zip | `ca2925b6044b72a7c077058c0a3cfbd00595ccc01aaa75d86daa0111da73f393` |
| [4c29705fa1c4](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/tree/4c29705fa1c4ba94737a858b206fa4f4c5bb2bde) | codex-unloading-ulpri-4c29705fa1c4.zip | `84aa1bf806d9008d17ef6fad9a730d6ce226ffe5bff4852101338aa9a1deb93c` |
| [854857e576a2](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/tree/854857e576a2a8aba07ec861dbee39d4bb59efae) | codex-lhs214-relaunch-854857e576a2.zip | `d83c3d270dd88d0c1b5c88b062e70100008047a645b683db1e60595f851583ad` |
| [2443a63eaa87](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/tree/2443a63eaa87d52e385a35f8bab4225efa0d25fe) | codex-dem-gen2-request-2443a63eaa87.zip | `68917168b8722e35fb3af01302cf4857058f22e70e7bfd7dda7fa723ffc55973` |
| [2b4b40ea5e37](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/tree/2b4b40ea5e375659bfad8243c1ccb6fe0ef2853f) | codex-dem-gen2-t12-2b4b40ea5e37.zip | `a5c6356e54bc9a985b7d3a5473858e11aed11862051cd528aeb8aabd45924482` |
| [bffc42cab29d](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/tree/bffc42cab29da37b45f8a713e30e8572b91e7da3) | codex-ulpri-closure-bffc42cab29d.zip | `125c7652bc83a8fec42be56d7b299785b82bc4e3b98e86b481f9173e6e588220` |
| [96f15ed17e03](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/tree/96f15ed17e03181b6096fb65f71ec7f577f17523) | codex-dem-gen2-t12r-96f15ed17e03.zip | `fd52dd397e47ee93d91432b4c045c43196b51527d5c52038b4c863d233518bb7` |
| [58b6ccb0d754](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/tree/58b6ccb0d754b07b6f1695328267c9aa531a4bb6) | codex-t12r01-closure-58b6ccb0d754.zip | `d99fdd2b50b02d7c10a9ae34b25372aecfb1b5c31a4983db409e4b616416b543` |
| [045e0b3098e8](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/tree/045e0b3098e8fe5a64d6eb0da310da776e68f995) | codex-mixer-mxd2-045e0b3098e8.zip | `39a41943eed7f4eb9897f1698e72d44ed32422487466290b74285bece201cac9` |
| [e0daf7b234bc](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/tree/e0daf7b234bcc7935259d786e270268372abe2a2) | codex-mixer-d3-design-e0daf7b234bc.zip | `1c72d096da35b7a24c2d513ba7ed004588debcf568fac19476d472d0e0e2d331` |

## 6. 향후 CI 연결 제안

아래는 **나중에 해당 고정 핀의 checkout에서** 사용할 기존 진입점 목록이다. 이번에는 실행하지 않았다. 작업 경로 자리표시는 실제 경로로 채워야 하며, 물리 실행 명령이 아니다. 전체 명령·소스 해시·의존성은 [기계 판독 근거](nonrint_handoff_20261026.json)에 있다.

**ULPRI — [고정 소스](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/tree/4c29705fa1c4ba94737a858b206fa4f4c5bb2bde)**

```text
python3 -I docs/data/ps45_unload_20261009/ul_reader.py --selftest
python3 -I docs/data/ps45_unload_20261009/ul_gates.py --selftest
python3 -I docs/data/ps45_unload_20261009/ul_runner_test.py --selftest
python3 -I docs/data/ps45_unload_20261009/make_unload_decks.py --check
python3 -I docs/data/ps45_unload_20261009/seal_kit.py --check
```

**LHS214 — [고정 소스](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/tree/854857e576a2a8aba07ec861dbee39d4bb59efae)**

```text
python3 scripts/run_network_194_parallel.py --selftest
python3 scripts/run_network_194_parallel.py preflight-verify --receipt <existing-receipt.json> --expect-set <production194|supp20> --approved-sha <approved-pin>
```

**T12R — [고정 소스](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/tree/96f15ed17e03181b6096fb65f71ec7f577f17523)**

```text
python3 -I scripts/test_dem_gen2_t12_consumer_contract.py --repo <object-repository> [--json <new-receipt.json>]
python3 -I scripts/test_dem_gen2_t12_offline.py --repo <object-repository> --source <pinned-checkout> --output <new-scratch-directory> --check-guard-mutation
```

**MixerD2 — [고정 소스](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/tree/045e0b3098e8fe5a64d6eb0da310da776e68f995)**

```text
python3 -I scripts/test_mixer_d2_consumers.py
python3 scripts/make_mixer_deck.py --selftest
python3 scripts/mixer_deck_readback.py --selftest
python3 scripts/mixer_deck_diff.py --selftest
python3 -I scripts/mixer_deck_readback.py --d2 <deck> <meta>
```

**MixerD3 — [고정 소스](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/tree/e0daf7b234bcc7935259d786e270268372abe2a2)**

```text
python3 -I scripts/test_mixer_d3_candidates.py
python3 -I scripts/mixer_d3_candidates.py --contract <contract.json> --observations <observations.json> --out <new-result.json>
```

ULPRI는 Python 표준 라이브러리와 전체 봉인 키트·fixture가 필요하고 runner 모의 검사는 Bash/임시 폴더를 사용한다. LHS는 저장소 pipeline/webapp 모듈과 과학·웹 의존성이 필요하며 표준 라이브러리 전용으로 보지 않는다. D2도 sibling 검증 모듈과 numpy를 가져온다. D3는 표준 라이브러리와 sibling 모듈을 쓴다. 기존 CI 패키지 기준은 numpy, scipy, matplotlib, flask, requests, networkx, adjustText, markdown, pandas, pillow이며 최소 의존성을 실험한 결과는 아니다.

T12에는 global --no-lazy-fetch를 지원하는 Git과 4c의 commit/tree/여섯 blob이 이미 로컬에 있어야 한다. 미지원 Git은 닫힌 실패로 처리한다. manifest/contract/fixture 결과도 해당 고정 소스에서 읽는다. offline 출력은 새 scratch 폴더여야 하며 guard 변이는 임시 로컬 file remote의 fetch만 일부러 관찰한다. 외부 네트워크나 물리 실행은 아니다.

LHS preflight-verify, D2 --d2, D3 --contract/--observations는 기존 실제 receipt/deck/contract가 필요한 인터페이스 예시다. 자리표시를 그대로 실행하는 검사가 아니다. 합성 selftest/직접 검사와 데이터가 필요한 CLI를 구분한다.

기존 공유 CI는 check_selftest_inventory의 --run-fast를 통해 LHS selftest와 기존 mixer 세 selftest를 이미 호출한다. 이 fast는 저장소 검사 분류명이다. TSV lane=none만 보고 미연결로 판정하면 안 된다. 반면 새 D2/D3 직접 검사, T12 계약/offline 검사, ULPRI 키트 검사는 관찰한 공유 workflow/check_all/inventory 경로에 연결되어 있지 않다. 향후 연결할 후보이며 이번에 공유 파일을 바꾸지 않았다.

통합 시에는 **고정 4c 회귀와 실제 통합 소비자 검사를 별도 작업으로** 유지해야 한다. T12의 --repo는 객체를 읽는 저장소만 바꾸고 대상 4c를 바꾸지 않는다. 현재 checkout의 소비자·생산자에 소스를 결속한 검사는 별도로 구현·검토해야 하며 이미 있다고 주장하지 않는다. 반입 이후 실제 트리에서 필요한 검증을 수행해야 한다. 과거 155 PASS를 미래 트리의 PASS로 재사용하지 않는다.

## 7. 다음 행위의 경계

사용자는 기존 P1 원본 여섯 파일의 신원 확인을 맡고 있다. 여기서는 그 결과를 기다리는 동안 구현·리뷰·종결 자료와 향후 CI 조건을 정리한다. 같은 확인을 다시 요청하거나 대신 실행하지 않는다. Claude 반입이 실제로 허용되면 먼저 대상 핀과 이미 포함된 조상을 확인하고, 위 독립 범위의 필요한 구현/회귀와 근거를 순서대로 검토한다. 공유 원장/CI의 후속 변경과 통합 검증은 별도 기록해야 한다.

D2·D3 외부 검토는 아직 대기이며 이번에 발송하지 않았다. 저장소에 이미 있는 P1 입력·과거 실행 압축본·문법/이력 검증 자료는 역사적 문맥으로 재사용하고 같은 자료를 다시 요청하지 않는다. 다만 이것을 실제 P2의 현재 R-a/S0나 물리 자격으로 바꾸지 않는다. 회신상 P2 생산·등록·R-a/S0와 Q7–Q9 실측은 없거나 미확인이다. P1 생산 침대 재사용이 다음 대상이며 새 P2와 별도 50kg gen-1 구상을 혼합하지 않는다. 실제 P2 지정 바이너리/이력·T10–T13·측정과 불확도는 여전히 미래 조건이다. 물리 T12는 NOT_RUN, physical_ready=false다. 이 목록은 전체 트랙 GO나 즉시 WSL/연구 실행 승인이 아니다.
