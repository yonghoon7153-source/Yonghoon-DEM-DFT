# 55차 준비 — lifecycle 경로의 신뢰 경계를 긋는다 (착수 전 초안)

**상태**: 초안. **아직 코드에 반영하지 않았다.** 54차 판정이 `d824ecf8` 로
나가 있는 동안 RUN_SCOPE(`src/ tools/ configs/ scripts/ run.sh
requirements*.txt`)를 건드리면 리뷰 대상 커밋이 그 자리에서 무효가 된다.
이 문서는 `docs/` 라 code identity 를 움직이지 않는다.

**결정이 필요한 곳은 §4 하나다** — 나머지는 그 결정이 나오면 기계적으로 쓴다.

---

## §1 왜 이 문서가 있나

54라운드째 같은 축에서 P0 가 나온다. 54차 P0 여섯 중 넷이 "authority 가
둘" 이었고 그건 한 함수로 모아 닫았다 — 그 종류는 수렴한다. 닫히지 **않는**
종류는 따로 있다:

> 원장·journal·anchor·`.FROZEN` 에 쓸 수 있는 주체를 적대자로 두면
> 표면이 유한하지 않다.

이건 새 발견이 아니다. **44차에 이미 확정됐다** (계약 §13.3.1):

> 39~43차 게이트 리뷰에서 cohort 게시 경로는 "적대적 same-process/namespace
> writer" 를 위협 모델에 두고 검사를 계속 늘렸다. 44차에 그 중 하나가
> **검사 횟수로 닫히지 않는다**는 것이 확정됐다.

그때 택한 답은 검사를 더 늘리는 것이 아니라 **보장을 철회하고 전제를 적는
것**이었고, 정본은 `row_projection.py:1749` 의 `_TRUST_BOUNDARY` 다.
`test_the_publisher_declares_its_trust_boundary` 가 계약서와 코드가 갈라지지
않게 붙들고 있다.

**그 처리가 게시 경로에만 있다.** `tools/preserve.py` 에는 `_TRUST_BOUNDARY`
가 없다. §13.3.1 을 곁다리로 두 번 인용할 뿐이다 —
`preserve.py:4411`(네트워크 파일시스템은 전제 밖) ·
`preserve.py:4821`(같은 uid 의 다른 process 는 token 을 읽는다). 개별 한계에
단 각주이지, 경로 전체의 위협 모델 선언이 아니다.

그래서 발급·동결·원장 경로는 위협 모델이 **무한한 채로** 리뷰를 받고 있고,
우리는 매 라운드 요청문 §0 에 표면을 **신고만** 한다. 신고는 범위를 좁히지
않는다.

---

## §2 현재 신고 중인 표면의 triage

요청문 §0 "남아 있는 표면" 각 항을, **무엇이 그것을 닫는가**로 나눈다.

| # | 표면 | 닫는 것 | 비고 |
|---|---|---|---|
| 1 | 원장·journal·anchor·`.FROZEN` 전부에 쓸 수 있는 주체는 역사를 다시 쓸 수 있다 | **전제** 또는 별도 OS principal | 44차가 게시 쪽에서 내린 결론과 동일한 형태 |
| 2 | 소유 증명 token(0600)을 같은 uid 의 다른 process 가 읽는다 | **전제** 또는 별도 principal | `preserve.py:4821` 이 이미 "§13.3.1 과 같은 경계" 라고 적었다 — 선언만 없다 |
| 3 | `flock` 은 같은 기계·같은 파일시스템 안에서만 배타 | **전제** 또는 provider CAS | `preserve.py:4411` 이 이미 각주로 달았다 |
| 4 | `freezing` 은 원장 한 필드 — 원장에 쓸 수 있으면 되돌린다 | **전제** (1과 같은 뿌리) | 54차에 durable 로 만든 것이지 위조 불가로 만든 것이 아니다 |
| 5 | 변이 증거의 pytest report 를 손으로 위조하면 checker 를 통과 | **독립 replay** (기계) | 전제로 뺄 것이 아니다 — checker 가 스스로 재생하면 닫힌다 |
| 6 | 실행된 source bytes 를 측정하는 주체가 측정 대상 안에 있다 | **trusted launcher** (기계, P0-8) | 전제로 빼면 provenance 주장 자체가 약해진다 |

**핵심 구분**: 1~4 는 "누가 이 기계에서 무엇을 할 수 있는가" 의 문제이고
검사로 안 닫힌다 — 44차 결론이 그대로 적용된다. 5~6 은 **만들면 닫힌다**.
지금은 여섯 개가 §0 에 같은 무게로 섞여 있어서, 리뷰어 입장에서 어느 것이
"안 한 것" 이고 어느 것이 "못 하는 것" 인지 구분되지 않는다.

---

## §3 전제 초안 (게시 쪽 `_TRUST_BOUNDARY` 를 본뜬 것)

코드에 넣을 자리: `tools/preserve.py` 모듈 상수. 계약서 §13.3.1 옆에 새 절.

```
_TRUST_BOUNDARY = """보존 원장(`LEG_PRESERVATION.yaml`)·실행권
디렉터리(`<ledger>/_claims/`)·소유 증명 파일·lifecycle journal 과 그
anchor 는 **하나의 OS principal 이 소유**하고, 그것들을 바꾸는 모든
writer 는 공개 lifecycle API(`open_leg_run`·`attach_leg_run`·
`claim_planned_leg`·`finalize_leg`·`release_leg_run`·`resume_claim`)를
지나 `LOCK_ORDER = ("attempt_path", "claim", "ledger")` 를 따른다.
비협조적 writer — 같은 principal 로 lock 없이 원장·claim·journal 을
직접 고치는 코드, 소유 증명 경로를 교체하는 코드 — 는 지원 범위
**밖**이다. 배타는 같은 기계의 `flock` 이므로 네트워크 파일시스템과
컨테이너 경계 밖의 동시 발급자도 범위 밖이다."""
```

동결 쪽(`row_projection.py` 의 `freeze_cohort`·`read_lifecycle`·
`backfill_frozen_markers`)은 같은 원장·journal 을 만지므로 **같은 전제**를
가리켜야 한다. 두 파일에 문구를 복제하면 그 순간 authority 가 둘이 된다 —
54차에 네 번 만난 바로 그 실수다. 한쪽이 정본이고 다른 쪽은 참조한다.

**강제 시험** (게시 쪽 `test_the_publisher_declares_its_trust_boundary` 를 본뜸):

- `preserve._TRUST_BOUNDARY` 가 존재하고 `principal`·`LOCK_ORDER`·`밖` 을 담는다
- 계약서가 그 상수 이름을 가리킨다 (산문과 코드가 갈라지지 않게)
- 계약서가 **무엇을 철회했는지** 적는다
- `row_projection` 쪽이 문구를 복제하지 않고 참조한다

---

## §4 결정이 필요한 것 — **이건 내가 정할 수 없다**

전제는 **실제 배포 형태에서 참일 때만** 적을 수 있다. 44차가 정당했던 이유는
배포가 진짜로 단일 기계·단일 principal·CAS provider 없음이었기 때문이다.
GO 를 받으려고 범위를 줄이는 것은 게이트를 속이는 것이다.

그러므로 답해야 할 것:

1. **이 원장·claim·journal 을 쓸 수 있는 OS principal 이 실제로 하나인가?**
   (본 실행이 도는 기계에서, 그 디렉터리에 write 권한을 가진 uid 가 몇인가)
2. **본 실행이 네트워크 파일시스템 위에서 도는가?** (`flock` 전제가 참인가)
3. **적대자를 상정해야 하는 실제 이유가 있는가?** 즉 위협이 "내가 실수로 내
   결과를 덮어쓴다" 인가, "다른 주체가 고의로 증거를 고친다" 인가.

3의 답이 전자라면 §2 의 1~4 를 전제로 빼는 것이 정직하고, 남는 P0 는 5·6 둘로
줄어든다. 후자라면 전제를 적으면 안 되고 별도 principal·CAS 를 **만들어야**
한다 (그건 배포 형태를 바꾸는 일이고 이 저장소 밖 작업을 포함한다).

---

## §5 착수 순서 (54차 판정이 온 뒤)

1. §4 를 답한다.
2. 답이 "전제를 적는다" 면: `_TRUST_BOUNDARY` + 계약 절 + 강제 시험 →
   RUN_SCOPE 가 움직이므로 **cohort 를 g10 으로 넘기고 산출물 재생성**
   (~28분) → 전체 회귀 + strict smoke + 변이 전수 12조각.
3. 그 다음에야 §2 의 5(독립 replay)·6(trusted launcher / P0-8)에 착수한다.
   그 둘은 전제로 못 빼는 것들이고, 51·52·53차 리뷰어가 세 번 권고한 순서의
   ②·③ 이다.
4. 55차 요청문 §0 은 그때 **처음으로** "못 하는 것" 과 "안 한 것" 을 나눠
   적을 수 있다.

**하지 않는 것**: 54차 판정이 오기 전에 RUN_SCOPE 를 건드리는 것.
