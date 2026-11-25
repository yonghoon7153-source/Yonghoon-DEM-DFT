---
title: "리뷰 CI 프롬프트 — A′ V5 VASP 외주 준비본 v4 재리뷰 (CG NO-GO 대응: 반송 허용 목록 · 봉인 파일럿 결속 · TITEL 접두 규칙 · 권고 3)"
date: 2026-09-27
updated: 2026-09-27
tags: [review, codex, adhesion, wad, prereg, vasp, outsourcing, lpscl, silver, uma, d3, dipole, g4, g5, pp-registry, packaging, re-review]
status: 발송 완료 · 회신 수령 2026-09-27 **NO-GO** (`codex_CI_reply_…` · CG P1 3 해제 · 새 P1 1 포장 오류 처리) → v5 → 재리뷰 CJ 발송 대기
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 CI — A′ V5 VASP 외주 **준비본 v4** 재리뷰 (CG NO-GO 대응 확인)

> 트랙 W_ad (점착) → 1저자 = 사용자. 정본 브랜치 `claude/friendly-meitner-lldvar` · **커밋 `c25e0ce2008b5c33dc6113b249cc8aa22097db2e`** (아래 해시는 전부 이 커밋의 트리에서 `tools/review_manifest.py --require_pushed` 로 뽑았다 · 원격에 있음).
> 앞 리뷰: CE (8f76b912d) NO-GO → v2 (e025c0db7) → CF NO-GO → v3 (c8d77dfd5) → **CG NO-GO** (새 P0 없음 · P1 3) — 회신 원문 `kb/reviews/codex_CG_reply_wad_aprime_v5_vasp_outsourcing_v3_2026_09_27.md` · 붙여 온 결과 JSON `db/raw/codex_CG_repro_2026_09_27/results_pasted.json` (⚠ `repro_cg.py`·`focused_cg.py` 는 받지 못했다 — 재현은 회신의 서술로 했다).
> 이번 요청은 **CG 해제조건 1–3** 이 채워졌는지, **CG 권고 1–3** 의 반영이 맞는지, **새로 생긴 구멍**을 보는 것이다.
> 상황은 그대로: V5 는 우리 GPU 한 장(48 GB)으로 RESOURCE_BLOCKED · 업체·예산 미정 · **준비본** (실행 결정 아님) · 결정 `D-2026-09-27-wad-aprime-v5-vasp-route` 는 proposed. 판정: GO / 조건부 GO / NO-GO.
> ⚠ selftest 는 합성 패키지 build 단계에서 **simple-dftd3** (python `dftd3` API) 가 필요하다 — CF·CG 환경엔 없어 재현을 못 했다. 안 되면 CG 때처럼 배포본 기준값으로 독립 시험해 주면 된다. 배포본 입력(INCAR·INCAR.r1·POSCAR·KPOINTS·POTCAR.spec 90 파일 · D3 기준값)은 v3 과 **같다** — 93 파일 중 `jobs.json`·`run_all.sh` 만 바뀌었다 (README 는 MANIFEST 밖).

## §0. CG P1 → v4 대응 → 음성시험 (한 장)

| CG | 지적 (요지) | v4 대응 | selftest 음성 (이름 요지) |
|---|---|---|---|
| P1-1 | 준비 실패·PACK_ONLY 경로에서 POTCAR 본문(·WAVECAR)이 반송 묶음에 들어간다 — 삭제가 정상 실행 뒤 경로에만 있다 | `pack()` 을 **허용 목록**으로 바꿨다: `run/<잡>/{OUTCAR OSZICAR INCAR KPOINTS POSCAR IBZKPT POTCAR.titel POTCAR.sha256 POTCAR.species.sha256 attempt.json stdout.log}` + `run/status.tsv` · `run/env.txt` · `MANIFEST.sha256` 만 `find … \| grep -E` 로 모아 `tar -T` 로 담는다 (정상·준비 실패·PACK_ONLY 전부 같은 함수). 담은 뒤 `tar tzf` 로 구성원을 검사해 `POTCAR\|WAVECAR\|CHGCAR\|CHG\|vasprun.xml` 이름이 있으면 **묶음을 만들지 않는다 (종료 4)**. 준비 실패(`POTCAR $p 없음`) 때 조립 중이던 `run/<잡>/POTCAR` 도 지운다. 검사기(`return_manifest_info`)는 반송 폴더의 금지 파일을 `return_bundle.forbidden_files` 로 보고한다 (판정 아님 · '저장하지 말고 지워라' 신호 · `--check/--collect` 가 ⚠ 줄로 찍는다). 목록은 파이썬 상수 `RETURN_ALLOWED`/`RETURN_FORBIDDEN` 하나에서 러너·검사기·README 로 간다 | 배포 러너 실제 실행 (bash + 가짜 VASP — 가짜가 WAVECAR·CHGCAR·CHG·vasprun.xml·IBZKPT·EIGENVAL 도 쓴다): **정상 실행** 묶음 = 허용 목록만 (IBZKPT 있음 · EIGENVAL 없음 · 금지 0) · **PP 트리에 Li_sv 만** → 준비 실패 종료 1 · 묶음에 부분 POTCAR 본문 없음 · 폴더의 부분 POTCAR 도 없음 · `✅` 없음 · **중단 뒤 POTCAR·WAVECAR·CHGCAR·vasprun.xml 남긴 폴더에 PACK_ONLY=1** → 종료 0 · 묶음 금지 0 · attempt.json·OUTCAR 는 있음 · 검사기 `forbidden_files` 가 넷을 보고 · `.sha256` 이 최종 파일명으로 쓰여 `sha256sum -c` 통과 |
| P1-2 | 등록부 `from_pilot` 은 형식만 검사 — 반송 파일럿 run_id 를 다음 날 ID 로 바꿔도 실제 CLI 가 rc 0 · G5 PASS | `check()` 끝에 **파일럿 결속**: 등록부가 있으면 파일럿 두 잡의 **채택 시도**(0 또는 정당한 r1 · 최종 상태 OK 인 것)의 `run_id == from_pilot[job]` 이어야 하고, 같으면 다시 `attempt.json`·`OUTCAR` sha 가 등록부 `from_pilot_sha256[job]` (봉인 당시 `seal_pp` 가 기록 · 등록부 **schema v3** · `validate_pp_registry` 가 필수 검사) 과 같아야 한다. 어긋나면 그 잡 = **`PILOT_NOT_SEALED`** (자동 교체 없음 · `why` 에 두 ID) → 잡 미완 → `--collect` 종료 3 · G5 `INCOMPLETE (분모 5)` · ① `total_w_citable` false. `check_job` 이 `attempt_json_sha256`·`outcar_sha256` 을 결과에 남긴다 | 반송 far 파일럿 run_id 를 `20260928T120000-99-456` 로 교체 → `PILOT_NOT_SEALED` (등록부 없이는 OK 인 정상 출력) · 그 상태 집계 → 종료 3 · 사용 자격 false · ① 인용 불가 · **실제 CLI** `--collect --pp_registry --pp_registry_sha256` → **종료 3** (리뷰어 재현은 0) · 같은 run_id 인데 OUTCAR·attempt.json 을 바꿈 → `PILOT_NOT_SEALED` (sha) · 봉인 그대로 → 두 파일럿 OK · 집계 종료 0 · **r1 로 봉인한 파일럿** → 최종 검사에서 r1 채택 · 결속 OK (양성 경로) · 첫 시도로 봉인한 등록부에 r1 채택 파일럿 → `PILOT_NOT_SEALED` · v2 등록부(from_pilot_sha256 없음)·sha 형식 틀림 → 검사·집계 시작 안 함 · 러너 산출물로 봉인한 등록부 + 그 산출물 → 결속 OK |
| P1-3 | 정상 POTCAR 기록 + OUTCAR 에 올바른 첫 TITEL 만 + rc 1 → POTCAR_MISMATCH 로 r1 을 막았다 (결측을 모순으로) | `check_job` 의 OUTCAR TITEL 대조를 셋으로 갈랐다: (a) 같음 → 통과 · (b) **정상 접두** = 관측 목록이 기대 목록보다 짧고 `titel[:len(ot)] == ot` (같은 순서 · **완전한 문자열** 일치) → 모순 아님 — 미완료 시도(rc ≠ 0 · 미종료)는 r1 자격 그대로, **성공 시도**(rc 0 · 종료 · 수렴)인데 접두만이면 ③ 완결성에서 `POTCAR_UNVERIFIED` (통과·r1 자격 아님) · (c) 그 밖(다른 종·다른 날짜·순서 바뀜·기대 뒤에 추가) → 즉시 `POTCAR_MISMATCH` (모순 · r1 자격 없음). 모순 검사의 위치(실행 상태 앞)는 그대로다 — CF P0-1 경로는 안 열린다 | 올바른 첫 TITEL 만 + rc 1 (미종료) + 정상 r1 → **r1 채택** (리뷰어 재현: POTCAR_MISMATCH) · TITEL 셋까지 + rc 1 + r1 → r1 채택 · **순서 바뀜 · 첫 TITEL 날짜 다름 · 둘째 종 다름(P→P_h) · 기대 전부 뒤에 Fe 추가 · Fe 하나** + rc 1 + 정상 r1 → 전부 `POTCAR_MISMATCH` · `r1_ignored` · `conflicts` 있음 · 성공 시도(rc 0 · 종료 · 수렴)인데 TITEL 둘만 → `POTCAR_UNVERIFIED` (r1 있어도 승격 안 함 · r1 없어도 통과 아님) · CF 의 여섯 조합(ENCUT 400 + rc 1 등)은 그대로 모순 |

## §1. CG 권고 1–3 대응 (선택 권고였지만 전부 반영)

- **권고 1 빈 에너지 레코드** — 에너지·Edisp 정규식을 `…=[ \t]*(\S*)` 로 바꿨다: 레코드의 존재는 머리말(`TOTEN =` 등)이 정하고 값은 **같은 줄**의 다음 토큰이다 (없으면 빈 값 → `_tok_float("")` → None). 값 패턴이 줄을 넘지 않으므로 다음 줄의 토큰을 집어 오지 않는다. 음성: 정상 최종 구획 뒤 EOF 에 `free energy TOTEN =` 만 → TOTEN None (E(σ→0)·E(무엔트로피)는 그대로) · 빈 σ→0 · 빈 무엔트로피 · 빈 `Edisp (eV)` · 빈 Edisp 다음 줄이 `FREE ENERGIE` 여도 None. 실물 5.4.4 픽스처 판독(TOTEN −1151.29778848 · E(σ→0) −1151.29228248 · Edisp −28.80731)은 불변.
- **권고 2 tar·sha 쌍 승격** — `.tgz.part` 를 만들고 구성원 검사 → sha 를 `.tgz.sha256.part` 에 **최종 파일명**(`V5_vasp_return.tgz`)으로 쓰고 → 둘 다 완성된 뒤 `mv` 둘 (tgz 먼저). 어느 단계가 실패해도 옛 tgz·옛 sha 쌍은 그대로 남고 종료 4. 음성: `sha256sum -c V5_vasp_return.tgz.sha256` 통과 (돌연변이 '.part 이름으로 sha 기록' 은 빨간불). 두 `mv` 사이의 순간은 남아 있다 (원자적 쌍 교체는 파일시스템이 안 준다) — 뒤 `mv` 가 실패하면 새 tgz + 옛 sha 가 잠깐 공존할 수 있고 러너는 종료 4 를 낸다.
- **권고 3 등록부 증거 확장** — `seal_pp` 가 `from_pilot_sha256 = {잡: {attempt.json: sha, OUTCAR: sha}}` 를 기록 · schema `aprime_v5_pp_registry/v3` · `validate_pp_registry` 가 두 잡 · 두 키 · 64 hex 를 필수로 본다 (없으면 v2 등록부로 취급 → 시작 안 함) · `check()` 가 run_id 다음에 이 sha 를 대조한다 (§0 P1-2).

## §2. CG 해제조건 대응

1. **정상·준비 실패·PACK_ONLY 모두 묶음에 POTCAR 본문 없음 — 실제 압축 구성원 검사로 입증** — §0 P1-1 행 (selftest 는 `tarfile.getnames()` 로 구성원을 읽는다) + **실제 재생성 패키지 v4** 로 같은 셋을 돌렸다 (§3 끝-끝).
2. **봉인 등록부 ↔ 채택 파일럿 run_id 불일치를 실제 CLI 에서 차단 · 정상 파일럿/r1 재사용 양성 경로 유지** — §0 P1-2 행 (합성 패키지 CLI 3 · 실제 패키지 CLI 3 · r1 봉인 양성).
3. **미완료 OUTCAR 의 정상 TITEL 접두 = 결측 · 잘못된 종·순서 = 모순 · 정상 r1 살림 · CF 세탁 경로 계속 차단** — §0 P1-3 행 + CF P0-1 여섯 조합 시험 그대로 통과.

## §3. 시험

- `python3 tools/wad/build_v5_vasp_package.py --selftest` → **155/155** (v3 130 + CG 25 · 실물 원본 대조 1 건은 저장소 경로가 있을 때만).
- **돌연변이 13/13 빨간불** (제품 코드만 깨고 selftest 재실행 · 각 6 초): 허용 목록 끄고 `run` 통째 tar · 준비 실패 시 부분 POTCAR 삭제 제거 · 파일럿 결속 블록 제거 · sha 결속만 제거 · 등록부 `from_pilot_sha256` 필수 해제 · TITEL 접두 규칙 되돌림(접두도 모순) · 접두 규칙 과대(문자열 안 보고 길이만) · 성공 시도 접두를 통과시킴 · 에너지 정규식 `\S+` 되돌림 · `forbidden_files` 항상 빈 목록 · `seal_pp` 가 sha 안 기록 · sha 파일을 `.part` 이름으로 · 묶음 목록에서 status.tsv·env.txt 제외. ⚠ 둘('등록부 필수 해제' · 'seal_pp sha 안 기록')은 assertion 이 아니라 **예외**로 죽었다 (필수 검사가 빠지면 뒤 코드가 KeyError · 봉인이 스스로 검증에 실패) — 빨간불이긴 하지만 깨끗한 신호는 아니라 적어 둔다.
- ⚠ **닿지 않는 방어 한 줄**: `pack()` 안의 `tar tzf … | grep -Eq "(^|/)(POTCAR|…)$"` 구성원 검사는 허용 목록이 멀쩡하면 **절대 발화하지 않는다** (허용 목록이 그 이름을 낼 수 없다). 허용 목록이 깨졌을 때의 두 번째 벽으로 두었고, 이 줄의 돌연변이는 세지 않았다 (시험이 도달할 수 없다).
- **시험 픽스처 변경**: 합성 시도의 run_id 를 잡·시도마다 **고정**(`…-4242-<잡번호><0|1>`)으로 바꿨다 — 같은 내용으로 다시 만들면 같은 실행 기록이 돼야 결속 시험이 성립한다. 가짜 VASP 가 WAVECAR·CHGCAR·CHG·vasprun.xml·IBZKPT·EIGENVAL 도 쓴다.
- **실제 재생성 패키지 v4 끝-끝** (bash 러너 + 가짜 VASP · 파일럿 2 잡): 묶음 **25 구성원 · 금지 0** · `sha256sum -c` 0 → `--check` 파일럿 OK (16 잡 MISSING → 3) → `--seal_pp` (schema v3 · 실제 run_id `20260927T125342-…` · sha 두 키) → `--collect` 등록부 없이 **2** · `--collect --pilot` 3 → `--check` + 등록부 → 파일럿 OK · 등록부 검증됨 · forbidden 0 → **far run_id 교체** → `PILOT_NOT_SEALED` · `--collect` **3** (리뷰어 재현은 0) → **PACK_ONLY 누출**(POTCAR·WAVECAR 남김) → 종료 0 · 묶음 금지 0 · 검사기 보고 2 → **준비 실패**(Li_sv 만) → 종료 1 · 묶음 금지 0 · 폴더 POTCAR 없음.
- 패키지 v3→v4: **입력 90 파일 + D3 기준값 불변** · `run_all.sh` (허용 목록 · 구성원 검사 · 부분 POTCAR 삭제 · tar/sha 쌍 승격 · 머리말 v4) · `jobs.json` (schema v4 · 도구 sha · `return_allowed`/`return_forbidden` · 등록부 schema v3) · README (허용 목록 · 파일럿 결속 문구 · 손 tar 금지).

## §4. 질문 (보내기 전 필수 수정만 P0/P1 · 나머지는 권고)

- **S1 허용 목록의 경계** — 이름 기준 허용 목록(11 개 + 3)으로 충분한가. 빠져서 나중에 아쉬울 파일(CONTCAR · XDATCAR · PCDAT · REPORT)이 있는가 — 단일점이라 넣지 않았다. `stdout.log` 는 VASP 표준출력이라 내용을 못 거른다 (VASP 는 POTCAR 본문을 출력하지 않는다고 본다).
- **S2 파일럿 결속의 표현** — "run_id + attempt.json·OUTCAR sha 가 봉인과 같다" 가 CG S2 의 **봉인 파일럿 재사용 검증**을 말하기에 충분한가. `PILOT_NOT_SEALED` 를 **잡 상태**(그 잡만 미완 → 종료 3 · G5 분모 INCOMPLETE)로 두었다 — 집계 자체를 거부(종료 2)하는 쪽이 나은가. 우리 이유: 나머지 16 잡의 진단은 보이는 채로 두고 싶다.
- **S3 TITEL 접두의 정의** — "완전한 문자열의 목록 접두" 로 좁게 두었다. **줄 중간에서 잘린 마지막 TITEL** (예: `PAW_PBE Ag 02Ap`) 은 접두가 아니라 **모순**으로 막힌다 (fail-closed · 그 잡은 새 승인 없이는 r1 을 못 쓴다). 이걸 "마지막 항목은 문자열 접두 허용" 으로 넓혀야 하는가 — CG 는 '관측된 **완전한** TITEL' 이라고 했고, 넓히면 잘린 줄과 다른 PP 의 경계를 문자열로 가르게 돼 좁게 두었다.
- **S4 금지 파일 보고의 강도** — 검사기는 반송 폴더의 POTCAR 본문 등을 **보고만** 한다 (판정에 안 쓴다). 값의 타당성과 무관해서다. 라이선스 위생 때문에 종료 2 로 거부해야 한다고 보는가.
- **S5 권고 2 의 남은 틈** — 두 `mv` 사이 새 tgz + 옛 sha 공존 순간 (종료 4 로 드러남). 더 할 것이 있는가 (예: sha 파일에 tgz 크기도 기록).
- **S6 그 밖에 보내기 전 막는 것** — README(업체용 · 허용 목록 · 파일럿 결속 · 손 tar 금지) · 개정 3 v4 의 `결속_금지_서술` (등록부 검증 = PP·버전 신원 + 봉인 파일럿 재사용, 두 문장을 섞지 않음) · 파일럿에서 실제 버전·NGZF·min pos·기대 cut·격자 편차를 기록한다는 S4(CG) 후속.

## §5. 첨부 (커밋 c25e0ce20 · sha256)

```
db/properties/wad_aprime_pilot_prereg_v5_amendment_3_vasp_v5_2026_09_27.json                        eeaa6f08157609d96216b8ed9e374da4001a9a7fd3246a71b96404b888b88f0b
db/inputs/wad_aprime_v5_vasp_2026_09_27/jobs.json                                                   794fb7223c60250471e34fc070852aa8fc2526b08ccf20b085d0406b3d040610
db/inputs/wad_aprime_v5_vasp_2026_09_27/MANIFEST.sha256                                             ccbc0988f6debfa716e1c2e2d7f7327939cc41cd378a3d0a35f5523ed11bcfb5
db/inputs/wad_aprime_v5_vasp_2026_09_27/run_all.sh                                                  6bf58a7a20e1ee8102d09b1ec712a7351062f869ea3898c5b9a48545e9affa25
db/inputs/wad_aprime_v5_vasp_2026_09_27/README.md                                                   120452af7dc7e8e423cfa37b6c59cc6066863ee5d48facd0fe7b959fbd9cd6bf
tools/wad/build_v5_vasp_package.py                                                                  f35606c6eeda9bbcc893d3ef77c7d39e18b46edf8b9267bee1d6652bf48f8494
db/governance/decisions.json                                                                        b1e5291a226765d4a9c1e16e104aed3a7d237c34a86364e6b559089cfac782ea
kb/reviews/codex_CG_reply_wad_aprime_v5_vasp_outsourcing_v3_2026_09_27.md                           0a4f450e139cb0b041658c26722e6a8c161e75302eee1979ab99cc278ba03193
db/raw/codex_CG_repro_2026_09_27/results_pasted.json                                                8d380b02dd32f245f2fc813ee85ab671927a5fed9c545f4c4798fcc7de5856ae
db/pipelines/adhesion_pipeline.json                                                                 17ce0f7ce573179b661cbbf02aeb27d634e8ab1195c86f77fbe7c78f43000b66
db/properties/sdcp_c12_v41_partial_raw/prospective/sdcp_neutral__b00__afm2424_pm1/static/OUTCAR.gz  a168ffd15d6657f2e2272fbe3a6f2af416150abb0690cbcd200825af710dee72
db/properties/sdcp_c12_v41_partial_raw/prospective/sdcp_neutral__b00__afm2424_pm1/static/INCAR      a83650c276dce85e5caa570537a439cab1e557254fad3ee8f37174e29f005a7a
db/properties/wad_aprime_s3v2_seal_2026_09_26.json                                                  8862a8e97d007361ee778ff0b643abea870701caabc1429d89c90c20f8b268c2
db/properties/wad_aprime_pilot_prereg_v5_2026_09_25.json                                            3d35dfb9e8fbcbc79c757fe9205fa78437f8e250d9c16522ac14f5ef1f2f0059
```

개정 3 v4 content_digest `sha256:dbcbc486f54e5a05fc1b72430f7f7f0b8c7ef0f7f4866d79ce048676b5cb5e2f` · 도구 sha 는 jobs.json 의 `tool_sha256` 과 같다 (`f35606c6…`). v3 의 MANIFEST `da260794…` → v4 `ccbc0988…` (jobs/* 90 파일 sha 는 두 MANIFEST 에서 같다 — 확인해 주면 좋다). 실물 OUTCAR·INCAR 두 줄은 픽스처 출처 확인용이다 (다른 계 · V5 결과 아님).

## §6. 회신 형식

판정 (GO / 조건부 GO / NO-GO) → **보내기 전 필수 수정** (P0 · P1, 재현 가능한 근거와 함께 — 가능하면 재현 스크립트도 붙여 주면 우리 쪽 음성시험으로 옮긴다) → 권고 (선택) → S1–S5 에 대한 명시 의견.
