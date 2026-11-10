# Rint ② 회차 ⑥ — 현장 점검 전달 증거 독립 대조

검토 핀: `aec8ca2f6cbc24d43e2ed447c61ce6b62dd19f1e`.
현장 점검 기록의 실행 핀: `db86ce9b955c2aa13430680f79a431e8a580ed83`.

판정: **전달된 비식별 JSON·로그의 내부 대조 및 고정 소스 기대 지문은 수용. 중첩 README 봉인 1건은 수정 필요(P3).** 실제 호스트 재실행·연구 계산·siteq 도구 실행은 하지 않았다. 원본 호스트 tgz 진위나 생산 실행 자격을 이 대조로 확정하지 않는다.

## 1. 독립 재계산

`audit_siteq_evidence.py`는 대상 모듈을 import하지 않고 파일 bytes, AST 상수, JSON과 로그를 읽는다. `counts` 자기신고를 신뢰하는 대신 `checks` 개별 항목의 상태를 다시 세고, 로그 각 행의 ID/상태/제목/상세 문장을 대응 JSON 항목과 대조했다.

| 항목 | kgy | gabia |
| --- | --- | --- |
| 개별 JSON 관측 / 실제 로그 관측 행 | 33 / 33 | 33 / 33 |
| 도구의 고정 CHECKS와 ID·제목·순서 | 33개 일치·중복 없음 | 33개 일치·중복 없음 |
| 상태 재계산 | PASS 25 / INFO 8 | PASS 24 / INFO 9 |
| WARN / FAIL / ERROR | 0 / 0 / 0 | 0 / 0 / 0 |
| 로그 ID·상태·제목·상세 대 JSON | 33/33 정확히 일치 | 33/33 정확히 일치 |
| `<HOME>` 토큰 JSON / 로그 | 25 / 2 | 21 / 2 |
| elapsed / UTC 반올림 | 14.7 s / 15 s | 17.5 s / 18 s |
| C13b | PASS, 읽기 전용 ledger 거부/공유 관측 | INFO, root의 권한 무시 가능성 표지 |
| C26 계획 폴더 포함 | 포함 | `plan_dirs=""`, 미포함 |

근거: `docs/data/rint2_siteq_20261109/{kgy,gabia}/siteq.log:2–34`; 상태 합계 로그 35행. JSON 총계는 kgy 869행, gabia 828행이지만 독립 대조는 이 칸을 세지 않고 각 `checks` 항목을 셌다. 도구의 고정 목록은 `docs/reviews/rint2_siteq_prep_20261109/tools/siteq_probe.py:1029–1063`이다.

준비 문서의 예상과 다른 기록은 찾지 못했다. C02=PASS, C28=INFO, gabia C13b=INFO, C26=PASS가 실제 관측과 맞는다. PASS는 각 도구 조건의 통과이며 서로 다른 의미의 33관측을 연구 검증 33건으로 합산하지 않는다.

## 2. 세 SAME 및 소스 지문

| 비교 | 재계산 |
| --- | --- |
| pin | 양쪽 `db86ce9b955c2aa13430680f79a431e8a580ed83` |
| C02 환경 같음 단위 | 양쪽 `numpy=1.24.4`, `python_minor=3.8`, `scipy=1.10.1` |
| C04 코드 키 | 양쪽 `095af7ab8bcced0ca2489fe09b7cb9b48da0727ba37c9ea1eb8a8e98c987d21d` |
| 제공된 siteq 도구 bytes | SHA256 `a490b9adc3eeb7468b051b32bdaa0110879b71322a3a2cfb3b723505a3df8588`, 양쪽 `probe_sha256`와 일치 |

근거: kgy JSON 101–158행·881–884행, gabia JSON 94–151행·840–843행. 도구가 실행 스크립트 자체를 해시하는 위치는 1127행이다.

추가로 이전 회차 ⑤ 패킷에 포함된 동일 scripts 트리의 19개 `CODE_FILES`를 실제 bytes로 SHA256 계산했다. `rint_r_chain.py:335–339`의 순서, 1902–1913행의 키 구성, 3591–3592행의 해시 규칙을 별도 Python 산술로 재구성했다. 실행 HEAD를 위 현장 핀, 환경 단위를 위 세 버전으로 놓은 **기대 코드 키도 `095af7...`로 정확히 일치**한다. 소스 실행·모듈 import 없이 얻었다. 전체 19개 입력 SHA와 정준 키 입력은 `audit_result.json/code_key_reconstruction`에 보존했다.

이 보강의 전제인 회차 ⑤/현장 db86/검토 aec의 scripts 트리 동일성은 주 검토의 별도 Git 트리 대조에 연결한다. C04 원 JSON은 `code_key_sha256`, 파일 개수, 결손 목록만 저장하고 현장 `code_record` 전체를 저장하지 않는다(도구 393–401행). 그러므로 위 결과는 **고정 소스와 신고된 핀/환경의 기대 키 일치**이며 현장 파일을 다시 읽었다는 뜻은 아니다.

주 검토에서 19개 실제 bytes가 원격 scripts 트리의 Git blob과 일치함도 대조했고(`codekey_sources.json`), 재현용 읽기 사본을 `codekey_sources/scripts/`에 넣었다. 마지막 감사 실행은 이 동봉 사본을 사용했으므로 과거 외부 작업 폴더에 의존하지 않는다.

C02 SAME은 등록된 세 버전 문자열에 한정한다. 두 기계의 CPU, OS/glibc, SIMD 기능 목록, GPU가 서로 다른 사실도 그대로 남아 있다. 수치 결과 동일성·CUDA 자격·전체 실행환경 동일성을 뜻하지 않는다.

## 3. 새 발견 — RR6-EV-01 / P3: 준비 README의 중첩 봉인만 낡음

대상: `docs/reviews/rint2_siteq_prep_20261109/SHA256SUMS:1`.

관측:

```text
봉인값 README.md = 6401d4f9a2850946588e4929326c13ff319827720f47f55165f69c748f7859f2
실제 핀 README.md (56,403 B) = c9a11392c24343b1130ef27257873f8c807752b3f0e772d7a200392d6e184f53
```

최상위 패킷 SHA256SUMS는 현재 README를 올바르게 봉인한다. 내부 준비 묶음은 5행 중 이 README 하나만 실패하고 도구·틀·두 summary 4행은 일치한다. 데이터 묶음 SHA256SUMS 4/4, 최상위 해당 12파일은 모두 일치한다. 준비 README 351행은 그 SHA256SUMS를 현재 위 파일들의 해시 목록으로 소개하고, 과거 버전 전용이라는 표지가 없다. 결과 안내 추가 뒤 옛 README SHA가 남은 범위다.

무너지는 결론: “제공된 모든 중첩 봉인을 현재 고정 바이트에 대조하면 전부 통과한다.”
무너지지 않는 결론: 도구 a490... 자체, 현장 비식별 JSON·로그 넷, 상태 집계·세 SAME 및 기대 코드 키 일치.

최소 수정: 다음 문서 커밋에서 내부 README 해시를 현재 바이트로 갱신하거나, 옛 준비 스냅샷의 해시 목록임을 명시하고 그 스냅샷을 별도로 보존한다. 현장 점검·연구 계산 재실행이 필요한 결함은 아니다. 코드/자료 수정은 본 검토에서 하지 않았다.

재현(리포 루트에서 읽기만):

```bash
python -c "import hashlib,pathlib; p=pathlib.Path('docs/reviews/rint2_siteq_prep_20261109'); print((p/'SHA256SUMS').read_text().splitlines()[0]); print(hashlib.sha256((p/'README.md').read_bytes()).hexdigest())"
```

## 4. 증거 한계 — 추가 결함으로 과장하지 않는 것

1. **원본과 비식별 사본 구분.** 데이터 README 4행·11–16행·22–25행은 원본을 동봉하지 않고 해시만 기록했다고 명시한다. 이 패킷으로 확인한 것은 비식별 사본의 bytes와 일관성이다. `<HOME>` 발생 횟수는 맞지만 “홈 치환 외 원본 bytes 전부 동일”과 원본 tgz/JSON/log SHA의 진위는 원본 부재로 독립 확인하지 못한다. 고정 해시는 내용 일관성 근거이며 현장 진위 인증이 아니다.
2. **rc0는 직접 영수증이 아님.** 데이터 README 41행은 1저자 화면 보고라고 한정한다. 로그와 JSON에 독립적인 최상위 셸 종료 코드 영수증은 없다. 0 FAIL/ERROR는 도구 1137–1143행의 예상 rc0와 정합한다. 이를 “원 로그에서 rc0를 직접 확인했다”로 바꾸면 안 된다.
3. **gabia 계획 폴더 미점검.** gabia JSON 841행은 빈 `plan_dirs`; C26은 home/out/repo만 기록한다. 현재 기록을 향후 계획 디렉터리의 flock·rename·권한·가용공간 검증으로 전용할 수 없다. 데이터 README 69행은 이 한계를 이미 보존한다.
4. **INFO를 통과 규율로 재해석하지 않음.** gabia의 root와 kgy의 umask002/new664는 관측 사실이다. root에서 권한 기반 보호, 같은 그룹 사용자의 접근 통제, 실제 저장장치의 장애 내구성은 별도 문제다. 도구 테스트 중단/종료·복구 관측을 12단위 끝-끝이나 GPU payload 실행으로 확대하지 않는다.

## 5. 재현 산출물

```powershell
python -I -B -X utf8 audit_siteq_evidence.py --package <round6-package> --code-scripts <동봉-codekey_sources/scripts> --out audit_result.json
```

이 감사 명령의 rc는 **1이 정상 재현**이다. 위 P3 중첩 README 해시 불일치가 실제로 존재하기 때문이다. 정상 siteq 상태 25/8·24/9와 모든 행 대조, 기대 키 일치는 결과 JSON에서 각각 분리되어 있다. 검토자 스크립트의 초기 로그 패딩 정규식 오차는 고친 뒤 재계산했으며 대상 데이터/코드 결함으로 세지 않았다.

전체 HOLD와 실제 연구·등록 R·봉인·발사 미승인 경계는 유지한다.
