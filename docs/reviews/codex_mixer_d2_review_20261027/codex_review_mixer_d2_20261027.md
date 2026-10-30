# 믹서 D2 개발 소비자 독립 재검토 — 2026-10-27

**판정: HOLD — MXD2-01의 개발 소비자 하위 범위도 현재 핀에서 종결하지 않는다.**

정상 덱의 밀도·계획수·CED 산술이 틀렸다는 판정이 아니다. 실제 명령의 의미가 달라진 덱을 세 소비자가 함께 PASS로 받는 반례와, 파일 바이트와 해시를 서로 다르게 처리하는 반례를 재현했다. **새 finding 3건: P1 2건, P2 1건.** 생성기와 생산 코드는 고치지 않았고, LIGGGHTS·WSL·스케줄러·물리 계산은 실행하지 않았다.

## 1. 검토 신원과 증거의 지위

- 검토 핀: `045e0b3098e8fe5a64d6eb0da310da776e68f995`, `codex/mixer-mxd2`.
- 요청서: `docs/reviews/codex_mixer_d2_consumers_request_20261024.md`.
- 받은 ZIP: `codex-mixer-mxd2-045e0b3098e8-rebuilt-20261027.zip`.
- ZIP SHA-256: `9aaaccd3cdc096ebe36ee6e7d610a4b90dc8c8985ace49bddc29bf6cae8fec01`.
- ZIP 안 리포 파일 **559/559**를 원격 고정 핀의 Git blob과 대조: 불일치 0. `PIN.txt`는 리포 파일 수에서 제외했다.
- 주 증거 폴더의 `MANIFEST.sha256` **347항목**을 실제 파일 바이트로 대조: 불일치 0.
- ZIP은 전체 리포가 아닌 변경 파일 묶음이다. 빠진 의존성과 구 시험 고정물은 같은 핀에서 읽고 blob을 대조했다. checkout·fetch·refs 변경 없이 별도 스냅샷에 보관했다.
- 제출된 canonical 전체 gate는 **155 PASS / 0 FAIL / rc 0**의 과거 실행 증거다. 그 대상 `34782a1874435e317f44c9d8f2045d53ceaf4dcc`와 검토 핀 사이에서 `scripts/`, `webapp/`, `dem_scripts/`, `.github/` 변경은 **0**이다. 전체 tree 차이 28파일은 코드가 아닌 문서·증거다. **내가 전체 gate를 새로 실행한 실적으로 세지 않는다.**

독립 실험은 `d2/evidence/independent_probe.py`가 만든 합성 덱과 실제 Python 소비자 API/CLI만 사용했다. 반례마다 양쪽 덱과 메타의 해시·길이를 일관되게 갱신했다. CRLF 반례는 그 자체가 해시 처리 시험이므로 아래에서 따로 설명한다.

## 2. 요청 범위별 판정

| 요청된 하위 범위 | 판정 | 근거와 한계 |
|---|---|---|
| lab/gen1 밀도·상·인쇄 CED의 정적 산술 | 수용 | 기존 신규 시험 13/13. 독립 다른 입력 48조합에서 정상 되읽기·D2 짝 비교와 SE Bo·상별 계획수 계산 일치 |
| 삽입 명령에서 실행 가능한 계획·시간·회전 순서 결합 | **부분** | MXD2R-01. 명령의 존재·순서는 보지만 `run upto`, 늦은 `timestep`, 늦은 삽입 시작, 다른 끝판 주기를 놓침 |
| 명시적 D2 쌍 비교 | **부분** | 정상 쌍 보존. 하지만 두 덱의 공통 변조는 non-CED 토큰 동일성으로 검출되지 않으며, 절대 되읽기에도 같은 공백 존재 |
| 실제 적용 접촉과 정적 힘 척도의 결합 | **부분** | MXD2R-02. SE–SE 상호작용을 제외해도 SE–SE 힘 검산 PASS |
| 실제 파일 SHA·바이트 결합 | **열림** | MXD2R-03. LF로 정규화한 텍스트를 해시해 물리 바이트와 불일치 가능 |
| `--d2-plan`이 관측 증서/실행 GO를 만들지 않음 | 수용 | 정상·반례 모두 `registered=null`, `execution_authorized=false` 유지 |
| 새 S1 셀·코호트·정책·실물 입력 | 미검토·미완료 유지 | 이번 요청도 전체 MXD2-01 종결을 주장하지 않음 |

## 3. MXD2R-01 — P1: 명령 토큰이 같아도 시간·삽입·회전 계약이 달라진다

**영향:** 요청서 §2의 “실제 덱의 시간·step·주기 및 삽입→정착 두 단계→회전 결합”을 현재 PASS로 인증할 수 없다. 정상 생성 덱이 잘못 실행됐다는 증거는 아니다.

**위치**

- `scripts/mixer_deck_readback.py:167`–171: `timestep` 위치를 고려하지 않고 값을 저장, `run`은 첫 정수만 읽음.
- 같은 파일 `:981`–1003, `:1104`–1179: 숫자·생명주기 검사. `run` 옵션, 실제 dt 효력 시점, 삽입 `start` 및 끝판 주기 값의 의미 검사가 빠짐.
- 같은 파일 `:1291`–1321: 이 파싱 결과로 계획 시간·step을 대조.
- `scripts/mixer_deck_diff.py:169`–204: 양쪽 되읽기 뒤 non-CED 토큰 동일성 대조.
- `scripts/mixer_smoke_blind.py:245`–252: 같은 되읽기를 사용하는 계획 소비자.

[고정 되읽기 소스](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/045e0b3098e8fe5a64d6eb0da310da776e68f995/scripts/mixer_deck_readback.py#L1104)

**독립 반례:** 아래 네 변경을 각각 uncoated/coated 양쪽에 동일 적용했다. 모두 API 3종 **PASS**, 실제 CLI 3종 **rc 0**이다.

| 변경 | 현재 검사 결과 | 명령 의미로 독립 계산한 차이 |
|---|---|---|
| 모든 `run N` → `run N upto` | `[1, 560606, 560606, 6595382]`를 여전히 상대 실행 길이로 해석 | 실제 증분 `[1, 560605, 0, 6034776]`. 최종 step 7,716,595 → 6,595,382. 두 번째 정착 길이 0 |
| 유일한 `timestep 2.373e-07`을 마지막 `run` 뒤로 이동 | dt=0.2373 μs 계약 PASS | 실행 중 쓰인 dt가 그 명령으로 설정되지 않음. 선언된 dt로 실행 시간을 인증할 수 없음 |
| 두 `insert/pack`에 `start 9000000` 추가 | 계획 총수·상별 계획 PASS | insA는 step560,607, insB는1,121,213에서 제거됨. 시작9,000,000 전에 두 fix가 사라져 계획 삽입을 수행할 기회가 없음 |
| Front의 회전 주기만 0.1 s로 변경 | 주기·D2 짝 비교 PASS | 드럼 약0.782508 s, Front0.1 s. 정상 회전 구간에서 Front는15.650841486회전, 드럼 약2회전 |

`run upto`의 회전 시간은 **1.5650841486 s → 1.4320523448 s**다. 메타의 반올림 전 주기로 계산하면 약 **2.00008713 → 1.83008017회전**이다. 드럼 인쇄 주기는6유효숫자이므로 이 마지막 자리의 차이는 회전 누락 효과와 구분해야 한다.

`run upto`는 틀린 문법을 던진 시험이 아니다. 고정 LIGGGHTS 소스는 이를 목표 누적 step에서 현재 step을 뺀 실행 길이로 처리한다. 늦은 `start`도 실제 지원 옵션이다. 이 시간/삽입 결론은 소비자 실행과 LIGGGHTS 소스 해석에서 얻었으며, DEM 실행을 했다고 주장하지 않는다. [run.cpp:102,145–156](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/run.cpp#L145), [fix_insert.cpp:169–175](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/fix_insert.cpp#L169), [삽입 스케줄 검사](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/fix_insert.cpp#L652)

**최소 해결:** 개발 덱의 지원 문법을 닫는다. 현재 생성기 문법만 지원한다면 `run <정수>` 두 토큰만 허용하고, dt가 최초 run 전에 한 번 설정되며 이후 바뀌지 않음을 검사한다. 삽입 `start`·반복 옵션은 거부하거나 실제 활성 구간과 스케줄을 계산한다. Drum/Front/Back의 주기·축·원점과 시작/종료 시점은 공동 회전 계약에 각각 결합한다. 두 덱에 같은 변경을 넣는 상주 회귀가 필요하다.

**재현:**

```bash
python3 -I -X utf8 -B d2/evidence/independent_probe.py
python3 -I -X utf8 -B d2/snapshot/scripts/mixer_deck_readback.py --d2 d2/evidence/cases/run_upto/old.in d2/evidence/cases/run_upto/old.meta.json
python3 -I -X utf8 -B d2/snapshot/scripts/mixer_deck_diff.py d2/evidence/cases/run_upto/old.in d2/evidence/cases/run_upto/new.in --allow D2 --meta-ref d2/evidence/cases/run_upto/old.meta.json --meta-new d2/evidence/cases/run_upto/new.meta.json
python3 -I -X utf8 -B d2/snapshot/scripts/mixer_smoke_blind.py --d2-plan d2/evidence/cases/run_upto/old.in --d2-meta d2/evidence/cases/run_upto/old.meta.json
```

현재 기대된 **반례 재현 결과는 세 CLI 모두0**이다. 같은 명령에서 `run_upto`를 `late_timestep`, `insert_start_late`, `front_period`로 바꿔도 재현된다.

## 4. MXD2R-02 — P1: SE–SE 접촉을 꺼도 실제 접촉력 계약 PASS

**위치:** `mixer_deck_readback.py:1240`의 허용 명령에 `neigh_modify`가 있지만 인자 의미를 제한하지 않는다. `:1248`–1252는 pair/wall 모델 문자열만 검사한다. `:1271`–1290의 힘·겹침 계산은 인쇄 행렬을 계산하며 접촉 제외를 확인하지 않는다.

**반례:** 양쪽 덱에 다음 한 줄을 추가하고 각 메타의 해시·길이를 재결합한다.

```text
neigh_modify exclude type 3 3
```

3상 고정물의 type3은 SE다. 되읽기·쌍 비교·계획 소비자는 모두 **PASS / rc0**이며, 정상 SE–SE CED와 Bo 검산 결과를 내보낸다. 그러나 이 명령은 SE–SE 쌍을 이웃 목록에서 제외하여 해당 쌍 상호작용을 계산하지 않게 한다. 이는 실물 STL이나 둘째 난수 시드의 인증 범위 밖 문제와 다르다. **동일 덱에 적힌 normal law가 실제 어떤 접촉에 적용되는지의 문제**다. [고정 LIGGGHTS 설명서, neigh_modify exclude](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/doc/neigh_modify.txt#L105)

별도 보조 탐침으로 `coefficientFriction` 행렬 fix를 통째로 지워도 세 소비자가 PASS했다. 이것은 검사 범위가 모든 재료 fix의 완비성을 포함하지 않음을 보여준다. 이번 리뷰에서는 바이너리를 실행해 그 덱의 초기화 실패를 확인하지 않았으므로, 이것을 별도 물리 실패나 새 finding 수로 부풀리지 않는다.

**무너지는 결론:** 인쇄 CED의 대수적 Bo 계산은 여전히 맞다. 하지만 PASS를 “실제 덱에서 이 힘 척도를 적용하는 D2 쌍”으로 읽는 결론은 성립하지 않는다. 두 덱의 공통 누락은 짝 비교로 해결되지 않는다.

**최소 해결:** 지원 `neigh_modify` 문법을 고정하고 접촉 제외 옵션을 거부한다. 같은 원리로 지원하는 pair/wall 모델에 필요한 재료 fix의 완비성과 적용 전 순서를 명시한다. 임의 LIGGGHTS 입력 전체를 해석할 필요는 없으며, 모르는 의미는 개발 소비자에서 명시 거부하면 된다.

**재현:** 위 CLI 명령의 사례 폴더를 `exclude_SE_SE`로 바꾼다. 세 CLI 모두 현재 rc0. 원본·메타·세 API JSON·세 CLI 로그가 해당 폴더에 있다.

## 5. MXD2R-03 — P2: 파일 바이트 해시와 정규화된 텍스트 해시가 뒤바뀜

**위치:** `mixer_deck_readback.py:1196`–1199는 `text.encode('utf-8')`로 해시·길이를 계산한다. 같은 파일 `:1358`, `mixer_deck_diff.py:838` 및 `:1798`, `mixer_smoke_blind.py:985`의 텍스트 읽기는 CRLF를 LF로 정규화한다.

**실제 CLI 반례:** LF 정상 덱을 CRLF 바이트로 저장하되, LF의 메타 해시·길이는 그대로 둔다.

| 항목 | 값 |
|---|---|
| 실제 CRLF 파일 길이 | **13,833 bytes** |
| 메타가 주장하는 LF 길이 | **13,654 bytes** |
| 실제 CRLF SHA-256 | `0b92f856e224d0537b36b2c4fb2cc257e23cfbdea9528c478ef42d0dda63f015` |
| 메타의 LF SHA-256 | `32033f6b0e17f33ecfe70121eaee393aa6c2748151f54b073243b916c6080644` |
| 되읽기 / 쌍 비교 / 계획 CLI | **0 / 0 / 0** |

반대로 **같은 CRLF 파일의 실제 SHA·길이를 정확하게 메타에 쓰면 1 / 1 / 1로 거부**된다. `cases/crlf_lf_metadata`와 `cases/crlf_crlf_metadata`가 두 방향의 증거다. 이 문제는 명령 의미나 물리 결과를 변경하는 반례가 아니라, “이 실제 파일 바이트를 검증했다”는 출처 보증의 결함이다.

**최소 해결:** CLI에서 `read_bytes()` 후 실제 bytes의 hash/length를 먼저 확인하고, 검증한 바이트를 디코딩해 파싱한다. LF만 지원하려면 CRLF를 구체 사유로 거부해도 된다. 정규화 해시를 쓰려면 별도 이름·규약으로 표시하고 물리 파일 해시도 별도로 보존한다. 세 CLI에 양방향 회귀를 둔다.

**재현:**

```bash
python3 -I -X utf8 -B d2/snapshot/scripts/mixer_deck_readback.py --d2 d2/evidence/cases/crlf_lf_metadata/old.in d2/evidence/cases/crlf_lf_metadata/old.meta.json
python3 -I -X utf8 -B d2/snapshot/scripts/mixer_deck_readback.py --d2 d2/evidence/cases/crlf_crlf_metadata/old.in d2/evidence/cases/crlf_crlf_metadata/old.meta.json
```

현재 순서대로 rc0, rc1이다. 짝 비교와 스모크 계획 경로도 동일 결과이며 로그를 보존했다.

## 6. 정상 대조·독립 산술·기존 회귀

- **신규 저자 시험:** 수정하지 않은 `test_mixer_d2_consumers.py` 13/13 PASS. Windows의 자식 Python 출력 인코딩 충돌만 `run_existing.py`에서 `-X utf8`로 고정하고 임시 폴더를 리뷰 작업 공간으로 옮겼다. 제품 코드는 바꾸지 않았다.
- **독립 정상 48조합:** 상2수준 × 밀도세대2 × 코팅비3 × 강성2 × 삽입방식2. 저자 기본값과 다른 N90,007·CGF135·seed49,979,687·Bo1.1을 사용했다. 정상 readback와 D2 pair가 모두 PASS. 인쇄 E·ν·r·ρ·CED를 읽어 별도 식 `A=(4/3)E*sqrt(R*)`, `B=2πR*CED`, `Bo=(B³/A²)/(mg)`로 SE Bo를 대조했다. 정적 모형 식의 검산이지 동적 측정이 아니다.
- 상별 수는 별도 식 `n_i ∝ w_i/(ρ_i d_i³)`에서 계산해 실제 출력 계획 벡터와 대조했다. 이는 실제 삽입 개수의 인증이 아니다.
- **명령 반례·대조9종:** 정상1 + 공통 변조6 + 음성대조2. 각 사례에 API3회와 CLI3회를 실행했다. 중력 변조와 적분기 제거는 세 경로 모두 FAIL/rc1로 발화한다. 관문이 단순히 항상 PASS인 시험이 아니다.
- **구 회귀:** readback24/24. diff54/55(남은 confirm 고정물의 Windows 텍스트 쓰기 문제). 이 실패는 고정물을 동일 텍스트의 LF bytes로 쓰면 FAIL→PASS임을 별도 확인했다(`legacy_windows_newline_diagnosis.json`). 구 smoke 전체 자체시험은 현 Windows 환경에서10실패였으며, POSIX 파일모드/등록 고정물 경로의 영향을 포함한다. 전부에 대한 독립 PASS를 주장하지 않는다. 새 `d2_plan_check` API/CLI는 위 독립 시험에서 직접 호출했다.
- 기준 `486a57cf58d3e0d93ef79be6aae50968929099c0`와 AST 대조에서 세 파일의 기존 함수/클래스91개 중 달라진 공통 함수는 `main`3개뿐이고 나머지88개는 동일, 삭제0이다. 이것은 구 경로 보존의 구조적 근거이지 전체 런타임 회귀 PASS를 대신하지 않는다.

## 7. 내부 독립 GO와 다른 점·해제 증거

| 항목 | 제출된 내부 최종 판단 | 이번 판단 |
|---|---|---|
| 공통 생명주기 변조 방어 | 알려진4종 수정 후 개발 범위 GO | 기본 명령 존재·순서 검사는 개선됨. 옵션/효력 시점/주기 값 변조는 남음 |
| non-CED 토큰 동일성 | 독립 절대 검사와 결합해 D2 비교 보증 | 절대 검사가 놓친 공통 변형에는 방어가 되지 않음 |
| 실제 SHA·바이트 결합 | 검증됨 | 실제 물리 bytes가 아니라 정규화 텍스트로 검증되는 경로 존재 |
| 정상 수치·계획 산술 | PASS | 반대하지 않음. 독립 입력48조합에서도 일치 |

최소 해제 증거는 (1) 위 공통 명령 변조를 세 소비자가 거부, (2) 접촉 제외 거부, (3) 실제 bytes 메타의 정확 결합, (4) 정상 2상/3상·밀도 두 세대·층상/균일·ρ=1 퇴화 비교를 보존한 회귀다. 구 경로 회귀는 지원 실행 환경에서 별도로 재확인하면 된다. 새 S1 수치·정책·실물 자료는 이 코드 종결과 별도다.

**HOLD — D2 개발 소비자의 현재 PASS 경계를 수정·재검증해야 한다. 실제 물리 실행 GO는 발행하지 않는다.**
