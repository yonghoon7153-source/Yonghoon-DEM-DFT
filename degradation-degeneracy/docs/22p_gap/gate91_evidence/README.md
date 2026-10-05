# 91차 제출자 증거 — 원문 로그 (G90-N1 정정 — 환경 프로필 C 의 origin 축을 경로 검색 범위로 · 이름 · `not_measured` · 문구 · C1)

스크래치패드 원문을 **바이트 그대로** 옮겼다. `.gitattributes` 의 `docs/22p_gap/gate91_evidence/** -text !eol` 규칙은 증거 로그를 넣기
**전에** 더했다 (`4b32db749`). `.gitignore` 의 `*.log` 때문에 로그는 `git add -f` 로 넣었다. 셸 래퍼 안의 절대 경로는 제출자 세션의
스크래치패드다. 편집한 파일은 이 README 하나다. 줄머리 집계는 고정 (`^물었다` · `^★ 안 물었다` · `^★ 실행오류`). 각 로그의 첫 줄 · 끝 줄은
래퍼가 쓴 HEAD · dirty · source_digest · 시각이다.

| 파일 | 무엇 | 실행 상태 |
|---|---|---|
| `00_red_test_gate90_91_38failed_5passed.log` | RED `pytest tests/test_gate90_env_profile.py tests/test_gate91_env_profile_scope.py -rA` — **38 failed / 5 passed** (test_gate90 의 `_assert_closed` 33 · test_gate91 5 · 통과 e01 · e07 · e09 · e11 · e12) · 머리 `source_digest 3f84c0db52d2b9ac` | `4b32db749` (= RED `e06e0cd6d` + 규칙 · 코드 `e2160c2ef` 그대로) · dirty 0 |
| `00b_kexpr_overlap_registry410_new_nodes5_overlap0.txt` | 등록부 `-k` 410 (k 없는 선언 11 제외) 을 pytest `KeywordMatcher` 로 새 node 5 에 대 본 출력 — 겹침 **0** · collect rc 0 | 같은 작업 트리 |
| `01_green_test_gate90_91_43passed.log` | GREEN — **43 passed** · 머리 `source_digest f0175fff71132003` | `b9abe993c` + GREEN 작업 트리 (= `b08bb6944`) |
| `02_related_modules_10failed_stale_receipt_identity.log` | 관련 10 모듈 — **577 passed / 10 failed** · 10 = "영수증이 낡았다 — validator `3f84c0db52d2b9ac` ≠ 현행 `f0175fff71132003`" (예상) · 끝 HEAD 같음 · dirty 0 | clean `b08bb6944` |
| `03_replay_g9_emit_expect_15killed_g90_witness_unchanged.log` | `-k g9 --emit-expect` — 15 변이 (-g90 13 + -g91 2) 모두 기대 node 사망 · -g90 13 은 EXPECT 선언이 있어 줄머리 `물었다` (관측 = 기존 EXPECT) · -g91 둘은 EXPECT 미선언이라 `★ 안 물었다` · rc 1 | `fe0cdfb06` + 등록 작업 트리 (→ `3b019c9e9`) |
| `04_replay_g9_verify_15_rc0.log` | `-k g9` (EXPECT 15) — **15/15 물었다 · rc 0** · scenario 15 · site 15 | 작업 트리 → `3b019c9e9` |
| `06_make_receipt_7ff263197_rc0.log` | `make_receipt.py paired_fixed5_v4 grid_fit_v5` — rc 0 · 35 · 34 · core `1e3ea7c8…` · `23c78ed0…` | clean `7ff263197` → `f27006370` |
| `06b_make_receipt_check_core_identical_rc0.log` | `make_receipt.py --check …` — 두 leg core 재생성 **바이트 동일** · rc 0 | `7ff263197` + 재생성 · 앵커 작업 트리 → `f27006370` |
| `07_receipt_modules_after_regeneration_113passed.log` | 재생성 뒤 `test_gate70/71/72/74_defensive` — **113 passed** (02 의 10 건이 닫힘) | 같은 작업 트리 → `f27006370` |
| `08_env_profile_json_f27006370_match.log` | `python -m tools.env_profile --json` — **MATCH** · rc 0 · `path_origins_in_record` 9 · `not_measured` [`loaded_module_origin`] · 시작 HEAD = 끝 HEAD · dirty 0 | clean `f27006370` |
| `10_full_pytest_f27006370_2182passed.log` | 전체 `pytest tests/ -q -rfEx -p no:cacheprovider` — **2182 passed / 1 xfailed / rc 0** · 23:55:11Z → 00:52:41Z (0:57:27) · 시작 HEAD = 끝 HEAD · dirty 0 | clean `f27006370` |
| `11_smoke_f27006370_rc0.log` | `./scripts/smoke_e2e.sh` — **rc 0** · 기록 단계 줄 MATCH (새 문구 "경로 검색 origin 의 RECORD 소속 9 (로드된 module origin 미측정)") · 00:52:42Z → 00:55:27Z (2:45) · 시작 HEAD = 끝 HEAD · dirty 0 | clean `f27006370` |
| `12_full_replay_f27006370_412_of_412_rc0.log` | 등록부 전체 재생 (`-k` 없음 · 분리 프로세스 · 시간 상한 없음) — **scenario 423 (executable 412 · declared 11) · site 461 · ran 412 · 412/412 call 단계에서 선언한 이유로 물었다 · ★ 0 · rc 0** · 00:55:28Z → 03:30:08Z (2:34:40) · 시작 HEAD = 끝 HEAD · dirty 0 | clean `f27006370` |

## 전체 sha256 · 크기 (바이트)

```
ecececb2f5622c7c553b032b01888fa22c6d227601d5dd41d93b0d30abb856a0  69826  00_red_test_gate90_91_38failed_5passed.log
aa922d8f18669e4b08b0d4644289d66a3d42499c8f10978fb8d1cad26a9e0c9f  1262  00b_kexpr_overlap_registry410_new_nodes5_overlap0.txt
ca68c1dffcbcbfec519e607799127cb10edf1dbae59c22108bfa3a1c91f96f9d  5558  01_green_test_gate90_91_43passed.log
04f96905949f8f96195e008376d21087a7fa7ebf7a8c8508b4994b9b5f7b3269  30701  02_related_modules_10failed_stale_receipt_identity.log
44932b9c6108f31d5bc5e127a7464a8722c04262c72cdc11505f79db3cf28613  10096  03_replay_g9_emit_expect_15killed_g90_witness_unchanged.log
c4485a703e6ab0b59fae52cdd47f38c0447f892851edbc3cd243a31ea38e9a37  2114  04_replay_g9_verify_15_rc0.log
d935c79df9a83a34a0c11bdf30ea59ecc2ef497556bbe1acbfa0b50e222097ec  541  06_make_receipt_7ff263197_rc0.log
de32e700c9f305f8e56048388451969b3e72b3c9b2585b9cfa8e1aaf400f0ca4  508  06b_make_receipt_check_core_identical_rc0.log
50a831970c469d2611790dc4738156f69e262a988ad4ab355998f00cff56559d  1176  07_receipt_modules_after_regeneration_113passed.log
7680c439e2f7523d57da02b6fd7a1c68a531cfc3ad20e4682578a2b3fbe06cac  998  08_env_profile_json_f27006370_match.log
22ee5dd1ba546ae5d2d39efae2546c5f1ba299ae178c05d4c7604a8ad5e33013  3646  10_full_pytest_f27006370_2182passed.log
541ca7e35b0ee6a7ff836806a2ae6ce3f31cce63362ff1a946d2838acaa13550  6599  11_smoke_f27006370_rc0.log
b648960fce8799bbd0985fda5aec76d05a6e38791f25911e46fa7b7ded4ed6d3  53873  12_full_replay_f27006370_412_of_412_rc0.log
```

## 없는 것 (그대로 적는다)

- 번호 05 · 09 · 13 은 비워 두었다 — 05 (GREEN 뒤 재실행) 는 이번에 필요한 단계가 없었다 · 09 (재생성 뒤 영수증 모듈) 는 90차처럼 07 로
  앞당겼다 · 13 (고정 표 커밋의 docs-lint 보충) 은 이번에 돌리지 않았다.
- 발송 HEAD 의 docs-lint 는 발송문에 적는다 (이 README 가 든 커밋보다 뒤라서). 발송 뒤 그 원문을 14 번으로 덧붙인다.
