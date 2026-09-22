# R17 후속 회신 — 대상 7c8f61f9 — NO-GO

대상 full SHA: `7c8f61f943199c3782bf3c3d81f6b573aa0a1b79`.
이번 검토는 BMS 하네스만이며 COMSOL/게이트 트랙과 별개다. 실데이터 재적합은 하지 않았고 이 회신은 재적합 승인이 아니다.

chain-rule의 1/a 수정·명시 인자와 9개 회귀는 수용한다. absolute run_id 및 legacy None wildcard의 기존 반례도 닫혔다. A/100·A/200·B/100의 GC 원 반례는 A/200 보존을 독립 확인했다. 그러나 “코드 여섯 전부 종결”은 수용하지 못한다.

## 잔여/새 반례 — P1 3건 · P2 2건

1. **P1 GC 경계** — `gc_partial.py:91–98`이 검사하는 것은 index.path지만 `:113–115`의 rmtree는 kind/attempt로 다시 만든다. path는 partial 안에 두고 kind=`..`, attempt=`victim`을 준 합성 index에서 rc0으로 partial 밖 victim이 삭제됐다. 별도로 같은 payload를 참조하는 중복 index에서 보존 항목만 남고 payload는 unlink된다. malformed index의 fail-closed 문제이며 실물 산출 삭제 주장은 아니다. 전체 삭제 대상 검증 + retained 실제 경로 보호가 필요하다.
2. **P1 본문/sidecar 결속** — 유효 SHA를 유지한 채 행만 objective_version=v2, meta는 legacy로 두거나 행 width_tol=.90/meta=.01, cell/run_id 불일치로 두어도 `width_report` rc0. 한 파일 안의 버전 혼합도 통과한다. cycle0.9/1.9는 int(float()) 때문에 [0,1]과 같다. 공유 body/meta 계약과 정수성 검사가 필요하다.
3. **P1 null 동일성** — 양쪽 meta의 git_commit/env/dataset_manifest를 null로, 또는 seed/lb/ub/initial/objective_version을 null로 채우면 rc0 + “동일 확인”. key 존재는 typed 완전성이 아니다. 합법 nullable인 gamma_lb와 필수 값을 구분해야 한다.
4. **P2 근최적 witness** — J≡1, 기본 a_PE상자[1,1.4], ref1.2인데 seed a_PE=10을 주면 LAM_PE min=-733.3333%p/is_lower_bound=true(참 범위±16.6667%p). 별도로 J=1+(a_PE−1)^2, best1.4/실제J1.16/전달best_val1/tol.01이면 feasible 밖 best를 vals에 재삽입해 min=-16.6667%p가 된다(참 min+8.3333%p). `_width_fields`도 measured. 모든 후보에 finite/bounds/feasibility를 적용하고 best_val 결속이 필요하다. 정상 실데이터 multistart가 잘못됐다는 주장은 아니다.
5. **P2 receipt 완전성** — 실제 commit/tree/blob인 영수증에서 runtime=null/문자열, materialized=17, produced_utc=not-a-date, package.digest=not-a-digest 각각을 넣으면 rc0/verified=true. 실제 r11 writer도 package_digest()가 돌려준 상태 dict를 str로 digest에 넣는다. 파일명이 같고 bytes가 다른 두 정상 합성 패키지가 모두 `{'one.txt': 'ok'}`라는 package.digest를 갖고 검증을 통과했다. 공유 nested schema와 실제 package content digest를 연결해야 한다. 공개 checksum 재계산을 암호학적 위조나 전체 replay 우회로 부풀리지 않는다.

재현은 동봉 `repro_followup.py --target <고정 checkout>/bms-balancing` 한 번이다. case별 로그와 `REPRO_RESULTS.json`에 명령/입력/실제 결과가 있다. 정상·거부 대조군도 포함한다. 대상 소스는 수정하지 않았다.

## 시험과 문서 주의

- 표적 3파일: **56 passed, 3 failed / 151.09초**. 실패 셋은 GC fixture 두 개와 width CLI 한 개의 `fcntl` 부재다. chain-rule 9개는 모두 통과했다.
- Windows 전체: **318 passed, 108 failed / 952.84초**. 79건 trace에 fcntl, 16건 Bash 부재, 나머지 4건 링크 권한/파일명/경로 구분자가 관측됐다. **9건은 원인 미확정**이며 runner 격리·skip-worktree 검출 실패 등도 포함한다. 전부 환경 문제로 돌리지 않았다. TEST_STATUS와 full_failures.json을 보고, 지원 환경 동일 SHA 전수 로그와 미확정 9건의 항목별 설명/재현을 제공할 것. 작성자 Linux 426 passed와 섞지 않는다.
- `test_r17_11`은 tol=-.5 검사에 걸려 objective 호출0회다. 공집합 분기 회귀로는 부족하다. 정상 tol에서 진짜 공집합이 RuntimeError가 되는 것은 독립 확인했다.
- cr_04의 잡음 입력은 버전마다 RNG를 다시 소비해 서로 다르다. v2 절대 허용 시험은 유효하지만 두 버전 간 오차차를 단일 축 개선으로 읽으면 안 된다. 입력 배열을 먼저 고정해 공유할 것.
- 과학 정정의 취지는 수용한다. 다만 BML_R1_RESPONSE §14-7의 현재 요약은 아직 “부호 식별을 잃는다”, 원인을 닫았다고 말한다. 원문 보존은 하되 최종 유효 요약에 철회를 연결할 것. 이를 별도 새 P1로 중복 집계하지 않았다.

위 다섯 조건의 독립 반례를 닫은 뒤 다시 코드 수용을 판정하자. UNKNOWN_BLOCKERS 정본화·실데이터 A/B 미실행은 이미 신고된 항목으로 유지하며 새 발견 수에 넣지 않는다. 실제 데이터의 숫자를 바꾸는 작업은 목적·입력·버전·자원·종료 조건을 고정해 사용자에게 별도 승인받아야 한다.
