# Gate75 회신 — 부분 수용 / 전체 종결 보류

대상 HEAD `ef6689bbe296e545df57dc481e45ec98c2b9ea3b`, 코드 `ebfb853d1b3dff0678f5f67985003498a3476982`, 독립 RUN_SCOPE 57 파일 `27390883eb132941`, 코드→HEAD diff 0.

**R1/R2·고정 캐시 gate·producer/validator 분리를 수용한다. 잔여 P1 1건·P2 2건만 다음 유한 보완 대상이다. 기존 Gabia 결과와 보존 묶음을 무효화하지 않으며 새 본 계산은 필요하지 않다.**

1. **G75-N1/P1 — index 최종화 실패의 rc 소실.** `archive_results.sh:294` 최종 Python 호출은 실패를 검사하지 않고, `:425`는 n_bad/n_missing만 본다. 실제 index heredoc의 replace 실패는 예외·옛 index 불변이지만, index 명령 rc17을 주입한 원래 shell 경계는 rc0·불완전0·commit 안내로 끝났다. write/replace 실패를 부모 nonzero와 명시적 미완으로 전파하고, 이미 승격된 상태가 있으면 숨기지 말 것. 실제 전체 archive는 실행하지 않은 격리 경계 재현이다.
2. **G75-N2/P2 — 중복 YAML 키를 모호한 index로 거부하지 않음.** `:70/:225/:313`의 safe_load는 `runs: {기존항목...}` 뒤 `runs: {}`를 뒤 값으로 접어 preflight rc0으로 받는다. 같은 run 이름/identity 키 중복도 동일하다. 최종 writer는 접힌 내용을 써 무관 항목을 잃는다. 진입·동명·병합의 동일한 중복 거부 정책과 첫 승격 전 원문 불변 회귀를 요구한다.
3. **G75-N3/P2 — 진단 소비자의 잘못된 out 누락.** 원장 사본의 grid_fit_v5 `evidence.out`만 `results/OTHER_RUN`으로 변경하면 `_scope_problems + _no_active_claim_evidence_problems=[]`이고 generic full_bundle lint도 통과한다. 동일한 실물 receipt/bundle의 bound run을 사용한 기존 `_assert_ledger_run_bound`는 거부한다. 새 소비자가 기존 결속 규칙을 재사용하도록 연결하고 정상/부재/공백/다른 out을 시험할 것. attach 자체는 이미 보호돼 있으며 이를 재설계하라는 요청이 아니다.

§5 답:

- ① 1/2/4/6 수용, 3은 N3·5는 N1/N2가 남아 전체 종결 보류.
- ② 현재 진단 전용·명부 분리 범위에서 row_projection 불변 수용. g18 재게시/복원을 요구하지 않는다. 단 publisher가 새 분류를 직접 강제한다는 주석/설명은 정정한다. 향후 claim/투영 편입은 별건이다.
- ③ grid_fit_v5 `current_validated` 유지 가능. producer c2ef… / validator 273908… / diagnostic / no_active_claim을 함께 기록하고 재계산·과학적 정본으로 확대하지 않는다. v4 과거 상태를 자동 변경하지 않는다.
- ④ 새 본 실행 불필요. 위 세 경계는 작은 격리 회귀로 확인한다. 미래 본 실행·캐시 계산·archive 게시·복원·receipt 재검증은 각각 필요한 승인 범위로 구분한다.

문구도 좁힐 것: 최종 1,922 PASS는 7ec4e234이며 SEND의 첫 8765068a와 구별한다. index 재직렬화는 entry 값 보존이지 raw 바이트 보존이 아니다. planner는 같은 startability 함수를 직접 부르지 않으므로 “같은 정책”과 “공유 함수”를 구분한다.

독립 대조: 기존 index/묶음/등록부/CLAIM_STATUS/publisher/g18 바이트 불변, 옛 receipt history 바이트 동일, 새 core 재해시 및 validation/outputs 동일. 수신자는 전체 suite/restore/재채점/COMSOL을 돌리지 않았다. 검토자 AST·heredoc·shell 경계 23 고유 사례와 원자료를 동봉한다. sender의 전체 PASS 보고와 합산하지 않는다.

이 회신은 코드 수정·시험·실행 승인문이 아니다. 다음 사용자 승인을 요청할 때 범위를 **N1/N2/N3 + 문구 정정**으로 한정한다. 기존 결과·실패·R1 편차·원장·영수증 원문은 보존한다.
