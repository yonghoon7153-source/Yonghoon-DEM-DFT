---
title: "리뷰 CK 프롬프트 — A′ V5 VASP 외주 준비본 v6 재리뷰 (CJ NO-GO 대응: 관리 파일 목록 쓰기마다 검사 + 목록 내용 검증 · sha 명령/형식 분리 · 정리 실패 ⚠ · 발송 조건 · 지원 환경)"
date: 2026-09-27
updated: 2026-09-27
tags: [review, codex, adhesion, wad, prereg, vasp, outsourcing, lpscl, silver, uma, d3, dipole, g4, g5, pp-registry, packaging, re-review]
status: 발송 대기 (1저자) — 도구·패키지·개정 3 v6 는 커밋 f4441c426 에 고정 (원격)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 CK — A′ V5 VASP 외주 **준비본 v6** 재리뷰 (CJ NO-GO 대응 확인)

> 트랙 W_ad (점착) → 1저자 = 사용자. 정본 브랜치 `claude/friendly-meitner-lldvar` · **커밋 `f4441c426701bc35690541737d4664a37da4db36`** (아래 해시는 전부 이 커밋의 트리에서 `tools/review_manifest.py --require_pushed` 로 뽑았다 · 원격에 있음).
> 앞 리뷰: CE → v2 → CF → v3 → CG → v4 → CI → v5 (a2374014b) → **CJ NO-GO** (CI 재현 3 경로 해제 확인 · 새 P0 없음 · **같은 P1 의 남은 경로 1 = 관리 파일 목록 쓰기 실패가 뒤 명령 성공에 가려짐**) — 회신 원문 `kb/reviews/codex_CJ_reply_wad_aprime_v5_vasp_outsourcing_v5_2026_09_27.md` · 첨부 zip 13 파일 그대로 `db/raw/codex_CJ_repro_2026_09_27/` (`probe_pack_cj.py --assert-fixed` 가 이번엔 **우리 selftest 안에서도 그대로 돈다**).
> 이번 요청은 **CJ 해제조건**(관리 목록·MANIFEST 쓰기 실패 → 종료 4 · 구본 보존 · 양성 경로 유지)이 채워졌는지, 권고 3 과 S3·S6 의 문구 요구가 맞게 반영됐는지, **새로 생긴 구멍**을 보는 것이다.
> 상황은 그대로: V5 는 RESOURCE_BLOCKED · 업체·예산 미정 · **준비본** · 결정 `D-2026-09-27-wad-aprime-v5-vasp-route` 는 proposed. 판정: GO / 조건부 GO / NO-GO.
> ⚠ selftest 는 합성 패키지 build 단계에서 **simple-dftd3** 가 필요하다. 안 되면 CJ 때처럼 배포본 기준값으로 독립 시험해 주면 된다. 배포본 입력(90 파일 · D3 기준값)은 v3–v5 와 **같다** — 93 파일 중 `jobs.json`·`run_all.sh` 만 바뀌었다.

## §0. CJ P1 → v6 대응 → 음성시험 (한 장)

| CJ | 지적 (요지) | v6 대응 | selftest 음성 (이름 요지) |
|---|---|---|---|
| P1 | `{ echo MANIFEST.sha256; cat mgmt sorted; } \|\| …` 는 앞 `echo` 의 실패를 못 잡고, `[ -f ] && echo >> mgmt` 도 실패를 안 본다 → `echo run/env.txt`·`run/status.tsv` 만 73 이면 **23 구성원** · `echo MANIFEST.sha256` 만 73 이면 **24 구성원** 묶음이 종료 0 · '✅' · `sha256sum -c` 0 · 옛 묶음 교체. `cmp` 는 이미 빠진 목록과 비교하고 sha 는 불완전한 tar 에 대해 정확하므로 못 잡는다 | ① **쓰기마다 검사**: `: > mgmt \|\| fail` · `echo "$f" >> mgmt \|\| fail` (있는 관리 파일마다) · `echo MANIFEST.sha256 > list \|\| fail` · `cat mgmt sorted >> list \|\| fail` ② **목록 내용 검증** (쓰기 실패가 어떤 식으로 가려졌더라도): 줄 수 = 1 + **디스크에 있는 관리 파일 수**(`[ -f ]` 로 센 `n_mg`) + 허용 파일 수 · `grep -qxF MANIFEST.sha256 list` · 디스크의 관리 파일마다 `grep -qxF "$f" list` — 어느 하나라도 아니면 `pack_fail` → 종료 4 · `.part` 삭제 · 옛 쌍 불변. ⚠ 처음엔 줄 수 기준을 **쓴 mgmt 파일의 줄 수**로 두었다가 "이름을 두 번 쓰는" 주입이 통과하는 것을 보고 **디스크 기준**으로 바꿨다 (§3) | **리뷰어 주입 그대로** (`mgmt_echo_error` · `manifest_echo_error`) → 종료 4 · '✅' 없음 · 옛 쌍(바이트) 보존 · 구성원 수 불변 · `.part` 없음 · **변형**: echo 가 관리 이름을 **쓰고도 73** · MANIFEST 를 **쓰고도 73** · 관리 이름을 **조용히 버리고 0** · MANIFEST 를 조용히 버리고 0 · 관리 이름을 **두 번 쓰고 0** (줄 수) · MANIFEST 자리에 **다른 이름**을 쓰고 0 (MANIFEST 존재) · env.txt 자리에 status.tsv 를 쓰고 0 (**줄 수는 맞고** 관리 파일 존재 검증만 잡는다) · `cat` 이 mgmt 만 실패 · `cat` 이 **다 쓰고 73** · `wc` 73 · `wc` 가 맞는 수를 찍고 73 → 전부 종료 4 · **양성**: 주입 없는 PACK_ONLY 종료 0 · 25 구성원 · 잡 파일 없는 run/ → MANIFEST + env.txt |
| 권고 sha | `h=$(sha256sum … \| cut …)` 은 종료값을 잃는다 — 맞는 해시 뒤 73 → 종료 0 · 64 자리 비-hex → 종료 0 (발송 직전 sha -c 만 잡음) | `sha256sum part > tmp/sha \|\| fail` · `h=$(cut … < tmp/sha) \|\| fail` · `[[ $h =~ ^[0-9a-fA-F]{64}$ ]] \|\| fail` — 명령 성공과 형식을 따로 본다 | sha256sum 이 **맞는 해시를 찍고 73** · **64 자리 비-hex** · 빈 출력 · `cut` 73 · `cut` 이 **맞는 해시를 찍고 73** → 전부 종료 4 |
| 권고 정리 | 마지막 `rm -rf tmp` 가 pack 의 반환값 → 정리만 실패해도 종료 4 (묶음·sha 는 정상 · 거짓 실패) | `rm -rf "$T" \|\| echo "⚠ 정리 실패 …"; return 0` — 정리 실패는 포장 실패가 아니다 | 승격 뒤 `rm` 실패 주입 → **종료 0 · '✅' + ⚠** · tmp 남음 · `sha256sum -c` 0 · 구성원 25 (v5 는 종료 4 였다) |
| 권고 문구 | README "종료 0 만 발송" vs "종료 1 도 실패 기록 반송" 충돌 · 계산 성공과 포장 성공을 분리하라 | README 6 · 러너 머리말: **보내는 것 = 일반 실행 종료 0 또는 1**(실패 잡 있음 · 실패도 기록) 뒤 `sha256sum -c` 통과 쌍 · 종료 4 → `PACK_ONLY=1` → 종료 0 + sha 확인 · 종료 2 = 아무것도 안 돎 · "옛 쌍 그대로" 의 예외(둘째 mv → 새 tgz + 옛 sha)를 같은 자리에 적었다 | (문구) |
| S3 | 이름 대조는 유지 · Windows bsdtar 3.8.8 은 `tar tzf` 출력 CRLF 로 거짓 실패 → Linux/GNU 지원 범위 명시 | README 7 · 러너 머리말: **지원 환경 = Linux · bash ≥ 4 · GNU coreutils(find sort grep cmp sha256sum) · GNU tar** · 다른 tar 는 구성원 대조가 거짓 실패(종료 4 · 누출 아님)할 수 있으니 **계산 전 PACK_ONLY smoke**(빈 run/ 에서도 됨) · 개정 3 재개 조건에도 | (문구 · 정규화는 넣지 않았다 — `../`·임의 경로 허용 위험) |

## §1. CJ 의 다른 확인 사항

- **S4·S5** — `TITEL_TRUNCATED` 경계 · 무엔트로피 None 처리는 그대로 (변경 없음).
- **S6** — CI 프롬프트의 "성공 뒤 발송" 은 **포장 성공**으로 좁혀 읽는다는 점을 README 6 에 그대로 적었다 (계산 성공 ≠ 포장 성공).
- (CJ 가 세지 않은 것) `pack_fail` 은 `.part` 둘만 지우고 진단 폴더 `V5_vasp_return.tmp/` 는 남긴다 — 다음 pack 이 처음에 지운다.

## §2. CJ 해제조건 대응

1. **관리 목록·MANIFEST 쓰기 실패 → 종료 4 · 구본 보존** — §0 P1 행 (리뷰어 주입 2 + 변형 10).
2. **양성 경로 유지** — 정상 25 · 준비 실패 · PACK_ONLY 누출 · 잡 파일 없는 run/ · r1 · tar 실패 shim (기존 시험 전부) + **리뷰어 `probe_pack_cj.py --assert-fixed` 그대로 종료 0** (합성 패키지: selftest 안 · 실제 패키지: §3).

## §3. 시험

- `python3 tools/wad/build_v5_vasp_package.py --selftest` → **194/194** (v5 175 + CJ 19 · 실물 원본 대조 1 건 · 리뷰어 스크립트 2 건은 저장소 경로가 있을 때만 — 없으면 SKIP 을 찍고 통과로 세지 않는다).
- **돌연변이 12/12 빨간불** (제품 코드만 깨고 selftest 재실행): 관리 이름 echo 검사 제거 · MANIFEST echo 검사 제거 · 줄 수 검증 제거 · MANIFEST 존재 검증 제거 · 관리 파일 존재 검증 제거 · sha256sum 명령 검사 제거 · 형식을 `.{64}` 로 · `cut` 검사 제거 · 정리 실패를 다시 종료 4 로 · `wc` 검사 제거 · `cat` 검사 제거 · **줄 수 기준을 쓴 mgmt 파일로 되돌림**.
  ⚠ **첫 판은 6/11 이었다** — 관리 목록의 다섯 검사(줄 수 · MANIFEST 존재 · `cut` · `wc` · `cat`)가 살아남았다. 이유는 CI 때와 같다: 내 주입은 **뒤 검사**(줄 수 · 존재 · cmp)가 대신 잡았다. '일은 다 하고 실패를 보고' 하는 주입(echo·cat·wc·cut 이 쓰고/찍고 73) · '이름을 두 번 쓰기' · 'MANIFEST 자리에 다른 이름' · 'env.txt 자리에 status.tsv' 를 더해 12/12.
  ⚠ **그 과정에서 제품 결함 하나를 더 잡았다**: 줄 수 검증의 기준 `n_mg` 를 **쓴 mgmt 파일의 줄 수**로 두었더니 관리 이름이 **두 번** 쓰여도 (mgmt 도 두 줄 · 목록도 두 줄) 통과했고 tar 는 같은 파일을 두 번 담아 26 구성원 묶음을 승격했다 (`cmp` 도 통과 — 목록과 묶음이 같으니까). 기준을 **디스크의 관리 파일 수**로 바꿔 잡았다. CJ 가 지적한 바로 그 형태(검증이 실패한 쓰기 자체를 기준으로 삼는다)였다.
- **리뷰어 재현물 그대로** — `probe_pack_cj.py --assert-fixed` 를 (a) selftest 가 합성 패키지에 (복사본 폴더에서 · 보존본 JSON 을 덮지 않게) (b) 우리가 **실제 패키지 v6** 에 돌렸다: 둘 다 **종료 0** — 주입 17 건 전부 종료 4 · 옛 쌍 보존(둘째 mv 만 선언대로 예외) · positive/recovery/empty_run 종료 0 · **`post_promotion_cleanup_error` 종료 0** (v5 는 4). `repro_ci.py --assert-fixed` 도 실제 패키지에 종료 0.
- 패키지 v5→v6: **입력 90 파일 + D3 기준값 불변** · `run_all.sh` (관리 목록 쓰기 검사 · 목록 내용 검증 · sha 명령/형식 · 정리 ⚠ · 머리말 v6 · 발송 조건 · 지원 환경) · `jobs.json` (schema v6 · 도구 sha) · README (6 · 7 항).

## §4. 질문 (보내기 전 필수 수정만 P0/P1 · 나머지는 권고)

- **S1 목록 내용 검증의 기준** — 줄 수 기준 `n_mg` 를 디스크(`[ -f ]`)에서 세고, 허용 파일 수는 `sorted`(find→grep→sort 산출) 의 줄 수로 센다. 허용 파일 쪽도 디스크와 독립으로 다시 세야 하는가 (find 가 '일은 다 하고 73' 이면 첫 검사가 잡고, 조용히 빠뜨리면 못 잡는다 — 그 경우 묶음도 목록도 같이 빠져 cmp 는 통과한다). 우리 판단: find 의 조용한 누락은 이 계층에서 잡을 수 없고(디스크를 다시 세는 것도 find 다), 수신 검사기가 잡 폴더 결측을 MISSING 으로 막는다 — 러너 계약("포장 실패 = 4") 밖의 잔여로 적어 둔다.
- **S2 `-q` grep 의 예외** — 존재 검증에 `grep -qxF` 를 썼다 (일치 → 0 · 무매치 → 1 · 오류 → 2 이상, 전부 비-0 은 실패로). CJ S2 가 말한 "-q 는 일치를 찾은 뒤의 오류를 숨긴다" 는 예외는 여기서 문제가 되는가 — 우리 판단: 일치 뒤 오류는 '이름이 있다' 는 사실을 바꾸지 않는다.
- **S3 이중 검사의 관계** — 쓰기마다 검사(첫 벽)와 목록 내용 검증(둘째 벽)이 서로를 가린다. 돌연변이는 '일은 다 하고 실패 보고' 주입으로만 첫 벽을 확인한다 — 이 방식이 충분한가, 아니면 첫 벽을 빼고 둘째 벽만 두는 편이 (검사할 코드가 줄어) 낫다고 보는가.
- **S4 발송 조건 문구** — "종료 0 또는 1 + `sha256sum -c`" 로 정리했다. 종료 1 (실패 잡 있음)을 보내는 것이 맞는지 — 실패 잡의 진단(attempt.json · stdout.log · OUTCAR 잘린 것)을 받아야 r1·수동 재실행 판단이 되므로 그렇게 두었다.
- **S5 그 밖에 보내기 전 막는 것** — README(6 · 7) · 개정 3 v6 (러너 v6 · 재개 조건) · 결정 원장.

## §5. 첨부 (커밋 f4441c426 · sha256)

```
db/properties/wad_aprime_pilot_prereg_v5_amendment_3_vasp_v5_2026_09_27.json                        6f7dab9e4be7ef62b30e149cd5bb9bc417983c69c6053bce9007e1107cf19b91
db/inputs/wad_aprime_v5_vasp_2026_09_27/jobs.json                                                   0a7c4caeb5eb91a79a2a288bd08a54e061fe647d0ca09b93c82bff25236831d3
db/inputs/wad_aprime_v5_vasp_2026_09_27/MANIFEST.sha256                                             8118bbc023d6699cd7cd1b6e6afd32872e0699af70b412e15b89365e556ee2f1
db/inputs/wad_aprime_v5_vasp_2026_09_27/run_all.sh                                                  bc507f3119a19bb42a45f395eefdd635c566af2613307abae69db710bfdfdac8
db/inputs/wad_aprime_v5_vasp_2026_09_27/README.md                                                   66f622d4c21c79c6642c496549950aa2d041ce6a539ed368b2ce35224a16c009
tools/wad/build_v5_vasp_package.py                                                                  1d0f4566ab93694c39a3031d041a4751383c5df23db8eacc84e079fc176424be
db/governance/decisions.json                                                                        a50b1f31c77544a5c06b1cfa0a31e841cb218661be1a2b943fec9cd1a15b6c3a
kb/reviews/codex_CJ_reply_wad_aprime_v5_vasp_outsourcing_v5_2026_09_27.md                           49808aab1bdd2206172ebf3b6fe58db6364539fd85cd80bec8bb177801e37e94
db/raw/codex_CJ_repro_2026_09_27/REVIEW_CJ.md                                                       36381b441106d5283ec13adf3cbda26525e8f1e7d3dbcb19a968d9db34105ad7
db/raw/codex_CJ_repro_2026_09_27/probe_pack_cj.py                                                   8b4f3542c74572facb983652e4f2cf16c0fd92fa721e89686afc9f4cdc05a2eb
db/raw/codex_CJ_repro_2026_09_27/pack_cj_results.json                                               ef3f319b0f6bc02d86e22dbee9b48f1f6de2b24f8cfb939909b0f95b0cfd3062
db/raw/codex_CJ_repro_2026_09_27/repro_ci.py                                                        b3a056c46864389ea836fc6b587c779ec5a7c6ee4a6486dd71de3c8f160fdf62
db/pipelines/adhesion_pipeline.json                                                                 ffd01192a9c83486eedc4eba062a9bad4df4ba02d57ac208de114148edb125c3
db/properties/sdcp_c12_v41_partial_raw/prospective/sdcp_neutral__b00__afm2424_pm1/static/OUTCAR.gz  a168ffd15d6657f2e2272fbe3a6f2af416150abb0690cbcd200825af710dee72
db/properties/sdcp_c12_v41_partial_raw/prospective/sdcp_neutral__b00__afm2424_pm1/static/INCAR      a83650c276dce85e5caa570537a439cab1e557254fad3ee8f37174e29f005a7a
db/properties/wad_aprime_s3v2_seal_2026_09_26.json                                                  8862a8e97d007361ee778ff0b643abea870701caabc1429d89c90c20f8b268c2
db/properties/wad_aprime_pilot_prereg_v5_2026_09_25.json                                            3d35dfb9e8fbcbc79c757fe9205fa78437f8e250d9c16522ac14f5ef1f2f0059
```

개정 3 v6 content_digest `sha256:eb5e36fa09b25ba1f3c394e404963d0bdb256a959fa03b4111e5354eb5e14153` · 도구 sha 는 jobs.json 의 `tool_sha256` 과 같다 (`1d0f4566…`). v5 MANIFEST `85bfebdb…` → v6 `8118bbc0…` (jobs/* 90 파일 sha 는 두 MANIFEST 에서 같다). 리뷰어 재현물 네 파일의 sha 는 받은 zip 의 것과 같다 (원문 무수정). 실물 OUTCAR·INCAR 두 줄은 픽스처 출처 확인용이다.

## §6. 회신 형식

판정 (GO / 조건부 GO / NO-GO) → **보내기 전 필수 수정** (P0 · P1, 재현 가능한 근거와 함께 — 재현 스크립트를 첨부해 주면 우리 selftest 가 그대로 돌린다) → 권고 (선택) → S1–S4 에 대한 명시 의견.
